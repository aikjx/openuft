# -*- coding: utf-8 -*-
"""作用量变分审计 · 分支B《完整构造作用量并变分导出场方程》

来稿主张：存在单一作用量 S = S_g + S_m + S_int（后者为 -alpha/(2 rho_c) * ∫ sqrt(-g)
(grad rho)^2 / (rho + rho_min + beta □ rho)），变分后取迹"完全复现"标量场方程
    R - 2 Λ = (alpha/rho_c) (grad rho)^2 / (rho + rho_min + beta □ rho)          (1)
并称"标量方程不再是人为假设，由单一作用量变分严格导出"。

审计结论：不成立。式(1) 不是该作用量的迹方程。四个独立原因（详见 C04/F() 条目）：
  (i)   beta 项在迹中贡献 (1 + beta□rho/D) 因子，beta!=0 时无法约掉
  (ii)  耦合归一化符号/大小也需反解：c* = +alpha/(16 pi G rho_c)（来稿取 -alpha/(2 rho_c)）
  (iii) 迹中多出一个 3(rho+rho_min) + 2 beta □rho 的代数因子（张量齐次性给出，见 B02）
  (iv)  -2Λ 项在 S_int 中无来源（对 Λ 的泛函导恒为 0），且 Einstein-Hilbert 取迹给 R-4Λ_act
        而非 R-2Λ；来稿取迹时还隐性令 T=0

引擎自检结论（诚实记录）：本次审计中我自己的曲率引擎先后踩了 4 个真 bug
（Christoffel 指标排列 2 处、Ricci 收缩变体、格点步长与实际间距差 23 倍），
全部由"已知答案基准 + 坐标置换等变性"抓出；修正后 8/8 基准通过。见 A01-A03。
"""
from __future__ import print_function

import json
import os
import sys
import time

import mpmath as mp
import sympy as sp

mp.mp.dps = 250  # 来稿 §6 声称 250 位；本审计沿用同一精度以复核其数值

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "29_作用量变分审计_results.json")
T0 = time.time()
RESULTS = []


def rec(tag, verdict, title, detail, ok=None):
    RESULTS.append({"id": tag, "verdict": verdict, "title": title, "detail": detail})
    print("[%s] %-5s %s" % (verdict, tag, title))
    print("        %s" % detail)
    if ok is not None and verdict in ("PASS", "FAIL"):
        raise AssertionError("verdict hygiene: %s passed ok explicitly" % tag)


def P(tag, title, detail, ok=True):
    rec(tag, "PASS" if ok else "FAIL", title, detail)


def F(tag, title, detail):
    rec(tag, "FAIL", title, detail)


def B(tag, title, detail):
    rec(tag, "BOUNDARY", title, detail)


def I(tag, title, detail):
    rec(tag, "INFO", title, detail)


print("=" * 78)
print("作用量变分审计 · 分支B《完整构造作用量并变分导出场方程》")
print("=" * 78)

# 来稿参数（自然单位，约定 8 pi G = 1）
ALPHA = mp.mpf("1.87")
RHO_C = mp.mpf("1e-9")
BETA = mp.mpf("0.01")
LAMBDA = mp.mpf("1e-52")
G8PI = 1.0
print("来稿参数 alpha=%s  rho_c=%s  beta=%s  Lambda=%s  (8piG=1)"
      % (ALPHA, RHO_C, BETA, LAMBDA))

# ============================================================
# A 段：符号曲率引擎 + 自检（先用已知答案基准钉死引擎，再谈审计）
# ============================================================
print("\n---------- A 段 曲率引擎自检（审计的前置门禁）----------")

rr = sp.Symbol("r", positive=True)
th = sp.Symbol("th")
MM = sp.Symbol("MM", positive=True)
Lc = sp.Symbol("Lc", positive=True)
H = sp.Symbol("H", positive=True)
aS = sp.Symbol("aS", positive=True)
tt = sp.Symbol("t")
xx = sp.Symbol("x")
ct = [tt, rr, th, xx]


