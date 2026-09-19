# -*- coding: utf-8 -*-
"""
triad_uft.artificial_field — 变化电磁场产生引力场（人工场设计）
================================================================
核心方程：∂B/∂t = -(g × E)/c²
反解：g = c² (∂B/∂t × E) / |E|²

基于张祥前统一场论。人工场实验设计与参数计算。
"""
import numpy as np
from dataclasses import dataclass


@dataclass
class ArtificialFieldResult:
    """人工场计算结果"""
    gravitational_field: np.ndarray  # 产生的引力场 g
    magnitude: float                  # |g|
    in_earth_g: float                 # g / g_earth
    config: dict                      # 输入配置


def artificial_gravity_field(dB_dt, E, c=299792458.0, g_earth=9.80665):
    """
    计算变化电磁场产生的引力场 g = c² (∂B/∂t × E) / |E|²

    参数:
        dB_dt: 磁场变化率矢量 (np.ndarray, shape=(3,)), 单位T/s
        E: 电场矢量 (np.ndarray, shape=(3,)), 单位V/m
        c: 光速
        g_earth: 地球重力加速度

    返回:
        ArtificialFieldResult
    """
    dB_dt = np.asarray(dB_dt, dtype=float)
    E = np.asarray(E, dtype=float)
    E_mag = np.linalg.norm(E)
    if E_mag < 1e-30:
        raise ValueError("Electric field magnitude must be non-zero")

    g = c**2 * np.cross(dB_dt, E) / E_mag**2
    g_mag = np.linalg.norm(g)

    return ArtificialFieldResult(
        gravitational_field=g,
        magnitude=g_mag,
        in_earth_g=g_mag / g_earth,
        config={"dB_dt": dB_dt.tolist(), "E": E.tolist(), "c": c},
    )


def required_dBdt_for_gravity(g_target, E, c=299792458.0):
    """
    计算产生目标引力场所需的磁场变化率 |∂B/∂t| = g |E| / c²
    （当∂B/∂t⊥E时）

    参数:
        g_target: 目标引力场大小 (m/s²)
        E: 电场大小 (V/m)
        c: 光速

    返回:
        dB_dt: 所需磁场变化率 (T/s)
    """
    return g_target * E / c**2


def solenoid_dBdt(n, dI_dt, mu0=1.25663706212e-6):
    """
    螺线管磁场变化率 ∂B/∂t = μ₀ n (dI/dt)

    参数:
        n: 线圈匝数密度 (匝/m)
        dI_dt: 电流变化率 (A/s)
        mu0: 真空磁导率

    返回:
        dB_dt: 磁场变化率 (T/s)
    """
    return mu0 * n * dI_dt


def design_experiment(E, dB_dt, c=299792458.0, g_earth=9.80665):
    """
    人工场实验设计：给定E和∂B/∂t，计算产生的引力场和可行性

    参数:
        E: 电场大小 (V/m)
        dB_dt: 磁场变化率 (T/s)
        c: 光速
        g_earth: 地球重力

    返回:
        dict: 设计结果
    """
    g = c**2 * dB_dt / E  # ∂B/∂t⊥E时
    g_ratio = g / g_earth

    # 可行性评估
    if g_ratio > 1e-6:
        measurable = "可测量（MEMS加速度计）"
    elif g_ratio > 1e-12:
        measurable = "可测量（超导加速度计/LIGO级）"
    else:
        measurable = "极难测量"

    # 技术可行性
    if dB_dt < 1:
        tech = "常规电源"
    elif dB_dt < 1e4:
        tech = "脉冲功率"
    elif dB_dt < 1e8:
        tech = "极限脉冲"
    else:
        tech = "激光驱动（当前极限）"

    return {
        "E_V_per_m": E,
        "dB_dt_T_per_s": dB_dt,
        "g_m_per_s2": g,
        "g_over_g_earth": g_ratio,
        "measurable": measurable,
        "technology": tech,
    }


def ligo_comparison(g, frequency=100.0, L=4000.0):
    """
    与LIGO灵敏度对比

    参数:
        g: 人工场引力场 (m/s²)
        frequency: 频率 (Hz)
        L: LIGO臂长 (m)

    返回:
        dict: 对比结果
    """
    omega = 2 * np.pi * frequency
    # LIGO应变灵敏度 ~1e-22, 对应位移 ΔL ~ 4e-19 m
    ligo_displacement = 1e-22 * L
    ligo_acceleration = omega**2 * ligo_displacement
    ratio = g / ligo_acceleration if ligo_acceleration > 0 else float('inf')

    return {
        "artificial_g": g,
        "ligo_equivalent_acceleration": ligo_acceleration,
        "ratio_artificial_to_ligo": ratio,
        "note": f"人工场比LIGO可探测加速度强 {ratio:.2e} 倍",
    }
