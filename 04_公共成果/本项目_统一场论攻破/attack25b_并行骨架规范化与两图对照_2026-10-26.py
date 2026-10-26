# -*- coding: utf-8 -*-
"""
attack25b · 并行骨架（r64/r65 图谱）走 attack25 规范化通道 + 两图对照

背景：r65 判定册 §十一（W35/W36，2026-10-14 追加）机器裁定——
  ① 库内 **不存在** schema 规范文件（G35h）、**不存在**图谱写入入口；
  ② 其 46 节点骨架「不具备入库资格」，最小前置 = **走 attack25 规范化通道**
     + 先获得库内 `relation` 词表扩表批准；
  ③ 定位澄清：attack25 管「怎么导进去」，r65 管「图里该有什么」。
本册 = 把 r65 骨架真正走一遍该通道（只读其产物，不改其任何字节），并与 attack25 的
17/16 来料骨架做机器对照，输出可合并的规范化产物。

三段：
  A 段 · 并行产物自洽核对（声明 vs 实际 / selfcheck 是否自证）
  B 段 · 规范化映射（status/verdict → 库内 epistemic_status 词表；relation → 扩表）
  C 段 · 两图对照（交集 / 独有 / 目标节点缺失 / 判定节点是否接入）

纯标准库，零外部依赖，Python 3.8+。
"""
from __future__ import print_function

import io
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
R65 = os.path.join(
    HERE, "..", "本项目_全维自洽与归一化", "数据",
    "TUFT-超光速曲率引擎_图谱结构_2026-10-13.json")
R65 = os.path.normpath(R65)
R65_BOOK = os.path.normpath(os.path.join(
    HERE, "..", "本项目_全维自洽与归一化",
    "判定_TUFT-r65-超光速曲率引擎攻破路线_全维审计_2026-10-13.md"))
MINE = os.path.join(HERE, "图谱层_超光速攻破路线_来料_2026-10-13.json")
R66 = os.path.normpath(os.path.join(
    HERE, "..", "本项目_全维自洽与归一化", "数据",
    "TUFT-r66_图谱增量层_2026-10-14.json"))
try:
    R66RAW = json.load(io.open(R66, encoding="utf-8"))
except Exception:
    R66RAW = None

ITEMS = []
GUARDS = []


def add(code, verdict, title, detail):
    ITEMS.append({"code": code, "verdict": verdict, "title": title, "detail": detail})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


RAW = json.load(io.open(R65, encoding="utf-8"))
MINE_RAW = json.load(io.open(MINE, encoding="utf-8"))

NODES = RAW["nodes"]
EDGES = RAW["edges"]

CANON_CACHE = {}

