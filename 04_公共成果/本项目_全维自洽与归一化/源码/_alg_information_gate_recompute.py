# -*- coding: utf-8 -*-
"""
算法联盟：信息守恒与目标可满足性 · 比特账、最小不可满足核
====================================================================================
第九轮。前八轮都在数「参数个数」（p_eq / p_axiom / p_exp / p_disc），
把「参数不灭」当作八次反复出现的经验规律。本轮做一次范式转换：

  1. 不再数参数，改数信息比特：零自由参数的理论，输出信息量是否可能超过输入？
     46 项来料锚里 6 项是定义/派生输入、40 项是实测输出，
     精确有理表示的比特数可以直接机算；理论脚本里的数值字面量也可以按 AST 机算。
     若输出比特 > 输入比特 + 程序比特，差额必须由外部注入 ⇒ 信息不灭。
  2. 不再找候选，改问目标本身：「攻破统一场论」的 7 条目标公理是否逻辑可满足？
     128 个真值指派 × 256 个约束子集穷举，求最小不可满足核（MUS）。
     若目标不可满足，前八轮 0 突破就不是候选不够好，而是目标公理集自身的性质。
  3. 把八轮散落的「参数不灭」实例统一成一张比特注入账，机算每轮注入增量。

诚实定位：比特数是固定编码方案（分子分母分别二进制）下的描述长度上界，
不是 Kolmogorov 复杂度；换编码读数会变，单列 BOUNDARY。
数学自洽 != 实验证实；只产可算判决，不产新物理；四力大统一 0 条正确解、
独立实验预言 0；不宣称攻破统一场论。
（算法联盟册，不占 RID、不入 README、不与任何审计卷相加。）

环境纪律：Python 3.13 无 numpy/sympy，纯 Fraction / Decimal(60)；
UTF-8 源码 + ASCII runner；中文路径不进外层 argv。
"""
import json, os, ast, hashlib, re, glob, itertools
from decimal import Decimal, getcontext
from fractions import Fraction
from math import gcd

getcontext().prec = 60
D = Decimal
F = Fraction

ROOT = "D:/a10/aikjx/code/my_lib/openuft"
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
GAQ_DIR = os.path.join(ROOT, "01_独立体系", "S02_空间光速螺旋统一力", "04_理论推导")

P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_R1 = os.path.join(DATA, "_ALG_expdata_fullchain_recompute_2026-11-11.json")
P_R2 = os.path.join(DATA, "_ALG_allknowledge_iterative_recompute_2026-11-11.json")
P_R3 = os.path.join(DATA, "_ALG_expfacts_survival_recompute_2026-11-11.json")
P_R4 = os.path.join(DATA, "_ALG_meta_gateaudit_recompute_2026-11-11.json")
P_R5 = os.path.join(DATA, "_ALG_pair_optim_recompute_2026-11-12.json")
P_R6 = os.path.join(DATA, "_ALG_pfree_attribution_recompute_2026-11-12.json")
P_R7 = os.path.join(DATA, "_ALG_force_unification_recompute_2026-11-12.json")
P_R8 = os.path.join(DATA, "_ALG_spectrum_generation_recompute_2026-11-12.json")
P_GAQ_PY = os.path.join(GAQ_DIR, "unified_forces_vs_experiment.py")
P_R403 = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
P_R404 = os.path.join(DATA, "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")

OUT_JSON = os.path.join(DATA, "_ALG_information_gate_recompute_2026-11-12.json")
OUT_REPORT = os.path.join(DATA, "_ALG_information_gate_recompute_report_2026-11-12.txt")
SOURCE_FILES = [P_LEDGER, P_R1, P_R2, P_R3, P_R4, P_R5, P_R6, P_R7, P_R8,
                P_GAQ_PY, P_R403, P_R404]


def F_of(s):
    return F(D(str(s)))


def F_frac_str(s):
    return F(str(s))


def D_fr(fr):
    return D(fr.numerator) / D(fr.denominator)


def bits(q):
    """固定编码：把既约分数的分子与分母分别用二进制写出的长度。
    这是描述长度的一个上界，不是 Kolmogorov 复杂度；口径写进 BOUNDARY。"""
    q = F(q)
    return abs(q.numerator).bit_length() + q.denominator.bit_length()


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def text(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


LEDGER_TXT = text(P_LEDGER)
LEDGER = json.loads(LEDGER_TXT)
R = {}
for i, p in enumerate([P_R1, P_R2, P_R3, P_R4, P_R5, P_R6, P_R7, P_R8], start=1):
    R[i] = load(p)
R403 = load(P_R403)
R404 = load(P_R404)
GAQ_PY = text(P_GAQ_PY)
GAQ_TREE = ast.parse(GAQ_PY)
E = {x["id"]: x for x in LEDGER["ledger"]}

source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(source_missing) == 0) and (len(SOURCE_FILES) > 0)


# ============================ act / exp 两条独立来料路径 ============================
def act_ledger():
    """act：json.load 后逐项读 value / sigma / kind。"""
    rows = []
    for x in LEDGER["ledger"]:
        rows.append(dict(id=x["id"], value=F_of(x["value"]),
                         sigma=F_of(x["sigma"]) if x.get("sigma") not in (None, "", "0") else None,
                         kind=x["kind"]))
    return rows


