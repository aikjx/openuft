# -*- coding: utf-8 -*-
r"""TUFT-r290 runner：执行引擎、回显尾部、透传退出码、落 _out_r290.txt。"""
import os
import subprocess
import sys

NAME = ("TUFT-r290_高维几何与电磁耦合第一性原理审计_KK规范变换与曲率分解系数验证_"
        "半径模与质量矛盾与radion反作用_精算与交互可视化_2026-10-31.py")
HERE = os.path.dirname(os.path.abspath(__file__))

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, NAME)],
                   capture_output=True)
out = (p.stdout or b"").decode("utf-8", "replace")
err = (p.stderr or b"").decode("utf-8", "replace")
print(out[-4400:])
if err.strip():
    print("[STDERR]", err[-1600:])
with open(os.path.join(HERE, "_out_r290.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(out)
    if err.strip():
        f.write("\n[STDERR]\n" + err)
sys.exit(p.returncode)
