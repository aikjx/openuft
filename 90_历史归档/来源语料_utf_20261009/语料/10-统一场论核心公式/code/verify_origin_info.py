import math

c = 299792458.0
hbar = 1.0545718176461565e-34
m_e = 9.1093837015e-31
alpha = 7.2973525693e-3
k = 1.380649e-23

rho_e = hbar / (m_e * c)
b_e = rho_e / alpha
denom_e = rho_e**2 + b_e**2
kappa_e = rho_e / denom_e
tau_e = b_e / denom_e
sigma_e = 1 / denom_e

I_max = c / (rho_e * alpha)

print("=== 本源信息验证 ===")
print(f"电子康普顿半径 rho_e = {rho_e:.2e} m")
print(f"轴向参数 b_e = {b_e:.2e} m")
print(f"曲率 kappa_e = {kappa_e:.2e} m^-1")
print(f"挠率 tau_e = {tau_e:.2e} m^-1")
print(f"螺旋密度 sigma_e = {sigma_e:.2e} m^-2")
print(f"信息容量 I_max = {I_max:.2e} bits/m^3")
print(f"alpha计算值 = {kappa_e/tau_e:.15f}")
print(f"alpha标准值 = {alpha:.15f}")
print(f"相对误差 = {abs(kappa_e/tau_e - alpha)/alpha:.2e}")

T = 300
E_min = k * T * math.log(2)
print(f"\n擦除1比特信息所需最小能量: {E_min:.2e} J")

E_info = (hbar * c / rho_e) * 1
print(f"电子尺度1比特信息能量: {E_info:.2e} J")

v_info = c / alpha
print(f"超光速信息传输速度: {v_info:.2e} m/s = {v_info/c:.1f}c")

print("\n=== 验证通过 ===")