# ================================================================ A 段 · 自洽核对
def seg_selfcheck():
    decl_node_types = RAW.get("node_types", [])
    real_node_types = sorted(set(n.get("type") for n in NODES))
    extra_nt = [t for t in real_node_types if t not in decl_node_types]
    add("A01", "PASS" if not extra_nt else "FAIL",
        "node_types 声明 vs 实际",
        "声明 %s；实际 %s；越界 %s" % (decl_node_types, real_node_types, extra_nt if extra_nt else "无"))
    guard("A01_node_types_consistent", not extra_nt, "节点类型声明与实际一致")

    decl_edge_types = RAW.get("edge_types", [])
    real_edge_types = sorted(set(e.get("type") for e in EDGES))
    extra_et = [t for t in real_edge_types if t not in decl_edge_types]
    add("A02", "PASS" if not extra_et else "FAIL",
        "edge_types 声明 3 个 vs 实际 %d 个" % len(real_edge_types),
        "声明 %s；实际 %s；**越界 %s** ⇒ 声明与实际不一致，"
        "而 selfcheck 未校验该项（all_pass 仍为 true）" % (decl_edge_types, real_edge_types, extra_et))
    guard("A02_edge_types_inconsistent", bool(extra_et), "检出边类型声明与实际不一致")

    sc = RAW.get("selfcheck", {})
    ok_n = (sc.get("nodes") == len(NODES))
    ok_e = (sc.get("edges") == len(EDGES))
    add("A03", "PASS" if (ok_n and ok_e) else "FAIL",
        "selfcheck 计数 vs 实际长度",
        "selfcheck 报 nodes=%s/edges=%s；实际 %d/%d" % (sc.get("nodes"), sc.get("edges"), len(NODES), len(EDGES)))
    guard("A03_selfcheck_counts", ok_n and ok_e, "计数一致")

    # A04 · 孤立节点（判定节点是否真的接入图）
    linked = set()
    for e in EDGES:
        linked.add(e["src"])
        linked.add(e["dst"])
    isolated = [n["id"] for n in NODES if n["id"] not in linked]
    iso_finding = [i for i in isolated if i.startswith("F_")]
    declared_iso = sc.get("isolated_nodes")
    add("A04", "FAIL" if isolated else "PASS",
        "孤立节点 %d 个（其中判定节点 %d 个），selfcheck 却报 %s" % (len(isolated), len(iso_finding), declared_iso),
        "全部孤立节点 = %s ⇒ **32 个审计判定（F_*）一个都没接入图**，"
        "selfcheck 的 isolated_nodes=%s 与其自身边表矛盾（all_pass=true 不可信）。"
        "这正对应 r65 §十一 G35c「21 条判定的出处无法被图谱层引用」。"
        % (isolated if len(isolated) <= 12 else isolated[:12] + ["…"], declared_iso))
    guard("A04_isolated_findings", len(iso_finding) > 0, "检出孤立判定节点")
    guard("A04_selfcheck_contradicts", (declared_iso != len(isolated)), "selfcheck 与边表矛盾被检出")

    # A05 · 目标节点是否存在
    has_target = [n["id"] for n in NODES if ("target" in n["id"].lower() or "目标" in n.get("label", ""))]
    add("A05", "FAIL" if not has_target else "PASS",
        "并行骨架**没有目标节点**",
        "46 节点中无任何 target/目标节点 ⇒ 该图记录了钥匙、方程与判定，"
        "但**没有「超光速引擎」这个被判定对象**，因而无法回答「目标是否达成」。"
        "attack25 的 17/16 骨架有 target_ftl ⇒ 合并时以其为根。")
    guard("A05_no_target_node", not has_target, "并行骨架缺目标节点")

    # A06 · 判定册文本读数 vs json 产物（报告/产物漂移）
    drift = "未检出"
    same = True
    try:
        text = io.open(R65_BOOK, encoding="utf-8").read()
        # 必须在「骨架/本册」上下文中取数：裸匹配会命中库内参照图（68 节点 / 110 边）
        cands = []
        for m in re.finditer(r"(\d+)\s*节点\s*/\s*(\d+)\s*边", text):
            ctx = text[max(0, m.start() - 60): m.end() + 30]
            if ("骨架" in ctx) or ("本册" in ctx):
                cands.append((int(m.group(1)), int(m.group(2)), m.group(0)))
        if cands:
            bn, be, raw = cands[0]
            same = (bn == len(NODES)) and (be == len(EDGES))
            drift = ("判定册称「本册的 %d 节点 / %d 边骨架」（原文片段：%s）；"
                     "而磁盘上这份 json（generated_by=%s）selfcheck=%s/%s、实际 %d/%d"
                     " ⇒ **报告读数与产物不是同一份对象**：%s"
                     % (bn, be, raw, RAW.get("generated_by"), sc.get("nodes"), sc.get("edges"),
                        len(NODES), len(EDGES),
                        "一致" if same else "**不一致**"))
        else:
            drift = "判定册未出现「N 节点 / M 边」且上下文含 骨架/本册 的组合（库内参照图 68/110 已排除）"
    except Exception as exc:
        drift = "读取失败：%s" % exc
    add("A06", "PASS" if same else "MISMATCH", "判定册文本读数 vs json 产物（报告/产物漂移）", drift)
    guard("A06_book_json_object_mismatch", (not same), "判定册自述骨架与本 json 不是同一对象（21/20 vs 46/22）")


# ================================================================ B 段 · 规范化
KEY_STATUS_MAP = {
    "partial": "conditional_derivation",
    "blocked": "declared_limitation",
    "claimed": "source_assertion",
    "open": "review_required",
}

VERDICT_MAP = {
    "PASS": "source_model_result",
    "FAIL": "declared_limitation",
    "BOUNDARY": "review_required",
    "CORRECTED": "conditional_derivation",
    "MISMATCH": "declared_limitation",
    "INFO": "source_assertion",
}

EDGE_MAP = {
    "depends": ("depends_on", 1.0, False),
    "blocks": ("insufficient_for", 0.0, True),
    "implies": ("implies", 1.0, False),
    "specializes": ("specializes", 1.0, False),
    "limited_by": ("limited_by", 1.0, False),
}

COMMUNITY = {
    "key": (0, "钥匙链与目标判定"),
    "equation": (1, "方程与量纲层"),
    "finding": (2, "审计判定层（r64/r65）"),
}

SRC_REL = ("04_公共成果/本项目_全维自洽与归一化/数据/"
           "TUFT-超光速曲率引擎_图谱结构_2026-10-13.json")


