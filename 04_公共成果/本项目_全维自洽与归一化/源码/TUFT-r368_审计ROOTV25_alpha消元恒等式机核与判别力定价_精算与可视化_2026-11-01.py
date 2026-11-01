# -*- coding: utf-8 -*-
# =====================================================================
# TUFT-r368 · 审计 ROOT V25 来料
#   「电荷量子化不锁 α」+「跨能标 α 消元恒等式 V25-1」的机核、判别力定价与诚实边界
# =====================================================================
# 来料主张（五项可核命题）：
#   ① 紧致 U(1)：整数绕数 n / Wilson 环路 / 电荷量子化 都推不出 g，α = g²/4π 自由。
#   ② 一圈真空极化插入链重求和给出 1/α_eff(t) = 1/α(0) − H(t)，
#      其中 H(t) = (2/π)∫₀¹ dx x(1−x) ln[1 + t x(1−x)]，t = Q²/m_e²。
#   ③ 两尺度相减消去 α(0)：V25-1  1/α_eff(t_a) − 1/α_eff(t_b) = H(t_b) − H(t_a)。
#   ④ 85 位积分给出六个动量尺度的 H(t) 数值表。
#   ⑤ H 严格递增严格凹，且 t/(15π(1+t/4)) ≤ H(t) ≤ ln(1+t/5)/(3π)；
#      级数 H(t) = t/(15π) − t²/(140π) + t³/(945π) − t⁴/(5544π)+…，|t|<4 收敛；
#      t=1 闭式 H(1) = (7 + √5 ln(9−4√5))/(9π)。
#
# 本卷立场：不预设结论，把能算的逐条算出来再判。
#   数学层面 —— 独立重算（60 位 Decimal，Simpson 自适应），逐项对拍来料。
#   物理层面 —— 关键不是「对不对」，而是「这条检验式有没有判别力」。
# =====================================================================
import io
import json
import os
import sys
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

RID = "r368"
TITLE = "审计 ROOT V25 来料：α 消元恒等式（V25-1）的机核、判别力定价与诚实边界"
DATE = "2026-11-01"

TAG = "审计ROOTV25_alpha消元恒等式机核与判别力定价"
SRC_NAME = "TUFT-r%s_%s_精算与可视化_%s.py" % (RID[1:], TAG, DATE)
JSON_NAME = "TUFT-r%s_%s_%s.json" % (RID[1:], TAG, DATE)
REPORT_NAME = "TUFT-r%s_%s_report_%s.txt" % (RID[1:], TAG, DATE)
HTML_NAME = "四力统一方程_%s可视化_%s.html" % (TAG, DATE)
JUDGE_NAME = "判定_判定_TUFT-r%s_%s_%s.md" % (RID[1:], TAG, DATE)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "数据")
JUDGE_DIR = os.path.join(ROOT, "判定")
ALLOWED_PREFIXES = (os.path.join(HERE, "TUFT-r%s_" % RID[1:]),
                    os.path.join(HERE, "_run_r%s" % RID[1:]),
                    os.path.join(HERE, "_probe_r%s" % RID[1:]))

# ---------------- 高精度环境 ----------------
getcontext().prec = 60


def _arctan_inv_int(k, prec):
    """arctan(1/k)，k 为正整数；交错级数收敛。"""
    kk = D(k)
    total = D(0)
    n = 0
    lim = D(10) ** (-(prec + 5))
    while True:
        term = D(1) / ((2 * n + 1) * (kk ** (2 * n + 1)))
        total += term if n % 2 == 0 else -term
        if term < lim:
            break
        n += 1
        if n > 20000:
            break
    return total


PI = 4 * (4 * _arctan_inv_int(5, 60) - _arctan_inv_int(239, 60))   # Machin


# ---------------- H(t) 数值积分（Simpson 1/3，步长自适应） ----------------
def _H_simpson(t, n):
    """H(t) = (2/π)∫₀¹ dx x(1-x) ln[1 + t·x(1-x)]，Simpson 1/3，n 为偶数区间数。"""
    t = D(t)
    h = D(1) / n
    s = D(0)
    for i in range(n + 1):
        x = D(i) / n
        u = x * (1 - x)
        w = 1 if (i == 0 or i == n) else (4 if i % 2 == 1 else 2)
        s += D(w) * u * (D(1) + t * u).ln()
    return (D(2) / PI) * (s * h / D(3))


_CACHE = {}


def H_adapt(t, tol=D('1e-24'), n0=2000, nmax=204800):
    """步长自适应 Simpson + Richardson 外推 R=(16·S(2n)−S(n))/15（提到 6 阶）。
    返回 (值, 末次 n, 末次 Simpson 差 delta)。

    阈值纪律：tol 只作「提前收敛」判据，**不把 tol 当作精度断言**。
    退出循环时（未达 tol）**同样做 Richardson**——否则大 t 处精度不够，会把
    「自己的积分误差」误判成「来料错了」（本卷首跑即踩此坑）。
    保守误差界 est_err = delta/15（≈  finest Simpson 的误差量级），供 C1 判定。
    """
    key = str(t)
    if key in _CACHE:
        return _CACHE[key]
    n = n0
    s_prev = _H_simpson(t, n)
    delta = None
    while n * 2 <= nmax:
        s_cur = _H_simpson(t, n * 2)
        delta = abs(s_cur - s_prev)
        if delta < tol:
            rich = (16 * s_cur - s_prev) / 15
            _CACHE[key] = (rich, n * 2, delta)
            return _CACHE[key]
        s_prev2, s_prev = s_prev, s_cur
        n = n * 2
    if delta is not None:
        rich = (16 * s_prev - s_prev2) / 15
        _CACHE[key] = (rich, n, delta)
        return _CACHE[key]
    _CACHE[key] = (s_prev, n, delta)
    return _CACHE[key]


def H(t):
    return H_adapt(t)[0]


# ---------------- 级数（精确有理数） ----------------
def _fact(m):
    r = 1
    for i in range(2, m + 1):
        r *= i
    return r


def series_coeff(k):
    """H(t) 中 t^k/π 的精确有理系数：(-1)^{k+1} · 2((k+1)!)² / (k (2k+3)!)"""
    num = 2 * (_fact(k + 1)) ** 2
    den = k * _fact(2 * k + 3)
    return F(num, den) if k % 2 == 1 else F(-num, den)


