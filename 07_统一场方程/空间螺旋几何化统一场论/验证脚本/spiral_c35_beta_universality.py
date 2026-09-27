# -*- coding: utf-8 -*-
"""C35 追加：金星 + 地球轨道进动交叉验证，检验 β 普适性（标准库 math，双精度）

用户下达的问题
--------------
「C35：金星 + 地球轨道进动交叉验证，检验 β 普适性」。

本轮要回答的不是「β 对不对」，而是**这个交叉验证在仓库现有的数据下能不能做**，
以及**它的判决力活在哪一条轴上**。三件事在代码里钉死：

1. **β 在任何跨行星比值里精确约掉。** 只要律对 β **可分离**（f(β,a)=g(β)·h(a)，
   几次幂都行）且两端共用同一个 β，比值里就约掉——线性只是它的特例（牙齿检验
   实测：把草稿式改成 β² 时 [Q4] 仍绿，真正被检验的是"两端同一个 β"这件事）。
   所以「用金星/地球检验 β」检验的**不是 β 的数值**（那已由水星标定吃掉），
   而是几何项对 a 的**幂次**。⇒「β 普适性」的可检验内核是一个 SHAPE 检验。
2. **仓库里没有金星/地球的观测残差。** 原脚本自己标注：
   `源码/空间螺旋修复版_第一性审计与伪派生判定.py:1362` 一带的参考值
   水星 43.03 是标定靶，金星 8.62 / 地球 3.84 是「GR 预言值（非独立观测残差）」。
   本脚本把这句话变成机器读数：[Q6] 判「把 8.62/3.84 当观测」是否循环。
3. **判决力低于仓库自身的噪声。** 仓库里水星的三个锚点互差 0.13 角秒每世纪
   （42.98 / 43.03 / 43.11，出处见 ANCHORS），而两条候选式在金星处的**差**
   只有 ~2.3e-3 角秒每世纪 ⇒ 信号/噪声 ~1/57。[Q7] 把这条比值算出来。

数据出处（全部为仓库内文件，脚本内不引入外部数据）
--------------------------------------------------
* 行星轨道元 a、e、T 与两条候选几何式：
  `04_公共成果/算法联盟_全维自洽与归一化/源码/空间螺旋修复版_第一性审计与伪派生判定.py:1335-1337`
  （§13-C35，草稿式 `planet_dphi` 与 Binet 一阶式 `dphi_geo_correct`）
* c、G、M_sun：同文件 1362-1368 行（G=6.67430e-11 CODATA2018、M_sun=1.98847e30）
* 250 位对账锚点（水星/金星/地球 GR 基础项）：
  `04_公共成果/算法联盟_全维自洽与归一化/数据/空间螺旋V21续修_C25C35_审计.md:14`
* 水星观测锚点：`02_共享基础/经典基准/经典实验基准/E0_水星近日点进动/README.md:7,9`（42.98）、
  `03_跨体系研究/物理领域/天体作用力/verify_celestial_forces.py:122`（43.11±0.21）、
  标定靶 43.03（上面 §13-C35 脚本 1335 行）

红线
----
* 「判据 PASS」只说明本仪器算对了，**不说明 β 普适性成立**。物理侧结论见 [Q9]：OPEN。
* 本脚本不改 `claims.csv` 里 C35 的 status（那是台账的活）。
* 只用标准库 `math`（本目录 README §1 红线：不引入 sympy / mpmath）。
  与 250 位版面的是非由 [Q1] 的双路对账判定，不由位数判定。
* 退出码默认恒为 0（本目录约定）；加 `--strict` 时任何内部判据 FAIL 则退出码 1。
* 每条判据的"牙齿"由同目录 `spiral_c35_beta_teeth.py` 检验（种缺陷要求按名字变红，
  该驱动自己打印 CAUGHT/MISSED 与判据覆盖率；它不产物理读数，故不进版面）。

运行：python spiral_c35_beta_universality.py [--h 0.0005] [--strict]
"""

import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- 常数（出处见头注）
C = 299792458.0                      # m/s，精确定义
G = 6.67430e-11                      # m^3 kg^-1 s^-2（CODATA 2018，草稿指定）
MSUN = 1.98847e30                    # kg（草稿指定）
GM = G * MSUN                        # m^3/s^2
ARCSEC = math.pi / (180.0 * 3600.0)  # 角秒 -> 弧度
JULIAN_YR = 365.25 * 86400.0         # 儒略年，定义值（非测量）
MU_SUN = 3.0 * GM / (C * C)          # GR 的 β（米）：Binet u''+u=A+βu² 里 β=3GM/c²
EPS = sys.float_info.epsilon         # 双精度机器 epsilon：[4] 的"约掉"判据地板
G_SIG, MSUN_SIG = 6, 6               # G、MSUN 两行的字面有效数字位数（[8] 的误差棒用）

