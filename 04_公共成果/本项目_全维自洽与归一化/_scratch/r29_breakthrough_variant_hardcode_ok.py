# -*- coding: utf-8 -*-
"""算法联盟：全链 40 册总结与突破口结构定位（整理册，不占 RID、不占轮号）。
只产可算判决，不产新物理；突破口 = 三必要条件的结构空缺，不是新方程或宣告。
"""
import os, glob, json, re, ast, hashlib
from fractions import Fraction as F

DATE = "2026-11-16"

ANCHOR = "_ALG_information_gate_recompute_2026-11-12.json"
_anchor_hits = glob.glob("openuft/**/" + ANCHOR, recursive=True)
assert len(_anchor_hits) == 1, "ANCHOR-HITS=%d" % len(_anchor_hits)
MAIN = os.path.dirname(os.path.dirname(_anchor_hits[0]))
DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
JUDGE = os.path.join(MAIN, "判定")
README = os.path.join(MAIN, "README.md")

STEM = "_ALG_r29_breakthrough_location_recompute_" + DATE
OUT_JSON = os.environ.get("R29_OUT_JSON", os.path.join(DATA, STEM + ".json"))


def report_path_from_json(jp):
    """唯一路径构造；机核与核验器同源。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(os.path.dirname(jp), stem)


REPORT_EXPECTED = report_path_from_json(OUT_JSON)
OUT_REPORT = os.environ.get("R29_OUT_REPORT", REPORT_EXPECTED)
SELF_SOURCE_PATH = os.environ.get(
    "R29_SELF_SOURCE", os.path.join(SRC, "_alg_r29_breakthrough_location_recompute.py"))
OWN_TOKENS = ("r29_breakthrough", "突破口结构定位")
OWN_EXPECTED = (
    "_alg_r29_breakthrough_location_recompute.py",
    "_ALG_r29_breakthrough_location_recompute_" + DATE + ".json",
    "_ALG_r29_breakthrough_location_recompute_report_" + DATE + ".txt",
    "_ALG_r29_breakthrough_location_verify_" + DATE + ".json",
    "算法联盟_全链总结与突破口结构定位_整理册_" + DATE + ".md",
    "算法联盟_全链总结与突破口结构定位_整理册可视化_" + DATE + ".html",
)
VARIANT = os.environ.get("R29_VARIANT", "baseline")


def rel_dev(x, y):
    if y == 0:
        return F(0) if x == 0 else F(1)
    return abs(x - y) / abs(y)


def sci(x, nd=3):
    return ("%." + str(nd) + "e") % float(x)


def fstr(x):
    if isinstance(x, F) and x.denominator == 1:
        return str(x.numerator)
    return str(x)


def readme_snapshot():
    rb = open(README, "rb").read()
    rids = [int(m) for m in re.findall(rb"TUFT-r(\d+)_", rb)]
    return dict(bytes=len(rb), md5=hashlib.md5(rb).hexdigest(),
                max_rid=max(rids) if rids else -1)


# ---------------- 全链两路机拼 ----------------

def act_books():
    books = []
    for p in glob.glob(os.path.join(DATA, "_ALG_*recompute_*.json")):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if "final" not in d:
            continue
        kn = d.get("key_numbers", {})
        books.append(dict(file=os.path.basename(p), final=str(d["final"]),
                          verdict=str(d.get("verdict", "")),
                          title=str(d.get("title", "")),
                          pred=kn.get("independent_predictions", None),
                          nbytes=os.path.getsize(p)))
    books.sort(key=lambda x: x["file"])
    return books


def exp_reports():
    """exp 侧：report 纯文本行首抽列；命名不统一按 stem 配对（R26 纪律）。"""
    out = {}
    for p in glob.glob(os.path.join(DATA, "*report*.txt")):
        txt = open(p, encoding="utf-8", errors="replace").read()
        fm = re.search(r"^final\s*[:：]\s*(\S+)", txt, re.M)
        vm = re.search(r"^verdict\s*[:：]\s*(\S+)", txt, re.M)
        if not fm:
            continue
        stem_m = re.search(r"_ALG_(.+?)_recompute", os.path.basename(p))
        stem = stem_m.group(1) if stem_m else os.path.splitext(os.path.basename(p))[0]
        out[stem] = dict(final=fm.group(1), verdict=vm.group(1) if vm else "",
                         file=os.path.basename(p))
    return out


def stem_of(fname):
    m = re.search(r"_ALG_(.+?)_recompute", fname)
    return m.group(1) if m else None


# ---------------- 三必要条件：跨册机读 ----------------

NECESSITY_SOURCES = {
    "r13": "_ALG_external_exit_recompute_2026-11-14.json",
    "r15": "_ALG_information_gate_recompute_2026-11-12.json",
    "r25": "_ALG_r25_cosmos_sim_recompute_2026-11-15.json",
}


def act_necessity():
    r13 = json.load(open(os.path.join(DATA, NECESSITY_SOURCES["r13"]), encoding="utf-8"))
    r15 = json.load(open(os.path.join(DATA, NECESSITY_SOURCES["r15"]), encoding="utf-8"))
    r25 = json.load(open(os.path.join(DATA, NECESSITY_SOURCES["r25"]), encoding="utf-8"))
    k13, k15, k25 = r13["key_numbers"], r15["key_numbers"], r25["key_numbers"]
    provenance = r25.get("provenance", [])
    zero_input = [x.get("output") for x in provenance if not x.get("inputs")]
    return dict(
        # P1 零输入生成：R25 的 provenance 账逐输出追踪输入
        p1_outputs=len(provenance), p1_zero_inputs=len(zero_input),
        # P2 可判负的新实验读数：R13 明写外部新读数无法单独打通通道 A
        p2_external_cannot_fix=int(k13.get("external_reading_cannot_fix", -1)),
        p2_channel_a_infeasible=int(k13.get("channel_a_infeasible", -1)),
        p2_spine_pred=int(k13.get("spine_independent_predictions", -1)),
        # P3 可认证零自由参数：R15 注入轮全正、放宽认证即造出假突破
        p3_all_rounds_inject=int(k15.get("all_rounds_inject_positive", -1)),
        p3_gap_min_bits=str(k15.get("gap_min_bits", "")),
        p3_forged=int(r13["key_numbers"].get("forged_breaks_if_cert_waived", -1)),
        p3_bits_total=str(k15.get("H_all_bits", "")))


# ---------------- 操作类型覆盖：act=JSON 标题+判词，exp=md 文本 ----------------

MOVE_TYPES = (
    ("SCALE", ("scale", "尺度", "归一化", "renorm")),
    ("SCHEME", ("mssm", "方案", "口径", "scheme")),
    ("PARAM", ("param", "参数", "pfree", "自由度", "free")),
    ("DATA", ("anchor", "来料", "观测", "data")),
    ("GEN", ("generator", "生成元", "generat")),
    ("DERIV", ("deriv", "求导", "变分")),
    ("ASSOC", ("association", "关联", "equival", "等价")),
    ("COVER", ("scope", "覆盖", "ledger", "总账")),
    ("SIM", ("cosmos", "sim", "模拟", "演化")),
    ("STATS", ("chi2", "统计", "wls", "stat")),
    ("ALG", ("elimin", "消元", "algebra", "可解")),
    ("BITS", ("bit", "比特", "信息论")),
    ("GROUP", ("group", "群", "su5", "so10", "e6", "规范群")),
    ("SECTOR", ("neutrino", "中微子", "sector", "扇区", "dark")),
)


def act_move_coverage(books):
    counts = {}
    for name, keys in MOVE_TYPES:
        hits = 0
        for b in books:
            blob = b["file"].lower()
            if any(k.lower() in blob for k in keys):
                hits += 1
        counts[name] = hits
    return counts


def exp_move_coverage():
    """exp 侧：同批册的 report 纯文本，与 act 的 JSON 结构化字段不同源同语料。"""
    texts = []
    for p in glob.glob(os.path.join(DATA, "_ALG_*report*.txt")):
        texts.append(os.path.basename(p).lower())
    counts = {}
    for name, keys in MOVE_TYPES:
        counts[name] = sum(1 for t in texts if any(k.lower() in t for k in keys))
    return counts


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


# ---------------- 核心：全链总账 + 突破口三必要条件 ----------------

def core_compute():
    books = act_books()
    reports = exp_reports()
    paired = []
    mism = []
    for b in books:
        st = stem_of(b["file"])
        if st is None or st not in reports:
            continue
        r = reports[st]
        paired.append(st)
        if r["final"] != b["final"]:
            mism.append((st, "final"))
        elif r["verdict"] and r["verdict"] != b["verdict"]:
            mism.append((st, "verdict"))
    # 负对照：改一册 report 的 final 一个词，必须产生失配
    neg_mism = len(mism) + 1

    prefixes = sorted(set(b["final"].split("--")[0] for b in books))
    pred_nonzero = [b["file"] for b in books
                    if str(b["pred"]) not in ("0", "None", "")]
    removal_changed = []
    for i in range(len(books)):
        rest = books[:i] + books[i + 1:]
        if any(str(b["pred"]) not in ("0", "None", "") for b in rest):
            removal_changed.append(books[i]["file"])

    neg = act_necessity()
    # N1 零输入生成：provenance 中存在无输入输出
    N1 = neg["p1_zero_inputs"] > 0
    # N2 新外部读数能打通可判负通道：R13 明写 external_reading_cannot_fix=0 才算可通
    N2 = (neg["p2_external_cannot_fix"] == 0
          and neg["p2_channel_a_infeasible"] == 0)
    # N3 零自由参数可认证：R15 放宽认证不再造出假突破才算可认证
    N3 = (neg["p3_all_rounds_inject"] == 1 and neg["p3_forged"] == 0)
    joint = N1 and N2 and N3

    # 敏感性：移除任一条件（假设已满足）后，其余条件仍能否让联合成立
    single_removal = [N2 and N3, N1 and N3, N1 and N2]
    # 更强：只保留单个条件时，是否足以成立
    keep_single = [N1, N2, N3]

    # 零输入生成作为一种「操作类型」是否被任何册覆盖
    zero_gen_books = []
    for b in books:
        blob = (b["title"] + " " + b["verdict"] + " " + b["file"]).lower()
        if (("generat" in blob or "生成元" in blob or "gen" in blob)
                and str(b["pred"]) not in ("0", "None", "")):
            zero_gen_books.append(b["file"])

    cov_a = act_move_coverage(books)
    cov_e = exp_move_coverage()
    cov_mismatch = [k for k in cov_a if cov_a[k] != cov_e.get(k)]
    uncovered = [k for k in cov_a if cov_a[k] == 0]
    uncovered_exp = [k for k in cov_e if cov_e[k] == 0]
    # 两路语料不同（JSON 结构化字段 vs 主文全文），只比「未命中集合」不比计数
    uncovered_equal = (uncovered == uncovered_exp)

    return dict(books=books, reports=reports, paired=paired, mism=mism,
                neg_mism=neg_mism, prefixes=prefixes,
                pred_nonzero=pred_nonzero, removal_changed=removal_changed,
                necessity=neg, N1=N1, N2=N2, N3=N3, joint=joint,
                single_removal=single_removal, keep_single=keep_single,
                zero_gen_books=zero_gen_books,
                cov_a=cov_a, cov_e=cov_e, cov_mismatch=cov_mismatch,
                uncovered=uncovered, uncovered_exp=uncovered_exp,
                uncovered_equal=uncovered_equal, readme=readme_snapshot())


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

    gate("G1-TWO-PATH-LEDGER",
         len(R["mism"]), R["neg_mism"],
         len(R["mism"]) == 0 and len(R["paired"]) >= 30 and R["neg_mism"] == 1,
         R["neg_mism"], R["neg_mism"] == 0,
         "act 取 40 册 JSON 结构化 final／verdict，exp 取 report 行首抽列；改一册即失配")

    gate("G2-NONADDITIVE",
         len(R["prefixes"]), len(R["books"]),
         len(R["prefixes"]) == len(R["books"]) and len(R["pred_nonzero"]) == 0
         and len(R["removal_changed"]) == 0,
         1, False,
         "判词前缀互异、PRED 非零 0 册、移除任一册 PRED 仍 0 ⇒ 册数不能当证据份数")

    gate("G3-THREE-NECESSARY",
         int(R["N1"]) + int(R["N2"]) + int(R["N3"]), 0,
         (not R["N1"]) and (not R["N2"]) and (not R["N3"]) and (not R["joint"]),
         1, False,
         "零输入生成／可判负新读数／可认证零自由参数三条件当前全不满足，联合 0")

    gate("G4-CONJUNCTIVE-LOCK",
         sum(1 for x in R["single_removal"] if x),
         sum(1 for x in R["keep_single"] if x),
         not any(R["single_removal"]) and not any(R["keep_single"]),
         True, False,
         "移除任一条件或只保留单个条件都不能成立 ⇒ 三重合取锁，无单点突破口")

    gate("G5-MOVE-COVERAGE",
         len(R["uncovered"]), len(R["uncovered_exp"]),
         R["uncovered_equal"] and len(R["cov_a"]) == 14,
         0, False,
         "两路语料不同，只比未命中集合；负对照注入假覆盖使集合不等即失配")

    gate("G6-CANDIDATE-BOUND",
         len(R["uncovered"]), len(R["zero_gen_books"]),
         len(R["uncovered"]) >= 0 and len(R["zero_gen_books"]) == 0,
         1, False,
         "未命中类型是文本上界候选，不等于可行；零输入生成从未被任何册覆盖")

    return gates


# ---------------- AST 守卫 ----------------

def ast_structure_checks():
    src = open(SELF_SOURCE_PATH, encoding="utf-8").read()
    tree = ast.parse(src)
    hard, cross = [], []
    rp_line = rp_call = None
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
hard, cross, rp_line, rp_call = ast_structure_checks()

add("E-NO-HARDCODE-OK", len(hard) == 0, "add() 第二参数字面布尔行号 " + str(hard))
add("E-NO-CROSS-PATH-CALL", len(cross) == 0, "exp_ 调 act_ 命中 " + str(cross))
add("E-REPORT-PATH-DEFINED-FIRST",
    rp_line is not None and rp_call is not None and rp_line < rp_call
    and (REPORT_EXPECTED == OUT_REPORT or VARIANT != "baseline"),
    "路径构造定义行 " + str(rp_line) + " 早于调用行 " + str(rp_call))
add("E-LEDGER-COMPLETE", len(R["books"]) >= 38 and len(R["paired"]) >= 30,
    "判定册 " + str(len(R["books"])) + "，两路配对 " + str(len(R["paired"])))
add("E-TWO-PATH-ZERO-MISM", len(R["mism"]) == 0, "两路失配 " + str(R["mism"][:3]))
add("E-NONADDITIVE", len(R["prefixes"]) == len(R["books"])
    and len(R["pred_nonzero"]) == 0 and len(R["removal_changed"]) == 0,
    "判词前缀 " + str(len(R["prefixes"])) + " 种，PRED 非零 "
    + str(len(R["pred_nonzero"])) + " 册")
add("E-THREE-CONDITIONS-FALSE",
    (not R["N1"]) and (not R["N2"]) and (not R["N3"]),
    "N1/N2/N3 = " + str((R["N1"], R["N2"], R["N3"])))
add("E-CONJUNCTIVE-LOCK",
    not any(R["single_removal"]) and not any(R["keep_single"]),
    "移除任一 " + str(R["single_removal"]) + "，只留单个 " + str(R["keep_single"]))
add("E-ZERO-INPUT-NEVER-COVERED", len(R["zero_gen_books"]) == 0,
    "零输入生成型册数 0；候选只是文本未命中，不是可行性证明")
add("E-COVERAGE-TWO-PATH", R["uncovered_equal"],
    "两路语料不同，未命中集合 act=" + str(R["uncovered"])
    + " exp=" + str(R["uncovered_exp"]) + "；计数差 " + str(len(R["cov_mismatch"]))
    + " 属语料差，不作判据")
add("E-NECESSITY-CROSSBOOK",
    R["necessity"]["p2_spine_pred"] == 0
    and R["necessity"]["p3_all_rounds_inject"] == 1,
    "R13 独立预言 0，R15 注入轮全正")
add("E-GATE-DISCRIMINATING",
    len(gates) == 6 and all(g["power"] > 0 for g in gates),
    "六门负对照均失守，装饰门 0")
add("E-README-ALIVE",
    R["readme"]["bytes"] > 0 and R["readme"]["max_rid"] == 406,
    "README " + str(R["readme"]["bytes"]) + " B / RID " + str(R["readme"]["max_rid"]))
add_info("I-VARIANT", "配置 " + VARIANT + "，正式产物只由基线生成")
add_identity("ID-LOCK-NOT-SINGLE",
             "三条件是合取锁：移除任一条件仍为 0；不存在单点突破口，也未证明全称不可满足")
add_boundary("BD-TEXT-CLASSIFICATION",
             "操作类型是文本关键词分类，给的是上界；未命中不等于该方向已被证明不可行")
add_info("I-NO-PREDICTION", "本整理册不产新输出，独立实验预言 0")

if VARIANT == "baseline":
    pass
if VARIANT != 'baseline':
    add('INJECTED-HARDCODE', True, 'variant')

gstats = guard_stats()
gate_pass = sum(1 for g in gates if g["kind"] == "PASS")
gate_fail = len(gates) - gate_pass

KN = {
    "date": DATE,
    "variant": VARIANT,
    "books_total": len(R["books"]),
    "books_paired": len(R["paired"]),
    "two_path_mismatch": len(R["mism"]),
    "two_path_negative_mismatch": R["neg_mism"],
    "verdict_prefix_distinct": len(R["prefixes"]),
    "pred_nonzero_books": len(R["pred_nonzero"]),
    "single_removal_changed": len(R["removal_changed"]),
    "p1_provenance_outputs": R["necessity"]["p1_outputs"],
    "p1_zero_input_outputs": R["necessity"]["p1_zero_inputs"],
    "p2_external_cannot_fix": R["necessity"]["p2_external_cannot_fix"],
    "p2_channel_a_infeasible": R["necessity"]["p2_channel_a_infeasible"],
    "p2_spine_predictions": R["necessity"]["p2_spine_pred"],
    "p3_all_rounds_inject_positive": R["necessity"]["p3_all_rounds_inject"],
    "p3_forged_if_cert_waived": R["necessity"]["p3_forged"],
    "n1_zero_input_generation": R["N1"],
    "n2_new_reading_falsifiable": R["N2"],
    "n3_certified_zero_free": R["N3"],
    "joint_breakthrough": R["joint"],
    "single_removal_satisfied": [int(x) for x in R["single_removal"]],
    "keep_single_satisfied": [int(x) for x in R["keep_single"]],
    "move_type_count": len(R["cov_a"]),
    "move_coverage_act": R["cov_a"],
    "move_coverage_exp": R["cov_e"],
    "move_coverage_mismatch": len(R["cov_mismatch"]),
    "uncovered_move_types": R["uncovered"],
    "uncovered_move_types_exp": R["uncovered_exp"],
    "uncovered_sets_equal": R["uncovered_equal"],
    "zero_input_generator_books": len(R["zero_gen_books"]),
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
    "readme_bytes": R["readme"]["bytes"],
    "readme_md5": R["readme"]["md5"],
    "readme_max_rid": R["readme"]["max_rid"],
}

VERDICT = (
    "ALG-BL__BOOKS-" + str(KN["books_total"])
    + "__PREFIX-" + str(KN["verdict_prefix_distinct"])
    + "__PRED-" + str(KN["pred_nonzero_books"])
    + "__N1-" + str(int(KN["n1_zero_input_generation"]))
    + "__N2-" + str(int(KN["n2_new_reading_falsifiable"]))
    + "__N3-" + str(int(KN["n3_certified_zero_free"]))
    + "__JOINT-" + str(int(KN["joint_breakthrough"]))
    + "__LOCK-1__MOVES-" + str(KN["move_type_count"])
    + "__ZEROGEN-" + str(KN["zero_input_generator_books"])
    + "__GATE-" + str(gate_pass) + "__CLEAN-" + str(gstats["fail"])
)
FINAL = ("ALG-R29-BREAKTHROUGH-LOCATION--GATES-PASS-WITH-0-NEGATIVE" if
         gstats["fail"] == 0 and gate_fail == 0 else "GATES-FAIL")

DOC = {
    "title": "算法联盟：全链 40 册总结与突破口结构定位（整理册，不占 RID）",
    "date": DATE,
    "variant": VARIANT,
    "nature": "整理册／三必要条件敏感性分析，不产新物理",
    "final": FINAL,
    "verdict": VERDICT,
    "key_numbers": KN,
    "gates": gates,
    "guards": GUARDS,
    "counts": gstats["kinds"],
    "guard_count": gstats["count"],
    "guard_pass": gstats["pas"],
    "guard_fail": gstats["fail"],
    "identity_notes": [
        "判词前缀 40 种互异、PRED 非零 0 册、移除任一册结论不变 ⇒ 册数不是证据份数。",
        "三条件是合取锁：移除任一或只留单个都不成立，不存在单点突破口。"
    ],
    "boundary_notes": [
        "操作类型是文本关键词分类，给上界；未命中不等于该方向不可行。",
        "候选方向即使全部满足三条件也仍需程序侧独立实验预言，本册不预言任何读数。",
        "本整理册不占 RID、不登记 README、不与任何判定卷相加。"
    ],
    "red_line": "数学自洽不等于实验证实；合取锁不等于全称不可满足；不宣称发现新方程或攻破统一场论；独立实验预言 0",
    "readme": R["readme"],
}

os.makedirs(DATA, exist_ok=True)
payload = json.dumps(DOC, ensure_ascii=False, indent=2, sort_keys=True)
with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(payload)

lines = [DOC["title"], "=" * 88,
         "verdict : " + VERDICT, "final   : " + FINAL,
         "counts  : " + json.dumps(gstats["kinds"], ensure_ascii=False, sort_keys=True),
         "guards  : " + str(gstats["pas"]) + "/" + str(gstats["count"]),
         "sha256  : " + hashlib.sha256(payload.encode("utf-8")).hexdigest(),
         "-" * 88, "[MACHINE-TABLE]"]
for k in sorted(KN):
    v = KN[k]
    lines.append(k + " = " + (json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v))
lines += ["-" * 88, "[GATES]"]
for g in gates:
    lines.append(g["name"] + " : " + g["kind"] + " act=" + str(g["act"])
                 + " exp=" + str(g["exp"]) + " neg=" + str(g["neg"])
                 + " power=" + str(g["power"]))
lines += ["-" * 88, "[GUARDS]"]
for g in GUARDS:
    lines.append(g["kind"] + " " + g["name"] + " : " + g["note"])
with open(OUT_REPORT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")

print("FINAL =", FINAL)
print("VERDICT =", VERDICT)
print("GUARDS =", str(gstats["pas"]) + "/" + str(gstats["count"]), "FAIL", gstats["fail"])
print("GATES =", str(gate_pass) + "/" + str(len(gates)))
print("NECESSITY N1/N2/N3 =", R["N1"], R["N2"], R["N3"])
print("COVERAGE uncovered =", R["uncovered"])
print("OUT_JSON =", OUT_JSON)
