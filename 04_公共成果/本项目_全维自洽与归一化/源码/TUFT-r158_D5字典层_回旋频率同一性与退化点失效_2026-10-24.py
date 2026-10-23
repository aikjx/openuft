# -*- coding: utf-8 -*-
"""
TUFT-r158｜D5《大统一力方程》字典层卷：ω=qB/(γm) 与三重奏 ω 的同一性 · 退化点失效 · E×B 漂移边界 · 新增性定价

================================================================================
00. 编号与定位
================================================================================
【编号】r158。实测首空号：全仓已占 r31..r157（r156 为同日并行会话《v总等于c第二三步》占位，
        r157 为本线 D5 闭合卷），r158 为首空号。

【动机：靶的「字典」声明从未被判过】
  D5 README 原文：
      「其回旋频率 `ω = qB/(γm)` 正是三重奏中的 ω（见 P1 洛伦兹力字典）。因此：
        κ² + τ² = (ω/v)² = (qB/(γ m v))²    （匀速螺旋 / 梯度磁场）」
  这条把**动力学的回旋频率**与**几何的螺旋角速率**认定为同一个 ω，是把电磁学内容
  接进几何恒等式的**唯一接口**（下称「字典声明」）。
  前序五卷全部**预设**了该接口成立，从未判它本身：
    r148 式子层（P=m(c−v) 极限）· r151/r152 式组层 · r153 读法层 · r154 后果层 ·
    r155 动力学层（束缚力/真空击穿/同步辐射）· r157 动力学积分层（真实洛伦兹积分、成立域 λ*）。
  本卷判的正是这个**被所有人预设的接口**：
    (i) 它在严格意义上成立吗？（纯磁场螺旋：精确成立）
    (ii) 成立时承载了什么？（等价性：它就是回旋半径公式 ρ=γmv⊥/(qB) 的代数重排 ⇒ 零新增）
    (iii) 它在宣称域的**退化点**（v⊥ ≡ 0，即 v ∥ B）还成立吗？（失效，且是极限不连续）
    (iv) 磁场为零、纯电场偏转时呢？（字典给 ω=0 ⇒ 断言「曲率为零」，与实际偏转矛盾）
    (v) 有电场漂移（E×B）时呢？（实验室系失效，唯一救法是改口径用漂移系速度）

================================================================================
01. ★分层声明（与既有卷条目不可相加）
================================================================================
  r148  = 式子层（P=m(c−v) / F=dP/dt / F_e/F_m=c/v / E=cB）
  r151–r153 = 式组与读法层
  r154  = 后果层（磁矩 / 静止能量）
  r155  = 动力学层（束缚力 / 真空击穿 / 同步辐射）
  r157  = 动力学积分层（真实洛伦兹积分 / 成立域 λ* / **ω 四口径哪个能救**）
  **本卷 = 字典层（ω 与 qB/(γm) 的同一性本身）**
  ⇒ 与 r157 的关键区别：r157 问「B 随位置变时 ω 取哪一点的 B」；
     本卷问「ω 凭什么等于 qB/(γm)」（r157 把字典当前提，本卷把字典当靶）。

================================================================================
02. 机读手段
================================================================================
  Frenet 全部**解析**构造（κ=|v×a|/v³、τ=(v×a)·j/|v×a|²，j 由参数曲线解析求导），
  **不用有限差分**（规避 r151 踩过的三阶差分噪声地板）；
  纯磁场螺旋、E×B 摆线（trochoid）、抛物线三种轨迹各有闭式；
  量纲四元组 (M,L,T,Q)；控制组 6 项；守卫 8 项；修复算子 {KEEP,DEL,REPLACE}。

================================================================================
03. 不自推声明
================================================================================
  NS1 不替靶补条件、不替靶选常数；不修改靶任何字节。
  NS2 不重判 r148/r151–r155/r157 的任何结论（分层铁律）。
  NS3 本卷只判「字典声明」，不宣称 D5/S02 体系被完全证伪。

================================================================================
04. 红线
================================================================================
  数学自洽 ≠ 实验证实；**恒等式成立 ≠ 有新内容**；**成立 ≠ 宣称域无边界**；
  防过度指控与防漏判同等重要（若机读显示某条指控越界，必须诚实削弱并登记）。
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
Q_E = 1.602176634e-19        # 元电荷 C
M_E = 9.1093837015e-31       # 电子质量 kg
C_L = 299792458.0            # 光速 m/s
B0 = 1.0                     # 参考磁场 T

# ============================================================
# 路径
# ============================================================
BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "数据")
STEM = "TUFT-r158_D5字典层_回旋频率同一性与退化点失效_2026-10-24"

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
# 量纲工具 (M, L, T, Q)（指数相加 = 相乘）
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
D_KAPPA = (0, -1, 0, 0)                       # L^-1
D_OMEGA = (0, 0, -1, 0)                       # T^-1
D_VEL = ddiv(D_LEN, D_TIME)                   # L T^-1
D_BFIELD = (1, 0, -1, -1)                     # M T^-1 Q^-1


def dim_check():
    """量纲工具自检（先守卫工具，再用于判定；承 r37/r59 纪律）。"""
    ok1 = dmul(D_MASS, (0, 1, -2, 0)) == (1, 1, -2, 0)          # ma = F
    ok2 = dmul(D_CHG, ddiv(D_BFIELD, D_MASS)) == D_OMEGA        # qB/m = T^-1
    ok3 = dpow(ddiv(D_OMEGA, D_VEL), 2) == dpow(D_KAPPA, 2)     # (ω/v)² = κ²
    return ok1 and ok2 and ok3


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


def det3(a, b, c):
    return dot(cross(a, b), c)


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


# ============================================================
# 轨迹族（全部闭式解析）
# ============================================================
def helix_frenet(rho, b):
    """匀速螺旋 r(t)=(ρ cos Ωt, ρ sin Ωt, b Ωt) 的 (κ, τ)。"""
    d = rho * rho + b * b
    if d == 0.0:
        return 0.0, 0.0
    return rho / d, b / d


def cyclotron(B, gamma, q=Q_E, m=M_E):
    return q * B / (gamma * m)


def gamma_of(beta):
    return 1.0 / math.sqrt(1.0 - beta * beta)


def trochoid_state(u, vp, w, om, t):
    """E×B 漂移（经典精确解）：r(t) = (u t + ρ sin Ωt, -ρ cos Ωt, w t), ρ=v'_⊥/Ω。

    返回 (v, a, j)（解析三阶导）。
    """
    rho = vp / om
    cs = math.cos(om * t)
    sn = math.sin(om * t)
    v = (u + rho * om * cs, rho * om * sn, w)
    a = (-rho * om * om * sn, rho * om * om * cs, 0.0)
    j = (-rho * om ** 3 * cs, -rho * om ** 3 * sn, 0.0)
    return v, a, j


def residual(lhs, rhs):
    """相对残差（两侧量纲同为 L^-2）。"""
    m = max(abs(lhs), abs(rhs))
    if m == 0.0:
        return 0.0
    return abs(lhs - rhs) / m


# ============================================================
# A 组 · 纯磁场螺旋：同一性 + 等价性（恒等式承载了什么？）
# ============================================================
CASES = [(0.10, 0.0), (0.0707, 0.0707), (0.01, 0.10), (0.5, 0.3), (0.9, 0.1)]


def group_a():
    rows = []
    for bp, bz in CASES:
        beta = math.sqrt(bp * bp + bz * bz)
        g = gamma_of(beta)
        om = cyclotron(B0, g)
        vp = bp * C_L
        vz = bz * C_L
        v = beta * C_L
        rho = vp / om            # ρ = γ m v⊥/(qB)（标准回旋半径）
        bb = vz / om             # 螺距参数 b = v∥/Ω
        k, t = helix_frenet(rho, bb)
        lhs = k * k + t * t
        rhs = (om / v) ** 2
        r = residual(lhs, rhs)
        # 等价性两路：由几何反解 Ω vs 由动力学给 Ω
        om_geo = v * math.sqrt(lhs)
        rows.append({
            "beta_perp": bp, "beta_par": bz, "gamma": g,
            "omega": om, "rho": rho, "b": bb, "v": v,
            "kappa": k, "tau": t, "lhs": lhs, "rhs": rhs,
            "res": r, "omega_geo": om_geo,
            "om_rel": abs(om_geo - om) / om,
            "rad": math.sqrt(rho * rho + bb * bb),
            "rad_std": g * M_E * v / (Q_E * B0),
            "rad_rel": abs(math.sqrt(rho * rho + bb * bb)
                           - g * M_E * v / (Q_E * B0))
                       / (g * M_E * v / (Q_E * B0)),
        })
    return rows


# ============================================================
# B 组 · 退化点：v⊥ ≡ 0（v ∥ B）
# ============================================================
DEG_BETAS = [0.001, 0.01, 0.1, 0.5, 0.9]
CONT_BETAS = [1e-3, 1e-6, 1e-9, 1e-12]     # v⊥ → 0+ 的连续性扫描


def group_b():
    """真实轨迹（直线）κ=τ=0；字典给 ω=qB/(γm)>0 ⇒ RHS>0。"""
    rows = []
    for bz in DEG_BETAS:
        g = gamma_of(bz)
        om = cyclotron(B0, g)
        v = bz * C_L
        lhs = 0.0                      # 直线：κ=τ=0
        rhs = (om / v) ** 2
        rows.append({"beta": bz, "gamma": g, "omega": om, "v": v,
                     "lhs": lhs, "rhs": rhs, "res": residual(lhs, rhs)})
    cont = []
    bz = 0.1
    g0 = gamma_of(bz)
    for bp in CONT_BETAS:
        beta = math.sqrt(bp * bp + bz * bz)
        g = gamma_of(beta)
        om = cyclotron(B0, g)
        vp = bp * C_L
        vz = bz * C_L
        v = beta * C_L
        rho = vp / om
        bb = vz / om
        k, t = helix_frenet(rho, bb)
        cont.append({"beta_perp": bp, "kappa": k, "tau": t,
                     "lhs": k * k + t * t,
                     "rhs": (om / v) ** 2,
                     "res": residual(k * k + t * t, (om / v) ** 2)})
    return rows, cont, g0


# ============================================================
# C 组 · 磁场为零的纯电场偏转（字典归零 vs 实际有曲率）
# ============================================================
E_FIELD = 1.0            # V/m
VX0 = 1.0e6              # m/s（β=3.34e-3 ⇒ 经典近似误差 ~5.6e-6）
E_TIMES = [0.0, 1.0e-9, 1.0e-8, 1.0e-7]


def group_c():
    a = Q_E * E_FIELD / M_E          # 加速度 m/s²（沿 y）
    rows = []
    for t in E_TIMES:
        vy = a * t
        v = (VX0, vy, 0.0)
        acc = (0.0, a, 0.0)
        jer = (0.0, 0.0, 0.0)
        k, tt = frenet(v, acc, jer)
        lhs = k * k + tt * tt
        rhs = 0.0                    # B=0 ⇒ ω=qB/(γm)=0
        rows.append({"t": t, "vy": vy, "kappa": k, "tau": tt,
                     "lhs": lhs, "rhs": rhs, "res": residual(lhs, rhs)})
    return rows, a


# ============================================================
# D 组 · E×B 漂移（实验室系 vs 漂移系）
# ============================================================
DRIFT_RATIOS = [1e-12, 0.01, 0.05, 0.1, 0.3, 1.0]
VP_DRIFT = 1.0e6           # 漂移系横向速率 m/s


def group_d():
    """u/v'_⊥ 扫描：实验室系残差 vs 漂移系残差。"""
    om = cyclotron(B0, 1.0)          # 经典极限 γ=1
    w = VP_DRIFT                     # 轴向速率
    rows = []
    for ratio in DRIFT_RATIOS:
        u = ratio * VP_DRIFT
        worst = 0.0
        worst_t = 0.0
        n = 240
        for i in range(n):
            t = 2.0 * math.pi * i / (n * om)
            v, a, j = trochoid_state(u, VP_DRIFT, w, om, t)
            k, tt = frenet(v, a, j)
            lhs = k * k + tt * tt
            rhs = (om / nrm(v)) ** 2
            r = residual(lhs, rhs)
            if r > worst:
                worst = r
                worst_t = t
        # 漂移系救援：同一条曲线去掉漂移 ⇒ 纯螺旋，速度取 |v'|
        v2, a2, j2 = trochoid_state(0.0, VP_DRIFT, w, om, 0.0)
        k2, t2 = frenet(v2, a2, j2)
        lhs2 = k2 * k2 + t2 * t2
        rhs2 = (om / nrm(v2)) ** 2
        rows.append({"ratio": ratio, "u": u, "res_lab": worst,
                     "res_drift": residual(lhs2, rhs2),
                     "worst_t": worst_t})
    # 标度指数（去掉控制点 1e-12，用 0.01..0.3 段）
    xs = []
    ys = []
    for r in rows:
        if 1e-4 <= r["ratio"] <= 0.35 and r["res_lab"] > 0:
            xs.append(math.log(r["ratio"]))
            ys.append(math.log(r["res_lab"]))
    slope = float('nan')
    if len(xs) >= 2:
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        den = sum((x - mx) ** 2 for x in xs)
        if den != 0:
            slope = num / den
    return rows, slope, om


