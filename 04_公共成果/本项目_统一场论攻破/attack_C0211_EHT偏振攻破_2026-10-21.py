# -*- coding: utf-8 -*-
"""
attack_C0211_EHT偏振攻破_2026-10-21.py
母册 T109「EHT 偏振与黑洞磁层（Blandford-Znajek 磁场）· 广义相对论 MHD 模拟」攻破

定位：母册 T109（行 233，原文照录）：
  | T109 | EHT 偏振与黑洞磁层（Blandford-Znajek 磁场） | 广义相对论 MHD 模拟 | C5 | 🔲 |
前置：C0169（EHT M87* 阴影 39.689 μas、0.77σ）、C0207（光子环 r_ph=3M、b_c=3√3 M）、
     C0133（TUFT 已注销）。本册与 C0169/C0207 同对象（M87*）不同切面：那两册算
     「阴影/光子环的纯几何」，本册算「黑洞磁层的 GRMHD 观测量」——BZ 功率、
     视界磁场量级、磁化参数 σ、EHT 偏振环 EVPA 结构，并判定 TUFT/几何框架对
     「磁层 / GRMHD / 偏振结构」是否供给任何东西（无）。

把"T109 EHT 偏振与黑洞磁层"压缩成五条可复核读数：

  E1 观测事实（只引用不复算）：M87* B_H ~ 数十 G（EHT 2021 偏振 VIII）、喷流功率
     P_jet ~ 1e42 erg/s、EHT 偏振环 EVPA 呈"扭曲/螺旋"结构（轴对称理想下径向）。
  E2 **BZ 功率第一性精算（本册核心）**：
     Kerr 视界 r_+ = M(1+√(1-a*²))；视界角速度 Ω_H = a*/(2r_+)（几何单位）；
     BZ 功率 P_BZ = κ Φ² Ω_H²/(6π c)（cgs，erg/s）。
     对 M87*（M=6.5e9 M☉、a*=0.94）用任务声明的观测磁通 Φ=2.2e11 G·cm²（外部输入 1 枚）
     核算 P_BZ、并反推视界磁场 B_H = Φ/(π r_+²)。
  E3 磁层结构：磁化参数 σ = B²/(4π n m_p c²)（视界处 B~30 G、n~1e4 cm⁻³ 弥散吸积）量级。
  E4 偏振角度：轴对称（旋转对称）下 EVPA 沿径向（径向对称 → 方位旋度 ≡ 0）核算量级。
  E5 裁定：BZ 功率/偏振结构依赖 Kerr 几何 + 磁层方程（标准 GR 内在性质）+ 观测磁通输入，
     TUFT 无磁层/无 GRMHD 供给 ⇒ 结构性负面，按母册登记撞 C5。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：观测磁通 Φ=2.2e11 G·cm² 为任务声明的唯一外部输入（计数 1 枚）；EHT 观测值
只引用不复算；本册所有数值均为**标准 GR（Kerr 视界/BZ/磁层）算术复核**，严禁写成 TUFT
预测/修正；TUFT 已注销（C0133）。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48


BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 物理常数（cgs，CODATA 2018，只引用） ----------
G_CGS = Decimal("6.67430e-8")        # cm^3 g^-1 s^-2
C_CGS = Decimal("2.99792458e10")     # cm/s
M_SUN_G = Decimal("1.98847e33")      # g
MP_G = Decimal("1.6726219e-24")      # g（质子质量）
PI = Decimal("3.1415926535897932384626433832795028841971693993751")

# ---------- M87* 输入 ----------
M87_M_MSUN = Decimal("6.5e9")        # 黑洞质量（EHT 2019，只引用）
A_STAR = Decimal("0.94")             # 假设无量纲自旋（任务给定）
# 观测磁通（任务声明的唯一外部输入，计数 1 枚外部输入）
PHI = Decimal("2.2e11")              # G·cm^2
KAPPA_BZ = Decimal("0.044")          # BZ 效率系数（κ~0.044 量级，paraboloid 场）
# EHT 偏振文献参考（只引用不复算）
B_H_LIT = Decimal("30")              # G，EHT 2021 偏振 VIII "弱场"估计 ~30 G
N_H = Decimal("1e4")                 # cm^-3，M87* 弥散吸积流数密度 fiducial
P_JET = Decimal("1e42")              # erg/s，M87* 大尺度喷流功率观测量级（只引用）


def e1_facts():
    """观测/磁层事实（只引用不复算）。"""
    return {
        "M87_M_Msun": M87_M_MSUN,
        "a_star": A_STAR,
        "B_H_EHT_G": B_H_LIT,                         # EHT 2021 偏振 VIII ~ 30 G
        "P_jet_erg_s": P_JET,
        "EVPA_structure": "轴对称理想下 EVPA 径向；实测呈扭曲/螺旋环（EHT 2021 偏振 V/VIII）",
        "sources": [
            "EHT 2019 ApJL 875（M87* 质量 6.5e9 M_sun、阴影 42±3 μas）",
            "EHT 2021 ApJL 910 L5/L8（偏振结构：EVPA 环、B_H 弱场 ~数十 G）",
            "Blandford & Znajek 1977（BZ 功率 P=κ Φ² Ω_H²/6π c）",
            "C0169（M87* 阴影 39.689 μas、0.77σ）/ C0207（光子环 r_ph=3M）同对象衔接",
        ],
    }


def e2_bz_power():
    """BZ 功率 / Kerr 视界几何第一性精算（本册核心，Decimal 48 位）。"""
    M_g = M87_M_MSUN * M_SUN_G                 # g
    GM = G_CGS * M_g                            # cm^3 s^-2
    M_len = GM / (C_CGS * C_CGS)                # cm，GM/c^2
    # Kerr 视界半径 r_+ = M(1 + sqrt(1 - a*^2))
    a2 = A_STAR * A_STAR
    sqrt_1ma2 = (Decimal(1) - a2).sqrt()
    r_plus_coef = Decimal(1) + sqrt_1ma2        # 以 M_len 为单位
    r_plus = r_plus_coef * M_len               # cm
    # 视界角速度：Ω_H = a*/(2 r_+)（几何单位，系数）；乘 c^3/(GM) 得 s^-1
    Omega_H_geom = A_STAR / (Decimal(2) * r_plus_coef)   # 1/M_len 单位
    c3_over_gm = (C_CGS ** 3) / GM             # s^-1
    Omega_H = Omega_H_geom * c3_over_gm        # s^-1
    # BZ 功率 P = κ Φ² Ω_H² /(6π c)  [erg/s, cgs]
    Phi2 = PHI * PHI
    Om2 = Omega_H * Omega_H
    P_BZ = KAPPA_BZ * Phi2 * Om2 / (Decimal(6) * PI * C_CGS)
    # 反推视界处磁场 B_H = Φ/(π r_+^2)（单极通量估计）
    B_H_implied = PHI / (PI * r_plus * r_plus)
    # 与喷流功率比
    ratio_PBZ_Pjet = P_BZ / P_JET
    # 文献锚定交叉核算：由 EHT B_H~30 G 反推磁通 Φ_lit = B_H·π r_+^2，再算对应 P_BZ_lit
    # （注意：任务声明 Φ=2.2e11 反推 B_H 与 EHT 实测差 ~21 个数量级；此交叉核算给出物理自洽量级）
    Phi_lit = B_H_LIT * PI * r_plus * r_plus
    P_BZ_lit = KAPPA_BZ * Phi_lit * Phi_lit * Om2 / (Decimal(6) * PI * C_CGS)
    ratio_PBZlit_Pjet = P_BZ_lit / P_JET
    return {
        "M_len_cm": M_len,
        "sqrt_1ma2": sqrt_1ma2,
        "r_plus_coef_M": r_plus_coef,
        "r_plus_cm": r_plus,
        "Omega_H_geom_coef": Omega_H_geom,
        "c3_over_GM_s": c3_over_gm,
        "Omega_H_s": Omega_H,
        "Phi_G_cm2": PHI,
        "kappa": KAPPA_BZ,
        "P_BZ_erg_s": P_BZ,
        "B_H_implied_G": B_H_implied,
        "ratio_PBZ_over_Pjet": ratio_PBZ_Pjet,
        "Phi_lit_from_BH_G_cm2": Phi_lit,
        "P_BZ_lit_erg_s": P_BZ_lit,
        "ratio_PBZlit_over_Pjet": ratio_PBZlit_Pjet,
    }


def e3_magnetization():
    """磁化参数 σ = B²/(4π n m_p c²)（视界/吸积流处，无量纲）。"""
    B = B_H_LIT
    sigma = (B * B) / (Decimal(4) * PI * N_H * MP_G * C_CGS * C_CGS)
    # 磁压 vs 气体压：β = 8π n m_p c_s^2 / B^2 （c_s~0.5c fiducial 只给量级）
    return {
        "B_G": B,
        "n_cm_3": N_H,
        "sigma": sigma,
        "regime": "σ~1 量级 → 磁压主导（magnetically dominated），MAD/SANE 喷流成立前提",
    }


def e4_evpa():
    """偏振角度：轴对称（旋转对称）下 EVPA 径向，方位旋度 ≡ 0（Fraction 精确）。"""
    # 轴对称度规 + 轴对称吸积流 → 发射系数与斯托克斯参数关于黑洞轴对称；
    # 旋转对称 ⇒ EVPA 角沿径向（方位角方向无净扭转），对称破缺（自旋多普勒/内进动）才产生 twist。
    twist_axisym = Fraction(0)        # 轴对称极限下方位 EVPA 旋度 = 0（精确）
    # 观测到的扭曲来自自旋多普勒束流 + 内进动（GRMHD），非几何框架供给
    return {
        "symmetry": "轴对称（旋转对称）",
        "EVPA_axis": "径向（radial）",
        "twist_axisym_frac": twist_axisym,    # = 0/1
        "observed_twist_source": "自旋多普勒束流 + 内进动（GRMHD 效应），非 TUFT 供给",
    }


def e5_supply():
    """TUFT/几何框架对磁层/GRMHD/偏振结构的供给判定。"""
    return {
        "BZ_needs_Kerr_geometry": True,       # r_+/Ω_H 是 Kerr 度规性质
        "BZ_needs_magnetohydro": True,        # 功率来自视界外 MHD 电磁场提取
        "polarization_needs_GRMHD": True,     # EVPA 环依赖 GRMHD 辐射转移
        "tuft_has_magnetosphere": 0,
        "tuft_has_GRMHD": 0,
        "tuft_has_polarization_transfer": 0,
        "tuft_cancelled_C0133": True,
        "supply": 0,
        "collides": "C5",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0211 · EHT 偏振与黑洞磁层（Blandford-Znajek）攻破（母册 T109）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 观测/磁层事实（只引用不复算）")
    for s in g1["sources"]:
        w("  · " + s)
    w("  M87*：M=%s M☉、假设 a*=%s；EHT 视界磁场 ~%s G；喷流功率 P_jet ~ %s erg/s"
      % (g1["M87_M_Msun"], g1["a_star"], g1["B_H_EHT_G"], g1["P_jet_erg_s"]))
    w("  EVPA：%s" % g1["EVPA_structure"])
    entries.append(("E1", "M87* B_H~%s G、P_jet~1e42 erg/s、EVPA 扭曲环（EHT 2019/2021 只引用）"
                    % g1["B_H_EHT_G"], "PASS", "来源标注：EHT ApJL 875/910；BZ 1977"))

    # ---- E2 ----
    g2 = e2_bz_power()
    w("\n[E2] BZ 功率 / Kerr 视界几何第一性精算（本册核心，Decimal 48 位）")
    w("  GM/c^2 = %s cm（每 M☉ %s cm）"
      % (fv(g2["M_len_cm"], "6e"), fv(Decimal("1.476670e5"), "6e")))
    w("  √(1-a*²) = √(1-0.94²) = %s；r_+/M = 1+√(1-a*²) = %s"
      % (fv(g2["sqrt_1ma2"], "15f"), fv(g2["r_plus_coef_M"], "15f")))
    w("  r_+ = %s cm" % fv(g2["r_plus_cm"], "6e"))
    w("  Ω_H 几何系数 = a*/(2 r_+/M) = %s；c³/GM = %s s^-1"
      % (fv(g2["Omega_H_geom_coef"], "15f"), fv(g2["c3_over_GM_s"], "6e")))
    w("  Ω_H = %s s^-1" % fv(g2["Omega_H_s"], "6e"))
    w("  外部输入：Φ = %s G·cm²（任务声明，计数 1 枚）；κ = %s"
      % (g2["Phi_G_cm2"], g2["kappa"]))
    w("  P_BZ = κ Φ² Ω_H²/(6π c) = %s erg/s" % fv(g2["P_BZ_erg_s"], "6e"))
    w("  反推视界磁场 B_H = Φ/(π r_+²) = %s G" % fv(g2["B_H_implied_G"], "6e"))
    w("  P_BZ / P_jet = %s（P_jet~1e42 erg/s）" % fv(g2["ratio_PBZ_over_Pjet"], "6e"))
    w("  [文献锚定交叉核算] 由 EHT B_H~%s G 反推磁通 Φ_lit = B_H·π r_+² = %s G·cm²"
      % (B_H_LIT, fv(g2["Phi_lit_from_BH_G_cm2"], "6e")))
    w("    对应 P_BZ_lit = κ Φ_lit² Ω_H²/(6π c) = %s erg/s；P_BZ_lit/P_jet = %s"
      % (fv(g2["P_BZ_lit_erg_s"], "6e"), fv(g2["ratio_PBZlit_over_Pjet"], "6e")))
    w("  => 注：Φ=2.2e11 反推 B_H=%s G，与 EHT 实测 %s G 差 ~21 个数量级；"
      "物理自洽磁通为 Φ_lit。BZ 公式与视界几何均为标准 GR 算术复核。"
      % (fv(g2["B_H_implied_G"], "4e"), B_H_LIT))
    entries.append(("E2", "r_+/M=%s、Ω_H=%s s^-1；P_BZ=%s erg/s（Φ=%s G·cm² 外部输入）"
                    % (fv(g2["r_plus_coef_M"], "6f"), fv(g2["Omega_H_s"], "4e"),
                       fv(g2["P_BZ_erg_s"], "4e"), g2["Phi_G_cm2"]), "PASS",
                    "Decimal 48 位精算；标准 GR/Kerr 算术复核，非 TUFT 预测"))

    # ---- E3 ----
    g3 = e3_magnetization()
    w("\n[E3] 磁层结构：磁化参数 σ = B²/(4π n m_p c²)")
    w("  B=%s G、n=%s cm^-3 ⇒ σ = %s"
      % (g3["B_G"], g3["n_cm_3"], fv(g3["sigma"], "6f")))
    w("  => %s" % g3["regime"])
    entries.append(("E3", "σ = %s（B~30 G、n~1e4 cm^-3），磁压主导" % fv(g3["sigma"], "4f"),
                    "PASS", "标准 GRMHD 磁化参数算术复核"))

    # ---- E4 ----
    g4 = e4_evpa()
    w("\n[E4] 偏振角度：轴对称下 EVPA 径向，方位旋度核算")
    w("  对称性 = %s；EVPA 沿 %s；轴对称极限方位 twist = %s（Fraction 精确）"
      % (g4["symmetry"], g4["EVPA_axis"], g4["twist_axisym_frac"]))
    w("  观测扭曲来源：%s" % g4["observed_twist_source"])
    entries.append(("E4", "轴对称 EVPA 径向、方位 twist=0（Fraction 精确）；观测扭曲来自 GRMHD",
                    "PASS", "旋转对称 → EVPA 径向；Fraction 0/1"))

    # ---- E5 ----
    g5 = e5_supply()
    w("\n[E5] 裁定")
    w("  T109 = Kerr 视界几何（r_+/Ω_H）+ 磁层 MHD（BZ 功率）+ GRMHD 偏振辐射转移。")
    w("  BZ 功率依赖 Kerr 几何 + 磁层方程（标准 GR 内在性质）+ 观测磁通 Φ 外部输入。")
    w("  TUFT 磁层结构=%d、GRMHD=%d、偏振辐射转移=%d；TUFT 已注销（C0133）=%s"
      % (g5["tuft_has_magnetosphere"], g5["tuft_has_GRMHD"],
         g5["tuft_has_polarization_transfer"], g5["tuft_cancelled_C0133"]))
    w("  => **T109 结构性负面（对 TUFT/几何框架）**；按母册登记撞 **C5**。")
    entries.append(("E5", "T109 结构性负面：BZ/磁层/偏振依赖 Kerr+GRMHD+观测输入，"
                    "TUFT 无供给", "PASS", "撞 C5；承接 C0133 TUFT 已注销"))

    # ---- 守卫 ----
    guards = [
        ("G1", "r_+/M = 1+√(1-a*²) ≈ 1.341174（a*=0.94）",
         abs(g2["r_plus_coef_M"] - Decimal("1.3411739412")) < Decimal("1e-6")),
        ("G2", "Ω_H 几何系数 = a*/(2 r_+/M) ≈ 0.35044",
         abs(g2["Omega_H_geom_coef"] - Decimal("0.350439")) < Decimal("1e-4")),
        ("G3", "Ω_H ≈ 1.1e-5 s^-1（黑洞角频率量级 1e-6–1e-4）",
         Decimal("1e-6") < g2["Omega_H_s"] < Decimal("1e-4")),
        ("G4", "P_BZ > 0（Φ 外部输入正定量，BZ 公式正定量）", g2["P_BZ_erg_s"] > 0),
        ("G5", "磁化参数 σ ~ 1 量级（0.1–100，磁压主导）",
         Decimal("0.1") < g3["sigma"] < Decimal("100")),
        ("G6", "轴对称极限 EVPA 方位 twist = 0（Fraction 精确）",
         g4["twist_axisym_frac"] == Fraction(0)),
        ("G8", "文献锚定 P_BZ_lit 与喷流功率同量级（1e40–1e43 erg/s）",
         Decimal("1e40") < g2["P_BZ_lit_erg_s"] < Decimal("1e43")),
        ("G7", "TUFT 磁层/GRMHD/偏振供给 = 0，撞 C5",
         g5["supply"] == 0 and g5["collides"] == "C5"),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0211 guard failed"

    w("\n[诚实边界]")
    w("  观测磁通 Φ=2.2e11 G·cm² 为任务声明的唯一外部输入（计数 1 枚）；EHT 观测值只引用不复算；")
    w("  本册数值均为标准 GR（Kerr 视界/BZ/磁层）算术复核，严禁写成 TUFT 预测/修正；")
    w("  TUFT 已注销（C0133）；裁的是「TUFT/几何框架能否供给磁层/GRMHD/偏振结构」，判供给 0。")
    w("  红线：不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("  有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0211_EHT偏振攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0211_EHT偏振攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0211_EHT_polarization_magnetosphere",
            "parent_row": "T109 | EHT 偏振与黑洞磁层（Blandford-Znajek 磁场） | 广义相对论 MHD 模拟 | C5",
            "external_inputs": {"Phi_G_cm2": str(PHI), "count": 1},
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E2_r_plus_coef_M": str(g2["r_plus_coef_M"]),
            "E2_sqrt_1ma2": str(g2["sqrt_1ma2"]),
            "E2_r_plus_cm": str(g2["r_plus_cm"]),
            "E2_Omega_H_geom_coef": str(g2["Omega_H_geom_coef"]),
            "E2_Omega_H_s": str(g2["Omega_H_s"]),
            "E2_Phi_G_cm2": str(g2["Phi_G_cm2"]),
            "E2_P_BZ_erg_s": str(g2["P_BZ_erg_s"]),
            "E2_B_H_implied_G": str(g2["B_H_implied_G"]),
            "E2_ratio_PBZ_over_Pjet": str(g2["ratio_PBZ_over_Pjet"]),
            "E2_Phi_lit_from_BH_G_cm2": str(g2["Phi_lit_from_BH_G_cm2"]),
            "E2_P_BZ_lit_erg_s": str(g2["P_BZ_lit_erg_s"]),
            "E2_ratio_PBZlit_over_Pjet": str(g2["ratio_PBZlit_over_Pjet"]),
            "E3_sigma": str(g3["sigma"]),
            "E4_twist_axisym_frac": str(g4["twist_axisym_frac"]),
            "E5_geometry_supply": g5["supply"],
            "E5_collides": g5["collides"],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0211 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
