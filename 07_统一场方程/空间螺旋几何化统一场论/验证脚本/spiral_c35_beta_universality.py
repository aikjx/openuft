# -*- coding: utf-8 -*-
"""C35 追加：金星 + 地球轨道进动交叉验证，检验 β 普适性（标准库 math，双精度）

用户下达的问题
--------------
「C35：金星 + 地球轨道进动交叉验证，检验 β 普适性」。

本轮要回答的不是「β 对不对」，而是**这个交叉验证在仓库现有的数据下能不能做**，
以及**它的判决力活在哪一条轴上**。三件事在代码里钉死：

1. **β 在任何跨行星比值里精确约掉。** 两条候选几何式都对 β 线性，
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
* 「判据 PASS」只说明本仪器算对了，**不说明 β 普适性成立**。物理侧结论见 [Q8]：OPEN。
* 本脚本不改 `claims.csv` 里 C35 的 status（那是台账的活）。
* 只用标准库 `math`（本目录 README §1 红线：不引入 sympy / mpmath）。
  与 250 位版面的是非由 [Q1] 的双路对账判定，不由位数判定。
* 退出码默认恒为 0（本目录约定）；加 `--strict` 时任何内部判据 FAIL 则退出码 1。

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

EPS = sys.float_info.epsilon           # 双精度机器 epsilon：[4] 的"约掉"判据地板
# 行星元：a [m]、e、T [年]、仓库内的"参考值"[角秒/百年]
PLANETS = [
    ('水星', 5.790905e10, 0.20563069, 0.240846, 43.03),
    ('金星', 1.0820893e11, 0.00677672, 0.615197, 8.62),
    ('地球', 1.4959787e11, 0.0167086, 1.000017, 3.84),
]
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
    数值色散与步长偏差全在相减里抵消，这样 [Q4] 测的是物理而不是求根器。
    """
    A = 1.0 / semilatus(a, e)

    def integrate(eps_loc, h_loc):
        def rhs(u, up):
            return (up, A + eps_loc * u * u - u)

        u, up = A * (1.0 + e), 0.0
        phi = 0.0
        prev = None
        while phi < 2.0 * math.pi + 0.5:
            k1u, k1p = rhs(u, up)
            k2u, k2p = rhs(u + 0.5 * h_loc * k1u, up + 0.5 * h_loc * k1p)
            k3u, k3p = rhs(u + 0.5 * h_loc * k2u, up + 0.5 * h_loc * k2p)
            k4u, k4p = rhs(u + h_loc * k3u, up + h_loc * k3p)
            un = u + h_loc / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
            upn = up + h_loc / 6.0 * (k1p + 2 * k2p + 2 * k3p + k4p)
            phin = phi + h_loc
            if prev is not None and prev[1] > 0.0 and upn <= 0.0 and phi > math.pi:
                # u' 由正转负：线性插值定根，再对根做二分细化
                lo_u, lo_up = prev[0], prev[1]
                lo_phi = phi
                for _ in range(60):
                    mid = 0.5 * (lo_phi + phin)
                    # 从 prev 点重积分半步（RK4 半步足够精细）
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
            u, up, phi = un, upn, phin
        return float('nan')

    phi_grav = integrate(eps, h)
    phi_flat = integrate(0.0, h)
    return (phi_grav - phi_flat)


def ulp_rel(value, decimals):
    """把表格里"只给到第 decimals 位"当成 ±0.5 末位，返回相对不确定度。"""
    return 0.5 * 10.0 ** (-decimals) / abs(value)


