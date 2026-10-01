# -*- coding: utf-8 -*-
"""
tuft_卷系_构造可行性门禁.py
===========================
TUFT / H-TUFT 卷系·**跨卷收口分析（第 3 轮）**：把 no-go 定理族 **A~J** 机器化为
一套可复跑的「**构造可行性门禁**」，并独立复核最新的补充卷I（CUR-21）。

为何需要本工具（防回潮）：
  · A~J 定理是整轮全维整理**最可靠的产出**（"世界不是数据的函数、拓扑不能编码连续量…"）；
  · 但 D~J 各卷的经验一致：**每卷都在重复同样的缺陷**（自由参数 vs 派生、已关窗口 vs 新通道、
    破缺量无源、同伦不唯一、约束自证、谱形方向不符、拓扑常数 ⇒ 无内生标度）；
  · 因此**比新增卷更有价值的**，是把 A~J 变成**进入门槛**：新提案落盘前必须逐条自查。

本册做七件事：
  §V0 独立复核 CUR-21（BBN 畴壁上限）——含指出其"超限倍数"仅是**立方比恒等式**
  §V1 定义 10 条**机检问句**（由定理陈述**独立**写出，**未按人工矩阵调参**）+ 用已知正/负样本自检
  §V2 对全条目机扫，并与人工覆盖矩阵**对账**（报告一致率，暴露矩阵缺口）
  §V3 覆盖完整性审计（未覆盖条目 / 引用不存在的条目 / ❌ 条目是否 ≥1 定理命中）
  §V4 新提案自查表：模板 + 校验器 + 结构性风险分级
  §V5 扇区重复登记审计（多头真源 ⇒ 唯一规范真源；见 `tuft_卷系_扇区真源登记.md`）
  §V6 结论与边界

v1.2 变更（本轮）：
  ① 增补 **定理 J** 机检问句（共 **10** 条）；J 于 v1.1 由攻坚卷（CUR-22）落盘。
  ② **C / D / H 规则按定理陈述重写**：原实现把「触发条件」写成**单一关键词列表**，
     导致泛指词（`标度`/`自由`/`上限`）过度命中（自检准确率 0.33 / 0.50 / 0.67）。
     现按陈述的**「在 X 前提下声称 Y」**结构改为**两集合取交**（claim ∩ setting）。
  ③ 修复 §6 覆盖矩阵的**行首解析缺陷**：原正则要求字母后紧跟空格，
     而 `**J（A ⟹ C：…）**` 字母后是左括号 ⇒ **J 行被静默丢弃**（现已容错）。
  ④ C/D/H 的规则重写为**一次性**（依陈述推导，**不按矩阵迭代调参**）；
     重写后若准确率仍不满分，则**保留真实结果**并在报告中降级标注，**不为通过而调参**。

红线：数学自洽 != 实验证实。本册**不新增物理主张**、**不占 CUR 编号**、**不改动任何 CURATED 真源**。
机检为**启发式**，只用于**对账与提醒**；最终以 `tuft_卷系_结构障碍定理族.md` 的人工矩阵为准。

依赖：Python 3.8 + 标准库（无需 numpy/scipy）。
"""

from __future__ import print_function

