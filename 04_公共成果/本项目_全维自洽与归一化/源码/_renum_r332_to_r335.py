# -*- coding: utf-8 -*-
"""One-off renumber: r332 -> r335 (my volume lost the race; earlier writer keeps r332).

Rationale (repo discipline): first-to-land keeps the number; later writer must yield.
Evidence: other session's TUFT-r332_nullFrenet... source 19:40:37, four-piece set complete
19:40:47. Mine: source 19:43:49, set complete 19:43:59. I am the later writer.

r333: only a scattered 来料原件 (14:07), no volume -> left alone (hot).
r334 / r336: neighbours already fully closed by parallel chains -> r335 is a cold gap.
"""
import io
import os
import shutil

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DAT = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")

OLD_STEM = "TUFT-r332_整性给格只是单通量现象_秩二Fano上的反例族与delPezzo复核_精算与可视化_2026-11-01"
NEW_STEM = "TUFT-r335_整性给格只是单通量现象_秩二Fano上的反例族与delPezzo复核_精算与可视化_2026-11-01"

PAIRS = [
    (os.path.join(SRC, OLD_STEM + ".py"), os.path.join(SRC, NEW_STEM + ".py")),
    (os.path.join(DAT, OLD_STEM + ".json"), os.path.join(DAT, NEW_STEM + ".json")),
    (os.path.join(DAT, OLD_STEM + ".md"), os.path.join(DAT, NEW_STEM + ".md")),
    (os.path.join(DAT, OLD_STEM + "_report.txt"), os.path.join(DAT, NEW_STEM + "_report.txt")),
    (os.path.join(JUD, "判定_" + OLD_STEM + ".md"), os.path.join(JUD, "判定_" + NEW_STEM + ".md")),
    (os.path.join(SRC, "_run_r332.py"), os.path.join(SRC, "_run_r335.py")),
]

HTML_OLD = os.path.join(ROOT, "四力统一方程_整性给格只是单通量现象_r332可视化_2026-11-01.html")
HTML_NEW = os.path.join(ROOT, "四力统一方程_整性给格只是单通量现象_r335可视化_2026-11-01.html")
PAIRS.append((HTML_OLD, HTML_NEW))

# ---- step 1: move (idempotent: skip if old missing and new present) ----
moved = 0
skipped = 0
for old, new in PAIRS:
    if os.path.exists(old):
        if os.path.exists(new):
            print("[STOP] both exist, refusing: %s" % os.path.basename(new))
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

# ---- step 2: content replacement ----
# order matters: handle X-R332-* (upper) before bare r332 (lower); they do not overlap anyway.
REPL = [("X-R332-", "X-R335-"), ("TUFT-r332", "TUFT-r335"),
        ("r332", "r335"), ("R332", "R335")]

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
        print("[REPL] %-70s %d hits" % (os.path.basename(new)[:70], n))
    else:
        print("[REPL] %-70s 0 hits (clean)" % os.path.basename(new)[:70])

print("[step2] total replacements=%d" % total)

# ---- step 3: residual audit (must be zero) ----
resid = 0
for _, new in PAIRS:
    with io.open(new, "r", encoding="utf-8", newline="") as f:
        txt = f.read()
    bad = txt.count("r332") + txt.count("R332")
    if bad:
        resid += bad
        print("[RESID] %s still has %d" % (os.path.basename(new), bad))
print("[step3] residual=%d" % resid)

# ---- step 4: registry hygiene ----
print("[check] r335 files in 源码/ = %d" % sum(1 for x in os.listdir(SRC) if "r335" in x))
print("[check] r335 files in 数据/ = %d" % sum(1 for x in os.listdir(DAT) if "r335" in x))
print("[check] r335 files in 判定/ = %d" % sum(1 for x in os.listdir(JUD) if "r335" in x))
print("[check] other session r332 intact: %d files in 数据/ = %d"
      % (1, sum(1 for x in os.listdir(DAT) if "r332" in x)))

print("RENUM-OK rc=0" if resid == 0 else "RENUM-FAIL rc=4")
raise SystemExit(0 if resid == 0 else 4)
