# env-sound-music

環境音（ノイズ）を音楽に変換する実験プロジェクト。
Google **Magenta RealTime 2**（MLXバックエンド、Apple Siliconネイティブ）を使用。

## 構成

- `docs/survey_environmental_sound_music.md` — 環境音→音楽のサーベイ（アート作品・研究・製品）
- `samples/` — 環境音素材（Wikimedia Commons のCC音源、`*.ogg` が原本。出典は [CREDITS.md](CREDITS.md)）
  - rain(雨+雷) / ocean(波) / subway(トロント地下鉄) / station(駅トンネル) / birds(鳥)
  - wav版は `scripts/prepare_samples.sh` で生成（リポジトリには含まない）
- `scripts/audio2audio.py` — メイン実験。環境音→MusicCoCaスタイル埋め込み→生成
- `scripts/stream.py` — 長尺ストリーム生成。stateを引き継ぎながらスタイル埋め込みをウェイポイント間で補間し、数分規模の連続した楽曲を生成（`--play`でライブ再生）
- `emerge.html` — emergence可視化ページ（環境音⇄音楽メーター、ゲイン/w_audioカーブのタイムライン、スペクトログラム）
- `scripts/live.py` + `live.html` — ライブ演奏モード。生成を止めずに w_audio・原音/生成ゲイン・drums・環境音ソース・プロンプトをブラウザから操作
- `scripts/loopify.py` — 生成クリップを等パワークロスフェードでシームレスループ化
- `listen.html` — 試聴ページ（原音と生成の比較＋リアルタイムビジュアライザー）。`python -m RangeHTTPServer 8240` で配信（`http.server`はRange非対応で長尺wavのシークが効かない）
- `out/` — 生成結果（8秒クリップと `*_loop.wav` シームレスループ）

## セットアップ / 実行

```bash
source .venv/bin/activate           # Python 3.12 + magenta-rt[mlx]
python scripts/audio2audio.py       # 全実験を実行（mrt2_base, 8-bit）
python scripts/stream.py            # 3分のストリーム生成（雨→地下鉄→波→鳥）
python scripts/stream.py --play     # 生成しながらライブ再生（M3 Maxでほぼ1.0x）
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

## 長尺ストリーム（stream.py）

MRT2はフレーム単位（40ms）の自己回帰生成で、`generate()` が返す `state` を
次の呼び出しに渡すと**音楽が途切れずに無限に続く**。ワンショット生成のモデル
（Stable Audio等）と違い、スタイル埋め込みが「連続的な制御信号」になるのが本質:

- **ウェイポイント**（時刻 + 環境音×テキストのブレンド + drums条件）を並べ、
  チャンク（2秒）ごとに埋め込みを線形補間 → 曲が鳴り続けたままスタイルがモーフする
- デフォルトのジャーニーは3分で「雨×テクノ → drums-in → 地下鉄×インダストリアル
  → 波×アンビエントパッド → 鳥×ジャズ」と遷移
- `--journey my.json` で任意のジャーニーを定義可（形式は `DEFAULT_JOURNEY` 参照）
- 生成速度はM3 Maxでほぼ実時間（40ms/frame）なので `--play` でライブ演奏になる

### emergence（rain_emerge ジャーニー）

「環境音が徐々に音楽と混ざり、音楽的になっていく」構成。2レイヤーのミックス:

- **原音レイヤー**: 生の雨の録音。`env_mix.gain` のカーブで徐々にフェードアウト（170秒で無音）
- **生成レイヤー**: `gen_gain` で無音からフェードイン。スタイルは w_audio=1.0
  （雨の埋め込みそのもの＝ドキュメンタリー）から 0.3（テキスト寄り＝音楽的）へ補間、
  125秒からdrums=1

```bash
python scripts/stream.py --journey rain_emerge          # レンダリング
open http://localhost:8240/emerge.html                  # 可視化つき試聴
```

`out/stream_<name>.json` にジャーニーのメタデータが出力され、`emerge.html` が
これを読んで「環境音⇄音楽」メーター・ゲインカーブのタイムライン（クリックでシーク）・
スペクトログラムを再生位置に同期して描画する。

## ライブ演奏モード（live.py）

emergenceのオートメーションを**手動リアルタイム操作**に置き換えたモード。

```bash
python scripts/live.py --record     # モデルロード後、音が出始める
open http://localhost:8241          # コントロールパネル
```

- 生成スレッドが1秒チャンクごとにパラメータを読み直す（反映まで約1〜3秒）
- 操作できるもの: `w_audio`（環境音⇄テキストのブレンド）/ 原音・生成ゲイン /
  drums（おまかせ・off・on）/ 環境音ソース切替 / テキストプロンプト書き換え
- 埋め込み計算は別スレッド（プロンプト変更で音は止まらない。新埋め込みが
  できるまで旧スタイルで演奏継続）
- 音はデフォルト出力デバイスへ直接出る。`--record` で終了時に `out/live_*.wav` を保存
- 注意: MLXはロードしたスレッドでしか推論できないため、モデルは生成スレッド内でロードする
