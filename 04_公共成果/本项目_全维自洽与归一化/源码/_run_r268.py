# -*- coding: utf-8 -*-
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(
    HERE,
    "TUFT-r268_ROOT-V5.0融合审计_四层分级映射与六条口径消解_Z与Z撇量纲及"
    "旧强场omega失效定理_精算与交互可视化_2026-10-31.py",
)
OUT = os.path.join(HERE, "_out_r268.txt")

p = subprocess.run([sys.executable, "-X", "utf8", ENGINE],
                   cwd=os.path.dirname(HERE), capture_output=True, text=True,
                   encoding="utf-8", errors="replace")
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(p.stdout or "")
    if p.stderr:
        f.write("\n[STDERR]\n" + p.stderr)
print(p.stdout or "")
print("[RC]", p.returncode)
sys.exit(p.returncode)
