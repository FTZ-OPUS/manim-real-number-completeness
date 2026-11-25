# 版式与代码规范（楷体大字讲义电影）

> 写任何场景代码之前必读。规范源头是样板间项目实测验证过的写法，照抄结构最稳。

## 1. 画布与全局常量

```python
config.pixel_width  = 1920          # 16:9 横屏
config.pixel_height = 1080
config.frame_width  = 16.0          # 画布宽 16 单位、高 9 单位
config.frame_height = 9.0
config.background_color = "#0F1720" # 深蓝黑底
```

渲染档位：`-ql` 480p15 烟测 / `-qm` 720p30 / `-qh` 1080p60 正式。**交付一律 1080P60**。

## 2. 中文字体策略（跨平台）

代码中字体是一个常量，跨机器运行前先确认本机可用楷体系字体：

```python
# 用 matplotlib（manim 必依赖，无需额外安装）检测可用字体
from matplotlib import font_manager
installed = {f.name for f in font_manager.fontManager.ttflist}
for name in ["Kaiti SC", "STKaiti", "KaiTi", "楷体", "AR PL UKai CN",
             "LXGW WenKai", "Noto Serif CJK SC"]:
    if name in installed:
        ZH_FONT = name
        break
```

- macOS：`Kaiti SC` 系统自带（样板间默认）。
- Windows：`KaiTi` / `楷体` 自带。
- Linux：装 `fonts-arphic-ukai`，或推荐开源 **霞鹜文楷 LXGW WenKai**（OFL 协议，效果最接近），见 `assets/fonts/字体说明.md`。

## 3. 颜色主题（样板间全片统一）

| 常量 | HEX | 用途 |
|---|---|---|
| `BG` | `#0F1720` | 背景 |
| `INK` | `#F6F2EA` | 正文暖白 |
| `MUTED` | `#A9B4C2` | 辅助灰字 |
| `BLUE` | `#5DADEC` | 标题/步骤 |
| `GREEN` | `#66D19E` | 结论/定理 |
| `YELLOW` | `#FFD166` | 核心高亮 |
| `ORANGE` | `#F59E62` | 辅助强调 |
| `RED` | `#FF6B6B` | 警示/矛盾 |
| `VIOLET` | `#B79CFF` | 典雅紫 |
| `GOLD` | `#F0A500` | 3D 金色核心 |

## 4. 基类 `BaseKaitiScene`（整段复制进每个场景文件）

```python
class BaseKaitiScene(Scene):
    def zh(self, content, font_size=36, color=INK, weight=NORMAL):
        return Text(content, font=ZH_FONT, font_size=font_size, color=color, weight=weight)

    def mt(self, content, font_size=46, color=INK, stroke_width=1):
        return MathTex(content, font_size=font_size, color=color, stroke_width=stroke_width)

    def title_bar(self, text, color=BLUE):
        title = self.zh(text, font_size=46, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        return VGroup(title)

    def fit(self, mob, width=13.8, height=None):
        target_width = width if width is not None else config.frame_width - 2.2
        target_height = height if height is not None else config.frame_height - 1.2
        if mob.width > target_width:  mob.scale_to_fit_width(target_width)
        if mob.height > target_height: mob.scale_to_fit_height(target_height)
        return mob

    def build_deduction_block(self, bar, rows, top_buff=0.42, row_buff=0.32):
        fitted_rows = [self.fit(r, width=13.6) for r in rows]
        content = VGroup(*fitted_rows).arrange(DOWN, buff=row_buff, aligned_edge=LEFT)
        content.next_to(bar, DOWN, buff=top_buff)
        content.to_edge(LEFT, buff=1.2)
        return content

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.6)
```

组件契约：
- `zh()` 只装中文；`mt()` 只装 LaTeX（**禁汉字**）；混排行 `VGroup(zh, mt).arrange(RIGHT, buff=0.1)`。
- `title_bar` 固定顶部；`build_deduction_block` 限制推导区在上半屏（y>0）。
- 每幕结尾 `clear_scene()`（末幕 3D 可改为整体 FadeOut），保证幕与幕之间干净切换。

## 5. 零重叠版式三原则

1. **上下隔离**：数轴/几何图形统一 `shift(DOWN * 1.9)` 到 `DOWN * 2.0`；文字推导只住上半屏。
2. **左右避让**：同一数轴上多条参考线的标签错开（一个 `UL` 一个 `UR`）；区间标记放刻度数字**正下方** `buff≈0.68`，不许压刻度。
3. **防截断**：任何行先进 `fit(width=13.6)` 再排版；新增元素后抽帧确认边界。

## 6. 3D 场景规范（片头神殿 / 终章模式）

```python
class MyTemple3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15~0.18)   # 环绕旋转
        # 2D 覆盖层（标题/HUD）必须 add_fixed_in_frame_mobjects 后再 FadeIn
        # 3D 阵列绕核自转：self.play(Rotate(assembly, angle=TAU/12), run_time=3.2)
        self.stop_ambient_camera_rotation()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
```

**彩色渲染（重要）**：`Cylinder`/`Sphere` 直接传 `fill_color` 不生效（默认青色棋盘格）：

```python
def shaded_pair(col):   # 同色系深浅棋盘，保立体感又显彩色
    c = ManimColor(col)
    return [interpolate_color(c, ManimColor("#FFFFFF"), 0.22),
            interpolate_color(c, ManimColor("#000000"), 0.30)]

Cylinder(radius=0.27, height=1.7, fill_color=col, fill_opacity=0.92,
         checkerboard_colors=shaded_pair(col), stroke_width=0)
Sphere(radius=1.0, fill_color=GOLD, fill_opacity=0.12, checkerboard_colors=False)  # 纯色光晕层
```

- 片头神殿配方：六根双层发光彩柱（内芯 0.92 实色 + 外层 0.25 光罩）+ 同色 `Annulus` 基准环 + 彩虹 `Line3D` 闭环 + 中心金色球体+光晕。
- `Line3D(p1, p2, color=col, thickness=0.03)` 可直接着色，不受棋盘格影响。

## 7. 节奏与时长预算

| 元素 | 建议时长 |
|---|---|
| 标题 Write | 0.8~0.9s |
| 单行推导 FadeIn | 0.7s（每幕 ≤3 行） |
| 数轴/图形 Create | 0.9~1.2s |
| 每幕收尾 hold（self.wait） | 2.2~3.2s（配音段的呼吸空间） |
| 一幕总长 | 30~90s，超长拆幕 |
| clear_scene | 0.6s（算进时间轴！） |

所有 `run_time` **显式写出来**，不要依赖默认值——时间轴重建全靠它们。
