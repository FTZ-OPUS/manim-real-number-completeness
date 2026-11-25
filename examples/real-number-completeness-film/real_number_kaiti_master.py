"""
=============================================================================
  项目：实数系的建立与实数完备性全景大电影 (楷体大字高奢版)
  遵循：横屏大·字公式标准 (16:9, KaiTi SC, 优雅深暗底色, 严禁文字图像重叠)
  特性：
    - 历史篇：包含戴德金、康托尔、魏尔斯特拉斯、柯西真实历史肖像与创立史
    - 六大定理专属可视化与严格推导证明 (确界、单调有界、区间套、致密性、有限覆盖、柯西)
    - 三维空间拓展：3D 嵌套立方体 (区间套高维推广) + 3D 六大定理闭环等价神殿
=============================================================================
"""

from manim import *
import numpy as np
import os

# -------------------------------------------------------------
# 1. 全局配置与横屏大字常量 (基于横屏大字 Manim 规范)
# -------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0

ZH_FONT = "Kaiti SC"
BG     = "#0F1720"   # 深蓝黑背景
INK    = "#F6F2EA"   # 暖白正文
MUTED  = "#A9B4C2"   # 灰字辅助
BLUE   = "#5DADEC"   # 标题/步骤
GREEN  = "#66D19E"   # 结论/定理
YELLOW = "#FFD166"   # 核心高亮
ORANGE = "#F59E62"   # 辅助强调
RED    = "#FF6B6B"   # 警示/矛盾
VIOLET = "#B79CFF"   # 典雅紫
READ_PAUSE = 1.6     # 停顿节奏

config.background_color = BG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTRAITS_DIR = os.path.join(BASE_DIR, "assets", "portraits")


# -------------------------------------------------------------
# 基础公共类：提供横屏大字标准组件与防重叠排版引擎
# -------------------------------------------------------------
class BaseKaitiScene(Scene):
    def zh(self, content, font_size=36, color=INK, weight=NORMAL):
        return Text(content, font=ZH_FONT, font_size=font_size, color=color, weight=weight)

    def mt(self, content, font_size=46, color=INK, stroke_width=1):
        return MathTex(content, font_size=font_size, color=color, stroke_width=stroke_width)

    def mt_small(self, content, font_size=38, color=INK):
        return self.mt(content, font_size=font_size, color=color)

    def title_bar(self, text, color=BLUE):
        title = self.zh(text, font_size=46, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        return VGroup(title)

    def fit(self, mob, width=13.8, height=None):
        target_width = width if width is not None else config.frame_width - 2.2
        target_height = height if height is not None else config.frame_height - 1.2
        if mob.width > target_width:
            mob.scale_to_fit_width(target_width)
        if mob.height > target_height:
            mob.scale_to_fit_height(target_height)
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


# =============================================================================
# 0. 历史篇：实数完备性的诞生与四大巨匠 (History & Portraits)
# =============================================================================
class Scene00_History(BaseKaitiScene):
    """
    序幕：分析学危机与实数创立史 (戴德金、康托尔、魏尔斯特拉斯、柯西)
    """
    def construct(self):
        # 1. 标题
        bar = self.title_bar("微积分的地基危机：实数完备性的诞生史")
        self.play(Write(bar), run_time=0.9)

        line1 = self.zh("19 世纪初，微积分已被广泛应用，但底层逻辑却危机四伏：", font_size=34, color=MUTED)
        line2 = self.zh("• 连续性是什么？无理数是什么？极限究竟走向何方？", font_size=36, color=ORANGE)
        line3 = self.zh("四位数学巨匠横空出世，彻底驱逐微积分中的直觉幽灵，铸造严密分析大厦！", font_size=34, color=GREEN)

        intro = self.build_deduction_block(bar, [line1, line2, line3], top_buff=0.7, row_buff=0.6)
        for l in [line1, line2, line3]:
            self.play(FadeIn(l, shift=UP * 0.15), run_time=0.7)
        self.wait(2.2)
        self.clear_scene()

        # 2. 四大数学家画卷肖像
        bar2 = self.title_bar("实数论的四位立法者")
        self.play(Write(bar2), run_time=0.8)

        mathematicians = [
            ("cauchy.jpg", "柯西 (A. Cauchy)", "1821 极限与收敛准则", BLUE),
            ("weierstrass.jpg", "魏尔斯特拉斯 (K. Weierstrass)", "现代分析之父 / 确界致密", YELLOW),
            ("dedekind.jpg", "戴德金 (R. Dedekind)", "1872 戴德金分割创立实数", RED),
            ("cantor.jpg", "康托尔 (G. Cantor)", "1872 基本列等价与区间套", GREEN),
        ]

        cards = Group()
        for idx, (img_name, name, desc, col) in enumerate(mathematicians):
            img_path = os.path.join(PORTRAITS_DIR, img_name)
            img = ImageMobject(img_path)
            img.scale_to_fit_height(3.0)

            # 圆角相框
            frame_box = RoundedRectangle(
                corner_radius=0.15,
                width=img.width + 0.25,
                height=img.height + 0.25,
                stroke_color=col,
                stroke_width=2.5,
                fill_color="#182230",
                fill_opacity=0.9
            )
            img.move_to(frame_box.get_center())

            t_name = self.zh(name, font_size=26, color=INK, weight=BOLD).next_to(frame_box, DOWN, buff=0.15)
            t_desc = self.zh(desc, font_size=20, color=MUTED).next_to(t_name, DOWN, buff=0.1)

            card_group = Group(frame_box, img, t_name, t_desc)
            cards.add(card_group)

        cards.arrange(RIGHT, buff=0.45).next_to(bar2, DOWN, buff=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards], lag_ratio=0.2), run_time=2.2)
        self.wait(3.0)
        self.clear_scene()


