# -*- coding: utf-8 -*-
"""driver：subprocess 调用中文名 runner，输出写入 ASCII 文件后由 Read 读取。"""
import os
import subprocess
import sys

PY = sys.executable
HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "04_公共成果", "本项目_全维自洽与归一化", "源码", "_run_r161.py")
OUT = os.path.join(HERE, "_r161_out.txt")

if not os.path.isfile(RUNNER):
    print("RUNNER NOT FOUND: %s" % RUNNER)
    sys.exit(3)

p = subprocess.run([PY, "-X", "utf8", RUNNER],
                   capture_output=True, cwd=os.path.dirname(RUNNER))
data = p.stdout.decode("utf-8", errors="replace") + p.stderr.decode("utf-8", errors="replace")
with open(OUT, "w", encoding="utf-8") as f:
    f.write(data)
    f.write("\n[EXIT CODE] %d\n" % p.returncode)
print("rc = %d" % p.returncode)
print("out -> %s (%d chars)" % (OUT, len(data)))
sys.exit(p.returncode)
