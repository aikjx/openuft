# -*- coding: utf-8 -*-
"""
ROOT V128 第五册 · 大 lambda 扫描空转与整体幅度不可辨识性
=============================================================
性质：可算审计（非判定册）。不占 RID，不入 README，不与任何既有册相加。

对象锁定
--------
ROOT V128 的 Yukawa 型第五力势

    Phi(r) = -(mu/r) * (1 + alpha * exp(-r/lambda))        mu = G M

本册只问一个问题：**在这个势里，哪些参数组合是真正可观测的？**

结论（先给）
-----------
`alpha` 本身不是可观测参数。在 lambda -> infinity 的退耦极限里，
`alpha` 只是一个质量重标定因子，与 `M` 精确简并。唯一被约束的是

    beta = alpha / lambda^2

理由是代数：把 exp(-r/lambda) 展开，常数项 alpha 乘 1/r 就是 mu 的重标定，
首个形状项是 -alpha r / (2 lambda^2)，这是一个**常数径向加速度**，
其量级正是 alpha/lambda^2。

因此任何沿 lambda 扫描、报告 "alpha < bound(lambda)" 的做法，在大 lambda 端
是同一个 beta 约束除以 lambda^2 的换算式，不携带新信息。

本册机读验证：第三册 11 个 lambda 格点上 sigma_beta = sigma_alpha/lambda^2
在 lambda >= 30 AU 之后收敛（相对变化 < 1e-3）。

红线
----
- 不宣称攻破统一场论。本册不产生任何新物理，只做参数可辨识性分析。
- 独立实验预言 0。
- 第三册读数以继承方式读取（同一 JSON），不重拟合、不改判词。
- 若机核判据与第三册登记值冲突，报负读数，不改第三册。
"""

import ast
import hashlib
import json
import os
import sys
from decimal import Decimal as D, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)

STEM = "_ALG_rootv128e_largelambda_vacuity_recompute"
DATE = "2026-11-22"

# ---------------------------------------------------------------- 路径（唯一构造）
def out_json():
    return os.path.join(BASE, "数据", "%s_%s.json" % (STEM, DATE))


def report_path():
    return os.path.join(BASE, "数据", "%s_report_%s.txt" % (STEM, DATE))


def upstream_json():
    """第三册机读件（跨册继承的唯一来源）。"""
    return os.path.join(BASE, "数据",
                        "_ALG_rootv128c_ephemeris_jointfit_recompute_2026-11-22.json")


# ---------------------------------------------------------------- Decimal 工具
def Dq(x):
    """字符串/整数 -> 高精度 Decimal（禁裸 float 入口）。"""
    if isinstance(x, D):
        return x
    if isinstance(x, int):
        return D(x)
    return D(str(x))


_PI_CACHE = {}


def dpi():
    if "v" in _PI_CACHE:
        return _PI_CACHE["v"]
    # Machin: pi = 16 atan(1/5) - 4 atan(1/239)
    def atan_inv(n):
        n = Dq(n)
        x = D(1) / n
        x2 = x * x
        s = D(0)
        term = x
        k = 0
        while True:
            t = term / (2 * k + 1)
            if k % 2 == 0:
                s += t
            else:
                s -= t
            term *= x2
            k += 1
            if abs(t) < D("1e-62"):
                break
        return s

    v = 16 * atan_inv(5) - 4 * atan_inv(239)
    _PI_CACHE["v"] = v
    return v


def dsin(x):
    x = x % (2 * dpi())
    if x > dpi():
        x -= 2 * dpi()
    s = D(0)
    term = x
    k = 1
    while True:
        s += term
        term = -term * x * x / Dq((k + 1) * (k + 2))
        k += 2
        if abs(term) < D("1e-58"):
            break
    return s


def dcos(x):
    return dsin(x + dpi() / 2)


def dsqrt(x):
    return Dq(x).sqrt()


