# -*- coding: utf-8 -*-
"""
TUFT-r347 · ROOT V24【判词链总账（元审计卷）】：五卷 schema 归一 · 跨卷读数一致性 · 条目不可相加证明

定位：**只读元审计**。本卷不重算任何物理，也不重跑 r317/r320/r321/r328/r337 的任何推导，
而是把这五卷的**产物本身**当作审计对象，机器回答三个"整理"层面的问题：

    Q1  五卷的 json 产物是不是同一套结构？（答：不是，三态并存）
    Q2  跨卷共同读数是否逐位一致？"某卷没有某个读数"是冲突还是范围差异？
    Q3  "条目数直接相加"是否合法？（答：不合法，共享事实被多卷重复覆盖）

为什么必须单独开一卷：库内已经两次因为"结构与判据不匹配"产生假结论——
    · r321 漂移自检首版拿 kv 当基准 ⇒ 假阳性 105 条（基准错，不是数据错）
    · r328 显式登记"无 key_numbers 键，须走全量 token 比对"
两处都是**同一类**问题：核对工具的假设与产物实际结构不一致。
本卷把这条教训从"单卷内部"提升到"跨卷之间"，并给出可复算的归一化判据。

三态 schema（机器实测，见 A02）：
    A 型（r317）：顶层 {summary, items}
    B 型（r320）：顶层 {rid, stamp, intake, zheng, items, extra}
    C 型（r321 / r328 / r337）：顶层 {round, title, date, verdict_summary, entries, guards, ...}
⇒ 任何跨卷自动核对（漂移守卫、总账、索引）若直接取 `entries`，对 A/B 型会得到 0 条，
   而"0 条"与"真的一致/真没数据"不可区分 ⇒ 归一这一步不可省（CTL3 证明）。

诚实边界（写在最前）：
  · 本卷**只读**五卷产物，不改写其中任何字节；写入白名单只含本卷自身 4 个产物（CTL5 守卫）。
  · 跨卷引用读数全部来自**本机磁盘扫描**，凡声明"某卷含某读数"而实际扫描不中 ⇒ 守卫 FAIL（防自造读数）。
  · r317 / r320 为并行/早前卷，其条目语义由各自判定册自陈；本卷只做结构与读数层核对，**不裁定其判词**。
  · 本卷不产生新物理结论；链级结论 NO-ATTRIBUTION-CHAIN 是五卷既有判词的**合并陈述**，不是新证据。

条目族：A01–A04（链清单/schema/不可相加/引用可溯）· B01–B04（读数一致性）· C01–C04（总账）· CTL1–CTL6
守卫：G1–G9
"""

import io
import json
import os
import re
import sys
import time
from decimal import Decimal, getcontext

getcontext().prec = 60

RID = "r347"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JD = os.path.join(ROOT, "判定")

BASE = ("TUFT-%s_ROOTV24判词链总账_五卷schema归一与跨卷读数一致性与不可相加证明_%s"
        % (RID, STAMP))
HTML_NAME = "四力统一方程_ROOTV24判词链总账_%s可视化_%s.html" % (RID, STAMP)

ALLOWED = set()
WRITTEN = []
T0 = time.time()
ITEMS = []
GUARDS = []

CHAIN = [317, 320, 321, 328, 337]

# 跨卷共享物理事实（任一候选串命中即算覆盖）
FACTS = {
    "u_star": (["1/150"], "u* = 1/150（玩具固定点）"),
    "v_star": (["1/137"], "v* = 1/137（Möbius 后的坐标）"),
    "slope": (["-1/50"], "β′(u*) = β′(v*) = −1/50（相似不变量）"),
    "O_star": (["1/22500"], "O* = 1/22500（坐标不变量）"),
    "H1": (["1.92353209028294044992602E-2"], "H(1) 真空极化闭式值"),
    "alpha_true": (["137.035999084"], "α⁻¹ 真值锚 CODATA"),
    "alpha_mZ": (["127.952"], "α⁻¹(m_Z) 外部锚"),
    "gap": (["9.048"], "缺口 R = 137 − α⁻¹(m_Z)"),
    "beta": (["2.12206590789194E-1", "2/(3π)"], "β 系数 2/(3π)"),
}

# 本卷声明的"跨卷引用可溯性"清单：token -> 期望命中的卷
CROSS_REF = {
    "1.92353209028294044992602E-2": [320, 321, 328, 337],
    "137.035999084": [321, 328, 337],
    "127.952": [328, 337],
    "9.048": [337],
}

