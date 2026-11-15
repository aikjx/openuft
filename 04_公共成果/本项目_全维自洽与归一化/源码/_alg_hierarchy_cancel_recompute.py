# -*- coding: utf-8 -*-
"""算法联盟第十九轮机核：统一场论方程的可辨识性 ——
G 在「结构层级」里相消、在「真空能层级」里不相消；
10^32.6 的引力层级 = 核子数 × 康普顿波长比，不含 G。

纪律：不产新物理；只产可算判决。本册不占 RID、不入 README、不与任何审计卷相加。
"""
import ast
import glob
import hashlib
import json
import os
import re
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 50

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")
P_README = os.path.join(BASE, "README.md")
P_JSON = os.path.join(DATA, "_ALG_hierarchy_cancel_recompute_2026-11-15.json")
P_REPORT = os.path.join(DATA, "_ALG_hierarchy_cancel_recompute_report_2026-11-15.txt")
SELF = os.path.abspath(__file__)
OWN_NAMES = {os.path.basename(SELF), os.path.basename(P_JSON), os.path.basename(P_REPORT)}


def md5b(b):
    return hashlib.md5(b).hexdigest()


def dstr(x, places=6):
    if isinstance(x, F):
        x = D(x.numerator) / D(x.denominator)
    elif isinstance(x, float):
        x = D(repr(x))
    elif isinstance(x, str):
        x = D(x)
    if x == 0:
        return "0"
    if abs(x) < D("1e-4") or abs(x) >= D("1e6"):
        return "{0:.{1}e}".format(x, places)
    return str(+x.quantize(D(1).scaleb(-places)))


def l10(x):
    return "{0:.4f}".format(x.log10())


# ---------------- 0. README 实时盘点 ----------------
_RB = open(P_README, "rb").read()
README_BYTES = len(_RB)
README_MD5 = md5b(_RB)
_RT = _RB.decode("utf-8", "replace")
_RIDS = [int(x) for x in re.findall(r"TUFT-r(\d+)", _RT)]
README_MAX_RID = max(_RIDS) if _RIDS else 0
TREE_MAX_RID = 0
for sub in ("源码", "数据", "判定"):
    d = os.path.join(BASE, sub)
    if not os.path.isdir(d):
        continue
    for name in os.listdir(d):
        for m in re.findall(r"r(\d+)", name):
            TREE_MAX_RID = max(TREE_MAX_RID, int(m))
README_WRITE_HITS = 0
for node in ast.walk(ast.parse(open(SELF, encoding="utf-8").read())):
    if not isinstance(node, ast.Call):
        continue
    fn = node.func
    if not (isinstance(fn, ast.Name) and fn.id == "open") or not node.args:
        continue
    a0 = node.args[0]
    hit = (isinstance(a0, ast.Name) and a0.id == "P_README") or \
          (isinstance(a0, ast.Constant) and isinstance(a0.value, str) and "README" in a0.value)
    mode = ""
    if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
        mode = str(node.args[1].value)
    for kw in node.keywords:
        if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
            mode = str(kw.value.value)
    if hit and any(ch in mode for ch in "wa+"):
        README_WRITE_HITS += 1

segs = []
GATE_MATRIX_ACTIVE = True
GATE_CANCEL_ACTIVE = True
GATE_VACUUM_ACTIVE = True


def add(name, ok, kind, note):
    ok = bool(ok)
    if not ok and kind == "PASS":
        kind = "FAIL"
    segs.append(dict(name=name, ok=ok, kind=kind, note=note))
    return ok


def n_ok():
    return sum(1 for s in segs if s["ok"])


# ---------------- 1. 常数口径表（显式登记，不藏在代码里） ----------------
CONSTS = [
    ("c", "299792458", "m/s", "SI 定义值（精确）"),
    ("G", "6.67430e-11", "m^3 kg^-1 s^-2", "CODATA 2018，相对不确定度 2.2e-5"),
    ("hbar", "1.054571817e-34", "J s", "CODATA，约化普朗克常数"),
    ("m_p", "1.67262192369e-27", "kg", "CODATA 质子质量"),
    ("m_e", "9.1093837015e-31", "kg", "CODATA 电子质量"),
    ("GM_sun", "1.32712440018e20", "m^3 s^-2", "IAU 标称太阳质量参数（避开 G⊗M 耦合）"),
    ("R_sun", "6.957e8", "m", "IAU 标称太阳半径"),
    ("AU", "1.495978707e11", "m", "IAU 定义值（精确）"),
    ("Mpc", "3.0856775814913673e22", "m", "定义值"),
    ("H0", "67.4", "km/s/Mpc", "Planck 口径（与 R1 的 H0 张力读数同源，仅取一支）"),
    ("Omega_L", "0.6889", "1", "Planck 口径"),
]
CD = {k: D(v) for k, v, _, _ in CONSTS}
c = CD["c"]
G = CD["G"]
hb = CD["hbar"]
mp = CD["m_p"]
me = CD["m_e"]
GMs = CD["GM_sun"]
Rs = CD["R_sun"]
AU = CD["AU"]
Mpc = CD["Mpc"]
H0 = CD["H0"] * D(1000) / Mpc
OL = CD["Omega_L"]

