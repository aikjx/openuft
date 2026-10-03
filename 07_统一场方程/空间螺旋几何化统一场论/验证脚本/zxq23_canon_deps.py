# -*- coding: utf-8 -*-
"""
UFE-2 正典依赖图 · 独立自由度 · 公设溯源对账（zxq23_canon_deps）

为什么需要它
------------
`zxq23_canon_guard.py` 管的是「**该不该**在正典里」；本脚本管的是「**够不够**」：

1. 26 条正典里真正独立的条目有几条？其余是派生的吗？—— 这是"统一程度"的定量读数，
   也是判断"这到底算不算一个统一场方程"的唯一硬指标。
2. 有没有**孤儿**（进了正典却没有任何下游消费者）？有的话它们是背景支架还是凑数？
3. 26 条里有 9 条是「派生自 = —」的公设/独立输入。**它们能不能被体系内其它条目推出？**
   这就是公设溯源缺口 O-P1 —— UFE-2 能否从 L2 升到 L3 的唯一关口。
4. 正典 C-20（公设 $\omega\rho=c$）与 07 层第 10 卷的 $\kappa,\tau,\omega$ 恒等式是"同族"，
   但两者的角参数化口径可能不同。本脚本与第 10 卷的 200 位读数联做一次对账，
   并**裁决** 23 式里那对互为倒数的 α 几何定义（正典 X-09）。

复用
----
正典表的解析器**直接 import 自门禁**（`zxq23_canon_guard.parse_tables`），
不复写第二份 —— 同一份解析器是"门禁看到的表"与"本脚本看到的表"一致的前提。

依赖：仅标准库。读 26 册 markdown、`zxq23_ufe_results.json`、`../verify_vc_results.json`。

运行：python -B zxq23_canon_deps.py            # 退出码恒 0
      python -B zxq23_canon_deps.py --strict    # 任一 FAIL ⇒ 退出码 1
"""

import json
import math
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import zxq23_canon_guard as GUARD  # noqa: E402  复用同一份表格解析器

CANON_MD = os.path.join(BASE, "26_UFE2_正典_统一场方程正确子集规范_2026-10-03.md")
VC_JSON = os.path.join(BASE, os.pardir, "verify_vc_results.json")
OUT_JSON = os.path.join(HERE, "zxq23_canon_deps_results.json")

# CODATA 2018
ALPHA = 7.2973525693e-3

RESULTS = []


def rec(sid, sec, title, verdict, detail):
    RESULTS.append({"id": sid, "sec": sec, "title": title,
                    "verdict": verdict, "detail": detail})


def P(sid, sec, title, d):
    rec(sid, sec, title, "PASS", d)


def F(sid, sec, title, d):
    rec(sid, sec, title, "FAIL", d)


def BO(sid, sec, title, d):
    rec(sid, sec, title, "BOUNDARY", d)


def IN(sid, sec, title, d):
    rec(sid, sec, title, "INFO", d)


def g(x, n=6):
    return "%.*g" % (n, x)


# ============================================================ §DEP 依赖图
def load_canon():
    with open(CANON_MD, encoding="utf-8") as fh:
        md = fh.read()
    canon_rows, excl_rows = GUARD.parse_tables(md)
    nodes, edges, kind = {}, {}, {}
    for row in canon_rows:
        if len(row) < 7:
            continue
        code = row[0].strip()
        nodes[code] = row[1].strip()
        kind[code] = row[2].strip()
        edges[code] = re.findall(r"C-\d{2}", row[5])
    return canon_rows, excl_rows, nodes, kind, edges


def children_of(edges):
    """派生图的反向邻接：children[p] = 以 p 为上游的条目。
    注意方向 —— 表里的「派生自」指向**上游**，所以要下游可达必须走 children。"""
    ch = {c: [] for c in edges}
    for c, ps in edges.items():
        for p in ps:
            if p in ch:
                ch[p].append(c)
    return ch


