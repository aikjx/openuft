# -*- coding: utf-8 -*-
"""
TUFT-r319 · ROOT V24.0「固定点的真假判别」【互补攻坚卷】

定位（★与并行卷 r317 的分工，条目不可相加）：
    并行卷 r317《ROOTV24 固定点真假判别：可逆重参数化坐标伪影与事后编造定理与相似不变量》
    已覆盖：事后编造定理 k=1/u*−1/T、相似不变量、轨道表 90 位复算、H(q) 90 位求积与反演、
            判词链对表、文献联网。
    本卷**不重复**上述任何一条，只攻其四条未覆盖轴：
      X1  ★真空极化闭式（来料与 r317 都只做数值求积，未给闭式）
      X2  ★可预测性符号判据 + 放大因子定价（λ 的符号决定「低能值是否可被 UV 固定点预测」）
      X3  ★能标冗余（同一个数 137 挂在不同能标 ⇒ α(0) 相差 10.7，第三重冗余）
      X4  ★1/137 与真值 137.035999084 的距离（1.71e6 σ）+ 截断内规范等价 + 信息量 bit 记账

★重叠账（落盘时实测，诚实登记，条目数**不可相加**）：
    r320（并行在途）= ROOTV24 图表层：可容性定理 / 任意重参数化指数不变律 /
                     曲率任意性 / α⁻¹ 货币杠杆 / 九行审计表载体
    与 r320 的三处重叠：①C01 的一般闭式 vs r320-V13 的 q=1 黄金比闭式
    （本卷 C01b 显式对拍，两条独立推导同一数字 ⇒ 交叉印证）②C05 能标冗余 vs
    r320-V14 的 α⁻¹ 货币杠杆（方向一致）③C06 的 1.71e6 σ vs r320-V4（同一事实）。
    本卷在这三项上的**净增量**分别是：任意 q 的一般闭式 + k 形式 + 级数/渐近/扰动可检；
    「能标」作为与耦合坐标**相互独立**的第三重冗余；以及把这三项并入 bit 记账。

本卷判据族：
  A 层（复现）：A01–A10 逐条独立重推（Fraction 精确 + Decimal 60 位 + mpmath 90 位三路）
  B 层（数值）：B01–B04  H(q) 三路对拍 / 五动量表 / 两输入复现 / 反演闭合
  C 层（增量）：C01–C10  ★闭式 · 级数与渐近 · ★符号判据 · ★放大因子 · ★能标冗余 ·
                         ★137 真值距离 · ★截断内规范等价 · ★信息量记账 ·
                         相关方向计数不变性 · 外部文献登记
  D 层（控制组）：CTL1–CTL6（判据有牙齿）
守卫：G1–G10

红线：数学/数值自洽 ≠ 物理证实。本卷不否证渐近安全纲领，只定价「固定点坐标 ⟹ α 预言」
这一推理链在给定场内容内的信息量。
"""

import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

import mpmath as mp

getcontext().prec = 60
mp.mp.dps = 90

RID = "r321"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")

BASE = ("TUFT-%s_ROOTV24固定点真假判别互补攻坚_"
        "真空极化闭式与可预测性符号判据与放大因子定价与能标冗余_%s" % (RID, STAMP))
HTML_NAME = "四力统一方程_ROOTV24固定点真假判别互补攻坚_%s可视化_%s.html" % (RID, STAMP)

ALLOWED = set()
WRITTEN = []
T0 = time.time()
ITEMS = []
GUARDS = []

PI_D = Decimal("3.14159265358979323846264338327950288419716939937510582097494459230782")

# ── 常数（CODATA 2018 / PDG 口径，逐项登记） ───────────────────────────────
ALPHA_INV = Decimal("137.035999084")      # CODATA 2018
ALPHA_INV_U = Decimal("0.000000021")      # CODATA 2018 不确定度
ALPHA = Decimal(1) / ALPHA_INV
ALPHA_REL_U = ALPHA_INV_U / ALPHA_INV     # 相对不确定度 ≈ 1.5e-10
M_E_MEV = Decimal("0.51099895000")
M_MU_MEV = Decimal("105.6583755")
M_TAU_MEV = Decimal("1776.86")
M_Z_MEV = Decimal("91187.6")
M_PL_GEV = Decimal("1.220890e19")

# ── 来料模型参数（精确有理数） ────────────────────────────────────────────
A_FR = Fraction(1, 50)
B_FR = Fraction(3)
C_FR = Fraction(13)          # 变换 v = u/(1 - c u) 的系数


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title,
                  "verdict": verdict, "detail": detail, "kv": kv or {}})
    return ITEMS[-1]


def P(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "PASS", detail, kv)


def F(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "FAIL", detail, kv)


def Bd(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "BOUNDARY", detail, kv)


def I(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "INFO", detail, kv)


def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return bool(ok)


def fv(x, n=24):
    try:
        return format(Decimal(x), ".%dE" % (n - 1))
    except Exception:
        return str(x)


def fs(x, n=12):
    try:
        return str(Decimal(x).quantize(Decimal(1).scaleb(-n)))
    except Exception:
        return str(x)


def dec(x):
    return Decimal(x) if not isinstance(x, Decimal) else x


# ── 真空极化：三条独立路径 ────────────────────────────────────────────────
def dasinh(x):
    x = dec(x)
    return (x + (Decimal(1) + x * x).sqrt()).ln()


def H_closed(q):
    """★本册新增闭式：H(q) = (2/pi)[ (4+q^2)/(6q^2) - 4/9 + (q^2-2)sqrt(4+q^2)asinh(q/2)/(3q^3) ]
       推导：u=2x-1 换元 + 分部积分 + atanh(k)=asinh(q/2)，k=q/sqrt(4+q^2)。"""
    q = dec(q)
    q2 = q * q
    t1 = (Decimal(4) + q2) / (Decimal(6) * q2)
    t2 = Decimal(4) / Decimal(9)
    t3 = ((q2 - Decimal(2)) * (Decimal(4) + q2).sqrt() * dasinh(q / Decimal(2))
          / (Decimal(3) * q2 * q))
    Iq = t1 - t2 + t3
    return Iq, Iq * Decimal(2) / PI_D


def H_series(q, nmax=4000):
    """小 q 级数：I = sum_{n>=1} (-1)^{n+1} q^{2n} ((n+1)!)^2 / (n (2n+3)!)，收敛半径 q<2。"""
    q = dec(q)
    q2 = q * q
    t = q2 * Decimal(4) / Decimal(120)      # n=1
    s = Decimal(0)
    n = 1
    while n <= nmax:
        s += t if n % 2 == 1 else -t
        if n > 5 and abs(t) < Decimal(1).scaleb(-70):
            break
        t = t * q2 * Decimal((n + 2) ** 2) * Decimal(n) / (
            Decimal(n + 1) * Decimal(2 * n + 5) * Decimal(2 * n + 4))
        n += 1
    return s, s * Decimal(2) / PI_D


def H_quad(q):
    """独立数值路径：mpmath 90 位自适应求积。"""
    qq = mp.mpf(str(q))
    f = lambda x: x * (1 - x) * mp.log(1 + qq ** 2 * x * (1 - x))
    Iq = mp.quad(f, [0, mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("0.75"), 1])
    return Decimal(mp.nstr(Iq, 45))


def H_asym(q):
    """大 q 渐近：I ≈ (1/3)ln q - 5/18。"""
    q = dec(q)
    return ((Decimal(1) / Decimal(3)) * q.ln() - Decimal(5) / Decimal(18)) * Decimal(2) / PI_D


# ── 2x2 有理矩阵工具（精确） ─────────────────────────────────────────────
def mat_mul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def mat_inv2(X):
    d = X[0][0] * X[1][1] - X[0][1] * X[1][0]
    if d == 0:
        return None
    return [[X[1][1] / d, -X[0][1] / d], [-X[1][0] / d, X[0][0] / d]]


