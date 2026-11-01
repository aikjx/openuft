import glob
import os
import sys
import subprocess

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
hits = glob.glob(os.path.join(BASE, "源码", "TUFT-r360_ROOTV29*.py"))
assert len(hits) == 1, "glob hit count != 1: %r" % (hits,)
src = hits[0]
print("RUN:", os.path.basename(src))

env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
p = subprocess.run([sys.executable, src], cwd=os.path.join(BASE, "源码"),
                   capture_output=True, text=True, encoding="utf-8", env=env)
out = (p.stdout or "") + ("\n[STDERR]\n" + p.stderr if p.stderr else "")
with open(os.path.join(BASE, "源码", "_out_r360.txt"), "w", encoding="utf-8") as f:
    f.write(out)
print(out[-7000:])
print("RC =", p.returncode)