# =============================================================================
# 1. 戴德金分割 (Dedekind Cut) —— 实数的创立
# =============================================================================
class Scene01_DedekindCut(BaseKaitiScene):
    def construct(self):
        bar = self.title_bar("实数的创立：戴德金分割 (Dedekind Cut, 1872)")
        self.play(Write(bar), run_time=0.8)

        # 几何演示区：数轴与分割 (下移至 y = -1.9，与上方文字完全隔离)
        line = NumberLine(x_range=[-1, 3, 1], length=11.5, color=MUTED, include_numbers=True, font_size=32).shift(DOWN * 1.9)
        self.play(Create(line), run_time=0.9)

        sqrt2 = 1.41421356
        cut_pt = line.number_to_point(sqrt2)

        # 刀刃与左右集
        blade = DashedLine(cut_pt + UP * 1.0, cut_pt + DOWN * 1.0, color=RED, stroke_width=3.5)
        blade_lbl = self.zh("分割切面 (A | B)", font_size=26, color=RED).next_to(blade, UP, buff=0.12)

        seg_A = Line(line.number_to_point(-1), cut_pt, color=BLUE, stroke_width=7)
        seg_B = Line(cut_pt, line.number_to_point(3), color=YELLOW, stroke_width=7)

        self.play(Create(blade), FadeIn(blade_lbl), Create(seg_A), Create(seg_B), run_time=1.2)

        # 上方严密推导行
        row1 = VGroup(
            self.zh("左集合 A：", font_size=32, color=BLUE),
            self.mt(r"A = \{ x \in \mathbb{Q} \mid x \le 0 \text{ or } x^2 < 2 \}", font_size=42, color=BLUE)
        ).arrange(RIGHT, buff=0.12)

        row2 = VGroup(
            self.zh("右集合 B：", font_size=32, color=YELLOW),
            self.mt(r"B = \{ x \in \mathbb{Q} \mid x > 0 \text{ and } x^2 > 2 \}", font_size=42, color=YELLOW)
        ).arrange(RIGHT, buff=0.12)

        row3 = VGroup(
            self.zh("核心洞察：", font_size=32, color=GREEN),
            self.zh("A 中无最大有理数，B 中无最小有理数。分割 (A, B) 唯一确定了 ", font_size=28, color=INK),
            self.mt(r"\sqrt{2} \in \mathbb{R}", font_size=36, color=GREEN),
            self.zh("！", font_size=28, color=GREEN),
        ).arrange(RIGHT, buff=0.08)

        content = self.build_deduction_block(bar, [row1, row2, row3], top_buff=0.45, row_buff=0.35)

        for r in [row1, row2, row3]:
            self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.7)

        # 闪烁实数点
        real_dot = Dot(cut_pt, radius=0.12, color=GREEN)
        real_lbl = self.mt(r"\sqrt{2} \in \mathbb{R}", font_size=44, color=GREEN).next_to(real_dot, UP, buff=0.25)
        self.play(Transform(blade, real_dot), FadeOut(blade_lbl), FadeIn(real_lbl), Flash(cut_pt, color=GREEN, num_lines=16), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()


# =============================================================================
# 2. 定理一：确界原理 (Supremum Principle) 与证明
# =============================================================================
class Scene02_SupremumPrinciple(BaseKaitiScene):
    def construct(self):
        bar = self.title_bar("定理一：确界原理 (Supremum Principle)")
        self.play(Write(bar), run_time=0.8)

        # 下方几何数轴：y = -1.9
        line = NumberLine(x_range=[0, 5, 1], length=11.5, color=MUTED, include_numbers=True, font_size=32).shift(DOWN * 1.9)
        self.play(Create(line), run_time=0.9)

        # 集合点群
        np.random.seed(42)
        vals = [1.2 + 2.15 * (1 - 0.5**i) for i in range(1, 12)] + list(np.random.uniform(1.2, 3.2, 18))
        dots = VGroup(*[Dot(line.number_to_point(v), radius=0.045, color=BLUE, fill_opacity=0.8) for v in vals])
        self.play(FadeIn(dots), run_time=0.8)

        # 上确界位置 beta = 3.35
        sup_pt = line.number_to_point(3.35)
        barrier = Line(sup_pt + UP * 0.9, sup_pt + DOWN * 0.9, color=YELLOW, stroke_width=4.5)
        barrier_lbl = self.mt(r"\sup S = \beta", font_size=42, color=YELLOW).next_to(barrier, UP, buff=0.12)
        self.play(Create(barrier), FadeIn(barrier_lbl), Flash(sup_pt, color=YELLOW))

        # 上半区 3 行严密证明推导
        row1 = VGroup(
            self.zh("定理表述：", font_size=32, color=BLUE),
            self.zh("非空有上界的实数集 S，必有唯一的最小上界 ", font_size=30, color=INK),
            self.mt(r"\beta = \sup S", font_size=38, color=YELLOW)
        ).arrange(RIGHT, buff=0.1)

        row2 = VGroup(
            self.zh("ε 判定准则：", font_size=32, color=YELLOW),
            self.mt(r"\forall \varepsilon > 0, \quad \exists x \in S : \quad \beta - \varepsilon < x \le \beta", font_size=40, color=YELLOW)
        ).arrange(RIGHT, buff=0.1)

        row3 = VGroup(
            self.zh("反证推导：", font_size=32, color=GREEN),
            self.zh("若 ", font_size=30, color=INK),
            self.mt(r"\beta - \varepsilon", font_size=36, color=INK),
            self.zh(" 仍为上界，则与 ", font_size=30, color=INK),
            self.mt(r"\beta", font_size=36, color=YELLOW),
            self.zh(" 是「最小」上界产生矛盾！", font_size=30, color=RED)
        ).arrange(RIGHT, buff=0.08)

        content = self.build_deduction_block(bar, [row1, row2, row3], top_buff=0.45, row_buff=0.35)

        for r in [row1, row2, row3]:
            self.play(FadeIn(r, shift=UP * 0.1), run_time=0.7)
        self.wait(3.0)
        self.clear_scene()


# =============================================================================
# 3. 定理二：单调有界定理 (Monotone Convergence) 与证明
# =============================================================================
class Scene03_MonotoneConvergence(BaseKaitiScene):
    def construct(self):
        bar = self.title_bar("定理二：单调有界定理 (Monotone Convergence)")
        self.play(Write(bar), run_time=0.8)

        # 下方几何数轴：y = -1.9
        line = NumberLine(x_range=[0, 4, 1], length=11.5, color=MUTED, include_numbers=True, font_size=32).shift(DOWN * 1.9)
        self.play(Create(line), run_time=0.9)

        # 极限线 L = 3.0 (向左放置标签，彻底避免碰撞)
        limit_pt = line.number_to_point(3.0)
        limit_line = Line(limit_pt + UP * 0.9, limit_pt + DOWN * 0.9, color=GREEN, stroke_width=3.5)
        limit_lbl = self.mt(r"L = \sup\{a_n\}", font_size=36, color=GREEN).next_to(limit_line.get_top(), UL, buff=0.1)

        # 天花板上界 M = 3.6 (向右放置标签，两标签横向间距充分，零重叠)
        ceiling_pt = line.number_to_point(3.6)
        ceiling = Line(ceiling_pt + UP * 0.9, ceiling_pt + DOWN * 0.9, color=RED, stroke_width=3.5)
        ceiling_lbl = VGroup(
            self.zh("上界", font_size=26, color=RED),
            self.mt("M = 3.6", font_size=30, color=RED)
        ).arrange(RIGHT, buff=0.06).next_to(ceiling.get_top(), UR, buff=0.1)

        seq_dots = VGroup(*[Dot(line.number_to_point(3.0 - 1.8 * (0.55**n)), radius=0.055, color=BLUE) for n in range(1, 8)])

        self.play(Create(ceiling), FadeIn(ceiling_lbl), LaggedStart(*[FadeIn(d) for d in seq_dots], lag_ratio=0.1), run_time=1.2)
        self.play(Create(limit_line), FadeIn(limit_lbl), Flash(limit_pt, color=GREEN))

        # 上半区推导行
        row1 = VGroup(
            self.zh("第一步（确界构造）：", font_size=30, color=BLUE),
            self.zh("令序列值域集 ", font_size=28, color=INK),
            self.mt(r"E = \{a_n\}", font_size=34, color=BLUE),
            self.zh("，由确界原理必存在最小上界 ", font_size=28, color=INK),
            self.mt(r"L = \sup E", font_size=34, color=GREEN)
        ).arrange(RIGHT, buff=0.08)

        row2 = VGroup(
            self.zh("第二步（ε 捕获）：", font_size=30, color=YELLOW),
            self.mt(r"\forall \varepsilon > 0, \quad \exists N \in \mathbb{N} : \quad L - \varepsilon < a_N \le L", font_size=38, color=YELLOW)
        ).arrange(RIGHT, buff=0.1)

        row3 = VGroup(
            self.zh("第三步（单调性收敛）：", font_size=30, color=GREEN),
            self.mt(r"\forall n > N, \quad L - \varepsilon < a_N \le a_n \le L \implies |a_n - L| < \varepsilon", font_size=36, color=GREEN)
        ).arrange(RIGHT, buff=0.1)

        content = self.build_deduction_block(bar, [row1, row2, row3], top_buff=0.45, row_buff=0.35)

        for r in [row1, row2, row3]:
            self.play(FadeIn(r, shift=UP * 0.1), run_time=0.7)
        self.wait(3.0)
        self.clear_scene()


# =============================================================================
# 4. 定理三：区间套定理 (Nested Intervals) —— 1D 与 3D 嵌套立方体
# =============================================================================
class Scene04_NestedIntervals(BaseKaitiScene):
    def construct(self):
        bar = self.title_bar("定理三：区间套定理 (Nested Interval Theorem)")
        self.play(Write(bar), run_time=0.8)

        # 几何数轴：y = -1.9
        line = NumberLine(x_range=[0, 4, 1], length=11.5, color=MUTED, include_numbers=True, font_size=32).shift(DOWN * 1.9)
        self.play(Create(line), run_time=0.9)

        intervals_info = [
            (0.8, 3.8, r"[a_1, b_1]", UP * 0.9, BLUE),
            (1.5, 3.2, r"[a_2, b_2]", UP * 0.5, YELLOW),
            (2.1, 2.7, r"[a_3, b_3]", UP * 0.1, GREEN),
        ]
        int_group = VGroup()
        for a, b, lbl_tex, sh, col in intervals_info:
            p_a = line.number_to_point(a)
            p_b = line.number_to_point(b)
            seg = Line(p_a, p_b, color=col, stroke_width=6).shift(sh)
            t_l = self.zh("[", font_size=36, color=col, weight=BOLD).move_to(p_a).shift(sh)
            t_r = self.zh("]", font_size=36, color=col, weight=BOLD).move_to(p_b).shift(sh)
            tag = self.mt(lbl_tex, font_size=26, color=WHITE).next_to(seg, UP, buff=0.06)
            int_group.add(VGroup(seg, t_l, t_r, tag))

        self.play(LaggedStart(*[FadeIn(it) for it in int_group], lag_ratio=0.15), run_time=1.4)

        # 上半区推导行
        row1 = VGroup(
            self.zh("定理表述：", font_size=32, color=BLUE),
            self.zh("闭区间套 ", font_size=30, color=INK),
            self.mt(r"[a_n, b_n]", font_size=36, color=YELLOW),
            self.zh(" 逐层嵌套且长度趋于 0，其交集必为唯一实数 ", font_size=30, color=INK),
            self.mt(r"\xi \in \mathbb{R}", font_size=36, color=GREEN)
        ).arrange(RIGHT, buff=0.08)

        row2 = VGroup(
            self.zh("证明（由单调有界导出）：", font_size=30, color=BLUE),
            self.mt(r"a_1 \le a_n \le b_1 \implies \lim a_n = \xi, \quad \lim b_n = \eta", font_size=38, color=BLUE)
        ).arrange(RIGHT, buff=0.1)

        row3 = VGroup(
            self.zh("端点重合收缩：", font_size=30, color=GREEN),
            self.mt(r"\lim (b_n - a_n) = 0 \implies \xi = \eta \implies \bigcap_{n=1}^\infty [a_n, b_n] = \{\xi\}", font_size=38, color=GREEN)
        ).arrange(RIGHT, buff=0.1)

        content = self.build_deduction_block(bar, [row1, row2, row3], top_buff=0.45, row_buff=0.35)

        for r in [row1, row2, row3]:
            self.play(FadeIn(r, shift=UP * 0.1), run_time=0.7)
        self.wait(3.0)
        self.clear_scene()


class Scene04_NestedIntervals3D(ThreeDScene):
    """
    高维震撼演示：三维空间区间套定理 (高维康托尔闭包定理 —— 嵌套立方体)
    """
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)

        # 2D 顶层悬浮标题
        t_bar = Text("三维空间区间套拓展：嵌套立方体定理 (R³)", font=ZH_FONT, font_size=46, color=BLUE, weight=BOLD)
        t_bar.to_edge(UP, buff=0.45)
        t_sub = Text("高维闭立方体逐层嵌套收缩：体积趋于0时，唯一锁定三维空间实数点 (ξ, η, ζ)", font=ZH_FONT, font_size=28, color=MUTED)
        t_sub.next_to(t_bar, DOWN, buff=0.12)

        # 底部左右悬浮徽章
        hud_left = VGroup(
            Text("三维闭立方体套：", font=ZH_FONT, font_size=24, color=YELLOW),
            MathTex(r"Q_1 \supset Q_2 \supset Q_3 \supset Q_4", font_size=30, color=YELLOW)
        ).arrange(RIGHT, buff=0.1).to_corner(DL, buff=0.55)

        hud_right = VGroup(
            Text("体积收缩交集：", font=ZH_FONT, font_size=24, color=GREEN),
            MathTex(r"\lim \mathrm{Vol}(Q_n) = 0 \implies \bigcap Q_n = \{P_0\}", font_size=30, color=GREEN)
        ).arrange(RIGHT, buff=0.1).to_corner(DR, buff=0.55)

        self.add_fixed_in_frame_mobjects(t_bar, t_sub, hud_left, hud_right)
        self.play(FadeIn(t_bar), FadeIn(t_sub), FadeIn(hud_left), FadeIn(hud_right), run_time=1.0)

        # 4 个层层嵌套的高清发光半透明立方体
        cubes_data = [
            (3.8, BLUE, 0.22),
            (2.4, YELLOW, 0.35),
            (1.4, VIOLET, 0.50),
            (0.6, GREEN, 0.75),
        ]

        cubes = VGroup()
        for side, col, opac in cubes_data:
            c = Cube(side_length=side, fill_color=col, fill_opacity=opac, stroke_width=2.5, stroke_color=col)
            cubes.add(c)

        # 逐层套入
        for cube in cubes:
            self.play(FadeIn(cube, scale=0.7), run_time=0.9)
            self.wait(0.3)

        # 奇点诞生
        core_pt = Sphere(radius=0.15, color=RED, fill_opacity=1.0)
        self.play(GrowFromCenter(core_pt), run_time=1.2)
        self.wait(3.0)


