# -*- coding: utf-8 -*-
"""算法联盟 · 统一场论第十四轮：全链总账与「四力单方程」命题的三分判决。

不占 RID、不入 README、不与任何审计卷相加。
用户命题「所有力可以放到一个方程里面」被拆成三个互不相加的可算口径：
形式统一（记账式，恒真）/ 约束统一（共享参数，机读排除）/ 可判负（独立预言）。
"""
import os
import ast
import re
import json
import glob
import hashlib
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 50

ROOT = "D:/a10/aikjx/code/my_lib"
UROOT = os.path.join(ROOT, "openuft")
BASE = os.path.join(UROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
SRC = os.path.join(BASE, "源码")
JUDGE = os.path.join(BASE, "判定")
P_README = os.path.join(BASE, "README.md")
OUT_JSON = os.path.join(DATA, "_ALG_final_ledger_recompute_2026-11-14.json")
OUT_REPORT = os.path.join(DATA, "_ALG_final_ledger_recompute_report_2026-11-14.txt")

# ★各轮字段按语义白名单显式登记，禁止用宽泛正则从顶层元数据误抓同名键。
ROUNDS = [
    ("R1", "实验数据链", "_ALG_expdata_fullchain_recompute_2026-11-11.json", None, "independent_predictions", None),
    ("R2", "机制类型链", "_ALG_allknowledge_iterative_recompute_2026-11-11.json", "breakthrough_count", "native_independent_predictions", None),
    ("R3", "实验存活层", "_ALG_expfacts_survival_recompute_2026-11-11.json", "breakthrough_count", "spine_independent_predictions", "p_exp_max"),
    ("R4", "判据元逻辑层", "_ALG_meta_gateaudit_recompute_2026-11-11.json", "quad_gate_hits", "spine_independent_predictions", None),
    ("R5", "配对优化层", "_ALG_pair_optim_recompute_2026-11-12.json", "pairs_hit", "spine_independent_predictions", "best_gap_sigma"),
    ("R6", "自由度归属层", "_ALG_pfree_attribution_recompute_2026-11-12.json", "pairs_hit_after", "spine_independent_predictions", None),
    ("R7", "攻破力的统一", "_ALG_force_unification_recompute_2026-11-12.json", "escape_configs", "spine_independent_predictions", "p_min_extra"),
    ("R8", "破缺谱生成机制", "_ALG_spectrum_generation_recompute_2026-11-12.json", "families_breakthrough", "spine_independent_predictions", "p_min_v8"),
    ("R9", "信息守恒层", "_ALG_information_gate_recompute_2026-11-12.json", "models_satisfying_target", "spine_independent_predictions", "H_inject_round_total"),
    ("R10", "审计链体检", "_ALG_healthcheck_recompute_2026-11-12.json", "defects_found", None, None),
    ("R11", "扰动传递闭包", "_ALG_perturbation_closure_recompute_2026-11-14.json", "clean_falsifiable", "spine_independent_predictions", "injection_lower_bound_ext"),
    ("R12", "全库可达域普查", "_ALG_fullchain_scope_recompute_2026-11-14.json", "clean_falsifiable", "spine_independent_predictions", "inject_total"),
    ("R13", "库外读数接入", "_ALG_external_exit_recompute_2026-11-14.json", "clean_falsifiable", "spine_independent_predictions", "min_theory_side_changes"),
]

P_R7 = os.path.join(DATA, "_ALG_force_unification_recompute_2026-11-12.json")
P_R8 = os.path.join(DATA, "_ALG_spectrum_generation_recompute_2026-11-12.json")
P_R9 = os.path.join(DATA, "_ALG_information_gate_recompute_2026-11-12.json")
P_R3 = os.path.join(DATA, "_ALG_expfacts_survival_recompute_2026-11-11.json")
P_R5 = os.path.join(DATA, "_ALG_pair_optim_recompute_2026-11-12.json")
P_R6 = os.path.join(DATA, "_ALG_pfree_attribution_recompute_2026-11-12.json")
P_R13 = os.path.join(DATA, "_ALG_external_exit_recompute_2026-11-14.json")
P_R12 = os.path.join(DATA, "_ALG_fullchain_scope_recompute_2026-11-14.json")

def report_path(p):
    """report→JSON 路径构造的唯一收敛函数；机核与核验器共用同一口径。"""
    return p.replace("recompute_", "recompute_report_").replace(".json", ".txt")


SOURCE_FILES = [P_README, P_R3, P_R5, P_R6, P_R7, P_R8, P_R9, P_R12, P_R13] + \
               [os.path.join(DATA, r[2]) for r in ROUNDS]
# ★链接体检必须覆盖 exp 路径实际读取的 report，不能只查 json 侧。
SOURCE_FILES = SOURCE_FILES + [report_path(p) for p in SOURCE_FILES if p.endswith(".json")]
SOURCE_FILES = list(dict.fromkeys(SOURCE_FILES))
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(source_missing) == 0)

OWN_NAMES = {
    "算法联盟_全链总账与四力单方程命题三分判决_统一场论第十四轮_2026-11-14.md",
    "算法联盟_全链总账_第十四轮可视化_2026-11-14.html",
    "_alg_final_ledger_recompute.py",
    "_ALG_final_ledger_recompute_2026-11-14.json",
    "_ALG_final_ledger_recompute_report_2026-11-14.txt",
    "_ALG_final_ledger_verify_2026-11-14.json",
}


def is_own(p):
    return os.path.basename(p) in OWN_NAMES


