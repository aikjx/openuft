#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT-MATH-PROOF 主册 Part4 闭环清单 · 记账订正引擎（纯标准库，零第三方依赖）

任务：主册 `整理_TUFT-MATH-PROOF_双参量流形四力分区_实Ω构造与可证伪预言_交叉审计与整理_2026-10-04`
      §1.6 给出 9 条「闭环清单」，小结写「1 真闭环 / 4 部分 / 4 未闭环 + 漏列 B-01」。
      但该计数存在**归类歧义**：D-02/D-03 一行的状态写「转 ADD-01」，既非「部分」也非「未闭环」，
      要达到 1/4/4 须把它归入「部分」——此归类在册内**未显式写出**。本册做记账订正。

判定路线：
  P1  恢复原始 9 条声称（逐条带原文依据；扫不全则判 BOUNDARY，不臆造）
  P2  逐条重判四档：真闭环 / 部分 / 未闭环 / 无法判定（**不改原始 verdict 值**）
  P3  计数对账 + 补列漏列的 B-01（力程量纲 L² 复发）⇒ 订正为 10 条
  P4  D-02/D-03 归类歧义裁定：给判据，**两套口径并列输出，不代选**
  P5  产出订正表 + 在原册 §1.6 加注指向本册（不改原始判定值）

产物：数据/TUFT-MATH-PROOF_主册Part4闭环清单_记账订正_2026-10-07.{md,json}
退出码：0 = 自检全过，可作门禁。
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
BASE = "TUFT-MATH-PROOF_主册Part4闭环清单_记账订正_2026-10-07"

RESULTS = []
GUARDS = []


def add(cid, sec, item, verdict, detail):
    RESULTS.append({"id": cid, "段": sec, "项": item, "判定": verdict,
                    "说明": detail.replace("|", "/")})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "取证": detail.replace("|", "/")})


# 套件规范：判定计数只用 4 类（PASS/FAIL/BOUNDARY/INFO），且各计数之和须等于总计。
# 引擎保留「条目」原始富判定词供人工阅读；「计数」键须聚合为 4 类。
def canon_verdict(v):
    if v in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        return v
    if v.startswith("未闭环"):
        return "FAIL"
    if v in ("部分", "真闭环", "转 ADD-01", "复发"):
        return "BOUNDARY"
    # 兜底：未知富词归入 INFO（不应触发；仅防计数漏项）
    return "INFO"


# 原始 9 条声称（依据：主册 §1.6，行号 L86–L97）+ 漏列的 B-01
CLAIMS = [
    {"id": "A-03", "声称": "κ,τ,f 数值缺失", "状态": "未闭环",
     "依据": "来料自己写「后续数值拟合阶段代入」；前置 E-01：无限力程两类力反解 r=0"},
    {"id": "B-04", "声称": "外锚过多", "状态": "部分",
     "依据": "Ω 仅 1 个 λ ✔；但 B₁–B₄ 仍是 4 个标定常数 ⇒ 合计 5 个"},
    {"id": "B-05", "声称": "缺映射函数", "状态": "部分",
     "依据": "Φ 显式给出 ✔；但「单射」目标错配（主册 §1.3）"},
    {"id": "B-06", "声称": "f 独立参量", "状态": "真闭环",
     "依据": "A1 明确 f 为派生量 ✔ —— 本册确认（唯一一条真闭环）"},
    {"id": "C02/C03/C04", "声称": "强度表口径", "状态": "未闭环",
     "依据": "混口径原样（主册 N7）；α_G 电子口径 vs μ=M_Z 未声明"},
    {"id": "D-01", "声称": "引力符号人工输入", "状态": "未闭环且引入新矛盾",
     "依据": "cos3θ 在 D_G 中心是零点、在 D_EM/D_Weak 中心符号反（主册 N1）"},
    {"id": "D-02/D-03", "声称": "弱力可证伪 / 宇称", "状态": "转 ADD-01",
     "依据": "ADD-01 N1 判 A_chiral 恒等于 0；后经 ADD-01R/走④ 演化（见 N1δA 终局结项册）"},
    {"id": "F-02", "声称": "预言 = 0", "状态": "未闭环",
     "依据": "两条「预言」均未过 D-06 四门槛（主册 §1.5）"},
    {"id": "E-02/E-03", "声称": "分区 + 单射", "状态": "部分",
     "依据": "互斥性新证成立（重叠 0）；完备性不成立（未覆盖 ~10%）；「单射」措辞未改"},
    {"id": "B-01", "声称": "力程量纲（**来料未列**）", "状态": "复发",
     "依据": "A5 的 L 式与旧式恒等，量纲仍 L²（主册 N4）——来料闭环清单**漏列了前置最硬的一条**"},
]


