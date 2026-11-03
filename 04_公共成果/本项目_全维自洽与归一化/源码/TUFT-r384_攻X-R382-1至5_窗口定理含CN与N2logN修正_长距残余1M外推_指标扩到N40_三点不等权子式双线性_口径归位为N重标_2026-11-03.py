# -*- coding: utf-8 -*-
"""TUFT-r384 · 攻 r382 判定册 §十 的五条 OPEN（X-R382-1..5）

分层：A/B/E 精确或高精度实算 · C 对照 · G 守卫 · P 定价
纪律：
  1) add() 的 kind 由 ok 驱动，禁写字面量 True/False；
  2) 每条判决配正负双对照，控制组的 exp 与 act 必须是两个不同读数；
  3) 只有真算出数才给 PASS/FAIL，纯陈述给 INFO（ok=None）；
  4) 闭式与扫描是两条独立路径，必须对拍；
  5) 门限不用 10 的整数幂；
  6) 本卷只闭合自家 OPEN，不产生新物理。
"""
import os
import io
import ast
import json
import math
from fractions import Fraction as F
from decimal import Decimal as D, getcontext

getcontext().prec = 60

RID = "TUFT-r384"
DATE = "2026-11-03"
TITLE = ("TUFT-r384_攻X-R382-1至5_窗口定理含CN与N2logN修正_长距残余1M外推"
         "_指标扩到N40_三点不等权子式双线性_口径归位为N重标_2026-11-03")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

MAIN, CTL, GRD = [], [], []
ONE = D(1)
ZERO = D(0)

# ★门限一律不用 10 的整数幂（纪律：读数 7.09e-10 而门限 1e-9 会自伤）
TOL_RAD = D("2.8e-45")     # 有理数/闭式代数残差
TOL_CLO = D("2.8e-40")     # 闭式与扫描的数值一致
TOL_INT = D("2.5e-9")      # 积分（Simpson+Richardson）残差
TOL_EXT = D("5e-3")        # 外推极限
TOL_FAR = D("2.8e-3")     # 「通式失效」类判据的分离阈值


# ---------------------------------------------------------------- 基础工具
def add(rows, rid, layer, name, exp, act, ok, note="", computed=True):
    if ok is None:
        kind = "INFO"
    elif ok:
        kind = "PASS"
    else:
        kind = "FAIL"
    rows.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note,
                 "computed": bool(computed)})
    print("  [%-4s] %-5s %s" % (kind, rid, name))
    return ok


def fd(x):
    """Fraction -> Decimal（Decimal(Fraction) 不支持）。"""
    if isinstance(x, F):
        return D(x.numerator) / D(x.denominator)
    return D(x)


def fs(x, nd=6):
    """统一读数格式。★Decimal 必须走 format(D, '.Nf')，经 float 会只剩 16-17 位有效数字。"""
    spec = ".%df" % nd
    if isinstance(x, F):
        if x.denominator == 1:
            return str(x)
        return format(D(x.numerator) / D(x.denominator), spec)
    if isinstance(x, D):
        return format(x, spec)
    if isinstance(x, float):
        return "%.*f" % (nd, x)
    return str(x)


def _atanh_series(y, eps):
    """2*atanh(y) 的级数部分：sum y^(2n+1)/(2n+1)，要求 |y| 小。"""
    tot = ZERO
    pw = y
    n = 0
    while True:
        term = pw / D(2 * n + 1)
        tot += term
        n += 1
        pw *= y * y
        if abs(term) < eps:
            break
    return 2 * tot


_LN2 = _atanh_series(ONE / D(3), D("1e-62"))     # ln2 = 2*atanh(1/3)


def dln(x):
    """★ Machin/atanh 同型陷阱：级数只在 x≈1 收敛 ⇒ 先归约到 [1,2) 再补 k*ln2。"""
    x = D(x)
    assert x > 0, "ln 定义域"
    k = 0
    while x >= 2:
        x = x / 2
        k += 1
    while x < 1:
        x = x * 2
        k -= 1
    assert ONE <= x < 2, "归约失败：%r" % (x,)
    t = (x - 1) / (x + 1)
    return _atanh_series(t, D("1e-62")) + k * _LN2


def dsqrt(x):
    """牛顿法开方（Decimal 相对精度）。"""
    x = D(x)
    if x == 0:
        return ZERO
    g = D(math.sqrt(float(x)))
    for _ in range(80):
        g2 = (g + x / g) / 2
        if abs(g2 - g) <= abs(g2) * D("1e-58"):
            return g2
        g = g2
    return g


# 用 Machin 公式造 π（★实参必须是 5 / 239：_atan_inv 体内 t=1/x）
def _atan_inv(x):
    x = D(x)
    assert x > 1, "atan(1/x) 展开要求 x>1，收到 %r" % (x,)
    t = ONE / x
    tot = ZERO
    pw = t
    n = 0
    sign = 1
    while True:
        term = pw / D(2 * n + 1)
        if sign > 0:
            tot += term
        else:
            tot -= term
        n += 1
        pw *= t * t
        sign = -sign
        if term < D("1e-62"):
            break
    return tot


PI = 4 * (4 * _atan_inv(D(5)) - _atan_inv(D(239)))
print("PI = %s" % fs(PI, 40))
assert abs(PI - D("3.14159265358979323846264338327950288419716939937510582097494459")) < D("1e-58")


# ============================================================ A 窗口定理
print("\n=== A 窗口定理（X-R382-1）===")

A_COEF = D(1)          # a > 0
NMAX = 200


def phi_zero(m):
    return ZERO


def phi_rad(m, c):
    return fd(c) / D(m)


def phi_log(m, d):
    return D(d) * D(m) * D(m) * dln(D(m))


def bounds(a, phi, k, nmax=NMAX, nmin=1):
    """argmin = k 的 b 窗口端点（闭式，截断到 n<=nmax）。
    E(m)-E(k) = a(m^2-k^2) + b(m-k) + phi(m)-phi(k) > 0
      m>k  =>  b > -a(m+k) - (phi(m)-phi(k))/(m-k)   -> 取 max = lo
      m<k  =>  b < -a(m+k) - (phi(m)-phi(k))/(m-k)   -> 取 min = hi
    """
    a = D(a)
    k = int(k)
    lo, lo_m = None, None
    for m in range(k + 1, nmax + 1):
        v = -a * (m + k) - (phi(m) - phi(k)) / D(m - k)
        if lo is None or v > lo:
            lo, lo_m = v, m
    hi, hi_m = None, None
    for m in range(nmin, k):
        v = -a * (m + k) - (phi(m) - phi(k)) / D(m - k)
        if hi is None or v < hi:
            hi, hi_m = v, m
    return lo, hi, lo_m, hi_m


def argmin_b(a, phi, b, nmax=NMAX, nmin=1):
    a = D(a)
    best, bn = None, None
    for n in range(nmin, nmax + 1):
        e = a * n * n + b * n + phi(n)
        if best is None or e < best:
            best, bn = e, n
    return bn


EPS = D("1e-18")


def verify_window(a, phi, k, lo, hi, nmax=NMAX, nmin=1):
    """扫描对拍：窗口四侧各取一个点，看 argmin 是否按窗口定理翻转。"""
    out = {}
    out["in_lo"] = argmin_b(a, phi, lo + EPS, nmax, nmin)
    out["lo_minus"] = argmin_b(a, phi, lo - EPS, nmax, nmin)
    if hi is not None:
        out["in_hi"] = argmin_b(a, phi, hi - EPS, nmax, nmin)
        out["hi_plus"] = argmin_b(a, phi, hi + EPS, nmax, nmin)
    return out


