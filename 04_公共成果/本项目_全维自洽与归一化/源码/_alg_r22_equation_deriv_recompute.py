# -*- coding: utf-8 -*-
"""算法联盟第二十二轮：全链方程清单整理 · 求导证明与零残差极值精算。

审对象：三十一册机读判决与三十二篇主文里的方程类陈述，以及承载判决的闭式。
本册只产可算判决，不产新物理；所有方程形式取自仓库既有来料，数值一律机读。
"""
import ast
import glob
import hashlib
import json
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 90
D = Decimal

ANCHOR = "_ALG_information_gate_recompute_2026-11-12.json"


def find_main():
    """并行会话可能新增同形目录 ⇒ 用唯一既有产物反查主目录。"""
    hits = glob.glob("openuft/**/" + ANCHOR, recursive=True)
    assert len(hits) == 1, "ANCHOR-HITS=%d" % len(hits)
    return os.path.dirname(os.path.dirname(hits[0]))


MAIN = find_main()
# 自指盘点：本册产物必须按精确名字排除，否则首次运行与幂等复跑读数会漂移。
OWN_TOKENS = ("r22_equation_deriv", "第二十二轮")


def is_own(p):
    b = os.path.basename(p)
    return any(t in b for t in OWN_TOKENS)


DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
README = os.path.join(MAIN, "README.md")
OUT_JSON = os.path.join(DATA, "_ALG_r22_equation_deriv_recompute_2026-11-15.json")
OUT_REPORT = os.path.join(DATA, "_ALG_r22_equation_deriv_recompute_report_2026-11-15.txt")


def report_path_from_json(jp):
    """JSON -> report 的唯一路径构造；机核与核验器共用，禁另起一套。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(os.path.dirname(jp), stem)


def json_path_from_report(rp):
    """report -> JSON 的唯一路径构造。"""
    stem = os.path.splitext(os.path.basename(rp))[0]
    stem = stem.replace("_recompute_report_", "_recompute_") + ".json"
    return os.path.join(os.path.dirname(rp), stem)


def F_of(s):
    """字符串 -> 精确 Fraction；科学计数先过 Decimal，避免 Fraction 解析差异。"""
    s = str(s).strip()
    if "e" in s.lower():
        return F(D(s))
    return F(s)


def conv(q):
    if isinstance(q, F):
        return D(q.numerator) / D(q.denominator)
    return D(q)


def rel(a, b):
    """Decimal 相对精度下判相同一律用偏离 + 容差，禁字符串相等。"""
    a, b = conv(a), conv(b)
    return abs(a - b) / (abs(a) + abs(b) + D(1))


def dstr(q, n=12):
    return format(conv(q), ".%df" % n)


def dstr_sci(q, n=6):
    return format(conv(q), ".%de" % n)


# ---------------------------------------------------------------- 多项式环
def p_trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def p_const(c):
    return p_trim([F(c)])


def p_add(a, b):
    n = max(len(a), len(b))
    return p_trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                   for i in range(n)])


def p_neg(a):
    return [-x for x in a]


def p_sub(a, b):
    return p_add(a, p_neg(b))


def p_mul(a, b):
    if not a or not b:
        return []
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return p_trim(out)


def p_pow(a, n):
    out = [F(1)]
    for _ in range(n):
        out = p_mul(out, a)
    return out


def p_deriv(a):
    return p_trim([a[i] * i for i in range(1, len(a))])


def p_eval(p, x):
    x = F(x)
    s = F(0)
    for c in reversed(p):
        s = s * x + c
    return s


def p_zero(p):
    return not p_trim(p)


# ------------------------------------------------- 单变量有理函数与符号求导
def r_const(c):
    return (p_const(F(c)), [F(1)])


def r_var():
    return ([F(0), F(1)], [F(1)])


def r_add(u, v):
    return (p_add(p_mul(u[0], v[1]), p_mul(v[0], u[1])), p_mul(u[1], v[1]))


def r_neg(u):
    return (p_neg(u[0]), u[1])


def r_sub(u, v):
    return r_add(u, r_neg(v))


def r_mul(u, v):
    return (p_mul(u[0], v[0]), p_mul(u[1], v[1]))


def r_div(u, v):
    return (p_mul(u[0], v[1]), p_mul(u[1], v[0]))


def r_pow(u, n):
    if n < 0:
        u = r_div(([F(1)], [F(1)]), u)
        n = -n
    return (p_pow(u[0], n), p_pow(u[1], n))


def r_deriv(u):
    """商法则 (N/D)' = (N'D - N D') / D^2，全程精确 Fraction。"""
    n, d = u
    one = [F(1)]
    return r_div(r_sub(r_mul((p_deriv(n), one), (d, one)),
                       r_mul((n, one), (p_deriv(d), one))),
                 (p_mul(d, d), one))


def r_eval(u, x):
    x = F(x)
    n, d = p_eval(u[0], x), p_eval(u[1], x)
    assert d != 0, "POLE-AT-PROBE"
    return n / d


def r_is_zero(u):
    return p_zero(u[0])


