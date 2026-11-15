# -*- coding: utf-8 -*-
"""算法联盟第二十三轮：核心公式体系的单一生成元可积性审计（形式层）。
只产可算判决，不产新物理；数学自洽不等于实验证实；不宣称攻破统一场论。
"""
import os, glob, json, re, ast, hashlib, itertools, sys
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 60
N = 3
DATE = "2026-11-15"

ANCHOR = "_ALG_information_gate_recompute_2026-11-12.json"
_anchor_hits = glob.glob("openuft/**/" + ANCHOR, recursive=True)
assert len(_anchor_hits) == 1, "ANCHOR-HITS=%d" % len(_anchor_hits)
MAIN = os.path.dirname(os.path.dirname(_anchor_hits[0]))
DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
JUDGE = os.path.join(MAIN, "判定")
README = os.path.join(MAIN, "README.md")

OUT_JSON = os.path.join(DATA, "_ALG_r23_generator_integrability_recompute_2026-11-15.json")
OUT_REPORT = os.path.join(DATA, "_ALG_r23_generator_integrability_recompute_report_2026-11-15.txt")

OWN_TOKENS = ("r23_generator", "第二十三轮", "生成元与交换子")


def is_own(p):
    """自指盘点：本册全部产物必须排除，否则首次与复跑读数漂移。"""
    b = os.path.basename(p)
    return any(t in b for t in OWN_TOKENS)


