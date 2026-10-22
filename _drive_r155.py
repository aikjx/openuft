# -*- coding: utf-8 -*-
# ASCII driver: run r155 engine via Python subprocess, capture output to file.
import os
import subprocess

PY = r"C:\Users\mo\.workbuddy\binaries\python\versions\3.13.12\python.exe"
BASE = os.path.join("D:\\a10\\aikjx\\code\\my_lib\\openuft",
                    "04_公共成果", "本项目_全维自洽与归一化", "源码")
T = os.path.join(BASE, "_run_r155.py")
OUT = os.path.join(BASE, "_r155_out.txt")

p = subprocess.run([PY, T], capture_output=True, text=True,
                   encoding="utf-8", errors="replace")
txt = p.stdout + "\n===STDERR===\n" + p.stderr + "\n===RC===" + str(p.returncode) + "\n"
with open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print("rc=" + str(p.returncode))
print("out=" + OUT)