# 行星元：a [m]、e、T [年]、仓库内的"参考值"[角秒/百年]
PLANETS = [
    ('水星', 5.790905e10, 0.20563069, 0.240846, 43.03),
    ('金星', 1.0820893e11, 0.00677672, 0.615197, 8.62),
    ('地球', 1.4959787e11, 0.0167086, 1.000017, 3.84),
]
# 上表字面的**书写精度**（数出来的，不是外部目录的标称误差）：
# (a 的有效数字位数, e 的小数位, T 的小数位, 参考值的小数位)
ELEMENT_DIGITS = {
    '水星': (7, 8, 6, 2),      # 5.790905e10 / 0.20563069 / 0.240846 / 43.03
    '金星': (8, 8, 6, 2),      # 1.0820893e11 / 0.00677672 / 0.615197 / 8.62
    '地球': (8, 7, 6, 2),      # 1.4959787e11 / 0.0167086 / 1.000017 / 3.84
}
# 250 位版面给出的 GR 基础项（角秒/百年），用于跨仪器对账
GR250 = {'水星': 42.98203636043861, '金星': 8.624863899085765, '地球': 3.8388229840403927}
# 仓库内水星的三个锚点（含标定靶）；[Q7] 的"噪声代理"就是它们之间的极差
MERCURY_ANCHORS = [('E0_水星近日点进动/README.md:7,9', 42.98),
                   ('空间螺旋修复版_第一性审计与伪派生判定.py:1335', 43.03),
                   ('verify_celestial_forces.py:122', 43.11)]

JUDGE = []


def rec(sid, title, verdict, detail):
    JUDGE.append({'id': sid, 'title': title, 'verdict': verdict, 'detail': detail})
    print('  [%-8s] %-9s %s' % (verdict, sid, title))
    print('            %s' % detail)
    return verdict == 'PASS'


def judge(sid, title, ok, detail):
    return rec(sid, title, 'PASS' if ok else 'FAIL', detail)


def semilatus(a, e):
    """p = a(1-e^2)：Binet 式里的半通径，进动只通过 p 依赖轨道元。"""
    return a * (1.0 - e * e)


def dphi_gr_per_orbit(a, e):
    """GR 一阶每圈进动（弧度）：6πGM/(c² p) = 2π·β_GR/p，β_GR = 3GM/c²。"""
    return 2.0 * math.pi * MU_SUN / semilatus(a, e)


def per_century(per_orbit, T_yr):
    """弧度/圈 -> 角秒/百年。两条独立换算路（[Q2] 用开普勒第三定律复核 T）。"""
    return per_orbit * (100.0 / T_yr) / ARCSEC


def law_binet(beta, a, e):
    """Binet 一阶式（草稿自身方程 u''+u=GM/h²+(GMβ/h²)u² 的正确积分）：
    Δφ = 2πβ/p²，弧度/圈。β 的量纲在这里是 m²。"""
    return 2.0 * math.pi * beta / semilatus(a, e) ** 2


def law_draft(beta, a, e):
    """草稿式（被 §13-C35-3 判 FAIL 的那一条）：Δφ = 3πβ·GM/(c² a³(1-e²)²)，弧度/圈。"""
    return 3.0 * math.pi * beta * GM / (C * C * a ** 3 * (1.0 - e * e) ** 2)


def per_century_of(law, beta, a, e, T_yr):
    return per_century(law(beta, a, e), T_yr)


def kepler_T_yr(a):
    """开普勒第三定律独立复算周期（年）：T = 2π sqrt(a^3/GM) / 儒略年。"""
    return 2.0 * math.pi * math.sqrt(a ** 3 / GM) / JULIAN_YR


def rk4_dphi(a, e, eps, h):
    """数值积分 Binet 方程 u'' + u = A + eps·u²，返回每圈进动（弧度）。

    A = 1/p，初值取未扰轨道的近星点 u=A(1+e)、u'=0。进动 = 下一次 u' 由正变零
    （u 的极大）相对 2π 的偏移。eps=0 的同一次积分作为**本底**一起返回：
    数值色散与步长偏差全在相减里抵消，这样 [Q3] 测的是物理而不是求根器。

    φ 一律由 `圈数 × h` 乘出来，不做 `phi += h` 累加。这条**不是**本底来源：
    牙齿检验实测两种写法在 h=5e-4 下把 [3] 的每一个读数打印得逐位相同，
    即累加舍入在本仪器里低于打印精度；保留乘式只因为它让 φ 成为 h 的确定性
    倍数。真正的本底来自 u' 的逐步舍入（∝ √(1/h)，网格越细越大，见 [Q3b]）。
    """
    A = 1.0 / semilatus(a, e)

    def integrate(eps_loc, h_loc):
        def rhs(u, up):
            return (up, A + eps_loc * u * u - u)

        u, up = A * (1.0 + e), 0.0
        step = 0
        phi = 0.0
        prev = None
        while phi < 2.0 * math.pi + 0.5:
            k1u, k1p = rhs(u, up)
            k2u, k2p = rhs(u + 0.5 * h_loc * k1u, up + 0.5 * h_loc * k1p)
            k3u, k3p = rhs(u + 0.5 * h_loc * k2u, up + 0.5 * h_loc * k2p)
            k4u, k4p = rhs(u + h_loc * k3u, up + h_loc * k3p)
            un = u + h_loc / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
            upn = up + h_loc / 6.0 * (k1p + 2 * k2p + 2 * k3p + k4p)
            phin = (step + 1) * h_loc
            if prev is not None and prev[1] > 0.0 and upn <= 0.0 and phi > math.pi:
                # u' 由正转负：把上一步的端点当根的左界，二分细化到 φ 的 ULP 以下
                lo_u, lo_up = prev[0], prev[1]
                lo_phi = phi
                for _ in range(60):
                    mid = 0.5 * (lo_phi + phin)
                    # 从 lo 点重积分半步（RK4 半步足够精细）
                    hh = mid - lo_phi
                    k1 = rhs(lo_u, lo_up)
                    k2 = rhs(lo_u + 0.5 * hh * k1[0], lo_up + 0.5 * hh * k1[1])
                    k3 = rhs(lo_u + 0.5 * hh * k2[0], lo_up + 0.5 * hh * k2[1])
                    k4 = rhs(lo_u + hh * k3[0], lo_up + hh * k3[1])
                    um = lo_u + hh / 6.0 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
                    upm = lo_up + hh / 6.0 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
                    if upm > 0.0:
                        lo_phi, lo_u, lo_up = mid, um, upm
                    else:
                        phin = mid
                return lo_phi
            prev = (un, upn)
            step += 1
            u, up, phi = un, upn, phin
        return float('nan')

    phi_grav = integrate(eps, h)
    phi_flat = integrate(0.0, h)
    return (phi_grav - phi_flat)