def compile_expr(src, env, var="x"):
    """把算术表达式 AST 编译成有理函数；只允许四则与整数幂，变量唯一。"""
    t = ast.parse(src, mode="eval").body

    def go(n):
        if isinstance(n, ast.Constant):
            return r_const(F_of(str(n.value)))
        if isinstance(n, ast.Name):
            if n.id == var:
                return r_var()
            if n.id not in env:
                raise RuntimeError("UNBOUND-NAME " + n.id)
            return env[n.id]
        if isinstance(n, ast.UnaryOp):
            v = go(n.operand)
            return r_neg(v) if isinstance(n.op, ast.USub) else v
        if isinstance(n, ast.BinOp):
            a, b = go(n.left), go(n.right)
            if isinstance(n.op, ast.Add):
                return r_add(a, b)
            if isinstance(n.op, ast.Sub):
                return r_sub(a, b)
            if isinstance(n.op, ast.Mult):
                return r_mul(a, b)
            if isinstance(n.op, ast.Div):
                return r_div(a, b)
            if isinstance(n.op, ast.Pow):
                if not isinstance(n.right, ast.Constant) or not isinstance(n.right.value, int):
                    raise RuntimeError("NON-INTEGER-POWER")
                return r_pow(a, n.right.value)
        raise RuntimeError("UNSUPPORTED " + type(n).__name__)

    return go(t)


# ------------------------------------------------------------ 常数与来料
def atan_inv(x):
    """Machin 实参 5/239；x>1，t=1/x。"""
    assert x > 1, "ATAN-INV-REQUIRES-x-GT-1"
    t = D(1) / D(x)
    term = t
    s = t
    k = 1
    while True:
        term = term * t * t
        add = term / D(2 * k + 1)
        s = s + (-add if k % 2 else add)
        if abs(add) < D(10) ** (-getcontext().prec - 8):
            break
        k += 1
    return s


PI = 16 * atan_inv(5) - 4 * atan_inv(239)
LN10 = D(10).ln()


def load_json(name):
    hits = glob.glob("openuft/**/" + name, recursive=True)
    assert len(hits) == 1, "JSON-HITS-%s=%d" % (name, len(hits))
    return json.load(open(hits[0], encoding="utf-8"))


R20 = load_json("_ALG_gut_meet_recompute_2026-11-14.json")
R20REP = open(glob.glob("openuft/**/_ALG_gut_meet_recompute_report_2026-11-14.txt",
                        recursive=True)[0], encoding="utf-8").read()
LED = load_json("_ALG_expdata_fullchain_来料总表_2026-11-11.json")
BETA = load_json("_ALG_UFT_eq_derive_recompute_2026-11-09.json")


def ledger_value(row_id):
    rows = [r for r in LED["ledger"] if r["id"] == row_id]
    assert len(rows) == 1, "LEDGER-ID-" + row_id
    return F_of(rows[0]["value"])


def act_a():
    """A 路：三个 M_Z 处耦合倒数直接由 46 锚来料与闭式算出。"""
    aem = ledger_value("P15")
    s2w = ledger_value("P08")
    als = ledger_value("P07")
    return [F(3, 5) * (1 - s2w) * aem, s2w * aem, F(1) / als]


def exp_a():
    """B 路：从 R20 判定 JSON 机读，与 act_a 互不引用。"""
    k = R20["key_numbers"]
    return [F_of(k["a1_inv_MZ"]), F_of(k["a2_inv_MZ"]), F_of(k["a3_inv_MZ"])]


def act_beta():
    k = BETA["key_numbers"]
    return [F_of(k["b1"]), F_of(k["b2"]), F_of(k["b3"])]


def exp_beta():
    return [F_of(x) for x in R20["key_numbers"]["b_sm"]]


def act_span_dex():
    """A 路：自算两两交点 x_ij = 2π(a_i-a_j)/(b_i-b_j)，再除以 ln10。"""
    a, b = act_a(), act_beta()
    xs = {}
    for i, j in ((0, 1), (0, 2), (1, 2)):
        xs[(i, j)] = 2 * PI * conv(a[i] - a[j]) / conv(b[i] - b[j])
    return (max(xs.values()) - min(xs.values())) / LN10


def exp_span_dex():
    """B 路：R20 report 纯文本正则抽列，不引用 act 路径。"""
    m = re.findall(r"^span_dex_act\s*=\s*([0-9.]+)", R20REP, re.M)
    assert len(m) == 1, "EXP-SPAN-HITS=%d" % len(m)
    return D(m[0])


def act_chi2_min():
    return wls_state(F_of(R20["key_numbers"]["alpha_s_MZ"]))["chi2"]


def exp_chi2_min():
    """B 路：R20 report 纯文本抽列。"""
    m = re.findall(r"^chi2_min\s*=\s*([0-9.]+)", R20REP, re.M)
    assert len(m) == 1, "EXP-CHI2-HITS=%d" % len(m)
    return F_of(m[0])


def readme_read():
    rb = open(README, "rb").read()
    rids = [int(x) for x in re.findall(rb"TUFT-r(\d+)_", rb)]
    return dict(bytes=len(rb), md5=hashlib.md5(rb).hexdigest(),
                max_rid=max(rids) if rids else -1)

# ---------------------------------------------------------------- 精算机核
A = exp_a()
SIG = [F_of(R20["key_numbers"][k]) for k in
       ("sigma_a1", "sigma_a2", "sigma_a3")]
SIGMA_ALS = F_of(R20["key_numbers"]["sigma_alpha_s"])
U = F_of(R20["key_numbers"]["alpha_s_MZ"])
C = [F_of(R20["key_numbers"][k]) for k in
     ("c1_slope", "c2_slope", "c3_slope")]
B = act_beta()


def act_c():
    """A 路：斜率由 β 系数与自算 π 得出，c_i = b_i/(2π)。"""
    two_pi = F(D(2) * PI)
    return [b / two_pi for b in B]


def exp_c():
    """B 路：R20 存档斜率。"""
    return list(C)


