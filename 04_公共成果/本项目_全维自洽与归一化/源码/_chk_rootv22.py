# -*- coding: utf-8 -*-
"""
ROOT V22.0 来料复算（整理册佐证，不占 r 号）
  1) 双耦合示范系统：符号固定点 / 精确 Jacobian / 特征值 / 线性解残差 / 三条非线性轨道
  2) 渐近自由尺度嬗变：一圈 QCD 三组输入的 Lambda 与条件数
  3) 轻子一圈真空极化：mpmath 85 位求积 + r321 闭式对拍
  4) 唯一权威门禁 _audit_acceptance.discriminate 复验该路线类别
输出：同目录 _out_rootv22.txt（utf-8）
"""
import io
import os
import sys

import mpmath as mp
import sympy as sp

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "_out_rootv22.txt")

LINES = []
GUARDS = []


def log(s=""):
    LINES.append(s)
    print(s)


def guard(name, ok, detail=""):
    GUARDS.append((name, bool(ok), detail))
    log("  [%s] %-38s %s" % ("PASS" if ok else "FAIL", name, detail))


def rel(a, b):
    return abs(a - b) / abs(b) if b != 0 else abs(a - b)


# ---------------------------------------------------------------------------
# 1. 双耦合示范系统
# ---------------------------------------------------------------------------
log("=" * 78)
log("§1 双耦合示范系统  beta_a=a^2(1/25+a-4y),  beta_y=y(2y-a)")
log("=" * 78)

a, y = sp.symbols("a y", positive=True)
ba = a ** 2 * (sp.Rational(1, 25) + a - 4 * y)
by = y * (2 * y - a)

sols = sp.solve([ba, by], [a, y], dict=True)
log("  solve(beta=0) 全部解: %s" % sols)
nonzero = [s for s in sols if s.get(a, 0) != 0 and s.get(y, 0) != 0]
log("  非零固定点: %s" % nonzero)
a_s, y_s = sp.Rational(1, 25), sp.Rational(1, 50)

log("  解析复算 beta_a(g*) = %s ; beta_y(g*) = %s"
    % (sp.simplify(ba.subs({a: a_s, y: y_s})), sp.simplify(by.subs({a: a_s, y: y_s}))))
guard("FP_BETA_ZERO_EXACT", sp.simplify(ba.subs({a: a_s, y: y_s})) == 0
      and sp.simplify(by.subs({a: a_s, y: y_s})) == 0,
      "符号代回残差 = 0（精确有理，非浮点）")

J = sp.Matrix([[sp.diff(ba, a), sp.diff(ba, y)],
               [sp.diff(by, a), sp.diff(by, y)]]).subs({a: a_s, y: y_s})
J_claim = sp.Matrix([[sp.Rational(1, 625), sp.Rational(-4, 625)],
                     [sp.Rational(-1, 50), sp.Rational(1, 25)]])
log("  Jacobian B* = %s   (trace=%s, det=%s)" % (J.tolist(), sp.trace(J), J.det()))
guard("JACOBIAN_MATCH", J == J_claim, "与来料矩阵逐元素相等（精确有理）")

ev = J.eigenvals()
ev_exact = list(ev.keys())
lam1, lam2 = sorted([sp.nsimplify(k) for k in ev_exact], key=lambda z: float(z.evalf()))
log("  特征值精确: %s ; %s" % (sp.srepr(lam1), sp.srepr(lam2)))
l1f, l2f = float(lam1.evalf(30)), float(lam2.evalf(30))
log("  特征值浮点: %.12f / %.12f" % (l1f, l2f))
log("  来料声明:   -0.00148542124 / +0.04308542124")
guard("EIGENVALUES_MATCH", rel(l1f, -0.00148542124) < 5e-9 and rel(l2f, 0.04308542124) < 5e-9,
      "相对差 %.2e / %.2e" % (rel(l1f, -0.00148542124), rel(l2f, 0.04308542124)))
guard("EIGENVALUE_SIGN_SPLIT", l1f < 0 < l2f,
      "一负一正 ⇒ 1 个 UV 吸引方向 + 1 个 UV 排斥方向（鞍点）")

# 线性化解残差（符号）
t, C1, C2 = sp.symbols("t C1 C2", real=True)
vecs = J.eigenvects()
v_neg = [sp.Matrix(v[2][0]) for v in vecs if float(v[0].evalf()) < 0][0]
v_pos = [sp.Matrix(v[2][0]) for v in vecs if float(v[0].evalf()) > 0][0]
log("  UV 吸引特征向量 v1 = %s" % v_neg.T.tolist())
log("  UV 排斥特征向量 v2 = %s" % v_pos.T.tolist())
delta = C1 * sp.exp(lam1 * t) * v_neg + C2 * sp.exp(lam2 * t) * v_pos
lin_res = sp.simplify(sp.diff(delta, t) - J * delta)
guard("LINEAR_SOLUTION_RESIDUAL_ZERO", lin_res == sp.zeros(2, 1),
      "d(δg)/dt − B*δg = %s" % lin_res.T.tolist())

