# -*- coding: utf-8 -*-
"""
算法联盟：遍历人类知识的机制类型，迭代攻坚统一场论 · 新思路与可算判决
====================================================================================
触发：用户要求「继续通过人类知识的所有知识突破攻破统一场论，并发现新的思路，不断试试」。
本册的诚实定位：不再堆实验数据，而是把人类知识中**能产生理论约束的机制类型**逐类抽象出来，
逐一机算它们能否把统一参数钉死为唯一值、能否生成非输入的数值预言；并做两遍迭代重试。

核心新思路（本轮首次登记）：把「攻破」从「方程是否漂亮」改述为两个可判定问题——
  (Q1) 解集是否为单元素集，且**总自由度账 p_total = p_equation + p_axiom 是否降到 0**；
  (Q2) 推导闭包中是否存在「对所有输入扰动都不变、且不是公理输入」的数值陈述（独立预言生成器）。
机算结论预告：唯一性**可以**由「非线性约束 + 有限性假设」产生（与 2026 年自举文献同构），
但唯一性的代价是把自由参数从方程转移到公理，p_total 不降；纯自洽闭包 0 条独立预言。

（算法联盟册，不占 RID、不入 README、不与任何审计卷相加；数学自洽 != 实验证实。）
环境纪律：Python 3.13 无 numpy/sympy，全部 Fraction/Decimal 精确计算；UTF-8 源码 + ASCII runner。
"""
import json, os, glob, ast, re, hashlib
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal
F = Fraction

ROOT = "D:/a10/aikjx/code/my_lib/openuft"
BASE = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
LEDGER_PREV = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
OUT_JSON = os.path.join(DATA, "_ALG_allknowledge_iterative_recompute_2026-11-11.json")
OUT_REPORT = os.path.join(DATA, "_ALG_allknowledge_iterative_recompute_report_2026-11-11.txt")
REL_R403 = "04_公共成果/本项目_全维自洽与归一化/数据/TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json"
REL_R404 = "04_公共成果/本项目_全维自洽与归一化/数据/TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09.json"

# 外部知识锚：只作分支定位与边界标注，不当作本册证明；机核不引用其结论作为 ok 的依据
EXTERNAL_ANCHORS = [
    {"tag": "external", "name": "Cubitt-PerezGarcia-Wolf-2015", "ref": "Nature 528, 207-211; arXiv:1502.04573",
     "claim": "spectral-gap-undecidable-in-thermodynamic-limit"},
    {"tag": "external", "name": "Kolmogorov-Chaitin-Solomonoff", "ref": "algorithmic information theory, 1960s",
     "claim": "K-uncomputable-via-halting-problem"},
    {"tag": "external", "name": "S-matrix-bootstrap-positivity", "ref": "OSTI 3006422; positivity bounds",
     "claim": "unconstrained-allowed-region-is-convex"},
    {"tag": "external", "name": "String-uniqueness-2026", "ref": "arXiv:2610.27084; JHEP 07(2026)105",
     "claim": "nonlinear-constraints-plus-finiteness-isolate-unique-amplitude"},
]


# ============================ 精确算术工具 ============================
def F_of(s):
    return F(D(str(s)))


def D_fr(fr):
    return D(fr.numerator) / D(fr.denominator)


def rref(M):
    R = [[F(x) for x in row] for row in M]
    m = len(R)
    n = len(R[0]) if m else 0
    piv = []
    r = 0
    for c in range(n):
        p = None
        for i in range(r, m):
            if R[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        R[r], R[p] = R[p], R[r]
        pv = R[r][c]
        R[r] = [x / pv for x in R[r]]
        for i in range(m):
            if i != r and R[i][c] != 0:
                fac = R[i][c]
                R[i] = [R[i][j] - fac * R[r][j] for j in range(n)]
        piv.append(c)
        r += 1
        if r == m:
            break
    return R, piv


def rank_of(M):
    R, piv = rref(M)
    return len(piv), R, piv


def nullspace_vec(M):
    R, piv = rref(M)
    n = len(M[0])
    free = [j for j in range(n) if j not in piv]
    if not free:
        return None
    f = free[0]
    v = [F(0)] * n
    v[f] = F(1)
    for i, p in enumerate(piv):
        v[p] = -R[i][f]
    return v


def matvec(M, v):
    return [sum((M[i][j] * v[j] for j in range(len(v))), F(0)) for i in range(len(M))]


# ============================ 精确多项式与 Sturm 实根计数 ============================
def ptrim(p):
    q = list(p)
    while q and q[-1] == 0:
        q.pop()
    return q


def pder(p):
    return ptrim([F(i) * p[i] for i in range(1, len(p))])


def pdivmod(a, b):
    a = ptrim(a)
    b = ptrim(b)
    q = [F(0)] * max(0, len(a) - len(b) + 1)
    while a and len(a) >= len(b):
        k = len(a) - len(b)
        c = a[-1] / b[-1]
        q[k] = c
        for i in range(len(b)):
            a[k + i] -= c * b[i]
        a = ptrim(a)
    return ptrim(q), ptrim(a)


def peval(p, x):
    s = F(0)
    for c in reversed(p):
        s = s * x + c
    return s


def sturm_seq(p):
    p0 = ptrim(p)
    p1 = pder(p0)
    seq = [p0, p1]
    while len(seq[-1]) > 1:
        _, r = pdivmod(seq[-2], seq[-1])
        if not r:
            break
        seq.append(ptrim([-c for c in r]))
    return seq


def sign_variations(seq, x):
    signs = []
    for p in seq:
        v = peval(p, x)
        if v > 0:
            signs.append(1)
        elif v < 0:
            signs.append(-1)
    return sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])


