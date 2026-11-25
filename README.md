# Manim 实数完备性全景大电影 & Kaiti Lecture Film Skill

本项目包含两部分完整内容：

1. **完整可运行案例：《实数完备性全景大电影》（1080P 60FPS · 楷体大字 · 配音版 + 无声母带 + 11 幕独立分片）**
2. **可复用 AI Skill：`kaiti-lecture-film-skill`**（根目录即标准 Skill 结构，支持把任意数学讲义、定理或课程内容制作成同款「楷体大字 · 深色高奢 · 音画逐句同步」讲解视频）

---

## 🎬 样板间成果：《实数完备性全景大电影》

围绕**实数系的建立（戴德金分割）**与**实数完备性六大等价定理**打造的全景动画工程，全长 `144.1s`（1080P 60FPS），共 11 幕动画、26 段逐句对齐中文解说：

- **直接观看配音成片**：[`examples/real-number-completeness-film/out/实数完备性大电影_配音版_1080P60.mp4`](examples/real-number-completeness-film/out/实数完备性大电影_配音版_1080P60.mp4)
- **无声高清母带**：[`examples/real-number-completeness-film/out/episodes/实数完备性全景大电影_楷体大字母带_1080P60.mp4`](examples/real-number-completeness-film/out/episodes/实数完备性全景大电影_楷体大字母带_1080P60.mp4)
- **11 幕独立分片**：[`examples/real-number-completeness-film/大字楷体分幕精选/`](examples/real-number-completeness-film/大字楷体分幕精选/)
  - `00_片头_六柱环核3D.mp4`（3D 六柱环绕实数核开场）
  - `00_历史篇_四大立法者肖像.mp4`（柯西、魏尔斯特拉斯、戴德金、康托尔）
  - `01_实数创立_戴德金分割.mp4`
  - `02_定理一_确界原理与证明.mp4`
  - `03_定理二_单调有界定理与证明.mp4`
  - `04_定理三_一维区间套定理.mp4`
  - `05_定理三拓展_三维嵌套立方体.mp4`
  - `06_定理四_致密性定理与二分证明.mp4`
  - `07_定理五_有限覆盖定理与反证.mp4`
  - `08_定理六_柯西审敛准则与证明.mp4`
  - `09_终章_3D等价闭环星系.mp4`

更多案例源码、时间轴对照表、配音稿与避坑交接文档见 [`examples/real-number-completeness-film/README.md`](examples/real-number-completeness-film/README.md)。

---

## 🛠️ 作为 AI Skill 安装使用（`kaiti-lecture-film-skill`）

仓库根目录即为标准 Agent Skill 包，克隆到你的 AI 助手技能目录即可直接使用：

```bash
# Claude Code / 通用 Agent Skills 目录
git clone https://github.com/FTZ-OPUS/manim-real-number-completeness.git ~/.claude/skills/kaiti-lecture-film-skill

# WorkBuddy
git clone https://github.com/FTZ-OPUS/manim-real-number-completeness.git ~/.workbuddy/skills/kaiti-lecture-film-skill
```

对 AI 助手说类似下面的话即可开始制作新视频：

> 请读取 `kaiti-lecture-film-skill` 的 `SKILL.md` 和 `AGENT-实操指南.md`，帮我把这份数学讲义做成《实数完备性大电影》同款楷体大字讲解视频，要求 1080P60 并配中文解说、音画逐句对齐。

核心文档与脚本：
- [`SKILL.md`](SKILL.md) — 技能总纲、标准 8 步工作流与铁律速查
- [`AGENT-实操指南.md`](AGENT-实操指南.md) — 任意讲义到分幕脚本与视觉隐喻映射指南
- [`references/`](references/) — 版式规范、时间轴重建与配音、长视频（30–60 分钟）指南、联网搜图与避坑清单
- [`scripts/`](scripts/) — 跨平台一键渲染缝合 (`build_film.py`)、分段 TTS 配音合成 (`dub_pipeline.py`)、自动体检验收 (`verify_film.py`)
- [`使用说明.pdf`](使用说明.pdf) · [`成本估算.pdf`](成本估算.pdf) — 人工阅读版使用说明与算力/成本估算