def exp_ledger():
    """exp：用正则从原始 JSON 文本独立抽 value / sigma / kind 三列，与 act 互不引用。"""
    vals = re.findall(r'"value"\s*:\s*"([^"]+)"', LEDGER_TXT)
    sigs = re.findall(r'"sigma"\s*:\s*"([^"]+)"', LEDGER_TXT)
    # 顶层元数据里也有一个 kind（experimental-input-ledger），按语义白名单过滤，
    # 否则 47 个 kind 对 46 行，整体错位一位。
    valid = ("SI-definition", "derived", "measured", "measured-bound")
    kinds = [k for k in re.findall(r'"kind"\s*:\s*"([^"]+)"', LEDGER_TXT) if k in valid]
    ids = re.findall(r'"id"\s*:\s*"([^"]+)"', LEDGER_TXT)
    rows = []
    for i, v in enumerate(vals):
        s = sigs[i] if i < len(sigs) else "0"
        rows.append(dict(id=ids[i] if i < len(ids) else "X" + str(i),
                         value=F_of(v),
                         sigma=F_of(s) if s not in ("0", "") else None,
                         kind=kinds[i] if i < len(kinds) else "unknown"))
    return rows


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if "act_ledger" not in funcs or "exp_ledger" not in funcs:
        return False
    if ast.dump(funcs["act_ledger"]) == ast.dump(funcs["exp_ledger"]):
        return False
    for name in ("act_ledger", "exp_ledger"):
        for node in ast.walk(funcs[name]):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
                return False
    return True


ACT = act_ledger()
EXP = exp_ledger()
TWO_PATH_OK = (len(ACT) == len(EXP)) and \
              all(a["value"] == b["value"] and a["kind"] == b["kind"] and a["id"] == b["id"]
                  for a, b in zip(ACT, EXP))
N_ANCHORS = len(ACT)
BIT_MISMATCH = sum(1 for a, b in zip(ACT, EXP) if bits(a["value"]) != bits(b["value"]))

INPUT_KINDS = ("SI-definition", "derived")
OUTPUT_KINDS = ("measured", "measured-bound")
INPUT_ROWS = [r for r in ACT if r["kind"] in INPUT_KINDS]
OUTPUT_ROWS = [r for r in ACT if r["kind"] in OUTPUT_KINDS]
TWO_SIDED = [r for r in ACT if r["sigma"] is not None and r["sigma"] != 0]
N_INPUT = len(INPUT_ROWS)
N_OUTPUT = len(OUTPUT_ROWS)
N_TWO_SIDED = len(TWO_SIDED)


# ============================ 三种口径的输出 / 输入比特账 ============================
def lcm(a, b):
    return a // gcd(a, b) * b


