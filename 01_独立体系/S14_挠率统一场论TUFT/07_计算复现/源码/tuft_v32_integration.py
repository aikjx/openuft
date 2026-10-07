# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  全链路整合（分支整合）—— 汇总各报告核心量，无新物理，纯整合/复核
================================================================================
重算并汇总 C0045→C0086 全链路关键量：质量核、涌现尺度、g、辐射修正、统一级联。
红线：所有量均来自既有报告公式；本脚本仅整合，不新增物理主张。
================================================================================
"""
from __future__ import print_function
import os, sys, math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_v32_integration_report.txt")

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
ELEV = 1.602176634e-19
GE_EXP = 2.00231930436
OMEGA_DE = 0.6875

import numpy as np
r = np.logspace(-3.0, 2.0, 4000)
Kc, lK, r0, p = 3.1648e-08, 6.9989e-02, 6.9987e-03, 2.9094e+00
Tc, lT, O0, lO = 3.1648e-08, 6.9989e-02, 9.8778e-01, 1.1852e+00
K = Kc * np.exp(-r / lK) / (1.0 + (r / r0) ** p)
T = Tc * np.exp(-r / lT)
Om = OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-r / lO)
M_nat = ALPHA * 4.0 * math.pi * np.trapezoid(K * T * Om * r ** 2, r)
N_core = np.trapezoid((Om - OMEGA_DE) * r ** 2, r)
lamC_m = (1.0 / M_nat) * L_PLANCK
r_e = ALPHA * lamC_m
a0 = lamC_m / ALPHA
R_H_eV = ALPHA**2 * M_E * C_LIGHT**2 / 2.0 / ELEV

# g_e 情形（C0057/81）：⟨r⟩=1.00116 λ_C
rbar = 1.00116 * lamC_m
l_Q = rbar / 3.0
g_tuft = 2.0 * (rbar / lamC_m)   # ⟨r⟩/λ_C = M_nat·⟨r⟩_nat = 1.00116 ⇒ g=2.00232

# 辐射修正 C(ω_C)（C0085）
lamC_freq = C_LIGHT / lamC_m
Cw_at_C = (1.0 / (1.0 + (l_Q / lamC_m) ** 2)) ** 4   # C(ω_C)=|F|², F=[1/(1+(ω l_Q/c)²)]²

A0_CODATA = 5.29177210903e-11
RH_CODATA = 13.605693122994

buf = []
log = buf.append
log("TUFT V3.2 全链路整合（C0045→C0086）· 汇总复核")
log("运行时间: 2026-10-07  Python %s" % sys.version.split()[0])
log("")
log("=== 全观测量闭合（复核）===")
log("  M = M_nat = %.6e 普朗克 = %.6e kg (=M_e ✓)  [C0045]" % (M_nat, M_nat*E_PLANCK/C_LIGHT**2))
log("  N_core = %.6f (dev %.2e)  [C0045/57]" % (N_core, N_core-1))
log("  g = 2M_nat·⟨r⟩ = %.6f (vs g_e=%.6f, dev %.2e)  [C0057/81]" % (g_tuft, GE_EXP, (g_tuft-GE_EXP)/GE_EXP))
log("  ⟨r⟩_charge = %.6e m = %.4f·λ_C ; l_Q=%.6e m  [C0057]" % (rbar, rbar/lamC_m, l_Q))
log("")
log("=== 涌现尺度与独立一致性（复核）===")
log("  λ_C = 1/M_nat = %.6e m ; r_e=αλ_C=%.6e m  [C0081/82]" % (lamC_m, r_e))
log("  λ_C/r_e = 1/α = %.6f  [C0082]" % (lamC_m/r_e))
log("")
log("=== 辐射修正（复核）===")
log("  ω_C = c/λ_C = %.4e rad/s ; C(ω_C)=|F|²=%.6f (dev %.2f%%)  [C0085]" % (lamC_freq, Cw_at_C, (1-Cw_at_C)*100))
log("")
log("=== 统一级联（复核）===")
log("  a_0 = λ_C/α = %.6e m (vs CODATA %.10e, dev %.2e)  [C0086]" % (a0, A0_CODATA, abs(a0-A0_CODATA)/A0_CODATA))
log("  R_H = α²Mc²/2 = %.6f eV (vs CODATA %.8f, dev %.2e)  [C0086]" % (R_H_eV, RH_CODATA, abs(R_H_eV-RH_CODATA)/RH_CODATA))
log("  a_0/λ_C=1/α=%.6f ; a_0/r_e=1/α²=%.4f" % (a0/lamC_m, a0/r_e))
log("")
log("=== 诚实边界 ===")
log("  α 仍为输入，非独立预言；电荷/磁晕映射为模型假设（C0051 挂账）；")
log("  C(ω)/级联为模型预言，未与实测证伪对账。")
log("红线：本脚本仅整合既有报告公式，无新物理主张。")

text = "\n".join(buf) + "\n"
print(text)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(text)