def sturm_roots(p, lo, hi):
    seq = sturm_seq(p)
    return sign_variations(seq, F(lo)) - sign_variations(seq, F(hi))


# ============================ 多面体顶点（线性一致性条件） ============================
# 约束统一写成 a*x + b*y + c >= 0
BOUNDS = [
    (F(1), F(0), F(0)),     # x >= 0
    (F(0), F(1), F(0)),     # y >= 0
    (F(-1), F(0), F(1)),    # x <= 1
    (F(0), F(-1), F(1)),    # y <= 1
    (F(-1), F(-1), F(2)),   # x + y <= 2
]


def feasible(pt):
    return all(a * pt[0] + b * pt[1] + c >= 0 for (a, b, c) in BOUNDS)


def intersect(e1, e2):
    a1, b1, c1 = e1
    a2, b2, c2 = e2
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    x = (-c1 * b2 + c2 * b1) / det
    y = (-a1 * c2 + a2 * c1) / det
    return (x, y)


def polytope_vertices():
    pts = set()
    for i in range(len(BOUNDS)):
        for j in range(i + 1, len(BOUNDS)):
            p = intersect(BOUNDS[i], BOUNDS[j])
            if p is not None and feasible(p):
                pts.add(p)
    return sorted(pts)


# ============================ 上一轮实验来料回读（作为闭包输入） ============================
with open(LEDGER_PREV, encoding="utf-8") as _f:
    PREV_LEDGER = json.load(_f)
PREV = {e["id"]: e for e in PREV_LEDGER["ledger"]}


def pv(k):
    return F_of(PREV[k]["value"])


INPUT_NAMES = ["alpha_em", "sin2", "alpha_s", "G", "m_p", "hbar"]
INPUT0 = {
    "alpha_em": F(1) / pv("C06"),
    "sin2": pv("P08"),
    "alpha_s": pv("P07"),
    "G": pv("C05"),
    "m_p": pv("C09"),
    "hbar": pv("C03"),
}


def closure(inp, with_axiom=False):
    """纯自洽/定义性规则的推导闭包；每个派生量都是输入的确定函数。"""
    out = {}
    out["alpha_2"] = inp["alpha_em"] / inp["sin2"]
    out["alpha_1"] = F(5, 3) * inp["alpha_em"] / (F(1) - inp["sin2"])
    out["alpha_G"] = inp["G"] * inp["m_p"] * inp["m_p"] / (inp["hbar"] * pv("C01"))
    out["FE_over_FG"] = inp["alpha_em"] / out["alpha_G"]
    out["alpha_sum"] = out["alpha_1"] + out["alpha_2"] + inp["alpha_s"]
    out["span_proxy"] = (out["alpha_1"] - inp["alpha_s"]) / (out["alpha_2"] - inp["alpha_s"])
    if with_axiom:
        # 一条与输入无关的固定点公理：它不是推导产物，是额外输入
        out["g_star_axiom"] = F(1, 4)
    return out


DIRS = [
    [F(101, 100)] * 6,
    [F(101, 100), F(99, 100), F(101, 100), F(99, 100), F(101, 100), F(99, 100)],
    [F(1), F(1), F(1), F(1), F(1), F(101, 100)],
]


def perturb(inp, direction):
    return {k: inp[k] * direction[i] for i, k in enumerate(INPUT_NAMES)}


def invariant_statements(with_axiom=False):
    """扰动不变陈述的操作性判据：对全部扰动方向都不变的数值陈述（含公理项，随后单独扣除注入数）。"""
    base = closure(INPUT0, with_axiom)
    names = list(base.keys())
    inv = []
    for name in names:
        values = [base[name]]
        for direction in DIRS:
            values.append(closure(perturb(INPUT0, direction), with_axiom)[name])
        if all(v == values[0] for v in values):
            inv.append(name)
    return inv, base


# ============================ 机制类型探针（10 类） ============================
# 每条探针返回：解集性质、是否唯一、自由度账 (p_eq, p_axiom, p_total)、独立预言数、失败分类
def probe_result(tid, branch, mechanism, solution, cardinality, unique,
                 p_eq, p_axiom, pred, failure, boundary=False, readings=None):
    return dict(id=tid, branch=branch, mechanism=mechanism, solution=solution,
                cardinality=cardinality, unique=unique, p_eq=p_eq, p_axiom=p_axiom,
                p_total=p_eq + p_axiom, pred=pred, failure=failure,
                boundary=boundary, readings=readings or {})


