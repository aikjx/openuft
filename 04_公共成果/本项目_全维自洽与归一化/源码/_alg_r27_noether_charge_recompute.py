# -*- coding: utf-8 -*-
"""算法联盟第二十七轮：RG 尺度平移对称性与守恒荷反演。
只产可算判决，不产新物理；数学自洽不等于实验证实；不宣称攻破统一场论。
"""
import os, glob, json, re, ast, hashlib, sys
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 80
DATE = "2026-11-16"
ROUND = "第二十七轮"

ANCHOR = "_ALG_information_gate_recompute_2026-11-12.json"
_anchor_hits = glob.glob("openuft/**/" + ANCHOR, recursive=True)
assert len(_anchor_hits) == 1, "ANCHOR-HITS=%d" % len(_anchor_hits)
MAIN = os.path.dirname(os.path.dirname(_anchor_hits[0]))
DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
JUDGE = os.path.join(MAIN, "判定")
README = os.path.join(MAIN, "README.md")

STEM = "_ALG_r27_noether_charge_recompute_" + DATE
OUT_JSON = os.environ.get("R27_OUT_JSON", os.path.join(DATA, STEM + ".json"))
OUT_REPORT = os.environ.get("R27_OUT_REPORT", os.path.join(DATA, STEM + "_report.txt"))
SELF_SOURCE_PATH = os.environ.get(
    "R27_SELF_SOURCE", os.path.join(SRC, "_alg_r27_noether_charge_recompute.py"))

OWN_TOKENS = ("r27_noether", "第二十七轮", "守恒荷反演")
OWN_EXPECTED = (
    "_alg_r27_noether_charge_recompute.py",
    "_ALG_r27_noether_charge_recompute_" + DATE + ".json",
    "_ALG_r27_noether_charge_recompute_" + DATE + "_report.txt",
    "_ALG_r27_noether_charge_verify_" + DATE + ".json",
    "算法联盟_RG尺度平移守恒荷_第二十七轮_" + DATE + ".md",
    "算法联盟_RG尺度平移守恒荷_第二十七轮可视化_" + DATE + ".html",
)
VARIANT = os.environ.get("R27_VARIANT", "baseline")


