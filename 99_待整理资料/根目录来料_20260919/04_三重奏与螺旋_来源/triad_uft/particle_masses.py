# -*- coding: utf-8 -*-
"""
particle_masses.py — 粒子物理质量谱与混合角模块
====================================================
三代费米子质量谱螺旋几何化、质量比与螺旋半径比、
CKM/PMNS混合角螺旋重叠模型、中微子质量与跷跷板机制。
"""
import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

# 物理常数
from .constants import C, HBAR

MEV = 1.602176634e-13  # 1 MeV in J
GEV = 1.602176634e-10  # 1 GeV in J

# 三代费米子质量（MeV/c²）
MASSES = {
    "e": 0.511, "mu": 105.658, "tau": 1776.86,
    "u": 2.2, "d": 4.7, "s": 95.0,
    "c": 1270.0, "b": 4180.0, "t": 173100.0,
}

# CKM矩阵元（绝对值，PDG）
CKM = {
    "V_ud": 0.97373, "V_us": 0.2243, "V_ub": 0.00382,
    "V_cd": 0.221, "V_cs": 0.9728, "V_cb": 0.0408,
    "V_td": 0.0086, "V_ts": 0.0411, "V_tb": 0.99914,
}

# PMNS矩阵元（绝对值，PDG）
PMNS = {
    "U_e1": 0.82, "U_e2": 0.55, "U_e3": 0.15,
    "U_mu1": 0.37, "U_mu2": 0.60, "U_mu3": 0.71,
    "U_tau1": 0.44, "U_tau2": 0.58, "U_tau3": 0.69,
}


@dataclass
class ParticleHelixParams:
    """粒子螺旋参数"""
    name: str
    mass: float       # 质量（MeV/c²）
    radius: float     # 螺旋半径（m）
    frequency: float  # 螺旋频率（Hz）
    compton_wavelength: float  # 康普顿波长（m）


def mass_to_helix_radius(mass_mev: float) -> float:
    """
    质量→螺旋半径（m = ħ/(cR) → R = ħ/(mc)）。

    参数:
        mass_mev: 质量（MeV/c²）

    返回:
        螺旋半径（m）
    """
    mass_kg = mass_mev * MEV / C**2
    radius = HBAR / (mass_kg * C)
    return radius


def helix_radius_to_mass(radius: float) -> float:
    """
    螺旋半径→质量（m = ħ/(cR)）。

    参数:
        radius: 螺旋半径（m）

    返回:
        质量（MeV/c²）
    """
    mass_kg = HBAR / (radius * C)
    return mass_kg * C**2 / MEV


def particle_helix_params(name: str) -> ParticleHelixParams:
    """
    获取粒子的螺旋参数。

    参数:
        name: 粒子名称（e, mu, tau, u, d, s, c, b, t）

    返回:
        ParticleHelixParams对象
    """
    if name not in MASSES:
        raise ValueError(f"Unknown particle: {name}")

    mass = MASSES[name]
    radius = mass_to_helix_radius(mass)
    frequency = C / (2 * np.pi * radius)  # ω = c/R, f = ω/(2π)
    compton = 2 * np.pi * radius  # 康普顿波长 = 螺旋周长

    return ParticleHelixParams(
        name=name, mass=mass, radius=radius,
        frequency=frequency, compton_wavelength=compton
    )


def mass_ratio_verification() -> Dict:
    """
    验证质量比=螺旋半径反比（恒等式）。

    m1/m2 = R2/R1（因为m = ħ/(cR)）
    """
    particles = ["e", "mu", "tau", "u", "d", "s", "c", "b", "t"]
    results = {}

    for i, p1 in enumerate(particles):
        for p2 in particles[i+1:]:
            m_ratio = MASSES[p1] / MASSES[p2]
            r1 = mass_to_helix_radius(MASSES[p1])
            r2 = mass_to_helix_radius(MASSES[p2])
            r_ratio = r2 / r1
            error = abs(m_ratio - r_ratio) / m_ratio * 100
            results[f"{p1}/{p2}"] = {
                "mass_ratio": m_ratio,
                "radius_inverse_ratio": r_ratio,
                "error_percent": error,
            }

    return results


