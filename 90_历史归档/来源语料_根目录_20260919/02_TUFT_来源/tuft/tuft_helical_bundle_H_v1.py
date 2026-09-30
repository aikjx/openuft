# -*- coding: utf-8 -*-
"""
tuft_helical_bundle_H_v1.py
==========================

H-TUFT 螺旋挠率丛 · 丛截面求解引擎（脚手架，非预言）

红线（与卷二十五 §0.4 一致，守 TUFT「数学自洽 ≠ 实验证实」）：
- 本引擎 ODE **不来自** §5 作用量（L = ¼ F∧⋆F + V 的变分给出 D⋆F = J[Ψ]，
  绝非 d2Omega = …）；它是为演示管道而写的**数值脚手架**。
- τ_proj = Q_hel · |Ψ| · Re(Ω) 是**发明投影式**：无量纲、无物理标度、无观测换算。
- 本文件**不声称**产生任何可检验预言；Q_hel = ±1 仅做代数符号反演，
  不给出任何手征分裂幅值（见 _demo 输出）。
- 诚实结论：引擎须替换为「从 §5 作用量变分导出的真实丛演化方程」方可作预言使用。

数值说明：
- Omega 方程的原始写法是纯虚数赋值给实数状态导数（内部不一致，§0.4 已记）。
  此处取其实部（恒为 0）以保证实数积分器可运行；故 Omega 不演化，
  保留初始值 0.05，与卷二十五 §11 文档所述一致。
- 依赖 numpy / scipy（jax 不可用）；不引入新假设。
"""

import hashlib
import os

import numpy as np
from scipy.integrate import solve_ivp


def bundle_ode(s, y, Q_hel, g_coupling):
    """H-TUFT 丛截面 ODE（脚手架：与 §5 作用量无派生关系，仅演示管道）。

    y = [Psi_r, Psi_i, dPsi_r, dPsi_i, Omega, dOmega]
    Psi 为复截面，Omega 为丛联络实分量。
    """
    Psi_r, Psi_i, dPsi_r, dPsi_i, Omega, dOmega = y
    Psi = Psi_r + 1j * Psi_i
    dPsi = dPsi_r + 1j * dPsi_i
    mod2 = abs(Psi) ** 2
    # V = g*(|Psi|^2 - Q^2)^2 的 Wirtinger 梯度
    dVdPsi = 2.0 * g_coupling * (mod2 - Q_hel ** 2) * np.conj(Psi)
    d2Psi = -2.0j * Q_hel * Omega * dPsi - dVdPsi
    # Omega 方程（脚手架）：原式为纯虚数，取实部（≡0）以保实数积分器可运行
    d2Omega = (-Q_hel * np.conj(Psi) * dPsi + Q_hel * Psi * np.conj(dPsi))
    return [dPsi_r, dPsi_i, d2Psi.real, d2Psi.imag, dOmega, d2Omega.real]


def solve_htuft(Q_hel, g_coupling, s0=0.0, s1=6.95):
    """求解丛截面，返回 (sol, tau_proj, |Psi|, Omega)。"""
    y0 = [0.1, 0.0, 0.0, 0.0, 0.05, 0.0]
    sol = solve_ivp(
        lambda s, y: bundle_ode(s, y, Q_hel, g_coupling),
        (s0, s1), y0, method="RK45", rtol=1e-6, atol=1e-9,
        dense_output=True,
    )
    Psi = sol.y[0, -1] + 1j * sol.y[1, -1]
    Omega = sol.y[4, -1]
    tau_proj = Q_hel * abs(Psi) * Omega.real  # 发明投影式，无量纲、无物理标度
    return sol, tau_proj, abs(Psi), Omega.real


def sha256_of_this_file():
    path = os.path.abspath(__file__)
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def _demo():
    print("=" * 72)
    print("H-TUFT 丛截面引擎 · 脚手架实跑（非预言）")
    print("红线：数学自洽 ≠ 实验证实；本引擎不来自 §5 作用量变分")
    print("=" * 72)
    for Q in (+1, -1):
        sol, tau, modpsi, om = solve_htuft(Q, 0.12, 0.0, 6.95)
        print(
            f"Q_hel={Q:+d} g=0.12 -> "
            f"|Psi|={modpsi:.3e}  Omega={om:.3e}  tau_proj={tau:.3e}"
        )
    print("-" * 72)
    print("诚实解读：tau_proj 无量纲、无标度；Q_hel=±1 仅符号反演，")
    print("            不给出任何手征分裂幅值 → 纯管道脚手架非预言。")
    print(f"script SHA256 = {sha256_of_this_file()}")


if __name__ == "__main__":
    _demo()
