"""
uft_essence_numerics.py
=======================
本质本源精算：黑洞熵、真空能差距、Dirac量子化、黑洞蒸发、自旋统计
mpmath 250 位
"""
import json, os, sys
TAG_NAME = "72_essence"
HERE = os.path.dirname(os.path.abspath(__file__))
# Windows GBK 控制台下 ²/⁴ 等上标字符会抛 UnicodeEncodeError ⇒ 强制 UTF-8 输出
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
from mpmath import mp, mpf, pi, sqrt, exp, log

mp.dps = 250

# 基础常数
c    = mpf('299792458')
hbar = mpf('1.054571817e-34')
G    = mpf('6.67430e-11')
k_B  = mpf('1.380649e-23')
e    = mpf('1.602176634e-19')
sigma_SB = mpf('5.670374419e-8')  # Stefan-Boltzmann W/m²/K⁴

# Planck 量
l_P = sqrt(hbar*G/c**3)
m_P = sqrt(hbar*c/G)
t_P = sqrt(hbar*G/c**5)
rho_P = c**5/(hbar*G**2)  # Planck 能量密度 J/m³

# ============================================================
# E1: Bekenstein-Hawking 黑洞熵
# S_BH = k_B A / (4 l_P²)
# 太阳质量黑洞
# ============================================================
M_sun = mpf('1.98847e30')
r_s_sun = 2*G*M_sun/c**2
A_sun = 4*pi*r_s_sun**2
S_BH_sun = k_B * A_sun / (4*l_P**2)  # J/K
# 熵的无量纲形式（除以 k_B）
S_BH_sun_over_kB = S_BH_sun/k_B

# ============================================================
# E2: 真空能密度：理论 vs 观测
# 理论（截断到 Planck）: ρ_theory ~ M_P^4 c^3 / (ħ)^3 ... 实际是
#   ρ_QFT ~ (E_P)^4 / (ħ c)^3
# 观测（ΛCDM）: ρ_obs ≈ 0.689 * 3 H0² c²/(8πG)
# ============================================================
rho_theory = c**7/(hbar*G**2)  # Planck 能量密度 J/m³ (正确公式)

H0 = mpf('67.66')*1000/(mpf('3.0857e22'))  # s^-1
Omega_L = mpf('0.6889')
rho_obs = Omega_L * 3*H0**2*c**2/(8*pi*G)  # J/m³

ratio_rho = rho_theory/rho_obs
log10_ratio = float(log(ratio_rho)/log(10))

# ============================================================
# E3: Dirac 电荷量子化条件
# eg = n ħ c / 2
# 即 e g / (4π ε0) = n ħ c / 2 ... 用 Gaussian 单位简化
# ============================================================
# 高斯单位下：e g = n ħ c / 2
# 所以磁单极荷 g = n ħ c / (2e)
# 狄拉克量子数 n=1 时
hbar_c_GeV_m = 1.  # 在自然单位下直接写
# 我们算 g/e 比值（Dirac 量子化预言 g/e ≈ 68.5）
alpha = mpf('7.2973525693e-3')
g_over_e_Dirac = 1/(2*alpha)  # n=1

# ============================================================
# E4: Hawking 温度
# T_H = ħ c³ / (8π G M k_B)
# ============================================================
def T_Hawking(M):
    return hbar*c**3/(8*pi*G*M*k_B)

T_sun_BH = T_Hawking(M_sun)  # K

# ============================================================
# E5: 黑洞蒸发时间
# t_evap ~ 5120 π G² M³ / (ħ c⁴)
# ============================================================
def t_evap(M):
    return 5120*pi*G**2*M**3/(hbar*c**4)

t_evap_sun_yr = t_evap(M_sun)/(365.25*24*3600)
# 银河系质量黑洞 ~ 1e12 M_sun
t_evap_galaxy_yr = t_evap(mpf('1e12')*M_sun)/(365.25*24*3600)
# 1 kg 微型黑洞
t_evap_1kg_s = t_evap(mpf('1'))

# ============================================================
# E6: 黑洞熵与恒星熵对比
# 太阳的标准热熵 ~ 10^35 J/K
# 太阳黑洞熵 ~ 10^77 k_B
# ============================================================
S_sun_thermal = mpf('1e35')  # J/K, 数量级估计
ratio_entropy = S_BH_sun/S_sun_thermal

# ============================================================
# E7: 量子引力能标与 LHC 的差距
# LHC 质子束能量 ~ 7 TeV, 质心 ~ 14 TeV
# Planck ~ 1.22e19 GeV
# ============================================================
E_LHC_TeV = mpf('14000')  # GeV = 14 TeV
E_P_GeV = m_P*c**2/e/1e9
gap_LHC_to_P = float(log(E_P_GeV/E_LHC_TeV)/log(10))

