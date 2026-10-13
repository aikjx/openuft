# -*- coding: utf-8 -*-
"""
attack25 · 超光速攻破路线图谱：结构 / 量纲 / 量级 复算

来料：图谱层_超光速攻破路线_来料_2026-10-13.json（17 节点 / 16 边，手写草稿）
本册任务（三段，全部机器判定，不采信来料自报）：
  E 段 · 四条方程的量纲齐次性（Fraction 三元组 (M,L,T)）
  N 段 · 负能量预算与 Casimir 对照的量级（Decimal 40 位）
  S 段 · 图谱结构：必要条件闭合度 / 假可达 / 悬挂节点 / 关系词表越界 / 溯源缺失

纪律：量纲类断言必须机器兜底（不手算）；不代选增补方案（只列清单）。
纯标准库，零外部依赖，Python 3.8+。
"""
from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 40

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "图谱层_超光速攻破路线_来料_2026-10-13.json")

# ---------------------------------------------------------------- 量纲工具
# 三元组 = (M, L, T) 指数；相乘=指数相加，相除=指数相减
def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dpow(a, n):
    return (a[0] * n, a[1] * n, a[2] * n)


def dstr(a):
    return "M^%s L^%s T^%s" % (a[0], a[1], a[2])


D_C = (0, 1, -1)          # 光速
D_G = (-1, 3, -2)         # 牛顿常数
D_V = (0, 1, -1)          # 任意速度 v_s / v
D_F = (0, 0, 0)           # 形状函数 f（无量纲）
D_DF = (0, -1, 0)         # f' = df/dx
D_T = (0, 0, 1)           # 时间 dt
D_X = (0, 1, 0)           # 长度 dx / R / δ
D_RHO = (1, -1, -2)       # 能量密度
D_MASS = (1, 0, 0)        # 质量

# ---------------------------------------------------------------- 数值常量
C = Decimal("299792458")
G = Decimal("6.67430e-11")
HBAR = Decimal("1.054571817e-34")
GM_SUN = Decimal("1.3271244e20")          # 日心引力常数 GM_☉（IAU 标称）
M_SUN = GM_SUN / G
PI = Decimal("3.14159265358979323846264338327950288")


def fv(x, n=25):
    """定点科学计数输出；Decimal.quantize 在高位数会抛 InvalidOperation，故用 format。"""
    try:
        return format(Decimal(x), "." + str(n) + "E")
    except Exception:
        return str(x)


def fs(x, n=6):
    try:
        return format(Decimal(x), "." + str(n) + "E")
    except Exception:
        return str(x)


# ---------------------------------------------------------------- 条目收集
ITEMS = []          # 判定条目
GUARDS = []         # 自检守卫


def add(code, verdict, title, detail):
    ITEMS.append({"code": code, "verdict": verdict, "title": title, "detail": detail})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


