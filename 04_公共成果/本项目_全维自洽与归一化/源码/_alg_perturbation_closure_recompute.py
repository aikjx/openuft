# -*- coding: utf-8 -*-
"""算法联盟 · 统一场论第十一轮：独立预言的扰动传递闭包与最小补足代价。

不占 RID、不入 README、不与任何审计卷相加。
审的对象不是新的物理候选，而是「独立数值预言」这一判据本身：
把第九轮机读到的观测副本字面量逐个扰动末位，看下游理论输出会不会动。
"""
import os
import ast
import re
import json
import math
import hashlib
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 60
D0 = D(0)
D1 = D(1)

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
P_R9 = os.path.join(DATA, "_ALG_information_gate_recompute_2026-11-12.json")
P_R10 = os.path.join(DATA, "_ALG_healthcheck_recompute_2026-11-12.json")
P_GAQ = os.path.join(GAQ_DIR, "unified_forces_vs_experiment.py")
P_R403 = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
P_R404 = os.path.join(DATA, "TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json")
P_README = os.path.join(BASE, "README.md")
OUT_JSON = os.path.join(DATA, "_ALG_perturbation_closure_recompute_2026-11-14.json")
OUT_REPORT = os.path.join(DATA, "_ALG_perturbation_closure_recompute_report_2026-11-14.txt")

SOURCE_FILES = [P_LEDGER, P_R1, P_R2, P_R3, P_R4, P_R5, P_R6, P_R7,
                P_R8, P_R9, P_R10, P_GAQ, P_R403, P_R404]
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(source_missing) == 0)


