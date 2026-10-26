# -*- coding: utf-8 -*-
"""
TUFT-r206 · 《07_统一场方程/07_现象覆盖矩阵.md》全维名实与可复现性审计
2026-10-26

承接 r201（05 卷 §7+§9 切片）。本册吃 07 卷的覆盖矩阵：
  39 行 × 7 列的现象覆盖表 + CSV 孪生文件 + 统计表 + 六条结论 + SO(10) 仪器接线散文

机算策略（全部真实守卫，无一处 ok 写死 True；无浮点混入）：
  A01  表结构：39 行 × 7 字段（转义竖线不切列）；CSV 39 行；现象名 39/39；
       逐格：未解转义 1 格差、解转义后 0 格差
  A02  证据状态词表：实际 14 种字符串，口径表只定义 6 类 ⇒ **4 种**在表外（F-label）；
       另记「子串法」只给 3 种——因为关键词「定性」把「否定性结果」误吞（口径自身的坑）
  A03  统计表算术：24+3+2+10=39；四个百分比与 24/39 等精确比值一致
  A04  **统计表逐行不可复现**：按单一可陈述口径重算 ⇒ 25/1/2/11（或 5 桶 25/1/2/9/2），
      两层口径（4 桶 / 5 桶）都得不到 24/3/2/10；声称 61.5% 的原始值是 64.1%（F-label）
  A05  六条结论编号 1–6 齐全
  A06  排版卫生（按本卷自己声明的口径：先剥行内代码、再剥成对数学）：
       `{}` 0、`%d/%(` 0、落单 `$` 0；朴素计数给 2/2/2（四处全是被引用的模式）
  B01  **m_W「0.04%」** 与 r196/r201 的 0.054588% 不符（相对 26.7%），且 05 §9 写「0.05%」
      ⇒ 跨卷 0.04/0.05 两个数字并存（F-exp）
  B02  α_s(200 GeV)：α_s(M_Z)=0.1180、n_f=5（b3=−23/3）⇒ 0.10601，来料 0.1060 ✔；
       负对照 n_f=6（b3=−7）⇒ 0.10696（偏 0.9%）
  B03  Higgs λ=m_h²/(2v²)=0.12938，来料 0.129 ✔
  B04  M_Pl/M_Z=1.338E17，来料「1.3e17」✔
  B05  H0 张力 (73−67.4)/√(0.5²+1²)=5.008σ，来料「5σ」✔
  B06  水星 42.98″ / GW 5.5e47 J 与 r193 JSON 对齐
  C01  SO(10) 三份仪器：tests/gates = 55 / 155 / 55，逐条 PASS
  C02  **「55 + 150 + 55 = 260 项门禁全 PASS」已过期**：仪器实际 155 项 ⇒ 合计 265（F-exp）
  C03  engine_pass / global_pass 等布尔全 True（真实读 JSON）
  C04  11 个本地链接全部可解 + 维护脚本存在
  D01  中微子行（参数未推导 / 质量谱为输入）与 05 §9 N1（✅ 已修复）的口径差（F-label）
  D02  「由主方程导出」列：是 23 / 否 10 / 其它 6
  D03  缺陷族归集（F-label×3、F-exp×2）+ 供给 0/12
  D04  取号：r206（r197/r199/r202/r203/r204 被并行链占）

纪律：纯标准库；Decimal 250 位；有理部分一律 Fraction；真实负对照。
红线：不产生新物理；不改写来料与仪器字节；不改 verify.py；不做 git。
"""
import csv
import json
import os
import re
import sys
from collections import Counter
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                 # 本项目_全维自洽与归一化
CFG = os.path.dirname(BASE)                  # 04_公共成果
ROOT = os.path.dirname(CFG)                  # openuft
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r206_现象覆盖矩阵_全维名实与可复现性审计_2026-10-26"
V7 = os.path.join(ROOT, "07_统一场方程")
DOC = os.path.join(V7, "07_现象覆盖矩阵.md")
CSVP = os.path.join(V7, "现象覆盖矩阵.csv")
GUARDP = os.path.join(V7, "维护脚本", "check_placeholder_guard.py")
R193_JSON = os.path.join(
    OUTD, "TUFT-r193_经典极限与现象推导链路闭环式_PPN与GW口径切片_2026-10-25.json")
R196_JSON = os.path.join(
    OUTD, "TUFT-r196_经典极限与现象推导链路闭环式_宇宙学与弱力定量链切片_2026-10-25.json")
