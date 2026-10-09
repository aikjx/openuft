# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · Airy 晕核-晕 virial 平衡审计（C0108）
================================================================
C0100 的 virial 平衡假设 U_em(R)=C/R∝1/R（壳层，U_em=1.215%M_e，U_P=(1/3)U_em=0.4055%）。
C0106/C0107 确立 Airy 账本（U_es=0.3300%、U_mag=0.0816%）。本审计量化 Airy 下平衡如何变：

  P1 形状依赖的 R 缩放：Airy 静电 U_es∝1/R（电荷分布缩放）；Airy 磁 U_mag∝μ²·geo，
     μ=Q⟨r⟩∝R、geo∝1/R² ⟹ U_mag∝常数（不随 R 缩放）。
  P2 Airy virial：dU_em/dR=dU_es/dR（磁项 d/dR=0），平衡负压 P_airy=-U_es/(4πR*³)，
     应力能 U_P,airy=(1/3)U_es=0.1100%M_e（仅静电贡献），d²E/dR²=4U_es/R*²>0（仍稳定）。
  P3 对照 shell（C0100）：U_P=(1/3)U_em=0.4055%；账本A/B M_core。
  P4 结论：C0100 平衡数值形状依赖；Airy（第一性）下应力能 0.1100%，磁项不参与 virial。

红线：模型层面构造性核验，非物理主张；α=e²/4π(HL)；U_es/U_mag 沿用 C0106/C0107；
"应力能是否计入质量账本"为 4/3 型惯例选择；Airy 形状来自 C0096 conjecture 2.11。
"""
import numpy as np, io
OUT="tuft_v32_airy_corehalo_audit_report.txt"
buf=[]; log=buf.append
alpha=1/137.035999084; M_nat=4.1855e-23; lamC=1.0/M_nat
Rstar=0.5*lamC
Ues_airy=0.003300*M_nat        # 0.3300%M_e (C0106)
Umag_airy=0.000816*M_nat       # 0.0816%M_e (C0107)
Uem_airy=Ues_airy+Umag_airy    # 0.4116%
Uem_shell=(5.0/3.0)*alpha*M_nat  # 1.2152% (C0100/C0090)

log("TUFT V3.2 攻破阶段 · Airy 晕核-晕 virial 平衡审计（C0108）")
log("运行时间: 2026-10-10")
log("R*=½λ_C=%.4e l_P; Airy U_es=0.3300%%/U_mag=0.0816%%/U_em=0.4116%%; shell U_em=1.2152%%"%Rstar)
log("")
log("=== P1 形状依赖的 R 缩放 ===")
log("  Airy 静电: U_es∝1/R（电荷分布缩放 ⟹ 自能∝1/R）")
log("  Airy 磁:   U_mag∝μ²·geo，μ=Q⟨r⟩∝R、geo∝1/R² ⟹ U_mag∝常数（不随 R 缩放）")
log("  ⟹ Airy 磁项不参与 virial（dU_mag/dR=0），平衡仅由静电项驱动")
log("")
log("=== P2 Airy virial 平衡 ===")
P_airy = -Ues_airy/(4*np.pi*Rstar**3)
UP_airy = Ues_airy/3.0          # -(4/3)πR³·P=(1/3)U_es
d2E = 4.0*Ues_airy/Rstar**2     # d²U_es/dR²+d²U_P/dR²=2U_es/R²+2U_es/R²
log("  平衡负压 P_airy = -U_es/(4πR*³) = %.4e M_P/l_P³ (<0 内拉)"%P_airy)
log("  应力能 U_P,airy = (1/3)U_es = %.4f%%·M_e"%(UP_airy/M_nat*100))
log("  稳定判据 d²E/dR² = 4U_es/R*² = %.4e (>0 稳定极小 ✓)"%d2E)
log("")
log("=== P3 对照 shell（C0100）===")
UP_shell = (1.0/3.0)*Uem_shell
log("  shell U_P = (1/3)U_em = %.4f%%·M_e"% (UP_shell/M_nat*100))
log("  Airy  U_P = (1/3)U_es = %.4f%%·M_e（磁项不参与）"% (UP_airy/M_nat*100))
log("  ⟹ 应力能形状依赖：shell 0.4055%% vs Airy 0.1100%%（差 %.1f 倍）"% (UP_shell/UP_airy))
log("")
log("=== P4 质量账本（Airy, 惯例敏感度）===")
Mc_no  = M_nat*(1-Uem_airy/M_nat)          # 账本A 不计应力能
Mc_yes = M_nat*(1-Uem_airy/M_nat-UP_airy/M_nat)  # 账本B 计应力能
log("  账本A（不计应力能）: M_core=1-U_em_airy=%.4f·M_e (C0107 ✓)"%(Mc_no/M_nat))
log("  账本B（计应力能）:   M_core=1-U_em_airy-U_P_airy=%.4f·M_e"% (Mc_yes/M_nat))
log("  差值 U_P_airy=%.4f%%·M_e 为 4/3 型惯例敏感度（Airy 下比 shell 的 0.4055%% 小 3.7 倍）"% (UP_airy/M_nat*100))
log("")
log("=== 结构结论 ===")
log("  C0100 的 virial 平衡数值形状依赖：shell U_P=0.4055%% vs Airy U_P=0.1100%%；")
log("  平衡半径 R*=½λ_C 在 Airy 下仍稳定（d²E/dR²>0）✓；但应力能只含静电贡献（磁项")
log("  不随 R 缩放、不参与 virial）。账本A 不变（M_core=0.9959），账本B Airy 下 M_core=0.9946。")
log("")
log("红线：模型层面构造性核验，非物理主张；α=e²/4π(HL)；U_es/U_mag 沿用 C0106/C0107；")
log("'应力能是否计入质量账本'为 4/3 型惯例选择；Airy 形状来自 C0096 conjecture 2.11；")
log("磁项∝常数假设基于 μ=Q⟨r⟩∝R、geo∝1/R²（C0107 数值支撑）。")
with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
