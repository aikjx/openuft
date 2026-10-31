# -*- coding: utf-8 -*-
"""r257 开发期探针 v2：视界热力学恒等式与量级核对（不产出交付物）。

要点：
1) S/k_B 双路径（πc⁵/(GħH²) vs A/(4ℓ_P²)，A=4πr_A²）、T 双路径（ħH/2πk_B vs ħc/(2πk_B r_A)）恒等性
2) 精确第一定律：T dS/dz = 2 dE_MS/dz（E_MS = ρc²V = c⁵/(2GH)，即视界处 Misner-Sharp 质量）
3) 朴素 p dV 形式 T dS = dE + p dV（p = p_r + p_Λ）的残差比 —— 预期不闭合
4) 第二定律 dS/dt > 0；纯 de Sitter 极限 dS/dt = 0；S_∞ = S0/ΩΛ
5) S 对 H0 的标度（H0×1.10 ⇒ S 比值 1/1.21）
"""
import sys
from math import sqrt, pi, log

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054571817e-34
KB = 1.380649e-23
MPC = 3.0856775814913673e22
H0_KM = 67.4
H0 = H0_KM * 1000.0 / MPC
OM = 0.3153
OR = 9.15e-5
OL = 1.0 - OM - OR
RHOC = 3.0 * H0 ** 2 / (8.0 * pi * G)
LP2 = HBAR * G / C ** 3
T_CMB = 2.7255


def Ez2(z, om=OM, orr=OR, ol=OL):
    return om * (1 + z) ** 3 + orr * (1 + z) ** 4 + ol


def H(z, om=OM, orr=OR, ol=OL, h0=H0):
    return h0 * sqrt(Ez2(z, om, orr, ol))


def Hp(z, om=OM, orr=OR, ol=OL, h0=H0):
    """dH/dz 解析（Ωr 项保留）。"""
    num = 0.5 * (3.0 * om * (1 + z) ** 2 + 4.0 * orr * (1 + z) ** 3) * h0 ** 2
    return num / H(z, om, orr, ol, h0)


def rho(z, om=OM, orr=OR, ol=OL, h0=H0):
    return 3.0 * h0 ** 2 / (8.0 * pi * G) * Ez2(z, om, orr, ol)


def p_tot(z, om=OM, orr=OR, ol=OL, h0=H0):
    """总压（含 c²）：辐射 p=ρ_r c²/3，Λ 的 p=−ρ_Λ c²，物质 0。"""
    rc = 3.0 * h0 ** 2 / (8.0 * pi * G)
    return (1.0 / 3.0) * rc * orr * (1 + z) ** 4 * C ** 2 - rc * ol * C ** 2


def rA(z, **kw):
    return C / H(z, **kw)


def S_kB(z, **kw):
    return pi * C ** 5 / (G * HBAR * H(z, **kw) ** 2)


def S_kB_area(z, **kw):
    A = 4.0 * pi * rA(z, **kw) ** 2
    return A / (4.0 * LP2)


def T_GH(z, **kw):
    return HBAR * H(z, **kw) / (2.0 * pi * KB)


def T_GH_area(z, **kw):
    return HBAR * C / (2.0 * pi * KB * rA(z, **kw))


def V(z, **kw):
    return 4.0 / 3.0 * pi * rA(z, **kw) ** 3


def E_J(z, **kw):
    return rho(z, **kw) * C ** 2 * V(z, **kw)


def dSdz_analytic(z, **kw):
    # S/kB = πc⁵/(GħH²) ⇒ dS/dz = −2πc⁵H'/(GħH³)
    return -2.0 * pi * C ** 5 * Hp(z, **kw) / (G * HBAR * H(z, **kw) ** 3)


def dEdz_analytic(z, **kw):
    # E = ρc²V = c⁵/(2GH) ⇒ dE/dz = −c⁵H'/(2GH²)
    return -C ** 5 * Hp(z, **kw) / (2.0 * G * H(z, **kw) ** 2)


def first_law_res(z, **kw):
    """T dS/dz 与 2 dE/dz 的相对残差（用解析导数）。"""
    lhs = KB * T_GH(z, **kw) * dSdz_analytic(z, **kw)
    rhs = 2.0 * dEdz_analytic(z, **kw)
    return abs(lhs - rhs) / max(abs(lhs), abs(rhs))