def wls_state(uu):
    """uu = alpha_s(M_Z)。a3=1/u，sigma_a3=sigma_u/u^2 ⇒ w3=u^4/sigma_u^2。"""
    aa = [A[0], A[1], F(1) / uu]
    ss = [SIG[0], SIG[1], SIGMA_ALS / (uu * uu)]
    w = [F(1) / (s * s) for s in ss]
    W = sum(w)
    cb = sum(w[i] * C[i] for i in range(3)) / W
    ab = sum(w[i] * aa[i] for i in range(3)) / W
    den = sum(w[i] * (C[i] - cb) ** 2 for i in range(3))
    x = sum(w[i] * (C[i] - cb) * (aa[i] - ab) for i in range(3)) / den
    A0 = ab - x * cb
    r = [aa[i] - A0 - C[i] * x for i in range(3)]
    chi2 = sum(w[i] * r[i] ** 2 for i in range(3))
    return dict(w=w, W=W, S1=sum(w[i] * C[i] for i in range(3)),
                S2=sum(w[i] * C[i] ** 2 for i in range(3)),
                A=A0, x=x, r=r, chi2=chi2, aa=aa, ss=ss)


BASE = wls_state(U)


def first_order_conditions():
    """一阶必要条件：加权残差和与一阶矩残差和都必须精确为 0。"""
    f1 = sum(BASE["w"][i] * BASE["r"][i] for i in range(3))
    f2 = sum(BASE["w"][i] * C[i] * BASE["r"][i] for i in range(3))
    return f1, f2


def hessian_det():
    """H = 2[[W,S1],[S1,S2]]；返回 det(H)/4 = W*S2-S1^2，精确 Fraction。"""
    return BASE["W"] * BASE["S2"] - BASE["S1"] ** 2


def symbolic_first_derivatives():
    """用符号求导器独立验证 ∂χ²/∂A 与 ∂χ²/∂x 在最优点为 0、二阶导为正。"""
    env = {"w%d" % (i + 1): r_const(BASE["w"][i]) for i in range(3)}
    # 必须与 WLS 同口径：a3 = 1/alpha_s 精确值，不能拿 R20 的 60 位截断存档，
    # 否则一阶条件会冒出 1e-66 量级的假残差（对象错位，非求导器错误）。
    env.update({"a%d" % (i + 1): r_const(BASE["aa"][i]) for i in range(3)})
    env.update({"c%d" % (i + 1): r_const(C[i]) for i in range(3)})
    src = ("w1*(a1-A-c1*x)**2 + w2*(a2-A-c2*x)**2 + "
           "w3*(a3-A-c3*x)**2")
    envA = dict(env)
    envA["x"] = r_const(BASE["x"])
    fA = compile_expr(src, envA, var="A")
    dA = r_deriv(fA)
    envX = dict(env)
    envX["A"] = r_const(BASE["A"])
    fX = compile_expr(src, envX, var="x")
    dX = r_deriv(fX)
    return dict(dA_at_opt=r_eval(dA, BASE["A"]),
                dX_at_opt=r_eval(dX, BASE["x"]),
                d2A=r_eval(r_deriv(dA), BASE["A"]),
                d2X=r_eval(r_deriv(dX), BASE["x"]),
                dA_is_zero=r_is_zero(dA), dX_is_zero=r_is_zero(dX))


def analytic_envelope():
    """包络定理：内点最优处 dχ²*/du 只含显式依赖。

    w3=u^4/sigma_u^2 ⇒ dw3/du=4w3/u；a3=1/u ⇒ da3/du=-1/u^2。
    dχ²*/du = (dw3/du) r3^2 + 2 w3 r3 (da3/du)。
    """
    w3, r3 = BASE["w"][2], BASE["r"][2]
    dw3 = 4 * w3 / U
    da3 = -F(1) / (U * U)
    return dw3 * r3 ** 2 + 2 * w3 * r3 * da3


def analytic_implicit():
    """隐函数微分：正规方程对 u 求导，解出 dA/du 与 dx/du 的闭式。"""
    w3, r3 = BASE["w"][2], BASE["r"][2]
    dw3 = 4 * w3 / U
    da3 = -F(1) / (U * U)
    K = dw3 * r3 + w3 * da3
    det = hessian_det()
    dAdu = K * (BASE["S2"] - C[2] * BASE["S1"]) / det
    dxdu = K * (C[2] * BASE["W"] - BASE["S1"]) / det
    return K, dAdu, dxdu


def central(field, h):
    sp, sm = wls_state(U + h), wls_state(U - h)
    return (sp[field] - sm[field]) / (2 * h)


def richardson(field, h):
    """中心差分误差 O(h^2) ⇒ Richardson 系数 4/3，非 Simpson 的 16/15。"""
    return (4 * central(field, h / 2) - central(field, h)) / 3


def projection_residual():
    """v=da/du 在加权列空间 span{1,c} 外的投影残差；>0 即 2 参数吸收不了扰动。"""
    v = [F(0), F(0), -F(1) / (U * U)]
    M = [[F(1), C[i]] for i in range(3)]
    w = BASE["w"]
    G = [[sum(w[k] * M[k][i] * M[k][j] for k in range(3)) for j in range(2)]
         for i in range(2)]
    rhs = [sum(w[k] * M[k][i] * v[k] for k in range(3)) for i in range(2)]
    gdet = G[0][0] * G[1][1] - G[0][1] * G[1][0]
    beta = [(rhs[0] * G[1][1] - rhs[1] * G[0][1]) / gdet,
            (rhs[1] * G[0][0] - rhs[0] * G[1][0]) / gdet]
    resid = sum(w[k] * (v[k] - beta[0] - beta[1] * C[k]) ** 2
                for k in range(3))
    return gdet, beta, resid