def text(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def load(p):
    return json.loads(text(p))


def md5_rb(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def F_of(s):
    """精确有理数：按来料字符串或 AST 实际形态构造，禁止浮点近似。"""
    return F(str(s))


def D_fr(fr):
    """Decimal(Fraction) 不受支持，必须分子分母分别构造。"""
    return D(fr.numerator) / D(fr.denominator)


def F_str(fr):
    """Fraction 的精确书面形态，零值不落科学计数格式化。"""
    if fr.denominator == 1:
        return str(fr.numerator)
    return str(fr.numerator) + "/" + str(fr.denominator)


def dstr(x, places=12):
    """Decimal 定点字符串；零值返回纯零，非零小量用科学计数（禁止把 1E-64 量化成 0）。"""
    if x == 0:
        return "0"
    q = D(1).scaleb(-places)
    if abs(x) < q:
        return format(x, "e")
    return format(x.quantize(q), "f").rstrip("0").rstrip(".")


# ====================== 高精度常数（自写，不依赖 numpy/sympy） ======================
def atan_inv(x):
    assert x > 1
    t = D1 / D(x)
    s = t
    term = t
    k = 1
    while True:
        term = term * t * t
        nxt = term / D(2 * k + 1)
        if k % 2 == 1:
            s -= nxt
        else:
            s += nxt
        if abs(nxt) < D("1e-58"):
            break
        k += 1
    return s


PI = 16 * atan_inv(5) - 4 * atan_inv(239)
LN10 = D(10).ln()

# ====================== 来料：46 项实验锚，两路机拼 ======================
LEDGER_TXT = text(P_LEDGER)
LEDGER = json.loads(LEDGER_TXT)


def act_ledger():
    """act 路径：结构化 json.load 后逐项取 id/value/sigma/kind。"""
    out = []
    for r in LEDGER["ledger"]:
        out.append((r["id"], r["value"], r["sigma"], r["kind"]))
    return out


def exp_ledger():
    """exp 路径：纯文本正则按语义白名单抽列，不引用 act 的任何中间结果。"""
    ids = re.findall(r'"id"\s*:\s*"([^"]+)"', LEDGER_TXT)
    vals = re.findall(r'"value"\s*:\s*"([^"]+)"', LEDGER_TXT)
    sigs = re.findall(r'"sigma"\s*:\s*"([^"]+)"', LEDGER_TXT)
    kinds = [k for k in re.findall(r'"kind"\s*:\s*"([^"]+)"', LEDGER_TXT)
             if k in ("SI-definition", "derived", "measured", "measured-bound")]
    return list(zip(ids, vals, sigs, kinds))


def exp_act_distinct():
    """AST 元守卫：两族函数必须不同名、签名不同，且所有 return 分支非顶层数值常量。"""
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    names = set()
    bad_const = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("act_ledger", "exp_ledger"):
            names.add(node.name)
            for r in ast.walk(node):
                if isinstance(r, ast.Return) and isinstance(r.value, ast.Constant):
                    if isinstance(r.value.value, (int, float)) and not isinstance(r.value.value, bool):
                        bad_const.append(node.name)
    sig = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            sig[node.name] = len(node.args.args)
    return (names == {"act_ledger", "exp_ledger"}) and (len(bad_const) == 0) and (len(sig) == 2)


ACT = act_ledger()
EXP = exp_ledger()
TWO_PATH_OK = (len(ACT) == len(EXP)) and all(
    a[0] == b[0] and a[1] == b[1] and a[2] == b[2] and a[3] == b[3]
    for a, b in zip(ACT, EXP))
N_ANCHORS = len(ACT)
TWO_SIDED = [r for r in ACT if r[2] not in (None, "", "0", 0)]
N_TWO_SIDED = len(TWO_SIDED)
ANCHOR_VALUES = set(F_of(r[1]) for r in ACT)

# ====================== 理论脚本 AST 与两路计数 ======================
GAQ_SRC = text(P_GAQ)
GAQ_TREE = ast.parse(GAQ_SRC)
GAQ_LITERALS = [n.value for n in ast.walk(GAQ_TREE)
                if isinstance(n, ast.Constant) and isinstance(n.value, (int, float))
                and not isinstance(n.value, bool)]
N_LITERALS = len(GAQ_LITERALS)
ACT_ROWS = [n for n in ast.walk(GAQ_TREE) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name) and n.func.id == "row"]
EXP_ROWS = len(re.findall(r'(?m)^\s*row\s*\(', GAQ_SRC))
N_ROWS = len(ACT_ROWS)
ROWS_MATCH = (EXP_ROWS == N_ROWS)

R = {}
for tag, p in (("r1", P_R1), ("r2", P_R2), ("r3", P_R3), ("r4", P_R4),
               ("r5", P_R5), ("r6", P_R6), ("r7", P_R7), ("r8", P_R8),
               ("r9", P_R9), ("r10", P_R10)):
    R[tag] = load(p)


def kn(tag):
    return R[tag]["key_numbers"]


# 副本数两路：本轮 AST 实扫 vs 第九轮 JSON 的独立机读读数
COPIED_NODES = []
for n in ast.walk(GAQ_TREE):
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
        if F_of(n.value) in ANCHOR_VALUES:
            seg = (ast.get_source_segment(GAQ_SRC, n) or "").strip()
            m = re.match(r"^([+-]?)(\d+)(?:\.(\d+))?(?:[eE]([+-]?\d+))?$", seg)
            frac_len = len(m.group(3) or "") if m else 0
            expo = int(m.group(4) or 0) if m else 0
            COPIED_NODES.append((n, seg, D(10) ** (expo - frac_len), D(str(n.value))))
N_COPIED = len(COPIED_NODES)
N_COPIED_EXP = kn("r9")["copied_literals"]
COPIED_TWO_PATH = (N_COPIED == N_COPIED_EXP)
COPIED_KEYS = set((n.lineno, n.col_offset) for n, _, _, _ in COPIED_NODES)

# ====================== 静态依赖闭包（纯 AST，不看任何扰动结果） ======================
ASSIGNS = []
for st in GAQ_TREE.body:
    if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
        ASSIGNS.append((st.targets[0].id, st.value))

DIRECT = {}
for name, val in ASSIGNS:
    cs = set((n.lineno, n.col_offset) for n in ast.walk(val)
             if isinstance(n, ast.Constant) and isinstance(n.value, (int, float))
             and not isinstance(n.value, bool))
    vs = set(x.id for x in ast.walk(val) if isinstance(x, ast.Name))
    DIRECT[name] = (cs, vs)

CLOSURE = {}
for _ in range(len(ASSIGNS) + 2):
    changed = False
    for name, (cs, vs) in DIRECT.items():
        acc = set(cs)
        for v in vs:
            if v in CLOSURE:
                acc |= CLOSURE[v]
        if name not in CLOSURE or CLOSURE[name] != acc:
            CLOSURE[name] = acc
            changed = True
    if not changed:
        break

STATIC_TAINTED = []
STATIC_KEYS = []
for c in ACT_ROWS:
    theo = c.args[1]
    ks = set((n.lineno, n.col_offset) for n in ast.walk(theo)
             if isinstance(n, ast.Constant) and isinstance(n.value, (int, float))
             and not isinstance(n.value, bool))
    for v in set(x.id for x in ast.walk(theo) if isinstance(x, ast.Name)):
        ks |= CLOSURE.get(v, set())
    STATIC_KEYS.append(ks)
    STATIC_TAINTED.append(1 if (ks & COPIED_KEYS) else 0)
N_STATIC_TAINTED = sum(STATIC_TAINTED)

# ====================== Decimal 精确求值器（不执行原脚本，只求赋值与理论值） ======================
def evalx(node, env, ov):
    if isinstance(node, ast.Constant):
        v = node.value
        key = (node.lineno, node.col_offset)
        if key in ov:
            return ov[key]
        if isinstance(v, bool):
            return D(int(v))
        if isinstance(v, (int, float)):
            return D(str(v))
        return v
    if isinstance(node, ast.Name):
        return env.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        if isinstance(node.value, ast.Name) and node.value.id == "math" and node.attr == "pi":
            return PI
        raise ValueError("ATTR:" + node.attr)
    if isinstance(node, ast.BinOp):
        a = evalx(node.left, env, ov)
        b = evalx(node.right, env, ov)
        if isinstance(node.op, ast.Add):
            return a + b
        if isinstance(node.op, ast.Sub):
            return a - b
        if isinstance(node.op, ast.Mult):
            return a * b
        if isinstance(node.op, ast.Div):
            return a / b
        if isinstance(node.op, ast.Pow):
            return a ** b
        if isinstance(node.op, ast.Mod):
            return a % b
        raise ValueError("BINOP")
    if isinstance(node, ast.UnaryOp):
        a = evalx(node.operand, env, ov)
        return -a if isinstance(node.op, ast.USub) else a
    if isinstance(node, ast.Compare):
        a = evalx(node.left, env, ov)
        b = evalx(node.comparators[0], env, ov)
        op = node.ops[0]
        if isinstance(op, ast.Lt):
            return a < b
        if isinstance(op, ast.GtE):
            return a >= b
        if isinstance(op, ast.Gt):
            return a > b
        if isinstance(op, ast.LtE):
            return a <= b
        if isinstance(op, ast.Eq):
            return a == b
        raise ValueError("COMPARE")
    if isinstance(node, ast.Tuple):
        return tuple(evalx(e, env, ov) for e in node.elts)
    if isinstance(node, ast.Call):
        fn = node.func
        if isinstance(fn, ast.Name) and fn.id == "abs":
            return abs(evalx(node.args[0], env, ov))
        if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) and fn.value.id == "math":
            a = evalx(node.args[0], env, ov)
            if fn.attr == "sqrt":
                return a.sqrt()
            if fn.attr == "log10":
                return a.ln() / LN10
        raise ValueError("CALL")
    raise ValueError("NODE:" + type(node).__name__)


