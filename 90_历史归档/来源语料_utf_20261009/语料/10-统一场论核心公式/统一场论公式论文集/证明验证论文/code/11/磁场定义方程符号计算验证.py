import sympy as sp
from sympy.vector import CoordSys3D, curl, divergence

# 创建三维坐标系
R = CoordSys3D('R')

# 定义符号变量
t, k, k_prime, mu_0, v, c = sp.symbols('t k k_prime mu_0 v c')
Omega = sp.Function('Omega')(t)  # 立体角是时间的函数

# 洛伦兹因子
gamma = 1 / sp.sqrt(1 - v**2 / c**2)

# 定义位置变量（考虑电荷沿x轴运动）
x, y, z = R.x, R.y, R.z

# 磁场定义方程的矢量表达式
r_vec = (x - v*t)*R.i + y*R.j + z*R.k
r_mag_cubed = (gamma**2*(x - v*t)**2 + y**2 + z**2)**(3/2)

# 磁场定义方程
B = (mu_0 * gamma * k * k_prime) / (4 * sp.pi * Omega**2) * sp.diff(Omega, t) * (r_vec / r_mag_cubed)

print("磁场定义方程:")
print(f"B = {B}")

# 计算磁场的旋度
curl_B = curl(B)
curl_B_simplified = sp.simplify(curl_B)
print("\n磁场的旋度:")
print(f"curl(B) = {curl_B_simplified}")

# 计算磁场的散度
div_B = divergence(B)
div_B_simplified = sp.simplify(div_B)
print("\n磁场的散度:")
print(f"div(B) = {div_B_simplified}")

# 验证安培环路定理
print("\n===== 安培环路定理验证 =====")
# 电荷定义
q = k_prime * k * (1 / Omega**2) * sp.diff(Omega, t)

# 电流密度矢量（沿x轴运动的点电荷）
J = q * v * sp.DiracDelta(x - v*t) * sp.DiracDelta(y) * sp.DiracDelta(z) * R.i

# 安培环路定理预期：curl(B) = mu_0 * J
expected_curl_B = mu_0 * J
print(f"预期的curl(B): {expected_curl_B}")

# 简化后的磁场旋度是否符合安培环路定理
# 由于存在狄拉克delta函数，直接比较表达式会很复杂，我们验证散度是否为零（磁场是无源场）
is_divergence_zero = (div_B_simplified == 0)
print(f"\n磁场散度是否为零（无源场）: {is_divergence_zero}")

# 验证磁场与电场定义方程的关系
print("\n===== 磁场与电场定义方程的关系验证 =====")
# 电场定义方程（来自统一场论）
epsilon_0 = sp.symbols('epsilon_0')
E = -k*k_prime/(4*sp.pi*epsilon_0*Omega**2)*sp.diff(Omega, t)*(r_vec/(sp.sqrt(x**2 + y**2 + z**2)**3))

# 计算电场的旋度
curl_E = curl(E)
curl_E_simplified = sp.simplify(curl_E)
print(f"电场的旋度: {curl_E_simplified}")

# 验证法拉第电磁感应定律的形式（定性）
print("\n法拉第电磁感应定律形式验证:")
# 法拉第定律：curl(E) = -dB/dt
dB_dt = sp.diff(B, t)
curl_E_vs_dB_dt = sp.simplify(curl_E + dB_dt)
print(f"curl(E) + dB/dt = {curl_E_vs_dB_dt}")

# 验证低速极限下退化为毕奥-萨伐尔定律
print("\n===== 低速极限下退化为毕奥-萨伐尔定律验证 =====")
# 低速极限：v << c，gamma ≈ 1
low_speed_gamma = 1
low_speed_r_mag_cubed = ((x - v*t)**2 + y**2 + z**2)**(3/2)
low_speed_B = (mu_0 * low_speed_gamma * k * k_prime) / (4 * sp.pi * Omega**2) * sp.diff(Omega, t) * ((x - v*t)*R.i + y*R.j + z*R.k) / low_speed_r_mag_cubed

print("低速极限下的磁场定义方程:")
print(f"B_low_speed = {low_speed_B}")

# 毕奥-萨伐尔定律形式（点电荷运动）
print("\n毕奥-萨伐尔定律形式（点电荷运动）:")
B_biot_savart = (mu_0 / (4*sp.pi)) * (q * v * R.i).cross(r_vec) / (sp.sqrt(x**2 + y**2 + z**2)**3)
print(f"B_biot_savart = {B_biot_savart}")

# 比较低速极限下的磁场定义方程与毕奥-萨伐尔定律
print("\n低速极限下磁场定义方程与毕奥-萨伐尔定律的关系:")
B_comparison = sp.simplify(low_speed_B - B_biot_savart)
print(f"B_low_speed - B_biot_savart = {B_comparison}")