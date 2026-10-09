import os
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题
import numpy as np
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""
教科书级别：时空波动方程可视化
方程：∂²L/∂t² = c²∇²L

参数说明（教科书级别）：
- L：时空波动量
- t：时间
- c：光速
- ∇²：拉普拉斯算子（∂²/∂x² + ∂²/∂y² + ∂²/∂z²）
"""

class SpacetimeWaveEquation:
    """时空波动方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.c = 1.0  # 归一化的光速
        self.wavelength = 1.0  # 波长
        self.frequency = self.c / self.wavelength  # 频率
        self.omega = 2 * np.pi * self.frequency  # 角频率
        self.k = 2 * np.pi / self.wavelength  # 波数
    
    def plane_wave_solution(self, x, y, z, t):
        """平面波解
        L(x, y, z, t) = A * cos(k·r - ωt + φ)
        这里选择沿x轴传播的平面波
        """
        A = 1.0  # 振幅
        phi = 0  # 相位
        
        # 沿x轴传播的平面波
        wave = A * np.cos(self.k * x - self.omega * t + phi)
        
        return wave
    
    def spherical_wave_solution(self, x, y, z, t):
        """球面波解
        L(x, y, z, t) = (A/r) * cos(kr - ωt + φ)
        """
        A = 1.0  # 振幅
        phi = 0  # 相位
        
        # 计算到原点的距离
        r = np.sqrt(x**2 + y**2 + z**2)
        
        # 避免除零错误
        r_safe = np.maximum(r, 1e-6)
        
        # 球面波解
        wave = (A / r_safe) * np.cos(self.k * r_safe - self.omega * t + phi)
        
        return wave
    
    def visualize_plane_wave_2d(self):
        """2D可视化平面波的传播"""
        # 创建空间网格
        x = np.linspace(-4*self.wavelength, 4*self.wavelength, 100)
        t = np.linspace(0, 2*np.pi/self.omega, 50)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 选择几个时间点显示波形
        time_indices = [0, 10, 20, 30, 40]
        colors = ['blue', 'green', 'red', 'purple', 'orange']
        labels = [f't={t[i]:.2f}' for i in time_indices]
        
        # 绘制每个时间点的波形
        for i, idx in enumerate(time_indices):
            wave = self.plane_wave_solution(x, 0, 0, t[idx])
            ax.plot(x, wave, color=colors[i], linewidth=1.5, label=labels[i])
        
        # 设置标题和标签
        ax.set_title('平面波的传播 (∂²L/∂t² = c²∇²L)', fontsize=16)
        ax.set_xlabel('位置 x', fontsize=14)
        ax.set_ylabel('波动量 L', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def visualize_spherical_wave_2d(self):
        """2D可视化球面波的传播"""
        # 创建空间网格
        x = np.linspace(-4*self.wavelength, 4*self.wavelength, 50)
        y = np.linspace(-4*self.wavelength, 4*self.wavelength, 50)
        X, Y = np.meshgrid(x, y)
        
        # 选择一个特定时间
        t = 0
        
        # 计算球面波
        wave = self.spherical_wave_solution(X, Y, 0, t)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 绘制等高线图表示波幅
        contour = ax.contourf(X, Y, wave, 20, cmap='viridis')
        
        # 添加颜色条
        cbar = plt.colorbar(contour, ax=ax)
        cbar.set_label('波动量 L', fontsize=12)
        
        # 设置标题和标签
        ax.set_title('球面波的传播 (t=0)', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.set_aspect('equal')
        
        return fig
    
    def visualize_wave_3d(self, wave_type='plane'):
        """3D可视化波动"""
        # 创建空间网格
        x = np.linspace(-4*self.wavelength, 4*self.wavelength, 50)
        y = np.linspace(-4*self.wavelength, 4*self.wavelength, 50)
        X, Y = np.meshgrid(x, y)
        
        # 选择一个特定时间
        t = 0
        
        # 计算波
        if wave_type == 'plane':
            wave = self.plane_wave_solution(X, Y, 0, t)
        else:  # spherical
            wave = self.spherical_wave_solution(X, Y, 0, t)
        
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制3D波形
        surf = ax.plot_surface(X, Y, wave, cmap=cm.viridis, 
                             linewidth=0, antialiased=True, alpha=0.8)
        
        # 添加颜色条
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        cbar.set_label('波动量 L', fontsize=12)
        
        # 设置标题和标签
        wave_name = '平面波' if wave_type == 'plane' else '球面波'
        ax.set_title(f'{wave_name}的3D可视化 (t=0)', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=12)
        ax.set_ylabel('Y坐标', fontsize=12)
        ax.set_zlabel('波动量 L', fontsize=12)
        
        return fig
    
    def visualize_wave_animation(self, wave_type='plane'):
        """创建波动动画（返回动画对象）"""
        # 创建空间网格
        x = np.linspace(-4*self.wavelength, 4*self.wavelength, 100)
        y = np.linspace(-4*self.wavelength, 4*self.wavelength, 100)
        X, Y = np.meshgrid(x, y)
        
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 初始时间
        t = 0
        
        # 计算初始波形
        if wave_type == 'plane':
            wave = self.plane_wave_solution(X, Y, 0, t)
        else:  # spherical
            wave = self.spherical_wave_solution(X, Y, 0, t)
        
        # 绘制初始表面
        surf = [ax.plot_surface(X, Y, wave, cmap=cm.viridis, 
                              linewidth=0, antialiased=True, alpha=0.8)]
        
        # 设置标题和标签
        wave_name = '平面波' if wave_type == 'plane' else '球面波'
        ax.set_title(f'{wave_name}传播动画', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=12)
        ax.set_ylabel('Y坐标', fontsize=12)
        ax.set_zlabel('波动量 L', fontsize=12)
        
        # 设置坐标轴范围
        ax.set_zlim(-1.5, 1.5)
        
        # 更新函数
        def update(frame):
            # 清除当前表面
            surf[0].remove()
            
            # 计算新时间的波形
            t = frame * 0.1
            if wave_type == 'plane':
                wave = self.plane_wave_solution(X, Y, 0, t)
            else:  # spherical
                wave = self.spherical_wave_solution(X, Y, 0, t)
            
            # 绘制新表面
            surf[0] = ax.plot_surface(X, Y, wave, cmap=cm.viridis, 
                                    linewidth=0, antialiased=True, alpha=0.8)
            
            # 更新标题
            ax.set_title(f'{wave_name}传播动画 (t={t:.2f})', fontsize=16)
            
            return surf
        
        # 创建动画
        ani = animation.FuncAnimation(fig, update, frames=50, interval=100, blit=False)
        
        return ani
    
    def visualize_dispersion_relation(self):
        """可视化色散关系 ω = ck"""
        # 创建波数范围
        k_range = np.linspace(0, 4*self.k, 100)
        
        # 计算角频率（根据色散关系 ω = ck）
        omega_range = self.c * k_range
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制色散关系
        ax.plot(k_range, omega_range, 'b-', linewidth=2.5)
        
        # 添加参考线表示光速
        ax.axline((0, 0), (self.k, self.omega), color='r', linestyle='--', linewidth=1.5, 
                 label=f'光速 c = {self.c}')
        
        # 设置标题和标签
        ax.set_title('色散关系 (ω = ck)', fontsize=16)
        ax.set_xlabel('波数 k', fontsize=14)
        ax.set_ylabel('角频率 ω', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 添加方程标签
        ax.text(0.5*np.max(k_range), 0.3*np.max(omega_range), 
                'ω = ck', fontsize=16, bbox=dict(facecolor='white', alpha=0.8))
        
        return fig
    
    def add_parameter_explanation(self, fig):
    # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
            """添加专业级别的参数解释文本框"""
        params_text = "时空波动方程参数详解 (教科书级别):\n" + \
                      "∂²L/∂t² = c²∇²L\n" + \
                      "\n参数含义:\n" + \
                      "- L: 时空波动量，表示时空中的扰动\n" + \
                      "- t: 时间变量\n" + \
                      "- c: 光速，波的传播速度\n" + \
                      "- ∇²: 拉普拉斯算子，表示空间中的二阶导数\n" + \
                      "      (∇² = ∂²/∂x² + ∂²/∂y² + ∂²/∂z²)\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程描述了时空中扰动的传播规律\n" + \
                      "- 是统一场论中描述时空波动的核心方程\n" + \
                      "- 方程左边表示波动量随时间的二阶变化率\n" + \
                      "- 方程右边表示波动量在空间中的分布变化与光速平方的乘积\n" + \
                      "- 平面波解形式: L = A cos(k·r - ωt)，其中 ω = ck\n" + \
                      "- 球面波解形式: L = (A/r) cos(kr - ωt)\n" + \
                      "- 该方程在真空中电磁波传播、引力波等现象中具有重要意义"
        
        # 在图形中添加参数说明文本框
        fig.text(0.02, 0.02, params_text, fontsize=10, 
                 verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建并显示可视化
if __name__ == "__main__":
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    # 创建时空波动方程可视化对象
    wave_eq = SpacetimeWaveEquation()
    
    # 显示平面波2D可视化
    fig_plane_2d = wave_eq.visualize_plane_wave_2d()
    wave_eq.add_parameter_explanation(fig_plane_2d)
    
    # 显示球面波2D可视化
    fig_sphere_2d = wave_eq.visualize_spherical_wave_2d()
    wave_eq.add_parameter_explanation(fig_sphere_2d)
    
    # 显示平面波3D可视化
    fig_plane_3d = wave_eq.visualize_wave_3d(wave_type='plane')
    wave_eq.add_parameter_explanation(fig_plane_3d)
    
    # 显示球面波3D可视化
    fig_sphere_3d = wave_eq.visualize_wave_3d(wave_type='spherical')
    wave_eq.add_parameter_explanation(fig_sphere_3d)
    
    # 显示色散关系
    fig_dispersion = wave_eq.visualize_dispersion_relation()
    wave_eq.add_parameter_explanation(fig_dispersion)
    
    # 添加方程到图形中
    equation_text = "时空波动方程: ∂²L/∂t² = c²∇²L"
    fig_plane_2d.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_plane_2d.savefig('./img/平面波2D可视化.png', dpi=300, bbox_inches='tight')
    fig_sphere_2d.savefig('./img/球面波2D可视化.png', dpi=300, bbox_inches='tight')
    fig_plane_3d.savefig('./img/平面波3D可视化.png', dpi=300, bbox_inches='tight')
    fig_sphere_3d.savefig('./img/球面波3D可视化.png', dpi=300, bbox_inches='tight')
    fig_dispersion.savefig('./img/色散关系.png', dpi=300, bbox_inches='tight')
    
    print("时空波动方程可视化已保存为PNG文件")
    print("注：动画功能在非交互式环境中不会自动播放，如需查看动画，请在交互式环境中运行代码")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")