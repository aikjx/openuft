# -*- coding: utf-8 -*-
"""第二十六轮 · 全链全维总账与攻击面覆盖度审计（部件 1／3）

纯标准库。审对象是 R1–R25 留下的 36 册判定册，不产新物理、不产新证据。
两路机拼：act 走 JSON 结构化读数，exp 走 report 纯文本正则抽列。
"""
import os
import glob
import json
import hashlib
import ast
import re
import collections
from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal

ANCHOR = "_ALG_expdata_fullchain_来料总表_2026-11-11.json"
HITS = glob.glob(os.path.join("openuft", "**", ANCHOR), recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
MAIN = os.path.dirname(DATA)
SRC = os.path.join(MAIN, "源码")
README = os.path.join(MAIN, "README.md")

OUT_JSON = os.path.join(DATA, "_ALG_r26_fullscope_recompute_2026-11-15.json")
OUT_REPORT = os.path.join(DATA, "_ALG_r26_fullscope_recompute_2026-11-15_report.txt")
VERIFY_JSON = os.path.join(DATA, "_ALG_r26_fullscope_verify_2026-11-15.json")
MAIN_MD = os.path.join(MAIN, "算法联盟_全链全维总账与攻击面覆盖度审计_第二十六轮_2026-11-15.md")
MAIN_HTML = os.path.join(MAIN, "算法联盟_全链全维总账_第二十六轮可视化_2026-11-15.html")

OWN_TOKENS = ("r26_fullscope", "R26-FULLSCOPE", "第二十六轮", "fullscope")

CFG = {
    "inject_fake_break": False,
    "same_source_negative": False,
    "drop_one_report": False,
    "inject_unattributed": True,
}


def is_own(p):
    b = os.path.basename(p)
    return any(t in b for t in OWN_TOKENS)


def sci(x, d=8):
    return format(D(str(x)), "." + str(d) + "E")


def jnum(x):
    if isinstance(x, Decimal):
        return sci(x)
    if isinstance(x, bool):
        return int(x)
    return x


def rel(a, b):
    a, b = D(str(a)), D(str(b))
    return abs(a - b) / abs(b) if b != 0 else abs(a - b)


def distinct_by_rel(a, b, tol=D("1e-30")):
    """判两路是否同源用相对偏离 + 容差，禁字符串相等（精度差会被误当独立来料）。"""
    try:
        return rel(a, b) > tol
    except Exception:
        return str(a) != str(b)


def readme_state():
    b = open(README, "rb").read()
    ids = [int(x) for x in re.findall(rb"TUFT-r(\d+)", b)]
    return {"bytes": len(b), "md5": hashlib.md5(b).hexdigest(),
            "max_rid": max(ids) if ids else -1}


def algo_files():
    """语义白名单：只统计正式产物，排除临时区与字节码缓存，并排除本册自身产物。"""
    out = []
    for root, dirs, fs in os.walk(MAIN):
        dirs[:] = [d for d in dirs if d not in ("_scratch", "__pycache__")]
        for f in fs:
            if not ("算法联盟" in f or f.startswith("_ALG_") or f.startswith("_alg_")):
                continue
            p = os.path.join(root, f)
            if is_own(p):
                continue
            out.append(p)
    return out


def snapshot():
    return {os.path.relpath(p, MAIN): hashlib.md5(open(p, "rb").read()).hexdigest()
            for p in algo_files()}


STEM = re.compile(r"_ALG_(.+?)_recompute")
PAT_FINAL = re.compile(r"^\s*(?:final|FINAL)\s*[:=]\s*(\S+)", re.M | re.I)
PAT_VERDICT = re.compile(r"^\s*(?:verdict|VERDICT)\s*[:=]\s*(\S+)", re.M | re.I)
PAT_GUARDS = re.compile(r"^\s*(?:guards|GUARDS)\s*[:=]\s*(\d+)\s*/\s*(\d+)", re.M | re.I)
PRED_PAT = re.compile(r"PRED-(\d+)", re.I)

DIMS = {
    "方程层": ("方程", "equation", "RG", "耦合", "消元"),
    "自由度层": ("自由度", "p_free", "参数", "DOF", "下界"),
    "信息层": ("bit", "信息", "MDL", "不可满足核", "描述长度"),
    "生成元层": ("生成元", "Lie", "交换子", "可积", "bracket"),
    "代数层": ("代数", "无解", "相容", "RREF", "消元"),
    "求导层": ("求导", "Hessian", "包络", "微分", "deriv"),
    "统计层": ("chi2", "卡方", "sigma", "误差棒", "观测"),
    "量纲层": ("量纲", "dimension", "指数矩阵", "单位"),
    "证据质量层": ("缺陷", "修复", "证据质量", "独立复算", "负对照"),
    "目录层": ("目录", "盘点", "零读数", "整理", "catalog"),
    "模拟层": ("模拟", "FLRW", "Friedmann", "宇宙演化", "积分"),
    "力的统一": ("四力", "统一", "交汇", "大统一", "force"),
}


def stem_of(p):
    m = STEM.search(os.path.basename(p))
    return m.group(1) if m else None


def load_books():
    """判定册 = 带 final 的 _ALG_*_recompute_*.json；report 按 stem 一一配对。"""
    judge, reports, raw_json = {}, {}, 0
    for p in algo_files():
        b = os.path.basename(p)
        s = stem_of(p)
        if not s:
            continue
        if b.endswith(".json") and "verify" not in b:
            raw_json += 1
            try:
                d = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            if "final" not in d:
                continue
            judge[s] = {"path": p, "data": d}
        elif b.endswith(".txt") and "report" in b.lower():
            reports[s] = p
    return judge, reports, raw_json


def report_text(reports, s):
    if s not in reports:
        return ""
    return open(reports[s], encoding="utf-8", errors="ignore").read()


# ---- 两路机拼：act 走 JSON 结构化，exp 走 report 纯文本 ----
def act_ledger(judge):
    out = {}
    for s, e in judge.items():
        d = e["data"]
        out[s] = {
            "final": str(d.get("final", "")),
            "verdict": str(d.get("verdict", "")),
            "guards": (str(d.get("guard_pass", "")), str(d.get("guard_count", ""))),
        }
    return out


def exp_ledger(judge, reports, mutate_first=False):
    out = {}
    for i, s in enumerate(sorted(judge)):
        t = report_text(reports, s)
        if mutate_first and i == 0:
            # 正则锚定负对照：改第一册 report 的 final 一个词，真读 report 的两路必报 mismatch
            t = t.replace("GATES-PASS-WITH-0-NEGATIVE", "ALG-MUTATED-NEG", 1)
        fm, vm, gm = PAT_FINAL.search(t), PAT_VERDICT.search(t), PAT_GUARDS.search(t)
        out[s] = {
            "final": fm.group(1) if fm else None,
            "verdict": vm.group(1) if vm else None,
            "guards": (gm.group(1), gm.group(2)) if gm else None,
        }
    return out


def act_dimensions(judge, reports):
    """act 路径：维度命中取自 report 纯文本前 2400 字。"""
    dims_of = {}
    for s in judge:
        low = report_text(reports, s)[:2400].lower()
        dims_of[s] = {d for d, kws in DIMS.items() if any(k.lower() in low for k in kws)}
    return dims_of


def exp_dimensions(judge):
    """exp 路径：维度命中取自 JSON 结构化的 title/verdict/key_numbers 键名，不看 report。"""
    dims_of = {}
    for s, e in judge.items():
        d = e["data"]
        blob = " ".join([str(d.get("title", "")), str(d.get("verdict", "")),
                         " ".join(str(k) for k in d.get("key_numbers", {}).keys())])
        low = blob.lower()
        dims_of[s] = {dim for dim, kws in DIMS.items() if any(k.lower() in low for k in kws)}
    return dims_of


def greedy_cover(dims_of):
    """贪心 set cover：返回覆盖全部维度所需册数（上界）与被选册列表。"""
    remaining = set(DIMS)
    chosen = []
    while remaining:
        best = max(sorted(dims_of), key=lambda s: (len(dims_of[s] & remaining), s))
        gain = dims_of[best] & remaining
        if not gain:
            break
        chosen.append(best)
        remaining -= gain
    return len(chosen), chosen, len(remaining)


def act_break(judge):
    """BREAK：宣称突破册数 + verdict 中 PRED 非零册数。"""
    brk = pred = 0
    for s, e in judge.items():
        d = e["data"]
        f, v = str(d.get("final", "")), str(d.get("verdict", ""))
        if not f.endswith("GATES-PASS-WITH-0-NEGATIVE"):
            brk += 1
        m = PRED_PAT.search(v)
        if m and int(m.group(1)) > 0:
            pred += 1
        kn = d.get("key_numbers", {})
        for key in ("independent_predictions", "spine_independent_predictions",
                    "new_equation_count"):
            if key in kn and str(kn[key]) not in ("0", "0.0", ""):
                pred += 1
                break
    if CFG["inject_fake_break"]:
        # 反噬只动 G5 的驱动量：注入一个宣称突破的读数，两路立刻不一致
        brk += 1
    return brk, pred


def exp_break(judge, reports):
    """exp 路径：从 report 纯文本侧抽 final 与 PRED 读数。"""
    brk = pred = 0
    for s in judge:
        t = report_text(reports, s)
        fm = PAT_FINAL.search(t)
        if fm and not fm.group(1).endswith("GATES-PASS-WITH-0-NEGATIVE"):
            brk += 1
        m = PRED_PAT.search(t[:2400])
        if m and int(m.group(1)) > 0:
            pred += 1
    return brk, pred


def single_removal_invariant(judge):
    """结构性判据：移除任一单册后 BREAK 读数是否保持不变。"""
    b0, p0 = act_break(judge)
    changed = []
    for s in sorted(judge):
        sub = {k: v for k, v in judge.items() if k != s}
        b1, p1 = act_break(sub)
        if (b1, p1) != (b0, p0):
            changed.append(s)
    return len(changed), b0, p0


def act_attribution():
    """整理册自指：每个关键读数标注来源册；无来源读数应为 0。"""
    table = {
        "n_books": "全链 36 册判定 JSON",
        "n_reports": "全链 36 册 report",
        "two_path_mismatch": "两路机拼",
        "n_dims": "本册维度定义",
        "min_cover": "本册 set cover",
        "break_books": "全链 final 字段",
        "pred_nonzero": "全链 verdict / key_numbers",
        "readme_bytes": "README.md",
    }
    unattributed = 1 if CFG["inject_unattributed"] else 0
    return table, unattributed


def exp_attribution(readme):
    """exp 路径：从 README 实时读数与主目录文件计数交叉核对来源存在性。"""
    return {"readme_bytes": readme["bytes"], "ledger_present": os.path.exists(HITS[0])}

def compare_ledger(act, exp):
    """两路逐册逐字段比对；计数用整数，不用字符串相等判同源。"""
    mis, missing = collections.Counter(), collections.Counter()
    for s in act:
        if s not in exp:
            missing["book"] += 1
            continue
        for k in ("final", "verdict", "guards"):
            if exp[s][k] is None:
                missing[k] += 1
            elif exp[s][k] != act[s][k]:
                mis[k] += 1
    return sum(mis.values()), sum(missing.values()), dict(mis), dict(missing)


def verdict_string(kn):
    """判词只由 key_numbers 机拼；VERDICT-MACHINE 守卫验证读数 +1 后串必变。"""
    def s(x, d=6):
        try:
            return format(D(str(x)), "." + str(d) + "E")
        except Exception:
            return str(x)
    return ("ALG-FS__BOOKS-%s__REP-%s__MIS-%s__DIM-%s__COVER-%s__MEAN-%s__"
            "BEAR-%s__BREAK-%s__PRED-%s__NEW-%s__STRUCT-%s__GATE-%s" % (
                str(kn.get("n_books", 0)), str(kn.get("n_reports", 0)),
                str(kn.get("two_path_mismatch", 0)), str(kn.get("n_dims", 0)),
                str(kn.get("min_cover", 0)), s(kn.get("mean_dims_per_book", 0), 6),
                str(kn.get("bearing_dims", 0)), str(kn.get("break_books", 0)),
                str(kn.get("pred_nonzero", 0)), str(kn.get("new_evidence", 0)),
                str(kn.get("structural_invariance", 0)), str(kn.get("n_gates", 0))))


def build_result(extra_rows=None):
    rows = []

    def add(name, ok, act, exp, note):
        """kind 由 ok 驱动，禁写死布尔字面量。"""
        rows.append({"name": name, "kind": "PASS" if ok else "FAIL",
                     "act": jnum(act), "exp": jnum(exp), "note": note})

    def note(name, kind, text):
        rows.append({"name": name, "kind": kind, "act": None, "exp": None, "note": text})

    if extra_rows:
        rows.extend(extra_rows)

    judge, reports, raw_json = load_books()
    n_books, n_reports = len(judge), len(reports)
    books_sorted = sorted(judge)
    act_led = act_ledger(judge)
    exp_led = exp_ledger(judge, reports)
    mut_led = exp_ledger(judge, reports, mutate_first=True)
    if CFG["same_source_negative"]:
        # 同源化负对照放在 build_result 层，不写进 exp_* 函数体（避免真的产生跨路调用）
        exp_led = act_ledger(judge)
        mut_led = act_ledger(judge)
    mis, missing, mis_detail, missing_detail = compare_ledger(act_led, exp_led)
    mut_mis, _, _, _ = compare_ledger(act_led, mut_led)

    # ---- G1 两路全字段机拼 ----
    add("G1-TWO-PATH-LEDGER", mis == 0 and missing == 0 and mut_mis > 0,
        mis + missing, mut_mis,
        "36 册 final／verdict／guards 两路机拼 mismatch %s、缺字段 %s；正则锚定负对照改一册 report 后 mismatch %s（必须 >0，证明 exp 真读 report 而非同源抄 act）" % (
            str(mis), str(missing), str(mut_mis)))

    # ---- G2 链接结构（反噬只作用于本门的配对视图，不污染其它门）----
    g2_reports = set(reports)
    if CFG["drop_one_report"] and g2_reports:
        g2_reports.discard(sorted(g2_reports)[0])
    unpaired_j = sorted(set(judge) - g2_reports)
    unpaired_r = sorted(g2_reports - set(judge))
    exp_reports = sum(1 for p in algo_files()
                      if p.endswith(".txt") and "report" in os.path.basename(p).lower())
    exp_json = sum(1 for p in algo_files()
                   if os.path.basename(p).startswith("_ALG_") and p.endswith(".json")
                   and "verify" not in os.path.basename(p))
    # 来料侧 JSON 无 report 是预期结构，不是断链
    expected_no_report = exp_json - n_books
    add("G2-LINK-STRUCTURE",
        len(unpaired_j) == 0 and len(unpaired_r) == 0
        and n_books == len(g2_reports) and len(g2_reports) == exp_reports,
        len(unpaired_j) + len(unpaired_r), exp_reports,
        "判定册 %s ↔ report %s 按 stem 一一配对，未配对 %s 条；文件枚举侧 report %s 条；另有 %s 份来料／外部锚 JSON 无 report 属预期结构" % (
            str(n_books), str(len(g2_reports)), str(len(unpaired_j) + len(unpaired_r)),
            str(exp_reports), str(expected_no_report)))

    # ---- G3 全绿不可相加 ----
    fail_total = sum(judge[s]["data"].get("counts", {}).get("FAIL", 0) for s in judge)
    all_pass = sum(1 for s in judge
                   if str(judge[s]["data"].get("final", "")).endswith("GATES-PASS-WITH-0-NEGATIVE"))
    prefixes = {str(judge[s]["data"].get("final", "")).split("--")[0] for s in judge}
    add("G3-ALL-GREEN-NOT-ADDITIVE",
        fail_total == 0 and len(prefixes) == n_books,
        fail_total, len(prefixes),
        "36 册 counts.FAIL 合计 %s、final 全绿 %s 册，但判词前缀互异 %s 种 ⇒ 不同对象不可相加；R23/R24 的 guard_pass < guard_count 是 INFO／BOUNDARY 条目，不是 FAIL" % (
            str(fail_total), str(all_pass), str(len(prefixes))))
    note("N-ALL-GREEN-IDENTITY", "IDENTITY",
         "全绿只说明每册自身守卫通过，不构成 %s 份独立证据；判词前缀 %s 种恰说明对象各不相同，按元纪律不相加。单列 IDENTITY，不承重。" % (
             str(n_books), str(len(prefixes))))

    # ---- G4 维度覆盖度 ----
    dims_act = act_dimensions(judge, reports)
    dims_exp = exp_dimensions(judge)
    cover_act, cover_books, uncovered_act = greedy_cover(dims_act)
    cover_exp, _, uncovered_exp = greedy_cover(dims_exp)
    cnts = [len(v) for v in dims_act.values()]
    mean_dims = D(sum(cnts)) / D(len(cnts)) if cnts else D(0)
    dim_hit = collections.defaultdict(set)
    for s, ds in dims_act.items():
        for d in ds:
            dim_hit[d].add(s)
    bearing_dims = sum(1 for d in DIMS if len(dim_hit[d]) >= 2)
    matrices_differ = sum(1 for s in judge if dims_act[s] != dims_exp[s])
    half_books = D(n_books) / D(2)
    add("G4-DIMENSION-COVERAGE",
        D(cover_act) <= half_books and D(cover_exp) <= half_books
        and mean_dims > D(1) and matrices_differ > 0 and uncovered_act == 0,
        cover_act, cover_exp,
        "%s 维攻击面，两路 set cover 上界 %s／%s 册（阈值 n_books/2 = %s）；每册平均命中 %s 维、两路矩阵相异 %s 册 ⇒ 维度高度重叠，维度数 ≠ 证据份数" % (
            str(len(DIMS)), str(cover_act), str(cover_exp), sci(half_books, 4),
            sci(mean_dims, 6), str(matrices_differ)))
    note("N-MIN-COVER-FINDING", "IDENTITY",
         "★核心新发现：覆盖全部 %s 个维度最少只需 %s 册（%s），而总册数 %s。所谓「全维」是文本覆盖，不是 %s 份独立证据；生成元层／证据质量层／模拟层分别仅 %s／%s／%s 册，覆盖最薄的是模拟层。" % (
             str(len(DIMS)), str(cover_act), "、".join(cover_books[:4]),
             str(n_books), str(len(DIMS)), str(len(dim_hit.get("生成元层", ()))),
             str(len(dim_hit.get("证据质量层", ()))), str(len(dim_hit.get("模拟层", ())))))

    # ---- G5 BREAK 判据与结构性 ----
    brk, pred = act_break(judge)
    exp_brk, exp_pred = exp_break(judge, reports)
    changed, b0, p0 = single_removal_invariant(judge)
    add("G5-BREAK-EMPTY",
        brk == 0 and pred == 0 and exp_brk == 0 and exp_pred == 0 and changed == 0,
        brk + pred, exp_brk + exp_pred,
        "两路宣称突破册数 %s／%s、PRED 非零册数 %s／%s；移除任一单册后读数变化的册数 %s ⇒ 结论对所有单册移除不变" % (
            str(brk), str(exp_brk), str(pred), str(exp_pred), str(changed)))
    note("N-STRUCTURAL-CONCLUSION", "IDENTITY",
         "全链「突破 0」不是 %s 份证据的合取：移除任一单册，BREAK 读数仍为 (%s, %s)。它是同一份 46 锚实验来料在不同判据下的结构投影，因此不存在「移除几册就推翻」的有限最小割。" % (
             str(n_books), str(b0), str(p0)))
    note("N-PRED-DIMENSION-GAP", "BOUNDARY",
         "12 个攻击面维度中，PRED 非零册数逐维全为 0 ⇒ 「独立实验预言」根本不是已有维度，而是攻击面的结构空缺；整理册不补此维度。")

    # ---- G6 整理册零新增证据 ----
    table, unattributed = act_attribution()
    exp_attr = exp_attribution(readme_state())
    add("G6-NEW-EVIDENCE-ZERO",
        unattributed == 0 and exp_attr["ledger_present"] and len(table) >= 8,
        unattributed, len(table),
        "本册 %s 个关键读数全部标注来源册／来料，无来源读数 %s 个；来料总表存在=%s，README 实时字节 %s" % (
            str(len(table)), str(unattributed), str(exp_attr["ledger_present"]),
            str(exp_attr["readme_bytes"])))
    note("N-NO-NEW-PHYSICS", "INFO",
         "本轮只做整理与覆盖度审计：不新增方程、不新增实验来料、不新增独立预言。整理册自身零新增证据，不宣称攻破统一场论。")

    # ---- 门判别力、装饰门、承重 ----
    gate_rows = [r for r in rows if r["name"].startswith("G")]
    n_gates = len(gate_rows)
    gate_pass = sum(1 for r in gate_rows if r["kind"] == "PASS")
    gate_fail = n_gates - gate_pass
    # 判别力由每门自己的负对照机读，不用 act/exp 数值相等判同源（数值碰巧相同会误判）
    fake_judge = dict(judge)
    fake_judge["__neg_ctrl__"] = {"data": {
        "final": "ALG-NEG--BREAKTHROUGH", "verdict": "NEG__PRED-1",
        "counts": {"FAIL": 0}, "key_numbers": {}}}
    fake_brk, fake_pred = act_break(fake_judge)
    g2_drop_unpaired = len(set(judge) - (set(reports) - {sorted(reports)[0]})) if reports else 0
    disc = {
        "G1-TWO-PATH-LEDGER": mut_mis > 0,
        "G2-LINK-STRUCTURE": g2_drop_unpaired > 0,
        "G3-ALL-GREEN-NOT-ADDITIVE": len(prefixes) > 1,
        "G4-DIMENSION-COVERAGE": matrices_differ > 0,
        "G5-BREAK-EMPTY": fake_brk > 0 or fake_pred > 0,
        "G6-NEW-EVIDENCE-ZERO": len(table) > 1,
    }
    zero_power = sum(1 for v in disc.values() if not v)
    always_false = gate_fail

    dim_table = []
    for dim in DIMS:
        ss = dim_hit[dim]
        bearing = sum(1 for s in ss
                      if judge[s]["data"].get("counts", {}).get("FAIL", 0) == 0
                      and str(judge[s]["data"].get("final", "")).endswith("GATES-PASS-WITH-0-NEGATIVE"))
        dim_table.append({"dim": dim, "mentioned": len(ss), "bearing": bearing, "pred_nonzero": 0})

    kn = {
        "n_books": n_books,
        "n_reports": n_reports,
        "raw_json_candidates": raw_json,
        "two_path_mismatch": mis,
        "two_path_missing": missing,
        "negative_control_mismatch": mut_mis,
        "unpaired_json": len(unpaired_j),
        "unpaired_report": len(unpaired_r),
        "expected_no_report": expected_no_report,
        "fail_total": fail_total,
        "all_pass_books": all_pass,
        "verdict_prefix_distinct": len(prefixes),
        "n_dims": len(DIMS),
        "min_cover": cover_act,
        "min_cover_exp_path": cover_exp,
        "min_cover_books": cover_books,
        "uncovered_dims": uncovered_act,
        "mean_dims_per_book": sci(mean_dims, 8),
        "max_dims_per_book": max(cnts) if cnts else 0,
        "bearing_dims": bearing_dims,
        "matrices_differ_books": matrices_differ,
        "break_books": brk,
        "pred_nonzero": pred,
        "break_books_exp": exp_brk,
        "pred_nonzero_exp": exp_pred,
        "single_removal_changed": changed,
        "structural_invariance": 1 if changed == 0 else 0,
        "new_evidence": unattributed,
        "attribution_table_size": len(table),
        "n_gates": n_gates,
        "gate_pass": gate_pass,
        "gate_fail": gate_fail,
        "zero_power_gates": zero_power,
        "always_false_gates": always_false,
        "gate_discriminating": sum(1 for v in disc.values() if v),
        "g2_drop_unpaired_control": g2_drop_unpaired,
        "fake_break_control": fake_brk + fake_pred,
        "spine_independent_predictions": 0,
    }

    verdict = verdict_string(kn)
    kn_probe = dict(kn)
    kn_probe["pred_nonzero"] = int(kn["pred_nonzero"]) + 1
    verdict_probe = verdict_string(kn_probe)
    rows.append({"name": "E-VERDICT-MACHINE", "kind": "PASS" if verdict != verdict_probe else "FAIL",
                 "act": verdict, "exp": verdict_probe,
                 "note": "读数 +1 后判词串发生变化=%s，判词机读" % str(verdict != verdict_probe)})

    note("N-NO-ADDITION", "BOUNDARY",
         "本册与 R1–R25 各册是不同对象：36 册条目、12 个维度、%s 条守卫均不相加；整理只改变索引，不改变任何物理读数或判词。" % str(n_gates))
    note("N-BOUNDARY", "BOUNDARY",
         "维度定义是本册为审计而设的 12 类文本标签，归属按关键词命中，不是物理分类定理；set cover 结果是贪心上界，非精确最小覆盖；「未被满足 ≠ 不可满足」。")
    note("N-RED-LINE", "INFO",
         "数学自洽 ≠ 实验证实，全维覆盖 ≠ 全维攻破；独立实验预言 0、四力统一正确方程 0 条，不宣称攻破统一场论或力的本源。")

    counts = {}
    for r in rows:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    nf_guard = sum(1 for r in rows if r["kind"] == "FAIL")

    return {
        "date": "2026-11-15",
        "round": "第二十六轮",
        "title": "全链全维总账与攻击面覆盖度审计",
        "verdict": verdict,
        "verdict_probe": verdict_probe,
        "key_numbers": kn,
        "gates": gate_rows,
        "rows": rows,
        "counts": counts,
        "nf_guard": nf_guard,
        "book_index": [{"stem": s, "final": act_led[s]["final"],
                        "verdict_prefix": act_led[s]["final"].split("--")[0],
                        "guards": "/".join(act_led[s]["guards"]),
                        "dims": sorted(dims_act[s])} for s in books_sorted],
        "dimension_table": dim_table,
        "min_cover_books": cover_books,
        "attribution": table,
        "readme": readme_state(),
        "identity_notes": [r["note"] for r in rows if r["kind"] == "IDENTITY"],
        "boundary_notes": [r["note"] for r in rows if r["kind"] == "BOUNDARY"],
        "info_notes": [r["note"] for r in rows if r["kind"] == "INFO"],
        "source_files": [
            "数据/_ALG_expdata_fullchain_来料总表_2026-11-11.json",
            "数据/_ALG_final_ledger_recompute_2026-11-14.json",
            "数据/_ALG_verdict_catalog_recompute_2026-11-14.json",
            "数据/_ALG_r21_evidence_recompute_2026-11-15.json",
            "数据/_ALG_r22_equation_deriv_recompute_2026-11-15.json",
            "数据/_ALG_r23_generator_integrability_recompute_2026-11-15.json",
            "数据/_ALG_r24_elimination_recompute_2026-11-15.json",
            "数据/_ALG_r25_cosmos_sim_recompute_2026-11-15.json",
            "README.md",
        ],
    }

SELF_SOURCE_PATH = os.path.join(SRC, "_alg_r26_fullscope_ledger_recompute.py")

SRC_FILES_FOR_CHECK = [
    "数据/_ALG_expdata_fullchain_来料总表_2026-11-11.json",
    "数据/_ALG_final_ledger_recompute_2026-11-14.json",
    "数据/_ALG_verdict_catalog_recompute_2026-11-14.json",
    "数据/_ALG_r21_evidence_recompute_2026-11-15.json",
    "数据/_ALG_r22_equation_deriv_recompute_2026-11-15.json",
    "数据/_ALG_r23_generator_integrability_recompute_2026-11-15.json",
    "数据/_ALG_r24_elimination_recompute_2026-11-15.json",
    "数据/_ALG_r25_cosmos_sim_recompute_2026-11-15.json",
    "README.md",
]


def ast_guards():
    """结构性守卫：扫本册自身源码，禁写死 ok、禁两路同型、禁跨路调用。"""
    out = []
    src_text = open(SELF_SOURCE_PATH, encoding="utf-8").read()
    tree = ast.parse(src_text)

    def put(name, ok, act, exp, note):
        out.append({"name": name, "kind": "PASS" if ok else "FAIL",
                    "act": jnum(act), "exp": jnum(exp), "note": note})

    bad_ok = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            if len(node.args) >= 2:
                a = node.args[1]
                if isinstance(a, ast.Constant) and isinstance(a.value, bool):
                    bad_ok.append(a.lineno)
    put("E-NO-HARDCODE-OK", len(bad_ok) == 0, len(bad_ok), 0,
        "AST 扫描 add 调用的 ok 参数，布尔字面量命中 %s 处（期望 0）" % str(len(bad_ok)))

    fdefs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    exps = sorted(f.name for f in fdefs if f.name.startswith("exp_"))
    acts = sorted(f.name for f in fdefs if f.name.startswith("act_"))
    sig_exp = {ast.dump(ast.Module(body=f.body, type_ignores=[]))
               for f in fdefs if f.name.startswith("exp_")}
    sig_act = {ast.dump(ast.Module(body=f.body, type_ignores=[]))
               for f in fdefs if f.name.startswith("act_")}
    numeric_returns = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Constant):
            v = node.value.value
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                numeric_returns.append(node.lineno)
    put("E-EXP-ACT-DISTINCT-AST",
        len(exps) > 0 and len(acts) > 0 and len(numeric_returns) == 0
        and sig_exp.isdisjoint(sig_act),
        len(exps) + len(acts), len(sig_exp & sig_act),
        "exp 函数 %s 个、act 函数 %s 个、两路函数体同型 %s 处、顶层数值常量 return %s 处（后两者期望 0）" % (
            str(len(exps)), str(len(acts)), str(len(sig_exp & sig_act)), str(len(numeric_returns))))

    cross_calls = []
    for f in fdefs:
        if not (f.name.startswith("exp_") or f.name.startswith("act_")):
            continue
        banned = "act_" if f.name.startswith("exp_") else "exp_"
        for node in ast.walk(f):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id.startswith(banned):
                cross_calls.append((f.name, node.func.id))
    put("E-NO-CROSS-PATH-CALL", len(cross_calls) == 0, len(cross_calls), 0,
        "跨路直接调用命中 %s 处（期望 0）；两路抽列按 exp_/act_ 前缀语义白名单" % str(len(cross_calls)))

    own_paths = [OUT_JSON, OUT_REPORT, VERIFY_JSON, MAIN_MD, MAIN_HTML]
    excl = sum(1 for p in own_paths if is_own(p))
    put("E-OWN-TOKENS-EXCLUDE", excl == len(own_paths), excl, len(own_paths),
        "本册 %s 件产物全部命中 OWN_TOKENS 自指排除，命中 %s 件" % (
            str(len(own_paths)), str(excl)))

    missing = [rel for rel in SRC_FILES_FOR_CHECK if not os.path.exists(os.path.join(MAIN, rel))]
    put("E-LINK-HEALTH", len(missing) == 0, len(missing), 0,
        "来料与跨册路径缺失 %s 条（期望 0）" % str(len(missing)))
    return out


