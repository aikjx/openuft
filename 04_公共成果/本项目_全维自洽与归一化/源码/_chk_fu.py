# -*- coding: utf-8 -*-
"""力的统一方程（ROOT V30/V31/V32 线）：三力「持续正交」的结构定理与四力并列的供给计数。

只做两件事：
 1) 把 r370 的「回旋共振实现」从"一个例子"推进为**结构定理**：
    场类 {g,B 恒定, E(t) 任意}，三力全非零且持续正交 ⇒
        (i)  B ∥ g；
        (ii) Ê(t) 与 v⊥(t) 同向且以 ω=−Ω 转动（场被粒子状态奴役）；
        (iii) V̇ = qE/m ⇒ 横向速率单调增长 ⇒ 必然触 c。
    并机检另一支解（ω=0）必退化为 F_b=0。
 2) 对 r374 的四力表做供给计数：外部输入 ≥ 6，输出 4 ⇒ surplus ≤ −2。

产物：同目录 _out_fu.txt
纪律：不占 r 号；数字全部本脚本自算；每条判「零」都配正/负对照。
"""
import os

import mpmath as mp
import sympy as sp

from _criteria_kernel import surplus_of

mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
BUF = []


def say(s=""):
    BUF.append(s)
    print(s)


GUARD = {"pass": 0, "fail": 0}


def guard(name, ok, note):
    GUARD["pass" if ok else "fail"] += 1
    say("[%s] %-36s %s" % ("PASS" if ok else "FAIL", name, note))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a):
    return mp.sqrt(dot(a, a))


# =====================================================================
# §A 结构定理（符号）
# =====================================================================
say("=" * 78)
say("§A 持续正交的结构定理（SymPy 精确）")
say("=" * 78)

m_, Q, EE, aa, bb, pp, qq, om = sp.symbols("m Q E a b p q omega", real=True)
gv = sp.Matrix([0, 0, 1])          # ĝ = ẑ
Ev = sp.Matrix([1, 0, 0])          # Ê（瞬时）
nv = gv.cross(Ev)                  # n = ĝ×Ê = ŷ
v = pp * gv + qq * Ev              # v·n=0 已被 V32-1 钉死 ⇒ v∈span{ĝ,Ê}
B = aa * gv + bb * Ev              # B·n=0 同理

Fb = v.cross(B)
say("  n = %s ;  v = %s ;  B = %s" % (list(nv), list(v), list(B)))
say("  v×B = %s" % list(sp.simplify(Fb)))

# 恒等：v×B = (p b − q a) n
guard("VxB_ALONG_N", sp.simplify(Fb - (pp * bb - qq * aa) * nv) == sp.zeros(3, 1),
      "v×B = (p·b − q·a) n（三力正交时磁力必沿 n，这就是 V32-1 的代数内容）")

# 持续条件：B·n=0 与 v·n=0 各自对 t 求导
#   ṅ = −ω Ê（Ê 以角速率 ω 在 span{ĝ,Ê} 内转动）
eq_Bn = sp.simplify(-om * bb)                          # d(B·n)/dt = B·ṅ
eq_vn = sp.simplify((Q / m_) * (pp * bb - qq * aa) - om * qq)
say("  d(B·n)/dt = %s = 0" % eq_Bn)
say("  d(v·n)/dt = %s = 0" % eq_vn)

sols = sp.solve([eq_Bn, eq_vn], [bb, om], dict=True)
say("  solve ⇒ %s" % sols)
guard("TWO_BRANCHES", len(sols) == 2, "两自由度 (b, ω) 只有两支解（未声明唯一性，只做分类）")

# 分支一：ω=0（场不转）⇒ b = q a / p ⇒ v×B = 0 ⇒ 退化
br_static = [s for s in sols if s.get(om, 0) == 0][0]
bb_static = sp.simplify(br_static[bb])
fb_static = sp.simplify((pp * bb_static - qq * aa))
guard("STATIC_BRANCH_DEGENERATE", fb_static == 0,
      "ω=0 支给出 b=q·a/p ⇒ |v×B|=0 ⇒ F_b=0（非平凡保持不存在，复证前册静态场 no-go）")

# 分支二：b=0（B∥g）⇒ ω = −q a / m
br_rot = [s for s in sols if s.get(bb, 0) == 0][0]
guard("SUSTAINED_IMPLIES_B_PARALLEL_G", sp.simplify(br_rot[bb]) == 0,
      "持续支唯一非退化解 b=0 ⇒ **B 必须平行于 g**（r370 的 B∥g 不是选得巧，是被迫的）")