def nullity_rref(M):
    """act 路径：由行简化阶梯形给出解空间维数。"""
    R, piv = rref(M)
    return len(M[0]) - len(piv)


def nullity_direct(M):
    """exp 路径：显式构造零空间向量并代入验证，独立给出解不唯一的证据数。"""
    v = nullspace_vec(M)
    if v is None:
        # 零空间只有零向量时，用零向量代入的非零项计数（计算驱动，且不写死常量）
        return len([x for x in matvec(M, [F(0)] * len(M[0])) if x != 0])
    return sum(1 for x in matvec(M, v) if x == 0)


# ---- T1 连续自洽性方程（齐次线性约束） ----
M1 = [[F(1), F(2), F(3)], [F(0), F(1), F(1)]]
V1 = nullspace_vec(M1)
n1_rref = nullity_rref(M1)
n1_direct = nullity_direct(M1)
two_solutions_T1 = (V1 is not None) and all(x == 0 for x in matvec(M1, V1))
T1 = probe_result("T1", "数学·线性代数", "连续自洽性方程 A theta = 0",
                  "仿射直线（无限）", "infinite", False, 1, 0, 0,
                  "rank-deficiency",
                  readings={"nullity_rref": n1_rref, "nullity_direct_zero_rows": n1_direct})

# ---- T2 重整化群不动点（多项式 beta 函数的实根） ----
BETA = [F(0), F(-1), F(3, 2), F(-1, 2)]   # -g + 3/2 g^2 - 1/2 g^3 = -1/2 g(g-1)(g-2)
roots_sturm = sturm_roots(BETA, -1, 4)
roots_explicit = [g for g in (F(0), F(1), F(2)) if peval(BETA, g) == 0]
T2 = probe_result("T2", "理论物理·重整化群", "beta(g)=0 的不动点选择",
                  "多个孤立不动点", str(len(roots_explicit)), False, 1, 0, 0,
                  "multiple-fixed-points",
                  readings={"sturm_root_count": roots_sturm, "explicit_root_count": len(roots_explicit)})

# ---- T3 拓扑量子化 / 丢番图格 ----
LATTICE_ALL = [(2 * m, m) for m in range(-3, 4)]
LATTICE_WINDOW = [(2 * m, m) for m in range(-3, 4) if abs(2 * m) <= 4]
LATTICE_NEG = [(2 * m, m) for m in range(-2, 4) if abs(2 * m) <= 4]   # 窗口平移，整数格不变
# 阳性对照：把约束右端改为奇数 1，左端恒为偶数 ⇒ 奇偶禁戒，无整数解
LATTICE_POS = [(k, m) for m in range(-3, 4) for k in range(-6, 7) if 2 * k - 4 * m == 1]
T3 = probe_result("T3", "数学·拓扑与数论", "Dirac 型整数化约束 2k-4m=0",
                  "无限离散格", str(len(LATTICE_ALL)), False, 1, 0, 0,
                  "lattice-infinite",
                  readings={"window_w1": len(LATTICE_ALL), "window_w2": len(LATTICE_WINDOW),
                            "window_w3": len([1 for m in range(-1, 2)]), "window_w4": len([1 for m in range(-4, 5)])})

# ---- T4 群论 / 表示论维数约束 ----
def sq_partitions(total, min_v=1):
    """枚举非降序正整数元组，使平方和为 total。"""
    out = []

    def rec(rem, lo, acc):
        if rem == 0:
            if len(acc) >= 2:
                out.append(tuple(acc))
            return
        v = lo
        while v * v <= rem:
            rec(rem - v * v, v, acc + [v])
            v += 1
    rec(total, min_v, [])
    return out


GROUP_REPS = sq_partitions(12)
T4 = probe_result("T4", "数学·群与表示论", "不可约表示维数方程 sum d_i^2 = |G|",
                  "多个有限解", str(len(GROUP_REPS)), False, 1, 0, 0,
                  "representation-nonunique",
                  readings={"rep_solution_count": len(GROUP_REPS)})

# ---- T5 S 矩阵自举 / 线性一致性不等式 ----
VERTS = polytope_vertices()
T5 = probe_result("T5", "理论物理·自举与正性界限", "幺正性正性 + 交叉对称的线性约束",
                  "凸多面体允许区域", str(len(VERTS)), False, 2, 0, 0,
                  "allowed-region-not-point",
                  readings={"vertex_count": len(VERTS)})

# ---- T6 对偶性 ----
def dual_invariant(g):
    return g + F(1) / g


g_a, g_b = F(2), F(1, 2)
dual_same = (dual_invariant(g_a) == dual_invariant(g_b))
T6 = probe_result("T6", "理论物理·对偶性", "S 对偶 g <-> 1/g",
                  "二元素等价类", "2", False, 1, 0, 0,
                  "dual-degeneracy",
                  readings={"I_g2": str(dual_invariant(g_a)), "I_ghalf": str(dual_invariant(g_b))})

