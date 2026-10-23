# -*- coding: utf-8 -*-
"""
TUFT-r155｜螺旋的【动力学层】：束缚力缺口 · 真空击穿 · 同步辐射判决

══════════════════════════════════════════════════════════════════════════
00. 编号与定位
══════════════════════════════════════════════════════════════════════════
【编号】r155。实测首空号：r150–r154 均已占用，r155 为空。

【★ 前四卷都在判几何 / 读法 / 参数，本卷第一次判【动力学】】
  r151（式子层）：{v=c} ∧ {ωr=c} ⇒ u≡0 ⇒ τ≡0 ⇒ 螺旋退化为圆。
  r152（式子层）：{ωr=c} ∧ {h·f=c} ⇒ v=√2·c 超光速。
  r153（读法层）：读法穷举 ⇒ 三式组 8 读法健康解 0；唯一健康分支 = 快度读法 + 删 v=c。
  r154（后果层）：该分支的电子磁矩差整整 g=2、静止能量差 +73.2%。
  **本卷（动力学层）**：不问几何，只问两件事——
      (1) **维持这个螺旋需要多大的力？** 谁提供？够不够？会不会击穿真空？
      (2) **这个螺旋会辐射掉多少能量？** 电子还能活多久？

  ⇒ 本卷是**独立于读法**的一票否决：r153 的「换读法」救不了它（见 B1）。

══════════════════════════════════════════════════════════════════════════
01. 本卷的形式化
══════════════════════════════════════════════════════════════════════════
  沿用 r151–r154 的几何：r = ħ/(2mc)（约化康普顿半波长），ωr = c（定义）。

  横向速率（两读法）：
      坐标读法：v_⊥ = c            ⇒ a_⊥ = c²/r，      γ 无定义（总速 √2c 超光速）
      快度读法：v_⊥ = c/γ = c/√3   ⇒ a_⊥ = c²/(3r)，   γ = √3

  横向力（相对论横向力 F_⊥ = γ m a_⊥）：
      坐标读法：F = m c²/r
      快度读法：F = γ m c²/(3r) = m c²/(√3 r)

  ★ Schwinger（真空击穿）临界场强：E_c = m²c³/(eħ)
      所需场强 E = F/e
      ⇒ E/E_c = ħ/(m c r) 〔坐标〕   = ħ/(√3 m c r) 〔快度〕
      ⇒ 代入 r = ħ/(2mc)：E/E_c ≡ **2**（坐标）与 **2/√3 = 1.1547**（快度）
      ⇒ **与质量无关**（r ∝ 1/m ⇒ m·c·r ≡ ħ/2）—— 标度不变的硬结论。

  ★ 相对论 Larmor（圆周运动 v ⊥ a）：
      P = e²γ⁴a² / (6πε₀c³)
      γ⁴a_⊥² 〔坐标〕 = 1·(c²/r)²      = c⁴/r²
      γ⁴a_⊥² 〔快度〕 = 9·(c²/(3r))²   = c⁴/r²
      ⇒ **两种读法精确相等** ⇒ **P 与读法无关** ≡ e²c/(6πε₀r²) —— 换读法救不了辐射。

══════════════════════════════════════════════════════════════════════════
02. 待检验命题
══════════════════════════════════════════════════════════════════════════
  Q1: 存在一种已知基本相互作用能提供维持该螺旋所需的向心力。
  Q2: 维持该螺旋所需的场强低于 Schwinger 真空击穿极限。
  Q3: 该螺旋的辐射功率与电子的实测稳定性相容。
"""

import json
import math
import os
import sys
import time

# ============================================================
# 常数（CODATA 2018 / SI 2019 定义值）
# ============================================================
C = 299792458.0
HBAR = 1.054571817e-34
H_PLANCK = 6.62607015e-34
M_E = 9.1093837015e-31
M_MU = 1.883531627e-28
M_P = 1.67262192369e-27
M_EARTH = 5.9722e24
Q_E = 1.602176634e-19
EPS0 = 8.8541878128e-12
K_E = 8.9875517923e9            # 1/(4πε₀)
G = 6.67430e-11
ALPHA = 7.2973525693e-3
YR = 3.1557e7                   # s per year（儒略年）

PARTICLES = [("电子 e⁻", M_E), ("μ 子 μ⁻", M_MU), ("质子 p⁺", M_P),
             ("地球", M_EARTH)]

# 电子寿命实验下限（PDG：> 6.6×10²⁸ yr）
E_LIFETIME_YR = 6.6e28
E_LIFETIME_S = E_LIFETIME_YR * YR

SQRT3 = math.sqrt(3.0)
TOL = 1e-9


# ============================================================
# 核心：给一个质量，算出全部动力学量（两种读法各一套）
# ============================================================
def dynamics(m, q=Q_E):
    r = HBAR / (2.0 * m * C)                 # r = ħ/(2mc)（r151–r154 同口径）

    # ---- 坐标读法：v_⊥ = c ----
    a_c = C * C / r
    F_c = m * C * C / r                      # F = m v_⊥²/r（γ 无定义）

    # ---- 快度读法：v_⊥ = c/γ = c/√3，γ = √3 ----
    a_p = (C / SQRT3) ** 2 / r               # = c²/(3r)
    F_p = SQRT3 * m * a_p                    # F_⊥ = γ m a_⊥

    # ---- Schwinger 临界场强与所需场强 ----
    E_crit = m * m * C ** 3 / (q * HBAR)
    E_req_c = F_c / q
    E_req_p = F_p / q
    ratio_c = E_req_c / E_crit
    ratio_p = E_req_p / E_crit

    # ---- 相对论 Larmor（圆周运动）----
    pref = q * q / (6.0 * math.pi * EPS0 * C ** 3)
    P_c = pref * 1.0 * a_c ** 2              # γ=1（坐标读法无 γ）
    P_p = pref * (SQRT3 ** 4) * a_p ** 2     # γ⁴ = 9
    P_closed = q * q * C / (6.0 * math.pi * EPS0 * r * r)   # 闭式 e²c/(6πε₀r²)

    mc2 = m * C * C
    tau_c = mc2 / P_c
    tau_p = mc2 / P_p

    # ---- 已知力能提供的力 ----
    F_em = K_E * q * q / (r * r)             # 库仑（自作用量级）
    F_grav = G * m * m / (r * r)             # 引力（自作用量级）

    return {"m": m, "r": r,
            "a_coord": a_c, "a_proper": a_p,
            "F_coord": F_c, "F_proper": F_p,
            "F_em": F_em, "F_grav": F_grav,
            "ratio_em_coord": F_em / F_c, "ratio_em_proper": F_em / F_p,
            "ratio_grav_coord": F_c / F_grav, "ratio_grav_proper": F_p / F_grav,
            "E_crit": E_crit, "E_req_coord": E_req_c, "E_req_proper": E_req_p,
            "ratio_schwinger_coord": ratio_c, "ratio_schwinger_proper": ratio_p,
            "P_coord": P_c, "P_proper": P_p, "P_closed": P_closed,
            "gamma4_a2_coord": a_c ** 2,
            "gamma4_a2_proper": (SQRT3 ** 4) * a_p ** 2,
            "c4_over_r2": C ** 4 / (r * r),
            "mc2": mc2, "tau_coord": tau_c, "tau_proper": tau_p,
            "lifetime_gap": E_LIFETIME_S / tau_c,
            "r_over_r_e": r / (K_E * q * q / (m * C * C))}


# ============================================================
# A 组：向心加速度与束缚力缺口
# ============================================================
def A1_acceleration():
    d = dynamics(M_E)
    return {"a_coord": d["a_coord"], "a_proper": d["a_proper"],
            "a_coord_in_g": d["a_coord"] / 9.80665,
            "a_proper_in_g": d["a_proper"] / 9.80665}