def rk4_dphi_probe(a, e, eps, h, coarse):
    """在 4 个网格上跑同一条路：coarse、h、h/2、h/4。

    返回 (最细网格值 v, d1=|v(h)-v(h/2)|, d2=|v(h/2)-v(h/4)|, spread, q)。
    spread = 四个值里的极差 = 本仪器的**实测本底**（含与 h 无关的那部分）。
    q = min(d1,d2)/max(d1,d2)：若误差真由 h⁴ 截断支配，相邻两级之差要按 16 倍
    衰减 ⇒ q≈1/16；q 明显大于 1/16 就说明"细化网格没在收敛"，即本底是舍入随机
    漫步（步数 ∝ 1/h ⇒ 越细越大），Richardson 棒在这种本底上系统性偏小。
    """
    vs = [rk4_dphi(a, e, eps, coarse)]
    vs += [rk4_dphi(a, e, eps, h / float(2 ** i)) for i in range(3)]
    d1, d2 = abs(vs[1] - vs[2]), abs(vs[2] - vs[3])
    hi = max(d1, d2)
    q = 1.0 if hi == 0.0 else min(d1, d2) / hi
    return vs[-1], d1, d2, max(vs) - min(vs), q


def second_order_term(eps, a, e):
    """一阶律 Δφ=2πx 被舍掉的下一阶项 = 5πx²，x = eps/p。推导如下（本轮独立做一遍）：

    u''+u = A + eps·u²，圆轨道半径 u0 满足 u0 = A + eps·u0² ⇒ u0 = A + eps·A² + O(eps²)。
    令 u = u0 + δ：δ'' + (1 - 2·eps·u0)δ = eps·δ²，且 δ' = 0 的解恰好落在
    τ = nπ（把 δ 展开到 O(eps) 后 δ' = -aω sinθ·[1 - (2eps·a/(3ω²))cosθ]，
    方括号项对小的 eps·a 不改根的位置）⇒ 近星点到近星点的相位 = 2π/ω。
    ω² = 1 - 2eps·u0 = 1 - 2x - 2x²，故
        Δφ = 2π[(1-2x-2x²)^(-1/2) - 1] = 2π[x + 2.5x² + O(x³)] = 2πx + 5πx²。
    关键在 u0 的那位移：只按 ω²=1-2x 展开会得到 3πx²，**少了一项 2πx²**。
    [Q3c] 用 eps×16 的实测把这两个候选分开。
    """
    x = eps / semilatus(a, e)
    return 5.0 * math.pi * x * x


# 本底用的 eps：小到 2π·eps/p ≈ 1e-22 弧度。**它测不出本底**（本轮实测：返回恰好
# 0.0，因为右端按 `A + eps*u*u - u` 求值时 eps·u² 在加法里就被舍掉了）——
# 这条只作打印用的反面教材，不当判据。
EPS_NULL = 1.0e-12
# 极差本底要跨足够宽的网格族才作数：coarse 这一点几乎不要钱。
# 但**本底的数值随这一点而变**（牙齿检验 pc1 实测：0.02→0.05 时 [3] 的极差与容差
# 都移动，而 13 条判决一条不动）⇒ 引用任何一条容差，必须把 H_COARSE 一起报出。
H_COARSE = 0.02
# eps 放大倍数：一阶项放大 C 倍、二阶项放大 C² 倍 ⇒ 用 (v(C)-C·v(1))/(C²-C) 解 B。
C_SECOND = 16.0


def rel_ulp_sig(sig_digits):
    """一个给到 d 位**有效数字**的数，±0.5 末位对应的相对不确定度 = 0.5·10^(1-d)。

    不能按"小数点后几位"算：a 是 1e11 量级，按小数位算会得到 1e-17 这种荒谬值，
    等于把表格的取整精度当成无限精度。
    """
    return 0.5 * 10.0 ** (1.0 - sig_digits)


def abs_ulp_dec(decimals):
    """一个给到小数点后 k 位的数，±0.5 末位对应的**绝对**不确定度。"""
    return 0.5 * 10.0 ** (-decimals)


def max_abs_rel_drift(vals):
    """同一比值在 β 缩放 λ 下的最大相对漂移 = 极差 / 量级。

    分母取 |值| 的最大者而不是均值：这里要的是"漂移有没有超出双精度舍入"，
    与比值本身的大小无关。
    """
    scale = max(abs(v) for v in vals)
    if scale == 0.0:
        return 0.0
    return (max(vals) - min(vals)) / scale


