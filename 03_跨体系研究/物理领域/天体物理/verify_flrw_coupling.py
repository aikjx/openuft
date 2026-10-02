# -*- coding: utf-8 -*-
"""
分支A：FLRW 宇宙学嵌入场方程(4) 的诚实检验
AI科技星 · 时空曲率-能量密度关系续篇

目的：检验"把场方程(4) R=(α/ρ_c)(∇ρ)²/(ρ+ρ_min) 嵌入均匀各向同性宇宙"
能否产生可观测的宇宙学信号（H0/CMB 修正）。

关键纠正（相对上轮口误）：
  上轮我说"FLRW 中 ∇ρ→0 → 纯 GR"。更精确：空间梯度 ∇ⁱρ=0，但
  时间梯度 ρ̇ 非零，故 (∇ρ)² = g^{μν}∂_μρ∂_νρ = -ρ̇²/c²（取绝对值即 ρ̇²/c²）。
  所以(4)在宇宙学里确实不严格为零——但量级极小，且在早宇宙会让
  修正 Friedmann 方程分母变负 → ill-posed。本脚本实算这两点。

闭合方式（与中子星脚本同哲学）：把(4)解释为对 GR 的 α-比例"额外有效密度"
  ρ_eff = ρ + (c²/8πG)·R_mod_extra,   R_mod_extra = (α/ρ_c)·(ρ̇²/c²)/(ρ+ρ_min)
  其中 ρ̇²/c² = |∇ρ|²（FLRW 下即时间梯度幅值）。
修正 Friedmann(00)： 3H² = 8πG(ρ + δρ),  δρ = (c²/8πG)·R_mod_extra
  => 3H² = 8πGρ + (α/ρ_c)·ρ̇²/(ρ+ρ_min)
  连续性：ρ̇ = -3H(ρ+p/c²)  →  ρ̇² = 9H²(ρ+p/c²)² （物质, p=0 时 =9H²ρ²）
  代入得隐式方程： H²[ 3 - (9α/ρ_c)·(ρ+p/c²)²/(ρ+ρ_min) ] = 8πGρ
  （注意：c² 在两端约掉，额外项量纲为 1/s²，与 H² 一致）

结论预告：
  (a) 低 z（小 ρ）：分母修正项 ~ (3α/ρ_c)·ρ ≪ 3  → H² 偏差 ~1e-35，完全 sterile；
  (b) 高 ρ（早宇宙）：分母修正项超过 3 → H² 无实根 → 理论在 T~1 GeV 即 ill-posed。
  ⇒ 原耦合无法做分支A；必须重构为"低密度大、高密度小"的耦合才有宇宙学信号。
"""

import math

G = 6.67430e-11
C = 299792458.0
C2 = C * C
RHO_C = 1.0e18      # kg/m^3  特征密度（与中子星脚本一致）
RHO_MIN = 1.0


def H2_GR(rho):
    return 8.0 * math.pi * G * rho / 3.0


def H2_mod_original(rho, alpha, p=0.0):
    """修正 Friedmann（原耦合）。返回 H²；若分母<=0 返回 None（ill-posed）。"""
    # 分母修正项： (9α/ρ_c)·(ρ+p/c²)²/(ρ+ρ_min)
    corr = (9.0 * alpha / RHO_C) * (rho + p / C2) ** 2 / (rho + RHO_MIN)
    denom = 3.0 - corr
    if denom <= 0:
        return None
    num = 8.0 * math.pi * G * rho
    return num / denom


def delta_H2_ratio(rho, alpha, p=0.0):
    """返回 H²_mod / H²_GR - 1（相对偏差）；ill-posed 返回 None。"""
    h2g = H2_GR(rho)
    h2m = H2_mod_original(rho, alpha, p)
    if h2m is None:
        return None
    return h2m / h2g - 1.0


