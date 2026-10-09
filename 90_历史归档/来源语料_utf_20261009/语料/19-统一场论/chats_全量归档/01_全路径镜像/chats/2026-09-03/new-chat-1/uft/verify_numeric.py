# -*- coding: utf-8 -*-
"""
verify_numeric.py —— 统一场论数值对标（mpmath 高精度）
  N1 量纲分析（全维度 D 维质量量纲表）
  N2 电弱统一数值：v、sin^2 theta_W、m_W、m_Z 自洽
  N3 RG 耦合汇合：SM vs MSSM（精确数值 + 偏差量化）
  N4 质子衰变寿命 vs Super-K（最小 SU(5) 排除、SUSY-SU(5) 兼容）
  N5 跷跷板机制：m_nu
  N6 KK 约化：M_Pl 关系、TeV 额外维排除
  N7 LQG 面积算符谱
"""
import mpmath as mp

mp.mp.dps = 50
Gev = 1.0

# =====================================================================
print("=" * 74)
print("N1：量纲分析（D 维质量量纲，自然单位 hbar=c=1）")
# 约定 [x]=-1, [d^D x]=-D, 作用量无量纲 [S]=0, 故 [L]=D
D = mp.mpf(4)
dims = {
    "R (Ricci 标量)": 2,
    "g_munu": 0,
    "kappa_D^2 (8pi G_D)": 2 - D,
    "F_munu": 2,
    "A_mu": 1,
    "g (规范耦合, D维)": (4 - D) / 2,
    "psi": (D - 1) / 2,
    "Phi (标量)": (D - 2) / 2,
    "y (Yukawa)": (4 - D) / 2,
    "lambda (phi^4)": 4 - D,
    "V(Phi) 势能": D,
}
print(f"D = {D} 维时：")
for k, v in dims.items():
    print(f"  [{k}] = {v}")
print("  说明：D=4 时 g, y, lambda 均无量纲（可重整）；D≠4 时均有质量量纲。")
print("  D=4 时 phi^4 为边缘算符（上临界维=4）；phi^6 在 D=3 边缘。")

# =====================================================================
print("=" * 74)
print("N2：电弱统一数值对标（PDG 2024 常数）")
GF = mp.mpf("1.1663788e-5")     # 费米常数 [GeV^-2]
v = 1 / mp.sqrt(mp.sqrt(2) * GF)  # v = (sqrt2 GF)^(-1/2)
print(f"v = (√2 G_F)^(-1/2) = {mp.nstr(v, 20)} GeV  (期望 ~246.22)")
alpha_em = 1 / mp.mpf("127.9")
sin2th = mp.mpf("0.23122")
alpha_2 = alpha_em / sin2th
alpha_1_sm = alpha_em / (1 - sin2th)
g = mp.sqrt(4 * mp.pi * alpha_2)
mW_pred = g * v / 2
mZ_pred = mW_pred / mp.sqrt(1 - sin2th)
print(f"α_em(M_Z)^-1 = {mp.nstr(1/alpha_em, 8)}, sin²θ_W = {mp.nstr(sin2th, 8)}")
print(f"α_2 = {mp.nstr(alpha_2, 8)}, g = {mp.nstr(g, 8)}")
print(f"m_W = g v/2 = {mp.nstr(mW_pred, 8)} GeV  (实验 80.369 ± 0.013)")
print(f"m_Z = m_W/cosθ_W = {mp.nstr(mZ_pred, 8)} GeV  (实验 91.188)")
print(f"m_W/m_Z = cosθ_W = {mp.nstr(mW_pred/mZ_pred, 10)}，cosθ_W = {mp.nstr(mp.sqrt(1-sin2th), 10)}")
print(f"→ 量级与实验吻合（精细阈值为 10^-3 级修正）")

# =====================================================================
print("=" * 74)
print("N3：RG 耦合汇合 —— SM vs MSSM")
MZ = mp.mpf("91.1876")
alpha3_inv = 1 / mp.mpf("0.1179")
a1i, a2i, a3i = (3/5) * (1 - sin2th) / alpha_em, sin2th / alpha_em, alpha3_inv
print(f"M_Z 处初值：α1^-1={mp.nstr(a1i,8)} α2^-1={mp.nstr(a2i,8)} α3^-1={mp.nstr(a3i,8)}")


def run_rg(b, m_start=MZ, a_start=None, m_susy=None, n=200000):
    """数值积分 dαi^-1/dt = -b_i/2π，t=ln(mu/MZ)。返回 mu、[αi^-1]。"""
    import mpmath as mp2
    if a_start is None:
        a_start = [a1i, a2i, a3i]
    a = [mp2.mpf(x) for x in a_start]
    ms = [mp2.mpf(m_start)]
    al = [[mp2.mpf(x) for x in a]]
    # 用大步长解析式（单圈可解析）：alpha^-1(mu) = alpha^-1(m0) - b/(2pi) ln(mu/m0)
    return a  # 占位


