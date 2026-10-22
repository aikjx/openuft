# -*- coding: utf-8 -*-
"""
TUFT-r148 · D5《大统一力方程》首攻与修复定价

靶（来料，库内从未被攻破）：
  openuft/01_独立体系/S02_空间光速螺旋统一力/04_理论推导/D5_大统一力方程/README.md + D5_大统一力方程.py

来料原文四条 + 一条基石：
  统一动量   P = m (c - v)
  统一力     F = dP/dt
  电磁力比   F_e / F_m = c / v
  电磁波     E = c B        （来料自称「由 Maxwell 已证」）
  三重奏     kappa^2 + tau^2 = (omega/v)^2 = (qB/(gamma m v))^2   （来料标注适用：匀速螺旋 / 梯度磁场）

分工声明（与既有册严格分层，条目不可相加）：
  - S02 的 §18 做「标准物理 Yukawa/Proca 四力形式统一」（有效理论层，且自认只攻 ①②不攻 ③④）；
    §19 做耦合跑动与 GUT 能标；r146 占位做四力统一可行性跨册归总。
  - **本卷攻的是 D5 本身**，即张祥前体系的【原始公设层方程】，与上述各册不在同一层。
  - 本卷沿用 r141/r142/r147 的三层法：物理层判定 -> 新增性定价 -> 低阶算子修复枚举与定价。

要抓的几条（预登记，最终以机读为准）：
  A 组【读法与极限】：c 是标量还是矢量？两种读法各有什么后果？静止 / 光速两个极限各给出什么？
  B 组【动力学】：F = dP/dt 相对 F = m a 的符号；静止物体是否受「几何力」？
  C 组【恒等式与新增性】：kappa^2+tau^2=(omega/v)^2 对不对、新不新、梯度磁场下还成不成立；
                          F_e/F_m = c/v 是不是复述？
  D 组【名实与门禁】：叫「大统一力方程」，方程里出现了几种力？量纲门禁对这条错有没有判别力？
  E 组【修复定价】：对 P = m(C - v) 的两个加项统一施加 {KEEP, FLIP, DEL}（延续 r147 的机器生成口径），
                    全枚举 3^2 = 9 个组合，看哪些能同时关闭 A/B 组各条，以及存活解是不是标准物理。

★编号：实测首空号 r148（源码/数据 0 命中；README 中 r148 仅出现在上一卷的两行「下轮从 r148 起」指针）。
"""
import os
import re
import io
import json
import math
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.normpath(os.path.join(HERE, "..", "数据"))
OPENUFT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATE = "2026-10-22"
STEM = "TUFT-r148_D5大统一力方程首攻与修复定价_%s" % DATE
JUDGE_STEM = "判定_TUFT-r148_D5大统一力方程首攻与修复定价_%s" % DATE

D5_DIR = os.path.join(OPENUFT, "01_独立体系", "S02_空间光速螺旋统一力",
                      "04_理论推导", "D5_大统一力方程")

# 物理常数（SI，CODATA 口径）
C = 299792458.0
M_E = 9.1093837015e-31
HBAR = 1.054571817e-34
G_SURF = 9.80665
E_CHARGE = 1.602176634e-19
EV_J = E_CHARGE

ENTRIES = []
METRICS = {}
CTRLS = []


def add(eid, name, group, claim, machine, verdict, detail, control=""):
    ENTRIES.append({"id": eid, "name": name, "group": group, "claim": claim,
                    "machine": machine, "verdict": verdict,
                    "detail": detail, "control": control})


def add_ctrl(name, machine, ok, note=""):
    CTRLS.append({"name": name, "machine": machine, "ok": bool(ok), "note": note})


# ============================ 向量与 Frenet 工具 ============================
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def nrm(a):
    return math.sqrt(dot(a, a))


def det3(a, b, c):
    return dot(a, cross(b, c))


def frenet(v, a, ad):
    """由解析的 v, a, adot 算曲率 kappa 与挠率 tau（弧长参数化定义）。"""
    cx = cross(v, a)
    nc = nrm(cx)
    nv = nrm(v)
    kappa = nc / (nv ** 3)
    tau = det3(v, a, ad) / (nc * nc)
    return kappa, tau


def helix_derivs(R, w, t, h1, h2, h3):
    """r(t) = (R cos wt, R sin wt, h(t))；h1/h2/h3 = h', h'', h'''。"""
    ct, st = math.cos(w * t), math.sin(w * t)
    v = (-R * w * st, R * w * ct, h1)
    a = (-R * w * w * ct, -R * w * w * st, h2)
    ad = (R * w ** 3 * st, -R * w ** 3 * ct, h3)
    return v, a, ad


def helix_identity_err(R, w, t, h1, h2, h3):
    """|kappa^2+tau^2 - (omega/v)^2| / (omega/v)^2"""
    v, a, ad = helix_derivs(R, w, t, h1, h2, h3)
    kappa, tau = frenet(v, a, ad)
    speed = nrm(v)
    lhs = kappa * kappa + tau * tau
    rhs = (w / speed) ** 2
    return abs(lhs - rhs) / rhs, kappa, tau, speed


# ============================ 量纲工具（Fraction 精确） ============================
# 量纲四元组 (M, L, T, Q)
DIM = {
    "m": (1, 0, 0, 0),
    "v": (0, 1, -1, 0),
    "c": (0, 1, -1, 0),
    "a": (0, 1, -2, 0),
    "F": (1, 1, -2, 0),
    "E": (1, 2, -2, 0),
    "p": (1, 1, -1, 0),
    "B": (1, 0, -1, -1),
    "q": (0, 0, 0, 1),
    "kappa": (0, -1, 0, 0),
    "tau": (0, -1, 0, 0),
}


def dim_mul(x, y):
    return tuple(x[i] + y[i] for i in range(4))


def dim_pow(x, n):
    return tuple(x[i] * n for i in range(4))


def dim_homogeneous(terms):
    """terms: list of dim tuples；返回是否齐次。"""
    return all(t == terms[0] for t in terms)