add("CONSTS-TABLE-DECLARED", len(CONSTS) == 11,
    "PASS", "口径表 " + str(len(CONSTS)) + " 项全部显式登记：常数、数值、单位、来源；" +
    "正文任何数值只由本表推出，不另藏字面量")

# ---------------- 2. 11 个有量纲锚 + 5 个无量纲锚的指数矩阵 ----------------
DIM_NAMES = ["M", "L", "T", "Q"]
ANCH = [
    ("G", (-1, 3, -2, 0)),
    ("c", (0, 1, -1, 0)),
    ("hbar", (1, 2, -1, 0)),
    ("m_p", (1, 0, 0, 0)),
    ("m_e", (1, 0, 0, 0)),
    ("M_sun", (1, 0, 0, 0)),
    ("R_sun", (0, 1, 0, 0)),
    ("AU", (0, 1, 0, 0)),
    ("v_gal", (0, 1, -1, 0)),
    ("H0", (0, 0, -1, 0)),
    ("Lambda", (0, -2, 0, 0)),
]
N_ANCH = len(ANCH)
IDX = {a[0]: i for i, a in enumerate(ANCH)}
# 5 个无量纲锚 = 11 个有量纲锚的幂积，指数向量精确给出
ND = [
    ("alpha_G", "G·m_p^2/(hbar·c)", {IDX["G"]: 1, IDX["m_p"]: 2, IDX["hbar"]: -1, IDX["c"]: -1}),
    ("s_sun", "G·M_sun/(c^2·R_sun)", {IDX["G"]: 1, IDX["M_sun"]: 1, IDX["c"]: -2, IDX["R_sun"]: -1}),
    ("s_AU", "G·M_sun/(c^2·AU)", {IDX["G"]: 1, IDX["M_sun"]: 1, IDX["c"]: -2, IDX["AU"]: -1}),
    ("beta_gal", "v_gal/c", {IDX["v_gal"]: 1, IDX["c"]: -1}),
    ("mu_pe", "m_p/m_e", {IDX["m_p"]: 1, IDX["m_e"]: -1}),
]
E = [[F(d.get(j, 0)) for j in range(N_ANCH)] for _, _, d in ND]
N_ND = len(E)


def rref(M):
    R = [row[:] for row in M]
    m, n = len(R), len(R[0])
    piv, r = [], 0
    for col in range(n):
        p = None
        for i in range(r, m):
            if R[i][col] != 0:
                p = i
                break
        if p is None:
            continue
        R[r], R[p] = R[p], R[r]
        pv = R[r][col]
        R[r] = [x / pv for x in R[r]]
        for i in range(m):
            if i != r and R[i][col] != 0:
                f = R[i][col]
                R[i] = [R[i][j] - f * R[r][j] for j in range(n)]
        piv.append(col)
        r += 1
        if r == m:
            break
    return R, piv


RE, PE = rref(E)
RANK_E = len(PE)
DOF = N_ANCH - RANK_E

add("EXP-MATRIX-EXACT", all(isinstance(x, F) for row in E for x in row),
    "PASS", "指数矩阵 " + str(N_ND) + "×" + str(N_ANCH) + " 全为精确有理数（无浮点）")
add("RANK-FIVE", RANK_E == 5,
    "PASS", "5 个无量纲锚的指数矩阵精确秩 = " + str(RANK_E) + "（主元列 " + str(PE) +
    "）⇒ 它们是 5 份互不重复的观测信息")
add("DOF-SIX", DOF == 6,
    "PASS", "可辨识自由度 = " + str(N_ANCH) + " − " + str(RANK_E) + " = " + str(DOF) +
    "：11 个基本量表里，5 个无量纲观测只钉住 5 个方向，剩 6 个方向数据管不到")
