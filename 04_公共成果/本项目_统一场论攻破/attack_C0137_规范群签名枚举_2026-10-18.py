# -*- coding: utf-8 -*-
"""
attack_C0137_规范群签名枚举_2026-10-18.py
独立复算：规范群签名枚举（P12 · 布局双分水岭之一）

定位：布局册（C0135）把 P12 规范群起源与 P01 量子引力并列为最高阻塞力
（各阻塞下游 6 项）。仓内此前对 P12 已做过四条相关判定（C0127：so(1,3)⊥SM；
攻破⑬-O3：已知几何途径不可闭合；attack19/20：CP^m×CP^n 复合唯一性；
并行册 S14-C0136/attack24：Killing 签名 (3,3)、KK 逃逸 n=5、逐圈系数计数），
但**从未枚举过规范代数签名本身**。本册补这一格（与并行册机制互补、不重复）：

  E1 李代数表：A/B/C/D 四族 + 例外代数按公式机器生成（dim/rank）。
  E2 签名枚举：固定「总维数=12、总秩=4」（=SM 的签名），穷举规范代数候选，
     看签名能否唯一锁定 SM。
  E3 时空-内部隔离定量版：so(1,3)（dim 6/rank 2）能否容纳 SM（dim 12/rank 4）。
  E4 反常消除的角色：它约束超荷**赋值**，不锁定**群选择**。
  E5 裁定：规范群起源需一枚唯一化原理（蓝本 C1），几何框架提供者 0 ⇒ 结构性负面。

纯标准库（itertools + Fraction），零外部依赖，退出码 0。

诚实边界：本册裁的是「签名能否唯一确定规范群」，不是「规范群起源」本身已解决；
SM 仍是唯一与观测吻合的候选，但那是实验选择，不是公设推导。
"""
from __future__ import annotations
import itertools
import json
import os

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"


# ---------------------------------------------------------------- E1 李代数表
def lie_table():
    """A_n/B_n/C_n/D_n 四族 + 例外代数，dim/rank 按公式现算。"""
    rows = []
    for n in range(1, 9):
        rows.append(("A_%d  su(%d)" % (n, n + 1), (n + 1) ** 2 - 1, n))
        rows.append(("B_%d  so(%d)" % (n, 2 * n + 1), n * (2 * n + 1), n))
        rows.append(("C_%d  sp(%d)" % (n, n), n * (2 * n + 1), n))
        if n >= 3:                       # D_2=so(4)≅A_1⊕A_1（非单）、D_3≅A_3
            rows.append(("D_%d  so(%d)" % (n, 2 * n), n * (2 * n - 1), n))
    for nm, d, r in (("G_2", 14, 2), ("F_4", 52, 4), ("E_6", 78, 6), ("E_7", 133, 7), ("E_8", 248, 8)):
        rows.append((nm, d, r))
    return rows


# 去重后的**互不同构**单因子（dim ≤ 12 的只有这三个）
SIMPLE_SMALL = [("su(2)", 3, 1), ("su(3)", 8, 2), ("so(5)", 10, 2)]
U1 = ("u(1)", 1, 1)


