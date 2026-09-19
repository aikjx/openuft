# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R3  尺度简并与绝对尺度锚定分析（一维球对称稳态孤子）
================================================================================

承接 TUFT-R2（tuft_knot_slsqp.py）的开放问题：
    "结尺度 ~ 2.5 l_P（普朗克尺度）；若要求结尺度 ~ 电子康普顿波长
     1.5e23 l_P —— 当前模型未强制此尺度，属开放参数。"

本文件正面剖析这个 23 数量级缺口，回答一个问题：
    TUFT 的纯几何孤子方程，能否【第一性】给出电子的质量/尺度？
    还是说绝对尺度必须外部锚定（与 openuft 的 M02 普朗克锚定谬误同构）？

--------------------------------------------------------------------------------
【尺度简并的解析推导】
--------------------------------------------------------------------------------
采用与 R2 同构的简化纯指数 ansatz（无量纲 r = r_phys/l_P，K,T 已乘 l_P）：
    K(r) = k * exp(-r/L)
    T(r) = k * exp(-r/L)          # 取 Kc=Tc=k 以隔离尺度自由度
    Omega(r) = Ode + (O0-Ode)*exp(-r/L)

总能量（R2 定义，无量纲、以 E_P 为单位）：
    E_tot = 4*pi * 积分 alpha*K*T*Omega * r^2 dr
          = 4*pi*alpha * k^2 * 积分 exp(-2r/L)[Ode+(O0-Ode)exp(-r/L)] r^2 dr

令 s = r/L, dr = L ds：
    积分 = L^3 * 积分_0^inf exp(-2s)[Ode+(O0-Ode)exp(-s)] s^2 ds = L^3 * J
其中 J = 2*Ode/8 + 2*(O0-Ode)/27 是与尺度无关的【形状积分】。

于是：
    E_tot = 4*pi*alpha * k^2 * L^3 * J = E_electron（守恒约束）
  => k^2 * L^3 = E_electron/(4*pi*alpha*J) = 常数       <== 尺度简并

结论：给定 E_tot = 电子静能，只约束 k^2*L^3 = 常数，k 与 L 之间存在一个
【自由参数】。绝对尺度 L 无法由方程自身确定——必须外部注入。

--------------------------------------------------------------------------------
【两条"自然"尺度分支的数值验证】
--------------------------------------------------------------------------------
  (a) L = l_P（普朗克尺度）   => k ~ 普朗克曲率（强曲率孤子，但尺度错）
  (b) L = 电子康普顿波长      => k ~ 10^-11 m^-1（几乎平坦，与"电子=扭结"矛盾）

并检验"L=康普顿 且 k=电子曲率"能否同时满足 E_tot 约束——预期严重冲突。

--------------------------------------------------------------------------------
红线：数学自洽 != 实验证实。本文件只做尺度/量纲的诚实分析，不构成对
      TUFT 物理真实性的主张；结论是诚实边界，非证伪宣告。
