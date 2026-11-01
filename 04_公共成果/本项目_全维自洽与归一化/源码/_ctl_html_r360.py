# -*- coding: utf-8 -*-
"""r360 HTML 几何体检的负对照：把第一个 rect 宽度改为 0，checker 必须报错且 rc != 0"""

import os
import shutil
import subprocess

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(BASE, "TUFT-r360_ROOTV29_DiracMaxwell自洽性_可视化_2026-11-02.html")
NEG = os.path.join(BASE, "_negctl_r360.html")      # ASCII 名：中文禁入 argv
SCRATCH = os.path.join(BASE, "scratch")
CHECK = os.path.join(BASE, "源码", "_check_html_geom.js")

with open(SRC, "r", encoding="utf-8") as f:
    s = f.read()

old = 'mk("panel1", "rect", { x: 0, y: 0, width: W, height: H, fill: "#ffffff", stroke: "#e6e9ee" });'
assert s.count(old) == 1, "anchor hit %d" % s.count(old)
new = 'mk("panel1", "rect", { x: 0, y: 0, width: 0, height: H, fill: "#ffffff", stroke: "#e6e9ee" });'
with open(NEG, "w", encoding="utf-8") as f:
    f.write(s.replace(old, new))

p = subprocess.run(["node", CHECK, "_negctl_r360.html"], cwd=BASE,
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
out = (p.stdout or "") + (p.stderr or "")

hit_invisible = ("宽度为 0" in out) and ("不可见" in out)
ok = (p.returncode != 0) and hit_invisible

print("NEG-RC      =", p.returncode)
print("NEG-OUT     =", out.strip()[:400])
print("HIT_INVIS   =", hit_invisible)
print("VERDICT_NEG =", "PASS" if ok else "FAIL")

if not os.path.isdir(SCRATCH):
    os.makedirs(SCRATCH)
dst = os.path.join(SCRATCH, "_negctl_r360.html")
if os.path.exists(dst):
    os.remove(dst)
shutil.move(NEG, dst)
print("MOVED       =", dst)
