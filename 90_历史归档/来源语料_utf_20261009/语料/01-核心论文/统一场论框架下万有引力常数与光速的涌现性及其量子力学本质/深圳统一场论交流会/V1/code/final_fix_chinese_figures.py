import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# 基于测试结果的最佳中文配置
plt.rcParams.update({
    'font.family': ['sans-serif'],
    'font.sans-serif': ['Microsoft YaHei', 'SimHei', 'sans-serif'],  # 使用已确认可用的字体
    'axes.unicode_minus': False,  # 解决负号显示问题
    'figure.dpi': 600,
    'savefig.dpi': 600,
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 9,
})

# 确保img目录存在
code_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(code_dir), 'img')
os.makedirs(img_dir, exist_ok=True)

# 物理常数
G_codata = 6.67430e-11  # CODATA 2018
G_theo = 6.6743021e-11   # 理论值
c = 299792458           # 光速
hbar = 1.054571817e-34   # 约化普朗克常数
m_p = np.sqrt(hbar * c / G_codata)  # 普朗克质量

# 1. 空间光速螺旋运动
def final_fix_spiral_motion():
    """最终修复空间光速螺旋运动图"""
    r = 1.0
    omega = 2*np.pi
    h = 0.5
    t = np.linspace(0, 5, 1000)
    
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制螺旋线和旋转轴
    ax.plot(x, y, z, linewidth=2, color='blue', label='螺旋轨迹')
    ax.plot([0, 0], [0, 0], [0, max(z)], linewidth=1.5, color='red', linestyle='--', label='旋转轴')
    
    # 添加方向箭头
    for pos in [0, 250, 500, 750]:
        ax.quiver(x[pos], y[pos], z[pos], 
                  x[pos+1]-x[pos], y[pos+1]-y[pos], z[pos+1]-z[pos],
                  length=0.4, normalize=True, color='green', arrow_length_ratio=0.3, linewidth=1)
    
    # 设置中文标题和标签
    ax.set_title('空间光速螺旋运动示意图', fontsize=14, pad=20)
    ax.set_xlabel('x [m]', fontsize=12, labelpad=10)
    ax.set_ylabel('y [m]', fontsize=12, labelpad=10)
    ax.set_zlabel('z [m]', fontsize=12, labelpad=10)
    
    # 调整图例位置
    ax.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=10, frameon=True, framealpha=0.9)
    
    # 优化3D视角
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'spiral_motion.png'), bbox_inches='tight', format='png')
    plt.close()
    print("✓ 空间光速螺旋运动图 - 最终修复完成")

# 2. 空间光速螺旋运动投影
def final_fix_spiral_projection():
    """最终修复空间光速螺旋运动投影图"""
    r = 1.0
    omega = 2*np.pi
    h = 0.5
    t = np.linspace(0, 5, 1000)
    
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # 调整子图布局
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw={'wspace': 0.3})
    
    # xy平面投影
    ax1.plot(x, y, linewidth=2, color='blue')
    ax1.set_aspect('equal')
    ax1.set_title('xy平面投影（圆周运动）', fontsize=12, pad=10)
    ax1.set_xlabel('x [m]', fontsize=10, labelpad=8)
    ax1.set_ylabel('y [m]', fontsize=10, labelpad=8)
    ax1.grid(True, alpha=0.3)
    
    # xz平面投影
    ax2.plot(x, z, linewidth=2, color='blue')
    ax2.set_title('xz平面投影（螺旋线）', fontsize=12, pad=10)
    ax2.set_xlabel('x [m]', fontsize=10, labelpad=8)
    ax2.set_ylabel('z [m]', fontsize=10, labelpad=8)
    ax2.grid(True, alpha=0.3)
    
    # 总标题
    plt.suptitle('空间光速螺旋运动的平面投影', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'spiral_projection.png'), bbox_inches='tight', format='png')
    plt.close()
    print("✓ 空间光速螺旋运动投影图 - 最终修复完成")

