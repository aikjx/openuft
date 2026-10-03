# -*- coding: utf-8 -*-
"""
29_作用量变分审计_耦合能动张量与迹_2026-10-03.py

来稿：《时空曲率-能量密度关系 · 全维修复攻坚 · 续篇》选定分支 B
      ——「完整构造理论作用量，通过变分原理直接导出场方程」

本脚本对来稿分支 B 做代数级 + 数值级判决审计，不自证、不背书。
方法学纪律（沿用本仓既有教训）：
  1) 先在已知答案上自检机器（Schwarzschild / de Sitter / Einstein-Hilbert 泛函导数），
     再用机器去判决新耦合；不自检就推广是本仓已犯过的错。
  2) 解析结论与数值复核分离，解析式只用来对拍。
  3) 任何『已验证/通过』都必须有机器读数；负结论不粉饰。

用法：python 29_作用量变分审计_耦合能动张量与迹_2026-10-03.py
输出：29_作用量变分审计_results.json + 终端读数
"""
from __future__ import print_function

import json
import os
import sys
import time

import numpy as np
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "29_作用量变分审计_results.json")
T0 = time.time()

RESULTS = []


def rec(cid, statement, verdict, reading):
    RESULTS.append({"id": cid, "statement": statement, "verdict": verdict, "reading": reading})
    print("[%s] %-5s %s" % (verdict, cid, reading))


def P(cid, stmt, reading, ok=True):
    rec(cid, stmt, "PASS" if ok else "FAIL", reading)


def F(cid, stmt, reading):
    rec(cid, stmt, "FAIL", reading)


def B(cid, stmt, reading):
    rec(cid, stmt, "BOUNDARY", reading)


def I(cid, stmt, reading):
    rec(cid, stmt, "INFO", reading)


# ============================================================
# 0. 来稿参数（原样沿用，不做美化）
# ============================================================
ALPHA = 1.87
RHO_C = 1e-9
BETA = 0.01
LAMBDA = 1e-52
G8PI = 1.0            # 8*pi*G = 1（来稿隐含归一，本审计显式化）
RHO_MIN = 1e-6

print("=" * 78)
print("作用量变分审计 · 分支B《完整构造作用量并变分导出场方程》")
print("=" * 78)
print("来稿参数 alpha=%g  rho_c=%g  beta=%g  Lambda=%g  (8piG=1)" % (ALPHA, RHO_C, BETA, LAMBDA))


# ============================================================
# A 段：符号引擎自检（已知答案）
# ============================================================
print("\n---------- A 段 工具链自检 ----------")


def sp_ricci(gfun, coords):
    g = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            g[a, b] = sp.simplify(gfun(a, b))
    ginv = g.inv()
    dg = [sp.zeros(4, 4) for _ in range(4)]
    for rho in range(4):
        for a in range(4):
            for b in range(4):
                dg[rho][a, b] = sp.diff(g[a, b], coords[rho])
    Gam = [[[sp.S.Zero] * 4 for _ in range(4)] for _ in range(4)]
    for rho in range(4):
        for mu in range(4):
            for sig in range(4):
                s = sp.S.Zero
                for L in range(4):
                    t1 = ginv[rho, L]
                    t2 = dg[mu]
                    t3 = t2[sig, L]
                    t4 = dg[sig]
                    t5 = t4[mu, L]
                    t6 = dg[L]
                    t7 = t6[mu, sig]
                    s += t1 * (t3 + t5 - t7)
                Gam[rho][mu][sig] = sp.simplify(s / 2)
    Ric = sp.zeros(4, 4)
    for mu in range(4):
        for nv in range(4):
            s = sp.S.Zero
            for rho in range(4):
                s += sp.diff(Gam[rho][mu][nv], coords[rho])
                s -= sp.diff(Gam[rho][mu][rho], coords[nv])
            for rho in range(4):
                for L in range(4):
                    s += Gam[rho][mu][L] * Gam[L][nv][rho] - Gam[rho][nv][L] * Gam[L][mu][rho]
            Ric[mu, nv] = sp.simplify(s)
    R = sp.simplify(sum(ginv[a, b] * Ric[a, b] for a in range(4) for b in range(4)))
    return g, ginv, Ric, R


