import numpy as np

# 验证角动量的计算与量子化条件（式13-14）
def verify_angular_momentum():
    # 定义参数
    r = 1.0  # 螺旋半径
    alpha = np.pi/4  # 螺距角
    k = 1  # 缠绕数
    c = 3.0e8  # 光速
    hbar = 1.054571817e-34  # 普朗克常数
    k_m = hbar / (c**2)  # 量纲转换常数
    
    # 从光速约束计算角频率
    omega = (c * np.cos(alpha)) / r
    
    # 计算质量（质量编码）
    m = k_m * k / r
    
    # 计算角动量
    L = m * r**2 * omega
    
    # 另外，根据论文中的式(13)直接计算
    L_direct = k_m * k * c * np.cos(alpha)
    
    # 验证角动量是否等于 k * hbar
    expected_L = k * hbar
    error = abs(L - expected_L)
    
    print("=== 角动量计算与量子化条件验证 ===")
    print(f"螺旋半径 r = {r}")
    print(f"螺距角 alpha = {alpha:.4f} rad")
    print(f"缠绕数 k = {k}")
    print(f"光速 c = {c}")
    print(f"量纲转换常数 k_m = {k_m}")
    print(f"计算得到的角频率 omega = {omega}")
    print(f"计算得到的质量 m = {m}")
    print(f"计算得到的角动量 L = {L}")
    print(f"根据式(13)直接计算的角动量 L_direct = {L_direct}")
    print(f"预期角动量 k*hbar = {expected_L}")
    print(f"误差: {error}")
    print(f"两种计算方法的差异: {abs(L - L_direct)}")
    print(f"验证结果: {'通过' if error < 1e-40 else '失败'}")
    print()

if __name__ == "__main__":
    verify_angular_momentum()
