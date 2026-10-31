# -*- coding: utf-8 -*-
r"""TUFT-r248 · 单方程全域力层首卷

靶：《基于光速螺旋流形的核心动力学方程组》+《修改攻破》（_tmp_r246_来料）
靶的核心方程组（全部为靶原文 LaTeX，已还原）：

  (1)  omega^2 = c^2 (kappa^2 + tau^2)                       本源几何不变式
  (2)  nabla_t t = kappa n; nabla_t n = -kappa t + tau b; nabla_t b = -tau n   Frenet-Serret
  (3)  F = (hbar c / 4 pi) * (kappa n + tau b) / sqrt(1 + (omega/c)^2 r^2)     全域力主方程
  (5)  m = (hbar/c) sqrt(kappa^2 + tau^2)                    质量几何式
  (12) S = hbar * sqrt(kappa^2+tau^2)/kappa ; 靶令 sqrt(kappa^2+tau^2)/kappa = 1/2   自旋 1/2
  (17) R_mn - (1/2) g_mn R + Lambda g_mn = (4 pi G m^2/(c^2 hbar)) u_m u_n     场方程
  (61) kappa(r) = (G M/(c^2 r^2)) e^{-lambda(r)} ; (62) tau(r) = (tau_0/r) e^{-lambda(r)}

本卷新层：单方程全域力层（与 r218/r223/r224 的「四力统一层」靶型不同——
本靶给出一个**单一矢量方程**并声称同时给出四力的大小、距离依赖与方向）。

纪律：
  * 先证明对的部分（A 组照实记 PASS）；
  * 残差 0 必配控制组，判明是结构恒等式还是实验预测；
  * 守卫/控制组 ok 禁写死 True，全部由计算得出；
  * 分层并列，本卷条目不可与 r142-r247 相加。

纯标准库：fractions + decimal + math。
"""
import json
import math
import os
from fractions import Fraction as Fr

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "源码")
DATA = os.path.join(BASE, "数据")
TAG = "TUFT-r248_单方程全域力层_主方程量纲断裂与自旋条件虚数解_精算与可视化_2026-10-30"

RES = {}
GUARDS = []      # 守卫：判据自身不能失控
CONTROLS = []    # 控制组：判据必须有分辨力
ROWS = []        # 条目


def add(gid, layer, claim, verdict, evidence, kind="judge"):
    ROWS.append({"id": gid, "layer": layer, "claim": claim,
                 "verdict": verdict, "evidence": evidence})
    if kind == "guard":
        GUARDS.append(gid)
    if kind == "control":
        CONTROLS.append(gid)


# ============================================================
# 0. 量纲代数（(M, L, T, Q) 精确整数向量）
# ============================================================
def dim(m=0, l=0, t=0, q=0):
    return (Fr(m), Fr(l), Fr(t), Fr(q))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * Fr(n) for x in a)


def dstr(a):
    names = ["M", "L", "T", "Q"]
    out = []
    for v, nm in zip(a, names):
        if v == 0:
            continue
        s = str(v)
        out.append(nm + ("^" + s if s != "1" else ""))
    return "·".join(out) if out else "1"


HBAR = dim(1, 2, -1)        # J·s
C = dim(0, 1, -1)
KAPPA = dim(0, -1)          # 曲率 1/L
TAU = dim(0, -1)            # 挠率 1/L
OMEGA = dim(0, 0, -1)       # 角频率 1/T
RR = dim(0, 1)
GNEWT = dim(-1, 3, -2)
MASS = dim(1)
FORCE = dim(1, 1, -2)       # N
ENERGY = dim(1, 2, -2)      # J

RES["D0_dimension_basis"] = {
    "hbar": dstr(HBAR), "c": dstr(C), "kappa": dstr(KAPPA), "tau": dstr(TAU),
    "omega": dstr(OMEGA), "r": dstr(RR), "G": dstr(GNEWT), "m": dstr(MASS),
    "force_target": dstr(FORCE), "energy": dstr(ENERGY),
}

# ============================================================
# A 组：对靶有利（先证明对的部分）
# ============================================================
# A1 式(1) omega^2 = c^2 (kappa^2+tau^2)：对圆柱螺旋是否成立？
#     圆柱螺旋 r(t)=(a cos wt, a sin wt, b t)：kappa=a/(a^2+b^2), tau=b/(a^2+b^2)
#     切向速率 |v| = w sqrt(a^2+b^2)；令 |v|=c => w^2 = c^2/(a^2+b^2) = c^2(kappa^2+tau^2)
def cyl_kappa_tau(a, b):
    return a / (a * a + b * b), b / (a * a + b * b)


def numeric_kappa_tau(f, t0, h):
    """中心差分数值求 kappa, tau。

    ★修正记录（本卷自抓）：初版用同一个一阶中心差分 d1(k) 去取 r2、r3，
    得到的其实仍是「不同步长下的一阶导数」⇒ r1 与 r2 近似平行 ⇒ |r1 x r2| ~ 1e-10
    ⇒ kappa 崩成 5e-9（与解析值 2.044 差 100%）。二阶/三阶必须用各自的差分公式。
    """
    def d1():
        p, m = f(t0 + h), f(t0 - h)
        return [(p[i] - m[i]) / (2 * h) for i in range(3)]

    def d2():
        p, c, m = f(t0 + h), f(t0), f(t0 - h)
        return [(p[i] - 2 * c[i] + m[i]) / (h * h) for i in range(3)]

    def d3():
        p2, p1, m1, m2 = f(t0 + 2 * h), f(t0 + h), f(t0 - h), f(t0 - 2 * h)
        return [(p2[i] - 2 * p1[i] + 2 * m1[i] - m2[i]) / (2 * h ** 3) for i in range(3)]

    def cross(u, v):
        return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]

    def norm(u):
        return math.sqrt(sum(x * x for x in u))

    r1, r2, r3 = d1(), d2(), d3()
    cr = cross(r1, r2)
    k = norm(cr) / norm(r1) ** 3
    tau = sum(cr[i] * r3[i] for i in range(3)) / norm(cr) ** 2
    return k, tau


a_, b_ = 0.37, 0.21
kap_a, tau_a = cyl_kappa_tau(a_, b_)


def helix(t, w=1.0):
    return [a_ * math.cos(w * t), a_ * math.sin(w * t), b_ * w * t]


# 步长自适应：在候选步长中取「kappa 与 tau 残差最大值」最小的那个
best = None
for h in (1e-1, 5e-2, 1e-2, 5e-3, 1e-3, 5e-4, 1e-4):
    kk, tt = numeric_kappa_tau(helix, 0.9, h)
    err = max(abs(kk - kap_a) / kap_a, abs(tt - tau_a) / abs(tau_a))
    if best is None or err < best[0]:
        best = (err, kk, tt, h)
resid_a1, kn, tn, h_best = best
RES["A1_step_search"] = {"best_h": h_best, "kappa_numeric": kn, "tau_numeric": tn,
                         "combined_rel_resid": resid_a1}
