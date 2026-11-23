# -*- coding: utf-8 -*-
"""attack71: price the remaining mSUGRA soft-breaking bridge.

Pure standard library; read-only source scan; no new physics and no git action.
"""
from __future__ import print_function

import io
import json
import os
import re
import sys
from decimal import Decimal, getcontext

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60
D = Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_NAME = "attack71_软破缺结构导出定价_零新增输入门槛与SUGRA重标记拒绝_2026-11-23"
OUT_JSON = os.path.join(HERE, BASE_NAME + ".json")
OUT_REPORT = os.path.join(HERE, BASE_NAME + "_report.txt")

SRC_ATTACK56_JSON = os.path.join(HERE, "attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.json")
SRC_ATTACK56_MD = os.path.join(HERE, "判定_attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.md")
SRC_ATTACK70_JSON = os.path.join(HERE, "attack70_attack56剩余两缺口定价_软破缺与引力结构导出判定_2026-11-23.json")
SRC_ATTACK70_MD = os.path.join(HERE, "判定_attack70_attack56剩余两缺口定价_软破缺与引力结构导出判定_2026-11-23.md")
SRC_CUNI_MD = os.path.join(HERE, "力的大统一方程_CUNI-v2_MSSM-SO10_2026-10-30.md")
SRC_P1_MD = os.path.join(HERE, "论文体系_Nature规范", "P1_力的大统一方程_MSSM-SO10.md")

entries = []
guards = []
cross_refs = []
self_corrections = []


def add(code, verdict, title, detail):
    entries.append({"code": code, "verdict": verdict, "title": title, "detail": detail})


def guard(code, name, ok, detail):
    guards.append({"code": code, "name": name,
                   "status": "PASS" if bool(ok) else "FAIL", "detail": str(detail)})
    return bool(ok)


def fs(x):
    return format(x, ".25E")


def jnum(x):
    if isinstance(x, D):
        return str(x)
    if isinstance(x, list):
        return [jnum(v) for v in x]
    if isinstance(x, dict):
        return {k: jnum(v) for k, v in x.items()}
    return x


def read_text(path):
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

SOURCE_NEEDLES = {
    SRC_ATTACK56_JSON: ["B_block_gate", "L4 软破缺块（mSUGRA 普适）", "counterfactuals"],
    SRC_ATTACK56_MD: ["软破缺结构性导出", "210/126", "gravitino"],
    SRC_ATTACK70_JSON: ["attack70", "soft_scan", "gravity_scan", "D14"],
    SRC_ATTACK70_MD: ["当前账本未供给", "k=0", "D-14"],
    SRC_CUNI_MD: ["L5 软破缺层", "m_0^2", "M_{1/2}", "\\mu\\,\\Phi_{10}\\Phi_{10}"],
    SRC_P1_MD: ["L5 软破缺", "M_SUSY=1 TeV 为输入假设"],
}
source_state = []
for path, needles in SOURCE_NEEDLES.items():
    exists = os.path.isfile(path)
    text = read_text(path) if exists else ""
    missing = [n for n in needles if n not in text]
    source_state.append({"path": os.path.relpath(path, HERE), "exists": exists,
                         "needles": len(needles), "missing": missing})

guard("G0-1", "all six fact sources exist", all(s["exists"] for s in source_state), str(source_state))
guard("G0-2", "all fact-source needles hit", all(len(s["missing"]) == 0 for s in source_state), str(source_state))

with io.open(SRC_ATTACK56_JSON, "r", encoding="utf-8") as f:
    src56 = json.load(f)
with io.open(SRC_ATTACK70_JSON, "r", encoding="utf-8") as f:
    src70 = json.load(f)

bg = src56["B_block_gate"]
soft56 = next(b for b in bg["blocks"] if b["block"].startswith("L4"))
grav56 = next(b for b in bg["blocks"] if b["block"].startswith("L5"))
current_total = D(str(bg["total_mSUGRA"]["delta"]))
negative_sum = D(str(bg["negative_sum"]))
current_soft_delta = D(str(soft56["delta"]))
current_grav_delta = D(str(grav56["delta"]))
attack70_soft_min_k = src70["D14"]["soft_min_k"]