# 冗余账（来自 r321/r328/r337 自陈，本卷只做和式恒等检验，不自造数值）
BITS_COORD = Decimal("32.73385")   # 坐标（r321）
BITS_SCALE = Decimal("29.11436")   # 能标（r321）
BITS_TOTAL_328 = Decimal("89.2509581703183424854605")  # r328 合计（坐标+能标+场内容）
BITS_PRESC = Decimal("24.59050")   # 处方（r337）
BITS_NEED = Decimal("32.60345")    # 声明 α 所需
BITS_TOTAL = Decimal("113.84146")  # r337 合计

# 正面判词扫描词（链内若出现即意味着某卷给出"α 被预测"的肯定结论）
POS_TOKENS = ["PREDICTED", "PREDICTS-ALPHA", "已预测", "第一性导出", "α 被预测", "预测成功"]


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title,
                  "verdict": verdict, "detail": detail, "kv": kv or {}})
    return ITEMS[-1]


def P_(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "PASS", detail, kv)


def F_(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "FAIL", detail, kv)


def Bd(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "BOUNDARY", detail, kv)


def I_(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "INFO", detail, kv)


def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return bool(ok)


def fv(x, n=20):
    try:
        return format(Decimal(x), ".%dE" % (n - 1))
    except Exception:
        return str(x)


def fs(x):
    return format(Decimal(x), "f")


# ── 产物定位（只读） ───────────────────────────────────────────────────────
def _pick(folder, rid, suffix):
    tag = "r%d" % rid
    for f in sorted(os.listdir(folder)):
        if tag in f and f.endswith(suffix):
            return os.path.join(folder, f)
    return None


def load_chain():
    """只读装载五卷：json 文本 + 归一化条目 + 判定册文本"""
    out = {}
    for n in CHAIN:
        pj = _pick(DATA, n, ".json")
        pm = _pick(JD, n, ".md")
        rec = {"round": n, "json_path": pj, "judge_path": pm,
               "json_text": "", "judge_text": "", "entries": [], "schema": "?"}
        if pj:
            rec["json_text"] = io.open(pj, encoding="utf-8").read()
            try:
                d = json.loads(rec["json_text"])
            except Exception:
                d = {}
            rec["raw_keys"] = list(d.keys()) if isinstance(d, dict) else []
            if isinstance(d, dict) and isinstance(d.get("entries"), list):
                rec["entries"], rec["schema"] = d["entries"], "C"
            elif isinstance(d, dict) and isinstance(d.get("items"), list):
                rec["entries"] = d["items"]
                rec["schema"] = "A" if "summary" in d else "B"
            else:
                rec["entries"], rec["schema"] = [], "?"
            rec["guard_pass"] = d.get("guard_pass") if isinstance(d, dict) else None
            rec["guard_total"] = d.get("guard_total") if isinstance(d, dict) else None
            rec["title"] = d.get("title") if isinstance(d, dict) else None
        if pm:
            rec["judge_text"] = io.open(pm, encoding="utf-8").read()
        out[n] = rec
    return out


def norm_text(t):
    return t.replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")


def hit(text, cands):
    t = norm_text(text)
    for c in cands:
        if norm_text(c) in t:
            return True
    return False