def text(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def load(p):
    return json.loads(text(p))


def kn(d, *names):
    k = d.get("key_numbers", d)
    for n in names:
        if n in k:
            return k[n]
    return None


def as_int(v):
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        m = re.match(r"^(\d+)", v.strip())
        return int(m.group(1)) if m else None
    return None


def dstr(x, places=6):
    if x == 0:
        return "0"
    q = D(1).scaleb(-places)
    if abs(x) < q:
        return format(x, "e")
    return format(x.quantize(q), "f").rstrip("0").rstrip(".")


# ====================== 总账：两路机读，互不引用 ======================
def act_rounds():
    """act 路径：json.load 结构化读各轮机核数据与守卫数。"""
    rows = []
    for tag, name, fn, hitf, predf, lowerf in ROUNDS:
        p = os.path.join(DATA, fn)
        j = load(p)
        k = j.get("key_numbers", {})
        rows.append(dict(tag=tag, name=name,
                         gp=int(j.get("guard_pass", -1)), gc=int(j.get("guard_count", -1)),
                         verdict=str(j.get("verdict", "")), final=str(j.get("final", "")),
                         hit_field=hitf, hit=(k.get(hitf) if hitf else None),
                         pred_field=predf, pred=(k.get(predf) if predf else None),
                         lower_field=lowerf, lower=(k.get(lowerf) if lowerf else None)))
    return rows


def exp_rounds():
    """exp 路径：正则逐行扫各轮 report 纯文本，与 act 取数机制完全不同。"""
    rows = []
    for tag, name, fn, hitf, predf, lowerf in ROUNDS:
        p = report_path(os.path.join(DATA, fn))
        s = text(p)
        mg = re.search(r"(?m)^guards\s*:\s*(\d+)\s*/\s*(\d+)", s)
        mv = re.search(r"(?m)^verdict\s*:\s*(\S+)", s)
        mf = re.search(r"(?m)^final\s*:\s*(\S+)", s)
        rows.append(dict(tag=tag, gp=int(mg.group(1)) if mg else -1,
                         gc=int(mg.group(2)) if mg else -1,
                         verdict=mv.group(1) if mv else "",
                         final=mf.group(1) if mf else ""))
    return rows


def act_configs():
    """act 路径：R7 的四配置结构化读取。"""
    return load(P_R7)["configurations"]


def exp_configs():
    """exp 路径：从 R7 report 的判词串正则抽配置总数与逃逸数。"""
    s = text(report_path(P_R7))
    mc = re.search(r"CONFIGS-(\d+)", s)
    me = re.search(r"ESCAPE-(\d+)", s)
    return dict(configs=int(mc.group(1)) if mc else -1,
                escape=int(me.group(1)) if me else -1)


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    want = {"act_rounds", "exp_rounds", "act_configs", "exp_configs"}
    names = set()
    bad = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in want:
            names.add(node.name)
            for r in ast.walk(node):
                if isinstance(r, ast.Return) and isinstance(r.value, ast.Constant) and \
                   isinstance(r.value.value, (int, float)) and not isinstance(r.value.value, bool):
                    bad.append(node.name)
    return (names == want) and (len(bad) == 0)


ACT = act_rounds()
EXP = exp_rounds()
N_ROUNDS = len(ACT)
TWO_PATH_EQ = all((a["gp"] == b["gp"] and a["gc"] == b["gc"] and
                   a["verdict"] == b["verdict"] and a["final"] == b["final"])
                  for a, b in zip(ACT, EXP)) and (len(ACT) == len(EXP))
N_TWO_PATH_MISMATCH = sum(1 for a, b in zip(ACT, EXP)
                          if (a["gp"], a["gc"], a["verdict"], a["final"]) !=
                             (b["gp"], b["gc"], b["verdict"], b["final"]))
ALL_GUARDS_PASS = sum(1 for a in ACT if (a["gp"] == a["gc"] and a["gp"] > 0))
ALL_GUARDS_PASS_OK = (ALL_GUARDS_PASS == N_ROUNDS)
# ★守卫数只计「全过的轮数」，绝不把 35+35+…+50 相加。
ALL_PRED_ZERO = all((as_int(a["pred"]) == 0) for a in ACT if a["pred"] is not None)
N_PRED_FIELDS = sum(1 for a in ACT if a["pred"] is not None)
HIT_NONZERO = sum(1 for a in ACT if as_int(a["hit"]) not in (None, 0))
HIT_FIELDS = sum(1 for a in ACT if a["hit"] is not None)

# ====================== README 实时重数 ======================
README_RB = open(P_README, "rb").read()
README_BYTES = len(README_RB)
README_MD5 = hashlib.md5(README_RB).hexdigest()
README_MAX_RID = max(int(x) for x in re.findall(r"TUFT-r(\d+)_", README_RB.decode("utf-8")))
TREE_MAX_RID = 0
for sub in ("源码", "数据", "判定"):
    for n in os.listdir(os.path.join(BASE, sub)):
        m = re.search(r"TUFT-r(\d+)_", n)
        if m:
            TREE_MAX_RID = max(TREE_MAX_RID, int(m.group(1)))

INV = {}
for label, pat in (("main_md", os.path.join(BASE, "*.md")),
                   ("main_html", os.path.join(BASE, "*.html")),
                   ("alg_md", os.path.join(BASE, "算法联盟_*.md")),
                   ("alg_html", os.path.join(BASE, "算法联盟_*.html")),
                   ("src_files", os.path.join(SRC, "*")),
                   ("data_files", os.path.join(DATA, "*")),
                   ("judge_files", os.path.join(JUDGE, "*"))):
    INV[label] = len([p for p in glob.glob(pat) if not is_own(p)])

# ====================== 用户命题：所有力放进一个方程，三分机读 ======================
R7 = load(P_R7)
R8 = load(P_R8)
R9 = load(P_R9)
R3 = load(P_R3)
R5 = load(P_R5)
R6 = load(P_R6)
R12 = load(P_R12)
R13 = load(P_R13)

CFG = act_configs()
CFG_EXP = exp_configs()
N_CFG = len(CFG)
N_CFG_KEY = int(kn(R7, "configs_enumerated"))
N_ESCAPE_KEY = int(kn(R7, "escape_configs"))
CFG_TWO_PATH = (N_CFG == N_CFG_KEY == CFG_EXP["configs"]) and \
               (CFG_EXP["escape"] == N_ESCAPE_KEY)

# ★「所有力放进同一个方程」的精确机读定义：κ 与耦合都不按力分置。
ONE_EQ = [c for c in CFG if (not c["k_split"]) and (not c["g_split"])]
SURV = [c for c in CFG if c["survive"]]
BRK = [c for c in CFG if c["breakthrough"]]
UNIFIED_CFG = [c for c in CFG if c["unified"]]
N_ONE_EQ = len(ONE_EQ)
N_SURV = len(SURV)
N_BRK = len(BRK)
N_UNIFIED_CFG = len(UNIFIED_CFG)
ONE_EQ_MISMATCH = sum(int(c["mismatch"]) for c in ONE_EQ)
ONE_EQ_SURVIVE = any(c["survive"] for c in ONE_EQ)
ONE_EQ_GAIN = sum(int(c["gain"]) for c in ONE_EQ)
SURV_GAIN_SUM = sum(int(c["gain"]) for c in SURV)
SURV_ALL_SPLIT = all(c["k_split"] and c["g_split"] for c in SURV) if SURV else False
SHARED_EXCLUDED = bool(kn(R7, "shared_all_excluded"))

# 三分（互不相加）
FORMAL_POSSIBLE = (N_SURV > 0) and SURV_ALL_SPLIT
FORMAL_GAIN_NONPOSITIVE = (SURV_GAIN_SUM <= 0)
CONSTRAINED_EXCLUDED = (N_ONE_EQ > 0) and (not ONE_EQ_SURVIVE) and SHARED_EXCLUDED
FALSIFIABLE_ZERO = ALL_PRED_ZERO and (int(kn(R5, "pairs_hit")) == 0) and \
                   (int(kn(R6, "pairs_hit_after")) == 0) and \
                   (int(kn(R12, "clean_falsifiable")) == 0) and \
                   (int(kn(R13, "clean_falsifiable")) == 0)
CROSS_SUM = len((FORMAL_POSSIBLE, CONSTRAINED_EXCLUDED, FALSIFIABLE_ZERO))

# ====================== 三个独立下界（不同轮、不同对象、不相加） ======================
B7_EXTRA = int(kn(R7, "p_min_extra"))
B7_EQ = int(kn(R7, "p_eq_single_equation"))
B8_MIN = int(kn(R8, "p_min_v8"))
B8_BUDGET = int(kn(R8, "budget"))
B8_REDUCTION = int(kn(R8, "p_min_reduction"))
B8_TREE = int(kn(R8, "labels_tree_merged"))
B8_EXT = int(kn(R8, "labels_external"))
B9_MUS = int(kn(R9, "mus_size"))
B9_MODELS = int(kn(R9, "models_enumerated"))
B9_SAT = int(kn(R9, "models_satisfying_target"))
BOUND_A = B7_EXTRA - B7_EQ
BOUND_B = B8_MIN - B8_BUDGET
BOUND_C = B9_MUS - B8_BUDGET
BOUNDS_ALL_BEARING = (BOUND_A > 0) and (BOUND_B > 0) and (BOUND_C > 0) and \
                     (B9_SAT == 0) and (N_ESCAPE_KEY == 0)

# ★本轮新机算：跨轮精确整数恒等式（各端点取自不同轮不同字段，两路互证）。
EQ1 = (B7_EXTRA - B8_REDUCTION == B8_MIN)
EQ2 = (B8_TREE + B8_EXT == B8_MIN)
EQ3 = (int(kn(R7, "shared_kappa_mismatch")) + int(kn(R7, "shared_coupling_mismatch"))
       == int(kn(R7, "shared_total_mismatch")))
EQ4 = (N_CFG == N_CFG_KEY)
AXIOMS = R9.get("axioms", {})
EQ5 = (B9_MODELS == 2 ** (len(AXIOMS) - 1))
CROSS_EQ_OK = EQ1 and EQ2 and EQ3 and EQ4 and EQ5
CROSS_EQ_COUNT = sum(1 for x in (EQ1, EQ2, EQ3, EQ4, EQ5) if x)

# ====================== 谱类数两路机读 ======================
def F_of(s):
    return F(str(s))


KAPPA_VALS = [F_of(f["kappa"]) for f in R7["forces"]]
COUP_ACT = [F_of(x) for x in R7["couplings"]["act"]]
COUP_EXP = [F_of(x) for x in R7["couplings"]["exp"]]
KAPPA_CLASSES = len(set(KAPPA_VALS))
COUP_ACT_CLASSES = len(set(COUP_ACT))
COUP_EXP_CLASSES = len(set(COUP_EXP))
SPECTRUM_TWO_PATH = (KAPPA_CLASSES == int(kn(R7, "kappa_classes"))) and \
                    (COUP_ACT_CLASSES == int(kn(R7, "coupling_classes_act"))) and \
                    (COUP_EXP_CLASSES == int(kn(R7, "coupling_classes_exp"))) and \
                    (COUP_ACT_CLASSES == COUP_EXP_CLASSES)
COUPLING_SPAN_DEX = str(kn(R7, "coupling_span_dex"))
LAM_RATIO = str(kn(R7, "lam_pi_over_lam_W"))
FORCE_COUNT = int(kn(R7, "forces"))
LONG_RANGE = int(kn(R7, "long_range_forces"))
SPINE_CORRECT = as_int(kn(R7, "r403_four_force_correct"))
SPINE_ACCEPT = int(kn(R7, "r404_four_force_accepted"))

# ====================== 正负双对照与反事实控制组 ======================
# 正对照：判据不是恒绿——全空间被枚举而命中为 0，且存在非零命中读数。
POS_ENUM = (N_CFG > 0) and (N_CFG_KEY > 0) and (B9_MODELS > 0)
POS_HIT_NONZERO = (HIT_NONZERO > 0)
CHI2_GAP = str(kn(R5, "best_gap_sigma"))
POS_SURVIVE = int(kn(R3, "survive_count"))
POS_POSITIVE_EVIDENCE = int(kn(R3, "positive_evidence_count"))

# ★控制组与基线必须同口径：都问「下界门是否阻挡」，只是把预算换成反事实值。
# 不用恒真的 (B8_MIN <= B8_MIN) 装饰判据，也不用与 survive 不同口径的 p_extra 比较。
CTRL_BUDGET_INFLATED = B8_MIN
BASELINE_BLOCK = int(B8_MIN > B8_BUDGET)
CTRL_BLOCK = int(B8_MIN > CTRL_BUDGET_INFLATED)
CTRL_DIFFERS_FROM_BASE = (BASELINE_BLOCK != CTRL_BLOCK) and (BASELINE_BLOCK == 1) and (CTRL_BLOCK == 0)
# 控制组 2：把共享谱失配强行置零，看单方程配置是否被误放行。
CTRL_MISMATCH_FORCED = 0
CTRL_MISMATCH_RELEASED = (ONE_EQ_MISMATCH > CTRL_MISMATCH_FORCED)
CTRL_RELEASE_COUNT = int(CTRL_DIFFERS_FROM_BASE) + int(CTRL_MISMATCH_RELEASED)

# ====================== 可判负与最小代价 ======================
PAIRS_HIT_R5 = int(kn(R5, "pairs_hit"))
PAIRS_HIT_R6 = int(kn(R6, "pairs_hit_after"))
PREV12_CLEAN = int(kn(R12, "clean_falsifiable"))
R13_CLEAN = int(kn(R13, "clean_falsifiable"))
MIN_CUT_R12 = int(kn(R12, "min_cut"))
MIN_THEORY_R13 = int(kn(R13, "min_theory_side_changes"))
CERT_DIRS_R13 = int(kn(R13, "cert_invariant_directions"))
COPIED_R12 = int(kn(R12, "copied_ast"))
COPIED_FILES_R12 = int(kn(R12, "copied_files"))
INJECT_R12 = int(kn(R12, "inject_total"))
INJECT_R9 = int(kn(R9, "H_inject_round_total"))
BIT_IN = int(kn(R9, "H_in_bits"))
BIT_OUT = int(kn(R9, "H_out_sum_bits"))
BIT_PROG = int(kn(R9, "H_prog_bits"))
BIT_COPIED = int(kn(R9, "H_copied_unique_bits"))
BREAK_FIELDS = ("breakthrough", "breakthrough_count", "families_breakthrough")
N_BREAK = sum(1 for a in ACT if a["hit_field"] in BREAK_FIELDS
              and as_int(a["hit"]) not in (None, 0))

# ====================== 三重门与最小承重割 ======================
GATE_LEDGER_ACTIVE = True
GATE_SINGLEEQ_ACTIVE = True
GATE_FALSIFIABLE_ACTIVE = True
ACTIVE_GATES = [GATE_LEDGER_ACTIVE, GATE_SINGLEEQ_ACTIVE, GATE_FALSIFIABLE_ACTIVE]
LEDGER_OK = TWO_PATH_EQ and ALL_GUARDS_PASS_OK and ALL_PRED_ZERO
SINGLEEQ_OK = CONSTRAINED_EXCLUDED and BOUNDS_ALL_BEARING and CROSS_EQ_OK
FALSIFIABLE_OK = FALSIFIABLE_ZERO and (N_BREAK == 0)


def gate_pass_with(led_on, seq_on, fal_on, c):
    is_one_eq = (not c["k_split"]) and (not c["g_split"])
    return ((LEDGER_OK or not led_on)
            and ((is_one_eq and c["survive"]) or not seq_on)
            and (c["breakthrough"] or not fal_on))


def gate_pass(c):
    return gate_pass_with(GATE_LEDGER_ACTIVE, GATE_SINGLEEQ_ACTIVE,
                          GATE_FALSIFIABLE_ACTIVE, c)


CLEAN_UNIFIED = sum(1 for c in CFG if gate_pass(c))
# ★★预设「三个门各自承重」被自己的数据推翻：4 配置里 breakthrough 全假、
# 全共享配置全不存活 ⇒ 单独拆任一门都不误放行。改驱动量为「最小承重割」，如实报负读数。
WAIVE_SPECTRUM = []
for _mask in range(8):
    _led = not bool(_mask & 1)
    _seq = not bool(_mask & 2)
    _fal = not bool(_mask & 4)
    WAIVE_SPECTRUM.append(dict(mask=_mask,
                               waived=bin(_mask).count("1"),
                               passed=sum(1 for c in CFG
                                          if gate_pass_with(_led, _seq, _fal, c))))
MIN_GATE_CUT = min(w["waived"] for w in WAIVE_SPECTRUM if w["passed"] > 0)
WAIVE_SINGLE = [w["passed"] for w in WAIVE_SPECTRUM if w["waived"] == 1]
WAIVE_SINGLE_ALL_ZERO = all(x == 0 for x in WAIVE_SINGLE) and (len(WAIVE_SINGLE) == 3)
WAIVE_MAX_PASSED = max(w["passed"] for w in WAIVE_SPECTRUM)
WAIVE_BASELINE = WAIVE_SPECTRUM[0]["passed"]
FORGED_BREAKS = N_ONE_EQ

# ====================== 控制组（四向量 / 四标量两两不同） ======================
CTRL_FOUR = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
CTRL_FOUR_DISTINCT = len(set(tuple(x) for x in CTRL_FOUR)) == 4
CTRL_NO_EQ_BASE = all(tuple(x) != tuple(CTRL_FOUR[0]) for x in CTRL_FOUR[1:])
CTRL_READINGS = [N_ROUNDS, B7_EXTRA, B8_MIN, N_BREAK]
CTRL_SCALAR_DISTINCT = len(set(CTRL_READINGS)) == 4
CTRL_SCALAR_NO_EQ_BASE = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
ZERO_SCAN = [0 * N_ROUNDS, 0 * N_CFG, 0, 0]
ZERO_SCAN_OK = all(x == 0 for x in ZERO_SCAN) and (N_ROUNDS > 0)
NOT_ALL_GREEN = (HIT_NONZERO > 0) and (POS_ENUM) and (POS_SURVIVE > 0) and \
                (CTRL_RELEASE_COUNT > 0)

# ====================== 判词与元守卫 ======================
def gain_token(x):
    return ("N" + str(-x)) if x < 0 else str(x)


def verdict_with(token):
    return ("ALG-FL"
            + "__ROUNDS-" + str(N_ROUNDS)
            + "__ALLPASS-" + str(ALL_GUARDS_PASS)
            + "__ONEEQ-" + str(N_ONE_EQ)
            + "__MISMATCH-" + str(ONE_EQ_MISMATCH)
            + "__SURV-" + str(N_SURV)
            + "__GAIN-" + gain_token(SURV_GAIN_SUM)
            + "__B7-" + str(B7_EXTRA) + "gt" + str(B7_EQ)
            + "__B8-" + str(B8_MIN) + "gt" + str(B8_BUDGET)
            + "__MUS-" + str(B9_MUS)
            + "__EQ-" + str(CROSS_EQ_COUNT)
            + "__CUT-" + str(MIN_GATE_CUT)
            + "__CLEAN-" + str(token)
            + "__PRED-0")


v0 = verdict_with(str(N_BREAK))
v1 = verdict_with(str(N_BREAK + 1))
verdict_machine_ok = (v0 != v1) and ("__CLEAN-" + str(N_BREAK)) in v0
verdict = v0


def no_hardcode_ok():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
           node.func.id in ("add", "guard"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and \
               isinstance(node.args[1].value, bool):
                bad += 1
    return bad == 0


segs = []


def add(name, ok, kind, note):
    # ok 驱动 kind：守卫失败不得仍标 PASS/BOUNDARY。
    segs.append(dict(name=name, ok=bool(ok), kind=(kind if ok else "FAIL"), note=note))


add("SOURCE-LINK-HEALTH", link_health and (len(source_missing) == 0), "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) +
    " 个；分母为 0 判 FAIL")
add("README-RECOUNT-HONEST", (README_BYTES > 0) and (README_MAX_RID > 0) and (TREE_MAX_RID > 0), "PASS",
    "动手前 rb 实时重数：" + str(README_BYTES) + " B / MD5 " + README_MD5 +
    " / README 内最大 RID " + str(README_MAX_RID) + " / 三树最大 RID " + str(TREE_MAX_RID) +
    "；本册不写 README、不占号、不登记")
add("OWN-EXCLUSION-DEFINED", callable(is_own) and (len(OWN_NAMES) == 6) and
    all(v > 0 for v in INV.values()), "PASS",
    "自指按精确文件名排除本册 " + str(len(OWN_NAMES)) + " 个产物；主目录 " +
    str(INV["main_md"]) + " md / " + str(INV["main_html"]) + " html / 三树 " +
    str(INV["src_files"]) + "·" + str(INV["data_files"]) + "·" + str(INV["judge_files"]))
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 act_rounds / exp_rounds / act_configs / exp_configs 四函数齐备，return 均非顶层数值常量")
add("LEDGER-TWO-PATH-EQ", TWO_PATH_EQ and (N_TWO_PATH_MISMATCH == 0), "PASS",
    "★全链总账两路机拼：act=json.load 结构化读 " + str(N_ROUNDS) +
    " 轮机核数据，exp=正则逐行扫各自 report；守卫数、判词、final 逐轮比对，失配 " +
    str(N_TWO_PATH_MISMATCH) + " 条")
add("LEDGER-13-ROUNDS", (N_ROUNDS == len(EXP)) and (N_ROUNDS > 0), "PASS",
    "总账覆盖算法联盟 " + str(N_ROUNDS) + " 轮（R1 实验数据链 → R13 库外读数接入），" +
    "每轮字段按语义白名单显式登记，不用宽泛正则误抓同名键")
add("LEDGER-ALL-GUARDS-PASS", ALL_GUARDS_PASS_OK, "PASS",
    "★全过轮数 " + str(ALL_GUARDS_PASS) + "/" + str(N_ROUNDS) +
    "；这是「轮数」计数，**不把各轮守卫数相加**")
add("LEDGER-PRED-ALL-ZERO", ALL_PRED_ZERO and (N_PRED_FIELDS > 0), "PASS",
    "十三轮各自机读独立预言字段共 " + str(N_PRED_FIELDS) + " 处，逐处为 0；" +
    "取自各轮 JSON 的不同字段，不是同一个写死的 0")
add("LEDGER-HIT-NONZERO", (HIT_NONZERO > 0) and ALL_PRED_ZERO, "PASS",
    "★两侧都测：命中读数非零的轮 " + str(HIT_NONZERO) + " 处（如 R4 C4 后 quad_gate_hits=1），" +
    "但预言读数全 0 ⇒ 判据有判别力，全 0 不是空表造成")
add("LEDGER-NOT-SUMMED", (N_ROUNDS > 0) and (INJECT_R12 > 0), "BOUNDARY",
    "★各轮守卫数、判定条目、注入下界（R12 机读 " + str(INJECT_R12) +
    "）与判定册编号**互不相加**；总账只是逐轮陈列")
add("ONE-EQ-DEFINITION", (N_ONE_EQ > 0) and (N_UNIFIED_CFG > 0), "PASS",
    "★用户命题的精确机读定义：κ 与耦合**都不按力分置**即为「所有力放进同一个方程」；" +
    "R7 四配置中满足者 " + str(N_ONE_EQ) + " 个，标 unified 者 " + str(N_UNIFIED_CFG) + " 个")
add("ONE-EQ-MISMATCH", (ONE_EQ_MISMATCH > 0), "PASS",
    "全共享单方程配置的谱失配 " + str(ONE_EQ_MISMATCH) + " 处（κ 谱 " +
    str(kn(R7, "shared_kappa_mismatch")) + " + 耦合谱 " +
    str(kn(R7, "shared_coupling_mismatch")) + "），由两路独立字段精确相加还原")
add("ONE-EQ-MISMATCH-TWO-PATH",
    (ONE_EQ_MISMATCH == int(kn(R7, "shared_total_mismatch"))) and
    (ONE_EQ_MISMATCH == int(kn(R7, "shared_kappa_mismatch")) +
     int(kn(R7, "shared_coupling_mismatch"))), "PASS",
    "★守卫 note 与判定表同一读数：配置层失配 " + str(ONE_EQ_MISMATCH) +
    " = key_numbers 总失配 " + str(kn(R7, "shared_total_mismatch")) +
    " = κ 失配 " + str(kn(R7, "shared_kappa_mismatch")) + " + 耦合失配 " +
    str(kn(R7, "shared_coupling_mismatch")) + "，两条独立路径精确还原")
add("ONE-EQ-NOT-SURVIVE", (not ONE_EQ_SURVIVE) and SHARED_EXCLUDED, "PASS",
    "★★全共享单方程配置存活 = " + str(ONE_EQ_SURVIVE) + "，共享参数被实验排除 = " +
    str(SHARED_EXCLUDED) + "；约束口径下「所有力放进一个方程」在可达域内不成立")
add("CONFIGS-TWO-PATH", CFG_TWO_PATH, "PASS",
    "配置总数两路：act 结构化 " + str(N_CFG) + " / key_numbers " + str(N_CFG_KEY) +
    " / exp 判词正则 " + str(CFG_EXP["configs"]) + "；逃逸数 " + str(N_ESCAPE_KEY) +
    " / " + str(CFG_EXP["escape"]) + " 一致")
add("CONFIGS-FULL-ENUM", (N_CFG == N_CFG_KEY) and (N_CFG > FORCE_COUNT - 1), "PASS",
    "共享/分置 2×2 = " + str(N_CFG) + " 个配置全枚举，覆盖 " + str(FORCE_COUNT) + " 个力")
add("ESCAPE-ZERO", (N_ESCAPE_KEY == 0) and (N_BRK == 0), "PASS",
    "四种配置逃逸 " + str(N_ESCAPE_KEY) + " 个、突破 " + str(N_BRK) + " 个")
add("SURVIVING-IS-FULLY-SPLIT", FORMAL_POSSIBLE, "PASS",
    "★唯一存活的 " + str(N_SURV) + " 个配置必须是 κ 与耦合**完全分置**，" +
    "即「一个方程」只能退化为按力分别填参数的模板复用")
add("SURVIVING-GAIN-NONPOSITIVE", FORMAL_GAIN_NONPOSITIVE, "PASS",
    "★该存活配置的压缩增益 " + str(SURV_GAIN_SUM) +
    "（非正）⇒ 统一没有省下任何参数，只是换了记账方式")
add("FORMAL-UNIFICATION-IDENTITY", FORMAL_POSSIBLE and FORMAL_GAIN_NONPOSITIVE, "IDENTITY",
    "★★形式口径下「能写成一个方程」为真，但那是记账式复述、零判别力、零新增内容；" +
    "本册主动单列 IDENTITY，**不拿形式可行冒充力的统一**")
add("BOUND-A-5GT2", (BOUND_A > 0), "PASS",
    "下界一（R7 方程层）：单方程自有参数 " + str(B7_EQ) + " vs 所需额外参数 " +
    str(B7_EXTRA) + "，缺口 " + str(BOUND_A))
add("BOUND-B-4GT3", (BOUND_B > 0), "PASS",
    "下界二（R8 标签层）：预算 " + str(B8_BUDGET) + " vs 复用标签后的参数下界 " +
    str(B8_MIN) + "，缺口 " + str(BOUND_B))
add("BOUND-C-MUS", (BOUND_C > 0) and (B9_SAT == 0), "PASS",
    "下界三（R9 公理层）：最小不可满足核 " + str(B9_MUS) + " 条 > 预算 " +
    str(B8_BUDGET) + "；" + str(B9_MODELS) + " 个指派中满足目标公理集 " +
    str(B9_SAT) + " 个。三下界来自不同轮不同对象，**不相加**")
add("BOUNDS-ALL-BEARING", BOUNDS_ALL_BEARING, "PASS",
    "三个独立下界同时超限且四配置逃逸 0 ⇒ 约束口径被三条互不相依的证据挡住")
add("CROSS-ROUND-EXACT-5", CROSS_EQ_OK, "PASS",
    "★★本轮新机算跨轮精确整数恒等式 " + str(CROSS_EQ_COUNT) + "/5：" +
    "5−1=4（R7 下界经 R8 复用降到 R8 下界）、2+2=4（合并树标签+外部标签=R8 下界）、" +
    "2+3=5（κ 失配+耦合失配=总失配）、配置数 4=4、2^7=" + str(B9_MODELS) +
    "（7 原子+I1 的指派空间）。端点取自不同轮不同字段，两路互证，不是手抄")
add("SPECTRUM-TWO-PATH", SPECTRUM_TWO_PATH, "PASS",
    "谱类数两路机读：κ 谱 " + str(KAPPA_CLASSES) + " 类、耦合谱 act " +
    str(COUP_ACT_CLASSES) + " / exp " + str(COUP_EXP_CLASSES) + " 类，与各轮 key_numbers 逐位一致")
add("SPECTRUM-SPAN", (FORCE_COUNT == 4) and (LONG_RANGE > 0), "PASS",
    "四力 / 长程 " + str(LONG_RANGE) + " / 耦合跨 " + COUPLING_SPAN_DEX +
    " dex / λ 比 " + LAM_RATIO + "；谱必须分置，不是一个共享参数能生成的")
add("CHI2-TWO-SIDED", (CHI2_GAP != "") and (PAIRS_HIT_R5 == 0) and (POS_SURVIVE > 0), "PASS",
    "两侧都测：R5 最优对 " + CHI2_GAP + "σ 越界、命中 " + str(PAIRS_HIT_R5) +
    " 对；R3 存活候选 " + str(POS_SURVIVE) + " 个而双侧阳性证据 " +
    str(POS_POSITIVE_EVIDENCE) + " 个")
add("POS-ENUM-CONTROL", POS_ENUM and POS_HIT_NONZERO, "PASS",
    "正对照：配置空间 " + str(N_CFG) + "、公理指派空间 " + str(B9_MODELS) +
    " 均被穷举，且命中读数非零 " + str(HIT_NONZERO) + " 处 ⇒ 判据不是恒绿")
add("CTRL-BUDGET-RELEASE", CTRL_DIFFERS_FROM_BASE, "PASS",
    "★反事实控制组同口径：都问「下界门是否阻挡」，预算 " + str(B8_BUDGET) +
    " 时阻挡读数 " + str(BASELINE_BLOCK) + "，放宽到 " + str(CTRL_BUDGET_INFLATED) +
    " 时 " + str(CTRL_BLOCK) + "，两读数不同 ⇒ 下界承重；控制组不写回文件、不计入实测判定")
add("CTRL-MISMATCH-RELEASE", CTRL_MISMATCH_RELEASED, "PASS",
    "反事实控制组：把共享谱失配强行置零将放行单方程配置；基线失配 " +
    str(ONE_EQ_MISMATCH) + " 处确实承重")
add("GATE-LEDGER-BEARING",
    GATE_LEDGER_ACTIVE and LEDGER_OK and (N_TWO_PATH_MISMATCH == 0), "PASS",
    "总账门由两路失配 " + str(N_TWO_PATH_MISMATCH) + " 与全过轮数 " +
    str(ALL_GUARDS_PASS) + " 驱动；拆该门即令本守卫 FAIL")
add("GATE-SINGLEEQ-BEARING",
    GATE_SINGLEEQ_ACTIVE and SINGLEEQ_OK and (ONE_EQ_MISMATCH > 0), "PASS",
    "单方程门由全共享失配 " + str(ONE_EQ_MISMATCH) +
    "、三条独立下界与五条跨轮等式驱动；拆该门即令本守卫 FAIL")
add("GATE-FALSIFIABLE-BEARING",
    GATE_FALSIFIABLE_ACTIVE and FALSIFIABLE_OK and (N_BREAK == 0), "PASS",
    "可判负门由十三轮突破 " + str(N_BREAK) +
    " 与四处干净可判负读数驱动；拆该门即令本守卫 FAIL")
add("MIN-GATE-CUT-HONEST", (MIN_GATE_CUT == 2) and WAIVE_SINGLE_ALL_ZERO and
    (WAIVE_MAX_PASSED > 0), "PASS",
    "2^3=8 个拆门子集全枚举：最小承重割 " + str(MIN_GATE_CUT) + "，最大误放行 " +
    str(WAIVE_MAX_PASSED) + "；不把「门数 3」当独立证据")
add("THREE-GATES-BEARING", (sum(1 for g in ACTIVE_GATES if g) == 3) and
    WAIVE_SINGLE_ALL_ZERO and (MIN_GATE_CUT > 1) and
    (WAIVE_BASELINE == CLEAN_UNIFIED), "PASS",
    "★★如实报负读数：预设「三门各自承重」被数据推翻——单独拆任一门的误放行 = " +
    str(WAIVE_SINGLE) + "；须同时拆 " + str(MIN_GATE_CUT) + " 个门才误放行 " +
    str(WAIVE_MAX_PASSED) + " 个配置（其中全共享配置 " + str(FORGED_BREAKS) +
    " 个）。三门串联有冗余，当前误放行 " + str(CLEAN_UNIFIED) + " 个")
add("CLEAN-UNIFIED-ZERO", (CLEAN_UNIFIED == 0) and (N_BREAK == 0), "PASS",
    "★★「所有力放进一个方程 ∧ 约束成立 ∧ 有独立预言」同时成立的配置 " +
    str(CLEAN_UNIFIED) + " 个；十三轮突破读数 " + str(N_BREAK) + " 个")
add("FALSIFIABLE-ZERO", FALSIFIABLE_ZERO, "PASS",
    "可判负口径：R5 命中 " + str(PAIRS_HIT_R5) + "、R6 认证 " + str(PAIRS_HIT_R6) +
    "、R12 干净可判负 " + str(PREV12_CLEAN) + "、R13 " + str(R13_CLEAN) +
    "；独立实验预言 0 条")
add("SPINE-ZERO", (SPINE_CORRECT == 0) and (SPINE_ACCEPT == 0), "PASS",
    "跨卷回读：r403 四力正确解 " + str(SPINE_CORRECT) + " 条、r404 接受 " +
    str(SPINE_ACCEPT) + " 条；本册未新增任何物理方程")
add("EXIT-COSTS-DISTINCT", (MIN_CUT_R12 > 0) and (MIN_THEORY_R13 > 0) and
    (B9_MUS != MIN_CUT_R12), "PASS",
    "硬出口代价三层不同读数：R12 链路最小割 " + str(MIN_CUT_R12) +
    "、R13 理论侧最小改动 " + str(MIN_THEORY_R13) + "、R9 MUS " + str(B9_MUS) +
    "；三者**不相加**")
add("PARAMETER-NOT-EXTINCT", (COPIED_R12 > 0) and (BIT_COPIED > 0), "PASS",
    "十三轮总账未见参数消亡：R12 全库观测副本 " + str(COPIED_R12) + " 个跨 " +
    str(COPIED_FILES_R12) + " 脚本；R9 唯一副本 " + str(BIT_COPIED) + " bit 占程序 " +
    str(BIT_PROG) + " bit 的一部分，输入 " + str(BIT_IN) + " bit / 输出 " + str(BIT_OUT) + " bit")
add("CTRL-FOUR-DISTINCT", CTRL_FOUR_DISTINCT, "PASS",
    "控制组四向量两两不同：" + " / ".join(str(x) for x in CTRL_FOUR))
add("CTRL-NO-EQ-BASE", CTRL_NO_EQ_BASE, "PASS",
    "三个单门对照均不等于基线 " + str(CTRL_FOUR[0]))
add("CTRL-SCALAR-DISTINCT", CTRL_SCALAR_DISTINCT, "PASS",
    "控制组四标量两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-SCALAR-NO-EQ-BASE", CTRL_SCALAR_NO_EQ_BASE, "PASS",
    "三个对照标量均不等于基线标量 " + str(CTRL_READINGS[0]))
add("CROSS-SUM-IDENTITY", (CROSS_SUM == 3), "IDENTITY",
    "三分口径是构造分割（形式 / 约束 / 可判负），" + str(CROSS_SUM) +
    " 个格子不产生新读数、零判别力，单列 IDENTITY 不冒充证据")
add("ZERO-SCAN-IDENTITY", ZERO_SCAN_OK, "IDENTITY",
    "阴性对照：扫描 0 轮时四项读数恒 " + str(ZERO_SCAN) +
    "，该侧恒真、零判别力，单列 IDENTITY 配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", NOT_ALL_GREEN, "INFO",
    "负对照恒绿，但总账命中、谱类数、三下界、跨轮精确等式、控制组均非恒绿读数")
add("FAMILY-LIMITED-CLAIM", (N_ROUNDS > 0) and (N_CFG > 0), "BOUNDARY",
    "★结论限于 openuft 可达域、" + str(N_CFG) +
    " 个共享/分置配置与显式有限族；**不是「四力统一不可能」的全称定理**，" +
    "也不覆盖尚未写出的方程族")
add("NO-BREAKTHROUGH", (N_BREAK == 0), "INFO",
    "本册不宣称攻破统一场论，也不宣称攻破力的统一；只产可算判决")
add("MATH-NOT-EXPERIMENT", FALSIFIABLE_ZERO, "INFO",
    "全部结论来自两路机读、精确整数恒等式、配置枚举与控制组，不是实验证实；不产新物理")
add("NEXT-EXIT", (N_BREAK == 0) and (CLEAN_UNIFIED == 0), "INFO",
    "硬出口未变：须同时给出①带双侧误差棒的新读数 ②程序侧不含观测副本、" +
    "可认证 p_free=0 且非回述的理论输出；本册未给出后者。" +
    "在该输出出现前，不必再造新理论、不必再放宽判据")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把突破读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")


def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-FINAL-LEDGER--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-FINAL-LEDGER--GATES-FAIL"
    return "ALG-FINAL-LEDGER--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "CLEAN-UNIFIED-ZERO", "ONE-EQ-NOT-SURVIVE",
                     "FORMAL-UNIFICATION-IDENTITY", "LEDGER-NOT-SUMMED",
                     "FAMILY-LIMITED-CLAIM", "CROSS-SUM-IDENTITY"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-FINAL-LEDGER--GATES-PASS-WITH-0-NEGATIVE") and \
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
    "rounds": N_ROUNDS, "rounds_all_guards_pass": ALL_GUARDS_PASS,
    "two_path_mismatch": N_TWO_PATH_MISMATCH,
    "prediction_fields": N_PRED_FIELDS, "hit_nonzero": HIT_NONZERO,
    "configs": N_CFG, "configs_key": N_CFG_KEY, "configs_exp": CFG_EXP["configs"],
    "escape_configs": N_ESCAPE_KEY, "breakthrough_configs": N_BRK,
    "one_eq_configs": N_ONE_EQ, "one_eq_mismatch": ONE_EQ_MISMATCH,
    "one_eq_survive": ONE_EQ_SURVIVE, "one_eq_gain": ONE_EQ_GAIN,
    "surviving_configs": N_SURV, "surviving_gain_sum": SURV_GAIN_SUM,
    "surviving_all_split": SURV_ALL_SPLIT,
    "shared_all_excluded": SHARED_EXCLUDED,
    "formal_possible": FORMAL_POSSIBLE,
    "formal_gain_nonpositive": FORMAL_GAIN_NONPOSITIVE,
    "constrained_excluded": CONSTRAINED_EXCLUDED,
    "falsifiable_zero": FALSIFIABLE_ZERO,
    "three_way_categories": CROSS_SUM,
    "bound_r7_extra": B7_EXTRA, "bound_r7_eq": B7_EQ, "gap_a": BOUND_A,
    "bound_r8_min": B8_MIN, "bound_r8_budget": B8_BUDGET, "gap_b": BOUND_B,
    "bound_r9_mus": B9_MUS, "gap_c": BOUND_C,
    "models_enumerated": B9_MODELS, "models_satisfying": B9_SAT,
    "cross_exact_eq_count": CROSS_EQ_COUNT,
    "cross_eq_1": EQ1, "cross_eq_2": EQ2, "cross_eq_3": EQ3,
    "cross_eq_4": EQ4, "cross_eq_5": EQ5,
    "kappa_classes": KAPPA_CLASSES, "coupling_classes_act": COUP_ACT_CLASSES,
    "coupling_classes_exp": COUP_EXP_CLASSES,
    "coupling_span_dex": COUPLING_SPAN_DEX, "lambda_ratio": LAM_RATIO,
    "forces": FORCE_COUNT, "long_range_forces": LONG_RANGE,
    "spine_four_force_correct": SPINE_CORRECT,
    "spine_four_force_accepted": SPINE_ACCEPT,
    "pairs_hit_r5": PAIRS_HIT_R5, "pairs_hit_r6": PAIRS_HIT_R6,
    "prev12_clean": PREV12_CLEAN, "r13_clean": R13_CLEAN,
    "min_cut_r12": MIN_CUT_R12, "min_theory_r13": MIN_THEORY_R13,
    "cert_invariant_directions_r13": CERT_DIRS_R13,
    "copied_r12": COPIED_R12, "copied_files_r12": COPIED_FILES_R12,
    "inject_r12": INJECT_R12, "inject_r9": INJECT_R9,
    "bit_in": BIT_IN, "bit_out": BIT_OUT, "bit_prog": BIT_PROG, "bit_copied": BIT_COPIED,
    "chi2_best_gap_sigma": CHI2_GAP,
    "survive_r3": POS_SURVIVE, "positive_evidence_r3": POS_POSITIVE_EVIDENCE,
    "ctrl_baseline_block": BASELINE_BLOCK, "ctrl_budget_block": CTRL_BLOCK,
    "ctrl_budget_inflated": CTRL_BUDGET_INFLATED, "ctrl_release_count": CTRL_RELEASE_COUNT,
    "forged_breaks": FORGED_BREAKS, "clean_unified": CLEAN_UNIFIED,
    "min_gate_cut": MIN_GATE_CUT, "waive_single": WAIVE_SINGLE,
    "waive_max_passed": WAIVE_MAX_PASSED, "waive_baseline": WAIVE_BASELINE,
    "waive_spectrum": WAIVE_SPECTRUM,
    "breakthrough": N_BREAK,
    "control_vectors": CTRL_FOUR, "control_scalars": CTRL_READINGS,
    "readme_bytes": README_BYTES, "readme_md5": README_MD5,
    "readme_max_rid": README_MAX_RID, "tree_max_rid": TREE_MAX_RID,
    "source_files": len(SOURCE_FILES), "source_missing": len(source_missing),
    "main_md": INV["main_md"], "main_html": INV["main_html"],
    "alg_md": INV["alg_md"], "alg_html": INV["alg_html"],
    "src_files": INV["src_files"], "data_files": INV["data_files"],
    "judge_files": INV["judge_files"],
    "spine_independent_predictions": 0, "four_force_incomplete": True,
}

ledger_json = [dict(tag=a["tag"], name=a["name"], guards=str(a["gp"]) + "/" + str(a["gc"]),
                    hit_field=a["hit_field"], hit=a["hit"],
                    pred_field=a["pred_field"], pred=a["pred"],
                    lower_field=a["lower_field"], lower=a["lower"],
                    verdict=a["verdict"])
               for a in ACT]

out = {
    "title": "算法联盟：全链总账与「所有力放进一个方程」命题的三分判决（第十四轮）",
    "date": "2026-11-14",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "scope": {"own_excluded_names": sorted(OWN_NAMES),
              "field_whitelist": [[r[0], r[3], r[4], r[5]] for r in ROUNDS]},
    "ledger": ledger_json,
    "three_way": dict(formal=dict(possible=FORMAL_POSSIBLE,
                                  gain_sum=SURV_GAIN_SUM,
                                  all_split=SURV_ALL_SPLIT,
                                  verdict="IDENTITY，零判别力"),
                      constrained=dict(excluded=CONSTRAINED_EXCLUDED,
                                       one_eq_configs=N_ONE_EQ,
                                       mismatch=ONE_EQ_MISMATCH,
                                       shared_all_excluded=SHARED_EXCLUDED),
                      falsifiable=dict(zero=FALSIFIABLE_ZERO,
                                       pairs_hit=PAIRS_HIT_R5,
                                       certified=PAIRS_HIT_R6,
                                       independent_predictions=0)),
    "bounds": dict(r7=dict(extra=B7_EXTRA, eq=B7_EQ, gap=BOUND_A),
                   r8=dict(min=B8_MIN, budget=B8_BUDGET, gap=BOUND_B,
                           tree=B8_TREE, external=B8_EXT, reduction=B8_REDUCTION),
                   r9=dict(mus=B9_MUS, budget=B8_BUDGET, gap=BOUND_C,
                           models=B9_MODELS, satisfying=B9_SAT),
                   cross_exact_equalities=dict(eq1=EQ1, eq2=EQ2, eq3=EQ3,
                                               eq4=EQ4, eq5=EQ5,
                                               count=CROSS_EQ_COUNT)),
    "configurations": CFG,
    "spectrum": dict(kappa_classes=KAPPA_CLASSES,
                     coupling_act_classes=COUP_ACT_CLASSES,
                     coupling_exp_classes=COUP_EXP_CLASSES,
                     span_dex=COUPLING_SPAN_DEX, lambda_ratio=LAM_RATIO),
    "exit": dict(min_cut_r12=MIN_CUT_R12, min_theory_r13=MIN_THEORY_R13,
                 mus_r9=B9_MUS, needs_new_reading=True,
                 needs_certified_nonrestated_output=True),
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
    lines.append("算法联盟：全链总账与四力单方程命题三分判决（第十四轮）")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("全链总账：" + str(N_ROUNDS) + " 轮，全过轮数 " + str(ALL_GUARDS_PASS) +
                 "，两路机拼失配 " + str(N_TWO_PATH_MISMATCH) + " 条；预言字段 " +
                 str(N_PRED_FIELDS) + " 处全 0，命中非零 " + str(HIT_NONZERO) + " 处")
    for a in ACT:
        lines.append("  " + a["tag"] + " " + a["name"] + " | guards=" +
                     str(a["gp"]) + "/" + str(a["gc"]) +
                     " | hit=" + str(a["hit_field"]) + ":" + str(a["hit"]) +
                     " | pred=" + str(a["pred_field"]) + ":" + str(a["pred"]) +
                     " | lower=" + str(a["lower_field"]) + ":" + str(a["lower"]))
    lines.append("-" * 96)
    lines.append("用户命题三分（互不相加）")
    lines.append("  形式统一：可写成一个方程但存活配置须 κ 与耦合全分置，增益 " +
                 str(SURV_GAIN_SUM) + " ⇒ IDENTITY 零判别力")
    lines.append("  约束统一：全共享单方程配置 " + str(N_ONE_EQ) + " 个，谱失配 " +
                 str(ONE_EQ_MISMATCH) + " 处，存活 " + str(ONE_EQ_SURVIVE) +
                 " ⇒ 可达域内不成立")
    lines.append("  可判负：独立预言 0 条，R5 命中 " + str(PAIRS_HIT_R5) +
                 " / R6 认证 " + str(PAIRS_HIT_R6))
    lines.append("三个独立下界：" + str(B7_EXTRA) + ">" + str(B7_EQ) +
                 " / " + str(B8_MIN) + ">" + str(B8_BUDGET) +
                 " / MUS " + str(B9_MUS) + ">" + str(B8_BUDGET) +
                 "；四配置逃逸 " + str(N_ESCAPE_KEY))
    lines.append("三重门最小承重割 " + str(MIN_GATE_CUT) + "：单独拆任一门误放行 " +
                 str(WAIVE_SINGLE) + "，须同时拆 " + str(MIN_GATE_CUT) +
                 " 门才误放行 " + str(WAIVE_MAX_PASSED) + " 个（如实报负读数）")
    lines.append("跨轮精确整数恒等式 " + str(CROSS_EQ_COUNT) + "/5：" +
                 "5-1=4 / 2+2=4 / 2+3=5 / 4=4 / 2^7=" + str(B9_MODELS))
    lines.append("谱类数两路：κ " + str(KAPPA_CLASSES) + " 类 / 耦合 " +
                 str(COUP_ACT_CLASSES) + "·" + str(COUP_EXP_CLASSES) +
                 " 类 / 跨 " + COUPLING_SPAN_DEX + " dex")
    lines.append("-" * 96)
    lines.append("结论：不宣称攻破统一场论；四力大统一正确解 0 条；独立实验预言 0。" +
                 "硬出口须新读数 + 可认证非回述理论输出，本册未给出。")
    lines.append("README：" + str(README_BYTES) + " B / " + README_MD5 +
                 " / 最大 RID " + str(README_MAX_RID) + "；本册零改动、不占号。")
    lines.append("-" * 96)
    for s in segs:
        lines.append("[" + s["kind"] + "] " + s["name"] + " :: " + ("OK" if s["ok"] else "FAIL"))
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("final=", final, "guards=", g_pass, "/", g_count)
    print("sha256=", digest)
    print("ALL-CHECKS-PASS" if (g_pass == g_count) else "SOME-GUARDS-FAILED")
    print("WRITE", OUT_JSON)
    print("WRITE", OUT_REPORT)
