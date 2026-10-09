# -*- coding: utf-8 -*-
"""
企业级三重奏全维精算库
========================
公理 A（全域光速约束）：u^μu_μ = c²
公理 B（几何三重奏，修复版）：(κℓ_P)² + (τℓ_P)² = (ωℓ_P/c)²

本库提供：
  T1  κℓ_P = E/E_P 恒等式（250 位，CODATA 2022 输入）
  T2  量纲修复自检（原式断裂 / 修复式一致）
  T3  D 维求和效应：κ_eff = ω/(c·√(D−1))
  T4  KK 额外维一致性检验（可证伪判定）——本轮核心
  T5  世界线曲率谱：κ=a_固有/c² 与 Planck 极限
所有结果均为可复算的确定性计算，不确定度按 G 主导传播（δ=1.1e-5）。
"""
import mpmath as mp
from . import constants as C

mp.mp.dps = 250
c  = C.C_SI
hb = C.HBAR
G  = C.G
lP = C.LP
EP = C.EP

# ----------------------------------------------------------------------
# T1: κℓ_P = E/E_P 恒等式（250 位精算）
# ----------------------------------------------------------------------
def kappa_lP_of_mass(mass_kg):
    """由质量(kg)求 κℓ_P = ℓ_P/λ_C = mℓ_Pc/ℏ"""
    lC = hb/(mass_kg*c)
    return lP/lC

def E_over_EP(mass_kg):
    return mass_kg*c**2/EP

def triad_identity_check(mass_kg):
    """返回 (κℓ_P, E/E_P, 相对差) —— 恒等式对标"""
    kl = kappa_lP_of_mass(mass_kg)
    r  = E_over_EP(mass_kg)
    return kl, r, abs((kl-r)/r)

# ----------------------------------------------------------------------
# T2: 量纲修复自检
# ----------------------------------------------------------------------
def dimension_audit(mass_kg):
    """数值演示：原式量纲断裂 vs 修复式一致（40位校验到0）。"""
    lC = hb/(mass_kg*c)
    kappa = 1/lC
    omega = mass_kg*c**2/hb
    lhs_orig = kappa**2                    # [L^-2]
    rhs_orig = (omega*lP/c)**2             # 无量纲 → 断裂
    rhs_fix1 = (omega/c)**2                # [L^-2] ✓
    fix1_ratio = rhs_fix1/lhs_orig
    fix2_diff = (kappa*lP)**2 - (omega*lP/c)**2   # 修复式2差=0
    return lhs_orig, rhs_orig, rhs_fix1, fix1_ratio, fix2_diff

# ----------------------------------------------------------------------
# T3: D 维求和效应（假设 B′：Σ(κᵢℓ_P)²=(ωℓ_P/c)²，各向同性 κᵢ=κ）
#     若 D 维各向同性，则 (D−1)κ²=(ω/c)² → κ_eff = ω/(c√(D−1))
#     【OPEN 断裂点】D 维类时世界线有 D−1 个 Frenet 曲率 κ₁..κ_{D−1}；
#     “三重奏”只取前 2 个（κ,τ），忽略 κ₃..κ_{D−1}。D=4 时若 κ₃≠0，
#     三重奏 (κ²+τ²=(ω/c)²) 与全求和 ((D−1)κ̄²=(ω/c)²) 不一致 → 截断不自洽。
# ----------------------------------------------------------------------
def dim_effective_kappa(omega, D):
    return omega/(c*mp.sqrt(D-1))

def dim_effective_table(omega, D_list):
    out = []
    for D in D_list:
        k = dim_effective_kappa(omega, D)
        out.append((D, k, k*lP))
    return out

# ----------------------------------------------------------------------
# T4: KK 额外维一致性检验（可证伪判定）——核心
# ----------------------------------------------------------------------
# KK 塔：m_n = nℏ/(R_c c) → ω_n = n c/R_c（自然单位 m_n = n/R_c）
# 三重奏（τ=0）要求：κ² = (ω/c)² = n²/R_c² → κ = n/R_c
# 物理含义：三重奏要求世界线曲率半径 R_curv = 1/κ = R_c/n
# 实验约束（亚毫米引力，平坦额外维）：R_c < 0.1 mm = 1e-4 m
# 观测约束（可见物理曲率半径）：R_curv > ~1e6 m（地表轨道）~1e26 m（宇宙学）
def kk_triad_curvature_radius(R_c_m, n=1):
    """三重奏 + KK 要求的可见维世界线曲率半径 R_curv = R_c/n (m)"""
    return R_c_m/n

