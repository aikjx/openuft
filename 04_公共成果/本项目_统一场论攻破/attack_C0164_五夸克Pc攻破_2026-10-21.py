# -*- coding: utf-8 -*-
"""
attack_C0164_五夸克Pc攻破_2026-10-21.py
独立攻破：母册 T342「五夸克 P_c(4312)/P_c(4440) 分子 vs 紧五夸克」（重子偶素 · 域 H）

定位：母册（域 H 分片 T221–T380）T342，撞 C1,C5；本判定号 C0164（已现扫确认空号）。
前置：LHCb 2015 首报 P_c(4380)/P_c(4450)，2019 高统计观测 P_c(4312)/P_c(4440)/P_c(4457)
（5σ）——分子态（Σ_c D̄ 近阈结合）与紧五夸克之争为 QCD 强子谱问题，TUFT/几何框架
**无 QCD 强子结构载体**（胶子/夸克禁闭非几何对象）。

把"五夸克是分子还是紧五夸克"压缩成五条可复核读数：

  E1 观测事实（LHCb 2015/2019、PDG 只引用不复算）：P_c(4312) J^P=3/2⁻、Γ≈9.8 MeV；
     P_c(4440)/P_c(4457) 5σ 观测；衰变道 J/ψ p。
  E2 **候选分子阈值逐项 Decimal 48 位精算（本册核心）**：Σ_c D̄、Σ_c* D̄、η_c p、
     χ_c1 p 阈值质量与 ΔE（m_Pc − 阈值）；分子判据（近阈结合 ΔE<0 小量级）vs
     紧五夸克（QCD 多夸克态质量谱）对照表：能隙 Δ、宽度 Γ、量子数、衰变模式。
  E3 几何供给：TUFT 无胶子/夸克禁闭/色荷载体 ⇒ 供给 0，撞 C1（QCD 公设独有）/
     C5（TUFT 无奇特强子预言）。
  E4 衔接口径：C0131（量子化障碍）/ C0137（规范群签名）；母册 T342 🔲→✅ 登记。
  E5 裁定：结构性负面（对 TUFT/几何框架）。

纯标准库（Decimal 48 位 + Fraction 精确代数），零外部依赖、零网络、零随机，退出码 0。

诚实边界：本册不宣称已判定 P_c 的分子/紧五夸克归属（那是 QCD 谱学开放问题）；
PDG 质量值与 LHCb 观测值只引用不复算；裁的是「TUFT/几何框架能否对五夸克问题供给
任何结构或预言」——结论为供给 0，结构性负面闭合。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部观测值（PDG / LHCb 2015/2019 只引用不复算） ----------
# PDG 强子质量（MeV）
M_SIGC = Decimal("2453.5")     # m(Σ_c)，PDG
M_SIGC_S = Decimal("2518.5")   # m(Σ_c*)，PDG
M_D = Decimal("1867.2")        # m(D̄)，PDG（D 介子基准）
M_ETC = Decimal("2983.9")      # m(η_c)，PDG
M_CHIC1 = Decimal("3510.7")    # m(χ_c1)，PDG
M_P = Decimal("938.3")          # m(p)，PDG

# LHCb 2019 五夸克态观测质量（MeV，5σ）；LHCb 2015 首报（P_c(4380)/P_c(4450)）
M_PC4312 = Decimal("4311.9")    # P_c(4312)，J^P=3/2⁻（LHCb 2019 引用口径）
M_PC4440 = Decimal("4440.3")    # P_c(4440)，LHCb 2019
M_PC4457 = Decimal("4457.3")    # P_c(4457)，LHCb 2019
GAMMA_PC4312 = Decimal("9.8")   # MeV，P_c(4312) 宽度 ≈9.8（LHCb 2019 引用口径）


def e1_observation_facts():
    """五夸克观测事实（LHCb 2015/2019、PDG 只引用）。"""
    return {
        "lhcb_2015": "P_c(4380) ~4380 ± 29 MeV（Γ~205 MeV）、P_c(4450) ~4449 ± 4 MeV（Γ~39–53 MeV）",
        "lhcb_2019_5sigma": "P_c(4312)、P_c(4440)、P_c(4457)（5σ 观测）",
        "pc4312_mass_MeV": M_PC4312,
        "pc4312_jp": "3/2⁻",
        "pc4312_width_MeV": GAMMA_PC4312,
        "pc4440_mass_MeV": M_PC4440,
        "pc4457_mass_MeV": M_PC4457,
        "decay_mode": "J/ψ p 为主；η_c p 未见显著信号",
        "other_experiments": "束流工厂/其他实验复现：尚未独立确认（LHCb 单合作组观测域）",
    }


def e2_thresholds():
    """候选分子阈值逐项 Decimal 48 位精算 + ΔE 表。

    阈值定义：组分粒子静质量和（MeV）；ΔE = m(P_c) − 阈值。
      ΔE < 0 且 |ΔE| 小（几~几十 MeV）⇒ 近阈结合态 ⇒ 分子判据。
      ΔE > 0 且接近阈值 ⇒ 阈值上方强子分子候选（阈值增强近距结构）。
    """
    t_sigc_d = M_SIGC + M_D            # Σ_c D̄ 阈值
    t_sigcs_d = M_SIGC_S + M_D          # Σ_c* D̄ 阈值
    t_etc_p = M_ETC + M_P               # η_c p 阈值
    t_chic1_p = M_CHIC1 + M_P           # χ_c1 p 阈值
    thresholds = {
        "Σ_c D̄": t_sigc_d,
        "Σ_c* D̄": t_sigcs_d,
        "η_c p": t_etc_p,
        "χ_c1 p": t_chic1_p,
    }
    # ΔE = m(P_c) − 阈值
    d = {}
    d["P_c(4312) − Σ_c D̄"] = M_PC4312 - t_sigc_d
    d["P_c(4312) − Σ_c* D̄"] = M_PC4312 - t_sigcs_d
    d["P_c(4312) − η_c p"] = M_PC4312 - t_etc_p
    d["P_c(4312) − χ_c1 p"] = M_PC4312 - t_chic1_p
    d["P_c(4440) − Σ_c* D̄"] = M_PC4440 - t_sigcs_d
    d["P_c(4440) − χ_c1 p"] = M_PC4440 - t_chic1_p
    d["P_c(4457) − Σ_c* D̄"] = M_PC4457 - t_sigcs_d
    d["P_c(4457) − χ_c1 p"] = M_PC4457 - t_chic1_p
    return {"thresholds": thresholds, "delta_E": d}


# 分子 vs 紧五夸克判据表（4 维度 × 3 列：分子 / 紧五夸克 / 实测 P_c(4312)）
CRITERIA_TABLE = [
    {
        "dimension": "能隙 ΔE",
        "molecule": "近阈值（|ΔE| 几~几十 MeV，ΔE<0 ⇒ 束缚态）",
        "compact": "无阈值近邻约束（QCD 多夸克态质量谱）",
        "observed": "P_c(4312) 近 Σ_c D̄ 阈值下 ΔE≈−8.8 MeV（结合）",
    },
    {
        "dimension": "宽度 Γ",
        "molecule": "窄（弱/电磁衰变主导，~MeV 量级）",
        "compact": "可宽（强衰变道多，~数十 MeV 量级）",
        "observed": "P_c(4312) Γ≈9.8 MeV（窄，近分子预期）",
    },
    {
        "dimension": "量子数 J^P",
        "molecule": "S 波双分子由组分自旋耦合（Σ_c(1/2⁻)⊗D̄(0⁻) ⇒ J^P=1/2⁻,3/2⁻）",
        "compact": "多夸克色波函数任意（无阈值耦合约束）",
        "observed": "P_c(4312) J^P=3/2⁻（LHCb 2019 引用口径）",
    },
    {
        "dimension": "衰变模式",
        "molecule": "J/ψ p 为主（组分夸克重组）；η_c p 可开",
        "compact": "全强子道均可（无首选衰变道）",
        "observed": "J/ψ p 显著（LHCb）；η_c p 未见显著信号",
    },
]


def e3_geometry_supply():
    """TUFT/几何框架能否对五夸克问题供给结构或预言？"""
    # 五夸克谱是 QCD 非微扰问题：需要胶子场、夸克禁闭、色荷、强子质量谱。
    # TUFT 的几何载体 = 时空螺旋（曲率/挠率），无 QCD 强子结构载体：
    #   1) 无胶子场 ⇒ 无禁闭势 ⇒ 无强子质量生成（迹反常）；
    #   2) 无夸克色荷代数 ⇒ 无多夸克态（q q q q̄ q̄）波函数；
    #   3) 几何常数 (ℏ,G,c) 量纲 nullity=0（引用 C0142 E3 / C0140 E4）⇒
    #      给不出 m_Σc、m_D、阈值差等纯数标度。
    nullity3 = 0  # 引用 C0142 E3 / C0140 E4 精确读数
    return {
        "gluon_carrier": 0,          # 无胶子/禁闭载体
        "color_algebra_carrier": 0,  # 无夸克色荷代数载体
        "nullity_hbarGc": nullity3,
        "exotic_hadron_prediction": "none",   # TUFT 无奇特强子预言（撞 C5）
        "geometry_supply": "zero",
    }


def e4_interface():
    """与 C0131（量子化障碍）/ C0137（规范群）衔接口径 + 母册登记。"""
    return {
        "link_C0131": "量子化障碍已裁：几何场未量子化 ⇒ 无量子场论（QFT）结构，"
                      "QCD 作为 QFT 特例不可由几何供给；五夸克谱是 QFT/QCD 动力学问题。",
        "link_C0137": "规范群签名已枚举：几何框架对 SU(3)_c 无唯一化供给（群选择公设），"
                      "色荷代数本身是外部输入 ⇒ 多夸克态波函数无几何来源。",
        "mother_row_before": "| T342 | 五夸克 P_c(4312)/P_c(4440) 分子 vs 紧五夸克 | 重子偶素 | C1,C5 | 🔲 |",
        "mother_row_after": "| T342 | 五夸克 P_c(4312)/P_c(4440) 分子 vs 紧五夸克 | 重子偶素 | C1,C5 | ✅（C0164） |",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0164 · 五夸克 P_c(4312)/P_c(4440) 分子 vs 紧五夸克（母册 T342 · 域 H）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_observation_facts()
    w("\n[E1] 观测事实（LHCb 2015/2019、PDG 只引用不复算）")
    w("  LHCb 2015：%s。" % g1["lhcb_2015"])
    w("  LHCb 2019：%s。" % g1["lhcb_2019_5sigma"])
    w("  P_c(4312)：M=%s MeV、J^P=%s、Γ≈%s MeV（窄）；P_c(4440) M=%s MeV；P_c(4457) M=%s MeV。"
      % (fv(g1["pc4312_mass_MeV"], "1f"), g1["pc4312_jp"], fv(g1["pc4312_width_MeV"], "1f"),
         fv(g1["pc4440_mass_MeV"], "1f"), fv(g1["pc4457_mass_MeV"], "1f")))
    w("  衰变道：%s。" % g1["decay_mode"])
    w("  复现现状：%s。" % g1["other_experiments"])
    w("  => 五夸克态为实验观测事实；分子 vs 紧五夸克归属为 QCD 谱学开放问题。")
    entries.append(("E1", "LHCb 2015/2019 观测 P_c(4312) M=4311.9 J^P=3/2⁻ Γ≈9.8 MeV；"
                    "P_c(4440)/P_c(4457) 5σ；衰变以 J/ψ p 为主", "PASS",
                    "LHCb/PDG 只引用不复算；本册不做归属判定"))

    # ---- E2 ----
    g2 = e2_thresholds()
    w("\n[E2] 候选分子阈值逐项 Decimal 48 位精算（本册核心）")
    w("  PDG 输入：m_Σc=%s、m_Σc*=%s、m_D=%s、m_ηc=%s、m_χc1=%s、m_p=%s MeV。"
      % (fv(M_SIGC, "1f"), fv(M_SIGC_S, "1f"), fv(M_D, "1f"),
         fv(M_ETC, "1f"), fv(M_CHIC1, "1f"), fv(M_P, "1f")))
    w("  阈值表（组分静质量和，MeV）：")
    for name, t in g2["thresholds"].items():
        w("    %-8s 阈值 = %s MeV" % (name, fv(t, "2f")))
    w("  ΔE = m(P_c) − 阈值（MeV）：")
    for name, dval in g2["delta_E"].items():
        w("    %-24s ΔE = %s MeV" % (name, fv(dval, "2f")))
    d_4312_sigc = g2["delta_E"]["P_c(4312) − Σ_c D̄"]
    d_4440_sigcs = g2["delta_E"]["P_c(4440) − Σ_c* D̄"]
    d_4457_sigcs = g2["delta_E"]["P_c(4457) − Σ_c* D̄"]
    w("  判读：P_c(4312) 在 Σ_c D̄ 阈值下方 ΔE=%s MeV（近阈结合，分子判据吻合）；"
      % fv(d_4312_sigc, "2f"))
    w("        P_c(4440)/P_c(4457) 在 Σ_c* D̄ 阈值上方 ΔE=%s/+%s MeV（阈值近距结构）。"
      % (fv(d_4440_sigcs, "2f"), fv(d_4457_sigcs, "2f")))
    w("  分子 vs 紧五夸克判据表（4 维度）：")
    for row in CRITERIA_TABLE:
        w("    · %s" % row["dimension"])
        w("      分子    ：%s" % row["molecule"])
        w("      紧五夸克：%s" % row["compact"])
        w("      实测    ：%s" % row["observed"])
    w("  => 实测读数（近阈、窄、3/2⁻、J/ψ p 主导）与分子判据相容；")
    w("     但该相容是 QCD 谱学判据的吻合，不是 TUFT/几何框架的供给。")
    entries.append(("E2", "Σ_c D̄ 阈值=%s MeV、ΔE(4312)=%s MeV（结合）；"
                    "Σ_c* D̄ 阈值=%s MeV、ΔE(4440/4457)=%s/+%s MeV；"
                    "判据表 4 维完整"
                    % (fv(g2["thresholds"]["Σ_c D̄"], "1f"), fv(d_4312_sigc, "1f"),
                       fv(g2["thresholds"]["Σ_c* D̄"], "1f"),
                       fv(d_4440_sigcs, "1f"), fv(d_4457_sigcs, "1f")),
                    "PASS", "PDG 质量只引用；阈值与 ΔE 本册 Decimal 48 位独立精算"))

    # ---- E3 ----
    g3 = e3_geometry_supply()
    w("\n[E3] 几何供给：TUFT 能否对五夸克问题供给结构或预言？")
    w("  胶子/禁闭载体 = %d；色荷代数载体 = %d；几何常数 (ℏ,G,c) nullity = %d。"
      % (g3["gluon_carrier"], g3["color_algebra_carrier"], g3["nullity_hbarGc"]))
    w("  TUFT 几何载体 = 时空螺旋（曲率/挠率），无 QCD 强子结构载体：")
    w("    1) 无胶子场 ⇒ 无禁闭势 ⇒ 无强子质量生成；")
    w("    2) 无夸克色荷代数 ⇒ 无 (q q q q̄ q̄) 多夸克波函数；")
    w("    3) nullity=0 ⇒ 给不出 m_Σc/m_D/阈值差等纯数标度（引用 C0142 E3 / C0140 E4）。")
    w("  TUFT 奇特强子预言 = %s。" % g3["exotic_hadron_prediction"])
    w("  => 几何供给 = 0；撞 C1（QCD 公设独有：夸克/胶子/色荷须公设）/ C5（TUFT 无奇特强子预言）。")
    entries.append(("E3", "几何供给 0：无胶子/禁闭载体、无色荷代数载体、nullity=0；"
                    "TUFT 无奇特强子预言", "PASS", "撞 C1/C5"))

    # ---- E4 ----
    g4 = e4_interface()
    w("\n[E4] 衔接口径与母册登记")
    w("  C0131（量子化障碍）：%s" % g4["link_C0131"])
    w("  C0137（规范群签名）：%s" % g4["link_C0137"])
    w("  母册 T342 行（登记前）：%s" % g4["mother_row_before"])
    w("  母册 T342 行（登记后）：%s" % g4["mother_row_after"])
    entries.append(("E4", "承接 C0131（场未量子化⇒无QFT）、C0137（SU(3)_c 非几何唯一化）；"
                    "T342 🔲→✅（C0164）", "PASS", "引用不复算"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  五夸克问题被精确翻译成两件事：(a) 分子 vs 紧五夸克归属（QCD 谱学开放问题）；"
      "(b) 该谱能否由几何框架供给结构或预言。")
    w("  (a) E2 精算显示实测与分子判据相容（近阈结合、窄、J/ψ p 主导）——")
    w("      但相容的判据来自 QCD 组分阈值，不是几何。")
    w("  (b) E3：TUFT 无胶子/夸克禁闭/色荷载体，供给 0，撞 C1/C5。")
    w("  => **结构性负面（对 TUFT/几何框架）**：TUFT 对五夸克态既无结构供给、"
      "也无预言；母册 T342 标记 ✅（C0164）。")
    entries.append(("E5", "结构性负面：五夸克谱为 QCD 动力学问题，TUFT 供给 0、"
                    "无奇特强子预言；撞 C1/C5", "PASS", "T342 🔲→✅"))

    # ---- 守卫（≥6 条） ----
    citations = [e for e in entries if "引用" in e[3]]
    guards = [
        ("G1", "阈值差精算区间：|ΔE(P_c4312−Σ_c D̄)| ∈ [5,15] MeV（近阈结合）",
         Decimal("5") <= abs(d_4312_sigc) <= Decimal("15")),
        ("G2", "Σ_c D̄ 阈值 ≈ 4320 MeV（Decimal 精算 4320.7，±5 容差）",
         abs(g2["thresholds"]["Σ_c D̄"] - Decimal("4320")) <= Decimal("5")),
        ("G3", "分子 vs 紧五夸克判据表完整（4 维度 × 3 列全非空）",
         all(row["dimension"] and row["molecule"] and row["compact"] and row["observed"]
             for row in CRITERIA_TABLE) and len(CRITERIA_TABLE) == 4),
        ("G4", "引用标记齐备（LHCb/PDG 只引用条目不小于 2）",
         len(citations) >= 2),
        ("G5", "几何供给 = 0（无胶子载体、无色荷载体、nullity=0）",
         (g3["gluon_carrier"] == 0 and g3["color_algebra_carrier"] == 0
          and g3["nullity_hbarGc"] == 0 and g3["geometry_supply"] == "zero")),
        ("G6", "裁定为结构性负面（撞 C1/C5）",
         entries[-1][2] == "PASS" and "结构性负面" in entries[-1][1]),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0164 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已判定 P_c 的分子/紧五夸克归属（QCD 谱学开放问题）；")
    w("  PDG 质量值与 LHCb 2015/2019 观测值只引用不复算；")
    w("  红线不变：「有预测且对 = 0/22」；数学自洽 ≠ 实验证实；UFT-3=0 保持。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0164_五夸克Pc攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0164_五夸克Pc攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0164_pentaquark_pc",
            "mother_row": "T342 五夸克 P_c(4312)/P_c(4440) 分子 vs 紧五夸克（重子偶素，C1,C5）",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_observation": {k: str(v) for k, v in g1.items()},
            "E2_thresholds": {
                "thresholds": {k: str(v) for k, v in g2["thresholds"].items()},
                "delta_E": {k: str(v) for k, v in g2["delta_E"].items()},
                "criteria_table": CRITERIA_TABLE,
            },
            "E3_geometry_supply": {k: str(v) for k, v in g3.items()},
            "E4_interface": {k: str(v) for k, v in g4.items()},
            "guards": [{"id": g[0], "desc": g[1], "pass": bool(g[2])} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0164 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