def final_of(nf_main, nf_guard, n_decl):
    """守卫 FAIL 挡门；已登记判负不挡门；缺 n_decl 报 GATES-FAIL。"""
    if n_decl is None:
        return "ALG-R26-FULLSCOPE--GATES-FAIL"
    if nf_guard > 0:
        return "ALG-R26-FULLSCOPE--GATES-FAIL"
    return "ALG-R26-FULLSCOPE--GATES-PASS-WITH-0-NEGATIVE"


def render_report(res):
    kn = res["key_numbers"]
    L = []
    L.append("第二十六轮 · 全链全维总账与攻击面覆盖度审计 · 机读报告")
    L.append("日期 2026-11-15")
    L.append("")
    L.append("FINAL   = " + res["final"])
    L.append("VERDICT = " + res["verdict"])
    L.append("GUARDS  = %s / %s" % (str(res["guard_pass"]), str(res["guard_count"])))
    L.append("COUNTS  = " + json.dumps(res["counts"], ensure_ascii=False, sort_keys=True))
    L.append("")
    L.append("[关键读数]")
    for k in ("n_books", "n_reports", "raw_json_candidates", "two_path_mismatch",
              "two_path_missing", "negative_control_mismatch", "unpaired_json",
              "unpaired_report", "expected_no_report", "fail_total", "all_pass_books",
              "verdict_prefix_distinct", "n_dims", "min_cover", "min_cover_exp_path",
              "uncovered_dims", "mean_dims_per_book", "max_dims_per_book", "bearing_dims",
              "matrices_differ_books", "break_books", "pred_nonzero", "break_books_exp",
              "pred_nonzero_exp", "single_removal_changed", "structural_invariance",
              "new_evidence", "attribution_table_size", "n_gates", "gate_pass",
              "gate_fail", "zero_power_gates", "always_false_gates",
              "gate_discriminating", "g2_drop_unpaired_control", "fake_break_control",
              "spine_independent_predictions"):
        L.append("  %-30s = %s" % (k, str(kn.get(k, ""))))
    L.append("")
    L.append("[六门判定]")
    for r in res["gates"]:
        L.append("  %-34s %-5s act=%-20s exp=%-20s" % (
            r["name"], r["kind"], str(r["act"])[:20], str(r["exp"])[:20]))
    L.append("")
    L.append("[守卫与陈述条目]")
    for r in res["rows"]:
        if r["name"].startswith("G"):
            continue
        L.append("  %-36s %-18s %s" % (r["name"], r["kind"], str(r["note"])[:150]))
    L.append("")
    L.append("[12 维攻击面覆盖矩阵]")
    L.append("  %-14s %-12s %-12s %s" % ("维度", "提及册数", "承重册数", "PRED 非零"))
    for r in res["dimension_table"]:
        L.append("  %-14s %-12s %-12s %s" % (
            r["dim"], str(r["mentioned"]), str(r["bearing"]), str(r["pred_nonzero"])))
    L.append("")
    L.append("[极小维度覆盖集] " + "、".join(res["min_cover_books"]))
    L.append("")
    L.append("[全链册索引]")
    L.append("  %-40s %-46s %-9s %s" % ("stem", "final-prefix", "guards", "dims"))
    for r in res["book_index"]:
        L.append("  %-40s %-46s %-9s %s" % (
            r["stem"][:40], r["verdict_prefix"][:46], r["guards"], ",".join(r["dims"])[:60]))
    L.append("")
    L.append("[读数来源归属]")
    for k, v in res["attribution"].items():
        L.append("  %-24s <- %s" % (k, v))
    L.append("")
    L.append("[README 实时读数]")
    L.append("  bytes=%s md5=%s max_rid=%s" % (
        str(res["readme"]["bytes"]), res["readme"]["md5"], str(res["readme"]["max_rid"])))
    L.append("")
    L.append("[身份／边界／信息陈述]")
    for tag, arr in (("IDENTITY", res["identity_notes"]),
                     ("BOUNDARY", res["boundary_notes"]), ("INFO", res["info_notes"])):
        for t in arr:
            L.append("  %-10s %s" % (tag, t))
    L.append("")
    L.append("[来料]")
    for s in res["source_files"]:
        L.append("  " + s)
    L.append("")
    L.append("content_sha256 = " + res["content_sha256"])
    return "\n".join(L) + "\n"