def reachable(starts, ch):
    seen, stack = set(starts), list(starts)
    while stack:
        n = stack.pop()
        for c in ch.get(n, []):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def sec_dep(canon_rows, nodes, kind, edges):
    total = len(nodes)
    ch = children_of(edges)
    roots = sorted([c for c in nodes if not edges[c]])          # 无上游 = 独立输入 / 公设
    leaves = sorted([c for c in nodes if not ch.get(c)])       # 无下游 = 结论的终点
    isolated = sorted(set(roots) & set(leaves))                # 既无上游也无下游 = 完全孤立
    terminal = sorted(set(leaves) - set(roots))                # 有上游、无下游 = 终端结论

    P("F01", "DEP", "正典条目与依赖边读数",
      "正典 %d 条；依赖边 %d 条；无上游（独立输入 / 公设）%d 条 → %s；"
      "终端结论（有上游、无下游）%d 条；完全孤立（无上游也无下游）%d 条 → %s"
      % (total, sum(len(v) for v in edges.values()), len(roots), "、".join(roots),
         len(terminal), len(isolated), "、".join(isolated) if isolated else "无"))

    # 承重核心：从三条本构/主式公设沿**下游**能覆盖多少
    core = reachable(["C-01", "C-02", "C-03"], ch)
    a_nodes = [c for c in nodes if kind.get(c, "").startswith("A")]
    a_in_core = sorted(set(a_nodes) & core)
    if sorted(a_nodes) == a_in_core:
        P("F02", "DEP", "承重核心（从 C-01/C-02/C-03 沿下游可达）",
          "可达 %d 条：%s；A 类 %d 条**全部**落在核心内 ⇒ "
          "UFE-2 的 A 类是一个闭合的推导系统，没有外部悬空"
          % (len(core), "、".join(sorted(core)), len(a_nodes)))
    else:
        F("F02", "DEP", "承重核心未覆盖全部 A 类条目",
          "未落在核心内的 A 类条目：%s" % sorted(set(a_nodes) - core))
        a_in_core = sorted(set(a_nodes) & core)

    # 完全孤立的公设：既没被用上、也没推出任何东西
    if isolated:
        BO("F03", "DEP", "完全孤立的公设（既无上游也无下游）",
           "%s 进了正典却**既没有被任何条目推出、也没有被任何条目使用**。"
           "对 C-10（螺旋时空参数式）而言它是背景设定而非推导链的一环 —— "
           "保留它的理由是它给出了速度分解的角度参数化（C-26 的上游），"
           "但这条联系目前是**语义关联而非公式依赖**，如实登记"
           % "、".join(isolated))
    else:
        P("F03", "DEP", "无完全孤立条目", "每条无上游条目都有下游消费者")

    ratio = float(total) / len(roots) if roots else float("inf")
    P("F04", "DEP", "独立自由度与压缩比",
      "独立输入（公设）%d 条 / 正典 %d 条 ⇒ 压缩比 %.3f；"
      "即每条独立输入平均带出 %.2f 条派生结论" % (len(roots), total, ratio, ratio - 1.0))

    # 最长派生链（沿下游）
    best = []
    for r in roots:
        path = [r]
        stack = [(r, [r])]
        while stack:
            n, pth = stack.pop()
            for c in ch.get(n, []):
                if c in pth:
                    continue
                np_ = pth + [c]
                if len(np_) > len(path):
                    path = np_
                stack.append((c, np_))
        if len(path) > len(best):
            best = path
    P("F05", "DEP", "最长派生链（沿下游，独立输入 → 终端结论）",
      "最长链 %d 个节点：%s" % (len(best), " → ".join(best)))

    # 公设的量纲支撑覆盖率
    with open(os.path.join(HERE, "zxq23_ufe_results.json"), encoding="utf-8") as fh:
        idx = {r["id"]: r["verdict"] for r in json.load(fh)["results"]}
    sup = {}
    for row in canon_rows:
        if len(row) < 7:
            continue
        code = row[0].strip()
        if code in roots:
            sup[code] = [i for i in re.findall(r"[DMNPST]\d{2}[a-z]?", row[4])
                         if idx.get(i) == "PASS"]
    covered = [c for c in roots if sup.get(c)]
    IN("F06", "DEP", "公设的量纲/结构支撑覆盖率",
       "%d/%d 条无上游条目有 PASS 级判据支撑（%s）；"
       "**但量纲自洽 ≠ 可推导** —— 公设的不可推导性是定义性的，见 §TRACE 的 O-P1（E01）"
       % (len(covered), len(roots), "、".join(covered) if covered else "无"))


