# -*- coding: utf-8 -*-
"""
TUFT-r177｜S17 核心公式 3.19「引力光速统一方程 Z = Gc/2」
          及其宣称的「G-c 三重核心闭环」—— 秩审计 + c 可替换性 + 常数口径互斥

00. 编号与定位
  【编号】r177（★改号）。起草时取 r177 并已落盘四件套；登记阶段复查磁盘，
        发现并行会话 `TUFT-r175_空间波动方程_桥关系符号与三维漏项_精算_2026-10-25.*`
        （源码 2026-10-25 00:24:13，早于本卷源码 00:38:22，且该线已推进到 r176）
        ⇒ 按「先占位者为权威，后到者整体改号」纪律，本卷整体改号 r177。
        实测首空号：r175 两份、r176 两份源码，r177 为空。**未改动并行会话任何字节**。
  【靶】S17/04_理论推导/核心公式集/19-引力光速统一方程/光速引力所有表达式.md
        （自称「ZUFT G-c 全公式终极汇总」）
    一、第一性原理本源式：G = 2Z/c ； Z = Gc/2 （并自注 Z = G/(2c) 为错误形式）
    二、三重核心公式·「数学自洽闭环（可互相推导）」：
        ① G = 2Z/c   ② G = c^2 r / m   ③ Z = c^3 r/(2m)（称由前两式联立导出）
    三、相对论衔接：r = Gm/c^2（自称史瓦西半径的 1/2）
    四、量子衔接：G = ħc/m_p^2 ； m_p = sqrt(ħc/G)
  【问题】判这套「闭环」是真约束还是重排；c 是否承担「光速」的专属角色；
         Z 与 m_p 的口径是否唯一。

01. 机读手段
  纯标准库。① 精确有理线性代数（Fraction 高斯消元）对四式取对数线性化后求秩，
  常数项并入 (log2, logc) 二维基，故「可互相推导」可被逐项验证；
  ② c 替换测试（c → 任意 λ）判光速的专属角色；
  ③ Decimal(60) 高精度重算 Z、m_P、史瓦西半径并与靶公布值按有效位数比对；
  ④ (M,L,T,Q) 四元组量纲计算器（Fraction）；
  ⑤ 全目录单位串/语境扫描（m_p 双口径、Z 单位双口径、Z 宣称值）。

02. 红线（纪律）
  · 数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容。
  · 守卫/控制组的 ok 必须由真实计算得出，禁止写死 True。
  · 分层铁律：本卷条目不与 r160–r174 任何卷相加；f 的量纲归 r168，不重判。
  · 靶自承优先；对靶有利的结论单列 PASS，不予否定。
"""

import io
import json
import os
import re
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
T_START = time.time()

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ============================================================
# 路径 / 登记器
# ============================================================
HERE = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.dirname(HERE)
BASE = os.path.dirname(os.path.dirname(NORM))
OUT = os.path.join(NORM, "数据")
STEM = "TUFT-r177_引力光速统一方程_Gc闭环秩与Z口径_精算_2026-10-25"

TARGET = os.path.join(
    BASE, "01_独立体系", "S17_统一场论核心公式", "04_理论推导", "核心公式集",
    "19-引力光速统一方程", "光速引力所有表达式.md")
SCAN_ROOT = os.path.join(BASE, "01_独立体系", "S17_统一场论核心公式")

ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append({"id": iid, "title": title, "status": status,
                  "note": note, "metrics": metrics})


def control(cid, desc, value, expect, ok):
    CONTROLS.append({"id": cid, "desc": desc, "value": value,
                     "expect": expect, "ok": bool(ok)})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def fs(x, n=6):
    try:
        return "%.*e" % (n, float(x))
    except Exception:
        return str(x)


def fr2dec(fr, prec=50):
    """Fraction -> Decimal，保持高精度。"""
    return Decimal(fr.numerator) / Decimal(fr.denominator)


# ============================================================
# 03. 高精度常数（CODATA 2018 与靶文自称值并用）
# ============================================================
C = Decimal("299792458")                 # c，定义值，精确
G = Decimal("6.67430e-11")               # CODATA 2018，靶文自称采用
G_REL_UNC = Decimal("2.2e-5")            # CODATA 2018 相对不确定度
HBAR = Decimal("1.054571817e-34")
M_PLANCK_LIT = Decimal("2.176434e-8")    # 靶文 22 公式表 L192「普朗克质量 m_p」
M_PROTON_LIT = Decimal("1.67262192369e-27")  # 靶文兼容性分析 L288「质子质量 m_p」
M_E = Decimal("9.1093837015e-31")
R_E_CLASS = Decimal("2.8179403262e-15")  # 经典电子半径
R_PROTON = Decimal("0.84e-15")           # 质子电荷半径
M_SUN = Decimal("1.9885e30")
R_SUN = Decimal("6.957e8")
M_EARTH = Decimal("5.9722e24")
R_EARTH = Decimal("6.371e6")
Z_CLAIM = Decimal("1.00065e-2")          # 靶文宣称的 Z 值

C2 = C * C
Z_EXACT = G * C / 2                      # 由靶文自称的 G、c 精算
Z_REL_DEV = (Z_CLAIM - Z_EXACT) / Z_EXACT
Z_DEV_OVER_UNC = abs(Z_REL_DEV) / G_REL_UNC
M_PLANCK_CALC = (HBAR * C / G).sqrt()    # m_p = sqrt(hbar c / G)
M_PLANCK_REL = (M_PLANCK_CALC - M_PLANCK_LIT) / M_PLANCK_LIT
G_FROM_PLANCK = HBAR * C / (M_PLANCK_LIT * M_PLANCK_LIT)
G_FROM_PROTON = HBAR * C / (M_PROTON_LIT * M_PROTON_LIT)
MP_RATIO = M_PLANCK_LIT / M_PROTON_LIT
G_PROTON_DEV = G_FROM_PROTON / G
R_SCH_SUN = 2 * G * M_SUN / C2
RM_REQUIRED = G / C2                     # 式②要求 r/m 恒等于此值

# ============================================================
# 04. 量纲计算器 (M,L,T,Q)，Fraction 精确
# ============================================================
DIM_NAMES = ("M", "L", "T", "Q")


def dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


def dprod(a, k):
    return tuple(x * Fraction(k) for x in a)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dfmt(a):
    parts = []
    for name, v in zip(DIM_NAMES, a):
        if v == 0:
            continue
        parts.append("%s^%s" % (name, v))
    return " ".join(parts) if parts else "1"


D_G = dim(m=-1, l=3, t=-2)              # [G] = M^-1 L^3 T^-2
D_C = dim(l=1, t=-1)                    # [c] = L T^-1
D_M = dim(m=1)
D_R = dim(l=1)
D_F = dim(m=1, l=1, t=-2)               # [F] = M L T^-2
D_HBAR_C = dmul(dim(m=1, l=2, t=-1), D_C)   # [ħ] = M L^2 T^-1
D_Z_DEF = dmul(D_G, D_C)                # [Z] = [Gc/2] = M^-1 L^4 T^-3
D_Z_WRONG = ddiv(D_G, D_C)              # [Z] = [G/(2c)] = M^-1 L^2 T^-1
D_Z_SM = dim(l=-1, t=1)                 # 文档「Z ≈ 0.01 s/m」口径 = L^-1 T^1
D_Z_G1 = D_C                            # 「令 G=1」辩解下的 [Z] = [c] = L T^-1

# 自检：已知量纲对（守卫用，必须真算）
DIM_SELFCHECK = [
    ("[G] 应为 M^-1 L^3 T^-2", D_G, dim(m=-1, l=3, t=-2)),
    ("[ħc] 应为 M L^3 T^-2", D_HBAR_C, dim(m=1, l=3, t=-2)),
    ("[F] 应为 M L T^-2", D_F, dim(m=1, l=1, t=-2)),
    ("[Gc/2] 应为 M^-1 L^4 T^-3", D_Z_DEF, dim(m=-1, l=4, t=-3)),
]
DIM_SELF_OK = all(a == b for _, a, b in DIM_SELFCHECK)

# 式② G = c^2 r/m 的右端量纲
D_EQ2_RHS = ddiv(dmul(dprod(D_C, 2), D_R), D_M)
D_EQ2_OK = D_EQ2_RHS == D_G
# 式③ Z = c^3 r/(2m) 的右端量纲
D_EQ3_RHS = ddiv(dmul(dprod(D_C, 3), D_R), D_M)
D_EQ3_OK = D_EQ3_RHS == D_Z_DEF
# 衔接式 r = Gm/c^2 右端量纲
D_LINK_RHS = ddiv(dmul(D_G, D_M), dprod(D_C, 2))
D_LINK_OK = D_LINK_RHS == D_R
# 量子衔接 G = ħc/m_p^2 右端量纲
D_QG_RHS = ddiv(D_HBAR_C, dprod(D_M, 2))
D_QG_OK = D_QG_RHS == D_G
# Z 形式下万有引力 F = Z·2m1m2/(R^2 c) 右端量纲
D_FZ_RHS = ddiv(dmul(D_Z_DEF, dprod(D_M, 2)), dmul(dprod(D_R, 2), D_C))
D_FZ_OK = D_FZ_RHS == D_F

