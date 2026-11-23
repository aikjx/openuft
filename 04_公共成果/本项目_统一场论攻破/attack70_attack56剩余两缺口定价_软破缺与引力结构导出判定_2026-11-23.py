# -*- coding: utf-8 -*-
"""attack70: price the two remaining attack56 gaps.

Pure standard library. Read-only on previous products except this engine's own
.json/_report.txt outputs. No new physics, no git operation.
"""
from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60
D = Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_NAME = "attack70_attack56剩余两缺口定价_软破缺与引力结构导出判定_2026-11-23"
OUT_JSON = os.path.join(HERE, BASE_NAME + ".json")
OUT_REPORT = os.path.join(HERE, BASE_NAME + "_report.txt")
SRC_ATTACK56 = os.path.join(HERE, "attack56_CUNI-v2二圈复算与方程块级净下降门_2026-11-10.json")

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


def ijson(x):
    if isinstance(x, D):
        return str(x)
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, list):
        return [ijson(v) for v in x]
    if isinstance(x, dict):
        return {k: ijson(v) for k, v in x.items()}
    return x


def relerr(a, b):
    return abs(a - b) / abs(b)


def gate(total):
    return D(total) < D(0)


guard("G0-1", "attack56 fact source exists", os.path.isfile(SRC_ATTACK56), SRC_ATTACK56)
with io.open(SRC_ATTACK56, "r", encoding="utf-8") as f:
    src56 = json.load(f)

bg = src56["B_block_gate"]
blocks = bg["blocks"]
block_by_name = {b["block"]: b for b in blocks}
soft = block_by_name["L4 软破缺块（mSUGRA 普适）"]
grav = block_by_name["L5 引力块（G 与 Lambda）"]
total_now = D(str(bg["total_mSUGRA"]["delta"]))
negative_sum = D(str(bg["negative_sum"]))
counter = bg["counterfactuals"]

loop2 = src56["A_two_loop"]["loop2"]
M_GUT_GEV = D(str(loop2["M_GUT_GeV"]))
ALPHA_GUT_INV = D(str(loop2["alpha_GUT_inv"]))
ALPHA_GUT = D(1) / ALPHA_GUT_INV

G_SI = D("6.67430e-11")
HBAR_SI = D("1.054571817e-34")
C_SI = D("299792458")
J_PER_GEV = D("1.602176634e-10")
RHO_LAMBMA_GEV4 = D("2.24e-12") ** 4

M_GUT_KG = M_GUT_GEV * J_PER_GEV / (C_SI * C_SI)
M_PLANCK_GEV = ((HBAR_SI * C_SI / G_SI).sqrt() / J_PER_GEV) * (C_SI * C_SI)
K_G_OBS = G_SI * M_GUT_KG * M_GUT_KG / (HBAR_SI * C_SI)
K_LAMBDA_OBS = RHO_LAMBMA_GEV4 / (M_GUT_GEV ** 4)
P_G_STAR = K_G_OBS.ln() / ALPHA_GUT.ln()
P_LAMBDA_STAR = K_LAMBDA_OBS.ln() / ALPHA_GUT.ln()

G_GRID = []
for p in range(-4, 5):
    kv = ALPHA_GUT ** p
    G_GRID.append({"p": p, "K": fs(kv), "rel_err": fs(relerr(kv, K_G_OBS))})
G_GRID_BEST = min(G_GRID, key=lambda row: D(row["rel_err"]))

guard("G0-2", "source round is attack56", src56.get("round") == "attack56", src56.get("round"))
guard("G0-3", "six ledger blocks present", len(blocks) == 6, str(len(blocks)))
guard("G0-4", "soft block ledger is +5 AXIOM_SWAP R=0",
      D(str(soft["delta"])) == D(5) and soft["class"] == "AXIOM_SWAP" and soft["R"] == 0,
      str(soft))
guard("G0-5", "gravity block ledger is +2 AXIOM_SWAP R=0",
      D(str(grav["delta"])) == D(2) and grav["class"] == "AXIOM_SWAP" and grav["R"] == 0,
      str(grav))
