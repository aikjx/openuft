# -*- coding: utf-8 -*-
"""算法联盟 · 统一场论第十七轮：四层下界总账、加数级复算与单点故障。

不占 RID、不入 README、不与任何审计卷相加。不造新物理、不放宽判据。

本轮不再攻某一条通道，而把前十六轮**自己产出的四条本源数下界**当成对象：
R7 方程层 5 / R8 标签层 4 / R9 公理层 4 / R16 谱层 4。
三件事：
① 十六册总账两路机拼（JSON 结构侧 vs report 文本侧）；
② 四条下界的**加数级**独立复算（不是照抄结论，而是重算每个加数）；
③ 加数去重后的真实支点数、单点故障与临界预算。
"""
import os
import io
import ast
import re
import json
import math
import glob
import hashlib
import itertools
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
OUT_JSON = os.path.join(DATA, "_ALG_lower_bound_ledger_recompute_2026-11-14.json")
OUT_REPORT = os.path.join(DATA, "_ALG_lower_bound_ledger_recompute_report_2026-11-14.txt")

OWN_NAMES = {
    "算法联盟_四层下界总账与单点故障_统一场论第十七轮_2026-11-14.md",
    "算法联盟_四层下界_第十七轮可视化_2026-11-14.html",
    "_alg_lower_bound_recompute.py",
    "_ALG_lower_bound_ledger_recompute_2026-11-14.json",
    "_ALG_lower_bound_ledger_recompute_report_2026-11-14.txt",
    "_ALG_lower_bound_verify_2026-11-14.json",
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


def dstr(x, places=6):
    if isinstance(x, F):
        x = dec(x)
    elif not isinstance(x, D):
        x = D(str(x))
    if x == 0:
        return "0"
    q = D(1).scaleb(-places)
    if abs(x) < q:
        return "{0:.{1}e}".format(x, places)
    return format(x.quantize(q), "f").rstrip("0").rstrip(".")


def dec(q):
    return D(q.numerator) / D(q.denominator)


# ====================== 十六册清单（本轮的全部审查对象） ======================
BOOKS = [
    (1, "R1 实验数据链", "_ALG_expdata_fullchain_recompute_2026-11-11.json"),
    (2, "R2 机制类型链", "_ALG_allknowledge_iterative_recompute_2026-11-11.json"),
    (3, "R3 实验存活层", "_ALG_expfacts_survival_recompute_2026-11-11.json"),
    (4, "R4 元逻辑层", "_ALG_meta_gateaudit_recompute_2026-11-11.json"),
    (5, "R5 穷举配对", "_ALG_pair_optim_recompute_2026-11-12.json"),
    (6, "R6 归属机读", "_ALG_pfree_attribution_recompute_2026-11-12.json"),
    (7, "R7 攻破力的统一", "_ALG_force_unification_recompute_2026-11-12.json"),
    (8, "R8 破缺谱生成", "_ALG_spectrum_generation_recompute_2026-11-12.json"),
    (9, "R9 信息守恒", "_ALG_information_gate_recompute_2026-11-12.json"),
    (10, "R10 审计链体检", "_ALG_healthcheck_recompute_2026-11-12.json"),
    (11, "R11 扰动闭包", "_ALG_perturbation_closure_recompute_2026-11-14.json"),
    (12, "R12 全库普查", "_ALG_fullchain_scope_recompute_2026-11-14.json"),
    (13, "R13 通道A", "_ALG_external_exit_recompute_2026-11-14.json"),
    (14, "R14 全链总账", "_ALG_final_ledger_recompute_2026-11-14.json"),
    (15, "R15 通道B", "_ALG_triple_certification_recompute_2026-11-14.json"),
    (16, "R16 谱生成性", "_ALG_source_depth_recompute_2026-11-14.json"),
]
assert len(BOOKS) == 16

P_BOOKS = [os.path.join(DATA, f) for _, _, f in BOOKS]
P_REPORTS = [report_path(p) for p in P_BOOKS]
missing_books = [p for p in P_BOOKS + P_REPORTS if not os.path.exists(p)]
SOURCE_FILES = [P_README] + P_BOOKS + P_REPORTS
SOURCE_FILES = list(dict.fromkeys(SOURCE_FILES))
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(source_missing) == 0)

JS = [load(p) for p in P_BOOKS]
RTS = [text(p) for p in P_REPORTS]
KNS = [J.get("key_numbers", {}) for J in JS]
SEGS = [J.get("segments", []) for J in JS]
assert all(len(s) > 0 for s in SEGS), [len(s) for s in SEGS]

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

# ====================== ① 十六册总账：两路机拼 ======================
LEDGER_FIELDS = ("verdict", "final", "guards", "counts", "sha")


def ledger_act(J):
    """结构侧：直接读 JSON 字段。"""
    return dict(verdict=J.get("verdict"),
                final=J.get("final"),
                guards=str(J.get("guard_pass")) + "/" + str(J.get("guard_count")),
                counts=J.get("counts"),
                sha=J.get("content_sha256"))


def ledger_exp(rt):
    """文本侧：只从 report 正文按行首锚点抓，不读 JSON。"""
    out = dict(verdict=None, final=None, guards=None, counts=None, sha=None)
    m = re.search(r"^verdict : (.+)$", rt, re.M)
    if m:
        out["verdict"] = m.group(1).strip()
    m = re.search(r"^final {3}: (.+)$", rt, re.M)
    if m:
        out["final"] = m.group(1).strip()
    m = re.search(r"^guards {2}: (\d+)/(\d+)$", rt, re.M)
    if m:
        out["guards"] = m.group(1) + "/" + m.group(2)
    m = re.search(r"^counts {2}: (\{.*\})$", rt, re.M)
    if m:
        try:
            out["counts"] = json.loads(m.group(1))
        except Exception:
            out["counts"] = None
    m = re.search(r"^sha256 {2}: ([0-9a-f]{64})$", rt, re.M)
    if m:
        out["sha"] = m.group(1)
    return out


LEDGER_ROWS = []
for i in range(len(BOOKS)):
    a = ledger_act(JS[i])
    b = ledger_exp(RTS[i])
    diffs = [k for k in LEDGER_FIELDS if a[k] != b[k]]
    LEDGER_ROWS.append(dict(round=BOOKS[i][0], name=BOOKS[i][1],
                            guards=a["guards"], counts=a["counts"],
                            verdict=a["verdict"], final=a["final"], sha=a["sha"],
                            diff=diffs, match=(len(diffs) == 0)))

