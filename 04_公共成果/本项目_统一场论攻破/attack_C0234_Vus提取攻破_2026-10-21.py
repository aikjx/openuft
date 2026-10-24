# -*- coding: utf-8 -*-
"""
attack_C0234_Vus提取攻破_2026-10-21.py
独立复算：母册 T372「从 π_l2/μ 衰变提取 V_us 与轻子普适检验」
（L 线域 H 批 · 轻子普适比核算，母册登记撞 C5/C6）

定位：母册 T372（轻子普适）。本册**不采信任何自报**，用 PDG 2024 实测质量/寿命/
分支比/衰变常数比独立精算：π→eν/π→μν  helicity 抑制比（含标准内辐射修正）、
由 Γ(Kμ2)/Γ(πμ2) 反解 |V_us|、R_π 观测 vs SM 预期偏差，并对 TUFT/几何框架判定
"是否供给轻子普适 / 衰变宽度结构"。

把"π_l2/μ 提取 V_us 与轻子普适检验"压缩成五条可复核读数：

  E1 输入事实（PDG 只引用不复算）：m_e/m_μ/m_π±/m_K±、寿命 τ_π/τ_K、分支比
     BR(π→μν)/BR(K→μν)、衰变常数比 f_K/f_π、|V_ud|、R_π 观测值、标准内辐射
     修正因子 η_rad。
  E2 **R_π = Γ(π→eν)/Γ(π→μν) 精算（本册核心）**：V-A 赝标轻子衰变宽度
     Γ(P→lν) = G_F²|V|²f_P² m_l² m_P/(8π)·(1−m_l²/m_P²)²，树级 helicity 抑制比
     (m_e/m_μ)²·(m_π²−m_e²)²/(m_π²−m_μ²)²，乘标准内辐射修正 η_rad。
  E3 **V_us 反解核算**：Γ(Kμ2)/Γ(πμ2) = [BR(Kμ2)/τ_K]/[BR(πμ2)/τ_π]，
     由 (|V_us|/|V_ud|)² = (Γ_Kμ/Γ_πμ)·(f_π/f_K)²·(m_π/m_K)·
     [(1−m_μ²/m_π²)²/(1−m_μ²/m_K²)²] 反解 |V_us|。
  E4 正演核对：以 |V_us|=0.2243 反算 Γ_Kμ/Γ_πμ 与观测比对；R_π 观测 vs
     SM 预期偏差核算。
  E5 裁定：TUFT 无轻子普适 / 无 CKM / 无衰变宽度结构供给 → 结构性负面，
     按母册登记撞 C5/C6。

纯标准库（Decimal 48 位 + Fraction 精确交叉核对），零外部依赖，退出码 0。

诚实边界：本册不宣称已解释 V_us 或轻子普适；PDG 实测值只引用不复算；
所有数值均为标准弱作用 / 手征算术复核，**严禁写成 TUFT 预测/修正**；
TUFT 已注销（C0133）。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（PDG 2024 / FLAG，只引用不复算） ----------
M_E = Decimal("0.510998950")      # 电子质量 MeV（PDG）
M_MU = Decimal("105.6583755")     # μ 子质量 MeV（PDG）
M_PIP = Decimal("139.57039")      # π± 质量 MeV（PDG）
M_KP = Decimal("493.677")         # K± 质量 MeV（PDG）
TAU_PI = Decimal("2.6033e-8")    # π± 寿命 s（PDG）
TAU_K = Decimal("1.2380e-8")     # K± 寿命 s（PDG）
BR_PI_MU = Decimal("0.9998770")  # BR(π±→μ±νμ)（PDG）
BR_K_MU = Decimal("0.6356")       # BR(K±→μ±νμ)（PDG）
FK_OVER_FPI = Decimal("1.1939")   # f_K/f_π（FLAG 20 LQCD 标准值，只引用）
V_UD = Decimal("0.973767")       # |V_ud|（PDG 超容许 β 衰变，只引用）
RPI_OBS = Decimal("1.2300e-4")   # R_π = Γ(π→eν)/Γ(π→μν) 观测均值（PDG）
ETA_RAD = Decimal("0.9627")       # 标准内辐射修正因子（Marciano–Sanda 型，只引用）
VUS_FID = Decimal("0.2243")       # PDG |V_us| 中心值（正演核对用，只引用）


def e1_inputs():
    """E1：PDG 输入事实（只引用）。"""
    return {
        "m_e_MeV": M_E, "m_mu_MeV": M_MU,
        "m_pip_MeV": M_PIP, "m_kp_MeV": M_KP,
        "tau_pi_s": TAU_PI, "tau_k_s": TAU_K,
        "BR_pi_mu": BR_PI_MU, "BR_k_mu": BR_K_MU,
        "fK_over_fpi": FK_OVER_FPI, "V_ud": V_UD,
        "Rpi_obs": RPI_OBS, "eta_rad": ETA_RAD,
    }


def e2_rpi():
    """E2：R_π = Γ(π→eν)/Γ(π→μν) 精算（本册核心）。

    第一性推导（SM V-A 赝标轻子衰变宽度）：
      Γ(P → l ν̄) = G_F²|V_ud|² f_P² m_l² m_P / (8π) · (1 − m_l²/m_P²)²
    自旋 0 赝标量 + V-A ⇒ 末态轻子左手、中微子右手，螺旋度对齐强制 m_l 耦合 ⇒
    helicity 抑制 m_l²。同 π 道取比，G_F、V_ud、f_π、m_π、8π 全消：
      R_π^tree = (m_e²/m_μ²) · (m_π²−m_e²)²/(m_π²−m_μ²)²
    标准内辐射修正（Marciano–Sanda 型，η_rad 外部引用）：
      R_π^SM = R_π^tree · η_rad
    """
    me2 = M_E * M_E
    mmu2 = M_MU * M_MU
    mpi2 = M_PIP * M_PIP
    mass_ratio = me2 / mmu2
    kin = (mpi2 - me2) / (mpi2 - mmu2)
    kin2 = kin * kin
    rpi_tree = mass_ratio * kin2
    rpi_sm = rpi_tree * ETA_RAD
    dev = (RPI_OBS - rpi_sm) / rpi_sm  # 观测 vs SM 相对偏差
    return {
        "me2": me2, "mmu2": mmu2, "mpi2": mpi2,
        "mass_ratio_m2": mass_ratio, "kin": kin, "kin2": kin2,
        "rpi_tree": rpi_tree, "rpi_sm": rpi_sm,
        "rpi_obs": RPI_OBS, "dev_obs_vs_sm": dev,
    }


def e3_vus_extract():
    """E3：由 Γ(Kμ2)/Γ(πμ2) 反解 |V_us|。

    Γ(P→μν) = BR(P→μν)/τ_P。比值：
      Γ_Kμ/Γ_πμ = [BR_Kμ/τ_K]/[BR_πμ/τ_π]
    由宽度公式（E2 同型）：
      Γ_Kμ/Γ_πμ = (|V_us|²/|V_ud|²)·(f_K²/f_π²)·(m_K/m_π)·
                  [(1−m_μ²/m_K²)²/(1−m_μ²/m_π²)²]
    反解：
      (|V_us|/|V_ud|)² = (Γ_Kμ/Γ_πμ)·(f_π/f_K)²·(m_π/m_K)·
                          [(1−m_μ²/m_π²)²/(1−m_μ²/m_K²)²]
    Fraction 交叉核对：Γ 比值用精确有理算术独立复算。
    """
    gamma_pi_mu = BR_PI_MU / TAU_PI
    gamma_k_mu = BR_K_MU / TAU_K
    r_gamma = gamma_k_mu / gamma_pi_mu
    # Fraction 精确交叉核对（输入 Decimal 字符串转精确有理数）
    fr = ((Fraction(str(BR_K_MU)) / Fraction(str(TAU_K)))
          / (Fraction(str(BR_PI_MU)) / Fraction(str(TAU_PI))))
    r_gamma_frac = Decimal(fr.numerator) / Decimal(fr.denominator)
    mmu2 = M_MU * M_MU
    mpi2 = M_PIP * M_PIP
    mk2 = M_KP * M_KP
    kin_pi = (Decimal(1) - mmu2 / mpi2) ** 2
    kin_k = (Decimal(1) - mmu2 / mk2) ** 2
    ratio2 = (r_gamma
              * (Decimal(1) / (FK_OVER_FPI * FK_OVER_FPI))
              * (M_PIP / M_KP)
              * (kin_pi / kin_k))
    ratio = ratio2.sqrt()
    v_us = ratio * V_UD
    return {
        "gamma_pi_mu": gamma_pi_mu, "gamma_k_mu": gamma_k_mu,
        "r_gamma": r_gamma, "r_gamma_frac": r_gamma_frac,
        "frac_check_diff": abs(r_gamma - r_gamma_frac),
        "kin_pi": kin_pi, "kin_k": kin_k,
        "vus_over_vud2": ratio2, "vus_over_vud": ratio,
        "v_us": v_us,
    }


def e4_forward_check(g3):
    """E4：正演核对——以 |V_us|=0.2243 反算 Γ_Kμ/Γ_πμ，与观测比值比对。"""
    mmu2 = M_MU * M_MU
    mpi2 = M_PIP * M_PIP
    mk2 = M_KP * M_KP
    kin_pi = (Decimal(1) - mmu2 / mpi2) ** 2
    kin_k = (Decimal(1) - mmu2 / mk2) ** 2
    r_pred = ((VUS_FID / V_UD) ** 2
              * (FK_OVER_FPI * FK_OVER_FPI)
              * (M_KP / M_PIP)
              * (kin_k / kin_pi))
    r_obs = g3["r_gamma"]
    dev = (r_pred - r_obs) / r_obs
    return {"r_gamma_pred": r_pred, "r_gamma_obs": r_obs, "dev_pred_vs_obs": dev}


def e5_verdict():
    """E5：TUFT 供给判定。"""
    return {
        "tuft_lepton_universality_supply": 0,  # TUFT 无轻子普适/无三代轻子结构
        "tuft_ckm_supply": 0,                  # TUFT 无 CKM 矩阵（承接 C0142 E4）
        "tuft_decay_width_supply": 0,          # TUFT 无弱作用宽度/G_f/f_P 供给
        "vus_needs": "轻子普适 + CKM |V_us| + LQCD f_K/f_π（标准弱作用）",
        "verdict": "结构性负面（对 TUFT/几何框架）",
        "hits": "C5（可检验）+ C6（误差带）",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0234 · π_l2/μ 提取 V_us 与轻子普适检验（母册 T372 · L 线域 H 批）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_inputs()
    w("\n[E1] PDG 输入事实（只引用不复算）")
    w("  m_e = %s MeV；m_μ = %s MeV" % (fv(M_E, "9f"), fv(M_MU, "7f")))
    w("  m_π± = %s MeV；m_K± = %s MeV" % (fv(M_PIP, "5f"), fv(M_KP, "3f")))
    w("  τ_π = %s s；τ_K = %s s" % (fv(M_PIP * 0 + TAU_PI, "4e"), fv(TAU_K, "4e")))
    w("  BR(π→μν) = %s；BR(K→μν) = %s" % (fv(BR_PI_MU, "7f"), fv(BR_K_MU, "4f")))
    w("  f_K/f_π = %s（FLAG LQCD）；|V_ud| = %s（PDG）" % (FK_OVER_FPI, V_UD))
    w("  R_π 观测 = %s；标准内辐射修正 η_rad = %s" % (RPI_OBS, ETA_RAD))
    w("  => 全部外部输入（PDG 2024 / FLAG），本册只做 helicity/弱作用算术与反解。")
    entries.append(("E1", "PDG 质量/寿命/分支比/f_K/f_π/V_ud 只引用；本册做 helicity 与反解算术",
                    "PASS", "外部输入显式计数"))

    # ---- E2 ----
    g2 = e2_rpi()
    w("\n[E2] R_π = Γ(π→eν)/Γ(π→μν) 精算（本册核心）")
    w("  宽度公式：Γ(P→lν) = G_F²|V_ud|²f_π² m_l² m_π/(8π)·(1−m_l²/m_π²)²（V-A helicity 抑制）")
    w("  质量平方：m_e²=%s；m_μ²=%s；m_π²=%s"
      % (fv(g2["me2"], "8f"), fv(g2["mmu2"], "3f"), fv(g2["mpi2"], "2f")))
    w("  (m_e/m_μ)² = %s" % fv(g2["mass_ratio_m2"], "8e"))
    w("  (m_π²−m_e²)/(m_π²−m_μ²) = %s，平方 = %s"
      % (fv(g2["kin"], "8f"), fv(g2["kin2"], "8f")))
    w("  R_π^tree = %s × %s = %s"
      % (fv(g2["mass_ratio_m2"], "6e"), fv(g2["kin2"], "6f"), fv(g2["rpi_tree"], "8e")))
    w("  R_π^SM = R_π^tree × η_rad(%s) = %s" % (ETA_RAD, fv(g2["rpi_sm"], "8e")))
    w("  R_π 观测 = %s；相对偏差 (obs−SM)/SM = %s"
      % (fv(g2["rpi_obs"], "8e"), fv(g2["dev_obs_vs_sm"], "6f")))
    w("  => SM 预期 ≈1.235e-4，观测 ≈1.230e-4，偏差 −0.4% 量级（PDG 误差带内），")
    w("     轻子普适在 π_l2 道闭合。")
    entries.append(("E2", "R_π^tree=%s；R_π^SM=%s（含 η_rad）；观测=%s；偏差=%s"
                    % (fv(g2["rpi_tree"], "6e"), fv(g2["rpi_sm"], "6e"),
                       fv(g2["rpi_obs"], "6e"), fv(g2["dev_obs_vs_sm"], "4f")),
                    "PASS", "V-A helicity 抑制比 + 标准内辐射修正，Decimal 48 位精算"))

    # ---- E3 ----
    g3 = e3_vus_extract()
    w("\n[E3] V_us 反解核算（Γ(Kμ2)/Γ(πμ2)）")
    w("  Γ(π→μν) = BR_πμ/τ_π = %s s^-1" % fv(g3["gamma_pi_mu"], "6e"))
    w("  Γ(K→μν) = BR_Kμ/τ_K = %s s^-1" % fv(g3["gamma_k_mu"], "6e"))
    w("  Γ_Kμ/Γ_πμ = %s（Fraction 精确交叉核对差 %s）"
      % (fv(g3["r_gamma"], "8f"), fv(g3["frac_check_diff"], "2e")))
    w("  运动学因子：(1−m_μ²/m_π²)²=%s；(1−m_μ²/m_K²)²=%s"
      % (fv(g3["kin_pi"], "6f"), fv(g3["kin_k"], "6f")))
    w("  (|V_us|/|V_ud|)² = 比值×(f_π/f_K)²×(m_π/m_K)×[(1−m_μ²/m_π²)²/(1−m_μ²/m_K²)²]")
    w("                  = %s" % fv(g3["vus_over_vud2"], "8f"))
    w("  |V_us|/|V_ud| = sqrt = %s" % fv(g3["vus_over_vud"], "8f"))
    w("  |V_us| = %s × %s = %s"
      % (fv(g3["vus_over_vud"], "6f"), V_UD, fv(g3["v_us"], "8f")))
    w("  => 反解 |V_us| ≈ 0.2243，与 PDG 中心值一致（标准弱作用算术复核）。")
    entries.append(("E3", "反解 |V_us| = %s（PDG ≈0.2243；Γ 比值 Fraction 交叉核对一致）"
                    % fv(g3["v_us"], "6f"), "PASS",
                    "PDG 分支比/寿命反解 + f_K/f_π，标准弱作用算术"))

    # ---- E4 ----
    g4 = e4_forward_check(g3)
    w("\n[E4] 正演核对：|V_us|=0.2243 → Γ_Kμ/Γ_πμ 预测 vs 观测")
    w("  预测 Γ_Kμ/Γ_πμ = %s；观测 = %s；偏差 = %s"
      % (fv(g4["r_gamma_pred"], "8f"), fv(g4["r_gamma_obs"], "8f"),
         fv(g4["dev_pred_vs_obs"], "6f")))
    w("  R_π 观测 vs SM 偏差（E2 同读数）= %s（PDG 误差带内，普适性闭合）"
      % fv(g2["dev_obs_vs_sm"], "4f"))
    entries.append(("E4", "正演比值 %s vs 观测 %s，偏差 %s；R_π 普适性偏差 %s"
                    % (fv(g4["r_gamma_pred"], "4f"), fv(g4["r_gamma_obs"], "4f"),
                       fv(g4["dev_pred_vs_obs"], "3f"), fv(g2["dev_obs_vs_sm"], "3f")),
                    "PASS", "正演/反演双向闭环核对"))

    # ---- E5 ----
    g5 = e5_verdict()
    w("\n[E5] 裁定：TUFT 供给检查")
    w("  TUFT 轻子普适/三代轻子供给 = %d；CKM 矩阵供给 = %d；衰变宽度/G_f/f_P 供给 = %d"
      % (g5["tuft_lepton_universality_supply"], g5["tuft_ckm_supply"],
         g5["tuft_decay_width_supply"]))
    w("  V_us 提取依赖：%s" % g5["vus_needs"])
    w("  => TUFT 已注销（C0133）；无轻子普适、无 CKM 结构、无弱衰变宽度供给，")
    w("     所有读数均为标准弱作用/手征算术复核，**严禁写成 TUFT 预测/修正**。")
    w("  => **结构性负面（对 TUFT/几何框架）**；按母册 T372 登记撞 C5（可检验）/C6（误差带）。")
    entries.append(("E5", "TUFT 无轻子普适/无 CKM/无衰变宽度供给 ⇒ 结构性负面；撞 C5/C6",
                    "PASS", "标准弱作用算术，非 TUFT 预测"))

    # ---- 守卫 ----
    guards = [
        ("G1", "R_π^tree 在 1.20e-4–1.36e-4 邻域（helicity 抑制）",
         Decimal("1.20e-4") < g2["rpi_tree"] < Decimal("1.36e-4")),
        ("G2", "R_π^SM（含辐射修正）在 1.21e-4–1.25e-4（标准值 ≈1.235e-4）",
         Decimal("1.21e-4") < g2["rpi_sm"] < Decimal("1.25e-4")),
        ("G3", "反解 |V_us| 在 0.220–0.228（PDG ≈0.2243）",
         Decimal("0.220") < g3["v_us"] < Decimal("0.228")),
        ("G4", "R_π 观测 vs SM 相对偏差 |dev| < 1%（普适性闭合）",
         abs(g2["dev_obs_vs_sm"]) < Decimal("0.01")),
        ("G5", "正演 Γ 比值与观测偏差 |dev| < 1%（反演/正演闭环）",
         abs(g4["dev_pred_vs_obs"]) < Decimal("0.01")),
        ("G6", "Fraction 交叉核对 Γ 比值差 ≈ 0",
         g3["frac_check_diff"] < Decimal("1e-30")),
        ("G7", "TUFT 轻子普适供给 = 0",
         g5["tuft_lepton_universality_supply"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0234 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解释 V_us 或轻子普适；PDG 实测值只引用不复算；")
    w("  所有数值为标准弱作用/手征算术复核，非 TUFT 预测；TUFT 已注销（C0133）。")
    w("  红线：不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("       有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0234_Vus提取攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0234_Vus提取攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0234_Vus_pil2_extraction",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_inputs": {k: str(v) for k, v in g1.items()},
            "E2_rpi": {k: str(v) for k, v in g2.items()},
            "E3_vus_extract": {k: str(v) for k, v in g3.items()},
            "E4_forward_check": {k: str(v) for k, v in g4.items()},
            "E5_verdict": {k: str(v) for k, v in g5.items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0234 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
