import io, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
tgt = os.path.join(here, "TUFT-r270_可机检验收规范层_统一场论验收器十二条必要条件与正负对照及GR_SM_TUFT三对象实跑_精算与可视化_2026-10-31.py")
out = os.path.join(here, "_out_r270.txt")
p = subprocess.Popen([sys.executable, "-X", "utf8", tgt],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=here)
data, _ = p.communicate()
txt = data.decode("utf-8", "replace")
with io.open(out, "w", encoding="utf-8", newline="") as f:
    f.write(txt)
print(txt)
print("RC =", p.returncode)
