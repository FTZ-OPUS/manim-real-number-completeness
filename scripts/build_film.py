#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""楷体讲义电影 · 一键渲染与缝合（跨平台通用版）。

用法:
    python build_film.py build/scenes.json [选项]

scenes.json 结构（模板见 assets/templates/scenes.template.json）:
{
  "project_dir": "/abs/path/to/project",      // 可省略，默认取 json 所在目录的上层
  "output_dir":  "大字楷体分幕精选",           // 相对 project_dir
  "master_name": "母带.mp4",
  "scenes": [
    {"script": "ch01/ch01_scenes.py", "scene": "Ch01_Intro", "output": "010_第一章_开场.mp4"},
    ...
  ]
}

选项:
    --only 名字 [名字 ...]   只渲染指定场景（场景类名或输出文件名，子串匹配），随后仍会缝合
    --no-render             跳过渲染，只重新缝合（分幕须已存在）
    --no-concat             只渲染分幕，不缝合母带
    --quality qh|qm|ql      渲染档位，默认 qh(1080p60)；烟测用 ql(480p15)
    --output-dir DIR        临时覆盖输出目录（测试用）
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

FF_HINTS = ("/opt/homebrew/bin", "/usr/local/bin", "/usr/bin")


def locate_bin(name, install_hint):
    p = shutil.which(name)
    if p:
        return p
    for h in FF_HINTS:
        cand = os.path.join(h, name)
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    sys.exit("[build] 未找到 %s。%s" % (name, install_hint))


def locate_manim():
    p = shutil.which("manim")
    if p:
        return [p]
    # 常见情况：用了 venv 的 python 但没激活 —— manim 就在解释器同目录
    sibling = os.path.join(os.path.dirname(sys.executable), "manim")
    if os.path.isfile(sibling) and os.access(sibling, os.X_OK):
        return [sibling]
    try:
        import manim  # noqa: F401
        return [sys.executable, "-m", "manim"]
    except ImportError:
        sys.exit("[build] 未找到 manim。请先 `pip install manim`（或激活对应虚拟环境）。")


def dur_of(path, ffprobe):
    r = subprocess.run([ffprobe, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", help="scenes.json 路径")
    ap.add_argument("--only", nargs="+", default=None)
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--no-concat", action="store_true")
    ap.add_argument("--quality", default="qh", choices=["ql", "qm", "qh", "qp"])
    ap.add_argument("--output-dir", default=None)
    args = ap.parse_args()

    manifest_path = os.path.abspath(args.manifest)
    cfg = json.load(open(manifest_path, encoding="utf-8"))
    # project_dir 未指定时：先试 json 所在目录，若场景源码不在那里则取其上层
    # （约定 manifest 放 <项目>/build/scenes.json 或直接放项目根）
    default_dir = os.path.dirname(manifest_path)
    if cfg.get("project_dir"):
        project_dir = os.path.abspath(cfg["project_dir"])
    elif all(os.path.isfile(os.path.join(default_dir, sc["script"])) for sc in cfg["scenes"]):
        project_dir = default_dir
    else:
        project_dir = os.path.dirname(default_dir)
    output_dir = os.path.abspath(args.output_dir) if args.output_dir \
        else os.path.join(project_dir, cfg.get("output_dir", "out/episodes"))
    master_name = cfg.get("master_name", "master.mp4")
    scenes = cfg["scenes"]
    os.makedirs(output_dir, exist_ok=True)

    ff = locate_bin("ffmpeg", "安装: macOS `brew install ffmpeg` / Win `winget install ffmpeg` / Linux `apt install ffmpeg`")
    ffprobe = locate_bin("ffprobe", "随 ffmpeg 一起安装")
    manim_cmd = locate_manim()

    todo = []
    for sc in scenes:
        if args.only:
            hay = (sc["scene"] + " " + sc["output"]).lower()
            if not any(k.lower() in hay for k in args.only):
                continue
        todo.append(sc)
    if not todo:
        sys.exit("[build] --only 过滤后没有匹配场景")

    # ---------- 渲染 ----------
    rendered = []
    if not args.no_render:
        for i, sc in enumerate(todo, 1):
            script = os.path.join(project_dir, sc["script"])
            if not os.path.isfile(script):
                sys.exit("[build] 找不到源码: %s" % script)
            print("\n[%d/%d] 渲染 %s (%s) -> %s"
                  % (i, len(todo), sc["scene"], args.quality, sc["output"]), flush=True)
            cmd = manim_cmd + ["-" + args.quality, script, sc["scene"]]
            res = subprocess.run(cmd, cwd=project_dir)
            if res.returncode != 0:
                sys.exit("[build] 渲染失败: %s" % sc["scene"])

            stem = os.path.splitext(os.path.basename(script))[0]
            pattern = os.path.join(project_dir, "media", "videos", stem, "*", sc["scene"] + ".mp4")
            hits = sorted(glob.glob(pattern), key=os.path.getmtime)
            if not hits:
                sys.exit("[build] 未找到渲染产物: %s" % pattern)
            src = hits[-1]
            dst = os.path.join(output_dir, sc["output"])
            shutil.copy2(src, dst)
            rendered.append(dst)
            print("  ✓ 导出 %s (%.1fs)" % (dst, dur_of(dst, ffprobe)), flush=True)

    # ---------- 缝合 ----------
    if args.no_concat:
        print("\n[build] 按要求跳过缝合。")
        return

    episodes = [os.path.join(output_dir, sc["output"]) for sc in scenes]
    missing = [e for e in episodes if not os.path.isfile(e)]
    if missing:
        sys.exit("[build] 缺少分幕无法缝合（先渲染或检查 scenes.json）:\n  " + "\n  ".join(missing))

    concat_list = os.path.join(project_dir, "work", "concat_list.txt")
    os.makedirs(os.path.dirname(concat_list), exist_ok=True)
    with open(concat_list, "w", encoding="utf-8") as f:
        for e in episodes:
            f.write("file '%s'\n" % e)

    master = os.path.join(output_dir, master_name)
    subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "concat", "-safe", "0", "-i", concat_list,
                    "-c", "copy", master], check=True)

    total = dur_of(master, ffprobe)
    expect = sum(dur_of(e, ffprobe) for e in episodes)
    ok = abs(total - expect) < 0.5
    print("\n== 缝合完成 ==")
    print("  母带: %s" % master)
    print("  时长 %.2fs（分幕之和 %.2fs）  校验: %s" % (total, expect, "PASS" if ok else "FAIL"))
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