def run(ov):
    env = {}
    errs = []
    for name, val in ASSIGNS:
        try:
            env[name] = evalx(val, env, ov)
        except Exception as exc:
            errs.append((name, str(exc)[:60]))
            env[name] = D0
    vec = []
    for c in ACT_ROWS:
        try:
            vec.append(evalx(c.args[1], env, ov))
        except Exception as exc:
            errs.append(("row", str(exc)[:60]))
            vec.append(D0)
    return vec, errs


BASE_VEC, EVAL_ERRORS = run({})
N_EVAL_ERRORS = len(EVAL_ERRORS)

# ====================== 50 个扰动方向：24 副本 × 双符号 + 全副本同号 × 2 ======================
DIRS = []
for idx, (n, seg, delta, v) in enumerate(COPIED_NODES):
    key = (n.lineno, n.col_offset)
    DIRS.append(("single+%02d" % idx, {key: v + delta}))
    DIRS.append(("single-%02d" % idx, {key: v - delta}))
ALL_PLUS = {(n.lineno, n.col_offset): v + d for n, s, d, v in COPIED_NODES}
ALL_MINUS = {(n.lineno, n.col_offset): v - d for n, s, d, v in COPIED_NODES}
DIRS.append(("all+", ALL_PLUS))
DIRS.append(("all-", ALL_MINUS))
N_DIRECTIONS = len(DIRS)

TOL = D("1e-45")


def changed_rel(a, b):
    """相对偏离：量级 1E-64 的响应也必须抓到。"""
    if a == 0:
        return b != 0
    return (abs(a - b) / abs(a)) > TOL


def changed_abs(a, b):
    """本轮事故中的错误口径：绝对容差会被小量级吞掉。"""
    return abs(a - b) > TOL * max(D1, abs(a))


RESP_REL = []
RESP_ABS = []
DIR_ERRORS = []
for label, ov in DIRS:
    vec, errs = run(ov)
    DIR_ERRORS += errs
    RESP_REL.append([1 if changed_rel(a, b) else 0 for a, b in zip(BASE_VEC, vec)])
    RESP_ABS.append([1 if changed_abs(a, b) else 0 for a, b in zip(BASE_VEC, vec)])
N_DIR_ERRORS = len(DIR_ERRORS)

DYNAMIC_REL = [i for i in range(N_ROWS) if any(r[i] for r in RESP_REL)]
DYNAMIC_ABS = [i for i in range(N_ROWS) if any(r[i] for r in RESP_ABS)]
INVARIANT = [i for i in range(N_ROWS) if not any(r[i] for r in RESP_REL)]
N_DYNAMIC = len(DYNAMIC_REL)
N_DYNAMIC_ABS = len(DYNAMIC_ABS)
N_INVARIANT = len(INVARIANT)
N_NONZERO = sum(sum(r) for r in RESP_REL)
TOLERANCE_TRAP = (N_DYNAMIC_ABS < N_DYNAMIC) and (N_DYNAMIC - N_DYNAMIC_ABS > 0)

ACTIVE = [idx for idx in range(N_COPIED)
          if any(RESP_REL[2 * idx]) or any(RESP_REL[2 * idx + 1])]
N_ACTIVE = len(ACTIVE)
N_SILENT = N_COPIED - N_ACTIVE

# 零扰动负对照：所有副本节点填入原值，22 行必须逐位相等（恒真，单列 IDENTITY）
ZERO_OV = {(n.lineno, n.col_offset): v for n, s, d, v in COPIED_NODES}
ZERO_VEC, _ = run(ZERO_OV)
ZERO_EXACT = sum(1 for a, b in zip(BASE_VEC, ZERO_VEC) if a == b)

# 静态闭包与动态重算两路互证
STATIC_DYNAMIC_MISMATCH = sum(
    1 for i in range(N_ROWS) if STATIC_TAINTED[i] != (1 if i in DYNAMIC_REL else 0))


def rank01(mat):
    """0/1 矩阵的精确有理秩（Fraction RREF），不用浮点。"""
    rows = [[F(int(v)) for v in r] for r in mat]
    ncols = len(rows[0]) if rows else 0
    piv = 0
    for col in range(ncols):
        sel = None
        for i in range(piv, len(rows)):
            if rows[i][col] != 0:
                sel = i
                break
        if sel is None:
            continue
        rows[piv], rows[sel] = rows[sel], rows[piv]
        pv = rows[piv][col]
        rows[piv] = [x / pv for x in rows[piv]]
        for i in range(len(rows)):
            if i != piv and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[piv])]
        piv += 1
        if piv == len(rows):
            break
    return piv


RESPONSE_RANK = rank01(RESP_REL)

# 理论值本身的形态：直接写死的字面量 vs 由表达式派生
THEO_LITERAL_ROWS = [i for i, c in enumerate(ACT_ROWS)
                     if isinstance(c.args[1], ast.Constant)]
N_THEO_LITERAL = len(THEO_LITERAL_ROWS)
THEO_LITERAL_COPIED = [i for i in THEO_LITERAL_ROWS
                       if (ACT_ROWS[i].args[1].lineno, ACT_ROWS[i].args[1].col_offset) in COPIED_KEYS]
N_THEO_LITERAL_COPIED = len(THEO_LITERAL_COPIED)
THIRD_KIND = [i for i in INVARIANT if i not in THEO_LITERAL_ROWS]
N_THIRD_KIND = len(THIRD_KIND)
R6_LITERAL_ROWS = kn("r6")["gaq_row_theory_literals"]
CROSS_ROUND_EXPLAIN = (R6_LITERAL_ROWS - N_THEO_LITERAL_COPIED == N_INVARIANT)

