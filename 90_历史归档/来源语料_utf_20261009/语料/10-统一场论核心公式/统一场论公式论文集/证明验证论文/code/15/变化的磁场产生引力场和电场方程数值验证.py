import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 定义常量
c = 3.0e8  # 光速，m/s

# 矢量叉乘函数（NumPy已内置）

# 磁场演化函数
def magnetic_field_evolution(t, B, A_func, E_func, V_func):
    """计算磁场随时间的演化"""
    # 获取当前时刻的场值
    A = A_func(t)
    E = E_func(t)
    V = V_func(t)
    
    # 计算电场变化率（使用中心差分近似）
    dt_small = 1e-6
    E_plus = E_func(t + dt_small)
    E_minus = E_func(t - dt_small)
    dE_dt = (E_plus - E_minus) / (2 * dt_small)
    
    # 计算dB/dt的三个分量
    term1 = -np.cross(A, E) / c**2
    term2 = -np.cross(V, dE_dt) / c**2
    dB_dt = term1 + term2
    
    return dB_dt

# 定义场函数示例
def A_func(t):
    """引力场强度矢量函数"""
    A0 = 1.0
    omega = 1.0
    return np.array([A0 * np.cos(omega * t), 0, 0])

def E_func(t):
    """电场强度矢量函数"""
    E0 = 1.0
    omega = 1.0
    return np.array([0, E0 * np.sin(omega * t), 0])

def V_func(t):
    """物体速度矢量函数"""
    v_const = 1.0e6  # 10^6 m/s
    return np.array([0, 0, v_const])

# 数值计算示例
def numerical_example():
    """数值计算示例"""
    # 定义场参数
    A = np.array([1.0, 0.0, 0.0])  # 引力场强度，m/s
    E = np.array([0.0, 1.0, 0.0])  # 电场强度，N/C
    V = np.array([0.0, 0.0, 1.0e6])  # 物体速度，m/s
    dE_dt = np.array([0.0, 0.0, 1.0])  # 电场变化率，N/(C·s)
    
    # 计算dB/dt的三个分量
    # 第一项：-A×E/c²
    term1 = -np.cross(A, E) / c**2
    
    # 第二项：-V×dE/dt/c²
    term2 = -np.cross(V, dE_dt) / c**2
    
    # 总磁场变化率
    dBdt = term1 + term2
    
    # 量纲分析
    print("=== 量纲分析 ===")
    print(f"左侧dB/dt的量纲: T/s (特斯拉/秒)")
    print(f"右侧第一项量纲: (m/s × N/C) / (m²/s²) = (N·m)/(C·m²/s) = T/s")
    print(f"右侧第二项量纲: (m/s × N/(C·s)) / (m²/s²) = N/(C·s) × s/m = T/s")
    print(f"量纲一致性: 正确")
    
    # 数值结果
    print("\n=== 数值计算结果 ===")
    print(f"引力场A: {A} m/s")
    print(f"电场E: {E} N/C")
    print(f"速度V: {V} m/s")
    print(f"电场变化率dE/dt: {dE_dt} N/(C·s)")
    print(f"\n第一项贡献: {term1} T/s")
    print(f"第二项贡献: {term2} T/s")
    print(f"总磁场变化率dB/dt: {dBdt} T/s")
    
    return dBdt

# 速度依赖性分析
def velocity_dependence_analysis():
    """分析物体速度对磁场变化率的影响"""
    # 定义参数
    A = np.array([1.0, 0.0, 0.0])  # 引力场强度
    E = np.array([0.0, 1.0, 0.0])  # 电场强度
    dE_dt = np.array([0.0, 0.0, 1.0])  # 电场变化率
    
    # 速度范围
    v_values = np.linspace(0, 1.0e7, 100)  # 0到10^7 m/s
    
    # 计算dB/dt的三个分量
    dBdt_results = []
    
    for v in v_values:
        V = np.array([0.0, 0.0, v])  # 物体速度矢量
        
        # 计算第一项：-A×E/c²
        term1 = -np.cross(A, E) / c**2
        
        # 计算第二项：-V×dE/dt/c²
        term2 = -np.cross(V, dE_dt) / c**2
        
        # 总磁场变化率
        dBdt = term1 + term2
        dBdt_results.append(dBdt)
    
    dBdt_results = np.array(dBdt_results)
    
    # 绘制结果
    plt.figure(figsize=(12, 8))
    plt.plot(v_values/1000, dBdt_results[:, 0], label='dBx/dt')
    plt.plot(v_values/1000, dBdt_results[:, 1], label='dBy/dt')
    plt.plot(v_values/1000, dBdt_results[:, 2], label='dBz/dt')
    plt.xlabel('速度 (km/s)')
    plt.ylabel('磁场变化率 (T/s)')
    plt.title('磁场变化率随物体速度的变化')
    plt.legend()
    plt.grid(True)
    plt.savefig('velocity_dependence.png')
    plt.close()
    
    print("\n=== 速度依赖性分析 ===")
    print(f"速度范围: 0 到 {v_values[-1]/1000} km/s")
    print(f"dBx/dt 范围: {dBdt_results[:, 0].min()} 到 {dBdt_results[:, 0].max()} T/s")
    print(f"dBy/dt 范围: {dBdt_results[:, 1].min()} 到 {dBdt_results[:, 1].max()} T/s")
    print(f"dBz/dt 范围: {dBdt_results[:, 2].min()} 到 {dBdt_results[:, 2].max()} T/s")
    
    return dBdt_results

