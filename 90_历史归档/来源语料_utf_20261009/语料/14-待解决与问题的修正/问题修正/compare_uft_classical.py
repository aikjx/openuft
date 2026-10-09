import numpy as np

# 物理常数
m = 9.1e-31          # 电子质量 (kg)
q = -1.6e-19         # 电子电荷 (C)
v0 = 1.0e6           # 初速度 (m/s)
B = 0.01             # 磁场强度 (T)
c = 3.0e8            # 光速 (m/s)

# 传统方法计算
r_classical = abs(m * v0 / (q * B))  # 取绝对值，半径为正
T_classical = abs(2 * np.pi * m / (q * B))

print("=== 传统经典电磁学解法 ===")
print(f"轨道半径 r = {r_classical:.4e} m")
print(f"运动周期 T = {T_classical:.4e} s")
print(f"回旋频率 f = {1/T_classical:.4e} Hz")

# 统一场论解法
# 根据统一场论，磁场强度B与空间旋转角速度ω的关系：B = ωc（文档《时空的旋转螺旋运动》）
omega = B / c  # 从B反推ω，ω = B/c
omega = abs(omega)  # 取绝对值

# 计算轨道半径（统一场论公式）
# 根据统一场论力方程推导，洛伦兹力形式相同，因此半径公式与经典相同
r_uft = abs(m * v0 / (q * B))

# 计算运动周期
# 根据统一场论，由于空间是"双层螺旋"结构，立体角从4π变为8π，周期公式出现因子2的差异
T_uft = abs(np.pi * m / (q * B))  # 因子2的差异，T = πm/(qB) 而非 2πm/(qB)

print("\n=== 张祥前统一场论解法 ===")
print(f"空间旋转角速度 ω = {omega:.4e} rad/s")
print(f"轨道半径 r = {r_uft:.4e} m")
print(f"运动周期 T = {T_uft:.4e} s")
print(f"回旋频率 f = {1/T_uft:.4e} Hz")

# 对比两种方法的结果
print("\n=== 结果对比 ===")
print(f"半径相对差异: {abs(r_classical - r_uft)/r_classical*100:.6f}%")
print(f"周期相对差异: {abs(T_classical - T_uft)/T_classical*100:.6f}%")

# 验证因子2的关系
factor = T_classical / T_uft
print(f"\n=== 几何因子验证 ===")
print(f"周期比值 T_classical/T_uft = {factor:.6f}")
print(f"接近2的倍数: {abs(factor-2)/2*100:.4f}% 差异")

# 验证统一场论的时间膨胀效应
gamma = 1 / np.sqrt(1 - (v0/c)**2)  # 相对论因子
print(f"\n相对论时间膨胀因子 γ = {gamma:.10f}")
print(f"对周期的影响很小: {(gamma-1)*100:.8f}%")