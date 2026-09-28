# 简单验证脚本

"""
快速验证修订版论文中的核心公式
"""

import math

# 物理常数
c = 299792458          # 光速 (m/s)
G = 6.67430e-11         # 万有引力常数 (m³/kg/s²)
h = 6.62607015e-34      # 普朗克常数 (J·s)
k_B = 1.380649e-23       # 玻尔兹曼常数 (J/K)
epsilon0 = 8.8541878128e-12  # 真空介电常数 (F/m)
e = 1.602176634e-19      # 元电荷 (C)
m_e = 9.1093837015e-31   # 电子质量 (kg)
lambda_e = 2.42631023867e-12  # 电子康普顿波长 (m)
M_sun = 1.98847e30       # 太阳质量 (kg)
R_earth_orbit = 1.496e11  # 地球公转轨道半径 (m)
T_earth_orbit = 3.154e7   # 地球公转周期 (s)
m_earth = 5.972e24       # 地球质量 (kg)

# 验证结果字典
results = {}

# 1. 验证电子属性
print("验证电子属性...")
r_e = lambda_e / (2 * math.pi)
omega_e = c / r_e
m_e_calc = (c**2 * r_e) / G
e_calc = math.sqrt(4 * math.pi * epsilon0 * G * m_e**2)
m_error = abs(m_e_calc - m_e) / m_e * 100
e_error = abs(e_calc - e) / e * 100

results['电子验证'] = {
    '螺旋半径': r_e,
    '角速度': omega_e,
    '质量计算值': m_e_calc,
    '质量实际值': m_e,
    '元电荷计算值': e_calc,
    '元电荷实际值': e,
    '质量误差(%)': m_error,
    '元电荷误差(%)': e_error
}

# 2. 验证太阳系
print("验证太阳系...")
r_M = (G * M_sun) / (c**2)
omega_M = c / r_M
T_calc = 2 * math.pi * math.sqrt(R_earth_orbit**3 / (G * M_sun))
F = m_earth * omega_M**2 * r_M**3 / R_earth_orbit**2
T_error = abs(T_calc - T_earth_orbit) / T_earth_orbit * 100

results['太阳系验证'] = {
    '太阳螺旋半径': r_M,
    '太阳角速度': omega_M,
    '公转周期计算值': T_calc,
    '公转周期实际值': T_earth_orbit,
    '向心加速度': F,
    '周期误差(%)': T_error
}

# 3. 验证黑洞
print("验证黑洞...")
r = (G * M_sun) / (c**2)
omega = c / r
nu = omega / (2 * math.pi)
T_H = (h * nu) / (8 * math.pi * k_B)
R_s = 2 * r

results['黑洞验证'] = {
    '黑洞螺旋半径': r,
    '黑洞角速度': omega,
    '黑洞频率': nu,
    '霍金温度': T_H,
    '视界半径': R_s
}

# 4. 验证核心公式
print("验证核心公式...")

# 验证 ωr = c
omega_test = 1e10  # 测试角速度
r_test = c / omega_test
omega_r_test = omega_test * r_test
omega_r_error = abs(omega_r_test - c) / c * 100

# 验证 m = c²r/G
m_test = (c**2 * r_test) / G

# 验证 hν = mc²
nu_test = omega_test / (2 * math.pi)
hnu_test = h * nu_test
mc2_test = m_test * c**2
hnu_error = abs(hnu_test - mc2_test) / mc2_test * 100

results['核心公式验证'] = {
    'ωr=c 误差(%)': omega_r_error,
    'hν=mc² 误差(%)': hnu_error
}

# 保存结果
with open('verification_results.txt', 'w', encoding='utf-8') as f:
    f.write("=== 验证结果 ===\n\n")
    
    for section, data in results.items():
        f.write(f"{section}:\n")
        for key, value in data.items():
            if '误差' in key:
                f.write(f"  {key}: {value:.6f}%\n")
            else:
                if abs(value) < 1e-6 or abs(value) > 1e6:
                    f.write(f"  {key}: {value:.6e}\n")
                else:
                    f.write(f"  {key}: {value:.6f}\n")
        f.write("\n")

print("验证完成！结果已保存到 verification_results.txt")