def report_path_from_json(jp):
    """JSON -> report 的唯一路径构造；机核与核验器共用，禁另起一套。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(DATA, stem)


def md5_of(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


# ---------------- 精确多元多项式环（单项式指数元组 -> Fraction 系数） ----------------

def p_const(c):
    c = F(c)
    return {} if c == 0 else {(0,) * N: c}


def p_var(i):
    e = [0] * N
    e[i] = 1
    return {tuple(e): F(1)}


def p_add(a, b):
    r = dict(a)
    for e, c in b.items():
        r[e] = r.get(e, F(0)) + c
        if r[e] == 0:
            del r[e]
    return r


def p_neg(a):
    return {e: -c for e, c in a.items()}


def p_sub(a, b):
    return p_add(a, p_neg(b))


def p_mul(a, b):
    r = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            r[e] = r.get(e, F(0)) + ca * cb
            if r[e] == 0:
                del r[e]
    return r


def p_deriv(a, i):
    r = {}
    for e, c in a.items():
        if e[i] == 0:
            continue
        ee = list(e)
        k = ee[i]
        ee[i] -= 1
        key = tuple(ee)
        r[key] = r.get(key, F(0)) + c * k
    return r


def p_eval(a, z):
    s = F(0)
    for e, c in a.items():
        t = c
        for i, k in enumerate(e):
            t *= z[i] ** k
        s += t
    return s


def p_is_zero(a):
    return not bool(a)


def vf(X):
    return tuple(X)


def vf_bracket(X, Y):
    """Lie bracket：[X,Y]^l = sum_m (X^m d_m Y^l - Y^m d_m X^l)。"""
    out = []
    for l in range(N):
        acc = {}
        for m in range(N):
            acc = p_add(acc, p_sub(p_mul(X[m], p_deriv(Y[l], m)),
                                   p_mul(Y[m], p_deriv(X[l], m))))
        out.append(acc)
    return tuple(out)


def vf_is_zero(X):
    return all(p_is_zero(c) for c in X)


def monomials(fields):
    b = set()
    for X in fields:
        for c in X:
            b.update(c.keys())
    return sorted(b)


def flatten(X, B):
    idx = {e: i for i, e in enumerate(B)}
    v = [F(0)] * (N * len(B))
    for l in range(N):
        for e, c in X[l].items():
            v[l * len(B) + idx[e]] = c
    return v


# ---------------- 精确线性代数 ----------------

def rref(mat):
    a = [row[:] for row in mat]
    if not a:
        return a, 0, []
    nr, nc = len(a), len(a[0])
    piv = []
    r = 0
    for c in range(nc):
        sel = None
        for i in range(r, nr):
            if a[i][c] != 0:
                sel = i
                break
        if sel is None:
            continue
        a[r], a[sel] = a[sel], a[r]
        pv = a[r][c]
        a[r] = [x / pv for x in a[r]]
        for i in range(nr):
            if i == r or a[i][c] == 0:
                continue
            f = a[i][c]
            a[i] = [a[i][j] - f * a[r][j] for j in range(nc)]
        piv.append(c)
        r += 1
        if r == nr:
            break
    return a, r, piv


def rank_of(vectors):
    if not vectors:
        return 0
    return rref([list(v) for v in vectors])[1]


def in_span(target, basis_vectors):
    """精确成员检验：增广矩阵与系数矩阵同秩则相容。"""
    if not basis_vectors:
        return target == [F(0)] * len(target)
    n = len(target)
    cols = [list(v) for v in basis_vectors]
    aug = [[cols[k][i] for k in range(len(cols))] + [target[i]] for i in range(n)]
    r1 = rref(aug)[1]
    r2 = rref([row[:-1] for row in aug])[1]
    return r1 == r2


def generic_rank(fields, probes):
    """逐点求秩取最大；多剖面避开退化点恒绿。"""
    ranks = []
    for z in probes:
        rows = [[p_eval(X[l], z) for X in fields] for l in range(N)]
        ranks.append(rref(rows)[1])
    return max(ranks), ranks


# ---------------- 来料（act：结构化 JSON 路径） ----------------

SRC_FILES = {
    "r99": "TUFT-r99_力公式体系压缩版与统一场论方程_机器审计_2026-10-18.json",
    "r99_report": "TUFT-r99_力公式体系压缩版与统一场论方程_机器审计_2026-10-18_report.txt",
    "r342": "TUFT-r342_核心公式理论体系全链路审计_六环量纲承载与定义域正确性总账_精算与可视化_2026-11-01.json",
    "r342_report": "TUFT-r342_核心公式理论体系全链路审计_六环量纲承载与定义域正确性总账_精算与可视化_2026-11-01_report.txt",
    "s17": "S17核心公式_闭合代价与单位约定组合_2026-10-03.json",
    "s17_md": "S17核心公式_闭合代价与单位约定组合_2026-10-03.md",
    "r141": "TUFT-r141_核心公式理论体系_物理层内部矛盾与新增性机检_2026-10-21.json",
    "r20": "_ALG_gut_meet_recompute_2026-11-14.json",
    "r20_report": "_ALG_gut_meet_recompute_report_2026-11-14.txt",
    "r22": "_ALG_r22_equation_deriv_recompute_2026-11-15.json",
    "r22_report": "_ALG_r22_equation_deriv_recompute_report_2026-11-15.txt",
    "beta": "_ALG_UFT_eq_derive_recompute_2026-11-09.json",
}


def load_json(key):
    return json.load(open(os.path.join(DATA, SRC_FILES[key]), encoding="utf-8"))


def load_text(key):
    return open(os.path.join(DATA, SRC_FILES[key]), encoding="utf-8", errors="replace").read()


def act_r99_deps():
    d = load_json("r99")
    return [tuple(e["deps"]) for e in d["formula_verdicts"]]


def act_r99_formula_count():
    return len(act_r99_deps())


def act_r99_check_codes():
    d = load_json("r99")
    return sorted(set(str(e["code"]) for e in d["items"]))


def act_r342_item_total():
    return int(load_json("r342")["summary"]["条目总数"])


def act_r342_exponents(name):
    d = load_json("r342")
    q2 = next(it for it in d["items"] if it["id"] == "Q2")["kv"]
    return [F(str(x)) for x in q2[name]]


def act_s17_combo_count():
    return len(load_json("s17")["组合枚举"])


def act_s17_max_fixed():
    return int(load_json("s17")["最大修复后通过"])


def act_s17_augmentation():
    return int(load_json("s17")["最小增广集"]["合计"])


def act_s17_switch_count():
    return len(load_json("s17")["口径开关"])


def act_beta():
    k = load_json("beta")["key_numbers"]
    return [F(str(k[x])) for x in ("b1", "b2", "b3")]


def act_wls_flow():
    k = load_json("r22")["key_numbers"]
    return F(str(k["dAdu_analytic"])), F(str(k["dxdu_analytic"]))


def act_wls_flow_text():
    """登记串口径：与 report 的舍入串逐字比较，禁拿 Fraction 序列化形式当值。"""
    k = load_json("r22")["key_numbers"]
    return str(k["dAdu_analytic"]), str(k["dxdu_analytic"])


def act_r141_fails():
    d = load_json("r141")
    return sum(1 for e in d["entries"] if e.get("verdict") == "FAIL")


# ---------------- 来料（exp：纯文本正则抽列，与 act 不同函数族） ----------------

def exp_r342_item_total():
    txt = load_text("r342_report")
    m = re.search(r"^\s*条目总数\s*[:：]\s*(\d+)\s*$", txt, re.M)
    return int(m.group(1)) if m else -1


def exp_r342_fail():
    txt = load_text("r342_report")
    m = re.search(r"^\s*FAIL\s*[:：]\s*(\d+)\s*$", txt, re.M)
    return int(m.group(1)) if m else -1


def exp_s17_combo_count():
    txt = load_text("s17_md")
    m = re.search(r"^##\s*(\d+)\s*种口径组合", txt, re.M)
    return int(m.group(1)) if m else -1


def exp_s17_max_fixed():
    txt = load_text("s17_md")
    m = re.search(r"最大修复后通过\s*\*\*(\d+)\s*/", txt)
    return int(m.group(1)) if m else -1


def exp_s17_augmentation():
    txt = load_text("s17_md")
    m = re.search(r"=\s*\*\*(\d+)\s*条\*\*", txt)
    return int(m.group(1)) if m else -1


def exp_beta_text():
    """独立册口径：R20 report 的 beta_text 是另一册的文本登记。"""
    txt = load_text("r20_report")
    m = re.search(r"^b_sm_text\s*=\s*[\"']?([^\"'\n]+)", txt, re.M)
    return m.group(1).strip() if m else ""


def exp_wls_flow():
    """R22 report 的 MACHINE-TABLE 读数（登记值为舍入串，按同口径逐字比对）。"""
    txt = load_text("r22_report")
    out = []
    for key in ("dAdu_analytic", "dxdu_analytic"):
        m = re.search(r"^%s\s*=\s*[\"']?([^\"'\n]+)" % key, txt, re.M)
        out.append(m.group(1).strip().strip("\"'") if m else "")
    return tuple(out)


def exp_r99_machine_keys():
    txt = load_text("r99_report")
    return len(re.findall(r"^\s*([a-z][a-z0-9_]*)\s*=\s*\S", txt, re.M))


def readme_snapshot():
    """README 实时读数：并行会话可能改动，禁时序型 MD5 判据。"""
    rb = open(README, "rb").read()
    rids = [int(m) for m in re.findall(rb"TUFT-r(\d+)_", rb)]
    tree = []
    for d in (DATA, SRC, JUDGE):
        for p in glob.glob(os.path.join(d, "**", "*"), recursive=True):
            mm = re.search(r"r(\d+)_", os.path.basename(p))
            if mm:
                tree.append(int(mm.group(1)))
    return dict(bytes=len(rb), md5=hashlib.md5(rb).hexdigest(),
                max_rid=max(rids) if rids else -1,
                tree_max_rid=max(tree) if tree else -1)


# ---------------- 守卫累加器（ok 由读数驱动，kind 由 ok 决定） ----------------

GUARDS = []


def add(name, ok, note="", tag=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, kind="PASS" if ok else "FAIL",
                       note=str(note), tag=str(tag)))
    return ok


def add_identity(name, note=""):
    GUARDS.append(dict(name=name, ok=None, kind="IDENTITY", note=str(note), tag="identity"))
    return None


def add_boundary(name, note=""):
    GUARDS.append(dict(name=name, ok=None, kind="BOUNDARY", note=str(note), tag="boundary"))
    return None


def add_info(name, note=""):
    GUARDS.append(dict(name=name, ok=None, kind="INFO", note=str(note), tag="info"))
    return None


def guard_stats():
    n = len(GUARDS)
    npass = sum(1 for g in GUARDS if g["kind"] == "PASS")
    nfail = sum(1 for g in GUARDS if g["kind"] == "FAIL")
    counts = {}
    for g in GUARDS:
        counts[g["kind"]] = counts.get(g["kind"], 0) + 1
    return dict(count=n, pas=npass, fail=nfail, kinds=counts)


# ---------------- 层 D：公式—外部前提依赖图（对象：r99 的 23 条公式） ----------------

def layer_d(deps):
    """单一生成元可行 <=> 全部公式共享至少一个外部前提（交集非空）。"""
    universe = sorted(set(x for d in deps for x in d))
    inter = set(universe)
    for d in deps:
        inter &= set(d)
    cover = {}

    def hit_size(S):
        return sum(1 for d in deps if any(x in S for x in d))

    for u in universe:
        cover[u] = hit_size({u})
    min_hit = None
    solutions = []
    for k in range(1, len(universe) + 1):
        for combo in itertools.combinations(universe, k):
            if hit_size(set(combo)) == len(deps):
                solutions.append(list(combo))
        if solutions:
            min_hit = k
            break
    return dict(formulas=len(deps), universe=universe,
                universe_size=len(universe),
                common_prerequisites=sorted(inter),
                common_count=len(inter),
                min_hitting_set=min_hit,
                min_hitting_solutions=len(solutions),
                best_single_coverage=max(cover.values()) if cover else 0,
                best_single_label=sorted(cover.items(), key=lambda t: (-t[1], t[0]))[0][0] if cover else "",
                single_generator_possible=bool(len(inter) > 0))


def renamed_deps(deps, suffix):
    """纯改名双射：只换标签，不改图结构。用于证明判据不是靠名字工作。"""
    return [tuple(str(x) + suffix for x in d) for d in deps]


def control_d_positive(deps):
    """正对照：人为让全部公式共享一个前提，谓词必须报「单生成元可行」。"""
    return layer_d([("G0",) + d for d in deps])


def control_d_negative(deps, foreign_ids):
    """负对照：跨册错配（r342 条目 id 作依赖标签），改变图结构而非册内置换。"""
    out = []
    for i, d in enumerate(deps):
        out.append(tuple(str(foreign_ids[(i + j) % len(foreign_ids)])
                         for j in range(len(d))))
    return layer_d(out)


# ---------------- 层 C：生成元向量场的 Lie 交换子与对合性 ----------------

PROBES = [(F(1), F(1), F(1)), (F(2), F(3), F(5)), (F(-1), F(4), F(2)),
          (F(7), F(-2), F(1)), (F(3), F(11), F(-5)), (F(-9), F(2), F(8))]


def build_fields(wls, beta, exp_h, exp_c, mode="real"):
    Z = [p_var(i) for i in range(N)]
    X_wls = vf([p_const(wls[0]), p_const(wls[1]), p_const(1)])
    X_rg = vf([p_const(-beta[0]), p_const(-beta[1]), p_const(-beta[2])])
    X_h = vf([p_mul(p_const(exp_h[i]), Z[i]) for i in range(N)])
    X_c = vf([p_mul(p_const(exp_c[i]), Z[i]) for i in range(N)])
    if mode == "positive":
        same = vf([p_const(1), p_const(2), p_const(3)])
        return [("X_SAME", same), ("X_SAME", same), ("X_SAME", same), ("X_SAME", same)]
    if mode == "negative":
        # 沿判据无法吸收的方向位移：把一个对角缩放场换成旋转场
        X_rot = vf([Z[1], p_neg(Z[0]), p_const(0)])
        return [("X_WLS", X_wls), ("X_RG", X_rg), ("X_HBAR", X_h), ("X_ROT", X_rot)]
    return [("X_WLS", X_wls), ("X_RG", X_rg), ("X_HBAR", X_h), ("X_C", X_c)]


def layer_c(fields):
    raw = [x for _, x in fields]
    grank, profiles = generic_rank(raw, PROBES)
    brackets = {}
    for i, j in itertools.combinations(range(len(raw)), 2):
        brackets[(i, j)] = vf_bracket(raw[i], raw[j])
    all_fields = raw + list(brackets.values())
    B = monomials(all_fields)
    basis = [flatten(X, B) for X in raw]
    r_initial = rank_of(basis)
    nz = 0
    outside = 0
    detail = []
    for (i, j), Zij in brackets.items():
        zero = vf_is_zero(Zij)
        inside = in_span(flatten(Zij, B), basis) if not zero else True
        if not zero:
            nz += 1
        if not inside:
            outside += 1
        detail.append(dict(pair=[fields[i][0], fields[j][0]],
                           zero=bool(zero), in_span=bool(inside)))
    # Lie 闭包：迭代加入跳出 span 的交换子，直到秩稳定
    closure = list(raw)
    trace = []
    rounds = 0
    for it in range(8):
        rounds = it + 1
        Bc = monomials(closure)
        bv = [flatten(X, Bc) for X in closure]
        trace.append(rank_of(bv))
        fresh = []
        for i, j in itertools.combinations(range(len(closure)), 2):
            Zij = vf_bracket(closure[i], closure[j])
            if vf_is_zero(Zij):
                continue
            B2 = monomials(closure + [Zij])
            cur = [flatten(X, B2) for X in closure]
            if not in_span(flatten(Zij, B2), cur):
                fresh.append(Zij)
        if not fresh:
            break
        closure.extend(fresh)
    return dict(field_count=len(raw), generic_rank_pointwise=grank, rank_profiles=profiles,
                poly_rank_initial=r_initial, poly_rank_closure=trace[-1],
                closure_trace=trace, closure_rounds=rounds,
                closure_fields=len(closure), monomial_basis_size=len(B),
                bracket_pairs=len(brackets), nonzero_brackets=nz,
                brackets_outside_span=outside, bracket_detail=detail,
                single_generator_possible=bool(grank <= 1),
                involutive=bool(outside == 0),
                closure_grows=bool(trace[-1] > trace[0]))


def sensitivity_outside(wls, beta, exp_h, exp_c):
    """WLS 流系数是 R22 的 9 位登记舍入串；扰动后判词是否稳定。"""
    out = []
    for eps in (F(1, 10 ** 9), F(-1, 10 ** 9), F(1, 10 ** 6)):
        w = (wls[0] + eps, wls[1] - eps)
        f = [x for _, x in build_fields(w, beta, exp_h, exp_c)]
        brk = [vf_bracket(f[i], f[j]) for i, j in itertools.combinations(range(4), 2)]
        Ba = monomials(f + brk)
        ba = [flatten(X, Ba) for X in f]
        n_out = 0
        for Zij in brk:
            if not vf_is_zero(Zij) and not in_span(flatten(Zij, Ba), ba):
                n_out += 1
        out.append(n_out)
    return out


# ---------------- 门判别力：剔除 100% / 0% 的装饰判据 ----------------

def gate_vector(D, C):
    return {
        "D-NO-COMMON-PREREQ": bool(D["common_count"] == 0),
        "D-MINHIT-GT1": bool(D["min_hitting_set"] is not None and D["min_hitting_set"] > 1),
        "C-GRANK-GT1": bool(C["generic_rank_pointwise"] > 1),
        "C-BRACKET-NONZERO": bool(C["nonzero_brackets"] > 0),
        "C-NOT-INVOLUTIVE": bool(C["brackets_outside_span"] > 0),
        "C-CLOSURE-GROWS": bool(C["closure_grows"]),
    }


def gate_power(configs):
    names = sorted(configs[0][1].keys())
    rates = {}
    for nm in names:
        vals = [bool(cfg[1][nm]) for cfg in configs]
        rates[nm] = dict(values=vals, pass_rate=sum(1 for v in vals if v) / len(vals))
    decisive = [nm for nm in names if 0 < rates[nm]["pass_rate"] < 1]
    decorative = [nm for nm in names if rates[nm]["pass_rate"] in (0.0, 1.0)]
    return dict(rates=rates, decisive=decisive, decorative=decorative,
                decisive_count=len(decisive), decorative_count=len(decorative))


# ---------------- 两路机拼 ----------------

def crosscheck():
    dAt, dxt = act_wls_flow_text()
    e1, e2 = exp_wls_flow()
    b = act_beta()
    beta_text = "、".join(str(x) for x in b)
    pairs = [
        ("r342_item_total", str(act_r342_item_total()), str(exp_r342_item_total())),
        ("r342_fail", str(sum(1 for i in load_json("r342")["items"] if i["verdict"] == "FAIL")),
         str(exp_r342_fail())),
        ("s17_combo_count", str(act_s17_combo_count()), str(exp_s17_combo_count())),
        ("s17_max_fixed", str(act_s17_max_fixed()), str(exp_s17_max_fixed())),
        ("s17_augmentation", str(act_s17_augmentation()), str(exp_s17_augmentation())),
        ("r22_dAdu_analytic", dAt, e1),
        ("r22_dxdu_analytic", dxt, e2),
        ("beta_text_cross_book", beta_text, exp_beta_text()),
    ]
    rows = [dict(key=k, act=a, exp=e, match=bool(a == e)) for k, a, e in pairs]
    return dict(rows=rows, match=sum(1 for r in rows if r["match"]), total=len(rows),
                r99_text_machine_keys=exp_r99_machine_keys())


# ---------------- 判词（机读：读数 +1 后字符串必须变化） ----------------

def verdict_of(K):
    return ("ALG-GI__FORM-%d__UNIV-%d__INTER-%d__MINHIT-%d__SOL-%d__S17-%d__AUG-%d"
            "__GRANK-%d__BRK-%d__OUT-%d__POLY-%d-%d__GATE-%d__CLEAN-%d__PRED-%d" %
            (K["r99_formula_count"], K["r99_universe_size"], K["common_prerequisites"],
             K["min_hitting_set"], K["min_hitting_solutions"], K["s17_combo_count"],
             K["s17_min_augmentation"], K["generic_rank_pointwise"],
             K["nonzero_brackets"], K["brackets_outside_span"],
             K["poly_rank_initial"], K["poly_rank_closure"], K["decisive_gates"],
             K["clean_zero_count"], K["independent_predictions"]))


def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-R23-GENERATOR--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-R23-GENERATOR--GATES-FAIL"
    return "ALG-R23-GENERATOR--GATES-PASS-WITH-0-NEGATIVE"


# ---------------- AST 结构性守卫 ----------------

def kernel_source():
    return open(os.path.join(SRC, "_alg_r23_generator_integrability_recompute.py"),
                encoding="utf-8").read()


def ast_no_hardcode_ok():
    """守卫：所有 add() 的 ok 实参不得是布尔/数值字面量。"""
    tree = ast.parse(kernel_source())
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "add"):
            continue
        arg = None
        if len(node.args) >= 2:
            arg = node.args[1]
        for kw in node.keywords:
            if kw.arg == "ok":
                arg = kw.value
        if arg is None or isinstance(arg, ast.Constant):
            bad.append(getattr(node, "lineno", -1))
    return dict(bad=bad, ok=bool(len(bad) == 0),
                scanned=sum(1 for n in ast.walk(tree)
                            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                            and n.func.id == "add"))


def ast_exp_act_distinct():
    """守卫：act 与 exp 必须是两个不同函数族，且 return 不得是顶层数值常量。"""
    tree = ast.parse(kernel_source())
    groups = {"act": set(), "exp": set()}
    bad_return = []
    calls = {"act": set(), "exp": set()}
    for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        for pref in groups:
            if not fn.name.startswith(pref + "_"):
                continue
            groups[pref].add(fn.name)
            for node in ast.walk(fn):
                if isinstance(node, ast.Return) and node.value is not None:
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                        bad_return.append(fn.name)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    calls[pref].add(node.func.id)
    main_loader = dict(act="load_json", exp="load_text")
    return dict(act_funcs=sorted(groups["act"]), exp_funcs=sorted(groups["exp"]),
                disjoint=bool(not (groups["act"] & groups["exp"])),
                bad_return=sorted(set(bad_return)),
                act_uses_json=bool(main_loader["act"] in calls["act"]),
                exp_uses_text=bool(main_loader["exp"] in calls["exp"]),
                ok=bool(len(groups["act"]) > 0 and len(groups["exp"]) > 0
                        and not (groups["act"] & groups["exp"])
                        and len(bad_return) == 0
                        and main_loader["act"] in calls["act"]
                        and main_loader["exp"] in calls["exp"]))


def ast_readme_zero_write():
    """结构性零写入：机核中不存在以写模式打开 README 的调用。"""
    tree = ast.parse(kernel_source())
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        if not (isinstance(fn, ast.Name) and fn.id in ("open", "write")):
            continue
        if not node.args:
            continue
        a0 = node.args[0]
        text = ""
        if isinstance(a0, ast.Name):
            text = a0.id
        elif isinstance(a0, ast.Attribute):
            text = a0.attr
        if text != "README":
            continue
        for arg in node.args[1:]:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and "w" in arg.value:
                bad.append(getattr(node, "lineno", -1))
    return dict(bad=bad, ok=bool(len(bad) == 0))


def self_exclusion_check():
    """自指盘点：按预期产物名逐个验证 OWN_TOKENS 覆盖，且不误排他册。
    用固定预期名而非磁盘实时枚举，避免首次与幂等复跑读数漂移。"""
    expected = [
        os.path.basename(OUT_JSON), os.path.basename(OUT_REPORT),
        "_alg_r23_generator_integrability_recompute.py",
        "_ALG_r23_generator_integrability_verify_2026-11-15.json",
        "算法联盟_核心公式体系单一生成元可积性审计_第二十三轮_2026-11-15.md",
        "算法联盟_核心公式体系生成元与交换子_第二十三轮可视化_2026-11-15.html",
    ]
    missed = [n for n in expected if not is_own(n)]
    false_positive = bool(is_own("_ALG_r22_equation_deriv_recompute.py") or
                          is_own("README.md") or is_own("S17核心公式_闭合代价_2026-10-03.json"))
    return dict(expected=len(expected), missed=missed,
                false_positive=false_positive,
                ok=bool(len(missed) == 0 and not false_positive))


def source_manifest():
    rows = []
    for key, name in sorted(SRC_FILES.items()):
        p = os.path.join(DATA, name)
        rows.append(dict(key=key, path=os.path.relpath(p, MAIN).replace("\\", "/"),
                         bytes=os.path.getsize(p), md5=md5_of(p)))
    return rows


def canonical_sha(obj):
    s = json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ---------------- 主流程 ----------------

def main():
    GUARDS.clear()
    deps = act_r99_deps()
    D = layer_d(deps)
    renamed = layer_d(renamed_deps(deps, "_RENAMED"))
    r342_ids = [str(it["id"]) for it in load_json("r342")["items"]]
    Dpos = control_d_positive(deps)
    Dneg = control_d_negative(deps, r342_ids)

    wls = act_wls_flow()
    beta = act_beta()
    eh = act_r342_exponents("ℏ")
    ec = act_r342_exponents("c")
    C = layer_c(build_fields(wls, beta, eh, ec))
    Cpos = layer_c(build_fields(wls, beta, eh, ec, mode="positive"))
    Cneg = layer_c(build_fields(wls, beta, eh, ec, mode="negative"))
    sens = sensitivity_outside(wls, beta, eh, ec)

    configs = [("baseline", gate_vector(D, C)),
               ("ctrl_pos", gate_vector(Dpos, Cpos)),
               ("ctrl_neg", gate_vector(Dneg, Cneg))]
    power = gate_power(configs)
    baseline_gates = configs[0][1]
    decisive_pass = sum(1 for nm in power["decisive"] if baseline_gates[nm])
    decisive_total = len(power["decisive"])

    cc = crosscheck()
    cc_by_key = {r["key"]: r for r in cc["rows"]}
    n_hc = ast_no_hardcode_ok()
    n_ea = ast_exp_act_distinct()
    n_rw = ast_readme_zero_write()
    n_se = self_exclusion_check()
    rdm = readme_snapshot()
    manifest = source_manifest()

    K = dict(
        r99_formula_count=act_r99_formula_count(),
        r99_universe_size=D["universe_size"],
        common_prerequisites=D["common_count"],
        min_hitting_set=D["min_hitting_set"],
        min_hitting_solutions=D["min_hitting_solutions"],
        best_single_coverage=D["best_single_coverage"],
        best_single_label=D["best_single_label"],
        renamed_min_hitting=renamed["min_hitting_set"],
        ctrl_d_pos_min_hitting=Dpos["min_hitting_set"],
        ctrl_d_neg_min_hitting=Dneg["min_hitting_set"],
        ctrl_d_pos_common=Dpos["common_count"],
        ctrl_d_neg_common=Dneg["common_count"],
        s17_combo_count=act_s17_combo_count(),
        s17_switch_count=act_s17_switch_count(),
        s17_max_fixed=act_s17_max_fixed(),
        s17_min_augmentation=act_s17_augmentation(),
        s17_total_items=int(load_json("s17")["总计"]),
        r141_fail_count=act_r141_fails(),
        r342_item_total=act_r342_item_total(),
        r342_hbar_exponents=[str(x) for x in eh],
        r342_c_exponents=[str(x) for x in ec],
        beta_text="、".join(str(x) for x in beta),
        wls_flow=[str(wls[0]), str(wls[1])],
        generic_rank_pointwise=C["generic_rank_pointwise"],
        rank_profiles=C["rank_profiles"],
        rank_profile_count=len(C["rank_profiles"]),
        poly_rank_initial=C["poly_rank_initial"],
        poly_rank_closure=C["poly_rank_closure"],
        closure_trace=C["closure_trace"],
        closure_rounds=C["closure_rounds"],
        closure_fields=C["closure_fields"],
        monomial_basis_size=C["monomial_basis_size"],
        bracket_pairs=C["bracket_pairs"],
        nonzero_brackets=C["nonzero_brackets"],
        brackets_outside_span=C["brackets_outside_span"],
        ctrl_c_pos_grank=Cpos["generic_rank_pointwise"],
        ctrl_c_pos_outside=Cpos["brackets_outside_span"],
        ctrl_c_neg_grank=Cneg["generic_rank_pointwise"],
        ctrl_c_neg_outside=Cneg["brackets_outside_span"],
        ctrl_c_neg_closure=Cneg["poly_rank_closure"],
        sensitivity_outside=sens,
        decisive_gates=power["decisive_count"],
        decorative_gates=power["decorative_count"],
        decisive_pass=decisive_pass,
        decisive_total=decisive_total,
        crosscheck_match=cc["match"],
        crosscheck_total=cc["total"],
        r99_text_machine_keys=cc["r99_text_machine_keys"],
        guards_add_scanned=n_hc["scanned"],
        act_func_count=len(n_ea["act_funcs"]),
        exp_func_count=len(n_ea["exp_funcs"]),
        own_expected=n_se["expected"],
        own_missed=len(n_se["missed"]),
        readme_bytes=rdm["bytes"],
        readme_max_rid=rdm["max_rid"],
        tree_max_rid=rdm["tree_max_rid"],
        clean_zero_count=0,
        independent_predictions=0,
    )
    verdict = verdict_of(K)
    K["verdict"] = verdict
    K["verdict_machine_shift"] = verdict_of(dict(K, min_hitting_set=K["min_hitting_set"] + 1))

    # ---------------- 守卫注册（ok 全部由读数驱动） ----------------
    add("ANCHOR-UNIQUE", len(_anchor_hits) == 1, "唯一锚点定位主目录")
    add("SRC-FILES-PRESENT", all(os.path.isfile(os.path.join(DATA, n)) for n in SRC_FILES.values()),
        "来料文件齐全")
    add("README-SNAPSHOT-VALID", rdm["bytes"] > 0 and rdm["max_rid"] > 0, "README 实时读数")
    add("README-ZERO-WRITE-AST", n_rw["ok"], "AST 结构性零写入", "structural")
    add("D-FORMULA-COUNT-MATCH", act_r99_formula_count() == int(load_json("r99")["counts"]["total"]),
        "公式数与册内总计一致")
    add("D-UNIVERSE-COVERED-BY-CHECKCODES",
        all(u in act_r99_check_codes() for u in D["universe"]),
        "依赖对象全部落在 r99 检查码清单内")
    add("D-NO-COMMON-PREREQ", D["common_count"] == 0, "无共同外部前提")
    add("D-MINHIT-GT1", D["min_hitting_set"] > 1, "最小外部前提集大于一")
    add("D-MINHIT-SOLUTIONS-POSITIVE", D["min_hitting_solutions"] > 0, "最优解非空")
    add("D-RENAME-INVARIANT", renamed["min_hitting_set"] == D["min_hitting_set"],
        "纯改名不改图结构", "identity")
    add("D-CTRL-POS-SINGLE", Dpos["single_generator_possible"], "正对照单生成元可行")
    add("D-CTRL-NEG-DIFFERS", Dneg["min_hitting_set"] != D["min_hitting_set"],
        "跨册错配改变读数")
    add("D-CTRL-READINGS-DISTINCT",
        len({D["min_hitting_set"], Dpos["min_hitting_set"], Dneg["min_hitting_set"]}) == 3,
        "三配置读数两两不同")
    add("S17-COMBO-MATCH", cc_by_key["s17_combo_count"]["match"], "16 种口径组合两路一致")
    add("S17-MAXFIXED-MATCH", cc_by_key["s17_max_fixed"]["match"], "最大修复后通过两路一致")
    add("S17-AUG-MATCH", cc_by_key["s17_augmentation"]["match"], "最小增广集两路一致")
    add("S17-SWITCH-COUNT", act_s17_switch_count() == 4, "口径开关四路")
    add("S17-AUG-LT-FORMULAS", act_s17_augmentation() < act_s17_combo_count(),
        "增广条数小于组合数")
    add("S17-MAXFIXED-LT-TOTAL", act_s17_max_fixed() < int(load_json("s17")["总计"]),
        "最优组合仍不能全通过")
    add("C-EXPONENTS-LENGTH", len(eh) == N and len(ec) == N, "量纲指数为三维向量")
    add("C-PROFILES-ALL-MAX",
        all(r == C["generic_rank_pointwise"] for r in C["rank_profiles"])
        and len(C["rank_profiles"]) >= 4, "六剖面全达泛秩，非退化")
    add("C-GRANK-GT1", C["generic_rank_pointwise"] > 1, "逐点分布维数大于一")
    add("C-BRACKET-NONZERO", C["nonzero_brackets"] > 0, "存在非零交换子")
    add("C-NOT-INVOLUTIVE", C["brackets_outside_span"] > 0, "交换子跳出生成元张成空间")
    add("C-CLOSURE-GROWS", C["closure_grows"], "Lie 闭包增加新方向")
    add("C-POLY-RANK-INITIAL", C["poly_rank_initial"] == C["field_count"],
        "四个生成元在多项式方向场空间线性无关")
    add("C-SENSITIVITY-STABLE", all(v == C["brackets_outside_span"] for v in sens),
        "三档系数扰动下判词稳定")
    add("C-CTRL-POS-SINGLE", Cpos["generic_rank_pointwise"] == 1, "正对照泛秩为一")
    add("C-CTRL-POS-INVOLUTIVE", Cpos["involutive"], "正对照对合")
    add("C-CTRL-NEG-DIFFERS", Cneg["brackets_outside_span"] != C["brackets_outside_span"] or
        Cneg["poly_rank_closure"] != C["poly_rank_closure"], "旋转场位移改变读数")
    add("C-CTRL-READINGS-DISTINCT",
        len({C["brackets_outside_span"], Cpos["brackets_outside_span"],
             Cneg["brackets_outside_span"]}) >= 2, "控制组至少两个不同读数")
    add("GATE-POWER-ALL-DECISIVE", power["decorative_count"] == 0,
        "无 100% 或 0% 装饰判据")
    add("GATE-DECISIVE-ALL-PASS", decisive_pass == decisive_total and decisive_total > 0,
        "全部有判别力门在基线判负方向成立")
    add("VERDICT-MACHINE", K["verdict_machine_shift"] != K["verdict"],
        "读数加一后判词串变化")
    add("CROSSCHECK-ALL-MATCH", cc["match"] == cc["total"], "两路机拼全一致")
    add("CROSSCHECK-BETA-CROSS-BOOK", cc_by_key["beta_text_cross_book"]["match"] and
        SRC_FILES["beta"] != SRC_FILES["r20_report"], "跨册独立 beta 口径一致")
    add("NO-HARDCODE-OK", n_hc["ok"], "守卫 ok 非字面量")
    add("EXP-ACT-DISTINCT-AST", n_ea["ok"], "两路函数族不同且非常量返回")
    add("SELF-EXCLUSION", n_se["ok"], "本册产物全部排除")
    add("R141-PHYSICS-FAILS", act_r141_fails() > 0, "独立册物理层已判负")
    add("SOURCE-MANIFEST-NONEMPTY", len(manifest) == len(SRC_FILES), "来料清单完整")

    add_identity("D-RENAME-IDENTITY", "纯双射改名不改变最小外部前提集，按定义恒真，只作归因不作证据")
    add_identity("C-CLOSURE-MONOTONE", "Lie 闭包秩随迭代单调不减是构造性质，单列")
    add_identity("CROSSCHECK-SAME-BOOK", "同源存档两路机拼只抓序列化错，不是独立复算")
    add_boundary("BOUNDARY-DEPENDENCE-GRAPH", "r99 的 deps 是公式对外部检查码的依赖，不是公式间推导图")
    add_boundary("BOUNDARY-FORMAL-FIELDS", "层 C 是把既有读数形式化为状态空间方向场，不构成新物理理论")
    add_boundary("BOUNDARY-ONE-LOOP-AND-ROUNDING", "只覆盖一圈 beta、R22 九位登记系数与有限轮 Lie 闭包")
    add_info("RED-LINE-NO-CLAIM", "数学自洽不等于实验证实；四力统一未证；独立实验预言 0；不宣称攻破统一场论")
    add_info("NON-ADDITIVITY", "层 D 与层 C 是不同对象，读数不相加、不互相替代")

    declared_negative = [
        "单一生成元形式判负：23 条公式无共同外部前提，最小外部前提集为 %d" % D["min_hitting_set"],
        "连续生成元形式判负：逐点分布泛秩 %d，非零交换子 %d 个，其中 %d 个跳出张成空间" %
        (C["generic_rank_pointwise"], C["nonzero_brackets"], C["brackets_outside_span"]),
        "Lie 闭包生成元不灭：多项式方向场秩 %d 增至 %d" %
        (C["poly_rank_initial"], C["poly_rank_closure"]),
        "S17 口径组合枚举 16 种仍不能闭合，最小增广集 %d 条" % act_s17_augmentation(),
    ]
    st = guard_stats()
    final = final_of(decisive_total - decisive_pass, st["fail"], len(declared_negative))

    doc = dict(
        title="算法联盟第二十三轮：核心公式体系的单一生成元可积性审计（依赖图与 Lie 交换子）",
        date=DATE, nature="可算判决（形式层），不产新物理",
        final=final, verdict=verdict, guard_count=st["count"],
        guard_pass=st["pas"], guards=GUARDS, counts=st["kinds"],
        key_numbers=K,
        layer_d=dict(D, renamed_min_hitting=renamed["min_hitting_set"],
                     positive_control=Dpos, negative_control=Dneg),
        layer_c=dict(C, positive_control=Cpos, negative_control=Cneg,
                     sensitivity_outside=sens),
        gate_power=power,
        gate_baseline=baseline_gates,
        crosscheck=cc,
        identity_notes=[g["note"] for g in GUARDS if g["kind"] == "IDENTITY"],
        boundary_notes=[g["note"] for g in GUARDS if g["kind"] == "BOUNDARY"],
        info_notes=[g["note"] for g in GUARDS if g["kind"] == "INFO"],
        declared_negative=declared_negative,
        red_line="数学自洽不等于实验证实；四力统一未证；独立实验预言 0；不宣称攻破统一场论",
        readme=rdm, source_files=manifest,
    )
    doc["content_sha256"] = canonical_sha(doc)

    body = json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True, default=str)
    open(OUT_JSON, "w", encoding="utf-8").write(body)

    lines = [
        "算法联盟：核心公式体系的单一生成元可积性审计（第二十三轮）",
        "=" * 96,
        "verdict : " + verdict,
        "final   : " + final,
        "counts  : " + json.dumps(st["kinds"], ensure_ascii=False, sort_keys=True),
        "guards  : %d/%d" % (st["pas"], st["count"]),
        "sha256  : " + doc["content_sha256"],
        "-" * 96,
        "[MACHINE-TABLE]",
    ]
    for k in sorted(K.keys()):
        lines.append("%s = %s" % (k, json.dumps(K[k], ensure_ascii=False, sort_keys=True)))
    lines += ["-" * 96, "[DECLARED-NEGATIVE]"] + ["- " + s for s in declared_negative]
    lines += ["-" * 96, "[BOUNDARY]"] + ["- " + s for s in doc["boundary_notes"]]
    lines += ["-" * 96, "[RED-LINE]", doc["red_line"]]
    open(OUT_REPORT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return doc


if __name__ == "__main__":
    d = main()
    print("FINAL =", d["final"])
    print("VERDICT =", d["verdict"])
    print("GUARDS = %d/%d" % (d["guard_pass"], d["guard_count"]))
    print("COUNTS =", json.dumps(d["counts"], ensure_ascii=False, sort_keys=True))
    print("LAYER-D minhit =", d["key_numbers"]["min_hitting_set"],
          "LAYER-C grank =", d["key_numbers"]["generic_rank_pointwise"],
          "outside =", d["key_numbers"]["brackets_outside_span"])