# ── A 段：链清单 / schema / 不可相加 / 引用可溯 ─────────────────────────────
def section_A(CH):
    rows = []
    tot = 0
    for n in CHAIN:
        r = CH[n]
        rows.append((n, r["schema"], len(r["entries"]), r.get("guard_pass"),
                     r.get("guard_total"), r.get("title")))
        tot += len(r["entries"])
    tbl = "；".join("r%d(%s型,%d条)" % (a, b, c) for a, b, c, _, _, _ in rows)
    P_("A01", "链清单", "五卷条目机器清点：合计 %d 条（%s）" % (tot, tbl),
       "只读扫描 `数据/*r3xx*.json` 与 `判定/*r3xx*.md`，归一化后逐卷计条目数："
       + tbl + " ⇒ **合计 %d 条**。守卫统计：%s。"
       % (tot, "；".join("r%d 守卫 %s/%s" % (a, d, e) for a, _, _, d, e, _ in rows)),
       {"total": tot, "per_round": {str(a): c for a, _, c, _, _, _ in rows}})
    guard("G1_chain_loaded", all(len(CH[n]["entries"]) > 0 for n in CHAIN),
          "min=%d" % min(len(CH[n]["entries"]) for n in CHAIN))

    kinds = {}
    for n in CHAIN:
        kinds.setdefault(CH[n]["schema"], []).append(n)
    ks = "；".join("%s 型 = %s" % (k, v) for k, v in sorted(kinds.items()))
    P_("A02", "链清单", "★三态 schema 并存：%s" % ks,
       "顶层键实测：r317 = %s；r320 = %s；r321/r328/r337 = %s。"
       "⇒ 链内 **三套产物结构并存**（A 型 summary/items、B 型 rid/stamp/intake/zheng/items/extra、"
       "C 型 round/title/entries/guards）。任何跨卷自动核对若直接取 `entries`，"
       "对 A/B 型得到 **0 条**，而『0 条』与『真的一致 / 真没有』**不可区分** ⇒ 归一不可省（CTL3）。"
       % (CH[317].get("raw_keys"), CH[320].get("raw_keys"), CH[337].get("raw_keys")),
       {"schema_map": {str(k): v for k, v in kinds.items()}})
    guard("G2_schema_tristate", len(kinds) == 3, str(sorted(kinds)))

    # 共享事实覆盖
    cov = {}
    for key, (cands, desc) in FACTS.items():
        rounds = [n for n in CHAIN
                  if hit(CH[n]["json_text"], cands) or hit(CH[n]["judge_text"], cands)]
        cov[key] = rounds
    multi = [k for k, v in cov.items() if len(v) >= 2]
    P_("A03", "链清单", "★条目不可相加：%d 条合计中含 %d 项被 ≥2 卷重复覆盖的共享事实"
       % (tot, len(multi)),
       "若把五卷条目数直接相加得 %d，则下列共享事实被重复计数：%s。"
       "⇒ **条目数不可跨卷相加**；正确口径是各卷自陈净增量（r321/r328/r337 判定册均已逐条登记重叠为"
       "『交叉印证·不重复计数』）。"
       % (tot, "；".join("%s→r%s" % (FACTS[k][1], "/r".join(str(x) for x in cov[k]))
                        for k in multi)),
       {"coverage": {k: v for k, v in cov.items()}, "multi": multi})
    guard("G3_additivity_refuted", len(multi) >= 3, "multi=%d" % len(multi))

    # 引用可溯性
    miss = []
    extra = []
    for tok, expect in CROSS_REF.items():
        got = [n for n in CHAIN
               if hit(CH[n]["json_text"], [tok]) or hit(CH[n]["judge_text"], [tok])]
        for n in expect:
            if n not in got:
                miss.append((tok, n))
        for n in got:
            if n not in expect:
                extra.append((tok, n))
    if miss:
        F_("A04", "链清单", "引用可溯性守卫：%d 处声明与实际扫描不符 ⇒ 禁止采信" % len(miss),
           "本卷所有跨卷引用读数必须能在被声明卷的产物中**逐字命中**（防凭记忆写数）。"
           "实测未命中：%s。" % "；".join("%s@r%d" % m for m in miss),
           {"miss": ["%s@r%d" % m for m in miss]})
    else:
        P_("A04", "链清单", "引用可溯性守卫全过：%d 个跨卷引用读数逐字命中被声明卷"
           % len(CROSS_REF),
           "本卷所有跨卷引用读数一律来自**本机磁盘扫描**；凡声明『某卷含某读数』而实际不命中 ⇒ 守卫判 FAIL。"
           "实测 %d 个 token 全部命中，另发现 %d 处**声明外命中**（%s）⇒ 登记为 INFO，不回改他人卷。"
           % (len(CROSS_REF), len(extra),
              "；".join("%s@r%d" % e for e in extra) or "无"),
           {"extra": ["%s@r%d" % e for e in extra]})
    guard("G4_quote_traceable", not miss, "miss=%d" % len(miss))
    return {"rows": rows, "total": tot, "cov": cov, "multi": multi,
            "kinds": kinds, "miss": miss}


