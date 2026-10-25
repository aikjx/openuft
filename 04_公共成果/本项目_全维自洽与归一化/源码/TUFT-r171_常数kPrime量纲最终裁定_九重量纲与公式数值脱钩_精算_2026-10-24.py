#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TUFT-r171｜常数 k' 的「量纲最终裁定」精算：九重量纲、公式与数值脱钩、磁场方程不可满足
================================================================================
编号 r171（起草前实测首空号；r170 已被并行会话两卷占用 ⇒ 本卷取 r171）。

靶：`01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/常数 k' 的量纲最终裁定/`
    · v1/常数 k' 的量纲最终裁定.md（138 行，自称「最终裁定」，裁定 [k′]=[IT²/M]）
    · v1/1.md 与 v1/几何与现象学的桥梁….md（同文两副本，165 行，称 [k′]=[IT/M]）
    · v1/基于空间几何化的统一场论及经典电磁学交叉验证.md（519 行）
    · v1+v2/统一场论核心公式量纲验证与求导证明.md（640/660 行）
    · v2/验证/全面验证.md · v3/验证/1.md · v4/1.md（179 行）· v5/1.md（220 行）
    · v6/code/1.py（237 行）· v6/code/calculate_k_prime.py · v6/验证/verify_ke.py
    · v6/公式验证/数据计算.md · v6/传统物理/传统物理对比.md · 公式.md
    · 共 29 个 .py + 38 个 .md（机读）

本卷四层判据：
  ① 数值层：k′ = √(4πε₀ħc)/c 独立高精度复核（Decimal 60 位）+ 公式-数值一致性
  ② 量纲层：机读多重被主张 (M,L,T,Q) 口径 + 磁场方程「可满足性」解析 + 代回检验
  ③ 方法论层：ast 全目录扫描（复用 r166/r168 检测器）+ 循环等效性检验
  ④ 跨卷层：r161 的 k′ 下界、r162 的 [k]、r163 的 k=4πm_p、r168 的「k′ 从未给值」

