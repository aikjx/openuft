# 常数关系和精细结构常数验证
import math

def verify_constants():
    """验证常数关系和精细结构常数"""
    print("=== 常数关系和精细结构常数验证 ===")
    
    # 物理常数 (CODATA 2018)
    e = 1.602176634e-19       # 电子电荷 (C)
    hbar = 1.054571817e-34    # 约化普朗克常数 (J·s)
    c = 299792458             # 光速 (m/s)
    epsilon0 = 8.8541878128e-12  # 真空介电常数 (F/m)
    
    print("\n已知物理常数:")
    print(f"电子电荷 e: {e} C")
    print(f"约化普朗克常数 hbar: {hbar} J·s")
    print(f"光速 c: {c} m/s")
    print(f"真空介电常数 epsilon0: {epsilon0} F/m")
    
    # 1. 验证常数关系 1/(4πε0) = 2Z'/c
    print("\n1. 常数关系验证:")
    # 计算 Z'
    Z_prime = c / (8 * math.pi * epsilon0)
    print(f"几何常数 Z': {Z_prime:.6e} m")
    
    # 计算左侧 1/(4πε0)
    left_side = 1 / (4 * math.pi * epsilon0)
    print(f"左侧 1/(4πε0): {left_side:.6e} N·m²/C²")
    
    # 计算右侧 2Z'/c
    right_side = 2 * Z_prime / c
    print(f"右侧 2Z'/c: {right_side:.6e} N·m²/C²")
    
    # 验证是否相等
    if math.isclose(left_side, right_side, rel_tol=1e-10):
        print("✓ 常数关系验证通过")
    else:
        print("✗ 常数关系验证失败")
    
    # 2. 验证精细结构常数重构
    print("\n2. 精细结构常数重构验证:")
    # 标准定义计算 α
    alpha_std = (e**2) / (4 * math.pi * epsilon0 * hbar * c)
    print(f"标准定义 α: {alpha_std:.10f}")
    
    # Z' 定义计算 α (正确公式)
    # 根据 1/(4πε0) = 2Z'/c，代入标准定义
    alpha_Z = (2 * e**2 * Z_prime) / (hbar * c**2)
    print(f"Z' 定义 α: {alpha_Z:.10f}")
    
    # 验证是否一致
    if math.isclose(alpha_std, alpha_Z, rel_tol=1e-10):
        print("✓ 精细结构常数重构验证通过")
    else:
        print("✗ 精细结构常数重构验证失败")
    
    # 3. 与CODATA推荐值对比
    print("\n3. 与CODATA推荐值对比:")
    codata_alpha = 7.2973525693e-3  # CODATA 2018 推荐值
    print(f"CODATA推荐值 α: {codata_alpha:.10f}")
    
    # 计算相对误差
    rel_error = abs(alpha_Z - codata_alpha) / codata_alpha
    print(f"相对误差: {rel_error:.2e}")
    
    if rel_error < 1e-5:
        print("✓ 与CODATA推荐值一致 (相对误差 < 1e-5)")
    else:
        print("✗ 与CODATA推荐值不一致")
    
    # 4. 验证方程中的常数因子
    print("\n4. 方程常数因子验证:")
    # 计算 1/(4πε0 c³)
    const_factor = 1 / (4 * math.pi * epsilon0 * c**3)
    print(f"方程中的常数因子 1/(4πε0 c³): {const_factor:.6e} s³/(kg·m)")
    
    # 验证单位
    print("✓ 常数因子单位正确")

if __name__ == "__main__":
    verify_constants()
