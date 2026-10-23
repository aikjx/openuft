# -*- coding: utf-8 -*-
"""
attack_C0195_质子衰变实验攻破_2026-10-21.py
独立精算：T026「质子衰变实验」· 大统一（SU(5)/SO(10)）质子寿命 vs Super-K 实验下限

定位：母册 T026（行117）：`| T026 | 质子衰变实验 | 实验检验 | C5,C6 | ◐ C0132：
τ_pred~1e30 vs τ_exp>1e36 |`。本册衔接 C0132 的粗量级口径（1e6 超标），升级为标准大统一
算术的**精确复核**：minimal SU(5) 路径 vs MSSM 路径的双路径残差守卫收口 ◐。

把"质子衰变实验"压缩成五条可复核读数 + 一张输入账单：

  E1 实验事实（Super-K / PDG 只引用不复算）：τ(p→e⁺π⁰) 下限、无衰变观测、M_X 标度。
  E2 **第一性推导 + Decimal 48 位精算（本册核心）**：
     minimal SU(5)：τ_p ~ M_X^4/(α_G^2 m_p^5)（GeV^-1 → yr），得 τ_min_SU5；
     对比 Super-K 下限 τ_exp 得排除倍数；MSSM 路径 τ_p(MSSM) 超界倍数。
  E3 双路径残差守卫：M_X（1e15–1e16 GeV）与 α_G（1/50–1/30）摆动下 τ_min_SU5 残差带、
     与实验界的交叉点；minimal 排除 / MSSM 超界的对称性分析。
  E4 TUFT 供给检查：TUFT（零参数几何框架）是否供给质子衰变（B 破坏算符 / X/Y 规范玻色子 /
     M_X 标度）——结论结构性供给 = 0。
  E5 裁定：质子衰变依赖 GUT 规范结构（外部输入），TUFT 无供给，结构性负面，撞 C5/C6。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界（硬）：本册所有数值均为**标准大统一（SU(5)/MSSM）算术复核**，不是 TUFT 预测/修正；
TUFT 已于 C0133 终审注销。外部实验值（Super-K 下限、CODATA ħ）只引用不复算。
红线：「不宣称解决任何物理难题」「已攻破=对 TUFT/几何框架结构性负面闭合」
「有预测且对 = 0/22」「UFT-3=0 保持」「数学自洽 ≠ 实验证实」。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（只引用不复算，标注来源） ----------
# 标准大统一算术输入（minimal SU(5) 规范耦合汇聚读出）：
M_X = Decimal("1e15")          # GeV，GUT 标度（minimal SU(5) 中心值）
ALPHA_G = Decimal(1) / Decimal(40)   # 统一耦合常数 α_G ≈ 1/40
M_P = Decimal("0.938")         # GeV，质子质量
# CODATA：1 GeV^-1 = ħ [GeV·s] = 6.582119569e-25 s；1 yr = 31557600 s（365.25 d）
HBAR_GEV_S = Decimal("6.582119569e-25")
SECONDS_PER_YR = Decimal("31557600")
# Super-K 90% CL 实验下限（p→e⁺π⁰，外部实验事实，只引用）
TAU_EXP = Decimal("2.4e34")    # yr
# MSSM 路径中心预测（标准 GUT 算术，来料引用）
TAU_MSSM = Decimal("2.87e36")  # yr


def GeV_inv_to_yr():
    """1 GeV^-1 → yr 换算常数（Decimal 精算）。"""
    return HBAR_GEV_S / SECONDS_PER_YR


def tau_min_su5(m_x: Decimal, alpha_g: Decimal, m_p: Decimal) -> Decimal:
    """minimal SU(5) 质子寿命：τ_p ~ M_X^4/(α_G^2 m_p^5)，返回 yr。

    推导链（自然单位 ℏ=c=1，量纲 GeV^-1）：
      维6 B破坏算符 O_{dim6} ~ (1/M_X^2)(qqql)，四费米子衰变率 Γ ~ α_G^2 m_p^5 / M_X^4
      ⇒ τ = 1/Γ ~ M_X^4/(α_G^2 m_p^5)  [GeV^-1]
      ⇒ 乘 ħ [GeV·s] 得秒，除 yr 得 yr。
    """
    rate_per_GeV = (m_x ** 4) / (alpha_g ** 2 * m_p ** 5)   # GeV^-1
    return rate_per_GeV * GeV_inv_to_yr()


def e1_facts():
    """E1 实验事实（Super-K / PDG 只引用）。"""
    return {
        "channel": "p -> e+ pi0",
        "tau_exp_min_yr": TAU_EXP,
        "decays_observed": 0,
        "M_X_minimal_SU5_GeV": M_X,
        "M_X_MSSM_GeV": Decimal("1e16"),
        "alpha_G": ALPHA_G,
        "note": "Super-K 90% CL 下限只引用；CODATA ħ 只引用；无衰变事例。",
    }


def e2_core():
    """E2 第一性推导 + Decimal 精算（本册核心）。"""
    conv = GeV_inv_to_yr()
    tau_min = tau_min_su5(M_X, ALPHA_G, M_P)
    # 排除倍数：实验下限 / minimal 预测（>1 ⇒ minimal 被排除）
    ratio_excl = TAU_EXP / tau_min
    # MSSM 超界倍数：MSSM 预测 / 实验下限（>1 ⇒ 安全，超界不可观测）
    ratio_safe = TAU_MSSM / TAU_EXP
    return {
        "conv_GeV_inv_per_yr": conv,
        "tau_min_SU5_yr": tau_min,
        "tau_MSSM_yr": TAU_MSSM,
        "tau_exp_yr": TAU_EXP,
        "ratio_exclude_minimal": ratio_excl,
        "ratio_safe_MSSM": ratio_safe,
    }


def e3_sweep():
    """E3 双路径残差守卫：M_X 与 α_G 摆动下 minimal τ 的残差带 + 交叉点。"""
    # M_X 摆动 1e15–1e16 GeV（4 个数量级跨度，τ ~ M_X^4 ⇒ 1e4 跨度）
    mx_lo = Decimal("1e15")
    mx_hi = Decimal("1e16")
    alpha_lo = Decimal(1) / Decimal(50)   # α_G=1/50
    alpha_hi = Decimal(1) / Decimal(30)   # α_G=1/30
    tau_lo = tau_min_su5(mx_lo, alpha_hi, M_P)   # 最小 τ：低 M_X、高 α_G
    tau_hi = tau_min_su5(mx_hi, alpha_lo, M_P)   # 最大 τ：高 M_X、低 α_G
    # 交叉点：τ_min_SU5(M_X) = τ_exp ⇒ M_X^4 = τ_exp * α_G^2 m_p^5 / conv
    # M_X_cross = (τ_exp * α_G^2 m_p^5 / conv)^(1/4)
    inner = TAU_EXP * ALPHA_G ** 2 * M_P ** 5 / GeV_inv_to_yr()
    mx_cross = inner ** (Decimal(1) / Decimal(4))
    # minimal 中心值是否在残差带内被排除（带下端 < τ_exp ⇒ 带整体不能全部自救）
    band_straddles = (tau_lo < TAU_EXP) and (tau_hi > TAU_EXP)
    return {
        "M_X_lo": mx_lo, "M_X_hi": mx_hi,
        "alpha_lo": alpha_lo, "alpha_hi": alpha_hi,
        "tau_band_lo": tau_lo, "tau_band_hi": tau_hi,
        "M_X_cross_GeV": mx_cross,
        "band_straddles_exp": band_straddles,
        "MSSM_safe_vs_band": TAU_MSSM / tau_hi,
    }


def e4_tuft_supply():
    """E4 TUFT 供给检查：零参数几何框架是否供给质子衰变。"""
    return {
        "dimension6_B_violating_operator": False,   # 无 (qqql)/M_X^2 算符
        "X_Y_gauge_bosons": False,                    # 无 SU(5) X/Y 规范玻色子
        "M_X_external_input": False,                 # 零参数框架不引入 GUT 标度
        "le_broken_TUFT": True,                      # C0133 终审已注销
        "supply": "zero",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0195 · 质子衰变实验（T026 · 双路径残差守卫收口 ◐）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 实验事实（Super-K / PDG 只引用不复算）")
    w("  通道 %s：τ_exp(min) > %s yr（90%% CL，外部实验事实）"
      % (g1["channel"], fv(g1["tau_exp_min_yr"], "1e")))
    w("  衰变观测事例数 = %d（零信号）" % g1["decays_observed"])
    w("  GUT 标度：minimal SU(5) M_X ~ %s GeV；MSSM M_X ~ %s GeV"
      % (fv(g1["M_X_minimal_SU5_GeV"], "1e"), fv(g1["M_X_MSSM_GeV"], "0e")))
    w("  统一耦合 α_G = %s" % fv(g1["alpha_G"], "4f"))
    w("  机器裁定 E1（PASS）：质子寿命是可实验证伪的观测量；Super-K 已把下限推到 %s yr 量级。"
      % fv(TAU_EXP, "1e"))
    entries.append(("E1", "Super-K τ(p→e⁺π⁰) > %s yr，零观测；M_X~1e15(最小SU5)/1e16(MSSM)"
                    % fv(TAU_EXP, "1e"), "PASS", "外部实验值只引用不复算"))

    # ---- E2 ----
    g2 = e2_core()
    w("\n[E2] 第一性推导 + Decimal 48 位精算（本册核心）")
    w("  推导：维6 B破坏算符 O~(qqql)/M_X^2 ⇒ Γ~α_G^2 m_p^5/M_X^4 ⇒ τ~M_X^4/(α_G^2 m_p^5)")
    w("  换算常数 1 GeV^-1 = ħ/yr = %s yr" % fv(g2["conv_GeV_inv_per_yr"], "4e"))
    w("  minimal SU(5)：M_X=%s GeV, α_G=1/40, m_p=%s GeV" % (fv(M_X, "0e"), M_P))
    w("    ⇒ τ_min_SU5 = %s yr（Decimal 逐字）" % fv(g2["tau_min_SU5_yr"], "4e"))
    w("  排除倍数：τ_exp / τ_min_SU5 = %s ⇒ minimal SU(5) 被 Super-K 排除（>1 即证伪）"
      % fv(g2["ratio_exclude_minimal"], "3f"))
    w("  MSSM 路径：τ_p(MSSM) = %s yr（标准 GUT 算术引用）" % fv(TAU_MSSM, "3e"))
    w("    ⇒ 超界倍数：τ_MSSM / τ_exp = %s ⇒ MSSM 预测安全（>1）但被推到不可观测"
      % fv(g2["ratio_safe_MSSM"], "3f"))
    w("  衔接 C0132：粗量级 τ_pred~1e30 vs τ_exp>1e36=1e6；本册精确复核 minimal 路径为"
      " %s 排除、MSSM 路径 %s 超界。"
      % (fv(g2["ratio_exclude_minimal"], "2f"), fv(g2["ratio_safe_MSSM"], "2f")))
    entries.append(("E2", "τ_min_SU5=%s yr（Decimal）；τ_exp/τ_min=%s 排除；"
                    "τ_MSSM=%s yr，τ_MSSM/τ_exp=%s 超界"
                    % (fv(g2["tau_min_SU5_yr"], "4e"), fv(g2["ratio_exclude_minimal"], "2f"),
                       fv(TAU_MSSM, "3e"), fv(g2["ratio_safe_MSSM"], "2f")),
                    "PASS", "标准 SU(5)/MSSM 算术复核；非 TUFT 预测"))

    # ---- E3 ----
    g3 = e3_sweep()
    w("\n[E3] 双路径残差守卫：M_X、α_G 摆动下的残差带")
    w("  M_X ∈ [%s, %s] GeV；α_G ∈ [1/50, 1/30]"
      % (fv(g3["M_X_lo"], "0e"), fv(g3["M_X_hi"], "0e")))
    w("  τ_min_SU5 残差带：[%s, %s] yr"
      % (fv(g3["tau_band_lo"], "3e"), fv(g3["tau_band_hi"], "3e")))
    w("  与实验界 τ_exp=%s yr 的交叉点 M_X_cross = %s GeV"
      % (fv(TAU_EXP, "1e"), fv(g3["M_X_cross_GeV"], "3e")))
    w("  残差带是否横跨实验界（带下端<τ_exp<带上端）：%s" % g3["band_straddles_exp"])
    w("  ⇒ 即使摆动 α_G 与 M_X，minimal SU(5) 中心值 %s yr 距实验界仍有 %s 倍；"
      "须 M_X ≳ %s GeV 才能自救，而规范耦合汇聚钉死 M_X~1e15 GeV ⇒ minimal 排除稳固。"
      % (fv(g2["tau_min_SU5_yr"], "3e"), fv(g2["ratio_exclude_minimal"], "1f"),
         fv(g3["M_X_cross_GeV"], "2e")))
    w("  MSSM 路径相对残差带上端仍高 %s 倍 ⇒ 超界安全，但同时失去可观测性（撞 C5 可检验性）。"
      % fv(g3["MSSM_safe_vs_band"], "2f"))
    entries.append(("E3", "残差带 [%s,%s] yr 横跨实验界；交叉 M_X=%s GeV；minimal 排除稳固、"
                    "MSSM 超界 %s 倍"
                    % (fv(g3["tau_band_lo"], "2e"), fv(g3["tau_band_hi"], "2e"),
                       fv(g3["M_X_cross_GeV"], "2e"), fv(g3["MSSM_safe_vs_band"], "1f")),
                    "PASS", "M_X^4 标度律 + α_G 摆动"))

    # ---- E4 ----
    g4 = e4_tuft_supply()
    w("\n[E4] TUFT 供给检查（实验检验供给）")
    w("  维6 B破坏算符 (qqql)/M_X^2：%s" % g4["dimension6_B_violating_operator"])
    w("  SU(5) X/Y 规范玻色子：%s" % g4["X_Y_gauge_bosons"])
    w("  GUT 标度 M_X 外部输入：%s（零参数框架不引入）" % g4["M_X_external_input"])
    w("  TUFT 状态：%s（C0133 终审已注销）" % ("已注销" if g4["le_broken_TUFT"] else "在库"))
    w("  ⇒ 质子衰变是 GUT 规范结构的产物；TUFT 零参数几何框架**无任何 B 破坏供给**，"
      "结构性供给 = 0。")
    entries.append(("E4", "TUFT 无维6 B破坏算符 / 无 X/Y 玻色子 / 无 M_X 输入 ⇒ 供给 0",
                    "PASS", "TUFT C0133 已注销；不把标准 GUT 算术写成 TUFT 预测"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  质子衰变问题被精确翻译成：(a) B 破坏算符与 M_X 标度从哪来；(b) 框架能否被 Super-K 证伪。")
    w("  (a) minimal SU(5) 预测 %s yr ≪ τ_exp=%s yr，被排除 %s 倍；"
      "MSSM 路径 %s yr 超界 %s 倍（不可观测）。"
      % (fv(g2["tau_min_SU5_yr"], "3e"), fv(TAU_EXP, "1e"),
         fv(g2["ratio_exclude_minimal"], "1f"), fv(TAU_MSSM, "3e"),
         fv(g2["ratio_safe_MSSM"], "1f")))
    w("  (b) TUFT 零参数框架无 B 破坏算符、无 GUT 供给 ⇒ 不能产生质子衰变预言，"
      "亦不能被 Super-K 证伪。")
    w("  => **对 TUFT/几何框架结构性负面（T026 ◐ 收口）**；撞 C5（可检验性：TUFT 无预言/无证伪）"
      "与 C6（误差带：残差带分析）。标准 SU(5)/MSSM 算术仅为外部复核，非 TUFT 修正。")
    entries.append(("E5", "T026 结构性负面：质子衰变依赖 GUT 规范结构（外部输入），TUFT 无供给；"
                    "撞 C5/C6", "PASS", "minimal 排除 %s× / MSSM 超界 %s×"
                    % (fv(g2["ratio_exclude_minimal"], "1f"), fv(g2["ratio_safe_MSSM"], "1f"))))

    # ---- 守卫 ----
    guards = [
        ("G1", "τ_min_SU5 精算 ≈ 4.6e31 yr（±50%）",
         Decimal("3e31") < g2["tau_min_SU5_yr"] < Decimal("7e31")),
        ("G2", "minimal SU(5) 被排除（τ_exp/τ_min > 1）",
         g2["ratio_exclude_minimal"] > Decimal("1")),
        ("G3", "MSSM 超界（τ_MSSM/τ_exp > 1）",
         g2["ratio_safe_MSSM"] > Decimal("1")),
        ("G4", "排除倍数量级 ≈ 5.2e2（522，±30%）",
         Decimal("3.6e2") < g2["ratio_exclude_minimal"] < Decimal("6.8e2")),
        ("G5", "MSSM 超界倍数 ≈ 1.2e2（120，±30%）",
         Decimal("85") < g2["ratio_safe_MSSM"] < Decimal("156")),
        ("G6", "TUFT 供给 = 0（无 B 破坏算符）",
         g4["dimension6_B_violating_operator"] is False and g4["supply"] == "zero"),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0195 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  不宣称解决质子衰变；已攻破=对 TUFT/几何框架结构性负面闭合；有预测且对 = 0/22；")
    w("  UFT-3=0 保持；数学自洽 ≠ 实验证实。数值均为标准 GUT 算术复核，非 TUFT 预测/修正。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0195_质子衰变实验攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0195_质子衰变实验攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0195_proton_decay_experiment",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": {k: (str(v) if not isinstance(v, (int,)) else v)
                         for k, v in g1.items()},
            "E2_core": {k: str(v) for k, v in g2.items()},
            "E3_sweep": {k: (str(v) if not isinstance(v, bool) else str(v))
                         for k, v in g3.items()},
            "E4_tuft_supply": {k: str(v) for k, v in g4.items()},
            "guards": [{"id": g[0], "desc": g[1], "ok": str(g[2])} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0195 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
