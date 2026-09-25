#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT 挠率场 / E/B 场静态分布仿真
===================================
仿真静态点源的挠率场，映射出电场E和磁场B的空间分布
支持：屏蔽汤川型 / 长程库仑型 切换
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ===================== 全局参数 =====================
c = 299792458.0
hbar = 1.054571817e-34
eps0 = 8.8541878128e-12
mu0 = 1.25663706212e-6

k = 1.0               # 拓扑-电磁耦合常数
mu_screen = 1.0e15   # 屏蔽参数 (mu=0退化为长程库仑)
C_tau = 1.0           # 挠率点源强度
eps_tau = eps0
mu_tau = mu0

# ===================== 径向场计算 =====================
def tau_field(r, mu):
    """静态球对称挠率场 tau(r) = C/r * exp(-mu*r)"""
    return C_tau / r * np.exp(-mu * r)

def e_field_from_tau(r, mu):
    """静电场 E = -kc * d(tau_t)/dr (球对称径向)"""
    tau = tau_field(r, mu)
    dtau_dr = -C_tau * np.exp(-mu * r) * (1 + mu * r) / r**2
    E = -k * c * dtau_dr
    return E, tau

def energy_density(E, B):
    """电磁能量密度 u = 0.5*(eps*E^2 + B^2/mu)"""
    return 0.5 * (eps_tau * E**2 + B**2 / mu_tau)

# ===================== 径向分布 =====================
r_min, r_max = 1e-16, 2e-14
Nr = 1000
r_arr = np.logspace(np.log10(r_min), np.log10(r_max), Nr)

# 屏蔽场 (汤川型)
E_screen, tau_screen = e_field_from_tau(r_arr, mu_screen)
B_screen = np.zeros_like(r_arr)  # 纯径向场旋度为零
u_screen = energy_density(E_screen, B_screen)

# 无屏蔽场 (库仑型, mu=0)
E_coul, tau_coul = e_field_from_tau(r_arr, 0.0)
u_coul = energy_density(E_coul, B_screen)

# ===================== 绘图 =====================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. 挠率场
ax = axes[0, 0]
ax.loglog(r_arr, np.abs(tau_screen), label=f'屏蔽 μ={mu_screen:.1e}', linewidth=2)
ax.loglog(r_arr, np.abs(tau_coul), label='库仑 μ=0', linestyle='--', linewidth=2)
ax.set_title('挠率场 |τ(r)| 静态点源', fontsize=13)
ax.set_xlabel('r [m]', fontsize=11)
ax.set_ylabel('|τ|', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# 2. 电场
ax = axes[0, 1]
ax.loglog(r_arr, np.abs(E_screen), label=f'屏蔽 μ={mu_screen:.1e}', linewidth=2)
ax.loglog(r_arr, np.abs(E_coul), label='库仑 μ=0', linestyle='--', linewidth=2)
ax.set_title('映射电场 |E(r)|', fontsize=13)
ax.set_xlabel('r [m]', fontsize=11)
ax.set_ylabel('|E| [V/m]', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# 3. 能量密度
ax = axes[1, 0]
ax.loglog(r_arr, u_screen, label=f'屏蔽 μ={mu_screen:.1e}', linewidth=2)
ax.loglog(r_arr, u_coul, label='库仑 μ=0', linestyle='--', linewidth=2)
ax.set_title('TUFT电磁能量密度 u(r)', fontsize=13)
ax.set_xlabel('r [m]', fontsize=11)
ax.set_ylabel('u [J/m³]', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# 4. 屏蔽因子
ax = axes[1, 1]
screen_factor = np.exp(-mu_screen * r_arr)
ax.semilogy(r_arr, screen_factor, 'r-', linewidth=2)
ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.7)
ax.axhline(y=0.01, color='gray', linestyle=':', alpha=0.7)
ax.set_title('汤川屏蔽因子 exp(-μr)', fontsize=13)
ax.set_xlabel('r [m]', fontsize=11)
ax.set_ylabel('屏蔽因子', fontsize=11)
ax.text(r_arr[10], 0.55, '50%', fontsize=9, color='gray')
ax.text(r_arr[10], 0.012, '1%', fontsize=9, color='gray')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('tuft_field_simulation.png', dpi=150, bbox_inches='tight')
print("仿真图保存: tuft_field_simulation.png")

# ===================== 数值输出 =====================
print("\n===== 关键采样点数据 =====")
print(f"{'r[m]':<14}{'|τ|':<14}{'|E|[V/m]':<14}{'u[J/m³]':<14}")
for r in [1e-15, 3e-15, 5e-15, 1e-14, 2e-14]:
    E, tau = e_field_from_tau(r, mu_screen)
    u = energy_density(E, 0)
    print(f"{r:14.2e}{tau:14.4e}{abs(E):14.4e}{u:14.4e}")

print("\n===== 仿真完成 =====")
print(f"屏蔽参数 μ = {mu_screen:.2e} 1/m")
print(f"力程 λ = 1/μ = {1/mu_screen:.4e} m = {1/mu_screen/1e-15:.3f} fm")
print(f"耦合常数 k = {k}")
print(f"光速 c = {c:.4e} m/s")
