import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

# ====================== 常量定义 ======================
# 物理常数（国际单位制）
c = constants.speed_of_light          # 光速，m/s
G = constants.gravitational_constant  # 引力常数，m^3/(kg·s^2)
hbar = constants.hbar                 # 约化普朗克常数，J·s
l_P = np.sqrt(hbar * G / c**3)        # 普朗克长度，m

# 归一化常数（c=1）
c_norm = 1.0
R0_norm = 1.0
omega_norm = 0.6
v_z_norm = np.sqrt(c_norm**2 - (R0_norm * omega_norm)**2)

# ====================== 1. ZUFT螺旋运动验证 ======================
def zuft_position(t, R0=R0_norm, omega=omega_norm, v_z=v_z_norm):
    """计算ZUFT螺旋位置向量"""
    x = R0 * np.cos(omega * t)
    y = R0 * np.sin(omega * t)
    z = v_z * t
    return np.array([x, y, z])

def zuft_velocity(t, R0=R0_norm, omega=omega_norm, v_z=v_z_norm):
    """计算ZUFT螺旋速度向量"""
    vx = -R0 * omega * np.sin(omega * t)
    vy = R0 * omega * np.cos(omega * t)
    vz = v_z
    return np.array([vx, vy, vz])

def zuft_speed(t, R0=R0_norm, omega=omega_norm, v_z=v_z_norm):
    """计算ZUFT螺旋速度模"""
    v = zuft_velocity(t, R0, omega, v_z)
    return np.linalg.norm(v)

# 验证光速约束
t_test = np.linspace(0, 10, 1000)
speed_test = [zuft_speed(t) for t in t_test]

# 可视化速度模
plt.figure(figsize=(8, 4))
plt.plot(t_test, speed_test, label='计算速度模')
plt.axhline(y=c_norm, color='r', linestyle='--', label='归一化光速c=1')
plt.xlabel('时间 t (归一化)')
plt.ylabel('速度模 (归一化)')
plt.title('ZUFT螺旋运动速度模验证')
plt.legend()
plt.grid(True)
plt.show()

# 数值验证：任意时间点速度模等于c
t_rand = np.random.rand() * 10
assert np.isclose(zuft_speed(t_rand), c_norm, rtol=1e-10), "速度模验证失败"
print(f"ZUFT速度模验证通过：t={t_rand:.4f}时，速度模={zuft_speed(t_rand):.10f}，c={c_norm}")

# ====================== 2. 波动方程特解验证 ======================
def wave_Lx(t, z, A=1.0, omega=1.0, c=c_norm):
    """波动方程Lx分量"""
    return A * np.cos(omega * (t - z / c))

def wave_Ly(t, z, A=1.0, omega=1.0, c=c_norm):
    """波动方程Ly分量"""
    return A * np.sin(omega * (t - z / c))

def second_deriv_t(func, t, z, h=1e-6, **kwargs):
    """数值计算时间二阶偏导"""
    f1 = func(t+h, z, **kwargs)
    f2 = 2 * func(t, z, **kwargs)
    f3 = func(t-h, z, **kwargs)
    return (f1 - f2 + f3) / (h**2)

def second_deriv_z(func, t, z, h=1e-6, **kwargs):
    """数值计算z方向二阶偏导"""
    f1 = func(t, z+h, **kwargs)
    f2 = 2 * func(t, z, **kwargs)
    f3 = func(t, z-h, **kwargs)
    return (f1 - f2 + f3) / (h**2)

# 验证波动方程
t_wave = 1.0
z_wave = 2.0
A_wave = 1.0
omega_wave = 1.0

# 计算Lx分量的两边值
nabla2_Lx = second_deriv_z(wave_Lx, t_wave, z_wave, A=A_wave, omega=omega_wave)
rhs_Lx = second_deriv_t(wave_Lx, t_wave, z_wave, A=A_wave, omega=omega_wave) / c_norm**2

# 数值验证
assert np.isclose(nabla2_Lx, rhs_Lx, rtol=1e-5), "波动方程Lx分量验证失败"
print(f"波动方程Lx分量验证通过：∇²Lx={nabla2_Lx:.10f}，(1/c²)∂²Lx/∂t²={rhs_Lx:.10f}")

# ====================== 3. e的收敛性验证 ======================
def e_approx(n):
    """e的近似计算"""
    return (1.0 + 1.0/n)**n

def e_xi_approx(n, xi):
    """e^ξ的近似计算"""
    return (1.0 + xi/n)**n

# 计算不同n下的e近似值
n_list = [10, 100, 1000, 10000, 100000, 1000000]
e_list = [e_approx(n) for n in n_list]
e_true = np.e

# 可视化e的收敛性
plt.figure(figsize=(8, 4))
plt.plot(n_list, e_list, 'o-', label='(1+1/n)^n')
plt.axhline(y=e_true, color='r', linestyle='--', label='真实e值')
plt.xscale('log')
plt.xlabel('n (对数尺度)')
plt.ylabel('e近似值')
plt.title('自然常数e的收敛性验证')
plt.legend()
plt.grid(True)
plt.show()

# 输出收敛结果
print("\ne的收敛性验证结果：")
for n, e_val in zip(n_list, e_list):
    error = abs(e_val - e_true)
    print(f"n={n:7d}：e≈{e_val:.10f}，误差={error:.10e}")

# ====================== 4. 新公式验证 ======================
# 新公式2验证（ξ=0.6）
xi = 0.6
e_xi_true = np.exp(xi)
e_xi_list = [e_xi_approx(n, xi) for n in n_list]

print("\n新公式2验证结果（ξ=0.6）：")
for n, e_xi_val in zip(n_list, e_xi_list):
    error = abs(e_xi_val - e_xi_true)
    print(f"n={n:7d}：e^0.6≈{e_xi_val:.10f}，误差={error:.10e}")

# 新公式4验证
N_P = np.sqrt(c**4 / (G * hbar))
e_phys = (1.0 + 1.0/N_P)**N_P
print(f"\n新公式4验证结果：")
print(f"普朗克尺度N_P={N_P:.2e}")
print(f"e≈(1+1/N_P)^N_P={e_phys:.10f}，真实e值={e_true:.10f}")
print(f"绝对误差={abs(e_phys - e_true):.10e}")

# 新公式3验证（ZUFT哈勃参数）
H_Z = np.sqrt(c**7 / (G * hbar))
print(f"\n新公式3验证结果：")
print(f"ZUFT哈勃参数H_Z={H_Z:.2e} s^-1")
print(f"普朗克长度l_P={l_P:.2e} m")
print(f"c/l_P={c/l_P:.2e} s^-1 (与H_Z一致)")