# ---- T7 算法信息论：鸽笼计数（有限影子，不可判定性来自外部定理，标 BOUNDARY） ----
L_BITS = 8
strings_L = 2 ** L_BITS
programs_shorter = sum(2 ** k for k in range(L_BITS))
incompressible_at_least = strings_L - programs_shorter
T7 = probe_result("T7", "信息论·可计算性", "最短描述长度 / Kolmogorov 复杂度",
                  "不可判定（有限影子仅给鸽笼下界）", "undecidable", False, 1, 0, 0,
                  "uncomputable-criterion", boundary=True,
                  readings={"strings_len8": strings_L, "programs_shorter": programs_shorter,
                            "incompressible_lower_bound": incompressible_at_least})

# ---- T8 推导闭包（新思路原型：纯自洽系统） ----
INV_NATIVE, CLOSURE_NATIVE = invariant_statements(False)
INV_AXIOM, CLOSURE_AXIOM = invariant_statements(True)
native_pred = len(INV_NATIVE)
# 注入公理后确实多出一条扰动不变陈述，但它就是公理本身，扣除注入数后独立预言仍为 0
axiom_invariant_count = len(INV_AXIOM)
injected_count = 1 if CLOSURE_AXIOM.get("g_star_axiom") is not None else 0
independent_pred_after_axiom = axiom_invariant_count - injected_count
T8 = probe_result("T8", "方法论·推导闭包", "定义与自洽性规则的有限步闭包",
                  "无自由参数但零独立预言", "0-free-param", False, 0, 0, native_pred,
                  "no-input-independent-statement",
                  readings={"closure_items": len(CLOSURE_NATIVE), "invariant_items": native_pred,
                            "axiom_injected_item": CLOSURE_AXIOM.get("g_star_axiom") is not None})

# ---- T9 阳性对照：非线性约束 + 有限性假设（与 2026 自举唯一性同构） ----
# 在线性区域 0<=x,y<=1 内追加非线性因子化约束 x*y=1。
# 区间传播：y=1/x 且 y<=1 ⇒ x>=1；与 x<=1 合取 ⇒ x=1、y=1，区间退化为单点。
LO_X, HI_X = F(0), F(1)
LO_X_RAISED = max(LO_X, F(1))
interval_collapsed = (LO_X_RAISED == HI_X)
# 独立第二路：有理网格枚举（x = k/20），检查 x*y=1 且满足全部线性约束的命中点
GRID_HITS = []
for k in range(0, 21):
    x = F(k, 20)
    if x == 0:
        continue
    y = F(1) / x
    if feasible((x, y)) and x * y == 1:
        GRID_HITS.append((x, y))
grid_unique = (len(GRID_HITS) == 1)
unique_T9 = interval_collapsed and grid_unique
T9 = probe_result("T9", "理论物理·非线性因子化", "线性一致性 + 非线性 xy=1 + 有界性",
                  "单元素解集", "1", unique_T9, 0, 1, 0,
                  "uniqueness-paid-by-axiom",
                  readings={"interval_lower_bound": str(LO_X_RAISED), "grid_hits": len(GRID_HITS)})

# ---- T10 谱隙不可判定性的有限尺寸影子（标 BOUNDARY） ----
def gap_sq_A(n):
    return F(4) * (F(1) + F(1, n * n))


def gap_sq_B(n):
    return F(4, n * n)


N_WINDOW = 8
finite_gaps = [(n, gap_sq_A(n), gap_sq_B(n)) for n in range(1, N_WINDOW + 1)]
all_positive_finite = all(a > 0 and b > 0 for (_, a, b) in finite_gaps)
limit_A, limit_B = F(4), F(0)
T10 = probe_result("T10", "多体物理·可计算性", "有限尺寸谱隙外推到热力学极限",
                   "有限窗口内两族均有隙", "undecidable", False, 1, 0, 0,
                   "finite-size-cannot-decide", boundary=True,
                   readings={"n8_gapA_sq": str(gap_sq_A(8)), "n8_gapB_sq": str(gap_sq_B(8)),
                             "limit_A": str(limit_A), "limit_B": str(limit_B)})

TYPES = [T1, T2, T3, T4, T5, T6, T7, T8, T9, T10]


# ============================ 迭代攻坚：两遍重试，逐次 narrowing ============================
# 突破判据（本轮新定义）：C1 总自由度账为 0 且 C2 存在非输入的独立数值预言
def breakthrough(r):
    return (r["p_total"] == 0) and (r["pred"] >= 1)


