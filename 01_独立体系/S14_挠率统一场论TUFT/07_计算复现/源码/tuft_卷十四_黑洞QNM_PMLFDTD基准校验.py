# -*- coding: utf-8 -*-
"""
================================================================================
TUFT 卷十四 · 主线 B：黑洞 QNM 基准校验（TB=0，退化为 Schwarzschild）
================================================================================

设计稿 / 规划骨架。依赖：jax + jax.scipy.sparse.linalg.eigs（或 scipy）。

目标：当 TB=0，求解器输出必须复现标准 Schwarzschild QNM：
    omega_ref ≈ 0.37367 - 0.08896i   (M=1, l=2 四极基模)

校验流程：
  1) TB=0，关闭挠率势；
  2) 网格收敛测试 N=400/800/1600；
  3) |omega_num - omega_ref| < 1e-4 判定基准通过；
  4) 基准通过后扫描 TB ∈ [0, 1e-4]，拟合 omega_R/I 的线性响应。

TODO（未实现占位）：
  - build_fdtd_matrix：PML-FDTD 复曲率-挠率波动方程矩阵装配，待落地
================================================================================
"""
from __future__ import print_function

import jax.numpy as jnp
from jax.scipy.sparse.linalg import eigs


def benchmark_schwarzschild():
    """TB=0，纯 Schwarzschild 基准校验。"""
    TB_test = 0.0
    rstar = jnp.linspace(-20.0, 20.0, 1600)
    sigma_pml = jnp.zeros_like(rstar)
    sigma_pml = sigma_pml.at[:160].set(2.0)
    sigma_pml = sigma_pml.at[-160:].set(2.0)
    A, B = build_fdtd_matrix(rstar, TB_test, sigma_pml)  # TODO: 实现
    vals, vecs = eigs(A, M=B, k=6, sigma=0.37 - 0.09j)
    omega = jnp.sqrt(vals)
    omega_sorted = sorted(omega, key=lambda x: jnp.abs(x.real - 0.37367))
    omega0 = omega_sorted[0]
    print(f"Numerical omega (TB=0): {omega0:.6f}")
    print(f"Reference omega: 0.37367 - 0.08896i")
    err = jnp.abs(omega0 - (0.37367 - 0.08896j))
    print(f"Absolute error: {err:.2e}")
    return omega0, err


def scan_TB():
    """基准通过后扫描 TB ∈ [0, 1e-4]，拟合线性响应。

    Returns: 离散采样点 omega 表 + 斜率 k_R, k_I。
    """
    points = [0.0, 1e-5, 2e-5, 5e-5, 1e-4]
    rows = []
    for tb in points:
        rstar = jnp.linspace(-20.0, 20.0, 1600)
        sigma_pml = jnp.zeros_like(rstar)
        sigma_pml = sigma_pml.at[:160].set(2.0)
        sigma_pml = sigma_pml.at[-160:].set(2.0)
        A, B = build_fdtd_matrix(rstar, tb, sigma_pml)  # TODO: 实现
        vals, _ = eigs(A, M=B, k=6, sigma=0.37 - 0.09j)
        omega = jnp.sqrt(vals)
        omega0 = sorted(omega, key=lambda x: jnp.abs(x.real - 0.37367))[0]
        rows.append((tb, float(omega0.real), float(omega0.imag)))
    # TODO: 拟合 omega_R/I = omega^(0) + k * TB
    return rows


# ---------------------------------------------------------------------------
# 占位函数（设计稿，运行前必须实现）
# ---------------------------------------------------------------------------
def build_fdtd_matrix(rstar, TB, sigma_pml):
    raise NotImplementedError("build_fdtd_matrix 待实现：PML-FDTD 矩阵装配")
