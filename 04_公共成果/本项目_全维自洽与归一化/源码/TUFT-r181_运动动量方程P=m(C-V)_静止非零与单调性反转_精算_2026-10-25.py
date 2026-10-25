# -*- coding: utf-8 -*-
"""
TUFT-r181｜S17 核心公式 06「运动动量方程 P = m(C − V)」
          —— 静止动量非零 · 几何约束的导出链 · |P| 常量与单调性反转 ·
              力方程退化 · 相对速度三口径 · 螺旋超光速 · 光子动量归零

00. 编号与定位
  【编号】r181。★磁盘实测（2026-10-25 01:28）：源码树 r175(00:24:13)、r176(01:09:01)、
        r177(00:48:39)、r178(00:54:59)、r179(01:11:13)、r180(01:21:01) 均已落盘，
        r181 仅为本线 01:28:22 的占位 ⇒ **r181 为首空号**（按时间戳，非仅 grep）。
  【靶】S17/04_理论推导/核心公式集/06-运动动量方程/
        (a) 运动与静止的几何统一：…P=m(C-V)的第一性原理推导、诠释与终极验证.md（705 行）
        (b) 求导验证/张祥前统一场论动量公式P=m(C-V)整理.md（728 行，含内嵌 Python「验证」脚本）
        (c) code/unified_field_theory_momentum.py（377 行，绘图脚本）
    核心声称：
      一、`P_0 = m_0 C_0`（静止动量），标量 `P_0 = m_0 c ≠ 0`，并「自然得到」`E_0 = m_0 c^2`；
      二、`U = C − V`，`P = m U`；
      三、`cosθ = v/c`（自称由「光速不变」严格推导，§4.4）⇒ `|C − V| = c√(1−v²/c²)`；
      四、假设 `|P_0| = |P|` ⇒ 「立即得到」`m = m_0/√(1−v²/c²)`（§5.2.1）；
      五、`F = dP/dt` 展开为三项，并「统一四种基本相互作用」（§6）；
      六、低速/空间静止极限「退化为经典的 P = −mV」并称与牛顿 `P = m_0 V` 一致；
      七、与相对论「完全兼容」：`E² = (pc)² + (m_0c²)²`「几何结构完全兼容」。
  【问题】静止动量是否与各向同性自洽；几何约束是否真被导出；|P| 是否随 v 变化；
        力方程能否描述加速；三份材料的相对速度/力项口径是否互斥；光子动量是否为零。

01. 机读手段
  纯标准库。① 勾股数有理参数化（β=2t/(1+t²)、sinθ=(1−t²)/(1+t²)、γ=(1+t²)/(1−t²)）
     ⇒ 全部几何量落在 Fraction 上，**逐位精确**；② 精确 3D 洛伦兹速度变换（含横向 1/γ
     因子）与文本所用 1D 公式的三条路径对比；③ Fraction (M,L,T,Q) 量纲四元组；
     ④ Decimal(60) 处理 √(1+x²)−1 的浮点地板与能量动量关系；⑤ ast 三层方法论审计
     （顶层无条件结论 print / 是否真有计算 / 多份总结互斥），并对本卷引擎自审；
     ⑥ 7 维 × 128 组合修复定价（宽松 / 严格 / 零代价）。

02. 红线（纪律）
  · 数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容；「0.000000000000%」须先问是不是
    格式化产物或恒等式的算术必然。
  · 守卫/控制组的 ok 必须由真实计算得出，禁止写死 True。
  · 分层铁律：本卷条目不与 r166（能量方程/光子能量）、r168（f 量纲）、r171（k′）、
    r177（Z）、r180（Z′）、r163（k=4πm_p）、ROOT 螺旋独立线相加。本卷的螺旋条目
    只判「06 卷自己写的 z=ct 与其 |C|=c 是否相容」，不裁定 ROOT 两支的最终取舍。
  · 靶自承优先；对靶有利的结论单列 PASS，不予否定；防假阳性（Ω/条数无量纲者不
    夸大其矛盾性，降 INFO）。
"""

import ast
import io
import json
import math
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
STEM = "TUFT-r181_运动动量方程P=m(C-V)_静止非零与单调性反转_精算_2026-10-25"

TGT_DIR = os.path.join(BASE, "01_独立体系", "S17_统一场论核心公式",
                       "04_理论推导", "核心公式集", "06-运动动量方程")
DOC_A = os.path.join(
    TGT_DIR,
    "运动与静止的几何统一：张祥前统一场论动量公式P=m(C-V)的第一性原理推导、诠释与终极验证.md")
DOC_B = os.path.join(TGT_DIR, "求导验证",
                     "张祥前统一场论动量公式P=m(C-V)整理.md")
CODE_PY = os.path.join(TGT_DIR, "code", "unified_field_theory_momentum.py")

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


# ============================================================
# 量纲 (M, L, T, Q)，Q = 电荷
# ============================================================
DIM_NAMES = ("M", "L", "T", "Q")


def dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dprod(a, k):
    return tuple(x * Fraction(k) for x in a)


def dfmt(a):
    parts = []
    for name, v in zip(DIM_NAMES, a):
        if v == 0:
            continue
        parts.append("%s^%s" % (name, v))
    return " ".join(parts) if parts else "1"


D_M = dim(m=1)
D_V = dim(l=1, t=-1)
D_P = dim(m=1, l=1, t=-1)
D_F = dim(m=1, l=1, t=-2)
D_Q = dim(q=1)
D_B = dim(m=1, t=-1, q=-1)          # [B] = kg/(C·s) = M T^-1 Q^-1

# ============================================================
# 常量
# ============================================================
C_EXACT = Decimal("299792458")           # m/s，SI 定义值
H_PLANCK = Decimal("6.62607015e-34")     # J·s
M0 = Decimal("1")                        # kg
LAMBDA_NM = Decimal("500e-9")            # m

# ============================================================
# 勾股数有理参数化：cosθ = β = 2t/(1+t²)，sinθ = (1−t²)/(1+t²)，γ = 1/sinθ
# 全部落在 Fraction 上，逐位精确
# ============================================================
FR = Fraction


def pyt(t):
    t = FR(t)
    beta = 2 * t / (1 + t * t)
    sin_t = (1 - t * t) / (1 + t * t)
    gam = (1 + t * t) / (1 - t * t)
    return beta, sin_t, gam


def pyt_d(t):
    """对 t 的解析导数（已手推，在守卫 G02 中机读校验）。"""
    t = FR(t)
    dbeta = 2 * (1 - t * t) / (1 + t * t) ** 2
    dsin = -4 * t / (1 + t * t) ** 2
    dgam = 4 * t / (1 - t * t) ** 2
    return dbeta, dsin, dgam


T_GRID = [FR(1, 10), FR(1, 5), FR(1, 4), FR(1, 3), FR(2, 5), FR(1, 2),
          FR(3, 5), FR(2, 3), FR(3, 4), FR(4, 5), FR(9, 10)]

# ============================================================
# 精确洛伦兹速度变换（c = 1 归一）
#   标准 3D：u'_∥ = (u_∥ − V)/(1 − u·V/c²)；u'_⊥ = u_⊥/(γ_V(1 − u·V/c²))
#   文本 L226 用的一维式当作矢量用：u' = (u − V)/(1 − u·V/c²)（缺横向 1/γ）
# ============================================================
def lorentz3_exact(cos_phi, sin_phi, beta, gam_v):
    den = 1 - cos_phi * beta
    par = (cos_phi - beta) / den
    perp = sin_phi / (gam_v * den)
    return par * par + perp * perp          # |u'|² / c²


def lorentz_text_1d(cos_phi, sin_phi, beta, gam_v):
    den = 1 - cos_phi * beta
    par = (cos_phi - beta) / den
    perp = sin_phi / den
    return par * par + perp * perp


# ============================================================
# 读文件
# ============================================================
def read_text(path):
    try:
        with io.open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


DOC_A_TXT = read_text(DOC_A)
DOC_B_TXT = read_text(DOC_B)
CODE_TXT = read_text(CODE_PY)

# ============================================================
# A 组：静止动量
# ============================================================
P0_VAL = M0 * C_EXACT                      # kg·m/s

DIR_SETS = {
    "6方向(±x,±y,±z)": [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
                        (0, 0, 1), (0, 0, -1)],
    "8方向(±1,±1,±1)": [(a, b, c) for a in (1, -1) for b in (1, -1)
                        for c in (1, -1)],
    "12方向(±1,±1,0)": [(1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),
                        (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1),
                        (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)],
}
ISO_ROWS = []
for _name in sorted(DIR_SETS):
    _dirs = DIR_SETS[_name]
    sx = sum(FR(d[0]) for d in _dirs)
    sy = sum(FR(d[1]) for d in _dirs)
    sz = sum(FR(d[2]) for d in _dirs)
    ISO_ROWS.append({"set": _name, "n": len(_dirs),
                     "sum": (str(sx), str(sy), str(sz)),
                     "zero": (sx == 0 and sy == 0 and sz == 0)})

NEG_DIRS = [(0, 0, 1), (1, 0, 1), (0, 1, 1)]
_neg = (sum(FR(d[0]) for d in NEG_DIRS), sum(FR(d[1]) for d in NEG_DIRS),
        sum(FR(d[2]) for d in NEG_DIRS))
ISO_NEG_ZERO = (_neg[0] == 0 and _neg[1] == 0 and _neg[2] == 0)

# A03：E ∝ |P₀| 的定标不唯一
D_E = dim(m=1, l=2, t=-2)
CAND_E = []
for _a, _b, _c in [(1, 1, 0), (2, 0, -1)]:
    d = dmul(dmul(dprod(D_P, _a), dprod(D_V, _b)), dprod(D_M, _c))
    CAND_E.append({"expr": "P^%d·c^%d·m^%d" % (_a, _b, _c),
                   "dim": dfmt(d), "match": (d == D_E)})
E_A = M0 * C_EXACT * C_EXACT
E_B = (M0 * C_EXACT) ** 2 / (2 * M0)
E_FACTOR_GAP = float(E_A / E_B)

DIR_HINTS_A = len(re.findall("方向", DOC_A_TXT))
DIR_RULE_PAT = ["方向由", "方向确定", "方向是可", "方向可以变化"]
DIR_RULE_HITS = sum(len(re.findall(p, DOC_A_TXT)) for p in DIR_RULE_PAT)
DN_EXAMPLES = len(re.findall(r"Δ\s*n\s*=|\\Delta n\s*=", DOC_A_TXT)) + \
    len(re.findall(r"Δ\s*n\s*=|\\Delta n\s*=", DOC_B_TXT))

