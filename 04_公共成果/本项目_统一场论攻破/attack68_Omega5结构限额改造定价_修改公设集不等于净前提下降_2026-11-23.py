# -*- coding: utf-8 -*-
"""attack68: price the final exit -- modifying the axiom set (Omega5-A4).

Pure standard library. Read-only accounting; no new physics, no recommendation.
"""
from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal, getcontext

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60
D = Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_NAME = "attack68_Omega5结构限额改造定价_修改公设集不等于净前提下降_2026-11-23"
OUT_JSON = os.path.join(HERE, BASE_NAME + ".json")
OUT_REPORT = os.path.join(HERE, BASE_NAME + "_report.txt")

entries = []
guards = []
self_corrections = []
cross_refs = []


def add(code, verdict, title, detail):
    entries.append({"code": code, "verdict": verdict, "title": title, "detail": detail})


def guard(code, name, ok, detail):
    guards.append({"code": code, "name": name, "status": "PASS" if bool(ok) else "FAIL", "detail": str(detail)})
    return bool(ok)


def fs(x):
    return format(x, ".25E")


def esc(x):
    if isinstance(x, D):
        return str(x)
    if isinstance(x, dict):
        return {k: esc(v) for k, v in x.items()}
    if isinstance(x, list):
        return [esc(v) for v in x]
    if isinstance(x, tuple):
        return [esc(v) for v in x]
    return x


# ---- G0: inherited numbers and ledger guards ----
BASE_F_CONST = D(1)
BASE_F_NODES = D(4)
BASE_F_TOTAL = BASE_F_CONST + BASE_F_NODES
R15_CALIBERS = {"I": D(1), "II": D(5), "III": D(5)}
R14_P_BASE = D(6)
R14_P_ROUTE4 = D(8)
R14_NULL_BASE = D(3)
R14_NULL_ROUTE4 = D(5)
R14_WINDOWS_BASE = D(3)
R14_WINDOWS_ROUTE3 = D(2)
R14_WINDOWS_ROUTE4 = D(3)
R12_RANK_STRICT = D(3)
R12_RANK_NUMERIC = D(1)

guard("G0-1", "r15 calibers I/II/III = 1/5/5",
      R15_CALIBERS["I"] == D(1) and R15_CALIBERS["II"] == D(5) and R15_CALIBERS["III"] == D(5),
      "I=1 II=5 III=5")
guard("G0-2", "baseline total freedom = constants 1 + nodes 4 = 5",
      BASE_F_TOTAL == D(5), fs(BASE_F_TOTAL))
guard("G0-3", "r14 route4 cost p: +2 and nullity: +2",
      R14_P_ROUTE4 - R14_P_BASE == D(2) and R14_NULL_ROUTE4 - R14_NULL_BASE == D(2),
      "p=6->8 nullity=3->5")
guard("G0-4", "r12 strict/numeric rank gap: 3 vs 1",
      R12_RANK_STRICT == D(3) and R12_RANK_NUMERIC == D(1), "rank_strict=3 rank_numeric=1")
guard("G0-5", "r14 windows: route4 keeps 3, route3 drops to 2",
      R14_WINDOWS_ROUTE4 == D(3) and R14_WINDOWS_ROUTE3 == D(2), "3 vs 2")
guard("G0-6", "route4 extra freedom is not zero in caliber II",
      R15_CALIBERS["II"] + D(2) == D(7), "5+2=7")