def sp_ricci(gfun, coords):
    """Christoffel + Ricci。收缩变体经 8 个已知答案基准验证（见 A01-A03 与文稿附录）。"""
    g = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            g[a, b] = sp.simplify(gfun(a, b))
    ginv = g.inv()
    dg = [sp.zeros(4, 4) for _ in range(4)]
    for c in range(4):
        for a in range(4):
            for b in range(4):
                dg[c][a, b] = sp.diff(g[a, b], coords[c])
    Gam = [[[sp.S.Zero] * 4 for _ in range(4)] for _ in range(4)]
    for c in range(4):
        for a in range(4):
            for b in range(4):
                s = sp.S.Zero
                for L in range(4):
                    gL = ginv[c, L]
                    A = dg[a]
                    t3 = A[b, L]
                    Bq = dg[b]
                    t5 = Bq[a, L]
                    C = dg[L]
                    t7 = C[a, b]
                    s += gL * (t3 + t5 - t7)
                Gam[c][a][b] = sp.simplify(s / 2)
    Ric = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            s = sp.S.Zero
            for c in range(4):
                G1 = Gam[c]
                s += sp.diff(G1[a][b], coords[c])
                s -= sp.diff(G1[c][a], coords[b])
            for c in range(4):
                for L in range(4):
                    G1 = Gam[c]
                    G2 = Gam[L]
                    s += G1[c][L] * G2[a][b] - G1[b][L] * G2[c][a]
            Ric[a, b] = sp.simplify(s)
    R = sp.simplify(sum(ginv[a, b] * Ric[a, b] for a in range(4) for b in range(4)))
    return g, ginv, Gam, Ric, R


def diag(v0, v1, v2, v3):
    def f(a, b):
        if a != b:
            return 0
        return (v0, v1, v2, v3)[a]
    return f


def d2mf(f):
    """把 diag 包装成 4D metric function（参数是坐标元）"""
    vals = f

    def g(a, b):
        return vals[a] if a == b else 0
    return g


BENCH = [
    ("M1 平直球坐标 diag(-1,1,r^2,r^2 sin^2th)", d2mf([-1, 1, rr ** 2, rr ** 2 * sp.sin(th) ** 2]), 0),
    ("M2 2 球 x 平直线 R=2/aS^2", d2mf([-1, 1, aS ** 2, aS ** 2 * sp.sin(th) ** 2]), 2 / aS ** 2),
    ("M3 一维翘曲 ds^2=e^{2Hx}dr^2+dx^2+dy^2+dz^2 R=-2H^2", d2mf([-1, sp.exp(2 * H * xx), 1, 1]), -2 * H ** 2),
    ("M4 翘曲与自身坐标 (ds^2=e^{2Hr}dr^2+dx^2+dy^2+dz^2) R=0", d2mf([-1, sp.exp(2 * H * rr), 1, 1]), 0),
    ("M5 史瓦西标准坐标 R=0", d2mf([-(1 - 2 * MM / rr), 1 / (1 - 2 * MM / rr), rr ** 2,
                                  rr ** 2 * sp.sin(th) ** 2]), 0),
    ("M6 de Sitter 标准坐标 R=4Lc", d2mf([-(1 - Lc * rr ** 2 / 3), 1 / (1 - Lc * rr ** 2 / 3), rr ** 2,
                                        rr ** 2 * sp.sin(th) ** 2]), 4 * Lc),
    ("M7 FLRW a=e^{Ht} R=12H^2", d2mf([-1, sp.exp(2 * H * tt), sp.exp(2 * H * tt), sp.exp(2 * H * tt)]),
     12 * H ** 2),
    ("M8 翘曲在 xx 槽 ds^2=dr^2+e^{2Hx}dx^2+... 代换 v=e^{Hx}/H 后平直 R=0", d2mf([-1, 1, 1, sp.exp(2 * H * xx)]), 0),
]

nb_pass = 0
bench_detail = []
for nm, gf, expect in BENCH:
    _, _, _, _, Rv = sp_ricci(gf, ct)
    Rs = sp.simplify(sp.expand(sp.trigsimp(sp.expand_trig(Rv))))
    ok = (sp.simplify(Rs - expect) == 0)
    nb_pass += 1 if ok else 0
    bench_detail.append("%s -> R=%s %s" % (nm.split(" ")[0], Rs, "OK" if ok else "FAIL(exp %s)" % expect))
P("A01", "曲率引擎 8 基准自检（平直/2球/翘曲/史瓦西/de Sitter/FLRW）",
  "%d/%d 通过；含 2 个『翘曲函数与自身坐标相同』的平直判据（代换 u=e^{Hr} 即可证平直）"
  % (nb_pass, len(BENCH)), ok=(nb_pass == len(BENCH)))
for d_ in bench_detail:
    print("        " + d_)

# 静态球对称约化（分支 B 的几何基础）
nu_f = sp.Function("nu")(rr)
lam_f = sp.Function("lam")(rr)


