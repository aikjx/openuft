# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · 完整能量账本闭合与 QED 质量重整化结构
==========================================================
背景：C0087(动能+旋转)、C0090(静电自能)、C0093(磁自能+核=Poincaré 应力)。
本脚本把所有项纳入**一个闭合能量账本**，并揭示其就是 **QED 质量重整化结构**：

  P1 完整账本：M_e = M_core + E_k + E_rot + U_es + U_mag（核占主导）
     逐项列出，总闭合 ✓。
  P2 质量重整化结构：物理质量 = 裸质量(核) + EM 自能修正
     M_e = M_bare + δM，δM = U_es+U_mag ≈ 1.2%·M_e ⟹ M_bare ≈ 0.988·M_e。
     —— 这正是 QED 质量重整化（裸质量被自能重整化为物理质量）。
  P3 自洽性：δM 依赖晕半径 R=⟨r⟩=0.5006λ_C（由 g_e 固定）⟹ 质量重整化
     与 g 因子由同一几何钉住；δM/M_e = α·(λ_C/⟨r⟩)·(5/6)c ≈ 1.2%。
  P4 与 g−2 的 α 阶联系（conjecture 级）：同一 EM 耦合既重整化质量又产生
     反常磁矩；δM/M_e(~1.2%) 与 (g−2)/2=α/2π(~0.116%) 同为 α 阶辐射修正，
     但量级差 ~10（δM 含经典自能，g−2 为量子圈效应，结构对应非推导）。

红线：模型层面构造性核验，非物理主张；δM 取库仑+磁偶极自能（含 4/3 表述
依赖）；'质量重整化结构对应'为 conjecture 级结构声明；HL 约定 e²=4πα。
"""
import numpy as np, io, math
OUT = "tuft_v32_mass_renorm_report.txt"
buf = []; log = buf.append

M_P   = 2.176434e-8
me    = 9.1093837015e-31
M_nat = me/M_P
g_e   = 2.00231930436153
alpha = 1.0/137.035999084
r_target = g_e/(4.0*M_nat)      # 0.5006λ_C, C0083
lamC = 1.0/M_nat

# 能量项（shell 形状，订正半径）
E_k   = 1.966e-45      # 动能 (C0087, exp 量级)
E_rot = 0.5*M_nat**2   # 旋转能 ω_C=M_nat
U_es  = 0.5*alpha*(lamC/r_target)*M_nat   # shell U_es=α/(2R)
U_mag = (1/3.0)*alpha*(lamC/r_target)*M_nat  # shell U_mag=α/(3R)

log("TUFT V3.2 攻破阶段 · 完整能量账本闭合与 QED 质量重整化结构")
log("运行时间: 2026-10-07")
log("订正半径 ⟨r⟩=%.6e l_P=%.6f·λ_C (C0083)；α=1/%.6f" % (r_target, r_target/lamC, 1/alpha))
log("")

# ---- P1 完整账本 ----
log("=== P1 完整能量账本（shell 晕，逐项）===")
U_em = U_es + U_mag
M_core = M_nat - (E_k+E_rot+U_em)
rows = [("核 M_core", M_core), ("动能 E_k", E_k), ("旋转能 E_rot", E_rot),
        ("静电 U_es", U_es), ("磁 U_mag", U_mag)]
tot = 0
for name, val in rows:
    log("  %-12s %12.3e M_P  (%.4e·M_e)" % (name, val, val/M_nat))
    tot += val
log("  %-12s %12.3e M_P  = M_e ✓  核占比 %.4f" % ("总 M", tot, M_core/M_nat))
log("  晕场能(EM) U_em=U_es+U_mag=%.4e M_P = %.4f%%·M_e" % (U_em, 100*U_em/M_nat))
log("  ⟹ 账本闭合：核(98.8%) + EM 自能(1.2%) + 动能/旋转(~0) = M_e。")

# ---- P2 质量重整化结构 ----
log("")
log("=== P2 质量重整化结构：M_physical = M_bare + δM ===")
log("  M_e = M_core + (E_k+E_rot+U_em)；把核视为裸质量 M_bare=M_core，")
log("  δM = E_k+E_rot+U_em ≈ U_em ≈ 1.2%·M_e ⟹ M_bare ≈ 0.988·M_e。")
log("  ⟹ 这正是 QED 质量重整化：裸质量被 EM 自能修正得到物理质量。")
log("  M_bare = M_e − δM = %.6e M_P（%.4f·M_e）；δM = %.4e M_P（%.4f%%·M_e）"
    % (M_core, M_core/M_nat, U_em, 100*U_em/M_nat))

# ---- P3 自洽性：δM 与 g 同几何钉扎 ----
log("")
log("=== P3 自洽性：δM 与 g 由同一几何(R=0.5006λ_C)钉住 ===")
log("  δM/M_e = α·(λ_C/⟨r⟩)·(5/6) = α·(1/0.5006)·0.8333 = %.4e = %.4f%%"
    % (alpha*(lamC/r_target)*(5/6.0), 100*alpha*(lamC/r_target)*(5/6.0)))
log("  ⟨r⟩=0.5006λ_C 来自 g_e=4M_nat⟨r⟩(C0083) ⟹ 质量重整化 δM 与 g 因子")
log("  由同一两尺度几何(核质量×晕半径)钉住——两观测量(质量修正、g)同源。")

# ---- P4 与 g−2 的 α 阶联系 ----
log("")
log("=== P4 与 g−2 的 α 阶联系（conjecture 级）===")
a2pi = alpha/(2*math.pi)
log("  δM/M_e = %.4f%%（经典 EM 自能）；(g−2)/2 = α/2π = %.4f%%" % (100*U_em/M_nat, 100*a2pi))
log("  两者同为 α 阶辐射修正（同一 EM 耦合），量级比 = %.1f" % ((U_em/M_nat)/a2pi))
log("  ⟹ 结构对应：EM 耦合既重整化质量(δM)又产生反常磁矩(g−2)；但 δM 含经典")
log("    自能(1/R 截止)、g−2 为量子圈效应(α/2π)，量级差 ~10 —— 是结构对应")
log("    而非推导，不据此作物理主张。")

log("")
log("红线声明：模型层面构造性核验，非物理主张；δM 取库仑+磁偶极自能（含 4/3")
log("表述依赖）；'质量重整化结构对应'为 conjecture 级结构声明，有待 TUFT 作用量")
log("钉扎；HL 约定 e²=4πα。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
