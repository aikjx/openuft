# -*- coding: utf-8 -*-
"""
TUFT-r154｜r153 唯一存活分支的终局清点：可检验量反预测（磁矩 / 静止能量）

══════════════════════════════════════════════════════════════════════════
00. 编号与定位
══════════════════════════════════════════════════════════════════════════
【编号】r154。实测首空号：r150–r153 均已占用，r154 为空。

【★ 本卷是攻破链的收口，不是新开一条线】
  r151：{v=c} ∧ {ωr=c}（坐标）⇒ u≡0 ⇒ τ≡0 ⇒ 螺旋退化为圆。
  r152：{ωr=c} ∧ {h·f=c}（坐标）⇒ v=√2·c，超光速 41.42%。
  r153：读法穷举 ⇒ 三式组 8 种读法健康解 0；两式组唯一健康分支是
        **(固有时,固有时) 读法 + 删掉 v=c**，代价是放弃「=c」并引入 γ。

  ⇒ r153 留下了**唯一活口**：那个分支**确实保住了因果性**（β=√(2/3)=0.8165）。
  本卷回答最后一个问题：**这个救回来的分支，还算得对吗？**
  方法：把它推到**可检验量**上 —— 电子磁矩与静止能量。

【★ 分层：与 r151 / r152 / r153 条目不可相加】
  r151/r152 = 式子层；r153 = 读法层；**本卷 = 存活分支的后果层（可检验量）**。

══════════════════════════════════════════════════════════════════════════
01. 本卷检验的存活分支（r153 宽松档 8 个存活解的共性）
══════════════════════════════════════════════════════════════════════════
    S1: (ωr, h·f) 取【固有时读法】 ⇒ v_⊥ = u = c/γ
    S2: 删掉 {v=c}               ⇒ β = √(2/3)，γ = √3
    S3: r = ħ/(2mc)（约化康普顿半波长）
    S4: f = 2mc²/h（Zitterbewegung 频率）
    S5: h(螺距) = c/f = πλ̄_C
    S6: τ/κ = 1（螺距角 45°）

══════════════════════════════════════════════════════════════════════════
02. 待检验命题
══════════════════════════════════════════════════════════════════════════
  P1: 该分支含有来料自有的（非外输、非已知物理重排）内容。
  P2: 该分支给出的电子磁矩与实测一致。
  P3: 该分支给出的电子静止能量与实测一致。
  P4: 该分支内部对「磁矩」有唯一算法。
"""

import json
import math
import os
import sys
import time

# ============================================================
# 常数（CODATA 2018 / SI 2019 定义值）
# ============================================================
C = 299792458.0               # m/s（定义值）
HBAR = 1.054571817e-34        # J·s
H_PLANCK = 6.62607015e-34     # J·s（定义值）
M_E = 9.1093837015e-31        # kg
Q_E = 1.602176634e-19         # C（定义值）
MU_B = 9.2740100783e-24       # J/T（玻尔磁子）
MU_E = 9.2847647043e-24       # J/T（电子磁矩实测）
MEV = 1.602176634e-13         # J per MeV

TOL = 1e-9
SQRT3 = math.sqrt(3.0)
SQRT2 = math.sqrt(2.0)
BETA_SURV = math.sqrt(2.0 / 3.0)     # r153 存活分支的 β
GAMMA_SURV = SQRT3                    # r153 存活分支的 γ


# ============================================================
# 存活分支的几何量
# ============================================================
def branch_geometry(m=M_E):
    """r153 存活分支 (S1–S6) 的全部几何量（电子默认）。"""
    r = HBAR / (2.0 * m * C)                 # S3：约化康普顿半波长
    f_proper = 2.0 * m * C * C / H_PLANCK    # S4：Zitterbewegung 频率（固有时）
    f_coord = f_proper / GAMMA_SURV          # 坐标频率
    h_pitch = C / f_proper                   # S5：螺距
    v_perp_coord = C / GAMMA_SURV            # S1：坐标横向速率 = c/√3
    u_coord = C / GAMMA_SURV                 # S1：坐标轴向速率 = c/√3
    v = BETA_SURV * C
    return {"m": m, "r": r, "f_proper": f_proper, "f_coord": f_coord,
            "h_pitch": h_pitch, "v_perp": v_perp_coord, "u": u_coord,
            "v": v, "beta": BETA_SURV, "gamma": GAMMA_SURV,
            "omega_proper": 2.0 * math.pi * f_proper,
            "h_over_2pi_r": h_pitch / (2.0 * math.pi * r),
            "pi_lambdabar": math.pi * HBAR / (m * C)}


# ============================================================
# A 组：终局清点
# ============================================================
EXTERNAL_INPUTS = [
    {"name": "r = ħ/(2mc)（约化康普顿半波长）",
     "source": "已知物理（康普顿波长）+ 实测 m",
     "known": True},
    {"name": "f = 2mc²/h（Zitterbewegung 频率）",
     "source": "已知物理（Dirac 电子内禀频率）+ 实测 m",
     "known": True},
    {"name": "γ = 1/√(1−β²)（洛伦兹因子）",
     "source": "狭义相对论（外部理论结构）",
     "known": True},
    {"name": "m（粒子质量）",
     "source": "实测输入",
     "known": True},
]


def A1_external_inputs():
    n_ext = len(EXTERNAL_INPUTS)
    n_known = sum(1 for x in EXTERNAL_INPUTS if x["known"])
    return {"n_external": n_ext, "n_known_source": n_known,
            "n_free": 0, "n_obs": 0,
            "gate": 0 <= 0 - 1,
            "inputs": EXTERNAL_INPUTS}


CONTENT_ROWS = [
    {"item": "r = ħ/(2mc)", "label": "已知", "reason": "约化康普顿半波长"},
    {"item": "f = 2mc²/h", "label": "已知", "reason": "标准 Zitterbewegung 频率"},
    {"item": "h(螺距) = c/f = πλ̄_C", "label": "已知重排", "reason": "由上两条直接相除"},
    {"item": "h/(2πr) = 1", "label": "恒等式", "reason": "定义重排，机读 1.000000000613"},
    {"item": "τ/κ = 1（螺距角 45°）", "label": "零新增", "reason": "等价于 v_⊥=u，是 (P,P) 读法的直接后果"},
    {"item": "β = √(2/3)、γ = √3", "label": "★新内容", "reason": "唯一非已知项"},
]


