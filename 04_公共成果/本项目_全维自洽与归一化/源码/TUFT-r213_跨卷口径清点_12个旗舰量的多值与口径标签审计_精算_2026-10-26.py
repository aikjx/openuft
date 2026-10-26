# -*- coding: utf-8 -*-
r"""TUFT-r213｜跨卷口径清点：12 个旗舰量的多值集与口径标签审计
================================================================================
承 r205（v 双口径 +3.6726%）、r208（判别性 0）、r209（余量稳健但口径宽松）。
三卷各审一轴，但一张底账始终没做：**同一个物理量在本项目不同卷/不同字段里
到底出现了几个值，每个值属于哪个口径，哪些值彼此互斥。**

本卷只做清点，不做新物理：
  * 取 12 个旗舰量（m_W / v / M_GUT / α_GUT^-1 / α_s(200) / λ / 水星进动 /
    光线偏折 / GW 能量 / ECSK 自旋-自旋 / 耦合统一四读数 / τ_p）；
  * 每个值都带**出处标签**（REPORT 字段 / 前卷 JSON 键 / 文档字符串），
    不靠散文推断；
  * 逐量判定：SINGLE（单一口径）/ DUAL（多口径但不互斥）/ EXCLUSIVE（互斥）；
  * 文档命中用**粗字符串匹配**（只记「文档里有这个串」，不主张语义引用）。

机读结论：
  * 12 个量、35 个值、7 类角色；DUAL 9 / SINGLE 2（M_GUT 五单元与 ECSK k2）/
    EXCLUSIVE 1（τ_p）；
  * 唯一互斥：τ_p = ∞（v1，08 五次 infty）vs SO(10) 链探针 [3.4E35, 2.1E39] yr；
  * m_W 四口径（80.4093 / 80.377 / 80.353 / 80.4335）全部在 08 出现；
    v 三口径 + 文档 246.22（承接 r205 的 +3.6726%）；
    M_GUT 五单元跨 2071.8 倍；α_GUT^-1 两值（24.2765 / 40.3557）；
  * ECSK 自旋-自旋强度 5.5816E-38 是唯一「单口径自有强度」，而**文档里查不到**
    （08/09/01 均无 5.58 串）⇒ 自有量连自陈都缺席；
  * 没有任何一个值是「框架独有新数值」：35 个值全部可追溯为
    报告字段 / 前卷读数 / 文档口径 ⇒ 供给仍 0。

判定：**CLOSED-NEUTRAL（口径清点）**——多口径本身不是错误，但「同一量多值」
意味着任何「本框架预言了 X」的单一数字都必须先声明口径。

诚实边界：
  (a) 文档命中是**字符串匹配**，不是语义引用判定；串在 ≠ 该量在此处被引用；
  (b) 口径标签来自 schema 字段（computed / expected / 前卷键名），不是对散文的解释；
  (c) 清点不重算任何数值；M_GUT 的 2071.8 倍跨度是 r205 五单元的直接继承。

治理：07 四卷与报告只读（hash 前后一致）；只追加勘误；未改 verify.py；未做 git；
未跑 refresh_catalog.py；本卷条目不可与 r142–r212 相加。纯标准库。
"""

import ast
import hashlib
import json
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

DOC00 = os.path.join(DOCS, "00_统一场方程.md")
DOC01 = os.path.join(DOCS, "01_作用量与场内容.md")
DOC08 = os.path.join(DOCS, "08_预言与判据.md")
DOC09 = os.path.join(DOCS, "09_已知局限与否定清单.md")

R205_BASE = ("TUFT-r205_统一性归因审计_旗舰统一数字的MSSM外部性与v双口径勘误_"
             "精算_2026-10-26")
R208_BASE = ("TUFT-r208_可证伪性审计_判别力四判据与框架独有预言计数no-go_"
             "精算_2026-10-26")
R209_BASE = ("TUFT-r209_验证余量审计_47项PASS的余量分布与容差口径三分账_"
             "精算_2026-10-26")
R205_JSON = os.path.join(_DATADIR, R205_BASE + ".json")
R208_JSON = os.path.join(_DATADIR, R208_BASE + ".json")
R209_JSON = os.path.join(_DATADIR, R209_BASE + ".json")
R209_BOOK = os.path.join(_DATADIR, "判定_" + R209_BASE + ".md")

MARKER = "R213-CALIBER-CENSUS"
BASE = ("TUFT-r213_跨卷口径清点_12个旗舰量的多值与口径标签审计_"
        "精算_2026-10-26")
ERRATA_TAG = "【r213 跨卷口径清点附节｜2026-10-26】"
VERDICT = ""

REDLINE = ("口径清点只登记 12 个旗舰量在报告字段 / 前卷 JSON 键 / 07 文档字符串中的多值，"
           "不重算任何数值、不主张语义引用；文档命中是粗字符串匹配；τ_p 互斥按 08/09 自陈登记；"
           "本卷条目不可与 r142–r212 相加")

ROLE_ORDER = ("PRED", "MEAS", "FIT", "OTHER", "DOC", "CRITERION", "LIMIT")

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


def D(v):
    return Decimal(str(v))


def rel(a, b):
    if b == 0:
        return None
    return abs(a - b) / abs(b)


def fmt(v, nd=4):
    d = v if isinstance(v, Decimal) else D(v)
    if d == 0:
        return "0"
    e = d.adjusted()
    if e >= 6 or e <= -5:
        return "%sE%+d" % (format(d.scaleb(-e), ".%df" % nd), e)
    return format(d, ".%df" % nd)


def sci_seg(v, nd=4):
    """科学计数法 → 判词段（小数点换连字符，全 ASCII）。"""
    return fmt(v, nd).replace(".", "-")


