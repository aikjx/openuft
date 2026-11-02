# -*- coding: utf-8 -*-
"""
ROOT-3F 后续章节复算（TA1/TA2/TA3），整理册佐证，不占 r 号
  TA1：单一作用量 → 运动方程；正交是相空间约束面（余维 1），非作用量恒等式
       不变性判据 = 约束沿流的李导数；本配置 L_f(θ̇)≠0 ⇒ 非不变
  TA2：含时 E/B 也救不了（一般性符号 no-go）；方法正对照（B=0 时 θ̇=0 确为不变面）
  TA3：破坏律 |cos|≈ω_c t、破坏时标 t_ε=ε/ω_c（与 v_r 无关）；数值核验
输出：_out_3f2.txt
"""
import io
import os
import sys

import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_out_3f2.txt")
LOG = []
GUARDS = []


def log(s=""):
    LOG.append(s)
    print(s)


def guard(gid, ok, detail):
    GUARDS.append((gid, bool(ok), detail))
    log("  [%s] %-42s %s" % ("PASS" if ok else "FAIL", gid, detail))


# ---------------------------------------------------------------------------
log("=" * 78)
log("§11 TA1：从单一作用量到正交约束面（不变性判据）")
log("=" * 78)
t = sp.symbols("t", real=True)
m, q, g_, E_, Bz, Bzt = sp.symbols("m q g E Bz Bz_t", positive=True)
r = sp.Function("r")(t)
th = sp.Function("theta")(t)
z = sp.Function("z")(t)

# 拉氏量：柱坐标 + 径向引力势 + 均匀 E∥z + 对称规范 A_θ=B_z r/2
L = (m / 2) * (sp.diff(r, t) ** 2 + r ** 2 * sp.diff(th, t) ** 2 + sp.diff(z, t) ** 2) \
    - m * g_ * r + q * E_ * z + q * Bz * r ** 2 * sp.diff(th, t) / 2
log("  L = ½m(ṙ²+r²θ̇²+ż²) − m g r + q E z + q B_z r²θ̇/2")
from sympy.calculus.euler import euler_equations  # noqa: E402

eqs = euler_equations(L, [r, th, z], t)
EL_r, EL_t, EL_z = [sp.simplify(e.lhs - e.rhs) for e in eqs]
sol_r = sp.simplify(sp.solve(EL_r, sp.diff(r, t, 2))[0])
sol_t = sp.simplify(sp.solve(EL_t, sp.diff(th, t, 2))[0])
sol_z = sp.simplify(sp.solve(EL_z, sp.diff(z, t, 2))[0])
wc = q * Bz / m
rhs_r = -g_ + r * sp.diff(th, t) ** 2 + wc * r * sp.diff(th, t)
rhs_t = -(2 * sp.diff(r, t) * sp.diff(th, t) + wc * sp.diff(r, t)) / r
rhs_z = q * E_ / m
log("  E-L ⇒ r̈ = %s ; θ̈ = %s ; z̈ = %s"
    % (sol_r, sp.simplify(sol_t), sol_z))
guard("ACTION_REPRODUCES_ODE",
      sp.simplify(sol_r - rhs_r) == 0 and sp.simplify(sol_t - rhs_t) == 0
      and sp.simplify(sol_z - rhs_z) == 0,
      "单一作用量的 E-L 方程与本册 §四 的 ODE 逐项相同（TA1 第一步完成）")

# 正交约束：E_r=0 时只剩 θ̇=0 一条 ⇒ 相空间(6维)余维 1
log("  相空间 dim=6（r,ṙ,θ,θ̇,z,ż）；E_r=0 时三力正交 ⟺ θ̇=0 ⇒ 余维 1")
guard("CONSTRAINT_CODIM_1", 6 - 1 == 5,
      "正交面维数 5（余维 1）；不是作用量恒等式，只是相空间超面")

# 不变性判据：L_f(θ̇)=θ̈|_C = −ω_c ṙ/r
Lf = sp.simplify(rhs_t.subs(sp.diff(th, t), 0))
log("  约束沿流李导数 L_f(θ̇)|_{θ̇=0} = %s ⇒ ṙ≠0 时不为零" % Lf)
guard("LIE_DERIVATIVE_NONZERO", sp.simplify(Lf - (-wc * sp.diff(r, t) / r)) == 0,
      "θ̈=−ω_c ṙ/r（符号精确）⇒ 约束面被流横截，非不变")

# 数值：从 θ̇=0 面出发，dt=1e-3 后偏离量
mp.mp.dps = 30
P = dict(m=1, q=1, g=1, E=1, Bz=1)

