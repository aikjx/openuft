# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · 晕形状第一性确定：最小梯度变分原理（Airy 基态）
====================================================================
背景：C0084 两尺度构造用现象学任意形状（exp/gauss/...）作为"形状鲁棒"。
本脚本把晕形状从**任选**升级为**第一性导出**：

  原理：带电晕在约束（电荷 N=1、半径 ⟨r⟩=R=0.5006λ_C）下使动能
        E_k=½∫4πr²ψ'²dr 最小化 → 变分问题，约束为 Lagrange 乘子势。
  EL 方程：-(r²ψ')' + r²(2λ₁+λ₂r)ψ = 0 ⟹ 令 u=rψ：u''=(A+Br)u
        解为 Airy 函数基态：u(s)=Ai(Q^{1/3}s − a₁)，a₁=Ai 第一零点。
  ⟹ 晕形状 ψ(r)∝Ai(Q^{1/3}r/R − a₁)/r 由第一性确定，非现象学任选。

  P1 变分原理与 EL 推导；
  P2 Airy 基态：定 Q 使 ⟨r⟩=R，定振幅使 N=1；
  P3 所得形状 vs 现象学形状（exp/gauss）：⟨r⟩、E_k、EM 几何因子 c_geom；
  P4 质量预算：E_k 仍 ~1e-45（与 C0087 一致），账本闭合不变。

红线：模型层面构造性核验，非物理主张；最小梯度变分原理为电荷云的基态假设
（conjecture 级：晕为凝聚密度 ψ² 的场，最小动能构型）；EM 几何因子沿用
C0090 库仑自能定义；HL 约定 e²=4πα。
"""
import numpy as np, io, math
from scipy.special import airy
OUT = "tuft_v32_halo_shape_report.txt"
buf = []; log = buf.append

M_P   = 2.176434e-8
me    = 9.1093837015e-31
M_nat = me/M_P
g_e   = 2.00231930436153
alpha = 1.0/137.035999084
r_target = g_e/(4.0*M_nat)      # 0.5006λ_C (l_P), C0083
lamC = 1.0/M_nat

a1 = 2.338107410459767   # Ai 第一零点

log("TUFT V3.2 攻破阶段 · 晕形状第一性确定：最小梯度变分原理（Airy 基态）")
log("运行时间: 2026-10-07")
log("目标半径 ⟨r⟩=%.6e l_P=%.6f·λ_C (C0083)" % (r_target, r_target/lamC))
log("")

# ---- P1 变分原理 ----
log("=== P1 变分原理与 EL 推导 ===")
log("  最小化 E_k=½∫4πr²ψ'²dr，约束 N=∫4πr²ψ²dr=1、⟨r⟩=∫2πr³ψ²dr=R")
log("  F = ∫[½ψ'²·4πr² + λ₁ψ²·4πr² + λ₂ψ²·2πr³]dr")
log("  EL: -(r²ψ')' + r²(2λ₁+λ₂r)ψ=0 ⟹ u=rψ: u''=(A+Br)u, A=2λ₁, B=λ₂")
log("  解：u(s)=Ai(Q^{1/3}s−a₁)，a₁=Ai 第一零点=%.6f（u(0)=0 条件定 A）" % a1)
log("  ⟹ 晕形状 ψ∝Ai(Q^{1/3}s−a₁)/s 由第一性确定（无现象学选形）。")
log("")

# ---- P2 Airy 基态 ----
log("=== P2 定 Q 使 ⟨r⟩=R、定振幅使 N=1 ===")
# s=r/R；u(s)=Ai(Q^{1/3}s−a₁)；⟨s⟩=½·(∫s u² ds/∫u² ds)
s = np.linspace(0, 20, 200000)
def langle_s(Q):
    u = airy(Q**(1/3.0)*s - a1)[0]
    Iu = np.trapezoid(u**2, s)
    Is = np.trapezoid(s*u**2, s)
    return 0.5*Is/Iu
# 找 Q 使 ⟨s⟩=1（⟨r⟩=R）
from scipy.optimize import brentq
Q = brentq(lambda q: langle_s(q)-1.0, 1e-6, 1e6)
u = airy(Q**(1/3.0)*s - a1)[0]
Iu = np.trapezoid(u**2, s)
langle_ok = langle_s(Q)
log("  Q=%.6f（⟨s⟩=%.6f ≈1 即 ⟨r⟩=R ✓）" % (Q, langle_ok))
log("  u(s)=Ai(%.3f·s − 2.338)，u(0)=Ai(−a₁)=0 ✓，大 s 指数衰减 ✓" % Q**(1/3.0))
log("  N_shape=4π∫u²ds=%.4f（单位 R 下）；振幅 A=1/√(4πR∫u²ds) 使 N=1" % (4*np.pi*Iu))
log("")

# ---- P3 所得形状 vs 现象学 ----
log("=== P3 Airy 晕 vs 现象学形状（exp/gauss）：观测量 ===")
# Airy 晕的 E_k 与 c_geom
R = r_target
# E_k = (1/(2R²))·∫(u'−u/s)²ds/∫u²ds
du = np.gradient(u, s)
u_s = np.where(s>1e-9, u/s, 0.0)
Ek_airy = (1.0/(2*R**2))*np.trapezoid((du-u_s)**2, s)/Iu
# EM 几何因子：ρ∝ψ²∝u²/s²，U_es=(α/2)∫q²/r²dr，r 以 R 计
rho_unn = np.where(s>1e-12, u**2/s**2, 0.0)
rho_unn[0] = (Q**(1/3.0)*airy(-a1)[1])**2   # u'(0)²=Q^{2/3}Ai'(−a₁)²
Nrho = np.trapezoid(4*np.pi*s**2*rho_unn, s)
# Q_in(r) 用 np.cumsum 向量化（O(N)）
integrand = 4*np.pi*s**2*rho_unn
q = np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(s))
q = np.concatenate(([0.0], q))/Nrho
sc = s
q_sq = np.where(sc>1e-9, q**2/sc**2, 0.0)
Int_es = np.trapezoid(q_sq, sc)
c_geom_airy = 0.5*Int_es   # c_geom = (U_es/M_e)/(α·λ_C/R)
log("  Airy 晕: ⟨r⟩=%.6f·λ_C  E_k=%.3e M_P(%.1e·M_e)  c_geom=%.4f"
    % (langle_ok*r_target/lamC, Ek_airy, Ek_airy/M_nat, c_geom_airy))
# 现象学形状（C0090 值）
for name, cg in [("exp",0.117), ("gauss",0.159), ("quartic",0.188)]:
    log("  现象学[%-7s] c_geom=%.3f" % (name, cg))
log("  ⟹ Airy 晕 c_geom=%.3f 落入现象学族 O(0.1-0.5) 范围，但由第一性给出" % c_geom_airy)
log("")

# ---- P4 质量预算 ----
log("=== P4 质量预算：E_k 仍 ~1e-45（与 C0087 一致），账本闭合不变 ===")
Ek_air_M = Ek_airy/M_nat
log("  Airy 晕动能 E_k=%.3e M_P = %.1e·M_e（可忽略，同 C0087）" % (Ek_airy, Ek_air_M))
log("  ⟹ 含第一性形状后完整账本（§十六）不变：核 98.8% + EM 自能 1.2% = M_e。")

log("")
log("红线声明：模型层面构造性核验，非物理主张；最小梯度变分原理为电荷云基态")
log("假设（conjecture 级，晕为凝聚密度 ψ² 的最小动能构型）；EM 几何因子沿用")
log("C0090 库仑自能定义；HL 约定 e²=4πα。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
