import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 第一步：定义符号变量和时间t，螺旋半径r，角速度ω
t, r, omega = sp.symbols('t r omega', real=True)

# 第二步：写出三维螺旋运动中，在xy平面内的旋转分量（圆周运动）
x = r * sp.cos(omega * t)  # x坐标
y = r * sp.sin(omega * t)  # y坐标

print("1. 三维螺旋运动的横向（旋转）分量：")
print(f"   x(t) = {x}")
print(f"   y(t) = {y}")

# 第三步：引入复数，将二维平面运动表示为复平面上的一个点
# 定义复变量 Z(t) = x(t) + i*y(t)
i = sp.I  # 虚数单位
Z = x + i * y
print(f"\n2. 在复平面上表示该运动： Z(t) = x(t) + i*y(t)")
print(f"   Z(t) = {Z}")

# 第四步：应用欧拉公式进行重构
# 根据欧拉公式 e^(iθ) = cosθ + i sinθ，令 θ = ωt
Z_euler = r * sp.exp(i * omega * t)
print(f"\n3. 应用欧拉公式 e^(iθ) = cosθ + i sinθ， 其中 θ = ω*t：")
print(f"   Z(t) = r * e^(i*ω*t) = {Z_euler}")

# 第五步：证明两种表示是等价的（数学恒等式）
# 展开复指数形式
Z_euler_expanded = sp.expand(Z_euler)
print(f"\n4. 展开复指数形式：")
print(f"   r * e^(i*ω*t) = {Z_euler_expanded}")
print(f"   其实部 Re = {sp.re(Z_euler_expanded)}")
print(f"   其虚部 Im = {sp.im(Z_euler_expanded)}")

# 判断是否与原始的x(t)+i*y(t)相等
equality = sp.simplify(Z - Z_euler)
print(f"\n5. 验证等价性： Z(t) - r*e^(iωt) = {equality}")
print(f"   是否恒等于0？ {equality == 0}")

# 第六步：验证复指数形式是微分方程 dZ/dt = iω Z 的解
# 对 Z = r * e^(iωt) 求导
dZ_dt = sp.diff(Z_euler, t)
print(f"\n6. 对复指数形式求导：")
print(f"   dZ/dt = d(r * e^(i*ω*t))/dt = {dZ_dt}")

# 计算 i * ω * Z
i_omega_Z = i * omega * Z_euler
print(f"   i * ω * Z = i * ω * (r * e^(i*ω*t)) = {i_omega_Z}")

# 验证两者相等
print(f"   验证 dZ/dt 是否等于 iωZ： {sp.simplify(dZ_dt - i_omega_Z) == 0}")
print(f"   这表明 Z(t) = r * e^(iωt) 是微分方程 dZ/dt = iω Z 的解。")

# 第七步：数值验证（代入具体值，直观感受）
print(f"\n7. 数值验证（取 r=1, ω=2, t=0.5）：")
r_val, omega_val, t_val = 1.0, 2.0, 0.5
# 传统三角函数计算
x_val = r_val * np.cos(omega_val * t_val)
y_val = r_val * np.sin(omega_val * t_val)
z_traditional = x_val + 1j * y_val
# 欧拉公式计算
z_euler = r_val * np.exp(1j * omega_val * t_val)

print(f"   三角函数计算： Z({t_val}) = {x_val} + i*{y_val} = {z_traditional}")
print(f"   欧拉公式计算： Z({t_val}) = {r_val} * exp(i*{omega_val}*{t_val}) = {z_euler}")
print(f"   两者是否近似相等？ {np.allclose(z_traditional, z_euler)}")

# 第八步：详细计算数据
print(f"\n8. 详细计算数据：")
print(f"   常数取值：r = {r_val}, ω = {omega_val}, t = {t_val}")
print(f"   角度计算：θ = ω·t = {omega_val} × {t_val} = {omega_val*t_val} 弧度")
print(f"   三角函数值：cos(θ) = {np.cos(omega_val*t_val):.6f}, sin(θ) = {np.sin(omega_val*t_val):.6f}")
print(f"   x坐标：x(t) = r·cos(ωt) = {r_val} × {np.cos(omega_val*t_val):.6f} = {x_val:.6f}")
print(f"   y坐标：y(t) = r·sin(ωt) = {r_val} × {np.sin(omega_val*t_val):.6f} = {y_val:.6f}")
print(f"   指数计算：e^(iθ) = e^(i×{omega_val*t_val}) = {np.exp(1j*omega_val*t_val):.6f}")
print(f"   欧拉公式验证：cos(θ)+i·sin(θ) = {np.cos(omega_val*t_val):.6f} + i×{np.sin(omega_val*t_val):.6f} = {z_traditional:.6f}")
print(f"   两种方法结果对比：")
print(f"     三角函数法：{z_traditional:.6f}")
print(f"     欧拉公式法：{z_euler:.6f}")
print(f"     绝对误差：|z_traditional - z_euler| = {abs(z_traditional - z_euler):.12f}")

# 第九步：详细求导过程
print(f"\n9. 详细求导过程：")
print(f"   复指数形式：Z(t) = r·e^(iωt)")
print(f"   求导规则：d/dt [e^(at)] = a·e^(at)，其中a = iω")
print(f"   第一步求导：dZ/dt = r·d/dt [e^(iωt)] = r·iω·e^(iωt)")
print(f"   第二步化简：dZ/dt = iω·r·e^(iωt) = iω·Z(t)")
print(f"   结论：dZ/dt = iωZ，验证了复指数形式是该微分方程的解")

# 第十步：螺旋运动可视化
print(f"\n10. 螺旋运动可视化：")
print(f"   生成三维螺旋运动轨迹...")

# 生成螺旋运动数据
t_values = np.linspace(0, 2*np.pi, 100)
z_values = np.linspace(0, 4, 100)  # z轴方向的线性运动

# 计算x, y坐标
x_spiral = r_val * np.cos(omega_val * t_values)
y_spiral = r_val * np.sin(omega_val * t_values)

# 创建3D图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制螺旋线
ax.plot(x_spiral, y_spiral, z_values, 'b-', linewidth=2, label='螺旋轨迹')

# 绘制初始点
ax.scatter(x_spiral[0], y_spiral[0], z_values[0], c='r', s=100, label='起始点')

# 绘制xy平面投影
ax.plot(x_spiral, y_spiral, np.zeros_like(x_spiral), 'g--', linewidth=1, label='xy平面投影')

# 设置坐标轴标签
ax.set_xlabel('X 坐标')
ax.set_ylabel('Y 坐标')
ax.set_zlabel('Z 坐标')

# 设置标题
ax.set_title('三维螺旋运动轨迹')

# 添加图例
ax.legend()

# 调整视角
ax.view_init(elev=30, azim=45)

# 保存图像
plt.savefig('spiral_motion.png', dpi=150, bbox_inches='tight')
print(f"   螺旋运动轨迹已保存为 'spiral_motion.png'")

# 显示图像
plt.show()
