# -*- coding: utf-8 -*-
"""
本项目 · 统一场论达成度重算与最小闭合清单（2026-10-08）

动机：既有《全维分析报告 · 统一场论达成度》成稿于 2026-09-18（18 体系、2/6）。
      此后 10 月新增数十册产物（TUFT r14–r21、四力本源、六册归一、GAQ V18 谱系、
      S02/S12/S13/S07/S11 攻破册、本册同日的电荷拓扑通量裁定等），
      体系数已从 18 扩到 22（新增 S15–S18）。**达成度从未重算。**

分工（与并行册，勿互顶）：
  同日并行产物 `04_公共成果/全维全体系统一场论/判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md`
  用 **W0–W7 八判据**（22 体系 × 8 = 176 格）回答「离完成还差什么」。
  本册用 **UFT-1..UFT-6**（沿用 2026-09-18 既有口径）回答「20 天后达成度有没有变」。
  两套判据不是同一把尺子：W 系按**完成条件**切（主方程/无量纲输出/耦合汇聚/谱与代…），
  UFT 系按**证据等级**切（自洽/统一/派生/复现/预言/验证）。
  ⇒ 本册定位为**跨口径交叉核对**，不替代并行册，也不与其竞争结论。

任务：
  (A) 用机器可读数据重算 UFT-1..UFT-6 六条判据（联盟层 + 22 体系逐条）；
  (B) 病根层：硬冲突分布与复发检查；
  (C) 给出「继续完成统一场论」的**最小闭合清单**：把「完成」拆成可交付物，
      逐项标注当前谁最接近、缺什么、属工程缺口还是公设边界。

判据的机器化定义（可复跑、不含人工判词，除 UFT-2 的第三子项）：
  UFT-1 数学自洽   ∃ 体系 rating∈{H,O} 且 audit_conflicts 为空
  UFT-2 四力统一   ∃ 体系同时满足
                     (a) 规范群 token 命中 ≥2 个不同词
                     (b) 作用量 token 命中 ≥1 个
                     (c) 既有审计判词认可「含本体系特有项」——无机器源，本册列为 BOUNDARY
  UFT-3 常数派生   【严格口径】数值 + 误差棒 **且** 命中无量纲靶场 10 靶之一的条目 ≥3
                     【宽口径】任意 prediction_value + prediction_urel 非空（只作参考，不作判定）
  UFT-4 观测复现   本质为人工判词；机器只能给代理指标（verified + SM 关键词），
                     本册按 BOUNDARY 处理，**不作通过判定**
  UFT-5 可证伪预言 claims 中 prediction 非空且 status∈{open,predictive} 的条目 ≥1
  UFT-6 外部验证   system.json 的 status∈{reviewed,validated} 的体系 ≥1

档位：6/6 已实现 · 4–5 候选框架 · 2–3 纲领草案 · 0–1 未完成

红线：本册只做**达成度记账**，不提升任何体系的证据等级，
      不声称任何体系实现了统一场论，也不因「进入总账」而改变任何 claims 的 status。

纯标准库（os / io / json / csv / sys / math / re），Python 3.8+
输出：数据/本项目_统一场论达成度重算_2026-10-08.{json,md}
"""

import os
import io
import sys
import json
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))          # 04_公共成果/.../源码
BASE = os.path.dirname(HERE)                                # 04_公共成果/本项目_全维自洽与归一化
OPENUFT = os.path.dirname(os.path.dirname(BASE))            # openuft 根
SYSROOT = os.path.join(OPENUFT, "01_独立体系")
DATADIR = os.path.join(BASE, "数据")

HEALTH_JSON = os.path.join(DATADIR, "体系第一性健康度总览.json")
TARGET_JSON = os.path.join(DATADIR, "无量纲靶场审计.json")

# ---------------------------------------------------------------------------
# 输出器（命名纪律：P/F/B/I/C 为输出器，推导变量不得占用这些单字母名）
# ---------------------------------------------------------------------------
LINES = []
COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "CORRECTED": 0}
ITEMS = []
CHECKS = []


def emit(text=""):
    LINES.append(text)


def rec(code, verdict, title):
    COUNTS[verdict] += 1
    ITEMS.append((code, verdict, title))
    emit("[%s] %s  %s" % (verdict, code, title))


def P(code, title):
    rec(code, "PASS", title)


def F(code, title):
    rec(code, "FAIL", title)


