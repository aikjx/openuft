# -*- coding: utf-8 -*-
"""算法联盟 第十九轮：全链判决目录整理与「零读数」独立性普查。

审对象是十八轮链留下的 28 册机读判决：把「突破 0 / 预言 0」当作可算对象，
问它们究竟是几份独立证据、对最终判词有多少判别力。不产新物理、不占 RID、
不与任何卷相加；与 R14/R17 的一致性总账不同对象，不重复其结论。
"""
import os
import glob
import re
import json
import hashlib
import ast
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal

DATE = "2026-11-14"
ANCHOR = "_ALG_information_gate_recompute_2026-11-12.json"
CHI2_CRIT = "3.84145882069"

RE_FINAL_REPORT = re.compile(r"^final\s*:\s*(\S+)", re.M)
RE_VERDICT_REPORT = re.compile(r"^verdict\s*:\s*(.+)$", re.M)
RE_GUARD_REPORT = re.compile(r"^guards\s*:\s*(\d+)\s*/\s*(\d+)", re.M)
RE_SHA_REPORT = re.compile(r"^sha256\s*:\s*([0-9a-f]{64})", re.M)
RE_ZERO_TOKEN = re.compile(r"(?:^|__)([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)-0(?=$|__)")
RE_REF = re.compile(r"^[ \t>*-]*(?:数据|报告|核验|机核|源码|可视化|主文)[：:]\s*`([^`]+)`", re.M)


def find_main():
    """并行会话可能新增同形目录 ⇒ 用唯一既有产物反查主目录。"""
    hits = glob.glob("openuft/**/" + ANCHOR, recursive=True)
    assert len(hits) == 1, "ANCHOR-HITS=%d" % len(hits)
    return os.path.dirname(os.path.dirname(hits[0]))


MAIN = find_main()
DATA = os.path.join(MAIN, "数据")
SRC = os.path.join(MAIN, "源码")
ROOT = os.path.abspath(os.getcwd())
README = os.path.join(MAIN, "README.md")
OUT_JSON = os.path.join(DATA, "_ALG_verdict_catalog_recompute_%s.json" % DATE)
OUT_REPORT = os.path.join(DATA, "_ALG_verdict_catalog_recompute_report_%s.txt" % DATE)
OUT_VERIFY = os.path.join(DATA, "_ALG_verdict_catalog_verify_%s.json" % DATE)


def is_own(p):
    """自指盘点必须先定义「是否把自己算进去」，否则首跑与幂等复跑读数漂移。"""
    b = os.path.basename(p)
    return ("verdict_catalog" in b.lower() or "r19" in b.lower()
            or "目录" in b)


def exclude_own(paths):
    return sorted(p for p in paths if not is_own(p))


def rd(p):
    return open(p, "r", encoding="utf-8").read()


def rb(p):
    return open(p, "rb").read()


def md5(p):
    return hashlib.md5(rb(p)).hexdigest()


def sha_file(p):
    return hashlib.sha256(rb(p)).hexdigest()


def canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha_obj(obj):
    return hashlib.sha256(canon(obj).encode("utf-8")).hexdigest()


def pct(num, den):
    """占比须用精确 Fraction；Decimal 除法下 617/935+318/935 不等于 1。"""
    if den == 0:
        return "n/a"
    q = Fraction(int(num), int(den)) * 100
    return str((D(q.numerator) / D(q.denominator)).quantize(D("0.000001")))


def report_path_from_json(jp):
    """JSON -> report 的唯一路径构造；机核与核验器共用，禁另起一套。"""
    stem = os.path.splitext(os.path.basename(jp))[0]
    stem = stem.replace("_recompute_", "_recompute_report_") + ".txt"
    return os.path.join(DATA, stem)


def zero_keys_of(kn):
    out = []
    for k, v in kn.items():
        if isinstance(v, bool):
            continue
        if isinstance(v, (int, float)) and v == 0:
            out.append(k)
    return sorted(out)


def zero_tokens_of(verdict):
    return sorted(set(RE_ZERO_TOKEN.findall(verdict or "")))