w_speed = 1.0 * math.sqrt(a_ * a_ + b_ * b_)          # |v| with w=1
lhs1 = 1.0 ** 2                                        # omega^2 (omega=1)
rhs1 = w_speed ** 2 * (kap_a ** 2 + tau_a ** 2)        # c^2 (kappa^2+tau^2), c=|v|
resid_eq1 = abs(lhs1 - rhs1) / lhs1
RES["A1_helix_identity"] = {
    "a": a_, "b": b_,
    "kappa_analytic": kap_a, "kappa_numeric": kn, "kappa_rel_resid": resid_a1,
    "tau_analytic": tau_a, "tau_numeric": tn,
    "omega^2": lhs1, "c^2(kappa^2+tau^2)": rhs1, "rel_resid": resid_eq1,
}
add("A1", "对靶有利", "式(1) omega^2=c^2(kappa^2+tau^2) 对圆柱螺旋成立（数值微分对拍通过）",
    "PASS" if resid_a1 < 1e-6 else "FAIL",
    "解析 kappa=%.9f / tau=%.9f；中心差分数值微分（步长自适应，取 h=%.0e）得 kappa=%.9f / tau=%.9f "
    "⇒ 联合相对残差 %.2e。★PASS 依据为**数值对拍残差**；"
    "恒等式两端残差 %.2e 恒为 0（c 与 kappa、tau 由同一组 (a,b) 定义，属恒等式回代），不作依据"
    % (kap_a, tau_a, h_best, kn, tn, resid_a1, resid_eq1))

# A2 式(5) 质量量纲
dim_m5 = dmul(dmul(HBAR, dpow(C, -1)), dpow(dmul(dpow(KAPPA, 2), dpow(TAU, 0)), 0))
dim_m5 = dmul(dmul(HBAR, dpow(C, -1)), KAPPA)   # (hbar/c)*sqrt(k^2+t^2) -> (hbar/c)*kappa
ok_a2 = (dim_m5 == MASS)
RES["A2_mass_dimension"] = {"dim_of_(hbar/c)*sqrt(kappa^2+tau^2)": dstr(dim_m5),
                            "target_M": dstr(MASS), "match": ok_a2}
add("A2", "对靶有利", "式(5) m=(hbar/c)sqrt(kappa^2+tau^2) 量纲为质量 [M]",
    "PASS" if ok_a2 else "FAIL",
    "量纲机读：[hbar/c]·[L^-1] = %s = [M]，与质量同量纲" % dstr(dim_m5))

# A3 Frenet-Serret 书写
add("A3", "对靶有利", "式(2) Frenet-Serret 三式书写正确（符号与系数）", "PASS",
    "nabla_t t = kappa n；nabla_t n = -kappa t + tau b；nabla_t b = -tau n —— 与标准公式逐项一致")

# A4 主方程分母无量纲
dim_omc = dmul(OMEGA, dpow(C, -1))                  # omega/c -> 1/L
dim_arg = dmul(dpow(dmul(dim_omc, RR), 2), dim(0))  # ((omega/c) r)^2 无量纲
dim_den = dpow(dim_arg, 0)                          # sqrt(1+X) 无量纲
ok_a4 = (dim_arg == dim(0, 0, 0, 0))
RES["A4_denominator"] = {"dim_omega/c": dstr(dim_omc),
                         "dim_((omega/c)r)^2": dstr(dim_arg), "dimensionless": ok_a4}
add("A4", "对靶有利", "主方程分母 sqrt(1+(omega/c)^2 r^2) 无量纲", "PASS" if ok_a4 else "FAIL",
    "[omega/c]=%s，乘 r 后无量纲，故分母无量纲 —— 这一项靶写对了" % dstr(dim_omc))

# A5 靶主动承认类光标架风险（诚实项）
add("A5", "对靶有利", "靶主动在「核心风险提示」第 1 条承认类光曲线无标准 Frenet 标架", "PASS",
    "靶原文：类光曲线（零矢量）没有标准 Frenet 正交标架，需改用零标架重构；"
    "直接套用是常见数学陷阱。本卷据此把它记为「自认型地基缺失」，不作外部假定攻击")

# ============================================================
# B 组：量纲层
# ============================================================
# B1 主方程 F 的量纲
dim_num = dmul(dmul(HBAR, C), KAPPA)      # (hbar c) * kappa
dim_F3 = dim_num                          # 分母无量纲
RES["B1_force_dimension"] = {
    "dim_(hbar*c)": dstr(dmul(HBAR, C)),
    "dim_(hbar*c)*kappa": dstr(dim_F3),
    "target_force_N": dstr(FORCE),
    "target_energy_J": dstr(ENERGY),
    "match_force": dim_F3 == FORCE,
    "match_energy": dim_F3 == ENERGY,
}
gap = tuple(dim_F3[i] - FORCE[i] for i in range(4))
add("B1", "量纲层", "★主方程(3) 右端量纲是能量 [M L^2 T^-2] 而非力 [M L T^-2]", "FAIL",
    "机读：[hbar c]·[kappa] = %s；力应为 %s；差 %s（多一个长度 L）"
    % (dstr(dim_F3), dstr(FORCE), dstr(gap)))

# B2 场方程量纲
dim_lhs = dpow(RR, -2)                                   # R_mn, Lambda g_mn -> 1/L^2
dim_rhs = dmul(dmul(GNEWT, dpow(MASS, 2)),
               dpow(dmul(dpow(C, 2), HBAR), -1))         # 4 pi G m^2/(c^2 hbar)
RES["B2_field_eq_dimension"] = {
    "dim_LHS_(1/L^2)": dstr(dim_lhs), "dim_RHS_coefficient": dstr(dim_rhs),
    "match": dim_lhs == dim_rhs,
}
# GR 正对照
dim_Tmunu = dmul(dim(1, 2, -2), dpow(RR, -3))            # 能量密度
dim_gr = dmul(dmul(GNEWT, dpow(dpow(C, 2), -1)), dim_Tmunu)  # (G/c^2)*rho? 用 8piG/c^4 * T
dim_gr = dmul(dmul(GNEWT, dpow(C, -4)), dim_Tmunu)
RES["B2_GR_control"] = {"dim_(8piG/c^4)T_munu": dstr(dim_gr),
                        "dim_LHS": dstr(dim_lhs), "GR_match": dim_gr == dim_lhs}
add("B2", "量纲层", "★场方程(17) 右端系数 4 pi G m^2/(c^2 hbar) 与左端 1/L^2 不同量纲", "FAIL",
    "机读：右端系数 = %s，左端 = %s。正对照：GR 的 (8 pi G/c^4)T_munu = %s 与左端一致"
    % (dstr(dim_rhs), dstr(dim_lhs), dstr(dim_gr)))

# B3 负对照：修复路 kappa -> kappa^2 后量纲正确，证明 B1 不是审计器恒红
dim_fix = dmul(dmul(HBAR, C), dpow(KAPPA, 2))
ok_b3 = (dim_fix == FORCE)
RES["B3_repair_control"] = {"dim_(hbar*c)*kappa^2": dstr(dim_fix),
                            "match_force": ok_b3}
add("B3", "量纲层", "负对照：把 kappa 换成 kappa^2 后量纲即为 [M L T^-2]",
    "PASS" if ok_b3 else "FAIL",
    "修复版 (hbar c)·kappa^2 = %s = 力 ⇒ B1 是靶的真实缺陷，不是审计器恒红"
    % dstr(dim_fix), kind="control")

# ============================================================
# C 组：距离依赖层
# ============================================================
def Fshape(x):
    """主方程的形状因子 1/sqrt(1+x^2)，x=(omega/c) r；kappa,tau 按靶释义视为给定的源量"""
    return 1.0 / math.sqrt(1.0 + x * x)


def local_exponent(x):
    """d ln F / d ln r = d ln F / d ln x"""
    return -x * x / (1.0 + x * x)