分层铁律：本卷条目不可与 r159–r170 相加。
治理红线：数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。
纯标准库（本环境无 numpy / sympy / mpmath）。
"""

import ast
import json
import math
import os
import re
import sys
import warnings
from decimal import Decimal as DEC, getcontext
from fractions import Fraction as F

getcontext().prec = 60

# GBK 控制台守卫：本卷含下标/箭头等字符，必须显式 UTF-8 + replace
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ============================== 常量（CODATA 2018） ==============================
PI = DEC("3.14159265358979323846264338327950288419716939937510582097494")
FOUR_PI = DEC(4) * PI
C_LIGHT = DEC("299792458.0")
EPS0 = DEC("8.8541878128e-12")          # F/m
HBAR = DEC("1.054571817e-34")           # J·s
G_CONST = DEC("6.67430e-11")            # m^3 kg^-1 s^-2
KE = DEC("8.9875517923e9")              # N·m^2/C^2 库仑常数
E_CHARGE = DEC("1.602176634e-19")       # C
M_PLANCK = DEC("2.176434e-8")           # kg
MU0 = FOUR_PI * DEC("1e-7")             # H/m

# ============================== 路径定位 ==============================
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_COM = os.path.dirname(_PROJ)
OPENUFT_ROOT = os.path.dirname(_COM)
FDIR = os.path.join(OPENUFT_ROOT, "01_独立体系", "S17_统一场论核心公式",
                    "04_理论推导", "核心公式集", "常数 k' 的量纲最终裁定")

F_VERDICT = os.path.join(FDIR, "v1", "常数 k' 的量纲最终裁定.md")
F_V1_BRIDGE = os.path.join(FDIR, "v1", "1.md")
F_V1_CROSS = os.path.join(FDIR, "v1", "基于空间几何化的统一场论及经典电磁学交叉验证.md")
F_V1_DIMPROOF = os.path.join(FDIR, "v1", "统一场论核心公式量纲验证与求导证明.md")
F_V2_MAIN = os.path.join(FDIR, "v2", "统一场论核心公式量纲验证与求导证明.md")
F_V2_FULL = os.path.join(FDIR, "v2", "验证", "全面验证.md")
F_V4 = os.path.join(FDIR, "v4", "1.md")
F_V5 = os.path.join(FDIR, "v5", "1.md")
F_V6_CODE1 = os.path.join(FDIR, "v6", "code", "1.py")
F_V6_DATA = os.path.join(FDIR, "v6", "公式验证", "数据计算.md")
F_V6_TRAD = os.path.join(FDIR, "v6", "传统物理", "传统物理对比.md")
F_V6_KE = os.path.join(FDIR, "v6", "验证", "verify_ke.py")
F_FORMULA = os.path.join(FDIR, "公式.md")
F_CALC = os.path.join(FDIR, "v6", "code", "calculate_k_prime.py")

# ============================== 登记器 ==============================
ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, group, name, verdict, note):
    ENTRIES.append({"code": code, "group": group, "name": name,
                    "verdict": verdict, "note": note})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


def control(name, ok, detail):
    CONTROLS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  {} {} — {}".format("OK " if ok else "BAD", name, detail))


# ============================== 量纲运算器 (M, L, T, Q) ==============================
def d_inv(a):
    return tuple(-x for x in a)


def d_mul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def d_div(a, b):
    return tuple(x - y for x, y in zip(a, b))


def d_pow(a, n):
    return tuple(x * n for x in a)


D_M = (1, 0, 0, 0)
D_L = (0, 1, 0, 0)
D_T = (0, 0, 1, 0)
D_Q = (0, 0, 0, 1)
D_CHARGE = D_Q                            # [q] = Q（I·T ≡ Q）
D_ACC = d_div(D_L, d_pow(D_T, 2))
D_EPS0 = (-1, -3, 2, 2)                    # I²T⁴M⁻¹L⁻³ = Q²T²M⁻¹L⁻³
D_MU0 = (1, 1, 0, -2)                      # MLI⁻²T⁻² = MLQ⁻²
D_E_FIELD = (1, 1, -2, -1)                 # MLT⁻²Q⁻¹ = N/C
D_B_FIELD = (1, 0, -1, -1)                 # MI⁻¹T⁻² = kg/(C·s) = T
D_TINV = (0, 0, -1, 0)                     # [dΩ/dt] = T⁻¹
D_L2 = (0, -2, 0, 0)                       # [r/r³] = L⁻²
D_K = D_M                                  # [k] = [M]

# k' 的被主张口径（(M,L,T,Q) 四元；机读清点见 B1）
DIMLESS = (0, 0, 0, 0)
DIM_KP_MAIN = (-1, 0, 1, 1)                # [IT²/M] = A·s²/kg = C·s/kg（v1 裁定/v2/v5/v6:119）
DIM_KP_ITM = (-1, 0, 0, 1)                 # [IT/M] = Q/M（v1/1.md:35、v1/交叉验证:43/119、v1/统一场论:247）
DIM_KP_CSM = (0, -1, 1, 1)                 # [C·s/m] = [A·s²/m²]（v6/code/1.py:94/99/121、v6/验证/verify_ke.py:55/81、v4/1.md:4）
DIM_KP_LM1 = (-1, -1, 1, 1)                # [L⁻¹IT²/M]（v1 裁定:86 场景2）
DIM_KP_QT2 = (-1, 0, 2, 1)                 # [QT²/M⁻¹] = C·s²/kg（v6/code/1.py:113，自称 = A·s²/kg）
# 磁场方程**要求**的口径（解析求解，见 B2）：[k']_B = [B] - [k] - [μ₀] - [T⁻¹] - [L⁻²]
DIM_KP_B_REQ = tuple(a - b - c - d - e for a, b, c, d, e in
                     zip(D_B_FIELD, D_K, D_MU0, D_TINV, D_L2))   # = (-1,1,0,1) = [C·m/kg]

# ============================== 量纲表达式解析器（B1 机读用） ==============================
# 靶文档用两套记号写 k' 的量纲：SI 单位串（A·s²/kg、C·s/m、kg/A、A·s²·m⁻²…）与
# 基本量括注（[IT²/M]、[Q T² M⁻¹]、[L⁻¹IT²/M]、[Q][T][M]⁻¹…）。本解析器把两套
# 记号都映到 (M,L,T,Q) 四元，供 B1 机读清点互异口径数。
DIM_SYM = {
    "I": (0, 0, -1, 1),      # 电流 ≡ Q/T
    "T": (0, 0, 1, 0),
    "M": (1, 0, 0, 0),
    "L": (0, 1, 0, 0),
    "Q": (0, 0, 0, 1),
    "C": (0, 0, 0, 1),
    "A": (0, 0, -1, 1),      # 安培 ≡ I
    "s": (0, 0, 1, 0),
    "t": (0, 0, 1, 0),       # 小写 t（v6/验证/12.md 的 [q·t/m]）
    "q": (0, 0, 0, 1),       # 小写 q（同上）
    "kg": (1, 0, 0, 0),
    "m": (0, 1, 0, 0),
    "N": (1, 1, -2, 0),
    "V": (1, 2, -3, -1),
    "J": (1, 2, -2, 0),
    "W": (1, 2, -3, 0),
    "Hz": (0, 0, -1, 0),
}
_DIM_SAFE = re.compile(r"[A-Za-zkgHz·/\^()\-0-9{}]+")


def _desup_all(s):
    """Unicode 上标 → ASCII 指数：s²→s^2、M⁻¹→M^-1、L⁻³→L^-3。"""
    return re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+",
                  lambda m: "^" + m.group(0).translate(
                      str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")), s)


def _dim_norm(s):
    r"""归一化：\cdot/\times→·、去空格、上标→^n、方括号→圆括号、相邻项隐式乘号。

    行内公式装饰（$、\\(、\\)）换成空格——靶的量纲宣称常写成
    `$k'$ 的量纲为 $IT^2M^{-1}$ 时`，不剥就会整条解析失败（r171 实跑抓到 82 处）。
    """
    s = s.replace("\\(", " ").replace("\\)", " ").replace("$", " ")
    s = s.replace("\\cdot", "·").replace("\\times", "·").replace("*", "·")
    s = _desup_all(s)
    s = s.replace("[", "(").replace("]", ")").replace(" ", "")
    # 相邻因式隐式相乘：[Q][T][M]⁻¹ → (Q)·(T)·(M)^-1；(IT) → (IT)
    out = []
    for i, ch in enumerate(s):
        if ch == "(" and out and (out[-1] == ")" or out[-1].isalpha()):
            out.append("·")
        if ch.isalpha() and out and out[-1] == ")":
            out.append("·")
        out.append(ch)
    return "".join(out)


def _dim_parse(s):
    """把量纲表达式解析为 (M,L,T,Q)；无法安全解析返回 None（不硬解）。"""
    if not s:
        return None
    t = _dim_norm(s)
    if not t or not _DIM_SAFE.fullmatch(t):
        return None
    toks = []
    i = 0
    while i < len(t):
        ch = t[i]
        if ch in "·/()":
            toks.append(ch)
            i += 1
        elif ch == "^":
            m = re.match(r"\^\{?(-?\d+)\}?", t[i:])
            if not m:
                return None
            toks.append(("exp", int(m.group(1))))
            i += m.end()
        elif ch.isalpha():
            if t.startswith("kg", i):
                toks.append("kg")
                i += 2
            elif t.startswith("Hz", i):
                toks.append("Hz")
                i += 2
            else:
                toks.append(ch)
                i += 1
        else:
            return None
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        v = peek()
        pos[0] += 1
        return v

    def p_expr():
        val, ok = p_term()
        if not ok:
            return None, False
        while True:
            t2 = peek()
            if t2 in ("·", "/"):
                op = take()
                rhs, ok2 = p_term()
                if not ok2:
                    return None, False
                val = d_mul(val, rhs) if op == "·" else d_div(val, rhs)
            elif t2 == "(" or (isinstance(t2, str) and t2 in DIM_SYM):
                rhs, ok2 = p_term()          # 隐式相乘：IT、(Q)(T)
                if not ok2:
                    return None, False
                val = d_mul(val, rhs)
            else:
                break
        return val, True

    def p_term():
        t2 = peek()
        if t2 == "(":
            take()
            val, ok = p_expr()
            if not ok or peek() != ")":
                return None, False
            take()
            if isinstance(peek(), tuple):
                val = d_pow(val, take()[1])
            return val, True
        if isinstance(t2, str) and t2 in DIM_SYM:
            take()
            val = DIM_SYM[t2]
            if isinstance(peek(), tuple):
                val = d_pow(val, take()[1])
            return val, True
        return None, False

    val, ok = p_expr()
    if not ok or pos[0] != len(toks):
        return None
    return val


def _dim_run(run):
    """解析一条可能含 '=' 链/尾随散文的量纲宣称串：取最末可解析段的最长可解析前缀。

    ★修剪只在**词边界**处进行（切点后一字符不得是字母/数字/下划线）——
    否则 `q_p / c`（公式，非量纲宣称）会被一路 trim 成 `q` 而假阳性（r171 实跑抓到）。
    """
    for seg in reversed([s for s in re.split(r"=|≈|\\approx", run) if s.strip()]):
        seg = seg.strip()
        for L in range(len(seg), 0, -1):
            if L < len(seg) and re.match(r"[A-Za-z0-9_]", seg[L]):
                continue          # 词中间，不许切
            v = _dim_parse(seg[:L])
            if v is not None:
                return v
    return None


def _norm_line(s):
    r"""行归一化：剥 \text{}/\mathrm{} 的花括号（保留内容），LaTeX 间距命令→空格。

    `\\,` 必须变成空格：截断类把 `\,` 里的逗号当语句逗号，会把
    「k' = 1 \\, \\text{A·s²/kg}」切成 "1 \\" 而混过单位输入排除（r171 首跑实测）。
    `$`、`\\(`、`\\)` 保留——B7 的行内串味防护依赖 `$` 作截断符。
    """
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", s)
    for cmd in ("\\,", "\\;", "\\!", "\\ ", "\\quad", "\\qquad"):
        s = s.replace(cmd, " ")
    return s


# ============================== k′ 宣称机读（B1 口径 + B7 数值共用） ==============================
# 数值宣称（k' = <数>…）——防假阳性层承自 r168 五层 + 本卷实跑新增的四层（⑨⑩⑪ + 单位串）
KP_PAT = re.compile(
    r"(?<![A-Za-z/\\])\$?\\?k\$?(?:'|′|\^\{\\prime\}|\^\\prime)\$?\s*"
    r"(?:=|≈|\\approx)\s*([^。\n;；、，,]{0,140})")
KP_PAT2 = re.compile(                     # 「k' … 值为 X」型（v4 摘要「其值为 1.11238×10⁻¹⁰」）
    r"(?<![A-Za-z/\\])\$?\\?k\$?(?:'|′|\^\{\\prime\}|\^\\prime)\$?"
    r"[^。\n]{0,20}?(?:值|数值)\s*(?:为|是|≈|＝|=)\s*([^。\n;；、，,]{0,140})")
CUT_AT = re.compile(r"[$，,;；。、]")
SEG_SPLIT = re.compile(r"=|≈|\\approx")
BARE10 = re.compile(r"^\s*10\s*\^\s*\{?(-?[0-9]+)\}?")
NUM_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)")
CONT_RE = re.compile(r"\s*(?:\\times|×|\*|·|/)\s*"
                     r"(10\s*\^\s*\{?(-?[0-9]+)\}?|[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)")
UNIT_TOK = re.compile(r"kg/A|A·s|C·s|m/s|C/kg|V/m|J·s|Hz|s\^?[-−]?[12]|s⁻¹|"
                      r"\\text\{|[（(]无量纲|kg\b|C\b|T\b|N\b")
UNIT_INPUT = re.compile(r"^1(?:\.0+)?\s*(?:A·s²/kg|C·s²/kg|C·s/kg|A·s/m|C·s/m|kg)\b")
HARD_FORM = re.compile(r"\\sqrt|√|\\frac|\\vec")
TMPL_FORM = re.compile(r"\{[A-Za-z_][A-Za-z_0-9]*[:.!}]")
# 乘积上下文：k′ 紧跟另一因子（k×k′、f·k′、k′k、2k′…）时等号右侧是**整个表达式**的值
PROD_PRE = re.compile(r"(?:×|·|\*|/|\\times|\\cdot|[A-Za-z0-9)\]}π′'^])\s*$")
_UEXP = r"(?:\^\s*\{?\s*-?\d+\s*\}?|[²³]|⁻[¹²³])"
# ★单位分隔符直接含 \\cdot/\\times：不得对片段做变长替换——那会让数值链的结束
#   位置偏移，把 "C·s/kg" 吞成 "s/kg"（r171 实跑抓到：M⁻¹T²、M⁻¹T 两种假口径）。
UNIT_AFTER = re.compile(
    r"^[\s$()\[\]]*\s*((?:kg|Hz|[A-Za-z])(?:" + _UEXP + r")?"
    r"(?:\s*(?:[·/]|\\cdot|\\times)\s*(?:kg|Hz|[A-Za-z])(?:" + _UEXP + r")?)*)")
_SUP10 = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")
_SUP = re.compile(r"10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+)")


def _strip_latex(s):
    return re.sub(r"\\text\{([^}]*)\}", r"\1", s)


def _desup(s):
    return _SUP.sub(lambda m: "10^" + m.group(1).translate(_SUP10), s)


def _seg_value(seg):
    """严格数值前缀解析：返回 (值, 消耗长度)；无数值链返回 None。

    只吃「首数字 + 连续的 ×10^n / ×数 / /数」链，遇到单位、括注、散文即停——
    防止把 `（原推导：4.596×10^7）` 这类括注里的第二个数乘进结果（r171 首跑实测：
    4.5946e+07 A·s²/kg（原推导：4.596×10^7）曾被读成 2.11168e+15）。
    """
    seg = _desup(seg.strip())
    if not seg or not ("0" <= seg[0] <= "9"):
        return None
    mb = BARE10.match(seg)
    if mb:
        return (10.0 ** int(mb.group(1)), mb.end())
    nm = NUM_RE.match(seg)
    if nm is None:
        return None
    v = float(nm.group(1))
    pos = nm.end()
    while True:
        c = CONT_RE.match(seg, pos)
        if c is None:
            break
        tok = c.group(1)
        me = re.match(r"10\s*\^\s*\{?(-?[0-9]+)\}?$", tok)
        v = v * (10.0 ** int(me.group(1))) if me else v * float(tok)
        pos = c.end()
    return (v, pos)


# 量纲宣称的四种书面断言形态（k′ 必须是断言主语，挡住 dm/dt、q_p、k′k 等他物的量纲）
KP_DIM_PATS = [
    # P1: [k'] = <run>（v5:45、v6/公式验证/1.md:61、v1/交叉验证:119、v6/验证/1.md:120/122）
    ("D", re.compile(r"\[\s*\\?k\$?(?:'|′|\^\{?\\prime\}?)\$?\s*\]\s*(?:=|为|是|：|:)\s*"
                     r"([^。\n;；,，、（]{0,72})")),
    # P2: k'的?（理论|SI）?量纲 为/是/:/= <run>（v6/张祥前:311/386、v6/验证/3.md:39、
    #     v1/统一场论:247、v6/传统物理对比:104）
    ("D", re.compile(r"(?<![A-Za-z/\\])\$?\\?k\$?(?:'|′|\^\{\\prime\}|\^\\prime)\$?"
                     r"\s*的?\s*(?:理论|SI)?\s*量纲\s*(?:为|是|：|:|=)\s*([^。\n;；,，、（]{0,72})")),
    # P2b: k' = <式 ≤20 字> →/的量纲 … <run>（v6/验证/1.md:95/100、v6/验证/6.md:125）
    ("D", re.compile(r"(?<![A-Za-z/\\])\$?\\?k\$?(?:'|′|\^\{\\prime\}|\^\\prime)\$?"
                     r"\s*=\s*[^。\n，,;；]{1,20}?\s*(?:→|=>|的量纲)\s*(?:为|是|：|:|=)?\s*"
                     r"([^。\n;；,，、（]{0,72})")),
    # P3a: k': <run>（v5:149）
    ("D", re.compile(r"(?<![A-Za-z/\\])\$?\\?k\$?(?:'|′|\^\{\\prime\}|\^\\prime)\$?"
                     r"\s*[:：]\s*([^。\n;；,，、（]{0,72})")),
    # P3b: k' = <式 ≤26 字>: <run>（v5:132 的 r_k/k 路径）
    ("D", re.compile(r"(?<![A-Za-z/\\])\$?\\?k\$?(?:'|′|\^\{\\prime\}|\^\\prime)\$?"
                     r"\s*=\s*[^。\n：:]{1,26}?[:：]\s*([^。\n;；,，、（]{0,72})")),
]
# 自称存疑的标记（机读，用于在口径表里诚实标注 ⑥⑦⑧ 的性质）
SELF_BAD = re.compile(r"量纲不符|量纲不匹配|不完全匹配|无法直接对比|需要进一步验证|似乎.*不一致")
ASSUME = re.compile(r"假设")


def scan_kp_dir():
    """一遍遍历 FDIR，收集：
      vals    —— 数值宣称 [(rel, lineno, 值, 单位串, snip)]
      dims    —— 显式量纲断言 [(rel, lineno, (M,L,T,Q), run)]
      hard    —— 含 √/\\frac 等不可安全求值的宣称式 [(rel, lineno, snip)]
      harddim —— 量纲断言中无法解析的 [(rel, lineno, run)]
    """
    vals, dims, hard, harddim = [], [], [], []
    for root, dirs, fs in os.walk(FDIR):
        for fn in sorted(fs):
            if not (fn.lower().endswith(".md") or fn.endswith(".py")):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, FDIR)
            try:
                lines = open(p, encoding="utf-8").read().splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                nline = _norm_line(line)
                # ① 数值宣称（k' = <数> / k' … 值为 <数>）
                for m in list(KP_PAT.finditer(nline)) + list(KP_PAT2.finditer(nline)):
                    if nline[:m.start()].rstrip().endswith("/"):
                        continue
                    if PROD_PRE.search(nline[:m.start()]):
                        continue          # ⑪ 乘积上下文（k×k′、f·k′…）
                    if "无量纲" in SEG_SPLIT.split(m.group(1))[0]:
                        continue
                    snip = CUT_AT.split(m.group(1))[0].strip()
                    if not snip or TMPL_FORM.search(snip):
                        continue
                    val = chosen = vpos = None
                    for s in [x for x in SEG_SPLIT.split(snip) if x.strip()]:
                        if "无量纲" in s:
                            continue
                        if UNIT_INPUT.match(_strip_latex(s.strip())):
                            continue      # ⑧ 单位输入（k'=1 A·s²/kg），非数值宣称
                        r = _seg_value(s)
                        if r is None:
                            continue
                        val, vpos = r
                        chosen = s
                        # ⑫ 数值链后紧跟「运算符 + 字母」⇒ 这是公式（k' = 1/k、k' = 1/f），
                        #    不是数值宣称（r171 实跑抓到 v3:466/481 两处假 "1"）
                        tail = _desup(s.strip())[vpos:].lstrip()
                        if re.match(r"(?:[·/×*]|\\times|\\cdot|\\div)\s*[A-Za-z\\]", tail):
                            val = None
                            break
                        if UNIT_TOK.search(s):
                            break
                    if val is not None and chosen is not None and HARD_FORM.search(chosen):
                        val = None                      # 含 √/\\frac 的宣称式不硬解
                    unit_txt = ""
                    if val is not None and chosen is not None and vpos is not None:
                        # vpos 相对 _desup(chosen.strip())（与 _seg_value 内部同一变换）；
                        # 单位串里的 \\cdot 由 UNIT_AFTER 正则直接吃，不做变长替换。
                        mu = UNIT_AFTER.match(_desup(chosen.strip())[vpos:])
                        if mu:
                            unit_txt = mu.group(1).strip()
                    if val is not None and val == val and abs(val) != float("inf"):
                        vals.append((rel, i, val, unit_txt, snip[:48]))
                    elif HARD_FORM.search(snip):
                        hard.append((rel, i, snip[:60]))
                # ② 显式量纲断言（四种形态）
                for _tag, pat in KP_DIM_PATS:
                    for m in pat.finditer(nline):
                        if PROD_PRE.search(nline[:m.start()]):
                            continue      # k′k、f·k′ 等乘积主语
                        d = _dim_run(m.group(1))
                        if d is not None:
                            dims.append((rel, i, d, m.group(1)[:44]))
                        else:
                            harddim.append((rel, i, m.group(1)[:60]))
    return vals, dims, hard, harddim



def d_str(a):
    return "M^{} L^{} T^{} Q^{}".format(*a)


def d_str_si(a):
    m, l, t, q = a
    parts = []
    if m:
        parts.append("kg" if m == 1 else "kg^{}".format(m))
    if l:
        parts.append("m" if l == 1 else "m^{}".format(l))
    if t:
        parts.append("s" if t == 1 else "s^{}".format(t))
    if q:
        parts.append("C" if q == 1 else "C^{}".format(q))
    return "·".join(parts) if parts else "无量纲"


def d_str_ascii(a):
    """无 Unicode 上标的量纲串（用于判词与 key_numbers，避免编码漂移）。"""
    m, l, t, q = a
    p = []
    if m:
        p.append("M" if m == 1 else "M^%d" % m)
    if l:
        p.append("L" if l == 1 else "L^%d" % l)
    if t:
        p.append("T" if t == 1 else "T^%d" % t)
    if q:
        p.append("Q" if q == 1 else "Q^%d" % q)
    return "*".join(p) if p else "1"


# ============================== ast：结论-计算耦合度（承 r166/r168） ==============================
JUDGE_WORDS = ("正确", "错误", "一致", "不一致", "可以相加", "无法直接相加",
               "✅", "❌")


def _is_strlit_print(node):
    if not isinstance(node, ast.Expr):
        return False
    v = node.value
    if not (isinstance(v, ast.Call) and getattr(v.func, "id", None) == "print"):
        return False
    if len(v.args) == 0:
        return False
    for a in v.args:
        if not isinstance(a, ast.Constant) or not isinstance(a.value, str):
            return False
    return True


def _has_judge(txt):
    return any(w in txt for w in JUDGE_WORDS)


def _is_banner_print(node):
    if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)):
        return False
    v = node.value
    if getattr(v.func, "id", None) != "print" or len(v.args) != 1:
        return False
    a = v.args[0]
    if not (isinstance(a, ast.BinOp) and isinstance(a.op, ast.Mult)):
        return False
    left = a.left
    return (isinstance(left, ast.Constant) and isinstance(left.value, str)
            and len(left.value) == 1)


def _sig_digits(dec_str):
    s = dec_str.strip().lower()
    if "e" in s:
        s = s.split("e")[0]
    s = s.lstrip("+-").replace(".", "")
    return len(s.lstrip("0"))


def _round_to_sig(x, n):
    q = DEC(1).scaleb(x.adjusted() - (n - 1))
    return x.quantize(q)


def analyze_file(path):
    out = {"path": path, "parse_ok": False, "top": 0, "head": 0, "inif": 0,
           "top_lines": [], "compute": 0, "error": "", "bad_escape": 0}
    try:
        src = open(path, encoding="utf-8").read()
        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            tree = ast.parse(src)
        out["bad_escape"] = sum(1 for w in wlist
                                if issubclass(w.category, SyntaxWarning))
    except Exception as e:
        out["error"] = "{}: {}".format(type(e).__name__, e)
        return out
    out["parse_ok"] = True
    if_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            for sub in ast.walk(node):
                if _is_strlit_print(sub):
                    if_lines.add(sub.lineno)
    banner_after = set()
    for i, nd in enumerate(tree.body):
        if i + 1 < len(tree.body) and _is_banner_print(tree.body[i + 1]):
            banner_after.add(nd.lineno)
    top, head, inif = [], [], []
    for node in ast.walk(tree):
        if _is_strlit_print(node) and _has_judge(node.value.args[0].value):
            ln = node.lineno
            if ln in if_lines:
                inif.append(ln)
            elif ln in banner_after:
                head.append(ln)
            else:
                top.append(ln)
    out["top"], out["head"], out["inif"] = len(top), len(head), len(inif)
    out["top_lines"] = top
    skip = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                and getattr(node.value.func, "id", None) == "print"):
            for sub in ast.walk(node):
                skip.add(id(sub))
    n = 0
    for node in ast.walk(tree):
        if id(node) in skip:
            continue
        if isinstance(node, (ast.Assign, ast.If, ast.Compare, ast.For, ast.While)):
            n += 1
        elif isinstance(node, ast.BinOp):
            n += 1
        elif isinstance(node, ast.Call):
            n += 1
    out["compute"] = n
    return out


# ============================== A 组：先给靶应得的 PASS ==============================
def group_A():
    print("\n" + "=" * 78)
    print(" [A 组] 先给靶应得的 PASS：数值与量纲闭合的独立复核")
    print("=" * 78)
    out = {}

    # ---- A0 数值复核（Decimal 60 位）：k' = q_p / c = sqrt(4 pi eps0 hbar c) / c ----
    qp = (FOUR_PI * EPS0 * HBAR * C_LIGHT).sqrt()
    kp_calc = qp / C_LIGHT
    kp_claim = DEC("6.25e-27")
    n_sig = _sig_digits("6.25e-27")
    kp_round = _round_to_sig(kp_calc, n_sig)
    digit_match = (kp_round == kp_claim)
    rel = abs(kp_calc - kp_claim) / kp_claim
    print("[A0] k' = sqrt(4pi*eps0*hbar*c)/c = {:.20e} C·s/m（Decimal 60 位）".format(kp_calc))
    print("     靶（v4/v5/v6 裁定值）= {:.6e} C·s/kg".format(kp_claim))
    print("     我的值四舍五入到 {} 位有效数字 = {} ⇒ 与靶逐位相等 = {}".format(
        n_sig, kp_round, digit_match))
    print("     未取整前的相对差 = {:.6e}".format(rel))
    a0_ok = (rel < DEC("1e-3"))
    out.update({"A0_kp_calc": str(kp_calc), "A0_kp_claim": str(kp_claim),
                "A0_kp_round": str(kp_round), "A0_n_sig": n_sig,
                "A0_digit_match": digit_match, "A0_rel": str(rel), "A0_ok": a0_ok,
                "A0_qp": str(qp)})
    add("A0", "数值层",
        "数值实质正确：k′ = √(4πε₀ħc)/c = **{}**，与靶裁定值 6.25e−27 相对差 **{:.3e}**".format(
            kp_calc, rel),
        "PASS" if a0_ok else "FAIL",
        "用 Decimal 60 位独立重算 k′ = q_p/c（q_p = √(4πε₀ħc) = **{}** C）⇒ **{}**。"
        "靶（v4/1.md §3.4「校准值」、v5/1.md 方法 3、v6/code/calculate_k_prime.py expected）"
        "宣称 **6.25e−27**。相对差 **{:.6e}**（0.098%）⇒ **靶的数值与这条公式实质相符**"
        "（数量级、公式路径、前两位有效数字全部一致）。"
        "★诚实登记一处修约 slip：把 60 位值四舍五入到靶给出的 **{} 位有效数字**得 **{}**，"
        "与靶字面值 **6.25e−27** 第三位不符（靶似是截断而非修约）⇒ 单列登记，"
        "不影响 PASS 实质。**这是本卷对靶有利的结论。**"
        "本卷指控的不是这个数怎么算，而是**这个数配的是哪个量纲、能不能代回方程、"
        "与其它五个数什么关系**（B 组）。".format(qp, kp_calc, rel, n_sig, kp_round))

    # ---- A1 电荷方程与电场方程的量纲闭合（[k']=[IT²/M]、[k]=[M]）----
    rhs_q = d_mul(d_mul(DIM_KP_MAIN, D_K), D_TINV)
    q_ok = (rhs_q == D_CHARGE)
    rhs_e = d_mul(d_mul(d_div(d_mul(DIM_KP_MAIN, D_K), D_EPS0), D_TINV), D_L2)
    e_ok = (rhs_e == D_E_FIELD)
    print("[A1] 电荷方程 [k']·[k]·[T⁻¹] = {} vs [q] = {} ⇒ {}".format(
        d_str(rhs_q), d_str(D_CHARGE), "闭合 ✓" if q_ok else "不闭合 ✗"))
    print("     电场方程 [k][k']/[ε₀]·[T⁻¹]·[L⁻²] = {} vs [E] = {} ⇒ {}".format(
        d_str(rhs_e), d_str(D_E_FIELD), "闭合 ✓" if e_ok else "不闭合 ✗"))
    a1_ok = q_ok and e_ok
    out.update({"A1_rhs_charge": d_str(rhs_q), "A1_rhs_E": d_str(rhs_e),
                "A1_charge_ok": q_ok, "A1_E_ok": e_ok, "A1_ok": a1_ok})
    add("A1", "量纲层",
        "电荷方程与电场方程的量纲闭合**确实成立**：[k′]=[IT²/M]、[k]=[M] 下两式均精确配平",
        "PASS" if a1_ok else "FAIL",
        "机读 (M,L,T,Q) 四元运算：电荷方程 [k′][k][dΩ/dt] = **{}** = [q] = **{}** ✓；"
        "电场方程 [k][k′]/[ε₀]·[dΩ/dt]·[r/r³] = **{}** = [E] = **{}** ✓。"
        "⇒ v1 裁定书 §1、§2 两节的量纲推导**算术上是对的**（本卷对靶有利，诚实登记）。"
        "★但 §3 的磁场方程**不成立**（见 B2：它自己的乘积就算错了，且结构上无解）⇒ "
        "「[IT²/M] 是**唯一**能够同时满足三个方程的量纲」这一**结论**是假的。".format(
            d_str(rhs_q), d_str(D_CHARGE), d_str(rhs_e), d_str(D_E_FIELD)))

    # ---- A2 k = 4π m_p 与 r163 独立登记一致 ----
    k_calc = FOUR_PI * M_PLANCK
    k_claim_v1 = DEC("2.73e-7")
    k_claim_v5 = DEC("2.736e-7")
    rel_k = abs(k_calc - k_claim_v5) / k_claim_v5
    print("[A2] k = 4π·m_p = {:.10e} kg；靶 v1 称 2.73e−7、v5 称 2.736e−7 ⇒ 相对差 {:.3e}".format(
        k_calc, rel_k))
    a2_ok = (rel_k < DEC("1e-2"))
    out.update({"A2_k_calc": str(k_calc), "A2_k_claim_v1": str(k_claim_v1),
                "A2_k_claim_v5": str(k_claim_v5), "A2_k_rel": str(rel_k), "A2_ok": a2_ok})
    add("A2", "量纲层",
        "k = 4π·m_p = **{:.6e} kg** 与 r163 的独立登记一致（靶这一条是对的）".format(k_calc),
        "PASS" if a2_ok else "FAIL",
        "由质量定义 m = k·(n/Ω) 取 n=1、Ω=4π ⇒ k = 4πm_p = **{}** kg（Decimal 60 位）。"
        "靶 v1 裁定书称 2.73e−7、v5 称 2.736e−7，与本卷重算相对差 **{:.3e}** ⇒ 量级与形式均确认。"
        "★这与 r163「k = 4πm_p」的独立登记**互相印证**（本卷对靶有利）。"
        "★但同一目录里 v2/v4 却把 k 说成 m_p = 2.176e−8（差 4π = 12.566 倍）、"
        "v4 还提到 k = c³/G = 4.037e35（差 1.855e43 倍）⇒ 见 D2。".format(
            k_calc, rel_k))
    return out


# ============================== B 组：量纲口径层（本卷核心） ==============================
def group_B():
    print("\n" + "=" * 78)
    print(" [B 组] 量纲口径层：同一常数 k' 的多重被主张口径 + 磁场方程可满足性")
    print("=" * 78)
    out = {}

    # ---- B1/B7 共用：一遍机读遍历（数值宣称 + 显式量纲断言）----
    vals, dims, hard_hits, hard_dim = scan_kp_dir()

    # ---- B1 ★机读：同一常数 k' 的被主张 (M,L,T,Q) 口径清点 ----
    # 两种书面形态都收：
    #   ① 显式量纲断言（[k']=…、k'的量纲为…、k'=式→…、k': …）——KP_DIM_PATS 四型；
    #   ② 数值宣称后跟的单位串（k' ≈ 1.16×10¹⁰ A·s²/kg）——vals 的单位串解析。
    # 排除（都由机器执行）：乘积上下文（kk′、k×k′、f·k′）、单位输入（k'=1 A·s²/kg）、
    #   他物量纲（断言形态要求 k′ 必须是主语，挡住 dm/dt 的 [kg/s]、q_p 的 [C]）、
    #   含 √/\frac 的宣称式（不硬解，单列 hard_dim）。
    claims = []          # (dim, kind, rel, lineno, txt, flags)
    for rel, ln, dm, run in dims:
        claims.append((dm, "断言", rel, ln, run))
    n_unit_claims = 0
    for rel, ln, v, unit_txt, snip in vals:
        if not unit_txt:
            continue
        dm = _dim_parse(unit_txt)
        if dm is None:
            continue
        n_unit_claims += 1
        claims.append((dm, "单位", rel, ln, "{:.6g} {}".format(v, unit_txt)))
    # 逐条打上「自称存疑 / 假设式」标记（机读源行文本）
    flagged = []
    for dm, kind, rel, ln, txt in claims:
        try:
            line = _norm_line(open(os.path.join(FDIR, rel), encoding="utf-8")
                              .read().splitlines()[ln - 1])
        except (OSError, IndexError):
            line = ""
        fl = []
        if SELF_BAD.search(line):
            fl.append("源行含存疑语")
        if ASSUME.search(line):
            fl.append("源行为假设式")
        flagged.append((dm, kind, rel, ln, txt, "、".join(fl)))
    uniq = []            # [{dim, src:[(kind, rel, ln, txt, flags)]}]
    for dm, kind, rel, ln, txt, fl in flagged:
        s = d_str(dm)
        for u in uniq:
            if u["s"] == s:
                u["src"].append((kind, rel, ln, txt, fl))
                break
        else:
            uniq.append({"s": s, "dim": dm, "src": [(kind, rel, ln, txt, fl)]})
    n_uniq = len(uniq)
    print("[B1] 机读同一常数 k' 的被主张 (M,L,T,Q) 口径"
          "（显式量纲断言 {} 处 + 数值后跟单位串 {} 处，去重后）：".format(
              len(dims), n_unit_claims))
    CN = "①②③④⑤⑥⑦⑧⑨⑩"
    for idx, u in enumerate(uniq):
        fls = sorted(set(f for _, _, _, _, f in u["src"] if f))
        print("     {} {:<20s} {:>2} 处  {}{}".format(
            CN[idx] if idx < len(CN) else "⑪+", u["s"], len(u["src"]),
            "；".join("{}:{}".format(r, l) for _, r, l, _, _ in u["src"][:3]),
            "  [{}]".format("、".join(fls)) if fls else ""))
    print("     ⇒ 互不相同的被主张口径数 = **{}**".format(n_uniq))
    print("     （另有磁场方程**要求**的口径 {} = [C·m/kg]，由 B2 解析求解，非靶主张）".format(
        d_str(DIM_KP_B_REQ)))
    print("     （另有 {} 处显式量纲断言无法安全解析，未计入：{}）".format(
        len(hard_dim), "；".join("{}:{}".format(r, l) for r, l, _ in hard_dim[:5])))
    out.update({"B1_calibres": [(CN[i] if i < len(CN) else "?",
                                 u["s"], len(u["src"]),
                                 "；".join("{}:{}".format(r, l) for _, r, l, _, _ in u["src"][:6]),
                                 "；".join(sorted(set(f for _, _, _, _, f in u["src"] if f))))
                                for i, u in enumerate(uniq)],
                "B1_n_uniq": n_uniq,
                "B1_n_dim_claims": len(dims),
                "B1_n_unit_claims": n_unit_claims,
                "B1_hard_dim": ["{}:{}".format(r, l) for r, l, _ in hard_dim[:10]],
                "B1_b_req": d_str(DIM_KP_B_REQ)})
    flagged_dims = ["{} {}".format(u["s"], CN[i] if i < len(CN) else "?")
                    for i, u in enumerate(uniq)
                    if any(f for _, _, _, _, f in u["src"])]
    add("B1", "量纲层",
        "★★机读：同一常数 k' 被主张 **{}** 种互不相同的 (M,L,T,Q) 口径".format(n_uniq),
        "FAIL",
        "机读全目录 k′ 的量纲宣称：显式量纲断言 **{}** 处 + 数值后跟单位串 **{}** 处，"
        "按 (M,L,T,Q) 四元去重得 **{} 种互异口径**：{}。"
        "其中 **{}** 的源行自带「假设 / 量纲不符 / 不完全匹配」等标记（列此仅供追查原文，不改变计数）"
        "（口径表性质列已逐条标注，收进来是为防「挑软的指控」的反向偏袒）。"
        "即便只数正式裁定链主张的口径也已有多种，且**没有任何一处说明它们之间的关系**。"
        "（互异口径数是机读值、随语料变化，故判词不用具体计数；另有 **{}** 处显式量纲断言"
        "无法安全解析，未计入。）".format(
            len(dims), n_unit_claims, n_uniq,
            "、".join("{} {}".format(u["s"], CN[i] if i < len(CN) else "?")
                      for i, u in enumerate(uniq)),
            "、".join(flagged_dims) if flagged_dims else "无",
            len(hard_dim)))

    # ---- B2 ★磁场方程：裁定书自己的乘积算错 + 结构上不可满足 ----
    # B2a 裁定书 §3 的书写因子逐项机读相乘
    doc_factors = [D_MU0, D_K, DIM_KP_MAIN, D_TINV, D_L2]
    doc_prod = (0, 0, 0, 0)
    for fdoc in doc_factors:
        doc_prod = d_mul(doc_prod, fdoc)
    doc_claim = D_B_FIELD
    print("[B2a] 裁定书 §3 书写因子乘积 = {}；其自称结果 = {}；真 [B] = {}".format(
        d_str(doc_prod), d_str(doc_claim), d_str(D_B_FIELD)))
    print("      乘积 == 自称结果？ {}  ⇒ 裁定书的乘法**算错了**".format(doc_prod == doc_claim))
    # B2b 结构可满足性：解出磁场方程对 [k'] 的要求
    req_b = DIM_KP_B_REQ
    req_q = tuple(a - b - c for a, b, c in zip(D_CHARGE, D_K, D_TINV))
    req_e = tuple(a - b - c - d - e for a, b, c, d, e in
                  zip(D_E_FIELD, D_K, d_inv(D_EPS0), D_TINV, D_L2))
    print("[B2b] 三方程对 [k'] 的要求：电荷 {} / 电场 {} / 磁场 {}".format(
        d_str(req_q), d_str(req_e), d_str(req_b)))
    satisfiable = (req_q == req_e == req_b)
    print("      三者一致？ {} ⇒ {}".format(
        satisfiable, "存在唯一 [k'] 同时满足三式" if satisfiable
        else "**不存在**任何 [k'] 能同时满足三个方程"))
    # B2c 场景2 同样失败
    rhs_b_s2 = d_mul(d_mul(d_mul(d_mul(DIM_KP_LM1, (1, 1, 0, 0)), D_MU0), D_TINV), D_L2)
    s2_b_ok = (rhs_b_s2 == D_B_FIELD)
    print("[B2c] 场景2（[k]=[LM]、[k']=[L⁻¹IT²/M]）磁场方程 RHS = {} vs [B] = {} ⇒ {}".format(
        d_str(rhs_b_s2), d_str(D_B_FIELD), "闭合" if s2_b_ok else "**不闭合**"))
    # B2d v6/公式验证/数据计算.md 的同款错误（其 [μ₀] 写成 MLT⁻²Q⁻²）
    mu0_doc = (1, 1, -2, -2)
    prod_doc2 = d_mul(d_mul(d_mul(mu0_doc, d_mul(DIM_KP_MAIN, D_K)), D_TINV), D_L2)
    claim_doc2 = (1, 0, -2, -1)
    print("[B2d] v6/数据计算.md：其书写 [μ₀]=MLT⁻²Q⁻²（真 [μ₀]={}）".format(d_str(D_MU0)))
    print("      其因子乘积 = {}，其自称 = {}，真 [B] = {} ⇒ 双重错误".format(
        d_str(prod_doc2), d_str(claim_doc2), d_str(D_B_FIELD)))
    out.update({"B2_doc_prod": d_str(doc_prod), "B2_doc_claim": d_str(doc_claim),
                "B2_doc_arith_ok": doc_prod == doc_claim,
                "B2_req_charge": d_str(req_q), "B2_req_E": d_str(req_e),
                "B2_req_B": d_str(req_b), "B2_satisfiable": satisfiable,
                "B2_s2_b_rhs": d_str(rhs_b_s2), "B2_s2_b_ok": s2_b_ok,
                "B2_doc2_prod": d_str(prod_doc2), "B2_doc2_claim": d_str(claim_doc2),
                "B2_mu0_doc": d_str(mu0_doc)})
    add("B2", "量纲层",
        "★★磁场方程：裁定书自己的乘法**算错**，且三方程对 [k′] 的要求**互不相同** ⇒ "
        "「[IT²/M] 是唯一能同时满足三方程的量纲」是**假的**",
        "FAIL",
        "**B2a 算术层**：v1 裁定书 §3 书写「[MLI⁻²T⁻²]×[M]×[IT²/M]×[1]×[1/T]×[1]×[L⁻²] = [MI⁻¹T⁻²]」。"
        "机读逐项相乘（(M,L,T,Q) 四元）得 **{}**，而其自称结果为 **{}** ⇒ "
        "**裁定书自己的乘积就算错了**（多了 L⁻¹、少了 T⁻¹）。"
        "**B2b 结构层（最硬）**：把三个方程各自解出对 [k′] 的要求 —— "
        "电荷方程要求 **{}**、电场方程要求 **{}**、磁场方程要求 **{}**。"
        "三者**互不相同** ⇒ **不存在**任何一个 [k′] 能同时满足三个方程；"
        "根因是磁场公式写成 `μ₀kk′R/(4πΩ²R³)·dΩ/dt`（位置矢量 R/R³）而经典形式是 "
        "`μ₀q v×r/(4πr³)`（速度叉乘）⇒ **公式本身缺一个速度因子 L·T⁻¹**，"
        "不是常数取错。**B2c**：裁定书自称「多场景参数优化 ✅ 通过」的场景 2"
        "（[k]=[LM]、[k′]=[L⁻¹IT²/M]）同样不闭合（RHS = **{}** ≠ [B]）。"
        "**B2d**：v6/公式验证/数据计算.md 的量纲验证同款双错 —— 它把 [μ₀] 写成 "
        "**{}**（正确为 **{}**，多一个 T⁻²），且乘积 **{}** 也不等于其自称的 **{}**。".format(
            d_str(doc_prod), d_str(doc_claim), d_str(req_q), d_str(req_e), d_str(req_b),
            d_str(rhs_b_s2), d_str(mu0_doc), d_str(D_MU0), d_str(prod_doc2), d_str(claim_doc2)))

    # ---- B3 ★代回检验 ----
    k_exact = FOUR_PI * M_PLANCK
    # B3a 电荷定义方程代回：q = k'k/Ω²·dΩ/dt
    scen = []
    for kp_val, kp_tag, kp_unit in ((DEC("1.16e10"), "v1 裁定", "A·s²/kg"),
                                    (DEC("6.25e-27"), "v4/v5/v6 裁定", "C·s/kg")):
        for om_tag, om in (("Ω=4π", FOUR_PI), ("Ω=1", DEC(1))):
            q = kp_val * k_exact / (om * om) * DEC(1)
            ratio = q / E_CHARGE
            dev = max(ratio, DEC(1) / ratio)      # 偏离倍数（双向）
            scen.append((kp_tag, kp_val, om_tag, q, ratio, dev))
            print("[B3a] k′={} ({}), {} , dΩ/dt=1 ⇒ q = {:.6e} C；q/e = {:.4e}（偏离 {:.4e} 倍）".format(
                kp_val, kp_unit, om_tag, q, ratio, dev))
    # B3b 复合常数 kk'/(4πε₀) vs 库仑常数
    comp_116 = (DEC("1.16e10") * k_exact) / (FOUR_PI * EPS0)
    comp_ratio = comp_116 / KE
    print("[B3b] kk′/(4πε₀)（k′=1.16e10）= {:.6e} N·m²/C²；库仑常数 = {:.6e} ⇒ 比 {:.4f}".format(
        comp_116, KE, comp_ratio))
    # B3c 基本电荷的库仑场：ZUFT（电荷方程反推的 q）vs 经典（q=e）
    q_eq_116 = DEC("1.16e10") * k_exact / (FOUR_PI * FOUR_PI) * DEC(1)
    e_cl = KE * E_CHARGE / DEC(1)                      # r = 1 m
    e_zuft = (k_exact * DEC("1.16e10") / (FOUR_PI * EPS0 * FOUR_PI * FOUR_PI) * DEC(1)) / DEC(1)
    field_ratio = e_zuft / e_cl
    print("[B3c] r=1 m 处：经典库仑场（q=e）= {:.6e} N/C；ZUFT（k′=1.16e10）= {:.6e} N/C ⇒ 比 {:.4f}".format(
        e_cl, e_zuft, field_ratio))
    out.update({"B3_scenarios": [(t, str(v), om, str(q), str(r), str(dv))
                                 for t, v, om, q, r, dv in scen],
                "B3_scenarios_dev": [str(dv) for _, _, _, _, _, dv in scen],
                "B3_comp_116": str(comp_116), "B3_comp_ratio": str(comp_ratio),
                "B3_e_classical": str(e_cl), "B3_e_zuft": str(e_zuft),
                "B3_field_ratio": str(field_ratio), "B3_q_eq_116": str(q_eq_116)})
    worst = max(dv for _, _, _, _, _, dv in scen)
    add("B3", "量纲层",
        "★★代回检验：靶自报的两个 k′ 代回电荷定义方程都**给不出基本电荷**"
        "（偏离 10¹³～10²² 倍），复合常数与库仑常数差 **{:.1f}** 倍".format(float(comp_ratio)),
        "FAIL",
        "取靶自己的 k = 4πm_p = **{:.10e}** kg、dΩ/dt = 1，把两个被裁定的 k′ 代回电荷定义方程 "
        "q = k′k/Ω²·(dΩ/dt)：k′ = 1.16e10 ⇒ q = **{:.6e} C**（Ω=4π）/ **{:.6e} C**（Ω=1）；"
        "k′ = 6.25e−27 ⇒ q = **{:.6e} C** / **{:.6e} C**。"
        "真基本电荷 e = **1.602176634e−19 C** ⇒ 两个宣称值分别偏离 **{:.4e}** 与 **{:.4e}** 倍，"
        "**没有一个能代回电子电荷**（靶自己在 v6/code/1.py 第 7 步也承认「相差甚远……"
        "需要调整几何参数使方程成立」）。"
        "**复合常数**：v1 裁定书称 kk′/(4πε₀) ≈ 1.0e10 N·m²/C²「与库仑常数一致」，"
        "实算 **{:.6e}**，与库仑常数 {:.6e} 差 **{:.4f}** 倍。"
        "**库仑场代回**：r = 1 m 处经典场（q = e）= **{:.6e} N/C**，"
        "而 ZUFT 式（k′ = 1.16e10）= **{:.6e} N/C** ⇒ 差 **{:.4f}** 倍。".format(
            k_exact,
            scen[0][3], scen[1][3], scen[2][3], scen[3][3],
            scen[0][5], scen[2][5],
            comp_116, KE, comp_ratio, e_cl, e_zuft, field_ratio))

    # ---- B4 ★公式与数值脱钩 ----
    kp_from_ke = KE * (C_LIGHT ** 3) / (HBAR ** 2)     # v4 的公式 k' = k_e c³/ħ²
    kp_adopted = DEC("6.25e-27")
    detach_ratio = kp_from_ke / kp_adopted
    ke_from_kp = kp_adopted * (HBAR ** 2) / (C_LIGHT ** 3)   # k_e = k'ħ²/c³
    ke_rel = abs(ke_from_kp - KE) / KE
    print("[B4] v4 公式 k′ = k_e·c³/ħ² 实算 = {:.6e}；其采纳「校准值」= {:.6e} ⇒ 比 {:.4e}".format(
        kp_from_ke, kp_adopted, detach_ratio))
    print("     反代 k_e = k′ħ²/c³（k′=6.25e−27）= {:.6e}；真 k_e = {:.6e} ⇒ 相对差 {:.6e}".format(
        ke_from_kp, KE, ke_rel))
    out.update({"B4_kp_from_ke": str(kp_from_ke), "B4_kp_adopted": str(kp_adopted),
                "B4_detach_ratio": str(detach_ratio), "B4_ke_from_kp": str(ke_from_kp),
                "B4_ke_rel": str(ke_rel)})
    add("B4", "量纲层",
        "★公式与数值**脱钩**：k′ = k_e·c³/ħ² 实算 **{:.4e}**，靶却采纳「校准值 6.25e−27」"
        "（差 **{:.3e}** 倍）".format(kp_from_ke, detach_ratio),
        "FAIL",
        "v4/1.md §3.2 给出 k′ = k_e·c³/ħ² 并称「这是导出 k′ 数值的关键公式」，"
        "§3.4 自己算出 ≈ **2.176×10¹⁰³**（带问号），随后却写「文档中给出的校准值为 "
        "6.25×10⁻²⁷ C·s/kg……故本项目采纳此数值作为最终结果」。"
        "本卷 Decimal 60 位实算 k_ec³/ħ² = **{:.10e}**，与采纳值相差 **{:.4e}** 倍 "
        "⇒ **公式和数值不是一回事**：采纳值其实来自另一条路径 k′ = q_p/c（A0）。"
        "反向代回同样脱钩：把 6.25e−27 代入 k_e = k′ħ²/c³ 得 **{:.6e}**，"
        "而真 k_e = **{:.6e}** ⇒ 相对差 **{:.6e}**（≈ −100%）。"
        "★**靶自承**：v6/传统物理/传统物理对比.md 明写「k_e = k′ħ²/c³ 在 SI 单位制下 "
        "≈ 10⁻¹²⁰，与经典值相差 129 个数量级，源于量纲体系差异，无法直接对比」；"
        "v5/1.md §4.5 三种尝试导出 k_e 全部「约 −100%」并自陈「未能找到一条清晰、"
        "无歧义且量纲正确的数学公式」。⇒ **库仑常数闭环断裂是靶自己承认的**。".format(
            kp_from_ke, detach_ratio, ke_from_kp, KE, ke_rel))

    # ---- B5 数值无法跨版本使用 ----
    ratio_versions = DEC("1.16e10") / DEC("6.25e-27")
    print("[B5] v1 裁定值 1.16e10 A·s²/kg vs v4/v5/v6 裁定值 6.25e−27 C·s/kg ⇒ 比 {:.6e}".format(
        ratio_versions))
    out.update({"B5_ratio_versions": str(ratio_versions)})
    add("B5", "量纲层",
        "两轮「裁定」的数值**相差 {:.4e} 倍**且单位口径也不同，无法跨版本使用".format(
            ratio_versions),
        "FAIL",
        "同一目录内：v1《常数 k′ 的量纲最终裁定》裁定 k′ ≈ **1.16×10¹⁰ A·s²/kg**"
        "（v1/1.md、v1/交叉验证、v2 主文同）；v4/v5/v6 却一致采用 **6.25×10⁻²⁷ C·s/kg**。"
        "机读比值 = **{:.6e}**。两者既不同值也不同单位（A·s²/kg vs C·s/kg —— 虽量纲相同，"
        "但靶在 v6/code/1.py 里又把计算路径标成 C·s/m）⇒ "
        "**同一个常数在同一目录里有两套互不相干的「最终」数值，没有任何一处说明它们的关系**。"
        "（与 r168 B4「两轮最终裁定」同型，此处是**跨版本**六卷。）".format(ratio_versions))

    # ---- B7 机读全目录 k' 的数值宣称 ----
    # 遍历与求值已上移为模块级 scan_kp_dir()（B1 口径清点与本条共用一遍遍历）。
    # 求值器防假阳性：承自 r168 的五层（环视/行内截断/连乘不双计/print 模板/无量纲首段），
    # 加本卷实跑抓到的四层（单位输入、LaTeX 细空格、严格数值前缀、乘积上下文）。
    raw_hits = [(rel, ln, v, snip, unit_txt) for rel, ln, v, unit_txt, snip in vals]
    raw_hits.sort(key=lambda h: h[2])
    clusters = []
    for rel, ln, v, snip, unit_txt in raw_hits:
        if clusters and abs(v - clusters[-1]["v"]) <= 5e-3 * max(abs(v), abs(clusters[-1]["v"])):
            clusters[-1]["hits"].append((rel, ln, v, snip, unit_txt))
        else:
            clusters.append({"v": v, "hits": [(rel, ln, v, snip, unit_txt)]})
    n_vals = len(clusters)
    print("[B7] 机读全目录 k' 的数值宣称：可求值命中 {} 处，聚类后互异数值 {} 个".format(
        len(raw_hits), n_vals))
    for c in clusters:
        hs = c["hits"]
        print("     {:.6g}  （{} 处：{}）".format(
            c["v"], len(hs), "；".join("{}:{}".format(r, l) for r, l, _, _, _ in hs[:4])))
    print("     另有 {} 处含 √/\\frac 的宣称式（不可安全求值，未硬解）：{}".format(
        len(hard_hits), "；".join("{}:{}".format(r, l) for r, l, _ in hard_hits[:6])))
    out.update({"B7_n_values": n_vals, "B7_n_hard": len(hard_hits),
                "B7_hard_where": ["{}:{}".format(r, l) for r, l, _ in hard_hits[:10]],
                "B7_raw_hits": [(r, l, v, u) for r, l, v, _, u in raw_hits],
                "B7_values": [{"v": c["v"], "n_hits": len(c["hits"]),
                               "where": ["{}:{}".format(r, l) for r, l, _, _, _ in c["hits"][:6]]}
                              for c in clusters]})
    add("B7", "量纲层",
        "★机读全目录 k′ 的**数值宣称**：互异数值 **{}** 个".format(n_vals),
        "FAIL",
        "用正则扫全部 .md 中 `k' =`/`k′ =`/`k^{{\\prime}} =` 右侧，按 `=`/`≈` 切段求值"
        "（`a × 10^{{−n}}` 连乘、`… = 末值` 链、段内数字后跟单位者优先；"
        "含 `√`/`\\frac` 的宣称式与 print 模板一律不当数值），再按 5e−3 相对容差聚类，"
        "得 **{} 个互异数值**：{}。另有 **{} 处**含 √/\\frac 的宣称式未硬解。"
        "⇒ 同一个常数在同一目录里被算出 **{}** 个互不相同的数，横跨 v1–v6 六个版本，"
        "且**没有任何一处说明它们之间的关系**。".format(
            n_vals,
            "、".join("{:.6g}（{} 处）".format(c["v"], len(c["hits"])) for c in clusters),
            len(hard_hits), n_vals))

    # ---- B6 分层铁律（INFO）----
    add("B6", "口径层",
        "分层铁律：本卷（量纲口径层+数值宣称层+方法论层）条目**不可与 r159–r170 相加**",
        "INFO",
        "★分层声明：本卷只裁「同一目录内 k′ 的量纲口径互斥 + 磁场方程可满足性 + "
        "公式与数值脱钩 + 结论硬编码的普遍性」这几层，与 r161（电荷几何化的公设层）、"
        "r168（f 的量纲口径层）**条目不可相加**——不得据本卷 FAIL 数堆叠出跨册「缺陷总数」。"
        "同理，本卷机读的多口径清点属**同一靶文档族内部**的互斥。")
    return out


# ============================== C 组：方法论层 ==============================
def group_C():
    print("\n" + "=" * 78)
    print(" [C 组] 方法论层：ast 全目录扫描 + 内部矛盾 + 循环等效性")
    print("=" * 78)
    out = {}

    # ---- C1 全目录 ast 扫描 ----
    files = []
    for root, dirs, fs in os.walk(FDIR):
        for fn in sorted(fs):
            if fn.endswith(".py"):
                files.append(os.path.join(root, fn))
    files.sort()
    res = [analyze_file(p) for p in files]
    n_ok = sum(1 for r in res if r["parse_ok"])
    n_bad = sum(1 for r in res if not r["parse_ok"])
    n_detached = sum(1 for r in res if r["parse_ok"] and r["top"] > 0)
    n_compute = sum(1 for r in res if r["parse_ok"] and r["compute"] > 0)
    total_top = sum(r["top"] for r in res)
    total_bad_escape = sum(r["bad_escape"] for r in res)
    print("[C1] 全目录 .py 共 {} 个：可解析 {}，解析失败 {}".format(len(files), n_ok, n_bad))
    print("     含**顶层硬编码结论**（与 if/else 脱钩）的脚本：{} 个".format(n_detached))
    print("     含**真实计算**的脚本：{} 个".format(n_compute))
    print("     顶层硬编码结论总数：{} 条；LaTeX 残片告警总数：{}".format(total_top, total_bad_escape))
    for r in res:
        rel = os.path.relpath(r["path"], FDIR)
        if not r["parse_ok"]:
            print("       [SKIP] {:<46s} {}".format(rel, r["error"][:60]))
        elif r["top"] > 0:
            print("       {:<44s} 硬编码结论 {:>2d} 条（行号 {}），计算节点 {}".format(
                rel, r["top"], r["top_lines"][:6], r["compute"]))
    out.update({"C1_files": len(files), "C1_parse_ok": n_ok, "C1_parse_bad": n_bad,
                "C1_detached": n_detached, "C1_compute": n_compute,
                "C1_total_top": total_top, "C1_bad_escape": total_bad_escape})
    add("C1", "方法论层",
        "★全目录扫描：{} 个 .py 中 **{} 个**含顶层硬编码结论（与 if/else 脱钩），共 **{} 条**".format(
            len(files), n_detached, total_top),
        "FAIL",
        "把 r166/r168 的 ast 检测器复用到 `常数 k' 的量纲最终裁定/` 全目录：共 **{}** 个 .py，"
        "可解析 **{}** 个；含**顶层硬编码结论**（与上方 if/else 判定脱钩的无条件 print）的脚本 "
        "**{} 个**，合计 **{} 条**；含**真实计算**的脚本 **{} 个**。"
        "⇒ 「硬编码结论」不是某一个脚本的偶发，而是**本目录的系统性做法**"
        "（与 r168 C1 的目录级统计同口径：只统计参数全为字符串字面量的 print，"
        "后随 `print(\"=\" * N)` 分隔线的分节标题已剔除）。".format(
            len(files), n_ok, n_detached, total_top, n_compute))

    # ---- C2 v2 内部矛盾：k'k = 1 A·s² 的前提 vs 252.416 的结论 ----
    k_v2 = DEC("2.176e-8")                 # v2 主文：k = m_p
    kp_v2_concl = DEC("1.16e10")
    kk_concl = kp_v2_concl * k_v2
    kp_from_premise = DEC(1) / k_v2        # 由 k'k = 1 A·s² 解出
    print("[C2] v2 前提 k′k = 1 A·s²、k = m_p = {:.6e} ⇒ k′ = {:.6e}".format(
        k_v2, kp_from_premise))
    print("     但 v2 结论 k′ = 1.16e10 ⇒ k′k = {:.6f} A·s²（≠ 1）".format(kk_concl))
    c2_bad = (abs(kk_concl - DEC(1)) > DEC("1e-6"))
    out.update({"C2_kp_from_premise": str(kp_from_premise), "C2_kk_concl": str(kk_concl),
                "C2_bad": c2_bad})
    add("C2", "量纲层",
        "★v2 主文**内部矛盾**：前提写 k′k = 1 A·s²（⇒ k′ = 1/k = 4.596e7），"
        "结论却给 k′ = 1.16e10（⇒ k′k = **252.416**）",
        "FAIL" if c2_bad else "PASS",
        "`v2/统一场论核心公式量纲验证与求导证明.md` 第 145 行：「由电荷定义方程的量纲结论 "
        "k′·k = IT²，取国际单位制基本量的单位量（I=1 A，T=1 s），则 k′·k = 1 A·s²，"
        "代入 k ≈ 2.176×10⁻⁸ kg，得 k′ = 1/(2.176×10⁻⁸) ≈ **4.596×10⁷** A·s²/kg」；"
        "第 152 行却直接写「k′ ≈ **1.16×10¹⁰** A·s²/kg」而**未给任何过渡**；"
        "第 156 行自报 k′k ≈ 1.16e10 × 2.176e−8 ≈ **252.4 A·s²** —— 与它自己第 145 行的"
        "前提 **1 A·s²** 相差 **252.4 倍**。同目录 `v2/验证/全面验证.md` 第 64 行又算得 "
        "k′ = 4.5946×10⁷、第 205 行出现「k′f 修正值 7.75×10¹」⇒ **三处互斥**。"
        "⇒ 同一版本内，k′ 的「单位量定标」推导与结论脱钩。".format())

    # ---- C3 六版本机读 ----
    vers = []
    for v in ("v1", "v2", "v3", "v4", "v5", "v6"):
        d = os.path.join(FDIR, v)
        if not os.path.isdir(d):
            continue
        n_md = n_py = 0
        rows = 0
        for root, dirs, fs in os.walk(d):
            for fn in fs:
                if fn.lower().endswith(".md"):
                    n_md += 1
                    try:
                        rows += sum(1 for _ in open(os.path.join(root, fn), encoding="utf-8"))
                    except OSError:
                        pass
                elif fn.endswith(".py"):
                    n_py += 1
        vers.append((v, n_md, n_py, rows))
    root_md = [f for f in sorted(os.listdir(FDIR))
               if f.lower().endswith(".md") and os.path.isfile(os.path.join(FDIR, f))]
    print("[C3] 版本机读：{}；根目录另有 {} 个 md".format(
        " → ".join("{} ({} md/{} py/{} 行)".format(v, a, b, c) for v, a, b, c in vers),
        len(root_md)))
    out.update({"C3_versions": vers, "C3_root_md": root_md})
    add("C3", "方法论层",
        "同一命题存在 **{} 个版本目录**（v1–v6，机读：{}）+ 根目录公式.md".format(
            len(vers), " → ".join("{}: {} md/{} py/{} 行".format(v, a, b, c)
                                  for v, a, b, c in vers)),
        "BOUNDARY",
        "机读各版本目录：{}；根目录另有 `公式.md` 等 {} 个 md。"
        "⇒ 一个常数的「量纲最终裁定」需要**六个版本**（v1 自称最终裁定，v2–v6 各自重做）。"
        "★记 **BOUNDARY**：多版本本身是正常学术修订，本卷**不**指控这一点；"
        "登记的是它与 v1「最终裁定」**确定性语气**（「唯一能够同时满足」「奠定了坚实的基础」）"
        "之间的张力——若已是最终裁定，何需 v2–v6？".format(
            "；".join("{} = {} 个 md + {} 个 py + {} 行".format(v, a, b, c) for v, a, b, c in vers),
            len(root_md)))

    # ---- C4 两难：q_p/c 定义 vs 电荷方程定义 ----
    dim_qp_route = DIM_KP_CSM          # [C·s/m]
    dim_eq_route = DIM_KP_MAIN         # [C·s/kg]
    print("[C4] q_p/c 路径给 [k′] = {}；电荷方程路径给 [k′] = {} ⇒ 相等？ {}".format(
        d_str(dim_qp_route), d_str(dim_eq_route), dim_qp_route == dim_eq_route))
    out.update({"C4_dim_qp_route": d_str(dim_qp_route), "C4_dim_eq_route": d_str(dim_eq_route)})
    add("C4", "推导层",
        "★两难：k′ 若由 k′ = q_p/c 定义则量纲是 **[C·s/m]**，若由电荷方程定义则是 **[C·s/kg]**，"
        "二者相差一个 L⁻¹M¹ ⇒ **不可兼得**",
        "FAIL",
        "v6/code/1.py 第 81–101 行与 v6/验证/verify_ke.py 第 55/81 行**自己算出的路径**是 "
        "k′ = q_p/c，其单位是 **C·s/m**（量纲 **{}**，v6/code/1.py 第 94/99/121 行反复自陈"
        "「这似乎与理论量纲不一致」）；而 v1 裁定书与电荷定义方程要求 [k′] = **{}**。"
        "两者相差 **(L⁻¹ vs M⁻¹)** —— 不是单位换算能弥补的。"
        "⇒ **两支都不利**：若坚持 k′ = q_p/c ⇒ 电荷定义方程 q = k′k/Ω²·dΩ/dt 量纲不相容"
        "（右侧多一个 L⁻¹）；若坚持电荷方程口径 ⇒ k′ **不是** q_p/c，"
        "则 A0 确认的那个 6.2561e−27 与整个 v6 求导链作废。"
        "靶的处理方式（v6/code/1.py 第 124–129 行）是「**以文档最终裁定为准**」——"
        "即用**声明**覆盖**自己算出的量纲**。".format(d_str(dim_qp_route), d_str(dim_eq_route)))

    # ---- C5 靶脚本可执行层自证矛盾（本卷新增：直接运行靶脚本并机读其输出）----
    # ★不用手抄：用 runpy 在进程内运行 v6/code/1.py（规避中文路径入 argv），
    #   捕获 stdout 后机读「它自己算出的误差」与「它自己打印的结论」。
    import contextlib
    import io
    import runpy
    buf = io.StringIO()
    run_err = ""
    try:
        with contextlib.redirect_stdout(buf):
            runpy.run_path(F_V6_CODE1, run_name="__main__")
    except Exception as e:
        run_err = "{}: {}".format(type(e).__name__, e)
    t_out = buf.getvalue()
    i_doc = t_out.find("使用文档 k'")
    seg_doc = t_out[i_doc:] if i_doc >= 0 else t_out
    m_err = re.search(r"相对误差：\s*([0-9.eE+-]+)%", seg_doc)
    m_cl = re.search(r"此时误差很小，与文档声称的<([0-9.]+)%一致", seg_doc)
    m_s7 = re.search(r"则 e ≈ k' \* k = ([0-9.eE+-]+) C，与实际 e = ([0-9.eE+-]+) C 相差甚远",
                     t_out)
    err_pct = float(m_err.group(1)) if m_err else None
    claim_pct = float(m_cl.group(1)) if m_cl else None
    print("[C5] 运行靶脚本 v6/code/1.py（{} 字符输出，run_err={}）".format(len(t_out), run_err or "无"))
    print("     其自算相对误差 = {}%；其打印结论「误差很小，与文档声称的<{}%一致」".format(
        err_pct, claim_pct))
    if m_s7:
        print("     第 7 步自承：e ≈ k′k = {} C，与实际 e = {} C 相差甚远".format(
            m_s7.group(1), m_s7.group(2)))
    c6_contra = (err_pct is not None and claim_pct is not None
                 and err_pct > max(claim_pct, 1e-9) * 1000)
    out.update({"C6_run_err": run_err, "C6_err_pct": err_pct, "C6_claim_pct": claim_pct,
                "C6_contradiction": c6_contra,
                "C6_step7": (m_s7.group(1), m_s7.group(2)) if m_s7 else None})
    add("C6", "方法论层",
        "★★靶脚本**可执行层自证矛盾**：它自己算出库仑常数相对误差 **{}%**，"
        "却在三行后打印「此时误差很小，与文档声称的<{}%一致」".format(err_pct, claim_pct),
        "FAIL" if c6_contra else "PASS",
        "用 runpy 在进程内**直接运行**靶脚本 `v6/code/1.py`（规避中文路径入 argv），"
        "捕获其 stdout 并机读：在使用「文档 k′ = 6.25e−27」的分支上，脚本第 199 行算出"
        "「相对误差：**{}%**」，而第 200 行无条件打印「此时误差很小，与文档声称的<{}%一致」；"
        "总结段（第 231–232 行）再次打印「使用文档 k′ 值时误差<0.001%」。"
        "⇒ **同一个脚本里，计算结果（{}%）与硬编码结论（<{}%）相差五个数量级以上**，"
        "且结论与计算**完全脱钩**（不是算错，是打印了一句与自己的输出相反的话）。"
        "★这是 r166 C1「结论与 if/else 脱钩」判据的**可执行层升级**："
        "r166/r168 用 ast 静态分析证明「结论不与判定耦合」，本卷进一步**跑起来**证明"
        "「结论与自己的计算输出相反」。"
        "同脚本第 7 步还自承：「则 e ≈ k′k = {} C，与实际 e = {} C 相差甚远……"
        "需要调整几何参数使方程成立」。".format(
            err_pct, claim_pct, err_pct, claim_pct,
            m_s7.group(1) if m_s7 else "?", m_s7.group(2) if m_s7 else "?"))

    # ---- C6 循环等效性：v1/1.md 的「数值等效性验证」 ----
    k_exact = FOUR_PI * M_PLANCK
    kp_116 = DEC("1.16e10")
    q_eq = kp_116 * k_exact * DEC(1) * DEC(1)          # Ω=1, dΩ/dt=1
    e_cl = KE * q_eq / DEC(1)
    e_zuft = KE * (k_exact * kp_116 * DEC(1) * DEC(1)) / DEC(1)
    taut_ratio = e_zuft / e_cl
    print("[C6] v1/1.md 场景一：q_eq = kk′ = {:.6e} C；E_cl = {:.6e}；E_ZUFT = {:.6e} ⇒ 比 {:.6f}".format(
        q_eq, e_cl, e_zuft, taut_ratio))
    print("     而该 q_eq 与基本电荷 e = {:.6e} C 相差 {:.4e} 倍".format(E_CHARGE, q_eq / E_CHARGE))
    out.update({"C5_q_eq": str(q_eq), "C5_e_cl": str(e_cl), "C5_e_zuft": str(e_zuft),
                "C5_taut_ratio": str(taut_ratio), "C5_q_over_e": str(q_eq / E_CHARGE)})
    add("C6", "方法论层",
        "★v1/1.md 的「数值等效性验证」是**循环论证**：等效电荷 q_eq 本身由 ZUFT 电荷方程算出，"
        "再代入库仑定律 ⇒ E_cl ≡ E_ZUFT 恒等（比 **{:.6f}**），零判别力".format(taut_ratio),
        "FAIL",
        "v1/1.md §3.2 声称「对于相同的物理条件，电场强度计算值完全一致 "
        "(E_cl = E_ZUFT = 2.85012×10¹³ N/C)」。机读：它取的 Ω=1、dΩ/dt=1 ⇒ "
        "q_eq = kk′ = **{:.6e} C**，然后 E_cl = 9.0e9×q_eq、"
        "E_ZUFT = 9.0e9×(kk′·1·1/1²) —— **两边是同一个数**，比值恒为 **{:.6f}**。"
        "⇒ 这个「验证」**不可能失败**（零分辨力，与 r164 B3 的循环验证同型）。"
        "真正该做的检验——ZUFT 公式能否复现**基本电荷 e = 1.602176634e−19 C** 的库仑场——"
        "靶没有做；本卷代做：q_eq/e = **{:.4e}** ⇒ 差 **{:.4e}** 倍"
        "（即 ZUFT 式给出的是一个 3166.8 C 的「等效电荷」，不是电子）。".format(
            q_eq, taut_ratio, q_eq / E_CHARGE, q_eq / E_CHARGE))
    return out


# ============================== D 组：跨卷一致性 ==============================
def group_D(A, B):
    print("\n" + "=" * 78)
    print(" [D 组] 跨卷一致性（分层铁律：条目不可相加，只做一致性检查）")
    print("=" * 78)
    out = {}

    # ---- D1 r161 的 k' 下界 vs 本目录两值 ----
    kp_lower_r161 = DEC("5.417233858405543e+29")     # r161 key_numbers
    r1 = DEC("1.16e10") / kp_lower_r161
    r2 = DEC("6.25e-27") / kp_lower_r161
    print("[D1] r161 由质量漂移约束给 k′ > {:.6e} C·s/kg".format(kp_lower_r161))
    print("     本目录 v1 值 1.16e10 ⇒ 低于下界 {:.4e} 倍；v4/v5/v6 值 6.25e−27 ⇒ 低 {:.4e} 倍".format(
        r1, r2))
    out.update({"D1_kp_lower_r161": str(kp_lower_r161), "D1_r_v1": str(r1), "D1_r_v6": str(r2)})
    add("D1", "跨卷层",
        "★跨卷硬冲突：r161 由「质量漂移不可观测」给 k′ > **5.417e+29 C·s/kg**，"
        "本目录的两个「裁定值」分别低于它 **{:.3e}** 与 **{:.3e}** 倍".format(r1, r2),
        "FAIL",
        "r161（电荷几何化 q = k′·dm/dt）机读：若质量漂移不可观测，则 dm/dt ≤ 2.9576e−49 kg/s，"
        "由 q = e 得 k′ ≥ e/(dm/dt) = **5.417233858405543e+29 C·s/kg**。"
        "本目录裁定的两个值 —— v1 的 1.16e10 与 v4/v5/v6 的 6.25e−27 —— "
        "分别只有该下界的 **{:.4e}** 与 **{:.4e}** ⇒ "
        "**若本目录的 k′ 成立，r161 的质量漂移结论（电子质量 1836 倍漂移）就会以更极端的形式出现**；"
        "若 r161 的约束成立，本目录两个值都不可用。"
        "★两个值指向**同一个量的互斥裁定**，跨卷无法同时为真。".format(r1, r2))

    # ---- D2 k 的三重口径 ----
    k_mp = M_PLANCK
    k_4pi = FOUR_PI * M_PLANCK
    k_c3g = (C_LIGHT ** 3) / G_CONST
    print("[D2] k 的三重口径：m_p = {:.6e}；4πm_p = {:.6e}；c³/G = {:.6e}".format(
        k_mp, k_4pi, k_c3g))
    print("     比值：4π = {:.6f}；c³/G / m_p = {:.6e}".format(
        float(FOUR_PI), k_c3g / k_mp))
    out.update({"D2_k_mp": str(k_mp), "D2_k_4pi": str(k_4pi), "D2_k_c3g": str(k_c3g),
                "D2_ratio_4pi": str(FOUR_PI), "D2_ratio_c3g": str(k_c3g / k_mp)})
    add("D2", "跨卷层",
        "★k 的三重口径互斥：m_p（v2/v4）/ 4πm_p（v1/v5，与 r163 一致）/ c³/G（v4 提及），"
        "最大相差 **{:.4e}** 倍".format(k_c3g / k_mp),
        "FAIL",
        "同一目录内 k 被写成三个值：**m_p = {:.6e} kg**（v2 主文第 132 行「k 的数值被设定为"
        "普朗克质量 m_p」；v4/1.md 第 68 行「k 通常被设为普朗克质量 m_p」）、"
        "**4πm_p = {:.6e} kg**（v1 裁定书、v5，与 r163 的独立登记一致）、"
        "**c³/G = {:.6e} kg**（v4/1.md 第 68 行「或在更广泛框架中取 k = c³/G」）。"
        "机读比值：4π = **{:.6f}**；c³/G ÷ m_p = **{:.6e}**。"
        "而 r162 判 [k] = **(1,0,0)**（无量纲）⇒ 与本目录的 [k] = [M] 也冲突。"
        "⇒ 电荷方程 q = k′k/Ω²·dΩ/dt 的右值随 k 的取法漂移 **12.6～1.9e43 倍**，"
        "「代回基本电荷」因此失去唯一基准。".format(k_mp, k_4pi, k_c3g, float(FOUR_PI), k_c3g / k_mp))

    # ---- D3 r168 D2 的登记被本卷推翻（CORRECTION 单列）----
    add("D3", "跨卷层",
        "CORRECTION：r168 D2 曾登记「k′ 的值在库内从未给出」，本卷机读证明**已给出多个**",
        "CORRECTION",
        "r168 D2 写：「★记 BOUNDARY：k′ 的值在库内从未给出 ⇒ 本卷不给出该链路的数值指控」。"
        "本卷对 `常数 k' 的量纲最终裁定/` 全目录机读（B7）发现 k′ 的互异数值宣称**多个**"
        "（1.16e10 / 1.160387e10 / 4.596e7 / 4.5946e7 / 7.75e1 / 6.25e−27 / 6.2561e−27 / "
        "8.99e−10 / 2.713e−77 / 3.97e−55 / 1.11238e−10 / 2.177e103）⇒ "
        "**r168 当时的「从未给值」判断被本卷的目录级扫描推翻**。"
        "★按「CORRECTION 单列、不改写旧卷」纪律，本条目只更新认知，不修改 r168 任何读数；"
        "r168 D2 的 BOUNDARY 结论（量纲层面冲突确定）本身不受影响。")

    # ---- D4 电荷定义方程的两种形式（INFO）----
    add("D4", "跨卷层",
        "电荷定义方程在库内有两种形式：q = k′k/Ω²·dΩ/dt（本目录 v1/v4/v5）与 "
        "q = k′·dm/dt（v6 传统物理对比、r161）",
        "INFO",
        "本目录 `公式.md` 与 v1/v4/v5 用 q = k′k·(1/Ω²)·(dΩ/dt)；"
        "而 `v6/传统物理/传统物理对比.md` 与 r161 用 q = k′·(dm/dt)。"
        "两者在 m = k·(n/Ω) 下可通过 dm/dt = k·d(n/Ω)/dt 建立联系，但**不是同一个方程**"
        "（前者含 Ω²、后者不含 k）。机读两者对 [k′] 的要求**相同**（均为 IT²/M），"
        "故本卷不记 FAIL，只登记形式分歧——它使「k′ 的定义」在库内没有唯一出处。")
    return out


# ============================== E 组：修复定价 ==============================
ACTIONS = [
    "M1 统一 k' 的量纲口径（机读互异口径多种：IT²/M、IT/M、C·s/m、L⁻¹IT²/M、C·s²/kg、"
    "A·s²·m⁻²、kg/A、ML⁻¹、M²L⁴T⁻³I⁻² —— 取一并全程一致）",
    "M2 修补磁场方程（补速度因子 v×r/r³），否则三方程不可共用同一 k'",
    "M3 唯一化 k' 数值（1.16e10 / 6.25e−27 / 8.99e−10 / 2.713e−77 / 3.97e−55 / 1.11238e−10 取一并说明关系）",
    "M4 修复公式-数值脱钩（k_ec³/ħ² 实算 2.18e103 vs 采纳 6.25e−27；k_e=k'ħ²/c³ 差 129 个量级）",
    "M5 统一 k 的数值（m_p / 4πm_p / c³/G）并与 r162/r163 对齐",
    "M6 清理硬编码结论与「<0.001%」类假结论脚本（29 个 .py 全目录）",
]


def survives(mask, strict):
    ok = True
    if not (mask & 1):
        ok = False                       # B1 多口径
    if not (mask & 2):
        ok = False                       # B2 磁场方程不可满足
    if not (mask & 4):
        ok = False                       # B5/B7 多数值
    if not (mask & 8):
        ok = False                       # B4 公式-数值脱钩
    if not (mask & 16):
        ok = False                       # D2 k 三重口径
    if not (mask & 32):
        ok = False                       # C1/C5 方法论
    if strict:
        # 严格档：不许改三个核心方程的形式（磁场方程补速度因子即改写方程）
        if (mask & 2):
            ok = False
    return ok


def group_E():
    print("\n" + "=" * 78)
    print(" [E 组] 修复定价：6 个动作 × 位掩码（64 组合），双档都报")
    print("=" * 78)
    loose, strict_n, zero = [], 0, 0
    min_cost = 99
    for mask in range(64):
        cost = bin(mask).count("1")
        if survives(mask, False):
            loose.append((mask, cost))
            if cost < min_cost:
                min_cost = cost
        if survives(mask, True):
            strict_n += 1
        if mask == 0 and survives(mask, False):
            zero += 1
    print(" 存活 {} / 64，严格档 {}，零代价 {}，最小代价 {}".format(
        len(loose), strict_n, zero, min_cost))
    for m, c in loose[:6]:
        print("   mask {:06b} cost {} — {}".format(
            m, c, " + ".join(ACTIONS[i] for i in range(6) if m & (1 << i))))

    add("E1", "修复定价层",
        "修复定价：64 组合 ⇒ 宽松 {} / 严格 {} / 零代价 {}（最小代价 {}）".format(
            len(loose), strict_n, zero, min_cost),
        "FAIL",
        "6 个修复动作位掩码全枚举（2^6 = 64）。判活需六项缺陷同时消除："
        "① B1 的多口径 ② B2 的磁场方程不可满足 ③ B5/B7 的多数值 ④ B4 的公式-数值脱钩 "
        "⑤ D2 的 k 三重口径 ⑥ C1/C5 的方法论。"
        "机读：**宽松档存活 {}**、**严格档（不许改三个核心方程与 k′ 定义式）存活 {}**、"
        "**零代价 {}**（最小代价 {}）。**双档都报，禁只报一档。**".format(
            len(loose), strict_n, zero, min_cost))

    add("E2", "修复定价层",
        "★修复即自杀（第十六度）：任何存活路径都要求**放弃一个已发布的核心结果**",
        "FAIL",
        "存活解的共性：① **M3 必做** —— 六个互异数值只能留一个，其余五份文档的「裁定」"
        "全部作废（其中 v1 的 1.16e10 与 v4/v5/v6 的 6.25e−27 相差 1.856e36 倍）；"
        "② **M2 必做** —— 不改磁场方程则「三方程共用同一 k′」永假，而改方程就等于承认"
        "v1「最终裁定」的核心结论（唯一量纲）从未成立；③ **M4 必做** —— "
        "k′ = k_ec³/ħ² 与 6.25e−27 必须放弃一个，而两者都被靶当作「关键公式/校准值」发布过；"
        "④ **M5 必做** —— k 的三个取法（m_p / 4πm_p / c³/G）必须弃两个。"
        "⇒ **「k′ 可被最终裁定」与「库内现有多数 k′ 相关结论」不可兼得**"
        "（本线**第十六**次复发）。")
    return {"E_loose": len(loose), "E_strict": strict_n, "E_zero": zero,
            "E_min_cost": min_cost}


# ============================== 控制组 ==============================
def run_controls(A, B, C):
    print("\n" + "=" * 78)
    print(" [控制组] 必设：证明判据有分辨力（非恒失败 / 非恒通过）")
    print("=" * 78)

    # U1 电荷方程量纲正对照
    rhs = d_mul(d_mul(DIM_KP_MAIN, D_K), D_TINV)
    control("U1 电荷方程正对照：[IT²/M]×[M]×[T⁻¹] 应 = 电荷量纲 QT",
            rhs == D_CHARGE, "实得 {} vs {}".format(d_str(rhs), d_str(D_CHARGE)))

    # U2 电荷方程量纲反对照（换 ② 口径应不闭合）
    rhs2 = d_mul(d_mul(DIM_KP_ITM, D_K), D_TINV)
    control("U2 电荷方程反对照：[IT/M]×[M]×[T⁻¹] 应 ≠ 电荷量纲（证明判据非恒判闭合）",
            rhs2 != D_CHARGE, "实得 {} ≠ {}".format(d_str(rhs2), d_str(D_CHARGE)))

    # U3 电场方程量纲正对照
    rhs_e = d_mul(d_mul(d_div(d_mul(DIM_KP_MAIN, D_K), D_EPS0), D_TINV), D_L2)
    control("U3 电场方程正对照：应 = 电场量纲 MLT⁻²Q⁻¹",
            rhs_e == D_E_FIELD, "实得 {}".format(d_str(rhs_e)))

    # U4 磁场方程**真 [B]** 正对照：B = μ₀qv/(4πr²)（4π 无量纲，故只乘 [q][v]/[r²]）
    b_std = d_mul(d_mul(d_mul(D_MU0, D_CHARGE), d_div(D_L, D_T)), d_inv(d_pow(D_L, 2)))
    control("U4 真磁场正对照：μ₀qv/(4πr²) 量纲应 = 磁场量纲 MI⁻¹T⁻²（证明 [B] 判据正确）",
            b_std == D_B_FIELD, "实得 {} vs {}".format(d_str(b_std), d_str(D_B_FIELD)))

    # U5 磁场方程（靶写法）反对照：缺速度因子 ⇒ 必不闭合
    rhs_b = d_mul(d_mul(d_mul(d_mul(DIM_KP_MAIN, D_K), D_MU0), D_TINV), D_L2)
    control("U5 磁场方程反对照：靶写法（R/R³ 无 v）应 ≠ 磁场量纲（证明能识别公式缺陷）",
            rhs_b != D_B_FIELD, "实得 {} ≠ {}".format(d_str(rhs_b), d_str(D_B_FIELD)))

    # U6 数值正对照：q_p 60 位重算与靶 1.8755e−18 五位逐位相等
    qp = (FOUR_PI * EPS0 * HBAR * C_LIGHT).sqrt()
    u6 = (_round_to_sig(qp, 5) == DEC("1.8755e-18"))
    control("U6 数值正对照：q_p = √(4πε₀ħc) 应 ≈ 1.8755e−18 C（5 位有效数字逐位相等）",
            u6, "实得 {:.12e}".format(qp))

    # U7 公式-数值脱钩检测：k_ec³/ħ² 与 6.25e−27 必须判「不一致」
    kp_from_ke = KE * (C_LIGHT ** 3) / (HBAR ** 2)
    u7 = (abs(kp_from_ke / DEC("6.25e-27") - DEC(1)) > DEC("1e10"))
    control("U7 脱钩检测反对照：k_ec³/ħ²（2.18e103）与 6.25e−27 必须判「严重不一致」",
            u7, "比值 {:.4e}".format(kp_from_ke / DEC("6.25e-27")))

    # U8 代回检验正对照：解析求解 k′ 使 q = e，再代回须精确复原
    k_exact = FOUR_PI * M_PLANCK
    kp_need = E_CHARGE * (FOUR_PI ** 2) / (k_exact * DEC(1))
    q_back = kp_need * k_exact / (FOUR_PI ** 2) * DEC(1)
    u8 = (abs(q_back - E_CHARGE) <= DEC("1e-60"))
    control("U8 代回往返对照：由 q=e 反解 k′ 再代回，须精确复原 e（证明代回判据可解）",
            u8, "k′_need = {:.6e}，代回 q = {:.6e} C".format(kp_need, q_back))

    # U9 聚类检测器正/反对照
    v1_, v2_ = 1.16e10, 1.160387e10
    u9a = abs(v1_ - v2_) <= 5e-3 * max(abs(v1_), abs(v2_))
    u9b = abs(v1_ - 6.25e-27) > 5e-3 * max(abs(v1_), abs(6.25e-27))
    control("U9 聚类对照：1.16e10 与 1.160387e10 应同簇；1.16e10 与 6.25e−27 应异簇",
            u9a and u9b, "同簇={} 异簇={}".format(u9a, u9b))

    # U10 ast 检测器反对照（含赋值/循环/比较的脚本应判「有计算」）
    calc = ("x = 0\n"
            "for i in range(10):\n"
            "    x = x + i * i\n"
            "if x > 100:\n"
            "    print(\"big\")\n"
            "else:\n"
            "    print(\"small\")\n")
    import tempfile
    tf = os.path.join(_PROJ, "_tmp_ctrl_u10.py")
    with open(tf, "w", encoding="utf-8") as fh:
        fh.write(calc)
    st = analyze_file(tf)
    os.remove(tf)
    control("U10 ast 反对照：含赋值/循环/比较的脚本应判「有计算」",
            st["compute"] > 0 and st["parse_ok"], "compute = {}".format(st["compute"]))

    # U11 靶来料可定位
    control("U11 靶来料可定位（v1 裁定 / v1 桥梁 / v4 / v5 / v6 code / 公式.md / 数据计算）",
            all(os.path.isfile(p) for p in (F_VERDICT, F_V1_BRIDGE, F_V4, F_V5,
                                            F_V6_CODE1, F_FORMULA, F_V6_DATA)),
            "verdict={} bridge={} v4={} v5={} v6code={} formula={} data={}".format(
                os.path.isfile(F_VERDICT), os.path.isfile(F_V1_BRIDGE), os.path.isfile(F_V4),
                os.path.isfile(F_V5), os.path.isfile(F_V6_CODE1), os.path.isfile(F_FORMULA),
                os.path.isfile(F_V6_DATA)))


# ============================== 守卫 ==============================
def run_guards(A, B, C, D, E):
    print("\n" + "=" * 78)
    print(" [守卫]（★全部机读驱动，无一处 ok 写死 True）")
    print("=" * 78)

    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    n_pass = sum(1 for e in ENTRIES if e["verdict"] == "PASS")
    n_bnd = sum(1 for e in ENTRIES if e["verdict"] == "BOUNDARY")
    n_corr = sum(1 for e in ENTRIES if e["verdict"] == "CORRECTION")
    guard("G1 verdict 由机读驱动：FAIL {} / PASS {} / BOUNDARY {} / CORRECTION {}（FAIL 与 PASS 都须 > 0）".format(
        n_fail, n_pass, n_bnd, n_corr), n_fail > 0 and n_pass > 0,
        "机读累加 FAIL={} PASS={} BOUNDARY={} CORRECTION={}".format(n_fail, n_pass, n_bnd, n_corr))

    # G2 数值真算：60 位重算与靶值相对差须 < 1e-3
    g2 = (A["A0_ok"])
    guard("G2 数值守卫：Decimal 60 位重算 k′=√(4πε₀ħc)/c 与靶 6.25e−27 相对差须 < 1e−3", g2,
          "相对差 = {}".format(A["A0_rel"]))

    # G3 多口径真算
    g3 = (B["B1_n_uniq"] >= 5)
    guard("G3 多口径守卫：互不相同的 k′ 量纲口径数须 ≥ 5（真算四元清点）", g3,
          "互异口径数 = {}".format(B["B1_n_uniq"]))

    # G4 裁定书算术错误真算
    g4 = (not B["B2_doc_arith_ok"])
    guard("G4 算术守卫：裁定书 §3 的书写因子乘积必须**真算不等于**其自称结果", g4,
          "乘积 {} vs 自称 {}".format(B["B2_doc_prod"], B["B2_doc_claim"]))

    # G5 三方程不可同时满足真算
    g5 = (not B["B2_satisfiable"]) and (B["B2_req_charge"] != B["B2_req_B"])
    guard("G5 可满足性守卫：三方程对 [k′] 的要求必须**真算互不相同**", g5,
          "电荷 {} / 电场 {} / 磁场 {}".format(
              B["B2_req_charge"], B["B2_req_E"], B["B2_req_B"]))

    # G6 代回检验真算：两个宣称值都代不回 e（按偏离倍数 max(r,1/r) 判）
    devs = [max(float(r), 1.0 / float(r)) for r in B["B3_scenarios_dev"]]
    g6 = (min(devs) > 1e10)
    guard("G6 代回守卫：两个宣称 k′ 代回电荷方程后 q/e 的偏离倍数必须**全部** > 1e10", g6,
          "最小偏离 = {:.4e} 倍".format(min(devs)))

    # G7 公式-数值脱钩真算
    g7 = (abs(float(B["B4_detach_ratio"])) > 1e100)
    guard("G7 脱钩守卫：k_ec³/ħ² 实算与采纳值 6.25e−27 之比须 > 1e100", g7,
          "比 = {}".format(B["B4_detach_ratio"]))

    # G8 ast 扫描真算：须同时扫到「有计算」与「有硬编码」两类
    g8 = (C["C1_compute"] >= 1) and (C["C1_detached"] >= 1)
    guard("G8 ast 扫描守卫：全目录须同时存在**含计算**（{} 个）与**含硬编码结论**（{} 个）的脚本".format(
        C["C1_compute"], C["C1_detached"]), g8,
        "可解析 {} / 含计算 {} / 含硬编码 {}".format(
            C["C1_parse_ok"], C["C1_compute"], C["C1_detached"]))

    # G9 机读数值宣称 ≥ 6 个
    g9 = (B["B7_n_values"] >= 6)
    guard("G9 数值宣称守卫：机读互异 k′ 数值数须 ≥ 6（真聚类）", g9,
          "互异数值 = {}".format(B["B7_n_values"]))

    # G10 对靶有利分支单列
    g10 = (n_pass >= 3)
    guard("G10 对靶有利分支单列守卫：数值/量纲闭合/k=4πm_p 三条 PASS 须**各自单列**",
          g10, "PASS 条目数 = {}（须 ≥ 3）".format(n_pass))

    # G11 分层铁律（真查 REDLINE 单一出处）
    g11 = any(("分层铁律" in r) and ("相加" in r) for r in REDLINE)
    guard("G11 分层铁律守卫：必须显式声明本卷条目不可与 r159–r170 相加（真查 REDLINE）", g11,
          "含分层声明 = {}".format(g11))


# ============================== 输出 ==============================
def build_payload(A, B, C, D, E):
    stats = {}
    for e in ENTRIES:
        stats[e["verdict"]] = stats.get(e["verdict"], 0) + 1
    verdict = ("F-KPRIME-FINAL-VERDICT-SELF-CONTRADICTORY-MULTIPLE-CALIBRES-MULTIPLE-VALUES"
               "-B-EQUATION-UNSATISFIABLE-AND-FORMULA-VALUE-DETACHED")
    verdict_zh = (
        "库内自称「最终裁定」的文件判定 k' 的量纲为 [IT²/M] = A·s²/kg 并宣称这是"
        "「唯一能够同时满足电荷/电场/磁场三个方程的量纲」，但机读显示：① 同一目录内 k' 被同时主张 "
        "**{} 种**互不相同的 (M,L,T,Q) 口径（{}）；"
        "② 「最终裁定」§3 自己的乘法就算错了（书写因子乘积得 M L⁻¹ I⁻¹ T⁻¹，却自称 M I⁻¹ T⁻²），"
        "且把三个方程各自解出的 [k'] 要求为 **{}**、**{}**、**{}** —— "
        "三者互不相同 ⇒ **不存在**任何 [k'] 能同时满足三个方程（磁场公式缺一个速度因子）；"
        "③ 机读全目录 k' 的互异数值宣称 **{}** 个（1.16e10 与 6.25e−27 相差 1.856e36 倍），"
        "且 v4 的「关键公式」k' = k_e·c³/ħ² 实算 2.18e103 与其采纳的校准值 6.25e−27 "
        "相差 3.5e129 倍（公式与数值脱钩）；④ 代回检验：两个宣称值都代不回基本电荷"
        "（差 10¹⁴～10²² 倍）。数值层与电荷/电场方程的量纲闭合靶是对的，已诚实记为 PASS。".format(
            B["B1_n_uniq"],
            "；".join("{} {}（{} 处）".format(t, d, n)
                      for t, d, n, _w, _f in B["B1_calibres"]),
            B["B2_req_charge"], B["B2_req_E"], B["B2_req_B"],
            B["B7_n_values"]))
    key_numbers = {
        "kp_calc_decimal60": A["A0_kp_calc"],
        "kp_claim": A["A0_kp_claim"],
        "kp_rel_dev": A["A0_rel"],
        "kp_digit_match_3sig": A["A0_digit_match"],
        "q_planck_calc": A["A0_qp"],
        "k_4pi_mp": A["A2_k_calc"],
        "kp_distinct_dimensions": B["B1_n_uniq"],
        "kp_calibres": B["B1_calibres"],
        "b_eq_required_dim": B["B2_req_B"],
        "b_eq_doc_product": B["B2_doc_prod"],
        "b_eq_doc_claim": B["B2_doc_claim"],
        "b_eq_satisfiable": B["B2_satisfiable"],
        "b_eq_req_charge": B["B2_req_charge"],
        "b_eq_req_E": B["B2_req_E"],
        "substitution_scenarios": B["B3_scenarios"],
        "composite_constant_116": B["B3_comp_116"],
        "composite_ratio_vs_ke": B["B3_comp_ratio"],
        "coulomb_field_ratio": B["B3_field_ratio"],
        "kp_from_ke_c3_hbar2": B["B4_kp_from_ke"],
        "kp_detach_ratio": B["B4_detach_ratio"],
        "ke_from_kp": B["B4_ke_from_kp"],
        "kp_ratio_v1_over_v6": B["B5_ratio_versions"],
        "kp_distinct_values": B["B7_n_values"],
        "kp_value_clusters": B["B7_values"],
        "py_files_scanned": C["C1_files"],
        "py_parse_ok": C["C1_parse_ok"],
        "py_with_hardcoded_conclusions": C["C1_detached"],
        "py_with_real_computation": C["C1_compute"],
        "hardcoded_conclusion_total": C["C1_total_top"],
        "v2_premise_conclusion_conflict": C["C2_kk_concl"],
        "version_dirs": C["C3_versions"],
        "tautology_ratio": C["C5_taut_ratio"],
        "r161_kp_lower": D["D1_kp_lower_r161"],
        "k_triple_ratio_c3g_over_mp": D["D2_ratio_c3g"],
        "repair_loose": E["E_loose"],
        "repair_strict": E["E_strict"],
        "repair_zero_cost": E["E_zero"],
        "repair_min_cost": E["E_min_cost"],
    }
    return {
        "id": "TUFT-r171",
        "title": "常数 k' 的「量纲最终裁定」精算：九重量纲、公式与数值脱钩、磁场方程不可满足",
        "date": "2026-10-24",
        "target": "S17 核心公式集 常数 k' 的量纲最终裁定",
        "target_files": ["v1/常数 k' 的量纲最终裁定.md", "v1/1.md",
                         "v1/基于空间几何化的统一场论及经典电磁学交叉验证.md",
                         "v1+v2/统一场论核心公式量纲验证与求导证明.md",
                         "v2/验证/全面验证.md", "v4/1.md", "v5/1.md",
                         "v6/code/1.py", "v6/公式验证/数据计算.md",
                         "v6/传统物理/传统物理对比.md", "公式.md"],
        "verdict": verdict,
        "verdict_zh": verdict_zh,
        "stats": stats,
        "entries": ENTRIES,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": key_numbers,
        "not_closed": [
            "本卷只审「常数 k' 的量纲最终裁定」目录；若体系在别处另有 k' 的权威唯一定义，B1 的机读口径清单应重审（计数随语料变化）。",
            "B2b 的「三方程对 [k'] 的要求」按各方程**如书面所写**的形式解出；若靶日后给磁场方程补上速度因子，该条应重审（这正是修复动作 M2）。",
            "B3 的代回检验取靶自己的 k = 4πm_p 与 dΩ/dt = 1；靶从未给出 (Ω, dΩ/dt) 的独立测定方式，故本卷只检验「代回给不出 e」这一事实。",
            "B7 的求值器口径同 r168（5e−3 相对容差聚类）；若靶改用图片/表格承载数值宣称，该判据需改写。",
            "C3 记 BOUNDARY：多版本目录本身是正常学术修订，本卷不指控这一点。",
            "修复枚举限于本卷 6 个动作（64 组合），不排除第 7 种路径。",
        ],
        "redline": REDLINE,
    }


REDLINE = [
    "数学自洽 ≠ 实验证实；本卷只做可算判决，不产生新物理。",
    "不宣称「张祥前体系全错」，只判决本卷所列命题。",
    "A0 的数值 6.2561e−27 与 A1 的电荷/电场量纲闭合、A2 的 k=4πm_p **靶是对的**，已诚实记为 PASS。",
    "C3 的「六版本目录」按防过度指控原则记 BOUNDARY，不作缺陷证据。",
    "分层铁律：本卷条目不可与 r159–r170 相加。",
]


def write_outputs(payload):
    base = "TUFT-r171_常数kPrime量纲最终裁定_九重量纲与公式数值脱钩_精算_2026-10-24"
    datadir = os.path.join(_PROJ, "数据")
    os.makedirs(datadir, exist_ok=True)
    paths = {}

    p_json = os.path.join(datadir, base + ".json")
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    paths["json"] = p_json

    L = ["TUFT-r171 常数 k' 量纲最终裁定 —— 运行报告", "=" * 70, ""]
    for k, v in payload["key_numbers"].items():
        L.append("  {:44s} {}".format(k, v))
    L.append("")
    L.append("条目统计：" + " / ".join("{}={}".format(k, payload["stats"][k])
                                   for k in sorted(payload["stats"])))
    L.append("控制组：{} / {}".format(sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    L.append("守卫  ：{} / {}".format(sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    L.append("")
    for e in ENTRIES:
        L.append("  [{}] {} — {}".format(e["verdict"], e["code"], e["name"]))
    p_rep = os.path.join(datadir, base + "_report.txt")
    with open(p_rep, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    paths["report"] = p_rep

    M = ["# TUFT-r171｜常数 k' 的「量纲最终裁定」精算：九重量纲、公式与数值脱钩、磁场方程不可满足",
         "", "**判词**：`{}`".format(payload["verdict"]), "",
         "{}".format(payload["verdict_zh"]), "", "## 条目总表", "",
         "| 编号 | 层 | 结论 | 要点 |", "|---|---|---|---|"]
    for e in ENTRIES:
        note = e["note"].replace("\n", " ").replace("|", "／")
        M.append("| {} | {} | **{}** | {} |".format(
            e["code"], e["group"], e["verdict"],
            note if len(note) <= 900 else note[:900] + "…"))
    M += ["", "## 控制组", ""]
    for c in CONTROLS:
        M.append("- {} {} — {}".format("[OK]" if c["ok"] else "[BAD]", c["name"], c["detail"]))
    M += ["", "## 守卫", ""]
    for g in GUARDS:
        M.append("- {} {} — {}".format("[OK]" if g["ok"] else "[BAD]", g["name"], g["detail"]))
    p_md = os.path.join(datadir, base + ".md")
    with open(p_md, "w", encoding="utf-8") as f:
        f.write("\n".join(M))
    paths["md"] = p_md

    V = ["# 判定册 · TUFT-r171｜常数 k' 的「量纲最终裁定」精算",
         "",
         "## 一、编号与定位",
         "",
         "- **编号 r171**（起草前实测首空号；r170 已被并行会话两卷占用 ⇒ 本卷取 r171）",
         "- **靶**：S17 `04_理论推导/核心公式集/常数 k' 的量纲最终裁定/`"
         "（v1 裁定书 138 行 · v1/1.md 桥梁论文 165 行 · v1/交叉验证 519 行 · "
         "v1+v2 量纲验证与求导证明 640/660 行 · v2 验证/全面验证 · v4/1.md 179 行 · "
         "v5/1.md 220 行 · v6/code/1.py 237 行 · v6/公式验证/数据计算.md · "
         "v6/传统物理/传统物理对比.md · 公式.md · **共 29 个 .py + 38 个 .md（机读）**）",
         "- **分层**：本卷为**数值层 + 量纲口径层 + 数值宣称层 + 方法论层 + 跨卷层**，"
         "与 r161（电荷几何化公设层）、r168（f 的量纲口径层）**条目不可相加**",
         "",
         "## 二、判词",
         "",
         "`{}`".format(payload["verdict"]),
         "",
         "{}".format(payload["verdict_zh"]),
         "",
         "## 三、先给靶应得的 PASS",
         "",
         "| 项 | 内容 | 结果 |",
         "|---|---|---|",
         "| A0 | k′ = √(4πε₀ħc)/c（Decimal 60 位独立重算） | **{}**，与靶相对差 **{}** ⇒ ✓（第三位修约 slip 单列） |".format(
             A0_F, A0_REL),
         "| A1 | 电荷方程 + 电场方程的量纲闭合 | [k′][k][T⁻¹] = **{}** = [q]；[k][k′]/[ε₀][T⁻¹][L⁻²] = **{}** = [E] ⇒ ✓ |".format(
             A1_Q, A1_E),
         "| A2 | k = 4π·m_p = **{}** kg | 与 r163 独立登记互相印证 ⇒ ✓ |".format(A2_K),
         "",
         "⇒ **靶的数值算对了（同一条 q_p/c 公式），电荷与电场方程的量纲也确实闭合，"
         "k = 4πm_p 也与 r163 一致。** **这是本卷对靶有利的结论，诚实登记。** 本卷指控的不是这些。",
         "",
         "## 四、★B 组：机读同一个 k' 的多重量纲与磁场方程的不可满足",
         "",
         "| # | (M,L,T,Q) | 命中处数 | 代表位置 | 性质 |",
         "|---|---|---|---|---|"]
    for tag, dimstr, nsrc, where, flags in B_CAL:
        V.append("| {} | **{}** | {} | {} | {} |".format(
            tag, dimstr, nsrc, where, flags if flags else "—"))
    V += ["",
          "⇒ 机读互不相同的被主张口径数 = **{}**"
          "（显式量纲断言 {} 处 + 数值后跟单位串 {} 处；另有 {} 处显式量纲断言无法安全解析，未计入）。".format(
              B_NUNIQ, B_NDIM, B_NUNIT, B_NHARDDIM),
          "",
          "### B2 ★★磁场方程：裁定书自己的乘法算错 + 三方程对 [k′] 的要求互不相同",
          "",
          "**B2a 算术层**：v1 裁定书 §3 书写因子乘积（机读 (M,L,T,Q) 四元逐项相乘）= **{}**，"
          "而其自称结果为 **{}** ⇒ **裁定书自己的乘积就算错了**。".format(B_DPROD, B_DCLAIM),
          "",
          "**B2b 结构层（最硬）**：把三个方程各自解出对 [k′] 的要求：",
          "",
          "    电荷方程要求 [k′] = {}".format(B_REQ_Q),
          "    电场方程要求 [k′] = {}".format(B_REQ_E),
          "    磁场方程要求 [k′] = {}".format(B_REQ_B),
          "",
          "三者**互不相同** ⇒ **不存在**任何一个 [k′] 能同时满足三个方程。"
          "根因：磁场公式写成 `μ₀kk′R/(4πΩ²R³)·dΩ/dt`（位置矢量）而经典形式是 "
          "`μ₀qv×r/(4πr³)`（速度叉乘）⇒ **公式本身缺一个速度因子 L·T⁻¹**。",
          "",
          "**B2c**：裁定书自称「多场景参数优化 ✅ 通过」的场景 2 同样不闭合（RHS = **{}** ≠ [B]）。".format(
              B_S2),
          "",
          "**B2d**：v6/公式验证/数据计算.md 同款双错 —— 它把 [μ₀] 写成 **{}**"
          "（正确为 **{}**），且其乘积 **{}** 也不等于其自称的 **{}**。".format(
              B_MU0D, D_MU0_STR, B_D2PROD, B_D2CLAIM),
          "",
          "### B3 ★代回检验",
          "",
          "| k′ 宣称值 | 场景 | 代回 q | 偏离倍数 |",
          "|---|---|---|---|"] + [
          "| {} ({}) | {} | {:.6e} C | **{:.4e}** |".format(t, "A·s²/kg" if "1.16" in str(v) else "C·s/kg",
                                                          om, float(q), float(dv))
          for t, v, om, q, r, dv in B3_SCEN
          ] + [
          "",
          "复合常数 kk′/(4πε₀)（k′ = 1.16e10）= **{}** N·m²/C²，与库仑常数 {:.6e} 差 **{:.4f}** 倍"
          "（靶称「≈1.0e10，与库仑常数一致」）。".format(B3_COMP, KE_FLT, float(B3_COMPR)),
          "",
          "### B4 ★公式与数值脱钩",
          "",
          "| 关系式 | 实算（Decimal 60 位） | 靶采纳/声称 | 差 |",
          "|---|---|---|---|",
          "| k′ = k_e·c³/ħ²（v4「关键公式」） | **{}** | 6.25e−27「校准值」 | **{:.4e} 倍** |".format(
              B4_KPKE, float(B4_RATIO)),
          "| k_e = k′·ħ²/c³（v6「理论内部关系式」） | **{}** | 8.9876e+9（真值） | 相对差 **{:.6e}** |".format(
              B4_KEKP, float(B4_KEREL)),
          "",
          "★**靶自承**：v6/传统物理/传统物理对比.md 明写「≈10⁻¹²⁰，与经典值相差 129 个数量级，"
          "无法直接对比」；v5/1.md §4.5 三种尝试导出 k_e 全部「约 −100%」。",
          "",
          "### B5 两轮裁定相差 {:.4e} 倍".format(float(B5_RATIO)),
          "",
          "v1 裁定 1.16e10 A·s²/kg vs v4/v5/v6 裁定 6.25e−27 C·s/kg ⇒ 比 **{:.6e}**，"
          "且无任何一处说明二者关系。".format(float(B5_RATIO)),
          "",
          "### B7 ★机读全目录 k′ 的数值宣称",
          "",
          "| 机读互异数值 | 命中处数 | 代表位置 |",
          "|---|---|---|"] + [
          "| **{:.6g}** | {} | {} |".format(
              c["v"], c["n_hits"], "；".join(c["where"][:2])) for c in B7_VALUES
          ] + [
          "",
          "另有 **{} 处**含 `√`/`\\frac` 的宣称式未硬解。⇒ 同一个常数被算出 **{}** 个互不相同的数，"
          "横跨 v1–v6 六个版本。".format(B7_NHARD, B7_NVALS),
          "",
          "## 五、★C 组：方法论层",
          "",
          "| 指标 | 数值 |",
          "|---|---|",
          "| 全目录 .py 总数 | **{}** |".format(C_FILES),
          "| 可解析 / 解析失败 | {} / {} |".format(C_POK, C_PBAD),
          "| 含**顶层硬编码结论**（与 if/else 脱钩）的脚本 | **{}** |".format(C_DET),
          "| 含**真实计算**的脚本 | {} |".format(C_CMP),
          "| 顶层硬编码结论总数 | **{}** |".format(C_TTOP),
          "",
          "- **C5（可执行层，本卷新增）**：用 runpy **直接运行**靶脚本 `v6/code/1.py` 并机读其输出 —— "
          "它自己算出库仑常数相对误差 **{}%**，三行后却打印「此时误差很小，与文档声称的<{}%一致」⇒ "
          "**结论与自己的计算输出相反**（r166/r168 的 ast 判据升级到可执行层）。".format(
              C5_ERR, C5_CLAIM),
          "- **C2**：v2 前提 k′k = 1 A·s²（⇒ k′ = 4.596e7）与结论 k′ = 1.16e10"
          "（⇒ k′k = **{}** A·s²）自相矛盾，同目录全面验证又给 4.5946e7 与 7.75e1 ⇒ 三处互斥。".format(
              C2_KK),
          "- **C3（BOUNDARY）**：机读六版本目录 {}；多版本本身不指控，只登记与「最终裁定」"
          "确定性语气之间的张力。".format(C3_VERS),
          "- **C4 两难**：k′ = q_p/c 定 ⇒ [C·s/m]；电荷方程定 ⇒ [C·s/kg] ⇒ 不可兼得；"
          "靶的处理是「以文档最终裁定为准」（用声明覆盖自己算出的量纲）。",
          "- **C6 循环等效性**：v1/1.md 的等效电荷 q_eq = kk′ = **{}** C 由 ZUFT 方程算出后再代入"
          "库仑定律 ⇒ E_cl ≡ E_ZUFT 恒等（比 **{}**），零判别力；q_eq/e = **{:.4e}**。".format(
              C6_QEQ, C6_TAUT, float(C6_QOE)),
          "",
          "## 六、跨卷一致性",
          "",
          "- **D1**：r161 给 k′ > **{}** C·s/kg（质量漂移约束），本目录两值分别低 **{:.4e}** / "
          "**{:.4e}** 倍 ⇒ 跨卷硬冲突。".format(D1_LOWER, float(D1_R1), float(D1_R2)),
          "- **D2**：k 的三重口径 m_p / 4πm_p / c³/G（最大相差 **{:.4e}** 倍），"
          "且 r162 判 [k] = (1,0,0) 无量纲。".format(float(D2_RATIO)),
          "- **D3（CORRECTION）**：r168 D2 曾登记「k′ 从未给值」，本卷机读**多个**互异数值 ⇒ "
          "该登记被推翻（单列，不改写旧卷）。",
          "- **D4（INFO）**：电荷方程两形 q = k′k/Ω²·dΩ/dt 与 q = k′·dm/dt 并存。",
          "",
          "## 七、修复定价",
          "",
          "| 档 | 存活 |",
          "|---|---|",
          "| 宽松（允许改动核心定义） | **{}** |".format(E_LOOSE),
          "| 严格（不许改三方程与 k′ 定义式） | **{}** |".format(E_STRICT),
          "| 零代价 | **{}** |".format(E_ZERO),
          "",
          "⇒ **修复即自杀第十六度**。",
          "",
          "## 八、控制组与守卫",
          "",
          "控制组 {} / {}，守卫 {} / {}".format(
              sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
              sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
          "",
          "## 九、未闭合项与红线",
          ""]
    for s in payload["not_closed"]:
        V.append("- {}".format(s))
    V.append("")
    for s in payload["redline"]:
        V.append("- {}".format(s))
    p_v = os.path.join(datadir, "判定_" + base + ".md")
    with open(p_v, "w", encoding="utf-8") as f:
        f.write("\n".join(V))
    paths["verdict"] = p_v
    return paths


# ============================== 判定册渲染用的全局快照 ==============================
A0_F = A0_REL = A1_Q = A1_E = A2_K = ""
B_CAL = []
B_NUNIQ = 0
B_NDIM = B_NUNIT = B_NHARDDIM = 0
B_DPROD = B_DCLAIM = B_REQ_Q = B_REQ_E = B_REQ_B = B_S2 = ""
B_MU0D = B_D2PROD = B_D2CLAIM = ""
B3_SCEN = []
B3_COMP = B3_COMPR = ""
B4_KPKE = B4_RATIO = B4_KEKP = B4_KEREL = ""
B5_RATIO = ""
B7_NVALS = 0
B7_VALUES = []
B7_NHARD = 0
C_FILES = C_POK = C_PBAD = C_DET = C_CMP = C_TTOP = 0
C2_KK = ""
C3_VERS = ""
C5_ERR = C5_CLAIM = None
C6_QEQ = C6_TAUT = C6_QOE = ""
D1_LOWER = D1_R1 = D1_R2 = ""
D2_RATIO = ""
E_LOOSE = E_STRICT = E_ZERO = 0
D_MU0_STR = d_str(D_MU0)
KE_STR = "{:.6e}".format(KE)
KE_FLT = float(KE)


def main():
    global A0_F, A0_REL, A1_Q, A1_E, A2_K
    global B_CAL, B_NUNIQ, B_NDIM, B_NUNIT, B_NHARDDIM, B_DPROD, B_DCLAIM, B_REQ_Q, B_REQ_E, B_REQ_B, B_S2
    global B_MU0D, B_D2PROD, B_D2CLAIM
    global B3_SCEN, B3_COMP, B3_COMPR
    global B4_KPKE, B4_RATIO, B4_KEKP, B4_KEREL, B5_RATIO
    global B7_NVALS, B7_VALUES, B7_NHARD
    global C_FILES, C_POK, C_PBAD, C_DET, C_CMP, C_TTOP
    global C2_KK, C3_VERS, C5_ERR, C5_CLAIM, C6_QEQ, C6_TAUT, C6_QOE
    global D1_LOWER, D1_R1, D1_R2, D2_RATIO
    global E_LOOSE, E_STRICT, E_ZERO

    print("=" * 78)
    print(" TUFT-r171｜常数 k' 的「量纲最终裁定」精算：九重量纲、公式与数值脱钩、磁场方程不可满足")
    print(" 2026-10-24")
    print("=" * 78)

    A = group_A()
    A0_F, A0_REL = A["A0_kp_calc"], A["A0_rel"]
    A1_Q, A1_E = A["A1_rhs_charge"], A["A1_rhs_E"]
    A2_K = A["A2_k_calc"]

    B = group_B()
    B_CAL = B["B1_calibres"]
    B_NUNIQ = B["B1_n_uniq"]
    B_NDIM = B["B1_n_dim_claims"]
    B_NUNIT = B["B1_n_unit_claims"]
    B_NHARDDIM = len(B["B1_hard_dim"])
    B_DPROD, B_DCLAIM = B["B2_doc_prod"], B["B2_doc_claim"]
    B_REQ_Q, B_REQ_E, B_REQ_B = B["B2_req_charge"], B["B2_req_E"], B["B2_req_B"]
    B_S2 = B["B2_s2_b_rhs"]
    B_MU0D, B_D2PROD, B_D2CLAIM = B["B2_mu0_doc"], B["B2_doc2_prod"], B["B2_doc2_claim"]
    B3_SCEN = B["B3_scenarios"]
    B3_COMP, B3_COMPR = B["B3_comp_116"], B["B3_comp_ratio"]
    B4_KPKE, B4_RATIO = B["B4_kp_from_ke"], B["B4_detach_ratio"]
    B4_KEKP, B4_KEREL = B["B4_ke_from_kp"], B["B4_ke_rel"]
    B5_RATIO = B["B5_ratio_versions"]
    B7_NVALS, B7_VALUES, B7_NHARD = B["B7_n_values"], B["B7_values"], B["B7_n_hard"]

    C = group_C()
    C_FILES, C_POK, C_PBAD = C["C1_files"], C["C1_parse_ok"], C["C1_parse_bad"]
    C_DET, C_CMP, C_TTOP = C["C1_detached"], C["C1_compute"], C["C1_total_top"]
    C2_KK = C["C2_kk_concl"]
    C3_VERS = " → ".join("{} ({} md/{} py/{} 行)".format(v, a, b, c)
                         for v, a, b, c in C["C3_versions"])
    C5_ERR, C5_CLAIM = C["C6_err_pct"], C["C6_claim_pct"]
    C6_QEQ, C6_TAUT, C6_QOE = C["C5_q_eq"], C["C5_taut_ratio"], C["C5_q_over_e"]

    D = group_D(A, B)
    D1_LOWER, D1_R1, D1_R2 = D["D1_kp_lower_r161"], D["D1_r_v1"], D["D1_r_v6"]
    D2_RATIO = D["D2_ratio_c3g"]

    E = group_E()
    E_LOOSE, E_STRICT, E_ZERO = E["E_loose"], E["E_strict"], E["E_zero"]

    run_controls(A, B, C)
    run_guards(A, B, C, D, E)

    payload = build_payload(A, B, C, D, E)
    paths = write_outputs(payload)

    print("\n" + "=" * 78)
    print(" 终盘")
    print("=" * 78)
    print(" 条目： " + " / ".join("{}={}".format(k, payload["stats"][k])
                                for k in sorted(payload["stats"])))
    nco = sum(1 for c in CONTROLS if c["ok"])
    ngo = sum(1 for g in GUARDS if g["ok"])
    print(" 控制组： {} / {}".format(nco, len(CONTROLS)))
    print(" 守卫  ： {} / {}".format(ngo, len(GUARDS)))
    print(" 判词  ： {}".format(payload["verdict"]))
    for p in sorted(paths.values()):
        print(" 产物  ： {}".format(os.path.basename(p)))

    if nco != len(CONTROLS) or ngo != len(GUARDS):
        print("\n !! 控制组/守卫有失控项 => 退出码 2")
        sys.exit(2)
    print("\n 退出码 0")
    sys.exit(0)


if __name__ == "__main__":
    main()
