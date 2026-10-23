# -*- coding: utf-8 -*-
"""
attack_C0180_轴子misalignment丰度攻破_2026-10-21.py
独立精算：轴子暗物质 misalignment 机制与丰度（母册 T410，行 548；PQ 对称破缺）

定位：母册 T410（本轮新立编号，不与 T021/T029 重复）；衔接 C0138（强 CP 问题，
f_a 窗口 4×10⁸–10¹² GeV，T029 ◐）。本册只做标准宇宙学算术与实测复核：
PQ 对称破缺后轴子场初值角 θ_i 冻结，质量项开启后场振荡贡献暗物质丰度。

把"轴子 misalignment 丰度"压缩成五条可复核读数：

  E1 机制事实与外部输入：Ω_DM h²=0.12（Planck/PDG，只引用）；f_a 窗口 4×10⁸–10¹² GeV
     （承接 C0138）；标度律 Ω_a h² ≈ (θ_i²/2)·(f_a/10¹² GeV)^(7/6)（量级公式，系数取 1）。
  E2 **f_a 扫点（本册核心）**：5×10⁹ / 10¹⁰ / 10¹¹ / 10¹² GeV 四点 × θ_i=1 与
     θ_i=√(2/3)（θ_i²=2/3，Fraction 精确）两口径，Decimal 48 位核算 Ω_a h²。
  E3 命中/过闭对照：与实测 0.12 对照——哪些 (f_a, θ_i) 命中、何处过闭；
     求 f_a 过闭边界（θ_i=1）与各扫点命中所需 θ_i。
  E4 精调量化：f_a=10¹² GeV 命中需 θ_i=√0.24；与 O(1) 自然初值的过闭倍数。
  E5 裁定：轴子暗物质依赖 PQ 对称破缺与 θ 真空（非微扰 QCD 拓扑），TUFT 无 PQ
     机制、无 θ 参数供给 ⇒ 结构性负面，按母册登记撞 C1/C2。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖，退出码 0。

诚实边界：标度律系数携带 O(1) 不确定度（QCD 热历史、非谐项），本册按量级（倍）
判定；数值均为标准宇宙学算术或实测复核，TUFT 已注销（C0133），本册不把标准物理
结果写成 TUFT 预测/修正。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（实测/承接，只引用） ----------
OMEGA_DM_H2 = Decimal("0.12")          # Planck/PDG 实测暗物质丰度
FA_REF = Decimal("1000000000000")      # 10^12 GeV 参考标度
FA_LO = Decimal("400000000")            # f_a 窗口下界 4×10^8 GeV（承接 C0138）
FA_HI = Decimal("1000000000000")        # f_a 窗口上界 10^12 GeV（承接 C0138）
# 扫点（全部落在窗口 [4×10^8, 10^12] 内）
FA_SCAN = [
    Decimal("5000000000"),              # 5×10^9 GeV
    Decimal("10000000000"),             # 10^10 GeV
    Decimal("100000000000"),           # 10^11 GeV
    Decimal("1000000000000"),          # 10^12 GeV
]
# θ_i² 两口径：θ_i=1 ⇒ 1；θ_i=√(2/3) ⇒ 2/3（Fraction 精确）
TH2_CASES = [("theta_i=1", Decimal(1)),
             # θ_i=√(2/3) ⇒ θ_i²=2/3：先 Fraction 锁定有理数，再 Decimal(分子/分母)
             ("theta_i=sqrt(2/3)", Decimal(Fraction(2, 3).numerator) / Decimal(Fraction(2, 3).denominator))]


def misalignment_omega(th2: Decimal, fa: Decimal) -> Decimal:
    """Ω_a h² = (θ_i²/2)·(f_a/10^12 GeV)^(7/6)，系数取 1（量级公式）。"""
    x = fa / FA_REF
    # (x)^(7/6) = exp((7/6)·ln x)
    return (th2 / 2) * ((Decimal(7) / Decimal(6) * x.ln()).exp())


def required_theta2(fa: Decimal) -> Decimal:
    """命中实测 Ω_DM h²=0.12 所需 θ_i²：θ_i² = 2·0.12/(f_a/10^12)^(7/6)。"""
    x = fa / FA_REF
    return (2 * OMEGA_DM_H2) / ((Decimal(7) / Decimal(6) * x.ln()).exp())


def e1_inputs():
    """机制事实与外部输入。"""
    return {
        "omega_dm_h2": OMEGA_DM_H2,
        "fa_window_GeV": (FA_LO, FA_HI),
        "formula": "Omega_a h^2 = (theta_i^2/2) * (f_a/1e12 GeV)^(7/6), 系数=1",
        "mechanism": "PQ 对称破缺 -> θ_i 冻结 -> QCD 相变质量项开启 -> 场振荡 -> DM",
    }


def e2_scan():
    """f_a 扫点 × θ_i 两口径（本册核心）。"""
    rows = []
    for fa in FA_SCAN:
        row = {"fa": fa}
        for name, th2 in TH2_CASES:
            row[name] = misalignment_omega(th2, fa)
        rows.append(row)
    return rows


def e3_hit_boundary(rows):
    """与实测 0.12 对照：命中判定、过闭边界、各扫点命中所需 θ_i。"""
    out = []
    for row in rows:
        fa = row["fa"]
        th2_req = required_theta2(fa)
        out.append({
            "fa": fa,
            "th2_req": th2_req,
            "th_req": th2_req.sqrt(),
            "feasible": th2_req <= Decimal("9.87"),  # θ_i ≤ π（θ² ≤ π²≈9.87）
            "overclosure_at_theta1": row["theta_i=1"] > OMEGA_DM_H2,
        })
    # θ_i=1 时 f_a 过闭边界：0.5·x^(7/6)=0.12 ⇒ x=(0.24)^(6/7)
    x_boundary = ((Decimal(6) / Decimal(7)) * (Decimal(2) * OMEGA_DM_H2).ln()).exp()
    fa_boundary = x_boundary * FA_REF
    return {"hit_solutions": out,
            "fa_overclosure_boundary_theta1": fa_boundary,
            "x_boundary": x_boundary}


def e4_tuning():
    """精调量化：f_a=10^12 GeV 处自然初值 vs 命中所需。"""
    omega_natural = misalignment_omega(Decimal(1), FA_HI)   # θ_i=1, f_a=1e12
    th2_needed = required_theta2(FA_HI)                     # =0.24
    return {
        "omega_at_1e12_theta1": omega_natural,             # 0.5
        "over_factor": omega_natural / OMEGA_DM_H2,         # 0.5/0.12
        "th2_needed": th2_needed,                           # 0.24
        "th_needed": th2_needed.sqrt(),                    # √0.24
        "volume_fraction": th2_needed / Decimal(1),        # θ_i²∈[0,1] 自然区间命中占比
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="4e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0180 · 轴子暗物质 misalignment 机制与丰度（母册 T410 · PQ 对称破缺）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_inputs()
    w("\n[E1] 机制事实与外部输入（实测/承接 C0138，只引用不复算）")
    w("  实测暗物质丰度 Ω_DM h² = %s（Planck/PDG）" % fv(OMEGA_DM_H2, "2f"))
    w("  f_a 窗口 = [%s, %s] GeV（承接 C0138 T029 ◐）"
      % (fv(FA_LO, "2e"), fv(FA_HI, "2e")))
    w("  标度律：Ω_a h² = (θ_i²/2)·(f_a/10¹² GeV)^(7/6)（量级公式，系数取 1；")
    w("  系数携带 O(1) 不确定度——QCD 热历史/非谐项，本册按量级（倍）判定）")
    w("  机制：PQ 对称破缺 → θ_i 冻结 → QCD 相变质量项开启 → 场振荡 → DM。")
    entries.append(("E1", "Ω_DM h²=0.12 实测；f_a 窗口 4×10⁸–10¹² GeV（承接 C0138）；"
                    "标度律 Ω_a h²=(θ_i²/2)·(f_a/10¹²)^(7/6)", "PASS",
                    "实测/承接值只引用；系数 O(1) 不确定度按量级判定"))

    # ---- E2 ----
    rows = e2_scan()
    w("\n[E2] f_a 扫点 × θ_i 两口径（本册核心，Decimal 48 位）")
    w("  %-14s %-16s %-16s %-14s" % ("f_a (GeV)", "Ω_a h² (θ_i=1)",
                                        "Ω_a h² (θ_i=√(2/3))", "vs 实测 0.12"))
    for row in rows:
        om1 = row["theta_i=1"]
        om2 = row["theta_i=sqrt(2/3)"]
        ratio = om1 / OMEGA_DM_H2
        tag = ("过闭 %.2fx" % ratio) if om1 > OMEGA_DM_H2 else ("欠额 %.2f%%" % (ratio * 100))
        w("  %-14s %-16s %-16s %-14s"
          % (fv(row["fa"], "2e"), fv(om1, "4e"), fv(om2, "4e"), tag))
    entries.append(("E2", "扫点表：f_a=10¹² GeV θ_i=1 得 Ω=0.500000（过闭 4.17x）；"
                    "f_a=10¹¹ GeV θ_i=1 得 Ω=0.034065（欠额 28.39%）；更低 f_a 深欠额",
                    "PASS", "Decimal 48 位精算；θ_i²=2/3 用 Fraction 精确"))

    # ---- E3 ----
    g3 = e3_hit_boundary(rows)
    w("\n[E3] 命中/过闭对照（与实测 Ω_DM h²=0.12）")
    for s in g3["hit_solutions"]:
        feas = "可行(θ≤π)" if s["feasible"] else "不可行(θ>π)"
        w("  f_a=%s：命中所需 θ_i²=%s（θ_i=%s）——%s；θ_i=1 时 %s"
          % (fv(s["fa"], "2e"), fv(s["th2_req"], "4e"), fv(s["th_req"], "4f"), feas,
             "过闭" if s["overclosure_at_theta1"] else "未过闭"))
    w("  θ_i=1 时 f_a 过闭边界：x=(0.24)^(6/7)=%s ⇒ f_a ≈ %s GeV"
      % (fv(g3["x_boundary"], "6f"), fv(g3["fa_overclosure_boundary_theta1"], "4e")))
    w("  （即 θ_i=O(1) 自然初值下，f_a ≳ 3×10¹¹ GeV 量级即过闭宇宙）")
    entries.append(("E3", "过闭边界 f_a≈2.9431×10¹¹ GeV（θ_i=1）；f_a=10¹¹ 命中需 θ_i≈1.8769；"
                    "f_a≤10¹⁰ 命中需 θ_i>π 不可行", "PASS",
                    "解方程 θ_i²=2·0.12/(f_a/10¹²)^(7/6)"))

    # ---- E4 ----
    g4 = e4_tuning()
    w("\n[E4] 精调量化（f_a=10¹² GeV）")
    w("  θ_i=1 自然初值：Ω_a h²=%s（过闭实测 %s 倍）"
      % (fv(g4["omega_at_1e12_theta1"], "4f"), fv(g4["over_factor"], "4f")))
    w("  命中实测需：θ_i²=%s（=0.24），θ_i=√0.24=%s"
      % (fv(g4["th2_needed"], "4f"), fv(g4["th_needed"], "6f")))
    w("  自然区间 θ_i²∈[0,1] 内命中占比 = %s（即约 24%% 体积；O(1) 初值需压到 ~0.49）"
      % fv(g4["volume_fraction"], "4f"))
    entries.append(("E4", "f_a=10¹² GeV 命中需 θ_i=√0.24≈0.489898；O(1) 初值过闭 4.1667 倍；"
                    "自然参数体积命中占比 24%", "PASS", "0.5/0.12=4.1667 倍精压"))

    # ---- E5 ----
    w("\n[E5] 裁定（对 TUFT/几何框架）")
    w("  轴子暗物质丰度的两个供给源：(a) PQ 对称破缺——新全局 U(1)_PQ 与新 VEV 标度 f_a；")
    w("  (b) θ 真空——非微扰 QCD 拓扑瞬子效应给轴子质量与势。")
    w("  TUFT/几何框架：无 PQ 对称机制、无 θ 参数供给（承接 C0138：PQ→C1、新 VEV f_a→C2）。")
    w("  本册 E2–E4 的 Ω 数值全是标准 misalignment 算术，与 TUFT 无关——TUFT 不供给")
    w("  f_a、不供给 θ_i、不供给 PQ 破缺标度 ⇒ **结构性负面**，按母册 T410 登记撞 C1/C2。")
    entries.append(("E5", "轴子 DM 依赖 PQ 破缺（新 U(1)、新 VEV f_a）+ θ 真空（QCD 拓扑）；"
                    "TUFT 无 PQ 机制/无 θ 参数供给 ⇒ 结构性负面，撞 C1/C2", "PASS",
                    "母册 T410 登记；衔接 C0138（T021 ✅ / T029 ◐）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "f_a=10¹² GeV 且 θ_i=1 时 Ω_a h² = 0.5（过闭实测 0.12）",
         rows[3]["theta_i=1"] == Decimal("0.5")),
        ("G2", "f_a=10¹¹ GeV 且 θ_i=1 时 Ω_a h² < 0.12（欠额）",
         rows[2]["theta_i=1"] < OMEGA_DM_H2),
        ("G3", "f_a=10¹² GeV 命中所需 θ_i² = 0.24（θ_i=√0.24）",
         g4["th2_needed"] == Decimal("0.24")),
        ("G4", "θ_i=1 过闭边界 f_a ∈ (10¹¹, 10¹²) GeV",
         Decimal("100000000000") < g3["fa_overclosure_boundary_theta1"] < FA_HI),
        ("G5", "标度律单调：Ω(10¹²) > Ω(10¹¹) > Ω(10¹⁰) > Ω(5×10⁹)（θ_i=1）",
         rows[3]["theta_i=1"] > rows[2]["theta_i=1"] > rows[1]["theta_i=1"] > rows[0]["theta_i=1"]),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0180 guard failed"

    w("\n[诚实边界]")
    w("  不宣称解决任何物理难题；标度律系数 O(1) 不确定度按量级判定；")
    w("  数值均为标准 misalignment 算术/实测复核，TUFT 已注销（C0133）；")
    w("  红线不变：已攻破=对 TUFT/几何框架结构性负面闭合；有预测且对=0/22；UFT-3=0 保持；")
    w("  数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0180_轴子misalignment丰度攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0180_轴子misalignment丰度攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0180_axion_misalignment_abundance",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_inputs": {k: (str(v) if not isinstance(v, tuple) else [str(x) for x in v])
                          for k, v in g1.items()},
            "E2_scan": [{k: str(v) for k, v in row.items()} for row in rows],
            "E3_hit_boundary": {
                "hit_solutions": [{k: str(v) for k, v in s.items()}
                                  for s in g3["hit_solutions"]],
                "fa_overclosure_boundary_theta1": str(g3["fa_overclosure_boundary_theta1"]),
                "x_boundary": str(g3["x_boundary"]),
            },
            "E4_tuning": {k: str(v) for k, v in g4.items()},
            "guards": [{"id": gid, "desc": d, "ok": bool(ok)} for gid, d, ok in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0180 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