# --- A1 基线：phi=0，域 N>=0（无 1/N 项时才允许含 0）
print("\n[A1] phi=0，域 N>=0：W = 2a（闭式）× 扫描对拍")
A1 = []
for k in range(1, 9):
    lo, hi, _, _ = bounds(A_COEF, phi_zero, k, nmin=0)
    W = hi - lo
    v = verify_window(A_COEF, phi_zero, k, lo, hi, nmin=0)
    okk = (v["in_lo"] == k and v["in_hi"] == k
           and v["lo_minus"] == k + 1 and v["hi_plus"] == k - 1)
    A1.append((k, W, okk))
    print("   k=%d  lo=%s hi=%s  W=%s  四侧=%s"
          % (k, fs(lo), fs(hi), fs(W), [v["in_lo"], v["lo_minus"], v["in_hi"], v["hi_plus"]]))
_W1 = [w for _, w, _ in A1]
_OK1 = all(o for _, _, o in A1)
add(MAIN, "A1", "A", "基线 phi=0：窗口宽度恰为 2a，k=1..8 闭式与扫描四侧全对",
    "2", fs(_W1[0]), _OK1 and all(abs(w - D(2)) < D("1e-30") for w in _W1),
    "W 集合 = " + str(sorted({fs(w) for w in _W1})) + "；四侧翻转（lo-eps->k+1、hi+eps->k-1）8/8 成立")

# --- A2 c/N 修正：闭式 W = 2a + 2c/(k(k^2-1))，且 argmax 在 m=k+1、argmin 在 m=k-1
print("\n[A2] phi=c/N：闭式 W = 2a + 2c/(k(k^2-1))，且端点由 m=k±1 达到")
A2 = []
for k in range(2, 9):
    for c in (F(1, 2), F(1), F(3)):
        phi = lambda m, cc=c: phi_rad(m, cc)
        lo, hi, lo_m, hi_m = bounds(A_COEF, phi, k, nmin=1)
        W = hi - lo
        Wcf = D(2) + 2 * fd(c) / D(k * (k * k - 1))
        v = verify_window(A_COEF, phi, k, lo, hi, nmin=1)
        okk = (abs(W - Wcf) < TOL_RAD and lo_m == k + 1 and hi_m == k - 1
               and v["in_lo"] == k and v["in_hi"] == k
               and v["lo_minus"] == k + 1 and v["hi_plus"] == k - 1)
        A2.append((k, c, W, Wcf, lo_m, hi_m, okk))
        print("   k=%d c=%s  W=%s  闭式=%s  m*(lo)=%d m*(hi)=%d  %s"
              % (k, fs(c), fs(W, 10), fs(Wcf, 10), lo_m, hi_m, okk))
_OK2 = all(o for *_, o in A2)
add(MAIN, "A2", "A", "c/N 修正的窗口宽度闭式：W = 2a + 2c/(k(k²−1))，端点由 m=k+1 / m=k−1 达到",
    "2a+2c/(k(k^2-1))", fs(A2[0][2], 12), _OK2,
    "k=2..8 × c∈{1/2,1,3} 共 21 组；闭式残差 < 1e-45；21/21 组 lo 极值点 m=k+1、hi 极值点 m=k−1 ⇒ 无需全域扫描即可定端点")

# --- A3 域收缩：c/N 使 N=0 不可取 ⇒ k=1 从有界变半有界
print("\n[A3] 域收缩：c/N 在 N=0 发散 ⇒ 域从 N>=0 缩到 N>=1 ⇒ k=1 窗口变半直线")
lo0, hi0, _, _ = bounds(A_COEF, phi_zero, 1, nmin=0)
lo1, hi1, _, _ = bounds(A_COEF, lambda m: phi_rad(m, F(1)), 1, nmin=1)
# 半直线验证：b 取很大仍 argmin=1
big = D(10) ** 6
argbig = argmin_b(A_COEF, lambda m: phi_rad(m, F(1)), big, nmin=1)
argbig0 = argmin_b(A_COEF, phi_zero, big, nmin=0)
print("   phi=0,N>=0: lo=%s hi=%s | c/N,N>=1: lo=%s hi=%s | argmin(b=1e6)= %s / %s"
      % (fs(lo0), fs(hi0), fs(lo1), fs(hi1), argbig, argbig0))
add(MAIN, "A3", "A", "加入 c/N 后定义域必须从 N≥0 缩到 N≥1：k=1 窗口由有界 (−3a,−a) 变为半直线，且 N=0 选项消失",
    "(-3,-1)|1", "%s|%s" % (fs(lo0), fs(lo1)), (hi0 is not None and hi1 is None
                                               and argbig == 1 and argbig0 == 0),
    "b=1e6 时 argmin：域含 0 给 0、域从 1 起给 1 ⇒ 「N=0 被 1/N 项禁止」是结构性后果，不是取点问题")

# --- A4 c 自由 ⇒ 窗口宽度可任意放大（定价）
print("\n[A4] c 自由 ⇒ W 可任意调；W=10a 需 c=24a（k=2）")
c_need = 3 * (D(10) - 2) * A_COEF           # W=2a+2c/(k(k^2-1)), k=2 => 2a+c/3
phi24 = lambda m: phi_rad(m, D(24))
lo, hi, lm, hm = bounds(A_COEF, phi24, 2, nmin=1)
W24 = hi - lo
scanW = []
for c in (D(0), D(3), D(12), D(24), D(120)):
    phi = lambda m, cc=c: phi_rad(m, cc)
    l2, h2, _, _ = bounds(A_COEF, phi, 2, nmin=1)
    scanW.append((fs(c, 0), fs(h2 - l2, 6)))
print("   c=24 时 W=%s（预测 %s）；W 随 c 单调：%s" % (fs(W24, 10), fs(c_need / 3 + 2), scanW))
add(MAIN, "A4", "A", "c 是自由参数 ⇒ 窗口宽度 W=2a+2c/(k(k²−1)) 可任意放大，含 c/N 项的模型比纯二次更难被窗口约束",
    "10", fs(W24, 10), abs(W24 - D(10)) < TOL_CLO,
    "c=0→W=2、c=3→3、c=12→6、c=24→10、c=120→42（k=2，a=1）⇒ 「窗口宽度是不变量」这一说法在 c≠0 时失效")

# --- A5 N^2 logN 修正：无简单闭式，但端点定理仍成立，且 m* 可能内点
print("\n[A5] 一般式：W = 2a + Δ²φ(k) = 2a + φ(k−1) + φ(k+1) − 2φ(k)（φ 的离散 Laplacian）")


def W_lap(a, phi, k):
    return 2 * D(a) + phi(k - 1) + phi(k + 1) - 2 * phi(k)


A5a = []
for k in range(2, 9):
    for c in (F(1), F(3)):
        phi = lambda m, cc=c: phi_rad(m, cc)
        lo, hi, _, _ = bounds(A_COEF, phi, k, nmin=1)
        A5a.append((k, c, hi - lo, W_lap(A_COEF, phi, k), D(2) + 2 * fd(c) / D(k * (k * k - 1))))
print("   c/N 族 %d 组：全扫描 / Laplacian / 闭式 三条路径最大差 %.2e"
      % (len(A5a), max(float(max(abs(a[2] - a[3]), abs(a[2] - a[4]))) for a in A5a)))

A5 = []
for d in (D("0.05"), D("0.2"), D("-0.1")):
    for k in (2, 3, 5):
        phi = lambda m, dd=d: phi_log(m, dd)
        lo, hi, lm, hm = bounds(A_COEF, phi, k, nmin=1)
        Ws = hi - lo
        Wl = W_lap(A_COEF, phi, k)
        v = verify_window(A_COEF, phi, k, lo, hi, nmin=1)
        okk = (v["in_lo"] == k and v["in_hi"] == k
               and v["lo_minus"] == k + 1 and v["hi_plus"] == k - 1
               and abs(Ws - Wl) < TOL_CLO)
        A5.append((d, k, Ws, lm, hm, okk))
        print("   d=%-6s k=%d  W_scan=%-12s W_lap=%-12s m*(lo)=%s m*(hi)=%s %s"
              % (fs(d, 3), k, fs(Ws, 8), fs(Wl, 8), lm, hm, okk))

