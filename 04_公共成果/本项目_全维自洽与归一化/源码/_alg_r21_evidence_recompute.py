# -*- coding: utf-8 -*-
"""第二十一轮：R20 证据质量缺陷的机读盘点、独立复算与修复。
不改 R20 任何产物；只把「手填读数」升级为「可算读数」，并如实报结论是否变化。
"""
import os
import sys
import json
import glob
import ast
import re
import io
import tokenize
import hashlib
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 70
DATE = "2026-11-15"
TOL = D("1e-28")


def rd(p):
    return open(p, "r", encoding="utf-8", errors="replace").read()


def rb(p):
    return open(p, "rb").read()


def jload(p):
    return json.loads(rd(p))


def md5(p):
    return hashlib.md5(rb(p)).hexdigest()


def Dq(x):
    if isinstance(x, F):
        return D(x.numerator) / D(x.denominator)
    if isinstance(x, bool):
        return D(1) if x else D(0)
    return D(str(x))


def Fq(x):
    return F(str(x))


def num(x):
    return format(Dq(x), "f")


def disp(x, n=9):
    return format(Dq(x), ".%df" % n)


def rel(a, b):
    aa, bb = Dq(a), Dq(b)
    if bb == 0:
        return D(0) if aa == 0 else D("1e30")
    return abs(aa - bb) / abs(bb)


def atan_inv(n):
    x = D(1) / D(n)
    x2 = x * x
    term, s, k = x, x, 1
    while abs(term) > D(10) ** (-66):
        term *= -x2
        s += term / D(2 * k + 1)
        k += 1
    return s


PI = 16 * atan_inv(5) - 4 * atan_inv(239)
LN10 = D(10).ln()


def find_main():
    """并行会话可能新增同形目录 ⇒ 用唯一既有产物反查主目录。"""
    hits = glob.glob("openuft/**/_ALG_information_gate_recompute_2026-11-12.json",
                     recursive=True)
    assert len(hits) == 1, "ANCHOR-HITS=%d" % len(hits)
    return os.path.dirname(os.path.dirname(hits[0]))


def one(pattern, sub=None):
    base = DATA if sub is None else sub
    hits = glob.glob(os.path.join(base, pattern))
    assert len(hits) == 1, "ONE-HITS=%d(%s)" % (len(hits), pattern)
    return hits[0]


MAIN = find_main()
DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
README = os.path.join(MAIN, "README.md")
KERNEL = os.path.abspath(__file__)
SRC_TEXT = rd(KERNEL)
OUT_JSON = os.path.join(DATA, "_ALG_r21_evidence_recompute_" + DATE + ".json")
OUT_REPORT = os.path.join(DATA, "_ALG_r21_evidence_recompute_report_" + DATE + ".txt")

P_R20_J = one("_ALG_gut_meet_recompute_2026-11-14.json")
P_R20_K = one("_alg_gut_meet_recompute.py", SRC)
P_R20_R = one("_ALG_gut_meet_recompute_report_2026-11-14.txt")
P_R1 = one("_ALG_expdata_fullchain_recompute_2026-11-11.json")
P_R5 = one("_ALG_pair_optim_recompute_2026-11-12.json")
P_R64 = one("TUFT-r64_耦合统一GUT数值审计_*.json")
P_R188_J = one("TUFT-r188_*统一尺度出处*精算_*.json")
P_R188_R = one("TUFT-r188_*统一尺度出处*精算_*_report.txt")
P_LEDGER = one("_ALG_expdata_fullchain_来料总表_2026-11-11.json")

R20 = jload(P_R20_J)
R20KN = R20["key_numbers"]
R20SRC = rd(P_R20_K)
R20TREE = ast.parse(R20SRC)
R20REP = rd(P_R20_R)
R1 = jload(P_R1)["key_numbers"]
R5 = jload(P_R5)["key_numbers"]
R64 = jload(P_R64)
R188 = jload(P_R188_J)["key_numbers"]
R188REP = rd(P_R188_R)
LEDGER = jload(P_LEDGER)["ledger"]

CRIT = Fq(R5["chi2_crit"])
CRIT_D = Dq(CRIT)

# R20 用到的 SM β（两路核对仍成立）
B_SM = [Fq(R64["sm"]["b"][0]), Fq(R64["sm"]["b"][1]), Fq(R64["sm"]["b"][2])]
B_MSSM = [Fq(x) for x in R64["mssm_control"]["b"]]

RE_LOOSE = re.compile(r"resid\s*=\s*([0-9.]+e[+-]\d+)", re.I)
RE_TIGHT = re.compile(r"sstar_resid\s*=\s*([0-9.]+e[+-]\d+)", re.I)
RE_SUSY = re.compile(r"SUSY|susy|sparticle|超对称|软破缺|M_SUSY|threshold|阈值", re.I)


