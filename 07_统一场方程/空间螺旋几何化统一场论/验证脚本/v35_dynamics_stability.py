#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 动力学线性稳定性谱（中性固定荷 Q-ball）
================================================================
对象：09 稿中性全局 U(1) 球对称六次势候选背景。
      U(s)=s-s^2+s^3, w^2=0.9, psi=e^{-iwt}f(r), f(0)~0.722694
      (剖面取自上级目录 V3_Qball_profile.csv, R=80 高精度)。
方法：耦合一阶扰动系统 (09稿 §2, u,v 实数分量)
      (L+ - Omega^2)u - 2iw Omega v = 0
      2iw Omega u + (L- - Omega^2)v = 0
      L+ = -Delta+1-w^2-6f^2+15f^4,  L- = -Delta+1-w^2-2f^2+3f^4
      线性化 A_lin = [[0,I2],[M,2iwJ]], M=blkdiag(L+,L-), J=[[0n,In],[-In,0n]]
      对 w=ru 作 1D 三对角（Dirichlet w(0)=w(R)=0），稠密全谱。
约定：|delta| ~ e^{Im(Omega) t}；增长模 Im(Omega)>0 即线性不稳定候选。
判据：所有通道无真正的 Im(Omega)>0 模 => 线性稳定候选。
边界：仅中性背景 ℓ=0,1,2 通道；带电规范零模、参数扫描、非线性稳定性未覆盖。
用法： python v35_dynamics_stability.py
"""
import os
import json
import numpy as np
import scipy.sparse as sp
from scipy.linalg import eig

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
CSV = os.path.join(PARENT, "V3_Qball_profile.csv")
OUT = os.path.join(PARENT, "V3_5_dynamics_spectrum.json")

w2 = 0.9
w = np.sqrt(w2)

with open(CSV, "r", encoding="utf-8") as fh:
    next(fh)
    rr, ff = [], []
    for line in fh:
        a, b, c = line.strip().split(",")
        rr.append(float(a)); ff.append(float(b))
r0 = np.array(rr); f0 = np.array(ff)


def spec(n, l, Rout):
    rmid = np.linspace(0, Rout, n + 1)[1:]
    fmid = np.interp(rmid, r0, f0)
    h = Rout / n
    h2 = h * h
    rmid_safe = np.maximum(rmid, 1e-9)
    cent = l * (l + 1.0) / rmid_safe**2
    Vp = 1.0 - w2 - 6.0 * fmid**2 + 15.0 * fmid**4 + cent
    Vm = 1.0 - w2 - 2.0 * fmid**2 + 3.0 * fmid**4 + cent

    def lap(V):
        diag = 2.0 / h2 + V
        off = -np.ones(len(V) - 1) / h2
        return sp.diags([off, diag, off], [-1, 0, 1], format="csc")

    Lp, Lm = lap(Vp), lap(Vm)
    In = sp.identity(n, format="csc"); Z = sp.csc_matrix((n, n))
    I2 = sp.identity(2 * n, format="csc"); Z2 = sp.csc_matrix((2 * n, 2 * n))
    M = sp.block_diag([Lp, Lm], format="csc")
    Jblk = sp.bmat([[Z, In], [-In, Z]], format="csc")
    G = 2j * w * Jblk
    A = sp.bmat([[Z2, I2], [M, G]], format="csc").toarray()
    return np.asarray(eig(A, right=False)), h


if __name__ == "__main__":
    rec = {
        "w2": w2, "w": float(w),
        "background": "U(s)=s-s^2+s^3, psi=e^{-iwt}f(r), f(0)~0.722694, V3_Qball_profile.csv R=80",
        "formulation": "coupled A_lin z=Omega z, M=blkdiag(L+,L-), G=2iwJ; dense full spectrum",
        "convention": "delta ~ e^{-i Omega t}; growth = Im(Omega)>0; linear stable iff all Im<=0",
        "channels": {}, "l1_translation_error": [], "conclusion": None,
    }
    tol = 1e-6
    for l in [0, 1, 2]:
        om, h = spec(600, l, 60.0)
        gr = om[om.imag > tol]
        om0 = om[np.abs(om.imag) <= tol]
        omin = float(np.abs(om0).min()) if len(om0) else None
        rec["channels"][str(l)] = {
            "n": 600, "r_out": 60.0, "h": h,
            "im_max": float(om.imag.max()), "im_min": float(om.imag.min()),
            "n_growth_modes_Im_gt_1e6": int(len(gr)),
            "growth_ReIm": [[float(x.real), float(x.imag)] for x in gr[:5]],
            "zero_mode_absmin": omin, "spec_size": int(len(om)),
        }
        print("l=%d: im_max=%.3e growth=%d zero|Om|min=%s"
              % (l, om.imag.max(), len(gr), omin))
    for n in [400, 600, 800]:
        om, h = spec(n, 1, 60.0)
        gr = om[om.imag > 1e-6]
        rec["l1_translation_error"].append(
            {"n": n, "h": h, "Re": float(gr[0].real) if len(gr) else None,
             "Im": float(gr[0].imag) if len(gr) else None})
    print("l1 translation error:", rec["l1_translation_error"])

    any_phys = any(
        rec["channels"][l]["n_growth_modes_Im_gt_1e6"] > 0
        and rec["channels"][l]["growth_ReIm"]
        and abs(rec["channels"][l]["growth_ReIm"][0][1]) > 5e-3
        for l in ["0", "1", "2"])
    rec["conclusion"] = "linear_stable_candidate" if not any_phys else "needs_careful_review"
    print("conclusion:", rec["conclusion"])
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=2)
    print("saved:", OUT)