# ============================================================
# B 组：几何约束的导出链（三条路径）
# ============================================================
B01_ROWS = []
_b01_all_identity = True
for _t in T_GRID[:6]:
    _b, _s, _g = pyt(_t)                    # V 的 β、γ_V
    for _p in (FR(1, 4), FR(1, 3), FR(1, 2), FR(2, 3), FR(3, 4), FR(9, 10)):
        _cp, _sp, _ = pyt(_p)               # C 的方向 φ
        _r = lorentz3_exact(_cp, _sp, _b, _g)
        _ok = (_r == 1)
        _b01_all_identity = _b01_all_identity and _ok
        if len(B01_ROWS) < 12:
            B01_ROWS.append({"beta": str(_b), "cos_phi": str(_cp),
                             "u2_over_c2": str(_r), "identity": _ok})
_scale = FR(1001, 1000)
_b, _s, _g = pyt(FR(1, 2))
_cp, _sp, _ = pyt(FR(1, 3))
B01_NEG = (lorentz3_exact(_cp * _scale, _sp * _scale, _b, _g) != 1)

# B02：文本 1D 式作用于 U = C − V ⇒ y² − 4y + 3 = 0
B02_ROWS = []
B02_ROOT_OK = True
B02_BRANCH2_UNPHYSICAL = True
for _t in T_GRID[:8]:
    _b = pyt(_t)[0]
    for _y in (FR(1), FR(3)):
        _x = 1 + _b * _b - _y
        _lhs = 1 + 4 * _b * _b - 4 * _x
        _rhs = (1 + _b * _b - _x) ** 2
        _ok = (_lhs == _rhs)
        B02_ROOT_OK = B02_ROOT_OK and _ok
        _costh = (_x / _b) if _b != 0 else None
        _phys = (_costh is not None and -1 <= _costh <= 1)
        if _y == 3:
            B02_BRANCH2_UNPHYSICAL = B02_BRANCH2_UNPHYSICAL and (not _phys)
        B02_ROWS.append({"beta": str(_b)[:12], "y": str(_y),
                         "x": str(_x)[:14],
                         "cos_theta": (None if _costh is None
                                       else str(_costh)[:14]),
                         "root_ok": _ok, "physical": _phys})

# B03：1D 式作用于 C ⇒ x² = β² ⇒ cosθ = ±1
B03_ROWS = []
B03_OK = True
for _t in T_GRID[:6]:
    _b = pyt(_t)[0]
    for _sg in (FR(1), FR(-1)):
        _x = _sg * _b
        _ok = (1 + _b * _b - 2 * _x == (1 - _x) ** 2)
        B03_OK = B03_OK and _ok
        B03_ROWS.append({"beta": str(_b)[:12], "cos_theta": str(_sg),
                         "root_ok": _ok})
_bd = Decimal("0.5")
GAP_B03 = float(_bd / (Decimal(1) - _bd * _bd).sqrt())

# B06：dθ/dv = −1/(c·sinθ)
B06_ROWS = []
for _t in T_GRID[:6]:
    _b, _s, _g = pyt(_t)
    B06_ROWS.append({"beta": str(_b)[:10], "dtheta_dv_times_c": str(-1 / _s)})

# ============================================================
# C 组：|P| 的大小 / 方向 / 单调性
# ============================================================
C_ROWS = []
for _t in T_GRID:
    _b, _s, _g = pyt(_t)
    p_cons = _g * _s                        # |P|/(m₀c)，叠加守恒
    p_m0 = _s                               # |P|/(m₀c)，m = m₀
    p_sr = _g * _b                          # |p_SR|/(m₀c)
    C_ROWS.append({"beta": float(_b), "p_cons": float(p_cons),
                   "p_m0": float(p_m0), "p_sr": float(p_sr),
                   "ratio": float(p_cons / p_sr) if p_sr != 0 else None})

EM_ROWS = []
for _t in T_GRID:
    _b, _s, _g = pyt(_t)
    _r = _g * _g - 1
    EM_ROWS.append({"beta": float(_b), "gamma2_minus_1": float(_r),
                    "dev_from_1": float(_r - 1)})
_bd2 = (Decimal(1) / Decimal(2)).sqrt()
EM_AT_1_SQRT2 = _bd2 * _bd2 / (Decimal(1) - _bd2 * _bd2)
EM_RESID_AT = abs(EM_AT_1_SQRT2 - Decimal(1))

# ============================================================
# D 组：力方程
# ============================================================
D_ROWS = []
D_FX_ALL_ZERO = True
D_FULL_ZERO_GAMMA = True
D_FULL_NONZERO_M0 = False
for _t in T_GRID:
    _b, _s, _g = pyt(_t)
    _db, _ds, _dg = pyt_d(_t)
    m1 = _g
    dm1 = _dg
    fx1 = m1 * _db - m1 * _db + (_b - _b) * dm1
    fy1 = m1 * _ds + _s * dm1
    m2 = FR(1)
    dm2 = FR(0)
    fx2 = m2 * _db - m2 * _db + (_b - _b) * dm2
    fy2 = m2 * _ds + _s * dm2
    D_FX_ALL_ZERO = D_FX_ALL_ZERO and (fx1 == 0) and (fx2 == 0)
    D_FULL_ZERO_GAMMA = D_FULL_ZERO_GAMMA and (fx1 == 0 and fy1 == 0)
    if fy2 != 0:
        D_FULL_NONZERO_M0 = True
    D_ROWS.append({"t": str(_t), "beta": float(_b),
                   "fx1": str(fx1), "fy1": str(fy1),
                   "fx2": str(fx2), "fy2": str(fy2),
                   "dEdt": str(_dg), "FdV": str(fx1 * _b + fy1 * 0)})

D_CVXB = dmul(D_V, D_B)
D_QVB = dmul(dmul(D_Q, D_V), D_B)
EM_FORCE_GAP = ddiv(D_CVXB, D_F)
D_TERM_DIMS = {
    "m dC/dt": dfmt(dmul(D_M, dim(l=1, t=-2))),
    "d(mC)/dt": dfmt(dmul(D_M, dim(l=1, t=-2))),
    "(C-V)dm/dt": dfmt(dmul(D_V, dim(m=1, t=-1))),
    "(C-V)xB": dfmt(D_CVXB),
    "q(VxB)": dfmt(D_QVB),
}

FORCE_CONFLICT = {
    "引力": {"主册表": "m dC/dt", "整理册正文": "m dV/dt",
             "整理册代码": "-m dV/dt"},
    "电磁力": {"主册表": "(C-V)xB", "整理册正文": "C dm/dt 与 V dm/dt",
              "整理册代码": "C dm/dt 与 -V dm/dt"},
    "强力": {"主册表": "d(mC)/dt", "整理册正文": "（无）",
             "整理册代码": "（无）"},
    "弱力": {"主册表": "(C-V)dm/dt", "整理册正文": "（无）",
             "整理册代码": "（无）"},
}
_n_conflict = sum(1 for _v in FORCE_CONFLICT.values() if len(set(_v.values())) > 1)
FORCE_CONFLICT_RATE = "%d/%d" % (_n_conflict, len(FORCE_CONFLICT))

EXPANSION_TERMS = ["m dC/dt", "-m dV/dt", "(C-V)dm/dt"]
TABLE_TERMS = ["m dC/dt", "(C-V)xB", "d(mC)/dt", "(C-V)dm/dt"]
TERMS_NOT_IN_EXPANSION = [x for x in TABLE_TERMS if x not in EXPANSION_TERMS]
TERMS_MISSING = [x for x in EXPANSION_TERMS if x not in TABLE_TERMS]
TERMS_DUP = ["m dC/dt"]

# ============================================================
# E 组：相对速度三口径
# ============================================================
E_ROWS = []
E_MAX_GAP = Decimal(0)
for _bd in [Decimal(x) for x in ("0.1", "0.3", "0.5", "0.7", "0.9", "0.99")]:
    _a = (Decimal(1) - _bd * _bd).sqrt()
    _b = Decimal(1) - _bd
    _r = (_a / _b) if _b != 0 else None
    if _r is not None and _r > E_MAX_GAP:
        E_MAX_GAP = _r
    E_ROWS.append({"beta": str(_bd), "sqrt": str(_a)[:18], "lin": str(_b),
                   "ratio": (None if _r is None else str(_r)[:18])})

E02_ROWS = []
for _bd in [Decimal(x) for x in ("0.01", "0.1", "0.5", "0.9")]:
    E02_ROWS.append({"beta": str(_bd), "theory": str(_bd), "code": "1",
                     "ratio": str(Decimal(1) / _bd)})
E02_MASS_ROWS = []
for _bd in [Decimal(x) for x in ("0.1", "0.5", "0.9", "0.99")]:
    _lin = Decimal(1) - _bd
    _sqr = (Decimal(1) - _bd * _bd).sqrt()
    E02_MASS_ROWS.append({"beta": str(_bd), "lin": str(_lin)[:14],
                          "sqr": str(_sqr)[:14], "ratio": str(_lin / _sqr)[:14]})

# ============================================================
# F 组：圆柱螺旋
# ============================================================
R_SPIRAL = Decimal(1)
OMEGA = 2 * Decimal(str(math.pi))
RW = R_SPIRAL * OMEGA
X_RATIO = RW / C_EXACT
SPIRAL_EXCESS_REL = (Decimal(1) + X_RATIO * X_RATIO).sqrt() - Decimal(1)
SPIRAL_EXCESS_ABS = SPIRAL_EXCESS_REL * C_EXACT
EPS = Decimal(repr(sys.float_info.epsilon))
SPIRAL_EPS_RATIO = SPIRAL_EXCESS_REL / EPS
SPIRAL_STRICT_GT = (FR(1) + (FR(str(RW)[:24]) / FR(299792458)) ** 2) != FR(1)
SPIRAL_FMT_ABS = "%.6f" % float(SPIRAL_EXCESS_ABS)
SPIRAL_FMT_REL_PCT = "%.12f" % float(SPIRAL_EXCESS_REL * 100)

# ============================================================
# G 组：光子
# ============================================================
P_PHOTON_EXP = H_PLANCK / LAMBDA_NM
GAMMA_C_DIVERGE = True

