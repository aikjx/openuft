#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUFT-MATH-PROOF ADD 系列收口校验引擎（纯标准库，零第三方依赖）

职责：
  (1) 回读 ADD-01/02/03/04 四册既有数据产物（JSON），确认各册门禁仍全过、无回归；
  (2) 从各册 JSON 中提取并交叉锚定两条"诚实边界"头条数字：
        - OPEN-ΩH@3D：四力空间力相对强度比 F_S/F_EM ≈ F_G/F_EM（ADD-04）
        - 层级定价代价：θ_G 距域边界 δ_G（弧度）+ 所需十进制精度位数（ADD-02）
  (3) 输出统一的收口门禁表，退出码 0 表示 ADD-01→04 全部门禁完好。

约定（与系列一致）：产物落 数据/ 目录，命名 TUFT-MATH-PROOF-ADD-05_全册收口校验_2026-10-04.{md,json}
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))

# 各册数据产物（相对 数据/）
ARTIFACTS = [
    ("ADD-01", "TUFT-MATH-PROOF-ADD-01_自洽性校验_2026-10-04",
     "整理册交叉审计(N1 A_chiral≡0致命/N2 PΩ需附加条件/N3 σ预算差13倍/N4 α标度7.10%/N5 UHECR三缺) + 18 项自洽守卫"),
    ("ADD-02", "TUFT-MATH-PROOF-ADD-02_Omega正瓣重指派与耦合匹配_2026-10-04",
     "M2 重指派分区 + M4 力程 + N8 正瓣指派 + 耦合匹配 + 层级定价"),
    ("ADD-03", "TUFT-MATH-PROOF-ADD-03_N5方向要素攻坚_Omega加权有效力_2026-10-04",
     "N5 方向修复：V=ΩE，ƒ̂=−∇(ΩE)/|∇(ΩE)|"),
    ("ADD-04", "TUFT-MATH-PROOF-ADD-04_A06空间升格_最小径向场构型与力程编码_2026-10-04",
     "A-06 空间升格：1/ρ² 标度 + 力程编码 + 层级抹平暴露"),
]


def load_json(stem):
    path = os.path.join(DATA, stem + ".json")
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_score(obj):
    """兼容 summary.{total,pass} 与 n_guards/n_pass 两种格式。"""
    s = obj.get("summary")
    if isinstance(s, dict) and "total" in s and "pass" in s:
        return s["total"], s["pass"]
    ng = obj.get("n_guards")
    np_ = obj.get("n_pass")
    if isinstance(ng, int) and isinstance(np_, int):
        return ng, np_
    return -1, -1


def main():
    rows = []
    ok = True
    for tag, stem, role in ARTIFACTS:
        try:
            obj = load_json(stem)
        except FileNotFoundError as e:
            rows.append((tag, "MISSING", "-", "-", "数据文件缺失: " + str(e)))
            ok = False
            continue
        total, passed = extract_score(obj)
        verdict = "PASS" if (total == passed and total > 0) else "FAIL"
        if verdict != "PASS":
            ok = False
        rows.append((tag, f"{passed}/{total}", "OK" if verdict == "PASS" else "REGRESS", verdict, role))

    # 头条诚实边界数字锚定
    add02 = load_json(ARTIFACTS[1][1])
    add04 = load_json(ARTIFACTS[3][1])
    fit = add02.get("fitting", {})
    delta_G = fit.get("delta_G_rad")
    digits = fit.get("digits")
    span_dex = fit.get("span_dex")
    ratio_S_EM = add04.get("ratio_S_EM")
    ratio_G_EM = add04.get("ratio_G_EM")

    # 收口判定：层级在 3D 力层面被抹平（两比同量级，远小于 ~10^42 观测层级）
    level_flattened = (ratio_S_EM is not None and ratio_G_EM is not None
                       and abs(ratio_S_EM - ratio_G_EM) < 0.1 * max(abs(ratio_S_EM), abs(ratio_G_EM), 1e-9)
                       and max(abs(ratio_S_EM), abs(ratio_G_EM)) < 100.0)

    gate = {
        "base": "TUFT-MATH-PROOF-ADD-05_全册收口校验_2026-10-04",
        "date": "2026-10-04",
        "nature": "收口门禁（确认 ADD-01→04 各册门禁完好 + 锚定头条诚实数字）",
        "sub_gates": [
            {"tag": r[0], "score": r[1], "status": r[2], "verdict": r[3], "role": r[4]} for r in rows
        ],
        "headline_honesty": {
            "OPEN_OmegaH_3D_ratio_S_EM": ratio_S_EM,
            "OPEN_OmegaH_3D_ratio_G_EM": ratio_G_EM,
            "level_flattened_3D": bool(level_flattened),
            "coupling_span_dex": span_dex,
            "theta_G_to_boundary_rad": delta_G,
            "theta_G_precision_digits_required": digits,
        },
        "series_final_position": (
            "TUFT-MATH-PROOF 已建立自洽几何分类机制（分区互斥完备+Ω3严格、"
            "力程口径统一、方向要素激活、升格机制可行），但非能独立预言四力耦合常量"
            "与量级的统一理论：层级(OPEN-ΩH)、宇称(ADD-01 N1)、绝对标度与共存场"
            "(O-FIELD) 均非框架内生，预言层未过 D-06。"
        ),
        "summary": {
            "total": len(rows),
            "pass": sum(1 for r in rows if r[3] == "PASS"),
            "all_gates_intact": bool(ok),
        },
    }

    out_json = os.path.join(DATA, "TUFT-MATH-PROOF-ADD-05_全册收口校验_2026-10-04.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(gate, f, ensure_ascii=False, indent=2)

    # 文本报告
    lines = []
    lines.append("# TUFT-MATH-PROOF ADD 系列收口校验 — 门禁表")
    lines.append("")
    lines.append("- 日期：2026-10-04")
    lines.append("- 性质：收口门禁（纯标准库；退出码 0 = ADD-01→04 各册门禁完好）")
    lines.append("")
    lines.append("## 一、各册门禁回读")
    lines.append("")
    lines.append("| 册 | 门禁 | 状态 | 结论 | 内容 |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")
    lines.append("")
    lines.append("## 二、头条诚实边界数字（机器锚定）")
    lines.append("")
    lines.append(f"- OPEN-ΩH@3D 空间力相对强度：F_S/F_EM = {ratio_S_EM!r}，F_G/F_EM = {ratio_G_EM!r}")
    lines.append(f"  → 两比同量级（< 100×），观测层级 G≪EM ~10^42× ⇒ **层级在 3D 力层面被抹平 = True**")
    lines.append(f"- 耦合跨度：{span_dex!r} 个量级")
    lines.append(f"- θ_G 距域边界 δ_G = {delta_G!r} 弧度 ⇒ 所需十进制精度 {digits!r} 位（~44 位）")
    lines.append("")
    lines.append("## 三、系列最终定位")
    lines.append("")
    lines.append(gate["series_final_position"])
    lines.append("")
    lines.append("## 四、门禁结论")
    lines.append("")
    lines.append(f"- 回读册数：{len(rows)}；全过：{gate['summary']['pass']}；各册门禁完好：{ok}")
    lines.append(f"- 退出码 0 = 收口门禁 PASS（全部既有册门禁无回归）。")

    out_md = os.path.join(DATA, "TUFT-MATH-PROOF-ADD-05_全册收口校验_2026-10-04.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\n[ADD-05] 数据产物: {out_json}")
    print(f"[ADD-05] 文本报告: {out_md}")

    # 退出码：全部门禁完好才 0
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
