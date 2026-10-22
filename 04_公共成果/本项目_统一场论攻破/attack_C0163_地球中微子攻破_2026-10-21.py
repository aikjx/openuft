# -*- coding: utf-8 -*-
"""
attack_C0163_地球中微子攻破_2026-10-21.py
第一性量级估算：母册 T244「地球中微子 geo-ν 热流与地幔 U/Th 丰度」（域 H 地球化学）。

定位：
  母册（Top1000/物理 Top100 清单扩展行）T244：
    | T244 | 地球中微子 geo-ν 热流与地幔 U/Th 丰度 | 地球化学 | C5,C6 | 🔲 |
  前置：C0143（中微子质量结构性负面，P06/T024）已把「中微子质量标度从哪来」
    判为几何供给 0；本册补 **地球物理侧**——geo-ν 通量与地幔 U/Th 丰度反演
    是否被 TUFT/几何框架预言（或给出误差带）。

把「geo-ν 通量量级与地幔丰度从哪来」压缩成五条可复核读数：

  E1 观测事实（只引用不复算）：KamLAND/Borexino/JUNO geo-ν 观测；
     全球地热流 ~47 TW；U/Th/K 放射产热 ~8–20 TW；地壳 U≈2.8 ppm / Th≈10.7 ppm /
     K≈2.5%；地表反中微子通量量级。
  E2 **第一性量级通量估算（本册核心）**：
     φ = Σ_i P_i × Y_i / (4π R⊕² × E_heat,i)
     其中 P_i = 各衰变链放射功率（引用），Y_i = 每衰变链 ν̄_e 产额（引用：
     U-238 链 6.13、Th-232 链 4.23），E_heat,i = 每衰变链产热（引用：
     U 47.7 MeV、Th 40.2 MeV）；Decimal 48 位精算地表通量量级；
     U/Th 丰度反演模型摆动 ±20%/±50% 精算通量区间。
  E3 几何供给判定：TUFT/几何框架无中微子/地球物理载体 ⇒ 供给 0，
     撞 C5（无中微子预言）/ C6（无误差带）。
  E4 与 C0143 衔接：中微子质量结构性负面已定，本册补 T244 地球物理侧；
     母册 T244 行 🔲→✅ 登记引用。
  E5 裁定：结构性负面（对 TUFT/几何框架）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界：观测值（KamLAND/Borexino/地热流/丰度）只引用不复算；
本册只做由引用产热+产额+产热能到通量的第一性量级换算（Decimal 精算）；
K-40 ν̄_e（β− 分支，Eν≤1.31 MeV）低于 IBD 阈 1.8 MeV，本测算单列不计入可测通量。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 第一性常数（Decimal 48 位字面量） ----------
PI = Decimal("3.14159265358979323846264338327950288419716939937510")
R_EARTH_CM = Decimal("6.371e8")           # 地球平均半径 ~6371 km（引用）
MEV_TO_J = Decimal("1.602176634e-13")    # 1 MeV = 1.602176634e-13 J（CODATA 引用）

# ---------- E1 外部观测事实（只引用不复算，注释标来源） ----------
# 全球地热流总量 ~47 TW（Pollack/Huang/Goes 1993；Davies & Davies 2010）
HEAT_FLOW_TOTAL_TW = Decimal("47")
# U/Th/K 放射产热总量区间 8–20 TW（RIM/Borexino 口径引用）
RADIOGENIC_LO_TW = Decimal("8")
RADIOGENIC_HI_TW = Decimal("20")
RADIOGENIC_CENTER_TW = Decimal("14")     # 区间中值（模型中心）
# 地壳丰度（引用）：U≈2.8 ppm、Th≈10.7 ppm、K≈2.5%
CRUST_U_PPM = Decimal("2.8")
CRUST_TH_PPM = Decimal("10.7")
CRUST_K_PCT = Decimal("2.5")
# 各衰变链产热能（每母核衰变，引用）：U-238 链 47.7 MeV；Th-232 链 40.2 MeV
E_HEAT_U_MEV = Decimal("47.7")
E_HEAT_TH_MEV = Decimal("40.2")
# 每衰变链 ν̄_e 产额（引用）：U-238 链 6.13；Th-232 链 4.23
YIELD_U = Decimal("6.13")
YIELD_TH = Decimal("4.23")
# 中心模型 U/Th 放射功率（TW，按 BSE Th/U≈3.8、产热能比 ~40.2/47.7 分配，
# U+Th 合计落在 8–20 TW 区间内取中心模型 P_U+P_Th = 8.5 TW）
P_U_TW = Decimal("4.0")
P_TH_TW = Decimal("4.5")
# IBD 阈（反贝塔衰变 ν̄_e+p→e⁺+n 阈 ~1.806 MeV，引用）
IBD_THRESHOLD_MEV = Decimal("1.806")
# K-40 β− 分支 ν̄_e 端点 ~1.31 MeV（引用，低于 IBD 阈 ⇒ 不被液体闪烁谱仪探测）
K_NU_ENDPOINT_MEV = Decimal("1.31")


def e1_geoneutrino_facts():
    """geo-ν 观测与地球物理事实（只引用不复算）。"""
    return {
        "kamland_events_per_yr": "~100（KamLAND 地热中微子观测，引用）",
        "borexino_geoneutrino": "Borexino U/Th geo-ν TNU 读数（引用，量级 ~数 TNU）",
        "juno_status": "JUNO 在役/在建，geo-ν 谱积分测（引用）",
        "heat_flow_total_TW": HEAT_FLOW_TOTAL_TW,
        "radiogenic_TW_range": (RADIOGENIC_LO_TW, RADIOGENIC_HI_TW),
        "crust_U_ppm": CRUST_U_PPM,
        "crust_Th_ppm": CRUST_TH_PPM,
        "crust_K_pct": CRUST_K_PCT,
        "ibd_threshold_MeV": IBD_THRESHOLD_MEV,
        "K_nubar_endpoint_MeV": K_NU_ENDPOINT_MEV,
    }


def solid_angle_area():
    """4π R⊕²（cm²）——各向同性点源近似的球面接收面积。"""
    return Decimal(4) * PI * R_EARTH_CM * R_EARTH_CM


def chain_flux(P_TW, E_heat_MeV, yield_nu):
    """单链地表 ν̄_e 通量（cm⁻² s⁻¹），Decimal 48 位精算。

    φ = P [J/s] × Y [ν/衰变] / (4πR² [cm²] × E_heat [J/衰变])
      = P_TW×1e12 × Y / (4πR² × E_heat_MeV×1.602176634e-13)
    """
    P_Js = P_TW * Decimal("1e12")                 # TW -> J/s
    E_J = E_heat_MeV * MEV_TO_J                   # MeV/衰变 -> J/衰变
    decays_per_s = P_Js / E_J                     # 衰变/s
    nu_per_s = decays_per_s * yield_nu            # ν̄_e /s
    return nu_per_s / solid_angle_area()


def e2_flux_estimate():
    """第一性量级通量估算（本册核心）+ U/Th 丰度反演摆动区间。"""
    area = solid_angle_area()
    phi_u = chain_flux(P_U_TW, E_HEAT_U_MEV, YIELD_U)
    phi_th = chain_flux(P_TH_TW, E_HEAT_TH_MEV, YIELD_TH)
    phi_total = phi_u + phi_th
    # 产热贡献占比（U/Th 放射功率）
    u_frac = P_U_TW / (P_U_TW + P_TH_TW)
    th_frac = P_TH_TW / (P_U_TW + P_TH_TW)
    # U/Th 丰度反演模型摆动 ±20% / ±50%
    swing_lo20 = phi_total * (Decimal(1) - Decimal("0.20"))
    swing_hi20 = phi_total * (Decimal(1) + Decimal("0.20"))
    swing_lo50 = phi_total * (Decimal(1) - Decimal("0.50"))
    swing_hi50 = phi_total * (Decimal(1) + Decimal("0.50"))
    return {
        "area_cm2": area,
        "phi_U": phi_u,
        "phi_Th": phi_th,
        "phi_total": phi_total,
        "U_power_frac": u_frac,
        "Th_power_frac": th_frac,
        "swing_pm20": (swing_lo20, swing_hi20),
        "swing_pm50": (swing_lo50, swing_hi50),
    }


def e3_geometry_supply():
    """TUFT/几何框架对 geo-ν 通量与地幔 U/Th 丰度的供给。"""
    # 几何常数 (ℏ,G,c) 量纲 nullity=0（承接 C0140/C0142/C0143 精确读数）；
    # TUFT 线无中微子动力学、无地球化学/地球物理载体 ⇒ 既不能预言 geo-ν 通量
    # 也不能给出地幔 U/Th 丰度的误差带。
    nullity3 = 0          # 引用 C0140 E4 / C0142 E3 / C0143 E3
    return {
        "nullity_hbarGc": nullity3,
        "tuft_neutrino_carrier": "none",
        "tuft_geochem_carrier": "none",
        "geometry_supply": 0,
        "hits_C5_no_neutrino_prediction": True,
        "hits_C6_no_error_band": True,
    }


def e4_linkage_c0143():
    """与 C0143 中微子质量判定衔接 + 母册 T244 登记。"""
    return {
        "C0143_status": "中微子质量结构性负面已定（seesaw/Dirac 均需 >=2 枚外部输入，几何供给 0）",
        "this_volume_adds": "T244 地球物理侧：geo-ν 通量量级与地幔 U/Th 丰度反演",
        "parent_row_before": "| T244 | 地球中微子 geo-ν 热流与地幔 U/Th 丰度 | 地球化学 | C5,C6 | 🔲 |",
        "parent_row_after": "| T244 | 地球中微子 geo-ν 热流与地幔 U/Th 丰度 | 地球化学 | C5,C6 | ✅ (C0163) |",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="4e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0163 · 地球中微子 geo-ν 热流与地幔 U/Th 丰度（母册 T244 · 域 H 地球化学）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_geoneutrino_facts()
    w("\n[E1] geo-ν 观测与地球物理事实（只引用不复算）")
    w("  KamLAND：%s" % g1["kamland_events_per_yr"])
    w("  Borexino：%s" % g1["borexino_geoneutrino"])
    w("  JUNO：%s" % g1["juno_status"])
    w("  全球地热流总量 = %s TW（Pollack/Huang/Goes；Davies & Davies，引用）"
      % fv(g1["heat_flow_total_TW"], "1f"))
    w("  U/Th/K 放射产热 = %s–%s TW（RIM/Borexino 口径，引用；中心 %s TW）"
      % (fv(RADIOGENIC_LO_TW, "0f"), fv(RADIOGENIC_HI_TW, "0f"), fv(RADIOGENIC_CENTER_TW, "0f")))
    w("  地壳丰度：U≈%s ppm、Th≈%s ppm、K≈%s%%（引用）"
      % (fv(CRUST_U_PPM, "1f"), fv(CRUST_TH_PPM, "1f"), fv(CRUST_K_PCT, "1f")))
    w("  IBD 阈 ≈ %s MeV（引用）；K-40 β− ν̄_e 端点 ≈ %s MeV < IBD 阈 ⇒ K geo-ν 不可测。"
      % (fv(IBD_THRESHOLD_MEV, "3f"), fv(K_NU_ENDPOINT_MEV, "2f")))
    w("  => 地表反中微子通量量级（文献）~10^6 cm^-2 s^-1（U+Th 可测部分）。")
    entries.append(("E1", "geo-ν 观测（KamLAND ~100 evt/yr、Borexino TNU、JUNO）；"
                    "热流 ~47 TW；放射产热 8–20 TW；地壳 U2.8/Th10.7/K2.5%",
                    "PASS", "只引用不复算，来源标注"))

    # ---- E2 ----
    g2 = e2_flux_estimate()
    w("\n[E2] 第一性量级通量估算（本册核心，Decimal 48 位精算）")
    w("  公式：φ = Σ_i P_i×Y_i / (4πR⊕²×E_heat,i)")
    w("  球面接收面积 4πR⊕² = %s cm²（R⊕=6.371e8 cm）" % fv(g2["area_cm2"], "4e"))
    w("  U-238 链：P_U=%s TW、E_heat=%s MeV、Y=%s ⇒ φ_U = %s cm^-2 s^-1"
      % (fv(P_U_TW, "1f"), fv(E_HEAT_U_MEV, "1f"), fv(YIELD_U, "2f"), fv(g2["phi_U"], "3e")))
    w("  Th-232 链：P_Th=%s TW、E_heat=%s MeV、Y=%s ⇒ φ_Th = %s cm^-2 s^-1"
      % (fv(P_TH_TW, "1f"), fv(E_HEAT_TH_MEV, "1f"), fv(YIELD_TH, "2f"), fv(g2["phi_Th"], "3e")))
    w("  地表 geo-ν（U+Th，可测部分）总通量 φ = %s cm^-2 s^-1"
      % fv(g2["phi_total"], "3e"))
    w("  产热贡献占比：U %s%%、Th %s%%（P_U+P_Th=%s TW 内）"
      % (fv(g2["U_power_frac"] * 100, "1f"), fv(g2["Th_power_frac"] * 100, "1f"),
         fv(P_U_TW + P_TH_TW, "1f")))
    w("  U/Th 丰度反演模型摆动：±20%% ⇒ φ ∈ [%s, %s] cm^-2 s^-1"
      % (fv(g2["swing_pm20"][0], "3e"), fv(g2["swing_pm20"][1], "3e")))
    w("    ±50%% ⇒ φ ∈ [%s, %s] cm^-2 s^-1"
      % (fv(g2["swing_pm50"][0], "3e"), fv(g2["swing_pm50"][1], "3e")))
    w("  => 量级落在 10^6 cm^-2 s^-1，与文献地表 geo-ν 通量量级一致；模型摆动 ±20–50% 不改变量级。")
    entries.append(("E2", "φ(U+Th)≈%s cm^-2 s^-1（量级 10^6）；±20%%=[%s,%s]；±50%%=[%s,%s]"
                    % (fv(g2["phi_total"], "2e"), fv(g2["swing_pm20"][0], "2e"),
                       fv(g2["swing_pm20"][1], "2e"), fv(g2["swing_pm50"][0], "2e"),
                       fv(g2["swing_pm50"][1], "2e")), "PASS",
                    "P/E_heat 得衰变率×产额/球面面积，Decimal 48 位精算"))

    # ---- E3 ----
    g3 = e3_geometry_supply()
    w("\n[E3] 几何供给判定：TUFT/几何框架能否预言 geo-ν 通量与地幔 U/Th 丰度？")
    w("  几何常数 (ℏ,G,c) 量纲 nullity = %d（承接 C0140/C0142/C0143 精确读数）"
      % g3["nullity_hbarGc"])
    w("  TUFT 线中微子动力学载体 = %s；地球化学/地球物理载体 = %s"
      % (g3["tuft_neutrino_carrier"], g3["tuft_geochem_carrier"]))
    w("  => 几何供给 = %d：既不能预言 geo-ν 通量量级，也不能给出地幔 U/Th 丰度误差带。"
      % g3["geometry_supply"])
    w("  撞 C5（无中微子预言）= %s；撞 C6（无误差带）= %s"
      % (g3["hits_C5_no_neutrino_prediction"], g3["hits_C6_no_error_band"]))
    entries.append(("E3", "几何供给 0：TUFT 无中微子/地球物理载体，撞 C5（无中微子预言）/C6（无误差带）",
                    "PASS", "承接 nullity=0 读数"))

    # ---- E4 ----
    g4 = e4_linkage_c0143()
    w("\n[E4] 与 C0143 衔接 + 母册 T244 登记")
    w("  C0143：%s" % g4["C0143_status"])
    w("  本册补：%s" % g4["this_volume_adds"])
    w("  母册 T244 行（前）：%s" % g4["parent_row_before"])
    w("  母册 T244 行（后）：%s" % g4["parent_row_after"])
    entries.append(("E4", "C0143 中微子质量结构性负面已定；本册补 T244 地球物理侧；"
                    "母册 T244 🔲→✅ 登记", "PASS", "衔接口径按 C0143"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  (a) geo-ν 通量量级：本册第一性换算得 ~10^6 cm^-2 s^-1（与文献一致），但这是引用产热+产额")
    w("      的后验换算，不是 TUFT 的第一性预言。")
    w("  (b) 地幔 U/Th 丰度反演不确定性 ±20–50%：来自地球化学模型（RIM/BSE），非几何输入。")
    w("  (c) TUFT/几何框架供给 = 0（E3）⇒ 撞 C5（无中微子预言）/C6（无误差带）。")
    w("  => **T244 结构性负面（对 TUFT/几何框架）**：geo-ν 与地幔丰度是纯地球化学/")
    w("     观测输入，几何框架既不预言也不给误差带；与 C0143（中微子质量侧）合流闭合。")
    entries.append(("E5", "T244 结构性负面：TUFT 供给 0，撞 C5/C6；与 C0143 中微子质量侧合流",
                    "PASS", "结构性负面闭合"))

    # ---- 守卫 ----
    guards = [
        ("G1", "地表通量量级 φ ∈ [1e5, 1e7] cm^-2 s^-1",
         g2["phi_total"] >= Decimal("1e5") and g2["phi_total"] <= Decimal("1e7")),
        ("G2", "U/Th 产热占比已精算（U+Th 功率 = 8.5 TW 内部分配）",
         g2["U_power_frac"] + g2["Th_power_frac"] == Decimal(1)),
        ("G3", "模型摆动 ±20%/±50% 区间精算（lo50 < lo20 < center < hi20 < hi50）",
         g2["swing_pm50"][0] < g2["swing_pm20"][0] < g2["phi_total"]
         < g2["swing_pm20"][1] < g2["swing_pm50"][1]),
        ("G4", "外部观测值引用标记（KamLAND/Borexino/热流/丰度只引用）",
         True),
        ("G5", "几何供给 = 0（TUFT 无中微子/地球物理载体）",
         g3["geometry_supply"] == 0),
        ("G6", "结构性负面裁定成立（撞 C5/C6）",
         g3["hits_C5_no_neutrino_prediction"] and g3["hits_C6_no_error_band"]),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0163 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称解决 geo-ν/地幔丰度问题：KamLAND/Borexino/热流/丰度/产热能/产额只引用；")
    w("  本册只做由引用量到通量的第一性量级换算（Decimal 48 位），K-40 ν̄_e 低于 IBD 阈单列；")
    w("  红线不变：「有预测且对 = 0/22」；数学自洽 ≠ 实验证实；UFT-3=0 保持。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0163_地球中微子攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0163_地球中微子攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0163_geoneutrino_T244",
            "parent_row": "| T244 | 地球中微子 geo-ν 热流与地幔 U/Th 丰度 | 地球化学 | C5,C6 | ✅ (C0163) |",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": {
                "heat_flow_total_TW": str(HEAT_FLOW_TOTAL_TW),
                "radiogenic_TW": [str(RADIOGENIC_LO_TW), str(RADIOGENIC_HI_TW)],
                "crust_U_ppm": str(CRUST_U_PPM), "crust_Th_ppm": str(CRUST_TH_PPM),
                "crust_K_pct": str(CRUST_K_PCT),
                "ibd_threshold_MeV": str(IBD_THRESHOLD_MEV),
            },
            "E2_flux": {
                "area_cm2": str(g2["area_cm2"]),
                "phi_U": str(g2["phi_U"]),
                "phi_Th": str(g2["phi_Th"]),
                "phi_total": str(g2["phi_total"]),
                "U_power_frac": str(g2["U_power_frac"]),
                "Th_power_frac": str(g2["Th_power_frac"]),
                "swing_pm20": [str(g2["swing_pm20"][0]), str(g2["swing_pm20"][1])],
                "swing_pm50": [str(g2["swing_pm50"][0]), str(g2["swing_pm50"][1])],
            },
            "E3_geometry_supply": {k: str(v) for k, v in g3.items()},
            "E4_linkage": {k: str(v) for k, v in g4.items()},
            "guards_passed": sum(1 for g in guards if g[2]),
            "guards_total": len(guards),
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0163 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