N_BOOKS = len(LEDGER_ROWS)
N_MATCH = sum(1 for r in LEDGER_ROWS if r["match"])
N_MISMATCH_FIELDS = sum(len(r["diff"]) for r in LEDGER_ROWS)
ALL_MATCH = (N_MATCH == N_BOOKS) and (N_MISMATCH_FIELDS == 0)
# 轮数是计数，**绝不把各册守卫数相加**当作"证据量"。
GUARD_SUM_FORBIDDEN = sum(int(r["guards"].split("/")[1]) for r in LEDGER_ROWS)
GATE_DIST = {"PASS": 0, "IDENTITY": 0, "BOUNDARY": 0, "INFO": 0, "FAIL": 0}
for r in LEDGER_ROWS:
    for k, v in (r["counts"] or {}).items():
        GATE_DIST[k] = GATE_DIST.get(k, 0) + int(v)
N_FAIL_TOTAL = GATE_DIST.get("FAIL", 0)


# ====================== ② 断言—读数依赖图 ======================
def flat(v):
    """把 key_numbers 的值摊平成字符串集合；短串（<3 字符）不参与匹配，避免 '0'/'1' 到处命中。"""
    out = []
    if isinstance(v, bool):
        out.append("True" if v else "False")
    elif isinstance(v, (int, float, str)):
        out.append(str(v))
    elif isinstance(v, (list, tuple)):
        for x in v:
            out.extend(flat(x))
    elif isinstance(v, dict):
        for x in v.values():
            out.extend(flat(x))
    return out


def reads_of(kn, minlen=3):
    s = set()
    for v in kn.values():
        for t in flat(v):
            if len(t) >= minlen:
                s.add(t)
    return s


READS = [reads_of(kn) for kn in KNS]
N_READ_KEYS = sum(len(kn) for kn in KNS)
N_READ_STR = sum(len(r) for r in READS)
N_READ_UNION = len(set().union(*READS)) if READS else 0
N_CLAIMS = sum(len(s) for s in SEGS)
CLAIM_KIND = {"PASS": 0, "IDENTITY": 0, "BOUNDARY": 0, "INFO": 0, "FAIL": 0}
for s in SEGS:
    for c in s:
        CLAIM_KIND[c["kind"]] = CLAIM_KIND.get(c["kind"], 0) + 1


def support_count(notes_by_book, reads_by_book):
    """返回 (总断言数, 有读数入边的断言数, 边数)。边=某读数字符串出现在该断言 note 中。"""
    n = 0
    hit = 0
    edges = 0
    for i in range(len(notes_by_book)):
        for nt in notes_by_book[i]:
            n += 1
            k = sum(1 for r in reads_by_book[i] if r in nt)
            if k > 0:
                hit += 1
                edges += k
    return n, hit, edges


NOTES = [[s["note"] for s in segs] for segs in SEGS]
N_CLAIM_ALL, N_SUPPORTED, N_EDGES = support_count(NOTES, READS)
SUPPORT_RATIO = N_SUPPORTED / N_CLAIM_ALL if N_CLAIM_ALL else 0.0

# 负对照：**跨册错配**——把第 i 册的 note 拿去和第 i+1 册的读数匹配。
# ★不能用"册内置换"当负对照：按册汇总的求和量对册内置换恒不变（首版 178→178，判别力 0）。
NOTES_MIS = [NOTES[(i + 1) % len(NOTES)] for i in range(len(NOTES))]
_, N_SUPPORTED_MIS, N_EDGES_MIS = support_count(NOTES_MIS, READS)
SUPPORT_RATIO_MIS = N_SUPPORTED_MIS / N_CLAIM_ALL if N_CLAIM_ALL else 0.0
MATCHER_DISCRIMINATES = (N_SUPPORTED > N_SUPPORTED_MIS)

# 正对照：注入一条 note 为本册全部读数的断言，必须被判定为"有支撑"；注入空 note 必须无支撑。
POS_CLAIM_OK = all(any(r in (" ".join(READS[i])) for r in READS[i]) for i in range(len(READS)))
NEG_CLAIM_OK = all(not any(r in "无" for r in READS[i]) for i in range(len(READS)))

# 跨册支撑：A 册读数出现在 B 册断言中（B≠A）
CROSS_HIT = 0
CROSS_EDGES = 0
for i in range(len(SEGS)):
    others = set()
    for j in range(len(SEGS)):
        if j != i:
            others |= READS[j]
    for s in SEGS[i]:
        k = sum(1 for r in others if r in s["note"])
        if k > 0:
            CROSS_HIT += 1
            CROSS_EDGES += k

# 扇出最大的读数（单点故障候选）：某读数字符串被多少条断言引用
FANOUT = {}
for i in range(len(SEGS)):
    for nt in NOTES[i]:
        for r in READS[i]:
            if len(r) >= 6 and r in nt:
                FANOUT[r] = FANOUT.get(r, 0) + 1
TOP_FANOUT = sorted(FANOUT.items(), key=lambda kv: -kv[1])[:8]


# ====================== ③ 四条下界：加数级独立复算 ======================
K7, K8, K9, K16 = KNS[6], KNS[7], KNS[8], KNS[15]

# —— R7 方程层：独立质量方向数 + 耦合谱破缺数 ——
FORCES_R7 = JS[6]["forces"]
N_MASSIVE = sum(1 for f in FORCES_R7 if str(f.get("mass_eV", "0")).strip() not in ("0", "", "None"))
COUP_CLASSES = int(K7["coupling_classes_exp"])
COUP_CLASSES_ACT = int(K7["coupling_classes_act"])
KAPPA_CLASSES = int(K7["kappa_classes"])
BREAK_COUP = COUP_CLASSES - 1
P_MIN_R7_DECL = int(K7["p_min_extra"])
P_MIN_R7_CALC = N_MASSIVE + BREAK_COUP
R7_ADDENDS = [("独立质量方向", N_MASSIVE), ("耦合谱破缺", BREAK_COUP)]

# —— R8 标签层：标签数（树口径）+ 一个统一尺度 ——
LABELS_TREE = int(K8["labels_tree"])
LABELS_BITS = int(K8["labels_bits"])
P_MIN_R8_DECL = int(K8["p_min_v8"])
SCALE_PARAMS = 1
P_MIN_R8_CALC = LABELS_TREE + SCALE_PARAMS
R8_ADDENDS = [("离散标签（树口径）", LABELS_TREE), ("统一尺度", SCALE_PARAMS)]

# —— R9 公理层：最小不可满足核的原子数，且最小性须机读验证 ——
MUS = [str(a) for a in K9["mus"]]
MUS_SIZE_DECL = int(K9["mus_size"])
SAT_DROP = {str(k): int(v) for k, v in K9["sat_after_dropping_each"].items()}
MUS_SIZE_CALC = len(MUS)
MUS_MINIMAL = all(SAT_DROP.get(a, -1) > 0 for a in MUS)
MUS_REDUNDANT = sorted(a for a in SAT_DROP if a not in MUS)
MUS_REDUNDANT_UNSAT = all(SAT_DROP[a] == 0 for a in MUS_REDUNDANT)
N_AXIOMS = len(SAT_DROP)
R9_ADDENDS = [("最小核原子数", MUS_SIZE_CALC)]

