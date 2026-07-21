"""Magenta RT 2 live mode: env recording + generated layer, mixed in realtime.

python scripts/live.py [--record]  ->  control panel at http://localhost:8241
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
CHUNK_FRAMES = 50           # 2s; 1s chunks had too much per-call overhead
CHUNK_SAMPLES = SR * CHUNK_FRAMES // FPS
MAX_STYLE_SECONDS = 20      # audio fed to MusicCoCa
QUEUE_CHUNKS = 4
PREBUFFER_CHUNKS = 3

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

    def chunk(self, name, n):
        if name not in self.cache:
            x = Waveform.from_file(str(SAMPLES / name)).samples
            if x.ndim == 1:
                x = np.stack([x, x], axis=1)
            self.cache[name] = x.astype(np.float32)
        if name != self.name:
            self.name, self.pos = name, 0
        x = self.cache[name]
        idx = (self.pos + np.arange(n)) % len(x)
        self.pos = (self.pos + n) % len(x)
        return x[idx]


def generator(audio_q):
    # MLX: inference only works on the thread that loaded the model
    t0 = time.time()
    print("Loading MagentaRT2SystemMlxfn (mrt2_base)...", flush=True)
    mrt = MagentaRT2SystemMlxfn(size="mrt2_base")
    print(f"Model ready in {time.time()-t0:.1f}s", flush=True)
    with LOCK:
        STATUS["ready"] = True

    # embeds take seconds -> run off-thread, keep using the old style until ready
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

    with LOCK:
        request(PARAMS["env"])
        request(PARAMS["prompt"])
    while not (PARAMS["env"] in emb_cache and PARAMS["prompt"] in emb_cache):
        time.sleep(0.1)
    for p in sorted(SAMPLES.glob("*.wav")):  # pre-embed so source switches are instant
        request(p.name)

    # raw gen chunks only; env layer and gains are mixed in the player
    state = None
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
        with LOCK:
            STATUS["chunks"] += 1
            STATUS["applied"] = p
        audio_q.put(wav.samples.astype(np.float32))  # blocks when full
    audio_q.put(None)


def player(audio_q, record):
    """Playback-side mix: env layer never stalls, gen layer fades out when starved."""
    import sounddevice as sd
    block = SR // 4
    env_player = EnvPlayer()
    gen_buf = np.zeros((0, 2), dtype=np.float32)
    filling = True
    prev = None
    with sd.OutputStream(samplerate=SR, channels=2, dtype="float32") as out:
        while True:
            with LOCK:
                p = dict(PARAMS)
            if not p["playing"]:
                # don't consume while paused -> full queue blocks the generator too
                out.write(np.zeros((block, 2), dtype=np.float32))
                continue

            if filling and audio_q.qsize() >= PREBUFFER_CHUNKS:
                filling = False
            if not filling:
                while len(gen_buf) < block:
                    try:
                        item = audio_q.get_nowait()
                    except queue.Empty:
                        break
                    if item is None:
                        return
                    gen_buf = np.concatenate([gen_buf, item])

            if len(gen_buf) >= block:
                gen = gen_buf[:block]
                gen_buf = gen_buf[block:]
            else:
                # gen starved: fade out and rebuffer (env keeps playing)
                if not filling:
                    filling = True
                    with LOCK:
                        if STATUS["chunks"] > PREBUFFER_CHUNKS:
                            STATUS["underruns"] += 1
                gen = np.zeros((block, 2), dtype=np.float32)
                if len(gen_buf):
                    fade = np.linspace(1, 0, len(gen_buf))[:, None]
                    gen[: len(gen_buf)] = gen_buf * fade
                    gen_buf = gen_buf[:0]

            env = env_player.chunk(p["env"], block)

            # ramp gains within the block to avoid zipper noise
            if prev is None:
                prev = (p["env_gain"], p["gen_gain"])
            ramp = np.linspace(0, 1, block)[:, None]
            g_env = prev[0] + (p["env_gain"] - prev[0]) * ramp
            g_gen = prev[1] + (p["gen_gain"] - prev[1]) * ramp
            prev = (p["env_gain"], p["gen_gain"])

            y = np.clip(gen * g_gen + env * g_env, -1.0, 1.0).astype(np.float32)
            with LOCK:
                STATUS["buffer"] = round(
                    (audio_q.qsize() * CHUNK_SAMPLES + len(gen_buf)) / SR, 1)
                STATUS["env_rms"] = float(np.sqrt(((env * g_env) ** 2).mean()))
                STATUS["gen_rms"] = float(np.sqrt(((gen * g_gen) ** 2).mean()))
            if record is not None:
                record.append(y)
            out.write(np.ascontiguousarray(y))


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            # UI is built entirely by live.js (defer: body must exist first)
            body = b'<!doctype html><meta charset="utf-8"><script defer src="/live.js"></script>'
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/live.js":
            body = (ROOT / "live.js").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/javascript; charset=utf-8")
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
    threading.Thread(target=generator, args=(audio_q,), daemon=True).start()
    threading.Thread(target=player, args=(audio_q, record), daemon=True).start()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    def _term(*_a):
        raise KeyboardInterrupt  # let SIGTERM save --record too
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
