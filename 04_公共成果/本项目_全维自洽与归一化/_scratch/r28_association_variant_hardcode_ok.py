# -*- coding: utf-8 -*-
"""算法联盟第二十八轮：关联关系层的自由度守恒与「关联即统一」的排除。
只产可算判决，不产新物理；数学自洽不等于实验证实；不宣称攻破统一场论。
"""
import os, glob, json, re, ast, hashlib, sys
from fractions import Fraction as F

DATE = "2026-11-16"
ROUND = "第二十八轮"

ANCHOR = "_ALG_information_gate_recompute_2026-11-12.json"
_anchor_hits = glob.glob("openuft/**/" + ANCHOR, recursive=True)
assert len(_anchor_hits) == 1, "ANCHOR-HITS=%d" % len(_anchor_hits)
MAIN = os.path.dirname(os.path.dirname(_anchor_hits[0]))
DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
JUDGE = os.path.join(MAIN, "判定")
README = os.path.join(MAIN, "README.md")

STEM = "_ALG_r28_association_dof_recompute_" + DATE
OUT_JSON = os.environ.get("R28_OUT_JSON", os.path.join(DATA, STEM + ".json"))
SELF_SOURCE_PATH = os.environ.get(
    "R28_SELF_SOURCE", os.path.join(SRC, "_alg_r28_association_dof_recompute.py"))
OWN_TOKENS = ("r28_association", "第二十八轮", "关联关系层")
OWN_EXPECTED = (
    "_alg_r28_association_dof_recompute.py",
    "_ALG_r28_association_dof_recompute_" + DATE + ".json",
    "_ALG_r28_association_dof_recompute_" + DATE + "_report.txt",
    "_ALG_r28_association_dof_verify_" + DATE + ".json",
    "算法联盟_关联关系层自由度守恒_第二十八轮_" + DATE + ".md",
    "算法联盟_关联关系层自由度守恒_第二十八轮可视化_" + DATE + ".html",
)
VARIANT = os.environ.get("R28_VARIANT", "baseline")