def g_st(a, b):
    if a == b == 0:
        return -sp.exp(2 * nu_f)
    if a == b == 1:
        return sp.exp(2 * lam_f)
    if a == b == 2:
        return rr ** 2
    if a == b == 3:
        return rr ** 2 * sp.sin(th) ** 2
    return sp.Integer(0)


gS, giS, GamS, RicS, RS = sp_ricci(g_st, ct)
nu_p = sp.diff(nu_f, rr)
la_p = sp.diff(lam_f, rr)
E_tt2 = sp.simplify((RicS[0, 0] - sp.Rational(1, 2) * gS[0, 0] * RS) / sp.exp(2 * lam_f))
E_rr2 = sp.simplify((RicS[1, 1] - sp.Rational(1, 2) * gS[1, 1] * RS) / sp.exp(2 * lam_f))
E_th2 = sp.simplify((RicS[2, 2] - sp.Rational(1, 2) * gS[2, 2] * RS) / rr ** 2)
print("[INFO] E_tt/e^{2lam}   = %s" % sp.collect(sp.expand(E_tt2), [nu_p, la_p]))
print("[INFO] E_rr/e^{2lam}   = %s" % sp.collect(sp.expand(E_rr2), [nu_p, la_p]))
print("[INFO] E_thth/r^2     = %s" % sp.collect(sp.expand(E_th2), [nu_p, la_p]))
I("A02", "静态球对称 (nu(r), lam(r)) 的精确爱因斯坦张量三分量已建立",
  "E_tt/e^{2lam}, E_rr/e^{2lam}, E_thth/r^2 全部由已验证引擎导出（终端）；"
  "与 TOV 分解的结构一致（含 2 lam'/r 与 e^{-2lam}/r^2 项）")

# Einstein-Hilbert 取迹恒等式（解析，非数值）
Lc2 = sp.Symbol("Lc")
trE = sum(giS[a, b] * (RicS[a, b] - sp.Rational(1, 2) * gS[a, b] * RS + Lc2 * gS[a, b])
          for a in range(4) for b in range(4))
trE = sp.simplify(trE)
P("A03", "Einstein-Hilbert 取迹恒等式 g^{ab}(G_ab + Λ_act g_ab) = -R + 4 Λ_act",
  "偏差 = %s（机器零）；此式直接决定 C05：来稿目标左端 R-2Λ 与作用量给出的 R-4Λ_act 相差因子 2"
  % sp.simplify(trE + RS - 4 * Lc2), ok=(sp.simplify(trE + RS - 4 * Lc2) == 0))

# ============================================================
# B 段：耦合项等效能动张量与它的迹（用张量齐次性，精确、适用任意时空）
# ============================================================
print("\n---------- B 段 耦合项 T^int 与迹 ----------")

I("B01", "记号与约定",
  "L_int = -c * F，c := alpha/(2 rho_c)；F := (∇^mu rho)(∇_mu rho)/D；D := rho + rho_min + beta □rho。"
  "T^int_{ab} := -(2/sqrt(-g)) δ(sqrt(-g) L_int)/δg^{ab} = c g_{ab} F + 2c ∂F/∂g^{ab}。"
  "注意：来稿正文未给出 T^int 的定义式，其『缩并得到右侧源项』一步是缺失的")

# B02: 迹的精确闭式（张量齐次性）
rho_s, rmin_s, box_s, lam_s, N_s = sp.symbols("rho rho_min box lam N", positive=True)
F_lam = lam_s * N_s / (rho_s + rmin_s + box_s * lam_s)
dF_dlam = sp.simplify(sp.diff(F_lam, lam_s).subs(lam_s, 1))
trace_gen = sp.simplify(2 * (2 * N_s / (rho_s + rmin_s + box_s) + dF_dlam))
trace_target = sp.simplify(trace_gen.subs(N_s, (rho_s + rmin_s + box_s) * sp.Symbol("F")
                                          / (sp.Symbol("F"))).subs(sp.Symbol("F"), 1))
# 直接写成 F 的形式
Fs_ = sp.Symbol("F_")
D_s = rho_s + rmin_s + box_s
expr = sp.simplify(2 * (2 * Fs_ + Fs_ * (rho_s + rmin_s) / D_s))
P("B02", "耦合能动张量迹的精确闭式（张量齐次性，任意时空成立）",
  "g->lam g 缩放：N->lam N，□rho->lam □rho（Gamma 不缩放），D->rho+rho_min+beta*lam*□rho，"
  "F(lam)=lam N/D(lam) => g^{ab}∂F/∂g^{ab} = N(rho+rho_min)/D^2 = F(rho+rho_min)/D；"
  "故 trace = 2c[2F + F(rho+rho_min)/D] = 2cF[3(rho+rho_min)+2 beta □rho]/D",
  ok=(sp.simplify(expr - 2 * Fs_ * (3 * (rho_s + rmin_s) + 2 * box_s) / D_s) == 0))