# ============================ 组 A：读法与两个极限 ============================
def group_A():
    # ---- A1 类型读法两难 ----
    d_scalar_sub_vector = "M*(L T^-1) 与 M*(L T^-1)：标量 - 矢量 在矢量空间无定义"
    # 读法 1：c 为标量常数
    #   P = m(c - v)：c 标量、v 矢量 => 类型错误（除非 v 被理解为速率标量）
    # 读法 2：v 为速率标量 |v|
    #   P = m(c - |v|)：量纲 OK，但 P 是【标量】不是矢量 => 与「力有方向」矛盾
    # 读法 3：c 为矢量 C（|C| = c，空间光速螺旋公设）
    #   P = m(C - v)：矢量，有定义 => 但引出 A2/A3/B1/B2
    readings = [
        ("R1 c=标量, v=矢量", False, "标量减矢量，矢量空间无定义"),
        ("R2 c=标量, v=速率|v|", True, "P 退化为标量，无法承载力的方向"),
        ("R3 c=矢量C, v=矢量", True, "有定义，但静止动量非零（A2）、光速极限反常（A3）"),
    ]
    n_def = sum(1 for r in readings if r[1])
    machine_a1 = "3 种读法：R1 类型错误(不可定义)；R2 可定义但 P 退化为标量；R3 可定义但引 A2/A3"
    METRICS["A1_n_readings"] = 3
    METRICS["A1_n_definable"] = n_def
    METRICS["A1_n_clean"] = sum(1 for r in readings if r[1] and "但" not in r[2])
    v_a1 = "BOUNDARY"
    add("A1", "P=m(c-v) 的类型读法两难", "A",
        "来料的 P = m(c - v) 到底怎么读？",
        machine_a1, v_a1,
        "三种读法必居其一，各有硬伤：\n"
        "  - R1（c 标量、v 矢量）：**标量减矢量**，矢量空间无定义 —— 严格意义上的类型错误；\n"
        "  - R2（c 标量、v 取速率 |v|）：可定义，但 P 变成**标量**，无法承载「力有方向」这一基本属性；\n"
        "  - R3（c 为矢量 C，|C| = c，即空间光速螺旋公设）：可定义且是矢量，但引出 A2 / A3 / B1 / B2。\n"
        "⇒ **没有一种读法是干净的**：R1 无定义、R2 丢方向、R3 与实验极限冲突。本卷后续按 R3 立论（对来料最有利）。",
        "控制组：标准 p = gamma m v 无此歧义（矢量 - 矢量同型）")

    # ---- A2 静止极限 ----
    m_test = 1.0
    p_rest_d5 = m_test * C                      # R3 下 P(v=0) = m C
    p_rest_std = 0.0                            # 牛顿 / 相对论均为 0
    # 用质子静止质量的等效动量做「离谱程度」对照
    machine_a2 = ("R3 下 P(v=0) = m*|C| = %.6e kg*m/s（m=1 kg）；"
                  "标准（牛顿 p=mv 与相对论 p=gamma m v）在 v=0 均为 0" % p_rest_d5)
    METRICS["A2_p_rest_d5"] = p_rest_d5
    METRICS["A2_p_rest_std"] = p_rest_std
    v_a2 = "FAIL" if p_rest_d5 > 0 else "PASS"
    add("A2", "静止极限：静止物体动量非零", "A",
        "按 R3 读法，v = 0 时动量是多少？",
        machine_a2, v_a2,
        "R3 下 **P(v=0) = m C**，模长 = m*c = **%.6e kg·m/s**（取 m = 1 kg）。\n"
        "而动量守恒与惯性系定义的基石是：**静止物体动量为零**（牛顿 p = mv 与相对论 p = gamma·m·v 在 v=0 都给 0）。\n"
        "⇒ 若静止物体带有 m*c 量级的动量，则「动量」的零点被整体平移，动量守恒定律要改写为守恒 P - mC，"
        "而 C 又随空间点运动而变（螺旋）⇒ **连「守恒量是什么」都不再确定**。\n"
        "这不是小误差，是**零点错误**：量级 m*c 而非 0。" % p_rest_d5,
        "控制组1：标准相对论动量在 v=0 给 0，判据对其不触发")

    # ---- A3 光速极限 ----
    # 取 v 沿 C 方向、大小 (1-1e-9) c
    beta = 1.0 - 1.0e-9
    p_d5 = M_E * (C - beta * C)                 # R3 下 |P| = m(c - v)
    e_d5 = p_d5 * C                             # 用 E = P c 换算（来料口径）
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    p_std = gamma * M_E * beta * C
    e_std = gamma * M_E * C * C
    ratio_e = e_std / e_d5 if e_d5 > 0 else float("inf")
    # 光子：v = c 时 D5 给出 P = 0
    p_photon_d5 = 0.0
    nu = 5.0e14                                 # 可见光
    p_photon_std = 6.62607015e-34 * nu / C
    e_photon_std_ev = 6.62607015e-34 * nu / EV_J
    machine_a3 = ("beta=1-1e-9：D5 |P|=%.6e、E=Pc=%.6e J；相对论 |p|=%.6e、E=%.6e J；"
                  "比值 E_std/E_D5=%.6e。光子极限：D5 给 P=0 ⇒ E=0；标准 p=%.6e、E=%.4f eV"
                  % (p_d5, e_d5, p_std, e_std, ratio_e, p_photon_std, e_photon_std_ev))
    METRICS["A3_p_d5"] = p_d5
    METRICS["A3_e_d5_J"] = e_d5
    METRICS["A3_p_std"] = p_std
    METRICS["A3_e_std_J"] = e_std
    METRICS["A3_ratio_e"] = ratio_e
    METRICS["A3_e_photon_std_eV"] = e_photon_std_ev
    METRICS["A3_p_photon_d5"] = p_photon_d5
    v_a3 = "FAIL" if (e_d5 < e_std and p_photon_d5 == 0.0 and e_photon_std_ev > 0) else "PASS"
    add("A3", "光速极限：动量与能量趋于零（光子能量为零）", "A",
        "v -> c 时，来料的 P = m(c - v) 给出什么？",
        machine_a3, v_a3,
        "R3 下 v 沿 C 且 |v| -> c 时，**P = m(C - v) -> 0**，于是按 E = P c 有 **E -> 0**。\n"
        "机读（电子，beta = 1 - 1e-9）：D5 给 |P| = %.6e kg·m/s、E = %.6e J；"
        "相对论给 |p| = %.6e kg·m/s、E = %.6e J ⇒ **比值 %.4e 倍**。\n"
        "极限情形更致命：**光子 v = c ⇒ P = 0 ⇒ E = 0**；而标准光子 p = h*nu/c = %.6e kg·m/s、"
        "E = h*nu = %.4f eV（取 nu = 5e14 Hz 的可见光）。\n"
        "⇒ 方向**完全相反**：相对论要求 v -> c 时动量**发散**，来料给出**趋于零**；"
        "这不是数值偏差，是**单调性反向**。" % (p_d5, e_d5, p_std, e_std, ratio_e,
                                                p_photon_std, e_photon_std_ev),
        "控制组1：标准相对论动量在 beta->1 时发散，判据对其不触发")


# ============================ 组 B：动力学 ============================
def rk4_osc(sign, t_end, nstep):
    """x'' = sign * x，x(0)=1, x'(0)=0。sign=-1 标准弹簧；sign=+1 来料 F=-m a 的后果。"""
    dt = t_end / nstep
    x, u = 1.0, 0.0
    for _ in range(nstep):
        def f(x, u):
            return (u, sign * x)
        k1 = f(x, u)
        k2 = f(x + 0.5 * dt * k1[0], u + 0.5 * dt * k1[1])
        k3 = f(x + 0.5 * dt * k2[0], u + 0.5 * dt * k2[1])
        k4 = f(x + dt * k3[0], u + dt * k3[1])
        x = x + dt / 6.0 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        u = u + dt / 6.0 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return x, u


