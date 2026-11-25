# 样板间：《实数完备性全景大电影》

这是本 skill 的完整可运行样例（输入输出配对的标准）：**3D 片头神殿 → 扩充历史篇（四大立法者）
→ 六大完备性定理逐一证明 → 3D 等价闭环终章**，26 段配音逐句对齐，144.1 秒，1080P60。

## 看效果

```
out/实数完备性大电影_配音版_1080P60.mp4     ← 带配音成片（直接播放）
```

## 复现它（在新机器上验证 skill 装好了）

```bash
# 0) 前置：pip install manim edge-tts；装好 ffmpeg 与 LaTeX（见 SKILL.md 环境表）

# 1) 渲染 11 幕并缝合母带（约 20~40 分钟机器时间；烟测单幕可加 --quality ql --only Scene00_ColdOpen3D）
python ../../scripts/build_film.py build/scenes.json

# 2) 配音合成（TTS 免费联网；约 3 分钟）
python ../../scripts/dub_pipeline.py work/dub_config.json

# 3) 复检验收
python ../../scripts/verify_film.py --master out/episodes/实数完备性全景大电影_楷体大字母带_1080P60.mp4 \
    --dubbed out/实数完备性大电影_配音版_1080P60.mp4 \
    --scenes-json build/scenes.json --probes 5.5,60,143 --probe-dir out/probes
```

## 文件导读

| 文件 | 学什么 |
|---|---|
| `real_number_cold_open_3d.py` | 3D 片头神殿：六根彩色圆柱环绕金色实数核（含 Surface 彩色渲染的正确写法） |
| `real_number_history_expanded.py` | 历史篇：肖像相框卡片 + 左图右推导的个人镜头模式 |
| `real_number_kaiti_master.py` | 六大定理九幕：数轴可视化、上半区推导、反证法动画的标准写法 |
| `配音稿_实数完备性大电影.md` | 26 段段落表（画面时间/音频时间/文案）与配音方法全记录 |
| `work/dub_config.json` | 配音管线输入格式实例 |
| `assets/portraits/` | 联网搜集的四位数学家肖像（照片版 + 版画版两套，见 references/web-image-sourcing.md） |
| `大字楷体分幕精选/` | 11 幕独立 1080P60 高清分幕视频（`00_片头_六柱环核3D.mp4` 至 `09_终章_3D等价闭环星系.mp4`） |
| `build_kaiti_master.py` / `concat_kaiti_list.txt` | 原工程独立一键全量渲染与无损缝合脚本 |
| `交接文档.md` / `README_原工程说明.md` | 原工程技术交接说明、避坑经验与历史版本归档（`work/` 含旧版 `v2` 配音脚本/配置及 `00_历史篇_旧版备份.mp4`） |