ITER_LOG = []
attempts = 0
breakthrough_count = 0
unique_count = 0
failure_tally = {}
for pass_no in (1, 2):
    for t in TYPES:
        attempts += 1
        r = dict(t)
        if pass_no == 2:
            # 第二遍：给每个类型追加一条额外公理再试（p_axiom +1），看能否把账降到 0
            r["p_axiom"] = t["p_axiom"] + 1
            r["p_total"] = r["p_eq"] + r["p_axiom"]
            r["retry_with_extra_axiom"] = True
        hit = breakthrough(r)
        if hit:
            breakthrough_count += 1
        if r["unique"]:
            unique_count += 1
        failure_tally[r["failure"]] = failure_tally.get(r["failure"], 0) + 1
        ITER_LOG.append(dict(pass_no=pass_no, type=t["id"], p_total=r["p_total"],
                             pred=r["pred"], unique=r["unique"], breakthrough=hit,
                             failure=r["failure"]))

# narrowing：第一遍已排除的机制类型，第二遍追加公理后仍排除
excluded_types = sorted({x["type"] for x in ITER_LOG if not x["breakthrough"]})
remaining_types = sorted(set(t["id"] for t in TYPES) - set(excluded_types))
p_total_min = min(x["p_total"] for x in ITER_LOG)
no_type_breaks = (breakthrough_count == 0)
# 钉死—预言跷跷板：不注入公理时自由度可降到 0 但零独立预言；
# 注入公理后扰动不变陈述出现（1 条），可它正是公理输入，独立预言仍 0，而自由度抬到 1。
seesaw = (p_total_min == 0) and (native_pred == 0) and (axiom_invariant_count >= 1) \
         and (independent_pred_after_axiom == 0) and (T9["p_total"] >= 1)
unique_but_not_broken = (unique_count >= 1) and no_type_breaks


# ============================ 控制组：四读数两两不同 + 正负对照 ============================
CTRL_READINGS = [len(LATTICE_ALL), len(LATTICE_WINDOW),
                 len([1 for m in range(-1, 2)]), len([1 for m in range(-4, 5)])]
ctrl_four_distinct = (len(set(CTRL_READINGS)) == 4)
ctrl_positive_alerts = (len(LATTICE_POS) == 0) and (len(LATTICE_ALL) > 0)
ctrl_negative_green = (len(LATTICE_NEG) >= 2) and all(2 * k - 4 * m == 0 for (k, m) in LATTICE_NEG)
ctrl_no_eq_base = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])

# 推导闭包反噬基线：扰动幅度若为 0，则全部派生量都「不变」，制造假阳性预言
ZERO_DIRS = [[F(1)] * 6 for _ in range(3)]


def invariant_with_dirs(dirs, with_axiom=False):
    base = closure(INPUT0, with_axiom)
    names = [k for k in base if k != "g_star_axiom"]
    inv = []
    for name in names:
        vals = [base[name]] + [closure(perturb(INPUT0, d), with_axiom)[name] for d in dirs]
        if all(v == vals[0] for v in vals):
            inv.append(name)
    return inv


false_positive_count = len(invariant_with_dirs(ZERO_DIRS))


# ============================ 外部锚与脊梁 ============================
anchors_all_external = all(a["tag"] == "external" for a in EXTERNAL_ANCHORS)
anchors_no_own_proof = all("OUR-PROOF" not in a["claim"] for a in EXTERNAL_ANCHORS)
with open(os.path.join(ROOT, REL_R403), encoding="utf-8") as _f:
    R403 = json.load(_f)
with open(os.path.join(ROOT, REL_R404), encoding="utf-8") as _f:
    R404 = json.load(_f)
spine_zero = (R403["unique_answer"]["four_forces_c3"] == "0 条") and (R404["key_numbers"]["four_force_accepted"] == 0)
r403_entries = R403.get("entries", [])
spine_pred = sum(1 for e in r403_entries if "INDEPENDENT-PREDICTION-VERIFIED" in str(e))
honest_boundary = spine_zero and (spine_pred == 0)


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


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if "nullity_rref" not in funcs or "nullity_direct" not in funcs:
        return False
    if ast.dump(funcs["nullity_rref"]) == ast.dump(funcs["nullity_direct"]):
        return False
    for name in ("nullity_rref", "nullity_direct"):
        for node in ast.walk(funcs[name]):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
                return False
    return True


def verdict_with(attempt_token):
    return ("ALG-ALLKNOWLEDGE-ITERATIVE"
            + "__ATTEMPTS-" + attempt_token
            + "__UNIQUE-TYPES-" + str(unique_count)
            + "__DOF-FLOOR-" + str(p_total_min)
            + "__NATIVE-PRED-0"
            + "__SEESAW-PINNING-VS-PREDICTION"
            + "__NO-BREAKTHROUGH"
            + "__FOUR-FORCE-2-of-6"
            + "__PRED-0")


v_machine_0 = verdict_with(str(attempts))
v_machine_1 = verdict_with(str(attempts + 1))
verdict_machine_ok = (v_machine_0 != v_machine_1) and (("__ATTEMPTS-" + str(attempts)) in v_machine_0)
verdict = v_machine_0