# 单圈可解析，直接算：
def alpha_inv_at(mu, b, a_inv0):
    t = mp.log(mu / MZ) / (2 * mp.pi)
    return [a_inv0[i] - b[i] * t for i in range(3)]


def find_cross(b, i, j, lo, hi, a_inv0):
    """二分求 alpha_i^-1 == alpha_j^-1 的 mu"""
    f = lambda m: (alpha_inv_at(m, b, a_inv0)[i] - alpha_inv_at(m, b, a_inv0)[j])
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) * f(lo) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ---- SM（b = 41/10, -19/6, -7）----
bSM = [mp.mpf("41/10"), mp.mpf("-19/6"), mp.mpf("-7")]
a0 = [a1i, a2i, a3i]
mu12 = find_cross(bSM, 0, 1, MZ, mp.mpf("1e30"), a0)
if mu12:
    a12 = alpha_inv_at(mu12, bSM, [a1i, a2i, a3i])
    dev = abs(a12[2] - a12[0]) / a12[0]
    print(f"\n[SM] α1^-1=α2^-1 交叉点 μ = {mp.nstr(mp.log10(mu12), 5)} (10^{mp.nstr(mp.log10(mu12),4)} GeV)")
    print(f"[SM] 该处 α1^-1=α2^-1={mp.nstr(a12[0],6)}，α3^-1={mp.nstr(a12[2],6)}")
    print(f"[SM] α3 偏离相对量 = {mp.nstr(dev*100,5)}%  (文档称 2-3%)")
# 三线最近距离（扫描）
best = (None, 1e99)
for p in range(60, 320):
    mu_ = MZ * mp.mpf(10) ** (p / 10)
    a = alpha_inv_at(mu_, bSM, [a1i, a2i, a3i])
    spread = max(a) - min(a)
    if spread < best[1]:
        best = (mu_, spread)
print(f"[SM] 三线最近点：μ≈10^{mp.nstr(mp.log10(best[0]),4)} GeV，α^-1 极差={mp.nstr(best[1],5)}"
      f"（相对 {mp.nstr(best[1]/mp.mpf(40)*100,4)}%）")

# ---- MSSM（b = 33/5, 1, -3），M_SUSY 以上用 MSSM β----
bMS = [mp.mpf("33/5"), mp.mpf("1"), mp.mpf("-3")]


def alpha_inv_at2(mu, b, a_inv0, m0):
    t = mp.log(mu / m0) / (2 * mp.pi)
    return [a_inv0[i] - b[i] * t for i in range(3)]


def find_cross2(b, i, j, lo, hi, a_inv0, m0):
    f = lambda m: alpha_inv_at2(m, b, a_inv0, m0)[i] - alpha_inv_at2(m, b, a_inv0, m0)[j]
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) * f(lo) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


for MSUSY in [mp.mpf("1000"), mp.mpf("2000")]:
    a_at_susy = alpha_inv_at(MSUSY, bSM, a0)
    print(f"\n[MSSM] M_SUSY={mp.nstr(MSUSY,5)} GeV 处（SM 跑到此）初值："
          f"α1^-1={mp.nstr(a_at_susy[0],6)} α2^-1={mp.nstr(a_at_susy[1],6)} α3^-1={mp.nstr(a_at_susy[2],6)}")
    muG = find_cross2(bMS, 0, 2, MSUSY, mp.mpf("1e30"), a_at_susy, MSUSY)
    muG12 = find_cross2(bMS, 0, 1, MSUSY, mp.mpf("1e30"), a_at_susy, MSUSY)
    aG = alpha_inv_at2(muG, bMS, a_at_susy, MSUSY)
    aG12 = alpha_inv_at2(muG12, bMS, a_at_susy, MSUSY)
    dev2 = abs(aG[1] - aG[0]) / aG[0] * 100
    print(f"[MSSM] α1^-1=α3^-1 交叉点 M_GUT ≈ 10^{mp.nstr(mp.log10(muG),4)} GeV = "
          f"{mp.nstr(muG,4)} GeV")
    print(f"[MSSM] 该处 α1^-1=α3^-1={mp.nstr(aG[0],6)}, α2^-1={mp.nstr(aG[1],6)}"
          f"（α2 相对偏离 {mp.nstr(dev2,4)}%）→ α_GUT^-1≈{mp.nstr(aG[0],5)}")
    print(f"[MSSM] α1^-1=α2^-1 交叉点 μ = 10^{mp.nstr(mp.log10(muG12),4)} GeV，"
          f"α^-1={mp.nstr(aG12[0],5)}")
