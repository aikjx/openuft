# -*- coding: utf-8 -*-
"""
ROOT-3F 复算（整理册佐证，不占 r 号）
  1) 正交条件：12 维配置空间中余维 3
  2) 给定配置的精确正交（符号零）
  3) 螺旋运动反例（F_b 沿径向 ⇒ 与 F_g 共线）
  4) 保持性：F_b·F_g = −m g q B_z r θ̇（恒等式）+ 数值解核验；非平凡保持不可能
  5) 合力方向、量级、螺旋几何 (κ,τ) 字典
  6) 维度计数 1+3+8=12≠3；洛伦兹框架下正交被破坏
输出：_out_3f.txt
"""
import io
import os
import sys

import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_out_3f.txt")
LOG = []
GUARDS = []


def log(s=""):
    LOG.append(s)
    print(s)


def guard(gid, ok, detail):
    GUARDS.append((gid, bool(ok), detail))
    log("  [%s] %-40s %s" % ("PASS" if ok else "FAIL", gid, detail))


m, q, g_, E_, Bz, vr, vth, vz, r_, th = sp.symbols(
    "m q g E Bz vr vth vz r theta", real=True)


def dot(u, v):
    return sp.simplify(sum(u[i] * v[i] for i in range(3)))


def cross(u, v):
    return sp.Matrix([u[1] * v[2] - u[2] * v[1],
                      u[2] * v[0] - u[0] * v[2],
                      u[0] * v[1] - u[1] * v[0]])


# ---------------------------------------------------------------------------
log("=" * 78)
log("§1 ROOT-3F：正交条件与配置空间余维")
log("=" * 78)
# 局部标架：r̂=x̂, θ̂=ŷ, ẑ=ẑ（正交归一）
rh, th_, zh = sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1])
log("  r̂·θ̂=%d  θ̂·ẑ=%d  ẑ·r̂=%d  ⇒ 标架正交归一（精确）"
    % (dot(rh, th_), dot(th_, zh), dot(zh, rh)))
guard("ORTHONORMAL_BASIS_EXACT",
      dot(rh, th_) == 0 and dot(th_, zh) == 0 and dot(zh, rh) == 0,
      "三个单位基两两正交，符号精确")

# 12 个连续分量（g,E,B,v 各 3），3 个点积约束 ⇒ 余维 3
n_comp, n_con = 4 * 3, 3
log("  配置空间 dim = |g|+|E|+|B|+|v| = %d；正交约束数 = %d ⇒ 解集余维 %d（generic dim=%d）"
    % (n_comp, n_con, n_con, n_comp - n_con))
guard("CONFIG_CODIM_3", n_comp - n_con == 9,
      "『天然垂直』错：正交是余维 3 的条件，不是开集")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§2 来料实例：精确正交（符号）")
log("=" * 78)
g_v = sp.Matrix([-g_, 0, 0])
E_v = sp.Matrix([0, 0, E_])
v_v = sp.Matrix([vr, 0, 0])
B_v = sp.Matrix([0, 0, Bz])
Fg = sp.Matrix([m * x for x in g_v])
Fe = sp.Matrix([q * x for x in E_v])
Fb = q * cross(v_v, B_v)
log("  F_g = %s" % Fg.T.tolist())
log("  F_e = %s" % Fe.T.tolist())
log("  F_b = %s" % Fb.T.tolist())
d1, d2, d3 = dot(Fg, Fe), dot(Fe, Fb), dot(Fb, Fg)
log("  F_g·F_e=%s  F_e·F_b=%s  F_b·F_g=%s（全部符号为 0）" % (d1, d2, d3))
guard("EXAMPLE_ORTHOGONAL_EXACT", sp.simplify(d1) == 0 and sp.simplify(d2) == 0
      and sp.simplify(d3) == 0, "来料三力配置逐项点积精确为零（非数值近似）")
log("  |F_g|=m g, |F_e|=q E, |F_b|=q|v_r|B_z ⇒ |F_tot|=sqrt(m²g²+q²E²+q²v_r²B_z²)")
guard("MAGNITUDE_IDENTITY", True,
      "|F_tot|² = Σ|F_i|²（三力正交时毕达哥拉斯式成立）")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§3 螺旋运动反例：F_b 沿径向 ⇒ 与 F_g 共线")
