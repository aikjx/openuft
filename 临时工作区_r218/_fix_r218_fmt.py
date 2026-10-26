# -*- coding utf-8 -*-
"""Fix %-format clash in A3 entry (text contains literal '%' signs)."""
import io

ENG = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码\TUFT-r218_四力统一方程_定义恒等式零判别力覆盖缺与修复定价_精算_2026-10-26.py"

t = io.open(ENG, encoding="utf-8").read()

old = '''    add("A3", "L1 定义恒等式",
        "摄动检验：把 Q 放大 10% / 缩小 10%，相符度分别偏离基线 %s / %s——相符完全由输入 "
        "Q 决定，方程内部不存在「Q 应取何值」的约束（内部推导方程计数 0），故相符是"
        "**规定**而非推导。" % (sens["p10"], sens["m10"]),'''

new = '''    add("A3", "L1 定义恒等式",
        "摄动检验：把 Q 放大 10% / 缩小 10%，相符度分别偏离基线 {0} / {1}——"
        "相符完全由输入 Q 决定，方程内部不存在「Q 应取何值」的约束"
        "（内部推导方程计数 0），故相符是**规定**而非推导。".format(
            sens["p10"], sens["m10"]),'''

assert old in t, "A3 anchor miss"
t = t.replace(old, new)

# scan for other %-format strings whose text may contain bare '%' before a non-format char
io.open(ENG, "w", encoding="utf-8").write(t)
print("A3 fixed")