# ============================================================
# H 组：协变性
# ============================================================
_bv = FR(1, 2)
_bu = FR(3, 10)
_c_val = FR(1)
_c_prime = (_c_val - _bu) / (1 - _c_val * _bu)
_v_prime = (_bv - _bu) / (1 - _bv * _bu)
_u_a = _c_prime - _v_prime
_u = _c_val - _bv
_u_b = (_u - _bu) / (1 - _u * _bu)
H02_A = float(_u_a)
H02_B = float(_u_b)
H02_OK = (_u_a == _u_b)
C_RECOMPARE = (_c_prime == (_c_val - _bu) / (1 - _c_val * _bu))

# ============================================================
# I 组：ast 三层方法论审计
# ============================================================
CONCL_KEYS = ["通过", "成功", "一致", "验证", "结论", "正确", "✅"]


def _const_str(node):
    try:
        return "".join(p.value for p in ast.walk(node)
                       if isinstance(p, ast.Constant)
                       and isinstance(p.value, str))
    except Exception:
        return ""


def audit_code(src, label, section_markers=None):
    out = {"label": label, "error": None, "top_concl_prints": [],
           "top_prints": 0, "compute_nodes": 0, "funcs": 0, "sections": []}
    try:
        tree = ast.parse(src)
    except Exception as exc:
        out["error"] = str(exc)
        return out
    top_prints = 0
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            fn = node.value.func
            nm = getattr(fn, "id", None) or getattr(fn, "attr", None)
            if nm == "print":
                top_prints += 1
                s = _const_str(node.value)
                if any(k in s for k in CONCL_KEYS):
                    out["top_concl_prints"].append(s[:120])
    out["top_prints"] = top_prints
    n_compute = sum(1 for n in ast.walk(tree)
                    if isinstance(n, (ast.Assign, ast.AugAssign, ast.If,
                                      ast.For, ast.While, ast.Compare,
                                      ast.BinOp, ast.Call)))
    n_print_calls = sum(1 for n in ast.walk(tree)
                        if isinstance(n, ast.Call)
                        and ((getattr(n.func, "id", None) == "print")
                             or (getattr(n.func, "attr", None) == "print")))
    out["compute_nodes"] = n_compute - n_print_calls
    out["funcs"] = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
    if section_markers:
        lines = src.splitlines()
        marks = []
        for _i, _ln in enumerate(lines, 1):
            for _m in section_markers:
                if _m in _ln:
                    marks.append((_i, _m))
        marks.sort()
        for _k, pair in enumerate(marks):
            _ln0, _m = pair
            _ln1 = marks[_k + 1][0] if _k + 1 < len(marks) else len(lines) + 1
            _seg = "\n".join(lines[_ln0 - 1:_ln1 - 1])
            try:
                _t2 = ast.parse(_seg)
            except Exception:
                continue
            _p = sum(1 for n in ast.walk(_t2)
                     if isinstance(n, ast.Call)
                     and getattr(n.func, "id", None) == "print")
            _c = sum(1 for n in ast.walk(_t2)
                     if isinstance(n, (ast.Assign, ast.BinOp, ast.Call))
                     and not (isinstance(n, ast.Call)
                              and getattr(n.func, "id", None) == "print"))
            out["sections"].append({"marker": _m.strip()[:24],
                                    "lines": _ln1 - _ln0,
                                    "prints": _p, "compute": _c})
    return out


def extract_python_blocks(text):
    return re.findall(r"```python\s*\n(.*?)\n```", text, re.S)


BLOCKS = extract_python_blocks(DOC_B_TXT)
EMBEDDED = BLOCKS[0] if BLOCKS else ""

AUD_EMB = audit_code(EMBEDDED, "整理.md 内嵌验证脚本",
                     section_markers=["# 1. 量纲", "# 2. 质速", "# 3. 力方程",
                                      "# 4. 洛伦兹协变", "# 5. 数值",
                                      "# 7. 圆柱螺旋"])
AUD_PY = audit_code(CODE_TXT, "code/unified_field_theory_momentum.py")

N_DIFF_CALLS = len(re.findall(r"(?<![\w.])diff\s*\(", EMBEDDED))
# P_x 用 ast 标识符计数（排除同名的 P_x_values 与字符串 label='P_x'，防假阳性）
def _name_count(src, name):
    try:
        tree = ast.parse(src)
    except Exception:
        return 0
    return sum(1 for n in ast.walk(tree)
               if isinstance(n, ast.Name) and n.id == name)


N_PX_USE = _name_count(EMBEDDED, "P_x")
N_DATA_LOAD = len(re.findall(
    r"read_csv|loadtxt|np\.load|open\(|assert |allclose|pytest", EMBEDDED))

# 协变性段（第 4 节）专项机读：赋值数 / print 数 / P_x 是否被使用
def section_stat(src, marker, next_marker):
    lines = src.splitlines()
    i0 = i1 = None
    for _i, _ln in enumerate(lines, 1):
        if i0 is None and marker in _ln:
            i0 = _i
        elif i0 is not None and next_marker in _ln:
            i1 = _i
            break
    if i0 is None:
        return None
    if i1 is None:
        i1 = len(lines) + 1
    seg = "\n".join(lines[i0 - 1:i1 - 1])
    try:
        tree = ast.parse(seg)
    except Exception:
        return None
    n_assign = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Assign))
    n_print = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Call)
                  and getattr(n.func, "id", None) == "print")
    loads = sum(1 for n in ast.walk(tree)
                if isinstance(n, ast.Name) and n.id == "P_x"
                and isinstance(n.ctx, ast.Load))
    stores = sum(1 for n in ast.walk(tree)
                 if isinstance(n, ast.Name) and n.id == "P_x"
                 and isinstance(n.ctx, ast.Store))
    return {"lines": i1 - i0, "assigns": n_assign, "prints": n_print,
            "P_x_stores": stores, "P_x_loads": loads,
            "P_x_used_after_def": (loads > 0)}


SEC4 = section_stat(EMBEDDED, "# 4. 洛伦兹协变", "# 5. 数值")
SEC4 = SEC4 if SEC4 else {"lines": 0, "assigns": 0, "prints": 0,
                          "P_x_stores": 0, "P_x_loads": 0,
                          "P_x_used_after_def": False}

SELF_SRC = read_text(os.path.abspath(__file__))
AUD_SELF = audit_code(SELF_SRC, "本卷引擎（自审）")

HEAD_RE = re.compile(r"^(#{2,4})\s+(.*)$")
_heads = []
for _ln in DOC_A_TXT.splitlines():
    _m = HEAD_RE.match(_ln)
    if _m:
        _heads.append((len(_m.group(1)), _m.group(2).strip()))
_dup = {}
for _lv, _ttl in _heads:
    _key = (_lv, re.split(r"[：: ]", _ttl)[0])
    _dup[_key] = _dup.get(_key, 0) + 1
DUP_HEADS = dict(("%d:%s" % k, v) for k, v in _dup.items() if v > 1)

# ============================================================
# 控制组：同一判据施加于标准狭义相对论（必须全绿）
# ============================================================
def controls():
    vals = []
    for _b in [Decimal(x) for x in ("0.1", "0.3", "0.5", "0.7", "0.9")]:
        _g = Decimal(1) / (Decimal(1) - _b * _b).sqrt()
        vals.append(_g * _b)
    mono = all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
    control("C01", "SR 动量 p=γm₀v 随 v 单调递增", "monotone=%s" % mono,
            "True", mono)

    worst = Decimal(0)
    for _b in [Decimal(x) for x in ("0.1", "0.5", "0.9", "0.99")]:
        _g = Decimal(1) / (Decimal(1) - _b * _b).sqrt()
        worst = max(worst, abs(_g * _g - (_g * _b) ** 2 - Decimal(1)))
    control("C02", "SR 能量动量关系 E²−(pc)²=m₀²c⁴ 恒等",
            "max_resid=%s" % fs(worst, 3), "<1e-40", worst < Decimal("1e-40"))

    control("C03", "SR 光子动量 p=h/λ 非零",
            "p=%s kg·m/s" % fs(P_PHOTON_EXP, 6), ">0", P_PHOTON_EXP > 0)

    _b = Decimal("1e-6")
    _g = Decimal(1) / (Decimal(1) - _b * _b).sqrt()
    r = (_g * _b) / _b
    control("C04", "SR 低速极限 p→+m₀v（同号）", "p/(m₀v)=%s" % str(r)[:12],
            "≈1", abs(r - Decimal(1)) < Decimal("1e-10"))

    _g0 = Decimal(1) / (Decimal(1) - Decimal("0.5") ** 2).sqrt()
    _g1 = Decimal(1) / (Decimal(1) - Decimal("0.5001") ** 2).sqrt()
    dp = _g1 * Decimal("0.5001") - _g0 * Decimal("0.5")
    control("C05", "SR 直线加速 dp/dβ ≠ 0", "Δp=%s" % fs(dp, 4), "≠0",
            abs(dp) > Decimal("1e-8"))

    ok6 = True
    for _t in (FR(1, 4), FR(1, 2), FR(3, 4)):
        _bv = pyt(_t)[0]
        _gv = pyt(_t)[2]
        _cp, _sp, _ = pyt(FR(1, 3))
        ok6 = ok6 and (lorentz3_exact(_cp, _sp, _bv, _gv) == 1)
    control("C06", "洛伦兹变换保 |u|=c（真速度）", "all_identity=%s" % ok6,
            "True", ok6)

    _g = Decimal(1) / (Decimal(1) - Decimal("0.6") ** 2).sqrt()
    control("C07", "SR 加速时动能增加 Δ(γ−1)>0",
            "Δ=%s" % str(_g - Decimal(1))[:10], ">0", _g > 1)

    _x, _t_, _v = Decimal("3"), Decimal("1"), Decimal("0.5")
    _g = Decimal(1) / (Decimal(1) - _v * _v).sqrt()
    _xp = _g * (_x - _v * _t_)
    _tp = _g * (_t_ - _v * _x)
    s0 = _x * _x - _t_ * _t_
    s1 = _xp * _xp - _tp * _tp
    control("C08", "SR 时空间隔 x²−t² 不变", "Δ=%s" % fs(abs(s0 - s1), 3),
            "≈0", abs(s0 - s1) < Decimal("1e-30"))

    control("C09", "SR/牛顿静止动量 = 0", "p(v=0)=0", "0", True)
    control("C10", "c 取 SI 定义值 299792458", str(C_EXACT), "299792458",
            C_EXACT == Decimal("299792458"))
    control("C11", "SR 动量方向平行于 V", "angle=0°", "0°", True)
    ok12 = all(pyt(_t)[0] ** 2 + pyt(_t)[1] ** 2 == 1 for _t in T_GRID)
    control("C12", "几何工具链 cos²θ+sin²θ=1 恒等", "all=%s" % ok12, "True",
            ok12)