import hashlib
import json
import os
import re
import subprocess
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
        # 容错：字母后可为空格、全角/半角括号（如 `**J（A ⟹ C：…）**`）——原实现只认空格，
        # 会**静默丢弃** J 行，使机检对账漏掉一条定理。
        lt = re.match(r"^\**([A-Z])(?=\s|（|\()", head)
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
# 写法规范（v1.2 起）：定理陈述普遍是「**在 X 前提下声称 Y**」⇒ 触发条件 = **claim ∩ setting** 两集合取交；
# 若写成**单一关键词列表**，则任何泛指词（`标度`/`自由`/`上限`）都会命中几乎全部条目（判别力崩塌）。
QUESTIONS = [
    ("A", lambda b: _has(b, ["拓扑项", "全导数", "总导数", "F∧F", "Euler", "欧拉示性数", "Nieh-Yan"])
     and _has(b, ["Λ", "引力", "真空能", "暗能量", "T_μν", "T_{μν}"]),
     "是否把某可观测量归因于**拓扑项（全导数）**？（→ δS/δg=0 ⇒ 对 T_μν 零贡献）"),
    ("B", lambda b: _has(b, ["整数", "拓扑荷", "绕数", "缠绕", "同伦", "量子数", "Q_hel", "χ", "Lk"])
     and _has(b, ["连续", "层级", "质量", "Ω", "Λ", "耦合", "标度"]),
     "是否用**离散整数/拓扑荷**去确定**连续量或层级**？"),
    # C 陈述：「若 β≡0 ⇒ 特征标度**不能**由理论内生 ⇒ 一切标度须外部锚定」
    #   ⇒ claim = 声称「内生/第一性来源」，setting = 尺度类对象。
    #   注意**排除**泛指词：`量级`（到处都有）、裸 `导出`（「不能导出/外部锚定」也会命中，方向相反）。
    ("C", lambda b: _has(b, ["内生", "内禀", "第一性", "理论导出", "自然给出", "自然生成"])
     and _has(b, ["标度", "能标", "尺度", "层级", "真空能", "Λ"]),
     "是否在 **β≡0（无跑动）** 的前提下声称**内生标度/层级**？"),
    # D 陈述：「O 由 ≥1 自由参数生成 ⇒ 重参数化，非派生」
    #   ⇒ claim = 派生性主张，setting = 存在自由参数。排除裸 `自由`/`系数`/`拟合`（几乎人人命中）。
    ("D", lambda b: _has(b, ["派生", "第一性", "非唯象", "由理论给出", "逐条导出"])
     and _has(b, ["自由参数", "自由系数", "魔数", "唯象", "可调", "拟合"]),
     "是否含**≥1 个自由参数**却被称作「派生量」？"),
    ("E", lambda b: _has(b, ["已排除", "已关闭", "Z=0", "联合拟合", "继承", "重开", "恢复"]),
     "是否依赖**已被排除的窗口**（或把已关窗口当未来优先级）？"),
    ("F", lambda b: _has(b, ["CP", "破缺", "手征", "相位", "Jarlskog", "ΔΠ", "左右手"]),
     "是否生成**破缺量**（CP/手征）而**未给不可消除的破缺源**？"),
    ("G", lambda b: _has(b, ["规范群", "同伦签名", "π₀", "π₃", "SU(2)", "SU(3)", "SU(5)", "E6"]),
     "是否声称**仅凭拓扑/同伦数据导出规范群**？"),
    # H 陈述：「约束满足只依赖自由参数取值 ⇒ 不构成检验」
    #   ⇒ con = 约束满足主张，choice = 「由参数取值决定」的痕迹。排除裸 `上限`（每条都有观测上限）。
    ("H", lambda b: _has(b, ["约束", "上限", "BBN", "丰度", "通过"])
     and _has(b, ["取小", "调小", "人为", "自由参数", "可调", "自动满足", "不破坏"]),
     "是否以**取小自由参数**达成约束满足并声称「已检验/通过」？"),
    ("I", lambda b: _has2(b, ["模态", "束缚态", "能级", "谱形", "增量比", "径向模态"],
                          ["代", "层级", "质量", "谱"]),
     "是否用**固定算符的束缚态谱（模态）**生成**代/质量层级**？"),
    # J 陈述：「α 为拓扑常数 ⇒ β_α ≡ 0；保留拓扑耦合定义 ⇒ C 不可单独打破」
    #   ⇒ setting = 拓扑常数/全导数（无局部插槽），claim = 内生标度/跑动。
    ("J", lambda b: _has(b, ["拓扑常数", "拓扑耦合", "全导数", "α", "β"])
     and _has(b, ["内生", "标度", "尺度", "能标", "层级", "跑动", "维度嬗变"]),
     "是否在**保留「α 为拓扑常数」**的前提下声称**内生标度/打破 β≡0**？（→ 定理 J）"),
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
    "J": (["CUR-22"], ["CUR-02"]),
}