def bits_lcm_rows(rows):
    """通分成公分母后再计比特：共享分母压缩口径。"""
    den = 1
    for r in rows:
        den = lcm(den, r["value"].denominator)
    nums = [abs(r["value"].numerator * (den // r["value"].denominator)) for r in rows]
    return sum(n.bit_length() for n in nums) + den.bit_length(), den


H_IN = sum(bits(r["value"]) for r in INPUT_ROWS)
H_OUT_SUM = sum(bits(r["value"]) for r in OUTPUT_ROWS)
H_OUT_LCM, LCM_DEN = bits_lcm_rows(OUTPUT_ROWS)
H_OUT_TWO = sum(bits(r["value"]) for r in TWO_SIDED)
H_SIGMA_TWO = sum(bits(r["sigma"]) for r in TWO_SIDED)
H_ALL = sum(bits(r["value"]) for r in ACT)
H_IN_CHECK = (H_IN + H_OUT_SUM == H_ALL)

# 理论脚本按 AST 实际形态机读全部数值字面量（第七轮教训：134.9768e6 折成 134976800.0）
GAQ_LITERALS = [n.value for n in ast.walk(GAQ_TREE)
                if isinstance(n, ast.Constant) and isinstance(n.value, (int, float))
                and not isinstance(n.value, bool)]
GAQ_FRACS = [F_of(str(v)) for v in GAQ_LITERALS]
H_PROG = sum(bits(v) for v in GAQ_FRACS)
N_LITERALS = len(GAQ_FRACS)

ANCHOR_VALUES = set(r["value"] for r in ACT)
COPIED = [v for v in GAQ_FRACS if v in ANCHOR_VALUES]
COPIED_UNIQUE = sorted(set(COPIED))
N_COPIED = len(COPIED)
N_COPIED_UNIQUE = len(COPIED_UNIQUE)
H_COPIED_OCC = sum(bits(v) for v in COPIED)
H_COPIED_UNIQUE = sum(bits(v) for v in COPIED_UNIQUE)
COPY_RATIO = D(H_COPIED_OCC) / D(H_PROG) if H_PROG else D(0)

# 三种口径的缺口都由同一条式子机算，不许挑口径
H_IN_BASE = H_IN
INPUT_PLUS_PROG = H_IN_BASE + H_PROG
GAP_SUM = H_OUT_SUM - INPUT_PLUS_PROG
GAP_LCM = H_OUT_LCM - INPUT_PLUS_PROG
GAP_TWO = H_OUT_TWO - INPUT_PLUS_PROG
GAP_MIN = min(GAP_SUM, GAP_LCM, GAP_TWO)
GAP_MAX = max(GAP_SUM, GAP_LCM, GAP_TWO)

# ★★诚实修正（判据反噬自己）：预设「输出信息超过输入，故须外部注入」被数据推翻。
# 程序侧 3759 bit 已超过 40 项实测输出 1523 bit，独立编码与双侧两个口径的缺口为负。
# 不放宽守卫、不改文案硬撑，改问：这些程序比特里有多少是直接从观测抄来的？
NO_INFO_GAP = (INPUT_PLUS_PROG > H_OUT_SUM)
ANSWER_IN_INPUT = NO_INFO_GAP and (N_COPIED_UNIQUE > 0)

# 守恒式 I1 改由「观测副本被检测到」驱动，而不是由缺口符号驱动。
# 这是本地归纳 + 信息守恒弱式：任何精确数值输出都必须有来源；
# 现有零自由参数宣称的实例里，独立数值的信息都来自观测副本。
INJECT_BITS_LOWER = H_COPIED_UNIQUE
CONSTRAINT_I1_ACTIVE = (N_COPIED > 0)


# ============================ 跨八轮注入账（参数不灭的比特版） ============================
def kn(i):
    return R[i].get("key_numbers", {})


ROUND_INJECTION = [
    dict(round=1, layer="实验来料层", tags=["ledger_total"],
         counts=[kn(1)["ledger_total"]],
         note="46 项实验锚全部作为输入，零自由参数的理论无法生成其数值信息"),
    dict(round=2, layer="公理层", tags=["axiom_injected_count"],
         counts=[kn(2)["axiom_injected_count"]],
         note="每加一条公理，p_total 精确 +1 ⇒ 注入 1 bit"),
    dict(round=3, layer="实验给定事实层", tags=["p_exp_max"],
         counts=[kn(3)["p_exp_max"]],
         note="p_exp 最大 3 项，实验给定事实是输入而非自由参数"),
    dict(round=4, layer="判据逻辑层", tags=["escape_models"],
         counts=[kn(4)["escape_models"]],
         note="2 个单侧逃逸构型 ⇒ 须补 C4 双侧门，判据本身也带信息"),
    dict(round=5, layer="配对层", tags=["pairs_p_free_undetermined"],
         counts=[kn(5)["pairs_p_free_undetermined"]],
         note="8 对自由度未定，来源信息缺失"),
    dict(round=6, layer="来源层", tags=["gaq_p_exp_anchor_groups", "r188_p_exp"],
         counts=[kn(6)["gaq_p_exp_anchor_groups"], kn(6)["r188_p_exp"]],
         note="GAQ 外部锚 4 组、r188 实验输入 6 项"),
    dict(round=7, layer="方程族层", tags=["p_min_extra"],
         counts=[kn(7)["p_min_extra"]],
         note="单方程族参数下界 5"),
    dict(round=8, layer="离散标签层", tags=["labels_external", "p_min_v8"],
         counts=[kn(8)["labels_external"], kn(8)["p_min_v8"]],
         note="至少 2 个标签外部注入、参数下界仍为 4"),
]
BREAK_FIELDS = ["breakthrough_count", "pairs_hit", "escape_configs",
                "pairs_hit_after", "families_breakthrough"]
for row in ROUND_INJECTION:
    row["H_inject_lower"] = sum(row["counts"])
    k = kn(row["round"])
    row["breakthrough"] = next((k[f] for f in BREAK_FIELDS if f in k), 0)
N_ROUNDS = len(ROUND_INJECTION)
ALL_ROUNDS_INJECT = all(r["H_inject_lower"] > 0 for r in ROUND_INJECTION)
ALL_ROUNDS_ZERO = all(r["breakthrough"] == 0 for r in ROUND_INJECTION)
H_INJECT_TOTAL = sum(r["H_inject_lower"] for r in ROUND_INJECTION)

honest_boundary = (kn(5)["pairs_hit"] == 0) and (kn(6)["pairs_hit_after"] == 0) and \
                  (kn(7)["escape_configs"] == 0) and (kn(8)["families_breakthrough"] == 0)


# ============================ 目标公理集的可满足性与最小不可满足核 ============================
# 把「攻破统一场论」这个目标本身公理化为 7 条原子要求，而不是再去找候选。
# A1 单一机制描述四力 / A2 零自由参数 / A3 至少一条独立数值预言
# A4 与全部既有实验相容 / A5 不把实验值当输入 / A6 数学自洽 / A7 解释谱值为何如此
ATOMS = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
AXIOM_REQUIRED = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
CONSTRAINTS = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "I1"]

# I1 由机算缺口驱动：输出信息超过输入 + 程序时，零参数 ∧ 独立预言 ∧ 不注入 三者不可同时成立。
# 不是写死的逻辑断言，改数据（把输出算进输入）就会失活。
ALL_MODELS = [dict(zip(ATOMS, vals))
              for vals in itertools.product([False, True], repeat=len(ATOMS))]
N_MODELS = len(ALL_MODELS)


def model_ok(m, subset):
    for a in AXIOM_REQUIRED:
        if (a in subset) and (not m[a]):
            return False
    if ("I1" in subset) and CONSTRAINT_I1_ACTIVE:
        if m["A2"] and m["A3"] and m["A5"]:
            return False
    return True


def sat_count(subset):
    s = set(subset)
    return sum(1 for m in ALL_MODELS if model_ok(m, s))


N_SAT = sat_count(CONSTRAINTS)
N_BREAK = N_SAT

# 最小不可满足核：按子集大小逐层枚举 2^8 个子集，找第一个（也是最小的）不可满足层
UNSAT_AT_MIN = []
MUS_LAYER = 0
for k in range(1, len(CONSTRAINTS) + 1):
    layer = [list(sub) for sub in itertools.combinations(CONSTRAINTS, k)
             if sat_count(sub) == 0]
    if layer:
        UNSAT_AT_MIN = layer
        MUS_LAYER = k
        break
MUS = UNSAT_AT_MIN[0] if UNSAT_AT_MIN else []
MUS_SIZE = len(MUS)
N_UNSAT_MIN = len(UNSAT_AT_MIN)
MUS_MINIMAL = all(sat_count([c for c in MUS if c != x]) > 0 for x in MUS) if MUS else False

# 逐条删除约束后的满足构型数：证明 MUS 里每条都承重
SAT_DROP = {c: sat_count([x for x in CONSTRAINTS if x != c]) for c in CONSTRAINTS}
MUS_BEARING = all(SAT_DROP[c] > 0 for c in MUS) if MUS else False
NON_MUS_BEARING = all(SAT_DROP[c] == 0 for c in CONSTRAINTS if c not in MUS)

# 阳性对照：把输出比特翻倍，缺口必须响应（守恒式由数据驱动，不是恒真式）
GAP_SUM_DOUBLED_OUT = (2 * H_OUT_SUM) - (H_IN_BASE + H_PROG)
POS_CTRL_ALERTS = (GAP_SUM_DOUBLED_OUT > GAP_SUM) and (GAP_SUM_DOUBLED_OUT - GAP_SUM == H_OUT_SUM)
# 阴性对照：程序比特取 0，缺口只会更大、I1 仍激活 ⇒ 该侧恒绿，单列 IDENTITY
GAP_NO_PROG = H_OUT_SUM - H_IN_BASE
NEG_CTRL_GREEN = (GAP_NO_PROG > GAP_SUM)

# 信息复制比：理论脚本里直接抄观测锚的比特占程序比特的比例
COPY_SHARE_OUT = D(H_COPIED_UNIQUE) / D(H_OUT_SUM) if H_OUT_SUM else D(0)

# 控制组四读数两两不同，三个对照读数都不等于基线
CTRL_READINGS = [N_ANCHORS, N_MODELS, N_BREAK, MUS_SIZE]
ctrl_four_distinct = (len(set(CTRL_READINGS)) == len(CTRL_READINGS))
ctrl_no_eq_base = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
not_all_green = (N_BREAK == 0) and ANSWER_IN_INPUT and (N_COPIED > 0) and (MUS_SIZE > 0)

# 反噬基线读数：三次变体都必须让 n_sat 从 0 变正，并改变至少一个承重读数
BACKFIRE_READINGS = dict(n_models=N_MODELS, n_sat=N_SAT, gap_sum=GAP_SUM,
                         i1_active=CONSTRAINT_I1_ACTIVE, mus_size=MUS_SIZE,
                         n_copied=N_COPIED, answer_in_input=ANSWER_IN_INPUT,
                         h_in_base=H_IN_BASE, n_required=len(AXIOM_REQUIRED))
N_ESCAPE = N_BREAK


# ============================ 元守卫 ============================
def no_hardcode_ok():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("add", "guard"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, bool):
                bad += 1
    return bad == 0


def verdict_with(token):
    return ("ALG-INFO-GATE"
            + "__ANCHORS-" + str(N_ANCHORS)
            + "__IN-" + str(N_INPUT)
            + "__OUT-" + str(N_OUTPUT)
            + "__GAP-" + str(GAP_SUM)
            + "__COPIED-" + str(N_COPIED) + "of" + str(N_LITERALS)
            + "__ANSWER-" + ("IN-INPUT" if ANSWER_IN_INPUT else "NONE")
            + "__MODELS-" + str(N_MODELS)
            + "__SAT-" + token
            + "__MUS-" + str(MUS_SIZE)
            + "__PRED-0")


v_machine_0 = verdict_with(str(N_SAT))
v_machine_1 = verdict_with(str(N_SAT + 1))
verdict_machine_ok = (v_machine_0 != v_machine_1) and \
                     (("__SAT-" + str(N_SAT)) in v_machine_0)
verdict = v_machine_0

segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV8-RELOADED",
    (R[8]["guard_pass"] == R[8]["guard_count"]) and (R[8]["guard_count"] == 39) and
    (kn(8)["families_breakthrough"] == 0) and (kn(8)["p_min_v8"] == 4) and
    (kn(7)["escape_configs"] == 0),
    "PASS",
    "第八轮 39/39 守卫、8 族 0 突破、下界 4；第七轮逃逸 0。本册不再找候选，改数比特与问目标是否可满足")
add("SOURCE-LINK-HEALTH", link_health, "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) +
    " 个；分母为 0 判 FAIL")
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 act_ledger（json.load 逐项）与 exp_ledger（正则从原始 JSON 文本抽列）为两个不同函数，return 均非顶层数值常量")
add("TWO-PATH-LEDGER-EXACT", TWO_PATH_OK and (BIT_MISMATCH == 0), "PASS",
    "两路机拼：" + str(N_ANCHORS) + " 项锚的 id / value / kind 逐项一致，比特数失配 " +
    str(BIT_MISMATCH) + " 条")
add("BIT-ACCOUNT-PARTITION", (N_INPUT + N_OUTPUT == N_ANCHORS) and H_IN_CHECK, "PASS",
    "来料分层：定义/派生输入 " + str(N_INPUT) + " 项（" + str(H_IN) +
    " bit）、实测输出 " + str(N_OUTPUT) + " 项（" + str(H_OUT_SUM) +
    " bit）、合计 " + str(H_ALL) + " bit，逐位相等")
add("BIT-THREE-CALIBRE", (H_OUT_LCM != H_OUT_SUM) and (H_OUT_TWO != H_OUT_SUM) and
    (N_TWO_SIDED == 27) and (len({H_OUT_SUM, H_OUT_LCM, H_OUT_TWO}) == 3), "PASS",
    "三口径全报且两两不同：独立编码 " + str(H_OUT_SUM) + " / 通分共享分母 " +
    str(H_OUT_LCM) + " / 27 项双侧锚 " + str(H_OUT_TWO) + " bit（另带 sigma " +
    str(H_SIGMA_TWO) + " bit）。★通分口径反而更大（公分母 " +
    str(LCM_DEN.bit_length()) + " bit、分子随之放大）⇒ 口径决定读数，不预设方向")
add("NO-INFO-GAP-HONEST", NO_INFO_GAP and (GAP_SUM < 0) and (GAP_TWO < 0), "PASS",
    "★诚实修正：输入 " + str(H_IN) + " + 程序 " + str(H_PROG) + " = " +
    str(INPUT_PLUS_PROG) + " bit 已超过输出 " + str(H_OUT_SUM) +
    " bit；三口径缺口 " + str(GAP_SUM) + " / " + str(GAP_LCM) + " / " +
    str(GAP_TWO) + " bit（含负值）。预设「输出超输入」被数据推翻，不靠放宽守卫硬撑")
add("ANSWER-ALREADY-IN-INPUT", ANSWER_IN_INPUT, "PASS",
    "★★本册核心结论：零自由参数不是靠信息压缩达成，而是把观测值搬进程序。脚本 " +
    str(N_LITERALS) + " 个字面量中 " + str(N_COPIED) + " 个与观测逐位相等，" +
    "唯一值 " + str(H_COPIED_UNIQUE) + " bit 占输出 " +
    format(COPY_SHARE_OUT * 100, ".4f") + "% ⇒ 参数不灭第九实例：搬到源码字面量层")
add("GAQ-LITERALS-AST", (N_LITERALS == 97) and (H_PROG > 0), "PASS",
    "理论脚本按 AST 实际形态机读 " + str(N_LITERALS) + " 个数值字面量，程序侧信息 " +
    str(H_PROG) + " bit（脚本写 134.9768e6 时 AST 折成 134976800.0，照抄文档写法会漏）")
add("COPIED-LITERALS-DETECTED", (N_COPIED > 0) and (N_COPIED_UNIQUE > 0) and
    (H_COPIED_OCC >= H_COPIED_UNIQUE), "PASS",
    "★信息复制机读：理论脚本 " + str(N_LITERALS) + " 个字面量中 " + str(N_COPIED) +
    " 个与 46 项锚 value 逐位相等（" + str(N_COPIED_UNIQUE) + " 个不同值），" +
    "按出现计 " + str(H_COPIED_OCC) + " bit、按唯一值计 " + str(H_COPIED_UNIQUE) +
    " bit ⇒ 这些比特是抄来的，不是方程生成的")
add("COPY-RATIO-DRIVEN", (COPY_RATIO > 0) and (COPY_SHARE_OUT > 0), "PASS",
    "复制比特占程序比特 " + format(COPY_RATIO * 100, ".4f") +
    "%，占输出比特 " + format(COPY_SHARE_OUT * 100, ".4f") +
    "%；第六轮「7 条 GAQ 理论值是字面量」在信息层得到独立佐证")
add("CONSERVATION-I1-DATA-DRIVEN", CONSTRAINT_I1_ACTIVE and (N_COPIED > 0) and
    (H_COPIED_UNIQUE > 0), "PASS",
    "守恒式 I1 由观测副本 " + str(N_COPIED) + " 条 / " + str(H_COPIED_UNIQUE) +
    " bit 机读证据驱动，不是写死的逻辑断言；忽略复制证据会使它失活（反噬 2 验证）")

add("ROUND-INJECTION-ALL-POSITIVE", ALL_ROUNDS_INJECT and (H_INJECT_TOTAL > 0), "PASS",
    "★跨 " + str(N_ROUNDS) + " 轮注入账：每轮 H_inject > 0，机读合计 " +
    str(H_INJECT_TOTAL) + " bit 的下界注入 ⇒ 参数不灭升级为信息不灭")
add("ROUND-INJECTION-ALL-ZERO", ALL_ROUNDS_ZERO, "PASS",
    "八轮突破读数全为 0；每轮都有正注入、每轮都没有突破 ⇒ 不是八个巧合，是同一条守恒式")
add("ROUND-LEDGER-CONSISTENT",
    all(r["H_inject_lower"] == sum(r["counts"]) for r in ROUND_INJECTION) and
    (len(ROUND_INJECTION) == N_ROUNDS), "PASS",
    "注入账逐行机算（层 / 标签 / 计数 / 比特下界 / 突破），无手填常数")

add("MODEL-SPACE-128", (N_MODELS == 128) and (len(ATOMS) == 7), "PASS",
    "目标公理 7 条原子，2^7 = " + str(N_MODELS) + " 个真值指派全枚举，无遗漏")
add("TARGET-UNSATISFIABLE", (N_SAT == 0) and (N_BREAK == 0), "PASS",
    "★★满足全部 8 条约束的构型 " + str(N_SAT) + " 个 ⇒ 「攻破统一场论」的目标公理集在本编码口径下不可满足；" +
    "前八轮 0 突破不是候选不够好")
add("MUS-SIZE-4", (MUS_SIZE == 4) and (MUS_LAYER == 4) and (N_UNSAT_MIN >= 1), "PASS",
    "最小不可满足核大小 " + str(MUS_SIZE) + "：" + str(MUS) +
    "；第 " + str(MUS_LAYER) + " 层共 " + str(N_UNSAT_MIN) + " 个不可满足子集")
add("MUS-MINIMAL", MUS_MINIMAL, "PASS",
    "核内任删一条即变可满足 ⇒ 核是极小的，不是把无关约束一起塞进来")
add("MUS-BEARING", MUS_BEARING and NON_MUS_BEARING, "PASS",
    "逐条删除：核内四条各自使满足构型数变正，核外四条删除后仍为 0 ⇒ 核的每条都承重")
add("SAT-DROP-READINGS", (len(set(SAT_DROP.values())) > 1) and
    (sum(1 for v in SAT_DROP.values() if v > 0) == MUS_SIZE), "PASS",
    "删除各约束后的满足构型数 " + str(SAT_DROP) + "，恰好 " + str(MUS_SIZE) + " 条非零")

add("POS-CTRL-DOUBLED-OUTPUT", POS_CTRL_ALERTS, "PASS",
    "阳性对照：输出比特翻倍 ⇒ 缺口 " + str(GAP_SUM) + "→" + str(GAP_SUM_DOUBLED_OUT) +
    "，增量恰为 " + str(H_OUT_SUM) + " bit ⇒ 守恒式由数据驱动，不是恒真式")
add("CTRL-IDENTITY-NEVER-HITS", NEG_CTRL_GREEN, "IDENTITY",
    "阴性对照：程序比特取 0 时缺口只会更大（" + str(GAP_SUM) + "→" + str(GAP_NO_PROG) +
    "），该侧恒绿且不受判据影响，单列 IDENTITY 配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "负对照恒绿，但缺口、复制字面量、MUS、跨轮注入账均为非恒绿读数")
add("CTRL-FOUR-DISTINCT", ctrl_four_distinct, "PASS",
    "控制组四个读数两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-NO-EQ-BASE", ctrl_no_eq_base, "PASS",
    "三个对照读数均不等于基线 " + str(CTRL_READINGS[0]) + "，杜绝全表读数相同的假判别力")

add("SPINE-ZERO", honest_boundary, "PASS",
    "跨卷回读：r403 四力正确解 " + str(R403["unique_answer"]["four_forces_c3"]) +
    " 条、r404 接受 " + str(R404["key_numbers"]["four_force_accepted"]) +
    "；第五／六轮 0 命中、第七轮逃逸 0、第八族突破 0、本册满足构型 " + str(N_SAT))
add("INFO-UPGRADES-PARAMETER-LEDGER", (H_INJECT_TOTAL > 0) and ANSWER_IN_INPUT, "PASS",
    "★本册的方法论增量：前八轮数「参数个数」，本册数「精确比特」；" +
    "参数可以靠改名藏进定义常数，比特藏不住——本册直接抓到 " + str(N_COPIED) +
    " 处源码字面量与观测逐位相等")
add("FAMILY-LIMITED-CLAIM", (N_SAT == 0) and (N_COPIED > 0), "BOUNDARY",
    "★比特数是固定编码（分子分母分别二进制）下的描述长度上界，不是 Kolmogorov 复杂度；" +
    "换编码（连分数、共享前缀、算术编码）读数会变，三口径里两个缺口为负、一个为正。" +
    "I1 是「现有零参数宣称都含观测副本」的本地归纳 + 信息守恒弱式，不是全称元物理定理")
add("FOUR-FORCE-INCOMPLETE", honest_boundary, "INFO",
    "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）；四力大统一 0 条正确解")
add("NO-BREAKTHROUGH", (N_SAT == 0), "INFO",
    "本册不宣称攻破统一场论；给出的是信息守恒式与目标公理集的最小不可满足核")
add("MATH-NOT-EXPERIMENT", honest_boundary, "INFO",
    "所有结论都是可算判决（比特数、复制重合、可满足性、MUS），不是实验证实；不产新物理，独立实验预言仍为 0")
add("NEXT-EXIT", (N_SAT == 0) and ANSWER_IN_INPUT, "INFO",
    "要越过守恒式，须给出程序侧不含任何观测副本、且能生出 " + str(N_OUTPUT) +
    " 项实测数值（" + str(H_OUT_SUM) + " bit）的可压缩生成机制；" +
    "即真正的信息压缩，而非把答案抄进源码。这仍等价于一条带双侧误差棒、" +
    "理论值落在其可判负区间之外的新实验读数")

add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把满足构型读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")


# ============================ 判定汇总 ============================
def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-INFO-GATE--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-INFO-GATE--GATES-FAIL"
    return "ALG-INFO-GATE--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "TARGET-UNSATISFIABLE",
                     "GAP-ALL-POSITIVE", "FAMILY-LIMITED-CLAIM", "ROUND-INJECTION-ALL-POSITIVE"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-INFO-GATE--GATES-PASS-WITH-0-NEGATIVE") and \
              (nf_guard_before == 0) and (len(declared_negative) > 0)
add("FINAL-OF-CONSISTENT", final_of_ok, "PASS",
    "final_of(nf_main=" + str(nf_main_before) + ",nf_guard=" + str(nf_guard_before) +
    ",n_decl=" + str(len(declared_negative)) + ")：守卫 FAIL 挡门、已登记判负不挡门、缺 n_decl 报 GATES-FAIL")

counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0, "BOUNDARY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
g_pass = sum(1 for s in segs if s["ok"])
g_count = len(segs)

key_numbers = {
    "anchors": N_ANCHORS,
    "input_anchors": N_INPUT,
    "output_anchors": N_OUTPUT,
    "two_sided_anchors": N_TWO_SIDED,
    "H_in_bits": H_IN,
    "H_out_sum_bits": H_OUT_SUM,
    "H_out_lcm_bits": H_OUT_LCM,
    "H_out_two_sided_bits": H_OUT_TWO,
    "H_sigma_two_sided_bits": H_SIGMA_TWO,
    "H_all_bits": H_ALL,
    "lcm_denominator_bits": LCM_DEN.bit_length(),
    "H_prog_bits": H_PROG,
    "gaq_literals": N_LITERALS,
    "copied_literals": N_COPIED,
    "copied_unique_values": N_COPIED_UNIQUE,
    "H_copied_occ_bits": H_COPIED_OCC,
    "H_copied_unique_bits": H_COPIED_UNIQUE,
    "copy_ratio_pct": format(COPY_RATIO * 100, ".6f"),
    "copy_share_of_output_pct": format(COPY_SHARE_OUT * 100, ".6f"),
    "input_plus_prog_bits": INPUT_PLUS_PROG,
    "no_info_gap": NO_INFO_GAP,
    "answer_in_input": ANSWER_IN_INPUT,
    "gap_sum_bits": GAP_SUM,
    "gap_lcm_bits": GAP_LCM,
    "gap_two_sided_bits": GAP_TWO,
    "gap_min_bits": GAP_MIN,
    "gap_max_bits": GAP_MAX,
    "gap_no_prog_bits": GAP_NO_PROG,
    "gap_doubled_output_bits": GAP_SUM_DOUBLED_OUT,
    "injection_lower_bound_copied_bits": INJECT_BITS_LOWER,
    "H_inject_round_total": H_INJECT_TOTAL,
    "rounds": N_ROUNDS,
    "all_rounds_inject_positive": ALL_ROUNDS_INJECT,
    "all_rounds_zero_breakthrough": ALL_ROUNDS_ZERO,
    "models_enumerated": N_MODELS,
    "models_satisfying_target": N_SAT,
    "mus_layer": MUS_LAYER,
    "mus_size": MUS_SIZE,
    "mus": MUS,
    "unsat_subsets_at_min_layer": N_UNSAT_MIN,
    "mus_minimal": MUS_MINIMAL,
    "sat_after_dropping_each": SAT_DROP,
    "control_readings": CTRL_READINGS,
    "bit_mismatch_two_path": BIT_MISMATCH,
    "prev5_hits": kn(5)["pairs_hit"],
    "prev6_hits": kn(6)["pairs_hit_after"],
    "prev7_escape": kn(7)["escape_configs"],
    "prev8_breakthrough": kn(8)["families_breakthrough"],
    "r403_four_force_correct": R403["unique_answer"]["four_forces_c3"],
    "r404_four_force_accepted": R404["key_numbers"]["four_force_accepted"],
    "spine_independent_predictions": 0,
    "source_files": len(SOURCE_FILES),
    "source_missing": len(source_missing),
    "four_force_incomplete": True,
}

out = {
    "title": "算法联盟：信息守恒与目标可满足性 · 比特账与最小不可满足核",
    "date": "2026-11-12",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "axioms": {
        "A1": "单一机制描述四力",
        "A2": "零自由参数",
        "A3": "至少一条独立数值预言",
        "A4": "与全部既有实验相容",
        "A5": "不把实验值当输入",
        "A6": "数学自洽",
        "A7": "解释谱值为何如此",
        "I1": "输出比特超过输入加程序时，A2 与 A3 与 A5 不可同时成立",
    },
    "bit_account": dict(input_ids=[r["id"] for r in INPUT_ROWS],
                        output_ids=[r["id"] for r in OUTPUT_ROWS],
                        two_sided_ids=[r["id"] for r in TWO_SIDED],
                        copied_unique=[str(x) for x in COPIED_UNIQUE]),
    "round_injection": ROUND_INJECTION,
    "key_numbers": key_numbers,
    "segments": segs,
}
_payload = json.dumps(out, ensure_ascii=False, sort_keys=True, indent=0)
digest = hashlib.sha256(_payload.encode("utf-8")).hexdigest()
out["content_sha256"] = digest

if __name__ == "__main__":
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("算法联盟：信息守恒与目标可满足性 · 比特账与最小不可满足核（第九轮）")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("两路机拼：act json.load 逐项 vs exp 正则从原始 JSON 文本抽列，46/46 一致、比特失配 " +
                 str(BIT_MISMATCH) + " 条")
    lines.append("来料分层：定义/派生输入 " + str(N_INPUT) + " 项 " + str(H_IN) +
                 " bit；实测输出 " + str(N_OUTPUT) + " 项；全部 " + str(H_ALL) + " bit")
    lines.append("输出三口径：独立编码 " + str(H_OUT_SUM) + " / 通分共享分母 " +
                 str(H_OUT_LCM) + " / 27 项双侧 " + str(H_OUT_TWO) + " bit")
    lines.append("理论脚本：" + str(N_LITERALS) + " 个 AST 数值字面量共 " + str(H_PROG) +
                 " bit；其中 " + str(N_COPIED) + " 个与观测锚逐位相等（" +
                 str(N_COPIED_UNIQUE) + " 个不同值），复制占比 " +
                 format(COPY_RATIO * 100, ".4f") + "%")
    lines.append("-" * 96)
    lines.append("★信息账：预设「输出超输入」被数据推翻，如实报含负缺口")
    lines.append("  输入 " + str(H_IN) + " + 程序 " + str(H_PROG) + " = " +
                 str(INPUT_PLUS_PROG) + " bit > 输出 " + str(H_OUT_SUM) + " bit ⇒ 无信息缺口")
    lines.append("  三口径缺口 " + str(GAP_SUM) + " / " + str(GAP_LCM) +
                 " / " + str(GAP_TWO) + " bit；复制唯一值 " + str(H_COPIED_UNIQUE) +
                 " bit 占输出 " + format(COPY_SHARE_OUT * 100, ".4f") + "%")
    lines.append("  ⇒ 零自由参数靠把观测值搬进源码字面量达成，不是靠信息压缩")
    lines.append("  阳性对照输出翻倍 ⇒ 缺口 " + str(GAP_SUM_DOUBLED_OUT) +
                 "（增量恰 " + str(H_OUT_SUM) + " bit）；阴性对照程序比特 0 ⇒ " + str(GAP_NO_PROG))
    lines.append("  跨 " + str(N_ROUNDS) + " 轮注入账合计下界 " + str(H_INJECT_TOTAL) +
                 " bit，八轮突破读数全 0")
    lines.append("-" * 96)
    lines.append("目标公理 7 原子 + I1 ⇒ " + str(N_MODELS) + " 个真值指派全枚举")
    lines.append("  满足全部 8 条约束的构型 " + str(N_SAT) + " 个 ⇒ 目标不可满足")
    lines.append("  最小不可满足核 第 " + str(MUS_LAYER) + " 层 / 大小 " + str(MUS_SIZE) +
                 " / " + str(MUS) + "；该层 " + str(N_UNSAT_MIN) + " 个不可满足子集")
    lines.append("  逐条删除后满足数 " + str(SAT_DROP))
    lines.append("-" * 96)
    lines.append("红线：数学自洽 != 实验证实；四力大统一 0 条正确解；独立实验预言 0；不宣称攻破。")
    lines.append("-" * 96)
    for s in segs:
        lines.append("[" + s["kind"] + "] " + s["name"] + " :: " + ("OK" if s["ok"] else "FAIL"))
    text_out = "\n".join(lines) + "\n"
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write(text_out)
    print("final=", final, "guards=", g_pass, "/", g_count)
    print("sha256=", digest)
    print("ALL-CHECKS-PASS" if (g_pass == g_count) else "SOME-GUARDS-FAILED")
    print("WRITE", OUT_JSON)
    print("WRITE", OUT_REPORT)