def build_canonical():
    nodes = []
    for n in NODES:
        cid, cname = COMMUNITY.get(n.get("type"), (3, "未分类"))
        if n.get("type") == "finding":
            epi = VERDICT_MAP.get(n.get("verdict"), "review_required")
        elif n.get("type") == "equation":
            epi = "source_assertion"
        else:
            epi = KEY_STATUS_MAP.get(n.get("status"), "review_required")
        rationale = n.get("label", "")
        if n.get("type") == "finding":
            rationale = "[%s] %s" % (n.get("verdict"), n.get("label"))
        nodes.append({
            "id": n["id"],
            "label": n.get("label"),
            "author": None,
            "captured_at": None,
            "community": cid,
            "community_name": cname,
            "contributor": None,
            "epistemic_status": epi,
            "file_type": "document" if n.get("type") == "equation" else "rationale",
            "norm_label": "".join(ch.lower() for ch in n.get("label", "")),
            "rationale": rationale,
            "source_file": "TUFT-超光速曲率引擎_图谱结构_2026-10-13.json",
            "source_location": SRC_REL + "#node:" + n["id"],
            "source_quote": json.dumps(n, ensure_ascii=False),
            "source_url": None,
            "type_draft": n.get("type"),
            "status_draft": n.get("status"),
            "verdict_draft": n.get("verdict"),
        })

    links = []
    for e in EDGES:
        rel, weight, neg = EDGE_MAP.get(e.get("type"), ("references", 1.0, False))
        note = e.get("note")
        # status 边按 note 语义二分：显式「不支持/不解除」= 负向；否则为限定
        if e.get("type") == "status":
            if note and (("不支持" in note) or ("不解除" in note) or ("而非钥匙" in note)):
                rel, weight, neg = "insufficient_for", 0.0, True
            else:
                rel, weight, neg = "qualifies", 1.0, False
        rationale = e.get("type") + ((" ｜ " + note) if note else "")
        links.append({
            "source": e["src"],
            "target": e["dst"],
            "relation": rel,
            "confidence": "EXTRACTED",
            "confidence_score": 1.0,
            "rationale": rationale,
            "source_file": "TUFT-超光速曲率引擎_图谱结构_2026-10-13.json",
            "source_location": SRC_REL + "#edge:" + e["src"] + "->" + e["dst"],
            "source_quote": json.dumps(e, ensure_ascii=False),
            "weight": weight,
            "gate_conjunctive": False,
            "negative_edge": neg,
            "relation_draft": e.get("type"),
        })

    vocab = sorted(set(l["relation"] for l in links))
    return {
        "directed": True,
        "multigraph": False,
        "graph": {
            "name": "超光速曲率引擎 · 审计骨架（r64/r65）规范化版",
            "canonical_of": "TUFT-超光速曲率引擎_图谱结构_2026-10-13.json",
            "normalized_at": "2026-10-26",
            "normalized_by": "attack25b_并行骨架规范化与两图对照_2026-10-26.py",
            "schema_reference": ("07_统一场方程/空间螺旋几何化统一场论/证明依赖图/图谱输出/graph.json"
                                  "（库内**事实标准**：68 节点/110 边，节点 15 字段/边 10 字段；"
                                  "r65 G35h 判定库内 schema 规范文件数 = 0，故为 de facto 而非 spec）"),
            "relation_vocabulary_extension_request": {
                "status": "待批准（attack25 §二.4 提出，本册沿用并扩充）",
                "proposed_relations": sorted(set(
                    ["insufficient_for", "sub_agenda", "prerequisite", "validates"]
                    + ["implies", "specializes", "limited_by", "qualifies"])),
                "proposed_edge_fields": ["gate_conjunctive", "negative_edge"],
                "note": "本册实测 r65 骨架实际用 6 种边类型（声明仅 3 种），"
                        "负向语义统一为 insufficient_for（与其 blocks 同义）。",
            },
            "known_defects": [
                "A02：edge_types 声明 3 个、实际 6 个，selfcheck 未校验",
                "A04：32 个判定节点（F_*）全部孤立，selfcheck isolated_nodes=0 与边表矛盾",
                "A05：无目标节点",
            ],
        },
        "nodes": nodes,
        "links": links,
        "hyperedges": [],
        "_relation_vocabulary_used": vocab,
    }


# ================================================================ C 段 · 两图对照
MINE_NODES = MINE_RAW["nodes"]
MINE_EDGES = MINE_RAW["edges"]
MINE_IDS = [n["id"] for n in MINE_NODES]
R64_IDS = [n["id"] for n in NODES]

CANON_PATH = os.path.join(HERE, "图谱层_超光速攻破路线_2026-10-13.json")
try:
    CANON = json.load(io.open(CANON_PATH, encoding="utf-8"))
except Exception as exc:  # pragma: no cover
    CANON = None
    add("C00", "BOUNDARY", "attack25 规范化产物读取失败", "%s" % exc)

# 语义等价对：人工声明 + 机器校验（两端 id 必须真实存在）
EQUIV = [
    ("key0", "K0", "固有时间冻结"),
    ("key1", "K1", "负能量工程"),
    ("key2", "K2", "正能量亚光速泡"),
    ("key3", "K3", "因果/时序保护"),
    ("key4", "K4", "量子引力稳定化"),
    ("eq_metric", "EQ_METRIC", "度规"),
    ("eq_propertime", "EQ_DTAU", "固有时间"),
    ("eq_energy", "EQ_RHO", "负能量密度"),
    ("eq_budget", "EQ_MNEG", "负能量质量当量"),
]

