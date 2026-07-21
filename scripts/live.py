"""Live performance mode: stream Magenta RT 2 while tweaking the mix in real time.

A generator thread produces 1s chunks (state carried over, so the music never
stops) and re-reads the shared params every chunk; a browser control panel
(live.html, served on --port) changes them mid-stream:

  w_audio    blend between env-audio embedding and text embedding (1.0 = pure env)
  env_gain   raw environmental recording layer volume
  gen_gain   generated layer volume
  drums      -1 masked / 0 off / 1 on
  env        which sample the env layer + audio embedding use
  prompt     text prompt (re-embedded on change)

Audio goes straight to the default output device (sounddevice).

Usage:
  python scripts/live.py            # -> open http://localhost:8241
  python scripts/live.py --record   # also dump the session to out/live_<n>.wav on exit
"""
import argparse
import json
import queue
import signal
import threading
import time
import numpy as np
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from magenta_rt.audio import Waveform
from magenta_rt.mlx.system import MagentaRT2SystemMlxfn

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"
OUT = ROOT / "out"

SR = 48000
FPS = 25
CHUNK_FRAMES = 50           # 2s per chunk: fewer calls = less overhead (1s chunks ran ~0.9x)
CHUNK_SAMPLES = SR * CHUNK_FRAMES // FPS
MAX_STYLE_SECONDS = 20
QUEUE_CHUNKS = 3            # generation self-paces against playback via this buffer
PREBUFFER_CHUNKS = 2        # wait for this many chunks before (re)starting playback

PARAMS = {
    "playing": True,
    "w_audio": 1.0,
    "env_gain": 1.0,
    "gen_gain": 0.3,
    "drums": -1,
    "env": "rain_long.wav",
    "prompt": "ambient techno with deep sub bass, hypnotic",
}
STATUS = {"ready": False, "chunks": 0, "underruns": 0, "buffer": 0,
          "env_rms": 0.0, "gen_rms": 0.0, "applied": dict(PARAMS)}
LOCK = threading.Lock()
STOP = threading.Event()


def set_params(update):
    ok = {}
    with LOCK:
        for k, v in update.items():
            if k == "playing":
                PARAMS[k] = bool(v)
            elif k in ("w_audio", "env_gain", "gen_gain"):
                PARAMS[k] = float(np.clip(v, 0.0, 1.5 if k != "w_audio" else 1.0))
            elif k == "drums" and v in (-1, 0, 1):
                PARAMS[k] = int(v)
            elif k == "env" and (SAMPLES / str(v)).exists() and str(v).endswith(".wav"):
                PARAMS[k] = str(v)
            elif k == "prompt" and isinstance(v, str) and 0 < len(v) < 200:
                PARAMS[k] = v
            else:
                continue
            ok[k] = PARAMS[k]
    return ok


class EnvPlayer:
    """Loops an env recording, remembers position across source switches."""
    def __init__(self):
        self.cache, self.pos, self.name = {}, 0, None

    def chunk(self, name):
        if name not in self.cache:
            x = Waveform.from_file(str(SAMPLES / name)).samples
            if x.ndim == 1:
                x = np.stack([x, x], axis=1)
            self.cache[name] = x
        if name != self.name:
            self.name, self.pos = name, 0
        x = self.cache[name]
        idx = (self.pos + np.arange(CHUNK_SAMPLES)) % len(x)
        self.pos = (self.pos + CHUNK_SAMPLES) % len(x)
        return x[idx]


