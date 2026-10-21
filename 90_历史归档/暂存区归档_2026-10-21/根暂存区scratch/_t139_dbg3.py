# -*- coding: utf-8 -*-
"""诊断：Kretschmann K 在 辐射(k=0) 与 图变换 两个度规上为何不等。"""
import os, math, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.normpath(os.path.join(
    HERE, "..", "04_公共成果", "本项目_全维自洽与归一化", "源码",
    "TUFT-r139_全维求导证明验证精算_自旋2路线非线性完备机检_2026-10-21.py"))
NS = runpy.run_path(TARGET, run_name="r139mod")
tensors_at = NS["tensors_at"]; kret = NS["kretschmann"]
D = NS["D"]
PoincareFRW = NS["PoincareFRW"]; WarpedExpFRW = NS["WarpedExpFRW"]
PowerFRW = NS["PowerFRW"]; DeSitterFRW = NS["DeSitterFRW"]
X = [2.0, 0.2, -0.3, 0.1]

def show(met, tag):
    g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, X)
    K = kret(met, X)
    print("%-34s R=%.8e  K=%.8e" % (tag, Rs, K))
    return K

print("== p 扫描：图变换度规（纤维平直 ⇒ 应与同 p 的 k=0 FRW 完全相同）==")
for p in (0.0, 0.5, 2.0 / 3.0):
    k1 = show(PowerFRW(p, "k0 p=%.4g" % p), "PowerFRW    p=%.4g" % p)
    k2 = show(WarpedExpFRW(p, "warp p=%.4g" % p), "WarpedExp   p=%.4g" % p)
    print("   相对差 %.3e" % (abs(k1 - k2) / max(abs(k1), 1e-30)))

print("")
print("== 纤维平直性自检：3D 纤维 γ_ij=e^{2x_i}δ_ij 的 Ricci（应恒零）==")
# 用一个 4D 静态度规 ds2 = -dt^2 + γ 直接算 4D Ricci：若为乘积平直 ⇒ 应为 0
met = WarpedExpFRW(0.0, "warp p=0")
g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, X)
print("   p=0 时 R=%.3e  G=%.3e  K=%.3e  （Minkowski 伪装 ⇒ 全应为 0）" % (
    Rs, abs(G[0][0]), kret(met, X)))
print("   非零 Christoffel:", [(a, m, n, round(Gam[a][m][n], 6))
                               for a in range(D) for m in range(D) for n in range(m, D)
                               if abs(Gam[a][m][n]) > 1e-12])

print("")
print("== 对照：Poincaré 球纤维（常曲率 -1）应为非平直 ==")
show(PoincareFRW(0.0, "poincare p=0"), "PoincareFRW p=0（a≡1，纤维 k=-1）")
show(PoincareFRW(2.0 / 3.0), "PoincareFRW p=2/3")
show(DeSitterFRW(0.1), "deSitter H=0.1")
