# -*- coding: utf-8 -*-
"""
attack_C0178_质子自旋危机攻破_2026-10-21.py
独立精算：质子自旋求和规则（母册 T343 · 行 475）· 质子自旋危机

定位：母册 T343 原文照录——
  | T343 | 质子自旋危机（夸克自旋仅占 ~30%） | 胶子自旋 + 轨道角动量 | C1,C5 | 🔲 |
主题：质子自旋求和规则 1/2 = (1/2)ΔΣ + ΔG + L_z。EMC 实验发现夸克自旋贡献仅 ~30%
（ΔΣ≈0.30），余 ~70% 须由胶子自旋 ΔG 与轨道角动量 L_z 补充。

把「质子自旋从哪来」压缩成四条可复核读数：

  E1 观测事实引用（EMC/COMPASS/HERMES/PDG 只引用不复算）：质子自旋 1/2、
     ΔΣ=0.30±0.07、求和规则三项分解、ΔG/G≈0.2–0.4、胶子动量份额 G≈0.40。
  E2 **自旋求和规则残差分解（本册核心）**：R = 1/2 − (1/2)ΔΣ = ΔG + L_z；
     以 ΔG/G≈0.2–0.4、G≈0.40 反解 L_z 区间（Fraction 精确 + Decimal 48 位）。
  E3 配分算术：各分量占总自旋百分比——夸克自旋 30%、胶子+轨道合计 70% 的配分。
  E4 NQM(ΔΣ=1) vs 实测(ΔΣ=0.30) 比值核算：缺口 70% 的来源。
  E5 裁定：质子自旋结构依赖部分子/QCD 自由度，TUFT 无部分子/无胶子场供给，
     结构性负面，撞 C1/C5。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

归因口径：全部数值为标准粒子物理（部分子模型 / 自旋求和规则）算术或实验测量复核；
TUFT 已注销（C0133）。严禁把标准物理结果写成 TUFT 预测/修正。
诚实边界：不宣称解决任何物理难题；数学自洽 ≠ 实验证实；已攻破=对 TUFT/几何框架
结构性负面闭合；有预测且对 = 0/22；UFT-3=0 保持。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（实验测量 / PDG 只引用不复算） ----------
# 质子总自旋（角动量单位），精确 = 1/2
SPIN_TOTAL = Fraction(1, 2)
# EMC / 后续全球拟合：夸克自旋反常 ΔΣ ≈ 0.30 ± 0.07（只引用，不复算）
DSIGMA_CTR = Fraction(30, 100)   # 0.30
DSIGMA_HALF = Fraction(7, 100)  # 0.07（± 半宽）
# 未分裂夸克模型（NQM）：全部自旋来自夸克 ⇒ ΔΣ = 1
DSIGMA_NQM = Fraction(1, 1)
# COMPASS/HERMES 量级：胶子自旋相对值 ΔG/G ≈ 0.2–0.4（只引用）
DG_OVER_G_LO = Fraction(1, 5)   # 0.2
DG_OVER_G_HI = Fraction(2, 5)  # 0.4
DG_OVER_G_MID = Fraction(3, 10)  # 0.3
# 质子中胶子动量份额 G ≈ 0.40（HERMES/COMPASS/DSSV 典型区域，只引用）
G_GLUE = Fraction(2, 5)        # 0.40


def d(x: Fraction) -> Decimal:
    """Fraction -> Decimal 精确（约分后分子分母转 Decimal）。"""
    return Decimal(x.numerator) / Decimal(x.denominator)


def e1_facts():
    """E1 观测事实（只引用）。"""
    return {
        "spin_total": "1/2",
        "dSigma": "0.30 ± 0.07 (EMC / global fit)",
        "dSigma_NQM": "1 (naive quark model)",
        "dG_over_G_range": "0.2–0.4 (COMPASS/HERMES)",
        "G_glue_momentum_share": "0.40",
        "sum_rule": "1/2 = (1/2)ΔΣ + ΔG + L_z",
    }


def e2_residual_decomposition():
    """E2 核心：R = 1/2 − (1/2)ΔΣ = ΔG + L_z；反解 L_z 区间。"""
    # 中心 ΔΣ = 0.30
    qspin_ctr = (Fraction(1, 2)) * DSIGMA_CTR          # (1/2)ΔΣ = 0.15
    R_ctr = SPIN_TOTAL - qspin_ctr                     # 残差 = ΔG + L_z
    # ΔΣ 误差带上/下界
    dsig_hi = DSIGMA_CTR + DSIGMA_HALF                 # 0.37
    dsig_lo = DSIGMA_CTR - DSIGMA_HALF                 # 0.23
    qspin_hi = Fraction(1, 2) * dsig_hi                # 0.185
    qspin_lo = Fraction(1, 2) * dsig_lo                # 0.115
    R_hi = SPIN_TOTAL - qspin_hi                       # 残差上界 0.315
    R_lo = SPIN_TOTAL - qspin_lo                       # 残差下界 0.385
    # ΔG 候选三点（ΔG/G = 0.2 / 0.3 / 0.4，G = 0.40）
    dg_lo = DG_OVER_G_LO * G_GLUE                      # 0.08
    dg_mid = DG_OVER_G_MID * G_GLUE                    # 0.12
    dg_hi = DG_OVER_G_HI * G_GLUE                      # 0.16
    # 反解 L_z = R_ctr − ΔG
    Lz_at_dglo = R_ctr - dg_lo                         # 0.27
    Lz_at_dgmid = R_ctr - dg_mid                       # 0.23
    Lz_at_dghi = R_ctr - dg_hi                         # 0.19
    Lz_lo = Lz_at_dghi                                 # 区间下界（ΔG 取最大）
    Lz_hi = Lz_at_dglo                                 # 区间上界（ΔG 取最小）
    return {
        "qspin_ctr": qspin_ctr, "R_ctr": R_ctr,
        "dsig_hi": dsig_hi, "dsig_lo": dsig_lo,
        "qspin_hi": qspin_hi, "qspin_lo": qspin_lo,
        "R_hi": R_hi, "R_lo": R_lo,
        "dg_lo": dg_lo, "dg_mid": dg_mid, "dg_hi": dg_hi,
        "Lz_at_dglo": Lz_at_dglo, "Lz_at_dgmid": Lz_at_dgmid, "Lz_at_dghi": Lz_at_dghi,
        "Lz_lo": Lz_lo, "Lz_hi": Lz_hi,
    }


def e3_partition():
    """E3 配分算术：各分量占总自旋 1/2 的百分比。"""
    g2 = e2_residual_decomposition()
    # 夸克自旋占总自旋 = ((1/2)ΔΣ)/(1/2) = ΔΣ
    q_frac = DSIGMA_CTR / Fraction(1, 1)              # = 0.30
    # 胶子+轨道合计占总自旋 = R/(1/2)
    glue_orb_frac = g2["R_ctr"] / SPIN_TOTAL           # 0.35/0.5 = 0.70
    # ΔG 占比区间（0.08/0.5=0.16 … 0.16/0.5=0.32）
    dg_frac_lo = g2["dg_lo"] / SPIN_TOTAL
    dg_frac_hi = g2["dg_hi"] / SPIN_TOTAL
    # L_z 占比区间（0.19/0.5=0.38 … 0.27/0.5=0.54）
    Lz_frac_lo = g2["Lz_lo"] / SPIN_TOTAL
    Lz_frac_hi = g2["Lz_hi"] / SPIN_TOTAL
    return {
        "q_frac": q_frac, "glue_orb_frac": glue_orb_frac,
        "dg_frac_lo": dg_frac_lo, "dg_frac_hi": dg_frac_hi,
        "Lz_frac_lo": Lz_frac_lo, "Lz_frac_hi": Lz_frac_hi,
    }


def e4_nqm_vs_measured():
    """E4 NQM(ΔΣ=1) vs 实测(ΔΣ=0.30) 比值核算。"""
    # NQM 预言夸克自旋贡献 = (1/2)*1 = 0.5（占 100%）
    qspin_nqm = Fraction(1, 2) * DSIGMA_NQM            # 0.5
    # 实测夸克自旋贡献 = 0.15
    qspin_meas = Fraction(1, 2) * DSIGMA_CTR           # 0.15
    # 比值
    ratio = qspin_meas / qspin_nqm                      # 0.15/0.5 = 0.30
    dsigma_ratio = DSIGMA_CTR / DSIGMA_NQM             # 0.30/1 = 0.30
    # NQM 残差（应=0）
    R_nqm = SPIN_TOTAL - qspin_nqm                      # 0
    # 缺口（实测相对 NQM 少占的份额）
    gap = DSIGMA_NQM - DSIGMA_CTR                       # 0.70
    return {
        "qspin_nqm": qspin_nqm, "qspin_meas": qspin_meas,
        "ratio": ratio, "dsigma_ratio": dsigma_ratio,
        "R_nqm": R_nqm, "gap": gap,
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def p(x: Fraction) -> str:
        """Decimal 48 位逐字输出（去尾零）。"""
        return format(d(x), "f")

    w("=" * 74)
    w("attack_C0178 · 质子自旋危机（母册 T343 · 质子自旋求和规则）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 观测事实引用（EMC/COMPASS/HERMES/PDG 只引用不复算）")
    w("  质子总自旋 = %s" % g1["spin_total"])
    w("  求和规则：%s" % g1["sum_rule"])
    w("  夸克自旋反常 ΔΣ = %s" % g1["dSigma"])
    w("  未分裂夸克模型 ΔΣ = %s" % g1["dSigma_NQM"])
    w("  胶子自旋相对值 ΔG/G = %s；胶子动量份额 G ≈ %s"
      % (g1["dG_over_G_range"], g1["G_glue_momentum_share"]))
    w("  => 质子自旋结构 = 夸克自旋(ΔΣ) + 胶子自旋(ΔG) + 轨道角动量(L_z)，")
    w("     三项皆为部分子/QCD 自由度。")
    entries.append(("E1", "质子自旋 = (1/2)ΔΣ + ΔG + L_z 三项部分子分解（ΔΣ=0.30±0.07 实测）",
                    "PASS", "EMC/COMPASS/HERMES/PDG 只引用"))

    # ---- E2 ----
    g2 = e2_residual_decomposition()
    w("\n[E2] 自旋求和规则残差分解（本册核心）：R = 1/2 − (1/2)ΔΣ = ΔG + L_z")
    w("  中心 ΔΣ=0.30：夸克自旋 (1/2)ΔΣ = %s" % p(g2["qspin_ctr"]))
    w("  残差 R(中心) = 1/2 − %s = %s（= ΔG + L_z）" % (p(g2["qspin_ctr"]), p(g2["R_ctr"])))
    w("  误差带：ΔΣ∈[0.23,0.37] ⇒ (1/2)ΔΣ∈[%s, %s] ⇒ R∈[%s, %s]"
      % (p(g2["qspin_lo"]), p(g2["qspin_hi"]), p(g2["R_hi"]), p(g2["R_lo"])))
    w("  ΔG 候选（ΔG/G=0.2/0.3/0.4，G=0.40）：ΔG = %s / %s / %s"
      % (p(g2["dg_lo"]), p(g2["dg_mid"]), p(g2["dg_hi"])))
    w("  反解 L_z = R(中心) − ΔG：")
    w("    ΔG=%s ⇒ L_z=%s" % (p(g2["dg_lo"]), p(g2["Lz_at_dglo"])))
    w("    ΔG=%s ⇒ L_z=%s" % (p(g2["dg_mid"]), p(g2["Lz_at_dgmid"])))
    w("    ΔG=%s ⇒ L_z=%s" % (p(g2["dg_hi"]), p(g2["Lz_at_dghi"])))
    w("  => L_z 反解区间 = [%s, %s]（中心 ΔΣ=0.30）" % (p(g2["Lz_lo"]), p(g2["Lz_hi"])))
    entries.append(("E2", "R=0.35=ΔG+L_z；ΔG=0.08/0.12/0.16 ⇒ L_z∈[0.19,0.27]（Decimal 逐字）",
                    "PASS", "Fraction 精确 + Decimal 48 位；G、ΔG/G 为实验引用"))

    # ---- E3 ----
    g3 = e3_partition()
    w("\n[E3] 配分算术：各分量占总自旋 1/2 的百分比")
    w("  夸克自旋占总自旋 = %s/%s = %s%%"
      % (p(g2["qspin_ctr"]), p(SPIN_TOTAL), p(g3["q_frac"] * 100)))
    w("  胶子+轨道合计占总自旋 = %s/%s = %s%%"
      % (p(g2["R_ctr"]), p(SPIN_TOTAL), p(g3["glue_orb_frac"] * 100)))
    w("  ΔG 占比区间 = [%s%%, %s%%]；L_z 占比区间 = [%s%%, %s%%]"
      % (p(g3["dg_frac_lo"] * 100), p(g3["dg_frac_hi"] * 100),
         p(g3["Lz_frac_lo"] * 100), p(g3["Lz_frac_hi"] * 100)))
    w("  => 夸克自旋 ~30%、胶子+轨道合计 ~70%，配分算术闭合（30+70=100）。")
    entries.append(("E3", "夸克自旋 30%、胶子+轨道 70% 配分闭合；ΔG 16–32%、L_z 38–54%",
                    "PASS", "占比分母 = 总自旋 1/2"))

    # ---- E4 ----
    g4 = e4_nqm_vs_measured()
    w("\n[E4] NQM(ΔΣ=1) vs 实测(ΔΣ=0.30) 比值核算")
    w("  NQM 预言夸克自旋贡献 = (1/2)×1 = %s（占 100%%；残差 R_nqm = %s）"
      % (p(g4["qspin_nqm"]), p(g4["R_nqm"])))
    w("  实测夸克自旋贡献 = (1/2)×0.30 = %s" % p(g4["qspin_meas"]))
    w("  比值 实测/NQM = %s / %s = %s（即 ΔΣ 比值 = %s）"
      % (p(g4["qspin_meas"]), p(g4["qspin_nqm"]), p(g4["ratio"]), p(g4["dsigma_ratio"])))
    w("  缺口（NQM 预言 100%% − 实测 30%%）= %s，由胶子自旋+轨道角动量补足。"
      % p(g4["gap"]))
    w("  => 这即『质子自旋危机』：NQM 夸克模型少解释了 70% 的质子自旋。")
    entries.append(("E4", "实测/NQM 夸克自旋比 = 0.30；NQM 缺口 0.70 由胶子+轨道补",
                    "PASS", "NQM ΔΣ=1 为模型引用"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  质子自旋求和规则的三项（ΔΣ 夸克自旋、ΔG 胶子自旋、L_z 轨道角动量）")
    w("  全部是部分子/QCD 自由度：须以部分子分布、胶子场、量子色动力学为供给。")
    w("  TUFT 已注销（C0133）：无部分子结构、无胶子场供给、无 QCD 轨道角动量动力学。")
    w("  标准物理算术（E2–E4）只复核实验测量，不构成 TUFT 的任何预测/修正。")
    w("  => 质子自旋结构依赖部分子/QCD 自由度，TUFT 无供给 ⇒ 结构性负面闭合。")
    entries.append(("E5", "质子自旋结构依赖部分子/QCD 自由度，TUFT 无部分子/无胶子场供给，"
                    "结构性负面", "PASS", "撞 C1 / C5（母册登记）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "残差 R(ΔΣ=0.30) = 0.35（Fraction 精确 7/20）", g2["R_ctr"] == Fraction(7, 20)),
        ("G2", "夸克自旋占总自旋 = 30%（ΔΣ=0.30）", g3["q_frac"] == Fraction(30, 100)),
        ("G3", "胶子+轨道合计占总自旋 = 70%（R/(1/2)=0.70）",
         g3["glue_orb_frac"] == Fraction(70, 100)),
        ("G4", "L_z 反解区间 = [0.19, 0.27]（即 [19/100, 27/100]）",
         g2["Lz_lo"] == Fraction(19, 100) and g2["Lz_hi"] == Fraction(27, 100)),
        ("G5", "实测/NQM 夸克自旋比 = 0.30（缺口 0.70）",
         g4["ratio"] == Fraction(30, 100) and g4["gap"] == Fraction(70, 100)),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0178 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  不宣称解决任何物理难题；已攻破 = 对 TUFT/几何框架结构性负面闭合；")
    w("  有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")
    w("  数值均为标准粒子物理（部分子模型/自旋求和规则）算术或实验测量复核；")
    w("  TUFT 已注销（C0133），严禁把标准物理结果写成 TUFT 预测/修正。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0178_质子自旋危机攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0178_质子自旋危机攻破_2026-10-21.json")

    def ser(x):
        if isinstance(x, Fraction):
            return {"fraction": "%d/%d" % (x.numerator, x.denominator),
                    "decimal48": str(d(x))}
        return str(x)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0178_proton_spin_crisis",
            "source_row": "T343 (母册行475)",
            "sum_rule": "1/2 = (1/2)dSigma + dG + L_z",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": g1,
            "E2_residual": {k: ser(v) for k, v in g2.items()},
            "E3_partition": {k: ser(v) for k, v in g3.items()},
            "E4_nqm": {k: ser(v) for k, v in g4.items()},
            "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0178 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