def A2_required_force():
    d = dynamics(M_E)
    return {"F_coord": d["F_coord"], "F_proper": d["F_proper"],
            "F_coord_in_N": d["F_coord"], "F_proper_in_N": d["F_proper"],
            "note": "单个电子需要约 0.42 N / 0.24 N 的向心力"}


FORCE_SOURCES = [
    {"name": "电磁（库仑自作用 ke²/r²）", "F": None, "kind": "em"},
    {"name": "引力（自作用 Gm²/r²）", "F": None, "kind": "grav"},
    {"name": "强相互作用", "F": None, "kind": "strong",
     "note": "电子**不参与**强相互作用（轻子）"},
    {"name": "弱相互作用", "F": None, "kind": "weak",
     "note": "量级远低于电磁，且力程 ~10⁻¹⁸ m ≪ r"},
]


def A3_force_sources():
    d = dynamics(M_E)
    rows = [
        {"source": "电磁（库仑自作用 ke²/r²）",
         "F": d["F_em"],
         "ratio_vs_coord": d["F_em"] / d["F_coord"],
         "ratio_vs_proper": d["F_em"] / d["F_proper"],
         "enough": False},
        {"source": "引力（自作用 Gm²/r²）",
         "F": d["F_grav"],
         "ratio_vs_coord": d["F_grav"] / d["F_coord"],
         "ratio_vs_proper": d["F_grav"] / d["F_proper"],
         "enough": False},
        {"source": "强相互作用", "F": None, "ratio_vs_coord": None,
         "ratio_vs_proper": None, "enough": False,
         "note": "电子是轻子，不参与强相互作用"},
        {"source": "弱相互作用", "F": None, "ratio_vs_coord": None,
         "ratio_vs_proper": None, "enough": False,
         "note": "力程 ~10⁻¹⁸ m，比 r=1.93e−13 m 小 5 个量级"},
    ]
    return {"rows": rows,
            "n_sources": len(rows),
            "n_enough": 0,
            "em_shortfall": d["F_coord"] / d["F_em"],
            "grav_shortfall": d["F_coord"] / d["F_grav"],
            "fifth_force_min_strength_vs_em": d["F_coord"] / d["F_em"]}


def A4_schwinger():
    d = dynamics(M_E)
    return {"E_crit": d["E_crit"],
            "E_req_coord": d["E_req_coord"], "E_req_proper": d["E_req_proper"],
            "ratio_coord": d["ratio_schwinger_coord"],
            "ratio_proper": d["ratio_schwinger_proper"],
            "analytic_coord": 2.0, "analytic_proper": 2.0 / SQRT3,
            "dev_coord": abs(d["ratio_schwinger_coord"] - 2.0),
            "dev_proper": abs(d["ratio_schwinger_proper"] - 2.0 / SQRT3),
            "both_exceed": (d["ratio_schwinger_coord"] > 1.0
                            and d["ratio_schwinger_proper"] > 1.0),
            "scale_invariant": True}


def A5_identity():
    """r/r_e = 1/(2α) 是精确恒等式 ⇒ 降 INFO（不是预言）
    ★自抓（本卷自纠）：初版用**绝对**阈值 1e-9 判 r/r_e（量级 68.5）与 1/(2α_公布) 相等
      ⇒ 相对阈值 1.5e-11，远低于**公布常数舍入地板**（K_E 末位 ±14、α 末位 ±11，
      各自相对 ~1.5e-10）⇒ 机读偏差 6.1e-10 被误判为恒等式不成立。
    正确做法（r154 常数舍入地板纪律）分两层：
      ① 同源常数层：α_implied = K_E q²/(ħ c) 与 r/r_e = ħc/(2K_E q²) 用**同一组**
         常数 ⇒ 代数恒等，偏差应为机器零（这才是恒等式的机检）；
      ② 公布常数层：与独立公布的 α（CODATA 2018）比较，偏差受双方舍入限制
         ⇒ 只能登记 BOUNDARY，**不得计入判据**。
    """
    d = dynamics(M_E)
    alpha_implied = K_E * Q_E * Q_E / (HBAR * C)      # 同源常数
    inv2a_implied = 1.0 / (2.0 * alpha_implied)
    inv2a_published = 1.0 / (2.0 * ALPHA)
    dev_internal = abs(d["r_over_r_e"] / inv2a_implied - 1.0)
    dev_published = abs(d["r_over_r_e"] / inv2a_published - 1.0)
    return {"r_over_r_e": d["r_over_r_e"],
            "alpha_implied": alpha_implied,
            "alpha_published": ALPHA,
            "inv2a_implied": inv2a_implied,
            "inv2a_published": inv2a_published,
            "dev_internal": dev_internal,
            "dev_published_rel": dev_published,
            "is_identity": dev_internal < 1e-12,
            "rounding_floor_note":
                "与公布 α 的相对偏差 %.3e 来自 K_E/α 各自舍入（~1e-10 量级）"
                "⇒ 登记 BOUNDARY，不计入判据" % dev_published,
            "derivation": "r/r_e = [ħ/(2mc)]·[4πε₀mc²/e²] = ħc/(2k_e e²) = 1/(2α)"}


# ============================================================
# B 组：同步辐射
# ============================================================
def B1_reading_independence():
    """★ γ⁴a² 在两种读法下精确相等 ⇒ P 与读法无关"""
    d = dynamics(M_E)
    gap = abs(d["gamma4_a2_proper"] / d["gamma4_a2_coord"] - 1.0)
    return {"gamma4_a2_coord": d["gamma4_a2_coord"],
            "gamma4_a2_proper": d["gamma4_a2_proper"],
            "c4_over_r2": d["c4_over_r2"],
            "rel_gap": gap,
            "identical": gap < 1e-12,
            "dev_vs_closed_coord": abs(d["gamma4_a2_coord"] / d["c4_over_r2"] - 1.0),
            "dev_vs_closed_proper": abs(d["gamma4_a2_proper"] / d["c4_over_r2"] - 1.0)}


def B2_power():
    d = dynamics(M_E)
    return {"P_coord": d["P_coord"], "P_proper": d["P_proper"],
            "P_closed": d["P_closed"],
            "dev_coord_vs_closed": abs(d["P_coord"] / d["P_closed"] - 1.0),
            "dev_proper_vs_closed": abs(d["P_proper"] / d["P_closed"] - 1.0),
            "P_in_MW": d["P_closed"] / 1e6,
            "identical_across_readings":
                abs(d["P_coord"] / d["P_proper"] - 1.0) < 1e-12}


def B3_lifetime():
    d = dynamics(M_E)
    return {"tau": d["tau_coord"], "tau_proper": d["tau_proper"],
            "mc2": d["mc2"], "P": d["P_closed"],
            "exp_lower_bound_s": E_LIFETIME_S,
            "exp_lower_bound_yr": E_LIFETIME_YR,
            "gap": d["lifetime_gap"],
            "gap_in_orders": math.log10(d["lifetime_gap"]),
            "fails": d["lifetime_gap"] > 1.0}


def B4_scan():
    rows = []
    for name, m in PARTICLES:
        d = dynamics(m)
        rows.append({"name": name, "m": m, "r": d["r"],
                     "P": d["P_closed"], "tau": d["tau_coord"],
                     "ratio_schwinger": d["ratio_schwinger_coord"],
                     "E_crit": d["E_crit"]})
    ratios = [x["ratio_schwinger"] for x in rows]
    return {"rows": rows, "spread_ratio": max(ratios) - min(ratios),
            "scale_invariant": (max(ratios) - min(ratios)) < 1e-9,
            "tau_monotone": all(rows[i]["tau"] > rows[i + 1]["tau"]
                                for i in range(len(rows) - 1))}


