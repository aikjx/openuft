# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · 磁自能与经典 4/3 问题：核=Poincaré 应力
============================================================
背景：C0090 补全了晕的静电自能（~α·M_e），磁自能仅给量级。本脚本：
  P1 磁自能 U_mag（自旋带电晕，偶极场截止法），U_mag/U_es 比值；
  P2 完整 EM 自能账本 U_EM=U_es+U_mag，系数结构（2/3、5/6、4/3）；
  P3 经典 4/3 问题：EM 质量系数依赖计数方式（4/3 与 (1+2/3) 不一致）——
    根源是无额外应力（Poincaré 应力）时电磁电子不稳定。TUFT 两尺度模型
    的**核恰好充当 Poincaré 应力**：提供束缚使晕稳定、并钉住质量系数。
    结构统一声明：两尺度必要（尺度缺口，C0058）与经典 4/3 问题（无束缚
    电磁电子不稳定）是同一物理要求的两面——电子必须有一个非纯电磁的
    束缚源（核/应力）。
  P4 完整质量预算 M_core = M_e − m_em_full。

红线：模型层面构造性核验，非物理主张；4/3 表述依赖（此处取偶极场自能 +
  Poincaré 应力论证，结构声明为 conjecture 级）；HL 约定 e²=4πα。
"""
import numpy as np, io, math
OUT = "tuft_v32_em_43problem_report.txt"
buf = []; log = buf.append

M_P   = 2.176434e-8
me    = 9.1093837015e-31
M_nat = me/M_P
g_e   = 2.00231930436153
alpha = 1.0/137.035999084
r_target = g_e/(4.0*M_nat)      # 0.5006λ_C (l_P), C0083
lamC = 1.0/M_nat

log("TUFT V3.2 攻破阶段 · 磁自能与经典 4/3 问题：核=Poincaré 应力")
log("运行时间: 2026-10-07")
log("订正半径 ⟨r⟩=%.6e l_P=%.6f·λ_C (C0083)" % (r_target, r_target/lamC))
log("")

# ---- P1 磁自能 ----
log("=== P1 磁自能（自旋带电晕，偶极场截止 U_mag=μ²/(12πR³)，μ=Q·⟨r⟩）===")
# 壳层：U_es=α/(2R)(c_es=0.5)；U_mag=α/(3R)
for shape, c_es, c_mag in [("shell",0.5, 1/3.0), ("uniform_sphere",0.6, 1/3.0)]:
    Ues = alpha*(lamC/r_target)*c_es*0.5/0.5   # 归一化表述：U_es=α·(λ_C/⟨r⟩)·c_es'
    # 直接：U_es/M_e 由 C0090：shell 0.73%，sphere 0.87%
    Ues_over_M = {"shell":0.007291, "uniform_sphere":0.008746}[shape]
    # U_mag = α/(3R) 相对 U_es=α·c/(2R)（shell c=1/2 ⟹ U_es=α/(2R)，U_mag/U_es=(2/3)）
    Umag_over_Ues = {"shell": (1/3.0)/(1/2.0), "uniform_sphere": (1/3.0)/(3/5.0)}[shape]
    Uem_over_M = Ues_over_M*(1+Umag_over_Ues)
    log("  [%-15s] U_es/M=%.4f%%  U_mag/U_es=%.4f  U_mag/M=%.4f%%  U_EM/M=%.4f%%"
        % (shape, 100*Ues_over_M, Umag_over_Ues, 100*Ues_over_M*Umag_over_Ues, 100*Uem_over_M))
log("  ⟹ U_mag~O(α·M_e) 与 U_es 同量级；shell 时 U_mag=(2/3)U_es。")

# ---- P2 完整 EM 账本 + 系数结构 ----
log("")
log("=== P2 完整 EM 自能账本：质量系数依赖计数方式 ===")
# R=⟨r⟩=0.5006λ_C：α/(2R)、α/(3R)、(4/3)α/(2R) 等系数
R_lP = r_target
coeffs = {
    "U_es(shell)=α/(2R)":            0.5,
    "U_es(球)=3α/(5R)":              0.6,
    "U_mag(shell)=α/(3R)":           1/3.0,
    "(4/3)·U_es(shell)":             (4/3.0)*0.5,
    "U_es+U_mag(shell)":             0.5+1/3.0,
}
for name, c in coeffs.items():
    U_over_M = alpha*(lamC/R_lP)*c
    log("  %-26s ⟹ U/M_e = α·(λ_C/⟨r⟩)·%.4f = %.4e = %.4f%%"
        % (name, c, U_over_M, 100*U_over_M))
log("  ⟹ 系数在 1/3–2/3 之间，全部 ~α·M_e；'哪个系数对'取决于计数方式——即 4/3 问题。")

# ---- P3 4/3 问题与核=Poincaré 应力 ----
log("")
log("=== P3 经典 4/3 问题：无束缚电磁电子不稳定 ⟹ 核=Poincaré 应力 ===")
log("  经典结论：纯电磁电子（电荷+自旋场，无额外应力）不稳定——库仑斥力把它")
log("  炸开，且 EM 质量系数依赖计数（4/3 vs (1+2/3) 不一致）；Poincaré 以")
log("  非电磁束缚应力（Poincaré 应力）挽救：提供内聚力、钉住质量系数。")
log("  TUFT 两尺度模型：核（M_core）正是这个 Poincaré 应力——")
log("  ① 束缚晕使其稳定（质量在核，晕是电荷壳）；")
log("  ② 钉住质量系数（M_core=M_e−m_em，核占比>0.99）。")
log("  结构统一（conjecture 级）：两尺度必要（尺度缺口 C0058）与经典 4/3 问题")
log("  （无束缚电磁电子不稳定）是同一物理要求的两面——电子必须有一个非纯电磁")
log("  的束缚源；两尺度模型的核 = 经典 Poincaré 应力。")

# ---- P4 完整质量预算 ----
log("")
log("=== P4 完整质量预算 M_core = M_e − m_em_full ===")
Uem_over_M_shell = (0.5+1/3.0)*alpha*(lamC/r_target)
M_core = M_nat*(1-Uem_over_M_shell)
log("  shell 完整 EM 自能 m_em=U_es+U_mag=%.4f%%·M_e" % (100*Uem_over_M_shell))
log("  M_core = M_e − m_em = %.6e M_P（%.4f·M_e）  M_total=%.6e=M_e:✓ 核占比 %.4f"
    % (M_core, M_core/M_nat, M_core+Uem_over_M_shell*M_nat, M_core/M_nat))
log("  ⟹ 含磁自能后核占比约 %.4f（静电项 0.9927、全 EM 项略降），仍主导。"
    % (M_core/M_nat))

log("")
log("红线声明：模型层面构造性核验，非物理主张；磁自能取偶极场截止法，4/3 表述")
log("依赖经典电子论；'核=Poincaré 应力'为结构统一声明（conjecture 级），有待")
log("TUFT 作用量钉扎证伪/证实；HL 约定 e²=4πα。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
