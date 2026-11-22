# -*- coding: utf-8 -*-
"""纯拼接器：p1+p2+p3+p4 -> _alg_rootv128e_largelambda_vacuity_recompute.py"""
import ast
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(os.path.dirname(HERE), "_scratch")

PARTS = ["_alg_rootv128e_p1.py", "_alg_rootv128e_p2.py",
         "_alg_rootv128e_p3.py", "_alg_rootv128e_p4.py"]
TARGET = "_alg_rootv128e_largelambda_vacuity_recompute.py"

chunks = []
for p in PARTS:
    fp = os.path.join(HERE, p)
    with open(fp, "rb") as fh:
        chunks.append(fh.read().decode("utf-8"))

body = chunks[0].rstrip("\n") + "\n" + "\n".join(c.strip("\n") + "\n" for c in chunks[1:])

ast.parse(body)  # 语法前置检查

tp = os.path.join(HERE, TARGET)
with open(tp, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(body)

raw = open(tp, "rb").read()
print("target    :", TARGET)
print("bytes     :", len(raw))
print("sha256    :", hashlib.sha256(raw).hexdigest())
print("ast_parse : ok")
print("lines     :", body.count("\n") + 1)

os.makedirs(SCRATCH, exist_ok=True)
for p in PARTS:
    src = os.path.join(HERE, p)
    if os.path.exists(src):
        shutil.move(src, os.path.join(SCRATCH, p))
print("parts moved to _scratch/")