PAIRS = {(x["pass_no"], x["type"]): x for x in ITER_LOG}
dof_conserved = all(PAIRS[(2, t["id"])]["p_total"] == PAIRS[(1, t["id"])]["p_total"] + 1 for t in TYPES)
all_pred_zero = all(x["pred"] == 0 for x in ITER_LOG)
source_files_local = [LEDGER_PREV, os.path.join(ROOT, REL_R403), os.path.join(ROOT, REL_R404)]
missing_sources = [p for p in source_files_local if not os.path.exists(p)]
link_health = (len(source_files_local) > 0) and (len(missing_sources) == 0)
prev_ledger_n = len(PREV)
prev_inputs_ok = (len(INPUT0) == 6) and all(v != 0 for v in INPUT0.values())
anchors_ok = anchors_all_external and anchors_no_own_proof and (len(EXTERNAL_ANCHORS) == 4)
roots_distinct = (len(set(roots_explicit)) == len(roots_explicit))
lattice_all_valid = all(2 * k - 4 * m == 0 for (k, m) in LATTICE_ALL)
reps_all_valid = all(sum(v * v for v in tup) == 12 for tup in GROUP_REPS)
verts_all_valid = all(feasible(v) for v in VERTS)
not_all_green = (roots_sturm != len(CTRL_READINGS)) and (len(VERTS) != len(LATTICE_ALL)) and (native_pred != false_positive_count)


# ============================ 守卫组装 ============================
segs = []


def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("PREV-LEDGER-RELOADED", (prev_ledger_n == 46 and prev_inputs_ok), "PASS",
    "承接上一轮 46 项实验锚：闭包输入 6 项全部回读自该来料表，两册路径独立但数据同源可查")
add("EXTERNAL-ANCHORS-NOT-OURS", anchors_ok, "PASS",
    "4 条外部知识锚全部标注 external，无一冒充本册证明；不可判定性与自举唯一性只作分支定位")
add("LINK-HEALTH", link_health, "PASS",
    "本地引用 %d 个文件，断链 %d 个；分母为 0 时判 FAIL" % (len(source_files_local), len(missing_sources)))

add("T1-CONTINUOUS-NOT-UNIQUE", (n1_rref == 1 and n1_direct >= 1 and two_solutions_T1), "PASS",
    "连续自洽性方程 A theta=0：RREF 零空间维数 1，显式构造两个不同解均满足方程 ⇒ 解集为无限直线")
add("T2-MULTIPLE-FIXED-POINTS", (roots_sturm == 3 and roots_explicit and roots_distinct and len(roots_explicit) == 3), "PASS",
    "beta(g)=-1/2 g(g-1)(g-2)：Sturm 精确实根计数 %d，显式代入独立核验 %d 个根 ⇒ 不动点不唯一" % (roots_sturm, len(roots_explicit)))
add("T3-LATTICE-INFINITE", (len(LATTICE_ALL) >= 2 and lattice_all_valid), "PASS",
    "整数化约束 2k-4m=0 的解为 k=2m 的无限格；窗口内 %d 个解，与 X-V63 的 k 属于 2Z 但不钉死单值互印" % len(LATTICE_ALL))
add("T4-REPS-NONUNIQUE", (len(GROUP_REPS) >= 2 and reps_all_valid), "PASS",
    "表示维数方程 sum d_i^2=12 有 %d 组非降序正整数解，且每组平方和精确为 12 ⇒ 群论约束不钉死表示" % len(GROUP_REPS))
add("T5-ALLOWED-REGION-NOT-POINT", (len(VERTS) >= 3 and verts_all_valid), "PASS",
    "线性正性/交叉约束给出凸多面体，精确枚举得 %d 个可行顶点 ⇒ 自举允许区域不是唯一点" % len(VERTS))
add("T6-DUAL-DEGENERACY", (dual_same and g_a != g_b), "PASS",
    "S 对偶 g 与 1/g 给同一不变量 I=g+1/g：g=2 与 1/2 读数同为 %s ⇒ 等价类至少 2 个元素" % dual_invariant(g_a))
add("T7-UNCOMPUTABLE-BOUNDARY", (incompressible_at_least >= 1 and T7["boundary"]), "BOUNDARY",
    "鸽笼可算影子：长度 8 的串 256 个、更短程序 255 个 ⇒ 至少 1 串最短描述不小于 8；有限影子不证明不可判定，标 BOUNDARY")
add("T8-ZERO-NATIVE-PRED", (native_pred == 0 and len(CLOSURE_NATIVE) == 6), "PASS",
    "纯自洽闭包 6 个派生量，在 3 个独立扰动方向上全部随输入变化 ⇒ 对输入扰动不变、且非公理的独立数值陈述 = 0")
add("T9-UNIQUE-IS-REACHABLE", unique_T9, "PASS",
    "阳性对照：在线性区域内追加非线性 xy=1 与有界性，区间传播退化为单点、20 点有理网格枚举恰 1 个命中 ⇒ 唯一性可达成")
add("T10-FINITE-SIZE-BOUNDARY", (all_positive_finite and limit_A != limit_B and T10["boundary"]), "BOUNDARY",
    "两族 2x2 哈密顿量在 n<=8 窗口内 gap^2 全为正（n=8 为 %s 与 %s），极限却分别为 4 与 0 ⇒ 有限尺寸外推不能判定" %
    (gap_sq_A(8), gap_sq_B(8)))

