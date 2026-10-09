import sympy as sp

t = sp.Symbol('t')
C = sp.Symbol('C', constant = True, positive = True)

# 时空同一化方程:r(t) = Ct
r = C * t

# 对时间求一阶导数
v = sp.diff(r, t)
print(f"速度: v = dr/dt = {v}")

# 对时间求二阶导数
a = sp.diff(v, t)
print(f"加速度: a = dv/dt = {a}")



import numpy as np

# 光速值(m/s)
c = 299792458

# 时间点数组(s)
times = np.array([0, 1, 2, 3, 4, 5])

# 计算位置(m)
positions = c * times

# 验证位置与时间的线性关系
print("时间(s)与位置(m)的关系:")
for t, r in zip(times, positions):
    print(f"t = {t}, r = {r:.2e}")

# 计算速度(m/s)
velocities = np.gradient(positions, times)
print(f"计算得到的速度:{velocities[0]:.2e} m/s")
print(f"理论光速值:{c:.2e} m/s")
print(f"相对误差:{(velocities[0] - c) / c * 100:.10f}%")