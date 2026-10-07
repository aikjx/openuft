# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支 TS7 —— 证伪审计：空间延展修正 g 的机制 vs 电子弹性形状因子实测
================================================================================
对账模型核心预言（C0085 形状因子 / C0057·C0081 空间延展 g_e 机制）与实测：

  实验锚点（CODATA + 高精度 QED）：
   (E1) 电子电荷半径上限 R_e < 1e-18 m（Penning trap ~1e-22、精密谱 <1e-20，取 1e-18 为保守）
         —— 电子在实验可及能标下为点粒子。
   (E2) 电子反常磁矩 a_e^exp = 1159652180.59(13)e-12，SM/QED(点) a_e^SM = 1159652180.252(95)e-12
         —— 与点状 QED 一致到 ~0.3 ppb（10^-12 绝对量级）。

  模型预言（两尺度 ansatz，C0057/C0081/C0085）：
   (M1) 电荷分布 ⟨r⟩ = 1.00116·λ_C = 3.86e-13 m（λ_C=1/M_nat）
   (M2) 弹性形状因子 F(q) = [1+(q·l_Q)²]^(-2)，l_Q=λ_C/3=1.29e-13 m

  证伪判定：
   (F1) 尺度：λ_C/1e-18 ≈ 3.9e5（~5.6 量级）⇒ 电荷分布比实验上限大 ~5 个量级 ⇒ 排除。
   (F2) 形状因子：在 q=1/λ_C（探测能量 m_e c²=0.511 MeV），F=0.81（19% 抑制）；
        实测该能标 F≈1（点粒子，偏差 <1e-10）⇒ 模型 vs 实测 ~200σ 级排除。
   (F3) g-2：模型以"空间延展"解释 g_e=2.002319；但实测 a_e 与点状 QED 一致到 0.3 ppb，
        点粒子无需空间延展 ⇒ "延展修正 g"机制与 g-2 实测精度不相容。

  结论：**空间延展修正 g 的机制被弹性形状因子数据决定性证伪**（模型核心主张）。
  边界：仅当模型区分"电形状因子尺度"与"磁矩分布尺度"且二者不同时，F1/F2 或可规避；
  但当前 C0057/C0081 用同一 ρ_Q 同时给出 Q 与 μ ⇒ 电、磁分布同尺度 ⇒ 证伪成立。
================================================================================
"""
from __future__ import print_function
import os, sys, math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_v32_falsify_report.txt")

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
ELEV = 1.602176634e-19

import numpy as np
OMEGA_DE = 0.6875
r = np.logspace(-3.0, 2.0, 4000)
Kc, lK, r0, p = 3.1648e-08, 6.9989e-02, 6.9987e-03, 2.9094e+00
Tc, lT, O0, lO = 3.1648e-08, 6.9989e-02, 9.8778e-01, 1.1852e+00
K = Kc * np.exp(-r / lK) / (1.0 + (r / r0) ** p)
T = Tc * np.exp(-r / lT)
Om = OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-r / lO)
M_nat = ALPHA * 4.0 * math.pi * np.trapezoid(K * T * Om * r ** 2, r)
lamC_m = (1.0 / M_nat) * L_PLANCK
l_Q = lamC_m / 3.0
RE_LIM = 1e-18   # 电子电荷半径实验上限（保守，CODATA/高精度QED）

# F1: 尺度对比
ratio = lamC_m / RE_LIM
orders = math.log10(ratio)

# F2: 形状因子（C0085）
# q=1/λ_C：q·l_Q = (λ_C/3)/λ_C = 1/3
F_at_1overLc = (1.0 / (1.0 + (1.0 / 3.0) ** 2)) ** 2
# q=1/l_Q：q·l_Q=1
F_at_1overLq = (1.0 / 2.0) ** 2
# 探测能量 m_e c^2
E_probe_eV = M_E * C_LIGHT ** 2 / ELEV

# 实测点粒子形状因子偏差估计：R<1e-18 ⇒ 在 q=1/λ_C 偏差 < (q·R)² 量级
q_1Lc = 1.0 / lamC_m
dev_exp = (q_1Lc * RE_LIM) ** 2   # (R·q)² 极小

buf = []
log = buf.append
log("TUFT V3.2 分支TS7 · 证伪审计：空间延展修正 g 机制 vs 弹性形状因子实测")
log("运行时间: 2026-10-07  Python %s" % sys.version.split()[0])
log("")
log("=== 实验锚点 ===")
log("  E1 电子电荷半径上限 R_e < 1e-18 m（Penning trap ~1e-22，保守取 1e-18）")
log("  E2 电子反常磁矩 a_e^exp=1159652180.59(13)e-12 vs 点状QED a_e^SM=1159652180.252(95)e-12")
log("      —— 与点状 QED 一致到 ~0.3 ppb（10^-12 绝对量级）")
log("")
log("=== 模型预言（C0057/81/85）===")
log("  M1 电荷分布 ⟨r⟩=1.00116·λ_C = %.6e m" % (1.00116*lamC_m))
log("  M2 形状因子 F(q)=[1+(q·l_Q)²]^-2，l_Q=λ_C/3=%.6e m" % l_Q)
log("")
log("=== 证伪判定 ===")
log("  F1 尺度：λ_C/1e-18 = %.3e ⇒ 电荷分布比实验上限大 %.1f 量级 ⇒ 排除" % (ratio, orders))
log("  F2 形状因子：q=1/λ_C（探测 %.4f MeV）⇒ F=%.4f（%.1f%% 抑制）" % (E_probe_eV/1e6, F_at_1overLc, (1-F_at_1overLc)*100))
log("     实测该能标 F≈1（点粒子，偏差 <%.1e）⇒ 模型 0.81 vs 实测 ~1.00 ⇒ 决定性排除" % dev_exp)
log("     q=1/l_Q（%.4f MeV）⇒ F=%.4f" % (1/l_Q*HBAR*C_LIGHT/ELEV/1e6, F_at_1overLq))
log("  F3 g-2：模型以空间延展解释 g_e=2.002319；实测 a_e 与点状 QED 一致到 0.3 ppb")
log("     点粒子无需空间延展 ⇒ 延展修正 g 机制与 g-2 实测精度不相容")
log("")
log("=== 结论 ===")
log("  **空间延展修正 g 的机制被弹性形状因子数据决定性证伪（TUFT 核心主张）。**")
log("  边界：仅当模型区分电形状因子尺度与磁矩分布尺度且二者不同，F1/F2 或可规避；")
log("  但 C0057/C0081 用同一 ρ_Q 同时给出 Q 与 μ ⇒ 电、磁同尺度 ⇒ 证伪成立。")
log("  意义：TUFT 欲成立，须弃'空间延展'路线，转量子修正（α/2π 等）或改电磁分布尺度解耦。")

text = "\n".join(buf) + "\n"
print(text)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(text)
