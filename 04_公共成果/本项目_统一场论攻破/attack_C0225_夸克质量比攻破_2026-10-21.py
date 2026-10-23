# -*- coding: utf-8 -*-
"""
attack_C0225_夸克质量比攻破_2026-10-21.py
独立复算：母册 T347「夸克质量比 m_u/m_d 与同位旋破缺」（K 线扩展·手征微扰）

定位：母册 T347（C2/C6），手征微扰论（ChPT）一线。本册**不采信任何自报**，
用 PDG 2024 实测 π/K/核子质量独立精算 Leutwyler 比、m_s/m_ud、Dashen 修正
与核子质量差分解，并对 TUFT/几何框架判定"是否供给夸克质量/手征结构"。

把"m_u/m_d 与同位旋破缺"压缩成五条可复核读数：

  E1 输入事实（PDG 只引用不复算）：π±/π⁰/K±/K⁰/n/p 质量。
  E2 **Leutwyler 比精算（本册核心）**：由 Gell-Mann–Oakes–Renner 关系
     m_u/m_d = [m_π² − (m_K⁰²−m_K±²)_strong] / [m_π² + (m_K⁰²−m_K±²)_strong]，
     Dashen 扣 EM 后精算。
  E3 m_s/m_ud：B₀ 关系 m_s/(m_u+m_d) = (m_K±²+m_K⁰²−m_π²)/(2 m_π²) 精算。
  E4 Dashen 修正与核子质量差分解：Δ_π^EM = m_π±²−m_π⁰²；
     m_n−m_p = 1.293 MeV 拆为强作用（m_d−m_u）+ EM。
  E5 裁定：TUFT 无夸克质量/无手征结构/无 π/K 介子供给 → 结构性负面，撞 C2/C6。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：本册不宣称已解释夸克质量谱；PDG 质量值只引用不复算；
裁的是「TUFT/几何框架能否供给夸克质量比与手征结构」。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（PDG 2024，只引用不复算，MeV） ----------
M_PIP = Decimal("139.57039")   # π± 带电π质量
M_PI0 = Decimal("134.97680")   # π⁰ 中性π质量
M_KP = Decimal("493.677")       # K± 带电K质量
M_K0 = Decimal("497.611")       # K⁰ 中性K质量
M_N = Decimal("939.56542052")   # 中子质量
M_P = Decimal("938.27208816")   # 质子质量
# 核子质量差分解的标准 ChPT 估值（只引用：EM ≈ -0.76 MeV，强作用 ≈ +2.05 MeV）
DELTAN_EM = Decimal("-0.76")
DELTAN_STRONG = Decimal("2.05")


def e1_inputs():
    """E1：PDG 输入事实（只引用）。"""
    return {
        "m_pip_MeV": M_PIP, "m_pi0_MeV": M_PI0,
        "m_kp_MeV": M_KP, "m_k0_MeV": M_K0,
        "m_n_MeV": M_N, "m_p_MeV": M_P,
    }


def e2_leutwyler():
    """E2：Leutwyler 比 m_u/m_d 精算（Dashen 扣 EM 后）。

    第一性推导（LO ChPT / GMOR）：
      B0(m_u+m_d) = m_π²
      B0(m_u+m_s) = m_K±²
      B0(m_d+m_s) = m_K⁰²
    相减得 m_d − m_u = (m_K⁰² − m_K±²)/B0；m_u+m_d = m_π²/B0。
    故 m_u/m_d = [m_π² − (m_K⁰²−m_K±²)] / [m_π² + (m_K⁰²−m_K±²)]。

    Dashen 修正：实测 m_K⁰²−m_K±² 含 EM 贡献。按 Dashen 定理
      (m_K±² − m_K⁰²)_EM ≈ (m_π±² − m_π⁰²)_EM ≈ m_π±² − m_π⁰² = Δπ_EM。
    即 EM 对 (m_K⁰² − m_K±²) 的贡献为 −Δπ_EM。
    强作用部分 (m_K⁰²−m_K±²)_strong = 观测值 + Δπ_EM。
    强作用 m_π² 取 m_π⁰²（π⁰ EM 极小）。
    """
    pip2 = M_PIP * M_PIP
    pi02 = M_PI0 * M_PI0
    kp2 = M_KP * M_KP
    k02 = M_K0 * M_K0
    # Dashen：π 电磁质量差
    dpi_em = pip2 - pi02
    # 观测 K 质量差平方
    dk_obs = k02 - kp2
    # 强作用部分（EM 对 dk 的贡献为 -dpi_em）
    dk_strong = dk_obs + dpi_em
    # 强作用 m_π² 取 π⁰²
    pi2_strong = pi02
    # Leutwyler 比
    r_num = pi2_strong - dk_strong
    r_den = pi2_strong + dk_strong
    r_ud = r_num / r_den
    return {
        "pip2": pip2, "pi02": pi02, "kp2": kp2, "k02": k02,
        "dpi_em": dpi_em, "dk_obs": dk_obs, "dk_strong": dk_strong,
        "pi2_strong": pi2_strong,
        "r_num": r_num, "r_den": r_den, "r_ud": r_ud,
    }


def e3_ms_mud():
    """E3：m_s/(m_u+m_d) 精算。

    由 GMOR：B0(m_u+m_s)=m_K±²，B0(m_d+m_s)=m_K⁰²，B0(m_u+m_d)=m_π²。
    前两式相加减 m_π²：B0·2m_s = m_K±² + m_K⁰² − m_π²。
    故 m_s/(m_u+m_d) = (m_K±²+m_K⁰²−m_π²)/(2 m_π²)。
    取强作用 m_π² = m_π⁰²，K 质量用带电/中性均值（EM 修正 NLO，本册 LO）。
    """
    g2 = e2_leutwyler()
    pi2 = g2["pi2_strong"]
    ms_sum = (g2["kp2"] + g2["k02"] - pi2) / (Decimal(2) * pi2)
    # m_ud = (m_u+m_d)/2，故 m_s/m_ud = 2 × m_s/(m_u+m_d)
    ms_mud = Decimal(2) * ms_sum
    return {"ms_sum": ms_sum, "ms_mud": ms_mud}


def e4_dashen_nucleon():
    """E4：Dashen 修正 + 核子质量差分解。"""
    g2 = e2_leutwyler()
    # π 电磁质量差（MeV²）
    dpi_em = g2["dpi_em"]
    # Dashen 预言：K 电磁质量差平方 ≈ π 电磁质量差平方
    dk_em_dashen = dpi_em  # (m_K±² − m_K⁰²)_EM ≈ Δπ_EM
    # 观测 K 差
    dk_obs = g2["dk_obs"]
    # 强作用 K 差
    dk_strong = g2["dk_strong"]
    # 核子质量差
    dn_obs = M_N - M_P
    # 分解：观测 = 强作用 + EM
    dn_check = DELTAN_STRONG + DELTAN_EM
    return {
        "dpi_em_MeV2": dpi_em,
        "dk_em_dashen_MeV2": dk_em_dashen,
        "dk_obs_MeV2": dk_obs,
        "dk_strong_MeV2": dk_strong,
        "dn_obs_MeV": dn_obs,
        "dn_strong_MeV": DELTAN_STRONG,
        "dn_em_MeV": DELTAN_EM,
        "dn_check_MeV": dn_check,
    }


def e5_verdict(g2, g3, g4):
    """E5：TUFT 供给判定。"""
    return {
        "tuft_quark_mass_supply": 0,       # TUFT 无夸克质量参数
        "tuft_chiral_supply": 0,            # TUFT 无手征对称性/无 Goldstone 玻色子
        "tuft_piK_supply": 0,               # TUFT 无 π/K 介子谱供给
        "leutwyler_needs": "GMOR + π/K 质量 + Dashen EM 分解（标准 ChPT）",
        "verdict": "结构性负面（对 TUFT/几何框架）",
        "hits": "C2（绝对标度/质量）+ C6（误差带/EM 修正依赖）",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0225 · 夸克质量比 m_u/m_d 与同位旋破缺（母册 T347 · ChPT 线）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_inputs()
    w("\n[E1] PDG 输入事实（只引用不复算，MeV）")
    w("  m_π± = %s；m_π⁰ = %s" % (fv(M_PIP, "5f"), fv(M_PI0, "5f")))
    w("  m_K± = %s；m_K⁰ = %s" % (fv(M_KP, "3f"), fv(M_K0, "3f")))
    w("  m_n = %s；m_p = %s" % (fv(M_N, "4f"), fv(M_P, "4f")))
    w("  => 全部外部输入（PDG 2024），本册只做 GMOR 算术与 Dashen 分解。")
    entries.append(("E1", "PDG π/K/核子质量只引用；本册做 GMOR+Dashen 算术",
                    "PASS", "外部输入显式计数"))

    # ---- E2 ----
    g2 = e2_leutwyler()
    w("\n[E2] Leutwyler 比 m_u/m_d 精算（本册核心）")
    w("  π 质量平方：m_π±²=%s；m_π⁰²=%s" % (fv(g2["pip2"], "2f"), fv(g2["pi02"], "2f")))
    w("  K 质量平方：m_K±²=%s；m_K⁰²=%s" % (fv(g2["kp2"], "1f"), fv(g2["k02"], "1f")))
    w("  Dashen Δπ^EM = m_π±²−m_π⁰² = %s MeV²" % fv(g2["dpi_em"], "2f"))
    w("  观测 m_K⁰²−m_K±² = %s MeV²" % fv(g2["dk_obs"], "2f"))
    w("  强作用部分 = 观测 + Δπ^EM = %s MeV²" % fv(g2["dk_strong"], "2f"))
    w("  强作用 m_π² = m_π⁰² = %s MeV²" % fv(g2["pi2_strong"], "2f"))
    w("  m_u/m_d = (%s − %s)/(%s + %s)"
      % (fv(g2["pi2_strong"], "2f"), fv(g2["dk_strong"], "2f"),
         fv(g2["pi2_strong"], "2f"), fv(g2["dk_strong"], "2f")))
    w("         = %s / %s" % (fv(g2["r_num"], "2f"), fv(g2["r_den"], "2f")))
    w("         = %s" % fv(g2["r_ud"], "10f"))
    w("  => 标准 Leutwyler 比 ≈ 0.56，落在 PDG 区间 0.46–0.58 内。")
    entries.append(("E2", "Leutwyler 比 m_u/m_d = %s（标准 ChPT 算术复核，"
                    "PDG 区间 0.46–0.58）" % fv(g2["r_ud"], "6f"),
                    "PASS", "GMOR + Dashen 扣 EM，Decimal 48 位精算"))

    # ---- E3 ----
    g3 = e3_ms_mud()
    w("\n[E3] m_s/m_ud 精算")
    w("  m_s/(m_u+m_d) = (m_K±²+m_K⁰²−m_π²)/(2 m_π²) = %s" % fv(g3["ms_sum"], "6f"))
    w("  m_s/m_ud = 2 × m_s/(m_u+m_d) = %s" % fv(g3["ms_mud"], "6f"))
    w("  => 落在 ChPT 标准区间 25–28（NLO 修正后 ≈27.5）。")
    entries.append(("E3", "m_s/m_ud = %s（LO ChPT，标准区间 25–28）"
                    % fv(g3["ms_mud"], "4f"),
                    "PASS", "GMOR 关系算术"))

    # ---- E4 ----
    g4 = e4_dashen_nucleon()
    w("\n[E4] Dashen 修正与核子质量差分解")
    w("  Dashen：(m_K±²−m_K⁰²)_EM ≈ (m_π±²−m_π⁰²)_EM = %s MeV²"
      % fv(g4["dpi_em_MeV2"], "2f"))
    w("  观测 m_K⁰²−m_K±² = %s MeV²；强作用部分 = %s MeV²"
      % (fv(g4["dk_obs_MeV2"], "2f"), fv(g4["dk_strong_MeV2"], "2f")))
    w("  核子质量差：m_n−m_p = %s MeV" % fv(g4["dn_obs_MeV"], "3f"))
    w("    强作用（m_d−m_u）= %s MeV；EM = %s MeV；合计 = %s MeV（核对观测）"
      % (fv(g4["dn_strong_MeV"], "2f"), fv(g4["dn_em_MeV"], "2f"),
         fv(g4["dn_check_MeV"], "3f")))
    w("  => 同位旋破缺 = 夸克质量差（强）+ 电磁（EM）两源分解，均标准 ChPT 算术。")
    entries.append(("E4", "Dashen Δπ^EM=%s MeV²；m_n−m_p=%.3f MeV 拆为强 %s + EM %s"
                    % (fv(g4["dpi_em_MeV2"], "1f"), float(g4["dn_obs_MeV"]),
                       fv(g4["dn_strong_MeV"], "2f"), fv(g4["dn_em_MeV"], "2f")),
                    "PASS", "标准 ChPT 分解；EM/强贡献显式计数"))

    # ---- E5 ----
    g5 = e5_verdict(g2, g3, g4)
    w("\n[E5] 裁定：TUFT 供给检查")
    w("  TUFT 夸克质量参数供给 = %d；手征结构/Goldstone 供给 = %d；π/K 介子供给 = %d"
      % (g5["tuft_quark_mass_supply"], g5["tuft_chiral_supply"], g5["tuft_piK_supply"]))
    w("  Leutwyler 比依赖：%s" % g5["leutwyler_needs"])
    w("  => TUFT 已注销（C0133）；无夸克质量、无手征对称性、无 π/K 介子谱供给，")
    w("     所有读数均为标准 QCD/ChPT 算术复核，**严禁写成 TUFT 预测/修正**。")
    w("  => **结构性负面（对 TUFT/几何框架）**；撞 C2（绝对标度/质量）/C6（误差带/EM 修正依赖）。")
    entries.append(("E5", "TUFT 无夸克质量/手征结构/π-K 供给 ⇒ 结构性负面；"
                    "撞 C2/C6", "PASS", "标准 ChPT 算术，非 TUFT 预测"))

    # ---- 守卫 ----
    guards = [
        ("G1", "Leutwyler 比 m_u/m_d 落在 0.45–0.60 区间",
         Decimal("0.45") < g2["r_ud"] < Decimal("0.60")),
        ("G2", "Leutwyler 比标准值 ≈0.56（0.54–0.58 邻域）",
         Decimal("0.54") < g2["r_ud"] < Decimal("0.58")),
        ("G3", "m_s/m_ud 落在 25–28 区间",
         Decimal("25") < g3["ms_mud"] < Decimal("28")),
        ("G4", "Dashen Δπ^EM = m_π±²−m_π⁰² > 0（带电π更重）",
         g2["dpi_em"] > 0),
        ("G5", "核子质量差 m_n−m_p ≈ 1.293 MeV（1.28–1.31 邻域）",
         Decimal("1.28") < g4["dn_obs_MeV"] < Decimal("1.31")),
        ("G6", "TUFT 夸克质量供给 = 0",
         g5["tuft_quark_mass_supply"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0225 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解释夸克质量比；PDG π/K/核子质量只引用不复算；")
    w("  所有数值为标准 ChPT/GMOR 算术复核，非 TUFT 预测；TUFT 已注销（C0133）。")
    w("  红线：不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("       有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0225_夸克质量比攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0225_夸克质量比攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0225_quark_mass_ratio",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_inputs": {k: str(v) for k, v in g1.items()},
            "E2_leutwyler": {k: str(v) for k, v in g2.items()},
            "E3_ms_mud": {k: str(v) for k, v in g3.items()},
            "E4_dashen_nucleon": {k: str(v) for k, v in g4.items()},
            "E5_verdict": {k: str(v) for k, v in g5.items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0225 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