# ============================================================
# 05. 靶文机读
# ============================================================
READ_OK = False
N_LINES = 0
TXT = ""
try:
    with io.open(TARGET, "r", encoding="utf-8") as f:
        TXT = f.read()
    READ_OK = True
    N_LINES = len(TXT.splitlines())
except Exception as exc:
    TXT = ""

# 归一化 LaTeX 空白（\, 之类），防扫描假阳性
TXT_N = TXT.replace("\\,", " ").replace("\\;", " ").replace("\\!", " ")

PAT_EQ1 = re.compile(r"G\s*=\s*\\?d?frac\{?\s*2\s*Z\s*\}?\s*/?\s*\{?\s*c\s*\}?")
PAT_Z_OK = re.compile(r"Z\s*=\s*\\?d?frac\{?\s*G\s*c\s*\}?\s*/?\s*\{?\s*2\s*\}?")
PAT_Z_BAD = re.compile(r"Z\s*=\s*\\?d?frac\{?\s*G\s*\}?\s*/?\s*\{?\s*2\s*c\s*\}?")
PAT_EQ2 = re.compile(r"G\s*=\s*\\?d?frac\{?\s*c\s*\^?\s*2\s*r\s*\}?\s*/?\s*\{?\s*m\s*\}?")
PAT_EQ3 = re.compile(r"Z\s*=\s*\\?d?frac\{?\s*c\s*\^?\s*3\s*r\s*\}?\s*/?\s*\{?\s*2\s*m\s*\}?")
PAT_LINK = re.compile(r"r\s*=\s*\\?d?frac\{?\s*G\s*m\s*\}?\s*/?\s*\{?\s*c\s*\^?\s*2\s*\}?")
PAT_QG = re.compile(r"G\s*=\s*\\?d?frac\{?\s*\\hbar\s*c\s*\}?\s*/?\s*\{?\s*m_p\s*\^?\s*2\s*\}?")

HIT = {
    "G=2Z/c": len(PAT_EQ1.findall(TXT_N)),
    "Z=Gc/2": len(PAT_Z_OK.findall(TXT_N)),
    "Z=G/(2c)": len(PAT_Z_BAD.findall(TXT_N)),
    "G=c^2r/m": len(PAT_EQ2.findall(TXT_N)),
    "Z=c^3r/(2m)": len(PAT_EQ3.findall(TXT_N)),
    "r=Gm/c^2": len(PAT_LINK.findall(TXT_N)),
    "G=ħc/m_p^2": len(PAT_QG.findall(TXT_N)),
}
# 靶文自承「错误形式」的标注
N_WRONG_FLAG = len(re.findall(r"错误形式", TXT_N))
# 传播动力学记号计数（波算符 / 时间导数 / 传播速度表述）
N_DYNA = (len(re.findall(r"\\partial", TXT_N))
          + len(re.findall(r"\\nabla", TXT_N))
          + len(re.findall(r"传播", TXT_N))
          + len(re.findall(r"波方程|波动方程| retarded|推迟势", TXT_N)))

# ============================================================
# 06. 精确有理线性代数：对数线性化后的秩
# ============================================================
# 变量序 x = (logG, logZ, logr, logm)；常数基 e = (log2, logc)
# 每式写为 Σ a_i x_i + b1*log2 + b2*logc = 0，存为长度 6 的整数向量
V_EQ1 = [1, -1, 0, 0, -1, 1]     # G = 2Z/c
V_EQ2 = [1, 0, -1, 1, 0, -2]     # G = c^2 r / m
V_EQ3 = [0, 1, -1, 1, 1, -3]     # Z = c^3 r/(2m)
V_LINK = [-1, 0, 1, -1, 0, 2]    # r = G m / c^2


def rank(rows):
    """Fraction 高斯消元求秩（精确）。"""
    m = [[Fraction(x) for x in r] for r in rows]
    if not m:
        return 0
    ncol = len(m[0])
    r = 0
    for cidx in range(ncol):
        piv = None
        for i in range(r, len(m)):
            if m[i][cidx] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][cidx]
        m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][cidx] != 0:
                f = m[i][cidx]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == len(m):
            break
    return r


def vec_add(a, b):
    return [x + y for x, y in zip(a, b)]


def vec_sub(a, b):
    return [x - y for x, y in zip(a, b)]


def vec_neg(a):
    return [-x for x in a]


RANK_TRIPLE = rank([V_EQ1, V_EQ2, V_EQ3])          # 宣称「三重闭环」
RANK_WITH_LINK = rank([V_EQ1, V_EQ2, V_EQ3, V_LINK])
EQ3_EQ_EQ2_MINUS_EQ1 = (vec_sub(V_EQ2, V_EQ1) == V_EQ3)   # 含常数项
LINK_EQ_NEG_EQ2 = (vec_neg(V_EQ2) == V_LINK)

# 本源式 Z = Gc/2 的向量：logZ = logG + logc − log2
V_ZGC2 = [-1, 1, 0, 0, 1, -1]
ZGC2_IS_NEG_EQ1 = (vec_neg(V_EQ1) == V_ZGC2)

# 三条「互相推导」路径的真算（Fraction 逐分量）
PATH_12_to_3 = (vec_sub(V_EQ2, V_EQ1) == V_EQ3)     # ①∧② ⇒ ③
PATH_13_to_2 = (vec_add(V_EQ1, V_EQ3) == V_EQ2)     # ①∧③ ⇒ ②
PATH_23_to_1 = (vec_sub(V_EQ2, V_EQ3) == V_EQ1)     # ②∧③ ⇒ ①
ALL_PATHS_OK = PATH_12_to_3 and PATH_13_to_2 and PATH_23_to_1

# 秩计算器正对照（控制组）：三组已知独立的式子
V_C1 = [1, 0, 0, 0, 0, 0]
V_C2 = [0, 1, 0, 0, 0, 0]
V_C3 = [0, 0, 1, 0, 0, 0]
RANK_POS_CTL = rank([V_C1, V_C2, V_C3])
# 秩计算器负对照：三式中第三式 = 第一式 + 第二式
V_N3 = [1, 1, 0, 0, 0, 0]
RANK_NEG_CTL = rank([V_C1, V_C2, V_N3])

# ============================================================
# 07. c 的可替换性：把 c 换成任意 λ，闭环是否仍成立
# ============================================================
LAMBDAS = [Decimal("1e3"), Decimal("1e5"), Decimal("1e8"),
           Decimal("1e12"), Decimal("7.77e6")]
SUB_ROWS = []
SUB_MAX_RES = Decimal(0)
SUB_MAX_CTL = Decimal(0)
for lam in LAMBDAS:
    # 重标定：Z_lam = G*lam/2（与式①同构），r 由 r = Gm/lam^2 给出
    Z_lam = G * lam / 2
    m_test = M_SUN
    r_lam = G * m_test / (lam * lam)
    # ① G = 2 Z_lam / lam
    lhs1 = G
    rhs1 = 2 * Z_lam / lam
    # ② G = lam^2 r / m
    rhs2 = lam * lam * r_lam / m_test
    # ③ Z_lam = lam^3 r /(2m)
    rhs3 = lam ** 3 * r_lam / (2 * m_test)
    res = max(abs(lhs1 - rhs1) / abs(lhs1),
              abs(lhs1 - rhs2) / abs(lhs1),
              abs(Z_lam - rhs3) / abs(Z_lam))
    # 控制：Z 仍取 Z = Gc/2（不随 λ 重标定）时，式① 的残差应为 |c/λ − 1|
    rhs1_ctl = 2 * Z_EXACT / lam
    res_ctl = abs(lhs1 - rhs1_ctl) / abs(lhs1)
    ctl_expect = abs(C / lam - 1)
    SUB_ROWS.append({
        "lambda": fs(lam, 3),
        "residual_recalibrated": fs(res, 3),
        "residual_Z_fixed": fs(res_ctl, 6),
        "expect_c_over_lambda_minus_1": fs(ctl_expect, 6),
        "ctl_match": abs(res_ctl - ctl_expect) / ctl_expect < Decimal("1e-30"),
    })
    SUB_MAX_RES = max(SUB_MAX_RES, res)
    SUB_MAX_CTL = max(SUB_MAX_CTL, res_ctl)
