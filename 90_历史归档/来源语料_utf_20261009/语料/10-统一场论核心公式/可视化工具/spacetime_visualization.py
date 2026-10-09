# 时空螺旋运动3D可视化工具
# 使用Matplotlib和Plotly实现时空螺旋运动的交互式可视化

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

print("=" * 100)
print("时空螺旋运动3D可视化工具")
print("=" * 100)
print()

def generate_spacetime_helix(radius=1.0, omega=2.0, pitch=0.5, duration=10.0, steps=1000):
    """生成时空螺旋运动轨迹"""
    t = np.linspace(0, duration, steps)
    
    # 三维螺旋时空方程
    x = radius * np.cos(omega * t)
    y = radius * np.sin(omega * t)
    z = pitch * t  # 时间维度
    
    return t, x, y, z

def calculate_velocity_acceleration(x, y, z, t):
    """计算速度和加速度分量"""
    dt = t[1] - t[0]
    
    # 速度分量
    vx = np.gradient(x, dt)
    vy = np.gradient(y, dt)
    vz = np.gradient(z, dt)
    
    # 加速度分量
    ax = np.gradient(vx, dt)
    ay = np.gradient(vy, dt)
    az = np.gradient(vz, dt)
    
    # 速度和加速度大小
    velocity_magnitude = np.sqrt(vx**2 + vy**2 + vz**2)
    acceleration_magnitude = np.sqrt(ax**2 + ay**2 + az**2)
    
    return vx, vy, vz, ax, ay, az, velocity_magnitude, acceleration_magnitude

def plot_matplotlib_3d_helix(x, y, z, t, title="时空螺旋运动轨迹"):
    """使用Matplotlib绘制3D螺旋轨迹"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制螺旋轨迹
    ax.plot(x, y, z, 'b-', linewidth=2, label='时空轨迹')
    
    # 添加时间标记
    time_markers = np.linspace(0, len(t)-1, 10, dtype=int)
    ax.scatter(x[time_markers], y[time_markers], z[time_markers], 
               c='r', s=50, label='时间点')
    
    # 添加坐标轴标签
    ax.set_xlabel('X 空间坐标', fontsize=12)
    ax.set_ylabel('Y 空间坐标', fontsize=12)
    ax.set_zlabel('Z 时间维度', fontsize=12)
    
    # 添加标题和图例
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    
    # 设置网格和视角
    ax.grid(True, alpha=0.3)
    ax.view_init(elev=30, azim=45)
    
    # 保存图像
    filename = f"spacetime_helix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Matplotlib 3D可视化已保存至: {filename}")
    
    # 显示图像
    plt.show()
    
    return fig

def plot_plotly_3d_helix(x, y, z, t, vx, vy, vz, ax, ay, az):
    """使用Plotly绘制交互式3D螺旋轨迹"""
    # 创建轨迹数据
    trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='lines',
        name='时空轨迹',
        line=dict(
            color='blue',
            width=3,
            colorscale='Viridis'
        )
    )
    
    # 创建速度矢量
    velocity_trace = go.Cone(
        x=x[::100],
        y=y[::100],
        z=z[::100],
        u=vx[::100],
        v=vy[::100],
        w=vz[::100],
        name='速度矢量',
        colorscale='Reds',
        sizemode='absolute',
        size=10
    )
    
    # 创建加速度矢量
    acceleration_trace = go.Cone(
        x=x[::150],
        y=y[::150],
        z=z[::150],
        u=ax[::150],
        v=ay[::150],
        w=az[::150],
        name='加速度矢量',
        colorscale='Greens',
        sizemode='absolute',
        size=8
    )
    
    # 创建时间点标记
    time_trace = go.Scatter3d(
        x=x[::200],
        y=y[::200],
        z=z[::200],
        mode='markers+text',
        name='时间点',
        marker=dict(
            size=8,
            color='red',
            symbol='circle'
        ),
        text=[f't={t_i:.1f}' for t_i in t[::200]],
        textposition='top center'
    )
    
    # 组合数据
    data = [trace, velocity_trace, acceleration_trace, time_trace]
    
    # 布局设置
    layout = go.Layout(
        title=dict(
            text='交互式时空螺旋运动可视化',
            font=dict(size=20, family='Arial', color='black')
        ),
        scene=dict(
            xaxis=dict(title='X 空间坐标'),
            yaxis=dict(title='Y 空间坐标'),
            zaxis=dict(title='Z 时间维度'),
            aspectmode='cube'
        ),
        width=1200,
        height=800,
        margin=dict(l=0, r=0, b=0, t=50)
    )
    
    # 创建图形
    fig = go.Figure(data=data, layout=layout)
    
    # 保存为HTML
    filename = f"interactive_spacetime_helix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    fig.write_html(filename)
    print(f"Plotly 交互式可视化已保存至: {filename}")
    
    # 显示图形
    fig.show()
    
    return fig

def plot_velocity_acceleration_profiles(t, v_mag, a_mag):
    """绘制速度和加速度随时间的变化"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # 速度曲线
    ax1.plot(t, v_mag, 'b-', linewidth=2)
    ax1.set_ylabel('速度大小', fontsize=12)
    ax1.set_title('速度随时间变化', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 加速度曲线
    ax2.plot(t, a_mag, 'r-', linewidth=2)
    ax2.set_xlabel('时间', fontsize=12)
    ax2.set_ylabel('加速度大小', fontsize=12)
    ax2.set_title('加速度随时间变化', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图像
    filename = f"velocity_acceleration_profiles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"速度加速度曲线已保存至: {filename}")
    
    plt.show()
    
    return fig

def main():
    """主函数"""
    print("生成时空螺旋运动轨迹...")
    
    # 生成轨迹数据
    t, x, y, z = generate_spacetime_helix(
        radius=1.0,
        omega=2.0,
        pitch=0.5,
        duration=10.0,
        steps=1000
    )
    
    print("计算速度和加速度...")
    vx, vy, vz, ax, ay, az, v_mag, a_mag = calculate_velocity_acceleration(x, y, z, t)
    
    print("绘制Matplotlib 3D轨迹...")
    plot_matplotlib_3d_helix(x, y, z, t)
    
    print("绘制Plotly交互式3D轨迹...")
    plot_plotly_3d_helix(x, y, z, t, vx, vy, vz, ax, ay, az)
    
    print("绘制速度加速度曲线...")
    plot_velocity_acceleration_profiles(t, v_mag, a_mag)
    
    print("\n" + "=" * 100)
    print("时空螺旋运动可视化完成！")
    print("=" * 100)

if __name__ == "__main__":
    main()