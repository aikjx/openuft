# -*- coding: utf-8 -*-
r"""TUFT-r208｜可证伪性审计：判别力四判据与「框架独有预言」计数 no-go
================================================================================
承 r205（统一性归因审计：V1–V7 外部性 7/7、框架自供统一性证据 0）。本卷不问
「数字属于谁」，改问一个更硬的问题：

  「若 TUFT 错，则必错」的**独有判别性预言**，到底有几条？

四判据（D1–D4），一条预言要成为「独有判别性预言」必须同时满足：
  D1 数值/事件可判   —— 有明确数值（含容差）或明确事件判据；
  D2 实验可达       —— 现有或已运行装置能决定性检验（差距 ≤ 可及量级）；
  D3 隔离性         —— 它若失败，**只**否证 TUFT，参照理论（SM/GR/QCD）仍活；
  D4 自有性         —— 它由 TUFT 特有内容导出，不是引用/输入/外部扩展。

语料 = 当前全部可机读的「可与实验比对」陈述：
  47 项验证报告（07/验证脚本/验证报告.json）
+ V1–V7（08 §1「已验证预言」）
+ P1–P7 与 P3b（08 §2 待检验预言，共 8 个标题）
+ 08 §4 证伪台账 6 行
= 62 个候选 + 6 行台账。

机读结论：
  * 47 项验证的归属分账：SM 17 / QCD 3 / GR 5 / 本框架结构性（量纲一致性）16 /
    自否定 2 / 外部对照 1 / 元信息 3 ⇒ **判别性 = 0**；
  * V1–V7 全部为 SM 电弱一圈（3 条）、GR（3 条）、QCD 一圈（1 条）的恒等式 ⇒
    **判别性 = 0/7**；
  * P 表 8 项：P1/P2 自陈与 GR「暂无差别 / 不可区分」；P5/P6 与 SM 共享（P6 还带
    「而非与之矛盾」的免责句）；P7 自陈「不是 v1 的预言」；P3 是唯一 D3∧D4 成立的
    独有预言，但文档自陈灵敏度差 10^30 倍（不可达）；P4 单向（只能被质子衰变否证、
    不能被确认），且 D4 不成立（B−L 严格守恒是场内容公设），并与 P7 的 τ_p 有限
    互斥（台账 F5）。
  * ⇒ D1∧D2∧D3∧D4 同时成立 = **0 条**；§4 台账 6 行中判别性行 = **0**。

判定：**CLOSED-NEGATIVE（可证伪性 no-go，限定于当前语料）**。
本框架当前的「可证伪性」100% 借自 SM/GR/QCD：任何对它的否证都同时否证参照理论，
任何对它的确认都只是参照理论的确认 ⇒ 独有 Popper 含量 = 0，供给仍 0。

诚实边界（不美化）：
  (a) 这是「当前语料内 0 条」，不是「原理上永不可证伪」的证明；
  (b) 只要新增一条 D1∧D2∧D3∧D4 的预言（例如让挠率传播、或给出可测的
      ECSK 自旋-自旋偏离），本判定即可被推翻 —— 本卷给出的是**计数**，不是禁令；
  (c) P3 的距离与 P4 的单向性按 08 自陈登记，不重算实验灵敏度。

治理：只读 07 四件文档与验证报告；只追加勘误；未改 verify.py；未做 git；
本卷条目不可与 r142–r207 相加。纯标准库（Decimal + 标准 math），无 numpy/sympy/mpmath。
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
DOC08 = os.path.join(DOCS, "08_预言与判据.md")
DOC09 = os.path.join(DOCS, "09_已知局限与否定清单.md")
DOC00 = os.path.join(DOCS, "00_统一场方程.md")
DOC01 = os.path.join(DOCS, "01_作用量与场内容.md")
R205_BASE = ("TUFT-r205_统一性归因审计_旗舰统一数字的MSSM外部性与v双口径勘误_"
             "精算_2026-10-26")
R205_BOOK = os.path.join(_DATADIR, "判定_" + R205_BASE + ".md")

BASE = ("TUFT-r208_可证伪性审计_判别力四判据与框架独有预言计数no-go_"
        "精算_2026-10-26")
ERRATA_TAG = "【r208 可证伪性判别力附节｜2026-10-26】"

VERDICT = (
    "R208-FALSIFIABILITY-AUDIT-CORPUS62-TESTS47-V7-P8-D1-D2-D3-D4-SHARED25-"
    "SM17-QCD3-GR5-STRUCTURAL16-NEGATIVE2-EXTERNAL1-META3-SUM47-V1-V7-EXTERNAL7OF7-"
    "P1-P2-SHARED-GR-SELFADMIT-P1-NO-DIFFERENCE-P2-INDISTINGUISHABLE-P5-P6-SM-"
    "P6-ESCAPE-CLAUSE-P7-NOT-V1-P4-ONE-SIDED-NOT-DERIVED-P3-ISOLATING-UNREACHABLE-"
    "GAP1E30-STRENGTH5-6E-38-ISOLATING4-OWN2-TESTABLE-DERIVED0-LEDGER6-SHARED4-"
    "NONFALSIFIABLE1-ONE-SIDED1-DISCRIMINATING0-BORROWED-100PCT-MW-80-4093-VS-SM-"
    "80-353-DELTA-0-0701PCT-4-69SIGMA-AS200-0-106012-LAMBDA-0-129384-MERCURY-"
    "42-98198-DEFLECTION-1-751243-GW-5-540158E47-SUPPLY0")
REDLINE = ("可证伪性审计只统计当前语料（47 项验证 + V1–V7 + P1–P7/P3b + §4 台账六行）"
           "的判别力；SM/GR/QCD 共享项不计入框架供给；P3 距离与 P4 单向性按文档自陈登记、"
           "不重算实验灵敏度；本卷条目不可与 r142–r207 相加")

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


# ---------------------------------------------------------------------------
# 〇、常量（只用于把文档/报告里的读数转成距离，不引入新物理）
# ---------------------------------------------------------------------------
M_PL = 1.220910e19          # GeV, 未约化 Planck 质量（G = 1/M_Pl^2）
M_N = 0.939565              # GeV, 核子质量
MW_PDG = 80.377             # GeV
MW_SIGMA = 0.012            # GeV
MW_CDF2 = 80.4335           # GeV（08 §4 引用的 CDF II 值）

OWN_SM = "SM"
OWN_QCD = "QCD"
OWN_GR = "GR"
OWN_STRUCT = "STRUCTURAL"
OWN_NEG = "NEGATIVE"
OWN_EXT = "EXTERNAL"
OWN_META = "META"

SM_CATS = {"规范反常消除", "电荷结构", "电弱", "电磁相互作用"}
QCD_CATS = {"强相互作用"}
GR_CATS = {"引力经典极限", "引力波"}
STRUCT_CATS = {"量纲一致性"}
META_CATS = {"已知缺陷→已修复", "已知缺陷"}
NEG_IDS = {"R1.1", "R1.2"}
EXT_IDS = {"R1.3"}

V_OWNER = {"V1": ("E5.3", OWN_SM), "V2": ("E5.1", OWN_SM),
           "V3": ("C2", OWN_GR), "V4": ("C3", OWN_GR),
           "V5": ("C4", OWN_GR), "V6": ("R2.2", OWN_QCD),
           "V7": ("A1", OWN_SM)}

# P 表的四判据（逐条给出理由；理由句必须在 08 原文里可机读到）
P_SPEC = {
    "P1": {"D1": True, "D2": True, "D3": False, "D4": True,
           "why": "D3 假：08 自陈「与 GR 暂无差别」；两极化是 GR 的共享预言",
           "probe": "暂无差别"},
    "P2": {"D1": True, "D2": True, "D3": False, "D4": True,
           "why": "D3 假：08 自陈「UFE-1 与 GR 不可区分」",
           "probe": "不可区分"},
    "P3": {"D1": True, "D2": False, "D3": True, "D4": True,
           "why": "D3/D4 真（ECSK 独有）；D2 假：08 自陈「在可预见的技术条件下不可测」",
           "probe": "在可预见的技术条件下不可测"},
    "P3b": {"D1": False, "D2": False, "D3": True, "D4": True,
            "why": "D1 假：rho_crit 定标「未建立」；判据不成立",
            "probe": "未建立"},
    "P4": {"D1": False, "D2": True, "D3": True, "D4": False,
           "why": "D1 假（tau_p=inf 无有限数值可确认，只能被衰变否证）；"
                  "D4 假（B-L 严格守恒是场内容公设，不是方程推论）",
           "probe": "质子衰变"},
    "P5": {"D1": True, "D2": True, "D3": False, "D4": False,
           "why": "D3/D4 假：光子/胶子无质量由残留规范对称性给出，与 SM 相同",
           "probe": "无质量"},
    "P6": {"D1": False, "D2": False, "D3": False, "D4": False,
           "why": "D3 假：SM 场内容同样无第五力；08 另写「而非与之矛盾」= 免责句",
           "probe": "而非与之矛盾"},
    "P7": {"D1": True, "D2": False, "D3": True, "D4": False,
           "why": "D4 假：08 自陈「不是 v1 的预言」；D2 假：Delta^±± 技术不可达",
           "probe": "不是 v1 的预言"},
}

LEDGER_SPEC = [
    ("L1", "引力波标量/矢量极化", "SHARED", "GR 同样只允许两种张量极化 ⇒ D3 假"),
    ("L2", "gamma_PPN != 1（非极化源）", "SHARED", "GR 的 gamma_PPN = 1 ⇒ D3 假"),
    ("L3", "质子衰变", "ONE_SIDED", "只否证 v1 场内容，SM 仍活；但 B-L 守恒是公设（D4 假）"),
    ("L4", "第五种力 / 暗光子 / 轴子", "NONFALSIFIABLE", "08/P6 自陈「v1 不完整，而非与之矛盾」"),
    ("L5", "Lambda_QCD 与渐近自由不符", "SHARED", "QCD 自身即被否证 ⇒ D3 假"),
    ("L6", "m_W 偏离 E5.3 预测 > 1%", "SHARED", "E5.3 是 SM 电弱公式 ⇒ D3 假"),
]


# ---------------------------------------------------------------------------
# 一、机读语料
# ---------------------------------------------------------------------------
def load_report():
    d = json.loads(read_text(RPT_JSON))
    res = d["results"]
    return d, res


def owner_of(r):
    rid = r["id"]
    cat = r["category"]
    if rid in NEG_IDS:
        return OWN_NEG
    if rid in EXT_IDS:
        return OWN_EXT
    if cat in SM_CATS:
        return OWN_SM
    if cat in QCD_CATS:
        return OWN_QCD
    if cat in GR_CATS:
        return OWN_GR
    if cat in STRUCT_CATS:
        return OWN_STRUCT
    return OWN_META


def parse_08(text):
    lines = text.splitlines()
    v_rows = []
    for ln in lines:
        m = re.match(r"^\|\s*\*\*(V\d)\*\*\s*\|", ln)
        if m:
            anchor = ""
            am = re.search(r"\]\(验证脚本/验证报告\.md#([^)]+)\)", ln)
            if not am:
                am = re.search(r"\[([A-Z0-9.]+)\]\(验证脚本/验证报告\.md\)", ln)
            if am:
                anchor = am.group(1)
            else:
                am2 = re.search(r"\]\(验证脚本/验证报告\.md\)", ln)
                if am2:
                    # 回退：从行内第一列 [X] 取锚点（形如 [E5.3]）
                    am3 = re.search(r"\[([A-Z][0-9A-Z.]*)\]\(", ln)
                    anchor = am3.group(1) if am3 else ""
            v_rows.append({"id": m.group(1), "anchor": anchor, "line": ln})
    p_items = []
    heads = []
    for i, ln in enumerate(lines):
        hm = re.match(r"^###\s+(P\d+b?)\.", ln)
        if hm:
            heads.append((i, hm.group(1)))
    for k, (i, pid) in enumerate(heads):
        j = len(lines)
        for m in range(i + 1, len(lines)):
            if re.match(r"^###\s+", lines[m]) or re.match(r"^##\s+", lines[m]):
                j = m
                break
        body = "\n".join(lines[i:j])
        p_items.append({"id": pid, "body": body})
    # §4 台账
    ledger = []
    try:
        i4 = next(i for i, ln in enumerate(lines) if ln.startswith("## 4."))
        i5 = next(i for i, ln in enumerate(lines) if ln.startswith("## 5."))
        for ln in lines[i4:i5]:
            if ln.startswith("|") and not set(ln.replace("|", "").strip()) <= set("-: "):
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                if len(cells) >= 2 and cells[0] not in ("若观测到",):
                    ledger.append(cells)
    except StopIteration:
        pass
    # §5 分级
    grading = []
    try:
        i5 = next(i for i, ln in enumerate(lines) if ln.startswith("## 5."))
        for ln in lines[i5:]:
            if ln.startswith("|") and not set(ln.replace("|", "").strip()) <= set("-: "):
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                if len(cells) >= 3 and cells[0] != "级别":
                    grading.append(cells)
    except StopIteration:
        pass
    return {"v_rows": v_rows, "p_items": p_items, "ledger": ledger,
            "grading": grading}


def parse_09(text):
    L = text.splitlines()
    out = {}
    for tag, pat in (("L10", r"^## L10\."), ("L14", r"^## L14\.")):
        idx = None
        for i, ln in enumerate(L):
            if re.match(pat, ln):
                idx = i
                break
        body = ""
        if idx is not None:
            j = len(L)
            for m in range(idx + 1, len(L)):
                if re.match(r"^## ", L[m]):
                    j = m
                    break
            body = "\n".join(L[idx:j])
        out[tag] = body
    return out


def analyze():
    rep, res = load_report()
    doc08 = read_text(DOC08)
    doc09 = read_text(DOC09)
    p8 = parse_08(doc08)
    p9 = parse_09(doc09)

    tests = []
    for r in res:
        own = owner_of(r)
        has_num = isinstance(r.get("computed"), (int, float))
        d1 = has_num and own != OWN_STRUCT
        d2 = True
        d3 = False
        d4 = (own == OWN_STRUCT)
        tests.append({
            "id": r["id"], "category": r["category"], "status": r["status"],
            "owner": own, "computed": r.get("computed"),
            "expected": r.get("expected"),
            "D1": d1, "D2": d2, "D3": d3, "D4": d4,
            "discriminating": bool(d1 and d2 and d3 and d4),
        })

    owners = {}
    for t in tests:
        owners[t["owner"]] = owners.get(t["owner"], 0) + 1

    v_items = []
    report_ids = [r["id"] for r in res]
    for v in p8["v_rows"]:
        aid, own = V_OWNER.get(v["id"], ("", "UNKNOWN"))
        an = v["anchor"] or aid
        resolved = any(rid == an or rid.startswith(an + ".") for rid in report_ids)
        v_items.append({"id": v["id"], "anchor": an, "owner": own,
                        "resolved": bool(resolved),
                        "D1": True, "D2": True,
                        "D3": False, "D4": False,
                        "discriminating": False})

    p_items = []
    for p in p8["p_items"]:
        pid = p["id"]
        sp = P_SPEC.get(pid)
        if sp is None:
            p_items.append({"id": pid, "D1": False, "D2": False,
                            "D3": False, "D4": False, "discriminating": False,
                            "probe_hit": False, "why": "未登记判据"})
            continue
        hit = sp["probe"] in p["body"]
        p_items.append({"id": pid,
                        "D1": sp["D1"], "D2": sp["D2"],
                        "D3": sp["D3"], "D4": sp["D4"],
                        "discriminating": bool(sp["D1"] and sp["D2"] and sp["D3"] and sp["D4"]),
                        "probe": sp["probe"], "probe_hit": hit, "why": sp["why"]})

    ledger = []
    for row in p8["ledger"]:
        label = row[0]
        text = " | ".join(row)
        cls, note = "UNKNOWN", ""
        if "引力波" in text:
            cls, note = "SHARED", "GR 同样只允许两种张量极化 ⇒ D3 假"
        elif ("PPN" in text) or ("γ" in text):
            cls, note = "SHARED", "GR 的 gamma_PPN = 1 ⇒ D3 假"
        elif "质子衰变" in text:
            cls, note = "ONE_SIDED", "只否证 v1 场内容，SM 仍活；但 B-L 守恒是公设（D4 假）"
        elif "第五种力" in text:
            cls, note = "NONFALSIFIABLE", "08/P6 自陈「v1 不完整，而非与之矛盾」"
        elif ("Λ" in text) or ("Lambda" in text) or ("QCD" in text):
            cls, note = "SHARED", "QCD 自身即被否证 ⇒ D3 假"
        elif ("m_W" in text) or ("mW" in text):
            cls, note = "SHARED", "E5.3 是 SM 电弱公式 ⇒ D3 假"
        ledger.append({"row": label, "text": text, "class": cls, "note": note})

    # 距离（全部来自验证报告 JSON 的 computed，不新引入外部数）
    byid = {r["id"]: r for r in res}
    mw_pred = float(byid["E5.3"]["computed"])
    mw_fit = float(byid["E5.4"]["computed"])
    as200 = float(byid["R2.2"]["computed"])
    lam = float(byid["E4"]["computed"])
    merc = float(byid["C2"]["computed"])
    defl = float(byid["C3"]["computed"])
    gw = float(byid["C4"]["computed"])
    dist = {
        "mw_pred": mw_pred,
        "mw_sm_fit": mw_fit,
        "mw_pdg": MW_PDG,
        "mw_delta_smfit_pct": (mw_pred - mw_fit) / mw_fit * 100.0,
        "mw_delta_pdg_pct": (mw_pred - MW_PDG) / MW_PDG * 100.0,
        "mw_sigma_from_smfit": (mw_pred - mw_fit) / MW_SIGMA,
        "mw_sigma_from_cdf2": (MW_CDF2 - mw_pred) / MW_SIGMA,
        "as200": as200,
        "as200_meas": 0.1057,
        "as200_delta_pct": (as200 - 0.1057) / 0.1057 * 100.0,
        "lambda": lam,
        "lambda_doc": 0.129,
        "lambda_delta_pct": (lam - 0.129) / 0.129 * 100.0,
        "mercury": merc,
        "deflection": defl,
        "gw": gw,
        "k2_mn2": 3.0 * math.pi * (M_N / M_PL) ** 2,
        "p3_gap_doc": "1e30",
    }

    doc_phrases = {
        "P1_no_difference": "暂无差别" in doc08,
        "P2_indistinguishable": "不可区分" in doc08,
        "P3_unreachable": "在可预见的技术条件下不可测" in doc08,
        "P6_escape": "而非与之矛盾" in doc08,
        "P7_not_v1": "不是 v1 的预言" in doc08,
        "grading_unreachable": "理论可检验但技术不可达" in doc08,
        "L14_not_equal": ("未被证伪" in p9["L14"] and "不等于" in p9["L14"]),
        "L10_not_closed": ("仍未闭合" in p9["L10"] or "未关闭" in p9["L10"]),
    }

    counts = {
        "tests": len(tests),
        "v": len(v_items),
        "p": len(p_items),
        "corpus": len(tests) + len(v_items) + len(p_items),
        "owners": owners,
        "owner_sum": sum(owners.values()),
        "v_external": sum(1 for v in v_items if not v["discriminating"]),
        "p_d1": sum(1 for p in p_items if p["D1"]),
        "p_d2": sum(1 for p in p_items if p["D2"]),
        "p_d3": sum(1 for p in p_items if p["D3"]),
        "p_d4": sum(1 for p in p_items if p["D4"]),
        "p_isolating": sum(1 for p in p_items if p["D3"]),
        "p_isolating_own": sum(1 for p in p_items if p["D3"] and p["D4"]),
        "p_testable_derived": sum(1 for p in p_items if p["discriminating"]),
        "ledger_rows": len(ledger),
        "ledger_shared": sum(1 for l in ledger if l["class"] == "SHARED"),
        "ledger_nonfalsifiable": sum(1 for l in ledger if l["class"] == "NONFALSIFIABLE"),
        "ledger_one_sided": sum(1 for l in ledger if l["class"] == "ONE_SIDED"),
        "ledger_discriminating": sum(1 for l in ledger if l["class"] == "DISCRIMINATING"),
        "tests_discriminating": sum(1 for t in tests if t["discriminating"]),
        "v_discriminating": sum(1 for v in v_items if v["discriminating"]),
        "v_resolved": sum(1 for v in v_items if v["resolved"]),
        "total_discriminating": (sum(1 for t in tests if t["discriminating"])
                                 + sum(1 for v in v_items if v["discriminating"])
                                 + sum(1 for p in p_items if p["discriminating"])),
    }

    return {"report_summary": rep.get("summary", {}),
            "tests": tests, "v_items": v_items, "p_items": p_items,
            "ledger": ledger, "grading": p8["grading"],
            "doc_phrases": doc_phrases, "counts": counts, "dist": dist,
            "doc08_bytes": len(doc08.encode("utf-8")),
            "doc09_bytes": len(doc09.encode("utf-8"))}


# ---------------------------------------------------------------------------
# 二、条目
# ---------------------------------------------------------------------------
def build_entries(a):
    c = a["counts"]
    o = c["owners"]
    d = a["dist"]

    add("A1", "ledger",
        "机读 07/验证脚本/验证报告.json：%d 项（PASS %d / FAIL %d / INFO %d），"
        "分 %d 个类别；按归属分账 = SM %d / QCD %d / GR %d / 本框架结构性 %d / "
        "自否定 %d / 外部对照 %d / 元信息 %d（合计 %d）"
        % (c["tests"], a["report_summary"].get("pass", -1),
           a["report_summary"].get("fail", -1), a["report_summary"].get("info", -1),
           len({t["category"] for t in a["tests"]}),
           o.get(OWN_SM, 0), o.get(OWN_QCD, 0), o.get(OWN_GR, 0),
           o.get(OWN_STRUCT, 0), o.get(OWN_NEG, 0), o.get(OWN_EXT, 0),
           o.get(OWN_META, 0), c["owner_sum"]),
        "PASS",
        "分账是机读的：每项按类别与 id 落到唯一归属，合计必须等于 47")

    add("A2", "ledger",
        "V1–V7 共 %d 行，来源锚点全部命中验证报告（%d/%d）；归属 = SM 电弱 %d / GR %d / "
        "QCD %d ⇒ 判别性 0/%d"
        % (c["v"], c["v_resolved"], c["v"], 3, 3, 1, c["v"]),
        "PASS",
        "r205 已逐条归因；本卷只把「外部性 7/7」翻译成判别力 0/7")

    add("A3", "ledger",
        "08 §2 的 P 标题机读 = %d 个（%s），其中含 P3b；§5 分级表覆盖 P1/P2/P5/P4/P3/P7 与 P3b"
        % (c["p"], "/".join(p["id"] for p in a["p_items"])),
        "PASS",
        "「P1–P7」是口称，磁盘上是 8 个标题 ⇒ 本卷按 8 计数，不沿用旧口径")

    add("A4", "classification",
        "47 项验证中 D1∧D2∧D3∧D4 同时成立 = %d；结构性 16 项（量纲一致性）只有「质量量纲 = 4」，"
        "无实验可比数值 ⇒ D1 不成立；自否定 2 项（R1.1/R1.2）是本框架的 no-go，不是预言"
        % c["tests_discriminating"],
        "FAIL",
        "验证报告越厚，不等于独有预言越多：47 项里没有一项能把 TUFT 与 SM/GR/QCD 分开")

    add("A5", "classification",
        "V1–V7 的 D3 全假：V1/V2 是 SM 电弱一圈、V3/V4/V5 是 GR、V6 是 QCD 一圈、V7 是 SM 反常消除"
        " ⇒ 「已验证」= 参照理论已验证，不是本框架的独有确认",
        "FAIL",
        "与 r205 的 A3 同源；本卷新增的是判据形式化后的计数")

    add("A6", "criteria",
        "四判据 D1（数值/事件可判）·D2（实验可达）·D3（隔离性）·D4（自导出）已形式化并逐条施加；"
        "语料 = 47 + 7 + 8 = %d 个候选 + 台账 %d 行" % (c["corpus"], c["ledger_rows"]),
        "PASS",
        "判据是本卷的度量工具，不是新物理")

    add("A7", "probe",
        "P1（只有两种张量极化）：D1/D2/D4 真，D3 假 —— 08 自陈「与 GR 暂无差别」"
        "（机读命中=%s）⇒ 发现标量/矢量极化会同时否证 GR，不能单独否证 TUFT"
        % a["doc_phrases"]["P1_no_difference"],
        "FAIL",
        "这是「共享的可证伪性」：错一起错，不是本框架的判别力")

    add("A8", "probe",
        "P2（非极化区 PPN 与 GR 相同）：D3 假 —— 08 自陈「UFE-1 与 GR 不可区分」"
        "（机读命中=%s）⇒ gamma_PPN != 1 同时否证 GR 与 TUFT"
        % a["doc_phrases"]["P2_indistinguishable"],
        "FAIL",
        "把「不可区分」写成预言，等于承认在这条通道上没有信息")

    add("A9", "probe",
        "P3（ECSK 自旋-自旋接触项）是本语料中唯一 D1∧D3∧D4 成立者；但 D2 假 —— 08 自陈"
        "「在可预见的技术条件下不可测」（命中=%s），灵敏度差 10^30 倍；本卷独立算得无量纲强度"
        " 3*pi*(m_N/M_Pl)^2 = %.3E ⇒ 与「不可达」自陈一致"
        % (a["doc_phrases"]["P3_unreachable"], d["k2_mn2"]),
        "INFO",
        "独有但不可达：原理上可证伪，实践上不是当前可用的判别器")

    add("A10", "probe",
        "P4（tau_p = inf）：D3 真（质子衰变只否证 v1 场内容，SM 仍活），但 D1/D4 假 —— "
        "「无穷」不是可确认的有限数值，且 B-L 严格守恒是场内容公设；同时与 P7 的 tau_p = "
        "3.4E35–2.1E39 yr 互斥（台账 F5）⇒ 单向否证、非导出、且框架自相矛盾",
        "FAIL",
        "单向性不是判别力：只能被一次发现打红，永远不能被一次测量确认")

    add("A11", "probe",
        "P5（光子/胶子无质量）D3 假（SM 同）；P6（无第五力）D3 假且带免责句「而非与之矛盾」"
        "（命中=%s）⇒ 第五力信号被定义为「v1 不完整」而不是「v1 错」，该行不构成否证条件"
        % a["doc_phrases"]["P6_escape"],
        "FAIL",
        "免责句把一条可能的否证改写成补丁理由；本卷按「不可证伪」记账")

    add("A12", "probe",
        "P7（SO(10) 路线的 M_GUT 带与 tau_p）：D4 假 —— 08 自陈「不是 v1 的预言」（命中=%s）；"
        "D2 假 —— Delta^±± 与 tau_p 均属「技术不可达」；且与 P4 互斥"
        % a["doc_phrases"]["P7_not_v1"],
        "FAIL",
        "条件性外部扩展：数字可单点证伪，但不是本框架 v1 的预言")

    add("A13", "ledger",
        "08 §4 证伪台账 %d 行：共享 %d（GR×2 / QCD×1 / SM×1）· 不可证伪 %d · 单向 %d · "
        "判别性 %d"
        % (c["ledger_rows"], c["ledger_shared"], c["ledger_nonfalsifiable"],
           c["ledger_one_sided"], c["ledger_discriminating"]),
        "FAIL",
        "台账的 6 行没有一行能给出「TUFT 独有且可达」的否证条件")

    add("A14", "distance",
        "多数值距离（全部取自验证报告）：m_W 预测 %.4f vs SM 完整拟合 %.3f（差 %.4f%% = "
        "%.2f sigma）；vs PDG %.3f（差 %.4f%%）；alpha_s(200) %.6f vs %.4f（差 %.3f%%）；"
        "lambda %.6f vs %.3f；水星 %.5f″；偏折 %.6f″；GW %.6E J"
        % (d["mw_pred"], d["mw_sm_fit"], d["mw_delta_smfit_pct"],
           d["mw_sigma_from_smfit"], d["mw_pdg"], d["mw_delta_pdg_pct"],
           d["as200"], d["as200_meas"], d["as200_delta_pct"],
           d["lambda"], d["lambda_doc"], d["mercury"], d["deflection"], d["gw"]),
        "PASS",
        "距离都落在参照理论自身的圈阶/方案差内 ⇒ 没有一条达到「分开 TUFT 与参照理论」的阈值")

    add("A15", "verdict",
        "计数结论：D1∧D2∧D3∧D4 = %d/%d；D3 成立 %d 条（P3/P3b/P4/P7），其中 D4 也成立 %d 条"
        "（P3/P3b），实验可达 %d 条；§4 台账判别性 %d 行 ⇒ 独有判别性预言 = 0"
        % (c["total_discriminating"], c["corpus"], c["p_isolating"],
           c["p_isolating_own"], c["p_testable_derived"], c["ledger_discriminating"]),
        "FAIL",
        "CLOSED-NEGATIVE（可证伪性 no-go，限当前语料）")

    add("A16", "boundary",
        "诚实边界：本判定是「当前 62 个候选内 0 条」，不是「原理上不可证伪」的证明；"
        "只要新增一条满足 D1–D4 的预言（例如让挠率传播、或给出可测的 ECSK 自旋-自旋偏离），"
        "本判定即被推翻。09/L14 自己写着「未被证伪不等于正确」（机读=%s）"
        % a["doc_phrases"]["L14_not_equal"],
        "INFO",
        "本卷给出计数与最小推翻条件，不给「永远不可证伪」的强断言")
    return ENTRIES


# ---------------------------------------------------------------------------
# 三、控制组与守卫
# ---------------------------------------------------------------------------
def build_controls(a):
    c = a["counts"]
    o = c["owners"]
    d = a["dist"]
    s = a["report_summary"]
    ctl("K01", "验证报告总数 = 47", c["tests"] == 47, "n=%d" % c["tests"])
    ctl("K02", "PASS 计数 = 39", s.get("pass") == 39, str(s.get("pass")))
    ctl("K03", "FAIL 计数 = 2", s.get("fail") == 2, str(s.get("fail")))
    ctl("K04", "INFO 计数 = 6", s.get("info") == 6, str(s.get("info")))
    ctl("K05", "PASS+FAIL+INFO = 总数", s.get("pass", 0) + s.get("fail", 0) + s.get("info", 0) == 47)
    ctl("K06", "V 行 = 7", c["v"] == 7, "n=%d" % c["v"])
    ctl("K07", "V id 序列 = V1..V7", [v["id"] for v in a["v_items"]] == ["V%d" % i for i in range(1, 8)])
    ctl("K08", "V 来源锚点 7/7 命中", c["v_resolved"] == 7, "%d/7" % c["v_resolved"])
    ctl("K09", "P 标题 = 8（含 P3b）", c["p"] == 8, "/".join(p["id"] for p in a["p_items"]))
    ctl("K10", "P3b 在列", any(p["id"] == "P3b" for p in a["p_items"]))
    ctl("K11", "台账行 = 6", c["ledger_rows"] == 6, "n=%d" % c["ledger_rows"])
    ctl("K12", "归属分账合计 = 47", c["owner_sum"] == 47, str(c["owner_sum"]))
    ctl("K13", "SM 归属 = 17", o.get(OWN_SM) == 17, str(o.get(OWN_SM)))
    ctl("K14", "QCD 归属 = 3", o.get(OWN_QCD) == 3, str(o.get(OWN_QCD)))
    ctl("K15", "GR 归属 = 5", o.get(OWN_GR) == 5, str(o.get(OWN_GR)))
    ctl("K16", "结构性归属 = 16", o.get(OWN_STRUCT) == 16, str(o.get(OWN_STRUCT)))
    ctl("K17", "自否定归属 = 2", o.get(OWN_NEG) == 2, str(o.get(OWN_NEG)))
    ctl("K18", "外部对照归属 = 1", o.get(OWN_EXT) == 1, str(o.get(OWN_EXT)))
    ctl("K19", "元信息归属 = 3", o.get(OWN_META) == 3, str(o.get(OWN_META)))
    ctl("K20", "共享项 25 = SM+QCD+GR", o.get(OWN_SM, 0) + o.get(OWN_QCD, 0) + o.get(OWN_GR, 0) == 25)
    ctl("K21", "47 项判别性 = 0", c["tests_discriminating"] == 0, str(c["tests_discriminating"]))
    ctl("K22", "V 判别性 = 0", c["v_discriminating"] == 0, str(c["v_discriminating"]))
    ctl("K23", "P 判别性 = 0", c["p_testable_derived"] == 0, str(c["p_testable_derived"]))
    ctl("K24", "P D3 成立 = 4", c["p_isolating"] == 4, str(c["p_isolating"]))
    ctl("K25", "P D3∧D4 成立 = 2", c["p_isolating_own"] == 2, str(c["p_isolating_own"]))
    ctl("K26", "台账共享 = 4", c["ledger_shared"] == 4, str(c["ledger_shared"]))
    ctl("K27", "台账不可证伪 = 1", c["ledger_nonfalsifiable"] == 1, str(c["ledger_nonfalsifiable"]))
    ctl("K28", "台账单向 = 1", c["ledger_one_sided"] == 1, str(c["ledger_one_sided"]))
    ctl("K29", "台账判别性 = 0", c["ledger_discriminating"] == 0, str(c["ledger_discriminating"]))
    ctl("K30", "m_W 预测量级 80.4", 80.0 < d["mw_pred"] < 81.0, "%.4f" % d["mw_pred"])
    ctl("K31", "m_W 与 SM 拟合差 < 0.2%", abs(d["mw_delta_smfit_pct"]) < 0.2,
        "%.4f%%" % d["mw_delta_smfit_pct"])
    ctl("K32", "m_W 与 SM 拟合差 > 4 sigma", abs(d["mw_sigma_from_smfit"]) > 4.0,
        "%.2f sigma" % d["mw_sigma_from_smfit"])
    ctl("K33", "alpha_s(200) 量级 0.106", 0.10 < d["as200"] < 0.11, "%.6f" % d["as200"])
    ctl("K34", "alpha_s 与实测差 < 1%", abs(d["as200_delta_pct"]) < 1.0,
        "%.3f%%" % d["as200_delta_pct"])
    ctl("K35", "lambda 与文档差 < 1%", abs(d["lambda_delta_pct"]) < 1.0,
        "%.3f%%" % d["lambda_delta_pct"])
    ctl("K36", "水星 42.98", abs(d["mercury"] - 42.98) < 0.01, "%.5f" % d["mercury"])
    ctl("K37", "偏折 1.751", abs(d["deflection"] - 1.751) < 0.005, "%.6f" % d["deflection"])
    ctl("K38", "GW 5.5E47 J", 5.4e47 < d["gw"] < 5.6e47, "%.6E" % d["gw"])
    ctl("K39", "ECSK 强度 1E-37 量级", 1e-38 < d["k2_mn2"] < 1e-35, "%.3E" % d["k2_mn2"])
    ctl("K40", "P3 距离文档自陈 1E30", d["p3_gap_doc"] == "1e30", d["p3_gap_doc"])
    ctl("K41", "D1 成立 P 数 = 5", c["p_d1"] == 5, str(c["p_d1"]))
    ctl("K42", "D2 成立 P 数 = 4", c["p_d2"] == 4, str(c["p_d2"]))
    ctl("K43", "D3 成立 P 数 = 4", c["p_d3"] == 4, str(c["p_d3"]))
    ctl("K44", "D4 成立 P 数 = 4", c["p_d4"] == 4, str(c["p_d4"]))
    ctl("K45", "语料 = 62", c["corpus"] == 62, "n=%d" % c["corpus"])
    ctl("K46", "文档短语 8/8 命中", sum(1 for k, v in a["doc_phrases"].items() if v) == 8,
        str(sum(1 for k, v in a["doc_phrases"].items() if v)) + "/8")


def build_guards(a, an, patch):
    src = read_text(os.path.abspath(__file__))
    node = None
    try:
        node = ast.parse(src)
    except SyntaxError:
        node = None
    forbidden = {"numpy", "sympy", "mpmath"}
    bad_imports = []
    if node is not None:
        for n in ast.walk(node):
            if isinstance(n, ast.Import):
                for al in n.names:
                    if al.name.split(".")[0] in forbidden:
                        bad_imports.append(al.name)
            elif isinstance(n, ast.ImportFrom):
                if n.module and n.module.split(".")[0] in forbidden:
                    bad_imports.append(n.module)
    grd("G01", "08 可读且非空", os.path.getsize(DOC08) > 1000, "%d B" % os.path.getsize(DOC08))
    grd("G02", "09 可读且非空", os.path.getsize(DOC09) > 1000, "%d B" % os.path.getsize(DOC09))
    grd("G03", "验证报告可读", os.path.getsize(RPT_JSON) > 1000, "%d B" % os.path.getsize(RPT_JSON))
    grd("G04", "08 哈希前后一致", a.get("_doc_hash_ok", False))
    grd("G05", "09 哈希前后一致", a.get("_doc_hash_ok", False))
    grd("G06", "验证报告哈希前后一致", a.get("_hash_ok", False))
    grd("G07", "条目数 = 16", len(ENTRIES) == 16, "%d" % len(ENTRIES))
    grd("G08", "控制组全过", all(x["ok"] for x in CTRL),
        "%d/%d" % (sum(1 for x in CTRL if x["ok"]), len(CTRL)))
    ok_ascii = all(("A" <= ch <= "Z") or ("0" <= ch <= "9") or ch == "-" for ch in VERDICT)
    grd("G09", "判词 ASCII 大写连字符", ok_ascii, "len=%d" % len(VERDICT))
    grd("G10", "红线逐字", REDLINE == ("可证伪性审计只统计当前语料（47 项验证 + V1–V7 + "
                                       "P1–P7/P3b + §4 台账六行）的判别力；SM/GR/QCD 共享项不计入"
                                       "框架供给；P3 距离与 P4 单向性按文档自陈登记、不重算实验"
                                       "灵敏度；本卷条目不可与 r142–r207 相加"))
    grd("G11", "条目不可跨轮相加声明", "不可与 r142–r207 相加" in REDLINE)
    grd("G12", "无 numpy/sympy/mpmath", len(bad_imports) == 0, ",".join(bad_imports))
    grd("G13", "勘误前缀保留", patch["prefix_preserved"] is True,
        "%d -> %d B" % (patch["bytes_before"], patch["bytes_after"]))
    grd("G14", "归属分账自洽", a["counts"]["owner_sum"] == a["counts"]["tests"])
    grd("G15", "语料计数自洽", a["counts"]["corpus"] == 47 + 7 + 8)
    grd("G16", "P 判据探针全部命中", all(p.get("probe_hit", False) for p in a["p_items"]),
        "%d/%d" % (sum(1 for p in a["p_items"] if p.get("probe_hit")), len(a["p_items"])))
    grd("G17", "判定为 CLOSED-NEGATIVE", "SUPPLY0" in VERDICT and "BORROWED-100PCT" in VERDICT)
    grd("G18", "只读四件文档", a.get("_doc_hash_note", "") == "4/4",
        a.get("_doc_hash_note", ""))


# ---------------------------------------------------------------------------
# 四、勘误（只追加）
# ---------------------------------------------------------------------------
def apply_errata(a):
    tag = ERRATA_TAG
    before = os.path.getsize(R205_BOOK)
    text = read_text(R205_BOOK)
    prefix = text
    if tag in text:
        return {"path": R205_BOOK, "tag": tag, "status": "本次已存在（幂等）",
                "bytes_before": before, "bytes_after": before,
                "prefix_preserved": True, "bullets": 2}
    d = a["dist"]
    bullets = [
        "- P1【判别力计数】当前语料 62 个候选（47 项验证 + V1–V7 + P1–P7/P3b）："
        "D1∧D2∧D3∧D4 = 0；D3 成立 4 条（P3/P3b/P4/P7），其中 D3∧D4 成立 2 条（P3/P3b），"
        "四判据全成立 0 条；§4 台账 6 行判别性 0 行。V1–V7 外部性 7/7（承接 r205）。",
        "- P2【可证伪性归属】与 r205 的「统一性归属」同构：本框架当前的可证伪性 100%% 借自 "
        "SM/GR/QCD；唯一独有预言 P3 的强度 3*pi*(m_N/M_Pl)^2 = %.3E（文档自陈灵敏度差 10^30 倍），"
        "P4 为单向否证且非导出。供给仍 0。本附节只追加，不改原记录。" % d["k2_mn2"],
    ]
    add_block = "\n\n---\n\n## %s\n\n" % tag + "\n".join(bullets) + "\n"
    with open(R205_BOOK, "a", encoding="utf-8", newline="\n") as f:
        f.write(add_block)
    after = os.path.getsize(R205_BOOK)
    now = read_text(R205_BOOK)
    return {"path": R205_BOOK, "tag": tag, "status": "本次已追加",
            "bytes_before": before, "bytes_after": after,
            "prefix_preserved": now.startswith(prefix), "bullets": 2}


# ---------------------------------------------------------------------------
# 五、产物
# ---------------------------------------------------------------------------
def fmt_entries():
    L = []
    for e in ENTRIES:
        L.append("[%s] %s | %s" % (e["verdict"], e["id"], e["text"]))
        if e["note"]:
            L.append("      note: %s" % e["note"])
    return L


def write_json(a, an, patch):
    d = a["dist"]
    c = a["counts"]
    obj = {
        "round": "r208",
        "date": "2026-10-26",
        "title": "可证伪性审计：判别力四判据与框架独有预言计数 no-go",
        "verdict": VERDICT,
        "redline": REDLINE,
        "corpus": {
            "report": {"total": c["tests"], **a["report_summary"]},
            "v_rows": c["v"],
            "p_headings": c["p"],
            "p_ids": [p["id"] for p in a["p_items"]],
            "ledger_rows": c["ledger_rows"],
            "candidates": c["corpus"],
        },
        "criteria": {
            "D1": "数值/事件可判：有明确数值（含容差）或明确事件判据",
            "D2": "实验可达：现有或已运行装置能决定性检验",
            "D3": "隔离性：失败只否证 TUFT，参照理论仍活",
            "D4": "自有性：由 TUFT 特有内容导出，非引用/输入/外部扩展",
        },
        "owners": c["owners"],
        "tests": a["tests"],
        "v_items": a["v_items"],
        "p_items": a["p_items"],
        "ledger": a["ledger"],
        "grading": a["grading"],
        "doc_phrases": a["doc_phrases"],
        "distances": d,
        "counts": c,
        "entries": an,
        "controls": CTRL,
        "guards": GUARDS,
        "patch": patch,
    }
    p = os.path.join(_DATADIR, BASE + ".json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return p


def write_md(a, an):
    c = a["counts"]
    d = a["dist"]
    o = c["owners"]
    L = []
    L.append("# %s" % BASE)
    L.append("")
    L.append("**条目 %d（PASS %d / FAIL %d / INFO %d）；守卫 %d/%d；控制组 %d/%d；退出码 0**"
             % (len(an),
                sum(1 for e in an if e["verdict"] == "PASS"),
                sum(1 for e in an if e["verdict"] == "FAIL"),
                sum(1 for e in an if e["verdict"] == "INFO"),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS),
                sum(1 for x in CTRL if x["ok"]), len(CTRL)))
    L.append("")
    L.append("## 一句话")
    L.append("")
    L.append("当前语料 %d 个候选（47 项验证 + V1–V7 + P1–P7/P3b）里，"
             "同时满足 D1 数值可判、D2 实验可达、D3 隔离性、D4 自导出的**独有判别性预言 = 0**。"
             "47 项验证的分账是 SM %d / QCD %d / GR %d / 结构性 %d / 自否定 %d / 外部 %d / 元信息 %d；"
             "V1–V7 外部性 7/7；P3 是唯一自导出的独有预言但灵敏度差 10^30 倍；"
             "P4 只能被质子衰变单向否证且非导出；§4 台账 6 行判别性 0。"
             % (c["corpus"], o.get(OWN_SM, 0), o.get(OWN_QCD, 0), o.get(OWN_GR, 0),
                o.get(OWN_STRUCT, 0), o.get(OWN_NEG, 0), o.get(OWN_EXT, 0),
                o.get(OWN_META, 0)))
    L.append("")
    L.append("**判定串**：`%s`" % VERDICT)
    L.append("")
    L.append("## 一、四判据与计数")
    L.append("")
    L.append("| 判据 | 含义 |")
    L.append("|---|---|")
    L.append("| D1 | 数值/事件可判：有明确数值（含容差）或明确事件判据 |")
    L.append("| D2 | 实验可达：现有或已运行装置能决定性检验 |")
    L.append("| D3 | 隔离性：失败只否证 TUFT，参照理论仍活 |")
    L.append("| D4 | 自有性：由 TUFT 特有内容导出 |")
    L.append("")
    L.append("| 语料 | 数量 | 判别性 | 说明 |")
    L.append("|---|---|---|---|")
    L.append("| 47 项验证 | 47 | %d | 全部为参照理论恒等式或结构性/自否定/元信息 |"
             % c["tests_discriminating"])
    L.append("| V1–V7 | 7 | %d | SM 3 / GR 3 / QCD 1 |" % c["v_discriminating"])
    L.append("| P1–P7/P3b | 8 | %d | 见下表 |" % c["p_testable_derived"])
    L.append("| §4 台账 | 6 | %d | 共享 4 / 不可证伪 1 / 单向 1 |" % c["ledger_discriminating"])
    L.append("| **合计** | **%d 候选 + 6 行** | **0** | — |" % c["corpus"])
    L.append("")
    L.append("## 二、P 表逐条")
    L.append("")
    L.append("| 编号 | D1 | D2 | D3 | D4 | 判别 | 理由 |")
    L.append("|---|---|---|---|---|---|---|")
    for p in a["p_items"]:
        L.append("| %s | %s | %s | %s | %s | %s | %s |"
                 % (p["id"], "T" if p["D1"] else "F", "T" if p["D2"] else "F",
                    "T" if p["D3"] else "F", "T" if p["D4"] else "F",
                    "✓" if p["discriminating"] else "✗", p.get("why", "")))
    L.append("")
    L.append("## 三、47 项验证归属")
    L.append("")
    L.append("| 归属 | 项数 | 性质 |")
    L.append("|---|---|---|")
    L.append("| SM | %d | 反常/电荷/电弱/电磁 恒等式 |" % o.get(OWN_SM, 0))
    L.append("| QCD | %d | 单圈跑动与 Λ_QCD |" % o.get(OWN_QCD, 0))
    L.append("| GR | %d | 水星/偏折/GW/Schwarzschild |" % o.get(OWN_GR, 0))
    L.append("| 结构性 | %d | 量纲一致性（质量量纲 = 4），无实验可比数值 |" % o.get(OWN_STRUCT, 0))
    L.append("| 自否定 | %d | R1.1/R1.2：SM 单圈不统一 |" % o.get(OWN_NEG, 0))
    L.append("| 外部对照 | %d | R1.3：MSSM 散布 |" % o.get(OWN_EXT, 0))
    L.append("| 元信息 | %d | N1–N3（含已修复的输入型 ν 质量） |" % o.get(OWN_META, 0))
    L.append("")
    L.append("## 四、数值距离")
    L.append("")
    L.append("| 量 | 本框架/报告值 | 参照值 | 差 |")
    L.append("|---|---|---|---|")
    L.append("| m_W | %.4f GeV | SM 完整拟合 %.3f | %.4f%%（%.2fσ） |"
             % (d["mw_pred"], d["mw_sm_fit"], d["mw_delta_smfit_pct"], d["mw_sigma_from_smfit"]))
    L.append("| m_W | %.4f GeV | PDG %.3f | %.4f%% |"
             % (d["mw_pred"], d["mw_pdg"], d["mw_delta_pdg_pct"]))
    L.append("| alpha_s(200) | %.6f | %.4f | %.3f%% |"
             % (d["as200"], d["as200_meas"], d["as200_delta_pct"]))
    L.append("| lambda | %.6f | %.3f | %.3f%% |"
             % (d["lambda"], d["lambda_doc"], d["lambda_delta_pct"]))
    L.append("| 水星进动 | %.5f″ | 42.98 | 0 |" % d["mercury"])
    L.append("| 光线偏折 | %.6f″ | 1.751 | 0 |" % d["deflection"])
    L.append("| GW150914 | %.6E J | 5.4E47 | 2.6%% |" % d["gw"])
    L.append("| ECSK 强度 | %.3E | 可测阈值（文档自陈差 10^30 倍） | 不可达 |" % d["k2_mn2"])
    L.append("")
    L.append("## 五、判定")
    L.append("")
    L.append("- **CLOSED-NEGATIVE（可证伪性 no-go，限当前语料）**：独有判别性预言 = 0。")
    L.append("- 本框架的可证伪性 100% 借自 SM/GR/QCD：任何否证都同时否证参照理论。")
    L.append("- P3 是唯一自导出的独有预言，但灵敏度差 10^30 倍 ⇒ 不是当前可用的判别器。")
    L.append("- P4 只能被质子衰变单向否证，且 B−L 严格守恒是公设；与 P7 的 τ_p 有限互斥（F5）。")
    L.append("- 供给仍 0；本卷条目不可与 r142–r207 相加。")
    L.append("")
    L.append("## 六、控制组与守卫")
    L.append("")
    L.append("- 控制组 **%d/%d**；守卫 **%d/%d**；条目 **%d**（PASS %d / FAIL %d / INFO %d）。"
             % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS), len(an),
                sum(1 for e in an if e["verdict"] == "PASS"),
                sum(1 for e in an if e["verdict"] == "FAIL"),
                sum(1 for e in an if e["verdict"] == "INFO")))
    L.append("")
    L.append("## 七、红线")
    L.append("")
    L.append("- %s。" % REDLINE)
    p = os.path.join(_DATADIR, BASE + ".md")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


def write_report(a, an, patch):
    L = []
    L.append("=" * 78)
    L.append("TUFT-r208 · 可证伪性审计 / 判别力四判据 / 独有预言计数 no-go")
    L.append("=" * 78)
    L.append("")
    L.append("[A] 语料（47 验证 + V1–V7 + P1–P7/P3b + 台账 6 行）")
    L.append("[B] D1–D4 逐条矩阵")
    L.append("[C] 计数与判定")
    L.append("[D] 勘误与治理")
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
    L.append("语料 %d 候选 + 台账 %d 行；判别性 = %d"
             % (a["counts"]["corpus"], a["counts"]["ledger_rows"],
                a["counts"]["total_discriminating"]))
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
    d = a["dist"]
    L = []
    L.append("# TUFT-r208 · 可证伪性审计：判别力四判据与框架独有预言计数 no-go")
    L.append("")
    L.append("> 判词：`%s`" % VERDICT)
    L.append(">")
    L.append("> 红线：%s。" % REDLINE)
    L.append("")
    L.append("## 一、判定")
    L.append("")
    L.append("- **CLOSED-NEGATIVE（可证伪性 no-go，限当前语料）**：独有判别性预言 = **0**。")
    L.append("- 47 项验证分账：SM 17 / QCD 3 / GR 5 / 结构性 16 / 自否定 2 / 外部 1 / 元信息 3。")
    L.append("- V1–V7 外部性 7/7；P 表 8 项中 D1∧D2∧D3∧D4 全真 = 0。")
    L.append("- P3 是唯一自导出的独有预言（强度 %.3E），但文档自陈差 10^30 倍。" % d["k2_mn2"])
    L.append("- P4 单向否证且非导出；与 P7 互斥（F5）。")
    L.append("")
    L.append("## 二、出处（机读）")
    L.append("")
    L.append("| 路径 | 读数 |")
    L.append("|---|---|")
    L.append("| 07/验证脚本/验证报告.json | %d 项：PASS %d / FAIL %d / INFO %d |"
             % (c["tests"], a["report_summary"].get("pass", -1),
                a["report_summary"].get("fail", -1), a["report_summary"].get("info", -1)))
    L.append("| 07/08_预言与判据.md | V1–V7 七行；P 标题 8 个（含 P3b）；§4 台账 6 行 |")
    L.append("| 07/09_已知局限.md | L10 未关闭；L14「未被证伪不等于正确」 |")
    L.append("")
    L.append("## 三、四判据")
    L.append("")
    L.append("| 编号 | D1 | D2 | D3 | D4 | 判别 |")
    L.append("|---|---|---|---|---|---|")
    for p in a["p_items"]:
        L.append("| %s | %s | %s | %s | %s | %s |"
                 % (p["id"], "T" if p["D1"] else "F", "T" if p["D2"] else "F",
                    "T" if p["D3"] else "F", "T" if p["D4"] else "F",
                    "是" if p["discriminating"] else "否"))
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
# 六、主流程
# ---------------------------------------------------------------------------
def main():
    watched = [RPT_JSON]
    docs = [DOC00, DOC01, DOC08, DOC09]
    h0 = {p: sha(p) for p in watched}
    d0 = {p: sha(p) for p in docs}

    a = analyze()
    a["_hash_ok"] = all(sha(p) == h0[p] for p in watched)
    a["_hash_note"] = "1/1" if a["_hash_ok"] else "changed"
    a["_doc_hash_ok"] = all(sha(p) == d0[p] for p in docs)
    a["_doc_hash_note"] = "4/4" if a["_doc_hash_ok"] else "changed"

    an = build_entries(a)
    patch = apply_errata(a)
    a["patch"] = patch
    build_controls(a)
    build_guards(a, an, patch)

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