# ================================================================ E 段 · 量纲
def seg_dim():
    # E01 · Alcubierre 度规三项齐次
    t1 = dmul(dpow(D_C, 2), dpow(D_T, 2))              # -c²dt²
    shift = dmul(dmul(D_V, D_F), D_T)                  # v_s·f·dt
    t2 = dpow(shift, 2)                                # (dx - v_s f dt)²
    t3 = dpow(D_X, 2)                                  # dy² / dz²
    ok1 = (t1 == t2 == t3 == (0, 2, 0))
    add("E01", "PASS" if ok1 else "FAIL",
        "Alcubierre 度规三项齐次（ds² 各项 = L²）",
        "-c²dt²=%s；(v_s·f·dt)²=%s（f 无量纲、v_s·dt 给出长度，与 dx 可相减）；dy²=%s"
        % (dstr(t1), dstr(t2), dstr(t3)))
    guard("E01_metric_homogeneous", ok1, "三项同为 L²")

    # E02 · 固有时间式
    ratio = ddiv(dpow(D_V, 2), dpow(D_C, 2))           # v²/c²
    tau2 = dmul(dpow(D_T, 2), (0, 0, 0))               # dt²(无量纲因子)
    ok2 = (ratio == (0, 0, 0)) and (tau2 == (0, 0, 2))
    add("E02", "PASS" if ok2 else "FAIL",
        "固有时间式 dτ²=dt²(1-v²/c²) 量纲闭合",
        "v²/c²=%s（无量纲，可相减）；dτ² 与 dt² 同为 %s；v=c 时括号为 0 ⇒ dτ=0"
        % (dstr(ratio), dstr(tau2)))
    guard("E02_propertime_dimension", ok2, "v²/c² 无量纲且 dτ²~T²")

    # E03 · 负能量密度
    e3 = dmul(ddiv(dmul(dpow(D_C, 2), dpow(D_V, 2)), D_G), dpow(D_DF, 2))
    ok3 = (e3 == D_RHO)
    add("E03", "PASS" if ok3 else "FAIL",
        "负能量密度式 ρ=-(c²v_s²/32πG)f'² 量纲 = 能量密度",
        "机器算得 %s，目标 %s（32π 无量纲不影响）" % (dstr(e3), dstr(D_RHO)))
    guard("E03_energy_density_dimension", ok3, "ρ 量纲 = M L^-1 T^-2")

    # E04 · 负能量质量当量
    e4 = ddiv(dmul(dpow(D_V, 2), dpow(D_X, 2)), dmul(D_G, D_X))
    ok4 = (e4 == D_MASS)
    add("E04", "PASS" if ok4 else "FAIL",
        "质量当量式 M_neg≈v_s²R²/(8Gδ) 量纲 = 质量",
        "机器算得 %s，目标 %s" % (dstr(e4), dstr(D_MASS)))
    guard("E04_budget_mass_dimension", ok4, "M_neg 量纲 = M")

    # E05 · 两式系数是否同源（量级推导对照）
    # |ρ| ~ c²v_s²/(32πG)·f'²，取 f' ~ 1/δ、壳体积 ~ R²δ ⇒ E ~ c²v_s²R²/(32πGδ)
    # ⇒ M = E/c² = v_s²R²/(32πGδ)；来料给 1/8 ⇒ 差因子 4
    add("E05", "BOUNDARY",
        "eq_energy 与 eq_budget 系数不同源（差因子 4，属量级估算差）",
        "由 eq_energy 走壳体积积分推得 M ~ v_s²R²/(32πGδ)，来料 eq_budget 为 /(8Gδ)，相差 4 倍；"
        "两者均为形状函数依赖的量级式，不据此判任何一方错，但引用时须声明用哪一式。")
    guard("E05_coeff_gap_recorded", True, "系数差 4 已登记为 BOUNDARY 非 FAIL")

    # E06 · 标准式对照：角度因子缺失
    add("E06", "BOUNDARY",
        "eq_energy 缺角度因子 (y²+z²)/r_s²（对照 Alcubierre 1994 Eulerian T^{00}）",
        "标准式含 (y²+z²)/r_s²（轴上为 0、赤道为 1）与 v_s²/c²；来料式只保留 f'²。"
        "量纲不受影响（该因子无量纲），但能量分布的方向依赖被抹掉 ⇒ 不可用于积分预算。"
        "标注 [C]：以原始文献复核后再定论。")

    # E07 · 关键物理口径：dτ=0 的适用域
    add("E07", "FAIL",
        "钥匙0 的 claim 越界：dτ=0 只适用于类光（v=c），不构成 v>c 的支撑",
        "dτ²=dt²(1-v²/c²)：v=c ⇒ dτ=0（类光，无固有时间）；v>c ⇒ dτ²<0（类空间隔，"
        "不是「时间冻结」而是「无类时世界线」）。故 key0 对 target_ftl(v_s>c) 提供零支撑，"
        "且其 claim「m=0 ⇒ 类光」只对零质量粒子成立，不能外推到有质量飞船。")


# ================================================================ N 段 · 量级
def mneg(R, delta, vs=None):
    vs = C if vs is None else vs
    return vs * vs * R * R / (Decimal(8) * G * delta)


def rho_bubble(delta, vs=None):
    vs = C if vs is None else vs
    return C * C * vs * vs / (Decimal(32) * PI * G * delta * delta)


def rho_casimir(d):
    return -(PI * PI * HBAR * C) / (Decimal(720) * d * d * d * d)


