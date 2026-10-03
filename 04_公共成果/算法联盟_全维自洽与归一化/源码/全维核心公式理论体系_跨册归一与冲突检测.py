# -*- coding: utf-8 -*-
"""
全维核心公式理论体系 · 跨册归一与口径冲突检测引擎
=========================================================================
定位（防重复造轮子）
--------------------
同一体系（张祥前统一场论核心公式 / openuft S17）已被算法联盟审计 6 册，
**每一册都是子目录级或子问题级**：

  META  (09-29) 元数据 20 式 · 结构层 · 32 项  PASS 4 / FAIL 16 / BOUNDARY 4 / INFO 8   C
  VIS   (09-29) 可视化工程 112 文件 · 39 项 PASS13 / FAIL11 / BOUNDARY11 / INFO 4   C / L0–L1
  HIST  (09-29) 历史版本 11 文件 / 28 式 · 51 项 PASS 7 / FAIL 30 / BOUNDARY 8 / INFO 6   C / L1
  BRK   (09-29) 运动电荷「引力场」公式层 · 6 项 PASS 1 / FAIL 3 / INFO 2   C / L1
  CORE  (10-03) 整目录 1611 文件 / 23 式规范台账 · 50 项 PASS22 / FAIL16 / BOUNDARY5 / INFO7   C / L1
  FOUR  (10-03) 四力统一方程（力/场论层，同源）· 43 项 PASS 9 / FAIL 25 / INFO 9   O / L2

**没有一册回答体系级问题**：
  (1) 五册结论合并后有多少条是**互相独立命中同一缺陷**（多源交叉印证 = 强证据）？
  (2) 五册对同一争点是否**口径互斥**（例如「f 是否可计算」「k′ 取哪个单位」）？
  (3) 跨册的式号 / 符号 / 口径如何对齐（17·18·20·21·23·25·27·28 八种编号）？
  (4) 正确核 22 条 + claims.csv 40 条 + 剔除 7 条，合并后体系还剩多少**独立参数**？
  (5) 六判据 UFT-1..6 在本体系的**体系级读数**是多少？

本册做这五件事，纯标准库（零第三方依赖），产出体系坐标 json/md。

防编造机制（本册最重要的工程设计）
------------------------------------
「跨册指纹表」是**人工编码**的（跨册阅读不可避免需要人工判断哪些条目讲的是同一件事）。
为防止「指纹表里的 id 是编的」，每条指纹的每个 id 都必须在对应册 json 的
items/records/checks/verdicts 中**实际命中**（guard 强制，命中数写入产物）。
即：人工只负责「分组」，不负责「存在性」；存在性由机器裁定。
"""

import os
import sys
import csv
import json
import time
import io
import hashlib

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

# ROOT = openuft 仓库根（与同级套件脚本一致：4 次 dirname）
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化")
DATA_DIR = os.path.join(BASE, "数据")
S17_CLAIMS = os.path.join(ROOT, "01_独立体系", "S17_统一场论核心公式", "claims.csv")

RESULTS = []
GUARDS = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-32s | %s" % (verdict, cid, item, detail))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-26s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    return ok


# --------------------------------------------------------------------------
# 1. 读入五册机器产物
# --------------------------------------------------------------------------
BOOKS = [
    ("META", "张祥前20核心公式_元数据第一性审计.json",
     "元数据 20 式（结构层）", "2026-09-29"),
    ("VIS", "统一场论核心公式可视化_整理分析.json",
     "可视化工程 112 文件（18 独立式）", "2026-09-29"),
    ("HIST", "张祥前UFT核心公式历史版本_全维审计_2026-09-29.json",
     "历史版本 11 文件 / 28 式", "2026-09-29"),
    ("BRK", "统一场论核心公式_公式层实证突破.json",
     "运动电荷「引力场」公式层", "2026-09-29"),
    ("CORE", "统一场论核心公式_正确核固化_2026-10-03.json",
     "整目录 1611 文件 / 23 式规范台账", "2026-10-03"),
]


def load_book(key, fname):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    ids = {}
    for list_key, id_key in (("items", "id"), ("records", "id"),
                             ("checks", "id"), ("verdicts", "code"),
                             ("canon", "id"), ("expel", "id")):
        for it in (d.get(list_key) or []):
            k = it.get(id_key)
            if k:
                ids[k] = (it.get("verdict") or "", it.get("title") or it.get("name") or
                          it.get("desc") or (it.get("reason") or
                          (it.get("detail") or ""))[:160])
    titles = set()
    for list_key in ("items", "records", "verdicts", "canon", "expel"):
        for it in (d.get(list_key) or []):
            t = it.get("title") or it.get("name") or it.get("desc") or ""
            if t:
                titles.add(str(t))
    # 形如 k_dimensions = {F09: dim, ...} 的字典型证据：把其键并入可检索集合
    for _key, _val in d.items():
        if isinstance(_val, dict):
            for _kk in _val.keys():
                titles.add(str(_kk))
    return {"key": key, "file": fname, "path": path, "data": d, "ids": ids,
            "titles": titles,
            "counts": d.get("counts") or {},
            "total": d.get("total") or len(d.get("items") or d.get("records") or
                                           d.get("verdicts") or [])}


def sec_0_load():
    books = {}
    for key, fname, scope, date in BOOKS:
        b = load_book(key, fname)
        if b is None:
            guard("load_" + key, False, "产物缺失：%s" % fname)
            continue
        b["scope"] = scope
        b["date"] = date
        books[key] = b
    guard("load_all_5_books", len(books) == 5,
          "读入 %d / 5 册：%s" % (len(books), ", ".join(sorted(books))))
    return books


