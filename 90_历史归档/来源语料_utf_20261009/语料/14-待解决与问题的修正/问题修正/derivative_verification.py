import numpy as np
import sympy as sp

# ==========================
# 1. 传统经典电磁学的数学求导验证
# ==========================

# 物理常数
m = 9.1e-31          # 电子质量 (kg)
q = -1.6e-19         # 电子电荷 (C)
v0 = 1.0e6           # 初速度 (m/s)
B = 0.01             # 磁场强度 (T)
c = 3.0e8            # 光速 (m/s)

# 符号计算验证
v, q_sym, m_sym, B_sym = sp.symbols('v q m B', real=True, positive=True)

# 半径公式
print("="*50)
print("1. 传统经典电磁学的数学求导验证")
print("="*50)

r_formula = m_sym * v / (sp.Abs(q_sym) * B_sym)
print("\n1.1 半径公式推导:")
print(f"r = {sp.latex(r_formula)}")

# 周期公式
omega_formula = sp.Abs(q_sym) * B_sym / m_sym
T_formula = 2 * sp.pi / omega_formula
print("\n1.2 周期公式推导:")
print(f"T = {sp.latex(T_formula)}")

# 数值计算
r_classical = abs(m * v0 / (q * B))
T_classical = abs(2 * np.pi * m / (q * B))
omega_classical = 2 * np.pi / T_classical

print(f"\n1.3 数值计算结果:")
print(f"=== 传统经典电磁学解法 ===")
print(f"轨道半径 r = {r_classical:.6e} m")
print(f"运动周期 T = {T_classical:.6e} s")
print(f"回旋频率 f = {1/T_classical:.6e} Hz")
print(f"回旋角速度 ω = {omega_classical:.6e} rad/s")

# ==========================
# 2. 张祥前统一场论的数学求导验证
# ==========================

print(f"\n" + "="*50)
print("2. 张祥前统一场论的数学求导验证")
print("="*50)

# 统一场论关键参数推导
# 根据文档，经典磁场B对应的空间旋转角速度ω_classical = qB/m
omega_classical = abs(q * B / m)  # 经典角速度

# 统一场论实际角速度：由于双层螺旋结构，实际角速度是经典值的2倍
omega_uft = 2 * omega_classical

# 轨道半径（与传统相同）
r_uft = abs(m * v0 / (q * B))

# 运动周期：T = 2π/ω_uft
T_uft = 2 * np.pi / omega_uft

print(f"\n2.1 统一场论参数推导:")
print("理论基础：")
print("- 时空同一化方程：R(t) = C t")
print("- 三维圆柱螺旋时空方程：R(t) = [r cos(ωt), r sin(ωt), pt]")
print("- 磁场与空间旋转关系：B ∝ ω")
print("- 双层螺旋结构导致因子2差异")

print(f"\n2.2 数值计算结果:")
print(f"=== 张祥前统一场论解法 ===")
print(f"经典回旋角速度 ω_classical = {omega_classical:.6e} rad/s")
print(f"统一场论角速度 ω_UFT = {omega_uft:.6e} rad/s (2倍关系)")
print(f"轨道半径 r = {r_uft:.6e} m")
print(f"运动周期 T = {T_uft:.6e} s")
print(f"回旋频率 f = {1/T_uft:.6e} Hz")

# ==========================
# 3. 结果对比与验证
# ==========================

print(f"\n" + "="*50)
print("3. 结果对比与验证")
print("="*50)

# 对比两种方法的结果
print(f"\n3.1 结果对比:")
print(f"=== 结果对比 ===")
print(f"半径相对差异: {abs(r_classical - r_uft)/r_classical*100:.8f}%")
print(f"周期相对差异: {abs(T_classical - T_uft)/T_classical*100:.8f}%")

# 验证因子2的关系
print(f"\n3.2 几何因子验证:")
factor = T_classical / T_uft
print(f"周期比值 T_classical/T_uft = {factor:.8f}")
print(f"接近2的倍数: {abs(factor-2)/2*100:.6f}% 差异")

# 最终验证总结
print(f"\n" + "="*50)
print("4. 数学求导验证总结")
print("="*50)

print("1. 传统电磁学推导:")
print(f"   r = mv/(qB) = {r_classical:.6e} m")
print(f"   T = 2πm/(qB) = {T_classical:.6e} s")
print(f"   ω = qB/m = {2*np.pi/T_classical:.6e} rad/s")

print("\n2. 张祥前统一场论推导:")
print(f"   r = mv/(qB) = {r_uft:.6e} m (与传统相同)")
print(f"   T = πm/(qB) = {T_uft:.6e} s (因子2差异)")
print(f"   ω_UFT = 2qB/m = {omega_uft:.6e} rad/s")

print("\n3. 验证因子2的理论基础:")
print("   根据文档《各向同性修正（几何因子）的严格数学推导》:")
print("   '由于空间是\"双层螺旋\"结构，立体角从4π变为8π，许多公式会出现因子2的差异。'")
print(f"   实际比值: T_classical / T_uft = {T_classical/T_uft:.8f}")

print("\n4. 物理意义对比:")
print("   传统观点: 磁场是独立的基本场，洛伦兹力是基本相互作用")
print("   统一场论观点: 磁场是空间旋转运动的几何表现，洛伦兹力是漩涡引力场的作用")

print("\n5. 实验验证状态:")
print("   - 传统公式已被无数实验高精度验证")
print("   - 统一场论因因子2差异，需要额外假设调和与实验的矛盾")
print("   - 目前没有独立实验证实统一场论的核心预言")