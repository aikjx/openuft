#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宇宙文明技术落地 - 批量数值计算引擎
生成大量参数扫描、常数计算、技术方案数据
"""
import mpmath as mp
import json
import os

mp.mp.dps = 100  # 100位精度

OUTPUT_DIR = "/home/user/.super_doubao/super-doubao-runtime/workspace/cosmic_civilization_book/data"

# CODATA 2022 基准常数
c = mp.mpf('299792458')
G_exp = mp.mpf('6.67430e-11')
eps0_exp = mp.mpf('8.8541878128e-12')
alpha_exp = mp.mpf('7.2973525693e-3')
hbar_exp = mp.mpf('1.054571817e-34')
kB_exp = mp.mpf('1.380649e-23')
me_exp = mp.mpf('9.1093837015e-31')
mmu_exp = mp.mpf('1.883531627e-28')
mtau_exp = mp.mpf('3.167540000e-27')

n0 = 1043350999  # 本体量子数基准值

def fmt(x, digits=12):
    """格式化mpmath数"""
    return mp.nstr(x, digits)

# ============================================================
# 数据集1: 不同本体量子数n下的物理常数扫描 (n从10^8到10^10, 1000个点)
# ============================================================
print("生成数据集1: 本体量子数n扫描...")
data1 = []
for i in range(1000):
    n_val = mp.mpf(10**8) * (mp.mpf(100) ** (mp.mpf(i)/999))  # 对数扫描 1e8到1e10
    n_int = int(mp.floor(n_val))
    if n_int < 1:
        continue
    delta_F = 1/(2*mp.pi*n_int)
    beta = mp.asinh(delta_F)
    G_theory = alpha_exp * delta_F / (2*mp.pi*c*eps0_exp)
    eps0_theory = alpha_exp * delta_F / (2*mp.pi*c*G_exp)
    G_residual = abs((G_theory - G_exp)/G_exp) * 100
    data1.append({
        'n': n_int,
        'delta_F': float(delta_F),
        'beta': float(beta),
        'G_theory': float(G_theory),
        'G_residual_pct': float(G_residual),
    })

with open(os.path.join(OUTPUT_DIR, '01_n_scan.json'), 'w') as f:
    json.dump(data1, f)
print(f"  生成 {len(data1)} 条数据")

# ============================================================
# 数据集2: 动态分形维随能量尺度演化 (1000个能量点)
# ============================================================
print("生成数据集2: 动态分形维能量演化...")
data2 = []
delta_F0 = 1/(2*mp.pi*n0)
for i in range(1000):
    # 能量从1eV到1e19GeV (普朗克尺度)
    logE_eV = 0 + (28) * (i/999)  # 0到28, 即1eV到1e28eV=1e19GeV
    E_eV = 10**logE_eV
    E_J = E_eV * 1.602176634e-19
    # kappa*tau/c^2 正比于 (E/E_P)^2
    E_P_J = mp.sqrt(hbar_exp * c**5 / G_exp)
    ratio = (E_J / E_P_J)**2
    # 限制ratio不超过1/sinh^2(beta)
    max_ratio = 1/delta_F0**2
    if ratio > max_ratio * 0.99:
        ratio = max_ratio * 0.99
    ds = 4 - delta_F0**2 * ratio
    if ds < 1.5:
        ds = 1.5
    data2.append({
        'logE_eV': logE_eV,
        'E_eV': float(E_eV),
        'E_GeV': float(E_eV/1e9),
        'ratio': float(ratio),
        'd_s': float(ds),
    })

with open(os.path.join(OUTPUT_DIR, '02_fractal_dimension_energy.json'), 'w') as f:
    json.dump(data2, f)
print(f"  生成 {len(data2)} 条数据")

# ============================================================
# 数据集3: 引力-电磁互激效应参数扫描 (磁场强度1-1000T, 距离0.01-10m)
# ============================================================
print("生成数据集3: 引力-电磁互激效应扫描...")
data3 = []
mu0 = 1/(eps0_exp * c**2)
for B_idx in range(50):
    B = 10**(0 + 3*(B_idx/49))  # 1T到1000T
    for r_idx in range(50):
        r = 10**(-2 + 2*(r_idx/49))  # 0.01m到1m
        V_coil = 0.001  # 线圈体积
        U_B = B**2/(2*mu0) * V_coil
        m_EM = U_B / c**2
        m_eff = m_EM * delta_F0
        delta_g = G_exp * m_eff / r**2
        snr = delta_g / 1e-20  # 探测器灵敏度1e-20
        data3.append({
            'B_T': float(B),
            'r_m': float(r),
            'U_B_J': float(U_B),
            'm_EM_kg': float(m_EM),
            'm_eff_kg': float(m_eff),
            'delta_g': float(delta_g),
            'SNR': float(snr),
        })

with open(os.path.join(OUTPUT_DIR, '03_gravity_em_coupling.json'), 'w') as f:
    json.dump(data3, f)
print(f"  生成 {len(data3)} 条数据")

# ============================================================
# 数据集4: 宇宙学参数红移演化 (z从0到1100, 500个点)
# ============================================================
print("生成数据集4: 宇宙学红移演化...")
data4 = []
H0_cmb = 67.66
H0_local = 73.04
Omega_m = 0.3111
Omega_L = 0.6889
Omega_r = 9.2e-5
for i in range(500):
    z = 1100 * (i/499)
    a = 1/(1+z)
    # LambdaCDM H(z)
    H_z_lcdm = H0_cmb * mp.sqrt(Omega_r*(1+z)**4 + Omega_m*(1+z)**3 + Omega_L)
    # 本理论修正: 双曲项随红移变化
    # 高红移时双曲修正大, H接近CMB值; 低红移时分形余项主导, H接近局部值
    correction = (H0_local - H0_cmb) * mp.exp(-z/0.5)  # 低红移增强
    H_z_theory = H_z_lcdm + correction
    # 物质密度
    rho_m = Omega_m * (1+z)**3
    # 辐射密度
    rho_r = Omega_r * (1+z)**4
    # 暗能量密度
    rho_L = Omega_L
    data4.append({
        'z': float(z),
        'a': float(a),
        'H_z_lcdm': float(H_z_lcdm),
        'H_z_theory': float(H_z_theory),
        'correction': float(correction),
        'rho_m': float(rho_m),
        'rho_r': float(rho_r),
        'rho_L': float(rho_L),
    })

with open(os.path.join(OUTPUT_DIR, '04_cosmology_redshift.json'), 'w') as f:
    json.dump(data4, f)
print(f"  生成 {len(data4)} 条数据")

# ============================================================
# 数据集5: CKM矩阵元Wolfenstein参数扫描 (lambda, A, rhobar, etabar)
# ============================================================
print("生成数据集5: CKM参数扫描...")
data5 = []
for lam_idx in range(20):
    lam = 0.220 + 0.010*(lam_idx/19)
    for A_idx in range(20):
        A = 0.78 + 0.10*(A_idx/19)
        rhobar = 0.159
        etabar = 0.352
        # Wolfenstein CKM
        Vud = 1 - lam**2/2 - lam**4/8
        Vus = lam
        Vub = A*lam**3*mp.sqrt(rhobar**2+etabar**2)
        Vcs = 1 - lam**2/2 - lam**4*(1/8+A**2/2)
        Vcb = A*lam**2
        Vtb = 1 - A**2*lam**4/2
        # 幺正性
        unitarity_row1 = Vud**2 + Vus**2 + Vub**2
        data5.append({
            'lambda': float(lam),
            'A': float(A),
            'Vud': float(Vud),
            'Vus': float(Vus),
            'Vub': float(Vub),
            'Vcs': float(Vcs),
            'Vcb': float(Vcb),
            'Vtb': float(Vtb),
            'unitarity_row1': float(unitarity_row1),
        })

with open(os.path.join(OUTPUT_DIR, '05_ckm_scan.json'), 'w') as f:
    json.dump(data5, f)
print(f"  生成 {len(data5)} 条数据")

# ============================================================
# 数据集6: 粒子质量谱与Koide关系参数扫描
# ============================================================
print("生成数据集6: Koide关系扫描...")
data6 = []
for theta_idx in range(100):
    theta = 0.5 + 0.4*(theta_idx/99)  # 弧度, ~28度到52度
    m0 = 1.0  # 基准质量
    sqrt_m = []
    for f in range(3):
        angle = theta + 2*mp.pi*f/3
        sqrt_m.append(mp.sqrt(m0)*(1 + 2*mp.sqrt(2)/3*mp.cos(angle)))
    m = [s**2 for s in sqrt_m]
    koide = sum(m)/(sum(sqrt_m)**2)
    # 质量比
    r12 = m[0]/m[1] if m[1] != 0 else 0
    r23 = m[1]/m[2] if m[2] != 0 else 0
    data6.append({
        'theta_rad': float(theta),
        'theta_deg': float(theta*180/mp.pi),
        'm1': float(m[0]),
        'm2': float(m[1]),
        'm3': float(m[2]),
        'koide_ratio': float(koide),
        'r12': float(r12),
        'r23': float(r23),
    })

with open(os.path.join(OUTPUT_DIR, '06_koide_scan.json'), 'w') as f:
    json.dump(data6, f)
print(f"  生成 {len(data6)} 条数据")

# ============================================================
# 数据集7: 技术方案 - 引力推进器参数扫描
# ============================================================
print("生成数据集7: 引力推进器参数...")
data7 = []
for power_idx in range(50):
    power_MW = 0.1 + 1000*(power_idx/49)  # 0.1MW到1000MW
    power_W = power_MW * 1e6
    for freq_idx in range(30):
        freq_GHz = 0.1 + 100*(freq_idx/29)  # 0.1GHz到100GHz
        freq_Hz = freq_GHz * 1e9
        # 电磁能量等效质量流
        mass_flow = power_W / c**2  # kg/s
        # 交叉耦合后的有效引力质量流
        eff_mass_flow = mass_flow * delta_F0
        # 推力 (假设动量完全转换)
        thrust = eff_mass_flow * c  # N
        # 推功比
        thrust_per_power = thrust / power_W  # N/W
        data7.append({
            'power_MW': float(power_MW),
            'freq_GHz': float(freq_GHz),
            'mass_flow_kg_s': float(mass_flow),
            'eff_mass_flow': float(eff_mass_flow),
            'thrust_N': float(thrust),
            'thrust_per_power_N_W': float(thrust_per_power),
        })

with open(os.path.join(OUTPUT_DIR, '07_gravity_thruster.json'), 'w') as f:
    json.dump(data7, f)
print(f"  生成 {len(data7)} 条数据")

# ============================================================
# 数据集8: 真空能提取技术参数
# ============================================================
print("生成数据集8: 真空能提取参数...")
data8 = []
# 分形余项对应的真空能密度
rho_vac_theory = 1e-9  # J/m^3 (与暗能量同量级, 粗略)
for volume_idx in range(50):
    volume_m3 = 10**(-3 + 6*(volume_idx/49))  # 0.001m3到1000m3
    for efficiency_idx in range(30):
        efficiency = 0.001 + 0.5*(efficiency_idx/29)  # 0.1%到50%
        total_energy = rho_vac_theory * volume_m3
        extractable_energy = total_energy * efficiency
        # 功率 (假设1秒提取周期)
        power = extractable_energy
        data8.append({
            'volume_m3': float(volume_m3),
            'efficiency': float(efficiency),
            'total_energy_J': float(total_energy),
            'extractable_J': float(extractable_energy),
            'power_W': float(power),
        })

with open(os.path.join(OUTPUT_DIR, '08_vacuum_energy.json'), 'w') as f:
    json.dump(data8, f)
print(f"  生成 {len(data8)} 条数据")

# ============================================================
# 数据集9: 时空工程 - 曲率操控参数
# ============================================================
print("生成数据集9: 时空曲率操控参数...")
data9 = []
for energy_idx in range(50):
    energy_J = 10**(0 + 20*(energy_idx/49))  # 1J到1e20J
    mass_eq = energy_J / c**2
    # 产生的时空曲率 (Schwarzschild半径比例)
    r_s = 2*G_exp*mass_eq / c**2
    # 曲率标量 ~ 1/r_s^2
    curvature = 1/r_s**2 if r_s > 0 else 0
    # 操控范围 (假设能量集中在1m^3)
    radius = 1.0
    # 度规扰动 h ~ G*M/(r*c^2)
    h_perturb = G_exp*mass_eq/(radius*c**2)
    data9.append({
        'energy_J': float(energy_J),
        'mass_eq_kg': float(mass_eq),
        'schwarzschild_radius_m': float(r_s),
        'curvature_1_m2': float(curvature),
        'metric_perturbation_h': float(h_perturb),
    })

with open(os.path.join(OUTPUT_DIR, '09_spacetime_engineering.json'), 'w') as f:
    json.dump(data9, f)
print(f"  生成 {len(data9)} 条数据")

# ============================================================
# 数据集10: 戴森球/恒星工程参数
# ============================================================
print("生成数据集10: 恒星工程参数...")
data10 = []
M_sun = 1.989e30  # kg
L_sun = 3.828e26   # W
R_sun = 6.96e8     # m
for star_mass_idx in range(30):
    star_mass = 0.1 + 100*(star_mass_idx/29)  # 0.1到100太阳质量
    M = star_mass * M_sun
    # 主序星光度 ~ M^3.5 (质量越大光度越大)
    L = L_sun * star_mass**3.5
    # 半径 ~ M^0.8
    R = R_sun * star_mass**0.8
    # 戴森球半径 (1AU)
    r_dyson = 1.496e11
    # 戴森球接收功率
    P_dyson = L * (R**2 / (4*r_dyson**2)) * 4*mp.pi  # 全部包裹
    # 实际可用 (假设效率)
    efficiency = 0.3
    P_usable = P_dyson * efficiency
    # 恒星寿命 ~ M/L
    lifetime = M * c**2 * 0.007 / L  # 7%质量转化为能量, 10%可用
    data10.append({
        'star_mass_solar': float(star_mass),
        'luminosity_solar': float(L/L_sun),
        'radius_solar': float(R/R_sun),
        'dyson_power_W': float(P_dyson),
        'usable_power_W': float(P_usable),
        'lifetime_s': float(lifetime),
        'lifetime_years': float(lifetime/(365.25*24*3600)),
    })

with open(os.path.join(OUTPUT_DIR, '10_stellar_engineering.json'), 'w') as f:
    json.dump(data10, f)
print(f"  生成 {len(data10)} 条数据")

# ============================================================
# 汇总统计
# ============================================================
total = sum(len(d) for d in [data1,data2,data3,data4,data5,data6,data7,data8,data9,data10])
print(f"\n全部数据集生成完成! 总计 {total} 条数据记录")
print(f"输出目录: {OUTPUT_DIR}")

# 生成汇总JSON
summary = {
    'total_records': total,
    'datasets': [
        {'name': '本体量子数n扫描', 'count': len(data1), 'file': '01_n_scan.json'},
        {'name': '动态分形维能量演化', 'count': len(data2), 'file': '02_fractal_dimension_energy.json'},
        {'name': '引力-电磁互激效应扫描', 'count': len(data3), 'file': '03_gravity_em_coupling.json'},
        {'name': '宇宙学红移演化', 'count': len(data4), 'file': '04_cosmology_redshift.json'},
        {'name': 'CKM参数扫描', 'count': len(data5), 'file': '05_ckm_scan.json'},
        {'name': 'Koide关系扫描', 'count': len(data6), 'file': '06_koide_scan.json'},
        {'name': '引力推进器参数', 'count': len(data7), 'file': '07_gravity_thruster.json'},
        {'name': '真空能提取参数', 'count': len(data8), 'file': '08_vacuum_energy.json'},
        {'name': '时空曲率操控参数', 'count': len(data9), 'file': '09_spacetime_engineering.json'},
        {'name': '恒星工程参数', 'count': len(data10), 'file': '10_stellar_engineering.json'},
    ],
    'benchmark_constants': {
        'c': float(c),
        'G': float(G_exp),
        'epsilon0': float(eps0_exp),
        'alpha': float(alpha_exp),
        'hbar': float(hbar_exp),
        'n0': n0,
        'delta_F0': float(delta_F0),
    }
}
with open(os.path.join(OUTPUT_DIR, 'summary.json'), 'w') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print("汇总文件已生成: summary.json")
