# -*- coding: utf-8 -*-
"""Driver for r239: run the r239 engine directly, capture stdout to _r239_out.txt.

r239 is one round with one 增量层 deliverable (四力统一 project):
  四力统一方程·Kerr 测地线层（旋转黑洞 ISCO(a)、光子球、顺/逆行方向效应）
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "源码")
OUT = os.path.join(ROOT, "_r239_out.txt")

ENGINES = [
    "TUFT-r239_四力统一方程_Kerr测地线层_旋转黑洞ISCO与光子球_精算与交互可视化_2026-10-26.py",
]

chunks = []
rc_max = 0
for name in ENGINES:
    run = os.path.join(SRC, name)
    chunks.append("=" * 78)
    chunks.append("ENGINE: %s" % name)
    chunks.append("=" * 78)
    if not os.path.exists(run):
        chunks.append("[MISSING] %s" % run)
        rc_max = 1
        continue
    p = subprocess.run([sys.executable, "-X", "utf8", run],
                       capture_output=True, text=True, encoding="utf-8")
    chunks.append(p.stdout or "")
    if p.stderr:
        chunks.append("\n[STDERR]\n" + p.stderr)
    rc_max = max(rc_max, p.returncode)
    chunks.append("rc=%d" % p.returncode)
    chunks.append("")

text = "\n".join(chunks)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print("rc_max=%d chars=%d out=%s" % (rc_max, len(text), OUT))
sys.exit(rc_max)