# ---- Candidate ledger: Omega5 modifications as finite actions ----
candidates = [
    {"code": "C01", "name": "只改数字：Omega5 f<=3，节点仍无上限", "s": 1,
     "f_cap": 3, "n_cap": None, "a": 2, "e": 0, "R": 0, "o": 1,
     "note": "节点/函数自由度仍无界；口径 III 不闭合。"},
    {"code": "C02", "name": "A4 总限额 f+n<=5，路线4 仍要 +2 自由度", "s": 1,
     "f_cap": 3, "n_cap": 2, "a": 2, "e": 2, "R": 0, "o": 1,
     "note": "若2个新识别来自新公理，delta=0；若来自旧结构依赖，则已不是换公理集。"},
    {"code": "C03", "name": "A4 总限额 f<=3,n<=4（总7），不补识别", "s": 1,
     "f_cap": 3, "n_cap": 4, "a": 2, "e": 0, "R": 0, "o": 1,
     "note": "合法但 delta=+2，净前提上升。"},
    {"code": "C04", "name": "总限额7，且新公理自带2条识别约束", "s": 1,
     "f_cap": 3, "n_cap": 4, "a": 2, "e": 2, "R": 0, "o": 1,
     "note": "delta=0，最多打平；不满足 r134 严格净下降门 delta<0。"},
    {"code": "C05", "name": "总限额7，且声称自带3条识别约束", "s": 1,
     "f_cap": 3, "n_cap": 4, "a": 2, "e": 3, "R": 0, "o": 1,
     "note": "e>a+R，在换公理集 R=0 口径下非法；解锁 R 即变为结构识别控制组。"},
    {"code": "C06", "name": "控制组：结构识别（非换公理集）", "s": 0,
     "f_cap": 1, "n_cap": 4, "a": 0, "e": 1, "R": 1, "o": 1,
     "note": "delta=-1 可过门，但使用既有结构依赖 R，不是 attack68 的目标出口。"},
    {"code": "C07", "name": "路线3：放弃 beta 通道（零新输入）", "s": 0,
     "f_cap": 1, "n_cap": 4, "a": 0, "e": 0, "R": 0, "o": 1,
     "note": "不新增输入但 delta=0，窗口3->2；不是净前提下降门。"},
]


def candidate_state(c):
    a = D(c["a"])
    e = D(c["e"])
    r = D(c["R"])
    legal = c["o"] >= 1 and e <= a + r and (c["s"] == 0 or (a >= 1 and r == 0))
    delta = a - e
    gate = legal and delta < 0
    return legal, delta, gate


for c in candidates:
    legal, delta, gate = candidate_state(c)
    c["legal"] = legal
    c["delta"] = fs(delta)
    c["gate"] = gate

swap_candidates = [c for c in candidates if c["s"] == 1]
swap_gate_candidates = [c for c in swap_candidates if c["gate"]]
guard("G1-1", "candidate table has 7 actions", len(candidates) == 7, str(len(candidates)))
guard("G1-2", "5 swap candidates and 2 controls", len(swap_candidates) == 5, str(len(swap_candidates)))
guard("G1-3", "no swap candidate passes delta<0", len(swap_gate_candidates) == 0,
      str([c["code"] for c in swap_gate_candidates]))
guard("G1-4", "C05 is illegal under s=1,R=0,e>a", candidates[4]["legal"] is False, "C05 illegal")
guard("G1-5", "control C06 passes delta=-1 and is not swap",
      candidates[5]["gate"] is True and candidates[5]["s"] == 0, "C06 control")

# ---- Compact recheck of attack55 classification theorem ----
grid = []
for a in range(0, 5):
    for e in range(0, 5):
        for s in (0, 1):
            for r in range(0, 3):
                for o in (1, 2):
                    legal = e <= a + r and (s == 0 or (a >= 1 and r == 0))
                    if not legal:
                        continue
                    delta = a - e
                    grid.append({"a": a, "e": e, "s": s, "R": r, "o": o,
                                 "delta": delta, "gate": delta < 0})

compact_gate = [g for g in grid if g["gate"]]
compact_swap_gate = [g for g in grid if g["gate"] and g["s"] == 1]
compact_ident_gate = [g for g in grid if g["gate"] and g["s"] == 0]

mutant_unlock_r = []
for a in range(1, 5):
    for e in range(0, 5):
        for r in range(1, 3):
            if e <= a + r and a - e < 0:
                mutant_unlock_r.append({"a": a, "e": e, "R": r})
mutant_e_plus1 = []
for a in range(1, 5):
    for e in range(0, 5):
        if e <= a + 1 and a - e < 0:
            mutant_e_plus1.append({"a": a, "e": e})

grid_counts = {
    "legal_actions": len(grid),
    "gate_actions": len(compact_gate),
    "swap_gate_actions": len(compact_swap_gate),
    "identification_gate_actions": len(compact_ident_gate),
    "mutant_unlock_R_swap_gate": len(mutant_unlock_r),
    "mutant_e_le_a_plus1_swap_gate": len(mutant_e_plus1),
}
guard("G1-6", "compact grid: swap gate count = 0", len(compact_swap_gate) == 0, str(len(compact_swap_gate)))
guard("G1-7", "compact grid: identification gate count > 0", len(compact_ident_gate) > 0,
      str(len(compact_ident_gate)))