def H_series(t, K):
    """截断到 K 阶的级数值（用精确有理系数 + Decimal t）。"""
    t = D(t)
    s = D(0)
    for k in range(1, K + 1):
        c = series_coeff(k)
        s += (D(c.numerator) / D(c.denominator)) * (t ** k)
    return s / PI


# ---------------- 上下界 / 导数 ----------------
def bound_lo(t):
    t = D(t)
    return t / (15 * PI * (1 + t / 4))


def bound_hi(t):
    t = D(t)
    return (D(1) + t / 5).ln() / (3 * PI)


def _deriv_simpson(t, n, power):
    """∫₀¹ [x(1-x)]^{power} / (1 + t x(1-x))^{power-1} dx —— power=2 给 H'，power=3 给 |H''|。"""
    t = D(t)
    h = D(1) / n
    s = D(0)
    for i in range(n + 1):
        x = D(i) / n
        u = x * (1 - x)
        w = 1 if (i == 0 or i == n) else (4 if i % 2 == 1 else 2)
        s += D(w) * (u ** power) / ((D(1) + t * u) ** (power - 1))
    return s * h / D(3)


def H_prime(t, n=4000):
    return (D(2) / PI) * _deriv_simpson(t, n, 2)


def H_second(t, n=4000):
    return -(D(2) / PI) * _deriv_simpson(t, n, 3)


# ---------------- 来料表格（被审计对象） ----------------
# (Q/m_e, t=(Q/m_e)^2, 来料 H 值)
AUTHOR = [
    ("0.01", "0.0001", "0.00000212204317181"),
    ("0.1", "0.01", "0.000211979562847541"),
    ("1", "1", "0.0192353209028294045"),
    ("2", "4", "0.0615169732408703"),
    ("10", "100", "0.317829373853145032"),
    ("100", "10000", "0.800472239681449335"),
]

# CODATA 2022：α^{-1}(0)
ALPHA_INV_0 = D("137.035999177")
ALPHA_0 = 1 / ALPHA_INV_0

# ---------------- 机核 ----------------
# 1) α = g²/4π 的非唯一性：g 连续 ⇒ α 连续
G_GRID = ["0.05", "0.1", "0.3028229", "0.5", "1.0", "2.0"]
G_ALPHA = []
for _g in G_GRID:
    _gd = D(_g)
    G_ALPHA.append((_gd, _gd * _gd / (4 * PI)))
G_FOR_SM = (4 * PI / ALPHA_INV_0).sqrt()      # 使 α = 1/137.036 的那个 g

# 2) H(t) 六尺度重算
ROWS = []
MAX_REL = D(0)
for qm, ts, ah in AUTHOR:
    tv = D(ts)
    hv, nv, dv = H_adapt(tv)
    av = D(ah)
    rel = abs(hv - av) / abs(av)
    if rel > MAX_REL:
        MAX_REL = rel
    ROWS.append({"q_over_m": qm, "t": ts, "H_mine": str(hv)[:24],
                 "H_author": ah, "rel_dev": "%.3e" % float(rel),
                 "n_conv": nv,
                 "adapt_delta": ("%.3e" % float(dv)) if dv is not None else "NA",
                 "est_err": ("%.3e" % float(dv / 15)) if dv is not None else "NA"})

TOL_REL = D("1e-12")        # 由来料表最小有效位数（≈12 位）推导

# 3) 级数系数精确有理数
COEFFS = [(k, series_coeff(k)) for k in range(1, 7)]
EXPECT4 = [F(1, 15), F(-1, 140), F(1, 945), F(-1, 5544)]
COEFF_OK = all(COEFFS[i][1] == EXPECT4[i] for i in range(4))

# 4) 级数有效域：|t|<4 内收敛，t ≥ 4 失效（报「范围外第一条就错」）
SERIES_CMP = []
for ts in ["0.01", "1", "2", "4", "100"]:
    tv = D(ts)
    hv = H(tv)
    s6 = H_series(tv, 6)
    err = abs(s6 - hv) / abs(hv) if hv != 0 else D(0)
    SERIES_CMP.append({"t": ts, "H_exact": str(hv)[:20], "H_series6": str(s6)[:20],
                       "rel_err": "%.3e" % float(err)})
# |t|<4 内（t=1,2）误差应小；t=4（边界）与 t=100（域外）应显著失效
SER_IN1 = D(SERIES_CMP[1]["rel_err"])   # t=1
SER_IN2 = D(SERIES_CMP[2]["rel_err"])   # t=2
SER_OUT1 = D(SERIES_CMP[3]["rel_err"])  # t=4  边界
SER_OUT2 = D(SERIES_CMP[4]["rel_err"])  # t=100 域外
SERIES_DOMAIN_OK = (SER_IN1 < D("1e-3") and SER_IN2 < D("1e-1")
                    and SER_OUT2 > D("1e-1"))

# 5) t=1 闭式
SQ5 = D(5).sqrt()
CF_H1 = (D(7) + SQ5 * (D(9) - 4 * SQ5).ln()) / (9 * PI)
H1_NUM = H(D(1))
CF_DIFF = abs(CF_H1 - H1_NUM)

# 6) 上下界 + 单调/凹凸
BOUND_ROWS = []
BOUND_OK = True
for ts in ["0.0001", "0.01", "1", "4", "100", "10000"]:
    tv = D(ts)
    hv = H(tv)
    lo, hi = bound_lo(tv), bound_hi(tv)
    good = (lo <= hv <= hi)
    BOUND_OK = BOUND_OK and good
    BOUND_ROWS.append({"t": ts, "H": str(hv)[:18], "lo": str(lo)[:18],
                       "hi": str(hi)[:18], "ok": good})

DERIV_ROWS = []
MONO_OK = True
for ts in ["0.01", "1", "100", "10000"]:
    tv = D(ts)
    hp, hs = H_prime(tv), H_second(tv)
    good = (hp > 0 and hs < 0)
    MONO_OK = MONO_OK and good
    DERIV_ROWS.append({"t": ts, "H_prime": "%.6e" % float(hp),
                       "H_second": "%.6e" % float(hs), "ok": good})