def B5_scaling_laws():
    """P ∝ m²、τ ∝ 1/m 的标度律机读验证
    ★自抓（本卷自纠，机读抓出的分析错误）：初版把 τ 的标度误写为 **1/m³**
      （τ = mc²/P、P ∝ m² ⇒ τ ∝ m/m² = **1/m**）——机读 tau_dev = 0.9999997
      立即抓出（质子/电子 τ 比 = 1836.15 = 质量比，而非质量比³ = 6.19e9）。
      已改为 1/m 并机读确认。保留此记录：判据抓出了卷作者自己的分析笔误。
    """
    d_e = dynamics(M_E)
    d_p = dynamics(M_P)
    r_P = d_p["P_closed"] / d_e["P_closed"]
    r_m = (M_P / M_E) ** 2
    r_tau = d_e["tau_coord"] / d_p["tau_coord"]
    r_m1 = M_P / M_E
    return {"P_ratio": r_P, "m2_ratio": r_m,
            "P_dev": abs(r_P / r_m - 1.0),
            "tau_ratio": r_tau, "m1_ratio": r_m1,
            "tau_dev": abs(r_tau / r_m1 - 1.0),
            "P_scales_as_m2": abs(r_P / r_m - 1.0) < 1e-9,
            "tau_scales_as_1_over_m": abs(r_tau / r_m1 - 1.0) < 1e-9}


# ============================================================
# C 组：两难（防过度指控）
# ============================================================
def C1_radiation_dilemma():
    d = dynamics(M_E)
    return {
        "branch_real": "该螺旋是**真实的经典加速运动** ⇒ 必辐射 "
                       "P = %.6e W，寿命 %.6e s，与实验下限差 %.2e 倍（%.1f 个量级）"
                       % (d["P_closed"], d["tau_coord"], d["lifetime_gap"],
                          math.log10(d["lifetime_gap"])),
        "branch_virtual": "该螺旋是**虚过程 / 不辐射** ⇒ 就不是来料主张的"
                          "『真实的空间螺旋运动』，且不能用它解释电磁场的起源",
        "both_unfavorable": True}


def C2_force_dilemma():
    d = dynamics(M_E)
    return {
        "branch_fifth": "引入**第五种力**：强度至少 %.2f 倍电磁、%.2e 倍引力"
                        " ⇒ 必然在散射/能谱实验中显现，而从未被观测"
                        % (d["F_coord"] / d["F_em"], d["F_coord"] / d["F_grav"]),
        "branch_none": "**没有力** ⇒ 电子做半径恒定的圆周运动而无需向心力"
                       " ⇒ 违反牛顿第一定律（惯性）/ 测地线运动",
        "both_unfavorable": True}


def C3_classical_caveat():
    return {"note": "Larmor 公式是经典电动力学的；QED 中 Zitterbewegung 属虚过程、不辐射。"
                    "本卷**不**忽略这一点，而是用 C1 两难把它封住："
                    "取经典 ⇒ 辐射致死；取虚过程 ⇒ 放弃来料的核心图像。",
            "qed_g2_note": "即便计入 QED 修正，本卷缺口是 **55 个量级**，"
                           "远非微扰修正所能弥补"}


# ============================================================
# D 组：参数计数与修复定价
# ============================================================
def D1_parameter_gate():
    return {"n_free": 0, "n_obs": 2,     # 电子寿命下限、Schwinger 极限（皆未通过）
            "gate": 0 <= 2 - 1,
            "su5_free": 2, "su5_obs": 3,
            "su5_gate": 2 <= 3 - 1,
            "su5_tree_sin2": 0.375, "su5_measured": 0.231210,
            "su5_dev": abs(0.375 - 0.231210) / 0.231210}


REPAIR_TARGETS = ["经典 Larmor 辐射", "力的来源", "半径 r = ħ/(2mc)"]
ACTS = ("KEEP", "DEL", "REPLACE")


def D2_repair_pricing():
    """
    三根支柱 × {KEEP, DEL, REPLACE} = 27。语义写死（记忆 §三）。
      R（辐射）：KEEP=经典 Larmor 必辐射；DEL=不辐射（无机制）；REPLACE=改用 QED 虚过程
      F（力）  ：KEEP=来源未指定；DEL=无力；REPLACE=引入第五种力
      X（半径）：KEEP=r=ħ/(2mc)；DEL=尺度外输；REPLACE=放大半径
    存活判据（机器执行）：
      (1) 寿命：τ ≥ 实验下限            ⇒ 只有 R ∈ {DEL, REPLACE}
      (2) 力机制：有明确机制            ⇒ 只有 F = REPLACE
      (3) 尺度定标：r 由 m 定标         ⇒ X ≠ DEL
      (4) 不击穿真空：E/E_c < 1         ⇒ 需 r > ħ/(mc)，即 X = REPLACE
    """
    d = dynamics(M_E)
    out = []
    for a_R in ACTS:
        for a_F in ACTS:
            for a_X in ACTS:
                # (1) 寿命
                life_ok = a_R in ("DEL", "REPLACE")
                # (2) 力机制
                force_ok = (a_F == "REPLACE")
                # (3) 尺度定标
                scale_ok = (a_X != "DEL")
                # (4) 不击穿真空
                if a_X == "REPLACE":
                    r_new = 2.0 * HBAR / (m_C := M_E) / C   # r 放大到 2ƛ_C = 2ħ/(mc)
                    # 真空门最小需求：E/E_c = ħ/(mcr) < 1 ⇒ r > ƛ_C = ħ/(mc)；
                    # 取 2ƛ_C（E/E_c = 1/2）干净过门。★自纠：初版注释误写 ħ/(mc)。
                    ratio = (HBAR / (M_E * C * r_new))
                    vac_ok = ratio < 1.0
                    ratio_val = ratio
                elif a_X == "KEEP":
                    vac_ok = False
                    ratio_val = d["ratio_schwinger_coord"]
                else:
                    vac_ok = True        # 尺度外输，本门不适用
                    ratio_val = None
                valid = life_ok and force_ok and scale_ok and vac_ok
                cost = []
                if a_R == "KEEP":
                    cost.append("必辐射 ⇒ 寿命 %.2e s，与观测差 %.1f 个量级"
                                % (d["tau_coord"], math.log10(d["lifetime_gap"])))
                if a_R == "DEL":
                    cost.append("不辐射但无机制 ⇒ 与『用该运动解释电磁场』互斥")
                if a_R == "REPLACE":
                    cost.append("改用 QED 虚过程 ⇒ 放弃『真实的空间螺旋运动』核心图像")
                if a_F == "KEEP":
                    cost.append("力的来源未指定 ⇒ 无机制")
                if a_F == "DEL":
                    cost.append("无力 ⇒ 违反牛顿第一定律 / 测地线运动")
                if a_F == "REPLACE":
                    cost.append("引入第五种力（≥%.1f×电磁、%.1e×引力）⇒ 从未被观测"
                                % (d["F_coord"] / d["F_em"], d["F_coord"] / d["F_grav"]))
                if a_X == "DEL":
                    cost.append("半径外输 ⇒ 尺度不定标（r151 结论）")
                if a_X == "REPLACE":
                    cost.append("放大半径到 2ƛ_C=2ħ/(mc)（真空门要求 r>ƛ_C）⇒ 放弃康普顿半径定标、"
                                "且 τ/κ=1 与 ωr=c 的取值需整体重调")
                out.append({"辐射": a_R, "力": a_F, "半径": a_X,
                            "life_ok": life_ok, "force_ok": force_ok,
                            "scale_ok": scale_ok, "vac_ok": vac_ok,
                            "E_over_Ec": ratio_val,
                            "valid": valid,
                            "cost": cost if cost else ["无代价"]})
    survivors = [x for x in out if x["valid"]]
    return {"enumeration": out, "n_total": len(out),
            "n_survivors": len(survivors), "survivors": survivors,
            "n_zero_cost": sum(1 for x in survivors if x["cost"] == ["无代价"])}


