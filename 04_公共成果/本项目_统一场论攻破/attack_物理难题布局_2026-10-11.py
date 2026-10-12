# -*- coding: utf-8 -*-
"""
attack_物理难题布局_2026-10-11.py
物理难题 · 攻破布局（路线图）独立复算

本册把 C0126–C0134 的"负面闭合"读数与仓内建设性纲领（O1–O4）／新原理蓝本
（C1–C8 硬约束、D1–D3 探索窗口）合并为一张**攻破布局图**：
  1) 已闭合账（七障碍 + 引力本质专项）；
  2) 物理层仍未解决的难题清单（所需机制 / 是否被 C1–C8 挡住 / 代价）；
  3) 依赖 DAG → 拓扑分层 → 分阶段路线图（谁必须先解决）；
  4) 阻塞力（下游依赖数）排序 → 优先级；
  5) 诚实总账：负面侧已闭合，建设侧仍需新物理。

纯标准库（无外部依赖）；输出 JSON + 报告；退出码 0。

诚实边界（红线）：
- "已攻破"专指**对 TUFT 原初声称的结构性负面闭合**；不等于物理难题已被解决。
- 物理层开放难题（量子引力、层级、暗物质…）**本册不宣称解决**，只给出布局与验收门槛。
- 红线：「有预测且对 = 0/22」不变；数学自洽 ≠ 实验证实。
"""
from __future__ import annotations
import json
import os

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------------------------------------------------------------- 一、已闭合账（七障碍 + 引力本质专项）
BARRIERS = [
    ("1 量纲", "FIXED", "C0123：挠率力量纲修复（ℓ_P 幂次 4→2）"),
    ("2 群论", "NEG", "C0125/C0127：so(1,3) ⊥ su(3)⊕su(2)⊕u(1)，Δdim=6"),
    ("3 手征", "NEG", "C0129：无 P_L/γ⁵/SU(2)_L 载体，P_LP_R=0"),
    ("4 量子化", "NEG", "C0131：[G]=−2 不可重整 + 挠率四费米子二圈发散 + RG 不闭合"),
    ("5 真空能", "NEG", "C0126：ρ_T 超暗能量 ~99 数量级"),
    ("6 等级", "NEG", "C0130：单尺度 vs 双尺度，η=1.02e-17、(M_P/M_H)²=9.52e33"),
    ("7 实验", "NEG", "C0132：τ 比 1e6、κ 比 1e29、偏振零信号"),
]
SPECIAL = [("引力本质", "SPECIAL", "C0134：引力=唯一质量耦合的自旋-2 几何耦合 (m/m_P)²")]

