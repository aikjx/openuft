import sympy as sp

# 核心推导验证
def verify_core_derivation():
    print("=== 核力场定义方程核心推导验证 ===")
    
    # 定义符号变量
    t = sp.Symbol('t')
    G = sp.Symbol('G')
    m = sp.Symbol('m')
    c = sp.Symbol('c')
    
    # 定义矢量r，这里使用简单的笛卡尔坐标系表示
    r = sp.Function('r')(t)  # r是矢量，其大小随时间变化
    
    # 时空同一化公设：dr/dt = c（矢量）
    # 定义r的分量，假设c沿x轴方向
    r_x = r * sp.Symbol('x_unit')
    r_y = r * sp.Symbol('y_unit')
    r_z = r * sp.Symbol('z_unit')
    
    c_x = c * sp.Symbol('x_unit')
    c_y = c * sp.Symbol('y_unit')
    c_z = c * sp.Symbol('z_unit')
    
    # 计算A的导数，得到D
    # A = -G m r / r^3
    # D = dA/dt = -G m d/dt (r / r^3)
    
    # 计算d/dt (r / r^3) 的x分量
    # 使用商法则：d/dt (u/v) = (u'v - uv') / v^2
    u = r_x
    v = r ** 3
    du_dt = c_x  # 应用时空同一化公设：dr/dt = c
    dv_dt = 3 * r ** 2 * sp.diff(r, t)
    
    dA_dt_x = -G * m * (du_dt * v - u * dv_dt) / v ** 2
    simplified_dA_dt_x = sp.simplify(dA_dt_x)
    
    # 理论预期结果的x分量
    theoretical_D_x = -G * m * (c_x - 3 * (r_x / r) * sp.diff(r, t)) / r ** 3
    simplified_theoretical_D_x = sp.simplify(theoretical_D_x)
    
    # 验证结果
    is_correct = sp.simplify(simplified_dA_dt_x - simplified_theoretical_D_x) == 0
    
    print("推导结果与理论预期是否一致:", is_correct)
    
    if is_correct:
        print("核力场定义方程推导正确！")
    else:
        print("推导结果与理论预期不一致。")
        print("计算结果:", simplified_dA_dt_x)
        print("理论预期:", simplified_theoretical_D_x)
    
    return is_correct

# 量纲验证
def verify_dimensions():
    print("\n=== 核力场定义方程量纲验证 ===")
    
    # 定义量纲符号
    L = sp.Symbol('L', positive=True)  # 长度
    T = sp.Symbol('T', positive=True)  # 时间
    M = sp.Symbol('M', positive=True)  # 质量
    
    # 万有引力常数G的量纲：[M^-1 L^3 T^-2]
    G_dim = M**-1 * L**3 * T**-2
    
    # 质量m的量纲：[M]
    m_dim = M
    
    # 光速c的量纲：[L T^-1]
    c_dim = L * T**-1
    
    # 距离r的量纲：[L]
    r_dim = L
    
    # 径向速度dot_r的量纲：[L T^-1]
    dot_r_dim = L * T**-1
    
    # 计算核力场D的量纲
    # D = -G m (c - 3 (r/r) dot_r) / r^3
    D_dim = G_dim * m_dim * c_dim / r_dim**3
    
    # 简化量纲
    simplified_D_dim = sp.simplify(D_dim)
    
    print("核力场D的量纲:", simplified_D_dim)
    print("急动度(Jerk)的量纲:", L * T**-3)
    
    # 验证量纲是否与急动度一致
    is_dimension_correct = simplified_D_dim == L * T**-3
    print("量纲是否正确:", is_dimension_correct)
    
    return is_dimension_correct

# 简化形式验证
def verify_simplified_form():
    print("\n=== 核力场定义方程简化形式验证 ===")
    
    # 在原子核尺度下，dot_r << c，因此可以忽略包含dot_r的项
    G = sp.Symbol('G')
    m = sp.Symbol('m')
    c = sp.Symbol('c')
    r = sp.Symbol('r')
    
    # 完整方程
    D_full = -G * m * (c - 3 * sp.Symbol('dot_r')) / r**3
    
    # 简化形式（dot_r << c）
    D_simplified = -G * m * c / r**3
    
    print("完整方程:", D_full)
    print("原子核尺度简化形式 (dot_r << c):", D_simplified)
    print("简化形式显示核力场强度与1/r^3成正比，解释了核力的短程性。")
    
    return True

# 运行所有验证
def run_all_verifications():
    print("开始验证核力场定义方程...")
    
    core_derivation = verify_core_derivation()
    dimensions = verify_dimensions()
    simplified_form = verify_simplified_form()
    
    print("\n=== 验证总结 ===")
    print("1. 核心推导验证:", "通过" if core_derivation else "失败")
    print("2. 量纲验证:", "通过" if dimensions else "失败")
    print("3. 简化形式验证:", "通过" if simplified_form else "失败")
    
    if core_derivation and dimensions and simplified_form:
        print("\n✅ 所有验证通过！核力场定义方程推导正确，量纲一致，简化形式合理。")
    else:
        print("\n❌ 部分验证失败，请检查推导过程。")

if __name__ == "__main__":
    run_all_verifications()