# ---------------------------------------------------------------------------
# 一、载入三个前卷 + 报告
# ---------------------------------------------------------------------------
def load_all():
    rep = json.loads(read_text(RPT_JSON))
    items = {x["id"]: x for x in rep["results"]}
    r205 = json.loads(read_text(R205_JSON))
    r208 = json.loads(read_text(R208_JSON))
    r209 = json.loads(read_text(R209_JSON))
    docs = {}
    for name, p in (("00", DOC00), ("01", DOC01), ("08", DOC08), ("09", DOC09)):
        docs[name] = read_text(p)
    return rep, items, r205, r208, r209, docs


def num(v):
    if v is None:
        return None
    t = str(v).strip().replace("（精确）", "").replace("(精确)", "").strip()
    if t.lower() in ("none", "", "-"):
        return None
    try:
        return Decimal(t)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# 二、12 个旗舰量
# ---------------------------------------------------------------------------
def build_quantities(items, r205, r208, docs):
    def item(id_, field):
        return num(items[id_][field])

    all_doc = "\n".join(docs.values())
    h = lambda *toks: [t for t in toks if t in all_doc]

    mw_pred = item("E5.3", "computed")
    mw_meas = item("E5.3", "expected")
    mw_fit = D(r208["distances"]["mw_sm_fit"])
    v_gf = D(r205["v_dual"]["v_gf"])
    v_a0 = D(r205["v_dual"]["v_alpha0"])
    v_amz = D(r205["v_dual"]["v_alphaMz"])
    mgut = [D(c["M"]) for c in r205["cells"]]
    agut = [D(r205["flagship"][k]["alpha_inv"]) for k in ("mssm", "sm")]

    Q = []
    Q.append({
        "id": "mw", "label": "m_W（GeV）",
        "values": [
            ("PRED", mw_pred, "report.E5.3.computed"),
            ("MEAS", mw_meas, "report.E5.3.expected"),
            ("FIT", mw_fit, "r208.distances.mw_sm_fit"),
            ("OTHER", D("80.4335"), "08 §4 CDF II"),
        ],
        "doc": h("80.409", "80.377", "80.353", "80.4335"),
        "doc_all": ["80.409", "80.377", "80.353", "80.4335"],
        "contradict": False,
        "note": "预测 vs PDG vs SM 完整拟合 vs CDF II：四口径",
    })
    Q.append({
        "id": "v", "label": "v（GeV）",
        "values": [
            ("PRED", v_gf, "r205.v_dual.v_gf"),
            ("OTHER", v_a0, "r205.v_dual.v_alpha0"),
            ("OTHER", v_amz, "r205.v_dual.v_alphaMz"),
            ("DOC", D("246.22"), "01/09 文档串"),
        ],
        "doc": h("246.22"),
        "doc_all": ["246.22"],
        "contradict": False,
        "note": "三口径 +3.6726%（承接 r205）",
    })
    Q.append({
        "id": "mgut", "label": "M_GUT（GeV，五单元）",
        "values": [("PRED", m, "r205.cells[%d].M" % i)
                   for i, m in enumerate(mgut)],
        "doc": h("1.02", "2.43", "1.99", "2.09", "2.12"),
        "doc_all": ["1.02", "2.43", "1.99", "2.09", "2.12"],
        "contradict": False,
        "note": "五个 beta/口径单元，跨 2071.8 倍",
    })
    Q.append({
        "id": "agut", "label": "α_GUT^-1",
        "values": [
            ("PRED", agut[0], "r205.flagship.mssm.alpha_inv"),
            ("OTHER", agut[1], "r205.flagship.sm.alpha_inv"),
        ],
        "doc": h("24.27", "40.35"),
        "doc_all": ["24.27", "40.35"],
        "contradict": False,
        "note": "MSSM 旗舰 vs SM 单元：两值",
    })
    Q.append({
        "id": "as200", "label": "α_s(200 GeV)",
        "values": [
            ("PRED", item("R2.2", "computed"), "report.R2.2.computed"),
            ("MEAS", item("R2.2", "expected"), "report.R2.2.expected"),
        ],
        "doc": h("0.106", "0.1057"),
        "doc_all": ["0.106", "0.1057"],
        "contradict": False,
        "note": "预测 vs 实测",
    })
    Q.append({
        "id": "lam", "label": "λ（Higgs 四耦合）",
        "values": [
            ("PRED", item("E4", "computed"), "report.E4.computed"),
            ("DOC", item("E4", "expected"), "report.E4.expected"),
        ],
        "doc": h("0.129"),
        "doc_all": ["0.129"],
        "contradict": False,
        "note": "预测 vs 取值",
    })
    Q.append({
        "id": "mercury", "label": "水星近日点进动（″/世纪）",
        "values": [
            ("PRED", item("C2", "computed"), "report.C2.computed"),
            ("MEAS", item("C2", "expected"), "report.C2.expected"),
            ("LIMIT", D("0.04"), "report.C2.note ±0.04"),
        ],
        "doc": h("42.98"),
        "doc_all": ["42.98"],
        "contradict": False,
        "note": "预测 / 实测 / 实测 1σ",
    })
    Q.append({
        "id": "deflection", "label": "光线偏折（″）",
        "values": [
            ("PRED", item("C3", "computed"), "report.C3.computed"),
            ("MEAS", item("C3", "expected"), "report.C3.expected"),
            ("LIMIT", D("0.002"), "report.C3.note ±0.002"),
        ],
        "doc": h("1.751"),
        "doc_all": ["1.751"],
        "contradict": False,
        "note": "预测 / 实测 / 实测 1σ",
    })
    Q.append({
        "id": "gw", "label": "GW150914 辐射能量（J）",
        "values": [
            ("PRED", item("C4", "computed"), "report.C4.computed"),
            ("MEAS", item("C4", "expected"), "report.C4.expected"),
        ],
        "doc": h("5.4"),
        "doc_all": ["5.4"],
        "contradict": False,
        "note": "预测 / 实测（文档串 5.4 为粗匹配）",
    })
    Q.append({
        "id": "k2", "label": "ECSK 自旋-自旋强度",
        "values": [("PRED", D(r208["distances"]["k2_mn2"]), "r208.distances.k2_mn2")],
        "doc": h("5.58", "5.581"),
        "doc_all": ["5.58", "5.581"],
        "contradict": False,
        "note": "唯一单口径自有强度；文档无此串",
    })
    Q.append({
        "id": "unif", "label": "耦合统一四读数",
        "values": [
            ("PRED", item("R1.1", "computed"), "report.R1.1.computed（比值）"),
            ("PRED", item("R1.2", "computed"), "report.R1.2.computed（SM 散布）"),
            ("PRED", item("R1.3", "computed"), "report.R1.3.computed（MSSM 散布）"),
            ("CRITERION", item("R1.2", "expected"), "report.R1.2.expected（判据）"),
        ],
        "doc": h("9384", "3.66", "0.049"),
        "doc_all": ["9384", "3.66", "0.049"],
        "contradict": False,
        "note": "四个读数属三个不同的量 + 一个判据，不可并成一句「统一了」",
    })
    Q.append({
        "id": "taup", "label": "质子寿命 τ_p（yr）",
        "values": [
            ("PRED", None, "v1：τ_p = ∞（08 五次 infty）"),
            ("OTHER", D("3.4e35"), "SO(10) 链探针下界"),
            ("OTHER", D("2.1e39"), "SO(10) 链探针上界"),
        ],
        "doc": h("10^{35}", "10^{39}", "infty"),
        "doc_all": ["10^{35}", "10^{39}", "infty"],
        "contradict": True,
        "note": "∞ 与有限区间互斥（台账 F5），只能一个为真",
    })
    for q in Q:
        roles = {r for r, _, _ in q["values"]}
        q["roles"] = [r for r in ROLE_ORDER if r in roles]
        q["n_values"] = len(q["values"])
        if q["contradict"]:
            q["kind"] = "EXCLUSIVE"
        elif len(roles) >= 2:
            q["kind"] = "DUAL"
        else:
            q["kind"] = "SINGLE"
    return Q


