import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 三维圆柱状螺旋运动可视化
def visualize_spiral_motion():
    # 参数设置
    r = 1.0       # 旋转半径
    omega = 2.0   # 角速度
    p = 1.0       # 直线运动速度
    t = np.linspace(0, 10, 1000)  # 时间范围
    
    # 计算三维坐标
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = p * t
    
    # 创建3D图形
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制螺旋轨迹
    ax.plot(x, y, z, label='螺旋轨迹', linewidth=2, color='blue')
    
    # 绘制旋转平面投影
    ax.plot(x, y, np.zeros_like(z), label='旋转分量投影', linewidth=1, color='red', linestyle='--')
    
    # 添加坐标轴标签
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.set_zlabel('Z 轴')
    
    # 添加标题
    ax.set_title('三维圆柱状螺旋运动可视化')
    
    # 添加图例
    ax.legend()
    
    # 设置视角
    ax.view_init(elev=30, azim=45)
    
    # 显示网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

# 不同参数下的螺旋运动对比
def compare_spiral_motions():
    t = np.linspace(0, 10, 1000)
    
    # 案例1：旋转分量为主
    r1, omega1, p1 = 2.0, 1.5, 0.5
    x1 = r1 * np.cos(omega1 * t)
    y1 = r1 * np.sin(omega1 * t)
    z1 = p1 * t
    
    # 案例2：直线分量为主
    r2, omega2, p2 = 0.5, 0.5, 2.0
    x2 = r2 * np.cos(omega2 * t)
    y2 = r2 * np.sin(omega2 * t)
    z2 = p2 * t
    
    # 创建3D图形
    fig = plt.figure(figsize=(15, 7))
    
    # 子图1：旋转分量为主
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(x1, y1, z1, label='旋转为主', linewidth=2, color='green')
    ax1.set_xlabel('X 轴')
    ax1.set_ylabel('Y 轴')
    ax1.set_zlabel('Z 轴')
    ax1.set_title('旋转分量为主的螺旋运动')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.view_init(elev=30, azim=45)
    
    # 子图2：直线分量为主
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot(x2, y2, z2, label='直线为主', linewidth=2, color='purple')
    ax2.set_xlabel('X 轴')
    ax2.set_ylabel('Y 轴')
    ax2.set_zlabel('Z 轴')
    ax2.set_title('直线分量为主的螺旋运动')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    print("正在生成三维螺旋运动可视化...")
    visualize_spiral_motion()
    print("正在生成不同参数下的螺旋运动对比...")
    compare_spiral_motions()
    print("可视化完成！")