# 单位化后，e_a 方向在 v1 上的投影（IR 存活幅度）
v1u = v_neg / v_neg.norm()
proj_a = float(v1u[0])
log("  单位化 v1 的 a 分量 = %.10f ⇒ IR 端 δa ≈ C1·e^{|λ1|Δ}·%.6f" % (proj_a, proj_a))

# 非线性 RK4：从 UV(1e19 GeV) 积到 IR(1 GeV)
f = sp.lambdify((a, y), (ba, by), "math")
gstar = (float(a_s), float(y_s))


def rk4(g0, t0, t1, h):
    g = list(g0)
    tt = t0
    n = int(abs((t1 - t0) / h))
    for _ in range(n):
        k1 = f(*g)
        k2 = f(g[0] + 0.5 * h * k1[0], g[1] + 0.5 * h * k1[1])
        k3 = f(g[0] + 0.5 * h * k2[0], g[1] + 0.5 * h * k2[1])
        k4 = f(g[0] + h * k3[0], g[1] + h * k3[1])
        g = [g[0] + h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0,
             g[1] + h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0]
        tt += h
    return g


MU_UV, MU_IR = 1.0e19, 1.0
DELTA = mp.log(MU_UV / MU_IR)  # ln(μ_UV/μ_IR)
log("  UV→IR 距离 Δ = ln(1e19/1) = %.6f" % float(DELTA))
endpoints = []
for C in (1e-4, 1e-3, 1e-2):
    g0 = (gstar[0] + C * float(v1u[0]), gstar[1] + C * float(v1u[1]))
    gT = rk4(g0, 0.0, -float(DELTA), -0.005)
    endpoints.append((C, gT[0], gT[1]))
    log("  C1=%8.1e  ⇒  a(IR)=%.10f  y(IR)=%.10f" % (C, gT[0], gT[1]))
spread = max(e[1] for e in endpoints) / min(e[1] for e in endpoints)
dev_ratio = max(e[1] - gstar[0] for e in endpoints) / min(e[1] - gstar[0] for e in endpoints)
log("  a(IR) 绝对极差比 = %.6f ；δa(IR) 偏离极差比 = %.4f（线性预期 C 比 100 × e^{|λ1|Δ}=%.4f）"
    % (spread, dev_ratio, 100 * float(mp.e ** (abs(l1f) * DELTA))))
guard("RK4_THREE_RUNS_OK", all(x == x for e in endpoints for x in e[1:]), "三条轨道无 NaN")
guard("IR_AMPLITUDE_FREE", dev_ratio > 50,
      "同一 UV 固定点、C1 跨 2 数量级 ⇒ a(IR) 偏离跨 %.1f 倍（C1 是自由参数，非预言）" % dev_ratio)

# ---------------------------------------------------------------------------
# 2. 渐近自由尺度嬗变（一圈 QCD）
# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§2 尺度嬗变  Lambda = mu*exp(-2pi/(beta0*alpha_s)), beta0=23/3, mu=100 GeV")
log("=" * 78)
mp.mp.dps = 60
beta0 = mp.mpf(23) / 3
mu0 = mp.mpf(100)
claim = {0.10: mp.mpf("0.02759036"), 0.12: mp.mpf("0.10813454"), 0.14: mp.mpf("0.28686913")}
lam_vals = {}
for als in (0.10, 0.12, 0.14):
    lam = mu0 * mp.e ** (-2 * mp.pi / (beta0 * mp.mpf(str(als))))
    lam_vals[als] = lam
    log("  α_s(100GeV)=%.2f ⇒ Λ=%.10f GeV （来料 %s，相对差 %.2e）"
        % (als, float(lam), mp.nstr(claim[als], 10), float(rel(lam, claim[als]))))
guard("QCD_LAMBDA_MATCH", all(float(rel(lam_vals[k], claim[k])) < 1e-6 for k in claim),
      "三组逐位复现（最大相对差 %.2e）"
      % max(float(rel(lam_vals[k], claim[k])) for k in claim))
cond = float(2 * mp.pi / (beta0 * mp.mpf("0.10")))
log("  条件数 dlnΛ/dlnα_s = 2π/(β0 α_s) = %.6f  (α_s 1%% → Λ 8.2%%)" % cond)
guard("QCD_CONDITION_NUMBER", cond > 1, "输入 0.10→0.14（+40%%）⇒ Λ 0.02759→0.28687（%.1f×）"
      % float(lam_vals[0.14] / lam_vals[0.10]))

# ---------------------------------------------------------------------------
# 3. 轻子一圈真空极化（85 位）
# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§3 轻子一圈真空极化  Δ_f=(2α/π)∫_0^1 x(1-x)ln[1+Q^2x(1-x)/m_f^2]dx")
log("=" * 78)
mp.mp.dps = 85
alpha0 = mp.mpf(1) / mp.mpf("137.035999177")
Q = mp.mpf("91.1876")
fermions = [("e", mp.mpf("0.00051099895000")),
            ("mu", mp.mpf("0.1056583755")),
            ("tau", mp.mpf("1.77686"))]
