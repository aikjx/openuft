# -*- coding: utf-8 -*-
"""逐分量有牙/空转普查：对每个度规的 ν=0..3 分解三个加法项。"""
import os, math, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.normpath(os.path.join(
    HERE, "..", "04_公共成果", "本项目_全维自洽与归一化", "源码",
    "TUFT-r139_全维求导证明验证精算_自旋2路线非线性完备机检_2026-10-21.py"))
NS = runpy.run_path(TARGET, run_name="r139mod")
tensors_at = NS["tensors_at"]; D = NS["D"]
MET = [NS["PowerFRW"](2.0 / 3.0, "尘埃"),
       NS["PowerFRW"](0.5, "辐射"),
       NS["PoincareFRW"](2.0 / 3.0),
       NS["WarpedExpFRW"](2.0 / 3.0),
       NS["DeSitterFRW"](0.1)]
X = [2.0, 0.2, -0.3, 0.1]
h = 2.5e-4

for met in MET:
    g, ginv, Gam, Ric, Rs, G, Gup, Rup = tensors_at(met, X)
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
    print("[%s]  |Gup| scale=%.4e  R=%.5e" % (met.name, scale, Rs))
    for nu in range(D):
        A1 = sum(dGup[mu][nu] for mu in range(D))
        A2 = sum(trGam[l] * Gup[l][nu] for l in range(D))
        A3 = sum(Gam[nu][mu][l] * Gup[mu][l] for mu in range(D) for l in range(D))
        tot = A1 + A2 + A3
        mag = (abs(A1) + abs(A2) + abs(A3)) / scale
        tag = "TOOTHED" if mag > 1e-3 else "VACUOUS(逐项为零)"
        print("   nu=%d A1=%+.3e A2=%+.3e A3=%+.3e 和=%+.3e 项量和/scale=%.3e %s"
              % (nu, A1, A2, A3, tot, mag, tag))
    print("")
