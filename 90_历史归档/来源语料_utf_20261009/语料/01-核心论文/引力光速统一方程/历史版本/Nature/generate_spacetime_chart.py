import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

try:
    # 避免显示窗口，直接保存图片
    plt.switch_backend('Agg')
    
    # 创建图形和3D轴
    fig = plt.figure(figsize=(10, 8), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    
    # 为了可视化方便，使用较小的比例因子
    scale_factor = 1
    c = 3  # 使用较小的数值代替3e8，便于可视化
    
    # 定义时空同一化方程：R = ct（缩放后）
    t = np.linspace(0, 5, 50)
    phi = np.linspace(0, 2*np.pi, 50)
    t_grid, phi_grid = np.meshgrid(t, phi)
    
    # 计算球面坐标（缩放后）
    r = c * t_grid * scale_factor
    x = r * np.cos(phi_grid)
    y = r * np.sin(phi_grid)
    z = t_grid  # 使用时间作为第三维
    
    # 绘制时空扩张的3D表面
    surf = ax.plot_surface(x, y, z, rstride=2, cstride=2, cmap=cm.viridis, 
                          alpha=0.8, linewidth=0.5, edgecolor='k')
    
    # 添加时间箭头表示时间流动
    t_arrow = 2.5
    r_arrow = c * t_arrow * scale_factor
    ax.quiver(r_arrow, 0, t_arrow, 0, 0, 1, color='r', linewidth=2, arrow_length_ratio=0.1)
    
    # 添加空间扩张箭头
    ax.quiver(0, 0, t_arrow, r_arrow/2, 0, 0, color='b', linewidth=2, arrow_length_ratio=0.1)
    
    # 添加公式标签
    ax.text(0, 0, 5.5, r'$R = ct$', fontsize=20, color='k', weight='bold')
    
    # 设置坐标轴标签
    ax.set_xlabel('X', fontsize=16)
    ax.set_ylabel('Y', fontsize=16)
    ax.set_zlabel('Time (t)', fontsize=16)
    
    # 设置坐标轴范围
    ax.set_xlim(-c*5*scale_factor/2, c*5*scale_factor/2)
    ax.set_ylim(-c*5*scale_factor/2, c*5*scale_factor/2)
    ax.set_zlim(0, 5)
    
    # 添加标题（英文，符合Nature格式）
    ax.set_title('3D Visualization of Spatiotemporal Identity', fontsize=18, pad=20)
    
    # 添加颜色条
    cbar = fig.colorbar(surf, ax=ax, shrink=0.6, aspect=10)
    cbar.set_label('Time Evolution', fontsize=14)
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 优化视角
    ax.view_init(elev=30, azim=45)
    
    # 保存为SVG格式
    save_path = r'd:\a10\aikjx\code\my_lib\utf\01-核心论文\引力光速统一方程\Nature\spacetime_unification.svg'
    plt.savefig(save_path, format='svg', dpi=300, bbox_inches='tight')
    print(f'Chart saved to: {save_path}')
    
    # 也保存为PNG格式作为备份
    png_path = save_path.replace('.svg', '.png')
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
    print(f'PNG version saved to: {png_path}')
    
    plt.close()
    
except Exception as e:
    print(f'Error generating chart: {str(e)}')
    # 如果3D绘图失败，创建一个简单的2D图表作为备选
    try:
        plt.figure(figsize=(10, 6), dpi=300)
        t = np.linspace(0, 5, 100)
        c = 3  # 缩放后的光速值
        r = c * t
        plt.plot(t, r, 'b-', linewidth=2)
        plt.xlabel('Time (t)', fontsize=14)
        plt.ylabel('Space Radius (R)', fontsize=14)
        plt.title('Spatiotemporal Identity: R = ct', fontsize=16)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.text(2, c*3, r'$R = ct$', fontsize=18, color='red', weight='bold')
        
        # 保存备选图表
        backup_path = r'd:\a10\aikjx\code\my_lib\utf\01-核心论文\引力光速统一方程\Nature\spacetime_unification_backup.svg'
        plt.savefig(backup_path, format='svg', dpi=300, bbox_inches='tight')
        print(f'Backup 2D chart saved to: {backup_path}')
        plt.close()
    except Exception as e2:
        print(f'Failed to generate even backup chart: {str(e2)}')