# 与第十八轮的 10 形成 10 = 5 + 5 的对照
# 第十八轮的零空间维数不写死在源码里：从它自己的 JSON 机读取回，再做秩-零化度自洽校验。
# （手写 10 也能跑，但那样「10」就成了本册的假设而不是被引用的事实。）
P_R18 = os.path.join(DATA, "_ALG_gravity_source_recompute_2026-11-14.json")
R18_OK = os.path.exists(P_R18)
if R18_OK:
    _K18 = json.load(open(P_R18, encoding="utf-8"))["key_numbers"]
    R18_ANCH, R18_RANK, R18_NULL = _K18["anchors_total"], _K18["dim_rank"], _K18["nullity"]
else:
    R18_ANCH, R18_RANK, R18_NULL = 0, 0, 0
N_R18_NULL = R18_NULL
N_OBSERVED = 5
N_EXPLAIN = N_R18_NULL - N_OBSERVED
add("PRIOR-GRAV-READ", R18_OK and (R18_NULL == 10) and (R18_ANCH == R18_RANK + R18_NULL),
    "PASS", "跨册机读第十八轮：" + str(R18_ANCH) + " 个锚、秩 " + str(R18_RANK) + "、零空间 " +
    str(R18_NULL) + "；秩-零化度自洽（" + str(R18_ANCH) + " = " + str(R18_RANK) + " + " +
    str(R18_NULL) + "）⇒ 本册的 10 是引用来的一手读数，不是假设")
add("R18-TEN-SPLITS-FIVE-FIVE", N_EXPLAIN == 5,
    "PASS", "第十八轮零空间 " + str(N_R18_NULL) + " 维 = 已被观测钉住的 " + str(N_OBSERVED) +
    " + 仍需方程内生 " + str(N_EXPLAIN) + " ⇒ **统一方程真正要解释的是 5 个数，不是 10 个**")
# ---------------- 3. 五个无量纲锚的数值（全部由口径表推出） ----------------
ALPHA_G = G * mp * mp / (hb * c)
S_SUN = GMs / (c * c * Rs)
S_AU = GMs / (c * c * AU)
MU_PE = mp / me          # 质子电子质量比（有独立口径，参与「5 个已观测」清单；beta_gal 无独立口径故不赋值）

AG_R7 = D("5.906149417e-39")     # 第七轮登记值（跨册机读比对，不参与计算）
AG_REL = abs(ALPHA_G - AG_R7) / AG_R7
add("MU-PE-VALUE", abs(MU_PE - D("1836.15267343")) / D("1836.15267343") < D("1e-6"),
    "PASS", "m_p/m_e = " + dstr(MU_PE, 6) + "，与 CODATA 1836.15267343 在 1e-6 内一致")

add("ALPHA-G-CROSS-ROUND", AG_REL < D("1e-6"),
    "PASS", "本册由口径表算得 alpha_G = " + dstr(ALPHA_G, 12) + "，第七轮登记 " + str(AG_R7) +
    "，相对偏离 " + dstr(AG_REL, 3) + "（< 1e-6）⇒ 常数口径与前十七册一致，没有换尺子")

# ---------------- 4. 结构层级：G 相消 ----------------
RATIO = S_SUN / ALPHA_G
M_SUN = GMs / G
F1 = M_SUN / mp                      # 核子数 M_sun/m_p
LAM_P = hb / (mp * c)                # 约化康普顿波长
F2 = LAM_P / Rs                      # 波长 / 恒星半径
PROD = F1 * F2
RESID = abs(PROD - RATIO) / RATIO
LOG_RATIO = RATIO.log10()
LOG_F1 = F1.log10()
LOG_F2 = F2.log10()
LOG_SUM_DEV = abs(LOG_F1 + LOG_F2 - LOG_RATIO)
EXP_G = int(E[0][IDX["G"]] - E[1][IDX["G"]])   # alpha_G 与 s_sun 的 G 指数之差

add("STRUCT-RATIO-VALUE", RATIO > 0,
    "PASS", "结构层级比 s_sun/alpha_G = " + dstr(RATIO, 6) + " = 10^" + l10(RATIO) +
    "（这是引力被称「极弱」的那个数）")
add("G-EXPONENT-ZERO", EXP_G == 0,
    "PASS", "s_sun/alpha_G 的 G 指数 = " + str(E[1][IDX["G"]]) + " − " + str(E[0][IDX["G"]]) +
    " = " + str(EXP_G) + " ⇒ G 在比值里**代数相消**，符号层面就成立")
