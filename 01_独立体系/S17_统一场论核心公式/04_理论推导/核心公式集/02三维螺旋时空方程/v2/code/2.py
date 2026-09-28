import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# 第一部分：SymPy 符号计算验证螺旋运动
# ==========================================
print("="*60)
print("第一部分：符号计算验证空间螺旋运动特性")
print("="*60)

# 1. 定义符号与位置矢量
# 注意：为避免混淆，方程中轴向速度用 v_z 表示，光速用 c0 表示
a, ω, v_z, t = sp.symbols('a ω v_z t', real=True, positive=True)
i, j, k = sp.Matrix([1,0,0]), sp.Matrix([0,1,0]), sp.Matrix([0,0,1])

# 你的方程：r(t) = a cosωt î + a sinωt ĵ + v_z t k̂
r = a * sp.cos(ω*t) * i + a * sp.sin(ω*t) * j + v_z * t * k
print("✅ 位置矢量 r(t):")
sp.pprint(r)

# 2. 验证速度与速率（匀速曲线运动）
v = sp.diff(r, t)
v_mag = sp.simplify(v.norm())
print("\n✅ 速度矢量 v(t):")
sp.pprint(v)
print("\n✅ 速率 (化简后):")
sp.pprint(v_mag)
print("   → 结论：速率与时间 t 无关，是匀速曲线运动")

# 3. 验证加速度（向心加速度）
a_acc = sp.diff(v, t)
a_mag = sp.simplify(a_acc.norm())
v_dot_a = sp.simplify(v.dot(a_acc))
print("\n✅ 加速度矢量 a(t):")
sp.pprint(a_acc)
print("\n✅ 加速度大小:")
sp.pprint(a_mag)
print("\n✅ 速度与加速度点积 (验证正交性):")
sp.pprint(v_dot_a)
print("   → 结论：点积为0，速度与加速度正交，仅改变方向，不改变大小")

# 4. 验证曲率 κ (螺旋线核心几何特性：常数)
s = sp.symbols('s', real=True, positive=True)
v0 = v_mag
T = v / v0  # 单位切向量
dT_dt = sp.diff(T, t)
dT_ds = dT_dt / v0
κ = sp.simplify(dT_ds.norm())
print("\n✅ 曲率 κ:")
sp.pprint(κ)
print("   → 结论：曲率与时间 t 无关，弯曲程度处处相同")

# 5. 验证挠率 τ (螺旋线核心几何特性：非零常数)
r_3rd = sp.diff(a_acc, t)  # 三阶导数
cross_v_a = v.cross(a_acc)
cross_norm_sq = sp.simplify(cross_v_a.norm()**2)
mixed_product = sp.simplify(cross_v_a.dot(r_3rd))
τ = sp.simplify(mixed_product / cross_norm_sq)
print("\n✅ 挠率 τ:")
sp.pprint(τ)
print("   → 结论：挠率与时间 t 无关且非零，空间扭转程度处处相同")

# 6. 验证螺距 h (等距螺旋线判定：常数)
h = 2 * sp.pi * v_z / ω
print("\n✅ 螺距 h:")
sp.pprint(h)
print("   → 结论：螺距与时间 t 无关，是等距圆柱螺旋线")

# ==========================================
# 第二部分：数值模拟与可视化
# ==========================================
print("\n" + "="*60)
print("第二部分：数值模拟与可视化")
print("="*60)

# 选取具体参数进行模拟
a_val = 1.0       # 螺旋半径
ω_val = 2 * np.pi # 角速度 (周期1秒)
v_z_val = 1.0     # 轴向速度
t_vals = np.linspace(0, 4, 500) # 模拟4个周期

# 计算轨迹坐标
x = a_val * np.cos(ω_val * t_vals)
y = a_val * np.sin(ω_val * t_vals)
z = v_z_val * t_vals

# 计算运动学量
vx = -a_val * ω_val * np.sin(ω_val * t_vals)
vy = a_val * ω_val * np.cos(ω_val * t_vals)
vz = v_z_val * np.ones_like(t_vals)

ax = -a_val * ω_val**2 * np.cos(ω_val * t_vals)
ay = -a_val * ω_val**2 * np.sin(ω_val * t_vals)
az = np.zeros_like(t_vals)

