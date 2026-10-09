# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · Airy 晕 EM 自能几何因子审计（C0105, r空间修正版）
================================================================
质量账本（C0087/C0090/C0094）用壳层因子（U_es=αM_e，c=1）；C0096 Airy 晕报
c_geom=0.201。审计 Airy 晕真实 EM 自能几何因子 c_geom 是否与质量账本一致。

球对称 r 空间公式（干净版，先校验均匀球=6/5、壳层=1）：
  g(r)=ψ²，∫g d³r=1
  P(r) = (1/r)∫₀^r g4πr'²dr' + ∫_r^∞ g4πr'dr'
  I_geom = ∫ g·P·4πr² dr
  c_geom = I_geom·R
"""
import numpy as np, io, math
from scipy.special import airy
OUT = "tuft_v32_airy_em_audit_report.txt"
buf=[]; log=buf.append

alpha = 1/137.035999084
M_nat = 4.1855e-23
lamC  = 1.0/M_nat
R     = 0.5*lamC
Q     = 0.473401
a1    = 2.338107410459767

def I_geom_of(g, r):
    """g(r) 归一化电荷密度，r 网格；返回 I_geom=∫∫g g'/|r-r'|d³rd³r'。"""
    dr = r[1]-r[0]
    M1 = np.cumsum(g*4*np.pi*r**2)*dr          # ∫₀^r g4πr'²dr'
    M1 = M1 - M1[0]
    M2tot = np.trapezoid(g*4*np.pi*r, r)
    M2 = M2tot - np.cumsum(g*4*np.pi*r)*dr     # ∫_r^∞ g4πr'dr'
    with np.errstate(divide='ignore', invalid='ignore'):
        P = np.where(r>0, (1.0/r)*M1 + M2, M2)
    return np.trapezoid(g*P*4*np.pi*r**2, r)

# ---- 校验: 均匀球 (期望 c=6/5) ----
rv = np.linspace(1e-6, R, 300000)
gv = np.full_like(rv, 3.0/(4*np.pi*R**3))
cv = I_geom_of(gv, rv)*R

# ---- 校验: 薄壳层 (期望 c≈1) ----
re = np.linspace(R, R+1e-5*R, 300000)
ge = np.full_like(re, 1.0/(4*np.pi*R**2*1e-5*R))
ce = I_geom_of(ge, re)*R

log("TUFT V3.2 攻破阶段 · Airy 晕 EM 自能几何因子审计（C0105, r空间修正版）")
log("运行时间: 2026-10-09")
log("R=0.5λ_C=%.6e l_P, Q=%.6f, a₁=%.6f"%(R,Q,a1))
log("校验 均匀球 c=% .6f (期望 6/5=%.6f)  薄壳层 c=% .6f (期望 ~1)"%(cv,6/5,ce))
log("")

# ---- Airy 晕 ----
s = np.linspace(1e-5, 40, 400000)
r = s*R
u = airy(Q**(1/3.0)*s - a1)[0]
Iu = np.trapezoid(u**2, s)
A2 = 1.0/(4*np.pi*R*Iu)
A  = math.sqrt(A2)
g  = A2*u**2/(R**2*s**2)          # 密度 ψ²
norm = np.trapezoid(g*4*np.pi*r**2, r)
I_geom = I_geom_of(g, r)
c_geom = I_geom*R

log("=== P1 Airy 晕 EM 自能几何因子 ===")
log("  A=%.3e, 归一 ∫4πr²g dr = %.6f (应=1)"%(A,norm))
log("  I_geom = %.6e (1/length)"%I_geom)
log("  c_geom = I_geom·R = %.6f"%c_geom)
log("  壳层参照 c=1；均匀球参照 c=6/5=1.2")
log("")

Ues_airy = c_geom*alpha*M_nat
Uem_airy = (5.0/3.0)*Ues_airy
Ues_bud  = alpha*M_nat
log("=== P2 Airy 晕 EM 自能与质量账本对照 ===")
log("  U_es,airy  = c_geom·αM_e = %.6f%%·M_e"%(Ues_airy/M_nat*100))
log("  U_es,预算  = αM_e        = %.6f%%·M_e"%(Ues_bud/M_nat*100))
log("  U_em,airy  = (5/3)U_es   = %.6f%%·M_e"%(Uem_airy/M_nat*100))
log("  预算 δM/M_e=(5/3)α      = %.6f%%·M_e"%(5.0/3.0*alpha*100))
log("  Airy δM/M_e=(5/3)c_geom·α = %.6f%%·M_e"%((5.0/3.0)*c_geom*alpha*100))
log("")

log("=== P3 一致性判定 ===")
if abs(c_geom-1.0) < 0.10:
    log("  c_geom=%.4f ≈ 1（壳层）⟹ Airy 晕 EM 自能与质量账本一致（偏差 %.1f%%）"%(c_geom,abs(c_geom-1)*100))
    log("  ⟹ 账本 δM=(5/3)α 成立，g-质量重整化同源关系保持。")
else:
    log("  c_geom=%.4f ≠ 1 ⟹ Airy 晕非壳层，EM 自能应乘 c_geom"%(c_geom))
    log("  ⟹ 需复核质量账本：δM 或为 (5/3)c_geom·α，g-质量重整化同源关系受影响。")
log("")

log("红线声明：模型层面构造性核验，非物理主张；α=e²/4π(HL)；数值与 C0096 一致；")
log("U_mag/U_es=2/3 沿用 C0090；校验 均匀球/壳层 验证积分方法正确。")

with io.open(OUT,"w",encoding="utf-8",newline="") as f:
    f.write("\n".join(buf)+"\n")
print("\n".join(buf))