# =============================================================================
# 5. 定理四：致密性定理 (Bolzano-Weierstrass) 与二分证明
# =============================================================================
class Scene05_BolzanoWeierstrass(BaseKaitiScene):
    def construct(self):
        bar = self.title_bar("定理四：致密性定理 (Bolzano-Weierstrass)")
        self.play(Write(bar), run_time=0.8)

        # 下方几何数轴：y = -1.9
        line = NumberLine(x_range=[0, 4, 1], length=11.5, color=MUTED, include_numbers=True, font_size=32).shift(DOWN * 1.9)
        self.play(Create(line), run_time=0.9)

        # 聚点分布
        np.random.seed(99)
        cluster_xi = 2.6
        vals = list(np.random.normal(cluster_xi, 0.22, 22)) + list(np.random.uniform(0.5, 3.8, 12))
        dots = VGroup(*[Dot(line.number_to_point(v), radius=0.045, color=BLUE, fill_opacity=0.8) for v in vals if 0.2 <= v <= 3.8])
        self.play(FadeIn(dots), run_time=0.8)

        # 斩下一刀：二分抽屉 (标签放置在数轴刻度数字正下方，绝不干扰上方聚点)
        cut_pt = line.number_to_point(2.0)
        cut_line = DashedLine(cut_pt + UP * 0.9, cut_pt + DOWN * 0.9, color=YELLOW, stroke_width=3)
        cut_lbl = self.zh("二分法：必有一半包含无穷多点！", font_size=24, color=YELLOW).next_to(line, DOWN, buff=0.7)
        self.play(Create(cut_line), FadeIn(cut_lbl))

        # 聚点
        pt_xi = Dot(line.number_to_point(cluster_xi), radius=0.12, color=GREEN)
        lbl_xi = self.mt(r"\exists x_{n_k} \to \xi", font_size=42, color=GREEN).next_to(pt_xi, UP, buff=0.25)
        self.play(Create(pt_xi), FadeIn(lbl_xi), Flash(line.number_to_point(cluster_xi), color=GREEN))

        # 上半区推导行
        row1 = VGroup(
            self.zh("定理表述：", font_size=32, color=BLUE),
            self.zh("有界无穷实数序列，必存在一个收敛的子序列 ", font_size=30, color=INK),
            self.mt(r"x_{n_k} \to \xi", font_size=38, color=GREEN)
        ).arrange(RIGHT, buff=0.1)

        row2 = VGroup(
            self.zh("核心思想（无限抽屉原理）：", font_size=30, color=YELLOW),
            self.zh("将区间一分为二，至少有一半含有无穷多个点！", font_size=28, color=YELLOW)
        ).arrange(RIGHT, buff=0.1)

        row3 = VGroup(
            self.zh("二分构造区间套：", font_size=30, color=GREEN),
            self.mt(r"[a_k, b_k] \to \xi \implies", font_size=38, color=GREEN),
            self.zh("挑出子列 ", font_size=28, color=GREEN),
            self.mt(r"x_{n_k} \to \xi \in \mathbb{R}", font_size=38, color=GREEN)
        ).arrange(RIGHT, buff=0.08)

        content = self.build_deduction_block(bar, [row1, row2, row3], top_buff=0.45, row_buff=0.35)

        for r in [row1, row2, row3]:
            self.play(FadeIn(r, shift=UP * 0.1), run_time=0.7)
        self.wait(3.0)
        self.clear_scene()


