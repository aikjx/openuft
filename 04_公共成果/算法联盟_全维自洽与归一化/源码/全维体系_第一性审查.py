# -*- coding: utf-8 -*-
"""
全维体系 · 第一性审查（可复跑）
===============================
对全部 17 个体系做统一口径的第一性审查（「全维完成」）：
  - 统计各体系 claims.csv 的 claim 数 / verified / falsified / unreviewed（鲁棒读取行末 status）
  - 检查 claims.csv **列数一致性**（数据质量：未转义逗号、字段缺失会导致列错位）
  - 结合归一化评级（H/O/C/U，审计冲突白名单）与第一性层级备注
产出：数据/全维第一性审查总表.md + .json
"""
import os
import sys
import json
import csv
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REG = os.path.join(ROOT, "00_项目治理", "system_registry.json")
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

H_SET = {"s01_triad_kinematics", "s13_duality_fractal_uft"}
U_SET = {"p01_space_compression", "p02_matter_source", "p03_gauge_unification", "p04_quantum_emergence"}
AUDIT_CONFLICT_IDS = {
    # 2026-09-15 增量：S14 TUFT 三册精算（四力统一 / 黑洞 / 暴胀CMB）+ 公理化的审计判定 FAIL
    "S14-C0001", "S14-C0002", "S14-C0003", "S14-C0004", "S14-C0005",
    "S14-C0006", "S14-C0007", "S14-C0008", "S14-C0012",
    "S14-C0013", "S14-C0014", "S14-C0015", "S14-C0016", "S14-C0017",
    "S14-C0018", "S14-C0019", "S14-C0020", "S14-C0021",
    "S14-C0022", "S14-C0023", "S14-C0024", "S14-C0025", "S14-C0026",
    "S14-C0027", "S14-C0028", "S14-C0029", "S14-C0030", "S14-C0031",
    "S02-C0001", "S05-C0001", "S05-C0002", "S06-C0001", "S06-C0002",
    "S07-C0001", "S08-C0001", "S08-C0002", "S09-C0001", "S10-C0001", "S12-C0006",
}
LAYER_NOTE = {
    "s14_torsion_unified_field_tuft": "L0/L1 为主 + L4 本体：可用部分为标准公式复用（慢滚骨架、`T_H=ħc√K/4πk_B`、SM 反常五类为零属**继承**）；"
                                      "TUFT 特有主张（`αKTΩ/c²` 类量纲、`F_T`、`Π_T`、直积归一、暴胀势）均 FAIL 且跨册复发",
    "s01_triad_kinematics": "L0（三重奏 κ²+τ²=(ω/v)² 代数恒等，引擎 B01–B04）；claims 空 → 零物理 claim",
    "s13_duality_fractal_uft": "L0/L1/L2（流守恒/曲率闭式/霍普夫荷整性/希格斯谱）+ L3 候选（4 预言，conjecture 待检验）",
    "s02_light_speed_helix_force": "含 M03 冲突（P=m(c−v) 低速极限）",
    "s03_gaq_geometric_atom": "L0 同义反复 + L1 概念循环（隔离审查）",
    "s04_ieg_information_gravity": "L1 恒等重述（隔离审查）",
    "s05_hdu_higher_dimensions": "含 FAIL：H2 量纲错（偏 1.4e14）、H3 数值错",
    "s06_tcl_topological_chirality": "含 FAIL：Cl(4,4)⊗ℂ 同构错、维数自相矛盾",
    "s07_gaq_complex_curvature": "含 M01/M02 冲突（普朗克锚定谬误）",
    "s08_gaq_geometrized_constants": "含 M01/M02 冲突 + 方向误置",
    "s09_gaq_mass_spectrum": "含 M01/M02 冲突（质量谱退化）",
    "s10_frequency_helix_ontology": "含 M01/M02 冲突（κ²+τ² 双身份）",
    "s11_gmuft_geometric_coupling": "L1 借用几何 + 已诚实标注欠定（OPEN-2）",
    "s12_light_speed_helix": "含 M03 冲突 + 本体—动力学接口未定义",
    "p01_space_compression": "未立项（无公设）",
    "p02_matter_source": "未立项（无公设）",
    "p03_gauge_unification": "未立项（已立项评估，建议立项）",
    "p04_quantum_emergence": "未立项（无公设）",
}