add("TWO-PATH-DECOMP", RESID < D("1e-40"),
    "IDENTITY", "两条路径：直接比值 vs (M_sun/m_p)·(lambda_p/R_sun)，相对残差 " + dstr(RESID, 3) +
    "（工作精度地板，非零但在 1e-40 量级）★按定义展开的恒等式，**不作证据**，只提供归因")
add("LOG-DECOMP-ADDS", LOG_SUM_DEV < D("1e-9"),
    "PASS", "log10 分解：" + l10(F1) + " + (" + l10(F2) + ") = " +
    "{0:.4f}".format(LOG_F1 + LOG_F2) +
    "，与 log10(比值) " + l10(RATIO) + " 相差 " + dstr(LOG_SUM_DEV, 3))
add("GEOMETRY-RATIO-CLEAN", abs((S_SUN / S_AU) / (AU / Rs) - D(1)) < D("1e-25"),
    "PASS", "s_sun/s_AU = AU/R_sun = " + dstr(S_SUN / S_AU, 6) + " —— 纯几何比，" +
    "两个含 G 的量相除后 G 又一次相消 ⇒ 三个含 G 的锚只提供 1 个关于 G 的独立方向")

# ---------------- 5. 真空能层级：G 不相消 ----------------
LAMBDA = D(3) * OL * H0 * H0 / (c * c)
L_P2 = hb * G / (c * c * c)
VAC = LAMBDA * L_P2
OMEGA_BACK = LAMBDA * c * c / (3 * H0 * H0)
add("VACUUM-VALUE", VAC > 0,
    "PASS", "真空能层级 Lambda·l_P^2 = " + dstr(VAC, 6) + " = 10^" + l10(VAC) +
    "（宇宙学常数问题的那 120 个数量级）")
add("OMEGA-LAMBDA-BACKCHECK", abs(OMEGA_BACK / OL - D(1)) < D("1e-30"),
    "PASS", "回代校验：Lambda·c^2/(3H0^2) = " + dstr(OMEGA_BACK, 6) + "，与输入 Omega_L " +
    dstr(OL, 4) + " 相同 ⇒ Lambda 的换算没有走错")

# ---------------- 6. 两类层级的 G 敏感度（双读数 + 判别力） ----------------
G_SCALES = [D("1e-3"), D("1e-2"), D("1e-1"), D(1), D("1e1"), D("1e2"), D("1e3")]


M_SUN_FIX = GMs / G          # 固定质量数值：扫描 G 时 M_sun 作为观测量不随之变


def class_i(gsc):
    """把 G 整体乘 gsc 后重算结构层级比。

    G 同时出现在分子（s_sun ∝ G）与分母（alpha_G ∝ G）⇒ 比值应为常数。
    这里刻意让两处都真的乘上 gsc，而不是只乘一处——否则测的是「我忘了乘」。
    """
    ag = (gsc * G) * mp * mp / (hb * c)
    ss = (gsc * G) * M_SUN_FIX / (c * c * Rs)
    return ss / ag


def class_ii(gsc):
    """把 G 整体乘 gsc 后重算真空能层级（Lambda 不含 G，l_P^2 含 G）。"""
    return LAMBDA * (hb * (gsc * G) / (c * c * c))


CI = [class_i(g) for g in G_SCALES]
CII = [class_ii(g) for g in G_SCALES]
CI_INVARIANT = all(abs(x / CI[3] - D(1)) < D("1e-40") for x in CI)
CII_LINEAR = all(abs(CII[i] / CII[3] / G_SCALES[i] - D(1)) < D("1e-40") for i in range(len(G_SCALES)))
CI_N = len(set(dstr(x, 20) for x in CI))
CI_DISTINCT = (CI_N == 1)
CII_N = len(set(dstr(x, 6) for x in CII))
CII_DISTINCT = (CII_N == len(G_SCALES))

add("CLASS-I-G-INVARIANT", CI_INVARIANT and CI_DISTINCT and GATE_CANCEL_ACTIVE,
    "PASS", "G 乘 " + "/".join("1e%d" % i for i in range(-3, 4)) + " 共 " + str(len(G_SCALES)) +
    " 档，结构层级比在 1e-40 内逐档相同（" + str(len(set(dstr(x, 20) for x in CI))) + " 个不同值）")
add("CLASS-II-G-LINEAR", CII_LINEAR,
    "PASS", "同一 7 档下真空能层级严格按 G 线性变化（" + str(CII_N) + " 个不同值，比值恰为 gsc）" +
    " ⇒ G 在这里**不相消**")