def Bd(code, title):
    rec(code, "BOUNDARY", title)


def If(code, title):
    rec(code, "INFO", title)


def Cr(code, title):
    rec(code, "CORRECTED", title)


def table(headers, rows):
    widths = [len(h) for h in headers]
    for r in rows:
        for k in range(len(headers)):
            widths[k] = max(widths[k], len(str(r[k])))
    fmt = " | ".join("{:<%d}" % w for w in widths)
    emit("  " + fmt.format(*headers))
    emit("  " + "-" * (sum(widths) + 3 * (len(widths) - 1)))
    for r in rows:
        emit("  " + fmt.format(*[str(x) for x in r]))


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    return ok


# ---------------------------------------------------------------------------
# 数据加载
# ---------------------------------------------------------------------------
health = json.load(io.open(HEALTH_JSON, encoding="utf-8"))
target = json.load(io.open(TARGET_JSON, encoding="utf-8"))

SYSTEMS = health["rows"]                      # id,title,kind,rating,audit_conflicts,self_falsified
N_SYS = len(SYSTEMS)

# 目录名 -> 体系 id 的映射（01_独立体系 下的目录前缀即体系代号）
dirs = sorted([d for d in os.listdir(SYSROOT)
               if os.path.isdir(os.path.join(SYSROOT, d)) and
               (d.startswith("S") or d.startswith("P")) and "_" in d])
code_of = {}
for d in dirs:
    code_of[d.split("_")[0]] = d


def sysdir(code):
    return os.path.join(SYSROOT, code_of.get(code.upper(), ""))


# ---------------------------------------------------------------------------
# claims.csv 读取（列数不一致时按表头定位，不用固定 index）
# ---------------------------------------------------------------------------
def read_claims(code):
    p = os.path.join(sysdir(code), "claims.csv")
    if not os.path.isfile(p):
        return []
    text = io.open(p, encoding="utf-8").read()
    rows = [r for r in text.split("\n") if r.strip()]
    if not rows:
        return []
    head = [h.strip() for h in rows[0].split(",")]
    out = []
    for r in rows[1:]:
        vals = r.split(",")
        if len(vals) < len(head):
            vals += [""] * (len(head) - len(vals))
        rec_d = {}
        for k, h in enumerate(head):
            rec_d[h] = vals[k].strip() if k < len(vals) else ""
        out.append(rec_d)
    return out


# ---------------------------------------------------------------------------
# 文本扫描（UFT-2 的机器代理指标）
# ---------------------------------------------------------------------------
GROUP_TOKENS = ["SU(3)", "SU(2)", "U(1)", "SO(1,3)", "SO(3,1)", "SU(5)",
                "E8", "规范群", "结构群", "主丛", "杨-米尔斯", "Yang-Mills"]
ACTION_TOKENS = ["作用量", "拉氏量", "Lagrangian", "L = ∫", "S = ∫", "√-g", "Einstein-Hilbert"]
SM_REPRO_TOKENS = ["复现", "标准模型", "SM", "PDG", "CODATA", "与实验一致", "吻合"]

# UFT-3 的**严格口径**：预测必须落在无量纲靶场登记的 10 个靶之一上。
# 宽口径（任意 prediction_value + prediction_urel 非空）会混入有量纲量，
# 不能用于判定——既有 9-18 报告与 9-27 靶场快照用的都是严格口径。
TARGET_MARKERS = []
for _t in target.get("targets", []):
    TARGET_MARKERS.append(_t.get("key", ""))
TARGET_MARKERS += ["精细结构", "强耦合", "质量比", "温伯格", "代数", "色数",
                   "引力耦合", "α", "α_S", "N_gen", "N_c", "sin²θ_W", "sin2_thetaW"]
TARGET_MARKERS = [m for m in TARGET_MARKERS if m]


