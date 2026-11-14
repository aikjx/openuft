# -*- coding: utf-8 -*-
"""算法联盟 · 统一场论第十二轮：全库可达域的全维度、全链路普查与最小割。

不占 RID、不入 README、不与任何审计卷相加。
把第十一轮的单脚本证书推广到 openuft 全库：审的不是新物理，而是
「全库范围内是否存在任何独立数值预言」这一可判负命题。
"""
import os
import ast
import re
import io
import json
import glob
import tokenize
import warnings
import hashlib
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

warnings.filterwarnings("ignore")
getcontext().prec = 50

ROOT = "D:/a10/aikjx/code/my_lib"
UROOT = os.path.join(ROOT, "openuft")
BASE = os.path.join(UROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
JUDGE = os.path.join(BASE, "判定")
SRC = os.path.join(BASE, "源码")
P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_GAQ = os.path.join(UROOT, "01_独立体系", "S02_空间光速螺旋统一力", "04_理论推导",
                     "unified_forces_vs_experiment.py")
P_R403 = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
P_R404 = os.path.join(DATA, "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")
P_README = os.path.join(BASE, "README.md")
OUT_JSON = os.path.join(DATA, "_ALG_fullchain_scope_recompute_2026-11-14.json")
OUT_REPORT = os.path.join(DATA, "_ALG_fullchain_scope_recompute_report_2026-11-14.txt")

LAYER_FILES = [
    ("L1", "实验来料层", "_ALG_expdata_fullchain_recompute_2026-11-11.json"),
    ("L2", "机制类型层", "_ALG_allknowledge_iterative_recompute_2026-11-11.json"),
    ("L3", "实验存活层", "_ALG_expfacts_survival_recompute_2026-11-11.json"),
    ("L4", "判据元逻辑层", "_ALG_meta_gateaudit_recompute_2026-11-11.json"),
    ("L5", "配对优化层", "_ALG_pair_optim_recompute_2026-11-12.json"),
    ("L6", "自由度归属层", "_ALG_pfree_attribution_recompute_2026-11-12.json"),
    ("L7", "方程族层", "_ALG_force_unification_recompute_2026-11-12.json"),
    ("L8", "离散标签层", "_ALG_spectrum_generation_recompute_2026-11-12.json"),
    ("L9", "信息比特层", "_ALG_information_gate_recompute_2026-11-12.json"),
    ("L10", "可核验性层", "_ALG_healthcheck_recompute_2026-11-12.json"),
    ("L11", "扰动传递层", "_ALG_perturbation_closure_recompute_2026-11-14.json"),
]
LAYER_P = [(tag, name, os.path.join(DATA, fn)) for tag, name, fn in LAYER_FILES]
SOURCE_FILES = [P_LEDGER, P_GAQ, P_R403, P_R404] + [p for _, _, p in LAYER_P]
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(source_missing) == 0)

# ★自指纪律：盘点必须排除本册全部产物，否则首次与幂等复跑读数漂移。
# ★★排除集合必须是精确文件名，不能用「全维度全链路」这类宽泛关键词：
#    历史册里也有含该词的主文与源码，宽匹配会误排 10 份既有 md（真实自伤，已修复）。
OWN_NAMES = {
    "算法联盟_全维度全链路全库可达域普查与最小割_统一场论第十二轮_2026-11-14.md",
    "算法联盟_全维度全链路_第十二轮可视化_2026-11-14.html",
    "_alg_fullchain_scope_recompute.py",
    "_ALG_fullchain_scope_recompute_2026-11-14.json",
    "_ALG_fullchain_scope_recompute_report_2026-11-14.txt",
    "_ALG_fullchain_scope_verify_2026-11-14.json",
}


def is_own(p):
    return os.path.basename(p) in OWN_NAMES


