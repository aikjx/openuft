# -*- coding: utf-8 -*-
"""
TUFT-r138 · 硬核审计 · ②规范群 SU(3)×SU(2)×U(1) 与 ③μ²<0 的第一性原理可导出性精算

承接 r135：r135 用「无质量自旋-2 ⇒ GR」导出 ①EH 形式与 ④SEP（Δ=−1，但循环存疑），
并指出真正的硬核是 **②规范群** 与 **③μ²<0**（已知无任何第一性原理导出路线）。
本卷正面攻这两块，回答「它们能不能被第一性原理导出」。

机检（精确有理数 Fraction；每条带反向对照以证有牙）：
  G1 SM 一圈 β 系数 (b1,b2,b3) = (41/10, −19/6, −7)（ng=3, nH=1）
  G2 渐近自由状态：SU(3) AF、SU(2) AF、U(1)_Y 不 AF（Landau 极点，跨普朗克）
  G3 渐近自由不选择群：SU(N) 的 AF 条件 n_f < 11N/2 对 N=2..8 全部通过 ⇒ 非唯一
  H1 μ² = −m_H²/2、λ = m_H²/(2v²)，与 r127 的 λ_H 交叉核验
  H2 μ²=0 ⇒ 树图 V 极小在 φ=0 ⇒ 无 EWSB（与实际 μ²<0 情形对照）

门记账（r130 准入判据）：
  ②规范群：e=0（无已知导出），任何嵌入企图（GUT/更大群+破缺扇区）a≥1 ⇒ Δ≥+1
  ③μ²<0  ：e=0，且「自然」逃逸（μ²=0、μ²~M_Pl）各自被排除 ⇒ 不可消除
  ⇒ 硬核两块 Δ≥0，UFT 完成度仍 1/7（与 r135 引力侧 Δ=−1 合计最好情况仍只 −1）

红线：数学自洽 ≠ 实验证实；文献结论与本机计算严格分列（不混充机读）。
"""
import os, json, glob, datetime, sys, math
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATE = "2026-10-21"
STEM = "TUFT-r138_硬核审计_规范群与mu2符号的第一性原理可导出性精算_%s" % DATE
JUDGE_STEM = "判定_TUFT-r138_硬核审计_规范群与mu2符号不可导出性_%s" % DATE

# ---- 观测输入 ----
M_H_GEV = F(501, 4)              # 125.25 GeV (PDG)
M_Z_GEV = 91.1876
ALPHA1_INV_MZ = 59.0             # GUT 归一化的 α_1^{-1}(M_Z)
M_PL_GEV = 1.2209e19

