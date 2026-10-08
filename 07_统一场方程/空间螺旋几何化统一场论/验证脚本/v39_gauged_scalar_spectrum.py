#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.5 · 带电 Q-ball 标量扰动谱（含背景静电势 W=w-a 效应）
承接 20 稿中性谱方法 + 38 稿带电背景。对象：带电 U(1) Q-ball（e=0.05）背景 f(r),a(r)。
方法：复标量扰动分解 u,v 实数分量，w→W(r)=w-a(r)（背景静电势）：
  (L+ - Omega^2)u - 2i W(r) Omega v = 0
  2i W(r) Omega u + (L- - Omega^2)v = 0
  L+ = -Δ+1-W(r)^2-6f^2+15f^4+cent,  L- = -Δ+1-W(r)^2-2f^2+3f^4+cent
  A_lin = [[0,I],[M,2i W J]] 本征值 Ω；增长模 Im(Ω)>0 => 线性不稳定候选。
边界：本谱为带电标量扰动主体（W 效应），未含 δA 反馈耦合（完整 6 分量谱缺口）；横模正定见 21 稿。
铁律：本谱是带电标量扰动充分判据的一部分，完整 δA 耦合另需补。
"""
import os
import json
import numpy as np
import scipy.sparse as sp
from scipy.linalg import eig

PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NPZ = os.path.join(PARENT, "V3_gauged_background_e005.npz")
OUT = os.path.join(PARENT, "V3_5_gauged_scalar_spectrum.json")
w = 0.960271793738176
e = 0.05


def spec(n, l, Rout, r_bg, f_bg, a_bg):
    rmid = np.linspace(0, Rout, n + 1)[1:]
    fmid = np.interp(rmid, r_bg, f_bg)
    amid = np.interp(rmid, r_bg, a_bg)
    W = w - amid
    h = Rout / n
    h2 = h * h
    rmid_safe = np.maximum(rmid, 1e-9)
    cent = l * (l + 1.0) / rmid_safe**2
    W2 = W**2
    Vp = 1.0 - W2 - 6.0 * fmid**2 + 15.0 * fmid**4 + cent
    Vm = 1.0 - W2 - 2.0 * fmid**2 + 3.0 * fmid**4 + cent

    def lap(V):
        diag = 2.0 / h2 + V
        off = -np.ones(len(V) - 1) / h2
        return sp.diags([off, diag, off], [-1, 0, 1], format="csc")

    Lp, Lm = lap(Vp), lap(Vm)
    In = sp.identity(n, format="csc"); Z = sp.csc_matrix((n, n))
    I2 = sp.identity(2 * n, format="csc"); Z2 = sp.csc_matrix((2 * n, 2 * n))
    M = sp.block_diag([Lp, Lm], format="csc")
    Jblk = sp.bmat([[Z, In], [-In, Z]], format="csc")
    W2blk = sp.block_diag([sp.diags(W, format="csc"), sp.diags(W, format="csc")], format="csc")
    G = 2j * W2blk * Jblk  # 2i W(r) J
    A = sp.bmat([[Z2, I2], [M, G]], format="csc").toarray()
    return np.asarray(eig(A, right=False)), h


if __name__ == "__main__":
    z = np.load(NPZ)
    r_bg, f_bg, a_bg = z["r"], z["f"], z["a"]
    R_bg = r_bg[-1]
    print("带电背景: R=%.0f f(0)=%.6f a(0)=%.6f" % (R_bg, f_bg[0], a_bg[0]))
    rec = {
        "background": "V3_gauged_background_e005.npz (e=0.05,Q_N=279.16,w=0.96027)",
        "formulation": "charged scalar perturbation, w->W(r)=w-a(r); A_lin=[[0,I],[M,2i W J]]",
        "convention": "delta ~ e^{-i Omega t}; growth = Im(Omega)>0 => linear unstable",
        "gauge": "横模 decouple 见 21 稿；本谱为标量扰动主体（W 效应），未含 δA 反馈耦合",
        "channels": {}, "conclusion": None,
    }
    tol = 1e-6
    any_phys = False
    for l in [0, 1, 2]:
        om, h = spec(600, l, min(R_bg, 60.0), r_bg, f_bg, a_bg)
        gr = om[om.imag > tol]
        om0 = om[np.abs(om.imag) <= tol]
        omin = float(np.abs(om0).min()) if len(om0) else None
        ngr = int(len(gr))
        # 物理增长：排除数值尾部（小 Im）
        real_growth = [g for g in gr if abs(g.imag) > 5e-3]
        if real_growth:
            any_phys = True
        rec["channels"][str(l)] = {
            "n": 600, "r_out": min(R_bg, 60.0), "h": h,
            "im_max": float(om.imag.max()), "n_growth_Im_gt_1e6": ngr,
            "growth_ReIm": [[float(x.real), float(x.imag)] for x in gr[:5]],
            "real_growth_Im_gt_5e3": [[float(x.real), float(x.imag)] for x in real_growth[:5]],
            "zero_mode_absmin": omin,
        }
        print("l=%d: im_max=%.3e growth(>1e-6)=%d real_growth(>5e-3)=%d zero|Om|min=%s"
              % (l, om.imag.max(), ngr, len(real_growth), omin))
    rec["conclusion"] = "linear_stable_candidate" if not any_phys else "needs_careful_review"
    print("conclusion:", rec["conclusion"])
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=2)
    print("saved:", OUT)