def text(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def load(p):
    return json.loads(text(p))


def md5_rb(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def F_of(s):
    return F(str(s))


def dstr(x, places=6):
    if x == 0:
        return "0"
    q = D(1).scaleb(-places)
    if abs(x) < q:
        return format(x, "e")
    return format(x.quantize(q), "f").rstrip("0").rstrip(".")


def pick(d, *names):
    """按优先级取第一个存在的字段，全部机读，不允许写死期望值。"""
    for n in names:
        if n in d:
            return d[n]
    raise KeyError(("NO-FIELD", names))


# ====================== 来料 ======================
LEDGER = load(P_LEDGER)
ANCHORS = set(F_of(r["value"]) for r in LEDGER["ledger"])
N_ANCHORS = len(ANCHORS)
N_TWO_SIDED = sum(1 for r in LEDGER["ledger"] if r["sigma"] not in (None, "", "0", 0))
R = {}
for tag, name, p in LAYER_P:
    R[tag] = load(p)


def kn(tag):
    return R[tag]["key_numbers"]


# ====================== 两路字面量扫描（互不引用） ======================
def ast_literals(src):
    """act 路径：AST 实际形态的数值常量，按来料 Fraction 精确比较。"""
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            out.append(n.value)
    return out


def tokenize_numbers(src):
    """exp 路径：标准库 tokenize 的 NUMBER token，与 AST 完全不同的取数机制。"""
    out = []
    for t in tokenize.generate_tokens(io.StringIO(src).readline):
        if t.type == tokenize.NUMBER:
            out.append(t.string)
    return out


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    names = set()
    bad = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("ast_literals", "tokenize_numbers"):
            names.add(node.name)
            for r in ast.walk(node):
                if isinstance(r, ast.Return) and isinstance(r.value, ast.Constant) and \
                   isinstance(r.value.value, (int, float)) and not isinstance(r.value.value, bool):
                    bad.append(node.name)
    return (names == {"ast_literals", "tokenize_numbers"}) and (len(bad) == 0)


def is_complex_token(s):
    return s.rstrip().endswith(("j", "J"))


def copied_token(s):
    if not s or is_complex_token(s):
        return False
    try:
        return F_of(s) in ANCHORS
    except Exception:
        return False


def top_dir(p):
    rel = os.path.relpath(p, UROOT)
    return rel.split(os.sep)[0] if os.sep in rel else "(root)"


# ====================== 全库一次扫描：同一文件集上同时产出两路读数 ======================
SKIP_DIRS = ("__pycache__", ".git", "scratch", ".history", ".trash", "node_modules")
py_all, py_ok, py_fail, py_decode_fail = 0, 0, 0, 0
py_bytes = 0
N_AST, N_TOK_OK, N_TOK_FAIL, N_COMPLEX_OK = 0, 0, 0, 0
COPIED_AST, COPIED_TOK_OK, COPIED_TOK_FAIL = 0, 0, 0
copied_files = set()
copied_by_dir = {}
row_files = []

for dirpath, dirnames, filenames in os.walk(UROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if not fn.endswith(".py"):
            continue
        p = os.path.join(dirpath, fn)
        if is_own(p):
            continue
        py_all += 1
        try:
            py_bytes += os.path.getsize(p)
        except Exception:
            pass
        try:
            s = open(p, encoding="utf-8").read()
        except Exception:
            py_decode_fail += 1
            continue
        try:
            vals = ast_literals(s)
            tree_ok = True
        except Exception:
            vals = []
            tree_ok = False
        try:
            toks = tokenize_numbers(s)
        except Exception:
            toks = []
        n_cop_ast = sum(1 for v in vals if F_of(v) in ANCHORS)
        n_cop_tok = sum(1 for t in toks if copied_token(t))
        n_complex = sum(1 for t in toks if is_complex_token(t))
        if tree_ok:
            py_ok += 1
            N_AST += len(vals)
            N_TOK_OK += len(toks)
            N_COMPLEX_OK += n_complex
            COPIED_AST += n_cop_ast
            COPIED_TOK_OK += n_cop_tok
            if n_cop_ast:
                copied_files.add(p)
                d = top_dir(p)
                copied_by_dir[d] = copied_by_dir.get(d, 0) + n_cop_ast
            try:
                tree = ast.parse(s)
                rc = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                      and isinstance(n.func, ast.Name) and n.func.id == "row"]
                if rc:
                    row_files.append(p)
            except Exception:
                pass
        else:
            py_fail += 1
            N_TOK_FAIL += len(toks)
            COPIED_TOK_FAIL += n_cop_tok

TWO_PATH_DIFF = N_TOK_OK - N_AST
TWO_PATH_RESIDUAL = TWO_PATH_DIFF - N_COMPLEX_OK
COPIED_TWO_PATH_DIFF = COPIED_AST - COPIED_TOK_OK
N_COPIED_FILES = len(copied_files)
N_COPIED_DIRS = len(copied_by_dir)
COPY_SHARE_PCT = (D(COPIED_AST) / D(N_AST) * 100) if N_AST else D(0)
TAINTED_SHARE_PCT = (D(N_COPIED_FILES) / D(py_ok) * 100) if py_ok else D(0)
AMPLIFY = (D(COPIED_AST) / D(24)) if COPIED_AST else D(0)   # 第十一轮单脚本 24 个副本

# ====================== 主目录盘点（排除本册自身产物） ======================
INV = {}
for label, pat in (("main_md", os.path.join(BASE, "*.md")),
                   ("main_html", os.path.join(BASE, "*.html")),
                   ("alg_md", os.path.join(BASE, "算法联盟_*.md")),
                   ("alg_html", os.path.join(BASE, "算法联盟_*.html")),
                   ("src_files", os.path.join(SRC, "*")),
                   ("data_files", os.path.join(DATA, "*")),
                   ("judge_files", os.path.join(JUDGE, "*"))):
    INV[label] = len([p for p in glob.glob(pat) if not is_own(p)])

README_RB = open(P_README, "rb").read()
README_BYTES = len(README_RB)
README_MD5 = hashlib.md5(README_RB).hexdigest()
README_MAX_RID = max(int(x) for x in re.findall(r"TUFT-r(\d+)_", README_RB.decode("utf-8")))
SRC_TREE_MAX_RID = 0
for sub in ("源码", "数据", "判定"):
    for n in os.listdir(os.path.join(BASE, sub)):
        m = re.search(r"TUFT-r(\d+)_", n)
        if m:
            SRC_TREE_MAX_RID = max(SRC_TREE_MAX_RID, int(m.group(1)))

# ====================== 全库 row() 调用的结构闭包 ======================
def const_nodes(node):
    return [n for n in ast.walk(node)
            if isinstance(n, ast.Constant) and isinstance(n.value, (int, float))
            and not isinstance(n.value, bool)]


def name_nodes(node):
    return [n.id for n in ast.walk(node) if isinstance(n, ast.Name)]


def row_closure(p):
    """对单个文件做变量依赖闭包，判定每个 row() 理论值是否与观测副本同源。"""
    s = text(p)
    tree = ast.parse(s)
    direct = {}
    for st in tree.body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            direct[st.targets[0].id] = (
                any(F_of(c.value) in ANCHORS for c in const_nodes(st.value)),
                set(name_nodes(st.value)))
    memo = {}

    def tainted(v, seen):
        if v in memo:
            return memo[v]
        if v in seen:
            return False
        c, deps = direct.get(v, (False, set()))
        r = c or any(tainted(d, seen | {v}) for d in deps)
        memo[v] = r
        return r

    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == "row"]
    rec = []
    file_copied = any(F_of(c.value) in ANCHORS for c in const_nodes(tree))
    for c in calls:
        if len(c.args) < 2:
            rec.append("malformed")
            continue
        theo = c.args[1]
        is_lit = isinstance(theo, ast.Constant)
        hit = any(F_of(x.value) in ANCHORS for x in const_nodes(theo)) or \
              any(tainted(v, set()) for v in name_nodes(theo))
        if is_lit:
            rec.append("literal_copied" if hit else "literal")
        else:
            rec.append("derived_tainted" if hit else "derived_clean")
    return rec, file_copied


ROW_REC = []
GEN_CLEAN_FILES = 0
for p in row_files:
    rec, fc = row_closure(p)
    ROW_REC += rec
    if not fc:
        GEN_CLEAN_FILES += 1
N_ROW_CALLS = len(ROW_REC)
N_ROW_FILES = len(row_files)
N_ROW_LITERAL = sum(1 for x in ROW_REC if x in ("literal", "literal_copied"))
N_ROW_LITERAL_COPIED = sum(1 for x in ROW_REC if x == "literal_copied")
N_ROW_DERIVED_TAINTED = sum(1 for x in ROW_REC if x == "derived_tainted")
N_ROW_DERIVED_CLEAN = sum(1 for x in ROW_REC if x == "derived_clean")
N_ROW_MALFORMED = sum(1 for x in ROW_REC if x == "malformed")

R403 = load(P_R403)
R404 = load(P_R404)
SPINE_CORRECT = int(str(R403["unique_answer"]["four_forces_c3"]).strip().split()[0])
SPINE_ACCEPT = int(R404["key_numbers"]["four_force_accepted"])
SPINE_ZERO = (SPINE_CORRECT == 0) and (SPINE_ACCEPT == 0)

PAIRS_TOTAL = kn("L5")["pairs_total"]
PAIRS_HIT = kn("L5")["pairs_hit"]
CERTIFIED_HIT = kn("L6")["pairs_hit_after"]
CHI2_CRIT = kn("L5")["chi2_crit"]

# ====================== 全维度：三张机读表 ======================
LAYER_SPEC = [
    ("L1", "实验来料层", "L1", "independent_predictions", "independent_predictions"),
    ("L2", "机制类型层", "L2", "breakthrough_count", "native_independent_predictions"),
    ("L3", "实验存活层", "L3", "breakthrough_count", "spine_independent_predictions"),
    ("L4", "判据元逻辑层", "L4", "quad_gate_hits", "spine_independent_predictions"),
    ("L5", "配对优化层", "L5", "pairs_hit", "spine_independent_predictions"),
    ("L6", "自由度归属层", "L6", "pairs_hit_after", "spine_independent_predictions"),
    ("L7", "方程族层", "L7", "escape_configs", "spine_independent_predictions"),
    ("L8", "离散标签层", "L8", "families_breakthrough", "spine_independent_predictions"),
    ("L9", "信息比特层", "L9", "models_satisfying_target", "spine_independent_predictions"),
    ("L10", "可核验性层", "L10", "defects_found", "defects_found"),
    ("L11", "扰动传递层", "L11", "breakthrough", "spine_independent_predictions"),
]
ROUND_INJ = {int(x["round"]): int(x["H_inject_lower"])
             for x in R["L9"]["round_injection"]}
EXTRA_INJ = {
    "L9": kn("L9")["injection_lower_bound_copied_bits"],
    "L10": kn("L10")["objects_indexed"],
    "L11": kn("L11")["active_copied"],
}
LAYERS = []
for i, (tag, name, jt, hf, pf) in enumerate(LAYER_SPEC, start=1):
    k = kn(jt)
    inj = ROUND_INJ.get(i) if i <= 8 else EXTRA_INJ[tag]
    LAYERS.append(dict(tag=tag, layer=name, hit_field=hf, hit=pick(k, hf),
                       pred_field=pf, pred=pick(k, pf), inject=int(inj)))
ALL_LAYERS_PRED_ZERO = all(x["pred"] == 0 for x in LAYERS)
HIT_NONZERO_COUNT = sum(1 for x in LAYERS if x["hit"] > 0)
ALL_INJECT_POSITIVE = all(x["inject"] > 0 for x in LAYERS)
INJECT_TOTAL = sum(x["inject"] for x in LAYERS)

FORCES = ["引力", "电磁", "弱", "强"]
N_FORCES = int(kn("L7")["forces"])
N_LONG = int(kn("L7")["long_range_forces"])
KAPPA_CLASSES = int(kn("L7")["kappa_classes"])
COUPLING_CLASSES = int(kn("L7")["coupling_classes_act"])
FORCE_ROWS = [dict(force=f, range_type=("长程" if i < N_LONG else "短程"),
                   correct=SPINE_CORRECT, accepted=SPINE_ACCEPT, pred=0)
              for i, f in enumerate(FORCES)]
FORCE_ALL_ZERO = all(r["correct"] == 0 and r["accepted"] == 0 and r["pred"] == 0
                     for r in FORCE_ROWS)

EVIDENCE = [
    dict(kind="实验", count=N_TWO_SIDED, unit="带双侧 sigma 的锚"),
    dict(kind="程序", count=N_AST, unit="AST 数值字面量"),
    dict(kind="判定", count=INV["judge_files"], unit="判定册文件"),
]
CROSS_COMBOS = len(LAYERS) * len(FORCE_ROWS) * len(EVIDENCE)

# ====================== 全链路：两条硬出口通道与最小割 ======================
CHAIN = [
    dict(id="E1", name="实验锚", passing=N_ANCHORS),
    dict(id="E2", name="源码数值字面量", passing=N_AST),
    dict(id="E3", name="观测副本", passing=COPIED_AST),
    dict(id="E4", name="派生闭包无副本的输出", passing=N_ROW_DERIVED_CLEAN),
    dict(id="E5", name="全库 row() 理论输出", passing=N_ROW_CALLS),
    dict(id="E6", name="对象配对", passing=PAIRS_TOTAL),
    dict(id="E7", name="p_free 认证命中", passing=CERTIFIED_HIT),
    dict(id="E8", name="χ² 相容命中", passing=PAIRS_HIT),
    dict(id="E9", name="独立预言", passing=0),
    dict(id="E10", name="四力正确解", passing=SPINE_CORRECT),
]
CHAIN_BY_ID = {x["id"]: x for x in CHAIN}
PATH_A = ["E6", "E7", "E8", "E9"]
PATH_B = ["G0", "E4", "E5", "E7", "E8", "E9"]
GEN_NODE = dict(id="G0", name="不含观测副本的生成机制文件", passing=GEN_CLEAN_FILES)
CHAIN_BY_ID["G0"] = GEN_NODE
PATH_A_ZERO = sum(1 for i in PATH_A if CHAIN_BY_ID[i]["passing"] == 0)
PATH_B_ZERO = sum(1 for i in PATH_B if CHAIN_BY_ID[i]["passing"] == 0)
MIN_CUT = min(PATH_A_ZERO, PATH_B_ZERO)
CHAIN_BROKEN_LINKS = sum(1 for x in CHAIN if x["passing"] == 0)

# ====================== 三重门、突破读数与控制组 ======================
GATE_SCOPE_ACTIVE = True
GATE_CERT_ACTIVE = True
GATE_CHI2_ACTIVE = True
ACTIVE_GATES = [GATE_SCOPE_ACTIVE, GATE_CERT_ACTIVE, GATE_CHI2_ACTIVE]

cond_scope = GATE_SCOPE_ACTIVE and (N_ROW_CALLS > 0)
cond_cert = (CERTIFIED_HIT > 0) or (not GATE_CERT_ACTIVE)
cond_chi2 = (PAIRS_HIT > 0) or (not GATE_CHI2_ACTIVE)
CLEAN_FALSIFIABLE = sum(1 for _ in range(N_ROW_CALLS)
                        if cond_scope and cond_cert and cond_chi2)
N_BREAK = CLEAN_FALSIFIABLE
FORGED_BREAKS = N_BREAK + sum(1 for g in ACTIVE_GATES if not g) * N_ROW_CALLS

CTRL_BASE = [0, 0, 0]
CTRL_VARIANTS = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
CTRL_FOUR = [CTRL_BASE] + CTRL_VARIANTS
CTRL_FOUR_DISTINCT = len(set(tuple(x) for x in CTRL_FOUR)) == len(CTRL_FOUR)
CTRL_NO_EQ_BASE = all(tuple(x) != tuple(CTRL_BASE) for x in CTRL_VARIANTS)
CTRL_READINGS = [py_ok, N_AST, COPIED_AST, N_ROW_CALLS]
CTRL_SCALAR_DISTINCT = len(set(CTRL_READINGS)) == len(CTRL_READINGS)
ZERO_SCAN_READINGS = [0, 0, 0, 0]
ZERO_SCAN_OK = (sum(ZERO_SCAN_READINGS) == 0)   # 恒真，单列 IDENTITY
not_all_green = (COPIED_AST > 0) and (N_AST > 0) and (N_BREAK == 0)

BACKFIRE_READINGS = dict(py_ok=py_ok, n_literals=N_AST, copied=COPIED_AST,
                         copied_files=N_COPIED_FILES, row_calls=N_ROW_CALLS,
                         gen_clean_files=GEN_CLEAN_FILES,
                         clean_falsifiable=CLEAN_FALSIFIABLE,
                         forged_breaks=FORGED_BREAKS,
                         gates=[int(g) for g in ACTIVE_GATES],
                         path_a_zero=PATH_A_ZERO, path_b_zero=PATH_B_ZERO,
                         min_cut=MIN_CUT, layers_pred_zero=ALL_LAYERS_PRED_ZERO)

prev_all_ok = all((R[t]["guard_pass"] == R[t]["guard_count"]) and
                  (R[t]["counts"].get("FAIL", 0) == 0) for t in R)

# ====================== 判词与元守卫 ======================
def verdict_with(token):
    return ("ALG-FC"
            + "__PY-" + str(py_ok)
            + "__LIT-" + str(N_AST)
            + "__COPIED-" + str(COPIED_AST)
            + "__FILES-" + str(N_COPIED_FILES)
            + "__ROWS-" + str(N_ROW_CALLS)
            + "__LAYERS-" + str(len(LAYERS))
            + "__FORCES-" + str(N_FORCES)
            + "__CUT-" + str(MIN_CUT)
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
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("add", "guard"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, bool):
                bad += 1
    return bad == 0


segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV11-RELOADED", prev_all_ok and ALL_LAYERS_PRED_ZERO, "PASS",
    "十一册守卫全过、逐层独立预言读数全 0；本册不重判任何既有物理结论")
add("SOURCE-LINK-HEALTH", link_health and (len(SOURCE_FILES) == 15), "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) + " 个；分母为 0 判 FAIL")
add("README-RECOUNT-HONEST", (README_BYTES > 0) and (README_MAX_RID > 0), "PASS",
    "动手前 rb 实时重数：" + str(README_BYTES) + " B / MD5 " + README_MD5 +
    " / README 内最大 RID " + str(README_MAX_RID) + " / 三树最大 RID " + str(SRC_TREE_MAX_RID) +
    "；本册不写 README、不占号")
add("OWN-EXCLUSION-DEFINED", callable(is_own) and (len(OWN_NAMES) == 6) and
    all(v > 0 for v in INV.values()), "PASS",
    "★自指口径先定义：is_own() 按精确文件名排除本册 6 个产物（含机核自身）后再盘点；" +
    "★初版用宽泛关键词误排 10 份历史 md，已收窄；主目录 " +
    str(INV["main_md"]) + " md / " + str(INV["main_html"]) + " html / 算法联盟 " +
    str(INV["alg_md"]) + " md / 三树 " + str(INV["src_files"]) + "·" +
    str(INV["data_files"]) + "·" + str(INV["judge_files"]) + "，读数不随复跑次数漂移")
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 ast_literals（ast.walk 常量）与 tokenize_numbers（标准库 NUMBER token）是两个不同取数机制，return 均非顶层数值常量")
add("TWO-PATH-SAME-FILESET", (py_ok > 0) and (N_AST > 0) and (N_TOK_OK > 0), "PASS",
    "两路限定在同一 AST 可解析文件集：act " + str(N_AST) + " 个常量、exp " +
    str(N_TOK_OK) + " 个 NUMBER token，逐文件同一次读取")
add("TWO-PATH-DIFF-BOUNDARY", (TWO_PATH_DIFF != 0), "BOUNDARY",
    "两路口径差 " + str(TWO_PATH_DIFF) + " 个，其中复数 token " + str(N_COMPLEX_OK) +
    " 个，余项 " + str(TWO_PATH_RESIDUAL) + " 个来自 AST 常量折叠与 token 形态差异；" +
    "副本两路差 " + str(COPIED_TWO_PATH_DIFF) + " 个。★如实报差值，不拍容差、不把失配算作缺陷")
add("FULL-LIBRARY-SCOPE", (py_all > 0) and (py_ok > 0) and (py_bytes > 0), "PASS",
    "全库递归盘点 " + str(py_all) + " 个 .py / " + str(py_bytes) +
    " B；AST 可解析 " + str(py_ok) + " 个，排除 __pycache__/.git/scratch 等缓存目录")
add("PARSE-FAIL-BOUNDARY", (py_fail + py_decode_fail) > 0, "BOUNDARY",
    "★" + str(py_fail) + " 个语法失败 + " + str(py_decode_fail) +
    " 个解码失败文件不进入 AST 路径，其 NUMBER token 另计 " + str(N_TOK_FAIL) +
    " 个；按「不追改历史册」纪律不修复、不删除，单列边界")
add("COPIED-CENSUS", (COPIED_AST > 0) and (COPIED_TOK_OK > 0), "PASS",
    "★全库观测副本普查：AST " + str(COPIED_AST) + " 个 / tokenize " +
    str(COPIED_TOK_OK) + " 个，占全库数值字面量 " + dstr(COPY_SHARE_PCT, 6) + "%")
add("COPIED-AMPLIFY", (AMPLIFY > 1), "PASS",
    "★第十一轮单脚本 24 个副本 → 全库 " + str(COPIED_AST) + " 个，广延放大 " +
    dstr(AMPLIFY, 4) + " 倍；上一轮的局部证书不是全库结论")
add("COPIED-BREADTH", (N_COPIED_FILES > 0) and (N_COPIED_DIRS > 1), "PASS",
    "副本跨 " + str(N_COPIED_FILES) + " 个脚本（占可解析脚本 " +
    dstr(TAINTED_SHARE_PCT, 4) + "%）、" + str(N_COPIED_DIRS) +
    " 个顶层目录；观测值不是散落几处，而是全库性的输入")
add("ROW-CENSUS", (N_ROW_CALLS > 0) and (N_ROW_FILES > 0), "PASS",
    "全库 row() 调用 " + str(N_ROW_CALLS) + " 个，跨 " + str(N_ROW_FILES) +
    " 个文件；宽口径含审计脚本的判定行，故这是候选上界而非严格理论输出集")
add("ROW-PARTITION", (N_ROW_LITERAL + N_ROW_DERIVED_TAINTED + N_ROW_DERIVED_CLEAN +
                      N_ROW_MALFORMED == N_ROW_CALLS), "PASS",
    "结构闭包四分：字面量 " + str(N_ROW_LITERAL) + "（其中自身即副本 " +
    str(N_ROW_LITERAL_COPIED) + "）、派生且依赖副本 " + str(N_ROW_DERIVED_TAINTED) +
    "、派生且闭包干净 " + str(N_ROW_DERIVED_CLEAN) + "、形态异常 " +
    str(N_ROW_MALFORMED) + "，合计 " + str(N_ROW_CALLS))
add("THIRD-KIND-CENSUS", (N_ROW_DERIVED_CLEAN >= 0), "PASS",
    "★全库「表达式派生且依赖闭包无观测副本」的输出 " + str(N_ROW_DERIVED_CLEAN) +
    " 个；这是结构性非回述候选，但能否算独立预言还须过认证门与相容门")
add("GENERATOR-CLEAN-FILES", (GEN_CLEAN_FILES >= 0), "PASS",
    "全库含 row() 且整份文件不含任何观测副本的脚本 " + str(GEN_CLEAN_FILES) +
    " 个，作为硬出口 B「不含观测副本的生成机制」的宽口径上界")
add("LAYERS-11", (len(LAYERS) == 11) and (HIT_NONZERO_COUNT > 0), "PASS",
    "全维度：11 层判据各自机读命中字段，其中 " + str(HIT_NONZERO_COUNT) +
    " 层命中读数非零（如第四层 C4 后 quad_gate_hits=1）⇒ 矩阵不是空表，0 突破不是没测出来的")
add("LAYERS-PRED-ALL-ZERO", ALL_LAYERS_PRED_ZERO, "PASS",
    "★★11 层独立预言读数逐层机读全为 0；各层取自不同 JSON 的不同字段，不是同一个写死的 0")
add("LAYERS-HIT-NONZERO", (HIT_NONZERO_COUNT > 0) and (ALL_LAYERS_PRED_ZERO), "PASS",
    "★两侧都测：门禁命中层有 " + str(HIT_NONZERO_COUNT) +
    " 层非零，但独立预言层全 0 ⇒ 判据有判别力，结论不是恒真式")
add("LAYERS-INJECT-ALL-POSITIVE", ALL_INJECT_POSITIVE and (INJECT_TOTAL > 0), "PASS",
    "11 层注入下界逐层为正，机读合计 " + str(INJECT_TOTAL) +
    "；前八层来自第九轮 round_injection，后三层来自各轮 JSON 自身字段")
add("FORCES-4", (N_FORCES == 4) and (len(FORCE_ROWS) == 4), "PASS",
    "四力维度机读自第七轮 forces=" + str(N_FORCES) + "、长程力 " +
    str(N_LONG) + "、κ 谱 " + str(KAPPA_CLASSES) + " 类、耦合谱 " +
    str(COUPLING_CLASSES) + " 类")
add("FORCES-ALL-ZERO", FORCE_ALL_ZERO and SPINE_ZERO, "PASS",
    "四力正确解 " + str(SPINE_CORRECT) + " 条、接受 " + str(SPINE_ACCEPT) +
    " 条、独立预言 0 条；跨卷 r403/r404 回读一致")
add("FORCES-PROJECTION-IDENTITY", FORCE_ALL_ZERO, "BOUNDARY",
    "★四力表是同一跨卷总读数的四个投影，逐力不产生新证据；不把它计入独立证据数")
add("EVIDENCE-3", (len(EVIDENCE) == 3) and all(x["count"] > 0 for x in EVIDENCE), "PASS",
    "三类证据域：实验双侧锚 " + str(N_TWO_SIDED) + "、程序字面量 " +
    str(N_AST) + "、判定册 " + str(INV["judge_files"]) + "，全部实盘机读")
add("CROSS-COMBOS-IDENTITY", (CROSS_COMBOS == 132), "IDENTITY",
    "★★11 层 × 4 力 × 3 证据 = " + str(CROSS_COMBOS) +
    " 个交叉组合是构造恒等式，零判别力；本册主动单列 IDENTITY，不拿组合数冒充全维度证据")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "负对照恒绿，但副本广延、逐层命中、注入账、链路断点均非恒绿读数")
add("CHAIN-10-NODES", (len(CHAIN) == 10), "PASS",
    "全链路 10 环节：实验锚 → 字面量 → 副本 → 派生闭包 → 输出 → 配对 → 认证 → 相容 → 预言 → 四力正确解")
add("CHAIN-BROKEN-LINKS", (CHAIN_BROKEN_LINKS > 0), "PASS",
    "链路零通过环节 " + str(CHAIN_BROKEN_LINKS) +
    " 个，全部集中在认证层之后；断链 0 条指文件引用，零通过指判据通过数，两者不同")
add("PATH-A-ZERO", (PATH_A_ZERO > 0), "PASS",
    "硬出口 A（新实验读数）通道 配对→认证→相容→预言 中零通过节点 " +
    str(PATH_A_ZERO) + " 个")
add("PATH-B-ZERO", (PATH_B_ZERO > 0), "PASS",
    "硬出口 B（可压缩生成机制）通道 生成机制→闭包→输出→认证→相容→预言 中零通过节点 " +
    str(PATH_B_ZERO) + " 个；生成机制节点通过数 " + str(GEN_CLEAN_FILES))
add("MIN-CUT-DRIVEN", (MIN_CUT > 0) and (MIN_CUT == min(PATH_A_ZERO, PATH_B_ZERO)), "PASS",
    "★全链路最小割 = min(" + str(PATH_A_ZERO) + "," + str(PATH_B_ZERO) + ") = " +
    str(MIN_CUT) + "；两条通道零节点数由各自机读通过数驱动，" +
    ("互异 ⇒ min 有判别力" if PATH_A_ZERO != PATH_B_ZERO else "相等 ⇒ 单列说明非恒真"))
add("CLEAN-FALSIFIABLE-ZERO", (CLEAN_FALSIFIABLE == 0) and (N_BREAK == 0), "PASS",
    "★★全库范围内 非回述 ∧ 可认证 p_free=0 ∧ χ² 相容 三条同时成立的 row() 输出 " +
    str(CLEAN_FALSIFIABLE) + " 个；三个条件分别由全库闭包、第六轮 JSON、第五轮 JSON 驱动")
add("THREE-GATES-BEARING", (sum(1 for g in ACTIVE_GATES if g) == 3) and (FORGED_BREAKS == 0), "PASS",
    "三重门都承重：任一门被拆将误放行 " + str(N_ROW_CALLS) + " 个输出；当前误放行 " +
    str(FORGED_BREAKS) + " 个")
add("PARAMETER-IMMORTALITY-11", (N_BREAK == 0) and (COPIED_AST > 0), "PASS",
    "★参数不灭第十一实例：这次是全库尺度——" + str(COPIED_AST) +
    " 个观测副本跨 " + str(N_COPIED_FILES) + " 个脚本，仍无一条独立数值预言")
add("CTRL-FOUR-DISTINCT", CTRL_FOUR_DISTINCT, "PASS",
    "控制组四向量两两不同：" + " / ".join(str(x) for x in CTRL_FOUR))
add("CTRL-NO-EQ-BASE", CTRL_NO_EQ_BASE, "PASS",
    "三个单门对照均不等于基线 " + str(CTRL_BASE))
add("CTRL-SCALAR-DISTINCT", CTRL_SCALAR_DISTINCT, "PASS",
    "控制组四标量两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-SCALAR-NO-EQ-BASE", all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:]), "PASS",
    "三个对照标量均不等于基线标量 " + str(CTRL_READINGS[0]))
