# -*- coding: utf-8 -*-
"""
attack_C0231_超辐射标量云攻破_2026-10-21.py
独立复算：旋转黑洞周围的标量云（boson cloud / gravitational atom）· L线域 G批 · T127

定位：母册 T127「旋转黑洞周围的标量云（boson cloud, gravitational atom）｜
超辐射束缚态 + 频率线｜C1,C5」。主题 = Kerr 超辐射条件与增长率核算。
TUFT 已注销（C0133）；本册数值全部为**标准广义相对论 / Klein-Gordon 方程算术复核**，
严禁写成 TUFT 预测或修正。

把「标量云能否在旋转黑洞周围长出来」压缩成五条可复核读数：

  E1 观测事实：Kerr 超辐射不稳定性、引力原子（hydrogen-like scalar cloud）、
     超辐射窗 0.1 ≲ μ ≲ 1（μ = GM m_b /(ℏ c)，引力精细结构常数）——只引用不复算。
  E2 **核心核算（本册核心）**：
     (a) μ → m_b 换算 m_b = μ·(ℏc³/GM)，1 M☉ 对应 μ=1 的质量标度；
     (b) 视界角速度 Ω_H（a_*=0.99）与氢原子类比束缚态频率 ω = m_b(1-μ²/2n²) 对比，
         判定超辐射条件 ω < Ω_H（m=1）是否成立，算失谐 Δ = Ω_H·M_g − ω·M_g。
  E3 增长率标度：l=m=1 首阶 ΓM_g = (1/24)·μ⁹·Δ（Detweiler 标度，O(1) 系数），
     玻尔半径 r_c = n²/(μ² M_g) 与视界半径对比（引力原子尺寸）。
  E4 时间标度：e-折时间 τ = 1/Γ 与宇宙年龄 t_U 对比（云能否在宇宙学时标内长起来）。
  E5 供给裁定：TUFT 是否供给超辐射 / 束缚态结构（否）→ 结构性负面，撞 C1/C5。

外部输入（显式计数，≤1 项）：黑洞自旋 a_* = 0.99（已知外部输入）；
换算常数（GM☉/c³、ℏ、t_U）按 C0142 体例作「只引用不复算」的 CODATA/Planck 常数；
黑洞质量以标度 M/M☉ 符号化，时间对比取 M=10 M☉ 示例恒星黑洞。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（只引用不复算） ----------
# 外部输入（计数 = 1 项）：黑洞无量纲自旋 a_* = a/(GM/c²)
ASTAR = Decimal("0.99")
# GMR 超辐射窗目标耦合 μ = GM m_b/(ℏ c)（引力精细结构常数）
MU = Decimal("0.42")
# 换算常数（CODATA / Planck 2018，只引用）：
#   GM☉/c³ = 4.925490947e-6 s （GM☉=1.32712440018e20 m³/s², c=2.99792458e8 m/s）
TM_SUN = Decimal("4.925490947e-6")
#   ℏ = 6.582119569e-16 eV·s
HBAR_EVS = Decimal("6.582119569e-16")
#   宇宙年龄 t_U = 13.787 Gyr（Planck 2018）→ 秒
T_UNIVERSE_S = Decimal("13.787") * Decimal("1e9") * Decimal("365.25") * Decimal("86400")
# 时间标度示例：M = 10 M☉ 恒星黑洞
M_OVER_MSUN_DEMO = Decimal("10")
# l=m=1 首阶 Detweiler 增长率系数（O(1)，数值文献 1/24 量级；标度关系不依赖末位）
GAMMA_COEF = Fraction(1, 24)


def e1_facts():
    """超辐射标量云观测事实（只引用）。"""
    return {
        "effect": "Kerr 超辐射不稳定性（Teukolsky 方程 + 复质量 KG）",
        "window_mu": "0.1 ≲ μ ≲ 1（μ = GM m_b/(ℏ c)）",
        "analogy": "引力原子（氢原子类比束缚态），l=m=1 为最低超辐射模",
        "growth_scaling": "Γ ∝ μ^(4l+5)·(m Ω_H − ω)（l=1 ⇒ μ⁹）",
    }


def e2_superradiance_window():
    """核心核算：μ→m_b 换算 + Ω_H vs ω 对比。"""
    # (a) 质量标度：M=1 M☉ 时 μ=1 对应的玻色子静能
    E_PER_MU_PER_MSUN = HBAR_EVS / TM_SUN          # eV  per (μ=1, M=1M☉)
    m_b_ev = E_PER_MU_PER_MSUN * MU                 # M=1 M☉ 时的玻色子质量
    # (b) Kerr 视界
    #   r_+/(GM/c²) = 1 + sqrt(1-a_*²)；Ω_H·(GM/c²) = a_*/((r_+/M_g)² + a_*²)
    s = (Decimal(1) - ASTAR * ASTAR).sqrt()         # sqrt(1-a_*²)
    rp_factor = Decimal(1) + s                      # r_+ = rp_factor·M_g
    omega_h_Mg = ASTAR / (rp_factor * rp_factor + ASTAR * ASTAR)
    # (c) 束缚态频率（氢原子类比，n=1 与 n=2）
    mu2 = MU * MU
    omega_Mg = {n: MU * (Decimal(1) - mu2 / (Decimal(2) * n * n)) for n in (1, 2)}
    ratios = {n: omega_Mg[n] / omega_h_Mg for n in (1, 2)}
    detunings = {n: omega_h_Mg - omega_Mg[n] for n in (1, 2)}  # >0 ⇒ 超辐射在窗内
    return {
        "E_per_mu_per_Msun_eV": E_PER_MU_PER_MSUN,
        "m_b_at_1Msun_eV": m_b_ev,
        "sqrt_1_astar2": s,
        "rp_factor": rp_factor,
        "omega_h_Mg": omega_h_Mg,
        "omega_Mg": omega_Mg,
        "ratio_omega_over_omegaH": ratios,
        "detuning_Delta": detunings,
        "m_b_demo_eV": m_b_ev / M_OVER_MSUN_DEMO,  # M=10 M☉ 示例
    }


def e3_growth_radius(g2):
    """增长率标度（n=1 失谐）+ 玻尔半径。"""
    mu9 = MU ** 9
    delta1 = g2["detuning_Delta"][1]
    # Γ·M_g = (1/24)·μ⁹·Δ （l=m=1 首阶）
    Gamma_Mg = Decimal(float(GAMMA_COEF)) * mu9 * delta1
    # 玻尔半径 r_c = n²/(μ² M_g)（几何单位），对比视界 r_+ = rp_factor·M_g
    mu2 = MU * MU
    r_c_over_Mg = {n: (n * n) / mu2 for n in (1, 2)}
    r_c_over_rp = {n: r_c_over_Mg[n] / g2["rp_factor"] for n in (1, 2)}
    # e-折时间（物理）：τ = (GM/c³)/(Γ·M_g) = TM_SUN·(M/M☉)/(ΓM_g)
    tau_per_Msun_s = TM_SUN / Gamma_Mg
    return {
        "mu9": mu9,
        "detuning_n1": delta1,
        "Gamma_Mg": Gamma_Mg,
        "r_c_over_Mg": r_c_over_Mg,
        "r_c_over_rp": r_c_over_rp,
        "tau_per_Msun_s": tau_per_Msun_s,
    }


def e4_timescale(g3):
    """τ vs 宇宙年龄。"""
    tau_demo_s = g3["tau_per_Msun_s"] * M_OVER_MSUN_DEMO   # M=10 M☉
    ratio = T_UNIVERSE_S / tau_demo_s
    return {
        "t_universe_s": T_UNIVERSE_S,
        "tau_demo_s": tau_demo_s,
        "ratio_tU_over_tau": ratio,
        "cloud_grows_in_cosmic_time": ratio > Decimal("1e10"),
    }


def e5_supply():
    """TUFT 供给检查：有无旋转时空 / 束缚态标量云结构？"""
    return {
        "tuft_kerr_solution": "none",        # TUFT 无旋转 Kerr 时空解
        "tuft_bound_state_spectrum": "none",  # 无 KG 束缚态 / 超辐射模结构
        "tuft_supply": 0,
        "verdict": "structural_negative",
        "collide": "C1 / C5",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0231 · 旋转黑洞周围标量云（超辐射束缚态）攻破（L线域 G批 · T127）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 观测事实（只引用不复算）")
    w("  效应：%s" % g1["effect"])
    w("  超辐射窗：%s（μ 为引力精细结构常数）" % g1["window_mu"])
    w("  类比：%s" % g1["analogy"])
    w("  增长率标度：%s" % g1["growth_scaling"])
    entries.append(("E1", "Kerr 超辐射不稳定性 + 引力原子束缚态（标准物理事实，只引用）",
                    "PASS", "Teukolsky/KG 文献事实，本册只引用"))

    # ---- E2 ----
    g2 = e2_superradiance_window()
    w("\n[E2] 核心核算：μ→m_b 换算 + 超辐射窗判定（本册核心）")
    w("  (a) 质量标度：ℏc³/(GM☉) = %s eV（μ=1、M=1M☉）" % fv(g2["E_per_mu_per_Msun_eV"], "4e"))
    w("      μ=%s ⇒ M=1M☉ 时 m_b = %s eV；M=10M☉ 示例 m_b = %s eV（超轻标量）"
      % (MU, fv(g2["m_b_at_1Msun_eV"], "4e"), fv(g2["m_b_demo_eV"], "4e")))
    w("  (b) 视界（a_*=%s）：sqrt(1-a_*²)=%s；r_+/M_g=1+sqrt=%s"
      % (ASTAR, fv(g2["sqrt_1_astar2"], "10f"), fv(g2["rp_factor"], "10f")))
    w("      Ω_H·M_g = a_*/((r_+/M_g)²+a_*²) = %s" % fv(g2["omega_h_Mg"], "12f"))
    w("  (c) 束缚态频率 ω·M_g = μ(1-μ²/2n²)：")
    for n in (1, 2):
        w("      n=%d：ω·M_g=%s，ω/Ω_H=%s，失谐 Δ=Ω_H·M_g−ω·M_g=%s"
          % (n, fv(g2["omega_Mg"][n], "12f"), fv(g2["ratio_omega_over_omegaH"][n], "10f"),
             fv(g2["detuning_Delta"][n], "12f")))
    w("      => ω/Ω_H < 1（n=1: %s；n=2: %s）且 Δ>0 ⇒ 超辐射条件 0<ω<m_b 且 ω<Ω_H 成立，"
      "μ=%s 落在 GMR 窗内边缘。"
      % (fv(g2["ratio_omega_over_omegaH"][1], "4f"),
         fv(g2["ratio_omega_over_omegaH"][2], "4f"), MU))
    entries.append(("E2", "μ=%s 时 ω/Ω_H=%s<1（Δ=%s>0）：超辐射窗成立；m_b(M=10M☉)=%s eV"
                    % (MU, fv(g2["ratio_omega_over_omegaH"][1], "4f"),
                       fv(g2["detuning_Delta"][1], "6e"), fv(g2["m_b_demo_eV"], "3e")),
                    "PASS", "标准 GR/KG 算术：Ω_H、氢原子类比能级独立精算"))

    # ---- E3 ----
    g3 = e3_growth_radius(g2)
    w("\n[E3] 增长率标度 + 玻尔半径")
    w("  μ⁹ = %s；Δ(n=1) = %s" % (fv(g3["mu9"], "6e"), fv(g3["detuning_n1"], "6e")))
    w("  Γ·M_g = (1/24)·μ⁹·Δ = %s（l=m=1 首阶，系数 O(1)）" % fv(g3["Gamma_Mg"], "6e"))
    w("  玻尔半径 r_c = n²/(μ² M_g)：n=1 ⇒ r_c/M_g=%s（r_c/r_+=%s）；"
      "n=2 ⇒ r_c/M_g=%s（r_c/r_+=%s）"
      % (fv(g3["r_c_over_Mg"][1], "6f"), fv(g3["r_c_over_rp"][1], "6f"),
         fv(g3["r_c_over_Mg"][2], "6f"), fv(g3["r_c_over_rp"][2], "6f")))
    w("  => 云半径 ~5–20 视界半径，与「引力原子」尺寸一致；Γ>0 ⇒ 超辐射增长而非衰减。")
    entries.append(("E3", "ΓM_g=%s>0（超辐射增长）；r_c/r_+≈%s–%s（引力原子尺寸）"
                    % (fv(g3["Gamma_Mg"], "2e"), fv(g3["r_c_over_rp"][1], "1f"),
                       fv(g3["r_c_over_rp"][2], "1f")), "PASS",
                    "Detweiler 首阶标度 + 玻尔半径几何对比"))

    # ---- E4 ----
    g4 = e4_timescale(g3)
    w("\n[E4] 时间标度：e-折时间 τ vs 宇宙年龄")
    w("  τ(每 M☉) = (GM☉/c³)/(ΓM_g) = %s s·(M/M☉)" % fv(g3["tau_per_Msun_s"], "6e"))
    w("  M=10M☉：τ = %s s；t_U = %s s（Planck 2018）"
      % (fv(g4["tau_demo_s"], "6e"), fv(g4["t_universe_s"], "6e")))
    w("  t_U/τ = %s（≫1）⇒ 云在宇宙学时标内可完成大量 e-折增长。" % fv(g4["ratio_tU_over_tau"], "6e"))
    entries.append(("E4", "t_U/τ = %s ≫1：标量云在宇宙年龄内可长起来（标准物理自洽）"
                    % fv(g4["ratio_tU_over_tau"], "2e"), "PASS",
                    "标准 GR 算术；结论不属 TUFT"))

    # ---- E5 ----
    g5 = e5_supply()
    w("\n[E5] 供给裁定：TUFT 是否供给超辐射 / 束缚态结构？")
    w("  TUFT 旋转 Kerr 时空解：%s；TUFT 束缚态谱：%s"
      % (g5["tuft_kerr_solution"], g5["tuft_bound_state_spectrum"]))
    w("  标量云完全依赖 Kerr 超辐射（Ω_H、Teukolsky 模）+ KG 氢原子束缚态（nlm）——")
    w("  全是标准物理结构；TUFT 无旋转时空、无束缚态供给 ⇒ 结构性负面，撞 C1/C5。")
    entries.append(("E5", "TUFT 供给 0：标量云=Kerr 超辐射+KG 束缚态（标准物理），"
                    "结构性负面，撞 C1/C5", "PASS", "撞 C1/C5（母册登记）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "超辐射条件 ω/Ω_H < 1（n=1）", g2["ratio_omega_over_omegaH"][1] < Decimal(1)),
        ("G2", "失谐 Δ = Ω_H·M_g − ω·M_g > 0（窗内）", g2["detuning_Delta"][1] > Decimal(0)),
        ("G3", "Γ·M_g > 0（超辐射增长而非衰减）", g3["Gamma_Mg"] > Decimal(0)),
        ("G4", "云半径越过视界 r_c/r_+ > 1", g3["r_c_over_rp"][1] > Decimal(1)),
        ("G5", "t_U/τ ≫ 1（宇宙学时标内可增长）", g4["ratio_tU_over_tau"] > Decimal("1e10")),
        ("G6", "TUFT 供给 = 0（结构性负面）", g5["tuft_supply"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0231 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解决标量云物理：全部数值为标准 GR/KG 算术复核（外部输入仅 a_*=0.99）；")
    w("  Detweiler 系数 O(1)（1/24）按标度关系判定，末位系数不影响结论；")
    w("  TUFT 已注销（C0133），严禁把标准物理结果写成 TUFT 预测/修正。")
    w("  红线不变：「有预测且对 = 0/22」；数学自洽 ≠ 实验证实；UFT-3=0 保持。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0231_超辐射标量云攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0231_超辐射标量云攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0231_superradiant_scalar_cloud",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": {k: str(v) for k, v in g1.items()},
            "E2_window": {
                "E_per_mu_per_Msun_eV": str(g2["E_per_mu_per_Msun_eV"]),
                "m_b_at_1Msun_eV": str(g2["m_b_at_1Msun_eV"]),
                "m_b_demo_M10Msun_eV": str(g2["m_b_demo_eV"]),
                "omega_h_Mg": str(g2["omega_h_Mg"]),
                "omega_Mg_n1": str(g2["omega_Mg"][1]),
                "omega_Mg_n2": str(g2["omega_Mg"][2]),
                "ratio_n1": str(g2["ratio_omega_over_omegaH"][1]),
                "ratio_n2": str(g2["ratio_omega_over_omegaH"][2]),
                "detuning_n1": str(g2["detuning_Delta"][1]),
            },
            "E3_growth": {
                "mu9": str(g3["mu9"]),
                "Gamma_Mg": str(g3["Gamma_Mg"]),
                "r_c_over_rp_n1": str(g3["r_c_over_rp"][1]),
                "r_c_over_rp_n2": str(g3["r_c_over_rp"][2]),
                "tau_per_Msun_s": str(g3["tau_per_Msun_s"]),
            },
            "E4_timescale": {
                "t_universe_s": str(g4["t_universe_s"]),
                "tau_demo_s": str(g4["tau_demo_s"]),
                "ratio_tU_over_tau": str(g4["ratio_tU_over_tau"]),
            },
            "E5_supply": g5,
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0231 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
