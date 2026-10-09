import numpy as np
import pandas as pd
from scipy import stats

# 光速定义值
c = 299792458.0  # m/s

# 定义多尺度时间范围（跨越27个数量级）
time_scales = {
    '量子尺度': np.linspace(0, 1e-24, 100),
    '微观尺度': np.linspace(0, 1e-9, 100),
    '宏观尺度': np.linspace(0, 1e-6, 100),
    '天文尺度': np.linspace(0, 1e3, 100)
}

# 选择光速分量（二维平面运动）
Cx, Cy, Cz = 0.6 * c, 0.8 * c, 0.0 * c
# 归一化确保总速度为光速
norm_factor = c / np.sqrt(Cx**2 + Cy**2 + Cz**2)
Cx, Cy, Cz = Cx * norm_factor, Cy * norm_factor, Cz * norm_factor

# 宏观尺度线性回归分析
T_macro = time_scales['宏观尺度']
X_macro = c * T_macro

# 线性回归分析
slope, intercept, r_value, p_value, std_err = stats.linregress(T_macro, X_macro)
print(f"线性回归斜率: {slope:.2f} m/s (理论值: {c:.2f} m/s)")
print(f"相关系数: r = {r_value}")
print(f"标准误差: {std_err:.2e}")
print(f"相对误差: {(slope - c) / c * 100:.12f}%")