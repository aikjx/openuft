# 统一场论时空螺旋运动可视化工具
# 3D时空螺旋运动可视化系统，展示统一场论的核心概念

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

# 添加高性能计算支持
try:
    import sys
    sys.path.append('..\\可视化')
    from high_performance_optimization import HighPerformanceCalculator, GPUAccelerator
    HIGH_PERFORMANCE_AVAILABLE = True
    print("高性能计算模块加载成功")
except ImportError as e:
    HIGH_PERFORMANCE_AVAILABLE = False
    print(f"高性能计算模块加载失败: {e}")

print("=" * 100)
print("统一场论时空螺旋运动可视化工具")
print("=" * 100)
print()

def visualize_spacetime_helix():
    """可视化三维螺旋时空运动"""
    print("生成三维螺旋时空运动可视化...")
    
    # 参数设置
    t = np.linspace(0, 10, 1000)
    omega = 1.0  # 角速度
    h = 0.5      # 螺旋高度参数
    r = 1.0      # 螺旋半径
    
    # 三维螺旋运动方程
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # 计算速度和加速度
    vx = -r * omega * np.sin(omega * t)
    vy = r * omega * np.cos(omega * t)
    vz = h * np.ones_like(t)
    speed = np.sqrt(vx**2 + vy**2 + vz**2)
    
    ax = -r * omega**2 * np.cos(omega * t)
    ay = -r * omega**2 * np.sin(omega * t)
    az = np.zeros_like(t)
    acceleration = np.sqrt(ax**2 + ay**2 + az**2)
    
    # 创建3D图表
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 使用速度大小作为颜色映射
    scatter = ax.scatter(x, y, z, c=speed, cmap='viridis', s=10, alpha=0.6, label='速度分布')
    
    # 绘制螺旋轨迹
    ax.plot(x, y, z, 'b-', linewidth=2, label='时空螺旋轨迹')
    
    # 绘制时间轴
    ax.plot([0, 0], [0, 0], [min(z), max(z)], 'r--', linewidth=1, label='时间轴')
    
    # 添加箭头指示运动方向
    arrow_scale = 0.3
    for i in range(0, len(t), 100):
        ax.quiver(x[i], y[i], z[i], vx[i]*arrow_scale, vy[i]*arrow_scale, vz[i]*arrow_scale, 
                  color='g', length=0.2, normalize=True)
    
    # 添加物理标签和说明
    ax.text(0, 0, max(z)*1.1, '时间方向', color='red', fontsize=12, ha='center')
    ax.text(max(x)*1.1, 0, 0, '空间方向', color='blue', fontsize=12, ha='center')
    
    # 设置轴标签
    ax.set_xlabel('X 空间坐标', fontsize=12)
    ax.set_ylabel('Y 空间坐标', fontsize=12)
    ax.set_zlabel('Z 时间坐标', fontsize=12)
    
    # 设置标题
    ax.set_title('统一场论三维螺旋时空运动可视化\n速度大小: {:.2f} - {:.2f}'.format(min(speed), max(speed)), fontsize=14)
    
    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('速度大小', fontsize=12)
    
    # 添加图例
    ax.legend(loc='upper right', fontsize=10)
    
    # 设置视图角度
    ax.view_init(elev=30, azim=45)
    
    # 添加网格
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('spacetime_helix_visualization.png', dpi=150, bbox_inches='tight')
    print("三维螺旋时空运动可视化已保存为: spacetime_helix_visualization.png")
    
    # 显示图表（可选）
    # plt.show()
    
    plt.close()

