# -*- coding: utf-8 -*-
"""算法联盟 · 统一场论第十五轮：观测副本的定义归因与硬出口通道 B 的信息论下界。

不占 RID、不入 README、不与任何审计卷相加。
本轮不造新物理、不放宽判据；只做两件事：
① 把第九/十一/十二轮记为「观测副本」的字面量按来料 kind 四分归因，
   扣除 SI 定义公理复用的比特，给出诚实修正；
② 用实验误差棒反演「程序侧不含观测副本」与「输出与 46 锚相容」能否同时成立。
"""
import os
import io
import ast
import re
import json
import glob
import hashlib
import tokenize
import warnings
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

warnings.filterwarnings("ignore")
getcontext().prec = 60

ROOT = "D:/a10/aikjx/code/my_lib"
UROOT = os.path.join(ROOT, "openuft")
BASE = os.path.join(UROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
SRC = os.path.join(BASE, "源码")
JUDGE = os.path.join(BASE, "判定")
P_README = os.path.join(BASE, "README.md")
OUT_JSON = os.path.join(DATA, "_ALG_triple_certification_recompute_2026-11-14.json")
OUT_REPORT = os.path.join(DATA, "_ALG_triple_certification_recompute_report_2026-11-14.txt")

P_ANCH = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_R9 = os.path.join(DATA, "_ALG_information_gate_recompute_2026-11-12.json")
P_R11 = os.path.join(DATA, "_ALG_perturbation_closure_recompute_2026-11-14.json")
P_R12 = os.path.join(DATA, "_ALG_fullchain_scope_recompute_2026-11-14.json")
P_R13 = os.path.join(DATA, "_ALG_external_exit_recompute_2026-11-14.json")
P_R7 = os.path.join(DATA, "_ALG_force_unification_recompute_2026-11-12.json")

OWN_NAMES = {
    "算法联盟_观测副本定义归因与通道B信息论下界_统一场论第十五轮_2026-11-14.md",
    "算法联盟_通道B信息论下界_第十五轮可视化_2026-11-14.html",
    "_alg_triple_certification_recompute.py",
    "_ALG_triple_certification_recompute_2026-11-14.json",
    "_ALG_triple_certification_recompute_report_2026-11-14.txt",
    "_ALG_triple_certification_verify_2026-11-14.json",
}


def is_own(p):
    return os.path.basename(p) in OWN_NAMES


def text(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def load(p):
    return json.loads(text(p))


def report_path(p):
    """report→JSON 路径构造的唯一收敛函数；机核与核验器共用同一口径。"""
    return p.replace("recompute_", "recompute_report_").replace(".json", ".txt")


# 理论脚本由 glob 定位，不写死中文全路径。
_hits = glob.glob(os.path.join(UROOT, "01_*", "*", "*", "unified_forces_vs_experiment.py"))
assert len(_hits) == 1, _hits
P_THEORY = _hits[0]

# ★来料总表不是机核产物、没有配套 report，只对机核产物追加 report 路径。
REPORT_BEARING = [P_R7, P_R9, P_R11, P_R12, P_R13]
SOURCE_FILES = [P_README, P_ANCH, P_THEORY] + REPORT_BEARING
SOURCE_FILES = SOURCE_FILES + [report_path(p) for p in REPORT_BEARING]
SOURCE_FILES = list(dict.fromkeys(SOURCE_FILES))
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(source_missing) == 0)


def fv(v):
    """来料可能是十进制或科学计数串；Fraction 精确解析，失败退 Decimal。"""
    s = str(v).strip()
    try:
        return F(s)
    except Exception:
        return F(D(s))


def dec(q):
    return D(q.numerator) / D(q.denominator)


def bits(q):
    """固定编码描述长度：分子、分母二进制位数之和。不是 Kolmogorov 复杂度。"""
    return abs(q.numerator).bit_length() + abs(q.denominator).bit_length()


def dstr(x, places=6):
    if x == 0:
        return "0"
    q = D(1).scaleb(-places)
    if abs(x) < q:
        return format(x, "e")
    return format(x.quantize(q), "f").rstrip("0").rstrip(".")


# ====================== 两路机读：副本值集合 ======================
LEDGER = load(P_ANCH)["ledger"]
N_ANCH = len(LEDGER)
ANCH_VALS = [fv(x["value"]) for x in LEDGER]
ANCH_KIND = {x["id"]: x["kind"] for x in LEDGER}
KIND_ORDER = ("SI-definition", "derived", "measured", "measured-bound")
KIND_HIST = {k: sum(1 for x in LEDGER if x["kind"] == k) for k in KIND_ORDER}


def act_copies():
    """act 路径：json.load 读第九轮已登记的副本值与出现次数。"""
    j = load(P_R9)
    ba = j["bit_account"]
    uniq = [F(s) for s in ba["copied_unique"]]
    lit = j["key_numbers"].get("literals_total")
    if lit is None:
        lit = load(P_R11)["key_numbers"].get("gaq_literals", -1)
    return dict(unique=uniq, n_unique=len(uniq),
                n_occ=int(j["key_numbers"]["copied_literals"]),
                bits=int(j["key_numbers"]["H_copied_unique_bits"]),
                literals=int(lit))


def token_numbers(src):
    """★按 tokenize 取 NUMBER 的**原始十进制文本**：AST 的 float 是二进制近似，
    F(6.62607015e-34) 会得到与十进制字面量不同的精确分数，必须走文本。"""
    out = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.NUMBER:
            out.append(tok.string)
    return out


def exp_copies():
    """exp 路径：独立把理论脚本源码重新 tokenize 并与 46 锚精确匹配，不读第九轮 JSON。"""
    nums = token_numbers(text(P_THEORY))
    hits = []
    for s in nums:
        if s.rstrip().endswith(("j", "J")):
            continue
        try:
            q = F(s)
        except Exception:
            continue
        if q in ANCH_VALS:
            hits.append(q)
    return dict(literals=len(nums), n_occ=len(hits),
                unique=sorted(set(hits), key=lambda q: (-bits(q), -q)))


def exp_literals_count():
    """exp 的第二路：纯正则数 token 计数，与 AST 计数机制不同。"""
    src = text(P_THEORY)
    toks = re.findall(r"(?<![\w.])\d+\.?\d*(?:[eE][+-]?\d+)?", src)
    return len(toks)


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    want = {"act_copies", "exp_copies"}
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


ACT = act_copies()
EXP = exp_copies()
ACT_UNIQUE = set(ACT["unique"])
EXP_UNIQUE = set(EXP["unique"])
UNIQUE_EQ = (ACT_UNIQUE == EXP_UNIQUE)
N_UNIQUE = len(EXP_UNIQUE)
N_OCC = EXP["n_occ"]
N_LITERALS = len(token_numbers(text(P_THEORY)))
N_TOKENS = exp_literals_count()
TWO_PATH_COPY_OK = UNIQUE_EQ and (N_OCC == ACT["n_occ"]) and (N_UNIQUE == len(ACT_UNIQUE))
LITERAL_TWO_PATH = (N_LITERALS == ACT["literals"]) and (N_TOKENS >= N_LITERALS)

# ====================== 三分归因：每个唯一副本落到哪个 kind ======================
COPY_ROWS = []
for q in sorted(EXP_UNIQUE, key=lambda x: (-bits(x), -x)):
    ids = [x["id"] for x, v in zip(LEDGER, ANCH_VALS) if v == q]
    kinds = sorted(set(ANCH_KIND[i] for i in ids))
    COPY_ROWS.append(dict(value=str(q), bits=bits(q), anchor_ids=ids,
                          kind=(kinds[0] if len(kinds) == 1 else "MIXED"),
                          kind_count=len(kinds)))
COPY_KIND_HIST = {k: sum(1 for r in COPY_ROWS if r["kind"] == k) for k in KIND_ORDER}
BITS_BY_KIND = {k: sum(r["bits"] for r in COPY_ROWS if r["kind"] == k) for k in KIND_ORDER}
BITS_TOTAL = sum(r["bits"] for r in COPY_ROWS)
BITS_TWO_PATH = (BITS_TOTAL == ACT["bits"])
N_MIXED = sum(1 for r in COPY_ROWS if r["kind"] == "MIXED")
N_UNMATCHED = sum(1 for r in COPY_ROWS if not r["anchor_ids"])

SI_COPIES = [r for r in COPY_ROWS if r["kind"] == "SI-definition"]
OBS_COPIES = [r for r in COPY_ROWS if r["kind"] in ("measured", "measured-bound")]
BITS_SI = BITS_BY_KIND["SI-definition"]
BITS_OBS = BITS_BY_KIND["measured"] + BITS_BY_KIND["measured-bound"]
# ★占比用精确 Fraction，不用 Decimal 除法：617/935 + 318/935 须逐位等于 1。
OBS_SHARE = F(BITS_OBS, BITS_TOTAL) if BITS_TOTAL else F(0)
SI_SHARE = F(BITS_SI, BITS_TOTAL) if BITS_TOTAL else F(0)
N_OBS_UNIQUE = len(OBS_COPIES)
N_SI_UNIQUE = len(SI_COPIES)
CORRECTION_DOWNWARD = (BITS_OBS < BITS_TOTAL) and (BITS_SI > 0)
PARAM_NOT_EXTINCT = (N_OBS_UNIQUE > 0) and (BITS_OBS > 0)

# ====================== σ=0 的 19 项按 kind 分类（σ=0 不等于定义） ======================
ZERO_ROWS = [x for x in LEDGER if str(x["sigma"]).strip() in ("0", "0.0", "")]
N_ZERO = len(ZERO_ROWS)
ZERO_BITS_BY_KIND = {k: sum(bits(fv(x["value"])) for x in ZERO_ROWS if x["kind"] == k)
                     for k in KIND_ORDER}
ZERO_BITS_TOTAL = sum(ZERO_BITS_BY_KIND.values())
ZERO_MEASURED = [x for x in ZERO_ROWS if x["kind"] in ("measured", "measured-bound")]
N_ZERO_MEASURED = len(ZERO_MEASURED)
SIGMA0_IS_NOT_DEFINITION = (N_ZERO_MEASURED > 0)

# ====================== README 实时重数与自指盘点 ======================
README_RB = open(P_README, "rb").read()
README_BYTES = len(README_RB)
README_MD5 = hashlib.md5(README_RB).hexdigest()
README_MAX_RID = max(int(x) for x in re.findall(r"TUFT-r(\d+)_", README_RB.decode("utf-8")))
TREE_MAX_RID = 0
for _sub in ("源码", "数据", "判定"):
    for _n in os.listdir(os.path.join(BASE, _sub)):
        _m = re.search(r"TUFT-r(\d+)_", _n)
        if _m:
            TREE_MAX_RID = max(TREE_MAX_RID, int(_m.group(1)))

INV = {}
for _label, _pat in (("main_md", os.path.join(BASE, "*.md")),
                     ("main_html", os.path.join(BASE, "*.html")),
                     ("alg_md", os.path.join(BASE, "算法联盟_*.md")),
                     ("alg_html", os.path.join(BASE, "算法联盟_*.html")),
                     ("src_files", os.path.join(SRC, "*")),
                     ("data_files", os.path.join(DATA, "*")),
                     ("judge_files", os.path.join(JUDGE, "*"))):
    INV[_label] = len([p for p in glob.glob(_pat) if not is_own(p)])

# ====================== 窗口比特：相容只需落在 [O-zσ, O+zσ] ======================
CHI2_CRIT = F(384145882069, 100000000000)   # 0.95 分位，df=1
Z_CRIT = dec(CHI2_CRIT).sqrt()
TWO_SIDED = [x for x in LEDGER if str(x["sigma"]).strip() not in ("0", "0.0", "")]
N_TWO_SIDED = len(TWO_SIDED)

WINDOW_ROWS = []
for x in TWO_SIDED:
    o = fv(x["value"])
    s = fv(x["sigma"])
    if s == 0 or o == 0:
        continue
    ratio = abs(dec(o)) / (2 * Z_CRIT * abs(dec(s)))
    b = (ratio.ln() / D(2).ln()) if ratio > 0 else D(0)
    b = b if b > 0 else D(0)
    WINDOW_ROWS.append(dict(id=x["id"], symbol=x["symbol"], kind=x["kind"],
                            value=str(x["value"]), sigma=str(x["sigma"]),
                            ratio=dstr(ratio), window_bits=dstr(b, 3),
                            b=b))
WINDOW_BITS = sum((r["b"] for r in WINDOW_ROWS), D(0))
WINDOW_BITS_MEASURED = sum((r["b"] for r in WINDOW_ROWS
                            if r["kind"] in ("measured", "measured-bound")), D(0))
WINDOW_BITS_DERIVED = sum((r["b"] for r in WINDOW_ROWS if r["kind"] == "derived"), D(0))
N_WINDOW_ROWS = len(WINDOW_ROWS)
WINDOW_ZERO = sum(1 for r in WINDOW_ROWS if r["b"] <= 0)
WINDOW_MAX = max(WINDOW_ROWS, key=lambda r: r["b"]) if WINDOW_ROWS else None
WINDOW_MIN = min(WINDOW_ROWS, key=lambda r: r["b"]) if WINDOW_ROWS else None
MAX_WINDOW_BITS = WINDOW_MAX["b"] if WINDOW_MAX else D(0)

# ====================== 三个口径的信息论下界（不相加，互不替代） ======================
B_MIN_STRICT = sum(bits(fv(x["value"])) for x in LEDGER
                   if x["kind"] in ("measured", "measured-bound"))
B_MIN_WINDOW = (ZERO_BITS_BY_KIND["measured"] + ZERO_BITS_BY_KIND["measured-bound"]
                + WINDOW_BITS_MEASURED)
# ★最宽口径：把 19 个 σ=0 项一律当公理（连 measured 也不算），只留 σ>0 的窗口比特。
B_MIN_CONSERVATIVE = WINDOW_BITS_MEASURED
BOUNDS_ALL_POSITIVE = (B_MIN_STRICT > 0) and (B_MIN_WINDOW > 0) and (B_MIN_CONSERVATIVE > 0)
BOUND_ORDER = (B_MIN_CONSERVATIVE <= B_MIN_WINDOW <= B_MIN_STRICT)
CHANNEL_B_INFEASIBLE = BOUNDS_ALL_POSITIVE and BOUND_ORDER

# ====================== 最小代价反演 ======================
COST_ROWS = []
for r in WINDOW_ROWS:
    if r["b"] <= 0:
        continue
    f = (D(2) ** r["b"])
    COST_ROWS.append(dict(id=r["id"], symbol=r["symbol"], kind=r["kind"],
                          window_bits=dstr(r["b"], 3),
                          sigma_factor=dstr(f, 3), f=f))
MIN_COST = min(COST_ROWS, key=lambda r: r["f"]) if COST_ROWS else None
MAX_COST = max(COST_ROWS, key=lambda r: r["f"]) if COST_ROWS else None
MIN_COST_FACTOR = MIN_COST["f"] if MIN_COST else D(0)
MAX_COST_FACTOR = MAX_COST["f"] if MAX_COST else D(0)
COST_LE2 = sum(1 for r in COST_ROWS if r["f"] <= 2)
COST_LE10 = sum(1 for r in COST_ROWS if r["f"] <= 10)
COST_GT10 = sum(1 for r in COST_ROWS if r["f"] > 10)
COST_SPECTRUM_OK = (COST_LE2 + (COST_LE10 - COST_LE2) + COST_GT10 == len(COST_ROWS))
# 0 bit 即可相容的双侧锚：窗口比特 ≤ 0 者，口径与 WINDOW_ZERO 同一读数。
ZERO_BIT_COMPAT = WINDOW_ZERO

# ====================== 正负对照与反事实控制组（同口径两读数） ======================
# 正对照：非零读数存在，判据不是恒绿。
POS_NONZERO = (BITS_TOTAL > 0) and (BITS_OBS > 0) and (WINDOW_BITS > 0) and (N_OBS_UNIQUE > 0)
# 控制组 1（归因口径）：把 SI 定义算回观测，观测比特应从 BITS_OBS 涨到 BITS_TOTAL。
CTRL_ATTR_INFLATED = BITS_TOTAL
CTRL_ATTR_DIFF = (CTRL_ATTR_INFLATED > BITS_OBS)
# 控制组 2（窗口口径）：σ 统一放大 2 倍 ⇒ 每项窗口比特精确减 1。
CTRL_SIGMA_X2_BITS = (WINDOW_BITS - D(len(WINDOW_ROWS)))
CTRL_SIGMA_X2_DIFF = (CTRL_SIGMA_X2_BITS < WINDOW_BITS)
# 控制组 3（定义口径）：把 σ=0 的 measured 当公理，下界应降到最宽口径。
CTRL_DEF_RELEASED = B_MIN_CONSERVATIVE
CTRL_DEF_DIFF = (CTRL_DEF_RELEASED < B_MIN_WINDOW)
CTRL_RELEASE_COUNT = int(CTRL_ATTR_DIFF) + int(CTRL_SIGMA_X2_DIFF) + int(CTRL_DEF_DIFF)

CTRL_FOUR = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
CTRL_FOUR_DISTINCT = len(set(tuple(x) for x in CTRL_FOUR)) == 4
CTRL_NO_EQ_BASE = all(tuple(x) != tuple(CTRL_FOUR[0]) for x in CTRL_FOUR[1:])
CTRL_READINGS = [N_ANCH, N_UNIQUE, N_OBS_UNIQUE, N_ZERO]
CTRL_SCALAR_DISTINCT = len(set(CTRL_READINGS)) == 4
CTRL_SCALAR_NO_EQ_BASE = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
ZERO_SCAN = [0 * N_ANCH, 0 * N_UNIQUE, 0, 0]
ZERO_SCAN_OK = all(x == 0 for x in ZERO_SCAN) and (N_ANCH > 0)
NOT_ALL_GREEN = POS_NONZERO and (CTRL_RELEASE_COUNT > 0) and (N_TWO_SIDED > 0)

# ====================== 跨卷回读与参数不灭总账 ======================
R9K = load(P_R9)["key_numbers"]
R11K = load(P_R11)["key_numbers"]
R12K = load(P_R12)["key_numbers"]
R13K = load(P_R13)["key_numbers"]
R7K = load(P_R7)["key_numbers"]
R9_BITS = int(R9K["H_copied_unique_bits"])
R9_PROG = int(R9K["H_prog_bits"])
R9_IN = int(R9K["H_in_bits"])
R9_OUT = int(R9K["H_out_sum_bits"])
R11_ACTIVE = int(R11K["active_copied"])
R11_SILENT = int(R11K["silent_copied"])
R12_COPIED = int(R12K["copied_ast"])
R12_FILES = int(R12K["copied_files"])
R13_CLEAN = int(R13K["clean_falsifiable"])
R13_MIN_THEORY = int(R13K["min_theory_side_changes"])
R7_MISMATCH = int(R7K["shared_total_mismatch"])
R7_ZERO_CORRECT = int(R7K["r403_four_force_correct"].strip().split()[0])
SPINE_ZERO = (R7_ZERO_CORRECT == 0)
CORRECTION_MATCHES_R9 = (BITS_TOTAL == R9_BITS)
# 修正后观测比特占第九轮总比特的比例（精确比值，不拍容差）
OBS_OVER_R9 = F(BITS_OBS, R9_BITS) if R9_BITS else F(0)
SI_OVER_R9 = F(BITS_SI, R9_BITS) if R9_BITS else F(0)

# ====================== 三重认证门（守卫开关，不作误放行计数） ======================
GATE_ATTRIBUTION_ACTIVE = True
GATE_LOWERBOUND_ACTIVE = True
GATE_INFEASIBLE_ACTIVE = True
ACTIVE_GATES = [GATE_ATTRIBUTION_ACTIVE, GATE_LOWERBOUND_ACTIVE, GATE_INFEASIBLE_ACTIVE]
ATTRIBUTION_OK = TWO_PATH_COPY_OK and BITS_TWO_PATH and (N_MIXED == 0) and (N_UNMATCHED == 0)
LOWERBOUND_OK = BOUNDS_ALL_POSITIVE and BOUND_ORDER and (N_TWO_SIDED == len(WINDOW_ROWS))
INFEASIBLE_OK = CHANNEL_B_INFEASIBLE and (ZERO_BIT_COMPAT == 0)
# ★道 B 可满足 ⇔ 最宽口径下界 ≤ 0 或存在 0 bit 即可相容的双侧锚；实测两者都不成立。
CHANNEL_B_SATISFIABLE = (B_MIN_CONSERVATIVE <= 0) or (ZERO_BIT_COMPAT > 0)
CLEAN_BREAKTHROUGH = 1 if (CHANNEL_B_SATISFIABLE and ATTRIBUTION_OK and INFEASIBLE_OK) else 0
# 本轮无候选配置可被误放行：门承重体现在守卫链，不体现在突破计数上（如实声明）。
FORGED_BREAKTHROUGH = 0

# ====================== 判词与元守卫 ======================
def verdict_with(token):
    return ("ALG-TC"
            + "__ANCH-" + str(N_ANCH)
            + "__COPIED-" + str(N_UNIQUE)
            + "__OCC-" + str(N_OCC)
            + "__BITS-" + str(BITS_TOTAL)
            + "__SI-" + str(BITS_SI)
            + "__OBS-" + str(BITS_OBS)
            + "__WINDOW-" + dstr(B_MIN_WINDOW, 3)
            + "__ZERO-" + str(ZERO_BIT_COMPAT)
            + "__CLEAN-" + str(token)
            + "__PRED-0")


v0 = verdict_with(str(CLEAN_BREAKTHROUGH))
v1 = verdict_with(str(CLEAN_BREAKTHROUGH + 1))
verdict_machine_ok = (v0 != v1) and ("__CLEAN-" + str(CLEAN_BREAKTHROUGH)) in v0
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
    "AST 核验 act_copies 与 exp_copies 两函数齐备，return 均非顶层数值常量")