def load(n):
    fs = glob.glob(os.path.join(DATA, "TUFT-r%d_*.json" % n))
    if not fs:
        return None
    try:
        with open(max(fs, key=os.path.getmtime), encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

def beta_coeffs(ng=F(3), nH=F(1)):
    """SM 一圈 β 系数（约定 dg/dt = b g^3/(16π^2)，t=ln μ）。
       b3 = −11 + (2/3) n_f,  n_f = 2 ng
       b2 = −22/3 + (4/3) ng + (1/6) nH
       b1 = (4/3) ng + (1/10) nH    （GUT 归一化 U(1)）"""
    nf = 2 * ng
    b3 = F(-11) + F(2, 3) * nf
    b2 = F(-22, 3) + F(4, 3) * ng + F(1, 6) * nH
    b1 = F(4, 3) * ng + F(1, 10) * nH
    return b1, b2, b3, nf

def check_G1():
    b1, b2, b3, nf = beta_coeffs()
    ok = (b1 == F(41, 10) and b2 == F(-19, 6) and b3 == F(-7))
    # 对照：ng=4 时系数改变 ⇒ 有牙
    c1, c2, c3, _ = beta_coeffs(ng=F(4))
    ctrl = (c1 != b1 and c2 != b2 and c3 != b3)
    return {"b1": str(b1), "b2": str(b2), "b3": str(b3), "n_f": str(nf),
            "control_ng4": {"b1": str(c1), "b2": str(c2), "b3": str(c3)},
            "verdict": "PASS" if (ok and ctrl) else "FAIL",
            "note": "一圈 β 系数（GUT 归一化）；b<0 ⇒ 渐近自由"}

def check_G2():
    b1, b2, b3, _ = beta_coeffs()
    af3 = b3 < 0          # SU(3)
    af2 = b2 < 0          # SU(2)
    af1 = b1 < 0          # U(1)
    # U(1) Landau 极点：α_1^{-1}(μ)=α_1^{-1}(M_Z) − (b1/2π) ln(μ/M_Z) = 0
    expo = 2 * math.pi * ALPHA1_INV_MZ / float(b1)
    mu_gev = M_Z_GEV * math.exp(expo)
    log10_mu = math.log10(mu_gev)
    ratio_pl = mu_gev / M_PL_GEV
    log10_ratio = math.log10(ratio_pl) if ratio_pl > 0 else float("nan")
    # 对照：b1 的符号决定有无 Landau 极点
    ctrl = (af1 is False) and (b1 > 0)
    return {"b1": str(b1), "b2": str(b2), "b3": str(b3),
            "af_SU3": bool(af3), "af_SU2": bool(af2), "af_U1": bool(af1),
            "u1_landau_gev": mu_gev, "u1_landau_log10": log10_mu,
            "m_pl_gev": M_PL_GEV, "log10_ratio_over_planck": log10_ratio,
            "trans_planckian": log10_ratio > 0,
            "verdict": "PASS" if (af3 and af2 and (not af1) and ctrl and log10_ratio > 0) else "FAIL",
            "note": "U(1)_Y 非渐近自由 ⇒ 存在 Landau 极点；但跨普朗克 ⇒ 形式上的 UV 不完备，非经验上相关"}

def check_G3():
    """渐近自由条件 n_f < 11N/2：对 N=2..8、n_f=6 全部通过 ⇒ 不选择群。
       对照：n_f=40 时仅 N≥8 通过 ⇒ 约束本身有牙（对小 N 有排除力），只是本例下不唯一。"""
    nf = F(6)
    passing = [N for N in range(2, 9) if nf < F(11 * N, 2)]
    nf2 = F(40)
    passing2 = [N for N in range(2, 9) if nf2 < F(11 * N, 2)]
    non_unique = len(passing) >= 2
    ctrl_teeth = len(passing2) < len(passing)      # 换输入后约束确实排除掉一部分
    return {"n_f": str(nf), "su_N_passing": passing,
            "control_n_f": str(nf2), "control_su_N_passing": passing2,
            "non_unique": non_unique, "verdict": "PASS" if (non_unique and ctrl_teeth) else "FAIL",
            "note": "渐近自由是约束而非选择：本例下 SU(2)..SU(8) 全通过 ⇒ 不唯一确定 SU(3)"}

def check_H1():
    r127 = load(127) or {}
    comp = r127.get("computed", {})
    lam_r127 = comp.get("lambda_h")
    v_r127 = comp.get("v_from_gf")
    if lam_r127 is None or v_r127 is None:
        return {"verdict": "NO-DATA", "note": "缺少 r127 的 lambda_h / v_from_gf"}
    v = F(v_r127)
    lam = M_H_GEV ** 2 / (2 * v ** 2)
    mu2 = -(M_H_GEV ** 2) / 2
    rel = abs(float(lam) - lam_r127) / abs(lam_r127)
    # 阈值【来自输入不确定度传播】，不拍脑袋：
    #   m_H 公布值 125.25 GeV，末位半刻度 0.005 GeV ⇒ 相对 4.0e-5；
    #   λ ∝ m_H² ⇒ λ 的相对容差 = 2 × 4.0e-5 = 8.0e-5。
    mh_half_last = F(5, 1000)
    rel_unc_mh = mh_half_last / M_H_GEV
    tol = 2.0 * float(rel_unc_mh)
    # 对照：换一个 m_H（120）则 λ 明显偏离 ⇒ 交叉核验有牙
    lam_ctrl = F(120) ** 2 / (2 * v ** 2)
    rel_ctrl = abs(float(lam_ctrl) - lam_r127) / abs(lam_r127)
    ok = rel < tol
    ctrl = rel_ctrl > tol
    return {"m_h_gev": float(M_H_GEV), "v_gev": float(v),
            "lambda_computed": float(lam), "lambda_r127": lam_r127,
            "rel_diff": rel, "tolerance_derived": tol,
            "tolerance_basis": "m_H 末位半刻度 0.005 GeV 传播（λ∝m_H²）⇒ 2×4.0e-5",
            "mu2_gev2": float(mu2),
            "control_lambda_mH120": float(lam_ctrl), "control_rel_diff": rel_ctrl,
            "verdict": "PASS" if (ok and ctrl) else "FAIL",
            "note": "λ = m_H²/(2v²)、μ² = −m_H²/2 —— 二者均为由测量读出的输入，非导出"}

def check_H2():
    """V(φ)=μ²φ²/2 + λφ⁴/4。
       μ²=0   ⇒ V(v)=λv⁴/4>0=V(0) ⇒ 极小在 0 ⇒ 无 EWSB
       μ²<0   ⇒ V(v)=−λv⁴/4<0=V(0) ⇒ 极小在 v ⇒ 有 EWSB（实际情形）
       两情形互相对照 ⇒ 有牙。"""
    r127 = load(127) or {}
    comp = r127.get("computed", {})
    lam_r127 = comp.get("lambda_h"); v_r127 = comp.get("v_from_gf")
    if lam_r127 is None or v_r127 is None:
        return {"verdict": "NO-DATA"}
    lam = F(lam_r127).limit_denominator(10 ** 9)
    v = F(v_r127).limit_denominator(10 ** 6)
    def V(mu2, phi):
        return mu2 * phi ** 2 / 2 + lam * phi ** 4 / 4
    mu2_act = -(M_H_GEV ** 2) / 2
    V0 = V(F(0), F(0))
    Vv_zero = V(F(0), v)                 # μ²=0 情形
    Vv_act = V(mu2_act, v)               # 实际 μ²<0 情形
    no_ssb = (Vv_zero > V0)              # μ²=0 ⇒ 无破缺
    ssb = (Vv_act < V0)                  # μ²<0 ⇒ 有破缺
    return {"V_0": float(V0), "V_v_mu2_0": float(Vv_zero), "V_v_mu2_actual": float(Vv_act),
            "mu2_0_gives_no_EWSB": bool(no_ssb), "mu2_lt0_gives_EWSB": bool(ssb),
            "verdict": "PASS" if (no_ssb and ssb) else "FAIL",
            "note": "μ²=0（尺度不变）在树图不给 EWSB；辐射诱导（CW）为文献项，本册不重算"}

def door_accounting():
    r125 = load(125) or {}
    c125 = r125.get("computed", {})
    r130 = load(130) or {}
    s130 = r130.get("summary", {})
    non_derived = (s130.get("n_posted", 13) + s130.get("n_assumed", 16) + s130.get("n_open", 8))
    return {
        "gauge_group": {
            "e": 0, "a": 1,
            "derivable": False,
            "constraints_only": ["异常抵消（定超荷比值，不定群）",
                                 "渐近自由（约束 N_f<11N/2，不唯一）",
                                 "秩障碍 r125：rank_SM=%s > rank_Cl(1,3)=%s ⇒ 需 Cl(1,%s)"
                                 % (c125.get("rank_sm"), c125.get("rank_cl13"), c125.get("cl_min_n"))],
            "uv_defect": "U(1)_Y 非渐近自由 ⇒ Landau 极点（跨普朗克 ⇒ 形式性）",
            "delta": +1,
        },
        "mu2_sign": {
            "e": 0, "a": 0,
            "derivable": False,
            "value_from_data": "μ² = −m_H²/2、λ = m_H²/(2v²)：由 (m_H, v) 读出",
            "natural_escapes": ["μ²=0（尺度不变）⇒ 树图无 EWSB ⇒ 被 v=246 GeV 排除",
                                "μ²~M_Pl² ⇒ 层级问题（r127 B07 = 16.99 dex）"],
            "delta": 0,
        },
        "non_derived_before": non_derived,
        "combined_best_delta_with_r135": -1,
        "u_conditions_still_fail": ["U1", "U2", "U3", "U4", "U5", "U6"],
    }

def build_json(checks, door):
    payload = {
        "doc": "r136 硬核审计 · 规范群与 μ² 符号的第一性原理可导出性精算",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "scope_note": "硬核 ②③ 的可导出性精算（非加和）。文献项与本机计算分列。",
        "checks": checks,
        "door_accounting": door,
        "verdict": "HARD-CORE-NOT-DERIVABLE",
        "verdict_detail": ("②规范群：仅被约束、不被导出（e=0，且 U(1) 形式 UV 不完备）；"
                           "③μ² 符号：由数据读出，自然逃逸被排除，不可消除（e=0，Δ=0）。"
                           "硬核两块 Δ≥0 ⇒ 与 r135 引力侧合计最好仍 −1，UFT 完成度仍 1/7。"),
        "literature_items_not_recomputed": [
            "Coleman–Weinberg 辐射诱导 EWSB 在 SM 中被排除（文献项，本册不重算 CW 有效势）",
        ],
        "non_additivity_freeze": True,
        "exit_code": 0,
    }
    out = os.path.join(DATA, STEM + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out

def build_md(checks, door):
    L = []
    L.append("# %s（机读）" % STEM)
    L.append("")
    L.append("> 硬核 ②规范群 / ③μ² 的第一性原理可导出性精算。非加和。")
    L.append("")
    L.append("## 判定")
    L.append("")
    L.append("- **HARD-CORE-NOT-DERIVABLE**")
    L.append("- ②规范群 e=0（不被导出，仅被约束）；U(1) 非渐近自由 ⇒ 形式 UV 不完备")
    L.append("- ③μ² e=0（由数据读出）；自然逃逸（μ²=0 / μ²~M_Pl）均被排除")
    L.append("")
    L.append("## 机检（精确有理数，带反向对照）")
    L.append("")
    L.append("| 检查 | 内容 | 判定 |")
    L.append("|------|------|------|")
    for k, v in checks.items():
        L.append("| %s | %s | %s |" % (k, v.get("note", "")[:46], v.get("verdict")))
    L.append("")
    G2 = checks["G2"]
    L.append("### 关键读数")
    L.append("- 一圈 β 系数 (b1,b2,b3) = (%s, %s, %s)" % (
        checks["G1"]["b1"], checks["G1"]["b2"], checks["G1"]["b3"]))
    L.append("- 渐近自由：SU(3)=%s, SU(2)=%s, U(1)=%s" % (
        G2["af_SU3"], G2["af_SU2"], G2["af_U1"]))
    L.append("- U(1) Landau 极点 ≈ 10^%.1f GeV；跨普朗克 %s dex ⇒ 形式性" % (
        G2["u1_landau_log10"], round(G2["log10_ratio_over_planck"], 2)))
    L.append("- 渐近自由不选择群：n_f=6 时 SU(N) 通过者 = %s" % checks["G3"]["su_N_passing"])
    L.append("- μ² = %.1f GeV², λ 计算值 %.6f vs r127 %.6f（相对 %.2e）" % (
        checks["H1"]["mu2_gev2"], checks["H1"]["lambda_computed"],
        checks["H1"]["lambda_r127"], checks["H1"]["rel_diff"]))
    L.append("- μ²=0 ⇒ 树图 V(v)=%.3e > V(0)=0 ⇒ 无 EWSB" % checks["H2"]["V_v_mu2_0"])
    L.append("")
    out = os.path.join(DATA, STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def build_report(checks, door):
    L = []
    L.append("=" * 74)
    L.append("r136 硬核审计 · ②规范群 与 ③μ²<0 的第一性原理可导出性精算")
    L.append("=" * 74)
    L.append("生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"))
    L.append("")
    L.append("【判定】HARD-CORE-NOT-DERIVABLE")
    L.append("")
    L.append("一、机检（精确有理数，带反向对照）")
    L.append("-" * 74)
    L.append("G1 一圈 β 系数 (b1,b2,b3) = (%s, %s, %s)  对照 ng=4 → (%s, %s, %s) : %s" % (
        checks["G1"]["b1"], checks["G1"]["b2"], checks["G1"]["b3"],
        checks["G1"]["control_ng4"]["b1"], checks["G1"]["control_ng4"]["b2"],
        checks["G1"]["control_ng4"]["b3"], checks["G1"]["verdict"]))
    L.append("G2 渐近自由 SU(3)=%s SU(2)=%s U(1)=%s : %s" % (
        checks["G2"]["af_SU3"], checks["G2"]["af_SU2"], checks["G2"]["af_U1"],
        checks["G2"]["verdict"]))
    L.append("    U(1) Landau 极点 ≈ 10^%.1f GeV（跨普朗克 %.1f dex）⇒ 形式 UV 不完备" % (
        checks["G2"]["u1_landau_log10"], checks["G2"]["log10_ratio_over_planck"]))
    L.append("G3 渐近自由不选择群：n_f=6 通过 %s；对照 n_f=40 通过 %s : %s" % (
        checks["G3"]["su_N_passing"], checks["G3"]["control_su_N_passing"],
        checks["G3"]["verdict"]))
    L.append("H1 λ 计算 %.6f vs r127 %.6f（相对 %.2e）；μ²=%.1f GeV²；对照 m_H=120 → %.6f : %s" % (
        checks["H1"]["lambda_computed"], checks["H1"]["lambda_r127"],
        checks["H1"]["rel_diff"], checks["H1"]["mu2_gev2"],
        checks["H1"]["control_lambda_mH120"], checks["H1"]["verdict"]))
    L.append("H2 μ²=0 ⇒ V(v)=%.3e > V(0)=0 ⇒ 无 EWSB；μ²<0 ⇒ V(v)=%.3e < 0 ⇒ 有 EWSB : %s" % (
        checks["H2"]["V_v_mu2_0"], checks["H2"]["V_v_mu2_actual"], checks["H2"]["verdict"]))
    L.append("")
    L.append("二、门记账")
    L.append("-" * 74)
    gg = door["gauge_group"]
    L.append("②规范群：e=%d a=%d Δ=%+d" % (gg["e"], gg["a"], gg["delta"]))
    for c in gg["constraints_only"]:
        L.append("    仅约束：%s" % c)
    L.append("    UV 缺陷：%s" % gg["uv_defect"])
    ms = door["mu2_sign"]
    L.append("③μ² ：e=%d a=%d Δ=%+d" % (ms["e"], ms["a"], ms["delta"]))
    L.append("    %s" % ms["value_from_data"])
    for e in ms["natural_escapes"]:
        L.append("    逃逸被排除：%s" % e)
    L.append("")
    L.append("三、诚实结论")
    L.append("-" * 74)
    L.append("硬核两块 Δ≥0：规范群不可导出（且 U(1) 形式 UV 不完备），μ² 不可导出且不可消除。")
    L.append("与 r135 引力侧 Δ=−1 合计，最好情况仍为 −1，且要求四块 POSTED 全导出才算完成")
    L.append("⇒ UFT 完成度仍 1/7（U1/U2/U3/U4/U5/U6 仍 FAIL）。")
    L.append("")
    L.append("文献项（本册未重算，不混入机读）：")
    for lit in ["Coleman–Weinberg 辐射诱导 EWSB 在 SM 中被排除"]:
        L.append("  - %s" % lit)
    L.append("")
    L.append("=" * 74)
    out = os.path.join(DATA, STEM + "_report.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def build_judge(checks, door):
    gg = door["gauge_group"]; ms = door["mu2_sign"]
    L = []
    L.append("# 判定_TUFT-r138 · 硬核审计 · ②规范群 与 ③μ² 符号的不可导出性")
    L.append("")
    L.append("**卷号**：r138（增补卷）")
    L.append("**分工声明**：r136 = 并行会话《力的大统一方程·非GUT候选族补齐与全链路终局账本》")
    L.append("  （已产出 json/md/_report 三件套 + 判定册，为 r136 的权威版本）；")
    L.append("  本册 r138 为独立的硬核（②规范群 / ③μ²）可导出性审计，**两册条目不可相加**。")
    L.append("**日期**：%s" % DATE)
    L.append("**类别**：硬核可导出性精算（承接 r135 所指硬核）")
    L.append("")
    L.append("## 卷首分工声明")
    L.append("")
    L.append("- 本卷正面攻 r135 指出的两块硬核：②规范群、③μ²<0。")
    L.append("- **各源卷拥有其条目；本卷机检与门记账独立，条目非加和。**")
    L.append("- **文献项与本机计算严格分列**：文献结论不混入机读结论。")
    L.append("- 红线：数学自洽 ≠ 实验证实。")
    L.append("")
    L.append("## 0. 判定")
    L.append("")
    L.append("> **HARD-CORE-NOT-DERIVABLE**")
    L.append(">")
    L.append("> ②规范群：**仅被约束、不被导出**；且 U(1)_Y 形式 UV 不完备（Landau 极点，跨普朗克）。")
    L.append("> ③μ²<0：**由数据读出**，自然逃逸（μ²=0 / μ²~M_Pl）均被排除 ⇒ 不可消除。")
    L.append(">")
    L.append("> 硬核两块 Δ≥0 ⇒ 与 r135 引力侧合计最好仍 −1 ⇒ **UFT 完成度仍 1/7**。")
    L.append("")
    L.append("## 1. 机检（精确有理数，每条带反向对照）")
    L.append("")
    L.append("| 检查 | 内容 | 结果 | 判定 |")
    L.append("|------|------|------|------|")
    L.append("| **G1** | SM 一圈 β 系数 | (b1,b2,b3)=(%s, %s, %s)；对照 ng=4 → (%s,%s,%s) | %s |"
             % (checks["G1"]["b1"], checks["G1"]["b2"], checks["G1"]["b3"],
                checks["G1"]["control_ng4"]["b1"], checks["G1"]["control_ng4"]["b2"],
                checks["G1"]["control_ng4"]["b3"], checks["G1"]["verdict"]))
    L.append("| **G2** | 渐近自由 / U(1) Landau | SU(3)=%s, SU(2)=%s, U(1)=%s | %s |"
             % (checks["G2"]["af_SU3"], checks["G2"]["af_SU2"], checks["G2"]["af_U1"],
                checks["G2"]["verdict"]))
    L.append("| **G3** | 渐近自由的选择力 | n_f=6 通过 %s；对照 n_f=40 通过 %s | %s |"
             % (checks["G3"]["su_N_passing"], checks["G3"]["control_su_N_passing"],
                checks["G3"]["verdict"]))
    L.append("| **H1** | μ²/λ 由测量读出 | μ²=%.1f GeV²；λ 计算 %.6f vs r127 %.6f（相对 %.1e） | %s |"
             % (checks["H1"]["mu2_gev2"], checks["H1"]["lambda_computed"],
                checks["H1"]["lambda_r127"], checks["H1"]["rel_diff"], checks["H1"]["verdict"]))
    L.append("| **H2** | μ²=0 ⇒ 树图无 EWSB | V(v)=%.2e > V(0)=0；实际 μ²<0 时 V(v)=%.2e < 0 | %s |"
             % (checks["H2"]["V_v_mu2_0"], checks["H2"]["V_v_mu2_actual"], checks["H2"]["verdict"]))
    L.append("")
    L.append("## 2. ②规范群：被约束，但不被导出")
    L.append("")
    L.append("### 2.1 已有的约束（都只约束，不定群）")
    for c in gg["constraints_only"]:
        L.append("- %s" % c)
    L.append("")
    L.append("### 2.2 一个真发现：U(1)_Y 形式上不 UV 完备")
    L.append("- 一圈 β 系数：b1=%s>0、b2=%s<0、b3=%s<0" % (
        checks["G2"]["b1"], checks["G2"]["b2"], checks["G2"]["b3"]))
    L.append("- ⇒ SU(3)、SU(2) 渐近自由；**U(1)_Y 不渐近自由**，存在 Landau 极点。")
    L.append("- Landau 极点 ≈ 10^%.1f GeV，跨普朗克约 %.1f dex ⇒ **形式上的** UV 不完备，"
             % (checks["G2"]["u1_landau_log10"], checks["G2"]["log10_ratio_over_planck"]))
    L.append("  不是经验上相关的问题（远高于普朗克尺度）。诚实登记，不夸大。")
    L.append("")
    L.append("### 2.3 门记账")
    L.append("- e=%d（无已知导出）、a=%d（任何嵌入企图需更大群+破缺扇区）⇒ Δ=%+d" % (
        gg["e"], gg["a"], gg["delta"]))
    L.append("")
    L.append("## 3. ③μ²<0：由数据读出，且不可消除")
    L.append("")
    L.append("- %s" % ms["value_from_data"])
    L.append("- 交叉核验：λ 计算值 %.6f 与 r127 的 λ_H=%.6f 一致（相对 %.1e）"
             % (checks["H1"]["lambda_computed"], checks["H1"]["lambda_r127"],
                checks["H1"]["rel_diff"]))
    L.append("- μ²=0（尺度不变）在树图不给 EWSB：V(v)=%.2e > V(0)=0" % checks["H2"]["V_v_mu2_0"])
    for e in ms["natural_escapes"]:
        L.append("- 逃逸被排除：%s" % e)
    L.append("- 门记账：e=%d、a=%d ⇒ Δ=%+d" % (ms["e"], ms["a"], ms["delta"]))
    L.append("")
    L.append("## 4. 文献项（本册未重算，不混入机读）")
    L.append("")
    L.append("- Coleman–Weinberg 辐射诱导 EWSB 在 SM 中被排除——**文献结论**，")
    L.append("  本册**不重算** CW 有效势，故不作为机读结论，仅登记。")
    L.append("")
    L.append("## 5. 诚实结论")
    L.append("")
    L.append("1. r135 的指认得到确认：**②与③才是真正的硬核**，已知无任何第一性原理导出路线。")
    L.append("2. ②仅被约束（异常抵消定超荷比值、渐近自由定 N_f 上界、秩障碍定最小代数 Cl(1,11)），")
    L.append("   **不被导出**；且 U(1) 有形式 UV 不完备。")
    L.append("3. ③的取值由 (m_H, v) 读出；μ²=0 与 μ²~M_Pl 两条自然出路均被排除 ⇒ **不可消除**。")
    L.append("4. 硬核 Δ≥0 ⇒ 与 r135 引力侧合计最好 −1；UFT 要求四块 POSTED 全导出才算完成")
    L.append("   ⇒ **完成度仍 1/7**（U1/U2/U3/U4/U5/U6 仍 FAIL）。")
    L.append("")
    L.append("## 附录 · Glossary")
    L.append("- **渐近自由**：b<0 ⇒ 耦合随能标升高而减小；b>0 ⇒ 有 Landau 极点。")
    L.append("- **Landau 极点**：一圈跑动使 α^{-1}→0 的能标。")
    L.append("- **尺度不变（μ²=0）**：树图无 EWSB；需辐射诱导（CW）才可能破缺。")
    L.append("- **HARD-CORE-NOT-DERIVABLE**：硬核前提仅被约束、不被导出。")
    L.append("")
    L.append("## 数据出处")
    L.append("- 机读册：`数据/%s.json` / `.md`" % STEM)
    L.append("- 上游：r127（λ_H、v）、r125（rank_SM/rank_Cl(1,3)/Cl(1,11)）、r130（前提账本）、r135（Δ=−1）")
    out = os.path.join(DATA, JUDGE_STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def main():
    os.makedirs(DATA, exist_ok=True)
    checks = {"G1": check_G1(), "G2": check_G2(), "G3": check_G3(),
              "H1": check_H1(), "H2": check_H2()}
    for k, v in checks.items():
        if v.get("verdict") not in ("PASS",):
            print("GUARD FAIL:", k, v)
            return 2
    door = door_accounting()
    p1 = build_json(checks, door)
    p2 = build_md(checks, door)
    p3 = build_report(checks, door)
    p4 = build_judge(checks, door)
    print("OK generated:")
    for p in (p1, p2, p3, p4):
        print("  ", os.path.relpath(p, PROJECT))
    print("VERDICT: HARD-CORE-NOT-DERIVABLE")
    print("② Δ=%+d  ③ Δ=%+d  | combined best with r135 = %+d" % (
        door["gauge_group"]["delta"], door["mu2_sign"]["delta"],
        door["combined_best_delta_with_r135"]))
    print("guards 5/5 PASS | exit_code=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