guard("G0-6", "current total remains +2 and fails strict gate",
      total_now == D(2) and not gate(total_now), str(total_now))
guard("G0-7", "structure-identify supply is -5", negative_sum == D(-5), str(negative_sum))
guard("G0-8", "attack56 counterfactual ledgers are -1/-4/-7",
      sorted(int(v) for v in counter.values()) == [-7, -4, -1], str(counter))
guard("G0-9", "M_GUT and alpha_GUT inherited from attack56 loop2",
      M_GUT_GEV > D(0) and ALPHA_GUT_INV > D(0), str(M_GUT_GEV) + " ; " + str(ALPHA_GUT_INV))
soft_scan = []
for k in range(0, 6):
    d_soft = D(5) - D(k)
    t_soft = negative_sum + d_soft + D(str(grav["delta"]))
    soft_scan.append({"derived_soft_inputs": k, "delta_soft": str(d_soft),
                      "delta_total": str(t_soft), "gate": gate(t_soft)})
grav_scan = []
for k in range(0, 4):
    d_grav = D(2) - D(k)
    t_grav = negative_sum + D(str(soft["delta"])) + d_grav
    grav_scan.append({"derived_gravity_inputs": k, "delta_gravity": str(d_grav),
                      "delta_total": str(t_grav), "gate": gate(t_grav)})

soft_min_k = min(row["derived_soft_inputs"] for row in soft_scan if row["gate"])
grav_min_k = min((row["derived_gravity_inputs"] for row in grav_scan if row["gate"]), default=None)
grav_full_derivation = next(row for row in grav_scan if row["derived_gravity_inputs"] == 2)

guard("G1-1", "soft path opens at k>=3 derived soft inputs",
      soft_min_k == 3 and soft_scan[3]["gate"] and not soft_scan[2]["gate"],
      str(soft_scan))
guard("G1-2", "soft k=0 keeps total +2", D(soft_scan[0]["delta_total"]) == D(2), str(soft_scan[0]))
guard("G1-3", "soft k=3 gives total -1 and opens strict gate",
      D(soft_scan[3]["delta_total"]) == D(-1) and soft_scan[3]["gate"], str(soft_scan[3]))
guard("G1-4", "gravity path needs k>=3, impossible with only G and Lambda outputs",
      grav_min_k == 3 and D(grav_scan[-2]["delta_total"]) == D(0) and not grav_scan[-2]["gate"],
      str(grav_scan))
guard("G1-5", "full derivation of two gravity inputs gives delta_total=0, not strict pass",
      D(grav_full_derivation["delta_total"]) == D(0) and not grav_full_derivation["gate"],
      str(grav_full_derivation))
guard("G1-6", "strict gate differs from non-positive mutant at gravity k=2",
      D(grav_full_derivation["delta_total"]) == D(0) and not gate(grav_full_derivation["delta_total"]),
      "strict delta<0 rejects zero")

guard("G2-1", "alpha_GUT is in (0,1)", D(0) < ALPHA_GUT and ALPHA_GUT < D(1), fs(ALPHA_GUT))
guard("G2-2", "required G exponent is strictly positive", P_G_STAR > D(0), fs(P_G_STAR))
guard("G2-3", "required G exponent is not an integer power of alpha_GUT",
      abs(P_G_STAR - P_G_STAR.to_integral_value()) > D("0.01"), fs(P_G_STAR))
guard("G2-4", "integer-power grid p=-4..4 cannot match K_G within 1e-3 relative error",
      D(G_GRID_BEST["rel_err"]) > D("0.001"), str(G_GRID_BEST))
guard("G2-5", "required Lambda exponent exceeds 4", P_LAMBDA_STAR > D(4), fs(P_LAMBDA_STAR))
guard("G2-6", "required Lambda coefficient is far below alpha_GUT^4",
      D(ALPHA_GUT) ** 4 > K_LAMBDA_OBS * D("1e100"), fs(K_LAMBDA_OBS))

