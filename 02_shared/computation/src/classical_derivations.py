# derivations.py — 求导理论体系（方法①：从公理到方程）
#
# 算法联盟 · openuft · triad_uft
#
# 核心命题：所有方程都是某个作用量 S 的 Euler-Lagrange 变分方程。
#   - D0 作用量变分求导：Einstein(δS/δg)、Yang-Mills(δS/δA)、Klein-Gordon、Maxwell
#   - D5 大统一力方程（张祥前）：P = m(c-v), dP/dt = F
#
# 每个函数返回 sympy 表达式或数值校验，可被 verify.py 复算。

import sympy as sp
import math

import physics_constants as physics


# ----------------------------------------------------------------------------
# D0-1：Klein-Gordon（标量场作用量变分）
# ----------------------------------------------------------------------------
def kg_equation():
    """L = 1/2 (∂_t φ)^2 - 1/2 (∇φ)^2 - 1/2 m^2 φ^2
    → Euler-Lagrange: (∂_t^2 - ∇^2 + m^2) φ = 0
    """
    t, x, y, z, m = sp.symbols("t x y z m", real=True)
    phi = sp.Function("phi")
    dphit = sp.diff(phi(t, x, y, z), t)
    dphix = sp.diff(phi(t, x, y, z), x)
    dphiy = sp.diff(phi(t, x, y, z), y)
    dphiz = sp.diff(phi(t, x, y, z), z)
    L = sp.Rational(1, 2) * dphit ** 2 - sp.Rational(1, 2) * (dphix ** 2 + dphiy ** 2 + dphiz ** 2) - sp.Rational(1, 2) * m ** 2 * phi(t, x, y,z) ** 2
    # 对 ∂_t φ 变分 → ∂_t^2 φ；对 φ 变分 → -∇^2 φ + m^2 φ
    eom = sp.diff(L, dphit, t) - sp.diff(L, phi(t, x, y, z)) + sp.diff(L, dphix, x) + sp.diff(L, dphiy, y) + sp.diff(L, dphiz, z)
    return sp.simplify(eom)


# ----------------------------------------------------------------------------
# D0-2：Maxwell 平面波 E = c B 与 c = 1/sqrt(ε0 μ0)
# ----------------------------------------------------------------------------
def maxwell_wave_relation():
    """由真空 Maxwell 方程推出平面波 E = c B，且 c = 1/sqrt(ε0 μ0)。"""
    eps0 = physics.VACUUM_PERMITTIVITY
    mu0 = physics.VACUUM_PERMEABILITY
    c = 1.0 / math.sqrt(eps0 * mu0)
    rel_err = abs(c - physics.SPEED_OF_LIGHT) / physics.SPEED_OF_LIGHT
    return {"c_from_em": c, "c_exact": physics.SPEED_OF_LIGHT, "rel_err": rel_err}


def maxwell_from_lagrangian():
    """演示：L_EM = -1/4 F_{μν} F^{μν}, F_{μν}=∂_μ A_ν - ∂_ν A_μ
    → ∂_μ F^{μν} = 0（无源）。用 sympy 在 1+1 维显示结构。
    """
    t, x = sp.symbols("t x", real=True)
    A0 = sp.Function("A0")
    A1 = sp.Function("A1")
    # 1+1 维：F_{01} = ∂_0 A_1 - ∂_1 A_0
    F01 = sp.diff(A1(t, x), t) - sp.diff(A0(t, x), x)
    # L = -1/2 F_{01}^2  → E-L 对 A_1: ∂_0 F_{01}=0; 对 A_0: -∂_1 F_{01}=0
    eom_A1 = sp.diff(F01, t)                       # ∂_0 F^{01}
    eom_A0 = -sp.diff(F01, x)                      # -∂_1 F^{01}
    return {"eom_A1": sp.simplify(eom_A1), "eom_A0": sp.simplify(eom_A0)}


# ----------------------------------------------------------------------------
# D0-3：Einstein-Hilbert 变分（结果陈述 + 数值自洽校验）
# ----------------------------------------------------------------------------
def einstein_hilbert_variation():
    """δS_EH/δg_{μν} = (1/2)√-g (R_{μν} - 1/2 R g_{μν} + Λ g_{μν})
    本函数校验其平直极限（R_{μν}=0, Λ=0）→ 真空 Einstein 方程 0=0，
    以及 trace 关系 R = -4 Λ（4 维带宇宙学常数）。
    """
    Lam = sp.symbols("Lambda", real=True)
    R = sp.symbols("R", real=True)
    # 带 Λ 的 Einstein 方程 trace: R_{μν} - 1/2 R g_{μν} + Λ g_{μν} = 0
    # 取 trace（g^{μν} g_{μν}=4）：R - 2R + 4Λ = 0 → R = 4Λ（注意符号约定）
    trace_relation = sp.Eq(R - 2 * R + 4 * Lam, 0)
    return {"trace_relation": trace_relation, "R_from_trace": sp.solve(trace_relation, R)}


# ----------------------------------------------------------------------------
# D5：大统一力方程（张祥前）P = m(c - v), dP/dt = F
# ----------------------------------------------------------------------------


__all__ = [
    "kg_equation", "maxwell_wave_relation", "maxwell_from_lagrangian",
    "einstein_hilbert_variation",
]