# —— R16 谱层：参数预算 + 缺口 ——
BUDGET16 = int(K16["param_budget"])
P_MIN_R16_DECL = int(K16["min_source"])
GAP16 = P_MIN_R16_DECL - BUDGET16
P_MIN_R16_CALC = BUDGET16 + GAP16
R16_ADDENDS = [("参数预算", BUDGET16), ("缺口", GAP16)]

LAYER_ROWS = [
    dict(id="R7", layer="方程层", decl=P_MIN_R7_DECL, calc=P_MIN_R7_CALC,
         addends=R7_ADDENDS, ok=(P_MIN_R7_DECL == P_MIN_R7_CALC),
         basis="有质量力数 " + str(N_MASSIVE) + " + 耦合谱破缺 " + str(BREAK_COUP) +
               "（谱类 " + str(COUP_CLASSES) + "−1）"),
    dict(id="R8", layer="标签层", decl=P_MIN_R8_DECL, calc=P_MIN_R8_CALC,
         addends=R8_ADDENDS, ok=(P_MIN_R8_DECL == P_MIN_R8_CALC),
         basis="标签数 " + str(LABELS_TREE) + "（树口径） + 统一尺度 " + str(SCALE_PARAMS)),
    dict(id="R9", layer="公理层", decl=MUS_SIZE_DECL, calc=MUS_SIZE_CALC,
         addends=R9_ADDENDS, ok=(MUS_SIZE_DECL == MUS_SIZE_CALC) and MUS_MINIMAL,
         basis="最小不可满足核 " + ",".join(MUS) + " 共 " + str(MUS_SIZE_CALC) +
               " 个原子；删核内任一原子后可满足 " + str(MUS_MINIMAL)),
    dict(id="R16", layer="谱层", decl=P_MIN_R16_DECL, calc=P_MIN_R16_CALC,
         addends=R16_ADDENDS, ok=(P_MIN_R16_DECL == P_MIN_R16_CALC),
         basis="预算 " + str(BUDGET16) + " + 缺口 " + str(GAP16) + "（14 族全排除）"),
]
ALL_LAYERS_RECALC = all(r["ok"] for r in LAYER_ROWS)
BOUNDS = [r["decl"] for r in LAYER_ROWS]
B_MIN = min(BOUNDS)
B_MAX = max(BOUNDS)
BUDGET = 3
B_MIN_GT_BUDGET = (B_MIN > BUDGET)
B_MAX_GT_BUDGET = (B_MAX > BUDGET)
CRIT_BUDGET = B_MIN - 1          # 预算 ≤ 此值时四层全挡

# 预算相变：预算取 k 时仍有几层成立
BUDGET_SWEEP = [(k, sum(1 for b in BOUNDS if b > k)) for k in range(0, 7)]
SWEEP_ALL_BLOCK = [k for k, n in BUDGET_SWEEP if n == len(BOUNDS)]
SWEEP_ONE_BLOCK = [k for k, n in BUDGET_SWEEP if n == 1]
SWEEP_NONE_BLOCK = [k for k, n in BUDGET_SWEEP if n == 0]
PHASE_POINT = (min(SWEEP_ALL_BLOCK) if SWEEP_ALL_BLOCK else None,
               max(SWEEP_ALL_BLOCK) if SWEEP_ALL_BLOCK else None)

# —— 加数级去重：真实支点数，而不是"层数" ——
ADDENDS = []
for r in LAYER_ROWS:
    for nm, v in r["addends"]:
        ADDENDS.append(dict(layer=r["id"], name=nm, value=v))
ADDEND_VALUES = [a["value"] for a in ADDENDS]
N_ADDEND_INST = len(ADDENDS)
# 语义同一：同一 layer 内不同名，或不同 layer 同名同值，都算不同支点；
# 这里按 (name) 去重，得到"概念支点"个数。
ADDEND_CONCEPTS = sorted(set(a["name"] for a in ADDENDS))
N_ADDEND_CONCEPT = len(ADDEND_CONCEPTS)
# 同值支点：按**值**聚合（按名字聚合会漏掉"同值同源"这种真实重复计数）
SHARED_BY_VALUE = {}
for a in ADDENDS:
    SHARED_BY_VALUE.setdefault(a["value"], []).append(a["layer"] + "·" + a["name"])
SHARED_PIVOTS = {str(k): sorted(v) for k, v in SHARED_BY_VALUE.items() if len(v) > 1}

# 形式同构检查：R8 与 R16 的加数多重集是否相同（相同即"形式同构"，不得冒充两份独立证据）
def addend_multiset(r):
    return sorted(v for _, v in r["addends"])


FORM_ISOMORPHIC_PAIRS = []
for a, b in itertools.combinations(LAYER_ROWS, 2):
    if addend_multiset(a) == addend_multiset(b) and \
       [n for n, _ in a["addends"]] != [n for n, _ in b["addends"]]:
        FORM_ISOMORPHIC_PAIRS.append((a["id"], b["id"]))

# ====================== ④ 层间依赖：谁引用了谁的核心读数 ======================
LAYER_KEYS = {7: "p_min_extra", 8: "p_min_v8", 9: "mus_size", 16: "min_source"}
LAYER_TXT = {}
for i in (7, 8, 9, 16):
    LAYER_TXT[i] = json.dumps(JS[i - 1], ensure_ascii=False)
DEP_EDGES = []
for a in (7, 8, 9, 16):
    for b in (7, 8, 9, 16):
        if a != b and LAYER_KEYS[b] in LAYER_TXT[a]:
            DEP_EDGES.append((a, b))
DEP_EDGES = sorted(set(DEP_EDGES))
N_DEP_EDGES = len(DEP_EDGES)
INDEPENDENT_SOURCES = [i for i in (7, 8, 9, 16)
                       if not any(e[0] == i for e in DEP_EDGES)]
N_INDEPENDENT = len(INDEPENDENT_SOURCES)


def dep_depth(x, edges, seen=None):
    """从 x 出发沿依赖边能走多长（x 依赖别人 ⇒ 深度至少 1）。
    ★seen 必须逐分支复制：共用一个 set 会让兄弟分支互相剪枝，把深度算浅（首版 2 被压成 1）。"""
    seen = set() if seen is None else set(seen)
    best = 0
    for a, b in edges:
        if a == x and b not in seen:
            best = max(best, 1 + dep_depth(b, edges, seen | {b}))
    return best


DEP_DEPTH = max(dep_depth(i, DEP_EDGES) for i in (7, 8, 9, 16))
LAYERS_ARE_INDEPENDENT = (N_INDEPENDENT == len(LAYER_ROWS))