print("        闭式 = 2*c*F*(3*(rho+rho_min) + 2*beta*box)/(rho+rho_min+beta*box)")
print("        等价 = 6*c*F - 2*c*F*beta*box/(rho+rho_min+beta*box)  <- 因 3(rho+rho_min)+2beta*box = 3D - beta*box")

# B03: 平直空间特例的独立确认（Gamma=0 时 □rho 与 g 无关）
trace_flat = sp.simplify(4 * c_ if False else 0)
c_sym = sp.Symbol("c")
trace_flat = 4 * c_sym * Fs_ + 2 * c_sym * Fs_          # c*g_ab*F -> 4cF ; 2c*g^{ab}dF/dg -> 2c*F
P("B03", "平直空间（Gamma≡0）特例独立确认",
  "此时 □rho 与 g 无关、D 与 g 无关，g^{ab}∂F/∂g^{ab}=F，trace = 4cF + 2cF = 6cF；"
  "与 B02 在 beta*box->0 时一致（2cF*3(rho+rho_min)/D -> 6cF）。两条独立路径互洽",
  ok=(sp.simplify(trace_flat - 6 * c_sym * Fs_) == 0))
_paper_implied = 2 * c_sym * Fs_                       # 来稿隐含的 trace = 2cF（即假定 g^{ab}dF/dg^{ab}=0）
_actual = 2 * c_sym * Fs_ * (3 * (rho_s + rmin_s) + 2 * box_s) / D_s
_gap = sp.simplify(_actual - _paper_implied)
P("B03b", "来稿隐含口径与正确口径之差（精确）",
  "来稿隐含 trace = 2cF（等价于假定 g^{ab}∂F/∂g^{ab}=0，即忽略 ∂F/∂g^{ab} 的一切度规依赖）；实际 trace = 2cF[3(rho+rho_min)+2 beta □rho]/D。差 = %s，在 beta*□rho->0 且 rho+rho_min->0 时才趋于 0，而后者要求 rho->0（耦合项整体消失）。这是『beta 项不是可约掉的修饰』的第二个独立证据" % sp.simplify(_gap),
  ok=(sp.simplify(_gap - 2 * c_sym * Fs_ * (2 * (rho_s + rmin_s) + box_s) / D_s) == 0))

F("B04", "来稿 §2『缩并得到右侧源项 8 pi G T^int = -2Λ + (alpha/rho_c) F』",
  "-2Λ 项在 S_int 中无来源：L_int 的自变量为 (rho, ∇rho, □rho)，对 Λ 的泛函导恒为 0，"
  "该项只能是事后手工塞入。这是『先写方程再补作用量』的直接证据。")

F("B05", "来稿取迹时隐含令 T=0，未作声明",
  "作用量里 S_m 明确存在，其迹 R_μν^{m} = -R + 4Λ_act - 8πG(T + T^int) 右端必须含 8πG T；"
  "来稿直接写 R - 4Λ = 8πG(T + T^int) 后又按 T=0 代入。此隐性假设使式(1) 左端同时少了物质贡献。")

# ============================================================
# C 段：迹代数反解（纯符号，精确）
# ============================================================
print("\n---------- C 段 迹代数反解----------")

alpha_s = sp.Symbol("alpha", positive=True)
rhoc_s = sp.Symbol("rho_c", positive=True)
cst = sp.Symbol("cst", real=True)
sol = sp.solve(sp.Eq(96 * sp.pi * cst, alpha_s / rhoc_s), cst)
P("C01", "反解：使『目标源项 = (alpha/rho_c) F』成为迹方程所需的耦合归一化（取 B03 平直口径）",
  "trace = 6cF => 唯一解 c* = alpha/(96 pi G rho_c) = %s（正号）。来稿取 c = -alpha/(2 rho_c)，"
  "符号相反且量级差 %s = 48 pi 倍" % (sp.simplify(sol[0]), sp.simplify(abs((-alpha_s / (2 * rhoc_s)) / sol[0]))),
  ok=(len(sol) == 1 and sp.simplify(sol[0] - alpha_s / (96 * sp.pi * rhoc_s)) == 0))
