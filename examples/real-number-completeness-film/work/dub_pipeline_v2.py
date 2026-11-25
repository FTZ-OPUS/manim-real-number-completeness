#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manim/无声视频配音流水线 v2（基于 manim-video-dubbing 技能 dub_pipeline.py 增强）。

增强点：
1. TTS 网络重试（指数退避），中途断连不报废整批
2. 音频首尾静音裁剪（edge-tts 自带尾部静音，回收时长预算，语速更自然）
3. 文案哈希缓存：同文案命中缓存不重复请求 TTS，改稿只重配受影响段
4. 语速 +4% 起步、+4% 递进、上限 +24%；仍超长标记 LONG 并给出建议删字数
排程/合成/验收逻辑与技能原版一致。

用法:
    python dub_pipeline_v2.py config.json
"""
import asyncio, hashlib, json, os, subprocess, sys

CFG = json.load(open(sys.argv[1], encoding="utf-8"))
D = CFG["project_dir"].rstrip("/")
AUDIO = os.path.join(D, "work", "audio")
OUT_DIR = os.path.join(D, "out")
SRC = os.path.join(D, CFG["video"])
FINAL = os.path.join(OUT_DIR, CFG["out_name"])
FF, FP = "/opt/homebrew/bin/ffmpeg", "/opt/homebrew/bin/ffprobe"
VOICE = CFG.get("voice", "zh-CN-XiaoyiNeural")
LEAD, GAP = 0.3, 0.25
SECTIONS = CFG["sections"]
TOTAL = SECTIONS[-1]["end"]
RATE_MAX = 24


def dur_of(path):
    r = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())


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
    durs, paths = [], []
    for i, sec in enumerate(SECTIONS):
        target = (sec["end"] - sec["start"]) - 0.7
        # 按文案哈希缓存：段落平移/增删后，未改文案的段直接复用已有音频
        h = hashlib.md5((VOICE + "|" + sec["text"]).encode("utf-8")).hexdigest()[:10]
        path = os.path.join(AUDIO, "tts_%s.mp3" % h)
        if os.path.exists(path):
            d = dur_of(path)
            durs.append(d)
            paths.append(path)
            print("TTS %2d/%d %-28s 段%5.1fs 缓存命中 音%6.2fs"
                  % (i + 1, len(SECTIONS), sec["name"], sec["end"] - sec["start"], d),
                  flush=True)
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
        flag = "OK" if d <= target else "LONG"
        extra = "" if d <= target else "  建议删约%d字" % max(1, round((d - target) * 4.4))
        print("TTS %2d/%d %-28s 段%5.1fs 音%6.2fs +%d%% %s%s"
              % (i + 1, len(SECTIONS), sec["name"],
                 sec["end"] - sec["start"], d, rate, flag, extra),
              flush=True)
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
            raise SystemExit("音频重叠: %s vs %s" % (a[0]["name"], b[0]["name"]))
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
    cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", *inputs,
           "-i", SRC, "-filter_complex", fc,
           "-map", "%d:v" % len(sched), "-map", "[mix]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(TOTAL), FINAL]
    subprocess.run(cmd, check=True)

    od = dur_of(FINAL)
    sz = os.path.getsize(FINAL) / 1e6
    print("\n== 成片 ==\n  %s\n  时长 %.2fs (源 %.1fs)  大小 %.1fMB"
          % (FINAL, od, TOTAL, sz))
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
    print("  段落表: %s" % table)


async def run():
    durs, paths = await gen_all()
    main(durs, paths)

asyncio.run(run())