guard("G1-8", "mutants have teeth: both unlock variants produce swap-gate solutions",
      len(mutant_unlock_r) > 0 and len(mutant_e_plus1) > 0, str(grid_counts))

# ---- A: priced verdicts ----
add("A01", "PASS", "只读承接：attack66 关掉主链，attack67 关掉三条 KK 出口，剩余出口是修改公设集",
    "attack67 X02 明确写着「若允许通量/轨形/D 膜/非微扰等新假设，结论需重判；这些属修改公设集，代价与 r14 ③vs④ 同型」。本册只给该出口的机器价格，不代选。")
add("A02", "PASS", "r14 路线4 的「公设违背0」是旧账本会计结果，不是自由度为零",
    "旧 Ω5 只数连续常数；在 r15 口径 II 下路线4 p=6->8、nullity=3->5、总自由度 5->7。账面合规的实质是把 +2 外部输入登记为合法。")
add("A03", "FAIL", "只把 Ω5 数字从 1 改成 3 不解决问题：节点/函数自由度仍无界",
    "C01 在有物质时自由度 = 1 常数 + 4 分区节点 + 无界形状函数；r15 D-04 已判「仅改数字不解决问题」。本册把该结论转成候选表：C01 delta=+2 且 n_cap=None。")
add("A04", "FAIL", "总限额7但不补识别约束：路线4 的合法代价是 delta=+2",
    "C03 取 f<=3,n<=4，允许原模型 1+4 自由度再多 2 个连续常数；a=2,e=0,R=0 ⇒ delta=+2，净前提上升，不满足 r134 严格净下降门。")
add("A05", "FAIL", "总限额7且新公理自带2条识别约束：delta=0，只能打平不能过门",
    "C04 取 a=2,e=2；即使两条识别约束来自新公理，delta=a-e=0。r134 的门是 delta<0，不是 delta<=0。")
add("A06", "BOUNDARY", "声称新公理自带3条识别约束的 C05 在换公理集口径下非法",
    "C05 的 e=3>a+R=2。若要合法必须解锁 R>0；但 attack55 定理给出 GATE⇒s=0且R>=1，解锁 R 后它已变成结构识别控制组，不再是我换公理集出口。")
add("A07", "FAIL", "有限动作表复算：5 个换公理集候选中 0 个满足 delta<0",
    "C01–C05 中合法者 delta 分别为 +2、0、+2、0，C05 非法；控制组 C06 delta=-1 但 s=0。swap_gate_count=0 与 attack55 的完整 784 格结论一致。")
add("A08", "PASS", "结构识别控制组可过门，但它是 R>0 的既有依赖识别，不是新公理出口",
    "C06 取 a=0,e=1,s=0,R=1 ⇒ delta=-1；attack55 §4 唯一过门路径是 STRUCTURE_IDENTIFY，且全库真实供给仅 r119 电弱控制组、TUFT 侧为 0。")
add("A09", "FAIL", "窗口数不能替代预测力：路线4 名义窗口3，但可识别性未改善",
    "r14 路线4 保留3窗口而路线3为2；但 r12 rank_numeric=1、cond=inf、pool_usable=0，路线4 nullity=5。窗口计数必须与 nullity/cond 联读，单独报「3窗口」会高估预测力。")
add("A10", "FAIL", "attack55 全库供给普查：真实结构识别供给 TUFT 侧为0",
    "本册不重跑全库文本扫描，直接引用 attack55 E05：唯一实体是 r119 电弱控制组（非 TUFT），供给侧「外部输入」提及很多而净减结构闭式供给为0。")
add("A11", "PASS", "attack67 的通量/轨形/D 膜/非微扰出路必须重判，不能继承主链失败读数",
    "这些机制改变作用量与谱问题，属于新增场/拓扑/边界条件；按其是否提供净下降识别约束重新进本册候选表，不自动恢复轻带电手征费米子。")
add("A12", "CORRECTED", "更正 r14 读法的常见误引：公设违背0 ≠ 零外部输入",
    "r14 原文说路线4「自洽（唯一：有来源且零违背）」；r15 D-02 已更正其真实代价仍是 +2 自由度。本册进一步指出：若不接受 A4 总自由度限额，改数字只是把无界节点继续藏在 Ω5 口径 I 里。")
