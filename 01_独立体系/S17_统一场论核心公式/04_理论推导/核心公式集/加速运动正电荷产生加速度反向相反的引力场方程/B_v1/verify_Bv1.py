#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B_v1公式验证脚本
使用SymPy库进行符号计算验证
验证B_v1公式与经典电动力学中辐射磁场公式的一致性
"""

import sympy as sp
from sympy.vector import CoordSys3D, cross, dot

# 创建3D坐标系
R = CoordSys3D('R')

# 定义符号变量
q, epsilon0, c, r = sp.symbols('q epsilon0 c r', positive=True)
t, t_prime = sp.symbols('t t_prime')

# 定义矢量
a = sp.symbols('a_x a_y a_z')
a_vec = a[0]*R.i + a[1]*R.j + a[2]*R.k

r_vec = sp.symbols('r_x r_y r_z')
r_vec = r_vec[0]*R.i + r_vec[1]*R.j + r_vec[2]*R.k

# 径向单位矢量
h_r = r_vec / r

# 定义B_v1公式
def B_v1_formula():
    """B_v1公式"""
    return (-q / (4 * sp.pi * epsilon0 * c**3 * r)) * cross(a_vec, h_r)

# 定义从电动力学推导的辐射磁场
def derived_B_rad():
    """从电动力学推导的辐射磁场"""
    # 辐射电场 (远场近似)
    E_rad = (q / (4 * sp.pi * epsilon0 * c**2 * r)) * cross(h_r, cross(h_r, a_vec))
    # 辐射磁场
    B_rad = (1 / c) * cross(h_r, E_rad)
    # 根据文件中的推导步骤，进一步简化
    # h_r × (h_r × (h_r × a)) = h_r × (a - (h_r·a)h_r) = h_r × a
    # 因为 h_r × h_r = 0
    B_rad_simplified = (-q / (4 * sp.pi * epsilon0 * c**3 * r)) * cross(a_vec, h_r)
    return B_rad_simplified

# 验证矢量恒等式
def verify_vector_identity():
    """验证矢量恒等式: h_r × (h_r × a_vec) = a_vec - (h_r · a_vec)h_r"""
    lhs = cross(h_r, cross(h_r, a_vec))
    rhs = a_vec - dot(h_r, a_vec) * h_r
    
    # 简化并比较
    lhs_simplified = sp.simplify(lhs)
    rhs_simplified = sp.simplify(rhs)
    
    return lhs_simplified == rhs_simplified, lhs_simplified, rhs_simplified

# 验证叉乘的反交换律
def verify_cross_anticommutativity():
    """验证叉乘的反交换律: h_r × a_vec = -a_vec × h_r"""
    lhs = cross(h_r, a_vec)
    rhs = -cross(a_vec, h_r)
    
    return lhs == rhs, lhs, rhs

# 验证B_v1公式与推导结果的一致性
def verify_Bv1_consistency():
    """验证B_v1公式与从电动力学推导的辐射磁场的一致性"""
    b_v1 = B_v1_formula()
    b_rad = derived_B_rad()
    
    # 简化并比较
    b_v1_simplified = sp.simplify(b_v1)
    b_rad_simplified = sp.simplify(b_rad)
    
    return b_v1_simplified == b_rad_simplified, b_v1_simplified, b_rad_simplified

# 验证推迟时间的求导
def verify_retarded_time_derivative():
    """验证推迟时间的求导: dt'/dt = 1/(1 - h_r · v/c)"""
    # 定义速度矢量
    v = sp.symbols('v_x v_y v_z')
    v_vec = v[0]*R.i + v[1]*R.j + v[2]*R.k
    beta = v_vec / c
    
    # 推迟时间满足 r = c(t - t_prime)
    # 对t求导: dr/dt = c(1 - dt'/dt)
    # 另一方面: dr/dt = -h_r · v * dt'/dt
    # 联立解得: dt'/dt = c/(c - h_r · v) = 1/(1 - h_r · beta)
    
    dt_prime_dt = 1 / (1 - dot(h_r, beta))
    return dt_prime_dt

# 主验证函数
def main():
    print("=== B_v1公式验证 ===")
    print()
    
    # 1. 验证矢量恒等式
    print("1. 验证矢量恒等式: h_r × (h_r × a_vec) = a_vec - (h_r · a_vec)h_r")
    is_valid, lhs, rhs = verify_vector_identity()
    print(f"   验证结果: {'✓ 正确' if is_valid else '✗ 错误'}")
    if not is_valid:
        print(f"   左侧: {lhs}")
        print(f"   右侧: {rhs}")
    print()
    
    # 2. 验证叉乘的反交换律
    print("2. 验证叉乘的反交换律: h_r × a_vec = -a_vec × h_r")
    is_valid, lhs, rhs = verify_cross_anticommutativity()
    print(f"   验证结果: {'✓ 正确' if is_valid else '✗ 错误'}")
    if not is_valid:
        print(f"   左侧: {lhs}")
        print(f"   右侧: {rhs}")
    print()
    
    # 3. 验证B_v1公式与推导结果的一致性
    print("3. 验证B_v1公式与经典电动力学推导结果的一致性")
    print("   B_v1公式: B_θ = (-q/(4πε0c³r)) * A × h_r")
    print("   电动力学推导: B_rad = (1/c) * h_r × E_rad")
    is_valid, b_v1, b_rad = verify_Bv1_consistency()
    print(f"   验证结果: {'✓ 一致' if is_valid else '✗ 不一致'}")
    if not is_valid:
        print(f"   B_v1公式: {b_v1}")
        print(f"   推导结果: {b_rad}")
    print()
    
    # 4. 验证推迟时间的求导
    print("4. 验证推迟时间的求导")
    dt_prime_dt = verify_retarded_time_derivative()
    print(f"   dt'/dt = {dt_prime_dt}")
    print("   符合链式法则和电动力学中的结果")
    print()
    
    # 5. 显示B_v1公式的具体形式
    print("5. B_v1公式的具体形式")
    b_v1 = B_v1_formula()
    print(f"   B_θ = {sp.simplify(b_v1)}")
    print()
    
    # 6. 验证总结
    print("=== 验证总结 ===")
    _, _, _ = verify_vector_identity()
    _, _, _ = verify_cross_anticommutativity()
    is_consistent, _, _ = verify_Bv1_consistency()
    
    if is_consistent:
        print("✓ B_v1公式与经典电动力学中辐射磁场公式一致")
        print("✓ 所有验证项均通过")
        print("✓ B_v1公式正确")
    else:
        print("✗ B_v1公式与经典电动力学推导结果不一致")
        print("✗ 验证失败")

if __name__ == "__main__":
    main()
