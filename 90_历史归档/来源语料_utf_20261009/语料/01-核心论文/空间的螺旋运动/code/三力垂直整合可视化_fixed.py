import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter
import sympy as sp

# 设置中文字体和样式
import matplotlib
# 确保使用正确的中文字体
matplotlib.rcParams['font.family'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')

# 尝试直接设置字体路径（针对Windows系统）
try:
    import os
    # 检查系统中是否有微软雅黑字体
    msyh_path = r'C:\Windows\Fonts\msyh.ttc'
    if os.path.exists(msyh_path):
        matplotlib.font_manager.fontManager.addfont(msyh_path)
        matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
except Exception as e:
    print(f"设置字体路径时出错：{e}")

# 定义全局常量
c = 3e8  # 光速 m/s

def main():
    """主函数"""
    print("=== 空间螺旋运动、加速正电荷与三力垂直的整合求导验证 ===")
    print("="*60)
    
    # 1. 理论推导与数学求导
    print("\n1. 理论推导与数学求导")
    t, r, omega, p, a, E_y, v = sp.symbols('t r omega p a E_y v', real=True)
    
    # 空间螺旋运动方程
    R = sp.Matrix([r*sp.cos(omega*t), r*sp.sin(omega*t), p*t])
    print("=== 空间螺旋运动方程 ===")
    print(f"R(t) = {R}")
    
    # 速度矢量
    V = R.diff(t)
    print(f"\n速度矢量 V(t) = dR/dt = {V}")
    
    # 加速度矢量
    a_vec = V.diff(t)
    print(f"\n加速度矢量 a(t) = dV/dt = {a_vec}")
    
    # 引力场定义
    A = -a_vec
    print(f"\n引力场 A = -dV/dt = {A}")
    
    # 磁场定义
    E = sp.Matrix([0, E_y, 0])
    V_charge = sp.Matrix([v, 0, 0])
    B = (1/c**2) * V_charge.cross(E)
    print(f"\n磁场 B = (V × E)/c² = {B}")
    
    # 变化磁场
    dBdt = B.diff(t)
    print(f"\n变化磁场 dB/dt = {dBdt}")
    
    # 三力垂直的核心方程
    A_charge = sp.Matrix([-a, 0, 0])
    core_eq = (-1/c**2) * A_charge.cross(E)
    print(f"\n核心方程 dB/dt = -1/c² (A × E) = {core_eq}")
    
    # 2. 空间螺旋运动可视化
    print("\n2. 创建空间螺旋运动可视化")
    visualize_spiral_motion()
    
    # 3. 三力垂直可视化
    print("3. 创建三力垂直可视化")
    visualize_three_forces()
    
    # 4. 综合可视化
    print("4. 创建综合可视化")
    create_comprehensive_visualization()
    
    # 5. 创建动画
    print("5. 创建动态动画")
    create_animation()
    
    print("\n" + "="*60)
    print("可视化完成！生成的文件：")
    print("1. 螺旋运动详细可视化.png")
    print("2. 三力垂直可视化.png")
    print("3. 综合可视化.png")
    print("4. 空间螺旋运动动态演示.gif")
    print("="*60)

def visualize_spiral_motion():
    """空间螺旋运动可视化"""
    # 参数设置
    r_plot = 2.0
    omega_plot = 3.0
    p_plot = 4.0
    t_range = np.linspace(0, 2*np.pi/omega_plot*3, 200)
    
    # 计算螺旋轨迹
    x = r_plot * np.cos(omega_plot * t_range)
    y = r_plot * np.sin(omega_plot * t_range)
    z = p_plot * t_range
    
    # 计算速度和加速度
    vx = -r_plot * omega_plot * np.sin(omega_plot * t_range)
    vy = r_plot * omega_plot * np.cos(omega_plot * t_range)
    vz = np.full_like(t_range, p_plot)
    
    ax = -r_plot * omega_plot**2 * np.cos(omega_plot * t_range)
    ay = -r_plot * omega_plot**2 * np.sin(omega_plot * t_range)
    az = np.zeros_like(t_range)
    
    # 创建可视化
    fig = plt.figure(figsize=(16, 12))
    
    # 3D螺旋轨迹与矢量场
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.plot(x, y, z, 'b-', linewidth=2, alpha=0.8, label='螺旋轨迹')
    
    # 绘制速度矢量
    stride = 10
    ax1.quiver(x[::stride], y[::stride], z[::stride], 
              vx[::stride]*0.1, vy[::stride]*0.1, vz[::stride]*0.1, 
              color='g', length=0.5, normalize=True, label='速度矢量')
    
    # 绘制加速度矢量
    ax1.quiver(x[::stride], y[::stride], z[::stride], 
              ax[::stride]*0.2, ay[::stride]*0.2, az[::stride]*0.2, 
              color='r', length=0.5, normalize=True, label='加速度矢量')
    
    ax1.set_title('(1) 空间螺旋运动3D轨迹与矢量场', fontsize=12, fontweight='bold')
    ax1.set_xlabel('X轴', fontsize=10)
    ax1.set_ylabel('Y轴', fontsize=10)
    ax1.set_zlabel('Z轴', fontsize=10)
    ax1.legend(fontsize=9, loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # 速度分量随时间变化
    ax2 = fig.add_subplot(222)
    ax2.plot(t_range, vx, 'r-', linewidth=2, alpha=0.7, label='vₓ (旋转分量)')
    ax2.plot(t_range, vy, 'g-', linewidth=2, alpha=0.7, label='vᵧ (旋转分量)')
    ax2.plot(t_range, vz, 'b-', linewidth=2, alpha=0.7, label='v_z (轴向分量)')
    ax2.set_title('(2) 速度分量随时间变化', fontsize=12, fontweight='bold')
    ax2.set_xlabel('时间 t', fontsize=10)
    ax2.set_ylabel('速度分量', fontsize=10)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # 加速度分量随时间变化
    ax3 = fig.add_subplot(223)
    ax3.plot(t_range, ax, 'r--', linewidth=2, alpha=0.7, label='aₓ')
    ax3.plot(t_range, ay, 'g--', linewidth=2, alpha=0.7, label='aᵧ')
    ax3.plot(t_range, az, 'b--', linewidth=2, alpha=0.7, label='a_z')
    ax3.set_title('(3) 加速度分量随时间变化', fontsize=12, fontweight='bold')
    ax3.set_xlabel('时间 t', fontsize=10)
    ax3.set_ylabel('加速度分量', fontsize=10)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # XY平面投影
    ax4 = fig.add_subplot(224)
    ax4.plot(x, y, 'orange', linewidth=2, alpha=0.7, label='XY平面投影（圆形轨迹）')
    ax4.set_aspect('equal')
    ax4.set_title('(4) XY平面投影', fontsize=12, fontweight='bold')
    ax4.set_xlabel('X轴', fontsize=10)
    ax4.set_ylabel('Y轴', fontsize=10)
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('螺旋运动详细可视化.png', dpi=300, bbox_inches='tight')
    plt.close()

def visualize_three_forces():
    """加速正电荷与三力垂直可视化"""
    # 参数设置
    a_val = 1.0
    E_val = 1.0
    
    # 定义场向量
    A_vec = np.array([-a_val, 0, 0])  # 引力场沿 -x 方向
    E_vec = np.array([0, E_val, 0])     # 电场沿 +y 方向
    dBdt_vec = (a_val * E_val / c**2) * np.array([0, 0, 1])  # 变化磁场沿 +z 方向
    
    # 创建可视化
    fig = plt.figure(figsize=(15, 10))
    
    # 3D矢量场可视化
    ax1 = fig.add_subplot(121, projection='3d')
    
    # 绘制坐标系
    ax1.quiver(0, 0, 0, 3, 0, 0, color='k', arrow_length_ratio=0.1, linewidth=1.5, label='X轴')
    ax1.quiver(0, 0, 0, 0, 3, 0, color='k', arrow_length_ratio=0.1, linewidth=1.5, label='Y轴')
    ax1.quiver(0, 0, 0, 0, 0, 3, color='k', arrow_length_ratio=0.1, linewidth=1.5, label='Z轴')
    
    # 绘制场向量
    scale = 2.0
    
    # 引力场 A (蓝色)
    ax1.quiver(0, 0, 0, A_vec[0]*scale, A_vec[1]*scale, A_vec[2]*scale, 
              color='#1f77b4', arrow_length_ratio=0.1, linewidth=2.5, 
              label=f'引力场 A = {A_vec}')
    
    # 电场 E (红色)
    ax1.quiver(0, 0, 0, E_vec[0]*scale, E_vec[1]*scale, E_vec[2]*scale, 
              color='#d62728', arrow_length_ratio=0.1, linewidth=2.5, 
              label=f'电场 E = {E_vec}')
    
    # 变化磁场 dB/dt (绿色)
    ax1.quiver(0, 0, 0, dBdt_vec[0]*scale*1e16, dBdt_vec[1]*scale*1e16, dBdt_vec[2]*scale*1e16, 
              color='#2ca02c', arrow_length_ratio=0.1, linewidth=2.5, 
              label=f'变化磁场 ∂B/∂t = {[f"{x:.2e}" for x in dBdt_vec]}')
    
    # 添加正电荷
    ax1.scatter(0, 0, 0, s=200, c='gold', marker='o', edgecolor='k', linewidth=2, 
               label='正电荷')
    
    # 设置坐标轴范围
    max_range = 3.5
    ax1.set_xlim(-max_range, max_range)
    ax1.set_ylim(-max_range, max_range)
    ax1.set_zlim(-max_range, max_range)
    
    ax1.set_title('(1) 三力垂直矢量场可视化', fontsize=14, fontweight='bold')
    ax1.set_xlabel('X轴', fontsize=12)
    ax1.set_ylabel('Y轴', fontsize=12)
    ax1.set_zlabel('Z轴', fontsize=12)
    ax1.legend(fontsize=10, loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # 点积验证垂直性
    ax2 = fig.add_subplot(122)
    
    # 计算点积
    dot_AE = np.dot(A_vec, E_vec)
    dot_AdBdt = np.dot(A_vec, dBdt_vec)
    dot_EdBdt = np.dot(E_vec, dBdt_vec)
    
    # 创建点积验证表格
    data = [
        ['矢量对', '点积结果', '垂直性结论'],
        ['A · E', f'{dot_AE:.6f}', '垂直' if abs(dot_AE) < 1e-10 else '不垂直'],
        ['A · ∂B/∂t', f'{dot_AdBdt:.6f}', '垂直' if abs(dot_AdBdt) < 1e-10 else '不垂直'],
        ['E · ∂B/∂t', f'{dot_EdBdt:.6f}', '垂直' if abs(dot_EdBdt) < 1e-10 else '不垂直']
    ]
    
    # 绘制表格
    table = ax2.table(cellText=data, colLabels=None, cellLoc='center', loc='center',
                     bbox=[0.1, 0.1, 0.8, 0.8])
    
    # 美化表格
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width([0, 1, 2])
    for i, cell in enumerate(table._cells):
        if i < 3:  # 表头
            table._cells[cell].set_facecolor('#4a90e2')
            table._cells[cell].set_text_props(color='white', fontweight='bold')
        else:  # 数据行
            table._cells[cell].set_facecolor('#f0f0f0')
    
    # 添加核心方程
    equation_text = r'$\frac{\partial\vec{B}}{\partial t} = -\frac{1}{c^2} (\vec{A} \times \vec{E})$'
    ax2.text(0.5, 0.05, equation_text, ha='center', fontsize=18, fontweight='bold',
            bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.5'))
    
    ax2.axis('off')
    ax2.set_title('(2) 三力垂直性验证', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('三力垂直可视化.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_comprehensive_visualization():
    """创建综合可视化"""
    # 综合展示图
    fig = plt.figure(figsize=(18, 12))
    
    # 1. 空间螺旋运动的几何结构
    ax1 = fig.add_subplot(231, projection='3d')
    
    r = 2.0
    omega = 2.0
    p = 3.0
    t = np.linspace(0, 2*np.pi/omega, 100)
    
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = p * t
    
    ax1.plot(x, y, z, 'b-', linewidth=3, alpha=0.8, label='螺旋轨迹')
    ax1.scatter(0, 0, 0, s=150, c='red', marker='o', label='螺旋轴中心')
    ax1.plot([0, 0], [0, 0], [z.min(), z.max()], 'k--', linewidth=2, alpha=0.6, label='螺旋轴')
    ax1.plot([0, x[0]], [0, y[0]], [z[0], z[0]], 'g-', linewidth=2, alpha=0.6, label='径向方向')
    
    ax1.set_title('(1) 空间螺旋运动几何结构', fontsize=12, fontweight='bold')
    ax1.set_xlabel('X轴', fontsize=10)
    ax1.set_ylabel('Y轴', fontsize=10)
    ax1.set_zlabel('Z轴', fontsize=10)
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # 2. 场的正交分解
    ax2 = fig.add_subplot(232)
    
    ax2.arrow(0, 0, 3, 0, head_width=0.2, head_length=0.3, fc='#1f77b4', ec='#1f77b4', linewidth=2, label='引力场 A (径向)')
    ax2.arrow(0, 0, 0, 3, head_width=0.2, head_length=0.3, fc='#d62728', ec='#d62728', linewidth=2, label='电场 E (轴向)')
    ax2.arrow(0, 0, -2, 2, head_width=0.2, head_length=0.3, fc='#2ca02c', ec='#2ca02c', linewidth=2, label='变化磁场 ∂B/∂t (角向)')
    
    ax2.scatter(0, 0, s=200, c='gold', marker='o', edgecolor='k', linewidth=2, label='正电荷')
    
    ax2.text(3.2, 0, 'X', fontsize=12, fontweight='bold')
    ax2.text(0, 3.2, 'Y', fontsize=12, fontweight='bold')
    ax2.text(-2.5, 2.5, 'Z', fontsize=12, fontweight='bold')
    
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-4, 4)
    ax2.set_aspect('equal')
    ax2.set_title('(2) 场的正交分解', fontsize=12, fontweight='bold')
    ax2.set_xlabel('X轴', fontsize=10)
    ax2.set_ylabel('Y轴', fontsize=10)
    ax2.legend(fontsize=8, loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    # 3. 核心方程展示
    ax3 = fig.add_subplot(233)
    
    equations = [
        r'$\vec{R}(t) = r\cos(\omega t)\hat{i} + r\sin(\omega t)\hat{j} + pt\hat{k}$',
        r'$|\vec{V}|^2 = (r\omega)^2 + p^2 = c^2$',
        r'$\vec{A} = -\frac{d\vec{V}}{dt}$',
        r'$\vec{B} = \frac{1}{c^2}(\vec{V} \times \vec{E})$',
        r'$\frac{\partial\vec{B}}{\partial t} = -\frac{1}{c^2}(\vec{A} \times \vec{E})$'
    ]
    
    for i, eq in enumerate(equations):
        ax3.text(0.05, 0.9 - i*0.15, eq, fontsize=14, fontweight='bold',
                ha='left', va='top', bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
    
    ax3.axis('off')
    ax3.set_title('(3) 核心方程体系', fontsize=12, fontweight='bold')
    
    # 4. 加速正电荷场景示意图
    ax4 = fig.add_subplot(234)
    
    ax4.arrow(-3, 0, 6, 0, head_width=0.3, head_length=0.5, fc='gray', ec='gray', linewidth=1, alpha=0.5)
    ax4.text(3.5, 0.2, '电荷加速方向', fontsize=10, ha='center')
    
    ax4.scatter(0, 0, s=250, c='gold', marker='o', edgecolor='k', linewidth=2, label='正电荷 +q')
    
    # 绘制电场线
    for angle in np.linspace(0, 2*np.pi, 8):
        x = np.linspace(0.5, 3, 20)
        y = np.tan(angle) * x
        ax4.plot(x, y, 'r-', alpha=0.6, linewidth=1.5)
        ax4.plot(-x, -y, 'r-', alpha=0.6, linewidth=1.5)
    
    # 绘制引力场线
    ax4.arrow(0, 0, -2, 0, head_width=0.2, head_length=0.3, fc='b', ec='b', linewidth=2, label='引力场 A')
    
    # 绘制磁场线
    circle1 = plt.Circle((0, 0), 2, color='g', fill=False, linestyle='--', linewidth=1.5, alpha=0.7)
    circle2 = plt.Circle((0, 0), 1, color='g', fill=False, linestyle='--', linewidth=1.5, alpha=0.7)
    ax4.add_patch(circle1)
    ax4.add_patch(circle2)
    ax4.text(2.2, 0, '磁场 B', fontsize=10, color='g')
    
    ax4.set_xlim(-4, 4)
    ax4.set_ylim(-4, 4)
    ax4.set_aspect('equal')
    ax4.set_title('(4) 加速正电荷场景', fontsize=12, fontweight='bold')
    ax4.set_xlabel('X轴', fontsize=10)
    ax4.set_ylabel('Y轴', fontsize=10)
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3)
    
    # 5. 三维空间正交性示意图
    ax5 = fig.add_subplot(235, projection='3d')
    
    ax5.quiver(0, 0, 0, 2, 0, 0, color='#1f77b4', arrow_length_ratio=0.1, linewidth=2, label='X轴 (A方向)')
    ax5.quiver(0, 0, 0, 0, 2, 0, color='#d62728', arrow_length_ratio=0.1, linewidth=2, label='Y轴 (E方向)')
    ax5.quiver(0, 0, 0, 0, 0, 2, color='#2ca02c', arrow_length_ratio=0.1, linewidth=2, label='Z轴 (dB/dt方向)')
    
    # 绘制空间网格
    x_grid, y_grid = np.meshgrid(np.linspace(-2, 2, 5), np.linspace(-2, 2, 5))
    z_grid = np.zeros_like(x_grid)
    ax5.plot_wireframe(x_grid, y_grid, z_grid, color='gray', alpha=0.3)
    ax5.plot_wireframe(x_grid, z_grid, y_grid, color='gray', alpha=0.3)
    ax5.plot_wireframe(z_grid, x_grid, y_grid, color='gray', alpha=0.3)
    
    ax5.set_xlim(-2, 2)
    ax5.set_ylim(-2, 2)
    ax5.set_zlim(-2, 2)
    ax5.set_title('(5) 三维空间正交性', fontsize=12, fontweight='bold')
    ax5.set_xlabel('X轴', fontsize=10)
    ax5.set_ylabel('Y轴', fontsize=10)
    ax5.set_zlabel('Z轴', fontsize=10)
    ax5.legend(fontsize=8)
    ax5.grid(True, alpha=0.3)
    
    # 6. 结论总结
    ax6 = fig.add_subplot(236)
    
    conclusions = [
        "1. 空间以螺旋运动形式存在",
        "2. 引力场由空间加速度决定",
        "3. 磁场由速度与电场叉乘产生",
        "4. 变化磁场与引力场、电场垂直",
        "5. 三力垂直源于空间三维正交性"
    ]
    
    for i, conclusion in enumerate(conclusions):
        ax6.text(0.1, 0.9 - i*0.15, conclusion, fontsize=11, fontweight='bold',
                ha='left', va='top', bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.3'))
    
    ax6.axis('off')
    ax6.set_title('(6) 主要结论', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('综合可视化.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_animation():
    """创建动态动画"""
    # 参数设置
    r = 2.0
    omega = 2.0
    p = 3.0
    t_max = 4*np.pi/omega
    frames = 200
    t_range = np.linspace(0, t_max, frames)
    
    # 计算轨迹数据
    x = r * np.cos(omega * t_range)
    y = r * np.sin(omega * t_range)
    z = p * t_range
    
    # 计算速度和加速度
    vx = -r * omega * np.sin(omega * t_range)
    vy = r * omega * np.cos(omega * t_range)
    vz = np.full_like(t_range, p)
    
    ax = -r * omega**2 * np.cos(omega * t_range)
    ay = -r * omega**2 * np.sin(omega * t_range)
    az = np.zeros_like(t_range)
    
    # 创建动画
    fig = plt.figure(figsize=(12, 10))
    ax_anim = fig.add_subplot(111, projection='3d')
    
    # 设置坐标轴范围
    max_range = np.max([r*1.5, p*t_max/2])
    ax_anim.set_xlim(-max_range, max_range)
    ax_anim.set_ylim(-max_range, max_range)
    ax_anim.set_zlim(0, p*t_max)
    
    # 初始化绘图对象
    trajectory, = ax_anim.plot([], [], [], 'b-', linewidth=2, alpha=0.7, label='螺旋轨迹')
    current_point, = ax_anim.plot([], [], [], 'ro', markersize=12, alpha=0.9, label='当前位置')
    
    # 速度矢量
    quiver_v = ax_anim.quiver([], [], [], [], [], [], 
                              color='g', arrow_length_ratio=0.1, linewidth=2, 
                              label='速度矢量')
    
    # 加速度矢量
    quiver_a = ax_anim.quiver([], [], [], [], [], [], 
                              color='r', arrow_length_ratio=0.1, linewidth=2, 
                              label='加速度矢量')
    
    # 添加标题和标签
    ax_anim.set_title('空间螺旋运动动态演示', fontsize=14, fontweight='bold')
    ax_anim.set_xlabel('X轴', fontsize=12)
    ax_anim.set_ylabel('Y轴', fontsize=12)
    ax_anim.set_zlabel('Z轴', fontsize=12)
    ax_anim.legend(fontsize=10, loc='upper left')
    ax_anim.grid(True, alpha=0.3)
    
    # 添加时间文本
    time_text = ax_anim.text2D(0.05, 0.95, '', transform=ax_anim.transAxes, 
                              fontsize=12, fontweight='bold', 
                              bbox=dict(facecolor='white', alpha=0.8))
    
    def init():
        """初始化动画"""
        trajectory.set_data([], [])
        trajectory.set_3d_properties([])
        current_point.set_data([], [])
        current_point.set_3d_properties([])
        quiver_v.set_segments([])
        quiver_a.set_segments([])
        time_text.set_text('')
        return trajectory, current_point, quiver_v, quiver_a, time_text
    
    def update(frame):
        """更新动画帧"""
        # 更新轨迹
        trajectory.set_data(x[:frame+1], y[:frame+1])
        trajectory.set_3d_properties(z[:frame+1])
        
        # 更新当前点
        current_point.set_data([x[frame]], [y[frame]])
        current_point.set_3d_properties([z[frame]])
        
        # 更新速度矢量
        scale_v = 0.2
        vx_scaled = vx[frame] * scale_v
        vy_scaled = vy[frame] * scale_v
        vz_scaled = vz[frame] * scale_v
        quiver_v.set_segments([[[x[frame], y[frame], z[frame]], 
                              [x[frame]+vx_scaled, y[frame]+vy_scaled, z[frame]+vz_scaled]]])
        
        # 更新加速度矢量
        scale_a = 0.3
        ax_scaled = ax[frame] * scale_a
        ay_scaled = ay[frame] * scale_a
        az_scaled = az[frame] * scale_a
        quiver_a.set_segments([[[x[frame], y[frame], z[frame]], 
                              [x[frame]+ax_scaled, y[frame]+ay_scaled, z[frame]+az_scaled]]])
        
        # 更新时间文本
        time_text.set_text(f'时间 t = {t_range[frame]:.2f}s')
        
        return trajectory, current_point, quiver_v, quiver_a, time_text
    
    # 创建动画
    ani = FuncAnimation(fig, update, frames=frames, init_func=init, 
                       interval=50, blit=False, repeat=True)
    
    # 保存动画
    ani.save('空间螺旋运动动态演示.gif', writer=PillowWriter(fps=30), dpi=150)
    plt.close()
    
    print("动画创建完成！")

if __name__ == "__main__":
    main()