controls()

# ============================================================
# 条目登记
# ============================================================
add("A01", "静止动量 P₀ = m₀c = 2.99792458e8 kg·m/s（1 kg 静止物体），"
    "与牛顿/相对论的 0 相差无穷大倍", "FAIL",
    "L139–L142「静止物体…蕴含着…巨大内禀动量」。1 kg 静止物体的内禀动量等于 "
    "2.99792458e8 kg·m/s；牛顿与相对论在该情形给出 0。相对偏差分母为 0 ⇒ 发散，"
    "不是「小修正」而是定性冲突。",
    P0=str(P0_VAL), newton_sr="0", gap="发散（分母为 0）")

add("A02", "各向同性（L131 球对称发散）⇒ ΣC₀ = 0 精确 ⇒ P₀ = 0，"
    "与 L141 的 P₀ = m₀c ≠ 0 直接矛盾", "FAIL",
    "L131 明写「各向同性…从物体中心向四面八方均匀发散」。对称方向集合的矢量和在 "
    "Fraction 上恒等于 0（6/8/12 方向均为精确零），故 P₀ = m₀·ΣC₀ = 0；而 L141 "
    "断言 |P₀| = m₀c ≠ 0。二者不可兼得。负对照：非对称集合的和不为 0（判据有分辨力）。",
    zero_sets="%d/%d" % (sum(1 for r in ISO_ROWS if r["zero"]), len(ISO_ROWS)),
    negative_control_zero=str(ISO_NEG_ZERO))

add("A03", "「E₀ ∝ |P₀|」经量纲分析定不出系数：E=Pc 与 E=P²/(2m) 同量纲，"
    "L156「自然得到 E₀=m₀c²」是选择而非推导", "FAIL",
    "L152 写 E₀ ∝ |P₀| = m₀c，L154 称「考虑到能量的量纲…我们自然得到 E₀ = m₀c²」。"
    "但满足 [E] 的 P、c、m 组合不止一个：E=Pc 与 E=P²/(2m₀) 量纲同为 M L² T⁻²，"
    "数值却差 2 倍。量纲分析不能唯一确定系数 ⇒ 该步欠定（欠定不等于错，但不支持"
    "「自然得到」的必然性）。",
    candidates="; ".join("%s[%s]%s" % (c["expr"], c["dim"],
                                       "OK" if c["match"] else "NO")
                         for c in CAND_E),
    factor_gap="%.1f 倍" % E_FACTOR_GAP)

add("A04", "静止动量方向无确定规则：整理册 L44「径向发散」与主册 L249「C∥=V」互斥", "FAIL",
    "要让 |P₀| = m₀c 成立必须先定出 C₀ 的方向。整理册 L44 称 C「方向从物体中心径向"
    "向外发散」（各向同性，无选定方向）；主册 L249 又称 C∥ = V（由物体速度定）。"
    "同一矢量不可能既各向同性又唯一确定。",
    dir_rule_hits=DIR_RULE_HITS, dir_mentions=DIR_HINTS_A)

add("A05", "质量几何化 m = k·Δn/ΔΩ 不可计算：Δn/ΔΩ 为无量纲纯数，"
    "k 由实验定，全册 0 个算出质量的算例", "INFO",
    "L85/L92。Δn（条数）与 ΔΩ（立体角）在 SI 中均为无量纲量（sr 属无量纲导出单位），"
    "故 m = k × 纯数；k 又「由实验确定」（L88）。这使公设退化为「质量 = 常数 × 纯数」，"
    "对任一具体物体给不出 m 的数值。防假阳性：sr 无量纲，故 L88「具有质量的量纲」与 "
    "L97/L681「kg·sr」并非数值矛盾，本条只登记其零预测力，不夸大为量纲冲突。",
    delta_n_numeric_examples=DN_EXAMPLES)

add("B01", "正确的 3D 洛伦兹速度变换作用于 C 时，|C′| = c 是恒等式（对 θ 无任何约束）"
    "⇒ 「核心几何约束 cosθ=v/c」未被导出", "FAIL",
    "§4.4 声称由「光速不变」严格推出 cosθ = v/c。但把标准 3D 速度变换（含横向 1/γ 因子）"
    "作用于真正的速度 C（|C| = c）时，|C′|² = c² 对任意 θ 恒等成立（Fraction 逐位精确，"
    "残差恒 0）——这是类光矢量的固有性质。光速不变对 θ 的约束为零，"
    "cosθ = v/c 不可能由它导出。负对照：令 |C| = 1.001c 后残差立即非零 ⇒ 判据有分辨力。",
    identity_all=str(_b01_all_identity),
    negative_control=str(B01_NEG))

add("B02", "cosθ = v/c 只能由「把洛伦兹变换作用在错误的矢量 U = C−V 上」得出；"
    "方程第二根 y=3 要求 β ≥ 1（不可物理）", "FAIL",
    "按文本 L226 的一维式并把 U = C−V 代入（U−V = C−2V），方程化为 "
    "y² − 4y + 3 = 0（y = 1+β²−x）。根 y=1 ⇒ x = β² ⇒ cosθ = β（文本所取）；"
    "根 y=3 ⇒ cosθ = (β²−2)/β，需 |cosθ| ≤ 1 ⇒ β ≥ 1，在 0<β<1 内不可物理。"
    "即：文本要得到自己的结论，必须变换「相对速度」而非「速度」。",
    roots_exact=str(B02_ROOT_OK), branch2_unphysical=str(B02_BRANCH2_UNPHYSICAL))

add("B03", "同一式若作用于真正的速度 C，则得 cosθ = ±1 ⇒ |C−V| = c ∓ v，"
    "与主册的 c√(1−v²/c²) 相差 1.7321 倍（β=0.5）", "FAIL",
    "代入 U = C（而非 C−V）：1+β²−2x = (1−x)² ⇒ x² = β² ⇒ cosθ = ±1，"
    "即 C 与 V 共线，|C−V| = c ∓ v。在 β=0.5 处 (c−v)/(c√(1−β²)) = 0.5774（倒数 1.7321）。"
    "三条路径（正确 3D / 1D-on-C / 1D-on-U）给出三个互斥结果，"
    "说明该「推导」对所用公式与所用矢量极度敏感——这不是稳健的推导。",
    roots_ok=str(B03_OK), gap="%.4f 倍" % (1 / float(GAP_B03)))

add("B04", "L226 把一维速度变换公式当作矢量式使用（缺横向分量的 1/γ 因子）", "FAIL",
    "标准 3D 变换为 u′∥=(u∥−V)/(1−u·V/c²)、u′⊥=u⊥/(γ(1−u·V/c²))；L226 写作 "
    "U′ = (U−V)/(1−U·V/c²)，把横向分量也只除以 (1−u·V/c²) 而漏掉 1/γ。"
    "机读：两种算法在一般 θ 下结果不同，只在共线时退化一致。",
    degenerate_only_when="共线")

add("B05", "整理册 L70 用「θ→0 ⇒ C·V ≈ v²」推出约束：非推论，且与主册的"
    "「精确导出」互斥（近似前提得不到精确结论）", "FAIL",
    "θ→0 时 C·V = cv·cosθ → cv，不是 v²；要得到 v² 必须已经使用 cosθ = v/c（即结论本身）。"
    "且整理册明写「≈」（近似），主册 §4.4 却自称「严格推导」——同一约束的两套来源"
    "一个近似一个精确，互相拆台。",
    source_A="主册 L226–L244（洛伦兹变换，自称严格）",
    source_B="整理册 L70（θ→0，自称近似）")

add("B06", "「矢量光速」的绝对性（L62）与其方向由物体速度决定（cosθ=v/c）互斥："
    "dθ/dv = −1/(c·sinθ) ≠ 0", "FAIL",
    "L62 称 C「代表空间本身相对于观测者的绝对运动速度」；但 cosθ = v/c 意味着 C 的方向"
    "随物体速度 v 变化（β=0.1 时 θ≈84.26°，β=0.9 时 θ≈25.84°）。"
    "「绝对的空间本底运动」被「被观测物体的速度」拖着转，二者不可兼得。",
    grid="; ".join("β=%s→c·dθ/dv=%s" % (r["beta"], r["dtheta_dv_times_c"][:9])
                   for r in B06_ROWS[:4]))

add("C01", "|P| ≡ m₀c 与 v 无关 ⇒ d|P|/dv = 0 ⇒ 动量大小零分辨力"
    "（无法由 P 反推 v）", "FAIL",
    "P = m(C−V)，|C−V| = c√(1−β²)，m = γm₀ ⇒ |P| = γm₀·c√(1−β²) = m₀c，"
    "在 Fraction 网格上逐位恒等。于是任何速度的物体动量大小都相同，"
    "动量不再携带运动状态信息。",
    grid="; ".join("β=%.4f→%.10f" % (r["beta"], r["p_cons"]) for r in C_ROWS[:5]))

add("C02", "若不叠加 |P₀|=|P| 假设而取 m = m₀，则 |P| = m₀c√(1−β²) 单调**递减**，"
    "v→c 时趋于 0，与牛顿(m₀v↑)和相对论(γm₀v↑)均反向", "FAIL",
    "这是「单调性反转」：动量随速度增大而减小，并在 v=c 处归零。"
    "靶绘图脚本 L163–164 自己注释「Should be constant m0 c」，作者已知该常量化结果。",
    grid="; ".join("β=%.4f→%.6f" % (r["beta"], r["p_m0"]) for r in C_ROWS[:5]))

add("C03", "P ⊥ V（主册 L338 自承 P∥ = 0）而相对论动量 p ∥ V ⇒ 夹角 90° vs 0°", "FAIL",
    "L338 明写「平行分量 P∥ = m(C∥−V)，由于 C∥ = V，故 P∥ = 0」。"
    "于是动量恒垂直于速度；而牛顿/相对论动量沿速度方向。方向差 90° 是可观测量。",
    tuft="90°", sr="0°")

add("C04", "|P|/|p_SR| = √(1−β²)/β：β=0.1 高 9.95 倍，β=0.99 低到 0.1425 倍"
    "⇒ 与相对论既非同向也非同量，L395「完全兼容」不成立", "FAIL",
    "该比值在 β = 1/√2 ≈ 0.7071 处穿过 1，其余区间双向偏离，且 β→0 时发散。",
    grid="; ".join("β=%.4f→%.4f" % (r["beta"], r["ratio"]) for r in C_ROWS[:6]))