D14 = {
    "rule": "DERIVE-NEW-INPUT-IS-ZERO-DELTA-NOT-NEGATIVE",
    "formal": "if n_after=k new inputs are converted into outputs, delta becomes 5-k or 2-k; strict gate requires delta_total<0, not <=0",
    "soft_min_k": soft_min_k,
    "gravity_min_k": grav_min_k,
}
add("A01", "PASS", "只读核入 attack56 原始账本，不重判二圈 RGE",
    "从 attack56 JSON 读取六个块、当前总账 +2、结构识别净减 -5 与三条反事实；本册不重跑 mpmath/RK4，不改 attack56 任何字节。")
add("A02", "PASS", "attack56 反事实总账逐位复现：-1 / -4 / -7",
    "引力导出 -1、软破缺导出 -4、两者同时 -7 三条反事实全部从原 JSON 读出并通过排序校验；确认上一轮筛出的突破口事实源存在。")
add("A03", "PASS", "结构识别三块净减 -5 保持，是全部负号来源",
    "规范 -2、Yukawa -1、seesaw -2 合计 -5；软破缺与引力仍为 AXIOM_SWAP 且 R=0，符号-动作类对应未被破坏。")
add("S01", "PASS", "软破缺路径的严格门槛：至少 3/5 个软参数必须由既有结构导出",
    "总账为 -5+(5-k)+2=2-k；严格门 delta_total<0 要求 k>=3，k=2 仍给 0，不够。")
add("S02", "FAIL", "当前软破缺块 k=0，attack56 事实源只给五个公理性软参数、无闭式关系",
    "attack56 evidence 明记 m0/M1/2/A0/mu/Bmu 五个软参数且普适性为新增公理，class=AXIOM_SWAP、R=0；当前账本没有可将其转成 STRUCTURE_IDENTIFY 的闭式。")
add("S03", "PASS", "阳性对照：若导出 3 个软参数，总账变为 -1，门真会打开",
    "k=3 时 delta_soft=+2、delta_total=-1；k=2 时 delta_total=0 仍不过严格门，证明判据不是恒真。")
add("S04", "CORRECTED", "attack56 软破缺反事实 +5→-1 强于必要门槛",
    "软破缺只需从 +5 降到 <=+2 即可让总账为负；+5→-1 是更强但非最小的反事实。本册不回改 attack56，只登记口径差。")
add("G01", "PASS", "引力路径的严格门槛：G/Λ 之外还必须有第三个结构识别单位",
    "若只处理 G、Λ，最多 k=2；总账 -5+5+(2-k)=2-k，k=2 给 0，严格门仍失败，必须 k>=3。")
add("G02", "FAIL", "即使 G 与 Λ 全部由统一点导出，总账也只到 0，不会自动过门",
    "全导出 k=2 后引力块 delta=0、总账=0；attack55/69 的严格门是 delta<0，不是 delta<=0。")
add("G03", "FAIL", "G 的 α_GUT 幂次要求非整数指数 4.1817",
    "用 attack56 的 M_GUT=1.4273005E16 GeV 与 alpha_GUT_inv=25.25645，K_G_obs=G·M_GUT^2/(hbar·c)=1.3667141E-6；令 K=alpha^p 得 p*=4.1817157，非整数。")
add("G04", "FAIL", "低阶 alpha_GUT 幂次穷举 p=-4..4 无法给出 K_G",
    "最接近的是 p=4，alpha^4=2.4575E-6，相对误差 79.82%；1e-4 阈值以内的解 0 个，说明当前统一点输入不自带 G 的规范系数。")
add("G05", "FAIL", "Λ 的所需系数比 alpha_GUT^4 还低约 100 个数量级",
    "取 rho_Lambda^(1/4)=2.24E-12 GeV [C]，K_Lambda=rho_Lambda/M_GUT^4=6.0663910E-112；alpha^p 需 p*=79.3064，远超低阶结构幂次。")
