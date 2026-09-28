import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# 第一部分：SymPy 符号计算验证推导
# ==========================================
print("="*50)
print("第一部分：符号计算验证")
print("="*50)

# 1. 定义符号与位置矢量
R, ω, c, t = sp.symbols('R ω c t', real=True, positive=True)
i, j, k = sp.Matrix([1,0,0]), sp.Matrix([0,1,0]), sp.Matrix([0,0,1])

# 论文修正后的标准方程 (1)
r = R*sp.cos(ω*t)*i + R*sp.sin(ω*t)*j + c*t*k
print("✅ 位置矢量 r(t):")
sp.pprint(r)

# 2. 验证速度与速率 (式2, 式3)
v = sp.diff(r, t)
v_mag = sp.simplify(v.norm())
print("\n✅ 速度矢量 v(t):")
sp.pprint(v)
print("\n✅ 速率 (化简后):")
sp.pprint(v_mag)

# 3. 验证加速度与正交性 (式4, 式5)
a = sp.diff(v, t)
a_mag = sp.simplify(a.norm())
v_dot_a = sp.simplify(v.dot(a))
print("\n✅ 加速度矢量 a(t):")
sp.pprint(a)
print("\n✅ 加速度大小:")
sp.pprint(a_mag)
print("\n✅ 速度与加速度点积 (验证正交性):")
sp.pprint(v_dot_a)

# 4. 验证切向/法向加速度
a_t = sp.diff(v_mag, t)
print("\n✅ 切向加速度 a_t:")
sp.pprint(a_t)

# 5. 验证曲率 κ (式8)
s = sp.symbols('s', real=True, positive=True)
v0 = v_mag
T = v / v0  # 单位切向量
dT_dt = sp.diff(T, t)
dT_ds = dT_dt / v0
κ = sp.simplify(dT_ds.norm())
print("\n✅ 曲率 κ:")
sp.pprint(κ)

# 6. 验证挠率 τ (式9)
r_3rd = sp.diff(a, t)  # 三阶导数
cross_v_a = v.cross(a)
cross_norm_sq = sp.simplify(cross_v_a.norm()**2)
mixed_product = sp.simplify(cross_v_a.dot(r_3rd))
τ = sp.simplify(mixed_product / cross_norm_sq)
print("\n✅ 挠率 τ:")
sp.pprint(τ)

# 7. 验证螺距与螺旋升角 (式10, 式11)
h = 2*sp.pi*c / ω
tan_lambda = c / (R*ω)
print("\n✅ 螺距 h:")
sp.pprint(h)
print("\n✅ 螺旋升角正切 tanλ:")
sp.pprint(tan_lambda)

# 8. 修正论文中的"经典关系式"笔误
print("\n" + "="*50)
print("⚠️  验证论文中的经典关系式 (发现笔误)")
print("="*50)
λ = sp.symbols('λ')
# 定义 cosλ = rω/v0, sinλ = c/v0
cosλ = R*ω / v0
sinλ = c / v0

print("\n❌ 论文声称 κ = cosλ/R:")
sp.pprint(sp.simplify(cosλ / R))
print("\n✅ 实际 κ = cos²λ/R:")
sp.pprint(sp.simplify(cosλ**2 / R))
print("\n验证相等性 (κ - cos²λ/R):", sp.simplify(κ - cosλ**2 / R) == 0)

print("\n❌ 论文声称 τ = sinλ/R:")
sp.pprint(sp.simplify(sinλ / R))
print("\n✅ 实际 τ = (sinλ cosλ)/R:")
sp.pprint(sp.simplify(sinλ * cosλ / R))
print("验证相等性 (τ - sinλ cosλ/R):", sp.simplify(τ - sinλ*cosλ/R) == 0)

# ==========================================
# 第二部分：NumPy 数值验证
# ==========================================
print("\n" + "="*50)
print("第二部分：数值实验验证")
print("="*50)

# 选取具体参数：R=2, ω=π(周期2秒), c=1(螺距2)
R_val = 2.0
ω_val = np.pi
c_val = 1.0
t_vals = np.linspace(0, 4, 200)

# 计算运动学量
x = R_val * np.cos(ω_val * t_vals)
y = R_val * np.sin(ω_val * t_vals)
z = c_val * t_vals

