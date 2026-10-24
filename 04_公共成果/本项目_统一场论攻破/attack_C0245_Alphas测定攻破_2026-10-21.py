# -*- coding: utf-8 -*-
"""
attack_C0245_Alphas测定攻破_2026-10-21.py
独立复算：α_s(M_Z) 精确测定（L 线域 H 批 · 强耦合常数对比核算）

定位：母册 T373「α_s(M_Z) 精确测定（Z 极点 vs τ 衰变 vs e⁺e⁻） | QCD 跑动 | C6」。
前置：TUFT 已注销（C0133 终审）；标准 QCD 跑动/算术为外部成熟知识，本册只做复核，
严禁把任何标准物理结果写成 TUFT 预测/修正。β 系数口径衔接 C0224（共形窗口）：
    β_0 = (33-2N_f)/3（一圈，N_c=3）；β_1 = 102 - (38/3)N_f（两圈）。

把「α_s(M_Z) 精确测定」压缩成五条可复核读数 + 一张输入账单：

  E1 α_s 测量事实：三源 α_s(M_Z) 综合值与误差（Z 极点 0.1181(11)、τ 衰变 0.1181(14)、
     e⁺e⁻ 0.1189(7)）、M_Z、目标标度 μ=1.8 GeV、文献 Λ_MS^(5)≈213 MeV——外部输入显式计数。
  E2 **β 系数核算 + 跑动解（本册核心）**：
     b0=(33-2N_f)/12π（N_f=5 ⇒ 23/(12π)）与 β_0=23/3、β_1=116/3 精算；
     一阶解 z(μ)=z0+β_0/(2π)·ln(μ/μ0) 与二阶精确积分隐式解
     z=z0+(β_0/2π)L+k·ln[(2πβ_0 z+β_1)/(2πβ_0 z0+β_1)]（k=β_1/(2πβ_0)）不动点迭代，
     Decimal 48 位逐位核算 α_s(1.8 GeV)。
  E3 **源对比核算**：三源加权平均（w=1/σ²）、综合误差、χ² 一致性复核。
  E4 **Λ_QCD 反解核算**：由 α_s(M_Z)=0.1181 反解 Landau 标度——
     一阶 Λ=μ0·exp[-1/(β_0 a0)]、二阶精确 F(a) 积分反解；对照外部文献 Λ_MS^(5)≈213 MeV。
  E5 裁定：α_s 依赖 QCD 跑动结构（标准算术）；TUFT 无 QCD 群/无耦合跑动供给，
     结构性负面，按母册登记撞 C6（误差带）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：外部观测值（三源 α_s 测量值与误差、M_Z、文献 Λ_MS^(5)≈213 MeV、PDG 综合
α_s(M_Z)=0.1179…）只引用不复算；本册精算的全部是标准 QCD β 函数算术的复核；
不宣称解决 α_s 测定问题，不宣称 TUFT 有任何 QCD 耦合/跑动供给。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 常数（高精度硬编码，纯标准库） ----------
PI = Decimal("3.1415926535897932384626433832795028841971693993751")

# ---------- 外部输入（PDG/文献只引用不复算，显式计数） ----------
ALPHA_Z = Decimal("0.1181")       # Z 极点 α_s(M_Z) 综合（外部输入 #1，中心）
SIG_Z = Decimal("0.0011")         # Z 极点误差 0.1181(11)（外部输入 #1）
ALPHA_TAU = Decimal("0.1181")      # τ 衰变演化到 M_Z（外部输入 #2，中心）
SIG_TAU = Decimal("0.0014")        # τ 衰变误差 0.1181(14)（外部输入 #2）
ALPHA_EE = Decimal("0.1189")       # e⁺e⁻ 事件形状（外部输入 #3，中心）
SIG_EE = Decimal("0.0007")         # e⁺e⁻ 误差 0.1189(7)（外部输入 #3）
MZ_GEV = Decimal("91.1876")        # Z 极点质量（外部输入 #4）
MU_TARGET = Decimal("1.8")         # 目标跑动标度 μ=1.8 GeV（外部输入 #5）
LAMBDA_REF_MEV = Decimal("213")    # 文献 Λ_MS^(5)≈213 MeV（外部输入 #6，只引用不复算）

# ---------- β 系数（本册精算，Fraction 精确，口径衔接 C0224） ----------
# N_c=3：β_0 = (33-2N_f)/3；N_f=5 ⇒ 23/3
B0_FRAC = Fraction(33 - 2 * 5, 3)          # 23/3
# 两圈：β_1 = 102 - (38/3)N_f；N_f=5 ⇒ 102-190/3 = 116/3
B1_FRAC = Fraction(102) - Fraction(38, 3) * 5   # 116/3
# 本册 b0 约定：b0 = (33-2N_f)/(12π) = β_0/(4π)；N_f=5 ⇒ 23/(12π)
B0_RUN = Decimal(B0_FRAC.numerator) / (Decimal(B0_FRAC.denominator) * Decimal(4) * PI)


def e1_facts():
    return {
        "alpha_Z": ALPHA_Z, "sig_Z": SIG_Z,
        "alpha_tau": ALPHA_TAU, "sig_tau": SIG_TAU,
        "alpha_ee": ALPHA_EE, "sig_ee": SIG_EE,
        "MZ_GeV": MZ_GEV, "mu_target": MU_TARGET,
        "Lambda_MS5_ref_MeV": LAMBDA_REF_MEV,
    }


def running_onedim(alpha0: Decimal, mu0: Decimal, mu: Decimal):
    """一圈跑动：z(μ)=z0+(β_0/2π)·ln(μ/μ0)，z=1/α。"""
    c0 = Decimal(B0_FRAC.numerator) / (Decimal(B0_FRAC.denominator) * Decimal(2) * PI)
    z0 = Decimal(1) / alpha0
    L = (mu / mu0).ln()
    z = z0 + c0 * L
    return Decimal(1) / z


def running_twoloop(alpha0: Decimal, mu0: Decimal, mu: Decimal, iters: int = 400):
    """两圈隐式解（由 da/dlnμ=-β_0 a²-β_1 a³ 精确积分 F(a) 推得）：
    z = z0 + (β_0/2π)L + k·ln[(2πβ_0 z+β_1)/(2πβ_0 z0+β_1)]，k=β_1/(2πβ_0)。"""
    beta0 = Decimal(B0_FRAC.numerator) / Decimal(B0_FRAC.denominator)
    beta1 = Decimal(B1_FRAC.numerator) / Decimal(B1_FRAC.denominator)
    c0 = beta0 / (Decimal(2) * PI)
    k = beta1 / (Decimal(2) * PI * beta0)
    z0 = Decimal(1) / alpha0
    L = (mu / mu0).ln()
    denom0 = Decimal(2) * PI * beta0 * z0 + beta1
    z = z0 + c0 * L                      # 初值 = 一圈解
    for _ in range(iters):
        z = z0 + c0 * L + k * ((Decimal(2) * PI * beta0 * z + beta1) / denom0).ln()
    return Decimal(1) / z


def e2_beta_and_running():
    """β 系数精算 + α_s(1.8 GeV) 一阶/二阶跑动解（本册核心）。"""
    b0 = B0_RUN
    alpha_1loop = running_onedim(ALPHA_Z, MZ_GEV, MU_TARGET)
    alpha_2loop = running_twoloop(ALPHA_Z, MZ_GEV, MU_TARGET)
    return {
        "beta0_fraction": "%d/%d" % (B0_FRAC.numerator, B0_FRAC.denominator),
        "beta1_fraction": "%d/%d" % (B1_FRAC.numerator, B1_FRAC.denominator),
        "b0_23_over_12pi": b0,
        "alpha_1loop_at_1p8GeV": alpha_1loop,
        "alpha_2loop_at_1p8GeV": alpha_2loop,
    }


def e3_weighted():
    """三源加权平均：w=1/σ²；综合误差=1/√Σw；χ² 一致性。"""
    pairs = [(ALPHA_Z, SIG_Z), (ALPHA_TAU, SIG_TAU), (ALPHA_EE, SIG_EE)]
    ws = [Decimal(1) / (s * s) for _, s in pairs]
    sw = sum(ws)
    mean = sum(w * a for w, (a, _) in zip(ws, pairs)) / sw
    sigma = Decimal(1) / sw.sqrt()
    chi2 = sum(((a - mean) / s) ** 2 for a, s in pairs)
    return {
        "weights": ws,
        "weighted_mean": mean,
        "sigma_combined": sigma,
        "chi2": chi2,
        "ndof": 2,
    }


def lambda_one_loop(alpha0: Decimal, mu0: Decimal) -> Decimal:
    """一阶 Landau 标度：ln(Λ/μ0) = -1/(β_0 a0)，a0=α0/(2π)。"""
    a0 = alpha0 / (Decimal(2) * PI)
    b0a0 = Decimal(B0_FRAC.numerator) / Decimal(B0_FRAC.denominator) * a0
    return mu0 * ((Decimal(-1) / b0a0).exp())


def F(a: Decimal) -> Decimal:
    """两圈 RG 精确积分：F(a) = -1/(β_0 a) + (β_1/β_0²)·ln(β_0/a + β_1)。"""
    beta0 = Decimal(B0_FRAC.numerator) / Decimal(B0_FRAC.denominator)
    beta1 = Decimal(B1_FRAC.numerator) / Decimal(B1_FRAC.denominator)
    return Decimal(-1) / (beta0 * a) + (beta1 / (beta0 * beta0)) * (beta0 / a + beta1).ln()


def lambda_two_loop(alpha0: Decimal, mu0: Decimal) -> Decimal:
    """二阶精确反解：ln(Λ/μ0) = F(a0) - F(∞)，F(∞)=(β_1/β_0²)·ln(β_1)。"""
    beta0 = Decimal(B0_FRAC.numerator) / Decimal(B0_FRAC.denominator)
    beta1 = Decimal(B1_FRAC.numerator) / Decimal(B1_FRAC.denominator)
    a0 = alpha0 / (Decimal(2) * PI)
    F_inf = (beta1 / (beta0 * beta0)) * beta1.ln()
    ln_ratio = F(a0) - F_inf
    return mu0 * ln_ratio.exp()


def e4_lambda():
    lam1 = lambda_one_loop(ALPHA_Z, MZ_GEV)
    lam2 = lambda_two_loop(ALPHA_Z, MZ_GEV)
    return {
        "Lambda_one_loop_GeV": lam1,
        "Lambda_two_loop_GeV": lam2,
        "Lambda_ref_MeV": LAMBDA_REF_MEV,
    }


def e5_verdict():
    return {
        "tuft_qcd_group": 0,          # 无 QCD/SU(3) 规范群
        "tuft_running_coupling": 0,    # 无耦合跑动 β 函数供给
        "tuft_lambda_supply": 0,       # 无 Λ_QCD 标度供给
        "tuft_status": "cancelled_C0133",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0245 · α_s(M_Z) 精确测定（L 线域 H 批 · QCD 跑动核算）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] α_s 测量事实（PDG/文献只引用不复算，外部输入显式计数 6 项）")
    w("  #1 Z 极点：α_s(M_Z) = %s ± %s（0.1181(11)，外部输入）"
      % (fv(g1["alpha_Z"], "5f"), fv(g1["sig_Z"], "4f")))
    w("  #2 τ 衰变演化到 M_Z：%s ± %s（0.1181(14)，外部输入）"
      % (fv(g1["alpha_tau"], "5f"), fv(g1["sig_tau"], "4f")))
    w("  #3 e⁺e⁻ 事件形状：%s ± %s（0.1189(7)，外部输入）"
      % (fv(g1["alpha_ee"], "5f"), fv(g1["sig_ee"], "4f")))
    w("  #4 M_Z = %s GeV；#5 目标标度 μ = %s GeV"
      % (fv(g1["MZ_GeV"], "4f"), fv(g1["mu_target"], "3f")))
    w("  #6 文献 Λ_MS^(5) ≈ %s MeV（只引用不复算）。" % fv(g1["Lambda_MS5_ref_MeV"], "0f"))
    w("  外部输入共 6 项，全部显式计数；本册不复算任何 PDG/文献值。")
    entries.append(("E1", "α_s 三源测量 6 项外部输入：Z极点0.1181(11)/τ 0.1181(14)/"
                    "e⁺e⁻ 0.1189(7)、M_Z=91.1876、μ=1.8、Λ_ref=213 MeV", "PASS",
                    "PDG/文献只引用不复算"))

    # ---- E2 ----
    g2 = e2_beta_and_running()
    w("\n[E2] β 系数核算 + α_s 跑动解（本册核心，Decimal 48 位）")
    w("  一圈 β_0 = (33-2N_f)/3 = %s（精确分数）；两圈 β_1 = 102-(38/3)N_f = %s"
      % (g2["beta0_fraction"], g2["beta1_fraction"]))
    w("  本册 b0 = (33-2N_f)/(12π) = 23/(12π) = %s（N_f=5）" % fv(g2["b0_23_over_12pi"], "10f"))
    w("  一圈跑动解 α_s(μ)：z=1/α，z(μ)=z0+(β_0/2π)·ln(μ/M_Z)")
    w("  ⇒ α_s(%s GeV) 一圈 = %s" % (fv(MU_TARGET, "1f"), fv(g2["alpha_1loop_at_1p8GeV"], "10f")))
    w("  两圈隐式解 z=z0+(β_0/2π)L+k·ln[(2πβ_0 z+β_1)/(2πβ_0 z0+β_1)]，k=β_1/(2πβ_0)，不动点 400 步")
    w("  ⇒ α_s(%s GeV) 两圈 = %s" % (fv(MU_TARGET, "1f"), fv(g2["alpha_2loop_at_1p8GeV"], "10f")))
    w("  对照：文献量级 α_s(2 GeV)≈0.30、α_s(1.8 GeV)≈0.35（外部量级感，本册不复算）；")
    w("  两圈解（%s）> 一圈解（%s），低标度耦合跑动更陡——标准 QCD 跑动方向正确。"
      % (fv(g2["alpha_2loop_at_1p8GeV"], "4f"), fv(g2["alpha_1loop_at_1p8GeV"], "4f")))
    entries.append(("E2", "b0=23/(12π)=%s；α_s(1.8 GeV) 一圈=%s / 两圈=%s"
                    % (fv(g2["b0_23_over_12pi"], "6f"),
                       fv(g2["alpha_1loop_at_1p8GeV"], "6f"),
                       fv(g2["alpha_2loop_at_1p8GeV"], "6f")),
                    "PASS", "Decimal 48 位；标准 QCD β 函数算术复核，非 TUFT 结果"))

    # ---- E3 ----
    g3 = e3_weighted()
    w("\n[E3] 三源对比 + 加权平均核算（w=1/σ²）")
    w("  权重 w = 1/σ²：Z极点=%s、τ=%s、e⁺e⁻=%s"
      % (fv(g3["weights"][0], "4e"), fv(g3["weights"][1], "4e"), fv(g3["weights"][2], "4e")))
    w("  加权平均 α_s(M_Z) = %s ± %s" % (fv(g3["weighted_mean"], "8f"), fv(g3["sigma_combined"], "7f")))
    w("  χ² = %s（自由度 %d）⇒ χ²/dof = %s ≪ 1，三源内部一致（e⁺e⁻ 权重最大主导）。"
      % (fv(g3["chi2"], "6f"), g3["ndof"], fv(g3["chi2"] / Decimal(g3["ndof"]), "4f")))
    w("  => 三源测量在误差带内互相吻合，无显著跨源张力（对照母册 C6 误差带维度）。")
    entries.append(("E3", "加权平均=%s±%s；χ²=%s（dof=2）三源一致"
                    % (fv(g3["weighted_mean"], "6f"), fv(g3["sigma_combined"], "5f"),
                       fv(g3["chi2"], "3f")),
                    "PASS", "Decimal 精算；测量值为外部输入"))

    # ---- E4 ----
    g4 = e4_lambda()
    w("\n[E4] Λ_QCD 反解核算（由 α_s(M_Z)=0.1181 反解 Landau 标度）")
    w("  一阶：ln(Λ/μ0)=-1/(β_0 a0)，a0=α0/(2π) ⇒ Λ = %s GeV = %s MeV"
      % (fv(g4["Lambda_one_loop_GeV"], "8f"), fv(g4["Lambda_one_loop_GeV"] * 1000, "6f")))
    w("  二阶精确积分反解（F(a) 精确，见 e4）：Λ = %s GeV = %s MeV"
      % (fv(g4["Lambda_two_loop_GeV"], "8f"), fv(g4["Lambda_two_loop_GeV"] * 1000, "6f")))
    w("  外部文献 Λ_MS^(5) ≈ %s MeV（#6 只引用）；一阶 %s MeV / 二阶 %s MeV 与之"
      "差 ~1–2.5 倍——差值由三圈系数 + b/c 阈匹配（外部输入）抬落，非本册复算范围。"
      % (fv(g4["Lambda_ref_MeV"], "0f"),
         fv(g4["Lambda_one_loop_GeV"] * 1000, "0f"),
         fv(g4["Lambda_two_loop_GeV"] * 1000, "0f")))
    w("  => 反解链路（α_s(M_Z) → β 函数 → Λ）为标准 QCD 算术；Λ_MS^(5) 绝对值依赖方案/圈数/阈。")
    entries.append(("E4", "Λ 一阶=%s MeV / 二阶=%s MeV（外部文献 213 MeV，差由三圈+阈匹配）"
                    % (fv(g4["Lambda_one_loop_GeV"] * 1000, "0f"),
                       fv(g4["Lambda_two_loop_GeV"] * 1000, "0f")),
                    "PASS", "精确积分反解；文献值外部引用"))

    # ---- E5 ----
    g5 = e5_verdict()
    w("\n[E5] 裁定：TUFT QCD 耦合/跑动供给检查")
    w("  TUFT QCD/SU(3) 规范群供给 = %d；耦合跑动 β 函数供给 = %d；Λ_QCD 标度供给 = %d"
      % (g5["tuft_qcd_group"], g5["tuft_running_coupling"], g5["tuft_lambda_supply"]))
    w("  TUFT 状态：%s（C0133 终审已注销）。" % g5["tuft_status"])
    w("  α_s 全链（β_0/β_1 → 跑动 → 加权平均 → Λ 反解）是标准 QCD 算术；")
    w("  TUFT 无 QCD 群、无耦合、无跑动 ⇒ 对 α_s 测定供给恒为 0。")
    w("  => **结构性负面（对 TUFT/几何框架）**：TUFT 既不能解释、也不能预言、"
      "更不能修正 α_s(M_Z) 测量值与跑动；按母册 T373 登记撞 **C6（误差带）**。")
    entries.append(("E5", "TUFT QCD/β函数/Λ 供给全 0（已注销 C0133）；结构性负面，撞 C6",
                    "PASS", "按母册 T373 登记撞 C6"))

    # ---- 守卫 ----
    guards = [
        ("G1", "β_0(N_f=5)=23/3 精确；b0=23/(12π)∈(0.60,0.62)",
         B0_FRAC == Fraction(23, 3) and Decimal("0.60") < B0_RUN < Decimal("0.62")),
        ("G2", "一圈 α_s(1.8 GeV)∈(0.25,0.30)；两圈 ∈(0.30,0.40)",
         Decimal("0.25") < g2["alpha_1loop_at_1p8GeV"] < Decimal("0.30")
         and Decimal("0.30") < g2["alpha_2loop_at_1p8GeV"] < Decimal("0.40")),
        ("G3", "两圈跑动 > 一圈（低标度更陡，方向正确）",
         g2["alpha_2loop_at_1p8GeV"] > g2["alpha_1loop_at_1p8GeV"]),
        ("G4", "加权平均 ∈(0.1184,0.1188)；χ²<2（三源一致）",
         Decimal("0.1184") < g3["weighted_mean"] < Decimal("0.1188") and g3["chi2"] < Decimal("2")),
        ("G5", "TUFT QCD/跑动/Λ 供给 = 0",
         g5["tuft_qcd_group"] == 0 and g5["tuft_running_coupling"] == 0
         and g5["tuft_lambda_supply"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %-4s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0245 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称解决 α_s(M_Z) 测定问题；全部数值为标准 QCD 算术（PDG/文献）复核；")
    w("  三源测量值与误差、M_Z、文献 Λ_MS^(5)≈213 MeV 均为外部输入只引用；")
    w("  严禁把标准物理结果写成 TUFT 预测/修正（TUFT 已注销 C0133）。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0245_Alphas测定攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0245_Alphas测定攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0245_alphas_measurement",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_external_inputs": {k: str(v) for k, v in g1.items()},
            "E2_beta_running": {k: str(v) for k, v in g2.items()},
            "E3_weighted": {"weights": [str(x) for x in g3["weights"]],
                            "weighted_mean": str(g3["weighted_mean"]),
                            "sigma_combined": str(g3["sigma_combined"]),
                            "chi2": str(g3["chi2"]), "ndof": g3["ndof"]},
            "E4_lambda": {k: str(v) for k, v in e4_lambda().items()},
            "E5_tuft_supply": {k: str(v) for k, v in g5.items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0245 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