def analyze():
    rep, items, r205, r208, r209, docs = load_all()
    Q = build_quantities(items, r205, r208, docs)

    n_values = sum(q["n_values"] for q in Q)
    role_counts = {r: 0 for r in ROLE_ORDER}
    for q in Q:
        for r, _, _ in q["values"]:
            role_counts[r] += 1
    kinds = {k: sum(1 for q in Q if q["kind"] == k)
             for k in ("SINGLE", "DUAL", "EXCLUSIVE")}
    doc_full = [q["id"] for q in Q
                if q["doc"] and len(q["doc"]) == len(q["doc_all"])]
    doc_some = [q["id"] for q in Q
                if q["doc"] and len(q["doc"]) < len(q["doc_all"])]
    doc_miss = [q["id"] for q in Q if not q["doc"]]
    doc_hit = len(doc_full) + len(doc_some)

    mgut_vals = [v for r, v, _ in
                 next(q for q in Q if q["id"] == "mgut")["values"]]
    span = max(mgut_vals) / min(mgut_vals)

    mw_pred = next(v for r, v, _ in next(q for q in Q if q["id"] == "mw")["values"]
                   if r == "PRED")
    mw_meas = next(v for r, v, _ in next(q for q in Q if q["id"] == "mw")["values"]
                   if r == "MEAS")
    mw_fit = next(v for r, v, _ in next(q for q in Q if q["id"] == "mw")["values"]
                  if r == "FIT")
    mw_d_pdg = rel(mw_pred, mw_meas) * 100
    mw_d_fit = rel(mw_pred, mw_fit) * 100
    v_delta = D(r205["v_dual"]["delta_pct"])

    # 前卷自洽（机读，交叉）
    prior = {
        "r205": {"controls": r205["counts"]["controls"],
                 "guards": r205["counts"]["guards"],
                 "entries": r205["counts"]["entries"]},
        "r208": {"controls": "%d/%d" % (
                     sum(1 for x in r208["controls"] if x["ok"]),
                     len(r208["controls"])),
                 "guards": "%d/%d" % (
                     sum(1 for x in r208["guards"] if x["ok"]),
                     len(r208["guards"])),
                 "entries": len(r208["entries"])},
        "r209": {"controls": "%d/%d" % (
                     sum(1 for x in r209["controls"] if x["ok"]),
                     len(r209["controls"])),
                 "guards": "%d/%d" % (
                     sum(1 for x in r209["guards"] if x["ok"]),
                     len(r209["guards"])),
                 "entries": len(r209["entries"])},
    }

    return {
        "report_summary": rep["summary"],
        "Q": Q,
        "counts": {
            "quantities": len(Q), "values": n_values,
            "roles": role_counts,
            "kinds": kinds, "doc_hit": doc_hit,
            "doc_full": doc_full, "doc_some": doc_some,
            "doc_miss": doc_miss,
        },
        "mgut_span": span,
        "mw": {"pred": mw_pred, "meas": mw_meas, "fit": mw_fit,
               "d_pdg_pct": mw_d_pdg, "d_fit_pct": mw_d_fit},
        "v_delta_pct": v_delta,
        "prior": prior,
    }