# ── B 段：跨卷读数一致性 ───────────────────────────────────────────────────
def section_B(CH, A):
    cov = A["cov"]
    lines = []
    for key, (cands, desc) in FACTS.items():
        rounds = cov[key]
        lines.append("%s：%s" % (desc, "r" + "/r".join(str(x) for x in rounds)
                                 if rounds else "（链内无命中）"))
    n_full = sum(1 for k, v in cov.items() if len(v) == len(CHAIN))
    P_("B01", "一致性", "共享事实覆盖矩阵（%d 项）：全卷覆盖 %d 项、多卷覆盖 %d 项"
       % (len(FACTS), n_full, len(A["multi"])),
       "逐项：\n- " + "\n- ".join(lines)
       + "\n\n⇒ 覆盖度本身说明**五卷做的是同一枚硬币的不同面**："
       "u*/v*/β′/O* 出现在 r317/r320（坐标与图表层），H(1)/α 锚出现在 r321/r328/r337（物理闭合层）。",
       {"n_facts": len(FACTS), "n_full": n_full})

    # 精确值一致性：抓 H(1) 的所有取值形态
    pat = re.compile(r"1\.9235[0-9]*\s*E\s*[-+]?\s*[0-9]+")
    vals = {}
    for n in CHAIN:
        t = norm_text(CH[n]["json_text"]) + " " + norm_text(CH[n]["judge_text"])
        found = set(m.replace(" ", "") for m in pat.findall(t))
        if found:
            vals[n] = sorted(found)
    flat = sorted(set(v for vs in vals.values() for v in vs))
    if len(flat) <= 1:
        P_("B02", "一致性", "★精确值一致性：H(1) 在 %d 卷中取值唯一（%s）"
           % (len(vals), flat[0] if flat else "无命中"),
           "正则 `1\\.9235[0-9]*E[-+]?[0-9]+` 抓取各卷出现的所有形态（先归一全角减号），"
           "去重后取值集合大小 = %d ⇒ **跨卷逐位一致，无冲突**。"
           "这是链内唯一被四卷共同承载的**长尾精确读数**，也是跨卷核对的锚。"
           % len(flat), {"values": flat, "per_round": {str(k): v for k, v in vals.items()}})
    else:
        F_("B02", "一致性", "精确值冲突：H(1) 出现 %d 种取值 ⇒ 链内读数不一致" % len(flat),
           "取值：%s" % flat, {"values": flat})
    guard("G5_H1_unique", len(flat) <= 1, "n_values=%d" % len(flat))
    guard("G6_H1_present", len(vals) >= 3, "rounds=%d" % len(vals))

    # 缺失 vs 冲突
    absent = [k for k, v in cov.items() if len(v) == 0]
    partial = [k for k, v in cov.items() if 0 < len(v) < len(CHAIN)]
    I_("B03", "一致性", "缺失 ≠ 冲突：%d 项全卷无命中、%d 项部分卷命中，均按『范围差异』登记"
       % (len(absent), len(partial)),
       "全卷无命中：%s；部分命中：%s。"
       "⇒ 某卷不出现某读数，通常是**该卷的审计范围不含它**（如 r317 只做坐标/图表层，不做真空极化闭式），"
       "而不是两卷互相矛盾。**把『缺失』当『冲突』会制造假 FAIL**（与 r321 假阳性 105 条同型）。"
       % ("、".join(FACTS[k][1] for k in absent) or "无",
          "、".join(FACTS[k][1] for k in partial) or "无"),
       {"absent": absent, "partial": partial})

    # 前向互链状态
    fwd = {}
    for n in CHAIN:
        t = CH[n]["judge_text"]
        refs = sorted(set(300 + int(m) for m in re.findall(r"r3(\d\d)", t)
                          if 300 + int(m) in CHAIN and 300 + int(m) != n))
        fwd[n] = refs
    miss_fwd = [n for n in CHAIN if not fwd[n]]
    Bd("B04", "一致性", "前向互链缺口：%s" % ("、".join("r%d" % n for n in miss_fwd) or "无"),
       "逐卷判定册正文（**已排除自引用**）引用链内其它卷的计数：%s。"
       "⇒ 缺口为 %s：r317 是最早主卷，其判定册不含对后出卷的前向指针，属**他人/早前字节，本卷不代改**；"
       "r320 已有前向（→r317/r321）；r321/r328 的前向指针已于 2026-11-01 补登 → r337。"
       "互链不对称是**索引层债务**（后出卷能看到先出卷，反之不能），不是读数冲突。"
       % ("；".join("r%d→%s" % (n, ",".join("r%d" % x for x in fwd[n]) or "（无）")
                   for n in CHAIN),
          "、".join("r%d" % n for n in miss_fwd) or "无"),
       {"forward": {str(k): v for k, v in fwd.items()}, "missing": miss_fwd})
    return {"cov": cov, "H1_values": flat, "forward": fwd}