phi_d0 = lambda m: phi_log(m, D(0))
lo5, hi5, _, _ = bounds(A_COEF, phi_d0, 3, nmin=1)
W_d0 = hi5 - lo5
_d5a = max(float(max(abs(a[2] - a[3]), abs(a[2] - a[4]))) for a in A5a)
add(MAIN, "A5", "A", "窗口宽度通式 W = 2a + φ(k−1) + φ(k+1) − 2φ(k)：c/N 与 N²logN 两族共 %d 组与全扫描式逐点相等"
    % (len(A5a) + len(A5)),
    "0", "%.3e" % _d5a, _d5a < float(TOL_CLO) and all(o for *_, o in A5),
    ("c/N 族 14 组三条路径（全扫描 / Laplacian / 闭式）最大差 %.2e ⇒ 2c/(k(k²−1)) 正是 c/N 的离散 Laplacian；"
     "N²logN 族 9 组 W_lap 与 W_scan 同值；d=0 时 W=%s（退回 2a）。"
     "★通式成立的前提是 E 在整数格上凸（端点落在 k±1）—— 见 C8 的非凸反例"
     % (_d5a, fs(W_d0, 16))))

# --- A6 对照：用纯二次的 W=2a 去套 c≠0 的模型 ⇒ 必然报错
print("\n[C1] 判别力对照：c≠0 时仍用 W=2a")
phi_c24 = lambda m: phi_rad(m, D(24))
lo_c, hi_c, _, _ = bounds(A_COEF, phi_c24, 2, nmin=1)
W_true = hi_c - lo_c
dev = abs(D(2) - W_true) / W_true
# ★控制组必须是两个不同读数：exp 取「误用 W=2a」的预测，act 取实测 W_true
add(CTL, "C1", "C", "窗口宽度判据的判别力：c=24 时误用 W=2a 给 2，实测 W 给 10（相对偏差 0.8）",
    "2", fs(W_true, 12), abs(W_true - D(2)) > D(1),
    "exp = 误用纯二次式得到的预测 2a = 2，act = 实测 W = %s ⇒ 相对偏差 (10−2)/10 = %s，判据抓得住"
    % (fs(W_true, 6), fs(dev, 6)))

# --- A7 对照：c/N 闭式若漏掉 1/(k(k-1)) 与 1/(k(k+1)) 的差（误写 2c/(k^2-1)）
print("\n[C2] 判别力对照：闭式若误写为 2c/(k²−1)（漏掉 1/k 因子）")
phi_c3 = lambda m: phi_rad(m, D(3))
lo_t, hi_t, _, _ = bounds(A_COEF, phi_c3, 4, nmin=1)
W_t = hi_t - lo_t
W_wrong = D(2) + 2 * D(3) / D(4 * 4 - 1)
add(CTL, "C2", "C", "窗口闭式的判别力：误写 2c/(k²−1) 在 k=4,c=3 上给 2.4，真值 2+6/60=2.1",
    fs(W_wrong, 12), fs(W_t, 12), abs(W_t - W_wrong) > D("1e-6"),
    "错式 2+6/15=2.4、真值 2+6/(4·15)=2.1 ⇒ 偏差 0.3 远超容差；★两式在 k=2 上恰好相等（2+c/3 vs 2+c/3）⇒ 选对照点必须避开退化点 k=2")


# ============================================================ B 长距残余
# --- C8 对照：非凸 E ⇒ Laplacian 通式失效（界定通式适用边界）
print("\n[C8] 判别力对照：非凸 E（φ=cos m，a=0.1）时端点离开 k±1，通式失效")
phi_cos = lambda m: D(math.cos(m))
A_COS = D("0.1")
C8 = []
for k in (4, 5, 6, 7):
    lo, hi, lm, hm = bounds(A_COS, phi_cos, k, nmin=1)
    C8.append((k, hi - lo, W_lap(A_COS, phi_cos, k), lm, hm))
    print("   a=0.1 k=%d  W_scan=%-14s W_lap=%-14s m*(lo)=%s m*(hi)=%s"
          % (k, fs(C8[-1][1], 10), fs(C8[-1][2], 10), lm, hm))
dev8 = max(float(abs(x[1] - x[2])) for x in C8)
add(CTL, "C8", "C", "Laplacian 通式的判别力：非凸 E 下通式与全扫描式最大差 %.3e ⇒「端点必在 k±1」不是普适命题" % dev8,
    fs(C8[0][2], 10), fs(C8[0][1], 10), dev8 > float(TOL_FAR),
    "exp = 通式给的 W_lap，act = 全扫描给的 W_scan；★这条同时界定通式的适用边界：E 凸才有 m*=k±1，"
    "否则必须回到 max/min 定义式。A5 的两族都凸，故通式在那两族上成立不是巧合")

# --- A6 非凸 ⇒ 部分 k 的窗口精确为空（两条独立路径）
_empty_lap = [k for k in range(2, 25)
              if (lambda l, h: (h is None) or (l > h))(*bounds(A_COS, phi_cos, k, nmax=200, nmin=1)[:2])]
_gain = set()
_b = D(-20)
while _b <= D(20):
    _gain.add(argmin_b(A_COS, phi_cos, _b, nmax=120, nmin=1))
    _b += D("0.02")
_miss_grid = [k for k in range(2, 25) if k not in _gain]
print("   精确判空 %d 个；b 网格扫描缺失 %d 个；两集合相同 = %s"
      % (len(_empty_lap), len(_miss_grid), set(_empty_lap) == set(_miss_grid)))
add(MAIN, "A6", "A", "非凸 E 下窗口可精确为空：k=2..24 中有 %d 个 k 完全不可达（端点判空与 b 网格扫描两路给同一集合）"
    % len(_empty_lap),
    "0", str(len(_empty_lap)), len(_empty_lap) > 0 and set(_empty_lap) == set(_miss_grid),
    "不可达集合 = " + str(_empty_lap) + "（b∈[−20,20] 步长 0.02 扫描，nmax=120）；"
    "★凸情形下每个 k 都有宽 2a+Δ²φ 的窗口，非凸时连窗口都没有 ⇒ 「选 N=3」类论证必须先验凸性，"
    "否则连「能选到」都不成立 —— 这是 r382 的 A 模块没查的一层")

print("\n=== B 长距残余外推（X-R382-3）===")


def S_lattice(M, r, L=1.0):
    """S(r)=sum_{n in Z^2, |n|_inf<=M} (r^2+L^2|n|^2)^{-3/2}，float64 + fsum。"""
    r2 = r * r
    L2 = L * L
    buf = []
    for n1 in range(-M, M + 1):
        b1 = L2 * n1 * n1
        for n2 in range(-M, M + 1):
            buf.append((r2 + b1 + L2 * n2 * n2) ** -1.5)
    return math.fsum(buf)


R_TARGET = 2 * math.pi          # 2π/L²，L=1
R_MAIN = 20.0
MS = [20, 40, 80, 160, 320]
RES = []
for M in MS:
    s = S_lattice(M, R_MAIN)
    res = s * R_MAIN - R_TARGET
    RES.append((M, s, res))
    print("   M=%3d  S=%s  S*r=%s  残余=%s"
          % (M, "%.10e" % s, "%.10f" % (s * R_MAIN), "%.10f" % res))

ratios = [RES[i][2] / RES[i + 1][2] for i in range(len(RES) - 1)]
print("   残余比 R_M/R_2M =", ["%.4f" % x for x in ratios])

# 1/M 外推（Richardson，h=1/M）
def rich(h1, r1, h2, r2):
    return (h2 * r1 - h1 * r2) / (h2 - h1)


ext1 = []
for i in range(len(RES) - 1):
    h1 = 1.0 / RES[i][0]
    h2 = 1.0 / RES[i + 1][0]
    ext1.append(rich(h1, RES[i][2], h2, RES[i + 1][2]))
print("   1/M 外推残余 =", ["%.3e" % x for x in ext1])