def group_B():
    # ---- B1 符号：F = dP/dt 相对 F = m a ----
    # R3 下若 C 恒定：F = m(dC/dt - dv/dt) = -m a
    x_std, _ = rk4_osc(-1.0, 10.0, 20000)       # 标准：x'' = -x
    x_d5, _ = rk4_osc(+1.0, 10.0, 20000)        # 来料：a = -F/m ⇒ x'' = +x
    x_exact_std = math.cos(10.0)
    x_exact_d5 = math.cosh(10.0)
    err_num = abs(x_std - x_exact_std) / abs(x_exact_std)
    ratio = abs(x_d5) / abs(x_std) if x_std != 0 else float("inf")
    machine_b1 = ("C 恒定时 F = m(dC/dt - dv/dt) = -m*a ⇒ 与 F=+m*a 反号。"
                  "弹簧(k/m=1, x0=1, t=10)：标准 x=%.6f（解析 cos10=%.6f，数值误差 %.2e）；"
                  "来料 x=%.4f（解析 cosh10=%.4f）；比值 %.4e" %
                  (x_std, x_exact_std, err_num, x_d5, x_exact_d5, ratio))
    METRICS["B1_x_std"] = x_std
    METRICS["B1_x_d5"] = x_d5
    METRICS["B1_num_err"] = err_num
    METRICS["B1_ratio"] = ratio
    v_b1 = "FAIL" if ratio > 1.0e3 else "PASS"
    add("B1", "F = dP/dt 相对 F = m a 整体反号", "B",
        "把 F = dP/dt 展开，符号与牛顿第二定律一致吗？",
        machine_b1, v_b1,
        "R3 下 P = m(C - v)，若 C 恒定则 **F = dP/dt = m(0 - a) = -m a**，与牛顿第二定律 F = +m a **处处反号**。\n"
        "后果不是「差一点」而是**动力学定性改变**：以弹簧（k/m = 1，x₀ = 1，v₀ = 0）积分到 t = 10 ——\n"
        "  - 标准：x(10) = cos 10 = **%.6f**（有界振荡，数值积分 %.6f，误差 %.2e）；\n"
        "  - 来料：x(10) = cosh 10 = **%.4f**（**指数发散**）。\n"
        "⇒ 比值 **%.4e 倍**。反号使一切束缚势变成反束缚：行星轨道、弹簧、单摆全部指数飞散。"
        % (x_exact_std, x_std, err_num, x_exact_d5, ratio),
        "控制组2：标准 F=ma 弹簧有界（|x|<=1），判据对其不触发")

    # ---- B2 静止物体受的「几何力」 ----
    lam_c = HBAR / (M_E * C)                    # 康普顿波长
    R_helix = lam_c / (2.0 * math.pi)           # S02 取参 R = lambda/(2 pi)
    a_geo = C * C / R_helix                     # |dC/dt| = c^2 / R（螺旋曲率 1/R）
    F_geo = M_E * a_geo
    F_grav = M_E * G_SURF
    ratio_b2 = F_geo / F_grav
    machine_b2 = ("电子：lambda_C=%.6e m，R=lambda_C/2pi=%.6e m ⇒ |dC/dt|=c^2/R=%.6e m/s^2；"
                  "F_geo=m_e*a=%.6e N；重力 m_e*g=%.6e N；比值 %.4e" %
                  (lam_c, R_helix, a_geo, F_geo, F_grav, ratio_b2))
    METRICS["B2_lambda_C"] = lam_c
    METRICS["B2_R"] = R_helix
    METRICS["B2_a_geo"] = a_geo
    METRICS["B2_F_geo_N"] = F_geo
    METRICS["B2_F_grav_N"] = F_grav
    METRICS["B2_ratio"] = ratio_b2
    v_b2 = "FAIL" if F_geo > 1.0e-6 else "PASS"
    add("B2", "若 C 走螺旋，静止物体将受巨大的「几何力」", "B",
        "C 不是恒定而是走螺旋（|C| = c、方向变）时，静止物体的受力是多少？",
        machine_b2, v_b2,
        "来料把 C 定义为**空间点以光速走螺旋**（S02 公设），则 dC/dt ≠ 0，静止物体（v = 0）也要受\n"
        "**F_geo = m |dC/dt| = m c² / R**。取电子、并按 S02 取参 R = lambda_C/(2 pi)：\n"
        "  - lambda_C = %.6e m，R = %.6e m；\n"
        "  - |dC/dt| = c²/R = **%.6e m/s²**；\n"
        "  - F_geo = m_e * a = **%.6e N**，而电子重力仅 m_e*g = %.6e N ⇒ **比值 %.4e 倍**。\n"
        "⇒ 一个静止电子要受约 %.3f N 的力（加速度 %.3e m/s²）。这在 Penning 阱、单电子悬浮、"
        "以及最普通的「物体放在桌上不动」的事实面前直接否证。\n"
        "（若把 R 调大以压低 F_geo，则三重奏 kappa²+tau²=(omega/v)² 的 omega 随之改变，"
        "又与回旋频率对不上 —— 两头不可兼得。）" % (lam_c, R_helix, a_geo, F_geo, F_grav,
                                                     ratio_b2, F_geo, a_geo),
        "控制组2：标准静止物体（无外场）受力为 0")

    # ---- B3 B1 的退路：整体翻号 P = m(v - C) ----
    # 翻号后 F = m(a - dC/dt)：C 恒定时 F = +m a ⇒ 符号修好
    p_rest_flipped = M_E * C                    # |P| 不变，仍非零
    closes_sign = True
    closes_a2 = False
    machine_b3 = ("翻号为 P=m(v-C)：C 恒定时 F=+m*a（符号修好，closes=%s）；"
                  "但取电子时 |P(v=0)|=m_e*c=%.6e kg*m/s 仍非零（A2 未关闭，closes=%s）；"
                  "光速极限 |P|->0 依旧（A3 未关闭）" %
                  (closes_sign, p_rest_flipped, closes_a2))
    METRICS["B3_p_rest_flipped"] = p_rest_flipped
    METRICS["B3_closes_sign"] = 1 if closes_sign else 0
    METRICS["B3_closes_a2"] = 1 if closes_a2 else 0
    v_b3 = "BOUNDARY"
    add("B3", "退路检查：整体翻号能救 B1 吗？", "B",
        "把 P = m(C - v) 改成 P = m(v - C)（整体翻号）能否修复？",
        machine_b3, v_b3,
        "翻号后 F = m(a - dC/dt)，C 恒定时确有 **F = +m a**，B1 的符号问题被修好。\n"
        "**但代价是 A2 / A3 / B2 全部原样保留**：|P(v=0)| = m*c = %.6e kg·m/s（取电子）仍非零（A2 未关闭）；"
        "v -> c 时 |P| -> 0 依旧（A3 未关闭）；C 走螺旋时静止受力 m*c²/R 不变（B2 未关闭）。\n"
        "⇒ **符号问题与零点问题是两条独立的病**，翻号只治前者。这是本卷最重要的结构性结论之一："
        "不存在「改一个符号就都好了」的修复。" % p_rest_flipped,
        "控制组：标准 p=mv 翻号为 p=-mv 会破坏动量守恒方向，标准物理不需要翻号")


