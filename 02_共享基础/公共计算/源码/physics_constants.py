# physics.py — 物理常数（CODATA2022 / PDG2024 字面量）
#
# AI科技星 · openuft · 三重奏统一场
# 所有常数以字面量给出（不使用 ${} 占位符，符合项目全局约束）。
# 单位：SI（米·千克·秒·安培·开尔文）。

# ---- 定义常数（CODATA2022 精确/推荐值）----
SPEED_OF_LIGHT = 299792458.0            # c [m/s]，精确值
PLANCK = 6.62607015e-34                 # h [J·s]，精确值
REDUCED_PLANCK = 1.054571817e-34        # hbar = h/(2*pi) [J·s]
ELEMENTARY_CHARGE = 1.602176634e-19     # e [C]，精确值
NEWTON_G = 6.67430e-11                  # G [m^3 kg^-1 s^-2]
VACUUM_PERMITTIVITY = 8.8541878128e-12  # epsilon0 [F/m]
VACUUM_PERMEABILITY = 1.25663706212e-6  # mu0 = 4*pi*1e-7 [N/A^2]
BOLTZMANN = 1.380649e-23                # k_B [J/K]，精确值
ELECTRON_MASS = 9.1093837015e-31        # m_e [kg]
PROTON_MASS = 1.67262192369e-27         # m_p [kg]
FINE_STRUCTURE = 7.2973525693e-3        # alpha = e^2/(4*pi*eps0*hbar*c) [无量纲]

# ---- 派生常数（由定义常数计算，用于回标 CODATA）----
import math


def planck_length():
    """l_P = sqrt(hbar * G / c^3)"""
    return math.sqrt(REDUCED_PLANCK * NEWTON_G / (SPEED_OF_LIGHT ** 3))


def planck_time():
    """t_P = l_P / c"""
    return planck_length() / SPEED_OF_LIGHT


def planck_mass():
    """m_P = sqrt(hbar * c / G)"""
    return math.sqrt(REDUCED_PLANCK * SPEED_OF_LIGHT / NEWTON_G)


def fine_structure_computed():
    """alpha = e^2 / (4*pi*eps0*hbar*c)"""
    return (ELEMENTARY_CHARGE ** 2) / (
        4.0 * math.pi * VACUUM_PERMITTIVITY * REDUCED_PLANCK * SPEED_OF_LIGHT
    )


def hubble_radius(h0_kms_mpc=67.4):
    """哈勃半径 R_H = c / H0。h0 单位 km/s/Mpc。"""
    h0_si = h0_kms_mpc * 1000.0 / (3.0856775814913673e22)  # Mpc -> m
    return SPEED_OF_LIGHT / h0_si


# ---- CODATA2022 参考值（用于回标验证，非定义值）----
CODATA_PLANCK_LENGTH = 1.616255e-35     # [m]
CODATA_PLANCK_MASS = 2.176434e-8        # [kg]
CODATA_PLANCK_TIME = 5.391247e-44       # [s]
CODATA_FINE_STRUCTURE = 7.2973525628e-3  # [无量纲]

# ---- 标准模型实验质量（PDG2024，单位 kg）----
MASS_MUON = 1.883531627e-28
MASS_TAU = 3.16754e-27
MASS_W = 80.379e9 * ELEMENTARY_CHARGE / (SPEED_OF_LIGHT ** 2)   # M_W = 80.379 GeV/c^2
MASS_Z = 91.1876e9 * ELEMENTARY_CHARGE / (SPEED_OF_LIGHT ** 2)  # M_Z = 91.1876 GeV/c^2

# ---- 地球（用于 TS4 牛顿引力回标）----
EARTH_MASS = 5.9722e24        # [kg]
EARTH_RADIUS = 6.371e6        # [m]
EARTH_G = NEWTON_G * EARTH_MASS / (EARTH_RADIUS ** 2)  # 标称 g ≈ 9.82 [m/s^2]

# ---- 太阳（TS10 黑洞熵参考）----
SOLAR_MASS = 1.98847e30       # [kg]

__all__ = [
    "SPEED_OF_LIGHT", "PLANCK", "REDUCED_PLANCK", "ELEMENTARY_CHARGE",
    "NEWTON_G", "VACUUM_PERMITTIVITY", "VACUUM_PERMEABILITY", "BOLTZMANN",
    "ELECTRON_MASS", "PROTON_MASS", "FINE_STRUCTURE",
    "planck_length", "planck_time", "planck_mass", "fine_structure_computed",
    "hubble_radius", "CODATA_PLANCK_LENGTH", "CODATA_PLANCK_MASS",
    "CODATA_PLANCK_TIME", "CODATA_FINE_STRUCTURE",
    "MASS_MUON", "MASS_TAU", "MASS_W", "MASS_Z",
    "EARTH_MASS", "EARTH_RADIUS", "EARTH_G", "SOLAR_MASS",
]