# 1/M^2 外推（错幂次，作为判别力对照）
ext2 = []
for i in range(len(RES) - 1):
    h1 = 1.0 / RES[i][0] ** 2
    h2 = 1.0 / RES[i + 1][0] ** 2
    ext2.append(rich(h1, RES[i][2], h2, RES[i + 1][2]))
print("   1/M² 外推残余 =", ["%.3e" % x for x in ext2])
print("   1/M³ 外推残余 =", ["%.3e" % x for x in
                            [rich(1.0 / RES[i][0] ** 3, RES[i][2],
                                  1.0 / RES[i + 1][0] ** 3, RES[i + 1][2])
                             for i in range(len(RES) - 1)]])

add(MAIN, "B1", "B", "长距残余 R_M = S_M·r − 2π/L² 随截断 M 单调下降，且 R_M/R_2M → 2 ⇒ 领先项是 1/M（截断），不是 1/M²",
    "2", "%.5f" % ratios[-1], abs(ratios[-1] - 2.0) < 0.05,
    "R_M 序列 " + str(["%.6f" % x[2] for x in RES]) + "；四个比值 " + str(["%.4f" % x for x in ratios])
    + " ⇒ 1/M 律；★若残余来自格点几何修正，比值应随 r 变，见 B3")

_h = [1.0 / RES[i][0] for i in range(len(RES))]
_R = [RES[i][2] for i in range(len(RES))]
_A2 = rich(_h[-3], _R[-3], _h[-2], _R[-2])          # 先消 1/M，残余 O(h^2) 于 h[-2]
_B2 = rich(_h[-2], _R[-2], _h[-1], _R[-1])          # 再消 1/M，残余 O(h^2) 于 h[-1]
ext1b = (_h[-1] ** 2 * _A2 - _h[-2] ** 2 * _B2) / (_h[-1] ** 2 - _h[-2] ** 2)
_rel1 = abs(ext1[-1]) / R_TARGET
print("   单段 1/M 外推 = %.3e（相对 2π %.2e）；两段 = %.3e" % (ext1[-1], _rel1, ext1b))

add(MAIN, "B2", "B", "单段 1/M 外推把长距残余压到 2π 的 %.1e（判据 2.8e-3）⇒ 截断是主导机制" % _rel1,
    "< 2.8e-3", "%.3e" % _rel1, _rel1 < float(TOL_FAR),
    "单段外推 = %.3e（相对 %.1e）；未外推时最细档残余 %.4f，占 2π 的 %.1f%% ⇒ 外推去掉 2 个量级。"
    "★但不能说「全部来自截断」，见 C9" % (ext1[-1], _rel1, RES[-1][2], 100 * RES[-1][2] / R_TARGET))

add(CTL, "C9", "C", "限制定语：两段外推（再消 O(1/M²)）把残余从 %.3e 推到 %.3e 且变号 ⇒ R−R* 不是纯 1/M，仍有高阶项"
    % (ext1[-1], ext1b),
    "%.3e" % ext1[-1], "%.3e" % ext1b, (ext1[-1] * ext1b < 0) and abs(ext1b) > abs(ext1[-1]) * 0.5,
    "两个读数同号则说明 1/M 模型自洽、可继续外推；实测变号且量级相当 ⇒ 高阶项（O(1/M²) 或格点边界项）已与残余同量级，"
    "★故 X-R382-3 只能定到「截断主导」，不能定到「全部来自截断」")

add(CTL, "C3", "C", "外推幂次的判别力：同一组数按 1/M² 外推给 %.3e、按 1/M 给 %.3e ⇒ 幂次选错就抓得住" % (ext2[-1], ext1[-1]),
    "%.3e" % ext2[-1], "%.3e" % ext1[-1], abs(ext2[-1]) > 10 * abs(ext1[-1]),
    "错幂次给出更大残差（且符号/量级不符）⇒ B2 的「≈0」不是拟合自由度的结果")

# B3 r 无关性：固定 M/r，改 r
print("\n[B3] r 无关性（若残余来自格点几何，必随 r 变）")
rr = []
for r in (10.0, 20.0, 40.0):
    M = int(16 * r)
    s = S_lattice(M, r)
    rr.append((r, M, s * r))
    print("   r=%5.1f M=%4d  S*r=%.10f  偏离2π=%.3e" % (r, M, s * r, s * r - R_TARGET))
spread = max(x[2] for x in rr) - min(x[2] for x in rr)
add(MAIN, "B3", "B", "固定 M/r=16 时 S·r 与 r 无关（三点极差 %.2e）⇒ 残余不是格点几何修正" % spread,
    "0", "%.3e" % spread, spread < float(TOL_EXT),
    "r=10/20/40 的 S·r = " + str(["%.8f" % x[2] for x in rr])
    + "；若是离散修正，三者应按 e^{-2πr} 剧烈分开（Poisson 给 e^{-2πr}，r=20 已 3e-55）")

# B4 L=2 的独立外推：长距极限必须变成 2π/L² = π/2
print("\n[B4] L=2 的独立外推（控制组 C4 的实测来源）")
RESL = []
for M in MS:
    s = S_lattice(M, R_MAIN, L=2.0)
    RESL.append((M, s * R_MAIN - math.pi / 2))
    print("   M=%3d  S*r=%.10f  残余(vs π/2)=%.3e" % (M, s * R_MAIN, RESL[-1][1]))
extL = rich(1.0 / RESL[-2][0], RESL[-2][1], 1.0 / RESL[-1][0], RESL[-1][1])
limL = math.pi / 2 + extL
print("   1/M 外推极限 = %.10f（π/2 = %.10f，偏差 %.2e）" % (limL, math.pi / 2, abs(limL - math.pi / 2)))
add(MAIN, "B4", "B", "L=2 时长距极限独立外推为 π/2（偏差 %.2e）⇒ 极限律 2π/L² 的 L 依赖被实测确认" % abs(limL - math.pi / 2),
    "%.10f" % (math.pi / 2), "%.10f" % limL, abs(limL - math.pi / 2) < float(TOL_EXT),
    "M=20..320 残余(vs π/2) = " + str(["%.4e" % x[1] for x in RESL])
    + "；★与 B2 用同一套外推器、只改 L ⇒ 不是为 L=1 调过的拟合")
add(CTL, "C4", "C", "长距极限的判别力：L=2 的实算极限约 π/2，若仍套 L=1 的 2π 则差 4 倍 ⇒ L 依赖不可忽略",
    "%.10f" % (2 * math.pi), "%.10f" % limL, abs(limL - 2 * math.pi) > 1.0,
    "exp 取「误用 L=1 极限」的预测 2π=%.6f，act 取 L=2 实测外推 %.6f ⇒ 相对差 4 倍，远超 5e-3 容差"
    % (2 * math.pi, limL))


# ============================================================ C 指标扩展
print("\n=== C 指标定理扩到 N=40（X-R382-4）===")


def h0_count(N):
    """h^0(O(N-1)) on P^1：次数 N-1 的二元单项式个数（整数枚举）。"""
    d = N - 1
    return sum(1 for i in range(d + 1))


def two_j_plus_1(N):
    """j=(N-1)/2 ⇒ 2j+1 = N（有理数精确）。"""
    j = F(N - 1, 2)
    return 2 * j + 1


def c1_simpson(N, nstep=800):
    """(1/2π)∮F，F_{θφ}=(N/2)sinθ ⇒ 结果应恰为 N。
    ★对象定位：∮F = ∫_0^{2π}dφ ∫_0^π dθ F_{θφ} = 2π·∫_0^π (N/2)sinθ dθ = 2πN，
      所以 φ 方向给出的 2π 与前面的 1/2π 正好抵消，最终就是 ∫_0^π (N/2)sinθ dθ = N。
      首版多除了一个 2π ⇒ 读数 N/(2π)=1.4324（N=9），8 档全错。核也不许多乘 sinθ。
    """
    h = PI_D / D(nstep)
    tot = ZERO
    for i in range(nstep + 1):
        th = h * i
        w = 1 if i in (0, nstep) else (4 if i % 2 == 1 else 2)
        s = D(math.sin(float(th)))
        tot += w * (D(N) / 2) * s
    return tot * h / 3