def json_finite(o, bag):
    """版面必须是**严格** JSON：`NaN` / `Infinity` 是 Python 的扩展，jq 与 JS 的
    `JSON.parse` 会因为它们打不开整份文件（C25 那一轮就因此写崩过一次版面）。
    非有限浮点一律写成 null，并把原值记进 bag——null 也要能被追问是谁写的。
    """
    if isinstance(o, float):
        if math.isfinite(o):
            return o
        bag.append(o)
        return None
    if isinstance(o, dict):
        return dict((k, json_finite(v, bag)) for k, v in o.items())
    if isinstance(o, (list, tuple)):
        return [json_finite(v, bag) for v in o]
    return o


def main(argv):
    strict = '--strict' in argv
    h = 5e-4
    for i, a in enumerate(argv):
        if a == '--h':
            h = float(argv[i + 1])
    print('=' * 78)
    print('C35 追加：水星标定 -> 金星/地球交叉验证，检验 β 普适性（标准库 math，双精度）')
    print('=' * 78)
    print('GM_sun=%r m^3/s^2；β_GR=3GM/c^2=%r m；1 角秒=%r rad' % (GM, MU_SUN, ARCSEC))

    # ---- 1) GR 基础项：双精度复算 vs 仓库 250 位版面 ----
    print('\n[1] GR 基础项（每圈 2πβ_GR/p，角秒/百年）与 250 位版面对账')
    gr_pc = {}
    for name, a, e, T, ref in PLANETS:
        gr_pc[name] = per_century(dphi_gr_per_orbit(a, e), T)
        ok = abs(gr_pc[name] - GR250[name]) / GR250[name] < 1e-11
        judge('Q1-%s' % name, '%s：双精度 6πGM/(c²p)·(100/T) 与 250 位版面逐位一致（<1e-11）' % name,
              ok, '本轮 %r vs 版面 %r（相对差 %r）'
                  % (gr_pc[name], GR250[name], abs(gr_pc[name] - GR250[name]) / GR250[name]))

    # ---- 2) 轨道元自洽：T 与 a 是否互相支撑（开普勒第三定律，独立一条路）----
    print('\n[2] 轨道元表自洽性：T(表) vs 2π√(a³/GM)（儒略年定义换算）')
    kep = []
    for name, a, e, T, ref in PLANETS:
        Tk = kepler_T_yr(a)
        dev = abs(Tk - T) / T
        kep.append((name, T, Tk, dev))
        print('  %-3s T_表=%-12r T_开普勒=%-14r 相对偏差=%r' % (name, T, Tk, dev))
    worst_kep = max(kep, key=lambda t: t[3])
    judge('Q2', 'a 与 T 互相支撑（开普勒第三定律）⇒ 进动公式里 a、T 不是两个独立自由度',
          worst_kep[3] < 5e-3, '最大偏差在 %s：%r（地球 T 含回归年/儒略年口径差，水星金星为历表取整）'
                               % (worst_kep[0], worst_kep[3]))

    # ---- 3) 数值积分 vs 闭式：进动公式本身要能被 RK4 打破 ----
    print('\n[3] Binet 方程 RK4 数值积分 vs 闭式 Δφ=2π·eps/p（eps=β_GR 与 eps=β/p 两例）')
    # 先按水星标定两条候选式的 β（几何项 = 43.03 - GR_水星 角秒/百年）
    geo_target = 43.03 - gr_pc['水星']
    a0, e0, T0 = PLANETS[0][1], PLANETS[0][2], PLANETS[0][3]
    beta_binet = geo_target / per_century_of(law_binet, 1.0, a0, e0, T0)
    beta_draft = geo_target / per_century_of(law_draft, 1.0, a0, e0, T0)
    print('  几何项标定靶（水星，角秒/百年）= %r' % geo_target)
    print('  β(Binet 一阶式, m²) = %r；β(草稿式) = %r；比值 = %r'
          % (beta_binet, beta_draft, beta_draft / beta_binet))
    # 反面教材先放这里：想用一个"零信号"跑本来定本底，得到的会是 0.0——那不是准，
    # 是信号在右端求值时就被舍掉了。本底只能用**有限信号**跨网格的极差来定。
    v_null = rk4_dphi_probe(a0, e0, EPS_NULL, h, H_COARSE)[0]
    print('  反面教材：eps=%r 的空实测返回恰好 %r（真信号 2π·eps/p=%r）——'
          'εu² 在 `A + eps*u*u` 这一步就被舍掉 ⇒ 零信号测不出本底，只能实测极差'
          % (EPS_NULL, v_null, 2.0 * math.pi * EPS_NULL / semilatus(a0, e0)))
    num_cases = []
    for label, eps, closed in (
            ('GR（eps=3GM/c²）', MU_SUN, dphi_gr_per_orbit(a0, e0)),
            ('Binet 一阶（eps=β/p，水星标定 β）', beta_binet / semilatus(a0, e0),
             law_binet(beta_binet, a0, e0))):
        num, d1, d2, spread, q = rk4_dphi_probe(a0, e0, eps, h, H_COARSE)
        resid = abs(num - closed)
        sec = second_order_term(eps, a0, e0)
        tol = sec + 3.0 * spread
        vC, _d1c, _d2c, spread_c, _qc = rk4_dphi_probe(a0, e0, C_SECOND * eps, h, H_COARSE)
        b_meas = (vC - C_SECOND * num) / (C_SECOND * C_SECOND - C_SECOND)
        b_bar = (C_SECOND * spread + spread_c) / (C_SECOND * C_SECOND - C_SECOND)
        num_cases.append((label, num, closed, resid, resid / abs(closed),
                          d1, d2, spread, q, sec, tol, b_meas, b_bar))
        print('  %-34s RK4(h/4)=%r 闭式=%r' % (label, num, closed))
        print('  %-34s 绝对残差=%r 相对=%r｜4 网格极差(本底)=%r、d1=%r d2=%r ⇒ q=%r'
              % ('', resid, resid / abs(closed), spread, d1, d2, q))
        print('  %-34s 容差 = 5πx²=%r + 3·本底=%r ⇒ %r；残差/容差 = %r'
              % ('', sec, 3.0 * spread, tol, resid / tol))
    worst_num = max(num_cases, key=lambda t: t[3] / t[10])
    judge('Q3', 'RK4 数值积分复现一阶闭式：两例残差都落在**逐项推导**的容差'
                '（该例一阶律被舍掉的 5πx² 项 + 3×跨 4 网格实测本底）之内'
                '⇒ 进动公式不是抄来的，是这条 ODE 的解',
          all(t[3] < t[10] for t in num_cases),
          '最紧例「%s」残差 %r < 容差 %r（比 %r，越接近 1 越说明容差在咬）；'
          'h=%r→%r 四档，eps=0 同批积分作本底相减'
          % (worst_num[0], worst_num[3], worst_num[10], worst_num[3] / worst_num[10],
             H_COARSE, h / 4.0))
    judge('Q3b', '两例的相邻网格差比 q=%r/%r 都**大于** h⁴ 截断要求的 1/16=%r'
                 '⇒ 本底是舍入随机漫步（步数 ∝ 1/h，网格越细本底越大），不是截断项；'
                 'Richardson 的 2^p 外推在这种本底下系统性偏小，所以 [Q3] 的容差用极差。'
                 '这条是**示警判据**：它哪天变红，说明本底被修掉了，容差该换回外推。'
          % (num_cases[0][8], num_cases[1][8], 1.0 / 16.0),
          all(t[8] > 1.0 / 16.0 for t in num_cases),
          'q(GR)=%r、q(弱信号)=%r；d1/d2 分别 %r、%r（截断支配时应为 16）。'
          '这条**只对当前网格族**作数：同一份代码加 `--h 0.002` 重跑，某一级相邻差'
          '会恰好为 0 ⇒ q=0 ⇒ 本条变红而 [Q3]/[Q3c] 仍绿（牙齿检验实测），'
          '所以它读的是"这一档网格上有没有反收敛"，不是普适的收敛性结论。'
          % (num_cases[0][8], num_cases[1][8],
             num_cases[0][5] / max(num_cases[0][6], 1e-300),
             num_cases[1][5] / max(num_cases[1][6], 1e-300)))
    b_meas, b_bar, b5 = num_cases[0][11], num_cases[0][12], num_cases[0][9]
    b_naive = b5 * 3.0 / 5.0        # 只按 ω²=1-2x 展开（漏掉圆半径 u0=A+eps·A² 的位移）
    dev5 = abs(b_meas - b5) / b_bar
    dev3 = abs(b_meas - b_naive) / b_bar
    print('  二阶系数实测（eps×%r 反解）：B=%r ±%r；5πx²=%r（偏 %r 棒）、3πx²=%r（偏 %r 棒）'
          % (C_SECOND, b_meas, b_bar, b5, dev5, b_naive, dev3))
    judge('Q3c', 'ODE 自己的二阶项能被这条数值路**钉出系数**：B=%r 与推导值 5πx²=%r 只差'
                 '%r 个实测棒（<4），而漏掉圆半径位移的 3πx²=%r 差 %r 个棒（>4）'
                 '⇒ [Q3] 容差里的物理项不是拟合出来的系数，是被独立复现的量'
          % (b_meas, b5, dev5, b_naive, dev3),
          dev5 < 4.0 and dev3 > 4.0,
          '棒 b_bar=(%r·本底(GR)+本底(×%r))/240=%r；eps×%r 后 x=%r 仍 ≪1，三阶项可忽略。'
          '两例残差的绝对值 %r vs %r 看着接近，主导源不同（GR 例含 5πx²=%r，'
          '弱信号例该项 %r 可忽略、残差是本底）⇒ 不读成同源结论。'
          % (C_SECOND, C_SECOND, b_bar, C_SECOND,
             C_SECOND * MU_SUN / semilatus(a0, e0),
             num_cases[0][3], num_cases[1][3], num_cases[0][9], num_cases[1][9]))
    print('  ⇒ 同一个绝对本底折成相对差要放大 %r 倍（两例闭式信号之比）：信号越弱，'
          '实测列越不可信，闭式是唯一可引用的读数（与 C25 同一课）。'
          % (num_cases[0][2] / num_cases[1][2]))

    # ---- 4) β 在跨行星比值里精确约掉：可检验内核是幂次，不是数值 ----
    print('\n[4] β 普适性的可检验内核：跨行星比值对 β 的耦合（三条 λ 缩放）')
    inv_ratio = {}
    for name, a, e, T, ref in PLANETS[1:]:
        vb_vals, vd_vals = [], []
        for lam in (0.4, 1.0, 1.7, 10.0):
            vb_vals.append(per_century_of(law_binet, lam * beta_binet, a, e, T) /
                           per_century_of(law_binet, lam * beta_binet, a0, e0, T0))
            vd_vals.append(per_century_of(law_draft, lam * beta_draft, a, e, T) /
                           per_century_of(law_draft, lam * beta_draft, a0, e0, T0))
        drift = max(max_abs_rel_drift(vb_vals), max_abs_rel_drift(vd_vals))
        inv_ratio[name] = (vb_vals[0], vd_vals[0], drift)
        print('  %-3s β 缩放 0.4/1.0/1.7/10 下：binet 律比值=%r draft 律比值=%r 最大相对漂移=%r'
              % (name, vb_vals[0], vd_vals[0], drift))
    worst_drift = max(v[2] for v in inv_ratio.values())
    # 四条 λ 各算一次比值，律内部乘除次数 <20 ⇒ 64·eps 是"纯舍入"的宽松上限
    drift_floor = 64.0 * EPS
    judge('Q4', '把 β 乘 0.4/1.0/1.7/10 之后，金星/地球对水星的几何项比值不随 λ 动'
                '（最大相对漂移 < 64·eps = %r，双精度内即"约掉"）⇒ β 普适性检验的载荷'
                '不是 β 的大小，是 a 的幂次' % drift_floor,
          worst_drift < drift_floor,
          '最大相对漂移 = %r（地板 %r）；比值本身：金星 binet=%r draft=%r，地球 binet=%r draft=%r'
          % (worst_drift, drift_floor, inv_ratio['金星'][0], inv_ratio['金星'][1],
             inv_ratio['地球'][0], inv_ratio['地球'][1]))
    print('  注：这不是"恒等式所以无信息"。它说明的是——任何只用水星标定 β 的方案，'
          '在跨行星比值上自动失去对 β 的敏感度；能失去的敏感度只剩 a 的幂次。')
    print('  负空间（[Q4] 看不见什么）：约掉的条件只是"两端共用同一个 β"，与该 β 的'
          '幂次无关——牙齿检验实测把草稿式改成 β² 时本条仍绿。真正的反命题是'
          '"两端不是同一个 β"，那条缺陷能红（把 λ 只乘比值的一端 ⇒ 本条红）。')

    # ---- 5) 两条候选式给出不同的金星/地球预言：幂次差 = a_M/a_p 的精确结构 ----
    print('\n[5] 同一水星标定下，两条几何式在金星/地球的预言差（§13-C35-3 的独立复现）')
    law_tab = []
    for name, a, e, T, ref in PLANETS:
        vb = per_century_of(law_binet, beta_binet, a, e, T)
        vd = per_century_of(law_draft, beta_draft, a, e, T)
        struct_pred = PLANETS[0][1] / a          # 结构预期：两式之比 = a_水星/a_行星，与 e 无关
        law_tab.append((name, vb, vd, vd / vb, struct_pred))
        print('  %-3s Binet 一阶=%r 草稿式=%r 草稿/Binet=%r 结构预期 a_水星/a=%r'
              % (name, vb, vd, vd / vb, struct_pred))
    struct = [(t[3] - t[4]) / t[4] for t in law_tab[1:]]
    judge('Q5', '草稿/Binet 的跨行星比 == a_水星/a_行星（相对偏差 <1e-12）⇒ 两式只差一个 1/a，'
                '与 §13-C35-3 记的 0.535×/0.387× 同源',
          max(abs(s) for s in struct) < 1e-12,
          '金星 %r、地球 %r（相对偏差）；水星自身恒为 1（标定条件）' % tuple(struct))
    venus_gap = abs(law_tab[1][1] - law_tab[1][2])
    earth_gap = abs(law_tab[2][1] - law_tab[2][2])
    print('  两式在金星/地球的**绝对差**（角秒/百年）= %r / %r' % (venus_gap, earth_gap))

    # ---- 6) 循环性守卫：仓库里的"金星/地球参考值"是不是观测 ----
    print('\n[6] 观测量侧：仓库里的参考值能否充当独立观测（循环性检查）')
    circular = []
    for name, a, e, T, ref in PLANETS[1:]:
        rel = abs(ref - gr_pc[name]) / gr_pc[name]
        circular.append((name, ref, gr_pc[name], rel))
        print('  %-3s 参考值=%r vs 本轮 GR 预言=%r 相对差=%r ⇒ %s'
              % (name, ref, gr_pc[name], rel,
                 '参考值就是预言本身（取整），不可作观测量' if rel < 0.01 else '可能是独立观测'))
    mer_rel = abs(PLANETS[0][4] - gr_pc['水星']) / gr_pc['水星']
    judge('Q6', '金星/地球的仓库参考值与 GR 预言之差 <1%%（8.62/3.84 是预言的取整），'
                '而水星的 43.03 与 GR 基础项差 %r%% ⇒ 只有水星是"待解释的数"，'
                '金星/地球在本仓库**没有观测侧**' % (100.0 * mer_rel),
          all(t[3] < 0.01 for t in circular) and mer_rel > 0.0005,
          '金星相对差 %r、地球相对差 %r、水星相对差 %r'
          % (circular[0][3], circular[1][3], mer_rel))

    # ---- 7) 判决力：信号 vs 仓库自身的锚点极差 ----
    print('\n[7] 判决力 = 两式之差 / 仓库内水星锚点极差（噪声代理，出处见头注）')
    vals = [v for _src, v in MERCURY_ANCHORS]
    spread_mer = max(vals) - min(vals)
    power_v = venus_gap / spread_mer
    power_e = earth_gap / spread_mer
    for src, v in MERCURY_ANCHORS:
        print('  锚点 %-52r = %r' % (src, v))
    print('  极差 = %r 角秒/百年；信号/噪声：金星 %r、地球 %r' % (spread_mer, power_v, power_e))
    judge('Q7', '即便补齐金星/地球的观测残差，仓库自身的水星锚点极差（%r）已把两式之差'
                '（%r/%r）压到噪声之下：判决力 %r/%r << 1 ⇒ 本仪器**测不出**幂次之争'
                % (spread_mer, venus_gap, earth_gap, power_v, power_e),
          power_v < 0.1 and power_e < 0.1,
          '金星判决力 %r（=1/%r）、地球 %r（=1/%r）；注意锚点极差无统一出处，'
          '这一条只是**量级**判据' % (power_v, 1.0 / power_v, power_e, 1.0 / power_e))

    # ---- 8) 理论侧误差棒：三条腿分别算，再与 [7] 的观测噪声比大小 ----
    print('\n[8] 理论侧误差棒（把字面书写精度当 ±0.5 末位传播；进动只通过 p、T 依赖轨道元）')
    orbit_bars = []
    for name, a, e, T, ref in PLANETS:
        da, de_dec, dT_dec, _dref = ELEMENT_DIGITS[name]
        rel_a = rel_ulp_sig(da)                            # a 用有效数字口径
        rel_p = math.hypot(rel_a, 2.0 * e * abs_ulp_dec(de_dec) / (1.0 - e * e))
        rel_T = abs_ulp_dec(dT_dec) / T                    # T 用小数位口径再折成相对
        rel_orbit = math.hypot(rel_p, rel_T)               # Δφ_百年 ∝ 1/(p·T)
        orbit_bars.append((name, rel_orbit, gr_pc[name] * rel_orbit))
        print('  轨道元腿 %-3s 相对 %r ⇒ 绝对 %r 角秒/百年（a %d 位、e %d 位小数、T %d 位小数）'
              % (name, rel_orbit, orbit_bars[-1][2], da, de_dec, dT_dec))
    worst_orbit = max(orbit_bars, key=lambda t: t[1])
    da_mer, de_mer, dT_mer, _ = ELEMENT_DIGITS['水星']
    leg_T = abs_ulp_dec(dT_mer) / PLANETS[0][3]
    leg_a = rel_ulp_sig(da_mer)
    judge('Q8a', '轨道元字面末位传播到 GR 基础项上最大相对 %r（绝对 %r 角秒/百年，在 %s）'
                 '<1e-4 ⇒ 轨道元这条腿不是瓶颈' % (worst_orbit[1], worst_orbit[2], worst_orbit[0]),
          worst_orbit[1] < 1e-4,
          '水星相对 %r、金星 %r、地球 %r；水星这一行里 T 腿 %r 是 a 腿 %r 的 %r 倍'
          '（a 按有效数字口径、T 只给到 6 位小数）'
          % (orbit_bars[0][1], orbit_bars[1][1], orbit_bars[2][1], leg_T, leg_a, leg_T / leg_a))
    # 几何项 = 43.03 − GR_水星 是**两个数之差** ⇒ 它的误差棒由三条腿合成：
    #   ① 标定靶末位（43.03 只到 2 位小数）② GR 常数腿（G、M_sun 各 6 位）③ 轨道元腿(水星)
    d_anchor = abs_ulp_dec(ELEMENT_DIGITS['水星'][3])
    rel_const = math.hypot(rel_ulp_sig(G_SIG), rel_ulp_sig(MSUN_SIG))
    bar_const = gr_pc['水星'] * rel_const
    bar_orbit_mer = gr_pc['水星'] * orbit_bars[0][1]
    bar_geo = math.hypot(d_anchor, bar_const, bar_orbit_mer)
    rel_geo = bar_geo / geo_target
    legs = max((('标定靶末位', d_anchor), ('常数腿', bar_const), ('轨道元腿', bar_orbit_mer)),
               key=lambda t: t[1])
    print('  几何项 %r = 43.03 − %r 的三条腿：靶末位 ±%r、常数腿 ±%r、轨道元腿 ±%r'
          % (geo_target, gr_pc['水星'], d_anchor, bar_const, bar_orbit_mer))
    print('  ⇒ 合成 ±%r（相对 %r），主导腿 = %s；c 是定义值、儒略年是定义值，不贡献' % (bar_geo, rel_geo, legs[0]))
    bar_v = venus_gap * rel_geo
    bar_e = earth_gap * rel_geo
    judge('Q8b', '把 %r 的相对棒乘到两式之差上：金星 ±%r、地球 ±%r，均比 [7] 的观测噪声代理 '
                 '%r 小一个量级以上 ⇒ 理论侧误差棒**不是**幂次之争的瓶颈，瓶颈在观测侧（[6]/[7]）'
                 % (rel_geo, bar_v, bar_e, spread_mer),
          bar_v < spread_mer / 10.0 and bar_e < spread_mer / 10.0,
          '金星棒/噪声 %r、地球棒/噪声 %r；主导腿 %s 占合成棒的 %r'
          % (bar_v / spread_mer, bar_e / spread_mer, legs[0], legs[1] / bar_geo))

    # ---- 9) 物理侧结论（不进 PASS 计数）----
    print('\n[9] 物理侧结论')
    rec('Q9-status', '金星+地球交叉验证「检验 β 普适性」当前不可执行', 'OPEN',
        'β 普适性可检验的内核是几何项的 a 幂次（[Q4]），而本仓库：'
        '①金星/地球无观测残差（[Q6]，参考值即预言）；②两式之差在水星锚点极差之下（[Q7]）；'
        '③β 本身无第一性来源（承接 §13-C35-2 BOUNDARY）。⇒ 本轮把 C35 从「框架就绪」'
        '推进到「**判决力已被定量定位**：要分辨幂次之争，历表残差的噪声得压到两式之差之下，'
        '即金星 %r / 地球 %r 角秒每百年（[Q5] 绝对差），而仓库水星锚点极差是 %r（[Q7]），'
        '差 %r 倍 / %r 倍；此外还要 β 的第一性式」，不升等级。'
        % (venus_gap, earth_gap, spread_mer, spread_mer / venus_gap, spread_mer / earth_gap))
    rec('Q9-mutual', '两条候选几何式互斥（复现 §13-C35-3 的 FAIL）', 'BOUNDARY',
        '同一水星标定下，金星几何项 Binet 一阶=%r vs 草稿=%r（差 %r×）；'
        '两式不可能同时为真，且差值不在同一 a 幂次上（[Q5]）⇒ 属公式缺陷，非约定自由度。'
        % (law_tab[1][1], law_tab[1][2], law_tab[1][1] / law_tab[1][2]))
    rec('Q9-scale', 'β 的量纲约定要显式声明', 'INFO',
        'Binet 一阶式里 β 量纲 m²（Δφ=2πβ/p²），GR 形式里 β 量纲 m（Δφ=2πβ/p）；'
        '本轮两套并记，β_GR=%r m，β_Binet(标定)=%r m²。混用会把"普适性"读成两个不同参数。'
        % (MU_SUN, beta_binet))

    # ---- 汇总 ----
    npass = sum(1 for j in JUDGE if j['verdict'] == 'PASS')
    nfail = sum(1 for j in JUDGE if j['verdict'] == 'FAIL')
    other = len(JUDGE) - npass - nfail
    print('\n' + '=' * 78)
    print('判定汇总：PASS %d / FAIL %d / OPEN+BOUNDARY+INFO %d（共 %d 条；'
          '本脚本不改变 claims.csv 里 C35 的 status）'
          % (npass, nfail, other, len(JUDGE)))
    out = {'script': 'spiral_c35_beta_universality.py',
           'inputs': {'GM': GM, 'c': C, 'M_sun': MSUN, 'beta_GR_m': MU_SUN,
                      'arcsec_rad': ARCSEC, 'julian_year_s': JULIAN_YR,
                      'planets': PLANETS, 'element_digits': ELEMENT_DIGITS,
                      'gr250_anchors': GR250,
                      'mercury_anchors': MERCURY_ANCHORS, 'h_rk4': h,
                      # [3] 的本底/容差是这 4 档网格的函数，引用时必须一起报出
                      'rk4_grids': [H_COARSE, h, h / 2.0, h / 4.0],
                      'c_second_for_2nd_order': C_SECOND},
           'gr_per_century': gr_pc,
           'beta_calibrated': {'binet_m2': beta_binet, 'draft': beta_draft},
           'law_table': [{'planet': t[0], 'geo_binet': t[1], 'geo_draft': t[2],
                          'ratio': t[3], 'structural_a_ratio': t[4]} for t in law_tab],
           'rk4': [{'label': t[0], 'numeric_h_over_4': t[1], 'closed_first_order': t[2],
                    'abs_resid': t[3], 'rel_resid': t[4], 'd_h_to_h2': t[5],
                    'd_h2_to_h4': t[6], 'floor_spread_4_grids': t[7], 'q_adjacent': t[8],
                    'second_order_term_5pi_x2': t[9], 'tolerance': t[10],
                    'second_order_measured': t[11], 'second_order_bar': t[12]}
                   for t in num_cases],
           'beta_lambda_drift': [{'planet': k, 'binet_ratio': v[0], 'draft_ratio': v[1],
                                  'max_rel_drift': v[2]} for k, v in inv_ratio.items()],
           'venus_gap_arcsec_century': venus_gap,
           'earth_gap_arcsec_century': earth_gap,
           'mercury_anchor_spread': spread_mer,
           'power': {'venus': power_v, 'earth': power_e},
           'error_bars': {'orbit_relative': {t[0]: t[1] for t in orbit_bars},
                          'anchor_half_ulp': d_anchor,
                          'gr_constant_relative': rel_const,
                          'geo_term_abs': bar_geo,
                          'geo_term_relative': rel_geo,
                          'dominant_leg': legs[0],
                          'gap_abs_venus': bar_v, 'gap_abs_earth': bar_e},
           'judgments': JUDGE}
    face = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'spiral_c35_beta_universality_claims.json')
    nonfinite = []
    out = json_finite(out, nonfinite)
    with open(face, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2, allow_nan=False)
    print('\n已写出 %s（版面钉在脚本旁边，可从文件名找回产生者）' % face)
    print('版面严格性：非有限浮点 %d 个已写成 null（`NaN` 字面量会让 jq / JSON.parse '
          '打不开整份版面）' % len(nonfinite))
    return 1 if (strict and nfail) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