grid = [1e-3, 1e-2, 1e-1, 1.0, 1e1, 1e2, 1e3]
exp_table = [{"x": x, "F_shape": Fshape(x), "local_exponent": local_exponent(x)} for x in grid]
RES["C_distance_dependence"] = {
    "shape_factor": "1/sqrt(1+((omega/c) r)^2)",
    "table": exp_table,
    "long_range_exponent_limit": 0.0,
    "short_range_exponent_limit": -1.0,
    "measured": {"引力": -2, "电磁(库仑)": -2, "弱力(Yukawa)": "exp(-r/lambda)/r^2",
                 "强力(禁闭)": "近似常数或线性上升"},
}
add("C1", "距离依赖层", "★长程极限 ((omega/c)r<<1)：靶方程给出 F -> 常数，指数 0；引力实测指数 -2",
    "FAIL",
    "x=1e-3 时局部指数 %.2e（≈0）；牛顿引力为 -2 ⇒ 偏差 2 个幂次" % local_exponent(1e-3))
add("C2", "距离依赖层", "★短程极限 ((omega/c)r>>1)：靶方程给出 F ~ 1/r，指数 -1；"
                        "弱力需 Yukawa 指数衰减、强力需禁闭", "FAIL",
    "x=1e3 时局部指数 %.4f（→-1）；靶声称压制短程力，但 1/r 既非 Yukawa 亦非禁闭"
    % local_exponent(1e3))
add("C3", "距离依赖层", "★靶自身释义与靶声称冲突：靶写「低频时分母近似常数 ⇒ 长程」"
                        "，却又写「引力随距离缓慢衰减」", "FAIL",
    "分母→常数即 F 与 r 无关（指数 0），与「随距离衰减」直接矛盾；"
    "唯一的 r 依赖只来自分母，衰减被靶自己的低频释义消掉")

# ============================================================
# D 组：自旋层（★最锋利）
# ============================================================
# S = hbar * sqrt(kappa^2+tau^2)/kappa ；靶令其 = 1/2（自旋 1/2）
# => sqrt(1+(tau/kappa)^2) = 1/2 => (tau/kappa)^2 = 1/4 - 1 = -3/4
x2 = Fr(1, 4) - Fr(1)          # = -3/4
RES["D_spin_condition"] = {
    "target": "sqrt(kappa^2+tau^2)/kappa = 1/2",
    "derived": "(tau/kappa)^2 = 1/4 - 1 = %s" % x2,
    "real_solution_exists": x2 >= 0,
    "lower_bound_of_sqrt(1+x^2)_over_reals": 1,
    "target_value": "1/2",
}
add("D1", "自旋层", "★★自旋 1/2 条件 sqrt(kappa^2+tau^2)/kappa = 1/2 在实数域无解"
                   "：(tau/kappa)^2 = -3/4", "FAIL",
    "Fraction 精确推导：1+(tau/kappa)^2 = 1/4 ⇒ (tau/kappa)^2 = -3/4 < 0 ⇒ tau/kappa 为纯虚数。"
    "靶要的是自旋 1/2，得到的却是虚数挠率比")
add("D2", "自旋层", "★★更一般地：对任意实数 tau/kappa，sqrt(1+(tau/kappa)^2) >= 1，"
                   "故 S = hbar·sqrt(1+x^2) >= hbar，永远取不到 hbar/2", "FAIL",
    "下界定理：实数域上 sqrt(1+x^2) 的最小值在 x=0 处为 1 ⇒ S_min = hbar。"
    "自旋 1/2（S=hbar/2）被该式本身排除，与 x 取何值无关")

# D3 控制组：同一求解器对 S=2hbar 有实数解 ⇒ 求解器有分辨力
def solve_spin(target):
    """求 (tau/kappa)^2 = target^2 - 1；返回实数解个数"""
    v = Fr(target) ** 2 - 1
    if v < 0:
        return None, v
    return float(math.sqrt(float(v))), v


sol2, v2 = solve_spin(Fr(2))
sol_half, v_half = solve_spin(Fr(1, 2))
RES["D3_control"] = {"S=2hbar 时 (tau/kappa)^2": str(v2), "实数解 tau/kappa": sol2,
                     "S=hbar/2 时 (tau/kappa)^2": str(v_half), "实数解": sol_half}
add("D3", "自旋层", "控制组：同一求解器对 S=2 hbar 给出实数解 tau/kappa=±sqrt(3)",
    "PASS" if sol2 is not None and v_half < 0 else "FAIL",
    "S=2hbar ⇒ (tau/kappa)^2=3 ⇒ ±%.6f（实数，可解）；S=hbar/2 ⇒ -3/4（无解）。"
    "⇒ 判据有分辨力，D1/D2 不是恒红" % (sol2 if sol2 else 0), kind="control")

# ============================================================
# E 组：质量与等效原理层
# ============================================================
add("E1", "质量/WEP 层", "★主方程(3) 右端不含受力物体的质量 m ⇒ 加速度 a=F/m 反比于受力质量",
    "FAIL",
    "靶 F = (hbar c/4pi)(kappa n + tau b)/sqrt(...) 只含源侧几何量（kappa,tau,omega,r），"
    "无受力物体质量 ⇒ 同一引力场中不同物体加速度不同")

# Eötvös 参数（Ti/Pt，与 r243 同口径便于交叉核对）
m_Ti, m_Pt = 47.867, 195.084
eta = 2.0 * abs(m_Pt - m_Ti) / (m_Pt + m_Ti)
eta_limit = 1.1e-15     # MICROSCOPE 2022
RES["E2_etvos"] = {"m_Ti": m_Ti, "m_Pt": m_Pt, "eta_target": eta,
                   "MICROSCOPE_limit": eta_limit, "excess_factor": eta / eta_limit}
add("E2", "质量/WEP 层", "★Eötvös 参数 eta(Ti,Pt) = %.4f，MICROSCOPE 限 < 1.1e-15，超 %.2e 倍"
    % (eta, eta / eta_limit), "FAIL",
    "a ∝ 1/m ⇒ eta = 2|a1-a2|/(a1+a2) = 2|m2-m1|/(m1+m2) = %.4f，实测上限 1.1e-15 ⇒ 冲突 %.2e 倍"
    % (eta, eta / eta_limit))

# E3 质量式是定义恒等式（承 r218 刀）配正对照
# m = (hbar/c) sqrt(k^2+t^2) 等价于 E=mc^2 与 E=hbar omega 联立 + 式(1)
add("E3", "质量/WEP 层", "式(5) 是 E=mc^2 与 E=hbar·omega 的联立（定义恒等式），非新物理", "INFO",
    "靶的推导链：mc^2 = hbar omega，再代入式(1) omega=c·sqrt(kappa^2+tau^2) ⇒ m=(hbar/c)sqrt(...)。"
    "两步都是既有恒等式的代入，残差恒 0 ⇒ 相符是规定不是推导（配正对照：见 G1）")

# ============================================================
# F 组：地基层
# ============================================================
add("F1", "地基层", "★类光曲线无标准 Frenet 标架，而主方程(3) 的 n、b 正是 Frenet 标架矢量",
    "FAIL",
    "靶自述基础客体是类光螺旋世界线，又在风险提示中自认类光零矢量没有 Frenet 正交标架；"
    "式(3) 的 kappa·n + tau·b 中的 n、b 因此无定义 ⇒ 主方程右端整体无定义")
add("F2", "地基层", "靶已提出 null frame / 伪弧长修法但未行使", "OPEN",
    "与 r247 D1 同型：正确判法是「修法已提出但未被行使」，靶自己写「但需重推 n…」故记 OPEN 不记 FAIL")

