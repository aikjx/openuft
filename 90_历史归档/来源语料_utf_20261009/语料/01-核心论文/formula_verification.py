import numpy as np
import sympy as sp

# 符号定义
t, R, omega, v0, c = sp.symbols('t R omega v0 c')
x, y, z = sp.symbols('x y z')

def verify_space_helical_motion():
    """验证空间螺旋运动的数学推导"""
    print("=" * 60)
    print("=== 空间螺旋运动验证 ===")
    print("=" * 60)
    
    # 位置矢量
    r = sp.Matrix([R*sp.cos(omega*t), R*sp.sin(omega*t), v0*t])
    print(f"\n📌 位置矢量:")
    print(f"   {r}")
    
    # 速度矢量
    v = r.diff(t)
    print(f"\n📌 速度矢量:")
    print(f"   {v}")
    
    # 速度大小
    v_magnitude = sp.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    print(f"\n📌 速度大小:")
    print(f"   {v_magnitude}")
    
    # 在真空中，v0 = c, omega = c/R
    v_magnitude_vacuum = v_magnitude.subs({v0: c, omega: c/R})
    print(f"\n📌 真空中速度大小:")
    print(f"   {v_magnitude_vacuum}")
    print(f"   简化后: {sp.simplify(v_magnitude_vacuum)}")
    
    # 加速度矢量
    a = v.diff(t)
    print(f"\n📌 加速度矢量:")
    print(f"   {a}")
    
    return r, v, a

def verify_four_dimensional_distance():
    """验证四维距离推导"""
    print("\n" + "=" * 60)
    print("=== 四维距离验证 ===")
    print("=" * 60)
    
    # 空间螺旋运动参数
    r = sp.Matrix([R*sp.cos(omega*t), R*sp.sin(omega*t), c*t])
    v = r.diff(t)
    
    # 微分
    dt = sp.Symbol('dt')
    dx = v[0] * dt
    dy = v[1] * dt
    dz = v[2] * dt
    
    # 四维距离
    dS2 = dx**2 + dy**2 + dz**2 - c**2 * dt**2
    print(f"\n📌 四维距离平方:")
    print(f"   {dS2}")
    
    # 代入 omega = c/R
    dS2_vacuum = dS2.subs({omega: c/R})
    print(f"\n📌 真空中四维距离平方:")
    print(f"   {dS2_vacuum}")
    print(f"   简化后: {sp.simplify(dS2_vacuum)}")
    
    return dS2

def verify_time_dilation():
    """验证时间膨胀公式推导"""
    print("\n" + "=" * 60)
    print("=== 时间膨胀验证 ===")
    print("=" * 60)
    
    # 时间定义
    phi = sp.Symbol('phi')
    t_def = sp.integrate(1/omega, phi)
    print(f"\n📌 时间定义:")
    print(f"   t = {t_def}")
    
    # 相对运动参考系中的角速度关系
    v = sp.Symbol('v')
    omega_prime = omega * sp.sqrt(1 - v**2/c**2)
    print(f"\n📌 运动参考系角速度:")
    print(f"   omega' = {omega_prime}")
    
    # 时间膨胀关系
    dt_prime = (omega / omega_prime) * sp.Symbol('dt')
    print(f"\n📌 时间微分关系:")
    print(f"   dt' = {dt_prime}")
    print(f"   简化后: {sp.simplify(dt_prime)}")
    
    return dt_prime

def verify_angular_momentum():
    """验证角动量计算"""
    print("\n" + "=" * 60)
    print("=== 角动量验证 ===")
    print("=" * 60)
    
    # 位置和速度矢量
    r = sp.Matrix([R*sp.cos(omega*t), R*sp.sin(omega*t), v0*t])
    v = r.diff(t)
    
    # 角动量 r × v
    cross_product = r.cross(v)
    print(f"\n📌 r × v:")
    print(f"   {cross_product}")
    
    # 简化轴向分量
    axial_component = cross_product[2]
    print(f"\n📌 轴向分量:")
    print(f"   {axial_component}")
    print(f"   简化后: {sp.simplify(axial_component)}")
    
    # 代入 omega = c/R, v0 = c
    axial_component_vacuum = axial_component.subs({omega: c/R, v0: c})
    print(f"\n📌 真空中轴向分量:")
    print(f"   {axial_component_vacuum}")
    print(f"   简化后: {sp.simplify(axial_component_vacuum)}")
    
    return cross_product

def verify_bell_inequality():
    """验证贝尔不等式推导"""
    print("\n" + "=" * 60)
    print("=== 贝尔不等式验证 ===")
    print("=" * 60)
    
    # 关联函数
    E_ab = sp.Symbol('E(a,b)')
    E_ac = sp.Symbol('E(a,c)')
    E_bc = sp.Symbol('E(b,c)')
    
    # 贝尔不等式推导
    expression = abs(E_ab - E_ac)
    print(f"\n📌 贝尔不等式:")
    print(f"   |E(a,b) - E(a,c)| ≤ 1 + E(b,c)")
    
    # 量子力学违反
    a = sp.Matrix([1, 0, 0])
    b = sp.Matrix([1/sp.sqrt(2), 1/sp.sqrt(2), 0])
    c = sp.Matrix([0, 1, 0])
    
    def dot_product(vec1, vec2):
        return sum(v1*v2 for v1, v2 in zip(vec1, vec2))
    
    E_ab_val = -dot_product(a, b)
    E_ac_val = -dot_product(a, c)
    E_bc_val = -dot_product(b, c)
    
    print(f"\n📌 量子力学计算值:")
    print(f"   E(a,b) = {E_ab_val}")
    print(f"   E(a,c) = {E_ac_val}")
    print(f"   E(b,c) = {E_bc_val}")
    print(f"   |E(a,b) - E(a,c)| = {abs(E_ab_val - E_ac_val)}")
    print(f"   1 + E(b,c) = {1 + E_bc_val}")
    print(f"   违反贝尔不等式: {abs(E_ab_val - E_ac_val) > 1 + E_bc_val}")
    
    return abs(E_ab_val - E_ac_val) > 1 + E_bc_val

if __name__ == "__main__":
    print("🚀 核心论文公式验证系统")
    print("=" * 60)
    
    verify_space_helical_motion()
    verify_four_dimensional_distance()
    verify_time_dilation()
    verify_angular_momentum()
    verify_bell_inequality()
    
    print("\n" + "=" * 60)
    print("🎉 验证完成!")
    print("=" * 60)