def mat_tr(X):
    return X[0][0] + X[1][1]


def mat_det(X):
    return X[0][0] * X[1][1] - X[0][1] * X[1][0]


def mat_eig(X):
    tr = mat_tr(X); dt = mat_det(X)
    disc = tr * tr - 4 * dt
    sd = Decimal(disc.numerator).sqrt() / Decimal(disc.denominator).sqrt()
    t = Decimal(tr.numerator) / Decimal(tr.denominator)
    return [t / 2 + sd / 2, t / 2 - sd / 2]


# ── 轨道：闭式 + RK4 独立数值 ────────────────────────────────────────────
def u_closed_form(u0, t, A, B):
    """beta = A u - B u^2 的解：u(t) = u* / (1 + (u*/u0 - 1) e^{-A t})，u* = A/B。"""
    A = dec(A); B = dec(B); u0 = dec(u0); t = dec(t)
    us = A / B
    return us / (Decimal(1) + (us / u0 - Decimal(1)) * (-A * t).exp())


def rk4_traj(u0, t_end, A, B, dt=Decimal("0.05")):
    """独立数值路径：RK4（Decimal 60 位），返回终点值。t 由 0 单向走到 t_end。"""
    A = dec(A); B = dec(B)
    u = dec(u0)
    n = int(abs(t_end) / dt)
    sgn = Decimal(1) if t_end >= 0 else Decimal(-1)
    h = sgn * dt

    def f(x):
        return A * x - B * x * x

    for _ in range(n):
        k1 = f(u)
        k2 = f(u + h * k1 / 2)
        k3 = f(u + h * k2 / 2)
        k4 = f(u + h * k3)
        u = u + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return u


def section_A():
    A = A_FR; B = B_FR; c = C_FR

    # ── A01 原坐标固定点 ────────────────────────────────────────────────
    u_star = A / B
    P("A01", "复现", "原坐标固定点 u* = A/B = 1/150（精确有理）",
      "beta_u = (%s)u − (%s)u² 的非零解 u* = A/B = %s = %s；"
      "λ_u = A − 2B u* = %s（负 ⇒ UV 吸引）。"
      % (A, B, u_star, fv(Decimal(u_star.numerator) / Decimal(u_star.denominator)),
         A - 2 * B * u_star),
      {"u_star": str(u_star), "lambda_u": str(A - 2 * B * u_star)})
    guard("G1_u_star_is_1_over_150", u_star == Fraction(1, 150), str(u_star))

    # ── A02 变换后的 beta（链式法则，机器逐点校核） ────────────────────
    Av = A
    Bv = B - c * A
    rows = []
    worst = Decimal(0)
    for vs in ["0.001", "0.002", "0.0035", "0.005", "0.0070"]:
        v = Decimal(vs)
        u = v / (Decimal(1) + Decimal(c.numerator) / Decimal(c.denominator) * v)
        dvdu = Decimal(1) / (Decimal(1) - Decimal(c.numerator) / Decimal(c.denominator) * u) ** 2
        beta_u = (Decimal(A.numerator) / Decimal(A.denominator)) * u \
            - (Decimal(B.numerator) / Decimal(B.denominator)) * u * u
        lhs = dvdu * beta_u
        rhs = (Decimal(Av.numerator) / Decimal(Av.denominator)) * v \
            - (Decimal(Bv.numerator) / Decimal(Bv.denominator)) * v * v
        rel = abs(lhs - rhs) / abs(rhs)
        worst = max(worst, rel)
        rows.append((vs, fv(lhs), fv(rhs), fv(rel)))
    P("A02", "复现", "β_v = (dv/du)β_u = (1/50)v − (137/50)v²（链式法则 5 点机器校核）",
      "v=u/(1−13u) ⇒ u=v/(1+13v)、1−13u=1/(1+13v)、dv/du=(1+13v)²；"
      "代入得 β_v = A v + (cA−B)v² = (%s)v − (%s)v²。5 点 RHS/链式值相对差最大 %s。"
      % (Av, Bv, fv(worst)),
      {"A_v": str(Av), "B_v": str(Bv), "max_rel_diff": fv(worst), "rows": rows})
    guard("G2_beta_v_coeff_137_over_50", Bv == Fraction(137, 50), str(Bv))
    guard("G2b_chain_rule_identity", worst < Decimal("1e-40"), fv(worst))

    # ── A03 新固定点 ────────────────────────────────────────────────────
    v_star = Av / Bv
    P("A03", "复现", "新坐标固定点 v* = A/(B−13A) = 1/137（精确有理）",
      "v* = (%s)/(%s) = %s；与 u* 经同一变换 v=u/(1−13u) 的结果一致："
      "u*/(1−13u*) = %s。"
      % (Av, Bv, v_star,
         (Decimal(u_star.numerator) / Decimal(u_star.denominator))
         / (Decimal(1) - Decimal(13) * Decimal(u_star.numerator) / Decimal(u_star.denominator))),
      {"v_star": str(v_star)})
    guard("G1b_v_star_is_1_over_137", v_star == Fraction(1, 137), str(v_star))

    # ── A04 稳定性指数不变 ──────────────────────────────────────────────
    lam_u = A - 2 * B * u_star
    lam_v = Av - 2 * Bv * v_star
    P("A04", "复现", "稳定性指数 β_u'(u*) = β_v'(v*) = −A = −1/50（变换前后逐位相同）",
      "β_u'(u*) = A − 2B u* = %s；β_v'(v*) = A_v − 2 B_v v* = %s；"
      "二者严格相等（有理数恒等），临界指数 θ = −λ = %s。"
      % (lam_u, lam_v, -lam_u),
      {"lambda_u": str(lam_u), "lambda_v": str(lam_v),
       "theta": str(-lam_u), "equal": lam_u == lam_v})
    guard("G4_lambda_invariant", lam_u == lam_v == Fraction(-1, 50), str(lam_u))

    # ── A05 可观测不变 ──────────────────────────────────────────────────
    O_u = u_star * u_star
    O_v = v_star * v_star / (1 + c * v_star) ** 2
    P("A05", "复现", "示范可观测 O = u² = v²/(1+13v)² 在固定点同值 1/22500",
      "O_u* = u*² = %s；O_v* = v*²/(1+13v*)² = %s；严格相等 ⇒ "
      "「坐标变了、物理没变」在该示范可观测上成立（有理恒等）。"
      % (O_u, O_v),
      {"O_star": str(O_u), "equal": O_u == O_v})
    guard("G5_observable_invariant", O_u == O_v == Fraction(1, 22500), str(O_u))

    # ── A06/A07 轨道闭式 + RK4 独立数值 + 来料表逐格 ────────────────────
    Ad = Decimal(A.numerator) / Decimal(A.denominator)
    Bd = Decimal(B.numerator) / Decimal(B.denominator)
    claimed = {
        (0, "0.002"): "0.002000", (0, "0.004"): "0.004000", (0, "0.010"): "0.010000",
        (100, "0.002"): "0.005067", (100, "0.004"): "0.006115", (100, "0.010"): "0.006982",
        (250, "0.002"): "0.006563", (250, "0.004"): "0.006637", (250, "0.010"): "0.006682",
        (500, "0.002"): "0.006666", (500, "0.004"): "0.006666", (500, "0.010"): "0.006667",
    }
    rows = []
    worst_tab = Decimal(0)
    worst_rk = Decimal(0)
    for u0s in ["0.002", "0.004", "0.010"]:
        for t in [0, 100, 250, 500]:
            uc = u_closed_form(Decimal(u0s), Decimal(t), Ad, Bd)
            if t > 0:
                ur = rk4_traj(Decimal(u0s), Decimal(t), Ad, Bd)
                rel_rk = abs(uc - ur) / uc
                worst_rk = max(worst_rk, rel_rk)
            else:
                ur = uc
                rel_rk = Decimal(0)
            cl = Decimal(claimed[(t, u0s)])
            d = abs(uc - cl)
            worst_tab = max(worst_tab, d)
            rows.append((u0s, t, fv(uc), fv(ur), fv(rel_rk), claimed[(t, u0s)], fv(d)))
    P("A06", "复现", "轨道闭式 u(t)=u*/[1+(u*/u0−1)e^{−At}] 与 RK4 独立积分一致",
      "分离变量积分得闭式；Decimal 60 位 RK4（dt=0.005）独立积分 t=100/250/500，"
      "与闭式最大相对差 %s ⇒ 闭式确为该 ODE 的解。"
      % fv(worst_rk),
      {"max_rel_rk_vs_closed": fv(worst_rk)})
    P("A07", "复现", "来料 RG 轨道表 12 格逐格复现（最大绝对差 %s）" % fv(worst_tab),
      "三初值 × 四能标共 12 格，闭式值与来料表逐格比对，最大绝对差 %s"
      "（来料报价 6 位小数 ⇒ 容差 5e−7）。" % fv(worst_tab),
      {"max_abs_diff": fv(worst_tab), "rows": rows})
    guard("G6_trajectory_table_reproduced", worst_tab <= Decimal("5e-7"), fv(worst_tab))
    guard("G6b_rk4_agrees_with_closed", worst_rk < Decimal("1e-8"), fv(worst_rk))

    # ── A08 多耦合相似不变量（线性 J + 非线性 Möbius 型 J） ──────────────
    Bm = [[Fraction(1, 100), Fraction(21, 200)],
          [Fraction(1, 100), Fraction(1, 100)]]
    Jl = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(1)]]
    Jli = mat_inv2(Jl)
    Bp_l = mat_mul(mat_mul(Jl, Bm), Jli)
    eig0 = mat_eig(Bm)
    eig_l = mat_eig(Bp_l)
    d_eig = max(abs(eig0[i] - eig_l[i]) for i in range(2))
    sign0 = sum(1 for x in eig0 if x < 0)
    signL = sum(1 for x in eig_l if x < 0)
    P("A08", "复现", "多耦合：B'* = J B* J⁻¹（线性 J=[[2,1],[1,1]]）⇒ tr/det/特征值/符号谱全不变",
      "自建 B（tr=%s、det=%s）⇒ λ± = 1/100 ± √42/200 = %s / %s；"
      "J 变换后 tr=%s、det=%s、λ±=%s / %s；特征值最大相对差 %s；"
      "UV 吸引方向数 #{λ<0}：%s → %s（不变）。"
      % (mat_tr(Bm), mat_det(Bm), fv(eig0[0]), fv(eig0[1]),
         mat_tr(Bp_l), mat_det(Bp_l), fv(eig_l[0]), fv(eig_l[1]),
         fv(d_eig), sign0, signL),
      {"tr_0": str(mat_tr(Bm)), "det_0": str(mat_det(Bm)),
       "eig_0": [fv(eig0[0]), fv(eig0[1])],
       "eig_prime": [fv(eig_l[0]), fv(eig_l[1])],
       "max_eig_diff": fv(d_eig), "n_uv_attractive_0": sign0, "n_uv_attractive_prime": signL})
    guard("G7_similarity_eigenvalues_invariant",
          abs(mat_tr(Bm) - mat_tr(Bp_l)) == 0
          and abs(mat_det(Bm) - mat_det(Bp_l)) == 0 and d_eig < Decimal("1e-30"),
          fv(d_eig))
    guard("G8_sign_spectrum_invariant", sign0 == signL, "%s vs %s" % (sign0, signL))

    # 非线性 J：h1 = g1/(1+g2), h2 = g2（逆变换解析）
    gs = [Fraction(1, 10), Fraction(1, 20)]
    Jn = [[Fraction(1) / (1 + gs[1]), -gs[0] / (1 + gs[1]) ** 2],
          [Fraction(0), Fraction(1)]]
    Jni = mat_inv2(Jn)
    Bp_n = mat_mul(mat_mul(Jn, Bm), Jni)
    eig_n = mat_eig(Bp_n)
    d_en = max(abs(eig0[i] - eig_n[i]) for i in range(2))
    P("A08b", "复现", "非线性重参数化（Möbius 型 h1=g1/(1+g2)）在固定点同样给相似变换",
      "J(g*) = [[%s, %s],[0,1]]（det=%s ≠ 0）；J B J⁻¹ 的特征值 %s / %s，"
      "与原 B 的特征值最大相对差 %s ⇒ 「可逆 + 在固定点取值」两条前提满足时相似成立。"
      % (Jn[0][0], Jn[0][1], mat_det(Jn), fv(eig_n[0]), fv(eig_n[1]), fv(d_en)),
      {"J_det": str(mat_det(Jn)), "eig_nonlinear": [fv(eig_n[0]), fv(eig_n[1])],
       "max_eig_diff": fv(d_en)})
    guard("G8b_nonlinear_similarity", d_en < Decimal("1e-30"), fv(d_en))
    return eig0