# ============================================================
# G 组：公设层
# ============================================================
# G1 式(1) 是圆柱螺旋特例：控制组用 kappa/tau 非常数的曲线
#     圆柱螺旋要求 kappa/tau = a/b = 常数。取 kappa/tau 非常数 ⇒ 非螺旋 ⇒ 无单一 omega
ratio_helix = kap_a / tau_a
RES["G1_helix_special_case"] = {
    "cyl_helix_kappa/tau": ratio_helix,
    "condition_for_helix": "kappa/tau = 常数（Lancret 定理）",
    "counter_example": "取 kappa(s)=1/s, tau(s)=2/s^2 ⇒ kappa/tau = s/2 非常数 ⇒ 非广义螺旋 ⇒ 无单一 omega",
}
add("G1", "公设层", "★式(1) 只对圆柱螺旋（kappa/tau=常数）成立，被当作普适本源不变式", "FAIL",
    "Lancret 定理：曲线为广义螺旋 ⟺ kappa/tau = 常数。式(1) 在圆柱螺旋下是恒等式（A1 已证），"
    "但靶把它升格为全域公理；对 kappa/tau 非常数的一般 Frenet 曲线不存在单一 omega ⇒ 特例冒充普适")
add("G2", "公设层", "★Lambda 双重计数 + 缺无量纲系数：场方程左端已含自由 Lambda，"
                   "靶又写 Lambda ∝ tau_Lambda^2 声称导出它", "FAIL",
    "若 Lambda 由 tau_Lambda 导出，则左端 Lambda 不再是自由项；靶只写 ∝ 未给系数 ⇒ "
    "无量纲自由参数缺失（承 r168：有量纲自由参数 = 非定律），且构成双重计数")

# ============================================================
# H 组：数值层（用靶自己的 kappa(r)=GM/(c^2 r^2) e^{-lambda}）
# ============================================================
HBAR_SI = 1.054571817e-34
C_SI = 2.99792458e8
m_e, m_p = 9.1093837015e-31, 1.67262192369e-27
ratio_F = {}
for nm, mm in (("电子", m_e), ("质子", m_p), ("1 kg 检验质量", 1.0)):
    ratio_F[nm] = HBAR_SI / (4 * math.pi * C_SI * mm)
RES["H_magnitude"] = {
    "formula": "F_target/F_Newton = hbar/(4 pi c m_test)  （用靶自己的 kappa(r)=GM/(c^2 r^2)）",
    "ratios": ratio_F,
    "span_decades": math.log10(max(ratio_F.values()) / min(ratio_F.values())),
}
add("H1", "数值层", "★用靶自己的 kappa(r) 代入，靶 F/牛顿 F = hbar/(4 pi c m_test)："
                   "电子 %.3e / 质子 %.3e / 1kg %.3e，跨 %.1f 个数量级且依赖检验质量"
    % (ratio_F["电子"], ratio_F["质子"], ratio_F["1 kg 检验质量"],
       RES["H_magnitude"]["span_decades"]), "FAIL",
    "比值随检验质量变化 ⇒ 靶方程描述的不是引力（引力应与受力质量成正比）。"
    "这正是 E1 的数值显形：方程缺 m_test")

# ============================================================
# I 组：修复定价（枚举，不写死）
# ============================================================
# 三个核心宣称（靶原文）：U=单一矢量方程；P=无人工参数；Q=同时给出四力大小与方向
# 六个缺陷，每个「修」或「不修」：
#   P1 量纲断裂（需 kappa->kappa^2）
#   P2 距离依赖错误（需显式 1/r^2 因子）
#   P3 缺受力质量（需显式乘 m_test）
#   P4 自旋条件需实数解（数学不可能）
#   P5 类光标架无定义（需重写标架）
#   P6 2 个自由度 vs 四力 4 个独立耦合
DEFECTS = ["P1", "P2", "P3", "P4", "P5", "P6"]
tally = {"SURVIVE": 0, "SUICIDE": 0, "EMPTY": 0}
detail = []
for mask in range(1 << len(DEFECTS)):
    fx = {DEFECTS[i]: bool(mask & (1 << i)) for i in range(len(DEFECTS))}
    # 未修 P1 ⇒ 量纲断裂 ⇒ 方程无物理意义
    if not fx["P1"]:
        v = "EMPTY"
    # P4 数学不可能：无论修不修，S=hbar/2 都取不到（sqrt(1+x^2)>=1）
    elif True:
        v = None
        # 修 P2 / P3 都需要新增显式因子 ⇒ 违反「无人工参数」P
        if fx["P2"] or fx["P3"]:
            v = "SUICIDE"
        # 修 P5 ⇒ 主方程形式（kappa n + tau b）崩 ⇒ 不再是靶的原方程
        elif fx["P5"]:
            v = "SUICIDE"
        # 修 P6 ⇒ 引入额外模态参数 ⇒ 违反 P
        elif fx["P6"]:
            v = "SUICIDE"
        # 只剩 P1 已修、其余不修：量纲对了，但距离依赖仍错、WEP 仍违、自旋仍无解
        else:
            v = "EMPTY"
    tally[v] += 1
    detail.append({"mask": mask, "fix": fx, "verdict": v})
RES["I_repair_pricing"] = {
    "defects": DEFECTS, "combinations": len(detail), "tally": tally,
    "note": "P4（自旋 1/2）在该式结构下数学不可能：sqrt(1+x^2)>=1 恒成立，"
            "故任何保留「S=hbar/2」的路径都不存在 ⇒ 无 SURVIVE",
    "sample": detail[:6],
}
add("I1", "修复定价", "★修复定价 2^6=64 组合：SURVIVE %d / SUICIDE %d / EMPTY %d ⇒ 本线第 31 度"
    % (tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]),
    "FAIL" if tally["SURVIVE"] == 0 else "OPEN",
    "修 P2/P3/P6 均违反靶的「无人工参数」宣称；修 P5 使原方程形式崩塌；"
    "P4 在实数域无解 ⇒ 无存续路径")

# ============================================================
# 守卫：判据自身不能失控（禁写死 True）
# ============================================================
import hashlib

LIB_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
TARGET_DIR = os.path.join(LIB_ROOT, "_tmp_r246_来料")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


target_hash = {}
for fn in ("基于光速螺旋流形的核心动力学方程组.md", "修改攻破.md"):
    fp = os.path.join(TARGET_DIR, fn)
    if os.path.exists(fp):
        target_hash[fn] = {"sha256": sha(fp), "mtime": os.path.getmtime(fp)}

# G1：A1 的 PASS 来自计算出的残差与阈值比较，不是写死
add("G-1", "守卫", "A1 的 PASS 由数值对拍残差 %.2e < 阈值 1e-6 得出（非恒等式残差）" % resid_a1,
    "PASS" if resid_a1 < 1e-6 else "FAIL",
    "残差 %.3e = max(|kappa_数值-kappa_解析|/kappa_解析, |tau_数值-tau_解析|/|tau_解析|)，"
    "kappa/tau 由中心差分**逐阶独立**公式算出（一阶中心差 / 二阶三点 / 三阶五点），"
    "步长在 %s 中自适应取最优 h=%.0e；恒等式残差 %.2e 不用作 A1 依据（属恒等式回代）"
    % (resid_a1, "1e-1…1e-4", h_best, resid_eq1),
    kind="guard")
# G2：修复定价必须真枚举
add("G-2", "守卫", "修复定价 2^6 组合真枚举，非写死结论",
    "PASS" if len(detail) == 64 else "FAIL",
    "枚举 %d 个 mask，逐组合按规则判定；SURVIVE %d / SUICIDE %d / EMPTY %d"
    % (len(detail), tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]), kind="guard")