# =============================================================================
# 6. 定理五：有限覆盖定理 (Heine-Borel) 与证明
# =============================================================================
class Scene06_HeineBorel(BaseKaitiScene):
    def construct(self):
        bar = self.title_bar("定理五：有限覆盖定理 (Heine-Borel)")
        self.play(Write(bar), run_time=0.8)

        # 下方几何数轴：y = -2.0 (给上方光伞留足完全无冲突的垂直高度)
        line = NumberLine(x_range=[0, 4, 1], length=11.5, color=MUTED, include_numbers=True, font_size=32).shift(DOWN * 2.0)
        self.play(Create(line), run_time=0.9)

        seg = Line(line.number_to_point(1.0), line.number_to_point(3.0), color=BLUE, stroke_width=7)
        # 标签放置于数轴刻度数字正下方，buff=0.68，彻底避免与数字「2」重叠！
        seg_lbl = self.mt(r"[a, b] = [1.0, 3.0]", font_size=32, color=BLUE).next_to(line, DOWN, buff=0.68)
        self.play(Create(seg), FadeIn(seg_lbl))

        # 3 顶主覆盖光伞 (弧度平缓，不向上穿透到文字推导区)
        umbrellas_data = [
            (0.8, 1.8, YELLOW), (1.6, 2.5, GREEN), (2.3, 3.2, ORANGE)
        ]
        arcs = VGroup()
        for l, r, col in umbrellas_data:
            p1 = line.number_to_point(l)
            p2 = line.number_to_point(r)
            arc = ArcBetweenPoints(p1, p2, angle=-TAU / 7, stroke_width=4.5, color=col).shift(UP * 0.15)
            arcs.add(arc)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.15), run_time=1.2)

        # 上半区推导行
        row1 = VGroup(
            self.zh("定理表述（紧致性之魂）：", font_size=30, color=BLUE),
            self.zh("闭区间的任意开覆盖，必能选出有限个开区间覆盖它", font_size=28, color=INK)
        ).arrange(RIGHT, buff=0.1)

        row2 = VGroup(
            self.zh("有限子覆盖式：", font_size=30, color=GREEN),
            self.mt(r"[a, b] \subseteq U_{i_1} \cup U_{i_2} \cup \dots \cup U_{i_m}", font_size=40, color=GREEN)
        ).arrange(RIGHT, buff=0.1)

        row3 = VGroup(
            self.zh("反证法：", font_size=30, color=RED),
            self.zh("若不能有限覆盖，二分法收缩至单点 ", font_size=28, color=INK),
            self.mt(r"\xi \in U_0", font_size=34, color=YELLOW),
            self.zh("，在极小邻域仅需 1 个开集即可覆盖，矛盾！", font_size=28, color=RED)
        ).arrange(RIGHT, buff=0.08)

        content = self.build_deduction_block(bar, [row1, row2, row3], top_buff=0.45, row_buff=0.35)

        for r in [row1, row2, row3]:
            self.play(FadeIn(r, shift=UP * 0.1), run_time=0.7)
        self.wait(3.0)
        self.clear_scene()


