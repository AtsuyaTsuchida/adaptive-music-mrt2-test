# env-sound-music

環境音（ノイズ）を音楽に変換する実験プロジェクト。
Google **Magenta RealTime 2**（MLXバックエンド、Apple Siliconネイティブ）を使用。

## 構成

- `docs/survey_environmental_sound_music.md` — 環境音→音楽のサーベイ（アート作品・研究・製品）
- `samples/` — 環境音素材（Wikimedia Commons のCC音源、`*.ogg` が原本。出典は [CREDITS.md](CREDITS.md)）
  - rain(雨+雷) / ocean(波) / subway(トロント地下鉄) / station(駅トンネル) / birds(鳥)
  - wav版は `scripts/prepare_samples.sh` で生成（リポジトリには含まない）
- `scripts/audio2audio.py` — メイン実験。環境音→MusicCoCaスタイル埋め込み→生成
- `scripts/loopify.py` — 生成クリップを等パワークロスフェードでシームレスループ化
- `listen.html` — 試聴ページ（原音と生成の比較＋リアルタイムビジュアライザー）。`python3 -m http.server 8240` で配信
- `out/` — 生成結果（8秒クリップと `*_loop.wav` シームレスループ）

## セットアップ / 実行

```bash
source .venv/bin/activate           # Python 3.12 + magenta-rt[mlx]
python scripts/audio2audio.py       # 全実験を実行（mrt2_base, 8-bit）
python scripts/loopify.py out/*.wav # ループ化
```

モデル本体は `~/Documents/Magenta/magenta-rt-v2/`（`MAGENTA_HOME`で変更可）。

## audio2audioの仕組み（MRT2のPython API）

MRT2の生成は **スタイル埋め込み条件付け**。`MusicCoCa.embed()` がテキストと
音声（`Waveform`）を同一の768次元空間に埋め込むため:

1. **A: audio-only** — 環境音の埋め込みをそのままstyleに → その音の「雰囲気」の音楽
2. **B: blend** — 環境音埋め込みとテキストプロンプト埋め込みの加重平均 → 「雨っぽいアンビエントテクノ」等
3. **C: blend + drums=1** — drums条件を立ててリズミックでループ向きの出力に

入力音声の波形そのものを引き継ぐ継続生成（真のaudio continuation）はPython APIには
無く、ライブのaudio-inジャムはC++アプリ（AUv3/Jamアプリ）側の機能。
