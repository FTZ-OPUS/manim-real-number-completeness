#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""楷体讲义电影 · 配音管线（跨平台通用版）。

音画同步原理与方法论见 references/timeline-dubbing.md。

用法:
    python dub_pipeline.py work/dub_config.json

config.json:
{
  "project_dir": "/abs/path/to/project",        // 可省略，默认取 config 上层
  "video": "母带.mp4",                           // 相对 project_dir，须无声或允许覆盖音轨
  "out_name": "成片_配音版.mp4",                  // 输出到 project_dir/out/
  "voice": "zh-CN-XiaoyiNeural",
  "sections": [ {"name":"...","start":0.0,"end":5.8,"text":"文案"}, ... ]
}

能力:
  1. 分段 TTS：edge-tts，语速 +4% 起步、+4% 递进、上限 +24%；网络断连自动重试 5 次（指数退避）
  2. 音频首尾静音裁剪（回收 TTS 尾部静音的时长预算）
  3. 文案哈希缓存：音频按 md5(voice|text) 存 work/audio/tts_<hash>.mp3，改稿只重配受影响段
     ★ 自备录音替换法：把自己的录音改名为对应哈希文件放回 work/audio/，重跑即被采用
     ★ work/audio/manifest.json 记录 段名->文件 映射
  4. 级联排程：每段于 段首+0.3s 起，前段结束+0.25s 防重叠；出现顺延 = 文案超长，先改文案
  5. ffmpeg adelay/amix 混流（视频流 -c copy 直拷）+ 时长/响度验收 + out/段落表.txt