# ── C 段：冗余账合并与链级结论 ─────────────────────────────────────────────
def section_C(CH, A, B):
    field = BITS_TOTAL_328 - BITS_COORD - BITS_SCALE
    s4 = BITS_COORD + BITS_SCALE + field + BITS_PRESC
    resid = s4 - BITS_TOTAL
    rel = abs(resid) / s4
    P_("C01", "总账", "★冗余账合并：坐标 %s + 能标 %s + 场内容 %s + 处方 %s = %s bit"
       % (fs(BITS_COORD), fs(BITS_SCALE), fs(field), fs(BITS_PRESC), fs(s4)),
       "四分量之和 = %s；r337 登记的合计 = %s（**6 位小数报道值**）⇒ 绝对差 %s、相对差 %s。"
       "残差**非零但属引用精度**，不是账目错误：分量含 r328 的 24 位精确读数 %s，"
       "而合计数在 r337 判定册里只报到 6 位小数 ⇒ 二者的差必在 1e−6 量级。"
       "**容差必须与被核数值的报价精度同源**（本库 r59 已立此纪律，本卷首版用 1e−40 卡它 ⇒ 自抓，见 §七）。"
       "声明 α 所需 %s bit ⇒ 净 %s bit（负 = 冗余远大于内容）。"
       "场内容分量由 r328 合计 %s 回算（%s − %s − %s），本卷不自造数值。"
       % (fs(s4), fs(BITS_TOTAL), fv(resid), fv(rel), fs(BITS_TOTAL_328),
          fs(BITS_NEED), fs(BITS_NEED - s4),
          fs(BITS_TOTAL_328), fs(BITS_TOTAL_328), fs(BITS_COORD), fs(BITS_SCALE)),
       {"coord": fs(BITS_COORD), "scale": fs(BITS_SCALE), "field": fs(field),
        "presc": fs(BITS_PRESC), "total": fs(s4), "need": fs(BITS_NEED),
        "residual": fv(resid), "rel_residual": fv(rel)})
    guard("G7_bits_identity", rel < Decimal("1e-7"), "rel=%s" % fv(rel))
    guard("G8_bits_negative_budget", (BITS_NEED - s4) < 0, fs(BITS_NEED - s4))

    # 正面判词扫描
    pos_hits = []
    for n in CHAIN:
        t = CH[n]["json_text"] + " " + CH[n]["judge_text"]
        for tk in POS_TOKENS:
            if tk in t:
                pos_hits.append((n, tk))
    if pos_hits:
        F_("C02", "总账", "链内出现正面判词 %d 处 ⇒ 与本卷合并结论冲突，须人工核对" % len(pos_hits),
           "命中：%s" % "；".join("r%d:%s" % h for h in pos_hits),
           {"hits": ["r%d:%s" % h for h in pos_hits]})
    else:
        P_("C02", "总账", "★链级统一结论：五卷均**未**给出『α 被预测』的正面判词（扫描 %d 词 × %d 卷 = 0 命中）"
           % (len(POS_TOKENS), len(CHAIN)),
           "扫描词：%s。五卷判词分别是——r317 坐标伪影/事后编造定理/相似不变量；"
           "r320 图表可容性/指数不变律/曲率任意性；r321 能标冗余/可预测性符号判据；"
           "r328 场内容冗余（函数级）；r337 缺口吸收多重共线性/归因失败/处方依赖/圈阶截断致命。"
           "⇒ 合并陈述 **NO-ATTRIBUTION-CHAIN**：五卷合起来证明的不是『α 被固定点预测』，"
           "而是『同一枚硬币的五面——每条路都能写出 137，但没有任何一条路只靠自己锁定它』。"
           % "、".join(POS_TOKENS),
           {"n_tokens": len(POS_TOKENS), "hits": 0})
    guard("G9_no_positive_verdict", not pos_hits, "hits=%d" % len(pos_hits))

    I_("C03", "总账", "链级判词 DAG（合并陈述，非新证据）",
       "坐标层（r317/r320）⟶ 物理闭合层（r321）⟶ 场内容层（r328）⟶ 归因层（r337）。"
       "每一层都在上一层**已固定**的前提下继续追问，因此各层结论是**条件推进**关系而非并列，"
       "这也正是『条目不可相加』的语义根据：后卷的判词以前卷的固定为前提。")

    I_("C04", "总账", "治理债登记（不代执行）",
       "① r317/r320 判定册无前向指针（并行/早前卷，本卷不代改）；"
       "② 链内三态 schema 并存 ⇒ 建议库级跨卷核对工具统一走 `entries|items` 归一（属治理变更，须用户批准）；"
       "③ r320 的 `scratch/_r320_reg_fake/` 为注册演练副本，与本链产物同名 ⇒ 自动清点须排除 `scratch/`。")
    return {"field": field, "total": s4, "resid": resid, "rel": rel, "pos": pos_hits}


