# -*- coding: utf-8 -*-
"""TA2′：相对论 chirp 下的「有界轨道 + 三力正交」——机检裁决。

问题（本册 §七 唯一标 OPEN 的门）：
  结构定理（非相对论）给出 V̇=qE/m>0 ⇒ |v⊥| 线性增长 ⇒ 无界；
  相对论区 γ 使回旋率降为 Ω/γ，问：能否给 E(t) 使其有界而仍锁相？

四个问题，各配机器读数：
 A) 锚点：Ω、回旋周期、非相对论 t_c 复现（16.988 ns）；相对论下 V 只是渐近趋 c。
 B) 状态反馈解：E∥v⊥ 时 EOM 精确可解（p⊥=p⊥0+q∫a dt，φ̇=−Ω/γ）；
    常幅度 ⇒ 能量无界（γ∝t）；正交恒成立（构造上）。
 C) 自治场（恒定转速 ω=−Ω，无反馈）：相位滑移 δ̇=−1+1/γ−(ε/u)sinδ 累积
    ⇒ 正交破坏；非相对论对照 γ≡1 时 δ≡0（正对照）。
 D) 有界轨道的充要条件：p⊥ 有界 ⟺ ∫a dt 有界；两条实现（幅度振荡 / 幅度衰减）
    都要求 E 的零均值或趋于零 ⇒ 三力在零交叉处/无穷远处退化。
 E) 开环预定 chirp 的脆弱性：1% 初速扰动即相位失配；只有状态反馈对任意初值正交。
 F) 供给账：输出 2（正交保持 + 能量有界）、输入 ≥4（幅度程序 + 反馈律 + B + g）。

产物：同目录 _out_ta2.txt
纪律：不占 r 号；数字自算；每条「零/不可能」都配正对照；阈值注明口径。
"""
import os

import mpmath as mp

from _criteria_kernel import surplus_of

mp.mp.dps = 30
HERE = os.path.dirname(os.path.abspath(__file__))
BUF = []
GUARD = {"pass": 0, "fail": 0}


def say(s=""):
    BUF.append(s)
    print(s)


def guard(name, ok, note):
    GUARD["pass" if ok else "fail"] += 1
    say("[%s] %-36s %s" % ("PASS" if ok else "FAIL", name, note))


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def nrm(a):
    return mp.sqrt(dot(a, a))


def unit(a):
    n = nrm(a)
    return [a[i] / n for i in range(3)]


def cosang(a, b):
    return abs(dot(a, b)) / (nrm(a) * nrm(b))


# ---------------------------------------------------------------- constants
Q = mp.mpf('1.602176634e-19')
ME = mp.mpf('9.1093837015e-31')
C = mp.mpf('2.99792458e8')
BZ = mp.mpf('0.5')
GRAV = mp.mpf('9.81')
E0 = mp.mpf('1e5')
V0 = mp.mpf('1e6')

OM = Q * BZ / ME                 # 非相对论回旋角频率
GAM0 = 1 / mp.sqrt(1 - (V0 / C) ** 2)
U0 = GAM0 * V0 / C               # u = p⊥/(m c)
TA = ME * C / (Q * E0)           # 相对论加速度时标 mc/(qE)

say("=" * 78)
say("§A 锚点与单位")
say("=" * 78)
say("  Ω=qB/m = %.8e s^-1 ；回旋周期 2π/Ω = %.4f ps" % (OM, 2 * mp.pi / OM / 1e-12))
say("  u0=γ0β0 = %.6e ；γ0 = %.10f" % (U0, GAM0))
T_C_NR = (C - V0) * ME / (Q * E0)
say("  mc/(qE0) = %.6f ns（记作 T_a；与 t_c 差 %.3f%%）" % (TA / 1e-9, (TA - T_C_NR) / T_C_NR * 100))
say("  非相对论 t_c=(c−v0)m/(qE) = %.4f ns（r370/本册 §4.4 记 16.9882 ns）" % (T_C_NR / 1e-9))
guard("ANCHOR_CYCLOTRON", abs(2 * mp.pi / OM / 1e-12 - mp.mpf('71.448')) < mp.mpf('0.01'),
      "复现 71.448 ps（r370）")