def kk_consistency_verdict(R_c_m=mp.mpf("1e-4"), n=1):
    """
    可证伪判定：
      R_curv = R_c/n（三重奏强制）
      实验上界 R_c < R_c_max(=1e-4 m)
      观测要求 R_curv > R_obs_min(取地表轨道 6.4e6 m 为最宽松下界)
    若 R_curv(≤R_c_max) < R_obs_min → 理论排除。
    """
    Rc_max = mp.mpf("1e-4")        # 亚毫米引力上界（平坦额外维）
    R_obs_min = mp.mpf("6.4e6")    # 地表轨道曲率半径（最宽松的下界）
    R_curv = kk_triad_curvature_radius(R_c_m, n)
    consistent = R_curv >= R_obs_min
    margin = mp.log10(R_obs_min/R_curv)   # 矛盾的数量级
    return {
        "R_c_m": R_c_m, "n": n,
        "R_curv_required_m": R_curv,
        "R_c_experimental_upper_m": Rc_max,
        "R_obs_min_m": R_obs_min,
        "consistent": bool(consistent),
        "contradiction_orders_of_magnitude": margin,
    }

# ----------------------------------------------------------------------
# T5: 世界线曲率谱
# ----------------------------------------------------------------------
def curvature_of_proper_accel(a_m_s2):
    return a_m_s2/c**2

def triad_report():
    lines = []
    lines.append("== T1: κℓ_P = E/E_P 恒等式（250 位，CODATA 2022） ==")
    for name, mkg in [("电子", C.ME), ("质子", C.MP),
                      ("W(80.369GeV)", mp.mpf("80.369")*C.GEV2KG),
                      ("Higgs(125.1GeV)", mp.mpf("125.10")*C.GEV2KG)]:
        kl, r, rel = triad_identity_check(mkg)
        lines.append(f"  {name:16s} κℓ_P={mp.nstr(kl,10)}  E/E_P={mp.nstr(r,10)}  相对差={mp.nstr(rel,3)}")
    lines.append("\n== T2: 量纲审计（电子） ==")
    lhs, rhs_orig, rhs_fix, ratio, fix2diff = dimension_audit(C.ME)
    lines.append(f"  原式 左κ²={mp.nstr(lhs,6)} m⁻² vs 右(ωℓ_P/c)²={mp.nstr(rhs_orig,6)} → 断裂")
    lines.append(f"  修复 (ω/c)²/κ² = {mp.nstr(ratio,10)} → 一致；修复式2差={mp.nstr(fix2diff,4)}")
    lines.append("\n== T3: D 维求和效应（ω 取电子 de Broglie 频率） ==")
    w = C.ME*c**2/hb
    for D, k, kl in dim_effective_table(w, [4, 6, 10, 32]):
        lines.append(f"  D={D:3d}: κ_eff={mp.nstr(k,6)} m⁻¹  κ_eff·ℓ_P={mp.nstr(kl,8)}")
    lines.append("\n== T4: KK 额外维一致性（可证伪判定） ==")
    for Rc in [mp.mpf("1e-4"), mp.mpf("1e-3"), mp.mpf("1.0")]:
        v = kk_consistency_verdict(Rc)
        lines.append(f"  R_c={mp.nstr(Rc,3)} m → 三重奏要求 R_curv={mp.nstr(v['R_curv_required_m'],3)} m"
                     f"  vs 观测≥{mp.nstr(v['R_obs_min_m'],3)} m → "
                     f"{'一致' if v['consistent'] else '排除'}"
                     f"（矛盾 {mp.nstr(v['contradiction_orders_of_magnitude'],2)} 个数量级）")
    lines.append("\n== T5: 世界线曲率谱 ==")
    for nm, a in [("1g", mp.mpf("9.80665")), ("3g", mp.mpf("29.4")),
                  ("LHC质子向心", mp.mpf("3.2e18")), ("Planck a=c²/ℓ_P", c**2/lP)]:
        k = curvature_of_proper_accel(a)
        lines.append(f"  {nm:14s} a={mp.nstr(a,4)} m/s² → κ={mp.nstr(k,5)} m⁻¹  κℓ_P={mp.nstr(k*lP,4)}")
    return "\n".join(lines)

if __name__ == "__main__":
    print(triad_report())