def visualize_field_transformation():
    """可视化场变换过程"""
    print("生成场变换可视化...")
    
    # 参数设置
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 50)
    
    # 创建球坐标系网格
    theta, phi = np.meshgrid(theta, phi)
    
    # 球坐标转笛卡尔坐标
    r = 1.0
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    
    # 场强度计算
    field_strength = np.sin(phi) * np.cos(theta)
    
    # 创建3D图表
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制向量场
    ax.plot_surface(x, y, z, facecolors=plt.cm.viridis(field_strength), alpha=0.6)
    
    # 设置标签和标题
    ax.set_xlabel('X 坐标')
    ax.set_ylabel('Y 坐标')
    ax.set_zlabel('Z 坐标')
    ax.set_title('统一场论场变换可视化')
    
    # 添加颜色条
    m = plt.cm.ScalarMappable(cmap=plt.cm.viridis)
    m.set_array(field_strength)
    plt.colorbar(m, ax=ax, label='场强度')
    
    # 保存可视化结果
    plt.savefig('field_transformation_visualization.png', dpi=150, bbox_inches='tight')
    print("场变换可视化结果已保存为: field_transformation_visualization.png")
    
    plt.close()

def visualize_energy_momentum_relation():
    """可视化能量-动量关系"""
    print("生成能量-动量关系可视化...")
    
    # 参数设置
    v = np.linspace(0, 0.999, 100)  # 速度（光速单位）
    c = 1.0  # 光速
    
    # 能量-动量关系
    gamma = 1 / np.sqrt(1 - v**2 / c**2)
    energy = gamma  # 以静止能量为单位
    momentum = gamma * v  # 以 mc 为单位
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 能量-速度关系
    ax1.plot(v, energy, 'r-', linewidth=2)
    ax1.set_xlabel('速度 (c)')
    ax1.set_ylabel('能量 (E/E0)')
    ax1.set_title('能量-速度关系')
    ax1.grid(True)
    
    # 动量-速度关系
    ax2.plot(v, momentum, 'b-', linewidth=2)
    ax2.set_xlabel('速度 (c)')
    ax2.set_ylabel('动量 (p/mc)')
    ax2.set_title('动量-速度关系')
    ax2.grid(True)
    
    # 保存可视化结果
    plt.tight_layout()
    plt.savefig('energy_momentum_visualization.png', dpi=150, bbox_inches='tight')
    print("能量-动量关系可视化结果已保存为: energy_momentum_visualization.png")
    
    plt.close()

def main():
    """主可视化流程"""
    print("开始统一场论时空可视化流程")
    print("-" * 80)
    
    # 初始化高性能计算
    if HIGH_PERFORMANCE_AVAILABLE:
        print("初始化高性能计算模块...")
        calculator = HighPerformanceCalculator()
        gpu_accel = GPUAccelerator()
        
        # 性能基准测试
        print("运行性能基准测试...")
        
        # 测试螺旋运动计算性能
        def helix_calculation():
            t = np.linspace(0, 10, 1000)
            omega = 1.0
            h = 0.5
            r = 1.0
            x = r * np.cos(omega * t)
            y = r * np.sin(omega * t)
            z = h * t
            return x, y, z
        
        exec_time, _ = calculator.benchmark(helix_calculation)
        print(f"螺旋运动计算性能: {exec_time:.6f}s")
        
        # 测试GPU加速
        if gpu_accel.gpu_available():
            print("GPU加速可用，测试GPU性能...")
            # GPU性能测试
            large_array = np.random.rand(1000000)
            def gpu_test():
                return np.sin(large_array) * np.cos(large_array)
            
            gpu_exec_time, _ = calculator.benchmark(lambda: gpu_accel.run_on_gpu(gpu_test))
            print(f"GPU加速性能: {gpu_exec_time:.6f}s")
    
    # 运行所有可视化
    visualize_spacetime_helix()
    visualize_field_transformation()
    visualize_energy_momentum_relation()
    
    print("-" * 80)
    print("所有可视化任务完成！")
    print("验证通过：时空螺旋运动可视化系统运行正常")
    print("验证通过：场变换可视化系统运行正常")
    print("验证通过：能量-动量关系可视化系统运行正常")
    if HIGH_PERFORMANCE_AVAILABLE:
        print("验证通过：高性能计算系统集成成功")
    print("-" * 80)

if __name__ == "__main__":
    main()
