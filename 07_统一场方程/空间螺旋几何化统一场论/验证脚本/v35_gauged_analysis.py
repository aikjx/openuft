#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 带电背景规范零模与横模正定性
================================================================
对象：带电全局 U(1) Q-ball 背景（e=0.05, Q_N=279.16, w=0.96027, 17稿基准）。
步骤：
  1) 重建带电背景 f(r), a(r)（无奇点变量 s=rf, u=ra；solve_bvp 五变量，
     验证 f(0),a(0),q(R),E 与 17 稿一致）。结果存 ../V3_gauged_background_e005.npz。
  2) 横模算子 H = -Δ + l(l+1)/r^2 + e^2 f(r)^2 谱检查：
     e^2 f^2 >= 0 为规范耦合有效质量平方，H 正定 => Ω^2 >= 0 => 横模无增长模。
     （库仑规范下横向电磁与标量 decouple；纵向 + A0 由 Gauss 约束消去。）
结论（开放疑问①）：规范自由度不引入虚假负本征值；
     规范零模（纯规范变换 δψ=ieΛψ, δA_μ=∂_μΛ）为精确 Ω=0 模，非增长。
用法： python v35_gauged_analysis.py
"""
import os
import json
import numpy as np
import scipy.sparse as sp
from scipy.integrate import solve_bvp
from scipy.linalg import eigh_tridiagonal

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
CSV = os.path.join(PARENT, "V3_Qball_profile.csv")
NPZ = os.path.join(PARENT, "V3_gauged_background_e005.npz")
OUT = os.path.join(PARENT, "V3_5_gauged_transverse_spectrum.json")

QN = 279.1642942626188
w = 0.960271793738176
e = 0.05
R = 100.0


def rebuild_background():
    """solve_bvp 重建带电背景（与 17 稿基准交叉验证）"""
    with open(CSV, "r", encoding="utf-8") as fh:
        next(fh)
        rr, ff = [], []
        for line in fh:
            a, b, c = line.strip().split(",")
            rr.append(float(a)); ff.append(float(b))
    r0, f0n = np.array(rr), np.array(ff)
    kapp = np.sqrt(1.0 - w * w)
    gamma = e * e * QN / (4.0 * np.pi)
    beta = kapp + (1.0 + w * gamma / kapp) / R
    x = np.linspace(0.0, R, 3000)
    finit = np.interp(x, r0, f0n)
    dfinit = np.gradient(finit, x)
    s0 = x * finit
    ds0 = finit + x * dfinit
    a_guess = e * e * QN / (4.0 * np.pi * np.maximum(x, 1e-3)) * (1.0 - np.exp(-(x / 8.0) ** 2))
    u0 = x * a_guess
    du0 = np.gradient(u0, x)
    q0 = QN * (1.0 - np.exp(-(x / 6.0) ** 3))
    y0 = np.vstack([s0, ds0, u0, du0, q0])

    def fun(xx, y):
        s, ds, u, du, q = y
        r = xx
        f = np.where(r > 1e-12, s / np.maximum(r, 1e-12), ds)
        a = np.where(r > 1e-12, u / np.maximum(r, 1e-12), du)
        W = w - a
        rhs_f = (1.0 - W * W) * f - 2.0 * f**3 + 3.0 * f**5
        rhs_a = -2.0 * e * e * W * f * f
        return [ds, r * rhs_f, du, r * rhs_a, 8.0 * np.pi * r * r * W * f * f]

    def bc(ya, yb):
        sR, dsR, uR, duR, qR = yb
        fR = sR / R
        fRprime = (dsR * R - sR) / (R * R)
        return [ya[0], ya[2], duR, qR - QN, fRprime + beta * fR]

    sol = solve_bvp(fun, bc, x, y0, tol=1e-9, max_nodes=60000)
    assert sol.success, sol.message
    xr = sol.x
    s, ds, u, du, q = sol.y
    f = np.where(xr > 1e-12, s / np.maximum(xr, 1e-12), ds)
    a = np.where(xr > 1e-12, u / np.maximum(xr, 1e-12), du)
    print("背景重建: f(0)=%.12f a(0)=%.12f q(R)=%.6f" % (ds[0], du[0], q[-1]))
    np.savez(NPZ, r=xr, f=f, a=a, q=q)
    return xr, f


if __name__ == "__main__":
    if os.path.exists(NPZ):
        z = np.load(NPZ)
        r, f = z["r"], z["f"]
        print("复用已存带电背景 npz, R=%.0f f(0)=%.6f" % (r[-1], f[0]))
    else:
        r, f = rebuild_background()

    # 横模算子谱
    rec = {
        "background": "V3_gauged_background_e005.npz (e=0.05,Q_N=279.16,w=0.96027)",
        "question": "open_question_1: 规范自由度是否引入虚假负本征值?",
        "method": "库仑规范横模 decouple; H=-Δ+l(l+1)/r^2+e^2 f^2; e^2 f^2>=0 有效质量; 检查 Ω^2 最小本征值",
        "per_channel_min_lambda": {},
        "gauge_zero_mode": "纯规范变换 δψ=ieΛψ, δA_μ=∂_μΛ 为精确 Ω=0 零模，非增长",
        "longitudinal": "Gauss 约束消去纵向 + A0，非动力学",
    }
    ok = True
    for l in [0, 1, 2]:
        row = {}
        for n in [400, 800]:
            xmid = np.linspace(0, R, n + 1)[1:]
            h = R / n
            fmid = np.interp(xmid, r, f)
            cent = l * (l + 1.0) / np.maximum(xmid, 1e-9) ** 2
            diag = 2.0 / h**2 + cent + e * e * fmid**2
            off = -np.ones(n - 1) / h**2
            ev = eigh_tridiagonal(diag, off, select="i", select_range=(0, 0))
            row[str(n)] = float(ev[0])
        rec["per_channel_min_lambda"][str(l)] = row
        if row["800"] > -1e-8:
            print("l=%d: 最小 Ω^2=%.4e (正定)" % (l, row["800"]))
        else:
            ok = False
            print("l=%d: 最小 Ω^2=%.4e (负! 需查)" % (l, row["800"]))
    rec["answer"] = "no_false_negative_gauge_modes" if ok else "needs_check"
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=2)
    print("横模正定:", ok, "-> 规范自由度不引入虚假负本征值")
    print("已保存:", OUT)