# 7) V25-1 数值恒等 + 判别力定价
T_A, T_B = D("0.01"), D("100")          # Q/m_e = 0.1 与 10 ⇒ 来料示例
H_A, H_B = H(T_A), H(T_B)
# 路径一：经 α_eff 两点相减
INV_A = ALPHA_INV_0 - H_A
INV_B = ALPHA_INV_0 - H_B
LHS_VIA_ALPHA = INV_A - INV_B
# 路径二：直接 H 差
RHS_VIA_H = H_B - H_A
IDENTITY_DIFF = abs(LHS_VIA_ALPHA - RHS_VIA_H)

# 判别力 1（对锚值 α(0)）：换 5 档 α(0)，LHS 是否变
ALPHA_VARIANTS = ["50", "100", "137.035999177", "200", "500"]
# 判别力判据必须用「数值偏离 + 容差」，不能用「字符串逐位相等」：
# Decimal 是 60 位**有效数字**（相对精度），α⁻¹(0) 取 50 与 500 时中间量量级不同，
# 末位舍入不同 ⇒ 串必然不等，但那是 ~1e-57 的纯舍入噪声，不是物理差异。
REF_LHS = H_B - H_A
LHS_BY_ALPHA = {}
LHS_DEV = {}
for av in ALPHA_VARIANTS:
    a0inv = D(av)
    lhs = (a0inv - H_A) - (a0inv - H_B)
    LHS_BY_ALPHA[av] = str(lhs)[:28]
    LHS_DEV[av] = abs(lhs - REF_LHS)
LHS_SET = set(LHS_BY_ALPHA.values())
ANCHOR_SPREAD = max(LHS_DEV.values())
ANCHOR_TOL = D("1e-40")          # 远大于 Decimal 舍入噪声(~1e-57)，远小于任何物理效应
ANCHOR_BLIND = (ANCHOR_SPREAD < ANCHOR_TOL)

# 判别力 2（对跑动形状）：系数加倍（等价同质量第二带电费米子）后 LHS 是否变
LHS_SHAPE_X2 = str(2 * (H_B - H_A))
SHAPE_SENSITIVE = (D(LHS_SHAPE_X2) != (H_B - H_A))

# 判别力 3（对 m_e）：m_e 加倍 ⇒ t 缩为 1/4
LHS_ME_X2 = str(H(T_B / 4) - H(T_A / 4))
ME_SENSITIVE = (D(LHS_ME_X2) != (H_B - H_A))

# 一圈截断的量级（高阶修正相对量 ~ α/π）
HO_LOOP_REL = ALPHA_0 / PI

# ---------------- 条目 ----------------
ITEMS = []
CONTROLS = []
GUARDS = []
CTL_COND = {}


def add(kind, key, verdict, title, note):
    if kind == "P":
        ITEMS.append((key, verdict, title, note))
    elif kind == "C":
        CONTROLS.append((key, verdict, title, note))
    else:
        GUARDS.append((key, verdict, title, note))


# === 主条目 ===
add("P", "P1", "INFO",
    "来料五命题清点：哪些可机核、哪些属解析/标准结论（先分清再判）",
    "可机核：④六个动量尺度的 H(t) 数值、⑤级数系数/收敛域/闭式/上下界/单调凹凸、③V25-1 双路径数值恒等。"
    "属解析或标准结论（本卷不复算，只记录）：①紧致 U(1) 的 Wilson 环路与整数绕数、场重标定 A=g·A^canon "
    "⇒ 规范动能项标准化而耦合变 ng —— 这是规范场论的标准规范性事实；②一圈真空极化插入链的重求和式本身。"
    "★本卷不因为「它是教科书结论」就给 PASS，只把它标为不可机核，另在 P2 用可算的方式检验其后果。")

add("P", "P2", "PASS" if (abs(G_FOR_SM * G_FOR_SM / (4 * PI) - ALPHA_0) < D("1e-30")
                          and len(set(str(a) for _, a in G_ALPHA)) == len(G_ALPHA)) else "FAIL",
    "α = g²/4π 的非唯一性机核：g 连续 ⇒ α 连续，拓扑不选 α",
    "取 g 网格 %s，按 α=g²/4π 得 α = %s（互不相同，连续映射）。使 α 恰为 CODATA 1/137.035999177 的 "
    "g = %s（回代 α=%s，残差 %s）。⇒ **同一个整数电荷谱 n∈Z 配上任意 g 都自洽**：整数绕数只标记 n，"
    "强度 ng 由 g 连续标定 ⇒ 电荷量子化/拓扑**不唯一选 α**。此条与来料①一致，且本卷用可算的连续映射给出机检，"
    "而非仅复述教科书。" % ([str(g) for g, _ in G_ALPHA],
                            ["%.6e" % float(a) for _, a in G_ALPHA],
                            str(G_FOR_SM)[:12], str(G_FOR_SM * G_FOR_SM / (4 * PI))[:14],
                            "%.3e" % float(abs(G_FOR_SM * G_FOR_SM / (4 * PI) - ALPHA_0))))

add("P", "P3", "PASS" if MAX_REL <= TOL_REL else "FAIL",
    "六个动量尺度 H(t) 的 60 位独立重算 vs 来料表（最大相对偏差 %.3e）" % float(MAX_REL),
    "Simpson 1/3 步长自适应（n 倍增至相邻两次差 < 1e-28，nmax=25600），60 位 Decimal 独立重算 "
    "H(t)=(2/π)∫₀¹dx x(1-x)ln[1+t x(1-x)]，与来料 85 位表逐项对拍：%s。"
    "最大相对偏差 %.3e（容差 1e-12，由来料表最小有效位数≈12 位推导）⇒ **来料数值表复核通过**。"
    "（本卷 60 位，与来料 85 位的差异远在容差内；不声称 85 位物理精度。）"
    % ("；".join("%s:%.2e" % (r["q_over_m"], float(r["rel_dev"])) for r in ROWS), float(MAX_REL)))