def D3_minimal():
    d2 = D2_repair_pricing()
    return {"n_survivors": d2["n_survivors"], "n_zero_cost": d2["n_zero_cost"],
            "survivors": d2["survivors"],
            "remaining_non_known": 0,
            "conclusion":
                "存活 %d 个、**零代价 0**；所有存活解都要求同时『改用 QED 虚过程』"
                "+『引入第五种力』+『放大半径』⇒ 施加后来料的螺旋骨架不再承担任何物理功能"
                " ⇒ **本库『修复即自杀』第六次复发**（须注明修复空间是低阶）"
                % d2["n_survivors"],
            "is_repair_equals_suicide": (d2["n_survivors"] > 0
                                         and d2["n_zero_cost"] == 0)}


# ============================================================
# 控制组
# ============================================================
def lep_control():
    """
    ★ 正对照：用 LEP2 的真实参数验证本卷的 Larmor 实现。
      LEP2：E = 104.5 GeV、弯转半径 ρ = 3096 m
      已知每圈能量损失 U₀ ≈ 88.46·E[GeV]⁴/ρ[m] keV
      P = U₀ / (2πρ/c)
    ★自抓（本卷自纠）：初版 γ = E_gev*1e9/(m c²) 漏乘 eV→J 换算（1 eV = Q_E J）
      ⇒ γ 虚高 6.24e18 倍、P_公式虚报 1.28e70 W ⇒ 假的控制组失败。已补 Q_E。
    """
    E_gev = 104.5
    rho = 3096.0
    gamma = E_gev * 1e9 * Q_E / (M_E * C * C)   # eV → J 再除以 mc²
    a = C * C / rho                     # 超相对论圆周运动：横向加速度
    P_formula = Q_E ** 2 * gamma ** 4 * a ** 2 / (6.0 * math.pi * EPS0 * C ** 3)
    U0_keV = 88.46 * E_gev ** 4 / rho       # 标准同步辐射损失公式
    U0_J = U0_keV * 1e3 * Q_E
    T_rev = 2.0 * math.pi * rho / C
    P_known = U0_J / T_rev
    return {"E_gev": E_gev, "rho": rho, "gamma": gamma,
            "U0_GeV": U0_keV / 1e6, "P_formula": P_formula,
            "P_known": P_known,
            "dev": abs(P_formula / P_known - 1.0)}


def control_group():
    out = []
    d = dynamics(M_E)

    # F1 Schwinger 极限自洽
    out.append(dict(id="F1",
                    desc="Schwinger 极限自洽：E_c = m²c³/(eħ) 必须与公布值 1.32e18 V/m 同量级",
                    value=d["E_crit"], expect="≈1.32e18",
                    ok=abs(d["E_crit"] / 1.323e18 - 1.0) < 1e-2))

    # F2 经典电子半径锚点
    r_e = K_E * Q_E * Q_E / (M_E * C * C)
    out.append(dict(id="F2", desc="经典电子半径锚点：r_e = ke²/(mc²) ≈ 2.817940e−15 m",
                    value=r_e, expect="2.817940e-15",
                    ok=abs(r_e / 2.817940e-15 - 1.0) < 1e-5))

    # F3 ★ LEP 正对照（证明 Larmor 实现正确）
    lep = lep_control()
    out.append(dict(id="F3",
                    desc="★LEP2 正对照：本卷 Larmor 实现必须复现 LEP 同步辐射功率"
                         "（E=104.5 GeV、ρ=3096 m）",
                    value=lep["dev"], expect="<5%",
                    ok=lep["dev"] < 0.05))

    # F4 反向控制：v<<c 时相对论与非相对论 Larmor 必须一致
    v_nr = 1.0e3
    a_nr = v_nr ** 2 / 1.0
    gamma_nr = 1.0 / math.sqrt(1.0 - (v_nr / C) ** 2)
    p_nr = Q_E ** 2 * a_nr ** 2 / (6.0 * math.pi * EPS0 * C ** 3)
    p_rel = Q_E ** 2 * gamma_nr ** 4 * a_nr ** 2 / (6.0 * math.pi * EPS0 * C ** 3)
    out.append(dict(id="F4",
                    desc="反向控制：v=1e3 m/s 时相对论 Larmor 必须退化为非相对论式",
                    value=abs(p_rel / p_nr - 1.0), expect="<1e-9",
                    ok=abs(p_rel / p_nr - 1.0) < 1e-9))

    # F5 库仑力锚点
    # ★自抓（本卷自纠）：初版阈值取 1e-12，低于 K_E 公布值舍入地板
    #   （CODATA K_E=8.9875517923(14)e9，末位 ±14 ⇒ 相对 ~1.6e-10；
    #     机读 ke²/r² 与 e²/(4πε₀r²) 偏差 4.32e-12 即该地板的实现）
    #   ⇒ 按 r154 纪律放宽到 1e-8（约 60 倍余量）并显式披露地板来源。
    r = d["r"]
    F_em_direct = Q_E ** 2 / (4.0 * math.pi * EPS0 * r * r)
    dev5 = abs(F_em_direct / d["F_em"] - 1.0)
    out.append(dict(id="F5",
                    desc="库仑力锚点：ke²/r² 必须与 e²/(4πε₀r²) 一致"
                         "（阈值按 K_E 公布值舍入地板 ~1.6e-10 取 1e-8）",
                    value=dev5, expect="<1e-8（舍入地板 4.3e-12 实测）",
                    ok=dev5 < 1e-8))

    # F6 电子寿命实验下限
    out.append(dict(id="F6", desc="已知锚点：电子寿命实验下限 > 6.6e28 yr",
                    value=E_LIFETIME_S, expect=">2e36 s",
                    ok=E_LIFETIME_S > 2.0e36))

    # F7 标度不变性：4 个质量点 E/E_c 必须恒为 2
    scan = B4_scan()
    out.append(dict(id="F7",
                    desc="标度不变性：4 个质量点的 E_needed/E_Schwinger 必须恒为 2",
                    value=scan["spread_ratio"], expect="<1e-9",
                    ok=scan["scale_invariant"]))

    # F8 引力/电磁强度比锚点（α_G）
    alpha_G = G * M_P * M_P / (HBAR * C)
    out.append(dict(id="F8",
                    desc="已知锚点：α_G = G m_p²/(ℏc) ≈ 5.9e−39（引力比电磁弱 39 个量级）",
                    value=alpha_G, expect="≈5.9e-39",
                    ok=abs(alpha_G / 5.9e-39 - 1.0) < 0.05))

    return out


def guards(led):
    g = []
    n = led.count()
    b1 = B1_reading_independence()
    a4 = A4_schwinger()
    d2 = D2_repair_pricing()
    g.append(("守卫1：条目数 ≥ 12", len(led.items) >= 12))
    g.append(("守卫2：存在 FAIL 条目", n.get("FAIL", 0) >= 1))
    g.append(("守卫3：控制组 ≥ 7 项", len(control_group()) >= 7))
    g.append(("守卫4：修复枚举数 = 27", d2["n_total"] == 27))
    g.append(("守卫5：辐射功率两读法必须**一致**（本卷论点成立的前提）",
              b1["identical"]))
    g.append(("守卫6：E/E_c 两读法必须**都 > 1**（换读法救不了）",
              a4["both_exceed"]))
    g.append(("守卫7：寿命缺口 > 40 个量级",
              math.log10(dynamics(M_E)["lifetime_gap"]) > 40.0))
    g.append(("守卫8：LEP 正对照通过（Larmor 实现无误）",
              lep_control()["dev"] < 0.05))
    return g


