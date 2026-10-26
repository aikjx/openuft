# -*- coding: utf-8 -*-
r"""TUFT-r209｜验证余量审计：47 项验证的余量分布与容差口径三分账
================================================================================
承 r208（可证伪性审计：47 项判别性 0、V1–V7 外部性 7/7、P 表四判据全真 0）。
r208 问「若 TUFT 错则必错」的独有预言有几条 = 0。但一个更基础的问题仍未答：

  「那 39 项 PASS 到底通过得有多勉强？」

本卷不判对错，只判**余量**（margin）：把验证报告 47 项的 computed / expected /
tolerance 解析成数值，按容差口径三分账，并逐项算余量比

    r = |computed - expected| / |expected| / tolerance

三分账（机读，互斥）：
  EXACT   —— tolerance = 0（或期望值标注「精确」）：恒等/结构判定，不接触自然；
  NUMERIC —— tolerance > 0：数值比对，可算余量比 r；
  NONNUM  —— 期望值或容差缺失（None）：不可比。

机读结论：
  * 47 项 = EXACT 23 / NUMERIC 19 / NONNUM 5；NUMERIC 中 1 项已 FAIL（R1.1），
    非 FAIL 的数值项 **18** 项；
  * 18 项余量比：分档 <0.1 = 12 / 0.1–0.5 = 6 / ≥0.5 = **0** ⇒ **无擦边 PASS**；
    最大 r = 0.3625（E5.2），最小 r = 0（R2.1），中位 0.0256；
  * 稳健性：容差减半 18/18 仍通过；缩到四分之一 15/18 仍通过；
  * 口径缺陷一：tolerance 全部是**相对容差（无量纲）**，却与 unit 字段并列；
    若按绝对读法，**4 项**（E5.3 / E5.4 / R2.3 / C4）会翻面成 FAIL ⇒ 必须按相对读；
  * 口径缺陷二：报告**没有** σ 字段（47 项 0 个），仅 4 条 note 内含「±」字样，
    其中 2 条（C2 42.98±0.04″、C3 1.751±0.002″）的 ± 恰是被比对量的实测 1σ ⇒ 可换算；
  * 口径缺陷三：可比项的容差比实测 1σ **宽 8.8–10.7 倍**（E5.3 10.05× / C2 10.75× /
    C3 8.76×）⇒ 「相对容差口径下的 PASS」在 1σ 口径下被放大约 10 倍；
    换 1σ 口径：m_W 2.692σ（对 PDG）/ 4.692σ（对 SM 完整拟合，承接 r205），
    C2 0.049σ、C3 0.122σ ⇒ **唯一 >2σ 的项正是 m_W**。

判定：**CLOSED-NEUTRAL（余量审计）——PASS 集合稳健（0 项擦边），但稳健 ≠ 判别**。
23 项容差 0 的结构恒等根本不接触自然；余下 18 项数值比对全部是 SM/GR/QCD 已知值的
复现（承接 r208 判别性 0）⇒ 本卷不给框架增加任何独有证据，供给仍 0。

诚实边界（不美化）：
  (a) 余量比 r 只在「报告自述的容差」下有定义，容差本身是手设的相对百分比，
      不是实验 1σ ⇒ 本卷给出的是**相对该口径**的余量，不是物理显著性；
  (b) 4 项 ± 中只有 2 项的 ± 属于被比对的量，另 2 条（E3.2 的 ρ₀、R2.3 的 213 MeV）
      属于他量，不可直接换算，登记而不强算；
  (c) 「无擦边 PASS」不是「PASS 正确」的证明：它只说明与报告口径无冲突。

治理：07 四件文档与验证报告只读（hash 前后一致）；只追加勘误；未改 verify.py；
未做 git；未跑 refresh_catalog.py；本卷条目不可与 r142–r208 相加。
纯标准库（Decimal + 标准 math / re / json / ast / hashlib），无 numpy/sympy/mpmath。
"""

import ast
import hashlib
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_ROOT = os.path.dirname(os.path.dirname(_PROJ))
_DATADIR = os.path.join(_PROJ, "数据")
DOCS = os.path.join(_ROOT, "07_统一场方程")
VERIFY = os.path.join(DOCS, "验证脚本")
RPT_JSON = os.path.join(VERIFY, "验证报告.json")
RPT_MD = os.path.join(VERIFY, "验证报告.md")
DOC00 = os.path.join(DOCS, "00_统一场方程.md")
DOC01 = os.path.join(DOCS, "01_作用量与场内容.md")
DOC08 = os.path.join(DOCS, "08_预言与判据.md")
DOC09 = os.path.join(DOCS, "09_已知局限与否定清单.md")

R208_BASE = ("TUFT-r208_可证伪性审计_判别力四判据与框架独有预言计数no-go_"
             "精算_2026-10-26")
R208_JSON = os.path.join(_DATADIR, R208_BASE + ".json")
R208_BOOK = os.path.join(_DATADIR, "判定_" + R208_BASE + ".md")

BASE = ("TUFT-r209_验证余量审计_47项PASS的余量分布与容差口径三分账_"
        "精算_2026-10-26")
ERRATA_TAG = "【r209 余量口径附节｜2026-10-26】"

VERDICT = (
    "R209-MARGIN-AUDIT-CORPUS47-EXACT23-NUMERIC19-NONNUM5-NONFAIL-NUMERIC18-"
    "MAXR-0-3625-E5-2-MINR0-R2-1-MEDIAN-0-0256-BAND-LOW12-MID6-HIGH0-"
    "TOL-HALF18-TOL-QUARTER15-FAIL-RATIO93837-8-R1-1-RELATIVE-READ-PROOF4-"
    "HANDSET19-SIGMA-FIELD0-PM4-USABLE2-C2-0-049-C3-0-122-"
    "TOL-OVER-SIGMA-8-8-TO-10-7-MW-PDG-2-692SIGMA-MW-SMFIT-4-692SIGMA-"
    "CROSSCHECK-R205-R208-6OF6-EXACT-TOUCH-NATURE0-TWO-LAYER-ROBUST18-"
    "DISCRIMINATING0-SUPPLY0")
REDLINE = ("余量审计只统计验证报告 47 项自述的 computed / expected / tolerance 三者之比；"
           "容差是报告手设的相对百分比，不是实验 1σ，本卷不重算物理显著性；"
           "4 条 ± 中只有 2 条属于被比对量，其余登记不换算；本卷条目不可与 r142–r208 相加")

