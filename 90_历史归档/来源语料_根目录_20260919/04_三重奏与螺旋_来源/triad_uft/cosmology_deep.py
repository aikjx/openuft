# -*- coding: utf-8 -*-
"""
cosmology_deep.py — 宇宙学深入模块
=====================================
暗能量视界截断、暴胀螺旋几何化、宇宙演化五阶段、
CMB声学峰、暗物质候选、宇宙学参数、宇宙学疑难。
"""
import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

# 物理常数
from .constants import C, G, HBAR, PLANCK_LENGTH as L_P, PLANCK_MASS as M_P

K_B = 1.380649e-23  # 玻尔兹曼常数

# 宇宙学参数（Planck 2018）
H0 = 67.66  # km/s/Mpc
H0_SI = H0 * 1000 / (3.0857e22)  # 1/s
OMEGA_M = 0.3111
OMEGA_LAMBDA = 0.6889
OMEGA_B = 0.0486
OMEGA_CDM = 0.2625
OMEGA_R = 9.2e-5
T_CMB = 2.7255  # K
AGE_UNIVERSE = 13.800  # Gyr


@dataclass
class CosmicEvolution:
    """宇宙演化结果"""
    age_gyr: float         # 宇宙年龄（Gyr）
    hubble_time_gyr: float  # 哈勃时间（Gyr）
    horizon_mpc: float      # 哈勃视界（Mpc）
    critical_density: float  # 临界密度（kg/m³）


def cosmological_constant_problem() -> Dict:
    """
    宇宙学常数问题与视界截断解决方案。
    """
    # 观测值
    rho_lambda = OMEGA_LAMBDA * 3 * H0_SI**2 * C**2 / (8 * np.pi * G)

    # 理论值（Planck能量密度）
    rho_vac = C**5 / (HBAR * G**2)

    # 比值
    ratio = rho_vac / rho_lambda

    # 视界截断
    R_H = C / H0_SI  # 视界半径
    k_max = 1 / R_H  # 视界波数
    rho_vac_truncated = k_max**4 * HBAR * C  # 截断后的真空能（量级）

    return {
        "observed_rho_lambda": float(rho_lambda),
        "theoretical_rho_vac": float(rho_vac),
        "ratio": float(ratio),
        "ratio_log10": float(np.log10(float(ratio))),
        "horizon_radius": float(R_H),
        "horizon_wavenumber": float(k_max),
        "truncated_rho_vac": float(rho_vac_truncated),
        "solution": "视界截断：真空能积分上限=宇宙视界波数（不是Planck波数）",
        "natural_suppression": "自然压制~122个数量级",
        "equation_of_state": "w = -1（宇宙学常数）",
    }


def inflation_helix() -> Dict:
    """
    暴胀的螺旋几何化。
    """
    return {
        "inflaton": "宇宙尺度的螺旋场",
        "slow_roll": "螺旋半径缓慢变化",
        "end_of_inflation": "螺旋半径达到临界值，开始振荡",
        "reheating": "螺旋振荡衰变为标准模型粒子",
        "primordial_fluctuations": "螺旋的量子涨落被拉伸到宇宙尺度",
        "power_spectrum": "P_ζ(k) = H²/(8π²εM_P²)",
        "spectral_index": "n_s = 1 - 6ε + 2η",
        "tensor_scalar_ratio": "r = 16ε",
        "planck_2018": {
            "n_s": 0.9649,
            "r_upper": 0.06,
            "slow_roll_satisfied": True,
        },
    }


def cosmic_age_calculation() -> float:
    """
    计算宇宙年龄（Friedmann方程数值积分）。

    返回:
        宇宙年龄（Gyr）
    """
    a = np.logspace(-20, 0, 100000)
    H_a = H0_SI * np.sqrt(OMEGA_M * a**-3 + OMEGA_R * a**-4 + OMEGA_LAMBDA)
    integrand = 1.0 / (a * H_a)
    age_seconds = np.trapezoid(integrand, a)
    age_gyr = age_seconds / (365.25 * 24 * 3600 * 1e9)
    return age_gyr


def cosmic_evolution_summary() -> CosmicEvolution:
    """
    宇宙演化汇总。
    """
    age = cosmic_age_calculation()
    t_H = 1 / H0_SI / (365.25 * 24 * 3600 * 1e9)
    R_H = C / H0_SI / (3.0857e22)  # Mpc
    rho_crit = 3 * H0_SI**2 * C**2 / (8 * np.pi * G)

    return CosmicEvolution(
        age_gyr=age,
        hubble_time_gyr=t_H,
        horizon_mpc=R_H,
        critical_density=rho_crit,
    )


def cosmic_stages() -> Dict:
    """
    宇宙演化五阶段。
    """
    return {
        "inflation": {
            "time": "10^-36 - 10^-32 s",
            "scale_factor": "a ~ e^{Ht}（指数膨胀）",
            "key_events": ["指数膨胀", "解决视界/平坦性/磁单极问题"],
        },
        "reheating": {
            "time": "10^-32 - 10^-12 s",
            "scale_factor": "过渡",
            "key_events": ["暴胀子衰变", "宇宙重新加热"],
        },
        "radiation_dominated": {
            "time": "10^-12 s - 50000 yr",
            "scale_factor": "a ~ t^{1/2}",
            "key_events": ["电弱相变", "QCD相变", "中微子退耦", "原初核合成"],
        },
        "matter_dominated": {
            "time": "50000 yr - 90亿 yr",
            "scale_factor": "a ~ t^{2/3}",
            "key_events": ["复合", "再电离", "第一代恒星", "星系形成"],
        },
        "dark_energy_dominated": {
            "time": "90亿 yr - 现在",
            "scale_factor": "a ~ e^{Ht}（指数膨胀）",
            "key_events": ["宇宙加速膨胀", "结构形成停止"],
        },
    }


