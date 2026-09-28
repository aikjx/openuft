import sympy as sp

# 定义符号变量
t = sp.Symbol('t')
G = sp.Symbol('G')
m = sp.Symbol('m')

# 定义矢量r的分量
theta = sp.Symbol('theta')  # 极角
phi = sp.Symbol('phi')      # 方位角
r_mag = sp.Function('r')(t)  # r的大小是时间的函数

# 将矢量r表示为球坐标系下的分量
r_x = r_mag * sp.sin(theta) * sp.cos(phi)
r_y = r_mag * sp.sin(theta) * sp.sin(phi)
r_z = r_mag * sp.cos(theta)

# 定义光速矢量c的分量（在球坐标系中，假设c沿径向方向）
c_x = sp.Symbol('c') * sp.sin(theta) * sp.cos(phi)
c_y = sp.Symbol('c') * sp.sin(theta) * sp.sin(phi)
c_z = sp.Symbol('c') * sp.cos(theta)

# 定义静引力场A的分量
A_x = -G * m * r_x / (r_mag ** 3)
A_y = -G * m * r_y / (r_mag ** 3)
A_z = -G * m * r_z / (r_mag ** 3)

# 计算A对时间的导数，得到D的分量
# 核心：应用时空同一化公设 dr/dt = c（矢量），而不是仅对r_mag求导
# 因此需要显式计算d/dt (r / r^3)，其中dr/dt = c

# 计算d/dt (r / r^3) 的x分量
# 使用商法则：d/dt (u/v) = (u'v - uv') / v^2
u_x = r_x
v = r_mag ** 3
du_dt_x = c_x  # 显式应用时空同一化公设：dr/dt = c
dv_dt = 3 * r_mag ** 2 * sp.diff(r_mag, t)
D_x = -G * m * (du_dt_x * v - u_x * dv_dt) / (v ** 2)

# 同样计算y和z分量
du_dt_y = c_y  # 显式应用时空同一化公设：dr/dt = c
D_y = -G * m * (du_dt_y * v - r_y * dv_dt) / (v ** 2)

du_dt_z = c_z  # 显式应用时空同一化公设：dr/dt = c
D_z = -G * m * (du_dt_z * v - r_z * dv_dt) / (v ** 2)

# 简化D的分量
dD_x = sp.simplify(D_x)
dD_y = sp.simplify(D_y)
dD_z = sp.simplify(D_z)

# 打印结果
print("=== 核力场分量计算结果 ===")
print("D_x =", dD_x)
print("D_y =", dD_y)
print("D_z =", dD_z)

# 计算理论预期结果的分量
dot_r = sp.diff(r_mag, t)  # r的大小对时间的导数
theoretical_D_x = -G * m * (c_x - 3 * (r_x / r_mag) * dot_r) / (r_mag ** 3)
theoretical_D_y = -G * m * (c_y - 3 * (r_y / r_mag) * dot_r) / (r_mag ** 3)
theoretical_D_z = -G * m * (c_z - 3 * (r_z / r_mag) * dot_r) / (r_mag ** 3)

# 简化理论结果
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

# 额外验证矢量求导的中间步骤
# 定义矢量函数 f = r / r^3
f_x = r_x / (r_mag ** 3)
f_y = r_y / (r_mag ** 3)
f_z = r_z / (r_mag ** 3)

# 计算df/dt，显式应用时空同一化公设 dr/dt = c
# 使用商法则：d/dt (u/v) = (u'v - uv') / v^2
v = r_mag ** 3
dv_dt = 3 * r_mag ** 2 * sp.diff(r_mag, t)

# 计算x分量
u_x = r_x
f_dot_x = (c_x * v - u_x * dv_dt) / (v ** 2)

# 计算y分量
u_y = r_y
f_dot_y = (c_y * v - u_y * dv_dt) / (v ** 2)

# 计算z分量
u_z = r_z
f_dot_z = (c_z * v - u_z * dv_dt) / (v ** 2)

simplified_f_dot_x = sp.simplify(f_dot_x)
simplified_f_dot_y = sp.simplify(f_dot_y)
simplified_f_dot_z = sp.simplify(f_dot_z)

print("\n=== 中间步骤验证：df/dt ===")
print("df/dt (x分量) =", simplified_f_dot_x)
print("df/dt (y分量) =", simplified_f_dot_y)
print("df/dt (z分量) =", simplified_f_dot_z)

# 理论上的df/dt应该是 [dr/dt - 3(r/r)dr/dt]/r^3
theoretical_f_dot_x = (c_x - 3 * (r_x / r_mag) * dot_r) / (r_mag ** 3)
theoretical_f_dot_y = (c_y - 3 * (r_y / r_mag) * dot_r) / (r_mag ** 3)
theoretical_f_dot_z = (c_z - 3 * (r_z / r_mag) * dot_r) / (r_mag ** 3)

p_theoretical_f_dot_x = sp.simplify(theoretical_f_dot_x)
p_theoretical_f_dot_y = sp.simplify(theoretical_f_dot_y)
p_theoretical_f_dot_z = sp.simplify(theoretical_f_dot_z)

print("\n=== 中间步骤理论预期：df/dt ===")
print("Theoretical df/dt (x分量) =", p_theoretical_f_dot_x)
print("Theoretical df/dt (y分量) =", p_theoretical_f_dot_y)
print("Theoretical df/dt (z分量) =", p_theoretical_f_dot_z)

print("\n=== 中间步骤验证结果 ===")
print("df/dt (x分量) 等于理论预期结果:", sp.simplify(simplified_f_dot_x - p_theoretical_f_dot_x) == 0)
print("df/dt (y分量) 等于理论预期结果:", sp.simplify(simplified_f_dot_y - p_theoretical_f_dot_y) == 0)
print("df/dt (z分量) 等于理论预期结果:", sp.simplify(simplified_f_dot_z - p_theoretical_f_dot_z) == 0)