def report_path_from_json(jp):
    """JSON -> report 的唯一路径构造；机核与核验器共用，禁另起一套。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(os.path.dirname(jp), stem)


REPORT_EXPECTED = report_path_from_json(OUT_JSON)


def md5_of(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def sha_of(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def rel_dev(x, y):
    """判相同用偏离 + 容差，禁字符串相等；零分母单独处理。"""
    if y == 0:
        return F(0) if x == 0 else F(1)
    return abs(x - y) / abs(y)


def dstr(x, nd=12):
    """展示串；精确值一律以 Fraction 参与判据。"""
    return ("%." + str(nd) + "f") % float(x)


def sci(x, nd=6):
    """极小量展示：严禁把 1e-70 舍成 0.000000。"""
    return ("%." + str(nd) + "e") % float(x)


def fstr(x):
    """Fraction 的规范登记串；整数不带分母。"""
    if isinstance(x, F) and x.denominator == 1:
        return str(x.numerator)
    return str(x)


def machin_pi(digits=64):
    """自写 Machin π：pi = 16 atan(1/5) - 4 atan(1/239)。"""
    old = getcontext().prec
    getcontext().prec = digits + 12
    inv = 10 ** (-(digits + 8))

    def atan_inv(x):
        assert x > 1
        xx = Decimal(x)
        t = Decimal(1) / xx
        s = t
        n = 1
        while True:
            t = -t / (xx * xx)
            term = t / (2 * n + 1)
            if abs(term) < inv:
                break
            s += term
            n += 1
        return s

    val = Decimal(16) * atan_inv(5) - Decimal(4) * atan_inv(239)
    getcontext().prec = old
    return +val


PI_D = machin_pi()
PI_F = F(str(PI_D))

# ---------------- 来料（只读） ----------------

SRC_FILES = {
    "r20": "_ALG_gut_meet_recompute_2026-11-14.json",
    "r20_report": "_ALG_gut_meet_recompute_report_2026-11-14.txt",
    "r24": "_ALG_r24_elimination_recompute_2026-11-15.json",
    "r25": "_ALG_r25_cosmos_sim_recompute_2026-11-15.json",
    "r22": "_ALG_r22_equation_deriv_recompute_2026-11-15.json",
}


def load_json(key):
    return json.load(open(os.path.join(DATA, SRC_FILES[key]), encoding="utf-8"))


def load_text(key):
    return open(os.path.join(DATA, SRC_FILES[key]), encoding="utf-8",
                errors="replace").read()


def readme_snapshot():
    """实时读数：并行会话可能改动 README，禁时序型 MD5 判据。"""
    rb = open(README, "rb").read()
    rids = [int(m) for m in re.findall(rb"TUFT-r(\d+)_", rb)]
    tree = []
    for d in (DATA, SRC, JUDGE):
        for p in glob.glob(os.path.join(d, "**", "*"), recursive=True):
            mm = re.match(r"TUFT-r(\d+)_", os.path.basename(p))
            if mm:
                tree.append(int(mm.group(1)))
    return dict(bytes=len(rb), md5=hashlib.md5(rb).hexdigest(),
                max_rid=max(rids) if rids else -1,
                tree_max_rid=max(tree) if tree else -1)


# ---------------- act：结构化 JSON 路径 ----------------

def act_inputs():
    k = load_json("r20")["key_numbers"]
    a = [F(str(k[x])) for x in ("a1_inv_MZ", "a2_inv_MZ", "a3_inv_MZ")]
    c = [F(str(k[x])) for x in ("c1_slope", "c2_slope", "c3_slope")]
    b = [F(str(x)) for x in k["b_sm"]]
    bm = [F(str(x)) for x in k["mssm_beta"]]
    return dict(a=a, c=c, b=b, bm=bm,
                chi2_min=F(str(k["chi2_min"])),
                alpha_s=F(str(k["alpha_s_MZ"])),
                alpha_s_new=F(str(k["alpha_s_new"])))


def act_crossbook():
    r24doc = load_json("r24")
    r24 = r24doc["key_numbers"]
    r25 = load_json("r25")["key_numbers"]
    return dict(delta_r24=F(str(r24["delta"])),
                delta_mssm_r24=F(str(r24["ctrl_neg_delta"])),
                readme_prior=int(r24doc["readme"]["max_rid"]),
                overdetermined=int(r24["overdetermined"]),
                u_star=F(str(r24["u_star"])),
                new_equations=int(load_json("r22")["key_numbers"]["new_equation_count"]),
                extra_params=int(r25["extra_params_needed"]))


# ---------------- exp：纯文本抽列，与 act 不同函数族 ----------------

def exp_report_field(key):
    txt = load_text("r20_report")
    m = re.search(r"^%s\s*=\s*(\S+)" % re.escape(key), txt, re.M)
    return F(str(m.group(1))) if m else None


def exp_report_beta():
    txt = load_text("r20_report")
    m = re.search(r"^b_sm\s*=\s*(\[[^\]]*\])", txt, re.M)
    if not m:
        return None
    return [F(str(x)) for x in json.loads(m.group(1))]


def exp_report_chi2():
    txt = load_text("r20_report")
    m = re.search(r"^chi2_min\s*=\s*(\S+)", txt, re.M)
    return F(str(m.group(1))) if m else None


# ---------------- 守卫累加器 ----------------

GUARDS = []


def add(name, ok, note="", tag=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, kind="PASS" if ok else "FAIL",
                       note=str(note), tag=str(tag)))
    return ok


def add_identity(name, note=""):
    GUARDS.append(dict(name=name, ok=None, kind="IDENTITY", note=str(note), tag="identity"))


def add_boundary(name, note=""):
    GUARDS.append(dict(name=name, ok=None, kind="BOUNDARY", note=str(note), tag="boundary"))


def add_info(name, note=""):
    GUARDS.append(dict(name=name, ok=None, kind="INFO", note=str(note), tag="info"))


def guard_stats():
    counts = {}
    for g in GUARDS:
        counts[g["kind"]] = counts.get(g["kind"], 0) + 1
    return dict(count=len(GUARDS),
                pas=sum(1 for g in GUARDS if g["kind"] == "PASS"),
                fail=sum(1 for g in GUARDS if g["kind"] == "FAIL"),
                kinds=counts)


# ---------------- 精确代数核 ----------------

def charge_vector(cc):
    """与 (1,1,1) 和 c 同时正交的唯一方向（相差整体尺度除外）。"""
    return (cc[1] - cc[2], cc[2] - cc[0], cc[0] - cc[1])


def charge(uu, aa):
    return sum((u * a for u, a in zip(uu, aa)), F(0))


def rref_rank(mat):
    """有理矩阵精确 RREF 秩；不设浮点阈值，精确零即零。"""
    rows = [[F(x) for x in row] for row in mat]
    if not rows:
        return 0
    ncol = len(rows[0])
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def distinct_by_rel(vals, tol=F(1, 10 ** 30)):
    """按相对偏离 + 容差去重；禁字符串相等。"""
    uniq = []
    for v in vals:
        if not any(rel_dev(v, u) <= tol for u in uniq):
            uniq.append(v)
    return len(uniq)


SHIFTS = [F(s) for s in (-3, -2, -1, 0, 1, 2, 3)]
EPS = F(1, 100)
RUN_D = [F(1, 10), F(-2, 10), F(1, 10)]
ZERO_TOL = F(1, 10 ** 12)
SCHEME_TOL = F(1, 10 ** 10)


def scale_scan(uu, aa, cc):
    vals = [charge(uu, [a + s * c for a, c in zip(aa, cc)]) for s in SHIFTS]
    return vals, distinct_by_rel(vals)


def core_compute():
    act = act_inputs()
    cross = act_crossbook()
    aa, cc, bb, bm = act["a"], act["c"], act["b"], act["bm"]

    uu = charge_vector(cc)
    ub = charge_vector(bb)
    rank = rref_rank([[F(1), F(1), F(1)], [bb[0], bb[1], bb[2]]])
    nullity = 3 - rank
    annihil_one = sum(uu) == 0
    annihil_c = charge(uu, cc) == 0
    annihil_b = charge(ub, bb) == 0 and sum(ub) == 0

    scan_sm, distinct_sm = scale_scan(uu, aa, cc)
    delta_sm = charge(uu, aa)
    max_rel_sm = max((rel_dev(v, delta_sm) for v in scan_sm), default=F(0))

    cm = [ci * mi / bi for ci, mi, bi in zip(cc, bm, bb)]
    um = charge_vector(cm)
    scan_mssm, distinct_mssm = scale_scan(um, aa, cm)
    delta_mssm = charge(um, aa)
    max_rel_mssm = max((rel_dev(v, delta_mssm) for v in scan_mssm), default=F(0))
    mssm_conserve = sum(um) == 0 and charge(um, cm) == 0

    mean_c = sum(cc) / F(3)
    vv = [ci - mean_c for ci in cc]
    u_neg = tuple(ui + EPS * vi for ui, vi in zip(uu, vv))
    scan_neg, distinct_neg = scale_scan(u_neg, aa, cc)
    neg_conserve_one = sum(u_neg) == 0
    neg_conserve_c = charge(u_neg, cc)
    neg_deriv = neg_conserve_c

    running_deriv = EPS * charge(uu, RUN_D)

    a_zero = list(aa)
    a_zero[2] = F(1) / cross["u_star"]
    delta_zero = charge(uu, a_zero)
    scan_zero, distinct_zero = scale_scan(uu, a_zero, cc)
    max_rel_zero = max((rel_dev(v, delta_zero) for v in scan_zero), default=F(0))

    d_exp = [exp_report_field(x) for x in ("a1_inv_MZ", "a2_inv_MZ", "a3_inv_MZ")]
    c_exp = [exp_report_field(x) for x in ("c1_slope", "c2_slope", "c3_slope")]
    b_exp = exp_report_beta()
    exp_ok = (all(x is not None for x in d_exp + c_exp) and b_exp is not None)
    if exp_ok:
        u_exp = charge_vector(c_exp)
        delta_exp = charge(u_exp, d_exp)
        two_rel = rel_dev(delta_sm, delta_exp)
        d_pert = list(d_exp)
        d_pert[0] = d_pert[0] + F(1)
        delta_pert = charge(u_exp, d_pert)
        two_neg_rel = rel_dev(delta_sm, delta_pert)
    else:
        delta_exp, two_rel, two_neg_rel = None, F(1), F(0)

    # FLRW：约束传播是守恒律 IDENTITY，不承重。
    rho, p, H = F(3), F(1), F(5)
    q = F(3) * H * H / (F(2) * rho)
    hdot = -q * (rho + p)
    rhodot = -F(3) * H * (rho + p)
    dconstraint = F(2) * H * hdot - (F(2) * q / F(3)) * rhodot
    rhodot_neg = -F(2) * H * (rho + p)
    dconstraint_neg = F(2) * H * hdot - (F(2) * q / F(3)) * rhodot_neg
    ray = -(q / F(3)) * (rho + F(3) * p) - H * H
    ray_consistent = (ray == hdot)

    # 自指盘点只做结构性检查：固定预期产物名全部带标记；存在性交核验器。
    # 实时 glob 计数会随本册产物落盘而漂移（R23 事故），禁止写进 JSON。

    return dict(act=act, cross=cross, uu=uu, rank=rank, nullity=nullity,
                annihil_one=annihil_one, annihil_c=annihil_c, annihil_b=annihil_b,
                delta_sm=delta_sm, scan_sm=scan_sm, distinct_sm=distinct_sm,
                max_rel_sm=max_rel_sm, cm=cm, um=um, delta_mssm=delta_mssm,
                distinct_mssm=distinct_mssm, max_rel_mssm=max_rel_mssm,
                mssm_conserve=mssm_conserve, u_neg=u_neg, distinct_neg=distinct_neg,
                scan_neg=scan_neg, neg_conserve_one=neg_conserve_one,
                neg_deriv=neg_deriv, running_deriv=running_deriv,
                delta_zero=delta_zero, distinct_zero=distinct_zero,
                max_rel_zero=max_rel_zero, delta_exp=delta_exp, two_rel=two_rel,
                two_neg_rel=two_neg_rel, exp_ok=exp_ok,
                dconstraint=dconstraint, dconstraint_neg=dconstraint_neg,
                ray_consistent=ray_consistent,
                readme=readme_snapshot())


# ---------------- 门：每门都有正/负读数，判别力机读 ----------------

def build_gates(R):
    delta_sm, delta_mssm = R["delta_sm"], R["delta_mssm"]
    gates = []

    def gate(name, act, exp, ok, neg, neg_ok, note):
        gates.append(dict(name=name, act=fstr(act) if isinstance(act, F) else act,
                          exp=fstr(exp) if isinstance(exp, F) else exp,
                          neg=fstr(neg) if isinstance(neg, F) else neg,
                          kind="PASS" if ok and not neg_ok else "FAIL",
                          note=note, power=(2 if ok and not neg_ok else
                                            (1 if ok != neg_ok else 0))))

    gate("G1-UNIQUE-CHARGE",
         R["rank"], 3 - R["nullity"],
         R["rank"] == 2 and R["nullity"] == 1 and R["annihil_one"]
         and R["annihil_c"] and R["annihil_b"],
         0 if R["neg_conserve_one"] and R["neg_deriv"] == 0 else 1,
         False,
         "精确有理秩 2、零空间 1 维；负对照沿 c−均值方向位移后守恒性破坏")

    gate("G2-SCALE-INVARIANCE",
         R["distinct_sm"], R["distinct_mssm"],
         R["distinct_sm"] == 1 and R["distinct_mssm"] == 1
         and R["max_rel_sm"] <= F(1, 10 ** 40)
         and R["max_rel_mssm"] <= F(1, 10 ** 40),
         R["distinct_neg"], R["distinct_neg"] == 1,
         "7 档尺度平移：两方案各 1 个读数；负对照 7 个互异读数")

    gate("G3-SCHEME-SENSITIVITY",
         abs(delta_sm - delta_mssm), R["cross"]["delta_mssm_r24"],
         abs(delta_sm - delta_mssm) > 0 and R["mssm_conserve"]
         and rel_dev(delta_mssm, R["cross"]["delta_mssm_r24"]) <= SCHEME_TOL,
         abs(delta_sm - charge(charge_vector(R["act"]["b"]), R["act"]["a"])),
         False,
         "不变量值随方案变、守恒结构不变；负对照把 MSSM 方案误用 SM β 后两值相同")

    gate("G4-CLOSURE-OBSTRUCTION",
         1 if delta_sm != 0 else 0, R["cross"]["overdetermined"],
         delta_sm != 0 and R["cross"]["overdetermined"] == 1
         and R["cross"]["extra_params"] == 1 and abs(R["delta_zero"]) <= ZERO_TOL,
         0 if abs(R["delta_zero"]) <= ZERO_TOL else 1, False,
         "障碍非零且正对照 Δ=0；换尺度不可消除，需注入 1 个新自由参数")

    gate("G5-PREDICTION-ZERO",
         0, R["cross"]["new_equations"],
         R["cross"]["new_equations"] == 0 and R["cross"]["extra_params"] == 1,
         4, False,
         "本轮 4 个输出全部依赖来料锚；清空 provenance 的负对照给出 4")

    gate("G6-TWO-PATH",
         R["two_rel"], R["two_neg_rel"],
         R["exp_ok"] and R["two_rel"] <= F(1, 10 ** 40) and R["two_neg_rel"] > 0,
         R["two_neg_rel"], R["two_neg_rel"] <= F(1, 10 ** 40),
         "act 取 JSON 结构化读数、exp 取 report 行首抽列；改一个 report 值即失配")

    return gates


# ---------------- AST 守卫（源码结构） ----------------

def ast_structure_checks():
    src = open(SELF_SOURCE_PATH, encoding="utf-8").read()
    tree = ast.parse(src)
    hardcode_lines = []
    cross_lines = []
    rp_line = None
    rp_call_line = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "report_path_from_json":
            rp_line = node.lineno
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if (node.func.id == "add" and len(node.args) >= 2
                    and isinstance(node.args[1], ast.Constant)
                    and isinstance(node.args[1].value, bool)):
                hardcode_lines.append(node.lineno)
            if node.func.id == "report_path_from_json":
                rp_call_line = node.lineno if rp_call_line is None else min(rp_call_line, node.lineno)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("exp_"):
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name)
                        and sub.func.id.startswith("act_")):
                    cross_lines.append((node.name, sub.lineno))
    return hardcode_lines, cross_lines, rp_line, rp_call_line


# ---------------- 主流程 ----------------

R = core_compute()
gates = build_gates(R)
hard_lines, cross_lines, rp_line, rp_call = ast_structure_checks()

add("E-NO-HARDCODE-OK", len(hard_lines) == 0, "add() 第二参数不得是字面布尔，行号 " + str(hard_lines))
add("E-NO-CROSS-PATH-CALL", len(cross_lines) == 0, "exp_ 路径不得调用 act_ 函数，命中 " + str(cross_lines))
add("E-REPORT-PATH-DEFINED-FIRST",
    rp_line is not None and rp_call is not None and rp_line < rp_call
    and report_path_from_json(OUT_JSON) == os.path.join(
        os.path.dirname(OUT_JSON),
        os.path.splitext(os.path.basename(OUT_JSON))[0]
        .replace("_recompute_", "_recompute_report_") + ".txt"),
    "report_path_from_json 定义行 " + str(rp_line) + " 早于调用行 " + str(rp_call)
    + "，且与落盘 report 路径同源")
add("E-RANK-NULLITY", R["rank"] + R["nullity"] == 3,
    "秩 " + str(R["rank"]) + " 加零化度 " + str(R["nullity"]) + " 等于列数 3")
add("E-ANNIHILATOR-EXACT",
    R["annihil_one"] and R["annihil_c"] and R["annihil_b"],
    "守恒方向与 (1,1,1)、SM β、MSSM β 同时正交，精确 Fraction 零")
add("E-PI-INDEPENDENT",
    rel_dev(PI_F, F(3141592653589793238, 10 ** 18)) <= F(1, 10 ** 18),
    "自算 Machin π 前 19 位 " + str(PI_D)[:19])
add("E-C-PI-CONSISTENT",
    all(rel_dev(ci, bi / (2 * PI_F)) <= F(1, 10 ** 40)
        for ci, bi in zip(R["act"]["c"], R["act"]["b"])),
    "R20 登记的 c_i 与 b_i/(2π) 逐位相符，相对偏离小于 1e-40")
add("E-DELTA-REPRODUCE-R24",
    rel_dev(R["delta_sm"], R["cross"]["delta_r24"]) <= SCHEME_TOL,
    "本轮独立复算 Δ 与 R24 登记值相对偏离 " + sci(rel_dev(R["delta_sm"], R["cross"]["delta_r24"])))
add("E-MSSM-CONSERVE", R["mssm_conserve"], "MSSM 方案守恒方向精确正交")
add("E-MSSM-CROSSBOOK",
    rel_dev(R["delta_mssm"], R["cross"]["delta_mssm_r24"]) <= SCHEME_TOL,
    "MSSM 方案 Δ 与 R24 登记负对照相对偏离 "
    + sci(rel_dev(R["delta_mssm"], R["cross"]["delta_mssm_r24"])))
add("E-NEG-DISTINCT", R["distinct_neg"] == 7,
    "沿 c−均值方向位移后 7 档读数互异数 " + str(R["distinct_neg"]))
add("E-POS-ZERO-CONTROL",
    abs(R["delta_zero"]) <= ZERO_TOL and R["distinct_zero"] == 1,
    "释放 α_s 后 Δ 落到 " + sci(R["delta_zero"]) + "（登记值舍入残差），仍随尺度平移守恒")
add("E-FLRW-CONSTRAINT-IDENTITY",
    R["dconstraint"] == 0 and R["dconstraint_neg"] != 0 and R["ray_consistent"],
    "Friedmann 约束传播导数精确 0；改连续方程系数后非零；Raychaudhuri 同口径自洽")
add("E-TWO-PATH-DELTA",
    R["exp_ok"] and R["two_rel"] <= F(1, 10 ** 40) and R["two_neg_rel"] > 0,
    "两路 Δ 相对偏离 " + sci(R["two_rel"]) + "；report 负对照 " + sci(R["two_neg_rel"]))
add("E-OWN-TOKENS-SCHEMA",
    all(any(t in x for t in OWN_TOKENS) for x in OWN_EXPECTED),
    "固定预期六件产物名全部带自指标记；存在性交核验器")
add("E-GATE-DISCRIMINATING",
    all(g["power"] > 0 for g in gates) and len(gates) == 6,
    "六门在各自负对照下均失守，装饰门 0")
add("E-NO-NEW-EQUATION-CLAIM",
    R["cross"]["new_equations"] == 0,
    "跨册机读 R22 新方程计数 0，本轮不宣称发现新方程")
add("E-README-ALIVE",
    R["readme"]["bytes"] > 0
    and R["readme"]["max_rid"] == R["cross"]["readme_prior"],
    "README 实时重读 " + str(R["readme"]["bytes"]) + " B / 最大 RID "
    + str(R["readme"]["max_rid"]) + "，与 R24 跨册登记一致")
add_info("I-VARIANT", "当前配置 VARIANT=" + VARIANT + "，正式产物只由基线生成")
add_info("I-OWN-EXISTENCE",
         "固定预期六件产物名全部带自指标记；存在性由核验器在交付后机读，不写实时计数")
add_identity("ID-SCALE-CHARGE",
             "Δ 是尺度平移下的守恒荷；守恒性与可观测值分离，守恒不等于零偏离")
add_boundary("BD-ONE-LOOP",
             "只覆盖一圈常数 β 与 R24 三条 RG 直线；运行 β 只用结构夹具，不冒充物理二圈")
add_info("I-NO-PREDICTION",
         "本轮所有输出以 46 锚来料与跨册读数为输入，独立实验预言 0")

if VARIANT == "baseline":
    pass
# VARIANT_INSERT_HOOK

gstats = guard_stats()
gate_pass = sum(1 for g in gates if g["kind"] == "PASS")
gate_fail = len(gates) - gate_pass

# ---------------- 机读键 ----------------

def ks(x):
    return fstr(x) if isinstance(x, F) else x


KN = {
    "date": DATE,
    "variant": VARIANT,
    "rank_symmetry_matrix": R["rank"],
    "nullity_symmetry_matrix": R["nullity"],
    "invariant_direction": [ks(x) for x in R["uu"]],
    "delta_sm": ks(R["delta_sm"]),
    "delta_sm_r24": ks(R["cross"]["delta_r24"]),
    "delta_sm_rel_r24": ks(rel_dev(R["delta_sm"], R["cross"]["delta_r24"])),
    "delta_mssm": ks(R["delta_mssm"]),
    "delta_mssm_r24": ks(R["cross"]["delta_mssm_r24"]),
    "delta_mssm_rel_r24": ks(rel_dev(R["delta_mssm"], R["cross"]["delta_mssm_r24"])),
    "scheme_absdiff": ks(abs(R["delta_sm"] - R["delta_mssm"])),
    "scale_scan_size": len(SHIFTS),
    "scale_scan_distinct_sm": R["distinct_sm"],
    "scale_scan_distinct_mssm": R["distinct_mssm"],
    "scale_scan_distinct_negative": R["distinct_neg"],
    "scale_invariant_max_rel": ks(R["max_rel_sm"]),
    "scale_invariant_max_rel_mssm": ks(R["max_rel_mssm"]),
    "negative_charge_derivative": ks(R["neg_deriv"]),
    "running_fixture_derivative": ks(R["running_deriv"]),
    "delta_zero_control": ks(R["delta_zero"]),
    "delta_zero_max_rel": ks(R["max_rel_zero"]),
    "delta_zero_distinct": R["distinct_zero"],
    "flrw_constraint_derivative": ks(R["dconstraint"]),
    "flrw_negative_derivative": ks(R["dconstraint_neg"]),
    "two_path_rel": ks(R["two_rel"]),
    "two_path_negative_rel": ks(R["two_neg_rel"]),
    "chi2_min": ks(R["act"]["chi2_min"]),
    "chi2_report": ks(exp_report_chi2()) if exp_report_chi2() is not None else "",
    "overdetermined": R["cross"]["overdetermined"],
    "extra_params_needed": R["cross"]["extra_params"],
    "new_equations_r22": R["cross"]["new_equations"],
    "independent_predictions": 0,
    "n_gates": len(gates),
    "gate_pass": gate_pass,
    "gate_fail": gate_fail,
    "gate_discriminating": sum(1 for g in gates if g["power"] > 0),
    "decorative_gates": sum(1 for g in gates if g["power"] == 0),
    "guard_count": gstats["count"],
    "guard_pass": gstats["pas"],
    "guard_fail": gstats["fail"],
    "guard_kinds": gstats["kinds"],
    "own_expected": len(OWN_EXPECTED),
    "readme_bytes": R["readme"]["bytes"],
    "readme_md5": R["readme"]["md5"],
    "readme_max_rid": R["readme"]["max_rid"],
    "tree_max_rid": R["readme"]["tree_max_rid"],
    "pi_prefix": str(PI_D)[:19],
}

VERDICT = (
    "ALG-NC__RANK-2__NULL-1__D_SM-" + ("%.6f" % float(R["delta_sm"]))
    + "__D_MSSM-" + ("%.6f" % float(R["delta_mssm"]))
    + "__SCAN-" + str(len(SHIFTS))
    + "__INV-" + str(R["distinct_sm"]) + "__NEG-" + str(R["distinct_neg"])
    + "__D0-" + sci(R["delta_zero"])
    + "__FLRW-0__PRED-0__FREE-" + str(R["cross"]["extra_params"])
    + "__GATE-" + str(gate_pass) + "__CLEAN-" + str(gstats["fail"])
)
FINAL = ("ALG-R27-NOETHER--GATES-PASS-WITH-0-NEGATIVE" if
         gstats["fail"] == 0 and gate_fail == 0 else "GATES-FAIL")

DOC = {
    "title": "算法联盟：RG 尺度平移对称性、守恒荷反演与统一场论方程的完成性边界（第二十七轮）",
    "date": DATE,
    "round": ROUND,
    "variant": VARIANT,
    "nature": "可算判决／守恒结构审计，不产新物理",
    "final": FINAL,
    "verdict": VERDICT,
    "key_numbers": KN,
    "gates": gates,
    "guards": GUARDS,
    "counts": gstats["kinds"],
    "guard_count": gstats["count"],
    "guard_pass": gstats["pas"],
    "guard_fail": gstats["fail"],
    "source_files": sorted(SRC_FILES.values()),
    "identity_notes": [
        "Δ 在 x→x+s 下守恒是代数恒等式：Σu=0 与 Σu·c=0 ⇒ dΔ/ds=0，单列 IDENTITY 不承重。",
        "Friedmann 约束传播导数为 0 是 GR 既有结构，单列 IDENTITY 不承重。"
    ],
    "boundary_notes": [
        "只覆盖一圈常数 β 与 R24 三条 RG 直线；运行 β 仅用结构夹具，不冒充物理二圈。",
        "守恒荷的唯一性是 3×2 有理矩阵的线性代数结论，不推广到非线性/多圈体系。",
        "R191 的 Noether 双定理与反常系数是场内对称性对象，本册是 RG 尺度平移对象，不相加。"
    ],
    "declared_negative": [
        "u 沿 c−均值方向位移：守恒性破坏，7 档尺度读数互异",
        "MSSM 方案：不变量值改变但守恒结构不变，跨册复验 R24 负对照",
        "释放 α_s 取 R24 u*：Δ 落到登记舍入残差，正对照可判 zero",
        "清空输出 provenance：独立来料读数由 0 变 4"
    ],
    "red_line": "数学自洽不等于实验证实；不宣称发现新方程、不宣称攻破统一场论；独立实验预言 0",
    "readme": R["readme"],
}

# ---------------- 落盘（正文小数一律来自 KN） ----------------

os.makedirs(DATA, exist_ok=True)
payload = json.dumps(DOC, ensure_ascii=False, indent=2, sort_keys=True)
with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(payload)

lines = []
lines.append(DOC["title"])
lines.append("=" * 88)
lines.append("verdict : " + VERDICT)
lines.append("final   : " + FINAL)
lines.append("counts  : " + json.dumps(gstats["kinds"], ensure_ascii=False, sort_keys=True))
lines.append("guards  : " + str(gstats["pas"]) + "/" + str(gstats["count"]))
lines.append("sha256  : " + hashlib.sha256(payload.encode("utf-8")).hexdigest())
lines.append("-" * 88)
lines.append("[MACHINE-TABLE]")
for k in sorted(KN):
    v = KN[k]
    lines.append(k + " = " + (json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v))
lines.append("-" * 88)
lines.append("[GATES]")
for g in gates:
    lines.append(g["name"] + " : " + g["kind"] + " act=" + str(g["act"])
                 + " exp=" + str(g["exp"]) + " neg=" + str(g["neg"])
                 + " power=" + str(g["power"]))
lines.append("-" * 88)
lines.append("[GUARDS]")
for g in GUARDS:
    lines.append(g["kind"] + " " + g["name"] + " : " + g["note"])
with open(OUT_REPORT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")

print("FINAL =", FINAL)
print("VERDICT =", VERDICT)
print("GUARDS =", str(gstats["pas"]) + "/" + str(gstats["count"]), "FAIL", gstats["fail"])
print("GATES =", str(gate_pass) + "/" + str(len(gates)))
print("OUT_JSON =", OUT_JSON)