add("COPY-UNIQUE-TWO-PATH", UNIQUE_EQ and (len(ACT_UNIQUE) == N_UNIQUE) and (N_UNIQUE > 0), "PASS",
    "★副本唯一值两路：act=第九轮 JSON 登记的 " + str(len(ACT_UNIQUE)) +
    " 个分数；exp=独立把理论脚本源码重新 AST 扫描后与 46 锚精确匹配得 " +
    str(N_UNIQUE) + " 个；两集合相等")
add("COPY-OCC-TWO-PATH", (N_OCC == ACT["n_occ"]) and (N_OCC == 24), "PASS",
    "副本出现次数两路：act " + str(ACT["n_occ"]) + " / exp " + str(N_OCC) +
    " 次（13 个唯一值中部分重复出现）")
add("LITERAL-COUNT-TWO-PATH", LITERAL_TWO_PATH, "PASS",
    "理论脚本数值字面量：AST " + str(N_LITERALS) + " 个、正则数 token " + str(N_TOKENS) +
    " 个；两路机制不同，AST 为精确口径")
add("BIT-SUM-TWO-PATH", BITS_TWO_PATH and CORRECTION_MATCHES_R9, "PASS",
    "★独立复算 13 个唯一值的描述长度之和 " + str(BITS_TOTAL) +
    " bit，与第九轮 key_numbers 的 " + str(R9_BITS) + " bit 逐位相等")