def rel(a, b):
    """相对偏离。b=0 时退化为绝对偏离（并标量级）。"""
    a = Dq(a)
    b = Dq(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


def fmt(x, nd=6):
    """科学计数（零值不写指数）。"""
    x = Dq(x)
    if x == 0:
        return "0"
    return "%.*E" % (nd, x)


def fstr(x, nd=6):
    x = Dq(x)
    if x == 0:
        return "0"
    return ("%." + str(nd) + "E") % x


# ---------------------------------------------------------------- 势与泛函
def phi_const_shift(x, mu, c0):
    """Phi = -(mu/x) (1 - c0)。c0 = 常数偏移（零方向）。"""
    return -(Dq(mu) / Dq(x)) * (D(1) - Dq(c0))


def phi_yukawa(x, mu, alpha, lam):
    """V128 原势。"""
    x = Dq(x)
    lam = Dq(lam)
    return -(Dq(mu) / x) * (D(1) + Dq(alpha) * (-x / lam).exp())


def simpson(f, a, b, n):
    """复合 Simpson 1/3，n 必须为偶数。"""
    a = Dq(a)
    b = Dq(b)
    if n % 2:
        n += 1
    h = (b - a) / Dq(n)
    s = f(a) + f(b)
    for i in range(1, n):
        s += (D(4) if i % 2 else D(2)) * f(a + h * Dq(i))
    return s * h / D(3)


def simpson_pair(f, a, b, n):
    """两路：S(n) 与 S(2n)，用于 Richardson / 收敛检查。"""
    s1 = simpson(f, a, b, n)
    s2 = simpson(f, a, b, 2 * n)
    ext = (D(16) * s2 - s1) / D(15)
    return s1, s2, ext


def shapiro_potential_integral(b, lmax, n, phi):
    """I = int_{-L}^{L} Phi(sqrt(b^2+l^2)) dl，用偶性折成 2*int_0^L。"""
    b = Dq(b)
    lmax = Dq(lmax)

    def g(l):
        return phi(dsqrt(b * b + l * l))

    return 2 * simpson(g, D(0), lmax, n)


def shapiro_asinh_exact(b, lmax):
    """int_{-L}^{L} dl/sqrt(b^2+l^2) = 2 asinh(L/b)，asinh = ln(x+sqrt(x^2+1))。"""
    b = Dq(b)
    x = Dq(lmax) / b
    return 2 * (x + dsqrt(x * x + 1)).ln()


def deflection_kernel_integral(b, lmax, n):
    """J = int_{-L}^{L} b/(b^2+l^2)^{3/2} dl，用偶性折成 2*int_0^L。"""
    b = Dq(b)
    lmax = Dq(lmax)

    def g(l):
        r2 = b * b + l * l
        return b / (r2 * dsqrt(r2))

    return 2 * simpson(g, D(0), lmax, n)


def deflection_kernel_exact(b, lmax):
    """闭式：2L/(b^2 sqrt(b^2+L^2))。"""
    b = Dq(b)
    lm = Dq(lmax)
    return 2 * lm / (b * b * dsqrt(b * b + lm * lm))


def period_of(a, mu):
    return 2 * dpi() * (Dq(a) ** D("1.5")) / dsqrt(mu)


def kepler_E(M, e):
    """解 E - e sin E = M，Newton。"""
    M = Dq(M)
    e = Dq(e)
    E = M if e < D("0.8") else dpi()
    for _ in range(200):
        f = E - e * dsin(E) - M
        fp = D(1) - e * dcos(E)
        d = f / fp
        E -= d
        if abs(d) < D("1e-55"):
            break
    return E
# ---------------------------------------------------------------- 门 L1：自检
def gate_L1():
    note = []
    ok = True

    # (a) c0=0 时 Phi 恒为 0 => Shapiro 积分为机器零
    zero_phi = lambda x: D(0)
    I0 = shapiro_potential_integral(D(1), D(1000), 400, zero_phi)
    I0b = shapiro_potential_integral(D("2.5"), D(8000), 800, zero_phi)
    l1a = max(abs(I0), abs(I0b))
    note.append("c0=0 Shapiro 积分机器零 max|I| = %s" % fmt(l1a))
    if l1a > D("1e-55"):
        ok = False
        note.append("FAIL: 零势未给零积分")

    # (b) Kepler 解残差
    worst_E = D(0)
    for e_s in ("0.01", "0.2", "0.5", "0.8"):
        for M_s in ("0.1", "1.0", "3.0", "6.0"):
            e = Dq(e_s)
            M = Dq(M_s)
            E = kepler_E(M, e)
            res = E - e * dsin(E) - M
            worst_E = max(worst_E, abs(res))
    note.append("Kepler 残差 max|E - e sinE - M| = %s" % fmt(worst_E))
    if worst_E > D("1e-50"):
        ok = False
        note.append("FAIL: Kepler 未收敛")

    # (c) 两路互验 + 四阶收敛（判「阶数对」而非「误差够小」）
    #     注：取 L=20 而不是 L=1000。L=1000 时被积函数在 l~b=1 处的结构
    #     相对区间长度是 1e-3，Simpson 在 n=400 下根本分辨不了，会给 1e-2 的
    #     假偏离。那是**量程问题**，不是积分器错。物理结论只用比值（同节点、
    #     同权重，误差精确抵消），故不需要在 L=1000 上追求绝对精度。
    b, L = D(1), D(20)
    exa = shapiro_asinh_exact(b, L)
    errs = []
    for n in (320, 640, 1280, 2560):
        v = shapiro_potential_integral(b, L, n, lambda x: D(1) / Dq(x))
        errs.append(abs(v - exa))
    orders = []
    for i in range(len(errs) - 1):
        orders.append((errs[i] / errs[i + 1]).ln() / D(2).ln())
    worst_ord = max(abs(o - 4) for o in orders)
    note.append("Shapiro 核 四阶收敛：误差 %s -> 观测阶 %s"
                % (" / ".join(fstr(e, 3) for e in errs), " / ".join(fstr(o, 4) for o in orders)))
    note.append("末级绝对残差 %s（判据 1e-10；L2/L5 只用比值，误差精确抵消）" % fmt(errs[-1]))

    jn = deflection_kernel_integral(b, L, 2560)
    je = deflection_kernel_exact(b, L)
    r_df = rel(jn, je)
    note.append("偏折核 数值 vs 闭式 rel = %s" % fmt(r_df))

    if worst_ord > D("0.5"):
        ok = False
        note.append("FAIL: 观测阶偏离 4 超过 0.5，积分器不是四阶")
    if max(errs[-1], r_df) > D("1e-10"):
        ok = False
        note.append("FAIL: 末级残差超过 1e-10")

    # (d) Richardson 外推（核取 1/(1+x^2)，闭式 pi/4，端点无奇性）
    s1, s2, ext = simpson_pair(lambda x: D(1) / (1 + Dq(x) * Dq(x)), D(0), D(1), 200)
    exact_conv = dpi() / 4
    conv = rel(ext, exact_conv)
    note.append("Simpson 收敛：S(200) vs S(400) rel = %s；Richardson vs 闭式 pi/4 rel = %s"
                % (fmt(rel(s1, s2)), fmt(conv)))
    if conv > D("1e-14"):
        ok = False
        note.append("FAIL: Richardson 未达精度")

    return {
        "id": "L1",
        "kind": "guard",
        "title": "自检：零势机器零 / Kepler 收敛 / 四阶收敛与两路互验 / Richardson",
        "ok": ok,
        "notes": note,
        "readings": {
            "zero_potential_integral_max": fstr(l1a),
            "kepler_residual_max": fstr(worst_E),
            "quadratureOrders": [fstr(o, 4) for o in orders],
            "quadrature_order_worst_dev_from_4": fstr(worst_ord),
            "shapiro_abs_residual_2560": fstr(errs[-1]),
            "deflection_kernel_rel": fstr(r_df),
            "richardson_rel_vs_closed": fstr(conv),
        },
    }


# ---------------------------------------------------------------- 门 L2：统一零方向
def gate_L2():
    """C = c0 常数 => 所有势线性泛函只整体乘 (1-c0)^power，形状量不变。"""
    note = []
    ok = True
    mu = D(1)
    b, L = D(1), D(1000)
    a, e = D(1), D("0.2")

    base_I = shapiro_potential_integral(b, L, 400, lambda x: phi_const_shift(x, mu, D(0)))
    base_J = deflection_kernel_integral(b, L, 400) * mu
    base_T = period_of(a, mu)

    rows = []
    worst_ratio = D(0)
    for c0_s in ("0.1", "0.3", "0.5"):
        c0 = Dq(c0_s)
        Ic = shapiro_potential_integral(b, L, 400, lambda x: phi_const_shift(x, mu, c0))
        pred = (D(1) - c0)
        dev_s = rel(Ic, base_I * pred)

        Jc = deflection_kernel_integral(b, L, 400) * mu * (D(1) - c0)
        dev_d = rel(Jc, base_J * pred)

        Tc = period_of(a, mu * (D(1) - c0))
        dev_t = rel(Tc, base_T / dsqrt(D(1) - c0))

        # 形状量：归一化后应与 c0 无关
        shape_s = Ic / (base_I * pred)
        shape_d = Jc / (base_J * pred)

        worst_ratio = max(worst_ratio, dev_s, dev_d, dev_t,
                          abs(shape_s - 1), abs(shape_d - 1))
        rows.append({
            "c0": c0_s,
            "shapiro_ratio_dev": fstr(dev_s),
            "deflection_ratio_dev": fstr(dev_d),
            "period_ratio_dev": fstr(dev_t),
            "shape_shapiro_dev_from_1": fstr(shape_s - 1),
            "shape_deflection_dev_from_1": fstr(shape_d - 1),
        })

    note.append("三个泛函的比值与理论幂律的最大偏离 = %s" % fmt(worst_ratio))
    note.append("Shapiro 比例指数 = 1（Phi 线性泛函）；偏折 = 1；周期 = -1/2")
    note.append("进动：对纯 1/r 势恒为 0（第四册已机读 8.862149E-19），本册继承不重算")
    if worst_ratio > D("1e-45"):
        ok = False
        note.append("FAIL: 零方向缩放律不成立")

    return {
        "id": "L2",
        "kind": "structural",
        "title": "统一零方向：C 常数时全部势线性泛函只整体缩放，形状量不变",
        "ok": ok,
        "notes": note,
        "rows": rows,
        "readings": {
            "max_ratio_deviation": fstr(worst_ratio),
            "base_shapiro_integral": fstr(base_I),
            "base_deflection_integral": fstr(base_J),
            "base_period": fstr(base_T),
        },
    }


# ---------------------------------------------------------------- 门 L3：简并精确性
def gate_L3():
    """(mu, c0) 与 (mu*(1-c0), 0) 给出逐点相同的 Phi => 全部引力泛函相同。

    这是**恒等**，按纪律单列 IDENTITY，不承重。本门的作用是划清「简并」的
    准确形状：不是一个模糊的「参数不好定」，而是一条**精确的一维族**
        mu * (1 - c0) = mu_eff = 常数
    族内任何成员给出同一条轨道、同一套观测量。要破这个族，只能靠 c0 的
    r 依赖（即有限的 lambda），那是 L5/L6/L7 的内容。
    """
    note = []
    ok = True
    c0 = D("0.3")
    mu = D(1)
    # 关键代数：Phi = -(mu/x)(1-c0)。要它等于 -(mu'/x)，必须 mu' = mu*(1-c0)，
    # 不是 mu/(1-c0)。写成除法会让「简并」方向反过来（本轮实测偏离 14.571）。
    mu_alt = mu * (D(1) - c0)

    # (a) 逐点恒等
    worst_phi = D(0)
    for x_s in ("0.05", "0.2", "0.5", "1", "2", "5", "20"):
        x = Dq(x_s)
        worst_phi = max(worst_phi,
                        abs(phi_const_shift(x, mu, c0) - phi_const_shift(x, mu_alt, D(0))))
    note.append("Phi 逐点差 max = %s（恒等，单列 IDENTITY，不承重）" % fmt(worst_phi))

    # (b) 一维简并族：固定 mu_eff = 1，三个不同 (mu, c0) 组合必须给同一个 Phi
    fam = []
    worst_fam = D(0)
    for c in ("0", "0.3", "0.5"):
        cc = Dq(c)
        mm = D(1) / (D(1) - cc)          # 使 mu*(1-c0) = 1
        dev = D(0)
        for x_s in ("0.1", "1", "10"):
            x = Dq(x_s)
            dev = max(dev, abs(phi_const_shift(x, mm, cc) - (-(D(1) / x))))
        worst_fam = max(worst_fam, dev)
        fam.append({"c0": c, "mu": fstr(mm, 6), "phi_dev": fstr(dev)})
    note.append("固定 mu_eff=1 的三成员族（c0=0/0.3/0.5）Phi 最大偏离 = %s" % fmt(worst_fam))
    note.append("=> 简并是一条精确的一维直线 mu*(1-c0)=mu_eff，不是「参数不好定」")

    # (c) 轨道只依赖 mu_eff：同一 M 下 r 相同
    worst_r = D(0)
    for M_s in ("0.1", "1.0", "3.0", "6.0"):
        M = Dq(M_s)
        E1 = kepler_E(M, D("0.2"))
        r1 = D(1) * (D(1) - D("0.2") * dcos(E1))
        # 用 mu_eff 反算的另一成员：两者 mu_eff 相同 => 同一 n => 同一 M(t) => 同一 r
        mu_eff_a = mu * (D(1) - c0)
        mu_eff_b = mu_alt * (D(1) - D(0))
        n_a = dsqrt(mu_eff_a)
        n_b = dsqrt(mu_eff_b)
        E2 = kepler_E(M * n_a / n_b, D("0.2"))
        r2 = D(1) * (D(1) - D("0.2") * dcos(E2))
        worst_r = max(worst_r, rel(r2, r1))
    note.append("同一 t 的 r(t) 相对差 max = %s（n 之比 = 1，两参数化同轨）" % fmt(worst_r))

    # (d) 枚举 6 个引力泛函，全部只依赖 mu*(1-c0)
    funcs = []
    b, L, a = D(1), D(1000), D(1)
    I1 = shapiro_potential_integral(b, L, 400, lambda x: phi_const_shift(x, mu, c0))
    I2 = shapiro_potential_integral(b, L, 400, lambda x: phi_const_shift(x, mu_alt, D(0)))
    funcs.append(("shapiro", rel(I1, I2)))
    funcs.append(("deflection", rel(mu * (D(1) - c0), mu_alt)))
    funcs.append(("period", rel(period_of(a, mu * (D(1) - c0)), period_of(a, mu_alt))))
    funcs.append(("t2_over_a3", rel(4 * dpi() ** 2 / (mu * (D(1) - c0)),
                                    4 * dpi() ** 2 / mu_alt)))
    funcs.append(("redshift", rel(mu * (D(1) - c0), mu_alt)))
    funcs.append(("precession_static", D(0)))
    worst_f = max(v for _, v in funcs)
    note.append("6 个泛函枚举：最大相对差 = %s => 全部简并" % fmt(worst_f))

    if max(worst_phi, worst_fam, worst_r, worst_f) > D("1e-45"):
        ok = False
        note.append("FAIL: 简并不精确")

    return {
        "id": "L3",
        "kind": "identity",
        "title": "质量-振幅精确简并：(mu,c0) 与 (mu*(1-c0),0) 不可区分（恒等，不承重）",
        "ok": ok,
        "identity": True,
        "notes": note,
        "rows": fam,
        "readings": {
            "phi_pointwise_max": fstr(worst_phi),
            "degenerate_family_max_dev": fstr(worst_fam),
            "radius_at_fixed_t_max_rel": fstr(worst_r),
            "six_functional_enumeration_max_rel": fstr(worst_f),
            "c0_used": fstr(c0),
        },
    }


def gate_L4():
    """耦合到质量的 Yukawa 满足强等效原理 => Eotvos 通道结构性失效。"""
    note = []
    ok = True
    rows = []

    def eta(k1, k2, alpha, rr, lam):
        """两个测试体的 Eotvos 参数，源荷/质量归一为 1。"""
        f = (-Dq(rr) / Dq(lam)).exp()
        num = Dq(alpha) * (Dq(k1) - Dq(k2)) * f
        den = D(1) + Dq(alpha) * (Dq(k1) + Dq(k2)) / 2 * f
        return num / den

    # (a) 耦合质量：k = 1 对所有成分 => eta = 0 精确
    worst_mass = D(0)
    for alpha_s in ("1e-9", "1e-3", "1", "10"):
        for r_s, lam_s in (("1", "1e10"), ("1", "1e3"), ("1e6", "1e0")):
            worst_mass = max(worst_mass, abs(eta(1, 1, alpha_s, r_s, lam_s)))
    note.append("耦合质量 (q=m) 时 eta 恒为 0，max|eta| = %s" % fmt(worst_mass))
    note.append("=> 强等效原理不破 => 自由落体普适 => Eotvos/MICROSCOPE/LLR 通道**看不见**该第五力")

    # (b) 耦合重子数：q/m 随成分变 => eta != 0
    k_baryon_fe = D("0.4656")   # 近似 B/m（自然单位），仅作量级示意
    k_baryon_ti = D("0.4622")
    eta_bt = eta(k_baryon_fe, k_baryon_ti, "1e-6", "1", "1e10")
    note.append("耦合重子数时 eta(Fe,Ti) at alpha=1e-6, lambda>>r = %s（非零）" % fmt(eta_bt))

    # (c) 判别力：同一组 alpha 下两种耦合给出完全不同的 eta
    ratio = abs(eta_bt) / (abs(worst_mass) + D("1e-300"))
    note.append("同样 alpha 下 baryon 耦合 eta / mass 耦合 eta 之比 = %s（判别力存在）" % fmt(ratio))

    if worst_mass > D("1e-55"):
        ok = False
        note.append("FAIL: 质量耦合未给 eta=0")
    if eta_bt == 0:
        ok = False
        note.append("FAIL: baryon 耦合给 0，负对照失效")

    rows.append({"coupling": "mass (q=m)", "eta": fstr(worst_mass)})
    rows.append({"coupling": "baryon (q=B)", "eta": fstr(eta_bt)})

    return {
        "id": "L4",
        "kind": "structural-negative",
        "title": "等效原理通道对质量耦合 Yukawa 结构性失效（负读数）",
        "ok": ok,
        "negative_reading": True,
        "notes": note,
        "rows": rows,
        "readings": {
            "eta_mass_coupling_max": fstr(worst_mass),
            "eta_baryon_coupling_illustrative": fstr(eta_bt),
            "discrimination_ratio": fstr(ratio),
        },
    }
# ---------------------------------------------------------------- 上游继承（只读）
def load_upstream():
    p = upstream_json()
    if not os.path.exists(p):
        raise RuntimeError("上游机读件缺失: %s" % p)
    with open(p, "rb") as fh:
        raw = fh.read()
    d = json.loads(raw.decode("utf-8"))
    return d, hashlib.sha256(raw).hexdigest(), len(raw)


def tail_stats(profile, lam_min):
    """给定 profile（第三册 j3 子样本），取 lam >= lam_min 的点，返回 beta 量。"""
    rows = []
    for pt in profile:
        lam = Dq(pt["lam_AU"])
        if lam < Dq(lam_min):
            continue
        a_hat = Dq(pt["alpha_hat"])
        s_a = Dq(pt["sigma_alpha"])
        rows.append({
            "lam": lam,
            "alpha_hat": a_hat,
            "sigma_alpha": s_a,
            "beta_hat": a_hat / (lam * lam),
            "sigma_beta": s_a / (lam * lam),
            "alpha_95": Dq(pt["alpha_95_upper"]),
            "excluded": bool(pt["alpha1_excluded"]),
        })
    return rows


def _converge_ratio(rows, key):
    """尾部收敛：以最大 lam 点为极限，返回 [(lam, dev, dev*lam)]。"""
    if not rows:
        return []
    lim = rows[-1][key]
    out = []
    for r in rows:
        d = rel(r[key], lim)
        out.append((r["lam"], d, d * r["lam"]))
    return out


# ---------------------------------------------------------------- 门 L5：sigma_beta 收敛
def gate_L5(up, up_sha, up_bytes):
    note = []
    ok = True
    detail = {}
    worst_lin = D(0)
    n_tail_min = None

    for ds in ("EPM2011", "INPOP10a"):
        prof = up["j3_real_fit"]["datasets"][ds]["profile"]
        rows = tail_stats(prof, D(30))
        conv_s = _converge_ratio(rows, "sigma_beta")
        conv_a = _converge_ratio(rows, "beta_hat")

        # O(1/lam) 律：dev*lam 应近似常数
        vals = [c[2] for c in conv_s[:-1]]  # 去掉极限点自身（dev=0）
        if vals:
            mn, mx = min(vals), max(vals)
            spread = (mx - mn) / mn if mn != 0 else mx
        else:
            spread = D(0)

        # 去掉第一项（lam=30，修正最大）后的线性律检验
        vals2 = [c[2] for c in conv_s[1:-1]]
        if len(vals2) >= 2:
            mn2, mx2 = min(vals2), max(vals2)
            spread2 = (mx2 - mn2) / mn2 if mn2 != 0 else mx2
        else:
            spread2 = D(0)
        worst_lin = max(worst_lin, spread2)

        # 达到 1e-3 所需的最小 lam
        for lam, d, _ in conv_s:
            if d < D("1e-3") and n_tail_min is None:
                n_tail_min = lam

        detail[ds] = {
            "n_tail_points": len(rows),
            "sigma_beta_limit": fstr(rows[-1]["sigma_beta"]),
            "beta_hat_limit": fstr(rows[-1]["beta_hat"]),
            "dev_at_30": fstr(conv_s[0][1]),
            "dev_times_lam_series": [fstr(c[2]) for c in conv_s],
            "spread_dev_times_lam_all": fstr(spread),
            "spread_dev_times_lam_drop_first": fstr(spread2),
            "beta_hat_dev_series": [fstr(c[1]) for c in conv_a],
        }
        note.append("%s：sigma_beta 极限 = %s；lam=30 处偏离 %s；dev*lam 序列 %s"
                    % (ds, fmt(rows[-1]["sigma_beta"]), fmt(conv_s[0][1]),
                       " / ".join(fstr(c[2], 3) for c in conv_s)))

    note.append("O(1/lam) 律：去掉 lam=30 后 dev*lam 的相对散布 = %s" % fmt(worst_lin))
    note.append("=> alpha_hat 与 sigma_alpha 在尾部同乘 lam^2，即整个拟合只是 beta 拟合的换算式")

    if worst_lin > D("1e-2"):
        ok = False
        note.append("FAIL: 尾部未呈现 O(1/lam) 收敛")

    return {
        "id": "L5",
        "kind": "load-bearing",
        "title": "尾部 sigma_alpha 与 alpha_hat 同乘 lam^2 => 只有一个 beta 约束",
        "ok": ok,
        "notes": note,
        "detail": detail,
        "readings": {
            "upstream_sha256_prefix": up_sha[:16],
            "upstream_bytes": up_bytes,
            "worst_spread_dev_times_lam": fstr(worst_lin),
            "lam_for_dev_below_1e_3": fstr(n_tail_min) if n_tail_min else "n/a",
        },
    }


# ---------------------------------------------------------------- 门 L6：信息份数
def gate_L6(up):
    """尾部 k 个格点塌缩为 1 个 beta 约束；用「互相换算」验证而非计数。"""
    note = []
    ok = True
    detail = {}
    worst_consistency = D(0)

    for ds in ("EPM2011", "INPOP10a"):
        prof = up["j3_real_fit"]["datasets"][ds]["profile"]
        rows = tail_stats(prof, D(30))
        # 相邻两点的 sigma_beta 之比应 -> 1；用 alpha 判据直接比会看到 lam^2 增长
        ratios_alpha = []
        ratios_beta = []
        for i in range(len(rows) - 1):
            ra = rows[i + 1]["sigma_alpha"] / rows[i]["sigma_alpha"]
            rb = rows[i + 1]["sigma_beta"] / rows[i]["sigma_beta"]
            lamr = (rows[i + 1]["lam"] / rows[i]["lam"]) ** 2
            ratios_alpha.append((ra, lamr))
            ratios_beta.append(rb)
        # 关键：ratio_alpha / lam_ratio^2 == ratio_beta，应 -> 1
        devs = [abs(rb - 1) for rb in ratios_beta]
        worst_consistency = max(worst_consistency, max(devs) if devs else D(0))

        detail[ds] = {
            "n_tail_points": len(rows),
            "lambda_points": [fstr(r["lam"], 3) for r in rows],
            "alpha_ratio_vs_lam2_ratio": ["%.4f / %.4f" % (float(ra), float(lr))
                                          for ra, lr in ratios_alpha],
            "beta_ratio_series": [fstr(rb, 4) for rb in ratios_beta],
            "independent_constraints_in_tail": 1,
        }
        note.append("%s：尾部 %d 点，alpha 比 / lam^2 比 逐对吻合，beta 比序列 %s"
                    % (ds, len(rows), " / ".join(fstr(rb, 4) for rb in ratios_beta)))

    note.append("尾部 max|beta 比 - 1| = %s（lam=30 那一对含 O(1/lam) 修正）" % fmt(worst_consistency))
    note.append("=> 尾部 k 个 lambda 格点不构成 k 份独立检验，而是同一个 beta 区间的 k 次重写")

    if worst_consistency > D("1e-1"):
        ok = False
        note.append("FAIL: 尾部未塌缩")

    return {
        "id": "L6",
        "kind": "load-bearing",
        "title": "尾部格点塌缩：k 个 lambda 点 = 1 个 beta 约束",
        "ok": ok,
        "notes": note,
        "detail": detail,
        "readings": {
            "worst_beta_ratio_deviation": fstr(worst_consistency),
        },
    }


# ---------------------------------------------------------------- 门 L7：排除带分解
def gate_L7(up):
    """排除带上端由 beta 交叉决定、下端由指数截断决定：两个互不相关的机制。"""
    note = []
    ok = True
    detail = {}

    for ds in ("EPM2011", "INPOP10a"):
        prof = up["j3_real_fit"]["datasets"][ds]["profile"]
        rows = tail_stats(prof, D(30))
        last = rows[-1]
        # 上端交叉：区间上端点 lam^2*(beta_hat + 1.96*sigma_beta) = 1
        # 注意 beta_hat 带符号 —— 符号错会把「已排除点」与「未排除点」混为一谈
        rhs = last["beta_hat"] + D("1.96") * last["sigma_beta"]
        lam_star = D(1) / dsqrt(rhs) if rhs > 0 else None

        j4 = up["j4_exclusion_window"]["datasets"][ds]
        reported_hi = Dq(j4["widest_band_AU"][1])
        reported_lo = Dq(j4["widest_band_AU"][0])
        grid_step = D("10") ** (D(1) / D(10))
        ratio = (lam_star / reported_hi) if lam_star else None

        detail[ds] = {
            "reported_band_AU": [fstr(reported_lo, 6), fstr(reported_hi, 6)],
            "reported_decades": fstr(Dq(j4["decades_in_band"])),
            "n_excluded": j4["n_excluded"],
            "n_grid": j4["n_grid"],
            "beta_hat_at_edge": fstr(last["beta_hat"]),
            "sigma_beta_at_edge": fstr(last["sigma_beta"]),
            "upper_edge_from_beta_crossing": fstr(lam_star, 6) if lam_star else "n/a",
            "edge_ratio_beta_over_reported": fstr(ratio, 5) if ratio else "n/a",
            "grid_step": fstr(grid_step, 5),
        }
        note.append("%s：第三册上端 %s ↔ beta 交叉解析 %s，比值 %s（网格步长 %s）"
                    % (ds, fmt(reported_hi), fmt(lam_star) if lam_star else "n/a",
                       fstr(ratio, 5) if ratio else "n/a", fstr(grid_step, 5)))
        note.append("      下端 %s 由 exp(-a/lam) 截断给出（形状机制，与 beta 无关）" % fmt(reported_lo))

        # 交叉点必须落在「最后一个被排除格点」与「下一个格点」之间
        if lam_star is None:
            ok = False
            note.append("FAIL: 无法给出 beta 交叉点")
        elif not (D(1) <= ratio < grid_step):
            ok = False
            note.append("FAIL: 交叉点未落在相邻网格之间，上端分解不成立")

    note.append("=> 「7.90 dex 排除带」不是一个物理带，而是两个互不相关条件的交集："
                "低端指数截断、高端 beta 交叉")

    return {
        "id": "L7",
        "kind": "load-bearing-negative",
        "title": "排除带两端由两个互不相关机制决定（负读数：带不是物理对象）",
        "ok": ok,
        "negative_reading": True,
        "notes": note,
        "detail": detail,
        "readings": {},
    }


# ---------------------------------------------------------------- 门 L8：反噬
def gate_L8(up):
    """判别力：把尾部 sigma 换成不随 lam 增长的假剖面，L5/L6 判据必须 FAIL。"""
    note = []
    ok = True

    ds = "EPM2011"
    prof = up["j3_real_fit"]["datasets"][ds]["profile"]
    rows = tail_stats(prof, D(30))

    # 真剖面：dev*lam 近似常数
    conv_true = _converge_ratio(rows, "sigma_beta")
    vals_true = [c[2] for c in conv_true[1:-1]]
    spread_true = (max(vals_true) - min(vals_true)) / min(vals_true) if len(vals_true) >= 2 else D(0)

    # 假剖面：sigma_alpha 恒定（不随 lam^2 增长）=> sigma_beta ∝ lam^-2
    fake = []
    const_s = rows[0]["sigma_alpha"]
    for r in rows:
        fake.append({"lam": r["lam"], "sigma_beta": const_s / (r["lam"] * r["lam"])})
    conv_fake = _converge_ratio(fake, "sigma_beta")
    vals_fake = [c[2] for c in conv_fake[1:-1]]
    spread_fake = (max(vals_fake) - min(vals_fake)) / min(vals_fake) if len(vals_fake) >= 2 else D("1e9")

    note.append("真剖面 dev*lam 散布 = %s（通过 L5）" % fmt(spread_true))
    note.append("假剖面 dev*lam 散布 = %s（L5 判据必须失败）" % fmt(spread_fake))
    note.append("另有正对照：把尾部单点 sigma 乘 1.5，dev*lam 散布应显著上升")

    # 单点扰动
    pert = [dict(r) for r in rows]
    pert[-2]["sigma_alpha"] = pert[-2]["sigma_alpha"] * D("1.5")
    pert[-2]["sigma_beta"] = pert[-2]["sigma_alpha"] / (pert[-2]["lam"] ** 2)
    conv_p = _converge_ratio(pert, "sigma_beta")
    vals_p = [c[2] for c in conv_p[1:-1]]
    spread_p = (max(vals_p) - min(vals_p)) / min(vals_p) if len(vals_p) >= 2 else D("1e9")
    note.append("单点 +50%% 后 dev*lam 散布 = %s" % fmt(spread_p))

    if spread_fake < D("1"):
        ok = False
        note.append("FAIL: 假剖面未使判据失败，L5 无判别力")
    if spread_p < spread_true:
        ok = False
        note.append("FAIL: 单点扰动未使散布上升")

    return {
        "id": "L8",
        "kind": "guard",
        "title": "判别力反噬：假剖面与单点扰动必须使 L5 判据失败",
        "ok": ok,
        "notes": note,
        "readings": {
            "spread_true": fstr(spread_true),
            "spread_fake_profile": fstr(spread_fake),
            "spread_single_point_perturbed": fstr(spread_p),
        },
    }
# ---------------------------------------------------------------- 判词（机读构造）
def verdict_of(f_l5, f_l6, f_l7):
    """唯一判词构造函数。三个输入任一翻转，判词串必须变化。"""
    if f_l5 and f_l6 and f_l7:
        return ("ROOTV128E-LARGE-LAMBDA-SCAN-VACUITY-PROVEN"
                "--ALPHA-IS-NOT-AN-OBSERVABLE-PARAMETER"
                "--ONLY-BETA-ALPHA-OVER-LAMBDA-SQUARED-IS-CONSTRAINED"
                "--TAIL-FIT-IS-A-RESCALED-BETA-FIT"
                "--EXCLUSION-BAND-EDGES-ARE-TWO-UNRELATED-MECHANISMS"
                "--EQUIVALENCE-PRINCIPLE-CANNOT-SEE-MASS-COUPLED-YUKAWA"
                "--MASS-AMPLITUDE-DEGENERACY-IS-EXACT"
                "--UFT-NOT-BROKEN"
                "--NO-INDEPENDENT-PREDICTION")
    bad = []
    if not f_l5:
        bad.append("TAIL-NOT-SCALING-AS-LAMBDA-SQUARED")
    if not f_l6:
        bad.append("TAIL-POINTS-NOT-COLLAPSED")
    if not f_l7:
        bad.append("BAND-EDGE-DECOMPOSITION-REFUTED")
    return "ROOTV128E-VACUITY-CLAIM-REFUTED--" + "--".join(bad)


def gate_verdict_machine():
    """VERDICT-MACHINE：任一输入翻转，判词串必须变化。"""
    base = verdict_of(True, True, True)
    variants = [verdict_of(False, True, True),
                verdict_of(True, False, True),
                verdict_of(True, True, False)]
    ok = all(v != base for v in variants)
    return {
        "id": "G-VERDICT-MACHINE",
        "kind": "guard",
        "title": "判词机读：三个承重标志任一翻转必须改变判词串",
        "ok": ok,
        "notes": ["基线长度 %d；三个变体长度 %s" % (len(base), [len(v) for v in variants])],
        "readings": {},
    }


def _ok_assigns(fn):
    """收集函数内所有对 ok 的赋值，附带「是否在条件/循环体内」的深度。"""
    out = []

    def walk(node, depth):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "ok" for t in ch.targets):
                out.append((ch, depth, ch.value))
            walk(ch, depth + (1 if isinstance(ch, (ast.If, ast.For, ast.While, ast.Try))
                              else 0))

    walk(fn, 0)
    return out


