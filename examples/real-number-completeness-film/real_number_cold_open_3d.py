"""
=============================================================================
  项目：实数完备性大电影 —— 3D 片头神殿（Cold Open）
  设计：参考终章 3D 等价闭环，全面彩色化升级——
        · 六根彩色双层发光圆柱 = 六大实数完备性定理（彩虹六色，基准环同色）
        · 六段彩色激光首尾相连成闭环（每段取起点支柱之色）
        · 中心金色球体 + 光晕 = 实数系的建立
        · 相机环境旋转 + 支柱阵列同步绕核旋转，开场即抓住眼球
  渲染：manim -qh real_number_cold_open_3d.py Scene00_ColdOpen3D
=============================================================================
"""

from manim import *
import numpy as np
import os

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0

ZH_FONT = "Kaiti SC"
MUTED  = "#A9B4C2"
BLUE   = "#5DADEC"
GREEN  = "#66D19E"
YELLOW = "#FFD166"
ORANGE = "#F59E62"
RED    = "#FF6B6B"
VIOLET = "#B79CFF"
GOLD   = "#F0A500"

config.background_color = "#0F1720"


def shaded_pair(col):
    """Surface 系专用：同色系深浅两色棋盘，既保立体感又显彩色。"""
    c = ManimColor(col)
    return [interpolate_color(c, ManimColor("#FFFFFF"), 0.22),
            interpolate_color(c, ManimColor("#000000"), 0.30)]


class Scene00_ColdOpen3D(ThreeDScene):
    """
    片头 3D：六柱环核 · 实数完备性神殿（总时长 10.0s，逐段显式 run_time）
    """
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.16)

        # ---------- 固定于画面的标题与图例 HUD ----------
        title_3d = Text("实数完备性", font=ZH_FONT, font_size=56, color=BLUE, weight=BOLD)
        title_3d.to_edge(UP, buff=0.4)
        sub_3d = Text("六大等价定理支柱，环绕实数系核心", font=ZH_FONT, font_size=26, color=MUTED)
        sub_3d.next_to(title_3d, DOWN, buff=0.12)

        legend_data = [
            ("① 确界原理", BLUE), ("② 单调有界", GREEN), ("③ 区间套", YELLOW),
            ("④ 致密性", ORANGE), ("⑤ 有限覆盖", RED), ("⑥ 柯西准则", VIOLET),
        ]
        row = VGroup()
        for i, (t, c) in enumerate(legend_data):
            row.add(Text(t, font=ZH_FONT, font_size=22, color=c))
            if i < 5:
                row.add(MathTex(r"\iff", font_size=24, color=BLUE))
        row.arrange(RIGHT, buff=0.12).to_edge(DOWN, buff=0.45)
        hud_bg = SurroundingRectangle(row, color=BLUE, stroke_width=1.5,
                                      fill_color="#101a28", fill_opacity=0.88, corner_radius=0.15)
        hud = VGroup(hud_bg, row)

        self.add_fixed_in_frame_mobjects(title_3d, sub_3d, hud)
        self.play(FadeIn(title_3d), FadeIn(sub_3d), FadeIn(hud), run_time=1.0)

        # ---------- 六根彩色双层发光圆柱 + 同色基准环 ----------
        cols = [BLUE, GREEN, YELLOW, ORANGE, RED, VIOLET]
        radius = 3.0
        rings = VGroup()
        pillars = VGroup()
        tops = []
        for i, col in enumerate(cols):
            ang = i * TAU / 6
            x, y = radius * np.cos(ang), radius * np.sin(ang)
            tops.append(np.array([x, y, 1.7]))

            outer = Cylinder(radius=0.42, height=1.7, direction=OUT,
                             fill_color=col, fill_opacity=0.25,
                             checkerboard_colors=False,
                             stroke_width=0).move_to([x, y, 0.85])
            inner = Cylinder(radius=0.27, height=1.7, direction=OUT,
                             fill_color=col, fill_opacity=0.92,
                             checkerboard_colors=shaded_pair(col),
                             stroke_width=0).move_to([x, y, 0.85])
            ring = Annulus(inner_radius=0.45, outer_radius=0.62, color=col,
                           fill_opacity=0.95, stroke_width=0).move_to([x, y, 0.02])

            pillars.add(VGroup(outer, inner))
            rings.add(ring)

        self.play(
            LaggedStart(*[FadeIn(r) for r in rings], lag_ratio=0.1),
            LaggedStart(*[FadeIn(p, shift=UP * 0.5) for p in pillars], lag_ratio=0.1),
            run_time=2.2,
        )

        # ---------- 六段彩色激光闭环（每段取起点支柱之色） ----------
        laser_lines = VGroup()
        for i in range(6):
            laser_lines.add(
                Line3D(tops[i], tops[(i + 1) % 6], color=cols[i], thickness=0.03)
            )
        self.play(LaggedStart(*[Create(l) for l in laser_lines], lag_ratio=0.14), run_time=1.6)

        # ---------- 金色实数核诞生（球体 + 光晕） ----------
        core = Sphere(radius=0.7, fill_color=GOLD, fill_opacity=0.95,
                      checkerboard_colors=shaded_pair(GOLD),
                      stroke_width=0).move_to([0, 0, 1.15])
        halo = Sphere(radius=1.02, fill_color=GOLD, fill_opacity=0.12,
                      checkerboard_colors=False,
                      stroke_width=0).move_to([0, 0, 1.15])
        self.play(GrowFromCenter(core), FadeIn(halo), run_time=1.2)

        # ---------- 支柱阵列绕核旋转展示（叠加相机环境旋转） ----------
        assembly = VGroup(rings, pillars, laser_lines)
        self.play(Rotate(assembly, angle=TAU / 12), run_time=3.2)

        # ---------- 淡出收场，为历史篇让位 ----------
        self.stop_ambient_camera_rotation()
        self.play(
            *[FadeOut(m) for m in [title_3d, sub_3d, hud, assembly, core, halo]],
            run_time=0.8,
        )
