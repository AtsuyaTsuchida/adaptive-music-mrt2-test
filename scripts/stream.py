"""Long-form streaming generation: morph through env-sound x text styles over minutes.

Magenta RT 2 generates frame-by-frame (40ms) with carry-over state, so unlike
one-shot models the style embedding becomes a *continuous control signal*:
we morph it through a sequence of waypoints while the music never stops.

A journey can also overlay the raw environmental recording with its own gain
curve ("env_mix"): the recording is the music at first, and the model's reading
of it gradually takes over (emergence).

Usage:
  python scripts/stream.py                            # default journey -> out/stream_<name>.wav
  python scripts/stream.py --journey rain_emerge      # builtin emergence piece
  python scripts/stream.py --journey scenes/my.json   # custom journey
  python scripts/stream.py --play                     # live playback (pre-buffered) + save
"""
import argparse
import json
import queue
import threading
import time
import numpy as np
from pathlib import Path

from magenta_rt.audio import Waveform
from magenta_rt.mlx.system import MagentaRT2SystemMlxfn

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"
OUT = ROOT / "out"

SR = 48000
FPS = 25                # model frames per second
CHUNK_FRAMES = 50       # style is updated every chunk (2s)
CHUNK_SAMPLES = SR * CHUNK_FRAMES // FPS
MAX_STYLE_SECONDS = 20  # feed at most N seconds of env audio to MusicCoCa

# Default journey: storm -> underground -> open sea -> dawn chorus.
# Each waypoint: time (s), env audio, text prompt, audio weight, drums (-1 masked / 0 off / 1 on).
DEFAULT_JOURNEY = {
    "name": "rain_to_birds",
    "duration": 180,
    "waypoints": [
        {"t": 0,   "audio": "rain_long.wav",   "text": "ambient techno with deep sub bass, hypnotic",  "w_audio": 0.5, "drums": -1},
        {"t": 35,  "audio": "rain_long.wav",   "text": "ambient techno with deep sub bass, hypnotic",  "w_audio": 0.5, "drums": 1},
        {"t": 70,  "audio": "subway.wav", "text": "industrial percussion loop, dark techno",      "w_audio": 0.5, "drums": 1},
        {"t": 110, "audio": "ocean.wav",  "text": "slow evolving ambient pads, generative music", "w_audio": 0.6, "drums": 0},
        {"t": 150, "audio": "birds.wav",  "text": "flute and marimba melody, jazz trio",          "w_audio": 0.5, "drums": -1},
    ],
}

# Emergence: the raw env recording *is* the piece at first, then the model's
# reading of it gradually takes over. env_mix/gen_gain are [t, gain] breakpoints;
# waypoints sweep w_audio 1.0 -> 0.3 (documentary -> musical) with drums late.
EMERGE_JOURNEY = {
    "name": "rain_emerge",
    "duration": 180,
    "env_mix": {"audio": "rain_long.wav",
                "gain": [[0, 1.0], [30, 0.95], [80, 0.7], [130, 0.35], [170, 0.0]]},
    "gen_gain": [[0, 0.0], [15, 0.25], [50, 0.6], [90, 0.9], [120, 1.0]],
    "waypoints": [
        {"t": 0,   "audio": "rain_long.wav", "text": "ambient techno with deep sub bass, hypnotic", "w_audio": 1.0,  "drums": -1},
        {"t": 60,  "audio": "rain_long.wav", "text": "ambient techno with deep sub bass, hypnotic", "w_audio": 0.8,  "drums": -1},
        {"t": 105, "audio": "rain_long.wav", "text": "ambient techno with deep sub bass, hypnotic", "w_audio": 0.55, "drums": -1},
        {"t": 125, "audio": "rain_long.wav", "text": "ambient techno with deep sub bass, hypnotic", "w_audio": 0.45, "drums": 1},
        {"t": 170, "audio": "rain_long.wav", "text": "ambient techno with deep sub bass, hypnotic", "w_audio": 0.3,  "drums": 1},
    ],
}
BUILTINS = {"rain_to_birds": DEFAULT_JOURNEY, "rain_emerge": EMERGE_JOURNEY}


def gain_curve(breakpoints, n_samples):
    """Sample-accurate gain envelope from [t, gain] breakpoints."""
    bp = np.asarray(breakpoints, dtype=np.float64)
    t = np.arange(n_samples) / SR
    return np.interp(t, bp[:, 0], bp[:, 1])[:, None]


def make_mixer(journey, n_samples):
    """Precompute env layer + gain envelopes; return per-chunk mixing closure."""
    gen_env = gain_curve(journey["gen_gain"], n_samples) if journey.get("gen_gain") else None
    env_layer = None
    if journey.get("env_mix"):
        mix = journey["env_mix"]
        x = Waveform.from_file(str(SAMPLES / mix["audio"])).samples
        if x.ndim == 1:
            x = np.stack([x, x], axis=1)
        x = np.tile(x, (int(np.ceil(n_samples / len(x))), 1))[:n_samples]
        env_layer = x * gain_curve(mix["gain"], n_samples)

    def mix_chunk(i, samples):
        s0 = i * CHUNK_SAMPLES
        s1 = s0 + len(samples)
        y = samples
        if gen_env is not None:
            y = y * gen_env[s0:s1]
        if env_layer is not None:
            y = y + env_layer[s0:s1]
        return np.clip(y, -1.0, 1.0).astype(np.float32)

    return mix_chunk


