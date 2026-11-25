"""
=============================================================================
  项目：实数完备性大电影 —— 历史篇【扩充版】(独立文件，不覆盖任何已验收资产)
  说明：前两幕（地基危机片头 + 四人画卷）与已验收版 real_number_kaiti_master.py
        的 Scene00_History 逐帧一致；在其后新增柯西 / 魏尔斯特拉斯 /
        戴德金 / 康托尔 四段个人展开推演小镜头，并以"四块基石"收束。
  渲染：manim -qh real_number_history_expanded.py Scene00_HistoryExpanded
=============================================================================
"""

from manim import *
import numpy as np
import os

# -------------------------------------------------------------
# 全局配置（与楷体大字规范一致：16:9 横屏，Kaiti SC，深暗底色）
# -------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0

ZH_FONT = "Kaiti SC"
BG     = "#0F1720"
INK    = "#F6F2EA"
MUTED  = "#A9B4C2"
BLUE   = "#5DADEC"
GREEN  = "#66D19E"
YELLOW = "#FFD166"
ORANGE = "#F59E62"
RED    = "#FF6B6B"
VIOLET = "#B79CFF"

config.background_color = BG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTRAITS_DIR = os.path.join(BASE_DIR, "assets", "portraits")


# -------------------------------------------------------------
# 基础公共类（与 real_number_kaiti_master.py 完全一致，自包含）
# -------------------------------------------------------------
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
# 历史篇扩充版：片头 + 四人画卷 + 四段个人展开镜头 + 收束
# =============================================================================
class Scene00_HistoryExpanded(BaseKaitiScene):
    def construct(self):
        # ---------- 第一幕：微积分的地基危机（与已验收版本一致） ----------
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

        # ---------- 第二幕：实数论的四位立法者画卷（与已验收版本一致） ----------
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

        # ---------- 第三幕：四位立法者个人展开推演镜头 ----------
        self.portrait_story(
            "cauchy.jpg", "柯西 (A. Cauchy)", "1821《分析教程》· 首位立法者", BLUE,
            "柯西：给极限上紧发条",
            [
                VGroup(
                    self.zh("极限的算术化：", font_size=28, color=BLUE),
                    self.mt(r"\lim_{n \to \infty} a_n = L", font_size=40, color=INK),
                ).arrange(RIGHT, buff=0.12),
                VGroup(
                    self.zh("柯西收敛准则：", font_size=28, color=BLUE),
                    self.mt(r"|a_n - a_m| < \varepsilon \iff a_n \to L", font_size=38, color=INK),
                ).arrange(RIGHT, buff=0.12),
                self.zh("连续、导数、积分，从此全部踏上不等式的轨道。", font_size=26, color=MUTED),
            ],
        )

        self.portrait_story(
            "weierstrass.jpg", "魏尔斯特拉斯 (K. Weierstrass)", "现代分析之父 · 确界与致密", YELLOW,
            "魏尔斯特拉斯：颁布 ε-δ 宪法",
            [
                VGroup(
                    self.zh("ε-δ 语言：", font_size=28, color=YELLOW),
                    self.mt(r"0 < |x - a| < \delta \implies |f(x) - L| < \varepsilon", font_size=36, color=INK),
                ).arrange(RIGHT, buff=0.12),
                VGroup(
                    self.zh("致密性定理：", font_size=28, color=YELLOW),
                    self.mt(r"\exists x_{n_k} \to \xi", font_size=40, color=INK),
                ).arrange(RIGHT, buff=0.12),
                self.zh("“无限接近”从此变成可检验的不等式。", font_size=26, color=MUTED),
            ],
        )

        self.portrait_story(
            "dedekind.jpg", "戴德金 (R. Dedekind)", "1872《连续性与无理数》", RED,
            "戴德金：一刀切出实数系",
            [
                VGroup(
                    self.zh("分割公理：", font_size=28, color=RED),
                    self.mt(r"(A \mid B) \longleftrightarrow \alpha \in \mathbb{R}", font_size=38, color=INK),
                ).arrange(RIGHT, buff=0.12),
                VGroup(
                    self.zh("有理数的裂缝由此补全：", font_size=28, color=RED),
                    self.mt(r"\sqrt{2} \in \mathbb{R}", font_size=40, color=INK),
                ).arrange(RIGHT, buff=0.12),
                self.zh("左右两集之间无最大亦无最小，分割点即实数。", font_size=26, color=MUTED),
            ],
        )

        self.portrait_story(
            "cantor.jpg", "康托尔 (G. Cantor)", "1872 基本列等价 · 区间套", GREEN,
            "康托尔：编织区间之网",
            [
                VGroup(
                    self.zh("基本列：", font_size=28, color=GREEN),
                    self.mt(r"|a_n - a_m| < \varepsilon \quad (n, m > N)", font_size=38, color=INK),
                ).arrange(RIGHT, buff=0.12),
                VGroup(
                    self.zh("区间套锁定：", font_size=28, color=GREEN),
                    self.mt(r"\bigcap_{n=1}^{\infty} [a_n, b_n] = \{\xi\}", font_size=40, color=INK),
                ).arrange(RIGHT, buff=0.12),
                self.zh("越收越紧的区间之网，网底就是唯一的实数点。", font_size=26, color=MUTED),
            ],
        )

        # ---------- 第四幕：收束（四块基石，一座大厦） ----------
        bar_c = self.title_bar("四块基石，一座大厦", color=VIOLET)
        self.play(Write(bar_c), run_time=0.8)

        row1 = self.zh("柯西立极限，魏尔斯特拉斯立 ε-δ，戴德金造实数，康托尔编区间之网。", font_size=32, color=INK)
        row2 = self.zh("实数完备性六大等价定理，全部站在这块坚实地基之上！", font_size=32, color=GREEN)
        content = self.build_deduction_block(bar_c, [row1, row2], top_buff=0.7, row_buff=0.55)
        self.play(FadeIn(row1, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(row2, shift=UP * 0.15), run_time=0.7)

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
        ).arrange(RIGHT, buff=0.12).next_to(content, DOWN, buff=0.8)

        chain_bg = SurroundingRectangle(chain_badges, color=BLUE, stroke_width=1.5,
                                        fill_color="#101a28", fill_opacity=0.88, corner_radius=0.15)
        self.play(FadeIn(chain_bg), FadeIn(chain_badges), run_time=0.8)
        self.wait(3.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 个人展开镜头：左侧肖像相框（ImageMobject 一律用 Group 承载），
    # 右侧独立推导行，互不重叠，收尾统一 clear_scene
    # ------------------------------------------------------------------
    def portrait_story(self, img_name, name, desc, accent, head, rows, hold=2.8):
        bar = self.title_bar(head, color=accent)
        self.play(Write(bar), run_time=0.8)

        img = ImageMobject(os.path.join(PORTRAITS_DIR, img_name))
        img.scale_to_fit_height(2.7)
        if img.width > 3.0:
            img.scale_to_fit_width(3.0)

        frame_box = RoundedRectangle(
            corner_radius=0.15,
            width=img.width + 0.25,
            height=img.height + 0.25,
            stroke_color=accent,
            stroke_width=2.5,
            fill_color="#182230",
            fill_opacity=0.9,
        )
        img.move_to(frame_box.get_center())
        t_name = self.zh(name, font_size=24, color=INK, weight=BOLD).next_to(frame_box, DOWN, buff=0.15)
        t_desc = self.zh(desc, font_size=18, color=MUTED).next_to(t_name, DOWN, buff=0.1)

        card = Group(frame_box, img, t_name, t_desc)
        card.next_to(bar, DOWN, buff=0.55)
        card.to_edge(LEFT, buff=0.9)
        self.play(FadeIn(card, shift=RIGHT * 0.2), run_time=0.9)

        fitted = [self.fit(r, width=10.4) for r in rows]
        block = VGroup(*fitted).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        block.next_to(card, RIGHT, buff=0.6)
        # 垂直对准相框视觉中心（相框在卡片上部，向上抬 0.4），保证不顶标题栏
        block.move_to([block.get_center()[0], card.get_center()[1] + 0.4, 0])

        for r in fitted:
            self.play(FadeIn(r, shift=UP * 0.1), run_time=0.7)
        self.wait(hold)
        self.clear_scene()