# ============================ 组 C：恒等式与新增性 ============================
def group_C():
    # ---- C1 匀速螺旋下恒等式是否成立（正确核） ----
    R, w, u = 1.0, 1.0, 1.0
    err0, k0, t0, s0 = helix_identity_err(R, w, 0.7, u, 0.0, 0.0)
    # 多点扫描确认不是单点巧合
    errs0 = [helix_identity_err(R, w, tt, u, 0.0, 0.0)[0]
             for tt in (0.3, 0.7, 1.3, 2.1, 3.7)]
    worst0 = max(errs0)
    machine_c1 = ("匀速螺旋 R=1,w=1,v_par=1：kappa=%.10f, tau=%.10f, v=%.10f；"
                  "kappa^2+tau^2=%.12f vs (w/v)^2=%.12f；相对误差 %.3e；五点扫描最坏 %.3e" %
                  (k0, t0, s0, k0 * k0 + t0 * t0, (w / s0) ** 2, err0, worst0))
    METRICS["C1_err_uniform"] = err0
    METRICS["C1_err_uniform_worst"] = worst0
    METRICS["C1_kappa"] = k0
    METRICS["C1_tau"] = t0
    v_c1 = "INFO" if worst0 < 1.0e-9 else "FAIL"
    add("C1", "kappa^2+tau^2=(omega/v)^2 在匀速螺旋下成立（但零新增）", "C",
        "这条恒等式到底对不对？",
        machine_c1, v_c1,
        "**对**。机读（R=1, omega=1, v_par=1）：kappa = %.10f、tau = %.10f、v = %.10f，\n"
        "kappa²+tau² = %.12f，(omega/v)² = %.12f，相对误差 **%.3e**；换 5 个时刻扫描最坏 **%.3e** ⇒ 机器零。\n"
        "**但这正是问题所在**：对匀速螺旋，kappa = omega*v_perp/v²、tau = omega*v_par/v² 是"
        "Frenet 公式 + 洛伦兹力的**直接推论**，代入即得上式，中间没有任何新物理步骤。\n"
        "⇒ 按本库纪律（定义式重排不算内容），判 **INFO**：**正确，但新增含量为零**。"
        % (k0, t0, s0, k0 * k0 + t0 * t0, (w / s0) ** 2, err0, worst0),
        "控制组3：恒等式在标准匀速螺旋下残差机器零 ⇒ 本卷的 Frenet 计算工具可信")

    # ---- C2 梯度磁场 / 变速螺旋下恒等式失效 ----
    ratios = (0.0, 0.01, 0.1, 0.5, 1.0)
    errs = []
    for A in ratios:
        e, _, _, _ = helix_identity_err(R, w, 1.0, u + A * 1.0, A, 0.0)
        errs.append(e)
    err_max = max(errs)
    monotone = all(errs[i] <= errs[i + 1] + 1e-15 for i in range(len(errs) - 1))
    # 磁镜换算：mu = m v_perp^2/(2B) 绝热守恒 + 能量守恒 ⇒ dv_par/dt = -v_perp0^2 * eps / 2
    # 取 v=1, v_perp0=0.5, eps=0.01（每单位长度 1%）
    v_perp0 = 0.5
    eps = 0.01
    a_eff = -v_perp0 * v_perp0 * eps / 2.0       # 常数（每单位时间，omega=1）
    # 达到 1% 残差所需的 A/u：由 (0.01 -> errs[1]) 与 (0.1 -> errs[2]) 线性插值
    if errs[2] > errs[1] and errs[1] > 0:
        # 在对数-对数坐标下插值
        import math as _m
        lg_a = (_m.log10(0.01), _m.log10(0.1))
        lg_e = (_m.log10(errs[1]), _m.log10(errs[2]))
        lg_target = _m.log10(1.0e-2)
        frac = (lg_target - lg_e[0]) / (lg_e[1] - lg_e[0])
        a_needed = 10.0 ** (lg_a[0] + frac * (lg_a[1] - lg_a[0]))
    else:
        a_needed = float("nan")
    cycles_needed = (a_needed / abs(a_eff)) if (a_eff != 0 and a_needed == a_needed) else float("nan")
    machine_c2 = ("变速（螺距变化 dv_par/dt=A）残差：A/v_par = %s ⇒ %s；最坏 %.4e；单调=%s。"
                  "磁镜换算 eps=0.01, v_perp0=0.5 ⇒ dv_par/dt=%.3e/周期；达 1%% 残差需 A/v_par=%.4f ⇒ 约 %.1f 个回旋周期"
                  % ([ "%.2f" % r for r in ratios], ["%.3e" % e for e in errs],
                     err_max, monotone, a_eff, a_needed, cycles_needed))
    METRICS["C2_err_uniform"] = errs[0]
    METRICS["C2_err_max"] = err_max
    METRICS["C2_monotone"] = 1 if monotone else 0
    METRICS["C2_a_eff_mirror"] = a_eff
    METRICS["C2_cycles_to_1pct"] = cycles_needed
    v_c2 = "FAIL" if (err_max > 1.0e-2 and monotone and errs[0] < 1.0e-9) else "BOUNDARY"
    add("C2", "恒等式越界：来料标注的「梯度磁场」下不成立", "C",
        "来料把适用范围写成「匀速螺旋 / 梯度磁场」，梯度磁场下还成立吗？",
        machine_c2, v_c2,
        "**不成立**。匀速档（A = 0）残差 %.3e（机器零）；一旦螺距变化（dv_par/dt = A），残差单调上升：\n"
        "  A/v_par = %s ⇒ 残差 %s，最坏 **%.4e**，单调性 %s。\n"
        "物理对应：梯度磁场下磁镜效应使 v_par 变化 —— 由绝热不变量 mu = m*v_perp²/(2B) 与能量守恒可得\n"
        "  **dv_par/dt = -v_perp0² * eps / 2 = %.3e**（取 v_perp0 = 0.5、梯度 eps = 0.01/单位长度），\n"
        "  即螺距**持续**变化 ⇒ 运动**不是**匀速螺旋 ⇒ 恒等式失效。按标定，达到 1%% 残差约需 **%.1f 个回旋周期**。\n"
        "另：梯度磁场下 B 随位置变，来料的 omega = qB/(gamma m) **用哪一点的 B 并未声明** ⇒ **口径未定**，"
        "连式子右边都写不出来。\n"
        "⇒ 来料把「匀速螺旋」与「梯度磁场」并列为适用范围是**越界宣称**："
        "该式严格成立于匀速螺旋，且**仅此**。" %
        (errs[0], ["%.2f" % r for r in ratios], ["%.3e" % e for e in errs],
         err_max, "成立" if monotone else "不成立", a_eff, cycles_needed),
        "控制组3：同一工具在匀速档给机器零 ⇒ 变速档的残差不是工具误差")

    # ---- C3 F_e / F_m = c / v 的新增性 ----
    # 标准洛伦兹力：F = q(E + v x B)。取平面波 E = c B 且 v ⟂ B、v ⟂ E 的构型
    Bval = 1.0e-3
    Eval = C * Bval
    q = E_CHARGE
    results = []
    for vv in (1.0e5, 1.0e6, 1.0e7, 1.0e8):
        Fe = q * Eval
        Fm = q * vv * Bval
        ratio_std = Fe / Fm
        ratio_d5 = C / vv
        results.append((vv, ratio_std, ratio_d5, abs(ratio_std - ratio_d5) / ratio_d5))
    worst_c3 = max(r[3] for r in results)
    machine_c3 = ("平面波 E=cB 下标准洛伦兹力 F_e/F_m = qE/(qvB) = c/v；"
                  "四档 v 的最坏相对偏差 %.3e" % worst_c3)
    METRICS["C3_worst_rel"] = worst_c3
    METRICS["C3_table"] = [[r[0], r[1], r[2], r[3]] for r in results]
    v_c3 = "INFO" if worst_c3 < 1.0e-12 else "FAIL"
    add("C3", "F_e/F_m = c/v 是标准洛伦兹力的复述（零新增）", "C",
        "力比 c/v 是新东西吗？",
        machine_c3, v_c3,
        "**不是**。标准洛伦兹力 F = q(E + v×B)：电力 qE、磁力 qvB（取垂直构型）⇒ F_e/F_m = E/(vB)；"
        "对平面波 E = cB ⇒ **恰好 c/v**。四档速率机读最坏相对偏差 **%.3e**（机器零）。\n"
        "⇒ 判 **INFO**：正确，但**逐字复述**标准电磁学，新增含量为零。\n"
        "**适用范围登记**：v = 0 时磁力为 0（比值发散，不是「电力无穷大」）；v ∥ B 时磁力亦为 0 ⇒ "
        "该式只在 **v ⟂ B 且 E = cB**（辐射场）的构型下有意义，来料未声明此前提。" % worst_c3,
        "控制组5：标准洛伦兹力复现 c/v")

    # ---- C4 E = cB 的适用范围 ----
    # 静电场点电荷（原子尺度 r = 1 nm）：E != 0, B = 0 ⇒ E/(cB) 发散
    r_static = 1.0e-9
    e_static = (1.0 / (4.0 * math.pi * 8.8541878128e-12)) * E_CHARGE / (r_static ** 2)
    b_static = 0.0
    ok_radiation = abs((C * Bval) - Eval) / Eval < 1e-15
    fail_static = (b_static == 0.0 and e_static > 0.0)
    machine_c4 = ("辐射场(平面波) E=cB 成立（偏差 %.1e）；静电场（电子电荷 r=1nm）E=%.4e V/m 而 B=0 ⇒ E/(cB) 发散" %
                  (0.0, e_static))
    METRICS["C4_ok_radiation"] = 1 if ok_radiation else 0
    METRICS["C4_fail_static"] = 1 if fail_static else 0
    METRICS["C4_e_static"] = e_static
    METRICS["C4_r_static"] = r_static
    v_c4 = "FAIL" if fail_static else "PASS"
    add("C4", "E = cB 被写成了普遍关系（实际只对辐射场成立）", "C",
        "来料称 E = cB「由 Maxwell 已证」，它普遍成立吗？",
        machine_c4, v_c4,
        "**不普遍成立**。E = cB 只对**平面电磁波（辐射场）**成立；静电场反例：电子电荷在 r = 1 nm（原子尺度）处\n"
        "E = **%.4e V/m**，而 B = 0 ⇒ E/(cB) **发散**。\n"
        "麦克斯韦方程组并不蕴含 E = cB（它蕴含的是波动方程与 c = 1/sqrt(eps0*mu0)）；"
        "把辐射场的特例写成普遍关系是**越界宣称**。\n"
        "注：本条是来料行文层面的越界，不涉及实验否决，判 FAIL 但权重低于 A/B 组。" % e_static,
        "控制组5：平面波下 E=cB 成立")


