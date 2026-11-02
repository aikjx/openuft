# -*- coding: utf-8 -*-
# r366 清场：把探查脚本移入 scratch/（禁 rm -rf）
import os, shutil, sys

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(BASE, "源码")
SC = os.path.join(BASE, "scratch")

names = [
    "_probe_r366.py",
    "_dev_r366_probe.py",
    "_dev_r366_probe2.py",
    "_dev_r366_probe3.py",
    "_dev_r366_probe3b.py",
    "_dev_r366_probe4.py",
]

moved = 0
missing = []
for n in names:
    p = os.path.join(SRC, n)
    if not os.path.exists(p):
        missing.append(n)
        continue
    dst = os.path.join(SC, n)
    if os.path.exists(dst):
        dst = os.path.join(SC, "_dup2_" + n)
    shutil.move(p, dst)
    moved += 1
    print("[moved] %s -> scratch/" % n)

print("[clean] moved=%d missing=%d" % (moved, len(missing)))
for n in missing:
    print("[missing] " + n)

left = sorted(x for x in os.listdir(SRC) if "r366" in x)
print("[left in 源码/] " + str(len(left)))
for x in left:
    print("   " + x)

pc = os.path.join(SRC, "__pycache__")
if os.path.isdir(pc):
    pyc = sorted(x for x in os.listdir(pc) if "r366" in x)
    print("[pycache r366 pyc] " + str(len(pyc)))
    for x in pyc:
        shutil.move(os.path.join(pc, x), os.path.join(SC, "_dup2_pyc_" + x))
        print("[moved pyc] " + x)
else:
    print("[pycache] none")

sys.exit(0 if (moved + len(missing)) == len(names) else 4)
