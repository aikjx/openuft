# -*- coding: utf-8 -*-
"""
全量理论体系架构 + 统一场论达成度判据 + 归一化（可复跑）
======================================================
本册回答一个问题：**算法联盟到底有没有实现统一场论？**

为了让"实现"两个字有意义，先给出可判定的六条判据（UFT-1..UFT-6），
然后对 18 个体系逐条打分。**任何一条都不能靠自述，只能靠登记与审计产物。**

  UFT-1 数学自洽   审计判定的硬冲突数 == 0（源：体系第一性健康度总览）
  UFT-2 四力统一   给出规范群 + 统一作用量，且作用量含**本体系特有项**
                  （源：全维自洽图谱 S14 判词：EH+YM+Dirac 逐字照搬，无特有项）
  UFT-3 常数派生   登记的无量纲靶 >= 3 且 V2 > 0（源：无量纲靶场审计.json）
  UFT-4 观测复现   复现 SM 谱/耦合且偏差落在观测不确定度内
  UFT-5 可证伪预言 有已登记的、与已知理论不同的可检验预言
  UFT-6 外部验证   生命周期进入 reviewed / validated

判定档位：
  6/6  已实现
  4-5  候选框架（待验证）
  2-3  纲领草案
  0-1  未完成

产出：
  数据/全量理论体系架构.json
  数据/全量理论体系架构.md（含 Mermaid 架构图）
  可视化/全量理论体系架构图.html（纯 SVG，无 CDN 依赖）
"""

import os
import json
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化")
OUT_DATA = os.path.join(BASE, "数据")
OUT_VIS = os.path.join(ROOT, "04_公共成果", "可视化")
REG = os.path.join(ROOT, "00_项目治理", "system_registry.json")

# ---------------------------------------------------------------------------
# 一、源数据（全部来自既有审计产物，本册不重新判定）
# ---------------------------------------------------------------------------

# 族系（源：数据/全维自洽图谱.md 第五节「融合聚类 F1–F6」）
FAMILY = {
    "s01_triad_kinematics": "F1", "s02_light_speed_helix_force": "F1",
    "s10_frequency_helix_ontology": "F1", "s12_light_speed_helix": "F1",
    "s14_torsion_unified_field_tuft": "F1",
    "s03_gaq_geometric_atom": "F2", "s07_gaq_complex_curvature": "F2",
    "s08_gaq_geometrized_constants": "F2", "s09_gaq_mass_spectrum": "F2",
    "s04_ieg_information_gravity": "F3", "s05_hdu_higher_dimensions": "F3",
    "s06_tcl_topological_chirality": "F3",
    "s13_duality_fractal_uft": "F4",
    "s11_gmuft_geometric_coupling": "F5",
    "p01_space_compression": "F6", "p02_matter_source": "F6",
    "p03_gauge_unification": "F6", "p04_quantum_emergence": "F6",
}
FAMILY_NAME = {
    "F1": "F1 螺旋运动学族（共享 Frenet 骨架，本体分叉）",
    "F2": "F2 GAQ 复曲率谱系（v1→v6 版本线，应作版本序列管理）",
    "F3": "F3 GAQ v3 三体系族（原著分册，已被 S07 v4 吸收）",
    "F4": "F4 对偶分形族（唯一含 verified claims）",
    "F5": "F5 几何耦合族（四自由度，场方程 OPEN）",
    "F6": "F6 待建模占位族（无公设无 claims）",
}

# 健康度（源：数据/体系第一性健康度总览.md）
HEALTH = {
    "s01_triad_kinematics": "H", "s13_duality_fractal_uft": "H",
    "s03_gaq_geometric_atom": "O", "s04_ieg_information_gravity": "O",
    "s11_gmuft_geometric_coupling": "O",
    "s02_light_speed_helix_force": "C", "s05_hdu_higher_dimensions": "C",
    "s06_tcl_topological_chirality": "C", "s07_gaq_complex_curvature": "C",
    "s08_gaq_geometrized_constants": "C", "s09_gaq_mass_spectrum": "C",
    "s10_frequency_helix_ontology": "C", "s12_light_speed_helix": "C",
    "s14_torsion_unified_field_tuft": "C",
    "p01_space_compression": "U", "p02_matter_source": "U",
    "p03_gauge_unification": "U", "p04_quantum_emergence": "U",
}

