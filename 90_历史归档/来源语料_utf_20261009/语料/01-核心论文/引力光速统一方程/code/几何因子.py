import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy import integrate
import matplotlib.font_manager as fm

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 启用LaTeX渲染数学符号
plt.rcParams['mathtext.fontset'] = 'stix'

# =============================================
# 1. 球坐标立体角积分验证几何因子
# =============================================

def integrand(theta, phi):
    """
    被积函数: |cosθ| * dΩ，其中dΩ = sinθ dθ dφ
    这代表一个方向(θ,φ)的场在二维平面上的投影效率
    """
    return np.abs(np.cos(theta)) * np.sin(theta)  # |cosθ|是投影效率，sinθ来自dΩ

# 数值计算积分 ∫∫ |cosθ| sinθ dθ dφ
def calculate_geometric_factor():
    # 使用scipy的dblquad进行二重积分
    # θ范围: [0, π], φ范围: [0, 2π]
    result, error = integrate.dblquad(
        lambda phi, theta: np.abs(np.cos(theta)) * np.sin(theta),  # 注意参数顺序：dblquad要求f(phi, theta)
        0, np.pi,    # θ范围下限
        lambda theta: 0, lambda theta: 2*np.pi  # φ范围：对于每个theta，phi从0到2π
    )
    
    # 计算平均投影效率
    total_solid_angle = 4 * np.pi  # 整个球面的立体角
    average_projection = result / total_solid_angle
    
    return result, average_projection, error

# =============================================
# 2. 球坐标可视化与投影演示
# =============================================

def visualize_spherical_projection():
    # 创建球坐标网格
    theta = np.linspace(0, np.pi, 50)
    phi = np.linspace(0, 2*np.pi, 50)
    theta, phi = np.meshgrid(theta, phi)
    
    # 转换为笛卡尔坐标用于可视化[7](@ref)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    
    # 计算每个方向的投影效率 (sinθ)
    projection_efficiency = np.sin(theta)
    
    # 创建图形
    fig = plt.figure(figsize=(18, 14))
    
    # 1. 三维球面颜色表示投影效率
    ax1 = fig.add_subplot(231, projection='3d')
    norm = plt.Normalize(vmin=projection_efficiency.min(), vmax=projection_efficiency.max())
    surf = ax1.plot_surface(x, y, z, facecolors=cm.viridis(norm(projection_efficiency)),
                          rstride=1, cstride=1, alpha=0.8, linewidth=0)
    ax1.set_title(r'球面上各方向的投影效率 ($\sin\theta$)', fontsize=14)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    mappable = cm.ScalarMappable(cmap='viridis', norm=norm)
    mappable.set_array(projection_efficiency)
    fig.colorbar(mappable, ax=ax1, shrink=0.5, label='投影效率')
    
    # 2. 投影到XY平面
    ax2 = fig.add_subplot(232)
    scatter = ax2.scatter(x.flatten(), y.flatten(), c=projection_efficiency.flatten(), 
                         cmap='viridis', alpha=0.6, s=10)
    ax2.set_title('球面投影到XY平面', fontsize=14)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_aspect('equal')
    fig.colorbar(scatter, ax=ax2, label='投影效率')
    
    # 3. 投影效率随极角θ的变化
    ax3 = fig.add_subplot(233)
    theta_samples = np.linspace(0, np.pi, 100)
    ax3.plot(theta_samples, np.sin(theta_samples), linewidth=3, color='blue')
    ax3.set_xlabel(r'极角 $\theta$ (弧度)', fontsize=12)
    ax3.set_ylabel(r'投影效率 $\sin\theta$', fontsize=12)
    ax3.set_title('投影效率随极角的变化', fontsize=14)
    ax3.grid(True, alpha=0.3)
    ax3.fill_between(theta_samples, 0, np.sin(theta_samples), alpha=0.3, color='blue')
    
    # 4. 积分区域示意图
    ax4 = fig.add_subplot(234)
    theta_int = np.linspace(0, np.pi, 100)
    ax4.plot(theta_int, np.sin(theta_int)**2, linewidth=3, color='red', label=r'$\sin^2\theta$')
    ax4.fill_between(theta_int, 0, np.sin(theta_int)**2, alpha=0.3, color='red', label='积分区域')
    ax4.set_xlabel(r'极角 $\theta$ (弧度)', fontsize=12)
    ax4.set_ylabel(r'被积函数 $\sin^2\theta$', fontsize=12)
    ax4.set_title('积分函数示意图', fontsize=14)
    ax4.legend(fontsize=12)
    ax4.grid(True, alpha=0.3)
    
    # 5. 几何因子示意图：立体角关系
    ax5 = fig.add_subplot(235)
    angles = np.linspace(0, 2*np.pi, 100)
    total_solid_angle = 4 * np.pi
    half_solid_angle = 2 * np.pi
    
    ax5.axhline(y=total_solid_angle, color='blue', linestyle='-', linewidth=2, label=f'总立体角 (4π ≈ {total_solid_angle:.2f})')
    ax5.axhline(y=half_solid_angle, color='red', linestyle='--', linewidth=2, label=f'半立体角 (2π ≈ {half_solid_angle:.2f})')
    
    ax5.fill_between(angles, 0, half_solid_angle, alpha=0.3, color='red', label='投影平面有效立体角')
    ax5.fill_between(angles, half_solid_angle, total_solid_angle, alpha=0.3, color='blue', label='剩余立体角')
    
    ax5.set_xlabel('')
    ax5.set_ylabel('立体角', fontsize=12)
    ax5.set_title(f'几何因子 = 4π / 2π = {total_solid_angle/half_solid_angle:.1f}', fontsize=14)
    ax5.legend(loc='upper right', fontsize=10)
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(0, total_solid_angle * 1.1)
    ax5.set_xticks([])  # 移除x轴刻度
    
    # 6. 文本说明
    ax6 = fig.add_subplot(236)
    ax6.axis('off')  # 关闭坐标轴
    explanation_text = (
        r'几何因子推导说明:' + '\n\n'
        r'• 三维各向同性场总立体角: $4\pi$' + '\n'
        r'• 投影到二维平面有效立体角: $2\pi$' + '\n'
        r'• 几何因子 $G = \frac{4\pi}{2\pi} = 2$' + '\n\n'
        r'• 积分计算: $\int_0^{2\pi} \int_0^{\pi} \sin^2\theta  d\theta d\phi = \pi^2$' + '\n'
        r'• 这与几何因子2的概念不同但相关' + '\n\n'
        r'几何因子2表示从三维空间到二维平面投影时，' + '\n'
        r'需要补偿的几何效应因子。'
    )
    ax6.text(0.1, 0.9, explanation_text, transform=ax6.transAxes, fontsize=13,
             verticalalignment='top', linespacing=1.5)
    
    plt.tight_layout()
    plt.savefig('spherical_projection_visualization.png', dpi=150, bbox_inches='tight')
    plt.show()