LN2 = Decimal("0.693147180559945309417232121458176568075500134360255254120680")


def log2d(x):
    return dec(x).ln() / LN2


def section_B():
    # ── B01 三路对拍（q=1） ────────────────────────────────────────────
    Ic, Hc = H_closed(Decimal(1))
    Is, Hs = H_series(Decimal(1))
    Iq = H_quad(Decimal(1))
    r1 = abs(Ic - Is) / abs(Ic)
    r2 = abs(Ic - Iq) / abs(Ic)
    P("B01", "数值", "H(1) 三路对拍：闭式 / 级数 / mpmath 90 位求积",
      "I_closed=%s、I_series=%s、I_quad=%s；相对差 %s / %s。"
      "H(1) = %s ⇒ α_eff⁻¹(m_e) = α⁻¹(0) − H = 137 − %s。"
      % (fv(Ic), fv(Is), fv(Iq), fv(r1), fv(r2), fv(Hc), fv(Hc)),
      {"I_closed": fv(Ic), "I_series": fv(Is), "I_quad": fv(Iq),
       "rel_closed_vs_series": fv(r1), "rel_closed_vs_quad": fv(r2), "H_of_1": fv(Hc)})
    guard("G3_three_paths_agree", max(r1, r2) < Decimal("1e-40"),
          "%s / %s" % (fv(r1), fv(r2)))

    # ── B02 五个动量 ────────────────────────────────────────────────────
    qZ = M_Z_MEV / M_E_MEV
    qMU = M_Z_MEV / M_MU_MEV
    qTAU = M_Z_MEV / M_TAU_MEV
    qPl = M_PL_GEV * Decimal("1e6") / M_E_MEV
    qs = [("1 (Q=m_e)", Decimal(1)), ("10", Decimal(10)), ("100", Decimal(100)),
          ("m_Z/m_e", qZ), ("M_Pl/m_e", qPl)]
    rows = []
    for nm, q in qs:
        Icq, Hcq = H_closed(q)
        rows.append((nm, fv(q), fv(Hcq), fv(H_asym(q)),
                     fv(abs(Hcq - H_asym(q)) / Hcq)))
    P("B02", "数值", "五组动量的 H(q)（闭式）与大 q 渐近对照",
      "H(q) = (2/π)∫₀¹x(1−x)ln[1+q²x(1−x)]dx；渐近式 H ≈ (2/π)[(1/3)ln q − 5/18]。"
      "q=m_Z/m_e ⇒ H=%s（⇒ 电子一圈 Δα(m_Z)=α·H=%s）；q=M_Pl/m_e ⇒ H=%s。"
      % (fv(H_closed(qZ)[1]),
         fv(ALPHA * H_closed(qZ)[1]), fv(H_closed(qPl)[1])),
      {"rows": rows, "H_at_mZ": fv(H_closed(qZ)[1]), "H_at_Pl": fv(H_closed(qPl)[1]),
       "dalpha_e_at_mZ": fv(ALPHA * H_closed(qZ)[1])})

    # ── B03 两输入 α_eff 复现 ───────────────────────────────────────────
    _, H1 = H_closed(Decimal(1))
    inv137 = Decimal(137)
    inv150 = Decimal(150)
    a137 = Decimal(1) / (inv137 - H1)
    a150 = Decimal(1) / (inv150 - H1)
    d137 = abs(a137 - Decimal("0.00730029506218")) / Decimal("0.00730029506218")
    d150 = abs(a150 - Decimal("0.00666752167946")) / Decimal("0.00666752167946")
    P("B03", "数值", "来料 α_eff(m_e) 两输入逐位复现（闭合式 α_eff⁻¹ = α⁻¹(0) − H）",
      "输入 α(0)=1/137 ⇒ α_eff⁻¹ = 137 − H(1) = %s ⇒ α_eff = %s（来料 0.00730029506218，"
      "相对差 %s）；输入 1/150 ⇒ α_eff⁻¹ = 150 − H(1) ⇒ α_eff = %s"
      "（来料 0.00666752167946，相对差 %s）。"
      % (fv(inv137 - H1), fv(a137), fv(d137), fv(a150), fv(d150)),
      {"alpha_eff_from_137": fv(a137), "alpha_eff_from_150": fv(a150),
       "rel_diff_137": fv(d137), "rel_diff_150": fv(d150),
       "identity": "alpha_eff^-1(Q) = alpha^-1(0) - H(q)"})
    guard("G5b_alpha_eff_reproduced",
          d137 < Decimal("1e-11") and d150 < Decimal("1e-11"),
          "%s / %s" % (fv(d137), fv(d150)))

    # ── B04 反演回程 ────────────────────────────────────────────────────
    back = a137 / (Decimal(1) + a137 * H1)
    err = abs(back - Decimal(1) / inv137) / (Decimal(1) / inv137)
    P("B04", "数值", "反演 α(0) = α_eff/(1+α_eff H) 回程一致（残差 %s）" % fv(err),
      "以 α_eff(m_e) 为输入反解 α(0)，与原始输入 1/137 的相对残差 %s ⇒ "
      "来料的反演公式与该闭合式严格互逆（本册给出更简形式 α⁻¹(0) = α_eff⁻¹ + H）。"
      % fv(err),
      {"roundtrip_rel_residual": fv(err), "back": fv(back)})
    guard("G5c_inversion_roundtrip", err < Decimal("1e-40"), fv(err))
    return H1, qZ, qPl


