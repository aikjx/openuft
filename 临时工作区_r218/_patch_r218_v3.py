# -*- coding: utf-8 -*-
"""r218 polish: raw docstring (kill SyntaxWarning) + machine-driven G11 distribution assertion."""
import io

ENG = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码\TUFT-r218_四力统一方程_定义恒等式零判别力覆盖缺与修复定价_精算_2026-10-26.py"

t = io.open(ENG, encoding="utf-8").read()

# 1) make derived_external_equations docstring raw
old_doc = '''def derived_external_equations(md):
    """'''
new_doc = '''def derived_external_equations(md):
    r"""'''
assert old_doc in t
t = t.replace(old_doc, new_doc, 1)

# 2) G11: machine-driven distribution assertion (was hardcoded True)
old_g11 = '''    grd("G11", "条目分布断言（本卷实算后登记）", True, "")'''
new_g11 = '''    grd("G11", "条目分布断言：total=19 且 {FAIL:13, PASS:3, INFO:3}",
        len(ENTRIES) == 19 and cnt.get("FAIL", 0) == 13 and cnt.get("PASS", 0) == 3
        and cnt.get("INFO", 0) == 3,
        str(cnt))'''
assert old_g11 in t
t = t.replace(old_g11, new_g11)

# G11 is now computed -> remove from the ast whitelist so the self-audit really checks it
old_allow = '''            allow = {"C26", "G2", "G3", "G6", "G8", "G11", "G12"}'''
new_allow = '''            allow = {"C26", "G2", "G3", "G6", "G8", "G12"}'''
assert old_allow in t
t = t.replace(old_allow, new_allow)

io.open(ENG, "w", encoding="utf-8").write(t)
print("polished")