SUB_ALL_ZERO = SUB_MAX_RES < Decimal("1e-40")
SUB_CTL_NONZERO = SUB_MAX_CTL > Decimal("1e-6")
SUB_CTL_ALL_MATCH = all(r["ctl_match"] for r in SUB_ROWS)

# ============================================================
# 08. 经验内容：G = c^2 r / m 对真实天体
# ============================================================
BODIES = [
    ("太阳（实际半径）", R_SUN, M_SUN),
    ("地球（实际半径）", R_EARTH, M_EARTH),
    ("质子（电荷半径）", R_PROTON, M_PROTON_LIT),
    ("电子（经典半径）", R_E_CLASS, M_E),
]
BODY_ROWS = []
BODY_MAX_DEV = Decimal(0)
RM_RATIOS = []
for name, r, m in BODIES:
    g_pred = C2 * r / m
    dev = g_pred / G
    rm = r / m
    rm_ratio = rm / RM_REQUIRED
    RM_RATIOS.append(rm_ratio)
    BODY_ROWS.append({
        "body": name,
        "c2r_over_m": fs(g_pred, 6),
        "G_true": fs(G, 6),
        "ratio_to_G": fs(dev, 6),
        "r_over_m": fs(rm, 6),
        "r_over_m_over_required": fs(rm / RM_REQUIRED, 6),
    })
    if dev > BODY_MAX_DEV:
        BODY_MAX_DEV = dev
RM_SPREAD = max(RM_RATIOS)
RM_MIN = min(RM_RATIOS)

# 二难的「恒等」分支：r 取史瓦西半半径
IDENT_ROWS = []
IDENT_MAX = Decimal(0)
for name, m in [("太阳", M_SUN), ("地球", M_EARTH),
                ("质子", M_PROTON_LIT), ("电子", M_E)]:
    r_half = G * m / C2
    g_back = C2 * r_half / m
    res = abs(g_back - G) / G
    IDENT_ROWS.append({"body": name, "r_half_schwarzschild_m": fs(r_half, 6),
                       "c2r_over_m": fs(g_back, 6), "rel_residual": fs(res, 3)})
    IDENT_MAX = max(IDENT_MAX, res)
IDENT_IS_TAUTOLOGY = IDENT_MAX < Decimal("1e-40")

# ============================================================
# 09. 全目录扫描：m_p 双口径 / Z 单位双口径 / Z 宣称值
# ============================================================
SCAN = {"files": 0, "planck_ctx": [], "proton_ctx": [],
        "z_unit_si": [], "z_unit_sm": [], "z_claim": [], "errors": []}

PAT_PLANCK = re.compile(r"m_p[^0-9]{0,40}?(2\.17\d*e?-?\d*|普朗克质量)")
PAT_PROTON = re.compile(r"m_p[^0-9]{0,40}?(1\.67\d*e?-?\d*|质子质量)")
PAT_CTX_PLANCK = re.compile(r"普朗克质量[^。\n]{0,60}m_p|m_p[^。\n]{0,60}普朗克质量")
PAT_CTX_PROTON = re.compile(r"质子质量[^。\n]{0,60}m_p|m_p[^。\n]{0,60}质子质量")
PAT_Z_SI = re.compile(r"(m\^?4\s*[·\.\s]*\s*kg\^?-?1\s*[·\.\s]*\s*s\^?-?3|"
                      r"m\^4\s*kg\^?\{?-1\}?\s*s\^?\{?-3\}?)")
PAT_Z_CLAIM = re.compile(r"1\.00065")
# 独立符号 Z：排除 ZUFT（Z 后跟 U）、Z_prime / Z'（Z 后跟 _ 或 ' 或字母）
PAT_Z_TOKEN = re.compile(r"(?<![A-Za-z_])Z(?![A-Za-z_0-9'])")


def z_sm_hits(line):
    """行内「Z 的 s/m 口径」命中：s/m 必须可归因于 Z，且排除 k′ 的 C·s/m。"""
    out = []
    for m in re.finditer(r"s/m", line):
        pre = line[max(0, m.start() - 3):m.start()]
        if "C" in pre or "c" in pre:      # C·s/m 是 k′ 的量纲讨论，不是 Z
            continue
        seg = line[max(0, m.start() - 45):m.start()]
        if PAT_Z_TOKEN.search(seg):
            out.append(m.start())
    return out

try:
    for root, dirs, files in os.walk(SCAN_ROOT):
        for fn in files:
            if not fn.lower().endswith(".md"):
                continue
            p = os.path.join(root, fn)
            try:
                with io.open(p, "r", encoding="utf-8", errors="replace") as f:
                    t = f.read()
            except Exception:
                continue
            SCAN["files"] += 1
            tn = t.replace("\\,", " ")
            rel = os.path.relpath(p, BASE).replace("\\", "/")
            for i, line in enumerate(tn.splitlines(), 1):
                if "m_p" not in line:
                    pass
                if PAT_CTX_PLANCK.search(line) or (
                        "m_p" in line and "普朗克" in line):
                    SCAN["planck_ctx"].append(
                        {"file": rel, "line": i, "text": line.strip()[:160]})
                if PAT_CTX_PROTON.search(line) or (
                        "m_p" in line and "质子" in line):
                    SCAN["proton_ctx"].append(
                        {"file": rel, "line": i, "text": line.strip()[:160]})
                if PAT_Z_TOKEN.search(line) and PAT_Z_SI.search(line):
                    SCAN["z_unit_si"].append(
                        {"file": rel, "line": i, "text": line.strip()[:160]})
                if z_sm_hits(line):
                    SCAN["z_unit_sm"].append(
                        {"file": rel, "line": i, "text": line.strip()[:160]})
                if PAT_Z_CLAIM.search(line):
                    SCAN["z_claim"].append(
                        {"file": rel, "line": i, "text": line.strip()[:160]})
except Exception as exc:
    SCAN["errors"].append(str(exc))

N_PLANCK_CTX = len(SCAN["planck_ctx"])
N_PROTON_CTX = len(SCAN["proton_ctx"])
N_Z_SI = len(SCAN["z_unit_si"])
N_Z_SM = len(SCAN["z_unit_sm"])
N_Z_CLAIM = len(SCAN["z_claim"])
# 去重文件数（防「同一文件反复出现」被当成多处独立证据）
F_PLANCK_CTX = len(set(x["file"] for x in SCAN["planck_ctx"]))
F_PROTON_CTX = len(set(x["file"] for x in SCAN["proton_ctx"]))
F_Z_SI = len(set(x["file"] for x in SCAN["z_unit_si"]))
F_Z_SM = len(set(x["file"] for x in SCAN["z_unit_sm"]))
F_Z_CLAIM = len(set(x["file"] for x in SCAN["z_claim"]))
MP_DUAL = (F_PLANCK_CTX >= 1) and (F_PROTON_CTX >= 1)
Z_UNIT_DUAL = (F_Z_SI >= 1) and (F_Z_SM >= 1)

# ============================================================
# 10. 条目 A：闭环秩
# ============================================================
add("A01",
    "「三重核心闭环」秩为 2：式③ ≡ 式② − 式①（连常数项都成立）",
    "FAIL",
    note="四式取对数线性化（变量 logG,logZ,logr,logm，常数基 log2,logc）后做 "
         "Fraction 高斯消元：rank(①,②,③)=%d，且式③向量 == 式② − 式① 逐分量相等"
         "（含 log2/logc 常数项）。故「三重可互相推导」实为「两独立约束 + 一个推论」，"
         "第三式不携带任何新约束。" % RANK_TRIPLE,
    rank_triple=RANK_TRIPLE,
    eq3_is_eq2_minus_eq1=EQ3_EQ_EQ2_MINUS_EQ1)

add("A02",
    "§三 衔接式 r = Gm/c^2 与核心式② G = c^2 r/m 是同一约束（系数向量互为相反数）",
    "FAIL",
    note="V_LINK == −V_EQ2 逐分量成立，rank 不因加入衔接式而增加："
         "rank(①,②,③)=%d → rank(①,②,③,衔接)=%d。"
         "「衔接广义相对论」这一步是核心式②的代数重排，零新增内容。"
         % (RANK_TRIPLE, RANK_WITH_LINK),
    rank_with_link=RANK_WITH_LINK, link_is_neg_eq2=LINK_EQ_NEG_EQ2)