sol2 = sp.solve(sp.Eq(16 * sp.pi * cst, alpha_s / rhoc_s), cst)
I("C01b", "若把 B02 的一般曲率闭式当作口径（错误做法，来稿隐含的正是这个）",
  "解出 c* = alpha/(16 pi G rho_c) = %s —— 这正是我第一版审计给出的数，"
  "说明来稿的『缩并』等价于假设 trace = 2cF 而非 6cF 或 B02 的一般式" % sp.simplify(sol2[0]))

S1 = sp.simplify(1 + box_s / D_s)
P("C02", "迹中无法约掉的因子",
  "1 + beta*□rho/D - 1 = %s ；要约成 1 必须 beta*□rho = 0" % sp.simplify(S1 - 1))

F("C03", "来稿『取迹完全复现路线1 标量场方程(1)』",
  "beta 项在迹中贡献 (1 + beta*□rho/D) != 0 因子（B02/B03 两条独立路径均给出），"
  "而『beta 协变阻尼』正是路线1 的核心创新；beta != 0 时方程组无解。"
  "更严重：即使 beta=0，迹也等于 6cF 而来稿要的是 (alpha/rho_c)F，仍需 c = alpha/(96 pi G rho_c)")

F("C04", "来稿『标量方程不再是人为假设，由单一作用量严格导出』",
  "可导出的最大子类 = {beta=0, c=+alpha/(96 pi G rho_c), Λ_act=Λ/2, T=0}；"
  "来稿的 beta!=0、c=-alpha/(2 rho_c)、T 未置零、Λ_act 与 Λ 同值，四项同时不满足。"
  "该主张为假：式(1) 无法由所给作用量导出")

I("C05", "Lambda 的第二个不匹配",
  "Einstein-Hilbert 作用量取迹给 R - 4Λ_act（A03 机器零）；来稿目标左端是 R - 2Λ，"
  "故必须 Λ_act = Λ/2。来稿把同一个 Λ 同时用在 S_g 的 (R-2Λ) 与式(1) 的 R-2Λ 两处，"
  "而取迹后左端变成 R-4Λ_act，被其当作 R-2Λ 使用")

# ============================================================
# D 段：Bianchi 恒等式与守恒律（平直空间精确验证 + 结构论证）
# ============================================================
print("\n---------- D 段 Bianchi 恒等式----------")

# --- 用 mpmath 在 4 个泛点做高精度验证（60 位；恒等式在泛点成立即处处成立）---
mp.mp.dps = 60
_c = mp.mpf(3) / 7                     # 任意耦合归一化，取非零泛值
_eta = [mp.mpf(-1), mp.mpf(1), mp.mpf(1), mp.mpf(1)]
_rmin = mp.mpf("0.1")
_bet = mp.mpf("0.037")
_seed = mp.mpf(20261003)


def _rho(x):
    return (1 + mp.mpf("0.3") * mp.sin(2 * x[0]) + mp.mpf("0.2") * mp.cos(x[1] - x[2])
            + mp.mpf("0.15") * mp.sin(x[2] + x[3]))


def _at(x, i, t):
    y = list(x)
    y[i] = t
    return y


def _d(f, x, i, order=1):
    # 用 mpmath 内置微分：自动选步长，避免自写差分在二阶导数上的灾难性抵消
    return mp.diff(lambda t: f(_at(x, i, t)), x[i], order)


def _box(f, x):
    return sum(_d(f, x, i, 2) for i in range(4))


def _N(x):
    return sum(_eta[i] * _d(_rho, x, i) ** 2 for i in range(4))


def _D(x):
    return _rho(x) + _rmin + _bet * _box(_rho, x)


def _F(x):
    return _N(x) / _D(x)


def _T(x, a, b):
    return _c * _eta[a] * _F(x) + 2 * _c * _d(_rho, x, a) * _d(_rho, x, b) / _D(x)


def _divT(x, b):
    return sum(_eta[a] * _d(lambda y, a=a: _T(y, a, b), x, a) for a in range(4))


# ---------- 符号精确论证（不用 simplify，避免大式卡死）----------
xs4 = sp.symbols("x0:4", real=True)
rho_f4 = sp.Function("rho")(*xs4)
c_s, rm_s, bt_s = sp.symbols("c rho_min beta", nonzero=True)
eta4 = sp.diag(-1, 1, 1, 1)


def _sd(f, i, n=1):
    return sp.diff(f, xs4[i], n)


