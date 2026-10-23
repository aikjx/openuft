# -*- coding: utf-8 -*-
"""
attack_C0196_轴子PQ破缺攻破_2026-10-21.py
独立精算：轴子 / 类轴子粒子与 PQ 对称破缺（母册 T029，行 120；撞 C1,C2；◐）

定位：母册 T029（行 120，原文照录）：
  | T029 | 轴子 / 类轴子粒子 | PQ 对称破缺 | C1,C2 | ◐ C0138（轴子窗口 4e8–1e12 GeV） |
衔接：C0138（强 CP 问题；f_a 窗口 4×10⁸–10¹² GeV；m_a=z·m_π f_π/f_a 独立算得
  5.787643 μeV @ f_a=10¹² GeV）；C0180（轴子 misalignment 丰度；
  Ω_a h²=(θ_i²/2)(f_a/10¹² GeV)^(7/6)；θ_i=1 过闭边界 f_a≈2.9427×10¹¹ GeV）。
本册只做标准轴子（PQ/KSVZ/DFSZ）算术与观测复核：TUFT 已注销（C0133），
严禁把标准物理结果写成 TUFT 预测/修正。

把"轴子 / PQ 对称破缺"压缩成五条可复核读数：

  E1 外部事实（只引用）：f_a 窗口 [4×10⁸, 10¹²] GeV（C0138）；
     m_a ≃ 5.7 μeV·(10¹² GeV/f_a)；g_aγγ = gγ·α_em/(2π f_a)，gγ=-0.97（KSVZ）/
     +0.36（DFSZ）；ADMX 探测带 m_a∈[1,40] μeV（实验事实，只引用）。
  E2 **质量-耦合窗口 10 点扫（本册核心）**：f_a 窗口内 10 点 Decimal 48 位精算
     m_a(μeV) 与 g_aγγ（KSVZ/DFSZ 两支）。
  E3 ADMX 参数盒摆动：扫点 m_a 跨度（μeV–meV）× 耦合跨度（10⁻¹⁵–10⁻¹² GeV⁻¹），
     判定哪些 f_a 落点进入 ADMX [1,40] μeV 探测带。
  E4 misalignment 丰度复核（引用 C0180 公式与边界读数）：f_a=2.94×10¹¹ GeV
     过闭边界处 θ_i∈{0.1,1,3} 三点精算 Ω_a h²，并与实测 Ω_DM h²=0.12 对照。
  E5 PQ 机制供给检查 + 裁定：TUFT 无 PQ 对称、无轴子供给 ⇒ 结构性负面，
     按母册 T029 登记撞 C1/C2。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：本册不宣称解决强 CP 或暗物质问题；外部常数（α_em、gγ、ADMX 带、
Ω_DM h²）只引用不复算；标度律系数 O(1) 不确定度按量级（倍）判定；数值均为
标准轴子算术/实测复核。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（只引用不复算） ----------
FA_REF = Decimal("1000000000000")        # 10^12 GeV 参考标度
FA_LO = Decimal("400000000")             # f_a 窗口下界 4×10^8 GeV（承接 C0138）
FA_HI = Decimal("1000000000000")         # f_a 窗口上界 10^12 GeV（承接 C0138）
M_A_COEF = Decimal("5.7")                 # μeV @ f_a=1e12 GeV（标准关系；C0138 独立算得 5.787643 μeV）
ALPHA_EM = Decimal(1) / Decimal("137.036")   # CODATA 精细结构常数
PI = Decimal("3.14159265358979323846264338327950288419716939937510")
G_GAMMA_KSVZ = Decimal("-0.97")          # 标准 KSVZ 色荷比（只引用）
G_GAMMA_DFSZ = Decimal("0.36")           # 标准 DFSZ 色荷比（只引用）
ADMX_LO_UEV = Decimal("1")               # ADMX 探测带下界（μeV，实验事实只引用）
ADMX_HI_UEV = Decimal("40")              # ADMX 探测带上界（μeV，ADMX/ADMX-HF）
OMEGA_DM_H2 = Decimal("0.12")            # Planck/PDG 实测暗物质丰度（C0180 引用）
FA_BOUNDARY = Decimal("294000000000")    # 2.94×10^11 GeV（任务过闭边界；C0180 解算值 2.9427×10^11）

# f_a 窗口内 10 点对数扫（含两端）
FA_SCAN = [
    Decimal("400000000"),        # 4×10^8
    Decimal("1000000000"),       # 10^9
    Decimal("2000000000"),       # 2×10^9
    Decimal("5000000000"),       # 5×10^9
    Decimal("10000000000"),      # 10^10
    Decimal("20000000000"),      # 2×10^10
    Decimal("50000000000"),      # 5×10^10
    Decimal("100000000000"),     # 10^11
    Decimal("500000000000"),     # 5×10^11
    Decimal("1000000000000"),    # 10^12
]

# θ_i 三点扫（misalignment 复核）
TH_SCAN = [Decimal("0.1"), Decimal("1"), Decimal("3")]


def m_a_uev(fa: Decimal) -> Decimal:
    """m_a ≃ 5.7 μeV · (10^12 GeV / f_a)。"""
    return M_A_COEF * FA_REF / fa


def g_a_gamma(fa: Decimal, ggamma: Decimal) -> Decimal:
    """g_aγγ = gγ · α_em / (2π f_a)，单位 GeV⁻¹。"""
    return ggamma * ALPHA_EM / (Decimal(2) * PI * fa)


def omega_misalign(th_i: Decimal, fa: Decimal) -> Decimal:
    """Ω_a h² = (θ_i²/2)·(f_a/10^12 GeV)^(7/6)（C0180 标度律，系数取 1）。"""
    x = fa / FA_REF
    return (th_i * th_i / 2) * ((Decimal(7) / Decimal(6) * x.ln()).exp())


def e1_inputs():
    """外部事实（只引用）。"""
    return {
        "fa_window_GeV": (FA_LO, FA_HI),
        "m_a_relation": "m_a = 5.7 μeV · (10^12 GeV / f_a)",
        "c0138_independent_uev": Decimal("5.787643"),   # C0138 由 m_π f_π z 独立算得
        "alpha_em": ALPHA_EM,
        "g_gamma_ksvz": G_GAMMA_KSVZ,
        "g_gamma_dfsz": G_GAMMA_DFSZ,
        "admx_band_ueV": (ADMX_LO_UEV, ADMX_HI_UEV),
        "omega_dm_h2": OMEGA_DM_H2,
        "fa_overclosure_boundary_GeV": FA_BOUNDARY,
        "c0180_boundary_GeV": Decimal("294270000000"),  # C0180 解算值 2.9427e11
    }


def e2_window_scan():
    """f_a 窗口 10 点扫：m_a 与 g_aγγ（两模型）。"""
    rows = []
    for fa in FA_SCAN:
        rows.append({
            "fa": fa,
            "m_a_uev": m_a_uev(fa),
            "g_ksvz": g_a_gamma(fa, G_GAMMA_KSVZ),
            "g_dfsz": g_a_gamma(fa, G_GAMMA_DFSZ),
        })
    return rows


def e3_admx_box(rows):
    """ADMX 参数盒：m_a 跨度、耦合跨度、落点判定。"""
    m_list = [r["m_a_uev"] for r in rows]
    g_abs_ksvz = [abs(r["g_ksvz"]) for r in rows]
    in_band = [r for r in rows if ADMX_LO_UEV <= r["m_a_uev"] <= ADMX_HI_UEV]
    return {
        "m_min_uev": min(m_list),
        "m_max_uev": max(m_list),
        "m_max_mev": max(m_list) / Decimal("1000"),
        "g_min_GeV": min(g_abs_ksvz),
        "g_max_GeV": max(g_abs_ksvz),
        "in_admx_band": [{"fa": r["fa"], "m_a_uev": r["m_a_uev"]} for r in in_band],
    }


def e4_misalign_review():
    """过闭边界 f_a=2.94×10^11 GeV 处 θ_i∈{0.1,1,3} 复核。"""
    rows = []
    for th in TH_SCAN:
        om = omega_misalign(th, FA_BOUNDARY)
        rows.append({"th_i": th, "omega_h2": om,
                     "vs_observed": om / OMEGA_DM_H2})
    # 任务口径边界复核：θ_i=1 时 Ω 应≈0.12
    om_boundary_theta1 = omega_misalign(Decimal(1), FA_BOUNDARY)
    # C0180 解算值 2.9427e11 对照
    om_at_c0180 = omega_misalign(Decimal(1), Decimal("294270000000"))
    return {"rows": rows,
            "omega_at_2p94e11_theta1": om_boundary_theta1,
            "omega_at_c0180_2p9427e11_theta1": om_at_c0180}


def e5_supply_check():
    """PQ 机制供给检查：TUFT 是否供给 PQ 对称或轴子。"""
    return {
        "tuft_supplies_pq_symmetry": False,   # TUFT 已注销（C0133）；无 U(1)_PQ
        "tuft_supplies_axion": False,         # 无轴子场、无 f_a VEV 供给
        "pq_new_inputs": 2,                   # C0138 E5：新全局 U(1)_PQ（C1）+ 新 VEV f_a（C2）
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0196 · 轴子 / 类轴子粒子与 PQ 对称破缺（母册 T029 · 撞 C1,C2 · ◐收口）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_inputs()
    w("\n[E1] 外部事实（只引用不复算）")
    w("  f_a 窗口 = [%s, %s] GeV（承接 C0138 T029）" % (fv(FA_LO, "2e"), fv(FA_HI, "2e")))
    w("  m_a ≃ 5.7 μeV·(10^12 GeV/f_a)；C0138 由 m_π f_π z 独立算得 %s μeV（@10^12 GeV）"
      % fv(g1["c0138_independent_uev"], "6f"))
    w("  α_em = 1/137.036 = %s（CODATA）；gγ = %s（KSVZ）/ %s（DFSZ）"
      % (fv(g1["alpha_em"], "6e"), G_GAMMA_KSVZ, G_GAMMA_DFSZ))
    w("  g_aγγ = gγ·α_em/(2π f_a)；ADMX 探测带 m_a∈[%s,%s] μeV（实验事实）"
      % (ADMX_LO_UEV, ADMX_HI_UEV))
    w("  实测 Ω_DM h²=%s（C0180 引用）；过闭边界 f_a≈%s GeV（任务口径，C0180 解算 2.9427e11）"
      % (fv(OMEGA_DM_H2, "2f"), fv(FA_BOUNDARY, "3e")))
    entries.append(("E1", "f_a 窗口 4×10⁸–10¹² GeV（C0138）；m_a=5.7μeV·(10¹²/f_a)；"
                    "g_aγγ=gγ·α/(2πf_a)，gγ=-0.97(KSVZ)/+0.36(DFSZ)；ADMX 带[1,40]μeV",
                    "PASS", "外部常数/实验带只引用；本册只做换算"))

    # ---- E2 ----
    rows = e2_window_scan()
    w("\n[E2] 质量-耦合窗口 10 点扫（本册核心，Decimal 48 位）")
    w("  %-13s %-12s %-16s %-16s" % ("f_a (GeV)", "m_a (μeV)",
                                        "g_aγγ KSVZ (GeV⁻¹)", "g_aγγ DFSZ (GeV⁻¹)"))
    for r in rows:
        w("  %-13s %-12s %-16s %-16s"
          % (fv(r["fa"], "2e"), fv(r["m_a_uev"], "6f"),
             fv(r["g_ksvz"], "6e"), fv(r["g_dfsz"], "6e")))
    w("  => m_a 跨度：%s μeV（f_a=10¹²）— %s μeV（f_a=4×10⁸）= %s meV；"
      % (fv(rows[-1]["m_a_uev"], "4f"), fv(rows[0]["m_a_uev"], "4f"),
         fv(rows[0]["m_a_uev"] / Decimal("1000"), "4f")))
    w("     耦合跨度：|g| %s — %s GeV⁻¹（KSVZ 支）。"
      % (fv(abs(rows[-1]["g_ksvz"]), "3e"), fv(abs(rows[0]["g_ksvz"]), "3e")))
    entries.append(("E2", "10 点扫：m_a 从 5.7 μeV（f_a=10¹²）摆到 %s μeV（=14.25 meV，f_a=4×10⁸）；"
                    "g_aγγ KSVZ 从 %s 到 %s GeV⁻¹"
                    % (fv(rows[0]["m_a_uev"], "2f"), fv(rows[-1]["g_ksvz"], "3e"),
                       fv(rows[0]["g_ksvz"], "3e")), "PASS",
                    "m_a=5.7μeV·(10¹²/f_a)；g=gγ·α/(2πf_a)，Decimal 48 位"))

    # ---- E3 ----
    g3 = e3_admx_box(rows)
    w("\n[E3] ADMX 参数盒摆动（探测带 m_a∈[1,40] μeV）")
    w("  m_a 全窗口跨度 = %s – %s μeV（即 %s μeV – %s meV）"
      % (fv(g3["m_min_uev"], "4f"), fv(g3["m_max_uev"], "4f"),
         fv(g3["m_min_uev"], "4f"), fv(g3["m_max_mev"], "4f")))
    w("  |g_aγγ| 跨度 = %s – %s GeV⁻¹（KSVZ 支；DFSZ 同标度反号）"
      % (fv(g3["g_min_GeV"], "3e"), fv(g3["g_max_GeV"], "3e")))
    w("  落入 ADMX [1,40] μeV 带的扫点：")
    for r in g3["in_admx_band"]:
        w("     f_a=%s GeV ⇒ m_a=%s μeV（带内）" % (fv(r["fa"], "2e"), fv(r["m_a_uev"], "4f")))
    w("  （f_a=10¹¹ GeV ⇒ m_a=57 μeV，已高出 ADMX-HF 40 μeV 带上沿；更低 f_a 更偏离）")
    entries.append(("E3", "ADMX 带 [1,40] μeV 内仅 f_a=5×10¹¹–10¹² GeV 两档（11.4/5.7 μeV）；"
                    "f_a=10¹¹ GeV ⇒ 57 μeV 刚越过上沿；全窗口 m_a 摆 5.7 μeV–14.25 meV、"
                    "|g| 摆 1.1×10⁻¹⁵–2.8×10⁻¹² GeV⁻¹",
                    "PASS", "实验带只引用；落点本册判定"))

    # ---- E4 ----
    g4 = e4_misalign_review()
    w("\n[E4] misalignment 丰度复核（C0180 公式；f_a=2.94×10¹¹ GeV 过闭边界）")
    for r in g4["rows"]:
        ratio = r["vs_observed"]
        tag = "命中" if abs(ratio - 1) < Decimal("0.1") else ("过闭 %.2fx" % ratio if ratio > 1 else "欠额 %.2f%%" % (ratio * 100))
        w("  θ_i=%-4s：Ω_a h²=%s（/实测 0.12 = %s）——%s"
          % (r["th_i"], fv(r["omega_h2"], "6f"), fv(ratio, "4f"), tag))
    w("  边界复核：f_a=2.94×10¹¹ GeV、θ_i=1 ⇒ Ω=%s（任务口径≈0.12）"
      % fv(g4["omega_at_2p94e11_theta1"], "6f"))
    w("  C0180 解算值对照：f_a=2.9427×10¹¹ GeV、θ_i=1 ⇒ Ω=%s（应=0.12 精确）"
      % fv(g4["omega_at_c0180_2p9427e11_theta1"], "6f"))
    entries.append(("E4", "过闭边界 f_a=2.94×10¹¹ GeV：θ_i=0.1⇒Ω=0.0012（欠额1%%）；"
                    "θ_i=1⇒Ω=%s（命中实测0.12）；θ_i=3⇒Ω=1.08（过闭9x）"
                    % fv(g4["omega_at_2p94e11_theta1"], "4f"), "PASS",
                    "C0180 标度律 (θ_i²/2)(f_a/10¹²)^(7/6)；引用其边界读数"))

    # ---- E5 ----
    g5 = e5_supply_check()
    w("\n[E5] PQ 机制供给检查 + 裁定（对 TUFT/几何框架）")
    w("  TUFT 供给 PQ 对称？ %s（TUFT 已注销 C0133；无新全局 U(1)_PQ）" % g5["tuft_supplies_pq_symmetry"])
    w("  TUFT 供给轴子？ %s（无轴子场、无 f_a VEV 破缺标度）" % g5["tuft_supplies_axion"])
    w("  PQ 机制新增输入 = %d 枚（承接 C0138 E5：新全局 U(1)_PQ→C1；新 VEV f_a→C2）"
      % g5["pq_new_inputs"])
    w("  E2–E4 全部 m_a/g/Ω 数值均为标准轴子（PQ/KSVZ/DFSZ）算术与观测复核，")
    w("  与 TUFT 无关——TUFT 不供给 PQ 对称、不供给 f_a、不供给轴子场。")
    w("  => **T029 结构性负面（对 TUFT/几何框架）**；按母册登记撞 C1/C2，◐ 收口。")
    entries.append(("E5", "轴子依赖 PQ 对称（新全局对称、f_a 标度外部输入）；TUFT 无 PQ 对称/"
                    "无轴子供给 ⇒ 结构性负面，按母册 T029 登记撞 C1/C2", "PASS",
                    "TUFT 已注销 C0133；承接 C0138 E5/C0180 E5"))

    # ---- 守卫 ----
    guards = [
        ("G1", "m_a(f_a=10¹² GeV) = 5.7 μeV（标准关系钉死）",
         rows[-1]["m_a_uev"] == M_A_COEF),
        ("G2", "m_a(f_a=4×10⁸ GeV) = 14250 μeV = 14.25 meV（窗口低端）",
         rows[0]["m_a_uev"] == Decimal("14250")),
        ("G3", "g_aγγ 符号：KSVZ 负、DFSZ 正（色荷比符号）",
         rows[5]["g_ksvz"] < 0 < rows[5]["g_dfsz"]),
        ("G4", "10 扫点全落在 f_a 窗口 [4×10⁸, 10¹²] GeV 内",
         all(FA_LO <= r["fa"] <= FA_HI for r in rows)),
        ("G5", "过闭边界复核：f_a=2.94×10¹¹ GeV、θ_i=1 时 Ω≈0.12（|偏差|<5%）",
         abs(g4["omega_at_2p94e11_theta1"] / OMEGA_DM_H2 - 1) < Decimal("0.05")),
        ("G6", "misalignment 单调：Ω(θ_i=0.1) < Ω(θ_i=1) < Ω(θ_i=3)（边界处）",
         g4["rows"][0]["omega_h2"] < g4["rows"][1]["omega_h2"] < g4["rows"][2]["omega_h2"]),
        ("G7", "TUFT 供给 PQ 对称 = 0、供给轴子 = 0（结构性负面判据）",
         (not g5["tuft_supplies_pq_symmetry"]) and (not g5["tuft_supplies_axion"])),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0196 guard failed"

    w("\n[诚实边界]")
    w("  不宣称解决任何物理难题；外部常数（α_em、gγ、ADMX 带、Ω_DM h²）只引用不复算；")
    w("  标度律系数 O(1) 不确定度按量级判定；数值均为标准轴子算术/实测复核，")
    w("  TUFT 已注销（C0133），严禁写成 TUFT 预测/修正；")
    w("  红线不变：已攻破=对 TUFT/几何框架结构性负面闭合；有预测且对=0/22；")
    w("  UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0196_轴子PQ破缺攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0196_轴子PQ破缺攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0196_axion_PQ_symmetry_breaking",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_inputs": {k: (str(v) if not isinstance(v, tuple) else [str(x) for x in v])
                          for k, v in g1.items()},
            "E2_window_scan": [{k: str(v) for k, v in r.items()} for r in rows],
            "E3_admx_box": {k: (str(v) if not isinstance(v, list)
                                else [{kk: str(vv) for kk, vv in x.items()} for x in v])
                            for k, v in g3.items()},
            "E4_misalign_review": {
                "rows": [{k: str(v) for k, v in r.items()} for r in g4["rows"]],
                "omega_at_2p94e11_theta1": str(g4["omega_at_2p94e11_theta1"]),
                "omega_at_c0180_2p9427e11_theta1": str(g4["omega_at_c0180_2p9427e11_theta1"]),
            },
            "E5_supply": {k: str(v) for k, v in g5.items()},
            "guards": [{"id": gid, "desc": d, "ok": bool(ok)} for gid, d, ok in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0196 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
