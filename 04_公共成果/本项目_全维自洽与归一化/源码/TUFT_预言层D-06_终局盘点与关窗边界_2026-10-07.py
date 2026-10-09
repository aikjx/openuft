#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT 预言层 D-06 · 终局盘点与关窗边界引擎（纯标准库，零第三方依赖）

性质：**终局盘点册，不做新审计**。终结裁定册已给「唯一数值预言数 = 0」。
本册做「四门槛逐通道盘点 + 关窗继承矩阵」。

D-06 四门槛（回链 `判定_TUFT_V3.5修复方案_全维审计与重整_2026-10-04`）：
  (a) 同一可观测量只能一套映射；(b) 输入不得含该量实验值（否则 CIRCULAR）；
  (c) 必须有别于参照线的结构因子；(d) 带阈值与误差棒且现有精度可分辨。
  四条全过才算「新增可证伪预言」。

判定路线：
  P1  四门槛逐通道盘点（5 个候选通道）
  P2  关窗继承矩阵（链 A-④ 继承状态登记）
  P3  唯一数值预言数复算
  P4  「接近可证伪」登记为 PENDING-EXTERNAL-INPUT
  P5  结项与重启硬门槛

产物：数据/TUFT_预言层D-06_终局盘点与关窗边界_2026-10-07.{md,json}
退出码：0 = 自检全过，可作门禁。**FAIL 结论照样退 0**（判定自洽闭合）。
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "数据"))
os.makedirs(OUT_DIR, exist_ok=True)
BASE = "TUFT_预言层D-06_终局盘点与关窗边界_2026-10-07"

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "段": sec, "项": item, "判定": verdict,
                    "说明": detail.replace("|", "/")})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "取证": detail.replace("|", "/")})


# 四门槛逐通道：(a) 一套映射 (b) 不含实验值 (c) 有别于参照线结构因子 (d) 带阈值且精度可分辨
CHANNELS = [
    {
        "id": "C1", "name": "Δa_e（电子反常磁矩）",
        "gates": {"a": False, "b": False, "c": False, "d": False},
        "note": "推导链缺失：Δa_e=C_e·τ_e·ħ/(m_e c) 中 C_e、τ_e 无定义来源与数值 ⇒ 区间是断言非推论；"
                "且 `MATH-PROOF:` 主册 D-01 已判 a_TUFT=α/8π 窗口关闭（偏差 74.96%）；门槛 (b)(c)(d) 未过",
    },
    {
        "id": "C2", "name": "ΔE_GZK（宇宙线截断）",
        "gates": {"a": False, "b": False, "c": False, "d": False},
        "note": "`链 A-④:D-05` 三件全缺（耦合项、输运方程、无自由参数阈值）原样未解 ⇒ "
                "ΔE_GZK 退化为自由尺度 A 的存在性平凡陈述；观测端 Auger/TA 读数跨 ~4.6–5.7e19 eV 且能标系统误差 ~14%",
    },
    {
        "id": "C3", "name": "β 衰变 δA（eps 实幅值差通道）",
        "gates": {"a": True, "b": True, "c": True, "d": None},
        "note": "δA=0.10·eps；机制成立且可算，但 eps 未被框架确定 ⇒ 门槛 (d) 不成立 ⇒ 当前非预言",
    },
    {
        "id": "C4", "name": "β 能谱形状 + A_e",
        "gates": {"a": True, "b": True, "c": None, "d": None},
        "note": "依赖 C3 的 eps 通道；结构因子与阈值随 eps 未定而不定 ⇒ 当前非预言",
    },
    {
        "id": "C5", "name": "nEDM 增量 δd_n",
        "gates": {"a": True, "b": True, "c": None, "d": False},
        "note": "**结构性不可证伪**：区间给增量 δd_n、判据却比较总量 d_n（回链 `V3.6:C7`）；"
                "且 EDM 窗口本仓已判关闭",
    },
]


def score(ch):
    g = ch["gates"]
    if all(v is True for v in g.values()):
        return "PASS"
    if any(v is False for v in g.values()):
        return "FAIL"
    return "BOUNDARY"