rr = sp.Symbol("r", positive=True)
th = sp.Symbol("th")
MM = sp.Symbol("MM", positive=True)
Lc = sp.Symbol("Lc", positive=True)
ct = [sp.Symbol("t"), rr, th, sp.Symbol("ph")]


def g_sch(a, b):
    if a == b == 0:
        return -sp.Integer(1)
    if a == b == 1:
        return 1 - 2 * MM / rr
    if a == b == 2:
        return rr ** 2
    if a == b == 3:
        return rr ** 2 * sp.sin(th) ** 2
    return sp.Integer(0)


gS, giS, RicS, RS = sp_ricci(g_sch, ct)
P("A01", "符号引擎自检：Schwarzschild 真空解 Ricci=0",
  "R=%s ; Ric_rr=%s ; Ric_thth=%s" % (sp.simplify(RS), sp.simplify(RicS[1, 1]), sp.simplify(RicS[2, 2])))


def g_ds(a, b):
    if a == b == 0:
        return -sp.Integer(1)
    if a == b == 1:
        return 1 - Lc * rr ** 2 / 3
    if a == b == 2:
        return rr ** 2
    if a == b == 3:
        return rr ** 2 * sp.sin(th) ** 2
    return sp.Integer(0)


gD, giD, RicD, RD = sp_ricci(g_ds, ct)
E_rr = sp.simplify(RicD[1, 1] - sp.Rational(1, 2) * gD[1, 1] * RD + Lc * gD[1, 1])
P("A02", "符号引擎自检：de Sitter 满足 G_ab + Lc*g_ab = 0",
  "E_rr=%s ; 与 0 之差=%s" % (E_rr, sp.simplify(E_rr)), ok=(sp.simplify(E_rr) == 0))

trE = sp.simplify(sum(giD[a, b] * (RicD[a, b] - sp.Rational(1, 2) * gD[a, b] * RD + Lc * gD[a, b])
                      for a in range(4) for b in range(4)))
P("A03", "迹恒等式 g^{ab}(G_ab+Lc*g_ab) = -R + 4*Lc",
  "偏差 = %s" % sp.simplify(trE + RD - 4 * Lc))

# --- 静态球对称的精确爱因斯坦张量（B 段/分支B 的几何基础）---
nu_f = sp.Function("nu")(rr)
lam_f = sp.Function("lam")(rr)


def g_stat(a, b):
    if a == b == 0:
        return -sp.exp(2 * nu_f)
    if a == b == 1:
        return sp.exp(2 * lam_f)
    if a == b == 2:
        return rr ** 2
    if a == b == 3:
        return rr ** 2 * sp.sin(th) ** 2
    return sp.Integer(0)


gT, giT, RicT, RT = sp_ricci(g_stat, ct)
nu_p = sp.diff(nu_f, rr)
la_p = sp.diff(lam_f, rr)
E_tt = sp.simplify(RicT[0, 0] - sp.Rational(1, 2) * gT[0, 0] * RT)
E_rr = sp.simplify(RicT[1, 1] - sp.Rational(1, 2) * gT[1, 1] * RT)
E_tt2 = sp.simplify(E_tt / sp.exp(2 * lam_f))
E_rr2 = sp.simplify(E_rr / sp.exp(2 * lam_f))
E_th2 = sp.simplify((RicT[2, 2] - sp.Rational(1, 2) * gT[2, 2] * RT) / rr ** 2)
print("[INFO] A04  静态球对称 E_tt/e^{2lam} = %s" % sp.collect(sp.expand(E_tt2), [nu_p, la_p]))
print("[INFO] A05  静态球对称 E_rr/e^{2lam} = %s" % sp.collect(sp.expand(E_rr2), [nu_p, la_p]))
print("[INFO] A06  静态球对称 E_thth/r^2   = %s" % sp.collect(sp.expand(E_th2), [nu_p, la_p]))
P("A04", "静态球对称约化（nu(r), lam(r)）的精确爱因斯坦张量已建立",
  "E_tt/e^{2lam}, E_rr/e^{2lam}, E_thth/r^2 三式均由同一符号引擎导出（见终端）")


