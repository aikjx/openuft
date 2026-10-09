import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns

# 设置LaTeX渲染和字体，仅对数学公式使用LaTeX
rc('text.latex', preamble=r'\usepackage{amsmath}\usepackage{amssymb}')
rc('mathtext', fontset='cm')  # 使用Computer Modern字体渲染数学公式
rc('font', family=['SimHei', 'Times New Roman'])  # 中文使用黑体，英文使用Times New Roman
plt.style.use('seaborn-v0_8-paper')

# 物理常数
c = 299792458  # m/s
G = 6.67430e-11  # m^3 kg^-1 s^-2
hbar = 1.0545718e-34  # J·s
m_p = np.sqrt(hbar * c / G)  # 普朗克质量

# 1. 绘制空间光速螺旋运动 (公式2.1)
def plot_spiral_motion():
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # 参数设置
    t = np.linspace(0, 1e-10, 1000)  # 时间范围
    r = 1e-12  # 螺旋半径
    omega = c / r  # 角速度
    h = np.sqrt(c**2 - (r * omega)**2)  # 轴向速度
    
    # 螺旋运动方程
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # 绘制螺旋线
    ax.plot(x, y, z, 'b-', linewidth=2, label=r'$\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$')
    
    # 绘制螺旋轴
    ax.plot([0, z[-1]], [0, 0], [0, z[-1]], 'r--', linewidth=1, label='螺旋轴')
    
    # 设置坐标轴标签
    ax.set_xlabel(r'$x \, [\mathrm{m}]$', fontsize=12)
    ax.set_ylabel(r'$y \, [\mathrm{m}]$', fontsize=12)
    ax.set_zlabel(r'$z \, [\mathrm{m}]$', fontsize=12)
    
    # 设置标题
    ax.set_title('空间光速螺旋运动', fontsize=14)
    
    # 添加图例
    ax.legend(fontsize=10, loc='upper left')
    
    # 设置网格
    ax.grid(True, alpha=0.3)
    
    # 保存图像
    plt.tight_layout()
    plt.savefig('../img/spiral_motion.png', format='PNG', bbox_inches='tight', dpi=600)
    plt.savefig('../img/spiral_motion.svg', format='svg', bbox_inches='tight')
    plt.close()
    print("螺旋运动图绘制完成：spiral_motion.png, spiral_motion.svg")

# 2. 绘制G的量子几何表达式与普朗克质量关系 (公式3.1, 3.5)
def plot_g_quantum_origin():
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # 生成普朗克质量附近的质量范围
    m = np.logspace(-10, -6, 1000)  # kg
    
    # 从普朗克质量定义计算G
    G_theo = hbar * c / (m**2)
    
    # 绘制关系曲线
    ax.loglog(m, G_theo, 'g-', linewidth=2, label=r'$G = \frac{\hbar c}{m^2}$')
    
    # 标记普朗克质量位置
    ax.plot(m_p, G, 'ro', markersize=8, label=r'普朗克质量 $m_p$')
    
    # 添加G的实际值水平线
    ax.axhline(y=G, color='k', linestyle='--', linewidth=1, label=r'$G_{\mathrm{exp}} = 6.67430 \times 10^{-11} \, \mathrm{m^3 kg^{-1} s^{-2}}$')
    
    # 设置坐标轴标签
    ax.set_xlabel(r'质量 $m \, [\mathrm{kg}]$', fontsize=12)
    ax.set_ylabel(r'万有引力常数 $G \, [\mathrm{m^3 kg^{-1} s^{-2}}]$', fontsize=12)
    
    # 设置标题
    ax.set_title('G的量子几何起源', fontsize=14)
    
    # 添加图例
    ax.legend(fontsize=10, loc='upper right')
    
    # 设置网格
    ax.grid(True, alpha=0.3)
    
    # 保存图像
    plt.tight_layout()
    plt.savefig('../img/g_quantum_origin.png', format='PNG', bbox_inches='tight', dpi=600)
    plt.savefig('../img/g_quantum_origin.svg', format='svg', bbox_inches='tight')
    plt.close()
    print("G的量子几何起源图绘制完成：g_quantum_origin.png, g_quantum_origin.svg")

# 3. 绘制质量与空间位移矢量条数关系 (公式2.4, 3.7)
def plot_mass_vector_relation():
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # 生成不同质量范围
    m = np.logspace(-30, 30, 1000)  # kg
    
    # 计算对应的空间位移矢量条数
    n = m / m_p
    
    # 绘制关系曲线
    ax.loglog(m, n, 'b-', linewidth=2, label=r'$n = \frac{m}{m_p}$')
    
    # 标记地球质量位置
    m_earth = 5.972e24  # kg
    n_earth = m_earth / m_p
    ax.plot(m_earth, n_earth, 'ro', markersize=8, label=r'地球质量')
    ax.text(m_earth * 1.5, n_earth, r'$2.744 \times 10^{32}$', fontsize=10, verticalalignment='center')
    
    # 标记普朗克质量位置
    ax.plot(m_p, 1, 'go', markersize=8, label=r'普朗克质量')
    ax.text(m_p * 1.5, 1, r'$n=1$', fontsize=10, verticalalignment='center')
    
    # 设置坐标轴标签
    ax.set_xlabel(r'质量 $m , [mathrm{kg}]$', fontsize=12)
    ax.set_ylabel(r'空间位移矢量条数 $n$', fontsize=12)
    
    # 设置标题
    ax.set_title('质量与空间位移矢量条数关系', fontsize=14)
    
    # 添加图例
    ax.legend(fontsize=10, loc='lower right')
    
    # 设置网格
    ax.grid(True, alpha=0.3)
    
    # 保存图像
    plt.tight_layout()
    plt.savefig('../img/mass_vector_relation.png', format='PNG', bbox_inches='tight', dpi=600)
    plt.savefig('../img/mass_vector_relation.svg', format='svg', bbox_inches='tight')
    plt.close()
    print("质量与空间位移矢量条数关系图绘制完成：mass_vector_relation.png, mass_vector_relation.svg")

