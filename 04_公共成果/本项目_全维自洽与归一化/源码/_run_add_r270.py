import io, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
tgt = os.path.join(here, "_readme_add_r270.py")
out = os.path.join(here, "_out_add_r270.txt")
p = subprocess.Popen([sys.executable, "-X", "utf8", tgt],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=here)
data, _ = p.communicate()
txt = data.decode("utf-8", "replace")
with io.open(out, "w", encoding="utf-8", newline="") as f:
    f.write(txt)
print(txt)
print("RC =", p.returncode)