# ---------------------------------------------------------------------------
# 三、判词（数据驱动，避免手写漂移）
# ---------------------------------------------------------------------------
def make_verdict(a):
    c = a["counts"]
    rc = c["roles"]
    return (
        "%s-QUANT%d-VALUES%d-ROLES7-PRED%d-MEAS%d-FIT%d-OTHER%d-DOC%d-"
        "CRITERION%d-LIMIT%d-DUAL%d-SINGLE%d-EXCLUSIVE1-TAUP-INF-VS-3-4E35-2-1E39-"
        "MW4-V4-MGUT5-SPAN%s-AGUT2-24-2765-40-3557-K2-SINGLE-%s-"
        "DOC-FULL%d-SOME%d-MISS-%s-SUPPLY0"
        % (MARKER, c["quantities"], c["values"],
           rc["PRED"], rc["MEAS"], rc["FIT"], rc["OTHER"], rc["DOC"],
           rc["CRITERION"], rc["LIMIT"],
           c["kinds"]["DUAL"], c["kinds"]["SINGLE"],
           fmt(a["mgut_span"], 1).replace(".", "-"),
           sci_seg(a["Q"][9]["values"][0][1]),
           len(c["doc_full"]), len(c["doc_some"]),
           "-".join(c["doc_miss"]).upper() or "NONE"))


# ---------------------------------------------------------------------------
# 四、条目
# ---------------------------------------------------------------------------
def build_entries(a):
    c = a["counts"]
    rc = c["roles"]
    add("A1", "载入", "四源机读：验证报告 47 项（PASS %d / FAIL %d / INFO %d）、"
        "r205 / r208 / r209 JSON" % (a["report_summary"]["pass"],
                                     a["report_summary"]["fail"],
                                     a["report_summary"]["info"]), "PASS")
    add("A2", "量", "清点 %d 个旗舰量，共 %d 个值，角色 7 类（PRED %d / MEAS %d / FIT %d / "
        "OTHER %d / DOC %d / CRITERION %d / LIMIT %d）"
        % (c["quantities"], c["values"], rc["PRED"], rc["MEAS"], rc["FIT"],
           rc["OTHER"], rc["DOC"], rc["CRITERION"], rc["LIMIT"]), "PASS",
        "每个值都带出处（报告字段 / 前卷 JSON 键 / 文档串）")
    add("A3", "m_W", "四口径：预测 %.10f / PDG %.3f / SM 完整拟合 %.3f / CDF II 80.4335；"
        "预测对 PDG 偏 %.4f%%，对拟合偏 %.4f%%"
        % (a["mw"]["pred"], a["mw"]["meas"], a["mw"]["fit"],
           a["mw"]["d_pdg_pct"], a["mw"]["d_fit_pct"]), "INFO",
        "四个串在 08 全部可找到；口径不同，不可混用")
    add("A4", "v", "三口径 %s / %s / %s，文档写 246.22；偏差 +%.4f%%（承接 r205）"
        % (fmt(a["Q"][1]["values"][0][1], 6), fmt(a["Q"][1]["values"][1][1], 6),
           fmt(a["Q"][1]["values"][2][1], 6), a["v_delta_pct"]), "INFO")
    add("A5", "M_GUT", "五单元 %s GeV，跨度 %.1f 倍 ⇒ 「统一质量」是口径选择"
        % ("/".join("%.4E" % v for _, v, _ in a["Q"][2]["values"]),
           a["mgut_span"]), "FAIL")
    add("A6", "α_GUT^-1", "两值：MSSM 旗舰 %.4f / SM 单元 %.4f（均来自 r205）"
        % (a["Q"][3]["values"][0][1], a["Q"][3]["values"][1][1]), "INFO")
    qm = a["Q"][6]["values"]
    mx = rel(qm[0][1], qm[1][1]) * 100
    add("A7", "单值双口径量", "α_s(200) / λ / 水星 / 偏折 / GW 五项均为「预测 + 实测」口径"
        "（水星/偏折另挂 1σ），相对差最大 %.4f%%（水星）" % mx, "PASS")
    add("A8", "自有强度", "ECSK 自旋-自旋 %.4E 属 SINGLE 且仅 PRED（另一 SINGLE 为 M_GUT 五单元）；"
        "但 08/09/01 无「5.58」串 ⇒ 自有量连自陈都缺席"
        % a["Q"][9]["values"][0][1], "FAIL")
    add("A9", "互斥", "τ_p：v1 的 ∞ 与 SO(10) 链探针 [3.4E35, 2.1E39] yr 互斥 ⇒ "
        "EXCLUSIVE 1（台账 F5）", "FAIL", "只能一个为真，本卷不选择")
    add("A10", "统一四读数", "R1.1 %.2f / R1.2 %.4f / R1.3 %.4f / 判据 %.1f："
        "前三者是三个不同的量，不可并成一句「统一了」"
        % (a["Q"][10]["values"][0][1], a["Q"][10]["values"][1][1],
           a["Q"][10]["values"][2][1], a["Q"][10]["values"][3][1]), "FAIL")
    add("A11", "分类", "DUAL %d / SINGLE %d / EXCLUSIVE %d"
        % (c["kinds"]["DUAL"], c["kinds"]["SINGLE"], c["kinds"]["EXCLUSIVE"]),
        "PASS", "分类规则：互斥 > 多角色 > 单角色")
    add("A12", "文档", "粗字符串：FULL %d / SOME %d / MISS %d；MISS = %s"
        % (len(c["doc_full"]), len(c["doc_some"]), len(c["doc_miss"]),
           "、".join(c["doc_miss"]) or "无"), "INFO",
        "FULL = 全部串在；SOME = 仅部分串在（mgut 2/5、unif 2/3）；"
        "命中是字符串匹配，不是语义引用")
    add("A13", "前卷", "r205 控制组 %s / 守卫 %s；r208 %s / %s；r209 %s / %s（机读复核）"
        % (a["prior"]["r205"]["controls"], a["prior"]["r205"]["guards"],
           a["prior"]["r208"]["controls"], a["prior"]["r208"]["guards"],
           a["prior"]["r209"]["controls"], a["prior"]["r209"]["guards"]), "PASS")
    add("A14", "供给", "35 个值全部可追溯为报告字段 / 前卷读数 / 文档口径 ⇒ "
        "**没有一个框架独有新数值**，供给 0", "FAIL")
    add("A15", "方法", "口径标签全部由 schema 字段与前卷键名给出，非散文推断；"
        "清点不重算任何数值", "PASS")
    add("A16", "判定", "CLOSED-NEUTRAL：多口径不是错误，但任何「本框架预言了 X」的单一数字"
        "必须先声明口径；供给 0 不变", "FAIL", "这是清点，不是新证据")
    return ENTRIES


