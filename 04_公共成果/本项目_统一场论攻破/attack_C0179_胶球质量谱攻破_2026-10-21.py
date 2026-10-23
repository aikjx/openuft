# -*- coding: utf-8 -*-
"""
attack_C0179_胶球质量谱攻破_2026-10-21.py
独立复算：母册 T339「胶球质量谱与 f0(1500)/f0(1710) 混合」· 格点 QCD（撞 C6/C7）

定位：母册 T339（行 471）。主题 = QCD 胶球（纯胶场束缚态）质量谱——
格点 QCD 预言 0⁺⁺ 基态 ~1.5–1.7 GeV、2⁺⁺ ~2.4 GeV、0⁻⁺ ~2.6 GeV，
实验候选 f0(1500)/f0(1710) 与夸克态混合。

把"胶球谱与 f0 混合"压缩成四条可复核读数：

  E1 实验候选事实（PDG 只引用不复算）：f0(1500)=1505 MeV、f0(1710)=1714 MeV。
  E2 **格点 QCD 胶球谱比独立精算（本册核心）**：M(2⁺⁺)/M(0⁺⁺)、
     M(0⁻⁺)/M(0⁺⁺)，含误差带（0⁺⁺ 取 1.5–1.7 GeV）。
  E3 f0(1500)/f0(1710) 两态混合算术：质量差 209 MeV、迹不变量、
     非对角混合元 V、混合角（2x2 质量矩阵反演）。
  E4 胶球占比约束：纯胶态质量 M_g 在格点带 1.5–1.7 GeV 内扫描，
     f0(1710) 胶球成分分数的物理区间。
  E5 裁定：胶球谱依赖 SU(3) 规范场纯胶态动力学（格点 QCD），
     TUFT 无胶场/无格点谱供给 ⇒ 结构性负面，撞 C6/C7。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：本册不宣称已解释胶球谱；PDG 质量值只引用不复算；
格点数值为标准纯胶格点 QCD（Morningstar–Peardon 量级）引用；
2x2 混合反演为代数构造，结论按数量级与区间判定。
TUFT 已注销（C0133）；严禁把标准物理结果写成 TUFT 预测/修正。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（PDG / 格点 QCD 只引用不复算） ----------
# PDG 实验候选（MeV）
M_F0_1500 = Decimal("1505")   # f0(1500) 质量（PDG，中心值）
M_F0_1710 = Decimal("1714")   # f0(1710) 质量（PDG，中心值）
# 任务口径取整值
M_F0_1500_R = Decimal("1500")
M_F0_1710_R = Decimal("1710")

# 格点 QCD 纯胶态谱（标准量级，只引用）
M_0PP_CEN = Decimal("1600")   # 0⁺⁺ 基态中心（MeV）
M_0PP_LO = Decimal("1500")    # 0⁺⁺ 误差带下沿
M_0PP_HI = Decimal("1700")    # 0⁺⁺ 误差带上沿
M_2PP = Decimal("2400")       # 2⁺⁺ 轨道激发
M_0MP = Decimal("2600")       # 0⁻⁺ 赝标胶球


def e1_experimental_facts():
    """实验候选事实（PDG 只引用）。"""
    return {
        "f0_1500_MeV": M_F0_1500,
        "f0_1710_MeV": M_F0_1710,
        "rounded_1500": M_F0_1500_R,
        "rounded_1710": M_F0_1710_R,
    }


def e2_lattice_ratios():
    """格点 QCD 胶球谱比独立精算（核心）。"""
    # 中心比
    r_2pp_cen = M_2PP / M_0PP_CEN
    r_0mp_cen = M_0MP / M_0PP_CEN
    # 误差带：0⁺⁺ 在 1.5–1.7 GeV 间滑动
    r_2pp_lo = M_2PP / M_0PP_HI   # 0⁺⁺ 取上沿 → 比下沿
    r_2pp_hi = M_2PP / M_0PP_LO   # 0⁺⁺ 取下沿 → 比上沿
    r_0mp_lo = M_0MP / M_0PP_HI
    r_0mp_hi = M_0MP / M_0PP_LO
    return {
        "r_2pp_over_0pp_cen": r_2pp_cen,
        "r_0mp_over_0pp_cen": r_0mp_cen,
        "r_2pp_band_lo": r_2pp_lo,
        "r_2pp_band_hi": r_2pp_hi,
        "r_0mp_band_lo": r_0mp_lo,
        "r_0mp_band_hi": r_0mp_hi,
    }


def e3_mixing_2x2(m_g: Decimal):
    """2x2 质量矩阵反演：给定纯胶态质量 M_g，反推夸克态质量与混合元。

    质量矩阵 [[M_q, V],[V, M_g]]，本征值 m1=1505, m2=1714。
    迹不变：m1+m2 = M_q + M_g ⇒ M_q = trace - M_g。
    分裂：Δ = m2 - m1；对角分裂 Δd = |M_q - M_g|。
    非对角元 V = 0.5*sqrt(Δ² - Δd²)（要求 Δ ≥ Δd 才物理）。
    tan(2θ) = 2V/Δd；cos(2θ) = 1/sqrt(1+tan²2θ)。
    f0(1710)（高阶本征态）胶球成分分数 = cos²θ = (1+cos2θ)/2。
    """
    m1, m2 = M_F0_1500, M_F0_1710
    delta = m2 - m1
    trace = m1 + m2
    m_q = trace - m_g
    d_diag = abs(m_q - m_g)
    discrim = delta * delta - d_diag * d_diag
    physical = discrim >= 0
    if physical:
        v = Decimal("0.5") * discrim.sqrt()
        tan2t = (Decimal("2") * v) / d_diag if d_diag > 0 else Decimal("0")
        cos2t = Decimal("1") / (Decimal("1") + tan2t * tan2t).sqrt()
        glue_frac_high = (Decimal("1") + cos2t) / Decimal("2")
    else:
        v = None
        tan2t = None
        cos2t = None
        glue_frac_high = None
    return {
        "m_g_MeV": m_g, "m_q_MeV": m_q, "delta_MeV": delta,
        "trace_MeV": trace, "d_diag_MeV": d_diag,
        "discriminant": discrim, "physical": physical,
        "V_MeV": v, "tan2theta": tan2t, "cos2theta": cos2t,
        "glue_frac_f0_1710": glue_frac_high,
    }


def e4_glue_fraction_scan():
    """纯胶态质量 M_g 在格点带 1.5–1.7 GeV 内扫描，胶球占比区间。"""
    rows = []
    for mg in [M_0PP_LO, Decimal("1650"), M_0PP_CEN, M_0PP_HI]:
        rows.append(e3_mixing_2x2(mg))
    return rows


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6f"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0179 · 胶球质量谱与 f0(1500)/f0(1710) 混合（母册 T339）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_experimental_facts()
    w("\n[E1] 实验候选事实（PDG 只引用不复算）")
    w("  f0(1500) = %s MeV；f0(1710) = %s MeV"
      % (fv(g1["f0_1500_MeV"], "0f"), fv(g1["f0_1710_MeV"], "0f")))
    w("  任务取整口径：%s / %s MeV ⇒ 质量差 %s MeV"
      % (fv(g1["rounded_1500"], "0f"), fv(g1["rounded_1710"], "0f"),
         fv(g1["rounded_1710"] - g1["rounded_1500"], "0f")))
    w("  => 两个标量共振，被视为 0⁺⁺ 胶球与 u/d/s 夸克态的混合候选。")
    entries.append(("E1", "实验候选 f0(1500)=1505 / f0(1710)=1714 MeV（PDG 只引用）",
                    "PASS", "PDG 只引用；本册只做差分与归一换算"))

    # ---- E2 ----
    g2 = e2_lattice_ratios()
    w("\n[E2] 格点 QCD 胶球谱比独立精算（本册核心）")
    w("  格点纯胶谱（中心）：0⁺⁺=%s MeV、2⁺⁺=%s MeV、0⁻⁺=%s MeV"
      % (fv(M_0PP_CEN, "0f"), fv(M_2PP, "0f"), fv(M_0MP, "0f")))
    w("  R(2⁺⁺/0⁺⁺) 中心 = %s（=%s/%s）"
      % (fv(g2["r_2pp_over_0pp_cen"], "6f"), fv(M_2PP, "0f"), fv(M_0PP_CEN, "0f")))
    w("  R(0⁻⁺/0⁺⁺) 中心 = %s" % fv(g2["r_0mp_over_0pp_cen"], "6f"))
    w("  0⁺⁺ 误差带 1.5–1.7 GeV 滑动 ⇒ R(2⁺⁺/0⁺⁺) ∈ [%s, %s]"
      % (fv(g2["r_2pp_band_lo"], "6f"), fv(g2["r_2pp_band_hi"], "6f")))
    w("                     R(0⁻⁺/0⁺⁺) ∈ [%s, %s]"
      % (fv(g2["r_0mp_band_lo"], "6f"), fv(g2["r_0mp_band_hi"], "6f")))
    w("  => 轨道/激发态比基态重 ~1.4–1.6 倍，与格点 QCD 标准预言一致。")
    entries.append(("E2", "R(2⁺⁺/0⁺⁺)=%s 中心、带 [%s,%s]；"
                          "R(0⁻⁺/0⁺⁺)=%s"
                    % (fv(g2["r_2pp_over_0pp_cen"], "4f"),
                       fv(g2["r_2pp_band_lo"], "4f"), fv(g2["r_2pp_band_hi"], "4f"),
                       fv(g2["r_0mp_over_0pp_cen"], "4f")),
                    "PASS", "标准格点纯胶谱算术，Decimal 48 位精算"))

    # ---- E3 ----
    g3 = e3_mixing_2x2(Decimal("1650"))
    w("\n[E3] f0(1500)/f0(1710) 两态 2x2 混合反演（取 M_g=1650 MeV）")
    w("  Δ = m2 - m1 = %s - %s = %s MeV"
      % (fv(M_F0_1710, "0f"), fv(M_F0_1500, "0f"),
         fv(g3["delta_MeV"], "0f")))
    w("  迹不变量 trace = %s + %s = %s MeV ⇒ M_q = trace - M_g = %s MeV"
      % (fv(M_F0_1500, "0f"), fv(M_F0_1710, "0f"), fv(g3["trace_MeV"], "0f"),
         fv(g3["m_q_MeV"], "0f")))
    w("  对角分裂 Δd = |M_q - M_g| = %s MeV；要求 Δ ≥ Δd 才物理（%s ≥ %s）"
      % (fv(g3["d_diag_MeV"], "0f"), fv(g3["delta_MeV"], "0f"),
         fv(g3["d_diag_MeV"], "0f")))
    w("  非对角混合元 V = 0.5*sqrt(Δ²-Δd²) = %s MeV" % fv(g3["V_MeV"], "4f"))
    w("  tan(2θ) = 2V/Δd = %s；cos(2θ) = 1/sqrt(1+tan²2θ) = %s"
      % (fv(g3["tan2theta"], "6f"), fv(g3["cos2theta"], "6f")))
    w("  => 混合角自由度存在；f0(1710) 胶球成分分数 = %s（≈ %s%%）"
      % (fv(g3["glue_frac_f0_1710"], "6f"),
         fv(g3["glue_frac_f0_1710"] * Decimal("100"), "2f")))
    entries.append(("E3", "Δ=%s MeV、trace=%s MeV、V=%s MeV、混合角自由度存在"
                    % (fv(g3["delta_MeV"], "0f"), fv(g3["trace_MeV"], "0f"),
                       fv(g3["V_MeV"], "2f")),
                    "PASS", "2x2 质量矩阵代数反演，Decimal sqrt"))

    # ---- E4 ----
    scan = e4_glue_fraction_scan()
    w("\n[E4] 胶球占比约束：M_g 在格点带 1.5–1.7 GeV 扫描")
    for r in scan:
        if r["physical"]:
            w("  M_g=%s MeV ⇒ M_q=%s MeV, V=%s MeV, "
              "f0(1710) 胶球占比=%s（%s%%）"
              % (fv(r["m_g_MeV"], "0f"), fv(r["m_q_MeV"], "0f"),
                 fv(r["V_MeV"], "2f"), fv(r["glue_frac_f0_1710"], "4f"),
                 fv(r["glue_frac_f0_1710"] * Decimal("100"), "2f")))
        else:
            w("  M_g=%s MeV ⇒ 判别式 %s < 0 ⇒ 非物理（无实混合元）"
              % (fv(r["m_g_MeV"], "0f"), fv(r["discriminant"], "0f")))
    w("  => 格点带内物理点 f0(1710) 胶球占比 54.6%–93.3%，与文献『胶球富集』定性一致；")
    w("     M_g=1500 MeV 端判别式为负 ⇒ 纯胶态不能低至 1.5 GeV 而仍给出实分裂。")
    phys_fracs = [r["glue_frac_f0_1710"] for r in scan if r["physical"]]
    entries.append(("E4", "格点带内 f0(1710) 胶球占比 %s%%–%s%%；M_g=1500 端非物理"
                    % (fv(min(phys_fracs) * Decimal("100"), "1f"),
                       fv(max(phys_fracs) * Decimal("100"), "1f")),
                    "PASS", "M_g 扫描，物理区间约束"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  胶球谱与 f0 混合的物理内容 = SU(3) 规范场纯胶态的禁闭动力学（格点 QCD 数值）。")
    w("  (a) 谱比 R(2⁺⁺/0⁺⁺) 由格点纯胶作用量给定（E2）；")
    w("  (b) f0 混合由夸克-胶 2x2 矩阵给定（E3/E4），V 是强子物理拟合量。")
    w("  TUFT/几何框架：无胶场自由度、无格点纯胶作用量、无夸克-胶混合元供给。")
    w("  => 胶球谱依赖 SU(3) 规范场纯胶态动力学（格点 QCD），")
    w("     TUFT 无胶场/无格点谱供给 ⇒ 结构性负面，按母册登记撞 C6/C7。")
    entries.append(("E5", "胶球谱依赖格点 QCD 纯胶动力学；TUFT 无胶场/无格点谱供给，"
                    "结构性负面", "PASS", "撞 C6（误差带）/ C7（数学自洽）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "PDG 中心质量差 Δ = 1714-1505 = 209 MeV",
         g3["delta_MeV"] == Decimal("209")),
        ("G2", "格点中心比 R(2⁺⁺/0⁺⁺) = 2400/1600 = 1.5",
         g2["r_2pp_over_0pp_cen"] == Decimal("1.5")),
        ("G3", "迹不变量 trace = 1505+1714 = 3219 MeV",
         g3["trace_MeV"] == Decimal("3219")),
        ("G4", "M_g=1650 时判别式 > 0（V 为实数，混合物理）",
         g3["discriminant"] > 0),
        ("G5", "f0(1710) 胶球占比在 (0,1) 内",
         Decimal("0") < g3["glue_frac_f0_1710"] < Decimal("1")),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0179 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解释胶球谱：PDG 质量与格点纯胶谱只引用；2x2 混合为代数构造；")
    w("  判定按数量级与区间。裁的是「TUFT/几何框架能否供给胶球谱与 f0 混合」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0179_胶球质量谱攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0179_胶球质量谱攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0179_glueball_spectrum",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_experimental": {k: str(v) for k, v in g1.items()},
            "E2_lattice_ratios": {k: str(v) for k, v in g2.items()},
            "E3_mixing_central": {k: (str(v) if v is not None else None)
                                  for k, v in g3.items()},
            "E4_scan": [{k: (str(v) if v is not None else None)
                         for k, v in r.items()} for r in scan],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0179 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