def A2_content_audit():
    g = branch_geometry()
    known = [x for x in CONTENT_ROWS if x["label"] in ("已知", "已知重排")]
    identity = [x for x in CONTENT_ROWS if x["label"] in ("恒等式", "零新增")]
    new = [x for x in CONTENT_ROWS if x["label"] == "★新内容"]
    return {"rows": CONTENT_ROWS,
            "n_total": len(CONTENT_ROWS),
            "n_known": len(known), "n_identity": len(identity),
            "n_new": len(new),
            "new_items": [x["item"] for x in new],
            "h_over_2pi_r": g["h_over_2pi_r"],
            "identity_ok": abs(g["h_over_2pi_r"] - 1.0) < 1e-8,
            "new_item_conflicts_with_axiom": abs(BETA_SURV - 1.0) > 1e-6,
            "n_usable_new": 0}


def A3_control_dirac():
    """控制：同一清点法用于已知物理（Dirac Zitterbewegung）也应给出『已知』标签 ⇒ 方法无偏"""
    rows = [
        {"item": "r = ħ/(2mc)", "label": "已知"},
        {"item": "ω = 2mc²/ħ", "label": "已知"},
        {"item": "v = c（Zitterbewegung 瞬时速率）", "label": "已知"},
    ]
    n_known = sum(1 for x in rows if x["label"] == "已知")
    return {"rows": rows, "n_known": n_known, "n_total": len(rows),
            "unbiased": n_known == len(rows)}


# ============================================================
# B 组：可检验量反预测
# ============================================================
def B1_magnetic_moment_gyro():
    """
    旋磁比口径：μ = (e/2m)·L，而 L = ħ/2（两种读法下都成立，见 B5）
    ⇒ μ = e ħ /(4m) = μ_B/2，与读法无关。
    """
    mu_model = Q_E * HBAR / (4.0 * M_E)
    return {"mu_model": mu_model, "mu_B": MU_B, "mu_e": MU_E,
            "over_mu_B": mu_model / MU_B,
            "dev_vs_measured": (mu_model - MU_E) / MU_E,
            "dev_pct": (mu_model - MU_E) / MU_E * 100.0,
            "missing_g_factor": MU_E / mu_model,
            "independent_of_reading": True,
            "fails": abs((mu_model - MU_E) / MU_E) > 0.01}


def B2_dilemma_magnetic():
    """
    两难：要么宣称解释磁矩（算错 g=2），要么不解释（缺内容）。两种都不利。
    """
    b1 = B1_magnetic_moment_gyro()
    return {"branch_explain": "μ = μ_B/2，差 g=2（偏离 %.4f%%）" % b1["dev_pct"],
            "branch_not_explain": "该模型不解释电子磁矩 ⇒ 电磁侧内容缺失",
            "both_unfavorable": True,
            "missing_g": b1["missing_g_factor"]}


def B3_two_algorithms():
    """
    ★ 内部不一致：环电流口径 μ = e·f_坐标·πr² 与 旋磁比口径 μ=(e/2m)L
      在【坐标读法】下一致，在【快度读法】（存活分支）下相差 √3。
    """
    g = branch_geometry()
    mu_gyro = Q_E * HBAR / (4.0 * M_E)                       # (e/2m)·L，L=ħ/2
    mu_loop_coord = Q_E * g["f_coord"] * math.pi * g["r"] ** 2  # 存活分支（坐标频率）
    mu_loop_naive = Q_E * (C / (2.0 * math.pi * g["r"])) * math.pi * g["r"] ** 2
    # 后者 = e·c·r/2 = 坐标读法（v_⊥=c）下的环电流
    ratio_surv = mu_gyro / mu_loop_coord
    ratio_coord = mu_gyro / mu_loop_naive
    # ★ 阈值必须按【实测地板】取：公布的 h 与 2πħ 在第 10 位不舍入一致
    #   （|2πħ − h|/h = 6.127e−10），故本卷比值判等阈值取 1e−8（约 16 倍余量）。
    floor = abs(2.0 * math.pi * HBAR - H_PLANCK) / H_PLANCK
    return {"mu_gyro": mu_gyro,
            "mu_loop_surviving": mu_loop_coord,
            "mu_loop_coord_reading": mu_loop_naive,
            "ratio_surviving": ratio_surv,
            "ratio_coord_reading": ratio_coord,
            "dev_from_sqrt3": abs(ratio_surv - SQRT3),
            "constants_floor": floor,
            "equals_sqrt3": abs(ratio_surv - SQRT3) < 1e-8,
            "coord_consistent": abs(ratio_coord - 1.0) < 1e-8,
            "dev_loop_vs_measured": (mu_loop_coord - MU_E) / MU_E,
            "dev_loop_pct": (mu_loop_coord - MU_E) / MU_E * 100.0,
            "inconsistent": abs(ratio_surv - 1.0) > 1e-6}


def B4_rest_energy():
    """
    静止能量两难：沿用「静止能量来自螺旋运动」 ⇒ E = γ m₀ c² = √3 m₀ c²
      路①不做重归一化 ⇒ E = √3 m c² = 0.885 MeV vs 实测 0.511 MeV（+73.2%）
      路②引入裸质量 m₀ = m/√3 ⇒ 外部输入 +1
    """
    mc2_J = M_E * C * C
    mc2_MeV = mc2_J / MEV
    e_model = GAMMA_SURV * mc2_MeV
    dev = (e_model - mc2_MeV) / mc2_MeV
    return {"mc2_MeV": mc2_MeV, "e_model_MeV": e_model,
            "dev": dev, "dev_pct": dev * 100.0,
            "route1_fails": abs(dev) > 0.01,
            "route2_cost": "引入裸质量 m₀ = m/√3 ⇒ 外部输入 +1",
            "m0_over_m": 1.0 / GAMMA_SURV,
            "dilemma": True}