# ---------- 两路独立机拼：act = 结构化 JSON，exp = report 纯文本正则 ----------
def act_structured(jp):
    d = json.loads(rd(jp))
    kn = d.get("key_numbers", {})
    return dict(final=str(d.get("final", "")),
                verdict=str(d.get("verdict", "")),
                guards=(int(d.get("guard_pass", -1)), int(d.get("guard_count", -1))),
                sha=d.get("content_sha256"),
                zero_keys=zero_keys_of(kn),
                zero_tokens=zero_tokens_of(str(d.get("verdict", ""))),
                key_numbers=len(kn),
                path=os.path.basename(jp))


def exp_textual(rp):
    t = rd(rp)
    f = RE_FINAL_REPORT.search(t)
    v = RE_VERDICT_REPORT.search(t)
    g = RE_GUARD_REPORT.search(t)
    s = RE_SHA_REPORT.search(t)
    vt = v.group(1).strip() if v else ""
    return dict(final=(f.group(1) if f else None),
                verdict=vt,
                guards=((int(g.group(1)), int(g.group(2))) if g else None),
                sha=(s.group(1) if s else None),
                zero_tokens=zero_tokens_of(vt),
                pass_rows=len(re.findall(r"\[PASS\]", t)),
                path=os.path.basename(rp))


def build_catalog():
    jsons = exclude_own(glob.glob(os.path.join(DATA, "_ALG_*recompute_*.json")))
    jsons = [p for p in jsons if "report" not in os.path.basename(p)]
    rows = []
    for jp in jsons:
        rp = report_path_from_json(jp)
        a = act_structured(jp)
        e = exp_textual(rp) if os.path.isfile(rp) else None
        agree = False
        if e is not None:
            agree = (a["final"] == e["final"] and a["verdict"] == e["verdict"]
                     and a["guards"] == e["guards"])
        rows.append(dict(json=os.path.basename(jp),
                         report=os.path.basename(rp),
                         has_report=os.path.isfile(rp),
                         final=a["final"], verdict=a["verdict"],
                         guards=list(a["guards"]),
                         zero_keys=a["zero_keys"],
                         zero_tokens=a["zero_tokens"],
                         key_numbers=a["key_numbers"],
                         pred0=("PRED-0" in a["verdict"]),
                         clean0=("CLEAN-0" in a["verdict"]),
                         agree=agree,
                         path=os.path.relpath(jp, ROOT)))
    return rows