add("G06", "CORRECTED", "attack56 引力反事实 +2→-1 的代价被低估",
    "+2→0 只把总账抬到 0；要达到 -1 必须额外识别一个既有输入或给出 R=1 的结构依赖，不能把“导出 G/Λ”直接等同于“过门”。")
add("B01", "FAIL", "当前唯一严格过门类突破口在现有账本下未实现",
    "软破缺仍 k=0，引力仍 k=0；总账锁定 +2。attack66–69 关闭的是外部出口，本册关闭的是 attack56 内部剩余反事实在现有闭式下的可实现性。")
add("B02", "PASS", "新增 D-14：把新输入变成输出只给零增量，负增量必须来自既有结构识别",
    "若 k 个新输入被导出，delta 为 5-k 或 2-k；严格负总账还可来自 R>0 的既有输入识别。与 attack69 的 GATE⇒s=0且R>=1 逐条一致。")
add("B03", "BOUNDARY", "本册不是物理普遍 no-go",
    "若未来作用量新增扇区使五个软参数中至少三个变成结构输出，或给出 G/Λ 之外的一个既有结构识别，须重跑 attack56/70；本册只判当前账本。")
add("B04", "INFO", "外部常数按 [C] 级登记，不伪装第一性",
    "G、hbar、c 采用 CODATA/SI 固定值；rho_Lambda^(1/4)=2.24E-12 GeV 为观测锚 [C]，M_GUT 与 alpha_GUT 继承 attack56 loop2。")
add("B05", "PASS", "红线保持不变",
    "本册不新增 L3 预言、不宣称四力统一完成；唯一对外读数仍为 0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条。")
add("X01", "INFO", "取号与查重：attack70 起草前磁盘零命中",
    "动态实扫 attack70* 为 0，编号空闲；只读引用 attack56、attack61、attack66–69，不触碰并行会话文件。")
add("X02", "INFO", "治理：未改 verify.py、未跑 refresh_catalog.py、未做 git",
    "产物仅本引擎 .py/.json/_report.txt、判定册与 README 登记。")

cross_refs = [
    {"target": "attack56 B_block_gate", "relation": "事实源", "detail": "软破缺 +5、引力 +2、总账 +2、反事实 -1/-4/-7。"},
    {"target": "attack55/attack69 D-12", "relation": "判据承接", "detail": "严格门 delta<0；换公理集 e<=a 只给 delta>=0，负增量需 R>0。"},
    {"target": "attack61 E09", "relation": "边界互印", "detail": "外部 no-go 对该路径 OUT-OF-SCOPE，故本册的关闭来自内部账本而非外部定理。"},
    {"target": "attack66–69", "relation": "链尾", "detail": "外部 KK/公设集/求导出口已关闭，本册处理 attack56 内部剩余两缺口。"},
]
self_corrections.append("SC1 首轮构思曾把 delta<=0 当成过门；严格按 attack55 定义改为 delta<0 后，引力全导出读数为 0 且不过门。")
self_corrections.append("SC2 区分“把新输入变成输出”和“识别一个既有结构输入”：前者只升至 0，后者才可能给出严格负增量。")

guard("G-C1", "entries >= 20", len(entries) >= 20, str(len(entries)))
guard("G-C2", "guards >= 22 at self-check point", len(guards) >= 22, str(len(guards)))
guard("G-C3", "unique entry codes", len({e["code"] for e in entries}) == len(entries), str(len(entries)))
guard("G-C4", "key entries present",
      all(any(e["code"] == k for e in entries) for k in ["A02", "S01", "S02", "G01", "G02", "G03", "G05", "B01", "B02"]),
      "ok")
guard("G-C5", "soft evidence explicitly names five soft parameters and new axiom",
      "五个软参数" in soft["evidence"] and "新增公理" in soft["evidence"], str(soft["evidence"]))
guard("G-C6", "D14 thresholds are integers and gravity minimum is beyond output count",
      soft_min_k == 3 and grav_min_k == 3 and len(grav_scan) == 4, str(D14))

counts = {}
for e in entries:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
guard("G-C7", "counts sum to entries", sum(counts.values()) == len(entries), str(counts))

