# 環境音を音楽にする — サーベイ

**作成日**: 2026-07-17
**目的**: 環境音（field recording / 自然音 / 都市音 / 環境データ）を「音楽」へ変換するアート作品・学術研究・製品を横断的に整理し、各事例について (a) 音がどう変換されるか（transformation technique）と (b) どう音楽的形式に編成されるか（musical arrangement）を明示する。最後に、今回の audio2audio 実験（Magenta RealTime 2 / Stable Audio）への示唆をまとめる。

---

## ① アート作品・インスタレーション

### 1.1 歴史的源流：musique concrète と anecdotal music

| 作品 | 変換手法 | 音楽化の方法 |
|---|---|---|
| Pierre Schaeffer《Cinq études de bruits》(1948) — 機関車の音などによる最初期の具体音楽 | テープ編集・ループ・速度変化（acousmatic reduction） | 反復とモンタージュによるリズム構造。[Chris Watson のレビューでも参照点として言及](https://www.musicworks.ca/reviews/recordings/chris-watson-el-tren-fantasma) |
| Luc Ferrari《Presque rien No.1》(1968–70) | ほぼ無加工。1日分の漁村の録音を**編集のみ**で21分に圧縮（["anecdotal music"](https://en.wikipedia.org/wiki/Luc_Ferrari)） | 「社会が決定するイベント」の反復を時間圧縮し、物語的な聴取の枠組みを与える。[Leonardo Music Journal の分析](https://direct.mit.edu/lmj/article-abstract/doi/10.1162/LMJ_a_01002/69463/A-Memory-of-Almost-Nothing-Luc-Ferrari-s-Listening) |
| World Soundscape Project / Hildegard Westerkamp《Kits Beach Soundwalk》(1989) 等 | field recording のレイヤリング・EQ・フィルタによる「聴取の拡大」（[soundscape composition](https://www.hildegardwesterkamp.ca/writings/writingsby/?post_id=15&title=linking-soundscape-composition(1)-and-acoustic-ecology)） | ナレーション＋録音現場の文脈を保存したまま構成。soundwalking という方法論を確立（[Westerkamp — Wikipedia](https://en.wikipedia.org/wiki/Hildegard_Westerkamp)、[ecomusicology 論考](https://scalar.usc.edu/works/soundscape-composition-as-environmental-activism-and-awareness-an-ecomusicological-approach/hildegard-westerkamp---kits-beach-soundwalk-1989)） |

### 1.2 環境音の「転送・共鳴」系インスタレーション

- **Bill Fontana**（1976–）: 都市・自然の複数地点にマイク／hydrophone／accelerometer を設置し、**real-time acoustic data を別の公共空間へ中継（relocation）**する sound sculpture。変換はほぼ行わず「文脈の転置」自体が作曲行為。近年は超音波スピーカーと振動センサーで建築の内部共鳴を可聴化（[Sonic Shadows, SFMOMA](https://www.sfmoma.org/publication/soundtracks/bill-fontana/)、[作家公式](https://www.resoundings.info/about)、[Landscape Soundings](https://www.resoundings.info/landscape-soundings)）。**音楽化**: 同時多点のポリフォニーとして空間に配置する（ミックス＝空間定位が「編曲」）。
- **David Tudor《Rainforest IV》**(1973): 自然科学系の音源（動物音など）を electromagnetic transducer で金属板・樽などの**共鳴物体に流し込み、物体の固有共鳴でフィルタリング**して「電子的エコシステム」を作る（[davidtudor.org](https://davidtudor.org/Works/rainforest.html)、[Getty Research](https://www.getty.edu/research/tools/guides_bibliographies/david_tudor/av/rainforest.html)、[MoMA の Rainforest V 保存論文](https://resources.culturalheritage.org/emg-review/conservation-of-a-software-based-sound-installation-insights-from-the-museum-of-modern-arts-installation-of-david-tudor-and-composers-inside-electronics-rainforest-v-variation-1-2/)）。**音楽化**: 各オブジェクト＝固有スピーカーの群を歩き回る walk-through 環境。物理共鳴が音色変換、空間配置が形式。
- **teamLab《呼応する森 / Resonating Forest》シリーズ**(2014–, サウンド: 高橋英明): 実際の森の木々をライトアップし、人の接近で**色と対応する tone が発火し隣の木へ伝播**する。環境音の変換ではなく「森を発音体グラフにする」タイプで、来場者と動物の存在が波となり**森全体が一つの音楽になる**（[teamLab 公式](https://www.teamlab.art/w/resonatingforest2016/)、[コンセプト](https://www.teamlab.art/concept/resonating/)）。**音楽化**: セルオートマトン的伝播ルール＋ペンタトニック的な音色セット（generative rules）。

### 1.3 bioacoustics / エコロジー系

- **Bernie Krause + United Visual Artists《The Great Animal Orchestra》**(2016, Fondation Cartier 委嘱): 7つの生息域の biophony 録音を合成した音響作品を、**リアルタイム streaming spectrogram を光の粒子として空間投影**する没入型インスタレーションに（[Fondation Cartier](https://www.fondationcartier.com/en/exhibitions/international/bernie-krause)、[UVA](https://www.uva.co.uk/features/great-animal-orchestra-cartier-foundation)、[Exploratorium 巡回](https://www.exploratorium.edu/TGAO)）。**変換**: 無加工再生＋spectrogram 可視化（「動物のオーケストラ＝楽譜」というメタファー）。**音楽化**: 生息域ごとの周波数ニッチ（niche hypothesis）をそのまま「オーケストレーション」として提示。
- **Jana Winderen**: hydrophone による不可聴領域（甲殻類のクリック、魚のうなり、海棲哺乳類）の採取。本人いわく制作は「書くというより彫刻に近い」**長時間の聴取とコラージュ**（[Columbia の展示解説](https://arts.columbia.edu/art-listening-under-water)、[TBA21](https://tba21.org/Jana_Winderen)、[MoMA Soundings](https://www.moma.org/interactives/exhibitions/2013/soundings/artists/15/works/)）。**音楽化**: 多チャンネル空間再生でのダイナミクス設計（クジラの歌を「強度のモーメント」として配置）。
- **Chris Watson《El Tren Fantasma》**(2011): メキシコ縦断鉄道の録音を**再配列して映画的ナラティブに再構成**。ループ化した列車のリズム、subtle な drone の付加、空間的レイヤリングという musique concrète 直系の手法（[Touch レーベル](https://touch33.net/catalogue/to42-chris-watson-el-tren-fantasma.html)、[Cyclic Defrost 評](https://www.cyclicdefrost.com/2012/01/chris-watson-el-tren-fantasma-touch/)、[Headphone Commute 評](https://headphonecommute.com/2012/04/17/chris-watson-el-tren-fantasma-touch/)）。**音楽化**: 列車の反復音→ビートとして loop、旅程→アルバムの時間構造。
- **David Rothenberg**: クラリネットで鳥・クジラ・セミと**その場で共演する interspecies music**。ライブ演奏そのものが「環境音の音楽化」（[Wikipedia](https://en.wikipedia.org/wiki/David_Rothenberg)、[Whale Music: Anatomy of an Interspecies Duet](https://www.researchgate.net/publication/249563692_Whale_Music_Anatomy_of_an_Interspecies_Duet)）。**音楽化**: 即興的 call & response。変換ではなく応答。

### 1.4 サンプリング／ポップ寄りの実践

- **Matthew Herbert《One Pig》**(2011): 一頭の豚の誕生から食卓までの**5,000以上の field recording だけ**で構成したアルバム。「Personal Contract for the Composition of Music」（プリセット・他人のサンプル禁止）という自己規範に基づく（[Sound on Sound インタビュー](https://www.soundonsound.com/people/matthew-herbert-sampling-pig-noises)、[Slate 評](https://www.slate.com/articles/arts/music_box/2011/12/matthew_herbert_s_one_pig_reviewed_experimental_album_made_from_a_pig.html)）。**変換**: sampler へのマッピング。**音楽化**: サンプルを鍵盤・トリガーギターに割り当てて**人間の演奏でメロディ／ダンスのリズムを構築**（quantize + 演奏）。ソースの意味（豚の一生）を保持したまま曲にする点が核心。
- **Holly Herndon《Holly+》**(2021, Never Before Heard Sounds と共同): 自身の声で訓練した **neural timbre transfer モデルを公開楽器化**。アップロードした任意の音（環境音含む）の pitch と rhythm を保持したまま Herndon の声のテクスチャに変換（[公式](https://paragraph.com/@holly-herndon/holly)、[Scientific American](https://www.scientificamerican.com/article/experimental-composer-holly-herndon-built-an-ai-voice-clone-that-anyone-can/)、[JPMS 論文](https://online.ucpress.edu/jpms/article-abstract/38/2/34/218373/Holly-Plus-Whom-The-Holly-Timbre-Transfer-Program)）。声というドメインだが「audio2audio 変換を作品＝制度（DAO）として設計した」先例。

### 1.5 環境データの sonification 系

- **坂本龍一 + YCAM InterLab《Forest Symphony》**(2013): 樹木の**生体電位（bioelectric potential）を専用センサーで世界各地から収集し、連続的に音へ変換**するインスタレーション（映像: 高谷史郎）。センサーキットはオープンソース化（[YCAM InterLab](https://special.ycam.jp/interlab/en/projects/forestsymphony.html)、[Google Arts & Culture](https://artsandculture.google.com/story/ryuichi-sakamoto%EF%BC%8Bycam-interlab-%E2%80%9Cforest-symphony%E2%80%9D-yamaguchi-center-for-arts-and-media/egURwLvtkRQlTw?hl=en)、[YCAM 2025 再展示](https://www.ycam.jp/en/events/2025/yamaguchi-seasonal-2025-forest-symphony/)）。**変換**: parameter mapping sonification。**音楽化**: 複数の木＝複数声部のアンサンブル（「交響曲」の比喩）、ドローン的持続。
- **Bartholomäus Traubeck《Years》**(2011): 改造ターンテーブル＋カメラで**木の年輪を読み取り、太さ・成長速度を Ableton Live 上の generative process でピアノ音へマッピング**。木の色・質感でスケールを決定（[作家公式](http://traubeck.com/works/years)、[Vice インタビュー](https://www.vice.com/en/article/making-tree-rings-sing-via-a-super-modified-turntable-q-a/)、[Bandcamp](https://traubeck.bandcamp.com/album/years)）。**音楽化**: pitch mapping + scale quantization + レコード再生という時間構造（回転＝テンポ）。
- **Chris Chafe (Stanford CCRMA)**: 850–2016年の気温・CO2 データを**physical model（ナイロン弦ギター）と FM 歌声合成のパラメータへマッピング**した気候 sonification（[CCRMA](https://ccrma.stanford.edu/news/listen-1200-years-of-earth-s-climate-transformed-sound)、[Earth Symphony](https://chrischafe.net/earth-symphony/)、[KQED](https://www.kqed.org/science/1918660/listen-1200-years-of-earths-climate-transformed-into-sound)）。

### 1.6 環境そのものを演奏者にする（aeolian / hydraulic）

- **Nikola Bašić《Sea Organ》**(Zadar, 2005): 階段下に35本のオルガンパイプ。**波が押す空気柱がパイプを鳴らす**。調律されたパイプ群により「ランダムだが調和する」音楽（[Wikipedia](https://en.wikipedia.org/wiki/Sea_organ)、[Atlas Obscura](https://www.atlasobscura.com/places/sea-organ)）。**音楽化**: 音高集合を建築側で固定（＝スケール量子化をハードウェアで実装）し、リズムは環境（波）に委譲。
- **Tonkin Liu《Singing Ringing Tree》**(Burnley, 2006): 積層鋼管を風が鳴らす aeolian 彫刻。数オクターブのコーラス（[Visit Lancashire](https://www.visitlancashire.com/things-to-do/singing-ringing-tree-panopticon-p66560)、[Atlas Obscura 特集](https://www.atlasobscura.com/articles/eerie-instruments-played-by-the-wind)）。
- **Félix Blume《Rumors from the Sea》**(Thailand, 2018): 海中に立てた数百本の竹の先端に笛を付け、**波と風で鳴る海のオーケストラ**（[作家公式](https://felixblume.com/)、[Freesound の記録](https://freesound.org/people/felix.blume/sounds/444653/)）。《Swarm》では600匹の蜂を1匹ずつ専用スタジオで録音し、**250個の小型スピーカー各々に1匹の蜂を再生**する群体スピーカー作品（[we-make-money-not-art](https://we-make-money-not-art.com/recording-studio-for-bees-and-other-sound-oddities/)）。**音楽化**: 個体＝1声部の超多声ポリフォニー（空間加算合成）。
- **Yuri Suzuki《Arborhythm》**(San Francisco, 2024): 樹状のホーンスピーカー群から、霧笛・波・ケーブルカー・アシカ等**100以上の現地 field recording をアンビエント・サウンドトラックとして再構成**して再生（[Dezeen](https://www.dezeen.com/2024/05/20/yuri-suzuki-arborhythm-installation-san-francisco/)、[作家公式](https://yurisuzuki.com/projects/arborhythm)）。《Sonic Bloom》《Otonomori》はホーンによる無電源の音響伝達で環境と人の声を音楽的体験にする（[Dezeen: Otonomori](https://www.dezeen.com/2025/03/25/yuri-suzuki-otonomori-jingan-international-sculpture-project/)、[stirworld 総説](https://www.stirworld.com/see-features-yuri-suzukis-sound-installations-combine-human-environmental-and-sonic-values)）。

---

## ② 学術研究

### 2.1 Corpus-based concatenative synthesis / audio mosaicing

- **CataRT (Diemo Schwarz, IRCAM)**: 分節化＋記述子解析済みの大規模コーパスから、**記述子空間内のターゲット位置に近い grain を連結再生**する real-time corpus-based concatenative synthesis (CBCS)。Max/MSP + FTM 実装、GPL（[eContact! 解説](https://econtact.ca/16_2/schwarz_corpus.html)、[NIME/JIM 論文](http://jim.afim-asso.org/jim08/upload/05_Schwarz_catart-jim2008-final.pdf)、[Corpus-Based Sound Synthesis Survey](http://imtr.ircam.fr/imtr/Corpus-Based_Sound_Synthesis_Survey)）。**環境音との関係**: 映画・ゲームの environmental sound texture 合成やインスタレーションが有望な応用として明記されている。**音楽化**: 記述子空間（pitch / loudness / spectral centroid…）を XY パッドや軌道でナビゲート＝「音色空間の演奏」。
- **NMF audio mosaicing「Let It Bee」(ISMIR 2015, AudioLabs Erlangen)**: ターゲット曲のスペクトログラムを、**ソース録音（例: 蜂の羽音）のスペクトルテンプレートの非負線形結合で近似**する NMF。activation matrix に対角スパース制約を入れてソースの音色の粒を保つ（[論文 PDF](https://archives.ismir.net/ismir2015/paper/000013.pdf)、[デモページ](https://www.audiolabs-erlangen.de/resources/MIR/2015-ISMIR-LetItBee)、[NMF Toolbox](https://www.audiolabs-erlangen.de/resources/MIR/NMFtoolbox/)）。まさに「蜂の羽音で Let It Be を歌わせる」＝環境音→既存楽曲構造への写像。
- **The Concatenator (2024)**: particle filter による **Bayesian real-time concatenative musaicing**。巨大コーパスでもリアルタイムにターゲット追従（[arXiv](https://arxiv.org/html/2411.04366v1)）。
- **FluCoMa (Fluid Corpus Manipulation, Univ. of Huddersfield / ERC)**: Max / SuperCollider / Pd 向けの**分解（NMF/HPSS）・機械聴取・機械学習（MLP, KMeans, UMAP…）ツール群**。コーパスの記述子解析→次元削減→2Dマップ演奏という CBCS ワークフローを民主化（[flucoma.org](https://www.flucoma.org/)、[Computer Music Journal 論文](https://direct.mit.edu/comj/article/45/2/9/111383/Enabling-Programmatic-Data-Mining-as-Musicking-The)、[learn.flucoma.org](https://learn.flucoma.org/)）。
- **AudioStellar (NIME 2021)**: 自前サンプル群を t-SNE / PCA で **2D latent map 化し、自律エージェント・リズム星座・軌道描画で「演奏」するオープンソース楽器**（[NIME 論文](https://nime.pubpub.org/pub/dwtopcue/release/1)、[IRCAM Forum 紹介](https://forum.ircam.fr/article/detail/audiostellar/)）。**音楽化**: エージェントのルール（generative）＋MIDI/OSC 制御。

### 2.2 Neural timbre transfer / 生成モデル

- **DDSP (Google Magenta, ICLR 2020)**: 微分可能な oscillator / filter / reverb を NN が制御。**入力音から f0 と loudness を抽出し、別楽器の音色で再合成**する timbre transfer が代表応用（10分程度のデータで学習可）（[GitHub](https://github.com/magenta/ddsp)、[OpenReview](https://openreview.net/forum?id=B1x1ma4tDr)）。リアルタイム化研究も（[Real-time Timbre Transfer using DDSP, arXiv:2103.07220](https://arxiv.org/abs/2103.07220)、[Timbre Remapping, arXiv:2407.04547](https://arxiv.org/pdf/2407.04547)）。**環境音での注意**: f0 追跡前提のため、非調波的な環境音（風・水・雑踏）では pitch 条件付けが破綻しやすい。
- **RAVE (Antoine Caillon & Philippe Esling, IRCAM ACIDS, 2021)**: VAE + multi-band 分解 + adversarial fine-tuning により **48kHz をラップトップ CPU 実時間の20倍速で合成**。**別ドメインで訓練した decoder に環境音を encode して流し込む zero-shot timbre transfer**（pitch・loudness・エンベロープは保持、音色は decoder 側に置換）（[arXiv:2111.05011](https://arxiv.org/abs/2111.05011)、[GitHub acids-ircam/RAVE](https://github.com/acids-ircam/RAVE)）。Max/PD 用 `nn~` でライブ運用可能。
- **VampNet (Hugo Flores García et al., ISMIR 2023)**: **masked acoustic token modeling**（双方向 Transformer、非自己回帰）。マスクの掛け方（prompt）次第で圧縮・inpainting・outpainting・**loop に変化を与える "vamping"** を実現（[arXiv:2307.04686](https://arxiv.org/abs/2307.04686)、[プロジェクトページ](https://interactiveaudiolab.github.io/project/music-audio-generation.html)）。環境音ループを入れて「保ちつつ変異させる」用途に直結。
- **MusicGen (Meta AudioCraft, 2023)**: テキスト＋**chromagram による melody conditioning**。参照音声からクロマを抽出し、音色に依存しない旋律・和声骨格だけを生成の誘導に使う（[公式ドキュメント](https://facebookresearch.github.io/audiocraft/docs/MUSICGEN.html)、[GitHub](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md)）。**環境音への含意**: 鳥の歌など音高性のある環境音はクロマ経由で「旋律素材」化できる。
- **Stable Audio 2.0 (Stability AI, 2024)**: 高圧縮 autoencoder + Diffusion Transformer。**audio-to-audio は sampling 時のノイズ初期化に入力音を使う（img2img 方式）style transfer** で、参照音声の時間構造を保ちながらテキストプロンプトで音色・様式を書き換える（例: ビートボックス→リアルなドラム）（[公式発表](https://stability.ai/news/stable-audio-2-0)、[技術デモ](https://stability-ai.github.io/stable-audio-2-demo/)、[3.0 も audio-to-audio / style transfer 対応](https://stability.ai/stable-audio)）。
- **Live Music Models / Magenta RealTime (Google DeepMind, 2025–26)**: ライブ音楽生成モデルの論文（[arXiv:2508.04651](https://arxiv.org/html/2508.04651v1)）。詳細は §3・§6。

### 2.3 Sonification / bioacoustics 研究

- **気候データ sonification のレビュー**: 395件の sonification プロジェクトから気候変動対象の32件を分析した [Frontiers in Psychology (2022)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1020102/full)、Data Sonification Archive ベースの [19事例レビュー](https://www.researchgate.net/publication/367511347_Sonifying_data_taking_action_on_Climate_Change_a_review_of_cases_from_the_Data_Sonification_Archive)、音楽的 sonification の設計論 [BAMS (2017)](https://journals.ametsoc.org/view/journals/bams/98/1/bams-d-15-00223.1.xml)。傾向として「工学的 parameter mapping から電子音響音楽の知見の導入へ」。
- **Chris Chafe (CCRMA)** の一連の climate/ecology sonification（→ §1.5）と [sonification workshop 資料](https://ccrma.stanford.edu/~cc/sonify/)。
- **bioacoustics → 音楽**: Krause の niche hypothesis（生態系内の周波数分担をオーケストレーションと見る）、Rothenberg の interspecies duet 研究（[Whale Music 論文](https://www.researchgate.net/publication/249563692_Whale_Music_Anatomy_of_an_Interspecies_Duet)）。作曲側の系譜は Messiaen の鳥歌採譜（人間の楽器に合わせ**低い音域へ移調・速度調整して西洋音組織に埋め込む**、[研究ノート](https://www.researchcatalogue.net/view/887686/887687)）から、Jonathan Harvey《Bird Concerto with Pianosong》（ピアニストが**鳥歌サンプルをシンセで演奏し、曲中で徐々に変形**、[Stereophile 解説](https://www.stereophile.com/content/olivier-messiaen-birds-youve-never-heard)）へ。「transcription → sampling → transformation」という段階的な技術史になっている。

---

## ③ 製品・ツール

| 製品 | 何をするか | 変換手法 | 音楽化の方法 |
|---|---|---|---|
| [Neutone Morpho](https://neutone.jp/morpho) (VST3/AU, $99+無料版) | リアルタイム tone morphing。入力音を学習済みモデルの音色に再合成 | RAVE 系 autoencoder（encoder が pitch/loudness/微細特徴を抽出→decoder が別音色で再合成）（[公式ブログ](https://neutone.jp/blog/introducing-neutone-morpho)） | 入力の時間形状を保持するので「環境音を演奏データとして使う」感覚。macro knob（Serendipity 等）で変換の逸脱度を制御。**ノーコードのカスタムモデル訓練**も提供予定と告知（[FAQ](https://neutone.jp/morpho/faq)） |
| [Magenta RealTime 2](https://huggingface.co/google/magenta-realtime-2) (2026-06, Apache 2.0 / CC-BY) | オンデバイス・ライブ音楽生成。**text + 参照 audio + MIDI を同時に**受けて約200ms で追従（[GIGAZINE](https://gigazine.net/gsc_news/en/20260605-magenta-realtime-2-live-music-ai/)、[解説記事](https://studio.aifilms.ai/blog/magenta-realtime-2-open-source-music-model)） | **MusicCoCa**: audio/text を共通768次元埋め込み→12 RVQ token に量子化して style 条件付け。SpectroStream が 48kHz stereo を 25Hz フレームの離散トークン化。decoder-only Transformer (2.4B / 230M) | style embedding の**連続的な補間・重み付きブレンド**がそのまま演奏インターフェース。ジャム／映画スコアリングなどライブ用途 |
| [Stable Audio 2.0 / 3.0](https://stability.ai/news/stable-audio-2-0) (Web / API) | テキスト・音声から最長数分のトラック生成。**audio-to-audio style transfer** | latent diffusion (DiT)。入力音でノイズを初期化し、**時間構造を保って音色様式をプロンプトで置換**（[デモ](https://stability-ai.github.io/stable-audio-2-demo/)） | プロンプト＝編曲指示。「環境録音→ジャンル付き楽曲」を一発で行える反面、構造は入力任せ |
| [Samplab 2](https://samplab.com/features) (VST/AU, 無料版あり) | **polyphonic audio → MIDI 変換**とステム分離（[BPB 紹介](https://bedroomproducersblog.com/2021/08/29/samplab-audio-midi/)） | サーバーサイド AI で音高推定・分離 | 環境音を「ピアノロールで編集できる音符」に変換→任意の音源で再演奏（pitch mapping の自動化） |
| [Samplebrain](https://thentrythis.org/projects/samplebrain/) (Aphex Twin + Dave Griffiths, 2022, 無料 OSS) | サンプル群を類似度ネットワーク（"brain"）化し、**ターゲット音を最も似た block の連結で再構成** | block-based audio mosaicing（FFT/MFCC 類似度マッチング）（[CDM 解説](https://cdm.link/free-sample-mashing-with-samplebrain-by-aphex-twin-and-dave-griffiths/)） | ターゲット（既存曲や声）の時間構造を保持したまま素材を環境音に置換 |
| [AudioStellar](https://forum.ircam.fr/article/detail/audiostellar/) (無料 OSS) | サンプルフォルダ→ **t-SNE 2D 音響マップ** | 次元削減による latent space 可視化 | 自律エージェント・リズム星座・軌道で generative 演奏、MIDI/OSC 連携 |
| [XLN XO](https://www.xlnaudio.com/products/xo) / [Algonaut Atlas 2](https://algonaut.audio/) | ワンショット群を**類似度マップに自動整理**し、ビートメイクへ | 音響特徴での類似度クラスタリング | 環境音の打撃系ワンショットをドラムキット化（grid sequencer に量子化） |
| [Ableton Granulator III](https://www.ableton.com/en/packs/granulator-iii/) (Robert Henke, Max for Live) | field recording を**グラニュラー楽器化**。Classic / Loop / Cloud の3モード、リアルタイムキャプチャ、MPE（[Sound on Sound](https://www.soundonsound.com/techniques/ableton-live-12-granulator-iii)） | granular synthesis（2ms〜の grain 重畳） | 鍵盤演奏＝環境音テクスチャの pitch mapping。Loop モードでリズム素材化 |
| [Endel](https://endel.io/technology) (アプリ / Amazon 出資) | 環境「データ」駆動の generative soundscape（天候・時刻・心拍・歩行ケイデンス） | parameter mapping → ノードベースのサウンドロジック（[How Endel Works](https://endel.zendesk.com/hc/en-us/articles/360012517639-How-Endel-Works)） | 事前デザインされたステム＋ルールベース編成（音楽側は人間が設計、環境がミックスを操縦） |
| [Holly+](https://paragraph.com/@holly-herndon/holly) (Web, Never Before Heard Sounds 実装) | 任意のアップロード音声を Herndon の声に変換 | neural timbre transfer | pitch/rhythm 保持 → 演奏・スコア入力・リアルタイム版も展開 |

補足: CataRT は [MuBu for Max](https://forum.ircam.fr/article/detail/audiostellar/) 系パッケージとして、FluCoMa は Max/SC/Pd パッケージとして、研究ツールでありながら実質「製品」として流通している。

---

## ④ 変換手法（transformation techniques）の分類まとめ

| 手法 | 原理 | ソースの何が残るか | 代表例 | 環境音での相性 |
|---|---|---|---|---|
| **Editing / montage**（テープ以来の編集） | 切断・並べ替え・時間圧縮 | ほぼ全て（音色・意味） | Ferrari《Presque rien》、Watson《El Tren Fantasma》 | ◎ 意味と場所性を最大限保持 |
| **Relocation / real-time relay** | 別空間への転送・同時多点ミックス | 全て（文脈だけ変わる） | Fontana の sound sculptures | ◎ 変換ゼロの極北 |
| **Physical resonance / transducer** | 物体・建築の固有共鳴でフィルタ | スペクトル骨格 | Tudor《Rainforest IV》、Fontana《Sonic Shadows》 | ◎ 物質性が加わる |
| **Aeolian / hydraulic**（環境が励起源） | 風・波が調律済み構造を鳴らす | ソースは「エネルギー」として使われる | Sea Organ、Singing Ringing Tree、Blume《Rumors from the Sea》 | ◎ 音高は構造側で決定 |
| **Granular synthesis** | 2–100ms の grain の重畳・再配置 | テクスチャ・質感 | Granulator III、CataRT の再生部 | ◎ 非調波音でも破綻しない |
| **Concatenative / CBCS** | 記述子空間で unit 選択・連結 | 粒単位の原音そのもの | CataRT、FluCoMa、AudioStellar、Samplebrain | ◎ 原音の粒を保ったまま再組織化 |
| **Audio mosaicing (NMF / particle filter)** | ターゲットのスペクトログラムをソース素材の結合で近似 | ソースの音色、ターゲットの構造 | Let It Bee、The Concatenator | ◎「環境音で既存曲を歌わせる」 |
| **Spectral processing** | FFT 領域の morphing / cross-synthesis / freeze | スペクトル包絡の一部 | pfft~ 系モーフィング、Harvey の鳥歌変形 | ○ ハイブリッド音色向き |
| **Audio-to-MIDI（転写）** | 音高・オンセット推定→記号化 | 旋律・リズムの骨格のみ | Samplab、Messiaen（人力転写の機械化） | △ 音高性のある素材（鳥・機械音）限定 |
| **Parameter mapping sonification** | 非音響データ→合成パラメータ | データの時系列形状 | Forest Symphony、Years、Chafe の気候音楽 | ◎（ただし入力は「音」でなく「データ」） |
| **Neural timbre transfer (DDSP / RAVE / Morpho)** | f0+loudness あるいは latent を別音色 decoder で再合成 | pitch・loudness・時間エンベロープ | DDSP Tone Transfer、RAVE + nn~、Neutone Morpho、Holly+ | ○ 入力がモデル分布外だと「誤読」が起こる（それが面白さでもある） |
| **Token-based generative conditioning** | 離散トークン化した音を LM/diffusion が継続・変換 | style embedding / chroma / ノイズ初期化に応じ可変 | VampNet (vamping)、MusicGen (chromagram)、Stable Audio (a2a)、Magenta RT 2 (MusicCoCa) | ○〜◎ 「どこまで残すか」をパラメータ化できるのが新しさ |

---

## ⑤ 音楽的アレンジ手法（musical arrangement）の分類まとめ

1. **Narrative montage（物語的モンタージュ）** — 時間圧縮と再配列で「旅・一日・一生」の物語弧を作る。Ferrari、Watson、Herbert《One Pig》（豚の一生＝アルバム構造）。
2. **Layering / collage（レイヤリング）** — 複数録音の重ね合わせでテクスチャの密度曲線を設計。Winderen（「彫刻に近い」コラージュ）、Westerkamp。
3. **Looping & rhythm extraction** — 環境音内の反復（列車・機械・波）をループ化してビートに昇格。Watson の列車ループ、Herbert のダンスリズム、VampNet の loop vamping。
4. **Pitch mapping / scale quantization** — データや音響特徴を音階に量子化。Traubeck《Years》（年輪→ピアノスケール）、Sea Organ（パイプ調律）、teamLab（色→tone のセット）、Samplab（audio→MIDI→任意音源）。
5. **Sampler performance（人間の演奏）** — 環境音サンプルを鍵盤・パッドに割り当てて演奏する。Herbert（トリガーキーボード）、Harvey（鳥歌サンプルの鍵盤演奏）。
6. **Generative rules / autonomous agents** — 伝播ルール・エージェント・確率過程が形式を生む。teamLab（共鳴伝播）、AudioStellar（エージェント）、Endel（コンテクスト駆動ノード）、Traubeck（generative process）。
7. **Descriptor-space navigation（記述子空間の航行）** — 音色空間内の軌道・ジェスチャーが「旋律」の代わりになる。CataRT、FluCoMa、AudioStellar。
8. **Spatialization as form（空間配置＝形式）** — 多チャンネル・多点配置そのものが編成。Fontana（多点中継）、Blume《Swarm》（250スピーカー＝250声部）、Tudor（歩行で聴くポリフォニー）。
9. **Ecological orchestration（生態系の周波数分担をそのまま提示）** — Krause の niche hypothesis：種ごとの周波数帯域の棲み分けを「オーケストレーション」として聴かせる。
10. **Style conditioning（プロンプト／埋め込みによる様式付与）** — 構造は入力音から、様式はテキスト／参照音から。Stable Audio a2a、MusicGen chromagram、Magenta RT 2 の text+audio ブレンド。
11. **Interspecies improvisation（応答としての音楽化）** — 変換せず、環境（生物）と人間がリアルタイムに応答し合う。Rothenberg。

**軸として整理すると**: (a) ソースの同一性をどれだけ残すか（documentary ↔ material）、(b) 形式を誰が決めるか（人間の編集 ↔ ルール/モデル ↔ 環境そのもの）、(c) 時間解像度（サンプル単位 / grain / unit / フレーズ / 曲）。既存事例はこの3軸空間のどこかに位置づけられる。

---

## ⑥ 今回の audio2audio 実験（Magenta RealTime 2 / Stable Audio）への示唆

### 6.1 2つのモデルの「環境音の扱い方」は根本的に異なる

- **Magenta RT 2**: 環境音は主に **MusicCoCa の style embedding（768次元→12 RVQ token）** として入る。つまり環境音は「連続音響としてではなく、様式ベクトルに要約されて」使われる（[HF モデルカード](https://huggingface.co/google/magenta-realtime-2)）。音楽データで対照学習された埋め込みに環境音を通すと、**最近傍の音楽的様式へ射影される**（波音→アンビエントパッド、虫の声→シェイカー的テクスチャ等の「誤読」）。この系統的な誤読のマッピング自体が実験として面白い：**同じ環境音を text prompt と重み付きブレンドし、blend 比率を掃引して「環境→音楽」の連続体を作る**のは MRT2 が最も得意とする操作。
- **Stable Audio**: audio-to-audio は **diffusion のノイズ初期化に入力波形を使う**方式なので、**環境音の時間構造（イベントの位置、エネルギー包絡、リズム）が出力に直接転写**される（[stable-audio-2-demo](https://stability-ai.github.io/stable-audio-2-demo/)）。「ビートボックス→ドラム」の環境音版、つまり**雨垂れ→ピアノ、波→ストリングスの swell** のような構造保存型変換に向く。strength（変換強度）の掃引が §5 の軸 (a)（documentary ↔ material）を直接パラメータ化する。

### 6.2 サーベイから導かれる設計指針

1. **「何を残すか」を先に決める**。歴史的に成功している作品は、残すものが明確：Herbert は「意味（豚）」、Watson は「リズムと物語」、Tudor は「スペクトル骨格」、CataRT は「粒」。実験でも *identity preservation* の評価軸（原音の認知可能性 vs 音楽性のトレードオフ）を最初に定義すべき。
2. **ハイブリッドパイプラインが未開拓**。ニューラル a2a（音色を書き換える）と CBCS/mosaicing（原音の粒を残す）は補完関係にある。例：環境音を Samplebrain / FluCoMa 的 mosaicing で「原音の粒のまま」リズム化 → それを MRT2 の audio prompt に入れて伴奏を生成、のような**「原音レイヤー＋モデル生成レイヤー」の2層構成**は、サーベイ中に直接の先行例が見当たらない。
3. **音高性のある環境音は chroma/MIDI 経由の別ルートを持つ**。鳥の歌・救急車・機械のうなりは MusicGen の chromagram conditioning や Samplab の audio-to-MIDI で「旋律素材」に昇格できる。非調波音（水・風・雑踏）はテクスチャ／リズム素材として granular・a2a に回す、という**素材のトリアージ**（音高性・リズム性・テクスチャ性で分類）が有効。これは Krause の niche hypothesis（周波数帯域での役割分担）の制作論的応用でもある。
4. **リアルタイム性は作品形式を変える**。MRT2 の ~200ms 追従は、Fontana 型の「環境音のライブ中継」と組み合わせて**「いま外で鳴っている音が数百 ms 遅れで音楽になる」インスタレーション**を可能にする（従来のオフライン生成では不可能だった形式）。マイク入力→ MusicCoCa 埋め込みの連続更新→生成、という構成は Rothenberg 的な「環境との即興」のモデル版になる。
5. **ループ＋変異は VampNet 的発想で**。環境音ループをそのまま反復させると単調になる。vamping（保ちつつ変異）の考え方を Stable Audio でも模倣できる：同一入力に対し strength とシードを少しずつ変えた生成を連結し、**「変奏曲」形式**にする。
6. **失敗（分布外の誤読）を記録する**。DDSP は f0 前提で環境音に弱く、RAVE の zero-shot は「decoder の世界観による誤読」を起こす。これはバグではなく、Messiaen が鳥歌を人間の楽器に「移調・減速」した行為の機械版であり、**誤読の系統性そのものを作品・研究の対象にできる**（どの環境音がどの楽器に聴こえるかのマップ作成など）。
7. **アレンジは依然として人間側の仕事**。本サーベイの全事例で、変換（technique）は自動化が進んでいるが、**形式（form）を決めているのは編集・ルール設計・空間配置**。MRT2 / Stable Audio の実験でも「プロンプトのスケジューリング」「blend 比率のオートメーション」「セクション構造の設計」を明示的に作曲行為として扱うと、単なるモデルデモを超えられる。

---

## 主要ソース一覧（抜粋）

- アート: [Bill Fontana](https://www.resoundings.info/about) / [Rainforest IV](https://davidtudor.org/Works/rainforest.html) / [Great Animal Orchestra](https://www.fondationcartier.com/en/exhibitions/international/bernie-krause) / [Jana Winderen](https://tba21.org/Jana_Winderen) / [El Tren Fantasma](https://touch33.net/catalogue/to42-chris-watson-el-tren-fantasma.html) / [One Pig (SOS)](https://www.soundonsound.com/people/matthew-herbert-sampling-pig-noises) / [Forest Symphony (YCAM)](https://special.ycam.jp/interlab/en/projects/forestsymphony.html) / [Years](http://traubeck.com/works/years) / [Sea Organ](https://en.wikipedia.org/wiki/Sea_organ) / [Félix Blume](https://felixblume.com/) / [Arborhythm](https://www.dezeen.com/2024/05/20/yuri-suzuki-arborhythm-installation-san-francisco/) / [teamLab Resonating](https://www.teamlab.art/concept/resonating/) / [Holly+](https://paragraph.com/@holly-herndon/holly)
- 研究: [CataRT (JIM 2008)](http://jim.afim-asso.org/jim08/upload/05_Schwarz_catart-jim2008-final.pdf) / [Let It Bee (ISMIR 2015)](https://archives.ismir.net/ismir2015/paper/000013.pdf) / [The Concatenator](https://arxiv.org/html/2411.04366v1) / [FluCoMa (CMJ)](https://direct.mit.edu/comj/article/45/2/9/111383/Enabling-Programmatic-Data-Mining-as-Musicking-The) / [AudioStellar (NIME)](https://nime.pubpub.org/pub/dwtopcue/release/1) / [DDSP (ICLR 2020)](https://openreview.net/forum?id=B1x1ma4tDr) / [RAVE](https://arxiv.org/abs/2111.05011) / [VampNet](https://arxiv.org/abs/2307.04686) / [MusicGen docs](https://facebookresearch.github.io/audiocraft/docs/MUSICGEN.html) / [Stable Audio 2 demo](https://stability-ai.github.io/stable-audio-2-demo/) / [Live Music Models](https://arxiv.org/html/2508.04651v1) / [気候 sonification レビュー (Frontiers 2022)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1020102/full) / [Chris Chafe (CCRMA)](https://ccrma.stanford.edu/news/listen-1200-years-of-earth-s-climate-transformed-sound)
- 製品: [Neutone Morpho](https://neutone.jp/morpho) / [Magenta RealTime 2 (HF)](https://huggingface.co/google/magenta-realtime-2) / [Stable Audio](https://stability.ai/stable-audio) / [Samplab](https://samplab.com/features) / [Samplebrain](https://thentrythis.org/projects/samplebrain/) / [Granulator III](https://www.ableton.com/en/packs/granulator-iii/) / [XO](https://www.xlnaudio.com/products/xo) / [Atlas 2](https://algonaut.audio/) / [Endel](https://endel.io/technology)