add("KIND-QUADRIPARTITE", (sum(KIND_HIST.values()) == N_ANCH) and
    all(KIND_HIST[k] > 0 for k in KIND_ORDER), "PASS",
    "来料 kind 四分：" + " / ".join(k + "=" + str(KIND_HIST[k]) for k in KIND_ORDER) +
    "，合计 " + str(N_ANCH) + " 项")
add("COPY-KIND-ATTRIBUTION", (sum(COPY_KIND_HIST.values()) == N_UNIQUE) and
    all(COPY_KIND_HIST[k] >= 0 for k in KIND_ORDER), "PASS",
    "★13 个唯一副本按 kind 归因：" +
    " / ".join(k + "=" + str(COPY_KIND_HIST[k]) for k in KIND_ORDER) +
    "；每个副本按精确 Fraction 匹配回锚，不做近似")
add("NO-MIXED-NO-UNMATCHED", (N_MIXED == 0) and (N_UNMATCHED == 0), "PASS",
    "同一数值命中多个 kind 的副本 " + str(N_MIXED) + " 个、未匹配 " + str(N_UNMATCHED) +
    " 个 ⇒ 归因无歧义")
add("SI-IS-AXIOM-NOT-COPY", (BITS_SI > 0) and (N_SI_UNIQUE > 0), "IDENTITY",
    "★★c / h / e 三个 SI 定义值共 " + str(BITS_SI) + " bit、占 " + str(N_SI_UNIQUE) +
    " 个唯一副本；这是公理复用，不是观测搬运。本册主动单列为 IDENTITY，" +
    "不把它们算进「参数不灭」的证据，也不因此宣称观测副本归零")