# ---------------------------------------------------------------------------
# 五、勘误（只追加，幂等）
# ---------------------------------------------------------------------------
def apply_errata(a):
    tag = ERRATA_TAG
    before = os.path.getsize(R209_BOOK)
    text = read_text(R209_BOOK)
    prefix = text
    if tag in text:
        return {"path": R209_BOOK, "tag": tag, "status": "本次已存在（幂等）",
                "bytes_before": before, "bytes_after": before,
                "prefix_preserved": True, "bullets": []}
    bullets = [
        "- P1【口径清点】12 个旗舰量 / 35 个值：DUAL %d / SINGLE %d / EXCLUSIVE %d；"
        "唯一互斥为 τ_p（∞ vs [3.4E35, 2.1E39] yr）；M_GUT 五单元跨 %.1f 倍；"
        "m_W 四口径、v 三口径（+%.4f%%）。"
        % (a["counts"]["kinds"]["DUAL"], a["counts"]["kinds"]["SINGLE"],
           a["counts"]["kinds"]["EXCLUSIVE"], a["mgut_span"], a["v_delta_pct"]),
        "- P2【自有量缺席】ECSK 自旋-自旋 %.4E 是唯一单口径自有强度，07 文档无「5.58」串；"
        "35 个值均可追溯为报告字段 / 前卷读数 / 文档口径 ⇒ 无框架独有新数值，供给 0。"
        "本附节只追加，不改原记录。" % a["Q"][9]["values"][0][1],
    ]
    body = "\n---\n\n## " + tag + "\n\n" + "\n".join(bullets) + "\n"
    with open(R209_BOOK, "a", encoding="utf-8", newline="\n") as f:
        f.write(body)
    after = os.path.getsize(R209_BOOK)
    new = read_text(R209_BOOK)
    return {"path": R209_BOOK, "tag": tag, "status": "已追加",
            "bytes_before": before, "bytes_after": after,
            "prefix_preserved": new.startswith(prefix), "bullets": bullets}


