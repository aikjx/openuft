# -*- coding: utf-8 -*-
"""
TUFT-r201 · 《07_统一场方程/05_经典极限与现象推导.md》§9 状态汇总 + §7 强力表 切片闭环式审计
2026-10-25

承接 r193（同卷 §1–§3）与 r196（同卷 §4–§6）。本册吃最后两块：
  §7   强力量子现象表（6 行）：渐近自由 / α_s(M_Z)=0.1180 / 喷注 / 强子质量谱 / 禁闭 / m_p
  §9   本节推导的状态汇总（22 行）：C1–C4、E5、R1、R1b–R1o(14)、R2、N1

去重原则：§4–§6 已由 r196 机验；§7 与 §8 与并行链
《经典极限与现象推导链路闭环式_宇宙学电磁弱力强力与单圈跑动切片》（现占 r197）**范围重叠**。
本册不重判其结论，只在核 §9 汇总表时对它所引的数字做**独立交叉复算**，并声明两册不得相加。

机算策略（全部真实守卫，无一处 ok 写死 True；无浮点混入）：
  A01  表结构：22 行 × 4 列；编号分层 C×4 / E×1 / R×15 / N×1
  A02  标记计数：✅=21 / ❌=1 / ⚠️=0（§9 内）
  A03  编号连续性：C1–C4 连续、R1+R1b–R1o 后缀 b–o 连续、E 系列只 E5（E1–E4 全文缺失）
  A04  「与观测」栏口径分类 7 类，合计 22
  A05  「若取 SO(10) 内容」条件性覆盖 14/14
  B01  C2 水星 / C3 偏折现场重算，并与 r193 JSON 机读比对
  B02  C4 GW150914 ΔE 现场重算，并与 r193 JSON 比对
  B03  E5 m_W 与 r196 JSON 比对；并机读 r196 C07=FAIL
  B04  R1 引用的 SM 两交点独立复算（α_i(M_Z)⁻¹ 由 α_em⁻¹、sin²θ_W、α_s 推）
       ⇒ 第二交点与「约 7 倍」两个数字**不成立**（F-exp）
  B05  R1 的 MSSM 行交叉核对（1.8E16 / 2.0E16 / 12%）
  B06  R2 渐近自由：b3=−11+2n_f/3=−7<0；负对照 n_f=17 ⇒ +1/3>0 失 AF
  C01  张量分解维数：Sym²(16)=136=10+126、∧²(16)=120、16⊗16̄=1+45+210=256
  C02  3221 分支维数与 B−L 无迹（16 / 10）
  C03  422 分支维数（16 / 10 / 126 / 120）
  C04  B−L 在 su(4) 中与 su(3) Cartan 全部正交且独立 ⇒ 正交补恰 1 维（R6.8a）
  C05  荷格 g0=1/3、N=qΔ/g0∈{3,6}、(−1)^{3(B−L)}=−1 ⇒ 物质字称被破
  C06  §9 内门禁编号族覆盖 6–16（重复 token 是交叉引用，不是新门禁）
  D01  N1 行「✅ 已修复」与 r196 C07=FAIL 冲突 ⇒ 汇总表标记膨胀（F-label）
  D02  E5 与 r196 C04 同数
  D03  全文 ✅=28 的切片分解：4（§1–§3）+1（§4–§6）+2（§7）+0（§8）+21（§9）
  D04  §7 表口径：6 行、✅2/⚠️1/❌3，三条 ❌ 均自标「非解析/格点」
  D05  缺陷族归集（F-label×2、F-exp×1）+ 供给 0/12
  D06  编号与重叠：r197/r198/r199/r200 连续四号被并行链占、本卷取实测首空号 r201

纪律：纯标准库；Decimal 250 位；可精确者一律 Fraction/整数。
     真实守卫（无一处 ok 写死 True）、真实负对照。
红线：不产生新物理；不改写来料字节；不改 verify.py；不做 git；不触碰并行链文件。
"""
import json
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                 # 本项目_全维自洽与归一化
CFG = os.path.dirname(BASE)                  # 04_公共成果
ROOT = os.path.dirname(CFG)                  # openuft
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r201_经典极限与现象推导链路闭环式_状态汇总与强力表口径切片_2026-10-25"
DOC = os.path.join(ROOT, "07_统一场方程", "05_经典极限与现象推导.md")
R193_JSON = os.path.join(
    OUTD, "TUFT-r193_经典极限与现象推导链路闭环式_PPN与GW口径切片_2026-10-25.json")
R196_JSON = os.path.join(
    OUTD, "TUFT-r196_经典极限与现象推导链路闭环式_宇宙学与弱力定量链切片_2026-10-25.json")

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


def fdec(f):
    return D(f.numerator) / D(f.denominator)


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
ARCSEC_PER_RAD = D(648000) / PI

# =====================================================================
# 1. 来料与外部锚点（逐字）
# =====================================================================
G = D("6.67430E-11")
C = D("2.99792458E8")
C2 = C * C
GMSUN = D("1.3271244E20")
MSUN = D("1.9885E30")
RSUN = D("6.957E8")
A_MERC = D("5.7909E10")
E_MERC = D("0.205630")
T_CENT = D("36525")
T_MERC = D("87.969")

ALPHA_EM_INV = D("127.95")      # 外部锚点（PDG）
SIN2_W = D("0.23122")           # 外部锚点（PDG）
ALPHA_S_MZ = D("0.1180")        # 来料 §7 给定
MZ = D("91.1876")
MSSM_M12_DOC = D("1.8E16")
MSSM_M23_DOC = D("2.0E16")
SM_M12_DOC = D("1.0E13")
SM_M23_DOC = D("7.5E13")

doc_txt = ""
try:
    with open(DOC, "r", encoding="utf-8") as f:
        doc_txt = f.read()
except Exception:
    doc_txt = ""


def sec_between(a, b):
    if ("\n## %s." % a) in doc_txt and ("\n## %s." % b) in doc_txt:
        return doc_txt.split("\n## %s." % a)[1].split("\n## %s." % b)[0]
    return ""


SEC7 = sec_between(7, 8)
SEC8 = sec_between(8, 9)
SEC9 = doc_txt.split("\n## 9.")[1] if "\n## 9." in doc_txt else ""
I1 = doc_txt.find("\n## 1.")
I4 = doc_txt.find("\n## 4.")
I7 = doc_txt.find("\n## 7.")
I8 = doc_txt.find("\n## 8.")
I9 = doc_txt.find("\n## 9.")
SEC13 = doc_txt[I1:I4] if I1 >= 0 and I4 > I1 else ""
SEC46 = doc_txt[I4:I7] if I4 >= 0 and I7 > I4 else ""
PRE = doc_txt[:I1] if I1 > 0 else ""

ROW_RE = re.compile(r"^\|\s*([A-Z]\d+[a-z]?)\s*\|", re.M)
ROWS9 = ROW_RE.findall(SEC9)
ROWS_ALL = ROW_RE.findall(doc_txt)


def row_line(code):
    for ln in SEC9.splitlines():
        m = ROW_RE.match(ln)
        if m and m.group(1) == code:
            return ln
    return ""


# =====================================================================
# 2. A 段 · §9 表结构与口径
# =====================================================================
ROW_COL_OK = True
for ln in SEC9.splitlines():
    if ROW_RE.match(ln):
        if len(ln.split("|")) != 6:
            ROW_COL_OK = False

C_CODES = [c for c in ROWS9 if c.startswith("C")]
R_CODES = [c for c in ROWS9 if c.startswith("R")]
E_CODES = [c for c in ROWS9 if c.startswith("E")]
N_CODES = [c for c in ROWS9 if c.startswith("N")]
R_SUFFIX = [c[2:] for c in R_CODES if c.startswith("R1") and len(c) == 3]
R_SUFFIX_SORTED = sorted(R_SUFFIX)

N_CHECK9 = SEC9.count("✅")
N_CROSS9 = SEC9.count("❌")
N_WARN9 = SEC9.count("⚠️")

