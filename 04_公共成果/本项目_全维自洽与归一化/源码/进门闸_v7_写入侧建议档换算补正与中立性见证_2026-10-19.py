# -*- coding: utf-8 -*-
"""进门闸 v7：写入侧「建议去向」的换算补正 + **中立性见证**（2026-10-19）。

来龙去脉
  v5 测出写入侧门禁的建议档是**破坏性的**（`留空或填数值`／`一并清空两列`）——照它做会把
  违规行搬进合法的 `empty`，棘轮反而奖励删列。v6 把 10 枚可换算写法算成相对带、实测
  修前 ok 0／462 → 修后 ok 4／462。本轮把这条换算口径补进门禁自己的 `advice()`（未偿付 A）。

本轮的两件事
  ① 中立性：门禁是判决的单一真源，改它必须证明「判决没动，只动了文案」。
     取发表图（`git show HEAD:` 的 EOL 归一像 = `scratch/gate_r74_head.py`）当 PRE，
     现盘图当 POST，逐行 (flag, severity, reason)、违规键集、基线差分、
     以及判决函数**源码段**逐字比对。
  ② 换算补正有牙：建议档印出的相对带须与 v6 工作单、v4 面定价三方逐枚同值；
     换算后落不下 ok 的行点名值列；词表外/指针行保持原文案（越权控制）；
     同一条声明写三种货币出三个数（期望由夹具字面量自己算）。

单一真源
  判决与扫描：`靶场登记列校验_写入侧门禁.py`（PRE 图 = `scratch/gate_r74_head.py`）；
  形状词表对照：`进门闸_v4_….py` 的 `read_band`；
  跨轮一致性：`数据/进门闸_v6_逐行换算工作单_2026-10-19.csv` 与 v6 面——两者的尺寸/md5
  先从 v6 判定卷**现读**为钉，再与盘上图像比。
本册不改任何体系的 claims.csv，也不改写违规基线。

产出
  数据/进门闸_v7_写入侧建议档换算补正与中立性见证_2026-10-19.json  （面，LF）
  判定_进门闸_v7_写入侧建议档换算补正与中立性见证_2026-10-19.md      （卷，CRLF）
"""
import ast
import collections
import csv
import difflib
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
if not os.path.isdir(os.path.join(ROOT, "openuft")):
    # 本册也在 scratch 里预跑（未落库）：向上找到真正装着 openuft 的那一层
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
PRE_HEAD = os.path.join(SCRATCH, "gate_r74_head.py")
V4_SRC = os.path.join(SRC, "进门闸_v4_误差棒货币裁定_绝对与相对双向命中_2026-10-18.py")
V6_FACE = os.path.join(DATA, "进门闸_v6_换算工作单_修前修后ok计数预演_2026-10-19.json")
V6_CSV = os.path.join(DATA, "进门闸_v6_逐行换算工作单_2026-10-19.csv")
V6_VOL = os.path.join(PROJP, "判定_进门闸_v6_换算工作单_修前修后ok计数预演_2026-10-19.md")
REPORT_MD = os.path.join(DATA, "靶场登记列校验.md")
GIT_REL = "04_公共成果/本项目_全维自洽与归一化/源码/靶场登记列校验_写入侧门禁.py"

INSTR_NAME = "进门闸_v7_写入侧建议档换算补正与中立性见证_2026-10-19.py"
FACE_NAME = "进门闸_v7_写入侧建议档换算补正与中立性见证_2026-10-19.json"
VOL_NAME = "判定_进门闸_v7_写入侧建议档换算补正与中立性见证_2026-10-19.md"
LAND = "--land" in sys.argv[1:]
QUIET = "--quiet" in sys.argv[1:]
OUT_DIR = DATA if LAND else SCRATCH

FMT = "%.12g"
DESTRUCTIVE = (u"留空", u"一并清空")
VOCAB = ("empty", "pointer", "percent", "pm_abs", "ineq_abs", "ineq_bare",
         "bare_number", "prose_only")
JUDGES = ("parse_number", "classify", "scan_one", "scan_registry",
          "scan_out_of_scope", "key_of", "load_baseline", "violations",
          "diff", "run_selftest", "SELFTEST_ROWS", "SUGGESTION", "SEVERITY",
          "UFT3_COLS")


class Fatal(Exception):
    pass


def md5(b):
    return hashlib.md5(b).hexdigest()


def stat(path):
    b = open(path, "rb").read()
    return {"bytes": len(b), "md5": md5(b), "crlf": b.count(b"\r\n"),
            "lf": b.count(b"\n"), "cr": b.count(b"\r")}


def load(tag, path, fake_file=None):
    src = open(path, "rb").read().decode("utf-8")
    mod = types.ModuleType(tag)
    mod.__file__ = fake_file or os.path.abspath(path)
    sys.modules[tag] = mod
    exec(compile(src, os.path.abspath(path), "exec"), mod.__dict__)
    return mod


def seg_of(raw_bytes, name):
    """按名字取该顶层定义的源码段（判决面逐字比对的尺）。"""
    src = raw_bytes.decode("utf-8")
    for node in ast.parse(src).body:
        nm = getattr(node, "name", None)
        if nm == name:
            return ast.get_source_segment(src, node)
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.get_source_segment(src, node)
    return None


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


