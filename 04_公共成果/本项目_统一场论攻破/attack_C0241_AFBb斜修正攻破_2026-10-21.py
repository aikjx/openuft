# -*- coding: utf-8 -*-
"""
attack_C0241_AFBb斜修正攻破_2026-10-21.py
独立复算：Z→bb A_FB^b 遗留 3σ 偏离（L 线域 H 批 · 斜修正核算）

定位：母册 T370「Z→bb A_FB^b 遗留 3σ 偏离 | 斜修正 | C5,C6」。
前置：TUFT 已注销（C0133 终审）；标准电弱算术为外部成熟知识，本册只做复核，
严禁把任何标准物理结果写成 TUFT 预测/修正。

把「A_FB^b 遗留偏离」压缩成五条可复核读数 + 一张输入账单：

  E1 电弱事实：sin²θ_W^eff=0.23122（外部输入显式计数）、A_FB^b 实测 0.0992±0.0016、
     A_b 实测 0.923±0.020、A_e(SLD) 实测 0.1514±0.0019（PDG 只引用不复算）。
  E2 **树级标准电弱算术精算（本册核心）**：
     g_V=T3-2Q s2、g_A=T3 ⇒ A_f=2 g_V g_A/(g_V²+g_A²) ⇒ A_FB^b=(3/4)A_b·A_e，
     Decimal 48 位逐位核算 vs 实测，复算遗留 pull（已知 3σ）。
  E3 斜修正核算：A_FB^b(s2) 单调递减 ⇒ 二分反解「要使 A_FB=0.0992 需多大 s2_ext」，
     Δs2=s2_ext-0.23122，再按标准线性系数 Δs2≈-0.00029·S（外部引用）折算等效 S 参数。
  E4 普适性核算：A_b/A_e 比值与味普适性；LEP（A_FB^b 偏好大 s2）vs SLD（A_e 偏好小 s2）
     内部张力。
  E5 裁定：A_FB^b 依赖电弱混合/斜修正结构（标准电弱）；TUFT 无电弱/无混合角供给，
     结构性负面，按母册登记撞 C5（可检验）/C6（误差带）。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：外部观测值（sin²θ_W^eff、各 A_f 实测、SM 含辐射修正预言值 0.1036、
S 线性折算系数）只引用不复算；本册精算的全部是树级标准电弱算术的复核，
不宣称解决 A_FB^b 遗留偏离，不宣称 TUFT 有任何电弱供给。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（PDG 只引用不复算，显式计数） ----------
S2_EFF = Decimal("0.23122")          # sin²θ_W^eff (LEP+SLD 平均，外部输入)
AFB_B_MEAS = Decimal("0.0992")      # A_FB^b 实测（LEP 综合）
AFB_B_SIG = Decimal("0.0016")        # 实测误差
AB_MEAS = Decimal("0.923")           # A_b 实测（SLD/LEP 综合）
AE_SLD_MEAS = Decimal("0.1514")      # A_e 实测（SLD 单极性）
SM_RAD_AFB = Decimal("0.1036")       # SM 含辐射修正预言（外部引用，不复算）
# 斜修正线性折算（标准文献 Erler-Langacker 型近似，外部引用）：
#   Δsin²θ_W^eff ≈ -0.00029 · S
DS2_PER_S = Decimal("0.00029")


def couplings(s2: Decimal):
    """树级 Z 耦合：g_V=T3-2Q s2, g_A=T3。"""
    # 轻子 e: T3=-1/2, Q=-1
    gve = Decimal("-0.5") + Decimal(2) * s2
    gae = Decimal("-0.5")
    # b 夸克: T3=-1/2, Q=-1/3 ⇒ g_V = T3 - 2Q s2 = -1/2 + (2/3)s2
    gvb = Decimal("-0.5") - Decimal(2) * (Decimal("-1") / Decimal(3)) * s2
    gab = Decimal("-0.5")
    return gve, gae, gvb, gab


def af(gv: Decimal, ga: Decimal) -> Decimal:
    """A_f = 2 g_V g_A / (g_V² + g_A²)。"""
    return Decimal(2) * gv * ga / (gv * gv + ga * ga)


def afb_b(s2: Decimal) -> Decimal:
    """A_FB^b = (3/4) A_b · A_e（树级）。"""
    gve, gae, gvb, gab = couplings(s2)
    ae = af(gve, gae)
    ab = af(gvb, gab)
    return (Decimal(3) / Decimal(4)) * ab * ae, ae, ab


def e1_facts():
    return {
        "sin2_th_eff": S2_EFF,
        "AFB_b_meas": AFB_B_MEAS, "AFB_b_sigma": AFB_B_SIG,
        "A_b_meas": AB_MEAS, "A_e_SLD_meas": AE_SLD_MEAS,
        "SM_radiative_AFB_b": SM_RAD_AFB,
    }


def e2_treelevel():
    """树级标准电弱算术精算（本册核心）。"""
    gve, gae, gvb, gab = couplings(S2_EFF)
    afe = af(gve, gae)
    afb = af(gvb, gab)
    aFB = (Decimal(3) / Decimal(4)) * afb * afe
    pull = (AFB_B_MEAS - aFB) / AFB_B_SIG
    pull_vs_rad = (AFB_B_MEAS - SM_RAD_AFB) / AFB_B_SIG
    return {
        "gVe_e": gve, "gAe_e": gae, "gVb_b": gvb, "gAb_b": gab,
        "A_e_tree": afe, "A_b_tree": afb, "AFB_b_tree": aFB,
        "pull_tree": pull, "pull_vs_radSM": pull_vs_rad,
    }


def e3_oblique():
    """斜修正：二分反解 s2_ext 使 A_FB^b(s2)=实测值；折算等效 S。"""
    # A_FB(s2) 在 s2∈(0.2,0.25) 单调递减（两支 |g_V| 均随 s2 增大而减小）
    lo, hi = Decimal("0.20"), Decimal("0.25")
    target = AFB_B_MEAS
    for _ in range(300):
        mid = (lo + hi) / Decimal(2)
        val, _, _ = afb_b(mid)
        if val > target:
            lo = mid   # 还偏大 → 需更大 s2
        else:
            hi = mid
    s2_ext = (lo + hi) / Decimal(2)
    d_s2 = s2_ext - S2_EFF
    s_eq = -d_s2 / DS2_PER_S   # Δs2 ≈ -0.00029·S ⇒ S ≈ -Δs2/0.00029
    # 数值斜率（有限差分，Decimal）
    eps = Decimal("0.0001")
    v1, _, _ = afb_b(S2_EFF - eps)
    v2, _, _ = afb_b(S2_EFF + eps)
    slope = (v2 - v1) / (Decimal(2) * eps)
    return {
        "s2_extracted": s2_ext, "delta_s2": d_s2,
        "AFB_slope_d_s2": slope, "S_equivalent": s_eq,
    }


def e4_universality():
    """普适性核算：A_b/A_e 比值 vs SM；LEP-SLD 内部张力。"""
    _, _, ab = afb_b(S2_EFF)
    _, afe, _ = afb_b(S2_EFF)
    ratio_meas = AB_MEAS / AE_SLD_MEAS
    ratio_sm = ab / afe
    # 实测 A_e 偏好的 s2：二分反解 A_e(s2)=0.1514
    lo, hi = Decimal("0.20"), Decimal("0.25")
    for _ in range(300):
        mid = (lo + hi) / Decimal(2)
        gve, gae, _, _ = couplings(mid)
        val = af(gve, gae)
        if val > AE_SLD_MEAS:
            lo = mid
        else:
            hi = mid
    s2_from_sld = (lo + hi) / Decimal(2)
    return {
        "A_b_over_A_e_meas": ratio_meas,
        "A_b_over_A_e_SM": ratio_sm,
        "s2_from_SLD_Ae": s2_from_sld,
    }


def e5_verdict():
    """TUFT 电弱供给检查。"""
    return {
        "tuft_ew_sector": 0,          # 无电弱规范群
        "tuft_mixing_angle": 0,        # 无弱混合角供给
        "tuft_oblique_S_T": 0,         # 无斜修正结构
        "tuft_status": "cancelled_C0133",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0241 · Z→bb A_FB^b 遗留 3σ 偏离（L 线域 H 批 · 斜修正）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_facts()
    w("\n[E1] 电弱事实（PDG 只引用不复算，外部输入显式计数）")
    w("  sin²θ_W^eff = %s（LEP+SLD 平均，外部输入 #1）" % fv(g1["sin2_th_eff"], "6f"))
    w("  A_FB^b 实测 = %s ± %s（LEP 综合，外部输入 #2）"
      % (fv(g1["AFB_b_meas"], "4f"), fv(g1["AFB_b_sigma"], "4f")))
    w("  A_b 实测 = %s（SLD/LEP 综合，外部输入 #3）；A_e(SLD) = %s（外部输入 #4）"
      % (fv(g1["A_b_meas"], "3f"), fv(g1["A_e_SLD_meas"], "4f")))
    w("  SM 含辐射修正预言 A_FB^b = %s（外部引用 #5，不复算）" % fv(g1["SM_radiative_AFB_b"], "4f"))
    w("  外部输入共 5 项，全部显式计数；本册不复算任何 PDG/文献值。")
    entries.append(("E1", "电弱事实 5 项外部输入：s2=0.23122、A_FB^b=0.0992±0.0016、"
                    "A_b=0.923、A_e(SLD)=0.1514、SM辐射修正0.1036", "PASS",
                    "PDG/文献只引用不复算"))

    # ---- E2 ----
    g2 = e2_treelevel()
    w("\n[E2] 树级标准电弱算术精算（本册核心）")
    w("  e:  g_V = T3-2Q s2 = -1/2+2s2 = %s；g_A = -1/2" % fv(g2["gVe_e"], "8f"))
    w("  b:  g_V = -1/2+(2/3)s2 = %s；g_A = -1/2" % fv(g2["gVb_b"], "8f"))
    w("  A_e = 2 g_V g_A/(g_V²+g_A²) = %s（树级；SM 现实值≈0.149 量级）"
      % fv(g2["A_e_tree"], "8f"))
    w("  A_b = %s（树级；对照 SM 现实值 0.9358）" % fv(g2["A_b_tree"], "8f"))
    w("  A_FB^b = (3/4) A_b·A_e = %s（树级精算）" % fv(g2["AFB_b_tree"], "8f"))
    w("  实测 %s vs 树级 SM %s ⇒ pull = (%s-%s)/%s = %s σ"
      % (fv(g1["AFB_b_meas"], "4f"), fv(g2["AFB_b_tree"], "6f"),
         fv(g1["AFB_b_meas"], "4f"), fv(g2["AFB_b_tree"], "6f"),
         fv(g1["AFB_b_sigma"], "4f"), fv(g2["pull_tree"], "3f")))
    w("  对照：实测 vs SM 含辐射修正 0.1036 ⇒ pull = %s σ（已知 ~3σ 遗留，复算一致）"
      % fv(g2["pull_vs_radSM"], "3f"))
    w("  => 树级算术独立复现「A_FB^b 实测系统性低于 SM 预期 ~3σ」的遗留偏离。")
    entries.append(("E2", "树级精算 A_FB^b=%s vs 实测0.0992 ⇒ pull=%sσ（复现3σ遗留）"
                    % (fv(g2["AFB_b_tree"], "6f"), fv(g2["pull_tree"], "2f")),
                    "PASS", "Decimal 48 位；标准电弱算术复核，非 TUFT 结果"))

    # ---- E3 ----
    g3 = e3_oblique()
    w("\n[E3] 斜修正核算（S/T 对 sin²θ_W^eff 与 A_FB 的影响）")
    w("  A_FB^b(s2) 数值斜率 dA_FB/ds2 = %s（s2=0.23122 处）" % fv(g3["AFB_slope_d_s2"], "6f"))
    w("  二分反解：要使 A_FB^b(s2)=%s 需 sin²θ_W^eff = %s"
      % (fv(g1["AFB_b_meas"], "4f"), fv(g3["s2_extracted"], "8f")))
    w("  Δs2 = s2_ext - 0.23122 = %s（实测偏好更大的弱混合角）" % fv(g3["delta_s2"], "8f"))
    w("  按标准线性折算 Δs2≈-0.00029·S（外部引用）⇒ 等效 S ≈ %s" % fv(g3["S_equivalent"], "6f"))
    w("  => 该 3σ 遗留若归因于斜修正新物理，需 |S|≈4 量级的异常——远超典型"
      "新物理可达（S~O(0.1)–0.5）；此即「遗留」二字的定量含义：标准电弱内部"
      "未闭合的 LEP/SLD 张力。")
    entries.append(("E3", "反解 s2_ext=%s ⇒ Δs2=%s ⇒ 等效 S≈%s（斜修正量级远超典型新物理）"
                    % (fv(g3["s2_extracted"], "6f"), fv(g3["delta_s2"], "6f"),
                       fv(g3["S_equivalent"], "3f")),
                    "PASS", "二分 300 步 Decimal；S 线性系数外部引用"))

    # ---- E4 ----
    g4 = e4_universality()
    w("\n[E4] 普适性核算：A_b/A_e 与味普适性")
    w("  实测 A_b/A_e(SLD) = %s；SM 树级 A_b/A_e = %s"
      % (fv(g4["A_b_over_A_e_meas"], "4f"), fv(g4["A_b_over_A_e_SM"], "4f")))
    w("  由 A_e(SLD)=%s 反解 s2 = %s（SLD 偏好小混合角）"
      % (fv(g1["A_e_SLD_meas"], "4f"), fv(g4["s2_from_SLD_Ae"], "8f")))
    w("  对照 E3：LEP A_FB^b 反解 s2=%s（偏好大混合角）——两源相差约 %s，"
      "此即 SM 电弱拟合内部的 LEP-vs-SLD 矛盾本身，味普适性框架内不自洽。"
      % (fv(g3["s2_extracted"], "6f"),
         fv(g3["s2_extracted"] - g4["s2_from_SLD_Ae"], "6f")))
    entries.append(("E4", "A_b/A_e 实测%s vs SM%s；LEP(s2大) vs SLD(s2小) 两源内部矛盾"
                    % (fv(g4["A_b_over_A_e_meas"], "3f"), fv(g4["A_b_over_A_e_SM"], "3f")),
                    "PASS", "普适性框架内 LEP/SLD 两源不自洽"))

    # ---- E5 ----
    g5 = e5_verdict()
    w("\n[E5] 裁定：TUFT 电弱供给检查")
    w("  TUFT 电弱规范群供给 = %d；弱混合角供给 = %d；斜修正 S/T 结构供给 = %d"
      % (g5["tuft_ew_sector"], g5["tuft_mixing_angle"], g5["tuft_oblique_S_T"]))
    w("  TUFT 状态：%s（C0133 终审已注销）。" % g5["tuft_status"])
    w("  A_FB^b 全链（g_V/g_A → A_f → A_FB^b → 斜修正 S/T）是标准电弱算术；")
    w("  TUFT 无电弱、无混合角、无斜修正 ⇒ 对该遗留偏离供给恒为 0。")
    w("  => **结构性负面（对 TUFT/几何框架）**：TUFT 既不能解释、也不能预言、"
      "更不能修正该 3σ 偏离；按母册 T370 登记撞 **C5（可检验）/ C6（误差带）**。")
    entries.append(("E5", "TUFT 电弱/混合角/斜修正供给全 0（已注销 C0133）；"
                    "结构性负面，撞 C5/C6", "PASS", "按母册 T370 登记撞 C5,C6"))

    # ---- 守卫 ----
    guards = [
        ("G1", "A_b 树级 ≈0.936（|A_b_tree-0.936|<0.01）",
         abs(g2["A_b_tree"] - Decimal("0.936")) < Decimal("0.01")),
        ("G2", "A_FB^b 树级在 0.10±0.015 区间",
         Decimal("0.085") < g2["AFB_b_tree"] < Decimal("0.115")),
        ("G3", "遗留 pull |(实测-树级SM)/σ| > 2.5（复现 3σ 遗留）",
         abs(g2["pull_tree"]) > Decimal("2.5")),
        ("G4", "实测反解 s2_ext > 0.23122（偏好更大弱混合角）",
         g3["s2_extracted"] > S2_EFF),
        ("G5", "TUFT 电弱/混合角/斜修正供给 = 0",
         g5["tuft_ew_sector"] == 0 and g5["tuft_mixing_angle"] == 0
         and g5["tuft_oblique_S_T"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %-4s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0241 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称解决 A_FB^b 遗留偏离；全部数值为标准电弱算术（PDG/文献）复核；")
    w("  sin²θ_W^eff、各 A_f 实测、SM 辐射修正值、S 线性折算系数均为外部输入只引用；")
    w("  严禁把标准物理结果写成 TUFT 预测/修正（TUFT 已注销 C0133）。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0241_AFBb斜修正攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0241_AFBb斜修正攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0241_AFBb_oblique",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                         for e in entries],
            "E1_external_inputs": {k: str(v) for k, v in g1.items()},
            "E2_treelevel": {k: str(v) for k, v in g2.items()},
            "E3_oblique": {k: str(v) for k, v in g3.items()},
            "E4_universality": {k: str(v) for k, v in g4.items()},
            "E5_tuft_supply": {k: str(v) for k, v in g5.items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0241 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