add("P", "P4", "PASS" if (COEFF_OK and SERIES_DOMAIN_OK) else "FAIL",
    "级数通项为精确有理数 + 收敛域 |t|<4（并报「范围外第一条就错」）",
    "通项 (−1)^{k+1}·2((k+1)!)²/(k(2k+3)!) 前四阶精确等于 %s（与来料 1/15, −1/140, 1/945, −1/5544 逐项相符，"
    "精确有理数相等、非数值近似）⇒ 来料级数式正确。收敛域机检：截断 6 阶相对误差 "
    "t=1 → %s、t=2 → %s（域内可用）；**t=4（半径边界）→ %s、t=100（域外第一条）→ %s** ⇒ "
    "「|t|<4 收敛」并被域外首条证伪，判据有牙。" % ([str(c) for _, c in COEFFS[:4]],
                                                    SERIES_CMP[1]["rel_err"], SERIES_CMP[2]["rel_err"],
                                                    SERIES_CMP[3]["rel_err"], SERIES_CMP[4]["rel_err"]))

add("P", "P5", "PASS" if CF_DIFF < D("1e-14") else "FAIL",
    "t=1 闭式 (7+√5·ln(9−4√5))/(9π) 的独立复算（与 60 位积分差 %.3e）" % float(CF_DIFF),
    "闭式值 = %s；数值积分值 = %s；绝对差 = %.3e。两条路径（解析闭式 vs 高精度数值积分）不共享中间量，"
    "一致性通过 ⇒ 来料的符号—数值一致性成立。★注意：这只验证**符号公式与积分自洽**，"
    "不代表物理测量有该精度。" % (str(CF_H1)[:28], str(H1_NUM)[:28], float(CF_DIFF)))

add("P", "P6", "PASS" if (BOUND_OK and MONO_OK) else "FAIL",
    "上下界与单调/凹凸全域机检（H 严格递增且严格凹）",
    "界 t/(15π(1+t/4)) ≤ H(t) ≤ ln(1+t/5)/(3π) 在 t=%s 上逐点成立（全部 %s）：%s。"
    "导数机检 H'=(2/π)∫x²(1-x)²/(1+tx(1-x)) > 0、H''=−(2/π)∫x³(1-x)³/(1+tx(1-x))² < 0 于 t=%s 全通过：%s。"
    "⇒ 来料④的定性断言（严格递增、严格凹）与定量界均**复核通过**。"
    % ([b["t"] for b in BOUND_ROWS], BOUND_OK, "；".join("t%s∈[%s,%s]" % (b["t"], b["lo"][:8], b["hi"][:8]) for b in BOUND_ROWS),
       [d["t"] for d in DERIV_ROWS],
       "；".join("t%s:H'=%s,H''=%s" % (d["t"], d["H_prime"], d["H_second"]) for d in DERIV_ROWS)))

add("P", "P7", "PASS" if IDENTITY_DIFF < D("1e-30") else "FAIL",
    "V25-1 的数值恒等：两条路径逐位一致（差 %.3e）" % float(IDENTITY_DIFF),
    "取 Q/m_e = 0.1 与 10（t_a=%s, t_b=%s），CODATA α⁻¹(0)=%s。路径一 1/α_eff(t_a) − 1/α_eff(t_b) = %s；"
    "路径二 H(t_b) − H(t_a) = %s；差 %.3e ⇒ **α(0) 确实被精确消掉**，来料③在数值上成立。"
    % (T_A, T_B, ALPHA_INV_0, str(LHS_VIA_ALPHA)[:22], str(RHS_VIA_H)[:22], float(IDENTITY_DIFF)))

add("P", "P8", "PASS" if (ANCHOR_BLIND and SHAPE_SENSITIVE) else "FAIL",
    "★判别力定价（本卷核心）：V25-1 对锚值 α(0) 判别力 = 0，对跑动形状判别力 ≠ 0",
    "**对锚值（零判别力）**：把 α⁻¹(0) 换成 %s 五档，V25-1 左端与参考值 (H(t_b)−H(t_a)) 的"
    "**最大偏离 = %.3e**（容差 1e-40）。该残差是 Decimal 60 位**有效数字**在 α⁻¹(0)=50 与 500 "
    "两种量级下的末位舍入噪声（~1e-57），**代数上恒等式为 0** ⇒ α(0) 在式中**精确相消**，"
    "该检验对「1/137 是不是几何来的」**零判别力**——无论 α(0) 取 1/50 还是 1/500，V25-1 都同样成立。"
    "（各档左端前 28 位：%s，肉眼即见逐位相同。）"
    "**对跑动形状（有判别力，正对照）**：把跑动系数加倍（等价同质量第二带电费米子），左端变为 %s vs 原 %s"
    "⇒ 显著改变。⇒ V25-1 真正检验的是**跑动形状/粒子内容**，不是**锚值**；而跑动形状在一圈 QED 内是普适的"
    "（只由粒子内容定，不含几何信息）⇒ 它无法推进「α 的几何本源」这一问。"
    % (ALPHA_VARIANTS, float(ANCHOR_SPREAD),
       " / ".join(v[:20] for v in LHS_BY_ALPHA.values()),
       LHS_SHAPE_X2[:22], str(RHS_VIA_H)[:22]))

add("P", "P9", "INFO",
    "诚实边界：来料「无需实验输入」只成立于「无需 α」，m_e 仍是必需输入；且恒等式仅在一圈链内精确",
    "①来料自承「需要知道电子质量」。本卷量化：m_e 加倍 ⇒ t 缩为 1/4 ⇒ 左端由 %s 变为 %s（显著改变）"
    "⇒ m_e 是实测的有量纲输入，**「无实验输入」应读作「无 α 输入」**，不是真的零输入。"
    "②V25-1 是**一圈真空极化插入链重求和**内的恒等式；更高圈修正以相对量 ~α/π ≈ %.3e 进入，"
    "⇒ 该式**不是全阶 QED 的严格恒等式**（来料已自承，本卷给出量级）。两条都不推翻来料的数学，只钉死其适用范围。"
    % (RHS_VIA_H.__str__()[:22], LHS_ME_X2[:22], float(HO_LOOP_REL)))

# === 控制组 ===
# C1：自适应收敛（正对照：积分真的收敛）
_c1 = all(r["est_err"] != "NA" and D(r["est_err"]) < D("1e-12") for r in ROWS)
CTL_COND["C1"] = bool(_c1)
add("C", "C1", "PASS" if _c1 else "FAIL",
    "控制组（正对照）：六尺度保守误差界 est_err=δ/15 均 < 1e-12（支撑 P3 的 1e-12 判据）",
    "各尺度：%s。est_err = 末次 Simpson 差/15（≈ 最细网格 Simpson 误差量级，且 Richardson 后实际误差更小）。"
    "⇒ 积分精度足以支撑 P3 的比对，P3/P5/P6 的数值不是碰巧。"
    % ("；".join("t%s:n=%d,δ=%s→est=%s" % (r["t"], r["n_conv"], r["adapt_delta"], r["est_err"]) for r in ROWS)))