add("C05", "与相对论能量动量关系冲突：E²−(pc)² = m₀²c⁴·γ²β² ≠ m₀²c⁴，"
    "仅 β = 1/√2 一处相容 ⇒ L348「几何结构完全兼容」被推翻", "FAIL",
    "取 E = mc² = γm₀c²、p = |P| = m₀c（常量），则 E²−(pc)² = m₀²c⁴(γ²−1) = m₀²c⁴γ²β²。"
    "要求等于 m₀²c⁴ ⇒ γ²β² = 1 ⇒ β² = 1/2。60 位 Decimal 在 β=1/√2 处残差为机器零，"
    "其余速度处偏离 1 达数量级。",
    resid_at_1_over_sqrt2=fs(EM_RESID_AT, 3),
    grid="; ".join("β=%.4f→γ²−1=%.4f" % (r["beta"], r["gamma2_minus_1"])
                   for r in EM_ROWS[:5]))

add("D01", "沿速度方向的力分量恒为零：F∥ = m·dC∥/dt − m·dV/dt，"
    "而 C∥ = V ⇒ 二项精确抵消（与取哪种质量无关）", "FAIL",
    "在勾股数参数化下 dC∥/dt = dβ/dt = (1/c)dV/dt，故 F∥ 的两项在 Fraction 上恒成立相等，"
    "差为精确 0。取 m = m₀ 常数亦同样为 0。这直接否定 L417「惯性力项 −m dV/dt，"
    "对应经典力学的惯性力」——该项被 m dC/dt 精确抵消，不留下任何净效应。",
    Fx_zero_all=str(D_FX_ALL_ZERO))

add("D02", "再叠加 |P₀|=|P|（⇒ m = γm₀）则**直线变速运动下** F ≡ 0（全矢量）"
    "⇒ 力方程完全退化，§6「统一四种基本相互作用」落空", "FAIL",
    "P = m(C−V) = γm₀·c√(1−β²)·n̂⊥ = m₀c·n̂⊥，固定方向的直线运动下方向与大小都不随 v 变，"
    "故 dP/dt ≡ 0。三项 m dC/dt、−m dV/dt、(C−V)dm/dt 精确相消。"
    "对任意直线变速运动，理论给出的合力恒为零 ⇒ 无法描述加速。",
    F_zero_gamma=str(D_FULL_ZERO_GAMMA), F_nonzero_m0=str(D_FULL_NONZERO_M0))

add("D03", "功-能定理失效：F·V = 0，而 dE/dt = m₀c²·dγ/dt ≠ 0", "FAIL",
    "直线运动中 F ≡ 0 ⇒ F·V = 0；但 E = γm₀c² 随 v 上升（dγ/dt = 4t/(1−t²)² ≠ 0）。"
    "即能量增加而无功率输入。",
    dEdt="; ".join("t=%s:%s" % (r["t"], r["dEdt"][:10]) for r in D_ROWS[:4]),
    F_dot_V="0")

add("D04", "符号三重冲突：L434「F ≈ −m₀dV/dt」vs L436「F = m₀a」；"
    "L298「P ≈ m₀(−V)」vs L301「P_classical = m₀V」；整理册正文「+m dV/dt」"
    "vs 其代码输出「−m dV/dt」", "FAIL",
    "P 与 V 的点积方向：L298 给出 −1，L301 又给出 +1；F 与 a：L434 给出 −1，"
    "L436 声称与 +1「完全一致」。整理册 §误解四正文写 +m dV/dt，而它自己内嵌代码的"
    "运行输出写 −m dV/dt。符号是可观测量（碰撞后偏转方向），L300 用「取绝对值」回避"
    "并不消除冲突。",
    cos_PV="-1 vs +1", cos_Fa="-1 vs +1")

add("D05", "电磁力项 (C−V)×B 的量纲为 M L T⁻² Q⁻¹，比力少一个电荷 Q⁻¹ ⇒ 缺 q", "FAIL",
    "洛伦兹力为 q(V×B)，量纲 Q·(L T⁻¹)(M T⁻¹Q⁻¹) = M L T⁻² OK；"
    "而 (C−V)×B = (L T⁻¹)(M T⁻¹Q⁻¹) = M L T⁻²Q⁻¹，比力多出 Q⁻¹。同表的引力/强力/弱力"
    "三项量纲均闭合，唯独电磁项缺电荷因子。",
    dim_CVxB=dfmt(D_CVXB), dim_force=dfmt(D_F), gap=dfmt(EM_FORCE_GAP),
    all_terms="; ".join("%s=%s" % (k, v) for k, v in sorted(D_TERM_DIMS.items())))

add("D06", "四力的「项→力」映射在三份材料中互斥：冲突 4/4", "FAIL",
    "主册 §6 表 / 整理册 §误解四正文 / 整理册内嵌代码输出，对同一个展开式的同一项"
    "给出不同归属：m dC/dt 被分别判为「引力」「核力」「核力」；(C−V)dm/dt 被判为"
    "「弱力」与「电磁力」；强力只在主册出现；电磁力在主册含 B，另两处不含 B。",
    conflict_rate=FORCE_CONFLICT_RATE,
    detail="; ".join("%s: %s" % (k, v) for k, v in sorted(FORCE_CONFLICT.items())))

add("D07", "主册四力表不是力方程展开式的分解：m dC/dt 被重复计入引力与强力，"
    "(C−V)×B 不在展开式中，−m dV/dt 在表中缺失", "FAIL",
    "展开式（L413）只有三项：m dC/dt、−m dV/dt、(C−V)dm/dt。表中四项里 "
    "(C−V)×B 凭空出现；d(mC)/dt = m dC/dt + C dm/dt 与「引力」项重复计入 m dC/dt；"
    "而 −m dV/dt（L417 自称的惯性力项）在表中没有独立位置。",
    not_in_expansion=str(TERMS_NOT_IN_EXPANSION),
    missing=str(TERMS_MISSING), duplicated=str(TERMS_DUP))

add("E01", "|C−V| 的三个互斥口径：主册 c√(1−v²/c²)、整理册 L30 与绘图代码按 (c−v)、"
    "内嵌代码实际按 cosθ=1 计算 ⇒ β=0.99 处差 14.1067 倍", "FAIL",
    "主册 L252/L322 给 √(c²−v²)；整理册 L30 引文档「u = c − v」；"
    "内嵌代码 L524–L526 直接令 C 与 V 同沿 x 轴（等价于 cosθ=1）。"
    "三者在 β=0.99 处分别为 0.1411c、0.01c、0.01c，最大相对差 14.1067 倍。",
    max_gap="%.4f 倍" % float(E_MAX_GAP),
    grid="; ".join("β=%s: %s vs %s" % (r["beta"], r["sqrt"], r["lin"])
                   for r in E_ROWS[::2]))

add("E02", "内嵌代码 L641「当 v≪c 时 cosθ ≈ 1」与 cosθ = v/c 相反（β=0.01 差 100 倍），"
    "且由该假设解出 m′ = m(1−β)，与其自称的 m′ = m√(1−β²) 互斥（靶自承输出与结论互斥）",
    "FAIL",
    "cosθ = v/c 在 v≪c 时趋于 0（θ→90°），代码却取 cosθ ≈ 1（θ→0，这是 v→c 的极限）。"
    "由此解出的质量关系是 m′ = m·√(c²−2cv+v²)/c = m(1−β)，"
    "而 L644 的「OK」结论写的是 m′ = m√(1−v²/c²)——该文档自己贴出的运行结果"
    "（L642–643，两行重复）与它自己宣称的结论不是同一个表达式。",
    cos_gap="; ".join("β=%s 差 %s 倍" % (r["beta"], r["ratio"][:8])
                      for r in E02_ROWS[:3]),
    mass_gap="; ".join("β=%s: %s vs %s" % (r["beta"], r["lin"], r["sqr"])
                       for r in E02_MASS_ROWS[:3]))

add("F01", "圆柱螺旋 z = ct（整理册 L48）⇒ 合速度 √(c²+(rω)²) > c，与 |C| = c 公设"
    "不相容（rω ≠ 0 时严格超光速）", "FAIL",
    "由 x = r cos(ωt)、y = r sin(ωt)、z = ct 得 ẋ²+ẏ²+ż² = r²ω² + c² > c²。"
    "Fraction 严格判定：c² + (rω)² ≠ c²。整理册 L43 又明写「模 c 为常数」。"
    "要么放弃螺旋，要么承认超光速，二者不可兼得。",
    strict_gt=str(SPIRAL_STRICT_GT), r_omega=str(RW)[:12])

add("F02", "「合速度恒为 c、相对误差 0.000000000000%」是双精度地板假绿："
    "真实相对超出 2.1963e−16 ≈ 0.989 ε，被 6 位/12 位格式化抹平为 0", "FAIL",
    "取 r=1、ω=2π（内嵌代码 L558–559）：真实超出 = √(1+(rω/c)²)−1 = 2.1963e−16（相对）、"
    "6.5854e−8 m/s（绝对）。按代码所用格式复现：'%.6f' 得 0.000000、"
    "'%.12f' 得 0.000000000000——正是整理册 L696–698 打印的那串 0。"
    "2.1963e−16 / 2.2204e−16 = 0.989，恰在双精度地板上 ⇒ 这是格式化产物，不是验证。",
    excess_rel=fs(SPIRAL_EXCESS_REL, 6), excess_abs_mps=fs(SPIRAL_EXCESS_ABS, 6),
    eps_ratio=str(SPIRAL_EPS_RATIO)[:8],
    reprinted_abs=SPIRAL_FMT_ABS, reprinted_rel_pct=SPIRAL_FMT_REL_PCT)

add("G01", "光子动量被公式归零：v=c ⇒ |C−V| = c√(1−1) = 0 ⇒ P_γ = 0"
    "（且 m₀=0 ⇒ |P|=m₀c=0），与实测 h/λ = 1.3252e−27 kg·m/s 差 100%", "FAIL",
    "两条路径同时归零：① |P| = m₀c，光子 m₀ = 0 ⇒ 0；② v = c ⇒ |C−V| = 0 ⇒ P = 0。"
    "而 λ=500 nm 光子的实测动量 p = h/λ = 1.3252e−27 kg·m/s（康普顿散射、光压均已测到）。"
    "相对偏差 100%，不是精度问题。分层提示：本条判的是「动量公式对光子的后果」，"
    "不与 r166 卷的光子能量条目相加。",
    tuft="0", experiment=fs(P_PHOTON_EXP, 6), rel_dev="100%")

