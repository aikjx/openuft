# -*- coding: utf-8 -*-
"""
TUFT-r165｜D5《大统一力方程》四力闭合层卷：κ、τ 是单粒子运动学量，不是场量

00. 编号与定位
  【编号】r165。实测首空号：全仓已占 r148..r164（r159/r160 引力侧与 S17 侧、
         r161–r164 电荷/时空/质量/本源侧，均属并行会话），r165 为首空号。
  【动机】D5 README 靶原文：
     「三重奏是统一力框架的**几何基石**（已严格证明），但本身不是"万有理论"——
       它不解释引力、不生成常数、不完成四力统一（见 A4 开放问题）。」
     字典：「κ² + τ² = (ω/v)² = (qB/(γ m v))²  （匀速螺旋 / 梯度磁场）」
  靶**自承**「不完成四力统一」（= 没做）。但靶没有自承、且前 16 卷从未判过的是：
  在现有字典下**能不能**做。本卷判三问：
    (i)   κ、τ 是「场量」还是「单粒子轨迹量」？（同点、同相互作用、异速度）
    (ii) 由 κ、τ 反演相互作用是否欠定？（κ 是 (r, v) 的二元函数）
    (iii) 三重奏的解空间多大？（1 方程 2 未知 ⇒ 两种力如何分工）

01. ★分层声明（与既有卷条目不可相加）
  r148 式子层 · r151–r153 式组/读法层 · r154 后果层 · r155 动力学层 ·
  r156 场论层 · r157 动力学积分层 · r158 字典层 · r159 引力侧还原（并行线）
  **本卷 = 四力闭合层（κ、τ 凭什么能承载相互作用）**
  与 r158 的区别：r158 判「ω 与 qB/(γm) 的同一性」；本卷判
  「κ、τ 这两个几何量的**载体身份**」——是场的量还是轨迹的量。

02. 机读手段
  全部**解析**构造（κ=|v×a|/v³、τ=(v×a)·j/|v×a|²），不用有限差分；
  开普勒中心力轨道闭式（r=p/(1+e cosφ)、径向加速度 −k/r²、
  加飙升 2kṙ/r³ r̂ − k φ̇/r² θ̂）；量纲四元组 (M,L,T,Q)；
  幂次穷举 [−3,3]^7；控制组 6 项；守卫 8 项；修复算子 {KEEP,DEL,REPLACE}。

03. 不自推声明
  NS1 不替靶补「κ 对应哪种力」的映射；不替靶选常数；不修改靶任何字节。
  NS2 不重判 r148–r164 任何结论（分层铁律）。
  NS3 只判 D5 的 Frenet 字典，**不判** S02 公设层的其它通道
      （κ₃ / 非度规性 / 四力重述属 S02 不属 D5）。

04. 红线
  数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容；成立 ≠ 宣称域无边界；
  **靶自承优先**：靶已自承「不完成四力统一」，本卷不得把「没做」当发现，
  本卷的发现只能是「**结构上做不成**」及其机器证据。
"""

import io
import json
import math
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ============================================================
# 常数（CODATA 2018 / SI）
# ============================================================
Q_E = 1.602176634e-19
M_E = 9.1093837015e-31
C_L = 299792458.0
B0 = 1.0

# ============================================================
# 路径
# ============================================================
BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "数据")
STEM = "TUFT-r165_D5四力闭合层_单粒子运动学量与源依赖冲突_2026-10-24"

# ============================================================
# 登记器
# ============================================================
ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append({"id": iid, "title": title, "status": status,
                  "note": note, "metrics": metrics})


def control(cid, desc, value, expect, ok):
    CONTROLS.append({"id": cid, "desc": desc, "value": value,
                     "expect": expect, "ok": bool(ok)})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def fv(x):
    try:
        return "%.6e" % float(x)
    except Exception:
        return str(x)


def fs(x, n=6):
    try:
        return "%.*e" % (n, float(x))
    except Exception:
        return str(x)


# ============================================================
# 量纲工具 (M, L, T, Q)（相乘 = 指数相加）
# ============================================================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * n for x in a)


D_LEN = (0, 1, 0, 0)
D_TIME = (0, 0, 1, 0)
D_MASS = (1, 0, 0, 0)
D_CHG = (0, 0, 0, 1)
D_KAPPA = (0, -1, 0, 0)
D_OMEGA = (0, 0, -1, 0)
D_VEL = ddiv(D_LEN, D_TIME)
D_BFIELD = (1, 0, -1, -1)
D_FORCE = (1, 1, -2, 0)
D_POT = (1, 2, -2, 0)


def dim_check():
    ok1 = dmul(D_MASS, (0, 1, -2, 0)) == D_FORCE                 # ma = F
    ok2 = dmul(D_CHG, ddiv(D_BFIELD, D_MASS)) == D_OMEGA         # qB/m = T^-1
    ok3 = dpow(ddiv(D_OMEGA, D_VEL), 2) == dpow(D_KAPPA, 2)      # (ω/v)² = κ²
    ok4 = dpow(D_KAPPA, -2) == (0, 2, 0, 0)                      # 1/κ² = L²
    return ok1 and ok2 and ok3 and ok4


# ============================================================
# 矢量工具
# ============================================================
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def nrm(a):
    return math.sqrt(dot(a, a))


def frenet(v, a, j):
    """由解析的 v, a, j 构造 Frenet 不变量（无差分）。"""
    cr = cross(v, a)
    m = nrm(cr)
    vn = nrm(v)
    if m == 0.0 or vn == 0.0:
        return 0.0, 0.0
    k = m / (vn ** 3)
    t = dot(cr, j) / (m * m)
    return k, t


def rel(x, y):
    m = max(abs(x), abs(y))
    if m == 0.0:
        return 0.0
    return abs(x - y) / m


