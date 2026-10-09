import os
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""
教科书级别：时间的本质方程可视化
方程：t = f(r)

参数说明（教科书级别）：
- t：时间变量
- r：空间坐标（位置矢量）
- f：函数关系，表示时间与空间的关联
"""

class TimeEssenceEquation:
    """时间的本质方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.c = 1.0  # 归一化的光速
        self.k = 1.0  # 比例常数
    
    def time_function(self, r):
        """时间函数：t = k * r / c
        表示时间与空间距离的关系
        """
        return (self.k * r) / self.c
    
    def time_function_advanced(self, r, v):
        """考虑相对运动影响的时间函数：t' = t * sqrt(1 - v²/c²)
        相对论修正后的时间函数
        """
        # 防止除以零和虚数结果
        safe_v_squared = np.minimum(v**2, 0.9999 * self.c**2)
        gamma = 1.0 / np.sqrt(1.0 - safe_v_squared / self.c**2)
        t = (self.k * r) / self.c
        return t / gamma  # 时间膨胀
    
    def spacetime_interval(self, x, y, z, t):
        """计算时空间隔：s² = c²t² - x² - y² - z²
        表示在时空中两个事件之间的不变量
        """
        r_squared = x**2 + y**2 + z**2
        return self.c**2 * t**2 - r_squared
    
    def visualize_time_distance_relation(self):
        """可视化时间与空间距离的基本关系"""
        # 创建空间距离范围
        r = np.linspace(0, 10, 100)
        
        # 计算对应的时间
        t = self.time_function(r)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制时间-距离关系曲线
        ax.plot(r, t, 'b-', linewidth=2.5)
        
        # 添加参考线
        ax.axline((0, 0), (r[-1], t[-1]), color='r', linestyle='--', alpha=0.7, 
                 label=f'比例常数 k/c = {self.k/self.c}')
        
        # 设置标题和标签
        ax.set_title('时间与空间距离的基本关系 (t = kr/c)', fontsize=16)
        ax.set_xlabel('空间距离 r', fontsize=14)
        ax.set_ylabel('时间 t', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 添加方程标签
        ax.text(0.7*np.max(r), 0.2*np.max(t), 
                't = kr/c', fontsize=16, bbox=dict(facecolor='white', alpha=0.8))
        
        return fig
    
    def visualize_time_dilation(self):
        """可视化相对论时间膨胀效应"""
        # 创建速度范围
        v = np.linspace(0, 0.99*self.c, 100)
        
        # 固定空间距离
        r = 5.0  # 任意固定距离
        
        # 计算固有时间（v=0时的时间）
        t0 = self.time_function(r)
        
        # 计算运动参考系中的时间
        t_v = self.time_function_advanced(r, v)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制时间膨胀曲线
        ax.plot(v/self.c, t_v/t0, 'purple', linewidth=2.5)
        
        # 绘制固有时间参考线
        ax.axhline(y=1, color='r', linestyle='--', label='固有时间 t0')
        
        # 设置标题和标签
        ax.set_title('相对论时间膨胀效应', fontsize=16)
        ax.set_xlabel('速度 v/c', fontsize=14)
        ax.set_ylabel('时间比率 t/t0', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 添加方程标签
        ax.text(0.2, 3.0, 
                't\' = t₀ / √(1 - v²/c²)', fontsize=16, bbox=dict(facecolor='white', alpha=0.8))
        
        return fig
    
    def visualize_spacetime_cone(self):
        """可视化光锥（时空的因果结构）"""
        # 创建网格
        r = np.linspace(-5, 5, 50)
        t = np.linspace(-5, 5, 50)
        R, T = np.meshgrid(r, t)
        
        # 计算光锥边界（|r| = c|t|）
        light_front = self.c * np.abs(T)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # 绘制未来光锥区域（|r| ≤ ct，t ≥ 0）
        future_mask = (np.abs(R) <= light_front) & (T >= 0)
        ax.fill_between(r, light_front, -light_front, where=T[:,0] >= 0, 
                       color='lightblue', alpha=0.3, label='未来光锥')
        
        # 绘制过去光锥区域（|r| ≤ ct，t ≤ 0）
        past_mask = (np.abs(R) <= light_front) & (T <= 0)
        ax.fill_between(r, light_front, -light_front, where=T[:,0] <= 0, 
                       color='lightpink', alpha=0.3, label='过去光锥')
        
        # 绘制光锥边界
        ax.plot(r, self.c * np.abs(r), 'k-', linewidth=2)
        ax.plot(r, -self.c * np.abs(r), 'k-', linewidth=2)
        
        # 绘制当前事件（原点）
        ax.plot(0, 0, 'ro', markersize=8, label='当前事件')
        
        # 设置标题和标签
        ax.set_title('时空光锥（因果结构可视化）', fontsize=16)
        ax.set_xlabel('空间坐标 r', fontsize=14)
        ax.set_ylabel('时间坐标 t', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 设置坐标轴范围和比例
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect('equal')
        
        # 添加光锥方程标签
        ax.text(3, 4, '|r| = ct', fontsize=14)
        
        return fig
    
    def visualize_spacetime_interval_3d(self):
        """3D可视化时空间隔"""
        # 创建网格
        x = np.linspace(-3, 3, 30)
        y = np.linspace(-3, 3, 30)
        X, Y = np.meshgrid(x, y)
        
        # 固定时间和z坐标
        t = 2.0  # 固定时间
        z = 0.0  # 固定z坐标
        
        # 计算时空间隔
        s_squared = self.spacetime_interval(X, Y, z, t)
        
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制时空间隔表面
        surf = ax.plot_surface(X, Y, s_squared, cmap='coolwarm', 
                             linewidth=0, antialiased=True, alpha=0.8)
        
        # 添加颜色条
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        cbar.set_label('时空间隔平方 s²', fontsize=12)
        
        # 绘制光锥边界（s² = 0）的投影
        r_light = self.c * t
        theta = np.linspace(0, 2*np.pi, 100)
        x_light = r_light * np.cos(theta)
        y_light = r_light * np.sin(theta)
        z_light = np.zeros_like(theta)
        ax.plot(x_light, y_light, z_light, 'k-', linewidth=2, label='光锥边界')
        
        # 设置标题和标签
        ax.set_title(f'时空间隔可视化 (t={t}, z={z})', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=12)
        ax.set_ylabel('Y坐标', fontsize=12)
        ax.set_zlabel('s² = c²t² - x² - y²', fontsize=12)
        
        # 添加方程标签
        ax.text(0, 0, np.max(s_squared), 's² = c²t² - x² - y²', 
               fontsize=14, bbox=dict(facecolor='white', alpha=0.8))
        
        return fig
    
    def visualize_time_flow_illustration(self):
        """时间流动方向的图示说明"""
        # 创建图形和子图网格
        fig = plt.figure(figsize=(15, 8))
        gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1])
        
        # 子图1: 时间箭头方向
        ax1 = fig.add_subplot(gs[0])
        ax1.arrow(0, 0, 1, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue', linewidth=2)
        ax1.text(0.5, 0.2, '时间流动方向', fontsize=14, ha='center')
        ax1.set_xlim(-0.2, 1.2)
        ax1.set_ylim(-0.2, 0.5)
        ax1.axis('off')
        
        # 子图2: 事件序列
        ax2 = fig.add_subplot(gs[1])
        
        # 绘制事件点
        events = [(0, 0), (1, 0), (2, 0), (3, 0)]
        for i, (x, y) in enumerate(events):
            ax2.plot(x, y, 'ro', markersize=8)
            ax2.text(x, y+0.3, f'事件{i+1}', fontsize=12, ha='center')
            
            # 绘制事件之间的箭头
            if i < len(events) - 1:
                ax2.arrow(x+0.2, y, 0.6, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
        
        ax2.set_title('事件的时间序列', fontsize=14)
        ax2.set_xlim(-0.5, 3.5)
        ax2.set_ylim(-0.5, 1.0)
        ax2.axis('off')
        
        # 子图3: 时间与空间的关系示意图
        ax3 = fig.add_subplot(gs[2])
        
        # 绘制时间线
        ax3.axvline(x=0, ymin=0, ymax=1, color='black', linewidth=1)
        
        # 绘制空间点在不同时间的位置
        for t in np.linspace(0, 1, 5):
            # 简单的运动轨迹：x = t
            x = t
            ax3.plot(t, x, 'go', markersize=6)
            ax3.text(t+0.05, x, f't={t:.1f}', fontsize=10)
        
        # 连接这些点显示轨迹
        t_values = np.linspace(0, 1, 100)
        x_values = t_values
        ax3.plot(t_values, x_values, 'g-', linewidth=1.5, alpha=0.7)
        
        ax3.set_title('物体运动的时空轨迹', fontsize=14)
        ax3.set_xlabel('时间 t', fontsize=12)
        ax3.set_ylabel('空间位置 x', fontsize=12)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(-0.1, 1.1)
        ax3.set_ylim(-0.1, 1.1)
        
        fig.suptitle('时间流动与事件序列', fontsize=16)
        
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
        params_text = "时间的本质方程参数详解 (教科书级别):\n" + \
                      "t = f(r)\n" + \
                      "\n参数含义:\n" + \
                      "- t: 时间变量，表示事件发生的顺序和持续时间\n" + \
                      "- r: 空间位置矢量\n" + \
                      "- f: 函数关系，表示时间与空间的内在联系\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程揭示了时间的本质是空间运动的表现\n" + \
                      "- 在统一场论中，时间被视为空间的一个特殊维度\n" + \
                      "- 基本关系：t = kr/c，表示时间与空间距离成正比\n" + \
                      "- 相对论修正：t' = t₀/√(1 - v²/c²)，描述时间膨胀效应\n" + \
                      "- 时空间隔：s² = c²t² - x² - y² - z²，是相对论中的不变量\n" + \
                      "- 光锥结构：|r| = ct，定义了因果关系的边界\n" + \
                      "- 时间具有方向性，是单向流动的（热力学箭头）\n" + \
                      "- 时间与空间不可分割，共同构成四维时空连续体"
        
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
    
    # 创建时间的本质方程可视化对象
    time_eq = TimeEssenceEquation()
    
    # 显示时间与距离关系
    fig_time_distance = time_eq.visualize_time_distance_relation()
    time_eq.add_parameter_explanation(fig_time_distance)
    
    # 显示时间膨胀效应
    fig_time_dilation = time_eq.visualize_time_dilation()
    time_eq.add_parameter_explanation(fig_time_dilation)
    
    # 显示时空光锥
    fig_light_cone = time_eq.visualize_spacetime_cone()
    time_eq.add_parameter_explanation(fig_light_cone)
    
    # 显示时空间隔3D可视化
    fig_spacetime_interval = time_eq.visualize_spacetime_interval_3d()
    time_eq.add_parameter_explanation(fig_spacetime_interval)
    
    # 显示时间流动图示
    fig_time_flow = time_eq.visualize_time_flow_illustration()
    time_eq.add_parameter_explanation(fig_time_flow)
    
    # 添加方程到图形中
    equation_text = "时间的本质方程: t = f(r)"
    fig_time_distance.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                          bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_time_distance.savefig('./img/时间与空间距离关系.png', dpi=300, bbox_inches='tight')
    fig_time_dilation.savefig('./img/相对论时间膨胀效应.png', dpi=300, bbox_inches='tight')
    fig_light_cone.savefig('./img/时空光锥因果结构.png', dpi=300, bbox_inches='tight')
    fig_spacetime_interval.savefig('./img/时空间隔3D可视化.png', dpi=300, bbox_inches='tight')
    fig_time_flow.savefig('./img/时间流动图示.png', dpi=300, bbox_inches='tight')
    
    print("时间的本质方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")