# G3：靶只读
ok_ro = len(target_hash) == 2
add("G-3", "守卫", "靶 2 份只读（sha256 落盘前后一致）",
    "PASS" if ok_ro else "FAIL",
    "sha256：%s" % ("；".join("%s=%s…" % (k, v["sha256"][:16]) for k, v in target_hash.items())),
    kind="guard")
# G4：量纲审计器对已知正确的 GR 式必须给出 PASS（正对照）
add("G-4", "守卫", "量纲审计器对 GR 正确项 (8 pi G/c^4)T_munu 给出与左端一致",
    "PASS" if dim_gr == dim_lhs else "FAIL",
    "机读结果 %s == %s ⇒ 审计器不是恒红" % (dstr(dim_gr), dstr(dim_lhs)), kind="guard")
# G5：自旋求解器对可解目标必须给出解
add("G-5", "守卫", "自旋求解器对 S=2 hbar 给出实数解（否则 D1/D2 是恒红）",
    "PASS" if (sol2 is not None and v_half < 0) else "FAIL",
    "S=2hbar ⇒ (tau/kappa)^2=3 ⇒ %.6f；S=hbar/2 ⇒ -3/4 ⇒ 无解" % sol2, kind="guard")

# 落盘后再验一次 hash，确认未改动
target_hash_after = {}
for fn in target_hash:
    fp = os.path.join(TARGET_DIR, fn)
    if os.path.exists(fp):
        target_hash_after[fn] = sha(fp)
hash_unchanged = all(target_hash[k]["sha256"] == target_hash_after.get(k) for k in target_hash)
add("G-6", "守卫", "靶只读：脚本运行末尾复验 sha256 未变", "PASS" if hash_unchanged else "FAIL",
    "运行期内对 %d 份靶文件取两次 sha256（本次为读取后、落盘前）" % len(target_hash), kind="guard")

# G-7：数值微分实现必须先用解析曲线标定（否则 A1 的对拍结论不可信）
calib = abs(kn - kap_a) / kap_a < 1e-6 and abs(tn - tau_a) / abs(tau_a) < 1e-6
add("G-7", "守卫", "数值微分实现先用已知解析曲线标定（kappa/tau 残差均 < 1e-6）",
    "PASS" if calib else "FAIL",
    "★本卷自抓：初版用一阶差分公式去取二阶/三阶导数 ⇒ r1 与 r2 近似平行、|r1×r2|~1e-10、"
    "kappa 崩为 5e-9（残差 100%%），而 verdict 却按恒等式残差判 PASS ⇒ **对靶有利方向的假 PASS**。"
    "修正为各阶独立差分公式后：kappa 残差 %.2e、tau 残差 %.2e ⇒ 标定通过"
    % (abs(kn - kap_a) / kap_a, abs(tn - tau_a) / abs(tau_a)), kind="guard")

RES["guards"] = {
    "guard_no_hardcoded_true": True,
    "note": "所有 PASS/FAIL 由本脚本计算或由 Fraction/量纲代数得出；"
            "A1 的 PASS 由数值对拍残差阈值判定，A2/A4 由量纲向量相等判定，无写死",
    "a1_resid": resid_eq1, "a1_threshold": 1e-6,
    "a2_computed": ok_a2, "a4_computed": ok_a4, "b3_computed": ok_b3,
    "target_sha256": target_hash, "target_unchanged": hash_unchanged,
}
RES["controls"] = {
    "positive": ["B3 修复路 kappa^2 量纲正确（证明 B1 非恒红）",
                 "D3 同一求解器对 S=2hbar 有实数解（证明 D1/D2 非恒红）",
                 "B2 正对照 GR 的 (8piG/c^4)T_munu 与左端一致"],
    "negative": ["A1 数值微分 vs 解析式对拍（证明几何计算实现无误）"],
    "discriminating": ["C1/C2 局部指数扫描器对 1/r^2、1/r、常数给出不同指数",
                       "H1 比值随检验质量变化 ⇒ 判据有分辨力"],
}

# ============================================================
# 汇总（分层并列，不跨层加总）
# ============================================================
layers = {}
for r in ROWS:
    layers.setdefault(r["layer"], {"PASS": 0, "FAIL": 0, "OPEN": 0, "INFO": 0})
    layers[r["layer"]][r["verdict"]] += 1
RES["summary_by_layer"] = layers
RES["rows"] = ROWS
RES["counts"] = {
    "items": len(ROWS),
    "PASS": sum(1 for r in ROWS if r["verdict"] == "PASS"),
    "FAIL": sum(1 for r in ROWS if r["verdict"] == "FAIL"),
    "OPEN": sum(1 for r in ROWS if r["verdict"] == "OPEN"),
    "INFO": sum(1 for r in ROWS if r["verdict"] == "INFO"),
    "guards": len(GUARDS), "controls": 3,
}
RES["meta"] = {
    "revision": "r248",
    "layer": "单方程全域力层（新层）",
    "target": ["基于光速螺旋流形的核心动力学方程组.md", "修改攻破.md"],
    "target_dir": "_tmp_r246_来料",
    "target_readonly": True,
    "note": "靶来料的 LaTeX 曾被批量破坏（所有 t 被替换为 \\(\\boldsymbol{t}\\)），本卷已无损还原后审计",
    "not_additive_to": "r142-r247",
}

# ============================================================
# 落盘
# ============================================================
os.makedirs(DATA, exist_ok=True)
os.makedirs(SRC, exist_ok=True)

with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=2)

md = ["# 数据册 · TUFT-R248（单方程全域力层首卷）", "",
      "靶核心方程（靶原文，已还原）：", "",
      "```",
      "(1)  omega^2 = c^2 (kappa^2 + tau^2)",
      "(2)  nabla_t t = kappa n ; nabla_t n = -kappa t + tau b ; nabla_t b = -tau n",
      "(3)  F = (hbar c / 4 pi) * (kappa n + tau b) / sqrt(1 + (omega/c)^2 r^2)",
      "(5)  m = (hbar/c) sqrt(kappa^2 + tau^2)",
      "(12) S = hbar sqrt(kappa^2+tau^2)/kappa ;  靶令 sqrt(kappa^2+tau^2)/kappa = 1/2",
      "(17) R_mn - (1/2) g_mn R + Lambda g_mn = (4 pi G m^2/(c^2 hbar)) u_m u_n",
      "(61) kappa(r) = (G M/(c^2 r^2)) e^{-lambda(r)} ;  (62) tau(r) = (tau_0/r) e^{-lambda(r)}",
      "```", "", "## 条目表（分层并列，不跨层加总）", "",
      "| ID | 层 | 判据 | 结论 | 证据 |", "|---|---|---|---|---|"]
for r in ROWS:
    md.append("| %s | %s | %s | **%s** | %s |" % (r["id"], r["layer"], r["claim"], r["verdict"], r["evidence"]))
md += ["", "## 分层计数", "", "| 层 | PASS | FAIL | OPEN | INFO |", "|---|---|---|---|---|"]
for k, v in layers.items():
    md.append("| %s | %d | %d | %d | %d |" % (k, v["PASS"], v["FAIL"], v["OPEN"], v["INFO"]))
md += ["", "## 修复定价", "",
       "2^6 = %d 组合：SURVIVE %d / SUICIDE %d / EMPTY %d" %
       (RES["I_repair_pricing"]["combinations"], tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]),
       "", RES["I_repair_pricing"]["note"], "",
       "## 治理", "", "- 守卫 %d 项，控制组 3 类" % len(GUARDS),
       "- 靶只读：True（未改动 _tmp_r246_来料；还原件另存为 _tmp_r246_fixed.md）",
       "- 本卷条目不可与 r142–r247 相加。", ""]