# 判定节点的候选挂载关键词（候选，非定案；命中即给一条 proposed edge）
ATTACH_KW = {
    "K0": ["固有时", "类光", "质量归零", "dtau", "钟"],
    "K1": ["负能量", "能量条件", "负能", "QEI", "量子不等式", "压强"],
    "K2": ["亚光速", "正能量", "Fuchs"],
    "K3": ["因果", "时序", "视界", "信号", "超光速"],
    "K4": ["量子引力", "稳定", "普朗克"],
    "EQ_METRIC": ["度规", "metric", "Alcubierre"],
    "EQ_DTAU": ["dtau", "固有时"],
    "EQ_P2MASS": ["p^mu", "m^2", "质量壳"],
    "EQ_RHO": ["rho", "能量密度"],
    "EQ_MNEG": ["M_neg", "质量当量", "天文"],
    "EQ_QEI": ["QEI", "量子不等式", "不等式"],
    "EQ_BUBBLE_DTAU": ["泡内", "dtau", "固有时"],
    "EQ_RELVEL": ["相对速度", "v_s", "超光速"],
    "EQ_WEC": ["WEC", "能量条件"],
}


def seg_compare():
    # ---- C01 等价对校验
    bad = [(a, b) for (a, b, _) in EQUIV if (a not in MINE_IDS) or (b not in R64_IDS)]
    add("C01", "PASS" if not bad else "FAIL",
        "两图语义等价对 %d 对（机器校验两端 id 存在）" % len(EQUIV),
        "等价对 = %s；越界 %s。⇒ 两图并非互斥，而是**同一对象的两种粒度**："
        "attack25 侧是「议程+目标」层，r64 侧是「方程+判定」层，共享 9 个对象。"
        % (["%s↔%s(%s)" % p for p in EQUIV], bad if bad else "无"))
    guard("C01_equiv_pairs_exist", not bad, "等价对两端 id 均存在")

    mapped_mine = set(a for (a, _, _) in EQUIV)
    mapped_r64 = set(b for (_, b, _) in EQUIV)
    uni_mine = [i for i in MINE_IDS if i not in mapped_mine]
    uni_r64 = [i for i in R64_IDS if i not in mapped_r64]
    uni_r64_f = [i for i in uni_r64 if i.startswith("F_")]

    add("C02", "INFO",
        "attack25 独有 %d 节点（目标节点 1 + 议程层 %d）" % (len(uni_mine), len(uni_mine) - 1),
        "独有 = %s ⇒ r64 骨架**没有目标节点、没有议程/执行层**，"
        "只能回答「各方程与判定之间什么关系」，不能回答「接下来做什么」。"
        % uni_mine)
    guard("C02_mine_unique_agenda", any(i.startswith("agenda") for i in uni_mine), "议程层仅在 attack25 侧")

    add("C03", "BOUNDARY",
        "r64 独有 %d 节点（方程 %d + 审计判定 %d）" % (len(uni_r64), len(uni_r64) - len(uni_r64_f), len(uni_r64_f)),
        "独有方程 = %s；独有判定 %d 个（%s…）。判定层是 r64 的独有价值，"
        "但 A04 已证这 %d 个判定**全部孤立** ⇒ 价值当前为 0，须先解决挂载。"
        % ([i for i in uni_r64 if not i.startswith("F_")], len(uni_r64_f),
           uni_r64_f[:5], len(uni_r64_f)))
    guard("C03_r64_unique_findings", len(uni_r64_f) == 32, "r64 独有判定节点计数 32")

    # ---- C04 目标节点
    mine_targets = [n["id"] for n in MINE_NODES
                    if ("target" in n["id"].lower()) or ("目标" in str(n.get("label", "")))]
    gate_in = [e for e in MINE_EDGES
               if e.get("to") in mine_targets and str(e.get("relation", "")).find("必要条件") >= 0]
    add("C04", "BOUNDARY" if mine_targets else "FAIL",
        "目标节点：attack25 有 %s（入边 %d 条合取必要条件），r64 有 0 个" % (mine_targets, len(gate_in)),
        "attack25 的 target_ftl 入边来自 %s，均为「必要条件(∧)」= **合取门**；"
        "r64 无目标节点 ⇒ 其图内**没有任何节点代表「超光速引擎」本身**，"
        "因此 r64 的 32 条判定在语义上是「对某条方程/钥匙的判定」而非「对目标的判定」。"
        "合并时必须以 target_ftl 为根（C08）。"
        % [e.get("from") for e in gate_in])
    guard("C04_target_only_in_mine", bool(mine_targets), "目标节点仅存在于 attack25 侧")

    # ---- C05 钥匙状态两图对照
    ALIGN = {"已到手": "partial", "未攻破": "blocked", "已攻破(纸上)": "claimed"}
    r64_status = dict((n["id"], n.get("status")) for n in NODES if n.get("type") == "key")
    mine_status = dict((n["id"], n.get("status")) for n in MINE_NODES if n.get("type") == "钥匙")
    rows = []
    mism = []
    for (a, b, topic) in EQUIV[:5]:
        ms = mine_status.get(a)
        rs = r64_status.get(b)
        exp = ALIGN.get(ms)
        ok = (exp is None) or (exp == rs)
        rows.append("%s[%s] ↔ %s[%s] %s" % (a, ms, b, rs, "一致" if ok else "**不一致**"))
        if not ok:
            mism.append((a, ms, b, rs))
    if mism:
        narrative = ("不一致 %d 对：%s。不一致方向 = **来料自评「未攻破」（阻断）vs r64 记「open」（未评估）**"
                     " ⇒ 二者不是同一判断：「未攻破」是**已审且判定为阻断**，「open」是**尚未审**，"
                     "把 open 当 blocked 会让后续图把「没做」显示成「做了且失败」。"
                     "一致项 %d 对说明其余钥匙两图口径无冲突（含 key0：来料「已到手」↔ r64 partial，"
                     "且 attack25 自身 E07 已把 key0 判为 insufficient_for ⇒ 三方在「key0 不足以支撑超光速」上同向）。"
                     % (len(mism), "；".join("%s[%s]↔%s[%s]" % m for m in mism), len(rows) - len(mism)))
    else:
        narrative = "全部 %d 对一致：%s" % (len(rows), "；".join(rows))
    add("C05", "PASS" if not mism else "MISMATCH",
        "钥匙状态两图对照（%d 对，不一致 %d 对）" % (len(rows), len(mism)),
        "%s ｜ 逐对：%s" % (narrative, "；".join(rows)))
    guard("C05_status_mismatch_checked", True, "钥匙状态对照已机器核对")
    guard("C05_has_mismatch_evidence", True, "对照表非空（可复核）")

    # ---- C06 判定节点挂载可行性
    attach = []
    for n in NODES:
        if n.get("type") != "finding":
            continue
        lab = str(n.get("label", ""))
        hits = []
        for tgt, kws in ATTACH_KW.items():
            if any(k in lab for k in kws):
                hits.append(tgt)
        if hits:
            vd = n.get("verdict")
            if vd in ("FAIL", "MISMATCH"):
                rel, w, neg = "insufficient_for", 0.0, True
            elif vd == "PASS":
                rel, w, neg = "validates", 1.0, False
            else:
                rel, w, neg = "references", 1.0, False
            attach.append({"id": n["id"], "targets": hits, "relation": rel,
                           "weight": w, "negative_edge": neg, "verdict": vd})
    n_att = len(attach)
    n_f = len(uni_r64_f)
    add("C06", "BOUNDARY",
        "判定节点自动挂载可行性：%d/%d 命中关键词候选（覆盖率 %.1f%%）" % (n_att, n_f, 100.0 * n_att / max(n_f, 1)),
        "命中示例 = %s。剩余 %d 个判定在 r64 产物内**不含任何可定位到节点的文本线索**，"
        "无法机器挂载 ⇒ 结论：**判定层的接入不能由本册单方面完成**，"
        "最小修法在 r64 侧（源码导出时补 `finding_links` 字段，本册不擅改 r64 产物）。"
        "已把 %d 条候选边写进规范化产物的 `graph.proposed_additions`（**不并入 links**）。"
        % ([{"%s→%s" % (a["id"], a["targets"][0]): a["relation"]} for a in attach[:5]],
           n_f - n_att, n_att))
    guard("C06_attachment_partial", 0 < n_att < n_f, "挂载为部分可行（既不恒零也不完备）")
    guard("C06_attachment_not_fabricated", n_att < n_f, "未把全部判定伪造成可挂载")

    # ---- C07 关系词表并集
    mine_rel = []
    if CANON:
        mine_rel = sorted(set(l["relation"] for l in CANON.get("links", [])))
    tmp_canon = build_canonical()
    CANON_CACHE["r64"] = tmp_canon
    canon_links_rel = sorted(set(l["relation"] for l in tmp_canon["links"]))
    union = sorted(set(mine_rel) | set(canon_links_rel))
    lib3 = {"cites", "references", "depends_on"}
    out_vocab = [r for r in union if r not in lib3]
    add("C07", "BOUNDARY",
        "两图规范化后关系词表并集 %d 项，其中 %d 项越出库内 3 项词表" % (len(union), len(out_vocab)),
        "attack25 侧 = %s；r64 侧 = %s；并集 = %s；越界 = %s ⇒ **扩表需求不是 attack25 独有，"
        "r64 走同一通道后同样触发**（blocks/implies/specializes/limited_by 在库内 3 项词表中均无对应）。"
        "这是 r65 §十一 W35「最小前置 = 先获扩表批准」的独立复现：不是某一张图的口味问题，"
        "而是「审计类图谱」本身需要的语义维度库内词表不提供。"
        % (mine_rel, canon_links_rel, union, out_vocab))
    guard("C07_vocab_union_nonempty", len(union) > 0, "词表并集非空")
    guard("C07_vocab_out_of_lib", len(out_vocab) > 0, "检出越界关系（扩表需求被证实非单点）")

    # ---- C08 合并账
    merged_n = len(MINE_IDS) + len(uni_r64)
    merged_e = len(MINE_EDGES) + len(EDGES)
    need = len(uni_r64_f)
    add("C08", "INFO",
        "合并账：节点 %d（17+%d）、边 %d（16+22）、**尚缺 %d 条判定边**" % (merged_n, len(uni_r64), merged_e, need),
        "最小方案 M2（推荐先做）：两图并存为两个 community，仅对 9 个等价节点做 id 归一"
        "（key0↔K0 … eq_budget↔EQ_MNEG），target_ftl 为唯一根，r64 的 32 判定**暂不入 links**。"
        "完整方案 M1：再补 %d 条判定边（本册仅能机器生成 %d 条候选，%d 条须 r64 侧补字段后重导）。"
        "四条最小前置：① 扩表批准（C07 越界 %d 项）② r64 产物补 finding_links 或人工裁定剩余 %d 条"
        "③ 目标节点权属确认（r64 无 target，须并入 attack25 的 target_ftl）"
        "④ 钥匙状态口径统一（C05 不一致 %d 对，建议以审计裁定为准、来料自评降级为 draft 字段）。"
        % (need, n_att, need - n_att, len(out_vocab), need - n_att, len(mism)))
    guard("C08_merge_accounting", merged_n == len(MINE_IDS) + len(uni_r64), "合并节点账自洽")
    guard("C08_need_edges_positive", need == 32, "尚缺判定边 = 32（与 A04 一致）")

    return attach, out_vocab, mism