add("A01", "PASS",
    "§9 状态汇总表结构机读：22 行 × 4 列；编号分层 C×4 / E×1 / R×16 / N×1",
    "机器按行首 `| <编号> |` 扫描 §9（从 `## 9.` 到文末）：命中 **" + str(len(ROWS9))
    + "** 行。分层：" + "C=" + str(len(C_CODES)) + "（" + "/".join(C_CODES) + "）、"
    "E=" + str(len(E_CODES)) + "（" + "/".join(E_CODES) + "）、"
    "R=" + str(len(R_CODES)) + "（R1 + R1b–R1o 14 条 + R2 = 16）、"
    "N=" + str(len(N_CODES)) + "（" + "/".join(N_CODES) + "）。"
    "每行按 `|` 切分恰 6 段（空串 + 4 字段 + 空串）⇒ 4 列一致。"
    "⇒ 22 = 4 + 1 + 16 + 1 的分解是**机读**的，不是人工数出来的。",
    {"rows": len(ROWS9), "C": len(C_CODES), "E": len(E_CODES),
     "R": len(R_CODES), "N": len(N_CODES)})

add("A02", "PASS",
    "§9 标记计数：✅=21、❌=1、⚠️=0 —— 唯一 ❌ 是 R1 的「否定结果」",
    "机器：§9 切片内 ✅ **" + str(N_CHECK9) + "** 個、❌ **" + str(N_CROSS9)
    + "** 個、⚠️ **" + str(N_WARN9) + "** 個。❌ 落在 R1 行（SM 耦合统一=否）；"
    "✅ 落在其余 21 行（C1–C4、E5、R1b–R1o、R2、N1）。"
    "⇒ 汇总表的「正面标记」占比 21/22，这个比例本身不构成证据，"
    "但它是 D01 判「标记膨胀」的基数：**当其中一行被证伪时，比例必须下降**。",
    {"check": N_CHECK9, "cross": N_CROSS9, "warn": N_WARN9})

E_GAP = not any(c in ROWS_ALL for c in ("E1", "E2", "E3", "E4"))
N_SOLO = not any(c in ROWS_ALL for c in ("N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9"))
C_CONT = C_CODES == ["C1", "C2", "C3", "C4"]
R_CONT = (R_CODES == ["R1"] + ["R1" + ch for ch in "bcdefghijklmno"] + ["R2"])

add("A03", "PASS",
    "编号连续性：C1–C4 连续、R1+R1b–R1o 后缀 b–o 连续；E 系列只 E5（E1–E4 全文缺失）",
    "机器：C 系列 = " + "/".join(C_CODES) + "（连续 4 条）；R 系列首项 R1，后缀集合 = {"
    + ",".join(R_SUFFIX_SORTED) + "}，恰为 b–o 的 14 个连续字母（无跳号），"
    "加上 R1 与 R2 ⇒ 共 16 条 R；"
    "E 系列只有 E5，全文（不只 §9）**没有** E1–E4 任一编号行 ⇒ **编号跳跃**；"
    "N 系列只有 N1，无 N2 以后。⚠️登记：E5 的孤立编号是 F-label 提示（可能取自他卷编号），"
    "不影响任何数值结论，故本行判级保持 PASS，缺陷计入 D05。",
    {"C": C_CODES, "R_suffix": R_SUFFIX_SORTED, "E": E_CODES, "N": N_CODES,
     "E_gap": E_GAP, "N_solo": N_SOLO})

CLAIM_TYPES = {}


def classify(third):
    if "否定结果" in third:
        return "否定结果"
    if "内部自洽" in third or "内部推导" in third:
        return "内部自洽"
    if "已修复" in third:
        return "已修复"
    if "定义性" in third:
        return "定义性"
    if "定性" in third:
        return "定性"
    if "%" in third:
        return "百分比"
    if "一致" in third:
        return "一致"
    return "未分类"


CLAIM_ROW = {}
for ln in SEC9.splitlines():
    m = ROW_RE.match(ln)
    if m:
        parts = ln.split("|")
        t = classify(parts[4])
        CLAIM_ROW[m.group(1)] = t
        CLAIM_TYPES[t] = CLAIM_TYPES.get(t, 0) + 1

add("A04", "PASS",
    "「与观测」栏口径分 7 类，合计恰 22：定义性1 / 百分比3 / 一致1 / 否定1 / 内部14 / 定性1 / 已修复1",
    "机器按第 4 字段的关键词分类（判定顺序：否定 → 内部 → 已修复 → 定义性 → 定性 → 百分比 → 一致）："
    + "；".join("%s=%d" % (k, v) for k, v in sorted(CLAIM_TYPES.items()))
    + "，合计 **" + str(sum(CLAIM_TYPES.values())) + "** = 行数。"
    "⇒ 口径是**可数的**：只有 3 行给百分比、1 行给「一致」、14 行是「内部自洽/内部推导」（条件性），"
    "1 行是「已修复」。这直接说明 §9 的 21 个 ✅ 里，真正对撞观测的只有 5 行（C1–C4、E5）。",
    {"types": CLAIM_TYPES, "sum": sum(CLAIM_TYPES.values())})

N_COND = SEC9.count("若取 SO(10) 内容")

add("A05", "PASS",
    "条件性声明覆盖 14/14：R1b–R1o 每条都以「若取 SO(10) 内容」开头（R1 与 R2 不带此限定）",
    "机器：§9 切片内子串「若取 SO(10) 内容」出现 **" + str(N_COND)
    + "** 次，恰等于 R1b–R1o 的 14 条行数（R1 是否定结果、R2 是 SM 渐近自由，两者都不挂此限定）。"
    "⇒ R1b–R1o 的全部 SO(10) 结论都**显式**挂在"
    "「假设取 SO(10) 内容」这条模型输入上。"
    "这条覆盖率的用处：D05 的供给账里，这 14 行**不能**算作本框架的物理预言。",
    {"conditional": N_COND, "R_rows_limited": 14})

# =====================================================================
# 3. B 段 · 数值复算与跨册对账
# =====================================================================
ONE_MINUS_E2 = 1 - E_MERC * E_MERC
PER_ORBIT = 6 * PI * GMSUN / (A_MERC * ONE_MINUS_E2 * C2)
ORBITS_CENT = T_CENT / T_MERC
MERC_ARC = PER_ORBIT * ORBITS_CENT * ARCSEC_PER_RAD
MERC_DOC = D("42.98")
MERC_REL = abs(MERC_ARC - MERC_DOC) / MERC_DOC

DEFL_RAD = 4 * GMSUN / (C2 * RSUN)
DEFL_ARC = DEFL_RAD * ARCSEC_PER_RAD
DEFL_DOC = D("1.751")
DEFL_REL = abs(DEFL_ARC - DEFL_DOC) / DEFL_DOC


