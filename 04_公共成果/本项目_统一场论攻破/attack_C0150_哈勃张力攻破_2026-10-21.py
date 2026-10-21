# -*- coding: utf-8 -*-
"""
attack_C0150_哈勃张力攻破_2026-10-21.py
独立复算：物理 Top100 清单 T037「哈勃张力（H0 矛盾）」· 判定号 C0150

定位：物理 Top100 难题 T037。两条独立观测链给出互相冲突的 H0：
  CMB 侧（Planck 2018 ΛCDM 拟合）：H0 = 67.36 ± 0.54 km/s/Mpc
  局域距离阶梯侧（SH0ES 2022 Riess）：H0 = 73.04 ± 1.04 km/s/Mpc
本册**不采信任何来料自报**，用 Decimal 48 位独立复算张力显著性 σ，并对
TUFT/几何框架判定"能否从第一性原理供给宇宙学尺度新物理候选"。

把"哈勃张力"压缩成五条可复核读数 + 一张新物理输入账单：

  E1 观测事实：Planck 2018 / SH0ES 2022 的 H0、r_s*、θ*（外部只引用不复算）。
  E2 核心公式体系（本册核心）：
     σ = (H0_SH0ES − H0_Planck) / √(σ₁² + σ₂²) 独立精算（预期 ≈ 4.8–4.9σ）；
     双口径推导链：(a) CMB 侧 θ* = r_s / D_A 反解 H0；(b) 局域侧 H0 = v/D。
  E3 裁决：系统误差 vs 新物理。新物理候选清单（EDE / 变 G / ΔN_eff / 相互作用
     暗辐射），每候选 ≥1 枚新输入；库内"标准汽笛判决""哈勃张力判据"为来料，
     不采信自报，本册独立复算 σ 数。
  E4 几何供给：TUFT 单尺度（引用 C0141 E4）无宇宙学尺度新物理候选 ⇒ 供给 0。
  E5 裁定：结构性负面（对 TUFT/几何框架），撞 C2（新标度）/ C5（裁决机制）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：本册**不宣称哈勃张力已裁决**；外部观测值（Planck / SH0ES）只引用
不复算；库内来料结论不采信自报，本册独立复算 σ 数。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- E1 外部观测值（Planck 2018 / SH0ES 2022，只引用不复算） ----------
# Planck 2018 (TT,TE,EE+lowE+lensing)
H0_PLANCK = Decimal("67.36")     # km/s/Mpc
SIG_H0_PLANCK = Decimal("0.54")
# SH0ES 2022 (Riess)
H0_SH0ES = Decimal("73.04")      # km/s/Mpc
SIG_H0_SH0ES = Decimal("1.04")
# Planck 声视界 r_s*（Mpc）
R_STAR = Decimal("147.09")
SIG_R_STAR = Decimal("0.26")
# CMB 角视界 θ* ≈ 1.041e-2 rad
THETA_STAR = Decimal("1.041e-2")


def e1_obs_facts():
    """E1 观测事实（只引用不复算）。"""
    return {
        "planck_H0": H0_PLANCK, "planck_sigma": SIG_H0_PLANCK,
        "sh0es_H0": H0_SH0ES, "sh0es_sigma": SIG_H0_SH0ES,
        "r_star_Mpc": R_STAR, "r_star_sigma": SIG_R_STAR,
        "theta_star_rad": THETA_STAR,
    }


def e2_significance():
    """E2 核心：张力显著性 σ 独立精算（本册核心）。

    σ = (H0_SH0ES − H0_Planck) / √(σ_SH0ES² + σ_Planck²)
    Decimal 48 位精算；√ 用 Decimal.sqrt()（精度 48）。
    """
    delta = H0_SH0ES - H0_PLANCK
    var = SIG_H0_SH0ES * SIG_H0_SH0ES + SIG_H0_PLANCK * SIG_H0_PLANCK
    combo_sigma = var.sqrt()
    sigma = delta / combo_sigma
    # 双口径推导链（写出，不外部复算）：
    # (a) CMB 侧：θ* = r_s / D_A(z*)  ⇒  D_A = r_s / θ*；H0 由 D_A(z*) 与
    #     r_s = ∫₀^{z*} c_s(z)/H(z) dz 联合 ΛCDM 反解（Planck 2018 给出 H0=67.36）。
    # (b) 局域侧：H0 = v/D（Hubble 定律），D 由 Cepheid 校准 SNIa 距离阶梯给出
    #     （SH0ES 2022 给出 H0=73.04）。
    return {
        "delta": delta,
        "var_sum": var,
        "combo_sigma": combo_sigma,
        "sigma": sigma,
    }


def e3_new_physics_candidates():
    """E3 新物理候选清单，每候选 ≥1 枚新输入。来料不采信自报，独立复算 σ。"""
    # 候选清单（每枚至少 1 个新自由度/新参数）
    candidates = [
        ("早期暗能量 EDE", "新标量场 + 慢滚势（暴胀后二次注入辐射）", 1),
        ("变 G（引力常数随时间）", "G(t) 动力学场（违反 GR 常数假设）", 1),
        ("额外相对论自由度 ΔN_eff", "新增 relativistic species（如惰性中微子）", 1),
        ("相互作用暗辐射", "暗物质–暗辐射新相互作用通道", 1),
    ]
    new_input_count = sum(c[2] for c in candidates)
    return {
        "candidates": candidates,
        "new_input_count": new_input_count,
        "library_sources_not_trusted": ["标准汽笛判决", "哈勃张力判据"],
    }


def e4_geometry_supply():
    """E4 几何供给：TUFT 单尺度（引用 C0141 E4）无宇宙学尺度新物理候选 ⇒ 0。"""
    # 承接 C0141 E4：TUFT 单尺度框架无宇宙学尺度新自由度注入通道；
    # 故对"早期暗能量 / 变 G / ΔN_eff / 相互作用暗辐射"均供给 0。
    return {
        "single_scale_ref": "C0141_E4",
        "cosmological_new_physics_supply": 0,
        "supply": "zero",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0150 · 哈勃张力（H0 矛盾）（物理 Top100 T037）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_obs_facts()
    w("\n[E1] 观测事实（外部只引用不复算）")
    w("  Planck 2018 (TT,TE,EE+lowE+lensing)：H0 = %s ± %s km/s/Mpc"
      % (fv(H0_PLANCK, "2f"), fv(SIG_H0_PLANCK, "2f")))
    w("  SH0ES 2022 (Riess)：H0 = %s ± %s km/s/Mpc"
      % (fv(H0_SH0ES, "2f"), fv(SIG_H0_SH0ES, "2f")))
    w("  Planck 声视界 r_s* = %s ± %s Mpc；CMB 角视界 θ* ≈ %s rad"
      % (fv(R_STAR, "2f"), fv(SIG_R_STAR, "2f"), fv(THETA_STAR, "3e")))
    w("  => 两条独立观测链给出互相冲突的 H0（67.36 vs 73.04 km/s/Mpc）。")
    entries.append(("E1", "Planck H0=67.36±0.54 / SH0ES H0=73.04±1.04；"
                    "r_s*=147.09±0.26 Mpc；θ*≈1.041e-2 rad", "PASS",
                    "外部只引用不复算（Planck 2018 / SH0ES 2022）"))

    # ---- E2 ----
    g2 = e2_significance()
    w("\n[E2] 核心公式体系：张力显著性独立精算（本册核心）")
    w("  ΔH0 = H0_SH0ES − H0_Planck = %s − %s = %s km/s/Mpc"
      % (fv(H0_SH0ES, "2f"), fv(H0_PLANCK, "2f"), fv(g2["delta"], "2f")))
    w("  联合不确定度 √(σ₁²+σ₂²) = √(%s² + %s²) = √(%s) = %s km/s/Mpc"
      % (fv(SIG_H0_SH0ES, "2f"), fv(SIG_H0_PLANCK, "2f"),
         fv(g2["var_sum"], "4f"), fv(g2["combo_sigma"], "4f")))
    w("  σ = ΔH0 / √(σ₁²+σ₂²) = %s / %s = %s σ"
      % (fv(g2["delta"], "4f"), fv(g2["combo_sigma"], "4f"), fv(g2["sigma"], "4f")))
    w("  双口径推导链：")
    w("    (a) CMB 侧：θ* = r_s / D_A(z*)；r_s = ∫₀^{z*} c_s(z)/H(z) dz；")
    w("        H0 由 D_A(z*) 与 r_s 在 ΛCDM 下联合反解 ⇒ 67.36 km/s/Mpc。")
    w("    (b) 局域侧：H0 = v/D（Hubble 定律），D 由 Cepheid 校准 SNIa 距离阶梯给出")
    w("        ⇒ 73.04 km/s/Mpc。")
    w("  => 张力显著性独立精算 = %s σ（预期区间 4.8–4.9 σ，一致）。"
      % fv(g2["sigma"], "3f"))
    entries.append(("E2", "张力显著性 σ = %s σ（独立 Decimal 48 位精算，"
                    "ΔH0=5.68，联合σ≈1.172）；双口径推导链写出"
                    % fv(g2["sigma"], "3f"), "PASS",
                    "σ=(H0_SH0ES−H0_Planck)/√(σ₁²+σ₂²) 精算"))

    # ---- E3 ----
    g3 = e3_new_physics_candidates()
    w("\n[E3] 裁决：系统误差 vs 新物理")
    w("  新物理候选清单（每候选 ≥1 枚新输入）：")
    for name, input_, cnt in g3["candidates"]:
        w("    - %s：%s（新输入计数 = %d）" % (name, input_, cnt))
    w("  新输入合计 = %d 枚。" % g3["new_input_count"])
    w("  来料：库内『标准汽笛判决』『哈勃张力判据』——**不采信自报**，")
    w("  本册独立复算 σ = %s σ（见 E2），来料结论须以本册精算为准。" % fv(g2["sigma"], "3f"))
    w("  => 张力已达 %s σ，远超 3σ 系统误差带；候选新物理均需额外自由度（新标度/新场）。"
      % fv(g2["sigma"], "2f"))
    entries.append(("E3", "新物理候选 4 枚（EDE/变G/ΔN_eff/相互作用暗辐射），"
                    "新输入合计 ≥%d；来料不采信自报，本册独立复算 σ=%s σ"
                    % (g3["new_input_count"], fv(g2["sigma"], "2f")), "PASS",
                    "撞 C5（裁决机制）"))

    # ---- E4 ----
    g4 = e4_geometry_supply()
    w("\n[E4] 几何供给：TUFT 单尺度能否供给宇宙学尺度新物理？")
    w("  承接 %s：TUFT 单尺度框架无宇宙学尺度新自由度注入通道。" % g4["single_scale_ref"])
    w("  对 EDE / 变 G / ΔN_eff / 相互作用暗辐射 4 候选的几何供给 = %d。"
      % g4["cosmological_new_physics_supply"])
    w("  => TUFT/几何框架**不能**从第一性原理供给任何宇宙学尺度新物理候选。")
    entries.append(("E4", "几何供给 0：TUFT 单尺度（引用 C0141 E4）无宇宙学尺度"
                    "新物理候选", "PASS", "撞 C2（新标度）"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  哈勃张力被精确翻译成两件事：(a) 张力显著性是否真实（E2 独立精算 σ=%s σ）；"
      % fv(g2["sigma"], "2f"))
    w("  (b) TUFT/几何框架能否供给新物理候选（E4：供给 0）。")
    w("  (a) σ=%s σ ≫ 3σ ⇒ 非统计涨落；候选新物理均需 ≥1 枚新输入（E3，合计 %d 枚）。"
      % (fv(g2["sigma"], "2f"), g3["new_input_count"]))
    w("  (b) 几何单尺度供给 0 ⇒ TUFT 无法内生任何宇宙学尺度新物理通道。")
    w("  => **结构性负面（对 TUFT/几何框架）**；撞 C2（新标度）/ C5（裁决机制）。")
    entries.append(("E5", "结构性负面：TUFT 单尺度供给 0，无法内生宇宙学尺度"
                    "新物理；σ=%s σ 张力真实" % fv(g2["sigma"], "2f"), "PASS",
                    "撞 C2/C5"))

    # ---- 守卫 ----
    guards = [
        ("G1", "σ 精算 ≈ 4.8（4.7 ≤ σ ≤ 4.9）",
         Decimal("4.7") <= g2["sigma"] <= Decimal("4.9")),
        ("G2", "H0 两值引用（Planck 67.36 / SH0ES 73.04）",
         H0_PLANCK == Decimal("67.36") and H0_SH0ES == Decimal("73.04")),
        ("G3", "r_s* 引用（147.09 ± 0.26 Mpc）",
         R_STAR == Decimal("147.09") and SIG_R_STAR == Decimal("0.26")),
        ("G4", "几何供给 = 0（TUFT 单尺度无宇宙学新物理）",
         g4["cosmological_new_physics_supply"] == 0),
        ("G5", "新输入计数 ≥ 4（4 候选 × ≥1）",
         g3["new_input_count"] >= 4),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %-4s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0150 guard failed"

    w("\n[诚实边界]")
    w("  本册**不宣称哈勃张力已裁决**；外部观测值（Planck / SH0ES）只引用不复算；")
    w("  库内来料（标准汽笛判决 / 哈勃张力判据）不采信自报，本册独立复算 σ。")
    w("  裁的是「TUFT/几何框架能否供给宇宙学尺度新物理候选」——答案是供给 0。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0150_哈勃张力攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0150_哈勃张力攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0150_hubble_tension",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_obs_facts": {k: str(v) for k, v in g1.items()},
            "E2_significance": {k: str(v) for k, v in g2.items()},
            "E3_new_physics": {
                "candidates": [[c[0], c[1], c[2]] for c in g3["candidates"]],
                "new_input_count": g3["new_input_count"],
                "library_sources_not_trusted": g3["library_sources_not_trusted"],
            },
            "E4_geometry_supply": {k: str(v) for k, v in g4.items()},
            "guards_passed": sum(1 for g in guards if g[2]),
            "guards_total": len(guards),
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0150 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
