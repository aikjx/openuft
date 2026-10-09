import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 参数设置
r = 1.0  # 半径
omega = 4.0  # 角速度
h = 3.0  # 螺距参数
c = 299792458.0  # 光速参考值

# 时间范围
t = np.linspace(0, 10, 1000)

# 计算位置坐标
x = r * np.cos(omega * t)
y = r * np.sin(omega * t)
z = h * t

# 计算速度分量（数值微分）
dt = t[1] - t[0]
vx = np.gradient(x, dt)
vy = np.gradient(y, dt)
vz = np.gradient(z, dt)

# 计算加速度分量（数值微分）
ax = np.gradient(vx, dt)
ay = np.gradient(vy, dt)
az = np.gradient(vz, dt)

# 计算速度和加速度大小
v_mag = np.sqrt(vx**2 + vy**2 + vz**2)
a_mag = np.sqrt(ax**2 + ay**2 + az**2)

# 理论值
v_theory = np.sqrt(r**2 * omega**2 + h**2)
a_theory = r * omega**2

# 统计分析
v_mean = np.mean(v_mag)
v_std = np.std(v_mag)
a_mean = np.mean(a_mag)
a_std = np.std(a_mag)

print(f"理论速度大小: {v_theory:.6f}")
print(f"数值模拟平均速度: {v_mean:.6f}")
print(f"速度标准差: {v_std:.6e}")
print(f"速度相对误差: {(v_mean - v_theory) / v_theory * 100:.12f}%")
print(f"\n理论加速度大小: {a_theory:.6f}")
print(f"数值模拟平均加速度: {a_mean:.6f}")
print(f"加速度标准差: {a_std:.6e}")
print(f"加速度相对误差: {(a_mean - a_theory) / a_theory * 100:.12f}%")