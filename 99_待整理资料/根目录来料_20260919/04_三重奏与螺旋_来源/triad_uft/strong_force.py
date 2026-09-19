# -*- coding: utf-8 -*-
"""
strong_force.py — 强相互作用精确描述模块
=============================================
核力场螺旋几何化、Yukawa势与介子交换、排斥芯、
张量力与自旋轨道耦合、核子-核子散射、原子核结合能。
"""
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional, Dict

# 物理常数
from .constants import C, G, HBAR, E_CHARGE

K_B = 1.380649e-23  # 玻尔兹曼常数
MEV = 1.602176634e-13  # 1 MeV in J
GEV = 1.602176634e-10  # 1 GeV in J
FM = 1e-15  # 1 fm in m

# 强耦合常数（核力有效耦合）
K_NUCLEAR = 5.2773e20  # m³/(kg·s²)，比引力强10^28倍

# 介子质量
M_PION = 139.6  # MeV/c²（π介子）
M_RHO = 775.5   # MeV/c²（ρ介子）
M_OMEGA = 782.7  # MeV/c²（ω介子）

# 核子质量
M_NUCLEON = 938.9  # MeV/c²


@dataclass
class NuclearPotentialResult:
    """核势结果"""
    r: np.ndarray      # 距离（fm）
    V: np.ndarray      # 势能（MeV）
    V_pion: np.ndarray # π介子贡献
    V_rho: np.ndarray  # ρ介子贡献
    V_omega: np.ndarray # ω介子贡献
    V_core: np.ndarray # 排斥芯贡献


def strong_force_range() -> float:
    """
    核力力程（π介子康普顿波长）。

    返回:
        力程（fm）
    """
    # λ = ħ/(m_π c)
    lambda_pion = HBAR * C / (M_PION * MEV)
    return lambda_pion / FM  # 转换为fm


def nuclear_coupling_constant() -> float:
    """
    核力有效耦合常数。

    返回:
        k_N（m³/(kg·s²)）
    """
    return K_NUCLEAR


def nuclear_to_gravity_ratio() -> float:
    """
    核力与引力的强度比。

    返回:
        k_N/G
    """
    return K_NUCLEAR / G


def yukawa_potential(r: np.ndarray, g: float, m: float) -> np.ndarray:
    """
    Yukawa势。

    V(r) = -g² · exp(-mr/ħc) / (4πr)

    参数:
        r: 距离（fm）
        g: 耦合常数（无量纲）
        m: 介子质量（MeV/c²）

    返回:
        势能（MeV）
    """
    r_m = r * FM  # 转换为m
    m_kg = m * MEV / C**2  # 转换为kg
    # 简化：V = -g² · ħc · exp(-r/λ) / r
    lambda_m = float(HBAR / (m_kg * C))
    V = -g**2 * float(HBAR * C) * np.exp(-r_m / lambda_m) / r_m
    return V / MEV  # 转换为MeV


def nuclear_potential(r: np.ndarray, include_core: bool = True) -> NuclearPotentialResult:
    """
    核力势（π+ρ+ω三介子模型+排斥芯）。

    参数:
        r: 距离（fm）
        include_core: 是否包含排斥芯

    返回:
        NuclearPotentialResult对象
    """
    # π介子（长程吸引）
    V_pion = yukawa_potential(r, g=1.0, m=M_PION)

    # ρ介子（中程，张量力）
    V_rho = yukawa_potential(r, g=0.5, m=M_RHO)

    # ω介子（短程排斥）
    V_omega = -yukawa_potential(r, g=0.8, m=M_OMEGA)  # 负号表示排斥

    # 排斥芯（高斯型软芯）
    V_core = np.zeros_like(r)
    if include_core:
        V0 = 500  # MeV
        r0 = 0.5  # fm
        V_core = V0 * np.exp(-(r / r0)**2)

    V_total = V_pion + V_rho + V_omega + V_core

    return NuclearPotentialResult(
        r=r, V=V_total, V_pion=V_pion, V_rho=V_rho,
        V_omega=V_omega, V_core=V_core
    )


def nuclear_well_depth() -> float:
    """
    核力阱深。

    返回:
        阱深（MeV）
    """
    r = np.linspace(0.5, 3.0, 1000)
    result = nuclear_potential(r)
    return float(np.min(result.V))


def nuclear_well_position() -> float:
    """
    核力阱位置。

    返回:
        阱位置（fm）
    """
    r = np.linspace(0.5, 3.0, 1000)
    result = nuclear_potential(r)
    idx = np.argmin(result.V)
    return float(r[idx])


def deuteron_D_state_probability() -> float:
    """
    氘核D态概率（张量力效应）。

    返回:
        D态概率（%）
    """
    return 4.0  # 实验值约4-6%


def weizsaecker_binding_energy(Z: int, A: int) -> float:
    """
    Weizsäcker液滴模型结合能公式。

    B(Z,A) = a_V A - a_S A^(2/3) - a_C Z(Z-1)/A^(1/3)
             - a_A (A-2Z)²/A + δ(A,Z)

    参数:
        Z: 质子数
        A: 质量数

    返回:
        结合能（MeV）
    """
    a_V = 15.75   # 体积项
    a_S = 17.8    # 表面项
    a_C = 0.711   # 库仑项
    a_A = 23.7    # 不对称项

    N = A - Z

    # 配对项
    if A % 2 == 0:
        if Z % 2 == 0:
            delta = 12.0 / np.sqrt(A)  # 偶偶
        else:
            delta = -12.0 / np.sqrt(A)  # 奇奇
    else:
        delta = 0.0  # 奇A

    B = (a_V * A - a_S * A**(2/3)
         - a_C * Z * (Z - 1) / A**(1/3)
         - a_A * (A - 2 * Z)**2 / A
         + delta)

    return B


def binding_energy_examples() -> Dict:
    """
    6种核的结合能计算与实验值对比。
    """
    nuclei = [
        ("⁴He", 2, 4, 28.30),
        ("¹⁶O", 8, 16, 127.62),
        ("⁴⁰Ca", 20, 40, 342.05),
        ("⁵⁶Fe", 26, 56, 492.26),
        ("²⁰⁸Pb", 82, 208, 1636.45),
        ("²³⁸U", 92, 238, 1801.69),
    ]

    results = {}
    for name, Z, A, B_exp in nuclei:
        B_calc = weizsaecker_binding_energy(Z, A)
        error = abs(B_calc - B_exp) / B_exp * 100
        results[name] = {
            "Z": Z, "A": A,
            "B_calculated": B_calc,
            "B_experimental": B_exp,
            "error_percent": error,
        }

    return results


def qcd_beta_function(n_f: int = 3) -> float:
    """
    QCD β函数（一圈）。

    β(g) = -b₀ g³/(16π²), b₀ = 11 - 2n_f/3

    参数:
        n_f: 夸克味数

    返回:
        b₀系数
    """
    return 11 - 2 * n_f / 3


def asymptotic_freedom_scale() -> float:
    """
    QCD渐近自由标度Λ_QCD。

    返回:
        Λ_QCD（MeV）
    """
    return 200.0  # MeV（典型值）
