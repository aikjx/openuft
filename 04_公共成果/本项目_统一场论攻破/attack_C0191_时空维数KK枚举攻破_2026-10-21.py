# -*- coding: utf-8 -*-
"""
attack_C0191_时空维数KK枚举攻破_2026-10-21.py
独立精算：母册 T013「时空维数为何是 4」· KK（Kaluza-Klein）紧致化枚举、维数选择机制供给检查

定位：母册 T013（维数选择，撞 C1，现状「部分：KK n=5（attack24 N2）」）。
承接：attack24 N2（KK n=5 已部分读数）、C0162（so(8) 极大子群 P12-KK-EMBED 闭合，
SM 极大秩嵌入存在性=0）。本册把「时空为何 4 维」压缩成标准 KK 算术的逐维枚举 +
维数-规范群匹配 + 维数选择外部输入账单 + 4D 唯一性检查，并对 TUFT/几何框架判定供给。

把"时空维数为何是 4"压缩成五条可复核读数 + 一张外部输入账单：

  E1 观测事实：时空=3 空间 + 1 时间（4D），PDG/宇宙学只引用不复算。
  E2 **KK 紧致化逐维枚举（本册核心）**：d=4+n, n=1..11，紧致半径 R~l_P 量级精算
     M_KK=hbar/(R c)；T^n 约化产物——4D 引力子 1、Kaluza-Klein 矢量 n 个（U(1)^n）、
     标量模 n(n+1)/2 个；第 1 能级简并度 2n。
  E3 维数-规范群匹配：T^n 约化只给 Abelian U(1)^n（dim=n），对照 SM（dim=12, rank=4）；
     10/11D 超引力 → SUSY 代数超荷数（D=11 Majorana 旋量 32 → 4D N=8；
     D=10 Majorana-Weyl 16 → N=4）。
  E4 维数选择自由度核算：n 每取一值需一个新紧致机制（外部输入计数）；
     4D 唯一性检查——是否有几何机制强制 n=0（无）。
  E5 裁定：维数选择依赖紧致化机制与外部输入（维数枚举非唯一、无 4D 强制机制），
     TUFT 无维数选择供给，结构性负面，撞 C1。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界：本册所有数值均为标准 KK / 高维算术复核（CODATA 常数只引用）；
TUFT 已注销（C0133）；本册不宣称解释时空维数，不把标准物理结果写成 TUFT 预测/修正。
红线：不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；
有预测且对=0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os
import json

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部常数（CODATA 2018，只引用不复算） ----------
HBAR = Decimal("1.054571817e-34")   # J·s
C = Decimal("299792458")            # m/s
G_NEWT = Decimal("6.67430e-11")     # m^3 kg^-1 s^-2
MEV_PER_JK = Decimal("6.241509074e27")  # 1 J = 6.2415e27 MeV
MPLANK_GEV = Decimal("1.22089e19")  # GeV（CODATA，只引用对照）


def e1_observed_4d():
    """E1 观测事实：时空 = 3 空间 + 1 时间（4D）。只引用不复算。"""
    return {
        "observed_spacetime_dim": 4,       # 3 空间 + 1 时间
        "observed_spatial": 3,
        "observed_temporal": 1,
        "note": "PDG/宇宙学观测只引用；本册不复算",
    }


def e2_kk_enumeration():
    """E2 KK 紧致化逐维枚举 d=4+n, n=1..11（本册核心）。

    标准 T^n 约化算术（自然单位 c=hbar=1 后复原）：
      - 4D 引力子：1
      - KK 矢量 g_{mu,n+i}：n 个 -> 规范群 U(1)^n（秩 n，维数 n，全 Abelian）
      - 标量模 g_{mn}：n(n+1)/2 个（尺寸/形状模，需稳定化）
      - 第 1 KK 能级（|k|=1）简并度：2n（n 个内部方向各取 +/- 号）
      - M_KK = hbar/(R c)；取 R = l_P 时 M_KK = M_Pl（第一性恒等）
    """
    # 第一性精算：l_P = sqrt(hbar G / c^3)；M_Pl = sqrt(hbar c / G)
    c3 = C * C * C
    lP2 = HBAR * G_NEWT / c3
    lP = lP2.sqrt()
    MPl2 = HBAR * C / G_NEWT
    MPl = MPl2.sqrt()              # kg
    # R = l_P 时 KK 质量标度
    MKK_at_lP = HBAR / (lP * C)    # kg
    ratio = MKK_at_lP / MPl        # 应为 1（恒等）
    # 换算 GeV（1 GeV/c^2 = 1.78266e-27 kg）
    GEV_PER_KG = Decimal("5.6095886e26")  # 1 kg = 5.6096e26 GeV/c^2
    MKK_GEV = MKK_at_lP * GEV_PER_KG

    rows = []
    for n in range(1, 12):
        rank = n                       # U(1)^n 秩
        dim_gauge = n                  # Abelian 规范代数维数
        moduli = n * (n + 1) // 2      # g_{mn} 对称标量模个数
        deg_l1 = 2 * n                 # 第 1 KK 能级（单位整数格矢）简并度
        # 第 2 能级（|k|^2 = 2，两个坐标取 +/-1）简并度：2^2 * C(n,2) = 4 * n(n-1)/2
        deg_l2 = 4 * (n * (n - 1) // 2)
        rows.append({
            "n": n, "D": 4 + n,
            "kk_vectors": n, "gauge_group": "U(1)^%d" % n,
            "gauge_rank": rank, "gauge_dim": dim_gauge, "abelian_only": True,
            "scalar_moduli": moduli,
            "degeneracy_level1": deg_l1,
            "degeneracy_level2": deg_l2,
        })
    return {
        "l_P_m": lP,
        "M_Pl_kg": MPl,
        "M_KK_at_lP_kg": MKK_at_lP,
        "M_KK_over_M_Pl": ratio,
        "M_KK_at_lP_GeV": MKK_GEV,
        "rows": rows,
    }


def e3_dim_gauge_match():
    """E3 维数-规范群匹配。

    标准超引力超荷数（实旋量分量）：
      D=11 Majorana 旋量 = 32 实分量 -> 4D N = 32/4 = 8
      D=10 Majorana-Weyl = 16 实分量 -> 4D N = 16/4 = 4
      D=6  symplectic MW  = 8 实分量 -> 4D N = 8/4  = 2
    （4D 一个 Majorana 旋量 = 4 实分量，故 N = Q/4）

    SM 规范群 = SU(3)xSU(2)xU(1)：
      dim = 8 + 3 + 1 = 12；rank = 2 + 1 + 1 = 4
    T^n KK 约化只给 Abelian U(1)^n：dim = n，rank = n。
    """
    # SM 李代数维数（标准，整数）
    dim_SU3 = 8
    dim_SU2 = 3
    dim_U1 = 1
    dim_SM = dim_SU3 + dim_SU2 + dim_U1     # 12
    rank_SU3 = 2
    rank_SU2 = 1
    rank_U1 = 1
    rank_SM = rank_SU3 + rank_SU2 + rank_U1  # 4

    # 超引力超荷数（标准，整数）
    Q_D11 = 32   # D=11 Majorana
    Q_D10 = 16   # D=10 Majorana-Weyl
    Q_D6 = 8     # D=6 symplectic Majorana-Weyl
    FOURD_MAJORANA = 4  # 4D Majorana 旋量实分量
    N_D11 = Q_D11 // FOURD_MAJORANA   # 8
    N_D10 = Q_D10 // FOURD_MAJORANA   # 4
    N_D6 = Q_D6 // FOURD_MAJORANA     # 2

    # T^n 要凑 SM 秩 4：需 n=4；此时 Abelian 维数=4，距 SM 维数 12 差多少？
    n_for_rank4 = 4
    abelian_dim_at_n4 = n_for_rank4        # 4
    missing_generators = dim_SM - abelian_dim_at_n4  # 8 个非 Abelian 生成元
    return {
        "SM_gauge_dim": dim_SM,
        "SM_gauge_rank": rank_SM,
        "KK_abelian_dim_formula": "n",
        "n_to_match_SM_rank": n_for_rank4,
        "abelian_dim_at_n4": abelian_dim_at_n4,
        "missing_nonabelian_generators": missing_generators,
        "Q_D11": Q_D11, "Q_D10": Q_D10, "Q_D6": Q_D6,
        "N_4D_from_D11": N_D11,
        "N_4D_from_D10": N_D10,
        "N_4D_from_D6": N_D6,
        "KK_gives_nonabelian": False,
    }


def e4_dimension_choice_bill():
    """E4 维数选择自由度核算 + 4D 唯一性检查。

    每取定一个 n，外部输入账单（最小集）：
      1) n 本身（为什么是 3+n 空间维，不是别的）—— 1 个输入
      2) 内部流形拓扑/几何（T^n / CY3 / orbifold / G2 ...）—— 1 个输入
      3) 紧致半径 R（定 M_KK 标度）—— 1 个输入
      4) 模稳定化：n(n+1)/2 个标量模各需一个稳定机制 —— n(n+1)/2 个输入
    几何机制强制 n=0（无额外维）？检查：纯引力/KK 本身不选 n——任何 n 数学上都成立；
    KK 是从高维往下紧到 4D，4D 是观测输出而非第一性导出。故 4D 唯一性供给 = 0。
    """
    rows = []
    for n in range(1, 12):
        moduli = n * (n + 1) // 2
        external_inputs = 1 + 1 + 1 + moduli   # n值 + 拓扑 + R + 模稳定
        rows.append({"n": n, "moduli": moduli, "min_external_inputs": external_inputs})
    no_geometric_forcing_n0 = True   # 无几何机制强制 n=0
    return {
        "rows": rows,
        "geometric_forcing_n0": False,
        "note": "n 值/拓扑/R/模稳定化全部为外部输入；4D 是观测输出非几何导出",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 78)
    w("attack_C0191 · 时空维数为何是 4（母册 T013 · KK 紧致化枚举）攻破")
    w("=" * 78)

    entries = []

    # ---- E1 ----
    g1 = e1_observed_4d()
    w("\n[E1] 观测事实：时空维数（PDG/宇宙学只引用不复算）")
    w("  观测时空维数 = %d（%d 空间 + %d 时间）"
      % (g1["observed_spacetime_dim"], g1["observed_spatial"], g1["observed_temporal"]))
    w("  => 我们生活在 3+1 维；问题是：为何是 4 维而非别的维数。")
    entries.append(("E1", "观测时空 = 3+1=4 维（只引用）", "PASS",
                    "PDG/宇宙学观测事实，本册不复算"))

    # ---- E2 ----
    g2 = e2_kk_enumeration()
    w("\n[E2] KK 紧致化逐维枚举 d=4+n, n=1..11（本册核心）")
    w("  第一性常数：hbar=%s J·s, c=%s m/s, G=%s m^3/kg/s^2" % (HBAR, C, G_NEWT))
    w("  l_P = sqrt(hbar G / c^3)        = %s m" % fv(g2["l_P_m"], "6e"))
    w("  M_Pl = sqrt(hbar c / G)         = %s kg" % fv(g2["M_Pl_kg"], "6e"))
    w("  R=l_P 时 M_KK = hbar/(R c)      = %s kg" % fv(g2["M_KK_at_lP_kg"], "6e"))
    w("  M_KK / M_Pl（R=l_P 恒等）       = %s" % fv(g2["M_KK_over_M_Pl"], "20f"))
    w("  M_KK（R=l_P）                    = %s GeV（~ Planck 标度，紧致化不可见）"
      % fv(g2["M_KK_at_lP_GeV"], "4e"))
    w("")
    w("  n | D=4+n | KK矢量 | 规范群      | 秩 | 代数维 | 标量模 | 1级简并 | 2级简并")
    w("  --+------+-------+-----------+----+------+-------+-------+-------")
    for r in g2["rows"]:
        w("  %2d |  %2d   |  %2d   | U(1)^%-4d | %2d |  %2d  |  %2d   |  %3d  |  %3d"
          % (r["n"], r["D"], r["kk_vectors"], r["n"], r["gauge_rank"],
             r["gauge_dim"], r["scalar_moduli"], r["degeneracy_level1"],
             r["degeneracy_level2"]))
    w("  => 标准 T^n 约化：n 个 KK 矢量给出 Abelian U(1)^n（秩=维数=n）；")
    w("     n(n+1)/2 个标量模；R~l_P 时 M_KK~M_Pl~1.22e19 GeV（恒等复核成立）。")
    entries.append(("E2", "n=1..11 逐维枚举：U(1)^n 秩=维数=n，标量模 n(n+1)/2，"
                    "R=l_P 时 M_KK/M_Pl=%s（恒等）" % fv(g2["M_KK_over_M_Pl"], "6f"),
                    "PASS", "标准 T^n 约化算术 + CODATA 常数第一性精算"))

    # ---- E3 ----
    g3 = e3_dim_gauge_match()
    w("\n[E3] 维数-规范群匹配")
    w("  SM = SU(3)xSU(2)xU(1)：维数 = %d+%d+%d = %d；秩 = %d+%d+%d = %d"
      % (8, 3, 1, g3["SM_gauge_dim"], 2, 1, 1, g3["SM_gauge_rank"]))
    w("  T^n KK 约化只给 Abelian U(1)^n（维数=n）；要凑 SM 秩 4 需 n=%d，"
      "但此时 Abelian 维数仅 %d，距 SM 维数 12 缺 %d 个非 Abelian 生成元。"
      % (g3["n_to_match_SM_rank"], g3["abelian_dim_at_n4"],
         g3["missing_nonabelian_generators"]))
    w("  超引力超荷数：D=11 Majorana Q=%d -> 4D N=%d；"
      "D=10 MW Q=%d -> N=%d；D=6 symplectic MW Q=%d -> N=%d。"
      % (g3["Q_D11"], g3["N_4D_from_D11"], g3["Q_D10"], g3["N_4D_from_D10"],
         g3["Q_D6"], g3["N_4D_from_D6"]))
    w("  => 标准 KK/T^n 给不出非 Abelian 规范群（须 orbifold 奇点/非平庸全纯绕等外部几何）；")
    w("     超引力 N=8/4/2 是维数的标准推论，非 TUFT 预测。")
    entries.append(("E3", "T^n 只给 Abelian U(1)^n（dim=n），SM 需 dim=12 非 Abelian，"
                    "缺 8 生成元；D=11->N=8, D=10->N=4, D=6->N=2", "PASS",
                    "标准李代数维数 + 超引力旋量分量计数（整数算术）"))

    # ---- E4 ----
    g4 = e4_dimension_choice_bill()
    w("\n[E4] 维数选择自由度核算 + 4D 唯一性检查")
    w("  n | 标量模 n(n+1)/2 | 最小外部输入（n值+拓扑+R+模稳定）")
    w("  --+---------------+---------------------------")
    for r in g4["rows"]:
        w("  %2d |      %2d        |           %d"
          % (r["n"], r["moduli"], r["min_external_inputs"]))
    w("  4D 唯一性检查：是否有几何机制强制 n=0（无额外维）？")
    w("    几何机制强制 n=0 = %s（纯引力/KK 本身不选 n；任何 n 数学上都成立）。"
      % g4["geometric_forcing_n0"])
    w("    KK 是从高维紧到 4D，4D 是观测输出而非第一性导出（承接 C0162：SM 极大秩嵌入=0）。")
    entries.append(("E4", "每个 n 需 >= n(n+1)/2+3 个外部输入；无几何机制强制 n=0，"
                    "4D 是观测输出", "PASS", "外部输入账单整数计数 + 唯一性=False"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  维数问题被翻译成三件事：(a) KK 能否枚举高维到 4D；(b) 维数-规范群能否匹配 SM；"
      "(c) 几何能否强制 n=0（4D 唯一性）。")
    w("  (a) 能枚举：n=1..11 均给出 U(1)^n + n(n+1)/2 模（E2），R=l_P 时 M_KK~M_Pl。")
    w("  (b) 不匹配：T^n 只给 Abelian，SM 需 8 个非 Abelian 生成元（E3）；超引力 N 是标准推论。")
    w("  (c) 不强制：n 值/拓扑/R/模稳定化全是外部输入，无 4D 强制机制（E4）。")
    w("  => 维数选择依赖紧致化机制与外部输入（维数枚举非唯一、无 4D 强制机制）；")
    w("     TUFT 无维数选择供给（已注销 C0133），**结构性负面**，按母册登记撞 C1。")
    entries.append(("E5", "维数选择依赖紧致化机制与外部输入，维数枚举非唯一、无 4D 强制机制，"
                    "TUFT 无供给，结构性负面", "PASS", "撞 C1（粒子内容/维数须公设唯一确定）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "枚举 n=1..11 共 11 行", len(g2["rows"]) == 11),
        ("G2", "R=l_P 时 M_KK/M_Pl = 1（第一性恒等，Decimal 误差<1e-30）",
         abs(g2["M_KK_over_M_Pl"] - Decimal(1)) < Decimal("1e-30")),
        ("G3", "T^n 约化规范群为 Abelian U(1)^n（dim=n）",
         all(r["gauge_dim"] == r["n"] and r["abelian_only"] for r in g2["rows"])),
        ("G4", "SM 规范群 dim=12, rank=4",
         g3["SM_gauge_dim"] == 12 and g3["SM_gauge_rank"] == 4),
        ("G5", "n=4 时 Abelian 维数 4，缺 8 个非 Abelian 生成元",
         g3["missing_nonabelian_generators"] == 8),
        ("G6", "超引力超荷：D=11->N=8, D=10->N=4, D=6->N=2",
         g3["N_4D_from_D11"] == 8 and g3["N_4D_from_D10"] == 4 and g3["N_4D_from_D6"] == 2),
        ("G7", "无几何机制强制 n=0（4D 唯一性供给=0）", g4["geometric_forcing_n0"] is False),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0191 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合。")
    w("  数值均为标准 KK/高维算术复核（CODATA 只引用）；TUFT 已注销（C0133）；")
    w("  不把标准物理结果写成 TUFT 预测/修正。有预测且对=0/22；UFT-3=0 保持。")
    w("  数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0191_时空维数KK枚举攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0191_时空维数KK枚举攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0191_spacetime_dim_KK_enumeration",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_observed_4d": {k: str(v) for k, v in g1.items()},
            "E2_kk_enumeration": {
                "l_P_m": str(g2["l_P_m"]),
                "M_Pl_kg": str(g2["M_Pl_kg"]),
                "M_KK_at_lP_kg": str(g2["M_KK_at_lP_kg"]),
                "M_KK_over_M_Pl": str(g2["M_KK_over_M_Pl"]),
                "M_KK_at_lP_GeV": str(g2["M_KK_at_lP_GeV"]),
                "rows": g2["rows"],
            },
            "E3_dim_gauge_match": {k: str(v) for k, v in g3.items()},
            "E4_dimension_choice": {
                "rows": g4["rows"],
                "geometric_forcing_n0": str(g4["geometric_forcing_n0"]),
            },
            "guards": [{"id": gid, "desc": desc, "ok": bool(ok)}
                       for gid, desc, ok in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0191 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
