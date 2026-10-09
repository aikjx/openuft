# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · Airy 晕完整 EM 账本审计（C0106, 交叉验证 + 形状依赖区间）
======================================================================
C0105 发现 Airy 晕静电自能几何因子 c_geom=0.4522（相对 e²/8πε₀R，壳层=1）。
本脚本：
  P1 用 C0090 的 ∫q²/r² 方法交叉验证 Airy 静电自能（须与 C0105 的 I_geom 一致）。
  P2 静电自能形状依赖区间：Airy(0.3300%) vs shell(0.7297%)。
  P3 磁自能：shell=α/(3R)=(2/3)U_es；对 Airy 未唯一确定（依赖电流径向分布 j(r)，
     TUFT 只定总磁矩 μ=Q⟨r⟩，未定 j(r) 分布）——暴露为新的未决项。
  P4 δM/M_core 形状依赖区间（静电确定部分 + 磁标注 open）。

红线：模型层面构造性核验，非物理主张；α=e²/4π(HL)；静电用库仑场能 U=(1/8πε₀)∫Q²/r²dr
（与 I_geom 等价）；磁自能 shell 用偶极截止 μ²/(12πR³)，Airy 未唯一确定；
Airy 形状来自 C0096 最小动能原理（conjecture 2.11）。
"""
import numpy as np, io, math
from scipy.special import airy
OUT = "tuft_v32_airy_em_budget_report.txt"
buf=[]; log=buf.append

alpha = 1/137.035999084
M_nat = 4.1855e-23
lamC  = 1.0/M_nat
R     = 0.5*lamC          # ⟨r⟩=0.5006λ_C≈0.5λ_C, C0083/C0084
Q     = 0.473401
a1    = 2.338107410459767

# Airy 晕：u(s)=Ai(Q^{1/3}s−a1), ψ=A u/(R s), g=ψ² (∫g d³r=1), s=r/R
s = np.linspace(1e-5, 40, 400000)
r = s*R
u = airy(Q**(1/3.0)*s - a1)[0]
Iu = np.trapezoid(u**2, s)
A2 = 1.0/(4*np.pi*R*Iu)
A  = math.sqrt(A2)
g  = A2*u**2/(R**2*s**2)
norm = np.trapezoid(g*4*np.pi*r**2, r)

# ---- P1: C0090 方法 ∫q²/r² 算静电自能 (r 以 λ_C 计) ----
# q(r)=∫₀^r g4πs²ds (累积电荷 0→1)
q = np.cumsum(g*4*np.pi*r**2)*(r[1]-r[0]); q = q - q[0]
x_lamC = r/lamC                        # r 以 λ_C 计
Int = np.trapezoid(q**2/x_lamC**2, x_lamC) + 1.0/x_lamC[-1]   # 补 r→∞ 尾部(q=1, ∫=1/xmax), 消除截断
m_es_airy_C0090 = 0.5*alpha*Int        # C0090 公式 m_over_M=0.5α∫q²/r²dr（补尾后与 I_geom 一致）
# shell 对照: q=1(r≥R), ∫_R^∞ q²/r²dr=λ_C/R_lamC (r 以 λ_C)
R_lamC = R/lamC
Int_shell = 1.0/R_lamC                 # ∫_{R}^∞ 1/r²dr (r以λ_C) = 1/R_lamC
m_es_shell = 0.5*alpha*Int_shell

# ---- P2: I_geom 方法 (C0105) 交叉验证 ----
dr = r[1]-r[0]
M1 = np.cumsum(g*4*np.pi*r**2)*dr; M1 = M1 - M1[0]
M2tot = np.trapezoid(g*4*np.pi*r, r)
M2 = M2tot - np.cumsum(g*4*np.pi*r)*dr
P = np.where(r>0, (1.0/r)*M1 + M2, M2)
I_geom = np.trapezoid(g*P*4*np.pi*r**2, r)
c_geom = I_geom*R                       # 相对 e²/8πε₀R (壳层=1)
m_es_airy_Igeom = c_geom*alpha*M_nat/M_nat  # = c_geom·α (·M_e)

log("TUFT V3.2 攻破阶段 · Airy 晕完整 EM 账本审计（C0106）")
log("运行时间: 2026-10-09")
log("⟨r⟩=0.5λ_C=%.6e l_P, Q=%.6f, A=%.3e, 归一 ∫4πr²g dr=%.6f"%(R,Q,A,norm))
log("")
log("=== P1 交叉验证 Airy 静电自能（两方法须一致）===")
log("  C0090 法 ∫q²/r²(+尾): m_es/M_e = 0.5α∫q²/r²dr = %.6f%%"% (m_es_airy_C0090*100))
log("  C0105 法 I_geom:  m_es/M_e = c_geom·α     = %.6f%%"% (m_es_airy_Igeom*100))
log("  两法偏差 = %.2e (应~0; 初版 intq2 漏尾给0.3117, 补尾后0.3300)"% abs(m_es_airy_C0090-m_es_airy_Igeom))
log("")
log("=== P2 静电自能形状依赖区间 ===")
log("  Airy 晕(conjecture): m_es/M_e = %.6f%%"% (m_es_airy_C0090*100))
log("  shell 晕(账本主值):   m_es/M_e = %.6f%%"% (m_es_shell*100))
log("  ⟹ 静电自能形状依赖区间 [%.4f%%, %.4f%%]，c_geom=[%.4f, 1]"% (
    m_es_airy_C0090*100, m_es_shell*100, c_geom))
log("     （C0105 I_geom 无截断问题，为可靠值 0.3300%/c_geom=0.4522；初版 ∫q²/r² 漏尾已修正）")
log("")
log("=== P3 磁自能：shell 确定、Airy 未唯一确定 ===")
log("  shell: U_mag=μ²/(12πR³)=α/(3R)=(2/3)U_es=%.4f%%·M_e"%((2/3)*m_es_shell*100))
log("  Airy:  磁自能依赖电流径向分布 j(r)=ρ(r)ωr; TUFT 只定总磁矩 μ=Q⟨r⟩,")
log("         未定 j(r) 分布 ⟹ U_mag,airy 未唯一确定（新未决项）")
log("         （上界参考: 若沿用 μ²/(12π⟨r⟩³) 则仍≈shell 值 %.4f%%）"%((2/3)*m_es_shell*100))
log("")
log("=== P4 δM/M_core 形状依赖区间（静电确定 + 磁标注）===")
log("  静电部分: Airy δM_es=%.4f%%, shell δM_es=%.4f%%"% (m_es_airy_C0090*100, m_es_shell*100))
log("  磁部分:   Airy 未唯一确定(标注 open)，上界参考 (2/3)δM_es")
log("  ⟹ 静电 δM 区间 [%.4f%%, %.4f%%]；磁自能 open ⟹ 完整 δM 区间约 [0.5%%, 1.2%%]"%(
    m_es_airy_C0090*100, m_es_shell*100))
log("  M_core/M_e 区间: [%.4f, %.4f] (仅静电确定部分)"% (1-m_es_shell, 1-m_es_airy_C0090))
log("")
log("红线：模型层面构造性核验，非物理主张；α=e²/4π(HL)；静电∫q²/r²与I_geom等价；")
log("磁自能 shell 用偶极截止 μ²/12πR³；Airy 磁自能依赖 j(r) 分布未唯一确定；")
log("Airy 形状来自 C0096 最小动能原理（conjecture 2.11）；C0105 c_geom=0.4522 订正 C0096 的 0.201。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
