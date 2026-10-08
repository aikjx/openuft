# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · 核-晕耦合动力学作用量实现（C0100）
============================================================
背景：C0093/C0094 把"核 = Poincaré 应力"作为结构对应（conjecture）。本脚本把
它实现为**可算的力学平衡（virial）条件**，升级为 verified（模型层面）：

  U_em(R) = (5/3)·α·M_e·(λ_C/(2R))   [EM 自能，C0090 成立；R*=½λ_C 时 =1.215%M_e ✓]
  U_P(R)  = -(4/3)πR³·P              [Poincaré 应力，常内压 P]
  E(R)    = M_core + U_em(R) + U_P(R)

  P1 平衡：dE/dR=0 于 R*=½λ_C ⟹ P（负压）与应力能 U_P(R*)=(1/3)U_em(R*)=(5/9)αM_e。
  P2 稳定：d²E/dR²>0 于 R*（稳定极小）。
  P3 质量账本（惯例敏感度）：不计应力能 → M_core=(1-(5/3)α)M_e=0.988M_e（=C0094）；
     计应力能 → M_core=(1-(20/9)α)M_e=0.984M_e。差值 (5/9)α=0.4055% 为 4/3 型
     惯例敏感度，显式暴露（C0093 遗留）。

红线：模型层面构造性核验，非物理主张；U_em 沿用 C0090 定义与数值；α=e²/4π(HL)；
"应力能是否计入质量账本"为 4/3 型惯例选择，本脚本如实并列两种账本。
"""
import numpy as np, io, math
OUT = "tuft_v32_corehalo_coupling_report.txt"
buf=[]; log=buf.append

alpha = 1/137.035999084
M_nat = 4.1855e-23          # M_e/M_P (C0083)
lamC  = 1.0/M_nat           # λ_C in l_P = 1/M_nat
Rstar = 0.5*lamC            # 目标晕半径 ½λ_C
U_em  = (5.0/3.0)*alpha*M_nat   # 于 R*=½λ_C
# U_em(R)=C/R, C=(5/3)αM_e·λ_C/2
C = (5.0/3.0)*alpha*M_nat*lamC/2.0

log("TUFT V3.2 攻破阶段 · 核-晕耦合动力学作用量实现（C0100）")
log("运行时间: 2026-10-07")
log("α=%.10e, M_e/M_P=%.6e, λ_C=%.6e l_P, R*=½λ_C=%.6e l_P"%(alpha,M_nat,lamC,Rstar))
log("U_em(R*)=(5/3)αM_e=%.6e M_P = %.6f%%·M_e  (C0090 ✓)"%(U_em, U_em/M_nat*100))
log("")

log("=== P1 力学平衡 dE/dR=0 于 R* ===")
P = -C/(4*math.pi*Rstar**4)          # 平衡负压
U_P = (1.0/3.0)*U_em                  # -(4/3)πR³·P = (1/3)U_em
log("  C=(5/3)αM_e·λ_C/2 = %.6e M_P·l_P"%C)
log("  平衡负压 P = -C/(4πR*⁴) = %.6e M_P/l_P³ (<0 内拉)  ✓"%P)
log("  应力能 U_P(R*) = -(4/3)πR*³·P = (1/3)U_em = %.6e M_P = %.6f%%·M_e"%(U_P, U_P/M_nat*100))
# 验证平衡式
dUem = -C/Rstar**2
dUP  = -4*math.pi*Rstar**2*P
log("  校验 dU_em/dR=%.6e, dU_P/dR=%.6e, 和=%.3e (≈0 ✓)"%(dUem,dUP,dUem+dUP))

log("")
log("=== P2 稳定判据 d²E/dR² > 0 ===")
d2Uem = 2.0*C/Rstar**3
d2UP  = -8*math.pi*Rstar*P
d2E   = d2Uem+d2UP
log("  d²U_em/dR²=%.6e, d²U_P/dR²=%.6e, d²E/dR²=%.6e (>0 稳定极小 ✓)"%(d2Uem,d2UP,d2E))
log("  ⟹ R*=½λ_C 是力学稳定平衡半径：外斥 EM 压被核的内拉 Poincaré 应力平衡。")

log("")
log("=== P3 质量账本：'核=Poincaré 应力'实现为可算平衡 ===")
M_core_no  = M_nat*(1-(5.0/3.0)*alpha)     # 不计应力能
M_core_yes = M_nat*(1-(20.0/9.0)*alpha)    # 计应力能
log("  账本A（不计应力能，U_P 视为约束非质量项）:")
log("    M_core = (1-(5/3)α)M_e = %.6e M_P = %.4f%%·M_e  (=C0094 ✓)"%(M_core_no,M_core_no/M_nat*100))
log("    E = M_core + U_em = %.6e M_P = M_e ✓"% (M_core_no+U_em))
log("  账本B（计应力能，U_P 计入质量）:")
log("    M_core = (1-(20/9)α)M_e = %.6e M_P = %.4f%%·M_e"%(M_core_yes,M_core_yes/M_nat*100))
log("    E = M_core + U_em + U_P = %.6e M_P = M_e ✓"% (M_core_yes+U_em+U_P))
log("  差值 (5/9)α = %.6f%%·M_e 为 4/3 型惯例敏感度（C0093 遗留，现显式暴露）。"%(5/9*alpha*100))

log("")
log("=== 结构结论 ===")
log("  '核=Poincaré 应力'从结构对应升级为可算力学平衡：晕半径 R*=½λ_C 是 EM 自斥")
log("  与核内拉应力平衡的稳定极小；应力能为 (5/9)αM_e=0.4055%·M_e；质量账本闭合，")
log("  但裸核质量对'应力能是否计入'敏感（0.988 vs 0.984·M_e，差 0.4055%）——")
log("  该 4/3 型惯例敏感度现显式化，作为诚实未决项保留。")

log("")
log("红线声明：模型层面构造性核验，非物理主张；U_em 沿用 C0090 定义；α=e²/4π(HL)；")
log("'应力能是否计入质量账本'为 4/3 型惯例选择，本脚本如实并列两种账本。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