add("A03",
    "宣称 5 式（三闭环 + r 衔接 + 第一性本源式）实际独立约束仅 2",
    "FAIL",
    note="① 与 ② 独立；③ = ② − ①（%s）；衔接 = −②（%s）；本源式 Z=Gc/2 的向量"
         " %s 与 −式① 逐分量相等（%s）。故 5 式只编码 2 个独立关系："
         "G = 2Z/c 与 r = Gm/c^2。"
         % (EQ3_EQ_EQ2_MINUS_EQ1, LINK_EQ_NEG_EQ2, V_ZGC2, ZGC2_IS_NEG_EQ1),
    independent_constraints=RANK_WITH_LINK, claimed_equations=5,
    zgc2_is_neg_eq1=ZGC2_IS_NEG_EQ1)

# ============================================================
# 11. 条目 B：c 的可替换性（「光速」是否承担专属角色）
# ============================================================
add("B01",
    "把 c 换成任意 λ 并重标定 Z，闭环仍精确成立 ⇒ c 不携带任何专属角色",
    "FAIL" if SUB_ALL_ZERO else "INFO",
    note="取 λ ∈ %s，令 Z_λ = Gλ/2、r_λ = Gm/λ²，三式残差最大 %s（机器零）"
         " ⇒ 该「闭环」对任何速度常数都成立，标题中的「光速」只是被塞进分母的"
         "标定因子，不是传播速度。元数据亦自承「该方程是静态比例关系，本身并不包含"
         "引力以光速传播的动力学证明」。"
         % (", ".join(r["lambda"] for r in SUB_ROWS), fs(SUB_MAX_RES, 3)),
    max_residual=fs(SUB_MAX_RES, 3), n_lambda=len(LAMBDAS))

add("B02",
    "判据判别力（负对照）：Z 固定为 Gc/2 而把 c 换成 λ，残差 = |c/λ − 1| ≠ 0",
    "PASS",
    note="不重标定 Z 时残差最大 %s，且与解析预期 |c/λ−1| 逐条吻合"
         "（%d/%d 条相对误差 < 1e−30）⇒ B01 的「残差为零」不是判据恒真的假绿，"
         "而是重标定后的真恒等。"
         % (fs(SUB_MAX_CTL, 6),
            sum(1 for r in SUB_ROWS if r["ctl_match"]), len(SUB_ROWS)),
    max_residual=fs(SUB_MAX_CTL, 6))

add("B03",
    "全篇无传播动力学记号：∂/∇/传播/波动 计数 = %d" % N_DYNA,
    "INFO",
    note="靶文共 %d 行，仅含代数比例式；标题「引力光速统一」无任何波算符、"
         "推迟势或传播速度推导支撑。" % N_LINES,
    dynamics_tokens=N_DYNA, lines=N_LINES)

# ============================================================
# 12. 条目 C：经验内容
# ============================================================
add("C01",
    "式② G = c^2 r/m 对真实天体（实际半径）偏离 G 达 1e5–1e42 倍",
    "FAIL",
    note="太阳 %s×、地球 %s×、质子 %s×、电子 %s×（最大 %s×）。"
         "若式②是普适定律则 G 随物体而变，与 G 为普适常数直接冲突。"
         % (BODY_ROWS[0]["ratio_to_G"], BODY_ROWS[1]["ratio_to_G"],
            BODY_ROWS[2]["ratio_to_G"], BODY_ROWS[3]["ratio_to_G"],
            fs(BODY_MAX_DEV, 6)),
    max_ratio=fs(BODY_MAX_DEV, 6))

RM_DECADES = (RM_SPREAD / RM_MIN).log10()   # 真实跨越的十进制数量级数

add("C02",
    "式②反解要求所有物体 r/m 恒为 G/c^2 = %s m/kg，实测跨越 %.1f 个数量级"
    % (fs(RM_REQUIRED, 6), float(RM_DECADES)),
    "FAIL",
    note="实测 r/m 与要求值之比：太阳 %s、地球 %s、质子 %s、电子 %s"
         " ⇒ 最大/最小 = %s，即跨越 %.1f 个数量级的离散，不存在统一的 r/m。"
         % (BODY_ROWS[0]["r_over_m_over_required"],
            BODY_ROWS[1]["r_over_m_over_required"],
            BODY_ROWS[2]["r_over_m_over_required"],
            BODY_ROWS[3]["r_over_m_over_required"],
            fs(RM_SPREAD / RM_MIN, 3), float(RM_DECADES)),
    required_rm=fs(RM_REQUIRED, 6),
    decades="%.1f" % float(RM_DECADES))

add("C03",
    "二难：r 取史瓦西半半径 ⇒ 恒等式（零预言）；取实际半径 ⇒ 被观测排除",
    "FAIL",
    note="取 r = Gm/c² 时代回式②的残差 %s（机器零）⇒ 式②与衔接式互相定义，"
         "对任何 (m,r) 都不产生可证伪预言；取实际半径则 C01 的 1e5–1e42 倍偏差成立。"
         "两条路都不剩经验内容。" % fs(IDENT_MAX, 3),
    tautology_residual=fs(IDENT_MAX, 3))

# ============================================================
# 13. 条目 D：m_p 双口径
# ============================================================
add("D01",
    "同一体系内 m_p 两个互斥值：普朗克质量 %s kg 与质子质量 %s kg，差 %s 倍"
    % (fs(M_PLANCK_LIT, 6), fs(M_PROTON_LIT, 6), fs(MP_RATIO, 6)),
    "FAIL",
    note="机读扫描 S17 全目录（%d 个 .md）：m_p 与「普朗克质量」同现 %d 处"
         "（分布于 %d 个文件）、与「质子质量」同现 %d 处（%d 个文件）。"
         "二者相差 1.30e19 倍，而 §四 的 G = ħc/m_p² 对二者给出相差 1e38 倍的 G"
         " ⇒ 符号未消歧使核心式的数值不可确定。抽样证据："
         "「%s」/「%s」。"
         % (SCAN["files"], N_PLANCK_CTX, F_PLANCK_CTX, N_PROTON_CTX,
            F_PROTON_CTX,
            (SCAN["planck_ctx"][0]["text"][:60] if SCAN["planck_ctx"] else "—"),
            (SCAN["proton_ctx"][0]["text"][:60] if SCAN["proton_ctx"] else "—")),
    planck_lines=N_PLANCK_CTX, planck_files=F_PLANCK_CTX,
    proton_lines=N_PROTON_CTX, proton_files=F_PROTON_CTX,
    ratio=fs(MP_RATIO, 6))

add("D02",
    "按质子质量读 §四：G = ħc/m_p² = %s，与真值 G 差 %s 倍"
    % (fs(G_FROM_PROTON, 6), fs(G_PROTON_DEV, 6)),
    "FAIL",
    note="若读者按物理学惯例把 m_p 读作质子质量（该体系自身在兼容性分析中正是"
         "这样用的），§四 给出 G ≈ 1.13e28 m³kg⁻¹s⁻²，偏离实测 1.69e38 倍。",
    ratio=fs(G_PROTON_DEV, 6))

add("D03",
    "按普朗克质量读 §四：ħc/m_P² 与 G 一致，相对差 %s" % fs(
        (G_FROM_PLANCK - G) / G, 6),
    "PASS",
    note="m_P = √(ħc/G) 重算 = %s kg，与靶文 22 公式表公布值 %s kg 相对差 %s"
         " ⇒ §四 的两式在「普朗克质量」读法下与标准普朗克单位完全一致，"
         "这是靶文正确且无争议的部分，单列不与 D01/D02 相抵。"
         % (fs(M_PLANCK_CALC, 12), fs(M_PLANCK_LIT, 12), fs(M_PLANCK_REL, 3)),
    m_planck_calc=fs(M_PLANCK_CALC, 12))

# ============================================================
# 14. 条目 E：Z 的量纲与单位口径
# ============================================================
add("E01",
    "量纲闭合：Z = Gc/2 的 [Z] = %s，与 F = Z·2m₁m₂/(R²c) 的要求一致" % dfmt(D_Z_DEF),
    "PASS",
    note="(M,L,T,Q) 四元组精确审计：[Gc/2]=%s；F 的 Z 形式右端 = %s = [F]；"
         "式②右端 = %s = [G]；式③右端 = %s = [Z]；衔接式右端 = %s = [r]；"
         "量子衔接右端 = %s = [G] ⇒ 全式量纲无一出错，这是靶文的真实优点。"
         % (dfmt(D_Z_DEF), dfmt(D_FZ_RHS), dfmt(D_EQ2_RHS), dfmt(D_EQ3_RHS),
            dfmt(D_LINK_RHS), dfmt(D_QG_RHS)),
    dim_Z=dfmt(D_Z_DEF))

