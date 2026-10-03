# -*- coding: utf-8 -*-
"""把模块 docstring 换成 pass 后做括号配平 + 二分定位。"""
import io
import sys
import tokenize

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

p = sys.argv[1] if len(sys.argv) > 1 else "29_作用量变分审计_耦合能动张量与迹_2026-10-03.py"
raw = open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
lines = raw.split("\n")

# 用注释屏蔽整个模块 docstring（从 line2 的 """ 到下一个独立 """ 行）
marks = [i for i, ln in enumerate(lines) if ln.strip() == '"""']
if len(marks) >= 2:
    for i in range(marks[0], marks[1] + 1):
        lines[i] = "#" + lines[i]

src = "\n".join(lines)
try:
    compile(src, p, "exec")
    print("COMPILES CLEAN")
except SyntaxError as e:
    print("err:", e.msg, "at line", e.lineno, "offset", e.offset)
    print("text:", repr(lines[e.lineno - 1]) if e.lineno and e.lineno <= len(lines) else "?")
    lo = 1
    for i in range(1, e.lineno + 1):
        try:
            compile("\n".join(lines[:i]), p, "exec")
        except SyntaxError:
            print("CULPRIT PREFIX END:", i)
            for k in range(max(0, i - 3), min(len(lines), i + 3)):
                print("   ", k + 1, repr(lines[k]))
            break

stack = []
try:
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.OP:
            if tok.string in "([{":
                stack.append((tok.string, tok.start[0]))
            elif tok.string in ")]}":
                if not stack:
                    print("EXTRA CLOSE at line", tok.start[0] + 1, repr(lines[tok.start[0]]))
                else:
                    stack.pop()
except Exception as e:
    print("tokenize stopped:", e)
for (s, ln) in stack:
    print("UNCLOSED", s, "opened at line", ln + 1, repr(lines[ln]))