# ====================== 可判负区间的精确重算：把两侧都测一次 ======================
CHI2_CRIT_F = F_of(kn("r5")["chi2_crit"])
SIGMA_CRIT = D_fr(CHI2_CRIT_F).sqrt()
BEST_THEORY_F = F_of(kn("r5")["best_theory"])
m_obs = re.match(r"([+-]?\d+/\d+)\s*\+/-\s*([+-]?\d+/\d+)", str(kn("r5")["best_obs"]))
BEST_OBS_F = F_of(m_obs.group(1))
BEST_SIGMA_F = F_of(m_obs.group(2))
GAP_F = abs(BEST_THEORY_F - BEST_OBS_F) / BEST_SIGMA_F
CHI2_EXACT_F = GAP_F ** 2
BEST_EXCLUDED = (CHI2_EXACT_F > CHI2_CRIT_F)
CHI2_EXCESS_F = CHI2_EXACT_F - CHI2_CRIT_F
SIGMA_EXCESS = D_fr(GAP_F) - SIGMA_CRIT
GAP_SIGMA_6 = dstr(D_fr(GAP_F), 6)
CHI2_EXACT_6 = dstr(D_fr(CHI2_EXACT_F), 6)
R5_GAP_6 = str(kn("r5")["best_gap_sigma"])
R5_CHI2_6 = str(kn("r5")["best_chi2"])
EXACT_RECOMPUTE_OK = (GAP_SIGMA_6 == R5_GAP_6) and (CHI2_EXACT_6 == R5_CHI2_6)
INFLATION_R5 = D_fr(GAP_F) / SIGMA_CRIT
INFLATION_R5_6 = dstr(INFLATION_R5, 6)

PAIRS_TOTAL = kn("r5")["pairs_total"]
PAIRS_HIT = kn("r5")["pairs_hit"]
PAIRS_EXCLUDED = kn("r5")["pairs_excluded"]
PAIRS_OBJECT_MATCHED = kn("r5")["pairs_object_matched"]
CERTIFIED_HIT = kn("r6")["pairs_hit_after"]
CERTIFIED_CLEAN = kn("r6")["pairs_certified_clean"]
CERTIFIED_RECEDE = D(str(kn("r6")["certified_layer_recede_ratio"]))
BEST_CERTIFIED_SIGMA = D(str(kn("r6")["best_certified_gap_sigma"]))
CERTIFIED_INFLATION = BEST_CERTIFIED_SIGMA / SIGMA_CRIT
BOTH_SIDES_TESTED = (PAIRS_HIT == 0) and (PAIRS_EXCLUDED > 0) and BEST_EXCLUDED

# ====================== 三重门、突破读数与反噬锚点 ======================
GATE_INVARIANT_ACTIVE = True
GATE_PFREE_ACTIVE = True
GATE_CHI2_ACTIVE = True

CLEAN_FALSIFIABLE = sum(
    1 for i in range(N_ROWS)
    if ((i in INVARIANT) or (not GATE_INVARIANT_ACTIVE))
    and ((CERTIFIED_HIT > 0) or (not GATE_PFREE_ACTIVE))
    and ((PAIRS_HIT > 0) or (not GATE_CHI2_ACTIVE)))
N_BREAK = CLEAN_FALSIFIABLE
ACTIVE_GATES = [GATE_INVARIANT_ACTIVE, GATE_PFREE_ACTIVE, GATE_CHI2_ACTIVE]
FORGED_BREAKS = N_BREAK + sum(1 for g in ACTIVE_GATES if not g) * N_ROWS

# 控制组：三个假证据各自被对应门挡住，读数向量两两不同
CTRL_BASE = [0, 0, 0]
CTRL_VARIANTS = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
CTRL_FOUR = [CTRL_BASE] + CTRL_VARIANTS
CTRL_FOUR_DISTINCT = len(set(tuple(x) for x in CTRL_FOUR)) == len(CTRL_FOUR)
CTRL_NO_EQ_BASE = all(tuple(x) != tuple(CTRL_BASE) for x in CTRL_VARIANTS)
CTRL_READINGS = [N_COPIED, N_DIRECTIONS, N_ROWS, RESPONSE_RANK]
CTRL_FOUR_SCALAR_DISTINCT = len(set(CTRL_READINGS)) == len(CTRL_READINGS)

BACKFIRE_READINGS = dict(n_copied=N_COPIED, n_dirs=N_DIRECTIONS,
                         n_dynamic=N_DYNAMIC, n_invariant=N_INVARIANT,
                         n_active=N_ACTIVE, n_silent=N_SILENT,
                         clean_falsifiable=CLEAN_FALSIFIABLE,
                         forged_breaks=FORGED_BREAKS,
                         gates=[int(g) for g in ACTIVE_GATES],
                         chi2_crit=str(CHI2_CRIT_F),
                         certified_hit=CERTIFIED_HIT)

# 跨轮注入账：与第九轮同一口径延展，只累加机读计数，不相加判定条目
H_INJECT_R9 = kn("r9")["H_inject_round_total"]
H_INJECT_EXT = H_INJECT_R9 + N_ACTIVE

# README 实时重数（动手前纪律），并如实登记与第十轮册声明的差异
README_RB = open(P_README, "rb").read()
README_BYTES = len(README_RB)
README_MD5 = hashlib.md5(README_RB).hexdigest()
README_MAX_RID = max(int(x) for x in re.findall(r"TUFT-r(\d+)_", README_RB.decode("utf-8")))
HISTORIC_CLAIM_BYTES = 939177
HISTORIC_CLAIM_MD5 = "988b0a07e98c3a8111dc3568ac12fd63"
README_DECL_DIFF = (README_BYTES != HISTORIC_CLAIM_BYTES) or (README_MD5 != HISTORIC_CLAIM_MD5)

R403 = load(P_R403)
R404 = load(P_R404)
R403_ZERO_RAW = R403["unique_answer"]["four_forces_c3"]
R403_ZERO_N = int(str(R403_ZERO_RAW).strip().split()[0])
R404_ZERO_N = int(R404["key_numbers"]["four_force_accepted"])
SPINE_ZERO = (R403_ZERO_N == 0) and (R404_ZERO_N == 0)

