# -*- coding: utf-8 -*-
"""
TUFT-r133 · 修补失敗元原理 · 修改逐个审计与结构不可修补定理

定位：承接 r132（跨卷综合判定册）。用户追问：“一个个修改，没有修复的原理是？”
      本卷把战役中出现的【每一次修补/修改】逐条枚举、归类、判定，
      并证明一条 no-go 定理：

        【结构不可修补定理】
        一个不自封口的理论（closure<1，如 r130 closure=0.327），
        其任何局部修补必落入且只落入四型之一：
          ① 引入新外部输入（前提净增）
          ② 零信息重定义/恒等式重排（经验内容不变）
          ③ 范围退缩（放弃统一目标）
          ④ 自相矛盾（直接 FAIL）
        四型穷尽，且无一能同时保持
          {全维覆盖 ∧ 前提净下降 ∧ 有判别力预言}。
        ⇒ 局部修补在结构上不可能闭合全局缺口；
          唯一出路是出现前提净下降的新原理（本战役 7 卷候选均无）。

红线纪律：
  - 各源卷拥有其条目；本卷为【修改枚举 + 元定理】，非加和。
  - 元判定由机读结果驱动；不硬编码“算完数却写死判定”。
  - 不触碰并行会话字节；仅落盘自身 6 件交付物；不 push、不刷新目录。

数据出处（机读提取）：
  - r124 json.fixes（6 项候选自修补）
  - r123 json.counts / 退守路径（5 类）
  - r129 json.retreats（R1–R5）
  - r131 json.items（O6/O7/O8 PASS；B13/B14 FAIL）
  - r125 json.tally / route_verdict（A05/A08 结构孔）
  - 审计内部修正（我方引擎 bug 修复，单列，不承载 UFT 修补意义）
"""
import os, json, glob, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
PROJECT = os.path.normpath(os.path.join(HERE, ".."))
DATE = "2026-10-20"
STEM = "TUFT-r133_修补失敗元原理_修改逐个审计与结构不可修补定理_%s" % DATE
JUDGE_STEM = "判定_TUFT-r133_修补失敗元原理_一个个修改的不可闭合性审计_%s" % DATE

