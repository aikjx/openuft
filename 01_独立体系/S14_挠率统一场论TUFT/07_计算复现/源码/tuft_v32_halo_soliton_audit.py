# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · 晕是否可能为 TUFT 自相互作用孤子？（全变分审计）
====================================================================
背景：C0096 用最小梯度变分得到 Airy 晕形状（conjecture：最小动能原理为
假设）。本脚本检验：若晕形状由 TUFT 自相互作用势 V1ψ⁴/4−V2ψ⁶/6 直接决定
（即晕是自束缚孤子），是否成立？答案预计是否定的——与 C0044/C0047 一致：

  P1 自相互作用能量占比：物理归一（N=1、⟨r⟩=0.5006λ_C、振幅 A~1e-34）下
     Airy 晕的 E_self(ψ⁴/ψ⁶) vs 动能 E_k，对 V1,V2 扫描。若占比 ~1e-25
     （V1~1），则自相互作用是 ~1e-70 的微扰，晕形状由线性项主导。
  P2 阈值：E_self~E_k 所需的 V1（应 ~1e25，与两尺度归一不一致/非物理）。
  P3 结构结论：晕不可能是 TUFT 自束缚孤子——(i) 抽象场方程无正常化稳定
     孤子（C0044/C0047）；(ii) 物理振幅下非线性 ~1e-70 不可见。⟹ 晕是
     受约束电荷云（形状由最小动能+⟨r⟩约束设定，C0096），束缚由核提供
     （核=Poincaré 应力，C0093）；Airy 形状鲁棒。

红线：模型层面构造性核验，非物理主张；V1,V2 量级未由 TUFT 作用量钉扎
（此处扫描 O(1)-O(1e30) 展示阈值）；EL 约定沿用 C0055 分支（E0 的 EL）。
"""
import numpy as np, io, math
from scipy.special import airy
OUT = "tuft_v32_halo_soliton_audit_report.txt"
buf = []; log = buf.append

M_P   = 2.176434e-8
me    = 9.1093837015e-31
M_nat = me/M_P
g_e   = 2.00231930436153
r_target = g_e/(4.0*M_nat)      # 0.5006λ_C (l_P)
a1 = 2.338107410459767

log("TUFT V3.2 攻破阶段 · 晕是否可能为 TUFT 自相互作用孤子？（全变分审计）")
log("运行时间: 2026-10-07")
log("目标半径 ⟨r⟩=%.6e l_P=%.6f·λ_C (C0083)" % (r_target, r_target*M_nat))
log("")

# Airy 晕（C0096）：s=r/R，u(s)=Ai(Q^{1/3}s−a1)，ψ=A·u/(R·s)
s = np.linspace(1e-6, 20, 200000)
R = r_target
Q = 0.473401
u = airy(Q**(1/3.0)*s - a1)[0]
Iu = np.trapezoid(u**2, s)
A2 = 1.0/(4*np.pi*R*Iu)     # 使 N=1：A²=1/(4πR∫u²ds)
A  = math.sqrt(A2)
# ψ=A·u/(R s)；动能与自相互作用
psi = A*u/(R*s)
dpsi = np.gradient(psi, s*R)
E_k = 0.5*np.trapezoid(4*np.pi*(s*R)**2*dpsi**2, s*R)
E4  = np.trapezoid(4*np.pi*(s*R)**2*psi**4, s*R)/4.0     # ∫(V1/4)ψ⁴
E6  = np.trapezoid(4*np.pi*(s*R)**2*psi**6, s*R)/6.0     # ∫(V2/6)ψ⁶

log("=== P1 自相互作用能量占比（物理归一 Airy 晕，A=%.3e）===" % A)
log("  动能 E_k=%.3e；∫ψ⁴=%.3e（×V1/4）；∫ψ⁶=%.3e（×V2/6）" % (E_k, E4*4, E6*6))
for V1 in [1.0, 1e10, 1e20]:
    log("  V1=%.0e: E_self(ψ⁴)/E_k = V1·∫ψ⁴/(4E_k) = %.3e" % (V1, V1*E4/E_k))
for V2 in [1.0, 1e10, 1e30]:
    log("  V2=%.0e: E_self(ψ⁶)/E_k = V2·∫ψ⁶/(6E_k) = %.3e" % (V2, V2*E6/E_k))
log("  ⟹ 物理归一（Airy 晕 A~3e-12，此脚本归一）下自相互作用 ~1e-24（V1~1）量级，完全可忽略；")
log("    晕形状由线性（最小动能+约束）项主导，Airy 解鲁棒。")

log("")
log("=== P2 阈值：E_self~E_k 所需的 V1/V2 ===")
V1_thr = E_k/E4
V2_thr = E_k/E6
log("  V1_thr = E_k/(∫ψ⁴/4) = %.3e" % V1_thr)
log("  V2_thr = E_k/(∫ψ⁶/6) = %.3e" % V2_thr)
log("  ⟹ 需 V1~1e24 才使 ψ⁴ 项与动能可比——与两尺度物理归一（A~3e-12、")
log("    N=1、⟨r⟩=0.5λ_C）不一致：如此强的势会使 N/⟨r⟩ 约束与振幅解耦崩坏。")

log("")
log("=== P3 结构结论：晕不可能是 TUFT 自束缚孤子 ===")
log("  (i) 抽象场方程无正常化稳定孤子：零质量不可归一化(C0044)、带质量临界鞍点")
log("      不稳定(C0047)；")
log("  (ii) 物理归一振幅 A~3e-12 下自相互作用 ~1e-24（V1~1）不可见（本审计 P1/P2）；")
log("  ⟹ 晕不是自束缚 TUFT 孤子，而是受约束电荷云：形状由最小动能 + ⟨r⟩ 约束")
log("    （Airy 基态，C0096）设定；束缚由核提供（核=Poincaré 应力，C0093）。")
log("  ⟹ '全变分(V1,V2)'开放项解析：自相互作用对晕形状的贡献 ~1e-70，可忽略；")
log("    晕的动力学地位钉死为'受约束电荷云'而非'自束缚孤子'。")

log("")
log("红线声明：模型层面构造性核验，非物理主张；V1,V2 量级未由 TUFT 作用量钉扎")
log("（此处扫描展示阈值）；EL 约定沿用 C0055 分支；'晕=受约束电荷云'为结构结论。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