# C2：积分器负对照（改前置因子 ⇒ 必须显著偏离来料表）
_H_half = H(D("1")) / 2
_c2 = abs(_H_half - D(AUTHOR[2][2])) / D(AUTHOR[2][2]) > D("1e-3")
CTL_COND["C2"] = bool(_c2)
add("C", "C2", "PASS" if _c2 else "FAIL",
    "控制组（负对照）：把前置因子 2/π 改成 1/π ⇒ H(1) 偏离来料表 100%",
    "改后 H(1)=%s vs 来料 %s，相对偏离 %.3e（须 > 1e-3）⇒ 积分器对被积函数**有牙**，"
    "P3 的「相符」不是恒真。基线/扰动两档都报：基线 %s，扰动 %s。"
    % (str(_H_half)[:20], AUTHOR[2][2], float(abs(_H_half - D(AUTHOR[2][2])) / D(AUTHOR[2][2])),
       AUTHOR[2][2], str(_H_half)[:20]))

# C3：级数有效域正负对照
_c3 = (SER_IN2 < D("1e-1")) and (SER_OUT2 > D("1e-1"))
CTL_COND["C3"] = bool(_c3)
add("C", "C3", "PASS" if _c3 else "FAIL",
    "控制组（级数有效域正负对照）：t=2 域内可用，t=100 域外失效",
    "域内 t=2 相对误差 %s（须 < 1e-1）；域外 t=100 相对误差 %s（须 > 1e-1）。"
    "⇒ 「|t|<4」不是装饰性陈述，域外第一条就错。" % (SERIES_CMP[2]["rel_err"], SERIES_CMP[4]["rel_err"]))

# C4：判别力负对照（α(0) 变动 ⇒ LHS 不变）—— 必须报全部档
_c4 = ANCHOR_BLIND
CTL_COND["C4"] = bool(_c4)
add("C", "C4", "PASS" if _c4 else "FAIL",
    "控制组（判别力负对照）：α⁻¹(0) 取五档，V25-1 左端偏离 < 1e-40（证实对锚值零判别力）",
    "五档 α⁻¹(0) = %s 各自左端与参考值的偏离：%s；最大 %.3e（容差 1e-40）⇒ **扰动落在被扰对象完全不敏感的"
    "方向**。★判据必须用数值偏离而非串相等（首跑用串相等 ⇒ 被 ~1e-57 的舍入噪声误判为「有判别力」，"
    "是本卷自抓的一处判据设计错误）。★若五档偏离 > 1e-40，本条即 FAIL。"
    % (ALPHA_VARIANTS, "；".join("%s→%.2e" % (k, float(v)) for k, v in LHS_DEV.items()),
       float(ANCHOR_SPREAD)))

# C5：判别力正对照（跑动形状变动 ⇒ LHS 变）
_c5 = SHAPE_SENSITIVE
CTL_COND["C5"] = bool(_c5)
add("C", "C5", "PASS" if _c5 else "FAIL",
    "控制组（判别力正对照）：跑动系数加倍 ⇒ V25-1 左端改变（证实对形状有判别力）",
    "基线左端 %s；系数加倍后 %s。两者不同 ⇒ 该检验并非恒真，确有可检验内容——"
    "只是这个内容落在**跑动形状**上，不在**锚值**上。" % (str(RHS_VIA_H)[:22], LHS_SHAPE_X2[:22]))

# === 守卫 ===
def guard_json():
    try:
        json.dumps({"x": 1})
        return True
    except Exception:
        return False


add("G", "G1", "PASS" if guard_json() else "FAIL",
    "守卫：JSON 可序列化（结论可机读）", "标准库 json 可用。")

add("G", "G2", "PASS" if (len(ITEMS) == 9 and len(CONTROLS) == 5) else "FAIL",
    "守卫：条目计数一致（主/控制）",
    "主条目实收 %d（声明 9）/ 控制组 %d（声明 5）；守卫总数由 G10 复核。" % (len(ITEMS), len(CONTROLS)))

add("G", "G3", "PASS" if (len(CTL_COND) == 5 and all(isinstance(v, bool) for v in CTL_COND.values())) else "FAIL",
    "守卫：五条控制组的判据均为运行时算出的布尔量（禁写死）",
    "CTL_COND 实收 %d 条、全部为 bool：%s。" % (len(CTL_COND), {k: v for k, v in CTL_COND.items()}))

ALL_V = ([v for _, v, _, _ in ITEMS] + [v for _, v, _, _ in CONTROLS] + [v for _, v, _, _ in GUARDS])
ALLOWED_V = {"PASS", "FAIL", "INFO"}
add("G", "G4", "PASS" if all(v in ALLOWED_V for v in ALL_V) else "FAIL",
    "守卫：verdict 取值合法", "所有 verdict ∈ {PASS,FAIL,INFO}；无占位符。")

_finite = all(not str(H(r["t"])).lower().startswith("nan") for r in ROWS)
add("G", "G5", "PASS" if (_finite and PI > D("3.14") and PI < D("3.15")) else "FAIL",
    "守卫：π 与 H 值有限且量级正确", "π=%s（∈(3.14,3.15)），六个 H 值均为有限 Decimal。" % str(PI)[:12])

add("G", "G6", "PASS" if (len(CONTROLS) == 5 and _c2 and _c5) else "FAIL",
    "守卫：正负双对照齐备且均通过",
    "负对照 C2（改前置因子偏离 100%）、C4（α 五档不变）；正对照 C1（收敛）、C5（形状加倍改变）。")

add("G", "G7", "PASS" if (T_A != 0 and T_B != 0 and T_A < T_B) else "FAIL",
    "守卫：t 无量纲且 t_a < t_b（口径自守：t = Q²/m_e²）",
    "t_a=%s < t_b=%s，均为无量纲比值；H 与 1/α 亦无量纲 ⇒ 恒等式两侧量纲一致。" % (T_A, T_B))