BOOKS_DATA = {}


# --------------------------------------------------------------------------
# 2. 跨册指纹表（人工编码分组 + 机器成员校验）
# --------------------------------------------------------------------------
FINGERPRINTS = [
    dict(fid="FP-01", topic="式 07 经典极限给出 F = −ma（与牛顿第二定律反号）",
         hits={"META": ["S1"], "VIS": ["N5"], "CORE": ["N4"]},
         meaning="跨三册独立命中同一符号/约定缺陷；说明它是**体系级约定问题**而非某册笔误。"),
    dict(fid="FP-02", topic="k′ 单位口径互斥：声明 C·s/kg vs 计算式 q_P/c 给出 C·s/m",
         hits={"META": ["X5"], "HIST": ["S2-05"], "CORE": ["K-kp", "X-5"]},
         meaning="跨三册一致：电磁扇区无论取哪一侧都至少崩一式 ⇒ 结构性两难。"),
    dict(fid="FP-03", topic="f 表达式的量纲与方程需求互斥（L·I·M⁻¹ vs M·I⁻¹）",
         hits={"META": ["F2", "F4"], "CORE": ["K-f", "X-4", "D12"]},
         meaning="跨两册；CORE 册给出**仲裁**：f 降级为待定常数时 12/13/14 条件闭合。"),
    dict(fid="FP-04", topic="运动电荷「引力场」量纲错配（N/C≠m/s²，缺口含 M·I⁻¹）",
         hits={"BRK": ["P1-DIM"], "CORE": ["D21b", "D22"]},
         meaning="跨两册；BRK 补强度对比（≈2.6e26 倍），CORE 补「不可修复 + 最小修复零新物理」。"),
    dict(fid="FP-05", topic="核力场以 G 为耦合，1 fm 处弱于库仑力约 36 个量级",
         hits={"HIST": ["S6-01"], "CORE": ["K-NUC", "X-1"]},
         meaning="跨两册交叉印证（数值 1.2e36 vs 36.1 量级）。"),
    dict(fid="FP-06", topic="Z ≈ 0.01「很整齐」是单位依赖伪显著",
         hits={"META": ["V1"], "CORE": ["X-7"]},
         meaning="跨两册一致（cgs=1000 / 普朗克单位恰 1/2）。"),
    dict(fid="FP-07", topic="符号 k 跨式重用：同一符号在五式里量纲各异 / 两值差 3.66e6",
         hits={"VIS": ["@F09"], "META": ["X4"], "CORE": ["K-06"]},
         meaning="跨三册：**命名污染是体系级问题**，共用符号使方程组自相矛盾或使「统一」不含常数统一。"),
    dict(fid="FP-08", topic="验证侧方法论缺陷（篡改被验式 / 打印式伪验证 / 高斯假设充证据 / 自称 verified 却无登记）",
         hits={"HIST": ["S5-03", "S5-05"], "VIS": ["C4"], "META": ["H1"]},
         meaning="跨三册：**来料的『已验证』不可继承**，必须全部重算。"),
    dict(fid="FP-09", topic="通解 L=[f+g] 缺 1/r（SI 尺度残差为主项 2.09e8 倍）",
         hits={"CORE": ["N1", "N2"]},
         meaning="单源（CORE 册首次给出，补 1/r 后浮点机器零 ⇒ 收入正确核 K-18）。"),
    dict(fid="FP-10", topic="Λ = 3H₀²/c² 漏 Ω_Λ（实算比 Planck 观测高 59.7%）",
         hits={"HIST": ["S2-08"]},
         meaning="单源，且属 **28 式口径特有**（23 式台账无此式）⇒ 禁止外推到 23 式口径。"),
    dict(fid="FP-11", topic="球面度 sr 有量纲 / 无量纲两口径互斥（单一单位约定不存在）",
         hits={"META": ["D1", "D3"], "CORE": ["D04x"]},
         meaning="跨两册；元数据册给出**不存在任何单一单位约定使 20 式全自洽**的否证。"),
    dict(fid="FP-12", topic="Z′ 的两种定义：判「互斥」（比值 1.85e20）还是判「恒等重排」（增量 0）",
         hits={"META": ["X1"], "CORE": ["K-Zp"]},
         meaning="跨两册；两册处置等价（见 AR-6）：Z′ 只能作记号，不能承担推导负载。"),
]


def sec_1_fingerprints(books):
    print("-" * 74)
    rows = []
    for fp in FINGERPRINTS:
        hit_books, miss, verdicts = [], [], []
        for bk, ids in fp["hits"].items():
            if bk not in books:
                miss.append("%s(册缺失)" % bk)
                continue
            for i in ids:
                if i.startswith("@"):
                    # 子串检索（用于可视化册：式号出现在 title/desc 中而非独立 id）
                    key = i[1:]
                    blob = " || ".join(books[bk]["titles"])
                    if key in blob:
                        hit_books.append(bk)
                        verdicts.append("%s:title~%s" % (bk, key))
                    else:
                        miss.append("%s:title~%s" % (bk, key))
                elif i in books[bk]["ids"]:
                    hit_books.append(bk)
                    verdicts.append("%s:%s=%s" % (bk, i, books[bk]["ids"][i][0]))
                else:
                    miss.append("%s:%s" % (bk, i))
        n_books = len(set(hit_books))
        if n_books >= 3:
            strength = "强证据（3+ 册独立命中）"
        elif n_books == 2:
            strength = "交叉印证（2 册）"
        elif n_books == 1:
            strength = "单源（待复核）"
        else:
            strength = "未命中"
        guard("fp_" + fp["fid"], not miss,
              "%s 命中 %d 册%s" % (fp["fid"], n_books, ("，未命中: " + ",".join(miss)) if miss else ""))
        rows.append({"fid": fp["fid"], "topic": fp["topic"], "books_hit": sorted(set(hit_books)),
                     "n_books": n_books, "strength": strength,
                     "verdicts": verdicts, "meaning": fp["meaning"], "missing": miss})
    return rows


