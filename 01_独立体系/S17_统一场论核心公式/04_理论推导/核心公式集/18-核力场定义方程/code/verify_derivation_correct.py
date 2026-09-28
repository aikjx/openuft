import sympy as sp

# 定义符号变量
t = sp.Symbol('t')
G = sp.Symbol('G')
m = sp.Symbol('m')
c = sp.Symbol('c')

# 定义矢量r的分量
theta = sp.Symbol('theta')  # 极角
phi = sp.Symbol('phi')      # 方位角
r_mag = sp.Function('r')(t)  # r的大小是时间的函数

# 将矢量r表示为球坐标系下的分量
r_x = r_mag * sp.sin(theta) * sp.cos(phi)
r_y = r_mag * sp.sin(theta) * sp.sin(phi)
r_z = r_mag * sp.cos(theta)

# 定义静引力场A的分量
A_x = -G * m * r_x / (r_mag ** 3)
A_y = -G * m * r_y / (r_mag ** 3)
A_z = -G * m * r_z / (r_mag ** 3)

# 时空同一化公设：dr/dt = c（这里dr是矢量，dt是标量）
# 因此，矢量r对时间的导数等于光速矢量c
# 即 dr/dt = c，所以 dr_x/dt = c_x, dr_y/dt = c_y, dr_z/dt = c_z
# 其中c_x, c_y, c_z是光速矢量c的分量
c_x = c * sp.sin(theta) * sp.cos(phi)
c_y = c * sp.sin(theta) * sp.sin(phi)
c_z = c * sp.cos(theta)

# 计算A对时间的导数，得到D的分量
# 应用链式法则和商法则
# d/dt (r / r^3) = (dr/dt * r^3 - r * d(r^3)/dt) / r^6

# 计算d(r^3)/dt
d_r3_dt = 3 * r_mag ** 2 * sp.diff(r_mag, t)

dot_r = sp.diff(r_mag, t)  # r的大小对时间的导数

# 计算每个分量的导数
# D_x = -Gm * d/dt (r_x / r^3)
# 使用商法则：d/dt (u/v) = (u'v - uv') / v^2
u_x = r_x
v_x = r_mag ** 3
du_x_dt = c_x  # 应用时空同一化公设：dr_x/dt = c_x
dv_x_dt = d_r3_dt
D_x = -G * m * (du_x_dt * v_x - u_x * dv_x_dt) / (v_x ** 2)

dD_x = sp.simplify(D_x)

u_y = r_y
v_y = r_mag ** 3
du_y_dt = c_y  # 应用时空同一化公设：dr_y/dt = c_y
dv_y_dt = d_r3_dt
D_y = -G * m * (du_y_dt * v_y - u_y * dv_y_dt) / (v_y ** 2)

dD_y = sp.simplify(D_y)

u_z = r_z
v_z = r_mag ** 3
du_z_dt = c_z  # 应用时空同一化公设：dr_z/dt = c_z
dv_z_dt = d_r3_dt
D_z = -G * m * (du_z_dt * v_z - u_z * dv_z_dt) / (v_z ** 2)

dD_z = sp.simplify(D_z)

# 打印结果
print("=== 核力场分量计算结果 ===")
print("D_x =", dD_x)
print("D_y =", dD_y)
print("D_z =", dD_z)

# 计算理论预期结果的分量
theoretical_D_x = -G * m * (c_x - 3 * (r_x / r_mag) * dot_r) / (r_mag ** 3)
theoretical_D_y = -G * m * (c_y - 3 * (r_y / r_mag) * dot_r) / (r_mag ** 3)
theoretical_D_z = -G * m * (c_z - 3 * (r_z / r_mag) * dot_r) / (r_mag ** 3)

p_theoretical_D_x = sp.simplify(theoretical_D_x)
p_theoretical_D_y = sp.simplify(theoretical_D_y)
p_theoretical_D_z = sp.simplify(theoretical_D_z)

print("\n=== 理论预期结果 ===")
print("Theoretical D_x =", p_theoretical_D_x)
print("Theoretical D_y =", p_theoretical_D_y)
print("Theoretical D_z =", p_theoretical_D_z)

# 验证计算结果是否与理论结果一致
print("\n=== 验证结果 ===")
print("D_x 等于理论预期结果:", sp.simplify(dD_x - p_theoretical_D_x) == 0)
print("D_y 等于理论预期结果:", sp.simplify(dD_y - p_theoretical_D_y) == 0)
print("D_z 等于理论预期结果:", sp.simplify(dD_z - p_theoretical_D_z) == 0)

# 提取共同的因子，简化验证
print("\n=== 提取共同因子后的简化验证 ===")
# 从D_x和theoretical_D_x中提取共同因子
common_factor_x = sp.sin(theta) * sp.cos(phi) / (r_mag ** 3)
dD_x_simplified = dD_x / (G * m * common_factor_x)
theoretical_D_x_simplified = p_theoretical_D_x / (G * m * common_factor_x)
print("D_x 简化后 =", dD_x_simplified)
print("理论 D_x 简化后 =", theoretical_D_x_simplified)
print("D_x 简化后是否相等:", sp.simplify(dD_x_simplified - theoretical_D_x_simplified) == 0)