# ---------------------------------------------------------------- E2 签名枚举
def enumerate_signature(target_dim=12, target_rank=4, max_factors=5):
    """穷举：单因子多重集（可重复）+ k 个 u(1)，使总维数=target_dim、总秩=target_rank。"""
    hits = []
    all_dim12 = []
    for n in range(0, max_factors + 1):
        for combo in itertools.combinations_with_replacement(range(len(SIMPLE_SMALL)), n):
            d = sum(SIMPLE_SMALL[i][1] for i in combo)
            r = sum(SIMPLE_SMALL[i][2] for i in combo)
            if d > target_dim:
                continue
            k = target_dim - d                      # 补 u(1) 个数
            names = tuple(sorted(SIMPLE_SMALL[i][0] for i in combo))
            all_dim12.append((names, k, d, r, r + k))
            if r + k == target_rank:
                hits.append({"simple_factors": list(names), "n_u1": k,
                             "simple_dim": d, "simple_rank": r, "total_rank": r + k})
    # 去重（同构只留一个代表）
    uniq, seen = [], set()
    for h in hits:
        key = (tuple(h["simple_factors"]), h["n_u1"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(h)
    return uniq, all_dim12


# ---------------------------------------------------------------- E3 时空-内部隔离
def containment(dim_outer, rank_outer, dim_inner, rank_inner):
    """子代数必须满足 dim ≤ 外层、rank ≤ 外层。"""
    return {"outer": (dim_outer, rank_outer), "inner": (dim_inner, rank_inner),
            "can_contain": (dim_inner <= dim_outer and rank_inner <= rank_outer),
            "dim_gap": dim_inner - dim_outer, "rank_gap": rank_inner - rank_outer}


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    w("=" * 74)
    w("attack_C0137 · 规范群签名枚举（P12 · 布局双分水岭之一）")
    w("=" * 74)

    # ---- E1
    tbl = lie_table()
    small = [r for r in tbl if r[1] <= 12]
    w("\n[E1] 紧致单李代数表（A/B/C/D + 例外，dim/rank 按公式现算）")
    w("  %-16s %-6s %-5s" % ("代数", "dim", "rank"))
    for nm, d, r in tbl:
        w("  %-16s %-6d %-5d" % (nm, d, r))
    w("  => 单因子中 dim ≤ 12 者：%s" % "、".join("%s(%d)" % (n, d) for n, d, r in small))
    w("     互不同构者：%s（so(5)≅sp(2)、su(2)≅so(3)≅sp(1)）"
      % "、".join(n for n, _, _ in SIMPLE_SMALL))

    # ---- E2
    hits, all12 = enumerate_signature()
    w("\n[E2] 签名枚举：固定（总维数=12，总秩=4）= SM 的签名")
    w("  单因子多重集 + k 个 u(1)，穷举满足 total_dim=12 & total_rank=4 的规范代数：")
    for h in hits:
        w("    %-34s + u(1)^%d   （简单部分 dim=%d rank=%d ⇒ 总秩 %d）"
          % (" ⊕ ".join(h["simple_factors"]) or "(空)", h["n_u1"],
             h["simple_dim"], h["simple_rank"], h["total_rank"]))
    n_hits = len(hits)
    w("  => 满足同一签名的规范代数候选：**%d 个**" % n_hits)
    w("     其中 SM = su(3)⊕su(2)⊕u(1)；其余候选：%s"
      % "；".join("%s ⊕ u(1)^%d" % ("⊕".join(h["simple_factors"]) or "空", h["n_u1"])
                 for h in hits if h["simple_factors"] != ["su(2)", "su(3)"] or h["n_u1"] != 1))
    w("  => （dim, rank）签名**不能唯一锁定** SM：至少 %d 个候选共享 (12, 4)。" % n_hits)

    # 附带：dim=12 的总候选数（不限 rank）
    n12 = len({(tuple(sorted(a)), b) for a, b, d, r, tr in all12})
    w("  附带：总维数 = 12（不限秩）的规范代数候选数 = %d 个。" % n12)

    # ---- E3
    ct = containment(6, 2, 12, 4)
    w("\n[E3] 时空-内部隔离（定量版）")
    w("  so(1,3)：dim=%d rank=%d；SM：dim=%d rank=%d"
      % (ct["outer"][0], ct["outer"][1], ct["inner"][0], ct["inner"][1]))
    w("  子代数必要条件 dim_inner ≤ dim_outer：12 ≤ %d ? %s；rank：4 ≤ %d ? %s"
      % (ct["outer"][0], ct["dim_gap"] <= 0, ct["outer"][1], ct["rank_gap"] <= 0))
    w("  => so(1,3) 可容纳 SM = %s（差 dim %+d / rank %+d）⇒ C0127 的定量复算"
      % (ct["can_contain"], ct["dim_gap"], ct["rank_gap"]))

    # ---- E4
    w("\n[E4] 反常消除的角色（结构判定）")
    w("  立方反常约化给出超荷约束（如最小 SM ⇒ x=±3q、U(1)_em 未破缺 ⇒ q=1/3），")
    w("  它锁定的是**超荷赋值**（Y_Q=1/6 等），不是**群选择**。")
    w("  => E2 的其余候选同样可以做反常分析；反常消除不把签名唯一化。")
    anom_constrains_assignment = True
    anom_fixes_group = False

    # ---- E5
    w("\n[E5] 裁定")
    w("  规范群起源（P12）需要一枚**唯一化原理**（蓝本 C1：群/空间选择必须被公设唯一确定）。")
    w("  本册机器结果：(dim,rank) 签名有 %d 个候选 ⇒ 签名不是唯一化原理；" % n_hits)
    w("  so(1,3)⊅SM 定量成立 ⇒ 时空几何也不是；反常消除只锁赋值不锁群。")
    w("  => 几何框架提供唯一化原理者：**0** ⇒ P12 结构性负面（对 TUFT/几何框架）。")
    w("  诚实边界：SM 仍是唯一与观测吻合的候选，但这是**实验选择**，不是公设推导。")
    w("  姊妹册：并行册 S14-C0136/attack24 用 Killing 签名 (3,3)、KK 逃逸 n=5、逐圈系数计数攻 P01/P12；")
    w("          本册用**规范代数签名枚举**攻 P12，机制互补、数值不复算。")

    w("\n退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0137_规范群签名枚举_2026-10-18_report.txt")
    json_path = os.path.join(BASE, "attack_C0137_规范群签名枚举_2026-10-18.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0137_gauge_signature_enumeration",
            "entries": [
                {"id": "E1", "claim": "紧致单李代数表（A/B/C/D + 例外）按公式生成", "verdict": "PASS",
                 "detail": "单因子 dim≤12 且互不同构：su(2)/su(3)/so(5)"},
                {"id": "E2", "claim": "(dim,rank)=(12,4) 签名枚举 ⇒ 规范群不唯一", "verdict": "PASS",
                 "detail": "候选 %d 个共享签名 (12,4)" % n_hits},
                {"id": "E3", "claim": "so(1,3) ⊅ SM（定量）", "verdict": "PASS",
                 "detail": "dim 12>6、rank 4>2 ⇒ 不可容纳"},
                {"id": "E4", "claim": "反常消除只锁超荷赋值、不锁群选择", "verdict": "STRUCT",
                 "detail": "anom_constrains_assignment=%s anom_fixes_group=%s"
                           % (anom_constrains_assignment, anom_fixes_group)},
                {"id": "E5", "claim": "P12 结构性负面：需唯一化原理（C1），几何提供者 0", "verdict": "PASS",
                 "detail": "签名 %d 候选 + so(1,3)⊥ + 反常不锁群" % n_hits},
            ],
            "lie_table": [{"alg": n, "dim": d, "rank": r} for n, d, r in tbl],
            "simple_small_distinct": [n for n, _, _ in SIMPLE_SMALL],
            "signature_candidates": hits,
            "n_signature_candidates": n_hits,
            "n_dim12_candidates_any_rank": n12,
            "containment": ct,
            "anomaly_role": {"constrains_assignment": anom_constrains_assignment,
                             "fixes_group": anom_fixes_group},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0137 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