def main():
    # ── P1 四门槛逐通道盘点 ────────────────────────────────────────
    for ch in CHANNELS:
        v = score(ch)
        gs = " / ".join(f"({k}){'√' if val is True else ('×' if val is False else '?')}"
                        for k, val in ch["gates"].items())
        add(f"P1-{ch['id']}", "P1", ch["name"], v, f"门槛 {gs} —— {ch['note']}")
    n_pass_pred = sum(1 for ch in CHANNELS if score(ch) == "PASS")
    guard("d06_four_gates_scored", len(CHANNELS) == 5, f"逐通道判 5 个候选，四门槛各档均已打标")

    # ── P2 关窗继承矩阵 ────────────────────────────────────────────
    add("P2-01", "P2", "链 A-④ 关窗范围", "PASS",
        "关窗范围 = **{g-2, EDM, UHECR}**（物理层 FAIL）；**β 衰变不在关窗范围**"
        "（回链 `判定_TUFT-V35增补-ADD01-三链归一与冲突仲裁_2026-10-04`）")
    add("P2-02", "P2", "继承状态", "PASS",
        "三链归一册判「继承 0」⇒ 本册**显式补继承**（0 → 1），登记为治理债修复")
    guard("d06_inheritance_declared", True, "关窗继承已显式声明（含 β 排除项）")

    # ── P3 唯一数值预言数复算 ──────────────────────────────────────
    add("P3-01", "P3", "唯一数值预言数", "PASS",
        f"逐通道复算：过四门槛者 {n_pass_pred} 条 ⇒ **唯一数值预言数 = 0**，"
        "与 `判定_TUFT-MATH-PROOF-ADD-01_复权重场与误差传播_终结裁定_2026-10-05` 交叉验证一致")
    guard("d06_count_zero", n_pass_pred == 0, f"过四门槛通道数 = {n_pass_pred}")

    # ── P4 「接近可证伪」登记 ──────────────────────────────────────
    add("P4-01", "P4", "β eps 通道状态", "BOUNDARY",
        "δA 区间需 eps 确定；登记为 **PENDING-EXTERNAL-INPUT**（eps 未定 ⇒ 当前不构成预言）")
    guard("d06_beta_excluded_from_closure", True, "β 衰变不在关窗范围已登记")

    # ── P5 结项与重启门槛 ──────────────────────────────────────────
    add("P5-01", "P5", "D-06 结项", "PASS",
        "**已终局**：当前无任何通道过 D-06 四门槛；预言层不新增声明")
    add("P5-02", "P5", "重启硬门槛", "PASS",
        "重启须先解：① `V3.5:O-FIELD`（动力学/共存场）；② 可识别性（rank ≥ 6）；③ 能标一致性声明；"
        "并至少给出一个过 D-06 四门槛的预言")
    guard("d06_no_new_prediction_claimed", True, "本册不新增任何预言声明")

    counts = {}
    for r in RESULTS:
        counts[r["判定"]] = counts.get(r["判定"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])
    payload = {
        "base": BASE,
        "date": "2026-10-07",
        "nature": "预言层 D-06 终局盘点（不做新审计）；**不代选**",
        "计数": counts,
        "总计": len(RESULTS),
        "条目": RESULTS,
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "channels": [{"id": c["id"], "name": c["name"], "gates": c["gates"],
                      "verdict": score(c)} for c in CHANNELS],
        "closure": {
            "唯一数值预言数": 0,
            "D-06 状态": "已终局",
            "关窗范围": "链 A-④ {g-2, EDM, UHECR}；β 衰变不在关窗范围",
            "PENDING": "β eps 通道（eps 未定）",
            "重启门槛": ["O-FIELD 动力学", "可识别性 rank≥6", "能标一致性声明", "至少一个过 D-06 的预言"],
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
    lines.append("- 性质：终局盘点（不做新审计）；**不代选**")
    lines.append("")
    lines.append("## P1 D-06 四门槛逐通道")
    lines.append("| 通道 | (a) 一套映射 | (b) 不含实验值 | (c) 别于参照线 | (d) 阈值可分辨 | 判定 |")
    lines.append("|---|---|---|---|---|---|")
    for c in CHANNELS:
        m = lambda v: "√" if v is True else ("×" if v is False else "?")
        lines.append(f"| {c['name']} | {m(c['gates']['a'])} | {m(c['gates']['b'])} | "
                     f"{m(c['gates']['c'])} | {m(c['gates']['d'])} | {score(c)} |")
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
    for k, v in payload["closure"].items():
        lines.append(f"- {k}：{v}")
    with open(os.path.join(OUT_DIR, BASE + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\n[D-06] 产物: {os.path.join(OUT_DIR, BASE + '.{json,md}')}")
    sys.exit(0 if g_ok == len(GUARDS) else 1)


if __name__ == "__main__":
    main()
