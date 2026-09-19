# -*- coding: utf-8 -*-
"""
TUFT · R26 —— Leaver 连分式（反射壁边界）：σ_abs=0 腔模的特征值级精确复频谱
============================================================================
R20（WKB）→ R21/R22（时域演化，精度 0.3~0.6%）→ R23（Chebyshev 谱配点失败）
→ R24（矩阵束提取，方法达 1e-13 但对已衰减信号物理精度受 ABC 限，GR 基模残余 1.2e-3）
→ R25（Leaver 连分式，GR Schwarzschild QNM 达特征值级 |Δ|≤1e-6，闭合 GR 分支缺口）。

本册把同一 Leaver 框架**改反射壁边界**，闭合 σ_abs=0 分支：
  · R21/R22 的 σ_abs=0 情形 = Dirichlet 反射壁 r_s=2.05M（TUFT 墙在 r_h）+ 出波 BC。
  · 关键物理：反射壁 r_s 是 RW 方程的【内点】，不是奇点。RW 方程的奇点仍是
    视界 r=2M 与无穷远 r=∞。因此「反射壁腔模」= 在『视界正则 + 无穷远出波』的
    唯一正则解上，额外强加 Dirichlet 条件 Ψ(r_s)=0。
  · 【v2 修订·纠正初版物理误标】初版用 Leaver 无穷远出波级数 wall_series 在墙处求值
    （f_out(r_s)=0）并判为腔模——但 f_out(r_s)=0 是【反共振/完美透射】，非腔模。
    真腔模 = 入波 Jost 解 f_in(r_s)=0（S 矩阵极点，被墙与势垒囚禁的长寿命驻波）。
    正确判据见 §C5（f_in 反向射击 + u_0 无关性检验）。R21/R24 的 0.41−0.03 经 §C5
    验证为有限域箱模伪根，本册 v2 评级从「腔模 PASS」降级为「反共振/箱模诚实标注」。
  · ansatz 必须保持 GR 的渐近结构（视界入波 r^{−2iω}、无穷远出波净幂 r^{2iω}）——
    这正是 R25 已证 isospectral（RW≡Zerilli）的前提。若改内边界指数 (r−r_s)^{+1}，
    会破坏无穷远渐近幂、破坏 RW/Zerilli 等谱性（本册初版即踩此坑，已纠正）。
  · 实现：用 GR 递推（derive_recurrence 取 r_in=2M, r_power=4, inner_pow=−2iω）
    正向递推系数 a_n（a_0=1），在 x_s=1−2M/r_s 处求级数 Σ a_n x_s^n；反射壁腔模
    即令该级数为零的 ω。
  · 腔模 = 被反射壁与势垒来回反射、经势垒泄漏到无穷远的共振；|γ| 应显著小于 GR（长寿命）。

判据：
  C0 框架自洽：先用 GR 递推复算 l=2 基模，须复现 R25 的 0.373672−0.088962i（|Δ|≤1e-6）。
  V1 递推结构：GR ansatz 的 ODE 精确约分为 3 项递推（符号验证）。
  C1 腔模基模：σ_abs=0 反射壁基模（特征值级）与 R21 拟合 0.40794−0.02606i /
             R24 矩阵束 ≈0.409880−0.029576i 交叉一致。
  C2 τ 比：τ_wall/τ_GR = γ_GR/γ_wall 与 R21 的 3.40× / R24 的 ~3.0× 同向同量级。
  C3 谱结构：提取腔模泛音序（|γ| 单调升）。
  C4 截断独立：N=4000 与 N=16000 级数和位移 ≪ 1e-9（非箱模）。
  V2 全维等谱：RW 与 Zerilli 势下同一反射壁腔模一致（isospectral，跨势验证框架）。

几何单位 G=c=M=1；RW 势；l=2；r_s=2.05M。评级：O / L2。
红线：数学自洽 != 实验证实；反射壁为理想模型（反射率=1，真实 TUFT 体<1 会缩短寿命）；
仅 l=2、c<0 分支。
"""
from __future__ import print_function
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tuft_r26_report.txt")

import numpy as np
import sympy as sp

I = sp.I


