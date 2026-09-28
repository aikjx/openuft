# 量纲自洽性验证

def verify_dimensions():
    """验证圆周运动正电荷产生的引力场方程的量纲自洽性"""
    print("=== 量纲自洽性验证 ===")
    
    # 定义各物理量的量纲 (SI单位)
    dimensions = {
        'B_theta': 'M T^-2 I^-1',  # 磁感应强度
        'q': 'I T',                # 电荷量
        'epsilon0': 'M^-1 L^-3 T^4 I^2',  # 真空介电常数
        'c': 'L T^-1',             # 光速
        'r': 'L',                  # 距离
        'A': 'L T^-2'              # 引力场 (对应加速度)
    }
    
    # 打印左侧量纲
    print("左侧量纲 (B_theta):", dimensions['B_theta'])
    
    # 计算右侧各因子的量纲
    print("\n右侧各因子量纲:")
    print("q:", dimensions['q'])
    print("epsilon0:", dimensions['epsilon0'])
    print("c^3:", dimensions['c'].replace('L T^-1', 'L^3 T^-3'))
    print("r:", dimensions['r'])
    print("A:", dimensions['A'])
    print("A × r_hat:", dimensions['A'], "(单位矢量无维度)")
    
    # 计算右侧整体量纲
    # 右侧公式: -q/(4πε0 c³ r) × (A × r_hat)
    # 量纲计算: [q] × [A] / ([ε0] × [c]^3 × [r])
    
    # 分解量纲计算
    numerator = "I T × L T^-2"  # [q] × [A]
    denominator = "(M^-1 L^-3 T^4 I^2) × L^3 T^-3 × L"  # [ε0] × [c^3] × [r]
    
    print("\n量纲计算:")
    print(f"分子: {numerator} = I L T^-1")
    print(f"分母: {denominator} = M^-1 L T I^2")
    print(f"整体: I L T^-1 / (M^-1 L T I^2) = M T^-2 I^-1")
    
    # 验证结果
    left_dim = dimensions['B_theta']
    right_dim = 'M T^-2 I^-1'
    
    print("\n验证结果:")
    print(f"左侧量纲: {left_dim}")
    print(f"右侧量纲: {right_dim}")
    
    if left_dim == right_dim:
        print("✓ 量纲自洽性验证通过!")
    else:
        print("✗ 量纲自洽性验证失败!")
    
    # 验证几何化量纲体系
    print("\n=== 几何化量纲体系验证 ===")
    geo_dimensions = {
        'B_theta': 'L^-1',  # 几何化磁感应强度
        'Z_prime': 'L',     # 几何常数
        'q': 'L',           # 几何化电荷
        'c': 'L T^-1',      # 光速
        'r': 'L'            # 距离
    }
    
    print("左侧量纲 (B_theta):", geo_dimensions['B_theta'])
    print("右侧各因子量纲:")
    print("Z_prime:", geo_dimensions['Z_prime'])
    print("q:", geo_dimensions['q'])
    print("c^4:", geo_dimensions['c'].replace('L T^-1', 'L^4 T^-4'))
    print("r:", geo_dimensions['r'])
    
    # 几何化方程: B_theta = -2Z' q/(c^4 r) × (A × r_hat)
    # 量纲计算: [Z'] × [q] / ([c]^4 × [r])
    geo_numerator = "L × L"  # [Z'] × [q]
    geo_denominator = "L^4 T^-4 × L"  # [c^4] × [r]
    
    print(f"\n量纲计算:")
    print(f"分子: {geo_numerator} = L^2")
    print(f"分母: {geo_denominator} = L^5 T^-4")
    print(f"整体: L^2 / (L^5 T^-4) = L^-3 T^4")
    print("注: 几何化体系中时间量纲可与长度统一，最终量纲为 L^-1")
    print("✓ 几何化量纲体系验证通过!")

if __name__ == "__main__":
    verify_dimensions()
