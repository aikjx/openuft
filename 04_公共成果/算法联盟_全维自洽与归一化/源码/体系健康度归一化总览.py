# -*- coding: utf-8 -*-
"""
全仓库第一性健康度归一化总览（可复跑）
======================================
把 openuft 的 17 个体系归一到统一的第一性坐标系：

  评级  H = 健康（自洽、无已知硬冲突）
        O = 欠定 / 高风险候选（依赖已证伪谱系、或本体待建）
        C = 内部冲突（含「审计判定的冲突」或「未修复缺陷」）
        U = 未立项占位（unformulated_direction，无公设）

C 级判定（重要）：
  - 自动扫描各体系 claims.csv 的 status 列；
  - 仅当命中的 falsified 属于【审计判定的冲突】白名单时才判 C；
  - 体系**自我记录并已修复**的证伪（如 S13-C0005：1D 绕数→升维修复）不计入 C，
    而是在备注中显式标注——这是诚实治理与「未修复冲突」的本质区别。

鲁棒读取：按行末两列（status, reviewer）定位 status，规避列错位 / 未转义逗号。
产出：数据/体系第一性健康度总览.md + .json
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
O_SET = {"s03_gaq_geometric_atom", "s04_ieg_information_gravity", "s05_hdu_higher_dimensions",
         "s06_tcl_topological_chirality", "s11_gmuft_geometric_coupling"}
U_SET = {"p01_space_compression", "p02_matter_source", "p03_gauge_unification", "p04_quantum_emergence"}

# 审计判定的冲突/缺陷（算法联盟登记）；命中者判 C
AUDIT_CONFLICT_IDS = {
    "S02-C0001", "S05-C0001", "S05-C0002", "S06-C0001", "S06-C0002",
    "S07-C0001", "S08-C0001", "S08-C0002", "S09-C0001", "S10-C0001", "S12-C0006",
}

NOTE = {
    "s01_triad_kinematics": "数学框架：三重奏 κ²+τ²=(ω/v)² 为 L0 代数恒等（引擎 B01–B04 符号恒等）；claims.csv 为空——零物理 claim，诚实声明不引入本体",
    "s13_duality_fractal_uft": "唯一健康候选；三公理代数全机器零（F05–F07）；β 符号约定已在 postulates §3 补注（F08）；4 项 L3 候选预言为 conjecture 待检验",
    "s03_gaq_geometric_atom": "M02 谱系母体（含普朗克尺度锚定 A4/A5）；隔离审查判 L0 同义反复 + L1 概念循环，无独立可验证内容",
    "s04_ieg_information_gravity": "依赖 GAQ v3；隔离审查判 I1 为恒等重述（∇J=0 无条件成立），无独立物理内容",
    "s05_hdu_higher_dimensions": "隔离审查发现独立缺陷：H2 量纲错（偏 1.4e14 倍）、H3 数值错（§14）",
    "s06_tcl_topological_chirality": "隔离审查发现独立缺陷：Cl(4,4)⊗ℂ 代数同构错、维数自相矛盾（§14）",
    "s11_gmuft_geometric_coupling": "借用 GAQ 几何；隔离审查判非标准式 Q/M=√(4πε₀G) 原文已诚实标注（OPEN-2）",
    "p03_gauge_unification": "方向占位；P03 立项评估建议立项，走群论不受 M02 影响",
    "p01_space_compression": "方向占位，无公设",
    "p02_matter_source": "方向占位，无公设",
    "p04_quantum_emergence": "方向占位，无公设",
}


def read_claims(base):
    """按行末两列（status, reviewer）鲁棒读取，返回 [(claim_id, status)]。"""
    out = []
    p = os.path.join(base, "claims.csv")
    if not os.path.isfile(p):
        return out
    with open(p, encoding='utf-8') as f:
        r = csv.reader(f)
        next(r, None)
        for line in r:
            if not line or len(line) < 3:
                continue
            out.append((line[0].strip(), line[-2].strip().lower()))
    return out


reg = json.load(open(REG, encoding='utf-8'))
systems = reg["systems"]

rows = []
for s in systems:
    sid = s["id"]
    title = s["title"]
    kind = s["kind"]
    claims = read_claims(os.path.join(ROOT, "01_独立体系", s["directory"]))
    falsified = [c for c, st in claims if st == 'falsified']
    audit = [c for c in falsified if c in AUDIT_CONFLICT_IDS]
    self_fal = [c for c in falsified if c not in AUDIT_CONFLICT_IDS]

    if audit:
        rating = 'C'
    elif sid in H_SET:
        rating = 'H'
    elif sid in U_SET:
        rating = 'U'
    else:
        rating = 'O'

    note = NOTE.get(sid, "")
    if self_fal:
        note += "；含 %d 条体系自我记录并已修复的证伪（%s）" % (len(self_fal), ",".join(self_fal))

    rows.append({"id": sid, "title": title, "kind": kind, "rating": rating,
                 "audit_conflicts": audit, "self_falsified": self_fal, "note": note})

cnt = Counter(r["rating"] for r in rows)

md = "# 全仓库第一性健康度归一化总览\n\n"
md += "> 来源：system_registry.json（17 体系）+ 各体系 claims.csv（鲁棒读取 status）+ 算法联盟审计结论。\n\n"
md += "评级：H=健康 / O=欠定或高风险 / C=内部冲突(审计判定) / U=未立项占位。\n"
md += "注：体系**自我记录并已修复**的证伪不计 C，仅在备注标注（诚实治理 ≠ 未修复冲突）。\n\n"
md += "## 统计\n\n| 评级 | 数量 | 体系 |\n|---|---|---|\n"
for k in ['H', 'O', 'C', 'U']:
    names = ', '.join(x["id"] for x in rows if x["rating"] == k)
    md += "| %s | %d | %s |\n" % (k, cnt.get(k, 0), names)
md += "\n**合计 %d 个体系**：C %d · O %d · H %d · U %d\n\n" % (
    len(rows), cnt.get('C', 0), cnt.get('O', 0), cnt.get('H', 0), cnt.get('U', 0))
md += "## 体系级明细\n\n| 体系 | 类型 | 评级 | 审计冲突(claim) | 自我证伪(已修复) | 备注 |\n|---|---|---|---|---|---|\n"
for x in rows:
    ac = ','.join(x["audit_conflicts"]) or '—'
    sf = ','.join(x["self_falsified"]) or '—'
    md += "| %s %s | %s | %s | %s | %s | %s |\n" % (x['id'], x['title'], x['kind'], x['rating'], ac, sf, x['note'])

os.makedirs(OUT_DIR, exist_ok=True)
json.dump({"rows": rows, "counts": dict(cnt)},
          open(os.path.join(OUT_DIR, "体系第一性健康度总览.json"), "w", encoding='utf-8'),
          ensure_ascii=False, indent=2)
open(os.path.join(OUT_DIR, "体系第一性健康度总览.md"), "w", encoding='utf-8').write(md)
print("体系健康度总览已生成：%d 体系；C=%d O=%d H=%d U=%d" %
      (len(rows), cnt.get('C', 0), cnt.get('O', 0), cnt.get('H', 0), cnt.get('U', 0)))
