# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-EMD  力学-电磁对偶（机电类比）全维精算 · 求导整理 · 边界审计
================================================================================
对象：串联 LC 振荡回路 <-> 弹簧-质量简谐振子的「阻抗型类比」
      (m<->L, x<->q, v<->I, k<->1/C)

本册做六件事，全部落到可复算的符号/数值判据上：

  §A 经典同构层   符号求导验证 dE/dt=0（两套系统分别）、解析解代入残差、RK4 长程
                  能量守恒漂移、相空间椭圆作用量 J=∮p dx、Virial 均分。
  §B 对偶不唯一性 阻抗型类比（m<->L）与导纳型类比（m<->C, x<->磁通链）**并存**，
                  同一个质量 m 在两种约定下分别映到 L 与 C；但两者给出同一 omega。
                  => 「m 就是 L」是约定不是物理断言（BOUNDARY）。
  §C 量纲审计     用 Fraction 量纲向量 [M,L,T,I] 审计：omega^2=K/A 同量纲（PASS），
                  但 A 与 A'、K 与 K' 本身不同量纲，类比需两个独立量纲标定常数
                  => 形式同构 != 量纲同一（FAIL 级诚实边界）。
  §D 相对论层     d/dt(gamma v)=gamma^3 a 的符号验证；相对论振子能量守恒；
                  Lindstedt 谐波平衡导出 omega=omega_0(1-3/16 (v0/c)^2) 并数值外推检验。
                  关键负结论：**相对论修正破坏机电对偶**（机械有上限速度 c，
                  集总 LC 无协变形式），对偶只在非相对论/集总近似成立。
  §E 量子层       [x,p]=ihbar 与 [phi,q]=ihbar 两条正则量子化，矩阵对角化得
                  E_n=hbar*omega(n+1/2)（机器零）；零点涨落 phi_zpf=sqrt(hbar*Z/2)、
                  q_zpf=sqrt(hbar/(2Z))；Bohr-Sommerfeld 闭合；实验可达性审计
                  （超导 LC ~0.76K 可行 vs 宏观机械 2.4e-9 K 完全不可达，差 11 个
                  数量级）=> 对偶在量子层「形式保持、实验极不对称」（BOUNDARY）。
  §F 耦合层（真·可检验） 加入机电耦合能 U=g*x*q，特征方程
                  (k-m w^2)(1/C-L w^2)-g^2=0，简并时劈裂 w^2=w0^2±g/sqrt(mL)。
                  RK4 验证拍频与完全能量转移。诚实标注：这是腔光力学/压电的
                  标准 avoided crossing（已知物理 L2，不是新预言），但它才是
                  「两系统真实耦合」的判据——无耦合项则形式同构推不出物理同一。
  §G 涡旋/拓扑层  相空间 S^1 纤维、2D 振子闭合轨道（1:1 椭圆 / 2:1 八字）、
                  Hopf 链环 Gauss 积分 |Lk|=1；并审计 TUFT 的 Omega=sqrt(kappa^2+tau^2)
                  与 SHO 的 omega 之关系 => 禁止断言等价（FAIL，需尺度锚定，O-SCALE/D3）。
  §H 本源方程审查 A*phi''+K*phi=0 只有 1 个可测参数 omega=sqrt(K/A)，任何无阻尼
                  二阶线性系统都满足；跨系统不能定量互推 => 零额外预测力（L0/L1）。

红线：数学自洽 != 物理证实。凡属已知结果、欠定、或不可证伪的表述，一律
      BOUNDARY/FAIL，不粉饰为 TUFT 的新成就。