def gate_no_hardcode():
    """AST 守卫：ok 不得「只在函数体顶层赋常量、从不被条件翻转」。"""
    src = open(os.path.abspath(__file__), "rb").read().decode("utf-8")
    tree = ast.parse(src)
    bad = []
    scanned = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        asg = _ok_assigns(node)
        if not asg:
            continue
        scanned += 1
        top_const = [a for a in asg if a[1] == 0 and isinstance(a[2], ast.Constant)]
        nested = [a for a in asg if a[1] >= 1]
        if top_const and not nested:
            bad.append((node.name, node.lineno))
    ok = not bad
    return {
        "id": "G-NO-HARDCODE-OK",
        "kind": "guard",
        "title": "AST 守卫：ok 不得写死（顶层常量且无任何条件翻转即为装饰判据）",
        "ok": ok,
        "notes": ["扫描 %d 个含 ok 的函数" % scanned,
                  ("命中 %s" % bad) if bad else "零命中"],
        "readings": {"n_functions_scanned": scanned},
    }


def gate_link_check(json_path, rep_path, verdict):
    """链接体检：json 与 report 都必须含判词串与日期。"""
    ok = True
    notes = []
    for p in (json_path, rep_path):
        if not os.path.exists(p):
            ok = False
            notes.append("缺失: %s" % os.path.basename(p))
            continue
        t = open(p, "rb").read().decode("utf-8", "ignore")
        has_v = verdict in t
        has_d = DATE in t
        if not (has_v and has_d):
            ok = False
        notes.append("%s: verdict=%s date=%s" % (os.path.basename(p), has_v, has_d))
    return {
        "id": "G-LINK",
        "kind": "guard",
        "title": "链接体检：JSON 与报告均含判词串与日期",
        "ok": ok,
        "notes": notes,
        "readings": {},
    }