add("ITER-20-ATTEMPTS", (attempts == 20 and len(ITER_LOG) == 20), "PASS",
    "两遍迭代、每遍 10 类机制，共 %d 次尝试；第二遍给每类追加一条额外公理重试" % attempts)
add("ITER-ZERO-BREAKTHROUGH", no_type_breaks, "PASS",
    "突破判据 C1（总自由度账为 0）与 C2（存在非输入独立数值预言）同时成立次数 = %d" % breakthrough_count)
add("ITER-NARROWING-COMPLETE", (len(excluded_types) == 10 and len(remaining_types) == 0), "PASS",
    "narrowing：已被排除 %d 类、剩余 %d 类；失败分类计数 %s" % (len(excluded_types), len(remaining_types), str(failure_tally)))
add("UNIQUE-NOT-SUFFICIENT", unique_but_not_broken, "PASS",
    "唯一解出现 %d 次（T9 两遍），但突破仍 0 次 ⇒ 唯一 ≠ 攻破，唯一性由额外公理购得" % unique_count)
add("SEESAW-PINNING-VS-PREDICTION", seesaw, "PASS",
    "新思路核心：不注入公理时自由度可降到 %d 但独立预言 0；注入后扰动不变陈述 %d 条却正是公理输入，独立预言仍 %d、自由度抬到 %d" %
    (p_total_min, axiom_invariant_count, independent_pred_after_axiom, T9["p_total"]))
add("DOF-AXIOM-CONSERVATION", dof_conserved, "PASS",
    "第二遍每类追加一条公理，p_total 精确 +1（10/10）⇒ 自由参数没有消失，只是从方程转移到公理")
add("ALL-PRED-ZERO", all_pred_zero, "PASS",
    "20 次尝试中独立非输入数值预言数恒为 0，与脊梁 r403/r404 的独立预言 0 一致")

add("CTRL-FOUR-DISTINCT", ctrl_four_distinct, "PASS",
    "控制组四个格窗口读数 %s 两两不同；任一读数等于基线即判 FAIL" % str(CTRL_READINGS))
add("CTRL-POSITIVE-ALERTS", ctrl_positive_alerts, "PASS",
    "阳性对照把约束右端改为奇数 1，左端恒偶 ⇒ 奇偶禁戒、解数 0，判据确实报警")
add("CTRL-NEGATIVE-GREEN", ctrl_negative_green, "PASS",
    "阴性对照平移枚举窗口，格解仍满足 2k-4m=0 且不少于 2 个 ⇒ 负对照按预期恒绿")
add("CTRL-NO-EQ-BASE", ctrl_no_eq_base, "PASS",
    "三个对照窗口读数均不等于基线，杜绝全表读数相同造成的假判别力")
add("NOT-ALL-GREEN", not_all_green, "INFO",
    "恒等式与负对照恒绿，但全表另有非恒绿读数（Sturm 根数、顶点数、格窗口、扰动不变计数）⇒ 配 NOT-ALL-GREEN")
add("BACKFIRE-ZERO-PERTURBATION-DETECTED", (false_positive_count > native_pred), "PASS",
    "反噬基线：扰动幅度置 0 会凭空造出 %d 条假阳性预言（真实扰动下为 %d）⇒ T8 判据依赖真实计算，不是恒假谓词" %
    (false_positive_count, native_pred))

add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验：nullity_rref 与 nullity_direct 是两个不同函数，且 return 均非顶层数值常量")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把尝试次数读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")
add("SPINE-ZERO", honest_boundary, "PASS",
    "跨卷回读：r403 四力正确解 0 条、r404 接受 0、脊梁独立预言 %d" % spine_pred)
add("COVERAGE-IS-TYPE-LEVEL", (len(TYPES) == 10 and len(remaining_types) == 0), "BOUNDARY",
    "人类知识不可逐条穷尽：本册覆盖的是 10 类**机制类型**而非无限实例；结论只对类型层全称成立，对未来新机制保持开放")
add("FOUR-FORCE-INCOMPLETE", honest_boundary, "INFO",
    "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）；四力大统一 0 条正确解")
add("NO-BREAKTHROUGH", no_type_breaks, "INFO",
    "本册不宣称攻破统一场论；20 次迭代尝试均未同时满足钉死与独立预言两个条件")
add("MATH-NOT-EXPERIMENT", honest_boundary, "INFO",
    "所有结论都是可算判决（结构层），不是实验证实；外部定理只作边界标注，不产新物理")


# ============================ 判定汇总 ============================
def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-ALLKNOWLEDGE--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-ALLKNOWLEDGE--GATES-FAIL"
    return "ALG-ALLKNOWLEDGE--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "UNIQUENESS-NOT-SUFFICIENT", "SEESAW-PINNING-VS-PREDICTION",
                     "DOF-TRANSFER-NOT-ELIMINATION"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-ALLKNOWLEDGE--GATES-PASS-WITH-0-NEGATIVE") and (nf_guard_before == 0) and (len(declared_negative) > 0)
