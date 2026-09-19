# -*- coding: utf-8 -*-
"""
triad_uft.constants — CODATA 2022 物理常数
==========================================
250位 mpmath 高精度 + float64 双精度。
误差传播：δG=2.2e-5 → 派生量 δ=½δG=1.1e-5。
来源：CODATA 2022 recommended values。
"""
import mpmath as mp

mp.mp.dps = 250

# ===== 基本常数（CODATA 2022）=====
C = mp.mpf("299792458")                           # 光速 m/s（精确）
HBAR = mp.mpf("1.054571817e-34")                  # 约化普朗克常数 J·s（精确）
E_CHARGE = mp.mpf("1.602176634e-19")              # 元电荷 C（精确）
G = mp.mpf("6.67430e-11")                          # 引力常数 m³/(kg·s²)
G_REL_ERROR = mp.mpf("2.2e-5")                    # G的相对不确定度
ELECTRON_MASS = mp.mpf("9.1093837015e-31")        # 电子质量 kg
PROTON_MASS = mp.mpf("1.67262192369e-27")         # 质子质量 kg
NEUTRON_MASS = mp.mpf("1.67492749804e-27")        # 中子质量 kg
FINE_STRUCTURE = mp.mpf("7.2973525693e-3")        # 精细结构常数
BOHR_MAGNETON = mp.mpf("9.2740100783e-24")        # 玻尔磁子 J/T
FERMI_CONSTANT = mp.mpf("1.1663787e-5")           # 费米常数 GeV⁻²
HIGGS_VEV = (mp.mpf("2") * FERMI_CONSTANT / mp.sqrt(mp.mpf("2"))) ** mp.mpf("-0.5")  # ~246 GeV

# 电子荷质比（电子带负电，q/m 为负）
ELECTRON_CHARGE = -E_CHARGE                           # 电子电荷 C
ELECTRON_QM = ELECTRON_CHARGE / ELECTRON_MASS         # C/kg ≈ -1.75882e11

# ===== Planck 单位 =====
PLANCK_LENGTH = mp.sqrt(HBAR * G / C**3)          # ℓ_P ≈ 1.616e-35 m
PLANCK_TIME = mp.sqrt(HBAR * G / C**5)            # t_P ≈ 5.391e-44 s
PLANCK_MASS = mp.sqrt(HBAR * C / G)               # M_P ≈ 2.176e-8 kg
PLANCK_ENERGY = PLANCK_MASS * C**2                # E_P ≈ 1.956e9 J
PLANCK_TEMP = PLANCK_ENERGY / mp.mpf("1.380649e-23")  # T_P ≈ 1.417e32 K
PLANCK_DENSITY = PLANCK_MASS / PLANCK_LENGTH**3   # ρ_P ≈ 5.155e96 kg/m³

# 电弱
SIN2_THETA_W = mp.mpf("0.23122")                   # 弱混合角平方
ALPHA_EM_INV = mp.mpf("127.9")                     # 1/α_em (M_Z)
ALPHA_S = mp.mpf("0.1179")                         # 强耦合 (M_Z)
M_W = mp.mpf("80.377")                             # W玻色子质量 GeV
M_Z = mp.mpf("91.1876")                            # Z玻色子质量 GeV
M_HIGGS = mp.mpf("125.1")                          # 希格斯质量 GeV


def to_float64(mp_val):
    """mpmath值转float64"""
    return float(mp_val)


def planck_units():
    """返回Planck单位字典（float64）"""
    return {
        "length": to_float64(PLANCK_LENGTH),
        "time": to_float64(PLANCK_TIME),
        "mass": to_float64(PLANCK_MASS),
        "energy": to_float64(PLANCK_ENERGY),
        "temperature": to_float64(PLANCK_TEMP),
        "density": to_float64(PLANCK_DENSITY),
    }


def relative_error(quantity="derived"):
    """G的误差传播：派生量含G^(1/2)时 δ=½δG"""
    return float(G_REL_ERROR) / 2.0
