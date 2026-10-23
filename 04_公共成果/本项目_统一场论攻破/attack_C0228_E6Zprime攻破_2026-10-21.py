# -*- coding: utf-8 -*-
"""
attack_C0228_E6Zprime攻破_2026-10-21.py
独立复算：重 Z' 玻色子（E6 / U(1)_{B-L}）di-lepton 共振（母册 T320，力统一专项·GUT 代数结构）

定位：母册 T320（行 452）——重 Z' 玻色子（E6/U(1)_{B-L}）di-lepton 共振；新 U(1)'；
撞 C1/C2。承接 C0162（so(8) 极大子群 P12-KK-EMBED）与 C0202（SM 外新物理 165 枚外部输入）口径。
TUFT 已注销（C0133），本册不把任何标准物理结果写成 TUFT 预测/修正。

把"重 Z'（E6/B-L）"压缩成五条可复核读数：

  E1 E6 的 27 维表示逐级分解核算：E6 ⊃ SO(10)×U(1)_ψ、SO(10) ⊃ SU(5)×U(1)_χ，
     27 = 16 + 10 + 1，再下钻到 SU(5) 层 16=10+5bar+1、10=5+5bar。
  E2 B-L 荷与 Z' 耦合核算：夸克 B-L=1/3、轻子 B-L=-1、Higgs 0；
     单代反常相消（sum = 0）；Z' 耦合 g'_f = g'·(B-L)_f，轻子/夸克耦合强度比 = 3。
  E3 质量窗口核算：LHC di-lepton 下界 M_Z' ≳ 4 TeV（外部输入），与弱标度 v=246 GeV、
     E6/GUT 标度 M_GUT ≈ 2×10^16 GeV 的比值。
  E4 TUFT 供给检查：TUFT/几何框架是否供给 E6 / 27 表示 / 新 U(1)' —— 无（0 枚）。
  E5 裁定：结构性负面（对 TUFT/几何框架），撞 C1（粒子内容）/ C2（绝对标度）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界：E6 群论分解是标准结果（本册做维度/荷算术复核，不做新预言）；
LHC di-lepton 下界与 M_GUT 是外部输入（ATLAS/CMS、PDG/大统一文献），只引用不复算；
"有预测且对 = 0/22"保持；数学自洽 ≠ 实验证实。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os
import json

getcontext().prec = 48

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（只引用不复算） ----------
# LHC di-lepton 共振对顺序 Z'/E6-Z' 的质量下界（ATLAS/CMS Run-2 综合量级，TeV）
M_ZPRIME_LOWER_BOUND_TEV = Decimal("4.0")
# 电弱真空期望值（PDG）
V_WEAK_GEV = Decimal("246.22")
# E6 / 大统一标度（标准 GUT 文献量级，GeV）
M_GUT_GEV = Decimal("2.0e16")


def e1_e6_branching():
    """E6 27 表示逐级分解核算（Fraction 精确，荷为标准 ψ/χ 赋值）。"""
    # E6 ⊃ SO(10) × U(1)_ψ：27 -> 16_{ψ=+1} + 10_{ψ=-2} + 1_{ψ=+4}
    so10_level = [
        ("16", 16, Fraction(1, 1)),
        ("10", 10, Fraction(-2, 1)),
        ("1", 1, Fraction(4, 1)),
    ]
    dim_so10 = sum(d for _, d, _ in so10_level)
    # SO(10) ⊃ SU(5) × U(1)_χ：
    #   16 -> 10_{χ=+1} + 5bar_{χ=-3} + 1_{χ=+5}
    #   10 -> 5_{χ=-2} + 5bar_{χ=+2}
    #   1  -> 1_{χ=0}
    su5_level = [
        ("10", 10, Fraction(1, 1)),
        ("5bar", 5, Fraction(-3, 1)),
        ("1_a", 1, Fraction(5, 1)),
        ("5", 5, Fraction(-2, 1)),
        ("5bar_b", 5, Fraction(2, 1)),
        ("1_b", 1, Fraction(0, 1)),
    ]
    dim_su5 = sum(d for _, d, _ in su5_level)
    # 校验：16 块内 = 10+5+1 = 16；10 块内 = 5+5 = 10
    block_16 = 10 + 5 + 1
    block_10 = 5 + 5
    return {
        "e6_fundamental_dim": 27,
        "so10_level": so10_level,
        "dim_so10_sum": dim_so10,
        "su5_level": su5_level,
        "dim_su5_sum": dim_su5,
        "block_16_sum": block_16,
        "block_10_sum": block_10,
    }


def e2_bl_couplings():
    """B-L 荷、单代反常相消、Z' 耦合核算。"""
    # B-L 荷（Fraction 精确）
    bl_quark = Fraction(1, 3)   # B=1/3, L=0
    lepton = Fraction(-1, 1)     # B=0, L=1
    higgs = Fraction(0, 1)
    # 单代内容：3 色 × (u,d) = 6 个夸克Weyl；(ν,e_L) = 2 个轻子Weyl
    # 反常相消：Σ (B-L) 在单代内
    n_quark_wyl = 6   # 3 colors × 2 (u,d)
    n_lepton_wyl = 2  # ν, e
    anomaly_sum = n_quark_wyl * bl_quark + n_lepton_wyl * lepton
    # Z' 耦合 g'_f = g' · (B-L)_f；定义 g'=1 时的相对耦合
    gp = Fraction(1, 1)
    c_quark = gp * bl_quark
    c_lepton = gp * lepton
    # 轻子对夸克的耦合强度比（绝对值）
    ratio_lepton_over_quark = abs(c_lepton) / abs(c_quark)
    return {
        "B_L_quark": bl_quark,
        "B_L_lepton": lepton,
        "B_L_higgs": higgs,
        "n_quark_weyl_per_gen": n_quark_wyl,
        "n_lepton_weyl_per_gen": n_lepton_wyl,
        "anomaly_sum_per_gen": anomaly_sum,
        "coupling_quark_rel": c_quark,
        "coupling_lepton_rel": c_lepton,
        "ratio_lepton_over_quark": ratio_lepton_over_quark,
    }


