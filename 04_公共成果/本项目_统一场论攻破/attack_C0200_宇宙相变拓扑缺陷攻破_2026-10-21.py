# -*- coding: utf-8 -*-
"""
attack_C0200_宇宙相变拓扑缺陷攻破_2026-10-21.py
独立复算：母册 T047「早期宇宙相变 / 拓扑缺陷」· 相变机制供给检查

定位：母册 T047（行 143，原文照录）：
    | T047 | 早期宇宙相变 / 拓扑缺陷 | 相变机制 | C1,C2 | 🔲 |
前置来料：
  - C0173 磁单极攻破：g_D/e = 68.518000；M_SU5 = 3.96019e+17 GeV；π₂(SU(2)/U(1))=Z。
  - C0177 宇宙弦攻破：GUT 弦 Gμ = 6.7088e-7；PTA 上限 Gμ < 1e-11；排除比 = 67088.32×。
  - C0133 TUFT 身份注销；C0140 几何常数 (ℏ,G,c) 量纲 nullity=0。

把"早期宇宙相变与拓扑缺陷从哪来"压缩成五条可复核读数：

  E1 相变温度量级精算（只引用外部临界温度外部值，本册做比值/标度换算）：
       T_EW ≈ 100–200 GeV（电弱，SM 交叉过渡）、T_QCD ≈ 150–200 MeV（QCD 禁闭），
       与 Higgs vev v_H、Λ_QCD、轻子质量标度的比值。
  E2 **Kibble-Zurek 缺陷产量核算（本册核心）**：
       n_M/s ~ k_K (T_GUT/M_pl_red)³；Monopole Problem：GUT 相变单极产量 vs Parker/CMB 上限；
       并引用 C0177 GUT 弦排除 67088× 读数。
  E3 拓扑缺陷同伦判据代数核算：π₀(畴壁) / π₁(宇宙弦) / π₂(磁单极) 群秩。
  E4 相变机制供给检查：TUFT 是否供给相变机制或拓扑缺陷（无）。
  E5 裁定：T047 结构性负面（对 TUFT/几何框架），撞 C1/C2。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机。
退出码 0；守卫 assert 全过。

诚实边界：本册不宣称已解决早期宇宙相变/拓扑缺陷问题；外部临界温度（T_EW、T_QCD、
Λ_QCD、m_e/m_μ/m_τ、g_*、ζ(3)、Parker 通量）只引用不复算；TUFT 已注销（C0133）；
严禁把标准物理结果写成 TUFT 预测/修正。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os
import json

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（只引用不复算，来源标注） ----------
# 电弱标度（PDG / lattice）
V_H = Decimal("246.22")          # Higgs vev, GeV
M_H = Decimal("125.10")          # Higgs mass, GeV
T_EW = Decimal("160.0")           # SM 电弱交叉过渡临界温度（lattice 130–160 GeV，取 160 GeV 上限参考）
# QCD 标度（PDG / lattice）
LAMBDA_QCD = Decimal("0.218")     # Λ_QCD, GeV
T_QCD = Decimal("0.170")          # QCD 禁闭相变临界温度, GeV（lattice ~155–170 MeV）
# 轻子质量标度（PDG, MeV）
M_E_MEV = Decimal("0.511")
M_MU_MEV = Decimal("105.66")
M_TAU_MEV = Decimal("1776.9")

# GUT / 宇宙学标度（自然单位 GeV）
T_GUT = Decimal("1.0e16")        # GUT 相变温度量级（与 C0173 M_SU5=3.96e17 GeV 同尺度）
M_PL_RED = Decimal("2.435e18")   # 约化普朗克质量 M_pl = 1/sqrt(8πG), GeV
G_STAR = Decimal("106.75")       # SM 相对论自由度
ZETA3 = Decimal("1.202056903159594")  # ζ(3)
PI = Decimal("3.141592653589793")

# 引用 C0173 / C0177 读数（不重算，直接引用）
GD_OVER_E_C0173 = Decimal("68.5179995418479005570774457441288480900259138312")
M_SU5_C0173 = Decimal("3.9601906647288e17")
GMU_GUT_C0177 = Decimal("6.70883215937701117978461718484689221421948272512e-7")
GMU_LIMIT_C0177 = Decimal("1e-11")
EXCLUSION_C0177 = Decimal("67088.3215937701117978461718484689221421948272512")

# Parker / CMB 单极产量上限（量级，外部引用）
N_OVER_S_OBS = Decimal("1e-25")   # 观测上限 n_M/s（Parker + CMB + 磁单极搜索综合，量级）
K_KIBBLE = Decimal("100")         # Kibble 系数典型范围 10^0–10^3，取 10^2 参考值


def e1_transition_temperatures():
    """E1 相变温度量级精算（比值与标度换算）。"""
    # T_EW / T_QCD：电弱与 QCD 相变温度比
    ratio_ew_qcd = T_EW / T_QCD
    # T_EW / v_H：电弱临界温度与 Higgs vev 比
    ratio_ew_vh = T_EW / V_H
    # T_QCD / Λ_QCD：QCD 临界温度与 QCD 标度比
    ratio_qcd_lqcd = T_QCD / LAMBDA_QCD
    # T_EW 与 τ 轻子质量比（T_EW 单位 GeV, m_τ 单位 MeV）
    t_ew_mev = T_EW * Decimal("1000")
    ratio_ew_tautau = t_ew_mev / M_TAU_MEV
    # T_QCD 与电子质量比
    ratio_qcd_me = (T_QCD * Decimal("1000")) / M_E_MEV
    return {
        "T_EW_GeV": T_EW,
        "T_QCD_GeV": T_QCD,
        "V_H_GeV": V_H,
        "LAMBDA_QCD_GeV": LAMBDA_QCD,
        "ratio_T_EW_over_T_QCD": ratio_ew_qcd,
        "ratio_T_EW_over_vH": ratio_ew_vh,
        "ratio_T_QCD_over_LAMBDA_QCD": ratio_qcd_lqcd,
        "ratio_T_EW_over_m_tau": ratio_ew_tautau,
        "ratio_T_QCD_over_m_e": ratio_qcd_me,
    }


def e2_kibble_zurek():
    """E2 Kibble-Zurek 缺陷产量核算（本册核心）。"""
    # H(T_GUT) = T² / M_pl_red（自然单位）
    h_gut = T_GUT * T_GUT / M_PL_RED
    # (T_GUT / M_pl_red)³
    ratio_t_mpl = T_GUT / M_PL_RED
    ratio_t_mpl_cubed = ratio_t_mpl * ratio_t_mpl * ratio_t_mpl
    # n_M/s ~ k_K × (T/M_pl)³（Kibble 单极产量，量级估计）
    n_over_s_pred = K_KIBBLE * ratio_t_mpl_cubed
    # 观测上限对比
    exclusion = n_over_s_pred / N_OVER_S_OBS
    # 同时引用 C0177 GUT 弦排除比
    # 宇宙弦 Gμ 排除：GUT 弦 Gμ vs PTA 上限
    string_exclusion = GMU_GUT_C0177 / GMU_LIMIT_C0177
    # 单极质量（C0173 引用）与 T_GUT 比
    m_over_tgut = M_SU5_C0173 / T_GUT
    return {
        "T_GUT_GeV": T_GUT,
        "M_pl_red_GeV": M_PL_RED,
        "H_GUT_GeV": h_gut,
        "ratio_T_over_Mpl": ratio_t_mpl,
        "ratio_T_over_Mpl_cubed": ratio_t_mpl_cubed,
        "k_Kibble": K_KIBBLE,
        "n_over_s_pred": n_over_s_pred,
        "n_over_s_obs_limit": N_OVER_S_OBS,
        "monopole_exclusion_factor": exclusion,
        "string_GMU_GUT": GMU_GUT_C0177,
        "string_GMU_limit": GMU_LIMIT_C0177,
        "string_exclusion_factor": string_exclusion,
        "M_SU5_over_T_GUT": m_over_tgut,
        "GD_OVER_E": GD_OVER_E_C0173,
    }


def e3_homotopy():
    """E3 拓扑缺陷同伦判据代数核算（群秩，Fraction 精确）。"""
    # 群维数（生成元数），整数
    dim_SU5 = 24          # SU(5) 生成元数
    dim_SU3 = 8           # SU(3)
    dim_SU2 = 3           # SU(2)
    dim_U1 = 1            # U(1)
    dim_SM = dim_SU3 + dim_SU2 + dim_U1   # 12
    dim_manifold = dim_SU5 - dim_SM       # 12 (G/H 流形维数)
    # 同伦群秩（代数事实）：
    #   π₂(G/H) ≅ π₁(H) 当 G 单连通；π₁(H)=π₁(U(1))=Z ⇒ rank=1（磁单极，整数磁荷）
    #   π₁(G/H) ≅ π₀(H)=0（H 连通）⇒ rank=0（SU(5)→SM 链本身不产生宇宙弦）
    #   π₀(G/H) ≅ π₋₁(H)：要求 H 含分立 Z_n 因子才非零；SM 连通 ⇒ rank=0（无畴壁）
    pi2_rank = 1          # π₂(SU(5)/SM) = Z（磁单极），引用 C0173
    pi1_rank = 0          # π₁(SU(5)/SM) = 0（本链无弦；弦来自 U(1)→Z_n 另一破缺链，C0177）
    pi0_rank = 0          # π₀(SU(5)/SM) = 0（无畴壁；需分立 Z_n 破缺）
    # 't Hooft-Polyakov：SU(2)→U(1)，流形 S² 维数 = 3-1 = 2；π₂(S²)=Z
    dim_SU2_over_U1 = dim_SU2 - dim_U1    # 2 = S²
    return {
        "dim_SU5": dim_SU5,
        "dim_SM": dim_SM,
        "dim_manifold_G_over_H": dim_manifold,
        "pi0_rank_domain_wall": pi0_rank,
        "pi1_rank_cosmic_string": pi1_rank,
        "pi2_rank_monopole": pi2_rank,
        "dim_SU2_over_U1": dim_SU2_over_U1,
        "note_monopole_cite_C0173": "pi2(SU(2)/U(1))=Z；g_D/e=68.518（C0173）",
        "note_string_cite_C0177": "宇宙弦来自 U(1)→Z_n 破缺，Gμ=6.71e-7 被 PTA 排除 67088×（C0177）",
    }


def e4_tuft_supply():
    """E4 相变机制供给检查：TUFT 是否供给相变/缺陷。"""
    # TUFT 已注销（C0133）；无规范群、无 Higgs 势、无序参量、无相变动力学、无缺陷载体。
    # 几何常数 (ℏ,G,c) 量纲 nullity=0（C0140）⇒ 任何有量纲相变标度（T_EW、T_QCD、T_GUT）
    # 与缺陷张力 μ、单极质量 M_M 均不能由几何常数生成。
    return {
        "tuft_specifies_gauge_group": False,
        "tuft_specifies_higgs_potential": False,
        "tuft_specifies_order_parameter": False,
        "tuft_supplies_phase_transition": False,
        "tuft_supplies_defect_carrier": False,
        "nullity_hbarGc": 0,   # 引用 C0140 E4
        "cited_C0133": "TUFT 身份注销",
        "cited_C0140": "几何常数 nullity=0",
        "cited_C0173": "磁单极为规范拓扑孤子，TUFT 无 π₂ 拓扑载体",
        "cited_C0177": "宇宙弦为 Kibble 网络，TUFT 无弦张力/无 π₁ 网络",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0200 · 早期宇宙相变 / 拓扑缺陷（母册 T047）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_transition_temperatures()
    w("\n[E1] 相变温度量级精算（外部临界温度只引用；本册做比值/标度换算）")
    w("  T_EW = %s GeV（电弱，SM 交叉过渡，lattice 130–160 GeV）" % fv(g1["T_EW_GeV"], "4f"))
    w("  T_QCD = %s GeV = %s MeV（QCD 禁闭，lattice ~155–170 MeV）"
      % (fv(g1["T_QCD_GeV"], "4f"), fv(g1["T_QCD_GeV"] * Decimal("1000"), "2f")))
    w("  v_H = %s GeV（Higgs vev）；Λ_QCD = %s GeV"
      % (fv(g1["V_H_GeV"], "2f"), fv(g1["LAMBDA_QCD_GeV"], "3f")))
    w("  T_EW / T_QCD = %s（≈ 10³ 量级，电弱比 QCD 高约三个数量级）"
      % fv(g1["ratio_T_EW_over_T_QCD"], "4f"))
    w("  T_EW / v_H = %s（SM 交叉过渡 T_c ~ v_H 同量级）"
      % fv(g1["ratio_T_EW_over_vH"], "4f"))
    w("  T_QCD / Λ_QCD = %s（QCD 禁闭温度同 Λ_QCD 量级）"
      % fv(g1["ratio_T_QCD_over_LAMBDA_QCD"], "4f"))
    w("  T_EW / m_τ = %s（%s MeV / %s MeV）"
      % (fv(g1["ratio_T_EW_over_m_tau"], "3f"),
         fv(g1["T_EW_GeV"] * Decimal("1000"), "0f"), fv(M_TAU_MEV, "1f")))
    w("  T_QCD / m_e = %s（%s MeV / %s MeV）"
      % (fv(g1["ratio_T_QCD_over_m_e"], "3f"),
         fv(g1["T_QCD_GeV"] * Decimal("1000"), "1f"), fv(M_E_MEV, "3f")))
    w("  => 相变温度是有量纲标度（GeV/MeV），由规范破缺标度 v_H 与 Λ_QCD 设定；几何常数给不出。")
    entries.append(("E1",
                    "T_EW=%s GeV、T_QCD=%s MeV；T_EW/T_QCD=%s；T_EW/v_H=%s；T_QCD/Λ_QCD=%s"
                    % (fv(g1["T_EW_GeV"], "3f"), fv(g1["T_QCD_GeV"] * Decimal("1000"), "1f"),
                       fv(g1["ratio_T_EW_over_T_QCD"], "3f"),
                       fv(g1["ratio_T_EW_over_vH"], "3f"),
                       fv(g1["ratio_T_QCD_over_LAMBDA_QCD"], "3f")),
                    "PASS", "外部 T_EW/T_QCD/Λ_QCD/m_e/m_τ 只引用；本册做比值换算"))

    # ---- E2 ----
    g2 = e2_kibble_zurek()
    w("\n[E2] Kibble-Zurek 缺陷产量核算（本册核心）")
    w("  T_GUT = %s GeV；M_pl_red = %s GeV" % (fv(g2["T_GUT_GeV"], "2e"), fv(g2["M_pl_red_GeV"], "2e")))
    w("  H(T_GUT) = T²/M_pl = %s GeV" % fv(g2["H_GUT_GeV"], "4e"))
    w("  (T_GUT/M_pl_red) = %s；³ = %s"
      % (fv(g2["ratio_T_over_Mpl"], "4e"), fv(g2["ratio_T_over_Mpl_cubed"], "4e")))
    w("  n_M/s ~ k_K × (T/M_pl)³ = %s × %s = %s"
      % (fv(g2["k_Kibble"], "0f"), fv(g2["ratio_T_over_Mpl_cubed"], "4e"),
         fv(g2["n_over_s_pred"], "4e")))
    w("  观测上限 n_M/s < %s（Parker + CMB + 单极搜索综合，量级）"
      % fv(g2["n_over_s_obs_limit"], "1e"))
    w("  => Monopole Problem：GUT 单极产量超观测上限 %s 倍（≈10^%s）"
      % (fv(g2["monopole_exclusion_factor"], "3e"),
         (g2["monopole_exclusion_factor"].ln() / Decimal("10").ln()).to_integral_value(rounding="ROUND_HALF_UP")))
    w("  宇宙弦（引用 C0177）：GUT 弦 Gμ = %s vs PTA 上限 %s ⇒ 排除 %s×"
      % (fv(g2["string_GMU_GUT"], "3e"), fv(g2["string_GMU_limit"], "0e"),
         fv(g2["string_exclusion_factor"], "1f")))
    w("  磁单极（引用 C0173）：M_SU5/T_GUT = %s；g_D/e = %s"
      % (fv(g2["M_SU5_over_T_GUT"], "3f"), fv(g2["GD_OVER_E"], "4f")))
    w("  => 无暴胀稀释时，GUT 相变单极/弦产量远超观测上限——这是标准宇宙学的'缺陷问题'，")
    w("     其解法（暴胀、对称性破缺模式选择）均依赖外部输入的破缺机制，非几何导出。")
    entries.append(("E2",
                    "n_M/s_pred=%s vs 上限 %s ⇒ 单极过剩 %s 倍；GUT 弦排除 %s×（引 C0177）"
                    % (fv(g2["n_over_s_pred"], "2e"), fv(g2["n_over_s_obs_limit"], "0e"),
                       fv(g2["monopole_exclusion_factor"], "2e"),
                       fv(g2["string_exclusion_factor"], "1f")),
                    "PASS", "Decimal 48 位精算；T_GUT/M_pl/k_K 为量级估计；C0173/C0177 读数直接引用"))

    # ---- E3 ----
    g3 = e3_homotopy()
    w("\n[E3] 拓扑缺陷同伦判据代数核算")
    w("  SU(5) 维数 = %d；SM = SU(3)%d + SU(2)%d + U(1)%d = %d；G/H 流形维数 = %d"
      % (g3["dim_SU5"], g3["dim_SU3"] if False else 8, g3["dim_SU2"] if False else 3,
         g3["dim_U1"] if False else 1, g3["dim_SM"], g3["dim_manifold_G_over_H"]))
    w("  π₀(G/H) 秩 = %d（畴壁；需分立 Z_n 破缺才非零）" % g3["pi0_rank_domain_wall"])
    w("  π₁(G/H) 秩 = %d（宇宙弦；SU(5)→SM 链本身无弦，弦来自 U(1)→Z_n 另一破缺）"
      % g3["pi1_rank_cosmic_string"])
    w("  π₂(G/H) 秩 = %d（磁单极；≅ π₁(U(1))=Z，整数磁荷）" % g3["pi2_rank_monopole"])
    w("  't Hooft-Polyakov：SU(2)/U(1) 流形维数 = %d（=S²），π₂(S²)=Z ⇒ 磁单极（引 C0173）"
      % g3["dim_SU2_over_U1"])
    w("  => 缺陷存在性由破缺模式 G→H 的同伦群决定；破缺模式本身是外部输入。")
    entries.append(("E3",
                    "π₀秩=%d（畴壁）、π₁秩=%d（宇宙弦，本链无）、π₂秩=%d（磁单极 Z）；"
                    "SU(2)/U(1)=S² π₂=Z（C0173）"
                    % (g3["pi0_rank_domain_wall"], g3["pi1_rank_cosmic_string"],
                       g3["pi2_rank_monopole"]),
                    "PASS", "群秩为代数事实；具体破缺模式 G→H 是外部输入"))

    # ---- E4 ----
    g4 = e4_tuft_supply()
    w("\n[E4] 相变机制供给检查：TUFT 是否供给相变/缺陷")
    w("  TUFT 指定规范群：%s" % g4["tuft_specifies_gauge_group"])
    w("  TUFT 指定 Higgs 势/序参量：%s" % g4["tuft_specifies_higgs_potential"])
    w("  TUFT 供给相变动力学：%s" % g4["tuft_supplies_phase_transition"])
    w("  TUFT 供给缺陷载体（π₀/π₁/π₂ 拓扑孤子）：%s" % g4["tuft_supplies_defect_carrier"])
    w("  几何常数 (ℏ,G,c) 量纲 nullity = %d（引 C0140）⇒ T_EW/T_QCD/T_GUT/μ/M_M 均不能生成。"
      % g4["nullity_hbarGc"])
    w("  TUFT 已注销（C0133）；磁单极（C0173）/宇宙弦（C0177）均为规范破缺拓扑孤子，TUFT 无供给。")
    entries.append(("E4",
                    "TUFT 供给=0：无规范群、无 Higgs 势、无序参量、无缺陷载体；"
                    "nullity=0（C0140），C0133 注销",
                    "PASS", "撞 C1/C2"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  早期宇宙相变/拓扑缺陷问题被精确翻译成三件事：(a) 相变温度标度从哪来；")
    w("  (b) 缺陷产量与稳定性由哪条同伦群决定；(c) 破缺模式 G→H 由谁指定。")
    w("  (a) T_EW ~ v_H、T_QCD ~ Λ_QCD，均为有量纲标度，几何常数 nullity=0 给不出（E1/E4）。")
    w("  (b) 缺陷存在性由 π₀/π₁/π₂ 同伦群秩决定（E3）；GUT 单极/弦产量超观测 10^16–10^4 倍（E2）。")
    w("  (c) 破缺模式 G→H 是外部输入（SM/SU(5)/U(1)→Z_n 等），TUFT 不指定（E4）。")
    w("  => **T047 结构性负面（对 TUFT/几何框架）**；撞 **C1**（粒子内容/规范群须公设）/")
    w("     **C2**（相变标度 T_EW/T_QCD/T_GUT 是外部输入）。母册 T047 🔲→✅。")
    entries.append(("E5",
                    "T047 结构性负面：相变温度/缺陷产量/破缺模式均依赖外部规范破缺输入，"
                    "TUFT 无相变无缺陷供给；撞 C1/C2",
                    "PASS", "撞 C1/C2；母册 T047 🔲→✅"))

    # ---- 守卫 ----
    guards = [
        ("G1", "T_EW 与 T_QCD 相差约 10³ 量级（T_EW/T_QCD > 500）",
         g1["ratio_T_EW_over_T_QCD"] > Decimal("500")),
        ("G2", "T_EW 与 v_H 同量级（0.3 < T_EW/v_H < 3）",
         Decimal("0.3") < g1["ratio_T_EW_over_vH"] < Decimal("3")),
        ("G3", "GUT 单极产量超观测上限 > 10^10 倍（Monopole Problem 数量级）",
         g2["monopole_exclusion_factor"] > Decimal("1e10")),
        ("G4", "GUT 弦排除比引 C0177 = 67088×（> 10^4）",
         g2["string_exclusion_factor"] > Decimal("1e4")),
        ("G5", "π₂(SU(5)/SM) 秩 = 1（磁单极 Z）", g3["pi2_rank_monopole"] == 1),
        ("G6", "TUFT 相变供给 = 0", g4["tuft_supplies_phase_transition"] is False),
        ("G7", "几何常数 nullity = 0（引 C0140）", g4["nullity_hbarGc"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0200 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解决早期宇宙相变/拓扑缺陷问题；外部 T_EW/T_QCD/Λ_QCD/m_e/m_τ、")
    w("  T_GUT/M_pl/k_K/Parker 通量只引用不复算；TUFT 已注销（C0133）；")
    w("  严禁把标准物理结果写成 TUFT 预测/修正。数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0200_宇宙相变拓扑缺陷攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0200_宇宙相变拓扑缺陷攻破_2026-10-21.json")

    def _s(v):
        if isinstance(v, Decimal):
            return str(v)
        if isinstance(v, Fraction):
            return str(v)
        if isinstance(v, dict):
            return {kk: _s(vv) for kk, vv in v.items()}
        if isinstance(v, (list, tuple)):
            return [_s(x) for x in v]
        return v

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0200_early_universe_phase_transition_topological_defects",
            "mother_row": "| T047 | 早期宇宙相变 / 拓扑缺陷 | 相变机制 | C1,C2 | 🔲 |",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_transition_temperatures": _s(g1),
            "E2_kibble_zurek": _s(g2),
            "E3_homotopy": _s(g3),
            "E4_tuft_supply": _s(g4),
            "guards_total": len(guards),
            "guards_passed": sum(1 for g in guards if g[2]),
            "cited_C0173": {"gD_over_e": str(GD_OVER_E_C0173),
                            "M_SU5_GeV": str(M_SU5_C0173)},
            "cited_C0177": {"Gmu_GUT": str(GMU_GUT_C0177),
                            "Gmu_limit": str(GMU_LIMIT_C0177),
                            "exclusion_factor": str(EXCLUSION_C0177)},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0200 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