# =============================================================================
# 7. 定理六：柯西审敛准则 (Cauchy Criterion) 与证明
# =============================================================================
class Scene07_CauchyCriterion(BaseKaitiScene):
    def construct(self):
        bar = self.title_bar("定理六：柯西审敛准则 (Cauchy Completeness)")
        self.play(Write(bar), run_time=0.8)

        # 下方几何数轴：y = -1.9
        line = NumberLine(x_range=[0, 4, 1], length=11.5, color=MUTED, include_numbers=True, font_size=32).shift(DOWN * 1.9)
        self.play(Create(line), run_time=0.9)

        # 弹性连杆拉近点列
        c_val = 2.4
        p1 = line.number_to_point(c_val - 0.5)
        p2 = line.number_to_point(c_val + 0.4)
        dot1 = Dot(p1, radius=0.07, color=BLUE)
        dot2 = Dot(p2, radius=0.07, color=BLUE)
        spring = Line(p1, p2, color=RED, stroke_width=4)
        spring_lbl = self.mt(r"|a_n - a_m| < \varepsilon", font_size=32, color=RED).next_to(spring, UP, buff=0.12)

        self.play(Create(dot1), Create(dot2), Create(spring), FadeIn(spring_lbl), run_time=1.0)

        limit_pt = line.number_to_point(c_val)
        limit_dot = Dot(limit_pt, radius=0.12, color=GREEN)
        limit_lbl = self.mt(r"\lim_{n \to \infty} a_n = L", font_size=42, color=GREEN).next_to(limit_dot, UP, buff=0.25)
        self.play(ReplacementTransform(VGroup(dot1, dot2, spring, spring_lbl), limit_dot), FadeIn(limit_lbl), Flash(limit_pt, color=GREEN), run_time=1.2)

        # 上半区推导行
        row1 = VGroup(
            self.zh("柯西收敛充要条件：", font_size=30, color=YELLOW),
            self.mt(r"\forall \varepsilon > 0, \quad \exists N, \quad \forall n, m > N : \quad |a_n - a_m| < \varepsilon", font_size=38, color=YELLOW)
        ).arrange(RIGHT, buff=0.1)

        row2 = VGroup(
            self.zh("证明第一步（有界致密）：", font_size=28, color=INK),
            self.zh("柯西列必有界 ", font_size=26, color=MUTED),
            self.mt(r"\implies", font_size=32, color=BLUE),
            self.zh(" 由致密性定理，必存在收敛子列 ", font_size=26, color=MUTED),
            self.mt(r"a_{n_k} \to L", font_size=34, color=GREEN)
        ).arrange(RIGHT, buff=0.08)

        row3 = VGroup(
            self.zh("证明第二步（三角不等式传递）：", font_size=28, color=GREEN),
            self.mt(r"|a_n - L| \le |a_n - a_{n_k}| + |a_{n_k} - L| < \varepsilon", font_size=36, color=GREEN)
        ).arrange(RIGHT, buff=0.1)

        content = self.build_deduction_block(bar, [row1, row2, row3], top_buff=0.45, row_buff=0.35)

        for r in [row1, row2, row3]:
            self.play(FadeIn(r, shift=UP * 0.1), run_time=0.7)
        self.wait(3.0)
        self.clear_scene()


