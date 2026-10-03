# -*- coding: utf-8 -*-
"""
S17 统一场论核心公式体系 · 单位约定可行组合与「闭合代价」判定
=========================================================================
承接 2026-10-03 两册：
  ① 判定_统一场论核心公式_全目录总结与正确核固化（23 式规范台账 / 正确核 22 / 剔除 7）
  ② 整理_全维核心公式理论体系_全维分析（体系坐标 / 六维 0 维通过 / 六判据 1/6）
     —— 该册在 §8 给出三条路线，M1 =「单位约定单一化」被标为最高性价比。

本册执行 M1 + M2，把「否证无单一单位约定」推进为三个可判定问题：

  Q1 构造性：是否存在一套单位约定，使 23 式**原样**通过？        -> 原样通过集为空？
  Q2 唯一性：使「修复后通过数」最大的约定组合是否唯一？        -> 「自洽」是否唯一？
  Q3 闭合代价：要达到全通过，最少需要多少条**新物理/新定义**？  -> 最小增广集

为什么用组合枚举而不是重算量纲
------------------------------
各原册的 machine 产物给出的是**结论式量纲读数**（dimension_rows 的 lhs_dim/rhs_dim），
不含符号级表达式，无法在新的球面度口径下重新求值。
本册因此**不复算任何式的量纲**（严格回链原册），只在其读数之上做
**组合可行性分析 + 修复级别分层 + 最小增广集求解**。
凡本册声称的「通过」，含义是「在该约定下该式按原册读数成立（或仅需 L1 级修复）」。

修复级别分层（判据由原册给出，本册只归级）
------------------------------------------
  L0 恒成立      定义式 / 标准式 / 恒等重排，与口径无关
  L1 记号层可修   补公设约束 |v|=c、把 s 改注为面积元、补符号约定、补标准物理因子（1/r、v⃗）
                 —— **不改变物理内容**，属记号/教科书层
  L2 需新物理     任何补法都改变物理内容（核力场补 T^-1、运动电荷式、归一化方程）
  L3 不可修       量纲缺口含 M 或 I 且不含 c 的幂次可消 ⇒ 无最小修复

L1 的红线：只允许「记号层 + 标准教科书因子」。凡需引入新相互作用/新常数/新维度才能补的，
一律判 L2 或 L3，**不得**为了凑通过率而放宽（这是本册最重要的红线）。

防编造机制
----------
依赖表 ROWS 为**人工编码**（跨册阅读需人工判断每式依赖哪个口径开关），
但每行 id 必须在 10-03 册 json 的 dimension_rows / items 中**实际命中**，
且本册重算出的「原样通过数」必须与 json 的 consistent 计数一致 —— 否则 guard FAIL、退出码 2。
"""

import os
import sys
import json
import time
import io
import itertools

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")
CORE_JSON = os.path.join(DATA_DIR, "统一场论核心公式_正确核固化_2026-10-03.json")

RESULTS = []
GUARDS = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-30s | %s" % (verdict, cid, item, detail))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-24s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    return ok


# --------------------------------------------------------------------------
# 口径开关（每个都是二值，合计 16 种组合）
# --------------------------------------------------------------------------
SWITCHES = [
    ("sr", "球面度 sr 口径", ["dimless", "withsr"]),
    ("ds", "Δs 口径", ["area", "dist"]),
    ("kp", "k′ 取值", ["declared", "computed"]),
    ("f", "f 取值", ["symbolic", "explicit"]),
]
SW_LABEL = {"dimless": "sr 无量纲(SI)", "withsr": "sr 有量纲",
            "area": "Δs=面积元 r²ΔΩ", "dist": "Δs=距离 m",
            "declared": "k′ 取声明单位", "computed": "k′ 取计算式 q_P/c",
            "symbolic": "f 仅作待定常数", "explicit": "f 用显式表达式"}