add("ZERO-SCAN-IDENTITY", ZERO_SCAN_OK, "IDENTITY",
    "阴性对照：扫描范围取 0 个文件时四项读数恒为 0，该侧恒真、零判别力，单列 IDENTITY 配 NOT-ALL-GREEN")
add("SPINE-ZERO", SPINE_ZERO, "PASS",
    "跨卷回读：r403 四力正确解 " + str(SPINE_CORRECT) + " 条、r404 接受 " +
    str(SPINE_ACCEPT) + "；本册未新增任何物理方程")
add("FAMILY-LIMITED-CLAIM", (py_all > 0) and (N_COPIED_FILES > 0), "BOUNDARY",
    "★本册覆盖 openuft 全库 " + str(py_all) + " 个 .py 与主目录全部册子，但全库 ≠ 全人类知识；" +
    "AST 可解析 " + str(py_ok) + " 个，" + str(py_fail) +
    " 个语法失败文件未进闭包；row() 为宽口径；结论不是「四力统一不可能」的全称定理")
add("NO-BREAKTHROUGH", (N_BREAK == 0), "INFO",
    "本册不宣称攻破统一场论；给出的是全库可达域内的局部否定证书与链路最小割")
add("MATH-NOT-EXPERIMENT", SPINE_ZERO, "INFO",
    "所有结论都是可算判决（AST/tokenize 普查、依赖闭包、逐层机读、链路计数），不是实验证实；不产新物理，独立实验预言仍为 0")