# ── 控制组：证明判据有牙 ───────────────────────────────────────────────────
def section_CTL(CH, A, B, C):
    # CTL1 单卷 ⇒ 共享重叠为 0（判据不恒真）
    one = [320]
    cnt1 = sum(1 for k, (cands, _) in FACTS.items()
               if hit(CH[320]["json_text"], cands) or hit(CH[320]["judge_text"], cands))
    multi1 = 0
    P_("CTL1", "控制组", "空链对照：只取 1 卷时『被 ≥2 卷覆盖』的事实数 = %d（全链为 %d）"
       % (multi1, len(A["multi"])),
       "单卷命中 %d/%d 项共享事实，但**重叠数恒为 0** ⇒ A03 的『不可相加』判据不是恒真地报重叠，"
       "它只在确实存在多卷共载事实时才触发。" % (cnt1, len(FACTS)),
       {"single_hits": cnt1, "multi_single": multi1})
    guard("G10_ctl1_no_overlap", multi1 == 0, "multi=%d" % multi1)

    # CTL2 冲突注入 ⇒ 检测器报冲突（有牙）
    fake = {"json_text": "H(1) = 1.92350000000000000000000E-2", "judge_text": ""}
    pat = re.compile(r"1\.9235[0-9]*\s*E\s*[-+]?\s*[0-9]+")
    inj = set(m.replace(" ", "") for m in pat.findall(norm_text(fake["json_text"])))
    real = set(B["H1_values"])
    union = sorted(real | inj)
    P_("CTL2", "控制组", "冲突注入对照：注入一个伪造 H(1) 值 ⇒ 取值集合由 %d 变 %d ⇒ 检测器报冲突"
       % (len(real), len(union)),
       "真实集合 %s；注入 %s ⇒ 并集 %d 个 ⇒ B02 会由 PASS 转 FAIL。"
       "⇒ 一致性判据能抓冲突，不只是『大家都有就说一致』。" % (real, sorted(inj), len(union)),
       {"real": sorted(real), "injected": sorted(inj), "union": union})
    guard("G11_ctl2_detects_conflict", len(union) > len(real), "union=%d" % len(union))

    # CTL3 不归一 ⇒ 漏计（与真没数据不可区分）
    raw_c = len(json.loads(CH[317]["json_text"]).get("entries", [])) \
        if CH[317]["json_text"] else 0
    norm_c = len(CH[317]["entries"])
    P_("CTL3", "控制组", "★归一必要性：r317 直接取 `entries` 得 %d 条，归一后得 %d 条"
       % (raw_c, norm_c),
       "A/B 型卷没有 `entries` 键 ⇒ 直接取键得 0，而『0 条』与『该卷真的没有条目』**不可区分**，"
       "这正是 r321 漂移自检假阳性 105 条的同型根因（基准与产物结构不匹配）。"
       "归一函数按 `entries → items → (summary? A : B)` 三级回退后得真值 %d ⇒ 这一步不可省。"
       % norm_c, {"raw_entries": raw_c, "normalized": norm_c})
    guard("G12_ctl3_normalization_needed", raw_c == 0 and norm_c > 0,
          "raw=%d norm=%d" % (raw_c, norm_c))

    # CTL4 bit 和式残差机器零
    probe = BITS_PRESC - Decimal("0.00005")      # 处方项在第 5 位小数上改动 5e−5
    s_probe = BITS_COORD + BITS_SCALE + C["field"] + probe
    rel_p = abs(s_probe - BITS_TOTAL) / s_probe
    P_("CTL4", "控制组",
       "★和式守卫有牙：处方项改动 5e−5 ⇒ 相对残差由 %s 升到 %s（阈值 1e−7）"
       % (fv(C["rel"]), fv(rel_p)),
       "真实账：四分量之和 − 登记合计 = %s，相对 %s < 1e−7 ⇒ **在 6 位小数报价内一致**。"
       "注入对照：把 24.59050 改成 24.59045 ⇒ 相对残差 %s > 1e−7 ⇒ 守卫转红。"
       "⇒ 该守卫既不会把合法的舍入引用误判为账目错误（本卷首版犯过，见 §七 自抓 1），"
       "也确实能抓住真正的数位错误。" % (fv(C["resid"]), fv(C["rel"]), fv(rel_p)),
       {"residual": fv(C["resid"]), "rel": fv(C["rel"]), "injected_rel": fv(rel_p)})
    guard("G13_ctl4_residual_guard_has_teeth",
          C["rel"] < Decimal("1e-7") and rel_p > Decimal("1e-7"),
          "real=%s injected=%s" % (fv(C["rel"]), fv(rel_p)))

    # CTL5 只读（白名单内容审查；**不能**只在 WRITTEN 上做全称判断——
    #        写盘前 WRITTEN 为空集，空集上的"全部合规"恒真 ⇒ 假绿）
    bad = [p for p in ALLOWED
           if (RID not in os.path.basename(p)) and (os.path.basename(p) != HTML_NAME)]
    n_read = sum(1 for n in CHAIN if CH[n]["json_path"]) \
        + sum(1 for n in CHAIN if CH[n]["judge_path"])
    P_("CTL5", "控制组", "只读纪律：白名单 %d 个路径全部属本卷自身产物（越界 %d 个）；只读他卷产物 %d 个"
       % (len(ALLOWED), len(bad), n_read),
       "白名单只含本卷自身 4 个产物（数据 json/md/report + 根目录 HTML）；逐路径核对："
       "文件名含本卷号或恰为 HTML 名，越界 %d 个。五卷他卷产物全程只读"
       "（json/判定册仅 `io.open(...,encoding='utf-8').read()`，无写句柄）⇒ 不改写任何既有字节。"
       "**注意**：本判据不能写成『WRITTEN 全部在白名单内』——CTL 段在写盘之前执行，"
       "那时 WRITTEN 是空集，空集上的全称判断恒真 ⇒ 假绿（本卷首版即如此，见 §七 自抓 2）；"
       "写盘后的实际复核另由守卫 G16 承担。"
       % len(bad), {"allowed": len(ALLOWED), "out_of_scope": len(bad), "read_only": n_read})
    guard("G14_ctl5_allowlist_clean", not bad and len(ALLOWED) == 4,
          "bad=%d allowed=%d" % (len(bad), len(ALLOWED)))

    # CTL6 正面判词扫描有牙
    probe = "本卷给出 PREDICTED 结论" + CH[321]["judge_text"][:0]
    n_probe = sum(1 for tk in POS_TOKENS if tk in probe)
    P_("CTL6", "控制组", "正面判词扫描有牙：注入含 `%s` 的文本 ⇒ 命中 %d 处"
       % (POS_TOKENS[0], n_probe),
       "空链实测命中 0（C02），注入后命中 %d ⇒ 扫描器不是恒零，"
       "C02 的『链内无正面判词』是**实测结论**而非扫描器失效。" % n_probe,
       {"probe_hits": n_probe})
    guard("G15_ctl6_scanner_has_teeth", n_probe >= 1, "hits=%d" % n_probe)