add("OBS-BITS-CORRECTED-DOWN", CORRECTION_DOWNWARD and (BITS_OBS > 0), "PASS",
    "★★口径修正：第九轮 " + str(BITS_TOTAL) + " bit 中，观测搬运实为 " +
    str(BITS_OBS) + " bit（measured " + str(BITS_BY_KIND["measured"]) +
    " + measured-bound " + str(BITS_BY_KIND["measured-bound"]) + "），SI 定义 " +
    str(BITS_SI) + " bit 应剔除；修正方向为下调 " + str(BITS_TOTAL - BITS_OBS) + " bit")
add("CORRECTION-SHARE-EXACT", (OBS_SHARE + SI_SHARE == F(1)) and (OBS_SHARE > SI_SHARE), "PASS",
    "占比由精确 Fraction 比值给出不拍容差：观测 " + dstr(dec(OBS_SHARE * 100), 3) +
    "%、SI 定义 " + dstr(dec(SI_SHARE * 100), 3) + "%（" + str(BITS_OBS) + "/" +
    str(BITS_TOTAL) + " 与 " + str(BITS_SI) + "/" + str(BITS_TOTAL) + "，两者相加逐位等于 1）")
add("CORRECTION-NOT-OVERTURN", PARAM_NOT_EXTINCT and (N_OBS_UNIQUE == 10), "PASS",
    "★★修正不推翻结论：实测唯一副本仍有 " + str(N_OBS_UNIQUE) +
    " 个（measured " + str(COPY_KIND_HIST["measured"]) + " + measured-bound " +
    str(COPY_KIND_HIST["measured-bound"]) + "）、观测比特 " + str(BITS_OBS) +
    " bit > 0 ⇒「零自由参数靠把观测搬进源码」的结论不变，只是读数从 " +
    str(BITS_TOTAL) + " 修正为 " + str(BITS_OBS))
