# frenet.py — Frenet-Serret 曲率/挠率（解析 + 数值高精度）
#
# 算法联盟 · openuft · triad_uft
# 提供：
#   - curvature_torsion_helix(R, omega, b)：解析曲率/挠率（匀速螺旋）
#   - numerical_curvature_torsion(curve, t, dps)：mpmath 四阶差分数值估计
#   - sample_helix(R, omega, b, t)：返回螺旋曲线点

import mpmath as mp


def curvature_torsion_helix(R, omega, b):
    """匀速螺旋 r(t)=(R cos wt, R sin wt, b t) 的解析曲率/挠率。

    标准 Frenet 结果（参数无关）：
        kappa = R * omega^2 / v^2,   tau = b * omega / v^2
        v^2 = R^2 omega^2 + b^2
    满足恒等式  kappa^2 + tau^2 = (omega / v)^2   （TS1 / R4）。
    """
    v2 = R * R * omega * omega + b * b
    v = mp.sqrt(v2)
    kappa = R * omega * omega / v2
    tau = b * omega / v2
    return kappa, tau, v


def sample_helix(R, omega, b, t):
    """螺旋曲线在参数 t 处的坐标。t 可为 mp.mpf。"""
    ct = mp.cos(omega * t)
    st = mp.sin(omega * t)
    return mp.matrix([R * ct, R * st, b * t])


def _deriv(curve, t, dps, order=3):
    """中心差分估计 curve 在 t 处的 1~3 阶导数。"""
    mp.mp.dps = dps
    h = mp.mpf(10) ** (-(dps // 3))  # 步长随精度增长
    r1 = (curve(t + h) - curve(t - h)) / (2 * h)
    r2 = (curve(t + h) - 2 * curve(t) + curve(t - h)) / (h * h)
    r3 = (curve(t + 2 * h) - 2 * curve(t + h) + 2 * curve(t - h) - curve(t - 2 * h)) / (2 * h ** 3)
    return r1, r2, r3


def numerical_curvature_torsion(curve, t, dps=50):
    """由 Frenet 公式数值估计曲率/挠率。

    kappa = |r' x r''| / |r'|^3
    tau   = (r' x r'') . r''' / |r' x r''|^2
    """
    mp.mp.dps = dps
    r1, r2, r3 = _deriv(curve, t, dps)
    cross = mp.matrix([
        r1[1] * r2[2] - r1[2] * r2[1],
        r1[2] * r2[0] - r1[0] * r2[2],
        r1[0] * r2[1] - r1[1] * r2[0],
    ])
    rp = mp.sqrt(r1[0] ** 2 + r1[1] ** 2 + r1[2] ** 2)
    cross_norm = mp.sqrt(cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2)
    kappa = cross_norm / (rp ** 3)
    dot = cross[0] * r3[0] + cross[1] * r3[1] + cross[2] * r3[2]
    tau = dot / (cross_norm ** 2)
    return kappa, tau


__all__ = [
    "curvature_torsion_helix", "sample_helix",
    "numerical_curvature_torsion",
]