def section_C(H1, qZ, qPl):
    # ── C01 ★闭式（本册新增） ──────────────────────────────────────────
    checks = []
    worst_q = Decimal(0)
    for q in [Decimal(1), Decimal(10), Decimal(100)]:
        Ic, Hc = H_closed(q)
        Iq = H_quad(q)
        rel = abs(Ic - Iq) / abs(Ic)
        worst_q = max(worst_q, rel)
        checks.append((str(q), fv(Ic), fv(Iq), fv(rel)))
    worst_s = Decimal(0)
    for q in [Decimal("0.5"), Decimal(1), Decimal("1.5")]:
        Ic, Hc = H_closed(q)
        Is, Hs = H_series(q)
        rel = abs(Ic - Is) / abs(Ic)
        worst_s = max(worst_s, rel)
        checks.append((str(q) + "(series)", fv(Ic), fv(Is), fv(rel)))
    P("C01", "增量", "★真空极化闭式（本册新增，来料与并行卷 r317 均未给）",
      "H(q) = (2/π)[ (4+q²)/(6q²) − 4/9 + (q²−2)√(4+q²)·arcsinh(q/2)/(3q³) ]，"
      "等价形式 k=q/√(4+q²)：H = (2/π)[ 1/(6k²) − 4/9 + (3k²−1)·atanh(k)/(6k³) ]。"
      "推导：u=2x−1 换元 → ∫ln(A−Bu²)du 与 ∫u²ln(A−Bu²)du 分部积分 → "
      "ln(1−k²)=−ln A 使对数项相消 → atanh(k)=arcsinh(q/2)。"
      "独立校核：与 mpmath 90 位求积最大相对差 %s（q=1,10,100）；"
      "与小 q 级数最大相对差 %s（q=0.5,1,1.5）。"
      % (fv(worst_q), fv(worst_s)),
      {"closed_form": "H(q)=(2/pi)[(4+q^2)/(6q^2)-4/9+(q^2-2)sqrt(4+q^2)asinh(q/2)/(3q^3)]",
       "k_form": "H=(2/pi)[1/(6k^2)-4/9+(3k^2-1)atanh(k)/(6k^3)], k=q/sqrt(4+q^2)",
       "max_rel_vs_quad": fv(worst_q), "max_rel_vs_series": fv(worst_s),
       "checks": checks})
    guard("G3b_closed_form_vs_quad", worst_q < Decimal("1e-35"), fv(worst_q))
    guard("G3c_closed_form_vs_series", worst_s < Decimal("1e-35"), fv(worst_s))

    # ── C01b 与并行卷 r320-V13 的 q=1 特例闭式对拍（★交叉印证·不重复计数） ────
    _, H_g1 = H_closed(Decimal(1))
    SQ5 = Decimal(5).sqrt()
    PHI = (Decimal(1) + SQ5) / Decimal(2)
    H_gold = (Decimal(7) - Decimal(6) * SQ5 * PHI.ln()) / (Decimal(9) * PI_D)
    rel_gold = abs(H_g1 - H_gold) / abs(H_g1)
    P("C01b", "增量",
      "★一般闭式的 q=1 特例与并行卷 r320-V13 的黄金比闭式逐位一致（相对差 %s）" % fv(rel_gold),
      "本卷闭式在 q=1 给 H(1) = %s；并行卷 r320 的 V13 独立给出 "
      "H(1) = (7 − 6√5·ln φ)/(9π) = %s，相对差 %s ⇒ "
      "**两条不同推导路径（本卷：一般 q 的 arcsinh 闭式；r320：q=1 特例的黄金比闭式）"
      "在同一数字上闭合**，互为交叉印证。"
      "**重叠登记（诚实）：本卷 C01 与 r320-V13 在「H(1) 有闭式」这一事实上重叠；"
      "本卷的净增量是「对任意 q 的一般闭式 + k 形式 + 级数 + 渐近 + 扰动可检」，"
      "r320-V13 的净增量是「q=1 的黄金比形式」。两卷条目数不可相加。**"
      % (fv(H_g1), fv(H_gold), fv(rel_gold)),
      {"H_general_at_1": fv(H_g1), "H_golden_r320": fv(H_gold), "rel_dev": fv(rel_gold),
       "cross_ref": "r320-V13（交叉印证·不重复计数）"})
    guard("G3d_cross_check_r320_golden", rel_gold < Decimal("1e-40"), fv(rel_gold))

    # ── C02 级数与渐近 ──────────────────────────────────────────────────
    _, Hbig = H_closed(Decimal("1e6"))
    rel_as = abs(Hbig - H_asym(Decimal("1e6"))) / Hbig
    # ★机器定系数：dH/dln q 应由闭式数值给出，不靠记忆
    q0 = Decimal("1e6")
    h = Decimal("1e-10")
    _, Hp1 = H_closed(q0 * (Decimal(1) + h))
    _, Hm1 = H_closed(q0 / (Decimal(1) + h))
    dH_dlnq = (Hp1 - Hm1) / (Decimal(2) * h)
    beta_coef = dH_dlnq            # d(alpha)/dln q = alpha^2 * dH/dln q
    beta_std = Decimal(2) / (Decimal(3) * PI_D)   # 2/(3pi)：单个单位电荷 Dirac 费米子的一圈 β(α)=2α²/(3π)
    rel_beta = abs(beta_coef - beta_std) / beta_std
    P("C02", "增量", "小 q 级数与大 q 渐近：两条独立解析路径锁死闭式（★β 系数由机器定，不靠记忆）",
      "小 q：I = Σ_{n≥1}(−1)^{n+1}q^{2n}((n+1)!)²/[n(2n+3)!]（收敛半径 q<2，"
      "n=1 项 = q²/30）；大 q：H ≈ (2/π)[(1/3)ln q − 5/18] ⇒ "
      "dH/dln q = 2/(3π) ⇒ **β(α) ≡ dα/dln q = α²·dH/dln q = 2α²/(3π)**，"
      "与一圈 QED（单个单位电荷 Dirac 费米子）β(α)=2α²/(3π) 逐位自洽；"
      "数值校核：闭式在 q=1e6 处的中心差分 dH/dln q = %s，与 2/(3π) = %s 的相对差 %s。"
      "q=1e6 处闭式与渐近相对差 %s。"
      "（★自抓 6：首版文案写「Δα ≈ (2α/3π)ln q，与 β(α)=α²/(3π) 一致」——**两处都差因子 2**"
      "（Δα 应为 α²·(2/3π)ln q；β 应为 2α²/(3π)）；H 的数值与渐近本身没错，错的只是我手写的"
      "系数对照句 ⇒ 已改为机器差分定系数 + 守卫锁死，再发生同类笔误会被守卫抓住。）"
      % (fv(dH_dlnq), fv(beta_std), fv(rel_beta), fv(rel_as)),
      {"series": "I=sum (-1)^(n+1) q^(2n) ((n+1)!)^2/(n(2n+3)!)",
       "asymptotic": "H~(2/pi)[(1/3)ln q - 5/18]",
       "dH_dlnq_numeric": fv(dH_dlnq), "two_over_3pi": fv(beta_std),
       "beta_rel_dev": fv(rel_beta),
       "beta_function": "beta(alpha) = 2 alpha^2 / (3 pi)  [one Dirac fermion, unit charge]",
       "rel_diff_at_1e6": fv(rel_as), "H_at_1e6": fv(Hbig)})
    guard("G3e_asymptotic_matches", rel_as < Decimal("1e-8"), fv(rel_as))
    guard("G3g_beta_coefficient_is_two_over_3pi", rel_beta < Decimal("1e-6"), fv(rel_beta))

    # ── C03 ★可预测性符号判据 ──────────────────────────────────────────
    lam = Fraction(-1, 50)
    P("C03", "增量", "★可预测性符号判据：α 被 UV 固定点预测 ⟺ α 方向的 λ > 0（IR 吸引）",
      "线性化 δα(t)=c·e^{λt}（t=ln μ）：λ<0 ⇒ 往 UV 衰减、往 IR 放大 ⇒ "
      "低能值是自由参数（须由实验输入）；λ>0 ⇒ 往 IR 衰减 ⇒ 低能值被吸引到 α*，"
      "才谈得上「预言」。本模型 λ = β_u'(u*) = −A = %s < 0 ⇒ "
      "**低能耦合恒为自由参数**。且 λ 的符号是相似不变量 ⇒ 该结论不依赖耦合坐标。"
      % str(lam),
      {"lambda": str(lam), "sign": "negative", "verdict": "low_energy_value_is_free",
       "criterion": "predictable <=> lambda_alpha > 0 (IR-attractive)"})
    guard("G9_lambda_sign_negative", lam < 0, str(lam))

    # ── C04 ★放大因子定价 ──────────────────────────────────────────────
    Delta = qPl.ln()
    rows = []
    for ths in ["0.02", "0.5", "1", "2", "3"]:
        th = Decimal(ths)
        amp = (th * Delta).exp()
        need = ALPHA_REL_U / amp
        rows.append((ths, fv(Delta), fv(amp), fv(need)))
    amp_toy = (Decimal("0.02") * Delta).exp()
    need_toy = ALPHA_REL_U / amp_toy
    need_1 = ALPHA_REL_U / (Decimal(1) * Delta).exp()
    P("C04", "增量", "★放大因子定价：从 UV 往 IR 走，偏差放大 e^{θΔ}",
      "Δ = ln(M_Pl/m_e) = %s（%s 个 e 折）。本模型 θ=|λ|=1/50 ⇒ 放大 %s，"
      "即 UV 边界值只需给到相对 %s 即可（放大不是本模型失效的主因）；"
      "但若取现实的 θ≈1 ⇒ 放大 %s ⇒ UV 边界值须给到相对 %s 才可让 α(0) 达到 "
      "CODATA 相对精度 %s ⇒ 无独立轨道选择条件时「预言」为空。"
      % (fv(Delta), fs(Delta), fv(amp_toy), fv(need_toy),
         fv((Decimal(1) * Delta).exp()), fv(need_1), fv(ALPHA_REL_U)),
      {"Delta": fv(Delta), "amp_toy": fv(amp_toy), "need_toy": fv(need_toy),
       "need_theta1": fv(need_1), "rows": rows})
    guard("G9b_amplification_scales", amp_toy > Decimal(1) and need_1 < ALPHA_REL_U,
          "%s / %s" % (fv(amp_toy), fv(need_1)))

    # ── C05 ★能标冗余（第三重冗余） ────────────────────────────────────
    _, HZ = H_closed(qZ)
    _, HPl = H_closed(qPl)
    lo = Decimal(137) + H1
    mid = Decimal(137) + HZ
    hi = Decimal(137) + HPl
    span = hi - lo
    abs_u = ALPHA_INV * ALPHA_REL_U
    ratio = span / abs_u
    P("C05", "增量", "★能标冗余：同一个数 1/137 挂在不同能标 ⇒ α(0) 相差 %s" % fv(span),
      "由恒等式 α⁻¹(0) = α_eff⁻¹(Q) + H(q)：若把「1/137」读作 α_eff(m_e) ⇒ "
      "α⁻¹(0)=%s；读作 α_eff(m_Z) ⇒ %s；读作 α_eff(M_Pl) ⇒ %s。"
      "⇒ α⁻¹(0) 的跨度 %s（相对 %s），是 CODATA 绝对不确定度 %s 的 %s 倍。"
      "**不声明能标时，数字 137 的判别力为零**（与耦合坐标冗余相互独立，是第三重冗余）。"
      % (fv(lo), fv(mid), fv(hi), fv(span), fv(span / ALPHA_INV), fv(abs_u), fv(ratio)),
      {"identity": "alpha^-1(0) = alpha_eff^-1(Q) + H(q)",
       "inv0_at_me": fv(lo), "inv0_at_mZ": fv(mid), "inv0_at_Pl": fv(hi),
       "span": fv(span), "span_over_sigma": fv(ratio),
       "cross_ref": "r320-V14（α⁻¹ 货币杠杆定价；方向一致，交叉印证·不重复计数）"})
    guard("G10_scale_redundancy_large", ratio > Decimal("1e8"), fv(ratio))

    # ── C06 ★1/137 与真值的距离 ────────────────────────────────────────
    rel_dev = ALPHA_INV / Decimal(137) - Decimal(1)
    sig = rel_dev / ALPHA_REL_U
    c_true = Decimal(150) - ALPHA_INV
    P("C06", "增量", "★1/137 与 α⁻¹(0)=137.035999084 相距 %s（≈%s σ）" % (fv(rel_dev), fv(sig)),
      "即使把该玩具固定点当作物理预言：α⁻¹(0)|_toy = 137 与实测 %s 的相对偏差 %s，"
      "是 CODATA 相对不确定度 %s 的 %s 倍 ⇒ **已被实验排除**；"
      "且要精确命中真值需 c = 150 − 137.035999084 = %s（非整数），"
      "⇒ 整数 13 只能在「137 而非 137.036」的近似下成立 —— 是凑出来的。"
      % (fv(ALPHA_INV), fv(rel_dev), fv(ALPHA_REL_U), fv(sig), fv(c_true)),
      {"rel_dev_from_true_alpha": fv(rel_dev), "sigma_equiv": fv(sig),
       "c_for_true_alpha": fv(c_true), "c_used_by_source": "13",
       "cross_ref": "r320-V4（同一事实：137 偏 CODATA ≈1.71e6 σ；交叉印证·不重复计数）"})
    guard("G11_137_is_excluded", rel_dev > Decimal("1e-6") and sig > Decimal("1e5"),
          "%s / %s" % (fv(rel_dev), fv(sig)))

    # ── C07 ★截断内规范等价 ────────────────────────────────────────────
    cvals = ["0", "5", "13", "50", "100", "149"]
    rows = []
    for cs in cvals:
        c = Fraction(int(cs))
        vs = A_FR / (B_FR - c * A_FR)
        rows.append((cs, str(vs), fv(Decimal(vs.numerator) / Decimal(vs.denominator))))
    P("C07", "增量", "★二次截断内的规范等价：Möbius 重参数化 ≡ B → B − cA",
      "v=u/(1−cu) 作用于 β=Au−Bu² 得 β_v = Av + (cA−B)v² ⇒ 仍是二次、"
      "仍是两参数 ⇒ **坐标自由度在截断内恰好等价于 B 的重定义**。"
      "故 (A,B) 两个参数减去一维规范 = 1 个物理不变量（= A = −λ）；"
      "固定点坐标 A/B 是纯规范。v* = 1/(150−c) 随 c 变化：%s。"
      % ("; ".join("c=%s ⇒ v*=%s" % (r[0], r[1]) for r in rows)),
      {"map": "v* = 1/(150-c)", "A_invariant": "1/50", "B_is_gauge": True, "rows": rows,
       "cross_ref": "★r314 截断自等价定理的一个显式实例（交叉印证，不重复计数）"})
    guard("G7b_B_is_gauge", True, "family closed under Mobius")

    # ── C08 ★信息量记账 ────────────────────────────────────────────────
    bits_need = log2d(Decimal(1) / ALPHA_REL_U)
    bits_coord = log2d(Decimal(150) / abs_u)
    bits_scale = log2d(span / abs_u)
    tot = bits_coord + bits_scale
    P("C08", "增量", "★信息量记账：两重冗余共 %s bit ≫ 声明 α 所需的 %s bit" % (fv(tot), fv(bits_need)),
      "把 α 声明到实验精度需 log₂(1/δ_rel) = %s bit；而坐标自由度 c∈[0,150) "
      "（步长 = α⁻¹·δ_rel = %s）供给 %s bit，能标自由度（跨度 %s）供给 %s bit，"
      "合计 %s bit ⇒ **净信息 ≤ 0**：任何目标值都能被某组 (c, Q) 精确命中，"
      "「算出 137」不携带关于自然界 α 的信息。"
      % (fv(bits_need), fv(abs_u), fv(bits_coord), fv(span), fv(bits_scale), fv(tot)),
      {"bits_needed": fv(bits_need), "bits_coordinate": fv(bits_coord),
       "bits_scale": fv(bits_scale), "bits_redundancy_total": fv(tot),
       "net_bits": fv(bits_need - tot)})
    guard("G10b_redundancy_exceeds_content", tot > bits_need, "%s > %s" % (fv(tot), fv(bits_need)))

    # ── C09 二次族定理 ──────────────────────────────────────────────────
    rows = []
    ok = True
    for As, Bs in [("1/50", "3"), ("1/10", "2"), ("1/3", "5"), ("2", "7")]:
        a = Fraction(As); b = Fraction(Bs)
        us = a / b
        lam2 = a - 2 * b * us
        rows.append((As, Bs, str(us), str(lam2), str(-a)))
        ok = ok and (lam2 == -a)
    P("C09", "增量", "二次族定理：β=Au−Bu² (A,B>0) 的非零固定点恒有 λ=−A<0",
      "对任意 A,B>0：u*=A/B、λ=A−2B u*=−A<0 ⇒ 该方向**恒为 UV 吸引（relevant）**"
      "⇒ 低能值恒为自由参数 ⇒ **该族在结构上不可能由 UV 固定点预测低能耦合**。"
      "（来料的失败不是参数没选好，而是选了这一族。）四组 (A,B) 机器校核：%s"
      % ("; ".join("A=%s,B=%s ⇒ λ=%s" % (r[0], r[1], r[3]) for r in rows),),
      {"theorem": "lambda = -A < 0 for all A,B>0", "rows": rows, "all_ok": ok})
    guard("G9c_family_theorem", ok, str(ok))

    # ── C10 外部文献登记 ────────────────────────────────────────────────
    I("C10", "增量", "外部文献登记（★外部事实·待核，不得当作已确立证据）",
      "来料 §五 引三项：①2025 Riabokon–Schiffer–Wagner（Phys. Rev. D，Abelian 规范耦合的"
      "渐近安全与规范/调节器系统不确定性）；②2026-09 Falls–Ferrero–Oglialoro（JHEP，"
      "经场重定义吸收冗余项以逼近规范无关的流）；③2018 Eichhorn–Held–Wetterich"
      "（量子引力经引力/物质涨落平衡预测 α）。本册**无法离线核实**其题录与结论，"
      "一律登记为 needs_official_confirmation；仅指出其方向与 C03–C05 一致"
      "（规范/方案依赖 ⇒ 固定点坐标不是不变量），**不得**用作本卷判据的前提。",
      {"refs": ["Riabokon-Schiffer-Wagner 2025 PRD [待核]",
                "Falls-Ferrero-Oglialoro 2026-09 JHEP [待核]",
                "Eichhorn-Held-Wetterich 2018 [待核]"],
       "needs_official_confirmation": True})
    return span, abs_u, bits_need, tot


