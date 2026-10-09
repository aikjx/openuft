import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 符号定义与新公式实现 ==========
t, z, R0, omega, c, lamda = sp.symbols('t z R_0 omega c lambda', real=True, positive=True)
# 相位因子
phi = omega * (t - z/c)
# 新公式：动态位置函数
x_tz = R0 * sp.exp(lamda * t) * sp.cos(phi)
y_tz = R0 * sp.exp(lamda * t) * sp.sin(phi)
z_t = t * sp.sqrt(c**2 - (R0*omega)**2)

# 求速度分量
vx = sp.diff(x_tz, t)
vy = sp.diff(y_tz, t)
vz = sp.diff(z_t, t)

# ========== 2. 代入参数验证光速约束（慢演化近似） ==========
params = {R0: 1.0, omega: 0.6, c: 1.0, lamda: 0.01}  # 慢演化：lambda=0.01 << omega=0.6
# 化简合速度平方
v_total_sq = sp.simplify(vx**2 + vy**2 + vz**2)
# 代入参数计算（添加t=0作为参考时间点）
params_with_t = params.copy()
params_with_t[t] = 0.0  # 选择t=0作为计算点
v_total_sq_val = v_total_sq.subs(params_with_t)
v_total_val = sp.sqrt(v_total_sq_val)

print("===== 新公式光速约束验证 =====")
print(f"合速度平方（符号化简）：{sp.pretty(v_total_sq)}")
print(f"慢演化近似下合速度值：{float(v_total_val):.6f}（目标：c={params[c]}）")

# ========== 3. 数值可视化：连续演化的螺旋轨迹 ==========
def zuft_evolve_spiral(t_range, z_fixed=0, alpha=0.01):
    """计算连续演化的螺旋轨迹"""
    R0 = 1.0
    omega = 0.6
    c = 1.0
    vz = np.sqrt(c**2 - (R0*omega)**2)
    
    x_list = []
    y_list = []
    z_list = []
    for t_val in t_range:
        phi_val = omega * (t_val - z_fixed/c)
        R_t = R0 * np.exp(alpha * t_val)  # 演化的半径
        x = R_t * np.cos(phi_val)
        y = R_t * np.sin(phi_val)
        z = vz * t_val
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
    return x_list, y_list, z_list

# 生成时间序列
t_range = np.linspace(0, 20, 1000)
# 计算两种演化状态的轨迹
x_evolve, y_evolve, z_evolve = zuft_evolve_spiral(t_range, alpha=0.01)  # 慢演化
x_static, y_static, z_static = zuft_evolve_spiral(t_range, alpha=0.0)   # 静态（原有公式）

# 绘制对比图
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_evolve, y_evolve, z_evolve, color='red', label='含e的连续演化轨迹')
ax.plot(x_static, y_static, z_static, color='blue', linestyle='--', label='原有静态轨迹')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('ZUFT连续演化螺旋轨迹（含自然常数e）')
ax.legend()
plt.show()