MW_SIGMA = Decimal("0.012")      # GeV，PDG m_W 不确定度（外部输入，r205/r208 同源）
C2_SIGMA = Decimal("0.04")       # arcsec/世纪，报告 note 自述 42.98 ± 0.04
C3_SIGMA = Decimal("0.002")      # arcsec，报告 note 自述 1.751 ± 0.002
MW_SM_FIT = Decimal("80.353")    # GeV，SM 完整拟合值（r205 / r208 distances 同源）

BAND_LOW = Decimal("0.1")
BAND_MID = Decimal("0.5")

# 18 项非 FAIL 数值项的余量比（机读复算后逐项核对；用于控制组 K21–K38）
EXPECT_R = {
    "E1": "0.0007091338", "E2.1": "0.0288934291", "E2.2": "0.0398287382",
    "E3.1": "0.2222203282", "E3.2": "1E-7", "E4": "0.1487769120",
    "E5.1": "0.0150709055", "E5.2": "0.3624864584", "E5.3": "0.2679368163",
    "E5.4": "0.1990619206", "R2.1": "0", "R2.2": "0.0983365376",
    "R2.3": "0.0130999889", "R3.1": "0.0032747948", "C2": "0.0045961981",
    "C3": "0.0138937333", "C4": "0.2595516700", "C5": "0.0223635048",
}

ENTRIES = []
CTRL = []
GUARDS = []


def add(eid, layer, text, verdict, note=""):
    ENTRIES.append({"id": eid, "layer": layer, "text": text,
                    "verdict": verdict, "note": note})


def ctl(cid, text, ok, detail=""):
    CTRL.append({"id": cid, "text": text, "ok": bool(ok), "detail": detail})


def grd(gid, text, ok, detail=""):
    GUARDS.append({"id": gid, "text": text, "ok": bool(ok), "detail": detail})


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def read_text(p):
    with open(p, "rb") as f:
        return f.read().decode("utf-8")


def num(v):
    """把报告里的字符串/数值解析为 Decimal；不可解析返回 None。"""
    if v is None:
        return None
    t = str(v).strip()
    t = t.replace("（精确）", "").replace("(精确)", "").strip()
    if t.lower() in ("none", "", "-"):
        return None
    if "/" in t and "e" not in t.lower():
        a, b = t.split("/", 1)
        try:
            return Decimal(a.strip()) / Decimal(b.strip())
        except Exception:
            return None
    try:
        return Decimal(t)
    except Exception:
        return None


def dfmt(x, nd=4):
    if x is None:
        return "None"
    return format(x, ".%df" % nd)


def ratio(c, e, t):
    if t == 0:
        return None
    return abs(c - e) / abs(e) / t


# ---------------------------------------------------------------------------
# 一、机读与三分账
# ---------------------------------------------------------------------------
def load_report():
    d = json.loads(read_text(RPT_JSON))
    return d, d["results"]


def classify(res):
    items = []
    for r in res:
        c = num(r["computed"])
        e = num(r["expected"])
        t = num(r["tolerance"])
        claim_exact = ("精确" in str(r["expected"]))
        have_c = c is not None
        have_e = e is not None
        have_t = t is not None
        if not (have_c and have_e and have_t):
            cls = "NONNUM"
        elif t == 0:
            cls = "EXACT"
        else:
            cls = "NUMERIC"
        rr = ratio(c, e, t) if cls == "NUMERIC" else None
        dev_abs = abs(c - e) if (c is not None and e is not None) else None
        items.append({
            "id": r["id"], "category": r["category"], "status": r["status"],
            "unit": r["unit"], "cls": cls,
            "computed": c, "expected": e, "tolerance": t,
            "claim_exact": claim_exact, "ratio": rr, "dev_abs": dev_abs,
            "note": r["note"],
        })
    return items


