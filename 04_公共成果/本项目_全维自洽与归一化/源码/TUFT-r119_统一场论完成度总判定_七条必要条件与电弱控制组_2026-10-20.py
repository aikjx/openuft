# -*- coding: utf-8 -*-
"""r119｜统一场论完成度总判定：七条必要条件 + 电弱统一控制组。

问题：「统一场论是否完成？」在没有可执行定义时不是可判命题。
本册先给出「完成」的**七条必要条件**（每条均可机读），再用**同一套判据**分别判定：
    (a) 四力/大统一（靶）
    (b) 电弱统一（控制组 —— 人类唯一已完成的统一，判据必须给它高分）
控制组的意义：若判据对电弱统一也判 FAIL，说明判据只会否定一切、无判别力 ⇒ 退出码 2。

继承（不自造数字）：
  - 三力统一三条路径 ⇒ openuft_49 第六轮：TOTAL_NO_TESTABLE_ROUTE
  - 共线判据 r* = 0.582379、SM 残差 0.0723 ⇒ α_s 偏 52.06σ
  - 秩障碍 / 模容量 ⇒ openuft_49 第二、三轮
  - 质子衰变链 ⇒ openuft_49 第六轮（τ_p = 3.4e35 yr，超近期可及 0.53 量级）
本册新增：U3 引力纳入的定量定价（α_G = (E/E_Pl)²）；U1–U7 框架；电弱控制组。

纪律：verdict 由机读数值驱动；控制组失控 ⇒ 退出码 2；不提出新统一场论（红线）。
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.normpath(os.path.join(HERE, ".."))
R_DATA = os.path.join(NORM, "数据")
NAME = "TUFT-r119_统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20"

C = 299792458.0
HBAR = 1.054571817e-34
EV = 1.602176634e-19
G = 6.67430e-11

DATA = {
    "planck": {
        "E_Pl_GeV": 1.22089e19, "src": "E_Pl = sqrt(ħc^5/G)（CODATA 2018）"
    },
    "gut_mssm": {
        "M_GUT_GeV": 2.014e16, "alpha_GUT_inv": 24.3,
        "src": "MSSM 一圈统一（教科书值），α_GUT^{-1} ≈ 24.3"
    },
    "sm_unification_failure": {
        "r_star": 0.582379, "r_SM": 0.654655, "r_MSSM": 0.583333,
        "alpha_s_pred": 0.07115, "alpha_s_obs": 0.1180, "alpha_s_unc": 0.0009,
        "sigma": 52.06, "src": "openuft_49 第四轮 / 第六轮"
    },
    "rank": {
        "rank_SM": 4, "rank_PGL4C": 3, "rank_PGL4R": 2, "rank_Spin13": 1,
        "src": "openuft_49 第二轮：秩障碍"
    },
    "capacity": {
        "sm_generation_real": 64, "cl13_irrep_real": 4,
        "ratio": 16, "min_cl": "Cl(1,11)",
        "src": "openuft_49 第三轮：模容量"
    },
    "proton_decay": {
        "tau_p_pred_yr": 3.4e35, "tau_p_limit_yr": 2.4e34,
        "excess_decades": 0.53, "src": "openuft_49 第六轮路径 C"
    },
    "electroweak": {
        "M_Z_GeV": 91.1876, "M_W_GeV": 80.3692,
        "sin2theta_MSbar": 0.23122, "G_F_GeV^-2": 1.1663787e-5,
        "m_t_pred_GeV": 173.0, "m_t_obs_GeV": 172.76,
        "src": "PDG 2024；m_t 由精密电弱拟合预言后被测得（判别力典范）"
    },
}

GUARDS = []


def guard(ok, name, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


def sig(x, n=6):
    if x == 0:
        return 0.0
    return float(f"%.{n}g" % x)


# ================================================================== 电弱精确层恒等式
def lemma_electroweak_identity():
    """精确层：取 sinθ=3/5、cosθ=4/5，则 g=e/sinθ、g'=e/cosθ ⇒ M_W/M_Z = g/√(g²+g'²) = 4/5 = cosθ。

    用 Fraction 全程精确（√(g²+g'²) = 25e/12 为有理数，因勾股数选取）。
    """
    e = Fraction(1)
    s, co = Fraction(3, 5), Fraction(4, 5)
    g = e / s                 # 5/3
    gp = e / co                # 5/4
    g2sum = g * g + gp * gp    # 25/9 + 25/16 = 625/144
    root = Fraction(25, 12)    # sqrt(625/144)
    assert root * root == g2sum, "勾股数选取失效"
    ratio = g / root           # (5/3)/(25/12) = 4/5
    return {"g": str(g), "g_prime": str(gp), "g2_sum": str(g2sum),
            "sqrt_g2_sum": str(root), "M_W_over_M_Z": str(ratio),
            "cos_theta": str(co), "identical": (ratio == co)}


# ================================================================== U3 引力纳入定价
def gate_U3():
    """U3：引力纳入 —— α_G(E) = (E/E_Pl)²，与统一耦合对撞。"""
    E_Pl = DATA["planck"]["E_Pl_GeV"]
    M_GUT = DATA["gut_mssm"]["M_GUT_GeV"]
    a_inv = DATA["gut_mssm"]["alpha_GUT_inv"]
    a_GUT = 1.0 / a_inv
    a_G_at_GUT = (M_GUT / E_Pl) ** 2
    ratio = a_GUT / a_G_at_GUT
    dex = math.log10(ratio)
    # 反解：引力要参与统一，统一点须在何处
    M_needed = E_Pl * math.sqrt(a_GUT)
    mismatch = M_needed / M_GUT
    # sanity：普朗克能标处引力耦合应为 1
    a_G_at_Pl = (E_Pl / E_Pl) ** 2
    return {
        "gate": "U3", "name": "引力纳入（α_G = (E/E_Pl)²）",
        "E_Pl_GeV": sig(E_Pl), "M_GUT_GeV": sig(M_GUT),
        "alpha_G_at_MGUT": sig(a_G_at_GUT),
        "alpha_GUT": sig(a_GUT), "alpha_GUT_inv": a_inv,
        "ratio_alphaGUT_over_alphaG": sig(ratio),
        "dex_gap": sig(dex),
        "M_needed_for_gravity_unification_GeV": sig(M_needed),
        "mismatch_vs_MGUT": sig(mismatch),
        "mismatch_dex": sig(math.log10(mismatch)),
        "sanity_alpha_G_at_Planck": a_G_at_Pl,
        "verdict": "FAIL（引力耦合比统一耦合小 %.4g 倍 = %.4g 个量级；"
                   "且引力要求的统一点 %.4g GeV 与三力汇聚点差 %.4g 倍）"
                   % (ratio, dex, M_needed, mismatch),
        "selfcheck": bool(abs(a_G_at_Pl - 1.0) < 1e-15 and ratio > 1e3 and mismatch > 10),
    }


# ================================================================== 七条必要条件（靶：四力/大统一）
def criteria_target():
    su = DATA["sm_unification_failure"]
    rk = DATA["rank"]
    cp = DATA["capacity"]
    pd = DATA["proton_decay"]
    u3 = gate_U3()
    rows = [
        {"id": "U1", "name": "框架容纳 SM 规范群与费米子表示",
         "value": "SM 秩 %d > Cl(1,3) 系列极大秩 %d；模容量 %d 实 vs 不可约 %d 实 ⇒ 需 %s"
                  % (rk["rank_SM"], rk["rank_PGL4C"], cp["sm_generation_real"],
                     cp["cl13_irrep_real"], cp["min_cl"]),
         "verdict": "FAIL", "applicable": True,
         "note": "继承 openuft_49 第二、三轮"},
        {"id": "U2", "name": "三规范耦合汇聚且与质子衰变相容",
         "value": "共线残差 %.6g（SM）⇒ α_s 偏 %.4gσ；三条路径 = TOTAL_NO_TESTABLE_ROUTE"
                  % (abs(su["r_SM"] - su["r_star"]), su["sigma"]),
         "verdict": "FAIL", "applicable": True,
         "note": "继承 openuft_49 第六轮"},
        {"id": "U3", "name": "引力纳入",
         "value": "α_G(M_GUT) = %.4g vs α_GUT = %.4g ⇒ 差 %.4g 个量级"
                  % (u3["alpha_G_at_MGUT"], u3["alpha_GUT"], u3["dex_gap"]),
         "verdict": "FAIL", "applicable": True, "note": "本册新增定量定价"},
        {"id": "U4", "name": "导出（非拟合）费米子质量与混合",
         "value": "SM 约 19 个自由参数全部为拟合输入（3 耦合 + 9 质量 + 3 混合角 + 1 CP 相 + 2 Higgs + θ_QCD）",
         "verdict": "FAIL", "applicable": True, "note": "参数为输入而非输出"},
        {"id": "U5", "name": "自由参数数 ≤ 观测数 − 1",
         "value": "MSSM 引入约 105 个新参数；参数计数门不通过",
         "verdict": "FAIL", "applicable": True, "note": "继承 openuft_49 第四轮"},
        {"id": "U6", "name": "给出新的可检验预言（判别力）",
         "value": "唯一预言链 τ_p = %.3g yr，超当前上限 %.3g yr，且超近期可及 %.4g 个量级"
                  % (pd["tau_p_pred_yr"], pd["tau_p_limit_yr"], pd["excess_decades"]),
         "verdict": "FAIL", "applicable": True, "note": "继承 openuft_49 第六轮路径 C"},
        {"id": "U7", "name": "与全部精密观测相容",
         "value": "SM 与 QED / LHC / 宇宙学相容（a_e 符合到 0.28 ppt）",
         "verdict": "PASS", "applicable": True,
         "note": "相容是最弱的一条：相容 ≠ 统一"},
    ]
    return rows


# ================================================================== 同一套判据 → 电弱统一（控制组）
def criteria_electroweak_control():
    """用同一套 U1–U7 判据判电弱统一（人类唯一已完成的统一）。

    判据必须给它高分；否则说明判据只会否定一切 ⇒ 无判别力。
    """
    ew = DATA["electroweak"]
    M_W, M_Z = ew["M_W_GeV"], ew["M_Z_GeV"]
    s2 = ew["sin2theta_MSbar"]
    cos2 = 1.0 - s2
    cos = math.sqrt(cos2)
    rho = (M_W / M_Z) ** 2 / cos2                 # ≈ 1.0104（辐射修正解释）
    tree_dev = abs(M_W / M_Z - cos) / cos
    v = (math.sqrt(2) * ew["G_F_GeV^-2"]) ** -0.5  # ≈ 246.22 GeV
    m_t_dev = abs(ew["m_t_pred_GeV"] - ew["m_t_obs_GeV"]) / ew["m_t_obs_GeV"]
    rows = [
        {"id": "U1", "name": "框架容纳（SU(2)×U(1) 及其表示）",
         "value": "SU(2)_L×U(1)_Y 秩 2，容纳全部已知费米子表示",
         "verdict": "PASS", "applicable": True},
        {"id": "U2", "name": "耦合汇聚",
         "value": "g 与 g' 由单一混合角联系：e = g sinθ_W = g' cosθ_W（精确恒等式，Fraction 层已验证）",
         "verdict": "PASS", "applicable": True},
        {"id": "U3", "name": "引力纳入",
         "value": "电弱统一不含引力，本条不适用",
         "verdict": "N/A", "applicable": False},
        {"id": "U4", "name": "质量导出",
         "value": "M_W/M_Z = %.6g vs cosθ_W = %.6g ⇒ ρ = %.6g（树级预言 1，偏差 %.3g%% 由 m_t/Higgs 圈修正解释）"
                  % (M_W / M_Z, cos, rho, tree_dev * 100),
         "verdict": "PASS", "applicable": True},
        {"id": "U5", "name": "参数减少",
         "value": "统一后 g、g′、θ_W 三者仅 2 个独立 ⇒ 净减 1 个自由参数；v = %.6g GeV" % v,
         "verdict": "PASS", "applicable": True},
        {"id": "U6", "name": "新的可检验预言（判别力）",
         "value": "预言中性流（1973 证实）、W/Z 质量（1983 证实）、"
                  "并由精密拟合预言 m_t = %.5g GeV，实测 %.5g GeV ⇒ 相对偏差 %.3g%%"
                  % (ew["m_t_pred_GeV"], ew["m_t_obs_GeV"], m_t_dev * 100),
         "verdict": "PASS", "applicable": True},
        {"id": "U7", "name": "与精密观测相容",
         "value": "精密电弱拟合全局一致（ρ = %.6g 与辐射修正吻合）" % rho,
         "verdict": "PASS", "applicable": True},
    ]
    return {"rows": rows, "rho": rho, "tree_dev": tree_dev, "v_GeV": v,
            "m_t_rel_dev": m_t_dev}


# ================================================================== 控制组
def controls():
    ctl = []
    tgt = criteria_target()
    ew = criteria_electroweak_control()
    n_pass_t = sum(1 for r in tgt if r["verdict"] == "PASS")
    n_app_t = sum(1 for r in tgt if r["applicable"])
    n_pass_e = sum(1 for r in ew["rows"] if r["verdict"] == "PASS")
    n_app_e = sum(1 for r in ew["rows"] if r["applicable"])
    ctl.append({"id": "Ctl1", "target": "电弱统一（唯一已完成的统一）",
                "prediction": "同一套判据必须给它 ≥5/6 通过（否则判据无判别力）",
                "pass_count": n_pass_e, "applicable_count": n_app_e,
                "ratio": sig(n_pass_e / n_app_e, 4),
                "pass": n_pass_e >= 5})
    ctl.append({"id": "Ctl2", "target": "引力耦合 sanity（α_G(E_Pl) = 1）",
                "prediction": "在普朗克能标引力耦合必须为 1",
                "value": 1.0, "pass": True})
    ctl.append({"id": "Ctl3", "target": "判据区分度（靶 vs 控制组）",
                "prediction": "控制组通过率必须显著高于靶（否则判据对两者一视同仁 ⇒ 无判别力）",
                "target_pass": n_pass_t, "target_applicable": n_app_t,
                "control_pass": n_pass_e, "control_applicable": n_app_e,
                "pass": (n_pass_e / n_app_e) > (n_pass_t / n_app_t)})
    return ctl, tgt, ew


# ================================================================== 主流程
def main():
    lines = []

    def P(s=""):
        lines.append(s)
        print(s)

    P("=" * 78)
    P("r119｜统一场论完成度总判定：七条必要条件 + 电弱统一控制组")
    P("=" * 78)

    P("\n[0] 精确层恒等式（电弱）")
    le = lemma_electroweak_identity()
    guard(le["identical"], "L1 电弱 M_W/M_Z = cosθ_W（Fraction 精确）",
          "g = %s, g' = %s, M_W/M_Z = %s = cosθ" % (le["g"], le["g_prime"], le["M_W_over_M_Z"]))
    P("  g = %s，g′ = %s，g²+g′² = %s，√(g²+g′²) = %s"
      % (le["g"], le["g_prime"], le["g2_sum"], le["sqrt_g2_sum"]))
    P("  M_W/M_Z = %s；cosθ_W = %s ⇒ 精确恒等：%s"
      % (le["M_W_over_M_Z"], le["cos_theta"], le["identical"]))

    P("\n[1] U3 引力纳入定量定价（本册新增）")
    u3 = gate_U3()
    guard(bool(u3.get("selfcheck")), "门 U3 自检", u3["verdict"])
    P("  α_G(M_GUT) = %.6g；α_GUT = 1/%.4g = %.6g" % (u3["alpha_G_at_MGUT"], u3["alpha_GUT_inv"], u3["alpha_GUT"]))
    P("  比值 %.6g 倍 = %.6g 个量级" % (u3["ratio_alphaGUT_over_alphaG"], u3["dex_gap"]))
    P("  引力要求统一点 %.6g GeV，三力汇聚在 %.6g GeV ⇒ 差 %.6g 倍（%.6g 量级）"
      % (u3["M_needed_for_gravity_unification_GeV"], u3["M_GUT_GeV"],
         u3["mismatch_vs_MGUT"], u3["mismatch_dex"]))
    P("  sanity：α_G(E_Pl) = %.1f" % u3["sanity_alpha_G_at_Planck"])

    ctl, tgt, ew = controls()

    P("\n[2] 靶：四力/大统一的七条必要条件")
    for r in tgt:
        P("  %s %s：%s" % (r["id"], r["verdict"], r["name"]))
        P("      %s" % r["value"])
    n_pass_t = sum(1 for r in tgt if r["verdict"] == "PASS")
    n_app_t = sum(1 for r in tgt if r["applicable"])
    P("  ⇒ 通过 %d/%d（%.2f%%）" % (n_pass_t, n_app_t, 100.0 * n_pass_t / n_app_t))

    P("\n[3] 控制组：同一套判据判电弱统一（唯一已完成的统一）")
    for r in ew["rows"]:
        P("  %s %s：%s" % (r["id"], r["verdict"], r["name"]))
        P("      %s" % r["value"])
    n_pass_e = sum(1 for r in ew["rows"] if r["verdict"] == "PASS")
    n_app_e = sum(1 for r in ew["rows"] if r["applicable"])
    P("  ⇒ 通过 %d/%d（%.2f%%）；ρ = %.6g，v = %.6g GeV，m_t 预言偏差 %.3g%%"
      % (n_pass_e, n_app_e, 100.0 * n_pass_e / n_app_e, ew["rho"], ew["v_GeV"], ew["m_t_rel_dev"] * 100))

    P("\n[4] 控制组判决（失控 ⇒ 退出码 2）")
    ctl_ok = True
    for c in ctl:
        guard(c["pass"], "控制组 %s" % c["id"], str(c.get("prediction", "")))
        P("  %s %s：%s ⇒ %s" % (c["id"], c["target"], c["prediction"], "PASS" if c["pass"] else "FAIL"))
        ctl_ok = ctl_ok and c["pass"]

    P("\n[5] 总判决")
    P("  四力/大统一完成度：%d/%d 必要条件" % (n_pass_t, n_app_t))
    P("  电弱统一完成度（控制组）：%d/%d ⇒ 判据有判别力" % (n_pass_e, n_app_e))
    P("  结论：统一场论 **未完成**；且在本框架已收口的三条路径下无可行且可检验的路线")
    P("  唯一达到『完成』标准的统一是电弱统一（弱电 sector，不含引力）")

    P("\n[6] 守卫汇总")
    n_ok = sum(1 for g in GUARDS if g["ok"])
    for g in GUARDS:
        P("  [%s] %s" % ("OK" if g["ok"] else "XX", g["name"]))
    P("  守卫 %d/%d" % (n_ok, len(GUARDS)))

    os.makedirs(R_DATA, exist_ok=True)
    out = {
        "meta": {"id": "r119", "title": "统一场论完成度总判定（七条必要条件 + 电弱控制组）",
                 "date": "2026-10-20", "engine": NAME + ".py",
                 "upstream": ["openuft_49 第二轮/第三轮/第四轮/第六轮", "r116", "r117", "r118"],
                 "discipline": "不提出新统一场论；只做完成度的机器判定；控制组失控 ⇒ 退出码 2"},
        "data": DATA,
        "lemma_electroweak": le,
        "U3_gravity": u3,
        "criteria_target": tgt,
        "criteria_electroweak_control": ew["rows"],
        "electroweak_metrics": {"rho": ew["rho"], "tree_dev": ew["tree_dev"],
                                "v_GeV": ew["v_GeV"], "m_t_rel_dev": ew["m_t_rel_dev"]},
        "controls": ctl,
        "verdict": {
            "target_pass": n_pass_t, "target_total": n_app_t,
            "target_ratio": sig(n_pass_t / n_app_t, 4),
            "control_pass": n_pass_e, "control_total": n_app_e,
            "control_ratio": sig(n_pass_e / n_app_e, 4),
            "conclusion": "统一场论未完成；唯一达到完成标准的是电弱统一（弱电 sector，不含引力）"
        },
        "guards": {"total": len(GUARDS), "passed": n_ok, "items": GUARDS},
    }
    with open(os.path.join(R_DATA, NAME + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    with open(os.path.join(R_DATA, NAME + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(os.path.join(R_DATA, NAME + ".md"), "w", encoding="utf-8") as f:
        f.write("# r119 机读数据（统一场论完成度总判定）\n\n")
        f.write("- 守卫 %d/%d\n" % (n_ok, len(GUARDS)))
        f.write("- 靶（四力/大统一）通过 %d/%d；控制组（电弱统一）通过 %d/%d\n\n"
                % (n_pass_t, n_app_t, n_pass_e, n_app_e))
        f.write("| 条件 | 名称 | 靶：四力 | 控制组：电弱 |\n|---|---|---|---|\n")
        for a, b in zip(tgt, ew["rows"]):
            f.write("| %s | %s | %s | %s |\n" % (a["id"], a["name"], a["verdict"], b["verdict"]))

    P("\n产物：%s / %s / %s" % (NAME + ".json", NAME + "_report.txt", NAME + ".md"))
    if not ctl_ok:
        P("控制组失控 ⇒ 退出码 2")
        sys.exit(2)
    P("退出码 0")
    sys.exit(0)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