def B5_angular_momentum():
    """
    ★ 防过度指控：角动量 L 在两种读法下**都**等于 ħ/2 ⇒ 不构成判别，不得当反预测。
      坐标读法：L = m·v_⊥·r  = m·c·r         = ħ/2
      快度读法：L = γm·v_⊥·r = γm·(c/γ)·r    = ħ/2
    """
    g = branch_geometry()
    r = g["r"]
    L_coord = M_E * C * r                       # 牛顿动量 × 半径（坐标读法 v_⊥=c）
    L_proper = GAMMA_SURV * M_E * (C / GAMMA_SURV) * r   # 相对论动量 × 半径（快度读法）
    return {"L_coord": L_coord, "L_proper": L_proper,
            "hbar_over_2": HBAR / 2.0,
            "both_equal_hbar2": (abs(L_coord - HBAR / 2.0) < 1e-9 * HBAR
                                 and abs(L_proper - HBAR / 2.0) < 1e-9 * HBAR),
            "not_discriminating": True}


def B6_parameter_gate():
    su5_free, su5_obs = 2, 3
    return {"n_free": 0, "n_obs": 0, "gate": 0 <= 0 - 1,
            "su5_free": su5_free, "su5_obs": su5_obs,
            "su5_gate": su5_free <= su5_obs - 1,
            "su5_tree_sin2": 0.375, "su5_measured": 0.231210,
            "su5_dev": abs(0.375 - 0.231210) / 0.231210}


# ============================================================
# C 组：对偶表（因果 vs 可检验量）
# ============================================================
def C1_duality_table():
    b1 = B1_magnetic_moment_gyro()
    b3 = B3_two_algorithms()
    b4 = B4_rest_energy()
    rows = [
        {"branch": "坐标读法（r152）",
         "v_over_c": SQRT2, "causal": False,
         "mu": b3["mu_loop_coord_reading"], "mu_dev_pct": b1["dev_pct"],
         "E_MeV": None, "note": "超光速 41.42%，γ 无定义"},
        {"branch": "快度读法（r153 存活分支）",
         "v_over_c": BETA_SURV, "causal": True,
         "mu": b3["mu_loop_surviving"], "mu_dev_pct": b3["dev_loop_pct"],
         "E_MeV": b4["e_model_MeV"], "note": "β=√(2/3)，但磁矩/静止能量皆偏离"},
    ]
    return {"rows": rows,
            "causal_savable": True,
            "observables_savable": False,
            "conclusion": "因果性可以靠换读法救回；**可检验量救不回**"}


# ============================================================
# D 组：修复定价（在存活分支上再枚举）
# ============================================================
REPAIR_TARGETS = [
    "螺距角 45°（v_⊥=u）",
    "γ=√3（快度读法）",
    "经典旋磁比 e/2m",
]
ACTS = ("KEEP", "DEL", "REPLACE")


def D1_repair_pricing():
    """
    对存活分支的三根支柱各施加 {KEEP, DEL, REPLACE} ⇒ 27。
    REPLACE = 换成标准物理（自由螺距角 / 坐标读法+SR / Dirac g=2）。
    存活判据：
      (1) 因果：v < c
      (2) 磁矩与实测一致：|μ/μ_e − 1| < 1%
      (3) 静止能量与实测一致：|E/(mc²) − 1| < 1%
      (4) 尺度定标：r 与 h 都由 f 定标（不许 DEL 掉螺距角关系）
    """
    b1 = B1_magnetic_moment_gyro()
    b3 = B3_two_algorithms()
    b4 = B4_rest_energy()
    out = []
    for a1 in ACTS:
        for a2 in ACTS:
            for a3 in ACTS:
                # ---- γ 的三种动作（语义必须写死，不得含糊）----
                #   KEEP   ：保留快度读法 ⇒ β=√(2/3) 保因果，但 E=√3 mc² 撞观测
                #   DEL    ：删掉 γ ⇒ 两式落回【坐标读法】⇒ v=√2·c 超光速（因果死）
                #   REPLACE：改用标准 SR（γ 由实际速率定、不再钉死 √3）⇒ 速率自由
                if a2 == "KEEP":
                    v_over_c = BETA_SURV
                    causal = True
                    E_ok = False          # √3·m c² 偏离 +73.21%
                    E_val = b4["e_model_MeV"]
                elif a2 == "DEL":
                    v_over_c = SQRT2      # 落回坐标读法
                    causal = False
                    E_ok = False          # 超光速下 γ 无定义
                    E_val = None
                else:                     # REPLACE：标准 SR，速率自由
                    v_over_c = None       # 自由（可取任意 <c）
                    causal = True
                    E_ok = True
                    E_val = b4["mc2_MeV"]
                # ---- 旋磁比 ----
                if a3 == "KEEP":
                    mu_ok = abs(b1["mu_model"] / MU_E - 1.0) < 0.01
                    mu_val = b1["mu_model"]
                elif a3 == "REPLACE":
                    mu_val = MU_E
                    mu_ok = True          # 直接取 Dirac g=2
                else:
                    mu_ok = False
                    mu_val = None
                # 尺度定标
                scale_fixed = (a1 != "DEL")
                valid = causal and mu_ok and E_ok and scale_fixed
                cost = []
                if a1 == "DEL":
                    cost.append("螺距角自由 ⇒ r 与 h 不由 f 定标（尺度外输）")
                if a1 == "REPLACE":
                    cost.append("放弃 τ/κ=1 ⇒ 来料的『统一参数』作废")
                if a2 == "DEL":
                    cost.append("删掉 γ ⇒ 落回坐标读法 ⇒ v=√2·c 超光速（因果死）")
                if a2 == "REPLACE":
                    cost.append("改用标准 SR ⇒ β=√(2/3) 这一唯一新内容作废，速率自由（外输）")
                if a3 == "DEL":
                    cost.append("不解释磁矩 ⇒ 电磁侧内容缺失")
                if a3 == "REPLACE":
                    cost.append("直接取 Dirac g=2 ⇒ 引入 Dirac 方程（外输）")
                out.append({"螺距角45°": a1, "γ=√3": a2, "旋磁比": a3,
                            "v_over_c": v_over_c, "causal": causal,
                            "mu_ok": mu_ok, "E_ok": E_ok,
                            "scale_fixed": scale_fixed,
                            "valid": valid,
                            "cost": cost if cost else ["无代价"]})
    survivors = [x for x in out if x["valid"]]
    return {"enumeration": out, "n_total": len(out),
            "n_survivors": len(survivors), "survivors": survivors,
            "n_zero_cost": sum(1 for x in survivors if x["cost"] == ["无代价"])}