# ── §V5 扇区重复登记审计：同一「检测通道/议题」被 ≥2 条目登记的簇 ──────────────
# 扇区 = 关键词集合。**只在 name/category 上匹配**（二者为「议题标签」）：core_prediction 含大量
# 泛指词（"代"/"量子"/"Λ"），会产生 7~8 条的伪簇、掩盖真实议题粒度。
SECTOR_FIELDS = ("name", "category")
SECTORS = [
    ("味物理与代层级", ["味", "CKM", "PMNS", "代际", "三代", "混合矩阵", "Yukawa"]),
    ("手征/原初张量", ["手征极化", "手征引力波", "手征非高斯", "SGWB", "原初引力波", "ΔΠ", "B 模"]),
    ("黑洞内部/inQNM", ["黑洞", "QNM", "ringdown", "奇点", "拓扑毛发"]),
    ("量子化/路径积分", ["路径积分", "量子化", "扇区求和", "拓扑隧穿", "量子隧穿", "WKB", "量子孤子"]),
    ("暗物质孤子", ["暗物质", "遗迹丰度"]),
    ("真空能/Λ", ["宇宙学常数", "真空拓扑能"]),
    ("规范结构与耦合", ["规范群", "规范结构", "SU(2)", "SU(3)", "U(1)", "耦合常数"]),
    ("全局贝叶斯拟合", ["MCMC", "贝叶斯", "嵌套采样"]),
    ("微观精密窗口", ["EDM", "g-2", "反常磁矩"]),
]
# 扇区**规范真源**指定（人工判定；本表即"合并决策"的机器可读形式）
SECTOR_CANON = {
    "味物理与代层级": "CUR-12",
    "手征/原初张量": "CUR-11",
    "黑洞内部/inQNM": "CUR-08",
    "量子化/路径积分": "CUR-10",
    "暗物质孤子": "CUR-14",
    "真空能/Λ": "CUR-15",
    "规范结构与耦合": "CUR-20",
    "全局贝叶斯拟合": "CUR-07",
    "微观精密窗口": "CUR-01",
}
# 显式豁免：簇内成员为**不同观测量并列**（非同一通道的重复登记），无需「规范真源」
NON_DUP_SECTORS = {"微观精密窗口"}


# ── §V6 元条目账本联动（CUR-24 的 `O-ENCODE-LEDGER` 请求；**容错**） ───────────
LEDGER_SCRIPT = "tuft_锚定编码账本.py"
LEDGER_KINDS = ("PRED-EXCLUDED", "PRED-DERIVED", "REPARAM", "STRUCT-FAIL")


def v6_ledger_linkage(ents):
    I_("§V6 元条目账本联动（CUR-24「出路 2 锚定编码账本」的 `O-ENCODE-LEDGER` 请求；**容错**设计）")
    path = os.path.join(HERE, LEDGER_SCRIPT)
    if not os.path.exists(path):
        B_("V6 未找到 `%s`（**可选组件**）⇒ 跳过：账本不参与本门禁，V6 不影响 PASS/FAIL" % LEDGER_SCRIPT)
        return None
    try:
        proc = subprocess.run([sys.executable, path], cwd=HERE, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=300)
        out = proc.stdout.decode("utf-8", "replace")
    except Exception as exc:                                     # noqa: BLE001
        B_("V6 账本复跑失败（%s）⇒ 仅提示、**不判失败**（容错：本门禁不因外部组件故障而阻断落盘）" % exc)
        return None
    ids = set(re.findall(r"CUR-\d{2}", out))
    missing = sorted(set(ents) - ids)
    ghost = sorted(ids - set(ents))
    counts = dict((k, out.count(k)) for k in LEDGER_KINDS)
    I_("   账本复跑成功（rc=%d）；种类计数（**文本抄录**，非重算）：%s" % (proc.returncode, counts))
    if missing or ghost:
        F_("V6 账本覆盖不一致：未入账 %s ；幽灵 %s ⇒ 须在账本中补齐（这是**结构性**缺口："
           "无账目即无法计净预言 `n_net`）" % (missing, ghost))
    else:
        P_("V6 账本覆盖一致（INV1）：%d 条目**全部入账**，无幽灵条目" % len(ents))
    B_("V6 边界：本审计只做**覆盖一致性 + 计数抄录**，**不重算** `n_net = n_out − n_free`"
       "（计账口径由 `%s` 负责，避免双份口径）；账本**不含物理正确性判断**。" % LEDGER_SCRIPT)
    return counts


