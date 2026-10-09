# -*- coding: utf-8 -*-
"""
四力三要素 · 空间光速螺旋（v=c）全维求导验证
=============================================

命题（用户给出，本册正面求导并机器验证）：
    以「空间光速螺旋 v=c」为唯一几何公设，用 曲率 kappa、挠率 tau、
    频率 f、角速度 Omega 这几个量，求导出四力统一场论中
    力的【大小 / 方向 / 距离(力程)】三要素，并给出全维求导证明验证。

本册立场（先声明，避免与既有册重复）：
  * 既有 ADD-02/03/04 三册在 (kappa,tau) 参数流形上做【经验耦合匹配】
    Omega = lambda*cos(3*theta)，其 tau 依赖来自外加函数，不是求导所得。
  * 既有 S02 攻破册只审动力学公设 P=m(c-v) / F=dP/dt，未做 kappa,tau 求导链。
  * 本册是【求导层】的正面构造：只从 v=c 圆柱螺旋的微分几何出发，
    逐阶求导（位置 -> 速度 -> 加速度 -> 加加速度 jerk），
    看三要素中哪几项真能由求导产生、哪几项必须由外部输入。

四条求导公设（本册唯一输入）：
  P1 光速螺旋：质点沿空间曲线弧长速率恒为 c，|dr/dt| = c
  P2 圆柱螺旋参数化：r(t) = (R cos(Omega t), R sin(Omega t), u t)
  P3 Frenet-Serret：kappa, tau 由 r(t) 的各阶导数定义
  P4 力 = 质量 x 加速度（牛顿第二定律，二阶动力学）

输出：数据/四力三要素_空间光速螺旋全维求导验证_2026-10-08.{json,md}
纯标准库（decimal 60 位 + fractions 量纲 + 有限差分对拍），退出码 0。
"""

from __future__ import annotations

import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

# ---------------------------------------------------------------- 常量（CODATA）

C = Decimal("299792458")                  # 真空光速 m/s
HBAR = Decimal("1.054571817e-34")         # 约化普朗克常数 J*s
G_N = Decimal("6.67430e-11")              # 引力常数
ALPHA = Decimal("7.2973525693e-3")        # 精细结构常数
M_E = Decimal("9.1093837015e-31")         # 电子质量 kg
M_P = Decimal("1.67262192369e-27")        # 质子质量 kg
Q_E = Decimal("1.602176634e-19")          # 元电荷 C
K_COUL = C * C * Decimal("1e-7")          # 1/(4 pi eps0) = c^2 * 1e-7（不由手抄截断值，避免伪残差）
G0 = Decimal("9.80665")                   # 标准重力加速度 m/s^2
YR = Decimal("31557600")                  # 年（儒略）
PC = Decimal("3.0856775814913673e16")     # 秒差距 m
AGE_UNIV = Decimal("4.35e17")             # 宇宙年龄 s（Planck18 138亿年）
R_UNIV = Decimal("8.8e26")                # 可观测宇宙半径 m（量级）

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "数据")
STEM = "四力三要素_空间光速螺旋全维求导验证_2026-10-08"

# ---------------------------------------------------------------- 记录器

ITEMS = []      # 判定条目
GUARDS = []     # 自检（负向/一致性）


def add(iid, status, title, expect, actual, note=""):
    ITEMS.append({
        "id": iid, "status": status, "title": title,
        "expect": expect, "actual": actual, "note": note,
    })


def guard(gid, ok, desc, detail=""):
    GUARDS.append({"id": gid, "ok": bool(ok), "desc": desc, "detail": str(detail)})
    return bool(ok)


def P(iid, t, e, a, n=""): add(iid, "PASS", t, e, a, n)
def F(iid, t, e, a, n=""): add(iid, "FAIL", t, e, a, n)
def B(iid, t, e, a, n=""): add(iid, "BOUNDARY", t, e, a, n)
def I(iid, t, e, a, n=""): add(iid, "INFO", t, e, a, n)
def M(iid, t, e, a, n=""): add(iid, "MISMATCH", t, e, a, n)


def d(x):
    """转 Decimal（接受 float/int/Decimal/str）"""
    if isinstance(x, Decimal):
        return x
    return Decimal(str(x))


def fx(x, n=6):
    """定点科学计数输出（不用 quantize，高位会抛 InvalidOperation）"""
    return format(d(x), "." + str(n) + "E")


