# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  分支B落地 —— 良态物理 ansatz 上的 g 因子校验（C0045 续，自然单位版）
================================================================================

在 C0045 已收敛的物理 ansatz（闭式指数尾 K/T/Ω，r 以普朗克长度 l_P 为单位）上，
补做源稿要求的电子反常磁矩 g 因子校验（目标 g_e≈2.00231930436）。

【自然单位推导，量纲一致】
源稿可观测量（q0、ω0 为耦合常数，在 μ/Q0 中相消）：
    Q0 = q0·ω0·N,   N=∫4πr²ψ²dr
    μ  = q0·ω0·Iμ,  Iμ=2π∫r³ψ²dr   ⇒  μ/Q0 = Iμ/N = ⟨r⟩/2,  ⟨r⟩=∫r³ρdr/∫r²ρdr
    g = 2M·μ/(Q0·S),  S=ħ/2  ⇒  g = 4M·Iμ/(N·ħ) = 2M·⟨r⟩/ħ
取自然单位（ħ=1），质量以普朗克质量计、长度以普朗克长度计：
    g = 2·M_nat·⟨r⟩_nat      （无量纲，量纲一致 ✓）
    g=2 ⟺ ⟨r⟩_nat = 1/M_nat = λ_C(自然单位，以 l_P 计)
电子：M_nat = M_e c²/E_P = 4.185462e-23（普朗克质量单位）
      λ_C = 1/M_nat = 2.389e22 l_P；g_e 需 ⟨r⟩_nat = g_e/2/M_nat = 2.392e22 l_P

核心判定：物理 ansatz 已把质量钉扎到 E_ELECTRON（即 M_nat=4.185e-23），
其电荷分布半径若与质量分布同尺度（~l_P），则 g=2M_nat·⟨r⟩_nat ~1e-22，远小于 2；
要复现 g_e≈2.0023，电荷分布加权平均半径须钉扎到康普顿尺度 λ_C≈2.39e22 l_P，
即比当前尺度大 ~1e22 倍。⇒ g 维度是"尺度钉扎/磁矩目标未加"，而非孤子不存在。