---

## 📁 仓库目录结构

```text
.
├── README.md                              # 本仓库总览
├── SKILL.md                               # AI Skill 入口与 8 步工作流
├── AGENT-实操指南.md                       # 任意内容转化为楷体讲义电影的操作指南
├── 使用说明.pdf                            # 环境搭建与操作手册（PDF）
├── 成本估算.pdf                            # 制作成本与耗时估算（PDF）
├── assets/
│   ├── fonts/字体说明.md                   # 跨平台楷体字体（Kaiti SC / KaiTi / 霞鹜文楷）配置
│   └── templates/                         # scenes.json 与 LaTeX 文档模板
├── references/                            # 专题参考规范（版式/配音/长片/搜图/排错）
├── scripts/                               # build_film.py / dub_pipeline.py / verify_film.py
└── examples/
    └── real-number-completeness-film/     # 《实数完备性全景大电影》完整案例与成片
        ├── real_number_cold_open_3d.py    # 3D 片头神殿源码
        ├── real_number_history_expanded.py# 扩充版历史篇源码
        ├── real_number_kaiti_master.py    # 六大定理 9 幕核心源码
        ├── build_kaiti_master.py          # 原工程一键渲染拼接脚本
        ├── build/scenes.json              # Skill 通用渲染清单
        ├── assets/portraits/              # 4 位数学家肖像（照片版 + 版画版）
        ├── 大字楷体分幕精选/               # 11 幕独立 1080P60 分幕视频
        ├── out/                           # 最终配音成片、无声母带与段落时间表
        ├── work/                          # 配音配置、TTS 分段音频与历史版本备份
        ├── 配音稿_实数完备性大电影.md       # 26 段定稿配音文案与时间轴记录
        └── 交接文档.md                     # 原工程交接说明与避坑记录
```

---

## 💻 运行环境依赖

| 依赖 | 用途 | 安装建议 |
| :--- | :--- | :--- |
| **Python ≥ 3.10** | 运行 Manim 与构建/配音脚本 | 官方安装包或虚拟环境 |
| **Manim CE ≥ 0.18** | 动画渲染（开发验证于 `v0.21.0`） | `pip install manim` |
| **FFmpeg & FFprobe** | 分幕拼接、音频混流与成片验收 | macOS `brew install ffmpeg` / Win `winget install ffmpeg` / Linux `apt install ffmpeg` |
| **LaTeX (含 dvisvgm)** | `MathTex` 公式编译 | MacTeX / MiKTeX / TeX Live |
| **edge-tts** *(可选)* | 免费中文分段语音合成 | `pip install edge-tts` |
| **楷体字体** | 标题与字幕视觉呈现 | macOS `Kaiti SC` / Windows `KaiTi` / Linux `LXGW WenKai`（详见 [`assets/fonts/字体说明.md`](assets/fonts/字体说明.md)） |

---

## 🚀 快速复现样板间

```bash
cd examples/real-number-completeness-film

# 1. 烟测单幕（480p15 秒出）
manim -pql real_number_kaiti_master.py Scene03_MonotoneConvergence

# 2. 使用 Skill 脚本全量渲染 11 幕并无损拼接（1080p60）
python ../../scripts/build_film.py build/scenes.json

# 3. 执行分段配音与音画混流
python ../../scripts/dub_pipeline.py work/dub_config.json

# 4. 自动复检验收
python ../../scripts/verify_film.py \
    --master out/episodes/实数完备性全景大电影_楷体大字母带_1080P60.mp4 \
    --dubbed out/实数完备性大电影_配音版_1080P60.mp4 \
    --scenes-json build/scenes.json \
    --probes 5.5,60,143 --probe-dir out/probes
```