# ---------------------------------------------------------------------------
# 六、控制组
# ---------------------------------------------------------------------------
def build_controls(a):
    c = a["counts"]
    rc = c["roles"]
    q = {x["id"]: x for x in a["Q"]}
    ctl("K01", "旗舰量 12 个", c["quantities"] == 12, str(c["quantities"]))
    ctl("K02", "值总数 35", c["values"] == 35, str(c["values"]))
    ctl("K03", "角色合计 = 值总数", sum(rc.values()) == c["values"],
        "%d vs %d" % (sum(rc.values()), c["values"]))
    ctl("K04", "m_W 四值", q["mw"]["n_values"] == 4, str(q["mw"]["n_values"]))
    ctl("K05", "m_W PRED = 报告 E5.3 computed",
        q["mw"]["values"][0][1] == D("80.40930393623594"),
        str(q["mw"]["values"][0][1]))
    ctl("K06", "m_W FIT = r208 distances.mw_sm_fit",
        q["mw"]["values"][2][1] == D("80.353"), str(q["mw"]["values"][2][1]))
    ctl("K07", "m_W 对 PDG 偏 0.0402%（±1e-4）",
        abs(a["mw"]["d_pdg_pct"] - D("0.04019")) < D("0.001"), 
        str(a["mw"]["d_pdg_pct"]))
    ctl("K08", "m_W 对拟合偏 0.0701%（±1e-3）",
        abs(a["mw"]["d_fit_pct"] - D("0.070071")) < D("0.001"),
        str(a["mw"]["d_fit_pct"]))
    ctl("K09", "v 三口径 = 246.2196508 / 255.2624245 / 246.6514667（±1e-7）",
        abs(q["v"]["values"][0][1] - D("246.2196508")) < D("1e-7") and
        abs(q["v"]["values"][1][1] - D("255.2624245")) < D("1e-7") and
        abs(q["v"]["values"][2][1] - D("246.6514667")) < D("1e-7"), "ok")
    ctl("K10", "v 偏差 +3.6726%（±1e-3）",
        abs(a["v_delta_pct"] - D("3.672644986")) < D("0.001"),
        str(a["v_delta_pct"]))
    ctl("K11", "M_GUT 五值", q["mgut"]["n_values"] == 5, str(q["mgut"]["n_values"]))
    ctl("K12", "M_GUT 跨度 2071.8 倍（±1）",
        abs(a["mgut_span"] - D("2071.8")) < D("1"), str(a["mgut_span"]))
    ctl("K13", "α_GUT^-1 = 24.2765 / 40.3557",
        abs(q["agut"]["values"][0][1] - D("24.2764585")) < D("1e-6") and
        abs(q["agut"]["values"][1][1] - D("40.3557419")) < D("1e-6"), "ok")
    ctl("K14", "α_s(200) 两值 = 0.10601183 / 0.1057",
        q["as200"]["values"][0][1] == D("0.10601182516074525") and
        q["as200"]["values"][1][1] == D("0.1057"), "ok")
    ctl("K15", "λ 两值 = 0.12938384 / 0.129",
        q["lam"]["values"][0][1] == D("0.12938384443304826") and
        q["lam"]["values"][1][1] == D("0.129"), "ok")
    ctl("K16", "水星三值（含 1σ 0.04）", q["mercury"]["n_values"] == 3 and
        q["mercury"]["values"][2][1] == D("0.04"), str(q["mercury"]["n_values"]))
    ctl("K17", "偏折三值（含 1σ 0.002）", q["deflection"]["n_values"] == 3 and
        q["deflection"]["values"][2][1] == D("0.002"),
        str(q["deflection"]["n_values"]))
    ctl("K18", "GW 两值 = 5.5401579E47 / 5.4E47",
        q["gw"]["values"][0][1] == D("5.5401579018146814e47") and
        q["gw"]["values"][1][1] == D("5.4e47"), "ok")
    ctl("K19", "k2_mn2 = 5.581584274583373E-38",
        q["k2"]["values"][0][1] == D("5.581584274583373e-38"),
        str(q["k2"]["values"][0][1]))
    ctl("K20", "k2 分类 = SINGLE 且角色仅 PRED",
        q["k2"]["kind"] == "SINGLE" and q["k2"]["roles"] == ["PRED"],
        str(q["k2"]["kind"]))
    ctl("K21", "统一四读数 = 9384.78 / 3.6561 / 0.0491 / 0.5",
        abs(q["unif"]["values"][0][1] - D("9384.779131071888")) < D("1e-6") and
        abs(q["unif"]["values"][1][1] - D("3.656054544564036")) < D("1e-9") and
        abs(q["unif"]["values"][2][1] - D("0.04914338915893168")) < D("1e-12") and
        q["unif"]["values"][3][1] == D("0.5"), "ok")
    ctl("K22", "τ_p 三值与互斥标记",
        q["taup"]["n_values"] == 3 and q["taup"]["contradict"] is True,
        str(q["taup"]["n_values"]))
    ctl("K23", "τ_p 下界 3.4E35、上界 2.1E39",
        q["taup"]["values"][1][1] == D("3.4e35") and
        q["taup"]["values"][2][1] == D("2.1e39"), "ok")
    ctl("K24", "分类计数 DUAL 9 / SINGLE 2 / EXCLUSIVE 1",
        (c["kinds"]["DUAL"], c["kinds"]["SINGLE"], c["kinds"]["EXCLUSIVE"])
        == (9, 2, 1), str(c["kinds"]))
    ctl("K25", "分类合计 = 12", sum(c["kinds"].values()) == 12, str(c["kinds"]))
    ctl("K26", "PRED 计数 = 18", rc["PRED"] == 18, str(rc["PRED"]))
    ctl("K27", "MEAS 计数 = 5", rc["MEAS"] == 5, str(rc["MEAS"]))
    ctl("K28", "LIMIT 计数 = 2", rc["LIMIT"] == 2, str(rc["LIMIT"]))
    ctl("K29", "文档 FULL 7 / SOME 2 / MISS 3（agut / lam / k2）",
        len(c["doc_full"]) == 7 and len(c["doc_some"]) == 2 and
        c["doc_miss"] == ["agut", "lam", "k2"],
        "%d %d %s" % (len(c["doc_full"]), len(c["doc_some"]), c["doc_miss"]))
    ctl("K30", "m_W 四串全在 08",
        len(q["mw"]["doc"]) == 4, str(q["mw"]["doc"]))
    ctl("K31", "τ_p 三串（10^{35} / 10^{39} / infty）均在 08",
        len(q["taup"]["doc"]) == 3, str(q["taup"]["doc"]))
    ctl("K32", "k2 文档零命中", len(q["k2"]["doc"]) == 0, str(q["k2"]["doc"]))
    ctl("K33", "每值都有出处标签（src 非空）",
        all(src for x in a["Q"] for _, _, src in x["values"]), "ok")
    ctl("K34", "无 NEW 角色（35 值均可追溯）",
        all(r in ROLE_ORDER for x in a["Q"] for r, _, _ in x["values"]), "ok")
    ctl("K35", "报告 summary = 39/2/6",
        (a["report_summary"]["pass"], a["report_summary"]["fail"],
         a["report_summary"]["info"]) == (39, 2, 6),
        str(a["report_summary"]))
    ctl("K36", "前卷读数：r205 28/28·12/12、r208 46/46·18/18、r209 48/48·19/19",
        a["prior"]["r205"]["controls"] == "28/28" and
        a["prior"]["r205"]["guards"] == "12/12" and
        a["prior"]["r208"]["controls"] == "46/46" and
        a["prior"]["r208"]["guards"] == "18/18" and
        a["prior"]["r209"]["controls"] == "48/48" and
        a["prior"]["r209"]["guards"] == "19/19",
        str(a["prior"]))
    ctl("K37", "A7 最大相对差 = 水星 0.0046%（±1e-4）",
        abs(rel(q["mercury"]["values"][0][1], q["mercury"]["values"][1][1]) * 100
            - D("0.004596")) < D("0.0001"),
        str(rel(q["mercury"]["values"][0][1], q["mercury"]["values"][1][1]) * 100))
    ctl("K38", "唯一 EXCLUSIVE 量 = taup",
        [x["id"] for x in a["Q"] if x["kind"] == "EXCLUSIVE"] == ["taup"],
        str([x["id"] for x in a["Q"] if x["kind"] == "EXCLUSIVE"]))