def cmb_acoustic_peaks() -> Dict:
    """
    CMB声学峰。
    """
    return {
        "first_peak": {"l": 220, "observed": 220.8, "interpretation": "宇宙学尺度"},
        "second_peak": {"l": 546, "observed": 537.5, "interpretation": "重子密度"},
        "third_peak": {"l": 820, "observed": 815.0, "interpretation": "暗物质密度"},
        "formula": "l_n = nπ r_s / D_A（r_s=声视界, D_A=角直径距离）",
        "helix_interpretation": "声学峰 = 螺旋的共振模式（声波振荡）",
    }


def cmb_polarization() -> Dict:
    """
    CMB偏振。
    """
    return {
        "E_mode": {
            "origin": "密度扰动产生（标量模式）",
            "measured": True,
            "helix_interpretation": "螺旋的电场偏振（标量扰动）",
        },
        "B_mode": {
            "origin": "引力波产生（张量模式）或引力透镜",
            "measured": False,
            "helix_interpretation": "螺旋的磁场偏振（张量扰动/引力波）",
            "primordial_gravitational_waves": "暴胀期间的螺旋张量涨落",
            "r_parameter": "r = 16ε（张量/标量比）",
        },
    }


def dark_matter_candidates() -> Dict:
    """
    暗物质候选者的螺旋几何化。
    """
    return {
        "WIMP": {
            "mass": "100 GeV - 1 TeV",
            "interaction": "弱相互作用",
            "helix_radius": "~10^-18 m",
            "abundance": "热遗迹丰度自然匹配观测（WIMP奇迹）",
            "detection": "直接/间接探测尚未发现",
        },
        "axion": {
            "mass": "10^-6 - 10^-3 eV",
            "interaction": "极弱",
            "helix_radius": "~10^-3 m",
            "origin": "Peccei-Quinn对称性破缺",
            "advantage": "解决强CP问题",
            "detection": "ADMX实验正在搜索",
        },
        "primordial_black_hole": {
            "mass": "小行星 - 太阳质量",
            "helix_radius": "~10^3 m（太阳质量）",
            "origin": "暴胀期间密度扰动坍缩",
            "detection": "引力波探测可能提供线索",
        },
        "helix_unification": "暗物质晕 = 螺旋的集合（玻色-爱因斯坦凝聚态）",
        "dark_energy_unification": "暗物质（物质模式）与暗能量（真空模式）都是螺旋场的不同激发",
    }


def cosmological_parameters() -> Dict:
    """
    宇宙学参数（Planck 2018）。
    """
    return {
        "H0": f"{H0} km/s/Mpc",
        "Omega_m": OMEGA_M,
        "Omega_lambda": OMEGA_LAMBDA,
        "Omega_b": OMEGA_B,
        "Omega_cdm": OMEGA_CDM,
        "Omega_r": OMEGA_R,
        "T_CMB": f"{T_CMB} K",
        "age": f"{AGE_UNIVERSE} Gyr",
        "n_s": 0.9649,
        "sigma_8": 0.8111,
        "helix_interpretation": {
            "H0": "宇宙螺旋的当前频率（ω = H0）",
            "Omega_m": "物质螺旋模式的能量占比",
            "Omega_lambda": "真空螺旋模式的能量占比",
            "age": "宇宙螺旋的当前年龄（螺旋圈数）",
        },
    }


def cosmological_puzzles() -> Dict:
    """
    宇宙学疑难的螺旋解释。
    """
    return {
        "horizon_problem": {
            "problem": "CMB全天空均匀，但复合时视界内区域今天只有~1°",
            "solution": "暴胀将微小因果区域拉伸到整个可观测宇宙",
            "helix_interpretation": "暴胀前宇宙是一个微小螺旋（R~ℓ_P），暴胀将螺旋半径指数拉伸",
        },
        "flatness_problem": {
            "problem": "宇宙空间近乎平坦（|Ω_k| < 0.001），但平坦性是不稳定不动点",
            "solution": "暴胀期间Ω_k ~ 1/(aH)²指数衰减",
            "helix_interpretation": "暴胀将螺旋半径拉伸到极大，大半径螺旋的曲率~1/R²→0",
        },
        "monopole_problem": {
            "problem": "GUT预言早期宇宙产生大量磁单极，但观测中从未发现",
            "solution": "暴胀将磁单极密度指数稀释",
            "helix_interpretation": "磁单极=螺旋的拓扑缺陷（扭结），暴胀将螺旋拉伸，缺陷被稀释",
        },
        "baryon_asymmetry": "螺旋的CP破坏产生物质-反物质不对称",
        "large_scale_structure": "螺旋的原初涨落演化成星系分布",
        "cosmological_constant": "螺旋的视界截断自然给出小Λ",
        "coincidence_problem": "今天Ω_m ~ Ω_Λ（螺旋演化的自然结果）",
    }


def cosmology_open_problems() -> Dict:
    """
    宇宙学开放问题清单。
    """
    return {
        "OPEN1": "暴胀子的具体势能（V(φ)形式尚未确定）",
        "OPEN2": "暗物质的具体候选者（WIMP/轴子/PBH尚未确认）",
        "OPEN3": "Reheating的具体机制（暴胀子衰变率、产物谱、热历史）",
        "OPEN4": "大爆炸之前（暴胀之前发生了什么？宇宙有开端吗？）",
        "OPEN5": "暗能量的动力学（宇宙学常数w=-1还是quintessence？）",
        "observational_tests": ["CMB B模观测", "暗物质直接探测", "引力波宇宙学", "重子声学振荡"],
    }