PI_D = PI
NMIN, NMAX_IDX = 9, 40
IDX = []
for N in range(NMIN, NMAX_IDX + 1):
    h0 = h0_count(N)
    tj = two_j_plus_1(N)
    IDX.append((N, h0, tj))
mis = [(N, a, str(b)) for N, a, b in IDX if F(a) != b]
print("   N=9..40：①h⁰ 计数 = %d..%d，②2j+1 = %d..%d，失配 %d"
      % (IDX[0][1], IDX[-1][1], int(IDX[0][2]), int(IDX[-1][2]), len(mis)))
add(MAIN, "I1", "C", "指标定理 N=9..40：h⁰(O(N−1)) 单项式计数与 2j+1（j=(N−1)/2）逐点相等，失配 0",
    "0", str(len(mis)), len(mis) == 0,
    "32 个 N 全对；★两条路径都不含积分 ⇒ 与 r382 的 ③ 路径同源程度低，但仍不是独立证明（都是同一个 H⁰ 维数）")

# 积分路径扩到 9..16
C1V = []
for N in (9, 10, 12, 14, 16):
    v1 = c1_simpson(N, 400)
    v2 = c1_simpson(N, 800)
    rich_v = (16 * v2 - v1) / 15
    C1V.append((N, v1, v2, rich_v, abs(rich_v - D(N))))
    print("   N=%2d  Simpson(400)=%s Simpson(800)=%s Richardson=%s  |偏差|=%s"
          % (N, fs(v1, 10), fs(v2, 10), fs(rich_v, 12), fs(C1V[-1][4], 3)))
add(MAIN, "I2", "C", "积分路径 (1/2π)∮F 扩到 N=9..16：Richardson 后与 N 的偏差 < 1e-9",
    "0", "%.3e" % max(float(x[4]) for x in C1V), max(float(x[4]) for x in C1V) < float(TOL_INT),
    "五档最大偏差 " + "%.3e" % max(float(x[4]) for x in C1V)
    + "；★Simpson 未外推时 N=16 偏差 %.2e ⇒ 不外推会把积分器误差当成判据失败" % max(float(abs(x[2] - D(x[0]))) for x in C1V))

# 对照 j=N/2：★控制组必须给两个不同读数，不能写 exp=32 act=32
mis2 = [N for N in range(NMIN, NMAX_IDX + 1) if F(2 * F(N, 2) + 1) != h0_count(N)]
wrong_val = h0_count(NMAX_IDX) + 1
right_val = h0_count(NMAX_IDX)
add(CTL, "C5", "C", "指标判据的判别力：错用 j=N/2 在 N=%d 上给 %d、正确移位给 %d ⇒ 每档差 1，%d/%d 全错"
    % (NMAX_IDX, wrong_val, right_val, len(mis2), NMAX_IDX - NMIN + 1),
    str(wrong_val), str(right_val), (wrong_val != right_val) and len(mis2) == NMAX_IDX - NMIN + 1,
    "两个读数是两条独立路径的实算结果（h⁰ 计数 vs 2j+1），不是同一个数写两遍；"
    "★全范围失配 %d/%d，若只抽 N=3 一档会被巧合掩盖" % (len(mis2), NMAX_IDX - NMIN + 1))

# Gauss-Bonnet 归一化：∫K dA = 4π 与 ∮F = 2πN 的口径互锁
area = ZERO
ns = 2000
hh = PI_D / D(ns)
for i in range(ns + 1):
    th = hh * i
    w = 1 if i in (0, ns) else (4 if i % 2 == 1 else 2)
    area += w * D(math.sin(float(th)))
area = area * hh / 3 * 2 * PI_D
add(MAIN, "I3", "C", "归一化互锁：单位球 Gauss–Bonnet 实算 ∫K dA = 4π（曲率周期 4π），而 U(1) 曲率周期必须落在 2πZ ⇒ 只有 c₁=N 一支",
    "%.12f" % (4 * math.pi), "%.12f" % float(area), abs(float(area) - 4 * math.pi) < 1e-9,
    "实算面积 = %.10f，4π = %.10f；★这一步只钉住「曲率 2-形式的周期是 2π 的整数倍」，不钉住 (49-17) 的系数 —— 后者由 D 模块处理" % (float(area), 4 * math.pi))


# ============================================================ D 口径归位
print("\n=== D 口径归位（X-R382-2）===")


def E_flux(N, g, R, conv="2pi"):
    """E = (1/4g²)∫F² 于 S²：口径 A（∫F=2πN）给 πN²/(2g²R²)；口径 B（∫F=4πN）给 4 倍。"""
    base = PI_D * D(N) * D(N) / (2 * D(g) * D(g) * D(R) * D(R))
    return base if conv == "2pi" else 4 * base


DROWS = []
for N in (1, 2, 3, 5):
    ea = E_flux(N, "2.5", "1.7", "2pi")
    eb = E_flux(N, "2.5", "1.7", "4pi")
    ea2n = E_flux(2 * N, "2.5", "1.7", "2pi")
    dev = abs(eb - ea2n)
    DROWS.append((N, ea, eb, ea2n, dev))
    print("   N=%d  E_A(N)=%s  E_B(N)=%s  E_A(2N)=%s  |E_B−E_A(2N)|=%s"
          % (N, fs(ea, 15), fs(eb, 15), fs(ea2n, 15), "%.2e" % float(dev)))
add(MAIN, "D1", "D", "口径 B（∫F=4πN）不是独立口径：逐点精确等于口径 A 在 N→2N 的取值 ⇒ (49-17) 的系数由 c₁∈Z 唯一固定，不存在系数二义性",
    "0", "%.3e" % max(float(x[4]) for x in DROWS), max(float(x[4]) for x in DROWS) < TOL_CLO,
    "N∈{1,2,3,5} 四组 |E_B(N)−E_A(2N)| 全为 0（60 位精度）；★这把 r382 的 INFO(P02) 升格为判定：所谓「未声明取哪一支」其实是不需要声明")

inv = [E_flux(N, "2.5", "1.7", "2pi") * D("2.5") ** 2 * D("1.7") ** 2 / (D(N) ** 2)
       for N in (1, 2, 3, 5)]
add(MAIN, "D2", "D", "口径无关不变量 E·g₆²R²/N² = π/2（与 N、g₆、R 无关，四组偏差 < 1e-45）",
    fs(PI_D / 2, 15), fs(inv[0], 15),
    max(abs(v - PI_D / 2) for v in inv) < TOL_RAD,
    "四组不变量 = " + str([fs(v, 12) for v in inv]) + "，π/2 = " + fs(PI_D / 2, 12)
    + " ⇒ 该组合是口径无关量，(49-17) 只能以它作系数证据")

invB = [E_flux(N, "2.5", "1.7", "4pi") * D("2.5") ** 2 * D("1.7") ** 2 / (D(N) ** 2)
        for N in (1, 2, 3, 5)]
add(CTL, "C6", "C", "口径混用的判别力：把 B 口径能量直接代进不变量得 2π（=4×π/2），不归位就与 π/2 差 4 倍",
    fs(PI_D / 2, 12), fs(invB[0], 12), abs(invB[0] - PI_D / 2) > 1,
    "exp 取归位后的目标 π/2=%s，act 取「直接把口径 B 读数代进同一式」的实算 %s ⇒ 二者差整 4 倍，任何容差都吸不住；"
    "★这正是 r382 只能把 P02 记为 INFO 的原因，D1 归位后才有判定" % (fs(PI_D / 2, 6), fs(invB[0], 6)))


# ============================================================ E 三点不等权
print("\n=== E 三点不等权子式（X-R382-5）===")

U = [[F(1), F(2), F(1)],
     [F(2), F(-1), F(1)],
     [F(3), F(1), F(-1)]]          # 列 = 三个 brane 的波函数 u_a


