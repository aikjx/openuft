# -*- coding: utf-8 -*-
"""Driver for r238: run the two r238 engines directly, capture stdout to _r238_out.txt.

r238 is one round with two 增量层 deliverables (both under the 四力统一 project):
  (a) warp 母稿残余面攻破（爱因斯坦张量实算与中微子 Casimir 议程审计）
  (b) 四力统一方程·高阶 PN 波形层（TaylorF2 牛顿阶 SPA 与 chirp 质量反演）
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "源码")
OUT = os.path.join(ROOT, "_r238_out.txt")

ENGINES = [
    "TUFT-r238_warp母稿残余面攻破_爱因斯坦张量实算与中微子Casimir议程审计_2026-10-26.py",
    "TUFT-r238_四力统一方程_高阶PN波形层_TaylorF2牛顿阶SPA与chirp质量反演_精算与交互可视化_2026-10-26.py",
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