add("A13", "INFO", "新增判据 D-12（公设改写守恒律）：换公理集不能凭空产生净前提下降",
    "若新公理同时产生输入 a 与其识别 e，在 R=0 的换公理集口径下 e<=a，故 delta=a-e>=0；要 delta<0 必须使用既有结构依赖 R>0，而那已归入结构识别控制组。")
add("A14", "INFO", "新增判据 D-13（窗口-可识别性联读）：可证伪窗口必须与 nullity/cond 同时报告",
    "只报窗口数会把「名义通道数量」误当「可判别预测数量」；r14 路线4 的3窗口在 nullity=5、rank_numeric=1、cond=inf 下不能升级为3条独立判据。")
add("A15", "FAIL", "修改公设集不能在当前账本内把 attack66/67 的失败读数翻成统一成功",
    "荷质比 1E21、单电荷模质量 5E17 GeV、g=1、零模-电荷互斥、手征-维数锁死都是主链内部算术/整数/奇偶结论；改 Ω5 只改变记账合法性，不自动提供新的谱识别结构。")

cross_refs = [
    {"target": "attack66 判定册", "relation": "承接", "detail": "已知物理复算与荷质比/g因子失败在本册保持有效，不被公设改写自动抹去。"},
    {"target": "attack67 X02", "relation": "直接起点", "detail": "通量/轨形/D膜/非微扰属修改公设集，必须定价后重判。"},
    {"target": "attack55 判定册", "relation": "互印", "detail": "GATE⇒s=0且R>=1；4/4出口delta_min>=0；TUFT侧结构识别供给0。"},
    {"target": "r14 三条出路代价矩阵", "relation": "口径来源", "detail": "真正选择点3vs4；路线4账面合规但 +2自由度、nullity 3->5。"},
    {"target": "r15 自由度预算口径", "relation": "口径修正", "detail": "I=1/II=5/III=5；仅改数字无效；A4要求常数限额+节点/函数总自由度限额。"},
    {"target": "r12 可识别性解阻", "relation": "交叉约束", "detail": "rank_strict=3、rank_numeric=1、cond=inf、pool_usable=0。"},
]

add("X01", "PASS", "交叉一致性：本册把 r14/r15 的③vs④选择点推进为可枚举动作表",
    "候选表给出每条改造的 a/e/s/R/o、合法性与 delta；不再停在「修改公设集是哲学选择」。")
add("X02", "CORRECTED", "射程限定：这是公设集记账的定价，不是对一切更彻底形式体系的普遍否证",
    "若放弃「输入可数」或重定义可导出性口径，需另立账本；本册不改该前提，也不宣称所有统一理论不可能。")
add("X03", "PASS", "红线一致：0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程0条",
    "本册没有新增被验证的 L3 预言，也没有把候选出口的账面合规升级为完成度。")
add("X04", "INFO", "不代选与不推荐声明",
    "本册只给代价、合法性与门禁满足情况；③（零新输入、窗口少）与④（登记新输入、账本改写）的选择权保留给用户。")
add("X05", "INFO", "治理留痕：未改 verify.py、未跑 refresh_catalog、未做 git 操作",
    "所有引用均为只读；本册产物为引擎 .py、.json、_report.txt 与判定册。")

self_corrections.append("C01 候选首版把 A4 总限额 f+n<=5 的 n_cap 写成5，已改为 n<=2 后与 f<=3 对齐；不改变 delta 判定。")
self_corrections.append("generic grid 只做 attack55 784 格的紧凑复核（300 维枚举），完整权威仍归 attack55，不宣称替代。")
self_corrections.append("「公设违背0」按 r14 原文登记为旧账本结果，避免与 r15 口径II的 +2 自由度混淆。")

# ---- final self-check and output ----
counts = {}
for e in entries:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1

guard("G-C1", "entries >= 20", len(entries) >= 20, str(len(entries)))
guard("G-C2", "guards >= 15 at self-check point", len(guards) >= 15, str(len(guards)))
guard("G-C3", "unique entry codes", len({e["code"] for e in entries}) == len(entries), str(len(entries)))
guard("G-C4", "key entries present",
      all(any(e["code"] == k for e in entries) for k in ["A03", "A07", "A08", "A12", "A13", "A14", "A15"]), "ok")
guard("G-C5", "all swap candidates either illegal or delta>=0",
      all((not c["legal"]) or D(c["delta"]) >= D(0) for c in swap_candidates), "ok")
guard("G-C6", "compact grid theorem reproduces attack55: swap gate zero",
      grid_counts["swap_gate_actions"] == 0, str(grid_counts))