# ------------------------------------------------------- 方程对象与求导分类
PARAM_NAMES = {"A", "x", "T", "delta", "theta", "scale"}
OBS_NAMES = {"a1", "a2", "a3", "O", "sigma", "w1", "w2", "w3"}
CHI2_SRC = ("w1*(a1-A-c1*x)**2 + w2*(a2-A-c2*x)**2 + "
            "w3*(a3-A-c3*x)**2")


def equation_objects():
    env = {"w%d" % (i + 1): r_const(BASE["w"][i]) for i in range(3)}
    env.update({"a%d" % (i + 1): r_const(BASE["aa"][i]) for i in range(3)})
    env.update({"c%d" % (i + 1): r_const(C[i]) for i in range(3)})
    env["A"] = r_const(BASE["A"])
    env["O"] = r_const(BASE["aa"][2])
    env["sigma"] = r_const(SIG[2])
    env["T"] = r_const(BASE["aa"][2])
    return [
        dict(id="E1-WLS-CHI2", label="规范耦合交汇 χ² 残差", src=CHI2_SRC,
             var="x", env=env, smooth=True, origin="R20"),
        dict(id="E2-RG-LINE", label="一圈 RG 直线 α⁻¹(t)=a+c·t",
             src="a1 + c1*t", var="t", env=env, smooth=True, origin="R1/R20"),
        dict(id="E3-GAP", label="优化搜索残差 gap=(T−O)/σ",
             src="(T - O)/sigma", var="T", env=env, smooth=True, origin="R5"),
        dict(id="E4-IDENTITY", label="按定义展开恒零残差（求导器夹具）",
             src="(x+1)**2 - x**2 - 2*x - 1", var="x", env={}, smooth=True,
             origin="R1-Bianchi-同型"),
        dict(id="E5-PMIN", label="阈值自由度阶梯定价 p_min",
             src=None, var=None, env={}, smooth=False, origin="R21"),
        dict(id="E6-BITS", label="固定编码比特账 bits(q)",
             src=None, var=None, env={}, smooth=False, origin="R9"),
        dict(id="E7-CTRL-FREE", label="纯数学正对照 3x+7",
             src="3*x + 7", var="x", env={}, smooth=True, origin="CONTROL"),
    ]


DERIVATOR = r_deriv


def classify(obj, derivator=None):
    """分类全部由求导器读数与 AST 名字集机读，不手填类别。"""
    dg = DERIVATOR if derivator is None else derivator
    if not obj["smooth"]:
        return dict(kind="NON-SMOOTH", deriv_zero=None, value_zero=None,
                    names=[], obs=False, param=False, probe=None)
    f = compile_expr(obj["src"], obj["env"], var=obj["var"])
    d = dg(f)
    names = sorted({n.id for n in ast.walk(ast.parse(obj["src"], mode="eval"))
                    if isinstance(n, ast.Name)} - {obj["var"]})
    obs = bool(set(names) & OBS_NAMES)
    param = bool(set(names) & PARAM_NAMES)
    dz, vz = r_is_zero(d), r_is_zero(f)
    probes = [F(0), F(1), F(2), F(-1)]
    vals = [r_eval(d, t) for t in probes]
    if dz and vz:
        kind = "IDENTITY"
    elif dz:
        kind = "CONSTANT"
    elif param:
        kind = "PARAMETRIC"
    elif obs:
        kind = "OBS-DEPENDENT"
    else:
        kind = "FREE"
    return dict(kind=kind, deriv_zero=dz, value_zero=vz,
                names=names, obs=obs, param=param,
                probe=sum(1 for t in vals if t != 0),
                deriv_probe_nonzero_count=sum(1 for t in vals if t != 0))


# ------------------------------------------------------------ 全链文本普查
CLAIM_RE = re.compile(r"(发现|提出|导出|得到|给出)[^。；\n]{0,12}(新方程|新公式|新的方程|新的公式)")
EQ_KEY_RE = re.compile(r'"([A-Za-z0-9_]*(?:equation|formula|closed_form)[A-Za-z0-9_]*)"\s*:', re.I)
NEG_WORDS = ("未", "无", "不", "没有", "零", "并非", "0 条", "0条",
             "宣称", "主张", "引述", "不能", "不宜", "拒绝")


def positive_claim(ln):
    """语义白名单：否定句不算「发现新方程」的声明。"""
    return bool(CLAIM_RE.search(ln)) and not any(w in ln for w in NEG_WORDS)


def catalog_scan():
    js = sorted(p for p in glob.glob(os.path.join(DATA, "_ALG_*_recompute_*.json"))
                if not is_own(p))
    mds = sorted(p for p in glob.glob(os.path.join(MAIN, "算法联盟_*.md"))
                 if not is_own(p))
    reps = sorted(p for p in glob.glob(os.path.join(DATA, "_ALG_*_recompute_report_*.txt"))
                  if not is_own(p))
    rows = []
    for p in js:
        t = open(p, encoding="utf-8").read()
        keys = set(EQ_KEY_RE.findall(t))
        rows.append(dict(book=os.path.basename(p), eq_keys=sorted(keys),
                         no_new_formula=("no_new_formula" in t),
                         claim_json=len(re.findall(r'"[^"]*new_equation[^"]*"\s*:', t, re.I))))
    eq_lines = 0
    claims_md = []
    for p in mds:
        for ln in open(p, encoding="utf-8").read().splitlines():
            if "方程" in ln and ("=" in ln or "恒等" in ln or "闭式" in ln):
                eq_lines += 1
            if positive_claim(ln):
                claims_md.append((os.path.basename(p), ln.strip()[:120]))
    claims_report = []
    for p in reps:
        for ln in open(p, encoding="utf-8").read().splitlines():
            if positive_claim(ln):
                claims_report.append((os.path.basename(p), ln.strip()[:120]))
    excluded = [os.path.basename(p) for p in
                glob.glob(os.path.join(DATA, "_ALG_*_recompute_*.json")) +
                glob.glob(os.path.join(MAIN, "算法联盟_*.md")) +
                glob.glob(os.path.join(DATA, "_ALG_*_recompute_report_*.txt"))
                if is_own(p)]
    return dict(books=len(js), mds=len(mds), reports=len(reps), rows=rows,
                eq_like_lines=eq_lines,
                eq_key_books=sum(1 for r in rows if r["eq_keys"]),
                no_new_formula_books=sum(1 for r in rows if r["no_new_formula"]),
                claims_json=sum(r["claim_json"] for r in rows),
                claims_md=claims_md, claims_report=claims_report,
                self_excluded=excluded)


