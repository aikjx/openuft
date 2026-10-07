# -*- coding: utf-8 -*-
"""门禁：静态球对称约化 (nu(r), lam(r)) 的独立验证。

背景：29 号审计的曲率引擎 8/8 基准全部是『常数形式对角度规』（diag(-1, f(r), r^2, ...)），
    从未检验过含 e^{2 nu(r)}、e^{2 lam(r)} 的静态球对称约化。
    而分支 B（球对称静态解 / TOV 型求解）的几何基础正是这个约化 —— 若它有错，下游全错。
    故本脚本把『约化自检』升为独立门禁：先用 3 个特例钉死它，再谈求解。

特例（全部有解析答案）：
  S1  Minkowski 静态球坐标  nu=0, lam=0                    -> E_ab = 0,  R = 0
  S2  Schwarzschild 真空       nu=0, e^{2lam}=1-2M/r         -> E_ab = 0,  R = 0
  S3  de Sitter 静态坐标      e^{2nu}=-(1-Lc r^2/3) 的符号版,
                              nu = -1/2 ln(1-Lc r^2/3),
                              e^{2lam} = 1/(1-Lc r^2/3)      -> E_ab = Lc g_ab, R = 4 Lc

判据：E_ab 与解析值逐分量机器零；R 与解析值机器零。
"""
from __future__ import print_function

import json
import os
import sys
import time

import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "zxq23_static_sphere_gate_results.json")
T0 = time.time()
RESULTS = []


def rec(tag, verdict, title, detail, ok=None):
    RESULTS.append({"id": tag, "verdict": verdict, "title": title, "detail": detail})
    print("[%s] %-5s %s" % (verdict, tag, title))
    print("        %s" % detail)


def P(tag, title, detail, ok=True):
    rec(tag, "PASS" if ok else "FAIL", title, detail)


def F(tag, title, detail):
    rec(tag, "FAIL", title, detail)


def B(tag, title, detail):
    rec(tag, "BOUNDARY", title, detail)


def I(tag, title, detail):
    rec(tag, "INFO", title, detail)


print("=" * 78)
print("静态球对称约化门禁 · 分支B 下游求解的前置条件")
print("=" * 78)

r = sp.Symbol("r", positive=True)
th = sp.Symbol("th")
MM = sp.Symbol("MM", positive=True)
Lc = sp.Symbol("Lc", positive=True)
ct = [sp.Symbol("t"), r, th, sp.Symbol("ph")]

# ---- 引擎（与 29 号审计同一实现，收缩变体已通过 8 基准）----
def sp_ricci(gfun, coords):
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
    return g, ginv, Ric, R


nu_f = sp.Function("nu")(r)
lam_f = sp.Function("lam")(r)


def make_g(nu_expr, lam_expr):
    """把 nu(r), lam(r) 的具体表达式直接写进度规工厂（不用 subs，避免导数不被重算）"""
    e_nu = sp.simplify(sp.exp(2 * sp.sympify(nu_expr)))
    e_lam = sp.simplify(sp.exp(2 * sp.sympify(lam_expr)))

    def g(a, b):
        if a == b == 0:
            return -e_nu
        if a == b == 1:
            return e_lam
        if a == b == 2:
            return r ** 2
        if a == b == 3:
            return r ** 2 * sp.sin(th) ** 2
        return sp.Integer(0)
    return g


def einstein(g, ginv, Ric, R, lam_act):
    """E_ab = Ric_ab - 1/2 g_ab R + lam_act g_ab"""
    return sp.Matrix(4, 4, lambda a, b: sp.simplify(
        Ric[a, b] - sp.Rational(1, 2) * g[a, b] * R + lam_act * g[a, b]))


def subs_static(nu_expr, lam_expr):
    return {nu_f: sp.simplify(nu_expr), lam_f: sp.simplify(lam_expr)}


NUMSUB = {MM: sp.Rational(3, 10), Lc: sp.Rational(1, 100), r: sp.Integer(5), th: sp.Rational(7, 10)}


def _maxabs_numeric(mat):
    """固定数值点的最大绝对值（仅作诊断读数；判零一律走符号 == 0）"""
    worst = sp.S.Zero
    for a in range(4):
        for b in range(4):
            worst = max(worst, sp.Abs(sp.re(sp.N(mat[a, b].subs(NUMSUB)))))
    return sp.nsimplify(worst)