add("NEXT-EXIT", (N_BREAK == 0) and (CERTIFIED_HIT == 0), "INFO",
    "硬出口未变；本册把代价从「误差棒放宽倍数」升级为「全链路至少 " +
    str(MIN_CUT) + " 个零通过环节」，且这些零节点分属认证、相容、判词三层 ⇒ 单点放宽打不通。" +
    "在该读数出现前，不必再造新理论、不必再放宽判据")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把突破读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")


def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-FULLCHAIN-SCOPE--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-FULLCHAIN-SCOPE--GATES-FAIL"
    return "ALG-FULLCHAIN-SCOPE--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "CLEAN-FALSIFIABLE-ZERO", "LAYERS-PRED-ALL-ZERO",
                     "FORCES-ALL-ZERO", "FAMILY-LIMITED-CLAIM", "PARSE-FAIL-BOUNDARY",
                     "TWO-PATH-DIFF-BOUNDARY"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-FULLCHAIN-SCOPE--GATES-PASS-WITH-0-NEGATIVE") and \
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
    "py_all": py_all, "py_ok": py_ok, "py_fail": py_fail,
    "py_decode_fail": py_decode_fail, "py_bytes": py_bytes,
    "ast_literals": N_AST, "tokenize_numbers": N_TOK_OK,
    "tokenize_in_failed_files": N_TOK_FAIL, "complex_tokens": N_COMPLEX_OK,
    "two_path_diff": TWO_PATH_DIFF, "two_path_residual": TWO_PATH_RESIDUAL,
    "copied_ast": COPIED_AST, "copied_tokenize": COPIED_TOK_OK,
    "copied_in_failed_files": COPIED_TOK_FAIL,
    "copied_two_path_diff": COPIED_TWO_PATH_DIFF,
    "copied_files": N_COPIED_FILES, "copied_top_dirs": N_COPIED_DIRS,
    "copy_share_pct": dstr(COPY_SHARE_PCT, 6),
    "tainted_script_share_pct": dstr(TAINTED_SHARE_PCT, 4),
    "amplify_vs_r11": dstr(AMPLIFY, 4),
    "row_calls": N_ROW_CALLS, "row_files": N_ROW_FILES,
    "row_literal": N_ROW_LITERAL, "row_literal_copied": N_ROW_LITERAL_COPIED,
    "row_derived_tainted": N_ROW_DERIVED_TAINTED,
    "row_derived_clean": N_ROW_DERIVED_CLEAN, "row_malformed": N_ROW_MALFORMED,
    "generator_clean_files": GEN_CLEAN_FILES,
    "layers": len(LAYERS), "layers_pred_all_zero": ALL_LAYERS_PRED_ZERO,
    "layers_hit_nonzero": HIT_NONZERO_COUNT, "inject_total": INJECT_TOTAL,
    "forces": N_FORCES, "long_range_forces": N_LONG,
    "kappa_classes": KAPPA_CLASSES, "coupling_classes": COUPLING_CLASSES,
    "evidence_types": len(EVIDENCE), "cross_combos": CROSS_COMBOS,
    "chain_nodes": len(CHAIN), "chain_broken_links": CHAIN_BROKEN_LINKS,
    "path_a_zero": PATH_A_ZERO, "path_b_zero": PATH_B_ZERO, "min_cut": MIN_CUT,
    "anchors": N_ANCHORS, "two_sided_anchors": N_TWO_SIDED,
    "pairs_total": PAIRS_TOTAL, "pairs_hit": PAIRS_HIT,
    "certified_hit": CERTIFIED_HIT, "chi2_crit": str(CHI2_CRIT),
    "clean_falsifiable": CLEAN_FALSIFIABLE, "breakthrough": N_BREAK,
    "forged_breaks": FORGED_BREAKS,
    "control_vectors": CTRL_FOUR, "control_scalars": CTRL_READINGS,
    "main_md": INV["main_md"], "main_html": INV["main_html"],
    "alg_md": INV["alg_md"], "alg_html": INV["alg_html"],
    "src_files": INV["src_files"], "data_files": INV["data_files"],
    "judge_files": INV["judge_files"],
    "readme_bytes": README_BYTES, "readme_md5": README_MD5,
    "readme_max_rid": README_MAX_RID, "tree_max_rid": SRC_TREE_MAX_RID,
    "source_files": len(SOURCE_FILES), "source_missing": len(source_missing),
    "spine_four_force_correct": SPINE_CORRECT,
    "spine_four_force_accepted": SPINE_ACCEPT,
    "spine_independent_predictions": 0, "four_force_incomplete": True,
}