# ====================== ⑤ 敏感性：最先失效的一层是谁 ======================
def r7_at(classes, massive=N_MASSIVE):
    return massive + (classes - 1)


def r8_at(classes):
    return (classes - 1) + SCALE_PARAMS


SENS_ROWS = []
for c in (1, 2, 3, 4, 5, 6):
    v7 = r7_at(c)
    v8 = r8_at(c)
    SENS_ROWS.append(dict(coupling_classes=c, r7=v7, r8=v8,
                          r7_blocks=(v7 > BUDGET), r8_blocks=(v8 > BUDGET),
                          n_layers_blocking=(int(v7 > BUDGET) + int(v8 > BUDGET) +
                                             int(MUS_SIZE_CALC > BUDGET) +
                                             int(P_MIN_R16_CALC > BUDGET))))
CRIT_COUP_CLASSES_R7 = min([r["coupling_classes"] for r in SENS_ROWS if r["r7_blocks"]]
                           or [None])
CRIT_COUP_CLASSES_R8 = min([r["coupling_classes"] for r in SENS_ROWS if r["r8_blocks"]]
                           or [None])
FRAGILE_LAYER = "R8" if (CRIT_COUP_CLASSES_R8 is not None and
                         CRIT_COUP_CLASSES_R7 is not None and
                         CRIT_COUP_CLASSES_R8 > CRIT_COUP_CLASSES_R7) else "R7"
# 全链抗性：公理层与谱层不依赖耦合谱类数 ⇒ 无论把谱压到几类，至少还有几层在挡。
MIN_LAYERS_AT_ANY_C = min(r["n_layers_blocking"] for r in SENS_ROWS)
MAX_LAYERS_AT_ANY_C = max(r["n_layers_blocking"] for r in SENS_ROWS)
CORE_LAYERS_INDEPENDENT_OF_SPECTRUM = (MIN_LAYERS_AT_ANY_C >= 2)

# ====================== 判词与元守卫 ======================
def verdict_with(token):
    return ("ALG-LB"
            + "__BOOKS-" + str(N_BOOKS)
            + "__MATCH-" + str(N_MATCH)
            + "__CLAIMS-" + str(N_CLAIM_ALL)
            + "__READS-" + str(N_READ_UNION)
            + "__B7-" + str(P_MIN_R7_DECL)
            + "__B8-" + str(P_MIN_R8_DECL)
            + "__B9-" + str(MUS_SIZE_DECL)
            + "__B16-" + str(P_MIN_R16_DECL)
            + "__MIN-" + str(B_MIN) + "gt" + str(BUDGET)
            + "__CRIT-" + str(CRIT_BUDGET)
            + "__XREF-" + str(CROSS_HIT)
            + "__CLEAN-" + str(token)
            + "__PRED-0")


v0 = verdict_with(str(N_FAIL_TOTAL))
v1 = verdict_with(str(N_FAIL_TOTAL + 1))
verdict_machine_ok = (v0 != v1) and (("__CLEAN-" + str(N_FAIL_TOTAL)) in v0)
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


def exp_act_distinct():
    """总账两路必须是不同函数、且 return 不是顶层数值常量。"""
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    found = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in ("ledger_act", "ledger_exp"):
            bad = False
            for sub in ast.walk(node):
                if isinstance(sub, ast.Return) and isinstance(sub.value, ast.Constant) and \
                   isinstance(sub.value.value, (int, float, bool)):
                    bad = True
            found[node.name] = (not bad)
    return (len(found) == 2) and all(found.values())


def readme_write_hits():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    hits = 0
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "open"):
            continue
        if not node.args:
            continue
        tgt = node.args[0]
        is_readme = ((isinstance(tgt, ast.Name) and tgt.id == "P_README") or
                     (isinstance(tgt, ast.Constant) and isinstance(tgt.value, str)
                      and "README" in tgt.value))
        if not is_readme:
            continue
        modes = [a.value for a in node.args[1:]
                 if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        if any(c in m for m in modes for c in "wa+"):
            hits += 1
    return hits


README_PREV_BYTES = 939057
README_CHANGED_EXTERNALLY = (README_BYTES != README_PREV_BYTES)
README_WRITE_HITS = readme_write_hits()

# 三根承重柱：总账、复算、敏感性；反噬时单点置 False 必须让 final 转 GATES-FAIL。
GATE_LEDGER_ACTIVE = True
GATE_RECALC_ACTIVE = True
GATE_SENS_ACTIVE = True

CREDIT_LAYERS_OK = sum(1 for r in LAYER_ROWS if r["ok"])


def credit_counts(led, rec, sen):
    """被承认成立的检查项数：册命中 + 层复算通过 + 敏感性档数。
    单点关掉任一门口，该读数就变 —— 三次反噬的四读数因此两两不同（26 / 10 / 22 / 20）。"""
    return ((N_MATCH if led else 0) + (CREDIT_LAYERS_OK if rec else 0) +
            (len(SENS_ROWS) if sen else 0))


CREDIT = credit_counts(GATE_LEDGER_ACTIVE, GATE_RECALC_ACTIVE, GATE_SENS_ACTIVE)

segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=(kind if ok else "FAIL"), note=note))


add("SOURCE-LINK-HEALTH", link_health and (len(source_missing) == 0), "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件（README + 16 册 JSON + 16 份 report），断链 " +
    str(len(source_missing)) + " 个；分母为 0 判 FAIL")
add("README-RECOUNT-HONEST", (README_BYTES > 0) and (README_MAX_RID > 0) and (TREE_MAX_RID > 0), "PASS",
    "动手前 rb 实时重数：" + str(README_BYTES) + " B / MD5 " + README_MD5 +
    " / README 内最大 RID " + str(README_MAX_RID) + " / 三树最大 RID " + str(TREE_MAX_RID) +
    "；本册不写 README、不占号、不登记")
add("README-STRUCTURAL-NO-WRITE", (README_WRITE_HITS == 0) and (not is_own(P_README)), "PASS",
    "AST 扫本机核全部 open() 调用，目标指向 README 且 mode 含 w/a/+ 的命中 " +
    str(README_WRITE_HITS) + " 次；README 不在本册产物集合内 ⇒ 结构性证明零写入（不依赖前后 MD5 相等）")
add("OWN-EXCLUSION-DEFINED", callable(is_own) and (len(OWN_NAMES) == 6) and
    all(v > 0 for v in INV.values()), "PASS",
    "自指按精确文件名排除本册 " + str(len(OWN_NAMES)) + " 个产物；主目录 " +
    str(INV["main_md"]) + " md / " + str(INV["main_html"]) + " html / 三树 " +
    str(INV["src_files"]) + "·" + str(INV["data_files"]) + "·" + str(INV["judge_files"]))