================================================================================
"""

from __future__ import print_function

import os
import sys
import math

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_r3_report.txt")

# ---------------------------------------------------------------- 常数 (CODATA)
C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
OMEGA_DE = 0.6875

# 普朗克单位
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)

# 电子静能（无量纲，以 E_P 为单位）
E_ELECTRON = M_E * C_LIGHT ** 2 / E_PLANCK          # = 4.185462e-23

# 电子曲率（物理，1/m）与对应无量纲 k
KAPPA_E = M_E * C_LIGHT / HBAR                       # = 2.590e12 m^-1
K_E_DIMLESS = KAPPA_E * L_PLANCK                      # = 4.185e-23
# 电子（普通）康普顿波长，无量纲（以 l_P 为单位）
LAMBDA_C = 2.426310238e-12                            # m
L_C_DIMLESS = LAMBDA_C / L_PLANCK                      # = 1.502e23
# 普朗克曲率（物理，1/m）≈ 1/l_P
KAPPA_PLANCK = 1.0 / L_PLANCK                          # = 6.188e34 m^-1

# 形状积分（解析）
O0 = 0.72
J_ANALYTIC = 2.0 * OMEGA_DE / 8.0 + 2.0 * (O0 - OMEGA_DE) / 27.0
CONST_K2L3 = E_ELECTRON / (4.0 * math.pi * ALPHA * J_ANALYTIC)   # = k^2 * L^3


def j_numeric():
    """数值积分 J，与解析值对照（验证形状积分口径）。"""
    s = np.linspace(0.0, 60.0, 200000)
    integrand = np.exp(-2.0 * s) * (OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-s)) * s ** 2
    return float(np.trapz(integrand, s))


def k_from_L(L):
    """由尺度简并关系 k = sqrt(CONST_K2L3 / L^3) 给出满足 E_tot=E_electron 的 k。"""
    return math.sqrt(CONST_K2L3 / (L ** 3))


def etot_numeric(k, L):
    """对给定 (k, L) 数值积分 E_tot，验证守恒残差。

    改用无量纲尺度变量 s = r/L，使积分核 J_s 与 L 无关，对任意 L（含极大 L）
    都精确，避免 logspace 网格对大 L 截断导致能量低估。
        E_tot = 4*pi*alpha*k^2*L^3 * 积分_0^inf exp(-2s)[Ode+(O0-Ode)exp(-s)] s^2 ds
    """
    s = np.linspace(0.0, 60.0, 200000)
    Om = OMEGA_DE + (O0 - OMEGA_DE) * np.exp(-s)
    js = float(np.trapz(np.exp(-2.0 * s) * Om * s ** 2, s))
    return 4.0 * math.pi * ALPHA * (k ** 2) * (L ** 3) * js


def main():
    out = []
    out.append("TUFT-R3 尺度简并与绝对尺度锚定分析（一维球对称稳态孤子）")
    out.append("运行时间: " + __import__("time").strftime("%Y-%m-%d %H:%M:%S"))
    out.append("")
    out.append("【常数】 alpha=%.6e  E_electron(无量纲)=%.6e  E_P=%.6e J"
               % (ALPHA, E_ELECTRON, E_PLANCK))
    out.append("        l_P=%.6e m  电子曲率 kappa_e=%.6e m^-1  普朗克曲率=%.6e m^-1"
               % (L_PLANCK, KAPPA_E, KAPPA_PLANCK))
    out.append("        电子康普顿波长(无量纲)=%.6e l_P" % L_C_DIMLESS)
    out.append("")

    # ---------- 形状积分核对
    jnum = j_numeric()
    jerr = abs(jnum - J_ANALYTIC) / J_ANALYTIC
    out.append("=== 形状积分 J ===")
    out.append("  解析 J = %.6e   数值 J = %.6e   相对偏差 = %.3e %s"
               % (J_ANALYTIC, jnum, jerr, "[PASS]" if jerr < 1e-3 else "[FAIL]"))
    out.append("  尺度简并常数 k^2 * L^3 = %.6e（无量纲）" % CONST_K2L3)
    out.append("")

    # ---------- 尺度简并数值验证：对一组 L，解 k 并核对 E_tot
    out.append("=== 尺度简并数值验证（E_tot 守恒 vs L 自由）===")
    L_list = [1.0, 1e3, 1e8, 1e15, L_C_DIMLESS, 1e30]
    label_list = ["l_P(普朗克)", "1e3 l_P", "1e8 l_P", "1e15 l_P",
                  "电子康普顿波长", "1e30 l_P"]
    rows = []
    for L, lab in zip(L_list, label_list):
        k = k_from_L(L)
        kap = k / L_PLANCK                     # 物理曲率 1/m
        rcurv = 1.0 / kap if kap > 0 else float("inf")
        etot = etot_numeric(k, L)
        eerr = abs(etot - E_ELECTRON) / E_ELECTRON
        rows.append((lab, L, k, kap, rcurv, eerr))
        # 与电子曲率 / 普朗克曲率比较
        ratio_e = kap / KAPPA_E
        ratio_p = kap / KAPPA_PLANCK
        out.append("  L = %-14s : k(无量纲)=%.3e  曲率=%.3e m^-1  "
                   "曲率半径=%.3e m" % (lab, k, kap, rcurv))
        out.append("          曲率/电子曲率 = %.3e   曲率/普朗克曲率 = %.3e   "
                   "E_tot偏差=%.2e %s"
                   % (ratio_e, ratio_p, eerr,
                      "[PASS]" if eerr < 1e-2 else "[FAIL]"))
    out.append("")
    out.append("  观察：k ∝ L^{-3/2}，L 每增 10^15 倍，曲率降 10^22.5 倍。"
               "绝对尺度 L 是自由参数——方程自身不能确定它。")
    out.append("")

    # ---------- 两条自然分支对照
    out.append("=== 两条'自然'尺度分支 ===")
    # (a) 普朗克尺度分支
    k_planck = k_from_L(1.0)
    out.append("  (a) L=l_P  => k=%.3e (无量纲) => 曲率=%.3e m^-1（普朗克曲率量级，强曲率孤子）"
               % (k_planck, k_planck / L_PLANCK))
    # (b) 康普顿尺度分支
    k_compton = k_from_L(L_C_DIMLESS)
    out.append("  (b) L=康普顿(%.2e l_P) => k=%.3e (无量纲) => 曲率=%.3e m^-1（几乎平坦）"
               % (L_C_DIMLESS, k_compton, k_compton / L_PLANCK))
    out.append("      电子要求曲率=%.3e m^-1 => 若取此 L，几何曲率差 %.2e 倍"
               % (KAPPA_E, KAPPA_E / (k_compton / L_PLANCK)))
    out.append("      => TUFT 不能在'康普顿尺度'上给出'高曲率扭结'，二者互斥。")
    out.append("")

    # ---------- 双重约束冲突（L=康普顿 且 k=电子曲率）
    out.append("=== 双重约束冲突测试：同时强制 L=康普顿 且 k=电子曲率 ===")
    etot_both = etot_numeric(K_E_DIMLESS, L_C_DIMLESS)
    ratio = etot_both / E_ELECTRON
    kl3_both = (K_E_DIMLESS ** 2) * (L_C_DIMLESS ** 3)
    kl3_const = CONST_K2L3
    conflict = kl3_both / kl3_const
    out.append("  若 L=%.3e l_P 且 k=%.3e（电子曲率）:" % (L_C_DIMLESS, K_E_DIMLESS))
    out.append("      k^2*L^3 = %.3e，而守恒要求 k^2*L^3 = %.3e"
               % (kl3_both, kl3_const))
    out.append("      偏差 = %.3e 倍（解析，等价于 E_tot 偏离 %.3e 倍）"
               % (conflict, conflict))
    out.append("      [数值核对] E_tot = %.3e（应为 %.3e）比值 = %.3e %s"
               % (etot_both, E_ELECTRON, ratio,
                  "[PASS]" if abs(math.log10(ratio) - math.log10(conflict)) < 1 else "[CHECK]"))
    out.append("  => 守恒律、'电子尺度'、'电子曲率'三者三角冲突：纯几何方程无法同时")
    out.append("     满足后两者；若强制 L=康普顿，守恒必迫 k=8.8e-46（平坦），非电子曲率。")
    out.append("  => 纯几何孤子【无法】第一性导出电子的绝对尺度与曲率；二者必须外部锚定。")
    out.append("")

    # ---------- 与 M02 同构性
    out.append("=== 与 openuft M02（普朗克锚定谬误）的同构性 ===")
    out.append("  M02：G=c^3/(hbar(κ^2+τ^2)) 与 m=hbar√(κ^2+τ^2)/c 联立 => 必推 m=m_P。")
    out.append("  R3  ：E_tot=4π α k^2 L^3 J 约束 k^2 L^3=const => 自然产出普朗克尺度；")
    out.append("        要落到电子尺度，必须额外注入 23 数量级（= λ_C/l_P 的 3/2 次方量级）。")
    out.append("  二者同构：纯几何/纯量纲方程无尺度锚，自然锁定在普朗克尺度；")
    out.append("  电子质量与尺度的绝对数值非第一性导出，须外部锚定（如 α_grav=(m/m_P)^2 修正）。")
    out.append("")

    # ---------- 诚实结论
    out.append("=== 诚实结论（开放项 O-SCALE）===")
    out.append("  1. TUFT 球对称稳态孤子存在尺度简并 k^2*L^3=const：绝对尺度 L 是自由参数。")
    out.append("  2. 自然解落在普朗克尺度（强曲率），但电子要求康普顿尺度+高曲率，二者互斥；")
    out.append("     同时强制二者破坏能量守恒 10^45 倍。")
    out.append("  3. 故 TUFT【不能】第一性给出电子质量/尺度的绝对数值，必须外部锚定。")
    out.append("  4. 这与 M02 普朗克锚定谬误同构，是 TUFT 的诚实边界，非证伪宣告；")
    out.append("     若要闭合，需引入能打破 k^2*L^3 简并的新机制（额外场/耦合/宇宙学标定）。")
    out.append("")
    out.append("红线声明：数学自洽 != 实验证实。本文件仅做尺度/量纲的诚实分析，")
    out.append("          不构成对 TUFT 物理真实性的任何主张。")

    text = "\n".join(out) + "\n"
    print(text)
    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write(text)
        out.append("[OK] 报告已写入 " + REPORT_PATH)
    except Exception as exc:
        print("[warn] 报告写入失败: " + str(exc))


if __name__ == "__main__":
    main()