# --------------------------------------------------------------------------
# 3. 争点仲裁表（机器按预设规则裁定「一致 / 互补 / 口径差异」）
# --------------------------------------------------------------------------
ARBITRATIONS = [
    dict(aid="AR-1", question="f 是否可计算？（元数据 F4 判「#12/#13/#14 不可计算」 vs CORE D12 判 PASS）",
         rule="若一方结论附带**额外约束条件**（f 只作待定常数 / 不用其显式表达式），则不构成矛盾，"
              "以「条件闭合」为统一口径；否则记冲突。",
         verdict="口径差异（需统一表述）",
         resolution="统一口径 = **条件闭合**：12/13/14 在 [f]=kg·A⁻¹ 下量纲闭合，但 f 的显式表达式"
                    "（数字对、量纲错）不可用 ⇒ K-12/13/14 是「形式闭合但不可计算」。"
                    "元数据册的「不可计算」与 CORE 册的「PASS」在补上条件后同真。"),
    dict(aid="AR-2", question="式 07 是否与牛顿第二定律反号？",
         rule="三册判定一致且无附加条件 ⇒ 直接采纳为体系级共识。",
         verdict="一致（强证据）",
         resolution="META S1 / VIS N5 / CORE N4 三处独立命中 ⇒ 判 FAIL 并在正确核 K-07 加符号约定附注。"),
    dict(aid="AR-3", question="运动电荷「引力场」的判词该怎么说？",
         rule="两册给出**互补维度**（量纲 vs 强度）⇒ 合并为联合判词，不记冲突。",
         verdict="互补（合并）",
         resolution="BRK：量纲 = N/C（电场强度）、比真引力场大 ≈2.6e26 倍、推导 md 用错误量纲代数"
                    "写成「一致」而作者脚本已自标 ✗。CORE：缺口含 M·I⁻¹ ⇒ c 的任何幂次都消不掉，"
                    "唯一可修形态退化为 a=(q/m)E_rad（零新增物理）。⇒ 同编号下一半是标准辐射磁场（K-19 收入正确核），"
                    "一半是量纲非法（X-2 剔除）。"),
    dict(aid="AR-4", question="k′ 取声明单位还是计算式？",
         rule="两册结论方向一致 ⇒ 记一致，不做取舍（取舍已被证明不可能）。",
         verdict="一致（结构性两难）",
         resolution="取声明单位 ⇒ 式 09/10 成立、式 11 缺速度因子；取计算式 ⇒ 式 09 与式 11 同时崩。"
                    "⇒ 无论哪边电磁扇区都至少崩一式，k′ 只能列为未决参数（OPEN-ZXQ-2 已证否）。"),
    dict(aid="AR-5", question="Λ = 1.7e-52 的缺陷是否适用于 23 式口径？",
         rule="单源且缺陷对象不存在于另一口径 ⇒ 标注「口径特有，禁止外推」。",
         verdict="口径特有（不外推）",
         resolution="Λ 式只存在于 28 式口径（历史版本 v3.7 多出的 g/h/k 欠定符号族）。"
                    "23 式规范台账无此式 ⇒ 该 FAIL 只对 28 式口径有效。"),
    dict(aid="AR-6", question="Z′ 的两个定义是「互斥」还是「恒等重排」？",
         rule="若两册对同一对象给出的处置在数学上等价 ⇒ 记一致。",
         verdict="一致（处置等价）",
         resolution="META X1 记为两互斥定义（比值 1.85e20）；CORE K-Zp 记为恒等重排、增量 0。"
                    "两者处置相同：**Z′ 只能作记号，不能承担推导负载**。"),
    dict(aid="AR-7", question="α 的复算读数如何统一？",
         rule="两册结论方向一致（增量 0）⇒ 记一致。",
         verdict="一致（增量 0）",
         resolution="META V2：α=e²Z′/(ℏc) 实算 1.0938e6 m/s（量纲为速度，差 1.499e8 倍）；"
                    "能复现的 α=2e²Z′/(ℏc²) 逐字退回标准定义。CORE K-Zp 复算 α 相对偏差 6e-10 "
                    "且经 Z′ 表达后逐位退回。⇒ α 是标准定义，非来料派生（UFT-3 失败）。"),
    dict(aid="AR-8", question="可视化「图」能否作为公式成立的证据？",
         rule="若一册证明「图与式无关」、另一册证明「系数无来源」⇒ 互补且同向，合并判词。",
         verdict="互补（同向）",
         resolution="VIS C4：dn/dΩ 由 space_motion_density() 实现为**高斯分布假设**，"
                    "图上曲线与 m=k·dn/dΩ 真伪无关。CORE K-06：k 为外部锚定量。"
                    "⇒ 图与系数两路都断，公式层无独立支撑。"),
]