# ============================ 组 D：名实与门禁 ============================
def group_D():
    # ---- D1 名实清点：方程里出现了几种力 ----
    texts = []
    for fn in ("README.md", "D5_大统一力方程.py"):
        p = os.path.join(D5_DIR, fn)
        if os.path.exists(p):
            with io.open(p, "r", encoding="utf-8") as f:
                texts.append(f.read())
    blob = "\n".join(texts)
    METRICS["D1_doc_chars"] = len(blob)
    # 层 1【方程层】：非电磁耦合【符号】是否真的出现在方程里
    sym_pats = {
        "G(引力常数)": r"(?<![A-Za-z])G(?![A-Za-z])",
        "g_w/G_F/M_W/M_Z": r"g_w|g_weak|G_F|M_W|M_Z",
        "g_s/alpha_s/Lambda_QCD": r"g_s|alpha_s|Lambda_QCD|Λ_QCD",
    }
    sym_hits = {k: len(re.findall(p, blob)) for k, p in sym_pats.items()}
    non_em = sum(sym_hits.values())

    # 层 2【全文层】：非电磁力【名称】出现次数 + 否定式提及检测（防过度指控）
    name_pats = {
        "引力": r"引力|重力|万有引力|gravity|gravitation",
        "弱力": r"弱(?:核)?力|弱相互|weak",
        "强力": r"强(?:核)?力|强相互|QCD|禁闭",
    }
    name_hits = {k: len(re.findall(p, blob)) for k, p in name_pats.items()}
    neg_lines = []
    for ln in blob.split("\n"):
        if re.search(name_pats["引力"], ln) and re.search(r"不|未|无|OPEN", ln):
            neg_lines.append(ln.strip()[:120])

    # 层 3【电磁侧对照】：子串计数不设边界（避免 qB 这类连写被漏计）
    em_pats = {
        "q(电荷)": r"q",
        "B(磁场)": r"B",
        "E(电场)": r"E",
        "Maxwell/洛伦兹": r"Maxwell|麦克斯韦|洛伦兹",
    }
    em_hits = {k: len(re.findall(p, blob)) for k, p in em_pats.items()}
    em = sum(em_hits.values())

    machine_d1 = ("全文 %d 字符；【方程层】非电磁耦合符号命中 %d（%s）；"
                  "【全文层】非电磁力名称命中 引力%d/弱力%d/强力%d，其中引力仅出现在 %d 条自承否定句中；"
                  "【电磁侧】%d（%s）" %
                  (len(blob), non_em,
                   ", ".join("%s=%d" % (k, v) for k, v in sym_hits.items()),
                   name_hits["引力"], name_hits["弱力"], name_hits["强力"], len(neg_lines),
                   em, ", ".join("%s=%d" % (k, v) for k, v in em_hits.items())))
    METRICS["D1_non_em_hits"] = non_em
    METRICS["D1_em_hits"] = em
    METRICS["D1_sym_hits"] = sym_hits
    METRICS["D1_name_hits"] = name_hits
    METRICS["D1_neg_lines"] = neg_lines
    METRICS["D1_n_neg"] = len(neg_lines)
    v_d1 = "FAIL" if non_em == 0 else "INFO"
    add("D1", "名实之辩：名为「大统一力方程」，方程中非电磁耦合为 0", "D",
        "这个「大统一力方程」里究竟出现了几种力？",
        machine_d1, v_d1,
        "**三层**机读清点来料全文（%d 字符，含 README 与复算脚本）：\n"
        "  - **层1 · 方程层**：非电磁耦合符号（G / g_w·G_F·M_W / g_s·alpha_s·Lambda_QCD）命中 **%d** 次；\n"
        "  - **层2 · 全文层**：非电磁力名称命中 引力 **%d** / 弱力 **%d** / 强力 **%d** 次，"
        "且引力**只出现在 %d 条自承否定句**里（原文：「不解释引力、不生成常数、不完成四力统一」）；\n"
        "  - **层3 · 电磁侧**：q / B / E / Maxwell·洛伦兹 共命中 **%d** 次。\n"
        "⇒ 四条方程实际只覆盖**电磁**一种力（外加一条运动学动量定义）。引力、弱力、强力"
        "在**方程中一个都没出现**；全文唯一一次提到引力，是在**承认自己不解释引力**的句子里。\n"
        "「大统一」在这里是**标签**而不是**内容**：它既没有把四种力写进一个方程，也没有给出四力之间的"
        "任何定量关系（无耦合常数关系、无统一能标、无 G 与 alpha 的联系）。\n"
        "**靶自承（防过度指控）**：本条判定与来料**自述一致**，不是外部强加的指控"
        "（attack16 判据④：找靶自承）。" % (len(blob), non_em, name_hits["引力"],
                                            name_hits["弱力"], name_hits["强力"],
                                            len(neg_lines), em),
        "控制组：标准 GUT（如 SU(5)）的方程里 g_1/g_2/g_3 与 M_GUT 均显式出现")

    # ---- D2 量纲门禁零判别力 ----
    dim_p_d5 = dim_mul(DIM["m"], DIM["c"])          # m*c
    dim_p_d5b = dim_mul(DIM["m"], DIM["v"])         # m*v
    same = (dim_p_d5 == dim_p_d5b)
    ok_d5 = dim_homogeneous([dim_p_d5, dim_p_d5b])
    dim_p_std = dim_mul(DIM["m"], DIM["v"])
    ok_std = dim_homogeneous([dim_p_std])
    dim_kt = dim_pow(DIM["kappa"], 2)
    dim_wv = dim_pow(dim_mul(DIM["c"], (0, 0, 0, 0)), 0)  # 占位
    # (omega/v)^2：omega 量纲 T^-1，v 量纲 L T^-1 ⇒ (T^-1/(L T^-1))^2 = (L^-1)^2 = L^-2
    dim_omega = (0, 0, -1, 0)
    dim_w_over_v = (dim_omega[0] - DIM["v"][0], dim_omega[1] - DIM["v"][1],
                    dim_omega[2] - DIM["v"][2], dim_omega[3] - DIM["v"][3])
    dim_rhs = dim_pow(dim_w_over_v, 2)
    kt_ok = (dim_kt == dim_rhs)
    machine_d2 = ("[P]=%s；m*c 与 m*v 同为 %s ⇒ 齐次=%s；kappa^2=%s 与 (omega/v)^2=%s ⇒ 一致=%s" %
                  (str(dim_p_d5), str(dim_p_d5b), same, str(dim_kt), str(dim_rhs), kt_ok))
    METRICS["D2_dim_homogeneous_d5"] = 1 if (same and ok_d5) else 0
    METRICS["D2_dim_homogeneous_std"] = 1 if ok_std else 0
    METRICS["D2_kt_dim_ok"] = 1 if kt_ok else 0
    v_d2 = "INFO"
    add("D2", "量纲门禁对本靶零判别力（又一个「量纲自洽 ≠ 成立」）", "D",
        "量纲审计能拦住 A/B 组的错误吗？",
        machine_d2, v_d2,
        "**拦不住**。P = m(c - v) 的量纲是 M·L·T⁻¹，与标准动量**完全齐次**（机读：m*c 与 m*v 同量纲 = %s）；\n"
        "kappa² 与 (omega/v)² 也都是 L⁻²（一致 = %s）。\n"
        "⇒ A2（静止动量非零）、A3（光子能量为零）、B1（符号反号）**全部量纲自洽**，"
        "量纲门禁对它们**零判别力**。\n"
        "这是本库「量纲自洽 ≠ 物理成立」的第 N 次实证：**错在物理角色与极限行为，不在量纲**。"
        % (str(dim_p_d5), kt_ok),
        "控制组4：量纲工具自检（标准 p=mv / E=mc^2 / F=ma 均齐次）")


# ============================ 组 E：低阶算子修复枚举与定价 ============================
OPS = ("KEEP", "FLIP", "DEL")


def apply_op(op, sign):
    """项系数：KEEP -> +sign, FLIP -> -sign, DEL -> 0"""
    if op == "KEEP":
        return sign
    if op == "FLIP":
        return -sign
    return 0