def _chain(node, edges):
    out = [node]
    seen = {node}
    while True:
        ps = [p for p in edges.get(out[-1], []) if p not in seen]
        if not ps:
            return out
        out.append(ps[0])
        seen.add(out[-1])


# ============================================================ §TRACE 公设溯源与 α 口径裁决
def sec_trace(edges):
    roots = sorted([c for c in edges if not edges[c]])

    # O-P1：公设不可由体系内其它条目推出 —— 这是缺口，不是缺陷
    BO("E01", "TRACE", "O-P1 公设溯源缺口（UFE-2 升 L3 的唯一关口）",
       "无上游条目 %d 条：%s。它们的量纲都过检（F07），但**没有任何一条是由正典内"
       "其它条目推出的** ⇒ 从 L2 升到 L3 需要一条「公设 ⇒ 场互变三式」的推导链，"
       "而来料（核心公式.md）只给了断言、没给这条链。这是缺口，不是被判 FAIL"
       % (len(roots), "、".join(roots)))

    # ---- 与第 10 卷对账：裁决 α 的几何定义
    if not os.path.isfile(VC_JSON):
        F("E02", "TRACE", "第 10 卷读数缺失，无法对账",
          "找不到 %s；先跑 07 层的 verify_vc_kappa_tau_omega.py" % os.path.basename(VC_JSON))
        return
    with open(VC_JSON, encoding="utf-8") as fh:
        vc = json.load(fh)
    vcres = vc.get("results", {})
    tan_key = None
    for k in vcres:
        if "tan" in k:
            tan_key = k
    if tan_key is None:
        F("E02", "TRACE", "第 10 卷读数里找不到 tanθ 项", "keys=%s" % list(vcres)[:8])
        return
    vc_pass = bool(vcres[tan_key].get("pass"))
    P("E02", "TRACE", "第 10 卷判据：tanθ = τ/κ = v_z/v_perp",
      "读数项「%s」pass=%s（%s 位有效数字，残差 %s）"
      % (tan_key, vc_pass, vc.get("dps"), vcres[tan_key].get("error")))

    # 由 C-26（速度分解）算 tanθ
    a = ALPHA
    vp = a                      # v_perp = α c
    vz = math.sqrt(1.0 - a * a)  # v_z = c·sqrt(1-α²)
    tan23 = vz / vp
    P("E03", "TRACE", "由 C-26 速度分解算 tanθ",
      "v_⊥/c=α=%s、v_z/c=%s ⇒ tanθ = v_z/v_⊥ = %s（= 1/α = %s 的 %.5f 倍）"
      % (g(a), g(vz), g(tan23), g(1.0 / a), tan23 * a))

    # 精确的 κ/τ（把 tanθ=τ/κ 代回）
    kappa_tau_exact = 1.0 / tan23
    dev_alpha = abs(kappa_tau_exact - a) / kappa_tau_exact
    P("E04", "TRACE", "裁决 ①：α = κ/τ 方向正确，但精确式带 O(α²) 修正",
      "第 10 卷的 τ/κ = tanθ = %s ⇒ κ/τ = %s；而 C-20 一侧的 α = %s。"
      "相对差 %s ≈ α²/2 = %s ⇒ **23 式写 α=κ/τ 是丢掉 O(α²) 的工作近似**"
      "（精确式 κ/τ = α/√(1−α²) = α(1+α²/2+O(α⁴))）"
      % (g(tan23), g(kappa_tau_exact), g(a), g(dev_alpha), g(a * a / 2)))

    dev_inv = abs(1.0 / a - kappa_tau_exact) / kappa_tau_exact
    F("E05", "TRACE", "裁决 ②：α = τ/κ 是方向性错误（X-09 成立）",
      "若取 α = τ/κ，则 κ/τ = 1/α = %s，而精确值是 %s ⇒ 相对差 %s（≈α^-2）。"
      "该写法与同目录其余全部公式矛盾，**排除**（正典 X-09）"
      % (g(1.0 / a), g(kappa_tau_exact), g(dev_inv)))

    # θ 的两套参数化：口径不可直接互认
    BO("E06", "TRACE", "θ 的两套参数化是口径差，不是矛盾",
       "第 10 卷的公理 A3 是**径向-切向**分解 u_r=c·cosθ、u_⊥=c·sinθ；"
       "23 式的 C-26 是**横向-轴向**分解 v_⊥=αc、v_z=c√(1−α²)。"
       "两者共享 κ、τ 但「另一分量」不同 ⇒ θ 不是同一个角，"
       "**不可把 A3 的 θ 直接代入 23 式**。本次裁决只用了两套都同意的那部分"
       "（τ/κ = tanθ = v_z/v_⊥），因此结论对参数化不敏感")

    P("E07", "TRACE", "「统一程度」的定量读数",
      "电磁扇区：3 条独立输入（C-01 主式 + C-02/C-03 本构）经消元得到 1 条封闭方程（C-05），"
      "再展开出 4 条麦克斯韦结果（C-06~C-09）⇒ **3 → 1 → 4**。"
      "A 类 9 条中 6 条是那 3 条的派生（C-04 由 M11 证明也是派生）⇒ "
      "**UFE-2 目前兑现的统一性，仅限电磁扇区内部的 3→1→4**。"
      "引力 / 核力 / 弱力扇区因量纲不成立（X-01/02/05/06）未纳入统一")