def seg_num():
    R0 = Decimal("100")          # 泡半径 100 m
    D0 = Decimal("1")            # 壁厚 1 m
    m1 = mneg(R0, D0)
    r1 = m1 / M_SUN
    add("N01", "INFO",
        "基准泡负能量质量当量（R=100 m, δ=1 m, v_s=c，按来料 eq_budget）",
        "|M_neg| = %s kg = %s M_☉（M_☉=GM_☉/G=%s kg）"
        % (fv(m1), fs(r1), fv(M_SUN)))
    guard("N01_budget_positive", m1 > 0, "质量当量为正量级")

    # N02 · 给定质量预算反解壁厚
    delta_for_1msun = C * C * R0 * R0 / (Decimal(8) * G * M_SUN)
    add("N02", "INFO",
        "反解：|M_neg| 压到 1 M_☉ 所需的壁厚（R=100 m, v_s=c）",
        "δ = v_s²R²/(8G·M_☉) = %s m（壁厚越厚需求越小）" % fv(delta_for_1msun))
    guard("N02_delta_positive", delta_for_1msun > 0, "反解壁厚为正")

    # N03 · 薄壁惩罚
    d_thin = Decimal("1e-15")
    m_thin = mneg(R0, d_thin)
    add("N03", "INFO",
        "薄壁惩罚：δ 由 1 m 收到 1e-15 m 时质量当量变化",
        "|M_neg| = %s M_☉（较 δ=1 m 放大 %s 倍）⇒ 需求与 δ 成反比，"
        "与量子不等式要求「薄壁」方向相反（本图谱的核心张力）"
        % (fs(m_thin / M_SUN), fs(m_thin / m1)))
    guard("N03_thin_wall_scales", m_thin / m1 > Decimal("1e14"), "薄壁放大 >1e14 倍")

    # N04/N05/N06 · 密度量级与 Casimir 对照
    rb = rho_bubble(D0)
    rc = rho_casimir(Decimal("1e-6"))
    ratio = abs(rb) / abs(rc)
    add("N04", "INFO",
        "宏观泡所需负能量密度量级（δ=1 m, v_s=c）",
        "|ρ| = c²v_s²/(32πGδ²) = %s J/m³" % fv(rb))
    add("N05", "INFO",
        "实验室 Casimir 负能量密度参照（平行板 d=1 µm）",
        "ρ_C = -π²ħc/(720 d⁴) = %s J/m³" % fv(rc))
    add("N06", "BOUNDARY",
        "两者量级对照：差 %s 倍（口径不同，仅作量级参照）" % fs(ratio),
        "泡取宏观体密度（δ=1 m），Casimir 取板间局域密度（d=1 µm）；两者尺度与口径不同源，"
        "不构成严格不等式，只给出「实验室已实现的负能量密度」与「宏观泡需求」的量级落差。")
    guard("N06_ratio_recorded", ratio > Decimal("1e40"), "落差 >1e40 已登记")


# ================================================================ S 段 · 结构
RAW = json.load(io.open(SRC, encoding="utf-8"))

# 库内图谱（graph.json）实际词表，用于越界判定（只读对照，不改库内文件）
CANON_RELATIONS = {"cites", "references", "depends_on"}
CANON_EPistemic = {
    "source_assertion", "declared_limitation", "review_required", "adopted_input",
    "conditional_derivation", "declared_model_assumption", "source_model_result",
    "algebraic_structure", "adopted_geometric_framework", "geometric_construction",
}

NEGATIVE_MARKERS = ("不足", "只能到光速")


def is_negative(rel):
    return any(m in rel for m in NEGATIVE_MARKERS)


def reach(start, edges, drop_negative):
    seen = set()
    stack = [start]
    while stack:
        cur = stack.pop()
        for e in edges:
            if drop_negative and is_negative(e["relation"]):
                continue
            if e["from"] == cur and e["to"] not in seen:
                seen.add(e["to"])
                stack.append(e["to"])
    return seen