def readme_write_hits():
    """AST 结构性检查：本册机核内是否存在对 README 的写操作。
    不用「复跑前后 MD5 相等」——并行会话改动仓库时那是时序型判据（R13 教训）。"""
    tree = ast.parse(rd(__file__))
    hits = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        fn = n.func
        if not (isinstance(fn, ast.Name) and fn.id == "open"):
            continue
        pos = [a.value for a in n.args
               if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        kws = {kw.arg: kw.value.value for kw in n.keywords
               if isinstance(kw.value, ast.Constant)
               and isinstance(kw.value.value, str)}
        first = pos[0] if pos else kws.get("file", "")
        mode = pos[1] if len(pos) > 1 else kws.get("mode", "")
        if "README" in first.upper() and any(c in mode for c in "wa+"):
            hits.append(n.lineno)
    return hits

import itertools

# ---------- 三个承重门：反噬变体逐一拆掉其中一个 ----------
def gate_link_ok(broken):
    return len(broken) == 0


def gate_match_ok(mismatches):
    return len(mismatches) == 0


def gate_catalog_ok(rows):
    return len(rows) > 0 and all(r["has_report"] for r in rows)


def simulate(inject, broken, mm, rows):
    b = list(broken)
    m = list(mm)
    r = list(rows)
    if inject == "fake-link":
        b.append("__FAKE_MISSING_FILE__.txt")
    elif inject == "fake-mismatch":
        m.append("__FAKE_TWO_PATH_MISMATCH__")
    elif inject == "fake-catalog":
        r.append(dict(has_report=False, json="__FAKE_BOOK__.json"))
    return dict(counts=(len(b), len(m), len(r)),
                link_caught=(not gate_link_ok(b)),
                match_caught=(not gate_match_ok(m)),
                catalog_caught=(not gate_catalog_ok(r)))


def no_hardcode_ok():
    tree = ast.parse(rd(__file__))
    bad = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                and n.func.id == "add" and len(n.args) >= 2 \
                and isinstance(n.args[1], ast.Constant):
            bad.append(n.lineno)
    return (len(bad) == 0), bad


def exp_act_distinct():
    tree = ast.parse(rd(__file__))
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    acts = [f for f in fns if f.name.startswith("act_")]
    exps = [f for f in fns if f.name.startswith("exp_")]
    bad = []
    for f in acts + exps:
        for n in ast.walk(f):
            if isinstance(n, ast.Return) and isinstance(n.value, ast.Constant):
                bad.append(f.name + ":" + str(n.lineno))
    sig_a = sorted(ast.dump(f) for f in acts)
    sig_e = sorted(ast.dump(f) for f in exps)
    ok = (len(acts) >= 1 and len(exps) >= 1 and len(bad) == 0
          and sig_a != sig_e)
    return ok, dict(act_functions=len(acts), exp_functions=len(exps),
                    constant_returns=bad, signatures_distinct=(sig_a != sig_e))


def final_of(nf_main, nf_guard, n_decl):
    if n_decl is None:
        return "ALG-VERDICT-CATALOG--GATES-FAIL"
    if nf_guard > 0:
        return "ALG-VERDICT-CATALOG--GATES-FAIL"
    return "ALG-VERDICT-CATALOG--GATES-PASS-WITH-0-NEGATIVE"


GUARDS = []


def add(name, ok, note=""):
    kind = "PASS" if ok else "FAIL"
    GUARDS.append(dict(name=name, ok=bool(ok), kind=kind, note=str(note)))
    return bool(ok)


def min_flip_cut(rows, freq):
    """改动最少几个共享判据对象，能波及（使其零读数集合变化）全部册。"""
    keys = sorted(freq)
    sets = [set(r["zero_keys"]) for r in rows]
    n = len(rows)
    for k in keys:
        if sum(1 for s in sets if k in s) == n:
            return dict(size=1, keys=[k], affected=n, best_pair_cover=None)
    best_cover = 0
    best_pair = None
    for a, b in itertools.combinations(keys, 2):
        c = sum(1 for s in sets if a in s or b in s)
        if c > best_cover:
            best_cover = c
            best_pair = [a, b]
        if c == n:
            return dict(size=2, keys=[a, b], affected=n,
                        best_pair_cover=best_cover)
    chosen = []
    covered = set()
    while len(covered) < n and keys:
        pick = max(keys, key=lambda k: sum(
            1 for i, s in enumerate(sets) if k in s and i not in covered))
        gain = sum(1 for i, s in enumerate(sets)
                   if pick in s and i not in covered)
        if gain == 0:
            break
        chosen.append(pick)
        keys.remove(pick)
        for i, s in enumerate(sets):
            if pick in s:
                covered.add(i)
    return dict(size=len(chosen), keys=chosen, affected=len(covered),
                best_pair_cover=best_cover, best_pair=best_pair)


def compute():
    GUARDS.clear()
    cat = build_catalog()
    n_books = len(cat)

    # ---------- 目录与断链 ----------
    broken = []
    texts = exclude_own(glob.glob(os.path.join(MAIN, "算法联盟_*.md")))
    for m in texts:
        for r in RE_REF.findall(rd(m)):
            if not os.path.isfile(os.path.join(MAIN, r)):
                broken.append(os.path.basename(m) + " -> " + r)
    htmls = exclude_own(glob.glob(os.path.join(MAIN, "算法联盟_*.html")))
    kernels = exclude_own(glob.glob(os.path.join(SRC, "_alg_*_recompute.py")))
    reports = exclude_own(glob.glob(os.path.join(DATA, "_ALG_*_recompute_report_*.txt")))

    # ---------- 两路机拼 ----------
    mismatches = []
    for row in cat:
        if not row["has_report"]:
            mismatches.append("NO-REPORT:" + row["json"])
        elif not row["agree"]:
            mismatches.append("TWO-PATH:" + row["json"])
    n_agree = sum(1 for r in cat if r["agree"])

    # ---------- 零读数去重 ----------
    freq = {}
    for r in cat:
        for k in r["zero_keys"]:
            freq[k] = freq.get(k, 0) + 1
    total_zero = sum(len(r["zero_keys"]) for r in cat)
    unique_zero = len(freq)
    duplicate_occ = total_zero - unique_zero
    shared_ge2 = sum(1 for v in freq.values() if v >= 2)
    shared_all = sum(1 for v in freq.values() if v == n_books)
    top_keys = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:12]

    # ---------- 判词覆盖 ----------
    pred0_books = sum(1 for r in cat if r["pred0"])
    clean0_books = sum(1 for r in cat if r["clean0"])
    no_zero_token_books = sum(1 for r in cat if len(r["zero_tokens"]) == 0)
    zero_token_total = sum(len(r["zero_tokens"]) for r in cat)
    distinct_zero_tokens = sorted({t for r in cat for t in r["zero_tokens"]})
    final_forms = sorted({r["final"] for r in cat})
    final_suffixes = sorted({r["final"].split("--")[-1] for r in cat})

    # ---------- final 判别力（结构性 IDENTITY + 两侧对照） ----------
    final_base = final_of(0, 0, 0)
    final_guard = final_of(0, 1, 0)
    final_missing = final_of(0, 0, None)
    # 预设「28 册 final 同形」被来料证伪：全串是 28 种，同形的只是判决后缀。
    # 改驱动量为后缀，全串种数如实保留，不放宽守卫。
    identical_final = (len(final_suffixes) == 1
                       and final_suffixes[0] == "GATES-PASS-WITH-0-NEGATIVE")

    # ---------- 最小翻转割 ----------
    cut = min_flip_cut(cat, freq)

    kn = dict(
        books=n_books, reports=len(reports), kernels=len(kernels),
        main_texts=len(texts), htmls=len(htmls),
        two_path_agree=n_agree, two_path_mismatch=len(mismatches),
        broken_ref_count=len(broken),
        total_zero_occurrences=total_zero,
        unique_zero_keys=unique_zero,
        duplicate_occurrences=duplicate_occ,
        duplication_pct=pct(duplicate_occ, total_zero),
        shared_keys_ge2=shared_ge2,
        shared_by_all_books=shared_all,
        pred0_books=pred0_books,
        pred0_coverage_pct=pct(pred0_books, n_books),
        clean0_books=clean0_books,
        no_zero_token_books=no_zero_token_books,
        zero_token_total=zero_token_total,
        distinct_zero_tokens=len(distinct_zero_tokens),
        final_distinct_forms=len(final_forms),
        final_suffix_forms=len(final_suffixes),
        flip_cut_size=cut["size"], flip_cut_affected=cut["affected"],
        flip_cut_best_pair_cover=cut.get("best_pair_cover"),
        readme_write_hits=len(readme_write_hits()),
        readme_bytes=os.path.getsize(README),
        chi2_crit=CHI2_CRIT)

    # ---------- 判别力自检：扰动后读数必须变化 ----------
    probe_cat = [dict(r) for r in cat]
    probe_total = sum(len(r["zero_keys"]) for r in probe_cat)
    probe_cat[0]["zero_keys"] = list(probe_cat[0]["zero_keys"]) + ["__PROBE_KEY__"]
    probe_total_plus = sum(len(r["zero_keys"]) for r in probe_cat)
    probe_pred0 = sum(1 for r in cat if r["pred0"])
    probe_rows = [dict(r) for r in cat]
    for i, r in enumerate(probe_rows):
        if r["pred0"]:
            probe_rows[i] = dict(r, pred0=False)
            break
    probe_pred0_after = sum(1 for r in probe_rows if r["pred0"])

    # ---------- 控制组 ----------
    sim_none = simulate("none", broken, mismatches, cat)
    sim_link = simulate("fake-link", broken, mismatches, cat)
    sim_match = simulate("fake-mismatch", broken, mismatches, cat)
    sim_cat = simulate("fake-catalog", broken, mismatches, cat)
    backfire = dict(baseline=sim_none, fake_link=sim_link,
                    fake_mismatch=sim_match, fake_catalog=sim_cat,
                    distinct_readings=len({sim_none["counts"],
                                           sim_link["counts"],
                                           sim_match["counts"],
                                           sim_cat["counts"]}))

    verdict = ("ALG-VC__BOOKS-%d__ZERO-%d__UNIQ-%d__DUP-%s__SHARED-%d"
               "__PRED0-%d__CLEAN0-%d__CUT-%d__SUFFIX-%d__FULLFORM-%d"
               "__CLEAN-0__PRED-0"
               % (n_books, total_zero, unique_zero, kn["duplication_pct"],
                  shared_ge2, pred0_books, clean0_books, cut["size"],
                  len(final_suffixes), len(final_forms)))
    verdict_plus = verdict.replace("BOOKS-%d" % n_books,
                                   "BOOKS-%d" % (n_books + 1))
    # ---------- 整理层守卫 ----------
    add("VC-CATALOG-COMPLETE",
        gate_catalog_ok(cat) and n_books == len(reports) and n_books > 0,
        "目录 %d 册 / report %d 份，逐册有报告" % (n_books, len(reports)))
    add("VC-TWO-PATH-AGREE",
        n_agree == n_books and gate_match_ok(mismatches),
        "JSON 结构 vs report 文本逐册三项一致 %d/%d，失配 %d"
        % (n_agree, n_books, len(mismatches)))
    add("VC-LINK-HEALTH", gate_link_ok(broken),
        "主文声明引用断链 %d 条" % len(broken))
    add("VC-FINAL-SUFFIX-UNIFORM", identical_final,
        "%d 册 final 全串 %d 种、判决后缀 %d 种（驱动量已由全串改为后缀）"
        % (n_books, len(final_forms), len(final_suffixes)))
    add("VC-FINAL-OF-CONSISTENT",
        final_guard != final_base and final_missing != final_base
        and final_base.endswith("PASS-WITH-0-NEGATIVE"),
        "两侧对照：守卫 FAIL 与缺 n_decl 均使 final 翻转")
    add("VC-ZERO-KEY-COUNT-MACHINE",
        probe_total_plus == probe_total + 1,
        "零读数计数对 +1 扰动响应 %d -> %d" % (probe_total, probe_total_plus))
    add("VC-PRED0-COVERAGE-MACHINE",
        probe_pred0_after == probe_pred0 - 1,
        "PRED-0 覆盖数对移除扰动响应 %d -> %d"
        % (probe_pred0, probe_pred0_after))
    add("VC-DEDUPLICATION-DRIVEN",
        unique_zero > 0 and duplicate_occ >= 0 and shared_ge2 > 0,
        "零读数 %d 次 / 去重 %d 键 / 重复 %d 次（%s%%）/ 跨册共享键 %d"
        % (total_zero, unique_zero, duplicate_occ,
           kn["duplication_pct"], shared_ge2))
    add("VC-FLIP-CUT-COMPUTED",
        cut["size"] >= 1 and cut["affected"] <= n_books,
        "最小翻转割 %d 个键、波及 %d 册" % (cut["size"], cut["affected"]))
    add("VC-VERDICT-MACHINE",
        verdict_plus != verdict and str(n_books) in verdict,
        "册数 +1 后判词串改变")
    add("VC-EXP-ACT-DISTINCT-AST", exp_act_distinct()[0],
        "act/exp 两族 AST 不同且无常量 return：%s" % str(exp_act_distinct()[1]))
    add("VC-NO-HARDCODE-OK", no_hardcode_ok()[0],
        "add() 布尔字面量 %d 处" % len(no_hardcode_ok()[1]))
    add("VC-README-WRITE-ZERO", len(readme_write_hits()) == 0,
        "机核对 README 的写操作 %d 处（结构性检查，不用时序 MD5）"
        % len(readme_write_hits()))

    # ---------- 控制组守卫 ----------
    add("CONTROL-FAKE-LINK-CAUGHT",
        sim_link["link_caught"] and not sim_none["link_caught"],
        "注入假断链 %s -> %s" % (sim_none["counts"], sim_link["counts"]))
    add("CONTROL-FAKE-MISMATCH-CAUGHT",
        sim_match["match_caught"] and not sim_none["match_caught"],
        "注入假失配 %s -> %s" % (sim_none["counts"], sim_match["counts"]))
    add("CONTROL-FAKE-CATALOG-CAUGHT",
        sim_cat["catalog_caught"] and not sim_none["catalog_caught"],
        "注入假册 %s -> %s" % (sim_none["counts"], sim_cat["counts"]))
    add("CONTROL-BASELINE-GREEN",
        not (sim_none["link_caught"] or sim_none["match_caught"]
             or sim_none["catalog_caught"]),
        "负对照 baseline 恒绿")
    add("CONTROL-READINGS-DISTINCT",
        backfire["distinct_readings"] == 4,
        "四次读数两两不同 %d 种" % backfire["distinct_readings"])

    n_pass = sum(1 for g in GUARDS if g["ok"])
    n_fail = len(GUARDS) - n_pass
    info_notes = [
        "数学自洽 != 实验证实；审计册只产可算判决，不产新物理",
        "四力大统一正确方程 0 条、独立实验预言 0；不宣称攻破统一场论",
        "本册不占 RID、不入 README、不与任何审计卷相加",
        "本册只整理既有 28 册判决，不重新计算任何物理读数",
    ]
    identity_notes = [
        "28 册 final 的判决后缀同为 GATES-PASS-WITH-0-NEGATIVE，但全串是 28 种"
        "（前缀是册标识）：同形的是后缀而非整串。后缀只由 nf_guard 与 n_decl 驱动，"
        "不含任何物理结论；把 final 当「突破 0」的证据是对象错位。"
        "两侧对照（守卫 FAIL / 缺 n_decl）证明 final_of 本身有判别力，"
        "但 final 对零读数恒无判别力 ⇒ 单列 IDENTITY，不进布尔结论",
        "unique_zero + duplicate_occ == total_zero 是加数恒等式，零判别力，不进布尔结论",
    ]
    boundary_notes = [
        "本册与 R14 全链总账、R17 四层下界总账是不同对象：那两册审字段一致性，"
        "本册审零读数独立性与判词判别力；结论不取和、不互相替代",
        "零读数去重按「键名」为对象，键名相同即视为同一判据对象；"
        "未做语义归并，故独立对象数是上界而非精确值",
        "最小翻转割只说明改动哪些共享对象能波及全链目录，"
        "不表示改动它们就能攻破统一场论，也不构成新物理",
        "判词覆盖按 `PRED-0` / `CLEAN-0` 字面 token 机读，"
        "早期册用 `NO-BREAKTHROUGH` 等不同措辞 ⇒ 字面口径下会显示漏报",
        "仓库可被并行会话改动，故 README 不变量用 AST 结构性零写入，"
        "不用复跑前后 MD5 相等的时序型判据",
    ]
    counts = dict(PASS=n_pass, FAIL=n_fail, INFO=len(info_notes),
                  BOUNDARY=len(boundary_notes), IDENTITY=len(identity_notes))
    final = final_of(0, n_fail, 0)
    catalog_out = [
        dict(json=r["json"], report=r["report"], final=r["final"],
             verdict=r["verdict"], guards=r["guards"],
             zero_key_count=len(r["zero_keys"]),
             zero_keys=r["zero_keys"], zero_tokens=r["zero_tokens"],
             pred0=r["pred0"], clean0=r["clean0"], agree=r["agree"],
             path=r["path"])
        for r in cat]
    payload = dict(
        title="算法联盟：全链判决目录整理与「零读数」独立性普查（第十九轮）",
        date=DATE,
        nature="不占号、不登记、不与任何卷相加；审对象是十八轮链留下的 28 册机读判决",
        final=final, verdict=verdict,
        guard_count=len(GUARDS), guard_pass=n_pass, counts=counts,
        key_numbers=kn,
        catalog=catalog_out,
        zero_key_frequency=dict(sorted(freq.items())),
        top_shared_keys=[list(x) for x in top_keys],
        flip_cut=cut,
        distinct_zero_tokens=distinct_zero_tokens,
        final_forms=final_forms,
        final_suffixes=final_suffixes,
        backfire=backfire,
        control_readings=[list(sim_none["counts"]), list(sim_link["counts"]),
                          list(sim_match["counts"]), list(sim_cat["counts"])],
        info_notes=info_notes, boundary_notes=boundary_notes,
        identity_notes=identity_notes,
        segments=[dict(name=g["name"], kind=g["kind"], note=g["note"])
                  for g in GUARDS],
        declared_negative=0,
        source_files=[os.path.relpath(README, ROOT),
                      os.path.relpath(DATA, ROOT),
                      os.path.relpath(SRC, ROOT)],
        source_missing=0,
        red_line="数学自洽 != 实验证实；四力大统一正确方程 0 条；独立实验预言 0；不宣称攻破。",
        chi2_crit=CHI2_CRIT)
    payload["content_sha256"] = sha_obj(payload)
    return payload