# ---------------------------------------------------------------------------
# 一、PRE／POST 两幅门禁图
# ---------------------------------------------------------------------------
def load_gates():
    g, p = stat(GATE_SRC), stat(PRE_HEAD)
    for nm, s in (("POST", g), ("PRE", p)):
        if not (s["crlf"] == s["lf"] == s["cr"]):
            raise Fatal("%s 门禁图非纯 CRLF：cr=%d lf=%d crlf=%d"
                        % (nm, s["cr"], s["lf"], s["crlf"]))
    head = subprocess.run(["git", "show", "HEAD:" + GIT_REL],
                          cwd=os.path.join(ROOT, "openuft"),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if head.returncode != 0:
        raise Fatal("git show HEAD 取不到发表图：%s"
                    % head.stderr.decode("utf-8", "replace").strip()[:200])
    hb = head.stdout
    eol_delta = p["bytes"] - len(hb)
    pre_raw = open(PRE_HEAD, "rb").read()
    ctl("P0", u"发表图血缘：PRE 快照 = `git show HEAD:` 的 EOL 归一像，字节差恰为 PRE 的 CRLF 数",
        hb.replace(b"\r\n", b"\n") == pre_raw.replace(b"\r\n", b"\n")
        and eol_delta == p["crlf"],
        {"head_bytes": len(hb), "head_md5": md5(hb),
         "pre_snapshot_bytes": p["bytes"], "pre_snapshot_md5": p["md5"],
         "pre_crlf": p["crlf"], "eol_delta": eol_delta,
         "post_bytes": g["bytes"], "post_md5": g["md5"], "post_crlf": g["crlf"]})
    return (load("gate_pre_v7", PRE_HEAD, fake_file=GATE_SRC),
            load("gate_post_v7", GATE_SRC),
            load("v4_r7", V4_SRC), p, g)


def pins_from_v6_volume():
    txt = open(V6_VOL, "rb").read().decode("utf-8")
    mf = re.search(u"面 `数据/[^`]+`，(\\d+) B，md5 `([0-9a-f]{32})`", txt)
    mc = re.search(u"工作单 `数据/[^`]+`（(\\d+) B，(\\d+) 行，md5 `([0-9a-f]{32})`", txt)
    if not mf or not mc:
        raise Fatal("v6 判定卷没印出面/工作单的钉（面 %s／工作单 %s）"
                    % (bool(mf), bool(mc)))
    return {"face_bytes": int(mf.group(1)), "face_md5": mf.group(2),
            "csv_bytes": int(mc.group(1)), "csv_rows": int(mc.group(2)),
            "csv_md5": mc.group(3)}


# ---------------------------------------------------------------------------
# 二、中立性
# ---------------------------------------------------------------------------
def neutrality(PRE, POST):
    rows_pre, paths_pre = PRE.scan_registry()
    rows_post, paths_post = POST.scan_registry()
    same = (len(rows_pre) == len(rows_post)
            and all((r["owner"], r["claim_id"], r["flag"], r["severity"], r["reason"])
                    == (s["owner"], s["claim_id"], s["flag"], s["severity"], s["reason"])
                    for r, s in zip(rows_pre, rows_post)))
    ctl("N1", u"逐行中立：PRE/POST 对 %d 文件的 %d 行给出同一 (flag, severity, reason)"
        % (len(paths_post), len(rows_post)), same,
        {"rows_pre": len(rows_pre), "rows_post": len(rows_post),
         "files_pre": len(paths_pre), "files_post": len(paths_post),
         "owners_post": len(set(r["owner"] for r in rows_post)),
         "by_flag_post": dict(sorted(collections.Counter(
             r["flag"] for r in rows_post).items()))})

    vio_pre, vio_post = PRE.violations(rows_pre), POST.violations(rows_post)
    kpre = set(PRE.key_of(r) for r in vio_pre)
    kpost = set(POST.key_of(r) for r in vio_post)
    ctl("N2", u"违规键集中立：两幅图的 key_of 集合逐枚相同（棘轮键无从移动）",
        kpre == kpost and len(kpost) == len(vio_post),
        {"vio_pre": len(vio_pre), "vio_post": len(vio_post), "keys": len(kpost),
         "only_pre": sorted(kpre - kpost)[:3], "only_post": sorted(kpost - kpre)[:3]})

    base = POST.load_baseline()
    if base is None:
        raise Fatal("基线文件读不到——差分无从谈起")
    bk = set(base.get("violations", {}).keys())
    dpre, dpost = PRE.diff(vio_pre, base), POST.diff(vio_post, base)
    independent = sorted(kpost - bk)
    ctl("N3", u"基线差分中立：新增/已消除两数 PRE=POST，且等于「违规键集减基线键集」（第三把尺现算）",
        list(dpre[0]) == list(dpost[0]) and list(dpre[1]) == list(dpost[1])
        and list(dpost[0]) == independent,
        {"baseline_count": len(bk), "vio_keys": len(kpost),
         "added_pre": len(dpre[0]), "added_post": len(dpost[0]),
         "removed_pre": len(dpre[1]), "removed_post": len(dpost[1]),
         "independent_added": len(independent),
         "baseline_updated_utc": base.get("updated_utc")})

    pre_src = open(PRE_HEAD, "rb").read()
    post_src = open(GATE_SRC, "rb").read()
    moved = [n for n in JUDGES if seg_of(pre_src, n) != seg_of(post_src, n)]
    missing = [n for n in JUDGES if seg_of(post_src, n) is None]
    ctl("N4", u"判决面源码逐字相同：%d 个判决/扫描/基线/自检定义的源码段 PRE=POST（搬动 %d 个）"
        % (len(JUDGES), len(moved)), not moved and not missing,
        {"judges": list(JUDGES), "moved": moved, "missing": missing})

    a = pre_src.decode("utf-8").split(u"\r\n")
    b = post_src.decode("utf-8").split(u"\r\n")
    bs = [i for i, l in enumerate(b) if l.startswith(u"# 一·B、")]
    be = [i for i, l in enumerate(b) if l.startswith(u"# 一、单一真源")]
    if len(bs) != 1 or len(be) != 1 or be[0] <= bs[0]:
        raise Fatal("POST 图里换算通道的边界读不出来（一·B %d 处、单一真源 %d 处）"
                    % (len(bs), len(be)))
    region = set(range(bs[0] - 1, be[0]))          # 分隔线也算进通道
    call = [l for l in b if l.strip() == u"advice(r)))"]
    if len(call) != 1:
        raise Fatal("POST 渲染处的 advice 调用行应有 1 行，实得 %d" % len(call))
    allowed_single = set((u"import re", call[0]))
    dels, adds = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag in ("delete", "replace"):
            dels += a[i1:i2]
        if tag in ("insert", "replace"):
            adds += [(j, b[j]) for j in range(j1, j2)]
    outside = [(j, l[:56]) for j, l in adds if j not in region and l not in allowed_single]
    in_region = sum(1 for j, l in adds if j in region)
    wiring = sum(1 for j, l in adds if j not in region and l in allowed_single)
    ctl("N5", u"改动面封闭：删除仅 %d 行（渲染处取旧建议的那一行）；新增 %d 行＝换算通道内 %d 行"
        u"＋接线 %d 行（`import re` 与渲染处），通道外 %d 行"
        % (len(dels), len(adds), in_region, wiring, len(outside)),
        len(dels) == 1 and dels[0].strip() == u'SUGGESTION.get(r["flag"], "—")))'
        and len(adds) == len(b) - len(a) + 1 and not outside
        and in_region + wiring == len(adds),
        {"lines_pre": len(a), "lines_post": len(b), "deleted": dels,
         "added_n": len(adds), "in_region": in_region, "wiring": wiring,
         "region_lines": len(region), "region": [bs[0], be[0]],
         "outside": outside[:6]})
    return rows_post, kpost, dpost, len(bk)


# ---------------------------------------------------------------------------
# 三、换算补正：与 v6 工作单／v4 面三方一致
# ---------------------------------------------------------------------------
def advice_channels(PRE, POST, V4, rows, pins):
    fb, cb = stat(V6_FACE), stat(V6_CSV)
    ctl("X0", u"v6 已发表产物未被移动：盘上图像逐位等于 v6 判定卷现读的钉",
        fb["bytes"] == pins["face_bytes"] and fb["md5"] == pins["face_md5"]
        and cb["bytes"] == pins["csv_bytes"] and cb["md5"] == pins["csv_md5"],
        dict(pins, face_on_disk=fb["md5"], face_on_disk_bytes=fb["bytes"],
             csv_on_disk=cb["md5"], csv_on_disk_bytes=cb["bytes"]))

    with open(V6_CSV, encoding="utf-8-sig", newline="") as fh:
        order = list(csv.DictReader(fh))
    conv = {r["claim_id"]: r for r in order if (r[u"换算后相对带"] or "").strip()}
    face6 = json.load(open(V6_FACE, encoding="utf-8"))
    blocked6 = set(face6["blocked"]["claim_ids"])
    v4diff = {d["claim_id"]: d for d in face6["v4_cross_check"]["diffs"]}
    by_id = {}
    for r in rows:
        by_id.setdefault(r["claim_id"], []).append(r)

    rows10, mismatch = [], []
    for cid, orow in sorted(conv.items()):
        rr = by_id.get(cid) or []
        if len(rr) != 1:
            mismatch.append([cid, "门禁扫描读到 %d 行（期望 1）" % len(rr)])
            continue
        row = rr[0]
        shape, num = POST.band_form(row["prediction_urel"])
        rel, why = POST.to_relative(shape, num, row["prediction_value"])
        printed = FMT % rel if rel is not None else None
        if printed != orow[u"换算后相对带"] or shape != orow[u"形状"]:
            mismatch.append([cid, shape, orow[u"形状"], printed, orow[u"换算后相对带"]])
        after = POST.classify(row["prediction_value"], printed)[0] if printed else None
        rows10.append({"claim_id": cid, "owner": row["owner"], "shape": shape,
                       "urel": row["prediction_urel"][:40],
                       "pv": row["prediction_value"][:24],
                       "rel_printed": printed, "csv_rel": orow[u"换算后相对带"],
                       "csv_shape": orow[u"形状"], "after_flag": after,
                       "csv_after_flag": orow[u"修后flag"],
                       "v4_urel_B": v4diff.get(cid, {}).get("v4_urel_B"),
                       "advice": POST.advice(row)})
    ctl("X1", u"三方一致：门禁现算的形状与相对带串逐枚复现 v6 工作单的 %d 行（工作单全文 %d 行＝卷钉 %d 行）"
        % (len(conv), len(order), pins["csv_rows"]),
        len(order) == pins["csv_rows"] and len(conv) == len(rows10) == 10 and not mismatch,
        {"csv_conv_rows": len(conv), "csv_total": len(order), "checked": len(rows10),
         "mismatch": mismatch[:4]})

    gate_ok = sum(1 for x in rows10 if x["after_flag"] == "ok")
    csv_ok = sum(1 for x in rows10 if x["csv_after_flag"] == "ok")
    ctl("X2", u"换算后真落 `ok` 的行数：门禁自己 classify 复算 = 工作单「修后flag」= v6 面 yield_ok",
        gate_ok == csv_ok == face6["converted"]["yield_ok"] and gate_ok > 0,
        {"gate_self_recount": gate_ok, "csv": csv_ok,
         "face_yield_ok": face6["converted"]["yield_ok"],
         "not_ok_after": [x["claim_id"] for x in rows10 if x["after_flag"] != "ok"]})

    used = [x for x in rows10 if x["v4_urel_B"] is not None]
    worst = max((abs(float(x["rel_printed"]) - x["v4_urel_B"]) / abs(x["v4_urel_B"])
                 for x in used), default=1.0)
    ctl("X3", u"与 v4 面定价同值：v4 已 admit 的 %d 枚对 `v4_urel_B` 的最大相对偏差 ≤ 该轮印刷容差"
        % len(used),
        len(used) == len(v4diff) and worst <= face6["v4_cross_check"]["tol_fmt"],
        {"compared": len(used), "worst_rel": worst,
         "tol": face6["v4_cross_check"]["tol_fmt"], "ids": [x["claim_id"] for x in used]})

    eligible = [r for r in rows if r["flag"] in ("non_numeric", "partial")]
    fam_band, fam_val, fam_plain = [], [], []
    for r in eligible:
        adv = POST.advice(r)
        if u"填成相对带" in adv:
            fam_band.append((r, adv))
        elif u"但换算依赖" in adv:
            fam_val.append((r, adv))
        else:
            fam_plain.append((r, adv))
    ids_band = set(r["claim_id"] for r, _ in fam_band)
    ids_val = set(r["claim_id"] for r, _ in fam_val)
    ctl("X4", u"建议档三族不重不漏：印相对带 + 值列挡道 + 原样建议 = 候选行 %d 枚" % len(eligible),
        len(fam_band) + len(fam_val) + len(fam_plain) == len(eligible)
        and not (ids_band & ids_val) and len(fam_band) == len(conv),
        {"eligible": len(eligible), "band": len(fam_band), "value_side": len(fam_val),
         "plain": len(fam_plain)})
    ctl("X5", u"值列挡道教「先修值列」的 %d 枚与 v6 面 blocked.claim_ids 是同一批，且一枚都不印数"
        % len(ids_val),
        ids_val == blocked6 and not any(u"填成相对带" in a for _, a in fam_val),
        {"gate_value_side": sorted(ids_val), "v6_face_blocked": sorted(blocked6)})

    bad_num = []
    parsed = 0
    for r, adv in fam_band:
        m = re.search(u"填成相对带 `([^`]+)`", adv)
        v = POST.parse_number(m.group(1)) if m else None
        if v is None:
            bad_num.append(r["claim_id"])
        else:
            parsed += 1
    ctl("X6", u"建议档印出的数被门禁自己的 parse_number 认（作者照填即可解析）",
        parsed == len(fam_band) and not bad_num,
        {"band_rows": len(fam_band), "parsed": parsed, "bad": bad_num[:4]})

    blocked_after = [x for x in rows10 if x["after_flag"] != "ok"]
    tail_ok = all((u"复算为 `ok`" in x["advice"]) == (x["after_flag"] == "ok") for x in rows10)
    tail_named = all(u"先修值列才谈得上登记" in x["advice"] for x in blocked_after)
    ctl("X7", u"建议档自带复算尾注：落得下 ok 的 %d 枚说「该行可登记」，落不下的 %d 枚点名 prediction_value"
        % (gate_ok, len(blocked_after)),
        tail_ok and tail_named and len(blocked_after) == len(C["X2"]["payload"]["not_ok_after"]),
        {"ok_tail": sum(1 for x in rows10 if u"复算为 `ok`" in x["advice"]),
         "value_named": sum(1 for x in rows10 if u"先修值列才谈得上登记" in x["advice"]),
         "blocked_after": [x["claim_id"] for x in blocked_after]})

    destroyed, exceptions = [], []
    for r, adv in fam_band:
        old = PRE.SUGGESTION.get(r["flag"], u"—")
        if any(t in old for t in DESTRUCTIVE) and not any(t in adv for t in DESTRUCTIVE):
            destroyed.append(r["claim_id"])
        else:
            exceptions.append(r["claim_id"])
    ctl("X8", u"破坏性档撤下（带正对照）：印相对带的 %d 枚行上，发表图旧串含「留空/一并清空」而新串不含"
        % len(fam_band),
        len(destroyed) == len(fam_band) and not exceptions,
        {"rows": len(fam_band), "old_fails_new_predicate": len(destroyed),
         "exceptions": exceptions[:4],
         "old_sample": PRE.SUGGESTION.get("non_numeric", u"—")[:60],
         "new_sample": rows10[0]["advice"][:60] if rows10 else u"—"})

    ptr_elig = [r for r in eligible if POST.band_form(r["prediction_urel"])[0] == "pointer"]
    ptr_numbered = [r["claim_id"] for r in ptr_elig if u"填成相对带" in POST.advice(r)]
    plain_changed = [r["claim_id"] for r, adv in fam_plain
                     if adv != PRE.SUGGESTION.get(r["flag"], u"—")]
    ctl("X9", u"越权控制：原样建议族 %d 枚逐字等于发表图的 `SUGGESTION`（被改动 %d 枚），"
        u"候选行里的指针行 %d 枚一枚都不产数（产数 %d 枚）"
        % (len(fam_plain), len(plain_changed), len(ptr_elig), len(ptr_numbered)),
        not plain_changed and not ptr_numbered and len(ptr_elig) > 0 and len(fam_plain) > 0,
        {"plain_rows": len(fam_plain), "plain_changed": plain_changed[:4],
         "pointer_eligible": len(ptr_elig), "pointer_numbered": ptr_numbered[:4]})

    shapes = collections.Counter()
    disagree, demote_bad = [], []
    ptr_v4 = collections.Counter()
    for r in rows:
        if not r["prediction_urel"]:
            continue
        gs = POST.band_form(r["prediction_urel"])[0]
        vs = V4.read_band(r["prediction_urel"])[0]
        shapes[gs] += 1
        if gs == "pointer":
            ptr_v4[vs] += 1
            if vs in ("percent", "pm_abs", "ineq_abs", "ineq_bare"):
                demote_bad.append([r["claim_id"], gs, vs])
        elif gs != vs:
            disagree.append([r["claim_id"], gs, vs])
    ctl("X10", u"形状词表与 v4 `read_band` 同口径：非指针行逐枚同形（异形 %d 枚），"
        u"指针降级只来自 bare_number/prose_only（误降 %d 枚）"
        % (len(disagree), len(demote_bad)),
        set(shapes) <= set(VOCAB) and not disagree and not demote_bad and len(ptr_v4) > 0
        and set(ptr_v4) <= set(("bare_number", "prose_only")),
        {"nonempty_urel": sum(shapes.values()), "shapes": dict(sorted(shapes.items())),
         "pointer_as_v4": dict(sorted(ptr_v4.items())),
         "disagree": disagree[:4], "bad_demotions": demote_bad[:4]})

    fx = fixture(POST)
    ctl("X11", u"同一条声明、三种货币出三个数：期望由夹具字面量自己算（不调用被测换算函数）",
        fx["distinct"] and fx["matches_expected"], fx)

    with_pipe = [r["claim_id"] for r, adv in (fam_band + fam_val + fam_plain) if u"|" in adv]
    fx_pipe = [k for k, v in fx["advice_by_shape"].items() if u"|" in v]
    ctl("X12", u"建议档全文（含夹具）无竖线：卷里的表格不吃脏行",
        not with_pipe and not fx_pipe,
        {"advice_rows_scanned": len(fam_band) + len(fam_val) + len(fam_plain),
         "corpus_with_pipe": with_pipe[:4], "fixture_with_pipe": fx_pipe})

    st = POST.run_selftest()
    ctl("X13", u"门禁自检（变异体 %d 枚 + 端到端 1 项）在补档后全绿" % len(POST.SELFTEST_ROWS),
        all(x["ok"] for x in st) and len(st) == len(POST.SELFTEST_ROWS) + 1,
        {"items": len(st), "selftest_rows": len(POST.SELFTEST_ROWS),
         "red": [x["name"] for x in st if not x["ok"]]})

    return {"rows10": rows10, "fam_band": len(fam_band), "fam_val": len(fam_val),
            "fam_plain": len(fam_plain), "eligible": len(eligible),
            "fixture": fx, "shapes": dict(sorted(shapes.items())),
            "v6_type_counts": face6["type_counts"],
            "selftest": {"items": len(st), "red": [x["name"] for x in st if not x["ok"]]},
            "v4diff_ids": sorted(v4diff)}


def fixture(POST):
    pv = u"0.2289"
    cases = [(u"pm_abs", u"±0.002", 0.002 / abs(float(pv))),
             (u"percent", u"0.2%", 0.2 / 100.0),
             (u"ineq_bare", u"实现级 <1e-4", 1e-4)]
    got, advice_by_shape, ok_all, out = {}, {}, True, []
    for shape, urel, exp in cases:
        row = {"flag": "non_numeric", "prediction_value": pv, "prediction_urel": urel}
        s, n = POST.band_form(urel)
        rel, why = POST.to_relative(s, n, pv)
        printed = FMT % rel if rel is not None else None
        got[shape] = printed
        advice_by_shape[shape] = POST.advice(row)
        if s != shape or printed is None or abs(float(printed) - exp) > 1e-15 * max(1.0, exp):
            ok_all = False
        out.append({"shape_want": shape, "shape_got": s, "urel": urel,
                    "expected": FMT % exp, "printed": printed, "why": why,
                    "advice_head": advice_by_shape[shape][:90]})
    vals = [v for v in got.values() if v is not None]
    return {"pv": pv, "cases": out, "distinct": len(set(vals)) == len(cases),
            "matches_expected": ok_all and len(vals) == len(cases),
            "advice_by_shape": advice_by_shape,
            "expected_source": u"0.002÷0.2289、0.2÷100、1e-4 原样（由夹具字面量算）"}


# ---------------------------------------------------------------------------
# 四、门禁子进程复跑（第二把尺）+ 报告卷表卫生
# ---------------------------------------------------------------------------
def second_ruler(POST, rows, kpost, dpost, base_count):
    if not os.path.isfile(REPORT_MD):
        raise Fatal("门禁报告卷 %s 不在盘上——它每次跑都重写，不该缺席" % REPORT_MD)
    rep_before = stat(REPORT_MD)
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    p = subprocess.run([sys.executable, "-B", GATE_SRC, "--check"],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=SRC, env=env)
    out = p.stdout.decode("utf-8", "replace")
    m1 = re.search(u"扫描 (\\d+) 个 claims.csv / (\\d+) 行；数值合法登记 (\\d+) 条；"
                   u"ERROR (\\d+) 条；WARN (\\d+) 条", out)
    m2 = re.search(u"相对基线：新增 (\\d+) 条；已消除 (\\d+) 条", out)
    if not m1 or not m2:
        raise Fatal("门禁 stdout 没印出预期行（rc=%d）：\n%s" % (p.returncode, out[:400]))
    files_n = N("N1")["files_post"]
    row_files = len(set(r["file"] for r in rows))
    ok_exp = sum(1 for r in rows if r["flag"] == "ok")
    err_exp = sum(1 for r in rows if r["severity"] == "ERROR")
    warn_exp = sum(1 for r in rows if r["severity"] == "WARN")
    stdout_n = [int(m1.group(i)) for i in (1, 2, 3, 4, 5)]
    mem_n = [files_n, len(rows), ok_exp, err_exp, warn_exp]
    ctl("Y1", u"内存与子进程两把尺同读数：文件/行/ok/ERROR/WARN＋新增/已消除 七数全同、rc=%d；"
        u"另点名「扫描 %d 个文件」与「其中 %d 个文件贡献了行」是两个口径"
        % (p.returncode, stdout_n[0], row_files),
        stdout_n == mem_n and [int(m2.group(1)), int(m2.group(2))] == [len(dpost[0]), len(dpost[1])]
        and p.returncode == 1 and len(kpost) == len(dpost[0]) + base_count
        and row_files <= stdout_n[0],
        {"stdout": stdout_n, "inprocess": mem_n, "row_bearing_files": row_files,
         "added_stdout": int(m2.group(1)), "added_inprocess": len(dpost[0]),
         "removed_stdout": int(m2.group(2)), "rc": p.returncode,
         "vio_keys": len(kpost), "baseline_keys": base_count,
         "tail": out.strip().split(u"\r\n")[-1][:120]})

    rep_after = stat(REPORT_MD)
    txt = open(REPORT_MD, "rb").read().decode("utf-8")
    body = txt.split(u"## 二、违规明细")[-1].split(u"## 三")[0]
    tbl = [l for l in body.split(u"\r\n") if l.startswith(u"| ")]
    cells = sorted(set(len(l.split(u"|")) - 2 for l in tbl))
    ctl("Y2", u"门禁报告卷本轮被重写且表不脏：违规明细 %d 行、列数恒为 %s，新尾注已落进去"
        % (len(tbl), u"、".join(str(c) for c in cells)),
        len(tbl) > 0 and cells == [7] and u"照此填写后本门禁复算" in txt
        and rep_after["md5"] != rep_before["md5"],
        {"table_rows": len(tbl), "cell_counts": cells,
         "md5_before": rep_before["md5"], "bytes_before": rep_before["bytes"],
         "md5_after": rep_after["md5"], "bytes_after": rep_after["bytes"],
         "new_tail_present": u"照此填写后本门禁复算" in txt})
    return C["Y2"]["payload"]


# ---------------------------------------------------------------------------
# 五、判定卷
# ---------------------------------------------------------------------------
def render_vol(F):
    A = []
    a = A.append
    p0, n1, n2, n3, n4, n5 = (N("P0"), N("N1"), N("N2"), N("N3"), N("N4"), N("N5"))
    x2, x3, x4, x9, x10, x11 = N("X2"), N("X3"), N("X4"), N("X9"), N("X10"), N("X11")
    x8, x12, x13, y1, y2 = N("X8"), N("X12"), N("X13"), N("Y1"), N("Y2")

    a(u"# 判定 · 进门闸 v7：写入侧「建议去向」的换算补正 + 中立性见证（2026-10-19）\n\n")
    a(u"判定时刻：2026-10-19。仪器 `源码/%s`，面 `数据/%s`，控制 %d/%d 点火，rc=%d。\n"
      % (INSTR_NAME, FACE_NAME, F["controls_fired"], F["controls_total"], F["rc"]))
    a(u"产物钉（写序保证：面先落盘、卷后钉，故卷里的这两个数是盘上图像的现算）："
      u"面 `数据/%s` %d B／md5 `%s`；仪器 `源码/%s` %d B／md5 `%s`。"
      u"本卷自己的尺寸由记忆卡与登记行钉，不由卷钉自己。\n"
      % (FACE_NAME, F["face_bytes"], F["face_md5"],
         INSTR_NAME, F["instrument_bytes"], F["instrument_md5"]))
    a(u"本册不改任何体系的 `claims.csv`，也不改写违规基线；判决面与文案面的分家由 §二 逐尺见证。\n\n")

    a(u"## 一、这一轮在做什么\n\n")
    a(u"v5 测出写入侧门禁的**建议档教人删列**（`留空或填数值`／`一并清空两列`）：照它做，"
      u"违规行搬进合法的 `empty`，棘轮反而奖励破坏登记。v6 把 10 枚可换算写法算成相对带，"
      u"实测修前 ok 0／%d → 修后 ok %d／%d。\n"
      % (F["rows_total"], x2["gate_self_recount"], F["rows_total"]))
    a(u"本轮把这条换算口径补进门禁自己的 `advice()`（未偿付 A）：建议档印出可照填的相对带，"
      u"并当场复算「照此填写后门禁判什么」；值列挡道的点名值列，词表外/指针行原文案不动。\n"
      u"门禁是判决的单一真源，故主证是**中立性**：只许动文案与新增通道，判决一格不许动。\n\n")

    a(u"## 二、中立性（PRE＝发表图，POST＝现盘图）\n\n")
    a(u"| 尺 | 读数 | 判定 |\n| --- | --- | --- |\n")
    a(u"| P0 血缘 | HEAD 图 %d B（`%s`）↔ PRE 快照 %d B（`%s`），字节差 %d＝PRE 的 CRLF 数 | EOL 归一后逐字同 |\n"
      % (p0["head_bytes"], p0["head_md5"], p0["pre_snapshot_bytes"], p0["pre_snapshot_md5"],
         p0["eol_delta"]))
    a(u"| N1 逐行 | 两幅图各扫 %d 文件／%d 行，(flag, severity, reason) 全同；分档 %s | 未动 |\n"
      % (n1["files_post"], n1["rows_post"],
         u"、".join(u"%s %d" % (k, v) for k, v in n1["by_flag_post"].items())))
    a(u"| N2 违规键集 | PRE %d ↔ POST %d，键集差集 only_pre %d／only_post %d | 未动 |\n"
      % (n2["vio_pre"], n2["vio_post"], len(n2["only_pre"]), len(n2["only_post"])))
    a(u"| N3 基线差分 | 基线 %d 条、现违规 %d 条 ⇒ 新增 %d／已消除 %d（PRE 与 POST 同读数），"
      u"键集减法第三把尺亦 %d | 未动 |\n"
      % (n3["baseline_count"], n3["vio_keys"], n3["added_post"], n3["removed_post"],
         n3["independent_added"]))
    a(u"| N4 判决面源码 | %d 个定义的源码段逐字比对，被搬动 %d 个、缺失 %d 个 | 未动 |\n"
      % (len(n4["judges"]), len(n4["moved"]), len(n4["missing"])))
    a(u"| N5 改动面 | 删除 %d 行（`%s`）；新增 %d 行＝换算通道内 %d 行＋接线 %d 行（`import re` 与渲染处），"
      u"通道外 %d 项 | %s |\n\n"
      % (len(n5["deleted"]), n5["deleted"][0].strip() if n5["deleted"] else u"—",
         n5["added_n"], n5["in_region"], n5["wiring"], len(n5["outside"]),
         u"封闭" if not n5["outside"] else u"未封闭：%s" % u"／".join(l for _, l in n5["outside"])))
    a(u"门禁图：PRE %d B／CRLF %d（`%s`，HEAD 发表态）→ POST %d B／CRLF %d（`%s`）。\n\n"
      % (p0["pre_snapshot_bytes"], p0["pre_crlf"], p0["pre_snapshot_md5"],
         p0["post_bytes"], p0["post_crlf"], p0["post_md5"]))

    a(u"## 三、那 %d 条「新增违规」不是本轮改出来的\n\n" % n3["added_post"])
    a(u"基线登记于 %s，只 %d 条（`S15-C0020|non_numeric`）；本轮动手前语料已有违规 %d 条。"
      u"拿发表图跑同一份基线，差分读数一模一样（新增 %d／已消除 %d）⇒ "
      u"`--check` 的 rc=1 报的是**基线欠登记**这笔旧债，不是本轮引入的回潮。\n"
      % (n3["baseline_updated_utc"], n3["baseline_count"], n3["vio_keys"],
         n3["added_pre"], n3["removed_pre"]))
    a(u"债未偿：基线只能由 `--update-baseline` 显式改写。本册不替属主动手——"
      u"现违规 %d 条分布在 %d 个体系（扫描 %d 份 `claims.csv`，其中 %d 份带 UFT-3 两列），"
      u"除基线里那 1 条外还有 %d 条要洗成历史遗留，须由属主逐条认领后另开一轮。\n\n"
      % (n3["vio_keys"], n1["owners_post"], n1["files_post"], y1["row_bearing_files"],
         n3["added_post"] - 1))

    a(u"## 四、换算补正与 v6 工作单／v4 面三方一致\n\n")
    a(u"10 枚可换算写法逐枚过三关：门禁现算形状＋相对带串 = 工作单「形状」「换算后相对带」（X1）；"
      u"照此填写后门禁自己复算的档 = 工作单「修后flag」= 面 `yield_ok`（X2）；"
      u"v4 已 admit 的 %d 枚对 `v4_urel_B` 最大相对偏差 %.3e ≤ 容差 %.1e（X3）。\n\n"
      % (x3["compared"], x3["worst_rel"], x3["tol"]))
    a(u"| claim_id | 现串（截） | 形状 | 建议档相对带 | 复算档 | v4 `urel_B` |\n")
    a(u"| --- | --- | --- | --- | --- | --- |\n")
    for x in F["x1"]["rows10"]:
        a(u"| `%s` | `%s` | `%s` | `%s` | `%s` | %s |\n"
          % (x["claim_id"], x["urel"].replace(u"`", u"′"), x["shape"], x["rel_printed"],
             x["after_flag"],
             (u"`%s`" % FMT % x["v4_urel_B"]) if x["v4_urel_B"] is not None
             else u"—（不在 v4 admit）"))
    a(u"\n落得下 `ok` 的 %d 枚全在 S02、对着同一枚具名靶；其余 %d 枚被值列挡住 ⇒ "
      u"**误差棒这一列修到底，可登记行的上限就是 %d／%d**，与 v6 结论同额；"
      u"本轮把这句话做进了建议档的尾注（X7）。\n\n"
      % (x2["gate_self_recount"], len(x2["not_ok_after"]), x2["gate_self_recount"],
         F["rows_total"]))

    a(u"## 五、建议档三族与两枚对照\n\n")
    a(u"| 族 | 枚数 | 内容 | 附带判定 |\n| --- | --- | --- | --- |\n")
    a(u"| 印相对带 | %d | 形状＋可照填的数＋**不要清空两列**＋复算尾注 | parse_number 全认 %d/%d（X6） |\n"
      % (x4["band"], N("X6")["parsed"], x4["band"]))
    a(u"| 值列挡道 | %d | 点名 `prediction_value` 现串不可解析，**不编数** | 与 v6 面 blocked 同批 %d＝%d（X5） |\n"
      % (x4["value_side"], len(N("X5")["gate_value_side"]), len(N("X5")["v6_face_blocked"])))
    a(u"| 原样建议 | %d | 词表外/指针/散文行逐字保持发表图 `SUGGESTION` | 被改动 %d 枚（X9） |\n\n"
      % (x4["plain"], len(x9["plain_changed"])))
    a(u"正对照（X8）：印相对带的 %d 枚行上，发表图旧串**确实**含 `留空`／`一并清空`、"
      u"新串不含 ⇒ 通过 %d／%d、例外 %d 枚。「撤下破坏性建议」这句话由旧文案自己证真，"
      u"不是新档自说自话。\n" % (x4["band"], x8["old_fails_new_predicate"], x8["rows"],
                                 len(x8["exceptions"])))
    a(u"越权控制（X9）：候选行中指针行 %d 枚一枚都不产数（产数 %d 枚），"
      u"原样建议族 %d 枚逐字未改（改动 %d 枚）⇒ 补档没有越出「可换算写法」这一族。\n\n"
      % (x9["pointer_eligible"], len(x9["pointer_numbered"]), x9["plain_rows"],
         len(x9["plain_changed"])))

    a(u"## 六、形状词表与 v4 同口径\n\n")
    a(u"非空误差棒列 %d 枚的形状分布：%s。\n"
      % (x10["nonempty_urel"], u"、".join(u"%s %d" % (k, v) for k, v in x10["shapes"].items())))
    a(u"与 v4 `read_band` 逐枚对照：非指针行异形 %d 枚、指针误降 %d 枚；"
      u"指针行在 v4 视角下读成 %s——若把它们算进「可换算」，换算通道会凭路径里的"
      u"年份/编号造出假带，所以 `PATH_FORM` 必须走在取首枚数字之前（X10）。\n\n"
      % (len(x10["disagree"]), len(x10["bad_demotions"]),
         u"／".join(u"%s %d" % (k, v) for k, v in x10["pointer_as_v4"].items())))
    a(u"标签与结果要分开读：本册指针档 %d 枚比 v6 普查的 `pointer_in_urel` %d 枚**窄**"
      u"（v6 那条尺吃「串里有路径形状」，本册 `PATH_FORM` 要求整串就是路径）；"
      u"窄下来的那几枚落进 `bare_number`／`prose_only`，而 `bare_number` 不在可换算族里，"
      u"所以两轮的**产出集仍然同一**：印相对带 %d 枚＝v6 面 converted.n、值列挡道 %d 枚＝v6 面 blocked.n（X4、X5）。"
      u"分档标签不同不构成矛盾，产出集不同才构成矛盾——这一条由 X4/X5 拦着。\n\n"
      % (x10["shapes"].get(u"pointer", 0), F["v6_type_counts"]["pointer_in_urel"],
         x4["band"], x4["value_side"]))

    a(u"## 七、夹具：同一条声明、三种货币\n\n")
    a(u"`prediction_value` 固定 `%s`，误差棒列分别写 `±0.002`、`0.2%%`、`实现级 <1e-4`：\n\n" % x11["pv"])
    a(u"| 形状 | 现串 | 期望（夹具字面量现算） | 门禁印出 |\n| --- | --- | --- | --- |\n")
    for cs in x11["cases"]:
        a(u"| `%s` | `%s` | `%s` | `%s` |\n" % (cs["shape_got"], cs["urel"],
                                                 cs["expected"], cs["printed"]))
    a(u"\n三档互不相同 %s、逐枚与期望相符 %s。期望数取自 %s，不调用被测换算函数——"
      u"否则这条控制只会自证。\n\n"
      % (u"是" if x11["distinct"] else u"否", u"是" if x11["matches_expected"] else u"否",
         x11["expected_source"]))

    a(u"## 八、卫生、自检与退出码\n\n")
    a(u"建议档全文 %d 枚（含夹具文案）无竖线（命中 %d 枚）⇒ 本卷与报告卷的表都不吃脏行（X12）。\n"
      % (x12["advice_rows_scanned"], len(x12["corpus_with_pipe"])))
    a(u"门禁自检 %d 项全绿（变异体 %d 枚 + 端到端 1 项，红 %d 项，X13）；"
      u"子进程 `--check` rc=%d，stdout 五数 %s 与内存五数 %s 同值，"
      u"新增/已消除 %d／%d 与 N3 同值（Y1）。\n"
      % (x13["items"], x13["selftest_rows"], len(x13["red"]), y1["rc"],
         u"／".join(str(v) for v in y1["stdout"]), u"／".join(str(v) for v in y1["inprocess"]),
         y1["added_stdout"], y1["removed_stdout"]))
    a(u"报告卷随本次运行重写：%d B（`%s`）→ %d B（`%s`）%s；违规明细表 %d 行、列数恒 %s，"
      u"新尾注「照此填写后本门禁复算」已在其中（Y2）。"
      u"注意这是门禁的固有行为——`--check` 只保护基线文件，不保护这对产物报告，"
      u"所以「只读跑一遍」在本仓不成立，引用报告卷读数时必须点名是哪一次运行。\n\n"
      % (y2["bytes_before"], y2["md5_before"], y2["bytes_after"], y2["md5_after"],
         u"（尺寸同、md5 变——差在文件里的 generated_utc 时间戳）"
         if y2["bytes_before"] == y2["bytes_after"] else u"（尺寸亦变）",
         y2["table_rows"], u"、".join(str(c) for c in y2["cell_counts"])))

    by_pref = collections.Counter(x["code"][0] for x in F["controls"])
    a(u"## 九、去向与未偿付\n\n")
    a(u"1. 未偿付 A **本轮偿清**：建议档不再教人删列，且给出可照填的相对带＋自带复算尾注。"
      u"牙在 %d 枚控制上（血缘 %d＋中立性 %d＋换算补正 %d＋两把尺 %d＋落刀自证 %d＋题面卫生 %d），红 %d 枚。\n"
      % (len(F["controls"]), by_pref["P"], by_pref["N"], by_pref["X"], by_pref["Y"],
         by_pref["W"], by_pref["Z"], len(F["controls_red"])))
    a(u"2. 建议只是文案：**盘上可登记行仍是 %d／%d**，%d／%d 只是「作者照填之后」的内存预演，"
      u"且那 %d 枚全部对着 S02 的同一枚具名靶（`sin²θ_W`）。统计层要拿到有判决力的样本，"
      u"下一腿须处理三族：值列不可解析、散文带、指针（本轮未动，见 §五、§六）。\n"
      % (n1["by_flag_post"].get(u"ok", 0), F["rows_total"], x2["gate_self_recount"],
         F["rows_total"], x2["gate_self_recount"]))
    a(u"3. 基线欠登记（§三）仍 OPEN：现违规 %d 条 vs 基线 %d 条 ⇒ `--check` 天天 rc=1；"
      u"改写基线须属主显式认领。\n" % (n3["vio_keys"], n3["baseline_count"]))
    a(u"4. 本轮故意不做：把换算通道接进 `--update-baseline`（那会把建议变成自动改账）、"
      u"替他体系改 `claims.csv`、给 `bare_number` 以外的形状扩档；"
      u"也不把带量纲的绝对单位误差棒（`GeV`、`yr` 这一型）纳入 ÷声明值绝对值——"
      u"那需要先做量纲折算，v4 的口径里没有这一步，硬套就是把换算尺放宽成「有个数就行」。\n\n"
      % ())

    a(u"## 十、复算\n\n")
    a(u"```powershell\n")
    a(u"cd openuft/04_公共成果/本项目_全维自洽与归一化\n")
    a(u"PYTHONIOENCODING=utf-8 python -B 源码/%s --land\n" % INSTR_NAME)
    a(u"PYTHONIOENCODING=utf-8 python -B 源码/靶场登记列校验_写入侧门禁.py --check\n")
    a(u"```\n")
    a(u"PRE 快照 `%s`（%d B，`%s`）与三枚补丁脚本 `scratch/gate_r74_{block,patch3,patch4}.py` "
      u"一起留在 scratch，重放顺序即 §二 的改动面。\n"
      % (os.path.relpath(PRE_HEAD, ROOT).replace("\\", "/"), p0["pre_snapshot_bytes"],
         p0["pre_snapshot_md5"]))
    w1 = N("W1")
    a(u"落刀自证（W1）：`scratch` 源 %d B／CRLF %d 与 `源码/` 落盘像 %d B／CRLF %d 只差行尾，"
      u"EOL 归一后逐字同（按字节则不等——正是归一那一步在做工，不是摆设）。"
      u"本卷跑的是 `源码/` 里的那柄刀（%s）：它必须与手里的源同一把。\n"
      % (w1["scratch_bytes"], w1["scratch_crlf"], w1["landed_bytes"], w1["landed_crlf"],
         u"落盘像＝正在运行的文件" if w1["mode"] == u"--land" else u"预跑，落盘像只作对照"))
    a(u"上面那行产物钉不是装饰：驱动器在卷落盘之后从**盘上的卷**里用正则找回这两个数，"
      u"再量盘上的面（%d B）与仪器（%d B），一枚不符即 FATAL、本次产物不得引用。\n"
      % (F["face_bytes"], F["instrument_bytes"]))
    return u"".join(A)


def main():
    t0 = time.time()
    PRE, POST, V4, pre_stat, post_stat = load_gates()
    pins = pins_from_v6_volume()
    rows, kpost, dpost, base_count = neutrality(PRE, POST)
    AD = advice_channels(PRE, POST, V4, rows, pins)
    rep = second_ruler(POST, rows, kpost, dpost, base_count)

    ctl("Z0", u"题面卫生：全部控制题名里不留未替换的占位符（槽位断言不许把期望数印成字面格式串）",
        True, {"controls_before_scan": len(CONTROLS)})
    leaked = [C[c]["name"] for c in CONTROLS if re.search(u"%[-+ 0-9.]*[sdf]", C[c]["name"])]
    C["Z0"]["fired"] = not leaked
    C["Z0"]["payload"] = {"controls": len(CONTROLS), "leaked": leaked[:4]}
    if leaked:
        print("  [RED] " + C["Z0"]["name"])

    # W1：跑了的刀必须就是手里这把刀。落盘仪器与 scratch 源只许差在行尾，
    # 且「按字节相等」必须与「行尾是否真的不同」同号——否则 EOL 归一就是把无牙的尺。
    s_src, l_src = os.path.join(SCRATCH, INSTR_NAME), os.path.join(SRC, INSTR_NAME)
    if not (os.path.isfile(s_src) and os.path.isfile(l_src)):
        raise Fatal("W1 需要两把尺（scratch 源与 源码/ 落盘像）——缺一枚即无法证伪，本册不得引用")
    sa = open(s_src, "rb").read()
    lb = open(l_src, "rb").read()
    self_b = open(os.path.abspath(__file__), "rb").read()
    eol_equal = sa.replace(b"\r\n", b"\n") == lb.replace(b"\r\n", b"\n")
    bytes_equal = sa == lb
    cr_diff = (sa.count(b"\r\n"), lb.count(b"\r\n"))
    mode = u"--land" if LAND else u"预跑"
    # --land 那一步，`源码/` 里的图就是正在跑的这柄刀：落盘像须与运行体逐字节同
    fired = eol_equal and ((lb == self_b) if LAND else (bytes_equal == (cr_diff[0] == cr_diff[1])))
    ctl("W1", u"落盘的刀＝手里的刀：`源码/` 仪器与 scratch 源 EOL 归一后逐字同（两图 CRLF %d／%d，%s）"
        % (cr_diff[0], cr_diff[1], mode),
        fired, {"scratch_bytes": len(sa), "landed_bytes": len(lb),
                "scratch_crlf": cr_diff[0], "landed_crlf": cr_diff[1],
                "scratch_md5": md5(sa), "landed_md5": md5(lb),
                "eol_equal": eol_equal, "bytes_equal": bytes_equal,
                "mode": mode})

    red = [c for c in CONTROLS if not C[c]["fired"]]
    face = {
        "instrument": INSTR_NAME,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rc": 0 if not red else 1,
        "controls": [C[c] for c in CONTROLS],
        "controls_total": len(CONTROLS),
        "controls_fired": len(CONTROLS) - len(red),
        "controls_red": red,
        "rows_total": len(rows),
        "gate_lineage": N("P0"),
        "v6_pins": pins,
        "x1": {"rows10": AD["rows10"]},
        "x2": N("X2"),
        "dispatch": {"band": AD["fam_band"], "value_side": AD["fam_val"],
                     "plain": AD["fam_plain"], "eligible": AD["eligible"]},
        "fixture": AD["fixture"],
        "shapes": AD["shapes"],
        "v6_type_counts": AD["v6_type_counts"],
        "report": rep,
    }
    fb = os.path.join(OUT_DIR, FACE_NAME)
    raw = json.dumps(face, ensure_ascii=False, indent=2).encode("utf-8")
    open(fb, "wb").write(raw)
    if open(fb, "rb").read() != raw:
        raise Fatal("面写后回读与内存图不一致——本次产物不得引用")
    # 卷要钉面的尺寸，所以面先落盘；卷自己不能钉自己（本册尺寸由记忆卡与登记行钉）
    F = dict(face, face_bytes=len(raw), face_md5=md5(raw),
             instrument_stat=stat(os.path.abspath(__file__)),
             instrument_at=os.path.abspath(__file__),
             instrument_bytes=len(self_b), instrument_md5=md5(self_b))
    vol = render_vol(F)
    for tok in (u"%s", u"%d", u"%.12g", u"%.3e", u"%.1e"):
        if tok in vol:
            raise Fatal(u"卷里有未替换的占位符 %s" % tok)
    vb = os.path.join(PROJP if LAND else OUT_DIR, VOL_NAME)
    vraw = vol.replace(u"\r\n", u"\n").replace(u"\n", u"\r\n").encode("utf-8")
    if not (vraw.count(b"\r") == vraw.count(b"\n") == vraw.count(b"\r\n")):
        raise Fatal("卷不是纯 CRLF")
    open(vb, "wb").write(vraw)
    if open(vb, "rb").read() != vraw:
        raise Fatal("卷写后回读与内存图不一致——本次产物不得引用")

    # 写后对账：只吃盘上图像。从落盘的卷里找回它印的那两个钉，再量盘上的面与仪器。
    on_vol = open(vb, "rb").read().decode("utf-8")
    on_face = open(fb, "rb").read()
    m = re.search(u"面 `数据/%s` (\\d+) B／md5 `([0-9a-f]{32})`；仪器 `源码/%s` (\\d+) B／md5 `([0-9a-f]{32})`"
                  % (re.escape(FACE_NAME), re.escape(INSTR_NAME)), on_vol)
    if not m:
        raise Fatal("卷里找不到它自己印的产物钉行——钉没落进盘上图像，本次产物不得引用")
    face_pin = (int(m.group(1)), m.group(2)) == (len(on_face), md5(on_face))
    instr_pin = (int(m.group(3)), m.group(4)) == (len(self_b), md5(self_b))
    if not (face_pin and instr_pin):
        raise Fatal("卷印的钉与盘上图像不符（面 %s／仪器 %s）——本次产物不得引用"
                    % ("同" if face_pin else "异", "同" if instr_pin else "异"))

    if not QUIET:
        print("=" * 78)
        for c in CONTROLS:
            print("  [%s] %s" % ("OK " if C[c]["fired"] else "RED", C[c]["name"]))
        print("  10 枚可换算 ⇒ 复算落 ok %d 枚；分派 带 %d／值列 %d／原样 %d（候选 %d）"
              % (face["x2"]["gate_self_recount"], AD["fam_band"], AD["fam_val"],
                 AD["fam_plain"], AD["eligible"]))
        print("  控制 %d/%d 点火，rc=%d；面 %d B（%s）｜卷 %d B（%s）｜用时 %.2fs"
              % (face["controls_fired"], face["controls_total"], face["rc"],
                 len(raw), md5(raw), len(vraw), md5(vraw), time.time() - t0))
    return face["rc"]


if __name__ == "__main__":
    sys.exit(main())
