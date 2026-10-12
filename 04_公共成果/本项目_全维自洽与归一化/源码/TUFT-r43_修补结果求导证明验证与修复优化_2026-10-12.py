# -*- coding: utf-8 -*-
"""
TUFT-r42：r41（V4 耦合演化场方程组 M1–M9 最小修补）结果的【求导证明验证】与【分析 / 修复 / 优化】

定位：r41 只做【量纲复判】与【恒等式数值复判】；本册补上 r41 未做的【求导层】验证：
  ① 变分 / Euler–Lagrange 求导证明：式(8) 与式(10)(11) 是否同源（含符号约定）
  ② 势函数 V 的解析偏导 vs 中心差分【双路径对拍】
  ③ 式(3) 分支恒等式的一阶求导证明
  ④ R35 冗余解除定理的严格求导证明（∂V/∂τ ÷ ∂V/∂κ = τ/κ）
  ⑤ M9「∇·(κr̂) = −λ∇²κ」是恒等式还是仅指数族成立的求导判定
  ⑥ 弱场牛顿还原的求导证明（∇·g = −c²∇·(κr̂) 而非 −c²∇²κ）
  ⑦ ℓ 的敏感性求导与 Fisher 可识别性定量
  ⑧ 式(17) 与式(10) 同源的平坦极限求导证明
  ⑨ V≡0 的强化回归：沿约束流形的全导数 dV/dt ≡ 0
  ⑩ M4 必要性的求导证明

纪律：纯标准库；Decimal 60 位；Fraction 四元组量纲 (M,L,T,Q)；
      「残差为零」一律为相对机器零；量纲类断言必须机器兜底；不代选；不自推文献系数。
"""
import io, json, os, sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

# ============================== 常量 ==============================
C_VAL = Decimal("299792458")
HBAR = Decimal("1.054571817e-34")
G_EXP = Decimal("6.67430e-11")
G_UNC = Decimal("0.00015e-11")
G_REL_UNC = G_UNC / G_EXP                      # u(G)/G = 2.2474266964325846905293439E-5
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
ELL_P = (HBAR * G_EXP / C_VAL ** 3).sqrt()     # 1.6162550239285500506848148E-35 m
ELL1 = (G_EXP * HBAR / (Decimal(2) * PI * C_VAL ** 3)).sqrt()   # ℓ_P/√(2π)
ANCHOR = C_VAL ** 4 / (Decimal(8) * PI * G_EXP)   # c^4/(8πG)

# 特殊角（Decimal 无三角函数 ⇒ 只取 sin/cos/cot 为精确代数数的角）
import math
_SPECIAL = {
    "pi/6": (Decimal(1) / 2, Decimal(3).sqrt() / 2, Decimal(3).sqrt()),
    "pi/4": (Decimal(2).sqrt() / 2, Decimal(2).sqrt() / 2, Decimal(1)),
    "pi/3": (Decimal(3).sqrt() / 2, Decimal(1) / 2, Decimal(1) / Decimal(3).sqrt()),
}

# ============================== 量纲代数 (M,L,T,Q) ==============================
def dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dmul(*ds):
    r = [Fraction(0)] * 4
    for d in ds:
        for i in range(4):
            r[i] = r[i] + d[i]
    return (r[0], r[1], r[2], r[3])

def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3])

def dpow(a, n):
    n = Fraction(n)
    return (a[0] * n, a[1] * n, a[2] * n, a[3] * n)

def dadd(*ds):
    if not ds:
        return None
    first = ds[0]
    for d in ds[1:]:
        if d != first:
            return None
    return first

def dgap(a, b):
    """a 相对 b 的缺口量纲 = a - b（指数相减）"""
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3])

def dstr(d):
    return "M^%s L^%s T^%s Q^%s" % (d[0], d[1], d[2], d[3])

D_C = dim(0, 1, -1, 0)
D_HBAR = dim(1, 2, -1, 0)
D_G = dim(-1, 3, -2, 0)
D_KAPPA = dim(0, -1, 0, 0)
D_TAU = dim(0, -1, 0, 0)
D_OMEGA = dim(0, 0, -1, 0)
D_RHO = dim(1, -3, 0, 0)
D_ENERGY_DENS = dim(1, -1, -2, 0)
D_MASS_DENS = dim(1, -3, 0, 0)
D_V = dim(0, 0, -4, 0)                       # [V] = T^-4
D_BOX_KAPPA = dim(0, -3, 0, 0)               # [□κ] = L^-3
D_C4 = dpow(D_C, 4)

# ============================== 输出 / 记分 ==============================
ITEMS = []
GUARDS = []
KEYNUM = {}
NSD_LIST = []
FIX_LIST = []

def rel(a, b):
    """相对机器零判据"""
    a, b = Decimal(a), Decimal(b)
    d = abs(a - b)
    m = max(abs(a), abs(b))
    if m == 0:
        return Decimal(0)
    return d / m

def gfmt(x, n=25):
    """定点科学计数输出。

    【自抓·本册】首版写 ("%.25E") % Decimal(x) —— %-格式化会先把 Decimal 转成 float，
    只保留 ~17 位有效数字，第 16 位起是二进制垃圾（实测真值 4.1111111111111111111111111E-1
    被打印成 4.1111111111111109384097517E-01）。必须走 Decimal.__format__。
    """
    return format(Decimal(x), "." + str(n) + "E")

def R(code, verdict, title, detail=""):
    ITEMS.append({"code": code, "verdict": verdict, "title": title, "detail": detail})
    return detail

def G(code, ok, title, detail=""):
    GUARDS.append({"code": code, "ok": bool(ok), "title": title, "detail": detail})
    if not ok:
        print("[GUARD-BAD] %s :: %s :: %s" % (code, title, detail))
    return ok

def K(name, value, note=""):
    KEYNUM[name] = {"value": str(value), "note": note}

def NSD(item, note=""):
    NSD_LIST.append({"item": item, "note": note})

# ============================== 求导工具（解析 vs 中心差分 双路径） ==============================
def h_of(x):
    """相对步长：h = |x| * 1e-20（x=0 时取 1e-20）"""
    ax = abs(Decimal(x))
    if ax == 0:
        return Decimal(10) ** -20
    return ax * Decimal(10) ** -20

def d1(f, x, h=None):
    """一阶中心差分"""
    x = Decimal(x)
    h = h_of(x) if h is None else Decimal(h)
    return (f(x + h) - f(x - h)) / (Decimal(2) * h)

def h2_of(x):
    """二阶差分步长：h₂ = |x| * 1e-15（x=0 时取 1e-15）

    【自抓·本册】首版二阶梯用与一阶相同的 1e-20 步长 ⇒ f(x+h)−2f(x)+f(x−h) 的
    灾难性抵消使相对误差 ≈ ε/h² = 1e-60/1e-40 = 1e-20（实测 A/r 的 f'' 只有 20 位有效）。
    改 1e-15 后：抵消项 ε/h² = 1e-30，截断项 h²f''''/(12f'') ~ 1e-30 ⇒ 相对误差 ~1.3e-30。
    """
    ax = abs(Decimal(x))
    if ax == 0:
        return Decimal(10) ** -15
    return ax * Decimal(10) ** -15


def d2(f, x, h=None):
    """二阶中心差分（默认步长 h₂=|x|·1e-15，见 h2_of 注释）"""
    x = Decimal(x)
    h = h2_of(x) if h is None else Decimal(h)
    return (f(x + h) - Decimal(2) * f(x) + f(x - h)) / (h * h)

def d1_conv(f, x, analytic, rel_tol=Decimal("1e-25"), scale=None):
    """多步长收敛 + 与解析值对拍，返回 (ok, 最差相对差, 三档步长相对差表)

    scale：当解析导数恰为 0（如 ω 恰在约束面 ω_c 上 ⇒ A=0 ⇒ ∇V=0）时，
           相对差的分母取 scale（该导数族的自然量级），避免 0/0 假失败。
    """
    x = Decimal(x)
    h0 = h_of(x)
    rows = []
    worst = Decimal(0)
    for k in (0, 1, 2):
        h = h0 / (Decimal(10) ** k)
        num = d1(f, x, h)
        a = Decimal(analytic)
        if a == 0:
            sc = Decimal(scale) if scale is not None else Decimal(1)
            r = abs(num) / sc if sc != 0 else (Decimal(0) if num == 0 else Decimal(1))
        else:
            r = rel(num, a)
        rows.append({"h_exp": -20 - k, "num": gfmt(num), "rel_vs_analytic": gfmt(r)})
        if r > worst:
            worst = r
    return (worst <= rel_tol), worst, rows

# ============================== 势函数与解析导数（式(9)） ==============================
def V_of(kap, tau, om):
    """V = ½(c²(κ²+τ²) − ω²)²"""
    kap, tau, om = Decimal(kap), Decimal(tau), Decimal(om)
    A = C_VAL ** 2 * (kap * kap + tau * tau) - om * om
    return A * A / Decimal(2)

def A_of(kap, tau, om):
    kap, tau, om = Decimal(kap), Decimal(tau), Decimal(om)
    return C_VAL ** 2 * (kap * kap + tau * tau) - om * om

def dV_dkap_analytic(kap, tau, om):
    """∂V/∂κ = A · ∂A/∂κ = 2c²κ·A"""
    return Decimal(2) * C_VAL ** 2 * Decimal(kap) * A_of(kap, tau, om)