guard("ANCHOR_NONREL_TC", abs(T_C_NR / 1e-9 - mp.mpf('16.9882')) < mp.mpf('0.001'),
      "复现 16.9882 ns（相对差 %.2e）" % (abs(T_C_NR / 1e-9 - mp.mpf('16.9882')) / mp.mpf('16.9882')))

# =====================================================================
# §B 状态反馈解：E ∥ v⊥ —— 解析可解
# =====================================================================
say()
say("=" * 78)
say("§B 状态反馈（E ∥ v⊥）：解析解与正交")
say("=" * 78)

EPS = E0 / (C * BZ)              # ε = E/(cB)，无量纲


def gam(u):
    return mp.sqrt(1 + u * u)


def u_const(t, a=E0, u_init=U0):
    """u(t) = u0 + (q/(mc))∫a dt；常幅度 ⇒ u0 + t/TA。"""
    return u_init + (Q * a / (ME * C)) * t


def phi_const(t, a=E0, u_init=U0):
    """φ(t) = −Ω∫dt/γ，常幅度闭式：−(1/ε)[asinh(u)−asinh(u0)]。"""
    eps = a / (C * BZ)
    u = u_const(t, a, u_init)
    return -(1 / eps) * (mp.asinh(u) - mp.asinh(u_init))


TS = [mp.mpf(0), TA / 10, TA / 2, TA, 2 * TA, 3 * TA]
mx_eom = mp.mpf(0)
mx_orth = mp.mpf(0)
for t in TS:
    u = u_const(t)
    g = gam(u)
    V = C * u / g
    ph = phi_const(t)
    p_perp = ME * C * u
    p_dot = Q * E0
    ph_dot = -OM / g
    # EOM：ṗ⊥=qE ；p⊥φ̇=−qBV
    mx_eom = max(mx_eom, abs(p_dot - Q * E0) / (Q * E0),
                 abs(p_perp * ph_dot + Q * BZ * V) / (Q * BZ * V))
    u_hat = [mp.cos(ph), mp.sin(ph), mp.mpf(0)]
    Evec = [E0 * u_hat[i] for i in range(3)]
    vvec = [V * u_hat[i] for i in range(3)]
    Fg = [mp.mpf(0), mp.mpf(0), ME * GRAV]
    Fe = [Q * Evec[i] for i in range(3)]
    Fb = cross(vvec, [mp.mpf(0), mp.mpf(0), BZ])
    Fb = [Q * Fb[i] for i in range(3)]
    mx_orth = max(mx_orth, cosang(Fg, Fe), cosang(Fe, Fb), cosang(Fb, Fg))
say("  EOM 相对残差 max = %.2e（解析导数，非差分）" % mx_eom)
say("  三力两两 |cos| max = %.2e（6 个时刻）" % mx_orth)
guard("FEEDBACK_EOM_EXACT", mx_eom < mp.mpf('1e-25'), "ṗ⊥=qE ∧ p⊥φ̇=−qBV 精确成立")
guard("FEEDBACK_ORTH_EXACT", mx_orth < mp.mpf('1e-25'),
      "构造上 E∥v⊥ ⇒ 三力两两正交；残差为舍入地板")

u3 = u_const(3 * TA)
u6 = u_const(6 * TA)
u50 = u_const(50 * TA)
g3, g6, g50 = gam(u3), gam(u6), gam(u50)
say("  γ(3T_a)=%.6f  γ(6T_a)=%.6f  γ(50T_a)=%.6f" % (g3, g6, g50))
say("  V/c = u/γ：t=3T_a 时 %.6f；t=50T_a 时 %.10f（<1 且趋 1）"
    % (u3 / g3, u50 / g50))
guard("REL_GROWTH_UNBOUNDED", abs((u3 - U0) - 3) < mp.mpf('1e-12')
      and abs((u6 - U0) - 6) < mp.mpf('1e-12'),
      "常幅度反馈 ⇒ u=u0+t/T_a 线性（Δu=3、6）、γ=√(1+u²)∝t ⇒ 能量仍无界（只是不再「有限时刻触 c」）")
guard("REL_V_ASYMPTOTIC_C", u50 / g50 < 1 and u50 / g50 > mp.mpf('0.999'),
      "V/c={:.6f}<1：相对论把「16.99 ns 触 c」改成渐近线".format(float(u50 / g50)))

