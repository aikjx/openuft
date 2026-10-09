import sympy as sp
from sympy.vector import CoordSys3D, gradient, divergence

# 创建三维坐标系
R = CoordSys3D('R')

# 定义符号变量
t, k, k_prime, epsilon_0 = sp.symbols('t k k_prime epsilon_0')
Omega = sp.Function('Omega')(t)  # 立体角是时间的函数

# 位置矢量和距离
r_vec = R.x*R.i + R.y*R.j + R.z*R.k
r = sp.sqrt(R.x**2 + R.y**2 + R.z**2)

# 电场定义方程
E = -k*k_prime/(4*sp.pi*epsilon_0*Omega**2)*sp.diff(Omega, t)*(r_vec/r**3)

print("电场定义方程:")
print(f"E = {E}")

# 计算电场的散度
div_E = divergence(E)
print("\n电场的散度:")
print(f"div(E) = {div_E}")

# 简化表达式
div_E_simplified = sp.simplify(div_E)
print("\n简化后的电场散度:")
print(f"div(E) = {div_E_simplified}")

# 验证高斯定理
# 对于点电荷，div(E) = ρ/epsilon_0
# 这里我们验证电场散度与电荷密度的关系
q = k_prime * k * (1 / Omega**2) * sp.diff(Omega, t)  # 电荷定义
rho = q * sp.DiracDelta(R.x) * sp.DiracDelta(R.y) * sp.DiracDelta(R.z)  # 点电荷密度
print("\n验证高斯定理:")
print(f"div(E) 应该等于 ρ/epsilon_0 = {rho/epsilon_0}")

# 计算电场的旋度
curl_E = sp.vector.curl(E)
curl_E_simplified = sp.simplify(curl_E)
print("\n电场的旋度:")
print(f"curl(E) = {curl_E_simplified}")

# 验证电场与库仑定律的关系
print("\n===== 电场与库仑定律的关系验证 =====")
# 从电场定义方程推导出库仑定律形式
expected_E_coulomb = -q / (4 * sp.pi * epsilon_0 * r**3) * r_vec
print(f"从电荷定义方程推导出的库仑定律形式: {expected_E_coulomb}")
print(f"电场定义方程: {E}")

# 比较两个表达式是否一致
expression_match = (sp.simplify(E - expected_E_coulomb) == 0)
print(f"\n电场定义方程与库仑定律形式是否一致: {expression_match}")

# 验证电场强度与距离平方反比关系
print("\n===== 电场强度与距离平方反比关系验证 =====")
# 计算电场强度的大小
E_magnitude = sp.sqrt(E.dot(E))
print(f"电场强度大小: {E_magnitude}")

# 简化电场强度大小
simplified_E_magnitude = sp.simplify(E_magnitude)
print(f"简化后的电场强度大小: {simplified_E_magnitude}")

# 检查是否包含1/r^2项
r_squared_term = 1/r**2
contains_inverse_square = (sp.simplify(simplified_E_magnitude / (q / (4 * sp.pi * epsilon_0 * r_squared_term))) == 1)
print(f"电场强度是否与距离平方成反比: {contains_inverse_square}")

# 验证电场的矢量方向
print("\n===== 电场矢量方向验证 =====")
# 计算电场方向与位置矢量方向的关系
dot_product = E.dot(r_vec)
print(f"电场与位置矢量的点积: {dot_product}")

# 简化点积
simplified_dot_product = sp.simplify(dot_product)
print(f"简化后的点积: {simplified_dot_product}")

# 检查点积是否为负（表明方向相反）
is_opposite_direction = (sp.simplify(simplified_dot_product / (q / (4 * sp.pi * epsilon_0 * r**2))) == -1)
print(f"电场方向是否与位置矢量方向相反: {is_opposite_direction}")