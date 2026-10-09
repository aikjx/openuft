import matplotlib.pyplot as plt
import numpy as np

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 光速
c = 299792458.0

# 宏观尺度时间范围
t_macro = np.linspace(0, 1e-6, 100)
x_macro = c * t_macro

# 创建可视化图表
plt.figure(figsize=(15, 7))

# 左侧：位置-时间关系图
plt.subplot(121)
plt.plot(t_macro, x_macro, 'b-', linewidth=2, label='空间位置')
plt.plot(t_macro, c * t_macro, 'r--', linewidth=1, label=f'理论线 (c = {c:.2e} m/s)')
plt.title('时空同一化方程: 空间位置随时间演化', fontsize=14)
plt.xlabel('时间 (s)', fontsize=12)
plt.ylabel('空间位置 (m)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# 右侧：拟合误差分析图
plt.subplot(122)
errors = x_macro - (c * t_macro)
plt.plot(t_macro, errors, 'g-', label='误差分析')
plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
plt.title('拟合误差分析', fontsize=14)
plt.xlabel('时间 (s)', fontsize=12)
plt.ylabel('误差 (m)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

plt.tight_layout()
plt.suptitle('时空同一化方程一维分析', fontsize=16, y=1.02)
plt.savefig('../visualizations/1d_position_time_analysis.png', dpi=300, bbox_inches='tight')
plt.show()