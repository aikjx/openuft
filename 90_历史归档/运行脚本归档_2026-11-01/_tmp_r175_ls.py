import os
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = r"d:/a10/aikjx/code/my_lib/openuft/01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集"
TARGETS = [
    "04引力场定义方程",
    "06-运动动量方程",
    "07-宇宙大统一方程（力方程）",
    "08-空间波动方程",
    "10-电场定义方程",
    "11-磁场定义方程",
    "12-变化的引力场产生电磁场",
    "19-引力光速统一方程",
]
for name in TARGETS:
    d = os.path.join(BASE, name)
    print("==", name, "==")
    for dp, dns, fns in os.walk(d):
        for f in sorted(fns):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, d)
            print("   %-56s %8d" % (rel, os.path.getsize(p)))
