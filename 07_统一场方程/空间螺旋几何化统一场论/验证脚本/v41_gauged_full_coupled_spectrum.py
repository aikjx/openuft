#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
v41：带电 Q-ball 完整标量-δA0 耦合谱（含 Gauss 约束消去的 δA0 反馈）
承接 39 稿（无 δA0 反馈的标量谱，ℓ=1 增长模 Im≈1.76e-2）+ 40 稿（平移不变性论证该模为伪影）。
本脚本加入 δA0 反馈，数值裁决增长模是否被恢复为 Ω=0 平移零模。
推导（库仑规范，δA 横向 decouple 见 21 稿）：
  标量扰动 δφ=e^{iwt}(u+iv)e^{-iΩt}，背景 W=w-a。
  (L+ - Ω^2)u - 2W Ω v + 2eWf α = 0
  2W Ω u + (L- - Ω^2)v = 0
  Gauss: (∇^2_l - 2e^2f^2)α = -2eWfv  =>  α = -B^{-1}(2eWfv), B=∇^2_l - 2e^2f^2
  代入 => M 的 (1,2) 块 += -4e^2W^2f^2 B^{-1}
  A_lin=[[0,I],[M,2iW J]]，本征值 Ω；增长模 Im(Ω)>0。
"""
import os, json
import numpy as np
import scipy.sparse as sp
from scipy.linalg import eig

PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
z = np.load(os.path.join(PARENT, "V3_gauged_background_e005.npz"))
r_bg, f_bg = z["r"], z["f"]
w = 0.960271793738176
e = 0.05


def spec(n, l, Rout, with_feedback):
    rmid = np.linspace(0, Rout, n + 1)[1:]
    fmid = np.interp(rmid, r_bg, f_bg)
    W = w - np.interp(rmid, r_bg, z["a"])
    h = Rout / n; h2 = h*h
    cent = l*(l+1)/np.maximum(rmid,1e-9)**2
    W2 = W**2
    Vp = 1-W2-6*fmid**2+15*fmid**4+cent
    Vm = 1-W2-2*fmid**2+3*fmid**4+cent
    def lap(V):
        return sp.diags([-np.ones(len(V)-1)/h2, 2/h2+V, -np.ones(len(V)-1)/h2],[-1,0,1],format="csc")
    Lp, Lm = lap(Vp), lap(Vm)
    Lp = Lp.toarray(); Lm = Lm.toarray()
    if with_feedback:
        # Gauss: (∇^2_l - 2e^2f^2)α = -2eWfv; ∇^2_l = d^2/dr^2 - l(l+1)/r^2
        B = lap(-cent - 2*e*e*fmid**2).toarray()   # = ∇^2_l - 2e^2f^2 (centrifugal included)
        B_inv = np.linalg.inv(B)
        cross = -4*e*e*W2*fmid**2 * B_inv     # -4e^2W^2f^2 B^{-1} 作用于 v -> u
    else:
        cross = np.zeros((n, n))
    M = np.block([[Lp, cross], [np.zeros((n, n)), Lm]])
    In = sp.identity(n); Z = sp.csc_matrix((n, n))
    Jblk = np.block([[Z.toarray(), In.toarray()], [-In.toarray(), Z.toarray()]])
    Wb = np.block([[np.diag(W), np.zeros((n, n))], [np.zeros((n, n)), np.diag(W)]])
    G = 2j * Wb @ Jblk
    A = np.block([[np.zeros((2*n, 2*n)), np.eye(2*n)], [M, G]])
    return np.asarray(eig(A, right=False))


if __name__ == "__main__":
    rec = {"background": "V3_gauged_background_e005.npz (e=0.05,Q_N=279.16,w=0.96027)",
           "method": "charged scalar + deltaA0 (Gauss-eliminated) coupled spectrum; A_lin=[[0,I],[M,2iWJ]]",
           "convention": "delta ~ e^{-i Omega t}; growth = Im(Omega)>0 => linear unstable"}
    for fb, tag in [(False, "no_dA0_feedback(reproduce_39)"), (True, "with_dA0_feedback")]:
        channels = {}
        for l in [0, 1, 2]:
            om = spec(300, l, 60.0, fb)
            gr = om[om.imag > 5e-3]
            om0 = om[np.abs(om.imag) <= 5e-3]
            omin = float(np.abs(om0).min()) if len(om0) else None
            channels[str(l)] = {
                "im_max": float(om.imag.max()),
                "growth_ReIm": [[float(x.real), float(x.imag)] for x in gr[:5]],
                "n_growth": int(len(gr)),
                "zero_absmin": omin,
            }
            print("[%s] l=%d im_max=%.3e growth=%d zero_min=%s"
                  % (tag, l, om.imag.max(), len(gr), omin))
        rec[tag] = channels
    with open(os.path.join(PARENT, "V3_5_gauged_full_coupled_spectrum.json"), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=2)
    print("saved V3_5_gauged_full_coupled_spectrum.json")
