---
name: kaiti-lecture-film-skill
description: 楷体大字讲义电影全流水线 —— 用 Manim CE 把数学讲义/定理/证明做成 3Blue1Brown 风格的 16:9 楷体大字讲解视频，源码重建时间轴、分段 TTS 配音逐句对齐、自动复检验收，并支持扩展到 30-60 分钟长篇课程视频。Use when 用户要把讲义内容/数学定理做成讲解视频、复刻《实数完备性大电影》的楷体大字风格、要求 Manim 动画配解说且音画同步、制作一小时左右的系列课程视频，或抱怨配音与画面对不上。
---

# 楷体大字讲义电影 Skill（Kaiti Lecture Film）

把**一份讲义 / 一组定理 / 一个主题**变成一支「楷体大字 · 深色高奢 · 音画逐句同步」的讲解视频。
样板间成果：`examples/real-number-completeness-film/out/实数完备性大电影_配音版_1080P60.mp4`
（144 秒 / 1080P60 / 26 段配音 / 片头 3D 神殿 + 历史篇 + 六大定理证明 + 3D 终章）。

**一张图看懂流水线**：

```
讲义内容 → ① 分幕脚本(Python/Manim) → ② 一键渲染+缝合(build_film)
        → ③ 源码重建时间轴 → ④ 段落表+配音文案(dub_config)
        → ⑤ TTS/自备录音 + 级联排程(dub_pipeline) → ⑥ 复检验收(verify_film) → 交付
```

---

## 一、环境要求（跨平台）

