# -*- coding: utf-8 -*-
"""ASCII runner for r249 (中文路径不进 argv)。"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = ("TUFT-r249_低能极限推导层_牛顿还原隐含普适质量与禁闭声称单调性反号"
        "_精算与可视化_2026-10-30.py")
p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, NAME)],
                   cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace")
out = (p.stdout or "") + (("\n[STDERR]\n" + p.stderr) if p.stderr else "")
with open(os.path.join(HERE, "_out_r249.txt"), "w", encoding="utf-8") as f:
    f.write(out + "\nrc=%d\n" % p.returncode)
print(out)
print("rc=%d" % p.returncode)
sys.exit(p.returncode)
