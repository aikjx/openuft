# -*- coding: utf-8 -*-
"""进门闸 v8：值列的**货币裁定**——「一个数＋尾注」能不能剥（2026-10-19，只读）。

来龙去脉
  v7 偿清了写入侧的「建议档」（不再教人删列，改印可照填的相对带），并证明判决一格未动；
  误差棒那一列修到底也只出 4／462 枚可登记——其余 6 枚被**值列**挡住。本轮查值列：
  462 行的 `prediction_value` 按形状闭合分桶，逐枚裁定「剥掉尾注取那个数」这条通道该不该开。

裁定要回答的不是「能不能解析」，而是「解析出来的数以什么货币进池」
  具名靶的 χ² 池是无量纲的。`1.257e16 GeV`、`3.95e35 yr` 这一型确实含一个可解析的数，
  剥掉单位就能过门禁——过了门禁却把量纲混进无量纲池。所以本轮把「放宽剥单位」的后果**算成钱**（T5）：
  门禁自己会放行几枚、放行的是什么量纲。

本册不改任何人的 `claims.csv`、不改门禁源码、不跑 `--check`（那会重写报告对）。
产出 数据/进门闸_v8_值列货币裁定_剥尾注通道定价_2026-10-19.json ＋ 判定卷（项目根）。
"""
import collections
import hashlib
import io
import json
import os
import re
import sys
import time
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
if not os.path.isdir(os.path.join(ROOT, "openuft")):
    _up = HERE
    while _up and not os.path.isdir(os.path.join(_up, "openuft")):
        _n = os.path.dirname(_up)
        if _n == _up:
            break
        _up = _n
    if not os.path.isdir(os.path.join(_up, "openuft")):
        raise SystemExit("FATAL: 找不到 openuft 的仓根（本册须放在 源码/ 或 scratch/）")
    ROOT = _up
