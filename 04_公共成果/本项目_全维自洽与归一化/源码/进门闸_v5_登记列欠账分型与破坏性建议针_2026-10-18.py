# -*- coding: utf-8 -*-
"""进门闸 v5：登记列欠账的**分型**与「建议去向」的破坏性针。

来龙去脉（为什么不是重复 v4）
----------------------------
v4 判的是**判决侧**（同一行喂两种货币，命中会不会翻面）。本册判的是**写入侧**：
`源码/靶场登记列校验_写入侧门禁.py` 是登记列语义的单一真源，它把 462 行台账逐行分级
（`ok`／`empty`／`non_numeric`／`partial`／…），并对每行给一句「建议去向」。
本轮实测两件事：

  ① **欠账不是一个型**。门禁只说「不可解析」（`non_numeric`）与「只填一列」（`partial`），
     但这一栏的实际形状至少四型：把带写成绝对/百分数/不等式（**可换算**）、写成散文
     （不可换算）、把**推导来源的路径**写进误差棒列（内容对、列错）、以及数值列本身
     带单位/区间（先修值再谈带）。四型修法不同，混在一个 flag 里就会给出一刀切建议。

  ② **建议文本有害**。`non_numeric` 建议「……留空或填数值」，`partial` 建议
     「补 `prediction_urel`（整数靶填 0）或一并清空两列」。在临时副本上端到端跑门禁
     自己的扫描：按建议**清空** ⇒ 该行从违规集消失（棘轮记成「改进」），带走的是
     一个真能解析出数值的带宽、或一个真能在盘上落地的推导指针；按建议**填 0** ⇒
     该行判 `ok`，而 `ok` 意味着拿 `urel=0`（精确预言）去喂观测载体，载体判不中。
     **唯一变绿的两条路：一条销毁信息，一条制造假精确。**

判决一律不自定：形状尺借 `进门闸_v4` 的 `read_band`（按语料实际拼写枚举），
命中一律喂观测载体 `无量纲靶场审计.py` 自己的 `hit_test`（3σ；urel=0 要求逐字相等），
逐行分级借门禁自己的 `classify/scan_registry/violations/key_of`。
所有期望值由该夹具或该面的字面量现推，不打字。

用法：`python 进门闸_v5_登记列欠账分型与破坏性建议针_2026-10-18.py [--land] [--quiet]`
（不带 `--land` 时面写 `scratch/`，不落仓库产物目录。）
"""
from __future__ import print_function