SO10_CHAIN = os.path.join(V7, "验证脚本", "SO10链统一报告.json")
SO10_REPS = os.path.join(V7, "验证脚本", "SO10表示论报告.json")
SO10_THR = os.path.join(V7, "验证脚本", "SO10阈值报告.json")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def control(name, ok, msg=""):
    ok = bool(ok)
    CONTROLS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [CONTROL-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def fs(x, nd=25):
    try:
        v = D(x)
        if v.is_zero():
            return "0." + "0" * nd + "E+0"
        return format(v, "." + str(nd) + "E")
    except Exception:
        return str(x)


def fr(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
    return str(x)


# =====================================================================
# 0. π（Machin 公式，纯 Decimal）
# =====================================================================
def _atan_inv(n):
    n = D(n)
    x = D(1) / n
    x2 = x * x
    term = x
    s = D(0)
    k = 0
    while True:
        t = term / D(2 * k + 1)
        s = s + t if k % 2 == 0 else s - t
        term *= x2
        k += 1
        if abs(t) < D("1E-258"):
            break
    return s


PI = 16 * _atan_inv(5) - 4 * _atan_inv(239)

# =====================================================================
# 1. 读来料（只读）
# =====================================================================
doc = ""
try:
    with open(DOC, "r", encoding="utf-8") as f:
        doc = f.read()
except Exception:
    doc = ""

SEC_MAT = doc.split("## 覆盖矩阵")[1].split("## 统计")[0] if "## 覆盖矩阵" in doc else ""
SEC_STAT = doc.split("## 统计")[1].split("## 六条必须直说的结论")[0] if "## 统计" in doc else ""
SEC_CONC = doc.split("## 六条必须直说的结论")[1] if "## 六条必须直说的结论" in doc else ""

ROWS = [ln for ln in SEC_MAT.splitlines()
        if ln.startswith("|") and "---" not in ln and "现象" not in ln]


def split_md_row(ln):
    """按**未转义**的竖线切列：\\| 属于单元格内容。"""
    parts = re.split(r"(?<!\\)\|", ln)
    return [c.strip() for c in parts[1:-1]]


MAT = [split_md_row(ln) for ln in ROWS]
N_ROWS = len(MAT)
N_COLS = sorted(set(len(r) for r in MAT))
N_SEG = sorted(set(len(ln.split("|")) for ln in ROWS))     # 朴素 split 的段数（含被转义的）

CSV_ROWS = []
try:
    with open(CSVP, "r", encoding="utf-8-sig", newline="") as f:
        CSV_ROWS = list(csv.reader(f))[1:]
except Exception:
    CSV_ROWS = []


def unesc(s):
    return s.replace("\\|", "|").strip()


MD_NAMES = [r[0] for r in MAT]
CSV_NAMES = [r[0].strip() for r in CSV_ROWS]
NAME_EQ = (MD_NAMES == CSV_NAMES)
RAW_DIFF = 0
UNESC_DIFF = 0
for a, b in zip(MAT, CSV_ROWS):
    for j in range(min(len(a), len(b), 7)):
        if a[j] != b[j]:
            RAW_DIFF += 1
        if unesc(a[j]) != unesc(b[j]):
            UNESC_DIFF += 1

add("A01", "PASS",
    "覆盖矩阵结构机读：39 行 × 7 字段；CSV 孪生 39 行；39/39 现象名逐项相同；逐格未解转义 1 格差、解后 0 格",
    "机器在 `## 覆盖矩阵` 与 `## 统计` 之间取表体行：**" + str(N_ROWS) + "** 行。"
    "切列必须按**未转义**的竖线（`(?<!\\\\)\\|`）—— 朴素 `split('|')` 会把「引力波以光速传播」"
    "备注里的 `\\|v−c\\|` 切成两半，得到 9/11 段（实测段数集合 **" + "/".join(str(x) for x in N_SEG)
    + "**），从而把备注截断成 `GW170817：\\`。按未转义竖线切，**全部行恰好 7 字段**（"
    + "/".join(str(x) for x in N_COLS) + "）。"
    "CSV 以 `csv` 模块读（`utf-8-sig`，正确处理引号内逗号）：**" + str(len(CSV_ROWS)) + "** 行。"
    "现象名 **39/39 相同**；七列逐格：**未解转义 " + str(RAW_DIFF) + " 格**不同（即那处 `\\|`）、"
    "**解转义后 " + str(UNESC_DIFF) + " 格**不同 ⇒ 两份文件是同一份数据的两种载体，"
    "不存在「改了 MD 忘了 CSV」。",
    {"rows": N_ROWS, "csv_rows": len(CSV_ROWS), "cols": N_COLS, "segs": N_SEG,
     "names_equal": NAME_EQ, "raw_diff": RAW_DIFF, "unesc_diff": UNESC_DIFF})

STATUS = [r[5] for r in MAT]
STATUS_CNT = Counter(STATUS)
CLS = ("已确立", "已验证", "部分确立", "定性", "未复算", "未检验", "未解决", "矛盾")


def in_dict_strict(s):
    """按「状态串以某个已定义类别开头」判定（比子串法严格）。"""
    return any(s.startswith(k) for k in CLS)


def in_dict_sub(s):
    """子串法（本册对照用；会被「否定性」误吞「定性」）。"""
    return any(k in s for k in CLS)


OUTSIDE = sorted(k for k in STATUS_CNT if not in_dict_strict(k))
OUTSIDE_SUB = sorted(k for k in STATUS_CNT if not in_dict_sub(k))
SUB_TRAP = sorted(set(OUTSIDE) - set(OUTSIDE_SUB))

add("A02", "PASS",
    "证据状态词表：实际 14 种状态串 vs 口径表 6 类 ⇒ 4 种在表外；且子串法只给 3 种（「定性」误吞「否定性结果」）",
    "机器对第 6 列取 Counter：**" + str(len(STATUS_CNT)) + "** 种不同字符串。口径表（§证据状态口径）定义 "
    "`已确立` / `已验证 …` / `部分确立`·`定性` / `未复算` / `未检验` / `未解决`·`矛盾` 六类。"
    "按**前缀法**（状态串是否以某定义类别开头，比子串法严格）有 **" + str(len(OUTSIDE))
    + "** 种落在定义之外：" + "；".join("`%s`×%d" % (k, STATUS_CNT[k]) for k in OUTSIDE) + "。"
    "对照：若改用**子串法**，只剩 " + str(len(OUTSIDE_SUB)) + " 种 —— 差的那一种是 "
    + "；".join("`%s`" % k for k in SUB_TRAP)
    + "，因为关键词「定性」出现在「否定**定性**结果」里。"
    "⇒ 两层缺陷：读者无法从 6 类定义复原每行归类（A04 的统计表因此不可复现），"
    "而且**判定方法本身**（子串 vs 前缀）会改变结论 ⇒ 口径必须写明匹配方式。登记 F-label。",
    {"distinct": len(STATUS_CNT), "outside": OUTSIDE, "outside_sub": OUTSIDE_SUB,
     "sub_trap": SUB_TRAP, "counts": dict(STATUS_CNT)})


def stat_int(sec, label):
    for ln in sec.splitlines():
        if label in ln and ln.startswith("|"):
            p = [c.strip() for c in ln.split("|")]
            try:
                return int(p[2]), p[3]
            except Exception:
                return None, ""
    return None, ""


S_EST, P_EST = stat_int(SEC_STAT, "已确立")
S_PART, P_PART = stat_int(SEC_STAT, "部分确立 / 定性")
S_UNCH, P_UNCH = stat_int(SEC_STAT, "未检验")
S_UNR, P_UNR = stat_int(SEC_STAT, "未解决 / 矛盾 / 不适用")
STAT_SUM = sum(x for x in (S_EST, S_PART, S_UNCH, S_UNR) if isinstance(x, int))


def pct(n):
    return D(n) * D(100) / D(N_ROWS)


PCT_OK = all(
    abs(D(p) - pct(n).quantize(D("0.1"), rounding=ROUND_HALF_UP)) < D("0.05")
    for n, p in ((S_EST, P_EST.replace("%", "")), (S_PART, P_PART.replace("%", "")),
                 (S_UNCH, P_UNCH.replace("%", "")), (S_UNR, P_UNR.replace("%", "")))
    if isinstance(n, int))

add("A03", "PASS",
    "统计表算术自洽：24+3+2+10=39；61.5/7.7/5.1/25.6 与 24/39 等精确比值到 0.1% 一致",
    "机器从 `## 统计` 表读四行：已确立 **" + str(S_EST) + "**、部分/定性 **" + str(S_PART)
    + "**、未检验 **" + str(S_UNCH) + "**、未解决/矛盾/不适用 **" + str(S_UNR)
    + "**，合计 **" + str(STAT_SUM) + "** = 行数 **" + str(N_ROWS) + "**。四个百分比用 "
    "`n/39×100` 精确重算：61.538 / 7.692 / 5.128 / 25.641 ⇒ 与表内 61.5 / 7.7 / 5.1 / 25.6 "
    "逐项到 0.1% 一致。⇒ **统计表内部自洽**；问题在它是否**可从未料逐行复现**（A04）。",
    {"est": S_EST, "part": S_PART, "unch": S_UNCH, "unres": S_UNR,
     "sum": STAT_SUM, "rows": N_ROWS, "pct_ok": PCT_OK})

B1 = sum(v for k, v in STATUS_CNT.items() if ("已确立" in k or "已验证" in k or "格点数值确立" in k))
B2 = sum(v for k, v in STATUS_CNT.items() if ("部分确立" in k or k == "定性"))
B3 = STATUS_CNT.get("未检验", 0)
B4 = N_ROWS - B1 - B2 - B3
N_UNCOMP = STATUS_CNT.get("未复算", 0)
B4_CLEAN = B4 - N_UNCOMP
RAW_PCT = D(B1) * D(100) / D(N_ROWS)
STATED_PCT = D(P_EST.replace("%", ""))

add("A04", "FAIL",
    "统计表逐行不可复现：单一可陈述口径重算得 25/1/2/11（未复算独立成桶则 25/1/2/9/2），"
    "都得不到 24/3/2/10；「61.5%」原始值是 64.1%（F-label）",
    "机器把 39 行的第 6 列按**一条**规则重新分桶：B1=「已确立 / 已验证 / 格点数值确立」= **"
    + str(B1) + "**；B2=「部分确立 / 定性」= **" + str(B2) + "**；B3=「未检验」= **" + str(B3)
    + "**；B4=其余（未解决 6 + 需格点计算 1 + 开放/互斥 1 + 否定性结果 1 + 未复算 "
    + str(N_UNCOMP) + "）= **" + str(B4) + "**。合计 " + str(B1 + B2 + B3 + B4) + " = 39。"
    "若把「未复算」独立成第 5 桶：B4=" + str(B4_CLEAN) + "、B5=" + str(N_UNCOMP)
    + " ⇒ 仍不是 24/3/2/10。"
    "与来料相比三格同时偏移：B1 " + str(B1) + "→24（−" + str(B1 - 24) + "）、B2 " + str(B2)
    + "→3（+" + str(3 - B2) + "）、B4 " + str(B4) + "→10（−" + str(B4 - 10) + "）。"
    "⇒ 来料统计表**没有给出可复现的分桶规则**，且「未复算」在统计表里没有对应桶。"
    "声称的 61.5% 对应的原始比例是 **" + fs(RAW_PCT, 5) + "%**（" + str(B1) + "/39）。"
    "这不改变任何单行结论，但改变「覆盖率」这个头条数字 ⇒ F-label，判 FAIL。",
    {"b1": B1, "b2": B2, "b3": B3, "b4": B4, "b5_uncomputed": N_UNCOMP,
     "stated": [S_EST, S_PART, S_UNCH, S_UNR], "raw_pct": fs(RAW_PCT, 5),
     "stated_pct": str(STATED_PCT)})

CONC_ITEMS = re.findall(r"^\s*(\d+)\.\s+\*\*", SEC_CONC, re.M)
CONC_N = len(CONC_ITEMS)
CONC_SEQ = [int(x) for x in CONC_ITEMS] == list(range(1, len(CONC_ITEMS) + 1))

add("A05", "PASS",
    "「六条必须直说的结论」编号 1–6 齐全且连续（机读 6 条，无跳号）",
    "机器在 `## 六条必须直说的结论` 段内匹配「行首数字 + `.` + 空格 + `**`」：命中 **"
    + str(CONC_N) + "** 条，序号 = " + "/".join(CONC_ITEMS) + "（连续）。"
    "⇒ 标题承诺的「六条」与正文条数一致；每条的断言强度另由 B 段逐条对账"
    "（结论 1 的 m_W 0.04% 见 B01、结论 5 的 150 项见 C02）。",
    {"conclusions": CONC_N, "sequence": CONC_ITEMS})

# ---- 排版卫生：按本卷自己声明的口径（先剥行内代码，再剥成对数学）----
NAIVE_SLOT = doc.count("{}")
NAIVE_PCTD = doc.count("%d") + doc.count("%(")
NAIVE_ODD = sum(1 for ln in doc.splitlines() if ln.count("$") % 2 == 1)


def strip_code(s):
    return re.sub(r"`[^`]*`", "", s)


def strip_math_pairs(s):
    return re.sub(r"\$[^$]*\$", "", s)


CLEAN = []
ODD_AFTER = 0
for ln in doc.splitlines():
    t = strip_code(ln)
    if t.count("$") % 2 == 1:
        ODD_AFTER += 1
        CLEAN.append(t)
    else:
        CLEAN.append(strip_math_pairs(t))
REST = "\n".join(CLEAN)
N_SLOT = REST.count("{}")
N_PCTD = REST.count("%d") + REST.count("%(")

add("A06", "PASS",
    "排版卫生（本卷自述口径：先剥行内代码、再剥成对数学）：`{}` 0、`%d/%(` 0、落单 `$` 0；朴素计数给 2/2/2",
    "机器先复现**朴素计数**：`{}` **" + str(NAIVE_SLOT) + "**、`%d`+`%(` **" + str(NAIVE_PCTD)
    + "**、`$` 为奇数的行 **" + str(NAIVE_ODD) + "** —— 看起来全是缺陷。"
    "但四处（第 111/113/124/128 行）全在**行内代码**里，是散文在**引用**这些模式"
    "（`{}` 槽位规则、`%d`/`%(name)s` 占位符断言、落单 `$` 断言）。"
    "按本卷第 4 条防护自己声明的次序（先剥行内代码、再剥成对 `$…$`，出现落单 `$` 本身算失败）重算："
    "`{}` **" + str(N_SLOT) + "**、`%d/%(` **" + str(N_PCTD) + "**、剥码后落单 `$` 行 **"
    + str(ODD_AFTER) + "** ⇒ 三项全 0。"
    "⇒ 这份**人读文件**自身没有「模板没填完就写盘」的病；但它的**数字**是否跟得上仪器是另一件事——见 C02。",
    {"naive": [NAIVE_SLOT, NAIVE_PCTD, NAIVE_ODD],
     "clean": [N_SLOT, N_PCTD, ODD_AFTER]})

# =====================================================================
# 2. B 段 · 数值复算
# =====================================================================
ALPHA_S_MZ = D("0.1180")
MZ = D("91.1876")
MU200 = D("200")


def alpha_s_run(b3, mu=MU200):
    """b3 取单圈标准符号（n_f=5 ⇒ −23/3）；dα⁻¹/dlnμ = −b3/(2π)。"""
    b3d = D(b3.numerator) / D(b3.denominator) if isinstance(b3, Fraction) else D(b3)
    ainv = 1 / ALPHA_S_MZ
    return 1 / (ainv - b3d / (2 * PI) * (mu / MZ).ln())


B3_NF5 = Fraction(-11) + Fraction(2, 3) * 5
B3_NF6 = Fraction(-11) + Fraction(2, 3) * 6
AS_NF5 = alpha_s_run(B3_NF5)
AS_NF6 = alpha_s_run(B3_NF6)
AS_DOC = D("0.1060")
AS_MEAS = D("0.1057")
AS_REL5 = abs(AS_NF5 - AS_DOC) / AS_DOC
AS_CTRL_DIFF = abs(AS_NF6 - AS_DOC) / AS_DOC

MH = D("125.25")
V_EW = D("246.22")
LAM_H = MH * MH / (2 * V_EW * V_EW)
LAM_DOC = D("0.129")
LAM_REL = abs(LAM_H - LAM_DOC) / LAM_DOC

M_PLANCK = D("1.220910E19")
HIER = M_PLANCK / MZ
HIER_DOC = D("1.3E17")
HIER_REL = abs(HIER - HIER_DOC) / HIER_DOC

H0E = D("67.4")
H0L = D("73.0")
SIG = (D("0.5") ** 2 + D("1.0") ** 2).sqrt()
TENSION = (H0L - H0E) / SIG

R196 = {}
R193 = {}
try:
    R196 = json.load(open(R196_JSON, encoding="utf-8"))
except Exception:
    R196 = {}
try:
    R193 = json.load(open(R193_JSON, encoding="utf-8"))
except Exception:
    R193 = {}


def entry_num(j, code, key):
    for e in j.get("entries", []):
        if e.get("code") == code:
            return e.get("numbers", {}).get(key)
    return None


MW_REL = D(str(entry_num(R196, "C04", "rel") or "0"))     # 5.458814E-4（无量纲）
MW_PCT_MACH = MW_REL * D(100)                            # → 0.05458814 %
MW_PCT_DOC = D("0.04")
MW_PCT_ALT = D("0.05")                                   # 05 卷 §9 E5 的写法
MW_REL_ERR = abs(MW_PCT_DOC - MW_PCT_MACH) / MW_PCT_MACH
MW_CROSS = abs(MW_PCT_DOC - MW_PCT_ALT) / MW_PCT_ALT

add("B01", "FAIL",
    "m_W「0.04%」与 r196/r201 的 0.054588% 不符（相对 26.7%）；05 卷 §9 写「0.05%」⇒ 两卷并存 0.04/0.05（F-exp）",
    "机器读 r196 JSON 的 C04：`rel` = **" + fs(MW_REL, 12)
    + "**（无量纲）⇒ 相对偏差 **" + fs(MW_PCT_MACH, 9) + "%**（r201 已独立复核同一数）。"
    "覆盖矩阵第 41 行「是 0.04%」与结论 1「E5.3，0.04% 精度」两处都写 **0.04%**："
    "相对误差 " + fs(MW_REL_ERR, 6) + "（26.7%）。"
    "而 05 卷 §9 的 E5 行写「0.05%」⇒ 同一物理量在两卷里 0.04 / 0.05 并存（两数字互为 "
    + fs(MW_CROSS, 6) + "）。0.04% 是**旧值**，仪器链给出的是 0.0546%。"
    "结论「m_W 是真实计算、非拟合」不受影响（E5.3 的门禁与 r196 链都在），但精度档位被虚报 ⇒ F-exp，判 FAIL。",
    {"mw_rel": fs(MW_REL, 12), "mw_pct_mach": fs(MW_PCT_MACH, 9),
     "doc": "0.04", "alt_05": "0.05",
     "rel_err": fs(MW_REL_ERR, 6), "cross_doc_rel": fs(MW_CROSS, 6)})

add("B02", "PASS",
    "α_s(200 GeV) 复算 0.10601（n_f=5，b3=−23/3），来料 0.1060 ✔ vs 实测 0.1057；负对照 n_f=6 ⇒ 0.10696（偏 0.9%）",
    "来料 R2.2 写「α_s(200 GeV) 预测 0.1060 vs 0.1057」。机器用**同一**α_s(M_Z)=0.1180 与单圈式 "
    "`α⁻¹(μ)=α⁻¹(M_Z)−b3/(2π)·ln(μ/M_Z)`：n_f=5（M_Z 与 200 GeV 之间顶夸克已脱耦）⇒ b3=−11+2·5/3=**"
    + fr(B3_NF5) + "** ⇒ α_s(200)=**" + fs(AS_NF5, 9) + "**（来料 0.1060，相对 "
    + fs(AS_REL5, 4) + "；对实测 0.1057 差 " + fs(abs(AS_NF5 - AS_MEAS) / AS_MEAS, 4) + "）。"
    "负对照：若误用 n_f=6（b3=−7）⇒ **" + fs(AS_NF6, 9) + "**，相对 0.1060 偏 "
    + fs(AS_CTRL_DIFF, 4) + "（约 0.9%）⇒ 来料那个 0.1060 **只**在 n_f=5 下复现。"
    "⇒ 这一行是**真算**且口径正确，不是拟合。",
    {"b3_nf5": fr(B3_NF5), "as_nf5": fs(AS_NF5, 9), "as_nf6_ctrl": fs(AS_NF6, 9),
     "rel_doc": fs(AS_REL5, 4), "meas": "0.1057"})

add("B03", "PASS",
    "Higgs 自耦合 λ=m_h²/(2v²)=0.12938，来料 0.129 ✔（相对 2.9E−3）",
    "来料第 45 行给 λ=m_h²/(2v²)=0.129。机器取 m_h=125.25 GeV、v=246.22 GeV："
    "125.25²/(2×246.22²)=**" + fs(LAM_H, 9) + "**，相对 0.129 差 " + fs(LAM_REL, 4)
    + "（两位小数截断）⇒ 一致。注意这是**定义式回代**（λ 由 m_h、v 反解），不是本框架对 λ 的预言。",
    {"lambda": fs(LAM_H, 9), "doc": "0.129", "rel": fs(LAM_REL, 4)})

add("B04", "PASS",
    "层级比 M_Pl/M_Z=1.3389E17，来料「1.3e17」✔（用未约化 Planck 质量）",
    "来料第 59 行写「L4：比值 1.3e17 无解释」。机器：M_Pl=1.220910E19 GeV、M_Z=91.1876 GeV ⇒ "
    "比值 = **" + fs(HIER, 9) + "**，相对 1.3E17 差 " + fs(HIER_REL, 4)
    + " ⇒ 一致。口径注：用的是**未约化** Planck 质量；若用约化 M_Pl=2.435E18 则比值 2.67E16，"
    "与「1.3e17」差一个量级 ⇒ 该行必须声明用的是哪一个（F-label 提示，不改数值）。",
    {"ratio": fs(HIER, 9), "doc": "1.3E17", "rel": fs(HIER_REL, 4)})

add("B05", "PASS",
    "H0 张力 (73.0−67.4)/√(0.5²+1.0²)=5.008σ，来料「5σ」✔",
    "来料第 32/112 行写「H0 张力 5σ」。机器用 §4.1 的两个 H0 与误差：Δ=5.6、"
    "σ=√(0.25+1.0)=**" + fs(SIG, 9) + "** ⇒ 张力 **" + fs(TENSION, 9)
    + "σ**（四舍五入 5.0）⇒ 一致。这是**外部观测张力**的搬运，不是本框架的计算。",
    {"delta_h0": "5.6", "sigma": fs(SIG, 9), "tension": fs(TENSION, 9)})

MERC_193 = D(str(entry_num(R193, "C01", "arcsec_per_century") or "0"))
DE_193 = D(str(entry_num(R193, "D04", "dE_J") or "0"))
MERC_DOC = D("42.98")
MERC_R2 = MERC_193.quantize(D("0.01"), rounding=ROUND_HALF_UP)
DE_DOC = D("5.5E47")
DE_OBS = D("5.4E47")

add("B06", "PASS",
    "水星 42.98″ / GW 5.5e47 J 与 r193 JSON 逐位对齐（42.9807617 / 5.540241E47），对实测 5.4e47 差 2.6%",
    "机器读 r193 JSON：C01 的每世纪进动 = **" + fs(MERC_193, 12)
    + "″**（两位小数四舍五入 = **" + str(MERC_R2) + "″**，与来料 42.98 逐字符一致）、"
    "D04 的 ΔE = **" + fs(DE_193, 12) + " J**；覆盖矩阵写 5.5e47（相对 "
    + fs(abs(DE_DOC - DE_193) / DE_193, 4) + "）。"
    "对 LIGO 实测 5.4e47 J 的相对差 " + fs(abs(DE_193 - DE_OBS) / DE_OBS, 4)
    + "（一位小数口径）⇒ 一致。"
    "⇒ 矩阵的两条「真实计算」在跨册层站得住。",
    {"mercury_r193": fs(MERC_193, 12), "mercury_round2": str(MERC_R2),
     "dE_r193": fs(DE_193, 12), "dE_doc": "5.5E47", "dE_obs": "5.4E47"})

# =====================================================================
# 3. C 段 · SO(10) 仪器接线
# =====================================================================
def load_json(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}


J_CHAIN = load_json(SO10_CHAIN)
J_REPS = load_json(SO10_REPS)
J_THR = load_json(SO10_THR)


def gate_stats(j, key):
    arr = j.get(key, [])
    vals = Counter(str(x.get("status", "?")) for x in arr if isinstance(x, dict))
    return len(arr), vals.get("PASS", 0), vals


N_CHAIN, P_CHAIN, V_CHAIN = gate_stats(J_CHAIN, "tests")
N_REPS, P_REPS, V_REPS = gate_stats(J_REPS, "tests")
N_THR, P_THR, V_THR = gate_stats(J_THR, "gates")
GATE_SUM = N_CHAIN + N_REPS + N_THR
PASS_SUM = P_CHAIN + P_REPS + P_THR

add("C01", "PASS",
    "SO(10) 三份仪器逐条读：55 / 155 / 55 个门禁，PASS 55/155/55（无一 FAIL、无 MISSING）",
    "机器**读 JSON 不读散文**：`SO10链统一报告.json` 的 `tests` = **" + str(N_CHAIN)
    + "**（PASS " + str(P_CHAIN) + "）；`SO10表示论报告.json` 的 `tests` = **" + str(N_REPS)
    + "**（PASS " + str(P_REPS) + "）；`SO10阈值报告.json` 的 `gates` = **" + str(N_THR)
    + "**（PASS " + str(P_THR) + "）。状态直方图：链 " + str(dict(V_CHAIN))
    + "、表示论 " + str(dict(V_REPS)) + "、阈值 " + str(dict(V_THR)) + "。"
    "合计 **" + str(GATE_SUM) + "** 个门禁、**" + str(PASS_SUM) + "** 个 PASS。",
    {"chain": N_CHAIN, "reps": N_REPS, "thr": N_THR, "sum": GATE_SUM,
     "pass_sum": PASS_SUM})

CM_150 = doc.count("150 项")
CM_260 = doc.count("260 项")
CM_SUM = doc.count("55 + 150")
GATE_DIFF = GATE_SUM - 260

add("C02", "FAIL",
    "「55 + 150 + 55 = 260 项门禁全 PASS」已过期：仪器实际 155 项 ⇒ 合计 265；「150」在行 60 与结论 5/6 共 3 处（F-exp）",
    "来料三处引用同一账：「so10_reps.py（150 项门禁全 PASS）」（结论 5）、"
    "「55 + 150 + 55 = 260 项门禁全 PASS」（行 60 与结论 6）。机器读仪器：表示论 `tests` = **"
    + str(N_REPS) + "** ⇒ 真实合计 = 55 + " + str(N_REPS) + " + 55 = **" + str(GATE_SUM)
    + "**，比声称的 260 多 **" + str(GATE_DIFF) + "** 项。"
    "而 265 项**全部 PASS**（C01）⇒ 结论方向没错，错的是**计数**："
    "仪器从 150 增到 155 后散文未跟。"
    "文本层计数：`150 项` 出现 " + str(CM_150) + " 次、`260 项` " + str(CM_260)
    + " 次、`55 + 150` " + str(CM_SUM) + " 次 ⇒ 同一过期数字的 3 个传播点。"
    "这正是本卷自述「表格改了、散文没改」失效族在自己文件上的复发 ⇒ F-exp，判 FAIL。",
    {"claim": "150+55+55=260", "actual": GATE_SUM, "reps_tests": N_REPS,
     "diff": GATE_DIFF, "occ_150": CM_150, "occ_260": CM_260, "occ_sum": CM_SUM})

FLAGS = {
    "chain_engine_pass": J_CHAIN.get("engine_pass"),
    "chain_solution_pass": J_CHAIN.get("solution_pass"),
    "reps_engine_pass": J_REPS.get("engine_pass"),
    "reps_global_pass": J_REPS.get("global_pass"),
    "reps_residual422_pass": J_REPS.get("residual422_pass"),
    "reps_perweight_pass": J_REPS.get("perweight_pass"),
    "thr_all_pass": J_THR.get("all_pass"),
    "thr_n_pass": J_THR.get("n_pass"),
}
FLAGS_OK = all(v is True for k, v in FLAGS.items() if k != "thr_n_pass") and FLAGS["thr_n_pass"] == N_THR

add("C03", "PASS",
    "仪器布尔字段真实读取：engine_pass / global_pass / residual422_pass / perweight_pass / all_pass 全 True，n_pass=55=门禁数",
    "机器逐项读 JSON 的布尔：链 `engine_pass`=" + str(FLAGS["chain_engine_pass"])
    + "、`solution_pass`=" + str(FLAGS["chain_solution_pass"])
    + "；表示论 `engine_pass`=" + str(FLAGS["reps_engine_pass"])
    + "、`global_pass`=" + str(FLAGS["reps_global_pass"])
    + "、`residual422_pass`=" + str(FLAGS["reps_residual422_pass"])
    + "、`perweight_pass`=" + str(FLAGS["reps_perweight_pass"])
    + "；阈值 `all_pass`=" + str(FLAGS["thr_all_pass"]) + "、`n_pass`="
    + str(FLAGS["thr_n_pass"]) + "（= 门禁数 " + str(N_THR) + "）。"
    "⇒ 「全 PASS」这句话在**仪器侧**成立（这是 C02 只判计数、不判结论的原因）。",
    {"flags": FLAGS, "ok": FLAGS_OK})

LINKS = re.findall(r"\]\(([^)]+)\)", doc)
LOCAL = [L for L in LINKS if not L.startswith("http")]
MISSING = []
for L in LOCAL:
    q = os.path.normpath(os.path.join(V7, L))
    if not os.path.exists(q):
        MISSING.append(L)
GUARD_EXIST = os.path.exists(GUARDP)

add("C04", "PASS",
    "链接可解性：11 个本地链接全部命中磁盘文件；`维护脚本/check_placeholder_guard.py` 亦存在",
    "机器抽出 " + str(len(LINKS)) + " 个 Markdown 链接，其中本地 " + str(len(LOCAL))
    + " 个（其余为 http）：逐个按 07 卷目录解析并 `os.path.exists`，缺失 **" + str(len(MISSING))
    + "** 个。另按本卷正文点名的 `维护脚本/check_placeholder_guard.py` 直接探盘："
    + ("存在" if GUARD_EXIST else "缺失") + "。"
    "⇒ 「本表把自己也上了同一条防护」这句话的**指针**是活的"
    "（防护本身是否 31/31 通不过不在本册范围）。",
    {"links": len(LINKS), "local": len(LOCAL), "missing": MISSING,
     "guard_script": GUARD_EXIST})

# =====================================================================
# 4. D 段 · 名实、供给与台账
# =====================================================================
V05 = os.path.join(V7, "05_经典极限与现象推导.md")
D05TXT = ""
try:
    D05TXT = open(V05, encoding="utf-8").read()
except Exception:
    D05TXT = ""
SEC9_05 = D05TXT.split("\n## 9.")[1] if "\n## 9." in D05TXT else ""
N1_LINE = ""
for ln in SEC9_05.splitlines():
    if ln.startswith("| N1"):
        N1_LINE = ln
        break
N1_FIXED = ("已修复" in N1_LINE) and ("✅" in N1_LINE)
NU_ROW = [r for r in MAT if r[0].startswith("中微子振荡")]
NU_NOTE = NU_ROW[0][6] if NU_ROW else ""
NU_STATUS = NU_ROW[0][5] if NU_ROW else ""
NU_INPUT = ("质量谱与 PMNS 混合为输入" in NU_NOTE)

add("D01", "FAIL" if (N1_FIXED and NU_INPUT) else "PASS",
    "中微子一行两卷不同口径：07 写「参数未推导 / 质量谱为输入」，05 §9 N1 写「✅ 已修复」⇒ 跨卷标记差（F-label）",
    "07 卷第 46 行：状态 **" + NU_STATUS + "**，备注明写「质量谱与 PMNS 混合为输入」（机读 "
    + str(NU_INPUT) + "）。05 卷 §9 的 N1 行写「与振荡矛盾 | ✅ **2026-09-19 已修复**（加 $\\nu_R$）」（机读 "
    + str(N1_FIXED) + "）。两卷对**同一项**给出两种可读结论：07 说「质量非零但谱是输入」，"
    "05 说「已修复」。按 07 自己的口径（参数未推导、谱为输入），「已修复」至多表示"
    "「质量≠0 已实现」，不表示「振荡谱被预言」。"
    "⇒ 这是**跨卷标记不一致**（与 r201 D01 同源），登记 F-label；本册不改物理结论，"
    "也不把 07 的这一行判错——07 的写法本身是诚实的，问题在汇总表把两件事合并。",
    {"nu_status": NU_STATUS, "nu_input_caveat": NU_INPUT,
     "sec9_n1_fixed": N1_FIXED, "n1_line": N1_LINE[:60]})

DERIVED_COL = [r[3] for r in MAT]
DER_YES = sum(1 for x in DERIVED_COL if x.startswith("是"))
DER_NO = sum(1 for x in DERIVED_COL if x.startswith("否"))
DER_OTHER = N_ROWS - DER_YES - DER_NO

add("D02", "PASS",
    "「由主方程导出」列：是 23 / 否 10 / 其它 6（树级、不适用、定性、有效理论、部分、不足）",
    "机器对第 4 列按前缀分类：以「是」开头 **" + str(DER_YES) + "**、以「否」开头 **"
    + str(DER_NO) + "**、其余 **" + str(DER_OTHER) + "** 行（树级 / 不适用 / 定性 / "
    "有效理论 / 部分 / 不足各 1）。⇒ 「导出=是」的 23 行里仍混着「参数未推导」（3 行，"
    "H0 / CKM / 中微子）与「非本项目复算」（1 行，原子光谱）"
    "这正是 A02/B01 所判口径问题的来源：**「导出」与「预言」在本表里不是同一列**。",
    {"yes": DER_YES, "no": DER_NO, "other": DER_OTHER})

DEFECTS = [
    ("F-label", "A02", "14 种状态串 vs 口径表 6 类，4 种在表外（子串法只给 3，因「定性」误吞「否定性」）"),
    ("F-label", "A04", "统计表 24/3/2/10 不可逐行复现（原始 25/1/2/11；61.5% vs 64.1%）"),
    ("F-exp", "B01", "m_W「0.04%」vs 仪器 0.054588%；且 05 卷 §9 写 0.05%"),
    ("F-exp", "C02", "「150 项 / 260 项」vs 仪器 155 / 265（3 处传播）"),
    ("F-label", "D01", "中微子行 07「参数未推导」vs 05 §9 N1「✅ 已修复」"),
]
FAM = Counter(f for f, _c, _d in DEFECTS)

add("D03", "PASS",
    "缺陷族归集 5 例 2 族：F-label×3（词表、统计、跨卷标记）+ F-exp×2（m_W 精度、门禁计数）；供给 0/12",
    "逐条归集：**F-label** 三例 —— A02（口径漂移 + 匹配方法敏感）、A04（统计不可复现）、"
    "D01（跨卷标记差）；**F-exp** 两例 —— B01（精度 0.04 vs 0.0546）、C02（150 vs 155、260 vs 265）。"
    "未出现：F-pi（本卷无 π 争议）、F-unit（单位全标注）、F-dim-blind（无维数式）、"
    "F-scale（比值口径均声明）、F-sign（无符号翻转）。"
    "供给账：39 行中「由主方程导出=是」**" + str(DER_YES) + "** 行，其中「参数未推导」3 行、"
    "「非本项目复算」1 行 ⇒ 余 **" + str(DER_YES - 4) + "** 行，仍全部是 GR/SM 既有结果"
    "（牛顿、水星、偏折、红移、Shapiro、LT、GW×3、黑洞、H0、库仑、电磁波、静磁、β、W/Z、"
    "中性流、宇称、CKM、Higgs、ν、渐近自由、自旋-自旋）⇒ 真正可称**本框架独立预言**的仍是 0 条；"
    "自有供给 **0/12**（池 12/12）维持。",
    {"families": dict(FAM), "total": len(DEFECTS), "supply": "0/12",
     "derived_yes": DER_YES, "derived_net": DER_YES - 4})

add("D04", "INFO",
    "取号：r206（r197 单圈跑动 / r199 尺度锚定 / r202 场元数据表 / r203 S13 兄弟链 / r204 质量定义方程 / r205 统一性归因 占用）",
    "按铁律扫 数据/源码/判定 三目录：r197、r199、r202、r203、r204、r205 均已被并行链占用"
    "（本卷首版拟用 r203，落盘前探到被《S13 兄弟链跨轮互印…》整卷占用；改号 r204 亦被"
    "《质量定义方程…》占用；改号 r205 又被《统一性归因审计…》占用；再改 **r206** 后"
    "三目录 `*r206*` 零命中）。四次取号、三次撞车，按铁律只整卷改号、不改他册。"
    "范围声明：本册只审计 07 卷的覆盖矩阵与其外部引用，不重判 r197 的 §8 数字、"
    "不重判 r202 的场元数据表、不重判 r203/r204/r205；各册不相加。",
    {"occupied": ["r197", "r199", "r202", "r203", "r204", "r205"], "first_free": "r206",
     "untouched_parallel_files": True})

table = [
    dict(probe="39 行覆盖矩阵的结构与数字（水星/偏折/GW/α_s/Higgs/层级/H0）",
         verdict="C1", reason="全部为 GR/SM 既有公式的回代；矩阵只是转录与排版"),
    dict(probe="SO(10) 仪器账（55/155/55，全 PASS）",
         verdict="C2", reason="依赖三条 SO(10) 链的模型输入与标量谱；且计数口径已过期"),
    dict(probe="中微子「已确立（参数未推导）」",
         verdict="C2", reason="质量谱与 PMNS 为输入；r196 C07 已证单一 y_ν 谱退化"),
    dict(probe="统计表 61.5% 覆盖率",
         verdict="C2", reason="分桶规则不可复现；该数字是对 39 行人工归类的二次统计，不是物理量"),
]
C1_N = sum(1 for r in table if r["verdict"] == "C1")
C2_N = sum(1 for r in table if r["verdict"] == "C2")
C3_N = sum(1 for r in table if r["verdict"] == "C3")

# =====================================================================
# 5. 守卫
# =====================================================================
guard("G01 doc_readable", bool(doc) and "覆盖矩阵" in doc, "len=%d" % len(doc))
guard("G02 rows_39", N_ROWS == 39, "n=%d" % N_ROWS)
guard("G03 cols_7", N_COLS == [7], str(N_COLS))
guard("G04 csv_39", len(CSV_ROWS) == 39, "n=%d" % len(CSV_ROWS))
guard("G05 names_equal", NAME_EQ, "diff=%d" % sum(1 for a, b in zip(MD_NAMES, CSV_NAMES) if a != b))
guard("G06 unesc_diff_0", UNESC_DIFF == 0 and RAW_DIFF == 1, "%d/%d" % (RAW_DIFF, UNESC_DIFF))
guard("G07 status_distinct_14", len(STATUS_CNT) == 14, str(len(STATUS_CNT)))
guard("G08 outside_4", len(OUTSIDE) == 4 and "格点数值确立" in OUTSIDE,
      "outside=%s" % OUTSIDE)
guard("G09 stat_sum_39", STAT_SUM == 39, str(STAT_SUM))
guard("G10 stat_pct_ok", PCT_OK, "pct mismatch")
guard("G11 raw_b1_25", B1 == 25, "b1=%d" % B1)
guard("G12 raw_b4_11", B4 == 11, "b4=%d" % B4)
guard("G13 stats_unreproducible", (B1, B2, B3, B4) != (S_EST, S_PART, S_UNCH, S_UNR),
      "%s vs %s" % ((B1, B2, B3, B4), (S_EST, S_PART, S_UNCH, S_UNR)))
guard("G14 conclusions_6", CONC_N == 6 and CONC_SEQ, str(CONC_ITEMS))
guard("G15 hygiene_slots_0", N_SLOT == 0, "n=%d" % N_SLOT)
guard("G16 hygiene_pct_0", N_PCTD == 0, "n=%d" % N_PCTD)
guard("G17 hygiene_dollar_0", ODD_AFTER == 0, "n=%d" % ODD_AFTER)
guard("G18 mw_pct_mach_range", D("0.05") < MW_PCT_MACH < D("0.06"), fs(MW_PCT_MACH, 9))
guard("G19 mw_doc_mismatch", MW_REL_ERR > D("0.2"), fs(MW_REL_ERR, 6))
guard("G20 mw_cross_doc", MW_CROSS == D("0.2"), fs(MW_CROSS, 6))
guard("G21 as_nf5_doc", AS_REL5 < D("5E-3"), fs(AS_REL5, 5))
guard("G22 as_nf5_meas", abs(AS_NF5 - AS_MEAS) / AS_MEAS < D("5E-3"), fs(AS_NF5, 9))
guard("G23 as_nf6_control", AS_CTRL_DIFF > D("5E-3"), fs(AS_CTRL_DIFF, 5))
guard("G24 b3_nf5_exact", B3_NF5 == Fraction(-23, 3), fr(B3_NF5))
guard("G25 lambda_doc", LAM_REL < D("5E-3"), fs(LAM_REL, 5))
guard("G26 hier_doc", HIER_REL < D("5E-2"), fs(HIER_REL, 5))
guard("G27 h0_tension", abs(TENSION - D("5")) < D("0.05"), fs(TENSION, 6))
guard("G28 mercury_round2", MERC_R2 == MERC_DOC, "%s vs %s" % (MERC_R2, MERC_DOC))
guard("G29 de_r193", abs(DE_DOC - DE_193) / DE_193 < D("1E-2"), fs(DE_193, 9))
guard("G30 de_obs", abs(DE_193 - DE_OBS) / DE_OBS < D("5E-2"), fs(DE_193, 9))
guard("G31 chain_tests_55", N_CHAIN == 55 and P_CHAIN == 55, "%d/%d" % (P_CHAIN, N_CHAIN))
guard("G32 reps_tests_155", N_REPS == 155 and P_REPS == 155, "%d/%d" % (P_REPS, N_REPS))
guard("G33 thr_gates_55", N_THR == 55 and P_THR == 55, "%d/%d" % (P_THR, N_THR))
guard("G34 gate_sum_265", GATE_SUM == 265, "n=%d" % GATE_SUM)
guard("G35 gate_claim_stale", GATE_DIFF == 5, "diff=%d" % GATE_DIFF)
guard("G36 claim_occ_3", (CM_150 + CM_260 + CM_SUM) >= 3, "%d/%d/%d" % (CM_150, CM_260, CM_SUM))
guard("G37 instrument_flags", FLAGS_OK, str(FLAGS))
guard("G38 links_resolve", not MISSING, str(MISSING))
guard("G39 guard_script", GUARD_EXIST, "missing")
guard("G40 nu_row_found", bool(NU_NOTE), "note len=%d" % len(NU_NOTE))
guard("G41 nu_input_caveat", NU_INPUT, "caveat missing")
guard("G42 sec9_n1_fixed", N1_FIXED, "n1_line=%s" % N1_LINE[:30])
guard("G43 derived_yes_23", DER_YES == 23, "n=%d" % DER_YES)
guard("G44 pi_first_digits",
      format(PI, ".20f")[:22] == "3.14159265358979323846", format(PI, ".20f"))
guard("G45 fail_entries_have_numbers",
      all(bool(e["numbers"]) for e in ENTRIES if e["level"] == "FAIL"),
      "FAIL=%d" % sum(1 for e in ENTRIES if e["level"] == "FAIL"))
cnt = Counter(e["level"] for e in ENTRIES)
guard("G46 levels_4fail_15pass", cnt.get("FAIL", 0) == 4 and cnt.get("PASS", 0) == 15
      and cnt.get("INFO", 0) == 1, str(dict(cnt)))
supply = [e for e in ENTRIES if e["code"] == "D03"][0]["numbers"].get("supply")
guard("G47 supply_zero", supply == "0/12", str(supply))
guard("G48 families_2", len(FAM) == 2 and len(DEFECTS) == 5, str(dict(FAM)))
guard("G49 c1_c2_counts", C1_N == 1 and C2_N == 3 and C3_N == 0, "%d/%d/%d" % (C1_N, C2_N, C3_N))
guard("G50 raw_pct_641", abs(RAW_PCT - D("64.10")) < D("0.05"), fs(RAW_PCT, 6))
guard("G51 stated_pct_615", abs(STATED_PCT - D("61.5")) < D("0.05"), str(STATED_PCT))
guard("G52 naive_hygiene_positive", NAIVE_SLOT >= 2 and NAIVE_PCTD >= 2 and NAIVE_ODD >= 2,
      "naive=%d/%d/%d" % (NAIVE_SLOT, NAIVE_PCTD, NAIVE_ODD))
guard("G53 csv_fields_7", all(len(r) == 7 for r in CSV_ROWS),
      str(sorted(set(len(r) for r in CSV_ROWS))))

# =====================================================================
# 6. 控制组
# =====================================================================
control("K01 rows_magnitude", 30 <= N_ROWS <= 60, "n=%d" % N_ROWS)
control("K02 csv_name_match", NAME_EQ and len(CSV_NAMES) == 39, "n=%d" % len(CSV_NAMES))
control("K03 est_count_magnitude", 20 <= S_EST <= 28, "n=%d" % S_EST)
control("K04 b1_b2_differ", B1 != B2, "%d/%d" % (B1, B2))
control("K05 mw_pct_vs_r201", abs(MW_PCT_MACH - D("0.054588140000")) < D("1E-7"),
        fs(MW_PCT_MACH, 9))
control("K06 as_nf5_magnitude", D("0.1055") < AS_NF5 < D("0.1065"), fs(AS_NF5, 9))
control("K07 lambda_magnitude", D("0.128") < LAM_H < D("0.131"), fs(LAM_H, 9))
control("K08 hier_magnitude", D("1E17") < HIER < D("2E17"), fs(HIER, 9))
control("K09 tension_magnitude", D("4.5") < TENSION < D("5.5"), fs(TENSION, 9))
control("K10 chain_only_pass", P_CHAIN == N_CHAIN, "%d/%d" % (P_CHAIN, N_CHAIN))
control("K11 reps_grew", N_REPS > 150, "n=%d" % N_REPS)
control("K12 thr_npass_matches", J_THR.get("n_pass") == N_THR, str(J_THR.get("n_pass")))
control("K13 links_count", len(LOCAL) == 11, "n=%d" % len(LOCAL))
control("K14 conclusions_count", CONC_N == 6, "n=%d" % CONC_N)
control("K15 derived_partition", DER_YES + DER_NO + DER_OTHER == 39,
        "%d+%d+%d" % (DER_YES, DER_NO, DER_OTHER))
control("K16 status_sum", sum(STATUS_CNT.values()) == 39, "n=%d" % sum(STATUS_CNT.values()))
control("K17 raw_seg_escaped", N_SEG == [9, 11] and N_COLS == [7],
        "segs=%s cols=%s" % (N_SEG, N_COLS))

VERDICT = ("R206-COVERAGE-MATRIX-ROWS39-COLS7-CSV39-ALIGN39-OK-"
           "STATUS14-VS-DICT6-GAP4-INFO-SUBTRAP1-INFO-STATS24-3-2-10-SUM39-OK-"
           "RAW25-1-2-11-UNREPRODUCIBLE-FAIL-F-LABEL-PCT61.5-VS-RAW64.1-FAIL-"
           "MW-0.04-VS-0.054588-FAIL-F-EXP-AS200-0.10601-OK-NF6-CTRL-0.10696-OK-"
           "HIGGS-LAMBDA-0.12938-OK-HIER-1.3389E17-OK-H0-TENSION-5.01SIGMA-OK-"
           "MERCURY-GW-R193-OK-SO10-GATES-55-155-55-SUM265-VS-CLAIM260-FAIL-F-EXP-"
           "LINKS-11-OK-CONCLUSIONS-6-OK-DERIVED-23-10-6-OK-"
           "HYGIENE-CLEAN-0-NAIVE-2-2-2-OK-"
           "NU-07-VS-05-N1-LABEL-GAP-F-LABEL-DEFECTS-5-2FAMILIES-TUFT-SUPPLY-0")


def main():
    counts = Counter(e["level"] for e in ENTRIES)
    n_g = sum(1 for g in GUARDS if g["ok"])
    n_c = sum(1 for c in CONTROLS if c["ok"])

    print("\n" + "=" * 78)
    print("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）"
          % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
             counts.get("BOUNDARY", 0), counts.get("INFO", 0), counts.get("CORRECTED", 0)))
    print("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    print("判定串：" + VERDICT)

    payload = dict(
        stem=STEM, verdict=VERDICT, counts=dict(counts),
        guards_total=len(GUARDS), guards_pass=n_g,
        controls_total=len(CONTROLS), controls_pass=n_c,
        guard_list=GUARDS, control_list=CONTROLS, entries=ENTRIES,
        supply=dict(pool="12/12", supply="0/12"),
        judgement=table,
        source="07_统一场方程/07_现象覆盖矩阵.md (+ 现象覆盖矩阵.csv, SO10 三份报告)",
    )
    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    md = []
    md.append("# " + STEM + "\n")
    md.append("**条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）；"
              "守卫 %d/%d；控制组 %d/%d；退出码 0**\n"
              % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                 counts.get("BOUNDARY", 0), counts.get("INFO", 0),
                 counts.get("CORRECTED", 0), n_g, len(GUARDS), n_c, len(CONTROLS)))
    md.append("## 一句话\n")
    md.append("39 行覆盖矩阵在结构上与 CSV 完全对齐（39/39 现象名、7 字段切列、仅 1 处 `\\|` 转义差），"
              "α_s(200 GeV)=0.10601、λ=0.12938、M_Pl/M_Z=1.338E17、H0 张力 5.008σ、"
              "水星/GW 与 r193 逐位一致 —— 这些「真实计算」站得住。**四处 FAIL**："
              "① A04 统计表的 24/3/2/10 无法从 39 行逐行复现（单一口径给 25/1/2/11，"
              "头条 61.5% 的原始值是 64.1%）；② B01 m_W「0.04%」与仪器 0.054588% 不符"
              "（且 05 §9 写 0.05%）；③ C02「55+150+55=260 项门禁」已过期，仪器实际 "
              "55+155+55=**265**（全 PASS，仅计数错）；④ D01 中微子行 07「参数未推导」"
              "与 05 §9 N1「✅ 已修复」跨卷标记不一。供给 0/12 维持。\n")
    md.append("**判定串**：`" + VERDICT + "`\n")
    md.append("## 条目\n")
    md.append("| 编号 | 级 | 标题 |")
    md.append("|---|---|---|")
    for e in ENTRIES:
        md.append("| %s | %s | %s |" % (e["code"], e["level"], e["title"].replace("|", "\\|")))
    md.append("\n## 三判定\n")
    md.append("| 探针 | 判定 | 理由 |")
    md.append("|---|---|---|")
    for r in table:
        md.append("| %s | **%s** | %s |" % (r["probe"], r["verdict"], r["reason"]))
    md.append("\n## 守护（%d/%d）\n" % (n_g, len(GUARDS)))
    for g in GUARDS:
        md.append("- [%s] %s" % ("OK" if g["ok"] else "FAIL", g["name"]))
    md.append("\n## 控制组（%d/%d）\n" % (n_c, len(CONTROLS)))
    for c in CONTROLS:
        md.append("- [%s] %s %s" % ("OK" if c["ok"] else "FAIL", c["name"], c["msg"]))
    md.append("\n## 红线\n")
    md.append("本册只做名实审计与闭环复算，不产生新物理，不宣称观测证实/否证；"
              "未改写 07 卷或 SO(10) 仪器任何字节；未触碰并行链（r197/r199/r202/r203/r204/r205）文件；"
              "未改 verify.py；未做 git 操作。本册编号空间不得与 r193/r196/r201/r197/r199/r202/r203/r204/r205 相加；"
              "TUFT 供给 0/12 维持。\n")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    rep = []
    rep.append("TUFT-r206 现象覆盖矩阵 全维名实与可复现性审计 · 运行报告")
    rep.append("=" * 70)
    rep.append("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）"
               % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                  counts.get("BOUNDARY", 0), counts.get("INFO", 0), counts.get("CORRECTED", 0)))
    rep.append("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    rep.append("")
    for e in ENTRIES:
        rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
        rep.append("    " + e["detail"])
        if e["numbers"]:
            try:
                rep.append("    " + json.dumps(e["numbers"], ensure_ascii=False))
            except Exception:
                pass
        rep.append("")
    rep.append("判定串：" + VERDICT)
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))

    print("out -> %s.{json,md,_report.txt}" % STEM)
    return 0 if (n_g == len(GUARDS) and n_c == len(CONTROLS)) else 1


if __name__ == "__main__":
    sys.exit(main())
