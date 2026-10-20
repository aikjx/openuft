"""
uft_full_chain_numerics.py
==========================
全链路精算：从经典力学到量子引力的桥梁常数
mpmath 250 位
"""
import json, os, sys
TAG_NAME = "71_full_chain"
HERE = os.path.dirname(os.path.abspath(__file__))
# Windows GBK 控制台下 ²/⁴ 等上标字符会抛 UnicodeEncodeError ⇒ 强制 UTF-8 输出
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
from mpmath import mp, mpf, pi, sqrt, exp, log, factorial

mp.dps = 250

# 基础常数
c    = mpf('299792458')
hbar = mpf('1.054571817e-34')
e    = mpf('1.602176634e-19')
m_e  = mpf('9.1093837139e-31')
m_p  = mpf('1.67262192595e-27')
k_B  = mpf('1.380649e-23')
G    = mpf('6.67430e-11')
alpha = mpf('7.2973525693e-3')
mu0 = 4e-7*pi
eps0 = 1/(mu0*c**2)

# ============================================================
# C1: Bohr 半径（经典→量子桥梁）
# a0 = 4π ε0 ħ² / (m_e e²)
# ============================================================
a0 = 4*pi*eps0*hbar**2/(m_e*e**2)  # 米

# ============================================================
# C2: 氢原子基态能级（Rydberg）
# E1 = -m_e e^4 / (8 ε0² h²) = -13.6057 eV
# ============================================================
E1_J = -m_e*e**4/(8*eps0**2*(2*pi*hbar)**2)  # Joule
E1_eV = E1_J/e  # eV

# ============================================================
# C3: 经典电子半径
# r_e = e²/(4π ε0 m_e c²) = 2.818e-15 m
# ============================================================
r_e = e**2/(4*pi*eps0*m_e*c**2)

# ============================================================
# C4: 精细结构常数的三个等价表达式
# α = e²/(4π ε0 ħ c)
# α = r_e / a0
# α² = 2 r_e / λ_C (约化 Compton 波长)
# ============================================================
lambda_C_e = hbar/(m_e*c)  # 约化 Compton 波长
alpha_check_1 = e**2/(4*pi*eps0*hbar*c)
# 几何关系：r_e = α λ_C，a0 = λ_C/α  =>  α = r_e/λ_C = λ_C/a0
alpha_check_2 = lambda_C_e/a0
alpha_check_3 = r_e/lambda_C_e

# ============================================================
# C5: 黑体辐射 Wien 位移
# λ_max T = b = 2.898e-3 m·K
# 太阳 5778 K → λ_max ≈ 501 nm
# ============================================================
b_Wien = mpf('2.897771955e-3')  # m·K
T_sun = mpf('5778')
lambda_max_sun = b_Wien/T_sun

# ============================================================
# C6: Stefan-Boltzmann 常数
# σ = 2 π^5 k_B^4 / (15 h^3 c^2)
# ============================================================
h = 2*pi*hbar
sigma_SB = 2*pi**5*k_B**4/(15*h**3*c**2)

# ============================================================
# C7: 谐振子能级（量子力学标志）
# E_n = (n+1/2) ħ ω
# 基态零点能 = ħω/2
# ============================================================
# 取典型分子振动 ω = 1e14 rad/s 做演示
omega_mol = mpf('1e14')
E_zero = hbar*omega_mol/2

# ============================================================
# C8: de Broglie 波长
# λ = h/p
# 室温热中子（2200 m/s）λ ≈ 1.8 Å
# ============================================================
m_n = mpf('1.6749275e-27')
v_neutron = mpf('2200')
lambda_deBroglie_neutron = h/(m_n*v_neutron)

# ============================================================
# C9: 宇宙学黑体：CMB 温度 2.7255 K 对应的峰值波长
# ============================================================
T_CMB = mpf('2.7255')
lambda_max_CMB = b_Wien/T_CMB  # 米 → mm

# ============================================================
# C10: Schwarzschild 半径与引力红移（GR 标志）
# ============================================================
# 太阳已经在 v2 算过，这里算 Sgr A* (4.3e6 M_sun)
M_SgrA = mpf('4.3e6') * mpf('1.98847e30')
r_s_SgrA = 2*G*M_SgrA/c**2

# ============================================================
# C11: Planck 黑体辐射的高频/低频极限（量子→经典对应）
# 维恩位移定律在 kT << hν 时退化为瑞利-金斯
# ============================================================
# 室温 T=300K, kT/h 在 THz
nu_peak_300K = (k_B*mpf('300'))/h  # Hz