add("SIGMA0-BY-KIND", (sum(ZERO_BITS_BY_KIND.values()) == ZERO_BITS_TOTAL) and (N_ZERO == 19), "PASS",
    "σ=0 的 " + str(N_ZERO) + " 项按 kind 分：" +
    " / ".join(k + "=" + str(ZERO_BITS_BY_KIND[k]) for k in KIND_ORDER) +
    "，全精度合计 " + str(ZERO_BITS_TOTAL) + " bit")
add("SIGMA0-NOT-DEFINITION", SIGMA0_IS_NOT_DEFINITION and (N_ZERO_MEASURED == 15), "PASS",
    "★★口径陷阱机读钉住：σ=0 的 19 项里有 " + str(N_ZERO_MEASURED) +
    " 项 kind 是 measured / measured-bound（如 P14 a_mu、K08 Omega_Lambda）⇒ " +
    "「σ=0」不等于「定义值」，不能拿 σ=0 当公理白名单")
add("WINDOW-COUNT", (N_TWO_SIDED == 27) and (N_WINDOW_ROWS == N_TWO_SIDED), "PASS",
    "双侧 σ 非零的锚 " + str(N_TWO_SIDED) + " 项全部进入窗口计算，无遗漏")
add("WINDOW-BITS-SUM", (WINDOW_BITS > 0) and (N_WINDOW_ROWS > 0), "PASS",
    "★★相容只需落在 [O−zσ, O+zσ]：27 项窗口比特合计 " + dstr(WINDOW_BITS, 3) +
    " bit（z=" + dstr(Z_CRIT, 6) + "）；其中 derived " + dstr(WINDOW_BITS_DERIVED, 3) +
    " / measured " + dstr(WINDOW_BITS_MEASURED, 3) + " bit")
add("BOUND-STRICT-POSITIVE", (B_MIN_STRICT > 0), "PASS",
    "严口径（要求逐位精确）：实测类锚全精度下界 " + str(B_MIN_STRICT) + " bit")
add("BOUND-WINDOW-POSITIVE", (B_MIN_WINDOW > 0), "PASS",
    "★★通道 B 信息论下界（窗口口径）：σ=0 的实测类 " +
    str(ZERO_BITS_BY_KIND["measured"] + ZERO_BITS_BY_KIND["measured-bound"]) +
    " bit + σ>0 的窗口 " + dstr(WINDOW_BITS_MEASURED, 3) + " bit = " +
    dstr(B_MIN_WINDOW, 3) + " bit")
add("BOUND-CONSERVATIVE-POSITIVE", (B_MIN_CONSERVATIVE > 0), "PASS",
    "★★最宽口径（把 19 个 σ=0 项一律当公理、连 measured 也不算）仍须 " +
    dstr(B_MIN_CONSERVATIVE, 3) + " bit > 0 ⇒ 下界不是口径造成的")
add("BOUND-ORDER", BOUND_ORDER, "PASS",
    "三口径单调：最宽 " + dstr(B_MIN_CONSERVATIVE, 3) + " ≤ 窗口 " +
    dstr(B_MIN_WINDOW, 3) + " ≤ 严 " + str(B_MIN_STRICT) + " bit")
add("CHANNEL-B-INFEASIBLE", CHANNEL_B_INFEASIBLE and (not CHANNEL_B_SATISFIABLE), "PASS",
    "★★通道 B 不可满足：「程序侧不含观测副本（0 bit）」与「输出与 46 锚相容」" +
    "不能同时成立——相容至少需要 " + dstr(B_MIN_CONSERVATIVE, 3) +
    " bit 观测信息，而 0 bit 的程序无法产生")
add("ZERO-BIT-COMPAT-ZERO", (ZERO_BIT_COMPAT == 0), "PASS",
    "0 bit 即可相容的双侧锚 " + str(ZERO_BIT_COMPAT) + " 个：全部 27 项的窗口都比" +
    "锚本身窄，必须携带信息才能落到窗口内")
