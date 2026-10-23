# -*- coding: utf-8 -*-
"""
attack_C0198_WIMP热遗迹攻破_2026-10-21.py
独立复算：母册 T300「WIMP 热遗迹密度与热平均截面 ⟨σv⟩」· 热退耦冻出（freeze-out）

母册 T300（原文照录）：
  | T300 | WIMP 热遗迹密度与热平均截面 ⟨σv⟩ | 热退耦 | C1,C2 |
      ◐ C0139：⟨σv⟩=1.906429e-26 cm³/s 落 WIMP 窗口 |

定位：本项由 D2 总账 B 级升级为 A 级（前置 C0139/C0184 已攻破满足）。
承接 C0139（⟨σv⟩=1.906429e-26 cm³/s 反解、落 WIMP 窗口=「巧合非推导」）
与 C0184（WIMP SI 核散射排除 45.5×）读数。本册**不采信自报**，用标准冻出算术
独立复核同一组读数，并对 TUFT/几何框架判定"是否供给 WIMP 热退耦或遗迹密度"。

把"WIMP 热遗迹密度与 ⟨σv⟩"压缩成五条可复核读数：

  E1 冻结温度核算：T_f ≃ m_χ/x_f（x_f≈20–25），m_χ∈{10,100,1000} GeV 扫点精算。
  E2 ⟨σv⟩ 反解复核（本册核心）：C0139 读数 1.906429e-26 cm³/s 的冻出方程独立复核，
     + x_f 自洽校核（Kolb-Turner 冻出公式）+ 量级对照（≈3e-26 cm³/s 热遗迹基准）。
  E3 遗迹密度 Ω_χh² 对 ⟨σv⟩ 摆动：⟨σv⟩∈[1e-27,1e-25] 扫点下 Ω_χh² 反比核算。
  E4 热遗迹机制供给检查：TUFT 是否供给 WIMP 热退耦或遗迹密度（无）。
  E5 裁定：结构性负面（对 TUFT/几何框架），撞 C1/C2（母册登记）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：所有数值均为标准暗物质冻出算术复核；TUFT 已注销（C0133）；
严禁把标准物理结果写成 TUFT 预测/修正。外部宇宙学参数（Planck 2018）只引用不复算。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部常数与观测值（只引用不复算，注明来源） ----------
M_PL = Decimal("1.220910e19")            # 约化 Planck 质量 GeV（CODATA/PDG）
G_STAR = Decimal("80")                   # 冻结时相对论自由度 g_*（典型弱标度，Kolb-Turner）
X_F = Decimal("20")                       # m_χ/T_f，C0139 取值；教科书区间 20–25
GEVM2_TO_CM2 = Decimal("0.3894e-27")     # 1 GeV⁻² = 0.3894 mb = 0.3894e-27 cm²（PDG）
C_CM_S = Decimal("2.99792458e10")        # 光速 cm/s
OMEGA_C_H2 = Decimal("0.1200")           # Planck 2018 Ω_c h²（只引用）
C0139_SIGMAV_CMS = Decimal("1.906429e-26")  # C0139 反解读数（本册引用复核对象）
G_CHI = Decimal("2")                     # Dirac 费米子内部自由度 g_χ
KT_COEF = Decimal("0.038")               # Kolb-Turner 冻出公式系数
WIMP_BENCHMARK = Decimal("3e-26")        # 热遗迹 ⟨σv⟩ 典型量级基准（教科书 ~3e-26 cm³/s）


def e1_freeze_temp():
    """E1：T_f ≃ m_χ/x_f 扫点，x_f ∈ {20,25}。"""
    masses = [Decimal("10"), Decimal("100"), Decimal("1000")]
    xfs = [Decimal("20"), Decimal("25")]
    rows = []
    for m in masses:
        row = {"m_chi_GeV": str(m)}
        for xf in xfs:
            row["Tf_x%s_GeV" % str(xf)] = str(m / xf)
        rows.append(row)
    return rows


def e2_sigmav_recheck():
    """E2：⟨σv⟩ 反解复核（本册核心）。

    标准冻出方程（Kolb-Turner 式）：
        Ω h² ≈ (1.07e9 GeV⁻¹ · x_f) / (√g_* · M_Pl · ⟨σv⟩[GeV⁻²])
    反解：
        ⟨σv⟩[GeV⁻²] = (1.07e9 · x_f) / (√g_* · M_Pl · Ω h²)
    换算：1 GeV⁻² × c = 0.3894e-27 cm² × 2.9979e10 cm/s = 1.1674e-17 cm³/s。
    """
    K = Decimal("1.07e9") * X_F / (G_STAR.sqrt() * M_PL)   # Ω h² = K/⟨σv⟩[GeV⁻²]
    sigmav_gev2 = K / OMEGA_C_H2                            # GeV⁻²
    conv = C_CM_S * GEVM2_TO_CM2                            # cm³/s per GeV⁻²
    sigmav_cms = sigmav_gev2 * conv                         # cm³/s
    # 与 C0139 读数相对偏差
    dev = abs(sigmav_cms - C0139_SIGMAV_CMS) / C0139_SIGMAV_CMS
    # x_f 自洽校核（Kolb-Turner）：m_χ=100 GeV 处
    #   x_f = ln[A] - 1/2 ln[ln[A]]，A = 0.038 (g_χ/√g_*) M_Pl m_χ ⟨σv⟩[GeV⁻²]
    m_test = Decimal("100")
    A = KT_COEF * (G_CHI / G_STAR.sqrt()) * M_PL * m_test * sigmav_gev2
    lnA = A.ln()
    xf_self = lnA - Decimal("0.5") * lnA.ln()
    # 量级对照：与教科书 ~3e-26 cm³/s 基准比
    ratio_bench = sigmav_cms / WIMP_BENCHMARK
    return {
        "K_dimensionless": str(K),
        "conv_cm3s_per_GeV-2": str(conv),
        "sigmav_GeV_minus2": str(sigmav_gev2),
        "sigmav_cm3_s": str(sigmav_cms),
        "c0139_reading_cm3_s": str(C0139_SIGMAV_CMS),
        "rel_dev_vs_c0139": str(dev),
        "xf_self_consistent_at_100GeV": str(xf_self),
        "wimp_benchmark_cm3_s": str(WIMP_BENCHMARK),
        "ratio_vs_benchmark": str(ratio_bench),
        "reproduces_c0139_within_1pct": dev < Decimal("0.01"),
        "xf_self_in_20_25_range": (Decimal("20") < xf_self < Decimal("25")),
    }


def e3_omega_scan():
    """E3：Ω_χh² 对 ⟨σv⟩ 摆动，⟨σv⟩∈[1e-27,1e-25] 扫点。"""
    K = Decimal("1.07e9") * X_F / (G_STAR.sqrt() * M_PL)
    conv = C_CM_S * GEVM2_TO_CM2
    sv_list = [Decimal("1e-27"), Decimal("3e-27"), Decimal("1e-26"),
               C0139_SIGMAV_CMS, Decimal("3e-26"), Decimal("1e-25")]
    rows = []
    for sv in sv_list:
        sv_gev2 = sv / conv
        omega = K / sv_gev2
        rows.append({"sigmav_cm3_s": str(sv), "omega_chi_h2": str(omega)})
    # 锚点核验
    anchor_sv_gev2 = C0139_SIGMAV_CMS / conv
    anchor_omega = K / anchor_sv_gev2
    anchor_dev = abs(anchor_omega - OMEGA_C_H2) / OMEGA_C_H2
    # 过闭（overclose）判定：Ω h² > 1
    overclose = [r for r in rows if Decimal(r["omega_chi_h2"]) > Decimal("1")]
    return {"rows": rows,
            "anchor_omega_h2": str(anchor_omega),
            "anchor_rel_dev_vs_0p12": str(anchor_dev),
            "anchor_matches_target_within_1pct": anchor_dev < Decimal("0.01"),
            "overclose_points": [r["sigmav_cm3_s"] for r in overclose]}


def e4_tuft_supply():
    """E4：TUFT/几何框架对 WIMP 热退耦/遗迹密度的供给。"""
    return {
        "has_wimp_particle_state": False,       # C0139 E4：挠率零程、无稳定中性粒子载体
        "has_thermal_decoupling_dynamics": False,  # 无冻出 Boltzmann 方程动力学
        "has_relic_density_prediction": False,   # 无 Ω_χh² 第一性预测
        "has_annihilation_cross_section": False,  # 无 ⟨σv⟩ 输入（C0184 E4）
        "cited": ("C0139 E4（挠率零程、无稳定中性粒子载体）；"
                  "C0184 E4（无粒子态/无散射截面/无核子矩阵元）；"
                  "C0133（TUFT 已注销）"),
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0198 · WIMP 热遗迹密度与热平均截面 ⟨σv⟩（T300 · 热退耦冻出）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_freeze_temp()
    w("\n[E1] 冻结温度核算：T_f ≃ m_χ/x_f（x_f≈20–25），m_χ 扫点")
    w("  m_χ (GeV) | T_f (x_f=20) GeV | T_f (x_f=25) GeV")
    for r in g1:
        w("  %-9s | %-15s | %s" % (r["m_chi_GeV"], r["Tf_x20_GeV"], r["Tf_x25_GeV"]))
    w("  => T_f 落在 GeV 量级（0.4–50 GeV），与弱标度 WIMP 冻出温度一致；")
    w("     x_f 提高（20→25）使 T_f 下移 ~20%，对 m_χ 线性缩放。")
    entries.append(("E1", "T_f=m_χ/x_f 扫点：m=10/100/1000 GeV ⇒ T_f=0.4–50 GeV（x_f=20–25）",
                    "PASS", "标准冻出算术；x_f 教科书区间 20–25"))

    # ---- E2 ----
    g2 = e2_sigmav_recheck()
    w("\n[E2] ⟨σv⟩ 反解复核（本册核心，复核 C0139 读数）")
    w("  冻出方程：Ω h² = K/⟨σv⟩[GeV⁻²]，K = (1.07e9·x_f)/(√g_*·M_Pl) = %s" % g2["K_dimensionless"])
    w("  换算系数：1 GeV⁻²·c = %s cm³/s" % g2["conv_cm3s_per_GeV-2"])
    w("  由 Ω_c h²=%s 反解 ⇒ ⟨σv⟩ = %s GeV⁻² = %s cm³/s"
      % (OMEGA_C_H2, g2["sigmav_GeV_minus2"], g2["sigmav_cm3_s"]))
    w("  C0139 读数 = %s cm³/s；本册复核相对偏差 = %s ⇒ 复现（<1%%）= %s"
      % (g2["c0139_reading_cm3_s"], g2["rel_dev_vs_c0139"], g2["reproduces_c0139_within_1pct"]))
    w("  x_f 自洽校核（Kolb-Turner，m_χ=100 GeV）⇒ x_f,self = %s（区间 20–25）= %s"
      % (g2["xf_self_consistent_at_100GeV"], g2["xf_self_in_20_25_range"]))
    w("  量级对照：与教科书热遗迹基准 %s cm³/s 比 = %s（同量级 O(1)）"
      % (g2["wimp_benchmark_cm3_s"], g2["ratio_vs_benchmark"]))
    w("  => 独立复算确认 C0139 的 ⟨σv⟩=1.906429e-26 cm³/s 落 WIMP 窗口；")
    w("     这是把弱标度质量+弱耦合**凑**出正确 Ω h² 的数值巧合（C0139 已判「巧合非推导」）。")
    entries.append(("E2", "⟨σv⟩ = %s cm³/s 复现 C0139（偏差 %s），x_f,self=%s 落 20–25，"
                    "与 3e-26 基准同量级" % (g2["sigmav_cm3_s"], g2["rel_dev_vs_c0139"],
                                             g2["xf_self_consistent_at_100GeV"]),
                    "PASS", "标准冻出方程独立复核；C0139 读数引用对照"))

    # ---- E3 ----
    g3 = e3_omega_scan()
    w("\n[E3] 遗迹密度 Ω_χh² 对 ⟨σv⟩ 摆动（反比核算）")
    w("  ⟨σv⟩ (cm³/s) | Ω_χ h²")
    for r in g3["rows"]:
        w("  %-14s | %s" % (r["sigmav_cm3_s"], r["omega_chi_h2"]))
    w("  锚点核验：⟨σv⟩=C0139 读数 ⇒ Ω h² = %s（目标 %s，相对偏差 %s）= %s"
      % (g3["anchor_omega_h2"], OMEGA_C_H2, g3["anchor_rel_dev_vs_0p12"],
         g3["anchor_matches_target_within_1pct"]))
    w("  过闭点（Ω h²>1）：%s" % g3["overclose_points"])
    w("  => Ω_χh² ∝ 1/⟨σv⟩：截面小 10×→遗迹密度大 ~19×（过闭宇宙）；")
    w("     截面大 10×→遗迹密度小 ~5×（欠闭）。WIMP 窗口窄（~1e-27~1e-25 cm³/s）即此反比所致。")
    entries.append(("E3", "Ω h² ∝ 1/⟨σv⟩：1e-27→过闭（Ω~2.3）、锚点→0.12、1e-25→欠闭（~0.023）",
                    "PASS", "标准冻出反比扫点；锚点偏差 %s" % g3["anchor_rel_dev_vs_0p12"]))

    # ---- E4 ----
    g4 = e4_tuft_supply()
    w("\n[E4] 热遗迹机制供给检查：TUFT 是否供给 WIMP 热退耦/遗迹密度")
    w("  有 WIMP 粒子态：%s" % g4["has_wimp_particle_state"])
    w("  有热退耦（冻出）动力学：%s" % g4["has_thermal_decoupling_dynamics"])
    w("  有遗迹密度 Ω_χh² 预测：%s" % g4["has_relic_density_prediction"])
    w("  有湮灭截面 ⟨σv⟩ 输入：%s" % g4["has_annihilation_cross_section"])
    w("  引用：%s" % g4["cited"])
    w("  => TUFT/几何框架对 WIMP 无粒子态、无冻出动力学、无 ⟨σv⟩、无 Ω_χh² 供给 = zero。")
    entries.append(("E4", "TUFT 热遗迹供给 0：无粒子态/无冻出动力学/无 ⟨σv⟩/无 Ω 预测",
                    "PASS", "承接 C0139 E4 / C0184 E4 / C0133"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  WIMP 热遗迹问题被精确翻译成两件事：(a) 存在一枚新稳定中性粒子（m_χ 外部输入）；")
    w("  (b) 其热退耦湮灭截面 ⟨σv⟩ 须落在窄窗口 ~1e-27~1e-25 cm³/s（E3 反比摆动）。")
    w("  本册独立复核：C0139 的 ⟨σv⟩=1.906429e-26 cm³/s 复现（偏差<1%），x_f,self≈22 落 20–25，")
    w("  与教科书 3e-26 基准同量级——但这是把弱标度质量+弱耦合凑对 Ω h² 的**数值巧合**，非推导。")
    w("  C0184 已判：30 GeV 规范耦合 WIMP 被零信号排除 ~45.5 倍（截面-丰度张力）。")
    w("  TUFT 无 WIMP 粒子态、无冻出供给（E4）；m_χ 与 ⟨σv⟩ 全是外部输入。")
    w("  => **T300 结构性负面（对 TUFT/几何框架）**；按母册登记撞 C1（粒子内容）/ C2（绝对标度）。")
    entries.append(("E5", "T300 结构性负面：WIMP 热遗迹依赖新粒子+热退耦动力学（m_χ、⟨σv⟩外部输入），"
                    "TUFT 无供给", "PASS", "撞 C1/C2（母册 T300 登记）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "E1 T_f(100 GeV, x_f=20) = 5 GeV（冻出温度量级）",
         Decimal([r for r in g1 if r["m_chi_GeV"] == "100"][0]["Tf_x20_GeV"]) == Decimal("5")),
        ("G2", "E2 本册复核 ⟨σv⟩ 复现 C0139 读数（相对偏差 < 1%）",
         g2["reproduces_c0139_within_1pct"]),
        ("G3", "E2 x_f 自洽校核落教科书区间 20–25", g2["xf_self_in_20_25_range"]),
        ("G4", "E3 锚点 ⟨σv⟩=C0139 读数反算 Ω h² ≈ 0.12（偏差 < 1%）",
         g3["anchor_matches_target_within_1pct"]),
        ("G5", "E3 小截面 1e-27 过闭（Ω h² > 1）",
         Decimal([r for r in g3["rows"] if r["sigmav_cm3_s"] in ("1e-27", "1E-27")][0]["omega_chi_h2"]) > 1),
        ("G6", "E4 TUFT 对 WIMP 热遗迹供给 = 0",
         (g4["has_wimp_particle_state"] is False
          and g4["has_thermal_decoupling_dynamics"] is False
          and g4["has_relic_density_prediction"] is False)),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0198 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解释 WIMP 热遗迹；所有数值均为标准暗物质冻出算术复核；")
    w("  Planck 2018 宇宙学参数与基本常数只引用不复算；TUFT 已注销（C0133）；")
    w("  严禁把标准物理结果写成 TUFT 预测/修正。裁的是「TUFT/几何框架能否供给 WIMP 热退耦与遗迹密度」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0198_WIMP热遗迹攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0198_WIMP热遗迹攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    import json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0198_wimp_thermal_relic",
            "mother_row": "T300 WIMP热遗迹密度与热平均截面<σv> 热退耦 C1,C2",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_freeze_temp": g1,
            "E2_sigmav_recheck": g2,
            "E3_omega_scan": g3,
            "E4_tuft_supply": g4,
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0198 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
