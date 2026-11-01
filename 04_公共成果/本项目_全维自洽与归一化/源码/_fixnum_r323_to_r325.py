# -*- coding: utf-8 -*-
"""r323 -> r325 改号留档：只改本卷文件，零碰并行会话的 _run_r323.py / _out_r323.txt / TUFT-r323_电磁侧*.py"""
import io
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRATCH = os.path.join(ROOT, "scratch")

OLD_TAG = "r323"
NEW_TAG = "r325"

OLD_NAME = ("TUFT-r323_通量量子数与稳定性的联立_"
            "Q是否为自由参数与三代选定的第一原理审计_精算与可视化_2026-11-01.py")
NEW_NAME = OLD_NAME.replace(OLD_TAG, NEW_TAG)

src = os.path.join(HERE, OLD_NAME)
dst = os.path.join(HERE, NEW_NAME)
if not os.path.exists(src):
    print("MISSING source: %s" % OLD_NAME)
    raise SystemExit(2)
if os.path.exists(dst):
    print("TARGET already exists (collision!): %s" % NEW_NAME)
    raise SystemExit(3)

s = io.open(src, encoding="utf-8").read()

# 只替换本卷自有的标记（都是带卷号前缀的串，不会误伤模板逻辑）
pairs = [
    ('RID = "r323"', 'RID = "r325"'),
    ('TUFT-r323 · 通量量子数与稳定性的联立', 'TUFT-r325 · 通量量子数与稳定性的联立'),
    ('BASE = ("TUFT-r323_', 'BASE = ("TUFT-r325_'),
    ('[r323]', '[r325]'),
    ('r318/r319/r323', 'r318/r319/r325'),
    ('TUFT-%s . 通量量子数与稳定性的联立', 'TUFT-%s . 通量量子数与稳定性的联立'),
]
n_chg = 0
for a, b in pairs:
    if a in s:
        s = s.replace(a, b)
        n_chg += 1

# 断言：新文件里不得残留旧的卷号锚点
bad = [ln for ln in s.splitlines() if "r323" in ln]
if bad:
    print("RESIDUAL r323 LINES = %d" % len(bad))
    for ln in bad[:5]:
        print("   %s" % ln[:100])
    raise SystemExit(5)

io.open(dst, "w", encoding="utf-8").write(s)
os.remove(src)
print("RENAMED-> %s" % NEW_NAME)
print("replace-patterns-hit = %d" % n_chg)
print("bytes = %d" % len(s.encode("utf-8")))

# 我自己的探针脚本移入 scratch（不是删除）；并行会话的 _run_r323.py / _out_r323.txt 一律不碰
probe = os.path.join(HERE, "_probe_r323.py")
if os.path.exists(probe):
    os.makedirs(SCRATCH, exist_ok=True)
    tgt = os.path.join(SCRATCH, "_probe_r323.py")
    if os.path.exists(tgt):
        os.remove(tgt)
    shutil.move(probe, tgt)
    print("MOVED probe -> scratch/_probe_r323.py")

print("UNTOUCHED (parallel):",
      [f for f in os.listdir(HERE) if f in ("_run_r323.py", "_out_r323.txt")])
print("PARALLEL SOURCE PRESENT:",
      [f for f in os.listdir(HERE) if f.startswith("TUFT-r323_") and "电磁" in f])
