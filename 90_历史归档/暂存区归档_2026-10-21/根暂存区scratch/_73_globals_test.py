# -*- coding: utf-8 -*-
"""验证 runpy.run_path 返回 dict 的写可见性 + 纪元机制。"""
import runpy
from mpmath import mp, mpf, log, exp

SRC = r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\73_higgs_stability_calc.py"
mod = runpy.run_path(SRC)

gi = mod["gauge_initial"]
print("gauge_initial.__globals__ is mod ?", gi.__globals__ is mod)
print("mod['A3_MZ'] =", mod["A3_MZ"])
print("gi.__globals__.get('A3_MZ') =", gi.__globals__.get("A3_MZ"))

# 写测试
mod["A3_MZ"] = mpf("0.1189")
print("after write: mod =", mod["A3_MZ"], " gi.__globals__ =", gi.__globals__.get("A3_MZ"))

# 纪元测试
e0 = mod["_GAUGE_EPOCH"]
g1 = gi()
e1 = mod["_GAUGE_EPOCH"]
print("epoch before/after first gauge_initial:", e0, e1)
mod["A3_MZ"] = mpf("0.1180")
g2 = gi()
e2 = mod["_GAUGE_EPOCH"]
print("epoch after A3 restored:", e2, " g3 =", mp.nstr(g2[2], 8))
mod["A3_MZ"] = mpf("0.1189")
g3 = gi()
e3 = mod["_GAUGE_EPOCH"]
print("epoch after A3 perturbed:", e3, " g3 =", mp.nstr(g3[2], 8))
