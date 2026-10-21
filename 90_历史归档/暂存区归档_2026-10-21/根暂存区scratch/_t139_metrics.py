# -*- coding: utf-8 -*-
"""r139 新度规单测：管道 vs 解析（Poincare k=-1 / WarpedExp 平直纤维）。
先验证度规类本身，再并入正式卷。"""
import os, sys, math, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "04_公共成果", "本项目_全维自洽与归一化", "源码",
                      "TUFT-r139_全维求导证明验证精算_自旋2路线非线性完备机检_2026-10-21.py")
TARGET = os.path.normpath(TARGET)
NS = runpy.run_path(TARGET, run_name="r139mod")

tensors_at = NS["tensors_at"]
PoincareFRW = NS["PoincareFRW"]
WarpedExpFRW = NS["WarpedExpFRW"]
PowerFRW = NS["PowerFRW"]
DeSitterFRW = NS["DeSitterFRW"]
D = NS["D"]

def cmp_metric(met, x, tag):
    g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, x)
    aG00, aG11, aG22, aG33, aRs = met.analytic(x)
    ref = max(abs(aG00), abs(aG11), abs(aG22), abs(aG33), abs(aRs), 1e-30)
    res = {
        "G00": abs(G[0][0] - aG00) / ref,
        "G11": abs(G[1][1] - aG11) / ref,
        "G22": abs(G[2][2] - aG22) / ref,
        "G33": abs(G[3][3] - aG33) / ref,
        "Rs": abs(Rs - aRs) / ref,
    }
    worst = max(res.values())
    print("[%s] %s" % (tag, met.name))
    print("   x =", x)
    for k in ("G00", "G11", "G22", "G33", "Rs"):
        print("   %-4s 相对 %.3e" % (k, res[k]))
    # 额外：纤维常曲率自检（Poincare 应为 -1）
    print("   R_scalar 计算 %.10e / 解析 %.10e" % (Rs, aRs))
    print("   worst %.3e => %s" % (worst, "PASS" if worst < 1e-9 else "FAIL"))
    return worst

X = [2.0, 0.2, -0.3, 0.1]
bad = 0
w = cmp_metric(PoincareFRW(2.0 / 3.0), X, "Poincare"); bad += (w >= 1e-9)
w = cmp_metric(WarpedExpFRW(2.0 / 3.0), X, "WarpedExp"); bad += (w >= 1e-9)
# 回归：原有两族在非零空间坐标点上仍应通过
w = cmp_metric(PowerFRW(2.0 / 3.0, "尘埃"), X, "回归"); bad += (w >= 1e-9)
w = cmp_metric(PowerFRW(0.5, "辐射"), X, "回归"); bad += (w >= 1e-9)
w = cmp_metric(DeSitterFRW(0.1), X, "回归"); bad += (w >= 1e-9)

# 平移不变性自检：Poincare 的 ν=i 分量在该点是否真的有牙（算三加法项）
print("")
print("== 逐分量加法项检查（粗查是否有牙） ==")
met = PoincareFRW(2.0 / 3.0)
g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, X)
h = 2.5e-4
dGup = [[0.0] * D for _ in range(D)]
for mu in range(D):
    xp = list(X); xm = list(X)
    xp[mu] += h; xm[mu] -= h
    _, _, _, _, _, _, Gp, _ = tensors_at(met, xp)
    _, _, _, _, _, _, Gm, _ = tensors_at(met, xm)
    for nu in range(D):
        dGup[mu][nu] = (Gp[mu][nu] - Gm[mu][nu]) / (2.0 * h)
trGam = [sum(Gam[a][a][l] for a in range(D)) for l in range(D)]
scale = max(abs(Gup[i][j]) for i in range(D) for j in range(D))
print("   |Gup| scale = %.4e" % scale)
for nu in range(D):
    A1 = sum(dGup[mu][nu] for mu in range(D))
    A2 = sum(trGam[l] * Gup[l][nu] for l in range(D))
    A3 = sum(Gam[nu][mu][l] * Gup[mu][l] for mu in range(D) for l in range(D))
    tot = A1 + A2 + A3
    mag = (abs(A1) + abs(A2) + abs(A3)) / scale
    print("   nu=%d  A1=%.4e A2=%.4e A3=%.4e | 和=%.3e | 项量和/scale=%.4e  => %s"
          % (nu, A1, A2, A3, tot, mag, "TOOTHED" if mag > 1e-3 else "VACUOUS"))

print("")
print("FAIL_COUNT =", bad)
sys.exit(1 if bad else 0)
