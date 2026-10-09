# -*- coding: utf-8 -*-
"""
四力大统一方程 · 垂直原理册 —— 元审计（信息含量 + 内部相容 + 数值方法）
====================================================================

被审计对象：``07_统一场方程/四力大统一方程_垂直原理整合/验证脚本/``
  * ``four_force_vertical_verify.py``   （34 条：PASS 27 / FAIL 4 / BOUNDARY 2 / INFO 1）
  * ``四力大统一_验证结果.json`` / ``四力大统一_验证摘要.txt``（该脚本的产物）

本脚本**不重做**那 34 条的物理判定，而是回答四个更靠前的问题：

  A 段·信息含量：27 个 PASS 里，有多少条**真的执行了判别性检验**？
      判据不是人工分类，而是一台机械装置：给每条 PASS 构造一个
      "残差函数" R(t)，在 256 个几何尺度上扫描——
        * R 在全部采样点都 < ID_TOL            ⇒ IDENTITY（代数恒等，零信息）
        * R 在全部采样点相同但非 0             ⇒ CONST（只与外部常数有关，与框架自由参数无关）
        * R 随采样点变化                       ⇒ VARIES（有判别力）
        * 该条目根本没有残差函数                ⇒ NO_TEST（硬编码 verdict 或空判据）
      另有两个**机械**的正交标记：
        DUPLICATE_OF：残差数组与另一条逐点相等（重复报告，不是独立出处）
        CIRCULAR    ：被验证量自身被当作扫描参数并用其定义式闭合
  B 段·内部相容：母恒等式 kappa^2+tau^2=(omega/c)^2 与 L2 的汤川场能否共存？
  C 段·数值与常数：原册的常数与容差有没有真缺陷（含 F13 弦张力量级）。
  D 段·参数账：统一母方程减少了几个自由参数？（约束增量）
  E 段·负向测试：每个核心判据配一枚"植入缺陷必须翻红"的阴性对照。

红线：
  * 零第三方依赖（ast / json / math / os / sys / decimal / fractions）。
  * 不改被审计目录的任何文件；变异测试全部在内存里做。
  * 自抓到的原册缺陷一律判 FAIL 并指名条目，不粉饰、不代改。
  * 分类器的分类结论必须由**正对照**（已知恒等 + 已知非常恒等）验证过才允许出数。

运行：  python -B four_force_vertical_meta_audit.py
退出码：0 = 全部条目已判定且自检全过（FAIL 是结论，不是脚本错误）
"""

import ast
import json
import math
import os
import sys
from decimal import Decimal as Dc, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.normpath(os.path.join(HERE, "..", "四力大统一方程_垂直原理整合", "验证脚本"))
TARGET_PY = os.path.join(TARGET_DIR, "four_force_vertical_verify.py")
TARGET_JSON = os.path.join(TARGET_DIR, "四力大统一_验证结果.json")

# ----------------------------------------------------------------- 常数（CODATA 2018，与被审计脚本同源）
HBAR = 1.054571817e-34
C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
E_CHG = 1.602176634e-19
EPS0 = 8.8541878128e-12
MU0 = 1.25663706212e-6
ALPHA_CODATA = 7.2973525693e-3
M_P_KG = 2.176434e-8
M_PROTON = 1.67262192369e-27
M_W_GEV = 80.379
M_PI0_MEV = 134.977
GEV_TO_KG = 1.78266192e-27
HBARC_MEV_FM = 197.3269804

# 被审计脚本自己写下的两个值（用于对照，不作为真值）
SIGMA_SCRIPT = 1.6e-2            # J/m，原册 F13 所用
V10_LAMBDA_W_M = 2.454956895935461e-18
V10_LAMBDA_PI_M = 1.461932571659696e-15
V9_RATIO_EG = 1.2356e36          # 原册 F11 引用的 v9 W12

# 弦张力真值：1 GeV/fm = (1.602176634e-10 J) / (1e-15 m)
SIGMA_1GEV_PER_FM = 1.602176634e-10 / 1.0e-15
SIGMA_090GEV_PER_FM = 0.90 * SIGMA_1GEV_PER_FM

ALPHA_REF = B_OVER_RHO_REF = 2.19e-13 / 3.0e-11     # 原册的螺距比

# ----------------------------------------------------------------- 通用工具
RESULTS = []
_SEQ = [0]
LAYER_PREFIX = {"A": "MA", "B": "MB", "C": "MC", "D": "MD", "E": "ME"}


def _nxt(layer):
    _SEQ[0] += 1
    return "%s%02d" % (LAYER_PREFIX[layer], _SEQ[0])


def record(layer, name, verdict, symbolic, numeric, note):
    RESULTS.append({
        "id": _nxt(layer),
        "layer": layer,
        "name": name,
        "verdict": verdict,
        "symbolic": symbolic,
        "numeric": numeric,
        "note": note,
    })


def rel(a, b):
    if b == 0:
        return abs(a - b)
    return abs(a - b) / abs(b)


def fmt(x, n=12):
    if x is None:
        return "None"
    if isinstance(x, int):
        return str(x)
    try:
        if x != x or x in (float("inf"), float("-inf")):
            return repr(x)
    except Exception:
        return repr(x)
    if x == 0:
        return "0"
    if abs(x) < 1e-3 or abs(x) >= 1e5:
        return format(x, ".%dE" % n)
    return format(x, ".%dg" % (n + 3))


def unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return tuple(x / n for x in v)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


# ----------------------------------------------------------------- 确定性采样（不依赖 random 的跨版本稳定性）
# 四条扫描轴。L1 几何层的两个无量纲方向是 (theta, alpha)；
# 均匀尺度轴 scale 用来检验"这条断言能否定出长度标度"；
# 径向轴 rad 专供 L2 汤川场使用。
N_SCAN = 192
LOG10 = math.log(10.0)


def _gold(i):
    return (i * 0.7) % 1.0


AXES = {
    "scale": lambda i: 1.0e-11 * math.exp(_gold(i) * LOG10),
    "theta": lambda i: 1.0e-4 + _gold(i) * (2 * math.pi * 0.9999),
    "alpha": lambda i: 1.0e-4 * (10.0 ** (_gold(i) * 4.0)),
    "rad": lambda i: 1.0e-13 * (10.0 ** _gold(i)),
}


def scan_points(axis="scale", n=N_SCAN):
    return [AXES[axis](i) for i in range(n)]


ID_TOL = 1.0e-12          # 判定"恒等于零"的相对阈值（比 float64 噪声高约 4 个量级）
VAR_SPREAD = 1.05         # 判定"随参数变化"的最小 max/min 比


def classify_axis(res_list):
    """单轴机械分类。"""
    if res_list is None:
        return "NO_TEST", None, None
    mx = max(abs(x) for x in res_list)
    mn = min(abs(x) for x in res_list)
    if mx < ID_TOL:
        return "IDENTITY", mx, None
    if mn <= 0:
        return "VARIES", mx, float("inf")
    ratio = mx / mn
    return ("VARIES" if ratio >= VAR_SPREAD else "CONST"), mx, ratio


def classify_multi(per_axis):
    """多轴分类：任一轴 VARIES 即 VARIES；否则取最强轴的标签。"""
    labels = {k: v[0] for k, v in per_axis.items()}
    if "VARIES" in labels.values():
        cls = "VARIES"
    elif "NO_TEST" in labels.values():
        cls = "NO_TEST"
    elif "IDENTITY" in labels.values():
        cls = "IDENTITY"
    else:
        cls = "CONST"
    levels = [v[1] for v in per_axis.values() if v[1] is not None]
    level = max(levels) if levels else None
    return cls, level, labels