| 依赖 | 用途 | 安装 |
|---|---|---|
| Python ≥ 3.10 | 运行 Manim 与脚本 | python.org / 系统包管理器 |
| Manim CE ≥ 0.18 | 渲染动画 | `pip install manim`（验证：`manim --version`） |
| FFmpeg + FFprobe | 缝合、配音混流、复检 | macOS `brew install ffmpeg`；Win `winget install ffmpeg`；Linux `apt install ffmpeg` |
| LaTeX（含 dvisvgm） | MathTex 公式渲染 | macOS MacTeX；Windows MiKTeX；Linux TeX Live |
| edge-tts | 免费中文 TTS | `pip install edge-tts`（自备录音则不需要） |
| 中文字体（楷体系） | 全片气质 | macOS 自带 `Kaiti SC`；Win 自带 `KaiTi（楷体）`；Linux 建议 `sudo apt install fonts-arphic-ukai` 或安装开源 [霞鹜文楷 LXGW WenKai](https://github.com/lxgw/LxgwWenKai/releases)。详见 `assets/fonts/字体说明.md` |

网络：TTS 与搜图需联网；渲染/缝合/复检全程离线可跑。

## 二、目录结构（标准 Skill 骨架）

| 部分 | 路径 | 作用 |
|---|---|---|
| 门面+大脑 | `SKILL.md`（本文件） | 何时用、怎么做、铁律索引 |
| **实操指南** | `AGENT-实操指南.md`（根目录） | **写给执行 Agent**：如何把用户的任意内容（不限样板间主题）套进本风格制作 |
| 知识库 | `references/` | 版式规范 · 配音方法论 · 长视频指南 · 联网搜图 · 避坑清单（按需翻阅，一个主题一个文件） |
| 手 | `scripts/` | `build_film.py` 渲染缝合 · `dub_pipeline.py` 配音合成 · `verify_film.py` 复检验收 |
| 样板间 | `examples/real-number-completeness-film/` | 完整可运行项目：3 个场景源码 + 肖像素材 + 配音稿 + 配置 + 成片 |
| 仓库 | `assets/` | 字体说明 · LaTeX 模板 · scenes.json 模板 |
| 人工文档 | `使用说明.pdf` · `成本估算.pdf` | 给客户本人阅读：环境安装/操作手册 与 Token 消耗费用估算 |

## 三、标准工作流（8 步）

0. **立项**：新建项目文件夹（建议 `_proj-<主题>/`），从样板间拷 `assets/portraits/` 结构与任一场景源码作骨架。
1. **分幕脚本**：按 `references/style-guide.md` 写场景类。每幕一个 `construct`，一幕 30~90 秒，自包含（常量+基类复制进文件，禁止跨文件 import 场景）。`MathTex` 里**严禁汉字**。
2. **单幕烟测**：`manim -ql 你的文件.py 场景类` 秒级出 480p，抽帧查排版（零重叠/防截断）。
3. **渲染缝合**：写 `build/scenes.json`（模板在 `assets/templates/scenes.template.json`），然后
   `python scripts/build_film.py build/scenes.json`（增量：`--only 场景名`；烟测：`--quality ql`）。
4. **重建时间轴**：按 `references/timeline-dubbing.md` 从源码逐段累加时长，**硬自检**：累加值 = ffprobe 实测（误差 ≤0.5s），必要时探针抽帧定位漂移。绝不靠目测抽帧建段落表。
5. **段落表+文案**：写 `work/dub_config.json`（26 段实例见样板间）。字数预算 ≈ (段长−0.7s)×4.6 字（实测语速），风趣但严格对应画面。
6. **配音合成**：`python scripts/dub_pipeline.py work/dub_config.json`
   自动完成：分段 TTS（重试+静音裁剪+文案哈希缓存）→ 级联排程 → ffmpeg 混流 → 成片。自备录音替换法见同文档。
7. **复检验收**：`python scripts/verify_film.py --master 母带.mp4 --dubbed 成片.mp4 --probes 5.5,11.2,143`
   硬标准：成片时长=源片±0.5s；响度 -20~-30dB 且无死气段；探针帧音画对位。
8. **交付**：`out/` 成片 + `out/段落表.txt` + 配音稿 md。交付前跑一遍 verify 拿全绿。

## 四、铁律速查（血泪 top 8，全表见 references/troubleshooting.md）

1. `MathTex` 中**严禁汉字**（LaTeX 无 ctex 必炸）——中文一律 `Text(zh_font=...)`，混排用 `VGroup(zh(...), mt(...)).arrange(RIGHT)`。
2. `ImageMobject` **不是** VMobject——多对象组合放 `Group`，放 `VGroup` 会崩。
3. Surface 系（`Cylinder`/`Sphere`）传 `fill_color` **不生效**（默认青色棋盘格）——必须 `checkerboard_colors=[亮色,暗色]`，纯色层用 `checkerboard_colors=False`。
4. 无 `run_time` 的 `self.play(...)` 按 1.0s 计，混合动画取最大值；时间轴累加必须逐段核对。
5. 上半区文字（`build_deduction_block`，y>0）与下半区图形（`shift(DOWN*1.9~2.0)`）绝对隔离；一切对象 `fit(width≤13.6)` 防截断。
6. 脚本零硬编码用户路径——一律 `BASE_DIR = os.path.dirname(os.path.abspath(__file__))`。
7. TTS 断连/超长是常态——管线已内置重试与哈希缓存，改文案只重配受影响段，不要整批重跑。
8. 时间轴对不上 ≠ 推倒重来：用「边界+0.4s 探针帧」定位漂移集中在哪几段，只修那几段。

## 五、长视频（30~60 分钟）——结论：没问题

架构天然支持：**一幕一文件、一章一清单、分章配音、无损缝合、哈希缓存增量重配**。
1 小时 ≈ 45~60 幕；渲染约为成片时长的 8~20 倍机器时间（可分章无人值守跑一晚）；TTS 免费且按段缓存。
操作细节、工程结构与断点续作规范见 **`references/long-film-playbook.md`**。

## 六、references 索引

> 接到"把这份讲义/文章做成这种风格的视频"类任务时，**先读根目录 `AGENT-实操指南.md`**（内容转化算法：任意内容 → 幕清单 → 视觉隐喻映射），再按下表按需翻阅。

| 文件 | 什么时候读 |
|---|---|
| `style-guide.md` | 写任何场景代码之前（版式/字体/颜色/组件契约/3D 规范） |
| `timeline-dubbing.md` | 进入配音阶段（时间轴重建/探针/字数预算/自备录音） |
| `long-film-playbook.md` | 立项超过 10 幕的项目（章节化/增量/产能估算） |
| `web-image-sourcing.md` | 需要历史人物肖像、插图素材（联网搜图+版权红线） |
| `troubleshooting.md` | 报错时先查这里，再动手修 |
