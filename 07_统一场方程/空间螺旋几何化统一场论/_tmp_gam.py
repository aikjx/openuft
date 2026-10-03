# -*- coding: utf-8 -*-
"""打印 T3/T7 的 Christoffel，与解析值对拍。"""
import sys

import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

r = sp.Symbol("r", positive=True)
t_ = sp.Symbol("t")
th = sp.Symbol("th")
x_ = sp.Symbol("x")
H = sp.Symbol("H", positive=True)
coords = [t_, r, th, x_]


def diag(v):
    def f(a, b):
        return 0 if a != b else v[a]
    return f


def gam_of(gf):
    g = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            g[a, b] = sp.simplify(gf(a, b))
    ginv = g.inv()
    dg = [sp.zeros(4, 4) for _ in range(4)]
    for c in range(4):
        for a in range(4):
            for b in range(4):
                dg[c][a, b] = sp.diff(g[a, b], coords[c])
    print("  g      =", g.tolist())
    print("  dg[0]  =", dg[0].tolist())
    print("  dg[1]  =", dg[1].tolist())
    print("  dg[2]  =", dg[2].tolist())
    print("  dg[3]  =", dg[3].tolist())
    out = {}
    for c in range(4):
        for a in range(4):
            for b in range(4):
                s = sp.S.Zero
                for L in range(4):
                    s += ginv[c, L] * (dg[a][b, L] + dg[b][a, L] - dg[L][a, b])
                v = sp.simplify(s / 2)
                if v != 0:
                    out[(c, a, b)] = v
    return out


print("T3: g=diag(-1, e^{2Hx}, 1, 1)   期望非零: Gam[1][1][3]=H, Gam[1][3][1]=H, Gam[3][1][1]=-H*e^{2Hx}")
g3 = gam_of(diag([-1, sp.exp(2 * H * x_), 1, 1]))
for k in sorted(g3):
    print("   Gam%s = %s" % (str(k), g3[k]))

print()
print("T7: g=diag(-1, e^{2Hr}, 1, 1)   期望非零: Gam[1][1][1]=H")
g7 = gam_of(diag([-1, sp.exp(2 * H * r), 1, 1]))
for k in sorted(g7):
    print("   Gam%s = %s" % (str(k), g7[k]))
