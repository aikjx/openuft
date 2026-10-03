# -*- coding: utf-8 -*-
"""逐块替换隔离法：把每个顶层块单独抽出编译，定位坏块。"""
import io
import re
import sys
import tokenize

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

p = sys.argv[1] if len(sys.argv) > 1 else "29_作用量变分审计_耦合能动张量与迹_2026-10-03.py"
raw = open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
lines = raw.split("\n")

marks = [i for i, ln in enumerate(lines) if ln.strip() == '"""']
if len(marks) >= 2:
    for i in range(marks[0], marks[1] + 1):
        lines[i] = "#" + lines[i]

# 顶层块边界：非空且首列非空白，且不是续行（括号/引号未闭合的续行以空白或非语句开头）
depth = 0
instr = False
q = ""
starts = []
for i, ln in enumerate(lines):
    if not instr and depth == 0 and ln and not ln[0].isspace() and not ln.lstrip().startswith("#"):
        starts.append(i)
    j = 0
    while j < len(ln):
        ch = ln[j]
        if instr:
            if ch == "\\":
                j += 2
                continue
            if ch == q:
                instr = False
        else:
            if ch == "#":
                break
            if ch == "'" or ch == '"':
                instr = True
                q = ch
            elif ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
        j += 1

print("blocks:", len(starts))
src = "\n".join(lines)
try:
    compile(src, p, "exec")
    print("COMPILES CLEAN")
    raise SystemExit(0)
except SyntaxError as e:
    print("baseline err:", e.msg, "line", e.lineno, repr(lines[e.lineno - 1]))

# 逐块单独编译（块内用 try 包裹以允许依赖前文）
for bi, s in enumerate(starts):
    e_ = starts[bi + 1] if bi + 1 < len(starts) else len(lines)
    body = lines[s:e_]
    # 去掉块首的 docstring 依赖：直接整块 try 编译
    chunk = "try:\n" + "\n".join(("    " + b) if b.strip() else b for b in body) + "\nexcept Exception:\n    pass\n"
    try:
        compile(chunk, p, "exec")
    except SyntaxError as se:
        print("BAD BLOCK at line", s + 1, "->", se.msg, "line", se.lineno)
        for k in range(s, min(e_, s + 12)):
            print("   ", k + 1, repr(lines[k]))
