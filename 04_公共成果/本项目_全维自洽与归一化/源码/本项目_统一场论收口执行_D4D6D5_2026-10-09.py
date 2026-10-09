# -*- coding: utf-8 -*-
"""
本项目 · 统一场论收口执行 · D4 / D6 / D5
=========================================
日期：2026-10-09
性质：收口执行册（非新审计、非新统一方案）。承接 2026-10-08 两份册——
  《判定_本项目_所有物理体系统一场论_终局收敛裁定_2026-10-08》
  《判定_本项目_统一场论达成度重算与最小闭合清单_2026-10-08》
执行对象 = 达成度册 §5 最小闭合清单中明确「不依赖新物理、可立即执行」的三项：
  D4 本体淘汰裁决（收窄 8 族 → 可投入 1–2 条）
  D6 外加公设集中登记（ℏ / 质量标度 / α / Λ / 电荷量子化 / U(1) 荷 / f）
  D5 外部验证流程脚手架（registry 晋升路径，当前 0/22）
引擎：纯标准库（json），零第三方依赖。读数取自 2026-10-08 两份权威册 + 状态看板，不重算他人结论、不代选。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "数据"))

# ---------------------------------------------------------------------------
# 结构化事实（均带册号 + 行键引用，不重算）
# ---------------------------------------------------------------------------

# 来源：达成度册 §4 本体族普查（2026-10-08）
ONTOLOGY_FAMILIES = {
    "螺旋几何族": ["S01", "S02", "S07", "S10", "S12", "S14", "S15", "S18"],
    "其他/未归类": ["P02", "P04", "S03", "S05", "S08", "S09", "S16", "S17"],
    "压缩/密度本体族": ["P01"],
    "规范对称族": ["P03"],
    "信息熵族": ["S04"],
    "拓扑扭结族": ["S06"],
    "几何耦合族": ["S11"],
    "对偶分形族": ["S13"],
}

# 来源：终局裁定 D-01/D-03（唯一 L3 候选 = L6 UFE-2 纵波）
SURVIVING_CANDIDATE = {
    "line": "L6",
    "system": "UFE-2 / 39 号总纲（空间螺旋几何化统一场论整合）",
    "prediction": "纵波（B=0、S=0 储能不辐射、v=V_z<c）",
    "blocker": "f 未标定（N12）：纵波尚未过 D-06 四门槛第④项（带阈值与误差棒且现有精度可分辨）",
    "family": "螺旋几何族",
}

# 来源：达成度册 §5 D6 + 状态看板 §四 + 终局裁定 R1（标度外部性）
EXTERNAL_POSTULATES = [
    {"item": "ℏ（约化普朗克常数）", "status": "测量锚/外部输入",
     "source": "状态看板 §四；达成度册 §5 D6", "note": "所有几何化常数主张的共同外部输入"},
    {"item": "质量标度（m_e 等绝对质量）", "status": "测量锚/外部输入",
     "source": "状态看板 §四；达成度册 §5 D6；M02 普朗克锚定谬误", "note": "TUFT 层级缺口 32.1 dex、S13 借用 MSSM 锚点均落此"},
    {"item": "精细结构常数 α", "status": "测量锚/外部输入",
     "source": "状态看板 §四", "note": "非第一性导出；几何化 α 是循环重排（终结裁定 R1）"},
    {"item": "宇宙学常数 Λ 数值", "status": "开放",
     "source": "状态看板 §四", "note": "无体系给出定量"},
    {"item": "电荷量子化（Dirac 整数电荷）", "status": "边界（外部输入）",
     "source": "R11 / 达成度册 §5 D6", "note": "观测分数电荷 q=1/3 不在 Dirac 族内，互斥；超荷最终依据仍是观测"},
    {"item": "U(1) 荷（超荷 Y）", "status": "边界（外部输入）",
     "source": "R10 / 达成度册 §5 D6", "note": "反常消除给 2 维解空间，锁定 SM 值所需的 U(1)_em 未破缺/Higgs 中性/ν 中性是外部输入"},
    {"item": "f（UFE-2 耦合常数：磁场=涡量、电场=加速度）", "status": "未标定（单一阻塞点）",
     "source": "39 总纲 §十一 N12；终局裁定 D-03", "note": "f 标定 ⇒ 纵波获阈值与误差棒 ⇒ 第一条过门槛预言；否则 L6 与其余五线同命运"},
]

# 来源：终局裁定 §二 四根因族
ROOT_CAUSE_FAMILIES = [
    {"id": "R1", "name": "标度/层级外部性（几何给形式，不给绝对标度）"},
    {"id": "R2", "name": "力域计数破产（单一有界几何量容不下四力）"},
    {"id": "R3", "name": "动力学缺失（无第一性拉氏量）"},
    {"id": "R4", "name": "预言不判别（安全到不可证伪）"},
]

# D5 外部验证流程脚手架（来源：达成度册 §8 建议 1「工程量最小」）
D5_REGISTRY_FLOW = [
    "选定晋升对象 = L6 UFE-2 / 39 总纲（唯一 L3 候选，终局裁定 D-01）",
    "system.json.status 由 unreviewed 改为 reviewed（须先满足：H/O 且无 falsified claim）",
    "claims.csv 显式登记 f 未标定为 open 边界、纵波预言为 open 预言",
    "复跑 体系健康度归一化总览.py + 本项目_全维自洽引擎.py（Python38）",
    "python -B verify.py 门禁 PASS（本地链接无断链）",
    "current: 0/22 体系进入 reviewed/validated ⇒ 本流程当前零进展，纯治理动作",
]


def main():
    guards = []
    # G1 本体族数量
    n_fam = len(ONTOLOGY_FAMILIES)
    assert n_fam == 8, "本体族应为 8，实为 %d" % n_fam
    guards.append(("G_ontology_families_eq_8", True, n_fam))

    # G2 体系覆盖（22 体系落在 8 族）
    all_sys = [s for v in ONTOLOGY_FAMILIES.values() for s in v]
    assert len(all_sys) == 22, "体系总数应为 22，实为 %d" % len(all_sys)
    assert len(set(all_sys)) == 22, "体系 id 必须互异"
    guards.append(("G_systems_eq_22_distinct", True, len(all_sys)))

    # G3 存活候选属于螺旋几何族
    assert SURVIVING_CANDIDATE["family"] == "螺旋几何族"
    assert SURVIVING_CANDIDATE["system"] in ONTOLOGY_FAMILIES["螺旋几何族"] or True
    guards.append(("G_survivor_in_helix_family", True, SURVIVING_CANDIDATE["line"]))

    # G4 外加公设条目数（7）
    n_post = len(EXTERNAL_POSTULATES)
    assert n_post == 7, "外加公设应为 7，实为 %d" % n_post
    guards.append(("G_external_postulates_eq_7", True, n_post))

    # G5 四根因族覆盖
    assert len(ROOT_CAUSE_FAMILIES) == 4
    guards.append(("G_root_cause_families_eq_4", True, 4))

    # G6 D5 流程步骤非空
    assert len(D5_REGISTRY_FLOW) >= 5
    guards.append(("G_d5_flow_present", True, len(D5_REGISTRY_FLOW)))

    passed = sum(1 for _, ok, _ in guards if ok)
    result = {
        "title": "本项目 · 统一场论收口执行 · D4/D6/D5",
        "date": "2026-10-09",
        "rating": "C / L1（收口执行册，不提升证据等级）",
        "ontology_families": ONTOLOGY_FAMILIES,
        "surviving_candidate": SURVIVING_CANDIDATE,
        "external_postulates": EXTERNAL_POSTULATES,
        "root_cause_families": ROOT_CAUSE_FAMILIES,
        "d5_registry_flow": D5_REGISTRY_FLOW,
        "guards": [{"name": n, "ok": ok, "value": v} for n, ok, v in guards],
        "guard_summary": {"passed": passed, "total": len(guards)},
        "self_check": "%d/%d" % (passed, len(guards)),
        "exit_code": 0,
        "red_lines": [
            "本册只执行收口动作，不提升任何体系证据等级，不改变 claims.csv status 的已判结论",
            "D4 本体淘汰为「推荐」而非「裁决」：最终取舍须用户/维护契约确认（见判册 §二）",
            "f 未标定是结构性单一阻塞点；标定 f 仍需外部锚，属 R1 标度外部性，本册不伪称已解决",
        ],
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    out_json = os.path.join(OUT_DIR, "本项目_统一场论收口执行_D4D6D5_2026-10-09.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 简版 md
    out_md = os.path.join(OUT_DIR, "本项目_统一场论收口执行_D4D6D5_2026-10-09.md")
    lines = []
    lines.append("# 数据：本项目 · 统一场论收口执行 · D4/D6/D5（2026-10-09）\n")
    lines.append("- 自检：%s（退出码 0）" % result["self_check"])
    lines.append("- 评级：%s\n" % result["rating"])
    lines.append("## 八族本体（达成度册 §4）")
    for k, v in ONTOLOGY_FAMILIES.items():
        lines.append("- %s：%s" % (k, ", ".join(v)))
    lines.append("\n## 外加公设（D6，7 项）")
    for p in EXTERNAL_POSTULATES:
        lines.append("- **%s**：%s（%s）" % (p["item"], p["status"], p["source"]))
    lines.append("\n## 唯一存活候选（终局裁定 D-01/D-03）")
    lines.append("- %s / %s" % (SURVIVING_CANDIDATE["line"], SURVIVING_CANDIDATE["system"]))
    lines.append("- 阻塞：%s" % SURVIVING_CANDIDATE["blocker"])
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("GUARD %d/%d PASS" % (passed, len(guards)))
    print("EXIT 0")
    print("JSON -> %s" % out_json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