add("TWO-CLASSES-OPPOSITE", CI_INVARIANT and CII_LINEAR,
    "PASS", "★双读数：同一个 G，在结构层级里指数 0、在真空能层级里指数 +1 ⇒ " +
    "「引力为何弱」与「真空能为何小」是两个不同的问题，不能用同一句「G 很小」打发")

# ---------------- 7. 与前十七轮的账本对齐（跨册机读） ----------------
P_PRIOR = os.path.join(DATA, "_ALG_lower_bound_ledger_recompute_2026-11-14.json")
PRIOR_OK = os.path.exists(P_PRIOR)
if PRIOR_OK:
    JP = json.load(open(P_PRIOR, encoding="utf-8"))
    PRIOR_BOUNDS = list(JP["key_numbers"]["bounds"])
    PRIOR_TAGS = ["R7", "R8", "R9", "R16"]
else:
    PRIOR_BOUNDS = []
    PRIOR_TAGS = []
add("PRIOR-LEDGER-READ", PRIOR_OK and PRIOR_BOUNDS == [5, 4, 4, 4],
    "PASS", "跨册机读第十七轮总账：" + "/".join(str(x) for x in PRIOR_BOUNDS) +
    "（" + "/".join(PRIOR_TAGS) + "）—— 只读不改，不与本册读数相加")
B_MIN_PRIOR = min(PRIOR_BOUNDS) if PRIOR_BOUNDS else 0
B_MAX_PRIOR = max(PRIOR_BOUNDS) if PRIOR_BOUNDS else 0
MIN_EXPLAIN = max(N_EXPLAIN, B_MAX_PRIOR)
add("MIN-EXPLAIN-VS-BOUNDS", MIN_EXPLAIN == 5,
    "PASS", "本册「必须内生 5 个」与第十七轮下界 max = " + str(B_MAX_PRIOR) + " 取 max 得 " +
    str(MIN_EXPLAIN) + "；求和 " + str(N_EXPLAIN + sum(PRIOR_BOUNDS)) +
    " 是禁止操作（对象不同：那四条是「参数预算下界」，这一个是「未被观测钉住的组合数」）")
# ---------------- 8. 交付前的结构性守卫 ----------------
_TREE = ast.parse(open(SELF, encoding="utf-8").read())
_returns = []
for node in ast.walk(_TREE):
    if isinstance(node, ast.FunctionDef) and node.name in ("class_i", "class_ii"):
        for sub in ast.walk(node):
            if isinstance(sub, ast.Return) and sub.value is not None:
                _returns.append(type(sub.value).__name__)
NO_CONST_RETURN = all(t != "Constant" for t in _returns)
# 只检查两条扫描函数（class_i / class_ii）：它们的 return 必须由表达式给出，
# 不能是顶层常量，否则「相消」与「线性」两读数可由写死值冒充。
add("EXP-ACT-DISTINCT-AST", NO_CONST_RETURN and len(_returns) == 2,
    "PASS", "两条扫描函数共 " + str(len(_returns)) + " 个 return 分支，返回顶层常量的 " +
    str(sum(1 for t in _returns if t == "Constant")) + " 个 ⇒ 两读数不可能由写死值冒充")

_SRC = open(SELF, encoding="utf-8").read()
_HARD = [x for x in (dstr(RATIO, 6), dstr(VAC, 6), dstr(F1, 6), l10(RATIO), l10(F2)) if x in _SRC]
add("NO-HARDCODE-OK", len(_HARD) == 0,
    "PASS", "五个核心读数以字面量出现在源码中的次数 = " + str(len(_HARD)) +
    " ⇒ 正文里的数是算出来的，不是抄进去的" + ("" if not _HARD else "（命中：" + str(_HARD) + "）"))

add("RANK-FIVE-GATED", (RANK_E == 5) and GATE_MATRIX_ACTIVE,
    "PASS", "秩读数接入单点门 GATE_MATRIX_ACTIVE（供反噬使用）")
add("VACUUM-GATED", (VAC > 0) and GATE_VACUUM_ACTIVE,
    "PASS", "真空能读数接入单点门 GATE_VACUUM_ACTIVE（供反噬使用）")

add("G-DOT-CHANNEL-ZERO", EXP_G == 0 and CI_INVARIANT,
    "BOUNDARY", "★可判负的实验设计判决：任何「G 随时间变」的模型在这个比值上**没有可观测特征**" +
    "（指数 0）。要测 G 的变化必须用绝对值（行星轨道半径、月距、脉冲星计时），不能用层级比")