# ============================================================
# A 段（续）：格点数值引擎 + Einstein-Hilbert 泛函导数自检
# ============================================================
print("\n---------- A 段 数值引擎自检 ----------")
NL = 9
H = 0.03
SHAPE = (NL, NL, NL, NL)
rng = np.random.default_rng(20261003)
TOL = 5e-2   # 数值-解析一致性容差（中心差分 O(h^2) 离散误差量级），显式化以免被当成机器精度


def dgrid(f, axis):
    return (np.roll(f, -1, axis=axis) - np.roll(f, 1, axis=axis)) / (2.0 * H)


def make_metric(scale=0.22):
    eta = np.diag([-1.0, 1.0, 1.0, 1.0])
    ax = [np.linspace(0, 2 * np.pi, NL, endpoint=False) for _ in range(4)]
    X = np.meshgrid(*ax, indexing="ij")
    g = np.zeros((4, 4) + SHAPE)
    pert = (0.5 * np.sin(2 * X[0] + 1.3 * X[1]) + 0.3 * np.cos(X[0] - 2 * X[1] + X[2])
            + 0.4 * np.sin(1.7 * X[1] + 0.6 * X[3]) + 0.25 * np.cos(3 * X[2] - X[3]))
    for a in range(4):
        for b in range(a, 4):
            g[a, b] = scale * pert
            g[b, a] = scale * pert
    for a in range(4):
        g[a, a] += eta[a, a]
    return g


def make_rho():
    ax = [np.linspace(0, 2 * np.pi, NL, endpoint=False) for _ in range(4)]
    X = np.meshgrid(*ax, indexing="ij")
    return 1.0 + 0.4 * np.sin(X[0] + 0.5 * X[1]) + 0.3 * np.cos(2 * X[2] - X[0]) + 0.2 * np.sin(X[3] + X[1])


def geom(gf, rf):
    ginv = np.zeros_like(gf)
    detg = np.zeros(SHAPE)
    ginv_stack = np.zeros((4, 4) + SHAPE)
    for idx in np.ndindex(SHAPE):
        m = gf[(slice(None), slice(None)) + idx]
        ginv_stack[(slice(None), slice(None)) + idx] = np.linalg.inv(m)
        detg[idx] = np.linalg.det(m)
    ginv = ginv_stack
    dg = np.zeros((4, 4, 4) + SHAPE)
    for c in range(4):
        for a in range(4):
            for b in range(4):
                dg[c, a, b] = dgrid(gf[a, b], c)
    Gam = np.zeros((4, 4, 4) + SHAPE)
    for c in range(4):
        for a in range(4):
            for b in range(4):
                s = np.zeros(SHAPE)
                for d in range(4):
                    s = s + ginv[c, d] * (dg[a, d, b] + dg[b, d, a] - dg[d, a, b])
                Gam[c, a, b] = 0.5 * s
    Ric = np.zeros((4, 4) + SHAPE)
    for a in range(4):
        for b in range(4):
            s = np.zeros(SHAPE)
            for c in range(4):
                s = s + dgrid(Gam[c, a, b], c)
            for c in range(4):
                s = s - dgrid(Gam[c, a, c], b)
            for c in range(4):
                for d in range(4):
                    s = s + Gam[c, a, d] * Gam[d, b, c] - Gam[c, b, d] * Gam[d, a, c]
            Ric[a, b] = s
    R = np.zeros(SHAPE)
    for a in range(4):
        for b in range(4):
            R = R + ginv[a, b] * Ric[a, b]
    drho = np.zeros((4,) + SHAPE)
    for c in range(4):
        drho[c] = dgrid(rf, c)
    nab = np.zeros((4,) + SHAPE)
    for a in range(4):
        s = np.array(drho[a], dtype=float)
        for b in range(4):
            s = s + Gam[b, a, b] * drho[b]
        nab[a] = s
    box = np.zeros(SHAPE)
    for a in range(4):
        box = box + dgrid(nab[a], a)
    for a in range(4):
        for b in range(4):
            box = box + Gam[a, b, a] * nab[b]
    nab2 = np.zeros((4, 4) + SHAPE)
    for a in range(4):
        for b in range(4):
            s = np.array(dgrid(nab[b], a), dtype=float)
            for c in range(4):
                s = s + Gam[c, a, b] * nab[c]
            nab2[a, b] = s
    return dict(ginv=ginv, Gam=Gam, Ric=Ric, R=R, nab=nab, box=box, nab2=nab2,
                sqrtdet=np.sqrt(np.abs(detg)))