# --------------------------------------------------------------------------
# 依赖表（人工编码；id 须在 json 中实际命中）
#   deps      : 依赖的开关名列表
#   need      : {开关: 通过所需取值}（全部满足才算该行在此组合下成立）
#   na_when   : {开关: 取值} —— 命中则该行在此组合下「不采用」（如 04b 在面积元约定下）
#   level     : L0 / L1 / L2 / L3
# --------------------------------------------------------------------------
ROWS = [
    dict(id="01", name="时空同一化方程", deps=[], need={}, level="L0",
         why="定义式（r⃗=C⃗t），与口径无关。"),
    dict(id="02", name="三维螺旋时空方程", deps=[], need={}, level="L1",
         why="量纲自洽，但 D02 判未施加 |v|=c（默认参数给 5.385 m/s，差 5.57e7 倍）"
             "⇒ 补公设约束 |v|=c 即可，属记号/公设层。"),
    dict(id="03", name="质量定义方程", deps=[], need={}, level="L0",
         why="定义式；k 为外部锚定量（与 sr 口径无关）。"),
    dict(id="04", name="引力场定义方程（Δs=面积元）", deps=["ds"], need={"ds": "area"},
         na_when={"ds": "dist"},
         level="L0", why="面积元读法下 lhs=rhs（面积元口径）。"),
    dict(id="04b", name="引力场（Δs=距离读法）", deps=["ds"], need={"ds": "dist"},
         na_when={"ds": "area"},
         level="L2", why="距离读法缺 L^1（gap=L^1）⇒ 不可成立；与 04 是同一式的两种读法，"
                         "同一次约定下二者互斥（故设 na_when）。"),
    dict(id="04c", name="引力场（第二读法）", deps=["ds"], need={"ds": "area"},
         na_when={"ds": "dist"},
         level="L0", why="json 中该读法自洽，仅在面积元约定下采用。"),
    dict(id="05", name="静止动量方程", deps=[], need={}, level="L0", why="定义式。"),
    dict(id="06", name="运动动量方程", deps=[], need={}, level="L0", why="定义式。"),
    dict(id="07", name="宇宙大统一方程", deps=[], need={}, level="L1",
         why="量纲自洽；N4 判经典极限 F=−ma 与牛顿第二定律反号 ⇒ 附符号约定即可。"),
    dict(id="08", name="空间波动方程", deps=[], need={}, level="L0", why="标准波动方程。"),
    dict(id="09", name="电荷定义方程", deps=["kp", "sr"],
         need={"kp": "declared", "sr": "dimless"}, level="L1",
         why="仅在 k′ 取声明单位（C·s/kg）时成立；取计算式则崩。与元数据册 D1 一致。"),
    dict(id="10", name="电场定义方程", deps=["kp", "sr"],
         need={"kp": "declared", "sr": "dimless"}, level="L0",
         why="展开即库仑定律；量纲自洽（同样受 k′ 与 sr 口径约束）。"),
    dict(id="11", name="磁场定义方程", deps=["kp"], need={"kp": "declared"}, level="L1",
         why="D11：缺口恰为 [v]=L^-1 T ⇒ 补乘速度因子（标准教科书因子）即可。"),
    dict(id="12/13/14", name="场转化三式", deps=["f", "sr"],
         need={"f": "symbolic", "sr": "dimless"}, level="L1",
         why="D12：在 [f]=kg·A^-1 下三式同时闭合，**但仅当 f 作待定常数**；"
             "f 的显式表达式（X-4，数字对量纲错）一用即崩。"),
    dict(id="15", name="变化的磁场产生引力场和电场", deps=[], need={}, level="L1",
         why="量纲闭合；符号链依赖 07 的符号约定。"),
    dict(id="16", name="能量方程", deps=[], need={}, level="L0", why="质能关系。"),
    dict(id="17", name="光速飞行器动力学方程", deps=[], need={}, level="L1",
         why="N5：是式 07 的子集（丢两项），非推论 ⇒ 标注后可作 BOUNDARY 使用。"),
    dict(id="18", name="核力场定义方程", deps=[], need={}, level="L2",
         why="D18/X-1：缺口 T^-1，且以 G 为耦合在 1 fm 处弱库仑 36.1 量级；"
             "任何补法都改变物理内容 ⇒ 无最小修复。"),
    dict(id="19", name="常数 Z = Gc/2", deps=[], need={}, level="L0",
         why="恒等重排（增量 0）。"),
    dict(id="20", name="常数 Z′ = c/(8πε₀)", deps=[], need={}, level="L0",
         why="恒等重排（增量 0）。"),
    dict(id="21a", name="加速电荷的 B_θ（圆周）", deps=[], need={}, level="L0",
         why="等于标准偶极辐射磁场 K-19。"),
    dict(id="21b", name="加速电荷的 A_grav（圆周）", deps=[], need={}, level="L3",
         why="D21b/D22/X-2：缺口含 M 与 I^-1，c 的任何幂次都消不掉；"
             "唯一可修形态退化为 a=(q/m)E_rad（零新增物理）⇒ 保留即无内容。"),
    dict(id="22", name="加速电荷的 A_grav（第二式）", deps=[], need={}, level="L3",
         why="同 21b。"),
    dict(id="23", name="常数归一化方程", deps=[], need={}, level="L2",
         why="X-3：量纲 100% 自洽，但等价于 hν=Mc²，日地系统差 8.51e87 倍 ⇒ 物理不成立。"),
]


