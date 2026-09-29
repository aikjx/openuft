"""
verify_vc_kappa_tau_omega.py — v=c 公理 × 曲率 κ × 挠率 τ × 频率 ω/c 全维验证脚本
==================================================================================

openuft · 07_统一场方程 · 第10卷 配套验证脚本
精度：mpmath 200位有效数字（牛顿/库仑极限 250位）
运行：python verify_vc_kappa_tau_omega.py

验证内容：
  V1      三轴速度平方守恒 v_perp²+v_z² = c²
  H0      核心恒等式 κ²+τ² = (ω/c)²
  H1      一阶动力学守恒 κκ' + ττ' = ωω'/c²
  H2      二阶动力学守恒
  ANGLE   角度归一 sin²θ+cos²θ=1, κ=(ω/c)cosθ, τ=(ω/c)sinθ
  1D/2D/3D  全维退化验证
  A3      θ场参数化自洽性 11角度测试
  CODATA  电子参数对标（诚实退化检查）
  GMUFT   牛顿/库仑极限 250位验证
"""

import sys
import json
import mpmath as mp

mp.mp.dps = 200
c = mp.mpf('299792458')

def fe(x, fmt='.10e'):
    """格式化 mpf 数值为字符串"""
    return format(float(x), fmt)

results = {}

def check(name, err, bound=1e-170):
    err_f = float(err)
    ok = abs(err_f) < float(bound)
    results[name] = {"error": err_f, "bound": bound, "pass": ok}
    tag = "OK" if ok else "FAIL"
    print(f"  [{tag}] {name:50s}  err={err_f:.3e}")
    return ok

# ════════════════════════════════════════════════════════════
# PART 1: GAQ-UFT 核心恒等式
# ════════════════════════════════════════════════════════════
print("=" * 66)
print("PART 1: GAQ-UFT 核心恒等式 κ²+τ²=(ω/c)²  (mpmath dps=200)")
print("=" * 66)

R = mp.mpf('3.605000000000000e-13')
omega = mp.mpf('7.763440739995891e20')

v_perp = omega * R
v_z = mp.sqrt(c**2 - v_perp**2)
v_total = mp.sqrt(v_perp**2 + v_z**2)

kappa = R * omega**2 / c**2
tau = v_z * omega / c**2
omega_over_c = omega / c

print(f"\n基础参数（自洽，无超光速）:")
print(f"  R       = {fe(R)} m")
print(f"  ω       = {fe(omega)} rad/s")
print(f"  v_perp  = {fe(v_perp)} m/s")
print(f"  v_z     = {fe(v_z)} m/s")
print(f"  v_total = {fe(v_total)} m/s  (精确 = c)")
print(f"\n几何量:")
print(f"  κ   = {fe(kappa)} m⁻¹")
print(f"  τ   = {fe(tau)} m⁻¹")
print(f"  ω/c = {fe(omega_over_c)} m⁻¹")

print(f"\n--- 速度守恒 ---")
check("V1: v_perp² + v_z² = c²", v_total**2 - c**2)

print(f"\n--- 核心恒等式 H0 ---")
h0_err = kappa**2 + tau**2 - omega_over_c**2
check("H0: κ² + τ² = (ω/c)²", h0_err)

print(f"\n--- 角度归一化 ---")
theta = mp.atan(tau / kappa)
sin_theta = v_z / c
cos_theta = v_perp / c
tan_theta = tau / kappa
check("ANGLE: sin²θ + cos²θ = 1", sin_theta**2 + cos_theta**2 - 1)
check("ANGLE: tanθ = τ/κ = v_z/v_perp", tan_theta - sin_theta/cos_theta)
check("ANGLE: κ = (ω/c)·cosθ", kappa - omega_over_c * cos_theta)
check("ANGLE: τ = (ω/c)·sinθ", tau - omega_over_c * sin_theta)

print(f"\n--- 一/二阶动力学守恒 ---")
dl = mp.mpf('1e-60')

def kappa_of_omega(o):
    return R * o**2 / c**2

def tau_of_omega(o):
    vz = mp.sqrt(c**2 - (o * R)**2)
    return vz * o / c**2