def max_abs_rel_drift(vals):
    """同一比值在 β 缩放 λ 下的最大相对漂移 = 极差 / 量级。

    分母取 |值| 的最大者而不是均值：这里要的是"漂移有没有超出双精度舍入"，
    与比值本身的大小无关。
    """
    scale = max(abs(v) for v in vals)
    if scale == 0.0:
        return 0.0
    return (max(vals) - min(vals)) / scale


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
    num_cases = []
    for label, eps, closed in (
            ('GR（eps=3GM/c²）', MU_SUN, dphi_gr_per_orbit(*PLANETS[0][1:3])),
            ('Binet 一阶（eps=β/p，水星标定 β）', beta_binet / semilatus(PLANETS[0][1], PLANETS[0][2]),
             law_binet(beta_binet, PLANETS[0][1], PLANETS[0][2]))):
        num = rk4_dphi(PLANETS[0][1], PLANETS[0][2], eps, h)
        rel = abs(num - closed) / abs(closed)
        num_cases.append((label, num, closed, rel))
        print('  %-34s RK4=%r 闭式=%r 相对差=%r' % (label, num, closed, rel))
    worst_num = max(num_cases, key=lambda t: t[3])
    judge('Q3', 'RK4 数值积分复现闭式（相对差 <1e-6）⇒ 进动公式不是抄来的，是这条 ODE 的解',
          worst_num[3] < 1e-6, '最差例「%s」相对差 %r（步长 h=%r，eps=0 同批积分作本底相减）'
                               % (worst_num[0], worst_num[3], h))

    # ---- 4) β 在跨行星比值里精确约掉：可检验内核是幂次，不是数值 ----
    print('\n[4] β 普适性的可检验内核：跨行星比值对 β 的耦合（三条 λ 缩放）')
    inv_ratio = {}
    spread = []
    for name, a, e, T, ref in PLANETS[1:]:
        vb_vals, vd_vals = [], []
        for lam in (0.4, 1.0, 1.7, 10.0):
            vb_vals.append(per_century_of(law_binet, lam * beta_binet, a, e, T) /
                           per_century_of(law_binet, lam * beta_binet, a0, e0, T0))
            vd_vals.append(per_century_of(law_draft, lam * beta_draft, a, e, T) /
                           per_century_of(law_draft, lam * beta_draft, a0, e0, T0))
        drift = max(max_abs_rel_drift(vb_vals), max_abs_rel_drift(vd_vals))
        inv_ratio[name] = (vb_vals[0], vd_vals[0], drift)
        spread.append((name, vb_vals, vd_vals))
        print('  %-3s β 缩放 0.4/1.0/1.7/10 下：binet 律比值=%r draft 律比值=%r 最大相对漂移=%r'
              % (name, vb_vals[0], vd_vals[0], drift))
    worst_drift = max(v[2] for v in inv_ratio.values())
    judge('Q4', '把 β 乘 0.4/1.0/1.7/10 之后，金星/地球对水星的几何项比值不随 λ 动'
                '（最大相对漂移 <1e-15，双精度内即"约掉"）⇒ β 普适性检验的载荷不是 β 的'
                '大小，是 a 的幂次',
          worst_drift < 1e-15,
          '最大相对漂移 = %r；比值本身：金星 binet=%r draft=%r，地球 binet=%r draft=%r'
          % (worst_drift, inv_ratio['金星'][0], inv_ratio['金星'][1],
             inv_ratio['地球'][0], inv_ratio['地球'][1]))
    print('  注：这不是"恒等式所以无信息"。它说明的是——任何只用水星标定 β 的方案，'
          '在跨行星比值上自动失去对 β 的敏感度；能失去的敏感度只剩 a 的幂次。')

    # ---- 5) 两条候选式给出不同的金星/地球预言：幂次差 = a_M/a_p 的精确结构 ----
    print('\n[5] 同一水星标定下，两条几何式在金星/地球的预言差（§13-C35-3 的独立复现）')
    law_tab = []
    for name, a, e, T, ref in PLANETS:
        vb = per_century_of(law_binet, beta_binet, a, e, T)
        vd = per_century_of(law_draft, beta_draft, a, e, T)
        law_tab.append((name, vb, vd, vd / vb, a_ := PLANETS[0][1] / a))
        print('  %-3s Binet 一阶=%r 草稿式=%r 草稿/Binet=%r 结构预期 a_水星/a_%s=%r'
              % (name, vb, vd, vd / vb, name, PLANETS[0][1] / a))
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
    judge('Q6', '金星/地球的仓库参考值与 GR 预言之差 <1%（8.62/3.84 是预言的取整），'
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

    # ---- 8) 误差棒：理论侧 vs 观测侧 ----
    print('\n[8] 误差棒（把表格末位当 ±0.5 末位传播；进动只通过 p 依赖轨道元）')
    bars = []
    for name, a, e, T, ref in PLANETS:
        sa = ulp_rel(a, 7 if a > 1e11 else 6)             # a 给到 8 位有效数字
        se = 0.5 * 1e-8                                    # e 给到 8 位小数
        # dln p = dln a 与 d ln(1-e²) = -2e de/(1-e²)；dln T 由 [2] 已知与 a 同一条腿
        rel_p = math.hypot(sa, 2.0 * e * se / (1.0 - e * e))
        sT = ulp_rel(T, 6)
        rel_dphi = math.hypot(rel_p, sT)                   # Δφ_百年 ∝ 1/(p·T)
        bars.append((name, rel_dphi, per_century(dphi_gr_per_orbit(a, e), T) * rel_dphi))
        print('  %-3s 理论侧相对误差棒=%r ⇒ 绝对 %r 角秒/百年' % (name, rel_dphi, bars[-1][2]))
    worst_bar = max(bars, key=lambda t: t[1])
    judge('Q8', '理论侧误差棒（末位取整传播）最大 %r ⇒ 相对 %r，比 [7] 的信号还小 12 个量级以上：'
                '**瓶颈完全不在轨道元精度**' % (worst_bar[2], worst_bar[1]),
          worst_bar[1] < 1e-9,
          '最大在 %s：相对 %r（观测侧在本仓库不存在，见 [6]）' % (worst_bar[0], worst_bar[1]))

    # ---- 9) 物理侧结论（不进 PASS 计数）----
    print('\n[9] 物理侧结论')
    rec('Q9-status', '金星+地球交叉验证「检验 β 普适性」当前不可执行', 'OPEN',
        'β 普适性可检验的内核是几何项的 a 幂次（[Q4]），而本仓库：'
        '①金星/地球无观测残差（[Q6]，参考值即预言）；②两式之差在水星锚点极差之下（[Q7]）；'
        '③β 本身无第一性来源（承接 §13-C35-2 BOUNDARY）。⇒ 本轮把 C35 从「框架就绪」'
        '推进到「**判决力已被定量定位：需要 ~1e-3 角秒/百年级历表残差 + β 的第一性式**」，'
        '不升等级。')
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
                      'planets': PLANETS, 'gr250_anchors': GR250,
                      'mercury_anchors': MERCURY_ANCHORS, 'h_rk4': h},
           'gr_per_century': gr_pc,
           'beta_calibrated': {'binet_m2': beta_binet, 'draft': beta_draft},
           'law_table': [{'planet': t[0], 'geo_binet': t[1], 'geo_draft': t[2],
                          'ratio': t[3], 'structural_a_ratio': t[4]} for t in law_tab],
           'rk4': [{'label': t[0], 'numeric': t[1], 'closed': t[2], 'rel': t[3]}
                   for t in num_cases],
           'venus_gap_arcsec_century': venus_gap,
           'mercury_anchor_spread': spread_mer,
           'power': {'venus': power_v, 'earth': power_e},
           'judgments': JUDGE}
    face = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'spiral_c35_beta_universality_claims.json')
    with open(face, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print('\n已写出 %s（版面钉在脚本旁边，可从文件名找回产生者）' % face)
    return 1 if (strict and nfail) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