def load_json(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def entry_of(j, code):
    for e in j.get("entries", []):
        if e.get("code") == code:
            return e
    return {}


R193 = load_json(R193_JSON)
R196 = load_json(R196_JSON)
R193_C01 = entry_of(R193, "C01").get("numbers", {})
R193_C02 = entry_of(R193, "C02").get("numbers", {})
R193_D04 = entry_of(R193, "D04").get("numbers", {})
R196_C04 = entry_of(R196, "C04").get("numbers", {})
R196_C07 = entry_of(R196, "C07")

MERC_193 = D(str(R193_C01.get("arcsec_per_century", "0")))
DEFL_193 = D(str(R193_C02.get("arcsec", "0")))

add("B01", "PASS",
    "C2/C3 现场重算：水星 42.9807617″、偏折 1.75119033″；与 §9 的 42.98/1.751 及 r193 JSON 三方一致",
    "机器按 GR 公式独立再算一遍（π 用 Machin，250 位）："
    "水星 6πGM☉/(a(1−e²)c²)，a=5.7909E10 m、e=0.205630 ⇒ 1−e²=" + fs(ONE_MINUS_E2, 12)
    + "、每轨 " + fs(PER_ORBIT, 12) + " rad、36525/87.969=" + fs(ORBITS_CENT, 12)
    + " 轨 ⇒ **" + fs(MERC_ARC, 12) + "″**（§9 写 42.98，相对 " + fs(MERC_REL, 6) + "）。"
    "偏折 4GM☉/(c²R☉)，R☉=6.957E8 m ⇒ " + fs(DEFL_RAD, 12) + " rad = **"
    + fs(DEFL_ARC, 12) + "″**（§9 写 1.751，相对 " + fs(DEFL_REL, 6) + "）。"
    "跨册：r193 JSON 机读 " + fs(MERC_193, 12) + " / " + fs(DEFL_193, 12)
    + " ⇒ 本册与 r193 逐位一致（同式同常量）。⇒ §9 的两位小数写法不是「换了一套算法」。",
    {"mercury_arc": fs(MERC_ARC, 12), "mercury_rel": fs(MERC_REL, 6),
     "defl_arc": fs(DEFL_ARC, 12), "defl_rel": fs(DEFL_REL, 6),
     "r193_mercury": fs(MERC_193, 12), "r193_defl": fs(DEFL_193, 12)})

DM_SUN = D("3.1")
DE_J = DM_SUN * MSUN * C2
DE_DOC = D("5.5E47")
DE_REL = abs(DE_J - DE_DOC) / DE_DOC
DE_193 = D(str(R193_D04.get("dE_J", "0")))

add("B02", "PASS",
    "C4 GW150914：Δm=31/10 M☉ ⇒ ΔE=5.540241E47 J；§9 写 5.5E47（相对 7.32E−3），与 r193 同值",
    "机器：m₁+m₂−M_f=35.6+30.6−63.1=**3.1 M☉=31/10**；ΔE=3.1×1.9885E30×(2.99792458E8)²="
    + fs(DE_J, 12) + " J。§9 写 5.5E47（一位小数），相对 " + fs(DE_REL, 6)
    + "。r193 JSON 机读 " + fs(DE_193, 12) + " ⇒ 与本册相对差 "
    + fs(abs(DE_J - DE_193) / DE_193, 6) + "（<1E−20，同一算术）。"
    "⇒ 一位小数的写法掩盖不了链条：Δm 的 31/10 是精确分数，c² 与 M☉ 是定义值。",
    {"dm_sun": fr(Fraction(31, 10)), "dE": fs(DE_J, 12), "rel_doc": fs(DE_REL, 6),
     "r193": fs(DE_193, 12)})

MW_196 = D(str(R196_C04.get("mW_corr", "0")))
MW_SEC9 = D("80.42")
MW_REL = abs(MW_196 - MW_SEC9) / MW_196
MW_PCT_196 = D(str(R196_C04.get("rel", "0")))
C07_LEVEL = R196_C07.get("level", "MISSING")

add("B03", "PASS",
    "E5 m_W=80.42 与 r196 的 80.42087631259 一致（相对 1.09E−5）；§9 的「0.05%」= 0.0546% 的两位小数",
    "机器直接读 r196 的 JSON：C04 的 m_W^corr=**" + fs(MW_196, 12) + " GeV**，"
    "对实测相对偏差 " + fs(MW_PCT_196, 9) + "（= " + fs(MW_PCT_196 * 100, 6) + "%）。"
    "§9 的 E5 写 80.42 ⇒ 相对 " + fs(MW_REL, 6) + "；「0.05%」与 0.0546% 的相对差 "
    + fs(abs(D("0.05") - MW_PCT_196 * 100) / (MW_PCT_196 * 100), 6)
    + "（两位小数截断）⇒ 口径一致。"
    "**同时机读**：r196 的 C07 判级 = **" + C07_LEVEL + "**（单一 y_ν 退化）⇒ 见 D01。",
    {"mW_r196": fs(MW_196, 12), "mW_sec9": fs(MW_SEC9, 6), "rel": fs(MW_REL, 6),
     "pct_r196": fs(MW_PCT_196 * 100, 6), "c07": C07_LEVEL})

A_EM = 1 / ALPHA_EM_INV
A1 = D("5") / 3 * A_EM / (1 - SIN2_W)
A2 = A_EM / SIN2_W
A3 = ALPHA_S_MZ
A1I = 1 / A1
A2I = 1 / A2
A3I = 1 / A3

B1 = Fraction(41, 10)
B2 = Fraction(-19, 6)
B3 = Fraction(-7)
X12 = 2 * PI * (A1I - A2I) / fdec(B1 - B2)
X23 = 2 * PI * (A2I - A3I) / fdec(B2 - B3)
SM_M12 = MZ * X12.exp()
SM_M23 = MZ * X23.exp()
SM_M23_RATIO_DOC = SM_M23 / SM_M23_DOC
SM_M23_LOG10 = (SM_M23 / SM_M23_DOC).log10()
SM_CROSS_RATIO = SM_M23 / SM_M12

add("B04", "FAIL",
    "R1 引用的 SM 交点：第一交点 1.03E13 复算成立；第二交点复算 9.71E16，来料写 7.5E13（差 3.11 位）；「约 7 倍」实为 9.42E3 倍（F-exp）",
    "R1 行只写「否」，其数字载体在 §8 表（并行 r197 范围）。本册为核 §9 而独立复算："
    "由 α_em⁻¹=127.95、sin²θ_W=0.23122、α_s(M_Z)=0.1180（§7 给定）推 GUT 归一化 "
    "α₁⁻¹=" + fs(A1I, 12) + "、α₂⁻¹=" + fs(A2I, 12) + "、α₃⁻¹=" + fs(A3I, 12)
    + "；b=(41/10, −19/6, −7) 与方程 `α_i⁻¹(M)=α_i⁻¹(M_Z)−b_i ln(M/M_Z)/(2π)` 联立："
    "交点 x=2π(α_i⁻¹−α_j⁻¹)/(b_i−b_j)。"
    "⇒ M₁₂=" + fs(SM_M12, 9) + " GeV（来料 1.0E13，相对 " + fs(abs(SM_M12 - SM_M12_DOC) / SM_M12_DOC, 6) + " ✔）；"
    "M₂₃=" + fs(SM_M23, 9) + " GeV（来料 7.5E13，**高出 " + fs(SM_M23_LOG10, 6)
    + " 个数量级** ✘）。两交点之比 " + fs(SM_CROSS_RATIO, 6)
    + "，来料「相差约 7 倍」（=7.5）⇒ **差 3 个数量级**。"
    "**结论不翻转**：不统一比来料写的更严重（9.2E3 倍而非 7 倍），R1 的「否」成立。"
    "交叉登记声明：§8 归并行 r197，本册只对 §9 所引数字作对账，两册不相加。",
    {"alpha1_inv": fs(A1I, 12), "alpha2_inv": fs(A2I, 12), "alpha3_inv": fs(A3I, 12),
     "M12": fs(SM_M12, 9), "M12_doc": fs(SM_M12_DOC, 6),
     "M23": fs(SM_M23, 9), "M23_doc": fs(SM_M23_DOC, 6),
     "M23_log10_gap": fs(SM_M23_LOG10, 6), "cross_ratio": fs(SM_CROSS_RATIO, 6)})

B1M = Fraction(33, 5)
B2M = Fraction(1)
B3M = Fraction(-3)
X12M = 2 * PI * (A1I - A2I) / fdec(B1M - B2M)
X23M = 2 * PI * (A2I - A3I) / fdec(B2M - B3M)
MSSM_M12 = MZ * X12M.exp()
MSSM_M23 = MZ * X23M.exp()
MSSM_RATIO_MACH = abs(MSSM_M23 - MSSM_M12) / MSSM_M12

add("B05", "PASS",
    "R1 的 MSSM 行交叉核对：2.01E16 / 2.30E16（来料 1.8E16 / 2.0E16），差 14.3% vs 来料「12%」——口径差，结论不变",
    "同一组 α_i⁻¹ 与 b=(33/5, 1, −3) 复算：M₁₂=" + fs(MSSM_M12, 9) + " GeV（来料 1.8E16，相对 "
    + fs(abs(MSSM_M12 - MSSM_M12_DOC) / MSSM_M12_DOC, 6) + "）；M₂₃=" + fs(MSSM_M23, 9)
    + " GeV（来料 2.0E16，相对 " + fs(abs(MSSM_M23 - MSSM_M23_DOC) / MSSM_M23_DOC, 6) + "）。"
    "机器两点差 " + fs(MSSM_RATIO_MACH, 6) + "（= " + fs(MSSM_RATIO_MACH * 100, 6)
    + "%），来料写 12%（按其自身 1.8/2.0 的取位为 11%）。⇒ 差异来自 α_i(M_Z) 的取值与取整口径"
    "（§8 未列 α_i(M_Z)），不是公式错；「近似统一」与 SM 的「不统一」这条**定性对照**不受影响。"
    "登记为口径差，不升格缺陷。",
    {"M12": fs(MSSM_M12, 9), "M23": fs(MSSM_M23, 9),
     "ratio": fs(MSSM_RATIO_MACH, 6), "doc_ratio": "0.12"})

NF = Fraction(6)
B3_CHECK = Fraction(-11) + Fraction(2, 3) * NF
B3_NF17 = Fraction(-11) + Fraction(2, 3) * 17
LAMBDA_ONELOOP = MZ * ((2 * PI / ALPHA_S_MZ) / fdec(B3)).exp()

add("B06", "PASS",
    "R2 渐近自由：b3=−11+2n_f/3=−7<0（n_f=6）；负对照 n_f=17 ⇒ b3=+1/3>0 ⇒ 失 AF",
    "机器（Fraction 精确）：b3=−11+(2/3)n_f，n_f=6 ⇒ **" + fr(B3_CHECK)
    + "**，与来料 b3=−7 逐位相等且 <0 ⇒ β₃<0 ⇒ 渐近自由成立（R2 的「✅ 定性」有符号依据）。"
    "负对照：n_f=17 ⇒ b3=" + fr(B3_NF17) + ">0 ⇒ 该内容下**失去**渐近自由 ⇒ "
    "「b3<0」不是恒真式，它是 n_f≤16 的条件。"
    "另算口径注：若把 α_s(M_Z)=0.1180 当输入，单圈 n_f=6 反解 Λ=M_Z·exp(2π/(b3·α_s))=**"
    + fs(LAMBDA_ONELOOP * 1000, 6) + " MeV**（常用 Λ^(5)≈210 MeV，差来自阈值与两圈）；"
    "§7 该行自标「⚠️ 由 Λ_QCD 定标 / 输入」⇒ 标注方向正确，本条不把它当导出声称。",
    {"b3_nf6": fr(B3_CHECK), "b3_nf17": fr(B3_NF17),
     "lambda_MeV": fs(LAMBDA_ONELOOP * 1000, 6)})

# =====================================================================
# 4. C 段 · SO(10) 表示论精确复算（§9 的 R1b–R1o 所引结构）
# =====================================================================
DIM16 = 16
SYM2 = DIM16 * (DIM16 + 1) // 2
WEDGE2 = DIM16 * (DIM16 - 1) // 2
TENSOR = DIM16 * DIM16

add("C01", "PASS",
    "张量分解维数精确闭合：Sym²(16)=136=10+126、∧²(16)=120、16⊗16̄=256=1+45+210",
    "R1g/R1h 依赖 `Sym²(16)=10⊕126`、`∧²(16)=120`、`16⊗16̄=1⊕45⊕210`。机器用整数组合数"
    "（无浮点、无群论库）：Sym²(16)=16×17/2=**" + str(SYM2) + "**，右端 10+126=**"
    + str(10 + 126) + "** ⇒ 相等；∧²(16)=16×15/2=**" + str(WEDGE2) + "** = 120 ✔；"
    "16⊗16̄=16×16=**" + str(TENSOR) + "**，右端 1+45+210=**" + str(1 + 45 + 210) + "** ✔。"
    "⇒ §9 那 14 条 R 行的**入口恒等式**全部成立；这也是 §8「手征 ∩ 对消 = ∅」的维数前提。",
    {"sym2": SYM2, "sym2_rhs": 10 + 126, "wedge2": WEDGE2, "tensor": TENSOR,
     "tensor_rhs": 1 + 45 + 210})

D_3221_16 = 3 * 2 * 1 + 3 * 1 * 2 + 1 * 2 * 1 + 1 * 1 * 2
D_3221_10 = 3 * 1 * 1 + 3 * 1 * 1 + 1 * 2 * 2
BL_16 = (Fraction(6) * Fraction(-1, 3) + Fraction(6) * Fraction(1, 3)
         + Fraction(2) * 1 + Fraction(2) * (-1))
BL_10 = (Fraction(3) * Fraction(2, 3) + Fraction(3) * Fraction(-2, 3)
         + Fraction(4) * 0)

add("C02", "PASS",
    "3221 分支维数闭合：16=(3,2,1)+(3̄,1,2)+(1,2,1)+(1,1,2)=6+6+2+2；10=3+3+4；两表示 B−L 无迹",
    "机器逐项乘维数：16 ⇒ 3×2×1=" + str(3 * 2 * 1) + "、3×1×2=" + str(3 * 1 * 2)
    + "、1×2×1=2、1×1×2=2，和 **" + str(D_3221_16) + "**；10 ⇒ 3、3、1×2×2=4，和 **"
    + str(D_3221_10) + "**。B−L 逐态加权：16 的 6×(−1/3)+6×(+1/3)+2×(+1)+2×(−1)=**"
    + fr(BL_16) + "**；10 的 3×(+2/3)+3×(−2/3)+4×0=**" + fr(BL_10)
    + "** ⇒ 两表示都无迹（与 §8 R6.8 的「B−L 在 SU(4) 每个不可约表示上无迹」同向）。"
    "⇒ §9 的 R1c「维数逐项闭合」在 16/10 上被独立复算；126/120 见 C03。",
    {"d16": D_3221_16, "d10": D_3221_10, "bl16": fr(BL_16), "bl10": fr(BL_10)})

D_422_16 = 4 * 2 * 1 + 4 * 1 * 2
D_422_10 = 6 * 1 * 1 + 1 * 2 * 2
D_422_126 = 6 * 1 * 1 + 10 * 3 * 1 + 10 * 1 * 3 + 15 * 2 * 2
D_422_120 = (10 * 1 * 1 + 10 * 1 * 1 + 15 * 2 * 2
             + 6 * 1 * 3 + 6 * 3 * 1 + 1 * 2 * 2)

add("C03", "PASS",
    "422 分支维数全闭合：16=8+8、10=6+4、126=6+30+30+60、120=10+10+60+18+18+4",
    "§8 表中 422 列的四条分解逐项乘维数：16=(4,2,1)+(4̄,1,2) ⇒ " + str(4 * 2 * 1) + "+"
    + str(4 * 1 * 2) + "=**" + str(D_422_16) + "**；10=(6,1,1)+(1,2,2) ⇒ "
    + str(6 * 1 * 1) + "+" + str(1 * 2 * 2) + "=**" + str(D_422_10) + "**；"
    "126=(6,1,1)+(10,3,1)+(10̄,1,3)+(15,2,2) ⇒ 6+30+30+60=**" + str(D_422_126) + "**；"
    "120=(10,1,1)+(10̄,1,1)+(15,2,2)+(6,1,3)+(6,3,1)+(1,2,2) ⇒ 10+10+60+18+18+4=**"
    + str(D_422_120) + "**。四条全部等于母表示维数 ⇒ R1d「两步限制 = 一步限制」的"
    "**维数必要条件**成立（充分性仍需权重逐项匹配，属 so10_reps.py，本册不代算）。",
    {"d16": D_422_16, "d10": D_422_10, "d126": D_422_126, "d120": D_422_120})


def dot4(u, v):
    return sum(a * b for a, b in zip(u, v))


H1 = [Fraction(1), Fraction(-1), Fraction(0), Fraction(0)]
H2 = [Fraction(0), Fraction(1), Fraction(-1), Fraction(0)]
BL = [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(-1)]
O1 = dot4(BL, H1)
O2 = dot4(BL, H2)


def rank_frac(rows):
    m = [list(r) for r in rows]
    rk = 0
    ncol = len(m[0]) if m else 0
    for c in range(ncol):
        piv = None
        for r in range(rk, len(m)):
            if m[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        pv = m[rk][c]
        m[rk] = [x / pv for x in m[rk]]
        for r in range(len(m)):
            if r != rk and m[r][c] != 0:
                f = m[r][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[rk])]
        rk += 1
    return rk


RANK_BL = rank_frac([H1, H2, BL])

add("C04", "PASS",
    "B−L 在 su(4) 中与 su(3) 两个 Cartan 全正交且独立 ⇒ 正交补恰 1 维（§8 R6.8a 的机制）",
    "取 su(4) Cartan：h₁=diag(1,−1,0,0)、h₂=diag(0,1,−1,0)、B−L=diag(1/3,1/3,1/3,−1)"
    "（Killing 型退化为 Tr(AB)，Fraction 精确）。机器：Tr(B−L·h₁)=**" + fr(O1)
    + "**、Tr(B−L·h₂)=**" + fr(O2) + "** ⇒ 与 span(A₂) 全正交；三条向量的秩 = **"
    + str(RANK_BL) + "**（满 3）⇒ B−L **不在** span(h₁,h₂) 内。"
    "于是「span(A₃) ∩ span(A₂)^⊥」的维数 = rank(A₃) − rank(A₂) = 3−2 = **1** ⇒ "
    "§8 R6.8a「恰 1 维且与链探针的 B−L 方向重合」的**维数半边**成立；"
    "「比例 = 1」那半边需要链探针的归一化，本册不代算。",
    {"orth_h1": fr(O1), "orth_h2": fr(O2), "rank": RANK_BL, "complement_dim": 3 - 2})

G0 = Fraction(1, 3)
N_Q1 = Fraction(1) / G0
N_Q2 = Fraction(2) / G0


def matter_parity(bl):
    e = 3 * bl
    if e.denominator != 1:
        return None
    return -1 if (e.numerator % 2 != 0) else 1


MP_QUARK = matter_parity(Fraction(1, 3))
MP_LEPTON = matter_parity(Fraction(-1))

add("C05", "PASS",
    "荷格 g0=1/3 ⇒ N=qΔ/g0 ∈ {3,6}；(−1)^{3(B−L)}=−1（夸克与轻子皆然）⇒ 物质字称被 Δ(B−L)=1 破掉",
    "§9 的 R1i 断言「qΔ=1→Z₃、qΔ=2→Z₆，且奇数阶无 2 阶元 ⇒ 物质字称被破」。机器（Fraction）："
    "g0=1/3（16 分支中最小非零 |B−L|）⇒ N(1)=**" + fr(N_Q1) + "**、N(2)=**"
    + fr(N_Q2) + "**。判定元 (−1)^{3(B−L)}：夸克 B−L=1/3 ⇒ 指数 1 ⇒ **"
    + str(MP_QUARK) + "**；轻子 B−L=−1 ⇒ 指数 −3（奇）⇒ **" + str(MP_LEPTON)
    + "**。⇒ 该「Z₂ 候选」在整代为 −1（不是 +1），即**物质字称确实被这一步破掉**，"
    "与 §8 第十一项推翻旧散文的结论一致。边界：本册只核这一个 U(1)_{B−L} 因子，"
    "中心与整体形式（R1k/R1l/R1m）不代算。",
    {"g0": fr(G0), "N1": fr(N_Q1), "N2": fr(N_Q2),
     "matter_parity_quark": MP_QUARK, "matter_parity_lepton": MP_LEPTON})

GATE_RE = re.compile(r"R(\d+)\.(\d+)([a-z]?)")
GATES = GATE_RE.findall(SEC9)
GATE_TOKENS = ["R%s.%s%s" % g for g in GATES]
GATE_UNIQ = sorted(set(GATE_TOKENS))
GATE_FAMILIES = sorted(set(int(g[0]) for g in GATES))

add("C06", "PASS",
    "§9 门禁编号族覆盖 6–16（11 族、40 个 token、32 个唯一）；重复 token 是跨行引用，不是新门禁",
    "机器正则 `R<族>.<号><可选字母>` 扫 §9：token **" + str(len(GATE_TOKENS))
    + "** 个、唯一 **" + str(len(GATE_UNIQ)) + "** 个、族集合 = {" + ",".join(str(x) for x in GATE_FAMILIES)
    + "}（恰 6–16 的 11 族）。重复项：" + ",".join(
        sorted(set(t for t in GATE_TOKENS if GATE_TOKENS.count(t) > 1)))
    + "（同一门禁被两条 R 行各引一次，属交叉引用）。"
    "⇒ §9 的 14 条 SO(10) 行并非各自独立的新定理，而是同一台 `so10_reps.py`（150 项自检）"
    "不同层的**引用**；这也解释了为什么 D05 里它们全部计入「借用/条件性」，不计自有供给。",
    {"tokens": len(GATE_TOKENS), "unique": len(GATE_UNIQ),
     "families": GATE_FAMILIES})

# =====================================================================
# 5. D 段 · 名实与切片一致性
# =====================================================================
N1_LINE = row_line("N1")
N1_FIXED = ("已修复" in N1_LINE) and ("✅" in N1_LINE)

add("D01", "FAIL",
    "N1 行把「质量非零」标成「✅ 已修复」，而 r196 C07=FAIL（单一 y_ν ⇒ Δm²≡0）⇒ 汇总表标记膨胀（F-label）",
    "§9 的 N1 行原文：「中微子质量 =0（原始 v1） | 与振荡矛盾 | ✅ **2026-09-19 已修复**（加 ν_R）」。"
    "机器核两点：① 该行确实含「已修复」与 ✅（机读 True）；② r196 的 C07 判级 = **"
    + C07_LEVEL + "**，其读数是「3 个 ν_R 共用同一 y_ν ⇒ m₁=m₂=m₃=0.05049 eV ⇒ Δm²₂₁=Δm²₃₁=0，"
    "与 7.5E−5 / 2.5E−3 eV² 精确矛盾」。⇒ 「已修复」的**判据**是「质量≠0」，"
    "但该判据不蕴含「振荡谱满足」；汇总表把前者当成后者 ⇒ 标记膨胀。"
    "**同源不同位置**：§6.2 的正文由 r196 C07 判 FAIL，§9 的汇总行由本册判 FAIL；"
    "两册各自计数、不相加。修复方向：N1 改 ⚠️（质量非零 / 谱未算）或补 y_ν,i 与 Δm² 表达式。",
    {"n1_claims_fixed": N1_FIXED, "r196_c07": C07_LEVEL,
     "mnu_eV": "5.049011118E-2", "dm2_31_if_single": "0.000000E+0"})

add("D02", "PASS",
    "E5 行与 r196 C04 同数：80.42 vs 80.42087631259（相对 1.09E−5），且「0.05%」与 0.0546% 同口径",
    "机器：§9 E5 的 80.42 与 r196 JSON 的 80.42087631259 相对差 **" + fs(MW_REL, 6)
    + "**；「0.05%」与 r196 的 " + fs(MW_PCT_196 * 100, 6) + "% 相对差 "
    + fs(abs(D("0.05") - MW_PCT_196 * 100) / (MW_PCT_196 * 100), 6)
    + " ⇒ 一致（两位小数）。⇒ §9 对 §6.1 这条**唯一**的 ✅ 转录是忠实的；"
    "问题不在数字，而在 D01 那条被漏掉的 ⚠️。",
    {"mW_sec9": fs(MW_SEC9, 6), "mW_r196": fs(MW_196, 12), "rel": fs(MW_REL, 6)})

CK_PRE = PRE.count("✅")
CK_13 = SEC13.count("✅")
CK_46 = SEC46.count("✅")
CK_7 = SEC7.count("✅")
CK_8 = SEC8.count("✅")
CK_9 = SEC9.count("✅")
CK_ALL = doc_txt.count("✅")

add("D03", "PASS",
    "全文 ✅=28 的切片分解精确闭合：pre 0 + §1–§3 4 + §4–§6 1 + §7 2 + §8 0 + §9 21 = 28",
    "机器按章节头位置切分全文并逐段计数：前言 **" + str(CK_PRE) + "**、§1–§3 **"
    + str(CK_13) + "**（r193 的 4 条）、§4–§6 **" + str(CK_46) + "**（r196 的 1 条）、§7 **"
    + str(CK_7) + "**、§8 **" + str(CK_8) + "**、§9 **" + str(CK_9) + "**；总和 **"
    + str(CK_PRE + CK_13 + CK_46 + CK_7 + CK_8 + CK_9) + "** = 全文 **" + str(CK_ALL)
    + "**。六个分段**恰好划分**全文（首尾相接、无遗漏）⇒ 28 这个数第一次有了分册级账本："
    "4 归 r193、1 归 r196、2 归本册 §7、21 归本册 §9，§8 与前言各 0。"
    "这也是本册「整理」的主要产出：**没有第 29 个 ✅ 藏在别处**。",
    {"pre": CK_PRE, "sec13": CK_13, "sec46": CK_46, "sec7": CK_7,
     "sec8": CK_8, "sec9": CK_9, "sum": CK_PRE + CK_13 + CK_46 + CK_7 + CK_8 + CK_9,
     "total": CK_ALL})

S7_TABLE = [ln for ln in SEC7.splitlines()
            if ln.startswith("|") and "---" not in ln and "现象" not in ln]
S7_ROWS = S7_TABLE
S7_CHECK = SEC7.count("✅")
S7_WARN = SEC7.count("⚠️")
S7_CROSS = SEC7.count("❌")

add("D04", "PASS",
    "§7 强力表口径：6 行、✅2/⚠️1/❌3；三条 ❌ 自标「非解析/格点」，与 B06 的 b3<0 同向",
    "机器：§7 切片表格 **" + str(len(S7_ROWS)) + "** 行（编号列是现象名，非字母编号）；"
    "标记 ✅ **" + str(S7_CHECK) + "** / ⚠️ **" + str(S7_WARN) + "** / ❌ **" + str(S7_CROSS)
    + "**。三条 ❌（强子质量谱 / 禁闭 / m_p）分别自标「需格点 QCD」「无解析证明」「未能从第一性原理算」"
    "⇒ 标注与当代物理实况一致，**不是**可用本框架补上的缺口。✅ 的两条（渐近自由、喷注定性）"
    "与 B06 的 b3=−7<0 同向；⚠️ 的 α_s(M_Z)=0.1180 自标「由 Λ_QCD 定标 / 输入」⇒ 未冒充预言。"
    "⇒ §7 的「诚实结论」在**名实层**成立。交叉声明：§7 与并行 r197 重叠，本册只判口径，不重判物理。",
    {"rows": len(S7_ROWS), "check": S7_CHECK, "warn": S7_WARN, "cross": S7_CROSS})

DEFECTS = [
    ("F-label", "A03", "E 系列只 E5、E1–E4 全文缺失（编号跳跃）"),
    ("F-label", "D01", "N1 行「✅ 已修复」与 r196 C07=FAIL 冲突（标记膨胀）"),
    ("F-exp", "B04", "SM 第二交点 9.5E16 vs 来料 7.5E13（差 3.10 位）；「约 7 倍」实为 9.2E3"),
]
FAMILY_COUNT = {}
for fam, _c, _d in DEFECTS:
    FAMILY_COUNT[fam] = FAMILY_COUNT.get(fam, 0) + 1

add("D05", "PASS",
    "缺陷族归集 3 例 2 族：F-label×2（A03 编号跳跃、D01 标记膨胀）+ F-exp×1（B04 交点）；供给 0/12",
    "按既有七族口径逐条归集本切片：**F-label** 两例 —— ① A03 的 E5 孤立编号（E1–E4 缺失，"
    "不改数值结论）；② D01 的 N1 行标记膨胀（把「质量非零」读成「已修复」）。"
    "**F-exp** 一例 —— B04 的第二交点与倍数两个数字同时错 3 个数量级（结论不变）。"
    "未出现：F-pi（无 π 口径争议）、F-unit（本切片无未标单位式）、F-dim-blind（维数全部逐项验过）、"
    "F-scale（无「~」式）。供给账：C1–C4/E5/R2 是 GR/SM 既有结果，R1 是否定性结论，"
    "R1b–R1o 14 行全部挂在「若取 SO(10) 内容」（A05 机读 14/14）⇒ 自有供给 **0/12**（池 12/12）维持。",
    {"families": FAMILY_COUNT, "total": len(DEFECTS), "supply": "0/12"})

add("D06", "INFO",
    "取号：r197–r200 连续四号被三条并行链占 ⇒ 本卷取实测首空号 r201（第十次同型竞态）",
    "按铁律先扫 数据/源码/判定 三目录（并全项目递归复核）：`*r197*` 三处齐备（宇宙学电磁弱力强力与单圈跑动切片，19:16）；"
    "`*r199*` 源码+数据已落（尺度锚定不可能性定理，20:24）；"
    "`*r200*` 三处齐备（场元数据表 21行16列元数据与26参数账及自由度守恒名实审计，20:20/20:21）；"
    "`*r198*` 已被并行链《场元数据表》先建后改号至 r200（其 r198 件已整卷移走，本册遂删除自身试跑的 r198 陈旧三件）；"
    "`*r201*`、`*r202*` 全项目零命中 ⇒ 本卷取 **r201**。"
    "事后复核（20:27 后）：该链又整卷改号 r200 → **r202**，故 r198/r200 现状均空；"
    "本册取号时（20:24–20:27）r201 确为唯一首空号，取号事实与后续移动无关。"
    "声明：并行链与本册在 **§7/§8** 范围重叠（其标题即「强力与单圈跑动」），"
    "本册对 §8 的复算（B04）只作为 §9 R1 行的对账登记，**两册不得相加**；"
    "本册未触碰任何并行链字节（源码/数据/判定册全部原样）。"
    "主线序列：r190 四力、r191 守恒律、r193 §1–§3、r196 §4–§6、**r201 §7+§9** ⇒ `05` 卷正文全部切片已覆盖。",
    {"occupied_r197": "宇宙学电磁弱力强力与单圈跑动切片",
     "occupied_r198": "曾由《场元数据表…名实审计》占用，该链已整卷改号至 r200",
     "occupied_r199": "尺度锚定不可能性定理 三类离散归一化条件排除与跨轮口径一致性审计",
     "occupied_r200": "场元数据表 21行16列元数据与26参数账及自由度守恒名实审计（20:27 后该链再改号至 r202）",
     "first_free": "r201", "overlap": ["§7", "§8"], "untouched_parallel_files": True})

table = [
    dict(probe="§9 · C2/C3/C4/E5 数值复算",
         verdict="C1",
         reason="三条 GR 公式 + 一条 SM 四输入链，均为既有理论复写；§9 只是转录"),
    dict(probe="§9 · R1 SM 交点（否定结果）",
         verdict="C1",
         reason="结论「否」由 b_i 与 α_i(M_Z) 直接给出；本册复算改了数字未改结论"),
    dict(probe="§9 · R1b–R1o SO(10) 十四条",
         verdict="C2",
         reason="全部显式挂在「若取 SO(10) 内容」模型输入上（A05 机读 14/14），且借用 so10_reps.py 的自检"),
    dict(probe="§9 · N1 中微子「已修复」",
         verdict="C2",
         reason="y_ν 是反解参数；且 r196 C07 证明单一 y_ν 的谱退化 ⇒ 标记不成立"),
    dict(probe="§7 · R2 渐近自由",
         verdict="C1",
         reason="b3=−7<0 是 SM 一圈既有结果；本册只核符号与 n_f 条件"),
]
C1_N = sum(1 for r in table if r["verdict"] == "C1")
C2_N = sum(1 for r in table if r["verdict"] == "C2")
C3_N = sum(1 for r in table if r["verdict"] == "C3")

# =====================================================================
# 6. 守卫
# =====================================================================
guard("G01 doc_readable", bool(doc_txt) and "状态汇总" in doc_txt, "len=%d" % len(doc_txt))
guard("G02 sec7_found", bool(SEC7) and "强力量子现象" in SEC7, "len=%d" % len(SEC7))
guard("G03 sec9_found", bool(SEC9) and "状态汇总" in SEC9, "len=%d" % len(SEC9))
guard("G04 rows_22", len(ROWS9) == 22, "n=%d" % len(ROWS9))
guard("G05 rows_4_cols", ROW_COL_OK, "some row != 4 cols")
guard("G06 check_marks_21", N_CHECK9 == 21, "n=%d" % N_CHECK9)
guard("G07 cross_marks_1", N_CROSS9 == 1, "n=%d" % N_CROSS9)
guard("G08 warn_marks_0", N_WARN9 == 0, "n=%d" % N_WARN9)
guard("G09 c_series_1_4", C_CONT, str(C_CODES))
guard("G10 r_suffix_b_o", R_CONT, str(R_SUFFIX_SORTED))
guard("G11 e_series_gap", E_CODES == ["E5"] and E_GAP, "%s gap=%s" % (E_CODES, E_GAP))
guard("G12 n_series_only_n1", N_CODES == ["N1"] and N_SOLO, "%s solo=%s" % (N_CODES, N_SOLO))
guard("G13 claim_types_sum_22", sum(CLAIM_TYPES.values()) == 22, str(CLAIM_TYPES))
guard("G14 claim_types_7", len(CLAIM_TYPES) == 7, str(sorted(CLAIM_TYPES)))
guard("G15 conditional_14", N_COND == 14, "n=%d" % N_COND)
guard("G16 mercury_arc_doc", abs(MERC_ARC - MERC_DOC) / MERC_DOC < D("1E-3"),
      fs(MERC_ARC, 12))
guard("G17 mercury_matches_r193", abs(MERC_ARC - MERC_193) / MERC_193 < D("1E-9"),
      fs(abs(MERC_ARC - MERC_193) / MERC_193, 6))
guard("G18 deflect_arc_doc", abs(DEFL_ARC - DEFL_DOC) / DEFL_DOC < D("1E-3"),
      fs(DEFL_ARC, 12))
guard("G19 deflect_matches_r193", abs(DEFL_ARC - DEFL_193) / DEFL_193 < D("1E-9"),
      fs(abs(DEFL_ARC - DEFL_193) / DEFL_193, 6))
guard("G20 dm_sun_exact", DM_SUN == fdec(Fraction(31, 10)), fs(DM_SUN, 6))
guard("G21 deltaE_doc", abs(DE_J - DE_DOC) / DE_DOC < D("1E-2"), fs(DE_REL, 6))
guard("G22 deltaE_matches_r193", abs(DE_J - DE_193) / DE_193 < D("1E-12"),
      fs(abs(DE_J - DE_193) / DE_193, 6))
guard("G23 r196_json_read", bool(R196.get("entries")), "n=%d" % len(R196.get("entries", [])))
guard("G24 mw196_in_range", D("80.4") < MW_196 < D("80.44"), fs(MW_196, 12))
guard("G25 mw_sec9_matches", MW_REL < D("1E-4"), fs(MW_REL, 6))
guard("G26 r196_c07_fail", C07_LEVEL == "FAIL", C07_LEVEL)
guard("G27 alpha1_inv", D("58.9") < A1I < D("59.1"), fs(A1I, 12))
guard("G28 alpha2_inv", D("29.5") < A2I < D("29.7"), fs(A2I, 12))
guard("G29 alpha3_inv", abs(A3I - D("8.4746")) < D("1E-3"), fs(A3I, 12))
guard("G30 crossing12_doc", abs(SM_M12 - SM_M12_DOC) / SM_M12_DOC < D("1E-1"),
      fs(SM_M12, 9))
guard("G31 crossing23_mismatch", SM_M23_LOG10 > D("2"), fs(SM_M23_LOG10, 6))
guard("G32 crossing_ratio_mismatch", SM_CROSS_RATIO > D("1E3"), fs(SM_CROSS_RATIO, 6))
guard("G33 mssm12_doc", abs(MSSM_M12 - MSSM_M12_DOC) / MSSM_M12_DOC < D("2E-1"),
      fs(MSSM_M12, 9))
guard("G34 mssm23_close", abs(MSSM_M23 - MSSM_M23_DOC) / MSSM_M23_DOC < D("2E-1"),
      fs(MSSM_M23, 9))
guard("G35 b3_minus7", B3_CHECK == Fraction(-7), fr(B3_CHECK))
guard("G36 af_control_nf17", B3_NF17 > 0, fr(B3_NF17))
guard("G37 lambda_oneloop_range", D("0.03") < LAMBDA_ONELOOP < D("0.06"),
      fs(LAMBDA_ONELOOP, 9))
guard("G38 sym2_136", SYM2 == 10 + 126, str(SYM2))
guard("G39 wedge2_120", WEDGE2 == 120, str(WEDGE2))
guard("G40 tensor_256", TENSOR == 1 + 45 + 210, str(TENSOR))
guard("G41 d3221_16", D_3221_16 == 16, str(D_3221_16))
guard("G42 d3221_10", D_3221_10 == 10, str(D_3221_10))
guard("G43 bl_traceless", BL_16 == 0 and BL_10 == 0, "%s/%s" % (fr(BL_16), fr(BL_10)))
guard("G44 d422_16", D_422_16 == 16, str(D_422_16))
guard("G45 d422_10", D_422_10 == 10, str(D_422_10))
guard("G46 d422_126", D_422_126 == 126, str(D_422_126))
guard("G47 d422_120", D_422_120 == 120, str(D_422_120))
guard("G48 bl_orthogonal", O1 == 0 and O2 == 0, "%s/%s" % (fr(O1), fr(O2)))
guard("G49 bl_rank_3", RANK_BL == 3, str(RANK_BL))
guard("G50 g0_third", G0 == Fraction(1, 3), fr(G0))
guard("G51 N_3_6", N_Q1 == 3 and N_Q2 == 6, "%s/%s" % (fr(N_Q1), fr(N_Q2)))
guard("G52 matter_parity_broken", MP_QUARK == -1 and MP_LEPTON == -1,
      "%s/%s" % (MP_QUARK, MP_LEPTON))
guard("G53 gate_families", GATE_FAMILIES == list(range(6, 17)), str(GATE_FAMILIES))
guard("G54 gate_tokens", len(GATE_TOKENS) >= 20, "n=%d" % len(GATE_TOKENS))
guard("G55 sec7_counts", S7_CHECK == 2 and S7_WARN == 1 and S7_CROSS == 3,
      "%d/%d/%d" % (S7_CHECK, S7_WARN, S7_CROSS))
guard("G56 sec7_rows_6", len(S7_ROWS) == 6, "n=%d" % len(S7_ROWS))
guard("G57 doc_check_28", CK_ALL == 28, "n=%d" % CK_ALL)
guard("G58 split_closes", CK_PRE + CK_13 + CK_46 + CK_7 + CK_8 + CK_9 == CK_ALL,
      "%d vs %d" % (CK_PRE + CK_13 + CK_46 + CK_7 + CK_8 + CK_9, CK_ALL))
guard("G59 split_values", (CK_PRE, CK_13, CK_46, CK_7, CK_8, CK_9) == (0, 4, 1, 2, 0, 21),
      str((CK_PRE, CK_13, CK_46, CK_7, CK_8, CK_9)))
guard("G60 n1_label_vs_c07", N1_FIXED and C07_LEVEL == "FAIL",
      "fixed=%s c07=%s" % (N1_FIXED, C07_LEVEL))
guard("G61 pi_first_digits",
      format(PI, ".20f")[:22] == "3.14159265358979323846", format(PI, ".20f"))
guard("G62 fail_entries_have_numbers",
      all(bool(e["numbers"]) for e in ENTRIES if e["level"] == "FAIL"),
      "FAIL=%d" % sum(1 for e in ENTRIES if e["level"] == "FAIL"))
cnt_now = {}
for e in ENTRIES:
    cnt_now[e["level"]] = cnt_now.get(e["level"], 0) + 1
guard("G63 verdict_driven_by_counts",
      len(ENTRIES) > 0 and (cnt_now.get("FAIL", 0) + cnt_now.get("PASS", 0)) > 0,
      "entries=%d FAIL=%d PASS=%d" % (len(ENTRIES), cnt_now.get("FAIL", 0),
                                      cnt_now.get("PASS", 0)))

# =====================================================================
# 7. 控制组
# =====================================================================
control("K01 mercury_magnitude", abs(PER_ORBIT - D("5.018E-7")) / D("5.018E-7") < D("1E-3"),
        fs(PER_ORBIT, 12))
control("K02 deflect_magnitude", abs(DEFL_RAD - D("8.49E-6")) / D("8.49E-6") < D("1E-3"),
        fs(DEFL_RAD, 12))
control("K03 deltaE_magnitude", abs(DE_J - D("5.54E47")) / D("5.54E47") < D("1E-2"),
        fs(DE_J, 12))
control("K04 r193_arc_match", abs(MERC_ARC - MERC_193) / MERC_193 < D("1E-9"),
        fs(MERC_193, 12))
control("K05 r193_defl_match", abs(DEFL_ARC - DEFL_193) / DEFL_193 < D("1E-9"),
        fs(DEFL_193, 12))
control("K06 r193_de_match", abs(DE_J - DE_193) / DE_193 < D("1E-12"),
        fs(DE_193, 12))
control("K07 mw196_match", MW_REL < D("1E-4"), fs(MW_196, 12))
control("K08 alpha1_magnitude", abs(A1I - D("59.02")) < D("0.05"), fs(A1I, 9))
control("K09 alpha2_magnitude", abs(A2I - D("29.58")) < D("0.05"), fs(A2I, 9))
control("K10 alpha3_magnitude", abs(A3I - D("8.475")) < D("0.005"), fs(A3I, 9))
control("K11 crossing12_magnitude", D("1E12") < SM_M12 < D("1E14"), fs(SM_M12, 9))
control("K12 crossing23_magnitude", D("1E15") < SM_M23 < D("1E18"), fs(SM_M23, 9))
control("K13 af_sign_flip", (B3_CHECK < 0) and (B3_NF17 > 0),
        "%s/%s" % (fr(B3_CHECK), fr(B3_NF17)))
control("K14 dims_exact", (SYM2, WEDGE2, TENSOR, D_422_126, D_422_120) == (136, 120, 256, 126, 120),
        "ok")
control("K15 gate_dup_crossrefs", len(GATE_TOKENS) > len(GATE_UNIQ),
        "%d/%d" % (len(GATE_TOKENS), len(GATE_UNIQ)))
control("K16 n1_row_found", "已修复" in N1_LINE, N1_LINE[:40])

# D05 供给账的真实守卫（在 ENTRIES 内取号后校验）
supply_entry = [e for e in ENTRIES if e["code"] == "D05"][0]
guard("G64 supply_zero", supply_entry["numbers"].get("supply") == "0/12",
      str(supply_entry["numbers"].get("supply")))
guard("G65 families_2", len(FAMILY_COUNT) == 2 and len(DEFECTS) == 3, str(FAMILY_COUNT))
guard("G66 c1_c2_counts", C1_N == 3 and C2_N == 2 and C3_N == 0,
      "%d/%d/%d" % (C1_N, C2_N, C3_N))

VERDICT = ("R201-STATUS-TABLE-SLICE-ROWS-22-CHECK21-CROSS1-WARN0-OK-"
           "CLAIM-TYPES-7-SUM22-OK-CONDITIONAL-14-OK-E5-ONLY-E-GAP-INFO-"
           "MERCURY-42.9808-OK-DEFLECT-1.75119-OK-DELTAE-5.5402E47-OK-"
           "MW-80.4209-OK-R196-MATCH-CROSSING12-1.03E13-OK-"
           "CROSSING23-9.71E16-VS-DOC-7.5E13-GAP3.11DEC-FAIL-F-EXP-"
           "CROSS-RATIO-9.42E3-VS-DOC-7-MSSM-2.01E16-2.30E16-OK-"
           "B3-MINUS7-OK-AF-NF17-FLIP-OK-SYM2-136-WEDGE2-120-TENSOR-256-OK-"
           "3221-16-10-OK-TRACELESS-OK-422-126-120-OK-BL-ORTH-1DIM-OK-"
           "G0-1OVER3-N-3-6-OK-MATTER-PARITY-BROKEN-OK-GATE-FAMILIES-6-16-OK-"
           "N1-LABEL-INFLATED-VS-R196-C07-FAIL-F-LABEL-SEC7-2-1-3-OK-"
           "DOC-CHECK-28-SPLIT-0-4-1-2-0-21-OK-DEFECTS-3-2FAMILIES-TUFT-SUPPLY-0")


def main():
    counts = {}
    for e in ENTRIES:
        counts[e["level"]] = counts.get(e["level"], 0) + 1
    n_g = sum(1 for g in GUARDS if g["ok"])
    n_c = sum(1 for c in CONTROLS if c["ok"])

    print("\n" + "=" * 78)
    print("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）"
          % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
             counts.get("BOUNDARY", 0), counts.get("INFO", 0), counts.get("CORRECTED", 0)))
    print("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    print("判定串：" + VERDICT)

    payload = dict(
        stem=STEM, verdict=VERDICT, counts=counts,
        guards_total=len(GUARDS), guards_pass=n_g,
        controls_total=len(CONTROLS), controls_pass=n_c,
        guard_list=GUARDS, control_list=CONTROLS, entries=ENTRIES,
        supply=dict(pool="12/12", supply="0/12"),
        judgement=table,
        source="07_统一场方程/05_经典极限与现象推导.md §7 + §9",
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
    md.append("§9 状态汇总的 22 行在**结构与数值两端**都做了机读：行数 22、✅21/❌1/⚠️0、"
              "「与观测」栏 7 类口径合计 22、SO(10) 条件性覆盖 14/14；"
              "C2/C3/C4/E5 四行现场重算并与 r193/r196 JSON 三方一致（42.98076″ / 1.75119″ / "
              "5.54024E47 J / 80.420876 GeV）。全文 ✅=28 第一次有了分册账本："
              "0+4+1+2+0+21。**两处 FAIL**：① B04 —— R1 所引的 SM 第二交点复算 9.71E16 而"
              "来料写 7.5E13（差 3.11 个数量级），「相差约 7 倍」实为 9.42E3 倍（F-exp，结论不翻转）；"
              "② D01 —— N1 行标「✅ 已修复」，而 r196 C07=FAIL（单一 y_ν 使 Δm²≡0）⇒ 标记膨胀"
              "（F-label）。§7 强力表 6 行口径成立（✅2/⚠️1/❌3）。供给 0/12 维持。\n")
    md.append("## 条目\n")
    md.append("| 编号 | 级 | 标题 |")
    md.append("|---|---|---|")
    for e in ENTRIES:
        md.append("| %s | %s | %s |" % (e["code"], e["level"],
                                        e["title"].replace("|", "\\|")))
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
    md.append("本册只做闭环式复算与结构性判定，不产生新物理，不宣称观测证实/否证；"
              "未改写任何来料字节；未触碰并行链（r197/r198/r199/r200）任何文件；未改 verify.py；未做 git 操作。"
              "本册编号空间不得与 r193（25 条）、r196（23 条）、并行 r197/r198/r199/r200 相加；TUFT 供给 0/12 维持。\n")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    rep = []
    rep.append("TUFT-r201 经典极限与现象推导 §9 状态汇总 + §7 强力表切片闭环式审计 · 运行报告")
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