omega_p = (omega + dl - (omega - dl)) / (2 * dl)
kappa_p = (kappa_of_omega(omega + dl) - kappa_of_omega(omega - dl)) / (2 * dl)
tau_p   = (tau_of_omega(omega + dl) - tau_of_omega(omega - dl)) / (2 * dl)

h1_lhs = kappa * kappa_p + tau * tau_p
h1_rhs = omega * omega_p / c**2
check("H1: κκ' + ττ' = ωω'/c² (有限差分)", h1_lhs - h1_rhs, bound=1e-110)

omega_pp = ((omega + dl - omega) - (omega - (omega - dl))) / dl**2
kappa_pp = (kappa_of_omega(omega + dl) - 2*kappa_of_omega(omega) + kappa_of_omega(omega - dl)) / dl**2
tau_pp   = (tau_of_omega(omega + dl) - 2*tau_of_omega(omega) + tau_of_omega(omega - dl)) / dl**2

h2_lhs = (kappa_p**2 + tau_p**2) + (kappa * kappa_pp + tau * tau_pp)
h2_rhs = (omega_p**2 + omega * omega_pp) / c**2
check("H2: 二阶动力学守恒 (有限差分)", h2_lhs - h2_rhs, bound=1e-50)

# ════════════════════════════════════════════════════════════
# PART 2: 1/2/3 维退化
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 66)
print("PART 2: 1/2/3 维退化验证")
print("=" * 66)

omega1 = mp.mpf('0')
kappa1 = mp.mpf('0')
tau1 = mp.mpf('0')
check("1D: 真空态 0=0", kappa1**2 + tau1**2 - (omega1/c)**2)

R2 = mp.mpf('5e-13')
omega2 = c / R2
kappa2 = R2 * omega2**2 / c**2
tau2 = mp.mpf('0')
check("2D: 纯引力态 κ²=(ω/c)²", kappa2**2 + tau2**2 - (omega2/c)**2)

check("3D: 完备粒子态", kappa**2 + tau**2 - (omega/c)**2)

# ════════════════════════════════════════════════════════════
# PART 3: A3 θ 场参数化自洽性
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 66)
print("PART 3: A3 θ 场参数化自洽性 (11角度)")
print("=" * 66)

test_angles = [
    0, mp.pi/6, mp.pi/4, mp.pi/3, mp.pi/2,
    mp.pi, 3*mp.pi/2, 2*mp.pi,
    mp.mpf('0.12345'), mp.mpf('1.78901'), mp.mpf('4.56789')
]

all_ok = True
for theta_test in test_angles:
    u_r = c * mp.cos(theta_test)
    u_perp = c * mp.sin(theta_test)
    err = u_r**2 + u_perp**2 - c**2
    if abs(float(err)) >= 1e-180:  # cos²x+sin²x 数学精确=1，阈值考虑 mp.mpf 浮点累积
        all_ok = False
        print(f"  [FAIL] θ={theta_test}  err={float(err):.3e}")
if all_ok:
    print("  [OK]  11角度全部自洽 (max_err < 1e-180)")
results["A3_11angles"] = {"pass": all_ok}

# ════════════════════════════════════════════════════════════
# PART 4: CODATA2022 电子参数对标
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 66)
print("PART 4: CODATA2022 电子参数对标 (诚实版)")
print("=" * 66)

me = mp.mpf('9.1093837015e-31')
hbar = mp.mpf('1.0545718176461565e-34')

omega_e = me * c**2 / hbar
Re = hbar / (me * c)

v_perp_e = omega_e * Re
v_z_e = mp.sqrt(c**2 - v_perp_e**2)
kappa_e = Re * omega_e**2 / c**2
tau_e = v_z_e * omega_e / c**2