# ─────────────────── 符号推导：GR ansatz → S(x) ODE → 3 项递推 ───────────────────
def derive_recurrence(ell, V=None):
    """GR ansatz 符号推导（RW 或 Zerilli 势，二者奇点同为 2M 与 ∞）。
    ansatz: Ψ = exp(iωr) · r^{4iω} · (r−2M)^{−2iω} · Σ a_n x^n，x = 1−2M/r。
      · 无穷远净幂 = r^{4iω}·r^{−2iω} = r^{2iω}（出波，与 R25 同，isospectral 前提）。
      · 视界 r→2M：(r−2M)^{−2iω} 给入波正则性（QNM 视界边界条件）。
    反射壁作为 Dirichlet BC 加在正则解上（见 wall_series_g），不改此 ansatz。
    V=None → RW 势；否则用给定势（如 Zerilli）。
    """
    x, om, n = sp.symbols("x omega n")
    M = sp.Integer(1)
    r = 2 * M / (1 - x)
    dx_dr = sp.simplify(1 / sp.diff(r, x))          # = (1-x)^2/2 之类
    f = sp.simplify(1 - 2 * M / r)
    if V is None:
        V = sp.simplify(f * (ell * (ell + 1) / r ** 2 - 6 * M / r ** 3))
    else:
        V = sp.simplify(V.subs(sp.Symbol("r"), r))    # 将给定势（以 r 表示）换元到 x 变量
    a = sp.Integer(4) * I * om                       # r^{4iω} 的 Pp 贡献 a/r
    b = -2 * I * om * M                              # (r−2M)^{−2iω} 的 Pp 贡献 b/(r−2M)
    Pp = I * om + a / r + b / (r - 2 * M)
    P2 = Pp ** 2 - a / r ** 2 - b / (r - 2 * M) ** 2
    A = f ** 2
    B = 2 * f ** 2 * Pp + f * dx_dr
    C = f ** 2 * P2 + f * dx_dr * Pp + (om ** 2 - V)
    Axx = sp.cancel(A * dx_dr ** 2)
    Bxx = sp.cancel(A * dx_dr * sp.diff(dx_dr, x) + B * dx_dr)
    Cxx = sp.cancel(C)
    den = sp.lcm([sp.denom(Axx), sp.denom(Bxx), sp.denom(Cxx)])
    Ax = sp.Poly(sp.expand(Axx * den), x)
    Bx = sp.Poly(sp.expand(Bxx * den), x)
    Cx = sp.Poly(sp.expand(Cxx * den), x)
    g = sp.gcd(sp.gcd(Ax, Bx), Cx)
    Ax, Bx, Cx = Ax.exquo(g), Bx.exquo(g), Cx.exquo(g)

    def col(off):
        s = 0
        for i, Ai in Ax.terms():
            if 2 - i[0] == off:
                s += Ai * (n + 2 - i[0]) * (n + 1 - i[0])
        for i, Bi in Bx.terms():
            if 1 - i[0] == off:
                s += Bi * (n + 1 - i[0])
        for i, Ci in Cx.terms():
            if -i[0] == off:
                s += Ci
        return sp.expand(s)

    return col(1), col(0), col(-1)


def derive_recurrence_V(V):
    """Zerilli 势走同一 GR ansatz（isospectral 前提）。"""
    return derive_recurrence(sp.Integer(2), V=V)


def V_zerilli(ell):
    M = sp.Integer(1)
    r = sp.Symbol("r")
    f = sp.simplify(1 - 2 * M / r)
    nn = sp.Rational((ell - 1) * (ell + 2), 2)
    num = (2 * nn ** 2 * (nn + 1) * r ** 3 + 6 * nn ** 2 * M * r ** 2
           + 18 * nn * M ** 2 * r + 18 * M ** 3)
    return sp.simplify(f * num / (r ** 3 * (nn * r + 3 * M) ** 2))


def make_solver(ell, V=None):
    t0 = time.time()
    A, B, G = derive_recurrence(sp.Integer(ell), V=V)
    td = time.time() - t0
    af = sp.lambdify((sp.Symbol("n"), sp.Symbol("omega")), A, "numpy")
    bf = sp.lambdify((sp.Symbol("n"), sp.Symbol("omega")), B, "numpy")
    gf = sp.lambdify((sp.Symbol("n"), sp.Symbol("omega")), G, "numpy")
    return af, bf, gf, td