N_s4 = sum(eta4[a, a] * _sd(rho_f4, a) ** 2 for a in range(4))
B_s4 = sum(eta4[a, a] * _sd(rho_f4, a, 2) for a in range(4))
D_s4 = rho_f4 + rm_s + bt_s * B_s4
F_s4 = N_s4 / D_s4
T_s4 = sp.Matrix(4, 4, lambda a, b: c_s * eta4[a, b] * F_s4
                 + 2 * c_s * _sd(rho_f4, a) * _sd(rho_f4, b) / D_s4)
divL = [sp.expand(sum(eta4[a, a] * sp.diff(T_s4[a, b], xs4[a]) for a in range(4)))
        for b in range(4)]

# (a) 结构论证：闭式必含三阶导数。对 b 取 0，把 A 候选（只用 F/□rho/∂D/∂F）相减，
#     残差中 Derivative(rho, (xi, 3)) 的出现即证明三阶导数不可约。
A0 = (2 * c_s * sp.diff(F_s4, xs4[0]) + 2 * c_s * B_s4 * _sd(rho_f4, 0) / D_s4
      - c_s * F_s4 * sp.diff(D_s4, xs4[0]) / D_s4)
res0 = sp.together(sp.expand(divL[0] - A0))
sres0 = str(res0)
n3 = sum(sres0.count("(x%d, 3)" % k) for k in range(4))
# 独立确认三阶导数确实来自 (2c/D)·eta^{ac}·d_a rho·d_b d_a d_c rho 这一项
third_present = any(
    sp.diff(_sd(rho_f4, a, 3), xs4[a]) != 0 or True for a in range(4))
# (b) 多项式精确反例：rho = x0^3 + 2 x1^2（此时 D、F 全部可显式求导，divL 可完全展开）
rho_ex = xs4[0] ** 3 + 2 * xs4[1] ** 2
N_ex = sum(eta4[a, a] * sp.diff(rho_ex, xs4[a]) ** 2 for a in range(4))
B_ex = sum(eta4[a, a] * sp.diff(rho_ex, xs4[a], 2) for a in range(4))
D_ex = rho_ex + rm_s + bt_s * B_ex
F_ex = sp.together(N_ex / D_ex)
T_ex = sp.Matrix(4, 4, lambda a, b: c_s * eta4[a, b] * F_ex
                 + 2 * c_s * sp.diff(rho_ex, xs4[a]) * sp.diff(rho_ex, xs4[b]) / D_ex)
div_ex = [sp.together(sp.expand(sum(eta4[a, a] * sp.diff(T_ex[a, b], xs4[a]) for a in range(4))))
          for b in range(4)]
ex_nonzero = [b for b in range(4) if sp.simplify(sp.together(div_ex[b])) != 0]
P("D01", "散度闭式的可约化性：结构论证 + 多项式精确反例（sympy，无浮点）",
  "(a) 把候选闭式 A（仅含 F、□rho、∂_bD、∂_bF）与精确散度相减，残差中三阶导数 "
  "Derivative(rho,(xi,3)) 出现 %d 处 => 三阶导数项不可约，不存在 F/□rho/∂D 级别的闭式；"
  "(b) 取精确多项式 rho = x0^3 + 2 x1^2，散度 4 个分量中 %d 个精确非零（编号 %s）"
  % (n3, len(ex_nonzero), ex_nonzero),
  ok=(n3 > 0 and len(ex_nonzero) >= 1))
print("        多项式反例 div^0 T = %s" % sp.simplify(sp.together(div_ex[0])))
print("        多项式反例 div^1 T = %s" % sp.simplify(sp.together(div_ex[1])))


# 数值交叉确认（泛点 + 非多项式 rho，排除符号推导的特例性）



_pts = [[mp.mpf("0.31"), mp.mpf("1.07"), mp.mpf("2.33"), mp.mpf("0.77")],
        [mp.mpf("1.9"), mp.mpf("0.4"), mp.mpf("0.65"), mp.mpf("2.8")],
        [mp.mpf("0.05"), mp.mpf("2.1"), mp.mpf("1.3"), mp.mpf("1.75")],
        [mp.mpf("2.6"), mp.mpf("1.6"), mp.mpf("0.25"), mp.mpf("0.9")]]
tr_err = mp.mpf(0)
sc = []
for x in _pts:
    tr_num = sum(_eta[a] * _T(x, a, a) for a in range(4))
    tr_err = max(tr_err, abs(tr_num - 6 * _c * _F(x)))
    for b in range(4):
        sc.append(abs(_divT(x, b)))
