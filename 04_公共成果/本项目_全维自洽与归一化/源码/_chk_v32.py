# -*- coding: utf-8 -*-
"""ROOT V32 三力垂直原理：独立复算（不重跑来料引擎）。
判据：常量/闭式/SymPy 回代/相对论积分/随机正交/漂移反例；以及表格与交叉项的可复现性。
产物：同目录 _out_v32.txt
"""
import io
import os
import random

import mpmath as mp
import sympy as sp

mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
BUF = []


def say(s=""):
    BUF.append(s)
    print(s)


GUARD = {"pass": 0, "fail": 0}


def guard(name, ok, note):
    GUARD["pass" if ok else "fail"] += 1
    say("[%s] %-38s %s" % ("PASS" if ok else "FAIL", name, note))


# ---------------- CODATA 2022 ----------------
e = mp.mpf('1.602176634e-19')
me = mp.mpf('9.1093837015e-31')
c = mp.mpf('2.99792458e8')
g = mp.mpf('9.81')
E = mp.mpf('1e5')
B = mp.mpf('0.5')
v0 = mp.mpf('1e6')

Fg = me * g
Fe = e * E
Fb = e * v0 * B
Om = e * B / me
T = 2 * mp.pi / Om
gam = 1 / mp.sqrt(1 - (v0 / c) ** 2)
kap = mp.sqrt(Fg ** 2 + Fb ** 2) / (me * gam * v0 ** 2)
ndmin = mp.sqrt(Fg ** 2 + Fb ** 2) / (me * gam * v0)

say("== A. 常量与闭式 ==")
say("Fg=%.6e N  Fe=%.6e N  Fb=%.6e N" % (Fg, Fe, Fb))
say("Omega=%.8e s^-1  T=%.4f ps  gamma0=%.10f" % (Om, T / 1e-12, gam))
say("kappa0=%.8e m^-1  |ndot|min=%.8e s^-1" % (kap, ndmin))
guard("Fg", abs(Fg - mp.mpf('8.936e-30')) / Fg < 1e-3, "claim 8.936e-30")
guard("Fe", abs(Fe - mp.mpf('1.602e-14')) / Fe < 1e-3, "claim 1.602e-14")
guard("Fb", abs(Fb - mp.mpf('8.011e-14')) / Fb < 1e-3, "claim 8.011e-14")
guard("T_cyclotron", abs(T / 1e-12 - mp.mpf('71.448')) / 71.448 < 1e-4, "claim 71.448 ps")
guard("gamma0", abs(gam - mp.mpf('1.0000055633')) < 1e-9, "claim 1.0000055633")
guard("kappa0", abs(kap - mp.mpf('8.7940511e4')) / kap < 1e-6, "claim 8.7940511e4")
guard("ndot_min", abs(ndmin - mp.mpf('8.79405e10')) / ndmin < 1e-5, "claim 8.79405e10")

# ---------------- B. 非相对论闭式与表格 ----------------
say()
say("== B. 运动解与「偏离直角」表 ==")


def v_yz(t):
    a = Om * t
    return (v0 * mp.cos(a) + (E / B) * mp.sin(a),
            -v0 * mp.sin(a) + (E / B) * (mp.cos(a) - 1))


claim = [('0', '0'), ('0.2', '1.0095'), ('1', '5.0837'),
         ('5', '26.3845'), ('10', '55.2836'), ('20', '62.7684')]
say(" t(ps) | 精确几何角 | arcsin(|vz|/v0) | 来料")
rows = []
for ts, cs in claim:
    vy, vz = v_yz(mp.mpf(ts) * 1e-12)
    exact = abs(mp.acos(vz / mp.sqrt(vy ** 2 + vz ** 2)) * 180 / mp.pi - 90)
    arc = mp.asin(min(abs(vz) / v0, 1)) * 180 / mp.pi
    rows.append((ts, exact, arc, mp.mpf(cs)))
    say(" %5s | %9.4f | %13.4f | %7s" % (ts, exact, arc, cs))