# ============================================================
# 台账
# ============================================================
class Ledger:
    def __init__(self):
        self.items = []

    def add(self, gid, title, status, metrics=None, note=""):
        self.items.append({"id": gid, "title": title, "status": status,
                           "metrics": metrics or {}, "note": note})

    def count(self):
        d = {}
        for it in self.items:
            d[it["status"]] = d.get(it["status"], 0) + 1
        return d

    def ok(self):
        return all(it["status"] != "GUARD-FAIL" for it in self.items)


def build_ledger():
    led = Ledger()

    a1 = A1_acceleration()
    led.add("A1", "向心加速度：坐标读法 4.654842e+29 m/s²（4.7467e+28 g）；"
                  "快度读法 1.551614e+29 m/s²",
            "FAIL", a1,
            "a_⊥ = v_⊥²/r；两种读法分别取 v_⊥=c 与 v_⊥=c/√3")

    a2 = A2_required_force()
    led.add("A2", "★所需向心力（单个电子）：坐标读法 **0.4240274 N**、"
                  "快度读法 **0.2448123 N**",
            "FAIL", a2,
            "F_⊥ = γ m a_⊥；坐标读法 γ 无定义取 m v_⊥²/r，快度读法 γ=√3")

    a3 = A3_force_sources()
    led.add("A3", "★力的来源枚举：电磁仅够 1/68.5、引力差 2.85e+44 倍、"
                  "强/弱不适用 ⇒ **四种已知力都提供不了**",
            "FAIL", {"rows": a3["rows"], "n_sources": a3["n_sources"],
                     "n_enough": a3["n_enough"],
                     "em_shortfall": a3["em_shortfall"],
                     "grav_shortfall": a3["grav_shortfall"]},
            "电磁 F_em = ke²/r² = 6.1886e−3 N；引力 F_grav = Gm²/r² = 1.4856e−45 N")

    a4 = A4_schwinger()
    led.add("A4", "★真空击穿：所需场强 / Schwinger 极限 = **2.0000000000（坐标）** 与 "
                  "**1.1547005384（快度）**，**两者都 > 1**，且**与质量无关**",
            "FAIL" if a4["both_exceed"] else "GUARD-FAIL",
            a4,
            "解析：E/E_c = ħ/(mcr)〔坐标〕、ħ/(√3 mcr)〔快度〕；代入 r=ħ/(2mc) 得 "
            "**2** 与 **2/√3**；r ∝ 1/m ⇒ mcr ≡ ħ/2 ⇒ **标度不变**。"
            "超 Schwinger 极限 ⇒ 真空自发产生正负电子对 ⇒ 模型不自洽")

    a5 = A5_identity()
    led.add("A5", "INFO：r/r_e = 1/(2α) = 68.518000 是**精确恒等式** ⇒ 降 INFO，不是预言",
            "INFO" if a5["is_identity"] else "GUARD-FAIL",
            a5, a5["derivation"])

    b1 = B1_reading_independence()
    led.add("B1", "★★γ⁴a_⊥² 在两种读法下**精确相等**（机读比值偏差 0）"
                  " ⇒ **辐射功率与读法无关 —— r153 的『换读法』救不了辐射**",
            "FAIL" if b1["identical"] else "GUARD-FAIL",
            b1,
            "γ⁴a²〔坐标〕=1·(c²/r)² = c⁴/r²；γ⁴a²〔快度〕=9·(c²/3r)² = c⁴/r² ⇒ 恒等")

    b2 = B2_power()
    led.add("B2", "★★同步辐射功率：P = e²c/(6πε₀r²) = **1.236855e+06 W**"
                  "（单个电子辐射 **1.24 兆瓦**）",
            "FAIL", b2,
            "闭式与两读法逐一核对一致；控制组 F3 用 LEP2 实测参数验证 Larmor 实现")

    b3 = B3_lifetime()
    led.add("B3", "★★寿命：τ = mc²/P = **6.619294e−20 s**；"
                  "实验下限 2.083e+36 s ⇒ **差 3.147e+55 倍（55.5 个量级）**",
            "FAIL" if b3["fails"] else "GUARD-FAIL",
            b3, "电子若真做此螺旋运动，将在 6.6e−20 s 内辐射掉全部静止能量")

    b4 = B4_scan()
    led.add("B4", "质量扫描（4 个质量点）：E/E_c 恒为 2.0000000000（标度不变）；"
                  "P ∝ m²、τ ∝ 1/m（质子 τ=3.605e−23 s）",
            "FAIL", {"rows": b4["rows"], "spread_ratio": b4["spread_ratio"],
                     "scale_invariant": b4["scale_invariant"],
                     "tau_monotone": b4["tau_monotone"]},
            "★与质量无关 ⇒ 不是『电子恰好特殊』，而是该几何结构的通病")

    b5 = B5_scaling_laws()
    led.add("B5", "标度律机读验证：P ∝ m²（偏差 %.2e）、τ ∝ 1/m（偏差 %.2e）"
                  % (b5["P_dev"], b5["tau_dev"]),
            "INFO" if (b5["P_scales_as_m2"] and b5["tau_scales_as_1_over_m"])
            else "GUARD-FAIL",
            b5, "P = e²c/(6πε₀r²)、r ∝ 1/m ⇒ P ∝ m²；τ = mc²/P ∝ m/m² = 1/m"
                 "（★初版误写 1/m³，机读 tau_dev=0.9999997 抓出后自纠）")

    c1 = C1_radiation_dilemma()
    led.add("C1", "★两难①（辐射）：真实经典加速 ⇒ 必辐射（1.24 MW / 6.6e−20 s，"
                  "与观测差 55 个量级）；虚过程/不辐射 ⇒ 放弃来料核心图像",
            "FAIL" if c1["both_unfavorable"] else "GUARD-FAIL",
            c1, "用两难形式封住『QED 中 Zitterbewegung 不辐射』这条退路")

    c2 = C2_force_dilemma()
    led.add("C2", "★两难②（力）：第五种力（≥68.5×电磁、2.85e44×引力）⇒ 从未被观测；"
                  "无力 ⇒ 违反牛顿第一定律 / 测地线运动",
            "FAIL" if c2["both_unfavorable"] else "GUARD-FAIL",
            c2, "两种都不利 ⇒ 规避『来料是否指定了束缚机制』的归属争议")

    c3 = C3_classical_caveat()
    led.add("C3", "BOUNDARY：Larmor 是经典公式（防过度指控，已由 C1 两难封住）",
            "BOUNDARY", c3, c3["note"])

    d1 = D1_parameter_gate()
    led.add("D1", "参数计数门：n_自由=0 ≤ n_观测−1=1？通过；但两项观测（寿命、"
                  "Schwinger）**皆未通过**；SU(5) 控制组 2≤2 通过",
            "FAIL", d1,
            "★诚实区分：参数计数门本身通过（自由度耗尽问题在本卷不是主要指控），"
            "真正的指控是**动力学不自洽**")

    d2 = D2_repair_pricing()
    led.add("D2", "修复定价：三根支柱 × {KEEP,DEL,REPLACE} = 27 ⇒ 存活 %d、零代价 %d"
                  % (d2["n_survivors"], d2["n_zero_cost"]),
            "FAIL" if d2["n_zero_cost"] == 0 else "GUARD-FAIL",
            {"n_total": d2["n_total"], "n_survivors": d2["n_survivors"],
             "n_zero_cost": d2["n_zero_cost"], "survivors": d2["survivors"]},
            "存活要求：寿命达标 ∧ 有力机制 ∧ 尺度定标 ∧ 不击穿真空")

    d3 = D3_minimal()
    led.add("D3", "最小完备修复集：%s" % d3["conclusion"],
            "FAIL" if d3["is_repair_equals_suicide"] else "GUARD-FAIL",
            {"n_survivors": d3["n_survivors"], "n_zero_cost": d3["n_zero_cost"],
             "remaining_non_known": d3["remaining_non_known"]},
            "★须注明修复空间是**低阶**（3 个三值算子的笛卡尔积），高阶新增型未枚举")

    led.add("G1", "BOUNDARY：『束缚机制』的归属由本卷代为枚举",
            "BOUNDARY",
            {"note": "来料未指定维持螺旋的力是什么；本卷枚举四种已知力并全部排除"},
            "若来料另行指定机制，需按其给出的力重算；但所需量级 0.24–0.42 N 不变")

    led.add("G2", "BOUNDARY：未处理量子辐射反作用与自能重整化",
            "BOUNDARY",
            {"note": "本卷全为经典电动力学；QED 的 Zitterbewegung 不辐射已由 C1 两难处理"},
            "本卷缺口是 **55 个量级**，任何微扰修正都无法弥补")

    led.add("G3", "BOUNDARY：Schwinger 极限取真空（无外场）情形",
            "BOUNDARY",
            {"note": "若来料主张该区域不是真空（如『空间本身』另有结构），"
                     "需重新定义击穿阈值"},
            "但所需场强 2.65e18 V/m 与 E_c 同量级这一事实不变")

    led.add("G4", "BOUNDARY：未处理引力自能（Poisson 层次）",
            "BOUNDARY",
            {"note": "本卷只用牛顿自作用量级；未做 GR/泊松层次修正"},
            "引力比所需小 2.85e44 倍，任何修正都无法跨 44 个量级")

    return led