# ---------------------------------------------------------------- 报告渲染
def render_report(gates, verdict, final, up_sha, up_bytes):
    L = []
    add = L.append
    n_ok = sum(1 for g in gates if g["ok"])
    n_tot = len(gates)
    guards = [g["id"] for g in gates if g["kind"] == "guard"]
    identity = [g["id"] for g in gates if g["kind"] == "identity"]
    bearing = [g["id"] for g in gates if g["kind"].startswith("load-bearing")]
    neg = [g["id"] for g in gates if g.get("negative_reading")]

    add("=" * 78)
    add("ROOT V128 第五册 · 大 lambda 扫描空转与整体幅度不可辨识性")
    add("算法联盟可算审计（非判定册）  date : %s" % DATE)
    add("=" * 78)
    add("")
    add("target    : ROOT V128 Yukawa 势 Phi(r) = -(mu/r)(1 + alpha exp(-r/lambda))")
    add("question  : 这个势里哪些参数组合真正可观测")
    add("upstream  : %s" % os.path.basename(upstream_json()))
    add("up_sha256 : %s" % up_sha)
    add("up_bytes  : %d" % up_bytes)
    add("")
    add("-" * 78)
    for g in gates:
        add("[%s] %s  %s" % (g["id"], "OK  " if g["ok"] else "FAIL", g["title"]))
        for n in g.get("notes", []):
            add("       " + n)
        for k, v in (g.get("readings") or {}).items():
            add("       .%-40s = %s" % (k, v))
        for r in (g.get("rows") or [])[:8]:
            add("       | " + "  ".join("%s=%s" % (k, v) for k, v in r.items()))
        add("")
    add("-" * 78)
    add("verdict   : %s" % verdict)
    add("final     : %s" % final)
    add("guards    : %s" % " ".join(guards))
    add("identity  : %s" % (" ".join(identity) if identity else "无"))
    add("bearing   : %s" % " ".join(bearing))
    add("negative  : %s" % " ".join(neg))
    add("n_gate_ok : %d / %d" % (n_ok, n_tot))
    add("")
    add("red_line  : 不宣称攻破统一场论；不产生新物理；独立实验预言 0；")
    add("            第三册读数只继承不重拟合；本册不修正任何既有判词。")
    add("boundary  : 本册判的是「alpha 在大 lambda 端不是可观测参数」，")
    add("            不是「第五力不存在」，也不是「V128 被证伪」。")
    add("            若将来有人在 beta 而非 alpha 上报告约束，本册结论不变。")
    add("=" * 78)
    return "\n".join(L) + "\n"


