# -*- coding: utf-8 -*-
"""
_ma_v59_v50_sens.py — v50 TUFT 频裂敏感度核查
1) 静态 pole 对 N 收敛（60/90/120）-> 判断 2.35e-6 偏差是网格还是系统
2) 0.04 barrier 手动参数敏感度：barrier=0 vs 0.04 的 split/a
复用 tuft_v50_tuft_spin_splitting 模块函数（import 不触发 main）。
"""
import math
import numpy as np
from scipy.linalg import eig
from tuft_v50_tuft_spin_splitting import (
    cm_t, d_t, BETA, RHO_H, tuft_pencil, rho_vs_t, fit_U, frob_a, V_of, cheb_gauss
)

b_t = complex(4.0, 0.5)
b_fit = 4.0
sol_fit = rho_vs_t(b_fit, 8.0)
Ud = fit_U(sol_fit, b_fit)
a12 = frob_a(Ud, 12)
GRADE_A = 0.434445178 - 0.056449760j

print("== [1] static TUFT pole vs N (convergence toward Grade-A ref) ==")
for N in (60, 90, 120):
    Q0s, Q1s, rho = tuft_pencil(N, b_t, a12[:5])
    evr = eig(-Q0s, Q1s, right=False); evr = evr[np.isfinite(evr)]
    k = int(np.argmin(np.abs(evr - 0.43445 + 0.05645j)))
    w0 = evr[k]
    d = abs(w0 - GRADE_A)
    print("  N=%3d  pole=%.9f%+.9fi  |d vs Grade-A|=%.3e (%.1f digits)" % (N, w0.real, w0.imag, d, -math.log10(d)))

print("")
print("== [2] barrier sensitivity: split/a with 0.04*barrier vs 0 ==")
def split_for_barrier(amp):
    Q0s, Q1s, rho = tuft_pencil(60, b_t, a12[:5])
    evr, lvec, rvec = eig(-Q0s, Q1s, left=True, right=True)
    k = int(np.argmin(np.abs(evr - 0.43445 + 0.05645j)))
    w0 = evr[k]
    v = rvec[:, k]; v = v/np.linalg.norm(v)
    u = lvec[:, k]; u = u/np.linalg.norm(u)
    den = u.conj()@Q1s@v
    A_lapse = np.exp(-2.0/rho)
    barrier = np.exp(-0.5*((rho-1.8)/0.7)**2)
    OmF = (2.0/rho**3)*A_lapse*(1.0 + amp*barrier)
    num = u.conj()@np.diag(OmF)@v
    c = complex(2.0*w0*num/den)
    return 4.0*c.real

for amp in (0.0, 0.04, 0.10):
    print("  barrier amp=%5.2f : split/a = %.6f" % (amp, split_for_barrier(amp)))

print("")
print("== [3] GR 2R^-3 band (no lapse) sanity ==")
def split_gr():
    Q0s, Q1s, rho = tuft_pencil(60, b_t, a12[:5])
    evr, lvec, rvec = eig(-Q0s, Q1s, left=True, right=True)
    k = int(np.argmin(np.abs(evr - 0.43445 + 0.05645j)))
    w0 = evr[k]
    v = rvec[:, k]; v = v/np.linalg.norm(v)
    u = lvec[:, k]; u = u/np.linalg.norm(u)
    den = u.conj()@Q1s@v
    OmF = 2.0/rho**3
    num = u.conj()@np.diag(OmF)@v
    c = complex(2.0*w0*num/den)
    return 4.0*c.real
print("  GR 2R^-3 band : split/a = %.6f (expect ~2.337)" % split_gr())