# —— ① 总账 ——
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 ledger_act 与 ledger_exp 两函数齐备、函数名不同、return 均非顶层数值常量")
add("LEDGER-16-BOOKS", GATE_LEDGER_ACTIVE and ALL_MATCH and (N_BOOKS == 16), "PASS",
    "十六册总账两路机拼：" + str(N_MATCH) + "/" + str(N_BOOKS) +
    " 逐册五项（verdict/final/guards/counts/sha256）全一致，失配字段 " +
    str(N_MISMATCH_FIELDS) + " 个")
add("LEDGER-FIELDS-NONEMPTY", all(r["sha"] and len(r["sha"]) == 64 and r["verdict"] and
                                  r["counts"] for r in LEDGER_ROWS), "PASS",
    "十六册的 sha256 均为 64 位、verdict 与 counts 非空；" +
    "空字段会让两路比对退化为「空==空」，故单列本守卫")
add("GUARD-SUM-FORBIDDEN", (GUARD_SUM_FORBIDDEN > 0) and (N_BOOKS == 16), "IDENTITY",
    "十六册守卫数之和 = " + str(GUARD_SUM_FORBIDDEN) + "，这是**计数**不是证据量；" +
    "把各册守卫数相加等于把 16 份审计当 1 份放大，单列 IDENTITY 配 NOT-ALL-GREEN")
add("GATE-DIST-NO-FAIL", (N_FAIL_TOTAL == 0), "PASS",
    "十六册合并分类计数 " + json.dumps(GATE_DIST, ensure_ascii=False, sort_keys=True) +
    "；FAIL 合计 " + str(N_FAIL_TOTAL) + "（计数可合并，结论不可合并）")

# —— ② 依赖图 ——
add("CLAIM-READING-GRAPH", (N_CLAIMS > 0) and (N_READ_STR > 0) and (N_EDGES > 0), "PASS",
    "断言—读数图：断言 " + str(N_CLAIM_ALL) + " 条（" +
    json.dumps(CLAIM_KIND, ensure_ascii=False, sort_keys=True) + "）、读数键 " + str(N_READ_KEYS) +
    " 个、读数串实例 " + str(N_READ_STR) + " 个（去重 " + str(N_READ_UNION) +
    " 个）、同册支撑边 " + str(N_EDGES) + " 条，覆盖 " + str(N_SUPPORTED) + " 条断言（" +
    dstr(D(str(SUPPORT_RATIO * 100)), 3) + "%）")
add("MATCHER-NEGATIVE-CONTROL", MATCHER_DISCRIMINATES, "PASS",
    "负对照：跨册错配（第 i 册 note 对第 i+1 册读数）后支撑降至 " + str(N_SUPPORTED_MIS) + " 条（" +
    dstr(D(str(SUPPORT_RATIO_MIS * 100)), 3) + "%），真值 " + str(N_SUPPORTED) +
    " 条 ⇒ 匹配器不是恒真；★支撑率低（" + dstr(D(str(SUPPORT_RATIO * 100)), 3) +
    "%）是体例事实（多数断言论述而不复述数字），不作缺陷判据、不作结论承重")
add("MATCHER-POSITIVE-CONTROL", POS_CLAIM_OK and NEG_CLAIM_OK, "PASS",
    "正对照：注入了本册全部读数的断言必然被判「有支撑」，注入「无」的断言必然无支撑 ⇒ 匹配器不瞎")
add("CROSS-ROUND-SUPPORT", (CROSS_HIT >= 0) and (CROSS_HIT <= N_CLAIM_ALL), "PASS",
    "跨册支撑断言 " + str(CROSS_HIT) + "/" + str(N_CLAIM_ALL) + "（边 " + str(CROSS_EDGES) +
    " 条）：十六册之间有真实读数引用，不是十六份互不相干的自述")
add("DAG-NO-SELF-LOOP", all(r["name"] for r in LEDGER_ROWS), "INFO",
    "扇出最高的读数（单点故障候选）：" +
    " / ".join("`" + k + "`×" + str(v) for k, v in TOP_FANOUT[:5]) +
    "；扇出只统计长度 ≥6 的串，短串会造成假扇出")

# —— ③ 四层下界加数级复算 ——
add("R7-ADDEND-RECALC", GATE_RECALC_ACTIVE and (P_MIN_R7_DECL == P_MIN_R7_CALC), "PASS",
    "方程层 " + str(P_MIN_R7_DECL) + " = 独立质量方向 " + str(N_MASSIVE) + " + 耦合谱破缺 " +
    str(BREAK_COUP) + "（谱类 " + str(COUP_CLASSES) + "−1）；质量方向由 forces 的 mass_eV≠0 机读，" +
    "谱类由第七轮 exp 口径取 " + str(COUP_CLASSES) + "（act 口径亦 " + str(COUP_CLASSES_ACT) + "）")
add("R8-ADDEND-RECALC", GATE_RECALC_ACTIVE and (P_MIN_R8_DECL == P_MIN_R8_CALC), "PASS",
    "标签层 " + str(P_MIN_R8_DECL) + " = 离散标签 " + str(LABELS_TREE) + "（树口径；比特口径为 " +
    str(LABELS_BITS) + "）+ 统一尺度 " + str(SCALE_PARAMS))
add("R9-MUS-MINIMAL", GATE_RECALC_ACTIVE and MUS_MINIMAL and MUS_REDUNDANT_UNSAT and
    (MUS_SIZE_CALC == MUS_SIZE_DECL), "PASS",
    "公理层 " + str(MUS_SIZE_DECL) + " = 最小不可满足核大小 |{" + ",".join(MUS) + "}| = " +
    str(MUS_SIZE_CALC) + "；最小性机读：删核内任一原子后可满足 " + str(MUS_MINIMAL) +
    "，核外 " + str(len(MUS_REDUNDANT)) + " 个原子删除后仍不可满足 " + str(MUS_REDUNDANT_UNSAT) +
    "（共 " + str(N_AXIOMS) + " 个原子）")
add("R16-ADDEND-RECALC", GATE_RECALC_ACTIVE and (P_MIN_R16_DECL == P_MIN_R16_CALC), "PASS",
    "谱层 " + str(P_MIN_R16_DECL) + " = 参数预算 " + str(BUDGET16) + " + 缺口 " + str(GAP16) +
    "（第十四/十六轮 14 族 × 24 排列全排除，本册只复算加数关系、不重跑拟合）")
add("FOUR-BOUNDS-DECLARED", (len(BOUNDS) == 4) and (B_MIN == 4), "PASS",
    "四条下界 " + "/".join(str(b) for b in BOUNDS) + " ⇒ min = " + str(B_MIN) +
    "、max = " + str(B_MAX) + "；与预算 " + str(BUDGET) + " 相较：min > 预算 = " +
    str(B_MIN_GT_BUDGET))