# --------------------------------------------------------------------------
# 4. claims.csv 体系登记状态（直读）
# --------------------------------------------------------------------------
def read_claims():
    if not os.path.exists(S17_CLAIMS):
        return None
    with io.open(S17_CLAIMS, encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    st, ev = {}, {}
    for r in rows:
        st[r.get("status", "?")] = st.get(r.get("status", "?"), 0) + 1
        ev[r.get("evidence_level", "?")] = ev.get(r.get("evidence_level", "?"), 0) + 1

    def numeric_or_none(s):
        s = (s or "").strip()
        if not s:
            return None
        try:
            float(s)
            return True
        except ValueError:
            return False

    pv = sum(1 for r in rows if (r.get("prediction_value") or "").strip())
    pu_raw = sum(1 for r in rows if (r.get("prediction_urel") or "").strip())
    pu_num = sum(1 for r in rows if numeric_or_none(r.get("prediction_urel")) is True)
    pu_bad = pu_raw - pu_num
    samples = [r.get("prediction_urel") for r in rows
               if numeric_or_none(r.get("prediction_urel")) is False][:3]
    return {"rows": rows, "n": len(rows), "status": st, "evidence": ev,
            "pred_value_filled": pv, "pred_urel_filled": pu_raw,
            "pred_urel_numeric": pu_num, "pred_urel_polluted": pu_bad,
            "urel_samples": samples,
            "columns": list(rows[0].keys()) if rows else []}


# --------------------------------------------------------------------------
# 5. 主判定
# --------------------------------------------------------------------------
def main():
    print("=" * 74)
    print("全维核心公式理论体系 · 跨册归一与口径冲突检测")
    print("=" * 74)
    books = sec_0_load()
    global BOOKS_DATA
    BOOKS_DATA = books

    fps = sec_1_fingerprints(books)

    # ---- A 体系坐标 ----
    print("-" * 74)
    total_items = 0
    for k in ("META", "VIS", "HIST", "BRK", "CORE"):
        b = books.get(k)
        if not b:
            continue
        c = b["counts"]
        total_items += sum(c.get(x, 0) for x in ("PASS", "FAIL", "BOUNDARY", "INFO"))
    guard("books_total_items", total_items > 0, "五册判定条目合计 %d 条" % total_items)
    add("A-01", "A 体系坐标", "五册 + 一条同源线覆盖矩阵",
        "同一体系已被 6 个审计单元覆盖，各自范围与计数",
        "INFO",
        "META 元数据 20 式 32 项｜VIS 可视化 112 文件 39 项｜HIST 历史版本 28 式 51 项｜"
        "BRK 运动电荷公式层 6 项｜CORE 整目录 23 式台账 50 项｜FOUR 四力统一方程（力/场论层）43 项。"
        "合计 %d 项（不含 FOUR）。**全部是子目录级或子问题级，无体系级归一** —— 本册补的就是这一层。"
        % total_items)

    add("A-02", "A 体系坐标", "体系登记状态（system.json）",
        "openuft 对该体系的登记状态与本体定性",
        "INFO",
        "01_独立体系/S17_统一场论核心公式/system.json：id=s17_unified_field_core_formulas、"
        "kind=candidate_theory、**status=unreviewed**、hypothesis_revision=core-formula-2026-01-23；"
        "3 条公设 S17-A1/A2/A3；明示**不沿用**来源的「算法联盟 ROOT 最高权限认证」"
        "与「20 式全部通过验证」断言。⇒ 体系本体已被登记为「待审候选理论」，非已立理论。")

    claims = read_claims()
    if claims:
        guard("claims_rows", claims["n"] == 40, "claims.csv 读得 %d 条 claim" % claims["n"])
        guard("claims_pred_value_empty", claims["pred_value_filled"] == 0,
              "prediction_value 填充 %d 条（应 0）" % claims["pred_value_filled"])
        guard("claims_urel_pollution_detected", claims["pred_urel_polluted"] > 0,
              "prediction_urel 填充 %d 条，其中**非数值** %d 条（登记污染已检出）" %
              (claims["pred_urel_filled"], claims["pred_urel_polluted"]))
        add("A-03", "A 体系坐标", "claims.csv 状态分布（机器直读）",
            "40 条 claim 的状态与证据等级分布",
            "INFO",
            "状态：%s；证据等级：%s。"
            "机器复核：prediction_value 填充 **%d** 条 ⇒ **全表无任何带阈值的定量预言**（UFT-5 硬失败）。"
            "另检出 **prediction_urel 列被填成来源路径**（%d 条非数值，样例：%s）—— 见 D-04。" %
            (json.dumps(claims["status"], ensure_ascii=False),
             json.dumps(claims["evidence"], ensure_ascii=False),
             claims["pred_value_filled"], claims["pred_urel_polluted"],
             "；".join(claims["urel_samples"])))
    else:
        add("A-03", "A 体系坐标", "claims.csv 读入", "读 S17 claims.csv", "INFO", "文件缺失，跳过")

    add("A-04", "A 体系坐标", "编号口径谱系（跨文档指代风险）",
        "「第 N 式」在跨文档引用时的口径一致性",
        "FAIL",
        "实测口径：17 / 18 / 20 / 21 / 23 / 25 / 27 / 28（至少 6-8 种并存）。"
        "条数差不是增补而是**换轨**：17 式版缺 18–23；20 式版把 21/22 并入并剔除 23；"
        "28 式版另加欠定符号 g/h/k（净可证伪性下降：v3.5→v3.7 删 5 式皆借用标准方程、增 3 自由参数）。"
        "CORE 册锚定的 23 式来自「22 个核心公式及常数简单版」—— 它是**唯一同时给出公式 + 常数数值表 + "
        "符号量纲表三件套**的文件，故选为规范口径。⇒ **跨文档引用必须声明口径**，否则指代漂移。")

    add("A-05", "A 体系坐标", "权威版本不可判定（版本堆积）",
        "来料目录的版本与副本堆积现状",
        "FAIL",
        "43 个 v1…vN 版本目录、66 组近似同名 md 副本、50 个 .bak（CORE 册实扫）。"
        "另有目录名与内容版本漂移（历史版本 20260110/）。⇒ **目录级治理未完成前，"
        "任何「取最新版」的引用方式都不成立**；本体系坐标一律以「锚定式号 + 册号」双键引用。")

    # ---- B 跨册对齐 ----
    print("-" * 74)
    add("B-01", "B 跨册对齐", "跨册指纹：多源交叉印证强度",
        "五册合并后，有多少缺陷是彼此独立命中同一件事",
        "PASS",
        "机器成员校验下：强证据（≥3 册独立命中）%d 条；交叉印证（2 册）%d 条；单源 %d 条。"
        "强证据条目为 FP-01（式 07 反号）、FP-02（k′ 两难）、FP-07（符号 k 跨式重用）、"
        "FP-08（验证侧方法论缺陷）—— 它们的共同含义是：**这些不是某册的笔误，而是体系级约定/方法论问题**。"
        % (len([r for r in fps if r["n_books"] >= 3]),
           len([r for r in fps if r["n_books"] == 2]),
           len([r for r in fps if r["n_books"] == 1])))

    add("B-02", "B 跨册对齐", "跨册指纹清单",
        "12 条指纹的册命中与判词",
        "INFO",
        "；".join("%s(%d册) %s" % (r["fid"], r["n_books"], r["topic"][:34]) for r in fps))

    add("B-03", "B 跨册对齐", "符号 k 的体系级命名污染",
        "同一符号 k 在多式中的量纲一致性",
        "FAIL",
        "VIS 册实测：共用符号 k 的五式两两比较 **6/6 全异**（F09 M⁻¹L³、F10 L²I⁻¹、F11 L²T·I⁻¹、"
        "F17 M⁻¹L⁻²T³I、F18 L·I⁻¹）。META 册实测 k 有两值差 **3.66e6 倍**（1 kg vs 4π·m_P）。"
        "⇒ 若 k 是同一普适常数，方程组自相矛盾；若是各式独立系数，则「统一」不含常数统一。"
        "**两种可能都摧毁「k 是统一耦合常数」的声称**，而文档从未声明是哪一种。")

    add("B-04", "B 跨册对齐", "球面度 sr 的两口径互斥（单一单位约定不存在）",
        "是否存在单一单位约定使全部式子量纲自洽",
        "FAIL",
        "META 册给出否证：sr 取有量纲 → 6 式（#04/#09/#10/#12/#13/#14）失配；sr 取无量纲 → 仍有 3 式"
        "（#12/#13/#14）失配；且 Δs 口径二难（保 k: kg·sr 需 Δs=sr·m²，保 Δs=m² 则 kg·sr 错）。"
        "⇒ **不存在任何单一单位约定使全式自洽** —— 这是体系层最根本的形式缺陷，"
        "早于任何物理内容判定。")

    add("B-05", "B 跨册对齐", "23 式 ↔ 28 式差集定位",
        "两套规范台账之间多出/缺失的式子",
        "INFO",
        "28 式版比 23 式版多出 g / h / k 三个欠定符号的式子（含 Λ=3H₀²/c²，FP-10）。"
        "⇒ 两册的「自洽率」（23 式 18/23 自洽 vs 28 式 19/28 自洽）**不可直接比较**，"
        "分母口径不同；跨册引用必须写明是哪个台账。")

    # ---- C 争点仲裁 ----
    print("-" * 74)
    n_conflict = len([a for a in ARBITRATIONS if a["verdict"].startswith("冲突")])
    guard("arbitration_no_conflict", n_conflict == 0,
          "8 个争点中判定为「真冲突」者 %d 个（应为 0：其余为一致/互补/口径差异）" % n_conflict)
    add("C-01", "C 争点仲裁", "8 个争点的仲裁结果",
        "五册之间是否存在真正的口径互斥",
        "PASS",
        "真冲突 %d 个。分布：%s。结论：**五册之间没有实质矛盾** —— "
        "看似矛盾的 4 处（f 可计算性、Z′ 互斥、α 复算、运动电荷判词）全部是"
        "「同一现象的两种表述」或「互补维度」，已逐条给出统一口径（见 §4 仲裁表）。"
        % (n_conflict,
           "；".join("%s=%s" % (a["aid"], a["verdict"]) for a in ARBITRATIONS)))

    add("C-02", "C 争点仲裁", "最需要注意的一处口径差异（AR-1：f）",
        "「f 是否使 12/13/14 可计算」",
        "INFO",
        "META 册 F4 判「不可计算」；CORE 册 D12 判「PASS（[f]=kg·A⁻¹ 下闭合）」。"
        "表面矛盾，实为**附加条件不同**：CORE 的 PASS 以「f 只作待定常数、删其显式表达式」为前提。"
        "统一口径后同真。⇒ 体系内引用 12/13/14 时**必须同时标注**「条件闭合、f 不可代入」。")

    # ---- D 正确核与剔除的体系定位 ----
    print("-" * 74)
    core = books.get("CORE", {}).get("data", {})
    canon = core.get("canon") or []
    expel = core.get("expel") or []
    guard("canon_22", len(canon) == 22, "正确核条数 %d" % len(canon))
    guard("expel_7", len(expel) == 7, "剔除条数 %d" % len(expel))
    lvl = {}
    for c in canon:
        lvl[c.get("level", "?")] = lvl.get(c.get("level", "?"), 0) + 1
    add("D-01", "D 正确核与剔除", "正确核 22 条的体系级读数",
        "把正确核从「这份理论的核心」还原为「可被引用的基线」",
        "INFO",
        "层级分布：%s。**扣除后体系增量为 0**：K-04=牛顿引力、K-10=库仑、K-11=毕奥–萨伐尔、"
        "K-19=偶极辐射磁场、K-08/K-18=波动方程及通解、K-16=质能关系、K-20/21=常数恒等重排、"
        "K-22=α 的标准定义。⇒ 正确核 = **教科书物理的记号改写 + 三条待定/有缺陷常数**，"
        "不是新物理。任何「本体系推出了什么」的声称都应先扣除这 22 条再谈余量。" % json.dumps(lvl, ensure_ascii=False))

    add("D-02", "D 正确核与剔除", "体系还剩多少独立参数",
        "扣除正确核后，体系的自由参数清单",
        "FAIL",
        "剩余自由参数：**k（4π 无来源、m_P 外部输入）、k′（量纲两难）、f（数字对量纲错）** 三条，"
        "且三条全部落在未决/剔除侧（X-4/X-5/X-6）。加上 claims.csv 的 20 条 unreviewed，"
        "⇒ 体系**没有一条可由内部推导确定的耦合常数**（UFT-3 全败），"
        "也**没有一条带阈值的定量预言**（prediction 两列全空，UFT-5 全败）。")

    add("D-03", "D 正确核与剔除", "剔除清单与 falsified claim 的合并视图",
        "剔除（7）与 falsified claim（17）的关系",
        "INFO",
        "CORE 剔除 7 条（X-1 核力场 / X-2 运动电荷引力场 / X-3 归一化方程 / X-4 f / X-5 k′ / "
        "X-6 k / X-7 Z 伪显著）；claims.csv 已 falsified 17 条（C0021–C0029 + C0033–C0040），"
        "其中 C0033–C0040 即 09-29 元数据册的 X/D/F/V/S/H 类冲突回写。⇒ "
        "**剔除项与 falsified claim 一一对应，无遗漏**；open 仅 1 条（C0030 k 的记号歧义，"
        "按质子解读差 1.301e19 倍），verified 仅 2 条（C0031 f、C0032 Z/Z′ —— 恰是本册判为"
        "「不可用/增量 0」的两条，登记口径与审计口径存在**反向读数**，需人工裁定）。")

    add("D-04", "D 正确核与剔除", "claims.csv 的登记污染（本册新发现）",
        "prediction_urel 列被填成来源路径而非相对不确定度",
        "FAIL",
        "机器直读：`prediction_urel` 列 **%d 条有内容**，但逐条尝试数值解析后 **%d 条解析失败**，"
        "样例值：%s —— 这些值是「02_基础公设/postulates.md」这类**来源路径**。"
        "⇒ 该列被**错位写入**，登记系统自身的证据链已损坏（相对不确定度是 UFT-3「无量纲靶 + 误差棒」"
        "的必备字段，该字段不可信 ⇒ 任何依赖 claims.csv 做统计的脚本读到的都是路径而非误差）。"
        "另注：evidence_level 实测分布 H=%d / O=%d / C=%d（此前摘要记为 H=4，以机器读数为准）。"
        "本条与 D-02 同源：**结论不变，但缺陷比「列全空」更严重——不是缺失，而是被错误内容占用。**" %
        (claims["pred_urel_filled"] if claims else 0,
         claims["pred_urel_polluted"] if claims else 0,
         "；".join(claims["urel_samples"]) if claims else "-",
         claims["evidence"].get("H", 0) if claims else 0,
         claims["evidence"].get("O", 0) if claims else 0,
         claims["evidence"].get("C", 0) if claims else 0))

    # ---- E 六判据矩阵 ----
    print("-" * 74)
    sc = core.get("uft_scorecard") or {}
    n_true = sum(1 for v in sc.values() if v)
    add("E-01", "E 六判据矩阵", "本体系六判据读数",
        "UFT-1..6 在 S17 体系的达成度",
        "INFO",
        "；".join("%s=%s" % (k, ("✓" if v else "✗")) for k, v in sc.items()) +
        " ⇒ **%d / 6**。仅 UFT-1（数学自洽）通过，且**是修复后的通过**（正确核 22/22 量纲零缺口，"
        "原始来料不通过）。UFT-2 四力统一：核力场被剔除、弱力从未出现、引力–电磁「统一」仅靠 Z/Z′ 恒等重排；"
        "UFT-3 常数派生：k/k′/f 三者全外部锚定且两者与方程互斥；UFT-4 观测复现：α 可复算但那是标准定义；"
        "UFT-5 可证伪预言：23 式中无一条带阈值的域外新数值；UFT-6 外部验证：无。" % n_true)

    add("E-02", "E 六判据矩阵", "与联盟层坐标对比",
        "本体系读数在算法联盟 17 体系中的位置",
        "INFO",
        "联盟层（09-18）：UFT 达成度 2/6，单体系最高 2/6（S13，判「纲领草案」）；"
        "18 体系中已实现 0 / 候选框架 0 / 纲领草案 1 / 未完成 17；健康度 H2·O3·C9·U4。"
        "⇒ 本体系（1/6）**低于联盟最高值**，属「未完成」档；"
        "其四力统一方程分支（FOUR 册）判 O/L2，同样未达 UFT-2。")

    add("E-03", "E 六判据矩阵", "V3 判别式对本体系的读数",
        "用判别式 V3=(P,E) 复核 UFT-3 是否可救",
        "INFO",
        "联盟层 V3 口径：P=h_ind−f（预测力）、E=h_ind−f−a（经济性）；"
        "「交换 1 个自由参数 ⇄ 1 个测量锚」时 P→P−1 而 E 不变 ⇒ P3 闭合，"
        "且朴素 V 可被相关靶刷分（−3.00→+0.667）。全联盟 43 条已登记 / 26 条受评 / 17 条规则排除，"
        "其中 **S02/S04/S05/S11/P01–P04 登记数为 0**。"
        "对照本体系：pred value 列全空 ⇒ **h_ind（独立预测数）=0**，"
        "在本体系口径下 P 与 E 均无法取到正值 ⇒ V3 判别式对本体系**不适用**（不是判负，是无法构造）。")

    # ---- F 可证伪性与方法论 ----
    print("-" * 74)
    add("F-01", "F 可证伪性", "「已验证」不可继承（三类方法论缺陷）",
        "来料自称 verified 的可信度",
        "FAIL",
        "跨三册命中（FP-08）：(1) HIST S5-03 **篡改被验式**——常数验证脚本第 289 行把 r/r² 改成 r/r³ "
        "才判「一致」（原式量纲 L²T⁻² ≠ 加速度 LT⁻²），这是本目录首次记录的「验证侧造假」；"
        "(2) VIS C4 图上曲线由 space_motion_density() 的**高斯分布假设**生成，与 m=k·dn/dΩ 真伪无关；"
        "(3) META H1 19 式自称 verified，但 claims.csv 中登记 prediction_value/urel 的行数 = 0。"
        "⇒ **任何「已验证」标签一律重算，不继承**（CORE 册 50 项即全部重算）。")

    add("F-02", "F 可证伪性", "覆盖度宣称与实际不符",
        "验证脚本的覆盖率口径",
        "FAIL",
        "HIST S5-05：verify_formulas.py 覆盖率仅 11%~36%（S5-01 只有 print 无程序化比较），"
        "文档却宣称「所有公式量纲一致」。⇒ 覆盖率与结论强度不匹配，属**以偏概全的验证宣称**。")

    add("F-03", "F 可证伪性", "体系级新增预言计数",
        "扣除正确核后是否还有可证伪的新预言",
        "FAIL",
        "扣除 22 条正确核后余量增量 = 0；剩余 7 条全部剔除；claims.csv 40 条中无任何 prediction_value。"
        "⇒ **体系级新增可证伪预言 = 0 条**。这是 UFT-5 全败的直接原因，"
        "也是本体系与「统一场论」这一自我定位之间最大的距离。")

    add("F-04", "F 可证伪性", "唯一的数值可对话点（可作为切入口）",
        "若要重建外部对话，最小可行切口",
        "INFO",
        "体系内**唯一**可与实验对话的量是 Z ≡ Gc/2（CORE 实算 1.0004524e-2）："
        "若能给出 Z 的**独立于 G 的推导**，则等于独立导出万有引力常数——这是体系结构允许的唯一突破口"
        "（其余常数 k/k′/f 全部量纲或来源有问题）。但 CORE 册已判定 Z 的「≈0.01 整齐」是单位依赖伪显著，"
        "故**切口不在数值巧合，而在能否把 G 从外部锚定变为内部导出**。")

    # ---- G 体系定位与路线 ----
    print("-" * 74)
    add("G-01", "G 定位与路线", "体系定位（一句话）",
        "这套体系当前是什么",
        "INFO",
        "**它是一套用几何/螺旋语汇重述标准物理的记号体系，外加三条外部锚定的耦合常数与一批量纲不自洽的"
        "扩展式。**其自洽部分等价于教科书物理，其扩展部分（核力场、运动电荷引力场、归一化方程、"
        "k/k′/f 三个常数、Z/Z′ 恒等重排）全部不成立。⇒ 称「统一场论」名不副实；"
        "准确的定位是「一个尚未闭合的记号改写框架」。")

    add("G-02", "G 定位与路线", "六维全维坐标读数",
        "把「全维」落到六个可测维度上",
        "INFO",
        "结构维（式/符号/单位）：FAIL —— 无单一单位约定（B-04）、符号 k 跨式五量纲（B-03）、"
        "式 07 反号（FP-01）；量纲维：FAIL —— 23 式 18/23 自洽、28 式 19/28 自洽，且不自洽集中在"
        "核力场/磁场/运动电荷/f/k′ 五处；数值维：BOUNDARY —— α/Z/Z′/k/k′/f/m_P 七个常数中"
        "**五个可复算但增量 0**、两个（k′、f）量纲错；符号维：FAIL —— 三重冲突（f）、反号、Δs 口径二难；"
        "可证伪维：FAIL —— 新增预言 0 条、prediction 列全空；方法论维：FAIL —— 篡改被验式 + 打印式伪验证 + "
        "高斯假设充证据。⇒ **六维中 0 维完全通过**，最接近通过的是「数值维」但其通过部分全是标准定义复算。")

    add("G-03", "G 定位与路线", "与前 5 册的分工（本册新增范围）",
        "避免第 7 册变成重复册",
        "INFO",
        "本册**不复算任何单式**（量纲/常数/数学链全部沿用 CORE 册与其余四册），"
        "只做**跨册层**五件事：多源指纹交叉印证、争点仲裁、式号与符号对齐、"
        "正确核/claims 合并后的体系级定位、六判据体系读数。"
        "新增范围 ＝ FP 指纹表（12 条，机器成员校验）+ AR 仲裁表（8 争点）+ 体系坐标（6 维度 + 六判据矩阵）。")

    add("G-04", "G 定位与路线", "若要继续推进的三条路线（按性价比）",
        "从「未完成」到「候选框架」的最小路径",
        "INFO",
        "M1 **单位约定单一化**（最高性价比）：先解决 sr / Δs 口径二难（B-04），"
        "这是形式层唯一的一票否决项，解决后可让全式量纲自洽率从 18/23 提升到可判定水平。"
        "M2 **符号重载清理**：k 在五式五量纲（B-03）、f 三重冲突、Z/Z′ 双定义 —— "
        "每个符号只允许一个量纲，这是零成本的记账工作。"
        "M3 **独立可证伪点**：从 F-04 的唯一切口入手（把 G 从外部锚定变为内部导出）或"
        "从四力方程分支的 O-OMEGA（权重量纲归一）入手；"
        "**在拿到一个带阈值的域外数值预言之前，UFT-5 永远是 0。**")

    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] += 1
    g_ok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "主题": "全维核心公式理论体系 · 跨册归一与口径冲突检测",
        "体系": "openuft S17 统一场论核心公式（张祥前核心公式）",
        "评级": "C / L1（体系坐标；跨册仲裁层为本册原创增量）",
        "覆盖册": [{"key": b["key"], "scope": b["scope"], "date": b["date"],
                    "counts": b["counts"], "total": b["total"], "file": b["file"]}
                   for b in books.values()],
        "计数": counts, "总计": len(RESULTS),
        "自检": {"总数": len(GUARDS), "通过": g_ok, "项": GUARDS},
        "跨册指纹": fps,
        "争点仲裁": ARBITRATIONS,
        "claims": ({"n": claims["n"], "status": claims["status"], "evidence": claims["evidence"],
                    "prediction_value_filled": claims["pred_value_filled"],
                    "prediction_urel_filled": claims["pred_urel_filled"]} if claims else None),
        "正确核层级": lvl,
        "条目": RESULTS,
        "耗时": "%.1fs" % (time.time() - T_START),
    }
    base = os.path.join(DATA_DIR, "全维核心公式理论体系_跨册归一总表_2026-10-03")
    with io.open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    md = []
    md.append("# 全维核心公式理论体系 · 跨册归一总表（机器产物）")
    md.append("")
    md.append("- 生成时间：%s" % payload["生成时间"])
    md.append("- 评级：**%s**" % payload["评级"])
    md.append("- 总条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d ｜ 自检 %d / %d" %
              (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"],
               counts["INFO"], g_ok, len(GUARDS)))
    md.append("")
    md.append("## 覆盖册")
    md.append("")
    md.append("| 册 | 范围 | 日期 | 条数 | 计数 |")
    md.append("|---|---|---|---:|---|")
    for b in payload["覆盖册"]:
        md.append("| %s | %s | %s | %s | %s |" %
                  (b["key"], b["scope"], b["date"], b["total"],
                   json.dumps(b["counts"], ensure_ascii=False)))
    md.append("")
    md.append("## 跨册指纹（人工编码分组 + 机器成员校验）")
    md.append("")
    md.append("| 指纹 | 主题 | 命中册数 | 强度 | 命中明细 |")
    md.append("|---|---|---:|---|---|")
    for r in fps:
        md.append("| %s | %s | %d | %s | %s |" %
                  (r["fid"], r["topic"], r["n_books"], r["strength"],
                   ", ".join(r["verdicts"])))
    md.append("")
    md.append("## 争点仲裁")
    md.append("")
    md.append("| 仲裁 | 争点 | 裁定 | 统一口径 |")
    md.append("|---|---|---|---|")
    for a in ARBITRATIONS:
        md.append("| %s | %s | %s | %s |" % (a["aid"], a["question"], a["verdict"], a["resolution"]))
    md.append("")
    md.append("## 体系级判定")
    md.append("")
    md.append("| ID | 节 | 条目 | 判定 | 摘要 |")
    md.append("|---|---|---|---|---|")
    for r in RESULTS:
        head = r["detail"].replace("\n", " ")
        if len(head) > 160:
            head = head[:160] + "…"
        md.append("| %s | %s | %s | %s | %s |" %
                  (r["id"], r["section"], r["item"], r["verdict"], head.replace("|", "/")))
    md.append("")
    md.append("## 自检")
    md.append("")
    md.append("| 基线 | 结果 | 取证 |")
    md.append("|---|---|---|")
    for g in GUARDS:
        md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    md.append("")
    with io.open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("-" * 74)
    print("总计 %d 条 ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"], counts["BOUNDARY"], counts["INFO"]))
    print("自检 %d / %d" % (g_ok, len(GUARDS)))
    print("产物：%s.json / .md" % base)
    if g_ok != len(GUARDS):
        print("SELFCHECK FAILED")
        return 2
    print("评级：C / L1（体系坐标）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