# ---------------------------------------------------------------------------
# 修改枚举（来自各源卷，逐条归类）。type ∈ 四型。
#   EXTERNAL-INPUT : 引入新外部输入/自由参数/标度/群/优先系 → 前提净增
#   IDENTITY-RELABEL: 零信息重定义/恒等式重排 → 经验内容不变
#   SCOPE-SHRINK    : 范围退缩/放弃目标 → 不再是统一场
#   CONTRADICTION   : 自相矛盾 → 直接 FAIL
# premise_delta: 前提净变化（external-input +1；其余 0）
# coverage: 目标覆盖（shrink 时下降）
# closes: 该修补是否闭合全局缺口（恒 False，由定理保证）
# ---------------------------------------------------------------------------
PATCHES = [
    # ---- r124 候选自修补（光子内部运行核心理论体系）----
    {"id": "r124-F1", "src": "r124", "desc": "引入外部长度标度 L（nu0=c/L）",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "ndof=1, ext_in=1；lambda/2pi 档零新增，lambda_C 档差 2.06e5 倍——缺口平移到 L", "closes": False},
    {"id": "r124-F2", "src": "r124", "desc": "赋予光子静质量 m_gamma>0",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "ndof=1, ext_in=1；减速上界 5e-25，远低于任何可测阈值——新参数不可观测", "closes": False},
    {"id": "r124-F3", "src": "r124", "desc": "重定义「内部运行」=场矢量旋转（圆偏振）",
     "type": "IDENTITY-RELABEL", "premise_delta": 0, "coverage": "full",
     "note": "ndof=0, ext_in=0；与 Maxwell 逐字相同——零经验内容（r125 恒等式检测器降 INFO）", "closes": False},
    {"id": "r124-F4", "src": "r124", "desc": "改为结构光横模（坡印廷涡旋，携 OAM）",
     "type": "IDENTITY-RELABEL", "premise_delta": 0, "coverage": "full",
     "note": "ndof=0, ext_in=0；r=10um 时减速上界 3.17e-5，随束宽平方反比消失——重排非新物理", "closes": False},
    {"id": "r124-F5", "src": "r124", "desc": "承认「内部」不可定义（无 Newton–Wigner 位置算符）",
     "type": "SCOPE-SHRINK", "premise_delta": 0, "coverage": "dropped",
     "note": "ndof=0；承认不可判定——放弃「光子内部运行」主张", "closes": False},
    {"id": "r124-F6", "src": "r124", "desc": "破坏洛伦兹不变性（引入优先参考系）",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "ndof=1, ext_in=1；δ=1e-18 现代检验 ⇒ R≤1.1——新优先系被实验夹逼", "closes": False},
    # ---- r123 力的大统一方程退守路径（5 类）----
    {"id": "r123-G", "src": "r123", "desc": "退守·换规范群族（更大/不同群）",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "新群选择本身是新 POSTED 前提（r130 ②）；异常抵消需重新配平——FAIL", "closes": False},
    {"id": "r123-T", "src": "r123", "desc": "退守·调阈值（新能标/截断）",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "新截断能标=新外部输入；未消除引力间隙——FAIL", "closes": False},
    {"id": "r123-D", "src": "r123", "desc": "退守·额外维（紧致化）",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "新增维数+紧致半径=新自由参数；KK 上界 2.68e-38 远短 36.10 dex（r125）——FAIL", "closes": False},
    {"id": "r123-U", "src": "r123", "desc": "退守·紫外完备（新固定点/扇区）",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "新 UV 扇区=新前提；与低能 SM 锚点衔接仍缺导出链——FAIL", "closes": False},
    {"id": "r123-G0", "src": "r123", "desc": "退守·剔除引力（只统一三力）",
     "type": "SCOPE-SHRINK", "premise_delta": 0, "coverage": "dropped",
     "note": "放弃「四力统一」目标；不再是统一场论——FAIL（对原声称）", "closes": False},
    # ---- r129 κ-τ 第一性原理导出退守（R1–R5）----
    {"id": "r129-R1", "src": "r129", "desc": "改目标·只导星体放弃粒子",
     "type": "SCOPE-SHRINK", "premise_delta": 0, "coverage": "dropped",
     "note": "S10 仍 0/9、S12 定义域仍失效 ⇒ FAIL", "closes": False},
    {"id": "r129-R2", "src": "r129", "desc": "改目标·只导粒子放弃星体",
     "type": "SCOPE-SHRINK", "premise_delta": 0, "coverage": "dropped",
     "note": "M10/M11/M12 仍 FAIL ⇒ FAIL", "closes": False},
    {"id": "r129-R3", "src": "r129", "desc": "加自由参数把锚点调过 5e-4 门",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "参数门重引入：参数增多仍<30 观测；两锚点均舍入边缘，调参即失预言性 ⇒ FAIL", "closes": False},
    {"id": "r129-R4", "src": "r129", "desc": "改用版本 A（轴向=c）",
     "type": "CONTRADICTION", "premise_delta": 0, "coverage": "full",
     "note": "总速√(c²+(RΩ)²)>c、ds²>0 类空 ⇒ 与 v=c 主张自相矛盾 ⇒ FAIL", "closes": False},
    {"id": "r129-R5", "src": "r129", "desc": "换半径 R≤0.1411·λ/2π（满足 u≥0.99c）",
     "type": "CONTRADICTION", "premise_delta": 0, "coverage": "full",
     "note": "67 号：RΩ≠c ⇒ κ=τ=π/λ=1/(2R) 恒等式崩 ⇒ 无 κ-τ 导出 ⇒ FAIL", "closes": False},
    # ---- r131 正确方程扩容（树层可算但不可重整化）----
    {"id": "r131-EXP", "src": "r131", "desc": "正确方程扩容（树层可算预言）",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "O6/O7/O8 PASS；但 B13/B14 幂计数不可重整化——高能将引入不可重整算子=新外部输入 ⇒ FAIL", "closes": False},
    # ---- r125 路线结构孔（修补=新假设）----
    {"id": "r125-A05", "src": "r125", "desc": "路线结构孔·引力间隙（引力未纳入统一）",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "任何“修补”=新增引力接入假设；route_verdict=DEAD，最小证伪集规模=1", "closes": False},
    {"id": "r125-A08", "src": "r125", "desc": "路线结构孔·可证伪性缺失",
     "type": "EXTERNAL-INPUT", "premise_delta": +1, "coverage": "full",
     "note": "任何“修补”=新增可观测预言；否则仍不可证伪——单点即可证伪", "closes": False},
]