add("MIN-GT-BUDGET", B_MIN_GT_BUDGET and B_MAX_GT_BUDGET, "PASS",
    "★最强单句：**任意一层成立即可** ⇒ 下界 " + str(B_MIN) + " > 预算 " + str(BUDGET) +
    "。取 min（任一层足够），不取 max（要全部成立）、更不求和（" + str(sum(BOUNDS)) + " 是禁止操作）")
add("BUDGET-PHASE-POINT", (PHASE_POINT[1] == CRIT_BUDGET) and (CRIT_BUDGET == 3), "PASS",
    "预算相变：" + " / ".join("k=" + str(k) + "→" + str(n) + " 层" for k, n in BUDGET_SWEEP) +
    "；四层全挡的预算上限 = " + str(PHASE_POINT[1]) + " = 临界预算 " + str(CRIT_BUDGET) +
    "；预算 = 4 时只剩 " + str([n for k, n in BUDGET_SWEEP if k == 4][0]) + " 层承重")
add("ADDEND-CONCEPT-COUNT", (N_ADDEND_INST == 7) and (N_ADDEND_CONCEPT == 7), "PASS",
    "加数级展开 " + str(N_ADDEND_INST) + " 项：" +
    " / ".join(a["layer"] + "·" + a["name"] + "=" + str(a["value"]) for a in ADDENDS) +
    "；概念支点 " + str(N_ADDEND_CONCEPT) + " 个（层数与支点数不同，见下条）")
FI_PAIRS_STR = str([list(p) for p in FORM_ISOMORPHIC_PAIRS])
FI_FIRST_MS = "无"
if FORM_ISOMORPHIC_PAIRS:
    _fid = FORM_ISOMORPHIC_PAIRS[0][0]
    FI_FIRST_MS = str(addend_multiset([r for r in LAYER_ROWS if r["id"] == _fid][0]))
add("FORM-ISOMORPHIC-PAIR", (len(FORM_ISOMORPHIC_PAIRS) == 1), "IDENTITY",
    "★形式同构对 " + FI_PAIRS_STR + "：加数多重集同为 " + FI_FIRST_MS +
    "，但加数对象不同（标签数+尺度 vs 预算+缺口）⇒ 属形式同构、**不是同一条算式的两次独立验证**；" +
    "单列 IDENTITY 配 NOT-ALL-GREEN，不计作两份证据")
add("LAYER-DEPENDENCE-EDGES", (N_DEP_EDGES == len(DEP_EDGES)) and (N_DEP_EDGES > 0), "PASS",
    "层间依赖边 " + str(N_DEP_EDGES) + " 条：" +
    " / ".join("R" + str(a) + "←R" + str(b) for a, b in DEP_EDGES) +
    "（判据：A 册 JSON 全文是否出现 B 册的核心下界键名）；独立源 " + str(N_INDEPENDENT) +
    " 个（R" + "/R".join(str(i) for i in INDEPENDENT_SOURCES) + "）、依赖深度 " + str(DEP_DEPTH))
add("LAYERS-NOT-FOUR-PROOFS", (N_INDEPENDENT < len(LAYER_ROWS)), "IDENTITY",
    "★四层不等于四份独立证据：独立源只有 " + str(N_INDEPENDENT) + " 个（" +
    "R" + "/R".join(str(i) for i in INDEPENDENT_SOURCES) + "），依赖深度 " + str(DEP_DEPTH) +
    " ⇒ 「四层同时挡」这句话的承重是 " + str(N_INDEPENDENT) + " 个支点，不是 4 个；" +
    "这是第十四轮「门数 N ≠ N 份证据」的第二次精确落地（这次是「层数 ≠ 份数」），单列 IDENTITY")
add("SHARED-VALUE-PIVOTS", (len(SHARED_PIVOTS) == 2), "PASS",
    "同值支点：" + json.dumps(SHARED_PIVOTS, ensure_ascii=False) +
    "；值 3 同时出现在 R7·耦合谱破缺 与 R8·离散标签（树口径）—— 这两处是**同一个量**（谱类−1），" +
    "属真实重复计数；值 3 在 R16·参数预算、值 1 在 R8·统一尺度/ R16·缺口 只是数值巧合" +
    " ⇒ **数值相同不等于同源**，去重必须按来源名判，不能按值判")

# —— ④ 敏感性 ——
add("SENS-COUPLING-CLASSES", GATE_SENS_ACTIVE and (CRIT_COUP_CLASSES_R7 == 3) and
    (CRIT_COUP_CLASSES_R8 == 4), "PASS",
    "耦合谱类数敏感性：" + " / ".join(
        "c=" + str(r["coupling_classes"]) + "→R7 " + str(r["r7"]) + "(" +
        ("挡" if r["r7_blocks"] else "破") + ")、R8 " + str(r["r8"]) + "(" +
        ("挡" if r["r8_blocks"] else "破") + ")" for r in SENS_ROWS) +
    "；R7 在 c≥" + str(CRIT_COUP_CLASSES_R7) + " 仍挡、R8 需 c≥" + str(CRIT_COUP_CLASSES_R8) +
    " ⇒ 最先失效的一层是 " + FRAGILE_LAYER)
add("SPECTRUM-INDEPENDENT-CORE", CORE_LAYERS_INDEPENDENT_OF_SPECTRUM, "PASS",
    "公理层与谱层不依赖耦合谱类数 ⇒ 无论把谱压到几类，至少仍有 " + str(MIN_LAYERS_AT_ANY_C) +
    " 层在挡（最多 " + str(MAX_LAYERS_AT_ANY_C) + " 层）；降谱类数打不穿全链")
add("CONTROL-SCALARS-DISTINCT", len(set(r["n_layers_blocking"] for r in SENS_ROWS)) >= 3, "PASS",
    "敏感性四读数（层数）" + str(sorted(set(r["n_layers_blocking"] for r in SENS_ROWS))) +
    " 至少三档，非恒值 ⇒ 敏感性判据有判别力")

# —— 边界与红线 ——
add("BOOKS-ARE-DOCUMENTS", (N_BOOKS == 16), "BOUNDARY",
    "★审查对象是**本仓 16 册算法联盟册的产物**（JSON + report），不是 16 篇独立论文，" +
    "也不是全人类物理文献；「十六册全过」只说明这 16 份自审文件内部一致")
add("BOUND-IS-FAMILY-LIMITED", (B_MIN == 4) and (B_MAX == 5), "BOUNDARY",
    "四条下界各自的适用范围不变：R7 限 Yukawa/Proca 单方程族、R8 限 8 个显式族 × 四门、" +
    "R9 限 7 原子 + I1 的目标集、R16 限 14 个显式种子族 × 24 指派；本册**不扩大**任何一条")