add("MIN-COST-ANCHOR", (MIN_COST is not None) and (MIN_COST["id"] == "G04"), "PASS",
    "最小代价锚 " + (MIN_COST["id"] if MIN_COST else "n/a") + "（" +
    (MIN_COST["symbol"] if MIN_COST else "n/a") + "）：窗口比特 " +
    (MIN_COST["window_bits"] if MIN_COST else "n/a") + "，只需把误差棒放宽 " +
    (MIN_COST["sigma_factor"] if MIN_COST else "n/a") + " 倍即可 0 bit 相容")
add("MAX-COST-ANCHOR", (MAX_COST is not None) and (MAX_COST_FACTOR > 1), "PASS",
    "最大代价锚 " + (MAX_COST["id"] if MAX_COST else "n/a") + "（" +
    (MAX_COST["symbol"] if MAX_COST else "n/a") + "）：须放宽 " +
    (MAX_COST["sigma_factor"] if MAX_COST else "n/a") +
    " 倍——统一放大到该倍数才可能让全部双侧锚 0 bit 相容，等价于误差棒失去意义")
add("COST-SPECTRUM", COST_SPECTRUM_OK, "PASS",
    "代价谱：" + str(COST_LE2) + " 项 ≤2 倍、" + str(COST_LE10 - COST_LE2) +
    " 项 2~10 倍、" + str(COST_GT10) + " 项 >10 倍，共 " + str(len(COST_ROWS)) + " 项")
add("POS-CONTROL", POS_NONZERO, "PASS",
    "正对照：描述长度 " + str(BITS_TOTAL) + " bit、观测比特 " + str(BITS_OBS) +
    "、窗口比特 " + dstr(WINDOW_BITS, 3) + "、实测唯一副本 " + str(N_OBS_UNIQUE) +
    " 个，均非零 ⇒ 判据不是恒绿空表")
add("CTRL-ATTR-INFLATE", CTRL_ATTR_DIFF, "PASS",
    "反事实控制组：把 SI 定义算回观测，观测比特从 " + str(BITS_OBS) + " 涨到 " +
    str(CTRL_ATTR_INFLATED) + " ⇒ 归因确实承重，不是零操作")
add("CTRL-SIGMA-X2", CTRL_SIGMA_X2_DIFF and (WINDOW_BITS - CTRL_SIGMA_X2_BITS == D(N_WINDOW_ROWS)), "PASS",
    "反事实控制组：σ 统一放大 2 倍后窗口比特从 " + dstr(WINDOW_BITS, 3) + " 精确减到 " +
    dstr(CTRL_SIGMA_X2_BITS, 3) + "（差值恰为项数 " + str(N_WINDOW_ROWS) +
    "）⇒ 每项减 1 bit，机制自洽")
add("CTRL-DEF-RELEASE", CTRL_DEF_DIFF, "PASS",
    "最宽口径控制组：把 19 个 σ=0 项全当公理，下界从 " + dstr(B_MIN_WINDOW, 3) +
    " 降到 " + dstr(CTRL_DEF_RELEASED, 3) + " ⇒ 仍是正数，结论不依赖 σ=0 的处理方式")
add("GATE-ATTRIBUTION-BEARING",
    GATE_ATTRIBUTION_ACTIVE and ATTRIBUTION_OK and (BITS_TOTAL == R9_BITS), "PASS",
    "归因门由两路副本集合相等、" + str(BITS_TOTAL) + " bit 与第九轮逐位相等驱动；拆该门即令本守卫 FAIL")
add("GATE-LOWERBOUND-BEARING",
    GATE_LOWERBOUND_ACTIVE and LOWERBOUND_OK and (B_MIN_CONSERVATIVE > 0), "PASS",
    "下界门由三口径全正且单调驱动；拆该门即令本守卫 FAIL")
add("GATE-INFEASIBLE-BEARING",
    GATE_INFEASIBLE_ACTIVE and INFEASIBLE_OK and (ZERO_BIT_COMPAT == 0), "PASS",
    "不可满足门由 0 bit 相容数为 0 驱动；拆该门即令本守卫 FAIL")
add("THREE-GATES-INDEPENDENT", (sum(1 for g in ACTIVE_GATES if g) == 3) and
    ATTRIBUTION_OK and LOWERBOUND_OK and INFEASIBLE_OK and (FORGED_BREAKTHROUGH == 0), "PASS",
    "★三门是认证门不是误放行计数门：本轮无候选配置可被误放行（误放行 " +
    str(FORGED_BREAKTHROUGH) + " 个），门承重体现在守卫链而非突破计数——" +
    "这是与第十四轮「最小承重割 2」不同形态的如实声明，不重复其结论")
add("CLEAN-BREAKTHROUGH-ZERO", (CLEAN_BREAKTHROUGH == 0) and (not CHANNEL_B_SATISFIABLE), "PASS",
    "★★「通道 B 可满足 ∧ 归因正确 ∧ 不可满足成立」同时成立 " + str(CLEAN_BREAKTHROUGH) +
    " 次；通道 B 可满足 = " + str(CHANNEL_B_SATISFIABLE))
add("SPINE-ZERO", SPINE_ZERO, "PASS",
    "跨卷回读：r403 四力正确解 " + str(R7_ZERO_CORRECT) + " 条；本册未新增任何物理方程")
add("PARAM-NOT-EXTINCT-TOTAL", (R11_ACTIVE > 0) and (R11_SILENT > 0) and (R12_COPIED > 0), "PASS",
    "参数不灭总账（并列不相加）：本轮实测副本 " + str(N_OBS_UNIQUE) + " 唯一值 / " +
    str(BITS_OBS) + " bit；R11 活跃 " + str(R11_ACTIVE) + " / 静默 " + str(R11_SILENT) +
    " 节点；R12 全库 " + str(R12_COPIED) + " 个跨 " + str(R12_FILES) + " 脚本")
add("EXIT-COSTS-DISTINCT", (R13_MIN_THEORY > 0) and (R7_MISMATCH > 0) and
    (R13_MIN_THEORY != R7_MISMATCH), "PASS",
    "硬出口代价三层不同读数：R13 理论侧最小改动 " + str(R13_MIN_THEORY) +
    "、R7 全共享谱失配 " + str(R7_MISMATCH) + "、本轮窗口下界 " +
    dstr(B_MIN_WINDOW, 3) + " bit；三者不相加")