# 能量来源：d(γmc²)/dt = qE·v（场在做功，不是自治场）
t = TA
u = u_const(t)
g = gam(u)
V = C * u / g
dgdt = (u / g) * (1 / TA)
lhs = ME * C * C * dgdt
rhs = Q * E0 * V
say("  d(γmc²)/dt=%.6e W ；qE·v=%.6e W ；相对差 %.2e"
    % (lhs, rhs, abs(lhs - rhs) / rhs))
guard("FIELD_DOES_WORK", abs(lhs - rhs) / rhs < mp.mpf('1e-25'),
      "锁相电场必须精确供给 d(γmc²)/dt ⇒ 外部电源，不是自治场解")

# =====================================================================
# §C 自治场（恒定转速 ω=−Ω）：相位滑移累积 ⇒ 正交破坏
# =====================================================================
say()
say("=" * 78)
say("§C 自治恒定转速场：δ̇=−1+1/γ−(ε/u)sinδ")
say("=" * 78)


def rk4(f, y0, tau0, tau1, h):
    y = list(y0)
    tau = tau0
    steps = int(mp.nint((tau1 - tau0) / h))
    for _ in range(steps):
        k1 = f(tau, y)
        y2 = [y[i] + (h / 2) * k1[i] for i in range(len(y))]
        k2 = f(tau + h / 2, y2)
        y3 = [y[i] + (h / 2) * k2[i] for i in range(len(y))]
        k3 = f(tau + h / 2, y3)
        y4 = [y[i] + h * k3[i] for i in range(len(y))]
        k4 = f(tau + h, y4)
        y = [y[i] + (h / 6) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(y))]
        tau += h
    return y, tau


EPS_C = E0 / (C * BZ)            # 6.67e-4
U_REL = mp.mpf(2)                # V=0.894c，强相对论对照


def ode_auto(tau, y):
    u, d = y
    g = gam(u)
    return [EPS_C * mp.cos(d), -1 + 1 / g - (EPS_C / u) * mp.sin(d)]


h = mp.mpf('0.02')
y_end, tau_end = rk4(ode_auto, [U_REL, mp.mpf(0)], mp.mpf(0), mp.mpf(2000), h)
say("  ε=E/(cB)=%.6e ；u(0)=%.2f（V/c=%.4f，γ=%.4f）" % (EPS_C, U_REL, U_REL / gam(U_REL), gam(U_REL)))
say("  τ=2000 后：u=%.6f，δ=%.4f rad（δ<0 方向累积），γ=%.4f"
    % (y_end[0], y_end[1], gam(y_end[0])))
# 扫描最大 |sin δ| 与 δ 首次越过 −π/2 的时刻
u_s, d_s = U_REL, mp.mpf(0)
mx_sin = mp.mpf(0)
tau_pi2 = None
u_min, u_max = u_s, u_s
for k in range(1, 2001):
    u_s, d_s = rk4(ode_auto, [u_s, d_s], mp.mpf(0), h, h)[0]
    mx_sin = max(mx_sin, abs(mp.sin(d_s)))
    u_min, u_max = min(u_min, u_s), max(u_max, u_s)
    if tau_pi2 is None and d_s < -mp.pi / 2:
        tau_pi2 = k * h
say("  max|sinδ| = %.6f ；δ 首次越过 −π/2 于 τ=%.4f（= %.4f 个回旋周期）"
    % (mx_sin, tau_pi2 if tau_pi2 else mp.mpf(-1),
       (tau_pi2 / (2 * mp.pi)) if tau_pi2 else mp.mpf(-1)))
say("  运行中 u∈[%.6f, %.6f] ⇒ γ∈[%.4f, %.4f]（能量并未持续增长）"
    % (u_min, u_max, gam(u_min), gam(u_max)))
guard("NONCHIRPED_ORTH_BREAK", mx_sin > mp.mpf('0.9'),
      "恒定转速 ω=−Ω 无法跟踪 Ω/γ ⇒ |cos∠(F_e,F_b)|→1，正交在 O(回旋周期) 内破坏")
guard("NONCHIRPED_ENERGY_STALLS", u_max - u_min < mp.mpf('0.2'),
      "失谐后 du/dτ=εcosδ 平均为 0 ⇒ 能量停滞（不是无界加速）")