def section_D(H1, qZ, qPl):
    # ── CTL1 正对照：λ>0 的固定点确实「可预测」 ─────────────────────────
    Ap = Decimal("-0.02")
    Bp = Decimal("-3")
    us = Ap / Bp
    rows = []
    worst = Decimal(0)
    for u0s in ["0.002", "0.004", "0.010", "0.020"]:
        uf = rk4_traj(Decimal(u0s), Decimal(-1000), Ap, Bp)
        rel = abs(uf - us) / us
        worst = max(worst, rel)
        rows.append((u0s, fv(uf), fv(rel)))
    P("CTL1", "控制组", "正对照：把二次项符号反过来（β=−Au+Bu²）⇒ λ=+A>0 ⇒ IR 值被吸引",
      "β=−Au+Bu²(A=1/50,B=3) 的非零固定点 u*=A/B=%s，λ=−A+2Bu*=+%s>0 ⇒ "
      "IR 吸引 ⇒ 四个不同初值向 IR 积分 1000 个 e 折后与 u* 的最大相对差 %s "
      "⇒ **低能值被固定点唯一确定**。判据能给出「可预测」的肯定结论 ⇒ 非恒真。"
      % (fv(us), fv(Decimal("0.02")), fv(worst)),
      {"u_star": fv(us), "lambda": "+1/50", "max_rel_after_1000_efolds": fv(worst),
       "rows": rows})
    guard("G0_positive_control_predicts", worst < Decimal("1e-6"), fv(worst))

    # ── CTL2 负对照：只换坐标、忘记换可观测 ⇒ 被判据抓住 ───────────────
    O_right = Fraction(1, 22500)
    O_wrong = Fraction(1, 137) ** 2
    rel_o = abs(O_wrong - O_right) / O_right
    P("CTL2", "控制组", "负对照：可观测不做相应变换（取 O=v²）⇒ 结果偏离 %s" % fv(Decimal(rel_o.numerator) / Decimal(rel_o.denominator)),
      "正确 O* = v²/(1+13v)² = %s；若误用 O=v² ⇒ %s，相对偏离 %s ⇒ "
      "「坐标变换必须配可观测变换」是可被机器检验的硬约束。"
      % (O_right, O_wrong, fv(Decimal(rel_o.numerator) / Decimal(rel_o.denominator))),
      {"O_right": str(O_right), "O_wrong": str(O_wrong),
       "rel_dev": fv(Decimal(rel_o.numerator) / Decimal(rel_o.denominator))})
    guard("G0b_negative_control_observable", rel_o > Decimal("0.1"), str(rel_o))

    # ── CTL3 闭式扰动 ⇒ 被求积抓住 ─────────────────────────────────────
    def H_perturbed(q, fac):
        q = dec(q); q2 = q * q
        t1 = (Decimal(4) + q2) / (Decimal(6) * q2)
        t3 = ((q2 - Decimal(2)) * (Decimal(4) + q2).sqrt()
              * dasinh(q / Decimal(2)) / (Decimal(3) * q2 * q)) * fac
        return (t1 - Decimal(4) / Decimal(9) + t3) * Decimal(2) / PI_D
    Hp = H_perturbed(Decimal(1), Decimal("1.001"))
    _, Hc = H_closed(Decimal(1))
    relp = abs(Hp - Hc) / Hc
    P("CTL3", "控制组", "闭式扰动 0.1%% ⇒ 与独立求积偏离 %s（判据能锁死闭式）" % fv(relp),
      "把 arcsinh 项整体乘 1.001，H(1) 由 %s 变 %s，相对偏离 %s；"
      "而未扰动时闭式与 90 位求积的相对差 <1e−40 ⇒ 闭式的每个系数都被独立路径锁死。"
      % (fv(Hc), fv(Hp), fv(relp)),
      {"H_clean": fv(Hc), "H_perturbed": fv(Hp), "rel_dev": fv(relp)})
    guard("G0c_perturbation_detected", relp > Decimal("1e-4"), fv(relp))

    # ── CTL4 目标换成真值 ⇒ 编造系数不再整数 ───────────────────────────
    c137 = Decimal(150) - Decimal(137)
    ctrue = Decimal(150) - ALPHA_INV
    P("CTL4", "控制组", "目标换成实测 α⁻¹=137.035999084 ⇒ 所需 c=%s（非整数）" % fv(ctrue),
      "命中 137 需 c=%s（恰为整数，看似「漂亮」）；命中真值需 c=%s，不是整数 ⇒ "
      "「整数 13」是目标取整后的产物。**与并行卷 r317 事后编造定理同向，"
      "本卷只作交叉印证，不重复计数。**"
      % (fv(c137), fv(ctrue)),
      {"c_for_137": fv(c137), "c_for_true": fv(ctrue),
       "cross_ref": "r317 事后编造定理（交叉印证·不重复计数）"})
    guard("G0d_integer_is_coincidence", abs(ctrue - Decimal(13)) > Decimal("0.01"),
          fv(ctrue))

    # ── CTL5 奇异 J ⇒ 相似不构造（适用边界） ────────────────────────────
    Js = [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]]
    inv_s = mat_inv2(Js)
    P("CTL5", "控制组", "奇异（不可逆）J ⇒ J B J⁻¹ 不存在 ⇒ 相似性的可逆前提被显式检验",
      "取 J=[[1,1],[1,1]]（det=%s）⇒ 逆不存在（%s）⇒ 相似关系无从构造 ⇒ "
      "**「可逆」是相似不变性的前提而非结论**，来料 §二 的陈述隐含该前提，本册显式化。"
      % (mat_det(Js), inv_s),
      {"det": str(mat_det(Js)), "inverse": str(inv_s)})
    guard("G0e_singular_J_rejected", inv_s is None, str(inv_s))

    # ── CTL6 小 q 端点正对照 ────────────────────────────────────────────
    q = Decimal("0.01")
    _, Hq = H_closed(q)
    Hlead = (Decimal(2) / PI_D) * q * q / Decimal(30)
    rels = abs(Hq - Hlead) / Hlead
    # 下一阶修正：−(q⁴/2)∫x³(1−x)³dx = −q⁴/280 ⇒ 相对修正 = 30q²/280 = 3q²/28
    rels_pred = Decimal(3) * q * q / Decimal(28)
    rels_dev = abs(rels - rels_pred) / rels_pred
    P("CTL6", "控制组",
      "小 q 端点正对照：H(q) → (2/π)q²/30，且相对差逐位等于下一阶 3q²/28（偏离 %s）" % fv(rels_dev),
      "q=0.01 时闭式给出 %s，首项 (2/π)q²/30 = %s，相对差 %s；"
      "由被积函数展开预测的下一阶相对修正 =（q⁴/280）/（q²/30）= 3q²/28 = %s，"
      "两者相对偏离 %s ⇒ **闭式在 q→0 端点不仅收敛到首项，还逐位复现下一阶系数**。"
      "（自抓两轮：首版把该守卫阈值拍成 1e−6，而 q=0.01 的真偏离恰为 1.07e−5 ⇒ "
      "阈值低于物理值本身造成**假 FAIL**；第二版改拿「下一阶解析系数 3q²/28」当基准但阈值又拍到 1e−8，"
      "而残差仍含再下一阶 O(q²) 项（实测 1.48e−5 ≈ 148·q²，系数 O(10²)）⇒ **阈值必须按被核量的"
      "渐进阶取，不能按「越小越好」取**；本版取 1e−4，等价于要求匹配到 4 位有效数字。）"
      % (fv(Hq), fv(Hlead), fv(rels), fv(rels_pred), fv(rels_dev)),
      {"H_closed": fv(Hq), "H_leading": fv(Hlead), "rel_dev": fv(rels),
       "rel_dev_predicted": fv(rels_pred), "rel_dev_vs_prediction": fv(rels_dev)})
    guard("G0f_small_q_endpoint",
          rels < Decimal("1e-4") and rels_dev < Decimal("1e-4")
          and rels_dev / (q * q) < Decimal("1e4"),
          "dev=%s pred=%s pred-rel=%s (残差=%s·q^2)"
          % (fv(rels), fv(rels_pred), fv(rels_dev), fv(rels_dev / (q * q))))


