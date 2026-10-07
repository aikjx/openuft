# -*- coding: utf-8 -*-
"""
跨册门禁回查：用 F4+E9 gate 复核本支线已产出审计册中的真实比较论断（2026-10-07）

目的：把 gate 当作回归自检器——抽取本支线真实审计册里的跨力/跨类比较场景，
逐一跑 check_table，比对「门禁判定」与「先前人工裁定」是否一致。

覆盖来源（均为本支线已落地产物，read-only 抽取）：
  - 四力本源 F1：α₂(M_Z) 与 α_em(M_Z) 同标度同范畴比较 → 先前裁定：方法合规（物理结论弱>电磁）
  - 四力本源 F4：四力强度表把引力(原始 G) 与三规范力并列 → 先前裁定：F4 FAIL（范畴混装）
  - 能标重算 T2 / ESCAPE E9：ADD-02 四力表混用能标 → 先前裁定：E9 FAIL（混标）
  - 四力本源 F4（正确化法）：α_G 化 α_G(M_Z) 与规范力同标度 → 先前裁定：方法合规
  - 四力本源 F6/F7：SM/MSSM 三规范耦合同取 M_Z → 先前裁定：方法合规（是否共点是另一物理问题）

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
            "id": "S1_textbook_rawG",
            "src": "四力本源 F4 / ESCAPE-AUDIT E9",
            "desc": "教科书四力强度表：原始带量纲 G 直接与三规范力并列",
            "expect": "FAIL",
            "items": [
                {"name": "强", "coupling": 1.0, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1.0},
                {"name": "电磁", "coupling": 1e-2, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1.0},
                {"name": "弱", "coupling": 1e-5, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1.0},
                {"name": "引力(raw G)", "coupling": G_NAT, "mass_dim": -2, "kind": "gravity",
                 "scale_GeV": None, "converted": False},
            ],
        },
        {
            "id": "S2_ADD02_mixed_scale",
            "src": "能标重算 T2 / ESCAPE-AUDIT E9",
            "desc": "ADD-02 四力耦合表：α_s@M_Z / α_weak@M_Z / α_em@零能标 / α_G@电子",
            "expect": "FAIL",
            "items": [
                {"name": "α_s", "coupling": 0.1179, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α_weak", "coupling": 0.01696, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α_em(零能标)", "coupling": 7.297e-3, "mass_dim": 0, "kind": "gauge", "scale_GeV": 1e-6},
                {"name": "α_G(电子标度)", "coupling": 1.75e-45, "mass_dim": -2, "kind": "gravity",
                 "scale_GeV": M_E, "converted": True},
            ],
        },
        {
            "id": "S3_alpha2_vs_alphaem_MZ",
            "src": "四力本源 F1",
            "desc": "α₂(M_Z) 与 α_em(M_Z) 比较（同范畴同标度）→ 弱在高能强于电磁",
            "expect": "PASS",
            "items": [
                {"name": "α₂(M_Z)", "coupling": 0.03380, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α_em(M_Z)", "coupling": 0.007816, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
            ],
        },
        {
            "id": "S4_alphaG_conv_MZ",
            "src": "四力本源 F4（正确化法）",
            "desc": "α_G 先化 α_G(M_Z) 再与规范力同标度并列（合规写法）",
            "expect": "PASS",
            "items": [
                {"name": "α₁(M_Z)", "coupling": 0.01694, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α₂(M_Z)", "coupling": 0.03380, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α_G(M_Z)", "coupling": gate.alpha_G(M_Z), "mass_dim": -2, "kind": "gravity",
                 "scale_GeV": M_Z, "converted": True},
            ],
        },
        {
            "id": "S5_SM_three_at_MZ",
            "src": "四力本源 F6 / F7",
            "desc": "SM/MSSM 三规范耦合同取 M_Z（方法合规；是否共点是另一物理问题）",
            "expect": "PASS",
            "items": [
                {"name": "α₁(M_Z)", "coupling": 0.01694, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α₂(M_Z)", "coupling": 0.03380, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
                {"name": "α₃(M_Z)", "coupling": 0.1179, "mass_dim": 0, "kind": "gauge", "scale_GeV": M_Z},
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
        "tag": "跨册门禁_回查本支线比较合规",
        "scenarios": len(scenarios),
        "gate_agrees_with_prior": n_match,
        "all_match": n_match == len(scenarios),
        "details": results,
    }
    out_json = os.path.join(HERE, "..", "数据", "跨册门禁_回查本支线比较合规_2026-10-07.json")
    out_md = os.path.join(HERE, "..", "数据", "跨册门禁_回查本支线比较合规_2026-10-07.md")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    lines = []
    lines.append("# 跨册门禁_回查本支线比较合规（回归自检产物）\n")
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
        print("  %-22s expect=%-6s got=%-6s %s" % (r["id"], r["expect"], r["got"], "OK" if r["match"] else "MISMATCH"))
    print("EXIT=0")


if __name__ == "__main__":
    main()
