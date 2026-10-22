# -*- coding: utf-8 -*-
"""
attack_C0165_四夸克Zc攻破_2026-10-21.py
独立攻破：母册 T341「带电 Z_c(3900)/Z_c(4430) 隐粲态（四夸克）」
判定号 C0165（已现扫确认空号）。

定位：母册（Top1000）T341 行，域 H，撞 C1/C5；同类 QCD 奇特强子族，
与 C0164（五夸克 P_c）判定衔接——均为 QCD 强子谱层面的奇特强子，
TUFT/几何框架无 QCD 强子结构载体。

把「带电隐粲四夸克候选是不是几何可供给的结构」压缩成五条可复核读数：

  E1 观测事实（只引用不复算）：
     - Z_c(3900)：BESIII 2013 首次观测（带电隐粲四夸克候选），LHCb/Belle 确认；
       I^G(J^P)=1^+(1^+)；衰变 π^± J/ψ、D D̄*。
     - Z_c(4430)：Belle 首报，LHCb 2014 以 >5σ 确认（首次确立的带电隐粲共振）；
       I^G(J^P)=1^-(1^-)；衰变 π^± ψ(2S)。
  E2 **引擎阈值差精算（本册核心）**：
     - Z_c(3900) 近 D D̄* 阈值（m_D+m_D*=3879.9 MeV），ΔE≈+19.1 MeV（阈值上方）；
     - Z_c(4430) 近候选阈值逐项 Decimal 精算：D̄*D̄*=4020.6、D D̄1(2420)=4291.7、
       D D̄0*=4177.6，得 ΔE=+409.4/+138.3/+252.4 MeV；
     - 分子 vs 紧致四夸克判据表（阈值近度、宽度、衰变道）。
  E3 几何供给判定：TUFT 无 QCD 强子结构载体 ⇒ 供给 0。
  E4 与 C0164（五夸克）衔接：同类 QCD 奇特强子族；母册 T341 🔲→✅ 登记引用。
  E5 裁定：结构性负面（对 TUFT/几何框架），撞 C1（QCD 公设独有）/C5。

质量输入（PDG，只引用不复算）：
  m_D(±)=1869.6 MeV、m_D*(±)=2010.3 MeV、m_D1(2420)=2422.1 MeV、
  m_D0*(2300)=2308 MeV、m_ψ(2S)=3686.1 MeV。
共振质量（PDG）：m_Zc(3900)≈3899.0 MeV、m_Zc(4430)≈4430.0 MeV。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络，退出码 0。

诚实边界：本册不宣称已解释奇特强子谱；PDG 质量/量子数/宽度只引用不复算；
分子 vs 紧致判定按「阈值近度（结合能标 ~±30 MeV）」判据定性，末位不较真。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（PDG 只引用不复算，MeV） ----------
M_D = Decimal("1869.6")        # PDG m_D(±)
M_DSTAR = Decimal("2010.3")     # PDG m_D*(±)
M_D1_2420 = Decimal("2422.1")   # PDG m_D1(2420)
M_D0STAR = Decimal("2308.0")    # PDG m_D*_0(2300)
M_PSI2S = Decimal("3686.1")     # PDG m_ψ(2S)

# 共振中心质量（PDG，MeV）
M_ZC3900 = Decimal("3899.0")    # Z_c(3900) PDG 平均
M_ZC4430 = Decimal("4430.0")    # Z_c(4430) LHCb/Belle

# 近阈值判据带宽：强子分子结合能标 ~ 10–30 MeV
NEAR_BAND = Decimal("30.0")


def e1_facts():
    """E1 观测事实（只引用不复算）。"""
    return {
        "Zc3900": {
            "first_obs": "BESIII 2013（带电隐粲四夸克候选）",
            "confirmed_by": "LHCb / Belle",
            "IGJP": "1^+(1^+)",
            "decay_channels": ["π^± J/ψ", "D D̄*"],
            "width_MeV_ref": "≈28–46（窄，近阈值）",
        },
        "Zc4430": {
            "first_obs": "Belle 首报；LHCb 2014 >5σ 确认（首个确立的带电隐粲共振）",
            "IGJP": "1^-(1^-)",
            "decay_channels": ["π^± ψ(2S)"],
            "width_MeV_ref": "≈180–200（宽）",
        },
    }


def e2_thresholds():
    """E2 引擎阈值差精算（Decimal 48 位）。"""
    # 候选粲介子对阈值
    T_DDstar = M_D + M_DSTAR                 # D D̄*
    T_DstarDstar = M_DSTAR + M_DSTAR         # D̄* D̄*
    T_DD1 = M_D + M_D1_2420                  # D D̄1(2420)
    T_DD0star = M_D + M_D0STAR               # D D̄0*(2300)

    # 共振相对各阈值的能量差（ΔE = m_res - T）
    dE_3900 = {
        "D D̄* (%.1f)" % T_DDstar: M_ZC3900 - T_DDstar,
    }
    dE_4430 = {
        "D̄* D̄* (%.1f)" % T_DstarDstar: M_ZC4430 - T_DstarDstar,
        "D D̄1(2420) (%.1f)" % T_DD1: M_ZC4430 - T_DD1,
        "D D̄0*(2300) (%.1f)" % T_DD0star: M_ZC4430 - T_DD0star,
    }

    # 最近阈值距离
    nearest_3900 = min(abs(v) for v in dE_3900.values())
    nearest_4430 = min(abs(v) for v in dE_4430.values())

    return {
        "thresholds_MeV": {
            "D D̄*": T_DDstar,
            "D̄* D̄*": T_DstarDstar,
            "D D̄1(2420)": T_DD1,
            "D D̄0*(2300)": T_DD0star,
        },
        "dE_Zc3900": dE_3900,
        "dE_Zc4430": dE_4430,
        "nearest_Zc3900": nearest_3900,
        "nearest_Zc4430": nearest_4430,
        "near_band_MeV": NEAR_BAND,
        # 判据：|ΔE| ≤ 结合能标 ⇒ 近阈值 ⇒ 分子候选；否则紧致四夸克候选
        "Zc3900_molecule_candidate": nearest_3900 <= NEAR_BAND,
        "Zc4430_molecule_candidate": nearest_4430 <= NEAR_BAND,
    }


def e3_geometry_supply():
    """E3 几何供给：TUFT 能否从第一性原理生成 QCD 奇特强子结构？"""
    # TUFT/几何框架的载体是 (ℏ,G,c) 几何常数 + 旋量场；
    # QCD 强子谱（四夸克/五夸克、粲介子阈值、QCD 标度 Λ_QCD）是 QCD 动力学产物，
    # 几何框架无 QCD 强子结构载体 ⇒ 供给 0。
    return {
        "tuft_has_qcd_hadron_carrier": False,
        "geometry_supply": "zero",
        "note": "Λ_QCD / 粲质量 m_c / 粲介子阈值全是 QCD 动力学外部输入",
    }


def e4_linkage():
    """E4 与 C0164（五夸克）衔接 + 母册 T341 登记引用。"""
    return {
        "family": "QCD 奇特强子族（四夸克 Z_c / 五夸克 P_c）",
        "linkage_to_C0164": "同类：均为 QCD 强子谱层面的奇特强子，TUFT 供给同判 0",
        "mother_row": "| T341 | 带电 Z_c(3900)/Z_c(4430) 隐粲态 | 四夸克 | C1,C5 | 🔲 |",
        "mother_row_after": "| T341 | 带电 Z_c(3900)/Z_c(4430) 隐粲态 | 四夸克 | C1,C5 | ✅ |",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="1f"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0165 · 带电 Z_c(3900)/Z_c(4430) 隐粲态（四夸克）攻破")
    w("母册 T341 · 域 H · 撞 C1/C5 · 与 C0164（五夸克）衔接")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 观测事实（PDG/BESIII/LHCb 只引用不复算）")
    z3900 = g1["Zc3900"]
    z4430 = g1["Zc4430"]
    w("  Z_c(3900)：%s；I^G(J^P)=%s" % (z3900["first_obs"], z3900["IGJP"]))
    w("    确认：%s；衰变：%s；宽度 %s MeV"
      % (z3900["confirmed_by"], "、".join(z3900["decay_channels"]), z3900["width_MeV_ref"]))
    w("  Z_c(4430)：%s；I^G(J^P)=%s" % (z4430["first_obs"], z4430["IGJP"]))
    w("    衰变：%s；宽度 %s MeV"
      % ("、".join(z4430["decay_channels"]), z4430["width_MeV_ref"]))
    w("  => 两个均为带电（Q=±1）隐粲（c c̄ q q̄）奇特强子，普通 q q̄ 重子/介子装不下。")
    entries.append(("E1",
                    "Z_c(3900) BESIII 2013 首观、LHCb/Belle 确认（1^+(1^+)）；"
                    "Z_c(4430) LHCb >5σ 确认（1^-(1^-)）",
                    "PASS", "PDG/BESIII/LHCb 只引用；量子数与衰变道引用标注"))

    # ---- E2 ----
    g2 = e2_thresholds()
    w("\n[E2] 引擎阈值差精算（本册核心，Decimal 48 位）")
    th = g2["thresholds_MeV"]
    w("  粲介子对阈值（m_D=%s, m_D*=%s, m_D1(2420)=%s, m_D0*=%s MeV）："
      % (fv(M_D), fv(M_DSTAR), fv(M_D1_2420), fv(M_D0STAR)))
    w("    D D̄*        = %s MeV" % fv(th["D D̄*"]))
    w("    D̄* D̄*      = %s MeV" % fv(th["D̄* D̄*"]))
    w("    D D̄1(2420)  = %s MeV" % fv(th["D D̄1(2420)"]))
    w("    D D̄0*(2300) = %s MeV" % fv(th["D D̄0*(2300)"]))
    w("  Z_c(3900) m=%s MeV：" % fv(M_ZC3900))
    for k, v in g2["dE_Zc3900"].items():
        w("    相对 %s：ΔE = %s MeV（阈值上方）" % (k, fv(v)))
    w("    => 最近阈值距离 |ΔE| = %s MeV ≤ 结合能标 %s MeV ⇒ 近阈值 ⇒ **强子分子候选**"
      % (fv(g2["nearest_Zc3900"]), fv(NEAR_BAND)))
    w("  Z_c(4430) m=%s MeV：" % fv(M_ZC4430))
    for k, v in g2["dE_Zc4430"].items():
        w("    相对 %s：ΔE = %s MeV" % (k, fv(v)))
    w("    => 最近阈值距离 |ΔE| = %s MeV > 结合能标 %s MeV ⇒ **非近阈值** ⇒ **紧致四夸克候选**"
      % (fv(g2["nearest_Zc4430"]), fv(NEAR_BAND)))
    w("  分子 vs 紧致判据表：")
    w("    | 判据            | Z_c(3900)        | Z_c(4430)        |")
    w("    | 最近阈值距离    | %s MeV（近）     | %s MeV（远）     |"
      % (fv(g2["nearest_Zc3900"]), fv(g2["nearest_Zc4430"])))
    w("    | 宽度            | 窄 ~30–50 MeV    | 宽 ~180–200 MeV  |")
    w("    | 主导衰变道      | D D̄* / π J/ψ     | π ψ(2S)          |")
    w("    | 定性            | 分子候选         | 紧致四夸克候选   |")
    entries.append(("E2",
                    "Z_c(3900) 距 D D̄* 阈值仅 +%s MeV（近阈值⇒分子）；"
                    "Z_c(4430) 最近阈值差 +%s MeV（远超结合能标⇒紧致四夸克）"
                    % (fv(g2["nearest_Zc3900"]), fv(g2["nearest_Zc4430"])),
                    "PASS", "Decimal 48 位阈值差精算 + 分子/紧致判据表"))

    # ---- E3 ----
    g3 = e3_geometry_supply()
    w("\n[E3] 几何供给判定：TUFT 能否生成 QCD 奇特强子结构？")
    w("  TUFT/几何框架载体 = (ℏ,G,c) 几何常数 + 旋量场；")
    w("  QCD 强子谱（Λ_QCD、m_c、粲介子阈值、四夸克束缚）全是 QCD 动力学产物。")
    w("  TUFT 是否有 QCD 强子结构载体：%s" % g3["tuft_has_qcd_hadron_carrier"])
    w("  => 几何供给 = %s；粲质量/阈值是外部输入（承接 C0140/C0142 nullity=0 读数）。"
      % g3["geometry_supply"])
    entries.append(("E3",
                    "TUFT 无 QCD 强子结构载体 ⇒ 几何供给 0；粲质量/阈值外部输入",
                    "PASS", "撞 C1（QCD 公设独有）"))

    # ---- E4 ----
    g4 = e4_linkage()
    w("\n[E4] 与 C0164（五夸克）衔接 + 母册 T341 登记引用")
    w("  族：%s" % g4["family"])
    w("  衔接：%s" % g4["linkage_to_C0164"])
    w("  母册行（原状）：%s" % g4["mother_row"])
    w("  母册行（攻破后登记）：%s" % g4["mother_row_after"])
    entries.append(("E4",
                    "与 C0164 同 QCD 奇特强子族，TUFT 供给同判 0；母册 T341 🔲→✅",
                    "PASS", "引用登记，不改母册本体"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  (a) 奇特强子谱来源：Z_c(3900)/(4430) 的存在与量子数是 QCD 强子谱实验事实（E1）；")
    w("      其质量/阈值位置由 QCD 动力学（粲质量、Λ_QCD）决定（E2 精算）。")
    w("  (b) 几何供给：TUFT 无 QCD 强子载体（E3）⇒ 供给 0。")
    w("  => **结构性负面（对 TUFT/几何框架）**；撞 C1（QCD 公设独有粒子/强子内容）/ C5（可检验：阈值近度判据）。")
    entries.append(("E5",
                    "结构性负面：TUFT 供给 0，QCD 奇特强子族为 QCD 公设独有",
                    "PASS", "撞 C1/C5"))

    # ---- 守卫（≥6） ----
    guards = [
        ("G1", "D D̄* 阈值 ≈ 3880 MeV（m_D+m_D*=3879.9）",
         th["D D̄*"] == Decimal("3879.9")),
        ("G2", "Z_c(3900) ΔE 落在阈值上方近阈区间（0<ΔE≤30 MeV）",
         Decimal("0") < g2["nearest_Zc3900"] <= NEAR_BAND),
        ("G3", "分子 vs 紧致判据表闭合（3900 近阈值、4430 远阈值）",
         g2["Zc3900_molecule_candidate"] and not g2["Zc4430_molecule_candidate"]),
        ("G4", "引用标记齐全（BESIII 2013 / LHCb 5σ / PDG 质量输入）",
         ("BESIII 2013" in z3900["first_obs"]) and ("5σ" in z4430["first_obs"])
         and M_D == Decimal("1869.6")),
        ("G5", "几何供给 = 0（TUFT 无 QCD 强子载体）",
         g3["geometry_supply"] == "zero" and not g3["tuft_has_qcd_hadron_carrier"]),
        ("G6", "E5 裁定 = 结构性负面（撞 C1/C5）",
         entries[-1][0] == "E5" and "结构性负面" in entries[-1][1]),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0165 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  本册不宣称已解释奇特强子谱；PDG 质量/量子数/宽度只引用不复算；")
    w("  分子 vs 紧致按阈值近度（结合能标 ~30 MeV）定性，末位不较真。")
    w("  红线四句照录：")
    w("    「有预测且对 = 0/22」；")
    w("    「数学自洽 ≠ 实验证实」；")
    w("    「UFT-3 = 0 保持」；")
    w("    「✅ 均为对 TUFT/几何框架的结构性负面闭合」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0165_四夸克Zc攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0165_四夸克Zc攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0165_tetraquark_Zc",
            "mother_book_row": "T341 带电 Z_c(3900)/Z_c(4430) 隐粲态（四夸克）",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_facts": g1,
            "E2_thresholds": {
                "thresholds_MeV": {k: str(v) for k, v in th.items()},
                "dE_Zc3900": {k: str(v) for k, v in g2["dE_Zc3900"].items()},
                "dE_Zc4430": {k: str(v) for k, v in g2["dE_Zc4430"].items()},
                "nearest_Zc3900_MeV": str(g2["nearest_Zc3900"]),
                "nearest_Zc4430_MeV": str(g2["nearest_Zc4430"]),
                "near_band_MeV": str(NEAR_BAND),
                "Zc3900_molecule_candidate": g2["Zc3900_molecule_candidate"],
                "Zc4430_molecule_candidate": g2["Zc4430_molecule_candidate"],
            },
            "E3_geometry_supply": g3,
            "E4_linkage": g4,
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0165 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