# 数值验证速率恒定
v_mag_num = np.sqrt(vx**2 + vy**2 + vz**2)
v0_theory = np.sqrt((a_val*ω_val)**2 + v_z_val**2)
print(f"\n✅ 数值验证速率恒定:")
print(f"   理论值: {v0_theory:.6f}")
print(f"   数值波动范围: [{v_mag_num.min():.12f}, {v_mag_num.max():.12f}]")
print(f"   最大误差: {np.max(np.abs(v_mag_num - v0_theory)):.2e}")

# 可视化
fig = plt.figure(figsize=(16, 7))

# 1. 3D螺旋线轨迹
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot(x, y, z, 'b-', label='螺旋轨迹', linewidth=2)

# 在 t=0, 1, 2, 3 处绘制速度(红)和加速度(绿)矢量
t_points = [0, 1, 2, 3]
scale_v = 0.15  # 速度矢量缩放
scale_a = 0.05  # 加速度矢量缩放
for ti in t_points:
    idx = np.argmin(np.abs(t_vals - ti))
    xp, yp, zp = x[idx], y[idx], z[idx]
    vxp, vyp, vzp = vx[idx], vy[idx], vz[idx]
    axp, ayp, azp = ax[idx], ay[idx], az[idx]
    
    ax1.quiver(xp, yp, zp, vxp*scale_v, vyp*scale_v, vzp*scale_v, 
               color='r', arrow_length_ratio=0.1, label='速度' if ti==0 else "")
    ax1.quiver(xp, yp, zp, axp*scale_a, ayp*scale_a, azp*scale_a, 
               color='g', arrow_length_ratio=0.1, label='加速度' if ti==0 else "")

ax1.set_xlabel('X'), ax1.set_ylabel('Y'), ax1.set_zlabel('Z')
ax1.set_title('空间圆柱螺旋线轨迹 (速度:红, 加速度:绿)')
ax1.legend()
ax1.view_init(elev=20, azim=45)

# 2. 运动学量随时间变化
ax2 = fig.add_subplot(122)
ax2.plot(t_vals, v_mag_num, 'b-', label='速率', linewidth=2)
ax2.axhline(y=v0_theory, color='b', linestyle='--', alpha=0.7, label='理论速率')
ax2.set_xlabel('时间 t (s)'), ax2.set_ylabel('数值')
ax2.set_title('速率的恒定性验证')
ax2.legend(), ax2.grid(True)

plt.tight_layout()
plt.show()

# ==========================================
# 第三部分：速率分析与光速关联的物理说明
# ==========================================
print("\n" + "="*60)
print("第三部分：速率分析与光速关联的物理说明")
print("="*60)

c0 = 299792458  # 真空中光速

# 1. 通用模型的速率公式
print(f"\n1. 通用数学模型的速率:")
print(f"   v = √[(aω)² + v_z²]")
print(f"   → 这是一个可任意取值的常数，由参数 a, ω, v_z 决定，不天然等于光速。")

# 2. 场景一：圆偏振光的电场矢量轨迹（等于光速）
print(f"\n2. 物理场景一：圆偏振光的电场矢量轨迹")
print(f"   物理约束：电磁波沿 z 轴传播，群速度（能量传播速度）恒等于光速 c0。")
print(f"   此时，电场矢量端点的轴向传播速度 v_z = c0。")
print(f"   注意：这里的螺旋是电场矢量的端点轨迹，不是光子的经典运动轨迹；")
print(f"         切向分量是相速度，不传递能量，不违背相对论。")

# 3. 场景二：带电粒子的相对论螺旋运动（光速上限）
print(f"\n3. 物理场景二：带电粒子的相对论螺旋运动")
print(f"   物理约束：有静质量的实物粒子，遵循狭义相对论。")
print(f"   相对论限制：当 v → c0 时，需要无穷大的能量，因此 v < c0。")
print(f"   实验验证：大型强子对撞机可将质子加速到 0.99999999c0，但永远无法达到 c0。")

print(f"\n✅ 总结：")
print(f"   方程本身是正确的空间圆柱螺旋线模型；")
print(f"   是否等于光速，取决于具体的物理应用场景和约束条件。")