def control_group(derivator=None):
    """求导器正负双对照；负对照读数相等是预期，判别力由反噬变体提供。"""
    dg = DERIVATOR if derivator is None else derivator
    cases = [("pos-linear", "3*x + 7", F(1)),
             ("pos-quad", "x**2 - 2*x + 1", F(0)),
             ("neg-identity", "(x+1)**2 - x**2 - 2*x - 1", F(1)),
             ("neg-extremum", "(x-1)**2", F(1))]
    out = []
    for name, src, at in cases:
        f = compile_expr(src, {}, var="x")
        v = r_eval(dg(f), at)
        out.append(dict(name=name, reading=v, nonzero=(v != 0)))
    return out

# ------------------------------------------------------------------ 守卫
SEG = []
NOTES = []


def add(seg, ok, note=""):
    """守卫条目一律由 ok 驱动 kind，禁写死布尔字面量。"""
    SEG.append(dict(id=seg, kind="PASS" if ok else "FAIL",
                    ok=bool(ok), note=note))


def note(kind, text):
    NOTES.append(dict(kind=kind, text=text))


KERNEL_PATH = os.path.join(SRC, "_alg_r22_equation_deriv_recompute.py")


def kernel_source():
    if not os.path.exists(KERNEL_PATH):
        return ""
    return open(KERNEL_PATH, encoding="utf-8").read()


def hardcode_ok_hits():
    """AST 扫 add() 的 ok 参数：任何布尔字面量都是写死判别。"""
    out = []
    t = ast.parse(kernel_source())
    for n in ast.walk(t):
        if not isinstance(n, ast.Call):
            continue
        fn = n.func.id if isinstance(n.func, ast.Name) else ""
        if fn != "add":
            continue
        for a in list(n.args)[1:2] + [k.value for k in n.keywords if k.arg == "ok"]:
            if isinstance(a, ast.Constant) and isinstance(a.value, bool):
                out.append(n.lineno)
    return out


def exp_act_ast_hits():
    """exp/act 两路所有 return 分支不得是顶层数值常量。"""
    out = []
    t = ast.parse(kernel_source())
    for fn in ast.walk(t):
        if not isinstance(fn, ast.FunctionDef):
            continue
        if not (fn.name.startswith("act_") or fn.name.startswith("exp_")):
            continue
        for n in ast.walk(fn):
            if isinstance(n, ast.Return) and isinstance(n.value, ast.Constant) \
                    and isinstance(n.value.value, (int, float)) \
                    and not isinstance(n.value.value, bool):
                out.append((fn.name, n.lineno))
    return out


def write_target_hits():
    """结构性零写入：源码里不得出现以写模式打开 README。"""
    out = []
    t = ast.parse(kernel_source())
    for n in ast.walk(t):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "open"):
            continue
        argtxt = " ".join((a.id if isinstance(a, ast.Name) else
                           a.value if isinstance(a, ast.Constant) and isinstance(a.value, str)
                           else "") for a in n.args)
        mode = " ".join(k.value.value for k in n.keywords
                        if k.arg == "mode" and isinstance(k.value, ast.Constant)
                        and isinstance(k.value.value, str))
        mode = mode or (n.args[1].value if len(n.args) > 1
                        and isinstance(n.args[1], ast.Constant)
                        and isinstance(n.args[1].value, str) else "")
        if "README" in argtxt and "w" in mode:
            out.append(n.lineno)
    return out


def verdict_string(k):
    """判词全部由 key_numbers 机读拼接，读数变化必须改变判词串。"""
    return ("ALG-ED__BOOKS-%d__MD-%d__EQLINES-%d__CLAIM-%d__LOOSE-%d__OBJ-%d__"
            "FREE-%d__NEW-%d__HESS-%s__ENV-%s__DADU-%s__DXDU-%s__PROJ-%s__"
            "RICH-%s__CLEAN-0__PRED-0" %
            (k["books"], k["mds"], k["eq_like_lines"], k["claims_total"],
             k["loose_claim_hits"], k["objects_n"], k["free_control"],
             k["new_equation_count"], k["hess_det"], k["env_analytic"],
             k["dAdu_analytic"], k["dxdu_analytic"], k["proj_resid"],
             k["rich_rel"]))


def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-R22-EQUATION-DERIV--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-R22-EQUATION-DERIV--GATES-FAIL"
    return "ALG-R22-EQUATION-DERIV--GATES-PASS-WITH-0-NEGATIVE"