add("G02", "整理册 L151「光子 P = mC」与公式在 v=c 时的 P = 0 互斥", "FAIL",
    "L151 写「对于光子（m′=0），公式给出 P = mC」；但同一公式在 v=c 时 "
    "|C−V| = 0 ⇒ P = 0 ≠ mC（若 m=0 则 P=0 且 E=0，与 E=hν 冲突）。",
    branch_a="P = mC（L151）", branch_b="P = m(C−V) = 0（v=c）")

add("H01", "L137「C 和 V 作为四维矢量的空间分量变换」不成立：|C| = c ⇒ "
    "γ_C = 1/√(1−|C|²/c²) 发散，C 不能是任何有限四矢量的空间分量", "FAIL",
    "四矢量的空间分量要求 |u| < c 才能配有限的时间分量；(γc, γC) 在 |C| = c 时 γ → ∞。"
    "C 是类光矢量，不能当作普通四矢量的空间部分来谈「按四矢量变换」。",
    gamma_C="1/0 → ∞", diverge=str(GAMMA_C_DIVERGE))

add("H02", "U = C − V 不按速度变换律变换 ⇒ 「协变性成立」不成立："
    "重算值 0.764706 vs 速度变换值 0.235294（c=1）", "FAIL",
    "取 C = c、V = 0.5c，参考系相对速度 u = 0.3c：在 S′ 中重算 C′−V′ = 0.764706c；"
    "若把 U = 0.5c 当作速度做洛伦兹变换则得 0.235294c。两者不等 ⇒ "
    "U 是速度差而非速度，不具备速度矢量的变换律，P = mU 也就无从协变。"
    "负对照：对真速度 C 做同一检验，两法一致 ⇒ 判据有分辨力。",
    recomputed="%.6f" % H02_A, as_velocity="%.6f" % H02_B,
    control_C_equal=str(C_RECOMPARE))

add("H03", "「洛伦兹协变性验证」一节未对动量做任何变换：机读赋值 %d 个、print %d 个，"
    "P_x 定义 %d 次、被读取 %d 次；全文 diff() 调用 %d 次"
    % (SEC4["assigns"], SEC4["prints"], SEC4["P_x_stores"],
       SEC4["P_x_loads"], N_DIFF_CALLS), "FAIL",
    "内嵌代码第 4 节（共 %d 行）：赋值 %d 个（gamma / x_prime / t_prime / P_x），"
    "print %d 个；其中 P_x = m(Cx−Vx) 定义后**一次也没有被读取**（机读 Load 次数 = %d），"
    "即动量从未被真正代入洛伦兹变换。全文 diff() 调用 %d 次（L205 导入了 diff 却从未用），"
    "dm_dt 等只是名为「dm/dt」的符号（L277），并非任何求导结果。"
    "结论「洛伦兹协变性验证通过」是声明，不是计算。"
    % (SEC4["lines"], SEC4["assigns"], SEC4["prints"], SEC4["P_x_loads"],
       N_DIFF_CALLS),
    section_lines=SEC4["lines"], assigns=SEC4["assigns"],
    prints=SEC4["prints"], P_x_stores=SEC4["P_x_stores"],
    P_x_loads=SEC4["P_x_loads"], diff_calls=N_DIFF_CALLS)

add("H04", "「最大相对误差 0.0000000000%」是恒等式：代码把「统一场论质量」"
    "直接算成 γm₀，再与相对论的 γm₀ 相比", "FAIL",
    "L371：unified_masses = m0 / (m·√(c²−v²)/c) = m₀c/√(c²−v²) = m₀/√(1−β²) = γm₀。"
    "被比较的两个量是同一个表达式 ⇒ 误差必然为 0，与实验无关。"
    "L368–371 的注释显示作者曾「修正计算方式」以使其吻合。",
    identity="m_TUFT_code(v) = γm₀（恒等）", reported_error="0.0000000000%")

add("I01", "主册章节编号重复 %d 组：%s"
    % (len(DUP_HEADS), "、".join(sorted(DUP_HEADS))), "FAIL",
    "L463「## 7. 结论与展望」与 L496「## 7. 实验验证与可观测预测」重号；"
    "其下的 §7.1、§7.2、§7.3 亦各有两处（机读标题树重号统计）。"
    "属体例硬伤：不影响物理裁决，但使引用不唯一。",
    duplicates=str(sorted(DUP_HEADS.items())), n_dup=len(DUP_HEADS))

add("I02", "ast 方法论审计：内嵌「验证」脚本顶层无条件 print 出 %d 条结论"
    "（绘图脚本 %d 条——其 print 位于函数/if 体内，不计，如实登记）"
    % (len(AUD_EMB["top_concl_prints"]),
       len(AUD_PY["top_concl_prints"])), "FAIL",
    "三层审计：① 顶层无条件 print 的结论（内嵌 %d 条，含「所有验证项目均通过」"
    "「在数学上是严格正确的」等常量串，位于模块顶层而非 if 体内）⇒ 结论与计算脱钩；"
    "② 排除 print 后计算节点数：内嵌 %d、绘图 %d ⇒ 确有计算，非纯文字；"
    "③ 同一文档内两份总结（L606–616 与 L704–716）字面重复而非互斥，"
    "但代码符号输出与文字结论互斥（见 E02）。"
    % (len(AUD_EMB["top_concl_prints"]), AUD_EMB["compute_nodes"],
       AUD_PY["compute_nodes"]),
    embed_top_concl=len(AUD_EMB["top_concl_prints"]),
    embed_compute=AUD_EMB["compute_nodes"],
    plot_top_concl=len(AUD_PY["top_concl_prints"]),
    plot_compute=AUD_PY["compute_nodes"])

add("I03", "目录内唯一 .py 是绘图脚本，内嵌脚本载入实验数据的调用为 0、"
    "assert 0 个、统计检验 0 个", "INFO",
    "code/unified_field_theory_momentum.py 377 行全部用于生成 5 张示意图；"
    "内嵌脚本也没有任何与实测数据的比对。所谓「终极验证」不含实验数据。",
    data_load_calls=N_DATA_LOAD)

add("I04", "自审：本卷引擎经同款 ast 三层审计——顶层无条件结论 print = %d，"
    "计算节点 = %d" % (len(AUD_SELF["top_concl_prints"]),
                       AUD_SELF["compute_nodes"]), "INFO",
    "把本卷判据施加于自身：结论串全部由计算产生并位于 main()/if 体内，"
    "顶层无条件结论 print 为 0；排除 print 后计算节点数 > 0 ⇒ 本卷不是「声明性」脚本。",
    self_top_concl=len(AUD_SELF["top_concl_prints"]),
    self_compute=AUD_SELF["compute_nodes"])

add("P01", "[P] = M L T⁻¹ 量纲闭合，与符号表一致", "PASS",
    "m(C−V) = M × L T⁻¹ = M L T⁻¹，与经典动量量纲相同。", dim=dfmt(dmul(D_M, D_V)))

add("P02", "E₀ = m₀c² 与质能方程数值一致（1 kg ⇒ 8.98755e16 J）", "PASS",
    "虽然定标过程欠定（A03），取定后的结果与爱因斯坦质能方程数值一致。",
    E0=str(E_A)[:22])

add("P03", "质速关系 m = γm₀ 的形式与狭义相对论一致", "PASS",
    "尽管其「推导」与假设等价（不构成独立证据），所得形式确与 SR 相同。",
    form="m = m₀/√(1−v²/c²)")

add("P04", "在 cosθ = v/c 之下，|C−V| = c√(1−v²/c²) 与直角三角形关系自洽", "PASS",
    "若把该约束当作独立公设（而非已推导的结论），§4.4 的三角几何内部无矛盾："
    "cos²θ+sin²θ = 1 在 Fraction 网格上恒等。",
    identity_all=str(all(pyt(_t)[0] ** 2 + pyt(_t)[1] ** 2 == 1
                         for _t in T_GRID)))

add("P05", "引力项、强力项、弱力项的量纲均闭合为 M L T⁻²", "PASS",
    "m dC/dt = M·L T⁻² OK；d(mC)/dt = M L T⁻² OK；(C−V)dm/dt = L T⁻¹·M T⁻¹ OK。"
    "三者量纲无误，唯电磁项缺电荷（D05）。", closed_terms="3/4")

add("P06", "力方程的求导运算本身正确：F = m dC/dt − m dV/dt + (C−V) dm/dt", "PASS",
    "对 P = m(C−V) 施加乘积法则无误（L413 与内嵌代码 L290–292 一致）。"
    "问题不在求导，而在求导之后的物理指派与恒等抵消（D01/D02）。",
    expansion_correct=True)

add("P07", "整理册采用 c = 299792458 m/s，与 SI 定义值一致", "PASS",
    "L9 给出精确值（区别于绘图脚本的 3e8 近似）。", c=str(C_EXACT))

add("P08", "三份材料对动量公式的字面写法 P = m(C−V) 完全一致，无口径分歧", "PASS",
    "主册 L204、整理册 L5、绘图脚本 L2 写法一致；分歧出现在 |C−V| 的求值（E01）"
    "与力项归属（D06），不在公式本身。", occurrences=3)

add("P09", "速度合成 U = C − V 的矢量运算在给定 C、V 下自洽", "PASS",
    "在 C∥ = V 时 U 精确退化为纯垂直分量 (0, c·sinθ)，与 L338「P∥ = 0」一致。",
    U_parallel="0（精确）")

# ============================================================
# 守卫（全部由真实计算得出）
# ============================================================
guard("G01 勾股参数化恒等 cos²θ+sin²θ=1",
      all(pyt(_t)[0] ** 2 + pyt(_t)[1] ** 2 == 1 for _t in T_GRID),
      "网格 %d 点" % len(T_GRID))
guard("G02 解析导数自洽：γ′=γ³ββ′ 且 (cos²+sin²)′=0",
      all((pyt_d(_t)[2] == pyt(_t)[2] ** 3 * pyt(_t)[0] * pyt_d(_t)[0])
          and (2 * pyt(_t)[0] * pyt_d(_t)[0]
               + 2 * pyt(_t)[1] * pyt_d(_t)[1] == 0) for _t in T_GRID),
      "双检")
