import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# 常量定义
G = 6.67430e-11  # 引力常数 (m^3 kg^-1 s^-2)
c = 299792458     # 光速 (m/s)
Z = (G * c) / 2   # 张祥前常数

print(f"引力光速统一方程: Z = (G·c)/2")
print(f"G = {G} m^3 kg^-1 s^-2")
print(f"c = {c} m/s")
print(f"Z = {Z} kg^-1·m^4·s^-3")

# 1. 时空同一化原理可视化
def plot_spacetime_identity():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 时间范围
    t = np.linspace(0, 10, 100)
    
    # 空间位移 R = Ct
    R = c * t / 1e8  # 缩放因子便于可视化
    
    ax.plot(t, R, 'b-', linewidth=2, label=r'$R = Ct$ (缩放: $10^8$)')
    ax.scatter(t[::10], R[::10], c='r', s=50)
    
    ax.set_xlabel('时间 t (s)')
    ax.set_ylabel('空间位移 R (m × $10^{-8}$)')
    ax.set_title('时空同一化原理: 时间与空间的统一')
    ax.legend()
    ax.grid(True)
    
    # 添加方程标签
    ax.text(0.5, 0.9, r'$\vec{r}(t) = \vec{C}t$', transform=ax.transAxes, fontsize=14, 
            bbox=dict(facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('spacetime_identity.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. 空间圆柱状螺旋运动可视化
def plot_spatial_spiral():
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 螺旋参数
    r = 1.0       # 螺旋半径
    omega = 2.0   # 角频率
    h = 0.5       # 螺距参数
    t = np.linspace(0, 10, 500)
    
    # 圆柱螺旋方程
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # 绘制螺旋线
    ax.plot(x, y, z, 'b-', linewidth=2, label='空间螺旋运动轨迹')
    
    # 绘制旋转分量 (xy平面投影)
    ax.plot(x, y, np.zeros_like(z), 'r--', alpha=0.6, label='旋转分量 (电磁场)')
    
    # 绘制轴向分量 (z轴)
    ax.plot([0, 0], [0, 0], [0, max(z)], 'g-', linewidth=3, label='轴向分量 (引力场)')
    
    # 添加箭头指示运动方向
    for i in range(0, len(t), 50):
        ax.quiver(x[i], y[i], z[i], 
                 -omega * r * np.sin(omega * t[i]), 
                  omega * r * np.cos(omega * t[i]), 
                  h, 
                  length=0.3, color='k', normalize=True)
    
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.set_zlabel('Z 轴')
    ax.set_title('空间圆柱状螺旋运动: 引力与电磁力的统一')
    ax.legend()
    
    # 添加光速约束公式
    ax.text2D(0.05, 0.95, r'$c^2 = (r\omega)^2 + h^2$', transform=ax.transAxes, 
             fontsize=14, bbox=dict(facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('spatial_spiral.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. 引力光速统一方程可视化
def plot_gravitational_light_speed_unification():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 创建一个概念图，展示G和c如何通过Z关联
    
    # 绘制三个节点
    ax.plot([G], [0], 'ro', markersize=20, label=f'G = {G:.2e}')
    ax.plot([0], [c/1e8], 'bo', markersize=20, label=f'c = {c:.2e}')
    ax.plot([G/2], [c/(2*1e8)], 'go', markersize=25, label=f'Z = {Z:.2e}')
    
    # 绘制连接线
    ax.plot([G, G/2], [0, c/(2*1e8)], 'r--', linewidth=2)
    ax.plot([0, G/2], [c/1e8, c/(2*1e8)], 'b--', linewidth=2)
    
    # 添加方程
    ax.text(G/2, c/(2*1e8) + 0.5, r'$Z = \frac{G \cdot c}{2}$', 
            fontsize=16, ha='center', bbox=dict(facecolor='yellow', alpha=0.5))
    
    # 坐标轴设置
    ax.set_xlim(-0.5e-10, 1.5e-10)
    ax.set_ylim(-1, 4)
    ax.set_xlabel('引力常数 G (m^3 kg^-1 s^-2)')
    ax.set_ylabel('光速 c (m/s × $10^{-8}$)')
    ax.set_title('引力光速统一方程')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('unification_equation.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. 引力场强度分布可视化
def plot_gravitational_field():
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 创建网格
    x = np.linspace(-5, 5, 40)
    y = np.linspace(-5, 5, 40)
    X, Y = np.meshgrid(x, y)
    
    # 质量位于原点
    m = 1.0  # 质量
    
    # 计算距离和引力场强度
    r = np.sqrt(X**2 + Y**2)
    r[r < 0.1] = 0.1  # 避免奇点
    
    # 引力场强度 g = -Gm/r^2 (径向)
    g_magnitude = G * m / r**2
    
    # 引力场分量
    gx = -g_magnitude * (X / r)
    gy = -g_magnitude * (Y / r)
    
    # 绘制矢量场
    ax.streamplot(X, Y, gx, gy, density=1.0, color='blue', linewidth=1, 
                 arrowstyle='->', arrowsize=1.5)
    
    # 绘制场强等值线
    contour_levels = np.logspace(-12, -10, 10)
    contour = ax.contour(X, Y, g_magnitude, levels=contour_levels, cmap='viridis')
    ax.clabel(contour, inline=True, fontsize=8, fmt='%.1e')
    
    # 绘制中心点质量
    ax.scatter(0, 0, c='red', s=200, marker='o', label='质量 m')
    
    ax.set_xlabel('X 轴 (m)')
    ax.set_ylabel('Y 轴 (m)')
    ax.set_title('引力场强度分布: 空间拖拽效应可视化')
    ax.legend()
    ax.set_aspect('equal')
    
    # 添加引力场公式
    ax.text(0.05, 0.95, r'$\mathbf{g} = -\frac{Gm}{r^3} \mathbf{R}$', 
           transform=ax.transAxes, fontsize=14, bbox=dict(facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('gravitational_field.png', dpi=300, bbox_inches='tight')
    plt.close()

# 5. 质量几何化概念可视化
def plot_mass_geometrization():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 左侧：质量与空间位移线密度关系
    dndOmega = np.linspace(0, 100, 50)  # 单位立体角内的空间位移条数密度
    k = 0.1  # 比例常数
    m = k * dndOmega  # 质量 = k * dn/dOmega
    
    ax1.plot(dndOmega, m, 'b-', linewidth=2)
    ax1.fill_between(dndOmega, m, alpha=0.3, color='blue')
    ax1.set_xlabel('单位立体角内空间位移条数密度 dn/dΩ')
    ax1.set_ylabel('质量 m (kg)')
    ax1.set_title('质量的几何化定义')
    ax1.grid(True)
    ax1.text(0.5, 0.9, r'$m = k \cdot \frac{dn}{d\Omega}$', transform=ax1.transAxes, 
             fontsize=14, bbox=dict(facecolor='yellow', alpha=0.5))
    
    # 右侧：空间位移线发散示意图
    # 绘制中心物体
    ax2.scatter(0, 0, c='red', s=200, marker='o', label='物体')
    
    # 绘制发散的空间位移线
    theta = np.linspace(0, 2*np.pi, 20)
    for angle in theta:
        x = np.linspace(0, 4, 20)
        y = x * np.tan(angle)
        ax2.plot(x, y, 'b-', alpha=0.7)
    
    ax2.set_xlim(-4.5, 4.5)
    ax2.set_ylim(-4.5, 4.5)
    ax2.set_xlabel('X 轴')
    ax2.set_ylabel('Y 轴')
    ax2.set_title('空间位移线的发散特性')
    ax2.legend()
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('mass_geometrization.png', dpi=300, bbox_inches='tight')
    plt.close()

# 6. 螺旋运动速度场旋度可视化
def plot_curl_visualization():
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 创建极坐标网格
    r = np.linspace(0.1, 4, 20)
    theta = np.linspace(0, 2*np.pi, 30)
    R, Theta = np.meshgrid(r, theta)
    
    # 转换为笛卡尔坐标
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)
    
    # 速度场分量 (螺旋运动的旋转分量)
    omega = 1.0
    vx = -omega * R * np.sin(Theta)
    vy = omega * R * np.cos(Theta)
    
    # 绘制速度矢量场
    ax.quiver(X, Y, vx, vy, color='blue', alpha=0.7, width=0.003)
    
    # 绘制旋度方向 (垂直向外)
    for i in range(0, len(r), 4):
        for j in range(0, len(theta), 6):
            x = R[j, i] * np.cos(Theta[j, i])
            y = R[j, i] * np.sin(Theta[j, i])
            ax.quiver(x, y, 0, 0.5, color='red', alpha=0.8, width=0.005, scale=5)
    
    # 绘制中心点
    ax.scatter(0, 0, c='black', s=100, marker='o')
    
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-4.5, 4.5)
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.set_title('空间旋转运动的旋度: 磁场起源')
    ax.set_aspect('equal')
    
    # 添加旋度公式
    ax.text(0.05, 0.95, r'$\nabla \times \vec{v} = 2\omega \cdot \vec{e}_z$', 
           transform=ax.transAxes, fontsize=14, bbox=dict(facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('curl_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()

# 7. 引力光速统一方程与物理常数关系图
def plot_constant_relationships():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 不同光速值下的Z值变化 (概念性)
    c_vals = np.linspace(1e8, 3e8, 50)
    Z_vals = (G * c_vals) / 2
    
    ax.plot(c_vals, Z_vals, 'g-', linewidth=2)
    ax.scatter(c, Z, c='red', s=100, label=f'实际值: c = {c:.2e}')
    
    ax.set_xlabel('光速 c (m/s)')
    ax.set_ylabel('张祥前常数 Z (kg^-1·m^4·s^-3)')
    ax.set_title('引力光速统一方程: Z与c的关系')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('constant_relationships.png', dpi=300, bbox_inches='tight')
    plt.close()

# 执行所有可视化
if __name__ == "__main__":
    print("正在生成可视化图表...")
    
    # 确保中文显示正常
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 生成所有图表
    plot_spacetime_identity()
    print("✓ 时空同一化原理图表生成完成")
    
    plot_spatial_spiral()
    print("✓ 空间螺旋运动图表生成完成")
    
    plot_gravitational_light_speed_unification()
    print("✓ 引力光速统一方程图表生成完成")
    
    plot_gravitational_field()
    print("✓ 引力场分布图表生成完成")
    
    plot_mass_geometrization()
    print("✓ 质量几何化图表生成完成")
    
    plot_curl_visualization()
    print("✓ 旋度可视化图表生成完成")
    
    plot_constant_relationships()
    print("✓ 常数关系图表生成完成")
    
    print("\n所有可视化图表已成功生成！")
    print("生成的文件:")
    print("1. spacetime_identity.png - 时空同一化原理")
    print("2. spatial_spiral.png - 空间圆柱状螺旋运动")
    print("3. unification_equation.png - 引力光速统一方程")
    print("4. gravitational_field.png - 引力场强度分布")
    print("5. mass_geometrization.png - 质量几何化概念")
    print("6. curl_visualization.png - 螺旋运动速度场旋度")
    print("7. constant_relationships.png - 常数关系图")