def rel(a, b):
    """相对偏差 |a-b|/|b|"""
    a, b = d(a), d(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


# ---------------------------------------------------------------- 量纲（L, M, T 整数指数）

def dim(*e):
    return (Fraction(e[0]), Fraction(e[1]), Fraction(e[2]))


D_L, D_M, D_T = dim(1, 0, 0), dim(0, 1, 0), dim(0, 0, 1)
D_C = dim(1, 0, -1)          # 速度
D_KAPPA = dim(-1, 0, 0)      # 曲率/挠率
D_HBAR = dim(2, 1, -1)       # 作用量
D_FORCE = dim(1, 1, -2)      # 力
D_ENERGY = dim(2, 1, -2)     # 能量
D_MOM = dim(1, 1, -1)        # 动量
D_OMEGA = dim(0, 0, -1)      # 角速度


def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dpow(a, n):
    return (a[0] * n, a[1] * n, a[2] * n)


def dstr(a):
    return "L^%s M^%s T^%s" % (a[0], a[1], a[2])


# ---------------------------------------------------------------- 圆柱螺旋的解析各阶导数

def helix_derivs(R, Om, u, t):
    """返回 r', r'', r'''（float 三元列表）"""
    R, Om, u, t = float(R), float(Om), float(u), float(t)
    s, co = math.sin(Om * t), math.cos(Om * t)
    r1 = [-R * Om * s, R * Om * co, u]
    r2 = [-R * Om * Om * co, -R * Om * Om * s, 0.0]
    r3 = [R * Om ** 3 * s, -R * Om ** 3 * co, 0.0]
    return r1, r2, r3


def vcross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def vdot(a, b):
    return sum(x * y for x, y in zip(a, b))


def vnorm(a):
    return math.sqrt(vdot(a, a))


def vunit(a):
    n = vnorm(a)
    return [x / n for x in a], n


def numeric_kappa_tau(R, Om, u, t, h=None):
    """用有限差分（纯数值，不经手解析式）复算 kappa / tau，用于对拍

    坑（本册踩过并修复）：差分步长必须按角速度缩放 h = 1e-6/Omega。
    样本 Omega ~ 3.5e20 s^-1，若仍取 h=1e-6 s，则相位步长 Omega*h ~ 3.5e14 rad，
    三角函数在差分点上完全无关 ⇒ 差分结果恒为垃圾（相对误差 1.0）。
    """
    if h is None:
        h = 1e-6 / max(abs(Om), 1e-30)   # 相位步长固定为 1e-6 弧度
    def r(tt):
        return [R * math.cos(Om * tt), R * math.sin(Om * tt), u * tt]

    def dr(tt, k):
        # k 阶中心差分
        if k == 1:
            return [(x - y) / (2 * h) for x, y in zip(r(tt + h), r(tt - h))]
        if k == 2:
            a, b, c = r(tt + h), r(tt), r(tt - h)
            return [(x - 2 * y + z) / (h * h) for x, y, z in zip(a, b, c)]
        if k == 3:
            p2, p1, m1, m2 = r(tt + 2 * h), r(tt + h), r(tt - h), r(tt - 2 * h)
            return [(a - 2 * b + 2 * c - e) / (2 * h ** 3) for a, b, c, e in zip(p2, p1, m1, m2)]
        raise ValueError

    r1, r2, r3 = dr(t, 1), dr(t, 2), dr(t, 3)
    if vnorm(r1) == 0.0 or vnorm(vcross(r1, r2)) == 0.0:
        raise ValueError("差分退化：步长 %g 在当前 t=%g 下被浮点吞掉（请取 t=0 使步长可分辨）" % (h, t))
    cr = vcross(r1, r2)
    kap = vnorm(cr) / (vnorm(r1) ** 3)
    tau = vdot(cr, r3) / (vnorm(cr) ** 2)
    return kap, tau


# ================================================================ A 段 · 求导链（正面构造）

def sec_A():
    """A 段：v=c 圆柱螺旋的逐阶求导链（全部机器复算）"""
    res = {}
    cc = float(C)

    # --- 取一组具体螺旋：给定 (kappa, tau)，由闭式反解 (R, u, Omega)
    kap0, ratio = 1.0e12, 0.6
    tau0 = kap0 * ratio
    rho = math.hypot(kap0, tau0)          # sqrt(k^2+t^2)
    Om = cc * rho                          # Omega = c*rho
    Rg = kap0 / (kap0 ** 2 + tau0 ** 2)    # R = kappa/rho^2
    uu = tau0 * cc / rho                   # u = tau*c/rho
    t0 = 0.37

    res["sample"] = {
        "kappa_m^-1": kap0, "tau_m^-1": tau0, "tau_over_kappa": ratio,
        "rho_m^-1": rho, "Omega_s^-1": Om, "R_m": Rg, "u_m/s": uu,
    }

    # --- A-01 速率分解：|dr/dt| = c（公设 P1 自洽性）
    r1, r2, r3 = helix_derivs(Rg, Om, uu, t0)
    speed = vnorm(r1)
    e01 = rel(speed, cc)
    if e01 < 1e-12:
        P("A-01", "速率分解 |dr/dt|^2 = (R*Omega)^2 + u^2 = c^2", "c = %s" % fx(C),
          "|r'| = %s m/s，相对偏差 %.3e" % (fx(speed), e01),
          "闭式反解出的 (R,u,Omega) 使弧长速率精确等于 c，公设 P1 与参数化自洽")
    else:
        F("A-01", "速率分解", "c", fx(speed), "反解不成立")
    guard("g-A01", e01 < 1e-12, "速率分解残差 < 1e-12", "%.3e" % e01)

    # --- A-02 曲率：闭式 R*Omega^2/c^2  vs  解析导数  vs  有限差分
    cr = vcross(r1, r2)
    kap_deriv = vnorm(cr) / (vnorm(r1) ** 3)
    kap_closed = Rg * Om ** 2 / cc ** 2
    # 差分对拍必须在 t=0 做：Omega~3.5e20 ⇒ 相位步长对应的绝对步长 h~2.9e-27 s，
    # 在 t=0.37 处会被 double 分辨率（~5e-17）整个吞掉（本册踩过，见函数 docstring）。
    kap_fd, tau_fd = numeric_kappa_tau(Rg, Om, uu, 0.0)
    e02a = rel(kap_deriv, kap_closed)
    e02b = rel(kap_fd, kap_closed)
    if max(e02a, e02b) < 1e-6:
        P("A-02", "Frenet 曲率 kappa = |r' x r''|/|r'|^3 = R*Omega^2/c^2",
          "kappa = %s m^-1" % fx(kap0),
          "解析导数 %s / 有限差分 %s，相对偏差 %.3e / %.3e" % (fx(kap_deriv), fx(kap_fd), e02a, e02b),
          "三路（闭式、解析导数、纯数值差分）一致")
    else:
        F("A-02", "曲率求导", fx(kap0), "%s / %s" % (fx(kap_deriv), fx(kap_fd)), "三路不一致")
    guard("g-A02", max(e02a, e02b) < 1e-6, "曲率三路对拍 < 1e-6",
          "%.3e / %.3e" % (e02a, e02b))

    # --- A-03 挠率：闭式 u*Omega/c^2
    tau_deriv = vdot(cr, r3) / (vnorm(cr) ** 2)
    tau_closed = uu * Om / cc ** 2
    e03a = rel(tau_deriv, tau_closed)
    e03b = rel(tau_fd, tau_closed)
    # 阈值分层：解析导数应机器精度（1e-9）；三阶中心差分受浮点抵消限制
    # （h~2.9e-27 s，h^3~2e-80，r''' 由 4 个 O(1e-13) 点差分而来 ⇒ 只能到 ~1e-4 量级），
    # 故差分量只作【量级确认】，阈值取 1e-3，且该局限必须写进 note（不得伪称精密对拍）。
    if e03a < 1e-9 and e03b < 1e-3:
        P("A-03", "Frenet 挠率 tau = det(r',r'',r''')/|r' x r''|^2 = u*Omega/c^2",
          "tau = %s m^-1" % fx(tau0),
          "解析导数 %s（偏差 %.3e）/ 有限差分 %s（偏差 %.3e，三阶差分固有精度）"
          % (fx(tau_deriv), e03a, fx(tau_fd), e03b),
          "解析路机器精度一致；差分路仅到量级（h^3~1e-80 的浮点抵消，非理论问题）")
    else:
        F("A-03", "挠率求导", fx(tau0), "%s / %s" % (fx(tau_deriv), fx(tau_fd)), "对拍不成立")
    guard("g-A03", e03a < 1e-9 and e03b < 1e-3, "挠率对拍（解析<1e-9 且 差分<1e-3）",
          "%.3e / %.3e" % (e03a, e03b))

    # --- A-04 三重奏 kappa^2 + tau^2 = (Omega/c)^2（高精度 Decimal）
    # 注意：Omega 必须用 Decimal 由 rhoD 现算；若用上面 float 的 Om 转 Decimal，
    # 会把 float 的 ~1e-16 相对误差带进来，60 位阈值 1e-40 永远过不去（本册踩过）。
    kD, tD = d(kap0), d(tau0)
    rhoD = (kD * kD + tD * tD).sqrt()
    OmD = C * rhoD
    lhsD = kD * kD + tD * tD
    rhsD = (OmD / C) ** 2
    e04 = rel(lhsD, rhsD)
    if e04 < Decimal("1e-40"):
        P("A-04", "三重奏 kappa^2 + tau^2 = (Omega/c)^2（v=c 特化）",
          "两边逐位相等", "相对偏差 %s（60 位）" % fx(e04),
          "回链第 7 章式 (4)：三重奏是 v=c 螺旋的数学恒等式，求导即得")
    else:
        F("A-04", "三重奏", "0", fx(e04), "不成立")
    guard("g-A04", e04 < Decimal("1e-40"), "三重奏残差 < 1e-40", fx(e04))
    res["triad_rel_err"] = float(e04)

    # --- A-05 逆映射闭式：(kappa,tau) -> (R,u,Omega)，并回代验证
    Om2 = C * rhoD
    R2 = kD / (kD * kD + tD * tD)
    u2 = tD * C / rhoD
    # 回代：kappa = R*Omega^2/c^2, tau = u*Omega/c^2
    k_back = R2 * Om2 * Om2 / (C * C)
    t_back = u2 * Om2 / (C * C)
    e05 = max(rel(k_back, kD), rel(t_back, tD))
    if e05 < Decimal("1e-40"):
        P("A-05", "逆映射闭式 Omega=c*rho, R=kappa/rho^2, u=tau*c/rho（rho=sqrt(k^2+t^2)）",
          "回代 (kappa,tau) 复原", "最大相对偏差 %s（60 位）" % fx(e05),
          "给定 (kappa,tau) 唯一确定螺旋三参量 (R,u,Omega)：自由度 0")
    else:
        F("A-05", "逆映射", "0", fx(e05), "回代不成立")
    guard("g-A05", e05 < Decimal("1e-40"), "逆映射回代残差 < 1e-40", fx(e05))
    res["inverse_map"] = {"Omega": fx(Om2), "R": fx(R2), "u": fx(u2)}

    # --- A-06 加速度（= 力）：Frenet 分解，检查 tau 是否进入
    T_, _ = vunit(r1)
    N_, _ = vunit(r2)
    Bv = vcross(r1, r2)
    B_, _ = vunit(Bv)
    aT, aN, aB = vdot(r2, T_), vdot(r2, N_), vdot(r2, B_)
    a_c2k = cc ** 2 * kap0
    e06 = max(abs(aT) / a_c2k, abs(aB) / a_c2k, rel(abs(aN), a_c2k))
    if e06 < 1e-9:
        P("A-06", "加速度分解 a = c^2*kappa*N（切向 0、副法向 0）",
          "|a| = c^2*kappa = %s m/s^2" % fx(a_c2k),
          "a·T = %.3e, a·N = %s, a·B = %.3e（|a| 归一）" % (abs(aT) / a_c2k, fx(aN), abs(aB) / a_c2k),
          "**tau 在加速度（=力）中系数严格为 0**：v=c 常量使切向导数为零、副法向无分量")
    else:
        F("A-06", "加速度分解", "纯 N 向", "aB=%.3e" % (abs(aB) / a_c2k), "分解不成立")
    guard("g-A06", e06 < 1e-9, "加速度纯主法向、无 tau 分量", "%.3e" % e06)
    res["accel_decomp"] = {"a_dot_T": aT / a_c2k, "a_dot_N": aN / a_c2k, "a_dot_B": aB / a_c2k}

    # --- A-07 加加速度 jerk：tau 只在三阶副法向出现
    jT, jN, jB = vdot(r3, T_), vdot(r3, N_), vdot(r3, B_)
    j_pred_B = cc ** 3 * kap0 * tau0
    j_pred_T = -(cc ** 3) * kap0 * kap0
    e07 = max(rel(jB, j_pred_B), rel(jT, j_pred_T), abs(jN) / abs(j_pred_B))
    if e07 < 1e-6:
        P("A-07", "三阶 jerk 分解 j = -c^3*kappa^2*T + c^3*kappa*tau*B",
          "j·B = c^3*kappa*tau = %s" % fx(j_pred_B),
          "j·T = %s, j·B = %s, |j·N|/|j·B| = %.3e" % (fx(jT), fx(jB), abs(jN) / abs(j_pred_B)),
          "tau 只在【三阶】副法向出现；标准力学是二阶的 ⇒ tau 进不到力")
    else:
        F("A-07", "jerk 分解", fx(j_pred_B), "%s / %s" % (fx(jT), fx(jB)), "不成立")
    guard("g-A07", e07 < 1e-6, "jerk 三阶分解对拍 < 1e-6", "%.3e" % e07)
    res["jerk_decomp"] = {"j_dot_T": fx(jT), "j_dot_B": fx(jB), "j_dot_N_over_jB": float(abs(jN) / abs(j_pred_B))}

    # --- A-08 康普顿闭合：映射公设 Omega = omega 且 E = hbar*omega = m*c^2
    for name, mm in (("电子", M_E), ("质子", M_P)):
        rho_c = mm * C / HBAR           # m c / hbar   (= 1/康普顿波长)
        om_c = C * rho_c                # Omega = c*rho = m c^2/hbar = omega
        E_chk = HBAR * om_c
        E_mc2 = mm * C * C
        e08 = rel(E_chk, E_mc2)
        res["compton_" + ("e" if name == "电子" else "p")] = {
            "rho_m^-1": fx(rho_c), "Omega_s^-1": fx(om_c),
            "compton_wl_m": fx(1 / rho_c), "hbar_Omega_J": fx(E_chk),
            "mc2_J": fx(E_mc2), "rel_err": float(e08),
        }
    e08m = max(res["compton_e"]["rel_err"], res["compton_p"]["rel_err"])
    if e08m < 1e-15:
        P("A-08", "康普顿闭合：Omega=omega 且 E=hbar*omega=m*c^2 ⇒ sqrt(kappa^2+tau^2) = m*c/hbar",
          "hbar*Omega = m*c^2",
          "电子 rho=%s m^-1（康普顿波长 %s m）、Omega=%s s^-1；相对偏差 %.3e"
          % (fx(res["compton_e"]["rho_m^-1"]), fx(res["compton_e"]["compton_wl_m"]),
             fx(res["compton_e"]["Omega_s^-1"]), e08m),
          "频率映射公设一旦采取，几何不变量 rho 被质量锁死为康普顿波数")
    else:
        F("A-08", "康普顿闭合", "0", "%.3e" % e08m, "不成立")
    guard("g-A08", e08m < 1e-15, "康普顿闭合残差 < 1e-15", "%.3e" % e08m)

    return res


# ================================================================ B 段 · 三要素（大小 / 方向 / 距离）

def sec_B(resA):
    res = {}

    # --- B-01 大小：|F| = m*c^2*kappa，量纲审计
    dimF = dmul(dmul(D_M, dpow(D_C, 2)), D_KAPPA)
    okB1 = (dimF == D_FORCE)
    kap_s = 1.0e12
    Fnum = M_P * C * C * d(kap_s)
    if okB1:
        P("B-01", "力的大小 |F| = m*c^2*kappa（由 A-06 求导直接得到）",
          "[m][c]^2[kappa] = L^1 M^1 T^-2 = [力]",
          "%s = 力量纲 ✓；质子 @ kappa=%s m^-1 ⇒ |F| = %s N"
          % (dstr(dimF), fx(kap_s), fx(Fnum)),
          "这是本册唯一一条【纯求导、无需任何外部耦合输入】的三要素读数")
    else:
        F("B-01", "力量纲", dstr(D_FORCE), dstr(dimF), "量纲不合")
    guard("g-B01", okB1, "[m c^2 kappa] == [力]", dstr(dimF))

    # --- B-02 自力标度：Omega=omega 且 E=hbar*omega=m*c^2 ⇒ kappa_max=rho=m*c/hbar
    for name, mm in (("电子", M_E), ("质子", M_P)):
        rho_c = mm * C / HBAR
        Fself = mm * C * C * rho_c                      # = m^2 c^3 / hbar
        lam_c = HBAR / (mm * C)                          # 约化康普顿波长
        r_cl = ALPHA * lam_c                             # 经典半径 = alpha*康普顿波长
        Fchk = ALPHA * mm * C * C / r_cl                 # alpha * m c^2 / r_e
        res["self_" + ("e" if name == "电子" else "p")] = {
            "rho_m^-1": fx(rho_c), "F_self_N": fx(Fself),
            "compton_wl_m": fx(lam_c), "classical_radius_m": fx(r_cl),
            "alpha_mc2_over_re_N": fx(Fchk), "ratio": fx(rel(Fself, Fchk) + 1),
        }
    r_e = res["self_e"]
    eB2 = abs(d(r_e["ratio"]) - 1)
    if eB2 < Decimal("1e-30"):
        P("B-02", "自力标度 F_self = m^2*c^3/hbar = alpha*(m*c^2/r_classical)",
          "两路恒等（比值 = 1）",
          "电子 F_self = %s N（r_e=%s m，比值 %s）｜质子 F_self = %s N"
          % (r_e["F_self_N"], r_e["classical_radius_m"], r_e["ratio"], res["self_p"]["F_self_N"]),
          "求导+康普顿映射给出的力的量级是【自力】标度（电子 ~0.212 N），"
          "它不是引力、不是电磁、与任何已知相互作用都不对应")
    else:
        F("B-02", "自力标度恒等式", "1", r_e["ratio"], "两路不等")
    guard("g-B02", eB2 < Decimal("1e-30"), "F_self 两路恒等（差值 < 1e-30）", fx(eB2))

    # --- B-03 方向：F 沿主法向 N；对圆柱螺旋 N 恒指向轴 ⇒ 恒向心
    cc = float(C)
    kap0, ratio = 1.0e12, 0.6
    tau0 = kap0 * ratio
    rho = math.hypot(kap0, tau0)
    Om = cc * rho
    Rg = kap0 / (kap0 ** 2 + tau0 ** 2)
    uu = tau0 * cc / rho
    worst = 0.0
    dirs = []
    for t in [0.0, 0.37, 1.1, 2.9, 5.3]:
        r1, r2, r3 = helix_derivs(Rg, Om, uu, t)
        N_, _ = vunit(r2)
        radial = [math.cos(Om * t), math.sin(Om * t), 0.0]   # 背离轴的径向外指单位矢
        dot = vdot(N_, radial)                                # 应为 -1（恒指向轴）
        dirs.append(dot)
        worst = max(worst, abs(dot + 1.0))
    if worst < 1e-12:
        P("B-03", "力的方向 F ∥ N（主法向），对螺旋恒指向轴：N·r̂ = -1",
          "N·r̂ = -1 恒成立",
          "5 个时刻 N·r̂ = %s，最大偏差 %.3e" % (["%.15f" % x for x in dirs], worst),
          "**方向要素在求导层恒为向心、零信息量**：它不随 kappa/tau/Omega 变化，"
          "因此【排斥型力（同号电荷相斥）无法由该几何导出】")
    else:
        F("B-03", "方向", "-1", "%.3e" % worst, "方向不恒向心")
    guard("g-B03", worst < 1e-12, "方向恒向心（N·r̂ = -1）", "%.3e" % worst)
    res["direction_dot"] = dirs

    # --- B-04 距离（编码层）：kappa = alpha*康普顿波长/r^2 ⇒ F = alpha*hbar*c/r^2
    lam_p = HBAR / (M_P * C)
    r_ref = Decimal("1e-15")
    kap_enc = ALPHA * lam_p / (r_ref ** 2)
    F_enc = M_P * C * C * kap_enc
    F_coul = K_COUL * Q_E * Q_E / (r_ref ** 2)
    eB4 = rel(F_enc, F_coul)
    # 阈值说明：残差不是框架误差，而是 CODATA 常数自身的不确定度
    # （alpha 相对不确定度 ~1.5e-10，eps0 在 2019 SI 后同量级）。故取 1e-7。
    if eB4 < Decimal("1e-7"):
        P("B-04", "距离（编码层）：kappa = alpha*ƛ_C/r^2 ⇒ |F| = alpha*hbar*c/r^2 逐位还原库仑",
          "F = k_e*e^2/r^2 = %s N（r=1 fm）" % fx(F_coul),
          "编码式得 %s N，相对偏差 %s；恒等式 alpha*hbar*c = k_e*e^2 自检 %s"
          % (fx(F_enc), fx(eB4), fx(rel(ALPHA * HBAR * C, K_COUL * Q_E * Q_E) + 1)),
          "**注意这是编码不是导出**：求导只给 |F|=m*c^2*kappa；"
          "把 kappa 取成 alpha*ƛ_C/r^2 就把耦合 alpha 与康普顿波长塞回了几何")
    else:
        F("B-04", "编码还原", fx(F_coul), fx(F_enc), "不还原")
    guard("g-B04", eB4 < Decimal("1e-7"),
          "kappa=alpha*ƛ_C/r^2 还原库仑 < 1e-7（残差=CODATA 常数不确定度）", fx(eB4))
    res["encoding"] = {"kappa": fx(kap_enc), "F": fx(F_enc), "F_coulomb": fx(F_coul)}

    # --- B-05 距离（求导层）：常力定理 —— Omega=omega=常数 ⇒ kappa 常数 ⇒ |F| 不随距离衰减
    kappa_at = []
    for rr in ["1e-15", "1e-10", "1"]:
        rD = Decimal(rr)
        kap_needed = ALPHA * lam_p / (rD ** 2)      # 为还原 1/r^2 所需的 kappa(r)
        Om_needed = C * kap_needed                   # 三重奏（tau=0）要求的角速度
        kappa_at.append({"r_m": rr, "kappa_needed": fx(kap_needed), "Omega_needed": fx(Om_needed)})
    k1 = d(kappa_at[0]["kappa_needed"])
    k3 = d(kappa_at[2]["kappa_needed"])
    ratio_k = k1 / k3
    F("B-05", "距离（求导层）：Omega=omega 常数 ⇒ rho=kappa_max 常数 ⇒ |F| 常数（不衰减）",
      "四力均需 |F| ∝ 1/r^2",
      "为还原 1/r^2，所需 kappa 从 r=1 fm 的 %s 变到 r=1 m 的 %s（跨 %s 倍），"
      "⇒ 三重奏要求 Omega 同步跨 %s 倍，与 Omega=omega（内禀单色频率）正面冲突"
      % (fx(k1), fx(k3), fx(ratio_k), fx(ratio_k)),
      "**求导层给不出 1/r^2**：v=c 螺旋 + 内禀频率 ⇒ 力是常数，与四种已知力全不符")
    guard("g-B05", ratio_k > 1e10, "所需 kappa 随距离剧烈变化（>1e10 倍）⇒ 常力定理成立", fx(ratio_k))
    res["kappa_needed_table"] = kappa_at

    # --- B-06 四力反解表：kappa = alpha*ƛ_C/r^2，并检验三重奏可编码条件 kappa <= rho = m*c/hbar
    rho_p = M_P * C / HBAR
    table = []
    forces = [
        ("强 (alpha_s≈1, r=1 fm)", Decimal("1.0"), Decimal("1e-15")),
        ("电磁 (alpha, r=1 Å)", ALPHA, Decimal("1e-10")),
        ("弱 (alpha_2(M_Z), r=1 am)", Decimal("3.3804e-2"), Decimal("1e-18")),
        ("引力 (alpha_G(质子), r=1 m)", G_N * M_P * M_P / (HBAR * C), Decimal("1")),
    ]
    for nm, al, rr in forces:
        kap = al * lam_p / (rr ** 2)
        ome = C * kap
        RR = 1 / kap if kap != 0 else Decimal(0)
        lam_o = 2 * Decimal(str(math.pi)) * C / ome
        EeV = HBAR * ome / Q_E
        TT = 2 * Decimal(str(math.pi)) / ome
        feasible = kap <= rho_p
        table.append({
            "force": nm, "alpha": fx(al), "r_m": fx(rr), "kappa_m^-1": fx(kap),
            "Omega_s^-1": fx(ome), "R_m": fx(RR), "lambda_m": fx(lam_o),
            "hbar_Omega_eV": fx(EeV), "period_s": fx(TT),
            "kappa_over_rho": fx(kap / rho_p), "encodable": bool(feasible),
        })
    n_ok = sum(1 for t in table if t["encodable"])
    res["force_table"] = table
    if n_ok == len(table):
        P("B-06", "四力反解表：kappa=alpha*ƛ_C/r^2，且满足三重奏可编码条件 kappa <= m*c/hbar",
          "4/4 可编码", "%d/4 可编码" % n_ok, "")
    else:
        bad = [t["force"] for t in table if not t["encodable"]]
        F("B-06", "四力反解表（三重奏可编码条件 kappa <= rho = m*c/hbar）",
          "4/4 可编码", "%d/4 可编码；越界：%s" % (n_ok, "、".join(bad)),
          "越界者所需曲率超过质子康普顿波数 ⇒ 该力无法由质子螺旋承载")

    # --- B-07 引力所需螺旋尺度荒谬性（由表中引力行读数判定）
    grow = table[3]
    R_over_univ = d(grow["R_m"]) / R_UNIV
    T_over_age = d(grow["period_s"]) / AGE_UNIV
    F("B-07", "引力编码的螺旋尺度：R = 1/kappa 与周期 T = 2*pi/Omega 是否落在物理可达范围",
      "R ≲ 可观测宇宙、T ≲ 宇宙年龄",
      "R = %s m = %s 倍可观测宇宙；T = %s s = %s 倍宇宙年龄"
      % (grow["R_m"], fx(R_over_univ), grow["period_s"], fx(T_over_age)),
      "**几何编码引力需要一个比可观测宇宙还大的螺旋半径、比宇宙年龄还长的周期**"
      "⇒ 该编码无物理承载物（与 ADD-04 的「标度是编码非推导」同构）")
    guard("g-B07", R_over_univ > 1 and T_over_age > 1, "引力编码尺度超宇宙（两条都超）",
          "R/R_univ=%s, T/T_age=%s" % (fx(R_over_univ), fx(T_over_age)))
    res["gravity_scale"] = {"R_over_universe": fx(R_over_univ), "T_over_age": fx(T_over_age)}

    return res


# ================================================================ C 段 · 互斥定理与否证性读数

def sec_C(resA, resB):
    res = {}

    # --- C-01 三约束互斥（动力学推广版）：{v=c 螺旋、Omega=omega 内禀、|F| ∝ 1/r^2} ⇒ ∅
    rho_p = M_P * C / HBAR
    F0 = M_P * C * C * rho_p          # 常力上界 = m^2 c^3/hbar
    fr = []
    for rr in ["1e-15", "1e-14"]:
        rD = Decimal(rr)
        fr.append(ALPHA * HBAR * C / (rD ** 2))   # 库仑 1/r^2 的力
    ratio_needed = fr[0] / fr[1]                   # 应为 100
    ratio_helix = d(1)                              # 常力定理：不随 r 变
    gap = ratio_needed / ratio_helix
    F("C-01", "三约束互斥（动力学推广）：{v=c 螺旋}{Omega=omega 内禀频率}{F ∝ 1/r^2} 三者不相容",
      "三约束可同时成立",
      "1/r^2 要求 F(1fm)/F(10fm) = %s，而 Omega=omega 常数（⇒ rho、kappa 上界常数）给 %s，缺口 %s 倍"
      % (fx(ratio_needed), fx(ratio_helix), fx(gap)),
      "回链第 7 章三约束互斥定理（v_path=c, u=c, R>0 ⇒ ∅）：本册是它在【力】层面的推广版，"
      "互斥项由「轴向速度=c」换成「力的距离衰减」")
    guard("g-C01", gap > 10, "常力 vs 1/r^2 缺口 > 10 倍", fx(gap))
    res["exclusion"] = {"needed_ratio": fx(ratio_needed), "helix_ratio": fx(ratio_helix), "gap": fx(gap),
                        "F_upper_bound_N": fx(F0)}

    # --- C-02 传播速度 vs 力的大小：F = m*c^2*rho*sqrt(1-beta^2)（beta = u/c）
    cc = float(C)
    rho_f = float(rho_p)
    rows = []
    # 注意：beta → 1 时 1-beta^2 在 float 下会退化成 0（double eps ~2.2e-16），
    # 必须用 Decimal 先算 sqrt(1-beta^2) 再转 float，否则 R=0 导致叉积除零。
    for beta_s in ["0", "0.5", "0.9", "0.99", "0.999999",
                   "0.999999999999999999999999999999"]:
        bD = Decimal(beta_s)
        sq = (Decimal(1) - bD * bD).sqrt()
        beta = float(bD)
        sqf = float(sq)
        kap = rho_f * sqf
        tau = rho_f * beta
        RR = sqf / rho_f
        uu = beta * cc
        Ome = cc * rho_f
        # 机器回代：由 (R,u,Omega) 复算 kappa, tau, 速率
        r1, r2, r3 = helix_derivs(RR, Ome, uu, 0.41)
        cr = vcross(r1, r2)
        kap_chk = vnorm(cr) / (vnorm(r1) ** 3)
        tau_chk = vdot(cr, r3) / (vnorm(cr) ** 2)
        sp_chk = vnorm(r1)
        rows.append({
            "beta": beta, "kappa": kap, "tau": tau, "R": RR,
            "kappa_chk": kap_chk, "tau_chk": tau_chk, "speed_chk": sp_chk,
            "F_over_Fmax": sqf,
        })
    errC2 = 0.0
    for r in rows:
        if r["kappa"] > 0:
            errC2 = max(errC2, rel(r["kappa_chk"], r["kappa"]), rel(r["tau_chk"], r["tau"]))
        errC2 = max(errC2, rel(r["speed_chk"], cc))
    F("C-02", "传播速度–力大小互斥：由 kappa/tau = v_perp/v_par 得 F = m*c^2*rho*sqrt(1-beta^2)",
      "既能以光速传播（beta≈1）又带非零力",
      "beta=0 ⇒ F/Fmax=1（但不传播）；beta=1-1e-30 ⇒ F/Fmax=%.3e；回代残差 %.3e"
      % (rows[-1]["F_over_Fmax"], errC2),
      "**求导硬结论：在 v=c 螺旋框架内，力与传播速度直接互斥**"
      "——引力必须以 c 传播（beta≈1），而 beta→1 时 F→0 ⇒ 该框架承载不了引力")
    guard("g-C02", errC2 < 1e-6 and rows[-1]["F_over_Fmax"] < 1e-14,
          "F ∝ sqrt(1-beta^2) 回代正确且 beta→1 时 F→0", "%.3e / %.3e" % (errC2, rows[-1]["F_over_Fmax"]))
    res["beta_table"] = [{"beta": r["beta"], "F_over_Fmax": "%.6e" % r["F_over_Fmax"],
                          "kappa": "%.6e" % r["kappa"], "R": "%.6e" % r["R"]} for r in rows]

    # --- C-03 牙齿（负向测试）：tau 对力的【零贡献】必须可被检出
    kap_fix = 1.0e12
    taus = [0.1, 0.6, 2.0, 10.0]
    accs, errs = [], []
    for rratio in taus:
        tau_v = kap_fix * rratio
        rho_v = math.hypot(kap_fix, tau_v)
        Om_v = cc * rho_v
        R_v = kap_fix / (kap_fix ** 2 + tau_v ** 2)
        u_v = tau_v * cc / rho_v
        r1, r2, r3 = helix_derivs(R_v, Om_v, u_v, 0.23)
        Bv = vcross(r1, r2)
        B_, _ = vunit(Bv)
        acc = vnorm(r2)
        accs.append(acc)
        errs.append(abs(vdot(r2, B_)) / acc)          # tau 分量归一化应为 0
        errs.append(rel(acc, cc ** 2 * kap_fix))      # |a| 应恒等于 c^2*kappa
    spread = (max(accs) - min(accs)) / max(accs)
    if max(errs) < 1e-9 and spread < 1e-9:
        P("C-03", "牙齿（负向测试）：固定 kappa、tau 跨 %s 倍，加速度大小是否变化" % fx(taus[-1] / taus[0]),
          "|a| = c^2*kappa 与 tau 无关（若有人声称 tau 贡献力，本条会红）",
          "tau/kappa ∈ %s 四条螺旋：|a| 相对极差 %.3e，a·B/|a| ≤ %.3e"
          % (taus, spread, max(errs[0::2])),
          " teeth 生效：tau 对力的贡献被机器判为严格零，且该判定可被推翻（不是恒真断言）")
    else:
        F("C-03", "tau 零贡献牙齿", "0", "%.3e / %.3e" % (spread, max(errs)), "测试自身不成立")
    guard("g-C03", max(errs) < 1e-9 and spread < 1e-9, "tau 零贡献牙齿（可被推翻）",
          "spread=%.3e, aB=%.3e" % (spread, max(errs[0::2])))
    res["tau_teeth"] = {"acc_spread": "%.3e" % spread, "a_dot_B_max": "%.3e" % max(errs[0::2])}

    # --- C-04 层次裁定：本册（3D 求导层恒向心） vs ADD-03（M 空间方向跨度 360°）
    B("C-04", "层次裁定：方向要素在两层上的结论相反，须分层引用",
      "两层结论可统一",
      "求导层（本册 B-03）：3D 力方向恒沿主法向、N·r̂ = -1，零信息；"
      "ADD-03 层：参数流形 (kappa,tau) 上 ƒ̂(θ) 跨度 360°——该跨度来自外加函数 Omega=lambda*cos3θ，非求导所得",
      "两条不矛盾但**不可混用**：把 ADD-03 的 360° 当作「力的方向已由几何导出」会越层；"
      "回链 突破_TUFT-MATH-PROOF-ADD-03_N5方向要素攻坚")

    # --- C-05 汇总：三要素的求导/输入二分账
    P("C-05", "三要素二分账（本册总裁定）", "求导可得项应被明确列出",
      "派生（求导即得）：大小形式 |F|=m*c^2*kappa、方向 N（恒向心）、kappa/tau=v_perp/v_par、"
      "三重奏、逆映射；"
      "外部输入（求导不可得）：kappa 的空间剖型 kappa(r)、耦合系数 alpha、"
      "质量标度（康普顿锚）、有限力程截断、排斥型方向",
      "三要素中【大小与方向的「形式」可导】，【大小的具体数值、方向的可区分性、距离的衰减律】全为输入")

    return res


# ================================================================ D 段 · 量纲审计

def sec_D():
    res = {}
    rows = [
        ("D-01", "|F| = m*c^2*kappa",
         dmul(dmul(D_M, dpow(D_C, 2)), D_KAPPA), D_FORCE, "力"),
        ("D-02", "既有势能式 E = (hbar*c/2)(kappa+tau)",
         dmul(dmul(D_HBAR, D_C), D_KAPPA), D_ENERGY, "能量"),
        ("D-03", "Omega = c*sqrt(kappa^2+tau^2)",
         dmul(D_C, D_KAPPA), D_OMEGA, "角速度"),
        ("D-04", "kappa = alpha*ƛ_C/r^2 = alpha*hbar/(m*c*r^2)",
         dmul(D_HBAR, dpow(dmul(dmul(D_M, D_C), dpow(D_L, 2)), -1)),
         D_KAPPA, "曲率"),
        ("D-05", "jerk 副法向项 c^3*kappa*tau",
         dmul(dpow(D_C, 3), dmul(D_KAPPA, D_KAPPA)),
         dim(1, 0, -3), "加加速度（LT^-3）"),
    ]
    out = []
    n_ok = 0
    for iid, expr, got, want, note in rows:
        ok = (got == want)
        n_ok += 1 if ok else 0
        out.append({"id": iid, "expr": expr, "dim": dstr(got), "want": dstr(want),
                    "ok": ok, "note": note})
        if ok and iid == "D-02":
            P(iid, "量纲审计：" + expr, "应为" + dstr(want), dstr(got) + " ✓ = " + note,
              "**自抓更正**：起稿时手算曾判该式为「动量」并据此断言 F=-grad(E) 少一次求导；"
              "机器兜底（Fraction 指数向量）确认 [hbar*c*kappa] = L^2 M^1 T^-2 = 【能量】，"
              "故 F = -grad(E) 量纲成立（能量/L = 力）。该式量纲层面无罪，"
              "其问题在别处（kappa,tau 的空间剖型为输入），本册不重复判它 FAIL")
        elif ok:
            P(iid, "量纲审计：" + expr, dstr(want), dstr(got) + " ✓", note)
        else:
            F(iid, "量纲审计：" + expr, dstr(want), dstr(got), note)
    res["dim_rows"] = out
    guard("g-D00", n_ok == len(rows), "量纲审计全部通过（%d/%d）" % (n_ok, len(rows)),
          "%d/%d" % (n_ok, len(rows)))
    return res


# ================================================================ 输出

def write_outputs(res_all):
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    counts = {}
    for it in ITEMS:
        counts[it["status"]] = counts.get(it["status"], 0) + 1
    total = len(ITEMS)
    gok = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "title": "四力三要素 · 空间光速螺旋（v=c）全维求导验证",
        "date": "2026-10-08",
        "engine": "源码/四力三要素_空间光速螺旋全维求导验证_2026-10-08.py",
        "counts": counts,
        "total_items": total,
        "guards": {"total": len(GUARDS), "ok": gok},
        "items": ITEMS,
        "guard_list": GUARDS,
        "key_numbers": res_all,
    }
    jpath = os.path.join(OUT_DIR, STEM + ".json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # ---- md
    L = []
    L.append("# 数据 · 四力三要素 · 空间光速螺旋（v=c）全维求导验证（2026-10-08）\n")
    L.append("引擎：`源码/四力三要素_空间光速螺旋全维求导验证_2026-10-08.py`（纯标准库，Decimal 60 位）\n")
    L.append("读数：**条目 %d（%s）｜自检 %d/%d**\n"
             % (total, " / ".join("%s %d" % (k, v) for k, v in sorted(counts.items())), gok, len(GUARDS)))
    L.append("\n## 判定条目\n")
    L.append("| ID | 状态 | 条目 | 期望 | 实测 |")
    L.append("|---|---|---|---|---|")
    for it in ITEMS:
        L.append("| %s | %s | %s | %s | %s |" % (it["id"], it["status"], it["title"], it["expect"], it["actual"]))
    L.append("\n## 自检\n")
    L.append("| ID | 通过 | 描述 | 读数 |")
    L.append("|---|---|---|---|")
    for g in GUARDS:
        L.append("| %s | %s | %s | %s |" % (g["id"], "✓" if g["ok"] else "✗", g["desc"], g["detail"]))
    L.append("\n## 四力反解表（kappa = alpha*ƛ_C/r^2）\n")
    L.append("| 力 | alpha | r (m) | kappa (m^-1) | Omega (s^-1) | R (m) | hbar*Omega (eV) | kappa/rho | 可编码 |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for t in res_all.get("B", {}).get("force_table", []):
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |"
                 % (t["force"], t["alpha"], t["r_m"], t["kappa_m^-1"], t["Omega_s^-1"],
                    t["R_m"], t["hbar_Omega_eV"], t["kappa_over_rho"], "是" if t["encodable"] else "**否**"))
    L.append("\n## 传播速度 β = u/c 与力的互斥\n")
    L.append("| β = u/c | F/F_max = sqrt(1-β²) | kappa (m^-1) | R (m) |")
    L.append("|---|---|---|---|")
    for t in res_all.get("C", {}).get("beta_table", []):
        L.append("| %s | %s | %s | %s |" % (t["beta"], t["F_over_Fmax"], t["kappa"], t["R"]))
    L.append("\n注：ρ = m_p·c/ħ = %s m^-1（质子康普顿波数），F_max = m²c³/ħ。\n"
             % res_all.get("B", {}).get("self_p", {}).get("rho_m^-1", ""))
    mpath = os.path.join(OUT_DIR, STEM + ".md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return jpath, mpath, counts, total, gok


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    res = {}
    res["A"] = sec_A()
    res["B"] = sec_B(res["A"])
    res["C"] = sec_C(res["A"], res["B"])
    res["D"] = sec_D()
    jpath, mpath, counts, total, gok = write_outputs(res)
    print("四力三要素 · 空间光速螺旋全维求导验证（2026-10-08）")
    print("条目 %d：%s" % (total, " / ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))))
    print("自检 %d/%d" % (gok, len(GUARDS)))
    print("json -> %s" % jpath)
    print("md   -> %s" % mpath)
    bad = [g for g in GUARDS if not g["ok"]]
    if bad:
        print("!! 自检未全过：%s" % ", ".join(g["id"] for g in bad))
    return 0


if __name__ == "__main__":
    main()