ok4 = all(abs(r[2] - r[3]) < mp.mpf('0.05') for r in rows[:4])
guard("table_first4_vs_arcsin", ok4, "前4行与 arcsin(|vz|/v0) 一致（<0.05deg）")
last2 = all(abs(r[1] - r[3]) > mp.mpf('1') and abs(r[2] - r[3]) > mp.mpf('1') for r in rows[4:])
guard("table_last2_inconsistent", last2,
      "10/20ps 与两种归一化均不符（精确 %.2f/%.2f，弧弦 %.2f/%.2f）"
      % (rows[4][1], rows[5][1], rows[4][2], rows[5][2]))

# ---------------- C. 交叉项 ----------------
say()
say("== C. 交叉项占比（10 ps）==")
vy, vz = v_yz(mp.mpf('10') * 1e-12)
Fbv = e * B * mp.sqrt(vy ** 2 + vz ** 2)
S = Fg ** 2 + Fe ** 2 + Fbv ** 2
CR = e ** 2 * E * B * vz
r_sum = abs(2 * CR) / S
r_tot = abs(2 * CR) / (S + 2 * CR)
say("2|cross|/SumF2=%.4f%%  2|cross|/|Ftot|2=%.4f%%  来料 36.69%%"
    % (r_sum * 100, r_tot * 100))
guard("cross_ratio", abs(max(r_sum, r_tot) * 100 - mp.mpf('36.69')) > mp.mpf('2'),
      "两种口径均无 36.69%%（差 %.2f / %.2f 个百分点）"
      % (36.69 - r_sum * 100, 36.69 - r_tot * 100))

# ---------------- D. SymPy 回代 ----------------
say()
say("== D. SymPy 严格回代 ==")
t, v0s, Es, Bs, gs, Os = sp.symbols('t v0 E B g Omega', positive=True)
vy_s = v0s * sp.cos(Os * t) + (Es / Bs) * sp.sin(Os * t)
vz_s = -v0s * sp.sin(Os * t) + (Es / Bs) * (sp.cos(Os * t) - 1)
vx_s = gs * t
r1 = sp.simplify(sp.diff(vy_s, t) - (Os * (Es / Bs) + Os * vz_s))
r2 = sp.simplify(sp.diff(vz_s, t) + Os * vy_s)
r3 = sp.simplify(sp.diff(vx_s, t) - gs)
say("res_y=%s  res_z=%s  res_x=%s" % (r1, r2, r3))
guard("sympy_backsub", r1 == 0 and r2 == 0 and r3 == 0, "三式符号精确为零")

# ---------------- E. 相对论积分 vs 非相对论 ----------------
say()
say("== E. 相对论动量方程 vs 非相对论轨道 ==")
beta = v0 / c
ey = E / (B * v0)


def f(tau, Y):
    uy, uz = Y[0], Y[1]
    gm = 1 / mp.sqrt(1 - beta ** 2 * (uy ** 2 + uz ** 2))
    dgm = gm ** 3 * beta ** 2 * (uy * (ey + uz) + uz * (-uy))
    return [(ey + uz - uy * dgm) / gm, (-uy - uz * dgm) / gm]


sol = mp.odefun(f, 0, [1, 0], tol=mp.mpf('1e-28'))
mx = mp.mpf(0)
for i in range(41):
    tau = mp.mpf(i) / 20
    uy_r, uz_r = sol(tau)
    uy_n = mp.cos(tau) + ey * mp.sin(tau)
    uz_n = -mp.sin(tau) + ey * (mp.cos(tau) - 1)
    cosang = (uy_r * uy_n + uz_r * uz_n) / (
        mp.sqrt(uy_r ** 2 + uz_r ** 2) * mp.sqrt(uy_n ** 2 + uz_n ** 2))
    mx = max(mx, mp.acos(min(cosang, 1)))
say("max |angle_rel - angle_nonrel| = %.6f deg ；来料 0.00328 deg" % (mx * 180 / mp.pi))
guard("rel_vs_nonrel_order", mx * 180 / mp.pi < mp.mpf('0.01'), "同量级（差 %.1f 倍）"
      % (0.00328 / (float(mx * 180 / mp.pi) or 1e-30)))