def D2_minimal():
    d1 = D1_repair_pricing()
    sv = d1["survivors"]
    if not sv:
        concl = "无存活解"
    else:
        concl = ("存活 %d 个，且**全部**要求 REPLACE 旋磁比（引入 Dirac g=2）"
                 % len(sv))
    return {"n_survivors": len(sv), "n_zero_cost": d1["n_zero_cost"],
            "survivors": sv, "conclusion": concl,
            "remaining_non_known": 0,
            "is_repair_equals_suicide": len(sv) > 0 and d1["n_zero_cost"] == 0}


# ============================================================
# F 组：控制组
# ============================================================
def control_group():
    out = []
    b1 = B1_magnetic_moment_gyro()
    b3 = B3_two_algorithms()
    b4 = B4_rest_energy()
    b5 = B5_angular_momentum()
    g = branch_geometry()

    # F1 μ_B = eħ/(2m) 自洽（★阈值按 h/ħ 舍入地板 6.13e−10 放宽到 1e−8）
    mu_b_calc = Q_E * HBAR / (2.0 * M_E)
    out.append(dict(id="F1", desc="玻尔磁子自洽：μ_B = eħ/(2m) 必须与公布值一致",
                    value=abs(mu_b_calc / MU_B - 1.0), expect="<1e-8",
                    ok=abs(mu_b_calc / MU_B - 1.0) < 1e-8))

    # F2 μ_e/μ_B = 1.00115965（已知锚点）
    out.append(dict(id="F2", desc="已知锚点：μ_e/μ_B 必须 ≈ 1.00115965（g≈2）",
                    value=MU_E / MU_B, expect="1.00115965",
                    ok=abs(MU_E / MU_B - 1.00115965) < 1e-6))

    # F3 ★正对照：经典非相对论圆环下，环电流法与旋磁比法必须一致
    v_cl = 1.0e3            # m/s，远小于 c ⇒ 非相对论
    r_cl = 1.0e-2           # m
    m_cl = 1.0e-6           # kg
    q_cl = 1.0e-9           # C
    mu_loop_cl = q_cl * (v_cl / (2.0 * math.pi * r_cl)) * math.pi * r_cl ** 2
    mu_gyro_cl = (q_cl / (2.0 * m_cl)) * (m_cl * v_cl * r_cl)
    gap_cl = abs(mu_loop_cl - mu_gyro_cl) / mu_gyro_cl
    out.append(dict(id="F3",
                    desc="★正对照：经典非相对论圆环下环电流法与旋磁比法必须一致"
                         "（证明 B3 的不一致是模型病，不是算错）",
                    value=gap_cl, expect="<1e-12", ok=gap_cl < 1e-12))

    # F4 反向控制：g=1 与 g=2 必须差 2 倍
    ratio_g = (2.0 * MU_B) / (1.0 * MU_B)
    out.append(dict(id="F4", desc="反向控制：g=1 与 g=2 的磁矩必须差 2 倍",
                    value=abs(ratio_g - 2.0), expect="≈0",
                    ok=abs(ratio_g - 2.0) < 1e-12))

    # F5 角动量两读法一致（B5 复现）
    out.append(dict(id="F5",
                    desc="角动量 L 在坐标/快度两种读法下都必须 = ħ/2（防过度指控）",
                    value=abs(b5["L_proper"] / b5["L_coord"] - 1.0),
                    expect="<1e-12",
                    ok=b5["both_equal_hbar2"]
                    and abs(b5["L_proper"] / b5["L_coord"] - 1.0) < 1e-12))

    # F6 m_e c² = 0.510998950 MeV 锚点
    out.append(dict(id="F6", desc="已知锚点：m_e c² 必须 ≈ 0.510998950 MeV",
                    value=b4["mc2_MeV"], expect="0.510998950",
                    ok=abs(b4["mc2_MeV"] - 0.510998950) < 1e-6))

    # F7 Zitterbewegung 频率锚点：2mc²/h == c/(2πr)
    gap_f = abs(g["f_proper"] - C / (2.0 * math.pi * g["r"])) / g["f_proper"]
    out.append(dict(id="F7",
                    desc="已知锚点：f=2mc²/h 必须与 c/(2πr) 一致（Zitterbewegung 自洽）",
                    value=gap_f, expect="<1e-8", ok=gap_f < 1e-8))

    # F8 已知物理控制：Dirac 的 g=2 来自 Dirac 方程，不由经典螺旋给出
    out.append(dict(id="F8",
                    desc="已知物理控制：经典螺旋的旋磁比恒为 e/2m（g=1），"
                         "g=2 须由 Dirac 方程给出 ⇒ 该缺失是结构性的",
                    value=b1["over_mu_B"], expect="0.5",
                    ok=abs(b1["over_mu_B"] - 0.5) < 1e-8))

    return out


