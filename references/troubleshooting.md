# 避坑清单（报错先查这里）

> 每一条都在样板间项目里真实踩过。按「症状 → 原因 → 修法」组织。

## A. 渲染崩溃类

### A1. MathTex 抛 `Unicode character` 致命错误
- **症状**：`! LaTeX Error: Unicode character 挑 not set up for use with LaTeX.`
- **原因**：MathTex 里写了汉字（如 `\text{挑选子列}`）。
- **修法**：中文一律 `Text(font=ZH_FONT)`；混排：
  `VGroup(self.zh("挑选子列 "), self.mt(r"x_{n_k} \to \xi")).arrange(RIGHT, buff=0.1)`。

### A2. 含图片的组合动画报错 / 行为异常
- **原因**：`ImageMobject` 不是 VMobject，放进 `VGroup` 会崩或行为怪异。
- **修法**：用 `Group`。`card = Group(frame_box, img, t_name, t_desc)`。

### A3. Cylinder / Sphere 全是青色棋盘格，fill_color 不生效
- **原因**：manim CE 的 Surface 系默认 `checkerboard_colors=[青, 深青]`，盖过 fill_color。
- **修法**：传 `checkerboard_colors=[亮色, 暗色]`（用 `interpolate_color(ManimColor(col), ...)` 生成同色系深浅）；
  纯色半透明层传 `checkerboard_colors=False`。详见 style-guide §6。

### A4. LaTeX 缺失 / dvisvgm 报错
- MathTex 依赖本机 LaTeX（MacTeX/MiKTeX/TeX Live）。CI 或新机器渲染前先 `latex --version` 验证。

## B. 版式类

### B1. 文字压到数轴 / 标签重叠
- **修法**：数轴 `shift(DOWN*1.9~2.0)`；推导区只住上半屏；多参考线标签一个 `UL` 一个 `UR`；
  区间标记放刻度数字**正下方** `buff≈0.68`。改完必抽帧确认。

### B2. 长公式超出画面
- **修法**：所有行进 `fit(width=13.6)`；仍超则拆两行或减字号（公式 ≥34 再降）。

### B3. 字体在别的电脑上不是楷体
- **修法**：场景文件顶部用 style-guide §2 的字体检测片段，候选列表依次回退；
  Linux 装 `fonts-arphic-ukai` 或霞鹜文楷（assets/fonts/字体说明.md）。

## C. 时间轴与配音类

### C1. 时间轴累加与实际时长对不上
- **先查**：`clear_scene` 的 0.6s 漏加；无 `run_time` 的 play 按 1.0s（混合动画取最大值）；
  `Flash` 默认 1.0s；3D 场景 `move_camera(run_time=...)` 也是一次 play。
- **再查**：漂移定位（探针帧法，见 timeline-dubbing §2），只修漂移段。

### C2. TTS 断连 `Cannot connect to speech.platform.bing.com` / `ConnectionResetError`
- 管线已内置 5 次指数退避重试；仍失败多为网络波动，隔几分钟重跑（哈希缓存会跳过已成功段）。

### C3. TTS 普遍超长（LONG）
- 本机语速 ≠ 经验语速。看管线打印的「建议删 N 字」**改文案**，不要硬提语速（+24% 以上会机 stiffness）。
- 长期方案：首次跑一个 3 段小 config 校准本项目机器的实测语速，更新段落预算系数。

### C4. 配音成片某段纯静音（-90dB 级）
- 该段画面长、文案短留了 5s+ 死气。把该段文案补到预算上限重配（缓存保证只重配这一段）。

### C5. 客户自备录音替换后后段顺延
- 录音超长。剪短到 ≈ 段长 − 0.7s，或在 config 增大该段 `end` 并回源码加 hold（音画一起改）。

## D. 工程类

### D1. 换电脑路径炸
- 一切脚本用 `BASE_DIR = os.path.dirname(os.path.abspath(__file__))` 与参数传入的 config；
  ffmpeg/ffprobe/manim 用 `shutil.which` 探测（scripts/ 已全部内置），禁止写死 `/Users/xxx`。

### D2. 会话回显污染（同形异码字）
- 中文路径在终端回显里可能被搅乱。对策：路径 `find ... | head -1` 现场解析后以变量引用；
  **只信程序自检输出**（语法检查、时长校验、排程表），不信回显文本。

### D3. 大批量任务被 OOM kill（exit 137）
- 拆批。渲染按章、配音按章，别一口气吞全片。

### D4. PDF/视频文件被占用无法覆盖（Windows 常见）
- 输出到新文件名（加时间戳），提示用户手动改名；不要反复硬写。

### D5. ffmpeg 无 drawtext 滤镜（部分 homebrew 构建）
- **烧字幕路线在本机不可用**；字幕需求一律走 Manim 内 `Text` 或外挂软字幕。

## E. 审美回归类（用户验收红线）

- 每幕 ≤3 行推导；一幕一个核心视觉；颜色语义不混用（红=矛盾/上界警示，绿=结论/极限，黄=核心高亮）。
- 改动任何已验收的幕之前，先抽原帧留档，改完并排对比再交付。
