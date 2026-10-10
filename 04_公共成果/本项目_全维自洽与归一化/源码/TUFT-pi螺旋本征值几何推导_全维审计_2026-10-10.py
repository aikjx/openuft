# -*- coding: utf-8 -*-
"""
TUFT 空间光速螺旋「pi 螺旋本征值」几何推导 · 全维机器审计（r25）

来料：《pi 螺旋本征值几何推导（接续）》全文
  前段 第一~六章：公理 ds/dt=c → 幂级数定义 cos/sin → 闭合条件
        cos(theta0)=1, sin(theta0)=0 → 定义 2*pi := theta0 → 复原 C=2*pi*r
  §4   Frenet-Serret 标架；圆柱螺旋 kappa=a/(a^2+b^2), tau=b/(a^2+b^2)；
       螺旋本征值 lambda_pi = sqrt(a^2+b^2)
  §5   TUFT 场论耦合：kappa=c_perp/c^2, tau=c_parallel/c^2, omega=c_perp/a
       声称推出 omega = c*kappa
  §6   Darboux 旋量 Omega = tau*T + kappa*B，|Omega| = 1/sqrt(a^2+b^2)，
       闭合判据 ∮|Omega| ds = 2*pi*n
  §7   自然参数重写 kappa = r*omega^2/c^2, tau = v_z*omega/c^2, tau/kappa = v_z/(r*omega)
  §8   三条诘难答辩（幂级数不含 pi / 旋转一周不用圆 / 数值近似可严格化）
  §9   衔接德布罗意 lambda = s0 = 2*pi*r, omega = 2*pi*c/lambda, p = h/lambda, E = hbar*omega
  附件 h = 2*pi*c^3*r_e/G

分工声明（不重复造轮子）：
  - 本册只审「pi 的几何 / 拓扑本源」这一支。
  - 当日既有 r22 / r23 / r24 审「垂直原理四力统一框架」，与本册主题不重合，
    仅在需要处标注引用，不重算其读数。
  - S02 / S12 / S13 螺旋体系的既有结论不重复断言。

引擎：纯标准库（Decimal 60 位 + Fraction 量纲层 + float Simpson 数值积分）
评级目标：O / L2（审计链自身严格成立、全部机器可复算）
"""

from decimal import Decimal, getcontext
from fractions import Fraction
import json
import math
import os
import sys

getcontext().prec = 60

# ------------------------------------------------------------------ 输出守卫
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "数据")
os.makedirs(DATA_DIR, exist_ok=True)

BASENAME = "TUFT-pi螺旋本征值几何推导_全维审计_2026-10-10"

# ------------------------------------------------------------------ 常数
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798")
TWO_PI = 2 * PI

C_LIGHT = Decimal("299792458")
H_PLANCK = Decimal("6.62607015e-34")
HBAR_PUBLISHED = Decimal("1.054571817e-34")     # CODATA 公布值（仅 10 位有效数字）
HBAR = H_PLANCK / (2 * PI)                       # 符号层真源：h/(2*pi)，避免截断污染恒等判定
G_N = Decimal("6.67430e-11")
M_E = Decimal("9.1093837015e-31")
R_E_CLASSICAL = Decimal("2.8179403262e-15")

entered = {"n": 0}


def fm(x, spec=".6E"):
    """定点格式；精确零统一显示为 0E+0（避免 Decimal(0) 输出 0.000000E+6）"""
    if x == 0:
        return "0E+0"
    return format(x, spec)


# ------------------------------------------------------------------ 记录器
ENTRIES = []
GUARDS = []


def rec(cid, verdict, claim, evidence, note=""):
    global entered
    entered["n"] += 1
    ENTRIES.append({
        "id": cid,
        "verdict": verdict,
        "claim": claim,
        "evidence": evidence,
        "note": note,
    })


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    return bool(ok)


# ------------------------------------------------------------------ 高精度三角函数（纯幂级数）
def _reduce(x):
    k = int(x / TWO_PI)
    return x - Decimal(k) * TWO_PI


def _fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def dsin(x):
    """由幂级数定义，自变量已做 2*pi 周期归约与对称性压缩"""
    x = _reduce(x)
    sgn = Decimal(1)
    if x < 0:
        x = -x
        sgn = Decimal(-1)
    if x > TWO_PI / 2:
        x = TWO_PI - x
        sgn = -sgn
    if x > PI / 2:
        x = PI - x
    total = Decimal(0)
    term = x
    n = 0
    while n < 200:
        total += term
        n += 1
        term = -term * x * x / Decimal((2 * n) * (2 * n + 1))
        if abs(term) < Decimal("1e-64"):
            break
    return sgn * total


def dcos(x):
    x = _reduce(x)
    if x < 0:
        x = -x
    if x > TWO_PI / 2:
        x = TWO_PI - x
    flip = False
    if x > PI / 2:
        x = PI - x
        flip = True
    total = Decimal(0)
    term = Decimal(1)
    n = 0
    while n < 200:
        total += term
        n += 1
        term = -term * x * x / Decimal((2 * n - 1) * (2 * n))
        if abs(term) < Decimal("1e-64"):
            break
    return -total if flip else total


# ------------------------------------------------------------------ 向量（Decimal）
def vsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def vscale(a, k):
    return tuple(x * k for x in a)


def vdot(a, b):
    return sum((x * y for x, y in zip(a, b)), Decimal(0))


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def vnorm(a):
    return vdot(a, a).sqrt()


# ------------------------------------------------------------------ 量纲层（M, L, T）
D_M = (Fraction(1), Fraction(0), Fraction(0))
D_L = (Fraction(0), Fraction(1), Fraction(0))
D_T = (Fraction(0), Fraction(0), Fraction(1))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, k):
    return tuple(x * Fraction(k) for x in a)


def deq(a, b):
    return all(x == y for x, y in zip(a, b))


def dstr(a):
    names = ("M", "L", "T")
    parts = []
    for nm, p in zip(names, a):
        if p == 0:
            continue
        parts.append(nm + ("^" + str(p) if p != 1 else ""))
    return "1" if not parts else "*".join(parts)


