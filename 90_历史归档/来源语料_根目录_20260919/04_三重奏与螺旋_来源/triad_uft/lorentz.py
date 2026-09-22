# -*- coding: utf-8 -*-
"""
triad_uft.lorentz — 洛伦兹力轨迹模拟器
======================================
RK4 积分带电粒子在任意磁场中的运动。
支持均匀磁场、空间梯度磁场。
经典非相对论（v<<c）；相对论版本为 OPEN。
"""
import numpy as np
from .geometry import frenet_from_trajectory
from . import constants as C


class MagneticField:
    """磁场基类：B(x,y,z) -> (Bx, By, Bz)"""
    def __call__(self, x, y, z):
        raise NotImplementedError

    def batch_norm(self, x_pos):
        """向量化计算 |B(x,0,0)|，子类可覆盖以优化。默认逐点计算。"""
        return np.array([np.linalg.norm(self(x, 0, 0)) for x in x_pos])


class UniformB(MagneticField):
    """均匀磁场 B = B0 * direction"""
    def __init__(self, B0=1.0, direction="z"):
        self.B0 = B0
        self.direction = direction

    def __call__(self, x, y, z):
        if self.direction == "z":
            return np.array([0.0, 0.0, self.B0])
        elif self.direction == "x":
            return np.array([self.B0, 0.0, 0.0])
        elif self.direction == "y":
            return np.array([0.0, self.B0, 0.0])
        raise ValueError(f"Unknown direction: {self.direction}")

    def batch_norm(self, x_pos):
        """均匀磁场：|B|=B0 常数，直接返回全B0数组"""
        return np.full_like(np.asarray(x_pos, dtype=float), self.B0)


class GradientB(MagneticField):
    """
    空间梯度磁场 B(x) = (B0 + g*x) * z_hat。
    方向不变（沿z），大小随x线性变化。
    三重奏在此磁场中精确成立（R11定理）。
    """
    def __init__(self, B0=1.0, g=50.0):
        self.B0 = B0
        self.g = g

    def __call__(self, x, y, z):
        return np.array([0.0, 0.0, self.B0 + self.g * x])

    def batch_norm(self, x_pos):
        """向量化：|B(x)| = |B0 + g*x|"""
        return np.abs(self.B0 + self.g * np.asarray(x_pos, dtype=float))


class LorentzSimulator:
    """
    带电粒子洛伦兹力运动模拟器（经典非相对论）。

    Parameters
    ----------
    q_over_m : float  荷质比 C/kg（电子为负）
    b_field : MagneticField  磁场对象
    """

    def __init__(self, q_over_m=None, b_field=None):
        if q_over_m is None:
            q_over_m = float(C.ELECTRON_QM)  # 电子默认
        if b_field is None:
            b_field = UniformB(B0=1.0)
        self.q_over_m = q_over_m
        self.b_field = b_field
        self.trajectory = None
        self.times = None
        self.dt = None

    def _rhs(self, state):
        x, y, z, vx, vy, vz = state
        Bx, By, Bz = self.b_field(x, y, z)
        qm = self.q_over_m
        ax = qm * (vy * Bz - vz * By)
        ay = qm * (vz * Bx - vx * Bz)
        az = qm * (vx * By - vy * Bx)
        return np.array([vx, vy, vz, ax, ay, az])

    def _rk4_step(self, state, dt):
        k1 = self._rhs(state)
        k2 = self._rhs(state + 0.5 * dt * k1)
        k3 = self._rhs(state + 0.5 * dt * k2)
        k4 = self._rhs(state + dt * k3)
        return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    def run(self, v0, t_end, dt=1e-15, x0=None):
        """
        运行模拟。

        Parameters
        ----------
        v0 : array(3,)  初速度 [vx, vy, vz]
        t_end : float  结束时间
        dt : float  时间步长
        x0 : array(3,)  初始位置（默认原点）

        Returns
        -------
        self
        """
        if x0 is None:
            x0 = np.zeros(3)
        n = int(t_end / dt)
        traj = np.zeros((n, 3))
        state = np.concatenate([x0, np.asarray(v0, dtype=float)])
        for i in range(n):
            traj[i] = state[:3]
            state = self._rk4_step(state, dt)
        self.trajectory = traj
        self.times = np.arange(n) * dt
        self.dt = dt
        return self

    def cyclotron_frequency(self, x=0.0):
        """局部回旋频率 ω_c = |q/m| * |B(x)|"""
        B = self.b_field(x, 0, 0)
        return abs(self.q_over_m) * np.linalg.norm(B)

    def cyclotron_radius(self, v_perp, x=0.0):
        """局部回旋半径 R_c = v_perp / ω_c"""
        return v_perp / self.cyclotron_frequency(x)

    def triad_check(self, order=4):
        """
        对轨迹做三重奏检验：κ²+τ² vs (ω_c(x)/v)²。

        Returns
        -------
        dict: {rel_errors, median, max, kappa2, tau2, rhs}
        """
        if self.trajectory is None:
            raise RuntimeError("Call run() first")
        fr = frenet_from_trajectory(self.trajectory, self.dt, order=order)
        x_pos = fr["x_pos"]
        # 局部回旋频率（向量化，UniformB/GradientB 已优化）
        B_norm = self.b_field.batch_norm(x_pos)
        w = abs(self.q_over_m) * B_norm
        rhs = w**2 / fr["v2"]
        lhs = fr["kappa2"] + fr["tau2"]
        rel = np.abs(lhs - rhs) / rhs
        return {
            "rel_errors": rel,
            "median": float(np.median(rel)),
            "max": float(np.max(rel)),
            "kappa2": fr["kappa2"],
            "tau2": fr["tau2"],
            "rhs": rhs,
            "x_pos": x_pos,
        }