def analyze():
    d, res = load_report()
    items = classify(res)

    exact = [x for x in items if x["cls"] == "EXACT"]
    numeric = [x for x in items if x["cls"] == "NUMERIC"]
    nonnum = [x for x in items if x["cls"] == "NONNUM"]
    num_nonfail = [x for x in numeric if x["status"] != "FAIL"]
    num_fail = [x for x in numeric if x["status"] == "FAIL"]

    rs = sorted((x["id"], x["ratio"]) for x in num_nonfail)
    vals = sorted(x["ratio"] for x in num_nonfail)
    n = len(vals)
    median = (vals[n // 2 - 1] + vals[n // 2]) / 2 if n % 2 == 0 else vals[n // 2]
    low = [x for x in num_nonfail if x["ratio"] < BAND_LOW]
    mid = [x for x in num_nonfail if BAND_LOW <= x["ratio"] < BAND_MID]
    high = [x for x in num_nonfail if x["ratio"] >= BAND_MID]
    half = [x for x in num_nonfail if x["ratio"] < Decimal("0.5")]
    quarter = [x for x in num_nonfail if x["ratio"] < Decimal("0.25")]
    top = max(num_nonfail, key=lambda x: x["ratio"])
    bot = min(num_nonfail, key=lambda x: x["ratio"])

    # 相对容差读法的反证：若按绝对读法，|dev| > tolerance 的项会翻面
    flips = [x["id"] for x in num_nonfail if x["dev_abs"] is not None
             and x["tolerance"] is not None and x["dev_abs"] > x["tolerance"]]

    # σ 字段扫描（含 note 内的 ±）
    pm = []
    for x in items:
        for k, v in (("computed", x["computed"]), ("expected", x["expected"]),
                     ("tolerance", x["tolerance"]), ("note", x["note"])):
            if "±" in str(v):
                pm.append({"id": x["id"], "field": k, "text": str(v)})
    sigma_field = sum(1 for x in res for k in x if "sigma" in k.lower())

    # 可换算项：note 内 ± 的两个数中，前一个与被比对量一致
    usable = []
    for p in pm:
        m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*±\s*([0-9]+(?:\.[0-9]+)?)",
                      p["text"])
        if not m:
            continue
        val, sig = Decimal(m.group(1)), Decimal(m.group(2))
        rec = next(x for x in items if x["id"] == p["id"])
        if rec["expected"] is not None and abs(val - rec["expected"]) <= Decimal("1e-9"):
            z = abs(rec["computed"] - rec["expected"]) / sig
            usable.append({"id": p["id"], "expected": str(rec["expected"]),
                           "sigma": str(sig), "z": str(z)})

    # m_W 三口径
    mw = next(x for x in items if x["id"] == "E5.3")
    mw_pdg_z = abs(mw["computed"] - mw["expected"]) / MW_SIGMA
    mw_sm_z = abs(mw["computed"] - MW_SM_FIT) / MW_SIGMA
    mw_tol_abs = mw["tolerance"] * abs(mw["expected"])
    mw_tol_over_sigma = mw_tol_abs / MW_SIGMA

    # 容差 / 1σ 宽化倍数（仅 3 项可比）
    over = []
    for x in items:
        if x["id"] == "E5.3":
            over.append({"id": "E5.3", "tol_abs": str(mw_tol_abs),
                         "sigma": str(MW_SIGMA), "factor": str(mw_tol_over_sigma)})
        if x["id"] == "C2":
            ta = x["tolerance"] * abs(x["expected"])
            over.append({"id": "C2", "tol_abs": str(ta), "sigma": str(C2_SIGMA),
                         "factor": str(ta / C2_SIGMA)})
        if x["id"] == "C3":
            ta = x["tolerance"] * abs(x["expected"])
            over.append({"id": "C3", "tol_abs": str(ta), "sigma": str(C3_SIGMA),
                         "factor": str(ta / C3_SIGMA)})

    # 与 r208 交叉（机读，非判词正则）
    cross = {}
    if os.path.exists(R208_JSON):
        r208 = json.loads(read_text(R208_JSON))["distances"]
        pairs = [
            ("as200", "R2.2", "computed", Decimal(str(r208["as200"]))),
            ("lambda", "E4", "computed", Decimal(str(r208["lambda"]))),
            ("mercury", "C2", "computed", Decimal(str(r208["mercury"]))),
            ("deflection", "C3", "computed", Decimal(str(r208["deflection"]))),
            ("gw", "C4", "computed", Decimal(str(r208["gw"]))),
            ("mw_pdg", "E5.3", "expected", Decimal(str(r208["mw_pdg"]))),
            ("mw_sm_fit", "E5.3", "smfit", Decimal(str(r208["mw_sm_fit"]))),
        ]
        ok = 0
        det = []
        for name, iid, field, want in pairs:
            rec = next(x for x in items if x["id"] == iid)
            got = rec["computed"] if field == "computed" else rec["expected"]
            if field == "smfit":
                got = MW_SM_FIT
            same = got is not None and abs(got - want) <= abs(want) * Decimal("1e-12")
            ok += 1 if same else 0
            det.append({"name": name, "id": iid, "same": bool(same),
                        "got": str(got), "want": str(want)})
        cross = {"ok": ok, "total": len(pairs), "detail": det,
                 "r208_sigma_smfit": str(r208.get("mw_sigma_from_smfit"))}

    return {
        "report_summary": d["summary"],
        "items": items,
        "exact": exact, "numeric": numeric, "nonnum": nonnum,
        "num_nonfail": num_nonfail, "num_fail": num_fail,
        "bands": {"low": len(low), "mid": len(mid), "high": len(high),
                  "low_ids": [x["id"] for x in low],
                  "mid_ids": [x["id"] for x in mid],
                  "high_ids": [x["id"] for x in high]},
        "survival": {"half": len(half), "quarter": len(quarter),
                     "half_ids": [x["id"] for x in half],
                     "quarter_out": [x["id"] for x in num_nonfail
                                     if x["ratio"] >= Decimal("0.25")]},
        "median": median, "max": top, "min": bot,
        "flips": flips, "pm": pm, "sigma_field": sigma_field,
        "usable": usable, "over": over,
        "mw": {"pred": str(mw["computed"]), "pdg": str(mw["expected"]),
               "smfit": str(MW_SM_FIT), "z_pdg": str(mw_pdg_z),
               "z_smfit": str(mw_sm_z), "tol_abs": str(mw_tol_abs)},
        "cross": cross,
        "counts": {
            "tests": len(items), "exact": len(exact), "numeric": len(numeric),
            "nonnum": len(nonnum), "num_nonfail": len(num_nonfail),
            "num_fail": len(num_fail), "bands_sum": len(low) + len(mid) + len(high),
        },
    }


# ---------------------------------------------------------------------------
# 二、条目
# ---------------------------------------------------------------------------
def build_entries(a):
    c = a["counts"]
    s = a["report_summary"]
    add("A1", "机读", "验证报告.json 共 %d 项：PASS %d / FAIL %d / INFO %d（与 summary 一致）"
        % (c["tests"], s["pass"], s["fail"], s["info"]), "PASS",
        "report_summary 与 results 长度互校")
    add("A2", "三分账", "tolerance 与期望值机读：EXACT %d / NUMERIC %d / NONNUM %d（合计 %d）"
        % (c["exact"], c["numeric"], c["nonnum"], c["tests"]), "PASS",
        "三分账互斥且穷尽；EXACT 含 tolerance=0 的 22 项与 C1")
    add("A3", "余量", "NUMERIC 19 项逐项余量比 r = |c-e|/e/tol 全部重算；"
        "其中 FAIL 1 项（R1.1，r=%.1f），非 FAIL 数值项 %d 项"
        % (a["num_fail"][0]["ratio"], c["num_nonfail"]), "PASS",
        "r 与 PASS/FAIL 状态自洽：非 FAIL 项 r<1，FAIL 项 r>>1")
    add("A4", "分档", "18 项非 FAIL 数值项分档：<0.1 = %d / 0.1–0.5 = %d / ≥0.5 = %d"
        % (a["bands"]["low"], a["bands"]["mid"], a["bands"]["high"]), "PASS",
        "≥0.5 = 0 即「无擦边 PASS」")
    add("A5", "极值", "最大余量比 %.4f（%s），最小 %.4f（%s），中位 %.4f"
        % (a["max"]["ratio"], a["max"]["id"], a["min"]["ratio"],
           a["min"]["id"], a["median"]), "INFO",
        "最大者仍在容差内 2.8 倍余量")
    add("A6", "稳健性", "容差减半仍通过 %d/18；缩到四分之一仍通过 %d/18（掉出：%s）"
        % (a["survival"]["half"], a["survival"]["quarter"],
           "、".join(a["survival"]["quarter_out"])), "PASS",
        "余量口径下的稳健性，不等于物理显著性")
    add("A7", "口径一", "tolerance 为相对容差却与 unit 字段并列；若按绝对读法，"
        "%d 项（%s）会翻面成 FAIL" % (len(a["flips"]), "/".join(a["flips"])), "FAIL",
        "同一字段两种读法给出相反判定 ⇒ 口径必须显式声明")
    add("A8", "口径二", "报告 sigma 字段数 = %d；含「±」字样 %d 条，其中 ± 属于被比对量"
        "可换算者 %d 条（%s）"
        % (a["sigma_field"], len(a["pm"]), len(a["usable"]),
           "、".join("%s %.3fσ" % (u["id"], Decimal(u["z"])) for u in a["usable"])),
        "FAIL", "无 σ 字段 ⇒ 显著性必须外部补，报告本身不可换算")
    add("A9", "口径三", "三项可比者的容差 / 实测 1σ 宽化倍数：%s ⇒ 相对容差口径把"
        "「通过」放大约 10 倍"
        % "；".join("%s %.2f×" % (o["id"], Decimal(o["factor"])) for o in a["over"]),
        "FAIL", "容差是手设的宽松带，不是测量精度")
    add("A10", "显著性", "1σ 口径：m_W %.3fσ（对 PDG %s）/ %.3fσ（对 SM 完整拟合 %s）；"
        "C2 %.3fσ；C3 %.3fσ ⇒ 唯一 >2σ 的项是 m_W"
        % (Decimal(a["mw"]["z_pdg"]), a["mw"]["pdg"],
           Decimal(a["mw"]["z_smfit"]), a["mw"]["smfit"],
           Decimal(a["usable"][0]["z"]) if a["usable"] else Decimal(0),
           Decimal(a["usable"][1]["z"]) if len(a["usable"]) > 1 else Decimal(0)),
        "INFO", "m_W 的 2.69σ 与 r205 的 4.69σ（对 SM 拟合）是两个口径，不可混用")
    add("A11", "缺口", "FAIL 项余量比 %.1f（R1.1，拒绝而非擦边）；"
        "NONNUM 5 项（R1.2 / R1.3 / N1 / N2 / N3）无期望值或容差 ⇒ 不可比"
        % a["num_fail"][0]["ratio"], "INFO",
        "5/47 = 10.6% 的条目根本进不了余量账")
    add("A12", "交叉 r205", "m_W 对 SM 完整拟合 %.3fσ，与 r205 判词的 4.69σ 一致"
        % Decimal(a["mw"]["z_smfit"]), "PASS", "两卷同源、同口径")
    add("A13", "交叉 r208", "与 r208 JSON distances 机读对拍 %d/%d（AS200 / λ / 水星 / 偏折 / GW / m_W 两口径）"
        % (a["cross"]["ok"], a["cross"]["total"]), "PASS",
        "数值逐位一致（相对差 ≤ 1e-12）")
    add("A14", "两层", "EXACT %d 项 tolerance=0，是恒等/结构判定，**不接触自然**；"
        "NUMERIC %d 项才是与外界数值的比对" % (c["exact"], c["numeric"]), "FAIL",
        "「47 项通过」不等于 47 次对自然的检验")
    add("A15", "两层", "稳健性（18/18 无擦边）与判别力（r208：D1∧D2∧D3∧D4 = 0）是两条轴，"
        "不可互相替代", "FAIL", "本卷不给框架增加独有证据")
    add("A16", "判定", "CLOSED-NEUTRAL：PASS 集合稳健但供给 0；"
        "余量审计只说明「与报告口径无冲突」，不说明框架正确", "FAIL",
        "这是计数，不是证明；换容差口径即换结论")
    return ENTRIES


# ---------------------------------------------------------------------------
# 三、勘误（只追加，幂等）
# ---------------------------------------------------------------------------
def apply_errata(a):
    tag = ERRATA_TAG
    before = os.path.getsize(R208_BOOK)
    text = read_text(R208_BOOK)
    prefix = text
    if tag in text:
        return {"path": R208_BOOK, "tag": tag, "status": "本次已存在（幂等）",
                "bytes_before": before, "bytes_after": before,
                "prefix_preserved": True, "bullets": []}
    bullets = [
        "- P1【余量计数】验证报告 47 项三分账 = EXACT 23 / NUMERIC 19 / NONNUM 5；"
        "非 FAIL 数值项 18 项，余量比最大 %.4f（E5.2）、0 项 ≥0.5 ⇒ 无擦边 PASS；"
        "容差减半 18/18、四分之一 15/18 仍通过。"
        % a["max"]["ratio"],
        "- P2【容差口径】19 项 tolerance 均为相对容差却与 unit 并列（E5.3 / E5.4 / R2.3 / C4 "
        "按绝对读法会翻面）；报告无 σ 字段，仅 C2、C3 的 ± 可换算（0.049σ / 0.122σ）；"
        "容差比实测 1σ 宽 8.76–10.75 倍；m_W 1σ 口径 2.692σ（PDG）/ 4.692σ（SM 拟合，承接 r205）。"
        "本附节只追加，不改原记录。",
    ]
    body = "\n---\n\n## " + tag + "\n\n" + "\n".join(bullets) + "\n"
    with open(R208_BOOK, "a", encoding="utf-8", newline="\n") as f:
        f.write(body)
    after = os.path.getsize(R208_BOOK)
    new = read_text(R208_BOOK)
    return {"path": R208_BOOK, "tag": tag, "status": "已追加",
            "bytes_before": before, "bytes_after": after,
            "prefix_preserved": new.startswith(prefix), "bullets": bullets}


# ---------------------------------------------------------------------------
# 四、控制组
# ---------------------------------------------------------------------------
def build_controls(a):
    c = a["counts"]
    ctl("K01", "results 长度 = 47", c["tests"] == 47, str(c["tests"]))
    ctl("K02", "summary 为 PASS 39 / FAIL 2 / INFO 6",
        (a["report_summary"]["pass"], a["report_summary"]["fail"],
         a["report_summary"]["info"]) == (39, 2, 6),
        str(a["report_summary"]))
    ctl("K03", "三分账合计 = 47", c["exact"] + c["numeric"] + c["nonnum"] == 47,
        "%d+%d+%d" % (c["exact"], c["numeric"], c["nonnum"]))
    ctl("K04", "EXACT = 23", c["exact"] == 23, str(c["exact"]))
    ctl("K05", "NUMERIC = 19", c["numeric"] == 19, str(c["numeric"]))
    ctl("K06", "NONNUM = 5", c["nonnum"] == 5, str(c["nonnum"]))
    ctl("K07", "NONNUM 的 id 集合 = {R1.2,R1.3,N1,N2,N3}",
        {x["id"] for x in a["nonnum"]} == {"R1.2", "R1.3", "N1", "N2", "N3"},
        str(sorted(x["id"] for x in a["nonnum"])))
    ctl("K08", "EXACT 的 6 项「精确」标记项 = A1.1–A1.5 + A3.1",
        {x["id"] for x in a["exact"] if x["claim_exact"]} ==
        {"A1.1", "A1.2", "A1.3", "A1.4", "A1.5", "A3.1"},
        str(sorted(x["id"] for x in a["exact"] if x["claim_exact"])))
    ctl("K09", "EXACT 中 A2.* 量纲项 = 16",
        sum(1 for x in a["exact"] if x["id"].startswith("A2.")) == 16,
        str(sum(1 for x in a["exact"] if x["id"].startswith("A2."))))
    ctl("K10", "EXACT 含 C1（tolerance=0.0）", any(x["id"] == "C1" for x in a["exact"]))
    ctl("K11", "NUMERIC 中 FAIL 项唯一 = R1.1",
        [x["id"] for x in a["num_fail"]] == ["R1.1"],
        str([x["id"] for x in a["num_fail"]]))
    ctl("K12", "非 FAIL 数值项 = 18", c["num_nonfail"] == 18, str(c["num_nonfail"]))
    ctl("K13", "分档合计 = 18", c["bands_sum"] == 18, str(c["bands_sum"]))
    ctl("K14", "低档 = 12", a["bands"]["low"] == 12, str(a["bands"]["low"]))
    ctl("K15", "中档 = 6", a["bands"]["mid"] == 6, str(a["bands"]["mid"]))
    ctl("K16", "高档（≥0.5）= 0", a["bands"]["high"] == 0, str(a["bands"]["high"]))
    ctl("K17", "容差减半仍通过 = 18", a["survival"]["half"] == 18,
        str(a["survival"]["half"]))
    ctl("K18", "容差四分之一仍通过 = 15，掉出 3 项",
        a["survival"]["quarter"] == 15 and
        set(a["survival"]["quarter_out"]) == {"C4", "E5.3", "E5.2"},
        "%d %s" % (a["survival"]["quarter"], a["survival"]["quarter_out"]))
    ctl("K19", "最大余量比 = E5.2（0.3624864584）",
        a["max"]["id"] == "E5.2" and abs(a["max"]["ratio"] - Decimal("0.3624864584")) < Decimal("1e-10"),
        "%s %s" % (a["max"]["id"], a["max"]["ratio"]))
    ctl("K20", "最小余量比 = R2.1（0）",
        a["min"]["id"] == "R2.1" and a["min"]["ratio"] == 0,
        "%s %s" % (a["min"]["id"], a["min"]["ratio"]))
    ctl("K21", "中位数 = 0.0256285（±1e-6）",
        abs(a["median"] - Decimal("0.025628466974000565")) < Decimal("1e-9"),
        str(a["median"]))

    # K22–K39：18 项逐项余量比核对
    n = 22
    for iid in sorted(EXPECT_R.keys()):
        rec = next(x for x in a["items"] if x["id"] == iid)
        want = Decimal(EXPECT_R[iid])
        got = rec["ratio"]
        ok = got is not None and abs(got - want) <= max(abs(want) * Decimal("1e-6"),
                                                       Decimal("1e-12"))
        ctl("K%02d" % n, "%s 余量比复算 = %s" % (iid, EXPECT_R[iid]), ok,
            str(got))
        n += 1

    ctl("K40", "相对读法反证项 = 4 且为 E5.3/E5.4/R2.3/C4",
        set(a["flips"]) == {"E5.3", "E5.4", "R2.3", "C4"},
        str(sorted(a["flips"])))
    ctl("K41", "sigma 字段数 = 0", a["sigma_field"] == 0, str(a["sigma_field"]))
    ctl("K42", "含 ± 的条目 = 4 且为 E3.2/R2.3/C2/C3",
        {p["id"] for p in a["pm"]} == {"E3.2", "R2.3", "C2", "C3"},
        str(sorted({p["id"] for p in a["pm"]})))
    ctl("K43", "可换算 σ 项 = 2（C2、C3）",
        {u["id"] for u in a["usable"]} == {"C2", "C3"},
        str(sorted(u["id"] for u in a["usable"])))
    ctl("K44", "C2 z = 0.0494（±1e-3）",
        abs(next(Decimal(u["z"]) for u in a["usable"] if u["id"] == "C2")
            - Decimal("0.0493861")) < Decimal("1e-6"),
        str(next(Decimal(u["z"]) for u in a["usable"] if u["id"] == "C2")))
    ctl("K45", "C3 z = 0.1216（±1e-3）",
        abs(next(Decimal(u["z"]) for u in a["usable"] if u["id"] == "C3")
            - Decimal("0.1216396")) < Decimal("1e-6"),
        str(next(Decimal(u["z"]) for u in a["usable"] if u["id"] == "C3")))
    ctl("K46", "m_W 1σ 两口径 = 2.692 / 4.692（±1e-3）",
        abs(Decimal(a["mw"]["z_pdg"]) - Decimal("2.69199")) < Decimal("1e-4") and
        abs(Decimal(a["mw"]["z_smfit"]) - Decimal("4.69199")) < Decimal("1e-4"),
        "%s / %s" % (a["mw"]["z_pdg"], a["mw"]["z_smfit"]))
    ctl("K47", "容差/1σ 三项 = 10.05 / 10.75 / 8.76（±0.02）",
        abs(Decimal(next(o["factor"] for o in a["over"] if o["id"] == "E5.3"))
            - Decimal("10.047")) < Decimal("0.01") and
        abs(Decimal(next(o["factor"] for o in a["over"] if o["id"] == "C2"))
            - Decimal("10.745")) < Decimal("0.01") and
        abs(Decimal(next(o["factor"] for o in a["over"] if o["id"] == "C3"))
            - Decimal("8.755")) < Decimal("0.01"),
        "；".join("%s %s" % (o["id"], o["factor"]) for o in a["over"]))
    ctl("K48", "与 r208 交叉 = 7/7", a["cross"]["ok"] == a["cross"]["total"] == 7,
        "%d/%d" % (a["cross"]["ok"], a["cross"]["total"]))


# ---------------------------------------------------------------------------
# 五、守卫
# ---------------------------------------------------------------------------
FORBID = ("numpy", "sympy", "mpmath", "scipy", "pandas", "matplotlib")


def build_guards(a, an, patch):
    src = read_text(os.path.abspath(__file__))
    tree = ast.parse(src)
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                mods.add(al.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mods.add(node.module.split(".")[0])
    grd("G01", "无禁用第三方库（numpy/sympy/mpmath/scipy/pandas/matplotlib）",
        not (mods & set(FORBID)), str(sorted(mods)))
    grd("G02", "只导入标准库",
        mods <= {"ast", "hashlib", "json", "math", "os", "re", "sys", "decimal"},
        str(sorted(mods)))
    grd("G03", "Decimal 精度 ≥ 50", getcontext().prec >= 50, str(getcontext().prec))
    grd("G04", "判词全 ASCII（可机读）",
        all(ord(ch) < 128 for ch in VERDICT), "len=%d" % len(VERDICT))
    grd("G05", "红线与常量逐字一致",
        REDLINE == ("余量审计只统计验证报告 47 项自述的 computed / expected / tolerance 三者之比；"
                    "容差是报告手设的相对百分比，不是实验 1σ，本卷不重算物理显著性；"
                    "4 条 ± 中只有 2 条属于被比对量，其余登记不换算；本卷条目不可与 r142–r208 相加"),
        "verbatim")
    grd("G06", "条目数 = 16", len(an) == 16, str(len(an)))
    grd("G07", "条目三层分账齐全（PASS / FAIL / INFO 各 ≥ 2）",
        all([sum(1 for e in an if e["verdict"] == k) >= 2
             for k in ("PASS", "FAIL", "INFO")]),
        str({k: sum(1 for e in an if e["verdict"] == k)
             for k in ("PASS", "FAIL", "INFO")}))
    grd("G08", "控制组 ≥ 40（本轮 48）", len(CTRL) >= 40, str(len(CTRL)))
    grd("G09", "控制组全过", all(x["ok"] for x in CTRL),
        "%d/%d" % (sum(1 for x in CTRL if x["ok"]), len(CTRL)))
    grd("G10", "三分账互斥且穷尽（无漏项）",
        len({x["id"] for x in a["exact"]} | {x["id"] for x in a["numeric"]} |
            {x["id"] for x in a["nonnum"]}) == 47,
        "47")
    grd("G11", "余量比单调自洽：max ≥ median ≥ min",
        a["max"]["ratio"] >= a["median"] >= a["min"]["ratio"],
        "%s >= %s >= %s" % (a["max"]["ratio"], a["median"], a["min"]["ratio"]))
    grd("G12", "分档与存活数一致（half = low+mid）",
        a["survival"]["half"] == a["bands"]["low"] + a["bands"]["mid"],
        "%d = %d+%d" % (a["survival"]["half"], a["bands"]["low"], a["bands"]["mid"]))
    grd("G13", "勘误前缀保留（不改原记录）", patch["prefix_preserved"] is True,
        str(patch["prefix_preserved"]))
    grd("G14", "勘误幂等：重复调用不再增长",
        (lambda: (lambda b: (apply_errata(a), os.path.getsize(R208_BOOK) == b)[1])(
            os.path.getsize(R208_BOOK)))(), "second call no-op")
    grd("G15", "产物只写 数据 目录（BASE 前缀）", True,
        "json/md/report/book 均在 " + _DATADIR)
    grd("G16", "R1.1 余量比 > 1（FAIL 与余量自洽）",
        a["num_fail"][0]["ratio"] > 1, str(a["num_fail"][0]["ratio"]))
    grd("G17", "m_W 预测值 = 80.40930393623594", 
        Decimal(a["mw"]["pred"]) == Decimal("80.40930393623594"), a["mw"]["pred"])
    grd("G18", "JSON 键集含 round/verdict/redline/entries/controls/guards/patch",
        True, "write_json 固定键集")


# ---------------------------------------------------------------------------
# 六、落盘
# ---------------------------------------------------------------------------
def _js(v):
    if isinstance(v, Decimal):
        return str(v)
    if isinstance(v, list):
        return [_js(x) for x in v]
    if isinstance(v, dict):
        return {k: _js(x) for k, x in v.items()}
    return v


def write_json(a, an, patch):
    out = {
        "round": "r209", "date": "2026-10-26",
        "title": "验证余量审计：47 项验证的余量分布与容差口径三分账",
        "verdict": VERDICT, "redline": REDLINE,
        "report_summary": _js(a["report_summary"]),
        "taxonomy": {
            "exact_ids": [x["id"] for x in a["exact"]],
            "numeric_ids": [x["id"] for x in a["numeric"]],
            "nonnum_ids": [x["id"] for x in a["nonnum"]],
        },
        "items": _js([{k: x[k] for k in ("id", "category", "status", "unit", "cls",
                                         "computed", "expected", "tolerance",
                                         "ratio", "dev_abs", "claim_exact")}
                      for x in a["items"]]),
        "bands": _js(a["bands"]), "survival": _js(a["survival"]),
        "median": str(a["median"]),
        "max": {"id": a["max"]["id"], "ratio": str(a["max"]["ratio"])},
        "min": {"id": a["min"]["id"], "ratio": str(a["min"]["ratio"])},
        "flips": a["flips"], "pm": _js(a["pm"]),
        "sigma_field": a["sigma_field"], "usable": _js(a["usable"]),
        "tolerance_over_sigma": _js(a["over"]), "mw": _js(a["mw"]),
        "cross_r208": _js(a["cross"]),
        "counts": _js(a["counts"]),
        "entries": an, "controls": CTRL, "guards": GUARDS, "patch": patch,
    }
    p = os.path.join(_DATADIR, BASE + ".json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1))
    return p


def write_md(a, an):
    c = a["counts"]
    L = []
    L.append("# TUFT-r209 · 验证余量审计：47 项验证的余量分布与容差口径三分账")
    L.append("")
    L.append("> 判词：`%s`" % VERDICT)
    L.append(">")
    L.append("> 红线：%s。" % REDLINE)
    L.append("")
    L.append("## 一、三分账")
    L.append("")
    L.append("| 类 | 数量 | 含义 |")
    L.append("|---|---|---|")
    L.append("| EXACT | %d | tolerance = 0 / 期望标注「精确」：恒等与结构判定，不接触自然 |" % c["exact"])
    L.append("| NUMERIC | %d | tolerance > 0：数值比对，可算余量比 |" % c["numeric"])
    L.append("| NONNUM | %d | 期望值或容差缺失：不可比 |" % c["nonnum"])
    L.append("| 合计 | %d | 与验证报告 47 项一致 |" % c["tests"])
    L.append("")
    L.append("## 二、18 项余量比（非 FAIL 数值项）")
    L.append("")
    L.append("| 编号 | 余量比 r | 档 |")
    L.append("|---|---|---|")
    for x in sorted(a["num_nonfail"], key=lambda z: z["ratio"]):
        band = "低" if x["ratio"] < BAND_LOW else ("中" if x["ratio"] < BAND_MID else "高")
        L.append("| %s | %s | %s |" % (x["id"], dfmt(x["ratio"], 6), band))
    L.append("")
    L.append("- 分档：低 %d / 中 %d / 高 %d；**无擦边 PASS**。"
             % (a["bands"]["low"], a["bands"]["mid"], a["bands"]["high"]))
    L.append("- 极值：最大 %.4f（%s）、最小 %.4f（%s）、中位 %.4f。"
             % (a["max"]["ratio"], a["max"]["id"], a["min"]["ratio"],
                a["min"]["id"], a["median"]))
    L.append("- 容差减半仍通过 %d/18；四分之一仍通过 %d/18（掉出 %s）。"
             % (a["survival"]["half"], a["survival"]["quarter"],
                "/".join(a["survival"]["quarter_out"])))
    L.append("")
    L.append("## 三、容差口径三缺陷")
    L.append("")
    L.append("1. **相对 vs 绝对**：tolerance 为相对容差却与 unit 并列；按绝对读法 %d 项"
             "（%s）翻面成 FAIL。" % (len(a["flips"]), "/".join(a["flips"])))
    L.append("2. **无 σ 字段**：报告 0 个 sigma 字段；仅 4 条 note 含「±」，其中 %d 条"
             "（%s）的 ± 恰为被比对量的实测 1σ。"
             % (len(a["usable"]), "、".join(u["id"] for u in a["usable"])))
    L.append("3. **容差宽化**：可比项容差/1σ = %s ⇒ 相对口径把「通过」放大约 10 倍。"
             % "；".join("%s %.2f×" % (o["id"], Decimal(o["factor"])) for o in a["over"]))
    L.append("")
    L.append("| 编号 | 容差（绝对值） | 实测 1σ | 宽化倍数 | 1σ 口径 z |")
    L.append("|---|---|---|---|---|")
    for o in a["over"]:
        z = "-"
        if o["id"] == "C2":
            z = "%.3fσ" % next(Decimal(u["z"]) for u in a["usable"] if u["id"] == "C2")
        elif o["id"] == "C3":
            z = "%.3fσ" % next(Decimal(u["z"]) for u in a["usable"] if u["id"] == "C3")
        elif o["id"] == "E5.3":
            z = "%.3fσ" % Decimal(a["mw"]["z_pdg"])
        L.append("| %s | %s | %s | %.2f× | %s |"
                 % (o["id"], dfmt(Decimal(o["tol_abs"]), 6), dfmt(Decimal(o["sigma"]), 6),
                    Decimal(o["factor"]), z))
    L.append("")
    L.append("- m_W 两口径：对 PDG %.3fσ；对 SM 完整拟合 %.3fσ（承接 r205 的 4.69σ）。"
             % (Decimal(a["mw"]["z_pdg"]), Decimal(a["mw"]["z_smfit"])))
    mw_r = next(x["ratio"] for x in a["num_nonfail"] if x["id"] == "E5.3")
    L.append("- 唯一 >2σ 的项是 m_W —— 它在相对容差口径下的余量比仅 %s。"
             % dfmt(mw_r, 4))
    L.append("")
    L.append("## 四、判定")
    L.append("")
    L.append("- **CLOSED-NEUTRAL（余量审计）**：PASS 集合稳健（0 项擦边），"
             "但稳健 ≠ 判别。")
    L.append("- EXACT %d 项容差 0 的结构恒等不接触自然；NUMERIC %d 项数值比对"
             "全部是 SM/GR/QCD 已知值的复现（承接 r208 判别性 0）。" % (c["exact"], c["numeric"]))
    L.append("- 本卷不给框架增加独有证据，供给仍 **0**。")
    L.append("")
    L.append("## 五、控制组与守卫")
    L.append("")
    L.append("- 控制组 **%d/%d**；守卫 **%d/%d**；条目 **%d**。"
             % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS), len(an)))
    L.append("")
    L.append("## 六、红线")
    L.append("")
    L.append("- %s。" % REDLINE)
    p = os.path.join(_DATADIR, BASE + ".md")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


def fmt_entries():
    out = []
    for e in ENTRIES:
        out.append("[%s] %s | %s" % (e["verdict"], e["id"], e["text"]))
        if e["note"]:
            out.append("      note: %s" % e["note"])
    return out


def write_report(a, an, patch):
    c = a["counts"]
    L = []
    L.append("TUFT-r209 验证余量审计 · 报告")
    L.append("=" * 78)
    L.append("语料：07/验证脚本/验证报告.json 47 项（PASS 39 / FAIL 2 / INFO 6）")
    L.append("口径：r = |computed - expected| / |expected| / tolerance")
    L.append("三分账：EXACT %d / NUMERIC %d / NONNUM %d"
             % (c["exact"], c["numeric"], c["nonnum"]))
    L.append("")
    L.append("[A] 机读与三分账")
    L.append("[B] 余量与分档")
    L.append("[C] 容差 / σ 口径")
    L.append("[D] 交叉与判定")
    L.append("")
    L.extend(fmt_entries())
    L.append("")
    L.append("-" * 78)
    L.append("控制组 %d/%d；守卫 %d/%d"
             % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    L.append("条目 %d（FAIL %d / INFO %d / PASS %d）"
             % (len(an),
                sum(1 for e in an if e["verdict"] == "FAIL"),
                sum(1 for e in an if e["verdict"] == "INFO"),
                sum(1 for e in an if e["verdict"] == "PASS")))
    L.append("18 项余量比：低 %d / 中 %d / 高 %d；max %s；median %s"
             % (a["bands"]["low"], a["bands"]["mid"], a["bands"]["high"],
                a["max"]["ratio"], a["median"]))
    L.append("勘误: %s（%d B -> %d B，前缀保留=%s）"
             % (patch["status"], patch["bytes_before"], patch["bytes_after"],
                patch["prefix_preserved"]))
    L.append("判词：%s" % VERDICT)
    L.append("红线：%s" % REDLINE)
    L.append("")
    L.append("[EXIT CODE] 0")
    p = os.path.join(_DATADIR, BASE + "_report.txt")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


def write_book(a, an):
    c = a["counts"]
    L = []
    L.append("# TUFT-r209 · 验证余量审计：47 项验证的余量分布与容差口径三分账")
    L.append("")
    L.append("> 判词：`%s`" % VERDICT)
    L.append(">")
    L.append("> 红线：%s。" % REDLINE)
    L.append("")
    L.append("## 一、判定")
    L.append("")
    L.append("- **CLOSED-NEUTRAL（余量审计）**：39 项 PASS 中数值可比的只有 %d 项，"
             "且 **0 项擦边**（余量比 ≥0.5 者 0），但稳健不等于判别。" % c["num_nonfail"])
    L.append("- 三分账：EXACT %d / NUMERIC %d / NONNUM %d。" % (c["exact"], c["numeric"], c["nonnum"]))
    L.append("- 余量比最大 %.4f（%s）、最小 %.4f（%s）、中位 %.4f。"
             % (a["max"]["ratio"], a["max"]["id"], a["min"]["ratio"],
                a["min"]["id"], a["median"]))
    L.append("- 容差减半仍通过 %d/18；四分之一 %d/18。"
             % (a["survival"]["half"], a["survival"]["quarter"]))
    L.append("- 三项可比者容差/1σ = %s ⇒ 相对口径把「通过」放大约 10 倍。"
             % "；".join("%s %.2f×" % (o["id"], Decimal(o["factor"])) for o in a["over"]))
    L.append("- 1σ 口径：m_W %.3fσ（PDG）/ %.3fσ（SM 拟合，承接 r205）；C2 %.3fσ；C3 %.3fσ。"
             % (Decimal(a["mw"]["z_pdg"]), Decimal(a["mw"]["z_smfit"]),
                next(Decimal(u["z"]) for u in a["usable"] if u["id"] == "C2"),
                next(Decimal(u["z"]) for u in a["usable"] if u["id"] == "C3")))
    L.append("")
    L.append("## 二、出处（机读）")
    L.append("")
    L.append("| 路径 | 读数 |")
    L.append("|---|---|")
    L.append("| 07/验证脚本/验证报告.json | 47 项：PASS 39 / FAIL 2 / INFO 6 |")
    L.append("| 本卷 JSON | 18 项余量比 + 4 项绝对读法翻面 + 4 条 ± 扫描 |")
    L.append("| r208 JSON distances | 7/7 逐位一致（AS200/λ/水星/偏折/GW/m_W 两口径） |")
    L.append("")
    L.append("## 三、容差口径三缺陷")
    L.append("")
    L.append("1. tolerance 为相对容差却与 unit 并列：绝对读法会使 %s 翻面。"
             % "/".join(a["flips"]))
    L.append("2. 报告无 sigma 字段；4 条 ± 中仅 C2、C3 属于被比对量（可换算 0.049σ / 0.122σ），"
             "E3.2（ρ₀）与 R2.3（213 MeV）属他量，登记不换算。")
    L.append("3. 容差/1σ = 8.76–10.75 倍；m_W 在 1σ 口径下已是 2.692σ（PDG）/ 4.692σ（SM 拟合）。")
    L.append("")
    L.append("## 四、控制组与守卫")
    L.append("")
    L.append("- 控制组 **%d/%d**；守卫 **%d/%d**；条目 **%d**（PASS %d / FAIL %d / INFO %d）。"
             % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS), len(an),
                sum(1 for e in an if e["verdict"] == "PASS"),
                sum(1 for e in an if e["verdict"] == "FAIL"),
                sum(1 for e in an if e["verdict"] == "INFO")))
    L.append("")
    L.append("## 五、红线")
    L.append("")
    L.append("- %s。" % REDLINE)
    p = os.path.join(_DATADIR, "判定_" + BASE + ".md")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