def generator(audio_q, record):
    # MLX streams are bound to the thread that created them, so the model MUST
    # be loaded and run entirely inside this thread.
    t0 = time.time()
    print("Loading MagentaRT2SystemMlxfn (mrt2_base)...", flush=True)
    mrt = MagentaRT2SystemMlxfn(size="mrt2_base")
    print(f"Model ready in {time.time()-t0:.1f}s", flush=True)
    with LOCK:
        STATUS["ready"] = True

    # Embeds run in their own worker thread (MusicCoCa is TFLite, not MLX, so it
    # is safe off this thread): a prompt/source change must NOT stall generation,
    # or the few-second embed drains the buffer and the audio glitches. Until the
    # new embedding is ready we keep playing with the previous style.
    emb_cache, requested = {}, set()
    embed_q = queue.Queue()

    def embed_worker():
        while not STOP.is_set():
            key = embed_q.get()
            if key is None or key in emb_cache:
                continue
            try:
                if key.endswith(".wav"):
                    wav = Waveform.from_file(str(SAMPLES / key))
                    n = min(len(wav.samples), wav.sample_rate * MAX_STYLE_SECONDS)
                    emb_cache[key] = mrt.embed_style(Waveform(wav.samples[:n], wav.sample_rate))
                else:
                    emb_cache[key] = mrt.embed_style(key)
            except Exception as e:
                print(f"embed error for {key!r}: {e}", flush=True)

    threading.Thread(target=embed_worker, daemon=True).start()

    def request(key):
        if key not in emb_cache and key not in requested:
            requested.add(key)
            embed_q.put(key)

    # initial embeddings must exist before the first chunk
    with LOCK:
        request(PARAMS["env"])
        request(PARAMS["prompt"])
    while not (PARAMS["env"] in emb_cache and PARAMS["prompt"] in emb_cache):
        time.sleep(0.1)

    env_player = EnvPlayer()
    state = None
    prev_gains = None
    emb_a = emb_t = None
    while not STOP.is_set():
        with LOCK:
            p = dict(PARAMS)
        request(p["env"])
        request(p["prompt"])
        emb_a = emb_cache.get(p["env"], emb_a)
        emb_t = emb_cache.get(p["prompt"], emb_t)
        w = p["w_audio"]
        emb = (w * emb_a + (1 - w) * emb_t).astype(emb_a.dtype)

        wav, state = mrt.generate(
            style=emb, frames=CHUNK_FRAMES, state=state,
            drums=None if p["drums"] == -1 else [p["drums"]],
        )
        gen = wav.samples
        env = env_player.chunk(p["env"])

        # per-chunk linear gain ramps (prev -> target) to avoid zipper noise
        if prev_gains is None:
            prev_gains = (p["env_gain"], p["gen_gain"])
        ramp = np.linspace(0, 1, CHUNK_SAMPLES)[:, None]
        g_env = prev_gains[0] + (p["env_gain"] - prev_gains[0]) * ramp
        g_gen = prev_gains[1] + (p["gen_gain"] - prev_gains[1]) * ramp
        prev_gains = (p["env_gain"], p["gen_gain"])

        y = np.clip(gen * g_gen + env * g_env, -1.0, 1.0).astype(np.float32)
        with LOCK:
            STATUS["chunks"] += 1
            STATUS["env_rms"] = float(np.sqrt(((env * g_env) ** 2).mean()))
            STATUS["gen_rms"] = float(np.sqrt(((gen * g_gen) ** 2).mean()))
            STATUS["applied"] = p
        if record is not None:
            record.append(y)
        audio_q.put(y)  # blocks when QUEUE_CHUNKS ahead -> self-pacing
    audio_q.put(None)


def player(audio_q):
    import sounddevice as sd
    block = SR // 4
    buf = np.zeros((0, 2), dtype=np.float32)
    filling = True  # rebuffering: play silence until PREBUFFER_CHUNKS are queued
    with sd.OutputStream(samplerate=SR, channels=2, dtype="float32") as out:
        while True:
            with LOCK:
                playing = PARAMS["playing"]
            if not playing:
                # paused: emit silence, don't consume the queue. The bounded queue
                # then blocks the generator, so generation pauses too; resume is
                # instant because the buffer stays full.
                out.write(np.zeros((block, 2), dtype=np.float32))
                continue
            if filling and audio_q.qsize() >= PREBUFFER_CHUNKS:
                filling = False
            if not filling:
                while len(buf) < block:
                    try:
                        item = audio_q.get_nowait()
                    except queue.Empty:
                        break
                    if item is None:
                        return
                    buf = np.concatenate([buf, item])
            with LOCK:
                STATUS["buffer"] = round(
                    (audio_q.qsize() * CHUNK_SAMPLES + len(buf)) / SR, 1)
            if len(buf) >= block:
                out.write(np.ascontiguousarray(buf[:block]))
                buf = buf[block:]
            else:
                # ran dry: count it once, then hold silence until the buffer refills
                with LOCK:
                    if not filling and STATUS["chunks"] > PREBUFFER_CHUNKS:
                        STATUS["underruns"] += 1
                filling = True
                out.write(np.zeros((block, 2), dtype=np.float32))


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/live.html"):
            body = (ROOT / "live.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/state":
            with LOCK:
                self._json({"params": dict(PARAMS), "status": dict(STATUS)})
        elif self.path == "/sources":
            self._json(sorted(p.name for p in SAMPLES.glob("*.wav")))
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/set":
            n = int(self.headers.get("Content-Length", 0))
            try:
                update = json.loads(self.rfile.read(n))
                self._json({"ok": set_params(update)})
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                self._json({"error": str(e)}, 400)
        else:
            self._json({"error": "not found"}, 404)

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=8241)
    ap.add_argument("--record", action="store_true", help="save session to out/ on exit")
    args = ap.parse_args()

    record = [] if args.record else None
    audio_q = queue.Queue(maxsize=QUEUE_CHUNKS)
    threading.Thread(target=generator, args=(audio_q, record), daemon=True).start()
    threading.Thread(target=player, args=(audio_q,), daemon=True).start()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    def _term(*_a):
        raise KeyboardInterrupt  # so SIGTERM also reaches the finally: (saves --record)
    signal.signal(signal.SIGTERM, _term)
    print(f"Live control: http://localhost:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        STOP.set()
        if record:
            OUT.mkdir(exist_ok=True)
            path = OUT / f"live_{int(time.time())}.wav"
            Waveform(np.concatenate(record), SR).write(str(path))
            print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