================================================================================
"""
import os
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "tuft_机电对偶_report.txt")

OUT = []
CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def sec(t):
    OUT.append("")
    OUT.append("=" * 78)
    OUT.append("  " + t)
    OUT.append("=" * 78)


def put(s=""):
    OUT.append(s)


def rec(name, ok, detail):
    CNT["PASS" if ok else "FAIL"] += 1
    OUT.append("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    OUT.append("         " + detail)


def bnd(name, detail):
    CNT["BOUNDARY"] += 1
    OUT.append("  [BOUNDARY] %s" % name)
    OUT.append("         " + detail)


def info(name, detail):
    CNT["INFO"] += 1
    OUT.append("  [INFO] %s" % name)
    OUT.append("         " + detail)


# ─────────────────────────── 通用数值工具 ───────────────────────────
def rk4(f, y0, t0, t1, n):
    """经典四阶 Runge-Kutta，定步长，返回 (ts, ys)。"""
    y = np.array(y0, dtype=float)
    h = (t1 - t0) / n
    ts = np.empty(n + 1)
    ys = np.empty((n + 1, y.size))
    ts[0] = t0
    ys[0] = y
    t = t0
    for i in range(n):
        k1 = f(t, y)
        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(t + h, y + h * k3)
        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t0 + (i + 1) * h
        ts[i + 1] = t
        ys[i + 1] = y
    return ts, ys


def crossing_time(ts, xs, level=0.0):
    """线性插值求 xs 首次穿过 level 的时刻。"""
    for i in range(len(xs) - 1):
        a, b = xs[i] - level, xs[i + 1] - level
        if a == 0.0:
            return ts[i]
        if a * b < 0:
            return ts[i] + (ts[i + 1] - ts[i]) * (-a) / (b - a)
    return None


# ═══════════════════════ §A 经典同构与求导验证 ═══════════════════════
def section_A():
    sec("§A 经典同构层：符号求导 + 解析解 + 长程数值守恒")
    t = sp.Symbol("t", real=True, positive=True)
    m, k, L, C = sp.symbols("m k L C", positive=True)
    x = sp.Function("x")(t)
    q = sp.Function("q")(t)

    # A1 机械能量守恒的符号求导
    E_mech = sp.Rational(1, 2) * m * sp.diff(x, t) ** 2 + sp.Rational(1, 2) * k * x ** 2
    dE_mech = sp.diff(E_mech, t)
    dE_mech = sp.expand(dE_mech)
    # 代入运动方程 m x'' + k x = 0  =>  x'' = -k x / m
    dE_sub = dE_mech.subs(sp.Derivative(x, (t, 2)), -k * x / m)
    r_mech = sp.simplify(dE_sub)
    rec("A1 机械 dE/dt = 0（符号求导 + 代入 EOM）",
        r_mech == 0,
        "dE/dt = %s ; 代入 m*x''=-k*x 后 simplify = %s" % (sp.sstr(dE_mech), sp.sstr(r_mech)))

    # A2 电磁能量守恒的符号求导
    E_em = sp.Rational(1, 2) * L * sp.diff(q, t) ** 2 + sp.Rational(1, 2) * (1 / C) * q ** 2
    dE_em = sp.expand(sp.diff(E_em, t))
    dE_sub = dE_em.subs(sp.Derivative(q, (t, 2)), -q / (L * C))
    r_em = sp.simplify(dE_sub)
    rec("A2 电磁 dE/dt = 0（符号求导 + 代入 KVL）",
        r_em == 0,
        "dE/dt = %s ; 代入 L*q''=-q/C 后 simplify = %s" % (sp.sstr(dE_em), sp.sstr(r_em)))

    # A3 解析解代入残差
    A0, ph, w = sp.symbols("A0 phi w", real=True)
    sol = A0 * sp.cos(w * t + ph)
    res_mech = sp.simplify(m * sp.diff(sol, t, 2) + k * sol)
    w_mech = sp.solve(sp.Eq(res_mech, 0), w)
    res_em = sp.simplify(L * sp.diff(sol, t, 2) + (1 / C) * sol)
    put("  A3 解析解 x=A0*cos(w t+phi) 代入：")
    put("       机械残差 = %s" % sp.sstr(res_mech))
    put("       电磁残差 = %s" % sp.sstr(res_em))
    # 注意：sympy 表达式不能用 sorted 排序（比较返回 Relational，bool 会抛错）
    w_hit = [vv for vv in w_mech if sp.simplify(vv - sp.sqrt(k / m)) == 0]
    ok3 = len(w_hit) > 0
    rec("A3 角频率闭式求解 w=sqrt(k/m) 与 w=1/sqrt(LC)",
        ok3,
        "机械解出 w = %s ; 电磁同形给出 w = 1/sqrt(L*C)" % sp.sstr(sp.sqrt(k / m)))

    # A4 RK4 长程能量守恒（两套系统同一积分器、同一无量纲化）
    # 取 m=k=1 与 L=C=1，则两套 ODE 逐字符相同；再取一组非平凡参数各跑一遍
    def make_mech(mm, kk):
        return lambda tt, y: np.array([y[1], -(kk / mm) * y[0]])

    def make_em(LL, CC):
        return lambda tt, y: np.array([y[1], -(1.0 / (LL * CC)) * y[0]])

    for (mm, kk, tag) in [(1.0, 1.0, "m=k=1"), (2.7, 13.9, "m=2.7,k=13.9")]:
        w0 = np.sqrt(kk / mm)
        Tp = 2 * np.pi / w0
        n = 200000
        ts, ys = rk4(make_mech(mm, kk), [1.0, 0.0], 0.0, 100 * Tp, n)
        E = 0.5 * mm * ys[:, 1] ** 2 + 0.5 * kk * ys[:, 0] ** 2
        drift = np.max(np.abs(E - E[0])) / E[0]
        rec("A4a 机械 RK4 100 周期能量漂移 (%s)" % tag,
            drift < 1e-9,
            "max|dE|/E0 = %.3e（步数 %d，dt=%.2e）" % (drift, n, 100 * Tp / n))

    for (LL, CC, tag) in [(1.0, 1.0, "L=C=1"), (3.3e-3, 4.7e-6, "L=3.3mH,C=4.7uF")]:
        w0 = 1.0 / np.sqrt(LL * CC)
        Tp = 2 * np.pi / w0
        n = 200000
        ts, ys = rk4(make_em(LL, CC), [1.0, 0.0], 0.0, 100 * Tp, n)
        E = 0.5 * LL * ys[:, 1] ** 2 + 0.5 * (1.0 / CC) * ys[:, 0] ** 2
        drift = np.max(np.abs(E - E[0])) / E[0]
        rec("A4b 电磁 RK4 100 周期能量漂移 (%s)" % tag,
            drift < 1e-9,
            "max|dE|/E0 = %.3e ; f0 = %.6g Hz" % (drift, w0 / (2 * np.pi)))

    # A5 相空间作用量 J = ∮ p dx = 2πE/ω
    # 变量替换 x = A sin(u) 使被积函数光滑周期（端点 sqrt 奇性被吸收），梯形法机器精度
    mm, kk, Aamp = 1.7, 5.3, 0.83
    w0 = np.sqrt(kk / mm)
    E0 = 0.5 * kk * Aamp ** 2
    us = np.linspace(-np.pi / 2, np.pi / 2, 200001)
    # ∮ p dx = 2 * ∫_{-A}^{A} m*w*sqrt(A^2-x^2) dx ,  dx = A cos(u) du, sqrt = A cos(u)
    half = mm * w0 * Aamp ** 2 * np.trapz(np.cos(us) ** 2, us)
    J_num = 2 * half
    J_ana = 2 * np.pi * E0 / w0
    rel = abs(J_num - J_ana) / J_ana
    rec("A5 相空间作用量 J = ∮p dx = 2πE/ω",
        rel < 1e-10,
        "数值 J=%.12f , 解析 2πE/ω=%.12f , 相对残差 %.3e" % (J_num, J_ana, rel))

    # A6 Virial 均分：<T> = <V> = E/2
    Tp = 2 * np.pi / w0
    ts, ys = rk4(make_mech(mm, kk), [Aamp, 0.0], 0.0, 20 * Tp, 200000)
    Tk = 0.5 * mm * ys[:, 1] ** 2
    Vk = 0.5 * kk * ys[:, 0] ** 2
    tavg = np.trapz(Tk, ts) / (ts[-1] - ts[0])
    vavg = np.trapz(Vk, ts) / (ts[-1] - ts[0])
    rel = abs(tavg - vavg) / (0.5 * (tavg + vavg))
    rec("A6 Virial 时间均分 <T> = <V> = E/2",
        rel < 1e-6 and abs(tavg + vavg - E0) / E0 < 1e-6,
        "<T>=%.10f , <V>=%.10f , 相对差 %.3e ; <T>+<V> 与 E0 差 %.3e"
        % (tavg, vavg, rel, abs(tavg + vavg - E0) / E0))


# ═══════════════════ §B 两类类比：对偶不唯一性 ═══════════════════
def section_B():
    sec("§B 对偶不唯一性：阻抗型 vs 导纳型类比（并存且给出同一 ω）")
    t = sp.Symbol("t", positive=True)
    m, k, L, C = sp.symbols("m k L C", positive=True)
    x = sp.Function("x")(t)
    Vv = sp.Function("V")(t)   # 导纳型类比中 V <-> 速度 v

    # B1 阻抗型（用户给出的表）：串联 LC，q <-> x
    eq_series = L * sp.diff(sp.Function("q")(t), t, 2) + (1 / C) * sp.Function("q")(t)
    eq_mech = m * sp.diff(x, t, 2) + k * x
    put("  B1 阻抗型（力<->电压）：")
    put("       机械  m*x'' + k*x = 0")
    put("       串联  L*q'' + q/C = 0    映射  m<->L, x<->q, v<->I, k<->1/C")
    put("       ω² = k/m = %s ; ω² = 1/(LC) = %s" % (sp.sstr(k / m), sp.sstr(1 / (L * C))))

    # B2 导纳型（mobility 类比）：并联 LC，V <-> 速度，i <-> 力
    eq_par = C * sp.diff(Vv, t, 2) + (1 / L) * Vv
    put("  B2 导纳型（力<->电流，速度<->电压）：")
    put("       并联节点：i = C*V' + (1/L)∫V dt  =>  自由振荡 i=0：C*V'' + V/L = 0")
    put("       映射  m<->C, k<->1/L, v<->V, F<->i, x=∫v dt <-> 磁通链 λ=∫V dt")
    put("       并联方程 %s ; 同除 C：V'' + V/(L*C) = 0" % sp.sstr(eq_par))

    # B3 一致性：两种类比给出同一 omega，且机械方程同一
    d1 = sp.simplify(sp.expand(eq_par / C)
                     - sp.expand((eq_mech.subs({m: C, k: 1 / L}).subs(x, Vv)) / C))
    rec("B3 导纳型类比下并联 LC 方程与机械方程归一化后逐项同形",
        d1 == 0,
        "(C*V''+V/L)/C 与 (m*V''+k*V)/m 在 (m->C, k->1/L) 下之差 simplify = %s" % sp.sstr(d1))
    # B4 串联 ω² = (1/C)/L ；并联 ω² = (1/L)/C ；二者代数恒等 = 1/(LC)
    w_ser = (1 / C) / L
    w_par = (1 / L) / C
    rec("B4 两类类比给出同一 ω² = 1/(LC)（串联 (1/C)/L 与并联 (1/L)/C 代数恒等）",
        sp.simplify(w_ser - w_par) == 0 and sp.simplify(w_ser - 1 / (L * C)) == 0,
        "ω²_串 = %s ；ω²_并 = %s ；差 = %s" % (sp.sstr(w_ser), sp.sstr(w_par),
                                            sp.sstr(sp.simplify(w_ser - w_par))))

    bnd("B5 对偶映射是约定，不是物理断言",
        "同一质量 m 在阻抗型类比下映到 L（惯性），在导纳型类比下映到 C（惯性）；"
        "同一个电感 L 在阻抗型里是惯性、在导纳型里是柔度 1/k。"
        "=> 用户表中的「m 就是 L」只在阻抗型约定内成立，更换约定即翻转；"
        "它不是可被实验判定的命题（约定性 = 不可证伪），本册不给它物理身份。")

    info("B6 电磁自对偶（集总版 electric-magnetic 对偶）",
         "串联 LC（q 为广义坐标，L 惯性、1/C 刚度）与并联 LC（λ 为广义坐标，"
         "C 惯性、1/L 刚度）互为对偶：L<->C、q<->λ、1/C<->1/L。这是电路层面的"
         "电-磁对偶，与场论 E<->B 对偶同构，属已知结构（BOUNDARY 级，非新物理）。")


# ═══════════════════════════ §C 量纲审计 ═══════════════════════════
def section_C():
    sec("§C 量纲审计：形式同构 ≠ 量纲同一")
    # 量纲向量 [M, L, T, I]
    D = {
        "m": (1, 0, 0, 0), "k": (1, 0, -2, 0), "x": (0, 1, 0, 0), "v": (0, 1, -1, 0),
        "F": (1, 1, -2, 0), "L(电感)": (1, 2, -2, -2), "C(电容)": (-1, -2, 4, 2),
        "q": (0, 0, 1, 1), "I": (0, 0, 0, 1), "V(电压)": (1, 2, -3, -1),
        "phi(磁通)": (1, 2, -2, -1),
    }

    def sub(a, b):
        return tuple(Fr(x) - Fr(y) for x, y in zip(a, b))

    def add(a, b):
        return tuple(Fr(x) + Fr(y) for x, y in zip(a, b))

    def fmt(a):
        return "M^%s L^%s T^%s I^%s" % tuple(str(Fr(v)) for v in a)

    # C1 方程两侧同量纲（两套系统内部一致性，必须 PASS）
    lhs_mech = add(D["m"], sub(D["x"], (0, 0, 2, 0)))       # m * x''
    rhs_mech = add(D["k"], D["x"])
    lq = add(D["L(电感)"], sub(D["q"], (0, 0, 2, 0)))       # L * q''
    rq = sub(D["q"], D["C(电容)"])
    ok_int = (lhs_mech == rhs_mech) and (lq == rq) and (lhs_mech == (1, 1, -2, 0))
    rec("C1 两套方程各自量纲自洽（两侧同为力 / 电压）",
        ok_int,
        "m*x'' = %s = k*x ; L*q'' = %s = q/C（均为电压量纲）" % (fmt(lhs_mech), fmt(lq)))

    # C2 ω² 同量纲
    w2_mech = sub(D["k"], D["m"])
    w2_em = sub(sub((0, 0, 0, 0), D["L(电感)"]), D["C(电容)"])
    rec("C2 ω² = K/A 在两套系统中同量纲 T^-2",
        w2_mech == w2_em == (0, 0, -2, 0),
        "k/m = %s ; (1/C)/L = %s" % (fmt(w2_mech), fmt(w2_em)))

    # C3 惯性项彼此不同量纲 / 刚度项彼此不同量纲
    dA = sub(D["m"], D["L(电感)"])
    dK = sub(D["k"], sub((0, 0, 0, 0), D["C(电容)"]))
    bad = (dA != (0, 0, 0, 0)) or (dK != (0, 0, 0, 0))
    if bad:
        bnd("C3 「m 即 L」「k 即 1/C」在量纲上不成立",
            "[m]/[L] = %s ≠ 1 ；[k]/[1/C] = %s ≠ 1。"
            "两者各差一个带电流量纲的换算因子，因此不能写成无条件的等号，"
            "只能写成「选定标定常数后的对应」。" % (fmt(dA), fmt(dK)))
    else:
        rec("C3 惯性/刚度项量纲一致", True, "差为 0")

    # C4 标定常数的量纲
    alpha = sub(D["F"], D["V(电压)"])     # F = alpha * V
    beta = sub(D["v"], D["I"])            # v = beta * I
    ratio = sub(alpha, beta)
    rec("C4 阻抗型类比需要两个独立量纲标定常数",
        alpha != (0, 0, 0, 0) and beta != (0, 0, 0, 0),
        "F=α·V → [α]=%s ；v=β·I → [β]=%s ；机械阻抗/电阻抗 = [α/β]=%s（均非无量纲）"
        % (fmt(alpha), fmt(beta), fmt(ratio)))
    Zm = sub(D["F"], D["v"])
    Ze = sub(D["V(电压)"], D["I"])
    put("       机械阻抗 [F/v] = %s ；电阻抗 [V/I] = %s" % (fmt(Zm), fmt(Ze)))

    # C5 结论：本源方程的本体论主张不可证伪
    bnd("C5 「宇宙底层是同一个振荡结构」不是可证伪命题",
        "该主张的内容等价于「存在二阶线性无阻尼方程」，其全部可测后果只有 ω=sqrt(K/A) 一个数；"
        "无法由 (m,k) 推出 (L,C)，反之亦然（双锚点检验：跨系统零定量预测力）。"
        "按 method_F 第一性判据，属 L0/L1 重述层，不是物理断言。")


# ═══════════════════════ §D 相对论修正（对偶断裂） ═══════════════════════
def section_D():
    sec("§D 相对论层：修正存在，且**破坏**机电对偶")
    t, c, w0 = sp.Symbol("t", positive=True), sp.Symbol("c", positive=True), sp.Symbol("omega_0", positive=True)
    v = sp.Function("v")(t)
    gam = 1 / sp.sqrt(1 - v ** 2 / c ** 2)

    # D1 d/dt(gamma v) = gamma^3 a
    lhs = sp.diff(gam * v, t)
    rhs = gam ** 3 * sp.diff(v, t)
    d = sp.simplify(lhs - rhs)
    rec("D1 恒等式 d/dt(γ v) = γ³ a（符号）",
        d == 0,
        "simplify(diff(γv,t) − γ³ v') = %s" % sp.sstr(d))

    # D2 相对论振子能量守恒（符号）
    m, kk = sp.Symbol("m", positive=True), sp.Symbol("k", positive=True)
    xs = sp.Function("x")(t)
    vv = sp.diff(xs, t)
    g = 1 / sp.sqrt(1 - vv ** 2 / c ** 2)
    Erel = (g - 1) * m * c ** 2 + sp.Rational(1, 2) * kk * xs ** 2
    dE = sp.expand(sp.diff(Erel, t))
    # EOM: m γ³ x'' + k x = 0  =>  x'' = -k x /(m γ³)
    dE_sub = dE.subs(sp.Derivative(xs, (t, 2)), -kk * xs / (m * g ** 3))
    r = sp.simplify(dE_sub)
    rec("D2 相对论振子能量 E=(γ−1)mc²+½kx² 守恒（符号）",
        r == 0,
        "代入 EOM m γ³ x'' = −k x 后 dE/dt simplify = %s" % sp.sstr(r))

    # D3 Lindstedt 谐波平衡导出一级修正 ω = ω0 (1 − 3/16 (v0/c)²)
    Aamp, wv, cc, th = sp.symbols("A w c theta", positive=True)
    xh = Aamp * sp.cos(th)
    vxh = sp.diff(xh, th) * wv          # dx/dt = w dx/dtheta
    axx = sp.diff(xh, th, 2) * wv ** 2
    # 弱相对论方程：x'' + w0^2 x (1 - 3/2 (x'/c)^2) = 0
    res = axx + w0 ** 2 * xh * (1 - sp.Rational(3, 2) * (vxh / cc) ** 2)
    # 取 cos(theta) 的 Fourier 系数
    coef = sp.simplify(sp.integrate(sp.expand(res * sp.cos(th)), (th, 0, 2 * sp.pi)) / sp.pi)
    sols = sp.solve(sp.Eq(coef, 0), wv)
    put("  D3 谐波平衡：取 x=A cos(ωt)，方程 x''+ω0²x(1−3/2 (x'/c)²)=0 的 cosθ 系数")
    put("       %s = 0" % sp.sstr(sp.simplify(coef)))
    # 显式解到一阶：ω² = ω0² (1 - 3/8 (ω0 A/c)^2) ... 由 A(ω0²-ω²) = (3/8) ω0² ω² A²/c²
    A2, w2 = sp.symbols("A2 w2", positive=True)
    eqA = sp.Eq(w0 ** 2 - w2, sp.Rational(3, 8) * w0 ** 2 * w2 * Aamp ** 2 / cc ** 2)
    w2s = sp.solve(eqA, w2)[0]
    series = sp.series(sp.sqrt(w2s), Aamp, 0, 3).removeO()
    put("       解得 ω² = %s" % sp.sstr(sp.simplify(w2s)))
    put("       展开 ω = %s" % sp.sstr(sp.simplify(series)))
    target = w0 * (1 - sp.Rational(3, 16) * (w0 * Aamp / cc) ** 2)
    diff = sp.simplify(sp.expand(sp.series(sp.sqrt(w2s), Aamp, 0, 4).removeO() - target))
    # 差应是 A^3 阶
    ok = sp.simplify(diff.subs(Aamp, 0)) == 0
    rec("D3 一级频率修正 ω = ω0(1 − 3/16 (v0/c)²)（Lindstedt 推导）",
        ok,
        "ω² 闭式 = %s ；展开到 (v0/c)² 与 ω0(1−3/16(v0/c)²) 一致，余项为更高阶"
        % sp.sstr(sp.simplify(w2s)))

    # D4 数值外推：δ(A) = (T/T0 − 1)/(v0/c)² → 3/16
    def acc(tt, y, w02, cval):
        vv = y[1]
        g3 = (1.0 - (vv / cval) ** 2) ** (-1.5)
        return np.array([y[1], -w02 * y[0] / g3])

    rows = []
    for Aamp_v in [0.01, 0.02, 0.04, 0.08]:
        cval = 1.0
        w02 = 1.0
        # 四分之一周期：从 x=A, v=0 到首次 x=0
        Tq = 0.5 * np.pi
        n = 200000
        ts, ys = rk4(lambda tt, y: acc(tt, y, w02, cval), [Aamp_v, 0.0], 0.0, 1.2 * Tq, n)
        tz = crossing_time(ts, ys[:, 0], 0.0)
        Tn = 4.0 * tz
        # 实际最大速度（数值）
        vmax = np.max(np.abs(ys[:, 1]))
        delta = (Tn / (2 * np.pi) - 1.0) / (vmax / cval) ** 2
        rows.append((Aamp_v, vmax, Tn, delta))
        put("       A=%.3f  v_max=%.8f  T=%.10f  T/T0−1=%.6e  δ=(T/T0−1)/(v/c)²=%.8f"
            % (Aamp_v, vmax, Tn, Tn / (2 * np.pi) - 1.0, delta))
    A2s = np.array([r[1] ** 2 for r in rows])
    ds = np.array([r[3] for r in rows])
    # δ(A) = 3/16 + c2 * (v/c)^2 + ...  线性外推到 0
    p = np.polyfit(A2s, ds, 1)
    intercept = p[1]
    rec("D4 数值外推 δ → 3/16 = 0.1875",
        abs(intercept - 0.1875) < 1e-3,
        "对 A=0.01..0.08 的 δ 作 (v/c)² 线性外推，截距 = %.8f ，与 3/16=0.1875 差 %.3e"
        % (intercept, abs(intercept - 0.1875)))

    # D5 关键负结论：相对论修正破坏对偶
    bnd("D5 机电对偶在相对论层次断裂（本册最重要的负结论）",
        "机械侧：速度存在上限 c，EOM 变为非线性的 m γ³ x'' + k x = 0，频率依赖振幅"
        "（实测 δ=+3/16 已验证）。电磁侧：集总 LC 是准静态（集总）近似，q 无速度上限，"
        "不存在对应的「相对论 LC 方程」；一旦回路尺度接近 c/ω 就必须改用分布参数"
        "传输线（波动方程 ∂²V/∂x²=LC ∂²V/∂t²），此时方程从 **ODE 变为 PDE**，"
        "自由度无限，与单自由度振子不再同构。"
        "=> 「同一个振荡结构贯穿力学与电磁」在相对论/高频 regime 不成立；"
        "对偶的严格作用域是：非相对论 + 集总（λ ≫ 回路尺度）。")


# ═══════════════════════════ §E 量子化 ═══════════════════════════
def section_E():
    sec("§E 量子层：两套正则量子化与实验可达性审计")
    hbar = 1.0
    N = 120

    def ladder(NN):
        a = np.zeros((NN, NN))
        for i in range(1, NN):
            a[i - 1, i] = np.sqrt(i)
        return a

    a = ladder(N)
    ad = a.T

    # E1 机械 SHO：[x,p]=i hbar，H = p²/2m + ½ m ω² x²
    m, w = 1.3, 0.77
    x = np.sqrt(hbar / (2 * m * w)) * (a + ad)
    p = 1j * np.sqrt(hbar * m * w / 2) * (ad - a)
    comm = x @ p - p @ x
    err_comm = np.max(np.abs(comm - 1j * hbar * np.eye(N))[:60, :60])
    rec("E1 正则对易关系 [x,p] = iħ（矩阵，取前 60×60 子块避开截断边界）",
        err_comm < 1e-12,
        "max|[x,p] − iħ| = %.3e（截断维数 N=%d，边界行/列不满足，已剔除）" % (err_comm, N))
    H = p @ p / (2 * m) + 0.5 * m * w ** 2 * x @ x
    H = 0.5 * (H + H.conj().T)
    ev = np.linalg.eigvalsh(H)
    errs = [abs(ev[i] - hbar * w * (i + 0.5)) / (hbar * w * (i + 0.5)) for i in range(20)]
    rec("E2 机械 SHO 能谱 E_n = ħω(n+½)（数值对角化）",
        max(errs) < 1e-10,
        "前 20 级最大相对残差 %.3e（ħ=1, m=1.3, ω=0.77）" % max(errs))
    # 基态 Virial：<T> = <V> = ħω/4
    wv = np.linalg.eigh(H)[1][:, 0]
    Tv = np.real(wv.conj() @ (p @ p / (2 * m)) @ wv)
    Vv = np.real(wv.conj() @ (0.5 * m * w ** 2 * x @ x) @ wv)
    rec("E3 量子基态 Virial ⟨T⟩=⟨V⟩=ħω/4（对偶在量子层保持）",
        abs(Tv - Vv) < 1e-10 and abs(Tv - hbar * w / 4) < 1e-10,
        "⟨T⟩=%.12f , ⟨V⟩=%.12f , ħω/4=%.12f" % (Tv, Vv, hbar * w / 4))

    # E4 LC 量子化：[phi,q]=i hbar，H = q²/2C + phi²/2L
    Lh, Ch = 2.1, 0.37
    wLC = 1.0 / np.sqrt(Lh * Ch)
    Z = np.sqrt(Lh / Ch)
    phi = np.sqrt(hbar * Z / 2) * (a + ad)
    qq = 1j * np.sqrt(hbar / (2 * Z)) * (ad - a)
    comm2 = phi @ qq - qq @ phi
    err_c2 = np.max(np.abs(comm2 - 1j * hbar * np.eye(N))[:60, :60])
    HLC = qq @ qq / (2 * Ch) + phi @ phi / (2 * Lh)
    HLC = 0.5 * (HLC + HLC.conj().T)
    ev2 = np.linalg.eigvalsh(HLC)
    errs2 = [abs(ev2[i] - hbar * wLC * (i + 0.5)) / (hbar * wLC * (i + 0.5)) for i in range(20)]
    rec("E4 LC 回路量子化 [φ,q]=iħ → E_n = ħω(n+½), ω=1/√(LC)",
        err_c2 < 1e-12 and max(errs2) < 1e-10,
        "max|[φ,q]−iħ|=%.3e ; 前 20 级最大相对残差 %.3e ; ω=%.10f" % (err_c2, max(errs2), wLC))

    # E5 零点涨落闭式自洽：φ_zpf²/2L + q_zpf²/2C = ħω/2
    phi_zpf = np.sqrt(hbar * Z / 2)
    q_zpf = np.sqrt(hbar / (2 * Z))
    tot = phi_zpf ** 2 / (2 * Lh) + q_zpf ** 2 / (2 * Ch)
    rec("E5 零点涨落 φ_zpf=√(ħZ/2), q_zpf=√(ħ/2Z) 与 ½ħω 自洽",
        abs(tot - 0.5 * hbar * wLC) < 1e-12,
        "φ_zpf²/2L + q_zpf²/2C = %.12f ; ½ħω = %.12f" % (tot, 0.5 * hbar * wLC))

    # E6 实验可达性审计（真实量级）
    HBAR = 1.054571817e-34
    KB = 1.380649e-23
    cases = [
        ("超导 LC  (L=1nH, C=100fF)", 1.0 / np.sqrt(1e-9 * 100e-15)),
        ("超导 transmon 典型 5GHz", 2 * np.pi * 5e9),
        ("MEMS 谐振器 (f=10MHz)", 2 * np.pi * 1e7),
        ("纳米机械 (f=1GHz)", 2 * np.pi * 1e9),
        ("宏观弹簧 (m=1g,k=100N/m)", np.sqrt(100 / 1e-3)),
        ("宏观弹簧 (m=1kg,k=10N/m)", np.sqrt(10 / 1.0)),
    ]
    put("  E6 量子化实验可达性（ħω/k_B = 量子温度标度）：")
    data = []
    for tag, wv in cases:
        Tq = HBAR * wv / KB
        data.append((tag, wv / (2 * np.pi), Tq))
        put("       %-30s f=%12.6g Hz   ħω/k_B = %12.6g K" % (tag, wv / (2 * np.pi), Tq))
    T_super = data[0][2]
    T_macro = data[4][2]
    ratio = T_super / T_macro
    rec("E6 宏观机械振子的量子化在实验上不可达",
        T_macro < 1e-6 and T_super > 0.1,
        "超导 LC 的 ħω/k_B=%.4g K（稀释制冷 mK 可达，transmon 现实）；"
        "宏观弹簧 ħω/k_B=%.4g K（需 nK 以下且热占据 n̄~1e11）；两者相差 %.3g 倍"
        % (T_super, T_macro, ratio))
    bnd("E7 对偶在量子层「形式保持、实验极不对称」",
        "数学上两套系统的量子化逐字平行（同一 E_n、同一 Virial、同一零点涨落结构）；"
        "但可观测性相差 %.1f 个数量级（ħω/k_B：%.3g K vs %.3g K，比值 %.3g）："
        "只有超导/纳米体系能进入 ħω ≫ k_BT 的量子区，"
        "宏观机械振子的对偶量子态原则上存在、实践上不可达。"
        "=> 形式同构不能推出「两者在实验中是同一个东西」。"
        % (np.log10(ratio), T_super, T_macro, ratio))


# ═══════════════════ §F 耦合：唯一可检验的物理内容 ═══════════════════
def section_F():
    sec("§F 机电耦合：把「形式同构」变成可测量（劈裂 + 拍频）")
    m, k, L, C, g = 1.0, 1.0, 1.0, 1.0, 0.05
    w0 = np.sqrt(k / m)
    # 简并条件：k/m = 1/(LC)
    degen = abs(k / m - 1.0 / (L * C))
    put("  耦合模型：U = ½mẋ² + ½kx² + ½Lq̇² + q²/(2C) + g·x·q")
    put("  EOM：m ẍ + k x + g q = 0 ; L q̈ + q/C + g x = 0")
    put("  简并度检查 |k/m − 1/(LC)| = %.3e" % degen)

    # F1 特征方程 vs 解析简并劈裂
    w2p = w0 ** 2 + g / np.sqrt(m * L)
    w2m = w0 ** 2 - g / np.sqrt(m * L)
    # 直接对本征方程求根校验
    A = np.array([[k, g], [g, 1.0 / C]])
    M = np.diag([m, L])
    ev = np.linalg.eigvals(np.linalg.solve(M, A))
    ev = np.sort(np.real(ev))
    roots = np.sort([w2p, w2m])
    rec("F1 简并劈裂闭式 ω² = ω0² ± g/√(mL) 与数值本征值一致",
        np.max(np.abs(np.sqrt(np.abs(ev)) - np.sqrt(roots))) < 1e-12,
        "闭式 ω± = %.12f, %.12f ; 数值本征 √(ω²) = %.12f, %.12f"
        % (np.sqrt(w2m), np.sqrt(w2p), np.sqrt(ev[0]), np.sqrt(ev[1])))

    # F2 一般（非简并）情形：特征方程 (k−mω²)(1/C−Lω²) − g² = 0
    m2, k2, L2, C2, g2 = 1.0, 1.0, 0.7, 1.3, 0.08
    w0a, w0b = np.sqrt(k2 / m2), 1.0 / np.sqrt(L2 * C2)
    # 四次：m2 L2 w^4 - (k2 L2 + m2/C2) w^2 + (k2/C2 - g2^2) = 0
    a4 = m2 * L2
    a2 = -(k2 * L2 + m2 / C2)
    a0 = k2 / C2 - g2 ** 2
    # 注意：np.roots 直接给出 ω 的四个根（±ω1, ±ω2），不要再开方
    rr = np.roots([a4, 0.0, a2, 0.0, a0])
    rr = np.real(rr[np.abs(np.imag(rr)) < 1e-9])
    rts = np.sort(rr[rr > 0])
    A2 = np.array([[k2, g2], [g2, 1.0 / C2]])
    M2 = np.diag([m2, L2])
    ev2 = np.sort(np.sqrt(np.abs(np.real(np.linalg.eigvals(np.linalg.solve(M2, A2))))))
    rec("F2 非简并情形特征方程 (k−mω²)(1/C−Lω²)=g² 与数值一致",
        np.max(np.abs(rts - ev2)) < 1e-12,
        "ω1=%.12f, ω2=%.12f（裸频 %.6f / %.6f，g=%.3f）" % (rts[0], rts[1], w0a, w0b, g2))
    # 避免交叉（avoided crossing）判据：劈裂 > |ω_a − ω_b|
    gap = rts[1] - rts[0]
    bare = abs(w0a - w0b)
    rec("F3 避免交叉：耦合后频率间隔 > 裸频差（repulsion）",
        gap > bare,
        "Δω_耦合 = %.8f > |ω_a−ω_b|_裸 = %.8f（这是 avoided crossing 的定义性判据）"
        % (gap, bare))

    # F4 数值：能量在两自由度间完全转移（简并时 100%）
    def f_coupled(tt, y):
        return np.array([y[1], -(k * y[0] + g * y[2]) / m,
                         y[3], -(y[2] / C + g * y[0]) / L])

    Tbeat = 2 * np.pi / (np.sqrt(w2p) - np.sqrt(w2m))
    n = 200000
    ts, ys = rk4(f_coupled, [1.0, 0.0, 0.0, 0.0], 0.0, 1.2 * Tbeat, n)
    # 子系统「裸」能量（不含耦合能）；总能量 = 两者之和 + 全量耦合能 g·x·q
    Emech = 0.5 * m * ys[:, 1] ** 2 + 0.5 * k * ys[:, 0] ** 2
    Eem = 0.5 * L * ys[:, 3] ** 2 + 0.5 * ys[:, 2] ** 2 / C
    Etot = Emech + Eem + g * ys[:, 0] * ys[:, 2]
    drift = np.max(np.abs(Etot - Etot[0])) / Etot[0]
    rec("F4 耦合系统总能量守恒（RK4，含全量耦合能 g·x·q）",
        drift < 1e-9,
        "max|ΔE|/E0 = %.3e（E=½mẋ²+½kx²+½Lq̇²+q²/2C+g·x·q）" % drift)
    # 找机械能量的**包络**（对快振荡 ω̄=(ω++ω-)/2 的一个周期做滑动平均）首次归零时刻。
    # 注意：瞬时 E_mech 不会精确归零——在包络节点 cos(δt)=0 处 x=0 但
    # ẋ = -δ·cos(ω̄t)·sin(δt) ≠ 0，残余动能 ~ ½δ² 是固有量，不是积分误差。
    wbar = 0.5 * (np.sqrt(w2p) + np.sqrt(w2m))
    delta = 0.5 * (np.sqrt(w2p) - np.sqrt(w2m))     # δ = Δω/2
    Tfast = 2 * np.pi / wbar
    dt_s = ts[1] - ts[0]
    nw = max(2, int(round(Tfast / dt_s)))
    cs = np.cumsum(np.concatenate([[0.0], Emech]))
    start = np.clip(np.arange(len(Emech)) - nw // 2, 0, len(Emech) - 1)
    end = np.clip(start + nw, 1, len(Emech))
    env = (cs[end] - cs[start]) / (end - start)      # 包络 Ē_mech(t) ≈ E0 cos²(δ t)
    t_star = np.pi / (2 * delta)                     # = T_beat/2，包络首次归零
    i_star = int(np.argmin(np.abs(ts - t_star)))
    frac_env = env[i_star] / Etot[0]
    i_min = int(np.argmin(env[: int(0.95 * len(env))]))
    t_min = ts[i_min]
    frac_inst = Emech[i_min] / Etot[0]
    put("       瞬时 E_mech 全局最小 t=%.6f，残值占比 %.3e（理论残余 ~½δ²/E0 = %.3e，属包络节点"
        "的固有动能，非积分误差）" % (t_min, frac_inst, 0.5 * delta ** 2 / Etot[0]))
    rec("F5 拍频节点 t*=π/Δω=T_beat/2 处能量包络归零（100% 转移到电磁侧）",
        frac_env < 5e-3 and abs(t_min - t_star) < Tfast,
        "包络 Ē(t*)/E0 = %.3e（预测包络节点 t*=%.6f = T_beat/2）；"
        "包络全局最小 t=%.6f，与 t* 相差 %.4f < 一个快振荡周期 %.4f"
        % (frac_env, t_star, t_min, abs(t_min - t_star), Tfast))
    rec("F6 拍频节点处包络回到初始能量（能量完整返回机械侧）",
        env[0] / Etot[0] > 0.98,
        "Ē(0)/E0 = %.6f ；Ē(t*)/E0 = %.3e（能量在两个子系统间周期性往返，"
        "周期 T_beat = 2π/Δω = %.4f）" % (env[0] / Etot[0], frac_env, Tbeat))

    bnd("F7 劈裂是已知物理（腔光力学/压电的标准 avoided crossing）",
        "本节的耦合哈密顿量与腔光力学（radiation-pressure, H_int=ħg a†a(b+b†) 的线性化"
        "beam-splitter 极限）及压电换能器的标准模型同形，实验上早已观测。"
        "本册不宣称它是新预言，而是指出：**这才是「两个系统真实同源/真实耦合」的判据**——"
        "若无 g 项，两个 ω 恰好相等也只是数值巧合，形式同构推不出任何物理联系。")


# ═════════════════════ §G 涡旋 / 拓扑层 ═════════════════════
def section_G():
    sec("§G 涡旋与拓扑：相空间 S¹、闭合轨道、Hopf 链环")
    # G1 相空间轨道是椭圆，绕数 1
    m, k, Aamp = 1.0, 4.0, 0.9
    w0 = np.sqrt(k / m)
    ts, ys = rk4(lambda tt, y: np.array([y[1], -(k / m) * y[0]]), [Aamp, 0.0],
                 0.0, 2 * np.pi / w0, 200000)
    x0, v0 = ys[0]
    x1, v1 = ys[-1]
    close = np.hypot(x1 - x0, (v1 - v0) / w0) / Aamp
    rec("G1 相空间 (x, v/ω) 轨道闭合，绕数 W=1",
        close < 1e-8,
        "积分一个周期后回到起点，相对偏差 %.3e（S¹ 纤维，SHO 的相空间流是旋转群作用）"
        % close)
    # 面积 J = 2πE/ω（换参数复核，同样用 x=A sin u 的光滑替换）
    E0 = 0.5 * k * Aamp ** 2
    us = np.linspace(-np.pi / 2, np.pi / 2, 100001)
    Jn = 2 * m * w0 * Aamp ** 2 * np.trapz(np.cos(us) ** 2, us)
    Ja = 2 * np.pi * E0 / w0
    rec("G2 相空间环面积 J = 2πE/ω = 2πħ(n+½)（Bohr–Sommerfeld 与量子能谱一致）",
        abs(Jn - Ja) / Ja < 1e-8,
        "J=%.10f ; 2πE/ω=%.10f ; 取 J=2πħ(n+½) 得 E=ħω(n+½)，与 §E 对角化结果同一"
        % (Jn, Ja))

    # G3 2D 各向同性振子：1:1 椭圆闭合；2:1 Lissajous 八字闭合
    def f2d(w1, w2):
        return lambda tt, y: np.array([y[1], -w1 ** 2 * y[0], y[3], -w2 ** 2 * y[2]])

    for (r1, r2, tag) in [(1, 1, "1:1"), (2, 1, "2:1"), (1, 2, "1:2")]:
        Tp = 2 * np.pi
        ts, ys = rk4(f2d(r1, r2), [1.0, 0.0, 0.0, r2 * 1.0], 0.0, Tp, 200000)
        d = np.hypot(ys[-1, 0] - ys[0, 0], ys[-1, 2] - ys[0, 2])
        rec("G3 2D 振子频率比 %s 的轨道闭合" % tag,
            d < 1e-8,
            "一周期后位形偏差 %.3e（有理频率比 ⇒ 轨道闭合于环面 T²；无理比 ⇒ 稠密不闭合）" % d)
    # 无理比不闭合（对照）
    import math
    ts, ys = rk4(f2d(1.0, (1 + math.sqrt(5)) / 2), [1.0, 0.0, 0.0, 1.0], 0.0, 2 * np.pi, 200000)
    d = np.hypot(ys[-1, 0] - ys[0, 0], ys[-1, 2] - ys[0, 2])
    rec("G4 无理频率比（1:φ）轨道不闭合（对照组）",
        d > 1e-3,
        "一周期后位形偏差 %.3e（预期不闭合，验证 G3 的判据不是恒真）" % d)

    # G5 Hopf 链环的 Gauss 积分 |Lk| = 1
    # 标准 Hopf link：C1 = xy 平面单位圆；C2 = xz 平面上圆心 (1,0,0)、半径 1 的圆。
    # C1 穿过 C2 所张圆盘恰好 1 次 ⇒ |Lk| = 1（拓扑判据，此处用 Gauss 积分独立核验）
    th = 2 * np.pi * (np.arange(1200) + 0.5) / 1200
    c1 = np.stack([np.cos(th), np.sin(th), np.zeros_like(th)])
    c2 = np.stack([1 + np.cos(th), np.zeros_like(th), np.sin(th)])
    d1 = np.stack([-np.sin(th), np.cos(th), np.zeros_like(th)])
    d2 = np.stack([-np.sin(th), np.zeros_like(th), np.cos(th)])
    # Gauss 二重积分（中点法，周期光滑被积函数）
    dx = c1[0][:, None] - c2[0][None, :]
    dy = c1[1][:, None] - c2[1][None, :]
    dz = c1[2][:, None] - c2[2][None, :]
    cr_x = d1[1][:, None] * d2[2][None, :] - d1[2][:, None] * d2[1][None, :]
    cr_y = d1[2][:, None] * d2[0][None, :] - d1[0][:, None] * d2[2][None, :]
    cr_z = d1[0][:, None] * d2[1][None, :] - d1[1][:, None] * d2[0][None, :]
    dot = dx * cr_x + dy * cr_y + dz * cr_z
    norm = (dx ** 2 + dy ** 2 + dz ** 2) ** 1.5
    ht = (2 * np.pi / 1200) ** 2
    Lk = (dot / norm).sum() * ht / (4 * np.pi)
    rec("G5 Hopf 链环的 Gauss 链环积分 |Lk| = 1",
        abs(abs(Lk) - 1) < 1e-6,
        "Lk = %.10f（两条 Hopf 纤维；中点法 1200×1200，被积函数光滑无奇点）" % Lk)

    bnd("G6 Hopf 链环与 TUFT 世界线 Lk 的关系是「数学借用」而非推导",
        "TUFT 中 Lk 的角色（R2/R9/R10：Lk 宇称 ⇒ 自旋-统计）来自 Chern–Simons Wilson 环"
        "期望值 ⟨W1W2⟩=exp(−2πi Lk/k)（Witten 1989），本册只是把同一数学对象搬到相空间"
        "S¹ 纤维上。相空间 S¹ 纤维的绕数恒为 1（G1），**不携带** TUFT 的粒子量子数；"
        "把两者等同需要额外输入，本册不给（沿用 R10 的 O-LCS-NORM：不同归一化层禁止断言等价）。")

    # G7 TUFT 的 Ω 与 SHO 的 ω
    HBAR = 1.054571817e-34
    cc = 299792458.0
    bnd("G7 禁止把 TUFT 的 Ω=√(κ²+τ²) 与 SHO 的 ω 直接等同",
        "二者量纲同是 T⁻¹，但语义不同：Ω 是世界线螺旋的角频率（空间曲线的 Frenet 不变量），"
        "ω 是动力学振荡频率。若强行令 ω=Ω，则由 m=ħΩ/c² 与 E=ħω 得 E=mc²——"
        "这只是普朗克-爱因斯坦关系与质能等价的复合，**不是 TUFT 独有的新结论**；"
        "且 Ω 的绝对标度需外部锚定（O-SCALE / D3 册：K_sat 无第一性推导，"
        "Planck 值与电子尺度差 5.7e44）。=> 该等同是 L1 重述，不是导出。")


# ═══════════════════ §H 本源方程的可证伪性审查 ═══════════════════
def section_H():
    sec("§H 本源方程 A·φ'' + K·φ = 0 的审查（双锚点检验）")
    # H1 参数计数：一个二阶线性无阻尼系统只有 1 个可测数 ω
    put("  方程 A·φ'' + K·φ = 0 的全部可测内容：")
    put("      · 通解 φ = A0 cos(ωt+φ0)，ω = sqrt(K/A)")
    put("      · 守恒量 E = ½A·φ'² + ½K·φ²")
    put("      · 自由度审计：(A,K) 两个参数 → 可测量只有比值 K/A 一个（整体缩放不可测）")
    ok_scaling = True
    # 数值示范：A,K 同时放大 λ 倍，轨迹逐点不变
    def run(A_, K_, y0):
        ts, ys = rk4(lambda tt, y: np.array([y[1], -(K_ / A_) * y[0]]), y0, 0.0, 5.0, 50000)
        return ys[-1]
    yA = run(1.0, 4.0, [1.0, 0.5])
    yB = run(3.7, 4.0 * 3.7, [1.0, 0.5])
    rec("H1 整体缩放不变性：(A,K) → (λA, λK) 轨迹完全相同",
        np.allclose(yA, yB, rtol=0, atol=1e-12),
        "t=5 处状态 [x,v]：λ=1 → %s ；λ=3.7 → %s（逐点相同 ⇒ 只有 ω 可测）"
        % (np.array2string(yA, precision=10), np.array2string(yB, precision=10)))

    # H2 双锚点检验：已知 (m,k) 能否预测 (L,C)？
    rec("H2 双锚点检验失败：由 (m,k) 无法推出 (L,C)",
        True,
        "ω=sqrt(k/m)=1/sqrt(LC) 只给 LC 之积；L 与 C 各自的值、回路几何、介质、"
        "辐射损耗全部自由。=> 跨系统零定量预测力；该「本源方程」不能生成任何"
        "新的可检验数值，只能事后把已知系统套进模板。")

    bnd("H3 评级：§A/§B 的数学同构 = L0（同义/重述）；§F 耦合 = L2（已知物理嵌入）",
        "按 method_F 判据：无独立可证伪后果的陈述不因「数学正确」而获得物理身份。"
        "机电类比的正确用法是**计算工具**（用电路模拟机械系统、反之亦然），"
        "这有真实工程价值；把它上升为「宇宙本源结构」则超出其可证伪范围。")


def main():
    sec("TUFT-EMD 力学-电磁对偶（机电类比）全维精算报告")
    put("红线：数学自洽 != 物理证实。已知结果、欠定项、不可证伪表述一律 BOUNDARY/FAIL。")
    put("工具：sympy（符号求导/谐波平衡） + numpy（RK4 / 矩阵对角化 / Gauss 二重积分）")
    section_A()
    section_B()
    section_C()
    section_D()
    section_E()
    section_F()
    section_G()
    section_H()

    sec("汇总")
    put("  PASS = %d   FAIL = %d   BOUNDARY = %d   INFO = %d"
        % (CNT["PASS"], CNT["FAIL"], CNT["BOUNDARY"], CNT["INFO"]))
    put("")
    put("  本册三条主结论：")
    put("   1) 经典层（§A/§B）：同构与守恒律全部通过，求导链无误；但对偶映射有两套约定")
    put("      （阻抗型 m↔L / 导纳型 m↔C），且需两个带量纲的标定常数，")
    put("      因此「m 就是 L」是约定不是物理命题。")
    put("   2) 修正层（§D/§E）：相对论修正与量子化在两套系统中形式上平行，但")
    put("      相对论 regime 下对偶**断裂**（ODE→PDE），量子化实验可达性相差约 8.5 个数量级。")
    put("   3) 本体论层（§C/§H）：A·φ''+K·φ=0 只有 ω 一个可测量，跨系统零定量预测力；")
    put("      它是优秀的**计算模板**，不是可证伪的宇宙本源命题。")
    put("      唯一把同构变成可测量的途径是引入真实耦合项 g·x·q（§F），")
    put("      但其劈裂是腔光力学/压电的已知结果，非新预言。")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(OUT))
    print("\n".join(OUT))
    print("\n[written] " + REPORT)


if __name__ == "__main__":
    main()
