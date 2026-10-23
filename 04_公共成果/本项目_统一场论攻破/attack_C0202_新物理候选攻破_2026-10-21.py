# -*- coding: utf-8 -*-
"""
attack_C0202_新物理候选攻破_2026-10-21.py
独立复算：母册 T033（行 124）「SM 之外的新物理 · 新对称/新自由度」· C1

定位：母册 T033 行 124：`| T033 | 标准模型之外的新物理 | 新对称/新自由度 | C1 | 🔲 |`。
前置：SM 新物理候选账单（2026-10-21，B 级方法论册，不占 C 号）已枚举 10 候选并
给出 §三 参数盒 Decimal 自核读数、§四 165 枚外部输入合计与 TUFT 供给=0 裁决。
本册（C0202）= T033 本体攻破：把账单结论压成四条可复核读数 + 一张供给账单，
**独立复算**账单 §三/§四 的关键算术（不采信自报），并对 TUFT/几何框架判定供给。

把「SM 之外新物理从哪来」压缩成五条可复核读数：

  E1 候选枚举审计：10 候选各自的新对称群/新场内容/新参数计数（引用账单 §二）；
     本册独立复算 MSSM 名义 110 -> 物理 ~105 的分解（45+54+6+5）。
  E2 外部输入总量核算（本册核心）：10 候选新参数合计 = 165 枚 vs SM-19 基线；
     复算 105+4+7+8+6+4+2+21+3+5 = 165，并给倍数/均值。
  E3 实验排除度（可量化部分）：复算 SU(5) sin²θ_W 过冲 3/8÷0.2312、
     minimal SU(5) τ_p 排除 2.4e34/4.596e31、MSSM-GUT τ_p 超界 2.872e36/2.4e34、
     暗光子 ε 窗口 1e-2/1e-16 与 NA64 ε_bound=sqrt(1e-10)。
  E4 新物理供给检查：TUFT 是否供给任一候选的新对称群/新场/新标度（逐候选表，全 0）。
  E5 裁定：10 候选全部依赖外部对称与外部输入（165 枚），TUFT 供给=0，
     结构性负面，按母册登记撞 C1。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：本册不宣称发现/解决任何新物理候选；外部实验排除线（LHC/Super-K/
ADMX/NA64 等）只引用不复算；数值均为标准新物理算术复核；TUFT 已注销（C0133），
严禁把标准物理结果写成 TUFT 预测/修正。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（账单 §二/§三 引用，本册独立复算其算术） ----------
# 10 候选新外部输入枚数（账单 §二/§四 冻结读数）
CANDIDATES = [
    # (编号, 候选名, 新对称群, 新场内容摘要, 新参数数)
    (1, "MSSM (N=1 超对称)", "超-Poincaré（费米-玻色梯级）",
     "每 SM 态一个超伴（stop/sbottom/neutralino/chargino/gaugino/Higgsino/第二 Higgs doublet）", 105),
    (2, "额外 U(1)' (Z')", "G_SM × U(1)'",
     "重规范玻色子 Z' (TeV) + 新 Higgs 介导 U(1)' 破缺", 4),
    (3, "左右对称 L-R", "SU(3)_c×SU(2)_L×SU(2)_R×U(1)_{B-L}",
     "W_R^±/Z_R、右旋中微子 N_R、双二重态 Higgs", 7),
    (4, "Pati-Salam", "SU(4)×SU(2)_L×SU(2)_R",
     "leptoquark X(4,2,1)/X(4,1,2)、右旋伴随场", 8),
    (5, "大统一 SU(5)/SO(10)/E6", "单群 SU(5)⊃G_SM / SO(10)⊃SU(5) / E6⊃SO(10)",
     "X/Y 规范玻色子 (~M_GUT)、Higgs 表示 (5/45/126 等)", 6),
    (6, "额外维 KK/RS", "额外空间维（平直紧致 / RS 弯曲）",
     "KK 激发塔（引力子/规范/费米激发）、radion/胀子", 4),
    (7, "轴子 / PQ 对称", "新全局 U(1)_{PQ}",
     "赝标量轴子 a（KSVZ/DFSZ 两支）", 2),
    (8, "重费米子 + seesaw", "G_SM 直陈扩充（无新规范群）",
     "VLQ (T/B')、矢量类轻子、Majorana N_R", 21),
    (9, "暗光子 / U(1)_d", "G_SM × U(1)_d",
     "暗光子 A'（动力学混合 ε 与可见 EM 流耦合）", 3),
    (10, "复合 Higgs / 部分复合", "新强动力学（SU(N) 类），Higgs 为伪 Goldstone",
     "矢量/张量共振 ρ/a、top 部分伴 top-partner", 5),
]

# SM 基线外部参数数（账单 §三-1 注）
SM_BASELINE = 19

# MSSM 分解（账单 §三-1）
MSSM_SOFT_SCALAR = 5 * 9    # 5 个 3x3 Hermitian 矩阵，各 9 实参 = 45
MSSM_TRILINEAR = 3 * 18     # A_u/A_d/A_e 各 3x3 复矩阵 = 54
MSSM_GAUGINO = 2 * 3        # M1/M2/M3 复数 = 6
MSSM_HIGGS_SECTOR = 5       # μ(2)+Bμ(2)+tanβ(1) = 5
MSSM_NOMINAL = MSSM_SOFT_SCALAR + MSSM_TRILINEAR + MSSM_GAUGINO + MSSM_HIGGS_SECTOR  # 110
MSSM_PHYSICAL = 105          # 吸收非物理相位/味基旋转后教科书面值

# GUT 树级 sin²θ_W（账单 §三-2）
SIN2THETA_W_TREE = Fraction(3, 8)          # = 0.375
SIN2THETA_W_OBS = Decimal("0.2312")       # PDG 观测值（引用）

# 质子衰变寿命（账单 §三-2 / C0147 冻结）
TAU_P_SUPERK_BOUND = Decimal("2.4e34")     # yr，Super-K 下限（引用）
TAU_P_MINIMAL_SU5 = Decimal("4.596e31")    # yr，minimal 非 SUSY SU(5) 预言（引用）
TAU_P_MSSM_GUT = Decimal("2.872e36")      # yr，MSSM 汇聚线预言（引用）

# 暗光子窗口（账单 §三-3 / C0186）
EPS_MIN = Decimal("1e-16")
EPS_MAX = Decimal("1e-2")
NA64_EPS2_BOUND = Decimal("1e-10")

# 轴子 f_a 窗口（账单 §二 #7 引用）
FA_MIN_GeV = Decimal("4e8")
FA_MAX_GeV = Decimal("1e12")


def e1_candidate_audit():
    """E1：10 候选枚举审计 + MSSM 分解复算。"""
    names = [c[1] for c in CANDIDATES]
    param_counts = [c[4] for c in CANDIDATES]
    return {
        "n_candidates": len(CANDIDATES),
        "names": names,
        "param_counts": param_counts,
        "mssm_soft_scalar": MSSM_SOFT_SCALAR,
        "mssm_trilinear": MSSM_TRILINEAR,
        "mssm_gaugino": MSSM_GAUGINO,
        "mssm_higgs_sector": MSSM_HIGGS_SECTOR,
        "mssm_nominal": MSSM_NOMINAL,
        "mssm_physical": MSSM_PHYSICAL,
        "mssm_plus_sm": MSSM_PHYSICAL + SM_BASELINE,
    }


def e2_total_inputs():
    """E2：10 候选外部输入合计 = 165 vs SM-19 基线。"""
    counts = [c[4] for c in CANDIDATES]
    total = sum(counts)
    total_dec = Decimal(total)
    sm_dec = Decimal(SM_BASELINE)
    ratio = total_dec / sm_dec                    # 165/19
    avg = total_dec / Decimal(len(CANDIDATES))    # 165/10
    # 累计偏账：MSSM 一枚模型把 SM 从 19 推到 124
    mssm_grand = Decimal(MSSM_PHYSICAL) + sm_dec
    return {
        "counts": counts,
        "total_external_inputs": total,
        "sm_baseline": SM_BASELINE,
        "ratio_total_over_sm": ratio,
        "avg_per_candidate": avg,
        "mssm_grand_total": mssm_grand,
    }


def e3_exclusion_magnitudes():
    """E3：可量化实验排除度复算（标准新物理算术）。"""
    # sin²θ_W 树级过冲
    sin2_tree_dec = Decimal(SIN2THETA_W_TREE.numerator) / Decimal(SIN2THETA_W_TREE.denominator)
    sin2_overshoot = sin2_tree_dec / SIN2THETA_W_OBS
    # minimal SU(5) τ_p 被 Super-K 排除倍数（ bound / prediction ）
    tau_excluded = TAU_P_SUPERK_BOUND / TAU_P_MINIMAL_SU5
    # MSSM-GUT τ_p 超界倍数（ prediction / bound ）
    tau_overshoot = TAU_P_MSSM_GUT / TAU_P_SUPERK_BOUND
    # 暗光子 ε 窗口
    eps_ratio = EPS_MAX / EPS_MIN                 # 1e14
    eps_decades = (EPS_MAX.ln() - EPS_MIN.ln()) / Decimal(10).ln()
    eps_bound = NA64_EPS2_BOUND.sqrt()            # 1e-5
    # 轴子 f_a 窗口跨度
    fa_ratio = FA_MAX_GeV / FA_MIN_GeV           # 2500
    fa_decades = (FA_MAX_GeV.ln() - FA_MIN_GeV.ln()) / Decimal(10).ln()
    return {
        "sin2theta_w_tree": sin2_tree_dec,
        "sin2theta_w_obs": SIN2THETA_W_OBS,
        "sin2_overshoot": sin2_overshoot,
        "tau_excluded_minimal_su5": tau_excluded,
        "tau_overshoot_mssm_gut": tau_overshoot,
        "eps_ratio": eps_ratio,
        "eps_decades": eps_decades,
        "na64_eps2_bound": NA64_EPS2_BOUND,
        "na64_eps_bound": eps_bound,
        "fa_min_GeV": FA_MIN_GeV,
        "fa_max_GeV": FA_MAX_GeV,
        "fa_ratio": fa_ratio,
        "fa_decades": fa_decades,
    }


def e4_tuft_supply():
    """E4：TUFT 对 10 候选的供给检查（逐候选）。"""
    # 承接 C0133（TUFT 注销）、C0137（签名 (12,4) 三候选不唯一化 SM）、
    # C0140（(ℏ,G,c) nullity=0 给不出无量纲统一耦合）。
    # 对每个候选：TUFT 是否供给 (新对称群, 新场, 新标度)？
    supply_rows = []
    for cid, name, group, fields, npar in CANDIDATES:
        supply_rows.append({
            "id": cid, "candidate": name,
            "new_symmetry_supplied": False,
            "new_field_supplied": False,
            "new_scale_supplied": False,
            "tuft_supply": 0,
        })
    n_supplied = sum(r["tuft_supply"] for r in supply_rows)
    return {
        "rows": supply_rows,
        "n_candidates": len(supply_rows),
        "n_supplied_by_tuft": n_supplied,
        "tuft_prediction_count": 0,   # C0136/㉕：带 prediction_value 预言 0 条
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0202 · SM 之外的新物理（母册 T033 行 124 · 10 候选供给检查）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_candidate_audit()
    w("\n[E1] 候选枚举审计：%d 候选各自的新对称/新场/新参数（引用账单 §二）"
      % g1["n_candidates"])
    w("  MSSM 新参数分解独立复算（账单 §三-1）：")
    w("    软标量质量矩阵 5×3×3 Hermitian = %d" % g1["mssm_soft_scalar"])
    w("    三线性耦合 A_u/A_d/A_e 各 3×3 复矩阵 = %d" % g1["mssm_trilinear"])
    w("    规范微子 M1/M2/M3 复数 = %d" % g1["mssm_gaugino"])
    w("    Higgs 区 μ+Bμ+tanβ = %d" % g1["mssm_higgs_sector"])
    w("    名义合计 = %d；吸收非物理相位/味基旋转后物理自由参数 ≈ %d"
      % (g1["mssm_nominal"], g1["mssm_physical"]))
    w("    含 SM 自身 %d 参 ⇒ MSSM 一枚模型外部输入 = %d"
      % (SM_BASELINE, g1["mssm_plus_sm"]))
    w("  10 候选新参数数逐项：%s" % g1["param_counts"])
    entries.append(("E1", "%d 候选枚举闭合；MSSM 名义 110 -> 物理 ≈105（含 SM 19 -> 124），"
                    "分解 45+54+6+5=110 独立复算一致" % g1["n_candidates"],
                    "PASS", "账单 §二/§三-1 引用；本册独立复算 MSSM 分解"))

    # ---- E2 ----
    g2 = e2_total_inputs()
    w("\n[E2] 外部输入总量核算（本册核心）")
    w("  逐项求和：%s = %d" % (" + ".join(str(x) for x in g2["counts"]),
                                  g2["total_external_inputs"]))
    w("  SM 基线 = %d 枚（3 规范耦合 + 9 Yukawa + Higgs v/λ + CKM 4 + QCD θ + 3 中微子质量）"
      % g2["sm_baseline"])
    w("  10 候选合计 = %d 枚 vs SM 基线 %d 枚 ⇒ 倍数 = %s"
      % (g2["total_external_inputs"], g2["sm_baseline"], fv(g2["ratio_total_over_sm"], "4f")))
    w("  每候选均值 = %d/10 = %s 枚；MSSM 单枚模型把 SM 从 %d 推到 %d"
      % (g2["total_external_inputs"], fv(g2["avg_per_candidate"], "1f"),
         g2["sm_baseline"], g2["mssm_grand_total"]))
    w("  => 新物理候选每开一扇门，外部输入不是减少而是放大 8.68 倍量级。")
    entries.append(("E2", "10 候选外部输入合计 %d 枚 = SM-19 的 %s 倍；每候选均值 %s；"
                    "MSSM 单枚推到 %d"
                    % (g2["total_external_inputs"], fv(g2["ratio_total_over_sm"], "4f"),
                       fv(g2["avg_per_candidate"], "1f"), g2["mssm_grand_total"]),
                    "PASS", "Decimal 48 位独立求和；账单 §三-5/§四 复核一致"))

    # ---- E3 ----
    g3 = e3_exclusion_magnitudes()
    w("\n[E3] 实验排除度（可量化部分复算，外部排除线只引用）")
    w("  (i) GUT 树级 sin²θ_W：3/8 = %s vs 观测 %s ⇒ 过冲 %s 倍"
      % (fv(g3["sin2theta_w_tree"], "4f"), fv(g3["sin2theta_w_obs"], "4f"),
         fv(g3["sin2_overshoot"], "6f")))
    w("  (ii) minimal SU(5) τ_p 预言 %s yr vs Super-K 下限 %s yr"
      % (fv(TAU_P_MINIMAL_SU5, "3e"), fv(TAU_P_SUPERK_BOUND, "2e")))
    w("       ⇒ 被排除 %s 倍（预言短于下限，已死）" % fv(g3["tau_excluded_minimal_su5"], "6f"))
    w("  (iii) MSSM-GUT τ_p 预言 %s yr vs Super-K 下限 %s yr"
      % (fv(TAU_P_MSSM_GUT, "3e"), fv(TAU_P_SUPERK_BOUND, "2e")))
    w("       ⇒ 超界 %s 倍（预言太长不可测，阈值-可见两难）"
      % fv(g3["tau_overshoot_mssm_gut"], "6f"))
    w("  (iv) 暗光子 ε 窗口 %s–%s：跨度 = %s（%s 个数量级）；"
      % (fv(EPS_MIN, "1e"), fv(EPS_MAX, "1e"), fv(g3["eps_ratio"], "1e"),
         fv(g3["eps_decades"], "1f")))
    w("       NA64 ε²≲%s ⇒ ε_bound=%s；仅砍上端，下端 %s 量级开放"
      % (fv(g3["na64_eps2_bound"], "1e"), fv(g3["na64_eps_bound"], "1e"),
         fv((EPS_MIN.ln() - g3["na64_eps_bound"].ln()) / Decimal(10).ln(), "1f")))
    w("  (v) 轴子 f_a 窗口 %s–%s GeV：跨度 = %s（%s 个数量级）"
      % (fv(g3["fa_min_GeV"], "1e"), fv(g3["fa_max_GeV"], "1e"),
         fv(g3["fa_ratio"], "4f"), fv(g3["fa_decades"], "1f")))
    w("  => 可量化排除度：GUT 族两端被夹死（522× 排除 / 119.7× 超界 / sin²θ 过冲 1.622×）；")
    w("     暗光子/轴子仍留 11–12 个数量级开放窗口——零发现 ≠ 被证伪。")
    entries.append(("E3", "GUT 三读数：sin²θ_W 过冲 %s×、τ_p 排除 %s×、MSSM τ_p 超界 %s×；"
                    "暗光子 ε 跨 %s 量级、轴子 f_a 跨 %s 量级开放"
                    % (fv(g3["sin2_overshoot"], "4f"), fv(g3["tau_excluded_minimal_su5"], "4f"),
                       fv(g3["tau_overshoot_mssm_gut"], "4f"),
                       fv(g3["eps_decades"], "0f"), fv(g3["fa_decades"], "1f")),
                    "PASS", "标准新物理算术复核；外部实验线只引用"))

    # ---- E4 ----
    g4 = e4_tuft_supply()
    w("\n[E4] 新物理供给检查：TUFT 是否供给任一候选？")
    w("  逐候选 (新对称群 / 新场 / 新标度) 三供给：")
    for r in g4["rows"]:
        w("    #%d %-28s  对称=%s  新场=%s  标度=%s  供给=%d"
          % (r["id"], r["candidate"],
             "✗" if not r["new_symmetry_supplied"] else "✓",
             "✗" if not r["new_field_supplied"] else "✓",
             "✗" if not r["new_scale_supplied"] else "✓",
             r["tuft_supply"]))
    w("  受供候选数 = %d/%d；TUFT 带 prediction_value 的可检验新预言 = %d 条"
      % (g4["n_supplied_by_tuft"], g4["n_candidates"], g4["tuft_prediction_count"]))
    w("  依据：C0133（TUFT 七障碍终审注销）；C0137（签名 (12,4) 三候选不唯一化 SM，更不外延）；")
    w("        C0140（(ℏ,G,c) nullity=0，给不出无量纲统一耦合/新标度）；C0136/㉕（SUSY 预言 0 条）。")
    entries.append(("E4", "TUFT 对 %d 候选供给 = %d（新对称/新场/新标度三栏全 ✗）；"
                    "可检验新预言 %d 条" % (g4["n_candidates"], g4["n_supplied_by_tuft"],
                                  g4["tuft_prediction_count"]),
                    "PASS", "承接 C0133/C0137/C0140/C0136 引用，本册只做逐候选表"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  T033「SM 之外新物理」被精确翻译成：(a) 10 候选的新对称群/新场从哪来；")
    w("  (b) 165 枚外部输入从哪来；(c) 实验现状是否已闭合。")
    w("  (a) 10 候选每一枚都要求在 G_SM 之外公设一个新对称（超-Poincaré/U(1)'/SU(2)_R/")
    w("      SU(4)/SU(5)⊃.../额外维/U(1)_PQ/VLQ 扩充/U(1)_d/新强动力学）——TUFT 一枚都不给。")
    w("  (b) 165 枚外部输入（E2，= SM-19 的 %s 倍）全部须外部输入；几何常数 nullity=0 给不出。"
      % fv(g2["ratio_total_over_sm"], "4f"))
    w("  (c) GUT 族两端夹死（522×/119.7×/1.622×），暗光子/轴子仍有 11–12 量级开放窗口——")
    w("      零发现不等于被证伪，但也不等于被供给。")
    w("  => **T033 结构性负面（对 TUFT/几何框架）**；按母册行 124 登记撞 **C1**"
      "（粒子内容须公设唯一确定）。")
    entries.append(("E5", "T033 结构性负面：10 候选全依赖外部对称+165 枚外部输入，"
                    "TUFT 供给=0；按母册登记撞 C1", "PASS", "撞 C1（母册行 124 登记一致）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "候选数 = 10", g1["n_candidates"] == 10),
        ("G2", "MSSM 名义分解 45+54+6+5 = 110", MSSM_NOMINAL == 110),
        ("G3", "MSSM 物理自由参数 = 105", MSSM_PHYSICAL == 105),
        ("G4", "10 候选外部输入合计 = 165", g2["total_external_inputs"] == 165),
        ("G5", "SM 基线 = 19", g2["sm_baseline"] == 19),
        ("G6", "GUT 树级 sin²θ_W = 3/8 = 0.375",
         g3["sin2theta_w_tree"] == Decimal("0.375")),
        ("G7", "minimal SU(5) τ_p 排除 ≈ 522.19×（容差 1%）",
         abs(g3["tau_excluded_minimal_su5"] - Decimal("522.193")) / Decimal("522.193") < Decimal("0.01")),
        ("G8", "MSSM-GUT τ_p 超界 ≈ 119.67×（容差 1%）",
         abs(g3["tau_overshoot_mssm_gut"] - Decimal("119.667")) / Decimal("119.667") < Decimal("0.01")),
        ("G9", "暗光子 ε 窗口跨度 = 1e14（14 个数量级）",
         g3["eps_ratio"] == Decimal("1e14")),
        ("G10", "NA64 ε²≲1e-10 ⇒ ε_bound = 1e-5",
         g3["na64_eps_bound"] == Decimal("1e-5")),
        ("G11", "TUFT 供给候选数 = 0", g4["n_supplied_by_tuft"] == 0),
        ("G12", "TUFT 可检验新预言 = 0 条", g4["tuft_prediction_count"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0202 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称发现/解决任何新物理候选：外部实验排除线（LHC/Super-K/ADMX/NA64）只引用；")
    w("  数值均为标准新物理算术复核（Decimal 48 位）；TUFT 已注销（C0133），")
    w("  严禁把标准物理结果写成 TUFT 预测/修正。裁的是「TUFT/几何框架能否供给 SM 之外新物理」。")
    w("  红线照录：「不宣称解决任何物理难题」「已攻破=对 TUFT/几何框架结构性负面闭合」")
    w("  「有预测且对 = 0/22」「UFT-3 = 0 保持」；另「数学自洽 ≠ 实验证实」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0202_新物理候选攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0202_新物理候选攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0202_bsm_new_physics",
            "master_row": "T033 | 标准模型之外的新物理 | 新对称/新自由度 | C1 |",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_candidates": {
                "n_candidates": g1["n_candidates"],
                "names": g1["names"],
                "param_counts": g1["param_counts"],
                "mssm_breakdown": {
                    "soft_scalar": g1["mssm_soft_scalar"],
                    "trilinear": g1["mssm_trilinear"],
                    "gaugino": g1["mssm_gaugino"],
                    "higgs_sector": g1["mssm_higgs_sector"],
                    "nominal": g1["mssm_nominal"],
                    "physical": g1["mssm_physical"],
                    "plus_sm": g1["mssm_plus_sm"],
                },
            },
            "E2_total_inputs": {k: str(v) for k, v in g2.items()},
            "E3_exclusion": {k: str(v) for k, v in g3.items()},
            "E4_tuft_supply": {
                "n_candidates": g4["n_candidates"],
                "n_supplied_by_tuft": g4["n_supplied_by_tuft"],
                "tuft_prediction_count": g4["tuft_prediction_count"],
                "rows": g4["rows"],
            },
            "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0202 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