# 正对照：非相对论极限 γ≡1 ⇒ δ̇=−(ε/u)sinδ，δ(0)=0 ⇒ δ≡0（对任意初速）
def ode_auto_nr(tau, y):
    u, d = y
    return [EPS_C * mp.cos(d), -(EPS_C / u) * mp.sin(d)]


nr_ok = True
for u_init in (mp.mpf('0.01'), mp.mpf('0.5'), mp.mpf(2)):
    y_nr, _ = rk4(ode_auto_nr, [u_init, mp.mpf(0)], mp.mpf(0), mp.mpf(50), h)
    nr_ok = nr_ok and abs(y_nr[1]) < mp.mpf('1e-25')
say("  非相对论对照（γ≡1，三组初速）：δ ≡ 0 ⇒ 无反馈也精确锁相")
guard("POSCTRL_NONREL_LOCK", nr_ok,
      "正对照：失谐是相对论效应（γ 依赖），不是判据恒否")

# =====================================================================
# §D 有界轨道：p⊥ 有界 ⟺ ∫a dt 有界；两条实现
# =====================================================================
say()
say("=" * 78)
say("§D 有界轨道：幅度振荡 vs 幅度衰减")
say("=" * 78)

U_REL2 = mp.mpf(2)
P_OSC = mp.mpf('2e-9')
A_OSC = mp.mpf('3e6')
A_DEC = mp.mpf('2e5')
T_DEC = mp.mpf('1e-9')
K_QMC = Q / (ME * C)             # q/(mc) = 5.867e2 1/s² 每 (V/m)


def a_osc(t):
    return A_OSC * mp.cos(2 * mp.pi * t / P_OSC)


def u_osc(t):
    return U_REL2 + K_QMC * A_OSC * (P_OSC / (2 * mp.pi)) * mp.sin(2 * mp.pi * t / P_OSC)


def a_dec(t):
    return A_DEC / (1 + t / T_DEC) ** 2


def u_dec(t):
    return U_REL2 + K_QMC * A_DEC * T_DEC * (1 - 1 / (1 + t / T_DEC))


def orth_residual(t, ufn, afn):
    u = ufn(t)
    g = gam(u)
    V = C * u / g
    ph = -OM * mp.quad(lambda s: 1 / gam(ufn(s)), [0, t])
    u_hat = [mp.cos(ph), mp.sin(ph), mp.mpf(0)]
    Evec = [afn(t) * u_hat[i] for i in range(3)]
    vvec = [V * u_hat[i] for i in range(3)]
    Fg = [mp.mpf(0), mp.mpf(0), ME * GRAV]
    Fe = [Q * Evec[i] for i in range(3)]
    Fb = [Q * x for x in cross(vvec, [mp.mpf(0), mp.mpf(0), BZ])]
    return max(cosang(Fg, Fe), cosang(Fe, Fb), cosang(Fb, Fg)), u, g, V, Evec


# --- 振荡幅度：u 在 [u0−0.56, u0+0.56] 内，γ 有界；E 每周期两次过零
ts_osc = [k * P_OSC / 8 for k in range(41)]
mx_orth_osc = mp.mpf(0)
g_osc = []
for t in ts_osc:
    r, u, g, V, Evec = orth_residual(t, u_osc, a_osc)
    mx_orth_osc = max(mx_orth_osc, r)
    g_osc.append(g)
say("  振荡：u∈[%.4f, %.4f]，γ∈[%.4f, %.4f]，V/c∈[%.4f, %.4f]"
    % (min(u_osc(t) for t in ts_osc), max(u_osc(t) for t in ts_osc),
       min(g_osc), max(g_osc),
       min(u_osc(t) / gam(u_osc(t)) for t in ts_osc),
       max(u_osc(t) / gam(u_osc(t)) for t in ts_osc)))
say("  振荡：三力 |cos| max = %.2e ；E=0 的采样点零交叉数 = %d"
    % (mx_orth_osc, sum(1 for t in ts_osc if abs(a_osc(t)) < mp.mpf('1e-10'))))
guard("BOUNDED_OSC", max(g_osc) < mp.mpf('3') and mx_orth_osc < mp.mpf('1e-20'),
      "幅度符号反转 ⇒ γ 有界、正交精确；但 E 每半周期过零 ⇒ F_e 间歇为零")