add("E02",
    "Z 的单位口径在体系内互斥：m⁴·kg⁻¹·s⁻³（%d 处）与 s/m（%d 处）"
    % (N_Z_SI, N_Z_SM),
    "FAIL",
    note="[m⁴kg⁻¹s⁻³] = %s；[s/m] = %s ⇒ 相差 %s。同一常数 Z ≈ 0.01 被赋予两种"
         "不可通约的单位。机读：SI 形态 %d 处（%d 个文件）、s/m 形态 %d 处"
         "（%d 个文件），两类口径在同一体系内并存。"
         % (dfmt(D_Z_DEF), dfmt(D_Z_SM), dfmt(ddiv(D_Z_DEF, D_Z_SM)),
            N_Z_SI, F_Z_SI, N_Z_SM, F_Z_SM),
    si_lines=N_Z_SI, si_files=F_Z_SI, sm_lines=N_Z_SM, sm_files=F_Z_SM,
    dim_gap=dfmt(ddiv(D_Z_DEF, D_Z_SM)))

add("E03",
    "「令 G=1 时质量量纲被长度-时间替代」的辩解自身算不对",
    "FAIL",
    note="若 G=1（无量纲），[Z] = [Gc/2] = [c] = %s = m/s；而文档写的是 s/m = %s "
         "⇒ 差 %s。该辩解即便在自己的前提（G=1）下也推不出 s/m，"
         "故 s/m 口径不是「单位简化」，而是与定义式冲突的独立错误。"
         % (dfmt(D_Z_G1), dfmt(D_Z_SM), dfmt(ddiv(D_Z_G1, D_Z_SM))),
    dim_under_G1=dfmt(D_Z_G1), gap=dfmt(ddiv(D_Z_G1, D_Z_SM)))

add("E04",
    "Z 的两种形式相差 c² = %s 倍（量纲差 %s）"
    % (fs(C2, 8), dfmt(ddiv(D_Z_DEF, D_Z_WRONG))),
    "FAIL",
    note="(Gc/2)/(G/(2c)) = c² ⇒ 两种形式不可并存。靶文已自注「Z = G/(2c) 为错误形式」"
         "（文内标注 %d 处，机读 Z=G/(2c) 形态 %d 处）⇒ 靶文的自我纠错方向正确，"
         "但该错误形式在体系文档中仍在流通，属未清理的口径污染。"
         % (N_WRONG_FLAG, HIT["Z=G/(2c)"]),
    ratio_c2=fs(C2, 8), wrong_flag=N_WRONG_FLAG)

add("E05",
    "F = Z·2m₁m₂/(R²c) 在 Z = Gc/2 下与牛顿 F = Gm₁m₂/R² 恒等（残差机器零）",
    "FAIL",
    note="代入 Z = Gc/2 得 F = (Gc/2)·2m₁m₂/(R²c) = Gm₁m₂/R²，逐项相消残差 0"
         " ⇒ 「引力光速统一」在力的层面是牛顿万有引力定律的符号替换，"
         "零新增物理内容；元数据也自承推导的最后一步就是「与牛顿定律对比，"
         "消去公因子」。",
    note_residual="exact 0")

add("E06",
    "Z 的宣称值 %s 与靶文自称输入（G=%s, c=%s）的精算值 %s 不符，"
    "相对差 %s（= G 不确定度的 %s 倍）"
    % (fs(Z_CLAIM, 6), fs(G, 6), fs(C, 6), fs(Z_EXACT, 8), fs(Z_REL_DEV, 4),
       fs(Z_DEV_OVER_UNC, 3)),
    "FAIL",
    note="靶文以 6 位有效数字给出 Z ≈ 1.00065e−2，而 G·c/2 的精算为 %s；"
         "偏差 1.97e−4 是 CODATA 2018 的 G 相对不确定度 2.2e−5 的约 9 倍"
         " ⇒ 不是舍入，是算术不自洽。宣称值机读 %d 处（%d 个文件），"
         "不是孤立的笔误而是体系内沿用的数值。"
         % (fs(Z_EXACT, 10), N_Z_CLAIM, F_Z_CLAIM),
    z_exact=fs(Z_EXACT, 10), rel_dev=fs(Z_REL_DEV, 4),
    dev_over_unc=fs(Z_DEV_OVER_UNC, 3), claim_lines=N_Z_CLAIM,
    claim_files=F_Z_CLAIM)

# ============================================================
# 15. 条目 F：循环性
# ============================================================
add("F01",
    "Z 只能由 G 反推 ⇒ G = 2Z/c 是符号替换，不是「G 从几何涌现」",
    "FAIL",
    note="推导链（元数据 §4）明确为：F ∝ (m₁m₂/R²)·c → 立体角积分得因子 2 → "
         "F = Z·2m₁m₂/(R²c) → 「与牛顿定律对比，消去公因子」得 G = 2Z/c。"
         "最后一步用牛顿定律的数值标定了 Z，故 Z ≡ Gc/2 是定义而非导出；"
         "再写回 G = 2Z/c 即循环。元数据自承「循环论证风险」。")

add("F02",
    "靶文自承的三条局限（循环论证风险 / 缺乏动力学信息 / 无独立实验验证）",
    "INFO",
    note="靶方自承优先：这三条与本卷的 A/B/F 结论方向一致，本卷只做机读确证，"
         "不额外加码。")

# ============================================================
# 16. 对靶有利的单列 PASS
# ============================================================
add("G01",
    "量纲：全部 5 式（含 Z 形式万有引力）无一出错",
    "PASS",
    note="(M,L,T,Q) 精确审计全部通过（见 E01）：这是靶文真实且可验证的优点，"
         "本卷的 FAIL 均不建立在量纲错误之上。")

add("G02",
    "r = Gm/c² 确为史瓦西半径的 1/2（靶文自注正确）",
    "PASS",
    note="r_s = 2Gm/c²，太阳 r_s = %s m ⇒ Gm/c² = %s m = r_s/2 ✓。"
         "靶文的该处注释与标准 GR 一致。" % (fs(R_SCH_SUN, 8),
                                             fs(R_SCH_SUN / 2, 8)),
    r_schwarzschild_sun_m=fs(R_SCH_SUN, 8))

add("G03",
    "靶文主动标注「Z = G/(2c) 为错误形式」（文内 %d 处）" % N_WRONG_FLAG,
    "PASS",
    note="靶文的自我纠错方向正确（两种形式确差 c²），单列不与 E04 的「口径污染」相抵。")

add("G04",
    "§四 两式互为逆且与标准普朗克质量一致（相对差 %s）" % fs(M_PLANCK_REL, 3),
    "PASS",
    note="m_P = √(ħc/G) 重算 %s kg vs 靶公布 %s kg ⇒ 该衔接段在「普朗克质量」"
         "读法下完全站得住。" % (fs(M_PLANCK_CALC, 12), fs(M_PLANCK_LIT, 12)))

add("G05",
    "「三重闭环」在数学上确为自洽（任意两式可推第三式）",
    "PASS",
    note="Fraction 逐分量验证三条路径：①∧②⇒③ = %s（式③ == 式②−式①）；"
         "①∧③⇒② = %s（式② == 式①+式③）；②∧③⇒① = %s（式① == 式②−式③）"
         " ⇒ 靶文的「可互相推导」主张本身为真；A01 判的是「因此它只有 2 个"
         "独立约束」，不是判它自相矛盾。"
         % (PATH_12_to_3, PATH_13_to_2, PATH_23_to_1),
    path_12_to_3=PATH_12_to_3, path_13_to_2=PATH_13_to_2,
    path_23_to_1=PATH_23_to_1)

# ============================================================
# 17. 控制组（必须真算，禁写死）
# ============================================================
control("K1", "Z 形式万有引力与牛顿式恒等（Z=Gc/2）",
        fs((abs((Z_EXACT * 2 * M_SUN * M_EARTH / (R_SUN ** 2 * C))
                - (G * M_SUN * M_EARTH / R_SUN ** 2))
            / abs(G * M_SUN * M_EARTH / R_SUN ** 2)), 3),
        "≈0", abs((Z_EXACT * 2 * M_SUN * M_EARTH / (R_SUN ** 2 * C))
                  - (G * M_SUN * M_EARTH / R_SUN ** 2)
                  ) / abs(G * M_SUN * M_EARTH / R_SUN ** 2) < Decimal("1e-40"))

_Z_PERT = Z_EXACT * (1 + Decimal("1e-3"))
control("K2", "扰动检验：Z 放大 1e−3 后式① 残差应 ≈ 1e−3（判据有判别力）",
        fs(abs(2 * _Z_PERT / C - G) / G, 4), "≈1e-3",
        abs(abs(2 * _Z_PERT / C - G) / G - Decimal("1e-3")) < Decimal("1e-6"))

control("K3", "普朗克质量 √(ħc/G) 与靶公布值比对",
        fs(M_PLANCK_REL, 3), "<1e-6", abs(M_PLANCK_REL) < Decimal("1e-6"))

