#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 参数扫描：中性 Q-ball 在 (w, Q_N) 平面的稳定性分支
势 U(s)=s-s^2+s^3。从基准 w0=0.9487 向两端逐步延续非平凡分支。
判据：线性稳定候选 <==> dQ_N/dw < 0（Friedberg-Lee-Sirlin；用 v35_scan_recheck.py 复核一致性）。
用法： python v35_param_scan.py
"""
import os
import json
import numpy as np
from scipy.integrate import solve_bvp

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
CSV = os.path.join(PARENT, "V3_Qball_profile.csv")
OUT = os.path.join(PARENT, "V3_5_param_scan_QN_w.json")
R = 80.0
mu2 = lam = g6 = 1.0
with open(CSV, "r", encoding="utf-8") as fh:
    next(fh)
    rr, ff = [], []
    for line in fh:
        a, b, c = line.strip().split(",")
        rr.append(float(a)); ff.append(float(b))
r0, f0n = np.array(rr), np.array(ff)


def solve_neutral(w, init_f):
    kapp = np.sqrt(max(mu2 - w * w, 1e-12))
    beta = kapp + 1.0 / R
    x = np.linspace(0, R, 2000)
    finit = np.interp(x, init_f[0], init_f[1])
    dfinit = np.gradient(finit, x)
    y0 = np.vstack([x * finit, finit + x * dfinit])

    def fun(xx, y):
        s, ds = y
        r = xx
        f = np.where(r > 1e-12, s / np.maximum(r, 1e-12), ds)
        rhs = (mu2 - w * w) * f - 2.0 * lam * f**3 + 3.0 * g6 * f**5
        return [ds, r * rhs]

    def bc(ya, yb):
        sR, dsR = yb
        fR = sR / R
        return [ya[0], (dsR * R - sR) / (R * R) + beta * fR]

    sol = solve_bvp(fun, bc, x, y0, tol=1e-8, max_nodes=30000)
    if not sol.success:
        return None, None, None
    xr = sol.x
    s, ds = sol.y
    f = np.where(xr > 1e-12, s / np.maximum(xr, 1e-12), ds)
    QN = 8.0 * np.pi * w * np.trapezoid(f**2 * xr**2, xr)
    return float(ds[0]), float(QN), (xr, f)


if __name__ == "__main__":
    points = {}
    prev = (r0, f0n)
    for w in [0.95, 0.955, 0.96, 0.965, 0.97, 0.975, 0.98, 0.985, 0.99, 0.993, 0.995, 0.997]:
        f0, QN, prf = solve_neutral(w, prev)
        if QN is None:
            print("w=%.4f 未收敛(向上)" % w); break
        points[w] = {"f0": f0, "QN": QN}; prev = prf
    prev = (r0, f0n)
    for w in [0.94, 0.93, 0.92, 0.91, 0.905, 0.90]:
        f0, QN, prf = solve_neutral(w, prev)
        if QN is None:
            print("w=%.4f 未收敛(向下)" % w); break
        points[w] = {"f0": f0, "QN": QN}; prev = prf
    ws = sorted(points.keys())
    qs = [points[w]["QN"] for w in ws]
    for i in range(1, len(ws)):
        dw = ws[i] - ws[i-1]
        if dw > 0:
            points[ws[i-1]]["dQdw"] = float((qs[i] - qs[i-1]) / dw)
    scan = [{"w": w, "f0": p["f0"], "QN": p["QN"], "dQdw": p.get("dQdw")}
            for w, p in sorted(points.items())]
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"potential": "s-s^2+s^3", "mu2": mu2, "lam": lam, "g6": g6,
                   "R": R, "scan": scan}, fh, ensure_ascii=False, indent=2)
    for s in scan:
        if s["dQdw"] is not None:
            print("w=%.3f Q_N=%9.1f dQ/dw=%+.0f -> %s"
                  % (s["w"], s["QN"], s["dQdw"], "稳定" if s["dQdw"] < 0 else "不稳定"))
    print("已保存:", OUT)
