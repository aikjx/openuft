# -*- coding: utf-8 -*-
"""One-off renumber: my G6 volume r339 -> r341 (lost the race; earlier writer keeps r339).

Evidence (mtime, 数据/判定/源码/HTML 四树 real files):
  other session  TUFT-r339_秩一超曲面整性...      source 20:36:54, full set 20:38:00, README reg 20:39:42
  mine           TUFT-r339_光速螺旋G6_EinsteinCartan... source 20:38:37, full set 20:40:05
=> I am the later writer. Repo discipline: first-to-land keeps the number, later writer yields.
r340 taken (source 20:39:13, another session). r341/r342 free at renumber time.
"""
import io
import os
import shutil

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DAT = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")

OLD = "TUFT-r339_光速螺旋G6_EinsteinCartan挠率源方程_代数slave与传播化代价与光子无源判据_2026-11-01"
NEW = "TUFT-r341_光速螺旋G6_EinsteinCartan挠率源方程_代数slave与传播化代价与光子无源判据_2026-11-01"

PAIRS = [
    (os.path.join(SRC, OLD + ".py"), os.path.join(SRC, NEW + ".py")),
    (os.path.join(DAT, OLD + ".json"), os.path.join(DAT, NEW + ".json")),
    (os.path.join(DAT, OLD + ".md"), os.path.join(DAT, NEW + ".md")),
    (os.path.join(DAT, OLD + "_report.txt"), os.path.join(DAT, NEW + "_report.txt")),
    (os.path.join(JUD, "判定_" + OLD + ".md"), os.path.join(JUD, "判定_" + NEW + ".md")),
]
PAIRS.append((os.path.join(ROOT, "四力统一方程_G6EC挠率源方程代价核算_r339可视化_2026-11-01.html"),
              os.path.join(ROOT, "四力统一方程_G6EC挠率源方程代价核算_r341可视化_2026-11-01.html")))

moved = skipped = 0
for old, new in PAIRS:
    if os.path.exists(old):
        if os.path.exists(new):
            print("[STOP] both exist: %s" % os.path.basename(new))
            raise SystemExit(4)
        shutil.move(old, new)
        moved += 1
        print("[MOVE] %s -> %s" % (os.path.basename(old), os.path.basename(new)))
    elif os.path.exists(new):
        skipped += 1
        print("[SKIP] already renamed: %s" % os.path.basename(new))
    else:
        print("[STOP] missing both: %s" % os.path.basename(old))
        raise SystemExit(4)
print("[step1] moved=%d skipped=%d" % (moved, skipped))

REPL = [("X-R339-", "X-R341-"), ("TUFT-r339", "TUFT-r341"),
        ("r339", "r341"), ("R339", "R341")]
total = 0
for _, new in PAIRS:
    with io.open(new, "r", encoding="utf-8", newline="") as f:
        txt = f.read()
    orig = txt
    for a, b in REPL:
        txt = txt.replace(a, b)
    if txt != orig:
        with io.open(new, "w", encoding="utf-8", newline="") as f:
            f.write(txt)
        n = sum(orig.count(a) for a, _ in REPL)
        total += n
        print("[REPL] %-72s %d hits" % (os.path.basename(new)[:72], n))
    else:
        print("[REPL] %-72s 0 hits (clean)" % os.path.basename(new)[:72])
print("[step2] total replacements=%d" % total)

resid = 0
for _, new in PAIRS:
    with io.open(new, "r", encoding="utf-8", newline="") as f:
        txt = f.read()
    bad = txt.count("r339") + txt.count("R339")
    if bad:
        resid += bad
        print("[RESID] %s still has %d" % (os.path.basename(new), bad))
print("[step3] residual=%d" % resid)

print("[check] r341 in 源码/ = %d, 数据/ = %d, 判定/ = %d"
      % (sum(1 for x in os.listdir(SRC) if "r341" in x),
         sum(1 for x in os.listdir(DAT) if "r341" in x),
         sum(1 for x in os.listdir(JUD) if "r341" in x)))
print("[check] other session r339 intact in 数据/ = %d, 判定/ = %d"
      % (sum(1 for x in os.listdir(DAT) if "r339" in x),
         sum(1 for x in os.listdir(JUD) if "r339" in x)))
print("RENUM-OK rc=0" if resid == 0 else "RENUM-FAIL rc=4")
raise SystemExit(0 if resid == 0 else 4)