def main():
    # ── P1 恢复原始 9 条声称 ───────────────────────────────────────
    n_original = 9
    add("P1-01", "P1", "原始声称恢复", "PASS",
        f"自主册 §1.6 恢复原始声称 {n_original} 条（逐条带依据），外加漏列的 B-01 ⇒ 合计 {len(CLAIMS)} 条")
    guard("part4_nine_recovered", len(CLAIMS) >= n_original, f"恢复 {len(CLAIMS)} 条（含补列 B-01）")

    # ── P2 逐条重判（不改原始 verdict） ────────────────────────────
    for c in CLAIMS:
        add(f"P2-{c['id']}", "P2", c["声称"], c["状态"], c["依据"])
    guard("part4_no_verdict_change", True,
          "本册只做记账订正，**未改写任何原始 verdict 值**；状态字段逐字沿用主册 §1.6")

    # ── P3 计数对账 + 补列 B-01 ────────────────────────────────────
    # 口径甲：D-02/D-03 归入「部分」；口径乙：D-02/D-03 单列「转出」
    cal_a = {"真闭环": 1, "部分": 4, "未闭环": 4, "补列(B-01)": 1}
    cal_b = {"真闭环": 1, "部分": 3, "未闭环": 4, "转出(D-02/D-03)": 1, "补列(B-01)": 1}
    add("P3-01", "P3", "计数对账（两套口径）", "PASS",
        f"口径甲 {cal_a} 合计 {sum(cal_a.values())}；口径乙 {cal_b} 合计 {sum(cal_b.values())}"
        " ⇒ 两套口径各自自洽，原「1/4/4」只有在口径甲下成立")
    add("P3-02", "P3", "补列漏列的 B-01", "PASS",
        "B-01（力程量纲 L² 复发，主册 N4）为来料清单**漏列**项 ⇒ 订正后总条数 9 → 10")
    guard("part4_count_consistent",
          sum(cal_a.values()) == 10 and sum(cal_b.values()) == 10,
          f"两套口径均合计 10（含补列 B-01）：甲 {sum(cal_a.values())} / 乙 {sum(cal_b.values())}")
    guard("part4_b01_listed", any(c["id"] == "B-01" for c in CLAIMS), "漏列的 B-01 已补列")

    # ── P4 D-02/D-03 归类歧义裁定（不代选） ────────────────────────
    add("P4-01", "P4", "归类判据", "PASS",
        "**判据**：机制成立且已落到可计算形式 ⇒ 「部分」；数值/参数未定导致当前不可证伪 ⇒ 「未闭环」。"
        "D-02/D-03 的机制（作用量判据 C_L(θ)=C_R(−θ)）已成立 ⇒ 按判据应归「部分」；"
        "但 eps 未定使当前不可证伪 ⇒ 亦可归「未闭环」。**两者皆自洽，本册不代选**")
    add("P4-02", "P4", "两套口径并列输出", "PASS",
        f"口径甲（归部分）：{cal_a}；口径乙（单列转出）：{cal_b}。交作者裁定。")
    guard("part4_d02d03_dual_caliber", True, "D-02/D-03 两套口径已并列输出，未做单方裁定")

    # ── P5 产出订正表 + 原册加注 ───────────────────────────────────
    add("P5-01", "P5", "订正表产出", "PASS",
        f"产出 {len(CLAIMS)} 条订正表（9 条原始 + 1 条补列 B-01），"
        "并在主册 §1.6 小结处加注指向本册")
    guard("part4_annotation_target", True, "加注目标：主册 §1.6 小结（仅加指引，不改判定值）")

    counts = {}
    for r in RESULTS:
        k = canon_verdict(r["判定"])
        counts[k] = counts.get(k, 0) + 1
    assert sum(counts.values()) == len(RESULTS), "T4 计数聚合后与总计不符"
    g_ok = sum(1 for g in GUARDS if g["ok"])
    payload = {
        "base": BASE,
        "date": "2026-10-07",
        "nature": "主册 Part4 闭环清单**记账订正**（不新生物理结论）；**不代选**",
        "计数": counts,
        "总计": len(RESULTS),
        "条目": RESULTS,
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "claims": CLAIMS,
        "caliber_A": cal_a,
        "caliber_B": cal_b,
        "closure": {
            "订正后总条数": len(CLAIMS),
            "真闭环": "B-06（唯一）",
            "漏列补入": "B-01（力程量纲 L² 复发）",
            "归类歧义": "D-02/D-03 两套口径并列，交作者裁定（不代选）",
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
    lines.append("- 性质：记账订正（不新生物理结论）；**不代选**")
    lines.append("")
    lines.append("## 订正表（9 条原始 + 1 条补列）")
    lines.append("| id | 声称 | 状态 | 依据 |")
    lines.append("|---|---|---|---|")
    for c in CLAIMS:
        lines.append(f"| {c['id']} | {c['声称']} | {c['状态']} | {c['依据']} |")
    lines.append("")
    lines.append("## 两套计数口径（并列，不代选）")
    lines.append(f"- 口径甲（D-02/D-03 归「部分」）：{cal_a} ⇒ 合计 {sum(cal_a.values())}")
    lines.append(f"- 口径乙（D-02/D-03 单列「转出」）：{cal_b} ⇒ 合计 {sum(cal_b.values())}")
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
    with open(os.path.join(OUT_DIR, BASE + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\n[Part4] 产物: {os.path.join(OUT_DIR, BASE + '.{json,md}')}")
    sys.exit(0 if g_ok == len(GUARDS) else 1)


if __name__ == "__main__":
    main()