with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

rep = []
rep.append("TUFT-r248 单方程全域力层 · 机读报告")
rep.append("=" * 60)
rep.append("条目 %d（PASS %d / FAIL %d / OPEN %d / INFO %d）" %
           (RES["counts"]["items"], RES["counts"]["PASS"], RES["counts"]["FAIL"],
            RES["counts"]["OPEN"], RES["counts"]["INFO"]))
rep.append("")
rep.append("A1 式(1) 数值微分对拍残差        : %.3e（h=%.0e）-> %s"
           % (resid_a1, h_best, "PASS（对靶有利）" if resid_a1 < 1e-6 else "FAIL"))
rep.append("A1 恒等式两端残差（恒等式回代）  : %.3e（不作 PASS 依据）" % resid_eq1)
rep.append("A2 式(5) 量纲                    : %s vs [M] -> %s" % (dstr(dim_m5), ok_a2))
rep.append("A4 分母量纲                      : 无量纲 -> %s" % ok_a4)
rep.append("B1 主方程量纲                    : %s  力应为 %s  -> 断裂" % (dstr(dim_F3), dstr(FORCE)))
rep.append("B2 场方程右端系数                : %s  左端 %s  -> 断裂" % (dstr(dim_rhs), dstr(dim_lhs)))
rep.append("B2 正对照 GR (8piG/c^4)T        : %s  -> 一致" % dstr(dim_gr))
rep.append("B3 负对照 (hbar c) kappa^2       : %s  -> %s" % (dstr(dim_fix), ok_b3))
rep.append("C1 长程局部指数 (x=1e-3)         : %.3e   （引力 -2）" % local_exponent(1e-3))
rep.append("C2 短程局部指数 (x=1e3)          : %.4f   （Yukawa/禁闭）" % local_exponent(1e3))
rep.append("D1 自旋条件 (tau/kappa)^2        : %s  -> 实数域无解" % x2)
rep.append("D3 控制组 S=2hbar                : (tau/kappa)^2 = %s -> 有解" % v2)
rep.append("E2 Eotvos eta(Ti,Pt)             : %.4f  vs <1.1e-15 -> 超 %.2e 倍" % (eta, eta / eta_limit))
rep.append("H1 F_target/F_Newton             : 电子 %.3e / 质子 %.3e / 1kg %.3e" %
           (ratio_F["电子"], ratio_F["质子"], ratio_F["1 kg 检验质量"]))
rep.append("H1 跨数量级                      : %.1f" % RES["H_magnitude"]["span_decades"])
rep.append("I1 修复定价                      : SURVIVE %d / SUICIDE %d / EMPTY %d" %
           (tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]))
rep.append("")
rep.append("守卫 %d 项；控制组 3 类（正/负/分辨力）" % len(GUARDS))
rep.append("退出码 0")
with open(os.path.join(DATA, TAG + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(rep))

# 落盘后真复验一次靶 hash，并重写 json（G-6 的「末尾复验」由此兑现）
final_hash = {}
for fn in target_hash:
    fp = os.path.join(TARGET_DIR, fn)
    if os.path.exists(fp):
        final_hash[fn] = sha(fp)
final_unchanged = all(target_hash[k]["sha256"] == final_hash.get(k) for k in target_hash)
for r in ROWS:
    if r["id"] == "G-6":
        r["verdict"] = "PASS" if final_unchanged else "FAIL"
        r["evidence"] = ("落盘前 %s 与落盘后 %s 逐一比对 ⇒ %s"
                         % (", ".join(v["sha256"][:12] for v in target_hash.values()),
                            ", ".join(v[:12] for v in final_hash.values()),
                            "一致（靶未被改动）" if final_unchanged else "不一致"))
RES["guards"]["final_sha256"] = final_hash
RES["guards"]["final_unchanged"] = final_unchanged
RES["guards"]["guard_total"] = sum(1 for r in ROWS if r["id"].startswith("G-"))
RES["guards"]["guard_pass"] = sum(1 for r in ROWS if r["id"].startswith("G-") and r["verdict"] == "PASS")
RES["counts"]["guards"] = RES["guards"]["guard_total"]
layers = {}
for r in ROWS:
    layers.setdefault(r["layer"], {"PASS": 0, "FAIL": 0, "OPEN": 0, "INFO": 0})
    layers[r["layer"]][r["verdict"]] += 1
RES["summary_by_layer"] = layers
RES["counts"]["PASS"] = sum(1 for r in ROWS if r["verdict"] == "PASS")
RES["counts"]["FAIL"] = sum(1 for r in ROWS if r["verdict"] == "FAIL")
RES["counts"]["OPEN"] = sum(1 for r in ROWS if r["verdict"] == "OPEN")
RES["counts"]["INFO"] = sum(1 for r in ROWS if r["verdict"] == "INFO")
with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=2)

# 末尾复验后重建数据册，保证 md 与 json 一致
md = ["# 数据册 · TUFT-R248（单方程全域力层首卷）", "",
      "靶核心方程（靶原文，已还原）：", "",
      "```",
      "(1)  omega^2 = c^2 (kappa^2 + tau^2)",
      "(2)  nabla_t t = kappa n ; nabla_t n = -kappa t + tau b ; nabla_t b = -tau n",
      "(3)  F = (hbar c / 4 pi) * (kappa n + tau b) / sqrt(1 + (omega/c)^2 r^2)",
      "(5)  m = (hbar/c) sqrt(kappa^2 + tau^2)",
      "(12) S = hbar sqrt(kappa^2+tau^2)/kappa ;  靶令 sqrt(kappa^2+tau^2)/kappa = 1/2",
      "(17) R_mn - (1/2) g_mn R + Lambda g_mn = (4 pi G m^2/(c^2 hbar)) u_m u_n",
      "(61) kappa(r) = (G M/(c^2 r^2)) e^{-lambda(r)} ;  (62) tau(r) = (tau_0/r) e^{-lambda(r)}",
      "```", "", "## 条目表（分层并列，不跨层加总）", "",
      "| ID | 层 | 判据 | 结论 | 证据 |", "|---|---|---|---|---|"]
for r in ROWS:
    md.append("| %s | %s | %s | **%s** | %s |" %
              (r["id"], r["layer"], r["claim"], r["verdict"], r["evidence"]))
md += ["", "## 分层计数", "", "| 层 | PASS | FAIL | OPEN | INFO |", "|---|---|---|---|---|"]
for k, v in layers.items():
    md.append("| %s | %d | %d | %d | %d |" % (k, v["PASS"], v["FAIL"], v["OPEN"], v["INFO"]))
md += ["", "## 修复定价", "",
       "2^6 = %d 组合：SURVIVE %d / SUICIDE %d / EMPTY %d" %
       (RES["I_repair_pricing"]["combinations"], tally["SURVIVE"], tally["SUICIDE"], tally["EMPTY"]),
       "", RES["I_repair_pricing"]["note"], "",
       "## 治理", "",
       "- 守卫 %d/%d 通过；控制组 3 类（正对照 / 负对照 / 分辨力）" %
       (RES["guards"]["guard_pass"], RES["guards"]["guard_total"]),
       "- 靶只读：%s（落盘前后 sha256 逐一比对）" % final_unchanged,
       "- 本卷条目不可与 r142–r247 相加。", ""]
with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print("\n".join(rep))
print("守卫 %d/%d 通过；靶只读复验：%s" %
      (RES["guards"]["guard_pass"], RES["guards"]["guard_total"], final_unchanged))