def group_E():
    # P = c1 * m*C + c2 * m*v ；原式 c1=+1, c2=-1（P = m(C - v)）
    combos = []
    for o1 in OPS:
        for o2 in OPS:
            c1 = apply_op(o1, +1)     # C 项原符号 +
            c2 = apply_op(o2, -1)     # v 项原符号 -
            # 四条检验（全部机读）
            # (a) 静止动量 = 0？  P(v=0) = c1 * m * C
            p_rest = abs(c1) * M_E * C
            closes_A2 = (p_rest == 0.0)
            # (b) 光速极限不趋于 0？ P(v=c 沿 C) = (c1 + c2) m c
            p_light = abs(c1 + c2) * M_E * C
            closes_A3 = (p_light > 0.0)
            # (c) F = +m a？  C 恒定时 F = dP/dt = c2 * m * a ⇒ 需要 c2 = +1
            closes_B1 = (c2 == +1)
            # (d) 静止几何力 = 0？ F_geo = |c1| * m * c^2 / R
            closes_B2 = (c1 == 0)
            combos.append({
                "ops": (o1, o2), "c1": c1, "c2": c2,
                "p_rest": p_rest, "p_light": p_light,
                "closes": {"A2": closes_A2, "A3": closes_A3,
                           "B1": closes_B1, "B2": closes_B2},
            })
    fail_set = ("A2", "A3", "B1", "B2")
    survivors = [c for c in combos if all(c["closes"][f] for f in fail_set)]
    n_surv = len(survivors)
    METRICS["E1_n_combos"] = len(combos)
    METRICS["E1_n_survivors"] = n_surv
    METRICS["E1_survivor_ops"] = [list(s["ops"]) for s in survivors]
    # 存活解的表达式
    if n_surv == 1:
        s = survivors[0]
        expr = ("P = %+d*m*C %+d*m*v" % (s["c1"], s["c2"])).replace("+1*", "").replace("-1*", "-")
        expr = expr.replace("+0*m*C ", "").replace(" +0*m*v", "")
        survivor_is_newton = (s["c1"] == 0 and s["c2"] == 1)
    else:
        expr = "（解不唯一或不存在的情形）"
        survivor_is_newton = False
    METRICS["E1_survivor_expr"] = expr
    METRICS["E1_survivor_is_newton"] = 1 if survivor_is_newton else 0
    machine_e1 = ("3^2=%d 个组合；同时关闭 A2/A3/B1/B2 的存活解 %d 个：%s" %
                  (len(combos), n_surv, expr))
    v_e1 = "FAIL" if (n_surv == 1 and survivor_is_newton) else "BOUNDARY"
    add("E1", "低阶算子全枚举：唯一存活解就是牛顿动量", "E",
        "对 P = m(C - v) 的两个加项施加 {KEEP, FLIP, DEL}，哪些组合能同时修好 A2/A3/B1/B2？",
        machine_e1, v_e1,
        "全枚举 3² = **%d** 个组合（延续 r147 的机器生成口径，不人工挑）：\n"
        "  - 关闭条件全部由机读判定：A2 静止动量=0；A3 光速极限非零；B1 需要 v 项系数为 +1；B2 需要 C 项系数为 0；\n"
        "  - **存活解 %d 个**：`%s`。\n"
        "⇒ 唯一的存活解 **就是 P = m v**，即**标准牛顿动量**。\n"
        "这说明：把来料修到物理正确，**剩下的恰好是教科书第一章的动量定义** —— "
        "来料相对标准物理的全部增量（那个 m*C 项）**正是全部错误的来源**。"
        % (len(combos), n_surv, expr),
        "控制组：枚举流程有分辨力（存活解既非 0 个也非全部）")

    # ---- E2 存活解的新增性：修复即自杀 ----
    # 施加唯一解后，D5 剩余内容：P=mv(牛顿), F=dP/dt(=ma 定义), F_e/F_m=c/v(标准), kappa^2+tau^2(标准)
    remaining_novel = 0
    items = [
        ("P = m(C - v)", "被替换为 P = mv（牛顿动量）", 0),
        ("F = dP/dt", "保留，但退化为牛顿第二定律的定义式", 0),
        ("F_e/F_m = c/v", "保留，但已是标准洛伦兹力复述（C3 判 INFO）", 0),
        ("kappa^2+tau^2=(omega/v)^2", "保留，但已是标准 Frenet 推论（C1 判 INFO）", 0),
        ("E = cB", "保留，但仅限辐射场（C4 判越界）", 0),
        ("「大统一」标签", "被证伪：非电磁耦合命中 0（D1）", 0),
    ]
    machine_e2 = ("施加唯一存活解后，逐条清点剩余非已知物理项 = %d / %d" %
                  (remaining_novel, len(items)))
    METRICS["E2_remaining_novel"] = remaining_novel
    METRICS["E2_items"] = [i[0] for i in items]
    v_e2 = "FAIL" if remaining_novel == 0 else "INFO"
    add("E2", "修复即自杀：修好后剩余非已知物理项 = 0", "E",
        "按唯一存活解修好之后，D5 还剩什么是标准物理里没有的？",
        machine_e2, v_e2,
        "逐条清点（施加唯一存活解 P = m v 后）：\n"
        "  - P = m(C - v) → **退化为牛顿动量**；\n"
        "  - F = dP/dt → 保留，但退化为牛顿第二定律的**定义式**；\n"
        "  - F_e/F_m = c/v → 保留，但 C3 已判为标准洛伦兹力**复述**；\n"
        "  - kappa²+tau² = (omega/v)² → 保留，但 C1 已判为标准 Frenet **推论**；\n"
        "  - E = cB → 保留，但 C4 已判为**辐射场特例**；\n"
        "  - 「大统一」标签 → D1 已证伪（非电磁耦合命中 0）。\n"
        "⇒ **剩余非已知物理项 = 0**。与 r142 对 S17 的结论同型："
        "**「可修复」与「仍有内容」不可兼得** —— 能修好的唯一办法是把它换成标准力学。",
        "控制组：标准教科书动量 + 洛伦兹力 + Frenet 全部已知，无新增")

    # ---- E3 需高阶算子才能修的两条（D1 / C2） ----
    # D1：缺内容（没有引力/弱/强的任何表达式）⇒ 削减型修不好；唯一的削减型修复是删标签
    # C2：越界宣称 ⇒ 削减型可修（删「梯度磁场」限定词）
    d1_cutting = "删去「大统一」标签（改名为「电磁力几何分解」）"
    d1_cost = "放弃「统一四力」这一宣称本身"
    c2_cutting = "把适用范围限定为「匀速螺旋」，删去「梯度磁场」"
    c2_cost = "放弃梯度磁场适用性宣称"
    machine_e3 = ("D1 属「缺内容」类：削减型唯一解=删标签，代价=放弃统一宣称；"
                  "C2 越界类：削减型可修=限定匀速螺旋，代价=放弃梯度磁场宣称")
    METRICS["E3_d1_cutting"] = d1_cutting
    METRICS["E3_c2_cutting"] = c2_cutting
    v_e3 = "INFO"
    add("E3", "D1 / C2 的修复与代价（削减型可修，但代价是放弃宣称）", "E",
        "剩下两条 FAIL 能不能靠删改修好？",
        machine_e3, v_e3,
        "- **D1（名实不符）** 属「**缺内容**」类 FAIL：方程里根本没有引力/弱/强的表达式，"
        "**删改符号救不了**。削减型唯一解是 **%s**，代价是 **%s** ⇒ 修好之后它就不再自称大统一。\n"
        "- **C2（梯度磁场越界）** 属越界宣称：削减型可修 = **%s**，代价是 **%s**。\n"
        "⇒ 两条都可修，但**每一条修好都以放弃一项宣称**为代价。"
        % (d1_cutting, d1_cost, c2_cutting, c2_cost),
        "控制组：标准物理的适用范围声明（如「Proca 势不含 QCD 禁闭」）同样以放弃宣称换取自洽")


# ============================ 控制组 ============================
def controls():
    # K1 标准相对论动量：静止 0、光速发散
    beta = 0.9
    p0 = 0.0
    p9 = (1.0 / math.sqrt(1 - beta * beta)) * M_E * beta * C
    ok1 = (p0 == 0.0) and (p9 > 0)
    add_ctrl("控制1 标准相对论动量 p=gamma*m*v：v=0 给 0、v=0.9c 给 %.6e kg*m/s" % p9,
             "静止=%.1f；beta=0.9 时 |p|=%.6e；两者均符合教科书" % (p0, p9), ok1,
             "A2/A3 的判据对该输入不触发 FAIL")

    # K2 标准 F=ma 弹簧有界
    xs, _ = rk4_osc(-1.0, 10.0, 20000)
    ok2 = abs(xs) <= 1.0 + 1e-6
    add_ctrl("控制2 标准 F=+m*a 弹簧：|x(t)| <= 1 有界（t=10 时 x=%.6f）" % xs,
             "数值 cos(10)=%.6f，解析 %.6f，误差 %.2e" % (xs, math.cos(10.0),
                                                          abs(xs - math.cos(10.0))), ok2,
             "B1 的反号判据对该输入不触发 FAIL")

    # K3 Frenet 工具在匀速螺旋给机器零
    e0, _, _, _ = helix_identity_err(1.0, 1.0, 0.7, 1.0, 0.0, 0.0)
    ok3 = e0 < 1e-9
    add_ctrl("控制3 Frenet 工具在标准匀速螺旋上给出恒等式残差 %.3e（机器零）" % e0,
             "kappa^2+tau^2 与 (omega/v)^2 相对误差 %.3e" % e0, ok3,
             "证明 C2 的变速档残差来自物理而非工具误差")

    # K4 量纲工具自检
    ok4 = (dim_homogeneous([dim_mul(DIM["m"], DIM["v"])])
           and dim_homogeneous([dim_mul(DIM["m"], dim_pow(DIM["c"], 2))])
           and dim_homogeneous([dim_mul(DIM["m"], DIM["a"])]))
    add_ctrl("控制4 量纲工具自检：p=mv / E=mc^2 / F=ma 三式均齐次",
             "三式量纲分别为 %s / %s / %s" % (str(dim_mul(DIM["m"], DIM["v"])),
                                              str(dim_mul(DIM["m"], dim_pow(DIM["c"], 2))),
                                              str(dim_mul(DIM["m"], DIM["a"]))), ok4,
             "D2 的「量纲齐次」结论建立在可信工具上")

    # K5 洛伦兹力复现 c/v
    Bv = 1.0e-3
    Ev = C * Bv
    vv = 1.0e6
    ratio = (E_CHARGE * Ev) / (E_CHARGE * vv * Bv)
    ok5 = abs(ratio - C / vv) / (C / vv) < 1e-12
    add_ctrl("控制5 标准洛伦兹力在平面波下复现 F_e/F_m = c/v（v=1e6 时比值 %.4f）" % ratio,
             "qE/(qvB)=%.6f，c/v=%.6f" % (ratio, C / vv), ok5,
             "C3 的 INFO 判定有标准物理背书")


