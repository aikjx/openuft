# -*- coding: utf-8 -*-
"""Schwarzschild 的 Gamma / Ricci 逐项对拍（解析已知：真空 => Ric=0, R=0）。"""
import sys

import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

r = sp.Symbol("r", positive=True)
t_ = sp.Symbol("t")
th = sp.Symbol("th")
ph_ = sp.Symbol("ph")
MM = sp.Symbol("MM", positive=True)
coords = [t_, r, th, ph_]


def gfun(a, b):
    if a == b == 0:
        return -1
    if a == b == 1:
        return 1 - 2 * MM / r
    if a == b == 2:
        return r ** 2
    if a == b == 3:
        return r ** 2 * sp.sin(th) ** 2
    return 0


g = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        g[a, b] = sp.simplify(gfun(a, b))
ginv = g.inv()
dg = [sp.zeros(4, 4) for _ in range(4)]
for c in range(4):
    for a in range(4):
        for b in range(4):
            dg[c][a, b] = sp.diff(g[a, b], coords[c])

Gam = [[[sp.S.Zero] * 4 for _ in range(4)] for _ in range(4)]
for c in range(4):
    for a in range(4):
        for b in range(4):
            s = sp.S.Zero
            for L in range(4):
                s += ginv[c, L] * (dg[a][b, L] + dg[b][a, L] - dg[L][a, b])
            Gam[c][a][b] = sp.simplify(s / 2)

print("引擎算出的非零 Gamma（Schwarzschild）：")
EXPECT = {
    (1, 1, 1): MM / (r ** 2 * (-2 * MM + r)),
    (1, 2, 2): -r / (-2 * MM + r),
    (1, 3, 3): -r * sp.sin(th) ** 2 / (-2 * MM + r),
    (2, 1, 2): 1 / r, (2, 2, 1): 1 / r,
    (3, 1, 3): 1 / r, (3, 3, 1): 1 / r,
    (3, 2, 3): sp.cos(th) / sp.sin(th),
    (3, 3, 2): sp.cos(th) / sp.sin(th),
}
got = {}
for c in range(4):
    for a in range(4):
        for b in range(4):
            v = sp.simplify(sp.expand_trig(Gam[c][a][b]))
            if v != 0:
                got[(c, a, b)] = v
for k in sorted(got):
    exp = EXPECT.get(k)
    ok = "" if exp is None else ("  OK" if sp.simplify(got[k] - exp) == 0 else
                                 "  <== 与解析式不符, 解析=%s" % exp)
    print("   Gam%s = %s%s" % (str(k), got[k], ok))
missing = [k for k in EXPECT if k not in got]
extra = [k for k in got if k not in EXPECT]
print("缺失:", missing)
print("多余:", extra)

# 用引擎的 Ricci 公式逐项算 Ric_rr
print()
print("Ric_rr 逐项（variant B）：")
a_, b_ = 1, 1
T1 = sp.S.Zero
T2 = sp.S.Zero
T3 = sp.S.Zero
T4 = sp.S.Zero
for c in range(4):
    T1 += sp.diff(Gam[c][a_][b_], coords[c])
    T2 += sp.diff(Gam[c][c][a_], coords[b_])
for c in range(4):
    for L in range(4):
        T3 += Gam[c][c][L] * Gam[L][a_][b_]
        T4 += Gam[c][b_][L] * Gam[L][c][a_]
print("  T1 = d_c Gam^c_rr          =", sp.simplify(T1))
print("  T2 = d_r Gam^c_cr          =", sp.simplify(T2))
print("  T3 = Gam^c_cL Gam^L_rr     =", sp.simplify(T3))
print("  T4 = Gam^c_rL Gam^L_cr     =", sp.simplify(T4))
print("  Ric_rr = T1-T2+T3-T4 =", sp.simplify(T1 - T2 + T3 - T4))

# 显式黎曼张量（不缩并）算 Ric_rr = sum_rho R^rho_{r rho r}
print()
print("显式黎曼 R^rho_{r rho r} 逐 rho：")
for rho in range(4):
    val = sp.diff(Gam[rho][a_][b_], coords[rho]) - sp.diff(Gam[rho][rho][a_], coords[b_])
    for L in range(4):
        val += Gam[rho][rho][L] * Gam[L][b_][a_] - Gam[rho][b_][L] * Gam[L][rho][a_]
    print("   rho=%d -> %s" % (rho, sp.simplify(val)))
