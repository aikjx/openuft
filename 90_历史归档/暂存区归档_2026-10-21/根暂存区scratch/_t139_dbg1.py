# -*- coding: utf-8 -*-
"""定位：WarpedExp 取 p=0（a≡1）时应为 Minkowski 伪装 ⇒ R≡0, G≡0。"""
import os, math, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.normpath(os.path.join(
    HERE, "..", "04_公共成果", "本项目_全维自洽与归一化", "源码",
    "TUFT-r139_全维求导证明验证精算_自旋2路线非线性完备机检_2026-10-21.py"))
NS = runpy.run_path(TARGET, run_name="r139mod")
tensors_at = NS["tensors_at"]; WarpedExpFRW = NS["WarpedExpFRW"]

X = [2.0, 0.2, -0.3, 0.1]
for p in (0.0, 2.0 / 3.0):
    met = WarpedExpFRW(p, "warp p=%.4g" % p)
    g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, X)
    print("p=%.4g  R=%.10e  G00=%.6e G11=%.6e G22=%.6e G33=%.6e" % (
        p, Rs, G[0][0], G[1][1], G[2][2], G[3][3]))
    print("   analytic:", ["%.6e" % v for v in met.analytic(X)])
    # 打印非零 Christoffel，人工核对
    nz = []
    for a in range(4):
        for m in range(4):
            for n in range(m, 4):
                if abs(Gam[a][m][n]) > 1e-12:
                    nz.append("G^%d_%d%d=%.5f" % (a, m, n, Gam[a][m][n]))
    print("   Gamma:", nz)
    # 逐项核对 dg：解析 ∂_b g_mn
    dg = met.dg(X)
    print("   dg[1][1][0]=%.6f (期望 2a*a'=0 for p=0)" % dg[1][1][0])
    print("   dg[1][1][1]=%.6f (期望 2a^2 E1=%.6f)" % (dg[1][1][1], 2 * math.exp(0.4)))
    ddg = met.ddg(X)
    print("   ddg[0][0][1][1]=%.6f  ddg[0][1][1][1]=%.6f  ddg[1][1][1][1]=%.6f" % (
        ddg[0][0][1][1], ddg[0][1][1][1], ddg[1][1][1][1]))
    print("   ddg[1][0][1][1]=%.6f  (对称性：应等于 ddg[0][1][1][1])" % ddg[1][0][1][1])