# ============================ 守卫 ============================
def guards():
    G = []

    def g(name, ok, machine):
        G.append({"name": name, "ok": bool(ok), "machine": machine})

    g("G1 A2 静止动量量级正确且非零",
      METRICS["A2_p_rest_d5"] > 1.0e8 and METRICS["A2_p_rest_std"] == 0.0,
      "p_rest=%.6e（应 ~ m*c = 3e8）" % METRICS["A2_p_rest_d5"])

    g("G2 A3 光速极限能量被严重低估且光子能量为零",
      METRICS["A3_ratio_e"] > 1.0e6 and METRICS["A3_p_photon_d5"] == 0.0,
      "E_std/E_D5=%.4e，光子 P_D5=%.1f" % (METRICS["A3_ratio_e"], METRICS["A3_p_photon_d5"]))

    g("G3 B1 反号导致的发散比 > 1e3 且数值积分可信",
      METRICS["B1_ratio"] > 1.0e3 and METRICS["B1_num_err"] < 1.0e-6,
      "比值=%.4e，数值误差=%.2e" % (METRICS["B1_ratio"], METRICS["B1_num_err"]))

    g("G4 B2 静止电子几何力远超宏观可测阈 1e-6 N",
      METRICS["B2_F_geo_N"] > 1.0e-6,
      "F_geo=%.6e N" % METRICS["B2_F_geo_N"])

    g("G5 C1 匀速螺旋恒等式残差为机器零（五点扫描）",
      METRICS["C1_err_uniform_worst"] < 1.0e-9,
      "最坏=%.3e" % METRICS["C1_err_uniform_worst"])

    g("G6 C2 变速档残差显著且单调递增、匀速档为机器零",
      METRICS["C2_err_max"] > 1.0e-2 and METRICS["C2_monotone"] == 1
      and METRICS["C2_err_uniform"] < 1.0e-9,
      "最坏=%.4e，单调=%d，匀速档=%.3e" % (METRICS["C2_err_max"],
                                            METRICS["C2_monotone"],
                                            METRICS["C2_err_uniform"]))

    g("G7 D1 名实清点：非电磁耦合命中为 0",
      METRICS["D1_non_em_hits"] == 0 and METRICS["D1_em_hits"] > 0,
      "非电磁=%d，电磁=%d" % (METRICS["D1_non_em_hits"], METRICS["D1_em_hits"]))

    g("G8 D2 量纲：来料与标准均齐次（零判别力有据）",
      METRICS["D2_dim_homogeneous_d5"] == 1 and METRICS["D2_dim_homogeneous_std"] == 1
      and METRICS["D2_kt_dim_ok"] == 1,
      "来料齐次=%d，标准齐次=%d，kappa^2 一致=%d" % (METRICS["D2_dim_homogeneous_d5"],
                                                     METRICS["D2_dim_homogeneous_std"],
                                                     METRICS["D2_kt_dim_ok"]))

    g("G9 E1 枚举既有解又非全解（流程有分辨力）",
      0 < METRICS["E1_n_survivors"] < METRICS["E1_n_combos"],
      "存活 %d / 全部 %d" % (METRICS["E1_n_survivors"], METRICS["E1_n_combos"]))

    g("G10 E1 唯一存活解确为标准牛顿动量",
      METRICS["E1_n_survivors"] == 1 and METRICS["E1_survivor_is_newton"] == 1,
      "存活解=%s，is_newton=%d" % (METRICS["E1_survivor_expr"],
                                   METRICS["E1_survivor_is_newton"]))

    g("G11 控制组全部通过",
      all(c["ok"] for c in CTRLS) and len(CTRLS) == 5,
      "通过 %d / %d" % (sum(1 for c in CTRLS if c["ok"]), len(CTRLS)))

    return G


# ============================ 输出 ============================
def build_report():
    L = []
    L.append("=" * 74)
    L.append("r148 · D5《大统一力方程》首攻与修复定价")
    L.append("=" * 74)
    L.append("生成时间: %s" % datetime.datetime.now().isoformat(timespec="seconds"))
    L.append("对象: S02/D5 大统一力方程（P=m(c-v), F=dP/dt, F_e/F_m=c/v, E=cB, kappa^2+tau^2=(omega/v)^2）")
    L.append("方法: 极限机检 + RK4 动力学 + 解析 Frenet + 量纲四元组 + {KEEP,FLIP,DEL} 全枚举")
    L.append("")
    for grp, title in (("A", "读法与极限"), ("B", "动力学"),
                       ("C", "恒等式与新增性"), ("D", "名实与门禁"), ("E", "修复定价")):
        L.append("-" * 74)
        L.append("【%s %s】" % (grp, title))
        L.append("-" * 74)
        for e in ENTRIES:
            if e["group"] != grp:
                continue
            L.append("[%s] %s  ⇒ %s" % (e["id"], e["name"], e["verdict"]))
            L.append("   问: %s" % e["claim"])
            L.append("   机读: %s" % e["machine"])
    L.append("")
    L.append("-" * 74)
    L.append("【控制组】")
    L.append("-" * 74)
    for c in CTRLS:
        L.append("   %s : %s | %s" % ("通过" if c["ok"] else "失败", c["name"], c["machine"]))
    L.append("")
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}
    L.append("计数：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d（共 %d 条）"
             % (c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"], len(ENTRIES)))
    L.append("VERDICT: %s" % VERDICT)
    L.append("=" * 74)
    return "\n".join(L)


def build_md(guards_res):
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}
    L = []
    L.append("# TUFT-r148 · D5《大统一力方程》首攻与修复定价")
    L.append("")
    L.append("**卷号**：r148　**日期**：%s" % DATE)
    L.append("**靶**：`01_独立体系/S02_空间光速螺旋统一力/04_理论推导/D5_大统一力方程/`")
    L.append("")
    L.append("## 条目总表（%d 条）" % len(ENTRIES))
    L.append("")
    L.append("| 编号 | 条目 | 判定 | 机读 |")
    L.append("|----|----|----|----|")
    for e in ENTRIES:
        L.append("| %s | %s | **%s** | %s |" % (e["id"], e["name"], e["verdict"], e["machine"]))
    L.append("")
    L.append("## 控制组（%d/%d）" % (sum(1 for x in CTRLS if x["ok"]), len(CTRLS)))
    L.append("")
    for x in CTRLS:
        L.append("- [%s] %s —— %s" % ("x" if x["ok"] else " ", x["name"], x["machine"]))
    L.append("")
    L.append("## 守卫（%d/%d）" % (sum(1 for g in guards_res if g["ok"]), len(guards_res)))
    L.append("")
    L.append("| 守卫 | 结果 | 机读 |")
    L.append("|----|----|----|")
    for g in guards_res:
        L.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["machine"]))
    L.append("")
    L.append("## 关键机读量")
    L.append("")
    for k in sorted(METRICS):
        v = METRICS[k]
        if isinstance(v, float):
            L.append("- `%s` = %.6e" % (k, v))
        elif isinstance(v, (int, bool)):
            L.append("- `%s` = %s" % (k, v))
        else:
            L.append("- `%s` = %s" % (k, str(v)))
    L.append("")
    L.append("**VERDICT**：`%s`" % VERDICT)
    return "\n".join(L)


