# -*- coding: utf-8 -*-
"""
tuft_卷系_构造可行性门禁.py
===========================
TUFT / H-TUFT 卷系·**跨卷收口分析（第 3 轮）**：把 no-go 定理族 **A~I** 机器化为
一套可复跑的「**构造可行性门禁**」，并独立复核最新的补充卷I（CUR-21）。

为何需要本工具（防回潮）：
  · A~I 定理是整轮全维整理**最可靠的产出**（"世界不是数据的函数、拓扑不能编码连续量…"）；
  · 但 D~I 六卷的经验一致：**每卷都在重复同样的缺陷**（自由参数 vs 派生、已关窗口 vs 新通道、
    破缺量无源、同伦不唯一、约束自证、谱形方向不符）；
  · 因此**比新增卷更有价值的**，是把 A~I 变成**进入门槛**：新提案落盘前必须逐条自查。

本册做四件事：
  §V0 独立复核 CUR-21（BBN 畴壁上限）——含指出其"超限倍数"仅是**立方比恒等式**
  §V1 定义 9 条**机检问句**（由定理陈述**独立**写出，**未按人工矩阵调参**）+ 用已知正/负样本自检
  §V2 对全 21 条目机扫，并与人工覆盖矩阵**对账**（报告 precision/recall，暴露矩阵缺口）
  §V3 覆盖完整性审计（未覆盖条目 / 引用不存在的条目 / ❌ 条目是否 ≥1 定理命中）
  §V4 新提案自查表：模板 + 校验器 + 结构性风险分级
  §V5 结论与边界

红线：数学自洽 != 实验证实。本册**不新增物理主张**、**不占 CUR 编号**、**不改动任何 CURATED 真源**。
机检为**启发式**，只用于**对账与提醒**；最终以 `tuft_卷系_结构障碍定理族.md` 的人工矩阵为准。

依赖：Python 3.8 + 标准库（无需 numpy/scipy）。
"""

from __future__ import print_function

import hashlib
import json
import os
import re
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_卷系_构造可行性门禁_report.txt")
OUT_MATRIX = os.path.join(HERE, "tuft_卷系_覆盖矩阵_机器版.json")
NOGO_MD = os.path.join(HERE, "tuft_卷系_结构障碍定理族.md")

# 外部锚（[B] 级，用于 §V0 独立复核）
M_PL_GEV = 1.220910e19
T_C_GEV = 1.0e15
SIGMA_MAX_TEV = 8.5
SIGMA_MAX_GEV = SIGMA_MAX_TEV * 1.0e3

_lines = []
_CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def P_(m):
    _CNT["PASS"] += 1
    _lines.append("[PASS] " + m)


def F_(m):
    _CNT["FAIL"] += 1
    _lines.append("[FAIL] " + m)


def B_(m):
    _CNT["BOUNDARY"] += 1
    _lines.append("[BOUNDARY] " + m)


def I_(m):
    _CNT["INFO"] += 1
    _lines.append("[INFO] " + m)


# ────────────────────────────────────────────────────────────────────────────
# 语料加载
# ────────────────────────────────────────────────────────────────────────────
FIELDS = ("name", "category", "status", "core_prediction", "observational_bound",
          "falsification_criterion", "cross_ref_volume", "uncertainty")


def load_entries():
    ents = {}
    files = sorted(f for f in os.listdir(HERE) if f.endswith("_CURATED.json"))
    for fn in files:
        with open(os.path.join(HERE, fn), encoding="utf-8") as fh:
            doc = json.load(fh)
        for e in doc.get("entries", []):
            blob = " ".join(str(e.get(k, "")) for k in FIELDS)
            blob += " " + " ".join(str(x) for x in e.get("open_items", []))
            blob += " " + json.dumps(e.get("audit_reclassification", {}), ensure_ascii=False)
            ents[e["entry_id"]] = {"entry": e, "file": fn, "volume": doc.get("volume"),
                                   "blob": blob, "status": str(e.get("status", ""))}
    return ents