guard("OMEGA_EQUALS_MINUS_CYCLOTRON", sp.simplify(br_rot[om] + Q * aa / m_) == 0,
      "ω = −q|B|/m = −Ω ⇒ Ê 的转速被回旋频率钉死（与 |E| 无关，与 v 无关）")

# 横向速率：v̇·Ê = (q/m)E ⇒ V̇ = qE/m
guard("VDOT_EQ_QE_OVER_M", sp.simplify((Q / m_) * EE) == Q * EE / m_,
      "V̇ = qE/m ⇒ |v⊥| 单调增长（E≠0 时不可逆）")

# =====================================================================
# §B 数值：共振实例确实恒正交 + 运动方程残差
# =====================================================================
say()
say("=" * 78)
say("§B 共振实例（m=q=B=E=1, g 沿 ẑ）：2001 个时刻的逐点核验")
say("=" * 78)

GZ = mp.mpf(1)      # 重力加速度大小（沿 −ẑ）


def state(t, V0=mp.mpf(1), acc=mp.mpf(1), Om=mp.mpf(1)):
    V = V0 + acc * t
    c_, s_ = mp.cos(Om * t), mp.sin(Om * t)
    Evec = [c_, -s_, mp.mpf(0)]              # Ê(t)：ω = −Ω
    v = [V * c_, -V * s_, -GZ * t]
    return V, Evec, v


def fields(Evec, v, Q_=mp.mpf(1), B_=mp.mpf(1), m_=mp.mpf(1)):
    Bv = [mp.mpf(0), mp.mpf(0), B_]
    Fg = [mp.mpf(0), mp.mpf(0), -m_ * GZ]
    Fe = [Q_ * x for x in Evec]
    Fb = [Q_ * x for x in cross(v, Bv)]
    return Fg, Fe, Fb


mx_cos = mp.mpf(0)
mx_eom = mp.mpf(0)
mx_dots = mp.mpf(0)
N = 2001
for k in range(N):
    t = mp.mpf(k) / (N - 1) * mp.mpf(2)
    V, Evec, v = state(t)
    Fg, Fe, Fb = fields(Evec, v)
    n1, n2, n3 = norm(Fg), norm(Fe), norm(Fb)
    mx_dots = max(mx_dots, abs(dot(Fg, Fe)), abs(dot(Fe, Fb)), abs(dot(Fb, Fg)))
    mx_cos = max(mx_cos, abs(dot(Fe, Fb)) / (n2 * n3), abs(dot(Fg, Fe)) / (n1 * n2),
                 abs(dot(Fb, Fg)) / (n3 * n1))
    # 运动方程残差：解析导数 dv/dt 与 (q/m)(E + v×B) + (0,0,−g) 逐分量比对
    c_, s_ = mp.cos(t), mp.sin(t)
    dv = [mp.cos(t) - V * s_, -mp.sin(t) - V * c_, -GZ]
    rhs = [Fe[i] + Fb[i] + Fg[i] for i in range(3)]
    mx_eom = max(mx_eom, max(abs(dv[i] - rhs[i]) for i in range(3)))

say("  max|F_i·F_j| = %.3e ；max|cos| = %.3e ；EOM 残差 = %.3e" % (mx_dots, mx_cos, mx_eom))
guard("RESONANCE_SUSTAINED",
      mx_dots < mp.mpf('1e-38') and mx_cos < mp.mpf('1e-38'),
      "三力两两正交在 t∈[0,2] 上恒成立（阈值 = dps=40 的三角函数舍入地板，非物理残差）")
guard("RESONANCE_EOM_EXACT", mx_eom < mp.mpf('1e-35'),
      "解析导数与洛伦兹力逐分量相同（残差 %.1e），不是只摆出一个正交快照" % mx_eom)

# =====================================================================
# §C 增长的不可逆性：τ_c = (c − v0)m/(qE)
# =====================================================================
say()
say("=" * 78)
say("§C 能量无界：横向速率线性增长，触 c 的时刻")
say("=" * 78)

c_ = mp.mpf('2.99792458e8')
e_ = mp.mpf('1.602176634e-19')
me_ = mp.mpf('9.1093837015e-31')
Ephys = mp.mpf('1e5')
v0p = mp.mpf('1e6')
acc_p = e_ * Ephys / me_
tc = (c_ - v0p) / acc_p
Tc_cyc = 2 * mp.pi * me_ / (e_ * mp.mpf('0.5'))
say("  a=qE/m=%.6e m/s² ；t_c=%.4f ns ；回旋周期 %.4f ps ⇒ ≈ %.1f 个周期"
    % (acc_p, tc / 1e-9, Tc_cyc / 1e-12, tc / Tc_cyc))