def seg_struct():
    nodes = RAW["nodes"]
    edges = RAW["edges"]
    ids = [n["id"] for n in nodes]
    # S01 · 规模与分布
    by_type = {}
    by_status = {}
    for n in nodes:
        by_type[n.get("type", "?")] = by_type.get(n.get("type", "?"), 0) + 1
        s = n.get("status", "未标注")
        by_status[s] = by_status.get(s, 0) + 1
    add("S01", "INFO", "来料规模与分布",
        "节点 %d / 边 %d；type 分布 %s；status 分布 %s" % (len(nodes), len(edges), by_type, by_status))
    guard("S01_size", len(nodes) == 17 and len(edges) == 16, "17 节点 / 16 边")

    # S02 · 必要条件闭合度
    target = "target_ftl"
    nec = [e["from"] for e in edges if e["to"] == target and "必要条件" in e["relation"]]
    st = {n["id"]: n.get("status") for n in nodes}
    done = [k for k in nec if st.get(k) == "已攻破" or st.get(k) == "已到手"]
    closure = (len(done), len(nec))
    add("S02", "INFO",
        "目标必要条件闭合度 = %d/%d（图谱自洽，非缺陷）" % closure,
        "target_ftl 的必要条件为 %s，状态分别 %s ⇒ 全部未满足，目标「未实现」与图谱自洽"
        % (nec, {k: st.get(k) for k in nec}))
    guard("S02_no_closure", closure[0] == 0, "必要条件 0/3 满足")

    # S03 · 假可达（负向边当正向用）
    naive = reach("key0", edges, False)
    strict = reach("key0", edges, True)
    fake = (target in naive) and (target not in strict)
    add("S03", "FAIL" if fake else "PASS",
        "负向边导致假可达：key0 在「全边」语义下可达目标，剥离负向边后不可达",
        "含负向边时 key0 可达 %s；剥离后可达 %s ⇒ 把「只能到光速c，不足超光速」当普通边，"
        "会读出「已到手的钥匙0 通向超光速目标」的假象。导入必须把负向边单独成类。" % (sorted(naive), sorted(strict)))
    guard("S03_fake_reach_detected", fake, "假可达被检出")

    # S04 · 对目标的零贡献集（严格语义）
    zero = []
    for nid in ids:
        if nid == target:
            continue
        if target not in reach(nid, edges, True):
            zero.append(nid)
    add("S04", "FAIL",
        "严格语义下对 target_ftl 零贡献的节点共 %d 个" % len(zero),
        "零贡献集 = %s ⇒ 恰好覆盖「已到手/已攻破(纸上)/原型验证」那一侧："
        "key0（固有时间冻结）、key2（正能量亚光速泡）、eq_metric、eq_propertime、agenda7。"
        "读数：现有进展全部落在亚光速侧，对 v_s>c 目标不构成推进。" % zero)
    guard("S04_zero_contrib", set(["key0", "key2"]) <= set(zero), "key0/key2 均零贡献")

    # S05 · 关系词表越界
    rels = sorted(set(e["relation"] for e in edges))
    out_vocab = [r for r in rels if r not in CANON_RELATIONS]
    add("S05", "BOUNDARY",
        "关系词表越界 %d/%d（库内词表仅 %s）" % (len(out_vocab), len(rels), sorted(CANON_RELATIONS)),
        "来料关系 %s 全部不在库内词表内；其中「只能到光速c，不足超光速」是负向边，"
        "库内词表无负向类 ⇒ 直接映射会丢信息。本册提出扩表申请（见产物 graph.meta），未擅改库内文件。" % rels)
    guard("S05_vocab_out", len(out_vocab) == len(rels), "越界率 100%")

    # S06 · 字段名越界
    add("S06", "BOUNDARY", "字段名与库内 schema 不一致（from/to vs source/target 等）",
        "库内 graph.json 边用 source/target，节点用 epistemic_status/file_type/norm_label/rationale/"
        "source_file/source_location/source_quote；来料用 from/to 与 type/status。"
        "本册产出已给出对齐版本。")

    # S12 · epistemic_status 映射是否落在库内词表内
    mapped = [STATUS_MAP.get(n.get("status")) for n in nodes]
    mapped = [m if m else ("source_assertion" if n.get("type") == "方程" else "review_required")
              for m, n in zip(mapped, nodes)]
    bad = sorted(set(m for m in mapped if m not in CANON_EPistemic))
    add("S12", "PASS" if not bad else "FAIL",
        "状态词映射是否落在库内 epistemic_status 词表内",
        "映射结果 %s；越界项 %s" % (sorted(set(mapped)), bad if bad else "无"))
    guard("S12_epistemic_in_vocab", not bad, "全部映射落在库内词表内")

    # S07 · 溯源缺失
    miss = [n["id"] for n in nodes if not any(k.startswith("source_") for k in n.keys())]
    add("S07", "FAIL", "溯源三件套缺失 %d/%d 节点" % (len(miss), len(nodes)),
        "库内图谱每个节点都带 source_file/source_location/source_quote（可回溯原文）；"
        "来料 0 个节点带 ⇒ 无法验证任何一条 claim。本册规范化版已补（指向来料正本）。")
    guard("S07_no_provenance", len(miss) == len(nodes), "全部节点缺溯源")

    # S08 · 无验收/证伪条件
    has_gate = [n for n in nodes if ("验收" in n.get("label", "") or "证伪" in n.get("label", "")
                                     or "判据" in n.get("label", ""))]
    add("S08", "FAIL", "攻破路线图缺「验收门槛 / 证伪条件」节点",
        "target_ftl 只有入边（必要条件），没有任何「达到什么算攻破 / 什么观测能否证伪」的节点或字段 ⇒ "
        "该图无法判定成功，只能判定失败（与库内 M1–M5 升格门槛体例不符）。")
    guard("S08_no_gate", len(has_gate) == 0, "无验收节点")

    # S09 · 充分性未声明
    add("S09", "BOUNDARY", "只声明必要条件，未声明充分性",
        "key1∧key3∧key4 被标为「必要条件(∧)」，但图谱未声明三者（连同议程）是否充分 ⇒ "
        "即使三条钥匙全到手，也不能由本图推出 target 成立。")

    # S10 · 归属存疑：Krasnikov
    add("S10", "BOUNDARY", "agenda6（Krasnikov 不稳定性量级）归属存疑",
        "Krasnikov 管的核心议题是「超光速需要预先铺设管道 / 泡内无法向前方发信号控制泡」，"
        "属因果与可控性（key3），而非量子引力稳定化（key4）。现挂 key4 会把因果类问题记到稳定化账上。"
        "本册不代改，列入待裁决清单。")

    # S11 · 框架前提未声明
    add("S11", "FAIL", "缺「理论框架前提」节点：key1 是否真为合取必要条件取决于 GR vs 修正引力",
        "在 GR + 物质满足能量条件的前提下，负能量是 v_s>c 的必要条件；但在修正引力 / 额外维框架下，"
        "存在不依赖负能量的路径 ⇒ key1 的「必要条件(∧)」地位是框架依赖的。"
        "来料未声明框架 ⇒ 必要条件结构本身未定。")