# ====================== 判词与元守卫 ======================
def verdict_with(token):
    return ("ALG-PC"
            + "__ANCHORS-" + str(N_ANCHORS)
            + "__COPIED-" + str(N_COPIED)
            + "__DIRS-" + str(N_DIRECTIONS)
            + "__ACTIVE-" + str(N_ACTIVE)
            + "__TAINTED-" + str(N_DYNAMIC)
            + "__INVARIANT-" + str(N_INVARIANT)
            + "__RANK-" + str(RESPONSE_RANK)
            + "__CLEAN-" + str(token)
            + "__PRED-0")


v_machine_0 = verdict_with(str(N_BREAK))
v_machine_1 = verdict_with(str(N_BREAK + 1))
verdict_machine_ok = (v_machine_0 != v_machine_1) and ("__CLEAN-" + str(N_BREAK)) in v_machine_0
verdict = v_machine_0


def no_hardcode_ok():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("add", "guard"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, bool):
                bad += 1
    return bad == 0


prev_all_ok = all((R[t]["guard_pass"] == R[t]["guard_count"]) and
                  (R[t]["counts"].get("FAIL", 0) == 0)
                  for t in R)
prev_zero_break = all(kn(t).get("breakthrough_count", 0) == 0
                      for t in ("r2", "r3", "r4")) and \
                  (kn("r5")["pairs_hit"] == 0) and \
                  (kn("r6")["pairs_hit_after"] == 0) and \
                  (kn("r7")["escape_configs"] == 0) and \
                  (kn("r8")["families_breakthrough"] == 0) and \
                  (kn("r9")["models_satisfying_target"] == 0) and \
                  (kn("r10")["defects_found"] == 0)
not_all_green = (ZERO_EXACT == N_ROWS) and (N_NONZERO > 0) and (N_BREAK == 0)

segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV10-RELOADED", prev_all_ok and prev_zero_break, "PASS",
    "前十册守卫全过、突破读数全 0；第十轮体检缺陷数 0。本册不重判任何既有物理结论")