def ckm_mixing_angles() -> Dict:
    """
    从CKM矩阵元计算混合角。

    返回:
        混合角字典（度）
    """
    theta12 = np.arcsin(CKM["V_us"]) * 180 / np.pi
    theta23 = np.arcsin(CKM["V_cb"]) * 180 / np.pi
    theta13 = np.arcsin(CKM["V_ub"]) * 180 / np.pi

    return {
        "theta12_deg": theta12,
        "theta23_deg": theta23,
        "theta13_deg": theta13,
        "hierarchy": "theta12 > theta23 >> theta13",
    }


def pmns_mixing_angles() -> Dict:
    """
    从PMNS矩阵元计算混合角。

    返回:
        混合角字典（度）
    """
    theta12 = np.arcsin(PMNS["U_e2"]) * 180 / np.pi
    theta23 = np.arcsin(PMNS["U_mu3"]) * 180 / np.pi
    theta13 = np.arcsin(PMNS["U_e3"]) * 180 / np.pi

    return {
        "theta12_deg": theta12,
        "theta23_deg": theta23,
        "theta13_deg": theta13,
        "maximal_mixing_theta23": abs(theta23 - 45) < 5,
    }


def ckm_pmns_comparison() -> Dict:
    """
    CKM与PMNS混合角对比。
    """
    ckm = ckm_mixing_angles()
    pmns = pmns_mixing_angles()

    return {
        "CKM": ckm,
        "PMNS": pmns,
        "ratio_theta12": pmns["theta12_deg"] / ckm["theta12_deg"],
        "ratio_theta23": pmns["theta23_deg"] / ckm["theta23_deg"],
        "ratio_theta13": pmns["theta13_deg"] / ckm["theta13_deg"],
        "interpretation": "夸克混合小（层级结构），轻子混合大（接近最大混合）",
    }


def neutrino_mass_seesaw(m_D: float = 100.0, M_R: float = 1e14) -> float:
    """
    中微子质量跷跷板机制。

    m_ν = m_D² / M_R

    参数:
        m_D: Dirac质量（GeV/c²），默认100
        M_R: 右手中微子质量（GeV/c²），默认10^14

    返回:
        中微子质量（eV/c²）
    """
    m_nu_gev = m_D**2 / M_R
    return m_nu_gev * 1e9  # 转换为eV


def neutrino_oscillation_params() -> Dict:
    """
    中微子振荡实验参数。
    """
    return {
        "Delta_m21_squared": 7.53e-5,  # eV²
        "Delta_m32_squared": 2.453e-3,  # eV²（正常序）
        "sin2_theta12": 0.307,
        "sin2_theta23": 0.545,
        "sin2_theta13": 0.02219,
        "delta_CP": 1.36,  # rad
    }


def yukawa_coupling_from_radius(radius: float) -> float:
    """
    从螺旋半径计算Yukawa耦合常数。

    y = m/v = ħ/(cRv)（v=246 GeV为Higgs真空期望值）

    参数:
        radius: 螺旋半径（m）

    返回:
        Yukawa耦合常数
    """
    v = 246.2196  # GeV
    mass_gev = helix_radius_to_mass(radius) / 1000  # MeV→GeV
    return mass_gev / v


def mass_hierarchy_explanation() -> Dict:
    """
    质量层级的螺旋几何化解释。
    """
    return {
        "electron": {"mass": "0.511 MeV", "radius": "3.86e-13 m", "yukawa": "2.9e-6"},
        "muon": {"mass": "105.7 MeV", "radius": "1.87e-15 m", "yukawa": "6.1e-4"},
        "tau": {"mass": "1.777 GeV", "radius": "1.11e-16 m", "yukawa": "1.0e-2"},
        "top": {"mass": "173 GeV", "radius": "1.14e-18 m", "yukawa": "~1.0"},
        "interpretation": "质量越大，螺旋半径越小，Yukawa耦合越强",
        "hierarchy_problem": "为何Yukawa耦合跨越6个数量级？（味问题）",
    }