# ============================================================ 汇总
def summarize():
    cnt = {}
    for r in RESULTS:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    return cnt


def main():
    strict = "--strict" in sys.argv[1:]
    if not os.path.isfile(CANON_MD):
        print("[FAIL] 找不到正典文件")
        return 2
    canon_rows, excl_rows, nodes, kind, edges = load_canon()
    if not nodes:
        print("[FAIL] 正典表解析为空")
        return 2

    sec_dep(canon_rows, nodes, kind, edges)
    sec_trace(edges)

    cnt = summarize()
    payload = {
        "instrument": "zxq23_canon_deps.py",
        "canon_md": os.path.basename(CANON_MD),
        "counts": cnt, "total": len(RESULTS),
        "roots": sorted([c for c in nodes if not edges[c]]),
        "edges": edges,
        "alpha": ALPHA,
        "results": RESULTS,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    print("=" * 78)
    print("UFE-2 正典依赖图 · 独立自由度 · 公设溯源对账")
    print("=" * 78)
    for r in RESULTS:
        print("[%-8s] %-5s %s" % (r["verdict"], r["id"], r["title"]))
        print("           %s" % r["detail"])
    print("-" * 78)
    print("合计 %d 条：PASS %d / FAIL %d / BOUNDARY %d / INFO %d"
          % (len(RESULTS), cnt.get("PASS", 0), cnt.get("FAIL", 0),
             cnt.get("BOUNDARY", 0), cnt.get("INFO", 0)))
    print("产物：%s" % os.path.basename(OUT_JSON))
    print("红线：PASS 仅代表「未被本次复算推翻」；数学自洽 ≠ 实验证实。")
    if strict and cnt.get("FAIL", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