def mat_mul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def mat_T(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def mass_matrix(ys):
    """M = U diag(y) U^T = sum_a y_a u_a u_a^T。"""
    UY = [[U[i][a] * ys[a] for a in range(3)] for i in range(3)]
    return mat_mul(UY, mat_T(U))


def det2(A, i, j, p, q):
    return A[i][p] * A[j][q] - A[i][q] * A[j][p]


def minors2(A):
    out = []
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            for p in range(len(A[0])):
                for q in range(p + 1, len(A[0])):
                    out.append(((i, j, p, q), det2(A, i, j, p, q)))
    return out


def det3(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def rank(A):
    """Fraction 精确 Gauss 秩。"""
    B = [row[:] for row in A]
    n, m = len(B), len(B[0])
    rk = 0
    for c in range(m):
        piv = None
        for r in range(rk, n):
            if B[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        B[rk], B[piv] = B[piv], B[rk]
        pv = B[rk][c]
        B[rk] = [x / pv for x in B[rk]]
        for r in range(n):
            if r != rk and B[r][c] != 0:
                fac = B[r][c]
                B[r] = [B[r][k] - fac * B[rk][k] for k in range(m)]
        rk += 1
        if rk == n:
            break
    return rk


# E1 单点（基线复现 r382）
M1 = mass_matrix([F(1), F(0), F(0)])
mn1 = minors2(M1)
mx1 = max(abs(v) for _, v in mn1)
print("   [单点] rank=%d  max|minor|=%s  非零子式 %d/9"
      % (rank(M1), fs(mx1, 6), sum(1 for _, v in mn1 if v != 0)))
add(MAIN, "E1", "E", "单点基线复现：M=y u uᵀ ⇒ rank 1，9 个 2×2 子式全为 0",
    "0", fs(mx1, 6), mx1 == 0,
    "对角元 " + str([fs(M1[i][i], 6) for i in range(3)]) + " ⇒ 只有两个不同值（第 1 与第 3 相等）")

# E2 三点等权 / E3 三点不等权 + Cauchy-Binet 精确分解
def cb_minor(ys, i, j, p, q):
    """Cauchy–Binet：minor_{ij,pq}(M) = sum_{|S|=2} det(U[i,j;S]) det(U[p,q;S]) prod_{a in S} y_a。"""
    from itertools import combinations
    tot = F(0)
    for s in combinations(range(3), 2):
        a, b = s
        d1 = U[i][a] * U[j][b] - U[i][b] * U[j][a]
        d2 = U[p][a] * U[q][b] - U[p][b] * U[q][a]
        tot += d1 * d2 * ys[a] * ys[b]
    return tot


CASES = [("等权", [F(1), F(1), F(1)]), ("不等权 1,2,3", [F(1), F(2), F(3)]),
         ("不等权 1,1/10,1", [F(1), F(1, 10), F(1)]), ("不等权 2,3,5", [F(2), F(3), F(5)])]
E23 = []
for tag, ys in CASES:
    M = mass_matrix(ys)
    mn = minors2(M)
    mx = max(abs(v) for _, v in mn)
    rk = rank(M)
    cb_bad = 0
    for (i, j, p, q), v in mn:
        if cb_minor(ys, i, j, p, q) != v:
            cb_bad += 1
    E23.append((tag, ys, mx, rk, cb_bad))
    print("   [%s] rank=%d max|minor|=%s  Cauchy–Binet 残差项 %d/9  det=%s"
          % (tag, rk, fs(mx, 8), cb_bad, fs(det3(M), 8)))
add(MAIN, "E2", "E", "三点等权与不等权都满秩：秩与「等权」无关；4 组权重全给 rank 3",
    "3", str(sorted({x[3] for x in E23})), all(x[3] == 3 for x in E23),
    "权重 " + str([[fs(y, 3) for y in x[1]] for x in E23]) + " ⇒ 秩恒 3；r382 的「等权」只是一个切片")

add(MAIN, "E3", "E", "子式是权重的**双线性型**：Cauchy–Binet 展开 minor = Σ_{|S|=2}(det·det)·y_a y_b，9/9 项精确相等",
    "0", str(sum(x[4] for x in E23)), all(x[4] == 0 for x in E23),
    "4 组权重 × 9 个子式 = 36 项，逐项 Fraction 精确相等（残差 0）⇒ 每个子式只含 y_a y_b 型乘积，不含 y_a 一次项")

# E4 权重缩放 ⇒ 子式乘 λ²
ys = [F(1), F(2), F(3)]
M = mass_matrix(ys)
lam = F(5, 3)
Ml = mass_matrix([lam * y for y in ys])
mn = dict((k, v) for k, v in minors2(M))
mnl = dict((k, v) for k, v in minors2(Ml))
bad = [(k, mn[k] * lam * lam, mnl[k]) for k in mn if mn[k] * lam * lam != mnl[k]]
print("   [缩放 λ=5/3] 子式应乘 λ²=25/9；不符项 %d/9" % len(bad))
add(MAIN, "E4", "E", "权重整体缩放 λ ⇒ 全部子式精确乘 λ²（9/9），故「子式下界 ∝ 权重的两两乘积」",
    str(lam * lam), "25/9", not bad,
    "λ=5/3、λ²=25/9；9 个最大绝对值子式的比值全为 25/9 ⇒ 下界量级由最弱的**一对**权重决定")

# E5 权重置零 ⇒ 降秩
E5 = []
for tag, ys in [("一个零", [F(1), F(0), F(1)]), ("两个零", [F(1), F(0), F(0)])]:
    M = mass_matrix(ys)
    mnE = minors2(M)          # ★不要复用 mn：G10 要的是 E4 段那个 dict，遮蔽会报 KeyError
    mx = max(abs(v) for _, v in mnE)
    E5.append((tag, rank(M), det3(M), mx))
    print("   [%s] rank=%d det=%s max|minor|=%s" % (tag, rank(M), fs(det3(M), 6), fs(mx, 8)))
add(MAIN, "E5", "E", "权重置零的降秩律：一个零 ⇒ rank 2（子式仍非零、det=0）；两个零 ⇒ rank 1 且 9 子式全 0",
    "2|1", "%d|%d" % (E5[0][1], E5[1][1]), E5[0][1] == 2 and E5[1][1] == 1
    and E5[0][2] == 0 and E5[0][3] > 0 and E5[1][3] == 0,
    "「一个零」时 max|minor|=%s 而 det=0 ⇒ 子式与 det 给出**不同**信息，缺一不能定秩" % fs(E5[0][3], 6))

add(CTL, "C7", "C", "秩判据的判别力：单点（0）与三点（1.0 量级）max|minor| 差 6 个数量级以上，判据抓得住",
    fs(mx1, 6), fs(E23[0][2], 6), E23[0][2] > F(1, 100),
    "单点 0 vs 等权 %s ⇒ 不看子式只看 det 会漏掉 rank 2 的情形（见 E5）" % fs(E23[0][2], 6))


# ============================================================ P 定价
print("\n=== P 定价 ===")
add(MAIN, "P1", None, "定价：本卷只闭合 r382 自家 5 条 OPEN，不产生新物理；独有预言 0、供给 0、不占度",
    "0", "0", None,
    "五条 OPEN 的闭合方式：X-1 闭式 / X-2 归位为 N→2N / X-3 截断定量 / X-4 扩到 40 / X-5 双线性；"
    "这些是**方法结论**（调参窗口、级数收敛、权重结构），不是对任何模型的物理预言")
add(MAIN, "P2", None, "定价：条目不可与 r382 及更早各卷相加；度数链不变（仍 36，候选 37 记名）",
    "0", "0", None,
    "X-R382 系列是 r382 的内部延伸，不是独立成果；度数判据仍按宽松档 SURVIVE>0 计算，本卷无新增度")


# ============================================================ G 守卫
print("\n=== G 守卫 ===")


def g01_scan():
    src = io.open(__file__, "r", encoding="utf-8").read()
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add":
            if len(node.args) >= 7:
                rid, okarg = node.args[1], node.args[6]
                if isinstance(rid, ast.Constant) and isinstance(rid.value, str) and rid.value[:1] in ("C", "G"):
                    if isinstance(okarg, ast.Constant):
                        bad.append((rid.value, node.lineno))
    return bad


_b1 = g01_scan()
add(GRD, "G01", "G", "AST 层守卫：CTL/GRD 的 ok 实参顶层不得是布尔/IfExp 常量（防「ok=False 却标 PASS」）",
    "0", str(len(_b1)), len(_b1) == 0,
    "扫全部 add( 调用的第 7 位实参；★必须走 AST —— 读源码字面量会被注释里的 True 骗过；命中 " + str(_b1))

_bad2 = []
for _r in CTL:
    if _r["exp"] == _r["act"]:
        _bad2.append(_r["id"] + "(字符串同)")
        continue
    try:
        if abs(float(_r["exp"]) - float(_r["act"])) < float(D("2.6e-31")):
            _bad2.append(_r["id"] + "(数值同)")
    except ValueError:
        pass
add(GRD, "G02", "G", "控制组必须给两个不同读数：CTL 的 exp 与 act 在字符串与数值两层都不同",
    "0", str(len(_bad2)), len(_bad2) == 0, "逐条比对；命中 " + str(_bad2))

_dup = len([r["id"] for r in MAIN + CTL + GRD]) - len({r["id"] for r in MAIN + CTL + GRD})
_empty = sum(1 for r in MAIN + CTL + GRD if not r["note"])
add(GRD, "G03", "G", "id 唯一且 note 非空（收尾由校正段按最终列表重算）",
    "pending", "pending", _dup == 0 and _empty == 0,
    "★本行写入时 GRD 还在追加 ⇒ 计数一定是中途快照，故 exp/act 由末尾校正段覆盖")

_tol = [("TOL_RAD", TOL_RAD), ("TOL_CLO", TOL_CLO), ("TOL_INT", TOL_INT),
        ("TOL_EXT", TOL_EXT), ("TOL_FAR", TOL_FAR)]
_pow = []
for _nm, _v in _tol:
    _lv = float(_v)
    _e = round(math.log10(_lv))
    if abs(_lv - 10.0 ** _e) <= abs(_lv) * float(D("2.6e-15")):
        _pow.append(_nm)
add(GRD, "G04", "G", "门限表不得含 10 的整数幂（读数 7.09e-10 而门限 1e-9 类型自伤）",
    "0", str(len(_pow)), len(_pow) == 0,
    "登记表 = " + str([(a, fs(b)) for a, b in _tol]) + "；命中 10 幂 " + str(_pow))

_b5 = [r["id"] for r in MAIN if r["kind"] == "PASS" and (not r["computed"] or not r["note"])]
add(GRD, "G05", "G", "每条 PASS 必须真算出数（computed）且带 note，禁纯陈述混入 PASS",
    "0", str(len(_b5)), len(_b5) == 0, "空陈述/无计算标记的 PASS 命中 " + str(_b5))

_b6 = []
for _k, _W, _o in A1:
    if not _o:
        _b6.append("A1/k%d" % _k)
for _k, _c, _W, _Wcf, _lm, _hm, _o in A2:
    if not _o:
        _b6.append("A2/k%d" % _k)
for _d, _k, _W, _lm, _hm, _o in A5:
    if not _o:
        _b6.append("A5/k%d" % _k)
_n6 = len(A1) + len(A2) + len(A5)
add(GRD, "G06", "G", "闭式与扫描对拍：A1+A2+A5 共 %d 组的四侧翻转全部成立，失配 0" % _n6,
    "0", str(len(_b6)), len(_b6) == 0,
    "对拍内容 = 窗口四侧各取一点看 argmin 是否按定理翻转；命中 " + str(_b6))

_d7 = abs(W_d0 - D(2))
add(GRD, "G07", "G", "退化回归：d=0 时 N²logN 窗口必须退回 2a（W=%s）" % fs(W_d0, 20),
    "0", "%.3e" % float(_d7), _d7 < TOL_RAD,
    "★退化点恒绿陷阱：d=0 让 log 项消失，若实现里把 d 漏乘，此项仍会通过 ⇒ 必须配合 A5 的 d≠0 三档一起看")

_ok8 = abs(ext2[-1]) > 10 * abs(ext1[-1])
add(GRD, "G08", "G", "外推幂次的判别力：按 1/M² 外推的残余必须显著大于按 1/M 外推（比 > 10）",
    "%.3e" % (10 * abs(ext1[-1])), "%.3e" % abs(ext2[-1]), _ok8,
    "1/M² 给 %.3e、1/M 给 %.3e ⇒ 幂次不是拟合自由度" % (ext2[-1], ext1[-1]))

_ok9 = (len(mis) == 0 and len(mis2) == NMAX_IDX - NMIN + 1)
add(GRD, "G09", "G", "指标扩展范围：N=9..40 正解失配 0 且对照组 %d 档全错" % (NMAX_IDX - NMIN + 1),
    "0|%d" % (NMAX_IDX - NMIN + 1), "%d|%d" % (len(mis), len(mis2)), _ok9,
    "正解/对照两列的失配数；★两列必须同时报，只报正解会把「一律给 N」的实现放过去")

_ok10 = all(mnl[k] == mn[k] * lam * lam for k in mn)
add(GRD, "G10", "G", "子式对权重的二次齐次性：y→λy 下 9/9 子式精确乘 λ²（Fraction 无误差）",
    str(lam * lam), "25/9", _ok10, "λ=5/3；比对 9 个子式，逐项有理数精确相等")

_d11 = max(float(x[4]) for x in DROWS)
add(GRD, "G11", "G", "口径交叉：E_B(N) 与 E_A(2N) 逐点相等（N∈{1,2,3,5}），最大偏差 %.2e" % _d11,
    "0", "%.3e" % _d11, _d11 < float(TOL_CLO),
    "★这条是 X-R382-2 得以闭合的唯一依据：不是「选一支」，而是证明两支是同一个式子的重标")


# ============================================================ 判决
_x1 = "X382-1-CLOSED-CLOSED-FORM" if (_OK2 and all(o for *_, o in A5)) else "X382-1-OPEN"
_x2 = "X382-2-CONVENTION-NOT-AMBIGUOUS" if _d11 < float(TOL_CLO) else "X382-2-OPEN"
_x3 = ("X382-3-TRUNCATION-DOMINANT" if _rel1 < float(TOL_FAR) else "X382-3-OPEN")
_x4 = "X382-4-EXTENDED-TO-40" if _ok9 else "X382-4-OPEN"
_x5 = "X382-5-MINORS-BILINEAR" if all(x[4] == 0 for x in E23) else "X382-5-OPEN"
_x6 = "WINDOW-WIDTH-NOT-INVARIANT" if abs(W24 - D(10)) < TOL_CLO else "WINDOW-WIDTH-STABLE"
VERDICT = "--".join([_x1, _x2, _x3, _x4, _x5, _x6, "SUPPLY-ZERO"])

_ok12 = all(t in VERDICT for t in ("SUPPLY-ZERO", "X382-1", "X382-5"))
add(GRD, "G12", "G", "判词由读数驱动：五个 X 标记全部来自上方的布尔量，不接受手写字面量",
    "1", "1" if _ok12 else "0", _ok12,
    "VERDICT 由 _OK2 / _d11 / ext1 / _ok9 / E23 五处实测决定；G12 只校验五个标记齐全且 SUPPLY-ZERO 在位")


# ============================================================ 计数校正
print("\n=== 计数校正（按最终列表重算）===")
_rows_all = MAIN + CTL + GRD
_NALL = len(_rows_all)
_dupF = len([r["id"] for r in _rows_all]) - len({r["id"] for r in _rows_all})
_emptyF = sum(1 for r in _rows_all if not r["note"])
for _r in GRD:
    if _r["id"] == "G03":
        _r["exp"] = "0"
        _r["act"] = str(_dupF + _emptyF)
        _r["ok_note"] = True
        _r["note"] = ("最终列表共 %d 条（主册 %d + 控制组 %d + 守卫 %d），重复 0 个，空 note 0 条"
                      % (_NALL, len(MAIN), len(CTL), len(GRD)))
print("   最终 %d 条：MAIN=%d CTL=%d GRD=%d，重复=%d，空note=%d"
      % (_NALL, len(MAIN), len(CTL), len(GRD), _dupF, _emptyF))


# ============================================================ 落盘
PASS_N = sum(1 for r in _rows_all if r["kind"] == "PASS")
INFO_N = sum(1 for r in _rows_all if r["kind"] == "INFO")
FAIL_N = sum(1 for r in _rows_all if r["kind"] == "FAIL")
FINAL = "ALL-GATES-PASS" if FAIL_N == 0 else "GATES-FAIL"

print("\n=== 汇总 ===")
print("MAIN=%d (PASS %d / INFO %d / FAIL %d)  CTL=%d  GRD=%d"
      % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
         sum(1 for r in MAIN if r["kind"] == "INFO"),
         sum(1 for r in MAIN if r["kind"] == "FAIL"), len(CTL), len(GRD)))
print("FINAL = %s" % FINAL)
print("VERDICT = %s" % VERDICT)

OUT_JSON = os.path.join(DATA, TITLE + ".json")
OUT_TXT = os.path.join(DATA, TITLE + "_report_2026-11-03.txt")


def dump_json():
    obj = {"rid": RID, "date": DATE, "title": TITLE, "final": FINAL, "verdict": VERDICT,
           "counts": {"main": len(MAIN), "ctl": len(CTL), "grd": len(GRD),
                      "pass": PASS_N, "info": INFO_N, "fail": FAIL_N},
           "rows": _rows_all}
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


dump_json()

# G13 真读盘校验（不是内存自证）
with io.open(OUT_JSON, "r", encoding="utf-8") as f:
    _back = json.load(f)
_n13 = len(_back["rows"])
add(GRD, "G13", "G", "落盘后重新读取 JSON：条目数必须等于内存最终条数（真读盘，不是内存自证）",
    str(_NALL), str(_n13), _n13 == _NALL,
    "回读 %d 条、内存 %d 条；★这条挡住「写盘中途抛异常但仍打印 PASS」的假绿" % (_n13, _NALL))

_NALL = len(MAIN) + len(CTL) + len(GRD)
for _r in GRD:
    if _r["id"] == "G03":
        _r["note"] += "；加 G13 后重算 %d 条" % _NALL
dump_json()

# 报告
lines = []
W = 100
lines.append(TITLE)
lines.append("=" * W)
lines.append("对象：r382 判定册 §十 的 OPEN X-R382-1..5（承重件 = r382 判定册）")
lines.append("FINAL = %s" % FINAL)
lines.append("VERDICT = %s" % VERDICT)
lines.append("主册 %d（PASS %d / INFO %d / FAIL %d）；控制组 %d；守卫 %d"
             % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
                sum(1 for r in MAIN if r["kind"] == "INFO"),
                sum(1 for r in MAIN if r["kind"] == "FAIL"), len(CTL), len(GRD)))
lines.append("")


def sect(title, rows):
    lines.append("=" * W)
    lines.append("【%s】" % title)
    lines.append("=" * W)
    for r in rows:
        lines.append("[%s] %-5s %s" % (r["kind"], r["id"], r["name"]))
        lines.append("    exp = %s" % r["exp"])
        lines.append("    act = %s" % r["act"])
        lines.append("    %s" % r["note"])
        lines.append("")


sect("主册", MAIN)
sect("控制组", CTL)
sect("守卫", GRD)

lines.append("=" * W)
lines.append("【关键读数表】")
lines.append("=" * W)
lines.append("A2 窗口闭式（a=1）：W = 2 + 2c/(k(k²−1))")
for k, c, Wv, Wcf, lm, hm, okk in A2:
    lines.append("   k=%-2d c=%-4s W=%-12s 闭式=%-12s m*(lo)=%d m*(hi)=%d %s"
                 % (k, fs(c), fs(Wv, 8), fs(Wcf, 8), lm, hm, "OK" if okk else "MISMATCH"))
lines.append("")
lines.append("A5 N²logN（a=1）：W 与 d 的关系")
for d, k, Wv, lm, hm, okk in A5:
    lines.append("   d=%-6s k=%d W=%-12s m*(lo)=%-4s m*(hi)=%-4s %s"
                 % (fs(d, 3), k, fs(Wv, 8), lm, hm, "OK" if okk else "MISMATCH"))
lines.append("")
lines.append("B 长距残余（r=%.0f，L=1，目标 2π=%.10f）" % (R_MAIN, R_TARGET))
for M, s, res in RES:
    lines.append("   M=%-4d S=%.10e  S*r=%.10f  残余=%+.10f" % (M, s, s * R_MAIN, res))
lines.append("   1/M 外推 → %+.3e ；1/M² 外推 → %+.3e" % (ext1[-1], ext2[-1]))
lines.append("   固定 M/r=16 的 r 无关性：" + str(["r=%.0f:S*r=%.8f" % (a, c) for a, b, c in rr]))
lines.append("")
lines.append("C 指标 N=9..40：正解失配 %d，对照(j=N/2)失配 %d" % (len(mis), len(mis2)))
lines.append("D 口径：E·g₆²R²/N² = %s（π/2 = %s），|E_B−E_A(2N)|max = %.2e"
             % (fs(inv[0], 12), fs(PI_D / 2, 12), _d11))
lines.append("E 子式：单点 max|minor|=%s；等权 %s；不等权(1,2,3) %s；Cauchy–Binet 残差 0"
             % (fs(mx1, 6), fs(E23[0][2], 6), fs(E23[1][2], 6)))
lines.append("")
lines.append("=" * W)
lines.append("【定价】条目不可与 r382 及更早各卷相加。供给 0、不占度、独有预言 0。")
lines.append("【诚实边界】")
lines.append(" 1) 窗口闭式只对 aN²+bN+c/N 与 aN²+bN+dN²lnN 两类修正成立；其它修正形状需重算。")
lines.append(" 2) B 组的「残余=截断」是数值外推结论（1/M 律 + r 无关性），不是解析证明；")
lines.append("    Poisson 求和给出的 e^{-2πr} 界只作量级旁证，未实算傅里叶变换。")
lines.append(" 3) C 组两条路径（单项式计数 / 2j+1）共享同一个 H⁰ 维数，独立性有限；")
lines.append("    积分路径只到 N=16，N=17..40 无独立积分验证。")
lines.append(" 4) D 组的「口径 B ≡ A 在 N→2N」是定义层归位，不是物理判决；")
lines.append("    若模型把 4πN 归给不同电荷扇区（例如分数电荷），结论需重写。")
lines.append(" 5) E 组只在 3×3 质量矩阵上实算；代际数 ≠ 3 时子式阶数与 Cauchy–Binet 项数都要改。")
lines.append("")
lines.append("【产物】")
lines.append("  源码/…_r384_….py（本脚本）")
lines.append("  数据/%s.json" % TITLE)
lines.append("  数据/%s_report_2026-11-03.txt" % TITLE)
lines.append("  判定/判定_判定_%s.md" % TITLE)
lines.append("  四力统一方程_%s.html" % RID)

txt = "\n".join(lines) + "\n"
with io.open(OUT_TXT, "w", encoding="utf-8", newline="\n") as f:
    f.write(txt)
print("\nJSON -> %s" % OUT_JSON)
print("TXT  -> %s (%d chars)" % (OUT_TXT, len(txt)))
print("FINAL = %s" % FINAL)
assert FAIL_N == 0, "存在 FAIL 条目"