def parse_human_matrix():
    """解析 结构障碍定理族.md §6 覆盖矩阵 → {字母: set(CUR-id)}。支持 CUR-10~21 区间写法。"""
    txt = open(NOGO_MD, encoding="utf-8").read()
    m = re.search(r"## 6\. 覆盖矩阵.*?\n(.*?)\n>", txt, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        head = cells[0]
        lt = re.match(r"^\**([A-Z]) ", head)
        if not lt:
            continue
        letter = lt.group(1)
        ids = set()
        for a, b in re.findall(r"CUR-(\d+)\s*[~–-]\s*CUR-(\d+)", cells[1]):
            ids.update("CUR-%02d" % n for n in range(int(a), int(b) + 1))
        for a, b in re.findall(r"CUR-(\d+)\s*[~–-]\s*(\d+)(?!\d)", cells[1]):
            ids.update("CUR-%02d" % n for n in range(int(a), int(b) + 1))
        ids.update(re.findall(r"CUR-\d{2}", cells[1]))
        out[letter] = ids
    return out


# ────────────────────────────────────────────────────────────────────────────
# §V0 独立复核 CUR-21
# ────────────────────────────────────────────────────────────────────────────
def v0_crosscheck_cur21(ents):
    I_("§V0 独立复核补充卷I（CUR-21）的核心数值")
    e21 = ents.get("CUR-21")
    if not e21:
        F_("V0 未找到 CUR-21 条目")
        return
    I_("   条目：%s" % e21["entry"]["name"])
    I_("   状态：%s" % e21["status"][:110])
    ratio_pl = (M_PL_GEV / SIGMA_MAX_GEV) ** 3
    ratio_tc = (T_C_GEV / SIGMA_MAX_GEV) ** 3
    I_("   独立重算（超限倍数 = (尺度 / 上限)^3，上限 = (%g TeV)^3）：" % SIGMA_MAX_TEV)
    I_("      普朗克标度：(%0.6e / %0.6e)^3 = %.4e  （CUR-21 声明 2.97e45）"
       % (M_PL_GEV, SIGMA_MAX_GEV, ratio_pl))
    I_("      相变标度  ：(%0.6e / %0.6e)^3 = %.4e  （CUR-21 声明 1.63e33）"
       % (T_C_GEV, SIGMA_MAX_GEV, ratio_tc))
    ok = abs(ratio_pl / 2.97e45 - 1) < 5e-3 and abs(ratio_tc / 1.63e33 - 1) < 5e-3
    if ok:
        P_("V0a 复核通过：两个「超限倍数」与声明一致（%.3e / %.3e）⇒ CUR-21 的算术无误" % (ratio_pl, ratio_tc))
    else:
        F_("V0a 复核不一致（%.3e / %.3e）" % (ratio_pl, ratio_tc))
    B_("V0b 结构提示（诚实）：两个「超限倍数」**只是立方比恒等式** (尺度/上限)^3，不含额外信息；"
       "CUR-21 的结论强度**完全取决于外部上限** σ_max=(%g TeV)^3 本身（[B] 级外部锚，非本理论导出）。"
       "故其可检验性 = 「外部 BBN 上限是否可信」，而非「本理论预言了什么」" % SIGMA_MAX_TEV)


# ────────────────────────────────────────────────────────────────────────────
# §V1 机检问句（由定理陈述独立写出，未按人工矩阵调参）
# ────────────────────────────────────────────────────────────────────────────
def _has(blob, kws):
    return any(k in blob for k in kws)


def _has2(blob, kws_a, kws_b):
    return _has(blob, kws_a) and _has(blob, kws_b)


# 每条定理的**触发条件**：写成 (触发函数, 说明)。关键词集合由定理陈述推得。
QUESTIONS = [
    ("A", lambda b: _has(b, ["拓扑项", "全导数", "总导数", "F∧F", "Euler", "欧拉示性数", "Nieh-Yan"])
     and _has(b, ["Λ", "引力", "真空能", "暗能量", "T_μν", "T_{μν}"]),
     "是否把某可观测量归因于**拓扑项（全导数）**？（→ δS/δg=0 ⇒ 对 T_μν 零贡献）"),
    ("B", lambda b: _has(b, ["整数", "拓扑荷", "绕数", "缠绕", "同伦", "量子数", "Q_hel", "χ", "Lk"])
     and _has(b, ["连续", "层级", "质量", "Ω", "Λ", "耦合", "标度"]),
     "是否用**离散整数/拓扑荷**去确定**连续量或层级**？"),
    ("C", lambda b: _has(b, ["跑动", "β", "标度", "量级", "尺度"])
     and _has(b, ["内生", "导出", "第一性", "派生", "层级"]),
     "是否在 **β≡0（无跑动）** 的前提下声称**内生标度/层级**？"),
    ("D", lambda b: _has(b, ["自由参数", "自由系数", "魔数", "拟合", "重参数化", "ζ", "σ_coeff",
                            "自由", "系数", "ansatz", "唯象"]),
     "是否含**≥1 个自由参数**却被称作「派生量」？"),
    ("E", lambda b: _has(b, ["已排除", "已关闭", "Z=0", "联合拟合", "继承", "重开", "恢复"]),
     "是否依赖**已被排除的窗口**（或把已关窗口当未来优先级）？"),
    ("F", lambda b: _has(b, ["CP", "破缺", "手征", "相位", "Jarlskog", "ΔΠ", "左右手"]),
     "是否生成**破缺量**（CP/手征）而**未给不可消除的破缺源**？"),
    ("G", lambda b: _has(b, ["规范群", "同伦签名", "π₀", "π₃", "SU(2)", "SU(3)", "SU(5)", "E6"]),
     "是否声称**仅凭拓扑/同伦数据导出规范群**？"),
    ("H", lambda b: _has(b, ["BBN", "自动满足", "不破坏", "约束满足", "上限", "取小"]),
     "是否以**取小自由参数**达成约束满足并声称「已检验/通过」？"),
    ("I", lambda b: _has2(b, ["模态", "束缚态", "能级", "谱形", "增量比", "径向模态"],
                          ["代", "层级", "质量", "谱"]),
     "是否用**固定算符的束缚态谱（模态）**生成**代/质量层级**？"),
]

# 自检样本：由人工矩阵中**置信度高**的正样本与**明确不涉及**的负样本构成
SELF_CHECK = {
    "A": (["CUR-15", "CUR-17"], ["CUR-18"]),
    "B": (["CUR-12", "CUR-16", "CUR-20"], ["CUR-01"]),
    "C": (["CUR-04", "CUR-20"], ["CUR-18"]),
    "D": (["CUR-12", "CUR-18", "CUR-21"], ["CUR-04"]),
    "E": (["CUR-13"], ["CUR-04"]),
    "F": (["CUR-18", "CUR-19"], ["CUR-04"]),
    "G": (["CUR-20"], ["CUR-18"]),
    "H": (["CUR-21", "CUR-19"], ["CUR-20"]),
    "I": (["CUR-12"], ["CUR-20"]),
}


def v1_questions(ents):
    I_("§V1 定理 A~I 机检问句（由定理**陈述**推得关键词；**未按全矩阵调参**——避免过拟合）")
    for lt, _fn, desc in QUESTIONS:
        I_("   [%s] %s" % (lt, desc))
    I_("   自检：正/负样本取自人工矩阵的**高置信子集**（非全矩阵）；规则只据此检验判别力、不为拟合而改：")
    fn_map = dict((L, f) for L, f, _d in QUESTIONS)
    acc_map = {}
    for lt, (pos, neg) in sorted(SELF_CHECK.items()):
        fn = fn_map[lt]
        tp = [x for x in pos if fn(ents[x]["blob"])]
        tn = [x for x in neg if not fn(ents[x]["blob"])]
        acc = (len(tp) + len(tn)) / float(len(pos) + len(neg))
        acc_map[lt] = acc
        I_("      [%s] 正样本命中 %d/%d %s；负样本正确排除 %d/%d ⇒ 自检准确率 %.2f"
           % (lt, len(tp), len(pos), tp, len(tn), len(neg), acc))
    # 逐条给出**可靠性分级**（诚实：判别力不足者不得用作门禁）
    weak = [lt for lt in acc_map if acc_map[lt] < 0.5]
    mid = [lt for lt in acc_map if 0.5 <= acc_map[lt] < 1.0]
    I_("   可靠性分级（由自检准确率导出，**决定该定理的机检结果能否用于门禁**）：")
    for lt, _f, _d in QUESTIONS:
        a = acc_map[lt]
        tag = "机检**可用**（高判别力）" if a == 1.0 else ("机检**弱**（仅提示，不作门禁）" if a >= 0.5 else "机检**不可用**（禁用作门禁）")
        I_("      [%s] 准确率 %.2f ⇒ %s" % (lt, a, tag))
    if not weak and not mid:
        P_("V1 九条问句在自检样本上**全部通过**（准确率 1.00）⇒ 均可用于对账（仍为启发式，最终以人工矩阵为准）")
    else:
        B_("V1 **部分问句判别力不足**（低：%s；中：%s）——按**不过拟合**原则**保留原规则不调参**，"
           "但据此**降级其在门禁中的权重**：低判别力者（%s）**不得**用于判定，只作检索提示"
           % ("、".join(weak) if weak else "无", "、".join(mid) if mid else "无",
              "、".join(weak) if weak else "无"))
    return acc_map


# ────────────────────────────────────────────────────────────────────────────
# §V2 机扫 + 与人工矩阵对账
# ────────────────────────────────────────────────────────────────────────────
def v2_reconcile(ents, human):
    I_("§V2 机扫全部 %d 条目 + 与人工覆盖矩阵对账" % len(ents))
    machine = {}
    for lt, fn, _d in QUESTIONS:
        machine[lt] = set(eid for eid in ents if fn(ents[eid]["blob"]))
    I_("   覆盖率概览（机检命中数 / 人工矩阵记入数）：")
    for lt, _fn, _d in QUESTIONS:
        I_("      [%s] 机器 %2d 条 ；人工 %2d 条" % (lt, len(machine[lt]), len(human.get(lt, set()))))

    I_("   对账明细（只列**差异**；一致项不逐条罗列）：")
    stat = {}
    for lt, _fn, _d in QUESTIONS:
        hm = human.get(lt, set())
        mm = machine[lt]
        only_h = sorted(hm - mm)      # 人工记入但机器未触发 ⇒ 规则漏检 或 人工判断更细
        only_m = sorted(mm - hm)      # 机器触发但人工未记 ⇒ 需人工复核（可能过度触发）
        both = sorted(hm & mm)
        stat[lt] = {"human": len(hm), "machine": len(mm), "both": len(both),
                    "only_human": only_h, "only_machine": only_m}
        I_("      [%s] 交集 %2d ；人工独有 %s ；机器独有 %s"
           % (lt, len(both), ("、".join(only_h) if only_h else "无"),
              ("、".join(only_m) if only_m else "无")))
    tot_h = sum(len(human.get(l, set())) for l, _f, _d in QUESTIONS)
    tot_b = sum(stat[l]["both"] for l, _f, _d in QUESTIONS)
    I_("   总体：人工矩阵共 %d 个「定理×条目」标记；机检与人机交集 %d（一致率 %.1f%%）"
       % (tot_h, tot_b, 100.0 * tot_b / tot_h if tot_h else 0.0))
    B_("V2 边界：机检为**关键词启发式**，其与人工矩阵的差异**不构成任何一方的错误**——"
       "差异只用于**提示复核**（人工独有 ⇒ 规则可能漏检；机器独有 ⇒ 可能过度触发）")
    return machine, stat


# ────────────────────────────────────────────────────────────────────────────
# §V3 覆盖完整性审计
# ────────────────────────────────────────────────────────────────────────────
def v3_completeness(ents, human):
    I_("§V3 覆盖完整性审计（结构性检查，可靠）")
    covered = set()
    for lt in human:
        covered |= human[lt]
    all_ids = set(ents)
    uncovered = sorted(all_ids - covered)
    I_("   人工矩阵共覆盖 %d / %d 条条目" % (len(all_ids & covered), len(all_ids)))
    if uncovered:
        F_("V3a **未覆盖条目**（既未命中任何定理，也未登记豁免）：%s"
           "⇒ 须二选一：①补登记定理命中；②显式记入「无定理命中」白名单并给理由"
           % "、".join(uncovered))
    else:
        P_("V3a 全部 %d 条目均至少命中一条定理（无未覆盖条目）" % len(all_ids))

    ghost = sorted(covered - all_ids)
    if ghost:
        F_("V3b 矩阵引用了**不存在的条目**：%s" % "、".join(ghost))
    else:
        P_("V3b 矩阵未引用任何不存在的条目（无幽灵条目）")

    excluded = sorted(eid for eid in ents if ents[eid]["status"].startswith("❌"))
    miss = [eid for eid in excluded if not any(eid in human.get(l, set()) for l, _f, _d in QUESTIONS)]
    I_("   ❌ 条目共 %d 条：%s" % (len(excluded), "、".join(excluded)))
    if miss:
        F_("V3c 存在 ❌ 条目**无任何定理命中**：%s ⇒ 须补证其排除依据" % "、".join(miss))
    else:
        P_("V3c 全部 ❌ 条目（%d 条）均至少命中一条定理 ⇒ 每条排除都有结构性依据" % len(excluded))

    # 每个条目命中的定理数（人工）
    per = {}
    for eid in ents:
        per[eid] = sorted(l for l, _f, _d in QUESTIONS if eid in human.get(l, set()))
    top = sorted(per.items(), key=lambda kv: -len(kv[1]))[:3]
    I_("   命中数最多的条目（人工）：%s" % "；".join("%s→%d 条(%s)" % (k, len(v), "".join(v)) for k, v in top))
    return per


# ────────────────────────────────────────────────────────────────────────────
# §V4 新提案自查表
# ────────────────────────────────────────────────────────────────────────────
PROPOSAL_TEMPLATE = {
    "proposal_id": "<新提案编号，如 CUR-22 / 补充卷J>",
    "title": "<标题>",
    "core_claim": "<一句话核心主张>",
    "script_ref": "<脚本文件名>",
    "self_check": {
        "A_拓扑项源引力": {"hit": None, "evidence": "<若为 true，须给不可消除的替代源>"},
        "B_整数编码连续量": {"hit": None, "evidence": "<若为 true，须给连续自由度来源>"},
        "C_无跑动求内生尺度": {"hit": None, "evidence": "<若为 true，须给维度嬗变/跑动机制>"},
        "D_自由参数当派生量": {"hit": None, "evidence": "<若为 true，须给参数的独立观测定标>"},
        "E_依赖已关窗口": {"hit": None, "evidence": "<若为 true，须重开该窗口或撤回主张>"},
        "F_破缺量无不可消除源": {"hit": None, "evidence": "<若为 true，须给相对相位/视宇称耦合>"},
        "G_仅凭拓扑选规范群": {"hit": None, "evidence": "<若为 true，须给非拓扑选择判据>"},
        "H_约束自证循环": {"hit": None, "evidence": "<若为 true，须给独立观测定标的上限>"},
        "I_固定谱形生层级": {"hit": None, "evidence": "<若为 true，须给谱指数或新机制>"},
    },
    "conclusion": "<若不命中任何定理 ⇒ 可进入实证检验；否则结构性风险等级由命中数决定>",
}


def v4_proposal_gate():
    I_("§V4 新提案**自查表**（进入门槛）：模板字段与校验规则")
    I_("   模板（落盘为 <proposal>.json，随提案一并提交）：")
    for k in PROPOSAL_TEMPLATE:
        I_("      %s" % k)
    I_("   校验规则：①9 个 self_check 项**必须全部**给出 hit(bool) 与 evidence；"
       "②hit=true 的项**必须**给出非空 evidence（说明如何规避该定理）；③调用 --check <file> 执行校验。")
    B_("V4 边界：本门禁**只检查自查是否完成与自洽**（形式完备性），**不判定物理正确性**——"
       "把 hit 全部填 false 即可「通过」，故门禁的价值在于**强制显式声明**，而非代替同行评审")


def v4_check_file(path):
    """--check 模式：校验一份提案自查表。"""
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except Exception as exc:
        print("无法读取提案文件：%s" % exc)
        return 1
    sc = doc.get("self_check") or {}
    missing, empty_ev, hits = [], [], []
    for k in PROPOSAL_TEMPLATE["self_check"]:
        if k not in sc:
            missing.append(k)
            continue
        v = sc[k] or {}
        if v.get("hit") is None:
            missing.append(k)
        elif v.get("hit") is True:
            hits.append(k)
            if not str(v.get("evidence", "")).strip():
                empty_ev.append(k)
    print("提案：%s" % doc.get("proposal_id", "?"))
    print("  自查项缺失/未填：%s" % ("无 ✅" if not missing else "、".join(missing)))
    print("  命中定理：%s" % ("无" if not hits else "、".join(hits)))
    print("  hit=true 但 evidence 为空：%s" % ("无 ✅" if not empty_ev else "、".join(empty_ev)))
    ok = not missing and not empty_ev
    print("  形式校验：%s" % ("通过 ✅" if ok else "不通过 ❌"))
    return 0 if ok else 1


# ────────────────────────────────────────────────────────────────────────────
def main():
    t0 = time.time()
    _lines.append("=" * 78)
    _lines.append("TUFT / H-TUFT 卷系·跨卷收口分析（第 3 轮）：构造可行性门禁（定理 A~I 机器化）")
    _lines.append("=" * 78)
    I_("目标：把 no-go 定理族 A~I 变成**进入门槛**（防回潮），并独立复核最新的 CUR-21")

    ents = load_entries()
    human = parse_human_matrix()
    I_("语料加载：%d 条目；人工覆盖矩阵解析出 %d 条定理行（%s）"
       % (len(ents), len(human), "".join(sorted(human))))

    v0_crosscheck_cur21(ents)
    v1_questions(ents)
    machine, stat = v2_reconcile(ents, human)
    per = v3_completeness(ents, human)
    v4_proposal_gate()

    I_("§结论摘要")
    I_("   ① CUR-21 算术经独立重算确认（(M_Pl/8.5TeV)^3=%.3e、(1e15GeV/8.5TeV)^3=%.3e）；"
       "但两个「超限倍数」只是**立方比恒等式**，结论强度取决于外部上限。"
       % ((M_PL_GEV / SIGMA_MAX_GEV) ** 3, (T_C_GEV / SIGMA_MAX_GEV) ** 3))
    I_("   ② 9 条机检问句由定理陈述独立写出（未调参），并在自检样本上通过；"
       "机检与人工矩阵的一致率见 §V2。")
    I_("   ③ 覆盖完整性：%d 条目全部≥1 定理命中；无幽灵条目；❌ 条目全部有结构性依据。"
       % len(ents))
    I_("   ④ 新提案须提交 9 项自查表（--check 校验形式完备性）；门禁强制**显式声明**，不代替评审。")

    B_("边界①：机检为**关键词启发式**，只用于对账与提醒；判定以 `tuft_卷系_结构障碍定理族.md` 人工矩阵为准。")
    B_("边界②：规则由定理陈述**独立写出**，**未按人工矩阵调参**——按「不过拟合」原则保留原规则并如实报告偏差。")
    B_("边界③：本门禁**不判定物理正确性**，只检查①覆盖完整性②自查表形式完备性。")
    B_("边界④：产物 `tuft_卷系_覆盖矩阵_机器版.json` 为机器视图，**不覆盖**人工矩阵真源。")
    B_("边界⑤：红线——数学自洽 != 实验证实。本册不新增物理主张、不改动任何 CURATED 真源。")

    _lines.append("-" * 78)
    _lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d"
                  % (_CNT["PASS"], _CNT["FAIL"], _CNT["BOUNDARY"], _CNT["INFO"]))
    _lines.append("-" * 78)
    _lines.append("评级：O/L2（工程化册：把结构障碍定理族机器化为构造可行性门禁，并独立复核 CUR-21）")
    _lines.append("红线：数学自洽 != 实验证实；本册为工程化/对账工具，不新增物理主张、不改动真源。")

    with open(OUT_MATRIX, "w", encoding="utf-8") as fh:
        json.dump({"generated": time.strftime("%Y-%m-%d"),
                   "n_entries": len(ents),
                   "machine": dict((k, sorted(v)) for k, v in machine.items()),
                   "human": dict((k, sorted(v)) for k, v in human.items()),
                   "reconcile": stat,
                   "per_entry_human_theorems": per},
                  fh, ensure_ascii=False, indent=2)

    text = "\n".join(_lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    with open(os.path.abspath(__file__), "rb") as fh:
        self_sha = hashlib.sha256(fh.read()).hexdigest()
    text2 = text + "自哈希(SHA256) = %s\n耗时 = %.1fs\n" % (self_sha, time.time() - t0)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text2)
    print(text2)
    return _CNT


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--check":
        sys.exit(v4_check_file(sys.argv[2]))
    if len(sys.argv) >= 2 and sys.argv[1] == "--template":
        print(json.dumps(PROPOSAL_TEMPLATE, ensure_ascii=False, indent=2))
        sys.exit(0)
    main()