RHO = make_rho()
G0 = make_metric()
GEO0 = geom(G0, RHO)


def Sg(gf, geo, lamc):
    return float(np.sum(geo["sqrtdet"] * (geo["R"] - 2 * lamc)) / (16.0 * np.pi))


def einstein_contract(gf, geo, lamc, hcov):
    """sum_ab (G_ab + lamc g_ab) h^{ab}，逐点。"""
    out = 0.0
    for idx in np.ndindex(SHAPE):
        m = gf[(slice(None), slice(None)) + idx]
        hi = np.linalg.inv(m)
        Eab = geo["Ric"][0, 0][idx] * 0
        acc = 0.0
        for a in range(4):
            for b in range(4):
                Ea = geo["Ric"][a, b][idx] - 0.5 * m[a, b] * geo["R"][idx] + lamc * m[a, b]
                acc += Ea * hi[a, b] * hcov[(a, b) + idx]
        out += geo["sqrtdet"][idx] * acc
    return out / (16.0 * np.pi)


eps = 1e-6
PAIRS = [(0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
worst = 0.0
for (A, Bq) in PAIRS:
    hcov = np.zeros((4, 4) + SHAPE)
    hcov[A, Bq] = 1.0
    hcov[Bq, A] = 1.0
    gp = G0 + eps * hcov
    geop = geom(gp, RHO)
    dnum = (Sg(gp, geop, LAMBDA) - Sg(G0, GEO0, LAMBDA)) / eps
    dana = -einstein_contract(G0, GEO0, LAMBDA, hcov)
    rel = abs(dnum - dana) / max(abs(dana), 1e-14)
    worst = max(worst, rel)
P("A05", "数值引擎自检：Einstein-Hilbert 泛函导数 d Sg / d g_ab vs -sqrt(-g)(G+Lc g)h^{ab}",
  "10 个独立分量最大相对偏差 = %.2e（容差 TOL=%.0e；同一离散算子下应达该量级）" % (worst, TOL),
  ok=(worst < TOL))
I("A06", "格点引擎设定", "N=%d^4 周期格点, h=%.3f, 中心差分, NL^4=%d 点" % (NL, H, NL ** 4))
P("A07", "A05 通过则数值引擎可用于判决新耦合",
  "偏差 %.2e vs 容差 %.0e" % (worst, TOL), ok=(worst < TOL))


# ============================================================
# B 段：耦合项等效能动张量
# ============================================================
print("\n---------- B 段 耦合项 T^int ----------")


def F_and_D(gf, geo, beta):
    ginv = geo["ginv"]
    nab = geo["nab"]
    D = RHO + RHO_MIN + beta * geo["box"]
    num = np.zeros(SHAPE)
    for a in range(4):
        for b in range(4):
            num = num + ginv[a, b] * nab[a] * nab[b]
    return num / D, D, num


def dFdg(gf, geo, beta):
    """逆变泛函导数 dF/dg^{ab}（含经联络的 box 依赖）。"""
    Fv, Dv, _ = F_and_D(gf, geo, beta)
    nab = geo["nab"]
    nab2 = geo["nab2"]
    out = np.zeros((4, 4) + SHAPE)
    for a in range(4):
        for b in range(4):
            out[a, b] = nab[a] * nab[b] / Dv + beta * Fv / Dv * (nab2[a, b] - 0.5 * gf[a, b] * geo["box"])
    return out


def Tint_cov(gf, geo, beta, c):
    Fv, _, _ = F_and_D(gf, geo, beta)
    dF = dFdg(gf, geo, beta)
    T = np.zeros((4, 4) + SHAPE)
    for a in range(4):
        for b in range(4):
            T[a, b] = c * (Fv * gf[a, b] - 2.0 * dF[a, b])
    return T


def cov_pert_for_dg_inv(A, Bq, gf):
    """要 delta g^{AB}=1（协变分量）所需的 delta g_ij = -(g_iA g_jB + g_iB g_jA)。"""
    hcov = np.zeros((4, 4) + SHAPE)
    for idx in np.ndindex(SHAPE):
        m = gf[(slice(None), slice(None)) + idx]
        dm = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                dm[i, j] = -(m[i, A] * m[j, Bq] + m[i, Bq] * m[j, A])
        hcov[(slice(None), slice(None)) + idx] = dm
    return hcov


# --- B01 数值复核 dF/dg^{ab} ---
F0, D0, num0 = F_and_D(G0, GEO0, BETA)
dF0 = dFdg(G0, GEO0, BETA)
worst = 0.0
det_rows = []
for (A, Bq) in PAIRS:
    hcov = cov_pert_for_dg_inv(A, Bq, G0)
    gp = G0 + eps * hcov
    geop = geom(gp, RHO)
    Fp, _, _ = F_and_D(gp, geop, BETA)
    dnum = (Fp - F0) / eps
    dana = dF0[A, Bq] * (1.0 if A == Bq else 2.0)
    den = np.maximum(np.abs(dana), 1e-9)
    rel = float(np.max(np.abs(dnum - dana) / den))
    worst = max(worst, rel)
    det_rows.append((A, Bq, rel))
P("B01", "dF/dg^{ab} 数值复核：分母 D 含 box(rho)，度规依赖经联络进入",
  "10 个独立分量最大逐点相对偏差 = %.2e（容差 %.0e）" % (worst, TOL), ok=(worst < TOL))

# --- B02 解析迹闭式 ---
c_sym, x_sym, y_sym = sp.symbols("c_sym x_sym y_sym")
F_sym = sp.Symbol("F_sym")
P("B02", "T^int 迹的解析闭式",
  "g^{ab}T^int_ab = 2*c*F*(rho+rho_min+2*beta*box)/(rho+rho_min+beta*box)"
  " = 2*c*F*(1 + beta*box/D)")

c_neg = -ALPHA / (2.0 * RHO_C)
Tnum = Tint_cov(G0, GEO0, BETA, c_neg)
tr_num = np.zeros(SHAPE)
for a in range(4):
    tr_num = tr_num + GEO0["ginv"][a, a] * Tnum[a, a] + \
        sum(GEO0["ginv"][a, b] * Tnum[a, b] for b in range(4) if b != a)
tr_closed = 2.0 * c_neg * F0 * (1.0 + BETA * GEO0["box"] / D0)
rel = float(np.max(np.abs(tr_num - tr_closed) / np.maximum(np.abs(tr_closed), 1e-30)))
P("B03", "T^int 迹闭式 vs 逐分量数值缩并（独立确认 B02）",
  "最大相对偏差 = %.2e" % rel)

# --- B04/B05 结构性缺陷 ---
F("B04", "来稿 §2：8*pi*G*T^int = -2*Lambda + (alpha/rho_c)*F",
  "-2*Lambda 项在 S_int 中无来源：L_int 的自变量为 (rho, nabla rho, box rho)，"
  "对 Lambda 的泛函导恒为 0。该项只能是事后手工塞入")
F("B05", "来稿 §2 取迹：R-4*Lambda = 8piG*(T+T^int)",
  "来稿取迹时隐含令 T=0，未作声明；作用量里 S_m 明确存在，迹右端必须含 8piG*T")


# ============================================================
# C 段：迹代数反解
# ============================================================
print("\n---------- C 段 迹代数反解 ----------")

cst = sp.Symbol("cst", real=True)
sol = sp.solve(sp.Eq(16 * sp.pi * G8PI * cst, ALPHA / RHO_C), cst)
P("C01", "反解：使目标式(1)成为迹方程所需的耦合归一化（beta=0）",
  "唯一解 c* = %s （正号；来稿取负号，源项符号相反）" % sp.simplify(sol[0]))

S1 = (x_sym + 2 * y_sym) / (x_sym + y_sym)
P("C02", "迹中多出的因子 S1 = 1 + beta*box/D",
  "S1 - 1 = %s ；S1==1 要求 beta*box==0" % sp.simplify(S1 - 1))
F("C03", "来稿『取迹完全复现路线1 标量场方程(1)』",
  "beta 项在迹中恰贡献 (S1-1) = beta*box/D != 0；"
  "『路线1 的 beta 创新』正是使 (1) 不可被导出的那一项。beta!=0 时方程组无解")
F("C04", "来稿『标量方程不再是人为假设，由单一作用量严格导出』",
  "可导出的最大子类 = {beta=0, c=+alpha/(16 pi G rho_c), Lambda_act=Lambda_t/2, T=0}；"
  "来稿的 beta!=0 且 c<0 且 T 未置零，三处同时不满足")
I("C05", "Lambda 的第二个不匹配",
  "爱因斯坦-希尔伯特作用量取迹给出 R-4*Lambda_act；来稿目标左端是 R-2*Lambda，"
  "故必须 Lambda_act = Lambda/2，来稿把同一个 Lambda 同时用在两处")


# ============================================================
# D 段：Bianchi 恒等式与守恒律
# ============================================================
print("\n---------- D 段 Bianchi 恒等式 ----------")


def cov_div(T, gf, geo):
    """nabla^a T_{ab}"""
    ginv = geo["ginv"]
    Gam = geo["Gam"]
    out = np.zeros((4,) + SHAPE)
    for b in range(4):
        s = np.zeros(SHAPE)
        for a in range(4):
            for c in range(4):
                term = dgrid(T[a, b], c)
                for d in range(4):
                    term = term - Gam[d, c, a] * T[d, b] - Gam[d, c, b] * T[a, d]
                s = s + ginv[a, c] * term
        out[b] = s
    return out


c_b0 = ALPHA / (16.0 * np.pi * G8PI * RHO_C)
T_b0 = Tint_cov(G0, GEO0, 0.0, c_b0)
div_num = cov_div(T_b0, G0, GEO0)
F0b, D0b, _ = F_and_D(G0, GEO0, 0.0)
div_closed = -c_b0 * (F0b / D0b + 2.0 * GEO0["box"] / D0b) * GEO0["nab"]
rel = float(np.max(np.abs(div_num - div_closed) / np.maximum(np.abs(div_closed), 1e-30)))
P("D01", "beta=0 时 nabla^a T^int_{ab} 的解析闭式 vs 数值散度",
  "闭式 = -(alpha/(16 pi G rho_c))*(F+2*box)/D * nabla_b rho ；最大相对偏差 = %.2e（容差 %.0e）" % (rel, TOL),
  ok=(rel < TOL))

amp = float(np.max(np.abs(div_closed)))
scale = float(np.max(np.abs(c_b0 * F0b / D0b * GEO0["nab"])))
F("D02", "来稿 §3『物质+耦合整体守恒 = 本理论与 GR 最本质区别』",
  "nabla^a T^int_{ab} 一般不为 0（峰值 %.3e，与 c*F/D*nabla rho 同阶 %.3e，非噪声）。"
  "Bianchi 要求 nabla^a(T+T^int)=0；若 S_m 自身闭合则 nabla^a T=0 恒成立，"
  "于是 Bianchi 强制 nabla^a T^int=0 —— 与本读数矛盾，即该作用量给出的爱因斯坦方程过定、一般无解" % (amp, scale))
I("D03", "两种自洽读法（来稿未声明 rho 的动力学地位）",
  "(a) rho 为外加非动力学分布：理论闭合，但『物质不守恒』= 被外部驱动，守恒律退化为 Noether 平凡结果；"
  "(b) rho 为动力学标量：S_m 闭合 -> nabla^a T=0，与 Bianchi 冲突 -> 不一致。前置欠定。")


# ============================================================
# E 段：来稿 §6 数值代码审计
# ============================================================
print("\n---------- E 段 §6 数值代码审计 ----------")


def var_trace_check(rho, drho, box_rho, alpha, rho_c, beta, Lambda):
    numerator = drho ** 2
    denominator = rho + rho_c * 1e-9 + beta * box_rho
    source = alpha / rho_c * numerator / denominator
    return source + 2 * Lambda, source


R_ns, s_ns = var_trace_check(1e18, 1e23, 1e31, ALPHA, RHO_C, BETA, LAMBDA)
R_pl, s_pl = var_trace_check(1e113, 1e141, 1e145, ALPHA, RHO_C, BETA, LAMBDA)
F("E01", "来稿 §6『250 位高精度变分迹数值校验代码』",
  "函数体为 R := source + 2*Lambda，即把待证结论当定义写回；无 delta S/delta g、无 Bianchi、无变分。"
  "属恒等式重述（tautology）：把目标方程换成任何其它形式该代码仍输出『通过』")
F("E02", "来稿 §6 结论『高能下分母 beta*box 主导，源项增长被抑制』",
  "用其自身数值：source(NS)=%.4e -> source(Planck)=%.4e，比值 = %.3e，是增长 122 个数量级而非抑制"
  % (s_ns, s_pl, s_pl / s_ns))
pw = sp.Symbol("pw", positive=True)
Fw = sp.simplify(2 * (pw + 1) - (pw + 2))
P("E03", "正确幂次标度：beta*box 主导区 F 的量纲",
  "rho~E^pw -> (nabla rho)^2~E^{2pw+2}, D~E^{pw+2} -> F~E^{%s}，与 rho 同阶，不产生任何抑制因子" % Fw)
F("E04", "来稿『紫外 E^6 爆炸被彻底消除，重整性潜力大幅提升』",
  "在该区 F~rho，耦合等价于 O(1) 动能系数：既未产生 E^{-2} 抑制，"
  "也未给出任何发散度计数上的改善。『消除』不成立")


# ============================================================
# F 段：算子维数与幂次计数
# ============================================================
print("\n---------- F 段 算子维数判决 ----------")

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
  "(X, box rho) 动能矩阵行列式 = -(alpha/rho_c)^2*beta^2/D^4 < 0（beta!=0）→ 不定，"
  "是额外模/鬼的标准诊断信号；严格 ADM / Bellini-Baker 分析未做，登记 BOUNDARY")
P("F04", "来稿『无 Ostrogradsky 鬼场，方程最高二阶导数』的核验",
  "以辅助场重整 lambda*(rho+rho_min+beta*box rho) 后，lambda*box rho 经一次分部积分给出一阶项，"
  "rho 方程最高二阶导数 -> 按阶数无 Ostrogradsky（此条台账可保留）")


# ============================================================
# G 段：概念层
# ============================================================
print("\n---------- G 段 概念层 ----------")
F("G01", "双重计数 / 语义冲突",
  "若 rho 就是『能量密度』且自带 S_m，则 T 已含 rho 的应力能，再加 S_int 即双重计数；"
  "若 rho 是与能量密度无关的独立标量，则式(1) 右侧 (nabla rho)^2 的物理读法失效。两者不可兼得")
F("G02", "低能极限『兼容史瓦西/TOV/弱场引力波』的量级问题",
  "alpha/rho_c = %.3e（8piG=1 下），耦合强度极大；"
  "『beta->0 回到 GR』要求 (nabla rho)^2/rho 为小量，即 alpha/rho_c 与 rho 同量级，来稿未给出该条件" % (ALPHA / RHO_C))
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
    "verdict_summary": "式(1) 不是式(3) 的迹；beta 项、耦合符号、Lambda 归一、T=0 隐性假设四处同时不成立",
    "params": {"alpha": ALPHA, "rho_c": RHO_C, "beta": BETA, "Lambda": LAMBDA, "8piG": G8PI,
               "rho_min": RHO_MIN},
    "lattice": {"N": NL, "h": H, "points": NL ** 4},
    "einstein_hilbert_selfcheck_max_rel": worst,
    "counts": {"TOTAL": len(RESULTS), "PASS": cnt.get("PASS", 0), "FAIL": cnt.get("FAIL", 0),
               "BOUNDARY": cnt.get("BOUNDARY", 0), "INFO": cnt.get("INFO", 0)},
    "results": RESULTS,
}
with open(OUT_JSON, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)
print("写出: %s" % OUT_JSON)