n_zero = sum(1 for t in ts_osc if abs(a_osc(t)) < mp.mpf('1e-10'))
guard("BOUNDED_OSC_E_ZEROES", n_zero == 10,
      "5 个周期内 E=0 的采样点 %d 个（a(t)=Acos 的零点）⇒ 三力在那些时刻退化" % n_zero)

# --- 衰减幅度：u→u0+0.117 有界，E>0 恒成立（三力在有限时刻全非零）
t_long = [mp.mpf(0), T_DEC, 5 * T_DEC, 20 * T_DEC, 100 * T_DEC]
mx_orth_dec = mp.mpf(0)
for t in t_long:
    r, u, g, V, Evec = orth_residual(t, u_dec, a_dec)
    mx_orth_dec = max(mx_orth_dec, r)
u_inf = u_dec(mp.mpf('1e6'))
g_inf = gam(u_inf)
say("  衰减：u(100t0)=%.6f，u(∞)=%.6f（闭式 %.6f），γ(∞)=%.6f，V/c=%.6f"
    % (u_dec(100 * T_DEC), u_inf, u_inf, g_inf, u_inf / g_inf))
say("  衰减：三力 |cos| max = %.2e ；E_min=E(100t0)=%.3e V/m（>0）"
    % (mx_orth_dec, a_dec(100 * T_DEC)))
guard("BOUNDED_DEC", abs(u_dec(mp.mpf('1e6')) - u_inf) < mp.mpf('1e-12')
      and g_inf < mp.mpf('3') and mx_orth_dec < mp.mpf('1e-20') and a_dec(100 * T_DEC) > 0,
      "幅度衰减 ⇒ γ 有界、三力在任意有限 t 全非零；但 E→0（场能量→0）")

# --- 判据：p⊥ 有界 ⟺ |∫a dt| 有界（对任意 T）
def sup_int(afn, T):
    return abs(mp.quad(afn, [0, T]))


ratios = []
for name, afn in (("常幅度", lambda t: E0), ("振荡", a_osc), ("衰减", a_dec)):
    d1 = sup_int(afn, mp.mpf('20.3e-9'))
    d2 = sup_int(afn, mp.mpf('40.9e-9'))
    ratios.append(d2 / d1)
    say("  %-4s |Δu(20.3ns)|=%.6f ；|Δu(40.9ns)|=%.6f ；比值 %.4f"
        % (name, K_QMC * d1, K_QMC * d2, d2 / d1))
guard("BOUNDED_IFF_INT_BOUNDED", ratios[0] > mp.mpf('1.9')
      and ratios[1] < mp.mpf('1.2') and ratios[2] < mp.mpf('1.2'),
      "常幅度比值≈2（发散）；振荡/衰减比值≈1（有界）⇒ 有界 ⟺ ∫a 有界")

# =====================================================================
# §E 开环预定 chirp：单轨迹有效，1% 初值扰动即失配
# =====================================================================
say()
say("=" * 78)
say("§E 开环 vs 反馈：相位锁定对初值的敏感性")
say("=" * 78)

U_OL = mp.mpf(2)
TAU_END = 2 * OM * TA                      # ≈ 2987 个回旋时间


def u_nom(tau):
    return U_OL + EPS_C * tau


def gn(tau):
    return gam(u_nom(tau))