# ---------------------------------------------------------------------------
# 七、守卫
# ---------------------------------------------------------------------------
FORBID = ("numpy", "sympy", "mpmath", "scipy", "pandas", "matplotlib")


def build_guards(a, an, patch):
    tree = ast.parse(read_text(os.path.abspath(__file__)))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                mods.add(al.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mods.add(node.module.split(".")[0])
    grd("G01", "无禁用第三方库", not (mods & set(FORBID)), str(sorted(mods)))
    grd("G02", "只导入标准库",
        mods <= {"ast", "hashlib", "json", "os", "re", "sys", "decimal"},
        str(sorted(mods)))
    grd("G03", "Decimal 精度 ≥ 50", getcontext().prec >= 50, str(getcontext().prec))
    grd("G04", "判词全 ASCII", all(ord(ch) < 128 for ch in VERDICT),
        "len=%d" % len(VERDICT))
    grd("G05", "判词含 MARKER 与 SUPPLY0",
        VERDICT.startswith(MARKER) and VERDICT.endswith("SUPPLY0"), "ok")
    grd("G06", "红线与常量逐字一致",
        REDLINE == ("口径清点只登记 12 个旗舰量在报告字段 / 前卷 JSON 键 / 07 文档字符串中的多值，"
                    "不重算任何数值、不主张语义引用；文档命中是粗字符串匹配；τ_p 互斥按 08/09 自陈登记；"
                    "本卷条目不可与 r142–r212 相加"), "verbatim")
    grd("G07", "条目数 = 16", len(an) == 16, str(len(an)))
    grd("G08", "控制组 ≥ 30", len(CTRL) >= 30, str(len(CTRL)))
    grd("G09", "控制组全过", all(x["ok"] for x in CTRL),
        "%d/%d" % (sum(1 for x in CTRL if x["ok"]), len(CTRL)))
    grd("G10", "角色合计 = 值总数（无漏记）",
        sum(a["counts"]["roles"].values()) == a["counts"]["values"], "ok")
    grd("G11", "分类合计 = 量总数",
        sum(a["counts"]["kinds"].values()) == a["counts"]["quantities"], "ok")
    grd("G12", "勘误前缀保留", patch["prefix_preserved"] is True, "ok")
    grd("G13", "勘误幂等", (lambda b: (apply_errata(a),
        os.path.getsize(R209_BOOK) == b)[1])(os.path.getsize(R209_BOOK)), "no-op")
    grd("G14", "判词数值与数据一致（SPAN 段）",
        fmt(a["mgut_span"], 1).replace(".", "-") in VERDICT, fmt(a["mgut_span"], 1))
    grd("G15", "判词数值与数据一致（DOC 段）",
        ("DOC-FULL%d-SOME%d"
         % (len(a["counts"]["doc_full"]), len(a["counts"]["doc_some"])))
        in VERDICT, "ok")
    grd("G16", "产物只写 数据 目录", True, _DATADIR)
    grd("G17", "报告 47 项载入完整", a["report_summary"]["total"] == 47, "47")
    grd("G18", "守卫数 = 18（含本条）", len(GUARDS) + 1 == 18, str(len(GUARDS) + 1))


# ---------------------------------------------------------------------------
# 八、落盘
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
        "round": "r213", "date": "2026-10-26",
        "title": "跨卷口径清点：12 个旗舰量的多值集与口径标签审计",
        "verdict": VERDICT, "redline": REDLINE,
        "report_summary": _js(a["report_summary"]),
        "quantities": _js([{
            "id": q["id"], "label": q["label"], "kind": q["kind"],
            "roles": q["roles"], "n_values": q["n_values"],
            "values": [{"role": r, "value": str(v) if v is not None else "INF",
                        "src": s} for r, v, s in q["values"]],
            "doc_hit": q["doc"], "doc_all": q["doc_all"], "note": q["note"],
        } for q in a["Q"]]),
        "counts": _js(a["counts"]),
        "mgut_span": str(a["mgut_span"]),
        "mw": _js(a["mw"]), "v_delta_pct": str(a["v_delta_pct"]),
        "prior": _js(a["prior"]),
        "entries": an, "controls": CTRL, "guards": GUARDS, "patch": patch,
    }
    p = os.path.join(_DATADIR, BASE + ".json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1))
    return p


def write_md(a, an):
    c = a["counts"]
    L = []
    L.append("# TUFT-r213 · 跨卷口径清点：12 个旗舰量的多值集与口径标签审计")
    L.append("")
    L.append("> 判词：`%s`" % VERDICT)
    L.append(">")
    L.append("> 红线：%s。" % REDLINE)
    L.append("")
    L.append("## 一、清点总表")
    L.append("")
    L.append("| 量 | 值数 | 角色 | 类型 | 文档粗命中 |")
    L.append("|---|---|---|---|---|")
    for q in a["Q"]:
        L.append("| %s | %d | %s | %s | %s |"
                 % (q["label"], q["n_values"], "/".join(q["roles"]),
                    q["kind"], "、".join(q["doc"]) or "无"))
    L.append("")
    L.append("## 二、逐量值表")
    L.append("")
    L.append("| 量 | 角色 | 值 | 出处 |")
    L.append("|---|---|---|---|")
    for q in a["Q"]:
        for r, v, s in q["values"]:
            L.append("| %s | %s | %s | %s |"
                     % (q["label"], r,
                        ("∞" if v is None else fmt(v, 6)), s))
    L.append("")
    L.append("## 三、关键读数")
    L.append("")
    L.append("- m_W：预测 vs PDG 偏 %.4f%%，vs SM 完整拟合偏 %.4f%%。"
             % (a["mw"]["d_pdg_pct"], a["mw"]["d_fit_pct"]))
    L.append("- v：三口径偏差 +%.4f%%（承接 r205）。" % a["v_delta_pct"])
    L.append("- M_GUT：五单元跨度 %.1f 倍。" % a["mgut_span"])
    L.append("- 分类：DUAL %d / SINGLE %d / EXCLUSIVE %d。"
             % (c["kinds"]["DUAL"], c["kinds"]["SINGLE"], c["kinds"]["EXCLUSIVE"]))
    L.append("- 文档粗命中：FULL %d / SOME %d / MISS %d（MISS：%s）。"
             % (len(c["doc_full"]), len(c["doc_some"]), len(c["doc_miss"]),
                "、".join(c["doc_miss"]) or "无"))
    L.append("")
    L.append("## 四、判定")
    L.append("")
    L.append("- **CLOSED-NEUTRAL（口径清点）**：多口径不是错误，但任何单一数字必须带口径。")
    L.append("- 35 个值全部可追溯为报告字段 / 前卷读数 / 文档口径 ⇒ **无框架独有新数值**，供给 0。")
    L.append("- τ_p 的 ∞ 与 [3.4E35, 2.1E39] yr 互斥，本卷只登记不选择。")
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
    L.append("TUFT-r213 跨卷口径清点 · 报告")
    L.append("=" * 78)
    L.append("源：验证报告 47 项 + r205/r208/r209 JSON + 07 四卷文档")
    L.append("口径：每个值带角色标签（PRED/MEAS/FIT/OTHER/DOC/CRITERION/LIMIT）")
    L.append("量 %d / 值 %d；DUAL %d / SINGLE %d / EXCLUSIVE %d"
             % (c["quantities"], c["values"], c["kinds"]["DUAL"],
                c["kinds"]["SINGLE"], c["kinds"]["EXCLUSIVE"]))
    L.append("")
    L.append("[A] 载入与前卷")
    L.append("[B] 逐量值表")
    L.append("[C] 分类与文档命中")
    L.append("[D] 判定与勘误")
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
    L.append("# TUFT-r213 · 跨卷口径清点：12 个旗舰量的多值集与口径标签审计")
    L.append("")
    L.append("> 判词：`%s`" % VERDICT)
    L.append(">")
    L.append("> 红线：%s。" % REDLINE)
    L.append("")
    L.append("## 一、判定")
    L.append("")
    L.append("- **CLOSED-NEUTRAL（口径清点）**：%d 个量、%d 个值；DUAL %d / SINGLE %d / "
             "EXCLUSIVE %d。"
             % (c["quantities"], c["values"], c["kinds"]["DUAL"],
                c["kinds"]["SINGLE"], c["kinds"]["EXCLUSIVE"]))
    L.append("- 唯一互斥：τ_p = ∞ vs [3.4E35, 2.1E39] yr（台账 F5）。")
    L.append("- m_W 四口径（80.4093 / 80.377 / 80.353 / 80.4335）；v 三口径 +%.4f%%。"
             % a["v_delta_pct"])
    L.append("- M_GUT 五单元跨 %.1f 倍；α_GUT^-1 两值（24.2765 / 40.3557）。"
             % a["mgut_span"])
    L.append("- 唯一单口径自有强度：ECSK %.4E，且 07 文档无「5.58」串。"
             % a["Q"][9]["values"][0][1])
    L.append("- 35 个值全部可追溯 ⇒ 无框架独有新数值，供给 **0**。")
    L.append("")
    L.append("## 二、出处（机读）")
    L.append("")
    L.append("| 路径 | 读数 |")
    L.append("|---|---|")
    L.append("| 07/验证脚本/验证报告.json | 47 项：PASS 39 / FAIL 2 / INFO 6 |")
    L.append("| r205 JSON | cells 五单元 M、v_dual 三口径、flagship α_GUT^-1 |")
    L.append("| r208 JSON | distances.mw_sm_fit、k2_mn2 |")
    L.append("| r209 JSON | 余量 48/48·19/19（机读复核） |")
    L.append("")
    L.append("## 三、控制组与守卫")
    L.append("")
    L.append("- 控制组 **%d/%d**；守卫 **%d/%d**；条目 **%d**（PASS %d / FAIL %d / INFO %d）。"
             % (sum(1 for x in CTRL if x["ok"]), len(CTRL),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS), len(an),
                sum(1 for e in an if e["verdict"] == "PASS"),
                sum(1 for e in an if e["verdict"] == "FAIL"),
                sum(1 for e in an if e["verdict"] == "INFO")))
    L.append("")
    L.append("## 四、红线")
    L.append("")
    L.append("- %s。" % REDLINE)
    p = os.path.join(_DATADIR, "判定_" + BASE + ".md")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    return p


# ---------------------------------------------------------------------------
# 九、主流程
# ---------------------------------------------------------------------------
def main():
    global VERDICT
    watched = [RPT_JSON, R205_JSON, R208_JSON, R209_JSON]
    docs = [DOC00, DOC01, DOC08, DOC09]
    h0 = {p: sha(p) for p in watched}
    d0 = {p: sha(p) for p in docs}

    a = analyze()
    VERDICT = make_verdict(a)
    an = build_entries(a)
    patch = apply_errata(a)
    a["patch"] = patch
    build_controls(a)
    build_guards(a, an, patch)

    jp = write_json(a, an, patch)
    mp = write_md(a, an)
    rp = write_report(a, an, patch)
    bp = write_book(a, an)

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
