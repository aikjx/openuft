# 物体宽度计算验证脚本
# 基于统一场论推导的不同运动状态宽度公式

import math

# 基准参数
w0 = 1.0  # 固有宽度 (m)
m0 = 1.0  # 物体质量 (kg)
c = 3.0e8  # 光速 (m/s)
hbar = 1.0546e-34  # 约化普朗克常数 (J·s)

# 速度测试点 (m/s)
velocities = [
    0.0,                    # 静止
    1.0e3, 1.0e6,           # 低速
    0.1*c, 0.5*c,           # 中速
    0.9*c, 0.99*c,          # 高速
    0.999*c, 0.9999*c       # 接近光速
]

# 计算函数
def calculate_widths(v):
    """计算不同运动状态的物体宽度"""
    # 洛伦兹因子
    gamma = 1.0 / math.sqrt(1 - (v**2)/(c**2)) if v < c else float('inf')
    
    # 匀速状态宽度
    w_v = w0
    
    # 加速状态宽度
    if v < c:
        w_a = w0 * math.sqrt(1 - (v**2)/(c**2))
    else:
        w_a = 0.0
    
    # 光速状态宽度 (假设光子质量)
    if v == c:
        m = m0  # 这里简化处理，实际光子质量与能量相关
        w_c = hbar / (m * c)
    else:
        w_c = float('nan')
    
    return gamma, w_v, w_a, w_c

# 执行计算
print("速度测试点验证结果")
print("-" * 100)
print(f"{'速度 (m/s)':<20} {'速度 (c)':<10} {'γ':<15} {'匀速宽度 (m)':<15} {'加速宽度 (m)':<15} {'光速宽度 (m)':<15}")
print("-" * 100)

for v in velocities:
    v_ratio = v / c
    gamma, w_v, w_a, w_c = calculate_widths(v)
    
    # 格式化输出
    v_str = f"{v:.2e}"
    v_ratio_str = f"{v_ratio:.4f}"
    gamma_str = f"{gamma:.6f}" if gamma < 1e6 else f"{gamma:.2e}"
    w_v_str = f"{w_v:.6f}"
    w_a_str = f"{w_a:.6f}" if not math.isnan(w_a) else "N/A"
    w_c_str = f"{w_c:.2e}" if not math.isnan(w_c) else "N/A"
    
    print(f"{v_str:<20} {v_ratio_str:<10} {gamma_str:<15} {w_v_str:<15} {w_a_str:<15} {w_c_str:<15}")

print("-" * 100)

# 光速状态特殊计算
print("\n光速状态宽度计算（光子）:")
print("-" * 80)
print(f"{'光子能量 (eV)':<20} {'质量 (kg)':<20} {'宽度 (m)':<20}")
print("-" * 80)

# 不同能量的光子
energies_eV = [1.0, 1000.0, 1.0e6, 1.0e9]  # 1eV, 1keV, 1MeV, 1GeV
for E_eV in energies_eV:
    E_J = E_eV * 1.6022e-19  # 转换为焦耳
    m = E_J / (c**2)  # 质能方程
    w_c = hbar / (m * c)  # 光速状态宽度
    print(f"{E_eV:.2e} {'':<5} {m:.2e} {'':<5} {w_c:.2e}")

print("-" * 80)