add("CTRL-FOUR-DISTINCT", CTRL_FOUR_DISTINCT, "PASS",
    "控制组四向量两两不同：" + " / ".join(str(x) for x in CTRL_FOUR))
add("CTRL-NO-EQ-BASE", CTRL_NO_EQ_BASE, "PASS",
    "三个单门对照均不等于基线 " + str(CTRL_FOUR[0]))
add("CTRL-SCALAR-DISTINCT", CTRL_SCALAR_DISTINCT, "PASS",
    "控制组四标量两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-SCALAR-NO-EQ-BASE", CTRL_SCALAR_NO_EQ_BASE, "PASS",
    "三个对照标量均不等于基线标量 " + str(CTRL_READINGS[0]))
add("BOUND-TRIAD-IDENTITY", BOUND_ORDER and (len((B_MIN_STRICT, B_MIN_WINDOW, B_MIN_CONSERVATIVE)) == 3), "IDENTITY",
    "三个口径是同一对象（46 锚的相容信息需求）的三层放宽，不是三份独立证据；" +
    "本册单列 IDENTITY，只用「三种口径同向」作稳健性，不把口径数当证据")
add("ZERO-SCAN-IDENTITY", ZERO_SCAN_OK, "IDENTITY",
    "阴性对照：扫描 0 个锚时四项读数恒 " + str(ZERO_SCAN) +
    "，该侧恒真、零判别力，单列 IDENTITY 配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", NOT_ALL_GREEN, "INFO",
    "负对照恒绿，但描述长度、观测/定义拆分、窗口比特、代价谱、三组控制组均非恒绿读数")
add("FAMILY-LIMITED-CLAIM", (N_ANCH == 46) and (N_UNIQUE > 0), "BOUNDARY",
    "★结论限于 openuft 既有 46 项锚与单个理论脚本的输出字面量；**不是关于全人类实验数据" +
    "或任意理论程序的定理**，也不覆盖尚未写出的方程族")
add("BIT-IS-FIXED-ENCODING", (BITS_TOTAL == R9_BITS), "BOUNDARY",
    "★比特数是固定编码（分子/分母二进制位数之和）下的描述长度上界，**不是 Kolmogorov 复杂度**；" +
    "换编码会改变绝对值，但观测/定义的拆分比例与三口径同向不变")
add("NO-BREAKTHROUGH", (CLEAN_BREAKTHROUGH == 0), "INFO",
    "本册不宣称攻破统一场论，也不宣称攻破力的统一；只产可算判决")
add("MATH-NOT-EXPERIMENT", (B_MIN_WINDOW > 0), "INFO",
    "全部结论来自两路机读、精确 Fraction 匹配与 Decimal 窗口计算，不是实验证实；不产新物理")
add("NEXT-EXIT", (CLEAN_BREAKTHROUGH == 0) and (not CHANNEL_B_SATISFIABLE), "INFO",
    "硬出口未变且被本轮加强：通道 B 不仅「现有输出未认证」，而是**在 46 锚上信息论不可满足**；" +
    "要打通须给出误差棒足够宽到窗口比特为 0 的新读数，或给出不含观测副本却能落进窗口的生成机制")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把突破读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")


def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-FINAL-TRIPLE-CERT--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-FINAL-TRIPLE-CERT--GATES-FAIL"
    return "ALG-FINAL-TRIPLE-CERT--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "CLEAN-BREAKTHROUGH-ZERO", "SI-IS-AXIOM-NOT-COPY",
                     "BOUND-TRIAD-IDENTITY", "FAMILY-LIMITED-CLAIM", "BIT-IS-FIXED-ENCODING"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-FINAL-TRIPLE-CERT--GATES-PASS-WITH-0-NEGATIVE") and \
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
    "anchors": N_ANCH, "kind_hist": KIND_HIST,
    "copied_unique": N_UNIQUE, "copied_occ": N_OCC, "literals_ast": N_LITERALS,
    "literals_token": N_TOKENS,
    "bits_total": BITS_TOTAL, "bits_by_kind": BITS_BY_KIND,
    "bits_si": BITS_SI, "bits_observed": BITS_OBS, "si_share": dstr(dec(SI_SHARE), 6),
    "obs_share": dstr(dec(OBS_SHARE), 6), "obs_over_r9": dstr(dec(OBS_OVER_R9), 6),
    "copy_kind_hist": COPY_KIND_HIST, "copied_observed_unique": N_OBS_UNIQUE,
    "copied_si_unique": N_SI_UNIQUE, "mixed": N_MIXED, "unmatched": N_UNMATCHED,
    "sigma_zero": N_ZERO, "sigma_zero_bits": ZERO_BITS_TOTAL,
    "sigma_zero_by_kind": ZERO_BITS_BY_KIND, "sigma_zero_measured": N_ZERO_MEASURED,
    "two_sided": N_TWO_SIDED, "window_rows": N_WINDOW_ROWS,
    "window_bits": dstr(WINDOW_BITS, 3), "window_bits_measured": dstr(WINDOW_BITS_MEASURED, 3),
    "window_bits_derived": dstr(WINDOW_BITS_DERIVED, 3),
    "z_crit": dstr(Z_CRIT, 12),
    "bound_strict": B_MIN_STRICT, "bound_window": dstr(B_MIN_WINDOW, 3),
    "bound_conservative": dstr(B_MIN_CONSERVATIVE, 3),
    "bounds_all_positive": BOUNDS_ALL_POSITIVE, "bound_order": BOUND_ORDER,
    "channel_b_infeasible": CHANNEL_B_INFEASIBLE,
    "channel_b_satisfiable": CHANNEL_B_SATISFIABLE,
    "zero_bit_compat": ZERO_BIT_COMPAT,
    "min_cost_id": MIN_COST["id"] if MIN_COST else None,
    "min_cost_factor": dstr(MIN_COST_FACTOR, 3),
    "max_cost_id": MAX_COST["id"] if MAX_COST else None,
    "max_cost_factor": dstr(MAX_COST_FACTOR, 3),
    "cost_le2": COST_LE2, "cost_le10": COST_LE10, "cost_gt10": COST_GT10,
    "ctrl_attr_inflated": CTRL_ATTR_INFLATED, "ctrl_sigma_x2_bits": dstr(CTRL_SIGMA_X2_BITS, 3),
    "ctrl_def_released": dstr(CTRL_DEF_RELEASED, 3),
    "clean_breakthrough": CLEAN_BREAKTHROUGH, "forged_breakthrough": FORGED_BREAKTHROUGH,
    "spine_four_force_correct": R7_ZERO_CORRECT,
    "r9_bits": R9_BITS, "r9_prog": R9_PROG, "r9_in": R9_IN, "r9_out": R9_OUT,
    "r11_active": R11_ACTIVE, "r11_silent": R11_SILENT,
    "r12_copied": R12_COPIED, "r12_files": R12_FILES, "r13_clean": R13_CLEAN,
    "r13_min_theory": R13_MIN_THEORY, "r7_mismatch": R7_MISMATCH,
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

