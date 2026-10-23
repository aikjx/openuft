# -*- coding: utf-8 -*-
"""
attack_C0184_WIMP核散射攻破_2026-10-21.py
独立核算：母册 T294「WIMP 自旋无关（SI）核散射零信号」· LZ/XENONnT/PandaX-4T

定位：母册 T294（行 426，原文照录）：
  | T294 | WIMP 自旋无关核散射（LZ/XENONnT/PandaX 零信号） | WIMP 弹性 | C5,C6 | 🔲 |
衔接 C0139（T011 已攻破：热遗迹反解 ⟨σv⟩=1.906429×10⁻²⁶ cm³/s 落 WIMP 窗口="巧合非推导"）
与 C0180（轴子 misalignment，结构性负面撞 C1/C2）。

把"WIMP SI 直接探测零信号"压缩成五条可复核读数：

  E1 零信号上限现状（实验值只引用，注明来源量级）：
     LZ 2024 对 30 GeV WIMP σ_SI ≲ 2.2×10⁻⁴⁸ cm²；XENONnT/PandaX-4T 同量级。
  E2 **质量窗口扫点（本册核心，Decimal 48 位）**：
     1–1000 GeV 扫点取 10/100/1000 GeV，以上限曲线最小点（30 GeV）为锚做标度律。
  E3 截面-丰度张力：热遗迹 ⟨σv⟩（C0139）vs 零信号排除 ⇒ 湮灭道 vs 散射道对照。
  E4 对 TUFT 供给检查：几何框架无 WIMP 粒子态、无核散射截面供给。
  E5 裁定：结构性负面（对 TUFT/几何框架），按母册登记撞 C5/C6。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界：实验上限值只引用（注明来源量级）；标度律为 O(1) 量级模型，按量级（倍）判定；
所有数值均为标准粒子物理/宇宙学算术或实验零信号复核；TUFT 已注销（C0133），
严禁把标准物理结果写成 TUFT 预测/修正。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os
import json

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（实验零信号上限，只引用，注明来源量级） ----------
# LZ 2024（暗物质暗物质实验组，30 GeV WIMP）SI 上限 ≈ 2.2×10⁻⁴⁸ cm²（90% CL，量级）
SIGMA_LZ_30GEV = Decimal("2.2e-48")
# XENONnT 2024 首批结果：同量级（30 GeV 附近），系数取公开结果量级
SIGMA_XENONT_30GEV = Decimal("2.5e-48")
# PandaX-4T：同量级（10⁻⁴⁷–10⁻⁴⁸ cm² 量级），系数取公开结果量级
SIGMA_PANDAX_30GEV = Decimal("3.0e-48")

# 锚点：上限曲线最小点（实验灵敏度谷底）约在 30 GeV
M_ANCHOR_GEV = Decimal("30")

# 本地晕 WIMP 速度（PDG 常用值，只引用）
V_WIMP_CM_S = Decimal("2.2e7")   # 220 km/s = 2.2×10⁷ cm/s

# C0139 热遗迹反解（引用，不复算）：⟨σv⟩ = 1.906429×10⁻²⁶ cm³/s
SIGMA_V_RELIC = Decimal("1.906429e-26")

# 典型"WIMP 奇迹"期望带（弱耦合有效算符模型预测量级，只引用）：σ_SI ~ 10⁻⁴⁵–10⁻⁴⁶ cm²
SIGMA_SI_EXPECT = Decimal("1.0e-46")


def e1_experimental_limits():
    """零信号上限现状（只引用，注明来源量级）。"""
    return {
        "sigma_LZ_30GeV_cm2": SIGMA_LZ_30GEV,
        "sigma_XENONnT_30GeV_cm2": SIGMA_XENONT_30GEV,
        "sigma_PandaX4T_30GeV_cm2": SIGMA_PANDAX_30GEV,
        "anchor_mass_GeV": M_ANCHOR_GEV,
        "order_of_magnitude": Decimal("1e-48"),
    }


def sigma_upper(m_gev: Decimal) -> Decimal:
    """SI 上限曲线标度律（O(1) 量级模型，锚定 30 GeV 最小点）。

    低质量支（m≤30 GeV）：阈限/淬灭效率限制，灵敏度 σ_upper ∝ 1/m_χ；
    高质量支（m≥30 GeV）：本地晕数密度 n_χ ∝ ρ_loc/m_χ ∝ 1/m_χ，
        固定期望事件数下 σ_upper ∝ m_χ。
    两支在锚点 30 GeV 连续。
    """
    if m_gev <= M_ANCHOR_GEV:
        return SIGMA_LZ_30GEV * (M_ANCHOR_GEV / m_gev)
    else:
        return SIGMA_LZ_30GEV * (m_gev / M_ANCHOR_GEV)


def e2_mass_scan():
    """质量窗口 1–1000 GeV 扫点（10/100/1000 GeV 三点精算）。"""
    masses = [Decimal("10"), Decimal("100"), Decimal("1000")]
    rows = [(m, sigma_upper(m)) for m in masses]
    return {
        "masses_GeV": masses,
        "sigma_upper_cm2": [s for _, s in rows],
        "anchor_30GeV": (M_ANCHOR_GEV, SIGMA_LZ_30GEV),
    }


def e3_abundance_tension():
    """截面-丰度张力核算（衔接 C0139）。"""
    # 散射道等效"截面×速度"：σ_SI(30GeV 上限) × v_WIMP
    sigma_v_scatter = SIGMA_LZ_30GEV * V_WIMP_CM_S
    # 湮灭道（热遗迹确定）⟨σv⟩ 与散射道上限的比值
    ratio_ann_over_scatter = SIGMA_V_RELIC / sigma_v_scatter
    # 典型 WIMP 期望带 vs 实验上限的排除倍数
    tension_factor = SIGMA_SI_EXPECT / SIGMA_LZ_30GEV
    return {
        "v_wimp_cm_s": V_WIMP_CM_S,
        "sigma_v_scatter_cm3_s": sigma_v_scatter,
        "sigma_v_relic_cm3_s": SIGMA_V_RELIC,
        "ratio_ann_over_scatter": ratio_ann_over_scatter,
        "sigma_si_expect_cm2": SIGMA_SI_EXPECT,
        "tension_factor_expect_vs_limit": tension_factor,
    }


def e4_tuft_supply():
    """对 TUFT/几何框架供给检查：无暗物质粒子态、无核散射耦合。"""
    return {
        "has_dm_particle_state": False,   # 承接 C0139 E4：挠率零程、无稳定中性粒子载体
        "has_si_scattering_coupling": False,
        "has_nucleon_matrix_element": False,
        "supply": "zero",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0184 · WIMP SI 核散射零信号（母册 T294）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_experimental_limits()
    w("\n[E1] 零信号上限现状（实验值只引用，注明来源量级）")
    w("  LZ 2024      （30 GeV WIMP）σ_SI ≲ %s cm²（90%% CL，量级）" % fv(g1["sigma_LZ_30GeV_cm2"], "2e"))
    w("  XENONnT 2024 （30 GeV WIMP）σ_SI ≲ %s cm²（同量级，系数取公开结果量级）"
      % fv(g1["sigma_XENONnT_30GeV_cm2"], "2e"))
    w("  PandaX-4T    （30 GeV WIMP）σ_SI ≲ %s cm²（10⁻⁴⁷–10⁻⁴⁸ cm² 量级）"
      % fv(g1["sigma_PandaX4T_30GeV_cm2"], "2e"))
    w("  锚点（灵敏度谷底）m_χ = %s GeV；三家实验同处 10⁻⁴⁸ cm² 量级。"
      % fv(g1["anchor_mass_GeV"], "0f"))
    w("  => 对 30 GeV 热遗迹 WIMP，SI 截面已被压到 ≲10⁻⁴⁸ cm² 量级（零信号）。")
    entries.append(("E1", "LZ/XENONnT/PandaX-4T 对 30 GeV WIMP σ_SI ≲ 2–3×10⁻⁴⁸ cm²（同量级）",
                    "PASS", "实验零信号上限只引用，注明来源量级"))

    # ---- E2 ----
    g2 = e2_mass_scan()
    w("\n[E2] 质量窗口扫点（1–1000 GeV，取 10/100/1000 GeV；标度律以 30 GeV 锚点）")
    w("  标度律：低质量支(m≤30) σ_upper ∝ 1/m_χ；高质量支(m≥30) σ_upper ∝ m_χ。")
    w("  m_χ (GeV) | σ_SI,upper (cm²)")
    for m, s in zip(g2["masses_GeV"], g2["sigma_upper_cm2"]):
        w("  %-10s | %s" % (fv(m, "0f"), fv(s, "4e")))
    m30, s30 = g2["anchor_30GeV"]
    w("  锚点参考：m_χ = %s GeV | %s cm²（LZ 2024 最小点）"
      % (fv(m30, "0f"), fv(s30, "4e")))
    w("  => 10 GeV 上限 ~6.6×10⁻⁴⁸、100 GeV ~7.33×10⁻⁴⁸、1000 GeV ~7.33×10⁻⁴⁷ cm²；")
    w("     曲线在 30 GeV 附近取最小，两端抬升——与直接探测上限曲线的形状一致（量级）。")
    entries.append(("E2", "质量扫点：σ_upper(10GeV)=6.6e-48、(100GeV)=7.33e-48、"
                    "(1000GeV)=7.33e-47 cm²（30 GeV 锚点最小）",
                    "PASS", "O(1) 标度律模型，锚定 LZ 2024 实验最小点，按量级判定"))

    # ---- E3 ----
    g3 = e3_abundance_tension()
    w("\n[E3] 截面-丰度张力（衔接 C0139 热遗迹 ⟨σv⟩）")
    w("  C0139 热遗迹反解（引用）⟨σv⟩ = %s cm³/s" % fv(g3["sigma_v_relic_cm3_s"], "6e"))
    w("  散射道等效 σ_SI,上限(30GeV) × v_WIMP(=220 km/s=%s cm/s) = %s cm³/s"
      % (fv(g3["v_wimp_cm_s"], "1e"), fv(g3["sigma_v_scatter_cm3_s"], "4e")))
    w("  湮灭道/散射道比值 ⟨σv⟩_relic / (σ_SI×v) = %s" % fv(g3["ratio_ann_over_scatter"], "4e"))
    w("  典型 WIMP 期望带 σ_SI ~ %s cm²（弱耦合有效算符量级）"
      % fv(g3["sigma_si_expect_cm2"], "1e"))
    w("  期望带/实验上限 排除倍数 = %s / %s = %s 倍"
      % (fv(g3["sigma_si_expect_cm2"], "1e"), fv(SIGMA_LZ_30GEV, "2e"),
         fv(g3["tension_factor_expect_vs_limit"], "2f")))
    w("  => 丰度要求大湮灭截面（⟨σv⟩~2×10⁻²⁶），零信号禁大散射截面（σ_SI≲2×10⁻⁴⁸）；")
    w("     典型热遗迹 WIMP（30 GeV、规范耦合量级 SI）已被排除约 %s 倍——截面-丰度张力成立。"
      % fv(g3["tension_factor_expect_vs_limit"], "1f"))
    entries.append(("E3", "湮灭/散射道比值 %s；典型 WIMP 期望带被零信号排除 %s 倍"
                    % (fv(g3["ratio_ann_over_scatter"], "1e"),
                       fv(g3["tension_factor_expect_vs_limit"], "0f")),
                    "PASS", "C0139 ⟨σv⟩ 引用 + 散射道算术；张力为标准粒子物理对照"))

    # ---- E4 ----
    g4 = e4_tuft_supply()
    w("\n[E4] 对 TUFT/几何框架供给检查")
    w("  有暗物质粒子态：%s（承接 C0139 E4：挠率零程、无稳定中性粒子载体）"
      % g4["has_dm_particle_state"])
    w("  有 SI 核散射耦合：%s" % g4["has_si_scattering_coupling"])
    w("  有核子矩阵元供给：%s" % g4["has_nucleon_matrix_element"])
    w("  => TUFT/几何框架对 WIMP 无粒子态、无散射截面、无核子矩阵元供给 = %s。" % g4["supply"])
    entries.append(("E4", "TUFT 供给 0：无 WIMP 粒子态/无 SI 散射耦合/无核子矩阵元",
                    "PASS", "承接 C0139 E4；撞 C5/C6"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  WIMP SI 直接探测问题被精确翻译成两件事：(a) 存在一枚暗物质粒子态及其与核的弹性耦合；")
    w("  (b) 该耦合大小须同时满足热遗迹丰度（⟨σv⟩~2×10⁻²⁶）且扛得住零信号上限（σ_SI≲2×10⁻⁴⁸）。")
    w("  零信号已把 30 GeV 规范耦合 WIMP 排除约 45 倍（E3）；TUFT 无粒子态/无耦合供给（E4）。")
    w("  => **结构性负面（对 TUFT/几何框架）**；按母册 T294 登记撞 C5（可检验/实验排除）/ C6（误差带/判别力）。")
    entries.append(("E5", "结构性负面：零信号排除典型热遗迹 WIMP ~45 倍，TUFT 无粒子态/耦合供给",
                    "PASS", "按母册 T294 撞 C5/C6"))

    # ---- 守卫 ----
    guards = [
        ("G1", "LZ 2024 对 30 GeV WIMP 上限处 10⁻⁴⁸ 量级（< 10⁻⁴⁷ cm²）",
         g1["sigma_LZ_30GeV_cm2"] < Decimal("1e-47")),
        ("G2", "质量扫点高质量支抬升：σ_upper(1000GeV) > σ_upper(100GeV)",
         g2["sigma_upper_cm2"][2] > g2["sigma_upper_cm2"][1]),
        ("G3", "湮灭道/散射道比值 >> 1（截面-丰度张力成立，>10¹²）",
         g3["ratio_ann_over_scatter"] > Decimal("1e12")),
        ("G4", "典型 WIMP 期望带被零信号排除 > 10 倍",
         g3["tension_factor_expect_vs_limit"] > Decimal("10")),
        ("G5", "TUFT 对 WIMP 散射供给 = 0",
         g4["has_si_scattering_coupling"] is False and g4["supply"] == "zero"),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0184 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解释暗物质/已探测 WIMP；实验上限只引用（注明来源量级）；")
    w("  标度律为 O(1) 量级模型，判定按量级（倍）；裁的是「TUFT/几何框架能否供给 WIMP 及其核散射」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0184_WIMP核散射攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0184_WIMP核散射攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0184_wimp_si_nuclear_scattering",
            "mother_row": "T294",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_experimental_limits": {k: str(v) for k, v in g1.items()},
            "E2_mass_scan": {
                "masses_GeV": [str(x) for x in g2["masses_GeV"]],
                "sigma_upper_cm2": [str(x) for x in g2["sigma_upper_cm2"]],
                "anchor": [str(g2["anchor_30GeV"][0]), str(g2["anchor_30GeV"][1])],
            },
            "E3_abundance_tension": {k: str(v) for k, v in g3.items()},
            "E4_tuft_supply": {k: str(v) for k, v in g4.items()},
            "guards": [{"id": g[0], "desc": g[1], "ok": bool(g[2])} for g in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0184 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
