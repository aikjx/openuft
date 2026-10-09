import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""
教科书级别：质量定义方程可视化
方程：m = k · dn/dΩ

参数说明（教科书级别）：
- m：物体的质量
- k：比例常数，与空间基本属性相关的系数
- dn/dΩ：单位立体角内的空间运动量变化率
- Ω：立体角（单位：球面度，sr）
"""

class MassDefinitionEquation:
    """质量定义方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.k = 1.0  # 比例常数，可调整
        self.max_omega = 4 * np.pi  # 最大立体角（整个球面）
        
    def space_motion_density(self, omega):
        """定义空间运动量密度函数
        这里使用高斯分布近似表示实际物理场景中的分布
        """
        # 使用高斯分布模拟空间运动量密度随立体角的变化
        mu = self.max_omega / 2
        sigma = self.max_omega / 6
        return np.exp(-0.5 * ((omega - mu) / sigma) ** 2) * 10
        
    def calculate_mass(self, omega):
        """根据质量定义方程计算质量
        m = k · dn/dΩ
        """
        dn_domega = self.space_motion_density(omega)
        return self.k * dn_domega
    
    def visualize_2d(self):
        """2D可视化：质量随立体角的变化关系"""
        # 生成立体角数据
        omega = np.linspace(0, self.max_omega, 500)
        
        # 计算空间运动量密度和质量
        dn_domega = self.space_motion_density(omega)
        mass = self.calculate_mass(omega)
        
        # 创建图形
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 绘制空间运动量密度
        ax1.plot(omega, dn_domega, 'b-', linewidth=2)
        ax1.set_title('空间运动量密度 dn/dΩ 随立体角 Ω 的变化', fontsize=14)
        ax1.set_xlabel('立体角 Ω (球面度, sr)', fontsize=12)
        ax1.set_ylabel('空间运动量密度 dn/dΩ', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # 绘制质量
        ax2.plot(omega, mass, 'r-', linewidth=2)
        ax2.set_title('质量 m 随立体角 Ω 的变化 (质量定义方程)', fontsize=14)
        ax2.set_xlabel('立体角 Ω (球面度, sr)', fontsize=12)
        ax2.set_ylabel('质量 m', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # 添加方程和参数说明
        equation_text = "质量定义方程: m = k · dn/dΩ"
        plt.figtext(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
        
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        return fig
    
    def visualize_3d(self):
        """3D可视化：立体角与质量的关系"""
        # 创建单位球面上的点（表示立体角）
        theta = np.linspace(0, np.pi, 30)
        phi = np.linspace(0, 2*np.pi, 30)
        theta, phi = np.meshgrid(theta, phi)
        
        # 计算球坐标到直角坐标的转换
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        
        # 计算每个点对应的立体角和质量
        # 立体角近似为球面上点的分布密度
        omega = np.sqrt(x**2 + y**2 + z**2)  # 简化处理
        mass = self.calculate_mass(omega * np.pi)
        
        # 创建3D图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制质量分布在球面上的热图
        scatter = ax.scatter(x, y, z, c=mass, cmap='viridis', s=100, alpha=0.7)
        
        # 设置坐标轴和标题
        ax.set_title('质量在空间立体角上的分布可视化', fontsize=14)
        ax.set_xlabel('X轴', fontsize=12)
        ax.set_ylabel('Y轴', fontsize=12)
        ax.set_zlabel('Z轴', fontsize=12)
        
        # 添加颜色条
        cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
        cbar.set_label('质量 m', fontsize=12)
        
        return fig
    
    def add_parameter_explanation(self, fig):
        """添加专业级别的参数解释文本框"""
        params_text = "质量定义方程参数详解 (教科书级别):\n" + \
                      "1. m: 物体的质量，是物体惯性和引力属性的量度\n" + \
                      "2. k: 比例常数，与空间的基本属性相关，反映空间对物质的作用强度\n" + \
                      "3. dn/dΩ: 单位立体角内的空间运动量变化率，表示\n" + \
                      "   空间运动量在特定方向上的分布密度\n" + \
                      "4. Ω: 立体角，描述空间中方向的量度，单位为球面度(sr)\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程从空间几何角度定义质量，揭示了质量与空间运动量\n" + \
                      "  分布之间的内在联系\n" + \
                      "- 质量并非物体的固有属性，而是空间运动量分布特征的表现\n" + \
                      "- 统一场论的核心思想之一：质量本质上是空间的一种运动效应"
        
        # 在图形中添加参数说明文本框
        fig.text(0.02, 0.02, params_text, fontsize=10, 
                 verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建并显示可视化
if __name__ == "__main__":
    # 创建质量定义方程可视化对象
    mass_eq = MassDefinitionEquation()
    
    # 显示2D可视化
    fig_2d = mass_eq.visualize_2d()
    mass_eq.add_parameter_explanation(fig_2d)
    
    # 显示3D可视化
    fig_3d = mass_eq.visualize_3d()
    mass_eq.add_parameter_explanation(fig_3d)
    
    # 确保img目录存在
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    # 保存图形为PNG文件到img目录
    fig_2d.savefig(f'{img_dir}/质量定义方程_2D可视化.png', dpi=300, bbox_inches='tight')
    fig_3d.savefig(f'{img_dir}/质量定义方程_3D可视化.png', dpi=300, bbox_inches='tight')
    
    print(f"质量定义方程可视化已保存到 {img_dir} 目录")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")