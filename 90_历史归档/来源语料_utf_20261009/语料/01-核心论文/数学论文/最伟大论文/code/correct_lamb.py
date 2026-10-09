"""
v5.5 · 正确氢原子波函数 + 环电荷势 → 兰姆移位
==============================================
正确归一化:
  R_{20}(r) = 1/(2√2 a₀^{3/2}) * (2 - r/a₀) * exp(-r/(2a₀))
  R_{21}(r) = 1/(2√6 a₀^{3/2}) * (r/a₀) * exp(-r/(2a₀))
验证:
  ∫|R_{20}|² r² dr = 1,  ∫|R_{21}|² r² dr = 1
  |ψ_{20}(0)|² = 1/(8π a₀³) ✓ (NIST 标准值)
  |ψ_{21}(0)|² = 0 ✓ (p-wave 在原点为零)
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
e_charge = 1.602176634e-19
eps_0 = 8.8541878128e-12
h_planck = 6.62607015e-34
pi = math.pi

R_e = hbar / (m_e * c)
a0 = 4*pi*eps_0*hbar**2/(m_e*e_charge**2)
Ec = m_e * c**2

print('='*70)
print('v5.5 · 正确氢原子波函数 + 环电荷势')
print('='*70)
print(f'R_e = {R_e:.6e} m')
print(f'a₀ = {a0:.6e} m')
print(f'α = R_e/a₀ = {alpha:.6e}')

# ===== 正确的归一化波函数 =====
# 2S: l=0, n=2
def R_2S(r):
    return (1/(2*math.sqrt(2)*a0**1.5)) * (2 - r/a0) * math.exp(-r/(2*a0))

# 2P: l=1, n=2
def R_2P(r):
    return (1/(2*math.sqrt(6)*a0**1.5)) * (r/a0) * math.exp(-r/(2*a0))

# 验证归一化
print('\n【波函数验证】')
def rho_2S(r):
    return R_2S(r)**2 * r**2

def rho_2P(r):
    return R_2P(r)**2 * r**2

# 使用 quad 从 0 到 ∞
n2S, _ = quad(rho_2S, 0, 50*a0, limit=500)
n2P, _ = quad(rho_2P, 0, 50*a0, limit=500)
print(f'  ∫|R_{{20}}|² r² dr = {n2S:.10f} (应为 1.0)')
print(f'  ∫|R_{{21}}|² r² dr = {n2P:.10f} (应为 1.0)')

# 原点值
print(f'  R_{{20}}(0) = {R_2S(0):.6e} (非零, s-wave)')
print(f'  R_{{21}}(0) = {R_2P(0):.6e} (零, p-wave)')
print(f'  |ψ_{{20}}(0)|² = {R_2S(0)**2/(4*pi):.6e} m⁻³ (标准值: {1/(8*pi*a0**3):.6e})')

# ===== 环电荷势 =====
def V_ring(r):
    return e_charge / (4*pi*eps_0*np.sqrt(r**2 + R_e**2))

def V_coul(r):
    return e_charge / (4*pi*eps_0*r)

# ===== 兰姆移位矩阵元 =====
print('\n' + '='*70)
print('【兰姆移位矩阵元】')

# 被积函数 (2S)
def integrand_2S(r):
    dV = V_coul(r) - V_ring(r)
    return rho_2S(r) * dV

# 被积函数 (2P)
def integrand_2P(r):
    dV = V_coul(r) - V_ring(r)
    return rho_2P(r) * dV

# 积分 (排除 r=0 点, 避免 0*∞ 问题)
r_min = 1e-30  # 极短距离
r_max = 50*a0

E_2S, err_2S = quad(integrand_2S, r_min, r_max, limit=1000)
E_2P, err_2P = quad(integrand_2P, r_min, r_max, limit=1000)
delta_E = E_2S - E_2P
delta_f = delta_E / h_planck

print(f'\n  ⟨V_Coul - V_ring⟩_{{20}} = {E_2S:.10e} J ± {err_2S:.2e}')
print(f'  ⟨V_Coul - V_ring⟩_{{21}} = {E_2P:.10e} J ± {err_2P:.2e}')
print(f'  ΔE = E_{{20}} - E_{{21}} = {delta_E:.10e} J')
print(f'  δf = ΔE/h = {delta_f:.4e} Hz = {delta_f/1e6:.6f} MHz')

# ===== 各距离段贡献 =====
print('\n' + '='*70)
print('【各距离段贡献分析】')

segments = [
    (1e-30, 0.01*R_e, "0 - 0.01R_e"),
    (0.01*R_e, 0.1*R_e, "0.01R_e - 0.1R_e"),
    (0.1*R_e, R_e, "0.1R_e - R_e"),
    (R_e, 0.01*a0, "R_e - 0.01a₀"),
    (0.01*a0, 0.1*a0, "0.01a₀ - 0.1a₀"),
    (0.1*a0, a0, "0.1a₀ - a₀"),
    (a0, 5*a0, "a₀ - 5a₀"),
    (5*a0, 20*a0, "5a₀ - 20a₀"),
]

print(f'  {"区域":>25s} {"E_2S (J)":>15s} {"E_2P (J)":>15s} {"ΔE (J)":>15s} {"δf (MHz)":>15s}')
total_dE = 0
for r_lo, r_hi, name in segments:
    e2s_s, _ = quad(integrand_2S, r_lo, r_hi, limit=200)
    e2p_s, _ = quad(integrand_2P, r_lo, r_hi, limit=200)
    de_s = e2s_s - e2p_s
    total_dE += de_s
    print(f'  {name:>25s} {e2s_s:15.10e} {e2p_s:15.10e} {de_s:15.10e} {de_s/h_planck/1e6:15.6f}')

print(f'\n  分段总和 ΔE = {total_dE:.10e} J')
print(f'  整体积分 ΔE = {delta_E:.10e} J')

# ===== 与实验对比 =====
print('\n' + '='*70)
print('【与实验对比 · CODATA 2018】')
f_exp = 1057.862  # MHz
print(f'\n  实验值:  f_Lamb = {f_exp:.3f} MHz')
print(f'  几何预测: f_geom = {delta_f/1e6:.6f} MHz')
ratio = delta_f/1e6 / f_exp
print(f'  比值: f_geom/f_exp = {ratio:.6f} ({ratio*100:.2f}%)')

# ===== 解析估算验证 =====
print('\n' + '='*70)
print('【解析估算验证】')
print(f'''
  远场近似 (r >> R_e):
    δV(r) ≈ V_Coul × (R_e/r)² / 2
  
  主要贡献来自 r ≈ a₀ (2S 概率密度峰值):
    |R_{{20}}(a₀)|² = {R_2S(a0)**2:.6e} m⁻³
    δV(a₀) ≈ V_Coul(a₀) × (R_e/a₀)²/2 = {e_charge**2/(4*pi*eps_0*a0)*(R_e/a0)**2/2:.6e} J
    ΔE_估算 ≈ |R|² × δV × 4πa₀² × Δr
         ≈ |R|² × δV × 4πa₀² × a₀
         ≈ {R_2S(a0)**2 * e_charge**2/(4*pi*eps_0*a0)*(R_e/a0)**2/2 * 4*pi*a0**2 * a0:.6e} J
    δf_估算 ≈ {R_2S(a0)**2 * e_charge**2/(4*pi*eps_0*a0)*(R_e/a0)**2/2 * 4*pi*a0**3 / h_planck / 1e6:.4f} MHz

  精确值: δf = {delta_f/1e6:.4f} MHz
  估算准确度: {delta_f/1e6 / (R_2S(a0)**2 * e_charge**2/(4*pi*eps_0*a0)*(R_e/a0)**2/2 * 4*pi*a0**3 / h_planck / 1e6):.4f}×
''')
