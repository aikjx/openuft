import sympy as sp
from sympy.vector import CoordSys3D, gradient

# 定义符号变量
t = sp.Symbol('t')
Cx = sp.Symbol('Cx', constant=True)
Cy = sp.Symbol('Cy', constant=True)
Cz = sp.Symbol('Cz', constant=True)

# 定义三维速度矢量
C_vector = sp.Matrix([Cx, Cy, Cz])
C = sp.sqrt(Cx**2 + Cy**2 + Cz**2)  # 光速大小

# 时空同一化方程: r = Ct
r_vector = C_vector * t
print(f"位置矢量: r = {r_vector}")

# 对时间求一阶导数(速度)
v_vector = r_vector.diff(t)
print(f"速度矢量: v = dr/dt = {v_vector}")

# 速度大小
v_magnitude = sp.sqrt(v_vector[0]**2 + v_vector[1]**2 + v_vector[2]**2)
print(f"速度大小: |v| = {v_magnitude}")

# 对时间求二阶导数(加速度)
a_vector = v_vector.diff(t)
print(f"加速度矢量: a = dv/dt = {a_vector}")

# 创建三维坐标系进行矢量分析
R = CoordSys3D('R')
r_vec = Cx * R.i * t + Cy * R.j * t + Cz * R.k * t

# 梯度分析
grad_r = gradient(r_vec.dot(R.i), R)  # x分量的梯度
print(f"x分量的梯度: ∇r_x = {grad_r}")