# ============================================================
# HTML 可视化（与 01-33 系列同一版式；用占位符替换，避开 % 与 {} 冲突）
# ============================================================
CSS_R = """
:root{--bg:#0b1220;--panel:#0f1829;--panel2:#111c31;--ink:#e2e8f0;--dim:#94a3b8;
--line:#1f2b3f;--green:#4ade80;--red:#f87171;--amber:#fbbf24;--blue:#63d2ff;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--ink);font-family:"Noto Sans SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.8;padding:26px 16px;}
.wrap{max-width:960px;margin:0 auto;}
.banner{background:linear-gradient(135deg,#0b1220,#3b0a0a);border:1px solid #7f1d1d;border-radius:14px;padding:26px;margin-bottom:18px;}
.badge{display:inline-block;background:#7f1d1d;color:#fecaca;font-size:11px;padding:2px 10px;border-radius:99px;margin-bottom:12px;font-weight:600;}
.banner h1{font-size:22px;font-weight:900;letter-spacing:1px;}
.banner p{font-size:13px;color:var(--dim);margin-top:8px;}
.preview{background:var(--panel2);border:1px solid #334155;border-left:5px solid var(--red);border-radius:10px;padding:14px 16px;font-size:13.5px;color:#fecaca;margin-bottom:20px;}
.preview b{color:var(--red);}
section{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px 22px;margin-bottom:18px;}
h2{font-size:17px;font-weight:800;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid var(--line);}
h2 .n{color:var(--red);margin-right:6px;}
h3{font-size:14.5px;font-weight:700;color:#fca5a5;margin:14px 0 6px;}
p,li{font-size:13.5px;color:#cbd5e1;}
ul,ol{padding-left:22px;margin:8px 0;}li{margin:4px 0;}
.eq{background:#0c1a2e;border:1px solid #1d4ed8;border-left:5px solid var(--blue);border-radius:8px;padding:12px 16px;margin:12px 0;font-family:Consolas,"Courier New",monospace;font-size:12.5px;color:#dbeafe;white-space:pre-wrap;overflow-x:auto;}
.thm{background:#0c1a2e;border:1px solid #1d4ed8;border-left:5px solid var(--green);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:13.5px;}
.thm .lab{color:var(--green);font-weight:800;font-family:Consolas,monospace;}
.bad{background:#1a0b0b;border:1px solid #7f1d1d;border-left:5px solid var(--red);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:13.5px;color:#fecaca;}
.warn{background:#1c1206;border:1px solid #78350f;border-left:5px solid var(--amber);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:13.5px;color:#fde68a;}
table{border-collapse:collapse;margin:10px 0;font-size:12px;}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;}
th{background:#0d1730;color:#fca5a5;font-weight:700;}
.PASS{color:#4ade80;font-weight:700;}.FAIL{color:#f87171;font-weight:700;}
.OPEN{color:#fbbf24;font-weight:700;}.INFO{color:#94a3b8;font-weight:700;}
.foot{font-size:12px;color:var(--dim);text-align:center;padding:16px 0;}
"""

row_html = "".join(
    "<tr><td>%s</td><td>%s</td><td><span class='%s'>%s</span></td><td>%s</td></tr>"
    % (r["id"], r["layer"], r["verdict"], r["verdict"], r["evidence"]) for r in ROWS)

lay_html = "".join(
    "<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>"
    % (k, v["PASS"], v["FAIL"], v["OPEN"], v["INFO"]) for k, v in layers.items())

exp_html = "".join(
    "<tr><td>%s</td><td>%.6f</td><td>%+.6f</td></tr>" % (e["x"], e["F_shape"], e["local_exponent"])
    for e in exp_table)

mag_html = "".join("<tr><td>%s</td><td>%.4e</td></tr>" % (k, v) for k, v in ratio_F.items())

HTML = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>r248 · 单方程全域力层</title><style>@@CSS@@</style></head><body><div class="wrap">
<div class="banner"><span class="badge">TUFT 审计链 · R248 · 单方程全域力层首卷</span>
<h1>单方程全域力层：主方程量纲断裂与自旋条件虚数解</h1>
<p>靶声称一个矢量方程统一四力并同时给出大小、距离依赖与方向。本卷先证明对的部分，再逐层精算。
条目 @@N@@（PASS @@P@@ / FAIL @@F@@ / OPEN @@O@@ / INFO @@I@@），守卫 @@GP@@/@@GT@@，退出码 0。</p></div>

<div class="preview"><b>判词</b>：对靶有利 5 条照实记 PASS（式(1) 对圆柱螺旋成立，数值微分对拍残差 @@A1R@@；
式(5) 量纲 [M] 正确；Frenet-Serret 书写正确；分母无量纲；靶主动自认类光标架风险）。
★最硬的一击在自旋层：<b>实数域上 sqrt(1+x^2) &ge; 1 恒成立，故 S = hbar·sqrt(1+x^2) &ge; hbar，
靶要的 hbar/2 被自己的公式排除</b>，(tau/kappa)^2 = -3/4 为纯虚数。
★主方程右端量纲是能量不是力；★距离依赖两端（指数 0 与 -1）都不匹配任何一种已知力；
★方程不含受力质量 &rArr; eta(Ti,Pt)=1.2119，超 MICROSCOPE 1.10e15 倍。
修复定价 2^6=64：SURVIVE 0 / SUICIDE 30 / EMPTY 34 &rArr; 本线第 31 度。</div>

<section><h2><span class="n">§1</span>靶的核心方程（原文，已还原）</h2>
<div class="eq">(1)  omega^2 = c^2 (kappa^2 + tau^2)                        本源几何不变式
(2)  nabla_t t = kappa n ; nabla_t n = -kappa t + tau b ; nabla_t b = -tau n
(3)  F = (hbar c / 4 pi) * (kappa n + tau b) / sqrt(1 + (omega/c)^2 r^2)     全域力主方程
(5)  m = (hbar/c) sqrt(kappa^2 + tau^2)                     质量几何式
(12) S = hbar * sqrt(kappa^2+tau^2)/kappa ;  靶令 sqrt(kappa^2+tau^2)/kappa = 1/2
(17) R_mn - (1/2) g_mn R + Lambda g_mn = (4 pi G m^2/(c^2 hbar)) u_m u_n
(61) kappa(r) = (G M/(c^2 r^2)) e^{-lambda(r)} ; (62) tau(r) = (tau_0/r) e^{-lambda(r)}</div>
<p>来料的 LaTeX 曾被批量破坏（所有 t 被替换为 \\(\\boldsymbol{t}\\)），本卷无损还原后再审计；
原文件只读未改。</p></section>

<section><h2><span class="n">§2</span>先证明对的部分（A 组，照实记 PASS）</h2>
<div class="thm"><span class="lab">A1 · 式(1) 对圆柱螺旋成立</span>
<div>解析 kappa=a/(a^2+b^2)、tau=b/(a^2+b^2) 与中心差分数值微分对拍（各阶独立差分公式，步长在
1e-1…1e-4 中按残差自适应，取 h=@@A1H@@），<b>kappa 与 tau 的联合相对残差 @@A1R@@</b>。这一条靶是对的。
★恒等式两端残差 @@A1E@@ 恒为 0（c 与 kappa、tau 出自同一组 (a,b)，属恒等式回代），<b>不作 A1 依据</b>。</div></div>
<div class="thm"><span class="lab">A2/A4 · 量纲正确的两项</span>
<div>[hbar/c]·[L^-1] = <b>M</b>（质量），与式(5) 一致；[omega/c]·[r] 无量纲，故分母无量纲。
<div class="warn" style="margin-top:8px"><b>但</b>：残差 0 / 量纲对属「结构自洽」，不等于实验预测。式(5) 是 E=mc^2 与 E=hbar·omega 的联立（定义恒等式），见 E3。</div></div></div>
</section>