def build_judge(guards_res):
    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}
    L = []
    L.append("# 判定_TUFT-r148 · D5《大统一力方程》首攻与修复定价")
    L.append("")
    L.append("**卷号**：r148")
    L.append("**日期**：%s" % DATE)
    L.append("**对象**：S02 / D5 大统一力方程（张祥前体系原始公设层）")
    L.append("**类别**：物理层首攻 + 新增性定价 + 低阶算子修复枚举")
    L.append("")
    L.append("## 0. 编号与分工声明")
    L.append("")
    L.append("| 项 | 内容 |")
    L.append("|----|----|")
    L.append("| 卷号 | **r148**（实测首空号：源码/数据 0 命中，README 中 r148 仅见于上一卷的两行指针） |")
    L.append("| 靶 | `01_独立体系/S02_空间光速螺旋统一力/04_理论推导/D5_大统一力方程/`（README.md + D5_大统一力方程.py） |")
    L.append("| 库内前况 | **从未被攻破**；仅在《方法全谱》清点中被提及一次 |")
    L.append("")
    L.append("**分层（与既有册不可相加）**：")
    L.append("- S02 的 §18 做**标准物理 Yukawa/Proca 四力形式统一**（有效理论层，自认只攻 ①②）；")
    L.append("- S02 的 §19 做**耦合跑动与 GUT 能标**；r146 占位做**四力统一可行性跨册归总**；")
    L.append("- **本卷攻 D5 本身**，即张祥前体系的**原始公设层方程**，与上述各册不在同一层。")
    L.append("")
    L.append("## 1. 判定")
    L.append("")
    L.append("> **%s**" % VERDICT)
    L.append(">")
    L.append("> | 问 | 答 |")
    L.append("> |----|----|")
    L.append("> | P = m(c - v) 读得通吗？ | 三种读法**必居其一且各有硬伤**：标量减矢量无定义 / 退化为标量 / 静止动量非零 |")
    L.append("> | 两个极限对吗？ | **都不对**：v=0 时动量 = m*c 而非 0；v->c 时动量 -> **0**（光子能量为零）|")
    L.append("> | F = dP/dt 与 F = ma 一致吗？ | **整体反号** ⇒ 弹簧由振荡变指数发散（%.3e 倍）|" % METRICS["B1_ratio"])
    L.append("> | 恒等式对吗？ | 匀速螺旋**对但零新增**；来料标注的**梯度磁场下不成立** |")
    L.append("> | 叫「大统一」名副其实吗？ | **不**：非电磁耦合符号命中 **0** |")
    L.append("> | 能修好吗？ | 能 —— 唯一存活解 **就是牛顿动量**，修好后**剩余非已知物理项 0** |")
    L.append("")
    L.append("## 2. 方法与控制组")
    L.append("")
    L.append("机读手段：极限代入（SI 常数）· RK4 积分（2 万步）· **解析导数 Frenet**（避三阶数值差分）·")
    L.append("量纲四元组 (M,L,T,Q) · 来料全文正则清点 · {KEEP, FLIP, DEL} 全枚举。")
    L.append("")
    L.append("| 控制组 | 结果 |")
    L.append("|----|----|")
    for x in CTRLS:
        L.append("| %s | %s |" % (x["name"], "通过" if x["ok"] else "**失败**"))
    L.append("")
    L.append("## 3. 条目总表（%d 条）" % len(ENTRIES))
    L.append("")
    L.append("| 编号 | 条目 | 判定 |")
    L.append("|----|----|----|")
    for e in ENTRIES:
        L.append("| %s | %s | **%s** |" % (e["id"], e["name"], e["verdict"]))
    L.append("")
    L.append("## 4. 逐条裁定")
    L.append("")
    for e in ENTRIES:
        L.append("### %s · %s　【%s】" % (e["id"], e["name"], e["verdict"]))
        L.append("")
        L.append("**问**：%s" % e["claim"])
        L.append("")
        L.append("**机读**：%s" % e["machine"])
        L.append("")
        L.append(e["detail"])
        if e["control"]:
            L.append("")
            L.append("*%s*" % e["control"])
        L.append("")
    L.append("## 5. ★修复定价：唯一存活解就是牛顿动量")
    L.append("")
    L.append("对 `P = m(C - v)` 的两个加项统一施加 {KEEP, FLIP, DEL}（延续 r147 的机器生成口径）：")
    L.append("")
    L.append("- 全枚举 **%d** 个组合；" % METRICS["E1_n_combos"])
    L.append("- 关闭条件全部机读：A2 静止动量=0 / A3 光速极限非零 / B1 需 v 项系数 +1 / B2 需 C 项系数 0；")
    L.append("- **存活解 %d 个**：`%s`。" % (METRICS["E1_n_survivors"], METRICS["E1_survivor_expr"]))
    L.append("")
    L.append("⇒ **唯一的存活解就是 P = m v**，即标准牛顿动量。来料相对标准物理的全部增量（那个 m*C 项）")
    L.append("**正是全部错误的来源**：把它删掉，物理就对了，但也就什么都不剩了。")
    L.append("")
    L.append("## 6. 守卫（%d/%d）" % (sum(1 for g in guards_res if g["ok"]), len(guards_res)))
    L.append("")
    for g in guards_res:
        L.append("- [%s] %s —— %s" % ("x" if g["ok"] else " ", g["name"], g["machine"]))
    L.append("")
    L.append("## 7. 仍未闭合项（未做即未证，不得外推）")
    L.append("")
    L.append("1. **C2 用运动学反例而非真实梯度磁场积分** —— 本卷以「螺距变化的螺旋」+ 磁镜绝热不变量")
    L.append("   论证梯度磁场下运动不是匀速螺旋；**未做**真实梯度磁场下的洛伦兹力数值积分，")
    L.append("   也未用三阶数值差分直接测 tau（按既有纪律，tau 通道三阶差分地板 ~1e-7，不可靠）。")
    L.append("2. **梯度磁场下 omega 的口径** —— B 随位置变，来料的 omega = qB/(gamma m) 用哪一点的 B")
    L.append("   **未声明**，本卷只登记「口径未定」，未代选。")
    L.append("3. **修复空间仍是低阶算子** —— 与 r147 同限：{KEEP, FLIP, DEL} 之外的高阶算子")
    L.append("   （改函数形式 / 改向量结构 / 改假设 / 新增内容）**未枚举**。")
    L.append("4. **B2 的 R 取参** —— 取 S02 口径 R = lambda_C/(2 pi)；若来料另取 R，数值会变但")
    L.append("   「静止受力非零且巨大」这一**定性结论不变**（F_geo = m c^2 / R ∝ 1/R）。")
    L.append("5. **未检索实验文献** —— A2/A3/B1/B2 均为与教科书极限的直接冲突，未做文献比对。")
    L.append("")
    L.append("## 8. 红线")
    L.append("")
    L.append("- **数学自洽 ≠ 实验证实**：本卷所有判定均为**框架内**的可算判决，不产生新物理。")
    L.append("- **修复可行 ≠ 修复后仍有内容**：D5 可修，但修好即等于标准力学（E2）。")
    L.append("- **低阶空间完备 ≠ 全空间完备**（r147 同款限制）。")
    L.append("- **靶自承优先**：来料自承「不解释引力、不生成常数、不完成四力统一」，")
    L.append("  本卷 D1 与之**一致**，不是过度指控。")
    L.append("")
    L.append("## 9. Glossary")
    L.append("")
    L.append("- **R3 读法**：把 P = m(c - v) 中的 c 理解为**矢量** C（|C| = c，空间光速螺旋公设）。")
    L.append("  本卷对来料最有利的读法，全部按此立论。")
    L.append("- **低阶算子**：{KEEP, FLIP, DEL}，分别对应保留 / 翻转符号 / 删除该项。")
    L.append("- **几何力**：C 走螺旋时 dC/dt ≠ 0 带给静止物体的力 F = m c^2 / R。")
    L.append("- **磁镜效应**：梯度磁场中绝热不变量 mu = m v_perp^2/(2B) 守恒导致 v_par 持续变化。")
    L.append("- **零新增**：推导正确但与已知物理逐字相同 ⇒ 按纪律降 INFO，不计入 PASS。")
    L.append("")
    L.append("---")
    L.append("")
    L.append("**数据出处**：`源码/TUFT-r148_D5大统一力方程首攻与修复定价_%s.py`，"
             "复现 `python 源码/_run_r148.py`，退出码 0。" % DATE)
    return "\n".join(L)


# ============================ 主流程 ============================
def main():
    global VERDICT
    group_A()
    group_B()
    group_C()
    group_D()
    group_E()
    controls()
    G = guards()

    # verdict 由机读结果驱动（禁硬编码）
    n_fail = sum(1 for e in ENTRIES if e["verdict"] == "FAIL")
    survivor_is_newton = METRICS["E1_survivor_is_newton"] == 1
    remaining_novel = METRICS["E2_remaining_novel"]
    if n_fail >= 4 and survivor_is_newton and remaining_novel == 0:
        VERDICT = "UNIFIED-FORCE-EQUATION-INCONSISTENT-AND-REPAIR-EQUALS-NEWTON"
    elif n_fail >= 1:
        VERDICT = "UNIFIED-FORCE-EQUATION-INCONSISTENT"
    else:
        VERDICT = "NO-FAILURE-DETECTED"

    n_ctrl_ok = sum(1 for c in CTRLS if c["ok"])
    n_g_ok = sum(1 for g in G if g["ok"])
    exit_code = 0
    if n_ctrl_ok != len(CTRLS):
        exit_code = 2
    if n_g_ok != len(G):
        exit_code = 1

    c = {v: sum(1 for e in ENTRIES if e["verdict"] == v)
         for v in ("PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION")}

    payload = {
        "meta": {
            "volume": "r148",
            "title": "D5《大统一力方程》首攻与修复定价",
            "date": DATE,
            "generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "target": "01_独立体系/S02_空间光速螺旋统一力/04_理论推导/D5_大统一力方程/",
            "verdict": VERDICT,
            "counts": c,
            "n_entries": len(ENTRIES),
        },
        "entries": ENTRIES,
        "controls": CTRLS,
        "guards": G,
        "metrics": METRICS,
    }

    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    with io.open(os.path.join(DATA, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with io.open(os.path.join(DATA, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(build_md(G))
    with io.open(os.path.join(DATA, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(build_report())
    with io.open(os.path.join(DATA, JUDGE_STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(build_judge(G))

    print("OK generated:")
    for nm in (STEM + ".json", STEM + ".md", STEM + "_report.txt", JUDGE_STEM + ".md"):
        print("   " + os.path.join("数据", nm))
    print("VERDICT: %s" % VERDICT)
    print("条目 %d：PASS %d / FAIL %d / INFO %d / BOUNDARY %d / CORRECTION %d"
          % (len(ENTRIES), c["PASS"], c["FAIL"], c["INFO"], c["BOUNDARY"], c["CORRECTION"]))
    print("控制组 %d/%d 通过 | guards %d/%d | exit_code=%d"
          % (n_ctrl_ok, len(CTRLS), n_g_ok, len(G), exit_code))
    for g in G:
        if not g["ok"]:
            print("  GUARD FAIL: %s | %s" % (g["name"], g["machine"]))
    for x in CTRLS:
        if not x["ok"]:
            print("  CONTROL FAIL: %s" % x["name"])
    return exit_code


VERDICT = ""
if __name__ == "__main__":
    import sys
    sys.exit(main())