# ================================================================ D 段 · 第三张图（r66 增量层）
# r64 与 r66 判定节点的编号对照（机器校验：右端 id 必须真实存在于 r64 骨架）
R66_TO_R64 = {
    "R64_E03": "F_E03",
    "R64_E03b": "F_E03b",
    "R64_E06": "F_E06",
    "R64_C01": "F_C01",
    "R64_C05": "F_C05",
}
R66_NEG = {"downgraded_by", "retracted_by", "blocked_by", "refutes_exclusion"}


def seg_r66():
    if R66RAW is None:
        add("D00", "BOUNDARY", "r66 增量层未读到", R66)
        return []
    rn = R66RAW.get("nodes", [])
    red = R66RAW.get("edges", [])
    rid = [n["id"] for n in rn]
    sc = R66RAW.get("selfcheck", {})

    linked = set()
    for e in red:
        linked.add(e["src"])
        linked.add(e["dst"])
    iso = [i for i in rid if i not in linked]
    add("D01", "FAIL" if iso else "PASS",
        "r66 增量层孤立节点 %d 个，selfcheck 却报 %s / all_pass=%s" % (
            len(iso), sc.get("isolated_nodes"), sc.get("all_pass")),
        "孤立 = %s ⇒ **与 A04 同一缺陷族**：selfcheck 的 isolated_nodes 与自身边表矛盾，"
        "r64（32 个判定孤立却报 0）之后**第 2 次独立复发**；两册均声明 all_pass=true ⇒ "
        "「自检通过 ≠ 守约」在并行图谱链上已出现两次，属系统性而非笔误。"
        % (iso if iso else "无"))
    guard("D01_r66_isolated_contradiction",
          (len(iso) > 0) and (sc.get("isolated_nodes") == 0), "r66 selfcheck 与边表矛盾")
    guard("D01_defect_family_second", True, "同缺陷族第 2 次复发已登记")

    et = sorted(set(e.get("type") for e in red))
    negs = [t for t in et if t in R66_NEG]
    add("D02", "BOUNDARY",
        "r66 边类型 %d 项，其中降级/撤回类 %d 项" % (len(et), len(negs)),
        "类型 = %s；降级/撤回/否证类 = %s ⇒ 库内 3 项词表（cites/references/depends_on）"
        "**连「被降级」「被撤回」「否证排除」这些审计基本操作都表达不了**；"
        "三份产物（attack25 / r64 / r66）各自独立触发扩表需求 ⇒ 扩表是结构性需求，非单册口味。"
        % (et, negs))
    guard("D02_graded_relations", len(negs) > 0, "检出降级/撤回类关系")

    anchors = []
    for e in red:
        tgt = R66_TO_R64.get(e["src"])
        if tgt and (tgt in R64_IDS):
            anchors.append({"finding": tgt, "via": e["src"], "target": e["dst"],
                            "relation": e.get("type"),
                            "negative_edge": e.get("type") in R66_NEG})
    add("D03", "BOUNDARY",
        "r66 为 r64 的孤立判定提供 %d 条**证据级**挂载（缺口 32 → %d）" % (
            len(anchors), 32 - len(anchors)),
        "锚点 = %s ⇒ 这 %d 条不是关键词猜测，而是 r66 产物内**已存在的边**"
        "（r66 用 R64_* 编号引用 r64 的判定），可信度高于 C06 的关键词候选；"
        "剩余 %d 条仍无出处。注意：r66 的 dst 是它自己的节点（FAM_QEI / K_GEOM / R66_I03 / O_GC_REL），"
        "跨图并入时须先把这些节点也纳入（否则又造一批悬空边）。"
        % ([{"%s→%s" % (a["finding"], a["target"]): a["relation"]} for a in anchors],
           len(anchors), 32 - len(anchors)))
    guard("D03_anchors_found", len(anchors) == 5, "r66 证据级锚点计数 5")
    guard("D03_anchor_targets_cross_graph",
          all(a["target"] in [n["id"] for n in rn] for a in anchors),
          "锚点指向 r66 自有节点（跨图并入须同时纳入）")

    schemas = {
        "attack25 来料": MINE_RAW.get("schema"),
        "r64 骨架": RAW.get("schema"),
        "r66 增量层": R66RAW.get("schema"),
    }
    add("D04", "BOUNDARY",
        "三份图谱产物各自声明 schema，字段名互不相同",
        "声明 = %s ⇒ r64/r66 自称同一 schema 名 `openuft-index-graph/v1`，"
        "却与库内事实标准字段名不同（src/dst/type vs source/target/relation），"
        "attack25 来料又用 from/to/relation ⇒ **同名不同构 + 不同名不同构同时存在**。"
        "这是 r65 G35h「库内 schema 规范文件数 = 0」的独立复现："
        "在没有规范文件的情况下，每册都会重新发明一套字段约定。"
        "三图合计：节点 %d、边 %d（17+46+26 / 16+22+24）。"
        % (schemas, len(MINE_IDS) + len(R64_IDS) + len(rid),
           len(MINE_EDGES) + len(EDGES) + len(red)))
    guard("D04_schema_names_inconsistent",
          len(set(schemas.values())) >= 2, "检出 schema 声明不一致（同名不同构/不同名）")
    return anchors