# 一组待检量纲（符号层，Fraction，精确）
DIM_KAPPA_TRUE = D_L                                  # 曲率：L^-1
DIM_OMEGA_TRUE = dpow(D_T, -1)                        # 角频率：T^-1
DIM_C = ddiv(D_L, D_T)
DIM_ACTION = dmul(dmul(D_M, dpow(D_L, 2)), dpow(D_T, -1))   # h：[M L^2 T^-1]
DIM_MOMENTUM = dmul(dmul(D_M, D_L), dpow(D_T, -1))          # p：[M L T^-1]


# ------------------------------------------------------------------ 数值积分（float Simpson）
def simpson(f, a, b, n):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


# ================================================================== A 段：定义层（前段第一~三章）
def section_A():
    # ---- A1 幂级数定义 → Newton 求最小正根 theta0（不调用任何内置 pi 常数）
    th = Decimal("6.3")
    for _ in range(80):
        step = dsin(th) / dcos(th)
        th = th - step
        if abs(step) < Decimal("1e-55"):
            break
    res_root = abs(th - TWO_PI)
    res_cos = abs(dcos(th) - Decimal(1))
    ok = res_root < Decimal("1e-50") and res_cos < Decimal("1e-50")
    rec("A1", "PASS",
        "由幂级数定义的 cos/sin 出发，cos(theta)=1 且 sin(theta)=0 的最小正根存在且等于 2*pi",
        "Newton 迭代 theta0 = " + format(th, ".25E") +
        "；|theta0-2pi| = " + fm(res_root) +
        "；|cos(theta0)-1| = " + fm(res_cos),
        "作为『定义』这一层的确无逻辑循环：2*pi := theta0 是 pi 的一个合法等价定义（等价于『sin 的最小正零点之两倍』）。"
        "但这是数学上已知的等价定义之一，不改变 pi 的任何数值内容，也不使 pi 成为物理量。")
    guard("A1_newton_root", ok, "|theta0-2pi|=" + format(res_root, ".6E"))

    # ---- A2 两个闭合条件不独立（cos 条件为二重根）
    row_cos = abs(dsin(th))          # d/dtheta (cos theta - 1) 在根处的绝对值
    row_sin = abs(dcos(th))          # d/dtheta (sin theta) 在根处的绝对值
    rec("A2", "INFO",
        "闭合『方程组』cos(theta0)=1 与 sin(theta0)=0 是两个独立约束",
        "在根处 |d(cos-1)/dtheta| = |sin| = " + format(row_cos, ".6E") +
        "（=0，故 cos-1 在该点为二重根），|d(sin)/dtheta| = |cos| = " + format(row_sin, ".6E") +
        " ⇒ 局部只有一个有效方程（sin(theta)=0）；cos 条件由 sin^2+cos^2=1 与符号分支给出",
        "Jacobian 秩亏 ⇒ 来料『解超越方程组』实为解单个方程；并且 cos-1 是二重根，"
        "这决定了用 |cos-1|<eps 判定根的精度只能达到 sqrt(eps)（见 A3）。")

    # ---- A3 来料数值样例与其自身代码不自洽
    h_grid = Decimal("1e-6")
    eps = Decimal("1e-12")
    n_near = int((TWO_PI / h_grid).to_integral_value(rounding="ROUND_HALF_EVEN"))
    dist_nearest = abs(Decimal(n_near) * h_grid - TWO_PI)
    # 首 kmax 圈内的最佳网格命中
    best = None
    kmax = 3000
    for k in range(1, kmax + 1):
        target = TWO_PI * Decimal(k)
        nk = int((target / h_grid).to_integral_value(rounding="ROUND_HALF_EVEN"))
        dk = abs(Decimal(nk) * h_grid - target)
        if best is None or dk < best[1]:
            best = (k, dk)
    # 单条件变体：n=1 处 |cos(h)-1|
    cos_h_minus_1 = abs(dcos(h_grid) - Decimal(1))
    # 双精度下要达到 15 位 pi 所需容差
    eps_needed = (Decimal("1e-15") ** 2) / 2
    ulp1 = 2.0 ** -52          # IEEE double 在 [1,2) 区间的间距（Python 3.8 无 math.nextafter）
    rec("A3", "MISMATCH",
        "来料第五章数值样例（step=1e-6, precision=1e-12）输出 theta0=6.283185307179586 / pi=3.141592653589793",
        "网格最近点残差 |n*h-2pi| = " + format(dist_nearest, ".6E") +
        " ≫ 容差 1e-12；前 " + str(kmax) + " 圈内最佳网格残差 = " + format(best[1], ".6E") +
        "（第 " + str(best[0]) + " 圈）仍 >1e-12 ⇒ 该步长/容差组合下程序不返回首圈值；"
        "若按漂移后的第 k 圈返回 theta，则 pi=theta/2 得到的是 k*pi 而非 pi；"
        "单看 cos 条件则 n=1 处 |cos(h)-1| = " + format(cos_h_minus_1, ".6E") + " < 1e-12 ⇒ 首步即返回 pi≈5e-7；"
        "要由 |cos-1|<eps 判出 15 位 pi，需 eps≈" + format(eps_needed, ".6E") +
        "，而 IEEE double 在 1 附近的 ulp = " + format(Decimal(ulp1), ".6E") + " ⇒ 双精度下不可达",
        "来料印刷的输出样例无法由其自身代码产生：习题级事实，但直接影响『已数值验证』的可信度。")

    # ---- A4 pi 对所有动力学参数不敏感
    rows = []
    worst = Decimal(0)
    for av in ["0.1", "1", "3.7"]:
        for bv in ["0", "0.5", "2.0"]:
            for cv in ["1.0", "299792458"]:
                a = Decimal(av)
                b = Decimal(bv)
                c = Decimal(cv)
                lam = (a * a + b * b).sqrt()
                omega = c / lam
                period = TWO_PI / omega
                # 由这套动力学反解 pi：pi = omega*period/2
                pi_back = omega * period / 2
                rows.append((av, bv, cv, pi_back))
                worst = max(worst, abs(pi_back - PI))
    rec("A4", "FAIL",
        "§3.3『pi 的数值由空间运动的动力学约束决定』",
        "在 (a,b,c) 的 18 组网格上（含 b=0 与 c=1 的量纲反常取值）反解 pi "
        "完全一致，最大偏差 " + format(worst, ".6E") +
        " ⇒ pi 对全部动力学参数 (a,b,omega,v_z,c) 严格不敏感",
        "被机器直接否证：动力学参数可以自由变动而 pi 不动，说明 pi 来自所选解析函数族本身，"
        "不是动力学的产物。这也使『由 closure 涌现』失去筛选力（任意参数都给出同一 theta0）。")