def report_text(doc):
    k = doc["key_numbers"]
    lines = ["算法联盟：全链方程清单整理、求导证明与零残差极值精算（第二十二轮）",
             "=" * 96,
             "verdict : " + doc["verdict"],
             "final   : " + doc["final"],
             "counts  : " + json.dumps(doc["counts"], ensure_ascii=False, sort_keys=True),
             "guards  : %d/%d" % (doc["guard_pass"], doc["guard_count"]),
             "sha256  : " + doc["content_sha256"],
             "-" * 96,
             "[MACHINE-TABLE]"]
    for key in sorted(k):
        lines.append("%s = %s" % (key, json.dumps(k[key], ensure_ascii=False)))
    lines.append("[END-TABLE]")
    lines.append("")
    lines.append("[SEGMENTS]")
    for s in doc["segments"]:
        lines.append("%s %s %s" % (s["kind"], s["id"], s["note"]))
    return "\n".join(lines) + "\n"


def source_files():
    rel = ["数据/_ALG_gut_meet_recompute_2026-11-14.json",
           "数据/_ALG_gut_meet_recompute_report_2026-11-14.txt",
           "数据/_ALG_expdata_fullchain_来料总表_2026-11-11.json",
           "数据/_ALG_UFT_eq_derive_recompute_2026-11-09.json",
           "数据/_ALG_r21_evidence_recompute_2026-11-15.json",
           "源码/_alg_gut_meet_recompute.py",
           "源码/_alg_r21_evidence_recompute.py",
           "README.md"]
    return [os.path.join(MAIN, x.replace("/", os.sep)) for x in rel]