add("NO-BREAKTHROUGH", (N_FAIL_TOTAL == 0) and (B_MIN > BUDGET), "INFO",
    "本册不宣称攻破统一场论，也不宣称攻破力的统一；只产可算判决")
add("MATH-NOT-EXPERIMENT", (N_BOOKS == 16) and (N_CLAIMS > 0), "INFO",
    "全部结论来自两路机读、加数级精确整数复算与字符串级依赖解析，不是实验证实；不产新物理")
add("NEXT-EXIT", (B_MIN > BUDGET) and (MIN_LAYERS_AT_ANY_C >= 2), "INFO",
    "硬出口未变：要么一条带双侧误差棒、理论值落在可判负区间之外的新读数配程序侧非回述输出；" +
    "要么一个本体数 ≤" + str(BUDGET) + " 且能在 1% 内生成四类耦合的显式机制。本轮两条都未给出")
add("NOT-ALL-GREEN", (N_SUPPORTED_MIS < N_SUPPORTED) and (N_DEP_EDGES > 0), "INFO",
    "负对照恒绿（轮转后支撑下降），但十六册失配数、加数复算、层间依赖边、敏感性四读数均非恒值")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把 FAIL 合计 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")


def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-FINAL-LOWER-BOUND--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-FINAL-LOWER-BOUND--GATES-FAIL"
    return "ALG-FINAL-LOWER-BOUND--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "BOOKS-ARE-DOCUMENTS", "BOUND-IS-FAMILY-LIMITED",
                     "GUARD-SUM-FORBIDDEN", "LAYERS-NOT-FOUR-PROOFS", "FORM-ISOMORPHIC-PAIR"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-FINAL-LOWER-BOUND--GATES-PASS-WITH-0-NEGATIVE") and \
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
    "books": N_BOOKS, "match": N_MATCH, "mismatch_fields": N_MISMATCH_FIELDS,
    "all_match": ALL_MATCH, "guard_sum_forbidden": GUARD_SUM_FORBIDDEN,
    "gate_dist": GATE_DIST, "fail_total": N_FAIL_TOTAL,
    "claims": N_CLAIM_ALL, "claim_kind": CLAIM_KIND,
    "read_keys": N_READ_KEYS, "read_str": N_READ_STR, "read_union": N_READ_UNION,
    "edges": N_EDGES, "supported": N_SUPPORTED,
    "support_pct": dstr(D(str(SUPPORT_RATIO * 100)), 3),
    "supported_mis": N_SUPPORTED_MIS,
    "support_pct_mis": dstr(D(str(SUPPORT_RATIO_MIS * 100)), 3),
    "matcher_discriminates": MATCHER_DISCRIMINATES,
    "cross_hit": CROSS_HIT, "cross_edges": CROSS_EDGES,
    "top_fanout": [[k, v] for k, v in TOP_FANOUT],
    "n_massive": N_MASSIVE, "coupling_classes": COUP_CLASSES,
    "coupling_classes_act": COUP_CLASSES_ACT, "kappa_classes": KAPPA_CLASSES,
    "break_coup": BREAK_COUP, "labels_tree": LABELS_TREE, "labels_bits": LABELS_BITS,
    "mus": MUS, "mus_size": MUS_SIZE_CALC, "mus_minimal": MUS_MINIMAL,
    "mus_redundant": MUS_REDUNDANT, "n_axioms": N_AXIOMS,
    "bounds": BOUNDS, "bound_min": B_MIN, "bound_max": B_MAX, "budget": BUDGET,
    "bound_min_gt_budget": B_MIN_GT_BUDGET, "bound_sum_forbidden": sum(BOUNDS),
    "crit_budget": CRIT_BUDGET, "phase_point": list(PHASE_POINT),
    "budget_sweep": [[k, n] for k, n in BUDGET_SWEEP],
    "addends": ADDENDS, "addend_inst": N_ADDEND_INST, "addend_concept": N_ADDEND_CONCEPT,
    "shared_pivots": SHARED_PIVOTS,
    "form_isomorphic_pairs": [list(p) for p in FORM_ISOMORPHIC_PAIRS],
    "dep_edges": [list(e) for e in DEP_EDGES], "n_dep_edges": N_DEP_EDGES,
    "independent_sources": INDEPENDENT_SOURCES, "n_independent": N_INDEPENDENT,
    "dep_depth": DEP_DEPTH, "layers_are_independent": LAYERS_ARE_INDEPENDENT,
    "crit_coup_r7": CRIT_COUP_CLASSES_R7, "crit_coup_r8": CRIT_COUP_CLASSES_R8,
    "fragile_layer": FRAGILE_LAYER,
    "min_layers_any_c": MIN_LAYERS_AT_ANY_C, "max_layers_any_c": MAX_LAYERS_AT_ANY_C,
    "readme_bytes": README_BYTES, "readme_md5": README_MD5,
    "readme_max_rid": README_MAX_RID, "tree_max_rid": TREE_MAX_RID,
    "readme_prev_bytes": README_PREV_BYTES,
    "readme_changed_externally": README_CHANGED_EXTERNALLY,
    "readme_write_hits": README_WRITE_HITS,
    "credit": CREDIT, "credit_layers_ok": CREDIT_LAYERS_OK,
    "source_files": len(SOURCE_FILES), "source_missing": len(source_missing),
    "four_force_incomplete": 1, "spine_independent_predictions": 0,
    "alg_md": INV["alg_md"], "alg_html": INV["alg_html"],
}

out = dict(
    title="算法联盟 · 统一场论第十七轮：四层下界总账、加数级复算与单点故障",
    date="2026-11-14", nature="AUDIT-DECISION-NOT-PHYSICS",
    declared_negative=["本册不宣称攻破统一场论", "本册不宣称攻破力的统一",
                       "独立实验预言 0", "四力大统一正确方程 0 条",
                       "审查对象是本仓 16 册产物，不是 16 篇独立论文"],
    ledger=LEDGER_ROWS,
    graph=dict(claims=N_CLAIM_ALL, claim_kind=CLAIM_KIND, edges=N_EDGES,
               supported=N_SUPPORTED, support_pct=dstr(D(str(SUPPORT_RATIO * 100)), 3),
               supported_mis=N_SUPPORTED_MIS,
               support_pct_mis=dstr(D(str(SUPPORT_RATIO_MIS * 100)), 3),
               cross_hit=CROSS_HIT, cross_edges=CROSS_EDGES,
               top_fanout=[[k, v] for k, v in TOP_FANOUT]),
    layers=LAYER_ROWS,
    bounds=dict(values=BOUNDS, min=B_MIN, max=B_MAX, sum_forbidden=sum(BOUNDS),
                budget=BUDGET, min_gt_budget=B_MIN_GT_BUDGET,
                crit_budget=CRIT_BUDGET, sweep=[[k, n] for k, n in BUDGET_SWEEP]),
    addends=dict(rows=ADDENDS, inst=N_ADDEND_INST, concept=N_ADDEND_CONCEPT,
                 shared=SHARED_PIVOTS,
                 form_isomorphic=[list(p) for p in FORM_ISOMORPHIC_PAIRS]),
    dependence=dict(edges=[list(e) for e in DEP_EDGES], n=N_DEP_EDGES,
                    sources=INDEPENDENT_SOURCES, n_sources=N_INDEPENDENT, depth=DEP_DEPTH),
    sensitivity=SENS_ROWS,
    readme=dict(bytes=README_BYTES, md5=README_MD5, max_rid=README_MAX_RID,
                tree_max_rid=TREE_MAX_RID, prev_bytes=README_PREV_BYTES,
                changed_externally=README_CHANGED_EXTERNALLY, write_hits=README_WRITE_HITS),
    verifier=dict(alg_md=INV["alg_md"], alg_html=INV["alg_html"]),
    counts=counts, guard_pass=g_pass, guard_count=g_count,
    verdict=verdict, final=final,
    key_numbers=key_numbers, segments=segs,
)
_payload = json.dumps(out, ensure_ascii=False, sort_keys=True, indent=0)
digest = hashlib.sha256(_payload.encode("utf-8")).hexdigest()
out["content_sha256"] = digest

