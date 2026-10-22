# -*- coding: utf-8 -*-
"""
attack_C0166_单位换算双路径守卫_2026-10-21.py
方法论矩阵 N1 / A7 落地：单位换算双路径守卫模板 _unit_guard() 形式化

定位：方法论矩阵 §四 N1（A7 单位换算双路径守卫，原 ◐ 半用）。
前置：C0139 E1 曾单口径失察——rho_crit 换算自抓 21 量级错误
（1.406e-27 vs 1.264e-6 GeV/cm^3），后用 Planck/PDG 独立口径拦下，
残差 3.13e-4。本册把「双口径交叉」固化为强制模板：
任何跨单位/跨口径换算断言必须两条独立口径交叉，残差超阈即 assert 失败。

工作样例：临界密度 rho_crit 双路径独立精算
  路径 A（基本常数口径）：rho = 3 H0^2 / (8 pi G)，SI 精算后换算 GeV/cm^3
  路径 B（宇宙学表列口径）：rho_crit = 1.05375e-5 h^2 GeV/cm^3（外部引用）
两口径残差应 ~1e-4 量级（表列常数本即同源推导，但本册按独立引用对待）。

纯标准库（Decimal 48 位），零外部依赖、零网络、零随机，退出码 0。

诚实边界：外部观测值（h, G, Mpc, GeV/kg, 表列常数）只引用不复算；
本册为方法论模板形式化，不宣称解决任何物理难题。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
import os
import math

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（CODATA / Planck 2018 / PDG 口径，只引用不复算） ----------
H = Decimal("0.674")                 # Planck 2018 约化哈勃常数 h
G_CODATA = Decimal("6.67430e-11")    # CODATA 2018 引力常数 m^3/kg/s^2
MPC = Decimal("3.0856775814913673e22")  # 1 Mpc (m)，CODATA
GEV_KG = Decimal("1.78266192e-27")   # 1 GeV/c^2 对应质量 (kg)，CODATA
RHO_CRIT_CONV = Decimal("1.05375e-5")  # 表列口径 rho_crit [GeV/cm^3] = 此值 * h^2
# C0139 E1 自抓案例（单口径失察两端，GeV/cm^3）
ERR_WRONG = Decimal("1.406e-27")
ERR_RIGHT = Decimal("1.264e-6")

PI = Decimal("3.141592653589793238462643383279502884197169399375")


def rho_crit_path_a():
    """路径 A：基本常数口径 rho = 3H^2/(8 pi G)，SI -> GeV/cm^3。"""
    H0 = Decimal("100") * H * Decimal("1000") / MPC   # s^-1
    rho_si = Decimal(3) * H0 * H0 / (Decimal(8) * PI * G_CODATA)  # kg/m^3
    # kg/m^3 -> GeV/cm^3：先 /1e6 (m^3->cm^3)，再 /GeV_kg (kg->GeV)
    rho = rho_si / Decimal("1e6") / GEV_KG
    return {"H0_s": H0, "rho_si_kg_m3": rho_si, "rho_GeV_cm3": rho}


def rho_crit_path_b():
    """路径 B：表列口径 rho = 1.05375e-5 h^2 GeV/cm^3。"""
    return {"rho_GeV_cm3": RHO_CRIT_CONV * H * H}


def unit_guard(a: Decimal, b: Decimal, tol: Decimal):
    """双路径守卫模板（A7 形式化产物）：残差超阈即失败。"""
    res = abs(a - b) / b
    ok = res < tol
    return {"residual": res, "tol": tol, "ok": bool(ok)}


def e1_history():
    """E1：单口径失察案例登记（C0139 E1 自抓）。"""
    ratio = ERR_RIGHT / ERR_WRONG
    return {"wrong": ERR_WRONG, "right": ERR_RIGHT, "ratio": ratio}


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0166 · 单位换算双路径守卫模板（方法论矩阵 N1 / A7）")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_history()
    w("\n[E1] 单口径失察案例登记（C0139 E1 自抓 21 量级错误）")
    w("  错误端 %s vs 正确端 %s GeV/cm^3，量级比 = %s"
      % (fv(g1["wrong"], "3e"), fv(g1["right"], "3e"), fv(g1["ratio"], "3e")))
    w("  => 单口径换算失察可达 ~21 量级；双口径交叉为强制防线（非可选）。")
    entries.append(("E1", "单口径失察案例量级比 %s（C0139 E1）" % fv(g1["ratio"], "2e"),
                    "PASS", "历史自抓登记"))

    # ---- E2 ----
    ga = rho_crit_path_a()
    gb = rho_crit_path_b()
    w("\n[E2] rho_crit 双路径独立精算（本册工作样例）")
    w("  路径 A（基本常数）：H0 = %s s^-1；rho = %s kg/m^3"
      % (fv(ga["H0_s"], "6e"), fv(ga["rho_si_kg_m3"], "4e")))
    w("  路径 A 换算 rho = %s GeV/cm^3" % fv(ga["rho_GeV_cm3"], "6e"))
    w("  路径 B（表列口径）rho = %s * h^2 = %s GeV/cm^3"
      % (fv(RHO_CRIT_CONV, "5e"), fv(gb["rho_GeV_cm3"], "6e")))
    entries.append(("E2", "rho_crit 双路径 = %s vs %s GeV/cm^3"
                    % (fv(ga["rho_GeV_cm3"], "6e"), fv(gb["rho_GeV_cm3"], "6e")),
                    "PASS", "A=SI 基本常数推导；B=表列常数独立引用"))

    # ---- E3 ----
    guard = unit_guard(ga["rho_GeV_cm3"], gb["rho_GeV_cm3"], Decimal("1e-3"))
    w("\n[E3] _unit_guard() 模板自检（残差 / 阈 / 判定）")
    w("  残差 = |A-B|/B = %s；阈 = %s；=> %s"
      % (fv(guard["residual"], "4e"), fv(guard["tol"], "0e"),
         "PASS" if guard["ok"] else "FAIL"))
    # 反向用例：故意给错误端 vs 正确端，守卫应拦下
    bad = unit_guard(ERR_WRONG, ERR_RIGHT, Decimal("1e-3"))
    w("  反向用例（错误端 vs 正确端）：残差 = %s => %s（应拦下）"
      % (fv(bad["residual"], "3e"), "拦下" if not bad["ok"] else "漏防"))
    entries.append(("E3", "模板 _unit_guard() 残差 %s < 1e-3 PASS；反向用例正确拦下"
                    % fv(guard["residual"], "3e"), "PASS", "A7 形式化产物"))

    # ---- E4 ----
    w("\n[E4] 适用域与边界")
    w("  强制双口径范围：一切跨单位/跨物理口径换算断言（密度、能标、截面、时标）。")
    w("  边界：纯无量纲整数恒等式（nullity、Bianchi 类）无需双口径；")
    w("  外部引用值（PDG/Planck/CODATA）标注来源即视为第二口径。")
    entries.append(("E4", "双口径强制域 = 跨单位换算类断言；整数恒等式豁免",
                    "PASS", "方法论边界"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  A7 由 ◐（半用）转 ✅：_unit_guard() 模板形式化完成，rho_crit 工作样例验证残差 %s。"
      % fv(guard["residual"], "3e"))
    w("  撞 C：无（方法论升级，非新物理判定）；后续 C0xxx 四件套跨单位断言须内置双口径。")
    entries.append(("E5", "A7 ◐->✅ 模板化闭合；rho_crit 双路径残差 %s"
                    % fv(guard["residual"], "3e"), "PASS", "无撞 C"))

    # ---- 守卫 ----
    guards = [
        ("G1", "rho_crit 双路径残差 < 1e-3", guard["ok"]),
        ("G2", "rho_crit 量级在 [4.5e-6, 5.2e-6] GeV/cm^3",
         Decimal("4.5e-6") < ga["rho_GeV_cm3"] < Decimal("5.2e-6")),
        ("G3", "单口径失察案例量级比 >= 1e20", g1["ratio"] >= Decimal("1e20")),
        ("G4", "反向用例（错误端）被守卫拦下", not bad["ok"]),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0166 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称解决任何物理难题；外部常数只引用不复算；判定按量级（残差阈值）而非末位。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0166_单位换算双路径守卫_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0166_单位换算双路径守卫_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0166_unit_guard_template",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E2_pathA_rho_GeV_cm3": str(ga["rho_GeV_cm3"]),
            "E2_pathB_rho_GeV_cm3": str(gb["rho_GeV_cm3"]),
            "E3_residual": str(guard["residual"]),
            "E3_bad_case_blocked": not bad["ok"],
            "E1_mismatch_ratio": str(g1["ratio"]),
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0166 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