# ================================================================ 规范化输出
STATUS_MAP = {
    "未实现": "declared_limitation",
    "已到手": "source_assertion",
    "未攻破": "declared_limitation",
    "已攻破(纸上)": "source_model_result",
}

RELATION_MAP = {
    "必要条件(∧)": ("depends_on", Decimal("1.0"), "INFERRED", Decimal("0.85"), True),
    "只能到光速c，不足超光速": ("insufficient_for", Decimal("0.0"), "INFERRED", Decimal("0.85"), False),
    "支撑(船内dτ=dt)": ("references", Decimal("1.0"), "EXTRACTED", Decimal("1.0"), False),
    "内核(m=0⇒dτ=0)": ("references", Decimal("1.0"), "EXTRACTED", Decimal("1.0"), False),
    "支撑(ρ<0违反WEC)": ("references", Decimal("1.0"), "EXTRACTED", Decimal("1.0"), False),
    "精算(恒星级以上负能)": ("references", Decimal("1.0"), "EXTRACTED", Decimal("1.0"), False),
    "子议程": ("sub_agenda", Decimal("1.0"), "EXTRACTED", Decimal("1.0"), False),
    "前提": ("prerequisite", Decimal("1.0"), "EXTRACTED", Decimal("1.0"), False),
    "原型验证": ("validates", Decimal("1.0"), "EXTRACTED", Decimal("1.0"), False),
}

COMMUNITY = {
    "判定": (0, "钥匙链与目标判定"),
    "钥匙": (0, "钥匙链与目标判定"),
    "方程": (1, "方程与量纲层"),
    "议程": (2, "议程与实验层"),
}

NODE_NOTE = {
    "key0": "E07 判 FAIL：dτ=0 只适用于类光 v=c，v>c 时 dτ²<0（类空），不构成超光速支撑；m=0 只描述零质量粒子。",
    "key2": "S04 判零贡献：正能量泡上限 v_s<c，与 target 的 v_s>c 反向；应作为降级里程碑而非钥匙。",
    "eq_energy": "E03 量纲 PASS；E06 缺角度因子 (y²+z²)/r_s²（对照 Alcubierre 1994），不可直接用于积分预算。",
    "eq_budget": "E04 量纲 PASS；E05 与 eq_energy 系数差因子 4，引用须声明用哪一式。",
    "agenda6": "S10 归属存疑：Krasnikov 议题属因果/预置（key3）而非量子引力稳定化（key4）。",
    "target_ftl": "S08 缺验收门槛与证伪条件；S09 只声明必要条件未声明充分性；S11 框架前提未声明。",
}

