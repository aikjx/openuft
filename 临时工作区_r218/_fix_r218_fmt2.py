# -*- coding: utf-8 -*-
"""Replace the perturbation block (line 892..895) with .format version (no % clash)."""
import io

ENG = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码\TUFT-r218_四力统一方程_定义恒等式零判别力覆盖缺与修复定价_精算_2026-10-26.py"

lines = io.open(ENG, encoding="utf-8").read().split("\n")
i0 = next(i for i, l in enumerate(lines) if "摄动检验：Q" in l)
# find the end of the statement (line containing 'len(kn["derived_external_eq"])')
i1 = i0
while "derived_external_eq" not in lines[i1] and i1 < i0 + 8:
    i1 += 1

new = [
    '    L.append("- 摄动检验：Q \u00b110% \u21d2 相符度偏离 {0} / {1}；方程内部**无**「Q 应取何值」的"',
    '             "约束（框架内推导方程计数 = {2}）\u21d2 相符是**规定**而非推导。".format(',
    '                 kn["sensitivity"]["p10"], kn["sensitivity"]["m10"],',
    '                 len(kn["derived_external_eq"])))',
]
lines[i0:i1 + 1] = new
io.open(ENG, "w", encoding="utf-8").write("\n".join(lines))
print("patched lines %d..%d" % (i0 + 1, i1 + 1))