all_ok = all(g["status"] == "PASS" for g in guards)
exit_code = 0 if all_ok else 1

payload = {
    "round": "attack70",
    "title": "attack56 剩余两缺口定价：软破缺与引力结构导出判定",
    "date": "2026-11-23",
    "source": "attack56 B_block_gate + attack55/69 GATE + attack61 E09 boundary",
    "scope": "当前账本下的结构导出可实现性；不产生新物理，不做普遍物理 no-go",
    "verdict": "SOFT-GRAVITY-GAPS-PRICED--SOFT-NEEDS-THREE-OUTPUTS--GRAVITY-NEEDS-EXTRA-R--DELTA-TOTAL-STILL-PLUS-2--NO-CURRENT-BREAKTHROUGH",
    "counts": counts,
    "entries_total": len(entries),
    "guard_pass": sum(1 for g in guards if g["status"] == "PASS"),
    "guard_total": len(guards),
    "exit_code": exit_code,
    "items": entries,
    "guards": guards,
    "self_corrections": self_corrections,
    "cross_refs": cross_refs,
    "soft_scan": soft_scan,
    "gravity_scan": grav_scan,
    "D14": D14,
    "constants": {
        "M_GUT_GeV": fs(M_GUT_GEV),
        "alpha_GUT_inv": fs(ALPHA_GUT_INV),
        "alpha_GUT": fs(ALPHA_GUT),
        "M_Planck_GeV": fs(M_PLANCK_GEV),
        "K_G_obs": fs(K_G_OBS),
        "p_G_star": fs(P_G_STAR),
        "K_Lambda_obs": fs(K_LAMBDA_OBS),
        "p_Lambda_star": fs(P_LAMBDA_STAR),
    },
    "G_integer_power_grid": G_GRID,
    "G_grid_best": G_GRID_BEST,
}

with io.open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(ijson(payload), f, ensure_ascii=False, indent=2)

lines = []
lines.append("attack70 report - attack56 剩余两缺口定价：软破缺与引力结构导出判定")
lines.append("date: 2026-11-23")
lines.append("entries: %d ; counts: %s" % (len(entries), str(counts)))
lines.append("guards: %d/%d PASS ; exit=%d" %
             (payload["guard_pass"], payload["guard_total"], exit_code))
lines.append("")
for e in entries:
    lines.append("[" + e["verdict"] + "] " + e["code"] + " : " + e["title"])
    lines.append("    " + e["detail"])
lines.append("")
lines.append("SOFT PATH SCAN")
for row in soft_scan:
    lines.append("  k=" + str(row["derived_soft_inputs"]) +
                 " delta_soft=" + row["delta_soft"] +
                 " delta_total=" + row["delta_total"] +
                 " gate=" + str(row["gate"]))
lines.append("")
lines.append("GRAVITY PATH SCAN")
for row in grav_scan:
    lines.append("  k=" + str(row["derived_gravity_inputs"]) +
                 " delta_gravity=" + row["delta_gravity"] +
                 " delta_total=" + row["delta_total"] +
                 " gate=" + str(row["gate"]))
lines.append("")
lines.append("NUMERICAL BLOCK")
lines.append("  M_GUT_GeV = " + fs(M_GUT_GEV))
lines.append("  alpha_GUT = " + fs(ALPHA_GUT))
lines.append("  M_Planck_GeV = " + fs(M_PLANCK_GEV))
lines.append("  K_G_obs = " + fs(K_G_OBS))
lines.append("  p_G_star = " + fs(P_G_STAR))
lines.append("  G_grid_best = " + str(G_GRID_BEST))
lines.append("  K_Lambda_obs = " + fs(K_LAMBDA_OBS))
lines.append("  p_Lambda_star = " + fs(P_LAMBDA_STAR))
lines.append("")
lines.append("D14")
lines.append("  " + D14["rule"])
lines.append("  soft_min_k=" + str(soft_min_k) + " gravity_min_k=" + str(grav_min_k))
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