guard("G0-3", "attack56 current ledger still +2", current_total == D(2), str(current_total))
guard("G0-4", "attack56 soft block is +5 AXIOM_SWAP R=0",
      current_soft_delta == D(5) and soft56["class"] == "AXIOM_SWAP" and soft56["R"] == 0,
      str(soft56))
guard("G0-5", "attack56 gravity block is +2 AXIOM_SWAP R=0",
      current_grav_delta == D(2) and grav56["class"] == "AXIOM_SWAP" and grav56["R"] == 0,
      str(grav56))
guard("G0-6", "attack70 soft minimum k is 3", int(attack70_soft_min_k) == 3, str(attack70_soft_min_k))
CLOSED_PATTERNS = [
    r"m_0\s*=",
    r"m0\s*=",
    r"M_\{1/2\}\s*=",
    r"M1/2\s*=",
    r"A_0\s*=",
    r"A0\s*=",
    r"B_\\mu\s*=",
    r"B\\mu\s*=",
    r"Bmu\s*=",
    r"\\mu\s*=",
]


def scan_closed_forms(text):
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pat in CLOSED_PATTERNS:
            if re.search(pat, line):
                hits.append({"line": lineno, "pattern": pat, "text": line.strip()[:180]})
    return hits


closed_hits = []
for s in source_state:
    if not s["exists"]:
        continue
    path = os.path.join(HERE, s["path"])
    for hit in scan_closed_forms(read_text(path)):
        row = dict(hit)
        row["file"] = s["path"]
        closed_hits.append(row)

positive_control = scan_closed_forms("m_0 = f(m_{3/2})\nM_{1/2} = c m_{3/2}\n")
negative_control = scan_closed_forms("L_soft = -m_0^2 |f|^2 - M_{1/2} gg\n")

guard("G1-1", "no closed mSUGRA relation in six fact sources", len(closed_hits) == 0, str(closed_hits[:5]))
guard("G1-2", "closed-form scanner has a positive control", len(positive_control) >= 2, str(positive_control))
guard("G1-3", "closed-form scanner has a negative control", len(negative_control) == 0, str(negative_control))

grid = []
for d in range(0, 5):
    for k in range(0, 6):
        delta_soft = D(5) - D(k) + D(d)
        total = negative_sum + delta_soft + current_grav_delta
        grid.append({"d_new_inputs": d, "k_derived_outputs": k,
                     "delta_soft": str(delta_soft), "delta_total": str(total),
                     "gate": D(total) < D(0), "needed": D(k) - D(d) >= D(3)})
gate_cells = [row for row in grid if row["gate"]]
need_cells = [row for row in grid if row["needed"]]
guard("G1-4", "gate cells exactly match k-d>=3",
      [row["gate"] for row in grid] == [row["needed"] for row in grid],
      str((len(gate_cells), len(need_cells))))
guard("G1-5", "zero-new-input requires k>=3 only",
      all(row["gate"] == (row["k_derived_outputs"] >= 3) for row in grid if row["d_new_inputs"] == 0),
      str([row for row in grid if row["d_new_inputs"] == 0]))

CANDIDATES = [
    {"id": "C01", "name": "当前 CUNI-v2 账本", "k": 0, "d": 0, "status": "REAL"},
    {"id": "C02", "name": "只把 m3/2 当新输入并乐观导出三项", "k": 3, "d": 1, "status": "NEW-INPUT"},
    {"id": "C03", "name": "m3/2 + Kähler/F 数据，乐观导出四项", "k": 4, "d": 2, "status": "NEW-INPUT"},
    {"id": "C04", "name": "m3/2 + Kähler/F + gauge kinetic，五项全导出", "k": 5, "d": 3, "status": "NEW-INPUT"},
    {"id": "C05", "name": "假设零新增输入直接导出三项", "k": 3, "d": 0, "status": "HYPOTHETICAL"},
]
for row in CANDIDATES:
    total = D(2) + D(row["d"]) - D(row["k"])
    row["delta_total"] = str(total)
    row["gate"] = total < D(0)