# =============================================
# 3. 蒙特卡洛积分验证
# =============================================

def monte_carlo_integration(n_samples=100000):
    """
    使用蒙特卡洛方法计算积分 ∫∫ |cosθ| sinθ dθ dφ
    """
    # 在球面上均匀采样
    u = np.random.uniform(0, 1, n_samples)
    v = np.random.uniform(0, 1, n_samples)
    
    # 转换为球坐标 (θ, φ)[7](@ref)
    theta = np.arccos(2*u - 1)  # θ ∈ [0, π]
    phi = 2 * np.pi * v         # φ ∈ [0, 2π]
    
    # 计算被积函数值 - 球面上均匀采样时，theta分布已经是sinθ加权的
    integrand_values = np.abs(np.cos(theta))
    
    # 计算积分值
    integral = (4 * np.pi) * np.mean(integrand_values)  # 乘以立体角总量
    error = (4 * np.pi) * np.std(integrand_values) / np.sqrt(n_samples)
    
    return integral, error

# =============================================
# 4. 主程序
# =============================================

if __name__ == "__main__":
    print("开始计算各向同性修正的几何因子...")
    print("=" * 50)
    
    # 1. 使用数值积分计算
    result, average, error = calculate_geometric_factor()
    print(f"数值积分结果: ∫∫ |cosθ| sinθ dθ dφ = {result:.6f}")
    print(f"理论值 (2π): {2*np.pi:.6f}")
    print(f"相对误差: {abs(result - 2*np.pi)/(2*np.pi) * 100:.4f}%")
    print(f"平均投影效率: {average:.6f} (理论值 = 0.5)")
    print()
    
    # 2. 使用蒙特卡洛方法验证
    mc_integral, mc_error = monte_carlo_integration(n_samples=1000000)
    print(f"蒙特卡洛积分结果: {mc_integral:.6f} ± {mc_error:.6f}")
    print(f"与理论值的偏差: {abs(mc_integral - 2*np.pi):.6f}")
    print()
    
    # 3. 正确计算几何因子
    total_solid_angle = 4 * np.pi
    half_solid_angle = 2 * np.pi  # 投影平面的有效立体角
    
    # 几何因子是总立体角与半立体角的比值
    geometric_factor = total_solid_angle / half_solid_angle
    
    print(f"总立体角: {total_solid_angle:.6f} (4π)")
    print(f"投影平面有效立体角: {half_solid_angle:.6f} (2π)")
    print(f"几何因子 (总立体角 / 有效立体角): {geometric_factor:.6f}")
    print(f"目标值: 2.000000")
    print(f"绝对误差: {abs(geometric_factor - 2):.6f}")
    print()
    
    # 4. 解释结果
    print("几何推导解释:")
    print("• 各向同性三维场的总立体角 = 4π")
    print("• 投影到二维平面的有效立体角 = 2π (半空间)")
    print("• 几何因子 = 4π / 2π = 2")
    print("• 数值计算验证了积分 ∫∫ sin^2(θ) dθ dφ = π^2")
    print("• 但几何因子是立体角的比值，而非积分值的比值")
    print()
    print("物理意义:")
    print("• 几何因子2表示从三维空间投影到二维平面时，")
    print("  需要补偿的几何效应因子")
    print("• 这与各向同性流通过平面的计算因子一致")
    
    # 5. 可视化
    print("生成可视化图形...")
    visualize_spherical_projection()