# ================================================================== B 段：圆从何处来（§8.1 / §8.2 答辩）
def section_B():
    # ---- B1 圆是被 ansatz 带进来的，不是闭合条件导出的
    worst = Decimal(0)
    for u in ["0", "0.3", "1.1", "2.9", "5.7"]:
        uu = Decimal(u)
        for a in ["1", "2.6"]:
            aa = Decimal(a)
            x = aa * dcos(uu)
            y = aa * dsin(uu)
            worst = max(worst, abs(x * x + y * y - aa * aa))
    rec("B1", "FAIL",
        "§8.1/§8.2『不依赖预先存在的圆概念；圆是闭合条件的导出结果』",
        "对 ansatz x=a*cos(u), y=a*sin(u)，恒有 x^2+y^2=a^2，"
        "最大残差 " + format(worst, ".6E") + "（机器零），且该式对任意 u 成立、与 theta0 数值无关",
        "圆的形状在选择 cos/sin 作为轨道函数的那一刻就已确定；闭合条件只给 theta0 取了个名字。"
        "因此传统体系的因果顺序并未被反转，被换掉的只是『命名次序』。")

    # ---- B2 同一闭合条件在邻近 ansatz 上给出不同的 C/r
    #      星形线 x=a*cos^3 u, y=a*sin^3 u：同样要求 cos u0=1, sin u0=0 ⇒ u0=2*pi
    def speed_astroid(u):
        c = math.cos(u)
        s = math.sin(u)
        return 3.0 * abs(s * c)
    C1 = simpson(speed_astroid, 0.0, 2.0 * math.pi, 4000)
    C2 = simpson(speed_astroid, 0.0, 2.0 * math.pi, 20000)
    conv = abs(C1 - C2)
    rec("B2", "FAIL",
        "§四章『周长公式 C=2*pi*r 是螺旋动力学的推导结果，不是前置公理』",
        "取同一族周期函数构建的邻近 ansatz x=a*cos^3(u), y=a*sin^3(u)，"
        "其闭合条件同样是 cos(u0)=1 且 sin(u0)=0 ⇒ u0=2*pi（与来料逐字相同），"
        "但它的周长 C = " + format(Decimal(C2), ".15E") + " * a 而 2*pi*a = " +
        format(Decimal(2.0 * math.pi), ".15E") + " * a；比值 C/(2*pi*a) = " +
        format(Decimal(C2 / (2.0 * math.pi)), ".12E") + "（解析值 3/pi），"
        "步长收敛残差 " + format(Decimal(conv), ".6E"),
        "决定性反证：闭合条件完全相同的两条轨迹给出不同的 C/r ⇒ C=2*pi*r 不可能由闭合条件导出，"
        "它由所选的（圆）函数族决定。来料所谓『消除逻辑循环』不成立。")

    # ---- B3 三维闭合判据对螺旋不可满足
    out = []
    for b in ["0", "0.001", "0.5", "1.0", "3.0"]:
        bb = Decimal(b)
        a = Decimal("1")
        lam = (a * a + bb * bb).sqrt()
        c = C_LIGHT
        omega = c / lam
        vz = bb * omega
        T = TWO_PI / omega
        gap = abs(vz * T)          # 一周期后 z 方向的位移
        out.append((b, gap))
    txt = "; ".join("b=" + b + " ⇒ |z(T)-z(0)|=" + format(g, ".6E") + " m" for b, g in out)
    rec("B3", "FAIL",
        "§8.2『寻找最小 T>0 使三维空间坐标 r(T)=r(0)；纯点集判据，不需要圆』",
        txt + " ⇒ b≠0 时该判据无解；真正被使用的是 xy 投影闭合",
        "§8.2 的答辩与螺旋本体直接矛盾：圆柱螺旋 z(t)=v_z*t 单调，永不在三维闭合。"
        "若改用全文实际采用的投影闭合 cos(omega*T)=1，则该条件只涉及投影圆 ⇒ 平面圆正是被假定而非导出。")

    # ---- B4 lambda_pi 名实不符 + 无离散性
    checks = []
    for a in ["0.2", "1", "5"]:
        for b in ["0", "0.7", "2.3"]:
            aa = Decimal(a)
            bb = Decimal(b)
            lam = (aa * aa + bb * bb).sqrt()
            ds = TWO_PI * lam
            dphi = TWO_PI
            checks.append(abs(ds / dphi - lam))
    worst = max(checks)
    rec("B4", "INFO",
        "§4『定义螺旋本征值 lambda_pi = Delta_s / Delta_phi』，宣称 pi 是闭合旋转轨道的本征谱元",
        "Delta_s/Delta_phi = 2*pi*lambda/(2*pi) = lambda，pi 在定义中严格抵消，"
        "9 组参数机器残差 " + format(worst, ".6E") +
        "；且 lambda 随 (a,b) 连续取值于 (0, 无穷)，不构成离散谱",
        "『本征值』无对应算符、无离散性、且不含 pi：是尺度因子的重命名。"
        "可作为恒等式记账，但不得作为『pi 的谱起源』的证据。")


# ================================================================== C 段：曲率 / 挠率层（§4 / §5 / §7）
def _helix_frame(a, b, s):
    """由位置矢量独立复算 Frenet 量（解析导数，非有限差分）"""
    lam = (a * a + b * b).sqrt()
    u = s / lam
    su, cu = dsin(u), dcos(u)
    r1 = (-a / lam * su, a / lam * cu, b / lam)
    r2 = (-a / (lam * lam) * cu, -a / (lam * lam) * su, Decimal(0))
    r3 = (a / (lam ** 3) * su, -a / (lam ** 3) * cu, Decimal(0))
    return lam, u, r1, r2, r3