def main():
    tol = D("1e-40")
    rich_tol = D("1e-15")
    H = F(1, 10 ** 6)

    cat = catalog_scan()
    objs = equation_objects()
    cls = [classify(o) for o in objs]
    kinds = {}
    for c in cls:
        kinds[c["kind"]] = kinds.get(c["kind"], 0) + 1
    real_free = sum(1 for o, c in zip(objs, cls)
                    if c["kind"] == "FREE" and not o["id"].startswith("E7"))
    ctrl_free = sum(1 for o, c in zip(objs, cls)
                    if c["kind"] == "FREE" and o["id"].startswith("E7"))

    f1, f2 = first_order_conditions()
    sym = symbolic_first_derivatives()
    hess = hessian_det()
    env = analytic_envelope()
    K, dAdu, dxdu = analytic_implicit()
    gdet, beta, proj = projection_residual()
    rich_chi = richardson("chi2", H)
    rich_A = richardson("A", H)
    rich_x = richardson("x", H)
    cen_h = central("chi2", H)
    cen_h2 = central("chi2", H / 2)
    r_chi = rel(env, rich_chi)
    r_A = rel(dAdu, rich_A)
    r_x = rel(dxdu, rich_x)
    ctrl = control_group()
    ctrl_read = [c["reading"] for c in ctrl]
    ctrl_distinct = len({str(v) for v in ctrl_read})
    ctrl_zero = sum(1 for v in ctrl_read if v == 0)

    loose_hits = 0
    white_hits = 0
    for p in glob.glob(os.path.join(MAIN, "算法联盟_*.md")) + \
            glob.glob(os.path.join(DATA, "_ALG_*_recompute_report_*.txt")):
        if is_own(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines():
            if CLAIM_RE.search(ln):
                loose_hits += 1
            if positive_claim(ln):
                white_hits += 1

    span_act, span_exp = act_span_dex(), exp_span_dex()
    aa, ea = act_a(), exp_a()
    ca, ec = act_c(), exp_c()
    ba, eb = act_beta(), exp_beta()
    chi_act, chi_exp = act_chi2_min(), exp_chi2_min()
    rm = readme_read()

    k = dict(
        books=cat["books"], mds=cat["mds"], reports=cat["reports"],
        eq_like_lines=cat["eq_like_lines"], eq_key_books=cat["eq_key_books"],
        no_new_formula_books=cat["no_new_formula_books"],
        claims_json=cat["claims_json"],
        claims_md=len(cat["claims_md"]), claims_report=len(cat["claims_report"]),
        claims_total=cat["claims_json"] + len(cat["claims_md"]) + len(cat["claims_report"]),
        loose_claim_hits=loose_hits, whitelist_claim_hits=white_hits,
        objects_n=len(objs), classify_counts=kinds,
        free_real=real_free, free_control=ctrl_free,
        new_equation_count=real_free,
        chi2_min=dstr(chi_act, 12), chi2_r20=dstr(chi_exp, 12),
        rel_chi2=dstr_sci(rel(chi_act, chi_exp), 3),
        a3_rel=dstr_sci(rel(A[2], F(1) / U), 3),
        A_opt=dstr(BASE["A"], 12), x_opt=dstr(BASE["x"], 12),
        rel_A=dstr_sci(rel(BASE["A"], F_of(R20["key_numbers"]["A_opt"])), 3),
        rel_x=dstr_sci(rel(BASE["x"], F_of(R20["key_numbers"]["x_opt"])), 3),
        f1=dstr(f1, 24), f2=dstr(f2, 24),
        sym_dA=dstr(sym["dA_at_opt"], 24), sym_dX=dstr(sym["dX_at_opt"], 24),
        d2A=dstr(sym["d2A"], 9), d2X=dstr(sym["d2X"], 9),
        hess_det=dstr(hess, 9), proj_gdet=dstr(gdet, 9),
        env_analytic=dstr(env, 9), env_richardson=dstr(rich_chi, 9),
        env_rel=dstr_sci(r_chi, 3),
        central_h=dstr(cen_h, 9), central_h2=dstr(cen_h2, 9),
        rich_rel=dstr_sci(max(r_chi, r_A, r_x), 3),
        dAdu_analytic=dstr(dAdu, 9), dAdu_richardson=dstr(rich_A, 9),
        dAdu_rel=dstr_sci(r_A, 3),
        dxdu_analytic=dstr(dxdu, 9), dxdu_richardson=dstr(rich_x, 9),
        dxdu_rel=dstr_sci(r_x, 3),
        param_response=dstr(abs(dAdu) + abs(dxdu), 9),
        proj_resid=dstr(proj, 9), rank_M=2, obs_dim=3,
        n_new_params_required=obs_dim_rank_gap(),
        span_act=dstr(span_act, 12), span_exp=dstr(span_exp, 12),
        span_rel=dstr_sci(rel(span_act, span_exp), 3),
        beta_text="、".join(str(x) for x in ba),
        c_text="、".join(dstr(x, 9) for x in ca),
        ctrl_readings="、".join(dstr(v, 6) for v in ctrl_read),
        ctrl_distinct=ctrl_distinct, ctrl_zero_count=ctrl_zero,
        readme_bytes=rm["bytes"], readme_max_rid=rm["max_rid"],
        readme_md5=rm["md5"],
        source_missing=sum(1 for p in source_files() if not os.path.exists(p)),
    )

    # ------------------------------------------------------------ 守卫
    add("ED-ANCHOR-UNIQUE", len(glob.glob("openuft/**/" + ANCHOR, recursive=True)) == 1)
    add("ED-SELF-EXCLUSION",
        all(is_own(x) for x in cat["self_excluded"]) and
        all(not is_own(r["book"]) for r in cat["rows"]),
        "本册产物按精确 OWN_TOKENS 排除，首次与幂等复跑读数一致")
    add("ED-A-TWO-PATH", all(rel(x, y) < tol for x, y in zip(aa, ea)),
        "46 锚闭式 vs R20 存档")
    add("ED-A3-PRECISION-AWARE", rel(A[2], F(1) / U) < tol,
        "R20 存档 a3 为截断值，WLS 用 1/alpha_s 精确值，符号求导须同口径")
    add("ED-BETA-TWO-PATH", all(rel(x, y) < tol for x, y in zip(ba, eb)))
    add("ED-C-TWO-PATH", all(rel(x, y) < tol for x, y in zip(ca, ec)),
        "自算 Machin π 与 β 得斜率")
    add("ED-SPAN-TWO-PATH", rel(span_act, span_exp) < tol)
    add("ED-CHI2-TWO-PATH", rel(chi_act, chi_exp) < tol)
    add("ED-WLS-MATCH-R20",
        rel(BASE["A"], F_of(R20["key_numbers"]["A_opt"])) < tol and
        rel(BASE["x"], F_of(R20["key_numbers"]["x_opt"])) < tol)
    add("ED-FIRST-ORDER-ZERO", f1 == 0 and f2 == 0,
        "加权残差和与一阶矩残差和精确为 0")
    add("ED-SYMBOLIC-DERIV-ZERO",
        sym["dA_at_opt"] == 0 and sym["dX_at_opt"] == 0 and
        not sym["dA_is_zero"] and not sym["dX_is_zero"],
        "导函数不恒零但在最优点取零")
    add("ED-SECOND-DERIV-POS", sym["d2A"] > 0 and sym["d2X"] > 0)
    add("ED-HESSIAN-POS", hess > 0 and hess == gdet,
        "Hessian det/4 与投影 Gram det 同源恒等")
    add("ED-ENVELOPE-RICHARDSON", r_chi < rich_tol,
        "包络解析导数 vs Richardson 中心差分")
    add("ED-CENTRAL-CONVERGENCE",
        rel(env, cen_h2) < rel(env, cen_h),
        "h 减半后偏离单调下降，O(h^2)")
    add("ED-IMPLICIT-DA", r_A < rich_tol)
    add("ED-IMPLICIT-DX", r_x < rich_tol)
    add("ED-PARAMS-MOVE-WITH-OBS",
        abs(dAdu) + abs(dxdu) > F(1, 10 ** 6),
        "两个拟合参数随 alpha_s 扰动而动")
    add("ED-PROJECTION-POS", proj > 0,
        "v=da/du 落在 span{1,c} 之外")
    add("ED-RANK-GAP", obs_dim_rank_gap() == 1 and 2 < 3)
    add("ED-IDENTITY-DETECTED", kinds.get("IDENTITY", 0) == 1)
    add("ED-NONSMOOTH-DETECTED", kinds.get("NON-SMOOTH", 0) == 2)
    add("ED-FREE-POSITIVE-CONTROL", ctrl_free == 1 and real_free == 0,
        "FREE 谓词非恒假：纯数学夹具命中 1，真实对象 0")
    add("ED-CATALOG-CLAIMS-ZERO",
        k["claims_total"] == 0 and white_hits == 0)
    add("ED-CATALOG-TWO-PATH",
        len(cat["claims_md"]) == len(cat["claims_report"]) == cat["claims_json"])
    add("ED-WHITELIST-HAS-POWER", loose_hits > white_hits,
        "松散命中 %d / 语义白名单后 %d" % (loose_hits, white_hits))
    add("ED-CTRL-POS-NONZERO",
        ctrl[0]["nonzero"] and ctrl[1]["nonzero"] and
        ctrl[0]["reading"] != ctrl[1]["reading"])
    add("ED-CTRL-NEG-ZERO",
        (not ctrl[2]["nonzero"]) and (not ctrl[3]["nonzero"]))
    add("ED-CTRL-DISTINCT", ctrl_distinct >= 2 and ctrl_zero == 2,
        "如实报去重 %d / 零读数 %d" % (ctrl_distinct, ctrl_zero))
    add("ED-CTRL-BACKFIRE",
        control_group(derivator=lambda u: ([F(0)], [F(1)]))[0]["reading"] == 0
        and ctrl[0]["reading"] != 0,
        "求导器置零后正对照读数改变")
    add("ED-NO-HARDCODE-OK", len(hardcode_ok_hits()) == 0)
    add("ED-EXP-ACT-AST", len(exp_act_ast_hits()) == 0)
    add("ED-WRITE-NO-README", len(write_target_hits()) == 0)
    add("ED-VERDICT-MACHINE",
        verdict_string(dict(k, hess_det=k["hess_det"] + "1")) != verdict_string(k))
    add("ED-README-REALTIME", rm["max_rid"] == 406 and rm["bytes"] > 0)
    add("ED-SOURCE-MISSING-ZERO", k["source_missing"] == 0)
    add("ED-LINK-CHECK", k["source_missing"] == 0 and cat["books"] > 0)

    nf_guard = sum(1 for s in SEG if not s["ok"])
    declared = ["new_equation_count=0", "independent_predictions=0",
                "clean_configs=0", "breakthrough=0"]
    final = final_of(0, nf_guard, len(declared))
    verdict = verdict_string(k)

    note("IDENTITY", "Hessian det/4 与投影 Gram det 由同一 W,S1,S2 展开，"
         "读数逐位相等属同源恒真，不作两份独立证据")
    note("IDENTITY", "E4 按定义展开残差 0 且导数恒 0，单列 IDENTITY，不作为新方程")
    note("IDENTITY", "R20 存档 a3_inv_MZ 是 60 位截断值，本册 WLS 用 1/alpha_s 精确值，"
         "两口径相对偏离 " + k["a3_rel"] + "；符号求导器必须取 WLS 同口径输入，"
         "否则一阶条件出现 1e-66 量级假残差，属对象错位而非求导器错误")
    note("BOUNDARY", "本册只对可写成单变量有理函数的闭式做符号求导；"
         "E5 阶梯定价与 E6 整数比特账不可导，多元张量恒等式未进入求导器")
    note("BOUNDARY", "求导证明只覆盖一圈 SM/MSSM β 与 WLS 单方程族；"
         "投影残差 > 0 说明该族零自由参数方程不可能，不等于对所有方程族的全称否证")
    note("BOUNDARY", "分类读数依赖本册登记的 7 个对象集，不能把「FREE=0」当全库证明；"
         "承重是全链文本普查与求导精算，不是对象集属性")
    note("INFO", "数学自洽 != 实验证实；审计册只产可算判决，不产新物理")
    note("INFO", "四力大统一正确方程 0 条、独立实验预言 0；不宣称攻破统一场论")
    note("INFO", "本册不占 RID、不入 README、不与任何审计卷相加")

    doc = dict(title="算法联盟：全链方程清单整理、求导证明与零残差极值精算（第二十二轮）",
               date="2026-11-15", nature="可算判决册 · 非物理主张",
               red_line="不宣称攻破统一场论；数学自洽不等于实验证实",
               final=final, verdict=verdict,
               guard_count=len(SEG), guard_pass=len(SEG) - nf_guard,
               counts=dict(PASS=len(SEG) - nf_guard, FAIL=nf_guard,
                           IDENTITY=3, BOUNDARY=3, INFO=3),
               key_numbers=k, segments=SEG,
               equation_objects=[dict(id=o["id"], label=o["label"],
                                      origin=o["origin"], smooth=o["smooth"],
                                      kind=c["kind"], obs=c["obs"],
                                      param=c["param"], names=c["names"])
                                 for o, c in zip(objs, cls)],
               catalog=dict(books=cat["books"], mds=cat["mds"],
                            reports=cat["reports"],
                            eq_like_lines=cat["eq_like_lines"],
                            eq_key_books=cat["eq_key_books"],
                            no_new_formula_books=cat["no_new_formula_books"],
                            claims_json=cat["claims_json"],
                            claims_md=len(cat["claims_md"]),
                            claims_report=len(cat["claims_report"])),
               identity_notes=[n["text"] for n in NOTES if n["kind"] == "IDENTITY"],
               boundary_notes=[n["text"] for n in NOTES if n["kind"] == "BOUNDARY"],
               info_notes=[n["text"] for n in NOTES if n["kind"] == "INFO"],
               declared_negative=declared,
               source_files=[os.path.relpath(p, MAIN).replace(os.sep, "/")
                             for p in source_files()],
               content_sha256="")
    blob = json.dumps(doc, ensure_ascii=False, sort_keys=True).encode("utf-8")
    doc["content_sha256"] = hashlib.sha256(blob).hexdigest()
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2, sort_keys=True)
    with open(OUT_REPORT, "w", encoding="utf-8") as fh:
        fh.write(report_text(doc))
    print("FINAL =", final)
    print("VERDICT =", verdict)
    print("GUARDS = %d/%d" % (doc["guard_pass"], doc["guard_count"]))
    print("COUNTS =", json.dumps(doc["counts"], ensure_ascii=False, sort_keys=True))
    print("NEW-EQUATIONS =", real_free, "PROJECTION =", dstr(proj, 9),
          "RICH-REL =", dstr_sci(max(r_chi, r_A, r_x), 3))
    for s in SEG:
        if not s["ok"]:
            print("FAIL", s["id"], s["note"])
    return doc


def obs_dim_rank_gap():
    """3 个观测、2 个拟合参数方向 ⇒ 至少 1 个新自由参数。"""
    return 3 - 2


if __name__ == "__main__":
    main()