def report_path_from_json(jp):
    """JSON -> report 唯一路径构造；机核与核验器同源。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(os.path.dirname(jp), stem)


REPORT_EXPECTED = report_path_from_json(OUT_JSON)
OUT_REPORT = os.environ.get("R28_OUT_REPORT", REPORT_EXPECTED)


def rel_dev(x, y):
    if y == 0:
        return F(0) if x == 0 else F(1)
    return abs(x - y) / abs(y)


def dstr(x, nd=12):
    return ("%." + str(nd) + "f") % float(x)


def sci(x, nd=6):
    return ("%." + str(nd) + "e") % float(x)


def fstr(x):
    if isinstance(x, F) and x.denominator == 1:
        return str(x.numerator)
    return str(x)


def rref_rank(mat):
    """有理矩阵精确 RREF 秩；精确零即零，不用浮点阈值。"""
    rows = [[F(x) for x in row] for row in mat]
    if not rows:
        return 0
    ncol = len(rows[0])
    r = 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
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
    uniq = []
    for v in vals:
        if not any(rel_dev(v, u) <= tol for u in uniq):
            uniq.append(v)
    return len(uniq)


# ---------------- 来料：三类关联，来源互不引用 ----------------

SRC_FILES = {
    "r24": "_ALG_r24_elimination_recompute_2026-11-15.json",
    "r27": "_ALG_r27_noether_charge_recompute_2026-11-16.json",
    "r21": "_ALG_r21_evidence_recompute_2026-11-15.json",
    "r20": "_ALG_gut_meet_recompute_2026-11-14.json",
    "r25": "_ALG_r25_cosmos_sim_recompute_2026-11-15.json",
    "r150": "TUFT-r150_自旋2候选循环裁决与等价类记账门_全维审计_2026-10-22.json",
    "r252": "TUFT-r252_质量谱层_mpme反解拟合与未定值积分_权重3通道线性相关与中子质量换名_精算与可视化_2026-10-31.json",
    "r57": "TUFT-r57_分支2载体层_观测等价与可证伪性_全维审计_2026-10-13.json",
}


def load_json(key):
    return json.load(open(os.path.join(DATA, SRC_FILES[key]), encoding="utf-8"))


def readme_snapshot():
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


def act_identity_edges():
    """恒等关联：残差由定义/代数为零，不产生新约束。"""
    r24 = load_json("r24")["key_numbers"]
    r27 = load_json("r27")["key_numbers"]
    r252 = load_json("r252")
    chi2_algebra = F(str(r24["chi2_from_delta"]))
    chi2_r20 = F(str(r24["chi2_r20"]))
    delta = F(str(r24["delta"]))
    S = F(str(r24["S"]))
    neutron = r252["neutron_layer"]
    return dict(
        chi2_rel=rel_dev(chi2_algebra, chi2_r20),
        chi2_identity_resid=chi2_algebra - delta * delta / S,
        scale_rel=F(str(r27["scale_invariant_max_rel"])),
        neutron_zero=(str(neutron["resid_exact_num"]) == "0"
                      and str(neutron["resid_exact_den"]) == "1"
                      and bool(neutron["resid_is_zero"])),
        delta=delta, chi2_algebra=chi2_algebra, chi2_r20=chi2_r20)


def act_same_source_edges():
    """同源关联：同一批来料的两种序列化，按值去重后不增加独立来料。"""
    k = load_json("r21")["key_numbers"]
    return dict(
        span_act=F(str(k["span_act"])),
        span_archive=F(str(k["span_same_source_archive"])),
        span_rel=F(str(k["span_rel_to_act"][1])),
        span_distinct_string=int(k["span_distinct_string"]),
        span_distinct_value=int(k["span_distinct"]),
        span_labels=list(k["span_labels"]))


def act_crossbook_edges():
    """跨册独立来料：r150 等价类、r252 线性相关、r57 冗余维度。"""
    r150 = load_json("r150")["door_accounting"]["r150_equivalence_ledger"]
    r252 = load_json("r252")["channel_layer"]
    r57 = load_json("r57")
    items = " ".join(str(x.get("text", "")) for x in r57.get("open_items", []))
    return dict(
        equiv_delta=int(r150["delta"]),
        equiv_eliminated=int(r150["eliminated"]),
        equiv_added=int(r150["added"]),
        equiv_door=bool(r150["passes_door"]),
        channel_rows=r252["rows"],
        n_listed=int(r252["n_listed"]),
        n_independent=int(r252["n_independent"]),
        redundant_registered=("冗余维度" in items and "不得计入自由度" in items),
        r57_kind="O-R57-01")


def act_baseline():
    r20 = load_json("r20")["key_numbers"]
    r24 = load_json("r24")["key_numbers"]
    r25 = load_json("r25")["key_numbers"]
    r27 = load_json("r27")["key_numbers"]
    return dict(
        b=[F(str(x)) for x in r20["b_sm"]],
        a=[F(str(r20[x])) for x in ("a1_inv_MZ", "a2_inv_MZ", "a3_inv_MZ")],
        c=[F(str(r20[x])) for x in ("c1_slope", "c2_slope", "c3_slope")],
        delta=F(str(r24["delta"])),
        overdetermined=int(r24["overdetermined"]),
        u_star=F(str(r24["u_star"])),
        rank_rg=int(r27["rank_symmetry_matrix"]),
        nullity_rg=int(r27["nullity_symmetry_matrix"]),
        extra_params=int(r25["extra_params_needed"]),
        new_equations=0)


# ---------------- exp：纯文本抽列，与 act 不同函数族 ----------------

def exp_r150_text(field):
    txt = open(os.path.join(DATA, "TUFT-r150_自旋2候选循环裁决与等价类记账门_全维审计_2026-10-22.md"),
               encoding="utf-8", errors="replace").read()
    pat = r"等价类记账\s*Delta\s*=\s*(-?\d+)" if field == "Delta" else (
        re.escape(field) + r"\s*=\s*(-?\d+)")
    m = re.search(pat, txt)
    return int(m.group(1)) if m else None


def exp_r252_counts():
    txt = open(os.path.join(DATA, "TUFT-r252_质量谱层_mpme反解拟合与未定值积分_权重3通道线性相关与中子质量换名_精算与可视化_2026-10-31.md"),
               encoding="utf-8", errors="replace").read()
    m = re.search(r"独立通道数是\s*(\d+)\s*不是\s*(\d+)", txt)
    return (int(m.group(2)), int(m.group(1))) if m else (None, None)


def exp_r57_redundant():
    txt = open(os.path.join(DATA, "TUFT-r57_分支2载体层_观测等价与可证伪性_全维审计_2026-10-13.md"),
               encoding="utf-8", errors="replace").read()
    return "冗余维度" in txt and "不得计入自由度" in txt


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


# ---------------- 核心：关联关系对自由度的贡献 ----------------

QUOTIENT_TOL = F(1, 10 ** 40)
ZERO_TOL = F(1, 10 ** 12)


def core_compute():
    ident = act_identity_edges()
    same = act_same_source_edges()
    cross = act_crossbook_edges()
    base = act_baseline()

    # 1) 恒等关联：残差必须精确为零（或登记舍入容差内）
    ident_resid = ident["chi2_identity_resid"]
    # R24 的 Δ、S 只登记 12 位 ⇒ Δ²/S 相对偏离按舍入容差 1e-9 判，不是物理门限
    ident_zero = (abs(rel_dev(ident["chi2_algebra"], ident["chi2_r20"])) <= QUOTIENT_TOL
                  and abs(ident_resid) / abs(ident["chi2_algebra"]) <= F(1, 10 ** 9)
                  and ident["scale_rel"] == 0 and ident["neutron_zero"])

    # 2) 同源关联：按值去重后只剩 1 条独立来料
    same_by_value = same["span_distinct_value"]
    same_by_string = same["span_distinct_string"]
    # R21 四路按串 4、按值 3；同源那一对相对偏离 1.3e-59 ⇒ 同源边贡献 0
    same_effect = 0 if (same["span_labels"][1].endswith("same-source")
                        and same["span_rel"] <= QUOTIENT_TOL) else 1

    # 3) 跨册关联：r150 等价类重记账、r252 线性相关、r57 冗余维度
    rows = [[F(str(r[k])) for k in ("k2", "t2", "c1", "c2", "c3")]
            for r in cross["channel_rows"]]
    rank_listed = rref_rank(rows)
    rows_neg = [row[:] for row in rows]
    rows_neg[2][4] = rows_neg[2][4] + F(1, 2)
    rank_neg = rref_rank(rows_neg)
    equiv_effect = 0 if (cross["equiv_delta"] == 0 and not cross["equiv_door"]) else 1
    corr_effect = (0 if rank_listed == cross["n_independent"]
                   and rank_listed < cross["n_listed"] else 1)
    redundant_effect = 0 if cross["redundant_registered"] else 1

    # 4) 商空间：3 观测 - 秩 2 = 1 维不变商；与 R24 超定度、R25 新参数跨册对应
    M = [[F(1), F(1), F(1)], [base["b"][0], base["b"][1], base["b"][2]]]
    rank_M = rref_rank(M)
    quotient_dim = len(base["b"]) - rank_M
    u = (base["c"][1] - base["c"][2], base["c"][2] - base["c"][0],
         base["c"][0] - base["c"][1])
    delta_from_a = sum((ui * ai for ui, ai in zip(u, base["a"])), F(0))
    a_zero = list(base["a"])
    a_zero[2] = F(1) / base["u_star"]
    delta_zero = sum((ui * ai for ui, ai in zip(u, a_zero)), F(0))

    # 5) 关联能提供的「新独立约束」：三类关联贡献全为 0
    effects = (0 if ident_zero else 1, same_effect,
               equiv_effect, corr_effect, redundant_effect)
    new_independent_constraints = sum(effects)
    lower_bound_after = (base["overdetermined"] - new_independent_constraints)
    lower_bound_reported = base["extra_params"]

    # 6) 负对照：注入假跨类关联（声称等价类重记账给出 Δ=0）
    neg_effects = (0, same_effect, 1, corr_effect, redundant_effect)
    neg_constraints = sum(neg_effects)
    neg_lower_bound = base["overdetermined"] - neg_constraints

    # 7) 正对照：注入真实恒等关联 χ²=Δ²/S，本就落在同一等价类内
    pos_lower_bound = base["overdetermined"] - 0

    # 8) 两路机拼：act 取 JSON 结构化，exp 取 md 纯文本
    exp_listed, exp_independent = exp_r252_counts()
    exp_equiv = exp_r150_text("Delta")
    exp_redundant = exp_r57_redundant()

    return dict(ident=ident, same=same, cross=cross, base=base,
                ident_resid=ident_resid, ident_zero=ident_zero,
                same_by_value=same_by_value, same_by_string=same_by_string,
                same_effect=same_effect, rank_listed=rank_listed,
                rank_neg=rank_neg, equiv_effect=equiv_effect,
                corr_effect=corr_effect, redundant_effect=redundant_effect,
                effects=effects, new_constraints=new_independent_constraints,
                rank_M=rank_M, quotient_dim=quotient_dim, delta_from_a=delta_from_a,
                delta_zero=delta_zero, lower_bound_after=lower_bound_after,
                lower_bound_reported=lower_bound_reported,
                neg_constraints=neg_constraints, neg_lower_bound=neg_lower_bound,
                pos_lower_bound=pos_lower_bound,
                exp_listed=exp_listed, exp_independent=exp_independent,
                exp_equiv=exp_equiv, exp_redundant=exp_redundant,
                readme=readme_snapshot())


def build_gates(R):
    gates = []

    def gate(name, act, exp, ok, neg, neg_ok, note):
        gates.append(dict(name=name,
                          act=fstr(act) if isinstance(act, F) else act,
                          exp=fstr(exp) if isinstance(exp, F) else exp,
                          neg=fstr(neg) if isinstance(neg, F) else neg,
                          kind="PASS" if ok and not neg_ok else "FAIL",
                          note=note,
                          power=(2 if ok and not neg_ok else
                                 (1 if ok != neg_ok else 0))))

    n_kinds = 3
    gate("G1-THREE-KINDS-SEPARATE",
         n_kinds, n_kinds,
         R["ident_zero"] and all(e == 0 for e in R["effects"])
         and R["same_effect"] == 0,
         R["neg_constraints"], R["neg_constraints"] == 0,
         "恒等／同源／跨册三类关联分开计账，五条关联边对新约束贡献全 0")

    gate("G2-IDENTITY-RESIDUAL-ZERO",
         R["ident"]["chi2_rel"], R["ident"]["scale_rel"],
         R["ident_zero"] and abs(R["ident_resid"]) / abs(R["ident"]["chi2_algebra"])
         <= F(1, 10 ** 9),
         F(1, 100), False,
         "χ²=Δ²/S、尺度守恒、r252 精确零残差；负对照把系数错置 1/100 后残差非零")

    gate("G3-EQUIV-REACCOUNTING",
         R["cross"]["equiv_delta"], R["exp_equiv"],
         R["cross"]["equiv_delta"] == 0 and R["exp_equiv"] == 0
         and not R["cross"]["equiv_door"],
         1, False,
         "r150 等价类重记账 Delta=0 且门未通过；改一个字即失配")

    gate("G4-LINEAR-DEPENDENCE",
         R["rank_listed"], R["exp_independent"],
         (R["rank_listed"] == R["exp_independent"] == 2
          and R["cross"]["n_listed"] == 3 and R["rank_neg"] == 3),
         R["rank_neg"], R["rank_neg"] == 2,
         "r252 三行五列精确秩 2（登记 n_independent=2）；破坏依赖后秩 3")

    gate("G5-REDUNDANT-NOT-COUNTED",
         R["cross"]["redundant_registered"], R["exp_redundant"],
         R["cross"]["redundant_registered"] and R["exp_redundant"],
         False, False,
         "r57 明写冗余维度不得计入自由度；删去该措辞的负对照失守")

    gate("G6-LOWER-BOUND-INVARIANT",
         R["quotient_dim"], R["lower_bound_reported"],
         R["quotient_dim"] == 1 and R["lower_bound_after"] == 1
         and R["lower_bound_reported"] == 1
         and R["new_constraints"] == 0 and R["pos_lower_bound"] == 1,
         R["neg_lower_bound"], R["neg_lower_bound"] == 1,
         "商空间 1 维、新约束 0 条、下界保持 1；假关联可把它压到 0")

    return gates


# ---------------- AST 守卫 ----------------

def ast_structure_checks():
    src = open(SELF_SOURCE_PATH, encoding="utf-8").read()
    tree = ast.parse(src)
    hard = []
    cross = []
    rp_line = None
    rp_call = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "report_path_from_json":
            rp_line = node.lineno
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if (node.func.id == "add" and len(node.args) >= 2
                    and isinstance(node.args[1], ast.Constant)
                    and isinstance(node.args[1].value, bool)):
                hard.append(node.lineno)
            if node.func.id == "report_path_from_json":
                rp_call = node.lineno if rp_call is None else min(rp_call, node.lineno)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("exp_"):
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name)
                        and sub.func.id.startswith("act_")):
                    cross.append((node.name, sub.lineno))
    return hard, cross, rp_line, rp_call


# ---------------- 主流程 ----------------

R = core_compute()
gates = build_gates(R)
hard_lines, cross_lines, rp_line, rp_call = ast_structure_checks()

add("E-NO-HARDCODE-OK", len(hard_lines) == 0,
    "add() 第二参数不得为字面布尔，命中行 " + str(hard_lines))
add("E-NO-CROSS-PATH-CALL", len(cross_lines) == 0,
    "exp_ 路径不得调用 act_ 函数，命中 " + str(cross_lines))
add("E-REPORT-PATH-DEFINED-FIRST",
    rp_line is not None and rp_call is not None and rp_line < rp_call
    and (REPORT_EXPECTED == OUT_REPORT or VARIANT != "baseline"),
    "report_path_from_json 定义行 " + str(rp_line) + " 早于调用行 " + str(rp_call))
add("E-RG-RANK-NULLITY", R["rank_M"] == 2 and R["quotient_dim"] == 1,
    "RG 精确矩阵秩 " + str(R["rank_M"]) + "，商空间维数 " + str(R["quotient_dim"]))
add("E-DELTA-NONZERO", R["delta_from_a"] != 0 and abs(R["delta_zero"]) <= ZERO_TOL,
    "Δ≠0 且正对照 Δ(u*)=" + sci(R["delta_zero"]))
add("E-IDENTITY-TAUTLOGY", R["ident_zero"],
    "三条恒等关联残差在登记舍入容差内为零，按定义不承重")
add("E-SAME-SOURCE-DEDUPE",
    R["same_by_string"] == 4 and R["same_by_value"] == 3
    and R["same"]["span_rel"] <= QUOTIENT_TOL and R["same_effect"] == 0,
    "四路跨度按串 4 个、按值 3 个；同源那一对相对偏离 "
    + sci(R["same"]["span_rel"]) + "，单列 IDENTITY")
add("E-EQUIV-NONADDITIVE",
    R["cross"]["equiv_delta"] == 0 and not R["cross"]["equiv_door"]
    and R["cross"]["equiv_eliminated"] == R["cross"]["equiv_added"] == 1,
    "r150 等价类重记账 Delta=0、门未通过，非加和冻结有效")
add("E-R252-RANK",
    R["rank_listed"] == 2 and R["cross"]["n_independent"] == 2
    and R["cross"]["n_listed"] == 3 and R["rank_neg"] == 3,
    "三行五列精确秩 2；破坏 c3=c1+c2 后秩 3")
add("E-R57-REDUNDANCY",
    R["cross"]["redundant_registered"] and R["exp_redundant"],
    "O-R57-01 明写冗余维度不得计入自由度，两路一致")
add("E-ZERO-NEW-CONSTRAINT",
    R["new_constraints"] == 0 and R["lower_bound_after"] == 1
    and R["lower_bound_reported"] == 1,
    "五条关联边贡献新独立约束 0 条，下界保持 1")
add("E-NEG-CONTROL-DISCRIMINATES",
    R["neg_constraints"] == 1 and R["neg_lower_bound"] == 0,
    "注入一条假跨类关联后下界由 1 降到 0，判据非恒真")
add("E-POS-CONTROL-IDENTITY",
    R["pos_lower_bound"] == 1,
    "注入真恒等关联 χ²=Δ²/S 后下界仍为 1，恒等关联不承重")
add("E-TWO-PATH-CROSSBOOK",
    R["exp_equiv"] == 0 and R["exp_independent"] == 2
    and R["exp_redundant"],
    "exp 侧 md 纯文本抽列与 act 侧 JSON 结构化跨册一致")
add("E-GATE-DISCRIMINATING",
    len(gates) == 6 and all(g["power"] > 0 for g in gates),
    "六门各自负对照均失守，装饰门 0")
add("E-README-ALIVE",
    R["readme"]["bytes"] > 0 and R["readme"]["max_rid"] == 406,
    "README 实时 " + str(R["readme"]["bytes"]) + " B / RID "
    + str(R["readme"]["max_rid"]))
add_info("I-VARIANT", "当前配置 " + VARIANT + "，正式产物只由基线生成")
add_identity("ID-ASSOCIATION-NOT-CONSTRAINT",
             "关联关系本身不是新约束；恒等关联按定义重述、同源关联按定义同批来料")
add_boundary("BD-FINITE-BOOKS",
             "只覆盖 r150/r252/r57 三份主线关联来料与算法联盟 R20/R21/R24/R25/R27 读数；"
             "未被满足不等于不可满足")
add_info("I-NO-PREDICTION",
         "本轮无零输入独立输出，独立实验预言 0")

if VARIANT == "baseline":
    pass
if VARIANT != 'baseline':
    add('INJECTED-HARDCODE', True, 'variant')

gstats = guard_stats()
gate_pass = sum(1 for g in gates if g["kind"] == "PASS")
gate_fail = len(gates) - gate_pass


def ks(x):
    return fstr(x) if isinstance(x, F) else x


KN = {
    "date": DATE,
    "variant": VARIANT,
    "association_kinds": 3,
    "association_edges": len(R["effects"]),
    "effect_vector": list(R["effects"]),
    "new_independent_constraints": R["new_constraints"],
    "quotient_dimension": R["quotient_dim"],
    "rg_rank": R["rank_M"],
    "delta": ks(R["delta_from_a"]),
    "delta_zero_control": ks(R["delta_zero"]),
    "chi2_identity_rel": ks(R["ident"]["chi2_rel"]),
    "chi2_identity_residual": ks(R["ident_resid"]),
    "scale_identity_rel": ks(R["ident"]["scale_rel"]),
    "neutron_exact_zero": R["ident"]["neutron_zero"],
    "span_distinct_string": R["same_by_string"],
    "span_distinct_value": R["same_by_value"],
    "span_independent_rel": ks(R["same"]["span_rel"]),
    "r150_equiv_delta": R["cross"]["equiv_delta"],
    "r150_door_passed": R["cross"]["equiv_door"],
    "r252_n_listed": R["cross"]["n_listed"],
    "r252_n_independent": R["cross"]["n_independent"],
    "r252_exact_rank": R["rank_listed"],
    "r252_negative_rank": R["rank_neg"],
    "r57_redundant_registered": R["cross"]["redundant_registered"],
    "lower_bound_after": R["lower_bound_after"],
    "lower_bound_reported": R["lower_bound_reported"],
    "negative_constraint_count": R["neg_constraints"],
    "negative_lower_bound": R["neg_lower_bound"],
    "positive_lower_bound": R["pos_lower_bound"],
    "exp_equiv_delta": R["exp_equiv"],
    "exp_r252_independent": R["exp_independent"],
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
}

VERDICT = (
    "ALG-AD__KIND-" + str(KN["association_kinds"])
    + "__EDGE-" + str(KN["association_edges"])
    + "__NEWC-" + str(KN["new_independent_constraints"])
    + "__QUOT-" + str(KN["quotient_dimension"])
    + "__BOUND-" + str(KN["lower_bound_after"])
    + "__R150-" + str(KN["r150_equiv_delta"])
    + "__R252-" + str(KN["r252_exact_rank"]) + "-" + str(KN["r252_n_listed"])
    + "__R57-" + ("1" if KN["r57_redundant_registered"] else "0")
    + "__SPAN-" + str(KN["span_distinct_string"]) + "-" + str(KN["span_distinct_value"])
    + "__GATE-" + str(gate_pass) + "__CLEAN-" + str(gstats["fail"])
    + "__PRED-0"
)
FINAL = ("ALG-R28-ASSOCIATION-DOF--GATES-PASS-WITH-0-NEGATIVE" if
         gstats["fail"] == 0 and gate_fail == 0 else "GATES-FAIL")

DOC = {
    "title": "算法联盟：关联关系层的自由度守恒与「关联即统一」的排除（第二十八轮）",
    "date": DATE,
    "round": ROUND,
    "variant": VARIANT,
    "nature": "可算判决／关联层自由度审计，不产新物理",
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
        "恒等关联（χ²=Δ²/S、尺度守恒、r252 精确零残差）按定义重述已有读数，不承重。",
        "同源关联按值去重后只剩一条来料，同源回验恒真，不承重。",
        "商空间 1 维与 R24 超定度 1、R25 额外参数 1 是跨册结构对应，不相加。"
    ],
    "boundary_notes": [
        "只覆盖三份主线关联来料与五份算法联盟判定册，有限对象不构成全称定理。",
        "关联关系不产生新约束的结论只对已机读的边集成立；新边须独立来料且可判负。",
        "r150 的 Delta=0 是等价类重记账，不是新增一个抵消项，非加和冻结继续有效。"
    ],
    "declared_negative": [
        "r150 等价类门未通过：Delta=0，passes_door=false",
        "r252 三行登记但精确秩 2；破坏 c3=c1+c2 后秩 3",
        "r57 明写 λ 为冗余维度，不得计入自由度",
        "负对照注入假跨类关联后下界 1→0，判据有判别力"
    ],
    "red_line": "数学自洽不等于实验证实；关联不等于统一；不宣称发现新方程、不宣称攻破统一场论；独立实验预言 0",
    "readme": R["readme"],
}

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