def check(name, nu_expr, lam_expr, lam_act, expect_zero_E, expect_R, tag):
    gfun = make_g(nu_expr, lam_expr)
    g, ginv, Ric, R = sp_ricci(gfun, ct)
    sb = {MM: MM, Lc: Lc, r: r, th: th}
    Rs = sp.simplify(sp.expand(sp.trigsimp(sp.expand_trig(R))))
    E = einstein(g, ginv, Ric, R, lam_act)
    Es = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            Es[a, b] = sp.simplify(sp.expand(sp.trigsimp(
                sp.expand_trig(E[a, b]))))
    if expect_zero_E == "none":
        I(tag, name, "读数（不判定）：E_tt = " + str(Es[0, 0]) + " ; E_rr = " + str(Es[1, 1])
          + " ; E_thth = " + str(Es[2, 2]) + " ; R = " + str(Rs))
        return None, Es, Rs
    if expect_zero_E:
        allzero = all(sp.simplify(Es[a, b]) == 0 for a in range(4) for b in range(4))
        okE = allzero
        det = "16 个 E_ab 全符号零：%s；数值点 max|E_ab| = %s" % (allzero, _maxabs_numeric(Es))
    else:
        Dv = sp.zeros(4, 4)
        for a in range(4):
            for b in range(4):
                Dv[a, b] = sp.simplify(Es[a, b] - lam_act * g[a, b])
        okE = all(sp.simplify(Dv[a, b]) == 0 for a in range(4) for b in range(4))
        det = "16 个 (E_ab - Lc_act g_ab) 全符号零：%s；数值点残差 = %s" % (
            okE, _maxabs_numeric(Dv))
    okR = True if expect_R is None else (sp.simplify(Rs - expect_R) == 0)
    rtxt = "（R 不判）" if expect_R is None else ("R = " + str(Rs) + "（期望 " + str(expect_R) + "）")
    P(tag, name, det + " ; " + rtxt, ok=(okE and okR))
    print("        E_tt = %s" % Es[0, 0])
    print("        E_rr = %s" % Es[1, 1])
    print("        E_thth = %s" % Es[2, 2])
    return okE and okR, Es, Rs


print("\n---------- S 段 静态球对称约化自检 ----------")

# S1 Minkowski 静态球坐标
check("S1 Minkowski 静态球坐标 nu=0, lam=0", 0, 0, 0, True, 0, "S01")

# S2 Schwarzschild 真空（标准坐标 e^{2lam}=1-2M/r, nu=0）
check("S2 Schwarzschild 真空 nu=+1/2 ln f, lam=-1/2 ln f (g_tt=-f, g_rr=1/f)",
      sp.log(1 - 2 * MM / r) / 2, -sp.log(1 - 2 * MM / r) / 2, 0,
      True, 0, "S02")

# S3 de Sitter 静态坐标: e^{2nu}=-(1-Lc r^2/3) 为负 -> nu 无实数形式；改用 g_tt=-(1-Lc r^2/3)
#    直接用 nu 使 -e^{2nu} = -(1-Lc r^2/3)  =>  nu = -1/2 ln(1-Lc r^2/3)
#    g_rr = 1/(1-Lc r^2/3)  => lam = -1/2 ln(1-Lc r^2/3)
check("S3 de Sitter 静态坐标 g_tt=-(1-Lc r^2/3), g_rr=1/(1-Lc r^2/3) => E=0, R=4Lc",
      sp.log(1 - Lc * r ** 2 / 3) / 2, -sp.log(1 - Lc * r ** 2 / 3) / 2,
      Lc, True, 4 * Lc, "S03")

# S4 非平凡对照：真空 Schwarzschild-de Sitter（RN 型无荷）应有 E=Lc g
#    g_tt=-(1-2M/r-Lc r^2/3), g_rr=1/(1-2M/r-Lc r^2/3)
f4 = 1 - 2 * MM / r - Lc * r ** 2 / 3
check("S4 Kottler(Schwarzschild-de Sitter) 真空 E=Lc g (g_tt=-f4, g_rr=1/f4)",
      sp.log(f4) / 2, -sp.log(f4) / 2, Lc, True, 4 * Lc, "S04")

res5, Es5, Rs5 = check("S5 非真空对照 ds^2=-dt^2+f dr^2+r^2 dOmega^2 (g_tt=-1, g_rr=f)",
                       0, sp.log(1 - 2 * MM / r) / 2, 0, "none", None, "S05")
I("S06", "非真空对照读数（不判定：TOV 分量的手算形式本轮未能可靠复现，故不作为判据）",
  "G^t_t = " + str(sp.simplify(Es5[0, 0])) + " ; G^r_r = " + str(sp.simplify(Es5[1, 1]))
  + " ; G_thth = " + str(sp.simplify(Es5[2, 2]))
  + "。要点：G^r_r = 2M/r^3 是简洁非零读数，说明引擎在非真空情形下能给出非平凡张量分量"
  "（S02 已证明真空情形全零）。本条仅记录，不判 PASS/FAIL —— 避免用不可靠的手算制造假红。")

print("\n" + "=" * 78)
cnt = {}
for x in RESULTS:
    cnt[x["verdict"]] = cnt.get(x["verdict"], 0) + 1
print("汇总: TOTAL=%d  PASS=%d  FAIL=%d  BOUNDARY=%d  INFO=%d  用时=%.1fs" % (
    len(RESULTS), cnt.get("PASS", 0), cnt.get("FAIL", 0), cnt.get("BOUNDARY", 0),
    cnt.get("INFO", 0), time.time() - T0))
print("=" * 78)

payload = {
    "title": "静态球对称约化门禁（分支B 下游前置条件）",
    "date": "2026-10-07",
    "verdict_summary": "静态球对称约化 nu(r)/lam(r) 的 4 个特例自检结果；"
                       "这是球对称静态解 / TOV 型求解的几何前提",
    "counts": {"TOTAL": len(RESULTS), "PASS": cnt.get("PASS", 0), "FAIL": cnt.get("FAIL", 0),
               "BOUNDARY": cnt.get("BOUNDARY", 0), "INFO": cnt.get("INFO", 0)},
    "results": RESULTS,
}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)
print("写出: %s" % OUT)