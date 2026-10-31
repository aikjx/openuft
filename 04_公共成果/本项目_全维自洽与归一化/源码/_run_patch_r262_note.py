import io, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
tgt = os.path.join(here, "_patch_readme_r262_note.py")
out = os.path.join(here, "_out_patch_r262_note.txt")
p = subprocess.Popen([sys.executable, "-X", "utf8", tgt],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=here)
data, _ = p.communicate()
txt = data.decode("utf-8", "replace")
with io.open(out, "w", encoding="utf-8", newline="") as f:
    f.write(txt)
print(txt)
print("RC =", p.returncode)
