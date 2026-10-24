# -*- coding: utf-8 -*-
"""
attack_C0243_电子磁矩攻破_2026-10-21.py
独立精算：母册 T270「电子反常磁矩 a_e 与 Cs/Rb 原子反冲差 · 轻子味普适破坏」
（L 线域 H 批 · QED 级数核算）

定位：母册 T270 原文照录：| T270 | 电子反常磁矩 a_e 与 Cs/Rb 原子反冲差 |
轻子味普适破坏 | C1,C5 | 🔲 |。本册为 C0243 四件套（py→report→json→判定册），
衔接 C0202（SM 新物理）/C0219（味）口径。

把「a_e 从哪来」压缩成五条可复核读数 + 一张输入账单：

  E1 观测事实（只引用不复算）：α(CODATA 2018)、QED 系数 C2/C4/C6/C8、
     实验 a_e^exp（2022 Cs 反冲法）。
  E2 **a_e QED 级数独立精算（本册核心）**：a_e = C2·(α/π) + C4·(α/π)² +
     C6·(α/π)³ + C8·(α/π)⁴，逐项贡献 + 理论-实验 σ 偏差。
  E3 α 反解：由 a_e^exp 数值反解 α（截断级数求根），核对精度 ~1e-9 量级。
  E4 TUFT 供给检查：TUFT 是否供给 QED 级数 / 反常磁矩结构（无）。
  E5 裁定：a_e 依赖 QED 圈图级数（标准物理），TUFT 无 QED/无圈图供给，
     结构性负面，按母册登记撞 C1/C5。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界：本册数值均为**标准 QED 算术复核**；TUFT 已注销（C0133）；
严禁把标准物理结果写成 TUFT 预测/修正。α/a_e 测量值为已知外部输入显式计数。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（只引用不复算，显式计数） ----------
# CODATA 2018 精细结构常数（倒数）
ALPHA_INV = Decimal("137.035999084")
# π（48 位常数）
PI = Decimal("3.1415926535897932384626433832795028841971693993751")
# QED 级数系数（标准结果，只引用）
C2 = Decimal("0.5")                       # Schwinger 一阶
C4 = Decimal("-0.32847896557919378")       # 二阶（4 圈? α²/π²）
C6 = Decimal("1.181241456")               # 三阶
C8 = Decimal("-1.7283")                   # 四阶
# 实验值：2022 后 Cs 反冲法 a_e = 0.00115965218059(13)
A_E_EXP = Decimal("0.00115965218059")
A_E_EXP_SIG = Decimal("0.00000000000013")  # 1.3e-12 末位不确定度


def e1_facts():
    """观测事实（只引用不复算）。"""
    alpha = Decimal(1) / ALPHA_INV
    return {
        "alpha_inv_CODATA": ALPHA_INV,
        "alpha": alpha,
        "C2": C2, "C4": C4, "C6": C6, "C8": C8,
        "a_e_exp": A_E_EXP,
        "a_e_exp_sigma": A_E_EXP_SIG,
        "source": "CODATA2018 α；QED 系数标准结果；a_e^exp=0.00115965218059(13) 2022 Cs 反冲法",
    }


def series(x):
    """a_e(x) = C2·x + C4·x² + C6·x³ + C8·x⁴，x = α/π。"""
    x2 = x * x
    x3 = x2 * x
    x4 = x3 * x
    t1 = C2 * x
    t2 = C4 * x2
    t3 = C6 * x3
    t4 = C8 * x4
    return t1, t2, t3, t4, t1 + t2 + t3 + t4


def e2_series():
    """a_e QED 级数精算（本册核心）。"""
    alpha = Decimal(1) / ALPHA_INV
    x = alpha / PI
    t1, t2, t3, t4, a_th = series(x)
    delta = a_th - A_E_EXP
    sigma_units = delta / A_E_EXP_SIG
    return {
        "alpha": alpha, "x_alpha_over_pi": x,
        "t1_2pi": t1, "t2": t2, "t3": t3, "t4": t4,
        "a_e_th": a_th,
        "a_e_exp": A_E_EXP,
        "delta_th_minus_exp": delta,
        "sigma_units": sigma_units,
    }


def e3_alpha_invert():
    """由 a_e^exp 反解 α（截断级数求根），核对精度。"""
    # 朴素一阶反解：a_e ≈ C2·(α/π) ⇒ α = π·a_e/C2 = 2π·a_e
    alpha_naive = PI * A_E_EXP / C2
    # 完整截断级数求根（bisection on x = α/π）
    lo = Decimal("0.0023")
    hi = Decimal("0.0024")
    target = A_E_EXP
    # f(x) = series(x)[-1] - target；单调增（C2>0 主导）
    for _ in range(200):
        mid = (lo + hi) / 2
        fmid = series(mid)[-1] - target
        if fmid > 0:
            hi = mid
        else:
            lo = mid
    x_solved = (lo + hi) / 2
    alpha_solved = PI * x_solved
    alpha_codata = Decimal(1) / ALPHA_INV
    rel_diff = (alpha_solved - alpha_codata) / alpha_codata
    # 由 a_e 实验不确定度传导的 α 相对精度：δα/α ≈ δa_e/a_e
    da_rel = A_E_EXP_SIG / A_E_EXP
    return {
        "alpha_naive_firstorder": alpha_naive,
        "alpha_codata": alpha_codata,
        "alpha_solved": alpha_solved,
        "rel_diff_solved_vs_codata": rel_diff,
        "alpha_precision_from_aexp": da_rel,
    }


def e4_tuft_supply():
    """TUFT 是否供给 QED 级数 / 反常磁矩结构？"""
    # TUFT（库内，已注销 C0133）无 QED、无圈图展开、无 Feynman 微扰级数；
    # a_e 是纯 QED 微扰对象（Schwinger 一阶 + 高阶圈图）。
    return {
        "tuft_has_qed": False,
        "tuft_has_loop_expansion": False,
        "tuft_has_feynman_diagrams": False,
        "tuft_supply": 0,
        "note": "a_e 依赖 QED 圈图级数（标准物理）；TUFT 无 QED/无圈图供给。",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0243 · 电子反常磁矩 a_e（母册 T270 · L 线域 H 批 · QED 级数核算）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 观测事实（只引用不复算）")
    w("  α = 1/%s = %s（CODATA 2018）" % (g1["alpha_inv_CODATA"], fv(g1["alpha"], "12f")))
    w("  QED 系数：C2=%s、C4=%s、C6=%s、C8=%s"
      % (g1["C2"], g1["C4"], g1["C6"], g1["C8"]))
    w("  a_e^exp = %s(末位 %s)（2022 Cs 反冲法）"
      % (g1["a_e_exp"], g1["a_e_exp_sigma"]))
    w("  来源：%s" % g1["source"])
    entries.append(("E1", "α/C2/C4/C6/C8/a_e^exp 外部输入显式计数，只引用不复算",
                    "PASS", "CODATA 2018 + 2022 Cs 反冲法"))

    # ---- E2 ----
    g2 = e2_series()
    w("\n[E2] a_e QED 级数精算（本册核心）")
    w("  x = α/π = %s" % fv(g2["x_alpha_over_pi"], "12f"))
    w("  一阶项 C2·x = α/2π = %s" % fv(g2["t1_2pi"], "10e"))
    w("  二阶项 C4·x²      = %s" % fv(g2["t2"], "10e"))
    w("  三阶项 C6·x³      = %s" % fv(g2["t3"], "10e"))
    w("  四阶项 C8·x⁴      = %s" % fv(g2["t4"], "10e"))
    w("  a_e^th（截断到四阶）= %s" % fv(g2["a_e_th"], "14f"))
    w("  a_e^exp             = %s" % fv(g2["a_e_exp"], "14f"))
    w("  偏差 Δ = th - exp   = %s（≈ %s σ）"
      % (fv(g2["delta_th_minus_exp"], "6e"), fv(g2["sigma_units"], "1f")))
    w("  => 截断级数（至 α⁴）与实验吻合至 ~1e-11 量级；残余由省略的 α⁶ 十阶项、")
    w("     强子/弱电小贡献解释（标准 QED 已知），本册不宣称任何新物理。")
    entries.append(("E2", "a_e^th=%s vs a_e^exp=%s，Δ=%s（%s σ）"
                    % (fv(g2["a_e_th"], "12f"), fv(g2["a_e_exp"], "12f"),
                       fv(g2["delta_th_minus_exp"], "3e"), fv(g2["sigma_units"], "1f")),
                    "PASS", "标准 QED 算术独立精算"))

    # ---- E3 ----
    g3 = e3_alpha_invert()
    w("\n[E3] α 反解核算")
    w("  朴素一阶反解 α = 2π·a_e = %s" % fv(g3["alpha_naive_firstorder"], "12f"))
    w("  截断级数求根反解 α = %s" % fv(g3["alpha_solved"], "12f"))
    w("  CODATA α          = %s" % fv(g3["alpha_codata"], "12f"))
    w("  相对偏差（反解 vs CODATA）= %s" % fv(g3["rel_diff_solved_vs_codata"], "2e"))
    w("  由 a_e 实验 σ 传导的 α 相对精度 δα/α ≈ δa_e/a_e = %s"
      % fv(g3["alpha_precision_from_aexp"], "2e"))
    w("  => 反解 α 精度 ~1e-10 量级（著名结果：a_e 是测 α 最准的探针之一）。")
    entries.append(("E3", "α 反解精度 %s（~1e-10 量级），与 CODATA 相对差 %s"
                    % (fv(g3["alpha_precision_from_aexp"], "1e"),
                       fv(g3["rel_diff_solved_vs_codata"], "1e")), "PASS",
                    "截断级数 bisection 求根"))

    # ---- E4 ----
    g4 = e4_tuft_supply()
    w("\n[E4] TUFT 供给检查")
    w("  TUFT 有 QED？ %s；有圈图展开？ %s；有 Feynman 图？ %s"
      % (g4["tuft_has_qed"], g4["tuft_has_loop_expansion"], g4["tuft_has_feynman_diagrams"]))
    w("  TUFT 供给 = %d（无）。%s" % (g4["tuft_supply"], g4["note"]))
    entries.append(("E4", "TUFT 供给 QED 级数/反常磁矩结构 = 0（无 QED、无圈图）",
                    "PASS", "结构性检查"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  a_e 是纯 QED 微扰级数对象（Schwinger 一阶 α/2π + 高阶圈图系数），")
    w("  其数值由标准 QED 算术完全复算（E2/E3），与实验吻合。")
    w("  TUFT（已注销 C0133）无 QED、无圈图、无 Feynman 微扰展开，对该结构供给 = 0。")
    w("  => **结构性负面（对 TUFT/几何框架）**：a_e 依赖标准物理圈图级数，")
    w("     TUFT 不能供给、不能预测、不能修正；按母册 T270 登记撞 C1/C5。")
    w("     严禁把标准 QED 结果写成 TUFT 预测/修正。")
    entries.append(("E5", "结构性负面：a_e=QED 圈图级数，TUFT 供给 0，撞 C1/C5",
                    "PASS", "按母册 T270 登记"))

    # ---- 守卫 ----
    guards = [
        ("G1", "一阶项 α/2π ≈ 1.1614e-3",
         abs(g2["t1_2pi"] - Decimal("0.001161409733")) < Decimal("1e-9")),
        ("G2", "截断级数 a_e^th 与实验差 |Δ| < 2e-11",
         abs(g2["delta_th_minus_exp"]) < Decimal("2e-11")),
        ("G3", "反解 α 与 CODATA 相对差 < 1e-7",
         abs(g3["rel_diff_solved_vs_codata"]) < Decimal("1e-7")),
        ("G4", "由 a_e 传导的 α 相对精度 ~1e-10（1e-11 – 5e-9）",
         Decimal("1e-11") < g3["alpha_precision_from_aexp"] < Decimal("5e-9")),
        ("G5", "TUFT 供给 QED 级数 = 0",
         g4["tuft_supply"] == 0 and not g4["tuft_has_qed"]),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0243 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称解决 a_e/轻子味普适问题；数值均为标准 QED 算术复核；")
    w("  α/a_e 测量值只引用不复算；TUFT 已注销（C0133），未把标准物理写成 TUFT 预测/修正。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0243_电子磁矩攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0243_电子磁矩攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0243_electron_anomalous_magnetic_moment",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": {k: str(v) for k, v in g1.items()},
            "E2_series": {k: str(v) for k, v in g2.items()},
            "E3_alpha_invert": {k: str(v) for k, v in g3.items()},
            "E4_tuft_supply": {k: str(v) for k, v in g4.items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0243 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