def scan_claims(base):
    """返回 (claims[(cid,status)], col_widths[list], header_len)。"""
    out = []
    widths = []
    hlen = None
    p = os.path.join(base, "claims.csv")
    if not os.path.isfile(p):
        return out, widths, hlen
    with open(p, encoding='utf-8') as f:
        r = csv.reader(f)
        header = next(r, None)
        hlen = len(header) if header else None
        for line in r:
            if not line:
                continue
            widths.append(len(line))
            if len(line) < 3:
                continue
            out.append((line[0].strip(), line[-2].strip().lower()))
    return out, widths, hlen


reg = json.load(open(REG, encoding='utf-8'))
systems = reg["systems"]

rows = []
for s in systems:
    sid = s["id"]
    claims, widths, hlen = scan_claims(os.path.join(ROOT, "01_独立体系", s["directory"]))
    statuses = [st for _, st in claims]
    n_total = len(claims)
    n_ver = sum(1 for st in statuses if st == 'verified')
    n_fal = sum(1 for st in statuses if st == 'falsified')
    n_unr = sum(1 for st in statuses if st == 'unreviewed')
    n_other = n_total - n_ver - n_fal - n_unr
    audit = [c for c, st in claims if st == 'falsified' and c in AUDIT_CONFLICT_IDS]

    # 数据质量：列数一致性
    if hlen is None:
        quality = "无 claims.csv"
    elif not widths:
        quality = "空（仅表头）"
    elif len(set(widths)) == 1 and widths[0] == hlen:
        quality = "一致(%d列)" % hlen
    else:
        quality = "⚠列数不一致 header=%s rows=%s" % (hlen, sorted(set(widths)))

    if audit:
        rating = 'C'
    elif sid in H_SET:
        rating = 'H'
    elif sid in U_SET:
        rating = 'U'
    else:
        rating = 'O'

    rows.append({"id": sid, "title": s["title"], "kind": s["kind"], "rating": rating,
                 "claims_total": n_total, "verified": n_ver, "falsified": n_fal,
                 "unreviewed": n_unr, "other": n_other,
                 "audit_conflicts": audit, "data_quality": quality,
                 "layer": LAYER_NOTE.get(sid, "")})

cnt = Counter(r["rating"] for r in rows)
bad_quality = [r for r in rows if r["data_quality"].startswith("⚠")]

md = "# 全维体系 · 第一性审查总表（全维完成）\n\n"
md += "> 对全部 %d 个体系做统一口径的第一性审查：claim 统计 + 列数一致性（数据质量）+ 归一化评级 + 层级备注。\n" % len(rows)
md += "> 读取方式：按行末两列（status, reviewer）定位 status，规避列错位。\n\n"
md += "## 一、评级统计\n\n| 评级 | 数量 | 体系 |\n|---|---|---|\n"
for k in ['H', 'O', 'C', 'U']:
    names = ', '.join(x["id"] for x in rows if x["rating"] == k)
    md += "| %s | %d | %s |\n" % (k, cnt.get(k, 0), names)
md += "\n**合计 %d 体系**：C %d · O %d · H %d · U %d\n\n" % (
    len(rows), cnt.get('C', 0), cnt.get('O', 0), cnt.get('H', 0), cnt.get('U', 0))

md += "## 二、逐体系明细\n\n"
md += "| 体系 | 类型 | 评级 | claim | verified | falsified | unreviewed | 数据质量 | 第一性层级 / 性质 |\n"
md += "|---|---|---|---|---|---|---|---|---|\n"
for x in rows:
    md += "| %s | %s | %s | %d | %d | %d | %d | %s | %s |\n" % (
        x["id"], x["kind"], x["rating"], x["claims_total"], x["verified"],
        x["falsified"], x["unreviewed"], x["data_quality"], x["layer"])

md += "\n## 三、数据质量告警\n\n"
if bad_quality:
    for x in bad_quality:
        md += "- **%s**：%s（未转义逗号 / 字段缺失会致列错位，固定列号读取会静默误判）\n" % (x["id"], x["data_quality"])
else:
    md += "- 无\n"

os.makedirs(OUT_DIR, exist_ok=True)
json.dump({"rows": rows, "counts": dict(cnt)},
          open(os.path.join(OUT_DIR, "全维第一性审查总表.json"), "w", encoding='utf-8'),
          ensure_ascii=False, indent=2)
open(os.path.join(OUT_DIR, "全维第一性审查总表.md"), "w", encoding='utf-8').write(md)
print("全维第一性审查总表已生成：%d 体系；C=%d O=%d H=%d U=%d；数据质量告警 %d 项" %
      (len(rows), cnt.get('C', 0), cnt.get('O', 0), cnt.get('H', 0), cnt.get('U', 0), len(bad_quality)))
for x in bad_quality:
    print("  [数据质量] %s：%s" % (x["id"], x["data_quality"]))
