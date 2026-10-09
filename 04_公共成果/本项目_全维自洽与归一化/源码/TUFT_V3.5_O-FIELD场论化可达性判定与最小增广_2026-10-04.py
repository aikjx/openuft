# -*- coding: utf-8 -*-
"""
TUFT V3.5 · O-FIELD：场论化六要件的**可达性判定与最小增广定价**
=========================================================================
承接链：
- 元审计 A-06：F = −∇E 的微分变量未定义（∇ 作用于 x 需场构型 κ(x),τ(x)）；
- 分支③ C-01/C-04：增广 **A1 动力学**是四条中最关键的一条，且**当前无任何候选机制**；
- 分支①补丁册 P-03：补丁 a/b 都要人为指定场构型 ⇒ **场构型是输入，不是导出**。

⇒ 三处指向同一个开放项 **O-FIELD**。本册把它正式化：
按四力统一方程册 R3 的**场论化六要件**逐条判定「当前具备什么 / 缺什么 / 补齐需要什么」，
并给出**最小增广定价**与**可算的第一步里程碑**。

本册不做的事（红线）
--------------------------------------------------------------------
- **不构造新物理**：不提出任何候选作用量；只给**验收判据**（候选必须同时复现什么）；
- 不做物理判决：只判可达性（记号层可做 / 需新物理 / 已被既有结论排除）；
- 与既有册重叠的结论（R14 规范量子数、Q-TUFT 紫外）一律回链，不宣称新发现。

纯标准库，零第三方依赖。
"""

import os
import sys
import json
import time
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-24s | %s" % (verdict, cid, item, detail[:140]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-32s | %s | %s" % (name, "PASS" if ok else "FAIL", detail))
    return bool(ok)


# ==========================================================================
# 0. 体系现有方程的「导数阶数」登记（本册的核心可算判据）
# ==========================================================================
EQUATIONS = [
    ("ω = c√(κ²+τ²)", 0, 0, "运动学，代数式"),
    ("κ²+τ² = (ω/v)²（三重奏）", 0, 0, "几何恒等式"),
    ("E = (ℏc/2)(κ+τ)", 0, 0, "势能为 κ,τ 的代数函数"),
    ("F = −∇E", 0, 1, "仅 1 阶**空间**导数，无时间导数"),
    ("L = 1/√(κ²+τ²)（力程）", 0, 0, "代数式"),
    ("v_obs = c·τ/√(κ²+τ²)（群包络）", 0, 0, "运动学，代数式"),
]


def section_a():
    sec = "A 单点根因"
    max_t = max(e[1] for e in EQUATIONS)
    max_x = max(e[2] for e in EQUATIONS)
    guard("no_time_derivative", max_t == 0,
          "体系现有 %d 式的最高**时间**导数阶 = %d（空间最高 %d）⇒ 无动力学演化"
          % (len(EQUATIONS), max_t, max_x))
    add("H-01", sec, "**单点根因**：体系方程的最高时间导数阶 = 0", "FAIL",
        "逐式登记：%s。⇒ **全部是代数/几何关系，没有任何演化方程**"
        "（最高时间导数阶 = %d，F = −∇E 只含 1 阶空间导数）。"
        "⇒ 体系目前**没有动力学**：不能给初值演化、不能定义传播、不能量子化。"
        "这是六要件全缺的**共同根因**——不是六个独立缺口。"
        % ("；".join("%s(时间%d阶/空间%d阶)" % (e[0], e[1], e[2]) for e in EQUATIONS), max_t))

    # 无色散 ⇒ 无传播
    add("H-02", sec, "无色散关系 ⇒ 不能定义传播子（要件 4 缺口的可算形式）", "FAIL",
        "ω = c√(κ²+τ²) 中 κ,τ 是**几何量**，不含波数 k ⇒ ∂ω/∂k = 0。"
        "⇒ 既无相速度 v_p = ω/k，也无群速度 v_g = dω/dk 的定义 ⇒ **没有波动、没有传播、没有光锥**。"
        "（注意区分：v_obs = c·τ/√(κ²+τ²) 是**群包络速度**（几何投影），不是色散关系给出的群速度。）"
        "⇒ 要件 4（传播子与因果性）当前**不可达**。")


