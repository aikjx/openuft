import matplotlib.pyplot as plt
import numpy as np

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 光速
c = 299792458.0

# 多尺度时间范围
time_scales = {
    '量子尺度': np.linspace(0, 1e-24, 100),
    '微观尺度': np.linspace(0, 1e-9, 100),
    '天文尺度': np.linspace(0, 1e3, 100)
}

plt.figure(figsize=(15, 12))

for i, (scale_name, t_scale) in enumerate(time_scales.items(), 1):
    x_scale = c * t_scale
    
    plt.subplot(3, 1, i)
    plt.plot(t_scale, x_scale, 'b-', linewidth=2)
    plt.title(f'{scale_name}空间运动分析 (t = {t_scale[0]:.2e}s 到 {t_scale[-1]:.2e}s)', fontsize=12)
    plt.xlabel('时间 (s)', fontsize=10)
    plt.ylabel('空间位置 (m)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 添加速度标注
    mid_idx = len(t_scale) // 2
    plt.annotate(f'v = {c:.2e} m/s', 
                 xy=(t_scale[mid_idx], x_scale[mid_idx]),
                 xytext=(t_scale[mid_idx], x_scale[mid_idx] * 1.1),
                 arrowprops=dict(facecolor='red', shrink=0.05, width=1.5),
                 fontsize=10)

plt.tight_layout()
plt.suptitle('时空同一化方程多尺度分析', fontsize=16, y=1.02)
plt.savefig('../visualizations/multiscale_analysis.png', dpi=300, bbox_inches='tight')
plt.show()