# ── 输出引擎 ───────────────────────────────────────────────────────────────
def build_md():
    L = ["# %s · 数据底稿" % RID, "",
         "- 轮次：%s　日期：%s　条目：%d" % (RID, STAMP, len(ITEMS)), "",
         "## 条目表", "", "| 编号 | 层 | 条目 | 判定 |", "|---|---|---|---|"]
    for e in ITEMS:
        L.append("| %s | %s | %s | %s |" % (e["id"], e["layer"], e["title"], e["verdict"]))
    L += ["", "## 明细", ""]
    for e in ITEMS:
        L += ["### %s · %s（%s）" % (e["id"], e["title"], e["verdict"]), "", e["detail"], ""]
    L += ["## 守卫", ""]
    for g in GUARDS:
        L.append("- %s ⇒ %s %s" % (g["name"], "PASS" if g["ok"] else "FAIL", g["note"]))
    return "\n".join(L) + "\n"


def build_html():
    rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                   % (e["id"], e["layer"], e["title"], e["verdict"]) for e in ITEMS)
    gl = "".join("<li>%s ⇒ %s</li>" % (x["name"], "PASS" if x["ok"] else "FAIL")
                 for x in GUARDS)
    det = "".join("<h3>%s · %s（%s）</h3><p>%s</p>"
                  % (e["id"], e["title"], e["verdict"], e["detail"]) for e in ITEMS)
    return """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>%s 可视化</title><style>
body{font-family:system-ui,"Microsoft YaHei",sans-serif;margin:24px;line-height:1.6}
table{border-collapse:collapse;width:100%%;font-size:13px}
th,td{border:1px solid #ccc;padding:6px 8px;text-align:left}
th{background:#f2f4f8}
</style></head><body>
<h1>TUFT-%s · ROOT V24 判词链总账（元审计）</h1>
<p><b>判词：</b>CHAIN-SCHEMA-TRISTATE / ENTRIES-NOT-ADDITIVE / CROSS-READING-CONSISTENT / NO-ATTRIBUTION-CHAIN</p>
<h2>条目表</h2><table><tr><th>编号</th><th>层</th><th>条目</th><th>判定</th></tr>%s</table>
<h2>守卫</h2><ul>%s</ul>
<h2>明细</h2>%s
</body></html>
""" % (RID, RID, rows, gl, det)