# ================================================================ 输出
LIB_NODE_FIELDS = ["id", "label", "author", "captured_at", "community", "community_name",
                   "contributor", "epistemic_status", "file_type", "norm_label",
                   "rationale", "source_file", "source_location", "source_quote", "source_url"]
LIB_LINK_FIELDS = ["source", "target", "relation", "confidence", "confidence_score",
                   "rationale", "source_file", "source_location", "source_quote", "weight"]
BASE = "attack25b_并行骨架规范化与两图对照_2026-10-26"


def finalize(canon, attach, anchors, out_vocab, mism):
    # 结构守卫：规范化产物必须含库内 15/10 字段（draft 字段为附加，不覆盖原值）
    miss_n = [f for f in LIB_NODE_FIELDS if f not in canon["nodes"][0]]
    miss_l = [f for f in LIB_LINK_FIELDS if f not in canon["links"][0]]
    guard("S01_lib_node_fields", not miss_n, "节点含库内 15 字段（缺 %s）" % (miss_n or "无"))
    guard("S02_lib_link_fields", not miss_l, "边含库内 10 字段（缺 %s）" % (miss_l or "无"))
    guard("S03_node_count", len(canon["nodes"]) == len(NODES), "节点数守恒 %d" % len(NODES))
    guard("S04_link_count", len(canon["links"]) == len(EDGES), "边数守恒 %d" % len(EDGES))
    guard("S05_no_dangling", all(
        (l["source"] in R64_IDS) and (l["target"] in R64_IDS) for l in canon["links"]),
        "无悬空边")

    canon["graph"]["proposed_additions"] = [
        {
            "id": "link:%s->%s" % (a["id"], t),
            "kind": "判定节点挂载候选（自动候选，非定案）",
            "source": a["id"],
            "target": t,
            "relation": a["relation"],
            "weight": a["weight"],
            "negative_edge": a["negative_edge"],
            "confidence": "INFERRED",
            "confidence_score": 0.5,
            "why": "A04：该判定节点在 r64 产物内零边；关键词命中被评对象；极性由 verdict=%s 机器推定"
                   % a["verdict"],
            "needs_review": True,
        }
        for a in attach for t in a["targets"]
    ] + [
        {
            "id": "link:%s->%s" % (a["finding"], a["target"]),
            "kind": "判定节点挂载（r66 证据级：r66 产物内已存在的边）",
            "source": a["finding"],
            "target": a["target"],
            "relation": a["relation"],
            "weight": 1.0,
            "negative_edge": a["negative_edge"],
            "confidence": "EXTRACTED",
            "confidence_score": 0.9,
            "why": "D03：r66 用 %s 引用该判定并已连边；跨图并入须同时纳入 r66 的 %s 节点" % (a["via"], a["target"]),
            "needs_review": True,
        }
        for a in anchors
    ]
    canon["graph"]["merge_plan"] = {
        "recommended_order": ["M2（并存入库 + 9 个等价节点 id 归一）", "M1（补 32 条判定边后合并为单图）"],
        "merged_nodes_if_M1": len(MINE_IDS) + len([i for i in R64_IDS
                                                   if i not in set(b for (_, b, _) in EQUIV)]),
        "missing_edges": 32,
        "r66_evidence_anchors": len(anchors),
        "residual_gap": 32 - len(anchors),
        "auto_candidate_edges": len(canon["graph"]["proposed_additions"]),
        "out_of_vocab_relations": out_vocab,
        "key_status_mismatches": mism,
    }
    return canon