# =============================================================================
# 8. 终章：3D 宏伟等价神殿 (3D Grand Equivalence)
# =============================================================================
class Scene08_GrandEquivalence3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)

        # 2D 顶层固定标题覆盖
        title_3d = Text("终章：实数完备性 3D 等价闭环星系", font=ZH_FONT, font_size=46, color=BLUE, weight=BOLD)
        title_3d.to_edge(UP, buff=0.45)
        sub_3d = Text("六大定理互为充要，在三维流光闭环中浑然一体，共同托起现代微积分大厦", font=ZH_FONT, font_size=28, color=MUTED)
        sub_3d.next_to(title_3d, DOWN, buff=0.12)

        # 底部闭环等价 HUD 指示器
        chain_badges = VGroup(
            Text("① 确界原理", font=ZH_FONT, font_size=22, color=YELLOW),
            MathTex(r"\iff", font_size=26, color=BLUE),
            Text("② 单调有界", font=ZH_FONT, font_size=22, color=YELLOW),
            MathTex(r"\iff", font_size=26, color=BLUE),
            Text("③ 区间套", font=ZH_FONT, font_size=22, color=YELLOW),
            MathTex(r"\iff", font_size=26, color=BLUE),
            Text("④ 致密性", font=ZH_FONT, font_size=22, color=YELLOW),
            MathTex(r"\iff", font_size=26, color=BLUE),
            Text("⑤ 有限覆盖", font=ZH_FONT, font_size=22, color=YELLOW),
            MathTex(r"\iff", font_size=26, color=BLUE),
            Text("⑥ 柯西准则", font=ZH_FONT, font_size=22, color=YELLOW),
        ).arrange(RIGHT, buff=0.12).to_edge(DOWN, buff=0.45)

        chain_bg = SurroundingRectangle(chain_badges, color=BLUE, stroke_width=1.5, fill_color="#101a28", fill_opacity=0.88, corner_radius=0.15)
        chain_group = VGroup(chain_bg, chain_badges)

        self.add_fixed_in_frame_mobjects(title_3d, sub_3d, chain_group)
        self.play(FadeIn(title_3d), FadeIn(sub_3d), FadeIn(chain_group), run_time=1.0)

        theorems = [
            ("确界原理", r"\sup S, \inf S"),
            ("单调有界", r"\lim a_n = L"),
            ("区间套定理", r"\bigcap I_n = \{\xi\}"),
            ("致密性定理", r"\exists a_{n_k} \to \xi"),
            ("有限覆盖", r"\bigcup_{i=1}^m U_i"),
            ("柯西准则", r"|a_n - a_m| < \varepsilon"),
        ]

        radius = 3.0
        pillars = VGroup()
        base_rings = VGroup()
        node_positions = []

        for i, (name, f_tex) in enumerate(theorems):
            angle = i * (2 * PI / 6)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            node_positions.append(np.array([x, y, 0]))

            cylinder = Cylinder(radius=0.35, height=1.6, direction=OUT, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to([x, y, 0.8])
            ring = Annulus(inner_radius=0.38, outer_radius=0.55, color=YELLOW).move_to([x, y, 0.02])

            pillars.add(cylinder)
            base_rings.add(ring)

        self.play(
            LaggedStart(*[FadeIn(r) for r in base_rings], lag_ratio=0.12),
            LaggedStart(*[FadeIn(p, shift=UP * 0.4) for p in pillars], lag_ratio=0.12),
            run_time=1.8
        )

        laser_lines = VGroup()
        for i in range(6):
            p1 = np.array([node_positions[i][0], node_positions[i][1], 1.6])
            p2 = np.array([node_positions[(i + 1) % 6][0], node_positions[(i + 1) % 6][1], 1.6])
            line3d = Line3D(p1, p2, color=GREEN, thickness=0.035)
            laser_lines.add(line3d)

        self.play(LaggedStart(*[Create(l) for l in laser_lines], lag_ratio=0.14), run_time=1.8)

        core_sphere = Sphere(radius=0.7, color=RED, fill_opacity=0.9).move_to([0, 0, 1.2])
        self.play(FadeIn(core_sphere, scale=0.5), run_time=1.2)
        self.wait(3.5)