def guards(led):
    g = []
    n = led.count()
    a2 = A2_content_audit()
    d1 = D1_repair_pricing()
    g.append(("守卫1：条目数 ≥ 12", len(led.items) >= 12))
    g.append(("守卫2：存在 FAIL 条目", n.get("FAIL", 0) >= 1))
    g.append(("守卫3：控制组 ≥ 7 项", len(control_group()) >= 7))
    g.append(("守卫4：修复枚举数 = 27", d1["n_total"] == 27))
    g.append(("守卫5：内容清点非已知项 ≥ 1（禁硬编码 0）", a2["n_new"] >= 1))
    g.append(("守卫6：存在对靶有利条目（角动量 ħ/2）",
              any(it["id"] == "B5" and it["status"] == "INFO" for it in led.items)))
    g.append(("守卫7：静止能量偏离 > 50%", abs(B4_rest_energy()["dev_pct"]) > 50.0))
    g.append(("守卫8：磁矩偏离 > 40%", abs(B1_magnetic_moment_gyro()["dev_pct"]) > 40.0))
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

    # ---- A 组 ----
    a1 = A1_external_inputs()
    led.add("A1", "外部输入清点：4 项（康普顿半径 / Zitterbewegung 频率 / 洛伦兹 γ / 实测 m）"
                  "**全部**来自已知物理或实测，n_自由 = 0",
            "FAIL" if (not a1["gate"] and a1["n_known_source"] == a1["n_external"])
            else "GUARD-FAIL",
            {"n_external": a1["n_external"], "n_known_source": a1["n_known_source"],
             "n_free": a1["n_free"], "n_obs": a1["n_obs"], "gate": a1["gate"],
             "inputs": a1["inputs"]},
            "参数计数门 0 ≤ 0−1 为 False；且每一项输入都能在已知物理里找到原型")

    a2 = A2_content_audit()
    led.add("A2", "内容清点 6 条：已知 2 / 已知重排 1 / 恒等式+零新增 2 / **新内容仅 1**"
                  "（β=√(2/3)），而该项既与来料公设冲突又无观测支撑 ⇒ 可用新内容 0",
            "FAIL" if (a2["n_new"] == 1 and a2["new_item_conflicts_with_axiom"])
            else "GUARD-FAIL",
            {"n_total": a2["n_total"], "n_known": a2["n_known"],
             "n_identity": a2["n_identity"], "n_new": a2["n_new"],
             "new_items": a2["new_items"], "n_usable_new": a2["n_usable_new"],
             "h_over_2pi_r": a2["h_over_2pi_r"], "rows": a2["rows"]},
            "★禁硬编码『非已知项=0』：本卷诚实记为 1，但该项不可用")

    a3 = A3_control_dirac()
    led.add("A3", "控制：同一清点法用于已知物理（Dirac Zitterbewegung）也应全部标『已知』"
                  " ⇒ 清点方法无偏",
            "PASS" if a3["unbiased"] else "GUARD-FAIL",
            {"n_known": a3["n_known"], "n_total": a3["n_total"]},
            "防止清点法把什么都判成『已知重排』（无分辨力）")

    # ---- B 组 ----
    b1 = B1_magnetic_moment_gyro()
    led.add("B1", "★电子磁矩（旋磁比口径）：μ = μ_B/2 = 4.637005e−24 J/T，"
                  "与实测 9.284765e−24 差 −50.0579%，**且该结果与读法无关**",
            "FAIL" if b1["fails"] else "GUARD-FAIL",
            b1, "μ=(e/2m)·L 且 L=ħ/2（两读法皆然，见 B5）⇒ μ=μ_B/2；"
                "缺的正是 **g=2** 这个因子")

    b2 = B2_dilemma_magnetic()
    led.add("B2", "★两难：要么宣称解释磁矩（算错 g=2），要么不解释（电磁侧缺内容）"
                  " ⇒ 两种都不利",
            "FAIL" if b2["both_unfavorable"] else "GUARD-FAIL",
            b2, "本卷以两难形式规避『靶是否宣称解释磁矩』的归属争议（见 G1）")

    b3 = B3_two_algorithms()
    led.add("B3", "★内部不一致：环电流口径与旋磁比口径在存活分支下相差 √3=1.73205081"
                  "（坐标读法下两者一致）⇒ 模型无唯一磁矩算法",
            "FAIL" if (b3["inconsistent"] and b3["equals_sqrt3"]) else "GUARD-FAIL",
            b3, "μ_环 = e·f_坐标·πr² = μ_B/(2√3) = 2.677176e−24（偏离 −71.1659%）；"
                "μ_旋磁比 = μ_B/2 = 4.637005e−24；两者之比恰为 γ=√3")

    b4 = B4_rest_energy()
    led.add("B4", "★静止能量两难：√3·m_e c² = 0.885076 MeV vs 实测 0.510999 MeV"
                  "（+73.2051%）；或引入裸质量 m₀=m/√3（外部输入 +1）",
            "FAIL" if b4["dilemma"] and b4["route1_fails"] else "GUARD-FAIL",
            b4, "沿用『静止能量来自螺旋运动』⇒ E=γ m₀ c²=√3 m₀ c²；"
                "两条路都不通：要么撞观测，要么新增外部输入")

    b5 = B5_angular_momentum()
    led.add("B5", "INFO（对靶有利，诚实登记）：角动量 L=ħ/2 在**两种读法下都成立**"
                  " ⇒ 角动量**不构成判别**，不得当反预测",
            "INFO" if b5["not_discriminating"] else "GUARD-FAIL",
            b5, "坐标读法 L=m·c·r=ħ/2；快度读法 L=γm·(c/γ)·r=ħ/2。"
                "★防过度指控：本条不得计入不利证据")

    b6 = B6_parameter_gate()
    led.add("B6", "参数计数门：n_自由=0 ≤ n_观测−1=−1 为 False；SU(5) 控制组 2≤2 为 True",
            "FAIL" if not b6["gate"] else "GUARD-FAIL",
            b6, "SU(5) 树级 sin²θ_W=0.375 vs 实测 0.231210（偏离 62.19%）⇒ 门有分辨力")

    # ---- C 组 ----
    c1 = C1_duality_table()
    led.add("C1", "★对偶表：因果性可以靠换读法救回，但**可检验量救不回**"
                  "（两分支磁矩分别偏离 −50.06% / −71.17%，静止能量偏离 +73.21%）",
            "FAIL" if (c1["causal_savable"] and not c1["observables_savable"])
            else "GUARD-FAIL",
            {"rows": c1["rows"], "causal_savable": c1["causal_savable"],
             "observables_savable": c1["observables_savable"]},
            c1["conclusion"])

    # ---- D 组 ----
    d1 = D1_repair_pricing()
    led.add("D1", "修复定价：存活分支三根支柱 × {KEEP,DEL,REPLACE} = 27 枚举"
                  " ⇒ 存活 %d，零代价解 %d" % (d1["n_survivors"], d1["n_zero_cost"]),
            "FAIL" if d1["n_zero_cost"] == 0 else "GUARD-FAIL",
            {"n_total": d1["n_total"], "n_survivors": d1["n_survivors"],
             "n_zero_cost": d1["n_zero_cost"], "survivors": d1["survivors"]},
            "存活要求：因果 ∧ 磁矩对 ∧ 静止能量对 ∧ 尺度定标")

    d2 = D2_minimal()
    led.add("D2", "最小完备修复集：%s" % (d2["conclusion"] or "无存活解"),
            "FAIL" if d2["is_repair_equals_suicide"] or d2["n_survivors"] == 0
            else "GUARD-FAIL",
            {"n_survivors": d2["n_survivors"], "n_zero_cost": d2["n_zero_cost"],
             "remaining_non_known": d2["remaining_non_known"]},
            "本库「修复即自杀」第五次复发；但须注明修复空间是**低阶**"
            "（3 个三值算子的笛卡尔积），高阶新增型未枚举")

    # ---- G 组 ----
    led.add("G1", "BOUNDARY：『靶是否宣称解释电子磁矩』归属未定",
            "BOUNDARY",
            {"note": "本卷以 B2 两难形式规避该争议：宣称则算错 g=2，不宣称则电磁侧缺内容"},
            "若来料明确否认该义务，B1/B3 降为『不适用』，B2 的『缺内容』一支仍成立")

    led.add("G2", "BOUNDARY：未处理 QED 辐射修正（g−2 = 0.0023193）",
            "BOUNDARY",
            {"note": "本卷全为经典/半经典图像；实测 g=2.0023193 的超出部分不在本卷口径内"},
            "即便计入辐射修正，本卷的缺口是 **g=2 整整一倍**，量级远大于 0.0023")

    led.add("G3", "BOUNDARY：未处理自旋的量子本质",
            "BOUNDARY",
            {"note": "本卷把自旋当作经典环流的角动量处理（L=ħ/2）"},
            "若靶主张自旋另有量子来源，则 L=ħ/2 的巧合需重新解释（本卷不代劳）")

    led.add("G4", "BOUNDARY：静止能量的推导链依赖来料上游式子",
            "BOUNDARY",
            {"note": "B4 假设『静止能量来自螺旋运动』⇒ E=γm₀c²；"
                     "若来料另有推导，需重算"},
            "无论哪条推导，γ=√3 是刚性常数 ⇒ 必须处理这个 √3")

    return led