def section_C():
    a = Decimal("1.3")
    b = Decimal("0.9")
    lam, u, r1, r2, r3 = _helix_frame(a, b, Decimal("0.77"))
    T = r1
    kap_num = vnorm(r2)                     # |r'| = 1 时曲率 = |r''|
    N = vscale(r2, Decimal(1) / kap_num)
    Bv = vcross(T, N)
    # 挠率：tau = det(r',r'',r''') / |r''|^2
    det = vdot(vcross(r1, r2), r3)
    tau_num = det / (kap_num * kap_num)
    kap_ch4 = a / (a * a + b * b)
    tau_ch4 = b / (a * a + b * b)
    unit_res = abs(vnorm(r1) - Decimal(1))
    kap_res = abs(kap_num - kap_ch4)
    tau_res = abs(tau_num - tau_ch4)
    orth_res = max(abs(vdot(T, N)), abs(vdot(T, Bv)), abs(vdot(N, Bv)))
    om_res = abs((kap_num * kap_num + tau_num * tau_num).sqrt() - Decimal(1) / lam)

    # Frenet ODE 数值校核（中心差分）
    hh = Decimal("1e-15")
    _, _, Tp, _, _ = _helix_frame(a, b, Decimal("0.77") + hh)
    _, _, Tm, _, _ = _helix_frame(a, b, Decimal("0.77") - hh)
    dT = vscale(vsub(Tp, Tm), Decimal(1) / (2 * hh))
    ode_res = vnorm(vsub(dT, vscale(N, kap_num)))

    rec("C1", "PASS",
        "§4 圆柱螺旋 kappa=a/(a^2+b^2), tau=b/(a^2+b^2) 与 §7 kappa=r*omega^2/c^2, tau=v_z*omega/c^2 互洽",
        "由位置矢量独立复算（det 公式，非查表达式）：|r'|-1 = " + fm(unit_res) +
        "；kappa 残差 " + fm(kap_res) + "；tau 残差 " + fm(tau_res) +
        "；标架正交性残差 " + fm(orth_res) +
        "；|Omega|-1/lambda 残差 " + fm(om_res) +
        "；Frenet 第一式 dT/ds=kappa*N 中心差分残差 " + fm(ode_res),
        "这是全来料中唯一完全站得住的板块：§4 与 §7 两套写法严格互洽，且与标准微分几何一致。")
    guard("C1_frenet_selfconsistency",
          max(unit_res, kap_res, tau_res, orth_res, om_res) < Decimal("1e-40")
          and ode_res < Decimal("1e-6"),
          "max res=" + format(max(unit_res, kap_res, tau_res, orth_res, om_res), ".6E"))

    # ---- C2 §5 的 kappa = c_perp/c^2
    dim_claim = ddiv(DIM_C, dpow(DIM_C, 2))          # c_⊥/c^2
    dim_true = DIM_KAPPA_TRUE
    same_dim = deq(dim_claim, dim_true)
    rows = []
    for av, bv in [("1", "1"), ("1", "0.25"), ("2", "1")]:
        aa = Decimal(av)
        bb = Decimal(bv)
        lam = (aa * aa + bb * bb).sqrt()
        c = C_LIGHT
        c_perp = c * aa / lam
        claim = c_perp / (c * c)
        true = aa / (lam * lam)
        rows.append((av, bv, claim, true, claim / true))
    ev = "; ".join("(a,b)=(" + av + "," + bv + "): 来料式=" + format(cl, ".12E") +
                   " / 正确式=" + format(tr, ".12E") + " 比值=" + format(rt, ".12E")
                   for av, bv, cl, tr, rt in rows)
    rec("C2", "FAIL",
        "§5『kappa = c_⊥/c^2，tau = c_∥/c^2，量纲自洽』",
        "量纲层：[c_⊥/c^2] = " + dstr(dim_claim) + " vs [kappa] = " + dstr(dim_true) +
        " ⇒ " + ("一致" if same_dim else "不一致（多出一个 T，即比值因子具时间量纲）") +
        "；数值层 " + ev + "；比值恰等于 lambda/c（= 一周期弧长除以光速，量纲 T）",
        "最小修复：右端补一个因子 omega ⇒ kappa = c_⊥*omega/c^2, tau = c_∥*omega/c^2（此时量纲 L^-1 且数值精确）。"
        "这是典型的『单位约定未登记』型缺陷（隐含要求 lambda = c 的数值），复发族同 r19 的 T_μν 系数 1/f vs c^4/f。")

    # ---- C3 omega = c*kappa 的成立域
    rows = []
    for bv in ["0", "0.001", "0.05", "0.25", "1", "2", "10"]:
        bb = Decimal(bv)
        aa = Decimal("1")
        lam = (aa * aa + bb * bb).sqrt()
        c = C_LIGHT
        omega = c / lam
        kap = aa / (lam * lam)
        rhs = c * kap
        rows.append((bv, (omega - rhs) / omega))
    ev = "; ".join("b/a=" + bv + ": 相对残差=" + fm(r_) for bv, r_ in rows)
    # 正确不变量
    worst_ok = Decimal(0)
    for bv in ["0", "0.25", "1", "3", "10"]:
        bb = Decimal(bv)
        aa = Decimal("1")
        lam = (aa * aa + bb * bb).sqrt()
        omega = C_LIGHT / lam
        kap = aa / (lam * lam)
        tau = bb / (lam * lam)
        worst_ok = max(worst_ok, abs(omega - C_LIGHT * (kap * kap + tau * tau).sqrt()) / omega)
    rec("C3", "FAIL",
        "§5『联立得 omega = c*kappa；几何曲率直接对应角频率』",
        ev + "；正确不变量 omega = c*sqrt(kappa^2+tau^2) 的最大相对残差 " +
        format(worst_ok, ".6E"),
        "omega=c*kappa 当且仅当 b=0（相对残差因子恰为 lambda/a = c/c_⊥）⇒ 只在 tau=0 的平面圆极限成立。"
        "而 b=0 时螺旋塌缩为圆、tau 恒 0，§6『pi 非平面专属』的前提同时消失 ⇒ 自我否证。"
        "正确式 omega = c*sqrt(kappa^2+tau^2) 即本库主线已知的 kappa^2+tau^2=(omega/c)^2；"
        "来料是把该恒等式丢掉 tau 后写成的新形式。")

    # ---- C4 §5 与 §7 的同名量冲突
    aa = Decimal("1")
    bb = Decimal("1")
    lam = (aa * aa + bb * bb).sqrt()
    c = C_LIGHT
    omega = c / lam
    k5 = (c * aa / lam) / (c * c)
    k7 = aa * omega * omega / (c * c)
    rec("C4", "MISMATCH",
        "§5 的 kappa = c_⊥/c^2 与 §7 的 kappa = r*omega^2/c^2 描述同一物理量",
        "取 a=r=1, b=1：§5 式 = " + format(k5, ".12E") + "，§7 式 = " + format(k7, ".12E") +
        "；比值 " + format(k5 / k7, ".12E") + "（= lambda/c，单位 s）",
        "同一份文稿的两章给出互相矛盾的曲率表达式（相差 lambda/c，约 10^-9 s 量级因子）；"
        "若不同 amoeba 章节被分别引用，读数会差 9 个量级。此为**跨节口径冲突**，须在数据字典登记。")


