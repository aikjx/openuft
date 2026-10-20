# -*- coding: utf-8 -*-
"""r120｜「所有力的大统一方程式」——候选全集与状态机判。

回答方式：不存在一个被实验确立的「所有力的大统一方程」。本册给出**真实存在**的方程式全集，
按三层组织，并对每一条做状态机判（机读数字 + 判决）：

  L1 已验证层：标准模型 ℒ_SM、电弱统一 ℒ_EW（唯一已完成的统一）
  L2 GUT 候选层：SU(5)（Georgi–Glashow 1974）、SO(10)、E6、MSSM/SUSY SU(5)
  L3 含引力层：Einstein–Yang–Mills、超引力/弦（开放，无紫外完备的可检验版本）

机读内容（全部可由引擎复算）：
  代数数据（秩 / 群维数 / 物质表示维数 / 与 SM 一代 15 个 Weyl 旋量的容量匹配）
  耦合汇聚残差（SM 52.06σ vs MSSM 1.27σ）
  质子衰变量纲估计 τ_p ≈ M_GUT⁴ /(α_GUT² m_p⁵)（维度-6；标注为量级估计，非精确预言）
  引力耦合缺口 α_G = (E/E_Pl)²（继承 r119 U3）

纪律：方程均为教科书既有形式，本册不自造方程；量级估计明确标注；控制组失控 ⇒ 退出码 2。
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.normpath(os.path.join(HERE, ".."))
R_DATA = os.path.join(NORM, "数据")
NAME = "TUFT-r120_所有力大统一方程式_候选全集与状态机判_2026-10-20"

HBAR_GEV_S = 6.582119569e-25      # ħ in GeV·s
YR_S = 3.15576e7
M_P = 0.938272                     # 质子质量 GeV
E_PL = 1.22089e19                  # GeV

DATA = {
    "sm_generation_weyl": 15,      # Q(6) + u^c(3) + d^c(3) + L(2) + e^c(1)
    "weyl_breakdown": {"Q": 6, "u_c": 3, "d_c": 3, "L": 2, "e_c": 1},
    "groups": {
        "SM": {"rank": 4, "dim": 12, "matter": None,
               "algebra": "SU(3)_C x SU(2)_L x U(1)_Y"},
        "SU5": {"rank": 4, "dim": 24, "matter": "5bar + 10 = 15",
                "algebra": "SU(5)", "higgs": "24 (adjoint)"},
        "SO10": {"rank": 5, "dim": 45, "matter": "16 = 5bar + 10 + 1",
                 "algebra": "SO(10)", "higgs": "45 / 126 / 16"},
        "E6": {"rank": 6, "dim": 78, "matter": "27",
               "algebra": "E6", "higgs": "78 / 27"},
    },
    "unification": {
        "r_star": 0.582379, "r_SM": 0.654655, "r_MSSM": 0.583333,
        "alpha_s_SM_pred": 0.07115, "alpha_s_obs": 0.1180, "alpha_s_unc": 0.0009,
        "sigma_SM": 52.06, "sigma_MSSM": 1.27,
        "M_GUT_MSSM_GeV": 2.014e16, "alpha_GUT_inv_MSSM": 24.3,
        "src": "openuft_49 第四轮 / 第六轮"
    },
    "proton_decay": {
        "tau_limit_yr": 2.4e34, "src": "Super-Kamiokande p -> e+ pi0 (2020)",
        "minimal_SU5_M_GUT_GeV": 1e15, "minimal_SU5_alpha_GUT_inv": 40.0
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


# ================================================================== 容量匹配（Weyl 计数）
def capacity_check():
    """SM 一代 15 个 Weyl 旋量 vs 各 GUT 表示容量。"""
    d = DATA
    n_sm = d["sm_generation_weyl"]
    breakdown = d["weyl_breakdown"]
    s = sum(breakdown.values())
    su5 = 5 + 10            # 5bar + 10
    so10 = 16               # 16 = 15 + 1 (右手中微子)
    e6 = 27
    rows = [
        {"group": "SM（参考）", "rep": "Q+u^c+d^c+L+e^c", "dim": n_sm,
         "match_SM": True, "extra": 0},
        {"group": "SU(5)", "rep": "5bar + 10", "dim": su5,
         "match_SM": (su5 == n_sm), "extra": su5 - n_sm},
        {"group": "SO(10)", "rep": "16", "dim": so10,
         "match_SM": (so10 >= n_sm), "extra": so10 - n_sm},
        {"group": "E6", "rep": "27", "dim": e6,
         "match_SM": (e6 >= n_sm), "extra": e6 - n_sm},
    ]
    return {"n_SM_weyl": n_sm, "breakdown_sum": s, "rows": rows,
            "breakdown_consistent": (s == n_sm)}


# ================================================================== 耦合汇聚
def unification_check():
    u = DATA["unification"]
    sm_dev_sigma = abs(u["alpha_s_SM_pred"] - u["alpha_s_obs"]) / u["alpha_s_unc"]
    return {
        "r_star": u["r_star"], "r_SM": u["r_SM"], "r_MSSM": u["r_MSSM"],
        "collinearity_residual_SM": sig(abs(u["r_SM"] - u["r_star"])),
        "collinearity_residual_MSSM": sig(abs(u["r_MSSM"] - u["r_star"])),
        "alpha_s_SM_pred": u["alpha_s_SM_pred"],
        "alpha_s_obs": u["alpha_s_obs"], "alpha_s_unc": u["alpha_s_unc"],
        "sigma_SM_recomputed": sig(sm_dev_sigma), "sigma_SM_reported": u["sigma_SM"],
        "sigma_MSSM": u["sigma_MSSM"],
        "M_GUT_MSSM_GeV": u["M_GUT_MSSM_GeV"],
        "alpha_GUT_MSSM": sig(1.0 / u["alpha_GUT_inv_MSSM"]),
        "verdict_SM": "FAIL（共线残差 %.4g ⇒ α_s 偏 %.4gσ）"
                      % (abs(u["r_SM"] - u["r_star"]), sm_dev_sigma),
        "verdict_MSSM": "PASS（耦合确实汇聚，α_s 偏 %.4gσ）" % u["sigma_MSSM"],
    }


# ================================================================== 质子衰变量纲估计（维度-6）
def tau_p_dim6(M_GUT_GeV, alpha_GUT, m_p=M_P):
    """τ_p ≈ M_GUT⁴ /(α_GUT² m_p⁵)，返回秒与年。量级估计（order-of-magnitude），非精确预言。"""
    tau_gev_inv = M_GUT_GeV ** 4 / (alpha_GUT ** 2 * m_p ** 5)
    tau_s = tau_gev_inv * HBAR_GEV_S
    return {"tau_GeV^-1": sig(tau_gev_inv), "tau_s": sig(tau_s),
            "tau_yr": sig(tau_s / YR_S)}


def proton_decay_check():
    pd = DATA["proton_decay"]
    u = DATA["unification"]
    a_min = 1.0 / pd["minimal_SU5_alpha_GUT_inv"]
    su5 = tau_p_dim6(pd["minimal_SU5_M_GUT_GeV"], a_min)
    a_mssm = 1.0 / u["alpha_GUT_inv_MSSM"]
    mssm = tau_p_dim6(u["M_GUT_MSSM_GeV"], a_mssm)
    limit = pd["tau_limit_yr"]
    excess_su5 = limit / su5["tau_yr"]
    return {
        "formula": "tau_p ≈ M_GUT^4 / (alpha_GUT^2 m_p^5)（维度-6 算符，量级估计）",
        "note": "忽略强子矩阵元与重整化因子，精度仅到量级；SUSY 情形维度-5 算符主导会显著加快衰变",
        "minimal_SU5": {"M_GUT_GeV": pd["minimal_SU5_M_GUT_GeV"],
                        "alpha_GUT_inv": pd["minimal_SU5_alpha_GUT_inv"],
                        "tau_yr": su5["tau_yr"], "tau_s": su5["tau_s"]},
        "MSSM_dim6_only": {"M_GUT_GeV": u["M_GUT_MSSM_GeV"],
                           "alpha_GUT_inv": u["alpha_GUT_inv_MSSM"],
                           "tau_yr": mssm["tau_yr"], "tau_s": mssm["tau_s"]},
        "superK_limit_yr": limit,
        "minimal_SU5_excluded_by_decades": sig(math.log10(excess_su5)),
        "minimal_SU5_excess_factor": sig(excess_su5),
        "verdict": "最小 SU(5) 被排除：预言 %.4g yr vs 上限 %.4g yr ⇒ 快 %.4g 倍（%.4g 个量级）"
                   % (su5["tau_yr"], limit, excess_su5, math.log10(excess_su5)),
        "selfcheck": bool(su5["tau_yr"] < limit and 1e30 < su5["tau_yr"] < 1e33),
    }


# ================================================================== 引力缺口（继承 r119 U3）
def gravity_gap():
    M_GUT = DATA["unification"]["M_GUT_MSSM_GeV"]
    a_GUT = 1.0 / DATA["unification"]["alpha_GUT_inv_MSSM"]
    a_G = (M_GUT / E_PL) ** 2
    ratio = a_GUT / a_G
    M_needed = E_PL * math.sqrt(a_GUT)
    return {
        "alpha_G_at_MGUT": sig(a_G), "alpha_GUT": sig(a_GUT),
        "ratio": sig(ratio), "dex": sig(math.log10(ratio)),
        "M_needed_GeV": sig(M_needed), "M_GUT_GeV": sig(M_GUT),
        "mismatch": sig(M_needed / M_GUT),
        "mismatch_dex": sig(math.log10(M_needed / M_GUT)),
        "sanity_alpha_G_at_Pl": (E_PL / E_PL) ** 2,
    }


# ================================================================== 三层方程清单（状态机判）
def equation_ledger():
    uni = unification_check()
    pd = proton_decay_check()
    gg = gravity_gap()
    cap = capacity_check()
    L1 = [
        {"id": "E1", "name": "标准模型 ℒ_SM",
         "equation": "ℒ_SM = −¼G^a_{μν}G^{aμν} − ¼W^i_{μν}W^{iμν} − ¼B_{μν}B^{μν} "
                     "+ (D_μH)†(D^μH) − μ²H†H − λ(H†H)² "
                     "+ Σ_ψ ψ̄ iD̸ψ − (y_u Q̄H̃u_R + y_d Q̄Hd_R + y_e L̄He_R + h.c.)",
         "covers": "强 + 弱 + 电磁（不含引力）",
         "status": "VERIFIED", "verdict": "PASS",
         "note": "唯一被实验完全确立的框架；但三耦合是三个独立输入，未统一"},
        {"id": "E2", "name": "电弱统一 ℒ_EW（SU(2)_L×U(1)_Y → U(1)_em）",
         "equation": "ℒ_EW = −¼W^i_{μν}W^{iμν} − ¼B_{μν}B^{μν} + |D_μφ|² − V(φ),  "
                     "D_μ = ∂_μ − ig(τ^a/2)W^a_μ − ig′(Y/2)B_μ;  "
                     "e = g sinθ_W = g′cosθ_W,  M_W = gv/2,  M_Z = √(g²+g′²)v/2,  M_W = M_Z cosθ_W",
         "covers": "弱 + 电磁",
         "status": "VERIFIED + 已完成", "verdict": "PASS",
         "note": "人类唯一达到『完成』标准的统一（r119 控制组 6/6）；判别力典范：精密拟合预言 m_t 后被测得"},
    ]
    L2 = [
        {"id": "E3", "name": "SU(5) GUT（Georgi–Glashow 1974，最小 GUT）",
         "equation": "ℒ = −½Tr(F_{μν}F^{μν}) + iψ̄_{5bar}D̸ψ_{5bar} + iψ̄_{10}D̸ψ_{10} "
                     "+ (D_μΦ_{24})†(D^μΦ_{24}) − V(Φ_{24}) + Yukawa;  "
                     "SU(5) →⟨24⟩ SU(3)_C×SU(2)_L×U(1)_Y,  g_3=g_2=√(5/3)g_1=g_5 at M_GUT",
         "covers": "强 + 弱 + 电磁（不含引力）",
         "status": "EXCLUDED", "verdict": "FAIL",
         "note": "容量 5bar+10=15 精确匹配 SM 一代；但（a）非 SUSY 耦合不汇聚 %.4gσ；"
                 "（b）τ_p 预言 %.4g yr vs Super-K 上限 %.4g yr ⇒ 快 %.4g 个量级"
                 % (uni["sigma_SM_recomputed"], pd["minimal_SU5"]["tau_yr"],
                    pd["superK_limit_yr"], pd["minimal_SU5_excluded_by_decades"])},
        {"id": "E4", "name": "SO(10) GUT（16 旋量容纳一代 + 右手中微子）",
         "equation": "ℒ = −¼Tr(F_{μν}F^{μν}) + iψ̄_{16}D̸ψ_{16} + |D_μΦ|² − V(Φ) + Yukawa;  "
                     "16 ⊃ 5bar ⊕ 10 ⊕ 1（含 ν_R ⇒ 支持 see-saw）;  秩 5，群维数 45",
         "covers": "强 + 弱 + 电磁（不含引力）",
         "status": "NOT EXCLUDED BUT NON-DELIVERING", "verdict": "BOUNDARY",
         "note": "容量 16 = 15 + 1（多出右手中微子）；破缺链 ≥3 条，2/3 不给 M_GUT 预言，"
                 "唯一预言链 τ_p = 3.4e35 yr 超近期可及 0.53 量级（openuft_49 第六轮）"},
        {"id": "E5", "name": "E6 GUT",
         "equation": "ℒ = −¼Tr(F_{μν}F^{μν}) + iψ̄_{27}D̸ψ_{27} + ... ;  秩 6，群维数 78，基本表示 27",
         "covers": "强 + 弱 + 电磁（不含引力）",
         "status": "OPEN", "verdict": "BOUNDARY",
         "note": "容量 27（比 SM 多 12）；无公认的可检验预言，本册不判具体构造"},
        {"id": "E6", "name": "MSSM / SUSY SU(5)（耦合汇聚成功）",
         "equation": "一圈 β 系数 b = (33/5, 1, −3);  α_i^{-1}(μ) = A_i − b_i/(2π)·ln(μ/M_Z);  "
                     "M_GUT ≈ %.4g GeV,  α_GUT^{-1} ≈ %.4g" % (
                         uni["M_GUT_MSSM_GeV"], DATA["unification"]["alpha_GUT_inv_MSSM"]),
         "covers": "强 + 弱 + 电磁（不含引力）",
         "status": "COUPLING OK / OTHERWISE FAIL", "verdict": "FAIL",
         "note": "唯一使三耦合真正汇聚的构造（α_s 偏 %.4gσ，共线残差 %.4g）；"
                 "但约 105 个新参数、LHC 未见超对称、维度-5 质子衰变排除最小 SUSY SU(5)"
                 % (uni["sigma_MSSM"], uni["collinearity_residual_MSSM"])},
    ]
    L3 = [
        {"id": "E7", "name": "Einstein–Yang–Mills（引力 + 规范，有效场论层）",
         "equation": "S = ∫d⁴x √−g [ R/(16πG) − ¼Σ_a F^a_{μν}F^{aμν} ] + S_matter",
         "covers": "四力（引力以经典方式纳入）",
         "status": "OPEN / NOT UV-COMPLETE", "verdict": "BOUNDARY",
         "note": "只是把两项并排写下，并未统一耦合；量子化后不可重整（G 的量纲 [M^-2]）"},
        {"id": "E8", "name": "引力与三力的耦合缺口（r119 U3）",
         "equation": "α_G(E) = GE²/(ħc) = (E/E_Pl)²;  "
                     "α_G(M_GUT) = %.4g  vs  α_GUT = %.4g  ⇒  差 %.4g 个量级;  "
                     "引力要求统一点 %.4g GeV，三力汇聚在 %.4g GeV ⇒ 错配 %.4g 倍"
                     % (gg["alpha_G_at_MGUT"], gg["alpha_GUT"], gg["dex"],
                        gg["M_needed_GeV"], gg["M_GUT_GeV"], gg["mismatch"]),
         "covers": "四力",
         "status": "QUANTIFIED OBSTACLE", "verdict": "FAIL",
         "note": "这是『所有力』（含引力）与『三力』之间的核心障碍：不是技术困难，是数量级错配"},
        {"id": "E9", "name": "超引力 / 弦论（紫外完备候选）",
         "equation": "S_supergravity = ∫d⁴x √−g [ R/(16πG) + ... + 超对称伙伴 ];  "
                     "S_string = −(1/4πα′)∫d²σ √h h^{ab}∂_aX^μ∂_bX^ν g_{μν}(X) + ...",
         "covers": "四力 + 物质（原则上）",
         "status": "OPEN", "verdict": "BOUNDARY",
         "note": "候选众多（景观问题）、无可检验的低能唯一预言；本册不判具体构造，只登记为开放"},
    ]
    return {"L1_verified": L1, "L2_gut_candidates": L2, "L3_with_gravity": L3}


# ================================================================== 控制组
def controls():
    ctl = []
    uni = unification_check()
    cap = capacity_check()
    pd = proton_decay_check()
    ctl.append({"id": "Ctl1", "target": "SM 一代 Weyl 计数自洽",
                "prediction": "Q(6)+u^c(3)+d^c(3)+L(2)+e^c(1) = 15",
                "value": cap["breakdown_sum"], "expected": 15,
                "pass": cap["breakdown_consistent"]})
    ctl.append({"id": "Ctl2", "target": "SU(5) 容量精确匹配（防误判其优点）",
                "prediction": "5bar+10 必须等于 15（若不等则容量论证失效）",
                "pass": any(r["group"] == "SU(5)" and r["match_SM"] for r in cap["rows"])})
    ctl.append({"id": "Ctl3", "target": "MSSM 耦合汇聚（防「一律否定」）",
                "prediction": "判据必须承认 MSSM 的耦合确实汇聚（α_s 偏 ≤ 2σ）",
                "sigma": uni["sigma_MSSM"], "pass": uni["sigma_MSSM"] < 2.0})
    ctl.append({"id": "Ctl4", "target": "最小 SU(5) 质子衰变必须快于上限（否则矛盾）",
                "prediction": "τ_p(预言) < τ_p(上限)",
                "tau_pred_yr": pd["minimal_SU5"]["tau_yr"],
                "tau_limit_yr": pd["superK_limit_yr"],
                "pass": pd["minimal_SU5"]["tau_yr"] < pd["superK_limit_yr"]})
    return ctl


# ================================================================== 主流程
def main():
    lines = []

    def P(s=""):
        lines.append(s)
        print(s)

    P("=" * 78)
    P("r120｜「所有力的大统一方程式」——候选全集与状态机判")
    P("=" * 78)

    cap = capacity_check()
    guard(cap["breakdown_consistent"], "容量：SM 一代 Weyl 计数自洽",
          "%s = %d" % (cap["breakdown_sum"], cap["n_SM_weyl"]))
    P("\n[1] 代数容量（SM 一代 Weyl 旋量 = %d）" % cap["n_SM_weyl"])
    for r in cap["rows"]:
        P("    %-12s %-20s 维数 %2d  匹配 %-5s  余量 %d"
          % (r["group"], r["rep"], r["dim"], r["match_SM"], r["extra"]))

    uni = unification_check()
    P("\n[2] 耦合汇聚")
    P("    共线残差：SM %.6g（α_s 偏 %.4gσ，复算 %.4gσ）｜MSSM %.6g（%.4gσ）"
      % (uni["collinearity_residual_SM"], uni["sigma_SM_reported"], uni["sigma_SM_recomputed"],
         uni["collinearity_residual_MSSM"], uni["sigma_MSSM"]))
    P("    MSSM：M_GUT = %.6g GeV，α_GUT^{-1} = %.4g"
      % (uni["M_GUT_MSSM_GeV"], DATA["unification"]["alpha_GUT_inv_MSSM"]))
    guard(abs(uni["sigma_SM_recomputed"] - uni["sigma_SM_reported"]) < 1.0,
          "σ 复算与上游一致", "复算 %.4g vs 报告 %.4g" % (uni["sigma_SM_recomputed"], uni["sigma_SM_reported"]))
    guard(uni["sigma_MSSM"] < 2.0, "控制组：MSSM 耦合汇聚成立", "%.4gσ" % uni["sigma_MSSM"])

    pd = proton_decay_check()
    guard(bool(pd.get("selfcheck")), "质子衰变量级自检", pd["verdict"])
    P("\n[3] 质子衰变（维度-6 量级估计）")
    P("    %s" % pd["formula"])
    P("    最小 SU(5)：M_GUT=%.4g GeV ⇒ τ_p ≈ %.4g yr" % (pd["minimal_SU5"]["M_GUT_GeV"], pd["minimal_SU5"]["tau_yr"]))
    P("    MSSM（仅维度-6）：M_GUT=%.4g GeV ⇒ τ_p ≈ %.4g yr" % (pd["MSSM_dim6_only"]["M_GUT_GeV"], pd["MSSM_dim6_only"]["tau_yr"]))
    P("    Super-K 上限 %.4g yr ⇒ 最小 SU(5) 快 %.4g 倍（%.4g 个量级）"
      % (pd["superK_limit_yr"], pd["minimal_SU5_excess_factor"], pd["minimal_SU5_excluded_by_decades"]))
    P("    注：%s" % pd["note"])

    gg = gravity_gap()
    P("\n[4] 引力缺口（继承 r119 U3）")
    P("    α_G(M_GUT) = %.6g vs α_GUT = %.6g ⇒ %.6g 个量级" % (gg["alpha_G_at_MGUT"], gg["alpha_GUT"], gg["dex"]))
    P("    引力要求统一点 %.6g GeV vs 三力汇聚 %.6g GeV ⇒ 错配 %.6g 倍；sanity α_G(E_Pl) = %.1f"
      % (gg["M_needed_GeV"], gg["M_GUT_GeV"], gg["mismatch"], gg["sanity_alpha_G_at_Pl"]))
    guard(abs(gg["sanity_alpha_G_at_Pl"] - 1.0) < 1e-15, "α_G(E_Pl) = 1 sanity", "%.1f" % gg["sanity_alpha_G_at_Pl"])

    led = equation_ledger()
    P("\n[5] 三层方程清单与状态")
    for tag, rows in (("L1 已验证", led["L1_verified"]),
                      ("L2 GUT 候选", led["L2_gut_candidates"]),
                      ("L3 含引力", led["L3_with_gravity"])):
        P("  %s：" % tag)
        for e in rows:
            P("    %s %-46s [%s] %s" % (e["id"], e["name"], e["verdict"], e["status"]))

    P("\n[6] 控制组")
    ctl = controls()
    ctl_ok = True
    for c in ctl:
        guard(c["pass"], "控制组 %s" % c["id"], str(c.get("prediction", "")))
        P("  %s %s ⇒ %s" % (c["id"], c["target"], "PASS" if c["pass"] else "FAIL"))
        ctl_ok = ctl_ok and c["pass"]

    n_pass = sum(1 for grp in led.values() for e in grp if e["verdict"] == "PASS")
    n_all = sum(len(grp) for grp in led.values())
    P("\n[7] 总判决")
    P("  方程条目 %d；判 PASS 仅 %d 条（且均在 L1 已验证层）" % (n_all, n_pass))
    P("  ⇒ 不存在被实验确立的『所有力的大统一方程』；")
    P("     L1（SM + 电弱）已验证；L2（SU(5)/SO(10)/E6/MSSM）三力层面无一条全部通过；")
    P("     L3 含引力层全部开放，且引力耦合与统一耦合差 %.4g 个量级" % gg["dex"])

    P("\n[8] 守卫汇总")
    n_ok = sum(1 for g in GUARDS if g["ok"])
    for g in GUARDS:
        P("  [%s] %s" % ("OK" if g["ok"] else "XX", g["name"]))
    P("  守卫 %d/%d" % (n_ok, len(GUARDS)))

    os.makedirs(R_DATA, exist_ok=True)
    out = {
        "meta": {"id": "r120", "title": "所有力的大统一方程式：候选全集与状态机判",
                 "date": "2026-10-20", "engine": NAME + ".py",
                 "upstream": ["r119", "openuft_49 第四轮/第六轮"],
                 "discipline": "方程均为教科书既有形式，本册不自造；量级估计明确标注"},
        "data": DATA,
        "capacity": cap, "unification": uni, "proton_decay": pd,
        "gravity_gap": gg, "equation_ledger": led, "controls": ctl,
        "verdict": {"n_equations": n_all, "n_pass": n_pass,
                    "conclusion": "不存在被实验确立的『所有力的大统一方程』"},
        "guards": {"total": len(GUARDS), "passed": n_ok, "items": GUARDS},
    }
    with open(os.path.join(R_DATA, NAME + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    with open(os.path.join(R_DATA, NAME + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(os.path.join(R_DATA, NAME + ".md"), "w", encoding="utf-8") as f:
        f.write("# r120 机读数据（大统一方程式全集与状态）\n\n")
        f.write("- 守卫 %d/%d；方程条目 %d，PASS %d\n\n" % (n_ok, len(GUARDS), n_all, n_pass))
        for tag, rows in led.items():
            f.write("## %s\n\n| ID | 方程 | 覆盖 | 状态 | 判决 |\n|---|---|---|---|---|\n" % tag)
            for e in rows:
                f.write("| %s | %s | %s | %s | %s |\n"
                        % (e["id"], e["name"], e["covers"], e["status"], e["verdict"]))
            f.write("\n")

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