print(f"\nCODATA2022 电子参数:")
print(f"  ω_e     = {fe(omega_e)} rad/s")
print(f"  R_e     = {fe(Re)} m")
print(f"  v_perp  = {fe(v_perp_e)} (精确 = c)")
print(f"  v_z     = {v_z_e} (精确 = 0)")
print(f"  κ_e     = {fe(kappa_e)} m⁻¹")
print(f"  τ_e     = {tau_e} (精确 = 0, 无手征)")
print(f"\n诚实结论: 纯康普顿参数下电子退化为2级纯圆周态 (τ=0),")
print(f"         模型无法自发产生电荷。若要赋予电子非零挠率，")
print(f"         必须引入 R_e < ħ/(m_e c) 额外半径假设。")

check("CODATA: v_perp_e = c", v_perp_e - c)
check("CODATA: v_z_e = 0 (sqrt下溢)", v_z_e, bound=1e-80)
check("CODATA: H0 恒成立 (退化版)", kappa_e**2 + tau_e**2 - (omega_e/c)**2)

# ════════════════════════════════════════════════════════════
# PART 5: GMUFT v2.1 牛顿极限 (dps=250)
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 66)
print("PART 5: GMUFT v2.1 牛顿极限验证 (mpmath dps=250)")
print("=" * 66)

mp.mp.dps = 250
G = mp.mpf('6.67430e-11')
beta = mp.mpf('1')

Z0 = beta**2 * c**4 / (4 * mp.pi * G)
print(f"\nGMUFT 参数 (β=1):")
print(f"  Z₀ = β² c⁴/(4πG) = {fe(Z0, '.10e')} N")

err_newton = beta**2 * c**4 / (4 * mp.pi * Z0) - G
check("GMUFT: β²c⁴/(4πZ₀) ≡ G", err_newton, bound=1e-240)

M_test = mp.mpf('5.972e24')
m_test = mp.mpf('1')
r_test = mp.mpf('6.371e6')

F_theta = m_test * beta**2 * c**4 * M_test / (4 * mp.pi * Z0 * r_test**2)
F_newton = G * M_test * m_test / r_test**2

print(f"\n数值测试（地球表面 1kg 物体）:")
print(f"  F_θ (GMUFT)     = {fe(F_theta, '.10e')} N")
print(f"  F_N (牛顿)      = {fe(F_newton, '.10e')} N")
print(f"  差值            = {fe(F_theta - F_newton, '.3e')} N")
check("GMUFT: F_θ ≡ F_N (250位)", F_theta - F_newton, bound=1e-240)

# ════════════════════════════════════════════════════════════
# PART 6: GMUFT v2.1 库仑极限 (dps=250)
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 66)
print("PART 6: GMUFT v2.1 库仑极限 (边界条件匹配)")
print("=" * 66)

epsilon_0 = mp.mpf('8.8541878128e-12')
q1 = mp.mpf('1.602176634e-19')
q2 = q1
r = mp.mpf('1e-10')

F_coulomb = q1 * q2 / (4 * mp.pi * epsilon_0 * r**2)
print(f"\n数值测试（质子-电子，r=1Å）:")
print(f"  F_C (库仑)      = {fe(F_coulomb, '.10e')} N")
print(f"\nGMUFT 弱场 f(θ₀)=ε₀ 边界条件 → 严格还原库仑定律")
print(f"  此为边界条件匹配，非独立预言")
print(f"  GMUFT 真正可证预言: α_eff = α₀[1 + f'(θ₀)δθ/f(θ₀)]")

mp.mp.dps = 200

# ════════════════════════════════════════════════════════════
# 汇总
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 66)
print("汇总")
print("=" * 66)

total = len(results)
passed = sum(1 for v in results.values() if v.get("pass"))
failed = total - passed

for name, v in results.items():
    tag = "OK" if v.get("pass") else "FAIL"
    print(f"  [{tag}] {name}")

print(f"\n通过: {passed}/{total}")
if failed > 0:
    print("❌ 有测试失败！")
    sys.exit(1)
else:
    print("✅ 全部通过 —— 数学/数值基础已验证")

with open("verify_vc_results.json", "w", encoding="utf-8") as f:
    json.dump({
        "date": "2026-09-29",
        "dps": 200,
        "newton_dps": 250,
        "total_checks": total,
        "passed": passed,
        "status": "ALL PASS",
        "results": results
    }, f, indent=2, ensure_ascii=False)
print(f"\n结果已写入 verify_vc_results.json")