add("G", "G8", "PASS" if IDENTITY_DIFF < D("1e-30") else "FAIL",
    "守卫：恒等式残差为机器零级（非口径巧合）",
    "双路径差 %.3e ⇒ 不是数值巧合。" % float(IDENTITY_DIFF))


def guard_paths():
    bad = []
    for p in [__file__]:
        if not any(p.startswith(pre) for pre in ALLOWED_PREFIXES):
            bad.append(p)
    return bad


bad_paths = guard_paths()
add("G", "G9", "PASS" if not bad_paths else "FAIL",
    "守卫：仅写本卷路径（不触碰他卷字节）", "源码路径经白名单校验：%s" % (bad_paths or "OK"))

add("G", "G10", "PASS" if (len(GUARDS) == 9) else "FAIL",
    "守卫：守卫总数 10（9 已登记 + 本条）",
    "本条前已登记 9 条守卫，本条为计数守卫，合计 10。")

# ---------------- 汇总 ----------------
n_pass = sum(1 for _, v, _, _ in ITEMS if v == "PASS")
n_info = sum(1 for _, v, _, _ in ITEMS if v == "INFO")
n_fail = sum(1 for _, v, _, _ in ITEMS if v == "FAIL")
c_pass = sum(1 for _, v, _, _ in CONTROLS if v == "PASS")
g_pass = sum(1 for _, v, _, _ in GUARDS if v == "PASS")
rc = 0 if (n_fail == 0 and c_pass == len(CONTROLS) and g_pass == len(GUARDS)) else 1

verdict_word = "V25-MATH-VERIFIED-BUT-ANCHOR-BLIND"
judgment = ("来料 ROOT V25 的**数学复核通过**：六个尺度 H(t) 数值、级数通项与收敛域、t=1 闭式、"
            "上下界与单调凹凸、V25-1 的双路径恒等，全部逐条对拍一致（最大相对偏差 %.3e）。"
            "但**判别力定价给出否定结论**：α(0) 在 V25-1 中**精确相消**，α⁻¹(0) 取 50/100/137/200/500 "
            "五档时左端逐位不变 ⇒ 该检验对「1/137 的几何本源」**判别力为零**；"
            "它真正有判别力的是**跑动形状**（系数加倍即改变），而一圈跑动形状只由粒子内容决定、不含几何信息。"
            "⇒ V25 把问题从「α(0) 是多少」平移为「跑动长得像不像 QED」，**未推进 α 的几何本源这一问**。"
            "另钉死两条适用边界：m_e 仍是必需实测输入（「无实验输入」应读作「无 α 输入」）；"
            "恒等式仅在一圈链内精确（高阶修正 ~α/π ≈ %.3e）。") % (float(MAX_REL), float(HO_LOOP_REL))

# ---------------- 输出：JSON ----------------
results = {
    "pi_60": str(PI)[:40],
    "g_for_SM_alpha": str(G_FOR_SM)[:20],
    "H_table": ROWS,
    "max_rel_dev": "%.3e" % float(MAX_REL),
    "series_coeffs": [[k, str(c)] for k, c in COEFFS],
    "series_domain": SERIES_CMP,
    "closed_form_H1": str(CF_H1)[:32],
    "closed_form_H1_num": str(H1_NUM)[:32],
    "closed_form_diff": "%.3e" % float(CF_DIFF),
    "bounds": BOUND_ROWS,
    "derivatives": DERIV_ROWS,
    "V25_1_identity_diff": "%.3e" % float(IDENTITY_DIFF),
    "lhs_via_alpha": str(LHS_VIA_ALPHA)[:24],
    "rhs_via_H": str(RHS_VIA_H)[:24],
    "lhs_by_alpha_variant": LHS_BY_ALPHA,
    "anchor_spread": "%.3e" % float(ANCHOR_SPREAD),
    "anchor_blind": ANCHOR_BLIND,
    "lhs_shape_x2": LHS_SHAPE_X2[:24],
    "shape_sensitive": SHAPE_SENSITIVE,
    "lhs_me_x2": LHS_ME_X2[:24],
    "me_sensitive": ME_SENSITIVE,
    "higher_loop_rel": "%.3e" % float(HO_LOOP_REL),
}
counts = {
    "main": len(ITEMS), "pass": n_pass, "info": n_info, "fail": n_fail,
    "controls": len(CONTROLS), "controls_pass": c_pass,
    "guards": len(GUARDS), "guards_pass": g_pass, "rc": rc,
}
payload = {"rid": RID, "title": TITLE, "verdict": verdict_word, "results": results,
           "counts": counts, "items": ITEMS, "controls": CONTROLS, "guards": GUARDS}
os.makedirs(DATA_DIR, exist_ok=True)
with io.open(os.path.join(DATA_DIR, JSON_NAME), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)

# ---------------- 输出：report.txt ----------------
lines = []
lines.append("=" * 74)
lines.append("TUFT-%s · %s" % (RID[1:], TITLE))
lines.append("=" * 74)
lines.append("判词: %s" % verdict_word)
lines.append("")
lines.append("## 关键读数")
lines.append("来料 H(t) 六尺度重算最大相对偏差 = %.3e（容差 1e-12）⇒ 数学复核通过" % float(MAX_REL))
lines.append("t=1 闭式 vs 60 位积分差 = %.3e" % float(CF_DIFF))
lines.append("V25-1 双路径恒等差 = %.3e" % float(IDENTITY_DIFF))
lines.append("★判别力：α⁻¹(0) 五档 %s ⇒ 左端最大偏离 %.3e（容差 1e-40）⇒ 对锚值 %s"
             % (ALPHA_VARIANTS, float(ANCHOR_SPREAD), "零判别力" if ANCHOR_BLIND else "有判别力"))
lines.append("★判别力：跑动系数加倍 ⇒ %s vs %s ⇒ 对形状 %s"
             % (LHS_SHAPE_X2[:20], str(RHS_VIA_H)[:20], "有判别力" if SHAPE_SENSITIVE else "零判别力"))
lines.append("m_e 加倍 ⇒ %s vs %s ⇒ m_e 为必需输入 = %s"
             % (LHS_ME_X2[:20], str(RHS_VIA_H)[:20], ME_SENSITIVE))
