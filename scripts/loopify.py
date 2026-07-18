"""Make seamless loops from generated clips: equal-power crossfade of tail into head.

Usage: python scripts/loopify.py out/*.wav   (writes *_loop.wav next to each input)
"""
import sys
import numpy as np
import soundfile as sf
from pathlib import Path

FADE_S = 0.5  # crossfade length in seconds

def loopify(path: Path):
    x, sr = sf.read(str(path))
    if x.ndim == 1:
        x = x[:, None]
    n_fade = int(FADE_S * sr)
    if len(x) < 3 * n_fade:
        print(f"skip (too short): {path.name}")
        return
    head, tail = x[:n_fade], x[-n_fade:]
    t = np.linspace(0, np.pi / 2, n_fade)[:, None]
    blended = tail * np.cos(t) ** 2 + head * np.sin(t) ** 2
    y = np.concatenate([blended, x[n_fade:-n_fade]])
    out = path.with_name(path.stem + "_loop.wav")
    sf.write(str(out), y, sr)
    print(f"{path.name} -> {out.name} ({len(y)/sr:.2f}s loop)")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        if "_loop" not in p:
            loopify(Path(p))