# ================================================================== D 段：守恒量与「量子化」（§6）
def section_D():
    # ---- D1 ∮|Omega| ds = 2*pi*n 的筛选力
    worst = Decimal(0)
    n_ok = 0
    for av in ["0.05", "0.3", "1", "7.5"]:
        for bv in ["0", "0.2", "1.9", "12"]:
            aa = Decimal(av)
            bb = Decimal(bv)
            lam = (aa * aa + bb * bb).sqrt()
            integ = (Decimal(1) / lam) * (TWO_PI * lam)
            worst = max(worst, abs(integ - TWO_PI))
            n_ok += 1
    rec("D1", "FAIL",
        "§6『轨道闭合判据 ∮|Omega| ds = 2*pi*n（缠绕数），pi 来自闭合流形上标架转动的拓扑缠绕数』",
        str(n_ok) + " 组 (a,b)（含 b=0 与极端轴径比）全部精确成立，与 2*pi 最大偏差 " +
        format(worst, ".6E") + "；且 n 恒为 1，不随参数变化",
        "零筛选力：该式是 Omega=1/lambda 与 Delta_s=2*pi*lambda 两个定义的代数乘积，"
        "恒等式复读（本库缺陷族复发）。任何 (a,b) 都『满足』它 ⇒ 它不选中任何东西，也不是量子化条件。")

    # ---- D2 一般闭合曲线的 |Omega| 积分不被 2*pi 量子化（定量反例）
    def rho_fn(d, sg):
        def f(t):
            z = (t - math.pi) / sg
            return 1.0 - d * math.exp(-0.5 * z * z)
        return f

    def rho_p_fn(d, sg):
        def f(t):
            z = (t - math.pi) / sg
            return d * z * math.exp(-0.5 * z * z) / sg
        return f

    def rho_pp_fn(d, sg):
        def f(t):
            z = (t - math.pi) / sg
            return d * math.exp(-0.5 * z * z) * (1.0 - z * z) / (sg * sg)
        return f

    def total_curvature(d, sg, N):
        r = rho_fn(d, sg)
        rp = rho_p_fn(d, sg)
        rpp = rho_pp_fn(d, sg)

        def psi_dot(t):
            ct, st = math.cos(t), math.sin(t)
            x1 = rp(t) * ct - r(t) * st
            y1 = rp(t) * st + r(t) * ct
            x2 = rpp(t) * ct - 2 * rp(t) * st - r(t) * ct
            y2 = rpp(t) * st + 2 * rp(t) * ct - r(t) * st
            sp2 = x1 * x1 + y1 * y1
            return (x1 * y2 - y1 * x2) / sp2

        return simpson(lambda t: abs(psi_dot(t)), 0.0, 2 * math.pi, N), psi_dot

    def total_variation(d, sg, N):
        r = rho_fn(d, sg)
        rp = rho_p_fn(d, sg)

        def psi(t):
            ct, st = math.cos(t), math.sin(t)
            return math.atan2(rp(t) * st + r(t) * ct, rp(t) * ct - r(t) * st)

        tv = 0.0
        prev = psi(0.0)
        for i in range(1, N + 1):
            t = 2 * math.pi * i / N
            cur = psi(t)
            dd = cur - prev
            while dd > math.pi:
                dd -= 2 * math.pi
            while dd < -math.pi:
                dd += 2 * math.pi
            tv += abs(dd)
            prev = cur
        return tv

    d0, sg0 = 0.8, 0.5
    tc1, psi_dot = total_curvature(d0, sg0, 40000)
    tc2, _ = total_curvature(d0, sg0, 160000)
    tv1 = total_variation(d0, sg0, 40000)
    rmin = min(rho_fn(d0, sg0)(2 * math.pi * i / 20000) for i in range(20001))
    per = abs(rho_fn(d0, sg0)(0.0) - rho_fn(d0, sg0)(2 * math.pi))
    # psi' 变号计数
    signs = 0
    prev_s = None
    for i in range(0, 4001):
        t = 2 * math.pi * i / 4000
        s = 1 if psi_dot(t) > 0 else -1
        if prev_s is not None and s != prev_s:
            signs += 1
        prev_s = s
    near2 = abs(tc2 - 2 * math.pi) / (2 * math.pi)
    near4 = abs(tc2 - 4 * math.pi) / (4 * math.pi)
    rec("D2", "FAIL",
        "§6 闭合缠饶判据 ∮|Omega| ds = 2*pi*n 具有一般性（对闭合轨道普遍成立）",
        "反例：光滑简单闭合（带深凹）曲线 rho(t)=1-0.8*exp(-(t-pi)^2/(2*0.5^2)) 的极坐标轨道，"
        "∮|kappa| ds = " + format(Decimal(tc2), ".15E") + " rad（2*pi=" +
        format(Decimal(2 * math.pi), ".15E") + "，4*pi=" + format(Decimal(4 * math.pi), ".15E") +
        "）；相对 2*pi 偏差 " + format(Decimal(near2), ".6E") + "，相对 4*pi 偏差 " +
        format(Decimal(near4), ".6E") + "；psi' 变号 " + str(signs) + " 次 ⇒ 切向角非单调；"
        "两条独立离散化互校：Simpson(N=4e4/1.6e5) 差 " + fm(Decimal(abs(tc1 - tc2))) +
        "，切向角全变差 " + format(Decimal(tv1), ".15E") + "；rho_min=" + str(round(rmin, 6)) +
        " >0（简单闭合），端点周期残差 " + fm(Decimal(per)),
        "真命题是 Fenchel 定理（∮|kappa| ds >= 2*pi，等号当且仅当凸平面曲线），"
        "而上界不存在、取值连续 ⇒ 不存在 2*pi 的整数量子化。来料把『圆形螺旋恰好等于 2*pi』读成了一般性判据。")

    # ---- D3 两种『总转动』定义给不同读数
    rows = []
    for bv in ["0", "0.5", "1", "3"]:
        bb = Decimal(bv)
        aa = Decimal("1")
        lam = (aa * aa + bb * bb).sqrt()
        darboux = TWO_PI                       # Darboux 旋量模积分
        tangent = TWO_PI * aa / lam            # 切向量球面像（indicatrix）的积分
        rows.append((bv, darboux, tangent))
    ev = "; ".join("b/a=" + bv + ": Darboux=" + format(db, ".12E") +
                   " vs 切向 indicatrix=" + format(tg, ".12E") for bv, db, tg in rows)
    rec("D3", "INFO",
        "§6『一周的标架总旋转增量恰为 2*pi』是唯一的自然读数",
        ev + " ⇒ 两种同样自然的『一周总转动』定义给出不同数值；只有选 Darboux 模长才恒等于 2*pi",
        "量的选择被调参到想要的结果（2*pi）；切向 indicatrix 读数在 b≠0 时严格小于 2*pi。"
        "属方法层面的自由度，须显式登记而不能作为证据。")


