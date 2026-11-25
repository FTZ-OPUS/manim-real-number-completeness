import os
import subprocess
import sys

import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 智能识别 Manim 运行环境（优先当前虚拟环境，其次环境变量 PATH）
VENV_MANIM = os.path.expanduser("~/venvs/manim/bin/manim")
if os.path.exists(VENV_MANIM):
    MANIM_BIN = VENV_MANIM
else:
    MANIM_BIN = shutil.which("manim") or "manim"

# 智能识别 FFmpeg 路径
HOMEBREW_FFMPEG = "/opt/homebrew/bin/ffmpeg"
if os.path.exists(HOMEBREW_FFMPEG):
    FFMPEG_BIN = HOMEBREW_FFMPEG
elif os.path.exists("/opt/homebrew/Cellar/ffmpeg/9.0.1_1/bin/ffmpeg"):
    FFMPEG_BIN = "/opt/homebrew/Cellar/ffmpeg/9.0.1_1/bin/ffmpeg"
else:
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"
OUTPUT_DIR = os.path.join(BASE_DIR, "大字楷体分幕精选")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# (源码文件, 场景类名, 输出分幕文件名) —— 按母带播放顺序排列
SCENES = [
    ("real_number_cold_open_3d.py", "Scene00_ColdOpen3D", "00_片头_六柱环核3D.mp4"),
    ("real_number_history_expanded.py", "Scene00_HistoryExpanded", "00_历史篇_四大立法者肖像.mp4"),
    ("real_number_kaiti_master.py", "Scene01_DedekindCut", "01_实数创立_戴德金分割.mp4"),
    ("real_number_kaiti_master.py", "Scene02_SupremumPrinciple", "02_定理一_确界原理与证明.mp4"),
    ("real_number_kaiti_master.py", "Scene03_MonotoneConvergence", "03_定理二_单调有界定理与证明.mp4"),
    ("real_number_kaiti_master.py", "Scene04_NestedIntervals", "04_定理三_一维区间套定理.mp4"),
    ("real_number_kaiti_master.py", "Scene04_NestedIntervals3D", "05_定理三拓展_三维嵌套立方体.mp4"),
    ("real_number_kaiti_master.py", "Scene05_BolzanoWeierstrass", "06_定理四_致密性定理与二分证明.mp4"),
    ("real_number_kaiti_master.py", "Scene06_HeineBorel", "07_定理五_有限覆盖定理与反证.mp4"),
    ("real_number_kaiti_master.py", "Scene07_CauchyCriterion", "08_定理六_柯西审敛准则与证明.mp4"),
    ("real_number_kaiti_master.py", "Scene08_GrandEquivalence3D", "09_终章_3D等价闭环星系.mp4"),
]

rendered_files = []

for script_file, scene_name, output_name in SCENES:
    print(f"\n==========================================")
    print(f"  正在以 1080P 60FPS 渲染: {scene_name} -> {output_name}")
    print(f"==========================================")
    cmd = [MANIM_BIN, "-qh", script_file, scene_name]
    res = subprocess.run(cmd, cwd=BASE_DIR)
    if res.returncode != 0:
        print(f"Error rendering {scene_name}!")
        sys.exit(1)

    script_stem = os.path.splitext(script_file)[0]
    src_mp4 = os.path.join(BASE_DIR, "media", "videos", script_stem, "1080p60", f"{scene_name}.mp4")
    dst_mp4 = os.path.join(OUTPUT_DIR, output_name)
    if os.path.exists(src_mp4):
        subprocess.run(["cp", src_mp4, dst_mp4])
        rendered_files.append(dst_mp4)
        print(f"✓ 成功导出分幕: {dst_mp4}")
    else:
        print(f"Warning: Expected output not found at {src_mp4}")

# 使用 ffmpeg 无损拼接为完整母带大电影
print("\n正在缝合拼接分幕为《实数完备性全景大电影_楷体大字母带_1080P60.mp4》...")
concat_list_file = os.path.join(BASE_DIR, "concat_kaiti_list.txt")
with open(concat_list_file, "w", encoding="utf-8") as f:
    for rf in rendered_files:
        f.write(f"file '{rf}'\n")

final_master = os.path.join(BASE_DIR, "实数完备性全景大电影_楷体大字母带_1080P60.mp4")
concat_cmd = [
    FFMPEG_BIN, "-f", "concat", "-safe", "0", "-i", concat_list_file,
    "-c", "copy", final_master, "-y"
]
subprocess.run(concat_cmd)
print(f"\n🎉 恭喜！楷体大字版全篇大电影已成功生成: {final_master}")