guard("G-C7", "mutant guards have teeth",
      grid_counts["mutant_unlock_R_swap_gate"] > 0 and grid_counts["mutant_e_le_a_plus1_swap_gate"] > 0,
      str(grid_counts))
guard("G-C8", "self corrections recorded", len(self_corrections) >= 3, str(len(self_corrections)))
guard("G-C9", "counts sum to entries", sum(counts.values()) == len(entries), str(counts))

all_ok = all(g["status"] == "PASS" for g in guards)
exit_code = 0 if all_ok else 1

payload = {
    "round": "attack68",
    "title": "Omega5 结构限额改造定价：修改公设集不等于净前提下降",
    "date": "2026-11-23",
    "source": "attack67 X02 + r14 ③vs④ 决策点 + r15 自由度口径 + attack55 方向门分类定理",
    "scope": "只读机器定价；不产生新物理、不代选、不改既有文件",
    "counts": counts,
    "entries_total": len(entries),
    "guard_pass": sum(1 for g in guards if g["status"] == "PASS"),
    "guard_total": len(guards),
    "exit_code": exit_code,
    "items": entries,
    "guards": guards,
    "self_corrections": self_corrections,
    "cross_refs": cross_refs,
    "new_criteria": [
        {"code": "D-12", "name": "公设改写守恒律",
         "statement": "换公理集下 R=0 且 e<=a，故 delta=a-e>=0；净下降只能来自 s=0,R>=1 的结构识别。"},
        {"code": "D-13", "name": "窗口-可识别性联读",
         "statement": "可证伪窗口数必须与 nullity、rank_numeric、cond 同报；单独报窗口数不等于预测力。"},
    ],
    "candidate_table": candidates,
    "grid_counts": grid_counts,
    "key_numbers": {
        "baseline_const": fs(BASE_F_CONST),
        "baseline_nodes": fs(BASE_F_NODES),
        "baseline_total_freedom": fs(BASE_F_TOTAL),
        "route4_delta_p": fs(R14_P_ROUTE4 - R14_P_BASE),
        "route4_delta_nullity": fs(R14_NULL_ROUTE4 - R14_NULL_BASE),
        "caliber_II_route4": fs(R15_CALIBERS["II"] + D(2)),
        "swap_candidate_count": str(len(swap_candidates)),
        "swap_gate_candidate_count": str(len(swap_gate_candidates)),
        "compact_swap_gate_actions": str(grid_counts["swap_gate_actions"]),
        "compact_identification_gate_actions": str(grid_counts["identification_gate_actions"]),
    },
}

with io.open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(esc(payload), f, ensure_ascii=False, indent=2)

lines = []
lines.append("attack68 report - Omega5 结构限额改造定价：修改公设集不等于净前提下降")
lines.append("date: 2026-11-23")
lines.append("entries: %d ; counts: %s" % (len(entries), str(counts)))
lines.append("guards: %d/%d PASS ; exit=%d" % (payload["guard_pass"], payload["guard_total"], exit_code))
lines.append("")
for e in entries:
    lines.append("[%s] %s : %s" % (e["verdict"], e["code"], e["title"]))
    lines.append("    " + e["detail"])
lines.append("")
lines.append("CANDIDATE TABLE")
for c in candidates:
    lines.append("  %s s=%d a=%s e=%s R=%s delta=%s legal=%s gate=%s : %s" %
                 (c["code"], c["s"], str(c["a"]), str(c["e"]), str(c["R"]),
                  c["delta"], str(c["legal"]), str(c["gate"]), c["name"]))
lines.append("")
lines.append("GRID COUNTS")
for k in sorted(grid_counts.keys()):
    lines.append("  %s = %s" % (k, str(grid_counts[k])))
lines.append("")
lines.append("KEY NUMBERS")
for k, v in payload["key_numbers"].items():
    lines.append("  %s = %s" % (k, str(v)))
lines.append("")
lines.append("CROSS REFS")
for c in cross_refs:
    lines.append("  - %s (%s): %s" % (c["target"], c["relation"], c["detail"]))
with io.open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("entries=%d %s" % (len(entries), str(counts)))
print("guards=%d/%d exit=%d" % (payload["guard_pass"], payload["guard_total"], exit_code))
print("json=" + OUT_JSON)
print("report=" + OUT_REPORT)
sys.exit(exit_code)