# ================================================================== E 段：德布罗意衔接（§9）
def section_E():
    rows = []
    for bv in ["0", "0.25", "1", "4"]:
        bb = Decimal(bv)
        aa = Decimal("1")
        lam = (aa * aa + bb * bb).sqrt()
        c = C_LIGHT
        omega = c / lam
        s0 = TWO_PI / (omega / c)        # §7.3：s0 = 2*pi/k_s = 2*pi*c/omega
        claim = TWO_PI * aa              # §9：lambda = s0 = 2*pi*r
        rows.append((bv, s0, claim, s0 / claim))
    ev = "; ".join("b/a=" + bv + ": s0=" + format(s0_, ".12E") + " vs 2*pi*r=" +
                   format(cl_, ".12E") + " 比值=" + format(rt_, ".12E")
                   for bv, s0_, cl_, rt_ in rows)
    rec("E1", "FAIL",
        "§9『螺旋一圈闭合弧长 s0 = 2*pi*r，即粒子物质波波长 lambda』",
        ev + "；比值恰为 lambda_helix/r = sqrt(1+(b/a)^2)",
        "第三处隐式退化：此式成立的充要条件仍是 v_z=0（b=0）。连同 C3（omega=c*kappa）与 B3（三维闭合），"
        "同一份文稿在三处关键结论上都必须回到平面圆极限，而此时 tau≡0，"
        "『pi 不是平面专属常数』这一核心 claim 的前提已被自身取消。")

    # E=hbar*omega 是否为几何推论
    lam = Decimal("1e-12")
    c = C_LIGHT
    omega = TWO_PI * c / lam
    p_pre = H_PLANCK / lam
    E_pc = p_pre * c
    E_hw = HBAR * omega
    resid_chain = abs(E_pc - E_hw) / E_pc
    trunc = abs(HBAR - HBAR_PUBLISHED) / HBAR
    rec("E2", "FAIL",
        "§9『E = hbar*omega 不再是量子力学的独立公理，而是光速螺旋闭合几何的推论』",
        "沿来料自身的链条复算：由 {E=pc, p=h/lambda, omega=2*pi*c/lambda, hbar=h/(2*pi)} "
        "得 E=pc=(h/lambda)c=(h*omega/(2*pi))=hbar*omega，数值残差 " +
        fm(resid_chain) + "（机器零，纯代数恒等）；"
        "（首跑曾读到 6.13E-10 的非零残差，根因是把 CODATA 只公布 10 位的 hbar 直接当常数用，"
        "其相对截断 " + fm(trunc) + "，本版已改用符号层 hbar=h/(2*pi)）；"
        "链条中唯一来自螺旋的项是 lambda = 2*pi*c/omega，而它正是 lambda=s0 的同义改写",
        "恒等式复读：{E=pc, p=h/lambda} 与 {E=hbar*omega, lambda=2*pi*c/omega} 互为代数重排，"
        "几何项在其中既非充分也非必要（换个传播模型同样可写出该链条）。"
        "真输入是两条：沿轨迹 E=pc 与德布罗意关系 p=h/lambda——两者皆非本框架推导所得。")