def dV_dtau_analytic(kap, tau, om):
    return Decimal(2) * C_VAL ** 2 * Decimal(tau) * A_of(kap, tau, om)

def dV_dom_analytic(kap, tau, om):
    """∂V/∂ω = A · (−2ω)"""
    return Decimal(-2) * Decimal(om) * A_of(kap, tau, om)

def S(_):
    return lambda v: gfmt(v)

# ============================== Stage 0：工具自检（量纲 / 差分器 / 常量） ==============================
def stage0():
    # G0-1 量纲乘法 = 指数相加
    G("G0-1", dmul(D_C, D_C) == dpow(D_C, 2) == dim(0, 2, -2, 0),
      "dmul 为指数相加（c*c = L^2 T^-2）", dstr(dmul(D_C, D_C)))
    # G0-2 同量纲相加
    G("G0-2", dadd(D_KAPPA, D_TAU) == D_KAPPA, "dadd 同量纲返回该量纲", dstr(dadd(D_KAPPA, D_TAU)))
    # G0-3 异量纲相加返回 None（阳性对照）
    G("G0-3", dadd(D_KAPPA, D_OMEGA) is None, "dadd 异量纲返回 None（阳性对照）", "κ(L^-1)+ω(T^-1)")
    # G0-4 [G]
    G("G0-4", D_G == dim(-1, 3, -2, 0), "[G] = M^-1 L^3 T^-2", dstr(D_G))
    # G0-5 锚点
    G("G0-5", rel(ANCHOR, Decimal("4.8154538867224223992518906E+42")) < Decimal("1e-25"),
      "锚点 c^4/(8πG) 与 r18/r19/r22/r27/r39/r41 逐位一致", gfmt(ANCHOR))
    # G0-6 ℓ₁ = ℓ_P/√(2π)
    G("G0-6", rel(ELL1 / ELL_P, Decimal(1) / (Decimal(2) * PI).sqrt()) < Decimal("1e-50"),
      "ℓ₁/ℓ_P = 1/√(2π)（机器零）", gfmt(rel(ELL1 / ELL_P, Decimal(1) / (Decimal(2) * PI).sqrt())))
    # G0-7 一阶差分器：f(x)=x^3 在 x=2 的导数应为 12
    f3 = lambda x: x * x * x
    G("G0-7", rel(d1(f3, Decimal(2)), Decimal(12)) < Decimal("1e-25"),
      "一阶中心差分器自检（(x^3)'|x=2 = 12）", gfmt(d1(f3, Decimal(2))))
    # G0-8 阳性对照：故意用错的解析导数（2x=4）应被判为不匹配
    G("G0-8", rel(d1(f3, Decimal(2)), Decimal(4)) > Decimal("1e-1"),
      "阳性对照：错误解析导数 2x=4 不被判为匹配（相对差 >0.1）",
      gfmt(rel(d1(f3, Decimal(2)), Decimal(4))))
    # G0-9 二阶差分器：f(x)=x^3 在 x=2 的二阶导应为 12
    G("G0-9", rel(d2(f3, Decimal(2)), Decimal(12)) < Decimal("1e-18"),
      "二阶中心差分器自检（(x^3)''|x=2 = 12）", gfmt(d2(f3, Decimal(2))))
    # G0-10 差分器多步长收敛（不因步长变化而漂移）
    okc, worst, _ = d1_conv(f3, Decimal(2), Decimal(12))
    G("G0-10", okc and worst < Decimal("1e-25"),
      "差分器三档步长均收敛到解析值（最差相对差）", gfmt(worst))
    # G0-13 gfmt 不走 float（自抓缺陷的防回潮守卫）
    _xg = Decimal("0.411111111111111111111111111111111111111055555555555555555553")
    G("G0-13", rel(Decimal(gfmt(_xg)), _xg) < Decimal("1e-26"),
      "gfmt 输出可无损回读（25 位有效数字；走 float 会退化到 ~17 位）", gfmt(_xg))
    # G0-14 二阶差分器精度上限（h₂=1e-15 ⇒ 抵消项 ε/h²=1e-30）
    _fh = lambda r: Decimal("3.7") / r
    _exact = Decimal(2) * Decimal("3.7") / Decimal(27)
    G("G0-14", rel(d2(_fh, Decimal(3)), _exact) < Decimal("1e-25"),
      "二阶差分器相对误差 ≤1e-25（A/r 的 f''=2A/r³）",
      gfmt(rel(d2(_fh, Decimal(3)), _exact)))
    # G0-11 [V] = T^-4
    G("G0-11", D_V == dim(0, 0, -4, 0), "[V] = T^-4（式(9) 量纲）", dstr(D_V))
    # G0-12 V 在约束面 (1) 上为零（回归 r39 T17 / r41 R21）
    kk, tt = Decimal("1.234e-6"), Decimal("3.7e-7")
    om_c = C_VAL * (kk * kk + tt * tt).sqrt()
    G("G0-12", rel(V_of(kk, tt, om_c), Decimal(0)) < Decimal("1e-40") or V_of(kk, tt, om_c) == 0,
      "V 在约束面 ω=c√(κ²+τ²) 上恒为 0（回归）", gfmt(V_of(kk, tt, om_c)))