guard("G1-6", "current candidate C01 fails", not CANDIDATES[0]["gate"], str(CANDIDATES[0]))
guard("G1-7", "m3/2-as-new-input optimistic candidate C02 gives total 0 and fails",
      D(CANDIDATES[1]["delta_total"]) == D(0) and not CANDIDATES[1]["gate"], str(CANDIDATES[1]))
guard("G1-8", "all-new-inputs candidate C04 also fails", not CANDIDATES[3]["gate"], str(CANDIDATES[3]))
guard("G1-9", "zero-new-input hypothetical C05 opens, proving criterion is falsifiable",
      CANDIDATES[4]["gate"] and D(CANDIDATES[4]["delta_total"]) == D(-1), str(CANDIDATES[4]))
guard("G1-10", "no candidate with d>=3 can pass because k<=5",
      all(not row["gate"] for row in grid if row["d_new_inputs"] >= 3 and row["k_derived_outputs"] <= 5),
      "ok")
D15 = {
    "rule": "SOFT-BRIDGE-ACCOUNTING",
    "formula": "delta_total = 2 + d - k; k=derived soft outputs, d=new independent inputs",
    "gate": "k - d >= 3",
    "reason": "re-expressing the same five parameters through Kähler/F/m3/2 does not reduce a unless those objects are already counted structure",
}

add("F01", "PASS", "六个事实源 6/6 实到，针词全命中",
    "attack56 JSON/判定、attack70 JSON/判定、CUNI-v2 母册、P1 论文均只读载入；未改任何源字节。")
add("F02", "PASS", "CUNI-v2 的 L5 只书写软破缺拉氏量，μ 仍是超势自由项",
    "母册第 50 行列 m0/M1/2/A/Bmu，第 42 行 W 中 μΦ10Φ10 直接以参数出现；没有从 210/126 扇区反解这些量的公式。")
add("F03", "PASS", "P1 论文把 M_SUSY=1 TeV 明记为输入假设",
    "P1 局限段逐字写明该阈值是输入；这与 attack56 的 AXIOM_SWAP、R=0 记账一致。")
add("F04", "PASS", "attack56 §11 把软破缺结构导出列为开放项，attack70 已判 k=0",
    "事实源没有把 210/126 F 项与 gravitino 质量写成五个 mSUGRA 参数的闭式；本册扫描进一步确认零命中。")
add("S01", "PASS", "闭式扫描器有阳性对照与阴性对照",
    "注入 m_0=f(m3/2)、M1/2=c m3/2 时命中≥2；仅写 L_soft 参数列表时命中 0，排除扫描器恒假或恒真。")
add("S02", "FAIL", "六个事实源中 m0/M1/2/A0/mu/Bmu 的闭式关系命中 0",
    "10 个闭式形态正则逐行扫描，命中清单为空；因此当前 k=0，d=0，软桥没有可入账的结构输出。")
add("A01", "PASS", "软桥总账通式为 delta_total=2+d-k",
    "从 attack56 当前总账 +2 出发，新增 d 个独立输入使 a 上升，导出 k 个软参数使 a 下降；负号三块 -5 与软块 +5 已含在常数 2 中。")
add("A02", "PASS", "严格门等价于 k-d>=3",
    "整数网格 d=0..4、k=0..5 中 gate 单元格与 k-d>=3 单元格逐格相同；delta<=0 的变异判据被排除。")
add("A03", "FAIL", "当前账本 d=0,k=0，总账仍 +2",
    "这是 CUNI-v2/attack56/attack70 的共同现状；软破缺桥没有把门打开。")