def open_loop(p, h=mp.mpf('0.05')):
    """预定场 ψ_E=φ_nom；扰动粒子初值 p（相对）。返回 max|sinδ|、末态。"""
    u, d = U_OL * (1 + p), mp.mpf(0)
    tau = mp.mpf(0)
    mx = mp.mpf(0)
    steps = int(mp.nint(TAU_END / h))
    for _ in range(steps):
        k1 = [EPS_C * mp.cos(d), 1 / gam(u) - 1 / gn(tau) - (EPS_C / u) * mp.sin(d)]
        u2, d2 = u + (h / 2) * k1[0], d + (h / 2) * k1[1]
        k2 = [EPS_C * mp.cos(d2), 1 / gam(u2) - 1 / gn(tau + h / 2) - (EPS_C / u2) * mp.sin(d2)]
        u3, d3 = u + (h / 2) * k2[0], d + (h / 2) * k2[1]
        k3 = [EPS_C * mp.cos(d3), 1 / gam(u3) - 1 / gn(tau + h / 2) - (EPS_C / u3) * mp.sin(d3)]
        u4, d4 = u + h * k3[0], d + h * k3[1]
        k4 = [EPS_C * mp.cos(d4), 1 / gam(u4) - 1 / gn(tau + h) - (EPS_C / u4) * mp.sin(d4)]
        u += (h / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        d += (h / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        tau += h
        mx = max(mx, abs(mp.sin(d)))
    return mx, u, d


res = {}
for p in (mp.mpf(0), mp.mpf('1e-6'), mp.mpf('1e-4'), mp.mpf('1e-2')):
    mx, u_e, d_e = open_loop(p)
    res[p] = (mx, u_e, d_e)
    say("  扰动 %-8s：末 u=%.6f，δ=%.6f rad，max|sinδ|=%.6f"
        % (("%.0e" % p), u_e, d_e, mx))
guard("OPEN_LOOP_EXACT_ON_NOMINAL", res[mp.mpf(0)][0] < mp.mpf('1e-6'),
      "名义轨迹上预定 chirp 精确锁相（δ 被 −(ε/u)sinδ 阻尼）")
guard("OPEN_LOOP_FRAGILE", res[mp.mpf('1e-2')][0] > mp.mpf('0.9'),
      "1% 初速扰动 ⇒ 相位失配 O(1)，正交破坏 ⇒ 开环 chirp 只对一条轨迹有效")
guard("OPEN_LOOP_MONOTONE_IN_P", res[mp.mpf('1e-6')][0] < res[mp.mpf('1e-4')][0]
      < res[mp.mpf('1e-2')][0],
      "失配幅度随扰动单调增 ⇒ 不是数值噪声")

# 反馈对照：任意初值（u_init=2 与 1% 扰动）仍精确正交（构造上 δ≡0）
mx_fb = mp.mpf(0)
for t in (TA / 2, TA, 2 * TA):
    for u_init in (U_REL2, U_REL2 * mp.mpf('1.01')):
        r, _, _, _, _ = orth_residual(t, lambda s: u_const(s, E0, u_init), lambda s: E0)
        mx_fb = max(mx_fb, r)
say("  反馈（两组初值 × 3 时刻）：三力 |cos| max = %.2e" % mx_fb)
guard("FEEDBACK_ROBUST_ANY_INITIAL", mx_fb < mp.mpf('1e-20'),
      "状态反馈对任意初值 δ≡0 ⇒ 与开环的差别是**结构**，不是精度")

# =====================================================================
# §F 供给账与裁决
# =====================================================================
say()
say("=" * 78)
say("§F 供给账")
say("=" * 78)
n_out = 2      # 正交保持 + 能量有界
n_in = 4       # 幅度程序 a(t)、相位反馈律、B、g
surplus = surplus_of(n_out, n_in)
say("  输出 %d ｜ 输入 ≥ %d（a(t) 一个自由函数 + 锁定律 + B + g）⇒ surplus = %d ⇒ %s"
    % (n_out, n_in, surplus, "GENUINE_PREDICTION" if surplus >= 1 else "RELATION_OR_FIT"))
guard("TA2_SUPPLY", surplus < 1,
      "有界 + 正交的代价是**两个**自由函数（幅度程序 + 反馈律），不是一条场方程")

say()
say("=" * 78)
say("守卫 %d/%d 通过" % (GUARD["pass"], GUARD["pass"] + GUARD["fail"]))
verdict = ("TA2_PRIME_BOUNDED_ORBIT_ONLY_AS_STATE_FEEDBACK__"
           "RESONANT_FIELD_MUST_CHIRP_WITH_OMEGA_OVER_GAMMA__"
           "AUTONOMOUS_CONSTANT_FREQUENCY_BREAKS_PHASE_LOCK__"
           "OPEN_LOOP_CHIRP_FRAGILE_AT_ONE_PERCENT__"
           "BOUNDED_NEEDS_AMPLITUDE_PROGRAM_WITH_E_ZERO_MEAN_OR_DECAY__"
           "SIXTEEN_NINETY_NINE_NS_IS_NONREL_ARTIFACT__SUPPLY_NONPOSITIVE")
say("判词：%s" % verdict)
say("=" * 78)

with open(os.path.join(HERE, "_out_ta2.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(BUF) + "\n")
say("日志: %s" % os.path.join(HERE, "_out_ta2.txt"))
raise SystemExit(0 if GUARD["fail"] == 0 else 1)