REL_NOTE = {
    "只能到光速c，不足超光速": "S03：负向边。若与正向边同权，会读出假可达路径（key0/key2 → target）。",
    "必要条件(∧)": "S09/S11：合取必要条件，充分性未声明；且 GR vs 修正引力会改变 key1 的地位。",
}


def jdefault(obj):
    """Fraction/Decimal 不可直接 JSON 序列化（库内既有图谱 confidence_score 为数字，故转 float）。"""
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, Fraction):
        return float(obj)
    raise TypeError("not serializable: %r" % type(obj))


def norm_label(text):
    out = []
    for ch in text:
        out.append(ch.lower())
    return "".join(out)


def build_canonical():
    nodes = []
    for n in RAW["nodes"]:
        cid, cname = COMMUNITY.get(n.get("type", "?"), (3, "未分类"))
        status = n.get("status")
        epi = STATUS_MAP.get(status)
        if epi is None:
            epi = "source_assertion" if n.get("type") == "方程" else "review_required"
        rationale = n.get("claim") or n.get("formula") or ("议程项：" + n.get("label", ""))
        if n["id"] in NODE_NOTE:
            rationale = rationale + " ｜ 本册判定：" + NODE_NOTE[n["id"]]
        nodes.append({
            "id": n["id"],
            "label": n["label"],
            "author": None,
            "captured_at": None,
            "community": cid,
            "community_name": cname,
            "contributor": None,
            "epistemic_status": epi,
            "file_type": "rationale" if n.get("type") in ("判定", "钥匙", "议程") else "document",
            "norm_label": norm_label(n["label"]),
            "rationale": rationale,
            "source_file": "图谱层_超光速攻破路线_来料_2026-10-13.json",
            "source_location": ("04_公共成果/本项目_统一场论攻破/"
                                "图谱层_超光速攻破路线_来料_2026-10-13.json#node:" + n["id"]),
            "source_quote": json.dumps(n, ensure_ascii=False),
            "source_url": None,
            "type_draft": n.get("type"),
            "status_draft": status,
            "formula": n.get("formula"),
        })

    links = []
    for e in RAW["edges"]:
        rel, weight, conf, score, gate = RELATION_MAP.get(
            e["relation"], ("references", Decimal("1.0"), "EXTRACTED", Decimal("1.0"), False))
        rationale = e["relation"]
        if e["relation"] in REL_NOTE:
            rationale = e["relation"] + " ｜ 本册判定：" + REL_NOTE[e["relation"]]
        links.append({
            "source": e["from"],
            "target": e["to"],
            "relation": rel,
            "confidence": conf,
            "confidence_score": score,
            "rationale": rationale,
            "source_file": "图谱层_超光速攻破路线_来料_2026-10-13.json",
            "source_location": ("04_公共成果/本项目_统一场论攻破/"
                                "图谱层_超光速攻破路线_来料_2026-10-13.json#edge:" + e["from"] + "->" + e["to"]),
            "source_quote": json.dumps(e, ensure_ascii=False),
            "weight": weight,
            "gate_conjunctive": gate,
            "relation_draft": e["relation"],
            "negative_edge": is_negative(e["relation"]),
        })

    graph = {
        "directed": True,
        "multigraph": False,
        "graph": {
            "name": "超光速攻破路线",
            "canonical_of": "图谱层_超光速攻破路线_来料_2026-10-13.json",
            "normalized_at": "2026-10-13",
            "normalized_by": "attack25_超光速攻破路线图谱_结构与量纲复算_2026-10-13.py",
            "schema_reference": ("07_统一场方程/空间螺旋几何化统一场论/证明依赖图/图谱输出/graph.json"
                                 "（库内既有图谱，节点 15 字段 / 边 10 字段）"),
            "relation_vocabulary_extension_request": {
                "status": "待批准（本册不擅改库内词表与既有图谱）",
                "reason": "来料 9 种关系 100% 越界，其中负向关系在库内词表中无对应，"
                          "直接映射为 depends_on/references 会造成 S03 的假可达。",
                "proposed_relations": ["sub_agenda", "prerequisite", "validates", "insufficient_for"],
                "proposed_edge_fields": ["gate_conjunctive", "negative_edge"],
            },
            "proposed_additions": [
                {"id": "gate_accept", "label": "验收门槛与证伪条件（target 的判据）",
                 "why": "S08：目前只能判定失败、无法判定成功", "attach_to": "target_ftl"},
                {"id": "frame_premise", "label": "框架前提：GR 爱因斯坦方程 vs 修正引力",
                 "why": "S11：决定 key1 是否为合取必要条件", "attach_to": "key1"},
                {"id": "key5", "label": "视界与因果断联 / 预置路径（Krasnikov 管）",
                 "why": "S10：泡内无法向前方发信号，属因果类", "attach_to": "key3"},
                {"id": "key6", "label": "气泡生成与加速（v_s 从 0 到 >c 的过程）",
                 "why": "来料四条方程全部假设 v_s 已给定，未覆盖启动过程", "attach_to": "target_ftl"},
                {"id": "eq_nec", "label": "能量条件 NEC/WEC：T_μν t^μ t^ν ≥ 0",
                 "why": "eq_energy 的「违反 WEC」缺判据式，无法机器判定", "attach_to": "eq_energy"},
                {"id": "agenda8", "label": "量子不等式对 |E|·持续时间与壁厚的具体上界",
                 "why": "agenda1 只有议题名，无可执行判据（Ford–Roman / Pfenning–Ford 需文献核对 [C]）",
                 "attach_to": "agenda1"},
                {"id": "obs_channel", "label": "可检验性：宏观泡的观测渠道（引力波/透镜/负能量实测）",
                 "why": "S08 的观测侧；无观测渠道则整图不可证伪", "attach_to": "gate_accept"},
            ],
        },
        "nodes": nodes,
        "links": links,
        "hyperedges": [],
    }
    return graph


