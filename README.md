# env-sound-music

環境音（ノイズ）を音楽に変換する実験プロジェクト。
Google **Magenta RealTime 2**（MLXバックエンド、Apple Siliconネイティブ）を使用。

環境音の中にある「音楽として解釈できる可能性」をAIで増幅・提示し、
聴こえ方そのものを操作する — 生成レイヤー（AIの解釈）と原音レイヤー（現実）の
バランスをリアルタイムで演奏するライブシステム。

## 構成

- `scripts/live.py` + `live.js` — ライブ演奏モード（本体）。UIはJSのみで構築（HTMLファイルなし）
- `docs/survey_environmental_sound_music.md` — 環境音→音楽のサーベイ（アート作品・研究・製品）
- `samples/` — 環境音素材（Wikimedia Commons のCC/PD音源、`*.ogg`/`*.flac` が原本。出典は [CREDITS.md](CREDITS.md)）
  - rain_long(雷雨4分) / birds_long(夜明けのコーラス10分) / ocean_long(湖の波5.5分) / city_long(メキシコシティ5分, Félix Blume)
  - wav版は `scripts/prepare_samples.sh` で生成（リポジトリには含まない）
- `out/` — `--record` 時のセッション録音（gitには含まない）

## セットアップ / 実行

```bash
source .venv/bin/activate           # Python 3.12 + magenta-rt[mlx]
scripts/prepare_samples.sh          # 環境音サンプルを取得・変換（初回のみ）
python scripts/live.py --record     # モデルロード後、音が出始める
open http://localhost:8241          # コントロールパネル
```

モデル本体は `~/Documents/Magenta/magenta-rt-v2/`（`MAGENTA_HOME`で変更可、
`mrt models init && mrt models download mrt2_base` で取得）。

## 仕組み

聴こえる音は2レイヤーのミックス:

1. **原音レイヤー** — 環境音の録音そのもの（ループ再生）
2. **生成レイヤー** — MRT2のストリーム生成。40msフレーム単位の自己回帰で、
   `state` を引き継ぐため音楽は途切れない

生成のスタイル条件は **MusicCoCa埋め込み**（audio/textを同一768次元空間へ）の
加重平均で、これがリアルタイム操作の中心:

| パラメータ | 役割 |
|---|---|
| `w_audio` | 環境音の埋め込み(1.0) ⇄ テキストプロンプト(0.0) のブレンド。Musicalityの操作軸 |
| `env_gain` / `gen_gain` | 原音/生成レイヤーの音量（再生側で適用、反映〜0.25秒） |
| `drums` | 生成へのリズム指示（auto / off / on） |
| `env` | 環境音ソース切替（原音レイヤーと埋め込みの両方が切り替わる） |
| `prompt` | テキストプロンプト（w_audio < 1.0 で効く） |

### 設計メモ

- **MLXはモデルをロードしたスレッドでしか推論できない**（`There is no Stream(gpu, 1)`）
  → モデルは生成スレッド内でロード
- **埋め込み計算は専用ワーカースレッド** — プロンプト/ソース変更で生成を止めない。
  新埋め込みができるまで旧スタイルで演奏継続。全サンプルは起動時にプリフェッチ
- **ミックスは再生側** — 原音レイヤーはただのファイル再生なので生成に依存させない。
  生成が実時間を割ってもAIレイヤーだけがフェードアウトし、環境音は途切れない
  （解釈が後退して現実が残る、という劣化の仕方）
- 生成速度はM3 Maxで実時間の0.85〜1.03倍（マシン負荷・電源状態に依存）。
  **バッテリー駆動はGPUが絞られて実時間を割る**ので電源接続を推奨
- 出力デバイスはストリーム開始時に固定。AirPods等に切り替えたら再起動が必要
