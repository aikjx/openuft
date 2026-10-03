# -*- coding: utf-8 -*-
"""Ricci 引擎基准测试台：6 个已知答案（含非零答案，用于定符号与定位扇区 bug）。"""
import sys

import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

r = sp.Symbol("r", positive=True)
t_ = sp.Symbol("t")
x_ = sp.Symbol("x")
th = sp.Symbol("th")
MM = sp.Symbol("MM", positive=True)
Lc = sp.Symbol("Lc", positive=True)
H = sp.Symbol("H", positive=True)
aS = sp.Symbol("aS", positive=True)
coords = [t_, r, th, x_]


def ricci(gf, coords, variant="B"):
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
    Gam = [[[sp.S.Zero] * 4 for _ in range(4)] for _ in range(4)]
    for c in range(4):
        for a in range(4):
            for b in range(4):
                s = sp.S.Zero
                for L in range(4):
                    gL = ginv[c, L]
                    A = dg[a]
                    t3 = A[b, L]
                    Bq = dg[b]
                    t5 = Bq[a, L]
                    C = dg[L]
                    t7 = C[a, b]
                    s += gL * (t3 + t5 - t7)
                Gam[c][a][b] = sp.simplify(s / 2)
    Ric = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            s = sp.S.Zero
            for c in range(4):
                G1 = Gam[c]
                if variant == "B":
                    s += sp.diff(G1[a][b], coords[c])
                    s -= sp.diff(G1[c][a], coords[b])
                else:
                    s += sp.diff(G1[a][b], coords[c])
                    s -= sp.diff(G1[a][a], coords[b])
            for c in range(4):
                for L in range(4):
                    G1 = Gam[c]
                    G2 = Gam[L]
                    if variant == "B":
                        s += G1[c][L] * G2[a][b] - G1[b][L] * G2[c][a]
                    else:
                        s += G1[a][L] * G2[b][c] - G1[b][L] * G2[a][c]
            Ric[a, b] = sp.simplify(s)
    R = sp.simplify(sum(ginv[a, b] * Ric[a, b] for a in range(4) for b in range(4)))
    return g, ginv, Ric, sp.simplify(sp.trigsimp(sp.expand(R)))


def diag(v0, v1, v2, v3):
    def f(a, b):
        if a != b:
            return 0
        return (v0, v1, v2, v3)[a]
    return f


TESTS = [
    ("T1 flat-sphere", diag(-1, 1, r ** 2, r ** 2 * sp.sin(th) ** 2), 0, "R"),
    ("T2 2sphere R=2/aS^2", diag(-1, 1, aS ** 2, aS ** 2 * sp.sin(th) ** 2), 2 / aS ** 2, "R"),
    ("T3 warp in xx slot", diag(-1, sp.exp(2 * H * x_), 1, 1), -2 * H ** 2, "R"),
    ("T7 warp in rr slot (T3 equiv)", diag(-1, sp.exp(2 * H * r), 1, 1), -2 * H ** 2, "R"),
    ("T8 T3 renamed slot", diag(-1, 1, 1, sp.exp(2 * H * x_)), -2 * H ** 2, "R"),
    ("T4 Schwarzschild", diag(-1, 1 - 2 * MM / r, r ** 2, r ** 2 * sp.sin(th) ** 2), 0, "R"),
    ("T5 deSitter E_rr=0", diag(-1, 1 - Lc * r ** 2 / 3, r ** 2, r ** 2 * sp.sin(th) ** 2), 0, "E"),
    ("T6 FLRW R=12H^2",
     diag(-1, sp.exp(2 * H * t_), sp.exp(2 * H * t_), sp.exp(2 * H * t_)), 12 * H ** 2, "R"),
]

for variant in ("B", "A"):
    print("#" * 74)
    print("### variant", variant)
    for name, gf, expect, kind in TESTS:
        g, ginv, Ric, R = ricci(gf, coords, variant)
        if kind == "E":
            val = sp.simplify(sp.trigsimp(sp.expand(Ric[1, 1] - sp.Rational(1, 2) * g[1, 1] * R
                                                    + Lc * g[1, 1])))
        else:
            val = R
        ok = sp.simplify(val - expect) == 0
        print("  %-46s R=%s" % (name, R))
        print("  %-46s 判据值=%s 期望=%s  %s" % ("", val, expect, "PASS" if ok else "FAIL"))