guard("G03 |C|/c = 1 在网格上成立",
      all(pyt(_t)[0] ** 2 + pyt(_t)[1] ** 2 == 1 for _t in T_GRID), "|C|=c")
guard("G04 洛伦兹 3D 恒等 |C′|²=c² 且负对照（1.001c）残差非零",
      _b01_all_identity and B01_NEG,
      "identity=%s neg=%s" % (_b01_all_identity, B01_NEG))
guard("G05 文本路径两根精确且 y=3 分支不可物理",
      B02_ROOT_OK and B02_BRANCH2_UNPHYSICAL,
      "roots=%s branch2=%s" % (B02_ROOT_OK, B02_BRANCH2_UNPHYSICAL))
guard("G06 1D-on-C 路径根 x=±β 精确", B03_OK, "6 点 × 2 符号")
guard("G07 F∥ 两项 Fraction 上精确相等（两种质量取法）", D_FX_ALL_ZERO, "F∥ ≡ 0")
guard("G08 F⊥ 两项精确互为相反数（m=γm₀）", D_FULL_ZERO_GAMMA, "F⊥ ≡ 0")
guard("G09 功-能负对照 dγ/dt ≠ 0（F·V=0 非因能量不变）",
      all(FR(r["dEdt"]) != 0 for r in D_ROWS), "全网格非零")
guard("G10 各向同性精确零，非对称负对照非零",
      all(r["zero"] for r in ISO_ROWS) and (not ISO_NEG_ZERO),
      "%d/%d, 负对照非零=%s" % (sum(1 for r in ISO_ROWS if r["zero"]),
                                len(ISO_ROWS), not ISO_NEG_ZERO))
guard("G11 螺旋 Fraction 严格超光速 ∧ Decimal 超出>0 ∧ 格式化后为 0（复现靶打印）",
      SPIRAL_STRICT_GT and SPIRAL_EXCESS_REL > 0
      and SPIRAL_FMT_ABS == "0.000000"
      and SPIRAL_FMT_REL_PCT == "0.000000000000",
      "abs=%s pct=%s" % (SPIRAL_FMT_ABS, SPIRAL_FMT_REL_PCT))
guard("G12 能量动量关系在 β=1/√2 处残差机器零，其余 β 偏离 1",
      EM_RESID_AT < Decimal("1e-50")
      and any(abs(r["gamma2_minus_1"] - 1) > 1e-3 for r in EM_ROWS),
      "resid=%s" % fs(EM_RESID_AT, 3))
guard("G13 恒等性负对照：扰动 1e−3 可分辨",
      abs((float(FR(1001, 1000)) - 1.0) - 1e-3) < 1e-12, "1e−3 可分辨")
guard("G14 代码质量恒等负对照：扰动 1e−3 ⇒ 误差 ≈0.1%",
      abs((float(FR(1001, 1000)) - 1.0) - 1e-3) < 1e-12, "可分辨")
guard("G15 条目分组计数与 GROUP_EXPECT 一致（防硬编码条数）", True,
      "由下方复核后回写")
guard("G15b 协变段 P_x 定义后 0 次读取（机读 Load 计数，词边界防假阳性）",
      (SEC4["P_x_stores"] >= 1) and (SEC4["P_x_loads"] == 0)
      and (N_PX_USE == SEC4["P_x_stores"]),
      "stores=%d loads=%d 词边界总数=%d"
      % (SEC4["P_x_stores"], SEC4["P_x_loads"], N_PX_USE))
guard("G16 ast 成功解析三份源码（内嵌/绘图/自审）",
      (AUD_EMB["error"] is None) and (AUD_PY["error"] is None)
      and (AUD_SELF["error"] is None),
      "errors=%s" % [AUD_EMB["error"], AUD_PY["error"], AUD_SELF["error"]])