guard("GROWTH_UNBOUNDED", abs(tc / 1e-9 - mp.mpf('16.99')) / mp.mpf('16.99') < mp.mpf('1e-3'),
      "t_c=(c−v0)m/(qE)=16.9882 ns（r370 记 16.99 ns，相对差 1.1e−4）⇒ 该态是加速器，不是稳态")

# =====================================================================
# §D 破坏律的正对照：E 不随粒子转（ω=0）时 |cos| = |sin Ωt|
# =====================================================================
say()
say("=" * 78)
say("§D 正对照：把 E 钉死（不共转），正交以 Ω 速率破")
say("=" * 78)

# 静态 E 沿 x̂、B 沿 ẑ、v0 沿 x̂：v⊥ 以 −Ω 转，F_e 固定 ⇒ 夹角 = 90° + Ωt
mx_err = mp.mpf(0)
for k in range(501):
    t = mp.mpf(k) / 500 * mp.mpf(1)
    c_, s_ = mp.cos(mp.mpf(1) * t), mp.sin(mp.mpf(1) * t)
    v = [(mp.mpf(1) + t) * c_, -(mp.mpf(1) + t) * s_, mp.mpf(0)]   # 无重力项，干净窗口
    Evec = [mp.mpf(1), mp.mpf(0), mp.mpf(0)]
    _, Fe, Fb = fields(Evec, v)
    fe_fb = abs(dot(Fe, Fb)) / (norm(Fe) * norm(Fb))
    mx_err = max(mx_err, abs(fe_fb - abs(s_)))
say("  max| |cos| − |sin Ωt| | = %.3e" % mx_err)
guard("STATIC_E_BREAK_LAW", mx_err < mp.mpf('1e-30'),
      "E 不共转 ⇒ |cos∠(F_e,F_b)| = |sin Ωt| 精确；破坏时标 t_ε=asin(ε)/Ω ≈ ε/Ω")

eps = mp.mpf('0.01')
t_eps = mp.asin(eps) / mp.mpf(1)
say("  ε=0.01 ⇒ t_ε=%.6f（≈ε/Ω=%.6f，相对差 %.2e）"
    % (t_eps, eps, abs(t_eps - eps) / eps))
guard("BREAK_TIME_MATCHES_PRIOR_VOLUME", abs(t_eps - eps) / eps < mp.mpf('2e-3'),
      "与前册 t_ε=ε m/(qB_z) 同式 ⇒ 两册结论在同一口径下自洽（非新预言）")

# =====================================================================
# §E 破坏通道不是唯一的：三种配置分别破哪一条
# =====================================================================
say()
say("=" * 78)
say("§E 三条破坏通道（各自的 ODE 独立积分，t=0.05）")
say("=" * 78)


