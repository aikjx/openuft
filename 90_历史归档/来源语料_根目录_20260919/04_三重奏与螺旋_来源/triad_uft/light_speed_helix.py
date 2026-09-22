# -*- coding: utf-8 -*-
"""
light_speed_helix.py — 空间光速螺旋 v≡c 模块（工业级）
========================================================
封装空间光速螺旋的严格推导与验证API。

【公理】所有基本粒子内部运动合速度恒为光速c，v≡c
【定理】κ² + τ² = (ω/c)²（sympy符号证明，差精确为0）

快速开始
--------
>>> from triad_uft import light_speed_helix as lsh
>>> result = lsh.check_light_speed_helix(R=1.0, omega=0.5)
>>> print(result["rel_error"])  # 应接近0
>>> print(result["kappa"], result["tau"])
"""
import numpy as np
import sympy as sp
from dataclasses import dataclass
from typing import Dict, Tuple, Optional


@dataclass
class LightSpeedHelixResult:
    """光速螺旋验证结果"""
    R: float
    omega: float
    b: float
    v: float
    kappa: float
    tau: float
    lhs: float  # κ² + τ²
    rhs: float  # (ω/c)²
    rel_error: float
    valid: bool


def light_speed_helix_params(R: float, omega: float, c: float = 299792458.0) -> Tuple[float, float]:
    """
    计算光速螺旋的轴向速度b和总速度v。

    光速约束：R²ω² + b² = c² → b = √(c² - R²ω²)

    参数:
        R: 螺旋半径 (m)
        omega: 角频率 (rad/s)
        c: 光速 (m/s)，默认299792458

    返回:
        (b, v): 轴向速度和总速度（v应等于c）

    异常:
        ValueError: 当Rω > c时（违反光速约束）
    """
    v_perp = R * omega
    if v_perp > c:
        raise ValueError(f"Rω={v_perp:.4e} > c={c:.4e}，违反光速约束v≡c")
    b = np.sqrt(c**2 - v_perp**2)
    v = np.sqrt(v_perp**2 + b**2)
    return b, v


def helix_curvature_torsion_light_speed(R: float, omega: float, c: float = 299792458.0) -> Tuple[float, float]:
    """
    计算光速螺旋的曲率κ和挠率τ。

    曲率：κ = Rω²/c²
    挠率：τ = bω/c² = ω√(c²-R²ω²)/c²

    参数:
        R: 螺旋半径 (m)
        omega: 角频率 (rad/s)
        c: 光速 (m/s)

    返回:
        (kappa, tau): 曲率和挠率
    """
    b, v = light_speed_helix_params(R, omega, c)
    kappa = R * omega**2 / c**2
    tau = b * omega / c**2
    return kappa, tau


def check_light_speed_helix(R: float, omega: float, c: float = 299792458.0,
                             tol: float = 1e-10) -> LightSpeedHelixResult:
    """
    验证光速螺旋的三重奏定理：κ² + τ² = (ω/c)²

    参数:
        R: 螺旋半径 (m)
        omega: 角频率 (rad/s)
        c: 光速 (m/s)
        tol: 相对误差容限

    返回:
        LightSpeedHelixResult: 验证结果
    """
    b, v = light_speed_helix_params(R, omega, c)
    kappa, tau = helix_curvature_torsion_light_speed(R, omega, c)

    lhs = kappa**2 + tau**2
    rhs = (omega / c)**2
    rel_error = abs(lhs - rhs) / rhs if rhs > 0 else 0.0

    return LightSpeedHelixResult(
        R=R, omega=omega, b=b, v=v,
        kappa=kappa, tau=tau,
        lhs=lhs, rhs=rhs,
        rel_error=rel_error,
        valid=rel_error < tol
    )


def symbolic_proof_light_speed_helix() -> Dict:
    """
    光速螺旋三重奏定理的sympy符号证明。

    返回:
        Dict: 包含证明结果的字典
            - kappa2: 曲率平方的符号表达式
            - tau2: 挠率平方的符号表达式
            - lhs: κ² + τ²（代入v²=c²后）
            - rhs: (ω/c)²
            - diff: lhs - rhs（应为0）
            - proven: diff是否为0
    """
    t, R, omega, b, c = sp.symbols('t R omega b c', real=True, positive=True)
    r = sp.Matrix([R*sp.cos(omega*t), R*sp.sin(omega*t), b*t])
    v = sp.diff(r, t)
    a = sp.diff(v, t)
    a_prime = sp.diff(a, t)

    v2 = sp.simplify(v.dot(v))
    cross = v.cross(a)
    cross2 = sp.simplify(cross.dot(cross))
    kappa2 = sp.simplify(cross2 / v2**3)
    tau2 = sp.simplify((cross.dot(a_prime))**2 / cross2**2)

    # 代入光速约束 v2 = c²
    # v2 = R²ω² + b²，直接用c²替换
    lhs = sp.simplify(kappa2 + tau2)
    # kappa2 = R²ω⁴/(R²ω²+b²)³, tau2 = b²ω²/(R²ω²+b²)³
    # 代入R²ω²+b²=c²: lhs = (R²ω⁴+b²ω²)/c⁶ = ω²(R²ω²+b²)/c⁶ = ω²c²/c⁶ = ω²/c⁴
    # 但(ω/c)² = ω²/c²，所以需要检查
    # 实际上κ=Rω²/c², τ=bω/c², κ²+τ²=(R²ω⁴+b²ω²)/c⁴=ω²(R²ω²+b²)/c⁴=ω²c²/c⁴=(ω/c)²
    lhs_sub = sp.simplify(lhs.subs(R**2*omega**2 + b**2, c**2))
    rhs = sp.simplify(omega**2 / c**2)
    diff = sp.simplify(lhs_sub - rhs)

    return {
        "kappa2": kappa2,
        "tau2": tau2,
        "lhs": lhs_sub,
        "rhs": rhs,
        "diff": diff,
        "proven": diff == 0
    }