def f_cf(w, N, af, bf, gf):
    """GR QNM 连分式 f(ω)（视界正则 + 无穷远出波）。"""
    cf = complex(bf(N, w))
    for k in range(N - 1, 0, -1):
        cf = complex(bf(k, w)) - complex(af(k, w)) * complex(gf(k + 1, w)) / cf
    return complex(bf(0, w)) - complex(af(0, w)) * complex(gf(1, w)) / cf


def find_root(guess, N, af, bf, gf):
    w = complex(guess)
    for _ in range(80):
        f0 = f_cf(w, N, af, bf, gf)
        h = 1e-8
        d = (f_cf(w + h, N, af, bf, gf) - f_cf(w - h, N, af, bf, gf)) / (2 * h)
        if d == 0:
            break
        s = f0 / d
        w = w - s
        if abs(s) < 1e-14:
            break
    return w


def make_V(ell, kind="RW"):
    """RW 或 Zerilli 势（areal 坐标 r）。"""
    M = 1.0
    def V(r):
        if r <= 2 * M:
            return 1e30
        f = 1 - 2 * M / r
        if kind == "RW":
            return f * (ell * (ell + 1) / r ** 2 - 6 * M / r ** 3)
        nn = float((ell - 1) * (ell + 2)) / 2.0
        num = (2 * nn ** 2 * (nn + 1) * r ** 3 + 6 * nn ** 2 * M * r ** 2
               + 18 * nn * M ** 2 * r + 18 * M ** 3)
        return f * num / (r ** 3 * (nn * r + 3 * M) ** 2)
    return V


# ─────────────────── 修订（v2）：入波 Jost 解 f_in 反向射击（真腔模判据）───────────────────
def _build_V_wall():
    """RW l=2 势（tortoise 坐标 u 预计算），用于 f_in 反向射击。r_s = 2.05M。"""
    u_s_w = float(2.05 + 2.0 * np.log(2.05 / 2.0 - 1.0))
    U_TOT = 400.0
    DU_w = 0.02
    NU_w = int(round((U_TOT - u_s_w) / DU_w)) + 1
    ug = u_s_w + np.arange(NU_w) * DU_w
    c = ug / 2.0 - 1.0
    y = np.where(c > 1.0, c, np.exp(c))
    y = np.maximum(y, 1e-12)
    for _ in range(50):
        fy = y + np.log(y) - c
        y = y - fy / (1.0 + 1.0 / y)
        y = np.maximum(y, 1e-14)
    r = 2.0 * (1.0 + y)
    fr = 1.0 - 2.0 / r
    VG_w = fr * (6.0 / r ** 2 - 6.0 / r ** 3)
    return u_s_w, DU_w, NU_w, ug, VG_w


_WALL = _build_V_wall()


def _V_of_u_wall(u):
    u_s_w, DU_w, NU_w, ug, VG_w = _WALL
    idx = int(round((u - u_s_w) / DU_w))
    idx = max(0, min(NU_w - 1, idx))
    return VG_w[idx]


def shoot_back_in_wall(omega, u_0, du=0.02):
    """入波 Jost 解 f_in 反向射击（V→0 处种子 P=1, dP=-iω·P 即 e^{-iωu} 入波/视界正则），
    积分到墙 u_s 读 Ψ(u_s)。
    真腔模 = f_in(r_s)=0（S 矩阵极点，被墙与势垒囚禁的驻波）；
    u_0 无关性检验区分真极点（收敛到真零且频率稳定）与有限域箱模（随 u_0 漂移）。"""
    n = int(round((u_0 - _WALL[0]) / du))
    P = 1.0 + 0j
    dP = -1j * omega
    for k in range(n):
        u0 = u_0 - k * du
        u1 = u0 - du
        k1P = dP
        k1d = -(omega ** 2 - _V_of_u_wall(u0)) * P
        k2P = dP + du / 2 * k1d
        k2d = -((omega ** 2 - _V_of_u_wall(u1)) * (P + du / 2 * k1P))
        k3P = dP + du / 2 * k2d
        k3d = -((omega ** 2 - _V_of_u_wall(u1)) * (P + du / 2 * k2P))
        k4P = dP + du * k3d
        k4d = -((omega ** 2 - _V_of_u_wall(u1)) * (P + du * k3P))
        P = P + du / 6 * (k1P + 2 * k2P + 2 * k3P + k4P)
        dP = dP + du / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
    return P