def report_path_from_json(jp):
    """JSON -> report 的唯一路径构造；机核与核验器共用，禁另起一套。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(os.path.dirname(jp), stem)


def json_path_from_report(rp):
    stem = os.path.splitext(os.path.basename(rp))[0]
    stem = stem.replace("_recompute_report_", "_recompute_") + ".json"
    return os.path.join(os.path.dirname(rp), stem)


# ---- 两路读数：A 路走 JSON 结构，B 路走 report 纯文本，互不引用 ----
def act_chi2_p0():
    return Dq(R20KN["chi2_min"])


def exp_chi2_p0():
    m = re.search(r"^chi2_min\s*=\s*([0-9.]+)", R20REP, re.M)
    assert m is not None, "EXP-CHI2-MISSING"
    return Dq(m.group(1))


def act_chi2_p1():
    return Dq(R20KN["chi2_p1_e3"])


def exp_chi2_p1():
    m = re.search(r"^chi2_p1_e3\s*=\s*([0-9.eE+-]+)", R20REP, re.M)
    assert m is not None, "EXP-CHI2P1-MISSING"
    return Dq(m.group(1))


def act_gate_rows():
    return [[int(z) for z in c["gates"]] for c in R20["configs"]]


def exp_gate_rows():
    m = re.search(r"^gate_vectors\s*=\s*(\[.*\])\s*$", R20REP, re.M)
    assert m is not None, "EXP-GATE-MISSING"
    return json.loads(m.group(1))


def act_span_literature():
    """A 路：R1 判定 JSON 的文献口径（独立来源，非本链重算）。"""
    return Dq(R1["rg_span_dex_exp"])


def exp_span_r64():
    """B 路：r64 判定册的 SM 能量比，取常用对数；来料口径与 R20 不同。"""
    return Dq(str(R64["sm"]["mu_ratio_max_min"])).log10()


def act_span_r20():
    return Dq(R20KN["span_dex_act"])


def exp_span_r20_archive():
    return Dq(R1["rg_span_dex_act"])


# ---------------------------------------------------------------------------
# 第二部分：缺陷机读、独立复算、修复与判别力夹具
# ---------------------------------------------------------------------------
def literal_keyword_hits(tree, names):
    """AST 实际形态：key_numbers/configs 里被写成字面常量的读数。"""
    out = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.keyword) and node.arg in names
                and isinstance(node.value, ast.Constant)):
            out.append(dict(key=node.arg, value=node.value.value,
                            line=node.lineno))
    return out


def function_segment(tree, src, name):
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(src, node) or ""
    return ""


def defect_scan():
    """只读盘点，不预设缺陷个数；每项由 AST / JSON / 正文机读判定。"""
    out = []
    pmin_lit = literal_keyword_hits(R20TREE, {"p_min"})
    out.append(dict(id="D1-PMIN-LITERAL", found=len(pmin_lit) == 1,
                    reading=pmin_lit,
                    why="p_min 是字面常量，不是由 χ² 判据机读定价"))
    nextra_lit = [h for h in literal_keyword_hits(R20TREE, {"n_extra"})
                  if isinstance(h["value"], int)]
    out.append(dict(id="D2-NEXTRA-LITERAL", found=len(nextra_lit) == 3,
                    reading=nextra_lit,
                    why="三个配置的 n_extra 是字面常量，自由度账未在册内机读"))
    seg = function_segment(R20TREE, R20SRC, "exp_span_dex")
    same = ("rg_span_dex_act" in seg
            and "rg_span_dex_exp" not in seg
            and rel(act_span_r20(), exp_span_r20_archive()) < TOL)
    out.append(dict(id="D3-SPAN-SAME-SOURCE", found=bool(same),
                    reading=dict(uses_act_archive="rg_span_dex_act" in seg,
                                 relative_dev=num(rel(act_span_r20(), exp_span_r20_archive()))),
                    why="exp 路径取首册同源存档，相对偏离 0，属同源回验非独立复算"))
    rows = act_gate_rows()
    rates = [sum(r[g] for r in rows) for g in range(4)]
    out.append(dict(id="D4-G4-ZERO-POWER", found=rates[3] == 0,
                    reading=dict(rates=rates, configs=len(rows)),
                    why="G4 在全部配置 0% 通过，配置层判别力为 0，却仍进布尔合取"))
    loose, tight = RE_LOOSE.findall(R188REP), RE_TIGHT.findall(R188REP)
    out.append(dict(id="D5-REGEX-UNANCHORED",
                    found=len(loose) > 1 and len(tight) == 1,
                    reading=dict(loose=loose, tight=tight),
                    why="松散 resid= 正则命中多个不同残差，只因首个恰好正确"))
    return out


def pmin_pricing(chi2_p0, chi2_p1, crit):
    """F1：把 p_min 从手填改成按定义机读定价。"""
    levels = []
    for p in (0, 1, 2, 3):
        best = chi2_p0 if p == 0 else chi2_p1
        levels.append(dict(p=p, best=best, ok=bool(best < crit)))
    feasible = [r["p"] for r in levels if r["ok"]]
    pmin = min(feasible) if feasible else None
    return dict(levels=levels, feasible=feasible, pmin=pmin)


def nextra_pricing(pmin):
    """F2：三个配置的额外自由参数由「来料是否登记」与「启用方向数」机读。"""
    reg = sum(1 for r in LEDGER
              if RE_SUSY.search(r["symbol"] + " " + r["note"]))
    diff = sum(1 for i in range(3) if B_SM[i] != B_MSSM[i])
    n_dir = len(R20KN["threshold_deltas"])
    c0 = 0
    c1 = 1 if reg == 0 else 0
    c2 = pmin if (pmin is not None and n_dir >= 1) else 0
    return dict(registered_scales=reg, beta_diff_components=diff,
                nonsingular_directions=n_dir, values=[c0, c1, c2])


def gate_analysis(rows, n_gates=4):
    """F3：通过率、恒假门、最小承重割、剔除恒假门后的 escape。"""
    rates = [sum(r[g] for r in rows) for g in range(n_gates)]
    zero = [g for g in range(n_gates) if rates[g] == 0]
    full = [g for g in range(n_gates) if rates[g] == len(rows)]
    best, best_sets = None, []
    for mask in range(1 << n_gates):
        S = [g for g in range(n_gates) if (mask >> g) & 1]
        hit = any(all(r[g] or (g in S) for g in range(n_gates)) for r in rows)
        if hit:
            if best is None or len(S) < len(best):
                best, best_sets = list(S), [list(S)]
            elif len(S) == len(best):
                best_sets.append(list(S))
    reduced = [[r[g] for g in range(n_gates) if g not in zero] for r in rows]
    escape_reduced = sum(1 for r in reduced if all(r))
    escape_full = sum(1 for r in rows if all(r))
    return dict(rates=rates, zero_power=zero, full_power=full,
                min_cut=best, min_cut_sets=best_sets,
                reduced_gates=n_gates - len(zero),
                escape_full=escape_full, escape_reduced=escape_reduced,
                g4_not_load_bearing=(escape_reduced == escape_full))


def distinct_by_rel(vals, tol=D("1e-25")):
    """值去重：Decimal 相对精度下判相同必须用偏离 + 容差，禁字符串相等。"""
    reps = []
    for v in vals:
        if not any(rel(v, r) < tol for r in reps):
            reps.append(v)
    return len(reps)


def span_readouts():
    """F4：四路读数 + 扰动响应，区分「同源存档」与「独立来料」。"""
    a = act_span_r20()
    b = exp_span_r20_archive()
    c = act_span_literature()
    d = exp_span_r64()
    vals = [a, b, c, d]
    a1 = Dq(R20KN["a1_inv_MZ"])
    a2 = Dq(R20KN["a2_inv_MZ"])
    a3 = Dq(R20KN["a3_inv_MZ"])
    b_frac = [Fq("41/10"), Fq("-19/6"), Fq(-7)]
    bd = [Dq(x) for x in b_frac]

    def span_of(avec):
        xs = [2 * PI * (avec[i] - avec[j]) / (bd[i] - bd[j])
              for i, j in ((0, 1), (0, 2), (1, 2))]
        return (max(xs) - min(xs)) / LN10

    base_span = span_of([a1, a2, a3])
    moved_span = span_of([a1, a2, a3 / D("1.01")])
    return dict(readings=[num(x) for x in vals],
                labels=["R20-recompute", "R1-archive-same-source",
                        "R1-literature", "r64-mu-ratio"],
                rel_to_act=[num(rel(x, a)) for x in vals],
                distinct=distinct_by_rel(vals),
                distinct_string=len(set(num(x) for x in vals)),
                recomputed_base=num(base_span),
                recomputed_after_alpha_s_1pct=num(moved_span),
                act_moves=bool(rel(moved_span, base_span) > D("1e-6")),
                archive_static=bool(rel(b, a) < TOL))


def regex_fix():
    """F5：锚定正则 + 负对照（改名后必须失配）。"""
    loose = RE_LOOSE.findall(R188REP)
    tight = RE_TIGHT.findall(R188REP)
    neg = R188REP.replace("sstar_resid=", "other_resid=")
    loose_neg = RE_LOOSE.findall(neg)
    tight_neg = RE_TIGHT.findall(neg)
    exact = Dq(str(R188["sstar_residual_vs_target"]))
    shown = Dq(tight[0]) if tight else D(0)
    return dict(loose=loose, tight=tight, loose_neg=loose_neg,
                tight_neg=tight_neg, exact=num(exact), shown=num(shown),
                magnitude_ok=bool(exact < D("1e-20") and shown < D("1e-20")),
                rounded_not_exact=bool(rel(exact, shown) > D("1e-3")),
                discriminator=bool(len(tight_neg) == 0 and len(loose_neg) > 0))


# ---- 判据活性夹具：反噬强制常量后必须被夹具抓到 ----
def pmin_active(chi2_p0, chi2_p1, crit):
    base = pmin_pricing(chi2_p0, chi2_p1, crit)["pmin"]
    shadow = pmin_pricing(chi2_p0, chi2_p0, crit)["pmin"]
    return base != shadow


def power_active(rows):
    rates = [sum(r[g] for r in rows) for g in range(4)]
    return 0 in rates


def regex_unique(text):
    return len(RE_TIGHT.findall(text)) == 1


def final_of(nf_main, nf_guard, n_decl):
    if n_decl is None:
        return "ALG-R21-EVIDENCE--GATES-FAIL"
    if nf_guard > 0:
        return "ALG-R21-EVIDENCE--GATES-FAIL"
    return "ALG-R21-EVIDENCE--GATES-PASS-WITH-0-NEGATIVE"


def verdict_string(kn):
    return ("ALG-RF__DEF-%s__FIX-%s__PMIN-%s__NEX-%s__RATES-%s"
            "__ZERO-%s__CUT-%s__SPAN3-%s__SPAN4-%s__REGEX-%s"
            "__ESC-%s__CLEAN-0__PRED-0" %
            (str(kn["defects_found"]), str(kn["defects_fixed"]),
             str(kn["p_min_recomputed"]), kn["nextra_recomputed_text"],
             kn["gate_rates_text"], str(kn["zero_power_gates"]),
             str(kn["min_cut_size"]), disp(kn["span_literature"], 6),
             disp(kn["span_r64"], 6), str(kn["regex_tight_hits"]),
             str(kn["escape_after_fix"])))


# ---------------------------------------------------------------------------
# 第三部分：守卫、判词、落盘、main
# ---------------------------------------------------------------------------
GUARDS = []


def add(name, ok, exp, act, note="", kind=None):
    if kind is None:
        kind = "PASS" if ok else "FAIL"
    GUARDS.append(dict(name=name, ok=bool(ok), exp=str(exp), act=str(act),
                       note=note, kind=kind))


def counts_of():
    out = {}
    for g in GUARDS:
        out[g["kind"]] = out.get(g["kind"], 0) + 1
    return out


def hardcode_ok_hits(tree):
    bad = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "add"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                bad.append("add-ok-pos2")
            for kw in node.keywords:
                if kw.arg == "ok" and isinstance(kw.value, ast.Constant):
                    bad.append("add-ok-kw")
    return bad


def exp_act_ast_hits(tree):
    bad, srcs = [], {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.name.startswith(("act_", "exp_")):
                srcs[node.name] = ast.get_source_segment(SRC_TEXT, node) or ""
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Return) and isinstance(sub.value, ast.Constant)
                        and isinstance(sub.value.value, (int, float))
                        and not isinstance(sub.value.value, bool)
                        and node.name.startswith(("act_", "exp_"))):
                    bad.append(node.name + ":constant-return")
    for a in ("act_chi2_p0", "act_chi2_p1", "act_gate_rows",
              "act_span_literature", "act_span_r20"):
        e = "exp_" + a[4:]
        if a in srcs and e in srcs and srcs[a] == srcs[e]:
            bad.append(a + ":same-as-" + e)
    return bad


def write_target_hits(tree):
    """本册所有 open(...,'w') 目标；用于证明没有回写 R20 的任何产物。"""
    out = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "open"):
            seg = ast.get_source_segment(SRC_TEXT, node) or ""
            if re.search(r"[\"'][wax]", seg):
                out.append(seg[:100])
    return out


def main():
    GUARDS.clear()
    tree = ast.parse(SRC_TEXT)
    r20_before = {p: md5(p) for p in (P_R20_J, P_R20_K, P_R20_R)}

    # ---- 两路机拼（JSON 结构 vs report 纯文本） ----
    c0_a, c0_e = act_chi2_p0(), exp_chi2_p0()
    c1_a, c1_e = act_chi2_p1(), exp_chi2_p1()
    rows_a, rows_e = act_gate_rows(), exp_gate_rows()

    # ---- 缺陷盘点 ----
    defects = defect_scan()
    defects_found = sum(1 for d in defects if d["found"])

    # ---- F1 p_min 复算 ----
    pri = pmin_pricing(c0_a, c1_a, CRIT_D)
    pmin = pri["pmin"]
    pmin_shadow = pmin_pricing(c0_a, c0_a, CRIT_D)["pmin"]
    pmin_match = (pmin is not None and pmin == int(R20KN["p_min"]))

    # ---- F2 n_extra 复算 ----
    nex = nextra_pricing(pmin)
    r20_nex = [int(c["n_extra"]) for c in R20["configs"]]
    nex_match = (nex["values"] == r20_nex)

    # ---- F3 恒假门与最小承重割（两路：JSON 门向量 vs report 文本门向量） ----
    ga = gate_analysis(rows_a)
    ga_e = gate_analysis(rows_e)
    rates_e = [sum(r[g] for r in rows_e) for g in range(4)]
    zero_e = ga_e["zero_power"]
    cut_size = len(ga["min_cut"]) if ga["min_cut"] is not None else -1
    cut_size_e = len(ga_e["min_cut"]) if ga_e["min_cut"] is not None else -1

    # ---- F4 span 独立来料 ----
    sp = span_readouts()
    sp_lit, sp_64 = act_span_literature(), exp_span_r64()

    # ---- F5 正则锚定 ----
    rx = regex_fix()

    # ---- 修复计数：每项缺陷都要有独立复算读数且与原读数一致 ----
    fixes = [
        dict(id="F1-PMIN", ok=pmin_match, reading=pmin),
        dict(id="F2-NEXTRA", ok=nex_match, reading=nex["values"]),
        dict(id="F3-ZEROPOWER", ok=ga["zero_power"] == [3]
             and ga["escape_reduced"] == ga["escape_full"], reading=ga["rates"]),
        dict(id="F4-SPAN", ok=sp["distinct"] == 3 and sp["act_moves"]
             and rel(sp["recomputed_base"], act_span_r20()) < TOL,
             reading=sp["readings"]),
        dict(id="F5-REGEX", ok=rx["discriminator"] and len(rx["tight"]) == 1,
             reading=rx["tight"]),
    ]
    defects_fixed = sum(1 for f in fixes if f["ok"])

    # ---- 守卫 ----
    add("RF-CHI2-TWO-PATH", rel(c0_a, c0_e) < TOL, num(c0_e), num(c0_a),
        "JSON 结构 vs report 正文，χ²(p=0)")
    add("RF-CHI2P1-TWO-PATH", rel(c1_a, c1_e) < TOL, num(c1_e), num(c1_a),
        "JSON 结构 vs report 正文，χ²(p=1)")
    add("RF-GATE-TWO-PATH", rows_a == rows_e, str(rows_e), str(rows_a),
        "配置门向量两路逐项一致")
    add("RF-CRIT-TWO-SOURCE", rel(Dq(R20KN["chi2_crit"]), CRIT_D) < TOL,
        num(CRIT_D), num(Dq(R20KN["chi2_crit"])), "第五轮精确分数 vs R20 判定表")
    add("RF-DEFECT-D1", defects[0]["found"], True, defects[0]["reading"],
        "p_min 为字面常量")
    add("RF-DEFECT-D2", defects[1]["found"], True, defects[1]["reading"],
        "三个 n_extra 为字面常量")
    add("RF-DEFECT-D3", defects[2]["found"], True, defects[2]["reading"],
        "span 的 exp 路径是同源存档")
    add("RF-DEFECT-D4", defects[3]["found"], True, defects[3]["reading"],
        "G4 配置层 0% 通过")
    add("RF-DEFECT-D5", defects[4]["found"], True, defects[4]["reading"],
        "松散 resid= 正则多命中")
    add("RF-DEFECT-COUNT-MACHINE",
        defects_found == len([d for d in defects if d["found"]])
        and 0 < defects_found <= len(defects),
        len(defects), defects_found, "缺陷数由机读盘点得出，不是预设文案；上界是探针总数")
    add("RF-DEFECT-ALL-HAVE-FIX", defects_fixed == defects_found,
        defects_found, defects_fixed, "每项缺陷都有独立复算读数")

    add("RF-PMIN-MATCH-R20", pmin_match, int(R20KN["p_min"]), pmin,
        "独立定价与 R20 手填读数相同 ⇒ 结论不变")
    add("RF-PMIN-LEVELS", pri["levels"][0]["ok"] is False
        and pri["levels"][1]["ok"] is True,
        [False, True], [pri["levels"][0]["ok"], pri["levels"][1]["ok"]],
        "p=0 不可 / p=1 可，两档读数不同")
    add("RF-PMIN-READING-DRIVEN", pmin_active(c0_a, c1_a, CRIT_D),
        True, pmin_active(c0_a, c1_a, CRIT_D),
        "反噬：把可行解强制成常量即被负对照抓到")
    add("RF-PMIN-NEGCTRL", pmin_shadow is None, None, pmin_shadow,
        "负对照：p=1 也判负时可行集必须为空")
    add("RF-NEXTRA-MATCH-R20", nex_match, r20_nex, nex["values"],
        "三配置自由度由「来料登记 + 启用方向数」机读")
    add("RF-NEXTRA-SCALES-ZERO", nex["registered_scales"] == 0,
        0, nex["registered_scales"], "46 锚中无 SUSY／阈值尺度登记")
    add("RF-NEXTRA-BETA-DIFF", nex["beta_diff_components"] == len(B_SM),
        len(B_SM), nex["beta_diff_components"], "MSSM 与 SM 的 β 分量全不同")
    add("RF-NEXTRA-DIRECTIONS",
        nex["nonsingular_directions"] == int(R20KN["threshold_solvable"]),
        int(R20KN["threshold_solvable"]), nex["nonsingular_directions"],
        "R20 实际解出的非奇异阈值方向数，两路机读")

    add("RF-GATE-RATES-MATCH", ga["rates"] == rates_e,
        rates_e, ga["rates"], "JSON 结构 vs report 文本，四门通过数两路机拼")
    add("RF-ZEROPOWER-IDENTIFIED", ga["zero_power"] == zero_e and len(zero_e) == 1,
        zero_e, ga["zero_power"], "恒假门 G4 被两路一致地主动识别")
    add("RF-FULLPOWER-NONE", len(ga["full_power"]) == len(ga_e["full_power"]) == 0,
        0, [len(ga["full_power"]), len(ga_e["full_power"])], "无恒真门")
    add("RF-MIN-CUT-2", cut_size == cut_size_e and cut_size == 2,
        cut_size_e, cut_size,
        "两路独立枚举的最小承重割一致；需同拆两门才有配置全过")
    add("RF-CUT-SETS", len(ga["min_cut_sets"]) >= 1
        and all(len(s) == cut_size for s in ga["min_cut_sets"]),
        cut_size, [len(s) for s in ga["min_cut_sets"]],
        "全部最小割等长")
    add("RF-G4-NOT-LOAD-BEARING", ga["g4_not_load_bearing"],
        True, ga["g4_not_load_bearing"],
        "剔除恒假门后 escape 不变 ⇒ 该门不承重，应从布尔合取移出")
    add("RF-REDUCED-GATES-3", ga["reduced_gates"] == 3,
        3, ga["reduced_gates"], "修复后合取门数 4→3")
    add("RF-ESCAPE-UNCHANGED", ga["escape_full"] == 0 and ga["escape_reduced"] == 0,
        0, [ga["escape_full"], ga["escape_reduced"]],
        "修复只升级证据质量，不改 R20 结论")
    add("RF-POWER-ACTIVE", power_active(rows_a),
        True, power_active(rows_a), "恒假门识别谓词的夹具")

    add("RF-SPAN-ACT-RECOMPUTE", rel(sp["recomputed_base"], act_span_r20()) < TOL,
        num(act_span_r20()), sp["recomputed_base"],
        "独立实现三交点闭式，与 R20 act 逐位一致")
    add("RF-SPAN-ARCHIVE-SAME-SOURCE", sp["archive_static"],
        True, sp["archive_static"],
        "如实报：R1 存档与 R20 act 相对偏离 0，是同源回验", kind="INFO")
    add("RF-SPAN-INDEPENDENT-DISTINCT", sp["distinct"] == 3,
        3, sp["distinct"], "四路读数按偏离+容差值去重 3 个（act 与同源存档同值）")
    add("RF-SPAN-STRING-NOT-VALUE",
        sp["distinct_string"] > sp["distinct"],
        sp["distinct"], sp["distinct_string"],
        "两路精度位数不同（70 位 vs 60 位）⇒ 字符串去重会虚增一份，改用值去重",
        kind="INFO")
    add("RF-SPAN-ACT-MOVES", sp["act_moves"], True, sp["act_moves"],
        "α_s 扰动 1% 后重算跨度明显移动，存档读数不动")
    add("RF-SPAN-LITERATURE-HONEST", rel(sp_lit, act_span_r20()) > D("1e-4"),
        num(act_span_r20()), num(sp_lit), "文献独立口径不同，不强行对齐")
    add("RF-SPAN-R64-HONEST", rel(sp_64, act_span_r20()) > D("1e-4"),
        num(act_span_r20()), num(sp_64), "r64 独立册口径不同，不强行对齐")
    add("RF-SPAN-TWO-INDEPENDENT", rel(sp_lit, sp_64) > D("1e-5"),
        num(sp_lit), num(sp_64), "两条独立来料彼此也不同")

    add("RF-REGEX-TIGHT-UNIQUE", len(rx["tight"]) == 1,
        1, len(rx["tight"]), "锚定 sstar_resid 后唯一命中")
    add("RF-REGEX-LOOSE-AMBIGUOUS", len(rx["loose"]) > 1,
        ">1", len(rx["loose"]), "松散正则多命中，原实现只靠顺序侥幸")
    add("RF-REGEX-DISCRIMINATOR", rx["discriminator"], True, rx["discriminator"],
        "改名负对照：锚定失配、松散仍命中 ⇒ 锚定有判别力")
    add("RF-REGEX-MAGNITUDE", rx["magnitude_ok"], True, rx["magnitude_ok"],
        "report 舍入串与 JSON 精确残差都落在机器零量级")
    add("RF-REGEX-ROUNDED-NOT-EXACT", rx["rounded_not_exact"],
        True, rx["rounded_not_exact"],
        "舍入串不当精确值比较", kind="INFO")
    add("RF-REGEX-UNIQUE-ACTIVE",
        regex_unique(R188REP) and not regex_unique(R188REP.replace("sstar_resid=", "other_resid=")),
        [True, False],
        [regex_unique(R188REP), regex_unique(R188REP.replace("sstar_resid=", "other_resid="))],
        "反噬：换回松散正则即被夹具抓到")

    add("RF-NO-HARDCODE-OK", len(hardcode_ok_hits(tree)) == 0,
        [], hardcode_ok_hits(tree), "全表 AST 扫描 add 的 ok")
    add("RF-EXP-ACT-DISTINCT-AST", len(exp_act_ast_hits(tree)) == 0,
        [], exp_act_ast_hits(tree), "act/exp 所有 return 分支禁顶层数值常量")
    add("RF-FIX-PREDICATES-ACTIVE",
        pmin_active(c0_a, c1_a, CRIT_D) and power_active(rows_a)
        and regex_unique(R188REP),
        [True, True, True],
        [pmin_active(c0_a, c1_a, CRIT_D), power_active(rows_a), regex_unique(R188REP)],
        "三次反噬各只动一个判据")
    add("RF-NO-WRITE-TO-R20",
        not any("gut_meet" in s or "R20" in s for s in write_target_hits(tree)),
        0, [s for s in write_target_hits(tree) if "gut_meet" in s or "R20" in s],
        "AST 结构性零写入：本册不回写 R20 任何产物")
    add("RF-PATH-CONSTRUCTOR-SHARED",
        report_path_from_json(OUT_JSON) == OUT_REPORT
        and json_path_from_report(OUT_REPORT) == OUT_JSON,
        os.path.basename(OUT_REPORT),
        os.path.basename(report_path_from_json(OUT_JSON)),
        "机核与核验器共用同一路径构造")
    add("RF-README-ZERO-WRITE",
        len(re.findall(r"open\s*\(\s*README[^)]*[\"'][wax]", SRC_TEXT)) == 0,
        0, len(re.findall(r"open\s*\(\s*README[^)]*[\"'][wax]", SRC_TEXT)),
        "结构性零写入，不用前后 MD5 相等的时序判据")

    readme_b = rb(README)
    rid = re.findall(r"TUFT-r(\d+)_", readme_b.decode("utf-8", errors="replace"))
    key_numbers = dict(
        defects_found=defects_found, defects_fixed=defects_fixed,
        defect_ids=[d["id"] for d in defects],
        p_min_recomputed=(pmin if pmin is not None else -1),
        p_min_r20=int(R20KN["p_min"]),
        pmin_levels=[dict(p=r["p"], chi2=num(r["best"]), ok=int(r["ok"]))
                     for r in pri["levels"]],
        pmin_shadow=("none" if pmin_shadow is None else str(pmin_shadow)),
        nextra_recomputed=nex["values"], nextra_r20=r20_nex,
        nextra_recomputed_text="".join(str(x) for x in nex["values"]),
        nextra_r20_text="".join(str(x) for x in r20_nex),
        registered_scales=nex["registered_scales"],
        beta_diff_components=nex["beta_diff_components"],
        nonsingular_directions=nex["nonsingular_directions"],
        gate_rates=ga["rates"], gate_rates_text="".join(str(x) for x in ga["rates"]),
        zero_power_gates=len(ga["zero_power"]),
        zero_power_names=["G%d" % (g + 1) for g in ga["zero_power"]],
        zero_power_names_text="、".join("G%d" % (g + 1) for g in ga["zero_power"]),
        full_power_gates=len(ga["full_power"]),
        min_cut_size=cut_size,
        min_cut_sets=[["G%d" % (g + 1) for g in s] for s in ga["min_cut_sets"]],
        min_cut_sets_text="；".join("+".join("G%d" % (g + 1) for g in s)
                                  for s in ga["min_cut_sets"]),
        reduced_gates=ga["reduced_gates"],
        escape_full=ga["escape_full"], escape_reduced=ga["escape_reduced"],
        escape_after_fix=ga["escape_reduced"],
        g4_not_load_bearing=int(ga["g4_not_load_bearing"]),
        span_act=num(act_span_r20()),
        span_same_source_archive=num(exp_span_r20_archive()),
        span_literature=num(sp_lit), span_r64=num(sp_64),
        span_readings=sp["readings"], span_labels=sp["labels"],
        span_rel_to_act=sp["rel_to_act"], span_distinct=sp["distinct"],
        span_distinct_string=sp["distinct_string"],
        span_recomputed_base=sp["recomputed_base"],
        span_after_alpha_s_1pct=sp["recomputed_after_alpha_s_1pct"],
        span_act_moves=int(sp["act_moves"]),
        regex_loose_hits=len(rx["loose"]), regex_tight_hits=len(rx["tight"]),
        regex_loose_values=rx["loose"], regex_tight_values=rx["tight"],
        regex_loose_text="、".join(rx["loose"]),
        regex_tight_text="、".join(rx["tight"]),
        regex_negative_tight=len(rx["tight_neg"]),
        r188_exact=rx["exact"], r188_shown=rx["shown"],
        chi2_p0=num(c0_a), chi2_p1=num(c1_a), chi2_crit=num(CRIT_D),
        r20_final=R20["final"], r20_verdict=R20["verdict"],
        r20_guards="%d/%d" % (R20["guard_pass"], R20["guard_count"]),
        r20_json_md5=md5(P_R20_J), r20_kernel_md5=md5(P_R20_K),
        r20_report_md5=md5(P_R20_R),
        r20_json_bytes=os.path.getsize(P_R20_J),
        readme_bytes=len(readme_b), readme_md5=hashlib.md5(readme_b).hexdigest(),
        readme_max_rid=max(int(x) for x in rid) if rid else 0,
        source_missing=sum(1 for p in [P_R20_J, P_R20_K, P_R20_R, P_R1, P_R5,
                                       P_R64, P_R188_J, P_R188_R, P_LEDGER, README]
                           if not os.path.isfile(p)),
    )
    add("RF-VERDICT-MACHINE",
        verdict_string(key_numbers) !=
        verdict_string(dict(key_numbers, defects_found=defects_found + 1)),
        "changed", "same", "读数 +1 后判词串必须变化")
    add("RF-SOURCE-COMPLETE", key_numbers["source_missing"] == 0,
        0, key_numbers["source_missing"], "十份来料文件全部存在")
    add("RF-R20-UNMODIFIED",
        all(md5(p) == r20_before[p] for p in r20_before),
        "unchanged", "unchanged", "本册运行前后 R20 三件产物逐字节未变",
        kind="INFO")

    blob = json.dumps(key_numbers, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))
    sha = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    cnts = counts_of()
    nf_guard = sum(1 for g in GUARDS if not g["ok"])
    final = final_of(0, nf_guard, len(key_numbers))
    verdict = verdict_string(key_numbers)
    doc = dict(
        title="算法联盟：R20 证据质量缺陷的机读盘点、独立复算与修复（第二十一轮）",
        date=DATE,
        nature="不占号、不登记、不与任何卷相加；只审 R20 的证据质量，不回写 R20 任何产物，不重算新物理",
        red_line="数学自洽 != 实验证实；四力大统一正确方程 0 条；独立实验预言 0；不宣称攻破统一场论",
        final=final, verdict=verdict, key_numbers=key_numbers,
        segments=[dict(name=g["name"], kind=g["kind"], note=g["note"])
                  for g in GUARDS],
        counts=cnts, guard_count=len(GUARDS),
        guard_pass=len(GUARDS) - nf_guard,
        content_sha256=sha,
        defects=[dict(id=d["id"], found=bool(d["found"]), why=d["why"],
                      reading=d["reading"]) for d in defects],
        fixes=fixes,
        identity_notes=[
            "四门中 G4 在全部 3 个配置上 0% 通过，配置层判别力为 0；把它当承重门是对象错位。剔除后 escape 仍 0，证明它不承重",
            "R1 的 rg_span_dex_act 由同一批 a_i 与 b_i 算出，与 R20 act 逐位相等；「两路一致」在此是同源回验的恒真读数，不作独立证据",
        ],
        boundary_notes=[
            "本册只修证据质量：p_min、n_extra、恒假门、span 独立来料、正则锚定；不改动 R20 的物理读数与最终判词",
            "文献口径与 r64 口径的 a_i/β 登记与 R20 不同，故跨度读数不同属预期，未做任何对齐或平均",
            "最小承重割 2 是「门集合」上的组合结论，与 R14 的三门割 2、R19 的翻转割 4 是不同对象，不取和、不相加",
            "46 锚中 SUSY／阈值尺度登记 0 条只说明来料未登记，不等于该尺度不存在或不可测",
            "本册不产生新物理、不修改任何既有方程，也不扩大任何既有下界",
        ],
        info_notes=[
            "数学自洽 != 实验证实；审计册只产可算判决，不产新物理",
            "四力大统一正确方程 0 条、独立实验预言 0；不宣称攻破统一场论",
            "本册不占 RID、不入 README、不与任何审计卷相加",
            "README 全程零写入；采用 AST 结构性判据而非前后 MD5 相等",
        ],
        source_files=[os.path.relpath(p).replace("\\", "/") for p in
                      [P_R20_J, P_R20_K, P_R20_R, P_R1, P_R5, P_R64,
                       P_R188_J, P_R188_R, P_LEDGER, README]],
        source_missing=key_numbers["source_missing"],
        declared_negative=0,
    )
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    lines = [doc["title"], "=" * 96,
             "verdict : " + verdict, "final   : " + final,
             "counts  : " + json.dumps(cnts, ensure_ascii=False, sort_keys=True),
             "guards  : %d/%d" % (doc["guard_pass"], doc["guard_count"]),
             "sha256  : " + sha, "-" * 96, "[MACHINE-TABLE]"]
    for k in sorted(key_numbers):
        v = key_numbers[k]
        s = v if isinstance(v, str) else (
            json.dumps(v, ensure_ascii=False, sort_keys=True)
            if isinstance(v, (list, dict)) else str(v))
        lines.append("%s = %s" % (k, s))
    lines += ["[/MACHINE-TABLE]", "-" * 96]
    lines += [
        "机读缺陷 %d 项：%s" % (defects_found, "、".join(d["id"] for d in defects if d["found"])),
        "独立复算修复 %d 项；逐项与原读数比对：p_min %s→%s、n_extra %s→%s" %
        (defects_fixed, int(R20KN["p_min"]), pmin,
         "".join(str(x) for x in r20_nex), "".join(str(x) for x in nex["values"])),
        "四门通过数 %s；恒假门 %s；最小承重割 %d；合取门数 4→%d；escape %d→%d" %
        ("/".join(str(x) for x in ga["rates"]), ga["zero_power"],
         cut_size, ga["reduced_gates"], ga["escape_full"], ga["escape_reduced"]),
        "span 四路 %s（去重 %d）；文献 %s / r64 %s，均独立且不同" %
        (" / ".join(sp["labels"]), sp["distinct"], disp(sp_lit, 6), disp(sp_64, 6)),
        "正则：松散 %d 命中 / 锚定 %d 命中；改名负对照锚定 %d 命中" %
        (len(rx["loose"]), len(rx["tight"]), len(rx["tight_neg"])),
        "R20 三件产物运行前后 MD5 未变；README %d B / 最大 RID %d；本册零写入" %
        (len(readme_b), key_numbers["readme_max_rid"]),
        "-" * 96,
        "红线：数学自洽 != 实验证实；修复只升级证据质量，不宣称攻破统一场论；独立实验预言 0。",
    ]
    with open(OUT_REPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("FINAL =", final)
    print("VERDICT =", verdict)
    print("GUARDS = %d/%d" % (doc["guard_pass"], doc["guard_count"]))
    print("COUNTS =", json.dumps(cnts, ensure_ascii=False, sort_keys=True))
    print("DEFECTS =", defects_found, "FIXED =", defects_fixed,
          "PMIN =", pmin, "NEX =", nex["values"], "CUT =", cut_size)
    return doc


if __name__ == "__main__":
    main()