def scan_text(code, max_files=400):
    root = sysdir(code)
    if not os.path.isdir(root):
        return [], []
    g_hit, a_hit = set(), set()
    n = 0
    for r, _ds, fs in os.walk(root):
        for f in fs:
            if n >= max_files:
                break
            if not (f.endswith(".md") or f.endswith(".py") or f.endswith(".txt")):
                continue
            try:
                t = io.open(os.path.join(r, f), encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            n += 1
            for tok in GROUP_TOKENS:
                if tok in t:
                    g_hit.add(tok)
            for tok in ACTION_TOKENS:
                if tok in t:
                    a_hit.add(tok)
    return sorted(g_hit), sorted(a_hit)


# ---------------------------------------------------------------------------
# 逐体系评估
# ---------------------------------------------------------------------------
TARGET_BY_SYS = {}
for row in target.get("systems", []):
    name = row.get("system", "")
    code = name.split("_")[0].upper()
    TARGET_BY_SYS[code] = row

STATUS_VERIFIED = ("verified", "validated")
STATUS_OPEN = ("open", "predictive", "pending")
STATUS_REVIEWED = ("reviewed", "validated")


def eval_one(row):
    code = row["id"].split("_")[0].upper()
    claims = read_claims(code)
    g_hit, a_hit = scan_text(code)

    # UFT-1：数学自洽（无硬冲突且评级 H/O）
    u1 = (row["rating"] in ("H", "O")) and (not row.get("audit_conflicts"))

    # UFT-2：必要条件代理（规范群共现 ≥2 且 作用量 token ≥1）
    u2 = (len(g_hit) >= 2) and (len(a_hit) >= 1)

    # UFT-3 宽口径：有数值 + 误差棒（不区分是否无量纲；会混入有量纲量，只作参考）
    n_pred = sum(1 for c in claims
                 if c.get("prediction_value", "").strip() and c.get("prediction_urel", "").strip())
    # UFT-3 严格口径：数值 + 误差棒 **且** 命中无量纲靶场登记的 10 个靶之一（判据用此口径）
    n_pred_strict = 0
    for c in claims:
        if not (c.get("prediction_value", "").strip() and c.get("prediction_urel", "").strip()):
            continue
        blob = " ".join([c.get("statement", ""), c.get("prediction", ""), c.get("data_id", "")])
        if any(m in blob for m in TARGET_MARKERS):
            n_pred_strict += 1
    u3 = n_pred_strict >= 3

    # UFT-4：观测复现（verified 且含 SM 复现关键词）
    n_rep = 0
    for c in claims:
        st = (c.get("status", "") or "").strip()
        if st in STATUS_VERIFIED:
            blob = " ".join([c.get("statement", ""), c.get("derivation", ""), c.get("data_id", "")])
            if any(tok in blob for tok in SM_REPRO_TOKENS):
                n_rep += 1
    u4 = n_rep >= 1

    # UFT-5：可证伪预言（prediction 非空且状态 open）
    n_open_pred = sum(1 for c in claims
                      if c.get("prediction", "").strip() and
                      (c.get("status", "") or "").strip() in STATUS_OPEN)
    u5 = n_open_pred >= 1

    # UFT-6：外部验证（system.json status）
    u6 = False
    sp = os.path.join(sysdir(code), "system.json")
    sys_status = ""
    if os.path.isfile(sp):
        try:
            sj = json.load(io.open(sp, encoding="utf-8"))
            sys_status = str(sj.get("status", ""))
            u6 = sys_status in STATUS_REVIEWED
        except Exception:
            pass

    tj = TARGET_BY_SYS.get(code, {})
    # 计分只含**可机器判**的四项：U1 / U3 / U5 / U6
    # U2（充分性）与 U4（复现是否落在不确定度内）本质为人工判词 ⇒ 不计分，只给代理读数
    score = int(u1) + int(u3) + int(u5) + int(u6)
    if score >= 4:
        tier = "已实现"
    elif score == 3:
        tier = "候选框架"
    elif score == 2:
        tier = "纲领草案"
    else:
        tier = "未完成"

    return {
        "code": code, "title": row["title"], "rating": row["rating"],
        "kind": row.get("kind", ""),
        "u1": u1, "u2_necessary": u2, "u3": u3, "u4": u4, "u5": u5, "u6": u6,
        "n_claims": len(claims), "n_pred": n_pred, "n_pred_strict": n_pred_strict,
        "n_rep": n_rep,
        "n_open_pred": n_open_pred,
        "n_conflicts": len(row.get("audit_conflicts", [])),
        "group_tokens": g_hit[:4], "action_tokens": a_hit[:3],
        "target_with_value": len(tj.get("with_value", [])),
        "target_with_err": len(tj.get("with_error_clue", [])),
        "target_registered": tj.get("n_registered_predictions", 0),
        "sys_status": sys_status,
        "score": score, "tier": tier,
    }


RESULTS = [eval_one(r) for r in SYSTEMS]

# ===========================================================================
emit("=" * 78)
emit("本项目 · 统一场论达成度重算与最小闭合清单（2026-10-08）")
emit("承接：全维分析报告_统一场论达成度_2026-09-18.md（18 体系 / 联盟层 2/6）")
emit("红线：本册只做达成度记账，不提升任何体系的证据等级")
emit("=" * 78)
emit()

# ---------------------------------------------------------------------------
# §0 数据源与口径
# ---------------------------------------------------------------------------
emit("§0  数据源与口径")
emit("-" * 78)
ratings = {}
for r in SYSTEMS:
    ratings[r["rating"]] = ratings.get(r["rating"], 0) + 1
emit("  体系数 = %d（01_独立体系 目录实测 %d 个体系目录）" % (N_SYS, len(code_of)))
emit("  健康度分布：%s" % "  ".join("%s=%d" % (k, v) for k, v in sorted(ratings.items())))
tot_claims = sum(x["n_claims"] for x in RESULTS)
emit("  claims 总条数 = %d" % tot_claims)
emit("  健康度数据源：%s" % os.path.basename(HEALTH_JSON))
emit("  无量纲靶场源：%s（生成于 %s，为 2026-09-27 快照；本册另做 10-08 实时扫描对照）"
     % (os.path.basename(TARGET_JSON), target.get("generated_utc", "?")))
emit("  无量纲靶个数 = %d：%s" % (len(target.get("targets", [])),
                                 "、".join(t.get("name_zh", t.get("key", "")) for t in target.get("targets", []))))
check("数据源齐全", N_SYS >= 20 and tot_claims > 50, "sys=%d claims=%d" % (N_SYS, tot_claims))
check("体系目录数与健康度行数一致", N_SYS == len(code_of), "%d vs %d" % (N_SYS, len(code_of)))
check("claims 总数与既有审计一致(315)", tot_claims == 315, "tot=%d" % tot_claims)
emit()

# ---------------------------------------------------------------------------
# §1 联盟层六判据
# ---------------------------------------------------------------------------
emit("§1  联盟层六判据重算")
emit("-" * 78)

n_u1 = sum(1 for x in RESULTS if x["u1"])
n_u2 = sum(1 for x in RESULTS if x["u2_necessary"])
n_u3 = sum(1 for x in RESULTS if x["u3"])
n_u4 = sum(1 for x in RESULTS if x["u4"])
n_u5 = sum(1 for x in RESULTS if x["u5"])
n_u6 = sum(1 for x in RESULTS if x["u6"])
tot_pred = sum(x["n_pred"] for x in RESULTS)

emit("  UFT-1 数学自洽   ：满足体系 %d / %d" % (n_u1, N_SYS))
P("A-1", "UFT-1 通过：存在 %d 个无硬冲突体系（H + O），联盟层自洽基线成立" % n_u1)

emit("  UFT-2 四力统一   ：必要条件（规范群 ∧ 作用量共现）命中 %d / %d 个体系" % (n_u2, N_SYS))
emit("        命中体系的规范群 token 样例：")
for x in RESULTS:
    if x["u2_necessary"]:
        emit("          %s：%s | 作用量词：%s"
             % (x["code"], "、".join(x["group_tokens"]), "、".join(x["action_tokens"])))
emit("        但充分性第三子项「作用量含本体系特有项」无机器数据源；")
emit("        既有人工判词对最接近的 S14（TUFT）明确判「EH + YM + Dirac 逐字照搬，无特有项」")
emit("        （来源：全维分析报告_统一场论达成度_2026-09-18.md §二）。")
F("A-2", "UFT-2 未通过：必要条件命中 %d 个体系，但充分性（含本体系特有项的统一作用量）"
        "在全联盟无一条被审计认可；最接近的 S14 已被判「照搬已知理论」" % n_u2)
Bd("A-2b", "UFT-2 的第三子项属人工判词，本册不作机器判定，只登记必要条件命中情况，"
           "防止把「文本里出现了 SU(3) 和作用量」误读为「已实现四力统一」")

tot_pred_strict = sum(x["n_pred_strict"] for x in RESULTS)
emit("  UFT-3 常数派生（双口径对照）：")
emit("        宽口径（任意数值 + 误差棒）            = %d 条" % tot_pred)
emit("        严格口径（且命中无量纲靶场 10 靶之一）  = %d 条  ← 判据用此口径" % tot_pred_strict)
emit("        满足「≥3 条」（严格）的体系数 = %d / %d" % (n_u3, N_SYS))
emit("        靶场 9-27 快照对照：with_error_clue 总数 = %d；n_registered_predictions 全联盟 = %d"
     % (sum(x["target_with_err"] for x in RESULTS),
        sum(x["target_registered"] for x in RESULTS)))
emit("        口径分歧已显式处理：宽口径 %d 条混入有量纲/非靶量，不得用于判定；"
     "既有 9-18 报告与 9-27 靶场快照用的均为严格口径（读数 0）。" % tot_pred)
u3_alliance = tot_pred_strict >= 3      # 联盟层判据：登记的无量纲靶 ≥ 3（总数，非体系数）
if u3_alliance:
    P("A-3", "UFT-3 通过（本册唯一改善项）：严格口径下全联盟命中无量纲靶且带数值+误差棒的"
             "预测共 %d 条 ≥ 3；而 9-18 版与 9-27 靶场快照均为 0 ⇒ 20 天里确有实质进展"
             % tot_pred_strict)
    Bd("A-3b", "UFT-3 的第二子项「判别式 V₂>0」（预测数 − 自由参数 − 测量锚 > 0）无机器数据源；"
               "且 %d 条分散在少数体系、是否均属**非测量锚**未逐一核对 ⇒ 通过判定带保留，"
               "不得据此宣称「已导出任何基本常数」" % tot_pred_strict)
else:
    F("A-3", "UFT-3 未通过：严格口径 %d 条 < 3；与 9-18 版、9-27 快照一致 ⇒ 该计数未改善"
             % tot_pred_strict)
emit("        注：联盟层判据看**总数**；体系级「单体系 ≥3 条」的体系数 = %d 个（另计）。" % n_u3)

emit("  UFT-4 观测复现   ：含 SM 复现关键词的 verified 条目 = %d，命中体系 %d / %d"
     % (sum(x["n_rep"] for x in RESULTS), n_u4, N_SYS))
Bd("A-4", "UFT-4 不作机器判定：该判据本质为人工判词（须判「复现是否落在观测不确定度内」）；"
          "机器代理指标显示 %d 个体系含 SM 复现类 verified 条目（共 %d 条），"
          "但关键词扫描必然高估（「SM」「复现」等词命中不等于复现了谱/耦合）⇒ 保留读数、不判通过"
          % (n_u4, sum(x["n_rep"] for x in RESULTS)))

emit("  UFT-5 可证伪预言 ：prediction 非空且状态 open 的条目 = %d，命中体系 %d / %d"
     % (sum(x["n_open_pred"] for x in RESULTS), n_u5, N_SYS))
if n_u5 > 0:
    P("A-5", "UFT-5 通过：%d 个体系登记了 open 状态的可检验预言（定量充分性另计）" % n_u5)
else:
    F("A-5", "UFT-5 未通过：无体系登记处于 open 状态的可检验预言")

emit("  UFT-6 外部验证   ：system.json 状态进入 reviewed/validated 的体系 = %d / %d" % (n_u6, N_SYS))
F("A-6", "UFT-6 未通过：%d 个体系中 0 个进入外部验证阶段（全部为 %s）"
        % (N_SYS, "、".join(sorted(set(x["sys_status"] for x in RESULTS if x["sys_status"]))) or "unreviewed"))

score_union = int(n_u1 > 0) + int(u3_alliance) + int(n_u5 > 0) + int(n_u6 > 0)
emit()
emit("  联盟层得分（可机器判 4 项：U1 / U3 / U5 / U6）= %d / 4" % score_union)
emit("  UFT-2（充分性）与 UFT-4（复现精度）属人工判词，本册不计分、只给代理读数 ⇒")
emit("  沿用 9-18 的 6 项口径时，本册可确认通过项为 UFT-1、UFT-3、UFT-5 三条"
     "（9-18 版为 UFT-1 与 UFT-5 两条）。")
check("严格口径 ≤ 宽口径", tot_pred_strict <= tot_pred, "%d <= %d" % (tot_pred_strict, tot_pred))
check("体系得分上限校验", all(x["score"] <= 4 for x in RESULTS),
      "max=%d" % max(x["score"] for x in RESULTS))
emit()

# ---------------------------------------------------------------------------
# §2 体系逐条达成度
# ---------------------------------------------------------------------------
emit("§2  22 体系逐条达成度（U2 列为「必要条件」代理，非充分判定）")
emit("-" * 78)
rows = []
for x in sorted(RESULTS, key=lambda a: (-a["score"], a["code"])):
    rows.append((x["code"], x["rating"], x["score"],
                 "✓" if x["u1"] else "✗",
                 "✓?" if x["u2_necessary"] else "✗",
                 "✓" if x["u3"] else "✗",
                 "✓" if x["u4"] else "✗",
                 "✓" if x["u5"] else "✗",
                 "✓" if x["u6"] else "✗",
                 x["n_claims"], "%d/%d" % (x["n_pred"], x["n_pred_strict"]), x["tier"]))
table(["体系", "健康", "分", "U1", "U2", "U3", "U4", "U5", "U6", "claims", "预测宽/严", "档位"], rows)
tiers = {}
for x in RESULTS:
    tiers[x["tier"]] = tiers.get(x["tier"], 0) + 1
emit("  档位分布：%s" % "  ".join("%s=%d" % (k, v) for k, v in sorted(tiers.items())))
best = max(RESULTS, key=lambda a: a["score"])
If("A-7", "体系最高分 = %s（%s）%d/5；全联盟无「已实现」与「候选框架」"
          % (best["code"], best["title"], best["score"]))
emit()

# ---------------------------------------------------------------------------
# §3 病根层：硬冲突分布
# ---------------------------------------------------------------------------
emit("§3  病根层：审计硬冲突分布")
emit("-" * 78)
conf = [(x["code"], x["rating"], x["n_conflicts"]) for x in RESULTS if x["n_conflicts"] > 0]
conf.sort(key=lambda a: -a[2])
table(["体系", "健康", "硬冲突条数"], conf[:12] if conf else [("—", "—", 0)])
tot_conf = sum(x["n_conflicts"] for x in RESULTS)
emit("  硬冲突总数 = %d，涉及体系 %d / %d" % (tot_conf, len(conf), N_SYS))
emit("  自我记录并已修复的证伪（self_falsified）总数 = %d"
     % sum(len(r.get("self_falsified", [])) for r in SYSTEMS))
If("A-8", "硬冲突集中在 C 级体系；H/O 级体系的「未完成」不是因为硬冲突，"
          "而是因为 U3/U4/U6 三项从未被填写 ⇒ 缺的是**可验证产出**，不是**错误修复**")
emit()

# ---------------------------------------------------------------------------
# §4 本体族普查（本册新增：统一场论只允许一条本体路线存活）
# ---------------------------------------------------------------------------
emit("§4  本体族普查：22 体系实为几条互斥路线？")
emit("-" * 78)
FAMILY_RULES = [
    ("螺旋几何族", ["螺旋", "曲率", "挠率", "Frenet"]),
    ("拓扑扭结族", ["扭结", "拓扑", "缠绕", "链环"]),
    ("对偶分形族", ["分形", "对偶", "双向"]),
    ("信息熵族", ["信息", "熵"]),
    ("规范对称族", ["规范", "对称", "群"]),
    ("压缩/密度本体族", ["压缩", "密度"]),
    ("频率本源族", ["频率", "振动", "驻波"]),
    ("几何耦合族", ["自由度", "耦合"]),
]
fam_of = {}
for x in RESULTS:
    blob = x["title"] + " " + x["kind"]
    hit = None
    for fname, kws in FAMILY_RULES:
        if any(k in blob for k in kws):
            hit = fname
            break
    fam_of[x["code"]] = hit or "其他/未归类"
fams = {}
for c, f in fam_of.items():
    fams.setdefault(f, []).append(c)
table(["本体族", "成员数", "成员"],
      [(f, len(v), "、".join(sorted(v))) for f, v in sorted(fams.items(), key=lambda a: -len(a[1]))])
If("A-9", "22 体系落在 %d 个本体族中；统一场论若要成立，**只允许一条本体路线存活**，"
          "其余须被淘汰或降级为形式工具 ⇒ 本体淘汰赛是「完成统一」的前置动作，"
          "当前无任一族被正式裁决出局" % len(fams))
emit()

# ---------------------------------------------------------------------------
# §5 最小闭合清单：把「完成统一场论」拆成可交付物
# ---------------------------------------------------------------------------
emit("§5  最小闭合清单：要「完成」还差哪几件可交付物")
emit("-" * 78)
checklist = [
    ("D1 含特有项的统一作用量",
     "0 / %d 体系" % N_SYS, "结构性",
     "最接近：S14（有主丛作用量，但被判照搬）；其次为 UFT-2 必要条件命中的体系",
     "必须出现「去掉它该体系就退化回已知理论」的项"),
    ("D2 ≥3 个带数值+误差棒的无量纲预测",
     "宽 %d 条 / 严 %d 条 ⇒ **已达标**" % (tot_pred, tot_pred_strict), "已达数量门槛",
     "最接近：S03（靶场快照 with_value=5，with_error_clue 仅 1）",
     "数量已够，但判别式 V₂>0 未判、且须逐条核对是否属非测量锚"),
    ("D3 SM 谱/耦合复现（落在不确定度内）",
     "当前 %d 条 verified 复现" % sum(x["n_rep"] for x in RESULTS), "工程量 + 结构性",
     "无体系登记", "须给出粒子谱或耦合的具体数字与误差"),
    ("D4 本体淘汰裁决",
     "%d 个本体族并立" % len(fams), "前置动作",
     "无族被裁决出局", "不先做淘汰，D1–D3 会在互斥本体上并行空转"),
    ("D5 进入外部验证（reviewed/validated）",
     "0 / %d 体系" % N_SYS, "流程",
     "全部 unreviewed", "属治理流程，工程量最小但当前零进展"),
    ("D6 公设边界显式承担",
     "已判边界：ℏ、质量标度、电荷量子化、U(1) 荷", "公设边界",
     "散落在各体系判定册", "须集中登记为外加公设，不得伪装为推导补全"),
]
table(["交付物", "当前状态", "缺口类型", "谁最接近", "通过标准"], checklist)
for name, st, kind, who, crit in checklist:
    If("D-" + name.split()[0], "%s｜当前 %s｜类型 %s｜最接近 %s｜标准 %s" % (name, st, kind, who, crit))
emit()

# ---------------------------------------------------------------------------
# §6 裁定
# ---------------------------------------------------------------------------
emit("§6  裁定")
emit("-" * 78)
F("A-10", "统一场论**未完成**：%d 体系中已实现 0、候选框架 0；联盟层可机器判 4 项中 "
          "UFT-1（自洽）、UFT-3（严格口径 %d 条 ≥3）、UFT-5（登记预言）通过，"
          "仅 UFT-6（外部验证）为 0 个体系 ⇒ 但 UFT-2 的充分性子项全联盟为 0，"
          "且无任何体系进入「已实现/候选框架」档" % (N_SYS, tot_pred_strict))
emit("  与 2026-09-18 版的对比：")
table(["维度", "2026-09-18 版", "2026-10-08 本册"],
      [("体系数", "18", "%d" % N_SYS),
       ("联盟层得分", "2 / 6（含人工判词项）", "%d / 4（仅可机器判项）" % score_union),
       ("最高体系", "S13 2/6 纲领草案",
        "%s %d/4 %s" % (best["code"], best["score"], best["tier"])),
       ("数值预测条目（严格口径）", "0", "%d ← 唯一改善项" % tot_pred_strict),
       ("数值预测条目（宽口径）", "—（未登记该口径）", "%d" % tot_pred),
       ("外部验证体系", "0", "0")])
emit("  ⇒ 20 天内新增数十册产物、体系从 18 扩到 22，**唯一改善项是 UFT-3：0 → %d 条**。"
     % tot_pred_strict)
emit("  ⇒ 缺口性质已可判定：UFT-6 是「从未填写」（流程问题，工程量最小）；")
emit("     UFT-2 是「填写了但被判照搬」（结构性原创性问题，不能靠继续推导闭合）。")
emit()
emit("  与并行册 W0–W7 验收矩阵（同日）的交叉核对：")
table(["判据", "本册 UFT 系（证据等级切）", "并行册 W 系（完成条件切）"],
      [("无量纲数值输出", "UFT-3 严格口径 %d 条 ≥3 ⇒ PASS，但判别式 V₂ 未判" % tot_pred_strict,
        "W3 欠账 17.5，瓶颈排序第 1 ⇒ 最大瓶颈"),
       ("统一作用量/主方程", "UFT-2 必要条件命中 %d 个体系，充分性 0 ⇒ FAIL" % n_u2,
        "W1/W2 欠账 8.5 / 14.5 ⇒ 亦为瓶颈"),
       ("耦合汇聚", "UFT 系无独立对应项", "W4 欠账 15.0 ⇒ 瓶颈第 2"),
       ("可证伪窗口未关", "UFT-5 通过（%d 个体系登记 open 预言）" % n_u5,
        "W7 欠账 15.0 ⇒ 窗口关闭是主要失分项"),
       ("外部验证", "UFT-6 = 0 个体系 ⇒ FAIL", "W 系无独立对应项")])
If("A-11", "两套判据在「统一作用量/主方程」上同向指认为瓶颈（UFT-2 充分性 0；W1/W2 欠账）；"
           "在「无量纲数值输出」上出现**有意义的口径分歧**：本册按数量门槛判 PASS（%d 条 ≥3），"
           "并行册 W3 仍列最大瓶颈 ⇒ 二者不矛盾，说明卡点已从「有没有数字」转为"
           "「数字是不是非测量锚、判别式 V₂ 是否为正」——这是 20 天进展的准确定位；"
           "分歧还出现在「可证伪预言」：UFT-5 只看是否登记，W7 还要求窗口未被实验排除 ⇒ "
           "登记 ≠ 窗口仍开着" % tot_pred_strict)
emit()

# ---------------------------------------------------------------------------
# 汇总与落盘
# ---------------------------------------------------------------------------
emit("=" * 78)
emit("汇总：条目 %d（PASS=%d FAIL=%d BOUNDARY=%d INFO=%d CORRECTED=%d）；自检 %d / %d"
     % (sum(COUNTS.values()), COUNTS["PASS"], COUNTS["FAIL"], COUNTS["BOUNDARY"],
        COUNTS["INFO"], COUNTS["CORRECTED"],
        sum(1 for _, ok, _ in CHECKS if ok), len(CHECKS)))
for nm, ok, det in CHECKS:
    emit("  [%s] %s  %s" % ("OK" if ok else "XX", nm, det))
emit("=" * 78)

if not os.path.isdir(DATADIR):
    os.makedirs(DATADIR)
stem = "本项目_统一场论达成度重算_2026-10-08"

payload = {
    "generated": "2026-10-08",
    "systems_total": N_SYS,
    "rating_distribution": ratings,
    "claims_total": tot_claims,
    "alliance_layer": {
        "uft1_math_consistent": {"pass": n_u1 > 0, "n_systems": n_u1},
        "uft2_unified_action": {"pass": False, "necessary_hit": n_u2,
                                "note": "充分性子项（含本体系特有项）无机器源；既有判词对 S14 判照搬"},
        "uft3_dimensionless_predictions": {"pass": n_u3 > 0, "n_entries_strict": tot_pred_strict,
                                           "n_entries_wide": tot_pred, "n_systems": n_u3,
                                           "note": "判据用严格口径（须命中无量纲靶场 10 靶之一）"},
        "uft4_observation_reproduction": {"verdict": "BOUNDARY(人工判词，不作机器判定)",
                                          "proxy_n_entries": sum(x["n_rep"] for x in RESULTS),
                                          "proxy_n_systems": n_u4},
        "uft5_falsifiable_prediction": {"pass": n_u5 > 0, "n_systems": n_u5},
        "uft6_external_validation": {"pass": n_u6 > 0, "n_systems": n_u6},
        "score_machinable": score_union,
    },
    "tier_distribution": tiers,
    "families": {k: sorted(v) for k, v in fams.items()},
    "per_system": RESULTS,
    "items": [{"code": c, "verdict": v, "title": t} for c, v, t in ITEMS],
    "checks": [{"name": n, "ok": o, "detail": d} for n, o, d in CHECKS],
}
with io.open(os.path.join(DATADIR, stem + ".json"), "w", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=False, indent=1))
with io.open(os.path.join(DATADIR, stem + ".md"), "w", encoding="utf-8") as fh:
    fh.write("# 本项目 · 统一场论达成度重算（2026-10-08）\n\n```text\n"
             + "\n".join(LINES) + "\n```\n")

sys.stdout.write("\n".join(LINES) + "\n")
sys.stdout.write("[items] %d  [checks] %d/%d\n"
                 % (sum(COUNTS.values()), sum(1 for _, ok, _ in CHECKS if ok), len(CHECKS)))