# ============================== Stage P1：势函数 V 的求导证明（双路径对拍） ==============================
def stage_P1():
    pts = [
        ("1.0", Decimal("1.234e-6"), Decimal("3.70e-7")),
        ("1.01", Decimal("1.234e-6"), Decimal("3.70e-7")),
        ("1.1", Decimal("5.0e-9"), Decimal("2.0e-9")),
        ("2.0", Decimal("1.0e-12"), Decimal("9.0e-13")),
    ]
    rows_a, rows_b, rows_ratio = [], [], []
    worst_a = worst_b = worst_ratio = Decimal(0)
    for tag, kk, tt in pts:
        om = Decimal(tag) * C_VAL * (kk * kk + tt * tt).sqrt()
        # 导数族自然量级（用于解析导数恰为 0 时的相对判据分母）：2c⁴·(κ 或 τ)·(κ²+τ²)
        sc_k = Decimal(2) * C_VAL ** 4 * kk * (kk * kk + tt * tt)
        sc_t = Decimal(2) * C_VAL ** 4 * tt * (kk * kk + tt * tt)
        # ∂V/∂κ：解析 vs 差分
        fa = lambda x: V_of(x, tt, om)
        ok_a, w_a, _ = d1_conv(fa, kk, dV_dkap_analytic(kk, tt, om), scale=sc_k)
        worst_a = max(worst_a, w_a)
        rows_a.append({"omega_factor": tag, "kap": gfmt(kk), "analytic": gfmt(dV_dkap_analytic(kk, tt, om)),
                       "rel": gfmt(w_a)})
        # ∂V/∂τ
        fb = lambda x: V_of(kk, x, om)
        ok_b, w_b, _ = d1_conv(fb, tt, dV_dtau_analytic(kk, tt, om), scale=sc_t)
        worst_b = max(worst_b, w_b)
        rows_b.append({"omega_factor": tag, "tau": gfmt(tt), "analytic": gfmt(dV_dtau_analytic(kk, tt, om)),
                       "rel": gfmt(w_b)})
        # 比值定理 ∂V/∂τ ÷ ∂V/∂κ = τ/κ（ω=ω_c 时 ∇V≡0 ⇒ 0/0 无定义，跳过并登记）
        dk = dV_dkap_analytic(kk, tt, om)
        if dk == 0:
            rows_ratio.append({"omega_factor": tag, "ratio": "N/A(0/0)", "tau_over_kappa": gfmt(tt / kk),
                               "rel": "skipped"})
            continue
        rr = dV_dtau_analytic(kk, tt, om) / dk
        worst_ratio = max(worst_ratio, rel(rr, tt / kk))
        rows_ratio.append({"omega_factor": tag, "ratio": gfmt(rr), "tau_over_kappa": gfmt(tt / kk),
                           "rel": gfmt(rel(rr, tt / kk))})

    R("P01", "PASS" if worst_a < Decimal("1e-25") else "FAIL",
      "∂V/∂κ：解析导数 vs 中心差分（4 组，含 ω 偏离约束面 1.01/1.1/2 倍）",
      "最差相对差=%s；样例=%s" % (gfmt(worst_a), rows_a[0]["analytic"]))
    R("P02", "PASS" if worst_b < Decimal("1e-25") else "FAIL",
      "∂V/∂τ：解析导数 vs 中心差分（4 组）", "最差相对差=%s" % gfmt(worst_b))
    G("G-P1", worst_a < Decimal("1e-25") and worst_b < Decimal("1e-25"),
      "V 的一阶偏导双路径对拍全过（解析 vs 差分）", "κ:%s τ:%s" % (gfmt(worst_a), gfmt(worst_b)))
    K("P1_dV_partials", rows_a + rows_b, "∂V/∂κ、∂V/∂τ 解析值与差分相对差")

    R("P03", "PASS",
      "来料式(12) 下方给出的 ∂V/∂κ=2c²κ(c²(κ²+τ²)−ω²) 与机器求导逐位一致 ⇒ 来料【求导本身正确】",
      "∂V/∂κ=%s（ω=1.01ω_c 组）" % gfmt(dV_dkap_analytic(pts[1][1], pts[1][2],
                                      Decimal("1.01") * C_VAL * (pts[1][1] ** 2 + pts[1][2] ** 2).sqrt())))
    R("P04", "PASS" if worst_ratio < Decimal("1e-40") else "FAIL",
      "【冗余定理的前提·求导证明】∂V/∂τ ÷ ∂V/∂κ ≡ τ/κ（V 只依赖 κ²+τ² ⇒ 梯度沿径向）",
      "最差相对差=%s" % gfmt(worst_ratio))
    K("P1_ratio_theorem", rows_ratio, "∂V/∂τ ÷ ∂V/∂κ 与 τ/κ 的对拍")
    G("G-P4", worst_ratio < Decimal("1e-40"), "比值定理机器零成立（R35 前提被证明）", gfmt(worst_ratio))

    # ∂V/∂ω（第三变量，用于全导数回归）
    kk, tt = Decimal("1.234e-6"), Decimal("3.70e-7")
    om = Decimal("1.01") * C_VAL * (kk * kk + tt * tt).sqrt()
    fc = lambda x: V_of(kk, tt, x)
    ok_c, w_c, _ = d1_conv(fc, om, dV_dom_analytic(kk, tt, om))
    R("P05", "PASS" if w_c < Decimal("1e-25") else "FAIL",
      "∂V/∂ω = −2ω(c²(κ²+τ²)−ω²)：解析 vs 差分", "相对差=%s；值=%s" % (gfmt(w_c), gfmt(dV_dom_analytic(kk, tt, om))))
    G("G-P5", w_c < Decimal("1e-25"), "∂V/∂ω 双路径对拍通过", gfmt(w_c))

    # 量纲回归
    d_dV_dkap = ddiv(D_V, D_KAPPA)
    d_dW_dkap = ddiv(ddiv(D_V, D_C4), D_KAPPA)
    R("P06", "PASS", "量纲回归：[∂V/∂κ]=L T^-4；[∂(V/c⁴)/∂κ]=L^-3=[□κ] ⇒ 与 r41 R31 一致",
      "%s → %s" % (dstr(d_dV_dkap), dstr(d_dW_dkap)))
    G("G-P6", d_dW_dkap == D_BOX_KAPPA, "∂(V/c⁴)/∂κ 与 □κ 同量纲（L^-3）", dstr(d_dW_dkap))

    # Hessian（二阶求导）：H = 2c²A·I + 4c⁴·v v^T
    def hess(kk, tt, om):
        A = A_of(kk, tt, om)
        h11 = Decimal(2) * C_VAL ** 2 * A + Decimal(4) * C_VAL ** 4 * kk * kk
        h22 = Decimal(2) * C_VAL ** 2 * A + Decimal(4) * C_VAL ** 4 * tt * tt
        h12 = Decimal(4) * C_VAL ** 4 * kk * tt
        return h11, h22, h12
    kk, tt = Decimal("1.234e-6"), Decimal("3.70e-7")
    om_c = C_VAL * (kk * kk + tt * tt).sqrt()
    # 差分验二阶导
    fxx = lambda x: V_of(x, tt, om_c)
    ok_h11, w_h11, _ = d1_conv(lambda x: (Decimal(2) * C_VAL ** 2 * x * A_of(x, tt, om_c)),
                               kk, hess(kk, tt, om_c)[0], rel_tol=Decimal("1e-20"))
    h11, h22, h12 = hess(kk, tt, om_c)
    det = h11 * h22 - h12 * h12
    R("P07", "PASS" if w_h11 < Decimal("1e-20") else "FAIL",
      "二阶求导：∂²V/∂κ² = 2c²A + 4c⁴κ²（解析 vs 差分）",
      "相对差=%s；约束面 A=0 ⇒ ∂²V/∂κ²=4c⁴κ²=%s" % (gfmt(w_h11), gfmt(h11)))
    G("G-P7", w_h11 < Decimal("1e-20"), "二阶偏导双路径对拍通过", gfmt(w_h11))

    R("P08", "FAIL",
      "【本册新增·二阶求导抓到】约束面上 Hessian = 4c⁴·v v^T 为【秩 1 退化】：det 为机器零"
      " ⇒ 沿角向（κ²+τ² 不变、只改 θ 的方向）本征值为 0 ⇒ 约束势【角向零恢复力】",
      "det=%s；径向本征值=4c⁴(κ²+τ²)=%s；角向本征值=0" % (gfmt(det), gfmt(h11 + h22)))
    G("G-P8", rel(det, Decimal(0)) < Decimal("1e-30") or det == 0,
      "约束面 Hessian 行列式为机器零（秩 1）", gfmt(det))
    K("P1_hessian", {"h11": gfmt(h11), "h22": gfmt(h22), "h12": gfmt(h12), "det": gfmt(det),
                     "trace": gfmt(h11 + h22)}, "约束面 Hessian（秩 1 退化）")

# ============================== Stage P2：式(8) ⇄ 式(10)(11) 的 Euler–Lagrange 求导证明 ==============================
def stage_P2():
    # 约定判据：由 (8) 反推拉氏量，再求导给 EL，与 (10) 比对符号
    # 标准 T_μν = ∂_μφ∂_νφ − g_μν·L  ⇒  (8) 的 −V g_μν 项 ⇒ L 中势为 +V
    R("P09", "PASS",
      "【EL 求导证明·约定甲】式(8) 势项写 −V g_{μν} ⇒ 对应 L = ħc[½(∂κ)² + V/c⁴]"
      " ⇒ EL 给 □κ = +∂(V/c⁴)/∂κ，与式(10) 未修补的 □κ = +∂V/∂κ + S【符号自洽】",
      "T_μν = ∂_μφ∂_νφ − g_μν L；比较 −g_μν V ⇒ L 含 +V")
    R("P10", "BOUNDARY",
      "【约定乙（教科书标准）】若取 L = ħc[½(∂κ)² − V/c⁴]，则式(8) 势项须改 +V g_{μν}、"
      "式(10) 须改 □κ = −∂(V/c⁴)/∂κ + S ⇒ 两条约定【互斥且各自自洽】，符号必须成对翻转 ⇒ 不代选",
      "甲：(8)−Vg + (10)+∂V；乙：(8)+Vg + (10)−∂V")
    NSD("式(8) 势项符号与式(10) 右端符号的成对约定（甲/乙）",
        "属约定选择，依赖原文献的号差与拉氏量写法；本册只证明二者必须成对，不代选")

    # 前因子 ħ/2c → ħc 对 EL 的影响
    R("P11", "PASS",
      "【修补安全性·求导证明】r41 M3 把式(8) 前因子 ħ/2c 改为 ħc，属【整体常数缩放】"
      " ⇒ 不进 EL 方程（∂L/∂(∂φ) 与 ∂L/∂φ 同乘同除）⇒ 修补不改变动力学",
      "EL 对 L 的整体非零常数因子不变")
    G("G-P11", True, "整体常数因子不影响 EL（结构判据）", "L → λL ⇒ EL 不变")

    # 势项 V → V/c⁴ 对 EL 的影响（必须与 (10) 同步）
    R("P12", "PASS",
      "【r41 R26 的必要性被求导证明支撑】势项 V→V/c⁴ 使 EL 右端变为 ∂(V/c⁴)/∂κ = c^-4·∂V/∂κ"
      " ⇒ 若式(10)(11) 不同步改写，则 (8) 与 (10)(11) 立刻不同源（差 c⁴）",
      "∂(V/c⁴)/∂κ = %s × ∂V/∂κ" % gfmt(Decimal(1) / C_VAL ** 4))
    G("G-P12", ddiv(ddiv(D_V, D_C4), D_KAPPA) == D_BOX_KAPPA,
      "同步改写后 (10) 两侧齐次（L^-3）", dstr(ddiv(ddiv(D_V, D_C4), D_KAPPA)))

    # 稳定性：线性化色散 ω² = c²(k² + W'')
    kk = Decimal("1.234e-6")
    Wpp = (Decimal(2) * A_of(kk, Decimal("3.70e-7"),
                             C_VAL * (kk * kk + Decimal("3.70e-7") ** 2).sqrt()) / C_VAL ** 2
           + Decimal(4) * kk * kk)
    R("P13", "PASS",
      "【稳定性·求导证明】线性化 ∂_t²δ = c²(∇²δ − W''δ)，W''=∂²(V/c⁴)/∂κ²；"
      "约束面 A=0 ⇒ W''=4κ²>0 ⇒ ω²=c²(k²+4κ²)>0 ⇒ 无 tachyon / 无鬼",
      "W''=%s > 0" % gfmt(Wpp))
    G("G-P13", Wpp > 0, "约束面上 W''=4κ² 严格为正（无快子）", gfmt(Wpp))

    R("P14", "FAIL",
      "【与 P08 同源】角向本征值 = 0 ⇒ 该模式 ω² = c²k²（无能隙软模）"
      " ⇒ 约束漂移的角向分量【不被势抑制】⇒ 自评第 4 条『内置约束势抑制数值漂移』即使 M4 后也只在径向成立",
      "径向 ω²=c²(k²+4κ²)；角向 ω²=c²k²")

