# -*- coding: utf-8 -*-
"""
跨册门禁回查：并行分支真实比较论断合规性（2026-10-07）

目的：把 F4+E9 gate 应用到「本支线其他并行审计册」里的真实跨力/跨类比较论断，
验证门禁判定与这些册自身的人工裁定一致（它们已自发标记 混标度 / 口径 缺陷）。

来源（均为本支线并行审计册，read-only 抽取）：
  - ADD-01R 外部审计 C08：α_em(0) vs α_em(M_Z) 相对差 7.10% → 混标度
  - 整理复核 N7：α_s/α_em 取 M_Z 口径、α_G 取电子口径 → 同表混口径
  - 修复方案 攻破 C-01：α(0) 与 α_s(M_Z) 同表 → 能标口径未统一
  - 修复版验收 D-03：α_G 采用电子参考并标注参考质量（合规写法，统一 M_Z 后 span 33.3 dex）

纯标准库；EXIT=0。
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GATE_PATH = os.path.join(HERE, "跨册门禁_F4范畴与E9能标一致性校验器_2026-10-07.py")
spec = importlib.util.spec_from_file_location("f4e9gate", GATE_PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
check_table = gate.check_table
G_NAT, M_Z, M_E = gate.G_NAT, gate.M_Z, gate.M_ELECTRON


def scenario_list():
    return [
        {
            "id": "P1_ADD01R_C08_mixed_alphaem_scale",
            "src": "ADD-01R 外部审计 C08（混标度）",
            "desc": "α_em(0)=7.297e-3 与 α_em(M_Z)=7.815e-3 同表（零能标 vs M_Z 口径）",
            "expect": "FAIL",
            "items": [
                {"name": "α_em(0)", "coupling": 7.2973526e-3, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1e-6},
                {"name": "α_em(M_Z)", "coupling": 7.8154308e-3, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
            ],
        },
        {
            "id": "P2_N7_fourforce_mixed_scale",
            "src": "整理复核 N7（同表混口径）",
            "desc": "四力表：α_s/α_em 取 M_Z 口径、α_G 取电子口径",
            "expect": "FAIL",
            "items": [
                {"name": "α_s(M_Z)", "coupling": 0.1179, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α_em(M_Z)", "coupling": 7.815e-3, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α_G(电子)", "coupling": 1.7518e-45, "mass_dim": -2, "kind": "gravity",
                 "scale_GeV": M_E, "converted": True},
            ],
        },
        {
            "id": "P3_fix_C01_alpha0_vs_alphas",
            "src": "修复方案 攻破 C-01（能标口径未统一）",
            "desc": "α(0)=7.297e-3 与 α_s(M_Z)=0.1179 同表",
            "expect": "FAIL",
            "items": [
                {"name": "α(0)", "coupling": 7.297e-3, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1e-6},
                {"name": "α_s(M_Z)", "coupling": 0.1179, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
            ],
        },
        {
            "id": "P4_fix_D03_declared_correct",
            "src": "修复版验收 D-03（合规写法）",
            "desc": "α_G 化 α_G(M_Z) 并同标度 + 规范力 @M_Z（声明参考质量、统一口径）",
            "expect": "PASS",
            "items": [
                {"name": "α_s(M_Z)", "coupling": 0.1179, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α_em(M_Z)", "coupling": 7.815e-3, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α_G(M_Z)", "coupling": gate.alpha_G(M_Z), "mass_dim": -2, "kind": "gravity",
                 "scale_GeV": M_Z, "converted": True},
            ],
        },
    ]


def main():
    scenarios = scenario_list()
    results = []
    n_match = 0
    for s in scenarios:
        v = check_table(s["id"], s["items"])
        match = (v["overall"] == s["expect"])
        n_match += 1 if match else 0
        results.append({
            "id": s["id"], "src": s["src"], "desc": s["desc"],
            "expect": s["expect"], "got": v["overall"], "match": match,
            "F4": v["F4"]["status"], "E9": v["E9"]["status"],
            "E9_spread_dex": v["E9"]["spread_dex"],
            "violations": v["F4"]["violations"] + v["E9"]["violations"],
        })
    summary = {
        "tag": "跨册门禁_回查并行分支比较合规",
        "scenarios": len(scenarios),
        "gate_agrees_with_prior": n_match,
        "all_match": n_match == len(scenarios),
        "details": results,
    }
    out_json = os.path.join(HERE, "..", "数据", "跨册门禁_回查并行分支比较合规_2026-10-07.json")
    out_md = os.path.join(HERE, "..", "数据", "跨册门禁_回查并行分支比较合规_2026-10-07.md")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    lines = []
    lines.append("# 跨册门禁_回查并行分支比较合规（回归自检产物）\n")
    lines.append("场景 %d / 门禁与先前人工裁定一致 %d / 全一致 %s\n" % (len(scenarios), n_match, summary["all_match"]))
    lines.append("\n## 逐条\n")
    for r in results:
        lines.append("- **%s**（%s）：期望 %s / 门禁 %s / %s" % (r["id"], r["src"], r["expect"], r["got"], "✓一致" if r["match"] else "✗不一致"))
        lines.append("  - %s" % r["desc"])
        lines.append("  - F4=%s；E9=%s（spread=%s）" % (r["F4"], r["E9"], r["E9_spread_dex"]))
        for viol in r["violations"]:
            lines.append("    - [%s] %s" % (viol["item"], viol["reason"]))
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("场景 %d / 一致 %d / 全一致 %s" % (len(scenarios), n_match, summary["all_match"]))
    for r in results:
        print("  %-34s expect=%-6s got=%-6s %s" % (r["id"], r["expect"], r["got"], "OK" if r["match"] else "MISMATCH"))
    print("EXIT=0")


if __name__ == "__main__":
    main()