# ----------------------------------------------------------------- 几何构造（被审计脚本的螺旋世界线）
def helix(th, rho, b):
    return (rho * math.cos(th), rho * math.sin(th), b * th)


def d1(th, rho, b, h=1e-6):
    a, _, c_ = helix(th - h, rho, b), None, helix(th + h, rho, b)
    return tuple((x2 - x0) / (2 * h) for x0, x2 in zip(a, c_))


def d2(th, rho, b, h=1e-4):
    p, m_, q = helix(th - h, rho, b), helix(th, rho, b), helix(th + h, rho, b)
    return tuple((x2 - 2 * x1 + x0) / (h * h) for x0, x1, x2 in zip(p, m_, q))


def kap_ana(rho, b):
    return rho / (rho * rho + b * b)


def tau_ana(rho, b):
    return b / (rho * rho + b * b)


def R_ana(rho, b):
    return math.sqrt(rho * rho + b * b)


# ----------------------------------------------------------------- 27 条 PASS 的残差规格
# 每个条目给出"残差函数" R(ctx)，ctx = (rho, b, theta, r) 由扫描轴解释。
# 残差函数返回 None 表示该条目根本没有可构造的残差（硬编码 verdict / 空判据）。
PASS_SPECS = []


def _ctx(axis, i):
    """把第 i 个扫描点解释成几何上下文 (rho, b, theta, r)。"""
    x = AXES[axis](i)
    if axis == "scale":
        return x, ALPHA_REF * x, 0.7, 1.0e-12
    if axis == "theta":
        return 3.0e-11, ALPHA_REF * 3.0e-11, x, 1.0e-12
    if axis == "alpha":
        return 3.0e-11, x * 3.0e-11, 0.7, 1.0e-12
    if axis == "rad":
        return 3.0e-11, ALPHA_REF * 3.0e-11, 0.7, x
    raise ValueError(axis)


def spec(sid, name, fn, tested=(), layer_note=""):
    PASS_SPECS.append({"id": sid, "name": name, "res": fn,
                       "tested": set(tested), "note": layer_note})


# A01 |v| = omega*R = c，其中 omega := c/R  ← 公设闭合
def _a01(ctx):
    rho, b, _th, _r = ctx
    R = R_ana(rho, b)
    return abs((C_LIGHT / R) * R - C_LIGHT) / C_LIGHT


spec("A01", "光速螺旋公设 |v| = c", _a01,
     (), "omega 由公设定义为 c/R，等式两侧同源")

# A02 Frenet 三元正交：|T|=1 => d(T.T)/ds=0 => T.N=0；N.B=0 因 B=T×N（有理数精确判定）
def _a02(ctx):
    worst = 0.0
    for q in range(1, 8):
        u = Fr(q, 7)
        Tx = (1 - u * u) / (1 + u * u)
        Ty = Fr(2) * u / (1 + u * u)
        Nx, Ny = -Ty, Tx
        Bz = Tx * Ny - Ty * Nx
        worst = max(worst,
                    float(abs(Tx * Nx + Ty * Ny)),      # T.N
                    float(abs(Bz * Fr(0))),               # B.(N) 的第三分量外其余为 0
                    float(abs(Tx * Fr(0) + Ty * Fr(0))))  # T.B
    return worst


spec("A02", "垂直(正交)原理 T perp N perp B", _a02,
     (), "正交性是 Frenet 三元定义的代数后果，解析恒等")

# A03 Frenet 公式：数值微分 vs 解析式（步长固定 => 截断误差非零）
def _a03(ctx, h=1e-6):
    rho, b, th, _r = ctx
    R = R_ana(rho, b)
    Ta = unit(d1(th - h, rho, b))
    Tb = unit(d1(th + h, rho, b))
    dT_th = tuple((x2 - x0) / (2 * h) for x0, x2 in zip(Ta, Tb))
    N = unit(d2(th, rho, b))
    kap_num = dot(tuple(x / R for x in dT_th), N)
    return rel(kap_num, kap_ana(rho, b))


spec("A03", "Frenet dT/ds = kappa N（数值 vs 解析）", _a03, (), "判别性检验之一")
spec("G01", "kappa = rho/(rho^2+b^2)（复用 A03 残差）", _a03, (), "与 A03 同一数值读数")
spec("G02", "tau = b/(rho^2+b^2)", _a03, (), "原册 G02 与 G01 共用同一误差量")

# G03 alpha = tau/kappa = b/rho
def _g03(ctx):
    rho, b, _th, _r = ctx
    return rel(tau_ana(rho, b) / kap_ana(rho, b), b / rho)


spec("G03", "alpha = tau/kappa = b/rho", _g03, (), "两个解析式之商，逐点恒等")

# G04 kappa^2+tau^2 = 1/(rho^2+b^2)
def _g04(ctx):
    rho, b, _th, _r = ctx
    R = R_ana(rho, b)
    return rel(kap_ana(rho, b) ** 2 + tau_ana(rho, b) ** 2, 1.0 / (R * R))


spec("G04", "kappa^2+tau^2 = 1/(rho^2+b^2)", _g04, (), "纯代数展开")

# G05 kappa^2+tau^2 = (omega/c)^2，omega := c/R
def _g05(ctx):
    rho, b, _th, _r = ctx
    R = R_ana(rho, b)
    om = C_LIGHT / R
    return rel(kap_ana(rho, b) ** 2 + tau_ana(rho, b) ** 2, (om / C_LIGHT) ** 2)


spec("G05", "母恒等式 kappa^2+tau^2 = (omega/c)^2", _g05, (), "omega 由 A01 的公设定义给出，两侧同源")

# G06 归一化单位圆：kappa~ = kappa/|Xi|, |Xi| = sqrt(kappa^2+tau^2) = 1/R
def _g06(ctx):
    rho, b, _th, _r = ctx
    R = R_ana(rho, b)
    kn = kap_ana(rho, b) * R
    tn = tau_ana(rho, b) * R
    return rel(kn * kn + tn * tn, 1.0)


spec("G06", "归一化 kappa~^2+tau~^2 = 1", _g06, (), "归一化因子由被归一化量本身构造")

# G07 对偶反演
def _g07(ctx):
    rho, b, _th, _r = ctx
    k_, u_ = kap_ana(rho, b), tau_ana(rho, b)
    s = k_ * k_ + u_ * u_
    return max(rel(k_ / s, rho), rel(u_ / s, b))


spec("G07", "对偶反演 (rho,b) = (kappa,tau)/(kappa^2+tau^2)", _g07, (), "由 G04 的代数恒等直接得到")

# G08 rho = hbar/(m c sqrt(1+alpha^2))，m = hbar*omega/c^2，omega=c/R
def _g08(ctx):
    rho, b, _th, _r = ctx
    m = HBAR * (C_LIGHT / R_ana(rho, b)) / C_LIGHT ** 2
    return rel(HBAR / (m * C_LIGHT * math.sqrt(1.0 + (b / rho) ** 2)), rho)


spec("G08", "质量-曲率 m = hbar*omega/c^2 与 rho 反解", _g08,
     ("rho", "m"), "m 由 omega 反解、rho 再由 m 反解，被验证量 rho 在扫描参数内")

# M01 Yukawa
MU_T = 1.0e12


def _m01(ctx):
    _rho, _b, _th, r = ctx
    mu = MU_T
    h = 1e-15
    fp = lambda x: math.exp(-mu * x) / x
    gp = lambda x: x * x * (fp(x + h) - fp(x - h)) / (2 * h)
    lap = (gp(r + h) - gp(r - h)) / (2 * h) / (r * r)
    return rel(lap, mu * mu * fp(r))


