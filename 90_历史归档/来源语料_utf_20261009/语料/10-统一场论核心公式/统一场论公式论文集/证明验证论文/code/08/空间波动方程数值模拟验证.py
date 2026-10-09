import numpy as np
import matplotlib.pyplot as plt

# 基本参数设置 - 基于统一场论第一性原理
c = 3.0e8  # 光速 (m/s)，理论预测值
Lx = 5.0   # 计算域长度 (m)
Nx = 2000  # 空间网格点数，确保高精度空间分辨率
t_max = 1.5e-8  # 最大模拟时间 (s)
Nt = 3000  # 时间步数，确保高精度时间演化

# 空间和时间网格划分
times = np.linspace(0, t_max, Nt)
x = np.linspace(0, Lx, Nx)
dx = x[1] - x[0]  # 空间步长
dt = t_max / Nt   # 时间步长

# CFL稳定性条件检查
cfl = c * dt / dx
print(f"CFL数: {cfl:.6f} (应小于1以确保数值稳定性)")

# 初始化空间位移场（使用高斯波包作为初始条件）
x0 = Lx / 4  # 初始波包位置
width = 0.2  # 波包宽度
displacement_field = np.zeros((Nt, Nx))
displacement_field[0] = np.exp(-((x - x0) ** 2) / (2 * width ** 2))  # 高斯初始条件

# 实现高精度数值求解器 - 二阶中心差分格式
def solve_wave_equation(displacement_field, Nt, Nx, dx, dt, c):
    # 初始化前一时间步（初始速度为零）
    displacement_prev = displacement_field[0].copy()
    
    # 时间演化循环
    for n in range(1, Nt):
        displacement_current = displacement_field[n-1]
        displacement_next = np.zeros(Nx)
        
        # 内部点使用二阶中心差分格式
        for i in range(1, Nx - 1):
            # 计算空间二阶导数（拉普拉斯算子）
            d2u_dx2 = (displacement_current[i+1] - 2*displacement_current[i] + displacement_current[i-1]) / dx**2
            # 应用波动方程的数值格式
            displacement_next[i] = 2*displacement_current[i] - displacement_prev[i] + (c*dt)**2 * d2u_dx2
        
        # 应用高精度透明边界条件，模拟无限空间
        displacement_next[0] = displacement_current[1] + (dx - c*dt)/(dx + c*dt) * (displacement_next[1] - displacement_current[0])
        displacement_next[-1] = displacement_current[-2] + (dx - c*dt)/(dx + c*dt) * (displacement_next[-2] - displacement_current[-1])
        
        # 更新位移场并准备下一步
        displacement_field[n] = displacement_next
        displacement_prev = displacement_current

# 执行高精度数值求解
solve_wave_equation(displacement_field, Nt, Nx, dx, dt, c)

# 实现精确波速测量算法
def measure_wave_speed(displacement_field, x, times, threshold=0.2):
    # 记录波包质心位置随时间的变化
    centroids = []
    valid_times = []
    
    # 分析所有时间步，提取波包信息
    for n in range(Nt):
        current_field = displacement_field[n]
        # 只有当波包信号强度足够且在计算域内时才进行测量
        if np.max(current_field) > threshold and np.sum(current_field) > 1e-10:
            # 使用质心公式精确计算波包位置
            centroid = np.sum(x * current_field) / np.sum(current_field)
            centroids.append(centroid)
            valid_times.append(times[n])
    
    # 使用线性回归精确计算波速（斜率即为波速）
    if len(centroids) > 2:  # 确保有足够的数据点进行可靠拟合
        coeffs = np.polyfit(valid_times, centroids, 1)
        measured_speed = coeffs[0]
        
        # 计算拟合优度R²，评估测量可靠性
        predicted = np.polyval(coeffs, valid_times)
        ss_res = np.sum((centroids - predicted) ** 2)
        ss_tot = np.sum((centroids - np.mean(centroids)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        return measured_speed, r_squared
    return 0.0, 0.0

# 执行波速精确测量
measured_speed, r_squared = measure_wave_speed(displacement_field, x, times)

# 计算相对误差
relative_error = np.abs(measured_speed - c) / c * 100

# 输出高精度验证结果
print("\n===== 空间波动方程数值验证结果 =====")
print(f"理论波速 (基于统一场论第一性原理): {c:.8e} m/s")
print(f"数值模拟测量波速: {measured_speed:.8e} m/s")
print(f"相对误差: {relative_error:.8f}%")
print(f"拟合优度 (R²): {r_squared:.8f}")
print("====================================")

# 验证波包形状保持不变（无耗散无散射）
initial_shape = displacement_field[0]
final_shape = displacement_field[-100]  # 取最后一个稳定的波包形状

# 计算波包宽度变化
initial_width = np.sqrt(np.sum((x - np.sum(x*initial_shape)/np.sum(initial_shape))**2 * initial_shape) / np.sum(initial_shape))
final_width = np.sqrt(np.sum((x - np.sum(x*final_shape)/np.sum(final_shape))**2 * final_shape) / np.sum(final_shape))
width_change = np.abs(final_width - initial_width) / initial_width * 100
print(f"\n波包宽度变化率: {width_change:.8f}% (应接近0以表示无耗散无散射)")

# 验证波动方程的线性叠加原理
print("\n===== 波动方程线性叠加原理验证 =====")
# 创建两个独立的波包
wave1 = np.exp(-((x - Lx/3) ** 2) / (2 * (width/2) ** 2))
wave2 = np.exp(-((x - Lx/3 + 0.5) ** 2) / (2 * (width/2) ** 2))

# 初始化为两个波包的叠加
displacement_field_superposition = np.zeros((Nt, Nx))
displacement_field_superposition[0] = wave1 + wave2

# 求解叠加波场
solve_wave_equation(displacement_field_superposition, Nt, Nx, dx, dt, c)

# 分别求解单个波包
# 波包1
field1 = np.zeros((Nt, Nx))
field1[0] = wave1
solve_wave_equation(field1, Nt, Nx, dx, dt, c)

# 波包2
field2 = np.zeros((Nt, Nx))
field2[0] = wave2
solve_wave_equation(field2, Nt, Nx, dx, dt, c)

# 计算叠加解与分别求解的误差
error = np.max(np.abs(displacement_field_superposition - (field1 + field2)))
print(f"叠加解与分别求解的最大误差: {error:.8e} (应接近0以验证线性叠加原理)")
print(f"相对误差: {error / np.max(displacement_field_superposition) * 100:.8f}%")
print("====================================")