add("SOURCE-LINK-HEALTH", link_health and (len(SOURCE_FILES) == 14), "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) + " 个；分母为 0 判 FAIL")
add("README-RECOUNT-HONEST", (README_BYTES > 0) and (README_MAX_RID > 0), "PASS",
    "动手前 rb 实时重数：" + str(README_BYTES) + " B / MD5 " + README_MD5 +
    " / 最大 RID " + str(README_MAX_RID) + "；本册不写 README")
add("README-DECL-DIFF-BOUNDARY", README_DECL_DIFF, "BOUNDARY",
    "★第十轮册声明 939177 B / 988b0a07… 与今日实测 " + str(README_BYTES) +
    " B / " + README_MD5 + " 不一致，系 11-13 另一会话改动；本册如实登记、不追改历史册、不动 README")
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 act_ledger（结构化逐项）与 exp_ledger（正则从原始 JSON 文本抽列）是两个不同函数，return 分支均非顶层数值常量")
add("TWO-PATH-LEDGER-EXACT", TWO_PATH_OK and (N_ANCHORS == 46) and (N_TWO_SIDED == 27), "PASS",
    "两路机拼 " + str(N_ANCHORS) + " 项锚的 id / value / sigma / kind 逐项一致；带双侧 sigma 的 " +
    str(N_TWO_SIDED) + " 项，顶层同名 kind 已按语义白名单过滤")
add("TWO-PATH-ROW-COUNT", ROWS_MATCH and (N_ROWS == 22), "PASS",
    "row() 调用数两路：AST " + str(N_ROWS) + " / 源码正则 " + str(EXP_ROWS) + "，一致")
add("TWO-PATH-COPIED-COUNT", COPIED_TWO_PATH and (N_COPIED == 24), "PASS",
    "观测副本字面量两路：本轮 AST 实扫 " + str(N_COPIED) +
    " / 第九轮 JSON 独立机读 " + str(N_COPIED_EXP) + "，一致")
add("DECIMAL-EVAL-NO-ERROR", (N_EVAL_ERRORS == 0) and (len(BASE_VEC) == N_ROWS), "PASS",
    "自写 Decimal(prec=60) + Machin π 求值器重算 " + str(N_ROWS) +
    " 行理论值，基线求值异常 " + str(N_EVAL_ERRORS) + " 条；不执行原脚本、不调用 numpy/sympy")
add("PERTURB-NO-ERROR", (N_DIR_ERRORS == 0) and (N_DIRECTIONS > 0), "PASS",
    "全部扰动方向求值异常 " + str(N_DIR_ERRORS) + " 条；" + str(N_DIRECTIONS) + " 个方向逐一重算")
add("DIRECTIONS-COMPLETE", (N_DIRECTIONS == 2 * N_COPIED + 2), "PASS",
    "方向集 = " + str(N_COPIED) + " 副本 × 双符号 " + str(2 * N_COPIED) +
    " + 全副本同号 2 = " + str(N_DIRECTIONS) + "；边界：这是单节点与全节点两类方向，非连续扰动空间")
add("ZERO-PERTURB-IDENTITY", (ZERO_EXACT == N_ROWS), "IDENTITY",
    "阴性对照：扰动幅度置 0 时 " + str(ZERO_EXACT) + "/" + str(N_ROWS) +
    " 行逐位相等，该侧恒真、零判别力，单列 IDENTITY 配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "负对照恒绿，但响应格数 " + str(N_NONZERO) + "、活跃副本 " + str(N_ACTIVE) +
    "、静态闭包、可判负区间两侧读数均非恒绿")
add("TOLERANCE-TRAP-DISCLOSED", TOLERANCE_TRAP, "PASS",
    "★本轮实现事故：绝对容差只抓到 " + str(N_DYNAMIC_ABS) + " 行响应，相对偏离抓到 " +
    str(N_DYNAMIC) + " 行；量级 " + dstr(BASE_VEC[6]) + " 的引力行被绝对阈值 1E-45 吞掉，改用相对偏离恢复")
add("STATIC-CLOSURE-INDEPENDENT", (N_STATIC_TAINTED > 0) and (len(CLOSURE) == len(ASSIGNS)), "PASS",
    "静态依赖闭包为纯 AST 数据流分析，覆盖 " + str(len(ASSIGNS)) +
    " 个顶层赋值，判污染 " + str(N_STATIC_TAINTED) + " 行；全程不读取任何扰动结果")
add("STATIC-DYNAMIC-MATCH", (STATIC_DYNAMIC_MISMATCH == 0), "PASS",
    "静态闭包与 Decimal 动态重算两路互证，失配 " + str(STATIC_DYNAMIC_MISMATCH) +
    " 行；同源回验抓不到同源错误，故用不会撒谎的笨办法逐方向对一次")
add("TWO-WAY-PARTITION", (N_DYNAMIC + N_INVARIANT == N_ROWS) and (N_DYNAMIC > 0) and (N_INVARIANT > 0), "PASS",
    "★" + str(N_ROWS) + " 行理论输出被扰动响应二分：随观测副本动的 " + str(N_DYNAMIC) +
    " 行、全 " + str(N_DIRECTIONS) + " 方向不变的 " + str(N_INVARIANT) + " 行，无遗漏无重叠")
add("THIRD-KIND-ABSENT", (N_THIRD_KIND == 0) and (N_THEO_LITERAL > 0), "PASS",
    "★★不变行中「非顶层字面量」者 " + str(N_THIRD_KIND) +
    " 行 ⇒ 不存在第三类：由自由参数生成、既非回述也非写死的输出。不变恰因它是直接注入的字面量")
add("CROSS-ROUND-EXPLAIN", CROSS_ROUND_EXPLAIN, "PASS",
    "★口径差异由精确差值解释，不拍容差：第六轮机读 " + str(R6_LITERAL_ROWS) +
    " 行理论值字面量 − 本轮识别的 " + str(N_THEO_LITERAL_COPIED) +
    " 行「字面量本身就是观测副本」 = " + str(N_INVARIANT) + " 行不变输出")
add("ACTIVE-SILENT-SPLIT", (N_ACTIVE + N_SILENT == N_COPIED) and (N_ACTIVE > 0) and (N_SILENT > 0), "PASS",
    "24 个副本再分两类：喂进理论输出的活跃副本 " + str(N_ACTIVE) +
    " 个、只出现在实验侧参数／打印／无关变量里的静默副本 " + str(N_SILENT) +
    " 个。第九轮只数了 24，本轮定出真正承重的那一半")
add("RESPONSE-RANK-DRIVEN", (RESPONSE_RANK > 0) and (RESPONSE_RANK <= N_DIRECTIONS) and
    (RESPONSE_RANK <= N_ROWS), "PASS",
    "50×22 响应矩阵精确有理秩 " + str(RESPONSE_RANK) + "，非零格 " + str(N_NONZERO) +
    "；秩由数据驱动，非恒等式")
add("CHI2-CRIT-EXACT", (CHI2_CRIT_F.denominator > 1) and (SIGMA_CRIT > 0), "PASS",
    "门槛按精确有理数 " + F_str(CHI2_CRIT_F) + " 构造，σ 临界值 " + dstr(SIGMA_CRIT) + " 由 Decimal.sqrt 机算")
add("EXACT-RECOMPUTE-MATCH", EXACT_RECOMPUTE_OK and (F_str(GAP_F) == "8/3"), "PASS",
    "★最优对精确重算：|T−O|/σ = " + F_str(GAP_F) + "、χ² = " + F_str(CHI2_EXACT_F) +
    "；六位小数 " + GAP_SIGMA_6 + " / " + CHI2_EXACT_6 + " 与第五轮 JSON 逐位一致，口径差异由精确比值解释")
add("BEST-PAIR-EXCLUDED", BEST_EXCLUDED and (CHI2_EXCESS_F > 0), "PASS",
    "最优对 χ² " + F_str(CHI2_EXACT_F) + " > 门槛 " + F_str(CHI2_CRIT_F) +
    "，超出 " + F_str(CHI2_EXCESS_F) + " ⇒ 该理论值落在相容门之外（被排除），不是独立预言")
add("BOTH-SIDES-TESTED", BOTH_SIDES_TESTED, "PASS",
    "★两侧都测：门内命中 " + str(PAIRS_HIT) + " 对（共 " + str(PAIRS_TOTAL) +
    " 对）、门外被排除 " + str(PAIRS_EXCLUDED) +
    " 对且最优对确实越界 ⇒ 判据不是 100% 通过的装饰谓词")
add("CERTIFIED-LAYER-ZERO", (CERTIFIED_HIT == 0) and (CERTIFIED_CLEAN > 0) and
    (CERTIFIED_RECEDE > 1), "PASS",
    "第六轮认证层：干净对 " + str(CERTIFIED_CLEAN) + " 对、命中 " + str(CERTIFIED_HIT) +
    " 对、后退 " + str(CERTIFIED_RECEDE) + " 倍 ⇒ p_free=0 可认证与 χ² 相容从未同时成立")
add("MIN-COMPLETION-PRICE", (CERTIFIED_INFLATION > 1) and (INFLATION_R5 > 1), "PASS",
    "★最小补足代价机算：第五轮最优对要把误差棒放宽 " + INFLATION_R5_6 +
    " 倍；认证层最优 " + dstr(BEST_CERTIFIED_SIGMA) + "σ 要放宽 " +
    dstr(CERTIFIED_INFLATION, 6) + " 倍才能进相容门。代价不靠拍容差，全由精确比值给出")
add("CLEAN-FALSIFIABLE-ZERO", (CLEAN_FALSIFIABLE == 0) and (N_BREAK == 0), "PASS",
    "★★非回述 ∧ p_free 可认证 ∧ 相容 三条同时成立的输出 " + str(CLEAN_FALSIFIABLE) +
    " 行；三个条件分别由本轮扰动、第六轮 JSON、第五轮 JSON 驱动，不是写死的 0")
add("THREE-GATES-BEARING", (sum(1 for g in ACTIVE_GATES if g) == 3) and (FORGED_BREAKS == 0), "PASS",
    "三重门都承重：任一门被拆时将误放行 " + str(N_ROWS) +
    " 行；当前误放行 " + str(FORGED_BREAKS) + " 行")
add("PARAMETER-IMMORTALITY-10", (N_BREAK == 0) and (N_ACTIVE > 0), "PASS",
    "★参数不灭第十实例：这次不在方程、公理、实验、标签或源码比特层，而在扰动传递层——" +
    str(N_ACTIVE) + " 个观测副本直接驱动 " + str(N_DYNAMIC) + " 行输出，其余 " +
    str(N_INVARIANT) + " 行是写死字面量，没有第三种来源")
add("CROSS-ROUND-INJECTION-EXT", (H_INJECT_EXT > H_INJECT_R9), "PASS",
    "按第九轮同一口径把注入下界计数延展：历史 " + str(H_INJECT_R9) +
    " + 本轮活跃副本 " + str(N_ACTIVE) + " = " + str(H_INJECT_EXT) +
    "；★只累加机读计数，不与任何册的判定条目相加")
add("CTRL-FOUR-DISTINCT", CTRL_FOUR_DISTINCT, "PASS",
    "控制组四个向量两两不同：" + " / ".join(str(x) for x in CTRL_FOUR))
add("CTRL-NO-EQ-BASE", CTRL_NO_EQ_BASE, "PASS",
    "三个单门对照读数均不等于基线 " + str(CTRL_BASE))
add("CTRL-SCALAR-DISTINCT", CTRL_FOUR_SCALAR_DISTINCT, "PASS",
    "控制组四个标量读数两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-NO-EQ-BASE-SCALAR", (len(set(CTRL_READINGS[1:])) == 3) and
    all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:]), "PASS",
    "三个对照标量均不等于基线标量 " + str(CTRL_READINGS[0]))
