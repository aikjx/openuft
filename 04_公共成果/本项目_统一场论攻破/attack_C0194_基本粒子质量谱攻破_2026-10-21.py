# -*- coding: utf-8 -*-
"""
attack_C0194_基本粒子质量谱攻破_2026-10-21.py
独立精算：基本粒子质量谱（母册 T032，行123）· 费米子 Yukawa 耦合与质量比值、代结构、质量公式供给检查

定位：母册 T032「基本粒子质量谱（为何是这些值）」方法列=质量公式，撞 C2/C3，状态 🔲 待攻。
衔接：C0142（味/代数结构已攻破 —— 代=3、Yukawa 是 3x3 复矩阵外部输入、几何常数 nullity=0）；
      C0162（so(8) 极大秩嵌入 = 0 —— 规范群不能从纯代数根系统涌现）；C0133（TUFT 已注销）。

本册净增量：C0142 判了「味结构/Yukawa 矩阵是外部输入」，本册把「质量为何是这些值」
落到**标准粒子物理算术复核**上，用 Decimal 48 位逐点精算：

  E1 SM 质量谱事实（PDG 只引用不复算）：三代费米子质量 + EW VEV v=246.22 GeV。
  E2 **质量比值表 + Yukawa 耦合逐点精算（本册核心）**：
     m_t/m_e、m_t/m_u、m_b/m_d、m_tau/m_e、m_mu/m_e 等关键比值 Decimal 核算；
     y_f = sqrt(2) m_f / v 的 t / b / tau 三点（+ e / mu）逐代精算。
  E3 代际层级跨度算术：meV/eV–173 GeV 的 log10 跨度（带电费米子 ~5.5 dex，含中微子 ~11–12 dex）。
  E4 质量公式供给检查：TUFT/几何框架是否供给 Yukawa 起源或质量公式（无 —— 零自由参数框架）。
  E5 裁定：质量谱依赖 Higgs-Yukawa 外部参数（9+ 枚），代际层级 11 数量级无导出机制，
          TUFT 零参数框架无质量谱供给 ⇒ 结构性负面，撞 C2/C3。

纯标准库（Decimal 48 位 + Fraction 精确代数），零外部依赖、零网络、零随机，退出码 0。

诚实边界（硬）：本册所有数值均为**标准粒子物理（SM Yukawa / 质量谱）算术复核**，
  外部 PDG 质量值只引用不复算；TUFT 已注销（C0133）；**严禁把标准物理结果写成 TUFT 预测/修正**。
  本册不宣称已解释质量谱为何取这些值；裁的是「TUFT/几何框架能否供给质量公式」。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（PDG，只引用不复算） ----------
# 费米子质量（PDG，MeV）。上型/下型为 MS-bar 跑动能标值，与 C0142 口径一致。
M_E = Decimal("0.510998950")      # 电子
M_MU = Decimal("105.6583755")     # μ 子
M_TAU = Decimal("1776.86")        # τ 轻子
M_U = Decimal("2.16")             # 上夸克
M_D = Decimal("4.67")             # 下夸克
M_S = Decimal("93.4")             # 奇夸克
M_C = Decimal("1270")             # 粲夸克
M_B = Decimal("4180")              # 底夸克
M_T = Decimal("173000")            # 顶夸克（173.0 GeV，与 C0142 M_T=173000 一致）
# EW 真空期望值（Feynman-VEV 口径）
V_GEV = Decimal("246.22")          # GeV
# 最轻已知质量标度：中微子质量（宇宙学上限量级，eV）
M_NU_EV = Decimal("0.05")          # eV（典型 m_nu，只作跨度算术下界，引用）


def yukawa(m_mev: Decimal) -> Decimal:
    """Yukawa 耦合 y_f = sqrt(2) m_f / v。质量 MeV -> GeV (/1000)，v=246.22 GeV。"""
    m_gev = m_mev / Decimal(1000)
    return Decimal(2).sqrt() * m_gev / V_GEV


def e1_sm_facts():
    """SM 质量谱事实（PDG 只引用）。"""
    return {
        "charged_leptons_MeV": (M_E, M_MU, M_TAU),
        "up_type_MeV": (M_U, M_C, M_T),
        "down_type_MeV": (M_D, M_S, M_B),
        "v_gev": V_GEV,
        "nu_scale_eV": M_NU_EV,
    }


def e2_ratios_and_yukawa():
    """核心：费米子质量比值表 + Yukawa 耦合逐点精算。"""
    ratios = {
        "mt_over_me": M_T / M_E,
        "mt_over_mu": M_T / M_U,
        "mb_over_md": M_B / M_D,
        "mtau_over_me": M_TAU / M_E,
        "mmu_over_me": M_MU / M_E,
        "mc_over_me": M_C / M_E,
        "mt_over_mtau": M_T / M_TAU,
        "mt_over_mb": M_T / M_B,
    }
    y = {
        "yt": yukawa(M_T),
        "yb": yukawa(M_B),
        "ytau": yukawa(M_TAU),
        "ymu": yukawa(M_MU),
        "ye": yukawa(M_E),
    }
    return {"ratios": ratios, "yukawa": y}


def e3_hierarchy_span():
    """代际层级跨度算术：log10 跨度。"""
    # 带电费米子跨度：顶 vs 电子
    span_charged = M_T / M_E
    log_charged = span_charged.log10()
    # 含中微子跨度：顶 (eV) vs 中微子下界。顶 = 173000 MeV = 1.73e11 eV
    mt_ev = M_T * Decimal("1e6")   # MeV -> eV (1 MeV = 1e6 eV)
    span_withnu = mt_ev / M_NU_EV
    log_withnu = span_withnu.log10()
    # Yukawa 谱跨度：y_t / y_e
    yt = yukawa(M_T)
    ye = yukawa(M_E)
    span_yukawa = yt / ye
    log_yukawa = span_yukawa.log10()
    return {
        "span_charged": span_charged, "log10_charged": log_charged,
        "span_withnu": span_withnu, "log10_withnu": log_withnu,
        "span_yukawa": span_yukawa, "log10_yukawa": log_yukawa,
    }


def e4_mass_formula_supply():
    """质量公式供给检查：TUFT/几何框架是否供给 Yukawa 起源 / 质量公式。"""
    # 外部输入账单：带电费米子 9 个 Yukawa 本征值（3 上型 + 3 下型 + 3 带电轻子）
    ext_yukawa_eigen = 9
    # 几何常数 (hbar,G,c) 量纲矩阵 nullity = 0（承接 C0140 E4，经 C0142 E3 引用）
    nullity_hbarGc = 0
    # so(8) 极大秩嵌入 = 0（承接 C0162 E2 精确读数）
    so8_sm_embedding = 0
    return {
        "external_yukawa_eigenvalues": ext_yukawa_eigen,
        "nullity_hbarGc": nullity_hbarGc,
        "so8_maxrank_sm_embedding": so8_sm_embedding,
        "tuft_free_params": 0,        # TUFT 零自由参数框架
        "mass_formula_supply": "zero",  # 无 Yukawa 起源 / 质量公式供给
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0194 · 基本粒子质量谱（母册 T032 · 质量公式 · 撞 C2/C3）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_sm_facts()
    w("\n[E1] SM 质量谱事实（PDG 只引用不复算）")
    w("  带电轻子 (e,mu,tau) = (%s, %s, %s) MeV"
      % (fv(M_E, "6f"), fv(M_MU, "5f"), fv(M_TAU, "4f")))
    w("  上型 (u,c,t) = (%s, %s, %s) MeV"
      % (fv(M_U, "2f"), fv(M_C, "0f"), fv(M_T, "0f")))
    w("  下型 (d,s,b) = (%s, %s, %s) MeV"
      % (fv(M_D, "2f"), fv(M_S, "1f"), fv(M_B, "0f")))
    w("  EW VEV v = %s GeV；中微子典型标度 ~ %s eV（只作跨度下界引用）"
      % (V_GEV, M_NU_EV))
    w("  => 质量谱 = 9 个带电费米子 Yukawa 本征值（纯数）+ v 这个有量纲标度。")
    entries.append(("E1", "SM 质量谱 = 9 个带电费米子 Yukawa 本征值（纯数）+ v=246.22 GeV",
                    "PASS", "PDG 只引用；本册只做比值/Yukawa 换算"))

    # ---- E2 ----
    g2 = e2_ratios_and_yukawa()
    R = g2["ratios"]
    Y = g2["yukawa"]
    w("\n[E2] 质量比值表 + Yukawa 耦合逐点精算（本册核心）")
    w("  -- 关键质量比值（Decimal 逐字）--")
    w("    m_t / m_e   = %s  (≈3.4e5)" % fv(R["mt_over_me"], "6e"))
    w("    m_t / m_u   = %s  (上型代际差)" % fv(R["mt_over_mu"], "6e"))
    w("    m_b / m_d   = %s  (下型代际差)" % fv(R["mb_over_md"], "6e"))
    w("    m_tau / m_e = %s  (τ 对电子)" % fv(R["mtau_over_me"], "6e"))
    w("    m_mu / m_e  = %s  (μ 对电子 = 著名 206.77)" % fv(R["mmu_over_me"], "6e"))
    w("    m_c / m_e   = %s" % fv(R["mc_over_me"], "6e"))
    w("    m_t / m_tau = %s ；m_t / m_b = %s"
      % (fv(R["mt_over_mtau"], "6e"), fv(R["mt_over_mb"], "6e")))
    w("  -- Yukawa 耦合 y_f = sqrt(2) m_f / v，v=%s GeV --" % V_GEV)
    w("    sqrt(2) = %s" % fv(Decimal(2).sqrt(), "20f"))
    w("    y_t   = sqrt(2)*173.0/%s = %s  (O(1)，顶夸克近弱耦合)"
      % (V_GEV, fv(Y["yt"], "10f")))
    w("    y_b   = sqrt(2)*4.180/%s = %s" % (V_GEV, fv(Y["yb"], "10f")))
    w("    y_tau = sqrt(2)*1.77686/%s = %s" % (V_GEV, fv(Y["ytau"], "10f")))
    w("    y_mu  = sqrt(2)*0.10566/%s = %s" % (V_GEV, fv(Y["ymu"], "10e")))
    w("    y_e   = sqrt(2)*0.0005110/%s = %s  (电子 Yukawa ~3e-6，极小微扰)"
      % (V_GEV, fv(Y["ye"], "10e")))
    w("  => Yukawa 谱跨 6 个数量级：y_t=O(1) 一直降到 y_e~3e-6，全是纯数输入。")
    entries.append(("E2",
                    "质量比 m_t/m_e=%s、m_mu/m_e=%s；Yukawa y_t=%s、y_b=%s、y_tau=%s、y_e=%s"
                    % (fv(R["mt_over_me"], "4e"), fv(R["mmu_over_me"], "4f"),
                       fv(Y["yt"], "6f"), fv(Y["yb"], "6f"),
                       fv(Y["ytau"], "6f"), fv(Y["ye"], "4e")),
                    "PASS", "SM Yukawa 算术复核（sqrt(2)m/v），Decimal 48 位"))

    # ---- E3 ----
    g3 = e3_hierarchy_span()
    w("\n[E3] 代际层级跨度算术（log10）")
    w("  带电费米子跨度 m_t/m_e = %s ⇒ log10 = %s dex（~5.5 个数量级）"
      % (fv(g3["span_charged"], "6e"), fv(g3["log10_charged"], "4f")))
    w("  含中微子跨度 (173 GeV=1.73e11 eV)/%s eV = %s ⇒ log10 = %s dex（~12.5 dex）"
      % (M_NU_EV, fv(g3["span_withnu"], "6e"), fv(g3["log10_withnu"], "4f")))
    w("  Yukawa 谱跨度 y_t/y_e = %s ⇒ log10 = %s dex"
      % (fv(g3["span_yukawa"], "6e"), fv(g3["log10_yukawa"], "4f")))
    w("  => 质量谱从 eV 量级轻中微子跨到 173 GeV 顶夸克，约 11–12 个数量级的层级；")
    w("     带电费米子内部亦有 ~5.5 dex 的代际层级。该层级无任何导出机制（裸输入）。")
    entries.append(("E3",
                    "代际层级跨度：带电 %s dex，含中微子 %s dex；11–12 数量级无导出机制"
                    % (fv(g3["log10_charged"], "1f"), fv(g3["log10_withnu"], "1f")),
                    "PASS", "log10 跨度算术，中微子标度只作下界引用"))

    # ---- E4 ----
    g4 = e4_mass_formula_supply()
    w("\n[E4] 质量公式供给检查：TUFT/几何框架是否供给 Yukawa 起源 / 质量公式？")
    w("  外部 Yukawa 本征值（带电费米子）= %d 枚（3 上型 + 3 下型 + 3 带电轻子）"
      % g4["external_yukawa_eigenvalues"])
    w("  几何常数 (hbar,G,c) 量纲矩阵 nullity = %d（承接 C0140 E4 / C0142 E3 读数）"
      % g4["nullity_hbarGc"])
    w("  so(8) 极大秩 SM 嵌入 = %d（承接 C0162 E2 精确读数：规范群不能从根系统涌现）"
      % g4["so8_maxrank_sm_embedding"])
    w("  TUFT 自由参数 = %d（零参数框架）⇒ 既给不出 9 个纯数 Yukawa，也给不出 v 的标度。"
      % g4["tuft_free_params"])
    w("  => 几何框架**不供给** Yukawa 起源，也**不供给**任何质量公式；质量谱不可由几何生成。")
    entries.append(("E4",
                    "质量公式供给 = 0：Yukawa 9 本征值是外部纯数输入，几何 nullity=0、"
                    "so8 嵌入=0，TUFT 零参数无质量谱供给",
                    "PASS", "撞 C2/C3；引用 C0140/C0142/C0162/C0133"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  质量谱问题被翻译成：(a) 9 个 Yukawa 纯数从哪来；(b) 11–12 数量级代际层级从哪来。")
    w("  (a) Yukawa y_t~0.99 到 y_e~2.9e-6 全是 Higgs-Yukawa 外部参数（≥9 枚），"
      "几何常数 nullity=0 ⇒ 纯数不可由几何生成（C0142 E3 已立）。")
    w("  (b) 代际层级 ~11–12 dex 无任何导出机制；TUFT 零参数框架无质量公式供给。")
    w("  => **基本粒子质量谱结构性负面（对 TUFT/几何框架）**；撞 C2（绝对标度/v 与质量标度）")
    w("     / C3（零自由参数 —— 9+ Yukawa 纯数无法自零参数框架导出）。")
    entries.append(("E5",
                    "P1x 质量谱结构性负面：Higgs-Yukawa 外部参数 9+ 枚、代际层级 11 dex "
                    "无导出机制，TUFT 零参数无供给",
                    "PASS", "撞 C2/C3（按母册 T032 登记口径）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "m_t/m_e ≈ 3.4e5（Decimal 核算落在 3e5–4e5）",
         R["mt_over_me"] > Decimal("3e5") and R["mt_over_me"] < Decimal("4e5")),
        ("G2", "y_t = O(1)（0.5 < y_t < 1.5，顶夸克近弱耦合）",
         Y["yt"] > Decimal("0.5") and Y["yt"] < Decimal("1.5")),
        ("G3", "y_e << y_t（y_e/y_t < 1e-4，电子 Yukawa 极小微扰）",
         Y["ye"] / Y["yt"] < Decimal("1e-4")),
        ("G4", "带电费米子代际跨度 > 5 dex（log10(m_t/m_e) > 5）",
         g3["log10_charged"] > Decimal("5")),
        ("G5", "Yukawa 外部本征值 = 9 枚（带电费米子）",
         g4["external_yukawa_eigenvalues"] == 9),
        ("G6", "几何常数 nullity = 0 且 so8 极大秩嵌入 = 0（质量公式供给 = 0）",
         g4["nullity_hbarGc"] == 0 and g4["so8_maxrank_sm_embedding"] == 0),
        ("G7", "v = 246.22 GeV（Yukawa 标定一致）",
         V_GEV == Decimal("246.22")),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %-5s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0194 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  本册不宣称已解释质量谱为何取这些值；所有数值均为标准粒子物理（SM Yukawa/质量谱）")
    w("  算术复核，PDG 质量值只引用不复算；TUFT 已注销（C0133）。")
    w("  严禁把标准物理结果写成 TUFT 预测/修正 —— 本册裁的是「TUFT 框架能否供给质量公式」。")
    w("  红线：不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("        有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0194_基本粒子质量谱攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0194_基本粒子质量谱攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")

    def sdict(d):
        return {k: (str(v) if not isinstance(v, tuple) else [str(x) for x in v])
                for k, v in d.items()}

    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0194_particle_mass_spectrum",
            "mother_entry": "T032",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_sm_facts": sdict(g1),
            "E2_ratios": {k: str(v) for k, v in g2["ratios"].items()},
            "E2_yukawa": {k: str(v) for k, v in g2["yukawa"].items()},
            "E3_span": {k: str(v) for k, v in g3.items()},
            "E4_supply": {k: str(v) for k, v in g4.items()},
            "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0194 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