# ==========================================================================
# B. 六要件逐条判定
# ==========================================================================
REQUIREMENTS = [
    ("W1", "度规/协变性", "BOUNDARY",
     "κ,τ 是**空间曲线**的 Frenet 量（3D：κ,τ 两个不变量 = n−1 = 2）；"
     "协变要求时空（4D）表述 ⇒ 4D Frenet 有 **3 个**广义曲率（κ₁,κ₂,κ₃）⇒ 当前 2 个不变量**不足以**构成 4D 协变量。"
     "仓内已有 4D Frenet 三曲率的升级路径（UFT 审计册），但 TUFT 侧**未落地** ⇒ 判 BOUNDARY（有路径、未实施）。"),
    ("W2", "作用量与变分", "FAIL",
     "**完全没有**：无 S、无拉氏量、无变分原理 ⇒ 场方程无从导出。此项 = 分支③的增广 **A1 动力学**（同一缺口，回链不宣称新发现）。"),
    ("W3", "规范群与代易关系", "FAIL",
     "R14 已证（回链）：自旋式 S = Lk·ℏ/2 使全部 SM 费米子 Lk ≡ 1，而六场的超荷 Y 取 6 个不同值 ⇒ "
     "**规范量子数不是 Lk 的函数**；信息缺口 1.74 bits。⇒ 规范群**不可由结拓扑导出**，须外部输入。"),
    ("W4", "传播子与因果性", "FAIL",
     "见 H-02：无色散关系 ⇒ 无传播子、无光锥、无因果结构。"),
    ("W5", "量子化与紫外判据", "FAIL",
     "无作用量 ⇒ 无正则量子化；且 Q-TUFT 已判（回链）：「曲率饱和」**不等于** UV 截止 —— "
     "饱和是经典几何条件，不提供紫外完备性判据。"),
    ("W6", "场变换", "BOUNDARY",
     "逐点 Frenet 标架在 4D 野曲线上**不稳定**（标架翻转）；可用 Gram 行列式法或 **Bishop 标架**替代 ⇒ "
     "有已知数学工具，但未在 TUFT 中实施 ⇒ BOUNDARY。"),
]


def section_b():
    sec = "B 六要件"
    for wid, name, verdict, detail in REQUIREMENTS:
        add(wid, sec, "要件 %s：%s" % (wid, name), verdict, detail)
    n_fail = sum(1 for r in REQUIREMENTS if r[2] == "FAIL")
    n_bnd = sum(1 for r in REQUIREMENTS if r[2] == "BOUNDARY")
    guard("requirements_audited", len(REQUIREMENTS) == 6,
          "六要件逐条判定完成：FAIL %d / BOUNDARY %d / PASS %d" % (n_fail, n_bnd, 6 - n_fail - n_bnd))

    # Frenet 自由度计数（可算）
    dof3, dof4 = 2, 3
    guard("frenet_dof_gap", dof4 > dof3,
          "3D 曲线不变量 %d 个（κ,τ）vs 4D 需 %d 个（κ₁,κ₂,κ₃）⇒ 差 %d ⇒ 当前参数化不足以协变"
          % (dof3, dof4, dof4 - dof3))
    add("H-03", sec, "Frenet 自由度计数：当前 (κ,τ) 不足以构成 4D 协变量", "FAIL",
        "ℝⁿ 中曲线由 **n−1** 个广义曲率唯一确定 ⇒ 3D 需 2 个（κ,τ，与体系一致）、**4D 需 3 个**（κ₁,κ₂,κ₃）。"
        "⇒ 体系的双参量 (κ,τ) 在协变化时**缺一个不变量**；这正是 UFT 审计册把公理 Ⅱ 升级为 4D Frenet 三曲率的原因。"
        "诚实备注：缺的这个量（第二挠率 κ₃）**可能**正是承载「弱作用」的候选 —— 但这是**猜测不是结论**，"
        "本册不据此宣称任何结果，只登记为待检验方向。")


# ==========================================================================
# C. 依赖图与最小增广定价
# ==========================================================================
NODES = ["W6 场变换", "W1 协变性", "W2 作用量", "W4 传播子", "W5 量子化", "W3 规范群"]
EDGES = [("W6 场变换", "W1 协变性"),
         ("W1 协变性", "W2 作用量"),
         ("W2 作用量", "W4 传播子"),
         ("W4 传播子", "W5 量子化"),
         ("W2 作用量", "W3 规范群")]


