# -*- coding: utf-8 -*-
"""
triad_uft.nuclear — 核力场与短程相互作用
==========================================
核力场方程：D = -G m (c - 3(r/r) ṙ) / r³
  - r⁻³衰减 → 短程力（原子核尺度主导）
  - 源于光速矢量c的方向变化

注意：核力场强度需用强耦合常数k_N而非引力常数G。
"""
import numpy as np


def nuclear_field(m, r, r_dot, c=299792458.0, G=6.67430e-11, coupling=None):
    """
    计算核力场 D = -G m (c - 3(r/r) ṙ) / r³

    参数:
        m: 质量 (scalar)
        r: 位置矢量 (np.ndarray, shape=(3,))
        r_dot: 速度矢量 (np.ndarray, shape=(3,))
        c: 光速 (scalar 或 np.ndarray)
        G: 耦合常数（默认引力常数，实际核力需替换为k_N）
        coupling: 若提供则覆盖G

    返回:
        D: 核力场矢量 (np.ndarray, shape=(3,))
    """
    if coupling is not None:
        G = coupling
    r = np.asarray(r, dtype=float)
    r_dot = np.asarray(r_dot, dtype=float)
    r_mag = np.linalg.norm(r)
    if r_mag < 1e-30:
        return np.zeros(3)
    r_hat = r / r_mag
    radial_v = np.dot(r_dot, r_hat)  # ṙ = v·r̂

    if np.isscalar(c):
        c_vec = c * r_hat  # 假设光速沿径向
    else:
        c_vec = np.asarray(c, dtype=float)

    D = -G * m * (c_vec - 3 * r_hat * radial_v) / r_mag**3
    return D


def nuclear_potential(m, r, c=299792458.0, G=6.67430e-11, coupling=None):
    """
    核力势能（ṙ=0时）V_N = -G m c / (2 r²)

    参数:
        m: 质量
        r: 距离 (scalar)
        c: 光速
        G: 耦合常数
        coupling: 若提供则覆盖G

    返回:
        V_N: 核力势能 (scalar)
    """
    if coupling is not None:
        G = coupling
    return -G * m * c / (2 * r**2)


def nuclear_force_range(m_W, hbar=1.054571817e-34, c=299792458.0):
    """
    核力/弱力力程（康普顿波长）λ = ħ/(m_W c)

    参数:
        m_W: 媒介玻色子质量（如W玻色子80.4GeV/c²）
        hbar: 约化普朗克常数
        c: 光速

    返回:
        lambda: 力程 (m)
    """
    return hbar / (m_W * c)


def infer_nuclear_coupling(V_target, r, m, c=299792458.0):
    """
    由目标核力势能反推耦合常数 k_N = 2 |V_target| r² / (m c)

    参数:
        V_target: 目标势能（绝对值，J）
        r: 距离 (m)
        m: 质量 (kg)
        c: 光速

    返回:
        k_N: 核力耦合常数 (m³/(kg·s²))
    """
    return 2 * abs(V_target) * r**2 / (m * c)


def nuclear_to_gravity_ratio(r, c=299792458.0):
    """
    核力/引力强度比 |D|/|g| = c/r （ṙ=0时）

    参数:
        r: 距离 (m)
        c: 光速

    返回:
        ratio: 核力/引力比
    """
    return c / r