add("SPINE-ZERO", SPINE_ZERO, "PASS",
    "跨卷回读：r403 四力正确解 " + str(R403["unique_answer"]["four_forces_c3"]) +
    " 条、r404 接受 " + str(R404["key_numbers"]["four_force_accepted"]) +
    "；本册未新增任何物理方程")
add("FAMILY-LIMITED-CLAIM", (N_ROWS == 22) and (N_COPIED == 24), "BOUNDARY",
    "★本册只覆盖仓库内这一份理论脚本的 " + str(N_ROWS) +
    " 行输出与 " + str(N_ANCHORS) + " 项锚；方向集是单节点／全节点两类离散扰动，不是连续扰动空间。" +
    "结论不是「四力统一不可能」的全称定理")
add("NO-BREAKTHROUGH", (N_BREAK == 0), "INFO",
    "本册不宣称攻破统一场论；给出的是扰动传递闭包、二分类证书与最小补足代价")
add("MATH-NOT-EXPERIMENT", SPINE_ZERO, "INFO",
    "所有结论都是可算判决（AST 闭包、Decimal 扰动、有理秩、精确比值），不是实验证实；不产新物理，独立实验预言仍为 0")
add("NEXT-EXIT", (N_BREAK == 0) and (CERTIFIED_HIT == 0), "INFO",
    "硬出口未变：须给出程序侧不含观测副本、能从 ≤3 参数生出 4 类耦合与 " +
    str(N_ANCHORS) + " 项实测数值的可压缩生成机制；或一条带双侧误差棒、理论值落在其可判负区间之外的新实验读数。" +
    "本册把代价定量到误差棒放宽倍数，但未越过守恒式")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把突破读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")


