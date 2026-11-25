# 实数完备性大电影 (Manim 3B1B 楷体大字高奢版)

本项目是基于 Manim CE 制作的 3Blue1Brown 风格数学动画工程，主题为**《实数系的建立与实数完备性六大定理》**。
遵循 16:9 横屏大字版式标准（Kaiti SC 楷体、暗色主题、严禁图文重叠、三维空间拓展）。

---

## 📁 目录结构说明

```text
MANIM 3B1B/
├── 实数完备性全景大电影_楷体大字母带_1080P60.mp4   # 最终成品（1080P 60FPS 完整全景片）
├── 大字楷体分幕精选/                              # 10 个独立章节高清视频
│   ├── 00_历史篇_四大立法者肖像.mp4
│   ├── 01_实数创立_戴德金分割.mp4
│   ├── 02_定理一_确界原理与证明.mp4
│   ├── 03_定理二_单调有界定理与证明.mp4
│   ├── 04_定理三_一维区间套定理.mp4
│   ├── 05_定理三拓展_三维嵌套立方体.mp4
│   ├── 06_定理四_致密性定理与二分证明.mp4
│   ├── 07_定理五_有限覆盖定理与反证.mp4
│   ├── 08_定理六_柯西审敛准则与证明.mp4
│   └── 09_终章_3D等价闭环星系.mp4
├── real_number_kaiti_master.py                  # 核心源码（所有 10 幕的场景定义都在此文件中）
├── build_kaiti_master.py                        # 一键全自动渲染与拼接脚本
├── concat_kaiti_list.txt                        # FFmpeg 无损拼接清单
├── assets/
│   └── portraits/                               # 柯西、魏尔斯特拉斯、戴德金、康托尔历史肖像素材
├── media/                                       # 缓存与中间产物（保留后二次渲染可秒级命中缓存）
└── README.md                                    # 本项目工程说明文档
```

---

## 🛠️ 环境依赖

1. **Python 3.10+**
2. **Manim Community Edition** (推荐 v0.18+)
   ```bash
   pip install manim
   ```
3. **LaTeX** (MacTeX 或 TeXLive)
4. **FFmpeg** (用于最终视频无损缝合)
   ```bash
   brew install ffmpeg
   ```
5. **字体**：macOS 系统内置的 `Kaiti SC`（如在 Windows/Linux 上运行，可修改脚本开头的 `ZH_FONT = "KaiTi"` 或系统已安装的中文字体名）。

---

## 🚀 常用运行与改动命令

### 1. 快速预览某一幕 (480P 低清秒出)
如果你修改了某一个场景（例如单调有界定理）：
```bash
manim -pql real_number_kaiti_master.py Scene03_MonotoneConvergence
```

### 2. 高清单幕渲染 (1080P 60FPS)
```bash
manim -pqh real_number_kaiti_master.py Scene03_MonotoneConvergence
```

### 3. 一键批处理渲染全剧并拼接完整大电影
直接运行构建脚本，脚本会自动检测渲染差异（有缓存的秒过），并将 10 幕自动导出至 `大字楷体分幕精选/`，再缝合为最终母带：
```bash
python3 build_kaiti_master.py
```

---

## 💡 代码修改指南

所有场景均集中在 `real_number_kaiti_master.py` 中，按类名对应各幕：

| 类名 (`Class Name`) | 对应章节 | 核心看点 |
| :--- | :--- | :--- |
| `Scene00_History` | 历史篇 | 4 位立法者卡片肖像排版 |
| `Scene01_DedekindCut` | 戴德金分割 | 左右数轴切面与 $\sqrt{2} \in \mathbb{R}$ |
| `Scene02_SupremumPrinciple` | 定理一：确界原理 | 点集逼近、上确界阻挡线 $\sup S = \beta$ |
| `Scene03_MonotoneConvergence` | 定理二：单调有界 | 上界天花板 $M$ 与极限线 $L$（双标分离无重叠） |
| `Scene04_NestedIntervals` | 定理三：区间套 | 一维区间嵌套收缩 $[a_n, b_n]$ |
| `Scene04_NestedIntervals3D` | 定理三 3D 拓展 | 三维空间嵌套立方体收缩至中心奇异点 |
| `Scene05_BolzanoWeierstrass` | 定理四：致密性 | 无限抽屉原理二分法与聚点 $\xi$ |
| `Scene06_HeineBorel` | 定理五：有限覆盖 | 紧致性弧形开覆盖光伞与反证法 |
| `Scene07_CauchyCriterion` | 定理六：柯西准则 | 弹性连杆拉紧动效与三角不等式 |
| `Scene08_GrandEquivalence3D` | 终章：3D 等价神殿 | 六边形等价柱阵列、激光环绕、底部 HUD 徽章 |

### 排版与防重叠要点：
- 页面推导每页严格控制在 **3 行以内**。
- 每行使用 `self.build_deduction_block(bar, [row1, row2, row3])`，会自动通过 `self.fit(row, width=13.6)` 限制行宽，绝不会溢出屏幕两端。
- 下方数轴通常下移至 `y = -1.9`，与上方文字推导块保持 $> 1.5$ 单元的纯粹留白，彻底避免文字与几何图形重叠。