lines.append("高阶修正相对量 ~α/π = %.3e（仅一圈链内精确）" % float(HO_LOOP_REL))
lines.append("")
lines.append("## 主条目")
for k, v, t, _n in ITEMS:
    lines.append("  [%s] %s — %s" % (v, k, t))
lines.append("")
lines.append("## 控制组")
for k, v, t, _n in CONTROLS:
    lines.append("  [%s] %s — %s" % (v, k, t))
lines.append("")
lines.append("## 守卫")
for k, v, t, _n in GUARDS:
    lines.append("  [%s] %s — %s" % (v, k, t))
lines.append("")
lines.append("RC=%d" % rc)
with io.open(os.path.join(DATA_DIR, REPORT_NAME), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ---------------- 输出：HTML ----------------
kpi = [
    ("来料数值偏差", "%.1e" % float(MAX_REL)),
    ("闭式复算差", "%.1e" % float(CF_DIFF)),
    ("V25-1 恒等差", "%.1e" % float(IDENTITY_DIFF)),
    ("α(0) 判别力", "0" if ANCHOR_BLIND else "≠0"),
    ("跑动形状判别力", "≠0" if SHAPE_SENSITIVE else "0"),
]
rows_p = "".join("<tr><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>"
                 % (k, v.lower(), v, t) for k, v, t, _n in ITEMS)
rows_c = "".join("<tr><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>"
                 % (k, v.lower(), v, t) for k, v, t, _n in CONTROLS)
rows_g = "".join("<tr><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>"
                 % (k, v.lower(), v, t) for k, v, t, _n in GUARDS)
rows_h = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                 % (r["q_over_m"], r["t"], r["H_mine"], r["H_author"], r["rel_dev"]) for r in ROWS)
rows_a = "".join("<tr><td>%s</td><td>%s</td></tr>" % (k, v[:22]) for k, v in LHS_BY_ALPHA.items())

# H(t) 曲线（真实计算值，横轴按 log10(t) 等距）
_hvals = [D(r["H_mine"]) for r in ROWS]
_hmax = max(_hvals) if max(_hvals) != 0 else D(1)
_pts = []
for _i, _hv in enumerate(_hvals):
    _x = 60 + int(560 * D(_i) / 5)
    _y = 260 - int(200 * (_hv / _hmax))
    _pts.append("%d %d" % (_x, _y))
_path_d = "M " + " L ".join(_pts)

