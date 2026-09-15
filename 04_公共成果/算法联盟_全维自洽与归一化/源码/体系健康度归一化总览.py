# -*- coding: utf-8 -*-
"""
全仓库第一性健康度归一化总览（可复跑）
======================================
把 openuft 的 17 个体系归一到统一的第一性坐标系：

  评级  H = 健康（自洽、无已知硬冲突）
        O = 欠定 / 高风险候选（依赖已证伪谱系、或本体待建）
        C = 内部冲突（已在 claims.csv 登记 falsified）
        U = 未立项占位（unformulated_direction，无公设）

C 级由每个体系的 claims.csv 自动提取（status/falsified 列），
其余 H/O/U 由算法联盟审计结论固定映射（透明、可复跑）。
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

# ── 审计结论归一化映射（来源：算法联盟全维自洽引擎 + 第一性冲突登记）──
H_SET = {"s01_triad_kinematics", "s13_duality_fractal_uft"}
O_SET = {"s03_gaq_geometric_atom", "s04_ieg_information_gravity", "s05_hdu_higher_dimensions",
         "s06_tcl_topological_chirality", "s11_gmuft_geometric_coupling"}
U_SET = {"p01_space_compression", "p02_matter_source", "p03_gauge_unification", "p04_quantum_emergence"}
NOTE = {
    "s01_triad_kinematics": "三重奏全 PASS（L0 代数恒等式）；诚实声明不引入物理本体，不构成统一场论成就",
    "s13_duality_fractal_uft": "唯一健康候选；三公理代数全机器零，仅 F08 β 函数 epsilon 符号补注",
    "s03_gaq_geometric_atom": "M02 谱系母体（含普朗克尺度锚定 A4/A5），未含显式导出谬误式；高风险",
    "s04_ieg_information_gravity": "依赖 GAQ v3；Einstein 方程重述（L1），无独立预言",
    "s05_hdu_higher_dimensions": "依赖 GAQ v3；含普朗克尺度紧致化半径",
    "s06_tcl_topological_chirality": "依赖 GAQ v3；Cl(4,4) 拓扑代结构",
    "s11_gmuft_geometric_coupling": "借用 GAQ 几何；四大自由度 R,T,Q,Pi，完整场方程待建",
    "p03_gauge_unification": "方向占位；P03 立项评估建议立项，走群论不受 M02 影响",
    "p01_space_compression": "方向占位，无公设",
    "p02_matter_source": "方向占位，无公设",
    "p04_quantum_emergence": "方向占位，无公设",
}

reg = json.load(open(REG, encoding='utf-8'))
systems = reg["systems"]

rows = []
for s in systems:
    sid = s["id"]
    title = s["title"]
    d = s["directory"]
    falsified = []
    csvp = os.path.join(ROOT, "01_独立体系", d, "claims.csv")
    if os.path.isfile(csvp):
        with open(csvp, encoding='utf-8') as f:
            r = csv.reader(f)
            header = next(r, None)
            for line in r:
                if not line or len(line) < 11:
                    continue
                if line[10].strip().lower() == 'falsified' or line[9].strip().lower() == 'falsified':
                    falsified.append(line[0])
    if falsified:
        rating = 'C'
    elif sid in H_SET:
        rating = 'H'
    elif sid in O_SET:
        rating = 'O'
    elif sid in U_SET:
        rating = 'U'
    else:
        rating = 'O'
    rows.append({"id": sid, "title": title, "kind": s["kind"], "rating": rating,
                 "falsified_claims": falsified, "note": NOTE.get(sid, "")})

cnt = Counter(r["rating"] for r in rows)

# ── 输出 markdown ──
md = "# 全仓库第一性健康度归一化总览\n\n"
md += "> 来源：system_registry.json（17 体系）+ 各体系 claims.csv（falsified 自动提取）+ 算法联盟审计结论。\n\n"
md += "评级：H=健康(自洽无硬冲突) / O=欠定或高风险候选 / C=内部冲突(已证伪登记) / U=未立项占位。\n\n"
md += "## 统计\n\n"
md += "| 评级 | 数量 | 体系 |\n|---|---|---|\n"
for r in ['H', 'O', 'C', 'U']:
    names = ', '.join(x["id"] for x in rows if x["rating"] == r)
    md += "| %s | %d | %s |\n" % (r, cnt.get(r, 0), names)
md += "\n**合计 %d 个体系**：C %d · O %d · H %d · U %d\n\n" % (len(rows), cnt.get('C', 0), cnt.get('O', 0), cnt.get('H', 0), cnt.get('U', 0))
md += "## 体系级明细\n\n"
md += "| 体系 | 类型 | 评级 | 命中冲突(claim) | 备注 |\n|---|---|---|---|---|\n"
for x in rows:
    fc = ','.join(x["falsified_claims"]) if x["falsified_claims"] else '—'
    md += "| %s %s | %s | %s | %s | %s |\n" % (x['id'], x['title'], x['kind'], x['rating'], fc, x['note'])

os.makedirs(OUT_DIR, exist_ok=True)
json.dump({"rows": rows, "counts": dict(cnt)},
          open(os.path.join(OUT_DIR, "体系第一性健康度总览.json"), "w", encoding='utf-8'),
          ensure_ascii=False, indent=2)
open(os.path.join(OUT_DIR, "体系第一性健康度总览.md"), "w", encoding='utf-8').write(md)
print("体系健康度总览已生成：%d 体系；C=%d O=%d H=%d U=%d" %
      (len(rows), cnt.get('C', 0), cnt.get('O', 0), cnt.get('H', 0), cnt.get('U', 0)))