# ============================================================
# 开普勒中心力轨道（闭式；k>0 吸引，a_vec = −k/r² r̂）
# ============================================================
def kepler_state(k, p, e, phi):
    """返回 (r, v3, a3, j3, v_tan)。比角动量 h=sqrt(k p)。"""
    h = math.sqrt(k * p)
    den = 1.0 + e * math.cos(phi)
    r = p / den
    drdphi = p * e * math.sin(phi) / (den * den)
    phidot = h / (r * r)
    rdot = drdphi * phidot
    cs, sn = math.cos(phi), math.sin(phi)
    rh = (cs, sn, 0.0)
    th = (-sn, cs, 0.0)
    v3 = (rdot * rh[0] + r * phidot * th[0],
          rdot * rh[1] + r * phidot * th[1],
          0.0)
    a3 = tuple(-(k / (r * r)) * rh[i] for i in range(3))
    j3 = (2.0 * k * rdot / (r ** 3) * rh[0] - k * phidot / (r * r) * th[0],
          2.0 * k * rdot / (r ** 3) * rh[1] - k * phidot / (r * r) * th[1],
          0.0)
    return r, v3, a3, j3, r * phidot


def kappa_tan(k, r, v_tan):
    """速度 ⊥ 径向处的曲率：κ = (k/r²)/v²。"""
    return (k / (r * r)) / (v_tan * v_tan)


# ============================================================
# A 组 · κ 是场量还是轨迹量？（同点、同相互作用、异速度）
# ============================================================
R0 = 1.0e6
K_CP = 1.0
V_LIST = [1.0e3, 2.0e3, 4.0e3]


def group_a():
    rows = []
    for v in V_LIST:
        vv = (0.0, v, 0.0)
        aa = (-K_CP / (R0 * R0), 0.0, 0.0)
        k, t = frenet(vv, aa, (0.0, 0.0, 0.0))
        rows.append({"v": v, "kappa": k, "tau": t,
                     "acc": K_CP / (R0 * R0),
                     "kappa_v2": k * v * v,
                     "kappa_ratio_to_first": k / rows[0]["kappa"] if rows else 1.0})
    return rows


# ============================================================
# B 组 · κ 是 (r, v) 的二元函数 ⇒ 反演欠定
# ============================================================
KAPPA_STAR = 1.0e-12
B_VS = [1.0e3, 2.0e3, 4.0e3]


def group_b():
    rows = []
    for v in B_VS:
        r = math.sqrt(K_CP / (KAPPA_STAR * v * v))
        kb = kappa_tan(K_CP, r, v)
        rows.append({"v": v, "r": r, "kappa_back": kb,
                     "res": rel(kb, KAPPA_STAR), "rho": 1.0 / kb})
    return rows


# ============================================================
# C 组 · 三重奏解空间：1 方程 2 未知 ⇒ 欠定 1 维
# ============================================================
THETAS = [0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0,
          210.0, 240.0, 270.0, 300.0, 330.0]
OMEGA_V = 1.0e-8


def group_c():
    rows = []
    for th in THETAS:
        t = math.radians(th)
        kap = OMEGA_V * math.cos(t)
        tau = OMEGA_V * math.sin(t)
        rows.append({"theta": th, "kappa": kap, "tau": tau,
                     "lhs": kap * kap + tau * tau,
                     "rhs": OMEGA_V * OMEGA_V,
                     "res": rel(kap * kap + tau * tau, OMEGA_V * OMEGA_V)})
    return rows


# ============================================================
# D 组 · 开普勒椭圆：ρ/r = 1 − e cosφ（仅圆轨道 ≡ r）
# ============================================================
P_SMA = 1.0
ECC = 0.6
PHIS = [0.0, 45.0, 90.0, 135.0, 180.0]


def rho_over_r_closed(k, p, e, phi):
    """开普勒轨道 ρ/r 的**正确**闭式：ρ/r = p(u²+u'²)^{3/2}/u²，
    u=(1+e cosφ)/p、u'=−e sinφ/p（由 κ=u³(u+u'')/(u²+u'²)^{3/2} 与 u+u''≡1/p 推出）。"""
    u = (1.0 + e * math.cos(phi)) / p
    up = -e * math.sin(phi) / p
    s = u * u + up * up
    return p * (s ** 1.5) / (u * u)


def group_d():
    rows = []
    for ph in PHIS:
        r, v3, a3, j3, v_tan = kepler_state(K_CP, P_SMA, ECC, math.radians(ph))
        k, t = frenet(v3, a3, j3)
        rho = 1.0 / k if k > 0 else float('inf')
        pred = rho_over_r_closed(K_CP, P_SMA, ECC, math.radians(ph))
        rows.append({"phi": ph, "r": r, "v": nrm(v3), "kappa": k, "rho": rho,
                     "rho_over_r": rho / r, "tau": t,
                     "pred": pred, "res_pred": rel(rho / r, pred),
                     "naive": 1.0 - ECC * math.cos(math.radians(ph)),
                     "res_naive": rel(rho / r, 1.0 - ECC * math.cos(math.radians(ph)))})
    return rows


def group_d_circle():
    """控制组：e=0 圆轨道，ρ/r 应恒为 1。"""
    rows = []
    for ph in PHIS:
        r, v3, a3, j3, v_tan = kepler_state(K_CP, P_SMA, 0.0, math.radians(ph))
        k, t = frenet(v3, a3, j3)
        rows.append({"phi": ph, "r": r, "kappa": k, "tau": t,
                     "rho_over_r": (1.0 / k) / r if k > 0 else float('inf')})
    return rows