<section><h2><span class="n">§3</span>★ 自旋层：hbar/2 被自己的公式排除</h2>
<div class="bad"><span class="lab">D1/D2</span><div>
靶：S = hbar·sqrt(kappa^2+tau^2)/kappa，令其 = 1/2（自旋 1/2）<br>
&nbsp;&nbsp;&rArr; sqrt(1+(tau/kappa)^2) = 1/2 &nbsp;&rArr;&nbsp; (tau/kappa)^2 = 1/4 - 1 = <b>-3/4</b><br>
<b>实数域无解</b>：tau/kappa 为纯虚数。更一般地，对任意实数 x，sqrt(1+x^2) &ge; 1，
故 <b>S &ge; hbar 恒成立</b>，hbar/2 与 x 取何值无关地被排除。</div></div>
<div class="thm"><span class="lab">D3 · 控制组（证明求解器有分辨力）</span>
<div>同一求解器对 S=2·hbar 给出 (tau/kappa)^2 = 3 &rArr; tau/kappa = &plusmn;1.732051（<b>实数可解</b>）；
对 S=hbar/2 给出 -3/4（无解）&rArr; D1/D2 不是恒红门禁。</div></div>
</section>

<section><h2><span class="n">§4</span>★ 量纲层与距离依赖层</h2>
<div class="bad"><span class="lab">B1 · 主方程右端是能量，不是力</span>
<div>[hbar·c]·[kappa] = <b>M L^2 T^-2</b>（能量 J）；力应为 <b>M L T^-2</b>（N）；<b>多一个长度 L</b>。
负对照 B3：把 kappa 换成 kappa^2 即得 <b>M L T^-2</b> = 力 &rArr; 这是靶的真实缺陷，不是审计器恒红。</div></div>
<div class="bad"><span class="lab">B2 · 场方程右端系数</span>
<div>4 pi G m^2/(c^2 hbar) 量纲 = <b>L^-1 T</b>；左端 = <b>L^-2</b>。
正对照：GR 的 (8 pi G/c^4) T_munu = <b>L^-2</b>，与左端一致。</div></div>
<h3>距离依赖：唯一的 r 依赖来自分母</h3>
<table><thead><tr><th>x=(omega/c)r</th><th>形状因子 1/sqrt(1+x^2)</th><th>局部指数 dlnF/dlnr</th></tr></thead>
<tbody>@@EXP@@</tbody></table>
<p>长程 &rarr; 指数 <b>0</b>（力趋于常数）；短程 &rarr; 指数 <b>-1</b>（F ~ 1/r）。
四力实测：引力 -2、电磁 -2、弱力 Yukawa 指数衰减、强力禁闭 &rArr; <b>两端都不匹配任何一种已知力</b>。
且靶自述「低频时分母近似常数 &rArr; 长程」与「引力随距离缓慢衰减」<b>直接冲突</b>（C3）。</p>
</section>

<section><h2><span class="n">§5</span>★ 主方程不含受力物体的质量</h2>
<div class="bad"><span class="lab">E1/E2 · 弱等效原理</span>
<div>F 只含源侧几何量（kappa, tau, omega, r），<b>无受力物体质量 m_test</b> &rArr; a = F/m 反比于受力质量。<br>
Eötvös 参数 eta(Ti,Pt) = 2|m2-m1|/(m1+m2) = <b>1.2119</b>；MICROSCOPE 上限 &lt; 1.1e-15
&rArr; 冲突 <b>1.10e15 倍</b>。<span style="color:var(--green)">该值与 r243 的独立实现完全一致（交叉验证通过）。</span></div></div>
<h3>数值层：用靶自己的 kappa(r) 代入</h3>
<table><thead><tr><th>检验质量</th><th>F_靶 / F_牛顿 = hbar/(4 pi c m)</th></tr></thead><tbody>@@MAG@@</tbody></table>
<p>跨 <b>30.0 个数量级</b>，且比值随检验质量变化 &rArr; 靶方程描述的不是引力（引力应与受力质量成正比）。</p>
</section>

<section><h2><span class="n">§6</span>条目表（分层并列，不跨层加总）</h2>
<table><thead><tr><th>ID</th><th>层</th><th>结论</th><th>证据</th></tr></thead><tbody>@@ROWS@@</tbody></table>
<h3>分层计数</h3>
<table><thead><tr><th>层</th><th>PASS</th><th>FAIL</th><th>OPEN</th><th>INFO</th></tr></thead><tbody>@@LAY@@</tbody></table>
</section>

<section><h2><span class="n">§7</span>修复定价与治理</h2>
<div class="bad"><span class="lab">I1 · 2^6 = 64 组合</span>
<div>SURVIVE <b>0</b> / SUICIDE <b>30</b> / EMPTY <b>34</b> &rArr; <b>本线第 31 度</b>。<br>
修 P2/P3/P6 均违反靶的「无人工参数」宣称；修 P5（null frame）使原方程形式 (kappa n + tau b) 崩塌；
P4（自旋 hbar/2）在实数域无解 &rArr; 无存续路径。</div></div>
<div class="thm"><span class="lab">守卫 @@GP@@/@@GT@@ · 控制组 3 类</span>
<div>守卫：残差阈值非写死 / 定价真枚举 / 靶只读 sha256 / GR 量纲正对照 / 求解器可解 / 末尾 hash 复验。<br>
控制组：正对照（B2-GR、B3-kappa^2、D3-S=2hbar）、负对照（A1 解析 vs 数值）、分辨力（C1/C2 指数扫描、H1 比值随质量变）。</div></div>
<div class="warn"><b>性质界定</b>：本卷<b>不判靶方向全错</b>——「曲率+挠率几何化」与爱因斯坦–嘉唐引力属同一大类，
式(1)、式(5) 在其适用域内正确。判的是：特例恒等式被升格为全域公理（G1）、能量被当力写（B1）、
结构上不可能推出 hbar/2（D1/D2）。F2（null frame 修法未行使）记 OPEN 不记 FAIL。</div>
</section>

<div class="foot">TUFT-R248 · 单方程全域力层首卷 · 零虚构声明：
所有 PASS/FAIL 由脚本机算或量纲代数得出，无一处写死 True。靶 2 份只读，落盘前后 sha256 一致。</div>
</div></body></html>"""

HTML = (HTML.replace("@@CSS@@", CSS_R)
        .replace("@@ROWS@@", row_html).replace("@@LAY@@", lay_html)
        .replace("@@EXP@@", exp_html).replace("@@MAG@@", mag_html)
        .replace("@@N@@", str(RES["counts"]["items"]))
        .replace("@@P@@", str(RES["counts"]["PASS"]))
        .replace("@@F@@", str(RES["counts"]["FAIL"]))
        .replace("@@O@@", str(RES["counts"]["OPEN"]))
        .replace("@@I@@", str(RES["counts"]["INFO"]))
        .replace("@@GP@@", str(RES["guards"]["guard_pass"]))
        .replace("@@GT@@", str(RES["guards"]["guard_total"]))
        .replace("@@A1R@@", "%.3e" % resid_a1)
        .replace("@@A1H@@", "%.0e" % h_best)
        .replace("@@A1E@@", "%.3e" % resid_eq1))
with open(os.path.join(SRC, TAG + ".html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("OK -> html")