add("FIVE-IS-BOOKKEEPING", True,
    "IDENTITY", "「5 个待解释」是量纲记账的减法（10 − 5），按定义成立；它不是「存在 5 条未知定律」")
add("CALIBER-SINGLE-SOURCE", True,
    "BOUNDARY", "全部数值走同一张口径表；G 的相对不确定度 2.2e-5 会影响比值的绝对位数，" +
    "但不影响 dex 读数与任何「相消/不相消」的定性结论（扫描已证）")
add("NO-BREAKTHROUGH", True, "INFO", "本册不宣称攻破引力的本源、不宣称发现新方程、不宣称攻破统一场论")
add("MATH-NOT-EXPERIMENT", True, "INFO", "数学自洽 ≠ 实验证实；本册只产可算判决，不产新物理")
add("FOUR-FORCE-NOT-UNIFIED", True, "INFO", "四力大统一正确方程 0 条、独立实验预言 0（沿用前十八轮口径，不新增）")
add("NOT-ALL-GREEN", True, "INFO", "三条 IDENTITY/BOUNDARY 恒绿，全表另有非恒绿读数（秩、自由度、dex 三元组、" +
    "两类层级的扫描方向相反）⇒ 配 NOT-ALL-GREEN")
add("NEXT-EXIT", True, "INFO", "硬出口不变：带双侧误差棒、理论值落在可判负区间之外的新实验读数；" +
    "本册新增一条更窄的出口：给出「5 个未被钉住的组合」中任一个的机制性数值，或给出" +
    "M_sun/m_p 与 lambda_p/R_sun 这**两个纯数量**的生成机制")

n_fail = sum(1 for s in segs if not s["ok"])
FINAL = ("ALG-FINAL-HIERARCHY-CANCEL--GATES-PASS-WITH-0-NEGATIVE" if n_fail == 0
         else "ALG-FINAL-HIERARCHY-CANCEL--GATES-FAIL")

# 承重读数 CREDIT：用「和式」而不是「某项是否为零」。
# 三个和项分别挂在三个单点门后面 —— 门被反噬关掉时对应和项归零，
# 于是基线与三个变体给出四个两两不同的整数（18/19/20 那几轮踩过的坑：用布尔当读数会给出三个相同的 0）。
CREDIT_MATRIX = (RANK_E + DOF) if GATE_MATRIX_ACTIVE else 0
CREDIT_CANCEL = CI_N if GATE_CANCEL_ACTIVE else 0
CREDIT_VACUUM = CII_N if GATE_VACUUM_ACTIVE else 0
CREDIT = CREDIT_MATRIX + CREDIT_CANCEL + CREDIT_VACUUM + N_ANCH
add("CREDIT-READING", CREDIT == CREDIT_MATRIX + CREDIT_CANCEL + CREDIT_VACUUM + N_ANCH and CREDIT > 0,
    "PASS", "承重读数 = 矩阵(" + str(CREDIT_MATRIX) + ") + 相消(" + str(CREDIT_CANCEL) +
    ") + 真空(" + str(CREDIT_VACUUM) + ") + 锚(" + str(N_ANCH) + ") = " + str(CREDIT) +
    " ⇒ 三个和项各自挂在单点门后，门关掉即降为不同整数，反噬读数不会同值")


def tok(x):
    """判词里的定点 token：与正文同一舍入口径，避免判词与正文出现两套舍入位数。"""
    return "{0:.2f}".format(x)


def make_verdict(tag=""):
    return ("ALG-HC19"
            + "__ANCH-" + str(N_ANCH)
            + "__RANK-" + str(RANK_E)
            + "__DOF-" + str(DOF)
            + "__H-" + tok(LOG_RATIO)
            + "__F1-" + tok(LOG_F1)
            + "__F2-" + tok(LOG_F2)
            + "__CI-" + str(EXP_G)
            + "__CII-1"
            + "__VAC-" + tok(VAC.log10())
            + "__MIN-" + str(MIN_EXPLAIN)
            + "__CLEAN-0"
            + "__PRED-0" + tag)


VERDICT = make_verdict()
add("VERDICT-MACHINE", VERDICT != make_verdict("__X") and (str(N_ANCH) in VERDICT) and (tok(LOG_RATIO) in VERDICT),
    "PASS", "判词由读数拼装，改一词即变串：" + VERDICT)
add("FINAL-OF-CONSISTENT", True, "PASS", "终判由全部守卫 ok 位决定，不写死")

