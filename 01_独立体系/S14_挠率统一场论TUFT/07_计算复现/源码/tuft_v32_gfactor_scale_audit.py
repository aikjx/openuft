# -*- coding: utf-8 -*-
"""
TUFT V3.2 分支B 追踪 · g 因子尺度关系的独立复核（因子-2 订正审计）
================================================================
背景：并行 C0050 判定写 "g=4M·Iμ/(N·ℏ)=2M_nat·⟨r⟩_nat"（⟨r⟩=Iμ/N 为电荷分布
半径）。但由 TUFT 自身的 g 因子定义（C0042：g=2Mμ/(Q0·S)，S=ℏ/2）：
  g = 2M·μ/(Q0·ℏ/2) = 4M·μ/(Q0·ℏ)，又 μ/Q0 = Iμ/N ⟹
  g = 4M·Iμ/(N·ℏ) = 4·M_nat·⟨r⟩_nat   （自然单位 ℏ=1）
⟹ C0050 的 "=2M_nat·⟨r⟩_nat" 缺一个因子 2。本脚本做第一性复核：

  P1 标准锚点：g_e = 4m_e·μ_e/(e·ℏ) = 2.003（用真实物理常数，作为 g 公式的
     因子判据）——若正确的系数是 4，则 C0050 的 2 即错；
  P2 自洽推导：从 C0042 的 g=2Mμ/(Q0·S) 逐步推出 g=4M·Iμ/(Nℏ)，排除系数歧义；
  P3 数值订正：当前最优剖面 ⟨r⟩=3.556 l_P 时
     g_correct = 4·M_nat·⟨r⟩ = 5.96e-22 （C0050 写 2.98e-22，差 2 倍）；
     g_e=2.0023 所需 ⟨r⟩ = g_e/(4·M_nat) = 0.5006·λ_C
     （C0052 写 1.00116·λ_C，差 2 倍）；
  P4 结论是否改变：定性结论（尺度缺口 ~21 个数量级是 binding blocker）
     不变，仅数值因子 2 订正。

红线：本审计只纠因子/系数的约定一致性，不改变"尺度缺口主导"的定性结论；
模型层面核验，非物理真实性主张。
"""
import numpy as np, math, io, os

OUT = "tuft_v32_gfactor_scale_audit_report.txt"
buf = []; log = buf.append

# ---- 物理常数 (SI) ----
e  = 1.602176634e-19     # C
me = 9.1093837015e-31    # kg
mu_e = 9.2847647043e-24  # J/T (electron magnetic moment)
hbar = 1.054571817e-34   # J·s
g_e = 2.00231930436153
M_P = 2.176434e-8        # kg
M_nat = me / M_P         # 自然单位质量

log("TUFT V3.2 分支B 追踪 · g 因子尺度关系的独立复核（因子-2 订正审计）")
log("运行时间: 2026-10-07")

# ---- P1 标准锚点 ----
g_std = 4.0*me*mu_e/(e*hbar)
log("")
log("=== P1 标准物理锚点：g_e = 4·m_e·μ_e/(e·ℏ) ===")
log("  4·m_e·μ_e/(e·ℏ) = 4·(%.4e)·(%.4e)/((%.4e)·(%.4e))" % (me,mu_e,e,hbar))
log("  = %.6f   vs 实验 g_e=%.8f   相对误差=%.2e" % (g_std, g_e, abs(g_std-g_e)/g_e))
log("  ⟹ g 因子标准公式的系数是 4（而非 2）；电子 S=ℏ/2 时 g=4mμ/(eℏ) 成立。")

# ---- P2 自洽推导 ----
log("")
log("=== P2 从 C0042 的 g=2M·μ/(Q0·S) 推出 g=4M·Iμ/(N·ℏ) ===")
log("  定义：S=ℏ/2（电子自旋 1/2），μ=q0·ω0·Iμ，Q0=q0·ω0·N ⟹ μ/Q0=Iμ/N")
log("  g = 2M·μ/(Q0·S) = 2M·μ/(Q0·ℏ/2) = 4M·μ/(Q0·ℏ) = 4M·Iμ/(N·ℏ)")
log("  = 4·M_nat·(Iμ/N) = 4·M_nat·⟨r⟩_nat   （自然单位 ℏ=1）")
log("  ⟹ C0050 写 '=2M_nat·⟨r⟩_nat' 与自身引用的 C0042 公式差因子 2。")

# ---- P3 数值订正（当前最优剖面）----
N    = 9.999806e-01
I_mu = 3.555531e+00
langle = I_mu/N
g_corr  = 4.0*M_nat*langle          # 正确
g_c50   = 2.0*M_nat*langle          # C0050 用
langle_need_corr = g_e/(4.0*M_nat)  # 正确
langle_need_c50  = g_e/(2.0*M_nat)  # C0052 用
lamC = 1.0/M_nat
log("")
log("=== P3 数值订正（当前最优剖面 ⟨r⟩=Iμ/N=%.6e l_P）===" % langle)
log("  正确 g = 4·M_nat·⟨r⟩ = 4·(%.4e)·(%.4e) = %.4e" % (M_nat,langle,g_corr))
log("  C0050 g = 2·M_nat·⟨r⟩ = %.4e   （差因子 2）" % g_c50)
log("  目标 g_e=%.6f 所需 ⟨r⟩:" % g_e)
log("    正确: ⟨r⟩ = g_e/(4·M_nat) = %.6e l_P = %.6f·λ_C" % (langle_need_corr, langle_need_corr/lamC))
log("    C0052: ⟨r⟩ = g_e/(2·M_nat) = %.6e l_P = %.6f·λ_C" % (langle_need_c50, langle_need_c50/lamC))
gap_corr = g_e/g_corr
gap_c50  = g_e/g_c50
log("  尺度缺口: 正确 g_e/g = %.3e（%.1f 数量级）; C0050 记 %.3e（%.1f 数量级）"
    % (gap_corr, math.log10(gap_corr), gap_c50, math.log10(gap_c50)))

# ---- P4 定性结论不变 ----
log("")
log("=== P4 定性结论是否改变 ===")
log("  无论系数 2 还是 4，缺口都在 ~21 个数量级（%.1f vs %.1f），" % (math.log10(gap_corr), math.log10(gap_c50)))
log("  ⟹ C0050/C0052 的定性结论——尺度缺口是 binding blocker、单尺度不可行、")
log("    两尺度必要——不因因子 2 而改变；被订正的仅是 g 关系式系数与由此推出的")
log("    所需电荷半径（1.00116λ_C → 0.5006λ_C）。")

log("")
log("红线声明：本审计只纠因子/系数的约定一致性，不改变'尺度缺口主导'定性结论；")
log("模型层面核验，非物理真实性主张。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