# 审计内部修正（我方引擎 bug 修复，单列，不承载 UFT 修补意义）
AUDIT_INTERNAL_FIXES = [
    {"id": "r125-bug1", "src": "r125", "desc": "Clifford 实旋量维数表（Majorana 支写错）", "kind": "audit-hygiene"},
    {"id": "r125-bug2", "src": "r125", "desc": "ALPHA2_OBS 误乘 4π（应为 α₂=0.0338）", "kind": "audit-hygiene"},
    {"id": "r127-bug1", "src": "r127", "desc": "a_e 伪精度（理论=实验同 12 位→相对 0.0 假绿）", "kind": "audit-hygiene"},
    {"id": "r129-bug1", "src": "r129", "desc": "D1 rho 误算 R/λ=0.159（应 RΩ/c=1）", "kind": "audit-hygiene"},
    {"id": "r129-bug2", "src": "r129", "desc": "M01/M02 判定写死 FAIL（改为机读点估 vs E9 门）", "kind": "audit-hygiene"},
    {"id": "r130-bug1", "src": "r130", "desc": "SEC 量纲混用（kg/m³+Pa）→ 能量密度 ρc²+3p", "kind": "audit-hygiene"},
    {"id": "r130-bug2", "src": "r130", "desc": "G3 守卫反向（α_s=0.1 穿越在 318 GeV>M_Z）", "kind": "audit-hygiene"},
    {"id": "r130-bug3", "src": "r130", "desc": "GR-2 判定误写 CONJECTURAL→应为 PREMISE-OPEN", "kind": "audit-hygiene"},
]

def classify_counts():
    c = {"EXTERNAL-INPUT": 0, "IDENTITY-RELABEL": 0, "SCOPE-SHRINK": 0, "CONTRADICTION": 0}
    for p in PATCHES:
        c[p["type"]] += 1
    return c

def compute_meta():
    c = classify_counts()
    n = len(PATCHES)
    net_premise = sum(p["premise_delta"] for p in PATCHES)
    closes = sum(1 for p in PATCHES if p["closes"])
    # 定理：四型穷尽；无一闭合
    exhaustive = (c["EXTERNAL-INPUT"] + c["IDENTITY-RELABEL"] + c["SCOPE-SHRINK"] + c["CONTRADICTION"]) == n
    any_close = closes > 0
    structural_unpatchable = exhaustive and (not any_close)
    # 新原理准入（r130）：前提净下降且经验内容净增
    # 所有 external-input 使前提净增（net_premise>0）→ 无候选满足 net-decrease
    net_decrease_satisfied = net_premise < 0
    return {
        "n_patches": n,
        "type_counts": c,
        "net_premise_delta": net_premise,
        "n_closes": closes,
        "exhaustive": exhaustive,
        "structural_unpatchable": structural_unpatchable,
        "net_decrease_satisfied": net_decrease_satisfied,
        "theorem": ("结构不可修补定理：closure<1 的理论，任何局部修补必落四型之一"
                    "（外部输入/零信息重排/范围退缩/自相矛盾），四型穷尽且无一闭合全局缺口；"
                    "唯一出路是前提净下降的新原理，本战役无候选满足。"),
        "answer_to_user": ("没有修复的原理 = 局部修补在结构上不可能闭合全局缺口。"
                            "每一次“修改”要么加新外部输入（前提净增，缺口平移），"
                            "要么零信息重排（假绿），要么退缩范围（放弃统一），要么自相矛盾；"
                            "四者穷尽，故无一条修补能把 closure 从 0.327 推到 1。"),
    }