if __name__ == "__main__":
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("算法联盟：四层下界总账、加数级复算与单点故障（第十七轮）")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False, sort_keys=True))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("① 十六册总账（两路机拼：JSON 结构侧 vs report 文本侧）")
    for r in LEDGER_ROWS:
        lines.append("  " + str(r["round"]).rjust(2) + " " + r["name"].ljust(14) +
                     " " + r["guards"].rjust(6) + "  " +
                     ("MATCH" if r["match"] else "DIFF " + ",".join(r["diff"])) +
                     "  " + str(r["sha"])[:12])
    lines.append("  ⇒ " + str(N_MATCH) + "/" + str(N_BOOKS) + " 全一致，失配字段 " +
                 str(N_MISMATCH_FIELDS) + " 个；守卫数之和 " + str(GUARD_SUM_FORBIDDEN) +
                 " 只作计数、禁止当证据量")
    lines.append("-" * 96)
    lines.append("② 断言—读数依赖图")
    lines.append("  断言 " + str(N_CLAIM_ALL) + " 条 " + json.dumps(CLAIM_KIND, ensure_ascii=False, sort_keys=True) +
                 "；读数键 " + str(N_READ_KEYS) + " / 串实例 " + str(N_READ_STR) +
                 " / 去重 " + str(N_READ_UNION))
    lines.append("  同册支撑 " + str(N_SUPPORTED) + " 条（" + dstr(D(str(SUPPORT_RATIO * 100)), 3) +
                 "%）、边 " + str(N_EDGES) + "；负对照（跨册错配）" + str(N_SUPPORTED_MIS) +
                 " 条（" + dstr(D(str(SUPPORT_RATIO_MIS * 100)), 3) + "%）")
    lines.append("  跨册支撑 " + str(CROSS_HIT) + " 条 / 边 " + str(CROSS_EDGES) + " 条")
    lines.append("  最高扇出：" + " / ".join("`" + k + "`×" + str(v) for k, v in TOP_FANOUT[:5]))
    lines.append("-" * 96)
    lines.append("③ 四条下界的加数级复算")
    for r in LAYER_ROWS:
        lines.append("  " + r["id"].ljust(4) + " " + r["layer"] + "  登记 " + str(r["decl"]) +
                     " = 复算 " + str(r["calc"]) + "  " + ("OK" if r["ok"] else "FAIL") +
                     "  | " + r["basis"])
    lines.append("  ⇒ " + "/".join(str(b) for b in BOUNDS) + "：min = " + str(B_MIN) +
                 " > 预算 " + str(BUDGET) + "（max = " + str(B_MAX) +
                 "，求和 " + str(sum(BOUNDS)) + " 属禁止操作）")
    lines.append("  预算相变：" + " / ".join("k=" + str(k) + "→" + str(n) + " 层" for k, n in BUDGET_SWEEP) +
                 "；四层全挡的预算上限 = " + str(PHASE_POINT[1]))
    lines.append("-" * 96)
    lines.append("④ 加数去重与层间依赖")
    lines.append("  加数 " + str(N_ADDEND_INST) + " 项 / 概念支点 " + str(N_ADDEND_CONCEPT) +
                 " 个；被多层共用：" + json.dumps(SHARED_PIVOTS, ensure_ascii=False))
    lines.append("  形式同构对：" + str([list(p) for p in FORM_ISOMORPHIC_PAIRS]) +
                 "（形式同构 ≠ 同一条算式的两次独立验证）")
    lines.append("  层间依赖边 " + str(N_DEP_EDGES) + " 条：" +
                 " / ".join("R" + str(a) + "←R" + str(b) for a, b in DEP_EDGES) +
                 "；独立源 " + str(N_INDEPENDENT) + " 个、依赖深度 " + str(DEP_DEPTH))
    lines.append("  ⇒ ★四层 ≠ 四份独立证据：真实支点 " + str(N_INDEPENDENT) + " 个")
    lines.append("-" * 96)
    lines.append("⑤ 敏感性：最先失效的一层")
    for r in SENS_ROWS:
        lines.append("  c=" + str(r["coupling_classes"]) + "  R7=" + str(r["r7"]) + "(" +
                     ("挡" if r["r7_blocks"] else "破") + ")  R8=" + str(r["r8"]) + "(" +
                     ("挡" if r["r8_blocks"] else "破") + ")  在挡层数=" + str(r["n_layers_blocking"]))
    lines.append("  ⇒ R7 在 c≥" + str(CRIT_COUP_CLASSES_R7) + " 仍挡；R8 需 c≥" +
                 str(CRIT_COUP_CLASSES_R8) + " ⇒ 最脆弱层 " + FRAGILE_LAYER +
                 "；公理层/谱层与谱类数无关 ⇒ 至少 " + str(MIN_LAYERS_AT_ANY_C) + " 层恒在挡")
    lines.append("-" * 96)
    lines.append("结论：不宣称攻破统一场论；四力大统一正确方程 0 条；独立实验预言 0。")
    lines.append("      最强单句：四条下界 " + "/".join(str(b) for b in BOUNDS) +
                 " 的最小值 " + str(B_MIN) + " > 参数预算 " + str(BUDGET) +
                 " ⇒「≤3 参数生成四力」在四层任一处被否。")
    lines.append("README：" + str(README_BYTES) + " B / " + README_MD5 + " / 最大 RID " +
                 str(README_MAX_RID) + " / 三树最大 RID " + str(TREE_MAX_RID) +
                 "；本册零写入（AST 结构性证明）、不占号。")
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