# 第一性层级（源：数据/全维自洽图谱.md 第四节「体系第一性分级」）
LEVEL = {
    "s01_triad_kinematics": "L0",
    "s02_light_speed_helix_force": "L2/L4",
    "s03_gaq_geometric_atom": "L1/L4",
    "s04_ieg_information_gravity": "L2/L4",
    "s05_hdu_higher_dimensions": "L4",
    "s06_tcl_topological_chirality": "L2/L4",
    "s07_gaq_complex_curvature": "L1/L4+冲突",
    "s08_gaq_geometrized_constants": "L1+方向误置",
    "s09_gaq_mass_spectrum": "L1/L4+冲突",
    "s10_frequency_helix_ontology": "L1/L4+冲突",
    "s11_gmuft_geometric_coupling": "L2",
    "s12_light_speed_helix": "L2/L4+借用",
    "s13_duality_fractal_uft": "L3候选",
    "s14_torsion_unified_field_tuft": "L1/L4+硬冲突",
    "p01_space_compression": "无", "p02_matter_source": "无",
    "p03_gauge_unification": "无", "p04_quantum_emergence": "无",
}

# 审计判定冲突数（源：体系第一性健康度总览.md「审计冲突(claim)」列）
CONFLICTS = {
    "s02_light_speed_helix_force": 1, "s05_hdu_higher_dimensions": 2,
    "s06_tcl_topological_chirality": 2, "s07_gaq_complex_curvature": 1,
    "s08_gaq_geometrized_constants": 2, "s09_gaq_mass_spectrum": 1,
    "s10_frequency_helix_ontology": 1, "s12_light_speed_helix": 1,
    "s14_torsion_unified_field_tuft": 28,
}

# 四力统一（UFT-2）：仅登记"给出规范群 + 统一作用量"的体系，并记判词
FORCE_UNIFICATION = {
    "s14_torsion_unified_field_tuft": (0, "给出 G=SO(1,3)×U(1)×SU(2)×SU(3) 主丛作用量，"
                                          "但审计判『EH+YM+Dirac 逐字照搬，无 TUFT 特有项』；"
                                          "结构群为直积非单群；三耦合 1e16 GeV 处 21% 分散不汇聚"),
    "s13_duality_fractal_uft": (0, "M2 涌现规范场覆盖电弱，未给出含强作用的完整统一作用量"),
    "p03_gauge_unification": (0, "方向占位，尚无公设与群签名落地"),
}

# 可证伪预言（UFT-5）
FALSIFIABLE = {
    "s13_duality_fractal_uft": (1, "4 项 L3 候选预言（含电子 EDM d_e=2.257e-34 C·m），待实验"),
    "s14_torsion_unified_field_tuft": (1, "Π_T 手性 B 模、暗物质非粒子；但 Π_T 无定量、"
                                          "手性来源与电弱破缺差 12 个数量级"),
}


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def load_registry():
    data = load_json(REG) or {}
    return {s["id"]: s for s in data.get("systems", [])}


# ---------------------------------------------------------------------------
# 二、UFT 六判据打分
# ---------------------------------------------------------------------------

def score_system(sid, title, status, target_audit, entry=None):
    # UFT-1 要求"有东西可自洽"：无公设的占位方向不参与自洽性评分
    has_postulates = bool((entry or {}).get("postulates"))
    u1 = 1 if (CONFLICTS.get(sid, 0) == 0 and has_postulates) else 0
    u2, u2n = FORCE_UNIFICATION.get(sid, (0, "未给出规范群 + 统一作用量"))
    # 靶场审计里的键是目录名（如 "S14_挠率统一场论TUFT"），而 sid 是小写 id（"s14_..."），
    # 必须忽略大小写与分隔符差异，否则匹配恒失败、n_reg 恒为 0（本册自查发现的真 bug）。
    n_reg = None
    key = sid.split("_")[0].upper()
    for row in (target_audit or {}).get("systems", []):
        sysname = str(row.get("system", "")).upper()
        if sysname.startswith(key):
            n_reg = row.get("n_registered_predictions", 0)
            break
    if n_reg is None:
        n_reg = 0
    u3 = 1 if (n_reg >= 3) else 0
    u3n = ("登记无量纲预测 %d 个（需 >=3 且 V2>0）" % n_reg)
    u4 = 0
    u4n = "未复现 SM 谱/耦合（S14 五类反常为零系继承 SM，非本体系导出）"
    u5, u5n = FALSIFIABLE.get(sid, (0, "无可证伪预言登记"))
    u6 = 1 if status in ("reviewed", "validated") else 0
    u6n = "生命周期状态 = %s" % status
    score = u1 + u2 + u3 + u4 + u5 + u6
    if score == 6:
        verdict = "已实现"
    elif score >= 4:
        verdict = "候选框架"
    elif score >= 2:
        verdict = "纲领草案"
    else:
        verdict = "未完成"
    return {
        "id": sid, "title": title, "status": status,
        "family": FAMILY.get(sid, "?"), "health": HEALTH.get(sid, "?"),
        "level": LEVEL.get(sid, "?"), "conflicts": CONFLICTS.get(sid, 0),
        "U1": u1, "U2": u2, "U3": u3, "U4": u4, "U5": u5, "U6": u6,
        "score": score, "verdict": verdict,
        "notes": {"U2": u2n, "U3": u3n, "U4": u4n, "U5": u5n, "U6": u6n},
    }


