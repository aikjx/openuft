"""
v5.4 · 正确归一化与兰姆移位计算
================================
"""
import math
import numpy as np
from scipy.integrate import simpson, quad
import warnings
warnings.filterwarnings("ignore")

c = 299792458.0
hbar = 1.054571817e-34
alpha = 7.2973525693e-3
m_e = 9.1093837015e-31
e = 1.602176634e-19
eps_0 = 8.8541878128e-12
h = 6.62607015e-34
pi = math.pi

R_e = hbar / (m_e * c)
a0 = 4*pi*eps_0*hbar**2/(m_e*e**2)

# 正确的类氢径向波函数 (数值确定归一化)
# R_{20}(r) = N_{2S} * (r/a₀) * (2 - r/a₀) * exp(-r/(2a₀))
# R_{21}(r) = N_{2P} * (r/a₀)^2 * exp(-r/(2a₀))

# 首先确定归一化常数
r_test = np.linspace(0, 50*a0, 50000)
dr = r_test[1] - r_test[0]

# 2S 未归一化
R2S_unnorm = (r_test/a0) * (2 - r_test/a0) * np.exp(-r_test/(2*a0))
rho2S_unnorm = R2S_unnorm**2 * r_test**2
norm2S_sq = simpson(rho2S_unnorm, r_test)
N2S = 1.0 / math.sqrt(norm2S_sq)
print(f"2S: ∫|R|²r²dr (unnorm) = {norm2S_sq:.6f}")
print(f"2S: N = {N2S:.10e}")

# 2P 未归一化
R2P_unnorm = (r_test/a0)**2 * np.exp(-r_test/(2*a0))
rho2P_unnorm = R2P_unnorm**2 * r_test**2
norm2P_sq = simpson(rho2P_unnorm, r_test)
N2P = 1.0 / math.sqrt(norm2P_sq)
print(f"2P: ∫|R|²r²dr (unnorm) = {norm2P_sq:.6f}")
print(f"2P: N = {N2P:.10e}")

# 验证
R2S_norm = N2S * R2S_unnorm
R2P_norm = N2P * R2P_unnorm
check_2S = simpson(R2S_norm**2 * r_test**2, r_test)
check_2P = simpson(R2P_norm**2 * r_test**2, r_test)
print(f"验证: ∫|R2S|²r²dr = {check_2S:.10f}")
print(f"验证: ∫|R2P|²r²dr = {check_2P:.10f}")

# 环电荷势 (numpy版)
def V_ring(r):
    return e / (4*pi*eps_0*np.sqrt(r**2 + R_e**2))

def V_coul(r):
    return e / (4*pi*eps_0*r)

# 兰姆移位矩阵元
delta_V = V_coul(r_test) - V_ring(r_test)

# 被积函数
integrand_2S = R2S_norm**2 * r_test**2 * delta_V
integrand_2P = R2P_norm**2 * r_test**2 * delta_V

E_2S = simpson(integrand_2S, r_test)
E_2P = simpson(integrand_2P, r_test)
delta_E = E_2S - E_2P
delta_f = delta_E / h

print(f"\n兰姆移位 (环电荷势修正):")
print(f"  ⟨δV⟩_2S = {E_2S:.6e} J = {E_2S/h/1e6:.4f} MHz")
print(f"  ⟨δV⟩_2P = {E_2P:.6e} J = {E_2P/h/1e6:.4f} MHz")
print(f"  ΔE = E_2S - E_2P = {delta_E:.6e} J")
print(f"  δf_Lamb = {delta_f:.4e} Hz = {delta_f/1e6:.4f} MHz")

# 与实验对比
f_exp = 1057.862
print(f"\n实验值: {f_exp:.3f} MHz")
print(f"几何预测: {delta_f/1e6:.4f} MHz")
print(f"比值: {delta_f/1e6/f_exp:.4f}")

# 各区域贡献
print(f"\n各距离段贡献:")
regions = [(0, 0.1*R_e, "0-0.1R_e"), (0.1*R_e, R_e, "0.1R_e-R_e"), 
           (R_e, 0.1*a0, "R_e-0.1a₀"), (0.1*a0, a0, "0.1a₀-a₀"),
           (a0, 5*a0, "a₀-5a₀"), (5*a0, 20*a0, "5a₀-20a₀")]
for r_lo, r_hi, name in regions:
    mask = (r_test >= r_lo) & (r_test <= r_hi)
    e2s_seg = simpson(integrand_2S[mask], r_test[mask])
    e2p_seg = simpson(integrand_2P[mask], r_test[mask])
    print(f"  {name:>12s}: ΔE = {e2s_seg - e2p_seg:.6e} J = {(e2s_seg - e2p_seg)/h/1e6:.4f} MHz")
