# -*- coding: utf-8 -*-
"""
attack_C0197_ADMX高频轴子探测攻破_2026-10-21.py
独立复算：母册 T289「ADMX-HF 扫描 KSVZ/DFSZ 轴子窗口」· PQ 轴子 CDM · 撞 C1,C5 · ◐ 收口

定位：母册 T289（行 421）；本项由 D2 总账 B 级升 A 级（前置 T029 轴子线 C0196 已攻破满足）。
承接：C0196（轴子窗口参数盒：m_a=5.7μeV–14.25meV、KSVZ/DFSZ 扫点，刚完成）与
      C0138（轴子窗口 f_a=4×10⁸–10¹² GeV、m_πf_πz 独立算 m_a=5.787643μeV@10¹²GeV）。

把「ADMX-HF 高频段轴子暗物质直接探测」压缩成四条可复核读数 + 供给账单：

  E1 外部事实只引用：m_a–f_a 标度律、α_em、gγ(KSVZ/DFSZ)、ADMX 常规带 [1,40]μeV、
     ADMX-HF 高频目标带 [40,200]μeV、实测 Ω_DM h²=0.12。
  E2 **ADMX-HF 高频窗口核算（本册核心）**：m_a∈[40,200]μeV → f_a 换算 + g_aγγ 扫点
     （m_a=5.7μeV·(10¹²GeV/f_a)；g_aγγ=gγ·α_em/(2πf_a)）。
  E3 KSVZ/DFSZ 耦合带：两模型 g_aγγ 数值差核算（同 f_a 下 |g_KSVZ|/|g_DFSZ|=0.97/0.36，
     符号相反——色荷比 E/N 是模型输入）。
  E4 探测灵敏度 vs 暗物质丰度：ADMX 已扫/排除区与 QCD 轴子带（m_a 窗口）重叠核算
     ——探测覆盖 vs 未覆盖区。
  E5 探测供给检查 + 裁定：TUFT 是否供给轴子暗物质或探测窗口（无）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：数值均为标准轴子探测（ADMX 类腔体 / KSVZ-DFSZ）算术与实验现状复核；
TUFT 已注销（C0133），严禁把标准物理结果写成 TUFT 预测/修正；
外部常数（α_em、gγ、实验带、Ω_DM h²）只引用不复算。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（只引用不复算） ----------
# 标准轴子质量-标度关系（C0196/C0138）：m_a = 5.7 μeV · (10^12 GeV / f_a)
MUEV_REF = Decimal("5.7")            # @ f_a = 10^12 GeV
FA_REF = Decimal("1000000000000")     # 1e12 GeV
# CODATA 精细结构常数（C0196 引用值，逐字沿用）
ALPHA = Decimal("0.00729735252050556058262062523716395691643071893517")
PI = Decimal("3.1415926535897932384626433832795028841971693993751")  # 引用常数
# 色荷比耦合系数（KSVZ / DFSZ，标准模型值，C0196 逐字沿用）
GAMMA_KSVZ = Decimal("-0.97")
GAMMA_DFSZ = Decimal("0.36")
# QCD 轴子 m_a 窗口（C0196 E2：f_a∈[4×10^8,10^12]GeV ⇒ m_a∈[5.7,14250]μeV）
M_WIN_LO = Decimal("5.7")            # μeV（f_a=10^12 GeV）
M_WIN_HI = Decimal("14250")          # μeV（f_a=4×10^8 GeV = 14.25 meV）
# ADMX 实验带（C0196 E3：常规腔扫 [1,40] μeV；本项任务口径 ADMX-HF 高频目标带）
ADMX_LOW = Decimal("1")              # μeV
ADMX_CONV_HI = Decimal("40")         # μeV（常规带/HF 带交界）
ADMX_HF_HI = Decimal("200")          # μeV（ADMX-HF 高频目标带上沿）
OMEGA_DM_H2 = Decimal("0.12")        # Planck 实测暗物质丰度（C0196 引用）


def fa_of_muev(m_uev: Decimal) -> Decimal:
    """m_a(μeV) -> f_a(GeV)：f_a = 5.7e12 / m_a(μeV)。"""
    return MUEV_REF * FA_REF / m_uev


def ga_gammagamma(gamma: Decimal, fa: Decimal) -> Decimal:
    """g_aγγ = gγ · α_em / (2π f_a)，单位 GeV⁻¹。"""
    return gamma * ALPHA / (Decimal(2) * PI * fa)


def e1_external_facts():
    return {
        "m_a_relation": "m_a = 5.7 μeV · (10^12 GeV / f_a)",
        "alpha_em": ALPHA,
        "pi": PI,
        "g_gamma_ksvz": GAMMA_KSVZ,
        "g_gamma_dfsz": GAMMA_DFSZ,
        "qcd_window_ueV": (M_WIN_LO, M_WIN_HI),
        "admx_conv_band_ueV": (ADMX_LOW, ADMX_CONV_HI),
        "admx_hf_band_ueV": (ADMX_CONV_HI, ADMX_HF_HI),
        "omega_dm_h2": OMEGA_DM_H2,
    }


def e2_admx_hf_window():
    """本册核心：ADMX-HF 高频带 m_a∈[40,200]μeV 的 f_a 换算 + g_aγγ 扫点。"""
    scan = [Decimal(x) for x in ("40", "60", "80", "100", "120", "150", "200")]
    rows = []
    for m in scan:
        fa = fa_of_muev(m)
        gk = ga_gammagamma(GAMMA_KSVZ, fa)
        gd = ga_gammagamma(GAMMA_DFSZ, fa)
        rows.append({"m_uev": m, "fa_GeV": fa, "g_ksvz": gk, "g_dfsz": gd})
    # 带边
    fa_lo = fa_of_muev(ADMX_CONV_HI)   # m=40 μeV -> f_a 高边
    fa_hi = fa_of_muev(ADMX_HF_HI)     # m=200 μeV -> f_a 低边
    return {
        "rows": rows,
        "edge_m40_fa": fa_lo,
        "edge_m200_fa": fa_hi,
        "hf_band_fa_range": (fa_hi, fa_lo),   # f_a∈[2.85e10, 1.425e11] GeV
    }


def e3_ksvz_dfsz_band():
    """两模型 g_aγγ 数值差：同 f_a 下比值与符号。"""
    ratio = GAMMA_KSVZ / GAMMA_DFSZ          # -0.97/0.36
    abs_ratio = abs(ratio)
    # 在带边 m=40μeV（f_a=1.425e11GeV）处的绝对差
    fa = fa_of_muev(ADMX_CONV_HI)
    gk = ga_gammagamma(GAMMA_KSVZ, fa)
    gd = ga_gammagamma(GAMMA_DFSZ, fa)
    abs_diff = abs(gk - gd)
    return {
        "g_gamma_ratio_ksvz_over_dfsz": ratio,
        "abs_ratio": abs_ratio,
        "same_fa_gk": gk,
        "same_fa_gd": gd,
        "same_fa_abs_diff": abs_diff,
        "sign": "KSVZ 负 / DFSZ 正（色荷比 E/N 符号相反）",
    }


def e4_detection_overlap():
    """ADMX 已扫/排除区与 QCD 轴子 m_a 窗口重叠核算。"""
    scanned_lo = ADMX_LOW
    scanned_hi = ADMX_HF_HI               # 常规 [1,40] + HF [40,200] = [1,200] μeV
    cover_lo = max(M_WIN_LO, scanned_lo)
    cover_hi = min(M_WIN_HI, scanned_hi)
    cover_span = cover_hi - cover_lo
    win_span = M_WIN_HI - M_WIN_LO
    uncovered_lo = cover_hi
    uncovered_hi = M_WIN_HI
    uncovered_span = uncovered_hi - uncovered_lo
    frac_covered = cover_span / win_span
    frac_uncovered = uncovered_span / win_span
    return {
        "scanned_band_ueV": (scanned_lo, scanned_hi),
        "cover_interval_ueV": (cover_lo, cover_hi),
        "cover_span_ueV": cover_span,
        "window_span_ueV": win_span,
        "uncovered_interval_ueV": (uncovered_lo, uncovered_hi),
        "uncovered_span_ueV": uncovered_span,
        "frac_covered": frac_covered,
        "frac_uncovered": frac_uncovered,
    }


def e5_supply_verdict():
    """TUFT 供给检查：是否供给轴子暗物质 / 探测窗口。"""
    return {
        "tuft_supplies_axion_dm": False,      # TUFT 已注销 C0133，无轴子场
        "tuft_supplies_detection_window": False,  # 无 f_a 标度、无 PQ 对称（C0196 E5）
        "detection_inputs_external": "PQ 全局对称 + KSVZ/DFSZ 色荷比 gγ（E/N）+ f_a 标度",
        "new_inputs": 3,   # U(1)_PQ(C1) + f_a VEV(C2) + gγ 模型选择(C1/C5)
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0197 · ADMX-HF 高频段轴子暗物质直接探测（母册 T289 · 撞 C1,C5 · ◐收口）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_external_facts()
    w("\n[E1] 外部事实（只引用不复算）")
    w("  m_a 标度律 = %s（承接 C0196/C0138）" % g1["m_a_relation"])
    w("  α_em = %s（CODATA，C0196 逐字引用）；π = %s" % (fv(ALPHA, "20f"), fv(PI, "20f")))
    w("  gγ = %s（KSVZ）/ %s（DFSZ）；g_aγγ = gγ·α_em/(2π f_a)"
      % (GAMMA_KSVZ, GAMMA_DFSZ))
    w("  QCD 轴子 m_a 窗口 = [%s, %s] μeV（C0196 E2，即 5.7 μeV – 14.25 meV）"
      % (M_WIN_LO, M_WIN_HI))
    w("  ADMX 常规腔扫带 = [%s, %s] μeV（C0196 E3）；ADMX-HF 高频目标带 = [%s, %s] μeV"
      % (ADMX_LOW, ADMX_CONV_HI, ADMX_CONV_HI, ADMX_HF_HI))
    w("  实测 Ω_DM h² = %s（Planck，C0196 引用）" % OMEGA_DM_H2)
    entries.append(("E1", "m_a–f_a 标度律、α_em、gγ(KSVZ/DFSZ)、QCD 窗口[5.7,14250]μeV、"
                    "ADMX 常规带[1,40]+HF 目标带[40,200]μeV、Ω_DM h²=0.12", "PASS",
                    "外部常数/实验带只引用；本册只做换算与重叠判定"))

    # ---- E2 ----
    g2 = e2_admx_hf_window()
    w("\n[E2] ADMX-HF 高频窗口核算（本册核心，Decimal 48 位）")
    w("  m_a (μeV)   f_a (GeV)      g_aγγ KSVZ (GeV⁻¹)  g_aγγ DFSZ (GeV⁻¹)")
    for r in g2["rows"]:
        w("  %-11s %-13s %-17s %s"
          % (fv(r["m_uev"], "0f"), fv(r["fa_GeV"], "3e"), fv(r["g_ksvz"], "6e"),
             fv(r["g_dfsz"], "6e")))
    w("  带边：m_a=40 μeV ⇒ f_a=%s GeV；m_a=200 μeV ⇒ f_a=%s GeV"
      % (fv(g2["edge_m40_fa"], "4e"), fv(g2["edge_m200_fa"], "4e")))
    w("  => HF 带 m_a∈[40,200]μeV 对应 f_a∈[%s, %s] GeV，"
      % (fv(g2["edge_m200_fa"], "3e"), fv(g2["edge_m40_fa"], "3e")))
    w("     全落在 C0138/C0196 QCD 轴子窗口 [4×10⁸, 10¹²] GeV 内。")
    entries.append(("E2", "HF 带 m_a∈[40,200]μeV ⇒ f_a∈[2.85e10,1.425e11]GeV；"
                    "g_aγγ KSVZ 从 %s 到 %s GeV⁻¹（DFSZ 同标度反号）"
                    % (fv(g2["rows"][0]["g_ksvz"], "3e"), fv(g2["rows"][-1]["g_ksvz"], "3e")),
                    "PASS", "m_a=5.7μeV·(10¹²/f_a)；g=gγ·α/(2πf_a)，Decimal 48 位精算"))

    # ---- E3 ----
    g3 = e3_ksvz_dfsz_band()
    w("\n[E3] KSVZ/DFSZ 耦合带数值差（同 f_a 下）")
    w("  |g_KSVZ|/|g_DFSZ| = |%s|/|%s| = %s；符号相反（%s）"
      % (GAMMA_KSVZ, GAMMA_DFSZ, fv(g3["abs_ratio"], "6f"), g3["sign"]))
    w("  m_a=40μeV(f_a=%sGeV) 处：g_KSVZ=%s、g_DFSZ=%s，绝对差 %s GeV⁻¹"
      % (fv(g2["edge_m40_fa"], "3e"), fv(g3["same_fa_gk"], "6e"),
         fv(g3["same_fa_gd"], "6e"), fv(g3["same_fa_abs_diff"], "6e")))
    w("  => 两模型在 g_aγγ–m_a 平面上分居于 g=0 两侧、相距 ~2.69 倍；")
    w("     gγ(E/N) 本身是模型输入（KSVZ/DFSZ 公设），非实验可由几何导出。")
    entries.append(("E3", "|g_KSVZ|/|g_DFSZ|=%s（同 f_a），符号相反；gγ(E/N) 是外部模型输入"
                    % fv(g3["abs_ratio"], "4f"), "PASS",
                    "比值=0.97/0.36 直接精算；色荷比符号承接 C0196 G3"))

    # ---- E4 ----
    g4 = e4_detection_overlap()
    w("\n[E4] 探测灵敏度 vs 暗物质丰度：已扫区与 QCD 窗口重叠核算")
    w("  已扫/排除带 = [%s, %s] μeV（常规 [1,40] + HF [40,200]）"
      % (g4["scanned_band_ueV"][0], g4["scanned_band_ueV"][1]))
    w("  QCD 窗口 = [%s, %s] μeV ⇒ 重叠覆盖区间 = [%s, %s] μeV，跨度 %s μeV"
      % (M_WIN_LO, M_WIN_HI, g4["cover_interval_ueV"][0], g4["cover_interval_ueV"][1],
         fv(g4["cover_span_ueV"], "1f")))
    w("  QCD 窗口总跨度 = %s μeV；覆盖占比 = %s" % (fv(g4["window_span_ueV"], "1f"),
        fv(g4["frac_covered"], "4%")))
    w("  未覆盖区间 = [%s, %s] μeV（=200μeV–14.25meV），跨度 %s μeV，占比 %s"
      % (g4["uncovered_interval_ueV"][0], g4["uncovered_interval_ueV"][1],
         fv(g4["uncovered_span_ueV"], "1f"), fv(g4["frac_uncovered"], "4%")))
    w("  => 即便 ADMX-HF 推到 200 μeV，QCD 轴子质量窗口的 ~%s 仍未被腔体探测覆盖"
      % fv(g4["frac_uncovered"], "1%"))
    entries.append(("E4", "已扫带[1,200]μeV 与 QCD 窗口[5.7,14250]μeV 重叠仅 [%s,%s]μeV；"
                    "覆盖 %s / 未覆盖 %s（200μeV–14.25meV 空白）"
                    % (g4["cover_interval_ueV"][0], g4["cover_interval_ueV"][1],
                       fv(g4["frac_covered"], "2%"), fv(g4["frac_uncovered"], "2%")),
                    "PASS", "实验带只引用；重叠/占比本册 Decimal 精算"))

    # ---- E5 ----
    g5 = e5_supply_verdict()
    w("\n[E5] 探测供给检查 + 裁定（对 TUFT/几何框架）")
    w("  TUFT 供给轴子暗物质？ %s（TUFT 已注销 C0133；承接 C0196 E5：无轴子场）"
      % g5["tuft_supplies_axion_dm"])
    w("  TUFT 供给探测窗口？ %s（无 PQ 全局对称、无 f_a VEV 破缺标度）"
      % g5["tuft_supplies_detection_window"])
    w("  探测依赖外部输入：%s（共 %d 枚新输入）" % (g5["detection_inputs_external"], g5["new_inputs"]))
    w("  E2–E4 全部 m_a/f_a/g/覆盖占比均为标准轴子探测（ADMX 腔体 / KSVZ-DFSZ）算术与")
    w("  实验现状复核，与 TUFT 无关——TUFT 不供给轴子、不供给探测窗口、不供给耦合模型。")
    w("  => **T289 结构性负面（对 TUFT/几何框架）**；按母册登记撞 C1（粒子内容须公设）/C5（可检验性：")
    w("     探测窗口与耦合全外部输入，TUFT 无可检验预言），◐ 收口。")
    entries.append(("E5", "轴子探测依赖外部 PQ 对称 + KSVZ/DFSZ 耦合 + f_a 标度；"
                    "TUFT 无轴子/无探测窗口供给 ⇒ 结构性负面，按母册 T289 登记撞 C1/C5",
                    "PASS", "TUFT 已注销 C0133；承接 C0138 E5/C0196 E5"))

    # ---- 守卫 ----
    guards = [
        ("G1", "m_a=40μeV ⇒ f_a=1.425e11GeV，落在 QCD 窗口[4e8,1e12]内",
         g2["edge_m40_fa"] == Decimal("1.425e11") and Decimal("4e8") <= g2["edge_m40_fa"] <= Decimal("1e12")),
        ("G2", "m_a=200μeV ⇒ f_a=2.85e10GeV，落在 QCD 窗口内",
         g2["edge_m200_fa"] == Decimal("2.85e10") and Decimal("4e8") <= g2["edge_m200_fa"] <= Decimal("1e12")),
        ("G3", "|g_KSVZ|/|g_DFSZ|=0.97/0.36≈2.694，符号相反",
         g3["abs_ratio"] == Decimal("97") / Decimal("36") and g3["same_fa_gk"] < 0 < g3["same_fa_gd"]),
        ("G4", "g 随 1/f_a：m=200μeV 处 |g|=5× m=40μeV 处（f_a 小 5 倍）",
         abs(g2["rows"][-1]["g_ksvz"]) == abs(g2["rows"][0]["g_ksvz"]) * Decimal(5)),
        ("G5", "QCD 窗口覆盖占比 < 5%（未覆盖 > 95%，HF 仅扫窗口边缘）",
         g4["frac_covered"] < Decimal("0.05")),
        ("G6", "TUFT 供给轴子=0、供给探测窗口=0（结构性负面判据）",
         (not g5["tuft_supplies_axion_dm"]) and (not g5["tuft_supplies_detection_window"])),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0197 guard failed"

    w("\n[诚实边界]")
    w("  不宣称解决任何物理难题；外部常数（α_em、gγ、ADMX 带、Ω_DM h²）只引用不复算；")
    w("  数值均为标准轴子探测（ADMX 腔体/KSVZ-DFSZ）算术与实验现状复核，")
    w("  TUFT 已注销（C0133），严禁写成 TUFT 预测/修正；")
    w("  红线不变：已攻破=对 TUFT/几何框架结构性负面闭合；有预测且对=0/22；")
    w("  UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0197_ADMX高频轴子探测攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0197_ADMX高频轴子探测攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0197_ADMX_HF_axion_direct_detection",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_inputs": {
                "m_a_relation": g1["m_a_relation"],
                "alpha_em": str(ALPHA), "pi": str(PI),
                "g_gamma_ksvz": str(GAMMA_KSVZ), "g_gamma_dfsz": str(GAMMA_DFSZ),
                "qcd_window_ueV": [str(M_WIN_LO), str(M_WIN_HI)],
                "admx_conv_band_ueV": [str(ADMX_LOW), str(ADMX_CONV_HI)],
                "admx_hf_band_ueV": [str(ADMX_CONV_HI), str(ADMX_HF_HI)],
                "omega_dm_h2": str(OMEGA_DM_H2),
            },
            "E2_admx_hf_scan": [
                {"m_uev": str(r["m_uev"]), "fa_GeV": str(r["fa_GeV"]),
                 "g_ksvz": str(r["g_ksvz"]), "g_dfsz": str(r["g_dfsz"])}
                for r in g2["rows"]
            ],
            "E2_edges": {"m40_fa": str(g2["edge_m40_fa"]),
                         "m200_fa": str(g2["edge_m200_fa"])},
            "E3_ksvz_dfsz": {
                "abs_ratio": str(g3["abs_ratio"]),
                "ratio_signed": str(g3["g_gamma_ratio_ksvz_over_dfsz"]),
                "same_fa_gk": str(g3["same_fa_gk"]),
                "same_fa_gd": str(g3["same_fa_gd"]),
                "same_fa_abs_diff": str(g3["same_fa_abs_diff"]),
            },
            "E4_overlap": {
                "cover_interval_ueV": [str(g4["cover_interval_ueV"][0]),
                                       str(g4["cover_interval_ueV"][1])],
                "cover_span_ueV": str(g4["cover_span_ueV"]),
                "window_span_ueV": str(g4["window_span_ueV"]),
                "uncovered_interval_ueV": [str(g4["uncovered_interval_ueV"][0]),
                                           str(g4["uncovered_interval_ueV"][1])],
                "uncovered_span_ueV": str(g4["uncovered_span_ueV"]),
                "frac_covered": str(g4["frac_covered"]),
                "frac_uncovered": str(g4["frac_uncovered"]),
            },
            "E5_supply": {k: str(v) for k, v in g5.items()},
            "guards": [{"id": gid, "desc": desc, "ok": bool(ok)} for gid, desc, ok in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0197 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