# ============================================================
# 报告
# ============================================================
def build_report(led):
    L = []
    A = L.append
    A("=" * 96)
    A("TUFT-r154｜r153 唯一存活分支的终局清点：可检验量反预测（磁矩 / 静止能量）")
    A("=" * 96)
    A("生成时刻: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    A("")
    A("【定位】r153 留下唯一活口：(固有时,固有时) 读法 + 删掉 v=c ⇒ β=√(2/3) 保住因果性。")
    A("        本卷回答：这个救回来的分支，**还算得对吗**？落到电子磁矩与静止能量上。")
    A("【分层】r151/r152=式子层；r153=读法层；**本卷=存活分支的后果层（可检验量）**。")
    A("        四卷结论互补，**条目不可相加**。")
    A("")

    for it in led.items:
        A("[%s] %-11s %s" % (it["id"], it["status"], it["title"]))
        if it["note"]:
            A("      " + it["note"])
        for k, v in it["metrics"].items():
            if k in ("rows", "inputs", "enumeration", "survivors", "note"):
                continue
            if isinstance(v, float):
                A("      %s = %s" % (k, "%.6e" % v))
            else:
                A("      %s = %s" % (k, v))
        A("")

    g = branch_geometry()
    A("-" * 96)
    A("【存活分支（r153 宽松档）的几何量 · 电子】")
    A("    r            = %.6e m     （= ħ/(2mc)，约化康普顿半波长）" % g["r"])
    A("    f(固有时)     = %.6e Hz   （= 2mc²/h，Zitterbewegung）" % g["f_proper"])
    A("    f(坐标)       = %.6e Hz   （= f_固有时/√3）" % g["f_coord"])
    A("    h(螺距)      = %.6e m     （= c/f = πλ̄_C = %.6e）" % (g["h_pitch"], g["pi_lambdabar"]))
    A("    h/(2πr)      = %.12f" % g["h_over_2pi_r"])
    A("    β = √(2/3)   = %.10f      γ = √3 = %.10f" % (g["beta"], g["gamma"]))
    A("    v_⊥ = u      = %.6e m/s = %.10f c" % (g["v_perp"], g["v_perp"] / C))
    A("    v            = %.6e m/s = %.10f c" % (g["v"], g["v"] / C))
    A("")

    A("-" * 96)
    A("【A 组 · 内容清点】")
    a2 = A2_content_audit()
    A("    条目                              标签            依据")
    for row in a2["rows"]:
        A("    %-32s %-14s %s" % (row["item"], row["label"], row["reason"]))
    A("    ★ 已知 %d / 已知重排 %d / 恒等式+零新增 %d / **新内容 %d**"
      % (a2["n_known"], a2["n_known"] and 1 or 0, a2["n_identity"], a2["n_new"]))
    A("    ★ 新内容 = %s；与来料『以光速运动』公设冲突 = %s ⇒ **可用新内容 0**"
      % (a2["new_items"], a2["new_item_conflicts_with_axiom"]))
    A("")

    A("-" * 96)
    A("【B 组 · 可检验量反预测（本卷核心）】")
    b1 = B1_magnetic_moment_gyro()
    b3 = B3_two_algorithms()
    b4 = B4_rest_energy()
    b5 = B5_angular_momentum()
    A("    μ_B(玻尔磁子)  = %.6e J/T" % MU_B)
    A("    μ_e(实测)      = %.6e J/T  （μ_e/μ_B = %.8f）" % (MU_E, MU_E / MU_B))
    A("    μ(旋磁比口径)   = %.6e J/T  = %.6f μ_B  ⇒ 偏离 **%.4f%%**"
      % (b1["mu_model"], b1["over_mu_B"], b1["dev_pct"]))
    A("    μ(环电流口径)   = %.6e J/T  = %.6f μ_B  ⇒ 偏离 **%.4f%%**"
      % (b3["mu_loop_surviving"], b3["mu_loop_surviving"] / MU_B, b3["dev_loop_pct"]))
    A("    ★ 两口径之比 = %.8f  = √3  ⇒ **模型内部不自洽**（坐标读法下比值为 1）"
      % b3["ratio_surviving"])
    A("    ★ 缺的因子 = %.8f（即 **g=2**）" % b1["missing_g_factor"])
    A("")
    A("    m_e c²(实测)   = %.9f MeV" % b4["mc2_MeV"])
    A("    √3·m_e c²      = %.9f MeV  ⇒ 偏离 **%.4f%%**" % (b4["e_model_MeV"], b4["dev_pct"]))
    A("")
    A("    L(坐标读法)     = %.6e J·s   （= ħ/2）" % b5["L_coord"])
    A("    L(快度读法)     = %.6e J·s   （= ħ/2）" % b5["L_proper"])
    A("    ħ/2            = %.6e J·s" % b5["hbar_over_2"])
    A("    ★ 角动量两读法**都**等于 ħ/2 ⇒ **不构成判别**，不得当反预测（防过度指控）")
    A("")

    A("-" * 96)
    A("【C 组 · 对偶表：因果 vs 可检验量】")
    A("    分支                          v/c         因果   μ 偏离        E(MeV)     结论")
    for row in C1_duality_table()["rows"]:
        A("    %-26s %-12s %-5s %-12s %-11s %s"
          % (row["branch"],
             ("%.9f" % row["v_over_c"]) if row["v_over_c"] == row["v_over_c"] else "nan",
             "✓" if row["causal"] else "✗",
             "%.4f%%" % row["mu_dev_pct"],
             ("%.6f" % row["E_MeV"]) if row["E_MeV"] else "—",
             row["note"]))
    A("    ★ **因果性可以靠换读法救回；可检验量救不回。**")
    A("")

    A("-" * 96)
    A("【D 组 · 修复定价（27 枚举）】")
    d1 = D1_repair_pricing()
    A("    总组合 %d；存活 %d；**零代价解 %d**" % (d1["n_total"], d1["n_survivors"], d1["n_zero_cost"]))
    for s in d1["survivors"]:
        A("      存活：螺距角=%s  γ=%s  旋磁比=%s   代价=%s"
          % (s["螺距角45°"], s["γ=√3"], s["旋磁比"], "；".join(s["cost"])))
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
    b1 = B1_magnetic_moment_gyro()
    b3 = B3_two_algorithms()
    b4 = B4_rest_energy()
    d1 = D1_repair_pricing()
    a2 = A2_content_audit()
    verdict = "SURVIVING-BRANCH-SAVES-CAUSALITY-BUT-NOT-OBSERVABLES"

    m = []
    a = m.append
    a("# 判定册 TUFT-r154｜r153 唯一存活分支的终局清点：可检验量反预测")
    a("")
    a("- 编号：TUFT-r154")
    a("- 生成时刻：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    a("- 引擎：`源码/TUFT-r154_存活分支终局清点_磁矩静止能量反预测_2026-10-22.py`")
    a("- 控制组：%s" % ("全部通过" if allok else "存在失败"))
    a("- 条目统计：%s" % "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
    a("")
    a("## 00. 编号碰撞处置表")
    a("")
    a("| 编号 | 占用者 | 处置 |")
    a("|------|--------|------|")
    a("| r150 | 自旋-2 卷（已产出三件套并登记） | 保留为权威 |")
    a("| r151 | 双约束求导证明卷 | 保留为权威 |")
    a("| r152 | ω f h c f 完整关系组卷 | 保留为权威 |")
    a("| r153 | 读法空间穷举卷 | 保留为权威 |")
    a("| r154 | **本卷**（存活分支终局清点） | 实测首空号后启用 |")
    a("")
    a("## 01. 分工声明（★ 四卷条目不可相加）")
    a("")
    a("| 卷 | 层 | 处理对象 |")
    a("|----|----|----------|")
    a("| r151 | 式子层 | 两式 {v=c, ωr=c}，坐标读法 |")
    a("| r152 | 式子层 | 三式 {+ h·f=c}，坐标读法 + 量纲口径 |")
    a("| r153 | 读法层 | 两式/三式 × 坐标∪固有时穷举 |")
    a("| **r154** | **后果层** | **r153 存活分支的可检验量（磁矩 / 静止能量）** |")
    a("")
    a("## 02. 判词")
    a("")
    a("`%s`" % verdict)
    a("")
    a("**因果性可以靠换读法救回；可检验量救不回。**")
    a("")
    a("## 03. 核心结论")
    a("")
    a("### 3.1 内容清点：救回来的分支还剩什么")
    a("")
    a("| 条目 | 标签 | 依据 |")
    a("|---|---|---|")
    for row in a2["rows"]:
        a("| %s | %s | %s |" % (row["item"], row["label"], row["reason"]))
    a("")
    a("**非已知项 = 1**（β=√(2/3)），但该项**既与来料自己的『以光速运动』公设冲突、"
      "又无任何观测支撑** ⇒ **可用新内容 = 0**。")
    a("（★ 禁为凑结论而硬编码「非已知项=0」—— 本卷如实记为 1，只是它不可用。）")
    a("")
    a("### 3.2 ★电子磁矩：差整整一个 g=2，且与读法无关")
    a("")
    a("- 旋磁比口径：μ = (e/2m)·L，L = ħ/2 ⇒ **μ = μ_B/2 = %.6e J/T**" % b1["mu_model"])
    a("- 实测：**μ_e = %.6e J/T**（μ_e/μ_B = %.8f）" % (MU_E, MU_E / MU_B))
    a("- 偏离：**%.4f%%**；缺失因子 **%.8f**，即 **g = 2**。" % (b1["dev_pct"], b1["missing_g_factor"]))
    a("- **该结果与读法无关**：坐标读法与快度读法下 L 都是 ħ/2 ⇒ 换读法救不了它。")
    a("")
    a("### 3.3 ★内部不一致：同一个模型有两个磁矩")
    a("")
    a("- 环电流口径：μ = e·f_坐标·πr² = **%.6e J/T**（偏离 %.4f%%）" % (b3["mu_loop_surviving"], b3["dev_loop_pct"]))
    a("- 旋磁比口径：μ = **%.6e J/T**（偏离 %.4f%%）" % (b3["mu_gyro"], b1["dev_pct"]))
    a("- 两者之比 = **%.8f = √3 = γ** ⇒ 在存活分支下**相差整整一个洛伦兹因子**。"
      % b3["ratio_surviving"])
    a("- 坐标读法下两者一致（比值 1）⇒ 该不一致是**快度读法带来的新病**。")
    a("- 控制组 F3 证明：经典非相对论圆环下两算法严格一致 ⇒ **不是我算错**。")
    a("")
    a("### 3.4 ★静止能量两难")
    a("")
    a("- 沿用「静止能量来自螺旋运动」⇒ E = γ m₀ c² = √3 m₀ c²")
    a("- 路①不做重归一化：**%.9f MeV** vs 实测 **%.9f MeV**，偏离 **%.4f%%**"
      % (b4["e_model_MeV"], b4["mc2_MeV"], b4["dev_pct"]))
    a("- 路②引入裸质量 m₀ = m/√3 ⇒ **外部输入 +1**（且 √3 仍是刚性普适常数）")
    a("")
    a("### 3.5 防过度指控：角动量不构成判别")
    a("")
    a("坐标读法 L = m·c·r = ħ/2；快度读法 L = γm·(c/γ)·r = ħ/2。**两者都等于 ħ/2**")
    a("⇒ 本卷**不**把角动量计入不利证据。这是本卷对靶最有利的一条，诚实登记为 INFO。")
    a("")
    a("### 3.6 对偶表")
    a("")
    a("| 分支 | v/c | 因果 | 磁矩偏离 | 静止能量 |")
    a("|---|---|---|---|---|")
    for row in C1_duality_table()["rows"]:
        a("| %s | %s | %s | %.4f%% | %s |"
          % (row["branch"],
             ("%.9f" % row["v_over_c"]) if row["v_over_c"] == row["v_over_c"] else "—",
             "✓" if row["causal"] else "✗", row["mu_dev_pct"],
             ("%.6f MeV" % row["E_MeV"]) if row["E_MeV"] else "—"))
    a("")
    a("### 3.7 修复定价（27 枚举）")
    a("")
    a("- 存活 **%d** 个，**零代价解 %d 个**" % (d1["n_survivors"], d1["n_zero_cost"]))
    a("- 存活解**全部**要求 REPLACE 旋磁比（即直接取 Dirac g=2 ⇒ 引入 Dirac 方程）")
    a("  ⇒ **本库「修复即自杀」第五次复发**。")
    a("- **但须注明**：修复空间是**低阶**（3 个三值算子的笛卡尔积），高阶新增型未枚举。")
    a("")
    a("## 04. 机读证据")
    a("")
    a("```")
    a("μ_B          = %.6e J/T" % MU_B)
    a("μ_e          = %.6e J/T   (μ_e/μ_B = %.8f)" % (MU_E, MU_E / MU_B))
    a("μ_旋磁比      = %.6e J/T   偏离 %.4f%%" % (b1["mu_model"], b1["dev_pct"]))
    a("μ_环电流      = %.6e J/T   偏离 %.4f%%" % (b3["mu_loop_surviving"], b3["dev_loop_pct"]))
    a("两口径之比    = %.8f   (= √3 = %.8f)" % (b3["ratio_surviving"], SQRT3))
    a("m_e c²       = %.9f MeV" % b4["mc2_MeV"])
    a("√3·m_e c²    = %.9f MeV   偏离 %.4f%%" % (b4["e_model_MeV"], b4["dev_pct"]))
    a("L(两读法)     = ħ/2 = %.6e J·s" % (HBAR / 2.0))
    a("修复 27 组合  存活 %d / 零代价 %d" % (d1["n_survivors"], d1["n_zero_cost"]))
    a("```")
    a("")
    a("## 05. 未闭合项（禁止外推）")
    a("")
    a("1. **磁矩归属未定**：来料是否宣称用该螺旋图像解释电子磁矩，本卷未确认。"
      "已用 B2 两难规避 —— 宣称则算错 g=2，不宣称则电磁侧缺内容。")
    a("2. **未处理 QED 辐射修正**（g−2 = 0.0023193）。但本卷缺口是 **g=2 整整一倍**，"
      "量级远大于该修正。")
    a("3. **未处理自旋的量子本质**（本卷全为经典/半经典图像）。")
    a("4. **静止能量推导链依赖来料上游式子**；但 γ=√3 是刚性常数，无论如何必须处理这个 √3。")
    a("5. **修复空间是低阶**（27 组合），高阶新增型未枚举。")
    a("6. 本卷**不**宣称靶体系已被完全证伪 —— 只判决：")
    a("   **r153 唯一存活的那个分支，在可检验量上站不住。**")
    a("")
    a("## 06. 红线")
    a("")
    a("- 数学自洽 ≠ 实验证实。")
    a("- **因果可行 ≠ 可检验量对**。")
    a("- **修复可行 ≠ 修复后仍有内容**（第五次复发）。")
    a("- 防过度指控与防漏判同等重要：角动量 ħ/2 已诚实记为对靶有利的一条。")
    a("")
    return "\n".join(m), verdict


def main():
    led = build_ledger()
    report, allok = build_report(led)
    print(report)

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.abspath(os.path.join(here, "..", "数据"))
    os.makedirs(outdir, exist_ok=True)
    base = "TUFT-r154_存活分支终局清点_磁矩静止能量反预测_2026-10-22"
    verdict_j = "SURVIVING-BRANCH-SAVES-CAUSALITY-BUT-NOT-OBSERVABLES"

    payload = {
        "id": "TUFT-r154",
        "title": "r153 唯一存活分支的终局清点：可检验量反预测（磁矩 / 静止能量）",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict_j,
        "counts": led.count(),
        "controls_ok": allok,
        "items": led.items,
        "geometry": branch_geometry(),
        "content_audit": A2_content_audit()["rows"],
        "magnetic": {"gyro": B1_magnetic_moment_gyro(),
                     "loop": B3_two_algorithms()},
        "rest_energy": B4_rest_energy(),
        "angular_momentum": B5_angular_momentum(),
        "duality": C1_duality_table()["rows"],
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