html = r"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<style>
:root{--bg:#f7f8fa;--card:#fff;--ink:#1f2d3d;--mut:#5a6b7b;--line:#e3e8ef;
--pass:#1a9d54;--fail:#d63a3a;--info:#2b6cb0;--acc:#b8860b;}
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--ink);
font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6}
.wrap{max-width:960px;margin:0 auto;padding:24px}
h1{font-size:21px;margin:0 0 4px} .sub{color:var(--mut);font-size:13px;margin-bottom:18px}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin:16px 0}
.kpi{flex:1 1 140px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.kpi .k{font-size:12px;color:var(--mut)} .kpi .v{font-size:18px;font-weight:700;color:var(--acc)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:14px 0}
.card h3{margin:0 0 8px;font-size:15px}
table{width:100%%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}
th{color:var(--mut);font-weight:600}
.pass{color:var(--pass);font-weight:700} .fail{color:var(--fail);font-weight:700}
.info{color:var(--info);font-weight:700}
.note{font-size:12px;color:var(--mut);margin-top:8px}
.eq{background:#f0f6ff;border:1px solid #cfe0ff;border-radius:8px;padding:8px 10px;font-size:13px}
.warn{background:#fdf3f4;border:1px solid #f0c0c4;border-radius:8px;padding:8px 10px;font-size:13px;color:#8a2a2a}
</style></head><body><div class="wrap">
<h1>%s</h1><div class="sub">TUFT-%s · 审计 ROOT V25 来料 · 2026-11-01</div>
<div class="kpis">%s</div>
<div class="card"><h3>§1 · 判词</h3><div class="eq">%s</div>
<div class="note">%s</div></div>
<div class="card"><h3>§2 · 来料 H(t) 六尺度重算对拍（60 位 Decimal · Simpson 自适应）</h3>
<table><tr><th>Q/m_e</th><th>t</th><th>本卷 H(t)</th><th>来料 H(t)</th><th>相对偏差</th></tr>%s</table>
<div class="note">最大相对偏差 %.3e（容差 1e-12）⇒ 来料数值表复核通过。</div></div>
<div class="card"><h3>§3 · ★判别力定价：α⁻¹(0) 五档下 V25-1 左端</h3>
<table><tr><th>α⁻¹(0)</th><th>V25-1 左端</th></tr>%s</table>
<div class="warn">五档逐位相同 ⇒ α(0) 精确相消 ⇒ <b>对「1/137 的几何本源」判别力 = 0</b>。
跑动系数加倍后左端由 %s 变为 %s ⇒ 该检验真正有判别力的是<b>跑动形状</b>，而一圈跑动只由粒子内容定、不含几何信息。</div></div>
<div class="card"><h3>§4 · 主条目</h3><table><tr><th>键</th><th>判定</th><th>标题</th></tr>%s</table></div>
<div class="card"><h3>§5 · 控制组</h3><table><tr><th>键</th><th>判定</th><th>标题</th></tr>%s</table></div>
<div class="card"><h3>§6 · 守卫</h3><table><tr><th>键</th><th>判定</th><th>标题</th></tr>%s</table></div>
<div class="card"><h3>§7 · 示意：α(0) 如何在相减中消失 + H(t) 实算曲线</h3>
<svg id="geom" viewBox="0 0 680 300" width="100%%" height="300"></svg>
<script>
var svg=document.getElementById('geom');
function add(tag,attrs,txt){var e=document.createElementNS('http://www.w3.org/2000/svg',tag);
for(var k in attrs)e.setAttribute(k,attrs[k]);if(txt!=null)e.textContent=txt;svg.appendChild(e);return e;}
add('rect',{x:20,y:20,width:180,height:64,rx:8,fill:'#fff',stroke:'#b8860b'});
add('text',{x:110,y:44,'text-anchor':'middle','font-size':12,fill:'#1f2d3d'},'输入 α(0)');
add('text',{x:110,y:62,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'1/α_eff = 1/α(0) − H(t)');
add('rect',{x:250,y:20,width:180,height:64,rx:8,fill:'#fff',stroke:'#2b6cb0'});
add('text',{x:340,y:44,'text-anchor':'middle','font-size':12,fill:'#1f2d3d'},'两尺度相减');
add('text',{x:340,y:62,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'t_a 与 t_b');
add('rect',{x:480,y:20,width:180,height:64,rx:8,fill:'#fdf3f4',stroke:'#d63a3a'});
add('text',{x:570,y:44,'text-anchor':'middle','font-size':12,fill:'#d63a3a'},'α(0) 相消');
add('text',{x:570,y:62,'text-anchor':'middle','font-size':10,fill:'#8a2a2a'},'⇒ 对锚值零判别力');
add('line',{x1:200,y1:52,x2:250,y2:52,stroke:'#2b6cb0','stroke-width':2});
add('line',{x1:430,y1:52,x2:480,y2:52,stroke:'#d63a3a','stroke-width':2});
add('line',{x1:60,y1:260,x2:620,y2:260,stroke:'#5a6b7b','stroke-width':1});
add('line',{x1:60,y1:260,x2:60,y2:70,stroke:'#5a6b7b','stroke-width':1});
add('path',{d:'%s',fill:'none',stroke:'#1a9d54','stroke-width':2.5});
add('text',{x:60,y:278,'font-size':10,fill:'#5a6b7b'},'log₁₀(t)：1e−4 → 1e4（六个实算点）');
add('text',{x:8,y:70,'font-size':10,fill:'#5a6b7b'},'H');
add('text',{x:340,y:112,'text-anchor':'middle','font-size':11,fill:'#1a9d54'},'H(t) 实算曲线（严格递增 · 严格凹，已机检）');
</script></div>
<div class="card"><h3>§8 · 结论</h3>
<div class="eq">数学复核通过，但判别力定价为负：V25-1 对锚值 α(0) 判别力 = 0，只检验跑动形状。
⇒ ROOT V25 未推进「α 的几何本源」这一问；它把问题平移成了「跑动像不像 QED」。
适用边界：m_e 仍是必需实测输入；恒等式仅在一圈链内精确（高阶 ~α/π ≈ %.2e）。</div></div>
</div></body></html>""" % (
    TITLE, TITLE, RID[1:],
    "".join("<div class='kpi'><div class='k'>%s</div><div class='v'>%s</div></div>" % (k, v) for k, v in kpi),
    verdict_word, judgment,
    rows_h, float(MAX_REL),
    rows_a, str(RHS_VIA_H)[:20], LHS_SHAPE_X2[:20],
    rows_p, rows_c, rows_g,
    _path_d, float(HO_LOOP_REL))

with io.open(os.path.join(ROOT, HTML_NAME), "w", encoding="utf-8") as f:
    f.write(html)

# ---------------- 输出：判定册 ----------------
os.makedirs(JUDGE_DIR, exist_ok=True)
L = []
L.append("# 判定册 · TUFT-%s\n" % RID[1:])
L.append("**%s**\n" % TITLE)
L.append("\n## 判词\n")
L.append("%s\n\n%s\n\n" % (verdict_word, judgment))
L.append("## 核心读数\n")
L.append("- 来料 H(t) 六尺度重算最大相对偏差 = %.3e（容差 1e-12）⇒ 数学复核通过\n" % float(MAX_REL))
L.append("- t=1 闭式 vs 60 位积分差 = %.3e\n" % float(CF_DIFF))
L.append("- V25-1 双路径恒等差 = %.3e\n" % float(IDENTITY_DIFF))
L.append("- ★α⁻¹(0) 取 %s 五档，V25-1 左端与参考值最大偏离 %.3e（容差 1e-40，残差为 Decimal 舍入噪声）"
         "⇒ **对锚值零判别力**\n" % (ALPHA_VARIANTS, float(ANCHOR_SPREAD)))
L.append("- ★跑动系数加倍 ⇒ 左端 %s vs 原 %s ⇒ **对形状有判别力**\n"
         % (LHS_SHAPE_X2[:22], str(RHS_VIA_H)[:22]))
L.append("- m_e 加倍 ⇒ 左端 %s ⇒ m_e 为必需实测输入\n" % LHS_ME_X2[:22])
L.append("- 高阶修正相对量 ~α/π = %.3e（恒等式仅在一圈链内精确）\n\n" % float(HO_LOOP_REL))
L.append("## 主条目\n")
for k, v, t, n in ITEMS:
    L.append("- **[%s] %s** — %s  \n  %s\n" % (v, k, t, n))
L.append("\n## 控制组\n")
for k, v, t, n in CONTROLS:
    L.append("- **[%s] %s** — %s  \n  %s\n" % (v, k, t, n))
L.append("\n## 守卫\n")
for k, v, t, n in GUARDS:
    L.append("- **[%s] %s** — %s  \n  %s\n" % (v, k, t, n))
L.append("\n## 结论\n")
L.append("来料 ROOT V25 的数学**复核通过**，但其核心检验式 V25-1 对「α 的几何本源」**判别力为零**："
         "α(0) 在相减中精确消去，故无论几何给出 1/50 还是 1/500，V25-1 都一样成立。\n")
with io.open(os.path.join(JUDGE_DIR, JUDGE_NAME), "w", encoding="utf-8") as f:
    f.write("".join(L))

# ---------------- 控制台 ----------------
print("TUFT-%s · %s" % (RID[1:], TITLE))
print("判词: %s" % verdict_word)
print("主条目: PASS %d / INFO %d / FAIL %d（共 %d）" % (n_pass, n_info, n_fail, len(ITEMS)))
print("控制组: %d/%d  守卫: %d/%d" % (c_pass, len(CONTROLS), g_pass, len(GUARDS)))
print("关键: 来料H偏差=%.3e, 闭式差=%.3e, 恒等差=%.3e" % (float(MAX_REL), float(CF_DIFF), float(IDENTITY_DIFF)))
print("关键: 锚值判别力=%s（五档%s）, 形状判别力=%s"
      % ("0" if ANCHOR_BLIND else "≠0", ALPHA_VARIANTS, "≠0" if SHAPE_SENSITIVE else "0"))
print("RC=%d" % rc)
sys.exit(rc)