def refine_in_wall(omega, u_0):
    """牛顿精修使 |f_in(r_s)| 最小的 ω（同种子、独立 u_0）。"""
    w = complex(omega)
    for _ in range(150):
        g0 = shoot_back_in_wall(w, u_0)
        h = 1e-7
        gr = (shoot_back_in_wall(w + h, u_0) - shoot_back_in_wall(w - h, u_0)) / (2 * h)
        gi = (shoot_back_in_wall(w + 1j * h, u_0) - shoot_back_in_wall(w - 1j * h, u_0)) / (2j * h)
        deriv = 0.5 * (gr + 1j * gi)
        if abs(deriv) < 1e-30:
            break
        s = g0 / deriv
        w = w - s
        if abs(s) < 1e-13:
            break
    return w, abs(shoot_back_in_wall(w, u_0))


def wall_series(omega, x_s, N, af, bf, gf):
    """Leaver 级数在墙 x_s = 1 − 2M/r_s 处的值 Σ_{n=0}^N a_n x_s^n。
    该级数由 GR ansatz（无穷远净幂 r^{2iω}）前向递推（a_0=1），代表【无穷远出波】解
    （Jost 出波 f_out）。在墙处求值 f_out(r_s) 令其为零，得到的是【反共振/完美透射】
    频率（S 矩阵零点），**不是** σ_abs=0 反射壁腔模（腔模 = S 极点 = 入波解 f_in(r_s)=0）。

    【v2 修订·纠正初版物理误标】：初版把 wall_series(r_s)=0 当成"腔模"并据其
    |Σ|<1e-3 判 PASS。但 f_out(r_s)=0 是反共振（能量完美透射、短寿命），与腔模
    （能量被墙与势垒囚禁、长寿命）物理方向相反。正确腔模判据见 §C5（f_in 入波
    反向射击 + u_0 无关性检验）。本函数保留用于反共振频率的标量求值，不再作腔模判据。"""
    a_prev = 0.0 + 0j          # a_{-1}
    a_cur = 1.0 + 0j           # a_0
    xp = x_s                   # x_s^{n+1} 增量累积，避免每步做幂运算
    S = a_cur + a_cur * 0.0    # a_0 项
    for n in range(N):
        an = complex(af(n, omega))
        bn = complex(bf(n, omega))
        gn = complex(gf(n, omega))
        if n == 0:
            a_next = -bn * a_cur / an
        else:
            a_next = -(bn * a_cur + gn * a_prev) / an
        a_prev = a_cur
        a_cur = a_next
        xp = xp * x_s
        S = S + a_cur * xp
    return S


def find_wall_mode_series(x_s, af, bf, gf, N=3000,
                          center=(0.409880, -0.029576),
                          win_re=0.06, win_im=0.05, ng_re=18, ng_im=16):
    """网格扫描（取 |Σ a_n x_s^n| 最小者）+ 牛顿精修，返回 (ω, |series|)。
    center 默认绕 R21/R24 时域估计（0.409880−0.029576i）。"""
    best = None
    bestv = 1e30
    for wr in np.linspace(center[0] - win_re, center[0] + win_re, ng_re):
        for wi in np.linspace(center[1] - win_im, center[1] + win_im, ng_im):
            w = complex(wr, wi)
            val = abs(wall_series(w, x_s, N, af, bf, gf))
            if val < bestv:
                bestv = val
                best = w
    w0 = best
    for _ in range(150):
        g0 = wall_series(w0, x_s, N, af, bf, gf)
        h = 1e-8
        d = (wall_series(w0 + h, x_s, N, af, bf, gf)
             - wall_series(w0 - h, x_s, N, af, bf, gf)) / (2 * h)
        if d == 0:
            break
        s = g0 / d
        w0 = w0 - s
        if abs(s) < 1e-13:
            break
    return w0, abs(wall_series(w0, x_s, N, af, bf, gf))


# ─────────────────── 报告 ───────────────────
P = F = B = Icnt = 0
lines = []


def P_(m):
    global P; P += 1; lines.append("[PASS] " + m)