# ---------------------------------------------------------------------------
# 三、归一化坐标
# ---------------------------------------------------------------------------

HEALTH_NUM = {"H": 3, "O": 2, "C": 1, "U": 0}


def level_num(lv):
    """把层级串归一到 0..3 的主层级（取出现的最高非冲突层级）。"""
    if lv.startswith("L0"):
        return 0
    if lv.startswith("L1"):
        return 1
    if lv.startswith("L2"):
        return 2
    if lv.startswith("L3"):
        return 3
    return None


def normalize(rows):
    out = []
    for r in rows:
        ln = level_num(r["level"])
        out.append({
            "id": r["id"],
            "x_level": ln,               # 0..3（None = 无分级）
            "y_health": HEALTH_NUM.get(r["health"], 0),
            "z_uft": r["score"],         # 0..6
            "family": r["family"],
            "bucket": "%s/%s/%d" % (r["family"], r["health"], r["score"]),
        })
    return out


# ---------------------------------------------------------------------------
# 四、SVG 架构图
# ---------------------------------------------------------------------------

HEALTH_COLOR = {"H": "#2e7d32", "O": "#ef6c00", "C": "#c62828", "U": "#616161"}
BAND_BG = ["#eef2f7", "#f6f4ee", "#eef7f1", "#f4eef7", "#fdf3e7", "#eaf1f8"]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_svg(rows, targets, engines):
    W = 1680
    bands = []
    y = 30
    # band 分块高度
    # H_SYS 必须容纳 F1 的 5 个成员：30(top pad) + 5*(44+6) + 12(bottom pad)
    H_VERDICT, H_TARGET, H_ENGINE, H_FAM, H_SYS, H_GOV = 90, 96, 96, 92, 300, 86
    layout = [
        ("判定层", H_VERDICT), ("靶场层", H_TARGET), ("审计层", H_ENGINE),
        ("族系层", H_FAM), ("公设/体系层", H_SYS), ("治理层", H_GOV),
    ]
    boxes = []
    for i, (name, h) in enumerate(layout):
        bands.append({"name": name, "y": y, "h": h, "bg": BAND_BG[i]})
        y += h + 26
    total_h = y + 10

    parts = []
    parts.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
                 'viewBox="0 0 %d %d" font-family="Microsoft YaHei, SimHei, sans-serif">'
                 % (W, total_h, W, total_h))
    parts.append('<rect width="100%%" height="100%%" fill="#ffffff"/>')
    parts.append('<text x="%d" y="20" font-size="18" font-weight="bold" fill="#1a237e">'
                 'openuft 全量理论体系架构图（18 体系 / 6 族系 / 7 审计引擎 / 10 无量纲靶）</text>'
                 % (W // 2))

    # band 容器
    for b in bands:
        parts.append('<rect x="16" y="%d" width="%d" height="%d" rx="10" fill="%s" '
                     'stroke="#b0bec5"/>' % (b["y"], W - 32, b["h"], b["bg"]))
        parts.append('<text x="30" y="%d" font-size="14" font-weight="bold" fill="#37474f">%s</text>'
                     % (b["y"] + 20, esc(b["name"])))

    def put_band(idx, items, bw, gap, color_fn, fontsize=11, top_pad=30):
        b = bands[idx]
        n = len(items)
        total = n * bw + (n - 1) * gap
        x0 = (W - total) // 2
        for i, it in enumerate(items):
            x = x0 + i * (bw + gap)
            yy = b["y"] + top_pad
            col = color_fn(it)
            parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" '
                         'stroke="#546e7a" stroke-width="1"/>'
                         % (x, yy, bw, b["h"] - top_pad - 12, col))
            label = it.get("label", "")
            parts.append('<text x="%d" y="%d" font-size="%d" fill="#ffffff" '
                         'text-anchor="middle">%s</text>'
                         % (x + bw // 2, yy + 20, fontsize, esc(label)))
            sub = it.get("sub", "")
            if sub:
                parts.append('<text x="%d" y="%d" font-size="%d" fill="#eceff1" '
                             'text-anchor="middle">%s</text>'
                             % (x + bw // 2, yy + 38, fontsize - 2, esc(sub)))
        return x0, bw, gap

    # 判定层
    verdict_items = [
        {"label": "H 健康 2", "sub": "无硬冲突且非欠定", "c": HEALTH_COLOR["H"]},
        {"label": "O 欠定 3", "sub": "高风险候选", "c": HEALTH_COLOR["O"]},
        {"label": "C 冲突 9", "sub": "审计判定硬冲突", "c": HEALTH_COLOR["C"]},
        {"label": "U 占位 4", "sub": "无公设", "c": HEALTH_COLOR["U"]},
        {"label": "UFT 达成度 最高 2/6", "sub": "联盟层：未实现", "c": "#4527a0"},
    ]
    put_band(0, verdict_items, 290, 14, lambda it: it["c"], 13, 30)

    # 靶场层
    put_band(1, [{"label": t["key"], "sub": t["value"][:14]} for t in targets],
             128, 12, lambda it: "#00695c", 11, 34)

    # 审计层
    put_band(2, [{"label": e} for e in engines], 200, 14,
             lambda it: "#1565c0", 11, 34)

    # 族系层
    fam_items = []
    for k in ("F1", "F2", "F3", "F4", "F5", "F6"):
        cnt = sum(1 for r in rows if r["family"] == k)
        fam_items.append({"label": k, "sub": "%d 个成员" % cnt})
    put_band(3, fam_items, 250, 12, lambda it: "#6a1b9a", 13, 32)

    # 体系层：按族分列
    b = bands[4]
    cols = ("F1", "F2", "F3", "F4", "F5", "F6")
    colw = 250
    gap = 12
    total = len(cols) * colw + (len(cols) - 1) * gap
    x0 = (W - total) // 2
    bh = 44
    for ci, fam in enumerate(cols):
        cx = x0 + ci * (colw + gap)
        members = [r for r in rows if r["family"] == fam]
        for mi, r in enumerate(members):
            yy = b["y"] + 30 + mi * (bh + 6)
            col = HEALTH_COLOR.get(r["health"], "#616161")
            parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="%s" '
                         'stroke="#37474f"/>' % (cx, yy, colw, bh, col))
            short = r["id"].split("_")[0].upper()
            parts.append('<text x="%d" y="%d" font-size="12" fill="#ffffff">%s %s</text>'
                         % (cx + 8, yy + 18, esc(short), esc(r["title"][:16])))
            parts.append('<text x="%d" y="%d" font-size="10" fill="#e8f5e9">%s · UFT %d/6 · %s</text>'
                         % (cx + 8, yy + 34, esc(r["level"]), r["score"], esc(r["verdict"])))

    # 治理层
    gov = [{"label": "system_registry.json", "sub": "18 体系登记"},
           {"label": "claims.csv", "sub": "各体系主张与 status"},
           {"label": "verify.py", "sub": "链接/目录门禁"},
           {"label": "缺漏诊断", "sub": "2026-09-18"}]
    put_band(5, gov, 330, 14, lambda it: "#37474f", 12, 32)

    # 层间箭头（自下而上）
    for i in range(len(bands) - 1):
        lower = bands[i + 1]
        upper = bands[i]
        y1 = lower["y"] - 4
        y2 = upper["y"] + upper["h"] + 2
        xc = W // 2
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#78909c" '
                     'stroke-width="2" marker-end="url(#ah)"/>' % (xc, y1, xc, y2))
    parts.append('<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="9" refY="3" '
                 'orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#78909c"/></marker></defs>')

    parts.append('<text x="%d" y="%d" font-size="11" fill="#78909c" text-anchor="middle">'
                 '箭头方向 = 数据流向（治理 → 体系 → 族系 → 审计 → 靶场 → 判定）；'
                 '颜色 = 健康度 H/O/C/U</text>' % (W // 2, total_h - 6))
    parts.append("</svg>")
    return "\n".join(parts)


HTML = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>openuft 全量理论体系架构图</title>
<style>
body{margin:0;background:#fafafa;font-family:"Microsoft YaHei",SimHei,sans-serif;}
header{padding:14px 22px;background:#1a237e;color:#fff;}
header h1{margin:0;font-size:18px;}
header p{margin:6px 0 0;font-size:12px;opacity:.85;}
main{padding:12px 18px 40px;}
.legend{font-size:13px;margin:10px 0;}
.legend span{display:inline-block;padding:3px 9px;color:#fff;border-radius:4px;margin-right:6px;}
</style></head><body>
<header><h1>openuft · 全量理论体系架构图</h1>
<p>18 体系 / 6 族系 / 7 审计引擎 / 10 无量纲靶 · 生成时间 __TS__ · 本图为可复跑产物，请勿手工编辑</p></header>
<main>
<div class="legend">
健康度：<span style="background:#2e7d32">H 健康</span>
<span style="background:#ef6c00">O 欠定</span>
<span style="background:#c62828">C 冲突</span>
<span style="background:#616161">U 占位</span>
&nbsp;&nbsp;统一场论达成度最高 __MAX__/6 —— <b>未实现</b>
</div>
__SVG__
</main></body></html>
"""


# ---------------------------------------------------------------------------
# 五、主流程
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    reg = load_registry()
    target_audit = load_json(os.path.join(OUT_DATA, "无量纲靶场审计.json")) or {}
    targets = target_audit.get("targets", [])
    engines = [
        "全维自洽引擎", "健康度归一化", "O级隔离审查", "O级缺陷修复",
        "普朗克锚定修正", "v_eq_c 求导验证", "无量纲靶场审计",
    ]

    rows = []
    for sid in sorted(reg.keys()):
        s = reg[sid]
        rows.append(score_system(sid, s.get("title", ""), s.get("status", ""), target_audit, s))
    rows.sort(key=lambda r: (-r["score"], r["id"]))

    coords = normalize(rows)
    max_score = max(r["score"] for r in rows)
    fam_count = {k: sum(1 for r in rows if r["family"] == k) for k in FAMILY_NAME}
    health_count = {k: sum(1 for r in rows if r["health"] == k) for k in ("H", "O", "C", "U")}

    # 联盟层判据
    alliance = {
        "UFT-1 数学自洽": (1, "存在 H/O 级无硬冲突体系（%d 个）" % (health_count["H"] + health_count["O"])),
        "UFT-2 四力统一": (0, "无一体系给出含特有项的统一作用量"),
        "UFT-3 常数派生": (0, "18 体系登记无量纲预测数 = 0"),
        "UFT-4 观测复现": (0, "无一体系复现 SM 谱/耦合"),
        "UFT-5 可证伪预言": (1, "S13/S14 有登记，但定量不足"),
        "UFT-6 外部验证": (0, "全部 unreviewed / unformulated"),
    }
    alliance_score = sum(v[0] for v in alliance.values())

    os.makedirs(OUT_DATA, exist_ok=True)
    os.makedirs(OUT_VIS, exist_ok=True)

    # ---- JSON
    payload = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0],
        "criteria": ["UFT-1 数学自洽", "UFT-2 四力统一", "UFT-3 常数派生",
                     "UFT-4 观测复现", "UFT-5 可证伪预言", "UFT-6 外部验证"],
        "tiers": {"6": "已实现", "4-5": "候选框架", "2-3": "纲领草案", "0-1": "未完成"},
        "alliance_score": alliance_score,
        "alliance_detail": {k: v[1] for k, v in alliance.items()},
        "verdict": "未实现统一场论",
        "max_system_score": max_score,
        "health_count": health_count,
        "family_count": fam_count,
        "systems": rows,
        "normalized_coords": coords,
    }
    with open(os.path.join(OUT_DATA, "全量理论体系架构.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    # ---- MD
    L = []
    L.append("# 全量理论体系架构与归一化（可复跑产物）\n")
    L.append("> 由 `源码/全量理论体系架构与归一化.py` 生成，**请勿手工编辑**。\n")
    L.append("## 一、结论：是否实现了统一场论？\n")
    L.append("**没有。** 联盟层判据 **%d/6**，单体系最高 **%d/6**（%s）。\n"
             % (alliance_score, max_score, rows[0]["id"]))
    L.append("| 判据 | 联盟层 | 依据 |")
    L.append("| --- | --- | --- |")
    for k, (v, note) in alliance.items():
        L.append("| %s | %s | %s |" % (k, "✅" if v else "❌", note))
    L.append("\n## 二、体系级 UFT 达成度（18 体系）\n")
    L.append("| 体系 | 族 | 健康 | 层级 | U1 | U2 | U3 | U4 | U5 | U6 | 得分 | 判定 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        L.append("| %s %s | %s | %s | %s | %d | %d | %d | %d | %d | %d | **%d/6** | %s |"
                 % (r["id"].split("_")[0].upper(), r["title"], r["family"], r["health"],
                    r["level"], r["U1"], r["U2"], r["U3"], r["U4"], r["U5"], r["U6"],
                    r["score"], r["verdict"]))
    L.append("\n## 三、归一化统计\n")
    L.append("| 健康度 | 数量 |\n| --- | --- |")
    for k in ("H", "O", "C", "U"):
        L.append("| %s | %d |" % (k, health_count[k]))
    L.append("\n| 族系 | 成员数 | 说明 |\n| --- | --- | --- |")
    for k, name in FAMILY_NAME.items():
        L.append("| %s | %d | %s |" % (k, fam_count.get(k, 0), name))
    L.append("\n## 四、架构图（Mermaid）\n")
    L.append("```mermaid")
    L.append("graph TD")
    L.append("  GOV[治理层: system_registry / claims.csv / verify.py]")
    for k, name in FAMILY_NAME.items():
        L.append("  %s[%s]" % (k, name.split("（")[0]))
    for r in rows:
        L.append("  %s[%s %s %s]" % (r["id"].split("_")[0].upper(),
                                     r["id"].split("_")[0].upper(),
                                     r["title"], r["health"]))
        L.append("  %s --> %s" % (r["id"].split("_")[0].upper(), r["family"]))
    for k in FAMILY_NAME:
        L.append("  %s --> AUDIT[审计层: 7 个引擎]" % k)
    L.append("  AUDIT --> TGT[靶场层: 10 个无量纲靶]")
    L.append("  TGT --> VER[判定层: H/O/C/U + UFT 达成度 %d/6]" % alliance_score)
    L.append("  GOV --> AUDIT")
    L.append("```\n")
    L.append("> 交互式 SVG 版见 `04_公共成果/可视化/全量理论体系架构图.html`。\n")
    with open(os.path.join(OUT_DATA, "全量理论体系架构.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    # ---- HTML
    svg = build_svg(rows, targets, engines)
    html = (HTML.replace("__SVG__", svg)
                .replace("__TS__", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
                .replace("__MAX__", str(max_score)))
    with open(os.path.join(OUT_VIS, "全量理论体系架构图.html"), "w", encoding="utf-8") as fh:
        fh.write(html)

    # ---- console
    print("=" * 78)
    print("全量理论体系架构 · 统一场论达成度判据（Python %s）" % sys.version.split()[0])
    print("=" * 78)
    print("联盟层：%d/6 —— 未实现统一场论" % alliance_score)
    for k, (v, note) in alliance.items():
        print("   [%s] %s : %s" % ("OK" if v else "!!", k, note))
    print("-" * 78)
    print("体系层（按得分降序）：")
    for r in rows:
        print("   %-4s %-22s %s %-6s %-12s UFT %d/6  %s"
              % (r["id"].split("_")[0].upper(), r["title"][:22], r["family"],
                 r["health"], r["level"], r["score"], r["verdict"]))
    print("-" * 78)
    print("健康度 H=%d O=%d C=%d U=%d；族系 %s"
          % (health_count["H"], health_count["O"], health_count["C"], health_count["U"], fam_count))
    print("产出：数据/全量理论体系架构.{json,md} + 可视化/全量理论体系架构图.html"
          "   用时 %.2fs" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