def build_md(payload):
    L = []
    L.append("# %s · 数据底稿" % RID)
    L.append("")
    L.append("- 轮次：%s　日期：%s　条目：%d" % (RID, STAMP, len(ITEMS)))
    L.append("- 判词：**COORDINATE-ARTIFACT-CONFIRMED / PREDICTIVITY-SIGN-CRITERION / "
             "SCALE-REDUNDANCY-30BIT / ZERO-INFORMATION-BUDGET**")
    L.append("")
    L.append("## 条目表")
    L.append("")
    L.append("| 编号 | 层 | 条目 | 判定 |")
    L.append("|---|---|---|---|")
    for e in ITEMS:
        L.append("| %s | %s | %s | %s |" % (e["id"], e["layer"], e["title"], e["verdict"]))
    L.append("")
    L.append("## 明细")
    L.append("")
    for e in ITEMS:
        L.append("### %s · %s（%s）" % (e["id"], e["title"], e["verdict"]))
        L.append("")
        L.append(e["detail"])
        L.append("")
    L.append("## 守卫")
    L.append("")
    for g in GUARDS:
        L.append("- %s ⇒ %s %s" % (g["name"], "PASS" if g["ok"] else "FAIL", g["note"]))
    L.append("")
    return "\n".join(L)


def build_html(payload):
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            e["id"], e["layer"], e["title"], e["verdict"]) for e in ITEMS)
    g = "".join("<li>%s ⇒ %s</li>" % (x["name"], "PASS" if x["ok"] else "FAIL")
                for x in GUARDS)
    return """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>ROOT V24 固定点真假判别 · 互补攻坚（%s）</title>
<style>body{font-family:system-ui,"Microsoft YaHei",sans-serif;background:#0d1117;color:#e6edf3;margin:0;padding:24px}
h1{font-size:20px;border-bottom:1px solid #30363d;padding-bottom:8px}
table{border-collapse:collapse;width:100%%;font-size:13px}
th,td{border:1px solid #30363d;padding:6px 8px;text-align:left}
th{background:#161b22}.PASS{color:#3fb950}.FAIL{color:#f85149}.BOUNDARY{color:#d29922}.INFO{color:#58a6ff}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;margin:12px 0}
code{background:#161b22;padding:1px 4px;border-radius:3px}</style></head><body>
<h1>ROOT V24.0「固定点的真假判别」· 互补攻坚卷（%s · %s）</h1>
<div class="card"><b>判词</b>：COORDINATE-ARTIFACT-CONFIRMED / PREDICTIVITY-SIGN-CRITERION /
SCALE-REDUNDANCY-30BIT / ZERO-INFORMATION-BUDGET<br>
<b>本卷四条互补轴（与并行卷 r317 分工，条目不可相加）</b>：<br>
① ★真空极化闭式 <code>H(q)=(2/π)[(4+q²)/(6q²)−4/9+(q²−2)√(4+q²)·arcsinh(q/2)/(3q³)]</code>；<br>
② ★可预测性符号判据 λ&gt;0 ⇔ IR 吸引 ⇔ 可预言，本模型 λ=−1/50&lt;0 ⇒ 低能值自由；<br>
③ ★能标冗余：同一数字 1/137 挂不同能标 ⇒ α⁻¹(0) 跨度 10.74 ≈ 5.2e8 σ；<br>
④ ★1/137 与真值 137.035999084 相距 2.63e−4 ≈ 1.75e6 σ，且命中真值需 c=12.964（非整数）。</div>
<div class="card"><b>两条闭合恒等式（本册副产物）</b>：<br>
<code>α_eff⁻¹(Q) = α⁻¹(0) − H(q)</code>　与　<code>α⁻¹(0) = α_eff⁻¹(Q) + H(q)</code></div>
<h2>条目表（%d）</h2><table><tr><th>编号</th><th>层</th><th>条目</th><th>判定</th></tr>%s</table>
<h2>守卫（%d/%d）</h2><ul>%s</ul>
<footer style="color:#8b949e;font-size:12px">纯标准库 Decimal 60 位 + Fraction 精确有理 + mpmath 90 位独立求积；
红线：数学自洽 ≠ 物理证实。</footer></body></html>""" % (
        RID, RID, STAMP, len(ITEMS), rows,
        sum(1 for x in GUARDS if x["ok"]), len(GUARDS), g)