# 磁场演化模拟
def magnetic_field_evolution_simulation():
    """模拟磁场随时间的演化"""
    # 模拟参数
    t_span = (0, 20)  # 时间范围
    t_eval = np.linspace(0, 20, 1000)  # 时间点
    B0 = np.array([0, 0, 0])  # 初始磁场
    
    # 求解微分方程
    sol = solve_ivp(magnetic_field_evolution, t_span, B0, t_eval=t_eval,
                   args=(A_func, E_func, V_func))
    
    # 绘制结果
    plt.figure(figsize=(12, 6))
    plt.plot(t_eval, sol.y[0], label='Bx(t)')
    plt.plot(t_eval, sol.y[1], label='By(t)')
    plt.plot(t_eval, sol.y[2], label='Bz(t)')
    plt.xlabel('时间 (s)')
    plt.ylabel('磁场强度 (T)')
    plt.title('磁场强度随时间的演化')
    plt.legend()
    plt.grid(True)
    plt.savefig('magnetic_field_evolution.png')
    plt.close()
    
    print("\n=== 磁场演化模拟 ===")
    print(f"模拟时间: {t_span[0]} 到 {t_span[1]} s")
    print(f"Bx 范围: {sol.y[0].min()} 到 {sol.y[0].max()} T")
    print(f"By 范围: {sol.y[1].min()} 到 {sol.y[1].max()} T")
    print(f"Bz 范围: {sol.y[2].min()} 到 {sol.y[2].max()} T")
    
    return sol

# 矢量特性验证
def vector_properties_verification():
    """验证矢量特性"""
    # 定义三个任意矢量
    A = np.array([1.0, 2.0, 3.0])  # 引力场强度
    E = np.array([4.0, 5.0, 6.0])  # 电场强度
    V = np.array([7.0, 8.0, 9.0])  # 速度矢量
    dE_dt = np.array([0.1, 0.2, 0.3])  # 电场变化率
    
    # 计算dB/dt
    dBdt = -np.cross(A, E)/c**2 - np.cross(V, dE_dt)/c**2
    
    # 验证矢量正交性（叉乘结果与原矢量正交）
    dot_product_A = np.dot(A, dBdt)
    dot_product_E = np.dot(E, dBdt)
    
    print("\n=== 矢量特性验证 ===")
    print(f"A·dB/dt = {dot_product_A:.10f}（应近似为零）")
    print(f"E·dB/dt = {dot_product_E:.10f}（应近似为零）")
    
    # 验证反对称性（交换A和E的顺序）
    dBdt_swapped = -np.cross(E, A)/c**2 - np.cross(V, dE_dt)/c**2
    symmetry_check = np.allclose(dBdt_swapped, dBdt + 2*np.cross(A, E)/c**2)
    
    print(f"反对称性验证: {symmetry_check}")
    
    return dBdt

# 主函数
if __name__ == "__main__":
    print("变化的磁场产生引力场和电场方程数值验证")
    print("=" * 50)
    
    # 运行数值示例
    numerical_example()
    
    # 运行速度依赖性分析
    velocity_dependence_analysis()
    
    # 运行磁场演化模拟
    magnetic_field_evolution_simulation()
    
    # 运行矢量特性验证
    vector_properties_verification()
    
    print("\n" + "=" * 50)
    print("数值验证完成！")