vx = -R_val * ω_val * np.sin(ω_val * t_vals)
vy = R_val * ω_val * np.cos(ω_val * t_vals)
vz = c_val * np.ones_like(t_vals)

ax = -R_val * ω_val**2 * np.cos(ω_val * t_vals)
ay = -R_val * ω_val**2 * np.sin(ω_val * t_vals)
az = np.zeros_like(t_vals)

# 验证1：速率恒定
v_mag_num = np.sqrt(vx**2 + vy**2 + vz**2)
v0_theory = np.sqrt(R_val**2 * ω_val**2 + c_val**2)
print(f"\n✅ 速率验证:")
print(f"   理论值: {v0_theory:.6f}")
print(f"   数值范围: [{v_mag_num.min():.6f}, {v_mag_num.max():.6f}]")
print(f"   最大误差: {np.max(np.abs(v_mag_num - v0_theory)):.2e}")

# 验证2：加速度大小恒定
a_mag_num = np.sqrt(ax**2 + ay**2 + az**2)
a_theory = R_val * ω_val**2
print(f"\n✅ 加速度大小验证:")
print(f"   理论值: {a_theory:.6f}")
print(f"   数值范围: [{a_mag_num.min():.6f}, {a_mag_num.max():.6f}]")
print(f"   最大误差: {np.max(np.abs(a_mag_num - a_theory)):.2e}")

# 验证3：速度与加速度正交
v_dot_a_num = vx*ax + vy*ay + vz*az
print(f"\n✅ 正交性验证 (v·a ≈ 0):")
print(f"   数值范围: [{v_dot_a_num.min():.2e}, {v_dot_a_num.max():.2e}]")

# 验证4：曲率与挠率恒定
κ_theory = R_val * ω_val**2 / v0_theory**2
τ_theory = c_val * ω_val / v0_theory**2
print(f"\n✅ 几何参数验证:")
print(f"   理论曲率 κ = {κ_theory:.6f}")
print(f"   理论挠率 τ = {τ_theory:.6f}")

# ==========================================
# 第三部分：可视化展示
# ==========================================
print("\n" + "="*50)
print("第三部分：可视化展示")
print("="*50)

fig = plt.figure(figsize=(14, 6))

# 1. 3D螺旋线与矢量图
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot(x, y, z, 'b-', label='螺旋轨迹', linewidth=2)

# 在 t=0, 1, 2 处绘制速度(红)和加速度(绿)矢量
t_points = [0, 1, 2]
for ti in t_points:
    idx = np.argmin(np.abs(t_vals - ti))
    xp, yp, zp = x[idx], y[idx], z[idx]
    vxp, vyp, vzp = vx[idx], vy[idx], vz[idx]
    axp, ayp, azp = ax[idx], ay[idx], az[idx]
    
    # 速度矢量 (缩放0.2)
    ax1.quiver(xp, yp, zp, vxp*0.2, vyp*0.2, vzp*0.2, 
               color='r', arrow_length_ratio=0.1, label='速度' if ti==0 else "")
    # 加速度矢量 (缩放0.1)
    ax1.quiver(xp, yp, zp, axp*0.1, ayp*0.1, azp*0.1, 
               color='g', arrow_length_ratio=0.1, label='加速度' if ti==0 else "")

ax1.set_xlabel('X'), ax1.set_ylabel('Y'), ax1.set_zlabel('Z')
ax1.set_title('空间圆柱螺旋线 (速度:红, 加速度:绿)')
ax1.legend()

# 2. 运动学量随时间变化
ax2 = fig.add_subplot(122)
ax2.plot(t_vals, v_mag_num, 'b-', label='速率', linewidth=1.5)
ax2.plot(t_vals, a_mag_num, 'g-', label='加速度大小', linewidth=1.5)
ax2.axhline(y=v0_theory, color='b', linestyle='--', alpha=0.7)
ax2.axhline(y=a_theory, color='g', linestyle='--', alpha=0.7)
ax2.set_xlabel('时间 t'), ax2.set_ylabel('数值')
ax2.set_title('速率与加速度大小的恒定性验证')
ax2.legend(), ax2.grid(True)

plt.tight_layout()
plt.show()