# ================================================================== F 段：常数层（前段第六章）
def section_F():
    DIM_G = (Fraction(-1), Fraction(3), Fraction(-2))     # [G] = M^-1 L^3 T^-2
    dim_expr = ddiv(dmul(dpow(ddiv(D_L, D_T), 3), D_L), DIM_G)     # c^3 * r_e / G
    expr = C_LIGHT ** 3 * R_E_CLASSICAL / G_N
    expr2 = C_LIGHT ** 3 * R_E_CLASSICAL ** 2 / G_N
    ratio1 = expr / H_PLANCK
    ratio2 = expr2 / H_PLANCK
    rec("F1", "FAIL",
        "前段第六章『h = 2*pi*c^3*r_e/G（pi 为螺旋闭合导出常数；h 由 r_e、c、G 共同给出）』",
        "量纲层：[c^3*r_e/G] = " + dstr(dim_expr) + "，而 [h] = " + dstr(DIM_ACTION) +
        " ⇒ 差一个长度量纲（所得是动量 " + dstr(DIM_MOMENTUM) + " 而非作用量）；"
        "数值层 c^3*r_e/G = " + format(expr, ".12E") + " kg*m/s，得上式后比 h 大 " +
        format(ratio1, ".12E") + " 倍；"
        "最小补维（再乘一个长度）c^3*r_e^2/G = " + format(expr2, ".12E") + " J*s，仍比 h 大 " +
        format(ratio2, ".12E") + " 倍",
        "双重 FAIL：量纲不成立 + 即便补足量纲也差约 40 个量级。该式不得作为『普朗克常数几何导出』的证据。")


# ================================================================== G 段：修复清单与分支选型
def section_G():
    # G1 最小修复清单（机器验证）
    worst_fix1 = Decimal(0)
    worst_fix2 = Decimal(0)
    for av in ["0.4", "1", "3.2"]:
        for bv in ["0", "0.3", "1", "5"]:
            aa = Decimal(av)
            bb = Decimal(bv)
            lam = (aa * aa + bb * bb).sqrt()
            c = C_LIGHT
            omega = c / lam
            kap = aa / (lam * lam)
            tau = bb / (lam * lam)
            c_perp = c * aa / lam
            c_par = c * bb / lam
            worst_fix1 = max(worst_fix1, abs(omega - c * (kap * kap + tau * tau).sqrt()) / omega)
            worst_fix2 = max(worst_fix2, abs(kap - c_perp * omega / (c * c)) / kap)
            worst_fix2 = max(worst_fix2, abs(tau - c_par * omega / (c * c)) / kap)
    ok = worst_fix1 < Decimal("1e-45") and worst_fix2 < Decimal("1e-45")
    rec("G1", "PASS",
        "最小修复清单 M1–M4 全部可机器验证",
        "M1 omega = c*sqrt(kappa^2+tau^2) 最大相对残差 " + format(worst_fix1, ".6E") +
        "；M2 kappa = c_⊥*omega/c^2, tau = c_∥*omega/c^2 最大相对残差 " +
        format(worst_fix2, ".6E") +
        "；M3 明确声明『闭合』是 xy 投影闭合（三维闭合在 b≠0 无解，见 B3）；"
        "M4 撤回 ∮|Omega|ds=2*pi*n 的量子化读法（见 D2）",
        "四条修复后 §4/§7 的计算板块保持完全正确（C1 已 PASS），且不再产生跨章口径冲突（C4）。")
    guard("G1_repairs_verified", ok, "worst=" + format(max(worst_fix1, worst_fix2), ".6E"))

    # G2 分支选型来账（回答来料末尾 A–F 六分支）
    zero_info_ids = ["A1", "B4", "D1", "D3", "E2"]
    rec("G2", "BOUNDARY",
        "来料末尾六分支（A 复解析延拓 / B 量纲全表 / C 牛顿法提速 / D 非圆柱螺旋 / E 引力耦合 / F 参考文献）选哪条",
        "本册可判账：①依赖量纲核验的硬缺陷 2 处（C2 的 kappa=c_⊥/c^2、F1 的 h 式）⇒ B 为强制前置；"
        "②零信息量（恒等式复读 / 参数不敏感）条目 " + str(len(zero_info_ids)) + " 处：" +
        ",".join(zero_info_ids) + "；③核心 claim『pi 非平面专属』已由 B2/B3/C3/D2 四面夹击判否；"
        "④A（复延拓）、C（换求根算法）、F（排版）三条不新增任何可证伪内容，属纯粹形式升级；"
        "⑤E（引力耦合）需要 T_μν，而 T_μν 须由作用量变分给出（[引用 r20] 最小闭合集代价 +2~4 参数，本册不重算）",
        "推荐次序：B（必做，清量纲账）→ D（决定性：它直接把核心 claim 判 FAIL，见 D2 的反例族）→ "
        "保留 M1–M4 修复后再谈 E；A/C/F 可并行但不得计入『已验证』条目数。")

    # G3 诚实边界：哪些仍然成立
    rec("G3", "INFO",
        "本册否证之后，来料中还剩什么",
        "仍然成立：①§4/§7 圆柱螺旋的 kappa、tau 计算与 Frenet 关系（C1 机器零）；"
        "②2*pi := theta0 作为 pi 的一个合法等价定义（A1，非新知识）；"
        "③不变量 omega = c*sqrt(kappa^2+tau^2)（M1，与主线三重奏同形式）；"
        "④欧氏平面的 C=2*pi*r 仍是标准恒等式——只是它由所选周期函数族而非由闭合条件给出（B2）",
        "不得宣称『pi 被物理推导』：pi 对所有动力学参数不敏感（A4），闭合条件不筛选 C/r（B2），"
        "量子化读数不成立（D2）。")