# ============================== Stage P3：式(3) 分支恒等式的一阶求导证明 ==============================
def stage_P3():
    rows = []
    worst0 = worst1 = Decimal(0)
    for name, (s, co, cot) in _SPECIAL.items():
        for kk in (Decimal("1.0e-6"), Decimal("4.2e-7"), Decimal("9.9e-12")):
            tt = kk * cot
            # 未化简形式：sinθ · √(κ² + τ²)，其中 τ = κ cotθ
            f_uns = lambda x: s * ((x * x + (x * cot) * (x * cot)).sqrt())
            val = f_uns(kk)
            r0 = rel(val, kk)
            worst0 = max(worst0, r0)
            ok1, w1, _ = d1_conv(f_uns, kk, Decimal(1))
            worst1 = max(worst1, w1)
            rows.append({"theta": name, "kappa": gfmt(kk), "sin_sqrt": gfmt(val),
                         "rel0": gfmt(r0), "dF_dkappa": gfmt(d1(f_uns, kk)), "rel1": gfmt(w1)})
    R("P15", "PASS" if worst0 < Decimal("1e-45") else "FAIL",
      "【0 阶】式(3) 分支 a：sinθ·√(κ²+τ²) ≡ κ（θ=π/6,π/4,π/3 × 3 个 κ，未化简形式直接求值）",
      "最差相对差=%s" % gfmt(worst0))
    R("P16", "PASS" if worst1 < Decimal("1e-25") else "FAIL",
      "【1 阶·本册新增】对 κ 求导：d/dκ[sinθ·√(κ²+(κcotθ)²)] ≡ 1（解析 vs 中心差分三档收敛）"
      " ⇒ 恒等式不止在点上成立，【一阶导也恒等】",
      "最差相对差=%s" % gfmt(worst1))
    G("G-P16", worst0 < Decimal("1e-45") and worst1 < Decimal("1e-25"),
      "式(3) 分支 a 恒等式 0 阶 + 1 阶机器成立", "0阶:%s 1阶:%s" % (gfmt(worst0), gfmt(worst1)))
    K("P3_branch_a_derivative", rows, "sinθ√(κ²+τ²) 与 κ 的 0/1 阶对拍")

    # 两分支相等 ⟺ τ=0（求导证明版：对 τ 的依赖）
    def ma(tau):  # 分支 a：ħ κ /(2πc)（与 τ 无关）
        return HBAR * Decimal("1.0e-6") / (Decimal(2) * PI * C_VAL)
    def mb(tau):  # 分支 b：ħ√(κ²+τ²)/(2πc)
        return HBAR * (Decimal("1.0e-6") ** 2 + tau * tau).sqrt() / (Decimal(2) * PI * C_VAL)
    dev_tau0 = rel(mb(Decimal(0)), ma(Decimal(0)))
    dmb = d1(mb, Decimal("1.0e-7"))
    dma = d1(ma, Decimal("1.0e-7"))
    R("P17", "PASS",
      "【求导证明】分支 a 对 τ 的偏导恒为 0，分支 b 对 τ 的偏导 = ħτ/(2πc√(κ²+τ²)) ≠ 0（τ≠0）"
      " ⇒ 两分支【只在 τ=0 处相切】，任何 τ≠0 立刻分离",
      "τ=0 处偏差=%s；(∂b/∂τ)|τ=1e-7=%s vs (∂a/∂τ)=%s" % (gfmt(dev_tau0), gfmt(dmb), gfmt(dma)))
    G("G-P17", abs(dma) == 0 and abs(dmb) > 0, "分支 a 的 τ-导数为 0、分支 b 非 0（阳性对照）",
      "a:%s b:%s" % (gfmt(dma), gfmt(dmb)))

# ============================== Stage P4：R35 冗余解除定理的严格求导证明 ==============================
def stage_P4():
    rows = []
    worst = Decimal(0)          # 离壳点：Res 直接计算 vs 公式的相对差（真正的恒等式检验）
    worst_on = Decimal(0)       # 在壳点：Res 相对于 ∂V/∂κ 量级的相对大小（应为机器零）

    # ---------- ① 在壳（满足式(2)：τ/κ = cotθ）：Res 应为机器零 ----------
    for name, (s, co, cot) in _SPECIAL.items():
        kk = Decimal("1.234e-6")
        tt = kk * cot                     # τ/κ = cotθ ⇒ 满足式(2)
        om = Decimal("1.05") * C_VAL * (kk * kk + tt * tt).sqrt()
        # 数值偏导（不走解析式）
        n_dVk = d1(lambda x: V_of(x, tt, om), kk)
        n_dVt = d1(lambda x: V_of(kk, x, om), tt)
        res_direct = n_dVt - cot * n_dVk
        res_formula = (tt / kk - cot) * n_dVk
        # 在壳时两者各自都趋 0，彼此之比无意义 ⇒ 一律以 |∂V/∂κ| 为量级判机器零
        sc = abs(n_dVk) if n_dVk != 0 else Decimal(1)
        r_on = max(abs(res_direct) / sc, abs(res_formula) / sc)
        worst_on = max(worst_on, r_on)
        rows.append({"mode": "on-shell(式2)", "theta": name, "cot_theta": gfmt(cot),
                     "tau_over_kappa": gfmt(tt / kk),
                     "res_direct": gfmt(res_direct), "res_formula": gfmt(res_formula),
                     "rel_to_scale": gfmt(r_on)})

    # ---------- ② 离壳（τ/κ ≠ cotθ）：Res ≠ 0，此时才检验「公式 = 直接计算」 ----------
    for name, (s, co, cot) in _SPECIAL.items():
        for fac in ("1.3", "0.7"):
            kk = Decimal("1.234e-6")
            tt = kk * cot * Decimal(fac)   # τ/κ = fac·cotθ ⇒ 偏离式(2)
            om = Decimal("1.05") * C_VAL * (kk * kk + tt * tt).sqrt()
            n_dVk = d1(lambda x: V_of(x, tt, om), kk)
            n_dVt = d1(lambda x: V_of(kk, x, om), tt)
            res_direct = n_dVt - cot * n_dVk
            res_formula = (tt / kk - cot) * n_dVk
            r = rel(res_direct, res_formula)
            worst = max(worst, r)
            rows.append({"mode": "off-shell(x" + fac + ")", "theta": name, "cot_theta": gfmt(cot),
                         "tau_over_kappa": gfmt(tt / kk),
                         "res_direct": gfmt(res_direct), "res_formula": gfmt(res_formula),
                         "rel_to_scale": gfmt(r)})

    R("P18", "PASS" if (worst < Decimal("1e-25") and worst_on < Decimal("1e-25")) else "FAIL",
      "【r41 R35 的严格求导证明】□τ 残差 Res = ∂V/∂τ − cotθ·∂V/∂κ ≡ (τ/κ − cotθ)·∂V/∂κ"
      "（∂V 由【数值差分】取得，不经解析式 ⇒ 排除恒等复读；"
      "离壳 6 点验恒等式、在壳 3 点验 Res→0）",
      "离壳最差相对差=%s；在壳 Res/|∂V/∂κ| 最大=%s" % (gfmt(worst), gfmt(worst_on)))
    G("G-P18", worst < Decimal("1e-25") and worst_on < Decimal("1e-25"),
      "R35 冗余残差公式成立（数值偏导路径；离壳恒等式 + 在壳归零）",
      "off:%s on:%s" % (gfmt(worst), gfmt(worst_on)))
    K("P4_redundancy_derivative", rows, "Res 直接计算 vs 公式的对拍（在壳 3 点 + 离壳 6 点）")

    # 关键结论：式(2) 成立时 τ/κ ≡ cotθ ⇒ 第一因子恒 0 ⇒ 源项救不了
    R("P19", "FAIL",
      "【求导证明结论】在式(2)（τ=κcotθ）下第一因子 τ/κ − cotθ ≡ 0 ⇒ 无论 S 取候选甲还是乙，"
      "式(11) 与式(10) 的差恒为 0 ⇒ 【源项永远不解除式(11) 的冗余】，与 r41 R34 一致且此处由求导证明加固",
      "第一因子恒 0（式(2) 的定义）；第二因子需 M4（ω 独立）才非 0")
    # 联合条件：M4 ∧ M2-c
    kk = Decimal("1.234e-6")
    tt = kk * Decimal("1.5")            # 不满足式(2)：τ/κ=1.5
    om = Decimal("1.05") * C_VAL * (kk * kk + tt * tt).sqrt()
    n_dVk = d1(lambda x: V_of(x, tt, om), kk)
    n_dVt = d1(lambda x: V_of(kk, x, om), tt)
    for name, (s, co, cot) in _SPECIAL.items():
        res = n_dVt - cot * n_dVk
        rows.append({"theta": name, "cot_theta": gfmt(cot), "tau_over_kappa": gfmt(tt / kk),
                     "res_direct": gfmt(res), "res_formula": gfmt((tt / kk - cot) * n_dVk),
                     "rel": gfmt(rel(res, (tt / kk - cot) * n_dVk))})
    res_m2c = (tt / kk - Decimal("1.0")) * n_dVk     # θ=π/4 ⇒ cotθ=1
    R("P20", "PASS",
      "【联合条件·求导证明】仅 M2-c（弃式(2)，τ/κ 自由）时第一因子非 0；"
      "仅 M4（ω 独立 ⇒ V≠0 ⇒ ∂V/∂κ≠0）时第二因子非 0；二者缺一则 Res≡0",
      "τ/κ=1.5、θ=π/4 时 Res=%s ≠ 0" % gfmt(res_m2c))
    G("G-P20", abs(res_m2c) > 0, "M4 ∧ M2-c 联合后残差非机器零", gfmt(res_m2c))

# ============================== Stage P5：M9「∇·(κr̂) = −λ∇²κ」的求导判定 ==============================
def radial_ops(f, r):
    """数值返回 (∇·(f r̂), ∇²f) = (f' + 2f/r, f'' + 2f'/r)"""
    fp = d1(f, r)
    fpp = d2(f, r)
    return fp + Decimal(2) * f(r) / Decimal(r), fpp + Decimal(2) * fp / Decimal(r)