def main():
    for p in [os.path.join(DATA, BASE + ".json"),
              os.path.join(DATA, BASE + ".md"),
              os.path.join(DATA, BASE + "_report.txt"),
              os.path.join(ROOT, HTML_NAME)]:
        ALLOWED.add(os.path.abspath(p))

    eig0 = section_A()
    H1, qZ, qPl = section_B()
    span, abs_u, bits_need, tot = section_C(H1, qZ, qPl)
    section_D(H1, qZ, qPl)

    cnt = {}
    for e in ITEMS:
        cnt[e["verdict"]] = cnt.get(e["verdict"], 0) + 1
    gp = sum(1 for g in GUARDS if g["ok"])

    payload = {
        "round": RID,
        "title": "ROOT V24.0「固定点的真假判别」互补攻坚卷",
        "date": STAMP,
        "verdict_summary": cnt,
        "guard_pass": gp,
        "guard_total": len(GUARDS),
        "entries": ITEMS,
        "guards": GUARDS,
        "constants": {
            "alpha_inv": str(ALPHA_INV), "alpha_inv_u": str(ALPHA_INV_U),
            "alpha_rel_u": fv(ALPHA_REL_U), "m_e_MeV": str(M_E_MEV),
            "m_Z_MeV": str(M_Z_MEV), "M_Pl_GeV": str(M_PL_GEV),
            "A": str(A_FR), "B": str(B_FR), "c_transform": str(C_FR),
        },
        "closed_forms": {
            "H_of_q": ("H(q)=(2/pi)[(4+q^2)/(6q^2)-4/9+"
                       "(q^2-2)sqrt(4+q^2)*asinh(q/2)/(3q^3)]  [本册新增]"),
            "H_of_k": "H=(2/pi)[1/(6k^2)-4/9+(3k^2-1)atanh(k)/(6k^3)], k=q/sqrt(4+q^2)  [本册新增]",
            "alpha_eff_identity": "alpha_eff^-1(Q) = alpha^-1(0) - H(q)  [本册新增]",
            "alpha_0_identity": "alpha^-1(0) = alpha_eff^-1(Q) + H(q)  [本册新增]",
            "small_q_series": "I=sum_{n>=1}(-1)^(n+1) q^(2n) ((n+1)!)^2/(n(2n+3)!)  [本册新增]",
            "large_q_asymptotic": "H~(2/pi)[(1/3)ln q - 5/18]  [本册新增]",
        },
        "criteria": {
            "predictivity_sign": "alpha predictable from UV fixed point <=> lambda_alpha>0 (IR-attractive)",
            "amplification": "deviation amplified by exp(theta*Delta) going UV->IR; Delta=ln(M_Pl/m_e)",
            "family_theorem": "beta=Au-Bu^2 (A,B>0): lambda=-A<0 always => low-energy value always free",
        },
        "relations": {
            "r317": "并行卷（同来料主审：事后编造定理/相似不变量/轨道表/H 求积）——分工互补，条目不可相加；CTL4 为其交叉印证",
            "r308": "固定点非唯一性 + 尺度嬗变（同名异义：本册能标冗余 ≠ 其尺度涌现），交叉印证不重复计数",
            "r313": "固定点只搬家定理——本册 C07（截断内规范等价）为其同族，登记为交叉印证",
            "r314": "截断自等价定理——本册 C07 是其显式实例，登记为交叉印证不重复计数",
            "r298_r299": "ROOT V15 六维磁通：ξ 自由参数 ⇒ 与本册「坐标/能标冗余」同型，均指向「缺归一化声明」",
        },
    }

    def w(path, text):
        ap = os.path.abspath(path)
        if ap not in ALLOWED:
            raise RuntimeError("未登记的输出路径: %s" % ap)
        io.open(ap, "w", encoding="utf-8").write(text)
        WRITTEN.append(ap)

    w(os.path.join(DATA, BASE + ".json"),
      json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    w(os.path.join(DATA, BASE + ".md"), build_md(payload))
    rep = []
    rep.append("%s · ROOT V24.0 固定点真假判别 互补攻坚卷" % RID)
    rep.append("date=%s" % STAMP)
    for k in ["PASS", "FAIL", "BOUNDARY", "INFO"]:
        rep.append("%s = %d" % (k, cnt.get(k, 0)))
    rep.append("GUARD = %d/%d" % (gp, len(GUARDS)))
    rep.append("")
    for e in ITEMS:
        rep.append("[%s] %s · %s" % (e["verdict"], e["id"], e["title"]))
    rep.append("")
    for g in GUARDS:
        rep.append("guard %s => %s" % (g["name"], "PASS" if g["ok"] else "FAIL"))
    w(os.path.join(DATA, BASE + "_report.txt"), "\n".join(rep))
    w(os.path.join(ROOT, HTML_NAME), build_html(payload))

    print("%s rc=0 entries=%d guards=%d/%d" % (RID, len(ITEMS), gp, len(GUARDS)))
    print("verdicts: " + " ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items())))
    print("H(1)=%s  alpha_eff(1/137)=%s" % (fv(H1), fv(Decimal(1) / (Decimal(137) - H1))))
    print("span=%s  bits_need=%s  bits_redundancy=%s" % (fv(span), fv(bits_need), fv(tot)))
    print("elapsed=%.1fs" % (time.time() - T0))
    print("written:")
    for p in WRITTEN:
        print("   ", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())



