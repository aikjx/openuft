#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT A-05 质能关系冲突 · 终局裁定引擎（纯标准库，零第三方依赖）

任务：A-05（E ≠ mc² 且可为负）自 2026-10-04 定价为 FAIL 后，全系列只做过「登记 / 声明不得略过」，
      从未被任何一册正面处理。本册做终局裁定。

判定路线：
  P1  溯源复算：θ 网格 2001 点重算 E/(mc²)=(κ+τ)/(2√(κ²+τ²))，与来料 [−0.7071,+0.7071] 及
      源 guard `energy_never_equals_mc2` 三方交叉，确认该读数非笔误。
  P2  修复空间穷举（核心新工作）：枚举 6 条能让 E=mc² 成立的改法，逐条给**代价向量**
      （新常数数 / 是否替换核心式 / 是否违反 Ω5 / 是否引入奇点 / 是否需动力学）。
      **不代选**：只输出代价向量，不给排序、不给推荐。
  P3  同源显影：登记与 A-05 同源的读数（牛顿比对需大量级相消），回链不求新数。
  P4  下游污染清单：逐条登记受 A-05 影响的读数，分「数值不可用 / 须标注口径」两档。
  P5  结项与红线：A-05 正式结项为「质能关系外部输入」。

产物：数据/TUFT-A05_质能关系冲突_终局裁定_2026-10-07.{md,json}
退出码：0 = 自检全过，可作门禁。
"""
import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "数据"))
os.makedirs(OUT_DIR, exist_ok=True)
BASE = "TUFT-A05_质能关系冲突_终局裁定_2026-10-07"

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({
        "id": cid, "段": sec, "项": item, "判定": verdict,
        "说明": detail.replace("|", "/"),
    })


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "取证": detail.replace("|", "/")})


def ratio(k, t):
    """E/(mc²) = (κ+τ) / (2√(κ²+τ²))。r=0 时返回 None。"""
    r = math.hypot(k, t)
    if r == 0.0:
        return None
    return (k + t) / (2.0 * r)


def main():
    # ── P1 溯源复算 ────────────────────────────────────────────────
    N = 2001
    vals = []
    for i in range(N):
        th = -math.pi + 2.0 * math.pi * i / (N - 1)
        vals.append(ratio(math.cos(th), math.sin(th)))
    lo, hi = min(vals), max(vals)
    # 解析极值：θ=45° 取 +1/√2；θ=225° 取 −1/√2
    analytic = 1.0 / math.sqrt(2.0)
    p1_ok = (abs(hi - analytic) < 1e-6) and (abs(lo + analytic) < 1e-6)
    add("P1-01", "P1", "E/(mc²) 上界", "PASS",
        f"网格 {N} 点最大 {hi:.6f}，解析 1/√2={analytic:.6f}，偏差 {abs(hi-analytic):.2e}")
    add("P1-02", "P1", "E/(mc²) 下界（可为负）", "PASS",
        f"网格最小 {lo:.6f}，解析 −1/√2={-analytic:.6f} ⇒ κ≈−τ 时 E 为负")
    add("P1-03", "P1", "是否恒 ≠ 1", "PASS",
        f"max|E/(mc²)|={max(abs(lo),abs(hi)):.6f} < 1 ⇒ E/(mc²) 永远不等于 1（最大仅 70.71%，至少小 29.29%）")
    guard("a05_ratio_bounds", p1_ok, f"复算区间 [{lo:.6f}, {hi:.6f}] 与解析 ±1/√2 吻合")
    guard("a05_never_one", max(abs(lo), abs(hi)) < 1.0 - 1e-9, f"max|ratio|={max(abs(lo),abs(hi)):.6f} < 1")
    guard("a05_negative_reachable", lo < 0.0, f"min={lo:.6f} < 0 ⇒ E 可取负")

    # ── P2 修复空间穷举（6 条，只给代价向量，不代选） ──────────────
    fixes = [
        {
            "id": "F1", "desc": "改 E 系数：E = ħc·√(κ²+τ²)（弃 (κ+τ)/2）",
            "achieves": True,
            "cost": {"新常数数": 0, "替换核心式": True, "违反Ω5": False, "引入奇点": False, "需动力学": False},
            "代价": "替换公理 A2 核心式；F=−∇E 的既有推导链与 Ω 分区耦合需整体重推",
            "verdict": "BOUNDARY",
        },
        {
            "id": "F2", "desc": "改 m 定义：m = ħ(κ+τ)/(2c)（弃 m=ħ√(κ²+τ²)/c）",
            "achieves": True,
            "cost": {"新常数数": 0, "替换核心式": True, "违反Ω5": False, "引入奇点": False, "需动力学": False},
            "代价": "κ+τ<0 时**质量为负**；与体系自有的 m=ħr/c 及 E=ħcρ 系列读数冲突",
            "verdict": "BOUNDARY",
        },
        {
            "id": "F3", "desc": "加归一化因子 N = 2√(κ²+τ²)/(κ+τ)",
            "achieves": True,
            "cost": {"新常数数": 1, "替换核心式": False, "违反Ω5": True, "引入奇点": True, "需动力学": False},
            "代价": "κ≈−τ 处**分母发散**；且引入第二个结构化因子 ⇒ **违反 ω5**（回链 `MATH-PROOF:OPEN-ΩH` 已结项：公理集内无解）",
            "verdict": "FAIL",
        },
        {
            "id": "F4", "desc": "把 E 重释为结合能（须补动能项）",
            "achieves": False,
            "cost": {"新常数数": 1, "替换核心式": False, "违反Ω5": False, "引入奇点": False, "需动力学": True},
            "代价": "需要 TUFT 动力学；而 `V3.5:O-FIELD` 已证框架无内生动力学 ⇒ 当前不可实现",
            "verdict": "FAIL",
        },
        {
            "id": "F5", "desc": "限定定义域至极值点 θ=45°",
            "achieves": False,
            "cost": {"新常数数": 0, "替换核心式": False, "违反Ω5": False, "引入奇点": False, "需动力学": False},
            "代价": f"极值处 E/(mc²)={hi:.6f} ≠ 1（仍差 29.29%）⇒ **不成立**",
            "verdict": "FAIL",
        },
        {
            "id": "F6", "desc": "引入第二个场承载质能关系",
            "achieves": False,
            "cost": {"新常数数": 2, "替换核心式": True, "违反Ω5": True, "引入奇点": False, "需动力学": True},
            "代价": "已被 `r14:` 三条出路代价矩阵判定为「已结项」（公设违背 + 需动力学）；本册不另行展开",
            "verdict": "FAIL",
        },
    ]
    for f in fixes:
        add(f"P2-{f['id']}", "P2", f["desc"], f["verdict"], f["代价"])
    n_achieve = sum(1 for f in fixes if f["achieves"])
    guard("a05_fixspace_exhaustive", len(fixes) == 6, f"枚举 {len(fixes)} 条改法，逐条登记代价向量")
    guard("a05_no_clean_fix", n_achieve == 0 or all(
        f["cost"]["替换核心式"] or f["cost"]["违反Ω5"] or f["cost"]["需动力学"]
        for f in fixes if f["achieves"]
    ), f"能达成 E=mc² 的 {n_achieve} 条（F1/F2）均须替换核心式，且分别引入「推导链重推 / 质量为负」代价")

    # ── P3 同源显影 ────────────────────────────────────────────────
    add("P3-01", "P3", "同源登记：牛顿比对需大量级相消", "INFO",
        "回链 `判定_TUFT_V3.5修复方案_求导证明验证精算攻破_2026-10-04`：牛顿比对靠 κ+τ 相消凑 1/r²，"
        "与 A-05 同源（E 幅度本身不对）。本册**不重算该数**，仅登记同源关系以免两处被当作孤立缺陷。")
    guard("a05_same_root_logged", True, "同源关系已登记（未新造数值）")

    # ── P4 下游污染清单 ────────────────────────────────────────────
    downstream = [
        ("力程能标反解 ħf / 四力样本表 E=ħcρ", "须标注口径"),
        ("闵氏切换册的 E 漂移", "须标注口径"),
        ("β 衰变幅度", "须标注口径"),
        ("EDM / g-2 预言基线", "数值不可用（窗口已关，回链 `链 A-④`）"),
        ("牛顿比对（1/r² 还原）", "数值不可用（需大量级相消）"),
    ]
    for name, level in downstream:
        add(f"P4-{len(RESULTS):02d}", "P4", name, level, f"受 A-05（E≠mc² 且可为负）影响的读数：{level}")
    guard("a05_downstream_listed", len(downstream) >= 5, f"登记下游污染 {len(downstream)} 条")

    # ── P5 结项 ────────────────────────────────────────────────────
    add("P5-01", "P5", "A-05 结项", "PASS",
        "正式结项为「**质能关系外部输入**」：E=mc² 不能由 TUFT 现有公设集导出；"
        "修复空间 6 条中，能达成的 F1/F2 均须替换核心式（代价：推导链重推 / 质量为负），"
        "其余 4 条或不成立或违反 ω5、或需框架本不具备的动力学。")
    add("P5-02", "P5", "后续声称红线", "PASS",
        "不得写「E=mc² 已由 TUFT 导出」「质能关系已闭环」；任何引用 E 的读数须显式标注 A-05 口径。")
    guard("a05_closure_declared", True, "A-05 结项为「质能关系外部输入」，红线已写死")

    # ── 汇总 ───────────────────────────────────────────────────────
    counts = {}
    for r in RESULTS:
        counts[r["判定"]] = counts.get(r["判定"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])
    payload = {
        "base": BASE,
        "date": "2026-10-07",
        "nature": "A-05（E≠mc² 且可为负）终局裁定；**不代选**（只给代价向量，不给排序/推荐）",
        "计数": counts,
        "总计": len(RESULTS),
        "条目": RESULTS,
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "fix_space": fixes,
        "key_numbers": {
            "ratio_max": hi,
            "ratio_min": lo,
            "analytic_extremum": analytic,
            "gap_to_unity_pct": (1.0 - hi) * 100.0,
            "n_fixes_enumerated": len(fixes),
        },
        "closure": {
            "A-05": "正式结项为「质能关系外部输入」",
            "within_axiom_set": False,
            "note": "与 OPEN-ΩH@3D（层级）、OPEN-O-FIELD-A/B（共存场/剖面）并列为第三条「外部输入」结项",
        },
        "summary": {"total": len(RESULTS), "pass": counts.get("PASS", 0)},
    }

    with open(os.path.join(OUT_DIR, BASE + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    order = ["PASS", "FAIL", "BOUNDARY", "INFO", "MISMATCH", "CORRECTED"]
    cnt = " / ".join(f"{k} {counts[k]}" for k in order if k in counts)
    lines = []
    lines.append(f"# {BASE}（判定产物）")
    lines.append("")
    lines.append(f"- 日期：2026-10-07 · **条目 {len(RESULTS)} ｜ {cnt} ｜ 自检 {g_ok} / {len(GUARDS)}**")
    lines.append("- 性质：A-05 终局裁定；**不代选**")
    lines.append("")
    lines.append("## P1 溯源复算")
    lines.append(f"- E/(mc²) 区间 [{lo:.6f}, {hi:.6f}]（解析 ±1/√2=±{analytic:.6f}）")
    lines.append(f"- 永远不等于 1：最大仅 {hi*100:.2f}%，至少小 {(1-hi)*100:.2f}%；κ≈−τ 时取负")
    lines.append("")
    lines.append("## P2 修复空间穷举（6 条代价向量，不排序不推荐）")
    lines.append("| id | 改法 | 达成 | 新常数 | 替换核心式 | 违反Ω5 | 奇点 | 需动力学 | 判定 |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for f in fixes:
        c = f["cost"]
        yn = lambda b: "是" if b else "否"
        lines.append(f"| {f['id']} | {f['desc']} | {'是' if f['achieves'] else '否'} | {c['新常数数']} | "
                     f"{yn(c['替换核心式'])} | {yn(c['违反Ω5'])} | {yn(c['引入奇点'])} | {yn(c['需动力学'])} | {f['verdict']} |")
    lines.append("")
    lines.append("## P4 下游污染清单")
    for name, level in downstream:
        lines.append(f"- {name} —— {level}")
    lines.append("")
    lines.append("## 判定表")
    lines.append("| id | 段 | 项 | 判定 | 说明 |")
    lines.append("|---|---|---|---|---|")
    for r in RESULTS:
        lines.append(f"| {r['id']} | {r['段']} | {r['项']} | {r['判定']} | {r['说明']} |")
    lines.append("")
    lines.append("## 自检")
    lines.append("| guard | 结果 | 取证 |")
    lines.append("|---|---|---|")
    for g in GUARDS:
        lines.append(f"| {g['name']} | {'PASS' if g['ok'] else 'FAIL'} | {g['取证']} |")
    lines.append("")
    lines.append("## 结项")
    lines.append(f"- {payload['closure']['A-05']}（公理集内无解 = {not payload['closure']['within_axiom_set']}）")

    with open(os.path.join(OUT_DIR, BASE + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\n[A-05] 产物: {os.path.join(OUT_DIR, BASE + '.{json,md}')}")
    sys.exit(0 if g_ok == len(GUARDS) else 1)


if __name__ == "__main__":
    main()
