# -*- coding: utf-8 -*-
"""
attack_C0162_so8极大子群P12闭合_2026-10-21.py
方法论矩阵 N2 路径（极大子群分类）闭合 attack24 B07 的 P12-KK-EMBED 开放项。

定位：
  attack24 B06：KK 逃逸最小额外维 n=5（so(1,8)：dim36 rank4；紧致部 so(8)：dim28 rank4），
    按「维数>=12 且 秩>=4」四重必要条件判 "可容纳 SM: YES"——但那只是必要条件。
  attack24 B07 [BOUNDARY]：so(8) 是否含 su(3)+su(2)+u(1) 的**极大秩子代数**需完整极大子群
    分类，本册不代判定（登记为 P12-KK-EMBED 开放项）。
  方法论矩阵 B9 / N2：机器枚举 so(8) 的秩-4 子代数（Borel-de Siebenthal 口径），闭合该开放项。
  C0137 E2：固定签名 (dim=12,rank=4) 有 3 个互不同构代数共享——su3⊕su2⊕u1、so5⊕u1²、su2⁴；
    本册在 so(8) 根系统内实算「SM 那一支 su3⊕su2⊕u1 能否极大秩嵌入」。

本册纯代数（不碰物理数值）：
  E1 so(8)/KK 方案事实（attack24 B05/B06/B07 引用不复算）。
  E2 D4 根系统精算 + 极大秩子代数候选枚举（本册核心）：
     - 根系统 24 根 ±e_i±e_j、秩 4、生成元 28；Cartan/根内积 Fraction 精确。
     - 枚举 A2 子根系统（su3，6 根两两 120°）。
     - 对每个 A2 枚举与其**正交**的 A1（su2，±γ）。
     - 枚举已知极大秩候选：A3×u(1)=so(6)×so(2)、A1^4=so(4)×so(4)。
  E3 与 attack24 P12-KK-EMBED 开放项闭合对照。
  E4 方法论 N2 落位 + C0137 衔接。
  E5 按实算裁定。

纯标准库（整数向量 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。

诚实边界：本册只做李代数根系统的纯代数嵌入判定，不宣称解决规范群起源；
外部 attack24/C0137 数值只引用不复算。
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations
import os

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"


# ---------- D4 根系统构造 ----------
def build_d4_roots():
    """so(8)=D4 根系统：±e_i ± e_j，1<=i<j<=4，整数 4 向量。"""
    roots = []
    for i in range(4):
        for j in range(i + 1, 4):
            for si in (1, -1):
                for sj in (1, -1):
                    r = [0, 0, 0, 0]
                    r[i] = si
                    r[j] = sj
                    roots.append(tuple(r))
    return roots


def dot(a, b):
    return sum(Fraction(x) * Fraction(y) for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def neg(a):
    return tuple(-x for x in a)


def build_a2_subsystems(roots, rootset):
    """枚举 A2 子根系统：正根 {a,b,a+b} 满足 a·b=-1、|a|²=|b|²=2、a+b 是根。
    返回去重后的 A2 集合列表，每个为 6 根 frozenset。"""
    a2_list = []
    seen = set()
    for a, b in combinations(roots, 2):
        if a == neg(b):
            continue
        if dot(a, b) != Fraction(-1):
            continue
        if norm2(a) != 2 or norm2(b) != 2:
            continue
        s = tuple(x + y for x, y in zip(a, b))
        if s not in rootset:
            continue  # 不闭合，非 A2
        six = frozenset({a, neg(a), b, neg(b), s, neg(s)})
        if six in seen:
            continue
        seen.add(six)
        a2_list.append({"positive": (a, b, s), "roots": six})
    return a2_list


def find_orthogonal_a1(a2, roots):
    """在 roots 中找与 A2 全部 6 根正交的根 γ（则 ±γ 成 A1）。返回 γ 列表。"""
    a, b = a2["positive"][0], a2["positive"][1]
    out = []
    for g in roots:
        if g in a2["roots"]:
            continue
        if dot(g, a) == 0 and dot(g, b) == 0:
            out.append(g)
    return out


def classify():
    roots = build_d4_roots()
    rootset = set(roots)

    n_roots = len(roots)
    rank = 4
    dim = n_roots + rank  # 24 + 4 = 28 = so(8)

    # ---- 根长核验（D4 全根同长 = 2）----
    lengths = {norm2(r) for r in roots}

    # ---- A2 枚举 ----
    a2_list = build_a2_subsystems(roots, rootset)
    n_a2 = len(a2_list)

    # 每个 A2 的正交 A1
    a2_with_orth_a1 = []
    for a2 in a2_list:
        orth = find_orthogonal_a1(a2, roots)
        if orth:
            a2_with_orth_a1.append({"a2": a2, "orth_gamma": orth})
    n_a2_orth_a1 = len(a2_with_orth_a1)

    # ---- 极大秩子代数候选枚举 ----
    # (1) A3 块：落在某 3 指标子集内的 12 根 = A3 = so(6)；补方向 e_4 = u(1) -> so(6)x so(2)
    a3_blocks = []
    for idx in combinations(range(4), 3):
        block = [r for r in roots if all(r[k] == 0 for k in range(4) if k not in idx)]
        if len(block) == 12:
            # 块内是否含 A2？块内 A2 = A3 中的 A2 子系统
            blk_set = set(block)
            inner_a2 = [a2 for a2 in a2_list if a2["roots"].issubset(blk_set)]
            a3_blocks.append({"idx": idx, "n_roots": len(block), "n_inner_a2": len(inner_a2)})

    # (2) A1^4：找 4 个两两正交的根对（每对 ±γ），8 根 = so(4)x so(4)
    # 直接枚举：取 4 个两两正交、长度2 的根（正交 A1 链）
    orth_quads = []
    for qu in combinations([r for r in roots], 4):
        ok = all(dot(qu[i], qu[j]) == 0 for i in range(4) for j in range(i + 1, 4))
        # 且不成对（qu 与 -qu 不共选）
        no_pair = all(neg(qu[i]) != qu[j] for i in range(4) for j in range(i + 1, 4))
        if ok and no_pair:
            orth_quads.append(qu)
    n_a1_4 = len(orth_quads)

    # ---- SM 代数账目 ----
    su3_dim, su3_rank = 8, 2
    su2_dim, su2_rank = 3, 1
    u1_dim, u1_rank = 1, 1
    sm_dim = su3_dim + su2_dim + u1_dim
    sm_rank = su3_rank + su2_rank + u1_rank

    # ---- 核心判定 ----
    # 极大秩嵌入 = 存在 A2(su3) 且存在与其正交的 A1(su2)，余下 1 秩方向给 u(1)
    sm_maxrank_embed = 1 if n_a2_orth_a1 > 0 else 0
    su3_embed_only = 1 if n_a2 > 0 else 0

    return {
        "n_roots": n_roots, "rank": rank, "dim": dim,
        "root_lengths": lengths,
        "n_a2": n_a2,
        "n_a2_with_orth_a1": n_a2_orth_a1,
        "a2_with_orth_a1": a2_with_orth_a1,
        "a3_blocks": a3_blocks,
        "n_orth_a1_quads": n_a1_4,
        "sm_dim": sm_dim, "sm_rank": sm_rank,
        "su3_embed_only": su3_embed_only,
        "sm_maxrank_embed": sm_maxrank_embed,
        "example_a2": a2_list[0]["positive"] if a2_list else None,
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    w("=" * 74)
    w("attack_C0162 · so(8) 极大子群分类 · P12-KK-EMBED 开放项闭合（方法论 N2）")
    w("=" * 74)

    R = classify()
    entries = []

    # ---- E1 ----
    w("\n[E1] so(8)/KK 方案事实（attack24 B05/B06/B07 引用不复算）")
    w("  attack24 B06：KK 逃逸最小额外维 n=5（so(1,8) dim36 rank4；紧致部 so(8) dim28 rank4），")
    w("    按「维数>=12 且 秩>=4」四重必要条件判 可容纳 SM: YES（仅必要条件）。")
    w("  attack24 B07 [BOUNDARY]：so(8) 是否含 su(3)+su(2)+u(1) 的极大秩子代数 = P12-KK-EMBED")
    w("    开放项，attack24 不代判定。本册（N2）即闭合此开放项。")
    w("  C0137 E2：SM 签名 (dim=12,rank=4) 下有 3 个互不同构代数；本册专判 su3⊕su2⊕u1 那一支。")
    entries.append(("E1", "so(8)=KK n=5 紧致部（dim28 rank4）；P12-KK-EMBED 为 attack24 B07 开放项",
                    "PASS", "引用 attack24 B06/B07、C0137 E2 不复算"))

    # ---- E2 ----
    w("\n[E2] D4 根系统精算 + 极大秩子代数枚举（本册核心）")
    w("  根数 = %d（±e_i±e_j, i<j<=4）；秩 = %d；生成元 = 根数+秩 = %d"
      % (R["n_roots"], R["rank"], R["dim"]))
    w("  根长² 集合 = %s（D4 单根长度，全根等长=2）" % {str(x) for x in R["root_lengths"]})
    ex = R["example_a2"]
    w("  A2 子根系统（su3）存在数 = %d；样例正根 = %s, %s, %s"
      % (R["n_a2"], ex[0], ex[1], ex[2]))
    w("    样例内积核验：a·b = %s（=-1 ⇒ 120°）；|a|²=|b|²=2；a+b 是根 ⇒ 闭合 A2。"
      % (str(dot(ex[0], ex[1]))))
    w("  其中「与正交 A1(su2) 共存」的 A2 数 = %d" % R["n_a2_with_orth_a1"])
    w("  --- 极大秩候选 ---")
    for blk in R["a3_blocks"]:
        w("  A3 块（指标 %s）：%d 根 = so(6)；块内含 A2(su3) 数 = %d；补方向=e_补=u(1) ⇒ so(6)×so(2)"
          % (blk["idx"], blk["n_roots"], blk["n_inner_a2"]))
    w("  A1^4（两两正交 4 根对）计数 = %d（8 根 = so(4)×so(4)，无 A2）" % R["n_orth_a1_quads"])
    w("  SM 代数账目：su3(dim8 rank2)+su2(dim3 rank1)+u1(dim1 rank1) = dim%d rank%d"
      % (R["sm_dim"], R["sm_rank"]))
    w("  （按代数实算 dim=8+3+1=12、秩=2+1+1=4；任务 prompt 写「15 生成元」与实算 12 不符，")
    w("    本册按实算 12 登记，自抓报备见 §六。）")
    w("  => 核心读数：su3(A2) 可嵌入 so(8) = %d；SM 全群(su3×su2×u1) 极大秩嵌入 = %d"
      % (R["su3_embed_only"], R["sm_maxrank_embed"]))
    entries.append(("E2", "D4: 24 根/秩4/28 元；A2(su3) 存在=%d；与正交 A1 共存的 A2=%d；"
                    "SM 极大秩嵌入=%d" % (R["n_a2"], R["n_a2_with_orth_a1"], R["sm_maxrank_embed"]),
                    "PASS", "整数向量+Fraction 精确枚举"))

    # ---- E3 ----
    w("\n[E3] 与 attack24 P12-KK-EMBED 开放项闭合对照")
    w("  attack24 B06 只证「维数/秩必要条件够」(YES)；B07 把充分性（极大秩嵌入）留为开放项。")
    if R["sm_maxrank_embed"] == 0:
        w("  本册实算：so(8) 根系统内**不存在**「A2(su3) 与其正交 A1(su2)」的闭合子根系统——")
        w("    每个 A2 所在 2D 平面的正交补只含 ±e_4 方向（非 D4 根）与三等量方向（非根），")
        w("    即**无任何 D4 根与某 A2 全部正交**。⇒ su3 可嵌入，但 su2 无法与之正交 commuting。")
        w("  => P12-KK-EMBED 开放项**闭合**：so(8) **不**含 su3×su2×u1 的极大秩子代数。")
        w("    attack24 B06 的『可容纳 SM: YES』仅为必要条件；充分性被本册实算否决。")
    else:
        w("  本册实算：存在 A2+正交A1 ⇒ SM 可极大秩嵌入（开放项按实算登记为可行）。")
    entries.append(("E3", "P12-KK-EMBED 闭合：so(8) 含 SM 极大秩子代数 = %d"
                    % R["sm_maxrank_embed"], "PASS", "对照 attack24 B07"))

    # ---- E4 ----
    w("\n[E4] 方法论 N2 落位 + C0137 衔接")
    w("  方法论矩阵 B9/N2：「机器枚举 so(8) 秩-4 子代数闭合 B07 开放项」——本册即该 N2 落地。")
    w("  C0137 衔接：C0137 证签名 (12,4) 不唯一化 SM（3 候选）；本册在候选① su3⊕su2⊕u1 上")
    w("    进一步否决其「以极大秩子代数身份从 so(8)/KK 涌现」的可能。候选② so5⊕u1² 无 A2，")
    w("    候选③ su2⁴ 无 A2（实算 A1^4 不含 A2）⇒ 三个候选在 so(8) 内均不能装配成 SM。")
    entries.append(("E4", "N2 路径落地；C0137 三候选在 so(8) 内均不可装配出 su3×su2",
                    "PASS", "方法论 B9/N2 + C0137 E2"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  (a) su3(A2) 能否嵌入 so(8)：%d（可）。" % R["su3_embed_only"])
    w("  (b) su3×su2×u1 能否以极大秩子代数嵌入 so(8)：%d（否——无正交 A1）。" % R["sm_maxrank_embed"])
    w("  (c) KK n=5 最小统一候选 so(8) 能否承载 SM 规范嵌入：否。")
    w("  => **P12-KK-EMBED 结构性负面闭合**：KK 逃逸路线（n=5 最小）连「规范嵌入」这一")
    w("    必要充分条件都不满足，撞 **C1**（粒子/规范内容须公设唯一确定）——规范群不能从")
    w("    so(8) 的纯代数结构涌现，须外部公设。attack24 B06 的 YES 降级为「维数秩够但装不下」。")
    entries.append(("E5", "P12-KK-EMBED 结构性负面：so(8) 不含 SM 极大秩子代数（无正交 A1），"
                    "撞 C1", "PASS", "按 E2 实算读数裁定"))

    # ---- 守卫 ----
    guards = [
        ("G1", "根数 = 24（D4）", R["n_roots"] == 24),
        ("G2", "生成元 = 28（24 根 + 4 Cartan = so(8) dim）", R["dim"] == 28),
        ("G3", "秩 = 4", R["rank"] == 4),
        ("G4", "A2(su3) 子根系统存在 = 1", R["n_a2"] >= 1),
        ("G5", "与正交 A1 共存的 A2 数（实算结果）= %d" % R["n_a2_with_orth_a1"],
         R["n_a2_with_orth_a1"] == 0),
        ("G6", "SM 极大秩嵌入判定（实算结果）= %d" % R["sm_maxrank_embed"],
         R["sm_maxrank_embed"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0162 guard failed"

    w("\n[诚实边界]")
    w("  本册为纯李代数根系统枚举：只判「so(8) 是否含 SM 极大秩子代数」，不宣称解决规范群起源；")
    w("  attack24/C0137 外部数值只引用不复算。样例 A2 内积以 Fraction 精确（a·b=-1、|·|²=2）。")
    w("  红线不变：「有预测且对 = 0/22」；数学自洽 ≠ 实验证实；UFT-3=0 保持。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0162_so8极大子群P12闭合_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0162_so8极大子群P12闭合_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0162_so8_maxrank_subalgebra",
            "method_note": "方法论矩阵 N2/B9：机器枚举 so(8) 秩-4 子代数，闭合 attack24 B07 P12-KK-EMBED",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "D4": {
                "n_roots": R["n_roots"], "rank": R["rank"], "dim": R["dim"],
                "root_length2": [str(x) for x in R["root_lengths"]],
            },
            "A2_su3": {"count": R["n_a2"],
                       "example_positive": [list(x) for x in R["example_a2"]]},
            "orthogonal_A1": {"a2_count_with_orth_a1": R["n_a2_with_orth_a1"]},
            "maxrank_candidates": {
                "A3_x_u1_so6xso2": R["a3_blocks"],
                "A1_4_so4xso4_count": R["n_orth_a1_quads"],
            },
            "SM_account": {"su3_dim": 8, "su2_dim": 3, "u1_dim": 1,
                           "sm_dim": R["sm_dim"], "sm_rank": R["sm_rank"]},
            "verdict": {
                "su3_embeds_in_so8": R["su3_embed_only"],
                "SM_maxrank_embed_in_so8": R["sm_maxrank_embed"],
            },
            "guards_passed": sum(1 for g in guards if g[2]),
            "guards_total": len(guards),
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2, default=str)
    print("C0162 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