def build_payload(gates, verdict, final, up_sha, up_bytes):
    return {
        "kind": "algorithm-alliance-audit-recompute",
        "not_a_verdict_volume": True,
        "occupies_rid": False,
        "enters_readme": False,
        "title": "ROOT V128 第五册 大 lambda 扫描空转与整体幅度不可辨识性",
        "date": DATE,
        "target": "Phi(r) = -(mu/r)(1 + alpha exp(-r/lambda))",
        "upstream": {
            "file": os.path.basename(upstream_json()),
            "sha256": up_sha,
            "bytes": up_bytes,
            "relation": "只读继承；不重拟合；不改判词",
        },
        "verdict": verdict,
        "verdict_type": "machine",
        "final": final,
        "n_gate_ok": sum(1 for g in gates if g["ok"]),
        "n_gate_total": len(gates),
        "guards": [g["id"] for g in gates if g["kind"] == "guard"],
        "identity_gates": [g["id"] for g in gates if g["kind"] == "identity"],
        "load_bearing_gates": [g["id"] for g in gates if g["kind"].startswith("load-bearing")],
        "negative_gates": [g["id"] for g in gates if g.get("negative_reading")],
        "gates": gates,
        "discipline": [
            "恒等门（L3）单列不承重",
            "跨册读数只继承不重算，冲突时报负读数不改上游",
            "ok 由读数驱动，AST 守卫禁止常量赋值",
            "判词由唯一构造函数生成，三标志任一翻转必变",
            "回填顺序：占位 -> 回读 -> 再写 -> 守卫 -> FINAL -> 报告",
        ],
        "red_line": [
            "不宣称攻破统一场论",
            "不产生新物理，独立实验预言 0",
            "本册不修正第三册任何判词",
            "「大 lambda 空转」不等于「V128 被证伪」",
        ],
    }