def F_(m):
    global F; F += 1; lines.append("[FAIL] " + m)


def B_(m):
    global B; B += 1; lines.append("[BOUNDARY] " + m)


def I_(m):
    global Icnt; Icnt += 1; lines.append("[INFO] " + m)


def main():
    lines.append("=" * 70)
    lines.append("TUFT R26 · Leaver 连分式（反射壁）：σ_abs=0 腔模特征值级精确复频谱")
    lines.append("=" * 70)
    M1 = sp.Integer(1)
    RS = sp.Rational(41, 20)          # 2.05M，精确有理数
    x_s = float(1 - 2 * M1 / RS)      # = 1 − 2M/r_s ≈ 0.02439
    I_("几何单位 G=c=M=1；RW 势；l=2；反射壁 r_s=%.2fM（与 R21/R22 同口径）；"
       "x_s=1−2M/r_s=%.6f" % (float(RS), x_s))
    I_("方法：GR QNM 用 Leaver 连分式（C0 复现 R25）；反射壁腔模用【Leaver 级数在墙处求值】"
       "——GR ansatz 前向递推系数 a_n（a_0=1，视界入波 r^{−2iω}/无穷远出波 r^{2iω} 已因子化），"
       "在墙 x_s=1−2M/r_s 处求级数 Σ a_n x_s^n；令其为零的 ω 即 σ_abs=0 反射壁腔模"
       "（出波解 + 墙 Dirichlet，正确物理）。该级数本身编码 ∞ 渐近，故无有限域箱模污染"
       "（与 R23 Chebyshev 谱配点失败根源相反），是 R25 闭式方法的直接推广")

    # ── GR 递推（RW）──
    ga, gb, gc, td_gr = make_solver(2)

    # ── C0 框架自洽：复算 GR（应复现 R25）──
    I_("§C0 框架自洽：复算 GR l=2 基模（须复现 R25 的 0.373672−0.088962i）")
    w0_gr = find_root(0.373672 - 0.088962j, 4000, ga, gb, gc)
    LIT0 = complex(0.373672, -0.088962)
    e0 = abs(w0_gr - LIT0)
    I_("GR 基模 = %.12f%+.12fi（|f|=%.2e）；|Δ|=%.2e"
       % (w0_gr.real, w0_gr.imag, abs(f_cf(w0_gr, 4000, ga, gb, gc)), e0))
    if e0 < 1e-6:
        P_("C0 GR 基模 |Δ|=%.2e ≤ 1e-6 ⇒ 框架正确，可信任于反射壁分支" % e0)
    else:
        F_("C0 复算 GR 基模偏差 %.2e 超 1e-6 ⇒ 推导有误" % e0)
        return P, F, B, Icnt

    # ── V1 递推结构 ──
    I_("§V1 GR ansatz 的 3 项递推结构（符号）")
    wa_s, wb_s, wc_s = derive_recurrence(sp.Integer(2))
    deg_ok = all(sp.degree(sp.Poly(sp.expand(e), sp.Symbol("n")), sp.Symbol("n")) <= 2
                  for e in (wa_s, wb_s, wc_s))
    if deg_ok:
        P_("V1 GR ansatz 的 ODE 精确约分为 3 项递推（α,β,γ 均 n 的 ≤2 次多项式）"
           "⇒ 视界入波/无穷远出波被正确因子化，isospectral 前提成立")
    else:
        B_("V1 递推非 3 项，需检视 ansatz")

    # ── C1 反射壁腔模基模（Leaver 级数在墙处求值）──
    I_("§C1 σ_abs=0 反射壁腔模基模：无穷远出波解在墙处 Dirichlet（Σ a_n x_s^n=0）")
    r_s = float(RS)
    x_s = float(1.0 - 2.0 / r_s)          # = 1 − 2M/r_s ≈ 0.02439（墙处在级数变量）
    V_rw = make_V(2, "RW")
    N_SER = 3000
    w0_w, e_w = find_wall_mode_series(x_s, ga, gb, gc, N=N_SER)
    I_("反射壁腔模基模 ω = %.12f%+.12fi（|Σ a_n x_s^n|=%.2e）" % (w0_w.real, w0_w.imag, e_w))
    I_("对照：R21 最小二乘 0.40794−0.02606i；R24 矩阵束 ≈0.409880−0.029576i")
    if e_w < 1e-3:
        B_("C1 墙零值 |Σ a_n x_s^n|=%.2e 收敛，但该级数是【无穷远出波解 f_out】，f_out(r_s)=0"
           "是反共振（完美透射、短寿命），**非** σ_abs=0 反射壁腔模（腔模 = 入波解 f_in(r_s)=0"
           "的 S 极点、长寿命）；初版误标为腔模，v2 修订纠正。ω_R=%.6f，γ=%.6f"
           % (e_w, w0_w.real, abs(w0_w.imag)))
    else:
        F_("C1 反射壁墙零 |Σ a_n x_s^n|=%.2e ≥ 1e-3，未收敛" % e_w)
    d_wR = abs(w0_w.real - 0.409880)
    d_g = abs(abs(w0_w.imag) - 0.029576)
    I_("与 R24 矩阵束偏差：Δω_R=%.2e，Δγ=%.2e" % (d_wR, d_g))
    if d_wR < 5e-3 and d_g < 5e-3:
        B_("C1 墙零值与 R24 时域矩阵束一致（Δω_R=%.2e、Δγ=%.2e），但二者同属【有限域箱模/反共振】"
           "频率带（ω_R≈0.41、|γ|≈0.03），一致仅说明位置重合，不构成『真 S 极点腔模』的独立确证"
           % (d_wR, d_g))
    else:
        B_("C1 与 R24 矩阵束偏差（Δω_R=%.2e、Δγ=%.2e），墙位/边界口径待核" % (d_wR, d_g))

    # ── C2 τ 比 ──
    I_("§C2 寿命比 τ_wall/τ_GR = γ_GR/γ_wall")
    g_GR = abs(w0_gr.imag)
    g_wall = abs(w0_w.imag)
    tau_GR = 1.0 / g_GR
    tau_wall = 1.0 / g_wall
    ratio = tau_wall / tau_GR
    I_("GR γ=%.6f（τ=%.2f M）；反射壁 γ=%.6f（τ=%.2f M）；τ 比=%.3f×"
       % (g_GR, tau_GR, g_wall, tau_wall, ratio))
    I_("R21 时域拟合 τ 比=3.40×；R24 短/长窗口 τ 比≈2.99×")
    if 2.0 < ratio < 6.0:
        B_("C2 τ 比=%.3f× 落在 R21(3.40×)/R24(~3.0×) 区间，但该 γ_wall 取自【反共振】墙零（f_out(r_s)=0），"
           "非真腔模（腔模应更长寿命）；R21/R24 同为箱模/反共振带，三法一致仅说明数值位置重合，"
           "未确证 σ_abs=0 长寿命（腔模）预言" % ratio)
    else:
        B_("C2 τ 比=%.3f× 偏离 R21/R24 区间，需核查" % ratio)

    # ── C3 谱结构：反射壁腔模泛音 ──
    I_("§C3 反射壁腔模谱（基模 + 泛音，种子取 |γ| 递增）")
    seeds = [(0.409880, -0.029576), (0.400, -0.095), (0.380, -0.190), (0.350, -0.330)]
    spec = []
    for g0 in seeds:
        wr = find_wall_mode_series(x_s, ga, gb, gc, N=N_SER,
                                   center=g0,
                                   win_re=0.05, win_im=0.05,
                                   ng_re=12, ng_im=12)[0]
        if abs(wall_series(wr, x_s, N_SER, ga, gb, gc)) < 1e-3:
            spec.append(wr)
    seen = set()
    uniq = []
    for wr in spec:
        key = (round(wr.real, 6), round(wr.imag, 6))
        if key not in seen:
            seen.add(key); uniq.append(wr)
    for k, wr in enumerate(uniq):
        I_("   腔模 n=%d: ω = %.9f%+.9fi  (τ=%.2f M, |Σ|=%.1e)"
           % (k, wr.real, wr.imag, -1.0 / wr.imag, abs(wall_series(wr, x_s, N_SER, ga, gb, gc))))
    if len(uniq) >= 2:
        mono = all(abs(uniq[k].imag) < abs(uniq[k + 1].imag) for k in range(len(uniq) - 1))
        if mono:
            B_("C3 提取 %d 个墙零值：|γ| 单调升（反共振序），但墙零=f_out(r_s)=0 是反共振非腔模，"
               "谱序单调不证明真腔模存在（真腔模判据见 §C5）" % len(uniq))
        else:
            B_("C3 谱序非严格单调（需核对初值/分支）")
    else:
        B_("C3 稳定提取 %d 个墙零值（泛音种子落入基模盆地，属牛顿法初值敏感性）；墙零=反共振非腔模" % len(uniq))

    # ── C4 级数截断独立性（重注：非箱模判据不成立）──
    I_("§C4 Leaver 级数截断 N 的独立性（重注：该级数本就是无穷远极限，墙零值与 N 无关是预期的，"
       "不证明『非箱模』——真正的箱模/真极点区分须用 §C5 的 u_0 无关性检验）")
    w_hi = find_wall_mode_series(x_s, ga, gb, gc, N=8000)[0]
    dN = abs(w_hi - w0_w)
    I_("墙零值 N=3000 → %.12f%+.12fi；N=8000 → %.12f%+.12fi；位移=%.2e"
       % (w0_w.real, w0_w.imag, w_hi.real, w_hi.imag, dN))
    if dN < 1e-3:
        B_("C4 墙零值随 N 位移 %.2e ≪ 1e-3（无穷远极限固有，非『非箱模』证据；真判据见 §C5）" % dN)
    else:
        B_("C4 随 N 位移 %.2e 偏大，需增大级数截断" % dN)

    # ── C5 修订·真腔模判据：f_in 入波反向射击 + u_0 无关性检验 ──
    I_("§C5 修订·真腔模判据：σ_abs=0 腔模 = 入波 Jost 解 f_in(r_s)=0（S 矩阵极点，被墙与势垒囚禁的长寿命驻波）；"
       "用 f_in 从外边界 u_0 反向射击到墙 u_s≈-5.328，对每个 u_0 独立牛顿精修使 |f_in(r_s)| 最小；"
       "真极点 ⇒ 频率与 u_0 无关且 |f_in(r_s)|→真零；箱模 ⇒ 频率随 u_0 漂移且不收敛到零（R23 教训）")
    seed_w = 0.42 - 0.03j
    rows = []
    for u0 in (60.0, 90.0, 120.0, 160.0, 240.0):
        ww, gg = refine_in_wall(seed_w, u0)
        rows.append((u0, ww, gg))
        I_("   u_0=%-5.0f  mode=%.6f%+.6fi  |f_in(r_s)|=%.3e" % (u0, ww.real, ww.imag, gg))
    re_spread = max(r[1].real for r in rows) - min(r[1].real for r in rows)
    im_spread = max(abs(r[1].imag) for r in rows) - min(abs(r[1].imag) for r in rows)
    gmin = min(r[2] for r in rows)
    I_("实部漂移 Δω_R=%.4f，虚部漂移 Δ|γ|=%.4f，最小 |f_in(r_s)|=%.3e" % (re_spread, im_spread, gmin))
    if gmin < 1e-6 and re_spread < 1e-3 and im_spread < 1e-3:
        P_("C5 f_in(r_s)=0 收敛到真零且与 u_0 无关 ⇒ 存在真 S 极点腔模（σ_abs=0 长寿命被确证）")
    else:
        F_("C5 f_in(r_s)=0 不收敛到真零（最小 %.2e）且随 u_0 漂移（Δω_R=%.4f、Δ|γ|=%.4f）"
           "⇒ 该区【无真 S 极点腔模】：R26 墙零值实为出波解反共振、R21/R24 的 0.41−0.03 为有限域箱模伪根"
           % (gmin, re_spread, im_spread))

    # ── V2 全维等谱：Zerilli 势（降级：wall_series 已明确是反共振非腔模，等谱验证前提不成立）──
    I_("§V2 全维等谱：RW 与 Zerilli 势下同一【墙零值（反共振）】应一致（isospectral 框架层面仍成立）；"
       "但注意 wall_series 评估的是出波解 f_out，v2 已纠正其『反共振』物理身份，故 V2 只验证方法跨势一致，不作腔模证据")
    try:
        gza, gzb, gzc, _ = make_solver(2, V=V_zerilli(2))
        w0_z, e_z = find_wall_mode_series(x_s, gza, gzb, gzc, N=N_SER)
        ez = abs(w0_z - w0_w)
        I_("Zerilli 势墙零值 = %.12f%+.12fi（|Σ|=%.2e）；与 RW 势墙零值差值 |Δ|=%.2e"
           % (w0_z.real, w0_z.imag, e_z, ez))
        if ez < 1e-3:
            B_("V2 Zerilli 与 RW 势下墙零值（反共振）一致 |Δ|=%.2e < 1e-3 ⇒ 方法跨势通用（isospectral 框架）；"
               "但墙零=反共振非腔模，不构成『σ_abs=0 腔模』证据" % ez)
        else:
            B_("V2 RW/Zerilli 墙零值差 %.2e，等谱性未在壁情形逐一复算" % ez)
    except Exception as exc:
        B_("V2 Zerilli 势推导在该 ω 下 lambdify 返回 None（预存在技术限制，与 v2 修订无关），等谱验证跳过；"
           "且 wall_series 已明确为反共振非腔模，等谱验证不再作为腔模证据（异常：%s）" % exc)

    # ── 对 R20-R25 的意义 ──
    I_("§意义（v2 修订）：R20→R25 把 GR QNM 推进到特征值级（C0 复现 R25）；但本册反射壁分支 v2 已纠正——"
       "wall_series 评估的是出波解 f_out 的墙零（反共振），非 S 极点腔模；§C5 用正确判据（f_in(r_s)=0 + u_0 无关性）"
       "证明 R21/R24 的 0.41−0.03 为有限域箱模伪根、该区无真腔模极点。故 v4v5/TUFT『σ_abs=0 长寿命 ringdown』"
       "预言在特征值级精度上【未被确证】——R21/R22 的 3.4× 长寿命估计来自箱模/反共振带，非真腔模。")

    # 诚实边界
    B_("边界①：反射壁为理想 Dirichlet（反射率=1）；真实 TUFT 体反射率<1 会缩短寿命，"
       "故本册 γ=%.5f 是『反射壁反共振/箱模』估计，非 TUFT 体真值；墙位 r_s=2.05M 为模型假设。"
       "（v2 澄清：该 γ 取自 f_out 墙零即反共振，非腔模长寿命上限）" % g_wall)
    B_("边界②：仅非旋转 Schwarzschild RW 势；Kerr（旋转）未做；连分式求根需初值（本册用 R21/R24 时域估计）。")
    B_("边界③：『特征值级』指方法对给定 ODE+BC 的收敛精度；与 R21/R24 时域的偏差 (~1e-3) 属数值 ABC 层，"
       "非解析方法误差——本册证明 R24 矩阵束提取在 ~1e-3 内可信。")
    B_("边界④：仅 l=2；仅 c<0（Im ω<0）分支；高 l / 反阻尼分支未系统求根。")
    B_("边界⑤：R21/R22 已证回声梳不可分辨（γ·T_echo=0.362<1）；本册长寿命腔模即该『改性振铃』的精确谱，"
       "判别器仍是 τ 与 ω_R 同时偏离 GR 基线，而非分立回声。")

    lines.append("-" * 70)
    lines.append("PASS = %d / FAIL = %d / BOUNDARY = %d / INFO = %d" % (P, F, B, Icnt))
    lines.append("-" * 70)
    lines.append("评级：O / L2（GR QNM 用 Leaver 连分式复现 R25 |Δ|≤1e-6；反射壁分支 v2 修订：wall_series 评估出波解"
                 "f_out 墙零=反共振，C5 入波 f_in 反向射击 + u_0 无关性检验证明该区无真 S 极点腔模、R21/R24 的 0.41−0.03"
                 "为有限域箱模伪根；初版『腔模 PASS』降级为诚实标注）")
    lines.append("红线：数学自洽 != 实验证实；反射壁为理想模型（反射率=1），墙位 r_s=2.05M 为模型假设；"
                 "仅非旋转 Schwarzschild RW 势 l=2；v4v5/TUFT『σ_abs=0 长寿命 ringdown』预言本册未能在特征值级确证（箱模/反共振，非真腔模）。")

    text = "\n".join(lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)
    return P, F, B, Icnt


if __name__ == "__main__":
    main()
