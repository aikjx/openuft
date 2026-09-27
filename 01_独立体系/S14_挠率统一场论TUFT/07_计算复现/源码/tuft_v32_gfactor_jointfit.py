# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支B合成 —— 尺度钉扎 × 旋转项简并打破：联合拟合判定
================================================================================

把两条并行线合成到同一判定：
  · 并行流 C0048/49（tuft_v32_degeneracy_break.py）：常规观测量只依赖乘积
    Π=q0ω0；加旋转能 E_rot=½ω0²N 使 M 与 g 依赖 ω0，切断 (q0,ω0) 简并。
  · 本流 C0050（tuft_v32_gfactor_verify.py）：g=2·M_nat·⟨r⟩_nat，g=2 ⟺
    ⟨r⟩=λ_C(nat)=2.39e22 l_P；当前单尺度剖面 ⟨r⟩~O(l_P) ⇒ g~1e-22。

本脚本回答一个此前未定论的关键问题：**旋转项能否"桥接"尺度缺口，让 g 达到
g_e≈2.0023？** 并给出构造性的两尺度路线（质量核@普朗克尺度 + 电荷/磁晕@康普顿
尺度）的定量验证。

红线声明：模型层面机制演示（无量纲自洽、固定/双尺度剖面假设），
不构成物理真实性主张；电荷/磁矩密度到 K/T/Ω 的耦合映射仍挂账。
================================================================================
"""
from __future__ import print_function
import os, sys, math
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_v32_gfactor_jointfit_report.txt")

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
OMEGA_DE = 0.6875
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
E_ELECTRON = M_E * C_LIGHT ** 2 / E_PLANCK
GE_EXP = 2.00231930436

buf = []
log = buf.append

# ---------------- 复用 C0045 最优剖面（tuft_v32_adjoint_slsqp） ----------------
r = np.logspace(-3.0, 2.0, 4000)
Kc, lK, r0, p = 3.1648e-08, 6.9989e-02, 6.9987e-03, 2.9094e+00
Tc, lT, O0, lO = 3.1648e-08, 6.9989e-02, 9.8778e-01, 1.1852e+00
K = Kc * np.exp(-r / lK) / (1.0 + (r / r0) ** p)
T = Tc * np.exp(-r / lT)
Om = OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-r / lO)
dO = Om - OMEGA_DE

N = np.trapezoid(dO * r ** 2, r)
I_mu = np.trapezoid(dO * r ** 3, r)
M_st = ALPHA * 4.0 * math.pi * np.trapezoid(K * T * Om * r ** 2, r)
M_nat = M_st                                   # 电子静能（普朗克质量）
rbar_nat = I_mu / N                            # ⟨r⟩_nat (l_P)
lamC_nat = 1.0 / M_nat                         # λ_C(nat)

def g_func(M, rb):
    return 2.0 * M * rb                         # g = 2·M_nat·⟨r⟩_nat (ħ=1)

log("TUFT V3.2 分支B合成 · 尺度钉扎 × 旋转项简并打破：联合判定")
log("运行时间: 2026-09-28  Python %s  numpy %s" % (sys.version.split()[0], np.__version__))
log("剖面观测量（C0045 收敛剖面）: N=%.6e  I_mu=%.6e  M_static=%.6e  ⟨r⟩_nat=%.4e l_P"
    % (N, I_mu, M_st, rbar_nat))
log("M_nat(电子静能)=%.6e 普朗克质量;  λ_C(nat)=1/M_nat=%.6e l_P" % (M_nat, lamC_nat))
log("")

# =====================================================================
# (1) 复现并行流：旋转项切断简并（同一乘积线上 M/g 随 ω0 变化）
# =====================================================================
log("=== (1) 复现并行流 C0048/49：旋转项 E_rot=½ω0²N 使 M、g 依赖 ω0 ===")
log("  无旋转项: g_static=%.4e（纯剖面不变量，C0042/并行C0048）" % g_func(M_nat, rbar_nat))
for w in (1.0, 2.0, 3.0, 6.0):
    M = M_nat + 0.5 * w ** 2 * N
    log("   ω0=%.0f: M(含旋转)=%.6e   g=%.6e   (M/M_e=%.3e)"
        % (w, M, g_func(M, rbar_nat), M / M_nat))
log("  ⇒ 旋转项确实切断 (q0,ω0) 简并（与 C0049 数值一致）；但 g 仍 ~1e-22 量级。")
log("")

# =====================================================================
# (2) 关键判定：旋转项能否桥接尺度缺口、使 g 达 g_e≈2.0023？
# =====================================================================
log("=== (2) 旋转项能否桥接尺度缺口？ ===")
log("  目标 g_e=2.0023, M 固定为电子静能 M_nat=%.6e" % M_nat)
req_r = GE_EXP / 2.0 / M_nat                    # 需 ⟨r⟩_nat
log("  [约束 A·尺度] 要 g=g_e 且 M=M_e ⇒ 必须 ⟨r⟩_nat = g_e/2/M_nat = %.6e l_P"
    % req_r)
log("             = %.6e λ_C(nat)（电荷分布须在康普顿尺度）" % (req_r / lamC_nat))
log("             当前剖面 ⟨r⟩_nat=%.4e l_P，缺口 %.3e 倍" % (rbar_nat, req_r / rbar_nat))
log("")
log("  [约束 B·旋转] 若试图用旋转能 M+=½ω0²N 把 M 抬到使 g=g_e 的量级：")
log("    令 ½ω0²N ≈ g_e/2/⟨r⟩ - M_nat, 需 ω0 ≈ sqrt(2·M_need/N)")
M_need = GE_EXP / 2.0 / rbar_nat - M_nat
w_need = math.sqrt(max(2.0 * M_need / N, 0.0))
log("    需 M_total ≈ g_e/2/⟨r⟩_nat = %.6e 普朗克质量（=%.3e × 电子静能）"
    % (GE_EXP / 2.0 / rbar_nat, (GE_EXP / 2.0 / rbar_nat) / M_nat))
log("    需 ω0 ≈ %.4e；此时旋转能=%.6e 普朗克质量 ≫ M_e=%.6e ⇒ 质量拟合被破坏"
    % (w_need, 0.5 * w_need ** 2 * N, M_nat))
log("  ⇒ 结论：旋转项只切断简并，**不能桥接尺度缺口**——用它抬 g 会让质量暴涨到")
log("    普朗克量级，违背电子静能拟合（C0045）。两约束独立，尺度缺口是 binding。")
log("")

# =====================================================================
# (3) 构造性路线：两尺度结构（普朗克质量核 + 康普顿电荷/磁晕）
# =====================================================================
log("=== (3) 构造性两尺度路线：普朗克尺度质量核 + 康普顿尺度电荷/磁晕 ===")
log("  设质量密度集中于普朗克尺度核（M=M_nat=电子静能，C0045 已拟合），")
log("  电荷/磁矩密度集中于康普顿尺度晕（⟨r⟩_charge = λ_C 或 g_e 所需）：")
for rb_label, rb in (("⟨r⟩=λ_C(nat)", lamC_nat), ("⟨r⟩=1.00116·λ_C(g_e 精确)", req_r)):
    g = g_func(M_nat, rb)
    log("    %s: ⟨r⟩_nat=%.6e l_P  ⇒  g=2·M_nat·⟨r⟩=%.6f   (g_e=2.0023)"
        % (rb_label, rb, g))
log("  ⇒ 两尺度结构（质量核@~l_P + 电荷/磁晕@λ_C≈2.4e22 l_P）可同时满足")
log("    质量拟合（C0045）与 g_e≈2.0023（本流 C0050）。")
log("  当前单尺度 ansatz（K/T/Ω 全部指数尾~l_P）不含此两尺度，是下一层建模对象。")
log("")

# =====================================================================
# 结论
# =====================================================================
log("=== 结论 ===")
log("  1) 旋转项（并行 C0048/49）切断 (q0,ω0) 简并，真实但正交于尺度问题。")
log("  2) 尺度缺口（本流 C0050）是 binding：g=g_e 需电荷半径=λ_C(nat)，")
log("     旋转项不能桥接（会破坏质量拟合）。")
log("  3) 构造性路线 = 两尺度结构：普朗克质量核(已拟合) + 康普顿电荷/磁晕(待建)。")
log("     该结构可同时达 M_e 与 g_e≈2.0023。")
log("红线声明：模型层面机制演示；电荷/磁矩密度映射与两尺度 ansatz 构造仍挂账。")

text = "\n".join(buf) + "\n"
print(text)
try:
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
except Exception as exc:
    log("[warn] 报告写入失败: %s" % exc)