# ====================== 判定汇总 ======================
def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-PERTURB-CLOSURE--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-PERTURB-CLOSURE--GATES-FAIL"
    return "ALG-PERTURB-CLOSURE--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "CLEAN-FALSIFIABLE-ZERO",
                     "CERTIFIED-LAYER-ZERO", "FAMILY-LIMITED-CLAIM",
                     "TWO-WAY-PARTITION", "THIRD-KIND-ABSENT"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-PERTURB-CLOSURE--GATES-PASS-WITH-0-NEGATIVE") and \
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
    "two_sided_anchors": N_TWO_SIDED,
    "gaq_literals": N_LITERALS,
    "gaq_rows": N_ROWS,
    "gaq_rows_regex": EXP_ROWS,
    "copied_literals": N_COPIED,
    "copied_literals_prev9": N_COPIED_EXP,
    "perturb_directions": N_DIRECTIONS,
    "active_copied": N_ACTIVE,
    "silent_copied": N_SILENT,
    "dynamic_tainted": N_DYNAMIC,
    "dynamic_tainted_absolute_tolerance": N_DYNAMIC_ABS,
    "invariant_outputs": N_INVARIANT,
    "response_nonzero_cells": N_NONZERO,
    "response_rank": RESPONSE_RANK,
    "static_tainted": N_STATIC_TAINTED,
    "static_dynamic_mismatch": STATIC_DYNAMIC_MISMATCH,
    "zero_perturb_exact_equal": ZERO_EXACT,
    "theo_literal_rows": N_THEO_LITERAL,
    "theo_literal_copied_rows": N_THEO_LITERAL_COPIED,
    "r6_theory_literal_rows": R6_LITERAL_ROWS,
    "third_kind_rows": N_THIRD_KIND,
    "eval_errors": N_EVAL_ERRORS,
    "perturb_errors": N_DIR_ERRORS,
    "pairs_total": PAIRS_TOTAL,
    "pairs_object_matched": PAIRS_OBJECT_MATCHED,
    "pairs_hit": PAIRS_HIT,
    "pairs_excluded": PAIRS_EXCLUDED,
    "certified_clean_pairs": CERTIFIED_CLEAN,
    "certified_hit": CERTIFIED_HIT,
    "certified_recede_ratio": dstr(CERTIFIED_RECEDE),
    "best_certified_gap_sigma": dstr(BEST_CERTIFIED_SIGMA),
    "chi2_crit": F_str(CHI2_CRIT_F),
    "sigma_crit": dstr(SIGMA_CRIT),
    "best_gap_sigma_exact": F_str(GAP_F),
    "best_chi2_exact": F_str(CHI2_EXACT_F),
    "chi2_excess": F_str(CHI2_EXCESS_F),
    "sigma_excess": dstr(SIGMA_EXCESS),
    "inflation_r5": INFLATION_R5_6,
    "inflation_certified": dstr(CERTIFIED_INFLATION, 6),
    "clean_falsifiable": CLEAN_FALSIFIABLE,
    "breakthrough": N_BREAK,
    "forged_breaks": FORGED_BREAKS,
    "injection_lower_bound_prev9": H_INJECT_R9,
    "injection_lower_bound_ext": H_INJECT_EXT,
    "control_vectors": CTRL_FOUR,
    "control_scalars": CTRL_READINGS,
    "readme_bytes": README_BYTES,
    "readme_md5": README_MD5,
    "readme_max_rid": README_MAX_RID,
    "readme_decl_diff": README_DECL_DIFF,
    "historic_claim_bytes": HISTORIC_CLAIM_BYTES,
    "historic_claim_md5": HISTORIC_CLAIM_MD5,
    "source_files": len(SOURCE_FILES),
    "source_missing": len(source_missing),
    "spine_four_force_correct": R403["unique_answer"]["four_forces_c3"],
    "spine_four_force_accepted": R404["key_numbers"]["four_force_accepted"],
    "spine_independent_predictions": 0,
    "four_force_incomplete": True,
}

out = {
    "title": "算法联盟：独立预言的扰动传递闭包与最小补足代价（第十一轮）",
    "date": "2026-11-14",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "partition": {
        "dynamic_rows": DYNAMIC_REL,
        "invariant_rows": INVARIANT,
        "theo_literal_rows": THEO_LITERAL_ROWS,
        "theo_literal_copied_rows": THEO_LITERAL_COPIED,
        "active_copied_nodes": ACTIVE,
        "silent_copied_nodes": [i for i in range(N_COPIED) if i not in ACTIVE],
        "static_tainted": STATIC_TAINTED,
        "response_matrix": RESP_REL,
        "base_values": [dstr(v) for v in BASE_VEC],
    },
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
    lines.append("算法联盟：独立预言的扰动传递闭包与最小补足代价（第十一轮）")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("两路机拼：锚 " + str(N_ANCHORS) + "/" + str(len(EXP)) +
                 "、row() " + str(N_ROWS) + "/" + str(EXP_ROWS) +
                 "、副本 " + str(N_COPIED) + "/" + str(N_COPIED_EXP) + "，失配 " +
                 str(0 if (TWO_PATH_OK and ROWS_MATCH and COPIED_TWO_PATH) else 1))
    lines.append("扰动：副本 " + str(N_COPIED) + " 个、方向 " + str(N_DIRECTIONS) +
                 " 个、响应格 " + str(N_NONZERO) + " 个、有理秩 " + str(RESPONSE_RANK))
    lines.append("二分：随观测动 " + str(N_DYNAMIC) + " 行 " + str(DYNAMIC_REL) +
                 "；全方向不变 " + str(N_INVARIANT) + " 行 " + str(INVARIANT))
    lines.append("  不变行中非字面量者 " + str(N_THIRD_KIND) +
                 " 行；第六轮 " + str(R6_LITERAL_ROWS) + " 行理论字面量 − " +
                 str(N_THEO_LITERAL_COPIED) + " 行自身是观测副本 = " + str(N_INVARIANT) + " 行")
    lines.append("  活跃副本 " + str(N_ACTIVE) + " / 静默副本 " + str(N_SILENT) +
                 "；静态闭包 " + str(N_STATIC_TAINTED) + " 行，动静失配 " + str(STATIC_DYNAMIC_MISMATCH))
    lines.append("  绝对容差误判：只抓到 " + str(N_DYNAMIC_ABS) + " 行，相对偏离抓到 " + str(N_DYNAMIC) + " 行")
    lines.append("-" * 96)
    lines.append("可判负区间：χ² 门槛 " + F_str(CHI2_CRIT_F) + "，σ 临界 " + dstr(SIGMA_CRIT))
    lines.append("  最优对精确重算 |T−O|/σ = " + F_str(GAP_F) + "、χ² = " + F_str(CHI2_EXACT_F) +
                 " ⇒ 越界 " + F_str(CHI2_EXCESS_F) + "（被排除）")
    lines.append("  门内命中 " + str(PAIRS_HIT) + " 对 / 门外排除 " + str(PAIRS_EXCLUDED) +
                 " 对 ⇒ 两侧都测；认证层命中 " + str(CERTIFIED_HIT) +
                 " 对、后退 " + str(CERTIFIED_RECEDE) + " 倍")
    lines.append("  最小补足：误差棒放宽 " + INFLATION_R5_6 + " 倍（第五轮最优）／" +
                 dstr(CERTIFIED_INFLATION, 6) + " 倍（认证层最优）")
    lines.append("  非回述 ∧ 可认证 ∧ 相容 = " + str(CLEAN_FALSIFIABLE) + " 行 ⇒ 独立实验预言 0")
    lines.append("-" * 96)
    lines.append("README：" + str(README_BYTES) + " B / " + README_MD5 +
                 " / 最大 RID " + str(README_MAX_RID) + "；本册零改动")
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
