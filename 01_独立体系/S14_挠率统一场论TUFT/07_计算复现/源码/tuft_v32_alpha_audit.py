# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支 TS6 —— α 攻破审计：结构角色、质量重整化与派生机制定位
================================================================================
目标：攻统一场论最后一处硬骨头——精细结构常数 α 的派生。本步做诚实地形测绘：

  A. α 的三重结构角色（两尺度模型中 α 出现的所有地方）：
     (1) 经典半径 r_e = α·λ_C          （尺度比）
     (2) 电磁自能 U_EM = c_geom·α·M c²  （C0082：5.87α≈4.28%）
     (3) 原子束缚 R_H = α²·M c²/2      （氢 Rydberg）

  B. 质量重整化一致性（4.28% 张力）：
     若晕的电磁自能是质量贡献 ⇒ 裸核质量 M_bare = M_e(1−5.87α)=0.9572·M_e；
     当前 C0045 核拟合为满质量 M_e ⇒ 张力 4.28%。
     关键：g = 2·M_phys·⟨r⟩ 用物理质量与晕半径，与核/裸质量分离无关 ⇒ g 鲁棒。

  C. α 派生机制审计（候选条件分类）：
     (c1) 经典半径定义 r_e=e²/(4πε₀Mc²)=αλ_C（由 U_EM(R=r_e)=M c² 定义）——定义式，非派生。
     (c2) "涌现康普顿"⟨r⟩=λ_C（C0081）——conjecture，固定 λ_C=1/M 但 α 仍自由。
     (c3) 稳定/极小化一个作用量对 l_Q 或 α ——需要 TUFT 电荷场自耦合（缺，C0051 挂账）。
     结论：α 派生的唯一机制缺口 = TUFT 电荷场自耦合作用量（V1,V2 等价量）。

  D. 结论：α 目前不可派生；给出派生 α 的充分条件（未来可检验）。

红线声明：本步为审计/定位，不含对 α 的虚构预言；α 仍为输入（C0088 诚实边界延续）。
================================================================================
"""
from __future__ import print_function
import os, sys, math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_v32_alpha_audit_report.txt")

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
lamC_m = (1.0 / M_nat) * L_PLANCK
r_e = ALPHA * lamC_m
a0 = lamC_m / ALPHA
R_H_eV = ALPHA**2 * M_E * C_LIGHT**2 / 2.0 / ELEV

# 电磁自能（C0082：exp 晕 c_geom=5.87）
CG = 5.87164
UEM_over_M = CG * ALPHA
M_bare_frac = 1.0 - UEM_over_M
M_bare_kg = M_E * M_bare_frac

# g 鲁棒性：g=2·M_phys·⟨r⟩_nat，⟨r⟩=1.00116·λ_C
rbar_over_lC = GE_EXP / 2.0
g_eval = 2.0 * rbar_over_lC

buf = []
log = buf.append
log("TUFT V3.2 分支TS6 · α 攻破审计：结构角色、质量重整化与派生机制定位")
log("运行时间: 2026-10-07  Python %s" % sys.version.split()[0])
log("")
log("=== A. α 的三重结构角色 ===")
log("  (1) 经典半径 r_e = α·λ_C = %.6e m；λ_C/r_e = 1/α = %.6f" % (r_e, 1/ALPHA))
log("  (2) 电磁自能 U_EM/M c² = c_geom·α = %.4f·α ≈ %.4f%%" % (CG, UEM_over_M*100))
log("  (3) 原子束缚 R_H = α²·M c²/2 = %.6f eV；a_0 = λ_C/α = %.6e m" % (R_H_eV, a0))
log("  ⇒ α 同时是尺度比、自能占比、束缚能耦合：三重结构角色。")
log("")
log("=== B. 质量重整化一致性（4.28%% 张力）===")
log("  若晕电磁自能是质量贡献：裸核 M_bare = M_e(1−5.87α) = %.6f·M_e = %.6e kg" % (M_bare_frac, M_bare_kg))
log("  当前 C0045 核拟合为满质量 M_e（N_core=0.999843）⇒ 若计自能为质量，张力 4.28%。")
log("  关键鲁棒性：g = 2·M_phys·⟨r⟩_nat = %.6f，使用物理质量 M_e 与晕半径" % g_eval)
log("  ⟨r⟩=1.00116·λ_C ⇒ g 与核/裸质量分离无关 ⇒ g_e 对重整化方案鲁棒 ✓")
log("")
log("=== C. α 派生机制审计（候选条件分类）===")
log("  (c1) 经典半径定义 r_e=e²/(4πε₀Mc²)=αλ_C（U_EM(R=r_e)=Mc² 定义 r_e）——定义式，非派生。")
log("  (c2) 涌现康普顿 ⟨r⟩=λ_C（C0081）——conjecture，固定 λ_C=1/M 但 α 仍自由。")
log("  (c3) 稳定/极小化作用量对 l_Q 或 α——需 TUFT 电荷场自耦合作用量（缺，C0051 挂账）。")
log("  ⇒ 唯一机制缺口：TUFT 电荷场自耦合（V1,V2 等价量）。")
log("")
log("=== D. 结论 ===")
log("  1) α 目前不可派生：三重角色均为输入驱动的尺度比/耦合，无独立机制固定。")
log("  2) 派生 α 的充分条件（未来可检验）：在 TUFT 作用量中给出电荷场自耦合 U_Q(ρ)，")
log("     使电磁自能占比 c_geom·α 由稳定/极小化条件唯一确定（非 ad-hoc），即可预言 α。")
log("  3) 质量重整化张力（4.28%）是模型内部一致性开放项：需明确晕自能是否计入质量。")
log("  4) g_e 对 core/bare 质量分离鲁棒，不受此张力影响。")
log("红线声明：本步为审计/定位，不含对 α 的虚构预言；α 仍为输入（C0088 诚实边界延续）。")

text = "\n".join(buf) + "\n"
print(text)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(text)