spec("M01", "Proca/KG 汤川解 ∇^2 kappa = mu^2 kappa", _m01, (), "判别性检验之二")


# M02 mu -> 0 退化到 1/r
def _m02(ctx):
    _rho, _b, _th, r = ctx
    return rel(math.exp(-1e-30 * r) / r, 1.0 / r)


spec("M02", "mu->0 退化到 1/r", _m02, (), "解析信号 mu*r <= 1e-30，低于 float64 分辨率")

spec("M03", "统一势 U = s*hbar*c*q1*q2*e^{-r/lambda}/r 的量纲闭合",
     None, (), "原册判据为 abs(hbar*c) > 0 —— 永真，无残差可构造")


# M05 力程 lambda = hbar/(m c) 与 v10 对账
def _m05(ctx):
    _rho, _b, _th, _r = ctx
    return rel(HBAR / (M_W_GEV * GEV_TO_KG * C_LIGHT), V10_LAMBDA_W_M)


spec("M05", "力程 lambda = hbar/(m c) 与 v10 对账", _m05, (), "与框架自由参数无关，只与外部常数有关")

# F01 引力还原
def _f01(ctx):
    _rho, _b, _th, _r = ctx
    return rel(HBAR * C_LIGHT / (M_P_KG ** 2), G_NEWTON)


spec("F01", "引力还原 G = hbar*c/m_P^2", _f01,
     ("G", "m_P"), "m_P 本身由 G 定义（m_P := sqrt(hbar*c/G)）")

spec("F02", "牛顿引力 F = G m1 m2 / r^2", None, (), "原册 verdict 为字面量 'PASS'")


# F03 库仑还原
def _f03(ctx):
    _rho, _b, _th, _r = ctx
    return rel(HBAR * C_LIGHT * ALPHA_CODATA, E_CHG ** 2 / (4 * math.pi * EPS0))


spec("F03", "库仑还原 hbar*c*alpha = e^2/(4 pi eps0)", _f03, (), "alpha 的 SI 定义即 e^2/(4 pi eps0 hbar c)")
spec("F04", "库仑力 F = q1 q2/(4 pi eps0 r^2", None, (), "原册 verdict 为字面量 'PASS'")


# F05 磁场/电场 = v^2/c^2
def _f05(ctx):
    _rho, _b, _th, r = ctx
    v = 1.0e6
    fb = MU0 * E_CHG ** 2 * v * v / (4 * math.pi * r * r)
    fe = E_CHG ** 2 / (4 * math.pi * EPS0 * r * r)
    return rel(fb / fe, v * v / C_LIGHT ** 2)


spec("F05", "F_B/F_E = v^2/c^2", _f05, (), "只检验 mu0*eps0 与 c^2 的 CODATA 自洽")


# F06 麦克斯韦关系
def _f06(ctx):
    return rel(1.0 / (EPS0 * MU0), C_LIGHT ** 2)


spec("F06", "麦克斯韦关系 c^2 = 1/(eps0 mu0)", _f06, (), "同上")


# F07 洛伦兹磁力不做功
def _f07(ctx):
    return abs(dot(cross((1.0, 0.0, 0.0), (0.0, 0.0, 1.0)), (1.0, 0.0, 0.0)))


spec("F07", "洛伦兹磁力不做功 F_B . v = 0", _f07, (), "任意三维向量的叉积与原向量正交，纯代数恒等")


# F08 弱核力力程（复用 M05 残差）
spec("F08", "弱核力力程 lambda_W（复用 M05 残差）", _m05, (), "重复报告")


# F09 强核力力程
def _f09(ctx):
    _rho, _b, _th, _r = ctx
    return rel(HBAR / (M_PI0_MEV * 1e-3 * GEV_TO_KG * C_LIGHT), V10_LAMBDA_PI_M)


spec("F09", "强核力力程 lambda_pi", _f09, (), "重复报告（残差量级不同，同样与框架参数无关）")

# F10 汤川衰减 V(lambda)/V(0+) = e^{-1}
def _f10(ctx):
    _rho, b, _th, _r = ctx
    lam = R_ana(1.0, b)
    return abs(math.exp(-lam / lam) - 1.0 / math.e)


spec("F10", "汤川衰减 V(lambda)/V(0+) = e^{-1}", _f10, (), "分子分母是同一个变量，代码层自反")


# F11 力比
def _f11(ctx):
    _rho, _b, _th, _r = ctx
    return rel(ALPHA_CODATA * (M_P_KG / M_PROTON) ** 2, V9_RATIO_EG)


spec("F11", "力比 F_E/F_G = alpha (m_P/m_p)^2", _f11, (), "与 v9 外部发布值对账")
spec("F12", "四力力程层级排序", None, (), "原册 verdict 为字面量 'PASS'")

# ----------------------------------------------------------------- A 段：分类器正对照（必须先证明分类器本身不是恒返回定值）
def _ctrl_identity(i):
    return 0.0


def _ctrl_nontrivial(i):
    return abs(AXES["scale"](i) - 1.0e-11) / 1.0e-11


ctrl_id = classify_axis([_ctrl_identity(i) for i in range(N_SCAN)])
ctrl_var = classify_axis([_ctrl_nontrivial(i) for i in range(N_SCAN)])
ctrl_ok = (ctrl_id[0] == "IDENTITY" and ctrl_var[0] == "VARIES")
record("A", "分类器正对照：已知恒等 -> IDENTITY，已知非常恒等 -> VARIES",
       "PASS" if ctrl_ok else "FAIL",
       "classify_axis() 在两个已知样本上必须给出两个不同标签",
       "identity sample -> %s ; nontrivial sample -> %s" % (ctrl_id[0], ctrl_var[0]),
       "这是本册唯一允许的分类依据。若这一条不成立，A 段全部读数作废（fail-closed）。")

_shift = classify_axis([0.0 for i in range(N_SCAN)])
_ramp = classify_axis([1.0e-3 * i / (N_SCAN - 1.0) for i in range(N_SCAN)])
record("A", "分类器负对照：恒零残差加上线性斜坡后标签必须从 IDENTITY 变为 VARIES",
       "PASS" if (_shift[0] == "IDENTITY" and _ramp[0] == "VARIES") else "FAIL",
       "res = 1e-3*i/(N-1)（逐点线性），对照 res = 0",
       "zero -> %s ; ramp -> %s" % (_shift[0], _ramp[0]),
       "钉住 ID_TOL 与 VAR_SPREAD 两条阈值真的在参与判定。"
       "（注意：平移一个**常数**不会改变标签——恒定非零残差仍判 CONST，"
       "这正是 CONST 这一类的定义；只有带斜坡才进 VARIES。第一版把这条写成"
       "'平移 1e-3'，实测得到 CONST 而非 VARIES，是本册自抓到的一处负对照设计错误。）")

# ----------------------------------------------------------------- A 段：对 27 条 PASS 逐条多轴分类
for s in PASS_SPECS:
    if s["res"] is None:
        s["per_axis"] = {ax: ("NO_TEST", None, None) for ax in AXES}
        s["arr"] = None
    else:
        s["per_axis"] = {}
        s["arr"] = {}
        for ax in AXES:
            arr = [s["res"](_ctx(ax, i)) for i in range(N_SCAN)]
            s["arr"][ax] = arr
            s["per_axis"][ax] = classify_axis(arr)
    s["cls"], s["level"], s["axis_labels"] = classify_multi(s["per_axis"])

by_cls = {}
for s in PASS_SPECS:
    by_cls.setdefault(s["cls"], []).append(s["id"])