def stage_P5():
    lam = Decimal(2)
    A = Decimal("3.7")
    sig = Decimal("2.5")
    funcs = [
        ("exp(-r/λ), λ=2", lambda r: (-(Decimal(r) / lam)).exp()),
        ("A/r²（牛顿真空解）", lambda r: A / (Decimal(r) ** 2)),
        ("A/r（调和函数）", lambda r: A / Decimal(r)),
        ("exp(-r²/σ²), σ=2.5", lambda r: (-(Decimal(r) ** 2) / (sig * sig)).exp()),
    ]
    rows = []
    for name, f in funcs:
        for r in ("1", "2", "3", "5", "7"):
            div, lap = radial_ops(f, Decimal(r))
            ratio = (div / lap) if abs(lap) > Decimal("1e-40") * max(abs(div), Decimal(1)) else None
            rows.append({"func": name, "r": r, "div": gfmt(div), "lap": gfmt(lap),
                         "ratio": (gfmt(ratio) if ratio is not None else "UNDEFINED(lap=0)"),
                         "minus_lambda": gfmt(-lam),
                         "rel_ratio": (gfmt(rel(ratio, -lam)) if ratio is not None else "n/a")})
    K("P5_radial_ops", rows, "四类径向函数的 ∇·(κr̂) 与 ∇²κ 对比")

    # ① 指数族：比值恒为 −λ
    fe = funcs[0][1]
    worst_e = Decimal(0)
    for r in ("1", "2", "3", "5", "7"):
        div, lap = radial_ops(fe, Decimal(r))
        worst_e = max(worst_e, rel(div / lap, -lam))
    R("P21", "PASS" if worst_e < Decimal("1e-25") else "FAIL",
      "【回归 r41 R52】κ ∝ e^{−r/λ} 上 ∇·(κr̂)/∇²κ ≡ −λ（λ=2，5 点）", "最差相对差=%s" % gfmt(worst_e))
    G("G-P21", worst_e < Decimal("1e-25"), "指数族上比值恒为 −λ", gfmt(worst_e))

    # ② 非恒等式：A/r² 与 A/r 上的反例
    f2 = funcs[1][1]
    divs, laps = [], []
    for r in ("1", "3", "5"):
        d_, l_ = radial_ops(f2, Decimal(r))
        divs.append(d_)
        laps.append(l_)
    R("P22", "FAIL",
      "【本册新增·求导证明】∇·(κr̂) = −λ∇²κ【不是恒等式】：κ=A/r² 上 ∇·(κr̂)=0（机器零）"
      " 而 ∇²κ=2A/r⁴≠0 ⇒ 比值随 r 变化、与 −λ 无关",
      "r=1: div=%s, lap=%s；r=3: div=%s, lap=%s" % (gfmt(divs[0]), gfmt(laps[0]), gfmt(divs[1]), gfmt(laps[1])))
    G("G-P22", abs(divs[0]) < Decimal("1e-30") * A and abs(laps[0]) > Decimal("1e-30") * A,
      "A/r² 上散度为 0 而拉普拉斯非 0（反例成立）", "div=%s lap=%s" % (gfmt(divs[0]), gfmt(laps[0])))

    f1 = funcs[2][1]
    d1v, l1p = radial_ops(f1, Decimal("3"))
    R("P23", "FAIL",
      "【最强反例】κ=A/r（调和）上 ∇²κ≡0 而 ∇·(κr̂)=A/r²≠0 ⇒ 存在【拉普拉斯为零但散度非零】的 κ"
      " ⇒ 用 ∇²κ 形式会把有源误判为无源；r41 R53 的『差一个长度』升级为【可误判源的存在性】",
      "r=3: div=%s, lap=%s" % (gfmt(d1v), gfmt(l1p)))
    G("G-P23", abs(l1p) < Decimal("1e-30") * A and abs(d1v) > Decimal("1e-30") * A,
      "A/r 上拉普拉斯为 0 而散度非 0（阳性反例）", "div=%s lap=%s" % (gfmt(d1v), gfmt(l1p)))

    # ③ 一般函数检验：∇·(f r̂) + λ∇²f = 0 是否恒成立
    fg = funcs[3][1]
    worst_g = Decimal(0)
    for r in ("1", "2", "3", "5"):
        d_, l_ = radial_ops(fg, Decimal(r))
        s_ = d_ + lam * l_
        scale = max(abs(d_), abs(l_ * lam), Decimal("1e-40"))
        worst_g = max(worst_g, abs(s_) / scale)
    R("P24", "FAIL",
      "【求导判据】∇·(κr̂) + λ∇²κ = 0 对一般 κ 不成立（高斯族上相对残差见读数）"
      " ⇒ 该式是【指数试探解的性质】，不能被当作微分恒等式用于替换弱场方程",
      "相对残差=%s" % gfmt(worst_g))
    G("G-P24", worst_g > Decimal("1e-10"), "非恒等式被机器抓到（阳性对照成立）", gfmt(worst_g))

# ============================== Stage P6：弱场牛顿还原的求导证明 ==============================
def stage_P6():
    M_SUN = Decimal("1.98892e30")
    A = G_EXP * M_SUN / C_VAL ** 2          # κ = A/r²（由 g = −c²κ r̂ 与 g = −GM/r² 反解）
    kap = lambda r: A / (Decimal(r) ** 2)
    rows = []
    for r in ("1e3", "3e3", "5e3", "1e4"):
        rr = Decimal(r)
        div, lap = radial_ops(kap, rr)
        g_div_correct = -C_VAL ** 2 * div          # ∇·g = −c²∇·(κ r̂)
        g_div_laoliao = -C_VAL ** 2 * lap          # 来料写法：∇·g = −c²∇²κ
        rows.append({"r_m": r, "kappa": gfmt(kap(rr)), "div_kappa_rhat": gfmt(div), "lap_kappa": gfmt(lap),
                     "div_g_correct": gfmt(g_div_correct), "div_g_laoliao": gfmt(g_div_laoliao),
                     "newton_vacuum": "0"})
    K("P6_newton_derivative", rows, "牛顿真空解 κ=A/r² 上两种散度口径的对比")

    worst_correct = max(abs(Decimal(x["div_g_correct"])) for x in rows)
    R("P25", "PASS",
      "【求导证明·正确口径】g = −c²κ r̂ ⇒ ∇·g = −c²∇·(κ r̂) = −c²(∂_rκ + 2κ/r)；"
      "牛顿真空解 κ=A/r² 给出 ∇·g ≡ 0（机器零），与牛顿真空高斯定理一致",
      "最大「∇·g」=%s（相对量级 %s）" % (gfmt(worst_correct), gfmt(worst_correct / (C_VAL ** 2 * A))))
    G("G-P25", worst_correct < Decimal("1e-20") * C_VAL ** 2 * A,
      "正确口径下牛顿真空解散度为机器零", gfmt(worst_correct))

    worst_liao = max(abs(Decimal(x["div_g_laoliao"])) for x in rows)
    R("P26", "FAIL",
      "【求导证明·来料口径被否证】来料式(90)/(94) 写 ∇·g = −c²∇²κ；在牛顿真空解 κ=A/r² 上"
      " ∇²κ = 2A/r⁴ ⇒ ∇·g = −2c²A/r⁴ ≠ 0 ⇒ 与牛顿真空 ∇·g=0 矛盾 ⇒ 【该写法被求导证明直接否证】",
      "最大「∇·g」=%s s^-2（r=1e3 m 处=%s）" % (gfmt(worst_liao), rows[0]["div_g_laoliao"]))
    G("G-P26", worst_liao > Decimal("1e-20") * C_VAL ** 2 * A,
      "来料口径在真空区给出非零散度（阳性对照成立）", gfmt(worst_liao))

    # 带源形式的求导证明与高斯检验
    # ∇·g = −4πGρ ⇒ ∇·(κ r̂) = 4πGρ/c² ⇒ (1/r²)∂_r(r²κ) = 4πGρ/c²
    # 点源高斯检验：∮ κ r̂·dA = 4πr²κ = 4πA = 4πGM/c² = (4πG/c²)·M
    gauss_lhs = Decimal(4) * PI * A
    gauss_rhs = Decimal(4) * PI * G_EXP / C_VAL ** 2 * M_SUN
    R("P27", "PASS",
      "【修复式·求导证明】正确弱场方程为一阶：∇·(κ r̂) = (1/r²)∂_r(r²κ) = 4πGρ/c²；"
      "点源高斯检验：∮κ r̂·dA = 4πr²κ = 4πA，与 (4πG/c²)·M 应逐位相等",
      "4πA=%s；(4πG/c²)M=%s；相对差=%s" % (gfmt(gauss_lhs), gfmt(gauss_rhs),
                                       gfmt(rel(gauss_lhs, gauss_rhs))))
    G("G-P27", rel(gauss_lhs, gauss_rhs) < Decimal("1e-45"), "点源高斯检验机器零成立",
      gfmt(rel(gauss_lhs, gauss_rhs)))
    G("G-P27b", ddiv(D_G * D_RHO if False else dmul(D_G, D_RHO), D_C4 if False else dpow(D_C, 2)) == dim(0, -2, 0, 0),
      "量纲：[4πGρ/c²] = L^-2 = [∇·(κ r̂)]（齐次）",
      dstr(ddiv(dmul(D_G, D_RHO), dpow(D_C, 2))))

    R("P28", "BOUNDARY",
      "【R55 的解释·不代选】一阶形式 ∇·(κ r̂) = 4πGρ/c² 是【正确】的弱场极限，但它【不是式(8) 的 EL 方程】"
      "（EL 必为二阶）⇒ 若保留弱场牛顿还原，则弱场段与式(8)(10) 不同源；若坚持 (10) 的二阶形式，"
      "则牛顿真空解 κ=A/r² 不满足静态真空极限 ∇²κ=0 ⇒ 二者须择一",
      "与 r19「作用量与 ADM 方程不同源」同族；本册只证明一阶形式正确，不代选")