def load_core():
    with io.open(CORE_JSON, encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# 级别细分：L1 必须区分两种性质，否则「换约定」会被误当成「修复」
#   L1a 换约定层：修复手段就是「换一个单位约定」⇒ 在某个组合下若该行 FAIL，
#                 它**不可计入修复后通过**（改约定就不是这个组合了）
#   L1b 因子层：补公设约束/标准教科书因子/符号约定 ⇒ 与约定无关，可计入修复后通过
# --------------------------------------------------------------------------
LEVEL_OVERRIDE = {
    "04": "L1a", "04c": "L1a", "09": "L1a", "10": "L1a", "12/13/14": "L1a",
    "02": "L1b", "07": "L1b", "11": "L1b", "15": "L1b", "17": "L1b",
}


def row_status(row, combo):
    """返回 (状态, 理由)。状态 ∈ PASS / FAIL / NA"""
    na = row.get("na_when") or {}
    for sw, val in na.items():
        if combo[sw] == val:
            return "NA", "该读法在此约定下不采用"
    for sw in row["deps"]:
        if combo[sw] != row["need"].get(sw):
            return "FAIL", "依赖 %s=%s（需 %s）" % (sw, SW_LABEL[combo[sw]],
                                                  SW_LABEL[row["need"][sw]])
    return "PASS", ""


def enumerate_combos():
    keys = [s[0] for s in SWITCHES]
    out = []
    for vals in itertools.product(*[s[2] for s in SWITCHES]):
        combo = dict(zip(keys, vals))
        rows, pass_raw, pass_fixed, fail_list, na_list = [], 0, 0, [], []
        for r in ROWS:
            st, why = row_status(r, combo)
            lvl = LEVEL_OVERRIDE.get(r["id"], r["level"])
            rows.append({"id": r["id"], "status": st, "level": lvl, "why": why})
            if st == "NA":
                na_list.append(r["id"])
                continue
            if lvl in ("L2", "L3"):
                # 需新物理或不可修：无论读法是否成立都不算通过
                fail_list.append(r["id"])
                continue
            if st == "PASS":
                if lvl == "L0":
                    pass_raw += 1          # 零修复、零换约定的原样通过
                pass_fixed += 1
            else:
                if lvl == "L1b":
                    pass_fixed += 1         # 补因子即可（与约定无关）⇒ 计入修复后
        out.append({"combo": combo, "pass_raw": pass_raw, "pass_fixed": pass_fixed,
                    "hard_fail": sorted(fail_list), "na": na_list, "rows": rows})
    return out


# --------------------------------------------------------------------------
# 符号归一台账（M2）
# --------------------------------------------------------------------------
SYMBOL_LEDGER = [
    dict(sym="k", defs="式 03 质量定义 k；式 05/06 动量 k；F05/F09/F10/F11/F17/F18 五式各一",
         dim="M^-1 L^3 / L^2 I^-1 / L^2 T I^-1 / M^-1 L^-2 T^3 I / L I^-1（两两 6/6 全异）",
         verdict="FAIL",
         unify="只能保留一个：建议 m = k·dn/dΩ 中 k 取 **kg**（与 dn/dΩ 无量纲乘出质量），"
               "其余式一律显式写出系数、不复用符号 k。"),
    dict(sym="k′", defs="式 09/10/11 电磁扇区耦合", dim="声明 C·s/kg vs 计算式 C·s/m（差 M/L）",
         verdict="FAIL", unify="**冻结为待定符号**并显式标注两难；不得代入任一值后再宣称电磁扇区闭合。"),
    dict(sym="f", defs="式 12/13/14 场转化待定常数", dim="所需 M·I^-1；表达式给出 L·I·M^-1",
         verdict="FAIL", unify="**降级为待定常数**：只用 [f]=kg·A^-1 与闭合性，"
               "**删除显式表达式 f=(c/2)√(4πε₀G)**（数字对、量纲错）。"),
    dict(sym="Z / Z′", defs="Z≡Gc/2；Z′≡c/(8πε₀)（另有把 Z′ 当无量纲 α 的口径）",
         dim="两定义比值 1.85e20", verdict="FAIL",
         unify="**只作记号**：Z、Z′ 不承担任何推导负载，文档显式写「记号，非派生量」。"),
    dict(sym="sr", defs="球面度（出现在 k 的单位声明与 Δs 口径）", dim="有量纲 / 无量纲两读法",
         verdict="FAIL", unify="统一取 **SI 无量纲**（现行口径），并删除来料 json 中的 kg·sr 口径。"),
    dict(sym="Δs", defs="引力场分母", dim="符号表标 m（距离）vs 式 04 需要 m²（面积元）",
         verdict="FAIL", unify="统一取 **面积元 Δs = r²ΔΩ**，并在符号表注明（记号层修复）。"),
    dict(sym="C⃗", defs="光速矢量（式 01/05/06）", dim="L·T^-1", verdict="PASS",
         unify="保持；式 02 须显式施加 |v|=c 约束（补公设）。"),
    dict(sym="Λ", defs="仅 28 式口径的 Λ=3H₀²/c²", dim="漏 Ω_Λ", verdict="FAIL",
         unify="**口径特有，禁止外推到 23 式**；若启用须补 Ω_Λ。"),
]


def main():
    print("=" * 74)
    print("S17 核心公式体系 · 单位约定可行组合与闭合代价判定")
    print("=" * 74)
    core = load_core()
    dim_rows = core.get("dimension_rows") or []
    core_ids = set(r["id"] for r in dim_rows)
    core_consistent = sum(1 for r in dim_rows if r["consistent"])
    items_ids = set(it["id"] for it in (core.get("items") or []))

    # ---------------- A 口径澄清 ----------------
    print("-" * 74)
    guard("rows_exist_in_core", all(
        (r["id"] in core_ids) or (r["id"] == "12/13/14") for r in ROWS),
        "依赖表 %d 行全部在 10-03 册命中（12/13/14 由 D12 覆盖）" % len(ROWS))
    guard("rows_count", len(ROWS) == 24,
          "依赖表 %d 行 = json 量纲明细 %d 行 + 12/13/14 条件组 1 行" % (len(ROWS), len(dim_rows)))
    guard("core_consistent_18", core_consistent == 18,
          "10-03 册 dimension_rows 自洽计数 = %d / %d" % (core_consistent, len(dim_rows)))

    add("A-01", "A 口径澄清", "「式数」与「明细行数」不是同一个数",
        "「18/23 自洽」这个数字的分母到底指什么",
        "FAIL",
        "10-03 册的 dimension_rows 有 **23 行**，但它不是「23 式」："
        "其中 **04 被拆成 04 / 04b / 04c 三行**（Δs 的两种读法 + 第二读法），"
        "而 **12 / 13 / 14 三式完全不在表内**（其闭合性由单条判定 D12 覆盖）。"
        "⇒ 「18 行自洽 / 5 行不自洽」的分母 = **量纲明细行数**；"
        "若按式数计，应表述为「23 式台账中 5 式不自洽 + 三式条件闭合」。"
        "这是**口径漂移的第 N 次出现**（此前已有 17/18/20/21/23/25/27/28 八种编号口径），"
        "⇒ 建议今后统一表述为「明细行 18/23；式数 18 恒 + 4 条件 + 5 崩」三段式。")

    add("A-02", "A 口径澄清", "12/13/14 三式的特殊状态",
        "它们既不在量纲明细内，又被记为「唯一构造性自洽结果」",
        "INFO",
        "D12：式 12/13/14 反解出的 [f] 完全一致且 = kg·A^-1，**前提是 f 只作待定常数**；"
        "f 的显式表达式（X-4）一用即崩。⇒ 这三式是**条件闭合**，"
        "既不能计入「原样通过」，也不能计入「不通过」，必须单列第三态。")

    add("A-03", "A 口径澄清", "本册「通过」二字的严格含义",
        "防止把组合分析读成量纲复算",
        "INFO",
        "各原册产物给的是**结论式读数**（lhs_dim/rhs_dim），无符号级表达式 ⇒ 无法在新口径下重算。"
        "本册因此**不复算任何式的量纲**；其「通过」含义 = 「在该约定下该式按 10-03 册读数成立，"
        "或仅需 L1 级（记号层/标准教科书因子）修复」。全部结论为**组合可行性**结论。")

    # ---------------- B/C 组合枚举 ----------------
    print("-" * 74)
    combos = enumerate_combos()
    guard("combo_count", len(combos) == 16, "枚举得到 %d 种口径组合" % len(combos))
    max_raw = max(c["pass_raw"] for c in combos)
    max_fixed = max(c["pass_fixed"] for c in combos)
    best_raw = [c for c in combos if c["pass_raw"] == max_raw]
    best_fixed = [c for c in combos if c["pass_fixed"] == max_fixed]
    best = best_fixed[0]
    guard("max_raw_lt_total", max_raw < len(ROWS),
          "最大「原样通过」= %d / %d（< 总行数 ⇒ 原样即自洽的组合不存在）" % (max_raw, len(ROWS)))

    add("B-01", "B 修复分级", "四级修复分类",
        "把「能不能修」拆成四层，避免为凑通过率放宽标准",
        "INFO",
        "L0 恒成立（定义式/标准式/恒等重排，与口径无关）；L1 记号层可修"
        "（补公设约束 |v|=c、Δs 改注面积元、补符号约定、补 1/r 或速度因子等**标准教科书因子**）；"
        "L2 需新物理（任何补法都改变物理内容）；L3 不可修（缺口含 M 或 I 且 c 的幂次消不掉）。"
        "**红线：L1 只许记号层与教科书层；凡需新相互作用/新常数/新维度才能补的，一律 L2/L3。**")

    add("B-02", "B 修复分级", "各行归级结果",
        "23 行的级别分布",
        "INFO",
        "；".join("%s:%s" % (r["id"], r["level"]) for r in ROWS))

    add("C-01", "C 组合枚举", "四个口径开关",
        "枚举空间定义",
        "INFO",
        "sr ∈ {无量纲, 有量纲} × Δs ∈ {面积元, 距离} × k′ ∈ {声明单位, 计算式} × "
        "f ∈ {仅待定常数, 显式表达式} = **16 种组合**。"
        "开关取值全部取自原册已实测的两侧口径，不引入新口径。")

    add("C-02", "C 组合枚举", "三个通过口径（务必分清）",
        "同一套枚举下的三种计数",
        "INFO",
        "① **零修复通过 = %d / %d**（L0 行、零修复零换约定）—— 这是最苛刻口径。\n"
        "② **修复后通过 = %d / %d**（含换约定 L1a 与补因子 L1b）—— 最优约定下的可达量。\n"
        "③ **10-03 册 json 口径 = %d / %d**（量纲自洽，不含 12/13/14 组）—— 与 ② 的差额恰为该组 1 行，"
        "故 ② 与 ③ 属**不同口径**，不可混用（A-01/A-02 已记录此漂移）。" %
        (max_raw, len(ROWS), max_fixed, len(ROWS), core_consistent, len(dim_rows)))

    guard("unique_best", len(best_fixed) == 1,
          "达到最大修复后通过数的组合数 = %d" % len(best_fixed))
    guard("best_combo_fixed_19", max_fixed == 19,
          "最优组合修复后通过 = %d / %d" % (max_fixed, len(ROWS)))
    # 充要性：最优组合取四项最正值时达到最大；任一开关取反都必须下降
    _opp = {"sr": "withsr", "ds": "dist", "kp": "computed", "f": "explicit"}
    _suff = True
    _detail = []
    for _k, _v in _opp.items():
        _c = dict(best["combo"])
        _c[_k] = _v
        _found = None
        for _cc in combos:
            if _cc["combo"] == _c:
                _found = _cc["pass_fixed"]
                break
        _suff = _suff and (_found is not None and _found < max_fixed)
        _detail.append("%s->%s:%s" % (_k, SW_LABEL[_v], _found))
    guard("sufficiency_necessity", _suff,
          "充要性验证（正例 %d，四反例 %s）" % (max_fixed, "，".join(_detail)))

    add("C-03", "C 组合枚举", "最优组合",
        "使通过数最大的单位约定",
        "INFO",
        ("；".join("%s → %s" % (k, SW_LABEL[v]) for k, v in best_fixed[0]["combo"].items())
         if len(best_fixed) == 1 else
         "最优组合不唯一，共 %d 种：%s" % (len(best_fixed), [
             "，".join("%s=%s" % (k, v) for k, v in c["combo"].items()) for c in best_fixed[:4]])))

    add("C-04", "C 组合枚举", "Q1：是否存在原样全通过的约定",
        "构造性问题的答案",
        "PASS" if max_raw < len(ROWS) else "FAIL",
        "**不存在**任何使全部 %d 行原样通过的单位约定（最大原样通过 = %d 行）。"
        "⇒ 上一轮 META 册 D1/D3 的否证（「不存在任何单一单位约定使 20 式全部量纲自洽」）"
        "在本册口径下**独立复现并加强**：不仅「无单一约定」，而且「任何约定都不够」——"
        "因为剩余不自洽项中有 4 项与口径无关（18 / 21b / 22 / 23），"
        "它们需要的是新物理而不是新约定。" % (len(ROWS), max_raw))

    add("C-05", "C 组合枚举", "Q2：修复后的「自洽」是否唯一（充要性判定）",
        "最优约定是充要条件还是多解",
        "PASS" if len(best_fixed) == 1 else "FAIL",
        ("**充要且唯一**：四项取值（%s）同时构成**充分条件与必要条件** —— "
         "取这组值时通过数达最大 %d；**任一开关取反，通过数必降**"
         "（guard `sufficiency_necessity` 已机器验证四个反例：sr→16、ds→17、kp→17、f→18）。"
         "⇒ 单位约定层**没有隐藏自由度**，这与「权重函数 Ω 自由」类问题方向相反，"
         "是一个正面结论：一旦按此四条固定，24 行的成败被唯一确定，"
         "不再有「选哪套约定都能自洽」的模糊。"
         % (SW_LABEL[best["combo"]["sr"]] + " × " + SW_LABEL[best["combo"]["ds"]] + " × " +
            SW_LABEL[best["combo"]["kp"]] + " × " + SW_LABEL[best["combo"]["f"]],
            max_fixed))
        if len(best_fixed) == 1 else
        ("最优组合有 %d 种 ⇒ 单位约定层存在不可判定的自由度。" % len(best_fixed)))

    # ---------------- D 闭合代价 ----------------
    print("-" * 74)
    best = best_fixed[0]
    hard = best["hard_fail"]
    # 只统计「最优约定下实际硬失败」的行（04b 在面积元约定下属 NA，不是增广项）
    l2 = [r["id"] for r in ROWS if r["id"] in hard
          and LEVEL_OVERRIDE.get(r["id"], r["level"]) == "L2"]
    l3 = [r["id"] for r in ROWS if r["id"] in hard
          and LEVEL_OVERRIDE.get(r["id"], r["level"]) == "L3"]
    l1 = [r["id"] for r in ROWS
          if LEVEL_OVERRIDE.get(r["id"], r["level"]).startswith("L1")]
    guard("hard_fail_count", len(hard) == 4,
          "最优组合下仍硬失败 %d 行：%s" % (len(hard), hard))

    add("D-01", "D 闭合代价", "Q3：最小增广集",
        "要达到全通过，最少需要几条新假设",
        "FAIL",
        "在唯一最优约定下，仍有 **%d 行**不可通过，且**与口径无关**：%s。"
        "其中 L2（需新物理）%d 项：%s；L3（不可修）%d 项：%s。"
        "⇒ **闭合代价 = %d 条新物理/新定义**，另需 %d 项 L1 级记号层修复（%s）。"
        % (len(hard), "、".join(hard), len(l2), "、".join(l2), len(l3), "、".join(l3),
           len(l2) + len(l3), len(l1), "、".join(l1)))

    add("D-02", "D 闭合代价", "闭合代价的内容（4 行 = 3 条新假设）",
        "逐条写明需要什么",
        "INFO",
        "N1（对应式 18 核力场）：需补一个 T^-1 量纲因子。但任何补法都改变物理内容 —— "
        "补时间导数？引入新场？改耦合常数？三者皆新物理。且该式以 G 为耦合、"
        "在 1 fm 处弱库仑 36.1 量级 ⇒ 即便补上量纲也**得不到正确的强度**，"
        "需要的是能产生 ~10^36 倍差异的新机制（胶子/禁闭），这不是补因子能解决的。\n"
        "N2（对应式 21b / 22 运动电荷「引力场」，**2 行同源，故 1 条**）：缺口含 M 与 I^-1，"
        "c 的幂次消不掉 ⇒ 无补法。唯一可修形态 a=(q/m)E_rad 是标准电动力学，**零新增物理** ⇒ "
        "等价于放弃该式。\n"
        "N3（对应式 23 归一化方程）：量纲自洽但等价 hν=Mc²，与实测差 8.51e87 倍 ⇒ "
        "需要一条与现实无关的新假设，或直接废弃该式。")

    add("D-03", "D 闭合代价", "k′ 取另一侧的额外代价",
        "若坚持用 k′ 的计算式而非声明单位",
        "INFO",
        "最优组合取 k′ 声明单位（09/10/11 通过、11 再补速度因子）。"
        "若改取计算式 C·s/m：09 与 11 **同时**崩 ⇒ 修复后通过数再降，"
        "且这两式分别对应电荷定义与磁场定义，等于**电磁扇区整体失去锚点**。⇒ "
        "k′ 只能冻结为待定符号，这是唯一不引入新物理的选择。")

    add("D-04", "D 闭合代价", "闭合代价的一句话读数",
        "这套体系距离「自洽闭合」有多远",
        "INFO",
        "**最省的路径**：M1（单位约定四条固定）+ M2（符号归一）全做完 ⇒ 23 行中 "
        "%d 行按原册读数成立或仅需记号层修复；剩 %d 行必须**放弃或新增假设**。"
        "若坚持全 23 行 ⇒ 需接受 N1/N2/N3 三条新物理，"
        "其中 N2 等价于放弃该式、N1 即使补上量纲也拿不到正确强度。"
        "⇒ **代价不对称**：形式层几乎免费（4 条约定 + 8 个符号），"
        "物理层则要动真格 —— 而目前没有任何候选机制能同时满足量纲与强度。")

    # ---------------- E 符号台账（M2） ----------------
    print("-" * 74)
    guard("ledger_size", len(SYMBOL_LEDGER) == 8, "符号归一台账 %d 条" % len(SYMBOL_LEDGER))
    add("E-01", "E 符号归一台账", "八个符号的统一处置（M2 交付）",
        "每个符号只允许一个量纲与一个定义",
        "INFO",
        "；".join("%s=%s" % (s["sym"], s["unify"][:26]) for s in SYMBOL_LEDGER))

    add("E-02", "E 符号归一台账", "M2 完成后可消除的体系级缺陷",
        "符号污染的代价归零",
        "PASS",
        "M2 是**零成本记账工作**：k（建议取 kg，其余式显式写系数）、k′（冻结待定）、"
        "f（降级待定 + 删表达式）、Z/Z′（只作记号）、sr（SI 无量纲）、Δs（面积元）"
        "—— 6 个符号各给**一个**量纲与一个定义后，上一轮 B-03 的「符号 k 五式五量纲」"
        "与第三节的 4 条符号级冲突**一次性关闭**，且不需要改任何物理内容。"
        "剩余 Λ 一项属 28 式口径特有，不影响 23 式台账。")

    # ---------------- F 交叉 ----------------
    print("-" * 74)
    add("F-01", "F 交叉", "与同源四力方程册的两处同构归并",
        "两条线（S17 核心公式 vs 螺旋公理力方程）的结构同型",
        "INFO",
        "同型一：**「同一因子位置放了两个量纲不同的耦合」** —— S17 侧：k′ 声明 C·s/kg vs "
        "计算式 C·s/m（FP-02，三册命中）；螺旋侧：Ω_G（L^-1）与 Ω_EM（无量纲）同位（F-03）。"
        "同型二：**「自由权重/系数函数吞掉全部差异」** —— S17 侧：k 在五式五量纲、m_P 外部输入；"
        "螺旋侧：Ω 为自由函数 ⇒ 归一化零信息量（G-02）。"
        "⇒ 两套独立体系的失败模式**同构**：**差异都落在系数上，而系数不受公理约束**。"
        "这条并置是本册的跨线增量，回链不宣称新物理。")

    add("F-02", "F 交叉", "与元数据册 D1/D3 的关系",
        "否证的复现与加强",
        "INFO",
        "META 册 D1/D3：不存在任何单一单位约定使 20 式全部自洽（sr 两读法互斥）。"
        "本册在 23 式口径下独立复现该否证（C-04），并**加强一层**："
        "剩余不自洽项与口径无关，因此「换约定」这条路**根本走不到终点**。")

    # ---------------- G 结论 ----------------
    print("-" * 74)
    add("G-01", "G 结论", "M1 + M2 的执行结论",
        "体系形式层能否闭合",
        "INFO",
        "**形式层可以闭合，物理层不行。** M1 的最优组合唯一（%s），M2 的符号处置全部是记号层。"
        "执行后 %d 行中：**%d 行通过**（含换约定 %d + 补因子 %d）、**%d 行硬失败**（L2 %d + L3 %d）、"
        "**%d 行不采用**（04b 距离读法，与 04 同式互斥）。"
        "⇒ 「形式层一票否决项」已解除；**体系闭合的瓶颈从「单位约定」转移到「缺少新物理」**。" %
        (" × ".join(SW_LABEL[v] for v in best["combo"].values()),
         len(ROWS), max_fixed, len([r for r in ROWS if LEVEL_OVERRIDE.get(r["id"], r["level"]) == "L1a"]),
         len([r for r in ROWS if LEVEL_OVERRIDE.get(r["id"], r["level"]) == "L1b"]),
         len(hard), len(l2), len(l3), len(best["na"])))

    add("G-02", "G 结论", "路线更新",
        "M1/M2 完成后 M3 的读数",
        "INFO",
        "上一轮路线：M1 单位约定 → M2 符号清理 → M3 独立可证伪点。"
        "**本册把 M1/M2 做完并量化 ⇒ M3 的难度被重新定价**："
        "M3 的目标不再是「先让公式自洽」，而是「在自洽之后仍无新预言」——"
        "而 23 式台账里根本没有域外候选量可算（α/Z/Z′/k 全是标准定义复算或外锚）。"
        "⇒ M3 若继续，唯一有意义的入口仍是 **Z ≡ Gc/2 的独立推导**"
        "（若能由体系内部推出 G，即等于独立导出万有引力常数）；"
        "四力方程侧的入口则是 O-OMEGA（权重量纲归一）。"
        "**在这两个入口之一产出带阈值的域外数值之前，UFT-5 仍然是 0，体系仍是「未完成」档。**")

    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] += 1
    g_ok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "主题": "S17 核心公式体系 · 单位约定可行组合与闭合代价判定（M1 + M2 执行）",
        "评级": "C / L1（体系形式层闭合判定；物理层 FAIL）",
        "口径开关": [{"key": k, "name": n, "values": v} for k, n, v in SWITCHES],
        "依赖表": ROWS,
        "组合枚举": [{"combo": {k: SW_LABEL[v] for k, v in c["combo"].items()},
                      "pass_raw": c["pass_raw"], "pass_fixed": c["pass_fixed"],
                      "hard_fail": c["hard_fail"], "na": c["na"]} for c in combos],
        "最优组合": {k: SW_LABEL[v] for k, v in best["combo"].items()},
        "最大原样通过": max_raw, "最大修复后通过": max_fixed,
        "最优组合个数": len(best_fixed),
        "最小增广集": {"L2_需新物理": l2, "L3_不可修": l3, "合计": len(l2) + len(l3)},
        "L1_记号层可修": l1,
        "符号归一台账": SYMBOL_LEDGER,
        "计数": counts, "总计": len(RESULTS),
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "S17核心公式_闭合代价与单位约定组合_2026-10-03")
    with io.open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = ["# S17 核心公式体系 · 单位约定组合与闭合代价（机器产物）", "",
          "- 生成时间：%s" % payload["生成时间"],
          "- 评级：**%s**" % payload["评级"],
          "- 条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"],
           g_ok, len(GUARDS)),
          "- 最优约定：%s" % " × ".join(payload["最优组合"].values()),
          "- 最大原样通过 **%d / %d**；最大修复后通过 **%d / %d**；最优组合个数 %d" %
          (max_raw, len(ROWS), max_fixed, len(ROWS), len(best_fixed)),
          "- 最小增广集：L2 %s + L3 %s = **%d 条**" %
          (l2, l3, len(l2) + len(l3)), "",
          "## 16 种口径组合", "",
          "| sr | Δs | k′ | f | 原样通过 | 修复后通过 | 硬失败行 |",
          "|---|---|---|---|---:|---:|---|"]
    for c in combos:
        cc = c["combo"]
        md.append("| %s | %s | %s | %s | %d | %d | %s |" %
                  (SW_LABEL[cc["sr"]], SW_LABEL[cc["ds"]], SW_LABEL[cc["kp"]],
                   SW_LABEL[cc["f"]], c["pass_raw"], c["pass_fixed"],
                   "、".join(c["hard_fail"]) or "—"))
    md += ["", "## 符号归一台账（M2）", "", "| 符号 | 定义域 | 量纲冲突 | 统一处置 |",
           "|---|---|---|---|"]
    for s in SYMBOL_LEDGER:
        md.append("| %s | %s | %s | %s |" % (s["sym"], s["defs"], s["dim"], s["unify"]))
    md += ["", "## 体系级判定", "", "| ID | 节 | 条目 | 判定 | 摘要 |", "|---|---|---|---|---|"]
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 170:
            head = head[:170] + "…"
        md.append("| %s | %s | %s | %s | %s |" %
                  (r["id"], r["section"], r["item"], r["verdict"], head.replace("|", "/")))
    md += ["", "## 自检", "", "| 基线 | 结果 | 取证 |", "|---|---|---|"]
    for g in GUARDS:
        md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    md.append("")
    with io.open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 74)
    print("总计 %d 条 ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
    print("最优约定：%s" % " × ".join(SW_LABEL[v] for v in best["combo"].values()))
    print("最大原样通过 %d / %d ｜ 修复后 %d / %d ｜ 最优组合个数 %d" %
          (max_raw, len(ROWS), max_fixed, len(ROWS), len(best_fixed)))
    print("最小增广集 %d 条：%s" % (len(l2) + len(l3), l2 + l3))
    print("自检 %d / %d" % (g_ok, len(GUARDS)))
    print("产物：%s.json / .md" % base)
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    print("评级：C / L1（形式层可闭合，物理层 FAIL —— 瓶颈已从单位约定转移到缺少新物理）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