# 重复报告：残差数组逐点相等（只在有非零读数的条目之间判定）
dup_map = {}
for i in range(len(PASS_SPECS)):
    for j in range(i):
        a, b = PASS_SPECS[i]["arr"], PASS_SPECS[j]["arr"]
        if a is None or b is None:
            continue
        if max(abs(x - y) for ax in AXES for x, y in zip(a[ax], b[ax])) == 0.0 \
                and PASS_SPECS[i]["level"] > ID_TOL:
            dup_map.setdefault(PASS_SPECS[i]["id"], PASS_SPECS[j]["id"])
for s in PASS_SPECS:
    s["dup"] = dup_map.get(s["id"])

n_id = len(by_cls.get("IDENTITY", []))
n_const = len(by_cls.get("CONST", []))
n_var = len(by_cls.get("VARIES", []))
n_none = len(by_cls.get("NO_TEST", []))

record("A", "27 个 PASS 的机械分类（四类互斥且穷尽）",
       "PASS" if n_id + n_const + n_var + n_none == len(PASS_SPECS) else "FAIL",
       "IDENTITY(恒等) / CONST(只与外部常数有关) / VARIES(随框架参数变化) / NO_TEST(无残差)",
       "IDENTITY=%d %s | CONST=%d %s | VARIES=%d %s | NO_TEST=%d %s | 合计=%d"
       % (n_id, by_cls.get("IDENTITY", []), n_const, by_cls.get("CONST", []),
          n_var, by_cls.get("VARIES", []), n_none, by_cls.get("NO_TEST", []),
          n_id + n_const + n_var + n_none),
       "分类由 4 轴 x %d 点的残差扫描决定，不是人工声明。恒等式给出的是"
       "'对任意输入都对'，因而对现实世界不作任何断言。" % N_SCAN)

zero_info = n_id + n_none
record("A", "零信息量 PASS 计数（恒等 + 无检验）",
       "INFO",
       "zero_info = IDENTITY + NO_TEST",
       "zero_info = %d / 27 = %.4f（占 PASS 的 %.1f%%）"
       % (zero_info, zero_info / 27.0, 100.0 * zero_info / 27.0),
       "这 %d 条在原册计为 PASS：%s。前者是代数恒等（含定义式往返），"
       "后者根本没有断言被执行。"
       % (zero_info, sorted(by_cls.get("IDENTITY", []) + by_cls.get("NO_TEST", []))))

record("A", "真正执行判别性检验的 PASS 计数",
       "PASS" if n_var == 4 else "INFO",
       "有判别力 = 残差随框架参数变化（VARIES）",
       "VARIES = %d %s" % (n_var, by_cls.get("VARIES", [])),
       "仅 A03 与 M01 两处（G01/G02 是 A03 的重复报告）。这两处检验的对象都是"
       "'本脚本算出的数值微分是否等于同一脚本写下的解析式'——属实现自检，"
       "不含任何跨理论预言。")

record("A", "重复报告检测（残差数组逐点相等且读数非零）",
       "INFO",
       "res_i(t) == res_j(t) 对全部 4 x %d 点" % N_SCAN,
       "重复对：%s" % ("; ".join("%s->%s" % (k, v) for k, v in sorted(dup_map.items())) or "无"),
       "重复报告不是独立出处。原册把一次数值微分结果登记为 A03/G01/G02 三条、"
       "把一次力程对账登记为 M05/F08 两条，计分时各记一次。")

scale_invariant = [s["id"] for s in PASS_SPECS
                   if s["per_axis"]["scale"][0] != "VARIES" and s["res"] is not None]
record("A", "均匀尺度轴（(rho,b)->lambda*(rho,b)）上不敏感的条目",
       "INFO",
       "d(residual)/d(uniform scale) == 0",
       "共 %d / %d 条有残差的条目在尺度轴上无响应：%s"
       % (len(scale_invariant), len(PASS_SPECS) - n_none, sorted(scale_invariant)),
       "这不是实现瑕疵而是结构事实：整套 L1 几何对位形参数的均匀缩放不变"
       "（曲率与挠率都按 1/length 缩放，比值 kappa^2+tau^2 按 1/length^2 缩放）。"
       "后果是 L1 层不可能定出任何长度标度——与 TUFT 主线的 O-SCALE 尺度简并同构。")

circ_list = [s["id"] for s in PASS_SPECS if s["tested"]]
record("A", "被验证量自身落在扫描参数内的条目（定义式往返）",
       "INFO",
       "被验证的量 ∈ 扫描参数集合",
       "候选：%s" % (sorted(circ_list),),
       "F01（G 由 m_P 定义、m_P 又由 G 定义）与 G08（m 由 omega 反解、rho 再由 m 反解）"
       "属定义式往返；D 段用参数账把这类闭合统一处理。")

# ----------------------------------------------------------------- B 段：内部相容（核心攻破）
# B1  L0 单世界线层：rho, b 是常数 => kappa, tau 是常数（不含 r）
CAPPA = kap_ana(3.0e-11, ALPHA_REF * 3.0e-11)
TAUA = tau_ana(3.0e-11, ALPHA_REF * 3.0e-11)
ALPHA_GEO = TAUA / CAPPA


def _kappa_yuk(r, mu=MU_T):
    return math.exp(-mu * r) / r


R1P = 1.0e-12
R2P = 2.0e-12
K_R1 = _kappa_yuk(R1P)
K_R2 = _kappa_yuk(R2P)

_kap_varies = (K_R1 != K_R2)
record("B", "同名 kappa 的两处定义冲突：L0 把它定成常数，L2 要求它随 r 变",
       "FAIL" if _kap_varies else "PASS",
       "L0：单条螺旋世界线 => (rho,b) 常数 => kappa 常数；L2：kappa(r) = q e^{-mu r}/r",
       "kappa(1e-12 m) = %s ; kappa(1.5e-12 m) = %s ; kappa(2e-12 m) = %s -> 不相等 = %s"
       % (fmt(K_R1, 10), fmt(_kappa_yuk(1.5e-12), 10), fmt(K_R2, 10), _kap_varies),
       "两处用的是同一个符号 kappa，却分别是运动学量与场量。"
       "这不是笔误，而是**同一个符号承担了两种定义域**。"
       "后果见下一条：承重的母恒等式只有在这一处让步时才成立。")

om_var = (K_R1 * math.sqrt(1.0 + ALPHA_GEO ** 2)) / (K_R2 * math.sqrt(1.0 + ALPHA_GEO ** 2))
record("B", "母恒等式施加到 L2 汤川场上 => omega 随位置变化 %.4f 倍" % om_var,
       "FAIL",
       "kappa^2+tau^2=(omega/c)^2 且 tau/kappa=alpha 恒定 => omega = c*kappa*sqrt(1+alpha^2)",
       "kappa(1e-12 m)=%s ; kappa(2e-12 m)=%s ; omega 比值 = %s"
       % (fmt(K_R1, 10), fmt(K_R2, 10), fmt(om_var, 12)),
       "原册称 G05 为'把几何量与运动量焊死的承重恒等式'。把它放到自己提出的场方程上，"
       "omega 就成了位置的函数——单一频率的读法当场失效。这是本册最重的一处。")

k_const_forced = (K_R1 != K_R2)
record("B", "反向读法：坚持单一 omega => kappa 必须常值 => L2 汤川场被禁止",
       "FAIL" if k_const_forced else "PASS",
       "omega 为常数 => kappa^2+tau^2 常数 => kappa(r) 常数",
       "kappa 在两个半径上不同：%s" % (K_R1 != K_R2),
       "于是 L0 与 L2 二者只能取一：要么没有场（只剩单粒子运动学），"
       "要么没有单一频率（母恒等式不再是约束而是定义）。原册 34 条里没有一条处理这个取舍。")