# ============================================================
# E 组 · 出口存在性：改用「相对运动」字典即可携带源信息
# ============================================================
def group_e():
    rows = []
    for m2 in (M_E, 10.0 * M_E, 100.0 * M_E):
        mu = M_E * m2 / (M_E + m2)
        r = R0
        v_tan = math.sqrt(K_CP / r)
        acc = K_CP / (mu * r * r)
        kap = acc / (v_tan * v_tan)
        rows.append({"m2_over_m1": m2 / M_E, "mu_over_m1": mu / M_E,
                     "kappa_rel": kap, "rho_rel": 1.0 / kap})
    return rows


# ============================================================
# F 组 · 框架量表穷举：能否凑出含「源/距离」依赖的力或势
# ============================================================
FRAME_QTY = [("kappa", D_KAPPA), ("tau", D_KAPPA), ("omega", D_OMEGA),
             ("v", D_VEL), ("c", D_VEL), ("m", D_MASS), ("q", D_CHG)]


def group_f():
    """幂次 [−3,3]^7 穷举：满足 [F]/[U] 的组合族数（r 不在基组 ⇒ r 指数恒 0）。"""
    exps = range(-3, 4)
    hits_f = []
    hits_u = []
    total = 0
    for a0 in exps:
        for a1 in exps:
            for a2 in exps:
                for a3 in exps:
                    for a4 in exps:
                        for a5 in exps:
                            for a6 in exps:
                                total += 1
                                # M=a5；L=−a0−a1+a3+a4；T=−a2−a3−a4；Q=a6
                                d = (a5, -a0 - a1 + a3 + a4,
                                     -a2 - a3 - a4, a6)
                                if d == D_FORCE:
                                    hits_f.append((a0, a1, a2, a3, a4, a5, a6))
                                elif d == D_POT:
                                    hits_u.append((a0, a1, a2, a3, a4, a5, a6))
    return total, hits_f, hits_u