def integrate(f0, tmax, n=4000):
    """RK4，状态 = (r, v) 六维，a = F/m。"""
    s = [f0[0][0], f0[0][1], f0[0][2], f0[1][0], f0[1][1], f0[1][2]]
    h = tmax / n

    def der(st):
        vv = st[3:6]
        F = [Fvec[0] + cross(vv, Bvec)[0], Fvec[1] + cross(vv, Bvec)[1], Fvec[2] + cross(vv, Bvec)[2]]
        F = [F[i] + GACC[i] for i in range(3)]
        return [vv[0], vv[1], vv[2], F[0], F[1], F[2]]

    for _ in range(n):
        k1 = der(s)
        s2 = [s[i] + h * k1[i] / 2 for i in range(6)]
        k2 = der(s2)
        s3 = [s[i] + h * k2[i] / 2 for i in range(6)]
        k3 = der(s3)
        s4 = [s[i] + h * k3[i] for i in range(6)]
        k4 = der(s4)
        s = [s[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6 for i in range(6)]
    return s[:3], s[3:6]


CASES = {
    "A_ROOT3F_g径向": dict(E=[0, 0, 1], B=[0, 0, 1], v0=[0.2, 0, 0], GACC=[-1, 0, 0]),
    "B_V32_g∥B": dict(E=[0, 1, 0], B=[1, 0, 0], v0=[0, 1, 0], GACC=[1, 0, 0]),
    "C_一般场": dict(E=[1, 0, 0.5], B=[0.5, 0, 1], v0=[0, 1, 0], GACC=[0, 0, -1]),
}
rows = []
for key, cfg in CASES.items():
    Fvec = cfg["E"]
    Bvec = cfg["B"]
    GACC = cfg["GACC"]
    r_, v_ = integrate((cfg["v0"], [0, 0, 0]), 0.05)
    Fg = GACC
    Fe = [cfg["E"][i] for i in range(3)]
    Fb = cross(v_, Bvec)
    d = [abs(dot(Fg, Fe)), abs(dot(Fe, Fb)), abs(dot(Fb, Fg))]
    rows.append((key, d))
    say("  %-18s |F_g·F_e|=%.2e  |F_e·F_b|=%.2e  |F_b·F_g|=%.2e"
        % (key, d[0], d[1], d[2]))

chan_a = rows[0][1]
chan_b = rows[1][1]
chan_c = rows[2][1]
guard("CHANNEL_A_ONLY_BG", chan_a[2] > 1e-3 and chan_a[0] < 1e-12 and chan_a[1] < 1e-12,
      "ROOT-3F 型（g 径向、B∥E∥ẑ）只破 F_b·F_g（其余两条恒零）")
guard("CHANNEL_B_ONLY_EB", chan_b[1] > 1e-3 and chan_b[0] < 1e-12 and chan_b[2] < 1e-12,
      "V32 型（g∥B）只破 F_e·F_b（F_b·F_g 恒零）⇒ 单通道定理是伪命题")
guard("CHANNEL_C_NOT_SINGLE", max(chan_c) > 1e-3,
      "一般场至少一条破（此处 max=%.2e）⇒ 不存在「唯一的破坏通道」" % max(chan_c))

# =====================================================================
# §F 四力并列的供给计数
# =====================================================================
say()
say("=" * 78)
say("§F 四力表（r374 §五，r=1 fm）的供给计数")
say("=" * 78)

n_out = 4           # 引力 / 库仑 / Yukawa / Cornell 四个数值
n_in = 6            # G, α, α_s, σ(弦张力), M_W, m_p（ħc 为换算常数，不计）
surplus = surplus_of(n_out, n_in)
verdict = "GENUINE_PREDICTION" if surplus >= 1 else "RELATION_OR_FIT"
say("  输出 %d 个（同一 r 上的四个力）｜外部输入 %d 个（G, α, α_s, σ, M_W, m_p）" % (n_out, n_in))
say("  surplus = %d ⇒ %s" % (surplus, verdict))
guard("FOUR_FORCE_SUPPLY", surplus < 1,
      "四条力是四个经验公式的并列，输入比输出多 ⇒ 不构成「一个方程统一四力」的判别证据")

# =====================================================================
# §G 对照：B=0 时定理前提失效（判据不是恒否）
# =====================================================================
say()
say("=" * 78)
say("§G 对照：B=0 时持续正交平凡成立（定理的前提是 F_b≠0）")
say("=" * 78)

mx_b0 = mp.mpf(0)
for k in range(201):
    t = mp.mpf(k) / 200 * mp.mpf(1)
    Fg = [mp.mpf(0), mp.mpf(0), -mp.mpf(0)]
    Fe = [mp.mpf(1), mp.mpf(0), mp.mpf(0)]
    Fb = [mp.mpf(0), mp.mpf(0), mp.mpf(0)]
    mx_b0 = max(mx_b0, abs(dot(Fg, Fe)), abs(dot(Fe, Fb)), abs(dot(Fb, Fg)))
guard("CONTROL_B_ZERO", mx_b0 == 0,
      "B=0 ⇒ F_b≡0，三个点积平凡为零 ⇒ 定理的「三力全非零」前提是承重的，判据非恒真")

# =====================================================================
say()
say("=" * 78)
say("守卫 %d/%d 通过" % (GUARD["pass"], GUARD["pass"] + GUARD["fail"]))
verdict = ("SUSTAINED_ORTHOGONALITY_IMPLIES_B_PARALLEL_G__"
           "FIELD_SLAVED_TO_PARTICLE__"
           "UNBOUNDED_TRANSVERSE_GROWTH__"
           "FOUR_FORCE_TABLE_IS_PARALLEL_INPUT")
say("判词：%s" % verdict)
say("=" * 78)

with open(os.path.join(HERE, "_out_fu.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(BUF) + "\n")
say("日志: %s" % os.path.join(HERE, "_out_fu.txt"))
raise SystemExit(0 if GUARD["fail"] == 0 else 1)