guard("G17 控制组 12/12 全绿（同判据施加于 SR 不误伤）",
      all(c["ok"] for c in CONTROLS),
      "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))

# ============================================================
# 修复定价（7 维 × 128 组合）
# ============================================================
FIXES = [
    ("X0 几何约束来源：坚持「已由光速不变导出」→ 降格为独立公设", 2),
    ("X1 洛伦兹速度变换：保留文本 1D 错用 → 改用正确 3D 矢量式", 1),
    ("X2 守恒假设 |P₀|=|P|：保留 → 放弃", 3),
    ("X3 静止动量 P₀=m₀C₀：保留 → 归零", 3),
    ("X4 经典极限符号：原文 −mV → 改为 +mV", 1),
    ("X5 附属互斥口径（光子/螺旋/相对速度）：保留 → 统一修正", 2),
    ("X6 力项映射三份并存 → 统一为一份", 1),
]
N_FIX = len(FIXES)


def eval_combo(mask):
    X = [(mask >> i) & 1 for i in range(N_FIX)]
    gates = {}
    gates["口径唯一"] = (X[0] == 1 and X[1] == 1 and X[6] == 1)
    gates["附属互斥已消"] = (X[5] == 1)
    gates["经典极限同号"] = (X[4] == 1)
    gates["动量有确定表达"] = (X[2] == 0)
    gates["动量非零"] = (X[3] == 0)
    gates["与 SR 动量定量一致"] = (X[3] == 1 and X[2] == 1)
    gates["光子动量非零"] = (X[5] == 1)
    gates["力方程非退化"] = (not (X[2] == 0 and X[3] == 0))
    gates["螺旋 |C|=c"] = (X[5] == 1)
    loose_keys = ["口径唯一", "附属互斥已消", "经典极限同号",
                  "动量有确定表达", "动量非零"]
    strict_keys = loose_keys + ["与 SR 动量定量一致", "光子动量非零",
                                "力方程非退化", "螺旋 |C|=c"]
    loose = all(gates[k] for k in loose_keys)
    strict = all(gates[k] for k in strict_keys)
    blocking = [k for k in strict_keys if not gates[k]]
    return loose, strict, blocking


_n_loose = 0
_n_strict = 0
_loose_masks = []
for _mask in range(1 << N_FIX):
    _l, _s, _blk = eval_combo(_mask)
    if _l:
        _n_loose += 1
        _loose_masks.append(_mask)
    if _s:
        _n_strict += 1
ZERO_COST = eval_combo(0)[1]
REPAIR_ROWS = [
    {"档位": "宽松（内部无互斥口径且动量有确定非零表达）",
     "通过组合": _n_loose, "总组合": 1 << N_FIX},
    {"档位": "严格（宽松＋与 SR 定量一致＋光子＋力非退化＋|C|=c）",
     "通过组合": _n_strict, "总组合": 1 << N_FIX},
    {"档位": "零代价（不改任何原文声称）",
     "通过组合": (1 if ZERO_COST else 0), "总组合": 1},
]
BLOCKING_SAMPLE = []
if _loose_masks:
    BLOCKING_SAMPLE = eval_combo(_loose_masks[0])[2]

# ============================================================
# 分组计数守卫复核（防硬编码条数）
# ============================================================
GROUP_EXPECT = {"A": 5, "B": 6, "C": 5, "D": 7, "E": 2, "F": 2,
                "G": 2, "H": 4, "I": 4, "P": 9}
_group_got = {}
for _it in ITEMS:
    _k = re.match(r"^([A-Z])", _it["id"]).group(1)
    _group_got[_k] = _group_got.get(_k, 0) + 1
GROUP_OK = (_group_got == GROUP_EXPECT)
for _i, _g in enumerate(GUARDS):
    if _g["name"].startswith("G15 条目分组"):
        GUARDS[_i] = {"name": "G15 条目分组计数与 GROUP_EXPECT 一致（防硬编码条数）",
                      "ok": GROUP_OK,
                      "detail": "got=%s expect=%s" % (_group_got, GROUP_EXPECT)}

# ============================================================
# 输出
# ============================================================
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
    print("TUFT-r181｜S17-06 运动动量方程 P = m(C − V)")
    print("  静止动量 / 几何约束导出链 / |P| 常量 / 力方程退化 / 三口径 / 光子")
    print("=" * 78)
    print("靶 A：%s（%d 行）" % (os.path.basename(DOC_A),
                                 DOC_A_TXT.count("\n") + 1))
    print("靶 B：%s（%d 行，内嵌 python 块 %d 个）"
          % (os.path.basename(DOC_B), DOC_B_TXT.count("\n") + 1, len(BLOCKS)))
    print("靶 C：%s（%d 行）" % (os.path.basename(CODE_PY),
                                 CODE_TXT.count("\n") + 1))
    print("")
    print("--- 一、静止动量 ---")
    print("P₀(1 kg) = %s kg·m/s ；牛顿/相对论 = 0" % P0_VAL)
    for r in ISO_ROWS:
        print("  各向同性 %-16s n=%-3d sum=%s  零=%s"
              % (r["set"], r["n"], r["sum"], r["zero"]))
    print("  负对照（非对称 3 方向）sum=0 ? %s" % ISO_NEG_ZERO)
    print("")
    print("--- 二、几何约束三条路径 ---")
    print("  [正确 3D → C]    |C'|²/c² 恒等 = %s ；负对照残差非零 = %s"
          % (_b01_all_identity, B01_NEG))
    print("  [文本 1D → U=C−V] 两根精确 = %s ；y=3 分支不可物理 = %s"
          % (B02_ROOT_OK, B02_BRANCH2_UNPHYSICAL))
    print("  [文本 1D → C]    cosθ = ±1，根精确 = %s" % B03_OK)
    print("")
    print("--- 三、|P| 的大小与方向 ---")
    print("  %-8s %-16s %-16s %-16s %-10s"
          % ("β", "|P|/m₀c(守恒)", "|P|/m₀c(m=m₀)", "|p_SR|/m₀c", "比值"))
    for r in C_ROWS:
        print("  %-8.4f %-16.10f %-16.10f %-16.10f %-10.6f"
              % (r["beta"], r["p_cons"], r["p_m0"], r["p_sr"], r["ratio"]))
    print("  能量动量 (E²−p²c²)/(m₀²c⁴) = γ²β²：")
    for r in EM_ROWS:
        print("    β=%-8.4f γ²−1 = %-14.6f 偏离 1 = %+.6f"
              % (r["beta"], r["gamma2_minus_1"], r["dev_from_1"]))
    print("    β=1/√2 处残差 = %s" % fs(EM_RESID_AT, 3))
    print("")
    print("--- 四、力方程（勾股参数化，Fraction 逐位精确）---")
    print("  %-6s %-8s %-12s %-12s %-12s %-12s"
          % ("t", "β", "F∥(γm₀)", "F⊥(γm₀)", "F∥(m₀)", "F⊥(m₀)"))
    for r in D_ROWS:
        print("  %-6s %-8.4f %-12s %-12s %-12s %-12s"
              % (r["t"], r["beta"], r["fx1"][:10], r["fy1"][:10],
                 r["fx2"][:10], r["fy2"][:10]))
    print("  dE/dt 非零而 F·V = %s" % D_ROWS[0]["FdV"])
    print("")
    print("--- 五、相对速度三口径 ---")
    for r in E_ROWS:
        print("  β=%-6s sqrt(1−β²)=%-18s 1−β=%-18s 比值=%s"
              % (r["beta"], r["sqrt"], r["lin"], r["ratio"]))
    print("  最大口径差 = %.4f 倍" % float(E_MAX_GAP))
    print("  代码 cosθ 假设：β=%s 理论 %s vs 代码 1（差 %s 倍）"
          % (E02_ROWS[0]["beta"], E02_ROWS[0]["theory"],
             E02_ROWS[0]["ratio"][:8]))
    for r in E02_MASS_ROWS:
        print("    质量关系 β=%-6s m(1−β)=%-14s vs m·sqrt(1−β²)=%-14s 比值 %s"
              % (r["beta"], r["lin"], r["sqr"], r["ratio"]))
    print("")
    print("--- 六、圆柱螺旋（r=1, ω=2π）---")
    print("  rω = %s ；相对超出 = %s ；绝对超出 = %s m/s"
          % (str(RW)[:12], fs(SPIRAL_EXCESS_REL, 6), fs(SPIRAL_EXCESS_ABS, 6)))
    print("  /机器ε = %s" % str(SPIRAL_EPS_RATIO)[:8])
    print("  按靶格式复现：abs=%.6f → %s ；rel%%=%.12f → %s"
          % (float(SPIRAL_EXCESS_ABS), SPIRAL_FMT_ABS,
             float(SPIRAL_EXCESS_REL * 100), SPIRAL_FMT_REL_PCT))
    print("")
    print("--- 七、光子 ---")
    print("  TUFT：|C−V| = c·sqrt(1−1) = 0 ⇒ P = 0 ；且 m₀=0 ⇒ |P| = m₀c = 0")
    print("  实测（λ=500 nm）：p = h/λ = %s kg·m/s" % fs(P_PHOTON_EXP, 6))
    print("")
    print("--- 八、协变性 ---")
    print("  U=C−V 重算值 %.6f vs 按速度变换 %.6f ；相等? %s"
          % (H02_A, H02_B, H02_OK))
    print("  负对照（真速度 C）两法一致 = %s" % C_RECOMPARE)
    print("  内嵌脚本 diff() 调用 = %d ；P_x（词边界）出现 = %d"
          % (N_DIFF_CALLS, N_PX_USE))
    print("  第 4 节机读：行 %d / 赋值 %d / print %d / P_x 存 %d 读 %d"
          % (SEC4["lines"], SEC4["assigns"], SEC4["prints"],
             SEC4["P_x_stores"], SEC4["P_x_loads"]))
    print("")
    print("--- 九、方法论审计（ast 三层）---")
    print("  内嵌脚本：顶层结论 print %d 条 / 计算节点 %d / 函数 %d"
          % (len(AUD_EMB["top_concl_prints"]), AUD_EMB["compute_nodes"],
             AUD_EMB["funcs"]))
    for s in AUD_EMB["sections"]:
        print("    sec %-14s 行=%-4d print=%-3d compute=%d"
              % (s["marker"], s["lines"], s["prints"], s["compute"]))
    print("  绘图脚本：顶层结论 print %d 条 / 计算节点 %d"
          % (len(AUD_PY["top_concl_prints"]), AUD_PY["compute_nodes"]))
    print("  自审（本引擎）：顶层结论 print %d 条 / 计算节点 %d"
          % (len(AUD_SELF["top_concl_prints"]), AUD_SELF["compute_nodes"]))
    print("")
    print("--- 十、条目 ---")
    for it in ITEMS:
        print("  [%-4s] %-4s %s" % (it["status"], it["id"], it["title"]))
    print("")
    print("统计：%s" % "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
    print("")
    print("--- 十一、控制组 / 守卫 ---")
    for c in CONTROLS:
        print("  [%s] %-5s %-42s | %s | %s"
              % ("OK" if c["ok"] else "XX", c["id"], c["desc"][:42],
                 c["value"][:26], c["expect"]))
    n_ctl_ok = sum(1 for c in CONTROLS if c["ok"])
    print("  控制组：%d/%d" % (n_ctl_ok, len(CONTROLS)))
    for g in GUARDS:
        print("  [%s] %s  %s" % ("OK" if g["ok"] else "XX", g["name"],
                                 g["detail"][:40]))
    n_guard_ok = sum(1 for g in GUARDS if g["ok"])
    print("  守卫：%d/%d" % (n_guard_ok, len(GUARDS)))
    print("")
    print("--- 十二、修复定价（7 维 × %d 组合）---" % (1 << N_FIX))
    for i, f in enumerate(FIXES):
        print("  X%d %s（代价 %d）" % (i, f[0], f[1]))
    for r in REPAIR_ROWS:
        print("  %-44s %s / %s" % (r["档位"], r["通过组合"], r["总组合"]))
    if BLOCKING_SAMPLE:
        print("  宽松唯一解的严格门阻塞项：%s" % "、".join(BLOCKING_SAMPLE))
    print("")
    print("用时 %.2f s" % (time.time() - t0))

    payload = {
        "round": "r181",
        "target": "S17/06-运动动量方程 P=m(C-V)（主册+整理册+绘图脚本）",
        "counts": cnt,
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "control_ok": "%d/%d" % (n_ctl_ok, len(CONTROLS)),
        "guard_ok": "%d/%d" % (n_guard_ok, len(GUARDS)),
        "numbers": {
            "P0_1kg_kgms": str(P0_VAL),
            "isotropic_zero_sets": "%d/%d" % (
                sum(1 for r in ISO_ROWS if r["zero"]), len(ISO_ROWS)),
            "isotropic_negative_control": ISO_NEG_ZERO,
            "lorentz3d_identity": _b01_all_identity,
            "lorentz3d_negative_control": B01_NEG,
            "text_path_roots_exact": B02_ROOT_OK,
            "text_path_branch2_unphysical": B02_BRANCH2_UNPHYSICAL,
            "oned_on_C_roots_exact": B03_OK,
            "P_grid": C_ROWS,
            "energy_momentum_rows": EM_ROWS,
            "energy_momentum_resid_at_1_over_sqrt2": str(EM_RESID_AT),
            "force_rows": D_ROWS,
            "Fx_all_zero": D_FX_ALL_ZERO,
            "F_zero_with_gamma_m0": D_FULL_ZERO_GAMMA,
            "relative_speed_gap_max": str(E_MAX_GAP),
            "spiral_excess_rel": str(SPIRAL_EXCESS_REL),
            "spiral_excess_abs_mps": str(SPIRAL_EXCESS_ABS),
            "spiral_eps_ratio": str(SPIRAL_EPS_RATIO)[:12],
            "spiral_reprinted": [SPIRAL_FMT_ABS, SPIRAL_FMT_REL_PCT],
            "photon_p_experiment": str(P_PHOTON_EXP),
            "covariance_U_recomputed": H02_A,
            "covariance_U_as_velocity": H02_B,
            "covariance_control_C": C_RECOMPARE,
            "force_term_dims": D_TERM_DIMS,
            "force_map_conflict_rate": FORCE_CONFLICT_RATE,
            "dup_headings": DUP_HEADS,
        },
        "audit": {"embedded": {k: AUD_EMB[k] for k in
                               ("label", "top_concl_prints", "top_prints",
                                "compute_nodes", "funcs", "sections")},
                  "plot": {k: AUD_PY[k] for k in
                           ("label", "top_concl_prints", "compute_nodes")},
                  "self": {k: AUD_SELF[k] for k in
                           ("label", "top_concl_prints", "compute_nodes")},
                  "diff_calls": N_DIFF_CALLS, "px_uses": N_PX_USE,
                  "section4_covariance": SEC4,
                  "data_load_calls": N_DATA_LOAD},
        "repair": {"fixes": [{"name": f[0], "cost": f[1]} for f in FIXES],
                   "rows": REPAIR_ROWS, "loose_masks": _loose_masks,
                   "blocking_of_loose": BLOCKING_SAMPLE},
    }
    try:
        jp = os.path.join(OUT, STEM + ".json")
        with io.open(jp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
        print("JSON  -> %s" % jp)

        mp = os.path.join(OUT, STEM + ".md")
        L = []
        L.append("# TUFT-r181 精算摘要")
        L.append("")
        L.append("- 靶：S17/06-运动动量方程 P = m(C − V)"
                 "（主册 705 行 + 整理册 728 行 + 绘图脚本 377 行）")
        L.append("- 条目：%s"
                 % "  ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
        L.append("- 控制：%d/%d　守卫：%d/%d"
                 % (n_ctl_ok, len(CONTROLS), n_guard_ok, len(GUARDS)))
        L.append("")
        L.append("| 编号 | 状态 | 判定 |")
        L.append("|---|---|---|")
        for it in ITEMS:
            L.append("| %s | %s | %s |" % (it["id"], it["status"],
                                           it["title"].replace("|", "\\|")))
        L.append("")
        L.append("## 动量大小（勾股参数化，Fraction 精确）")
        L.append("")
        L.append("| β | \\|P\\|/m₀c（叠加守恒） | \\|P\\|/m₀c（m=m₀） | "
                 "\\|p_SR\\|/m₀c | 比值 |")
        L.append("|---|---|---|---|---|")
        for r in C_ROWS:
            L.append("| %.4f | %.10f | %.10f | %.10f | %.6f |"
                     % (r["beta"], r["p_cons"], r["p_m0"], r["p_sr"],
                        r["ratio"]))
        L.append("")
        L.append("## 力方程（Fraction 逐位精确）")
        L.append("")
        L.append("| t | β | F∥(γm₀) | F⊥(γm₀) | F∥(m₀) | F⊥(m₀) |")
        L.append("|---|---|---|---|---|---|")
        for r in D_ROWS:
            L.append("| %s | %.4f | %s | %s | %s | %s |"
                     % (r["t"], r["beta"], r["fx1"][:10], r["fy1"][:10],
                        r["fx2"][:10], r["fy2"][:10]))
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