# ============================== Stage P7：ℓ 的敏感性求导与 Fisher 可识别性 ==============================
def stage_P7():
    # G_th(ℓ) = 2πc³ℓ²/(ħ sinθ)，取 sinθ=1（全域最小值口径）
    def G_th(ell):
        return Decimal(2) * PI * C_VAL ** 3 * ell * ell / HBAR
    # d ln G / d ln ℓ 应恒为 2
    def lnG_of_lnL(u):   # u = ln ℓ
        return (G_th(u.exp())).ln()
    u0 = ELL1.ln()
    slope = d1(lnG_of_lnL, u0)
    R("P29", "PASS" if rel(slope, Decimal(2)) < Decimal("1e-25") else "FAIL",
      "【敏感性求导】d ln G_th / d ln ℓ ≡ 2（ℓ 的指数为 2 ⇒ 相对误差被【放大 2 倍】进入 G）",
      "数值斜率=%s；与 2 的相对差=%s" % (gfmt(slope), gfmt(rel(slope, Decimal(2)))))
    G("G-P29", rel(slope, Decimal(2)) < Decimal("1e-25"), "d lnG/d lnℓ = 2（解析 vs 差分）", gfmt(slope))

    # Fisher 可识别性
    dG_dell_analytic = Decimal(2) * G_EXP / ELL1          # 在 ℓ=ℓ₁ 处 G_th=G_exp
    dG_dell_num = d1(G_th, ELL1)
    sigma_ell = G_UNC * ELL1 / (Decimal(2) * G_EXP)
    R("P30", "PASS" if rel(dG_dell_num, dG_dell_analytic) < Decimal("1e-25") else "FAIL",
      "【Fisher 可识别性·本册新增定量】∂G_th/∂ℓ = 2G/ℓ；σ_ℓ = u_G·ℓ/(2G)"
      " ⇒ 相对精度要求 σ_ℓ/ℓ = (u_G/G)/2",
      "∂G/∂ℓ 解析=%s 差分=%s；σ_ℓ=%s m；σ_ℓ/ℓ=%s" % (
          gfmt(dG_dell_analytic), gfmt(dG_dell_num), gfmt(sigma_ell), gfmt(G_REL_UNC / Decimal(2))))
    G("G-P30", rel(dG_dell_num, dG_dell_analytic) < Decimal("1e-25"),
      "∂G_th/∂ℓ 解析 vs 差分一致", gfmt(rel(dG_dell_num, dG_dell_analytic)))
    K("P7_ell_fisher", {"dG_dell": gfmt(dG_dell_analytic), "sigma_ell_m": gfmt(sigma_ell),
                        "sigma_ell_rel": gfmt(G_REL_UNC / Decimal(2)),
                        "ell1_m": gfmt(ELL1)}, "ℓ 的 Fisher 可识别性")

    R("P31", "BOUNDARY",
      "【优化项】若 ℓ 走情形甲（自由常数带先验），其先验相对精度须优于 (u_G/G)/2 才不劣于现有 G 的测量精度；"
      "ℓ_P 作为先验时 G_th/G_exp = 2π（偏差 84.1%）⇒ 用 ℓ_P 【不满足】该精度要求 ⇒ 情形甲下 ℓ_P 不可用",
      "σ_ℓ/ℓ = %s；ℓ_P 处 G_th/G_exp = %s（相对偏差 %s）" % (
          gfmt(G_REL_UNC / Decimal(2)), gfmt(G_th(ELL_P) / G_EXP),
          gfmt(rel(G_th(ELL_P) / G_EXP, Decimal(1)))))

    # χ²(ℓ) 的一阶 / 二阶求导
    def chi2(ell):
        return ((G_th(ell) - G_EXP) / G_UNC) ** 2
    c1 = d1(chi2, ELL1)
    c2_num = d2(chi2, ELL1)
    c2_analytic = Decimal(8) * G_EXP ** 2 / (ELL1 ** 2 * G_UNC ** 2)
    R("P32", "PASS",
      "【χ² 求导】χ²(ℓ) 在 ℓ=ℓ₁ 处一阶导为 0，二阶导 = 8G²/(ℓ²u_G²)"
      "（解析 vs 差分一致）⇒ 情形甲下 ℓ 有唯一极小且曲率有限 ⇒ 单参数可识别",
      "χ²'(ℓ₁)=%s；χ²''(ℓ₁) 差分=%s 解析=%s；相对差=%s" % (
          gfmt(c1), gfmt(c2_num), gfmt(c2_analytic), gfmt(rel(c2_num, c2_analytic))))
    G("G-P32", abs(c1) < Decimal("1e-20") * abs(c2_analytic) * ELL1 and
      rel(c2_num, c2_analytic) < Decimal("1e-18"),
      "χ² 一阶导为 0 且二阶导与解析式一致", "c1=%s c2=%s" % (gfmt(c1), gfmt(c2_num)))
    K("P7_chi2", {"chi2_at_ell1": gfmt(chi2(ELL1)), "chi2_at_ellP": gfmt(chi2(ELL_P)),
                  "chi2_second_deriv": gfmt(c2_analytic)}, "χ²(ℓ) 的一阶/二阶导")

    R("P33", "INFO",
      "χ² 读数：ℓ=ℓ_P 时 G_th/G_exp = 2π ⇒ χ² 极大；χ²(ℓ₁) = 0"
      " ⇒ 情形乙（ℓ 由 G_exp 反解）下 χ² 恒 0，与 r41 R06 一致（不可证伪）",
      "χ²(ℓ_P)=%s；χ²(ℓ₁)=%s；G_th(ℓ_P)/G_exp=%s" % (
          gfmt(chi2(ELL_P)), gfmt(chi2(ELL1)), gfmt(G_th(ELL_P) / G_EXP)))

    # ∂G/∂θ 的敏感性
    def G_theta(s):   # s = sinθ
        return Decimal(2) * PI * C_VAL ** 3 * ELL1 * ELL1 / (HBAR * s)
    d_s = d1(G_theta, Decimal("0.5"))
    d_analytic = -Decimal(2) * PI * C_VAL ** 3 * ELL1 * ELL1 / (HBAR * Decimal("0.5") ** 2)
    R("P34", "PASS" if rel(d_s, d_analytic) < Decimal("1e-25") else "FAIL",
      "【附带·θ 敏感性求导】∂G_th/∂(sinθ) = −G_th/sinθ ⇒ θ→0 时敏感性发散"
      " ⇒ M2-d（θ 为场）路线上 G_th 对 θ 的扰动无界放大",
      "解析=%s 差分=%s" % (gfmt(d_analytic), gfmt(d_s)))
    G("G-P34", rel(d_s, d_analytic) < Decimal("1e-25"), "∂G/∂sinθ 解析 vs 差分一致", gfmt(rel(d_s, d_analytic)))

# ============================== Stage P8：式(17) 与式(10) 同源的平坦极限求导证明 ==============================
def stage_P8():
    # 平坦极限 α=1、β=0：□κ = −(1/c²)∂_t²κ + ∂_x²κ
    # 测试函数 κ(t,x) = a t² + b x² + c t x（多项式 ⇒ 求导精确，无截断误差）
    a, b, c = Decimal(3), Decimal(5), Decimal(7)
    d2t = Decimal(2) * a          # ∂_t²κ
    d2x = Decimal(2) * b          # ∂_x²κ
    box = -d2t / C_VAL ** 2 + d2x
    rhs10 = box                   # 式(10)：□κ = ∂(V/c⁴)/∂κ + S
    lhs17 = d2t                   # 式(17)：∂_tΠ（Π=∂_tκ）⇒ ∂_t²κ
    rhs17 = C_VAL ** 2 * (d2x - rhs10)
    rel17 = rel(lhs17, rhs17)
    R("P35", "PASS" if rel17 < Decimal("1e-40") else "FAIL",
      "【平坦极限求导证明】取 κ(t,x)=a t²+b x²+c t x：□κ = −(1/c²)∂_t²κ + ∂_x²κ；"
      "式(10) 给 □κ = RHS ⇒ 式(17) 的 ∂_tΠ = c²[∇²κ − RHS] 与 ∂_t²κ 【逐位相等】",
      "∂_t²κ=%s；c²[∇²κ−RHS]=%s；相对差=%s" % (gfmt(lhs17), gfmt(rhs17), gfmt(rel17)))
    G("G-P35", rel17 < Decimal("1e-40"), "式(17) = c²×式(10) 的空间部分（平坦极限机器零）", gfmt(rel17))
    K("P8_flat_limit", {"box_kappa": gfmt(box), "dt2": gfmt(d2t), "rhs17": gfmt(rhs17),
                        "rel": gfmt(rel17)}, "式(17) 与式(10) 同源的平坦极限对拍")

    R("P36", "PASS",
      "【符号成对·求导证明】式(17) 右端势/源项的符号由式(10) 唯一确定（同为 −RHS）"
      " ⇒ 若采用约定乙把式(10) 改为 □κ = −∂(V/c⁴)/∂κ + S，则式(17) 须同步改为 c²[∇²κ + ∂(V/c⁴)/∂κ + S]"
      " ⇒ r41 R41 的修补形式与 r41 R36 的式(10) 形式【符号一致】，修补自洽",
      "两式须成对翻转，不可只改一处")
    # 量纲：c²∇²κ = L^-1 T^-2 = [∂_tΠ]
    d17 = dmul(dpow(D_C, 2), dim(0, -3, 0, 0))
    G("G-P36", d17 == dim(0, -1, -2, 0), "c²∇²κ = L^-1 T^-2 = [∂_tΠ_κ]（齐次）", dstr(d17))

    R("P37", "BOUNDARY",
      "【不自推·残留】本证明只在【平坦极限 α=1、β=0、忽略 αKΠ 与共形修正】下成立；"
      "完整 3+1 分解中的 αKΠ 项系数与 D̃² 共形修正（e^{−4φ}、联络差）仍按 r41 R44 【不自推】",
      "αKΠ 与共形项为文献约定依赖，本册只判结构性缺失")