# ================================================================== 自检守卫（工具层）
def selfcheck():
    g1 = abs(dsin(Decimal(1)) - Decimal("0.84147098480789650665250232163029899962256306079837")) < Decimal("1e-40")
    guard("tools_dsin", g1, format(abs(dsin(Decimal(1))), ".6E"))
    g2 = abs(dcos(Decimal(1)) - Decimal("0.54030230586813971740093660744297660373231042061792")) < Decimal("1e-40")
    guard("tools_dcos", g2, format(abs(dcos(Decimal(1))), ".6E"))
    worst = Decimal(0)
    for x in ["0.37", "1.9", "-4.2", "12.7"]:
        xx = Decimal(x)
        worst = max(worst, abs(dsin(xx) ** 2 + dcos(xx) ** 2 - Decimal(1)))
    guard("tools_trig_identity", worst < Decimal("1e-50"), "max=" + format(worst, ".6E"))
    g4 = abs(dsin(PI / 6) - Decimal("0.5")) < Decimal("1e-50")
    guard("tools_sin_pi_over_6", g4, format(abs(dsin(PI / 6) - Decimal("0.5")), ".6E"))
    # Simpson 对已知积分的自校验：∫_0^{2pi} |sin(2u)| du = 4
    v = simpson(lambda t: abs(math.sin(2 * t)), 0.0, 2 * math.pi, 20000)
    guard("tools_simpson_known", abs(v - 4.0) < 1e-8, "value=" + str(v))
    # 量纲层自校验：作用量 / 时间 = 能量；作用量 / 动量 = 长度
    DIM_GUARD = (Fraction(-1), Fraction(3), Fraction(-2))
    dim_energy = ddiv(DIM_ACTION, D_T)
    ok_en = deq(dim_energy, (Fraction(1), Fraction(2), Fraction(-2)))
    ok_len = deq(ddiv(DIM_ACTION, DIM_MOMENTUM), D_L)
    expr_dim = ddiv(dmul(dpow(ddiv(D_L, D_T), 3), D_L), DIM_GUARD)
    ok_expr = deq(ddiv(DIM_ACTION, expr_dim), D_L)      # 差一个长度
    guard("tools_dim_algebra", ok_en and ok_len and ok_expr,
          "energy=" + dstr(dim_energy) + " action/momentum=" + dstr(ddiv(DIM_ACTION, DIM_MOMENTUM)) +
          " action/c3r_over_G=" + dstr(ddiv(DIM_ACTION, expr_dim)))
    g5 = abs(HBAR - HBAR_PUBLISHED) / HBAR < Decimal("1e-9")
    guard("tools_hbar_symbolic", g5, "rel=" + fm(abs(HBAR - HBAR_PUBLISHED) / HBAR))
    return True


# ================================================================== 报告输出
def dump_report():
    counts = {}
    for e in ENTRIES:
        counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
    for k in ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED", "MISMATCH"]:
        counts.setdefault(k, 0)

    payload = {
        "basename": BASENAME,
        "date": "2026-10-10",
        "round": "r25",
        "topic": "TUFT 空间光速螺旋：pi 螺旋本征值的几何推导（前段第一~六章 + §4~§9）",
        "entries": ENTRIES,
        "counts": counts,
        "guards": GUARDS,
        "guard_pass": sum(1 for g in GUARDS if g["ok"]),
        "guard_total": len(GUARDS),
        "key_numbers": {
            "theta0_minus_2pi_root_residual": "见 A1",
            "grid_step_1e-6_nearest_residual_to_2pi": "见 A3",
            "kappa_section5_over_correct_ratio": "见 C2",
            "omega_eq_c_kappa_relative_residual": "见 C3",
            "closed_curve_total_curvature_counterexample": "见 D2",
            "h_formula_dimension_defect": "见 F1",
        },
        "not_self_derived": {
            "Fenchel_total_curvature_theorem": "引自标准微分几何教科书结论（∮|kappa|ds>=2*pi，等号 iff 凸平面曲线），本册只做数值示例，不重推证明",
            "r20_minimal_closure_cost": "如需 T_mu_nu，最小闭合集代价 +2~4 个参数（[引用 r20]，本册不重算）",
        },
    }
    jpath = os.path.join(DATA_DIR, BASENAME + ".json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# " + BASENAME + " · 数据产物")
    lines.append("")
    lines.append("- 条目数：" + str(len(ENTRIES)))
    lines.append("- 自检：" + str(sum(1 for g in GUARDS if g["ok"])) + "/" + str(len(GUARDS)))
    lines.append("")
    lines.append("| 编号 | 判定 | 主张 | 机器证据 |")
    lines.append("| --- | --- | --- | --- |")
    for e in ENTRIES:
        ev = e["evidence"].replace("|", "\\|")
        cl = e["claim"].replace("|", "\\|")
        lines.append("| " + e["id"] + " | " + e["verdict"] + " | " + cl + " | " + ev[:400] + " |")
    lines.append("")
    lines.append("## 自检明细")
    lines.append("")
    for g in GUARDS:
        lines.append("- [" + ("OK" if g["ok"] else "NG") + "] " + g["name"] + " " + g["detail"])
    lines.append("")
    mpath = os.path.join(DATA_DIR, BASENAME + ".md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    rl = []
    rl.append(BASENAME + " 机器读数")
    rl.append("")
    rl.append("条目 " + str(len(ENTRIES)) + "：PASS=" + str(counts["PASS"]) +
              " FAIL=" + str(counts["FAIL"]) + " BOUNDARY=" + str(counts["BOUNDARY"]) +
              " INFO=" + str(counts["INFO"]) + " CORRECTED=" + str(counts["CORRECTED"]) +
              " MISMATCH=" + str(counts["MISMATCH"]))
    rl.append("自检 " + str(sum(1 for g in GUARDS if g["ok"])) + "/" + str(len(GUARDS)))
    rl.append("")
    for e in ENTRIES:
        rl.append("[" + e["id"] + "] " + e["verdict"] + " " + e["claim"])
        rl.append("    " + e["evidence"])
        if e["note"]:
            rl.append("    >> " + e["note"])
        rl.append("")
    rl.append("PASS = " + str(counts["PASS"]))
    rl.append("FAIL = " + str(counts["FAIL"]))
    rl.append("BOUNDARY = " + str(counts["BOUNDARY"]))
    rl.append("INFO = " + str(counts["INFO"]))
    tpath = os.path.join(DATA_DIR, BASENAME + "_report.txt")
    with open(tpath, "w", encoding="utf-8") as f:
        f.write("\n".join(rl))

    print("\n".join(rl))
    print("")
    print("自检 " + str(sum(1 for g in GUARDS if g["ok"])) + "/" + str(len(GUARDS)))
    for g in GUARDS:
        if not g["ok"]:
            print("  [NG] " + g["name"] + " " + g["detail"])
    return payload


def main():
    section_A()
    section_B()
    section_C()
    section_D()
    section_E()
    section_F()
    section_G()
    selfcheck()
    dump_report()
    bad = [g for g in GUARDS if not g["ok"]]
    if bad:
        print("SELFCHECK_FAILED count=" + str(len(bad)))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

