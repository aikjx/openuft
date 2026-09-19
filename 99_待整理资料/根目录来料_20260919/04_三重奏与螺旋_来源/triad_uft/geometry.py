# -*- coding: utf-8 -*-
"""
triad_uft.geometry — Frenet 几何框架
====================================
全维曲线的曲率/挠率计算（解析 + 数值差分）。
支持 3D 螺旋解析解与任意离散轨迹的数值 Frenet 标架。
"""
import numpy as np


def helix_curvature_torsion(R, omega, b):
    """
    匀速螺旋 r(t)=(R cosωt, R sinωt, bt) 的解析曲率/挠率。

    Parameters
    ----------
    R : float  回旋半径
    omega : float  角频率
    b : float  轴向速度

    Returns
    -------
    dict: {kappa, tau, v, kappa2, tau2, sum2, omega2_over_v2, rel_error}
    """
    v2 = R**2 * omega**2 + b**2
    v = np.sqrt(v2)
    kappa = R * omega**2 / v2
    tau = omega * b / v2
    kappa2 = kappa**2
    tau2 = tau**2
    sum2 = kappa2 + tau2
    rhs = omega**2 / v2
    rel = abs(sum2 - rhs) / rhs if rhs > 0 else float('inf')
    return {
        "kappa": kappa, "tau": tau, "v": v,
        "kappa2": kappa2, "tau2": tau2,
        "sum_kappa_tau_sq": sum2,
        "omega2_over_v2": rhs,
        "rel_error": rel,
    }


def alldim_helix_curvatures(omegas, Rs, b):
    """
    D维多平面超螺旋的曲率平方和。

    Parameters
    ----------
    omegas : list[float]  各平面角频率 [ω₁,...,ω_m]
    Rs : list[float]  各平面半径 [R₁,...,R_m]
    b : float  轴向速度

    Returns
    -------
    dict: {sum_kappa_sq, sum_omega_sq, v2, rel_error}
    """
    m = len(omegas)
    v2 = sum(Rs[j]**2 * omegas[j]**2 for j in range(m)) + b**2
    sum_omega2 = sum(w**2 for w in omegas)
    # 全维定理：Σκᵢ² = Σωⱼ² / v²
    sum_kappa2 = sum_omega2 / v2
    rhs = sum_omega2 / v2
    rel = abs(sum_kappa2 - rhs) / rhs if rhs > 0 else float('inf')
    return {
        "sum_kappa_sq": sum_kappa2,
        "sum_omega_sq": sum_omega2,
        "v2": v2,
        "rel_error": rel,
        "dimension": 2 * m + 1,
    }


def frenet_from_trajectory(traj, dt, order=4):
    """
    从离散轨迹数值计算曲率平方和挠率平方（3D）。

    Parameters
    ----------
    traj : ndarray (N, 3)  轨迹点
    dt : float  时间步长
    order : int  差分阶数 (2 或 4)

    Returns
    -------
    dict: {kappa2, tau2, v2, x_pos, indices}
    """
    n = len(traj)
    if order == 4:
        i0, i1 = 3, n - 4
        sl = slice(i0, i1 + 1)
        v = (-traj[i0+2:i1+3] + 8*traj[i0+1:i1+2]
             - 8*traj[i0-1:i1] + traj[i0-2:i1-1]) / (12 * dt)
        a = (-traj[i0+2:i1+3] + 16*traj[i0+1:i1+2] - 30*traj[sl]
             + 16*traj[i0-1:i1] - traj[i0-2:i1-1]) / (12 * dt**2)
        j = (-traj[i0+3:i1+4] + 8*traj[i0+2:i1+3] - 13*traj[i0+1:i1+2]
             + 13*traj[i0-1:i1] - 8*traj[i0-2:i1-1] + traj[i0-3:i1-2]) / (8 * dt**3)
    else:
        i0, i1 = 2, n - 3
        sl = slice(i0, i1 + 1)
        v = (traj[i0+1:i1+2] - traj[i0-1:i1]) / (2 * dt)
        a = (traj[i0+1:i1+2] - 2*traj[sl] + traj[i0-1:i1]) / dt**2
        j = (traj[i0+2:i1+3] - 2*traj[i0+1:i1+2]
             + 2*traj[i0-1:i1] - traj[i0-2:i1-1]) / (2 * dt**3)

    vv = np.cross(v, a, axis=1)
    nv2 = np.sum(vv * vv, axis=1)
    v2 = np.sum(v * v, axis=1)
    # 避免除零
    safe = nv2 > 1e-40
    kappa2 = np.where(safe, nv2 / v2**3, 0.0)
    tau2 = np.where(safe, (np.sum(vv * j, axis=1))**2 / nv2**2, 0.0)
    x_pos = traj[sl, 0]
    return {
        "kappa2": kappa2, "tau2": tau2, "v2": v2,
        "x_pos": x_pos, "indices": np.arange(i0, i1 + 1),
    }


def curvature_2d(vx, vy, ax, ay):
    """2D曲线曲率 κ = |vx*ay - vy*ax| / (vx²+vy²)^(3/2)"""
    return abs(vx * ay - vy * ax) / (vx**2 + vy**2)**1.5


def torsion_3d(v, a, j):
    """3D曲线挠率 τ = (v×a)·j / |v×a|²"""
    va = np.cross(v, a)
    return np.dot(va, j) / np.dot(va, va)