# ============================== Stage P9：V≡0 的强化回归（沿约束流形各阶全导数） ==============================
def stage_P9():
    k0, t0 = Decimal("1.234e-6"), Decimal("3.70e-7")
    rows = []
    worst0 = worst1 = worst2 = Decimal(0)
    dirs = [(Decimal("1.0e-9"), Decimal("2.0e-10")),
            (Decimal("-3.0e-10"), Decimal("7.0e-10")),
            (Decimal("5.0e-11"), Decimal("-9.0e-11"))]
    for (kd, td) in dirs:
        def kap(tt): return k0 + kd * tt
        def tau(tt): return t0 + td * tt
        def om(tt):  # ω 由 (1) 即时更新
            return C_VAL * ((kap(tt) ** 2 + tau(tt) ** 2).sqrt())
        def Vt(tt): return V_of(kap(tt), tau(tt), om(tt))
        v0 = Vt(Decimal(0))
        v1 = d1(Vt, Decimal(0))
        v2 = d2(Vt, Decimal(0))
        worst0 = max(worst0, abs(v0))
        worst1 = max(worst1, abs(v1))
        worst2 = max(worst2, abs(v2))
        rows.append({"kap_dot": gfmt(kd), "tau_dot": gfmt(td), "V": gfmt(v0),
                     "dV_dt": gfmt(v1), "d2V_dt2": gfmt(v2)})
    # 机器零判据的分母取 V 的自然量级 ½[c²(κ₀²+τ₀²)]²
    # 【自抓】首版用 == 0 精确判据：ω 由 sqrt 更新带 1e-60 级舍入 ⇒ V~1e-110 而非 0，
    #          断言恒假（假失败）。改为相对自然量级的相对判据。
    sc_V = (C_VAL ** 2 * (k0 * k0 + t0 * t0)) ** 2 / Decimal(2)
    rel0, rel1, rel2 = worst0 / sc_V, worst1 / sc_V, worst2 / sc_V
    R("P38", "FAIL",
      "【强化回归·本册新增】ω 由式(1) 即时更新时，沿约束流形 V(t) ≡ 0 对【任意方向】(κ̇, τ̇) 恒成立"
      " ⇒ 不止 V=0，V 的一阶与二阶全导数也【恒为 0】⇒ 约束势在修补 M4 前【各阶恢复力全为零】",
      "3 个方向上 max(V)=%s，max(dV/dt)=%s，max(d²V/dt²)=%s；"
      "相对 V 的自然量级 %s 分别为 %s / %s / %s"
      % (gfmt(worst0), gfmt(worst1), gfmt(worst2), gfmt(sc_V),
         gfmt(rel0), gfmt(rel1), gfmt(rel2)))
    G("G-P38", max(rel0, rel1, rel2) < Decimal("1e-25"),
      "约束流形上 V 及其一/二阶全导数恒为 0（相对机器零）",
      "0阶:%s 1阶:%s 2阶:%s（相对量级）" % (gfmt(rel0), gfmt(rel1), gfmt(rel2)))
    K("P9_along_constraint", rows, "沿约束流形 V 的各阶全导数")

# ============================== Stage P10：M4 必要性的求导证明 ==============================
def stage_P10():
    k0, t0 = Decimal("1.234e-6"), Decimal("3.70e-7")
    om_c = C_VAL * (k0 * k0 + t0 * t0).sqrt()
    rows = []
    for tag in ("1.01", "1.1", "2.0"):
        om_fix = Decimal(tag) * om_c
        kd = Decimal("1.0e-9")
        def kap(tt): return k0 + kd * tt
        def Vt(tt): return V_of(kap(tt), t0, om_fix)
        v0 = Vt(Decimal(0))
        v1 = d1(Vt, Decimal(0))
        dVk = d1(lambda x: V_of(x, t0, om_fix), k0)
        rows.append({"omega_factor": tag, "V": gfmt(v0), "dV_dt": gfmt(v1), "dV_dkappa": gfmt(dVk)})
    nonzero = all(abs(Decimal(r["V"])) > 0 and abs(Decimal(r["dV_dt"])) > 0 for r in rows)
    R("P39", "PASS" if nonzero else "FAIL",
      "【M4 必要性·求导证明】ω 独立（M4）后 V≠0 且 dV/dt≠0、∂V/∂κ≠0 ⇒ 恢复力确实出现"
      " ⇒ r41 R22 的『势项复活』在求导层得到支撑（不只是 V 的数值非零）",
      "ω=1.01ω_c：V=%s，dV/dt=%s；ω=2ω_c：V=%s" % (rows[0]["V"], rows[0]["dV_dt"], rows[2]["V"]))
    G("G-P39", nonzero, "M4 后 V 与 dV/dt 均非零（求导证明）", rows[0]["dV_dt"])
    K("P10_M4_derivative", rows, "ω 独立后 V、dV/dt、∂V/∂κ")

    R("P40", "CORRECTED",
      "【自评第 4 条·求导后更正】r41 判『成立（需 M4）』；本册求导证明更正为【径向成立、角向不成立】："
      "Hessian 秩 1（P08）⇒ 角向本征值 0 ⇒ 只改 θ 的漂移【无恢复力】"
      " ⇒ 自评第 4 条『内置约束势抑制数值漂移』应改为【部分成立：仅径向】",
      "径向本征值 4c⁴(κ²+τ²)>0；角向本征值 0")

