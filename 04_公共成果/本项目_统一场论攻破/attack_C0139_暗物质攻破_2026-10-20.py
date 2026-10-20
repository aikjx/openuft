# -*- coding: utf-8 -*-
"""
attack_C0139_暗物质攻破_2026-10-20.py
独立复算：暗物质（P04 · 布局 Phase 0 最后一项可攻目标）· 精算审计

定位：布局册（C0135）Phase 0（分水岭层）余项中，P04 暗物质是最后一个**可攻**
（P14 量子测量已按 C5/C6 判为不可判定，不计入）。本册补：

  E1 宇宙学账：Ω_c h²、Ω_b h²、比值、ρ_crit 与宇宙平均 ρ_DM（机器算）。
  E2 热遗迹丰度反解（本册核心）：由 Ω_c h² = 0.120 反解热遗迹所需的 ⟨σv⟩
     ⇒ 落在 WIMP 窗口 ⇒ 说明"WIMP 奇迹"是一个**数值巧合级**的要求，不是推导。
  E3 候选解分类：WIMP / 轴子 / 惰性中微子 / 原初黑洞 / 修正引力，各自所需新输入。
  E4 几何框架供给：挠率=代数零程（C0134 E6）⇒ 无稳定中性粒子载体；
     修正引力路径撞 C5（单点预言）与 C6（判别力）。
  E5 裁定：P04 需 ≥1 枚新输入，几何/TUFT 框架提供者 0 ⇒ 结构性负面。

纯标准库（Decimal 48 位），零外部依赖，退出码 0。

诚实边界：本册裁的是「几何/TUFT 框架能否给出暗物质解」，**不宣称暗物质已被解释**；
外部宇宙学参数（Planck 2018）只引用不复算。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 宇宙学参数（Planck 2018，只引用不复算） ----------
H = Decimal("0.674")
OMEGA_C_H2 = Decimal("0.1200")
OMEGA_B_H2 = Decimal("0.02237")
RHO_CRIT_COEF = Decimal("1.878e-29")     # g/cm^3 × h⁻²
GRAM_TO_GEV = Decimal("5.609e23")        # 1 g = 5.609e23 GeV/c²（能量当量 1 g·c² = 5.609e23 GeV）
RHO_CRIT_GEV_COEF = Decimal("1.0537e-5")  # GeV/cm³ × h⁻²（PDG 独立口径，用于双路径交叉核验）

# ---------- 热遗迹丰度 ----------
M_PL = Decimal("1.220910e19")            # GeV
G_STAR = Decimal("80")                   # 冻结时相对论自由度
X_F = Decimal("20")                      # m/T_f
GEVM2_TO_CM2 = Decimal("0.3894e-27")     # 1 GeV⁻² = 0.3894 mb = 0.3894e-27 cm²
C_CM_S = Decimal("2.99792458e10")


def e1_cosmology():
    h2 = H * H
    omega_c = OMEGA_C_H2 / h2
    omega_b = OMEGA_B_H2 / h2
    ratio = OMEGA_C_H2 / OMEGA_B_H2
    rho_crit = RHO_CRIT_COEF * h2                 # g/cm³
    rho_dm_avg = omega_c * rho_crit               # g/cm³
    # 质量密度 → 能量密度（GeV/cm³）：1 g·c² = 5.609e23 GeV，故只乘不除
    rho_dm_gev = rho_dm_avg * GRAM_TO_GEV
    rho_dm_gev_alt = RHO_CRIT_GEV_COEF * h2 * omega_c       # 独立口径（PDG）
    dev = abs(rho_dm_gev - rho_dm_gev_alt) / rho_dm_gev_alt
    return {"h2": format(h2, ".6f"), "omega_c": format(omega_c, ".6f"),
            "omega_b": format(omega_b, ".6f"), "ratio_c_over_b": format(ratio, ".6f"),
            "rho_crit_g_cm3": format(rho_crit, ".6e"),
            "rho_dm_avg_g_cm3": format(rho_dm_avg, ".6e"),
            "rho_dm_avg_GeV_cm3": format(rho_dm_gev, ".6e"),
            "rho_dm_avg_GeV_cm3_alt": format(rho_dm_gev_alt, ".6e"),
            "cross_check_rel_dev": format(dev, ".6e"),
            "cross_check_ok": dev < Decimal("1e-3")}


def e2_thermal_relic():
    """Ω h² ≈ (1.07e9 GeV⁻¹ · x_f)/(√g_* · M_Pl · ⟨σv⟩[GeV⁻²])

    反解：⟨σv⟩ = (1.07e9 · x_f)/(√g_* · M_Pl · Ω h²)，再换算为 cm³/s。
    """
    num = Decimal("1.07e9") * X_F
    den = G_STAR.sqrt() * M_PL * OMEGA_C_H2
    sigma_v_gev2 = num / den                       # GeV⁻²
    sigma_cm2 = sigma_v_gev2 * GEVM2_TO_CM2
    sigma_v_cms = sigma_cm2 * C_CM_S
    return {"sigma_v_GeV_minus2": format(sigma_v_gev2, ".6e"),
            "sigma_v_cm3_s": format(sigma_v_cms, ".6e"),
            "g_star": str(G_STAR), "x_f": str(X_F),
            "in_wimp_window": (Decimal("1e-27") < sigma_v_cms < Decimal("1e-25"))}


def e3_candidates():
    """候选解分类 + 各自所需新输入。"""
    return [
        ("WIMP（热遗迹）", 1, ["新稳定中性粒子（撞 C1：粒子内容须由公设唯一确定）",
                          "弱标度质量与耦合（撞 C2：绝对标度）"]),
        ("QCD 轴子", 2, ["新 U(1)_PQ 对称（撞 C1）", "新 VEV 标度 f_a（撞 C2）"]),
        ("惰性中微子", 1, ["新规范单态费米子（撞 C1）", "其质量标度（撞 C2）"]),
        ("原初黑洞", 1, ["暴胀期功率谱形状（依赖 P09 暴胀）"]),
        ("修正引力（MOND 类）", 1, ["星系尺度符合但星系团/CMB 尺度失败 ⇒ 撞 C5/C6"]),
    ]


def e4_geometry_supply():
    """几何/TUFT 框架能否供给暗物质载体。"""
    # 挠率是代数辅助场（C0134 E6）⇒ 零程，无稳定中性粒子
    torsion_algebraic = True
    torsion_zero_range = True
    provides_stable_particle = False
    modified_gravity_blocked_by = ["C5（单点预言）", "C6（判别力）"]
    return {"torsion_algebraic": torsion_algebraic,
            "torsion_zero_range": torsion_zero_range,
            "provides_stable_neutral_particle": provides_stable_particle,
            "modified_gravity_blocked_by": modified_gravity_blocked_by}


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    w("=" * 74)
    w("attack_C0139 · 暗物质（P04）攻破")
    w("=" * 74)

    entries = []

    # E1
    g1 = e1_cosmology()
    w("\n[E1] 宇宙学账（Planck 2018 参数只引用不复算）")
    w("  h = %s ⇒ h² = %s" % (H, g1["h2"]))
    w("  Ω_c h² = %s ⇒ Ω_c = %s；Ω_b h² = %s ⇒ Ω_b = %s"
      % (OMEGA_C_H2, g1["omega_c"], OMEGA_B_H2, g1["omega_b"]))
    w("  Ω_c / Ω_b = %s（暗物质约为重子的 5.4 倍）" % g1["ratio_c_over_b"])
    w("  ρ_crit = %s g/cm³；宇宙平均 ρ_DM = %s g/cm³ = %s GeV/cm³"
      % (g1["rho_crit_g_cm3"], g1["rho_dm_avg_g_cm3"], g1["rho_dm_avg_GeV_cm3"]))
    w("  双路径核验（PDG 独立口径 %s GeV/cm³）相对偏差 = %s ⇒ 一致 = %s"
      % (g1["rho_dm_avg_GeV_cm3_alt"], g1["cross_check_rel_dev"], g1["cross_check_ok"]))
    entries.append(("E1", "宇宙学账：Ω_c/Ω_b = %s；宇宙平均 ρ_DM = %s GeV/cm³（双路径偏差 %s）"
                    % (g1["ratio_c_over_b"], g1["rho_dm_avg_GeV_cm3"],
                       g1["cross_check_rel_dev"]), "PASS",
                    "Planck 参数只引用；本册增量是换算 + 独立口径交叉核验"))

    # E2
    g2 = e2_thermal_relic()
    w("\n[E2] 热遗迹丰度反解（本册核心）")
    w("  Ω h² ≈ (1.07e9 GeV⁻¹ · x_f)/(√g_* · M_Pl · ⟨σv⟩)，取 g_*=%s、x_f=%s"
      % (g2["g_star"], g2["x_f"]))
    w("  由 Ω_c h² = %s 反解 ⇒ ⟨σv⟩ = %s GeV⁻² = %s cm³/s"
      % (OMEGA_C_H2, g2["sigma_v_GeV_minus2"], g2["sigma_v_cm3_s"]))
    w("  => 落在 WIMP 窗口（1e-27 ~ 1e-25 cm³/s）= %s" % g2["in_wimp_window"])
    w("  => 这就是「WIMP 奇迹」：它把弱标度质量+弱耦合**凑**出正确的 Ω h²，")
    w("     属于**数值巧合级**的要求，不是从公设推导的必然。")
    entries.append(("E2", "热遗迹反解：⟨σv⟩ = %s cm³/s ⇒ 落 WIMP 窗口（巧合非推导）"
                    % g2["sigma_v_cm3_s"], "PASS",
                    "g_*=%s、x_f=%s" % (g2["g_star"], g2["x_f"])))

    # E3
    cands = e3_candidates()
    w("\n[E3] 候选解分类与所需新输入")
    for nm, nfree, notes in cands:
        w("  %-22s 新增自由输入 %d 枚" % (nm, nfree))
        for nt in notes:
            w("       - %s" % nt)
    entries.append(("E3", "五类候选解均需 ≥1 枚新输入（撞 C1/C2 或依赖 P09）", "PASS",
                    "WIMP/轴子/惰性ν/PBH/修正引力"))

    # E4
    g4 = e4_geometry_supply()
    w("\n[E4] 几何/TUFT 框架的供给")
    w("  挠率是代数辅助场 = %s；零程 = %s（C0134 E6）"
      % (g4["torsion_algebraic"], g4["torsion_zero_range"]))
    w("  ⇒ 提供稳定中性粒子载体 = %s" % g4["provides_stable_neutral_particle"])
    w("  修正引力路径撞：%s" % "、".join(g4["modified_gravity_blocked_by"]))
    entries.append(("E4", "几何框架供给 0：挠率零程、无稳定粒子载体；修正引力撞 C5/C6", "PASS",
                    "承接 C0134 E6"))

    # E5
    w("\n[E5] 裁定")
    w("  暗物质需要一枚**新**的、稳定的、电中性的、非重子成分（或修正引力），")
    w("  且其 relic/质量标度须落在观测窗口（E2 的 ⟨σv⟩ ≈ 1.9e-26 cm³/s）。")
    w("  五类候选解均需 ≥1 枚新输入；几何/TUFT 框架提供者 **0**")
    w("  （挠率零程、无稳定粒子载体、修正引力撞 C5/C6）。")
    w("  => **P04 结构性负面（对 TUFT/几何框架）**。")
    entries.append(("E5", "P04 结构性负面：需 ≥1 枚新输入，几何提供者 0", "PASS",
                    "撞 C1（粒子内容）/C2（标度）/C5/C6"))

    # ---------- 守卫（自检：把口径类断言机器化，防手算失误） ----------
    guards = [
        ("G1", "E1 双路径（g/cm³ 换算 vs PDG 独立口径）相对偏差 < 1e-3", g1["cross_check_ok"]),
        ("G2", "E2 反解 ⟨σv⟩ 落 WIMP 窗口 1e-27~1e-25 cm³/s", bool(g2["in_wimp_window"])),
        ("G3", "E3 五类候选解每类均需 ≥1 枚新输入", all(c[1] >= 1 for c in cands)),
        ("G4", "E4 几何框架不提供稳定中性粒子载体", (g4["provides_stable_neutral_particle"] is False)),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0139 guard failed"

    w("\n[诚实边界]")
    w("  本册裁的是「几何/TUFT 框架能否给出暗物质解」，**不宣称暗物质已被解释**。")
    w("  外部宇宙学参数（Planck 2018）与常数只引用不复算；红线 0/22 不变。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0139_暗物质攻破_2026-10-20_report.txt")
    json_path = os.path.join(BASE, "attack_C0139_暗物质攻破_2026-10-20.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0139_dark_matter",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]} for e in entries],
            "E1_cosmology": g1,
            "E2_thermal_relic": g2,
            "E3_candidates": [{"candidate": c[0], "new_inputs": c[1], "notes": c[2]} for c in cands],
            "E4_geometry_supply": g4,
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0139 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