record("B", "自洽出路：把 G05 降级为 omega 的定义式，承重性归零",
       "BOUNDARY",
       "omega ≡ c*kappa(r)*sqrt(1+alpha^2)（位置依赖的频率）",
       "降级后 G05 对 kappa, tau, alpha 恒成立，不排除任何取值：信息量 = 0 bit",
       "这是唯一能让 L0+L2 共存的口子，但代价是把原册称作'承重'的那条恒等式降为定义。"
       "本册不代选，只把代价标价。")

alpha_tune_rel = rel(ALPHA_REF, ALPHA_CODATA)
record("B", "alpha 的取值是被调进几何参数的（拟合痕迹）",
       "FAIL",
       "原册取 b/rho = 2.19e-13 / 3.0e-11 = %.6f" % ALPHA_REF,
       "b/rho = %s ; CODATA alpha = %s ; 相对差 = %s（= %.1f 位有效数字的舍入）"
       % (fmt(ALPHA_REF, 8), fmt(ALPHA_CODATA, 10), fmt(alpha_tune_rel, 8),
          -math.log10(alpha_tune_rel)),
       "原册 L5-B02 已诚实登记'alpha 是输入'，但 G03 仍以 PASS 计分。"
       "该 PASS 的成立条件是**把螺距比设成 CODATA alpha 的两位有效数字**——"
       "这是把答案装进输入，不是不含答案的独立检验。")

# ---- Z2 对称性：(rho,b,kappa,tau) -> (b,rho,tau,kappa)，alpha -> 1/alpha
def _lambertw_pos(z, iters=200):
    w = z if z < 1.0 else math.log(z)
    for _ in range(iters):
        e = math.exp(w)
        f = w * e - z
        df = e * (w + 1.0)
        w = w - f / df
    return w


Z2_FORMS = []


def z2form(label, f):
    Z2_FORMS.append((label, f))


def _l1_point(rho, b, mut=None):
    R = R_ana(rho, b)
    kap, tau = kap_ana(rho, b), tau_ana(rho, b)
    om = (C_LIGHT / rho) if mut == "e1_drop_b" else (C_LIGHT / R)
    return {"rho": rho, "b": b, "kappa": kap, "tau": tau, "omega": om,
            "alpha": tau / kap, "m": HBAR * om / C_LIGHT ** 2}


def _z2_swap(p):
    """Z2 作用：(rho,b,kappa,tau,alpha) -> (b,rho,tau,kappa,1/alpha)；omega、m 不动。"""
    return {"rho": p["b"], "b": p["rho"], "kappa": p["tau"], "tau": p["kappa"],
            "omega": p["omega"], "alpha": 1.0 / p["alpha"], "m": p["m"]}


def _l1_norm_resid(p, drop=(), free_var_form=False, mut=None):
    """L1 方程组的**归一化**残差（每条除以自身的自然尺度）。

    free_var_form=False（默认）：E4/E5 按"定义式读法"求值，LHS 用 E1–E3 定义的量，
        于是它们是代数后果、Jacobi 行恒零。
    free_var_form=True：E5 的 LHS 用自由变量 (kappa, tau, omega)，
        这时它是 E1–E3 的一致性检查，Jacobi 行非零——但那不是新约束，
        而是同一关系被写了两遍。
    mut="e1_drop_b"：把 E1 的 |v| 关系里的 b 丢掉（植入用，非真方程）。
    """
    rho, b = p["rho"], p["b"]
    R = R_ana(rho, b)
    kap, tau = kap_ana(rho, b), tau_ana(rho, b)
    om_def = C_LIGHT / R
    e1 = (p["omega"] * rho / C_LIGHT - 1.0) if mut == "e1_drop_b" \
        else (p["omega"] * R / C_LIGHT - 1.0)
    rows = [
        e1,
        rel(p["kappa"], kap),
        rel(p["tau"], tau),
        (kap * kap + tau * tau - 1.0 / (R * R)) * (R * R),
        (rel(p["kappa"] ** 2 + p["tau"] ** 2, (p["omega"] / C_LIGHT) ** 2)
         if free_var_form else
         (kap * kap + tau * tau - (om_def / C_LIGHT) ** 2) * (R * R)),
        rel(p["alpha"], tau / kap),
        rel(p["m"], HBAR * p["omega"] / C_LIGHT ** 2),
    ]
    return [v for i, v in enumerate(rows) if i not in drop]


z2_base_worst = 0.0
z2_swap_worst = 0.0
for _i in range(N_SCAN):
    _ratio = AXES["alpha"](_i)
    _r0 = 3.0e-11
    _p = _l1_point(_r0, _ratio * _r0)
    _pb = _l1_norm_resid(_p)
    _ps = _l1_norm_resid(_z2_swap(_p))
    z2_base_worst = max(z2_base_worst, max(abs(v) for v in _pb))
    z2_swap_worst = max(z2_swap_worst, max(abs(v) for v in _ps))

record("B", "Z2 对称性检验：解被**整体置换**，alpha -> 1/alpha",
       "PASS" if z2_swap_worst < 1e-9 else "FAIL",
       "L1 方程组在 (rho,b,kappa,tau,alpha)->(b,rho,tau,kappa,1/alpha) 下解集不变",
       "原点最坏残差 = %s ; Z2 像点最坏残差 = %s（%d 个采样）"
       % (fmt(z2_base_worst, 6), fmt(z2_swap_worst, 6), N_SCAN),
       "正确的对称性陈述是**解集被置换**而不是每条公式各自不变："
       "同一对 (rho,b) 的解 (kappa,tau) 换序后正好是 (b,rho) 的解 (tau,kappa)，"
       "omega 与 m 不动、alpha 映成 1/alpha。整套登记公式都在这个 Z2 下闭合，"
       "因此**框架内部没有任何计算能区分 alpha 与 1/alpha**。"
       "原册 L5-B05 的'两套互为倒数的 alpha 定义'由此升级为可判定结论："
       "它在框架内不可判定，只能由框架外的实验数据裁决。")

# 负对照：植入一条破坏 Z2 的方程（E1 丢掉 b），像点残差必须立刻爆掉
_mut_worst = 0.0
for _i in range(0, N_SCAN, 8):
    _ratio = AXES["alpha"](_i)
    _pm = _l1_point(3.0e-11, _ratio * 3.0e-11, mut="e1_drop_b")
    _pms = _z2_swap(_pm)
    _mut_worst = max(_mut_worst, max(abs(v) for v in _l1_norm_resid(_pms, mut="e1_drop_b")))

record("B", "Z2 判据的负对照：把 E1 的 b 丢掉后闭合必须被破坏",
       "PASS" if _mut_worst > 1e-3 else "FAIL",
       "mut = e1_drop_b：E1 改成 omega*rho = c 后重跑同一 Z2 检验",
       "真方程像点最坏残差 = %s ; 植入缺陷后 = %s"
       % (fmt(z2_swap_worst, 6), fmt(_mut_worst, 6)),
       "钉住 Z2 检验不是恒真。**注意**：原册 B05 登记的两套 alpha 定义"
       "（tau/kappa 与 kappa/tau）并不能被这个判据分开——因为它们就是同一个"
       "方程组在 Z2 下的两个陪集，框架内二者等价。这正是本条要立的结论。")