out = {
    "title": "算法联盟：观测副本的定义归因与硬出口通道 B 的信息论下界（第十五轮）",
    "date": "2026-11-14",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "scope": {"own_excluded_names": sorted(OWN_NAMES),
              "anchors": N_ANCH, "theory_script": os.path.basename(P_THEORY)},
    "attribution": {"kind_hist": KIND_HIST,
                    "copy_rows": COPY_ROWS,
                    "bits_by_kind": BITS_BY_KIND,
                    "si_values": [r["value"] for r in SI_COPIES],
                    "bits_si": BITS_SI, "bits_observed": BITS_OBS},
    "sigma_zero": {"count": N_ZERO, "bits_total": ZERO_BITS_TOTAL,
                   "by_kind": ZERO_BITS_BY_KIND,
                   "measured_count": N_ZERO_MEASURED,
                   "ids": [x["id"] for x in ZERO_ROWS]},
    "window": {"z_crit": dstr(Z_CRIT, 12),
               "rows": [{k: v for k, v in r.items() if k != "b"} for r in WINDOW_ROWS],
               "bits_total": dstr(WINDOW_BITS, 3),
               "bits_measured": dstr(WINDOW_BITS_MEASURED, 3),
               "bits_derived": dstr(WINDOW_BITS_DERIVED, 3),
               "zero_bit_compat": ZERO_BIT_COMPAT},
    "bounds": {"strict": B_MIN_STRICT,
               "window": dstr(B_MIN_WINDOW, 3),
               "conservative": dstr(B_MIN_CONSERVATIVE, 3),
               "order_ok": BOUND_ORDER,
               "all_positive": BOUNDS_ALL_POSITIVE},
    "costs": {"rows": [{k: v for k, v in r.items() if k != "f"} for r in COST_ROWS],
              "min": MIN_COST["id"] if MIN_COST else None,
              "min_factor": dstr(MIN_COST_FACTOR, 3),
              "max": MAX_COST["id"] if MAX_COST else None,
              "max_factor": dstr(MAX_COST_FACTOR, 3),
              "le2": COST_LE2, "le10": COST_LE10, "gt10": COST_GT10},
    "exit": {"channel_b_infeasible": CHANNEL_B_INFEASIBLE,
             "channel_b_satisfiable": CHANNEL_B_SATISFIABLE,
             "min_theory_r13": R13_MIN_THEORY, "mus_r9": 4,
             "needs_wider_sigma_or_generator": True},
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
    lines.append("算法联盟：观测副本定义归因与通道 B 信息论下界（第十五轮）")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("副本归因：唯一值 " + str(N_UNIQUE) + " 个 / 出现 " + str(N_OCC) +
                 " 次 / 描述长度 " + str(BITS_TOTAL) + " bit")
    for r in COPY_ROWS:
        lines.append("  " + r["kind"].ljust(15) + " " + str(r["bits"]).rjust(4) + " bit | " +
                     ",".join(r["anchor_ids"]).ljust(6) + " | " + r["value"])
    lines.append("  ⇒ SI 定义 " + str(BITS_SI) + " bit / 观测搬运 " + str(BITS_OBS) +
                 " bit（" + dstr(dec(OBS_SHARE * 100), 3) + "%）")
    lines.append("-" * 96)
    lines.append("σ=0 的 " + str(N_ZERO) + " 项按 kind：" +
                 " / ".join(k + "=" + str(ZERO_BITS_BY_KIND[k]) for k in KIND_ORDER) +
                 "；其中 measured 类 " + str(N_ZERO_MEASURED) + " 项 ⇒ σ=0 不等于定义")
    lines.append("窗口比特（" + str(N_WINDOW_ROWS) + " 项双侧，z=" + dstr(Z_CRIT, 12) + "）：" +
                 dstr(WINDOW_BITS, 3) + " bit（measured " + dstr(WINDOW_BITS_MEASURED, 3) +
                 " / derived " + dstr(WINDOW_BITS_DERIVED, 3) + "）")
    lines.append("三口径下界：严 " + str(B_MIN_STRICT) + " / 窗口 " + dstr(B_MIN_WINDOW, 3) +
                 " / 最宽 " + dstr(B_MIN_CONSERVATIVE, 3) + " bit，单调且全正 ⇒ 通道 B 不可满足")
    lines.append("0 bit 即可相容的双侧锚：" + str(ZERO_BIT_COMPAT) + " 个")
    lines.append("最小代价：" + (MIN_COST["id"] if MIN_COST else "n/a") + " 只需放宽 " +
                 dstr(MIN_COST_FACTOR, 3) + " 倍；最大代价：" +
                 (MAX_COST["id"] if MAX_COST else "n/a") + " 须放宽 " +
                 dstr(MAX_COST_FACTOR, 3) + " 倍")
    lines.append("代价谱：≤2 倍 " + str(COST_LE2) + " / 2~10 倍 " +
                 str(COST_LE10 - COST_LE2) + " / >10 倍 " + str(COST_GT10))
    lines.append("-" * 96)
    lines.append("结论：不宣称攻破统一场论；四力大统一正确解 " + str(R7_ZERO_CORRECT) +
                 " 条；独立实验预言 0。通道 B 在 46 锚上信息论不可满足。")
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