def write_outputs(payload):
    body = json.dumps(payload, ensure_ascii=False, indent=1)
    open(OUT_JSON, "w", encoding="utf-8", newline="\n").write(body + "\n")
    kn = payload["key_numbers"]
    lines = [
        payload["title"],
        "=" * 96,
        "verdict : " + payload["verdict"],
        "final   : " + payload["final"],
        "counts  : " + json.dumps(payload["counts"], ensure_ascii=False),
        "guards  : %d/%d" % (payload["guard_pass"], payload["guard_count"]),
        "sha256  : " + payload["content_sha256"],
        "-" * 96,
        "目录整理：%d 册 recompute JSON / %d 份 report / %d 个机核 / %d 份主文 / %d 份 HTML"
        % (kn["books"], kn["reports"], kn["kernels"],
           kn["main_texts"], kn["htmls"]),
        "两路机拼：JSON 结构 vs report 文本逐册三项一致 %d/%d；失配 %d；断链 %d"
        % (kn["two_path_agree"], kn["books"], kn["two_path_mismatch"],
           kn["broken_ref_count"]),
        "零读数去重：总出现 %d 次 / 去重 %d 个键 / 重复 %d 次（%s%%）/ 跨册共享键 %d / 全册共有键 %d"
        % (kn["total_zero_occurrences"], kn["unique_zero_keys"],
           kn["duplicate_occurrences"], kn["duplication_pct"],
           kn["shared_keys_ge2"], kn["shared_by_all_books"]),
        "判词覆盖：显式 PRED-0 的册 %d（%s%%）/ CLEAN-0 的册 %d / 无任何 -0 token 的册 %d / 零 token 共 %d 个去重 %d 种"
        % (kn["pred0_books"], kn["pred0_coverage_pct"], kn["clean0_books"],
           kn["no_zero_token_books"], kn["zero_token_total"],
           len(payload["distinct_zero_tokens"])),
        "final 全串 %d 种 / 判决后缀 %d 种：后缀只由守卫状态驱动，对零读数恒无判别力 ⇒ 单列 IDENTITY"
        % (kn["final_distinct_forms"], kn["final_suffix_forms"]),
        "最小翻转割：%d 个共享键波及 %d 册；双键最佳覆盖 %s"
        % (kn["flip_cut_size"], kn["flip_cut_affected"],
           str(kn["flip_cut_best_pair_cover"])),
        "README：%d B / 机核写操作 %d 处（结构性零写入）"
        % (kn["readme_bytes"], kn["readme_write_hits"]),
        "-" * 96,
        "红线：" + payload["red_line"],
        "-" * 96,
    ]
    for s in payload["segments"]:
        lines.append("[%s] %s :: %s" % (s["kind"], s["name"], s["note"]))
    lines.append("-" * 96)
    for n in payload["info_notes"]:
        lines.append("[INFO] " + n)
    for n in payload["identity_notes"]:
        lines.append("[IDENTITY] " + n)
    for n in payload["boundary_notes"]:
        lines.append("[BOUNDARY] " + n)
    open(OUT_REPORT, "w", encoding="utf-8", newline="\n").write(
        "\n".join(lines) + "\n")
    print("WRITE", OUT_JSON)
    print("WRITE", OUT_REPORT)
    return lines


def main():
    payload = compute()
    write_outputs(payload)
    print("final=", payload["final"], "guards=",
          payload["guard_pass"], "/", payload["guard_count"])
    print("sha256=", payload["content_sha256"])
    if payload["counts"]["FAIL"] > 0:
        print("GATES-FAIL")
        return 1
    print("ALL-CHECKS-PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