# ============================================================
# 主流程
# ============================================================
def main():
    a_rows = group_a()
    b_rows = group_b()
    c_rows = group_c()
    d_rows = group_d()
    d_circ = group_d_circle()
    e_rows = group_e()
    total, hits_f, hits_u = group_f()

    # ---------- 假 ω 判别力（承 r158 控制组项）：Ω′ = Ω/2 ⇒ 残差恒 0.75 ----------
    # 自抓：首版硬编码 0.75 且标注 Ω′=2Ω（2Ω 应给 rel(x,4x)=3.0）；
    #       现改为从 c_rows 现算，标签同步改为 Ω/2。
    disc_res = rel(c_rows[0]["lhs"], (OMEGA_V / 2.0) ** 2)

    # ---------- 关键汇总量 ----------
    kv2 = [r["kappa_v2"] for r in a_rows]
    kv2_spread = (max(kv2) - min(kv2)) / max(kv2) if max(kv2) else 0.0
    accs = [r["acc"] for r in a_rows]
    acc_spread = (max(accs) - min(accs)) / max(accs) if max(accs) else 0.0
    k_ratio = a_rows[-1]["kappa"] / a_rows[0]["kappa"]
    r_span = max(r["r"] for r in b_rows) / min(r["r"] for r in b_rows)
    ror = [r["rho_over_r"] for r in d_rows]
    ror_span = max(ror) / min(ror)
    closed_span = (max(r["pred"] for r in d_rows)
                   / min(r["pred"] for r in d_rows))
    pred_dev = max(r["res_pred"] for r in d_rows)
    naive_dev = max(r["res_naive"] for r in d_rows)
    circ_dev = max(abs(r["rho_over_r"] - 1.0) for r in d_circ)
    c_res = max(r["res"] for r in c_rows)
    e_span = e_rows[-1]["kappa_rel"] / e_rows[0]["kappa_rel"]

    # ---------- 条目 ----------
    add("A1", "κ 不是场量：同点、同相互作用、异速度 ⇒ κ ∝ 1/v²", "FAIL",
        "若 κ 是相互作用强度的几何化身，则同一点的 κ 应唯一；机读显示 κ 随粒子"
        "速率改变（κ(2v)/κ(v)=%.6f=1/4，κ(4v)/κ(v)=%.6f=1/16），"
        "而该点的加速度三点严格相同（离散度 %.1e）⇒ κ 不是场的函数。"
        % (a_rows[1]["kappa"] / a_rows[0]["kappa"],
           a_rows[2]["kappa"] / a_rows[0]["kappa"], acc_spread),
        kappa_v2_spread=kv2_spread, acc_spread=acc_spread,
        k_ratio_2v=k_ratio, k_ratio_4v=a_rows[2]["kappa"] / a_rows[0]["kappa"])

    add("A2", "本组 τ 恒 0（j 指定为 0）⇒ 该组不判 τ", "INFO",
        "τ 的计算需要加飙升 j，而「同一点任意指定速度」不给 j；本组只判 κ，"
        "τ 的同点异速检验未做（未做即未证）。", tau_all_zero=all(r["tau"] == 0.0 for r in a_rows))

    add("B1", "由 κ 反演距离欠定：同一 κ* 对应 r 跨 %.1f 倍" % r_span, "FAIL",
        "κ = (k/r²)/v² 是 (r, v) 的二元函数；固定 κ*=%s，v=1e3/2e3/4e3 分别给 "
        "r=%.6g/%.6g/%.6g（三点反演残差 %.1e）⇒ 给定 κ 有无穷多 (r,v) 解，"
        "不可能由 κ 单独确定「相互作用有多强、源在哪」。"
        % (fv(KAPPA_STAR), b_rows[0]["r"], b_rows[1]["r"], b_rows[2]["r"],
           max(r["res"] for r in b_rows)),
        r_span=r_span, max_back_res=max(r["res"] for r in b_rows))

    add("B2", "反演欠定的自由度来源：κ 同时依赖 r 与 v", "INFO",
        "κ ∝ r^(−2)·v^(−2)（切向配比下），比「力只是 r 的函数」多一个自由度 ⇒ "
        "κ 不能充当力的化身。", kappa_scaling="r^-2 v^-2")

    add("C1", "三重奏解空间欠定 1 维：1 方程 2 未知", "INFO",
        "κ²+τ²=(ω/v)² 给定 (ω/v) 后解集是 1 参数椭圆族（12 个 θ 全部满足，"
        "最大残差 %.1e）⇒ 「κ 归电磁、τ 归引力」式的分工需要第 2 个独立方程，"
        "框架内不存在。" % c_res, theta_points=len(c_rows), max_res=c_res)

    add("D1", "κ 与距离无固定比例：椭圆轨道 ρ/r 跨 %.4f 倍" % ror_span, "FAIL",
        "开普勒椭圆（e=%.1f）上 ρ/r = p(u²+u'²)^{3/2}/u²，从 %.6f（φ=180°，远心点）"
        "到 %.6f（φ=45°）跨 %.4f 倍；仅当 e=0（圆轨道）才有 ρ≡r（控制组 C2）。"
        "⇒ 「κ ∝ 1/r」只在圆轨道这一零测集上成立。"
        % (ECC, min(ror), max(ror), ror_span),
        rho_over_r_min=min(ror), rho_over_r_max=max(ror), span=ror_span,
        closed_span=closed_span)

    add("D2", "解析闭式与 Frenet 机读一致（判据有分辨力）", "PASS",
        "机读 ρ/r 与**正确**闭式 p(u²+u'²)^{3/2}/u² 最大偏差 %.1e（机器零 ⇒ 工具可信）；"
        "与**错误**式 1−e·cosφ 最大偏差 %.4f（O(1) 量级 ⇒ 判据分得清对错、非恒真）⇒ "
        "D1 来自真实几何而非工具失效。" % (pred_dev, naive_dev),
        max_dev=pred_dev, naive_dev=naive_dev)

    add("E1", "出口存在：改「相对运动」字典即可携带源信息", "PASS",
        "把 Frenet 对象从「单粒子轨迹」换成「两体相对运动」后，κ_rel 随第二体"
        "质量改变（m₂/m₁=1→100 时降至 %.4f 倍）⇒ 源信息可进入几何量；"
        "但这是**换字典对象**（= 换框架），不是修补。" % e_span,
        kappa_rel_span=e_span, rows=len(e_rows))

    add("F1", "框架量表穷举：%d 组中满足 [F] 的 %d 族、[U] 的 %d 族，r 依赖恒 0"
        % (total, len(hits_f), len(hits_u)), "INFO",
        "框架量 {κ,τ,ω,v,c,m,q} 的幂次 [−3,3]^7 穷举：能量纲为力/势的组合"
        "全部与「到源的距离」无关（r 不在基组内，r 指数恒 0）；"
        "源侧唯一入口是 B（经 ω 进入），而 B 在 D5 适用域内是常数。",
        total=total, n_force=len(hits_f), n_pot=len(hits_u))

    add("F2", "靶自承登记（防过度指控）", "BOUNDARY",
        "D5 README 明写「不解释引力、不生成常数、不完成四力统一（见 A4）」"
        "⇒ 本卷**不得**把「四力未闭合」记为本卷发现（那是靶自承）；"
        "本卷的发现是 A1/B1/D1 三条「结构上做不成」的机器证据。")

    add("R1", "修复定价：3 动作枚举", "INFO",
        "KEEP（κ,τ 仍取单粒子轨迹）⇒ A1/B1/D1 依旧成立，修不好；"
        "REPLACE（改取两体相对运动）⇒ E1 显示可行，但字典对象更换 = 换框架，"
        "且三重奏随之退化为相对运动学恒等式；DEL（删掉几何基石角色）⇒ "
        "框架退回标准力学。宣称域内成立 1 / 零代价 0。",
        survive=1, zero_cost=0)

    # ---------- 控制组 ----------
    control("C1", "量纲工具自检（ma=F / qB/m=T^-1 / (ω/v)²=κ² / 1/κ²=L²）",
            str(dim_check()), "True", dim_check())
    control("C2", "圆轨道对照：ρ/r ≡ 1（e=0，5 个相位）",
            "%.3e" % circ_dev, "<1e-9", circ_dev < 1e-9)
    control("C3", "同点同力：三点加速度严格相同（阳性对照）",
            "%.3e" % acc_spread, "<1e-12", acc_spread < 1e-12)
    control("C4", "三重奏参数化恒成立（12 点，判据非恒假）",
            "%.3e" % c_res, "<1e-12", c_res < 1e-12)
    control("C5", "判据分辨力：假 Ω′=Ω/2 ⇒ 残差",
            "%.6f" % disc_res, "0.750000", abs(disc_res - 0.75) < 1e-12)
    control("C6", "平面曲线 τ ≡ 0（椭圆 5 点 + 圆轨道 5 点）",
            "%.3e" % max(max(abs(r["tau"]) for r in d_rows),
                         max(abs(r["tau"]) for r in d_circ)),
            "<1e-15", max(max(abs(r["tau"]) for r in d_rows),
                          max(abs(r["tau"]) for r in d_circ)) < 1e-15)

    # ---------- 守卫 ----------
    guard("G1-κ∝1/v²（三点 κ·v² 恒定）", kv2_spread < 1e-12,
          "spread=%.3e" % kv2_spread)
    guard("G2-阳性对照：同点加速度恒定（机器能分辨）", acc_spread < 1e-12,
          "spread=%.3e" % acc_spread)
    guard("G3-反演欠定：r 跨度 = (v₂/v₁)²", abs(r_span - 4.0) < 1e-9,
          "span=%.6f" % r_span)
    guard("G4-椭圆 ρ/r 跨度 = 闭式跨度", abs(ror_span - closed_span) < 1e-9,
          "span=%.6f closed=%.6f" % (ror_span, closed_span))
    guard("G5-解析 vs Frenet 机读一致", pred_dev < 1e-9,
          "max_dev=%.3e" % pred_dev)
    guard("G6-圆轨道对照 ρ/r ≡ 1", circ_dev < 1e-9,
          "dev=%.3e" % circ_dev)
    guard("G7-穷举族存在且 r 依赖恒 0",
          len(hits_f) > 0 and len(hits_u) > 0,
          "F=%d U=%d / total=%d" % (len(hits_f), len(hits_u), total))
    guard("G8-控制组全部通过", all(c["ok"] for c in CONTROLS),
          "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))

    # ---------- 汇总 ----------
    cnt = {}
    for it in ITEMS:
        cnt[it["status"]] = cnt.get(it["status"], 0) + 1
    allok = all(c["ok"] for c in CONTROLS)
    gallok = all(g["ok"] for g in GUARDS)
    verdict = ("FRENET-QUANTITIES-ARE-SINGLE-PARTICLE-KINEMATICS-NOT-FIELDS"
               "-FOUR-FORCE-CLOSURE-STRUCTURALLY-UNREACHABLE")

    return dict(a_rows=a_rows, b_rows=b_rows, c_rows=c_rows, d_rows=d_rows,
                d_circ=d_circ, e_rows=e_rows, total=total,
                hits_f=len(hits_f), hits_u=len(hits_u),
                kv2_spread=kv2_spread, acc_spread=acc_spread, r_span=r_span,
                ror_span=ror_span, closed_span=closed_span,
                pred_dev=pred_dev, naive_dev=naive_dev, circ_dev=circ_dev,
                c_res=c_res, e_span=e_span, disc_res=disc_res,
                cnt=cnt, allok=allok, gallok=gallok, verdict=verdict,
                controls=CONTROLS, guards=GUARDS, items=ITEMS)


# ============================================================
# 报告 + 判定册 + 落盘
# ============================================================
def report_and_write(R):
    a_rows, b_rows, c_rows = R["a_rows"], R["b_rows"], R["c_rows"]
    d_rows, d_circ, e_rows = R["d_rows"], R["d_circ"], R["e_rows"]
    cnt, allok, gallok = R["cnt"], R["allok"], R["gallok"]
    verdict = R["verdict"]
    CONTROLS, GUARDS, ITEMS = R["controls"], R["guards"], R["items"]

    L = []
    w = L.append
    w("=" * 78)
    w(" TUFT-r165｜D5 四力闭合层：κ、τ 是单粒子运动学量，不是场量")
    w("=" * 78)
    w("")
    w("[A1] 同点（r0=%.3e）、同相互作用（a=%.6e）、异速度 ⇒ κ ∝ 1/v²" % (R0, a_rows[0]["acc"]))
    for r in a_rows:
        w("   v=%-10.4g κ=%.6e  κ·v²=%.6e  τ=%.1e  加速度=%.6e"
          % (r["v"], r["kappa"], r["kappa_v2"], r["tau"], r["acc"]))
    w("")
    w("[B1] 反演欠定：固定 κ*=%s" % fv(KAPPA_STAR))
    for r in b_rows:
        w("   v=%-10.4g ⇒ r=%.6e  ρ=%.6e  反演残差=%.3e"
          % (r["v"], r["r"], r["rho"], r["res"]))
    w("")
    w("[C1] 三重奏解空间：κ²+τ²=(ω/v)² 的 12 点参数化")
    for r in c_rows:
        w("   θ=%-7.1f κ=%.6e τ=%.6e 残差=%.3e"
          % (r["theta"], r["kappa"], r["tau"], r["res"]))
    w("")
    w("[D1] 开普勒椭圆（e=%.1f）：ρ/r = p(u²+u'²)^{3/2}/u²" % ECC)
    for r in d_rows:
        w("   φ=%-7.1f r=%.6e ρ=%.6e ρ/r=%.6f（闭式 %.6f）τ=%.1e"
          % (r["phi"], r["r"], r["rho"], r["rho_over_r"], r["pred"], r["tau"]))
    w("   [圆轨道对照 e=0]")
    for r in d_circ:
        w("   φ=%-7.1f ρ/r=%.6f" % (r["phi"], r["rho_over_r"]))
    w("")
    w("[E1] 出口：两体相对运动字典 ⇒ κ_rel 随 m₂/m₁（1→100）降至 %.4f 倍" % R["e_span"])
    for r in e_rows:
        w("   m₂/m₁=%-8.4g μ/m₁=%.6f κ_rel=%.6e ρ_rel=%.6e"
          % (r["m2_over_m1"], r["mu_over_m1"], r["kappa_rel"], r["rho_rel"]))
    w("")
    w("[F1] 框架量表穷举：total=%d  满足[F]的族=%d  满足[U]的族=%d  r 依赖恒 0"
      % (R["total"], R["hits_f"], R["hits_u"]))
    w("")
    w("[控制组]")
    for c in CONTROLS:
        w("   %s %-46s %-24s %s" % ("OK " if c["ok"] else "BAD", c["desc"],
                                    c["value"], c["expect"]))
    w("")
    w("[守卫]")
    for g in GUARDS:
        w("   %s %s  %s" % ("OK " if g["ok"] else "BAD", g["name"], g["detail"]))
    w("")
    w("[条目] %s" % cnt)
    w("[verdict] %s" % verdict)
    w("[控制组] %d/%d   [守卫] %d/%d"
      % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
         sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    report = "\n".join(L)

    # ============================================================
    # 判定册
    # ============================================================
    m = []
    b = m.append
    b("# 判定册 TUFT-r165｜D5 四力闭合层：κ、τ 是单粒子运动学量，不是场量")
    b("")
    b("- 编号：TUFT-r165")
    b("- 生成时刻：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    b("- 引擎：`源码/%s.py`" % STEM)
    b("- 控制组：%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    b("- 守卫：%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    b("- 条目统计：%s" % "  ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items())))
    b("")
    b("## 00. 分工声明（★ 与既有卷条目不可相加）")
    b("")
    b("| 卷 | 层 | 判的是什么 |")
    b("|----|----|-----------|")
    b("| r148 | 式子层 | P=m(c−v)、F=dP/dt、F_e/F_m=c/v、E=cB |")
    b("| r151–r153 | 式组 / 读法层 | 关系组定标、快度救援 |")
    b("| r154 | 后果层 | 磁矩、静止能量 |")
    b("| r155 | 动力学层 | 束缚力、真空击穿、同步辐射 |")
    b("| r156 | 场论层 | 作用量、电荷环流、Frank 分解 |")
    b("| r157 | 动力学积分层 | 真实洛伦兹积分、成立域 λ*、ω 四口径 |")
    b("| r158 | 字典层 | ω 凭什么等于 qB/(γm) |")
    b("| **r165** | **四力闭合层** | **κ、τ 凭什么能承载相互作用** |")
    b("")
    b("## 01. 判词")
    b("")
    b("`%s`" % verdict)
    b("")
    b("**D5 把 κ、τ（轨迹 Frenet 不变量）指派为「统一力框架的几何基石」，但这两个量")
    b("只由单粒子自身运动状态 (v, a, j) 决定：同一点、同相互作用下，粒子速率改变即使 κ")
    b("按 1/v² 改变（κ(2v)/κ(v)=1/4），而该点的加速度三点严格相同 ⇒ κ 不是场的函数；")
    b("且 κ 是 (r, v) 的二元函数，固定一个 κ 值对应无穷多组 (r, v)（r 跨 4 倍），")
    b("不可能由 κ 反推「源在哪、相互作用有多强」。⇒ 几何基石承载四力统一在现有字典下")
    b("结构上不可行——不是「尚未做」（靶已自承未做），而是「这么做不成」。**")
    b("")
    b("## 02. 核心结论")
    b("")
    b("### 2.1 κ 不是场量（A1，本卷唯一的硬 FAIL）")
    b("")
    b("| v (m/s) | κ | κ·v² | 该点加速度 |")
    b("|---|---|---|---|")
    for r in a_rows:
        b("| %-10.4g | %.6e | %.6e | %.6e |"
          % (r["v"], r["kappa"], r["kappa_v2"], r["acc"]))
    b("")
    b("- κ·v² 三点离散度 **%.1e**（机器零）⇒ κ ∝ 1/v² 精确成立；" % R["kv2_spread"])
    b("- 同点加速度三点离散度 **%.1e**（机器零）⇒ **阳性对照**：机器分得清「力相同、κ 不同」；"
      % R["acc_spread"])
    b("- ⇒ 若 κ 是相互作用强度的几何化身，同一点的 κ 应唯一；事实相反 ⇒ κ 不是场量。")
    b("")
    b("### 2.2 反演欠定（B1）")
    b("")
    b("| v (m/s) | 反解 r | ρ=1/κ | 反演残差 |")
    b("|---|---|---|---|")
    for r in b_rows:
        b("| %-10.4g | %.6e | %.6e | %.3e |"
          % (r["v"], r["r"], r["rho"], r["res"]))
    b("")
    b("- 固定 κ*=%s：v=1e3/2e3/4e3 分别给 r=%.6g/%.6g/%.6g，**r 跨 %.1f 倍**"
      "（=(v₂/v₁)²），三点反演残差 %.1e；" % (fv(KAPPA_STAR), b_rows[0]["r"],
                                        b_rows[1]["r"], b_rows[2]["r"],
                                        R["r_span"], max(r["res"] for r in b_rows)))
    b("- κ ∝ r^(−2)·v^(−2) ⇒ 比「力只是 r 的函数」多一个自由度 ⇒ 不能充当力的化身。")
    b("")
    b("### 2.3 κ 与距离无固定比例（D1）")
    b("")
    b("| φ（度） | r | ρ | ρ/r | 闭式 p(u²+u'²)^{3/2}/u² |")
    b("|---|---|---|---|---|")
    for r in d_rows:
        b("| %-7.1f | %.6e | %.6e | %.6f | %.6f |"
          % (r["phi"], r["r"], r["rho"], r["rho_over_r"], r["pred"]))
    b("")
    b("- 机读 ρ/r 与**正确**闭式最大偏差 **%.1e**（机器零 ⇒ 工具可信）；"
      "与**错误**式 1−e·cosφ 最大偏差 **%.4f**（O(1) ⇒ 判据有分辨力，D2）；"
      % (R["pred_dev"], R["naive_dev"]))
    b("- ρ/r 从 **%.6f**（φ=180°，远心点）到 **%.6f**（φ=45°）跨 **%.4f 倍**"
      "（闭式跨度 %.4f，逐位一致）；"
      % (min(r["rho_over_r"] for r in d_rows), max(r["rho_over_r"] for r in d_rows),
         R["ror_span"], R["closed_span"]))
    b("- 圆轨道对照（e=0）：ρ/r ≡ 1（偏差 %.1e，控制组 C2）⇒ 「κ ∝ 1/r」"
      "只在圆轨道这一零测集上成立。" % R["circ_dev"])
    b("")
    b("### 2.4 三重奏解空间欠定（C1）")
    b("")
    b("- 1 个标量方程、2 个未知量 ⇒ 给定 (ω/v) 后解集是 **1 参数椭圆族**")
    b("  （12 个 θ 全部满足，最大残差 %.1e）；" % R["c_res"])
    b("- 「κ 归电磁、τ 归引力」式的分工需要**第 2 个独立方程**，框架内不存在。")
    b("")
    b("### 2.5 出口存在但等于换框架（E1）")
    b("")
    b("| m₂/m₁ | μ/m₁ | κ_rel | ρ_rel |")
    b("|---|---|---|---|")
    for r in e_rows:
        b("| %-8.4g | %.6f | %.6e | %.6e |"
          % (r["m2_over_m1"], r["mu_over_m1"], r["kappa_rel"], r["rho_rel"]))
    b("")
    b("- 改用**两体相对运动**作 Frenet 对象后，κ_rel 随 m₂/m₁（1→100）**降至 %.4f 倍**"
      "⇒ 源信息可以进入几何量；" % R["e_span"])
    b("- 但这是**更换字典对象**（= 换框架），且更换后三重奏退化为相对运动学恒等式。")
    b("")
    b("### 2.6 框架量表穷举（F1）")
    b("")
    b("- 框架量 {κ, τ, ω, v, c, m, q} 幂次 [−3,3]⁷ 共 **%d** 组；" % R["total"])
    b("- 量纲为力 [F]=MLT⁻² 的 **%d** 族、为势 [U]=ML²T⁻² 的 **%d** 族；"
      % (R["hits_f"], R["hits_u"]))
    b("- **r（到源的距离）不在基组内 ⇒ 全部族的 r 指数恒 0**；源侧唯一入口是 B")
    b("  （经 ω 进入），而 B 在 D5 适用域内是常数 ⇒ 无力律的距离/力程依赖。")
    b("")
    b("## 03. 修复定价")
    b("")
    b("| 动作 | 宣称域内成立 | 代价 |")
    b("|---|---|---|")
    b("| KEEP（κ,τ 仍取单粒子轨迹） | 否 | A1/B1/D1 依旧成立 ⇒ 修不好 |")
    b("| REPLACE（改取两体相对运动） | 是 | 字典对象更换 = 换框架；三重奏退化为相对运动学恒等式 |")
    b("| DEL（删掉几何基石角色） | 是 | 框架退回标准力学（承 r148 E2） |")
    b("")
    b("- 宣称域内成立 **1** 个、**零代价 0** 个 ⇒ **修复可行 ≠ 修复后仍有内容**")
    b("  （「修复即自杀」同型结构第九次登记）。")
    b("")
    b("## 04. 靶自承与防过度指控（F2）")
    b("")
    b("- D5 README 明写「不解释引力、不生成常数、**不完成四力统一**（见 A4 开放问题）」；")
    b("  ⇒ 本卷**不得**把「四力未闭合」记为本卷发现，那是靶自承。")
    b("- 本卷的发现仅限三条**结构性**机器证据：κ 不是场量（A1）、")
    b("  由 κ 反演欠定（B1）、κ 与距离无固定比例（D1）。")
    b("- 本卷**不判** S02 公设层的其它通道（κ₃ / 非度规性 / 四力重述）——")
    b("  那些属 S02 公设层，不属 D5 的 Frenet 字典。")
    b("")
    b("## 05. 未闭合项（未做即未证，不得外推）")
    b("")
    b("1. A 组指定 j=0，故该组只判 κ、未判 τ 的「同点异速」行为。")
    b("2. 反演欠定只在「速度 ⊥ 径向」配比下给出闭式 κ=(k/r²)/v²；")
    b("   一般配比下 κ = a_n/v²，其中 a_n 依赖速度方向，结论（二元函数）不变但闭式不同。")
    b("3. 场模型为理想开普勒 1/r² 中心力；强力程/弱力程未纳入 F1 穷举（无 λ 量）。")
    b("4. 修复空间是低阶（3 动作）；新增型算子（改函数形式 / 改向量结构）未枚举。")
    b("5. 本卷**不宣称** D5 / S02 体系被完全证伪 —— 只判决几何基石角色的载体身份。")
    b("")
    b("## 06. 自抓与更正（本卷自身缺陷）")
    b("")
    b("1. **占位文件首次 write 未落盘**（工具长中文参数静默失败）⇒ 改为")
    b("   「短 write_to_file 建占位 + 多次 replace_in_file 填哨兵」的两段式；")
    b("   本轮实际还发生「补全段与既有内容交错成双机器段」⇒ 以「截断 + 外部补全」")
    b("   收口（交错段已整块移除，未改动既有判定文字）。")
    b("")
    b("2. **D2 文案自抓（已修）**：首版把解析式误标为 1−e·cosφ——该式在 φ=0° 给")
    b("   1−e（真值 1+e，符号反）、φ=90° 给 1（真值 (1+e²)^{3/2}，结构亦错）；")
    b("   正确闭式为 p(u²+u'²)^{3/2}/u²（Binet u=1/r 口径）。D2 已升级为双侧判别：")
    b("   正确式机器零 + 错误式 O(1) 偏差（见条目 D2 与控制组 C2/C5）。")
    b("")
    b("3. **C5 自抓（已修）**：假 ω 残差首版硬编码 0.75 且标注 Ω′=2Ω")
    b("   （Ω′=2Ω 应给 rel(x, 4x)=3.0）；现改为从 c_rows 现算，标签改为 Ω′=Ω/2。")
    b("")
    b("4. **group_f 量纲公式自抓（已修）**：消息草稿版的手写维度元组与量表实际维度")
    b("   不符（M 分量写成 a0+a1+a2+a4+a5）；磁盘版已就地改为正确口径")
    b("   （M=a5；L=−a0−a1+a3+a4；T=−a2−a3−a4；Q=a6），穷举读数 F=182 / U=177。")
    b("")
    b("5. **存量产物校准**：数据目录曾存在一版 6/8 守卫的旧跑产物（当时 ρ/r 仍用")
    b("   错误式，G4/G5 报 BAD）——已由本跑覆盖重写，旧读数不得再引用。")
    b("")
    b("## 07. 修复定价 recap 与出口")
    b("")
    b("- KEEP（κ,τ 仍取单粒子轨迹）⇒ A1/B1/D1 依旧成立，修不好；")
    b("- REPLACE（改取两体相对运动）⇒ E1 显示可行，但字典对象更换 = 换框架，")
    b("  且更换后三重奏退化为相对运动学恒等式；")
    b("- DEL（删掉几何基石角色）⇒ 框架退回标准力学。")
    b("- ⇒ 宣称域内成立 **1** 个、**零代价 0** 个 ⇒ 修复可行 ≠ 修复后仍有内容。")
    b("")
    b("## 08. 未闭合项与红线")
    b("")
    b("- 未闭合：① A 组指定 j=0，τ 的「同点异速」未判（未做即未证）；")
    b("  ② 反演闭式 κ=(k/r²)/v² 只在「速度 ⊥ 径向」配比下给出；")
    b("  ③ 场模型为理想开普勒 1/r² 中心力，强力程/弱力程未纳入穷举（表内无 λ 量）；")
    b("  ④ 修复空间只枚举 3 个低阶动作；⑤ 不宣称 D5/S02 被完全证伪。")
    b("- 红线：数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容；成立 ≠ 宣称域无边界；")
    b("  靶自承优先（不把「没做」当发现）；降级一条旧结论 ≠ 该方向被否证。")
    b("")

    # ============================================================
    # 落盘：json / 数据 md / 判定册 md / 运行报告 txt
    # ============================================================
    os.makedirs(OUT, exist_ok=True)
    jp = os.path.join(OUT, STEM + ".json")
    dp = os.path.join(OUT, STEM + ".md")
    vp = os.path.join(OUT, "判定_" + STEM + ".md")
    rp = os.path.join(OUT, STEM + "_report.txt")

    key_numbers = {
        "kappa_ratio_2v": a_rows[1]["kappa"] / a_rows[0]["kappa"],
        "kappa_ratio_4v": a_rows[2]["kappa"] / a_rows[0]["kappa"],
        "kappa_v2_spread": R["kv2_spread"],
        "acc_spread": R["acc_spread"],
        "r_span_fixed_kappa": R["r_span"],
        "rho_distinct": len(set(repr(r["rho"]) for r in b_rows)),
        "theta_points": len(c_rows),
        "c_max_res": R["c_res"],
        "rho_over_r_min": min(r["rho_over_r"] for r in d_rows),
        "rho_over_r_max": max(r["rho_over_r"] for r in d_rows),
        "rho_over_r_span": R["ror_span"],
        "closed_span": R["closed_span"],
        "pred_dev_correct": R["pred_dev"],
        "pred_dev_naive": R["naive_dev"],
        "circle_dev": R["circ_dev"],
        "e_span": R["e_span"],
        "f_total": R["total"], "f_force": R["hits_f"], "f_pot": R["hits_u"],
        "disc_res": R["disc_res"],
    }
    payload = {
        "volume": "TUFT-r165",
        "title": "D5 四力闭合层：κ、τ 是单粒子运动学量，不是场量",
        "date": "2026-10-24",
        "engine": "源码/" + STEM + ".py",
        "stats": cnt,
        "verdict": verdict,
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": key_numbers,
        "not_closed": [
            "A 组指定 j=0，τ 的同点异速行为未判（未做即未证）。",
            "反演闭式 κ=(k/r²)/v² 只在速度 ⊥ 径向配比下给出。",
            "场模型为理想开普勒 1/r² 中心力；强力程/弱力程未纳入穷举。",
            "修复空间只枚举 3 个低阶动作；改函数形式/改向量结构未枚举。",
            "不宣称 D5/S02 被完全证伪——只判决几何基石角色的载体身份。",
        ],
        "redline": [
            "数学自洽 ≠ 实验证实。",
            "恒等式成立 ≠ 有新内容。",
            "成立 ≠ 宣称域无边界。",
            "靶自承优先：不把『没做』当发现。",
            "降级一条旧结论 ≠ 该方向被否证。",
        ],
    }
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    with open(vp, "w", encoding="utf-8") as f:
        f.write("\n".join(m))
    with open(rp, "w", encoding="utf-8") as f:
        f.write(report)

    d = []
    d.append("# 数据 TUFT-r165｜D5 四力闭合层关键读数")
    d.append("")
    d.append("- 判词：`%s`" % verdict)
    d.append("- 条目：%s" % "  ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items())))
    d.append("- 控制组 %d/%d ｜ 守卫 %d/%d" % (
        sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
        sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    d.append("")
    d.append("| 读数 | 值 |")
    d.append("|---|---|")
    for kk, vv in key_numbers.items():
        d.append("| %s | %s |" % (kk, vv))
    with open(dp, "w", encoding="utf-8") as f:
        f.write("\n".join(d))

    print(report)
    print("")
    print("[产物] " + os.path.basename(jp))
    print("[产物] " + os.path.basename(dp))
    print("[产物] " + os.path.basename(vp))
    print("[产物] " + os.path.basename(rp))
    print("[控制组] %d/%d  [守卫] %d/%d" % (
        sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
        sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    print("[退出码] %d" % (0 if (allok and gallok) else 2))
    return 0 if (allok and gallok) else 2


if __name__ == "__main__":
    sys.exit(report_and_write(main()))