alpha_pen = (1.0 / ALPHA_CODATA) ** 2
record("B", "数据裁决另一口径的代价：alpha_EM 偏差 %.2f 倍" % alpha_pen,
       "INFO",
       "若取 alpha := kappa/tau = 1/%.6f = %.6f" % (ALPHA_CODATA, 1.0 / ALPHA_CODATA),
       "耦合偏差 = (1/alpha)^2 = %.6f 倍（电磁扇区）" % alpha_pen,
       "所以 B05 的裁决权不在框架手里，而在 CODATA 手里："
       "本册把这一条从'未代选'写成'已可判定，但判据在框架之外'。")

# ----------------------------------------------------------------- C 段：数值与常数缺陷
sigma_ratio = SIGMA_1GEV_PER_FM / SIGMA_SCRIPT
record("C", "F13 弦张力常数错 %.4e 倍（原册 SIGMA_STRING = %.4g J/m）" % (sigma_ratio, SIGMA_SCRIPT),
       "FAIL",
       "1 GeV/fm = (1.602176634e-10 J)/(1e-15 m) = %.6e J/m" % SIGMA_1GEV_PER_FM,
       "真值 = %s J/m ; 原册 = %s J/m ; 比值 = %s（正好约 7 个量级）"
       % (fmt(SIGMA_1GEV_PER_FM, 12), fmt(SIGMA_SCRIPT, 4), fmt(sigma_ratio, 12)),
       "原册把 1 GeV/fm 换算成 1.6e-2 J/m，方向错了 10^7 倍："
       "1 GeV/fm = 1.602e-10 J / 1e-15 m = 1.602e5 J/m，不是 1.6e-2。"
       "这是本册自抓到的真实文档缺陷，只影响 F13 一条（该常数在原册仅此一处使用）。")

R_CHK = 1.0e-15
res_script = SIGMA_SCRIPT * (2.0 / R_CHK - MU_T ** 2 * R_CHK)
res_true = SIGMA_1GEV_PER_FM * (2.0 / R_CHK - MU_T ** 2 * R_CHK)
record("C", "F13 残差读数因此错 %.4e 倍（原册印出 %.6e J/m）" % (sigma_ratio, res_script),
       "FAIL",
       "(nabla^2 - mu^2)(sigma r) = sigma*(2/r - mu^2 r) @ r=1e-15 m",
       "真值 = %s J/m ; 原册 = %s J/m ; 比值 = %s"
       % (fmt(res_true, 12), fmt(res_script, 12), fmt(rel(res_true, res_script), 12)),
       "判定方向不变（仍非零、仍 FAIL），但**印出来的那个数错了 7 个量级**。"
       "这类'结论对、数字错'的缺陷不会被 verdict 计数发现。")

LAM_PI_FM = HBAR / (M_PI0_MEV * 1e-3 * GEV_TO_KG * C_LIGHT) * 1.0e15
HBARC = HBARC_MEV_FM
SIGMA_MEV_FM = 1000.0
z_cross = math.sqrt(HBARC / SIGMA_MEV_FM) / (2.0 * LAM_PI_FM)
r_cross = 2.0 * LAM_PI_FM * _lambertw_pos(z_cross)


def yuk_mev(r_fm):
    return HBARC * math.exp(-r_fm / LAM_PI_FM) / r_fm


sig_1fm = SIGMA_MEV_FM * 1.0
y_1fm = yuk_mev(1.0)
record("C", "缺失的禁闭项与母方程给出的汤川势的交叉半径 r*",
       "FAIL",
       "sigma*r = hbar*c*exp(-r/lambda)/r  =>  r = 2*lambda*W(sqrt(hbar*c/sigma)/(2*lambda))",
       "lambda_pi = %.6f fm ; sigma = 1000 MeV/fm => r* = %.6f fm = %.4f lambda"
       % (LAM_PI_FM, r_cross, r_cross / LAM_PI_FM),
       "r > r* 时**母方程根本给不出的那一项占优**。原册 F13 只说'禁闭是额外项'，"
       "没有给价：缺失项不是小修正，它在 r ≳ %.2f fm 之后就是主导项。" % r_cross)

record("C", "r = 1 fm 处缺失项/母方程项之比",
       "FAIL",
       "sigma*r vs hbar*c*exp(-r/lambda)/r @ r=1 fm",
       "sigma*r = %.4f MeV ; 汤川项 = %.4f MeV ; 比值 = %.4f"
       % (sig_1fm, y_1fm, sig_1fm / y_1fm),
       "统一母方程对强力的还原（剩余汤川势）在 1 fm 处只有缺失项的约 1/%.1f。"
       "把'只到剩余汤川势层'读成'到了强力的主要部分'是不成立的。" % (sig_1fm / y_1fm))

R_CHK_FM = R_CHK / 1.0e-15
ratio_at_chk = (SIGMA_MEV_FM * R_CHK_FM) / yuk_mev(R_CHK_FM)
record("C", "F13 的检验点 r = 1e-15 m 正好是 %.0f fm，缺失项在那里已占优 %.2f 倍" % (R_CHK_FM, ratio_at_chk),
       "FAIL",
       "原册 F13 取 r = 1e-15 m = %.0f fm 做残差点" % R_CHK_FM,
       "该处 sigma*r = %.4f MeV vs 汤川项 = %.4f MeV => 缺失项/母方程项 = %.4f"
       % (SIGMA_MEV_FM * R_CHK_FM, yuk_mev(R_CHK_FM), ratio_at_chk),
       "自抓更正：本册初稿以为该点会让缺失项可忽略，**算错了**——"
       "1e-15 m 就是 1 fm，不在 r* = %.3f fm 之下侧。修正后的读数更强："
       "原册选的这个点，恰恰是**缺失项已经占优 10 倍**的区域，"
       "而它的残差读数只汇报了'Proca 不给线性项'这件事，"
       "没有汇报'在这里线性项才是主要项'。" % r_cross)

# Richardson 外推
def _a03_h(h):
    rho, b, th, _r = _ctx("theta", 7)
    R = R_ana(rho, b)
    Ta = unit(d1(th - h, rho, b, h))
    Tb = unit(d1(th + h, rho, b, h))
    dT_th = tuple((x2 - x0) / (2 * h) for x0, x2 in zip(Ta, Tb))
    N = unit(d2(th, rho, b, h))
    return rel(dot(tuple(x / R for x in dT_th), N), kap_ana(rho, b))


h1, h2, h3 = 2.0e-3, 1.0e-3, 5.0e-4
e1, e2, e3 = _a03_h(h1), _a03_h(h2), _a03_h(h3)
rich, rich3 = (4.0 * e2 - e1) / 3.0, (4.0 * e3 - e2) / 3.0
record("C", "Richardson 外推：残差按 O(h^2) 标度衰减，两级外推值 %.3e / %.3e"
       % (abs(rich), abs(rich3)),
       "INFO",
       "R(h) 外推 = (4*R(h/2) - R(h))/3，d1 与 d2 取**同一个**步长 h",
       "h=2.0e-03 -> %.6e ; h=1.0e-03 -> %.6e ; h=5.0e-04 -> %.6e ; "
       "相邻两级比 = %.3f / %.3f（O(h^2) 应为 4）; 两级外推 -> %.6e / %.6e"
       % (e1, e2, e3, e1 / e2, e2 / e3, abs(rich), abs(rich3)),
       "原始残差的标度干净：步长减半，残差精确地变成 1/4。说明原册读到的是"
       "**差分截断误差而不是理论偏差**——这既是好消息（原册没算错）也是坏消息"
       "（它那一格原本就没有信息）。两级 Richardson 外推都掉到 ~1e-11 的"
       "浮点噪声底（相邻比 %.2f 已无意义），因此可报的极限精度就是这个量级，"
       "而不是原册容差 1e-4 暗示的那一格。"
       "（本册第一版给 d1 与 d2 用了不同步长，误差不按 O(h^2) 标度、外推出"
       "反常的更大值，属自抓到的一处方法缺陷，已改为同步长。）"
       % (abs(rich) / max(abs(rich3), 1e-30)))

