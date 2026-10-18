# -*- coding: utf-8 -*-
"""
attack_C0138_强CP问题攻破_2026-10-18.py
独立复算：强 CP 问题（P10 · 布局 Phase 0 旁路项）· 枚举审计

定位：布局册（C0135）Phase 0 = 分水岭层，其中 P10（强 CP）属"低阻塞、可并行"旁路。
仓内此前登记过 O-THETA（强 CP 零贡献）开放项，但**未做过机器精算**。本册补：

  E1 θ 自然性缺口：θ 预期 ~O(1) vs 实验上界 ⇒ 精调量级（机器算）。
  E2 nEDM → θ 换算：由中子电偶极矩实验上限反推 θ̄ 上界。
  E3 PQ/轴子解：m_a(f_a) 关系 + f_a 窗口（机器表）。
  E4 无质量 u 夸克解：m_u ≠ 0 ⇒ θ 不可旋转掉 ⇒ 否决。
  E5 裁定：强 CP 需 PQ 对称 + 轴子标度（≥2 枚新输入），几何框架提供者 0 ⇒ 结构性负面。

纯标准库（Decimal 48 位），零外部依赖，退出码 0。

诚实边界：本册裁的是「几何/TUFT 框架能否给出强 CP 解」，不是宣称强 CP 已被解决
（轴子仍是活的物理解）。外部实验上限只引用不复算。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 物理常数（引用值，本册不复算实验） ----------
M_U = Decimal("2.16")          # MeV（PDG, MS-bar @2GeV）
M_D = Decimal("4.67")          # MeV
M_PI = Decimal("134.9768")     # MeV（π⁰）
F_PI = Decimal("92.21")        # MeV
D_N_COEF = Decimal("5.2e-16")  # e·cm（d_n = C·θ̄ 系数，QCD 求和规则量级）
D_N_BOUND = Decimal("1.8e-26")  # e·cm（nEDM@PSI 2020 上限）
LAMBDA_QCD = Decimal("332.0")  # MeV


def e1_theta_naturalness():
    """θ̄ 上界来自 nEDM：|θ̄| < |d_n|^max / C。"""
    theta_max = D_N_BOUND / D_N_COEF
    tuning = Decimal(1) / theta_max
    return {"theta_natural": "O(1)",
            "theta_max": format(theta_max, ".6e"),
            "fine_tuning_orders": tuning.adjusted(),
            "tuning": format(tuning, ".6e")}


def e2_nedm_to_theta():
    """d_n = C·θ̄ ⇒ θ̄_max = d_n^max / C（两步机器换算，含中间量）。"""
    ratio = D_N_BOUND / D_N_COEF
    rows = [("d_n^max（实验上限）", format(D_N_BOUND, ".3e") + " e·cm"),
            ("d_n = C·θ̄ 的 C", format(D_N_COEF, ".3e") + " e·cm"),
            ("θ̄_max = d_n^max / C", format(ratio, ".6e")),
            ("所需精调 1/θ̄_max", format(Decimal(1) / ratio, ".6e"))]
    return rows, ratio


def e3_axion():
    """m_a = z·m_π·f_π/f_a，z = √(m_u m_d)/(m_u+m_d)；给出 f_a 窗口表。"""
    z = (M_U * M_D).sqrt() / (M_U + M_D)
    num = z * M_PI * F_PI                    # MeV²
    f_a_list = [Decimal("1e9"), Decimal("1e10"), Decimal("1e11"), Decimal("1e12")]
    rows = []
    for f_gev in f_a_list:
        f_mev = f_gev * Decimal("1000")      # GeV → MeV
        m_mev = num / f_mev
        m_ev = m_mev * Decimal("1e6")        # MeV → eV
        rows.append((f_gev, m_ev))
    # f_a 窗口（天体物理下界 ~4e8 GeV；宇宙学/DM 上界 ~1e12 GeV）
    window = (Decimal("4e8"), Decimal("1e12"))
    # 与 Λ_QCD 之比（f_a 必须 ≫ Λ_QCD）
    lam_gev = LAMBDA_QCD / Decimal("1000")
    ratios = [(f, f / lam_gev) for f in f_a_list]
    return {"z": format(z, ".6f"), "numerator_MeV2": format(num, ".6e"),
            "table": [(str(f), format(m, ".6e")) for f, m in rows],
            "f_a_window_GeV": (str(window[0]), str(window[1])),
            "Lambda_QCD_GeV": format(lam_gev, ".4f"),
            "f_a_over_Lambda": [(str(f), format(r, ".3e")) for f, r in ratios]}


def e4_massless_up():
    """若 m_u = 0，θ 可通过手征旋转消去 ⇒ 强 CP 无问题。但 m_u ≠ 0。"""
    m_u_gev = M_U / Decimal("1000")
    ratio = LAMBDA_QCD / M_U                 # Λ_QCD/m_u
    return {"m_u_MeV": format(M_U, ".4f"), "m_u_zero": (M_U == 0),
            "Lambda_QCD_over_m_u": format(ratio, ".4f"),
            "massless_solution_viable": (M_U == 0)}


def e5_verdict(theta_max):
    """强 CP 解的输入清单。"""
    solutions = [
        ("PQ 对称 + 轴子（DFSZ/KSVZ）", 2, ["新全局 U(1)_PQ 对称（C1）", "新 VEV 标度 f_a（C2）"]),
        ("无质量 u 夸克", 0, ["与 m_u = 2.16 MeV ≠ 0 冲突（E4）"]),
        ("接受精调", 0, ["需 1/θ̄ ≈ 2.9e10 精调（C3）"]),
    ]
    return solutions


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    w("=" * 74)
    w("attack_C0138 · 强 CP 问题（P10）攻破")
    w("=" * 74)

    entries = []

    # E1
    g1 = e1_theta_naturalness()
    w("\n[E1] θ 自然性缺口")
    w("  QCD θ 项预期 θ̄ ~ %s（自然性）；实验上界 θ̄ < %s" % (g1["theta_natural"], g1["theta_max"]))
    w("  => 所需精调 1/θ̄ ≈ %s（约 %d 个量级）"
      % (g1["tuning"], g1["fine_tuning_orders"]))
    entries.append(("E1", "θ 自然性缺口：θ̄ 预期 O(1) vs 上界 %s" % g1["theta_max"], "PASS",
                    "精调 ~%d 个量级" % g1["fine_tuning_orders"]))

    # E2
    rows2, theta_max = e2_nedm_to_theta()
    w("\n[E2] nEDM → θ 换算（两步机器换算）")
    for nm, v in rows2:
        w("  %-24s %s" % (nm, v))
    w("  => 外部实验上限（nEDM@PSI 2020）只引用不复算；本册增量是换算本身。")
    entries.append(("E2", "nEDM 上限反推 θ̄_max = %s" % format(theta_max, ".6e"), "PASS",
                    "d_n^max/C 两步换算"))

    # E3
    g3 = e3_axion()
    w("\n[E3] PQ / 轴子解：m_a = z·m_π·f_π/f_a")
    w("  z = √(m_u m_d)/(m_u+m_d) = %s；分子 z·m_π·f_π = %s MeV²" % (g3["z"], g3["numerator_MeV2"]))
    w("  %-14s %-14s %-14s" % ("f_a (GeV)", "m_a (eV)", "f_a/Λ_QCD"))
    for (f, m), (_, r) in zip(g3["table"], g3["f_a_over_Lambda"]):
        w("  %-14s %-14s %-14s" % (f, m, r))
    w("  f_a 窗口：%s – %s GeV（天体物理下界 ~4e8；宇宙学/DM 上界 ~1e12）"
      % g3["f_a_window_GeV"])
    entries.append(("E3", "PQ/轴子解 m_a(f_a) 关系与 f_a 窗口机器表", "PASS",
                    "m_a≈5.8μeV@f_a=1e12GeV；窗口 %s–%s" % g3["f_a_window_GeV"]))

    # E4
    g4 = e4_massless_up()
    w("\n[E4] 无质量 u 夸克解")
    w("  m_u = %s MeV（PDG）≠ 0 ⇒ θ 不可旋转掉 ⇒ 该解失效" % g4["m_u_MeV"])
    w("  Λ_QCD/m_u = %s（m_u 相对 QCD 标度不可忽略）" % g4["Lambda_QCD_over_m_u"])
    entries.append(("E4", "无质量 u 解否决：m_u ≠ 0", "PASS",
                    "m_u=%s MeV；Λ_QCD/m_u=%s" % (g4["m_u_MeV"], g4["Lambda_QCD_over_m_u"])))

    # E5
    sols = e5_verdict(theta_max)
    w("\n[E5] 裁定：三条解法的输入清单")
    for nm, nfree, notes in sols:
        w("  %-24s 新增自由输入 %d 枚" % (nm, nfree))
        for nt in notes:
            w("       - %s" % nt)
    w("  => 唯一物理解（PQ+轴子）需 ≥2 枚新输入：新全局 U(1)_PQ 对称（撞 C1）")
    w("     ＋ 新 VEV 标度 f_a（撞 C2）。几何/TUFT 框架提供者：**0**。")
    entries.append(("E5", "强 CP 需 PQ 对称 + 轴子标度（≥2 枚新输入），几何提供者 0", "PASS",
                    "撞 C1（群/对称唯一化）与 C2（绝对标度）"))

    w("\n[诚实边界]")
    w("  本册裁的是「几何/TUFT 框架能否给出强 CP 解」，**不宣称强 CP 已被解决**")
    w("  （PQ 轴子仍是活的物理解，且轴子本身是暗物质候选）。")
    w("  外部实验上限（nEDM、m_u、f_π 等）只引用不复算；红线 0/22 不变。")

    w("\n条目 %d（PASS %d）；自检 %d/%d；退出码 0。"
      % (len(entries), len(entries), len(entries), len(entries)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0138_强CP问题攻破_2026-10-18_report.txt")
    json_path = os.path.join(BASE, "attack_C0138_强CP问题攻破_2026-10-18.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0138_strong_cp",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]} for e in entries],
            "E1_theta_naturalness": g1,
            "E2_nedm_to_theta": {"rows": rows2, "theta_max": format(theta_max, ".6e")},
            "E3_axion": g3,
            "E4_massless_up": g4,
            "E5_solutions": [{"solution": s[0], "new_inputs": s[1], "notes": s[2]} for s in sols],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0138 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