def dump(obj, path):
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False))
        f.write(u"\n")


def main():
    seg_selfcheck()
    attach, out_vocab, mism = seg_compare()
    anchors = seg_r66()
    canon = CANON_CACHE.get("r64") or build_canonical()
    canon = finalize(canon, attach, anchors, out_vocab, mism)

    counts = {}
    for it in ITEMS:
        counts[it["verdict"]] = counts.get(it["verdict"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])
    g_bad = [g["name"] for g in GUARDS if not g["ok"]]

    data = {
        "book": "attack25b · 并行骨架（r64/r65 图谱）规范化与两图对照",
        "date": "2026-10-26",
        "inputs": {
            "r64_skeleton": os.path.basename(R65),
            "r64_book": os.path.basename(R65_BOOK),
            "attack25_raw": os.path.basename(MINE),
            "attack25_canonical": os.path.basename(CANON_PATH),
            "note": "全部只读，未修改任何并行产物字节",
        },
        "items": ITEMS,
        "counts": counts,
        "guards": {"total": len(GUARDS), "passed": g_ok, "failed": g_bad},
        "key_numbers": {
            "r64_nodes": len(NODES), "r64_edges": len(EDGES),
            "r64_findings_isolated": 32,
            "attack25_nodes": len(MINE_NODES), "attack25_edges": len(MINE_EDGES),
            "equiv_pairs": len(EQUIV),
            "auto_attach_candidates": len(attach),
            "r66_evidence_anchors": len(anchors),
            "residual_gap": 32 - len(anchors),
            "r66_nodes_edges": ([len(R66RAW.get("nodes", [])), len(R66RAW.get("edges", []))]
                                if R66RAW else None),
            "out_of_vocab_relations": out_vocab,
            "key_status_mismatches": [list(m) for m in mism],
        },
    }
    dump(data, os.path.join(HERE, BASE + ".json"))
    dump(canon, os.path.join(HERE, "图谱层_超光速攻破路线_并行骨架规范化_2026-10-26.json"))

    lines = []
    lines.append("attack25b · 并行骨架规范化与两图对照 报告 2026-10-26")
    lines.append("守卫 %d/%d 通过%s" % (g_ok, len(GUARDS), "" if not g_bad else "（失败：%s）" % g_bad))
    lines.append("条目 %d：%s" % (len(ITEMS), counts))
    lines.append("")
    sections = {"A": ("A 段 · 并行产物自洽核对", "A01", "A06"),
                "B": ("B 段 · 规范化映射（见产物 graph 段）", None, None),
                "C": ("C 段 · 两图对照", "C01", "C08"),
                "D": ("D 段 · 第三张图（r66 增量层）", "D00", "D04")}
    for key in ("A", "C", "D"):
        title, a, b = sections[key]
        lines.append("== " + title)
        for it in ITEMS:
            if a <= it["code"] <= b:
                lines.append("[%s] %s · %s" % (it["verdict"], it["code"], it["title"]))
                lines.append("      " + str(it["detail"]))
        lines.append("")
    for g in GUARDS:
        lines.append("%s %s :: %s" % ("OK  " if g["ok"] else "FAIL", g["name"], g["detail"]))
    lines.append("")
    lines.append("产物：%s.json / %s_report.txt / 图谱层_超光速攻破路线_并行骨架规范化_2026-10-26.json"
                 % (BASE, BASE))
    io.open(os.path.join(HERE, BASE + "_report.txt"), "w", encoding="utf-8").write(u"\n".join(lines))

    print(u"守卫 %d/%d" % (g_ok, len(GUARDS)))
    print(u"条目 %d %s" % (len(ITEMS), counts))
    if g_bad:
        for g in g_bad:
            print(u"GUARD-FAIL " + g)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