add("A04", "FAIL", "即便乐观假设 m3/2 作为新输入可导出三项，总账也只有 0",
    "k=3,d=1 得 delta_total=0，严格门失败；把 m3/2 说成结构输出前必须证明它已由既有输入导出，否则它仍是新输入。")
add("A05", "FAIL", "Kähler/F 与 gauge kinetic 若作为新输入，五项全导出也不够",
    "k=5,d=3 得 delta_total=0；d>=3 时需 k>=6，但软参数只有 5 个，故任何三新输入以上的重标记路线在 attack55 门下不可能净下降。")
add("A06", "CORRECTED", "SUGRA 重标记不等于结构导出",
    "把 m0/M1/2 改写成 Kähler 导数、gauge kinetic function 与 F 项的公式，只是换变量；若这些对象未在原账本中计为既有结构，必须计入 d。")
add("A07", "PASS", "阳性对照：零新增输入导出三项即可打开门",
    "k=3,d=0 得 delta_total=-1；说明本册判据能给出过门解，不是把结论硬编码为 FAIL。")
add("B01", "FAIL", "当前唯一突破口在零新增输入口径下未实现",
    "软桥要求 k-d>=3，而事实源 k-d=0；结合 attack70 引力路径，attack56 的 +2 总账保持不变。")
add("B02", "PASS", "新增 D-15：软桥记账必须 Net=k-d，而非只数被重标记的软参数",
    "净结构输出数才是 attack55 的 e；新增对象 d 回到 a，不能免费消去。")
add("B03", "BOUNDARY", "若存在未入库的新结构扇区，须重跑而非由本册外推",
    "只有给出无新增独立常数、且至少三项软参数由既有 GUT 变量唯一决定的闭式，才可把 k-d 抬到 3；本册不宣称该机制不存在。")
add("B04", "INFO", "标准 SUGRA 中介公式按 [C] 级背景，不作为库内事实源",
    "本册只做账本与库内文本扫描，不引入外部公式充当本库已证事实。")
add("B05", "PASS", "红线保持不变",
    "不新增 L3 预言、不宣称四力统一；对外读数仍为 0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条。")
add("X01", "INFO", "取号：attack71 起草前磁盘零命中",
    "attack70 为当前上界，attack71 首空；只读扫描未触碰并行会话文件。")
add("X02", "INFO", "治理：未改 verify.py、未跑 refresh_catalog.py、未做 git",
    "产物仅本引擎 .py/.json/_report.txt、判定册与 README 登记。")

cross_refs = [
    {"target": "attack56 §11-①", "relation": "开放项", "detail": "软破缺结构导出被明确列为下一步，非已完成。"},
    {"target": "attack70 D14", "relation": "判据承接", "detail": "导出新输入只给零增量；attack71 加入 d 记账推广。"},
    {"target": "CUNI-v2 L4/L5", "relation": "事实源", "detail": "μ 为超势自由项，软参数只作为拉氏量项列出。"},
    {"target": "P1 局限段", "relation": "互印", "detail": "M_SUSY=1 TeV 为输入假设。"},
]
self_corrections.append("SC1 初稿只数 k，未把 Kähler/F/m3/2 的新增自由度计入 d；按 attack55 的 a/e 定义改为 Net=k-d。")
self_corrections.append("SC2 “导出五个软参数”不能自动判过门；d>=3 时 k-d<=2，严格门仍失败。")
self_corrections.append("SC3 闭式正则首版把 B_\\mu 写成单反斜杠导致 re.error bad escape；已改为双反斜杠并复跑。")

guard("G-C1", "entries >= 20", len(entries) >= 20, str(len(entries)))
guard("G-C2", "guards >= 17 at self-check point", len(guards) >= 17, str(len(guards)))
guard("G-C3", "unique entry codes", len({e["code"] for e in entries}) == len(entries), str(len(entries)))
guard("G-C4", "key entries present",
      all(any(e["code"] == k for e in entries) for k in ["F02", "S02", "A02", "A04", "A05", "B01", "B02"]),
      "ok")