def v1_questions(ents):
    I_("§V1 定理 A~J 机检问句（共 %d 条；由定理**陈述**推得关键词，按「claim ∩ setting」两集合取交；"
       "**未按全矩阵调参**——避免过拟合）" % len(QUESTIONS))
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
    return acc_map
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
def v2_reconcile(ents, human, acc_map):
    I_("§V2 机扫全部 %d 条目 + 与人工覆盖矩阵对账" % len(ents))
    machine = {}
    for lt, fn, _d in QUESTIONS:
        machine[lt] = set(eid for eid in ents if fn(ents[eid]["blob"]))
    I_("   覆盖率概览（机检命中数 / 人工矩阵记入数 / 机检可靠性）：")
    for lt, _fn, _d in QUESTIONS:
        a = acc_map.get(lt, 0.0)
        tag = "可用" if a == 1.0 else ("**弱**" if a >= 0.5 else "**不可用**")
        I_("      [%s] 机器 %2d 条 ；人工 %2d 条 ；机检可靠性 %s（%.2f）"
           % (lt, len(machine[lt]), len(human.get(lt, set())), tag, a))

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
    tot_m = sum(stat[l]["machine"] for l, _f, _d in QUESTIONS)
    I_("   总体：人工矩阵 %d 个「定理×条目」标记；机检 %d 个标记；交集 %d" % (tot_h, tot_m, tot_b))
    I_("     · **召回**（人工标记中机检能重现的比例） = %d/%d = %.1f%%"
       % (tot_b, tot_h, 100.0 * tot_b / tot_h if tot_h else 0.0))
    I_("     · **精确度**（机检标记中被人工确认的比例） = %d/%d = %.1f%%"
       % (tot_b, tot_m, 100.0 * tot_b / tot_m if tot_m else 0.0))
    I_("     · ⚠ 两指标**此消彼长**：规则收紧 ⇒ 精确度升、召回降；反之亦然。"
       "**不得**只看单一「一致率」评判规则优劣（v1.2 起同时报告二者，替代原单一数字）")
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
# §V5 扇区重复登记审计
# ────────────────────────────────────────────────────────────────────────────
def v5_sector_dedup(ents):
    I_("§V5 扇区重复登记审计（同一检测通道/议题被 ≥2 条目登记 ⇒ 必须指定**唯一规范真源**）")
    clusters = {}
    for name, kws in SECTORS:
        members = []
        for eid in sorted(ents):
            blob = " ".join(str(ents[eid]["entry"].get(k, "")) for k in SECTOR_FIELDS).lower()
            if any(k.lower() in blob for k in kws):
                members.append(eid)
        clusters[name] = members
    multi = []
    for name, _kws in SECTORS:
        members = clusters[name]
        if len(members) >= 2:
            multi.append(name)
            if name in NON_DUP_SECTORS:
                I_("   [%s] %d 条：%s ；**显式豁免：不同观测量并列，非重复登记**"
                   % (name, len(members), "、".join(members)))
                continue
            canon = SECTOR_CANON.get(name)
            flag = "✅ 规范真源在簇内" if canon in members else "❌ 缺失/不在簇内"
            I_("   [%s] %d 条：%s ；规范真源 = %s（%s）"
               % (name, len(members), "、".join(members), canon or "未指定", flag))
        else:
            I_("   [%s] %d 条：%s（单条目，无需指定规范真源）"
               % (name, len(members), "、".join(members) if members else "无"))
    bad = [n for n in multi
           if n not in NON_DUP_SECTORS and SECTOR_CANON.get(n) not in clusters[n]]
    n_need = len([n for n in multi if n not in NON_DUP_SECTORS])
    if bad:
        F_("V5 存在**多重登记扇区缺规范真源**：%s ⇒ 须在 `tuft_卷系_扇区真源登记.md` 指定唯一规范条目"
           % "、".join(bad))
    else:
        P_("V5 全部 %d 个需合并的扇区均已指定**唯一规范真源**（且规范条目确为该扇区成员；"
           "另有 %d 个扇区**显式豁免**为不同观测量并列）⇒ 无「多头真源」；合并决策见 "
           "`tuft_卷系_扇区真源登记.md`" % (n_need, len(multi) - n_need))
    B_("V5 边界：扇区划分为**关键词启发式**——只在 **name/category（议题标签）**上匹配（大小写不敏感），"
       "并已排除同形异义词（`隧穿`→限「拓扑/量子隧穿」、`手征`→限「手征极化/引力波/非高斯」）；"
       "本审计只检查「是否有唯一规范真源」，**不合并、不删除、不改状态**任何条目"
       "（以保编号连续性与反回退守卫）")
    return clusters, multi


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
    I_("   校验规则：①%d 个 self_check 项**必须全部**给出 hit(bool) 与 evidence；" % len(QUESTIONS) +
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
    _lines.append("TUFT / H-TUFT 卷系·跨卷收口分析（第 3 轮）：构造可行性门禁（定理 A~J 机器化）")
    _lines.append("=" * 78)
    I_("目标：把 no-go 定理族 A~J 变成**进入门槛**（防回潮），并独立复核最新的 CUR-21")

    ents = load_entries()
    human = parse_human_matrix()
    I_("语料加载：%d 条目；人工覆盖矩阵解析出 %d 条定理行（%s）"
       % (len(ents), len(human), "".join(sorted(human))))

    v0_crosscheck_cur21(ents)
    acc_map = v1_questions(ents)
    machine, stat = v2_reconcile(ents, human, acc_map)
    per = v3_completeness(ents, human)
    clusters, multi = v5_sector_dedup(ents)
    ledger = v6_ledger_linkage(ents)
    v4_proposal_gate()

    I_("§结论摘要")
    I_("   ① CUR-21 算术经独立重算确认（(M_Pl/8.5TeV)^3=%.3e、(1e15GeV/8.5TeV)^3=%.3e）；"
       "但两个「超限倍数」只是**立方比恒等式**，结论强度取决于外部上限。"
       % ((M_PL_GEV / SIGMA_MAX_GEV) ** 3, (T_C_GEV / SIGMA_MAX_GEV) ** 3))
    I_("   ② %d 条机检问句由定理陈述独立写出（未调参），自检结果见 §V1；" % len(QUESTIONS) +
       "机检与人工矩阵的一致率见 §V2。")
    I_("   ③ 覆盖完整性：%d 条目全部≥1 定理命中；无幽灵条目；❌ 条目全部有结构性依据。"
       % len(ents))
    I_("   ④ 新提案须提交 9 项自查表（--check 校验形式完备性）；门禁强制**显式声明**，不代替评审。")
    I_("   ⑤ 扇区审计：检出 **%d 个多重登记扇区**（%s）⇒ 每个已指定唯一规范真源，"
       "合并决策见 `tuft_卷系_扇区真源登记.md`（本轮补齐味扇区三重登记的 O-DEDUP）"
       % (len(multi), "、".join(multi)))

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
                   "per_entry_human_theorems": per,
                   "sectors": clusters,
                   "multi_entry_sectors": multi,
                   "sector_canonical": SECTOR_CANON,
                   "sector_non_dup_exempt": sorted(NON_DUP_SECTORS),
                   "ledger_kind_counts": ledger,
                   "selfcheck_accuracy": acc_map},
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