# ============================================================
# 报告
# ============================================================
def build_report(led):
    L = []
    A = L.append
    A("=" * 96)
    A("TUFT-r155｜螺旋的【动力学层】：束缚力缺口 · 真空击穿 · 同步辐射判决")
    A("=" * 96)
    A("生成时刻: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    A("")
    A("【定位】前四卷判几何/读法/参数/可检验量；**本卷第一次判动力学**：")
    A("        (1) 维持这个螺旋需要多大的力？谁提供？会不会击穿真空？")
    A("        (2) 它会辐射掉多少能量？电子还能活多久？")
    A("【关键】本卷结论**与读法无关** ⇒ r153 的『换读法』救不了它（见 B1）。")
    A("")

    for it in led.items:
        A("[%s] %-11s %s" % (it["id"], it["status"], it["title"]))
        if it["note"]:
            A("      " + it["note"])
        for k, v in it["metrics"].items():
            if k in ("rows", "enumeration", "survivors", "note"):
                continue
            if isinstance(v, float):
                A("      %s = %s" % (k, "%.6e" % v))
            else:
                A("      %s = %s" % (k, v))
        A("")

    d = dynamics(M_E)
    A("-" * 96)
    A("【A 组 · 向心加速度与束缚力缺口（电子）】")
    A("    r             = %.6e m" % d["r"])
    A("    a_⊥(坐标)      = %.6e m/s² = %.6e g" % (d["a_coord"], d["a_coord"] / 9.80665))
    A("    a_⊥(快度)      = %.6e m/s² = %.6e g" % (d["a_proper"], d["a_proper"] / 9.80665))
    A("    F_需(坐标)     = %.6e N" % d["F_coord"])
    A("    F_需(快度)     = %.6e N" % d["F_proper"])
    A("")
    A("    力的来源                        F (N)            与所需之比（坐标 / 快度）")
    for row in A3_force_sources()["rows"]:
        fv = ("%.6e" % row["F"]) if row["F"] is not None else "—"
        rc = ("%.4e" % row["ratio_vs_coord"]) if row["ratio_vs_coord"] is not None else "—"
        rp = ("%.4e" % row["ratio_vs_proper"]) if row["ratio_vs_proper"] is not None else "—"
        A("    %-28s %-17s %s / %s" % (row["source"], fv, rc, rp))
    A("    ★ **四种已知力都提供不了**（电磁仅 1/68.5、引力差 2.85e+44 倍）")
    A("")
    A("    Schwinger 极限 E_c   = %.6e V/m" % d["E_crit"])
    A("    所需场强 E(坐标)      = %.6e V/m   ⇒ E/E_c = %.10f" % (d["E_req_coord"], d["ratio_schwinger_coord"]))
    A("    所需场强 E(快度)      = %.6e V/m   ⇒ E/E_c = %.10f" % (d["E_req_proper"], d["ratio_schwinger_proper"]))
    A("    ★ 解析值：2 与 2/√3=1.1547005384；**两者都 > 1 ⇒ 真空击穿**")
    A("")

    A("-" * 96)
    A("【B 组 · 同步辐射（本卷最硬）】")
    b1 = B1_reading_independence()
    b2 = B2_power()
    b3 = B3_lifetime()
    A("    γ⁴a²(坐标)  = %.6e" % b1["gamma4_a2_coord"])
    A("    γ⁴a²(快度)  = %.6e" % b1["gamma4_a2_proper"])
    A("    c⁴/r²       = %.6e" % b1["c4_over_r2"])
    A("    ★ 两读法相对差 = %.3e ⇒ **精确相等 ⇒ P 与读法无关**" % b1["rel_gap"])
    A("")
    A("    P(坐标)      = %.6e W" % b2["P_coord"])
    A("    P(快度)      = %.6e W" % b2["P_proper"])
    A("    P(闭式)      = %.6e W = %.6f **兆瓦**" % (b2["P_closed"], b2["P_closed"] / 1e6))
    A("")
    A("    m_e c²       = %.6e J" % b3["mc2"])
    A("    τ = mc²/P    = %.6e s" % b3["tau"])
    A("    实验下限      = %.6e s（6.6e28 yr）" % b3["exp_lower_bound_s"])
    A("    ★ 缺口        = %.6e 倍 = **%.2f 个量级**" % (b3["gap"], b3["gap_in_orders"]))
    A("")

    A("-" * 96)
    A("【质量扫描（4 个质量点）】")
    A("    对象            r (m)          P (W)          τ (s)          E/E_c")
    for row in B4_scan()["rows"]:
        A("    %-14s %.6e   %.6e   %.6e   %.10f"
          % (row["name"], row["r"], row["P"], row["tau"], row["ratio_schwinger"]))
    A("    ★ E/E_c 离散度 = %.3e ⇒ **标度不变**（与质量无关）" % B4_scan()["spread_ratio"])
    A("")

    A("-" * 96)
    A("【控制组】")
    allok = True
    for c in control_group():
        try:
            vs = "%.6e" % c["value"]
        except Exception:
            vs = str(c["value"])
        A("    %s %-6s %s" % (c["id"], "PASS" if c["ok"] else "FAIL", c["desc"]))
        A("         实测 %s  期望 %s" % (vs, c["expect"]))
        allok = allok and c["ok"]
    lep = lep_control()
    A("    [LEP 正对照明细] E=%.1f GeV  ρ=%.0f m  γ=%.4e  U₀=%.4f GeV  "
      "P_公式=%.6e W  P_已知=%.6e W  偏差=%.4f"
      % (lep["E_gev"], lep["rho"], lep["gamma"], lep["U0_GeV"],
         lep["P_formula"], lep["P_known"], lep["dev"]))
    A("    控制组小结: %s" % ("全部通过" if allok else "存在失败"))
    A("")

    A("-" * 96)
    A("【守卫】")
    for n, o in guards(led):
        A("    %s  %s" % ("OK  " if o else "FAIL", n))
    A("")

    A("=" * 96)
    cnt = led.count()
    A("【条目统计】" + "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
    A("=" * 96)
    return "\n".join(L), allok


# ============================================================
# 判定册
# ============================================================
def build_judge(led, allok):
    cnt = led.count()
    d = dynamics(M_E)
    b2 = B2_power()
    b3 = B3_lifetime()
    d2 = D2_repair_pricing()
    lep = lep_control()
    verdict = "HELIX-DYNAMICALLY-IMPOSSIBLE-FORCE-VACUUM-AND-RADIATION"

    m = []
    a = m.append
    a("# 判定册 TUFT-r155｜螺旋的【动力学层】：束缚力缺口 · 真空击穿 · 同步辐射判决")
    a("")
    a("- 编号：TUFT-r155")
    a("- 生成时刻：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    a("- 引擎：`源码/TUFT-r155_螺旋束缚力缺口_真空击穿与同步辐射判决_2026-10-22.py`")
    a("- 控制组：%s" % ("全部通过" if allok else "存在失败"))
    a("- 条目统计：%s" % "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
    a("")
    a("## 00. 编号碰撞处置表")
    a("")
    a("| 编号 | 占用者 | 处置 |")
    a("|------|--------|------|")
    a("| r150 | 自旋-2 卷 | 保留为权威 |")
    a("| r151 | 双约束求导证明卷 | 保留为权威 |")
    a("| r152 | ω f h c f 完整关系组卷 | 保留为权威 |")
    a("| r153 | 读法空间穷举卷 | 保留为权威 |")
    a("| r154 | 存活分支终局清点卷 | 保留为权威 |")
    a("| r155 | **本卷**（动力学层） | 实测首空号后启用 |")
    a("")
    a("## 01. 分工声明（★ 五卷条目不可相加）")
    a("")
    a("| 卷 | 层 | 判的是什么 |")
    a("|----|----|-----------|")
    a("| r151 | 式子层 | 两式 {v=c, ωr=c} ⇒ 退化为圆 |")
    a("| r152 | 式子层 | 三式 ⇒ √2·c 超光速 |")
    a("| r153 | 读法层 | 读法穷举 ⇒ 三式组健康解 0 |")
    a("| r154 | 后果层 | 存活分支的磁矩 / 静止能量 |")
    a("| **r155** | **动力学层** | **力从哪来 · 会不会击穿真空 · 辐射多少** |")
    a("")
    a("## 02. 判词")
    a("")
    a("`%s`" % verdict)
    a("")
    a("**这个螺旋在动力学上不可能存在：没有已知力能束缚它，"
      "束缚它所需的场强恒超真空击穿极限，而它一旦真实存在就会在 6.6×10⁻²⁰ 秒内辐射殆尽。**")
    a("")
    a("## 03. 核心结论")
    a("")
    a("### 3.1 束缚力缺口")
    a("")
    a("- 所需向心力：**%.6e N**（坐标读法）/ **%.6e N**（快度读法）—— 单个电子。"
      % (d["F_coord"], d["F_proper"]))
    a("- 向心加速度：%.6e m/s² = %.4e g。" % (d["a_coord"], d["a_coord"] / 9.80665))
    a("")
    a("| 来源 | 力 (N) | 与所需之比 |")
    a("|---|---|---|")
    for row in A3_force_sources()["rows"]:
        fv = ("%.6e" % row["F"]) if row["F"] is not None else "不适用"
        rc = ("%.4e" % row["ratio_vs_coord"]) if row["ratio_vs_coord"] is not None else "—"
        a("| %s | %s | %s |" % (row["source"], fv, rc))
    a("")
    a("**四种已知力都提供不了**（电磁仅 1/68.5、引力差 2.85e+44 倍、电子不参与强作用、弱作用力程太短）。")
    a("")
    a("### 3.2 ★真空击穿（标度不变的硬结论）")
    a("")
    a("- Schwinger 临界场强 E_c = m²c³/(eħ) = **%.6e V/m**" % d["E_crit"])
    a("- 所需场强：坐标 **%.6e V/m**、快度 **%.6e V/m**" % (d["E_req_coord"], d["E_req_proper"]))
    a("- **E/E_c = %.10f（坐标）与 %.10f（快度）**，解析值 **2** 与 **2/√3**。"
      % (d["ratio_schwinger_coord"], d["ratio_schwinger_proper"]))
    a("- 解析：E/E_c = ħ/(mcr)，代入 r = ħ/(2mc) ⇒ **恒等于 2**；"
      "r ∝ 1/m ⇒ mcr ≡ ħ/2 ⇒ **与质量无关**（4 个质量点机读全是 2.0000000000）。")
    a("- **两者都 > 1** ⇒ 换读法也救不了 ⇒ 真空会自发产生正负电子对。")
    a("")
    a("### 3.3 ★★同步辐射（与读法无关）")
    a("")
    a("- **γ⁴a_⊥² 在两种读法下精确相等**（机读相对差 %.3e）："
      % B1_reading_independence()["rel_gap"])
    a("  γ⁴a²〔坐标〕= 1·(c²/r)² = c⁴/r²；γ⁴a²〔快度〕= 9·(c²/3r)² = c⁴/r²。")
    a("  ⇒ **P ≡ e²c/(6πε₀r²)，与读法无关 —— r153 的『换读法』救不了辐射。**")
    a("- **P = %.6e W = %.6f 兆瓦**（单个电子）。"
      % (b2["P_closed"], b2["P_closed"] / 1e6))
    a("- **τ = m_ec²/P = %.6e s**；实验下限 %.3e s（6.6e28 yr）。"
      % (b3["tau"], b3["exp_lower_bound_s"]))
    a("- **缺口 %.3e 倍 = %.2f 个量级。**" % (b3["gap"], b3["gap_in_orders"]))
    a("")
    a("### 3.4 两难（防过度指控，两条退路都封住）")
    a("")
    a("- **两难①（辐射）**：真实经典加速 ⇒ 必辐射（1.24 MW / 6.6e−20 s，差 55 量级）；"
      "改口说是 QED 虚过程不辐射 ⇒ 那就不是来料主张的『真实的空间螺旋运动』，"
      "也不能用它解释电磁场起源。")
    a("- **两难②（力）**：引入第五种力（≥68.5×电磁、2.85e44×引力）⇒ 从未被观测；"
      "说没有力 ⇒ 违反牛顿第一定律 / 测地线运动。")
    a("")
    a("### 3.5 修复定价（27 枚举）")
    a("")
    a("- 存活 **%d**、**零代价 %d**" % (d2["n_survivors"], d2["n_zero_cost"]))
    a("- 所有存活解都要求同时：改用 QED 虚过程 + 引入第五种力 + 放大半径")
    a("  ⇒ 施加后来料的螺旋骨架不再承担任何物理功能"
      " ⇒ **本库『修复即自杀』第六次复发**（须注明修复空间是低阶）。")
    a("")
    a("## 04. 机读证据")
    a("")
    a("```")
    a("r                = %.6e m" % d["r"])
    a("a_⊥(坐标)         = %.6e m/s²  (%.4e g)" % (d["a_coord"], d["a_coord"] / 9.80665))
    a("F_需(坐标/快度)    = %.6e / %.6e N" % (d["F_coord"], d["F_proper"]))
    a("F_em             = %.6e N  (仅 %.4e of 所需)" % (d["F_em"], d["ratio_em_coord"]))
    a("F_grav           = %.6e N  (差 %.4e 倍)" % (d["F_grav"], d["ratio_grav_coord"]))
    a("E_c              = %.6e V/m" % d["E_crit"])
    a("E/E_c (坐标/快度)  = %.10f / %.10f" % (d["ratio_schwinger_coord"], d["ratio_schwinger_proper"]))
    a("γ⁴a² 两读法相对差  = %.3e" % B1_reading_independence()["rel_gap"])
    a("P                = %.6e W  (%.6f MW)" % (b2["P_closed"], b2["P_closed"] / 1e6))
    a("τ                = %.6e s" % b3["tau"])
    a("寿命缺口          = %.6e 倍 (%.2f 量级)" % (b3["gap"], b3["gap_in_orders"]))
    a("E/E_c 四质量离散度 = %.3e" % B4_scan()["spread_ratio"])
    b5m = B5_scaling_laws()
    a("τ 标度（质子/电子） = %.6f = 质量比 %.6f（偏差 %.2e）⇒ **τ ∝ 1/m**"
      % (b5m["tau_ratio"], b5m["m1_ratio"], b5m["tau_dev"]))
    a("A5 恒等式：同源常数偏差 %.3e（机器零）；与公布 α 偏差 %.3e（舍入地板，BOUNDARY）"
      % (A5_identity()["dev_internal"], A5_identity()["dev_published_rel"]))
    a("LEP 正对照偏差     = %.6f (P_公式 %.4e W vs P_已知 %.4e W, γ=%.6e)"
      % (lep["dev"], lep["P_formula"], lep["P_known"], lep["gamma"]))
    a("修复 27 组合       存活 %d / 零代价 %d" % (d2["n_survivors"], d2["n_zero_cost"]))
    a("```")
    a("")
    a("## 05. 未闭合项（禁止外推）")
    a("")
    a("1. **束缚机制的归属由本卷代为枚举**（来料未指定）；若来料另行指定，需按其力重算，"
      "但所需量级 0.24–0.42 N 不变。")
    a("2. **未处理量子辐射反作用与自能重整化**；QED 的 Zitterbewegung 不辐射已由 C1 两难封住。"
      "本卷缺口是 **55 个量级**，任何微扰修正都无法弥补。")
    a("3. **Schwinger 极限取真空（无外场）情形**；若来料主张该区域另有结构，需重定义阈值，"
      "但所需场强与 E_c 同量级这一事实不变。")
    a("4. **未处理引力自能（泊松/GR 层次）**；引力比所需小 2.85e44 倍，任何修正都无法跨 44 量级。")
    a("5. **修复空间是低阶**（27 组合），高阶新增型未枚举。")
    a("6. 本卷**不**宣称靶体系已被完全证伪 —— 只判决：")
    a("   **该螺旋在动力学上不可能存在，且此结论与读法无关。**")
    a("")
    a("## 06. 自抓与更正（机读/控制组抓出的本卷自身缺陷，全部已修）")
    a("")
    a("**初版引擎以退出码 2 中止（控制组 F3/F5 失败、守卫 8 失败、B5/A5 两项 GUARD-FAIL）。"
      "按「控制组失败先分代码错还是期望错」纪律逐项排查，五处全部是本卷自身缺陷：**")
    a("")
    a("1. **F3 LEP 正对照 · 单位 bug（代码错）**：γ = E[GeV]·1e9/(m c²) 漏乘 eV→J 换算"
      "（1 eV = Q_E J）⇒ γ 虚高 **6.24e18** 倍、P_公式虚报 **1.28e70 W**"
      "（对照值 8.41e−06 W）⇒ 假的控制组失败。补乘 Q_E 后 γ=2.045e+05，"
      "P_公式/P_已知 偏差 **3.1e−05**（<5% 门限）。LEP 锚点本身（U₀=3.4073 GeV/圈）"
      "经两条独立路径互证，期望值无误。")
    a("2. **B5 标度律 · 分析笔误（卷作者错，机读抓出）**：初版把 τ 标度写成 **1/m³**，"
      "但 τ = mc²/P、P ∝ m² ⇒ τ ∝ m/m² = **1/m**。机读 tau_dev = **0.9999997**"
      "（质子/电子 τ 比 1836.15 = 质量比，而非质量比³ 6.19e9）立即抓出。"
      "已改为 1/m 并机读确认。**保留此记录：判据抓出了卷作者自己的分析错误。**")
    a("3. **A5 恒等式 · 阈值低于常数舍入地板（门限错）**：初版以**绝对**阈值 1e-9 判"
      " r/r_e（量级 68.5）≡ 1/(2α_公布)，相对门限 1.5e-11，远低于公布常数舍入地板"
      "（K_E 末位 ±14、α 末位 ±11，各自相对 ~1.5e-10；机读相对偏差 6.1e-10）"
      "⇒ 恒等式被误判为不成立。已改为**同源常数**机检"
      "（α_implied = K_E q²/(ħc)，偏差机器零）+ 与公布 α 的偏差登记 BOUNDARY。"
      "**这是 r154「常数舍入地板」纪律在本卷的第二次实例（不同常数对）。**")
    a("4. **F5 库仑锚点 · 同一族门限错**：阈值 1e-12 低于 K_E 舍入地板"
      "（机读 ke²/r² vs e²/(4πε₀r²) 偏差 **4.32e-12** 即该地板的实现）"
      "⇒ 放宽到 1e-8 并披露地板来源。**与 A5 同源：都是「用公布常数的两种"
      "互相独立的舍入表示做相等性判断」时忘了留舍入余量。**")
    a("5. **D2 修复枚举 · 注释与代码不一致（文档错）**：注释写「放大到 ħ/(mc)」，"
      "代码实为 2ħ/(mc) = 2ƛ_C。已统一为 2ƛ_C 并注明真空门最小需求 r > ƛ_C。"
      "结论不受影响（任何 r > ƛ_C 均过真空门，存活解计数不变）。")
    a("")
    a("## 07. 红线")
    a("")
    a("- 数学自洽 ≠ 实验证实。")
    a("- **几何可行 ≠ 动力学可行**（本卷与前四卷的分工）。")
    a("- **修复可行 ≠ 修复后仍有内容**（第六次复发）。")
    a("- 防过度指控与防漏判同等重要：Larmor 的经典性已由 C1 两难处理，"
      "r/r_e=1/(2α) 已诚实降为 INFO。")
    a("")
    return "\n".join(m), verdict


def main():
    led = build_ledger()
    report, allok = build_report(led)
    print(report)

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.abspath(os.path.join(here, "..", "数据"))
    os.makedirs(outdir, exist_ok=True)
    base = "TUFT-r155_螺旋束缚力缺口_真空击穿与同步辐射判决_2026-10-22"
    verdict_j = "HELIX-DYNAMICALLY-IMPOSSIBLE-FORCE-VACUUM-AND-RADIATION"

    payload = {
        "id": "TUFT-r155",
        "title": "螺旋的【动力学层】：束缚力缺口 · 真空击穿 · 同步辐射判决",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict_j,
        "counts": led.count(),
        "controls_ok": allok,
        "items": led.items,
        "dynamics_electron": dynamics(M_E),
        "scan": B4_scan()["rows"],
        "lep_control": lep_control(),
        "controls": control_group(),
        "guards": [{"name": n, "ok": bool(o)} for n, o in guards(led)],
    }

    with open(os.path.join(outdir, base + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(os.path.join(outdir, base + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)

    md, verdict = build_judge(led, allok)
    with open(os.path.join(outdir, base + ".md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(outdir, "判定_" + base + ".md"), "w", encoding="utf-8") as f:
        f.write(md)

    print("\n[已写出] " + os.path.join(outdir, base + ".json"))
    print("[已写出] " + os.path.join(outdir, base + ".md"))
    print("[已写出] " + os.path.join(outdir, base + "_report.txt"))
    print("[已写出] " + os.path.join(outdir, "判定_" + base + ".md"))
    return 0 if (allok and led.ok()) else 2


if __name__ == "__main__":
    sys.exit(main())
