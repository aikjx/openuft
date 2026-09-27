#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.5 · dQ/dw 判据 vs A_lin 动力学谱一致性复核
对 (w, Q_N) 扫描分支上的代表性 w 点解背景 + A_lin(4n) 稠密全谱。
预期：w 稳定区(dQ/dw<0) 无增长模；w 不稳定区(dQ/dw>0) 有增长模。
用法： python v35_scan_recheck.py
"""
import os
import json
import numpy as np
import scipy.sparse as sp
from scipy.integrate import solve_bvp
from scipy.linalg import eig

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
CSV = os.path.join(PARENT, "V3_Qball_profile.csv")
OUT = os.path.join(PARENT, "V3_5_scan_recheck.json")
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
        return None
    xr = sol.x
    s, ds = sol.y
    f = np.where(xr > 1e-12, s / np.maximum(xr, 1e-12), ds)
    return (xr, f)


def alin(w, f_r, n=400, Rout=80.0):
    xr, f = f_r
    xmid = np.linspace(0, Rout, n + 1)[1:]
    h = Rout / n
    fmid = np.interp(xmid, xr, f)
    Vp = 1.0 - w*w - 6.0*fmid**2 + 15.0*fmid**4
    Vm = 1.0 - w*w - 2.0*fmid**2 + 3.0*fmid**4
    def lap(V):
        return sp.diags([-np.ones(n-1)/h**2, 2.0/h**2+V, -np.ones(n-1)/h**2],
                        [-1, 0, 1], format="csc")
    Lp, Lm = lap(Vp), lap(Vm)
    In = sp.identity(n, format="csc"); Z = sp.csc_matrix((n, n))
    I2 = sp.identity(2*n, format="csc"); Z2 = sp.csc_matrix((2*n, 2*n))
    M = sp.block_diag([Lp, Lm], format="csc")
    Jblk = sp.bmat([[Z, In], [-In, Z]], format="csc")
    G = 2j*w*Jblk
    A = sp.bmat([[Z2, I2], [M, G]], format="csc").toarray()
    return np.asarray(eig(A, right=False))


if __name__ == "__main__":
    tol = 1e-6
    rec = {"potential": "s-s^2+s^3", "recheck": [], "conclusion": None}
    for w, dQdw in [(0.96, -3912.0), (0.985, 2227.0), (0.99, 5982.0)]:
        prf = solve_neutral(w, (r0, f0n))
        if prf is None:
            print("w=%.3f 背景未收敛" % w)
            continue
        om = alin(w, prf)
        growth = om[om.imag > tol]
        entry = {"w": w, "dQdw_scan": dQdw,
                 "n_growth_modes": int(len(growth)),
                 "max_Im": float(om.imag.max()),
                 "growth_ReIm": [[float(x.real), float(x.imag)] for x in growth]}
        rec["recheck"].append(entry)
        print("w=%.3f dQ/dw=%+.0f 增长模=%d 最大Im=%.3e"
              % (w, dQdw, len(growth), om.imag.max()))
    # 一致性：dQ/dw<0 -> 无增长；dQ/dw>0 -> 有增长
    consistent = all(
        (e["dQdw_scan"] < 0) == (e["n_growth_modes"] == 0)
        for e in rec["recheck"])
    rec["conclusion"] = "consistent: dQ/dw<0 无增长模, dQ/dw>0 有增长模" if consistent else "inconsistent"
    print("一致性:", consistent)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=2)
    print("已保存:", OUT)