# ---------------------------------------------------------------- 二、物理层开放难题清单
# (id, 名称, 所需机制, TUFT/几何框架是否提供, 被 C1–C8 哪几条挡住, 补丁代价(自由参数/外部输入), 依赖)
OPEN_PROBLEMS = [
    ("P12", "规范群起源", "群/空间由公设唯一确定（纲领 O3）", False, ["C1"], "1 枚唯一化原理", []),
    ("P13", "耦合常数绝对值", "绝对标度第一性导出（α、G 数值）", False, ["C2", "C3"], "1 枚标度", ["P12"]),
    ("P01", "量子引力 / 引力量子化", "紫外完备 + 背景无关量子化", False, ["C1", "C7"], "无穷多枚前置系数", []),
    ("P02", "层级 / 等级问题", "第二尺度 + 保护机制（SUSY/额外维/复合）", False, ["C2", "C7"], "≥2 枚（新尺度+保护）", ["P13", "P01"]),
    ("P03", "宇宙学常数 / 真空能", "真空能抵消或选择机制", False, ["C2"], "1 枚（抵消/选择）", ["P01"]),
    ("P08", "大统一 / 质子衰变", "GUT 群 + 重玻色子 + 阈值", False, ["C1", "C2"], "≥2 枚（群+能标）", ["P12", "P13"]),
    ("P11", "味 / 代数结构", "代结构与 Yukawa 起源", False, ["C1", "C2"], "≥2 枚（代+Yukawa）", ["P12"]),
    ("P06", "中微子质量", "seesaw / Dirac + 右手中微子", False, ["C2"], "≥1 枚（右手中微子标度）", ["P11"]),
    ("P07", "重子生成 / 重子不对称", "B 违反 + CP 破坏 + 偏离热平衡", False, ["C1", "C2"], "≥2 枚（CP 相+能标）", ["P08", "P11"]),
    ("P10", "强 CP 问题（θ）", "Peccei–Quinn / axion 或 θ=0 机制", False, ["C1"], "1 枚（新对称/场）", []),
    ("P04", "暗物质", "新稳定中性粒子 / 修正引力", False, ["C1", "C5"], "≥1 枚（粒子/修正）", []),
    ("P09", "暴胀", "inflaton + 慢滚势（或替代）", False, ["C1", "C2", "C5"], "≥2 枚（势+标度）", ["P01", "P03"]),
    ("P05", "暗能量", "状态方程 w 与演化机制", False, ["C2", "C5"], "≥1 枚", ["P03"]),
    ("P15", "黑洞信息悖论", "量子引力 + 幺正演化", False, ["C1", "C7"], "依赖 P01", ["P01"]),
    ("P16", "量子引力现象学", "可检验预言（单点+误差带）", False, ["C5", "C6"], "依赖 P01 且需数值", ["P01"]),
    ("P14", "量子测量 / 测量问题", "解释或新动力学（collapse 机制）", False, ["C5", "C6"], "不可判定（诠释层）", []),
]

# ---------------------------------------------------------------- 拓扑分层（最长路径分层）
def topo_layers(nodes, deps):
    """返回 {id: 层号}；层 = 最长依赖路径长度（0 = 无依赖）。"""
    memo = {}

    def depth(n, stack):
        if n in memo:
            return memo[n]
        if n in stack:            # 环保护
            return 0
        stack.add(n)
        d = 0
        for p in deps.get(n, []):
            d = max(d, depth(p, stack) + 1)
        stack.discard(n)
        memo[n] = d
        return d

    for n in nodes:
        depth(n, set())
    return memo