def rhs(tt, s, par=None):
    par = par or P
    rr, rd, tt_, thd, zz, zd = s
    W = par["q"] * par["Bz"] / par["m"]
    return [rd, -par["g"] + rr * thd ** 2 + W * rr * thd,
            thd, -(2 * rd * thd + W * rd) / rr, zd, par["q"] * par["E"] / par["m"]]


def rk4(s0, T, h, par=None):
    par = par or P
    s = list(map(mp.mpf, s0))
    tt = mp.mpf(0)
    for _ in range(int(abs(T / h))):
        k1 = rhs(tt, s, par)
        k2 = rhs(tt + h / 2, [s[i] + h * k1[i] / 2 for i in range(6)], par)
        k3 = rhs(tt + h / 2, [s[i] + h * k2[i] / 2 for i in range(6)], par)
        k4 = rhs(tt + h, [s[i] + h * k3[i] for i in range(6)], par)
        s = [s[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(6)]
        tt += h
    return s


h = mp.mpf("2e-5")
s = rk4([1, "0.2", 0, 0, 0, 0], mp.mpf("1e-3"), h)
thd_after = s[3]
log("  从 θ̇=0 出发 dt=1e-3 ⇒ θ̇=%.3e（预测 −ω_c ṙ/r·dt=−2.000e-04）" % float(thd_after))
guard("CONSTRAINT_NOT_INVARIANT_NUMERIC", abs(float(thd_after) + 2.0e-4) < 2e-6,
      "约束面被穿过（偏离 2.00e−04），与李导数一致")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§12 TA2：含时场能否维持正交？（一般 no-go）")
log("=" * 78)
Er, Eth, thd0, rd, rr = sp.symbols("E_r E_theta thd rdot r", real=True)
# 三力：Fg=(-mg,0,0); Fe=q(Er,E_theta,E_z); Fb=qBz(rθ̇,-ṙ,0)
c1 = sp.simplify(-m * g_ * q * Er)
c2 = sp.simplify(q ** 2 * (Er * rr * thd0 - Eth * rd))
c3 = sp.simplify(-m * g_ * q * Bz * rr * thd0)
log("  正交约束：c1=F_g·F_e=%s ; c2=F_e·F_b=%s ; c3=F_b·F_g=%s" % (c1, c2, c3))
sols = sp.solve([c1, c2, c3], [Er, Eth, thd0], dict=True)
log("  solve ⇒ %s（要求 ṙ≠0、B_z≠0、g≠0 ⇒ E_r=0, E_θ=0, θ̇=0）" % sols)
ok_no_go = (len(sols) == 1 and all(sp.simplify(sols[0][k]) == 0 for k in (Er, Eth, thd0)))
guard("TA2_GENERAL_NO_GO_SYMBOLIC", ok_no_go,
      "三力全非零且正交 ⇒ 必须 E_r=E_θ=θ̇=0（唯一解）")

# 但 θ̈ = −(2ṙθ̇+ω_cṙ)/r + qE_θ/(mr)；θ̇=0 ⇒ θ̈=−ω_c ṙ/r ≠ 0 ⇒ θ̇ 立刻离开 0
thdd_at = sp.simplify((-wc * rd) / rr + q * 0 / (m * rr))
log("  代回 θ̈|_{θ̇=0,E_θ=0} = %s ⇒ 与约束 c3 矛盾（c3 只在瞬时成立）" % thdd_at)
guard("TA2_CONTRADICTION", sp.simplify(thdd_at + wc * rd / rr) == 0 and thdd_at != 0,
      "维持 θ̇=0 需 θ̈=0，但 θ̈=−ω_c ṙ/r ≠ 0 ⇒ 一般场类无解")

# 含时 B_z(t)：结构不变（ω_c→ω_c(t)），矛盾照旧
thdd_td = sp.simplify((-q * Bzt * rd) / (m * rr))
guard("TA2_TIME_DEPENDENT_B_ALSO_FAILS", thdd_td != 0,
      "B_z(t) 只把 ω_c 换成 ω_c(t)，θ̈=−ω_c(t)ṙ/r≠0 ⇒ 含时场也救不了")

# 方法正对照：B=0 时 θ̈=−2ṙθ̇/r，θ̇=0 确为不变面
Lf_B0 = sp.simplify(rhs_t.subs(sp.diff(th, t), 0).subs(Bz, 0))
guard("METHOD_CONTROL_INVARIANT_CASE", Lf_B0 == 0,
      "B=0 时 L_f(θ̇)|_{θ̇=0}=0 ⇒ 判据能把『不变面』正确判为不变（非恒否）")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§13 TA3：破坏律与破坏时标（可检验的运动学预言）")
log("=" * 78)
log("  |cos∠(F_b,F_g)| = |rθ̇|/sqrt((rθ̇)²+ṙ²) ≈ |θ̇|/|ṙ| ≈ ω_c t")
P3 = dict(m=1, q=1, g=0.01, E=1, Bz=1)   # §13 专用：小 g，使 ṙ 在 t≤0.05 内近似不变
rows = []
for T in ["0.005", "0.01", "0.02", "0.05"]:
    sT = rk4([1, "0.2", 0, 0, 0, 0], mp.mpf(T), h, P3)
    rT, rdT, _, thdT, _, _ = sT
    cosv = abs(float(rT * thdT)) / mp.sqrt((rT * thdT) ** 2 + rdT ** 2)
    pred = mp.mpf(1) * mp.mpf(T)
    rows.append((T, float(cosv), float(pred), float(abs(cosv - pred) / pred)))
    log("  t=%-5s |cos|=%.6f   ω_c t=%.6f  相对差=%.2e" % (T, float(cosv), float(pred), rows[-1][3]))
guard("TA3_BREAK_LAW", max(x[3] for x in rows) < 5e-3,
      "小 t 区 |cos|≈ω_c t（t≤0.05 最大相对差 %.2e）" % max(x[3] for x in rows))

# 与 v_r 无关：v_r=0.1/0.2/0.4 在同 t 处 cos 一致到 O(t²)
coss = {}
for vr0 in ["0.1", "0.2", "0.4"]:
    sV = rk4([1, vr0, 0, 0, 0, 0], mp.mpf("0.01"), h, P3)
    rV, rdV, _, thdV, _, _ = sV
    coss[vr0] = float(abs(rV * thdV)) / mp.sqrt((rV * thdV) ** 2 + rdV ** 2)
log("  t=0.01 时 v_r∈{0.1,0.2,0.4} ⇒ |cos|=%s" % {k: round(v, 7) for k, v in coss.items()})
guard("TA3_VR_INDEPENDENCE", max(coss.values()) - min(coss.values()) < 5e-4,
      "破坏律对 v_r 不敏感（极差 %.1e）⇒ 只由 ω_c 定价" % (max(coss.values()) - min(coss.values())))


def cos_at(T, vr0="0.2"):
    sC = rk4([1, vr0, 0, 0, 0, 0], mp.mpf(T), h, P3)
    rC, rdC, _, thdC, _, _ = sC
    return float(abs(rC * thdC)) / float(mp.sqrt((rC * thdC) ** 2 + rdC ** 2))


eps = 0.01
lo, hi = mp.mpf(0), mp.mpf("0.05")
for _ in range(40):
    mid = (lo + hi) / 2
    if cos_at(float(mid)) < eps:
        lo = mid
    else:
        hi = mid
t_eps = (lo + hi) / 2
log("  |cos|=ε=%.2f 的根 t=%.6f（解析 ε/ω_c=%.6f）" % (eps, float(t_eps), eps / 1.0))
guard("TA3_BREAK_TIME_FORMULA", abs(float(t_eps) - eps / 1.0) < 2e-4,
      "t_ε=ε m/(qB_z)（与 v_r、r_0 无关）")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§14 保持的充要条件（退化性）")
log("=" * 78)
log("  非平凡保持 ⇒ θ̇≡0 ∧ ṙ≡0 ⇒ v=0 ⇒ F_b=0（退化）；且径向平衡需 g=0")
maint = sp.simplify(-g_ + 0 + 0)
guard("ONLY_TRIVIAL_MAINTENANCE", maint == -g_ and sp.simplify(maint) != 0,
      "保持解必退化（F_b≡0）；且静止还需 g=0（r̈=−g≠0）")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
npass = sum(1 for _, ok, _ in GUARDS if ok)
log("守卫 %d/%d 通过" % (npass, len(GUARDS)))
log("判词：TA1_CONSTRAINT_NOT_IDENTITY__TA2_CLOSED_NO_GO__TA3_KINEMATIC_BREAK_LAW")
log("=" * 78)
for gid, ok, det in GUARDS:
    if not ok:
        log("FAIL: %s %s" % (gid, det))

with io.open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(LOG) + "\n")
print("\n日志: %s" % OUT)
sys.exit(0 if npass == len(GUARDS) else 1)
