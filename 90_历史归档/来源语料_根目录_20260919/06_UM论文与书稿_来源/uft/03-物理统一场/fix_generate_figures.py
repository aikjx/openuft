# -*- coding: utf-8 -*-
import subprocess, os

path = r"D:\a10\aikjx\code\my_lib\uft\arxiv\code\generate_figures.py"
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

old = "    experiment = [1/137.036, 0.03106, 0.1179]"
new = ("    # E10 CRITICAL: use M_Z-scale INDEPENDENT values consistently.\n"
       "    # alpha_EM(M_Z)=1/127.955, alpha_2(M_Z)=0.0338 (NOT 4*alpha_EM=0.03106, circular)\n"
       "    # alpha_S(M_Z)=0.1179. All at M_Z scale for valid comparison.\n"
       "    experiment = [1/127.955, 0.0338, 0.1179]")

if old in code:
    code = code.replace(old, new, 1)
    print("REPLACED")
else:
    print("NOT FOUND")

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

# Regenerate figures
r = subprocess.run(["python", path], capture_output=True, text=True, encoding='utf-8',
                   cwd=r"D:\a10\aikjx\code\my_lib\uft\arxiv\code")
print("=== REGEN OUTPUT ===")
print(r.stdout)
print(r.stderr[-800:])
print("EXIT", r.returncode)