import collections
import csv
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
PROJP = os.path.join(ROOT, "openuft", "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(PROJP, "源码")
DATA = os.path.join(PROJP, "数据")
GATE_SRC = os.path.join(SRC, "靶场登记列校验_写入侧门禁.py")
V4_SRC = os.path.join(SRC, "进门闸_v4_误差棒货币裁定_绝对与相对双向命中_2026-10-18.py")
V4_FACE = os.path.join(DATA, "进门闸_v4_误差棒货币裁定_绝对与相对双向命中_2026-10-18.json")
CARRIER = os.path.join(SRC, "无量纲靶场审计.py")
FACE = "进门闸_v5_登记列欠账分型与破坏性建议针_2026-10-18.json"
LAND = "--land" in sys.argv[1:]
QUIET = "--quiet" in sys.argv[1:]
OUT_DIR = DATA if LAND else os.path.join(ROOT, "scratch")


class Fatal(Exception):
    pass


def load(name, path):
    if not os.path.isfile(path):
        raise Fatal("依赖文件不在盘：%s" % path)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


G = load("intake_v5_gate", GATE_SRC)
V4 = load("intake_v5_v4", V4_SRC)
CAR = load("intake_v5_carrier", CARRIER)
read_band = V4.read_band
CUR_SHAPES = ("pm_abs", "ineq_abs", "ineq_bare", "percent")
PATHISH = re.compile(r"[/\\]")
# 只有分隔符不够：`kg/m³`、`（S1/S2）`、`50/50̄ 分解` 都是散文里的斜杠（假阳族）。
# 路径形状的正面判据＝整串只由路径字符集组成且含至少一个分隔段。
PATH_SHAPE = re.compile(u"^\\w+(?:\\.\\w+)?(?:/\\w+(?:\\.\\w+)?)+$")
EXTS = (".md", ".py", ".csv", ".json", ".txt", ".tex")
VOCAB = ("pointer_in_urel", "urel_other_currency", "urel_prose_band", "value_unparseable",
         "urel_absent", "value_absent", "urel_zero_exact_noninteger", "negative_urel",
         "clean_numeric", "other")


def rel_of(owner):
    return os.path.join(G.SYS_DIR, owner)


def resolve_pointer(owner, raw):
    """推导指针能否在盘上落地。file/dir 都算落地（S17 公式集里一项就是一个目录）。"""
    base = rel_of(owner)
    cand = os.path.normpath(os.path.join(base, str(raw).strip().lstrip("/"))) if os.path.isdir(base) else None
    if cand is None:
        return "owner_dir_absent", None
    if os.path.isfile(cand):
        return "file", os.path.relpath(cand, ROOT).replace("\\", "/")
    if os.path.isdir(cand):
        return "dir", os.path.relpath(cand, ROOT).replace("\\", "/")
    hits = sorted({cand + e for e in EXTS if os.path.isfile(cand + e)})
    if len(hits) == 1:
        return "file_by_extension", os.path.relpath(hits[0], ROOT).replace("\\", "/")
    if len(hits) > 1:
        return "ambiguous", hits
    return "dangling", None


def pv_state(pv):
    if not pv:
        return "absent"
    return "number" if G.parse_number(pv) is not None else "prose"


def rel_band(shape, num, pv_num):
    """把带换算成**声明的相对货币**：百分数除以 100，绝对/不等式写法除以 |pv|。"""
    if num is None:
        return None
    if shape == "percent":
        return abs(num) / 100.0
    if shape in ("pm_abs", "ineq_abs", "ineq_bare"):
        if pv_num is None:
            return None
        v = abs(float(pv_num))
        return (abs(num) / v) if v else None
    return None


def debt_of(row):
    """逐行分型。顺序即判据：能解析成数的列先归数，剩下的路径列**必须**早于带尺
    （路径里的数字会被带尺读成误差棒——S15-C0020 的 `09_验证结果/…` 被读成 9.0）。"""
    pv, pu = row["prediction_value"], row["prediction_urel"]
    shape, num = read_band(pu)
    parses = G.parse_number(pu) is not None
    if not pu:
        return ("urel_absent", {"pv_state": pv_state(pv)}) if pv else ("clean_numeric", {})
    landed = resolve_pointer(row["owner"], pu)[0] if not parses else None
    if not parses and (landed in ("file", "dir", "file_by_extension", "ambiguous")
                       or PATH_SHAPE.match(pu.strip())):
        return "pointer_in_urel", {"band_ruler_reads": shape, "numeral_misread_as_band": num,
                                   "pv_state": pv_state(pv)}
    if shape == "empty":
        return "urel_absent", {"pv_state": pv_state(pv)}
    if shape in CUR_SHAPES:
        pvn = G.parse_number(pv)
        return "urel_other_currency", {"shape": shape, "numeral": num,
                                       "pv_state": pv_state(pv),
                                       "rel_converted": rel_band(shape, num, pvn)}
    if shape == "prose_only":
        return "urel_prose_band", {"pv_state": pv_state(pv)}
    if pv_state(pv) == "absent":
        return "value_absent", {"band_ruler_reads": shape}
    if row["flag"] == "urel_zero_noninteger":
        return "urel_zero_exact_noninteger", {"pv_state": pv_state(pv)}
    if row["flag"] == "negative_urel":
        return "negative_urel", {}
    if row["flag"] == "ok":
        return "clean_numeric", {}
    if pv_state(pv) != "number":
        return "value_unparseable", {"band_ruler_reads": shape}
    return "other", {"why_gate_flag": row["flag"], "band_ruler_reads": shape}


def mkrow(owner, pv, pu, flag="synthetic"):
    return {"owner": owner, "claim_id": "FIXTURE", "prediction_value": pv,
            "prediction_urel": pu, "flag": flag}


def census(nonempty):
    cls = collections.OrderedDict((k, []) for k in VOCAB)
    grid = collections.Counter()
    for r in nonempty:
        if not os.path.isdir(rel_of(r["owner"])):
            raise Fatal("体系目录不在盘：%s（基准错了就不许判「悬空」）" % rel_of(r["owner"]))
        c, extra = debt_of(r)
        cls[c].append(dict(claim_id=r["claim_id"], owner=r["owner"], flag=r["flag"],
                           pv=r["prediction_value"], urel=r["prediction_urel"], **extra))
        if r["prediction_value"]:
            grid["%s x %s" % (pv_state(r["prediction_value"]),
                              read_band(r["prediction_urel"])[0])] += 1
    for k in VOCAB:
        if k not in cls:
            raise Fatal("词表里冒出不认识的分型 %s——补词表，别放宽判据" % k)
    return cls, grid


def harm_experiment(pointer_row, pointer_literal):
    """在临时副本（不落仓库）上跑门禁自己的扫描：逐支验证「建议去向」的后果。"""
    tmp = tempfile.mkdtemp(prefix="intake_v5_harm_")
    try:
        d = os.path.join(tmp, "X_自检体系")
        os.makedirs(d)
        ledger = os.path.join(d, "claims.csv")

        def write(pairs):
            with open(ledger, "w", encoding="utf-8", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["claim_id", "prediction_value", "prediction_urel"])
                for cid, pv, pu in pairs:
                    w.writerow([cid, pv, pu])

        def vkey(r):
            return "%s|%s|%s" % (os.path.basename(r["file"]), r["claim_id"], r["flag"])

        def scan():
            rows, paths = G.scan_registry(tmp)
            if len(paths) != 1 or len(rows) != 3:
                raise Fatal("自检台账扫描异常（paths=%d rows=%d）——这台实验没有输入，不许出判决"
                            % (len(paths), len(rows)))
            return dict((r["claim_id"], r) for r in rows)

        clean = ("H3", "0.2289", "0.002")
        write([("H1", "0.2289", u"±0.002（两实现离散）"), ("H2", "", pointer_literal), clean])
        before = scan()
        vio_before = sorted(vkey(r) for r in G.violations(list(before.values())))
        if len(vio_before) != 2 or before["H3"]["flag"] != "ok":
            raise Fatal("实验前提不成立：改前应有 2 条违规且 H3 干净（实得 %d 条、H3=%s）"
                        % (len(vio_before), before["H3"]["flag"]))
        band_num = read_band(before["H1"]["prediction_urel"])[1]
        band_parses_by_gate = G.parse_number(before["H1"]["prediction_urel"]) is not None

        write([("H1", "", ""), ("H2", "", ""), clean])
        blank = scan()
        vio_blank = sorted(vkey(r) for r in G.violations(list(blank.values())))
        blank_flags = dict((k, blank[k]["flag"]) for k in ("H1", "H2", "H3"))

        write([("H1", "0.2289", "0"), ("H2", "", "0"), clean])
        zero = scan()
        vio_zero = sorted(vkey(r) for r in G.violations(list(zero.values())))
        zero_flags = dict((k, zero[k]["flag"]) for k in ("H1", "H2"))

        keyerr = None
        try:
            G.key_of(before["H1"])
        except ValueError as e:
            keyerr = str(e)[:120]
        return {
            "ledger_carrier": "tempfile 副本（不落仓库真实台账）",
            "gate_key_of_on_temp_path": keyerr,
            "violations_before": vio_before,
            "H1_band_has_numeral": band_num is not None,
            "H1_numeral_parses_by_gate": band_parses_by_gate,
            "H2_pointer_resolves_in_corpus": resolve_pointer(pointer_row["owner"],
                                                            pointer_row["urel"])[0],
            "branch_blank": {"violations_after": vio_blank, "flags": blank_flags,
                             "improvement_reported_keys": sorted(set(vio_before) - set(vio_blank))},
            "branch_fill_zero": {"violations_after": vio_zero, "flags": zero_flags,
                                 "green_keys": sorted(set(vio_before) - set(vio_zero)),
                                 "new_keys": sorted(set(vio_zero) - set(vio_before)),
                                 "count_before_after": [len(vio_before), len(vio_zero)]},
        }
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_controls(flips, classes, harm, contam, by_id, v4chan, literal, firstdigit):
    out = []

    def fire(name, ok, detail):
        out.append({"name": name, "fired": bool(ok), "detail": detail})

    c1a = debt_of(mkrow("S02", "0.2289", u"±0.002（两实现离散）", "non_numeric"))
    c1b = debt_of(mkrow("S02", "0.2289", "0.002", "ok"))
    fire("C1 同一行只改 `±` 有无 ⇒ 分型必须分叉（可换算 vs 干净），且换算值由字面量现推 0.002/0.2289",
         c1a[0] == "urel_other_currency" and c1b[0] == "clean_numeric"
         and abs(c1a[1]["rel_converted"] - 0.002 / 0.2289) < 1e-15, (c1a, c1b[0]))
    c2 = debt_of(mkrow("S02", "0.2289", "0.2%", "non_numeric"))
    fire("C2 百分数走 /100、绝对写法走 /|pv|：两条规则不许混用（同一数值 0.2 与 0.002 各自换算后必须不同）",
         c2[0] == "urel_other_currency" and c2[1]["shape"] == "percent"
         and abs(c2[1]["rel_converted"] - 0.002) < 1e-15
         and abs(c2[1]["rel_converted"] - c1a[1]["rel_converted"]) > 1e-6,
         (c2[1]["shape"], c2[1]["rel_converted"], c1a[1]["rel_converted"]))
    c3 = debt_of(mkrow("S02", "0.2289", u"实现级离散约千分之二", "non_numeric"))
    fire("C3 散文带（数值写成汉字）判 prose 型且**不许**被换算（不发明数）",
         c3[0] == "urel_prose_band" and "rel_converted" not in c3[1], c3)
    real = [c for c in classes["pointer_in_urel"]
            if c["resolves"] in ("file", "dir", "file_by_extension")]
    if not real:
        raise Fatal("抽不到能落地的推导指针做夹具——C4 没有输入")
    p = real[0]
    c4 = debt_of(mkrow(p["owner"], "", p["urel"], "partial"))
    numpath = [c for c in real if read_band(c["urel"])[0] == "bare_number"]
    if not numpath:
        raise Fatal("没有一条路径串的带尺读数是 bare_number——C4 的反例无输入")
    fire("C4 路径写进误差棒列：判 pointer 型，且带尺对同一串报 bare_number（数字来自目录名）⇒ 指针判据必须早于带尺",
         c4[0] == "pointer_in_urel" and read_band(numpath[0]["urel"])[0] == "bare_number",
         (c4[0], read_band(numpath[0]["urel"]), numpath[0]["claim_id"], numpath[0]["urel"]))
    c5 = debt_of(mkrow(p["owner"], "", u"04_理论推导/核心公式集/绝不存在_XYZ", "partial"))
    r5 = resolve_pointer(p["owner"], u"04_理论推导/核心公式集/绝不存在_XYZ")[0]
    fire("C5 悬空指针夹具：落点必须读成 dangling（没落地的不许算落地）",
         c5[0] == "pointer_in_urel" and r5 == "dangling", r5)
    hb = harm["branch_blank"]
    fire("C6 删除支：按建议清空两列 ⇒ 违规集从 2 缩到 0（棘轮记两条「改进」），而带走的带能解析出数、指针能在盘上落地",
         hb["violations_after"] == [] and len(hb["improvement_reported_keys"]) == len(harm["violations_before"])
         and hb["flags"]["H1"] == "empty" and hb["flags"]["H2"] == "empty" and hb["flags"]["H3"] == "ok"
         and harm["H1_band_has_numeral"] and not harm["H1_numeral_parses_by_gate"]
         and harm["H2_pointer_resolves_in_corpus"] in ("file", "dir", "file_by_extension"),
         (hb["improvement_reported_keys"], hb["flags"], harm["H2_pointer_resolves_in_corpus"]))
    hz = harm["branch_fill_zero"]
    fire("C7 填 0 支：违规数不减（2→2）只是换了 flag ⇒ 记账键含 flag，同一行被记成「改进＋新增」，换旗可洗棘轮；"
         "H2 填 0 后仍 partial（不绿）⇒ 两条建议里只有删除真能变绿",
         hz["count_before_after"][0] == hz["count_before_after"][1] == len(harm["violations_before"])
         and hz["flags"]["H1"] == "urel_zero_noninteger" and hz["flags"]["H2"] == "partial"
         and len(hz["green_keys"]) == 1 and len(hz["new_keys"]) == 1,
         (hz["flags"], hz["green_keys"], hz["new_keys"], hz["count_before_after"]))
    f0 = flips[0]
    obs, pvv = float(f0["obs"]), float(f0["pv"])
    conv = abs(read_band(f0["urel_spelling"])[1]) / pvv
    fire("C8 填 0 之害由载体自己的 hit_test 定价：同一行 urel=0 判不中、换算后的相对带判得中",
         CAR.hit_test(pvv, obs, 0) is False and CAR.hit_test(pvv, obs, conv) is True,
         (f0["claim_id"], f0["key"], "urel0=%s rel=%s" % (CAR.hit_test(pvv, obs, 0),
                                                          CAR.hit_test(pvv, obs, conv))))
    slashnon = [c for k, v in classes.items() if k != "pointer_in_urel"
                for c in v if PATHISH.search(c["urel"])]
    fakeptr = [c for c in classes["pointer_in_urel"]
               if c["resolves"] == "dangling" and not PATH_SHAPE.match(c["urel"].strip())]
    fire("C11 双向自证：散文里的斜杠（kg/m³、（S1/S2）、50/50̄）留在非 pointer 型且串本身不是路径字符集；"
         "pointer 型里也不许有「既没落地又不像路径」的行",
         bool(slashnon) and all(not PATH_SHAPE.match(c["urel"].strip()) for c in slashnon) and not fakeptr,
         {"slash_in_non_pointer": [(c["claim_id"], c["urel"][:44]) for c in slashnon],
          "pointer_rows_neither_landed_nor_path_shape": [c["claim_id"] for c in fakeptr]})
    fire("C12 带尺的 bare_number 档不等于「该列字面是个数」：两读数之差必须逐枚点名（v4 面 §二 的 18 档由此定价）",
         len(literal) < len(firstdigit) and bool(firstdigit)
         and all(G.parse_number(r["prediction_urel"]) is None for r in firstdigit)
         and all(G.parse_number(r["prediction_urel"]) is not None for r in literal),
         {"literal": [r["claim_id"] for r in literal],
          "first_digit_only": [(r["claim_id"], r["prediction_urel"][:40]) for r in firstdigit]})
    details = []
    for cid in contam:
        row = by_id[cid]
        printed = v4chan[cid]["priced"]["shape"]
        details.append((cid, printed, row["urel"], row["band_ruler_reads"],
                        row["numeral_misread_as_band"]))
    fire("C10 门禁的违规键 key_of 用 os.path.relpath(文件, ROOT)，跨盘即 ValueError ⇒ 基线键把盘符写进了语义（本轮改用 basename 自建键跑通实验）",
         harm["gate_key_of_on_temp_path"].startswith("path is on mount"), harm["gate_key_of_on_temp_path"])
    fire("C9 上一轮录取集的污染逐枚点名：v4 面对这些行的误差棒列印 bare_number，而该串是路径（数字来自目录名）；散文支单列",
         bool(contam) and any(d[1] == "bare_number" for d in details)
         and all(d[1] == d[3] for d in details) and len(details) == len(contam), details)
    return out


def main():
    rows, paths = G.scan_registry()
    if not paths or not rows:
        raise Fatal("扫描集为空（%d 文件 / %d 行）——不许在空台账上出分型" % (len(paths), len(rows)))
    flagc = collections.Counter(r["flag"] for r in rows)
    nonempty = [r for r in rows if r["flag"] != "empty"]
    classes, grid = census(nonempty)
    if classes["other"]:
        raise Fatal("有 %d 行归不进词表（%s）——补词表，别放宽判据"
                    % (len(classes["other"]), [c["claim_id"] for c in classes["other"]][:6]))
    if sum(len(v) for v in classes.values()) != len(nonempty):
        raise Fatal("分型不闭合：%d ≠ 非空行 %d"
                    % (sum(len(v) for v in classes.values()), len(nonempty)))
    if not classes["pointer_in_urel"]:
        raise Fatal("指针型为空——本轮的核心发现无输入，不许出判决")

    v4f = json.load(io.open(V4_FACE, encoding="utf-8", errors="ignore"))
    v4chan = dict((c["claim_id"], c) for c in v4f["channels"])
    sc_face = dict(v4f["funnel"]["shape_counts"])
    mine = collections.Counter()
    for r in nonempty:
        if r["prediction_value"]:
            mine[read_band(r["prediction_urel"])[0]] += 1
    if dict(mine) != sc_face:
        raise Fatal("与 v4 面口径不符：本册带尺 %s vs 面 %s（两把尺子必须同口径）" % (dict(mine), sc_face))
    face_ids = set(c["claim_id"] for c in v4f["channels"])
    ptr_rows = classes["pointer_in_urel"]
    ptr_ids = set(c["claim_id"] for c in ptr_rows)
    contam = sorted(face_ids & ptr_ids)
    by_id = dict((c["claim_id"], c) for c in ptr_rows)
    contam_split = collections.Counter()
    for cid in contam:
        printed = v4chan[cid]["priced"]["shape"]
        if printed != by_id[cid]["band_ruler_reads"]:
            raise Fatal("同一串在两台的带尺下读数不一致（%s：v4 印 %s、本册读 %s）——尺子先对齐再谈分类"
                        % (cid, printed, by_id[cid]["band_ruler_reads"]))
        contam_split["v4_%s" % printed] += 1
    if sum(contam_split.values()) != len(contam):
        raise Fatal("污染子型不闭合")

    for c in classes["pointer_in_urel"]:
        c["resolves"] = resolve_pointer(c["owner"], c["urel"])[0]
    res = dict(collections.Counter(c["resolves"] for c in classes["pointer_in_urel"]))
    if sum(res.values()) != len(classes["pointer_in_urel"]):
        raise Fatal("指针落点子型不闭合：%s" % res)
    if res.get("file", 0) + res.get("dir", 0) + res.get("file_by_extension", 0) == 0:
        raise Fatal("一条指针都没落地——先把基准路径修对，再谈「悬空」")

    cand0 = [c for c in classes["pointer_in_urel"]
               if c["resolves"] in ("file", "dir", "file_by_extension") and not c["pv"]]
    if not cand0:
        raise Fatal("没有一条「值为空＋指针能落地」的行——删除支实验无输入")
    literal = [r for r in nonempty if r["prediction_value"]
               and G.parse_number(r["prediction_urel"]) is not None]
    firstdigit = [r for r in nonempty if r["prediction_value"]
                  and read_band(r["prediction_urel"])[0] == "bare_number"
                  and G.parse_number(r["prediction_urel"]) is None]
    ptr0 = cand0[0]
    harm = harm_experiment(ptr0, ptr0["urel"])
    ctl = run_controls(v4f["flips"], classes, harm, contam, by_id, v4chan, literal, firstdigit)
    fired = sum(1 for c in ctl if c["fired"])
    rc = 0 if fired == len(ctl) else 1

    cur = classes["urel_other_currency"]
    priced = [c for c in cur if c.get("rel_converted") is not None]
    face = collections.OrderedDict()
    face["instrument"] = os.path.basename(__file__)
    face["generated_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    face["rc"] = rc
    face["single_sources"] = dict((k, os.path.relpath(v, ROOT).replace("\\", "/")) for k, v in [
        ("gate", GATE_SRC), ("band_ruler", V4_SRC), ("carrier", CARRIER), ("cross_face", V4_FACE)])
    face["totals"] = {"files": len(paths), "rows": len(rows), "flag_counts": dict(flagc),
                      "nonempty_rows": len(nonempty), "ok_rows_whole_corpus": int(flagc.get("ok", 0))}
    face["class_counts"] = dict((k, len(v)) for k, v in classes.items())
    face["closure"] = {"sum_classes": int(sum(len(v) for v in classes.values())),
                       "equals_nonempty_rows": bool(sum(len(v) for v in classes.values()) == len(nonempty))}
    face["grid_pv_x_band"] = dict(grid)
    face["band_shapes_vs_v4_face"] = {"mine": dict(mine), "face": sc_face,
                                      "admission_note": "v4 只收 prediction_value 非空的行；指针型 pv 为空，结构上落在 v4 面的录取集之外"}
    face["urel_literal_vs_band_ruler"] = {
        "rows_in_v4_admission": len([r for r in nonempty if r["prediction_value"]]),
        "urel_parses_as_number_by_gate": len(literal),
        "urel_parses_named": [r["claim_id"] for r in literal],
        "band_ruler_took_first_digit_from_prose_or_path": len(firstdigit),
        "band_ruler_named": [r["claim_id"] for r in firstdigit],
        "consequence": "v4 面 §二 把带尺读到首数字的行印成 bare_number，其中只有 urel_parses_as_number_by_gate 条真由该列字面解析；"
                       "v4 面不可改（数据件、md5 已钉），本册 grid 与字面账为准"}
    face["v4_face_admission_contaminated_by_pointer"] = {
        "n": len(contam), "claim_ids": contam,
        "note": "v4 面的 shape_counts 里 bare_number 档把这几行的路径读成了数（数字来自目录名）；v4 面不可改，本册的 grid 为准",
        "split_by_v4_printed_shape": dict(contam_split),
        "rows": [dict(claim_id=c, urel=by_id[c]["urel"], v4_printed_shape=v4chan[c]["priced"]["shape"],
                       numeral_read_by_band_ruler=by_id[c]["numeral_misread_as_band"]) for c in contam]}
    face["pointer_class"] = {"n": len(classes["pointer_in_urel"]), "resolves": res,
                             "by_owner": dict(collections.Counter(c["owner"] for c in classes["pointer_in_urel"])),
                             "rows": classes["pointer_in_urel"]}
    face["currency_class"] = {"n": len(cur), "convertible_now": len(priced),
                              "blocked_by_value_side": len(cur) - len(priced),
                              "pv_state_counts": dict(collections.Counter(c["pv_state"] for c in cur)),
                              "rows": cur}
    face["prose_class"] = {"n": len(classes["urel_prose_band"]),
                           "pv_state_counts": dict(collections.Counter(c["pv_state"] for c in classes["urel_prose_band"])),
                           "rows": classes["urel_prose_band"]}
    face["value_class"] = {"n": len(classes["value_unparseable"]), "rows": classes["value_unparseable"]}
    face["absent_band_class"] = {"n": len(classes["urel_absent"]), "rows": classes["urel_absent"]}
    face["exact_claim_class"] = {"n": len(classes["urel_zero_exact_noninteger"]),
                                 "rows": classes["urel_zero_exact_noninteger"]}
    face["advice_text"] = dict((k, G.SUGGESTION[k]) for k in sorted(G.SUGGESTION))
    face["harm_experiment"] = harm
    face["controls"] = ctl
    face["controls_fired"] = "%d/%d" % (fired, len(ctl))

    if not os.path.isdir(OUT_DIR):
        raise Fatal("输出目录不在盘：%s" % OUT_DIR)
    out = os.path.join(OUT_DIR, FACE)
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(face, ensure_ascii=False, indent=1))
    if not QUIET:
        print(json.dumps({"class_counts": face["class_counts"], "grid": face["grid_pv_x_band"],
                          "pointer_resolves": res, "controls": face["controls_fired"],
                          "blank_after": harm["branch_blank"]["violations_after"],
                          "zero_flags": harm["branch_fill_zero"]["flags"]},
                         ensure_ascii=False, indent=1))
    print("WROTE=%s rc=%d" % (out, rc))
    if rc:
        raise Fatal("对照未全点火：%d/%d（%s）" % (fired, len(ctl),
                    [c["name"] for c in ctl if not c["fired"]]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