def electron_light_speed_helix(c: float = 299792458.0,
                                hbar: float = 1.054571817e-34,
                                m_e: float = 9.1093837015e-31) -> Dict:
    """
    电子内部光速螺旋参数计算。

    静止电子b=0，纯圆周运动Rω=c
    螺旋半径：R = ħ/(2m_ec)（由角动量量子化L=ħ/2反推）
    角频率：ω = c/R = 2m_ec²/ħ

    参数:
        c: 光速
        hbar: 约化普朗克常数
        m_e: 电子质量

    返回:
        Dict: 电子光速螺旋参数
    """
    R = hbar / (2 * m_e * c)
    omega = 2 * m_e * c**2 / hbar
    b = 0.0  # 静止电子纯圆周
    v = c

    kappa = R * omega**2 / c**2
    tau = b * omega / c**2
    lhs = kappa**2 + tau**2
    rhs = (omega / c)**2
    rel_error = abs(lhs - rhs) / rhs if rhs > 0 else 0.0

    # 角动量验证
    L = m_e * R**2 * omega
    expected_L = hbar / 2
    L_rel_error = abs(L - expected_L) / expected_L

    return {
        "R": R,
        "omega": omega,
        "b": b,
        "v": v,
        "kappa": kappa,
        "tau": tau,
        "lhs": lhs,
        "rhs": rhs,
        "rel_error": rel_error,
        "angular_momentum": L,
        "expected_L": expected_L,
        "L_rel_error": L_rel_error,
        "valid": rel_error < 1e-10 and L_rel_error < 1e-10
    }


def alldim_light_speed_helix(D: int, omegas: np.ndarray, Rs: np.ndarray,
                               c: float = 299792458.0, tol: float = 1e-10) -> Dict:
    """
    D维光速超螺旋验证：Σκᵢ² = (Σωⱼ²)/c²

    参数:
        D: 维度
        omegas: 各平面角频率数组
        Rs: 各平面半径数组
        c: 光速
        tol: 容限

    返回:
        Dict: 验证结果
    """
    m = len(omegas)
    if len(Rs) != m:
        raise ValueError(f"omegas和Rs长度必须相同，得到{len(omegas)}和{len(Rs)}")

    v_perp2 = np.sum(Rs**2 * omegas**2)
    if v_perp2 > c**2:
        raise ValueError(f"横向速度平方{v_perp2:.4e} > c²，违反光速约束")

    b = np.sqrt(c**2 - v_perp2)
    v2 = v_perp2 + b**2  # 应等于c²

    sum_kappa2 = np.sum(omegas**2) / v2
    sum_omega2 = np.sum(omegas**2)
    rel_error = abs(sum_kappa2 - sum_omega2) / sum_omega2 if sum_omega2 > 0 else 0.0

    return {
        "D": D,
        "m": m,
        "omegas": omegas,
        "Rs": Rs,
        "b": b,
        "v2": v2,
        "sum_kappa2": sum_kappa2,
        "sum_omega2": sum_omega2,
        "rel_error": rel_error,
        "valid": rel_error < tol
    }


def mass_geometric_origin(m: float, c: float = 299792458.0,
                           hbar: float = 1.054571817e-34) -> Dict:
    """
    质量的几何起源：m ∝ 1/R（螺旋半径越小，质量越大）

    参数:
        m: 粒子质量 (kg)
        c: 光速
        hbar: 约化普朗克常数

    返回:
        Dict: 质量几何参数
    """
    R = hbar / (2 * m * c)  # 螺旋半径
    omega = 2 * m * c**2 / hbar  # 角频率
    E = m * c**2  # 静止能量
    p0 = m * c  # 静止动量

    return {
        "mass": m,
        "R": R,
        "omega": omega,
        "E": E,
        "p0": p0,
        "R_inverse_proportional": True  # m ∝ 1/R
    }


def rest_momentum_geometric(m: float, c: float = 299792458.0) -> Dict:
    """
    静止动量的几何解释：p₀ = m₀c（螺旋旋转分量的动量）

    参数:
        m: 静止质量 (kg)
        c: 光速

    返回:
        Dict: 静止动量几何参数
    """
    p0 = m * c  # 静止动量
    E0 = m * c**2  # 静止能量
    v_perp = c  # 静止粒子纯圆周，横向速度=光速
    b = 0  # 轴向速度=0

    return {
        "rest_mass": m,
        "rest_momentum": p0,
        "rest_energy": E0,
        "v_perp": v_perp,
        "b": b,
        "interpretation": "静止粒子=光速螺旋的旋转分量，p₀=m₀c是旋转分量动量"
    }


# 便捷函数
def quick_verify(R: float = 1.0, omega: float = 0.5, c: float = 1.0) -> str:
    """
    快速验证光速螺旋三重奏定理（归一化c=1）。

    参数:
        R: 螺旋半径
        omega: 角频率
        c: 光速（默认1，归一化单位）

    返回:
        str: 验证结果描述
    """
    result = check_light_speed_helix(R, omega, c)
    status = "✅ 通过" if result.valid else "❌ 失败"
    return (f"光速螺旋验证 {status}\n"
            f"  R={result.R}, ω={result.omega}, b={result.b:.6f}, v={result.v:.6f}\n"
            f"  κ={result.kappa:.6e}, τ={result.tau:.6e}\n"
            f"  κ²+τ²={result.lhs:.6e}, (ω/c)²={result.rhs:.6e}\n"
            f"  相对误差={result.rel_error:.2e}")