def embed_waypoints(mrt, journey):
    """Resolve each waypoint to a single style embedding (audio x text blend)."""
    cache = {}

    def embed_audio(fname):
        if fname not in cache:
            wav = Waveform.from_file(str(SAMPLES / fname))
            n = min(len(wav.samples), wav.sample_rate * MAX_STYLE_SECONDS)
            cache[fname] = mrt.embed_style(Waveform(wav.samples[:n], wav.sample_rate))
        return cache[fname]

    for wp in journey["waypoints"]:
        emb_a = embed_audio(wp["audio"])
        emb_t = mrt.embed_style(wp["text"])
        w = wp["w_audio"]
        wp["emb"] = np.average(
            np.stack([emb_a, emb_t]), axis=0, weights=[w, 1.0 - w]
        ).astype(emb_a.dtype)
    return journey


def style_at(journey, t):
    """Linearly interpolate waypoint embeddings at time t; drums step at waypoints."""
    wps = journey["waypoints"]
    if t <= wps[0]["t"]:
        return wps[0]["emb"], wps[0]["drums"]
    for a, b in zip(wps, wps[1:]):
        if t < b["t"]:
            u = (t - a["t"]) / (b["t"] - a["t"])
            emb = ((1 - u) * a["emb"] + u * b["emb"]).astype(a["emb"].dtype)
            return emb, a["drums"]
    return wps[-1]["emb"], wps[-1]["drums"]


def stream(mrt, journey, on_chunk):
    """Generate the whole journey chunk by chunk, calling on_chunk(i, samples) per chunk."""
    duration = journey["duration"]
    n_chunks = int(np.ceil(duration * FPS / CHUNK_FRAMES))
    state = None
    t_wall = time.time()
    for i in range(n_chunks):
        t_mid = (i + 0.5) * CHUNK_FRAMES / FPS
        emb, drums = style_at(journey, t_mid)
        wav, state = mrt.generate(
            style=emb, frames=CHUNK_FRAMES, state=state,
            drums=None if drums == -1 else [drums],
        )
        on_chunk(i, wav.samples)
        done = (i + 1) * CHUNK_FRAMES / FPS
        speed = done / (time.time() - t_wall)
        print(f"\r  {done:5.1f}s / {duration}s  ({speed:.2f}x realtime)", end="", flush=True)
    print()
    return n_chunks


def dump_metadata(journey, path):
    """Journey metadata for the visualizer page (embeddings stripped)."""
    meta = {k: v for k, v in journey.items() if k != "waypoints"}
    meta["waypoints"] = [{k: v for k, v in wp.items() if k != "emb"}
                        for wp in journey["waypoints"]]
    path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--journey", help="builtin name (rain_to_birds / rain_emerge) or journey JSON path")
    ap.add_argument("--duration", type=float, help="override journey duration (s)")
    ap.add_argument("--play", action="store_true", help="live playback while generating")
    ap.add_argument("--prebuffer", type=float, default=8.0, help="seconds to buffer before playback starts")
    args = ap.parse_args()

    if args.journey in BUILTINS:
        journey = dict(BUILTINS[args.journey])
    elif args.journey:
        journey = json.loads(Path(args.journey).read_text())
    else:
        journey = dict(DEFAULT_JOURNEY)
    if args.duration:
        journey["duration"] = args.duration

    t0 = time.time()
    print("Loading MagentaRT2SystemMlxfn (mrt2_base)...", flush=True)
    mrt = MagentaRT2SystemMlxfn(size="mrt2_base")
    embed_waypoints(mrt, journey)
    print(f"Model + embeddings ready in {time.time()-t0:.1f}s", flush=True)

    n_chunks = int(np.ceil(journey["duration"] * FPS / CHUNK_FRAMES))
    mix_chunk = make_mixer(journey, n_chunks * CHUNK_SAMPLES)

    chunks = []
    if args.play:
        import sounddevice as sd
        q = queue.Queue()

        def player():
            buf = np.zeros((0, 2), dtype=np.float32)
            with sd.OutputStream(samplerate=SR, channels=2, dtype="float32") as out:
                while True:
                    item = q.get()
                    if item is None:
                        if len(buf):
                            out.write(np.ascontiguousarray(buf))
                        break
                    buf = np.concatenate([buf, item])
                    # write in small blocks so we keep draining the queue
                    while len(buf) >= SR // 2:
                        out.write(np.ascontiguousarray(buf[: SR // 2]))
                        buf = buf[SR // 2:]

        th = threading.Thread(target=player, daemon=True)
        prebuffer_chunks = int(np.ceil(args.prebuffer * FPS / CHUNK_FRAMES))

        def on_chunk(i, samples):
            y = mix_chunk(i, samples)
            chunks.append(y)
            q.put(y)
            if len(chunks) == prebuffer_chunks:
                th.start()

        print(f"Streaming live (prebuffer {args.prebuffer:.0f}s)... Ctrl-C to stop", flush=True)
        try:
            stream(mrt, journey, on_chunk)
        except KeyboardInterrupt:
            print("\nstopped")
        q.put(None)
        if th.is_alive():
            th.join()
    else:
        stream(mrt, journey, lambda i, s: chunks.append(mix_chunk(i, s)))

    if chunks:
        OUT.mkdir(exist_ok=True)
        y = np.concatenate(chunks)
        path = OUT / f"stream_{journey['name']}.wav"
        Waveform(y, SR).write(str(path))
        dump_metadata(journey, path.with_suffix(".json"))
        print(f"wrote {path} ({len(y)/SR:.1f}s) + metadata json")


if __name__ == "__main__":
    main()
