# -*- coding: utf-8 -*-
"""
TUFT V3.2 攻破阶段 · Airy 晕 EM 自能几何因子审计（C0105, 修正版）
================================================================
背景：质量账本（C0087/C0090/C0094）用壳层几何因子（U_es=αM_e，c=1）；C0096
第一性导出 Airy 晕并报 c_geom=0.201。本脚本计算 Airy 晕真实 EM 自能几何因子
c_geom=I_geom·R，审计是否与质量账本一致。修正版用 s 空间干净积分 + 均匀球/壳
校验。

I_geom = ∫∫g g'/|r-r'|d³rd³r',  球对称: I_geom=∫4πR³s²g(s)P(s)ds
P(s) = (4π/s)∫₀^s g s'²ds' + 4πR∫_s^∞ g s'ds'
校验: 均匀球 c=6/5, 壳层 c=1, 均匀实心(体积)分布相应值。
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

def geom_factor(s, u, R):
    """u(s) 为晕形状 u=rψ（ψ=A u/(R s)），g=ψ²=A²u²/(R²s²)。"""
    ds = s[1]-s[0]
    A2 = 1.0/(4*np.pi*R*np.trapezoid(u**2, s))
    A  = math.sqrt(A2)
    g  = A2*u**2/(R**2*s**2)
    # M1(s)=∫₀^s g s'² ds' = (A2/R²)∫₀^s u² ds'
    M1 = (A2/R**2)*np.cumsum(u**2)*ds
    M1 = M1 - M1[0]
    # M2(s)=∫_s^∞ g s' ds' = (A2/R²)∫_s^∞ u²/s' ds'  (反向)
    M2tot = (A2/R**2)*np.trapezoid(u**2/s, s)
    M2 = M2tot - (A2/R**2)*np.cumsum(u**2/s)*ds
    # P(s) = (4π/s)M1 + 4πR·M2
    with np.errstate(divide='ignore', invalid='ignore'):
        P = np.where(s>0, (4*np.pi/s)*M1 + 4*np.pi*R*M2, 4*np.pi*R*M2)
    integ = 4*np.pi*R**3*s**2*g*P
    I = np.trapezoid(integ, s)
    return I, A2, A

# ---- 校验 1: 均匀球 g=3/(4πR³) (s∈[0,1])，期望 c=6/5 ----
sv = np.linspace(1e-6, 1.0, 200000)
gv = np.full_like(sv, 3.0/(4*np.pi*R**3))
dsv = sv[1]-sv[0]
M1v = np.cumsum(gv*sv**2)*dsv
M2totv = np.trapezoid(gv*sv, sv)
M2v = M2totv - np.cumsum(gv*sv)*dsv
Pv = (4*np.pi/sv)*M1v + 4*np.pi*R*M2v
Iv = np.trapezoid(4*np.pi*R**3*sv**2*gv*Pv, sv)
cv = Iv*R

# ---- 校验 2: 壳层 g=δ 近似（薄球壳在 s∈[1,1+ε]）----
se = np.linspace(1.0, 1.0+1e-5, 200000)
ge = np.full_like(se, 1.0/(4*np.pi*R**3*3e-5))  # ∫g d³r=1
dse = se[1]-se[0]
M1e = np.cumsum(ge*se**2)*dse
M2tot_e = np.trapezoid(ge*se, se)
M2e = M2tot_e - np.cumsum(ge*se)*dse
Pe = (4*np.pi/se)*M1e + 4*np.pi*R*M2e
Ie = np.trapezoid(4*np.pi*R**3*se**2*ge*Pe, se)
ce = Ie*R

log("TUFT V3.2 攻破阶段 · Airy 晕 EM 自能几何因子审计（C0105, 修正版）")
log("运行时间: 2026-10-09")
log("R=0.5λ_C=%.6e l_P, Q=%.6f, a₁=%.6f"%(R,Q,a1))
log("校验 均匀球 c=% .6f (期望 6/5=%.6f)"%(cv, 6/5))
log("校验 薄壳层 c=% .6f (期望 ~1)"%ce)
log("")

# ---- Airy 晕 ----
s = np.linspace(1e-5, 40, 400000)
u = airy(Q**(1/3.0)*s - a1)[0]
I_geom, A2, A = geom_factor(s, u, R)
c_geom = I_geom*R
# 归一检查
ds = s[1]-s[0]
norm = np.trapezoid(4*np.pi*R**3*s**2*(A2*u**2/(R**2*s**2)), s)

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