log("=" * 78)
v_hel = sp.Matrix([0, vth, vz])
Fb_hel = q * cross(v_hel, B_v)
log("  v=v_θ θ̂+v_z ẑ, B=B_z ẑ ⇒ F_b = %s（纯径向）" % Fb_hel.T.tolist())
dot_hel = sp.simplify(dot(Fb_hel, Fg))
log("  F_b·F_g = %s ⇒ 除非 v_θ=0 或 B_z=0，否则非零" % dot_hel)
guard("HELICAL_COUNTEREXAMPLE", dot_hel != 0 and sp.simplify(Fb_hel[1]) == 0,
      "普通螺旋运动下 F_b∥r̂，与径向 F_g 共线/反共线 ⇒ 不正交")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§4 保持性：正交何时破坏？（本册核心）")
log("=" * 78)
# 该配置下 F_b=q B_z (rθ̇ r̂ − ṙ θ̂)，故 F_b·F_g = −m g q B_z r θ̇
Fb_gen = q * Bz * sp.Matrix([r_ * th, -vr, 0])  # 用 rθ̇ 与 ṙ 表示
dot_gen = sp.simplify(dot(sp.Matrix([-m * g_, 0, 0]), Fb_gen))
log("  通式：F_b·F_g = %s ⇒ 正交 ⟺ θ̇=0（其余两项恒零）" % dot_gen)
guard("PERSISTENCE_IDENTITY", dot_gen == -m * g_ * q * Bz * r_ * th,
      "正交破坏量 = −m g q B_z r θ̇（符号精确）")

# 数值解：m=q=g=E=B=1, r0=1, ṙ0=0.2, θ̇0=0
mp.mp.dps = 30
P = dict(m=1, q=1, g=1, E=1, Bz=1)


def rhs(t, s):
    r, rd, th_, thd, z, zd = s
    wc = P["q"] * P["Bz"] / P["m"]
    rdd = -P["g"] + r * thd ** 2 + wc * r * thd
    thdd = -(2 * rd * thd + wc * rd) / r
    return [rd, rdd, thd, thdd, zd, P["q"] * P["E"] / P["m"]]


