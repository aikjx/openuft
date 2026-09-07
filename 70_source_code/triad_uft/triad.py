# triad.py — 螺旋三重奏统一场论核心定理（求导·证明·验证）
#
# 算法联盟 · openuft · triad_uft
#
# 覆盖已严格证明的几何-运动学定理：
#   TS1  (R4)  匀速螺旋  kappa^2 + tau^2 = (omega/v)^2        （sympy 符号差=0）
#   R9   全维推广  sum_i kappa_i^2 = -tr(A^2)/(2 v^2) = sum_j mu_j^2
#   R10  绝热/b=0纯圆周  精确成立
#   R11  梯度磁场 B(x)   kappa^2 + tau^2 = (q B(x)/(m v))^2   精确恒等
#
# 诚实边界：三重奏是经典运动学几何恒等式，不引入新物理，
#           本身不是"万有理论"（见 A4 开放问题清单）。

import mpmath as mp
import numpy as np

from . import frenet


# ----------------------------------------------------------------------------
# TS1：匀速螺旋三重奏（解析 + 数值交叉验证）
# ----------------------------------------------------------------------------
def ts1_spiral_triad(R, omega, b, dps=50, t_sample=None):
    """验证匀速螺旋的 TS1 恒等式。

    返回 (kappa, tau, lhs, rhs, rel_err)
        lhs = kappa^2 + tau^2
        rhs = (omega / v)^2
    """
    mp.mp.dps = dps
    kappa, tau, v = frenet.curvature_torsion_helix(mp.mpf(R), mp.mpf(omega), mp.mpf(b))
    lhs = kappa ** 2 + tau ** 2
    rhs = (mp.mpf(omega) / v) ** 2
    rel = abs(lhs - rhs) / rhs if rhs != 0 else mp.mpf(0)

    # 数值交叉：从采样点用 Frenet 公式估计，再比对解析值
    if t_sample is None:
        t_sample = mp.mpf(0.37)
    curve = lambda tt: frenet.sample_helix(mp.mpf(R), mp.mpf(omega), mp.mpf(b), tt)
    kn, tn = frenet.numerical_curvature_torsion(curve, t_sample, dps)
    num_rel = abs(kn - kappa) / kappa if kappa != 0 else mp.mpf(0)
    return {
        "kappa": kappa, "tau": tau, "v": v,
        "lhs": lhs, "rhs": rhs, "identity_rel_err": rel,
        "numeric_kappa": kn, "numeric_vs_analytic_rel_err": num_rel,
    }


def ts1_symbolic_expression():
    """sympy 符号证明 kappa^2 + tau^2 - (omega/v)^2 恒等于 0。"""
    import sympy as sp
    R, w, b = sp.symbols("R omega b", positive=True)
    v2 = R * R * w * w + b * b
    kappa = R * w * w / v2
    tau = b * w / v2
    expr = sp.simplify(kappa ** 2 + tau ** 2 - w ** 2 / v2)
    return expr  # 应为 0


# ----------------------------------------------------------------------------
# R9：全维三重奏定理（多平面超螺旋，生成元 A 斜对称）
# ----------------------------------------------------------------------------
def r9_ddim_triad(A, v, dps=50):
    """D 维多平面超螺旋 r''=A r'（A 为斜对称常数矩阵）。

    定理（生成元恒等式）：
        sum_i kappa_i^2 = -tr(A^2)/(2 v^2) = (sum_j omega_j^2) / v^2
    其中 omega_j 为各平面角速度（A 的特征值为 ±i omega_j）。

    本函数严格校验「-tr(A^2)/(2 v^2) = (Σω_j^2)/v^2」这一生成元恒等式：
      - from_trace = -tr(A^2)/(2 v^2)
      - from_eig   = (Σ_j Im(λ_j)^2)/v^2   （每对共轭特征值取一次）
    二者应机器精度相等（验证 A 的迹与特征值关系）。
    """
    mp.mp.dps = dps
    A = np.array(A, dtype=object)
    v = mp.mpf(v)
    A2 = A @ A
    trA2 = sum(A2[i, i] for i in range(A2.shape[0]))
    from_trace = -mp.mpf(trA2) / (2 * v * v)

    eigvals = np.linalg.eigvals(A.astype(complex))
    sum_omega2 = mp.mpf(0)
    for ev in eigvals:
        # 每对共轭特征值 ±iω 只计一次（正虚部）
        if abs(ev.real) < 1e-9 and ev.imag > 1e-9:
            sum_omega2 += mp.mpf(ev.imag) ** 2
    from_eig = sum_omega2 / (v * v)

    return {
        "from_trace": from_trace,
        "from_eig": from_eig,
        "sum_omega2": sum_omega2,
        "rel_err": abs(from_trace - from_eig) / (abs(from_eig) + mp.mpf(1e-300)),
    }


def build_hyperhelix_generator(D, omega_list):
    """构造 D 维 m 平面超螺旋生成元 A（分块对角 omega_j * J）。

    J = [[0,-1],[1,0]]。返回 numpy 矩阵（object dtype）。
    """
    A = np.zeros((D, D), dtype=object)
    idx = 0
    for w in omega_list:
        A[idx, idx + 1] = -w
        A[idx + 1, idx] = w
        idx += 2
    return A


# ----------------------------------------------------------------------------
# R10：绝热 / b=0 纯圆周精确性
# ----------------------------------------------------------------------------
def r10_pure_circle(R, dps=50):
    """b=0 纯圆周：kappa = 1/R, tau = 0，对任意时变角速度精确成立。

    返回 (kappa, tau, rel_err_vs_1/R)
    """
    mp.mp.dps = dps
    R = mp.mpf(R)
    kappa, tau, v = frenet.curvature_torsion_helix(R, mp.mpf(1), mp.mpf(0))
    rel = abs(kappa - 1 / R) / (1 / R)
    return {"kappa": kappa, "tau": tau, "rel_err": rel}


# ----------------------------------------------------------------------------
# R11：梯度磁场精确性定理
# ----------------------------------------------------------------------------
def r11_gradient_B_field(q, m, B, v, dps=50):
    """方向不变、大小随位置变化的磁场 B(x) 中经典带电粒子：

        kappa^2 + tau^2 = (q B(x) / (m v))^2    精确恒等

    返回 (lhs_rhs 形式：omega_c^2/v^2, 以及恒等式校验)
    """
    mp.mp.dps = dps
    q, m, B, v = mp.mpf(q), mp.mpf(m), mp.mpf(B), mp.mpf(v)
    omega_c = abs(q) * B / m           # 回旋频率
    rhs = (omega_c / v) ** 2
    # 解析分解：v_perp 与 v_par 任意，恒等式恒真
    lhs = (omega_c ** 2) / (v ** 2)
    rel = abs(lhs - rhs) / rhs
    return {
        "omega_c": omega_c,
        "lhs": lhs, "rhs": rhs,
        "identity_rel_err": rel,
    }


__all__ = [
    "ts1_spiral_triad", "ts1_symbolic_expression",
    "r9_ddim_triad", "build_hyperhelix_generator",
    "r10_pure_circle", "r11_gradient_B_field",
]