claim_df = {"e": mp.mpf("0.017434662642"), "mu": mp.mpf("0.009178441295"),
            "tau": mp.mpf("0.004809588624")}
claim_red = {"e": mp.mpf("2.3891764"), "mu": mp.mpf("1.2577769"), "tau": mp.mpf("0.6590868")}


def H_closed(q):
    """r321-C01 闭式：H(q)=(2/π)[(4+q²)/(6q²) − 4/9 + (q²−2)√(4+q²)asinh(q/2)/(3q³)]"""
    q2 = q * q
    return (mp.mpf(2) / mp.pi) * ((4 + q2) / (6 * q2) - mp.mpf(4) / 9
                                  + (q2 - 2) * mp.sqrt(4 + q2) * mp.asinh(q / 2) / (3 * q ** 3))


tot_df = mp.mpf(0)
tot_red = mp.mpf(0)
max_cf = mp.mpf(0)
rel_diffs = []
for name, m in fermions:
    q = Q / m
    I = mp.quad(lambda x: x * (1 - x) * mp.log(1 + q * q * x * (1 - x)), [0, 1])
    df = (2 * alpha0 / mp.pi) * I
    red = df / alpha0
    cf = alpha0 * H_closed(q)
    max_cf = max(max_cf, abs(df - cf) / df)
    rel_diffs.append(float(rel(df, claim_df[name])))
    tot_df += df
    tot_red += red
    log("  %-3s q=%.6e  Δ_f=%s" % (name, float(q), mp.nstr(df, 30)))
    log("       来料 Δ_f=%s  相对差=%.2e ；Δ_f/α=%s（来料 %s，相对差 %.2e）"
        % (mp.nstr(claim_df[name], 12), float(rel(df, claim_df[name])),
           mp.nstr(red, 20), mp.nstr(claim_red[name], 10), float(rel(red, claim_red[name]))))
log("  合计 Δ=%s （来料 0.031422692560，相对差 %.2e）"
    % (mp.nstr(tot_df, 30), float(rel(tot_df, mp.mpf("0.031422692560")))))
log("  合计 Δ/α=%s （来料 4.3060401，相对差 %.2e）"
    % (mp.nstr(tot_red, 20), float(rel(tot_red, mp.mpf("4.3060401")))))
guard("LEPTON_VALUES_MATCH", max(rel_diffs) < 1e-6,
      "三个 Δ_f 与来料 12 位印刷值一致（最大相对差 %.2e）" % max(rel_diffs))
guard("LEPTON_CLOSED_FORM_75DIGIT", float(max_cf) < 1e-60,
      "85 位求积 vs r321 闭式最大相对差 %.2e ⇒ 75 位精度可复现" % float(max_cf))

alpha_inv_lept = mp.mpf("137.035999177") - tot_red
log("  α⁻¹_leptons-only(-M_Z²) = %s （来料 132.7299591052，相对差 %.2e）"
    % (mp.nstr(alpha_inv_lept, 30), float(rel(alpha_inv_lept, mp.mpf("132.7299591052")))))
guard("ALPHA_INV_LEPTONS_MATCH", float(rel(alpha_inv_lept, mp.mpf("132.7299591052"))) < 1e-9,
      "与来料 10 位一致")

# ---------------------------------------------------------------------------
# 4. 权威门禁复验（单一真相源）
# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§4 _audit_acceptance.discriminate 复验")
log("=" * 78)
sys.path.insert(0, BASE)
from _audit_acceptance import discriminate  # noqa: E402

cand = 1.0 / 137.035999177
sig = cand * 1.532e-10
g_route = discriminate("V22_RG_ROUTE", candidate=cand, center=cand, sigma=sig,
                       n_matched=1, n_free=2, is_fit_to_target=True,
                       predicts_target_quantity=True)
log("  V22 RG 路线: surplus=%.2f verdict=%s" % (g_route["surplus"], g_route["verdict"]))
guard("GATE_ROUTE_RELATION_OR_FIT", g_route["verdict"] == "RELATION_OR_FIT",
      "n_free=2 ⇒ surplus=%.1f<1" % g_route["surplus"])

g_pos = discriminate("POSCTRL_GR", candidate=42.981, center=42.98, sigma=0.02,
                     n_matched=1, n_free=0, is_fit_to_target=False,
                     predicts_target_quantity=True)
log("  正对照 GR: surplus=%.2f verdict=%s" % (g_pos["surplus"], g_pos["verdict"]))
guard("GATE_POSCTRL_DISCOVERY", g_pos["is_discovery_of_target"],
      "门禁能给出发现级判词（非恒否）")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
npass = sum(1 for _, ok, _ in GUARDS if ok)
log("守卫 %d/%d 通过" % (npass, len(GUARDS)))
log("=" * 78)
for name, ok, detail in GUARDS:
    if not ok:
        log("FAIL: %s %s" % (name, detail))

with io.open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(LINES) + "\n")
print("\n日志已写入: %s" % OUT)
sys.exit(0 if npass == len(GUARDS) else 1)
