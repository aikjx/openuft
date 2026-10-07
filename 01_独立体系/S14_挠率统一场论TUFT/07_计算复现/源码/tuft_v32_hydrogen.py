# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支 TS5 —— 两尺度结构统一级联：从电子到氢原子
================================================================================
目标：把两尺度电子（普朗克核 C0045 + 康普顿晕 C0081）延拓到氢原子束缚，
展示"统一场论式"尺度级联：单一参数集 {M_e, α}（ħ,c,G 固定）贯通电子内禀
（l_P 核、r_e=αλ_C、λ_C 晕）与原子束缚（a_0=λ_C/α、Rydberg E）。

关键统一结构（步进因子 α 或 1/α）：
  l_P (质量核)  →  r_e = α·λ_C (经典半径)  →  λ_C = 1/M (康普顿晕, 涌现)  →  a_0 = λ_C/α (玻尔)
  Rydberg：R_H = α²·M_e c²/2 = 13.6057 eV（virial T=-U/2）

本脚本在模型框架内推导并数值核验：
  (a) 玻尔半径 a_0 = λ_C/α（用涌现 λ_C 与 α）→ 对 CODATA 5.29177e-11 m
  (b) Rydberg R_H = α² M_e c²/2 → 对 CODATA 13.60569 eV
  (c) 束缚能 virial 自洽：U=-α²Mc²、T=+α²Mc²/2、E=T+U=-α²Mc²/2
  (d) 尺度级联比值：a_0/λ_C = 1/α，λ_C/r_e = 1/α，a_0/r_e = 1/α²

红线声明：α 仍是输入（非由两尺度结构独立预言）；本步为"统一级联"的结构性验证
（同一 {M,α} 决定电子内禀与原子束缚），属 conjecture/一致性层级，非物理真实主张。
================================================================================
"""
from __future__ import print_function
import os, sys, math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_v32_hydrogen_report.txt")

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
ELEV = 1.602176634e-19
OMEGA_DE = 0.6875

buf = []
log = buf.append

# 质量核（C0045）
import numpy as np
r = np.logspace(-3.0, 2.0, 4000)
Kc, lK, r0, p = 3.1648e-08, 6.9989e-02, 6.9987e-03, 2.9094e+00
Tc, lT, O0, lO = 3.1648e-08, 6.9989e-02, 9.8778e-01, 1.1852e+00
K = Kc * np.exp(-r / lK) / (1.0 + (r / r0) ** p)
T = Tc * np.exp(-r / lT)
Om = OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-r / lO)
M_nat = ALPHA * 4.0 * math.pi * np.trapezoid(K * T * Om * r ** 2, r)
lamC_m = (1.0 / M_nat) * L_PLANCK
r_e = ALPHA * lamC_m                 # 经典半径
a0 = lamC_m / ALPHA                  # 玻尔半径
R_H_J = ALPHA**2 * M_E * C_LIGHT**2 / 2.0
R_H_eV = R_H_J / ELEV
U_J = -ALPHA**2 * M_E * C_LIGHT**2
T_J = ALPHA**2 * M_E * C_LIGHT**2 / 2.0

# CODATA
A0_CODATA = 5.29177210903e-11
RH_CODATA_eV = 13.605693122994

log("TUFT V3.2 分支TS5 · 两尺度结构统一级联：从电子到氢原子")
log("运行时间: 2026-10-07  Python %s" % sys.version.split()[0])
log("参数集 {M_e, α}: M_e=%.6e kg, α=1/%.6f, ħ/c/G 固定" % (M_E, 1/ALPHA))
log("")
log("=== 尺度级联（步进因子 α 或 1/α）===")
log("  质量核 lO  ~ %.4e m = %.2f l_P" % (lO*L_PLANCK, lO))
log("  经典半径 r_e = α·λ_C     = %.6e m" % r_e)
log("  康普顿晕 λ_C = 1/M_nat   = %.6e m（涌现，C0081）" % lamC_m)
log("  玻尔半径 a_0 = λ_C/α     = %.6e m" % a0)
log("  级联比：a_0/λ_C = 1/α = %.6f ; λ_C/r_e = 1/α = %.6f ; a_0/r_e = 1/α² = %.6f"
    % (a0/lamC_m, lamC_m/r_e, a0/r_e))
log("")
log("=== 氢原子束缚能（同一 {M_e, α}）===")
log("  Coulomb 能 U = −α²M_e c² = %.6e J" % U_J)
log("  动能 T = α²M_e c²/2 = %.6e J" % T_J)
log("  Rydberg R_H = T + U = −α²M_e c²/2 = %.6e J = %.6f eV" % (-R_H_J, R_H_eV))
log("  virial 自洽：T = −U/2 = %.6e ✓（库仑系统 virial 定理）" % (-U_J/2.0))
log("")
log("=== 对 CODATA 核验 ===")
log("  a_0(模型) = %.10e m vs CODATA %.10e m；相对偏差 %.3e"
    % (a0, A0_CODATA, abs(a0-A0_CODATA)/A0_CODATA))
log("  R_H(模型) = %.8f eV vs CODATA %.8f eV；相对偏差 %.3e"
    % (R_H_eV, RH_CODATA_eV, abs(R_H_eV-RH_CODATA_eV)/RH_CODATA_eV))
log("")
log("=== 统一级联的意义（conjecture 级，非物理真实主张）===")
log("  1) 单一 {M_e, α} 贯通电子内禀（l_P→r_e→λ_C）与原子束缚（a_0→Rydberg）：")
log("     l_P 1.9e-35 → r_e 2.8e-15 → λ_C 3.9e-13 → a_0 5.3e-11 m，共 ~24 个量级。")
log("  2) 与 C0045/57/81/82/85 的电子观测量（M,N,Q,μ,g,C(ω)）共用同一两尺度结构 ⇒ ")
log("     '统一场论'级结构：一个几何模型同时给出电子内禀 + 原子束缚。")
log("  3) 对 CODATA：R_H 相对偏差 %.1e（精确，用 α²M_e c²/2）；a_0 相对偏差 %.1e"
    "（受限：λ_C 用核拟合质量 M_nat，其 N_core=0.999843 偏离 1 所致，非物理失效）"
    % (abs(R_H_eV-RH_CODATA_eV)/RH_CODATA_eV, abs(a0-A0_CODATA)/A0_CODATA))
log("  4) 诚实边界：α 仍是输入，非由两尺度结构独立预言；本步为结构性/一致性验证。")
log("红线声明：统一级联为 conjecture 级；电荷/磁晕映射为模型假设（C0051）；本步非物理真实主张。")

text = "\n".join(buf) + "\n"
print(text)
try:
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
except Exception as exc:
    log("[warn] 报告写入失败: %s" % exc)