guard("G-C5", "source_state has six entries and all needles hit",
      len(source_state) == 6 and all(len(s["missing"]) == 0 for s in source_state), str(len(source_state)))
guard("G-C6", "closed-form scan and controls are coherent",
      len(closed_hits) == 0 and len(positive_control) >= 2 and len(negative_control) == 0,
      str((len(closed_hits), len(positive_control), len(negative_control))))

counts = {}
for e in entries:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
guard("G-C7", "counts sum to entries", sum(counts.values()) == len(entries), str(counts))

all_ok = all(g["status"] == "PASS" for g in guards)
exit_code = 0 if all_ok else 1

payload = {
    "round": "attack71",
    "title": "attack56 软破缺结构导出定价：零新增输入门槛与 SUGRA 重标记拒绝",
    "date": "2026-11-23",
    "source": "attack56 §11-① + attack70 D14 + CUNI-v2 L4/L5 + P1 limitation",
    "scope": "库内事实源扫描与 attack55/69 账本判据；不引入外部公式充当库内已证事实",
    "verdict": "SOFT-BRIDGE-CLOSED-AT-ZERO-NEW-INPUT--DELTA-TOTAL-2-PLUS-D-MINUS-K--SUGRA-RELABEL-NOT-DERIVATION--NO-CURRENT-GATE-EXIT",
    "counts": counts,
    "entries_total": len(entries),
    "guard_pass": sum(1 for g in guards if g["status"] == "PASS"),
    "guard_total": len(guards),
    "exit_code": exit_code,
    "items": entries,
    "guards": guards,
    "self_corrections": self_corrections,
    "cross_refs": cross_refs,
    "sources": source_state,
    "closed_form_hits": closed_hits,
    "closed_form_patterns": CLOSED_PATTERNS,
    "scanner_controls": {"positive_hits": len(positive_control), "negative_hits": len(negative_control)},
    "soft_bridge_grid": grid,
    "candidates": CANDIDATES,
    "D15": D15,
}

with io.open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(jnum(payload), f, ensure_ascii=False, indent=2)

lines = []
lines.append("attack71 report - 软破缺结构导出定价：零新增输入门槛与 SUGRA 重标记拒绝")
lines.append("date: 2026-11-23")
lines.append("entries: " + str(len(entries)) + " ; counts: " + str(counts))
lines.append("guards: " + str(payload["guard_pass"]) + "/" + str(payload["guard_total"]) +
             " PASS ; exit=" + str(exit_code))
lines.append("")
for e in entries:
    lines.append("[" + e["verdict"] + "] " + e["code"] + " : " + e["title"])
    lines.append("    " + e["detail"])
lines.append("")
lines.append("CLOSED FORM SCAN")
for s in source_state:
    lines.append("  " + s["path"] + " exists=" + str(s["exists"]) + " missing=" + str(s["missing"]))
lines.append("  hits=" + str(len(closed_hits)) + " positive_control=" + str(len(positive_control)) +
             " negative_control=" + str(len(negative_control)))
lines.append("")
lines.append("SOFT BRIDGE CANDIDATES")
for row in CANDIDATES:
    lines.append("  " + row["id"] + " k=" + str(row["k"]) + " d=" + str(row["d"]) +
                 " delta_total=" + row["delta_total"] + " gate=" + str(row["gate"]) +
                 " " + row["name"])
lines.append("")
lines.append("D15")
lines.append("  " + D15["rule"])
lines.append("  " + D15["formula"])
lines.append("  " + D15["gate"])
lines.append("")
lines.append("SELF CORRECTIONS")
for sc in self_corrections:
    lines.append("  " + sc)
with io.open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("entries=%d %s" % (len(entries), str(counts)))
print("guards=%d/%d exit=%d" % (payload["guard_pass"], payload["guard_total"], exit_code))
print("json=" + OUT_JSON)
print("report=" + OUT_REPORT)
sys.exit(exit_code)