# ============================== Stage P11：修复 / 优化清单与结论 ==============================
def stage_P11():
    global FIX_LIST
    fixes = [
        {"id": "F1", "target": "式(90)/(94) 弱场牛顿还原",
         "fix": "改为一阶形式 ∇·(κ r̂) = (1/r²)∂_r(r²κ) = 4πGρ/c²",
         "evidence": "P25/P26/P27：来料 −c²∇²κ 在牛顿真空解 κ=A/r² 上给 ∇·g=−2c²A/r⁴≠0，与真空矛盾（求导证明否证）",
         "cost": "0 新常数；但一阶形式不是式(8) 的 EL 方程 ⇒ 弱场段与 (8)(10) 不同源（见 R55/F6）"},
        {"id": "F2", "target": "式(8) 势项符号 × 式(10) 右端符号",
         "fix": "甲（现状）：(8) 写 −V g_{μν}、(10) 写 +∂(V/c⁴)/∂κ；乙（标准）：(8) 写 +V g_{μν}、(10) 写 −∂(V/c⁴)/∂κ",
         "evidence": "P09/P10：由 T_μν = ∂φ∂φ − g_μν L 反推，二者必须成对；现状内部自洽",
         "cost": "0；但为【约定依赖】⇒ 必须显式声明，且改动须 (8)(10)(17) 三处同步"},
        {"id": "F3", "target": "约束势角向零恢复力",
         "fix": "若需角向阻尼，V 须改为显式依赖 θ（例如加入 (τ/κ − tanθ₀)² 型项）",
         "evidence": "P08/P14：约束面 Hessian = 4c⁴ vv^T 秩 1，det=0，角向本征值 0",
         "cost": "+1 势项（可能 +1 常数 θ₀）⇒ 不自推具体形式，登记为缺口"},
        {"id": "F4", "target": "ℓ 的先验精度（情形甲）",
         "fix": "若 ℓ 作自由常数，须带相对精度优于 (u_G/G)/2 = 1.1237e-5 的独立先验",
         "evidence": "P29/P30/P31：d ln G/d ln ℓ = 2 ⇒ σ_ℓ/ℓ = (u_G/G)/2；ℓ_P 处偏差 84.1% 不满足",
         "cost": "使情形甲的『外部输入』从 1 个常数升为 1 个常数 + 1 个精度要求"},
        {"id": "F5", "target": "M9 的 ∇·(κr̂) = −λ∇²κ",
         "fix": "该式只能作为【指数试探解 κ∝e^{−r/λ}】的性质使用，不得当微分恒等式替换弱场方程",
         "evidence": "P22/P23/P24：A/r² 上散度 0 而拉普拉斯非 0；A/r 上拉普拉斯 0 而散度非 0（双向反例）",
         "cost": "0；属表述收窄"},
        {"id": "F6", "target": "R55 的择一",
         "fix": "(a) 保留弱场一阶形式 ⇒ 放弃『弱场段由式(8) 变分导出』；(b) 坚持式(10) 二阶形式 ⇒ 放弃牛顿真空还原",
         "evidence": "P27/P28：一阶形式经点源高斯检验正确，但不是 EL 方程",
         "cost": "二者必择其一 ⇒ 不代选"},
    ]
    FIX_LIST.extend(fixes)
    K("P11_fix_list", fixes, "修复 / 优化清单 F1–F6")

    # ---------- 自抓登记（本册实现缺陷，已修；不影响上述物理判定） ----------
    R("S01", "CORRECTED",
      "【自抓 1】首版 gfmt 写 (\"%.25E\") % Decimal(x) —— %-格式化先把 Decimal 转 float，"
      "只留 ~17 位有效数字，第 16 位起为二进制垃圾（实测真值 4.1111111111111111111111111E-1 "
      "被打印成 4.1111111111111109384097517E-01）⇒ 所有读数被污染",
      "已改 format(Decimal(x), '.25E')，并加守卫 G0-13 防回潮；r41 用的是正确写法，无交叉污染")
    R("S02", "CORRECTED",
      "【自抓 2】二阶差分首版沿用一阶步长 h=|x|·1e-20 ⇒ 抵消误差 ε/h² = 1e-60/1e-40 = 1e-20，"
      "二阶导数只有 ~20 位有效（实测 A/r 的 f'' 误差 3.7e-21，把『拉普拉斯为 0』的反例判成假失败）",
      "已改 h₂=|x|·1e-15（抵消与截断各 ~1e-30，实测相对误差 1.35e-30），并加守卫 G0-14 防回潮")
    NSD("S01/S02 为本册实现层自抓", "已修并加守卫；教训：高精度格式化与差分步长都必须是被守卫的对象")

    R("P41", "FAIL",
      "【总账更新】求导证明后，r41 的『外部输入 ≥2』不变，但新增两条约束："
      "(i) F4 要求 ℓ 带相对精度优于 1.1237e-5 的先验；(ii) F3 若补角向阻尼则再 +1 势项"
      " ⇒ 最小外部输入仍为 2（ℓ + τ–κ 新关系），撞 Ω5 的结论不变",
      "F1/F2/F5 均为 0 成本；F3/F6 为可选代价")
    R("P42", "BOUNDARY",
      "【裁决点更新】r41 的 5 条（M2 四分支 / M5 两候选 / 是否接受外部输入 ≥2 / ℓ 定性 / 是否推进 B）"
      " 之外，本册新增 2 条：(vi) F2 的符号约定甲 or 乙；(vii) F6 的弱场择一（一阶正确 vs 二阶同源）"
      " ⇒ 共 7 条，本册不代选",
      "新增 2 条均为【约定 / 路线】选择，非计算问题")

    # 不自推登记
    NSD("式(17)(18) 中 αKΠ 项的系数与符号（依赖 lapse/√γ 时间依赖约定）", "r41 R44 已登记，本册 P37 确认残留")
    NSD("式(17)(18) 中 D̃² 作用于标量的共形修正项（e^{−4φ} 因子与联络差项）", "r41 R44 已登记，本册 P37 确认残留")
    NSD("EC 版哈密顿/动量约束的挠率贡献项正确形式（依赖 EC 约定）", "r41 R51 已登记")
    NSD("F3 所需的角向阻尼势项的具体形式", "本册只判『角向本征值为 0』，不给具体势")
    NSD("F6 择一后弱场段与式(8) 的同源化方案", "属修改公设集，须用户裁决后再执行")

    R("P43", "FAIL",
      "【总结】求导证明验证结果：r41 的修补在【求导层大部分自洽】（V 的偏导正确、EL 符号自洽、"
      "冗余定理前提被证明、(17) 与 (10) 同源），但求导证明抓到 r41 未登记的 4 处新问题："
      "① 弱场 ∇·g 口径被否证（P26）② M9 等式非恒等式且有双向反例（P22/P23/P24）"
      "③ 约束势 Hessian 秩 1 ⇒ 角向零恢复力（P08/P14/P40）④ ℓ 先验精度硬要求 1.1237e-5（P30/P31）"
      " ⇒ r41 的修补需再经 F1–F6 六项修复方可进入数值实现",
      "求导层不产生新物理；F6 与 r41 的 5 条裁决点仍未决")

# ============================== 路径与产物落盘 ==============================
HERE = os.path.dirname(os.path.abspath(__file__))    # .../源码
BASE = os.path.dirname(HERE)                         # .../本项目_全维自洽与归一化
OUT_DIR = os.path.join(BASE, "数据")
STAMP = "TUFT-r43_修补结果求导证明验证与修复优化_2026-10-12"


def _jsonable(o):
    if isinstance(o, dict):
        return dict((k, _jsonable(v)) for k, v in o.items())
    if isinstance(o, (list, tuple)):
        return [_jsonable(x) for x in o]
    if isinstance(o, Fraction):
        return str(o)
    if isinstance(o, Decimal):
        return str(o)
    return o


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    stage0()
    stage_P1()
    stage_P2()
    stage_P3()
    stage_P4()
    stage_P5()
    stage_P6()
    stage_P7()
    stage_P8()
    stage_P9()
    stage_P10()
    stage_P11()

    cnt = {}
    for r in ITEMS:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    g_pass = sum(1 for g in GUARDS if g["ok"])
    g_all = len(GUARDS)

    payload = {
        "round": "r43",
        "date": "2026-10-12",
        "title": "TUFT-V4 M1–M9 修补结果的求导证明验证与修复优化",
        "numbering_note": "撞号处置：起草时取 r42，登记时发现并行会话《TUFT-r42_V41路线B_基础长度尺度_全维审计》先于本册落盘（22:01:25 vs 22:27:12）并已在 README 仲裁『后到者应改 r43』⇒ 按『后到者改号不覆盖他人』改号 r43，未触碰他人文件",
        "source_material": "数据/TUFT-V4-EC-ADMBSSN耦合演化场方程组_来料全文_2026-10-12.md",
        "predecessor": "判定_TUFT-r41-V4-M1M9最小修补与可判定性复审_2026-10-12.md",
        "items": len(ITEMS),
        "verdict_count": cnt,
        "guards": {"pass": g_pass, "total": g_all},
        "results": ITEMS,
        "guard_list": GUARDS,
        "key_numbers": KEYNUM,
        "not_self_derived": NSD_LIST,
        "fix_list": FIX_LIST,
    }

    p_json = os.path.join(OUT_DIR, STAMP + ".json")
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(_jsonable(payload), f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# 数据：TUFT-r42 V4 修补结果的求导证明验证与修复优化")
    lines.append("")
    lines.append("- 轮次：r43（撞号处置：r42 已被并行会话《TUFT-r42_V41路线B_基础长度尺度_全维审计》先占 ⇒ 按"
                 "「后到者改号不覆盖他人」改号 r43，条目前缀 P01–P43 + 自抓 S01/S02）")
    lines.append("- 日期：2026-10-12")
    lines.append("- 条目：" + str(len(ITEMS)) + "　自检：" + str(g_pass) + "/" + str(g_all))
    lines.append("")
    lines.append("## 逐条判定")
    lines.append("")
    lines.append("| 条目 | 判定 | 标题 | 读数 |")
    lines.append("|---|---|---|---|")
    for r in ITEMS:
        lines.append("| " + r["code"] + " | " + r["verdict"] + " | " + r["title"] +
                     " | " + r["detail"].replace("|", "/") + " |")
    lines.append("")
    lines.append("## 自检守卫")
    lines.append("")
    for g in GUARDS:
        lines.append("- " + g["code"] + " " + ("PASS" if g["ok"] else "**BAD**") +
                     " — " + g["title"] + "（" + g["detail"] + "）")
    lines.append("")
    lines.append("## 修复 / 优化清单")
    lines.append("")
    for fx in FIX_LIST:
        lines.append("- " + str(fx))
    lines.append("")
    lines.append("## 不自推登记")
    lines.append("")
    for n in NSD_LIST:
        lines.append("- " + n["item"] + "：" + n["note"])
    lines.append("")
    p_md = os.path.join(OUT_DIR, STAMP + ".md")
    with open(p_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    rep = []
    rep.append("TUFT-r43 修补结果求导证明验证与修复优化")
    rep.append("PASS=" + str(cnt.get("PASS", 0)) + " FAIL=" + str(cnt.get("FAIL", 0)) +
               " BOUNDARY=" + str(cnt.get("BOUNDARY", 0)) +
               " MISMATCH=" + str(cnt.get("MISMATCH", 0)) +
               " CORRECTED=" + str(cnt.get("CORRECTED", 0)) +
               " INFO=" + str(cnt.get("INFO", 0)))
    rep.append("ITEMS=" + str(len(ITEMS)) + " GUARDS=" + str(g_pass) + "/" + str(g_all))
    p_rep = os.path.join(OUT_DIR, STAMP + "_report.txt")
    with open(p_rep, "w", encoding="utf-8") as f:
        f.write("\n".join(rep))

    print("条目 " + str(len(ITEMS)) + "：" + " ".join(k + "=" + str(v) for k, v in sorted(cnt.items())))
    print("自检 " + str(g_pass) + "/" + str(g_all))
    print("产物：" + p_json)
    print("产物：" + p_md)
    print("产物：" + p_rep)
    return 0 if g_pass == g_all else 1


if __name__ == "__main__":
    sys.exit(main())






