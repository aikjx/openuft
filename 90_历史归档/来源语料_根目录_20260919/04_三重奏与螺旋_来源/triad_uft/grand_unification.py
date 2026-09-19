# -*- coding: utf-8 -*-
"""
triad_uft.grand_unification — 宇宙大统一力方程
================================================
核心方程：F = d[m(c-v)]/dt = c dm/dt - v dm/dt + m dc/dt - m dv/dt
  ├─ c dm/dt   → 电场力
  ├─ -v dm/dt  → 磁场力
  ├─ m dc/dt   → 引力/核力（光速方向变化）
  └─ -m dv/dt  → 惯性力（牛顿第二定律）

基于张祥前统一场论20核心公式。
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class ForceComponents:
    """大统一力的四力分解结果"""
    electric: np.ndarray    # c dm/dt
    magnetic: np.ndarray    # -v dm/dt
    gravitational: np.ndarray  # m dc/dt
    inertial: np.ndarray    # -m dv/dt
    total: np.ndarray       # 合力

    def as_dict(self):
        return {
            "electric": self.electric.tolist(),
            "magnetic": self.magnetic.tolist(),
            "gravitational": self.gravitational.tolist(),
            "inertial": self.inertial.tolist(),
            "total": self.total.tolist(),
        }


def grand_force(m, dm_dt, c, dc_dt, v, dv_dt):
    """
    计算大统一力 F = d[m(c-v)]/dt

    参数:
        m: 质量 (scalar)
        dm_dt: 质量变化率 (scalar)
        c: 光速矢量 (np.ndarray, shape=(3,))
        dc_dt: 光速矢量变化率 (np.ndarray, shape=(3,))
        v: 物体速度矢量 (np.ndarray, shape=(3,))
        dv_dt: 加速度矢量 (np.ndarray, shape=(3,))

    返回:
        ForceComponents: 四力分解结果
    """
    c = np.asarray(c, dtype=float)
    dc_dt = np.asarray(dc_dt, dtype=float)
    v = np.asarray(v, dtype=float)
    dv_dt = np.asarray(dv_dt, dtype=float)

    F_electric = c * dm_dt
    F_magnetic = -v * dm_dt
    F_gravitational = m * dc_dt
    F_inertial = -m * dv_dt
    F_total = F_electric + F_magnetic + F_gravitational + F_inertial

    return ForceComponents(
        electric=F_electric,
        magnetic=F_magnetic,
        gravitational=F_gravitational,
        inertial=F_inertial,
        total=F_total,
    )


def mass_velocity_relation(m0, v, c=299792458.0, model="relativistic"):
    """
    质速关系

    参数:
        m0: 静止质量
        v: 速度大小 (scalar)
        c: 光速
        model: "relativistic" (相对论m=γm₀) 或 "zhang" (张祥前m=m₀/(1-v/c))

    返回:
        运动质量
    """
    beta = v / c
    if model == "relativistic":
        gamma = 1.0 / np.sqrt(1.0 - beta**2)
        return m0 * gamma
    elif model == "zhang":
        return m0 / (1.0 - beta)
    else:
        raise ValueError(f"Unknown model: {model}")


def energy_momentum_relation(m, v, c=299792458.0, model="relativistic"):
    """
    能量-动量关系 E² - (pc)²

    参数:
        m: 静止质量
        v: 速度大小
        c: 光速
        model: "relativistic" 或 "zhang"

    返回:
        (E, p, E2_p2c2): 能量、动量、E²-(pc)²
    """
    beta = v / c
    if model == "relativistic":
        gamma = 1.0 / np.sqrt(1.0 - beta**2)
        E = gamma * m * c**2
        p = gamma * m * v
    elif model == "zhang":
        m_moving = m / (1.0 - beta)
        E = m_moving * c**2 * np.sqrt(1.0 - beta**2)
        p = m_moving * (c - v)  # P = m(c-v), v∥c
    else:
        raise ValueError(f"Unknown model: {model}")

    E2_p2c2 = E**2 - (p * c)**2
    return E, p, E2_p2c2


def rest_energy(m0, c=299792458.0):
    """静止能量 E₀ = m₀c²"""
    return m0 * c**2


def rest_momentum(m0, c=299792458.0):
    """静止动量 p₀ = m₀c（张祥前统一场论核心假设）"""
    return m0 * c