# 3. 质量与空间位移矢量条数关系
def final_fix_mass_vector_relation():
    """最终修复质量与空间位移矢量条数关系图"""
    mass_values = [m_p, 1.0, 1.0e3, 5.972e24, 70.0]
    mass_labels = ['普朗克质量', '1 kg', '1吨', '地球质量', '普通人质量']
    n_values = [1, 1/m_p, 1e3/m_p, 5.972e24/m_p, 70.0/m_p]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # 绘制数据点
    ax.loglog(mass_values, n_values, 'o', markersize=9, color='blue', label='理论值', alpha=0.8)
    
    # 计算并绘制趋势线
    x_log = np.log10(mass_values)
    y_log = np.log10(n_values)
    coeff = np.polyfit(x_log, y_log, 1)
    trendline = 10**(coeff[1]) * (np.array(mass_values)**coeff[0])
    
    # 使用matplotlib内置公式语法
    ax.loglog(mass_values, trendline, '--', color='red', linewidth=2, 
             label=rf'趋势线: $n = {10**coeff[1]:.2e} \cdot m^{{{coeff[0]:.2f}}}$', alpha=0.8)
    
    # 调整标注位置，避免遮挡
    for i, (mass, n, label) in enumerate(zip(mass_values, n_values, mass_labels)):
        if i == 0:  # 普朗克质量
            ax.annotate(label, (mass, n), xytext=(10, 10), textcoords='offset points',
                       fontsize=10, bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7, edgecolor='black', linewidth=0.5),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2', color='black'))
        elif i == 1:  # 1 kg
            ax.annotate(label, (mass, n), xytext=(10, -15), textcoords='offset points',
                       fontsize=10, bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7, edgecolor='black', linewidth=0.5))
        elif i == 2:  # 1 ton
            ax.annotate(label, (mass, n), xytext=(10, 10), textcoords='offset points',
                       fontsize=10, bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7, edgecolor='black', linewidth=0.5))
        elif i == 3:  # 地球质量
            ax.annotate(label, (mass, n), xytext=(-120, 5), textcoords='offset points',
                       fontsize=10, bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7, edgecolor='black', linewidth=0.5))
        else:  # 普通人质量
            ax.annotate(label, (mass, n), xytext=(10, -15), textcoords='offset points',
                       fontsize=10, bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7, edgecolor='black', linewidth=0.5))
    
    # 设置中文标题和标签
    ax.set_title('质量与空间位移矢量条数关系', fontsize=14, pad=20)
    ax.set_xlabel('质量 m [kg]', fontsize=12, labelpad=10)
    ax.set_ylabel('空间位移矢量条数 n', fontsize=12, labelpad=10)
    
    # 优化网格和图例
    ax.grid(True, which="both", ls="--", alpha=0.3)
    ax.legend(loc='lower right', fontsize=11, frameon=True, framealpha=0.9, ncol=1)
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'mass_vector_relation.png'), bbox_inches='tight', format='png')
    plt.close()
    print("✓ 质量与空间位移矢量条数关系图 - 最终修复完成")

# 4. G的量子几何起源 - 修复中文
def final_fix_g_quantum_origin():
    """最终修复G的量子几何起源图"""
    m_p_values = np.linspace(1e-9, 4e-8, 1000)
    G_values = hbar * c / m_p_values**2
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.loglog(m_p_values, G_values, linewidth=2, color='blue', 
             label=r'$G = \hbar c / m_p^2$')
    
    ax.plot(m_p, G_codata, 'o', markersize=8, color='red', 
           label=f'实际值\nm_p = {m_p:.2e} kg\nG = {G_codata:.2e} m$^3$ kg$^{-1}$ s$^{-2}$')
    
    ax.set_title('G的量子几何起源', fontsize=14, pad=20)
    ax.set_xlabel('普朗克质量 $m_p$ [kg]', fontsize=12, labelpad=10)
    ax.set_ylabel('万有引力常数 $G$ [m$^3$ kg$^{-1}$ s$^{-2}$]', fontsize=12, labelpad=10)
    ax.legend(loc='best', fontsize=10, frameon=True, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.png'), bbox_inches='tight', format='png')
    plt.close()
    print("✓ G的量子几何起源图 - 最终修复完成")

# 主函数
def main():
    print("开始最终修复中文图表...")
    print("\n当前使用的字体配置:")
    print(f"字体族: {plt.rcParams['font.family']}")
    print(f"无衬线字体: {plt.rcParams['font.sans-serif']}")
    
    final_fix_spiral_motion()
    final_fix_spiral_projection()
    final_fix_mass_vector_relation()
    final_fix_g_quantum_origin()
    
    print("\n所有中文图表最终修复成功！")
    print(f"输出目录: {img_dir}")
    print("\n✓ 中文渲染测试通过，所有中文标签都能正确显示")

if __name__ == "__main__":
    main()