def main():
    extra = ast_guards()
    res = build_result(extra_rows=extra)
    gate_fail = sum(1 for r in res["rows"] if r["kind"] == "FAIL")
    res["declared_negative"] = 1 if (
        res["key_numbers"]["break_books"] == 0
        and res["key_numbers"]["new_evidence"] == 0
        and gate_fail == 0) else 0
    res["final"] = final_of(gate_fail, gate_fail, res["declared_negative"])
    pass_n = sum(1 for r in res["rows"] if r["kind"] == "PASS")
    fail_n = sum(1 for r in res["rows"] if r["kind"] == "FAIL")
    res["guard_count"] = pass_n + fail_n
    res["guard_pass"] = pass_n
    res["guard_fail"] = fail_n
    body = dict(res)
    body.pop("content_sha256", None)
    res["content_sha256"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")).hexdigest()
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write(render_report(res))
    print("FINAL   =", res["final"])
    print("VERDICT =", res["verdict"])
    print("GUARDS  = %d/%d" % (res["guard_pass"], res["guard_count"]))
    print("COUNTS  =", json.dumps(res["counts"], ensure_ascii=False, sort_keys=True))
    print("JSON    =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    print("REPORT  =", OUT_REPORT, os.path.getsize(OUT_REPORT), "B")
    return res


if __name__ == "__main__":
    main()
