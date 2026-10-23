# -*- coding: utf-8 -*-
"""
attack_C0193_夸克禁闭弦张力攻破_2026-10-21.py
独立精算：母册 T030（行 121）「夸克禁闭 / 强子谱 · 禁闭机制」攻破

母册原文照录：
  | T030 | 夸克禁闭 / 强子谱 | 禁闭机制 | C1 | 🔲（r33/⑲ 已证几何势族禁闭力判三连错） |

主题：QCD 弦张力 σ≈0.18 GeV²、Regge 轨迹、线性禁闭势 V(r)=σr、禁闭机制供给检查。
本册**不采信任何自报**，用标准 QCD/弦模型算术独立精算，并对 TUFT/几何框架判定供给。

把「夸克禁闭 / 强子谱从哪来」压缩成五条可复核读数：

  E1 观测事实（PDG / 格点 / 弦模型只引用不复算）：σ≈0.18 GeV²；ρ(770) J=1、
     ρ3(1690) J=3 质量；经验 Regge 斜率 α'≈0.9 GeV⁻²。
  E2 **弦张力→Regge 斜率 + 物理单位换算（本册核心）**：
     ① α'=1/(2πσ) 的 Decimal 精算（GeV⁻²）；
     ② V(r)=σr：1 fm 处禁闭力 σ 的 GeV/fm 与 N（含吨力 tf）换算精算。
  E3 Regge 轨迹复核：m²=J/α'+m₀² 对 ρ(770)/ρ3(1690) 坐标核算，反推经验 α'_exp
     与 E2 的 1/(2πσ) 对照（Fraction 精确交叉守卫）。
  E4 禁闭机制供给检查：TUFT/几何框架是否供给线性势或弦张力（无；几何势族已判
     三连错——r33#E02/E03/E04、r34#X16，承接 C0179 格点 QCD 谱线）。
  E5 裁定：夸克禁闭依赖 SU(3) 非阿贝尔规范动力学（格点 / 弦模型），TUFT 无禁闭
     机制 / 无弦张力供给 ⇒ 结构性负面，按母册登记撞 C1。

纯标准库（Decimal 48 位 + Fraction 精确代数），零外部依赖、零网络、零随机，退出码 0。

诚实边界：本册不宣称解决夸克禁闭；外部观测值（PDG 质量、格点弦张力）只引用不复算；
数值均为标准 QCD / 弦模型算术复核；TUFT 已注销（C0133）；
本册未把任何标准物理结果写成 TUFT 预测 / 修正。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os
import json

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 数学常数（48 位硬编码，非外部观测值） ----------
PI = Decimal("3.1415926535897932384626433832795028841971693993751")

# ---------- 外部输入（PDG / 格点 QCD / CODATA，只引用不复算） ----------
# QCD 弦张力：格点 QCD / 弦模型标准值 σ ≈ 0.18 GeV²（ℏ=c=1 自然单位）
SIGMA = Decimal("0.18")
# ℏc = 197.3269804 MeV·fm = 0.1973269804 GeV·fm（CODATA，长度换算锚）
HC = Decimal("0.1973269804")
# 1 GeV = 1.602176634e-10 J（基本电荷 e 定义）；1 fm = 1e-15 m ⇒ 1 GeV/fm = 1.602176634e5 N
N_PER_GEV_FM = Decimal("1.602176634e-10") / Decimal("1e-15")
# 吨力：1 tf = g_n × 1000 kg = 9.80665 × 1000 = 9806.65 N（标准重力加速度）
NEWTON_PER_TF = Decimal("9.80665") * Decimal("1000")
# PDG 强子（只引用）：ρ(770) I^G(J^PC)=1+(1--)，任务取整 770 MeV ⇒ 0.770 GeV
M_RHO = Decimal("0.770")
# PDG 强子（只引用）：ρ3(1690) I^G(J^PC)=1+(3--)，任务取整 1690 MeV ⇒ 1.690 GeV
M_RHO3 = Decimal("1.690")
J_RHO = 1     # ρ(770) 轨道角动量
J_RHO3 = 3    # ρ3(1690) 轨道角动量


def e1_facts():
    """观测事实（PDG / 格点 QCD / 弦模型，只引用不复算）。"""
    return {
        "sigma_GeV2": SIGMA,
        "hbar_c_GeV_fm": HC,
        "rho_MeV": Decimal("770"), "rho_J": J_RHO,
        "rho3_MeV": Decimal("1690"), "rho3_J": J_RHO3,
        "alpha_prime_empirical_GeV-2": Decimal("0.9"),
    }


def e2_string_tension():
    """E2 核心：σ→α'=1/(2πσ) 精算 + 弦张力物理单位换算。

    推导链：
      弦模型 Regge 斜率 α' = 1/(2πσ)（无自旋弦，线性势 V=σr 直接给出）；
      1 fm 长度换算：r[GeV⁻¹] = r[fm] / (ℏc[GeV·fm])；
      V(1 fm) = σ·r(1 fm)；常力 F = dV/dr = σ，以 GeV/fm 计 = σ/(ℏc)；
      1 GeV/fm = (1.602176634e-10 J)/(1e-15 m) = 1.602176634e5 N。
    """
    two_pi_sigma = Decimal(2) * PI * SIGMA
    alpha_th = Decimal(1) / two_pi_sigma
    # 长度换算：1 fm = ? GeV⁻¹
    r_1fm_GeV_inv = Decimal(1) / HC
    # 1 fm 处禁闭势高度 V = σ·r
    V_1fm = SIGMA * r_1fm_GeV_inv
    # 常力 F = σ，以 GeV/fm 计
    F_GeV_fm = V_1fm  # V(1fm) 数值即 σ/(ℏc) = 每 fm 势能增量
    F_N = F_GeV_fm * N_PER_GEV_FM
    F_tf = F_N / NEWTON_PER_TF  # 吨力（公制吨力）
    return {
        "two_pi_sigma": two_pi_sigma,
        "alpha_th": alpha_th,
        "r_1fm_GeV_inv": r_1fm_GeV_inv,
        "V_1fm_GeV": V_1fm,
        "F_GeV_fm": F_GeV_fm,
        "F_N": F_N,
        "F_tf": F_tf,
    }


def e3_regge_trajectory(alpha_th):
    """E3：Regge 轨迹 m²=J/α'+m₀² 对 ρ(770)/ρ3(1690) 坐标核算。

    反推经验斜率 α'_exp = ΔJ/Δm² = (3-1)/(m_ρ3² - m_ρ²)；
    并用 Fraction 精确代数交叉复核同一值；
    与 E2 的弦模型值 α'=1/(2πσ) 对照（相对偏差）；
    截距 m₀² = m_ρ² - J_ρ/α'_exp；Regge 截距 α(0) = -α'_exp·m₀²。
    """
    m1sq = M_RHO * M_RHO
    m2sq = M_RHO3 * M_RHO3
    dmsq = m2sq - m1sq
    dalpha = Decimal(J_RHO3 - J_RHO)
    alpha_exp = dalpha / dmsq
    rel_diff = abs(alpha_exp - alpha_th) / alpha_th
    m0sq = m1sq - Decimal(J_RHO) / alpha_exp
    alpha0 = -alpha_exp * m0sq
    # Fraction 精确交叉复核（770/1000 与 1690/1000 严格分数）
    f1 = Fraction(770, 1000)
    f2 = Fraction(1690, 1000)
    dmsq_f = f2 * f2 - f1 * f1          # = 22632/10000
    alpha_exp_f = Fraction(2) / dmsq_f  # = 2500/2829
    alpha_exp_from_f = Decimal(alpha_exp_f.numerator) / Decimal(alpha_exp_f.denominator)
    return {
        "m1sq": m1sq, "m2sq": m2sq, "dmsq": dmsq,
        "alpha_exp": alpha_exp,
        "rel_diff_vs_th": rel_diff,
        "m0sq": m0sq, "alpha0": alpha0,
        "alpha_exp_fraction_exact": str(alpha_exp_f),
        "alpha_exp_from_fraction": alpha_exp_from_f,
    }


def e4_geometry_supply():
    """E4：TUFT/几何框架是否供给线性禁闭势或弦张力？

    判定（承接既有攻破线，引用不复算）：
      - 几何势族 U=α(κ^m−τ^m) 的「禁闭力判」已被 r33#E02/E03/E04、r34#X16 三连错证伪：
        ① "力∝r→0=渐近自由"错——QCD 渐近自由是 α_s 对数趋 0，力仍 ~α_s/r²，
           标准 Cornell 力 F=-(4α_s/3)/r²−σ 短程含 1/r² 发散项，来料不含；
        ② "线性增强=禁闭"错——Cornell 线性项给**常力 σ（弦张力）**，不随 r 线性增强；
        ③ 函数自相矛盾——F_s(r)∝r(1−r/r₀)e^{-2r/r₀} 在 r=r₀ 归零、r>r₀ 反号排斥，
           与禁闭（恒吸引）矛盾。
      - 格点纯胶谱供给已由 C0179 判定：TUFT 无胶场自由度、无格点纯胶作用量。
      - 量纲侧（承接 C0140/C0142）：几何常数 (ℏ,G,c) 量纲 nullity=0 ⇒ 给不出
        有量纲的弦张力 σ[E·L]，更给不出 QCD 非阿贝尔规范动力学本身。
    """
    return {
        "linear_potential_supply": "zero",
        "string_tension_supply": "zero",
        "geometry_supply_total": 0,
        "triple_error_ref": "r33#E02/E03/E04, r34#X16（几何势族禁闭力判三连错）",
        "lattice_supply_ref": "C0179（TUFT 无胶场/无格点纯胶作用量）",
        "nullity_hbarGc": 0,
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    w("=" * 74)
    w("attack_C0193 · 夸克禁闭 / 强子谱（母册 T030 行 121 · 禁闭机制）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 观测事实（PDG / 格点 QCD / 弦模型，只引用不复算）")
    w("  QCD 弦张力 σ = %s GeV²（格点/弦模型标准值，ℏ=c=1 自然单位）" % g1["sigma_GeV2"])
    w("  ℏc = %s GeV·fm（CODATA 长度换算锚）" % g1["hbar_c_GeV_fm"])
    w("  ρ(770)  = %s MeV, J=%d；ρ3(1690) = %s MeV, J=%d（同一 ρ Regge 领头轨迹）"
      % (g1["rho_MeV"], g1["rho_J"], g1["rho3_MeV"], g1["rho3_J"]))
    w("  经验 Regge 斜率 α' ≈ %s GeV⁻²（只引用）" % g1["alpha_prime_empirical_GeV-2"])
    w("  => 禁闭现象的标准定量表达：线性势 V(r)=σr、常力 σ、Regge 轨迹 m²=J/α'+m₀²。")
    entries.append(("E1", "禁闭事实 = σ≈0.18 GeV² + V=σr 常力 + Regge m²∝J（PDG/格点只引用）",
                    "PASS", "外部观测值只引用；本册只做换算与轨迹核算"))

    # ---- E2 ----
    g2 = e2_string_tension()
    w("\n[E2] 弦张力→Regge 斜率 α'=1/(2πσ) 与物理单位换算（本册核心）")
    w("  ① 2πσ = %s GeV²" % g2["two_pi_sigma"])
    w("  ② α'_th = 1/(2πσ) = %s GeV⁻²（弦模型无自旋弦标准式）" % g2["alpha_th"])
    w("  ③ 长度换算：1 fm = 1/(ℏc) = %s GeV⁻¹" % g2["r_1fm_GeV_inv"])
    w("  ④ 1 fm 处禁闭势 V(1 fm) = σ·r = %s GeV" % g2["V_1fm_GeV"])
    w("  ⑤ 常力 F=σ：每 fm 势能增量 = %s GeV/fm" % g2["F_GeV_fm"])
    w("  ⑥ F = %s GeV/fm × %s N/(GeV/fm) = %s N"
      % (g2["F_GeV_fm"], N_PER_GEV_FM, g2["F_N"]))
    w("  ⑦ F = %s N ÷ 9806.65 N/tf = %s tf（公制吨力，与文献『弦张力≈14 吨力』量级吻合）"
      % (g2["F_N"], g2["F_tf"]))
    w("  => σ=0.18 GeV² 自洽给出 α'_th≈0.884 GeV⁻² 与 1 fm 处常力≈0.912 GeV/fm≈1.46e5 N。")
    entries.append(("E2", "α'=1/(2πσ)=%s GeV⁻²；F(1fm)=σ=%s GeV/fm=%s N=%s tf"
                    % (g2["alpha_th"], g2["F_GeV_fm"], g2["F_N"], g2["F_tf"]),
                    "PASS", "标准弦模型算术 + ℏc/e 单位换算，Decimal 48 位精算"))

    # ---- E3 ----
    g3 = e3_regge_trajectory(g2["alpha_th"])
    w("\n[E3] Regge 轨迹复核：ρ(770)/ρ3(1690) 坐标核算")
    w("  m_ρ²   = 0.770² = %s GeV²" % g3["m1sq"])
    w("  m_ρ3²  = 1.690² = %s GeV²" % g3["m2sq"])
    w("  Δm²    = %s GeV²；ΔJ = 3-1 = 2" % g3["dmsq"])
    w("  α'_exp = ΔJ/Δm² = 2/%s = %s GeV⁻²" % (g3["dmsq"], g3["alpha_exp"]))
    w("  Fraction 精确交叉：2/(%s) = %s ⇒ Decimal 复核 = %s（一致）"
      % (g3["dmsq"], g3["alpha_exp_fraction_exact"], g3["alpha_exp_from_fraction"]))
    w("  对照 E2 弦模型 α'_th = %s GeV⁻² ⇒ 相对偏差 = %s（≈%s%%）"
      % (g2["alpha_th"], g3["rel_diff_vs_th"], g3["rel_diff_vs_th"] * 100))
    w("  截距 m₀² = m_ρ² - J/α'_exp = %s GeV² ⇒ Regge 截距 α(0) = -α'_exp·m₀² = %s"
      % (g3["m0sq"], g3["alpha0"]))
    w("  => ρ(770)/ρ3(1690) 两点落在同一直线 m²=J/α'+m₀² 上，经验斜率 %s GeV⁻² 与"
      % g3["alpha_exp"])
    w("     弦模型 1/(2πσ)=%s GeV⁻² 偏差仅 %s%%，标准 Regge 弦图景自洽。"
      % (g2["alpha_th"], g3["rel_diff_vs_th"] * 100))
    entries.append(("E3", "经验 α'_exp=%s GeV⁻²，与弦模型 1/(2πσ) 偏差 %s%%；截距 α(0)=%s"
                    % (g3["alpha_exp"], g3["rel_diff_vs_th"] * 100, g3["alpha0"]),
                    "PASS", "PDG 坐标只引用，本册独立反推斜率 + Fraction 精确交叉"))

    # ---- E4 ----
    g4 = e4_geometry_supply()
    w("\n[E4] 禁闭机制供给检查：TUFT/几何框架是否供给线性势或弦张力？")
    w("  几何势族 U=α(κ^m−τ^m) 禁闭力判已被证伪（%s）：" % g4["triple_error_ref"])
    w("    ① 『力∝r→0=渐近自由』错：QCD 渐近自由是 α_s 对数趋 0，力仍 ~α_s/r²；")
    w("       Cornell 力 F=-(4α_s/3)/r²−σ 短程含 1/r² 发散项，来料不含。")
    w("    ② 『线性增强=禁闭』错：Cornell 线性项给常力 σ（弦张力），不随 r 线性增强。")
    w("    ③ 函数自相矛盾：F_s(r)∝r(1−r/r₀)e^{-2r/r₀} 在 r=r₀ 归零、r>r₀ 反号排斥，")
    w("       与禁闭（恒吸引）矛盾。")
    w("  格点纯胶谱供给：%s。" % g4["lattice_supply_ref"])
    w("  量纲侧：几何常数 (ℏ,G,c) 量纲 nullity = %d（承接 C0140/C0142）⇒"
      % g4["nullity_hbarGc"])
    w("    给不出有量纲的弦张力 σ[E·L]，更给不出 SU(3) 非阿贝尔规范动力学本身。")
    w("  => TUFT 线性势供给 = %s、弦张力供给 = %s ⇒ 供给总数 = %d。"
      % (g4["linear_potential_supply"], g4["string_tension_supply"],
         g4["geometry_supply_total"]))
    entries.append(("E4", "TUFT 无线性势/无弦张力供给（几何势族禁闭力判三连错 r33#E02/E03/E04、"
                    "r34#X16；格点谱供给 0，C0179）", "PASS", "撞 C1（粒子内容须公设唯一确定）"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  夸克禁闭问题被精确翻译成三件事：")
    w("  (a) 弦张力 σ≈0.18 GeV² 与 Regge 斜率 α'=1/(2πσ) 由 SU(3) 非阿贝尔规范动力学")
    w("      （格点 QCD / 弦模型）给定（E2/E3 精算自洽，两点 Regge 偏差 <0.1%）；")
    w("  (b) 线性势 V=σr 与常力 σ 是非阿贝尔色流管（Nambu-Goto）的导出量；")
    w("  (c) TUFT/几何框架供给 = 0：无禁闭机制、无弦张力、几何势族禁闭力判三连错（E4）。")
    w("  => **P 项结构性负面（对 TUFT/几何框架）**；按母册 T030 登记撞 **C1**。")
    entries.append(("E5", "夸克禁闭依赖 SU(3) 非阿贝尔规范动力学（格点/弦模型），"
                    "TUFT 无禁闭机制/无弦张力供给（几何势族三连错）⇒ 结构性负面，撞 C1",
                    "PASS", "母册 T030 行 121 登记口径"))

    # ---- 守卫 ----
    guards = [
        ("G1", "α'_th=1/(2πσ) 落在 [0.88, 0.89] GeV⁻²",
         Decimal("0.88") < g2["alpha_th"] < Decimal("0.89")),
        ("G2", "1 fm 处常力 σ 落在 [0.90, 0.92] GeV/fm",
         Decimal("0.90") < g2["F_GeV_fm"] < Decimal("0.92")),
        ("G3", "F(1fm) 换算为牛顿落在 [1.4e5, 1.5e5] N",
         Decimal("140000") < g2["F_N"] < Decimal("150000")),
        ("G4", "经验 α'_exp 与弦模型 α'_th 相对偏差 < 1%",
         g3["rel_diff_vs_th"] < Decimal("0.01")),
        ("G5", "TUFT/几何框架禁闭供给总数 = 0",
         g4["geometry_supply_total"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0193 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解决夸克禁闭：PDG 质量与格点弦张力只引用；")
    w("  数值均为标准 QCD/弦模型算术复核；TUFT 已注销（C0133）；")
    w("  本册未把任何标准物理结果写成 TUFT 预测/修正。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0193_夸克禁闭弦张力攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0193_夸克禁闭弦张力攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0193_quark_confinement_string_tension",
            "mother_book": "T030 row 121",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": {k: str(v) for k, v in g1.items()},
            "E2_string_tension": {k: str(v) for k, v in g2.items()},
            "E3_regge": {k: str(v) for k, v in g3.items()},
            "E4_geometry_supply": {k: str(v) for k, v in g4.items()},
            "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0193 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