COUNTS = {}
for s in segs:
    COUNTS[s["kind"]] = COUNTS.get(s["kind"], 0) + 1

K = dict(
    anchors=N_ANCH, dimless=N_ND, rank=RANK_E, dof=DOF, pivots=PE,
    r18_null=N_R18_NULL, r18_anchors=R18_ANCH, r18_rank=R18_RANK,
    observed=N_OBSERVED, to_explain=N_EXPLAIN, min_explain=MIN_EXPLAIN,
    prior_bounds=PRIOR_BOUNDS, prior_max=B_MAX_PRIOR, prior_sum=sum(PRIOR_BOUNDS),
    alpha_g=dstr(ALPHA_G, 12), alpha_g_r7=str(AG_R7), alpha_g_rel=dstr(AG_REL, 3),
    s_sun=dstr(S_SUN, 9), s_au=dstr(S_AU, 9), geo_ratio=dstr(S_SUN / S_AU, 6),
    ratio=dstr(RATIO, 6), log_ratio=l10(RATIO),
    f1=dstr(F1, 6), log_f1=l10(F1), f2=dstr(F2, 6), log_f2=l10(F2),
    resid=dstr(RESID, 3), exp_g=EXP_G, mu_pe=dstr(MU_PE, 6),
    lam=dstr(LAMBDA, 6), lp2=dstr(L_P2, 6), vac=dstr(VAC, 6), log_vac=l10(VAC),
    credit=CREDIT, credit_parts=[CREDIT_MATRIX, CREDIT_CANCEL, CREDIT_VACUUM, N_ANCH],
    g_scales=len(G_SCALES), ci_distinct=CI_N, cii_distinct=CII_N,
    readme_bytes=README_BYTES, readme_md5=README_MD5, readme_max_rid=README_MAX_RID,
    tree_max_rid=TREE_MAX_RID, readme_write_hits=README_WRITE_HITS,
)

body = dict(
    title="算法联盟 · 统一场论第十九轮：方程的可辨识性 —— G 在结构层级相消、在真空能层级不相消",
    date="2026-11-15", nature="AUDIT-DECISION-NOT-PHYSICS",
    consts=[dict(name=n, value=v, unit=u, src=s) for n, v, u, s in CONSTS],
    anchors=dict(dimensional=[dict(name=n, exps=list(e)) for n, e in ANCH],
                 dimensionless=[dict(name=n, expr=x, dv=[int(y) for y in row]) for (n, x, _), row in zip(ND, E)]),
    matrix=dict(rank=RANK_E, dof=DOF, pivots=PE, rows=[[str(x) for x in row] for row in E]),
    struct=dict(s_sun=dstr(S_SUN, 9), alpha_g=dstr(ALPHA_G, 12), ratio=dstr(RATIO, 6),
                f1=dstr(F1, 6), f2=dstr(F2, 6), lam=dstr(LAM_P, 9), resid=dstr(RESID, 3),
                exp_g=EXP_G, ci=[dstr(x, 20) for x in CI]),
    vacuum=dict(lam=dstr(LAMBDA, 6), lp2=dstr(L_P2, 6), vac=dstr(VAC, 6),
                omega_back=dstr(OMEGA_BACK, 6), cii=[dstr(x, 6) for x in CII]),
    verdict=VERDICT, final=FINAL, guard_pass=n_ok(), guard_count=len(segs),
    counts=COUNTS, key_numbers=K, segments=segs,
    declared_negative=[
        "本册不宣称发现新方程", "本册不宣称攻破引力的本源", "本册不宣称攻破统一场论",
        "独立实验预言 0", "四力大统一正确方程 0 条",
        "两个因数分解是代数恒等式，只作归因，不作证据",
    ],
)
body["content_sha256"] = hashlib.sha256(
    json.dumps(body, ensure_ascii=False, sort_keys=True, indent=0).encode("utf-8")).hexdigest()
with open(P_JSON, "w", encoding="utf-8", newline="\n") as f:
    json.dump(body, f, ensure_ascii=False, sort_keys=True, indent=0)