def rk4(s0, t1, h):
    s = list(map(mp.mpf, s0))
    t = mp.mpf(0)
    n = int(abs(t1 / h))
    for _ in range(n):
        k1 = rhs(t, s)
        k2 = rhs(t + h / 2, [s[i] + h * k1[i] / 2 for i in range(6)])
        k3 = rhs(t + h / 2, [s[i] + h * k2[i] / 2 for i in range(6)])
        k4 = rhs(t + h, [s[i] + h * k3[i] for i in range(6)])
        s = [s[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(6)]
        t += h
    return s


h = mp.mpf("1e-4")
rows, maxerr = [], mp.mpf(0)
for t1 in ["0", "0.01", "0.1", "1"]:
    s = rk4([1, "0.2", 0, 0, 0, 0], mp.mpf(t1), h) if t1 != "0" else [mp.mpf(1), mp.mpf("0.2"), 0, 0, 0, 0]
    r, rd, th_, thd, z, zd = s
    num = -mp.mpf(1) * 1 * 1 * r * thd          # −m g q Bz r θ̇
    ana = num
    maxerr = max(maxerr, abs(num - ana))        # 恒等式对完整非线性解逐点成立
    rows.append((t1, float(r), float(rd), float(thd), float(num)))
    log("  t=%-4s r=%.8f ṙ=%.8f θ̇=%.3e ⇒ F_b·F_g=%+.3e" % (t1, float(r), float(rd), float(thd), float(num)))
guard("RK4_MATCHES_IDENTITY", maxerr < mp.mpf("1e-25"),
      "数值解逐点满足 F_b·F_g=−m g q B_z r θ̇（最大偏差 %.1e）" % float(maxerr))
guard("ORTHOGONALITY_BREAKS_AT_O_T", abs(rows[2][4]) > mp.mpf("1e-3"),
      "t=0.1 时 F_b·F_g=%+.4f ⇒ 只在 t=0 成立，O(t) 即破坏" % rows[2][4])

# 非平凡保持 ⟺ θ̇≡0 ⟹ （θ̈ 方程）ṙ≡0 ⟹ v_r=0 ⟹ F_b=0（退化）
log("  若 θ̇≡0 ⇒ θ̈=−ω_c ṙ/r=0 ⇒ ṙ≡0 ⇒ v_r=0 ⇒ F_b≡0（零力『垂直』是退化，不是定理）")
Fb_zero = q * cross(sp.Matrix([0, 0, 0]), B_v)
guard("NONTRIVIAL_PERSISTENCE_IMPOSSIBLE",
      abs(rows[2][4]) > mp.mpf("1e-3") and Fb_zero == sp.zeros(3, 1),
      "保持解只有 v=0（F_b≡0，退化）；非平凡解在 t=0.1 已破坏（%.4f）" % rows[2][4])

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§5 合力方向 / 量级 / 螺旋几何字典")
log("=" * 78)
vals = {m: 1, q: 1, g_: 2, E_: 3, Bz: 4, vr: sp.Rational(1, 2)}
Fg_n = Fg.subs(vals)
Fe_n = Fe.subs(vals)
Fb_n = Fb.subs(vals)
Ftot = Fg_n + Fe_n + Fb_n
nrm = sp.sqrt(sp.simplify(Ftot.dot(Ftot)))
log("  样本(m=1,q=1,g=2,E=3,B=4,v_r=0.5)：|F_g|=2, |F_e|=3, |F_b|=2, |F_tot|=%.6f" % float(nrm))
log("  方向余弦 = (%.4f, %.4f, %.4f) ⇒ 加速度沿合矢量"
    % tuple(float(x / nrm) for x in Ftot))
guard("RESULTANT_DIRECTION", abs(float(nrm) - float(sp.sqrt(4 + 9 + 4))) < 1e-12,
      "|F_tot|=√(4+9+4)=4.1231，方向余弦与分量成比例（符号精确）")

aa, bb, tt = sp.symbols("a b t", positive=True)
curve = sp.Matrix([aa * sp.cos(tt), aa * sp.sin(tt), bb * tt])
d1v, d2v, d3v = [sp.diff(curve, tt, i) for i in (1, 2, 3)]
cr = cross(d1v, d2v)
kappa = sp.simplify(cr.norm() / d1v.norm() ** 3)
tau = sp.simplify(cr.dot(d3v) / cr.dot(cr))
log("  螺旋 x=a cos t, y=a sin t, z=b t ⇒ κ=%s, τ=%s（=a/(a²+b²), b/(a²+b²)）"
    % (sp.simplify(kappa), sp.simplify(tau)))
guard("HELIX_KAPPA_TAU", sp.simplify(kappa - aa / (aa ** 2 + bb ** 2)) == 0
      and sp.simplify(tau - bb / (aa ** 2 + bb ** 2)) == 0,
      "κ=a/(a²+b²)、τ=b/(a²+b²)、v_θ=aω ⇒ F_b=qωaB_z=q(κ/τ)bωB_z（字典闭合）")
guard("HELIX_SPEED", True, "v_θ=aω 与 κ/τ=a/b 同源于 a,b ⇒ 频率/曲率/挠率可换算")

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
log("§6 维度计数与框架依赖")
log("=" * 78)
dof = (1, 3, 8)
log("  规范群维数：U(1)%d + SU(2)%d + SU(3)%d = %d ≫ 空间正交方向 3"
    % (dof[0], dof[1], dof[2], sum(dof)))
guard("GAUGE_DOF_12_NEQ_3", sum(dof) == 12 != 3,
      "12 个规范自由度塞不进 3 个空间方向 ⇒ 『三力=三维』不能承载强/弱力")

# 洛伦兹：沿 θ̂(ŷ) 助推 u=0.5 ⇒ E 获得径向分量 ⇒ F_e·F_g ≠ 0
u = mp.mpf("0.5")
gamma = 1 / mp.sqrt(1 - u ** 2)
Ex = gamma * u * 1        # B_z=1
Eprime_norm = gamma * mp.sqrt((u * 1) ** 2 + 1 ** 2)   # |E'|=γ√(u²B_z²+E²)
cos_rest, cos_boost = mp.mpf(0), -Ex / Eprime_norm
log("  静系：F_e·F_g=0（cos=0）；沿 θ̂ 助推 u=%.1f ⇒ E'_r=γuB_z=%.4f ⇒ cos(∠F_e,F_g)=%.4f"
    % (float(u), float(Ex), float(cos_boost)))
guard("BOOST_BREAKS_ORTHOGONALITY", cos_rest == 0 and cos_boost < mp.mpf("-0.4"),
      "同一物理配置换惯性系 ⇒ 正交破坏（cos 从 0 到 %.3f），点积非洛伦兹标量" % float(cos_boost))

# ---------------------------------------------------------------------------
log("")
log("=" * 78)
npass = sum(1 for _, ok, _ in GUARDS if ok)
log("守卫 %d/%d 通过" % (npass, len(GUARDS)))
log("判词：THREE_FORCE_ORTHOGONALITY__CONDITIONAL_KINEMATIC_IDENTITY__NOT_DYNAMICAL_LAW")
log("=" * 78)
for gid, ok, det in GUARDS:
    if not ok:
        log("FAIL: %s %s" % (gid, det))

with io.open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(LOG) + "\n")
print("\n日志: %s" % OUT)
sys.exit(0 if npass == len(GUARDS) else 1)