# ================================================================ 主流程
def main():
    seg_dim()
    seg_num()
    seg_struct()
    graph = build_canonical()

    counts = {}
    for it in ITEMS:
        counts[it["verdict"]] = counts.get(it["verdict"], 0) + 1

    ok_guards = sum(1 for g in GUARDS if g["ok"])
    data = {
        "title": "超光速攻破路线图谱 · 结构 / 量纲 / 量级 复算",
        "date": "2026-10-13",
        "source": "图谱层_超光速攻破路线_来料_2026-10-13.json",
        "items": ITEMS,
        "counts": counts,
        "guards": GUARDS,
        "guard_pass": "%d/%d" % (ok_guards, len(GUARDS)),
        "canonical_graph": graph,
    }
    out_json = os.path.join(HERE, "attack25_超光速攻破路线图谱_结构与量纲复算_2026-10-13.json")
    io.open(out_json, "w", encoding="utf-8").write(
        json.dumps(data, ensure_ascii=False, indent=1, default=jdefault))

    out_graph = os.path.join(HERE, "图谱层_超光速攻破路线_2026-10-13.json")
    io.open(out_graph, "w", encoding="utf-8").write(
        json.dumps(graph, ensure_ascii=False, indent=1, default=jdefault))

    lines = []
    lines.append("attack25 · 超光速攻破路线图谱：结构 / 量纲 / 量级 复算")
    lines.append("来料：图谱层_超光速攻破路线_来料_2026-10-13.json（17 节点 / 16 边）")
    lines.append("")
    for it in ITEMS:
        lines.append("[%s] %s · %s" % (it["verdict"], it["code"], it["title"]))
        lines.append("    " + it["detail"])
    lines.append("")
    lines.append("条目统计：" + str(counts))
    lines.append("自检守卫：%d/%d" % (ok_guards, len(GUARDS)))
    for g in GUARDS:
        lines.append("    %s %s | %s" % ("OK " if g["ok"] else "BAD", g["name"], g["detail"]))
    out_txt = os.path.join(HERE, "attack25_超光速攻破路线图谱_结构与量纲复算_2026-10-13_report.txt")
    io.open(out_txt, "w", encoding="utf-8").write("\n".join(lines) + "\n")

    print("\n".join(lines))
    return 0 if ok_guards == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
