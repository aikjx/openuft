import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 120
plt.style.use('seaborn-v0_8-whitegrid')

# 创建输出目录
output_dir = r'd:\a10\aikjx\code\my_lib\utf\01-核心论文\能量强守恒\img'
os.makedirs(output_dir, exist_ok=True)

def plot_energy_conservation_equation():
    """绘制能量强守恒方程：m₀c² = m c² √(1 - v²/c²)"""
    
    # 设置速度范围（c=1）
    v = np.linspace(0, 0.9999, 1000)
    
    # 计算运动质量m = m₀ / sqrt(1 - v²/c²)
    m = 1 / np.sqrt(1 - v**2)
    
    # 计算能量项
    E_rest = np.ones_like(v)  # m₀c² = 1（单位制）
    E_moving = m * np.sqrt(1 - v**2)  # m c² √(1 - v²/c²)
    E_relativistic = m  # 相对论能量 m c²
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    
    plt.plot(v, E_rest, label=r'静止能量 $E_0 = m_0c^2$', 
             color='blue', linewidth=3, linestyle='-')
    plt.plot(v, E_moving, label=r'统一场论能量 $E = mc^2\sqrt{1 - v^2/c^2}$', 
             color='red', linewidth=3, linestyle='--')
    plt.plot(v, E_relativistic, label=r'相对论能量 $E = mc^2$', 
             color='green', linewidth=2, linestyle=':')
    
    plt.xlabel('速度 $v/c$', fontsize=14, fontweight='bold')
    plt.ylabel('能量 $E/E_0$', fontsize=14, fontweight='bold')
    plt.title('能量强守恒方程可视化', fontsize=16, fontweight='bold')
    
    plt.legend(fontsize=12, frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    
    plt.ylim(0, 5)
    plt.xlim(0, 1)
    
    # 添加说明文本
    plt.text(0.5, 3, r'$E_0 = mc^2\sqrt{1 - v^2/c^2}$', fontsize=18, 
             ha='center', va='center', bbox=dict(boxstyle='round,pad=0.5', 
             facecolor='yellow', alpha=0.3))
    
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(f'{output_dir}/energy_conservation_equation.png', dpi=600, bbox_inches='tight')
    plt.savefig(f'{output_dir}/energy_conservation_equation.svg', bbox_inches='tight')
    plt.close()

def plot_momentum_formulas():
    """绘制动量公式：静止动量P₀ = m₀C₀ 和运动动量P = m(C - V)"""
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    
    # 绘制静止动量的几何表示
    ax1 = plt.subplot(121, projection='3d')
    
    # 原点和矢量位置
    origin = np.array([0, 0, 0])
    C0 = np.array([1, 0, 0])  # 光速矢量
    
    # 绘制光速矢量
    ax1.quiver(0, 0, 0, C0[0], C0[1], C0[2], color='blue', linewidth=3, 
              label=r'$\vec{C}_0$（光速）', arrow_length_ratio=0.1)
    
    # 绘制球体表示物体
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = 0.1 * np.cos(u) * np.sin(v)
    y = 0.1 * np.sin(u) * np.sin(v)
    z = 0.1 * np.cos(v)
    ax1.plot_surface(x, y, z, color='lightgray', alpha=0.7)
    
    ax1.set_xlim(-1.2, 1.2)
    ax1.set_ylim(-1.2, 1.2)
    ax1.set_zlim(-1.2, 1.2)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title(r'静止动量 $\vec{P}_0 = m_0\vec{C}_0$', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10, loc='upper right')
    
    # 绘制运动动量的几何表示
    ax2 = plt.subplot(122, projection='3d')
    
    # 矢量位置
    C = np.array([1, 0, 0])   # 空间本底光速
    V = np.array([0.5, 0, 0])  # 物体运动速度
    C_minus_V = C - V         # C - V
    
    # 绘制矢量
    ax2.quiver(0, 0, 0, C[0], C[1], C[2], color='blue', linewidth=3, 
              label=r'$\vec{C}$（空间本底光速）', arrow_length_ratio=0.1)
    ax2.quiver(0, 0, 0, V[0], V[1], V[2], color='green', linewidth=3, 
              label=r'$\vec{V}$（物体速度）', arrow_length_ratio=0.1)
    ax2.quiver(0, 0, 0, C_minus_V[0], C_minus_V[1], C_minus_V[2], color='red', linewidth=3, 
              label=r'$\vec{C} - \vec{V}$', arrow_length_ratio=0.1)
    
    # 绘制球体表示物体
    ax2.plot_surface(x, y, z, color='lightgray', alpha=0.7)
    
    ax2.set_xlim(-1.2, 1.2)
    ax2.set_ylim(-1.2, 1.2)
    ax2.set_zlim(-1.2, 1.2)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title(r'运动动量 $\vec{P} = m(\vec{C} - \vec{V})$', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10, loc='upper right')
    
    plt.suptitle('动量公式几何表示', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(f'{output_dir}/momentum_formulas.png', dpi=600, bbox_inches='tight')
    plt.savefig(f'{output_dir}/momentum_formulas.svg', bbox_inches='tight')
    plt.close()

def plot_mass_velocity_relation():
    """绘制质量-速度关系"""
    
    # 设置速度范围（c=1）
    v = np.linspace(0, 0.9999, 1000)
    
    # 计算运动质量m = m₀ / sqrt(1 - v²/c²)
    m = 1 / np.sqrt(1 - v**2)
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    
    plt.plot(v, m, label=r'运动质量 $m = m_0 / \sqrt{1 - v^2/c^2}$', 
             color='purple', linewidth=3, linestyle='-')
    
    # 绘制光速限制线
    plt.axvline(x=1, color='red', linestyle='--', alpha=0.7, label='光速限制')
    
    plt.xlabel('速度 $v/c$', fontsize=14, fontweight='bold')
    plt.ylabel('质量 $m/m_0$', fontsize=14, fontweight='bold')
    plt.title('质量-速度关系', fontsize=16, fontweight='bold')
    
    plt.legend(fontsize=12, frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    
    plt.ylim(0, 10)
    plt.xlim(0, 1.05)
    
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(f'{output_dir}/mass_velocity_relation.png', dpi=600, bbox_inches='tight')
    plt.savefig(f'{output_dir}/mass_velocity_relation.svg', bbox_inches='tight')
    plt.close()

def plot_force_decomposition():
    """绘制力的分解：宇宙大统一力方程"""
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    
    # 定义力的分量
    forces = ['电场力', '磁场力', '核力', '惯性力/万有引力']
    components = [r'$\vec{C} \frac{dm}{dt}$', r'$-\vec{V} \frac{dm}{dt}$', 
                 r'$m \frac{d\vec{C}}{dt}$', r'$-m \frac{d\vec{V}}{dt}$']
    colors = ['blue', 'red', 'green', 'purple']
    
    # 绘制力的分量示意图
    x = np.arange(len(forces))
    y = [1, -0.5, 0.8, -1]
    
    # 绘制箭头表示力的分量
    for i, (xi, yi, color, component) in enumerate(zip(x, y, colors, components)):
        plt.arrow(xi, 0, 0, yi, head_width=0.1, head_length=0.2, 
                 fc=color, ec=color, linewidth=2)
        plt.text(xi, yi+0.1*(1 if yi > 0 else -1), component, 
                ha='center', va='bottom' if yi > 0 else 'top', 
                fontsize=12, fontweight='bold')
    
    plt.xticks(x, forces, fontsize=12, fontweight='bold', rotation=15)
    plt.ylabel('力的分量', fontsize=14, fontweight='bold')
    plt.title('宇宙大统一力方程分量分解', fontsize=16, fontweight='bold')
    
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.grid(True, axis='y', alpha=0.3)
    
    plt.ylim(-1.5, 1.5)
    plt.xlim(-0.5, len(forces)-0.5)
    
    # 添加大统一力方程
    plt.text(1.5, 1.2, r'$\vec{F} = \frac{d\vec{P}}{dt} = \vec{C} \frac{dm}{dt} - \vec{V} \frac{dm}{dt} + m \frac{d\vec{C}}{dt} - m \frac{d\vec{V}}{dt}$', 
            fontsize=14, ha='center', va='center', bbox=dict(boxstyle='round,pad=0.5', 
            facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(f'{output_dir}/force_decomposition.png', dpi=600, bbox_inches='tight')
    plt.savefig(f'{output_dir}/force_decomposition.svg', bbox_inches='tight')
    plt.close()

def plot_energy_transfer_paradigm():
    """绘制能量传递的新范式：施力者-空间场-受力者"""
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    
    # 绘制传统模式 vs 统一场论模式
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    
    # 传统模式：施力者(A)-受力者(B)
    ax1.scatter(1, 2, s=200, color='blue', label='施力者A')
    ax1.scatter(3, 2, s=200, color='red', label='受力者B')
    
    # 绘制能量传递箭头
    ax1.arrow(1.3, 2, 1.4, 0, head_width=0.2, head_length=0.3, 
             fc='green', ec='green', linewidth=2, label='能量传递')
    
    ax1.text(2, 2.3, '直接能量转移', fontsize=12, ha='center')
    ax1.text(2, 1.7, r'$W = \Delta E_k$', fontsize=14, ha='center')
    
    ax1.set_xlim(0, 4)
    ax1.set_ylim(0, 4)
    ax1.set_title('传统能量传递模式', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10, loc='best')
    ax1.grid(True, alpha=0.3)
    
    # 统一场论模式：施力者(A)-空间场-受力者(B)
    ax2.scatter(1, 2, s=200, color='blue', label='施力者A')
    ax2.scatter(3, 2, s=200, color='red', label='受力者B')
    
    # 绘制空间场（用椭圆表示）
    ellipse = plt.matplotlib.patches.Ellipse((2, 2), 3, 2, fill=True, 
                                           color='yellow', alpha=0.3, label='空间场')
    ax2.add_patch(ellipse)
    
    # 绘制能量传递箭头
    ax2.arrow(1.3, 2, 0.4, 0, head_width=0.2, head_length=0.3, 
             fc='green', ec='green', linewidth=2, label='能量激发场')
    ax2.arrow(2.3, 2, -0.4, 0, head_width=0.2, head_length=0.3, 
             fc='purple', ec='purple', linewidth=2, label='场引导运动')
    
    ax2.text(1.6, 2.3, '激发空间场', fontsize=12, ha='center')
    ax2.text(2.4, 2.3, '场引导运动', fontsize=12, ha='center')
    ax2.text(2, 1.7, r'$E_0 = m_0c^2$ 守恒', fontsize=14, ha='center')
    
    ax2.set_xlim(0, 4)
    ax2.set_ylim(0, 4)
    ax2.set_title('统一场论能量传递模式', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10, loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('能量传递范式对比', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(f'{output_dir}/energy_transfer_paradigm.png', dpi=600, bbox_inches='tight')
    plt.savefig(f'{output_dir}/energy_transfer_paradigm.svg', bbox_inches='tight')
    plt.close()

# 主函数
if __name__ == '__main__':
    print('开始生成能量强守恒可视化图表...')
    
    # 调用所有可视化函数
    plot_energy_conservation_equation()
    print('1. 能量强守恒方程可视化完成')
    
    plot_momentum_formulas()
    print('2. 动量公式几何表示完成')
    
    plot_mass_velocity_relation()
    print('3. 质量-速度关系完成')
    
    plot_force_decomposition()
    print('4. 力的分量分解完成')
    
    plot_energy_transfer_paradigm()
    print('5. 能量传递范式对比完成')
    
    print('所有图表生成完成！')
    print(f'图表已保存到目录：{output_dir}')