# -*- coding: utf-8 -*-
# r358 清场：把探查脚本移入 scratch/（禁 rm -rf）
import os, shutil, sys

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(BASE, "源码")
SC = os.path.join(BASE, "scratch")

names = [
    "_probe_r358.py",
    "_dev_r358_probe.py",
    "_dev_r358_probe2.py",
    "_dev_r358_probe3.py",
    "_dev_r358_probe4.py",
    "_dev_r358_probe5.py",
    "_dev_r358_probe6.py",
    "_dev_r358_probe6b.py",
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

# 残留审计：源码树里除引擎/收口脚本外不应再有 r358 探查件
left = sorted(x for x in os.listdir(SRC) if "r358" in x)
print("[left in 源码/] " + str(len(left)))
for x in left:
    print("   " + x)

# pycache 陈旧 .pyc 会让后续扫号误判该号仍被占
pc = os.path.join(SRC, "__pycache__")
if os.path.isdir(pc):
    pyc = sorted(x for x in os.listdir(pc) if "r358" in x)
    print("[pycache r358 pyc] " + str(len(pyc)))
    for x in pyc:
        shutil.move(os.path.join(pc, x), os.path.join(SC, "_dup2_pyc_" + x))
        print("[moved pyc] " + x)
else:
    print("[pycache] none")

sys.exit(0 if (moved + len(missing)) == len(names) else 4)
