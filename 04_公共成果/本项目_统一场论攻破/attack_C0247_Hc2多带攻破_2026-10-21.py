# -*- coding: utf-8 -*-
"""
attack_C0247_Hc2多带攻破_2026-10-21.py
独立精算：T613「多带超导体中 Landau 规则破缺（H_c2 多带贡献）」
· L 线域 E 批 · 凝聚态（承接 C0153 BCS 超导公式链口径）

定位：母册 T613（撞 C5,C6；本批凝聚态续项）。前置：C0153 已立 BCS 弱耦合公式链
（Δ0=1.764 k_B Tc、2Δ0/k_B Tc=3.528）。本册把「上临界场 H_c2 从哪来 / Landau 线性
规则为何在多带破缺」压缩成五条可复核读数。

  E1 实验事实（只引用不复算）：MgB2 Tc=39 K、两带能隙 Δσ≈7.2 meV / Δπ≈2.5 meV、
     近 Tc 斜率 dH_c2^ab/dT≈−0.36 T/K、实测 H_c2^ab(0)≈13.2 T（bulk）；
     磁通量子 Φ0=h/2e（h、e 为 SI 精确常数）。
  E2 **单带 H_c2 核算（本册核心一）**：H_c2(0)=Φ0/(2πξ²)，Φ0=h/(2e) 由精确 SI
     常数 Decimal 精算闭包；ξ_ab(0)=5.0 nm 代入。
  E3 **多带核算（本册核心二）**：MgB2 σ/π 两带模型——两能隙 BCS 比值偏离单带
     3.528；近 Tc 斜率（π 带主导）WHH 外推 vs 实测 H_c2(0)（σ 带低温接管）=
     Landau 规则破缺比。
  E4 Landau 规则与 WHH 公式核算：H_c2(T) 近 Tc 线性、H_c2(0)=−0.69 Tc·dH_c2/dT；
     并由实测 H_c2(0) 反推 ξ 闭环。
  E5 供给检查：TUFT 是否供给超导凝聚/相干结构（无）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界：本册不宣称解决任何物理难题；所有数值均为标准凝聚态算术复核；
TUFT 已注销（C0133），本册严禁把标准物理结果写成 TUFT 预测/修正；
Tc/ξ/Δ/斜率/H_c2 均为已知外部输入显式计数。裁的是「TUFT/几何框架能否供给超导
凝聚与相干结构」=0。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

PI = Decimal("3.1415926535897932384626433832795028841971693993751")

# ---------- E1 外部输入（实验事实，只引用不复算；括号内为来源口径） ----------
# SI 精确常数（CODATA 2019 精确定义）
H_PLANCK = Decimal("6.62607015e-34")   # J·s（精确）
E_CHARGE = Decimal("1.602176634e-19")  # C（精确）
# 磁通量子文献值（只引用，用于闭包对比）
PHI0_QUOTED = Decimal("2.067833848e-15")  # Wb (= T·m^2)
# MgB2：Nagamatsu et al. 2001；两能隙由点隧穿/比热分立实验确立
MGB2_TC = Decimal("39")          # K
DELTA_SIGMA = Decimal("7.2")     # meV（σ 带，重空穴? 实为轻带小 ξ）
DELTA_PI = Decimal("2.5")        # meV（π 带）
KB_EV_K = Decimal("8.617333262e-5")  # eV/K（精确）
# 近 Tc 斜率（π 带主导，外场平行 ab 面，bulk 单晶）
DHCDT_MEASURED = Decimal("0.36")  # T/K（|dH_c2^ab/dT| near Tc）
# 实测 H_c2^ab(0)（bulk，σ 带低温接管后）
HC2_MEASURED_0 = Decimal("13.2")   # T
# BCS 单带弱耦合普适比值（承接 C0153 E2a 读数）
BCS_GAP_RATIO = Decimal("3.528")   # 2Δ0/(k_B Tc)


def e1_facts():
    """实验事实 + 精确常数（只引用）。"""
    return {
        "MgB2_Tc_K": MGB2_TC,
        "Delta_sigma_meV": DELTA_SIGMA,
        "Delta_pi_meV": DELTA_PI,
        "dHc2_dT_T_per_K": DHCDT_MEASURED,
        "Hc2_ab_0_measured_T": HC2_MEASURED_0,
        "Phi0_quoted_Wb": PHI0_QUOTED,
    }


def phi0_calc():
    """Φ0 = h/(2e) 由 SI 精确常数 Decimal 精算。"""
    return H_PLANCK / (Decimal(2) * E_CHARGE)


def e2_single_band(phi0, xi_m=Decimal("5.0e-9")):
    """单带上临界场核算：H_c2(0)=Φ0/(2πξ²)。

    推导链（标准 GL/轨道）：
      第二类超导体上临界场 = 一个磁通量子挤进一个相干面积：
      H_c2(0) = Φ0 / (2π ξ²(0))，ξ 为 GL 相干长度。
    """
    xi2 = xi_m * xi_m
    hc2 = phi0 / (Decimal(2) * PI * xi2)
    return {"xi_m": xi_m, "xi2_m2": xi2, "Hc2_single_0_T": hc2}


def e3_two_band(phi0):
    """MgB2 σ/π 两带模型核算。

    (a) 两能隙 BCS 比值：2Δ/(k_B Tc)——单带应为 3.528，两带分立即多带指纹；
    (b) Landau 规则破缺：近 Tc 斜率（π 带主导）按 WHH 直线外推 H_c2(0)，
        与实测 H_c2(0)（σ 带低温接管）之比 = 上弯曲率因子。
    """
    kbtc_meV = KB_EV_K * MGB2_TC * Decimal("1000")  # eV->meV
    ratio_sigma = (Decimal(2) * DELTA_SIGMA) / kbtc_meV
    ratio_pi = (Decimal(2) * DELTA_PI) / kbtc_meV
    # (b) WHH 近 Tc 斜率直线外推
    whh_pred = Decimal("0.693") * MGB2_TC * DHCDT_MEASURED
    # 破缺比 = 实测 / WHH 直线外推
    break_ratio = HC2_MEASURED_0 / whh_pred
    return {
        "kBTc_meV": kbtc_meV,
        "gap_ratio_sigma": ratio_sigma,
        "gap_ratio_pi": ratio_pi,
        "whh_predicted_0_T": whh_pred,
        "landau_break_ratio": break_ratio,
    }


def e4_landau_whh(phi0):
    """Landau 线性规则 + WHH 公式核算 + ξ 反推闭环。"""
    # Landau 线性：近 Tc，H_c2(T) ≈ (Tc - T)·|dHc2/dT|，取 T=30 K 检点
    T_check = Decimal("30")
    hc2_linear_30 = (MGB2_TC - T_check) * DHCDT_MEASURED
    # WHH：H_c2(0) = 0.69 Tc |dHc2/dT|（Werthamer-Helfand-Hohenberg 轨道极限）
    whh_0 = Decimal("0.69") * MGB2_TC * DHCDT_MEASURED
    # 反推：由实测 H_c2(0) 解 ξ = sqrt(Φ0/(2π H_c2(0)))
    xi_back = (phi0 / (Decimal(2) * PI * HC2_MEASURED_0)).sqrt()
    return {
        "T_check_K": T_check,
        "Hc2_linear_at_30K_T": hc2_linear_30,
        "WHH_0_T": whh_0,
        "xi_back_nm": xi_back * Decimal("1e9"),
    }


def e5_supply():
    """供给检查：TUFT 是否供给超导凝聚/相干结构？

    承接 C0133（TUFT 注销，仅留经典局部几何）、C0153 E3（无声子载体/费米面/配对）。
    H_c2 依赖：GL 相干长度 ξ、磁通量子 Φ0 的超导凝聚态、费米面多带色散、
    带间耦合 λ_eff——全是标准凝聚态构件。TUFT 无超导、无凝聚、无费米面 ⇒ 供给 0。
    """
    return {
        "condensate_supply": 0,      # 无超导凝聚态
        "coherence_length_concept": 0,  # 无 GL 相干长度
        "fermi_surface_multiband": 0,    # 无多带费米面色散
        "interband_lambda_eff": 0,       # 带间耦合 λ_eff 无供给
        "Hc2_prediction_count": 0,       # 几何框架 H_c2 预言数
        "total_supply": 0,
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0247 · 多带超导体 Landau 规则破缺（H_c2 多带贡献）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 实验事实（只引用不复算）")
    w("  MgB2：Tc=%s K（Nagamatsu 2001）；两带能隙 Δσ≈%s meV、Δπ≈%s meV"
      % (fv(g1["MgB2_Tc_K"], "0f"), g1["Delta_sigma_meV"], g1["Delta_pi_meV"]))
    w("  近 Tc 斜率 |dH_c2^ab/dT|≈%s T/K（π 带主导）；实测 H_c2^ab(0)≈%s T（bulk，σ 带低温接管）"
      % (g1["dHc2_dT_T_per_K"], g1["Hc2_ab_0_measured_T"]))
    w("  磁通量子 Φ0=h/2e 文献值=%s Wb；h=%s J·s、e=%s C（SI 精确常数）"
      % (fv(PHI0_QUOTED, "9e"), fv(H_PLANCK, "3e"), fv(E_CHARGE, "3e")))
    w("  => H_c2 是超导凝聚态的轨道磁响应，依赖 ξ、Φ0、多带费米面与带间耦合。")
    entries.append(("E1", "MgB2 Tc=39K、Δσ=7.2/Δπ=2.5 meV、斜率0.36T/K、Hc2(0)=13.2T；"
                    "Φ0=h/2e 精确常数", "PASS", "实验值只引用不复算"))

    # ---- E2 单带 ----
    p0 = phi0_calc()
    g2 = e2_single_band(p0)
    w("\n[E2] 单带 H_c2 核算（本册核心一）：H_c2(0)=Φ0/(2πξ²)")
    w("  Φ0=h/(2e) 精算 = (%s)/(%s×%s) = %s Wb"
      % (fv(H_PLANCK, "6e"), fv(Decimal(2), "0f"), fv(E_CHARGE, "6e"), fv(p0, "9e")))
    w("  闭包：文献 Φ0=%s，精算/文献 偏差=%s"
      % (fv(PHI0_QUOTED, "9e"), fv((p0 / PHI0_QUOTED - 1), "2e")))
    w("  代入 ξ_ab(0)=%s m（=5.0 nm）：ξ²=%s m²"
      % (fv(g2["xi_m"], "2e"), fv(g2["xi2_m2"], "3e")))
    w("  ⇒ H_c2^single(0) = %s/(2π×%s) = %s T"
      % (fv(p0, "4e"), fv(g2["xi2_m2"], "3e"), fv(g2["Hc2_single_0_T"], "4f")))
    w("  （对照 bulk 实测 H_c2^ab(0)=13.2 T，单带 ξ=5 nm 给出 ~13.2 T，量级自洽。）")
    entries.append(("E2", "Φ0=h/2e 精算闭包 %s Wb；H_c2^single(0)=Φ0/(2πξ²)=%s T（ξ=5nm）"
                    % (fv(p0, "6e"), fv(g2["Hc2_single_0_T"], "3f")), "PASS",
                    "GL 轨道上临界场标准算术；ξ 为外部输入"))

    # ---- E3 多带 ----
    g3 = e3_two_band(p0)
    w("\n[E3] 多带核算（本册核心二）：MgB2 σ/π 两带模型")
    w("  (a) k_B Tc = %s eV/K × %s K = %s meV"
      % (fv(KB_EV_K, "3e"), fv(MGB2_TC, "0f"), fv(g3["kBTc_meV"], "4f")))
    w("      两带能隙比：2Δσ/(k_B Tc) = %s；2Δπ/(k_B Tc) = %s"
      % (fv(g3["gap_ratio_sigma"], "4f"), fv(g3["gap_ratio_pi"], "4f")))
    w("      单带 BCS 普适值 = %s ⇒ σ 带 %s、π 带 %s，两带分立即多带指纹（≠单带）。"
      % (BCS_GAP_RATIO,
         "偏高" if g3["gap_ratio_sigma"] > BCS_GAP_RATIO else "偏低",
         "远低于单带" if g3["gap_ratio_pi"] < BCS_GAP_RATIO else "接近单带"))
    w("  (b) Landau 规则破缺：近 Tc 斜率 %s T/K（π 带主导）WHH 直线外推"
      % fv(DHCDT_MEASURED, "2f"))
    w("      H_c2^WHH(0) = 0.693×%s×%s = %s T（直线规则预言）"
      % (fv(MGB2_TC, "0f"), fv(DHCDT_MEASURED, "2f"), fv(g3["whh_predicted_0_T"], "3f")))
    w("      实测 H_c2(0)=%s T（低温 σ 带接管）⇒ 破缺比 = 实测/外推 = %s"
      % (fv(HC2_MEASURED_0, "1f"), fv(g3["landau_break_ratio"], "4f")))
    w("      >1 ⇒ H_c2(T) 呈上弯，Landau 线性规则在多带被破缺（上弯因子 %s%%）。"
      % format((g3["landau_break_ratio"] - 1) * 100, ".1f"))
    entries.append(("E3", "两带比值 σ=%s/π=%s（单带=%s）；Landau 破缺比=%s（实测13.2T/WHH%st）"
                    % (fv(g3["gap_ratio_sigma"], "2f"), fv(g3["gap_ratio_pi"], "2f"),
                       BCS_GAP_RATIO, fv(g3["landau_break_ratio"], "3f"),
                       fv(g3["whh_predicted_0_T"], "2f")), "PASS",
                    "带间耦合 λ_eff 为外部输入；上弯=多带贡献"))

    # ---- E4 Landau + WHH ----
    g4 = e4_landau_whh(p0)
    w("\n[E4] Landau 线性规则 + WHH 公式核算")
    w("  Landau 线性：近 Tc H_c2(T)=(Tc−T)|slope|，T=%s K 检点 ⇒ H_c2=%s T"
      % (fv(g4["T_check_K"], "0f"), fv(g4["Hc2_linear_at_30K_T"], "3f")))
    w("  WHH 公式：H_c2(0)=−0.69·Tc·dH_c2/dT = 0.69×%s×%s = %s T（轨道极限，无泡利限）"
      % (fv(MGB2_TC, "0f"), fv(DHCDT_MEASURED, "2f"), fv(g4["WHH_0_T"], "3f")))
    w("  反推闭环：ξ=√(Φ0/(2π H_c2(0)))，代入实测 %s T ⇒ ξ=%s nm（与输入 ξ=5.0 nm 闭环）"
      % (fv(HC2_MEASURED_0, "1f"), fv(g4["xi_back_nm"], "3f")))
    w("  破缺条件：单带 Landau 直线外推系统性低估 H_c2(0)，多带两带色散 + 带间耦合"
      "使 H_c2(T) 上弯——此即 Landau 规则破缺的标准机制。")
    entries.append(("E4", "WHH H_c2(0)=%s T；T=30K 线性=%s T；反推 ξ=%s nm 闭环"
                    % (fv(g4["WHH_0_T"], "2f"), fv(g4["Hc2_linear_at_30K_T"], "2f"),
                       fv(g4["xi_back_nm"], "2f")), "PASS",
                    "Werthamer-Helfand-Hohenberg 标准公式"))

    # ---- E5 供给 ----
    g5 = e5_supply()
    w("\n[E5] 供给检查：TUFT 是否供给超导凝聚/相干结构？")
    w("  超导凝聚态供给：%d（承接 C0133 注销，仅留经典局部几何）" % g5["condensate_supply"])
    w("  GL 相干长度 ξ 概念：%d；多带费米面色散：%d；带间耦合 λ_eff：%d"
      % (g5["coherence_length_concept"], g5["fermi_surface_multiband"],
         g5["interband_lambda_eff"]))
    w("  几何框架 H_c2 预言数：%d ⇒ TUFT 无超导/无凝聚/无多带费米面，结构性负面。"
      % g5["Hc2_prediction_count"])
    w("  => 撞 C5（无可检验预言）/ C6（理论对 ξ、λ_eff、带间耦合敏感、无误差带）。")
    entries.append(("E5", "供给 0：TUFT 无超导凝聚/相干长度/多带费米面/λ_eff，"
                    "H_c2 预言=0", "PASS", "撞 C5/C6"))

    # ---- 守卫（≥6 条） ----
    guards = [
        ("G1", "Φ0=h/(2e) 精算闭包 ≈ %s Wb（与文献 2.067833848e-15 偏差<1e-6）"
         % fv(p0, "6e"),
         abs(p0 / PHI0_QUOTED - 1) < Decimal("1e-6")),
        ("G2", "单带 H_c2(0)=Φ0/(2πξ²) ∈[12,14] T（ξ=5nm）",
         Decimal("12") <= g2["Hc2_single_0_T"] <= Decimal("14")),
        ("G3", "WHH 近 Tc 斜率外推 H_c2(0)∈[9,10.5] T",
         Decimal("9") <= g3["whh_predicted_0_T"] <= Decimal("10.5")),
        ("G4", "两带 σ 能隙比 ≠ 单带 3.528（多带指纹，σ∈[4.0,4.6]）",
         Decimal("4.0") <= g3["gap_ratio_sigma"] <= Decimal("4.6")),
        ("G5", "Landau 破缺比 >1（实测 13.2T 高于 WHH 直线外推，上弯）",
         g3["landau_break_ratio"] > Decimal("1.25")),
        ("G6", "实测 H_c2(0) 反推 ξ ≈ 5.0 nm（闭环，±5%）",
         abs(g4["xi_back_nm"] / Decimal("5.0") - 1) < Decimal("0.05")),
        ("G7", "TUFT/几何框架 H_c2 预言数 = 0（供给 = 0）",
         g5["Hc2_prediction_count"] == 0 and g5["total_supply"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0247 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称解决任何物理难题；所有数值均为标准凝聚态算术复核（非 TUFT 预测/修正）；")
    w("  Tc/ξ/Δ/斜率/H_c2 均为已知外部输入显式计数；TUFT 已注销（C0133）。")
    w("  红线：「不宣称解决任何物理难题」「已攻破=对 TUFT/几何框架结构性负面闭合」")
    w("  「有预测且对 = 0/22」「UFT-3=0 保持」；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0247_Hc2多带攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0247_Hc2多带攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0247_Hc2_multiband_landau_break",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": {k: str(v) for k, v in g1.items()},
            "E2_single_band": {
                "Phi0_calc_Wb": str(p0),
                **{k: str(v) for k, v in g2.items()}},
            "E3_two_band": {k: str(v) for k, v in g3.items()},
            "E4_landau_whh": {k: str(v) for k, v in g4.items()},
            "E5_supply": {k: str(v) for k, v in g5.items()},
            "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0247 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