def descendants(nodes, deps):
    """返回 {id: 下游（传递）依赖它的难题数} = 阻塞力。"""
    rev = {n: [] for n in nodes}
    for n in nodes:
        for p in deps.get(n, []):
            rev[p].append(n)

    def all_desc(n, seen):
        out = 0
        for m in rev[n]:
            if m in seen:
                continue
            seen.add(m)
            out += 1 + all_desc(m, seen)
        return out

    return {n: all_desc(n, {n}) for n in nodes}


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    w("=" * 76)
    w("attack_物理难题布局 · 攻破路线图 独立复算")
    w("=" * 76)

    # 一、已闭合账
    n_fixed = sum(1 for b in BARRIERS if b[1] == "FIXED")
    n_neg = sum(1 for b in BARRIERS if b[1] == "NEG")
    w("\n[一] 已闭合账（TUFT 七障碍 + 引力本质专项）")
    for name, st, note in BARRIERS:
        w("  %-8s %-6s %s" % (name, st, note))
    for name, st, note in SPECIAL:
        w("  %-8s %-6s %s" % (name, st, note))
    w("  => 七障碍：修复 %d / 负面闭合 %d（合计 7 项）；引力本质专项 1 项。" % (n_fixed, n_neg))

    # 二、开放难题
    ids = [p[0] for p in OPEN_PROBLEMS]
    deps = {p[0]: p[6] for p in OPEN_PROBLEMS}
    blocked_by_c = {}
    cost = {}
    need = {}
    provides = {}
    for pid, name, nd, prov, blocked, cst, dp in OPEN_PROBLEMS:
        blocked_by_c[pid] = blocked
        cost[pid] = cst
        need[pid] = nd
        provides[pid] = prov
    w("\n[二] 物理层开放难题清单（%d 项）" % len(OPEN_PROBLEMS))
    w("  %-5s %-16s %-30s %-16s %s" % ("id", "难题", "所需机制", "被 C 挡住", "补丁代价"))
    for pid, name, nd, prov, blocked, cst, dp in OPEN_PROBLEMS:
        w("  %-5s %-16s %-30s %-16s %s" % (pid, name, nd[:28], ",".join(blocked), cst))
    w("  => TUFT/几何框架提供所需机制者：%d / %d" % (sum(1 for p in provides.values() if p), len(OPEN_PROBLEMS)))

    # 三、拓扑分层 → 阶段
    layers = topo_layers(ids, deps)
    maxl = max(layers.values())
    phases = {}
    for n in ids:
        phases.setdefault(layers[n], []).append(n)
    w("\n[三] 依赖 DAG → 拓扑分层的阶段布局（层 = 最长依赖链）")
    for L in sorted(phases):
        names = [p[1] for p in OPEN_PROBLEMS if p[0] in phases[L]]
        w("  第 %d 层（phase %d）：%s" % (L, L, "、".join(names)))
    w("  => 共 %d 层；第 0 层为**分水岭**（无上游依赖，必须先解决）" % (maxl + 1))

    # 四、阻塞力排序
    desc = descendants(ids, deps)
    order = sorted(ids, key=lambda n: (-desc[n], n))
    w("\n[四] 阻塞力排序（下游传递依赖数越多越优先）")
    for n in order:
        nm = [p[1] for p in OPEN_PROBLEMS if p[0] == n][0]
        w("  %-5s %-16s 下游依赖 %d 项" % (n, nm, desc[n]))
    top = order[0]
    top_name = [p[1] for p in OPEN_PROBLEMS if p[0] == top][0]
    w("  => 最高阻塞力：%s（%s），下游 %d 项" % (top, top_name, desc[top]))

    # 五、代价账
    w("\n[五] 代价账（若逐项打补丁所需外部输入）")
    tot_min = sum(1 for p in OPEN_PROBLEMS if "≥" in p[5] or "枚" in p[5])
    w("  16 项开放难题中，%d 项需至少 1 枚新自由参数/外部输入；" % tot_min)
    w("  其中 P01（量子引力）需**无穷多枚**前置系数（逐圈 D=2+2L，见 C0131/G11 型记账）。")
    w("  => 按蓝本 C3「自由参数必须为零」：全部 %d 项均不满足 ⇒ UFT-3=0 保持。" % len(OPEN_PROBLEMS))

    # 六、总账与诚实边界
    w("\n[六] 攻破总账与诚实边界")
    w("  负面侧（对 TUFT 原初声称）：七障碍 7/7 闭合 + 引力本质专项 ⇒ 已全部攻破。")
    w("  建设侧（物理难题本身）：%d 项仍开放，**本册不宣称解决**。" % len(OPEN_PROBLEMS))
    w("  布局用途：给出有序队列 + 验收门槛（C1–C8、M1–M5），下一轮从最高阻塞力项推进。")
    w("  红线：「有预测且对 = 0/22」不变；数学自洽 ≠ 实验证实。")

    w("\n退出码 0（布局复算完成，读数送布局册与总账）。")

    report_path = os.path.join(BASE, "attack_物理难题布局_2026-10-11_report.txt")
    json_path = os.path.join(BASE, "attack_物理难题布局_2026-10-11.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "physics_problem_roadmap",
            "barriers_closed": {"fixed": n_fixed, "negative": n_neg, "special": len(SPECIAL)},
            "open_problems": [
                {"id": p[0], "name": p[1], "need": p[2], "tuft_provides": p[3],
                 "blocked_by": p[4], "cost": p[5], "deps": p[6]} for p in OPEN_PROBLEMS
            ],
            "layers": {str(k): phases[k] for k in sorted(phases)},
            "blocking_power": desc,
            "priority_order": order,
            "top_blocking": {"id": top, "name": top_name, "downstream": desc[top]},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("roadmap written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