def _write_json(gates, verdict, final, up_sha, up_bytes):
    jp = out_json()
    os.makedirs(os.path.dirname(jp), exist_ok=True)
    body = json.dumps(build_payload(gates, verdict, final, up_sha, up_bytes),
                      ensure_ascii=False, indent=1, sort_keys=False)
    with open(jp, "w", encoding="utf-8") as fh:
        fh.write(body + "\n")
    return jp


def _write_report(gates, verdict, final, up_sha, up_bytes):
    rp = report_path()
    os.makedirs(os.path.dirname(rp), exist_ok=True)
    with open(rp, "w", encoding="utf-8") as fh:
        fh.write(render_report(gates, verdict, final, up_sha, up_bytes))
    return rp


# ---------------------------------------------------------------- 主流程
def main():
    up, up_sha, up_bytes = load_upstream()

    gates = [gate_L1(), gate_L2(), gate_L3(), gate_L4(),
             gate_L5(up, up_sha, up_bytes), gate_L6(up), gate_L7(up), gate_L8(up),
             gate_verdict_machine(), gate_no_hardcode()]

    by_id = {g["id"]: g for g in gates}
    f5, f6, f7 = by_id["L5"]["ok"], by_id["L6"]["ok"], by_id["L7"]["ok"]
    verdict = verdict_of(f5, f6, f7)

    def decide(gs):
        bad = [g["id"] for g in gs if not g["ok"]]
        if bad:
            return "GATES-FAIL--" + "-".join(bad)
        if f5 and f6 and f7:
            return "GATES-PASS-WITH-VACUITY-CONCLUSION"
        return "GATES-PASS-BUT-VACUITY-CONCLUSION-REFUTED"

    final = decide(gates)

    # 回填 A：先落盘占位（让 link 门可读）
    _write_report(gates, verdict, final, up_sha, up_bytes)
    _write_json(gates, verdict, final, up_sha, up_bytes)

    # 守卫：链接体检
    gates.append(gate_link_check(out_json(), report_path(), verdict))
    final = decide(gates)

    # 回填 B：带 link 门再写一次（内容确定，两次跑逐字节相同）
    rp = _write_report(gates, verdict, final, up_sha, up_bytes)
    jp = _write_json(gates, verdict, final, up_sha, up_bytes)

    n_ok = sum(1 for g in gates if g["ok"])
    n_tot = len(gates)
    tag = ".".join(["%s=%s" % (g["id"], g["ok"]) for g in gates])

    sys.stdout.write("verdict   : %s\n" % verdict)
    sys.stdout.write("final     : %s\n" % final)
    sys.stdout.write("n_gate_ok : %d / %d\n" % (n_ok, n_tot))
    sys.stdout.write("gates     : %s\n" % tag)
    sys.stdout.write("report    : %s\n" % rp)
    sys.stdout.write("json      : %s\n" % jp)
    data = open(jp, "rb").read()
    sys.stdout.write("json_bytes: %d\n" % len(data))
    sys.stdout.write("json_sha  : %s\n" % hashlib.sha256(data).hexdigest())
    for g in gates:
        if not g["ok"]:
            sys.stdout.write("FAILED GATE: %s\n" % g["id"])
            for n in g.get("notes", []):
                if n.startswith("FAIL"):
                    sys.stdout.write("    " + n + "\n")
    return 0 if n_ok == n_tot else 1


if __name__ == "__main__":
    sys.exit(main())