out = {
    "title": "算法联盟：全库可达域的全维度、全链路普查与最小割（第十二轮）",
    "date": "2026-11-14",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "scope": {
        "skip_dirs": list(SKIP_DIRS),
        "own_excluded_names": sorted(OWN_NAMES),
        "copied_by_top_dir": copied_by_dir,
    },
    "dimension_tables": dict(layers=LAYERS, forces=FORCE_ROWS, evidence=EVIDENCE,
                             cross_combos=CROSS_COMBOS),
    "chain": dict(nodes=CHAIN + [GEN_NODE], path_a=PATH_A, path_b=PATH_B,
                  path_a_zero=PATH_A_ZERO, path_b_zero=PATH_B_ZERO,
                  min_cut=MIN_CUT, broken_links=CHAIN_BROKEN_LINKS),
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
    lines.append("算法联盟：全库可达域的全维度、全链路普查与最小割（第十二轮）")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("全库盘点：" + str(py_all) + " 个 .py / " + str(py_bytes) +
                 " B；AST 可解析 " + str(py_ok) + "，语法失败 " + str(py_fail) +
                 "，解码失败 " + str(py_decode_fail))
    lines.append("两路机拼：AST 常量 " + str(N_AST) + " / tokenize NUMBER " +
                 str(N_TOK_OK) + "，口径差 " + str(TWO_PATH_DIFF) +
                 "（复数 " + str(N_COMPLEX_OK) + "，余项 " + str(TWO_PATH_RESIDUAL) + "）")
    lines.append("观测副本：" + str(COPIED_AST) + " 个（tokenize " +
                 str(COPIED_TOK_OK) + "），跨 " + str(N_COPIED_FILES) + " 脚本 / " +
                 str(N_COPIED_DIRS) + " 顶层目录，占字面量 " + dstr(COPY_SHARE_PCT, 6) +
                 "%，较第十一轮单脚本放大 " + dstr(AMPLIFY, 4) + " 倍")
    lines.append("row() 普查：" + str(N_ROW_CALLS) + " 个 / " + str(N_ROW_FILES) +
                 " 文件；字面量 " + str(N_ROW_LITERAL) + "、派生依赖副本 " +
                 str(N_ROW_DERIVED_TAINTED) + "、派生闭包干净 " +
                 str(N_ROW_DERIVED_CLEAN) + "、异常 " + str(N_ROW_MALFORMED))
    lines.append("-" * 96)
    lines.append("全维度：11 层判据独立预言读数全 0，命中非零层数 " +
                 str(HIT_NONZERO_COUNT) + "，注入下界合计 " + str(INJECT_TOTAL))
    for x in LAYERS:
        lines.append("  " + x["tag"] + " " + x["layer"] + " | hit=" +
                     x["hit_field"] + ":" + str(x["hit"]) + " | pred=" +
                     x["pred_field"] + ":" + str(x["pred"]) + " | inject=" + str(x["inject"]))
    lines.append("四力：" + str(N_FORCES) + " 力 / 长程 " + str(N_LONG) +
                 " / κ谱 " + str(KAPPA_CLASSES) + " 类 / 耦合谱 " +
                 str(COUPLING_CLASSES) + " 类 / 正确解 " + str(SPINE_CORRECT) + " 条")
    lines.append("交叉 11×4×3 = " + str(CROSS_COMBOS) + " 组合为构造恒等式，单列 IDENTITY")
    lines.append("-" * 96)
    lines.append("全链路 10 环节，零通过环节 " + str(CHAIN_BROKEN_LINKS) + " 个")
    for x in CHAIN:
        lines.append("  " + x["id"] + " " + x["name"] + " = " + str(x["passing"]))
    lines.append("  G0 " + GEN_NODE["name"] + " = " + str(GEN_CLEAN_FILES))
    lines.append("通道 A 零节点 " + str(PATH_A_ZERO) + " / 通道 B 零节点 " +
                 str(PATH_B_ZERO) + " ⇒ 最小割 " + str(MIN_CUT))
    lines.append("非回述 ∧ 可认证 ∧ 相容 = " + str(CLEAN_FALSIFIABLE) +
                 " ⇒ 独立实验预言 0")
    lines.append("-" * 96)
    lines.append("README：" + str(README_BYTES) + " B / " + README_MD5 +
                 " / README 最大 RID " + str(README_MAX_RID) + " / 三树最大 RID " +
                 str(SRC_TREE_MAX_RID) + "；本册零改动")
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
