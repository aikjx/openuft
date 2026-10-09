import sympy as sp
from sympy.vector import CoordSys3D, curl, divergence

# 定义符号变量
t, r, omega, h = sp.symbols('t r omega h')

# 定义位置矢量的三个分量
x = r * sp.cos(omega * t)
y = r * sp.sin(omega * t)
z = h * t

# 计算速度矢量（一阶导数）
vx = sp.diff(x, t)
vy = sp.diff(y, t)
vz = sp.diff(z, t)

# 计算加速度矢量（二阶导数）
ax = sp.diff(vx, t)
ay = sp.diff(vy, t)
az = sp.diff(vz, t)

# 计算速度大小
v_magnitude = sp.simplify(sp.sqrt(vx**2 + vy**2 + vz**2))
print(f"速度大小: v = {v_magnitude}")

# 计算加速度大小
a_magnitude = sp.simplify(sp.sqrt(ax**2 + ay**2 + az**2))
print(f"加速度大小: a = {a_magnitude}")

# 计算曲率
curvature = sp.simplify(sp.sqrt(ax**2 + ay**2) / v_magnitude**3)
print(f"曲率: kappa = {curvature}")

# 计算螺距
pitch = 2 * sp.pi * h / omega
print(f"螺距: P = {pitch}")

# 创建三维坐标系进行矢量分析
R = CoordSys3D('R')
r_vec = r * sp.cos(omega * t) * R.i + r * sp.sin(omega * t) * R.j + h * t * R.k

# 计算速度矢量的旋度
v_vec = r_vec.diff(t)
curl_v = curl(v_vec, R)
print(f"速度矢量的旋度: ∇×v = {curl_v}")