# ============================================================
# 守卫
# ============================================================
guards = {}
def guard(name, cond, detail=""):
    guards[name] = {"pass": bool(cond), "detail": detail}
    if not cond:
        print(f"[FAIL] {name}: {detail}")

guard("E1_BH_entropy_sun", abs(S_BH_sun_over_kB/mpf('1.0e77')-1)<10,
      f"S_BH(sun)/k_B = 10^{float(log(S_BH_sun_over_kB)/log(10)):.2f}")
guard("E2_vacuum_gap_123", 120 < log10_ratio < 126,
      f"log10(ρ_theory/ρ_obs) = {log10_ratio:.2f}")
guard("E3_Dirac_g_over_e", abs(g_over_e_Dirac/mpf('68.5')-1)<0.01,
      f"g/e (Dirac n=1) = {float(g_over_e_Dirac):.3f}")
guard("E4_Hawking_T_sound", T_sun_BH < mpf('1e-7'),
      f"T_H(sun) = {float(T_sun_BH):.3e} K (远低于 CMB 2.7K)")
guard("E5_evap_sun_1e67yr", abs(t_evap_sun_yr/mpf('1.1e67')-1)<1,
      f"t_evap(sun) = {float(log(t_evap_sun_yr)/log(10)):.2e} yr")
guard("E6_entropy_ratio", 1e18 < float(ratio_entropy) < 1e21,
      f"S_BH/S_thermal(sun) = 10^{float(log(ratio_entropy)/log(10)):.1f}")
guard("E7_LHC_to_Planck_gap", gap_LHC_to_P > 14,
      f"LHC vs Planck 差距 = 10^{gap_LHC_to_P:.1f}")

def f(x, n=10): return f"{float(x):.{n}g}"
out = {
    "E1_BH_entropy_sun_over_kB_log10": float(log(S_BH_sun_over_kB)/log(10)),
    "E2_vacuum_energy_density_gap_log10": log10_ratio,
    "E3_Dirac_g_over_e": f(g_over_e_Dirac, 6),
    "E4_Hawking_T_sun_K": f(T_sun_BH, 6),
    "E5_evap_sun_yr_log10": float(log(t_evap_sun_yr)/log(10)),
    "E5_evap_galaxy_yr": f(t_evap_galaxy_yr, 6),
    "E5_evap_1kg_s": f(t_evap_1kg_s, 6),
    "E6_BH_vs_sun_entropy_ratio_log10": float(log(ratio_entropy)/log(10)),
    "E7_LHC_to_Planck_gap_orders": gap_LHC_to_P,
    "guards": guards
}
with open(os.path.join(HERE, "72_essence_results.json"), "w", encoding="utf-8") as fp:
    json.dump(out, fp, indent=2, ensure_ascii=False)

print("="*70)
print("  本质本源精算")
print("="*70)
print(f"  E1  太阳黑洞熵 S/kB       = 10^{float(log(S_BH_sun_over_kB)/log(10)):.2f}")
print(f"  E2  真空能密度差          = 10^{log10_ratio:.1f} 倍")
print(f"  E3  Dirac g/e             = {float(g_over_e_Dirac):.3f}")
print(f"  E4  太阳 Hawking 温度     = {float(T_sun_BH):.3e} K")
print(f"  E5  太阳黑洞蒸发时间      = 10^{float(log(t_evap_sun_yr)/log(10)):.1f} yr")
print(f"  E5  1kg 微黑洞蒸发时间    = {float(t_evap_1kg_s):.3e} s")
print(f"  E6  黑洞熵/太阳热熵       = 10^{float(log(ratio_entropy)/log(10)):.1f}")
print(f"  E7  LHC→Planck 能标差     = 10^{gap_LHC_to_P:.1f}")
print("-"*70)
passed = sum(1 for g in guards.values() if g["pass"])
print(f"  GUARDS: {passed}/{len(guards)} passed")
for k, v in guards.items():
    print(f"    [{'PASS' if v['pass'] else 'FAIL'}] {k}: {v['detail']}")
print("="*70)

def _emit_report(tag):
    rep = os.path.join(HERE, tag + "_report.txt")
    lines = []
    lines.append(tag + " guards=%d/%d" % (passed, len(guards)))
    for k, v in guards.items():
        lines.append("[%s] %s  %s" % ("PASS" if v["pass"] else "FAIL", k, v["detail"]))
    with open(rep, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")
    print("  report -> " + rep)

_emit_report(TAG_NAME)

sys.exit(0 if passed==len(guards) else 1)
