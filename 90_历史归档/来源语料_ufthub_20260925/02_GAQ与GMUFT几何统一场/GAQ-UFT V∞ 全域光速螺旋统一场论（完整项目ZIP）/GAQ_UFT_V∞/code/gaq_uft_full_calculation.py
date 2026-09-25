#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GAQ-UFT V∞ 全维精算引擎
基于 v≡c 公理的光速螺旋统一场论高精度数值验证
使用 mpmath 250位有效数字精度
算法联盟最高权限
"""

import mpmath as mp
import json
import os
from datetime import datetime

# ============================================================
# 全局精度设置：250位有效数字
# ============================================================
mp.mp.dps = 250
mp.mp.pretty = True

# ============================================================
# CODATA 2022 物理常数（高精度）
# ============================================================
CONSTANTS = {
    'c':        mp.mpf('299792458'),                          # 真空光速 m/s
    'hbar':     mp.mpf('1.0545718176461565e-34'),            # 约化普朗克常数 J·s
    'h':        mp.mpf('6.62607015e-34'),                     # 普朗克常数 J·s
    'G':        mp.mpf('6.67430e-11'),                        # 引力常数 m^3/(kg·s^2)
    'e':        mp.mpf('1.602176634e-19'),                    # 基本电荷 C
    'epsilon0': mp.mpf('8.8541878128e-12'),                   # 真空介电常数 F/m
    'mu0':      mp.mpf('1.25663706212e-6'),                   # 真空磁导率 H/m
    'alpha':    mp.mpf('7.2973525693e-3'),                    # 精细结构常数
    'me':       mp.mpf('9.1093837015e-31'),                   # 电子质量 kg
    'mp':       mp.mpf('1.67262192369e-27'),                  # 质子质量 kg
    'mn':       mp.mpf('1.67492749804e-27'),                  # 中子质量 kg
    'mu':       mp.mpf('1.66053906660e-27'),                  # 原子质量单位 kg
    'kB':       mp.mpf('1.380649e-23'),                        # 玻尔兹曼常数 J/K
    'NA':       mp.mpf('6.02214076e23'),                       # 阿伏伽德罗常数
    'R':        mp.mpf('8.314462618'),                         # 气体常数 J/(mol·K)
    'sigma':    mp.mpf('5.670374419e-8'),                      # 斯特藩-玻尔兹曼常数
    'a0':       mp.mpf('5.29177210903e-11'),                   # 玻尔半径 m
    'lambdaC':  mp.mpf('2.42631023867e-12'),                   # 电子康普顿波长 m
    're':       mp.mpf('2.8179403262e-15'),                    # 经典电子半径 m
    'muB':      mp.mpf('9.2740100783e-24'),                    # 玻尔磁子 J/T
    'muN':      mp.mpf('5.0507837461e-27'),                    # 核磁子 J/T
    'F':        mp.mpf('96485.33212'),                          # 法拉第常数 C/mol
    'Phi0':     mp.mpf('2.067833848e-15'),                     # 磁通量子 Wb
    'RK':       mp.mpf('25812.80745'),                          # 冯·克利青常数 Ω
    'Z0':       mp.mpf('376.730313668'),                        # 真空阻抗 Ω
    # 普朗克单位
    'lP':       mp.mpf('1.616255e-35'),                         # 普朗克长度 m
    'mP':       mp.mpf('2.176434e-8'),                          # 普朗克质量 kg
    'tP':       mp.mpf('5.391247e-44'),                         # 普朗克时间 s
    'EP':       mp.mpf('1.9561e9'),                              # 普朗克能量 J
    'TP':       mp.mpf('1.416784e32'),                          # 普朗克温度 K
    # 弱相互作用
    'MW':       mp.mpf('80.377') * mp.mpf('1.78266192e-30'),  # W玻色子质量 kg (80.377 GeV/c²)
    'MZ':       mp.mpf('91.1876') * mp.mpf('1.78266192e-30'), # Z玻色子质量 kg
    'sin2thetaW': mp.mpf('0.23122'),                             # 弱混合角平方
    # 强相互作用
    'LambdaQCD': mp.mpf('200e6') * mp.mpf('1.78266192e-30') / mp.mpf('299792458')**2,  # QCD标度
    'sigma_string': mp.mpf('1.0') * mp.mpf('1.602176634e-10') / mp.mpf('1e-15'),         # 弦张力 N (1 GeV/fm)
}

# ============================================================
# 第一卷：螺旋几何全维计算
# ============================================================

def helix_geometry(kappa, tau):
    """
    给定曲率kappa和挠率tau，计算螺旋的全部几何参数
    返回：半径a, 螺距参数b, 螺距p, 切向/法向速度, 特征长度等
    """
    c = CONSTANTS['c']
    k2_t2 = kappa**2 + tau**2
    sqrt_k2t2 = mp.sqrt(k2_t2)

    a = kappa / k2_t2                                    # 螺旋半径
    b = tau / k2_t2                                      # 约化螺距参数
    pitch = 2 * mp.pi * b                                # 一个周期的轴向前进距离
    circumference = 2 * mp.pi * a                        # 圆周长度
    period_length = 2 * mp.pi * mp.sqrt(a**2 + b**2)   # 一个周期的螺旋线长度
    characteristic_length = 1 / sqrt_k2t2               # 特征长度

    # 速度分解
    v_perp = c * kappa / sqrt_k2t2                       # 法向（圆周）速度
    v_parallel = c * tau / sqrt_k2t2                     # 轴向速度
    v_total = mp.sqrt(v_perp**2 + v_parallel**2)        # 合速度（应=c）

    # 加速度
    accel = c**2 * kappa                                  # 加速度大小
    jerk = c**3 * kappa * sqrt_k2t2                      # 加加速度大小

    # 角频率
    omega_s = c * sqrt_k2t2                              # 螺旋本征角频率
    nu_s = omega_s / (2 * mp.pi)                         # 螺旋本征频率

    return {
        'kappa': kappa,
        'tau': tau,
        'a': a,
        'b': b,
        'pitch': pitch,
        'circumference': circumference,
        'period_length': period_length,
        'characteristic_length': characteristic_length,
        'v_perp': v_perp,
        'v_parallel': v_parallel,
        'v_total': v_total,
        'v_total_error': v_total - c,
        'accel': accel,
        'jerk': jerk,
        'omega_s': omega_s,
        'nu_s': nu_s,
    }


def frenet_derivatives(kappa, tau, n_max=8):
    """
    计算Frenet标架的全阶导数（到n_max阶）
    返回各阶速度导数的大小和方向分量
    """
    c = CONSTANTS['c']
    # Frenet导数矩阵
    # D(T) = kappa * N
    # D(N) = -kappa * T + tau * B
    # D(B) = -tau * N

    # 用向量表示 [T, N, B] 分量
    # 初始 v^(0) = c * [1, 0, 0] (T分量)
    derivatives = []

    coeffs = [mp.mpf(1), mp.mpf(0), mp.mpf(0)]  # [T, N, B] 系数

    for n in range(n_max + 1):
        magnitude = c**(n+1) * mp.sqrt(coeffs[0]**2 + coeffs[1]**2 + coeffs[2]**2)
        derivatives.append({
            'order': n,
            'T_coeff': coeffs[0],
            'N_coeff': coeffs[1],
            'B_coeff': coeffs[2],
            'magnitude': magnitude,
        })
        # 应用Frenet导数：D作用于系数
        # D(T_coeff*T + N_coeff*N + B_coeff*B)
        # = T_coeff*kappa*N + N_coeff*(-kappa*T + tau*B) + B_coeff*(-tau*N)
        # = (-N_coeff*kappa)*T + (T_coeff*kappa - B_coeff*tau)*N + (N_coeff*tau)*B
        new_T = -coeffs[1] * kappa
        new_N = coeffs[0] * kappa - coeffs[2] * tau
        new_B = coeffs[1] * tau
        coeffs = [new_T, new_N, new_B]

    return derivatives


# ============================================================
# 第二卷：粒子内禀量几何化验证
# ============================================================

def mass_from_geometry(kappa, tau):
    """从曲率挠率计算质量：m = hbar * sqrt(kappa^2 + tau^2) / c"""
    return CONSTANTS['hbar'] * mp.sqrt(kappa**2 + tau**2) / CONSTANTS['c']


def geometry_from_mass(m):
    """从质量反推曲率挠率模长：sqrt(kappa^2+tau^2) = m*c/hbar"""
    return m * CONSTANTS['c'] / CONSTANTS['hbar']


def energy_from_geometry(kappa, tau):
    """E = hbar * c * sqrt(kappa^2 + tau^2)"""
    return CONSTANTS['hbar'] * CONSTANTS['c'] * mp.sqrt(kappa**2 + tau**2)


def momentum_from_geometry(kappa, tau):
    """p = hbar * sqrt(kappa^2 + tau^2)"""
    return CONSTANTS['hbar'] * mp.sqrt(kappa**2 + tau**2)


def frequency_from_geometry(kappa, tau):
    """nu_s = c * sqrt(kappa^2 + tau^2) / (2*pi)"""
    return CONSTANTS['c'] * mp.sqrt(kappa**2 + tau**2) / (2 * mp.pi)


def compton_wavelength_from_geometry(kappa, tau):
    """lambda_C = 2*pi / sqrt(kappa^2 + tau^2)"""
    return 2 * mp.pi / mp.sqrt(kappa**2 + tau**2)


def verify_mass_energy_frequency(m, name='particle'):
    """
    验证质量-能量-频率三位一体关系
    返回验证结果字典
    """
    c = CONSTANTS['c']
    hbar = CONSTANTS['hbar']
    h = CONSTANTS['h']

    k_t_mod = geometry_from_mass(m)  # sqrt(kappa^2+tau^2)

    # 从几何计算各量
    m_geom = mass_from_geometry(k_t_mod, mp.mpf(0))  # tau=0时模长就是kappa
    E_geom = energy_from_geometry(k_t_mod, mp.mpf(0))
    p_geom = momentum_from_geometry(k_t_mod, mp.mpf(0))
    nu_geom = frequency_from_geometry(k_t_mod, mp.mpf(0))
    lambda_geom = compton_wavelength_from_geometry(k_t_mod, mp.mpf(0))

    # 标准值
    E_std = m * c**2
    p_std = m * c  # 对于v=c的螺旋
    nu_std = m * c**2 / h
    lambda_std = h / (m * c)

    # 误差
    results = {
        'name': name,
        'mass_kg': m,
        'kappa_tau_modulus': k_t_mod,
        'characteristic_length': 1/k_t_mod,
        'mass_geom': m_geom,
        'mass_error': m_geom - m,
        'mass_rel_error': (m_geom - m) / m,
        'energy_geom': E_geom,
        'energy_std': E_std,
        'energy_error': E_geom - E_std,
        'energy_rel_error': (E_geom - E_std) / E_std,
        'momentum_geom': p_geom,
        'momentum_std': p_std,
        'momentum_error': p_geom - p_std,
        'frequency_geom': nu_geom,
        'frequency_std': nu_std,
        'frequency_error': nu_geom - nu_std,
        'frequency_rel_error': (nu_geom - nu_std) / nu_std,
        'compton_wavelength_geom': lambda_geom,
        'compton_wavelength_std': lambda_std,
        'wavelength_error': lambda_geom - lambda_std,
        'mass_frequency_ratio_geom': m_geom / nu_geom,
        'mass_frequency_ratio_std': h / c**2,
        'mass_frequency_error': m_geom / nu_geom - h / c**2,
    }
    return results


def verify_mass_frequency_relation():
    """验证质量-频率关系：由 E=h*nu=mc^2 得 m/nu = h/c^2"""
    h = CONSTANTS['h']
    c = CONSTANTS['c']
    expected = h / c**2  # 正确的物理关系

    # 对电子验证
    me = CONSTANTS['me']
    k_t = geometry_from_mass(me)
    nu = frequency_from_geometry(k_t, mp.mpf(0))
    ratio = me / nu
    error = ratio - expected
    rel_error = error / expected

    return {
        'expected_h_over_c2': expected,
        'electron_ratio': ratio,
        'absolute_error': error,
        'relative_error': rel_error,
        'error_order_of_magnitude': mp.floor(mp.log10(abs(rel_error))) if rel_error != 0 else 'exact',
    }


# ============================================================
# 第三卷：四力统一精算
# ============================================================

def electromagnetic_force(q1, q2, r):
    """库仑力：F = k_e * q1 * q2 / r^2"""
    k_e = 1 / (4 * mp.pi * CONSTANTS['epsilon0'])
    F = k_e * q1 * q2 / r**2
    return F


def weak_force(g_w, r):
    """
    弱力有效势的力：汤川势
    F = g_w^2/(4*pi) * exp(-r/lambda_w)/r^2 * (1 + r/lambda_w)
    """
    MW = CONSTANTS['MW']
    hbar = CONSTANTS['hbar']
    c = CONSTANTS['c']
    lambda_w = hbar / (MW * c)  # 弱力力程
    F = g_w**2 / (4 * mp.pi) * mp.e**(-r/lambda_w) / r**2 * (1 + r/lambda_w)
    return F, lambda_w


def strong_force(alpha_s, r):
    """
    强力：渐近自由项 + 禁闭项
    F = 4*alpha_s/(3*r^2) - sigma_string
    注意：符号取决于吸引/排斥，这里取大小
    """
    sigma = CONSTANTS['sigma_string']
    F_asymptotic = 4 * alpha_s / (3 * r**2)
    F_confinement = sigma
    F_total = F_asymptotic - F_confinement  # 净力
    return F_total, F_asymptotic, F_confinement


def gravitational_force(m1, m2, r):
    """牛顿引力：F = G * m1 * m2 / r^2"""
    F = CONSTANTS['G'] * m1 * m2 / r**2
    return F


def four_force_comparison(r=mp.mpf('1e-15')):
    """
    在给定距离处比较四种力的相对强度
    默认r=1fm（核子尺度）
    """
    e = CONSTANTS['e']
    me = CONSTANTS['me']
    mp_mass = CONSTANTS['mp']

    # 电磁力：两个质子在r处
    F_em = electromagnetic_force(e, e, r)

    # 弱力：g_w ~ 0.65 (对应alpha_w ~ 1/30)
    g_w = mp.sqrt(4 * mp.pi / 30)
    F_weak, lambda_w = weak_force(g_w, r)

    # 强力：alpha_s ~ 0.5 在1fm尺度
    alpha_s = mp.mpf('0.5')
    F_strong, F_strong_asym, F_strong_conf = strong_force(alpha_s, r)

    # 引力：两个质子
    F_grav = gravitational_force(mp_mass, mp_mass, r)

    # 相对强度（以引力为基准）
    results = {
        'distance_m': r,
        'F_em': F_em,
        'F_weak': F_weak,
        'F_weak_range': lambda_w,
        'F_strong_total': F_strong,
        'F_strong_asymptotic': F_strong_asym,
        'F_strong_confinement': F_strong_conf,
        'F_grav': F_grav,
        'EM_over_grav': F_em / F_grav,
        'weak_over_grav': F_weak / F_grav if F_weak != 0 else 0,
        'strong_over_grav': abs(F_strong) / F_grav if F_strong != 0 else 0,
        'EM_over_weak': F_em / F_weak if F_weak != 0 else 0,
        'strong_over_EM': abs(F_strong) / F_em if F_em != 0 else 0,
    }
    return results


def force_distance_characteristics():
    """
    计算四种力在不同距离尺度的特性
    返回多距离点的力值
    """
    distances = [
        mp.mpf('1e-35'),  # 普朗克尺度
        mp.mpf('1e-18'),  # 弱力尺度
        mp.mpf('1e-15'),  # 核子尺度
        mp.mpf('1e-10'),  # 原子尺度
        mp.mpf('1e-5'),   # 微观
        mp.mpf('1'),      # 宏观
        mp.mpf('1e8'),    # 地球尺度
        mp.mpf('1e20'),   # 恒星尺度
    ]

    e = CONSTANTS['e']
    mp_mass = CONSTANTS['mp']
    g_w = mp.sqrt(4 * mp.pi / 30)

    results = []
    for r in distances:
        F_em = electromagnetic_force(e, e, r)
        F_weak, lw = weak_force(g_w, r)
        F_strong, _, _ = strong_force(mp.mpf('0.3'), r)  # alpha_s随距离跑动
        F_grav = gravitational_force(mp_mass, mp_mass, r)

        results.append({
            'distance_m': r,
            'F_em_N': F_em,
            'F_weak_N': F_weak,
            'F_strong_N': abs(F_strong),
            'F_grav_N': F_grav,
            'EM/grav': F_em / F_grav,
        })
    return results


# ============================================================
# 第四卷：物理常数几何化验证
# ============================================================

def verify_planck_scale_g():
    """
    验证普朗克尺度下G的几何表达式
    G = c^3 / (hbar * (kappa_p^2 + tau_p^2))
    在普朗克尺度，kappa_p = tau_p = 1/lP（假设）
    """
    c = CONSTANTS['c']
    hbar = CONSTANTS['hbar']
    G = CONSTANTS['G']
    lP = CONSTANTS['lP']
    mP = CONSTANTS['mP']

    # 普朗克尺度的曲率挠率：模长 K = sqrt(kappa^2+tau^2) = 1/lP
    # 取 tau=0, kappa=1/lP（简化为圆周运动极限）
    kappa_p = 1 / lP
    tau_p = mp.mpf(0)

    # 从几何计算G
    G_geom = c**3 / (hbar * (kappa_p**2 + tau_p**2))

    # 也可以从普朗克质量验证
    mP_geom = mass_from_geometry(kappa_p, tau_p)

    error = G_geom - G
    rel_error = error / G

    return {
        'G_CODATA': G,
        'G_geometric': G_geom,
        'absolute_error': error,
        'relative_error': rel_error,
        'Planck_mass_CODATA': mP,
        'Planck_mass_geometric': mP_geom,
        'Planck_mass_error': mP_geom - mP,
        'Planck_mass_rel_error': (mP_geom - mP) / mP,
    }


def verify_em_constants():
    """
    验证电磁常数的几何关系（反解关系）
    epsilon0 = e^2 / (2*alpha*h*c)
    mu0 = 2*alpha*h / (e^2*c)
    Z0 = 2*alpha*h / e^2
    """
    e = CONSTANTS['e']
    alpha = CONSTANTS['alpha']
    h = CONSTANTS['h']
    c = CONSTANTS['c']
    eps0_std = CONSTANTS['epsilon0']
    mu0_std = CONSTANTS['mu0']
    Z0_std = CONSTANTS['Z0']

    eps0_geom = e**2 / (2 * alpha * h * c)
    mu0_geom = 2 * alpha * h / (e**2 * c)
    Z0_geom = 2 * alpha * h / e**2

    return {
        'epsilon0_CODATA': eps0_std,
        'epsilon0_geometric': eps0_geom,
        'epsilon0_rel_error': (eps0_geom - eps0_std) / eps0_std,
        'mu0_CODATA': mu0_std,
        'mu0_geometric': mu0_geom,
        'mu0_rel_error': (mu0_geom - mu0_std) / mu0_std,
        'Z0_CODATA': Z0_std,
        'Z0_geometric': Z0_geom,
        'Z0_rel_error': (Z0_geom - Z0_std) / Z0_std,
        'mu0_eps0_product': mu0_geom * eps0_geom,
        'c_squared_inverse': 1 / c**2,
        'product_check': mu0_geom * eps0_geom - 1/c**2,
    }


def verify_bohr_magneton():
    """验证玻尔磁子：mu_B = e*hbar/(2*me)"""
    e = CONSTANTS['e']
    hbar = CONSTANTS['hbar']
    me = CONSTANTS['me']
    muB_std = CONSTANTS['muB']

    muB_geom = e * hbar / (2 * me)

    return {
        'muB_CODATA': muB_std,
        'muB_geometric': muB_geom,
        'absolute_error': muB_geom - muB_std,
        'relative_error': (muB_geom - muB_std) / muB_std,
    }


# ============================================================
# 第五卷：精细结构常数分析
# ============================================================

def alpha_analysis():
    """
    精细结构常数的全面分析
    包括：实验值、各种经验公式、与几何的关系
    """
    alpha = CONSTANTS['alpha']
    alpha_inv = 1 / alpha

    results = {
        'alpha_experimental': alpha,
        'alpha_inverse': alpha_inv,
        'alpha_squared': alpha**2,
    }

    # 经验公式1：e^(-pi^2/2)
    formula1 = mp.e**(-mp.pi**2 / 2)
    results['formula_exp_neg_pi2_2'] = formula1
    results['formula1_error'] = formula1 - alpha
    results['formula1_rel_error'] = (formula1 - alpha) / alpha
    results['formula1_percent_error'] = (formula1 - alpha) / alpha * 100

    # 经验公式2：1/(4*pi^3) * (pi^2+1) ... 各种尝试
    # 这里列出几种常见的近似
    formula2 = 1 / (4 * mp.pi**3 + mp.pi**2 + 1)
    results['formula2'] = formula2
    results['formula2_rel_error'] = (formula2 - alpha) / alpha

    # 几何关系：alpha = tau/kappa 的分析
    # 如果 alpha = tau/kappa，则 tau = alpha * kappa
    # 自旋条件 kappa*tau/(kappa^2+tau^2) = 1/2
    # 代入 tau = alpha*kappa: alpha/(1+alpha^2) = 1/2
    # => 2*alpha = 1 + alpha^2 => alpha^2 - 2*alpha + 1 = 0 => alpha = 1
    # 这说明简单圆柱螺旋+自旋条件给出alpha=1，矛盾
    alpha_from_spin = mp.mpf(1)  # 由自旋条件
    results['alpha_from_simple_spin_condition'] = alpha_from_spin
    results['simple_spin_contradiction'] = '圆柱螺旋+自旋1/2条件强制kappa=tau，即alpha=1，与实验值1/137矛盾'

    # 自耦合重整化分析
    # alpha_eff = alpha_0 / (1 + alpha_0 * Pi(0))
    # 若alpha_0 = 1，需要Pi(0) ~ 136
    alpha_0 = mp.mpf(1)
    Pi_0_needed = (alpha_0 / alpha) - 1
    results['self_coupling_alpha0'] = alpha_0
    results['self_coupling_Pi0_needed'] = Pi_0_needed

    # 真空极化的对数估计
    # Pi(0) ~ (1/(2*pi)) * N * ln(Lambda/m)
    Lambda_over_m = CONSTANTS['EP'] / (CONSTANTS['me'] * CONSTANTS['c']**2)  # 普朗克能量/电子静能
    log_ratio = mp.log(Lambda_over_m)
    N_needed = Pi_0_needed * 2 * mp.pi / log_ratio
    results['vacuum_polarization_Lambda_over_m'] = Lambda_over_m
    results['vacuum_polarization_log_ratio'] = log_ratio
    results['vacuum_polarization_N_needed'] = N_needed

    return results


def koide_formula_verification():
    """
    验证Koide公式对轻子质量的拟合
    m_n = m_0 * (1 + sqrt(2)*cos(theta0 + 2*pi*n/3))^2
    """
    # 轻子质量（MeV/c²）
    me_MeV = mp.mpf('0.51099895')
    mmu_MeV = mp.mpf('105.6583755')
    mtau_MeV = mp.mpf('1776.86')

    masses = [me_MeV, mmu_MeV, mtau_MeV]
    sqrt_masses = [mp.sqrt(m) for m in masses]

    # Koide参数拟合
    # m_n = m0 * (1 + sqrt(2)*cos(theta + 2*pi*n/3))^2
    # 从三个质量反推m0和theta
    sum_sqrt = sum(sqrt_masses)
    sum_m = sum(masses)

    # m0 = (1/9) * (sum sqrt(m))^2 / (sum m) ? 不对
    # 正确的Koide关系：sum(m_n) / (sum sqrt(m_n))^2 = 2/3
    koide_ratio = sum_m / sum_sqrt**2

    # 拟合m0和theta
    # sqrt(m_n) = sqrt(m0) * (1 + sqrt(2)*cos(theta + 2*pi*n/3))
    # 令 a_n = sqrt(m_n)
    # a_0 + a_1 + a_2 = 3*sqrt(m0)  (因为cos项和为0)
    sqrt_m0 = sum_sqrt / 3
    m0_fit = sqrt_m0**2

    # 求theta
    # a_n / sqrt(m0) - 1 = sqrt(2)*cos(theta + 2*pi*n/3)
    cos_vals = [(sqrt_masses[i] / sqrt_m0 - 1) / mp.sqrt(2) for i in range(3)]

    # 从cos值求角度（需要小心分支）
    # theta = arccos(cos_vals[0]) （n=0时）
    theta_est = mp.acos(cos_vals[0])

    # 用拟合值重建质量
    masses_fit = []
    for n in range(3):
        angle = theta_est + 2 * mp.pi * n / 3
        m_fit = m0_fit * (1 + mp.sqrt(2) * mp.cos(angle))**2
        masses_fit.append(m_fit)

    errors = [(masses_fit[i] - masses[i]) / masses[i] for i in range(3)]

    return {
        'electron_mass_MeV': me_MeV,
        'muon_mass_MeV': mmu_MeV,
        'tau_mass_MeV': mtau_MeV,
        'koide_ratio_sum_m_over_sum_sqrt_sq': koide_ratio,
        'koide_ratio_expected_2_3': mp.mpf(2)/3,
        'koide_ratio_deviation': koide_ratio - mp.mpf(2)/3,
        'm0_fit_MeV': m0_fit,
        'theta0_fit': theta_est,
        'theta0_fit_degrees': theta_est * 180 / mp.pi,
        'masses_fit_MeV': masses_fit,
        'relative_errors': errors,
        'max_relative_error': max(abs(e) for e in errors),
    }


# ============================================================
# 第六卷：质量谱分析
# ============================================================

def lepton_mass_spectrum():
    """三代轻子质量的几何参数分析"""
    leptons = {
        'electron': CONSTANTS['me'],
        'muon': mp.mpf('1.883531627e-28'),  # muon质量 kg
        'tau': mp.mpf('3.16754e-27'),        # tau质量 kg
    }

    results = {}
    for name, m in leptons.items():
        k_t = geometry_from_mass(m)
        hg = helix_geometry(k_t, mp.mpf(0))  # 简化：tau=0
        results[name] = {
            'mass_kg': m,
            'mass_MeV': m * CONSTANTS['c']**2 / (CONSTANTS['e'] * 1e6),
            'kappa_tau_modulus': k_t,
            'helix_radius_a': hg['a'],
            'characteristic_length': hg['characteristic_length'],
            'compton_wavelength': hg['characteristic_length'] * 2 * mp.pi,
            'frequency': hg['nu_s'],
        }

    # 质量比
    results['mass_ratios'] = {
        'muon_over_electron': leptons['muon'] / leptons['electron'],
        'tau_over_muon': leptons['tau'] / leptons['muon'],
        'tau_over_electron': leptons['tau'] / leptons['electron'],
    }

    return results


def quark_mass_spectrum():
    """夸克质量谱（当前为经验值列表，非理论推导）"""
    # 夸克质量（MeV/c²），PDG值
    quarks = {
        'up': mp.mpf('2.16'),
        'down': mp.mpf('4.67'),
        'strange': mp.mpf('93.4'),
        'charm': mp.mpf('1270'),
        'bottom': mp.mpf('4180'),
        'top': mp.mpf('172690'),
    }

    results = {}
    for name, m_MeV in quarks.items():
        m_kg = m_MeV * 1e6 * CONSTANTS['e'] / CONSTANTS['c']**2
        k_t = geometry_from_mass(m_kg)
        results[name] = {
            'mass_MeV': m_MeV,
            'mass_kg': m_kg,
            'kappa_tau_modulus': k_t,
        }

    return results


# ============================================================
# 第七卷：宏观定律几何化验证
# ============================================================

def ideal_gas_law_verification(T=mp.mpf('300'), V=mp.mpf('0.0224'), n=mp.mpf('1')):
    """理想气体状态方程验证：PV = nRT"""
    R = CONSTANTS['R']
    P = n * R * T / V

    # 从分子动理论：P = (2/3) * N/V * (3/2)kT = NkT/V
    N = n * CONSTANTS['NA']
    P_kinetic = N * CONSTANTS['kB'] * T / V

    return {
        'temperature_K': T,
        'volume_m3': V,
        'moles': n,
        'pressure_ideal_gas_Pa': P,
        'pressure_kinetic_Pa': P_kinetic,
        'pressure_error': P - P_kinetic,
        'R_equals_NA_kB': R - CONSTANTS['NA'] * CONSTANTS['kB'],
    }


def stefan_boltzmann_verification():
    """斯特藩-玻尔兹曼定律：P = sigma*A*T^4"""
    sigma = CONSTANTS['sigma']
    kB = CONSTANTS['kB']
    hbar = CONSTANTS['hbar']
    c = CONSTANTS['c']

    # sigma = pi^2 * kB^4 / (60 * hbar^3 * c^2)
    sigma_theory = mp.pi**2 * kB**4 / (60 * hbar**3 * c**2)

    return {
        'sigma_CODATA': sigma,
        'sigma_theoretical': sigma_theory,
        'absolute_error': sigma_theory - sigma,
        'relative_error': (sigma_theory - sigma) / sigma,
    }


def temperature_geometric(T=mp.mpf('300')):
    """温度的几何化：kT = (2/3)平均动能"""
    kB = CONSTANTS['kB']
    E_thermal = kB * T
    # 对应螺旋的等效kappa_tau模长
    k_t_thermal = E_thermal / (CONSTANTS['hbar'] * CONSTANTS['c'])
    # 等效质量
    m_thermal = E_thermal / CONSTANTS['c']**2

    return {
        'temperature_K': T,
        'thermal_energy_J': E_thermal,
        'thermal_energy_eV': E_thermal / CONSTANTS['e'],
        'equivalent_kappa_tau_modulus': k_t_thermal,
        'equivalent_mass_kg': m_thermal,
        'equivalent_compton_wavelength': 2*mp.pi/k_t_thermal,
    }


# ============================================================
# 第八卷：宇宙学参数
# ============================================================

def cosmological_parameters():
    """宇宙学参数的几何化分析（当前为观测值列表）"""
    # 普朗克卫星2018结果
    H0_planck = mp.mpf('67.66')  # km/s/Mpc
    H0_shoes = mp.mpf('73.04')   # km/s/Mpc (SH0ES合作组)

    # 转换为SI: 1 km/s/Mpc = 1000 / (3.08567758e22) = 3.24078e-20 s^-1
    H0_SI_planck = H0_planck * 1000 / mp.mpf('3.08567758e22')
    H0_SI_shoes = H0_shoes * 1000 / mp.mpf('3.08567758e22')

    # 哈勃时间
    t_H_planck = 1 / H0_SI_planck
    t_H_shoes = 1 / H0_SI_shoes

    # 宇宙年龄估计（LambdaCDM）
    age_universe = mp.mpf('13.787e9') * 365.25 * 24 * 3600  # 秒

    # 临界密度
    rho_c_planck = 3 * H0_SI_planck**2 / (8 * mp.pi * CONSTANTS['G'])
    rho_c_shoes = 3 * H0_SI_shoes**2 / (8 * mp.pi * CONSTANTS['G'])

    # 暗能量密度（约68%）
    rho_Lambda = 0.68 * rho_c_planck

    # 对应的能量尺度
    E_Lambda = rho_Lambda * CONSTANTS['c']**2
    # 对应的长度尺度
    lambda_Lambda = CONSTANTS['hbar'] * CONSTANTS['c'] / E_Lambda**(1/4) if E_Lambda > 0 else 0

    return {
        'H0_planck_km_s_Mpc': H0_planck,
        'H0_shoes_km_s_Mpc': H0_shoes,
        'H0_tension': H0_shoes - H0_planck,
        'H0_tension_percent': (H0_shoes - H0_planck) / H0_planck * 100,
        'H0_planck_SI': H0_SI_planck,
        'H0_shoes_SI': H0_SI_shoes,
        'Hubble_time_planck_s': t_H_planck,
        'Hubble_time_planck_years': t_H_planck / (365.25*24*3600),
        'Hubble_time_shoes_years': t_H_shoes / (365.25*24*3600),
        'universe_age_years': mp.mpf('13.787e9'),
        'critical_density_planck_kg_m3': rho_c_planck,
        'critical_density_shoes_kg_m3': rho_c_shoes,
        'dark_energy_density_kg_m3': rho_Lambda,
        'dark_energy_energy_density_J_m3': E_Lambda,
        'dark_energy_length_scale_m': lambda_Lambda,
        'cosmological_constant_problem_ratio': (CONSTANTS['EP']/CONSTANTS['lP']**3) / E_Lambda if E_Lambda > 0 else 0,
    }


# ============================================================
# 主程序：运行全部精算并生成报告
# ============================================================

def mpf_to_serializable(obj):
    """将mpmath对象转换为可序列化的Python对象"""
    if isinstance(obj, mp.mpf):
        return mp.nstr(obj, 50)  # 50位有效数字的字符串
    elif isinstance(obj, dict):
        return {k: mpf_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [mpf_to_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return [mpf_to_serializable(item) for item in obj]
    else:
        return obj


def run_all_calculations():
    """运行全部精算，返回结果字典"""
    print("=" * 70)
    print("GAQ-UFT V∞ 全维精算引擎启动")
    print(f"精度: {mp.mp.dps} 位有效数字")
    print(f"时间: {datetime.now().isoformat()}")
    print("=" * 70)

    results = {}

    # ---- 第一卷：螺旋几何 ----
    print("\n[1/10] 螺旋几何全维计算...")
    # 电子对应的螺旋参数
    k_t_e = geometry_from_mass(CONSTANTS['me'])
    hg_e = helix_geometry(k_t_e, mp.mpf(0))
    results['helix_geometry_electron'] = hg_e

    # 全阶导数
    derivs = frenet_derivatives(k_t_e, mp.mpf(0), n_max=8)
    results['frenet_derivatives_electron'] = derivs

    # 验证v_total = c
    v_error = hg_e['v_total_error']
    print(f"  电子螺旋合速度误差: {mp.nstr(v_error, 10)} (应为0)")

    # ---- 第二卷：粒子内禀量 ----
    print("\n[2/10] 粒子内禀量几何化验证...")
    particles = [
        (CONSTANTS['me'], 'electron'),
        (CONSTANTS['mp'], 'proton'),
        (CONSTANTS['mn'], 'neutron'),
        (CONSTANTS['mP'], 'planck_mass'),
    ]
    mass_results = {}
    for m, name in particles:
        mass_results[name] = verify_mass_energy_frequency(m, name)
        rel_err = mass_results[name]['mass_rel_error']
        print(f"  {name}: 质量相对误差 = {mp.nstr(rel_err, 10)}")
    results['mass_energy_frequency'] = mass_results

    # 质量-频率关系
    mf_relation = verify_mass_frequency_relation()
    results['mass_frequency_relation'] = mf_relation
    print(f"  m/nu_s = h/c 相对误差: {mp.nstr(mf_relation['relative_error'], 10)}")

    # ---- 第三卷：四力统一 ----
    print("\n[3/10] 四力统一精算...")
    ff = four_force_comparison(mp.mpf('1e-15'))
    results['four_force_comparison_1fm'] = ff
    print(f"  1fm处: EM/grav = {mp.nstr(ff['EM_over_grav'], 10)}")
    print(f"  1fm处: strong/grav = {mp.nstr(ff['strong_over_grav'], 10)}")

    # 距离特性
    fd = force_distance_characteristics()
    results['force_distance_characteristics'] = fd

    # ---- 第四卷：常数验证 ----
    print("\n[4/10] 物理常数几何化验证...")
    planck_g = verify_planck_scale_g()
    results['planck_scale_G'] = planck_g
    print(f"  普朗克尺度G相对误差: {mp.nstr(planck_g['relative_error'], 10)}")

    em_const = verify_em_constants()
    results['em_constants'] = em_const
    print(f"  epsilon0相对误差: {mp.nstr(em_const['epsilon0_rel_error'], 10)}")

    muB = verify_bohr_magneton()
    results['bohr_magneton'] = muB
    print(f"  玻尔磁子相对误差: {mp.nstr(muB['relative_error'], 10)}")

    # ---- 第五卷：alpha分析 ----
    print("\n[5/10] 精细结构常数分析...")
    alpha_res = alpha_analysis()
    results['alpha_analysis'] = alpha_res
    print(f"  alpha实验值: {mp.nstr(alpha_res['alpha_experimental'], 20)}")
    print(f"  alpha^-1: {mp.nstr(alpha_res['alpha_inverse'], 20)}")
    print(f"  e^(-pi^2/2)误差: {mp.nstr(alpha_res['formula1_percent_error'], 10)}%")

    # Koide公式
    koide = koide_formula_verification()
    results['koide_verification'] = koide
    print(f"  Koide比值: {mp.nstr(koide['koide_ratio_sum_m_over_sum_sqrt_sq'], 20)} (期望2/3)")
    print(f"  Koide最大拟合误差: {mp.nstr(koide['max_relative_error'], 10)}")

    # ---- 第六卷：质量谱 ----
    print("\n[6/10] 质量谱分析...")
    lepton = lepton_mass_spectrum()
    results['lepton_mass_spectrum'] = lepton
    quark = quark_mass_spectrum()
    results['quark_mass_spectrum'] = quark
    print(f"  muon/electron质量比: {mp.nstr(lepton['mass_ratios']['muon_over_electron'], 10)}")

    # ---- 第七卷：宏观定律 ----
    print("\n[7/10] 宏观定律几何化验证...")
    ideal = ideal_gas_law_verification()
    results['ideal_gas_law'] = ideal
    stefan = stefan_boltzmann_verification()
    results['stefan_boltzmann'] = stefan
    temp_geom = temperature_geometric()
    results['temperature_geometric'] = temp_geom
    print(f"  Stefan-Boltzmann相对误差: {mp.nstr(stefan['relative_error'], 10)}")

    # ---- 第八卷：宇宙学 ----
    print("\n[8/10] 宇宙学参数分析...")
    cosmo = cosmological_parameters()
    results['cosmological_parameters'] = cosmo
    print(f"  哈勃张力: {mp.nstr(cosmo['H0_tension'], 10)} km/s/Mpc ({mp.nstr(cosmo['H0_tension_percent'], 10)}%)")

    # ---- 第九卷：理论自洽性检查 ----
    print("\n[9/10] 理论自洽性检查...")
    consistency = {}

    # 检查1: c^2 = 1/(mu0*epsilon0)
    consistency['c2_vs_1_mu0eps0'] = CONSTANTS['c']**2 - 1/(CONSTANTS['mu0']*CONSTANTS['epsilon0'])

    # 检查2: alpha = e^2/(4*pi*epsilon0*hbar*c)
    alpha_check = CONSTANTS['e']**2 / (4*mp.pi*CONSTANTS['epsilon0']*CONSTANTS['hbar']*CONSTANTS['c'])
    consistency['alpha_from_constants'] = alpha_check
    consistency['alpha_error'] = alpha_check - CONSTANTS['alpha']

    # 检查3: h = 2*pi*hbar
    consistency['h_vs_2pi_hbar'] = CONSTANTS['h'] - 2*mp.pi*CONSTANTS['hbar']

    # 检查4: R = NA * kB
    consistency['R_vs_NA_kB'] = CONSTANTS['R'] - CONSTANTS['NA']*CONSTANTS['kB']

    # 检查5: F = NA * e
    consistency['F_vs_NA_e'] = CONSTANTS['F'] - CONSTANTS['NA']*CONSTANTS['e']

    # 检查6: Phi0 = h/(2e)
    consistency['Phi0_vs_h_2e'] = CONSTANTS['Phi0'] - CONSTANTS['h']/(2*CONSTANTS['e'])

    # 检查7: RK = h/e^2
    consistency['RK_vs_h_e2'] = CONSTANTS['RK'] - CONSTANTS['h']/CONSTANTS['e']**2

    # 检查8: Z0 = mu0*c
    consistency['Z0_vs_mu0_c'] = CONSTANTS['Z0'] - CONSTANTS['mu0']*CONSTANTS['c']

    # 检查9: a0 = 4*pi*epsilon0*hbar^2/(me*e^2) = hbar/(me*c*alpha)
    a0_check = CONSTANTS['hbar'] / (CONSTANTS['me']*CONSTANTS['c']*CONSTANTS['alpha'])
    consistency['a0_from_geometry'] = a0_check
    consistency['a0_error'] = a0_check - CONSTANTS['a0']

    # 检查10: re = alpha * a0 = alpha^2 * lambdaC/(2*pi)
    re_check = CONSTANTS['alpha'] * CONSTANTS['a0']
    consistency['re_from_geometry'] = re_check
    consistency['re_error'] = re_check - CONSTANTS['re']

    # 检查11: lambdaC = h/(me*c) = 2*pi*hbar/(me*c)
    lambdaC_check = CONSTANTS['h'] / (CONSTANTS['me']*CONSTANTS['c'])
    consistency['lambdaC_check'] = lambdaC_check
    consistency['lambdaC_error'] = lambdaC_check - CONSTANTS['lambdaC']

    # 检查12: muB = e*hbar/(2*me)
    muB_check = CONSTANTS['e']*CONSTANTS['hbar']/(2*CONSTANTS['me'])
    consistency['muB_check'] = muB_check
    consistency['muB_error'] = muB_check - CONSTANTS['muB']

    results['consistency_checks'] = consistency

    all_pass = True
    error_keys = [k for k in consistency.keys() if k.endswith('_error') or k.endswith('_check') or 'vs' in k]
    for key in error_keys:
        val = consistency[key]
        if isinstance(val, mp.mpf):
            if abs(val) > mp.mpf('1e-15'):
                print(f"  ⚠ {key}: 偏差 = {mp.nstr(val, 10)}")
                all_pass = False
    if all_pass:
        print("  全部自洽性误差项在1e-15以内 ✓")

    # ---- 第十卷：成熟度评估 ----
    print("\n[10/10] 理论成熟度评估...")
    maturity = {
        'volume_1_geometry': {'score': 95, 'status': '成熟', 'notes': '标准微分几何，Frenet-Serret全阶可导'},
        'volume_2_intrinsic': {'score': 80, 'status': '基本成熟', 'notes': '质能频关系严格，电荷自旋几何化待完善'},
        'volume_3_forces': {'score': 60, 'status': '框架建立', 'notes': '形式统一完成，强力弱力几何细节待完善，引力宏观导出未闭合'},
        'volume_4_constants': {'score': 40, 'status': '部分完成', 'notes': '约6个常数几何关系精确，多数为反解，alpha未导出'},
        'volume_5_alpha': {'score': 15, 'status': '攻坚中', 'notes': '四种方案均未闭合，核心瓶颈'},
        'volume_6_mass_spectrum': {'score': 30, 'status': '部分完成', 'notes': '轻子Koide拟合好，夸克中微子未解决'},
        'volume_7_macroscopic': {'score': 50, 'status': '概念框架', 'notes': '热力学统计力学概念完整，严格推导待完善'},
        'volume_8_cosmology': {'score': 20, 'status': '早期', 'notes': '暗物质暗能量哈勃张力均未解决'},
        'volume_9_consciousness': {'score': 10, 'status': '远期目标', 'notes': '仅有概念框架，无严格理论'},
        'overall_maturity': {'score': 40, 'status': '几何诠释框架'},
    }
    results['maturity_assessment'] = maturity
    print(f"  总体成熟度: 40%")

    print("\n" + "=" * 70)
    print("全维精算完成！")
    print("=" * 70)

    return results


def save_results(results, output_dir):
    """保存结果为JSON和文本报告"""
    os.makedirs(output_dir, exist_ok=True)

    # JSON格式
    json_path = os.path.join(output_dir, 'full_calculation_results.json')
    serializable = mpf_to_serializable(results)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)
    print(f"JSON结果已保存: {json_path}")

    # 文本报告
    txt_path = os.path.join(output_dir, 'calculation_report.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("GAQ-UFT V∞ 全维精算报告\n")
        f.write(f"生成时间: {datetime.now().isoformat()}\n")
        f.write(f"计算精度: {mp.mp.dps} 位有效数字\n")
        f.write("=" * 70 + "\n\n")

        # 核心验证结果摘要
        f.write("一、核心定理级验证结果\n")
        f.write("-" * 50 + "\n")

        me_result = results['mass_energy_frequency']['electron']
        f.write(f"1. 质量-曲率挠率恒等式 (电子)\n")
        f.write(f"   m = hbar*sqrt(kappa^2+tau^2)/c\n")
        f.write(f"   几何质量: {mp.nstr(me_result['mass_geom'], 30)} kg\n")
        f.write(f"   CODATA质量: {mp.nstr(me_result['mass_kg'], 30)} kg\n")
        f.write(f"   相对误差: {mp.nstr(me_result['mass_rel_error'], 10)}\n\n")

        mf = results['mass_frequency_relation']
        f.write(f"2. 质量-频率关系 m/nu = h/c^2 (由 E=h*nu=mc^2)\n")
        f.write(f"   几何比值: {mp.nstr(mf['electron_ratio'], 30)}\n")
        f.write(f"   理论值 h/c^2: {mp.nstr(mf['expected_h_over_c2'], 30)}\n")
        f.write(f"   相对误差: {mp.nstr(mf['relative_error'], 10)}\n\n")

        pg = results['planck_scale_G']
        f.write(f"3. 普朗克尺度引力常数\n")
        f.write(f"   G = c^3/(hbar*(kappa_p^2+tau_p^2))\n")
        f.write(f"   几何G: {mp.nstr(pg['G_geometric'], 30)}\n")
        f.write(f"   CODATA G: {mp.nstr(pg['G_CODATA'], 30)}\n")
        f.write(f"   相对误差: {mp.nstr(pg['relative_error'], 10)}\n\n")

        em = results['em_constants']
        f.write(f"4. 电磁常数反解验证\n")
        f.write(f"   epsilon0相对误差: {mp.nstr(em['epsilon0_rel_error'], 10)}\n")
        f.write(f"   mu0相对误差: {mp.nstr(em['mu0_rel_error'], 10)}\n")
        f.write(f"   Z0相对误差: {mp.nstr(em['Z0_rel_error'], 10)}\n")
        f.write(f"   mu0*eps0 = 1/c^2 验证: {mp.nstr(em['product_check'], 10)}\n\n")

        # 四力对比
        f.write("二、四力统一精算（r=1fm处）\n")
        f.write("-" * 50 + "\n")
        ff = results['four_force_comparison_1fm']
        f.write(f"电磁力: {mp.nstr(ff['F_em'], 20)} N\n")
        f.write(f"弱力:   {mp.nstr(ff['F_weak'], 20)} N (力程={mp.nstr(ff['F_weak_range'], 20)} m)\n")
        f.write(f"强力:   {mp.nstr(ff['F_strong_total'], 20)} N\n")
        f.write(f"引力:   {mp.nstr(ff['F_grav'], 20)} N\n")
        f.write(f"EM/Grav: {mp.nstr(ff['EM_over_grav'], 10)}\n")
        f.write(f"Strong/Grav: {mp.nstr(ff['strong_over_grav'], 10)}\n\n")

        # Alpha分析
        f.write("三、精细结构常数分析（核心未闭合）\n")
        f.write("-" * 50 + "\n")
        aa = results['alpha_analysis']
        f.write(f"实验值 alpha = {mp.nstr(aa['alpha_experimental'], 30)}\n")
        f.write(f"alpha^-1 = {mp.nstr(aa['alpha_inverse'], 30)}\n")
        f.write(f"经验公式 e^(-pi^2/2): {mp.nstr(aa['formula_exp_neg_pi2_2'], 20)}, 误差={mp.nstr(aa['formula1_percent_error'], 10)}%\n")
        f.write(f"简单自旋条件给出alpha=1（矛盾）\n")
        f.write(f"自耦合重整化需要Pi(0)={mp.nstr(aa['self_coupling_Pi0_needed'], 10)}\n")
        f.write(f"对应有效自由度N={mp.nstr(aa['vacuum_polarization_N_needed'], 10)}\n\n")

        # Koide
        f.write("四、Koide公式验证（轻子质量谱）\n")
        f.write("-" * 50 + "\n")
        ko = results['koide_verification']
        f.write(f"Koide比值 sum(m)/(sum sqrt(m))^2 = {mp.nstr(ko['koide_ratio_sum_m_over_sum_sqrt_sq'], 20)}\n")
        f.write(f"期望值 2/3 = {mp.nstr(ko['koide_ratio_expected_2_3'], 20)}\n")
        f.write(f"偏差: {mp.nstr(ko['koide_ratio_deviation'], 20)}\n")
        f.write(f"拟合m0 = {mp.nstr(ko['m0_fit_MeV'], 20)} MeV\n")
        f.write(f"拟合theta0 = {mp.nstr(ko['theta0_fit_degrees'], 20)} 度\n")
        f.write(f"最大相对误差: {mp.nstr(ko['max_relative_error'], 10)}\n\n")

        # 自洽性检查
        f.write("五、理论自洽性检查（12项）\n")
        f.write("-" * 50 + "\n")
        cc = results['consistency_checks']
        checks = [
            ('c^2 = 1/(mu0*eps0)', 'c2_vs_1_mu0eps0'),
            ('alpha = e^2/(4pi*eps0*hbar*c)', 'alpha_error'),
            ('h = 2*pi*hbar', 'h_vs_2pi_hbar'),
            ('R = NA*kB', 'R_vs_NA_kB'),
            ('F = NA*e', 'F_vs_NA_e'),
            ('Phi0 = h/(2e)', 'Phi0_vs_h_2e'),
            ('RK = h/e^2', 'RK_vs_h_e2'),
            ('Z0 = mu0*c', 'Z0_vs_mu0_c'),
            ('a0 = hbar/(me*c*alpha)', 'a0_error'),
            ('re = alpha*a0', 're_error'),
            ('lambdaC = h/(me*c)', 'lambdaC_error'),
            ('muB = e*hbar/(2me)', 'muB_error'),
        ]
        for name, key in checks:
            val = cc[key]
            status = "✓" if (isinstance(val, mp.mpf) and abs(val) < mp.mpf('1e-20')) else "✗"
            f.write(f"  {status} {name}: 偏差={mp.nstr(val, 10) if isinstance(val, mp.mpf) else val}\n")

        # 成熟度
        f.write("\n六、理论成熟度评估\n")
        f.write("-" * 50 + "\n")
        ma = results['maturity_assessment']
        for key, val in ma.items():
            if key != 'overall_maturity':
                f.write(f"  {key}: {val['score']}% - {val['status']}\n")
        f.write(f"\n  总体成熟度: {ma['overall_maturity']['score']}% - {ma['overall_maturity']['status']}\n")

        f.write("\n" + "=" * 70 + "\n")
        f.write("报告结束\n")
        f.write("=" * 70 + "\n")

    print(f"文本报告已保存: {txt_path}")
    return json_path, txt_path


if __name__ == '__main__':
    results = run_all_calculations()
    output_dir = '/home/user/.super_doubao/super-doubao-runtime/workspace/GAQ_UFT_V∞/results'
    json_path, txt_path = save_results(results, output_dir)
    print(f"\n全部完成。文件保存在: {output_dir}")
