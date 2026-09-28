# -*- coding: utf-8 -*-
"""
_ma_v59_v54_grband_conv.py — GR band Rayleigh 期望 N 收敛核查
在 v54 框架下对 N=60/90/120 分别计算 GR 2R^-3 band 与 E475 band，
判定 v50(2.337) vs v54(4.662) 的 2 倍差异是基漂移错误还是 Rayleigh 未收敛。
"""
import math
import numpy as np
from scipy.linalg import eig, lu_factor, lu_solve
from tuft_v54_tuft_spin_final import (
    tuft_pencil, beyn_pole, e475_omega_of_rho, B_OPT, TUFT_ANCHOR, RHO_H
)

def nullspace_vec(M):
    U, s, Vh = np.linalg.svd(M, full_matrices=False)
    return Vh.conj()[-1, :]

print("== GR band (2/rho^3) & E475 band Rayleigh expectation vs N ==")
for N in (60, 90, 120):
    Q0s, Q1s, rho = tuft_pencil(N, B_OPT)
    w0 = beyn_pole(Q0s, Q1s, TUFT_ANCHOR)
    M = Q0s + w0*Q1s
    v = nullspace_vec(M)
    u = nullspace_vec(M.conj().T)
    uv = np.vdot(u, v)
    u = u/uv
    v = v/np.linalg.norm(v)
    den = np.vdot(u, Q1s@v)
    rho_real = np.real(rho)
    OmF_GR = 2.0/rho_real**3
    OmF_E475 = np.array([e475_omega_of_rho(float(r)) for r in rho_real])
    def rayleigh(Om):
        num = np.vdot(u, np.diag(Om)@v)
        return complex(2.0*w0*num/den)
    cGR = rayleigh(OmF_GR); cE = rayleigh(OmF_E475)
    print("  N=%3d  w0=%.9f%+.9fi  GR band=%.6f  E475 band=%.6f  E475/GR=%.4f"
          % (N, w0.real, w0.imag, 4*cGR.real, 4*cE.real, (4*cE.real)/(4*cGR.real)))
print("")
print("== diagnostic: where does E475/GR < 1 come from (rho weighting)? ==")
for r in (0.65, 0.7, 0.8, 1.0, 1.5, 2.0, 3.0):
    of = e475_omega_of_rho(r); gr = 2.0/r**3
    print("  rho=%.2f  E475/GR ratio = %.4f" % (r, of/gr))