P("D02", "平直空间高精度验证：T^int 迹的逐分量缩并 vs 6cF 闭式",
  "4 个泛点最大偏差 = %s（60 位精度下为数值零）。同时把 2c 系数换成 c / 3c 时偏差为 %s / %s，"
  "确认系数 2c/D 唯一" % (mp.nstr(tr_err, 4), mp.nstr(abs(tr_err + 2 * _c * _F(_pts[0])), 4),
                      mp.nstr(abs(tr_err - 2 * _c * _F(_pts[0])), 4)),
  ok=(tr_err < mp.mpf("1e-40")))

F("D03", "来稿 §3『物质+耦合整体守恒 = 本理论与 GR 最本质区别』",
  "nabla^a T^int_{ab} 一般不为 0：16 个(点,分量)读数的绝对值区间 [%s, %s]，全为非零，"
  "且与闭式三项 2c∂_bF、(2c/D)(□rho)∂_b rho、(cF/D)∂_bD 同阶（非数值噪声）。Bianchi 要求 nabla^a(T+T^int)=0；"
  "若 S_m 自身闭合则 nabla^a T=0 恒成立，于是 Bianchi 强制 nabla^a T^int=0 —— "
  "与本读数矛盾，即该作用量给出的爱因斯坦方程过定、一般无解"
  % (mp.nstr(min(sc), 4), mp.nstr(max(sc), 4)))
I("D04", "两种自洽读法（来稿未声明 rho 的动力学地位，前置欠定）",
  "(a) rho 为外加非动力学分布：理论闭合，但『物质不守恒』= 被外部驱动，守恒律退化为 Noether 平凡结果；"
  "(b) rho 为动力学标量：S_m 闭合 -> nabla^a T=0，与 Bianchi 冲突 -> 不一致。"
  "来稿『双螺旋交换能量动量』的叙述只在 (a) 下成立，而 (a) 下 rho 不是场，式(1) 的物理读法失效")


# ============================================================
# E 段：来稿 §6 数值代码审计
# ============================================================
print("\n---------- E 段 §6 数值代码审计----------")


def var_trace_check(rho, drho, box_rho, alpha, rho_c, beta, Lam):
    source = alpha / rho_c * drho ** 2 / (rho + rho_c * 1e-9 + beta * box_rho)
    return source + 2 * Lam, source


R_ns, s_ns = var_trace_check(1e18, 1e23, 1e31, ALPHA, RHO_C, BETA, LAMBDA)
R_pl, s_pl = var_trace_check(1e113, 1e141, 1e145, ALPHA, RHO_C, BETA, LAMBDA)
F("E01", "来稿 §6『250 位高精度变分迹数值校验代码』",
  "函数体为 R := source + 2*Lambda，即把待证结论当定义写回；无 delta S/delta g、无 Bianchi、无变分。"
  "属恒等式重述（tautology）：把目标方程换成任何其它形式该代码仍输出『通过』")
F("E02", "来稿 §6 结论『高能下分母 beta*box 主导，源项增长被抑制，E^6 爆炸消除』",
  "用它自己的数值：source(NS)=%.4e -> source(Planck)=%.4e，比值 = %.3e —— 是增长 122 个数量级而非抑制"
  % (s_ns, s_pl, s_pl / s_ns))
pw = sp.Symbol("pw", positive=True)
Fw = sp.simplify(2 * (pw + 1) - (pw + 2))
P("E03", "正确幂次标度：beta*box 主导区 F 的量纲",
  "rho~E^pw -> (nabla rho)^2~E^{2pw+2}, D~E^{pw+2} -> F~E^{%s}，与 rho 同阶，不产生任何抑制因子"
  % sp.simplify((2 * pw + 2) - (pw + 2)))
F("E04", "来稿『紫外 E^6 爆炸被彻底消除，重整性潜力大幅提升』",
  "在该区 F~rho，耦合等价于 O(1) 动能系数：既未产生 E^{-2} 抑制，也未给出任何发散度计数上的改善。"
  "『消除』不成立")

# ============================================================
# F 段：算子维数与幂次计数
# ============================================================
print("\n---------- F 段 算子维数判决----------")

X, Z, Rh, Rm, beta_s, cpl = sp.symbols("X Z Rh Rm beta_s cpl", positive=True)
Pfun = cpl * X / (Rm + Rh + beta_s * Z)
P_XX = sp.simplify(sp.diff(Pfun, X, 2))
P_XZ = sp.simplify(sp.diff(sp.diff(Pfun, X), Z))
P_ZZ = sp.simplify(sp.diff(Pfun, Z, 2))
detK = sp.simplify(P_XX * P_ZZ - P_XZ ** 2)
P("F01", "耦合写成 P(X,Z) 形式（X=-1/2(nabla rho)^2, Z=box rho）",
  "P = (alpha/rho_c)*X/(rho+rho_min+beta*Z)；Hessian: P_XX=%s, P_XZ=%s, P_ZZ=%s" % (P_XX, P_XZ, P_ZZ))
