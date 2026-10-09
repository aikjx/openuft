import sympy as sp
from sympy import symbols, Function, diff, integrate, cos, sin

# 定义符号
A0, E0, omega, c, t, tau = symbols('A0 E0 omega c t tau')

# 手动计算矢量叉乘的函数
def vector_cross(a, b):
    """计算两个三维矢量的叉乘"""
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

# 定义时间函数
def define_vector_function(name):
    return [Function(f"{name}_x")(t), 
            Function(f"{name}_y")(t), 
            Function(f"{name}_z")(t)]

# 定义矢量函数
A = define_vector_function('A')  # 引力场强度
E = define_vector_function('E')  # 电场强度
V = define_vector_function('V')  # 物体速度

# 计算电场变化率
dE_dt = [diff(E[0], t), diff(E[1], t), diff(E[2], t)]

# 磁场变化率方程的三个分量
dBdt_x = (-vector_cross(A, E)[0] - vector_cross(V, dE_dt)[0]) / c**2
dBdt_y = (-vector_cross(A, E)[1] - vector_cross(V, dE_dt)[1]) / c**2
dBdt_z = (-vector_cross(A, E)[2] - vector_cross(V, dE_dt)[2]) / c**2

print("磁场变化率矢量分量：")
print(f"dB/dt_x = {dBdt_x}")
print(f"dB/dt_y = {dBdt_y}")
print(f"dB/dt_z = {dBdt_z}")

# 特殊情况：简谐变化场
# 定义具体的场函数
A_x_t = A0 * cos(omega * t)
A_y_t = 0
A_z_t = 0
A_vec = [A_x_t, A_y_t, A_z_t]

E_x_t = 0
E_y_t = E0 * sin(omega * t)
E_z_t = 0
E_vec = [E_x_t, E_y_t, E_z_t]

V_x_t = 0
V_y_t = 0
V_z_t = 0
V_vec = [V_x_t, V_y_t, V_z_t]

# 计算电场变化率
dE_dt_x = diff(E_x_t, t)
dE_dt_y = diff(E_y_t, t)
dE_dt_z = diff(E_z_t, t)
dE_dt_vec = [dE_dt_x, dE_dt_y, dE_dt_z]

# 计算dB/dt在特殊情况下的表达式
dBdt_special = vector_cross(A_vec, E_vec)
dBdt_special = [-comp - vector_cross(V_vec, dE_dt_vec)[i] for i, comp in enumerate(dBdt_special)]
dBdt_special = [comp / c**2 for comp in dBdt_special]

print(f"\n特殊情况下的磁场变化率分量：")
print(f"dB/dt_x = {dBdt_special[0]}")
print(f"dB/dt_y = {dBdt_special[1]}")
print(f"dB/dt_z = {dBdt_special[2]}")
print(f"dB/dt_z化简后：{sp.simplify(dBdt_special[2])}")

# 积分得到B(t)
B_z_t = integrate(dBdt_special[2], t)
print(f"\nB_z(t) = {B_z_t} + B_z(0)")
print(f"化简后：{sp.simplify(B_z_t)} + B_z(0)")

# 验证能量守恒
# 计算各场能量密度（标量近似）
U_A = (A0**2 * cos(omega*t)**2) / (2 * c**4)
U_E = (E0**2 * sin(omega*t)**2) / 2
U_B = (B_z_t**2) * c**2 / 2  # 简化近似

# 总能量密度
U_total = U_A + U_E + U_B
print(f"\n总能量密度对时间的导数：{sp.diff(U_total, t)}")
print(f"化简后：{sp.simplify(sp.diff(U_total, t))}")

# 额外验证：对偶关系检查
# 定义变化的引力场产生电场方程
E_from_A = -sp.diff(A0 * cos(omega*t), t)
print(f"\n由变化的引力场产生的电场：{E_from_A}")
print(f"化简后：{sp.simplify(E_from_A)}")

# 验证矢量叉乘的反对称性
cross_AB = vector_cross(A_vec, E_vec)
cross_BA = vector_cross(E_vec, A_vec)

print(f"\n叉乘反对称性验证：")
print(f"A×E = {cross_AB}")
print(f"B×A = {cross_BA}")
print(f"A×E + B×A = {[sp.simplify(a + b) for a, b in zip(cross_AB, cross_BA)]}")