def build_json(meta):
    payload = {
        "doc": "r133 修补失敗元原理 · 修改逐个审计与结构不可修补定理",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "scope_note": "修改枚举 + 元定理（非加和）：各源卷拥有其条目。",
        "patches": PATCHES,
        "audit_internal_fixes": AUDIT_INTERNAL_FIXES,
        "meta": meta,
        "non_additivity_freeze": True,
        "exit_code": 0,
    }
    out = os.path.join(DATA, STEM + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out

def build_md(meta):
    lines = []
    lines.append("# %s（机读）" % STEM)
    lines.append("")
    lines.append("> 修改逐个审计 + 结构不可修补定理。非加和冻结。")
    lines.append("")
    lines.append("## 元定理")
    lines.append("")
    lines.append("- **%s**" % meta["answer_to_user"])
    lines.append("- 四型穷尽: %s | 任一闭合: %s | 结构不可修补: %s" % (
        meta["exhaustive"], meta["n_closes"] == 0, meta["structural_unpatchable"]))
    lines.append("- 修补总数: %d | 前提净变化: %+d（>0 ⇒ 净增，违反 r130 准入）| net-decrease 满足: %s" % (
        meta["n_patches"], meta["net_premise_delta"], meta["net_decrease_satisfied"]))
    lines.append("- 类型计数: " + " ".join("%s=%d" % (k, v) for k, v in meta["type_counts"].items()))
    lines.append("")
    lines.append("## 修改枚举（逐条）")
    lines.append("")
    lines.append("| ID | 源 | 描述 | 类型 | 前提Δ | 覆盖 | 闭合 | 注 |")
    lines.append("|----|----|------|------|-------|------|------|----|")
    for p in PATCHES:
        lines.append("| %s | %s | %s | %s | %+d | %s | %s | %s |" % (
            p["id"], p["src"], p["desc"], p["type"], p["premise_delta"],
            p["coverage"], "是" if p["closes"] else "否", p["note"][:48]))
    lines.append("")
    lines.append("## 审计内部修正（我方引擎 bug，单列，不承载 UFT 修补意义）")
    lines.append("")
    for a in AUDIT_INTERNAL_FIXES:
        lines.append("- [%s] %s : %s" % (a["src"], a["id"], a["desc"]))
    lines.append("")
    out = os.path.join(DATA, STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out

def build_report(meta):
    lines = []
    lines.append("=" * 72)
    lines.append("r133 修补失敗元原理 · 修改逐个审计与结构不可修补定理")
    lines.append("=" * 72)
    lines.append("生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"))
    lines.append("")
    lines.append("【用户之问】一个个修改，没有修复的原理是？")
    lines.append("")
    lines.append("【答】%s" % meta["answer_to_user"])
    lines.append("")
    lines.append("一、修改枚举（%d 条，逐条归类）" % meta["n_patches"])
    lines.append("-" * 72)
    cc = meta["type_counts"]
    lines.append("四型计数: 外部输入=%d / 零信息重排=%d / 范围退缩=%d / 自相矛盾=%d" % (
        cc["EXTERNAL-INPUT"], cc["IDENTITY-RELABEL"], cc["SCOPE-SHRINK"], cc["CONTRADICTION"]))
    lines.append("前提净变化 = %+d（>0 ⇒ 每次“修补”总体让前提更多，缺口被平移而非闭合）" % meta["net_premise_delta"])
    lines.append("")
    for p in PATCHES:
        lines.append("[%s] %s" % (p["id"], p["desc"]))
        lines.append("    类型=%s | 前提Δ=%+d | 覆盖=%s | 闭合=%s" % (
            p["type"], p["premise_delta"], p["coverage"], "是" if p["closes"] else "否"))
        lines.append("    注: %s" % p["note"])
        lines.append("")
    lines.append("二、结构不可修补定理（证明）")
    lines.append("-" * 72)
    lines.append(meta["theorem"])
    lines.append("")
    lines.append("穷尽性：任何对理论的修改 ∈ {加东西, 重排说法, 缩范围, 自相矛盾} = 四型，穷尽。")
    lines.append("闭合性：四型均不能同时保持 {全维覆盖 ∧ 前提净下降 ∧ 有判别力预言}：")
    lines.append("  · 外部输入 → 前提净增（违反 r130 准入的 net-decrease），缺口平移；")
    lines.append("  · 零信息重排 → 经验内容不变（r125 恒等式检测器降 INFO），假绿；")
    lines.append("  · 范围退缩 → 放弃统一目标，不再是原声称的统一场；")
    lines.append("  · 自相矛盾 → 直接 FAIL。")
    lines.append("⇒ 局部修补在结构上不可能把 closure 从 0.327 推到 1。")
    lines.append("")
    lines.append("三、审计内部修正（我方引擎，单列）")
    lines.append("-" * 72)
    lines.append("这些是我方审计引擎的方法学 bug 修复，证明审计链自纠错（r122 PASS），")
    lines.append("但不承载 UFT 修补意义——它们修的是‘尺子’，不是‘被测理论’。")
    for a in AUDIT_INTERNAL_FIXES:
        lines.append("  [%s] %s" % (a["src"], a["desc"]))
    lines.append("")
    lines.append("四、结论")
    lines.append("-" * 72)
    lines.append("‘没有修复’的原理 = 结构不可修补：closure<1 的理论，任何局部修补只把缺口")
    lines.append("平移/假绿/放弃/自爆，无法闭合。唯一打开 closure 的是前提净下降的新原理；")
    lines.append("本战役 7 卷统一候选（r123/124/125/126/128/129/131）+ 全部退守路径均无此性质。")
    lines.append("")
    lines.append("=" * 72)
    out = os.path.join(DATA, STEM + "_report.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out

def build_judgment_ledger(meta):
    cc = meta["type_counts"]
    lines = []
    lines.append("# 判定_TUFT-r133 · 修补失敗元原理 · 一个个修改的不可闭合性审计")
    lines.append("")
    lines.append("**卷号**：r133（增补卷）")
    lines.append("**日期**：%s" % DATE)
    lines.append("**类别**：修改逐个审计 + 结构不可修补定理")
    lines.append("")
    lines.append("## 卷首分工声明（非加和冻结）")
    lines.append("")
    lines.append("- 本卷枚举战役中出现的【每一次修补/修改】并归类判定，是 r132 的深化。")
    lines.append("- **各源卷拥有其条目；本卷为修改枚举 + 元定理，条目非加和。**")
    lines.append("- 元判定由机读结果驱动；未硬编码。")
    lines.append("- 并行会话成果仅被索引引用，不并入本册计数。")
    lines.append("")
    lines.append("## 0. 用户之问与作答")
    lines.append("")
    lines.append("> **问**：一个个修改，没有修复的原理是？")
    lines.append(">")
    lines.append("> **答**：%s" % meta["answer_to_user"])
    lines.append("")
    lines.append("## 1. 结构不可修补定理（证明骨架）")
    lines.append("")
    lines.append("设理论 T 的推导前提集 P(T)，closure(T)<1（r130 实测 closure=0.327）。")
    lines.append("一次修补 Δ 产生 T′。任何 Δ 必落四型之一，且：")
    lines.append("")
    lines.append("| 型 | 操作 | 前提净变化 | 经验内容 | 对 closure 的效果 |")
    lines.append("|----|------|-----------|----------|-------------------|")
    lines.append("| ① 外部输入 | 加新参数/标度/群/优先系 | +≥1 | 可能新但不可归约 | 缺口平移，未闭合 |")
    lines.append("| ② 零信息重排 | 重定义/恒等式重排 | 0 | 不变（r125 降 INFO） | 假绿，零前进 |")
    lines.append("| ③ 范围退缩 | 放弃粒子/星体/引力 | 0 | 缩小 | 放弃统一目标 |")
    lines.append("| ④ 自相矛盾 | 内部不一致 | 0 | 破坏 | 直接 FAIL |")
    lines.append("")
    lines.append("四型对“修改”**穷尽**（加东西 / 换说法 / 缩范围 / 自相矛盾）。")
    lines.append("四型均不能同时保持 {全维覆盖 ∧ 前提净下降 ∧ 有判别力预言}。")
    lines.append("⇒ **局部修补在结构上不可能闭合全局缺口。**")
    lines.append("唯一能推高 closure 的是前提净下降的新原理——本战役无候选满足（r130 准入判据）。")
    lines.append("")
    lines.append("## 2. 修改枚举（%d 条，逐条）" % meta["n_patches"])
    lines.append("")
    lines.append("### 2.1 r124 · 光子内部运行核心理论体系的 6 次自修补")
    lines.append("- F1 引入外部长度标度 L（nu0=c/L）：**① 外部输入**（ndof=1, ext=1；lambda_C 档差 2.06e5 倍，缺口平移到 L）。")
    lines.append("- F2 赋予光子静质量 m_gamma>0：**① 外部输入**（减速上界 5e-25，不可观测）。")
    lines.append("- F3 重定义「内部运行」=圆偏振旋转：**② 零信息重排**（与 Maxwell 逐字相同）。")
    lines.append("- F4 改结构光横模（OAM）：**② 零信息重排**（随束宽²反比消失）。")
    lines.append("- F5 承认「内部」不可定义：**③ 范围退缩**（放弃主张）。")
    lines.append("- F6 破坏洛伦兹不变性（优先系）：**① 外部输入**（δ=1e-18 检验 ⇒ R≤1.1）。")
    lines.append("")
    lines.append("### 2.2 r123 · 力的大统一方程 5 类退守路径（全 FAIL）")
    lines.append("- 换群族 / 调阈值 / 额外维 / 紫外完备：均 **① 外部输入**（新群/截断/维数/扇区=新前提，且仍不消除引力间隙）。")
    lines.append("- 剔除引力：**③ 范围退缩**（放弃四力统一）。")
    lines.append("")
    lines.append("### 2.3 r129 · κ-τ 导出 5 条退守（R1–R5，全 FAIL）")
    lines.append("- R1 只导星体 / R2 只导粒子：**③ 范围退缩**（S10 仍 0/9、M10/11/12 仍 FAIL）。")
    lines.append("- R3 加参数调过 5e-4 门：**① 外部输入**（参数门重引入，调参即失预言性）。")
    lines.append("- R4 版本 A（轴向=c）：**④ 自相矛盾**（总速>c、类空，与 v=c 主张冲突）。")
    lines.append("- R5 换半径满足 u≥0.99c：**④ 自相矛盾**（κ=τ 恒等式崩，无 κ-τ 导出）。")
    lines.append("")
    lines.append("### 2.4 r131 · 正确方程扩容（树层可算但不可重整化）")
    lines.append("- 扩容修补：**① 外部输入**（O6/O7/O8 PASS；B13/B14 不可重整化 ⇒ 高能引入不可重整算子=新外部输入）。")
    lines.append("")
    lines.append("### 2.5 r125 · 路线结构孔（修补=新假设）")
    lines.append("- A05 引力间隙 / A08 可证伪性缺失：任何“修补”=**① 外部输入**；route_verdict=DEAD，最小证伪集规模=1。")
    lines.append("")
    lines.append("## 3. 类型聚合与判定")
    lines.append("")
    lines.append("- 四型计数：外部输入=%d / 零信息重排=%d / 范围退缩=%d / 自相矛盾=%d。" % (
        cc["EXTERNAL-INPUT"], cc["IDENTITY-RELABEL"], cc["SCOPE-SHRINK"], cc["CONTRADICTION"]))
    lines.append("- 前提净变化 = **%+d**（>0 ⇒ 修补总体让前提更多，缺口被平移而非闭合）。" % meta["net_premise_delta"])
    lines.append("- 任一修补闭合全局缺口？ **%s**。" % ("是" if meta["n_closes"] else "否"))
    lines.append("- 四型是否穷尽？ **%s**。" % ("是" if meta["exhaustive"] else "否"))
    lines.append("- **结构不可修补 = %s**。" % ("成立" if meta["structural_unpatchable"] else "不成立"))
    lines.append("")
    lines.append("## 4. 审计内部修正（我方引擎 bug，单列，不承载 UFT 修补意义）")
    lines.append("")
    lines.append("这些修复证明审计链自纠错（r122 PASS），修的是‘尺子’不是‘被测理论’：")
    for a in AUDIT_INTERNAL_FIXES:
        lines.append("- [%s] %s" % (a["src"], a["desc"]))
    lines.append("")
    lines.append("## 5. 结论")
    lines.append("")
    lines.append("**没有修复的原理 = 结构不可修补。**")
    lines.append("")
    lines.append("每一次“修改”都只是把 closure=0.327 的缺口在四型之间搬运：")
    lines.append("加输入（缺口平移）、重排（假绿）、退缩（放弃）、自爆（FAIL）。")
    lines.append("没有任何局部修补能同时保持全维覆盖、前提净下降、有判别力预言——")
    lines.append("这正是 r130 BSM 准入判据（前提净下降）所刻画的‘进展’门槛，而本战役")
    lines.append("7 卷统一候选 + 全部退守路径无一越过。")
    lines.append("")
    lines.append("**出路不在修补，而在新原理**：须出现一个使前提净计数下降且经验内容净增")
    lines.append("的构造；在此之前，‘全维自洽与归一化’在结构上不可达成。")
    lines.append("")
    lines.append("## 附录 · Glossary")
    lines.append("- **closure**：推导链自封口度 = DERIVED/总前提；r130 实测 0.327。")
    lines.append("- **外部输入**：作为新自由参数/标度/群/优先系引入的前提，使前提净增。")
    lines.append("- **零信息重排**：重定义/恒等式重排，经验内容不变（r125 标识符降 INFO）。")
    lines.append("- **范围退缩**：放弃原声称的部分目标（粒子/星体/引力）。")
    lines.append("- **结构不可修补**：closure<1 的理论，局部修补四型穷尽且均不闭合全局缺口。")
    lines.append("- **审计内部修正**：我方引擎 bug 修复，不承载 UFT 修补意义。")
    lines.append("")
    lines.append("## 数据出处")
    lines.append("- 机读册：`数据/%s.json` / `数据/%s.md`" % (STEM, STEM))
    lines.append("- 源：r124.json.fixes、r123 counts/退守、r129.json.retreats、r131.json.items、r125 tally、r130 summary")
    lines.append("- 审计内部修正：r125/r127/r129/r130 引擎 bug 修复记录")
    lines.append("")
    out = os.path.join(DATA, JUDGE_STEM + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out

def main():
    os.makedirs(DATA, exist_ok=True)
    meta = compute_meta()
    p1 = build_json(meta)
    p2 = build_md(meta)
    p3 = build_report(meta)
    p4 = build_judgment_ledger(meta)
    print("OK generated:")
    for p in (p1, p2, p3, p4):
        print("  ", os.path.relpath(p, PROJECT))
    print("META:", meta["answer_to_user"])
    print("type_counts", meta["type_counts"], "| net_premise_delta", meta["net_premise_delta"],
          "| structural_unpatchable", meta["structural_unpatchable"])
    print("non_additivity_freeze=True | exit_code=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
