# -*- coding: utf-8 -*-
"""
triad_uft.triad — 三重奏定理高层 API
====================================
封装已严格证明的三重奏定理，提供统一验证接口。

定理体系：
  1. 螺旋三重奏（R4）：κ²+τ²=(ω/v)²  [PROVEN]
  2. 全维三重奏（R9）：Σκᵢ²=(Σωⱼ²)/v²  [PROVEN]
  3. 绝热三重奏（R10）：缓变频率二阶修正  [VERIFIED]
  4. 纯圆周精确性（R10）：b=0任意时变角速度精确  [PROVEN]
  5. 梯度磁场精确性（R11）：空间梯度磁场精确恒等  [PROVEN]
"""
import numpy as np
from .geometry import helix_curvature_torsion, alldim_helix_curvatures
from .lorentz import LorentzSimulator, GradientB, UniformB
from . import constants as C
from .provenance import THEOREMS, ValidationStatus


def check_helix(R=1.0, omega=1.0, b=0.5):
    """
    螺旋三重奏验证。

    Returns
    -------
    dict: 曲率/挠率/相对差
    """
    return helix_curvature_torsion(R, omega, b)


def check_alldim(omegas, Rs, b=0.0):
    """
    全维多平面超螺旋三重奏验证。

    Parameters
    ----------
    omegas : list  各平面角频率
    Rs : list  各平面半径
    b : float  轴向速度
    """
    return alldim_helix_curvatures(omegas, Rs, b)


def check_adiabatic(omega0=2.0, eps=0.01, R=1.0, b=0.6, t=1.0):
    """
    绝热缓变螺旋三重奏验证（θ(t)=ω₀t+½εt²）。

    Returns
    -------
    dict: {kappa2, tau2, rhs, rel_error, epsilon}
    """
    theta_p = omega0 + eps * t
    theta_pp = eps
    theta_ppp = 0.0
    v2 = R**2 * theta_p**2 + b**2
    # 数值曲率/挠率（从解析轨迹差分）
    dt = 1e-7
    ts = np.array([t - 2*dt, t - dt, t, t + dt, t + 2*dt])
    thetas = omega0 * ts + 0.5 * eps * ts**2
    traj = np.stack([R * np.cos(thetas), R * np.sin(thetas), b * ts], axis=1)
    from .geometry import frenet_from_trajectory
    fr = frenet_from_trajectory(traj, dt, order=4)
    idx = len(fr["kappa2"]) // 2
    kappa2 = fr["kappa2"][idx]
    tau2 = fr["tau2"][idx]
    v2_num = fr["v2"][idx]
    rhs = theta_p**2 / v2_num
    lhs = kappa2 + tau2
    rel = abs(lhs - rhs) / rhs if rhs > 0 else float('inf')
    return {
        "kappa2": kappa2, "tau2": tau2,
        "omega_instant": theta_p, "v2": v2_num,
        "rhs": rhs, "lhs": lhs,
        "rel_error": rel, "epsilon": eps,
    }


def check_gradient_b_field(B0=1.0, g=50.0, v_perp=1e7, v_par=5e6,
                           t_end=None, dt=1e-15):
    """
    梯度磁场三重奏精确性验证（R11定理）。

    Parameters
    ----------
    B0 : float  基准磁场 T
    g : float  梯度 T/m
    v_perp : float  垂直速度 m/s
    v_par : float  平行速度 m/s
    t_end : float  模拟时长（默认1/4圈）
    dt : float  时间步长

    Returns
    -------
    dict: {rel_errors, median, max, simulator}
    """
    qm = float(C.ELECTRON_QM)
    omega0 = abs(qm) * B0
    if t_end is None:
        t_end = (np.pi / 2) / omega0  # 1/4 圈
    sim = LorentzSimulator(q_over_m=qm, b_field=GradientB(B0, g))
    sim.run(v0=[v_perp, 0.0, v_par], t_end=t_end, dt=dt)
    result = sim.triad_check()
    result["simulator"] = sim
    result["B0"] = B0
    result["g"] = g
    return result


def check_uniform_b_field(B0=1.0, v_perp=1e7, v_par=5e6,
                          n_turns=2, dt=1e-15):
    """均匀磁场三重奏验证（对照，应精确）"""
    qm = float(C.ELECTRON_QM)
    omega0 = abs(qm) * B0
    t_end = n_turns * 2 * np.pi / omega0
    sim = LorentzSimulator(q_over_m=qm, b_field=UniformB(B0))
    sim.run(v0=[v_perp, 0.0, v_par], t_end=t_end, dt=dt)
    result = sim.triad_check()
    result["simulator"] = sim
    return result


def electron_benchmark(B=1.0, v_perp_frac=0.6, v_par_frac=0.5):
    """
    电子在磁场中的相对论对标（R6 AD4）。
    v_perp_frac, v_par_frac 为光速分数。

    Returns
    -------
    dict: {omega, gamma, kappa, tau, rel_error}
    """
    c = float(C.C)
    v_perp = v_perp_frac * c
    v_par = v_par_frac * c
    v = np.sqrt(v_perp**2 + v_par**2)
    gamma = 1.0 / np.sqrt(1 - v**2 / c**2)
    omega = abs(float(C.ELECTRON_QM)) * B / gamma
    R = v_perp / omega
    result = helix_curvature_torsion(R, omega, v_par)
    result["gamma"] = gamma
    result["B"] = B
    return result


def theorem_status(name=None):
    """查询定理验证状态"""
    if name:
        return THEOREMS.get(name)
    return dict(THEOREMS)


def proven_theorems():
    """返回所有已严格证明的定理"""
    return {k: v for k, v in THEOREMS.items()
            if v.status == ValidationStatus.PROVEN}


def open_problems():
    """返回所有开放问题"""
    return {k: v for k, v in THEOREMS.items()
            if v.status == ValidationStatus.OPEN}