PROJP = os.path.join(ROOT, "openuft", "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(PROJP, "源码")
DATA = os.path.join(PROJP, "数据")
SCRATCH = os.path.join(ROOT, "scratch")
GATE_SRC = os.path.join(SRC, "靶场登记列校验_写入侧门禁.py")
BASELINE = os.path.join(DATA, "靶场登记列_违规基线.json")
V6_FACE = os.path.join(DATA, "进门闸_v6_换算工作单_修前修后ok计数预演_2026-10-19.json")
V7_FACE = os.path.join(DATA, "进门闸_v7_写入侧建议档换算补正与中立性见证_2026-10-19.json")
SYS_DIR = os.path.join(ROOT, "openuft", "01_独立体系")

INSTR_NAME = "进门闸_v8_值列货币裁定_剥尾注通道定价_2026-10-19.py"
FACE_NAME = "进门闸_v8_值列货币裁定_剥尾注通道定价_2026-10-19.json"
VOL_NAME = "判定_进门闸_v8_值列货币裁定_剥尾注通道定价_2026-10-19.md"
GATE_MD5_V7 = "e997593cd676213654fbd19d61615c76"
LAND = "--land" in sys.argv[1:]
QUIET = "--quiet" in sys.argv[1:]
OUT_DIR = DATA if LAND else SCRATCH

NUM = u"[-+]?[0-9]*\\.?[0-9]+(?:[eE][-+]?[0-9]+)?"
LEAD = re.compile(u"^\\s*(" + NUM + u")\\s*(.*)$", re.U)
LETTERS = re.compile(u"[A-Za-z]")
INTERVAL = re.compile(u"[–—~]|\\[[^\\]]*,")
EXACT_TAIL = (u"（精确）", u"(精确)", u"（exact）", u"(exact)")


class Fatal(Exception):
    pass


def md5(b):
    return hashlib.md5(b).hexdigest()


def stat(path):
    b = open(path, "rb").read()
    return {"bytes": len(b), "md5": md5(b), "crlf": b.count(b"\r\n"),
            "lf": b.count(b"\n"), "cr": b.count(b"\r")}


def load_gate():
    g = stat(GATE_SRC)
    if not (g["crlf"] == g["lf"] == g["cr"]):
        raise Fatal("门禁图非纯 CRLF：cr=%d lf=%d crlf=%d" % (g["cr"], g["lf"], g["crlf"]))
    spec = importlib.util.spec_from_file_location("G8", GATE_SRC)
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = GATE_SRC
    spec.loader.exec_module(mod)
    return mod, g


def float_ruler(s):
    """第二把尺：Python 字面量能不能吃这个串（不吃门禁自己的 parse_number）。"""
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


CONTROLS = []
C = {}


def ctl(code, title, cond, payload):
    name = code + u"｜" + title
    CONTROLS.append(code)
    C[code] = {"code": code, "name": name, "fired": bool(cond), "payload": payload}
    if not cond:
        print("  [RED] " + name)


def N(code):
    return C[code]["payload"]


def bucket(G, pv):
    """值列现串读成 (桶, 剥出的数串或 None, 尾注)。桶集必须闭合（T1）。"""
    s = (pv or "").strip()
    if not s:
        return "pv_empty", None, u""
    if G.PATH_FORM.match(s):
        return "pv_is_path", None, u""
    if G.parse_number(s) is not None:
        return "pv_parseable", None, u""
    m = LEAD.match(s)
    if not m:
        return "pv_no_leading_numeral", None, u""
    num, rest = m.group(1), m.group(2).strip()
    if not rest:
        return "pv_no_leading_numeral", None, u""
    if INTERVAL.search(rest):
        return "pv_interval", None, rest
    if re.search(NUM, rest):
        return "pv_second_numeral", None, rest
    return "pv_numeral_plus_tail", num, rest


def strip_verdict(G, num, rest, urel):
    """尾注含 ASCII 字母＝带绝对单位（或英文注）⇒ 不开；纯中文括注且声明「精确」⇒ 可剥并以 urel=0 登记。"""
    if LETTERS.search(rest):
        return "blocked_dimensional", LETTERS.search(rest) and "".join(
            re.findall(u"[A-Za-z]+", rest))
    if rest in EXACT_TAIL:
        if G.classify(num, u"0")[0] == "ok":
            return "strip_ok_and_registers", u""
        return "strip_but_not_ok", u""
    return "strip_value_only", u""


def main():
    t0 = time.time()
    G, g_stat = load_gate()
    pre_corpus = {}
    for name in sorted(os.listdir(SYS_DIR)):
        p = os.path.join(SYS_DIR, name, "claims.csv")
        if os.path.isfile(p):
            pre_corpus[p] = md5(open(p, "rb").read())

    rows, paths = G.scan_registry()
    vio = [r for r in rows if r["severity"]]
    base = json.loads(io.open(BASELINE, encoding="utf-8").read())
    added, removed = G.diff(vio, base)

    buckets = collections.Counter()
    tally = collections.Counter()
    roster = []
    detail = {}
    for r in rows:
        b, num, rest = bucket(G, r["prediction_value"])
        buckets[b] += 1
        pv = (r["prediction_value"] or "").strip()
        pu = (r["prediction_urel"] or "").strip()
        if b != "pv_empty":
            roster.append({"owner": r["owner"], "claim_id": r["claim_id"], "pv": pv,
                           "urel": pu, "bucket": b, "tail": rest})
        if b == "pv_numeral_plus_tail":
            verdict, unit = strip_verdict(G, num, rest, pu)
            tally[verdict] += 1
            detail[r["claim_id"]] = {"num": num, "tail": rest, "unit": unit,
                                     "verdict": verdict, "urel_now": pu}

    # T5：把「剥单位」真的执行一遍，看门禁自己放行几枚、放行的是什么量纲
    relax = []
    for cid, d in detail.items():
        if d["verdict"] != "blocked_dimensional":
            continue
        shape, val = G.band_form(d["urel_now"])
        rel, why = G.to_relative(shape, val, d["num"])
        cand = u"%.12g" % rel if rel is not None else None
        after = G.classify(d["num"], cand)[0] if cand else None
        relax.append({"claim_id": cid, "unit": d["unit"], "pv_stripped": d["num"],
                      "band_shape": shape, "why": why, "urel_relative": cand,
                      "gate_recount_after": after, "would_enter_pool": after == "ok"})
    relax_ok = sum(1 for x in relax if x["would_enter_pool"])
    strip_ok_ids = sorted(cid for cid, d in detail.items()
                          if d["verdict"] == "strip_ok_and_registers")

    v6 = json.loads(io.open(V6_FACE, encoding="utf-8").read())
    v7 = json.loads(io.open(V7_FACE, encoding="utf-8").read())
    v7_ok_ids = sorted(set(x["claim_id"] for x in v7["x1"]["rows10"]
                           if x["after_flag"] == "ok"))
    v6_blocked_ids = sorted(v6["blocked"]["claim_ids"])
    v6_value_debt = v6["type_counts"].get("value_unparseable", 0)
    fam_ids = set(x["claim_id"] for x in roster if x["bucket"] != "pv_parseable")
    v6_blocked_here = [cid for cid in v6_blocked_ids if cid in fam_ids]
    v6_blocked_buckets = collections.Counter(
        x["bucket"] for x in roster if x["claim_id"] in set(v6_blocked_ids))

    unparse_nonempty = (len(rows) - buckets["pv_empty"] - buckets["pv_parseable"])

    # ---------------- 控制 ----------------
    ctl("T0", u"门禁血缘：本册吃的仍是 v7 发表的那柄刀（源码未再动）",
        g_stat["md5"] == GATE_MD5_V7,
        {"gate_bytes": g_stat["bytes"], "gate_md5": g_stat["md5"], "expect": GATE_MD5_V7})

    ctl("T1", u"值列分桶闭合：%d 行分到 %d 桶、求和逐枚等于行数" % (len(rows), len(buckets)),
        sum(buckets.values()) == len(rows),
        {"rows": len(rows), "sum": sum(buckets.values()), "by_bucket": dict(buckets),
         "files": len(paths), "nonempty_roster": len(roster)})

    disagree = [(x["claim_id"], x["pv"]) for x in roster
                if (x["bucket"] == "pv_parseable") != float_ruler(x["pv"])]
    ctl("T2", u"两把尺同判可解析性：门禁 parse_number 对 Python float()（不一致 %d 枚）"
        % len(disagree),
        not disagree,
        {"pv_parseable": buckets["pv_parseable"], "pv_empty": buckets["pv_empty"],
         "unparse_nonempty": unparse_nonempty, "disagreements": disagree[:6],
         "gate_only": sorted(set(x["claim_id"] for x in roster
                                 if x["bucket"] == "pv_parseable")
                             - set(x["claim_id"] for x in roster
                                   if float_ruler(x["pv"]))),
         "python_only": sorted(set(x["claim_id"] for x in roster if float_ruler(x["pv"]))
                               - set(x["claim_id"] for x in roster
                                     if x["bucket"] == "pv_parseable"))})

    fam = [x for x in roster if x["bucket"] == "pv_numeral_plus_tail"]
    ctl("T3", u"「一个数＋尾注」逐枚点名（%d 枚）：判定分派求和＝该族枚数" % len(fam),
        sum(tally.values()) == len(fam),
        {"n_family": len(fam), "by_verdict": dict(tally),
         "strip_ok_ids": strip_ok_ids,
         "roster": [{"claim_id": x["claim_id"], "pv": x["pv"], "urel": x["urel"],
                     "unit_or_tail": detail[x["claim_id"]]["unit"] or detail[x["claim_id"]]["tail"],
                     "verdict": detail[x["claim_id"]]["verdict"]} for x in fam]})

    inter = set(strip_ok_ids) & set(v7_ok_ids)
    ctl("T4", u"剥尾注新落 ok %d 枚（%s），与 v7 换算落 ok %d 枚交集 %d 枚 ⇒ 两通道并集 %d 枚"
        % (len(strip_ok_ids), u"、".join(strip_ok_ids) or u"无",
           len(v7_ok_ids), len(inter), len(set(strip_ok_ids) | set(v7_ok_ids))),
        (not inter) and len(v7_ok_ids) == v7["x2"]["gate_self_recount"]
        and len(strip_ok_ids) == tally.get("strip_ok_and_registers", -1),
        {"strip_new_ok": len(strip_ok_ids), "strip_ok_ids": strip_ok_ids,
         "v7_ok_ids": v7_ok_ids, "intersection": sorted(inter),
         "union": sorted(set(strip_ok_ids) | set(v7_ok_ids)),
         "rows_total": len(rows)})

    ctl("T5", u"放宽的代价算成钱：剥掉绝对单位并按 v7 口径换算带后，门禁自己放行 %d／%d 枚（量纲进无量纲池）"
        % (relax_ok, len(relax)),
        len(relax) > 0 and all(x["unit"] for x in relax),
        {"candidates": relax, "ok_if_relaxed": relax_ok,
         "units_seen": sorted(set(x["unit"] for x in relax)),
         "not_entered": [x["claim_id"] for x in relax if not x["would_enter_pool"]]})

    ctl("T6", u"与 v5/v6/v7 分家：本册非空不可解析 %d 枚 ⊇ v6 主债 value_unparseable %d 枚；v6 值侧挡道 %d 枚逐枚落在本册桶里（%s）"
        % (unparse_nonempty, v6_value_debt, len(v6_blocked_ids),
           u"、".join(u"%s:%d" % (k, v) for k, v in sorted(v6_blocked_buckets.items()))),
        len(v6_blocked_here) == len(v6_blocked_ids)
        and sum(v6_blocked_buckets.values()) == len(v6_blocked_ids)
        and len(v7_ok_ids) == 4,
        {"this_unparse_nonempty": unparse_nonempty, "v6_value_debt": v6_value_debt,
         "v6_blocked_ids": v6_blocked_ids, "v6_blocked_here": v6_blocked_here,
         "v6_blocked_buckets": dict(v6_blocked_buckets),
         "v7_yield_ok": v7["x2"]["gate_self_recount"]})

    post_corpus = {}
    for name in sorted(os.listdir(SYS_DIR)):
        p = os.path.join(SYS_DIR, name, "claims.csv")
        if os.path.isfile(p):
            post_corpus[p] = md5(open(p, "rb").read())
    changed = [p for p in pre_corpus if pre_corpus[p] != post_corpus.get(p)]
    ctl("T7", u"中立性（只读）：%d 份 claims.csv 图像前后逐份相同（改动 %d 份）；门禁图＝v7 发表态；违规名册 %d 条、新增 %d／已消除 %d 与 v7 卷同读数"
        % (len(pre_corpus), len(changed), len(vio), len(added), len(removed)),
        (not changed) and g_stat["md5"] == GATE_MD5_V7
        and len(added) == 106 and len(removed) == 0 and len(vio) == 107,
        {"files": len(pre_corpus), "changed": changed, "vio_keys": len(vio),
         "added": len(added), "removed": len(removed)})

    fixtures = []
    for pv, pu, want in ((u"1.257e16 GeV", u"±20%（文献跨度）", "blocked_dimensional"),
                         (u"0（精确）", u"无", "strip_ok_and_registers"),
                         (u"0（approx）", u"无", "blocked_dimensional"),
                         (u"0.2298–0.2318", u"", "pv_interval"),
                         (u"07_计算复现/源码/x.py", u"", "pv_is_path"),
                         (u"无", u"", "pv_no_leading_numeral")):
        b, num, rest = bucket(G, pv)
        got = strip_verdict(G, num, rest, pu)[0] if b == "pv_numeral_plus_tail" else b
        fixtures.append({"pv": pv, "bucket": b, "verdict": got, "want": want,
                         "match": got == want})
    ctl("T8", u"夹具：%d 串各落已知答案的桶／判定（含两枚反对照：`（approx）` 有字母即不开、路径整串不算数）"
        % len(fixtures),
        len(fixtures) == 6 and all(f["match"] for f in fixtures),
        {"fixtures": fixtures,
         "misses": [f for f in fixtures if not f["match"]]})

    dirty = [str(v)[:24] for x in roster for v in (x["pv"], x["urel"], x["tail"]) if u"|" in v]
    ctl("T9", u"卫生：名册与卷表格不吃脏行（含竖线的文本 %d 处）" % len(dirty),
        not dirty, {"hits": dirty[:4], "roster_n": len(roster)})

    leaked = [c for c in CONTROLS if re.search(u"%[-+ 0-9.]*[sdf]", C[c]["name"])]
    ctl("Z0", u"题面卫生：全部控制题名里不留未替换的占位符", not leaked,
        {"controls": len(CONTROLS), "leaked": leaked[:4]})

    s_src = os.path.join(SCRATCH, INSTR_NAME)
    l_src = os.path.join(SRC, INSTR_NAME)
    if not (os.path.isfile(s_src) and os.path.isfile(l_src)):
        raise Fatal("W1 需要两把尺（scratch 源与 源码/ 落盘像）——本册的产物不可引用")
    sa = open(s_src, "rb").read()
    lb = open(l_src, "rb").read()
    self_b = open(os.path.abspath(__file__), "rb").read()
    eol_equal = sa.replace(b"\r\n", b"\n") == lb.replace(b"\r\n", b"\n")
    cr_diff = (sa.count(b"\r\n"), lb.count(b"\r\n"))
    mode = u"--land" if LAND else u"预跑"
    fired_w1 = eol_equal and ((lb == self_b) if LAND
                              else (sa == lb) == (cr_diff[0] == cr_diff[1]))
    ctl("W1", u"落盘的刀＝手里的刀：`源码/` 仪器与 scratch 源 EOL 归一后逐字同（两图 CRLF %d／%d，%s）"
        % (cr_diff[0], cr_diff[1], mode), fired_w1,
        {"scratch_bytes": len(sa), "landed_bytes": len(lb),
         "scratch_crlf": cr_diff[0], "landed_crlf": cr_diff[1],
         "scratch_md5": md5(sa), "landed_md5": md5(lb),
         "eol_equal": eol_equal, "mode": mode})

    red = [c for c in CONTROLS if not C[c]["fired"]]
    face = {
        "instrument": INSTR_NAME,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rc": 0 if not red else 1,
        "controls": [C[c] for c in CONTROLS],
        "controls_total": len(CONTROLS),
        "controls_fired": len(CONTROLS) - len(red),
        "controls_red": red,
        "gate": g_stat,
        "rows_total": len(rows),
        "files": len(paths),
        "buckets": dict(buckets),
        "verdicts": dict(tally),
        "strip_ok_ids": strip_ok_ids,
        "relax": relax,
        "relax_ok": relax_ok,
        "roster": roster,
        "vio_keys": len(vio), "added": len(added), "removed": len(removed),
        "v6_value_debt": v6_value_debt, "v6_blocked_ids": v6_blocked_ids,
        "v6_blocked_buckets": dict(v6_blocked_buckets),
        "v7_ok_ids": v7_ok_ids,
    }

    fb = os.path.join(OUT_DIR, FACE_NAME)
    raw = json.dumps(face, ensure_ascii=False, indent=2).encode("utf-8")
    open(fb, "wb").write(raw)
    if open(fb, "rb").read() != raw:
        raise Fatal("面写后回读与内存图不一致——本次产物不得引用")
    F = dict(face, face_bytes=len(raw), face_md5=md5(raw),
             instrument_bytes=len(self_b), instrument_md5=md5(self_b))
    vol = render_vol(F)
    for tok in (u"%s", u"%d", u"%.12g"):
        if tok in vol:
            raise Fatal(u"卷里有未替换的占位符 %s" % tok)
    vb = os.path.join(PROJP if LAND else OUT_DIR, VOL_NAME)
    vraw = vol.replace(u"\r\n", u"\n").replace(u"\n", u"\r\n").encode("utf-8")
    if not (vraw.count(b"\r") == vraw.count(b"\n") == vraw.count(b"\r\n")):
        raise Fatal("卷不是纯 CRLF")
    open(vb, "wb").write(vraw)
    if open(vb, "rb").read() != vraw:
        raise Fatal("卷写后回读与内存图不一致——本次产物不得引用")

    on_vol = open(vb, "rb").read().decode("utf-8")
    on_face = open(fb, "rb").read()
    m = re.search(u"面 `%s` (\\d+) B／md5 `([0-9a-f]{32})`；仪器 `%s` (\\d+) B／md5 `([0-9a-f]{32})`"
                  % (re.escape(FACE_NAME), re.escape(INSTR_NAME)), on_vol)
    if not m:
        raise Fatal("卷里找不到它自己印的产物钉行——钉没落进盘上图像")
    if ((int(m.group(1)), m.group(2)) != (len(on_face), md5(on_face))
            or (int(m.group(3)), m.group(4)) != (len(self_b), md5(self_b))):
        raise Fatal(u"卷印的钉与盘上图像不符——本次产物不得引用")

    if not QUIET:
        print("=" * 78)
        for c in CONTROLS:
            print("  [%s] %s" % ("OK " if C[c]["fired"] else "RED", C[c]["name"]))
        print("  值列分桶 %s" % u"、".join(u"%s %d" % (k, v) for k, v in sorted(buckets.items())))
        print("  剥尾注：可剥且落 ok %d 枚（%s）｜绝对单位判不开 %d 枚｜若放宽则门禁放行 %d 枚"
              % (len(strip_ok_ids), u"、".join(strip_ok_ids) or u"无", len(relax), relax_ok))
        print("  控制 %d/%d 点火，rc=%d；面 %d B（%s）｜卷 %d B（%s）｜用时 %.2fs"
              % (face["controls_fired"], face["controls_total"], face["rc"],
                 len(raw), md5(raw), len(vraw), md5(vraw), time.time() - t0))
    return face["rc"]


def render_vol(F):
    A = []
    a = A.append
    b = F["buckets"]
    t3, t5, t6, t7, t8 = N("T3"), N("T5"), N("T6"), N("T7"), N("T8")
    a(u"# 判定 · 进门闸 v8：值列的货币裁定——「剥尾注」这条通道该不该开（2026-10-19）\n\n")
    a(u"判定时刻：2026-10-19。仪器 `源码/%s`，面 `数据/%s`，控制 %d/%d 点火，rc=%d。\n"
      % (INSTR_NAME, FACE_NAME, F["controls_fired"], F["controls_total"], F["rc"]))
    a(u"产物钉（面先落盘、卷后钉）：面 `%s` %d B／md5 `%s`；仪器 `%s` %d B／md5 `%s`。"
      u"本卷自己的尺寸由记忆卡与登记行钉。\n"
      % (FACE_NAME, F["face_bytes"], F["face_md5"], INSTR_NAME,
         F["instrument_bytes"], F["instrument_md5"]))
    a(u"本册不改任何体系的 `claims.csv`、不改门禁源码、不跑 `--check`；判决面一格未动（T7）。\n\n")

    a(u"## 一、这一轮问的是值列\n\n")
    a(u"v7 把误差棒那一列修到底，也只出 4／%d 枚可登记，其余 6 枚被**值列**挡住。本轮不问「能不能解析」，"
      u"而问「解析出来的数以什么货币进池」：值列里有一族长得像「一个数＋尾注」（`1.257e16 GeV`、`0（精确）`），"
      u"剥掉尾注那个数就过门禁。具名靶的 χ² 池是无量纲的，所以剥它是一笔**货币**交易，不是排版问题。\n\n"
      % F["rows_total"])

    a(u"## 二、值列分桶（%d 行闭合，T1）\n\n" % F["rows_total"])
    a(u"| 桶 | 枚数 | 是什么 |\n| --- | --- | --- |\n")
    for k, why in (("pv_empty", u"值列空（未登记）"),
                   ("pv_parseable", u"值列本身可解析"),
                   ("pv_is_path", u"整串是路径——该住推导/证据列"),
                   ("pv_no_leading_numeral", u"散文开头，没有先行的数"),
                   ("pv_second_numeral", u"一个数之后还有第二个数（多数值行）"),
                   ("pv_interval", u"区间／范围写法"),
                   ("pv_numeral_plus_tail", u"一个数＋尾注（本轮裁定对象）")):
        a(u"| %s | %d | %s |\n" % (k, b.get(k, 0), why))
    a(u"非空而不可解析 %d 枚——这才是登记瓶颈：%d 行两列皆空（未登记），只有 %d 行的值列本身可解析（T2）。"
      u"两把尺（门禁 `parse_number` 与 Python `float()`）对可解析性逐枚同判：不一致 %d 枚；"
      u"有理数写法只由门禁认（`3/8` 这一型），本轮语料里没有出现，所以两把尺同值不是巧合而是空集同值，"
      u"已点名（T2 payload 的 gate_only／python_only 两列皆空）。\n\n"
      % (t2_unparseable(F), b["pv_empty"], b["pv_parseable"],
         len(N("T2")["disagreements"])))

    a(u"## 三、那一族「一个数＋尾注」逐枚点名（%d 枚）\n\n" % b["pv_numeral_plus_tail"])
    a(u"| claim_id | 现串 | 剥出的数 | 尾注/单位 | 判定 |\n| --- | --- | --- | --- | --- |\n")
    for x in t3["roster"]:
        a(u"| %s | %s | %s | %s | %s |\n" % (x["claim_id"], x["pv"], x["pv"].split()[0],
                                             x["unit_or_tail"], x["verdict"]))
    a(u"分派：绝对单位判不开 %d 枚、量纲中性且声明精确可剥并落 `ok` %d 枚（%s）、"
      u"可剥但带仍缺 %d 枚；求和＝该族枚数（T3）。\n\n"
      % (t3["by_verdict"].get("blocked_dimensional", 0),
         t3["by_verdict"].get("strip_ok_and_registers", 0),
         u"、".join(F["strip_ok_ids"]) or u"无",
         t3["by_verdict"].get("strip_value_only", 0)))

    a(u"## 四、若把「剥单位」放宽，代价算成钱（门禁自己复算）\n\n")
    a(u"| claim_id | 单位 | 剥出的数 | 带形状 | 换算后相对带 | 门禁复算档 | 进池 |\n"
      u"| --- | --- | --- | --- | --- | --- | --- |\n")
    for x in t5["candidates"]:
        a(u"| %s | %s | %s | %s | %s | %s | %s |\n"
          % (x["claim_id"], x["unit"], x["pv_stripped"], x["band_shape"],
             x["urel_relative"] or u"—", x["gate_recount_after"] or u"—",
             u"会" if x["would_enter_pool"] else u"不会"))
    a(u"门禁**自己**不认量纲：剥完再按 v7 口径把带换算成相对数，%d／%d 枚被门禁判成 `ok` 放进池里"
      u"（出现的单位：%s）。⇒ 值列的 `non_numeric` 在这一族上不是刁难，是在替 χ² 池挡量纲。"
      u"所以本轮不把剥单位接进门禁；带单位的值要进池，须由属主先把它折算成无量纲声明。\n\n"
      % (F["relax_ok"], len(t5["candidates"]), u"、".join(t5["units_seen"])))

    a(u"## 五、裁定规则与夹具（宽窄由对象实际形状定）\n\n")
    a(u"规则两条：尾注含 ASCII 字母＝带绝对单位或英文注⇒不开；尾注是中文括注且声明「精确」⇒值可剥并以 "
      u"`urel=0` 登记（整数靶允许 0，这是门禁自己的口径，不是本册新发明的豁免）。\n")
    a(u"| 夹具串 | 读成的桶 | 规则给的判定 | 期望 | 相符 |\n| --- | --- | --- | --- | --- |\n")
    for f in t8["fixtures"]:
        a(u"| %s | %s | %s | %s | %s |\n" % (f["pv"], f["bucket"], f["verdict"], f["want"],
                                             u"是" if f["match"] else u"否"))
    a(u"两枚反对照各管一边：`0（approx）` 无量纲却有 ASCII 字母，规则判「不开」——这是**已知过窄**，"
      u"本轮接受，因为该族只有 4 枚且全部点名（§三），过窄不改变产出集；"
      u"`07_计算复现/源码/x.py` 以数字开头，若不先按整串路径判形，就会被剥成一个假数——"
      u"路径优先那一步走在校验首位数的尺之前（与 v7 §六同一条教训）。\n\n")

    a(u"## 六、与 v5／v6／v7 三本账的分家\n\n")
    a(u"本册「值列非空不可解析」%d 枚 ⊇ v5/v6 主债口径 `value_unparseable` %d 枚；"
      u"v6「值侧挡道」%d 枚逐枚落在本册桶里（%s），一枚不漏（T6）。"
      u"分家原因同 v7：v5 给每行只派一个主债，指针与散文优先，所以值列里带数的路径行不计进 `value_unparseable`。"
      u"标签的宽窄不构成矛盾，产出集的差异才构成矛盾——那一条由 T6 的逐枚落桶拦着。\n\n"
      % (t6["this_unparse_nonempty"], t6["v6_value_debt"], len(t6["v6_blocked_ids"]),
         u"、".join(u"%s %d" % (k, v) for k, v in sorted(F["v6_blocked_buckets"].items()))))

    a(u"## 七、中立性（本册只读）\n\n")
    a(u"门禁图未动：`靶场登记列校验_写入侧门禁.py` %d B／md5 `%s`＝v7 发表态（T0）。"
      u"%d 份 `claims.csv` 图像在判定前后逐份相同（改动 %d 份）；违规名册 %d 条、"
      u"相对基线新增 %d／已消除 %d，与 v7 卷 §二 同读数 ⇒ 语料在本册期间未移动。\n\n"
      % (F["gate"]["bytes"], F["gate"]["md5"], t7["files"], len(t7["changed"]),
         t7["vio_keys"], t7["added"], t7["removed"]))

    a(u"## 八、上限与去向\n\n")
    a(u"两条通道都走到底：v7 换算落 ok %d 枚 ＋ 本册剥尾注落 ok %d 枚（%s）＝ 全仓可登记上限 %d／%d，"
      u"两通道产出集不相交（交集 %d 枚，T4），且全部落在 S02 一个体系的同一族靶上。\n"
      % (len(F["v7_ok_ids"]), len(F["strip_ok_ids"]), u"、".join(F["strip_ok_ids"]) or u"无",
         len(F["v7_ok_ids"]) + len(F["strip_ok_ids"]), F["rows_total"],
         len(set(F["strip_ok_ids"]) & set(F["v7_ok_ids"]))))
    a(u"剩下的账不是排版能还的：%d 行未登记、%d 行值列是路径、%d 行是散文开头、"
      u"%d 行是多数值/区间。未偿付：B `ineq_bare` 档位待治理裁定；C 路径与散文两族要的是列语义分工，"
      u"本册不给编造的数；D 基线欠登记 %d 条 OPEN；E 新债——带绝对单位的值若要进池须先立「量纲折算」判据"
      u"（v4 口径没有这一步，硬套就是把换算尺放宽成「有个数就行」）。\n\n"
      % (b["pv_empty"], b["pv_is_path"], b["pv_no_leading_numeral"],
         b["pv_second_numeral"] + b["pv_interval"], F["added"]))
    a(u"本轮对「完成统一场论」这句话的净贡献是一条**否定**读数："
      u"可判决样本集的上限是 %d／%d 且集中于单一体系的同一枚靶 ⇒ 进门闸在现语料上给不出有判决力的样本，"
      u"χ² 层的缺口不在阈值与货币口径，在登记本身。\n\n"
      % (len(F["v7_ok_ids"]) + len(F["strip_ok_ids"]), F["rows_total"]))

    a(u"## 九、复算\n\n")
    a(u"```powershell\n")
    a(u"cd openuft/04_公共成果/本项目_全维自洽与归一化\n")
    a(u"PYTHONIOENCODING=utf-8 python -B 源码/%s --land\n" % INSTR_NAME)
    a(u"```\n")
    w1 = N("W1")
    a(u"落刀自证（W1）：`scratch` 源 %d B／CRLF %d 与 `源码/` 落盘像 %d B／CRLF %d，EOL 归一后逐字同；"
      u"本卷跑的是 `源码/` 里那柄刀（%s）。上面那行产物钉由驱动器在卷落盘后从**盘上的卷**正则找回、"
      u"再量盘上的面与仪器，一枚不符即 FATAL。\n"
      % (w1["scratch_bytes"], w1["scratch_crlf"], w1["landed_bytes"], w1["landed_crlf"],
         u"落盘像＝正在运行的文件" if w1["mode"] == u"--land" else u"预跑，落盘像只作对照"))
    return u"".join(A)


def t2_unparseable(F):
    bb = F["buckets"]
    return F["rows_total"] - bb["pv_empty"] - bb["pv_parseable"]


if __name__ == "__main__":
    sys.exit(main())