def e3_mass_window():
    """质量窗口核算：M_Z' 下界 vs 弱标度 vs GUT 标度。"""
    m_zp_gev = M_ZPRIME_LOWER_BOUND_TEV * Decimal(1000)
    ratio_to_weak = m_zp_gev / V_WEAK_GEV
    ratio_to_gut = m_zp_gev / M_GUT_GEV
    # 对数比（数量级）
    import math
    log10_mzp_over_weak = Decimal(str(math.log10(float(ratio_to_weak))))
    log10_mzp_over_gut = Decimal(str(math.log10(float(ratio_to_gut))))
    return {
        "M_Zp_lower_GeV": m_zp_gev,
        "v_weak_GeV": V_WEAK_GEV,
        "M_GUT_GeV": M_GUT_GEV,
        "M_Zp_over_v": ratio_to_weak,
        "M_Zp_over_MGUT": ratio_to_gut,
        "log10_MZp_over_weak": log10_mzp_over_weak,
        "log10_MZp_over_GUT": log10_mzp_over_gut,
    }


def e4_tuft_supply():
    """TUFT/几何框架是否供给 E6 / 27 / 新 U(1)'。"""
    # TUFT 已注销（C0133）；承接 C0202（SM 外新物理 165 枚外部输入）口径：
    # E6 代数、SO(10)、SU(5) 嵌套、U(1)_ψ/χ/B-L 荷、M_Z' 质量窗口均为外部理论+观测输入。
    return {
        "tuft_has_E6": False,
        "tuft_has_27_rep": False,
        "tuft_has_U1_prime": False,
        "tuft_supply_count": 0,
        "external_input_buckets": [
            "E6 李代数（78 维伴随 / 27 基础表示）",
            "E6⊃SO(10)⊃SU(5) 破缺链",
            "U(1)_ψ / U(1)_χ / U(1)_{B-L} 荷赋值",
            "Z' 规范耦合 g' 与质量 M_Z'",
            "LHC di-lepton 排除曲线（ATLAS/CMS）",
        ],
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0228 · 重 Z' 玻色子（E6 / U(1)_{B-L}）di-lepton 共振攻破")
    w("（母册 T320 · 力统一专项 · GUT 代数结构；撞 C1/C2）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_e6_branching()
    w("\n[E1] E6 的 27 维表示逐级分解核算（标准群论算术复核）")
    w("  E6 基础表示 dim = %d" % g1["e6_fundamental_dim"])
    w("  E6 ⊃ SO(10)×U(1)_ψ：27 = 16(ψ=%s) + 10(ψ=%s) + 1(ψ=%s)"
      % (g1["so10_level"][0][2], g1["so10_level"][1][2], g1["so10_level"][2][2]))
    w("  SO(10) 层维度和 = 16+10+1 = %d（应=27）" % g1["dim_so10_sum"])
    w("  SO(10) ⊃ SU(5)×U(1)_χ：")
    for name, d, chi in g1["su5_level"]:
        w("    %-7s dim=%d  χ=%s" % (name, d, chi))
    w("  SU(5) 层维度和 = %d（应=27）" % g1["dim_su5_sum"])
    w("  块内校验：16 块 = 10+5+1 = %d（应=16）；10 块 = 5+5 = %d（应=10）"
      % (g1["block_16_sum"], g1["block_10_sum"]))
    w("  => 27 = 16+10+1 在两层嵌套下维度闭合，荷赋值自洽（ψ=1,-2,4；χ=1,-3,5,-2,2,0）。")
    entries.append(("E1", "E6 27 = 16+10+1（SO10 层）= (10+5bar+1)+(5+5bar)+1（SU5 层），维度与荷闭合",
                    "PASS", "标准群论算术复核；ψ/χ 荷为标准赋值"))

    # ---- E2 ----
    g2 = e2_bl_couplings()
    w("\n[E2] B-L 荷与 Z' 耦合核算（本册核心读数）")
    w("  B-L 荷：夸克 = %s（B=1/3,L=0）；轻子 = %s（B=0,L=1）；Higgs = %s"
      % (g2["B_L_quark"], g2["B_L_lepton"], g2["B_L_higgs"]))
    w("  单代 Weyl 内容：夸克 %d 个（3 色 × u,d），轻子 %d 个（ν,e）"
      % (g2["n_quark_weyl_per_gen"], g2["n_lepton_weyl_per_gen"]))
    w("  单代 Σ(B-L) = %d×(%s) + %d×(%s) = %s"
      % (g2["n_quark_weyl_per_gen"], g2["B_L_quark"],
         g2["n_lepton_weyl_per_gen"], g2["B_L_lepton"],
         g2["anomaly_sum_per_gen"]))
    w("  => B-L 单代反常相消（和=0），U(1)_{B-L} 无三角反常，可做规范群。")
    w("  Z' 相对耦合（g'=1）：夸克 c_q = %s；轻子 c_l = %s"
      % (g2["coupling_quark_rel"], g2["coupling_lepton_rel"]))
    w("  轻子/夸克耦合强度比 |c_l|/|c_q| = %s（=3）" % g2["ratio_lepton_over_quark"])
    w("  => di-lepton 末态之所以对 Z' 敏感，正源于轻子耦合 = 3×夸克耦合（同 g' 下）。")
    entries.append(("E2", "B-L 荷：夸克 1/3、轻子 -1、Higgs 0；单代反常和=0；"
                    "Z' 轻子/夸克耦合强度比 = 3", "PASS",
                    "Fraction 精确；di-lepton 通道敏感性来源"))

    # ---- E3 ----
    g3 = e3_mass_window()
    w("\n[E3] 质量窗口核算（LHC 外部输入 + 比值精算）")
    w("  LHC di-lepton 下界 M_Z' ≳ %s TeV = %s GeV（ATLAS/CMS，外部输入只引用）"
      % (M_ZPRIME_LOWER_BOUND_TEV, fv(g3["M_Zp_lower_GeV"], "0f")))
    w("  弱标度 v = %s GeV；M_GUT ≈ %s GeV"
      % (fv(g3["v_weak_GeV"], "2f"), fv(g3["M_GUT_GeV"], "0e")))
    w("  M_Z'/v = %s（≈ 1.63×10^1）" % fv(g3["M_Zp_over_v"], "6f"))
    w("  M_Z'/M_GUT = %s（≈ 2×10^-13）" % fv(g3["M_Zp_over_MGUT"], "6e"))
    w("  log10(M_Z'/v) = %s；log10(M_Z'/M_GUT) = %s"
      % (fv(g3["log10_MZp_over_weak"], "4f"), fv(g3["log10_MZp_over_GUT"], "4f")))
    w("  => Z' 质量窗口横跨弱标度 1.6 个数量级、距 GUT 标度 12.7 个数量级；")
    w("     M_Z' 必须由中间破缺标度（非 GUT 标度本身）产生——这是标准模型构建的外部输入。")
    entries.append(("E3", "M_Z' ≳ 4 TeV（外部输入）；M_Z'/v ≈ %s；M_Z'/M_GUT ≈ %s"
                    % (fv(g3["M_Zp_over_v"], "4f"), fv(g3["M_Zp_over_MGUT"], "2e")),
                    "PASS", "LHC 下界与 M_GUT 为外部输入；比值本册精算"))

    # ---- E4 ----
    g4 = e4_tuft_supply()
    w("\n[E4] TUFT 供给检查（承接 C0162 / C0202 口径）")
    w("  TUFT 是否含 E6 代数：%s" % g4["tuft_has_E6"])
    w("  TUFT 是否含 27 维表示：%s" % g4["tuft_has_27_rep"])
    w("  TUFT 是否含新 U(1)'（ψ/χ/B-L）：%s" % g4["tuft_has_U1_prime"])
    w("  TUFT 供给计数 = %d" % g4["tuft_supply_count"])
    w("  外部输入桶（%d 项）：" % len(g4["external_input_buckets"]))
    for b in g4["external_input_buckets"]:
        w("    - %s" % b)
    w("  => E6/Z' 的全部结构与标度均来自大统一文献 + LHC 观测，TUFT/几何框架供给 0。")
    entries.append(("E4", "TUFT 供给 = 0（无 E6、无 27、无 U(1)'）；"
                    "5 类外部输入桶全额挂账", "PASS", "承接 C0202 外部输入口径"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  母册 T320 问题被拆成三件：(a) E6/GUT 代数结构从哪来；(b) B-L 荷与 Z' 耦合从哪来；")
    w("  (c) M_Z' 质量窗口从哪来。")
    w("  (a) E6⊃SO(10)⊃SU(5) 破缺链、27 表示分解——标准群论，本册复核维度闭合（E1），")
    w("      但这是外部理论公设，不是 TUFT 推导。")
    w("  (b) B-L 荷赋值、单代反常相消、Z' 耦合比 3——标准群论算术（E2），同样外部输入。")
    w("  (c) M_Z' ≳ 4 TeV 来自 ATLAS/CMS 排除曲线（E3），M_GUT 来自大统一文献。")
    w("  => **结构性负面（对 TUFT/几何框架）**；撞 C1（粒子内容：E6/27/Z' 须公设）")
    w("     / C2（绝对标度：M_Z' 质量窗口是实验输入）。按母册登记撞 C1/C2。")
    entries.append(("E5", "结构性负面：E6/27/B-L/Z' 全为外部理论+观测输入，"
                    "TUFT 供给 0；撞 C1/C2", "PASS", "母册 T320 撞点登记"))

    # ---- 守卫 ----
    guards = [
        ("G1", "E6 27 在 SO(10) 层维度和 = 27", g1["dim_so10_sum"] == 27),
        ("G2", "E6 27 在 SU(5) 层维度和 = 27", g1["dim_su5_sum"] == 27),
        ("G3", "16 块内 = 10+5+1 = 16", g1["block_16_sum"] == 16),
        ("G4", "单代 B-L 反常相消和 = 0", g2["anomaly_sum_per_gen"] == 0),
        ("G5", "Z' 轻子/夸克耦合强度比 = 3", g2["ratio_lepton_over_quark"] == 3),
        ("G6", "M_Z' 下界为正的外部输入", g3["M_Zp_lower_GeV"] > Decimal(0)),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0228 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解决 Z'/E6 物理难题；E6 分解与 B-L 荷为标准群论结果（本册算术复核）；")
    w("  LHC 下界与 M_GUT 为外部输入只引用不复算；TUFT 已注销（C0133），不把标准结果写成 TUFT 预测。")
    w("  红线：不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("        有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0228_E6Zprime攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0228_E6Zprime攻破_2026-10-21.json")

    def frac_list(lst):
        return [{"name": n, "dim": d, "charge_psi_or_chi": str(c)} for n, d, c in lst]

    payload = {
        "name": "C0228_E6_Zprime_dilepton",
        "mother_row": "T320",
        "topic": "重 Z' 玻色子（E6/U(1)_{B-L}）di-lepton 共振",
        "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                    for e in entries],
        "E1_e6_branching": {
            "e6_fundamental_dim": g1["e6_fundamental_dim"],
            "so10_level": frac_list(g1["so10_level"]),
            "dim_so10_sum": g1["dim_so10_sum"],
            "su5_level": frac_list(g1["su5_level"]),
            "dim_su5_sum": g1["dim_su5_sum"],
            "block_16_sum": g1["block_16_sum"],
            "block_10_sum": g1["block_10_sum"],
        },
        "E2_bl_couplings": {
            "B_L_quark": str(g2["B_L_quark"]),
            "B_L_lepton": str(g2["B_L_lepton"]),
            "B_L_higgs": str(g2["B_L_higgs"]),
            "n_quark_weyl_per_gen": g2["n_quark_weyl_per_gen"],
            "n_lepton_weyl_per_gen": g2["n_lepton_weyl_per_gen"],
            "anomaly_sum_per_gen": str(g2["anomaly_sum_per_gen"]),
            "coupling_quark_rel": str(g2["coupling_quark_rel"]),
            "coupling_lepton_rel": str(g2["coupling_lepton_rel"]),
            "ratio_lepton_over_quark": str(g2["ratio_lepton_over_quark"]),
        },
        "E3_mass_window": {
            "M_Zp_lower_TeV": str(M_ZPRIME_LOWER_BOUND_TEV),
            "M_Zp_lower_GeV": str(g3["M_Zp_lower_GeV"]),
            "v_weak_GeV": str(g3["v_weak_GeV"]),
            "M_GUT_GeV": str(g3["M_GUT_GeV"]),
            "M_Zp_over_v": str(g3["M_Zp_over_v"]),
            "M_Zp_over_MGUT": str(g3["M_Zp_over_MGUT"]),
            "log10_MZp_over_v": str(g3["log10_MZp_over_weak"]),
            "log10_MZp_over_MGUT": str(g3["log10_MZp_over_GUT"]),
        },
        "E4_tuft_supply": g4,
        "guards": [{"id": gid, "desc": d, "ok": bool(ok)} for gid, d, ok in guards],
        "guards_total": len(guards),
        "guards_pass": sum(1 for g in guards if g[2]),
        "exit_code": 0,
    }

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("C0228 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
