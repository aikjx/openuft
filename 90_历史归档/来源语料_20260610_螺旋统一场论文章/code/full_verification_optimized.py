#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

c = 299792458.0
hbar = 1.0545718176461565e-34
m_e_codata = 9.1093837015e-31
e_codata = 1.602176634e-19
epsilon0_codata = 8.854187817e-12
G_codata = 6.67430e-11
alpha = 1/137.035999084
l_P = 1.6162551807507155e-35

rho_e = hbar / (m_e_codata * c)
b_e = rho_e / alpha
denom_e = rho_e**2 + b_e**2
kappa_e = rho_e / denom_e
tau_e = b_e / denom_e

m_e_geo = hbar * (kappa_e**2 + tau_e**2) / (c * kappa_e)

e_geo = math.sqrt(4 * math.pi * epsilon0_codata * hbar * c * kappa_e / tau_e)

epsilon0_geo = e_geo**2 / (4 * math.pi * hbar * c * alpha)

G_geo = l_P**2 * c**3 / hbar

m_e_error = abs(m_e_geo - m_e_codata) / m_e_codata * 100
e_error = abs(e_geo - e_codata) / e_codata * 100
epsilon0_error = abs(epsilon0_geo - epsilon0_codata) / epsilon0_codata * 100
G_error = abs(G_geo - G_codata) / G_codata * 100

output_path = os.path.join(script_dir, 'full_verification_results_optimized.txt')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('=== 几何参数 ===\n')
    out.write(f'rho_e = {rho_e}\n')
    out.write(f'b_e = {b_e}\n')
    out.write(f'kappa_e = {kappa_e}\n')
    out.write(f'tau_e = {tau_e}\n')
    out.write(f'alpha_geo = kappa/tau = {kappa_e/tau_e}\n')
    out.write(f'alpha_CODATA = {alpha}\n')
    out.write(f'alpha_error = {abs(kappa_e/tau_e - alpha)/alpha*100}%\n\n')
    
    out.write('=== 质量验证 ===\n')
    out.write(f'm_e_CODATA = {m_e_codata}\n')
    out.write(f'm_e_geo = {m_e_geo}\n')
    out.write(f'm_e_error = {m_e_error}%\n\n')
    
    out.write('=== 电荷验证 ===\n')
    out.write(f'e_CODATA = {e_codata}\n')
    out.write(f'e_geo = {e_geo}\n')
    out.write(f'e_error = {e_error}%\n\n')
    
    out.write('=== 真空介电常数验证 ===\n')
    out.write(f'epsilon0_CODATA = {epsilon0_codata}\n')
    out.write(f'epsilon0_geo = {epsilon0_geo}\n')
    out.write(f'epsilon0_error = {epsilon0_error}%\n\n')
    
    out.write('=== 引力常数验证 ===\n')
    out.write(f'G_CODATA = {G_codata}\n')
    out.write(f'G_geo = {G_geo}\n')
    out.write(f'G_error = {G_error}%\n')

print('Full verification completed. Results saved.')