# ============================================================
# 判别力：假理论 Ω' = 2Ω（判据是否只是零分辨力手法？）
# ============================================================
def group_discrim(rows_a):
    r0 = rows_a[1]
    lhs = r0["lhs"]
    rhs = (2.0 * r0["omega"] / r0["v"]) ** 2
    return {"lhs": lhs, "rhs_fake": rhs, "ratio_fake": rhs / lhs,
            "res": residual(lhs, rhs)}


# ============================================================
# 主流程
# ============================================================
def main():
    a_rows = group_a()
    b_rows, b_cont, _g0 = group_b()
    c_rows, c_acc = group_c()
    d_rows, d_slope, om_cls = group_d()
    disc = group_discrim(a_rows)

    # ---------- 量纲工具自检 + 齐次性 ----------
    dim_ok = dim_check()
    d_rhs = dpow(ddiv(D_OMEGA, D_VEL), 2)
    d_lhs = dpow(D_KAPPA, 2)
    dim_homo = (d_rhs == d_lhs)
    guard("G7-量纲工具自检与齐次性", bool(dim_ok and dim_homo),
          "dim_ok=%s homo=%s" % (dim_ok, dim_homo))
    add("B1", "量纲门禁：(ω/v)² 与 κ²+τ² 同为 L^-2", "INFO",
        "两侧量纲齐次 ⇒ 量纲门禁对本靶**零判别力**（与 r148 D2 同型：量纲自洽 ≠ 成立）",
        dim_rhs=str(d_rhs), dim_lhs=str(d_lhs))

    # ---------- A1 纯磁场螺旋同一性 ----------
    worst_a = max(r["res"] for r in a_rows)
    guard("G1-纯磁场螺旋恒等式机器零", worst_a < 1e-12, "worst=%.3e" % worst_a)
    add("A1", "纯磁场匀速螺旋：κ²+τ²=(qB/(γmv))² 精确成立", "PASS",
        "5 组 (β⊥,β∥) 最大相对残差 %.3e（机器零）⇒ 字典声明**在严格螺旋情形**下确实成立；"
        "成立与否不是本卷的争点，" % worst_a,
        worst_res=worst_a,
        worst_om_rel=max(r["om_rel"] for r in a_rows))

    # ---------- A2 等价性（零新增） ----------
    worst_eq = max(max(r["om_rel"], r["rad_rel"]) for r in a_rows)
    guard("G4-等价性三路机器零", worst_eq < 1e-12, "worst=%.3e" % worst_eq)
    add("A2", "等价性：恒等式 ⟺ 回旋半径公式 ρ=γmv⊥/(qB) 的代数重排", "INFO",
        "机读三路逐位一致（几何反解 Ω_geo=v√(κ²+τ²) ≡ 动力学 Ω=qB/(γm)；"
        "√(ρ²+b²) ≡ γmv/(qB)），最大相对差 %.3e ⇒ 恒等式的全部内容 = "
        "「匀速圆周运动 + 螺距=v∥·(2π/Ω)」这两条**纯运动学**陈述；"
        "q、m、B 只通过 Ω 进入，**不承载任何可检验的新关系** ⇒ 零新增。" % worst_eq,
        worst=worst_eq)

    # ---------- A3 退化点 v⊥ ≡ 0 ----------
    worst_b = min(r["res"] for r in b_rows)
    guard("G2-退化点失效达 100% 级", worst_b > 0.99, "min=%.6f" % worst_b)
    add("A3", "退化点失效：v⊥≡0（v ∥ B）时恒等式在**纯磁场宣告域内**失效", "FAIL",
        "v ∥ B ⇒ 洛伦兹力为零 ⇒ 真实轨迹是**直线**，κ=τ=0；而字典给 ω=qB/(γm)>0 ⇒ "
        "RHS=(ω/v)²>0 ⇒ 恒等式断言「存在曲率」而实际没有。"
        "5 个 β 档残差恒为 %.6f（100%%），与速率无关 ⇒ 结构性失效非数值伪影。" % worst_b,
        min_res=worst_b,
        rhs_sample=b_rows[2]["rhs"])

    cont_tail = b_cont[-1] if b_cont else None
    guard("G3-非零 v⊥ 极限仍成立（排除数值伪影）",
          bool(cont_tail) and cont_tail["res"] < 1e-9,
          "res@β⊥=1e-12 = %.3e" % (cont_tail["res"] if cont_tail else float('nan')))
    add("A3b", "极限不连续：v⊥→0⁺ 保持 RHS，v⊥≡0 处突降为 0", "INFO",
        "β⊥=1e-3/1e-6/1e-9/1e-12 四档 lhs 恒 ≈ %.6e 且与 rhs 残差 <1e-9；"
        "而 β⊥≡0 处 lhs 突降为 0 ⇒ 失效是**严格退化点上的拓扑不连续**"
        "（半径→0 而角速率不变，极限曲线不是直线），不是积分误差。"
        % (cont_tail["lhs"] if cont_tail else float('nan')),
        lhs_tail=cont_tail["lhs"] if cont_tail else None)

    # ---------- A4 纯电场偏转（字典归零） ----------
    c0 = c_rows[0]
    add("A4", "B=0 纯电场偏转：字典给 ω=0 ⇒ 恒等式断言「曲率为零」，与实际偏转矛盾", "BOUNDARY",
        "电子 E=%.0f V/m、v_x=%.0e m/s（β=3.3e-3 ⇒ 经典近似误差 ~6e-6，不影响 100%% 级判定）："
        "机读 κ=%.6e m^-1、τ=0 ⇒ κ²+τ²=%.6e > 0，而 RHS=0 ⇒ 残差 %.3f。"
        "**防过度指控**：D5 明写适用域为「匀速螺旋 / 梯度磁场」，B=0 不在其宣称域内 ⇒ "
        "本条只判**字典同一性**（ω=qB/(γm) 随 B→0 归零而几何 ω 不归零），记为 BOUNDARY 而非 FAIL。"
        % (E_FIELD, VX0, c0["kappa"], c0["lhs"], c0["res"]),
        kappa=c0["kappa"], res=c0["res"])

    # ---------- A5 平凡真 ----------
    add("A5", "B=0 且 v ∥ E：0=0 平凡成立", "INFO",
        "直线（κ=τ=0）且 ω=qB/(γm)=0 ⇒ 恒等式退化为 0=0 ⇒ **空洞的真**，"
        "与 A4 合起来说明：B=0 时该式在「有曲率」时判假、在「无曲率」时平凡真 ⇒ 零判别内容。")

    # ---------- A6 E×B 漂移 ----------
    ctrl_row = d_rows[0]
    guard("G5-E×B 漂移→0 恢复机器零", ctrl_row["res_lab"] < 1e-9,
          "res@u/v'=1e-12 = %.3e" % ctrl_row["res_lab"])
    guard("G6-漂移系救援全档机器零",
          max(r["res_drift"] for r in d_rows) < 1e-12,
          "worst=%.3e" % max(r["res_drift"] for r in d_rows))
    worst_lab = max(r["res_lab"] for r in d_rows[1:])
    add("A6", "E×B 漂移：实验室系失效，唯一救法是改口径用漂移系速度", "BOUNDARY",
        "经典精确解（r = u t + 螺旋，u=E×B/B²）：u/v'⊥ 从 0.01 到 1 扫描，"
        "实验室系最大残差 %.3e → %.3e（标度指数 p=%.3f）；u→0 时恢复机器零（内嵌控制）⇒ 失效确由漂移引起。"
        "去掉漂移、速度改取 |v'| 后**全档残差 <1e-12** ⇒ 唯一救法成立，"
        "但代价是**引入来料从未声明的速度口径**（外部输入 +1）。"
        % (d_rows[1]["res_lab"], worst_lab, d_slope),
        worst_lab=worst_lab, slope=d_slope)

    # ---------- A7 判别力 ----------
    guard("G4b-判据分辨力（假 Ω'=2Ω）", disc["res"] > 1e-6,
          "res=%.6f（rhs/lhs=%.3f）" % (disc["res"], disc["ratio_fake"]))
    add("A7", "判据分辨力：假理论 Ω'=2Ω 被判残差 %.1f%%" % (disc["res"] * 100.0), "PASS",
        "把 ω 换成 2qB/(γm) 而轨迹不变 ⇒ 残差 %.6f（rhs/lhs=4）≫ 噪声地板 1e-15 ⇒ "
        "本卷判据**不是零分辨力手法**（承 r153「快度救援无判别力」的教训）；"
        "但请注意分辨力的方向：它检验的是「代入的 ω 是否为轨迹的真实角速率」，"
        "**不是**「ω 是否等于 qB/(γm)」——后者是外加拼接，恒等式本身测不到它。"
        % disc["res"],
        res=disc["res"])

    # ---------- A8 γ 口径依赖 ----------
    r0 = a_rows[1]
    g_tot = r0["gamma"]
    g_perp = gamma_of(r0["beta_perp"])
    om_wrong = cyclotron(B0, g_perp)
    res_gam = residual(r0["lhs"], (om_wrong / r0["v"]) ** 2)
    add("A8", "γ 口径依赖：γ 取总速率还是仅横向速率，来料未声明", "BOUNDARY",
        "取 γ=γ(v_⊥) 时残差 %.3e（非零、比噪声地板高 12 个量级 ⇒ 判据可分辨，"
        "但量级仅 5e-3 未达致命）⇒ 字典声明依赖一个**未声明的 γ 约定**，"
        "与 r157「ω 取哪一点的 B」是同一类口径缺陷在**另一处**的复发。" % res_gam,
        res=res_gam)

    # ---------- B3 精算读数（电子） ----------
    r1 = a_rows[1]
    add("B3", "精算读数（电子，B=1 T，β⊥=β∥=0.0707）", "INFO",
        "γ=%.10f、Ω=qB/(γm)=%.6e rad/s、ρ=%.6e m、b=%.6e m、v=%.6e m/s、"
        "κ=%.6e m^-1、τ=%.6e m^-1、κ²+τ²=%.6e = (Ω/v)²=%.6e（残差 %.3e）。"
        % (r1["gamma"], r1["omega"], r1["rho"], r1["b"], r1["v"],
           r1["kappa"], r1["tau"], r1["lhs"], r1["rhs"], r1["res"]),
        omega=r1["omega"], rho=r1["rho"], kappa=r1["kappa"], tau=r1["tau"])

    # ---------- 控制组 ----------
    k_line, t_line = frenet((0.0, 0.0, b_rows[2]["v"]), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    control("C1", "纯磁场螺旋恒等式机器零（5 组）", "%.3e" % worst_a, "<1e-12", worst_a < 1e-12)
    control("C2", "工具能识别退化：直线 κ=τ 机读为 0",
            "%.1e / %.1e" % (k_line, t_line), "0 / 0",
            k_line == 0.0 and t_line == 0.0)
    control("C3", "工具能识别平面曲线：抛物线 κ>0、τ=0",
            "%.6e / %.1e" % (c0["kappa"], c0["tau"]), ">0 / 0",
            c0["kappa"] > 0 and c0["tau"] == 0.0)
    control("C4", "判据分辨力：Ω'=2Ω 残差", "%.6f" % disc["res"], ">1e-6", disc["res"] > 1e-6)
    control("C5", "量纲工具自检（ma=F / qB/m=T^-1 / (ω/v)²=κ²）",
            str(dim_ok), "True", dim_ok)
    control("C6", "Ω_geo ≡ Ω_dyn（SI 电子数，同源常数现算）",
            "%.3e" % max(r["om_rel"] for r in a_rows), "<1e-12",
            max(r["om_rel"] for r in a_rows) < 1e-12)

    # ---------- 常数同源守卫 ----------
    cons = max(abs(r["rho"] - r["v"] * r["beta_perp"] * C_L / (r["v"] * r["omega"]))
               for r in a_rows) if False else 0.0
    cons = max(abs(r["rho"] - (r["beta_perp"] * C_L) / r["omega"]) for r in a_rows)
    guard("G8-常数同源（ρ 两路现算一致）", cons / max(r["rho"] for r in a_rows) < 1e-15,
          "max_abs=%.3e" % cons)

    # ---------- 修复定价 ----------
    repairs = [
        {"动作": "KEEP（字典无条件通用）",
         "宣称域内成立": False,
         "代价": "A3 在**纯磁场宣告域内**失效（残差 100%）⇒ 保持原样即假"},
        {"动作": "DEL（删掉字典，只留几何恒等式）",
         "宣称域内成立": True,
         "代价": "电磁—几何接口断裂；恒等式退化为纯运动学（A2 已证零新增）⇒ 剩余非已知内容 0"},
        {"动作": "REPLACE（补条件：v⊥≠0 且 B≠0 且无电场；或改用漂移系速度）",
         "宣称域内成立": True,
         "代价": "外部条件声明 +1（漂移系口径再 +1）；补完后恒等式仍零新增"},
    ]
    n_surv = sum(1 for r in repairs if r["宣称域内成立"])
    n_zero = sum(1 for r in repairs if r["宣称域内成立"] and "外部" not in r["代价"]
                 and "退化为" not in r["代价"])
    add("B2", "修复定价（3 动作低阶枚举）", "FAIL",
        "宣称域内成立 %d 个、**零代价 %d 个** ⇒ 修好的唯一办法是收窄宣称域或删掉接口，"
        "而恒等式零新增 ⇒ 「字典接口」角色空转 ⇒ **修复可行 ≠ 修复后仍有内容**"
        "（「修复即自杀」同型结构第八次登记）。" % (n_surv, n_zero),
        survive=n_surv, zero_cost=n_zero)

    # ---------- 汇总 ----------
    cnt = {}
    for it in ITEMS:
        cnt[it["status"]] = cnt.get(it["status"], 0) + 1
    allok = all(c["ok"] for c in CONTROLS)
    gallok = all(g["ok"] for g in GUARDS)
    verdict = ("CYCLOTRON-DICTIONARY-TAUTOLOGICAL-OVERCLAIMED-AT-DEGENERACY-ZERO-NEW-CONTENT")

    # ============================================================
    # 报告（控制台 / _report.txt）
    # ============================================================
    L = []
    w = L.append
    w("=" * 78)
    w(" TUFT-r158｜D5 字典层：ω=qB/(γm) 与三重奏 ω 的同一性判决")
    w("=" * 78)
    w("")
    w("[A1] 纯磁场匀速螺旋（B=1 T）")
    for r in a_rows:
        w("   β⊥=%-8.4g β∥=%-8.4g γ=%.6f Ω=%.6e κ=%.6e τ=%.6e 残差=%.3e"
          % (r["beta_perp"], r["beta_par"], r["gamma"], r["omega"],
             r["kappa"], r["tau"], r["res"]))
    w("")
    w("[A2] 等价性：Ω_geo vs Ω_dyn，√(ρ²+b²) vs γmv/(qB)")
    for r in a_rows:
        w("   Ω相对差=%.3e  半径相对差=%.3e" % (r["om_rel"], r["rad_rel"]))
    w("")
    w("[A3] 退化点 v⊥≡0（v ∥ B）")
    for r in b_rows:
        w("   β=%-8.4g Ω=%.6e v=%.6e RHS=(ω/v)²=%.6e LHS=0  残差=%.6f"
          % (r["beta"], r["omega"], r["v"], r["rhs"], r["res"]))
    w("")
    w("[A3b] v⊥→0⁺ 连续性（β∥=0.1）")
    for r in b_cont:
        w("   β⊥=%-8.4g κ=%.6e τ=%.6e lhs=%.6e 残差=%.3e"
          % (r["beta_perp"], r["kappa"], r["tau"], r["lhs"], r["res"]))
    w("")
    w("[A4] B=0 纯电场偏转（E=%.0f V/m, vx=%.0e m/s, a=%.6e m/s²）" % (E_FIELD, VX0, c_acc))
    for r in c_rows:
        w("   t=%-10.3e κ=%.6e τ=%.1e lhs=%.6e rhs=0 残差=%.3f"
          % (r["t"], r["kappa"], r["tau"], r["lhs"], r["res"]))
    w("")
    w("[A6] E×B 漂移（u/v'⊥ 扫描，Ω_cls=%.6e）" % om_cls)
    for r in d_rows:
        w("   u/v'=%-10.4g res_lab=%.6e  res_drift=%.3e"
          % (r["ratio"], r["res_lab"], r["res_drift"]))
    w("   标度指数 p = %.6f" % d_slope)
    w("")
    w("[A7] 判别力：Ω'=2Ω ⇒ 残差=%.6f（rhs/lhs=%.3f）" % (disc["res"], disc["ratio_fake"]))
    w("[A8] γ 取横向速率 ⇒ 残差=%.6e" % res_gam)
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
    b("# 判定册 TUFT-r158｜D5 字典层：ω=qB/(γm) 与三重奏 ω 的同一性 · 退化点失效 · E×B 边界")
    b("")
    b("- 编号：TUFT-r158")
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
    b("| r157 | 动力学积分层 | 真实洛伦兹积分、成立域 λ*、**ω 取哪一点的 B** |")
    b("| **r158** | **字典层** | **ω 凭什么等于 qB/(γm)**（前六卷全部预设该接口） |")
    b("")
    b("## 01. 判词")
    b("")
    b("`%s`" % verdict)
    b("")
    b("**「ω = qB/(γm) 正是三重奏中的 ω」这条字典声明，在严格螺旋情形下精确成立"
      "（机器零），但它的全部内容等价于回旋半径公式 ρ=γmv⊥/(qB) 的代数重排 ⇒ 零新增；"
      "同时它在纯磁场宣告域的退化点 v⊥≡0 处失效（残差 100%，且是极限不连续而非数值伪影），"
      "在有电场漂移时实验室系失效（唯一救法是改口径用漂移系速度）。"
      "⇒ 接口可以成立，但成立时不承载新物理，不成立时又是来料自己宣称域内的点。**")
    b("")
    b("## 02. 核心结论")
    b("")
    b("### 2.1 严格螺旋：成立（机器零）")
    b("")
    b("| β⊥ | β∥ | γ | Ω=qB/(γm) | κ | τ | 残差 |")
    b("|---|---|---|---|---|---|---|")
    for r in a_rows:
        b("| %-8.4g | %-8.4g | %.6f | %.6e | %.6e | %.6e | %.3e |"
          % (r["beta_perp"], r["beta_par"], r["gamma"], r["omega"],
             r["kappa"], r["tau"], r["res"]))
    b("")
    b("### 2.2 等价性：它就是回旋半径公式（零新增）")
    b("")
    b("- 几何反解 Ω_geo = v·√(κ²+τ²) 与动力学 Ω = qB/(γm)：最大相对差 **%.3e**；"
      % max(r["om_rel"] for r in a_rows))
    b("- √(ρ²+b²) 与 γmv/(qB)：最大相对差 **%.3e**。"
      % max(r["rad_rel"] for r in a_rows))
    b("- ⇒ 恒等式的全部内容 = 「匀速圆周运动（ρ=v⊥/Ω）+ 螺距=v∥·(2π/Ω)」两条**纯运动学**陈述；")
    b("  q、m、B 只经 Ω 进入，**不含任何可检验的新关系**（A7 证明判据本身有分辨力，"
      "所以它测的确实是「代入的 ω 是否为真实角速率」，而不是「ω 是否等于 qB/(γm)」——后者是外加拼接）。")
    b("")
    b("### 2.3 退化点失效（本卷唯一的硬 FAIL）")
    b("")
    b("| β（v∥B） | Ω | v | RHS=(ω/v)² | LHS（真实直线） | 残差 |")
    b("|---|---|---|---|---|---|")
    for r in b_rows:
        b("| %-8.4g | %.6e | %.6e | %.6e | 0 | %.6f |"
          % (r["beta"], r["omega"], r["v"], r["rhs"], r["res"]))
    b("")
    b("- v ∥ B ⇒ 洛伦兹力为零 ⇒ **真实轨迹是直线**（工具机读 κ=τ=0，控制组 C2 佐证），")
    b("  而字典给 ω=qB/(γm)>0 ⇒ 恒等式断言存在曲率 ⇒ **在纯磁场宣告域内失效**。")
    b("- **极限不连续**（A3b）：β⊥=1e-3→1e-12 四档 lhs 恒 ≈ %.6e（残差 <1e-9），"
      % (b_cont[-1]["lhs"] if b_cont else float('nan')))
    b("  而 β⊥≡0 处突降为 0 ⇒ 半径→0 而角速率不变，极限曲线不是直线 ⇒ 非数值伪影。")
    b("")
    b("### 2.4 电场：实验室系失效，漂移系可救")
    b("")
    b("| u/v'⊥ | 实验室系残差 | 漂移系残差 |")
    b("|---|---|---|")
    for r in d_rows:
        b("| %-10.4g | %.6e | %.3e |" % (r["ratio"], r["res_lab"], r["res_drift"]))
    b("")
    b("- 标度指数 p = **%.6f**；u→0 内嵌控制恢复机器零（守卫 G5）。" % d_slope)
    b("- B=0 纯电偏转（A4）：κ=%.6e>0 而字典给 ω=0 ⇒ 断言「曲率为零」⇒ 残差 100%%；"
      % c0["kappa"])
    b("  **防过度指控**：D5 明写适用域「匀速螺旋 / 梯度磁场」，B=0 不在宣称域 ⇒ 记 BOUNDARY。")
    b("")
    b("## 03. 修复定价")
    b("")
    b("| 动作 | 宣称域内成立 | 代价 |")
    b("|---|---|---|")
    for r in repairs:
        b("| %s | %s | %s |" % (r["动作"], "是" if r["宣称域内成立"] else "否", r["代价"]))
    b("")
    b("- 宣称域内成立 **%d** 个、零代价 **%d** 个 ⇒ **修复可行 ≠ 修复后仍有内容**"
      "（第八次登记）。" % (n_surv, n_zero))
    b("")
    b("## 04. 未闭合项（未做即未证，不得外推）")
    b("")
    b("1. E×B 分支用**经典精确解**（γ=1）；相对论下漂移系变换未做，但「漂移使 |v| 不再恒定」"
      "这一失效机理与 γ 无关 ⇒ 定性结论不依赖。")
    b("2. 纯电场分支同样取经典极限（β=3.3e-3，相对论修正 ~6e-6），不影响 100% 级判定。")
    b("3. 场模型限于**均匀** B / 均匀 E；非均匀场属 r157 层（λ*），本卷不重判。")
    b("4. 修复空间是低阶（3 动作）；新增型算子（改函数形式 / 改向量结构）未枚举。")
    b("5. 本卷**不宣称** D5 / S02 体系被完全证伪 —— 只判决字典接口：成立时零新增、"
      "退化点失效、电场下需换口径。")
    b("")
    b("## 05. 自抓与更正（本卷自身缺陷，均已修并复跑至 rc=0）")
    b("")
    b("1. **判词段拼接缺右括号** ⇒ 首跑 SyntaxError（rc=1）。")
    b("2. **A7 条目的 % 只作用于最后一段拼接串**、参数个数不匹配 ⇒ 二跑 TypeError（rc=1）。")
    b("3. **量纲工具自检 ok2 原式写成 q/(B·m)**（正确为 q·B/m）⇒ 守卫 G7 判 FAIL、")
    b("   控制组 5/6、三跑 rc=2；已修后控制组 6/6、守卫 9/9、rc=0。")
    b("")
    b("- **纪律复现**：量纲类断言（含量纲工具自身的自检）必须机器兜底 ——")
    b("  本库已在 r37 / r44 / r64 / r66 等多卷同型翻车，本卷为同类第三次。")
    b("")
    b("## 06. 红线")
    b("")
    b("- 数学自洽 ≠ 实验证实。")
    b("- **恒等式成立 ≠ 有新内容**；**成立 ≠ 宣称域无边界**。")
    b("- 防过度指控与防漏判同等重要：A4/A6 因靶未宣称该域而降 BOUNDARY，不按 FAIL 计。")
    b("- **判据分辨力的方向要说清**：本卷判据测的是「ω 是否为真实角速率」，"
      "不是「ω 是否等于 qB/(γm)」。")
    b("")
    judge = "\n".join(m)

    # ---------- 落盘 ----------
    os.makedirs(OUT, exist_ok=True)
    payload = {
        "id": "TUFT-r158",
        "title": "D5 字典层：ω=qB/(γm) 与三重奏 ω 的同一性 · 退化点失效 · E×B 边界",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict,
        "counts": cnt,
        "controls_ok": allok,
        "guards_ok": gallok,
        "items": ITEMS,
        "helix_rows": a_rows,
        "degenerate_rows": b_rows,
        "continuity_rows": b_cont,
        "efield_rows": c_rows,
        "drift_rows": d_rows,
        "drift_slope": d_slope,
        "discrim": disc,
        "gamma_convention_res": res_gam,
        "repairs": repairs,
        "controls": CONTROLS,
        "guards": [{"name": g["name"], "ok": g["ok"], "detail": g["detail"]}
                   for g in GUARDS],
    }
    with io.open(os.path.join(OUT, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with io.open(os.path.join(OUT, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)
    with io.open(os.path.join(OUT, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(judge)
    with io.open(os.path.join(OUT, "判定_" + STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(judge)

    print(report)
    print("")
    print("[已写出] " + os.path.join(OUT, STEM + ".json"))
    print("[已写出] " + os.path.join(OUT, STEM + ".md"))
    print("[已写出] " + os.path.join(OUT, STEM + "_report.txt"))
    print("[已写出] " + os.path.join(OUT, "判定_" + STEM + ".md"))
    return 0 if (allok and gallok
                 and all(it["status"] != "GUARD-FAIL" for it in ITEMS)) else 2


if __name__ == "__main__":
    sys.exit(main())
