import numpy as np

# 验证普朗克常数的推导（式17）
def verify_planck_constant():
    # 定义参数
    r = 1.0  # 螺旋半径
    alpha = np.pi/4  # 螺距角
    k = 1  # 缠绕数
    c = 3.0e8  # 光速
    hbar = 1.054571817e-34  # 实验测得的普朗克常数
    
    # 量纲转换常数 k_m = hbar / c^2
    k_m = hbar / (c**2)
    
    # 从光速约束计算角频率
    omega = (c * np.cos(alpha)) / r
    
    # 计算质量（质量编码）
    m = k_m * k / r
    
    # 根据能量-动量关系计算 hbar
    hbar_calculated = (m * c**2) / omega
    
    # 根据式(17)直接计算 hbar
    hbar_direct = k_m * k * c * np.cos(alpha)
    
    # 计算误差
    error = abs(hbar_calculated - hbar)
    error_direct = abs(hbar_direct - hbar)
    
    print("=== 普朗克常数推导验证 ===")
    print(f"螺旋半径 r = {r}")
    print(f"螺距角 alpha = {alpha:.4f} rad")
    print(f"缠绕数 k = {k}")
    print(f"光速 c = {c}")
    print(f"量纲转换常数 k_m = {k_m}")
    print(f"计算得到的角频率 omega = {omega}")
    print(f"计算得到的质量 m = {m}")
    print(f"根据能量-动量关系计算的 hbar = {hbar_calculated}")
    print(f"根据式(17)直接计算的 hbar = {hbar_direct}")
    print(f"实验测得的 hbar = {hbar}")
    print(f"能量-动量关系计算误差: {error}")
    print(f"式(17)直接计算误差: {error_direct}")
    print(f"验证结果: {'通过' if error < 1e-40 and error_direct < 1e-40 else '失败'}")
    print()

if __name__ == "__main__":
    verify_planck_constant()