control("K4", "太阳史瓦西半径 2GM/c² 落在 2.9e3 m 量级",
        fs(R_SCH_SUN, 8), "≈2.95e3 m",
        abs(R_SCH_SUN - Decimal("2953")) / Decimal("2953") < Decimal("1e-2"))

control("K5", "秩计算器正对照：3 个独立式 ⇒ rank=3",
        str(RANK_POS_CTL), "3", RANK_POS_CTL == 3)

control("K6", "秩计算器负对照：第三式为前两式之和 ⇒ rank=2",
        str(RANK_NEG_CTL), "2", RANK_NEG_CTL == 2)

control("K7", "c→λ 替换的负对照：Z 不重标定时代入 λ=1e3 残差 = |c/λ−1|",
        SUB_ROWS[0]["residual_Z_fixed"],
        SUB_ROWS[0]["expect_c_over_lambda_minus_1"], SUB_ROWS[0]["ctl_match"])

control("K8", "量纲计算器自检：4 组已知量纲对全部命中",
        "%d/4" % sum(1 for _, a, b in DIM_SELFCHECK if a == b), "4/4",
        DIM_SELF_OK)

control("K9", "靶文读取成功且 7 类公式形态全部命中",
        "%d 行 / 命中 %d 类" % (N_LINES, sum(1 for v in HIT.values() if v > 0)),
        "≥6 类", READ_OK and sum(1 for v in HIT.values() if v > 0) >= 6)

control("K10", "全目录扫描（按文件去重）：m_p 双口径 + Z 单位双口径 均 ≥1",
        "planck=%d/%d proton=%d/%d / si=%d/%d sm=%d/%d"
        % (N_PLANCK_CTX, F_PLANCK_CTX, N_PROTON_CTX, F_PROTON_CTX,
           N_Z_SI, F_Z_SI, N_Z_SM, F_Z_SM), "均 ≥1 个文件",
        MP_DUAL and Z_UNIT_DUAL)

control("K11", "扫描规模守卫：扫到的 .md 文件数 ≥ 50（防路径失效静默变 0）",
        str(SCAN["files"]), "≥50", SCAN["files"] >= 50)

# ============================================================
# 18. 修复定价：7 个修补维度 → 128 组合，宽松/严格双档
# ============================================================
# 缺陷清单（必须被修掉才算「内部自洽」）
DEFECTS = {
    "d1_closed_rank": True,     # 三重闭环只有 2 个独立约束
    "d2_link_tautology": True,  # 衔接式是核心式②的重排
    "d3_newton_identity": True,  # G=2Z/c 与牛顿定律恒等
    "d4_c_replaceable": True,   # c 可替换为任意 λ
    "d5_mp_ambiguity": True,    # m_p 双口径
    "d6_z_unit_dual": True,     # Z 单位双口径
    "d7_z_value": True,         # Z 宣称值与输入不自洽
}
# 修法 → 修掉的缺陷 / 代价（代价 = 改动的式数或主张数）
FIXES = [
    ("R1 删「三重闭环」措辞，改称「两独立约束 + 一推论」",
     ["d1_closed_rank"], 1),
    ("R2 删去衔接式 r=Gm/c² 或明示其为式②重排",
     ["d2_link_tautology"], 1),
    ("R3 明示 G=2Z/c 是牛顿定律的符号替换",
     ["d3_newton_identity"], 1),
    ("R4 给出 c 的专属角色（补传播动力学/波方程）",
     ["d4_c_replaceable"], 1),
    ("R5 m_p 消歧（普朗克质量改记 m_P）",
     ["d5_mp_ambiguity"], 1),
    ("R6 Z 单位统一为 m⁴·kg⁻¹·s⁻³，撤 s/m 与其辩解",
     ["d6_z_unit_dual"], 1),
    ("R7 Z 值更正为 1.00045e−2",
     ["d7_z_value"], 1),
]
N_FIX = len(FIXES)
REPAIR_ROWS = []
loose_pass = 0
strict_pass = 0
zero_cost_pass = 0
min_cost_strict = None
for mask in range(1 << N_FIX):
    fixed = set()
    cost = 0
    for i in range(N_FIX):
        if mask & (1 << i):
            fixed.update(FIXES[i][1])
            cost += FIXES[i][2]
    remaining = [d for d in DEFECTS if d not in fixed]
    # 宽松档：内部不再自相矛盾（无互斥口径、无错误数值）
    loose = not remaining
    # 严格档：还要保住立论 —— 「G 由 c 与 Z 涌现」必须是非循环的、且带新内容
    keep_claim = not (mask & (1 << 2))   # 未采用 R3（承认是牛顿定律重排）
    has_new_content = (mask & (1 << 3))  # 采用了 R4（给 c 专属角色）
    non_circular = keep_claim
    strict = loose and keep_claim and has_new_content and non_circular
    if loose:
        loose_pass += 1
    if strict:
        strict_pass += 1
        if min_cost_strict is None or cost < min_cost_strict:
            min_cost_strict = cost
    if loose and cost == 0:
        zero_cost_pass += 1
REPAIR_TOTAL = 1 << N_FIX
REPAIR_ROWS.append({"档位": "宽松（仅要求内部自洽）", "通过组合": loose_pass,
                    "总组合": REPAIR_TOTAL})
REPAIR_ROWS.append({"档位": "严格（还要求立论存活且有新内容）",
                    "通过组合": strict_pass, "总组合": REPAIR_TOTAL})
REPAIR_ROWS.append({"档位": "零代价（不改任何式）", "通过组合": zero_cost_pass,
                    "总组合": REPAIR_TOTAL})

add("H01",
    "修复定价：%d 组合中宽松 %d / 严格 %d / 零代价 %d"
    % (REPAIR_TOTAL, loose_pass, strict_pass, zero_cost_pass),
    "FAIL",
    note="严格档要求「保住 G 由 c、Z 涌现的立论」+「c 有专属角色」+「无循环」+"
         "「全部缺陷清零」。R3（承认恒等）与「保住立论」互斥，R4（给 c 角色）"
         "必须新增一条本体系没有的动力学 ⇒ 两条不可同时满足于原稿范围内，"
         "故严格档 0。最小代价组合（严格档）= %s。"
         % (min_cost_strict if min_cost_strict is not None else "不存在"),
    loose=loose_pass, strict=strict_pass, zero_cost=zero_cost_pass)

# ============================================================
# 19. 守卫（全部真算）
# ============================================================
guard("G1 秩审计：rank(三式)=2 且 式③ ≡ 式②−式①（含常数项）",
      RANK_TRIPLE == 2 and EQ3_EQ_EQ2_MINUS_EQ1,
      "rank=%d eq3==eq2-eq1=%s" % (RANK_TRIPLE, EQ3_EQ_EQ2_MINUS_EQ1))
guard("G2 衔接式 ≡ −式②（重排）",
      LINK_EQ_NEG_EQ2 and RANK_WITH_LINK == RANK_TRIPLE,
      "link==-eq2=%s rank_with_link=%d" % (LINK_EQ_NEG_EQ2, RANK_WITH_LINK))
guard("G3 c→λ 重标定后残差机器零（%d 个 λ）" % len(LAMBDAS), SUB_ALL_ZERO,
      "max=%s" % fs(SUB_MAX_RES, 3))
guard("G4 c→λ 负对照残差显著非零且与解析式吻合", SUB_CTL_NONZERO and SUB_CTL_ALL_MATCH,
      "max=%s match=%s" % (fs(SUB_MAX_CTL, 6), SUB_CTL_ALL_MATCH))
guard("G5 天体量级表非空且最大偏离 > 1e5", len(BODY_ROWS) == 4 and BODY_MAX_DEV > 1e5,
      "max_ratio=%s" % fs(BODY_MAX_DEV, 6))
guard("G6 m_p 双口径两处语境各自命中", MP_DUAL,
      "planck=%d proton=%d" % (N_PLANCK_CTX, N_PROTON_CTX))
guard("G7 Z 单位双口径两处各自命中", Z_UNIT_DUAL,
      "si=%d sm=%d" % (N_Z_SI, N_Z_SM))
guard("G8 量纲计算器自检 4/4 且全式量纲闭合",
      DIM_SELF_OK and D_EQ2_OK and D_EQ3_OK and D_LINK_OK and D_QG_OK and D_FZ_OK,
      "self=%s eq2=%s eq3=%s link=%s qg=%s fz=%s"
      % (DIM_SELF_OK, D_EQ2_OK, D_EQ3_OK, D_LINK_OK, D_QG_OK, D_FZ_OK))
