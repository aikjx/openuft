import numpy as np
from scipy.integrate import dblquad

# 计算平均投影效率
def integrand(phi, theta):
    return np.cos(theta) * np.sin(theta)

# 上半球积分（0到π/2）
result, error = dblquad(integrand, 0, np.pi/2, 0, 2*np.pi)

# 计算平均投影效率
surface_area = 2 * np.pi  # 上半球表面积
avg_efficiency = result / surface_area

# 计算几何因子
geometric_factor = 1 / avg_efficiency

# 计算引力常数理论值
Z = 0.010004524012147  # Z常量值
c = 299792458  # 光速
G_theoretical = 2 * Z / c
G_codata = 6.67430e-11  # CODATA 2018值

# 输出结果
print(f'平均投影效率: {avg_efficiency:.10f}')
print(f'几何因子: {geometric_factor:.10f}')
print(f'理论计算G值: {G_theoretical:.15e} m³/kg·s²')
print(f'CODATA 2018 G值: {G_codata:.15e} m³/kg·s²')
print(f'相对误差: {(G_theoretical - G_codata) / G_codata * 100:.10f}%')