# ---------------- F. 5000 组随机正交 ----------------
say()
say("== F. V32-1 充分性：5000 组随机配置 ==")
random.seed(20261102)
bad = 0
N = 5000
for _ in range(N):
    gv = [mp.mpf(random.uniform(-1, 1)) for _ in range(3)]
    Ev = [mp.mpf(random.uniform(-1, 1)) for _ in range(3)]
    g2 = sum(x * x for x in gv)
    Ev = [Ev[i] - sum(gv[k] * Ev[k] for k in range(3)) * gv[i] / g2 for i in range(3)]
    n = [gv[1] * Ev[2] - gv[2] * Ev[1], gv[2] * Ev[0] - gv[0] * Ev[2], gv[0] * Ev[1] - gv[1] * Ev[0]]
    vv = [mp.mpf(random.uniform(-1, 1)) for _ in range(3)]
    dotn = sum(vv[i] * n[i] for i in range(3))
    vv = [vv[i] - dotn * n[i] / sum(x * x for x in n) for i in range(3)]
    Bv = [mp.mpf(random.uniform(-1, 1)) for _ in range(3)]
    dotnB = sum(Bv[i] * n[i] for i in range(3))
    Bv = [Bv[i] - dotnB * n[i] / sum(x * x for x in n) for i in range(3)]
    w = [vv[1] * Bv[2] - vv[2] * Bv[1], vv[2] * Bv[0] - vv[0] * Bv[2], vv[0] * Bv[1] - vv[1] * Bv[0]]
    if sum(x * x for x in w) < mp.mpf('1e-18'):
        continue
    d1 = sum(gv[i] * Ev[i] for i in range(3))
    d2 = sum(Ev[i] * w[i] for i in range(3))
    d3 = sum(w[i] * gv[i] for i in range(3))
    if max(abs(d1), abs(d2), abs(d3)) > mp.mpf('1e-18'):
        bad += 1
say("违例 = %d / %d" % (bad, N))
guard("random_orth_5000", bad == 0, "V32-1 充分性无违例")

# ---------------- G. 漂移反例 ----------------
say()
say("== G. 漂移反例 v_d x B = -E ==")
Ed = [mp.mpf(0), mp.mpf(1), mp.mpf(0)]
Bd = [mp.mpf(0), mp.mpf(0), mp.mpf(1)]
vd = [(Ed[1] * Bd[2] - Ed[2] * Bd[1]), (Ed[2] * Bd[0] - Ed[0] * Bd[2]), (Ed[0] * Bd[1] - Ed[1] * Bd[0])]
B2 = sum(x * x for x in Bd)
vd = [x / B2 for x in vd]
w2 = [vd[1] * Bd[2] - vd[2] * Bd[1], vd[2] * Bd[0] - vd[0] * Bd[2], vd[0] * Bd[1] - vd[1] * Bd[0]]
say("v_d x B = %s ; -E = %s" % (w2, [-x for x in Ed]))
guard("drift_identity", all(abs(w2[i] + Ed[i]) < mp.mpf('1e-30') for i in range(3)), "恒等成立")

# ---------------- H. V32-M 在静态 g,E 下为空条件 ----------------
say()
say("== H. V32-M：静态 g,E 时 n 被钉死 ==")
s = sp.symbols('t')
gg = sp.Matrix([1, 0, 0])
EE = sp.Matrix([0, 1, 0])
nn = gg.cross(EE)
nn = nn / nn.norm()
say("n = g x E / |g x E| = %s （不显含 t）" % list(nn))
say("=> n_dot = 0 ；而 F_b·n = qB|v_yz| ≠ 0 => V32-M 在静态场实例中无解")
guard("V32M_static_vacuous", sp.diff(nn, s) == sp.zeros(3, 1), "ṅ≡0 与 F_b·n≠0 互斥")

say()
say("SUMMARY guard_pass=%d guard_fail=%d" % (GUARD["pass"], GUARD["fail"]))
with io.open(os.path.join(HERE, "_out_v32.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(BUF) + "\n")