if __name__ == "__main__":
    print("=" * 72)
    print("  分支A：FLRW 嵌入场方程(4) 诚实检验")
    print("=" * 72)
    alpha = 1.87
    print("α = %.3f, ρ_c = %.1e kg/m^3" % (alpha, RHO_C))
    print()

    # ---- (1) 跨宇宙学密度扫描：原耦合的 H² 偏差 / 是否 ill-posed ----
    print("-" * 72)
    print("【原耦合 (nabla rho)^2】跨密度扫描（物质 p=0）")
    print("  密度(kg/m^3)        对应温度(粗估)     H2偏差      状态")
    print("-" * 72)
    # 粗估温度：辐射期 ρ ≈ 1.5e4 (T/MeV)^4 kg/m^3  => T/MeV = (ρ/1.5e4)^0.25
    scan = [
        1.0e-26,   # 今天物质密度
        1.0e-20,   # z~10^2
        1.0e-17,   # z~10^3 (复合附近)
        1.0e4,     # T~1 MeV (BBN)
        1.0e12,    # T~100 MeV (QCD)
        1.0e17,    # T~几百 MeV
        1.0e18,    # T~1 GeV (电弱附近)
        1.0e20,    # T~10 GeV
    ]
    for rho in scan:
        ratio = delta_H2_ratio(rho, alpha)
        if rho > 0 and rho < 1.0e15:
            T_MeV = (rho / 1.5e4) ** 0.25
            Tstr = "T~%.1e MeV" % T_MeV
        else:
            Tstr = "T>>MeV"
        if ratio is None:
            print("  %.1e     %-14s   --         ILL-POSED (denom<0)" % (rho, Tstr))
        else:
            print("  %.1e     %-14s   %.2e    OK" % (rho, Tstr, ratio))
    print()

    # ---- (2) 失稳阈值 ----
    print("-" * 72)
    print("【失稳阈值】令 3 - (9*alpha/rho_c)*rho^2/(rho+rho_min) = 0 的临界密度")
    # 近似 ρ>>ρ_min: ρ_crit = 3ρ_c/(9α) = ρ_c/(3α)
    rho_crit = RHO_C / (3.0 * alpha)
    T_crit_MeV = (rho_crit / 1.5e4) ** 0.25
    print("  rho_crit ~ %.2e kg/m^3  (~ T ~ %.1e MeV, 电弱尺度附近)" % (rho_crit, T_crit_MeV))
    print("  => 原耦合在 rho > rho_crit 时修正 Friedmann 无实根，宇宙学不自洽。")
    print("     宇宙必然经历 T>1 GeV 的早epoch，故原理论在分支A下ill-posed。")
    print()

    # ---- (3) 若要做分支A，必须重构耦合：密度-比例型 vs 常数地板型 ----
    print("-" * 72)
    print("【重构耦合示范】使分支A产生信号（非退化、不早发散）")
    print("-" * 72)
    # 常数地板型：δρ = κ·ρ_c  => 3H² = 8πG(ρ + κρ_c)  ≡ GR + 有效Λ
    #   标定：今日 ρ_crit0 = 3H0²/(8πG) ≈ 9e-27 kg/m^3；观测 Ω_Λ≈0.69
    #   κρ_c = Ω_Λ·ρ_crit0  => κ = Ω_Λ·ρ_crit0/ρ_c
    H0 = 2.2e-18
    rho_crit0 = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
    kappa = 0.69 * rho_crit0 / RHO_C
    print("  方案① 常数地板 delta_rho = kappa * rho_c （=> 等效宇宙学常数）:")
    print("     kappa ≈ %.2e   (rho_crit0≈%.2e kg/m^3)" % (kappa, rho_crit0))
    print("     => 退化为标准 LambdaCDM，可解释 H0 张力但非'新'预言；")
    print("        若要'本理论独有'信号，需非Lambda函数型（如 delta_rho=kappa*rho_c*(rho_c/rho)^n）。")
    print()
    # 密度比例型：δρ = κ·ρ  => 3H² = 8πGρ(1+κ) ≡ 仅重标 G，与GR退化
    print("  方案② 密度比例 delta_rho=kappa*rho  => 3H^2 = 8*pi*G*rho*(1+kappa) == 仅重标 G（与GR退化，无新信号）")
    print()
    print("结论：原 (nabla rho)^2 耦合在宇宙学里 sterile(低z)+ill-posed(高z)；")
    print("      分支A 必须先重构耦合为'低密度大、高密度有界'的形式，")
    print("      方可产生可对比 NICER/H0/CMB 的本理论独有曲线。")
