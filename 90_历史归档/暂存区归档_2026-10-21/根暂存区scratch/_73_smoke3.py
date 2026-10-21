# -*- coding: utf-8 -*-
"""B3 分解前提冒烟：A_BM 读数 + mh_crit_A_BM 括号检验。"""
import runpy
from mpmath import mpf, log, exp

SRC = "D:/a10/aikjx/code/my_lib/openuft/07_统一场方程/73_higgs_stability_calc.py"
mod = runpy.run_path(SRC)
assemble = mod["assemble"]
lam_at_mpl = mod["lam_at_mpl"]
V = mod["V"]
BM_M_H, BM_M_T = mod["BM_M_H"], mod["BM_M_T"]
DT = mpf("0.01")

print("== A_BM（LO 匹配 @ 文献锚点）==")
out = assemble(BM_M_H, BM_M_T, None, None, 2, DT)
lam_I = None if out["t_cross0"] is None else exp(out["t_cross0"])
print("  λ(M_Pl) = %.6f   Λ_I = %s GeV (log10 = %s)" % (
    out["lam_Mpl"], lam_I, None if lam_I is None else log(lam_I) / log(10)))

print("== mh_crit_A_BM 括号检验（f=λ(M_Pl) @ BM_M_T, LO 匹配）==")


def f(mh):
    return lam_at_mpl(mpf(mh), BM_M_T, None, None, 2, DT)


for mh in ["110", "120", "130", "140", "150"]:
    print("  f(%s) = %.6f" % (mh, f(mh)))
fa, fb = f("110"), f("150")
print("  bracket [110,150]: fa*fb =", "OK (<0)" if fa * fb < 0 else "FAIL (>=0)")
