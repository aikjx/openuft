#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 带电 Q-ball 稳定性相图（能量方法 dQ/dω）
对象：带电全局 U(1) Q-ball，势 U(f)=f^2-f^4+f^6，e=0.05。
从基准 ω0=0.96027（17 稿，Q_N=279.16）向两端延续带电背景（solve_bvp 五变量 s,u,q）。
判据：线性稳定候选 <==> dQ_N/dω < 0（Friedberg-Lee-Sirlin，同 22 稿中性）。
能量 E=4π∫[f'^2+W^2 f^2 + a'^2/(2e^2)+U(f)]r^2 dr；Q=8π∫W f^2 r^2 dr；dE/dQ=ω 一阶自洽检验。
PARENT 输出到体系根。铁律：能量方法为线性稳定必要判据，非完整 6 分量谱。
"""
import os
import json
import numpy as np
from scipy.integrate import solve_bvp

PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(PARENT, "V3_Qball_profile.csv")
OUT = os.path.join(PARENT, "V3_5_gauged_scan_QN_w.json")
R = 100.0
e = 0.05
QN0 = 279.1642942626188
w0 = 0.960271793738176
with open(CSV, "r", encoding="utf-8") as fh:
    next(fh)
    rr, ff = [], []
    for line in fh:
        a, b, c = line.strip().split(",")
        rr.append(float(a)); ff.append(float(b))
r0, f0n = np.array(rr), np.array(ff)


def solve_gauged(w, init_f, QN_est):
    """带电 Q-ball：固定 ω、QN 渐近估计 beta，q(R) 自由输出（延续自洽）。"""
    kapp = np.sqrt(max(1.0 - w * w, 1e-12))
    gamma = e * e * QN_est / (4.0 * np.pi)
    beta = kapp + (1.0 + w * gamma / kapp) / R
    x = np.linspace(0, R, 2000)
    finit = np.interp(x, init_f[0], init_f[1])
    dfinit = np.gradient(finit, x)
    s0 = x * finit
    ds0 = finit + x * dfinit
    a_guess = e * e * QN_est / (4.0 * np.pi * np.maximum(x, 1e-3)) * (1.0 - np.exp(-(x / 8.0) ** 2))
    u0 = x * a_guess
    du0 = np.gradient(u0, x)
    q0 = QN_est * (1.0 - np.exp(-(x / 6.0) ** 3))
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
        return [ya[0], ya[2], duR, fRprime + beta * fR]

    sol = solve_bvp(fun, bc, x, y0, tol=1e-8, max_nodes=50000)
    if not sol.success:
        return None
    xr = sol.x
    s, ds, u, du, q = sol.y
    f = np.where(xr > 1e-12, s / np.maximum(xr, 1e-12), ds)
    a = np.where(xr > 1e-12, u / np.maximum(xr, 1e-12), du)
    W = w - a
    QN = q[-1]
    # 能量 E=4π∫[f'^2+W^2 f^2 + a'^2/(2e^2)+f^2-f^4+f^6]r^2 dr
    fr = (ds * xr - s) / np.maximum(xr, 1e-12)**2  # f'(r) 无奇点形式
    ar = (du * xr - u) / np.maximum(xr, 1e-12)**2
    integ = (fr**2 + W**2 * f**2 + ar**2/(2*e*e) + f**2 - f**4 + f**6) * xr**2
    E = 4.0 * np.pi * np.trapezoid(integ, xr)
    return {"f0": float(ds[0]), "a0": float(du[0]), "QN": float(QN), "E": float(E),
            "prf": (xr, f)}


if __name__ == "__main__":
    # 基准验证
    base = solve_gauged(w0, (r0, f0n), QN0)
    print("基准 ω=%.5f: f0=%.6f a0=%.6f QN=%.2f E=%.3f" % (w0, base["f0"], base["a0"], base["QN"], base["E"]))

    points = {}
    prev_f = (base["prf"][0], base["prf"][1]); prev_q = base["QN"]
    # 向上
    for w in [0.965, 0.97, 0.975, 0.98, 0.985, 0.99, 0.993, 0.995]:
        r = solve_gauged(w, prev_f, prev_q)
        if r is None:
            print("w=%.3f 未收敛(向上)" % w); break
        points[w] = {"f0": r["f0"], "a0": r["a0"], "QN": r["QN"], "E": r["E"]}
        prev_f = r["prf"]; prev_q = r["QN"]
    prev_f = (base["prf"][0], base["prf"][1]); prev_q = base["QN"]
    # 向下
    for w in [0.955, 0.95, 0.945, 0.94, 0.935, 0.93, 0.925, 0.92, 0.91, 0.90]:
        r = solve_gauged(w, prev_f, prev_q)
        if r is None:
            print("w=%.3f 未收敛(向下)" % w); break
        points[w] = {"f0": r["f0"], "a0": r["a0"], "QN": r["QN"], "E": r["E"]}
        prev_f = r["prf"]; prev_q = r["QN"]
    points[w0] = {"f0": base["f0"], "a0": base["a0"], "QN": base["QN"], "E": base["E"]}

    ws = sorted(points.keys())
    for i in range(1, len(ws)):
        dw = ws[i] - ws[i-1]
        if dw > 0:
            points[ws[i-1]]["dQdw"] = float((points[ws[i]]["QN"] - points[ws[i-1]]["QN"]) / dw)
    scan = [{"w": w, "f0": p["f0"], "a0": p["a0"], "QN": p["QN"], "E": p["E"],
             "dQdw": p.get("dQdw")} for w, p in sorted(points.items())]
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"potential": "f^2-f^4+f^6", "e": e, "R": R, "e0": e, "scan": scan},
                  fh, ensure_ascii=False, indent=2)
    print("\n带电相图 (e=0.05):")
    for s in scan:
        if s["dQdw"] is not None:
            print("w=%.3f Q_N=%9.1f E=%9.2f dQ/dw=%+.0f -> %s"
                  % (s["w"], s["QN"], s["E"], s["dQdw"], "稳定" if s["dQdw"] < 0 else "不稳定"))
    # dE/dQ=ω 一阶检验（相邻点）
    print("\ndE/dQ vs ω（一阶自洽，相邻差分）:")
    for i in range(1, len(scan)):
        dE = scan[i]["E"] - scan[i-1]["E"]
        dQ = scan[i]["QN"] - scan[i-1]["QN"]
        if abs(dQ) > 1e-9:
            wmid = 0.5*(scan[i]["w"] + scan[i-1]["w"])
            print("w~%.3f dE/dQ=%.4f (应≈%.4f)" % (wmid, dE/dQ, wmid))
    print("已保存:", OUT)