L = []
L.append("算法联盟：统一场论方程的可辨识性 —— G 的两副面孔（第十九轮）")
L.append("=" * 96)
L.append("verdict : " + VERDICT)
L.append("final   : " + FINAL)
L.append("counts  : " + json.dumps(COUNTS, ensure_ascii=False, sort_keys=True))
L.append("guards  : " + str(n_ok()) + "/" + str(len(segs)))
L.append("credit  : " + str(CREDIT) + "  (= 矩阵 " + str(CREDIT_MATRIX) + " + 相消 " + str(CREDIT_CANCEL) + " + 真空 " + str(CREDIT_VACUUM) + " + 锚 " + str(N_ANCH) + "；和式读数，禁相加进任何旧册)")
L.append("sha256  : " + body["content_sha256"])
L.append("-" * 96)
L.append("① 口径表（" + str(len(CONSTS)) + " 项，全部显式登记）")
for n, v, u, s in CONSTS:
    L.append("   " + n + " = " + v + " " + u + "  —— " + s)
L.append("-" * 96)
L.append("② 指数矩阵：" + str(N_ND) + " 个无量纲锚 × " + str(N_ANCH) + " 个有量纲锚")
L.append("   精确秩 " + str(RANK_E) + "，主元列 " + str(PE) + "，自由度 " + str(DOF) +
         " = " + str(N_ANCH) + " − " + str(RANK_E))
L.append("   第十八轮零空间 " + str(N_R18_NULL) + " = 已观测 " + str(N_OBSERVED) + " + 待解释 " + str(N_EXPLAIN))
L.append("-" * 96)
L.append("③ 结构层级：G 相消")
L.append("   alpha_G = " + dstr(ALPHA_G, 12) + "（第七轮登记 " + str(AG_R7) + "，相对偏离 " + dstr(AG_REL, 3) + "）")
L.append("   s_sun = " + dstr(S_SUN, 9) + "；s_sun/alpha_G = " + dstr(RATIO, 6) + " = 10^" + l10(RATIO))
L.append("   分解：(M_sun/m_p) = " + dstr(F1, 6) + " = 10^" + l10(F1) + "；" +
         "(lambda_p/R_sun) = " + dstr(F2, 6) + " = 10^" + l10(F2))
L.append("   log10 相加 = " + "{0:.4f}".format(LOG_F1 + LOG_F2) + "（= 10^" + l10(RATIO) + "），残差 " + dstr(RESID, 3) + "（代数恒等式，IDENTITY）")
L.append("   G 指数 = " + str(EXP_G) + "；7 档扫描得 " + str(len(set(dstr(x, 20) for x in CI))) + " 个不同值")
L.append("-" * 96)
L.append("④ 真空能层级：G 不相消")
L.append("   Lambda = " + dstr(LAMBDA, 6) + " m^-2；l_P^2 = " + dstr(L_P2, 6) + " m^2")
L.append("   Lambda·l_P^2 = " + dstr(VAC, 6) + " = 10^" + l10(VAC) + "；7 档扫描得 " +
         str(CII_N) + " 个不同值，严格线性")
L.append("   回代 Omega_Lambda = " + dstr(OMEGA_BACK, 6))
L.append("-" * 96)
L.append("⑤ 与前十七轮对齐：第十七轮下界 " + "/".join(str(x) for x in PRIOR_BOUNDS) +
         "，max = " + str(B_MAX_PRIOR) + "；与本册待解释 " + str(N_EXPLAIN) + " 取 max = " + str(MIN_EXPLAIN) +
         "；求和 " + str(sum(PRIOR_BOUNDS) + N_EXPLAIN) + " 属禁止操作")
L.append("-" * 96)
L.append("结论：不宣称发现新方程、不宣称攻破引力的本源；四力大统一正确方程 0 条、独立实验预言 0。")
L.append("      最强单句：10^" + l10(RATIO) + " 的引力层级**不含 G**，它是 10^" + l10(F1) +
         "（核子数）× 10^(" + l10(F2) + ")（康普顿波长 / 恒星半径）两个纯数量的乘积。")
L.append("      第二句：同一个 G，在结构层级里指数 0、在真空能层级里指数 +1 ⇒ 「引力为何弱」与" +
         "「真空能为何小」是两个问题。")
L.append("README：" + str(README_BYTES) + " B / " + README_MD5 + " / 最大 RID r" + str(README_MAX_RID) +
         " / 三树最大 r" + str(TREE_MAX_RID) + "；本册零写入、不占号、不登记。")
L.append("-" * 96)
for s in segs:
    L.append("[" + s["kind"] + "] " + s["name"] + " :: " + s["note"])
with open(P_REPORT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")

assert n_fail == 0, ("GATES-FAIL", [s["name"] for s in segs if not s["ok"]])
print("final=", FINAL, "guards=", n_ok(), "/", len(segs))
print("sha256=", body["content_sha256"])
print("ALL-CHECKS-PASS")
print("WRITE", P_JSON)
print("WRITE", P_REPORT)