def naive_res(z, **kw):
    """朴素形式 T dS = dE + p dV 的残差比（解析导数）。"""
    h = 1e-6
    dV = (V(z + h, **kw) - V(z - h, **kw)) / (2 * h)
    lhs = KB * T_GH(z, **kw) * dSdz_analytic(z, **kw)
    rhs = dEdz_analytic(z, **kw) + p_tot(z, **kw) * dV
    return lhs, rhs, abs(lhs - rhs) / max(abs(lhs), abs(rhs))


def dSdt_sign(z, **kw):
    """dS/dt = dS/dz · dz/dt，dz/dt = −(1+z)H。返回 d(S/kB)/dt。"""
    return dSdz_analytic(z, **kw) * (-(1 + z) * H(z, **kw))


print("== 1) 双路径恒等 ==")
for z in [0.0, 1.0, 5.0]:
    a, b = S_kB(z), S_kB_area(z)
    print(f"z={z:4.1f} S/kB  πc5/GhH2={a:.10e}  A/4lP2={b:.10e}  rel={abs(a-b)/a:.3e}")
    ta, tb = T_GH(z), T_GH_area(z)
    print(f"        T     hH/2pikB={ta:.6e}  hc/2pikB rA={tb:.6e}  rel={abs(ta-tb)/ta:.3e}")

print("\n== 2) 精确第一定律 T dS = 2 dE_MS ==")
for z in [0.0, 0.3, 1.0, 2.0, 5.0, 10.0]:
    lhs = KB * T_GH(z) * dSdz_analytic(z)
    rhs = 2.0 * dEdz_analytic(z)
    print(f"z={z:5.2f} TdS/dz={lhs:.6e} J   2dE/dz={rhs:.6e} J   rel={first_law_res(z):.3e}")

print("\n== 3) 朴素 p dV 形式残差（预期不闭合）==")
for z in [0.0, 1.0, 2.0, 5.0]:
    l, r, rel = naive_res(z)
    print(f"z={z:4.1f} TdS/dz={l:.4e}  dE/dz+pdV/dz={r:.4e}  ratio={r/l:.4f}  rel={rel:.3e}")

print("\n== 4) 第二定律 / de Sitter 极限 / 标度 ==")
for z in [0.0, 1.0, 5.0, 10.0]:
    print(f"z={z:4.1f} d(S/kB)/dt={dSdt_sign(z):.4e} /s (>0 ?)")
print("pure dS (Om=0,Or=0): H(z)=", H(0.0, om=0.0, orr=0.0, ol=1.0), " dS/dt=",
      dSdz_analytic(0.0, om=0.0, orr=0.0, ol=1.0)
      * (-(1 + 0.0) * H(0.0, om=0.0, orr=0.0, ol=1.0)))
print("S_inf/kB = S0/OL =", S_kB(0.0) / OL)
h10 = 1.10
print("H0*1.10: S ratio =", S_kB(0.0, h0=H0 * h10) / S_kB(0.0), " expect", 1 / h10 ** 2,
      " T ratio =", T_GH(0.0, h0=H0 * h10) / T_GH(0.0))

print("\n== 5) 量级 ==")
print("T0 =", T_GH(0.0), "K;  T_GH/T_CMB =", T_GH(0.0) / T_CMB)
print("S0/kB =", S_kB(0.0), " log10 =", log(S_kB(0.0), 10))
S_dS = 3.0 * pi * C ** 3 / (G * HBAR * (3.0 * H0 ** 2 / C ** 2))
print("S_dS/kB (form 3πc3/GħΛ) =", S_dS, " vs S0/OL =", S_kB(0.0) / OL)
print("r_A0 =", rA(0.0), "m =", rA(0.0) / MPC, "Mpc")
print("E_MS0 =", E_J(0.0), "J")
# 光子熵（今日）
A_RAD = 7.5657e-16  # J m^-3 K^-4
s_gamma = (4.0 / 3.0) * A_RAD * T_CMB ** 3  # J/(m^3 K) 熵密度
s_gamma_n = s_gamma / KB  # k_B/m^3
print("s_gamma/kB =", s_gamma_n, " /m3  (s/n =", s_gamma_n / 4.107e8, ")")
print("S_matter/kB in horizon =", s_gamma_n * V(0.0), " ratio to S_h =",
      s_gamma_n * V(0.0) / S_kB(0.0))