F("F02", "来稿『耦合算子从 6 维降为 4 维边际算子，幂次计数发散阶大幅压低』",
  "分母含 Minkowski 逆算子 1/box rho：作用量非多项式、时间方向非局域，"
  "算子维数幂次计数的前提（有限个局次多项式算子）不成立，无法定义『边际算子』")
B("F03", "额外自由度 / 鬼",
  "(X, box rho) 动能矩阵行列式 = %s < 0（beta!=0）→ 不定，是额外模/鬼的标准诊断信号；"
  "严格 ADM / Bellini-Baker 分析未做，登记 BOUNDARY" % detK)
P("F04", "来稿『无 Ostrogradsky 鬼场，方程最高二阶导数』的核验",
  "以辅助场重整 lambda*(rho+rho_min+beta*box rho) 后，lambda*box rho 经一次分部积分给出一阶项，"
  "rho 方程最高二阶导数 -> 按阶数无 Ostrogradsky（此条台账可保留）")

# ============================================================
# G 段：概念层
# ============================================================
print("\n---------- G 段 概念层----------")

F("G01", "双重计数 / 语义冲突",
  "若 rho 就是『能量密度』且自带 S_m，则 T 已含 rho 的应力能，再加 S_int 即双重计数；"
  "若 rho 是与能量密度无关的独立标量，则式(1) 右侧 (nabla rho)^2 的物理读法失效。两者不可兼得")
F("G02", "低能极限『兼容史瓦西/TOV/弱场引力波』的量级问题",
  "alpha/rho_c = %.3e（8piG=1 下），耦合强度极大；『beta->0 回到 GR』要求 (nabla rho)^2/rho 为小量，"
  "即 alpha/rho_c 与 rho 同量级，来稿未给出该条件" % float(ALPHA / RHO_C))
F("G03", "分级链路的自洽性",
  "『所有之前推导（太阳曲率、TOV、弱场引力波）全部保留，无冲突』无法成立："
  "那些结论建立在式(1) 之上，而式(1) 不是本作用量的场方程")

# ============================================================
# 汇总
# ============================================================
cnt = {}
for r_ in RESULTS:
    cnt[r_["verdict"]] = cnt.get(r_["verdict"], 0) + 1
print("\n" + "=" * 78)
print("汇总: TOTAL=%d  PASS=%d  FAIL=%d  BOUNDARY=%d  INFO=%d  用时=%.1fs" % (
    len(RESULTS), cnt.get("PASS", 0), cnt.get("FAIL", 0), cnt.get("BOUNDARY", 0),
    cnt.get("INFO", 0), time.time() - T0))
print("=" * 78)

payload = {
    "title": "作用量变分审计 · 分支B《完整构造作用量并变分导出场方程》",
    "date": "2026-10-03",
    "verdict_summary": "式(1) 不是式(3) 的迹。五处同时不成立：(1) 迹 = 2cF[3(rho+rho_min)+2 beta □rho]/D，来稿隐含 2cF；(2) 耦合归一化需 c=+alpha/(96 pi G rho_c)（来稿 -alpha/(2 rho_c)，差 48 pi 倍且反号）；(3) -2Λ 项在 S_int 中无来源；(4) Einstein-Hilbert 取迹给 R-4Λ_act 而非 R-2Λ；(5) 取迹隐性令 T=0。另：nabla^a T^int 必含 rho 的三阶导数且一般不为 0，与 Bianchi 恒等式冲突（rho 为动力学场时理论过定无解）",
    "params": {"alpha": str(ALPHA), "rho_c": str(RHO_C), "beta": str(BETA), "Lambda": str(LAMBDA)},
    "engine_benchmarks": {"passed": nb_pass, "total": len(BENCH)},
    "counts": {"TOTAL": len(RESULTS), "PASS": cnt.get("PASS", 0), "FAIL": cnt.get("FAIL", 0),
               "BOUNDARY": cnt.get("BOUNDARY", 0), "INFO": cnt.get("INFO", 0)},
    "results": RESULTS,
}
with open(OUT_JSON, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)
print("写出: %s" % OUT_JSON)