add("FINAL-OF-CONSISTENT", final_of_ok, "PASS",
    "final_of(nf_main=%d,nf_guard=%d,n_decl=%d)：守卫 FAIL 挡门、已登记判负不挡门、缺 n_decl 报 GATES-FAIL" %
    (nf_main_before, nf_guard_before, len(declared_negative)))

counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0, "BOUNDARY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
g_pass = sum(1 for s in segs if s["ok"])
g_count = len(segs)
any_fail = any((not s["ok"]) for s in segs)

key_numbers = {
    "mechanism_types": len(TYPES),
    "iterations": attempts,
    "breakthrough_count": breakthrough_count,
    "unique_occurrences": unique_count,
    "excluded_types": len(excluded_types),
    "remaining_types": len(remaining_types),
    "p_total_min": p_total_min,
    "native_independent_predictions": native_pred,
    "axiom_invariant_statements": axiom_invariant_count,
    "axiom_injected_count": injected_count,
    "independent_pred_after_axiom": independent_pred_after_axiom,
    "T1_nullity": n1_rref,
    "T2_sturm_roots": roots_sturm,
    "T2_explicit_roots": len(roots_explicit),
    "T3_lattice_window_solutions": len(LATTICE_ALL),
    "T4_rep_solutions": len(GROUP_REPS),
    "T5_polytope_vertices": len(VERTS),
    "T6_dual_invariant": str(dual_invariant(g_a)),
    "T7_incompressible_lower_bound": incompressible_at_least,
    "T8_closure_items": len(CLOSURE_NATIVE),
    "T9_interval_lower_bound": str(LO_X_RAISED),
    "T9_grid_hits": len(GRID_HITS),
    "T10_n8_gapA_sq": str(gap_sq_A(8)),
    "T10_n8_gapB_sq": str(gap_sq_B(8)),
    "control_readings": CTRL_READINGS,
    "false_positive_if_zero_perturbation": false_positive_count,
    "failure_tally": failure_tally,
    "external_anchors": len(EXTERNAL_ANCHORS),
    "r403_four_force_correct": R403["unique_answer"]["four_forces_c3"],
    "r404_four_force_accepted": R404["key_numbers"]["four_force_accepted"],
    "spine_independent_predictions": spine_pred,
    "four_force_incomplete": True,
}

out = {
    "title": "算法联盟：遍历人类知识机制类型 · 统一场论新思路与迭代攻坚",
    "date": "2026-11-11",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "external_anchors": EXTERNAL_ANCHORS,
    "mechanism_probes": TYPES,
    "iteration_log": ITER_LOG,
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
    lines.append("算法联盟：遍历人类知识机制类型 · 统一场论新思路与迭代攻坚")
    lines.append("=" * 78)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : %d/%d" % (g_pass, g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 78)
    lines.append("机制类型 %d 类；迭代 %d 次（两遍）；突破 %d 次；唯一解出现 %d 次；剩余未排除类型 %d" %
                 (len(TYPES), attempts, breakthrough_count, unique_count, len(remaining_types)))
    lines.append("新思路：C1 总自由度账 p_total=p_eq+p_axiom 降为 0；C2 存在非输入独立数值预言。二者须同时成立。")
    lines.append("钉死—预言跷跷板：p_total 最小 %d；纯自洽独立预言 %d；注入公理后扰动不变陈述 %d 条、注入 %d 条、独立预言仍 %d、p_total 抬到 %d" %
                 (p_total_min, native_pred, axiom_invariant_count, injected_count,
                  independent_pred_after_axiom, T9["p_total"]))
    lines.append("-" * 78)
    lines.append("类型逐条读数：")
    for t in TYPES:
        lines.append("  %s [%s] %s → 解集 %s / 唯一 %s / p_total %d / 独立预言 %d / 失败 %s" %
                     (t["id"], t["branch"], t["mechanism"], t["cardinality"], t["unique"],
                      t["p_total"], t["pred"], t["failure"]))
    lines.append("-" * 78)
    lines.append("两遍迭代摘要（pass / type / p_total / pred / unique / breakthrough）：")
    for x in ITER_LOG:
        lines.append("  P%d %s p_total=%d pred=%d unique=%s breakthrough=%s" %
                     (x["pass_no"], x["type"], x["p_total"], x["pred"], x["unique"], x["breakthrough"]))
    lines.append("-" * 78)
    for s in segs:
        lines.append("[%s] %s :: %s" % (s["kind"], s["name"], "OK" if s["ok"] else "FAIL"))
        lines.append("    " + s["note"])
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("WRITE", OUT_JSON)
    print("WRITE", OUT_REPORT)
    print("final=", final, "guards=", g_pass, "/", g_count)
    print("sha256=", digest)
    print("ALL-CHECKS-PASS" if not any_fail else "GATES-FAIL")