"""
import asyncio
import hashlib
import json
import os
import shutil
import subprocess
import sys

FF_HINTS = ("/opt/homebrew/bin", "/usr/local/bin", "/usr/bin")
LEAD, GAP = 0.3, 0.25
RATE_MAX = 24


def locate_bin(name, install_hint):
    p = shutil.which(name)
    if p:
        return p
    for h in FF_HINTS:
        cand = os.path.join(h, name)
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    sys.exit("[dub] 未找到 %s。%s" % (name, install_hint))


FF = None
FP = None
CFG = None
D = AUDIO = OUT_DIR = SRC = FINAL = None
VOICE = "zh-CN-XiaoyiNeural"
SECTIONS = []
TOTAL = 0.0


def setup(config_path):
    global CFG, D, AUDIO, OUT_DIR, SRC, FINAL, VOICE, SECTIONS, TOTAL, FF, FP
    CFG = json.load(open(config_path, encoding="utf-8"))
    # project_dir 未指定时：config 所在目录（或其上层，约定 config 放 <项目>/work/ 下）二选一，
    # 以「源视频实际存在」为准
    here = os.path.dirname(os.path.abspath(config_path))
    if CFG.get("project_dir"):
        D = os.path.abspath(CFG["project_dir"])
    elif os.path.isfile(os.path.join(here, CFG["video"])):
        D = here
    else:
        D = os.path.dirname(here)
    AUDIO = os.path.join(D, "work", "audio")
    OUT_DIR = os.path.join(D, "out")
    SRC = os.path.join(D, CFG["video"])
    FINAL = os.path.join(OUT_DIR, CFG["out_name"])
    VOICE = CFG.get("voice", VOICE)
    SECTIONS = CFG["sections"]
    TOTAL = SECTIONS[-1]["end"]
    if not os.path.isfile(SRC):
        sys.exit("[dub] 源视频不存在: %s" % SRC)


def dur_of(path):
    r = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def trim_silence(path):
    tmp = path + ".trim.mp3"
    r = subprocess.run(
        [FF, "-hide_banner", "-loglevel", "error", "-y", "-i", path, "-af",
         "silenceremove=start_periods=1:start_threshold=-45dB,"
         "areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
         "-c:a", "libmp3lame", "-q:a", "2", tmp],
        capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(tmp) and dur_of(tmp) > 0.2:
        os.replace(tmp, path)


async def tts_with_retry(text, rate, path):
    import edge_tts
    delay = 2
    for attempt in range(5):
        try:
            c = edge_tts.Communicate(text, VOICE, rate=rate)
            await c.save(path)
            return
        except Exception as e:
            if attempt == 4:
                raise
            print("  .. 网络异常重试 %d/4 (%s)" % (attempt + 1, type(e).__name__), flush=True)
            await asyncio.sleep(delay)
            delay *= 2


async def gen_all():
    os.makedirs(AUDIO, exist_ok=True)
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        sys.exit("[dub] 缺少 edge-tts：`pip install edge-tts`（自备录音也建议安装，便于校验时长）")
    durs, paths, manifest = [], [], {}
    for i, sec in enumerate(SECTIONS):
        target = (sec["end"] - sec["start"]) - 0.7
        h = hashlib.md5((VOICE + "|" + sec["text"]).encode("utf-8")).hexdigest()[:10]
        path = os.path.join(AUDIO, "tts_%s.mp3" % h)
        if os.path.exists(path):
            d = dur_of(path)
            durs.append(d)
            paths.append(path)
            manifest[sec["name"]] = {"file": os.path.basename(path), "dur": round(d, 2)}
            print("TTS %2d/%d %-28s 段%5.1fs 缓存命中 音%6.2fs"
                  % (i + 1, len(SECTIONS), sec["name"], sec["end"] - sec["start"], d), flush=True)
            continue
        rate = 4
        for _ in range(6):
            await tts_with_retry(sec["text"], "+%d%%" % rate, path)
            trim_silence(path)
            d = dur_of(path)
            if d <= target or rate >= RATE_MAX:
                break
            rate += 4
        durs.append(d)
        paths.append(path)
        manifest[sec["name"]] = {"file": os.path.basename(path), "dur": round(d, 2), "rate": rate}
        flag = "OK" if d <= target else "LONG"
        extra = "" if d <= target else "  建议删约%d字" % max(1, round((d - target) * 4.6))
        print("TTS %2d/%d %-28s 段%5.1fs 音%6.2fs +%d%% %s%s"
              % (i + 1, len(SECTIONS), sec["name"], sec["end"] - sec["start"], d, rate, flag, extra),
              flush=True)
    with open(os.path.join(AUDIO, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return durs, paths


def main(durs, paths):
    sched, prev_end = [], -9.0
    for i, sec in enumerate(SECTIONS):
        start = max(sec["start"] + LEAD, prev_end + GAP)
        sched.append((sec, start, durs[i]))
        prev_end = start + durs[i]
    print("\n== 排程 ==")
    for sec, st, d in sched:
        print("  %-28s 画面%6.1f-%6.1f  音%7.2f-%7.2f"
              % (sec["name"], sec["start"], sec["end"], st, st + d))
    for a, b in zip(sched, sched[1:]):
        if b[1] < a[1] + a[2] - 1e-6:
            raise SystemExit("音频重叠: %s vs %s（先改超长文案）" % (a[0]["name"], b[0]["name"]))
    last = sched[-1]
    if last[1] + last[2] > TOTAL:
        print("警告: 尾部超出 %.2fs" % (last[1] + last[2] - TOTAL))

    inputs, chains, labels = [], [], ""
    for i, (sec, st, d) in enumerate(sched):
        inputs += ["-i", paths[i]]
        ms = int(round(st * 1000))
        chains.append("[%d:a]aformat=sample_rates=44100:channel_layouts=stereo,"
                      "adelay=%d|%d[a%d]" % (i, ms, ms, i))
        labels += "[a%d]" % i
    fc = ";".join(chains) + ";%samix=inputs=%d:normalize=0[mix]" % (labels, len(sched))
    os.makedirs(OUT_DIR, exist_ok=True)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *inputs,
                    "-i", SRC, "-filter_complex", fc,
                    "-map", "%d:v" % len(sched), "-map", "[mix]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(TOTAL), FINAL],
                   check=True)

    od = dur_of(FINAL)
    print("\n== 成片 ==\n  %s\n  时长 %.2fs (源 %.1fs)  大小 %.1fMB"
          % (FINAL, od, TOTAL, os.path.getsize(FINAL) / 1e6))
    print("  时长校验: %s" % ("PASS" if abs(od - TOTAL) < 0.5 else "FAIL"))
    step = max(1, int(TOTAL) // 8)
    for t in range(3, int(TOTAL) - 2, step):
        r = subprocess.run([FF, "-hide_banner", "-ss", str(t), "-t", "2", "-i", FINAL,
                            "-map", "0:a", "-af", "volumedetect", "-f", "null", "-"],
                           capture_output=True, text=True)
        line = [l for l in r.stderr.splitlines() if "mean_volume" in l]
        v = line[0].split("mean_volume:")[1].strip() if line else "??"
        print("  t=%3ds 音轨 %s" % (t, v))

    table = os.path.join(OUT_DIR, "段落表.txt")
    with open(table, "w", encoding="utf-8") as f:
        f.write("段名\t画面起\t画面止\t音频起\t音频止\t文案\n")
        for sec, st, d in sched:
            f.write("%s\t%.1f\t%.1f\t%.2f\t%.2f\t%s\n"
                    % (sec["name"], sec["start"], sec["end"], st, st + d, sec["text"]))
    print("  段落表: %s\n  音频清单: %s" % (table, os.path.join(AUDIO, "manifest.json")))


def run():
    global FF, FP
    config_path = sys.argv[1] if len(sys.argv) > 1 else "work/dub_config.json"
    FF = locate_bin("ffmpeg", "安装: macOS `brew install ffmpeg` / Win `winget install ffmpeg` / Linux `apt install ffmpeg`")
    FP = locate_bin("ffprobe", "随 ffmpeg 一起安装")
    setup(config_path)
    durs, paths = asyncio.run(gen_all())
    main(durs, paths)


if __name__ == "__main__":
    run()