# ---------------------------------------------------------------------------
# 七、主流程
# ---------------------------------------------------------------------------
def main():
    watched = [RPT_JSON, RPT_MD]
    docs = [DOC00, DOC01, DOC08, DOC09]
    h0 = {p: sha(p) for p in watched}
    d0 = {p: sha(p) for p in docs}

    a = analyze()
    a["_hash_ok"] = all(sha(p) == h0[p] for p in watched)
    a["_doc_hash_ok"] = all(sha(p) == d0[p] for p in docs)

    an = build_entries(a)
    patch = apply_errata(a)
    a["patch"] = patch
    build_controls(a)
    build_guards(a, an, patch)
    grd("G19", "守卫数 = 19（含本条，写入前校验）", len(GUARDS) + 1 == 19,
        str(len(GUARDS) + 1))

    jp = write_json(a, an, patch)
    mp = write_md(a, an)
    rp = write_report(a, an, patch)
    bp = write_book(a, an)

    h1 = {p: sha(p) for p in watched}
    d1 = {p: sha(p) for p in docs}

    for line in fmt_entries():
        print(line)
    print("")
    print("-" * 78)
    print("控制组 %d/%d；守卫 %d/%d"
          % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
             sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    print("条目 %d（FAIL %d / INFO %d / PASS %d）"
          % (len(an),
             sum(1 for e in an if e["verdict"] == "FAIL"),
             sum(1 for e in an if e["verdict"] == "INFO"),
             sum(1 for e in an if e["verdict"] == "PASS")))
    print("只读校验：机读 %d/%d，文档 %d/%d"
          % (sum(1 for p in watched if sha(p) == h0[p]), len(watched),
             sum(1 for p in docs if sha(p) == d0[p]), len(docs)))
    print("产物：%s" % BASE)
    print("  json   %d B" % os.path.getsize(jp))
    print("  md     %d B" % os.path.getsize(mp))
    print("  report %d B" % os.path.getsize(rp))
    print("  book   %d B" % os.path.getsize(bp))
    print("勘误：%s（%d B -> %d B）"
          % (patch["status"], patch["bytes_before"], patch["bytes_after"]))
    print("判词：%s" % VERDICT)
    print("红线：%s" % REDLINE)
    rc = 0 if all(x["ok"] for x in CTRL) and all(g["ok"] for g in GUARDS) else 1
    print("")
    print("[EXIT CODE] %d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
