"""Audio2audio experiments: environmental sounds -> musical loops via Magenta RT 2 (MLX).

For each environmental sample:
  A) audio-only style conditioning  (music "in the vibe of" the noise)
  B) blend: env-audio embedding x text-prompt embedding (weighted average)
  C) blend + drums=1 (force a rhythmic, loopable result)
"""
import sys
import time
import numpy as np
from pathlib import Path

from magenta_rt.audio import Waveform
from magenta_rt.mlx.system import MagentaRT2SystemMlxfn

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

DUR_S = 8            # seconds per generation
FPS = 25             # frames per second (25 frames = 1s @ 48kHz)
MAX_STYLE_SECONDS = 20  # only feed the first N seconds of the env sound to MusicCoCa

# (sample file, text prompt to blend with, audio weight for blend)
EXPERIMENTS = [
    ("rain.wav",    "ambient techno with deep sub bass, hypnotic", 0.5),
    ("ocean.wav",   "slow evolving ambient pads, generative music", 0.5),
    ("subway.wav",  "industrial percussion loop, dark techno", 0.5),
    ("station.wav", "minimal glitch electronica", 0.5),
    ("birds.wav",   "flute and marimba melody, jazz trio", 0.5),
]

def main():
    t0 = time.time()
    print("Loading MagentaRT2SystemMlxfn (mrt2_base exported)...", flush=True)
    mrt = MagentaRT2SystemMlxfn(size="mrt2_base")
    print(f"Model loaded in {time.time()-t0:.1f}s", flush=True)

    def gen(style_emb, name, drums=None):
        t = time.time()
        wav, _ = mrt.generate(style=style_emb, frames=DUR_S * FPS, drums=drums)
        path = OUT / f"{name}.wav"
        wav.write(str(path))
        print(f"  {name}: {time.time()-t:.1f}s -> {path.name}", flush=True)

    # Baseline sanity check (text only)
    emb_text_baseline = mrt.embed_style("disco funk")
    gen(emb_text_baseline, "00_baseline_text_disco_funk")

    for fname, prompt, w_audio in EXPERIMENTS:
        stem = Path(fname).stem
        print(f"== {stem} (prompt: {prompt}) ==", flush=True)
        wav_in = Waveform.from_file(str(SAMPLES / fname))
        n = min(len(wav_in.samples), wav_in.sample_rate * MAX_STYLE_SECONDS)
        wav_in = Waveform(wav_in.samples[:n], wav_in.sample_rate)

        emb_audio = mrt.embed_style(wav_in)
        emb_text = mrt.embed_style(prompt)

        # A) audio-only style
        gen(emb_audio, f"{stem}_A_audio_only")

        # B) weighted blend of audio and text embeddings
        emb_blend = np.average(
            np.stack([emb_audio, emb_text]), axis=0,
            weights=[w_audio, 1.0 - w_audio],
        ).astype(emb_audio.dtype)
        gen(emb_blend, f"{stem}_B_blend{int(w_audio*100)}")

        # C) blend + force drums for a loopable groove
        gen(emb_blend, f"{stem}_C_blend_drums", drums=[1])

    print(f"All done in {time.time()-t0:.1f}s", flush=True)

if __name__ == "__main__":
    main()