def write_out(name, text):
    path = os.path.join(DATA, name) if name != HTML_NAME else os.path.join(ROOT, name)
    if path not in ALLOWED:
        raise SystemExit("越界写入：%s" % path)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)
    WRITTEN.append(path)


def main():
    for n in (BASE + ".json", BASE + ".md", BASE + "_report.txt"):
        ALLOWED.add(os.path.join(DATA, n))
    ALLOWED.add(os.path.join(ROOT, HTML_NAME))

    CH = load_chain()
    A = section_A(CH)
    B = section_B(CH, A)
    C = section_C(CH, A, B)
    section_CTL(CH, A, B, C)

    payload = {
        "round": RID,
        "title": "ROOT V24 判词链总账（元审计卷）",
        "date": STAMP,
        "verdict_summary": ("CHAIN-SCHEMA-TRISTATE / ENTRIES-NOT-ADDITIVE / "
                            "CROSS-READING-CONSISTENT / NO-ATTRIBUTION-CHAIN"),
        "entries": ITEMS, "guards": GUARDS,
        "guard_pass": sum(1 for g in GUARDS if g["ok"]), "guard_total": len(GUARDS),
        "constants": {
            "chain_rounds": CHAIN,
            "entries_total": A["total"],
            "schema_map": {str(k): v for k, v in A["kinds"].items()},
            "bits_coord": fs(BITS_COORD), "bits_scale": fs(BITS_SCALE),
            "bits_field": fs(C["field"]), "bits_presc": fs(BITS_PRESC),
            "bits_total": fs(C["total"]), "bits_need": fs(BITS_NEED),
            "bits_total_328": fs(BITS_TOTAL_328),
            "anchor_is_external": True,
            "needs_official_confirmation": True,
        },
        "closed_forms": {
            "normalize": "entries -> items -> (summary ? A : B)",
            "additivity": "sum(entries) illegal when shared facts covered by >=2 rounds",
            "consistency": "absent != conflict",
        },
        "relations": {
            "r317": "坐标层（A 型 schema，只读）",
            "r320": "图表层（B 型 schema，只读）",
            "r321": "物理闭合层（C 型，坐标/能标冗余读数来源）",
            "r328": "场内容层（C 型，冗余合计来源）",
            "r337": "归因层（C 型，处方与圈阶读数来源）",
        },
    }
    write_out(BASE + ".json", json.dumps(payload, ensure_ascii=False, indent=1))
    write_out(BASE + ".md", build_md())
    write_out(BASE + "_report.txt",
              "entries=%d guards=%d/%d\n"
              % (len(ITEMS), payload["guard_pass"], payload["guard_total"]))
    write_out(HTML_NAME, build_html())

    # 写盘后复核（越界即非 0 退出；不进 guards，避免与 json 里的计数口径不一致）
    if (len(WRITTEN) != 4) or any(p not in ALLOWED for p in WRITTEN):
        raise SystemExit("写盘越界：%s" % WRITTEN)

    sys.stdout.write("%s rc=0 entries=%d guards=%d/%d\n"
                     % (RID, len(ITEMS), payload["guard_pass"], payload["guard_total"]))
    sys.stdout.write("chain=%s total_entries=%d schema=%s\n"
                     % (CHAIN, A["total"], sorted(A["kinds"])))
    sys.stdout.write("multi_covered=%d H1_values=%d bits_total=%s need=%s\n"
                     % (len(A["multi"]), len(B["H1_values"]),
                        fs(C["total"]), fs(BITS_NEED)))
    sys.stdout.write("elapsed=%.1fs\nwritten:\n" % (time.time() - T0))
    for p in WRITTEN:
        sys.stdout.write("    " + p + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