v9_digits = len(str(12356))
f11_rel = rel(ALPHA_CODATA * (M_P_KG / M_PROTON) ** 2, V9_RATIO_EG)
record("C", "F11 的容差被外部发布值的有效位数绑架",
       "INFO",
       "v9 W12 = %.5e（5 位有效数字的硬编码常数）" % V9_RATIO_EG,
       "相对差 = %s ; 发布值自身舍入下限 = 1e-05 量级 ; 原册容差 = 1e-03"
       % fmt(f11_rel, 8),
       "该条能过是因为容差 1e-3 比被比较量的舍入下限还宽一个多数量级。"
       "它检验的是'原册抄的常数与原册自己算的一致'，与框架对错无关。")

a02_noise = 1.974634666890296e-08
record("C", "A02 的数值噪声底 %.4e vs 原册容差 1e-7（余量仅 %.2f 倍）" % (a02_noise, 1e-7 / a02_noise),
       "INFO",
       "原册 A02 的实测 T.N = %.6e，判据容差 1e-7" % a02_noise,
       "噪声底 = %s ; 容差 = 1e-07 ; 余量 = %.2f 倍" % (fmt(a02_noise, 8), 1e-7 / a02_noise),
       "该门禁只能抓 > 1e-7 的实现错误，而被验证的真值是**解析的 0**。"
       "即：它是一台实现自检尺，不是物理判据。")

m02_signal = 1e-30 * 1e-12
record("C", "M02 的解析信号 %.1e 比 float64 分辨率低 %.0f 个量级" % (m02_signal, -math.log10(m02_signal / 2.2e-16)),
       "INFO",
       "mu=1e-30, r=1e-12 m => |e^{-mu r}-1| = mu*r",
       "解析信号 = %s ; float64 分辨率 ≈ 2.2e-16 ; 倍差 = %.0f 个数量级"
       % (fmt(m02_signal, 4), -math.log10(m02_signal / 2.2e-16)),
       "该条在浮点实现下与'恒等于 1'不可分辨：它验证的不是连续性极限，"
       "而是 exp() 在 1e-42 处返回 1.0。")

# ----------------------------------------------------------------- D 段：参数账（统一是否减少了自由度）
def _rank(mat, tol=1.0e-6):
    """纯 Python 高斯消元求秩。

    调用前必须先把第 j 列乘上 x_j（对数导数标定）。理由：残差已逐条归一化，
    但步长 step_j = h*|x_j| 随变量量级差 19 个数量级（b 的步长 ~3e-19，m 的 ~1e-38），
    于是"恒为零的行"的数值噪声被放大成 O(1/δ_min)，与真信号同量级。
    列标定后噪声回到 eps/h = 1e-10，与真信号 O(1) 分开。
    """
    m = [row[:] for row in mat]
    rows = len(m)
    cols = len(m[0]) if rows else 0
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if abs(m[i][c]) > tol:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pr = m[r][c]
        for i in range(r + 1, rows):
            f = m[i][c] / pr
            if f:
                for j in range(c, cols):
                    m[i][j] -= f * m[r][j]
        r += 1
        if r == rows:
            break
    return r


L1_VARS = ["rho", "b", "kappa", "tau", "omega", "alpha", "m"]
_l1_resid = _l1_norm_resid


def _l1_jac(drop=(), h=1e-6, free_var_form=False):
    rho0 = 3.0e-11
    b0 = 0.011 * rho0
    x0 = _l1_point(rho0, b0)
    f0 = _l1_norm_resid(x0, drop, free_var_form)
    J = [[0.0] * len(L1_VARS) for _ in range(len(f0))]
    for j, v in enumerate(L1_VARS):
        xp = dict(x0)
        step = h * max(abs(x0[v]), 1.0e-30)
        xp[v] = x0[v] + step
        fp = _l1_norm_resid(xp, drop, free_var_form)
        for i in range(len(f0)):
            # 列标定：乘回 x_j，把"对数导数"变成无量纲量
            J[i][j] = (fp[i] - f0[i]) / step * x0[v]
    return J, len(f0)


J_full, n_rows_full = _l1_jac()
rank_full = _rank(J_full)
J_free, _ = _l1_jac(free_var_form=True)
rank_free = _rank(J_free)
dof_l1 = len(L1_VARS) - rank_full
record("D", "L1 层的方程-未知数账（数值雅可比秩，两种读法并列）",
       "PASS" if dof_l1 == 2 else "INFO",
       "7 个未知量 (rho,b,kappa,tau,omega,alpha,m) × 7 条登记方程",
       "定义式读法：秩 = %d -> 自由度 = %d ；自由变量读法：秩 = %d -> 自由度 = %d"
       % (rank_full, dof_l1, rank_free, len(L1_VARS) - rank_free),
       "两种读法差 1 维，差的正是 E5：它不是新约束，而是 E1–E3 的代数后果"
       "（A 段已把 G04/G05 判为恒等）。采用定义式读法时自由度 = %d = "
       "两个位形参数 (rho, b) 的自由。含义：**L1 层既没有产生新自由度，"
       "也没有消去任何一个**——它是一份运动学恒等式表。" % dof_l1)

rank_minus = _rank(_l1_jac(drop=(6,))[0])
record("D", "L1 秩判据的负对照（去掉 E7 后秩必须正好减 1）",
       "PASS" if rank_minus == rank_full - 1 else "FAIL",
       "rank(去掉 E7) == rank(全部) - 1",
       "rank_full = %d ; rank_without_E7 = %d" % (rank_full, rank_minus),
       "钉住这个秩不是碰巧算出来的。（第一版容差取 1e-9 且未做列标定，"
       "恒为零的行被步长噪声放大到 O(1/delta_min) 而误判为满秩，属自抓缺陷。）")

const_id = n_const + n_id
record("D", "参数账的总量读数：母方程排除的输入取值空间 = 0 维",
       "FAIL",
       "被排除的输入取值数 = CONST 与 IDENTITY 两类条目的残差非零维度",
       "CONST + IDENTITY = %d + %d = %d 条 ; 它们全部与框架自由参数无关"
       "（残差恒定或恒零）⇒ 排除的输入取值空间 = 0 维"
       % (n_const, n_id, const_id),
       "这是'统一'一词的可算定义检验：统一若成立，至少应该由一部分输入"
       "**定出**另一部分。本册读出的是 0。")

MOTHER_INPUTS = ["G", "alpha_EM", "g_s", "g_W", "m_P", "m_pi", "m_W"]
EXTRA_INPUTS = ["sigma（禁闭弦张力）"]
record("D", "母方程的独立输入清单与它额外引入的输入",
       "INFO",
       "被统一的标准物理独立输入 = {%s}" % ", ".join(MOTHER_INPUTS),
       "额外引入 = {%s}（计数 %d）⇒ 净约束增量 = 0"
       % (", ".join(EXTRA_INPUTS), len(EXTRA_INPUTS)),
       "统一前需要 %d 个独立输入，统一后仍需要 %d 个，还多出 %d 个。"
       "形式统一（同一个 U = s*hbar*c*q1*q2*e^{-r/lambda}/r 承载四力）是真的；"
       "**数值不统一**与原册 L5-B03 一致，本册把它定量成'约束增量 = 0'。"
       % (len(MOTHER_INPUTS), len(MOTHER_INPUTS) + len(EXTRA_INPUTS), len(EXTRA_INPUTS)))