guard("G9 控制组 10/10 全绿（防声明性假绿）",
      all(c["ok"] for c in CONTROLS),
      "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
GROUP_EXPECT = {"A": 3, "B": 3, "C": 3, "D": 3, "E": 6, "F": 2, "G": 5, "H": 1}
N_BY_GROUP = {}
for _it in ITEMS:
    _p = _it["id"][0]
    N_BY_GROUP[_p] = N_BY_GROUP.get(_p, 0) + 1
ITEMS_STRUCT_OK = (N_BY_GROUP == GROUP_EXPECT) and \
    (len(ITEMS) == sum(GROUP_EXPECT.values()))
guard("G10 条目结构：%s（合计 %d）"
      % (" ".join("%s=%d" % (k, N_BY_GROUP.get(k, 0))
                  for k in sorted(GROUP_EXPECT)), len(ITEMS)),
      ITEMS_STRUCT_OK, "got=%s" % N_BY_GROUP)

guard("G13 三重闭环三条推导路径全部 Fraction 精确成立", ALL_PATHS_OK,
      "12to3=%s 13to2=%s 23to1=%s"
      % (PATH_12_to_3, PATH_13_to_2, PATH_23_to_1))

guard("G14 本源式 Z=Gc/2 的向量确为 −式①（A03 未写死）", ZGC2_IS_NEG_EQ1,
      "v_zgc2=%s" % V_ZGC2)

guard("G15 扫描命中按文件去重后仍双口径并存（非单文件重复计数）",
      MP_DUAL and Z_UNIT_DUAL,
      "planck_files=%d proton_files=%d / si_files=%d sm_files=%d"
      % (F_PLANCK_CTX, F_PROTON_CTX, F_Z_SI, F_Z_SM))
guard("G11 Z 宣称值偏差 > G 不确定度 5 倍（非舍入）",
      Z_DEV_OVER_UNC > 5, "dev/unc=%s" % fs(Z_DEV_OVER_UNC, 3))
guard("G12 PASS 条目中含真计算（D03/G04 的 m_P 重算命中 1e−6）",
      abs(M_PLANCK_REL) < Decimal("1e-6"), "rel=%s" % fs(M_PLANCK_REL, 3))


def summarize():
    cnt = {}
    for it in ITEMS:
        cnt[it["status"]] = cnt.get(it["status"], 0) + 1
    return cnt


class Tee(object):
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            try:
                st.write(s)
            except Exception:
                pass
        return len(s)

    def flush(self):
        for st in self.streams:
            try:
                st.flush()
            except Exception:
                pass


def main():
    t0 = T_START
    cnt = summarize()
    _rp = os.path.join(OUT, STEM + "_report.txt")
    _orig = sys.stdout
    _rf = None
    try:
        os.makedirs(OUT, exist_ok=True)
        _rf = io.open(_rp, "w", encoding="utf-8")
        sys.stdout = Tee(_orig, _rf)
    except Exception:
        _rf = None

    print("=" * 78)
    print("TUFT-r177｜S17-3.19 引力光速统一方程（G-c 全公式汇总）"
          "—— 闭环秩 / c 可替换性 / 常数口径")
    print("=" * 78)
    print("靶文: %s" % os.path.relpath(TARGET, BASE).replace("\\", "/"))
    print("读取: %s  行数=%d" % ("OK" if READ_OK else "FAIL", N_LINES))
    print("形态命中: %s" % ", ".join("%s=%d" % (k, v) for k, v in HIT.items()))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %s  %s" % (it["status"], it["id"], it["title"]))
        if it["note"]:
            print("       · %s" % it["note"])
        if it["metrics"]:
            kv = ", ".join("%s=%s" % (k, v)
                           for k, v in sorted(it["metrics"].items()))
            print("       · %s" % kv)
    print("-" * 78)
    print("精确秩（Fraction 高斯消元，变量 logG/logZ/logr/logm + 常数基 log2/logc）:")
    print("  式① G=2Z/c      向量 %s" % V_EQ1)
    print("  式② G=c^2 r/m   向量 %s" % V_EQ2)
    print("  式③ Z=c^3r/(2m) 向量 %s" % V_EQ3)
    print("  衔接 r=Gm/c^2   向量 %s" % V_LINK)
    print("  rank(①,②,③)=%d   rank(①,②,③,衔接)=%d"
          % (RANK_TRIPLE, RANK_WITH_LINK))
    print("  式③ == 式②−式① : %s ； 衔接 == −式② : %s"
          % (EQ3_EQ_EQ2_MINUS_EQ1, LINK_EQ_NEG_EQ2))
    print("-" * 78)
    print("c 替换测试（c → λ）:")
    for r in SUB_ROWS:
        print("  λ=%-10s 重标定后残差=%-12s | Z 固定时残差=%-12s 期望|c/λ−1|=%-12s %s"
              % (r["lambda"], r["residual_recalibrated"], r["residual_Z_fixed"],
                 r["expect_c_over_lambda_minus_1"],
                 "OK" if r["ctl_match"] else "NG"))
    print("-" * 78)
    print("式② G = c²r/m 对真实天体（实际半径）:")
    for r in BODY_ROWS:
        print("  %-16s c²r/m=%-12s vs G=%-12s => %s 倍 ; r/m 与要求值比 = %s"
              % (r["body"], r["c2r_over_m"], r["G_true"], r["ratio_to_G"],
                 r["r_over_m_over_required"]))
    print("  要求 r/m = G/c² = %s m/kg（恒定）" % fs(RM_REQUIRED, 6))
    print("恒等分支（r = Gm/c² 代回）:")
    for r in IDENT_ROWS:
        print("  %-6s r_half=%-14s c²r/m=%-12s 残差=%s"
              % (r["body"], r["r_half_schwarzschild_m"], r["c2r_over_m"],
                 r["rel_residual"]))
    print("-" * 78)
    print("常数口径:")
    print("  Z 精算 Gc/2 = %s  ; 靶宣称 %s  ; 相对差 %s (= %s × G 不确定度)"
          % (fs(Z_EXACT, 10), fs(Z_CLAIM, 6), fs(Z_REL_DEV, 4),
             fs(Z_DEV_OVER_UNC, 3)))
    print("  m_P = √(ħc/G) 重算 = %s kg ; 靶公布 = %s kg ; 相对差 %s"
          % (fs(M_PLANCK_CALC, 12), fs(M_PLANCK_LIT, 12), fs(M_PLANCK_REL, 3)))
    print("  m_p 双口径比 = %s  ; 按质子质量读 G = %s（%s 倍于真值）"
          % (fs(MP_RATIO, 6), fs(G_FROM_PROTON, 6), fs(G_PROTON_DEV, 6)))
    print("  扫描（%d 个 .md）：m_p/普朗克 %d 处(%d 文件)，m_p/质子 %d 处(%d 文件)，"
          "Z 单位 SI %d 处(%d 文件) / s·m⁻¹ %d 处(%d 文件)，Z 宣称值 %d 处(%d 文件)"
          % (SCAN["files"], N_PLANCK_CTX, F_PLANCK_CTX, N_PROTON_CTX,
             F_PROTON_CTX, N_Z_SI, F_Z_SI, N_Z_SM, F_Z_SM, N_Z_CLAIM,
             F_Z_CLAIM))
    print("  抽样：普朗克口径「%s」" % (
        SCAN["planck_ctx"][0]["text"][:70] if SCAN["planck_ctx"] else "—"))
    print("        质子口径「%s」" % (
        SCAN["proton_ctx"][0]["text"][:70] if SCAN["proton_ctx"] else "—"))
    print("        s/m 口径「%s」" % (
        SCAN["z_unit_sm"][0]["text"][:70] if SCAN["z_unit_sm"] else "—"))
    print("  量纲：[Z]_def=%s  [Z]_s/m=%s  差 %s  ; [Z]_{G=1}=%s 差 %s"
          % (dfmt(D_Z_DEF), dfmt(D_Z_SM), dfmt(ddiv(D_Z_DEF, D_Z_SM)),
             dfmt(D_Z_G1), dfmt(ddiv(D_Z_G1, D_Z_SM))))
    print("-" * 78)
    print("修复定价（7 维 × 128 组合）:")
    for r in REPAIR_ROWS:
        print("  %-34s %s / %s" % (r["档位"], r["通过组合"], r["总组合"]))
    print("-" * 78)
    for c in CONTROLS:
        print("  [ctl%s] %-46s 值=%-18s 期望=%-12s"
              % ("OK" if c["ok"] else "NG", c["desc"][:46], c["value"],
                 c["expect"]))
    for g in GUARDS:
        print("  [grd%s] %-52s %s"
              % ("OK" if g["ok"] else "NG", g["name"][:52], g["detail"]))
    n_guard_ok = sum(1 for g in GUARDS if g["ok"])
    n_ctl_ok = sum(1 for c in CONTROLS if c["ok"])
    print("-" * 78)
    print("条目 %d：%s" % (len(ITEMS),
                          "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt))))
    print("控制 %d/%d   守卫 %d/%d   用时 %.2fs"
          % (n_ctl_ok, len(CONTROLS), n_guard_ok, len(GUARDS), time.time() - t0))

    payload = {
        "stem": STEM,
        "round": "r177",
        "target": os.path.relpath(TARGET, BASE).replace("\\", "/"),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "text_scan": {"lines": N_LINES, "forms": HIT,
                      "wrong_form_flag": N_WRONG_FLAG,
                      "dynamics_tokens": N_DYNA},
        "verdict": {
            "core": "「G-c 三重核心闭环」只有 2 个独立约束（式③ ≡ 式②−式①，"
                    "衔接式 ≡ −式②），式② 与衔接式互相定义故零预言；"
                    "c 可被任意 λ 替代而闭环不变，故不承担「光速」专属角色；"
                    "同一体系内 m_p 有两个相差 1.30e19 倍的值、Z 有两种不可通约"
                    "的单位、Z 的宣称值与其自称输入算术不自洽。",
            "defects": [
                "三重闭环秩 2（第三式为推论，非独立约束）",
                "衔接式 r=Gm/c² 是核心式②的代数重排",
                "G=2Z/c 与牛顿万有引力定律恒等（符号替换）",
                "c 可替换为任意 λ ⇒ 无光速专属内容",
                "m_p 双口径（普朗克 2.176e−8 / 质子 1.673e−27，差 1.30e19）",
                "Z 单位双口径（m⁴kg⁻¹s⁻³ vs s/m，差 L⁵M⁻¹T⁻⁴）",
                "Z 宣称值 1.00065e−2 与 Gc/2 精算 1.00045e−2 差 1.97e−4"
                "（≈9×G 不确定度）",
            ],
            "favourable": [
                "全式量纲无一出错（(M,L,T,Q) 精确审计）",
                "r=Gm/c² 确为史瓦西半径 1/2（自注正确）",
                "主动标注 Z=G/(2c) 为错误形式（自我纠错方向正确）",
                "§四 与标准普朗克单位完全一致（相对差 <1e−6）",
            ],
        },
        "rank_audit": {
            "vars": ["logG", "logZ", "logr", "logm"],
            "const_basis": ["log2", "logc"],
            "v_eq1": V_EQ1, "v_eq2": V_EQ2, "v_eq3": V_EQ3, "v_link": V_LINK,
            "rank_triple": RANK_TRIPLE, "rank_with_link": RANK_WITH_LINK,
            "eq3_is_eq2_minus_eq1": EQ3_EQ_EQ2_MINUS_EQ1,
            "link_is_neg_eq2": LINK_EQ_NEG_EQ2,
            "v_zgc2": V_ZGC2, "zgc2_is_neg_eq1": ZGC2_IS_NEG_EQ1,
            "paths": {"12_to_3": PATH_12_to_3, "13_to_2": PATH_13_to_2,
                      "23_to_1": PATH_23_to_1},
            "rank_pos_control": RANK_POS_CTL, "rank_neg_control": RANK_NEG_CTL,
        },
        "c_replaceability": SUB_ROWS,
        "bodies": BODY_ROWS,
        "tautology_branch": IDENT_ROWS,
        "constants": {
            "G": str(G), "c": str(C), "hbar": str(HBAR),
            "Z_exact_Gc_over_2": str(Z_EXACT), "Z_claim": str(Z_CLAIM),
            "Z_rel_dev": str(Z_REL_DEV), "Z_dev_over_G_uncertainty":
                str(Z_DEV_OVER_UNC),
            "m_planck_calc": str(M_PLANCK_CALC),
            "m_planck_lit": str(M_PLANCK_LIT),
            "m_proton_lit": str(M_PROTON_LIT),
            "m_p_ratio": str(MP_RATIO),
            "G_from_proton_reading": str(G_FROM_PROTON),
            "G_proton_reading_dev": str(G_PROTON_DEV),
            "r_schwarzschild_sun_m": str(R_SCH_SUN),
            "required_r_over_m": str(RM_REQUIRED),
        },
        "dimensions": {
            "Z_from_Gc_over_2": dfmt(D_Z_DEF),
            "Z_from_s_over_m": dfmt(D_Z_SM),
            "gap": dfmt(ddiv(D_Z_DEF, D_Z_SM)),
            "Z_under_G_equals_1": dfmt(D_Z_G1),
            "gap_G1_vs_sm": dfmt(ddiv(D_Z_G1, D_Z_SM)),
            "Z_wrong_form_G_over_2c": dfmt(D_Z_WRONG),
            "gap_two_Z_forms": dfmt(ddiv(D_Z_DEF, D_Z_WRONG)),
            "all_equations_closed": bool(D_EQ2_OK and D_EQ3_OK and D_LINK_OK
                                         and D_QG_OK and D_FZ_OK),
        },
        "scan": {"files_scanned": SCAN["files"],
                 "m_p_planck_ctx": SCAN["planck_ctx"][:12],
                 "m_p_proton_ctx": SCAN["proton_ctx"][:12],
                 "z_unit_si": SCAN["z_unit_si"][:12],
                 "z_unit_sm": SCAN["z_unit_sm"][:12],
                 "z_claim_hits": SCAN["z_claim"][:12],
                 "counts": {"planck": N_PLANCK_CTX, "proton": N_PROTON_CTX,
                            "z_si": N_Z_SI, "z_sm": N_Z_SM,
                            "z_claim": N_Z_CLAIM},
                 "file_counts": {"planck": F_PLANCK_CTX, "proton": F_PROTON_CTX,
                                 "z_si": F_Z_SI, "z_sm": F_Z_SM,
                                 "z_claim": F_Z_CLAIM}},
        "repair_pricing": {"fixes": [{"name": f[0], "cost": f[2],
                                      "fixes": f[1]} for f in FIXES],
                           "rows": REPAIR_ROWS,
                           "min_cost_strict": min_cost_strict},
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "counts": cnt,
        "guard_ok": "%d/%d" % (n_guard_ok, len(GUARDS)),
        "control_ok": "%d/%d" % (n_ctl_ok, len(CONTROLS)),
    }
    try:
        os.makedirs(OUT, exist_ok=True)
        jp = os.path.join(OUT, STEM + ".json")
        with io.open(jp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
        print("JSON  -> %s" % jp)

        mp = os.path.join(OUT, STEM + ".md")
        L = []
        L.append("# TUFT-r177 精算摘要")
        L.append("")
        L.append("- 靶：`%s`" % payload["target"])
        L.append("- 条目：%s" % "  ".join("%s=%d" % (k, cnt[k])
                                          for k in sorted(cnt)))
        L.append("- 控制：%d/%d　守卫：%d/%d"
                 % (n_ctl_ok, len(CONTROLS), n_guard_ok, len(GUARDS)))
        L.append("")
        L.append("| 编号 | 状态 | 判定 |")
        L.append("|---|---|---|")
        for it in ITEMS:
            L.append("| %s | %s | %s |"
                     % (it["id"], it["status"],
                        it["title"].replace("|", "\\|")))
        L.append("")
        L.append("## 式② G = c²r/m 对真实天体")
        L.append("")
        L.append("| 天体 | c²r/m | 真值 G | 倍数 | (r/m) / (G/c²) |")
        L.append("|---|---|---|---|---|")
        for r in BODY_ROWS:
            L.append("| %s | %s | %s | %s | %s |"
                     % (r["body"], r["c2r_over_m"], r["G_true"],
                        r["ratio_to_G"], r["r_over_m_over_required"]))
        L.append("")
        L.append("## c 替换测试")
        L.append("")
        L.append("| λ | 重标定后残差 | Z 固定时残差 | 期望 \\|c/λ−1\\| |")
        L.append("|---|---|---|---|")
        for r in SUB_ROWS:
            L.append("| %s | %s | %s | %s |"
                     % (r["lambda"], r["residual_recalibrated"],
                        r["residual_Z_fixed"],
                        r["expect_c_over_lambda_minus_1"]))
        L.append("")
        L.append("## 修复定价")
        L.append("")
        L.append("| 档位 | 通过组合 / 总组合 |")
        L.append("|---|---|")
        for r in REPAIR_ROWS:
            L.append("| %s | %s / %s |" % (r["档位"], r["通过组合"],
                                           r["总组合"]))
        L.append("")
        with io.open(mp, "w", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")
        print("MD    -> %s" % mp)
    except Exception as exc:
        print("[warn] 落盘失败: %s" % exc)

    try:
        sys.stdout = _orig
        if _rf is not None:
            _rf.close()
            print("REPORT-> %s" % _rp)
    except Exception:
        pass

    return 0 if n_guard_ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