# ============================================================
# 守卫
# ============================================================
guards = {}
def guard(name, cond, detail=""):
    guards[name] = {"pass": bool(cond), "detail": detail}
    if not cond:
        print(f"[FAIL] {name}: {detail}")

guard("C1_Bohr_radius", abs(a0/mpf('5.29177e-11')-1)<1e-6,
      f"a0 = {float(a0):.6e} m (expected 5.29177e-11)")
guard("C2_H_ground_state_eV", abs(E1_eV/mpf('-13.6057')-1)<1e-4,
      f"E1 = {float(E1_eV):.6f} eV")
guard("C3_classical_e_radius", abs(r_e/mpf('2.81794e-15')-1)<1e-5,
      f"r_e = {float(r_e):.6e} m")
guard("C4_alpha_three_expressions",
      abs(alpha_check_1-alpha)<1e-9 and abs(alpha_check_2-alpha)<1e-9 and abs(alpha_check_3-alpha)<1e-9,
      f"α1={float(alpha_check_1):.10f}, α2={float(alpha_check_2):.10f}, α3={float(alpha_check_3):.10f}")
guard("C5_sun_peak_500nm", abs(lambda_max_sun/mpf('5.015e-7')-1)<0.02,
      f"λ_max(sun) = {float(lambda_max_sun*1e9):.1f} nm")
guard("C6_SB_constant", abs(sigma_SB/mpf('5.67037e-8')-1)<1e-5,
      f"σ = {float(sigma_SB):.6e} W/m²/K⁴")
guard("C8_thermal_neutron_1.8A", abs(lambda_deBroglie_neutron/mpf('1.798e-10')-1)<0.02,
      f"λ_n = {float(lambda_deBroglie_neutron*1e10):.3f} Å")
guard("C9_CMB_peak", abs(lambda_max_CMB/mpf('1.063e-3')-1)<0.02,
      f"λ_max(CMB) = {float(lambda_max_CMB*1e3):.2f} mm")
guard("C10_SgrA_r_s", abs(r_s_SgrA/mpf('1.27e10')-1)<0.1,
      f"r_s(Sgr A*) = {float(r_s_SgrA):.3e} m ≈ {float(r_s_SgrA/1e9):.2f} 千万公里")

def f(x, n=10): return f"{float(x):.{n}g}"
out = {
    "C1_Bohr_radius_m": f(a0),
    "C2_H_ground_eV": f(E1_eV, 6),
    "C3_classical_e_radius_m": f(r_e),
    "C4_alpha_check": f(alpha_check_1, 12),
    "C5_sun_peak_nm": f(lambda_max_sun*1e9, 6),
    "C6_SB_W_m2_K4": f(sigma_SB),
    "C7_zero_point_J": f(E_zero, 6),
    "C8_thermal_neutron_A": f(lambda_deBroglie_neutron*1e10, 6),
    "C9_CMB_peak_mm": f(lambda_max_CMB*1e3, 6),
    "C10_SgrA_rs_m": f(r_s_SgrA),
    "C11_nu_peak_300K_Hz": f(nu_peak_300K, 6),
    "guards": guards
}
with open(os.path.join(HERE, "71_full_chain_results.json"), "w", encoding="utf-8") as fp:
    json.dump(out, fp, indent=2, ensure_ascii=False)

print("="*70)
print("  全链路精算：经典 → 量子 → 相对论 → 宇宙学")
print("="*70)
print(f"  C1  Bohr 半径      = {float(a0):.6e} m")
print(f"  C2  H 基态能级     = {float(E1_eV):.6f} eV")
print(f"  C3  经典电子半径   = {float(r_e):.6e} m")
print(f"  C4  α 三式互验     = {float(alpha_check_1):.10f}")
print(f"  C5  太阳 λ_max     = {float(lambda_max_sun*1e9):.1f} nm")
print(f"  C6  Stefan-Boltzmann= {float(sigma_SB):.6e} W/m²/K⁴")
print(f"  C8  热中子 λ       = {float(lambda_deBroglie_neutron*1e10):.3f} Å")
print(f"  C9  CMB λ_max      = {float(lambda_max_CMB*1e3):.2f} mm")
print(f"  C10 Sgr A* r_s     = {float(r_s_SgrA):.3e} m")
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