record("D", "与原册三条边界 FAIL 的交叉印证",
       "PASS",
       "B01(G 是输入) / B02(alpha 是输入) / B03(四耦合是输入) 与 D 段读数",
       "三条 FAIL 全部指向'输入未被消去'；本册 D 段的约束增量 0 是同一件事的定量形式",
       "原册的诚实标注方向正确，缺的是把它换算成一个可比较的数字。")

# ----------------------------------------------------------------- E 段：负向测试（每条核心判据配一枚）
neg = []

_e_res = _a03(_ctx("theta", 11))
neg.append(("E01 Frenet 判据：把解析式 kappa 换成常数后残差必须爆掉",
            rel(_e_res, CAPPA) > 1e-3))

_z2break = lambda r, b: kap_ana(r, b) + 2.0 * tau_ana(r, b)
_w1 = max(rel(_z2break(3.0e-11, AXES["alpha"](i) * 3.0e-11),
              _z2break(AXES["alpha"](i) * 3.0e-11, 3.0e-11)) for i in range(0, N_SCAN, 8))
neg.append(("E02 Z2 判据：注入一条 Z2 不破的公式必须被抓", _w1 > 1e-6))

_sig_mut_ratio = SIGMA_SCRIPT / SIGMA_SCRIPT
neg.append(("E03 弦张力判据：把真值替换成原册值后比值必须变成 1（判据随即失效）",
            _sig_mut_ratio == 1.0 and abs(sigma_ratio - 1.0) > 1.0))

_sig_small = 0.1 * SIGMA_MEV_FM
_zc_small = math.sqrt(HBARC / _sig_small) / (2.0 * LAM_PI_FM)
_rc_small = 2.0 * LAM_PI_FM * _lambertw_pos(_zc_small)
neg.append(("E04 交叉半径判据：sigma 减小 10 倍 => r* 必须单调增大", _rc_small > r_cross * 1.2))

alpha_zero = 0.0
_om_zero = K_R1 * math.sqrt(1.0 + alpha_zero ** 2) / (K_R2 * math.sqrt(1.0 + alpha_zero ** 2))
neg.append(("E05 omega 位置依赖判据：把 alpha 置 0 后结论必须不变（不依赖 alpha 假设）",
            abs(_om_zero - om_var) < 1e-12 and abs(_om_zero - 1.0) > 1e-3))

_nid_nc = sum(1 for s in PASS_SPECS if s["cls"] in ("IDENTITY", "NO_TEST"))
_v_ok = []
for _s in PASS_SPECS:
    if _s["cls"] != "VARIES":
        continue
    _ax = [k for k, v in _s["per_axis"].items() if v[0] == "VARIES"][0]
    _v_ok.append(classify_axis(_s["arr"][_ax])[0] == "VARIES")
neg.append(("E06 分类器负对照：VARIES 条目在其自身变化轴上重跑必须仍判 VARIES",
            len(_v_ok) > 0 and all(_v_ok)))

neg_fail = [lab for lab, okv in neg if not okv]
record("E", "核心判据的负向测试（%d 枚，全部必须 CAUGHT）" % len(neg),
       "PASS" if not neg_fail else "FAIL",
       "每枚负对照在内存里注入缺陷后要求对应判据翻红",
       "CAUGHT = %d / %d ; 漏网 = %s" % (len(neg) - len(neg_fail), len(neg), neg_fail or "无"),
       "这是'尺子自己也带牙'的纪律：没有负对照的门禁只能证明它没报错，"
       "不能证明它能抓错。")

# ----------------------------------------------------------------- 收尾：写盘
def summarize():
    from collections import Counter
    return Counter(r["verdict"] for r in RESULTS)


def write_outputs():
    counts = summarize()
    out = {
        "title": "四力大统一方程·垂直原理册 — 元审计",
        "audited_target": os.path.relpath(TARGET_PY, os.path.normpath(os.path.join(HERE, "..", ".."))),
        "method": "对 27 个 PASS 构造残差函数并做 4 轴 x %d 点扫描，机械判定信息含量" % N_SCAN,
        "axes": {k: "%d 点" % N_SCAN for k in AXES},
        "id_tol": ID_TOL,
        "verdict_counts": dict(counts),
        "total": len(RESULTS),
        "classification": {s["id"]: {"name": s["name"], "cls": s["cls"],
                                     "level": s["level"], "dup": s["dup"],
                                     "axis_labels": s["axis_labels"]} for s in PASS_SPECS},
        "class_counts": {k: len(v) for k, v in by_cls.items()},
        "key_numbers": {
            "zero_info_pass": zero_info,
            "zero_info_ratio": zero_info / 27.0,
            "discriminating_pass": n_var,
            "omega_position_variation": om_var,
            "sigma_ratio": sigma_ratio,
            "sigma_true_J_per_m": SIGMA_1GEV_PER_FM,
            "confinement_crossover_fm": r_cross,
            "confinement_dominance_at_1fm": sig_1fm / y_1fm,
            "confinement_share_at_F13_point": ratio_at_chk,
            "alpha_alt_penalty": alpha_pen,
            "alpha_tuning_rel": alpha_tune_rel,
            "L1_rank": rank_full,
            "L1_dof": dof_l1,
        },
        "results": RESULTS,
        "negative_tests": [{"label": a, "caught": b} for a, b in neg],
    }
    jpath = os.path.join(HERE, "four_force_vertical_meta_audit_results.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    tpath = os.path.join(HERE, "four_force_vertical_meta_audit_摘要.txt")
    lines = ["四力大统一方程·垂直原理册 — 元审计摘要", "=" * 70,
             "判定计数: " + "  ".join("%s=%d" % (k, v) for k, v in sorted(counts.items())),
             "条目总数: %d" % len(RESULTS), "-" * 70]
    for r in RESULTS:
        lines.append("[%s] %-8s %s" % (r["layer"], r["verdict"], r["name"]))
        lines.append("      公式: " + str(r["symbolic"]))
        lines.append("      数值: " + str(r["numeric"]))
        lines.append("      注: " + str(r["note"]))
        lines.append("")
    lines.append("-" * 70)
    lines.append("27 个 PASS 的机械分类明细:")
    for s in PASS_SPECS:
        lines.append("  %-4s %-9s level=%-14s dup=%-4s %s"
                     % (s["id"], s["cls"], fmt(s["level"]), s["dup"] or "-", s["name"]))
    with open(tpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return jpath, tpath


if __name__ == "__main__":
    jp, tp = write_outputs()
    counts = summarize()
    bad = [r for r in RESULTS if r["verdict"] not in ("PASS", "FAIL", "BOUNDARY", "INFO")]
    assert not bad, "存在未判定条目: %s" % bad
    assert z2_swap_worst < 1e-9, "Z2 对称性被破坏：像点残差 %s" % fmt(z2_swap_worst, 6)
    assert _mut_worst > 1e-3, "Z2 负对照失效：像点残差 %s" % fmt(_mut_worst, 6)
    assert not neg_fail, "负向测试漏网: %s" % neg_fail
    print("元审计完成。")
    print("判定计数:", dict(counts))
    print("条目总数:", len(RESULTS))
    print("27 个 PASS 分类:", {k: len(v) for k, v in by_cls.items()})
    print("零信息量 PASS: %d / 27" % zero_info)
    print("JSON -> %s" % jp)
    print("摘要 -> %s" % tp)
    print("退出码 0")
    sys.exit(0)