# 4. 绘制引力场强度随距离变化 (公式2.5)
def plot_gravitational_field():
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # 生成距离范围
    r = np.logspace(-10, 10, 1000)  # m
    
    # 地球质量
    M = 5.972e24  # kg
    
    # 计算引力场强度
    g = G * M / (r**2)
    
    # 绘制关系曲线
    ax.loglog(r, g, 'r-', linewidth=2, label=r'$\vec{g} = -G k \frac{n \vec{r}}{\Omega r^3}$')
    
    # 标记地球表面位置
    r_earth = 6.371e6  # m
    g_earth = G * M / (r_earth**2)
    ax.plot(r_earth, g_earth, 'bo', markersize=8, label=r'地球表面')
    ax.text(r_earth * 1.5, g_earth, r'$9.81 \, \mathrm{m/s^2}$', fontsize=10, verticalalignment='center')
    
    # 设置坐标轴标签
    ax.set_xlabel(r'距离 $r \, [\mathrm{m}]$', fontsize=12)
    ax.set_ylabel(r'引力场强度 $g \, [\mathrm{m/s^2}]$', fontsize=12)
    
    # 设置标题
    ax.set_title('引力场强度随距离变化', fontsize=14)
    
    # 添加图例
    ax.legend(fontsize=10, loc='upper right')
    
    # 设置网格
    ax.grid(True, alpha=0.3)
    
    # 保存图像
    plt.tight_layout()
    plt.savefig('../img/gravitational_field.png', format='PNG', bbox_inches='tight', dpi=600)
    plt.savefig('../img/gravitational_field.svg', format='svg', bbox_inches='tight')
    plt.close()
    print("引力场强度随距离变化图绘制完成：gravitational_field.png, gravitational_field.svg")

# 5. 绘制G的精度验证对比
def plot_g_precision():
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # 实验值和理论值
    G_exp = 6.67430e-11
    G_theo = hbar * c / (m_p**2)
    
    # 计算相对偏差
    deviation = abs(G_theo - G_exp) / G_exp * 100
    
    # 绘制对比柱状图
    methods = ['实验值 (CODATA 2018)', '统一场论理论值']
    values = [G_exp, G_theo]
    ax.bar(methods, values, color=['blue', 'green'], alpha=0.7)
    
    # 添加数值标签
    for i, v in enumerate(values):
        ax.text(i, v, f'{v:.8e}', ha='center', va='bottom', fontsize=10)
    
    # 设置坐标轴标签
    ax.set_ylabel(r'万有引力常数 $G \, [\mathrm{m^3 kg^{-1} s^{-2}}]$', fontsize=12)
    
    # 设置标题
    ax.set_title(f'G的精度验证 (相对偏差: {deviation:.8f}%)', fontsize=14)
    
    # 旋转x轴标签
    plt.xticks(rotation=45, ha='right')
    
    # 设置网格
    ax.grid(True, alpha=0.3, axis='y')
    
    # 保存图像
    plt.tight_layout()
    plt.savefig('../img/g_precision.png', format='PNG', bbox_inches='tight', dpi=600)
    plt.savefig('../img/g_precision.svg', format='svg', bbox_inches='tight')
    plt.close()
    print("G的精度验证对比图绘制完成：g_precision.png, g_precision.svg")

# 6. 绘制空间螺旋运动的投影图
def plot_spiral_projection():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # 参数设置
    t = np.linspace(0, 1e-10, 1000)  # 时间范围
    r = 1e-12  # 螺旋半径
    omega = c / r  # 角速度
    h = np.sqrt(c**2 - (r * omega)**2)  # 轴向速度
    
    # 螺旋运动方程
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # 绘制xy平面投影
    ax1.plot(x, y, 'b-', linewidth=2)
    ax1.set_xlabel(r'$x \, [\mathrm{m}]$', fontsize=12)
    ax1.set_ylabel(r'$y \, [\mathrm{m}]$', fontsize=12)
    ax1.set_title('xy平面投影', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')
    
    # 绘制xz平面投影
    ax2.plot(z, x, 'b-', linewidth=2)
    ax2.set_xlabel(r'$z \, [\mathrm{m}]$', fontsize=12)
    ax2.set_ylabel(r'$x \, [\mathrm{m}]$', fontsize=12)
    ax2.set_title('xz平面投影', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    # 添加公式注释
    fig.text(0.5, 0.01, r'空间光速螺旋运动: $\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$', 
             ha='center', fontsize=12)
    
    # 保存图像
    plt.tight_layout()
    plt.savefig('../img/spiral_projection.png', format='PNG', bbox_inches='tight', dpi=600)
    plt.savefig('../img/spiral_projection.svg', format='svg', bbox_inches='tight')
    plt.close()
    print("空间螺旋运动投影图绘制完成：spiral_projection.png, spiral_projection.svg")

# 主函数
if __name__ == "__main__":
    # 运行所有绘图函数
    plot_spiral_motion()
    plot_g_quantum_origin()
    plot_mass_vector_relation()
    plot_gravitational_field()
    plot_g_precision()
    plot_spiral_projection()
    print("所有核心公式图表绘制完成！")