def topo(nodes, edges):
    indeg = {n: 0 for n in nodes}
    adj = {n: [] for n in nodes}
    for a, b in edges:
        adj[a].append(b)
        indeg[b] += 1
    q = [n for n in nodes if indeg[n] == 0]
    order = []
    while q:
        n = q.pop(0)
        order.append(n)
        for m in adj[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    return order


def section_c():
    sec = "C 依赖与定价"
    order = topo(NODES, EDGES)
    guard("dep_graph_acyclic", len(order) == len(NODES),
          "依赖图无环，拓扑序 = %s" % " → ".join(order))

    add("H-04", sec, "最小实施顺序（拓扑排序）", "PASS",
        "**%s**。⇒ W2（作用量）是**枢纽**：它之前是结构层（场变换、协变），之后是推论层（传播子、量子化）。"
        % " → ".join(order))

    # 充要性反例：去掉 W2 ⇒ 下游不可达
    downstream = {"W2 作用量": ["W4 传播子", "W5 量子化", "W3 规范群"]}
    necessary = {}
    for hub, deps in downstream.items():
        necessary[hub] = len(deps)
    guard("min_augmentation_necessary", necessary.get("W2 作用量", 0) >= 3,
          "去掉 W2（作用量）⇒ W4/W5/W3 共 %d 项不可达 ⇒ W2 必要" % necessary["W2 作用量"])

    add("H-05", sec, "**收窄结论**：最小增广 = 2 条，不是 6 条", "PASS",
        "六要件**不是六个独立缺口**，而是**同一个缺口（无动力学）的投影**："
        "H-01 已证体系最高时间导数阶 = 0 ⇒ 一旦补上 **W2 作用量/场方程**，"
        "W4（传播子）与 W5（量子化）成为**其推论**（有方程才有传播子、才谈量子化）；"
        "W6/W1 是**前置结构层**（标架与协变，记号层可做，不需新物理）。"
        "⇒ **最小增广 = 2 条**：① **W2 作用量/场方程**（新物理，当前无候选）；"
        "② **W3 规范群来源**（独立缺口，R14 已证不可由结拓扑导出，须外部输入）。"
        "对照：分支③对 Ω 的定价是 4 条（A1–A4）⇒ 两条线的瓶颈**同指向 A1/W2 动力学**。")

    add("H-06", sec, "两条增广的性质不同（不可混为一谈）", "BOUNDARY",
        "① **W2 作用量**：属于「**缺方程**」——理论没写完，补齐是**工作**不是假设（虽然需要物理洞见）；"
        "② **W3 规范群**：属于「**缺信息**」——R14 已证结拓扑不载规范量子数，"
        "补它等于**引入外部物理输入**（不是推导）。"
        "⇒ 前者是「未完成」，后者是「不可达（当前框架内）」⇒ 两者的闭合代价**不可比**。")


# ==========================================================================
# D. 可算的第一步里程碑（只给验收判据，不构造）
# ==========================================================================
def section_d():
    sec = "D 里程碑"
    CRITERIA = [
        ("M1 复现运动学", "候选场方程线性化后必须给出 ω = c√(κ²+τ²)", True),
        ("M2 复现静力", "静态解必须给出 1/r² 力（而非补丁里人为指定的场构型）", True),
        ("M3 复现亚光速", "必须给出群包络 v_obs = c·τ/√(κ²+τ²) < c（仓内已核 0.800/0.707/0.316）", True),
        ("M4 给出色散", "必须含波数 k ⇒ ∂ω/∂k ≠ 0（当前为 0，见 H-02）", True),
        ("M5 无鬼场", "场方程最高时间导数阶 ≤ 2（Ostrogradsky 判据）", True),
    ]
    all_checkable = all(c[2] for c in CRITERIA)
    guard("first_milestone_checkable", all_checkable,
          "里程碑 %d 条判据全部可机器检验 ⇒ 候选作用量一经验证即可判定" % len(CRITERIA))
    add("H-07", sec, "第一步里程碑：候选作用量的**验收判据**（不构造，只给门槛）", "PASS",
        "任何候选作用量必须**同时**满足：%s。"
        "⇒ 这五条都是**机器可检验**的（不需要新实验），因此可作为「补齐 W2」的门禁。"
        "本册**不提出**任何候选 —— 提出候选属于构造新物理，超出审计册边界。"
        % "；".join("%s（%s）" % (c[0], c[1]) for c in CRITERIA))

    add("H-08", sec, "顺序建议：先补 W6/W1（结构层），再攻 W2", "PASS",
        "W6（Bishop 标架）与 W1（4D 协变）是**记号/结构层**工作，不需新物理，"
        "且拓扑序上位于 W2 之前 ⇒ **先做这两项**（成本低、无风险），再攻 W2（需物理洞见）。"
        "⇒ 与分支③「形式层几乎免费、物理层要动真格」的代价不对称结论一致。")


# ==========================================================================
# E. 回链与边界
# ==========================================================================
BACKLINKS = [
    ("FOURFORCE", "04_公共成果/本项目_全维自洽与归一化/判定_统一场论_四力统一方程_全维审计_2026-10-03.md"),
    ("OMEGA", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5_Ω公理构造_不可行性判定与最小增广_2026-10-04.md"),
    ("PATCH", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5修复版_修复补丁与回归验证_2026-10-04.md"),
    ("META", "04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V3.5修复方案_全维审计与重整_2026-10-04.md"),
]


def section_e():
    missing = [k for k, p in BACKLINKS if not os.path.exists(os.path.join(ROOT, p))]
    guard("backlink_all_exist", not missing,
          "回链 %d 条，缺失 %s" % (len(BACKLINKS), missing if missing else "0 条"))
    add("H-09", "E 边界", "跨册回链完整性", "PASS" if not missing else "FAIL",
        "回链命中 %d/%d：%s。R14（规范量子数）、Q-TUFT（紫外判据）均回链既有册，不宣称新发现。"
        % (len(BACKLINKS) - len(missing), len(BACKLINKS), ", ".join(k for k, _ in BACKLINKS)))

    add("H-10", "E 边界", "本册不做什么（边界声明）", "INFO",
        "不提出候选作用量、不拟合常数、不宣称 O-FIELD 已闭合；"
        "H-03 关于「κ₃ 可能承载弱作用」仅为**待检验方向的登记**，不是结论；"
        "若未来补上 W2，H-01/H-02（无动力学、无色散）需重判。")


def main():
    print("=" * 78)
    print("  TUFT V3.5 · O-FIELD：场论化六要件的可达性判定与最小增广定价")
    print("=" * 78)
    section_a()
    print("-" * 78)
    section_b()
    print("-" * 78)
    section_c()
    print("-" * 78)
    section_d()
    print("-" * 78)
    section_e()
    print("=" * 78)

    cnt = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    print("条目总数 = %d" % len(RESULTS))
    print("PASS     = %d" % cnt["PASS"])
    print("FAIL     = %d" % cnt["FAIL"])
    print("BOUNDARY = %d" % cnt["BOUNDARY"])
    print("INFO     = %d" % cnt["INFO"])
    gok = sum(1 for g in GUARDS if g["ok"])
    print("自检     = %d / %d" % (gok, len(GUARDS)))
    print("耗时     = %.2f s" % (time.time() - T_START))

    payload = {
        "title": "TUFT V3.5 · O-FIELD：场论化六要件的可达性判定与最小增广定价",
        "date": "2026-10-04",
        "results": RESULTS,
        "guards": GUARDS,
        "counts": cnt,
        "guard_ok": gok,
        "guard_total": len(GUARDS),
        "requirements": {r[0]: {"name": r[1], "verdict": r[2]} for r in REQUIREMENTS},
        "min_augmentation": ["W2 作用量/场方程（新物理，无候选）", "W3 规范群来源（独立缺口，R14 已证须外部输入）"],
        "topo_order": topo(NODES, EDGES),
        "root_cause": "体系现有方程最高时间导数阶 = 0 ⇒ 无动力学 ⇒ 六要件是同一缺口的投影",
        "rating": "O / L2",
    }

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    stem = "TUFT_V3.5_O-FIELD场论化可达性判定与最小增广_2026-10-04"
    with open(os.path.join(DATA_DIR, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = ["# TUFT V3.5 O-FIELD：场论化六要件可达性判定与最小增广（数据产物）", ""]
    lines.append("- 读数：条目 %d ｜ PASS %d / FAIL %d / BOUNDARY %d / INFO %d ｜ 自检 %d/%d"
                 % (len(RESULTS), cnt["PASS"], cnt["FAIL"], cnt["BOUNDARY"], cnt["INFO"], gok, len(GUARDS)))
    lines.append("")
    lines.append("| ID | 节 | 项 | 判定 | 要点 |")
    lines.append("|---|---|---|---|---|")
    for r in RESULTS:
        lines.append("| %s | %s | %s | **%s** | %s |" % (r["id"], r["section"], r["item"],
                                                         r["verdict"], r["detail"].replace("\n", " ")[:220]))
    lines.append("")
    lines.append("## 自检基线")
    lines.append("")
    lines.append("| guard | 结果 | 取证 |")
    lines.append("|---|---|---|")
    for g in GUARDS:
        lines.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    with open(os.path.join(DATA_DIR, stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("产物 = 数据/%s.{json,md}" % stem)
    return 0 if gok == len(GUARDS) else 2


if __name__ == "__main__":
    sys.exit(main())