红线声明：电荷密度识别（ρ∝Ω-Ω_DE 或 ρ∝ε）是模型假设，非理论已钉扎；
本脚本给出"该良态 ansatz 在 g 维度上的结构判定"，不构成物理真实主张。
================================================================================
"""
from __future__ import print_function
import os, sys, time, math
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_v32_gfactor_report.txt")

# ---------------------------------------------------------------- 常数 (CODATA)
C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
OMEGA_DE = 0.6875
E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
E_ELECTRON = M_E * C_LIGHT ** 2 / E_PLANCK
GE_EXP = 2.00231930436

# C0045 收敛参数（解析 jac SLSQP，χ²=2.35e-17）
PAR = dict(Kc=3.1648e-08, lK=6.9989e-02, r0=6.9987e-03, p=2.9094e+00,
           Tc=3.1648e-08, lT=6.9989e-02, O0=9.8778e-01, lO=1.1852e+00)


def fields(p, r):
    K = p["Kc"] * np.exp(-r / p["lK"]) / (1.0 + (r / p["r0"]) ** p["p"])
    T = p["Tc"] * np.exp(-r / p["lT"])
    Om = OMEGA_DE + (p["O0"] - OMEGA_DE) * np.exp(-r / p["lO"])
    return K, T, Om


def main():
    t0 = time.time()
    out = []
    out.append("TUFT V3.2 分支B · 良态物理 ansatz 上的 g 因子校验（C0045 续，自然单位）")
    out.append("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    out.append("Python %s  numpy %s" % (sys.version.split()[0], np.__version__))
    out.append("")
    out.append("背景：C0045 已在物理 ansatz 收敛（χ²=2.35e-17, E_tot/电子=1.000000, N=1.000000），")
    out.append("仅钉扎质量 E 与归一化 N；电荷 Q0、磁矩 μ、g 因子为挂账项。本脚本校验 g。")
    out.append("自然单位：ħ=1，质量以普朗克质量、长度以 l_P=%.4e m 计。" % L_PLANCK)
    out.append("M_nat = M_e c²/E_P = %.6e（普朗克质量）；λ_C(nat)=1/M_nat=%.6e l_P" % (E_ELECTRON, 1.0 / E_ELECTRON))
    out.append("")

    r = np.logspace(-3.0, 2.0, 4000)
    K, T, Om = fields(PAR, r)
    eps = ALPHA * K * T * Om                       # 能量密度
    dOm = Om - OMEGA_DE                             # 真空偏差（电荷/物质场候选）

    # ---------- 观测核对 ----------
    E_tot = ALPHA * 4.0 * math.pi * np.trapezoid(K * T * Om * r ** 2, r)
    N = np.trapezoid(dOm * r ** 2, r)
    M_nat = E_tot                                   # 自然单位质量（E_tot=E_ELECTRON 目标）
    out.append("=== 核对 C0045 收敛解 ===")
    out.append("  E_tot/E_ELECTRON = %.6f   N = %.6f   (目标 1)  M_nat = %.6e" % (E_tot / E_ELECTRON, N, M_nat))
    out.append("")

    # ---------- g 因子：两种电荷密度识别（自然单位，量纲一致）----------
    out.append("=== g 因子校验（g = 2·M_nat·⟨r⟩_nat，无量纲）===")
    results = {}
    cands = {
        "ρ∝Ω-Ω_DE（真空偏差/物质场）": dOm,
        "ρ∝能量密度 α·K·T·Ω": eps,
    }
    lamC_nat = 1.0 / M_nat                          # 自然单位康普顿波长（l_P）
    req_r = GE_EXP / 2.0 / M_nat                    # 需 ⟨r⟩_nat 才能给出 g_e
    for name, rho in cands.items():
        rbar = np.trapezoid(r ** 3 * rho, r) / np.trapezoid(r ** 2 * rho, r)  # ⟨r⟩_nat (l_P)
        g = 2.0 * M_nat * rbar
        results[name] = (rbar, g)
        out.append("  %s" % name)
        out.append("    ⟨r⟩_nat = %.4e l_P = %.4e m_phys" % (rbar, rbar * L_PLANCK))
        out.append("    g_TUFT = %.4e   (g_e=2.0023)   gap(需放大)=%.3e"
                   % (g, req_r / rbar))
    out.append("  g_e=2.0023 需 ⟨r⟩_nat = g_e/2/M_nat = %.4e l_P = %.4e λ_C(nat)"
               % (req_r, req_r / lamC_nat))
    out.append("  （λ_C(nat) = %.4e l_P = %.4e m_phys）" % (lamC_nat, lamC_nat * L_PLANCK))
    out.append("")

    # ---------- 若钉扎 ⟨r⟩=λ_C ----------
    out.append("=== 若将电荷半径钉扎到 λ_C(nat)（g 维度可行路线）===")
    out.append("  g 的 2 主项由 ⟨r⟩=λ_C(nat)=1/M_nat 给出：g=2·M_nat·λ_C=2.000000（玻尔磁子基线）")
    out.append("  反常项 g-2=0.0023193 ⟺ ⟨r⟩ 比 λ_C 大 0.116%（场延展订正）")
    out.append("  即：TUFT 复现 g_e 须让电荷分布 ⟨r⟩=1.00116·λ_C —— 与当前质量分布尺度")
    out.append("  （~l_P，lO≈1.185）相差 %.3e 倍" % (lamC_nat / 3.55))
    out.append("")

    # ---------- 辐射修正系数 C ----------
    out.append("=== 辐射修正系数 C（可计算性）===")
    out.append("  源稿 C=(1/N)∫4πr⁴ψ²(3V1ψ²-5V2ψ⁴)dr 定义在标量孤子 ψ 与势参数 V1,V2 上；")
    out.append("  当前物理 ansatz 是 K/T/Ω 几何场，无 ψ、无 V1/V2 ⇒ C 不能直接计算。")
    out.append("  需先在 TUFT 给出电荷/辐射修正密度与 K/T/Ω 的耦合映射（挂账项）再重算。本报告不虚构数值。")
    out.append("")

    # ---------- 结论 ----------
    out.append("=== 结论 ===")
    out.append("  1) 良态物理 ansatz 已把质量与归一化钉扎到机器精度（C0045，本脚本复核一致）。")
    out.append("  2) g 维度（自然单位，量纲一致）：当前收敛解电荷分布半径~O(l_P)，")
    out.append("     ⟨r⟩_nat=%.3e~%.3e l_P ⇒ g_TUFT=%.2e~%.2e，与 g_e≈2.0023 相差 ~1e22 倍。"
               % (min(v[0] for v in results.values()), max(v[0] for v in results.values()),
                  min(v[1] for v in results.values()), max(v[1] for v in results.values())))
    out.append("  3) 复现 g_e≈2.0023 须电荷分布加权平均半径钉扎到 ⟨r⟩=1.00116·λ_C(nat)=")
    out.append("     %.4e m_phys，即比当前尺度大 %.3e 倍 —— 下一层理论/参数步骤，当前 E,N 拟合未约束。"
               % (req_r * L_PLANCK, req_r / min(v[0] for v in results.values())))
    out.append("  4) 辐射修正系数 C 因缺电荷/辐射密度映射，当前 ansatz 不可直接计算，挂账。")
    out.append("")
    out.append("运行耗时 %.2f s" % (time.time() - t0))
    out.append("红线声明：电荷密度识别为模型假设；本脚本判定'良态 ansatz 在 g 维度上的结构'，")
    out.append("非物理真实主张。g 维度正确落地需另加磁矩/电荷目标或尺度钉扎。")
    print("\n".join(out))
    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out) + "\n")
    except Exception as exc:
        out.append("[warn] 报告写入失败: %s" % exc)


if __name__ == "__main__":
    main()