print("\n说明：M_GUT 与 α_GUT^-1 数值对 α_s、sin²θ_W、M_SUSY、阈值修正敏感，")
print("     文档所引 2×10^16 GeV / α_GUT^-1≈24 在输入合理范围内。")

# =====================================================================
print("=" * 74)
print("N4：质子衰变寿命 vs Super-K（最小 SU(5) 排除、SUSY-SU(5) 兼容）")
# 量级估计：Gamma ~ alpha_GUT^2 m_p (m_p/M_X)^4，tau=1/Gamma
hGeVs = mp.mpf("6.582119569e-25")  # hbar [GeV·s]
yr = mp.mpf("3.15576e7")
mp_p = mp.mpf("0.938272")


def tau_p_years(MX, aG):
    G = aG**2 / (4 * mp.pi) * mp_p * (mp_p / MX)**4
    return (1 / G) * hGeVs / yr


print("M_X [GeV]      α_GUT       τ_p [年]          vs SK 2.4e34")
for MX, aG, label in [(mp.mpf("1e14"), 1 / mp.mpf("40"), "最小SU(5)"),
                      (mp.mpf("1e15"), 1 / mp.mpf("40"), "最小SU(5)"),
                      (mp.mpf("2e16"), 1 / mp.mpf("24"), "SUSY-SU(5)")]:
    tp = tau_p_years(MX, aG)
    verdict = "被 SK 排除" if tp < mp.mpf("2.4e34") else "与 SK 兼容"
    print(f"{mp.nstr(MX,4):>12} {mp.nstr(aG,8)}  {mp.nstr(tp,5)}   {verdict} ({label})")
print("注：上式为量级估计，hadron 矩阵元可带来 O(1-10^2) 修正；")
print("    文献一致结论：最小非超对称 SU(5) 预言 τ_p≲10^34 yr → 被 Super-K 排除；")
print("    SUSY-SU(5)（M_X~2×10^16 GeV）预言 τ_p~10^34-10^36 yr → 仍存活。")

# =====================================================================
print("=" * 74)
print("N5：跷跷板机制（SO(10) 右手中微子）")
mD = mp.mpf("100")   # GeV
MR = mp.mpf("1e14")  # GeV
mn = mD**2 / MR
print(f"m_ν = m_D²/M_R = {mp.nstr(mD,4)}²/{mp.nstr(MR,4)} = {mp.nstr(mn,8)} GeV = {mp.nstr(mn*1e9,6)} eV")
print(f"  → ~0.1 eV，与大气中微子 √Δm²_32 ≈ 0.0496 eV 同量级")
am32 = mp.sqrt(mp.mpf("2.46e-3"))
print(f"  √Δm²_32 = {mp.nstr(am32,5)} eV")

# =====================================================================
print("=" * 74)
print("N6：KK 约化 —— M_Pl 关系与 TeV 额外维排除")
MPl = mp.mpf("1.2209e19")  # Planck 质量 [GeV]
MPl2 = MPl**2


def R_from_M5(M5):
    return MPl2 / (2 * mp.pi * M5**3)


print("若 M_5 = 1 TeV：R = M_Pl²/(2πM_5³) =",
      mp.nstr(R_from_M5(mp.mpf("1e3")), 5), "GeV^-1 =",
      mp.nstr(R_from_M5(mp.mpf("1e3")) * mp.mpf("1.97327e-16"), 5), "m ≈",
      mp.nstr(R_from_M5(mp.mpf("1e3")) * mp.mpf("1.97327e-16") / mp.mpf("1.496e11"), 5), "AU")
# 由 R 反推 M_5
for R_mm in ["1", "0.1", "0.03"]:
    R_g = mp.mpf(R_mm) * mp.mpf("1e-3") / mp.mpf("1.97327e-16")  # m -> GeV^-1
    M5 = (MPl2 / (2 * mp.pi * R_g)) ** (1 / mp.mpf("3"))
    print(f"R = {R_mm} mm → M_5 ≥ {mp.nstr(M5,5)} GeV（亚毫米引力实验排除更大 R）")

# =====================================================================
print("=" * 74)
print("N7：LQG 面积算符谱 Â = 8πγℓ_P² Σ√(j(j+1))")
lP = mp.mpf("1.616255e-35")  # m
lP2 = lP**2
gamma_bi = mp.mpf("0.2375")  # Barbero-Immirzi（j=1/2 定标）
for j in ["1/2", "1", "3/2"]:
    jj = mp.mpf(j)
    A = 8 * mp.pi * gamma_bi * lP2 * mp.sqrt(jj * (jj + 1))
    print(f"j = {j}: Â = {mp.nstr(A,6)} m² = {mp.nstr(A/lP2,6)} ℓ_P²")

print("\n数值对标完成。")
