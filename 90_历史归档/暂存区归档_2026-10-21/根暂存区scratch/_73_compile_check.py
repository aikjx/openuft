# -*- coding: utf-8 -*-
"""编译级检查：73 卷引擎语法/缩进（禁中文路径入 argv，故走本 runner）。"""
import ast
import py_compile
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\73_higgs_stability_calc.py"
with open(SRC, "r", encoding="utf-8") as f:
    src = f.read()
ast.parse(src)
print("AST parse OK, lines =", src.count("\n") + 1)
py_compile.compile(SRC, cfile=r"D:\a10\aikjx\code\my_lib\openuft\scratch\_73_ok.pyc",
                   doraise=True)
print("py_compile OK")
# 结构自检：关键符号存在
for name in ["mh_crit_scan", "mh_triv", "log_scan", "gauge_initial", "rk4_run",
             "instability_scale", "instability_scale_f64", "crossing_from_traj"]:
    assert f"def {name}(" in src, f"missing {name}"
print("symbols OK")
sys.exit(0)
