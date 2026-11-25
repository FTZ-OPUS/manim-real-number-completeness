#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""楷体讲义电影 · 复检验收程序。

对母带/配音成片做自动化体检，输出 PASS/FAIL 报告；探针帧供人眼/视觉裁判最终确认音画对位。

用法:
    python verify_film.py --master 母带.mp4 [--dubbed 配音成片.mp4]
                          [--scenes-json build/scenes.json]     # 校验 母带时长 == Σ分幕
                          [--probes 5.5,11.2,143 --probe-dir out/probes]
                          [--samples 10]                        # 响度抽点数

检查项:
  1. 母带: 时长、无异常（文件可读、有视频流）
  2. 分幕(可选): Σ分幕时长 == 母带 ±0.5s
  3. 配音成片(可选): 时长 == 母带 ±0.5s；必须含音频流；
     等间隔响度抽点，说话区应 -20~-30dB，任一抽点 < -55dB 判死气段 FAIL
  4. 探针帧(可选): 按给定时间戳逐帧导出 PNG 到 --probe-dir，供人工/视觉裁判确认
退出码: 0 = 全部 PASS，1 = 存在 FAIL
"""
import argparse
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
    sys.exit("[verify] 未找到 %s。%s" % (name, install_hint))


def dur_of(path, fp):
    r = subprocess.run([fp, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def has_stream(path, ff, kind):
    # 注意：不能用 -loglevel error，否则输入流清单(info 级)被吞，永远返回 False
    r = subprocess.run([ff, "-hide_banner", "-i", path],
                       capture_output=True, text=True)
    return (": " + kind + ":") in r.stderr


def mean_volume_at(path, ff, t, dur=2.0):
    r = subprocess.run([ff, "-hide_banner", "-ss", str(t), "-t", str(dur), "-i", path,
                        "-map", "0:a", "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "mean_volume" in line:
            try:
                return float(line.split("mean_volume:")[1].strip().split(" ")[0])
            except ValueError:
                pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", required=True)
    ap.add_argument("--dubbed", default=None)
    ap.add_argument("--scenes-json", default=None)
    ap.add_argument("--probes", default="", help="逗号分隔的抽帧时间戳(秒)")
    ap.add_argument("--probe-dir", default="out/probes")
    ap.add_argument("--samples", type=int, default=10)
    args = ap.parse_args()

    ff = locate_bin("ffmpeg", "安装 ffmpeg 后重试")
    fp = locate_bin("ffprobe", "随 ffmpeg 一起安装")

    results = []

    def check(name, ok, detail=""):
        results.append((name, ok, detail))
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  " + detail) if detail else ""))

    print("== 1. 母带 ==")
    master = os.path.abspath(args.master)
    if not os.path.isfile(master):
        sys.exit("[verify] 母带不存在: %s" % master)
    m_dur = dur_of(master, fp)
    check("母带时长有效", m_dur > 0, "%.2fs" % m_dur)
    check("母带含视频流", has_stream(master, ff, "Video"))

    if args.scenes_json:
        import json
        cfg = json.load(open(args.scenes_json, encoding="utf-8"))
        proj = os.path.abspath(cfg.get("project_dir") or os.path.dirname(os.path.abspath(args.scenes_json)))
        out_dir = os.path.join(proj, cfg.get("output_dir", "out/episodes"))
        total, bad = 0.0, []
        for sc in cfg["scenes"]:
            e = os.path.join(out_dir, sc["output"])
            if not os.path.isfile(e):
                bad.append(sc["output"])
                continue
            total += dur_of(e, fp)
        if bad:
            check("分幕齐全", False, "缺失: " + ", ".join(bad))
        else:
            check("Σ分幕 == 母带", abs(total - m_dur) < 0.5,
                  "分幕和 %.2fs vs 母带 %.2fs" % (total, m_dur))

    if args.dubbed:
        print("== 2. 配音成片 ==")
        dubbed = os.path.abspath(args.dubbed)
        if not os.path.isfile(dubbed):
            sys.exit("[verify] 配音成片不存在: %s" % dubbed)
        d_dur = dur_of(dubbed, fp)
        check("成片时长 == 母带", abs(d_dur - m_dur) < 0.5,
              "%.2fs vs %.2fs" % (d_dur, m_dur))
        check("成片含音频流", has_stream(dubbed, ff, "Audio"))
        lows = []
        vols = []
        for i in range(args.samples):
            t = m_dur * (i + 0.5) / args.samples
            v = mean_volume_at(dubbed, ff, t)
            vols.append((round(t, 1), v))
            if v is not None and v < -55:
                lows.append((round(t, 1), v))
        lvl_txt = " ".join("%ss:%s" % (t, ("%.1fdB" % v) if v is not None else "??") for t, v in vols)
        print("    响度抽点: %s" % lvl_txt)
        check("无死气段(>=%ddB)" % -55, not lows,
              ("死气: " + ", ".join("%ss %.1fdB" % x for x in lows)) if lows else "全部 %d 点正常" % args.samples)

    if args.probes:
        print("== 3. 探针帧 ==")
        pdir = os.path.abspath(args.probe_dir)
        os.makedirs(pdir, exist_ok=True)
        made = []
        for t in [x.strip() for x in args.probes.split(",") if x.strip()]:
            out = os.path.join(pdir, "probe_t%s.png" % t.replace(".", "_"))
            subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y",
                            "-ss", t, "-i", args.dubbed or master, "-frames:v", "1", out],
                           check=True)
            made.append(out)
        check("探针帧导出", len(made) > 0, "%d 张 -> %s" % (len(made), pdir))
        for m in made:
            print("    " + m)
        print("    （请人工/视觉裁判逐帧确认：该时刻的画面与段落表文案是否对位）")

    print("\n== 复检结论 ==")
    fails = [r for r in results if not r[1]]
    for name, ok, detail in results:
        print("  %s %s" % ("✓" if ok else "✗", name))
    print("  合计 %d 项，FAIL %d 项 -> %s" % (len(results), len(fails), "不通过，回炉" if fails else "ALL PASS，可交付"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
