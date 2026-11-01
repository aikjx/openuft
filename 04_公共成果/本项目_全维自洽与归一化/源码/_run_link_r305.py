# -*- coding: utf-8 -*-
"""r305 链接体检 runner（ASCII 入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = "_check_r305_links.py"
OUT = os.path.join(SRC, "_out_link_r305.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt)
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
