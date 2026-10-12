# -*- coding: utf-8 -*-
"""
判定：TUFT-V4 完整耦合演化场方程组（爱因斯坦-嘉唐 EC + ADM-BSSN）· 全维机器审计（r39）
===================================================================================
来料：《TUFT-V4 完整耦合演化场方程组（适配 ADM-BSSN 数值相对论）》
  符号索引 + 前置恒等式 (1)(2)(3)(4)
  第一部分 流形层：嘉唐场方程 (5)、挠率映射 (6)(7)、螺旋场能动张量 (8)、约束势 (9)
  第二部分 动力学：kappa/tau 协变波动方程 (10)(11) + 物质源项 (12) + 弱场牛顿极限校验
  第三部分 ADM-BSSN 3+1 分解：共轭动量 (13)(14)、演化 (15)(16)、动量演化 (17)(18)、约束集合
  第四部分 边界条件与初始数据
  第五部分 与旧体系对照审计（4 条对照 + 5 条自评）
  末尾：请用户在 任务A（高精度 G_th 数值原型）/ 任务B（g-2 挠率修正）之间选择

本册职责：对**可判定的每一条定量/结构性论断**做独立机器核验（纯标准库；
  Fraction 精确四元组量纲代数 (M,L,T,Q) + Decimal 60 位读数 + 解析/数值双路径对拍），
  **只判「论断在其自称口径下是否成立」，不代选（A/B 交用户）、不自推未验证的系数。**

本册自研 machinery（beyond-citation 技术增量）：
  (A) 四元组量纲代数 (M,L,T,Q)：对 (3)(4)(8)(9)(10)(11)(12)(17)(18) 逐项齐次性判定。
  (B) 三角函数规避参数化：Decimal 无 sin/cos，改以 s=sin(theta) 为自由参数、
      cos=sqrt(1-s^2)、cot=sqrt(1-s^2)/s，全部 Decimal 精确可算 —— 使「tau==0 定理」
      与「冗余定理」可被机器证明。
  (C) 冗余/恒零判据：dV/dtau = cot*dV/dkappa 且 S_tau = cot*S_kappa ⇒ (11) == cot*(10)。
  (D) 牛顿还原两难定理：G_th*sin^2(theta)=G_exp 与 tau/kappa=cot(theta) 联立闭式解。

运行：python TUFT-r39_V4-EC-ADMBSSN耦合场方程组_全维审计_2026-10-12.py
产物：数据/TUFT-r39_V4-EC-ADMBSSN耦合场方程组_全维审计_2026-10-12.{json,md,_report.txt}
===================================================================================
"""
import json, os, sys
from decimal import Decimal as Dc, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RESULTS = []       # [id, verdict, title, detail]
GUARDS = []        # (id, ok, note)
KEYNUM = {}        # name -> string
NOT_SELF_DERIVED = []


def rec(rid, verdict, title, detail):
    RESULTS.append([rid, verdict, title, detail])


def guard(rid, ok, note):
    GUARDS.append((rid, bool(ok), note))


def nsli(s):
    NOT_SELF_DERIVED.append(s)


def E(x):
    return format(Dc(x), ".25E")


def rel(a, b):
    a, b = Dc(a), Dc(b)
    m = max(abs(a), abs(b))
    if m == 0:
        return Dc(0)
    return abs(a - b) / m


# ======================= 0. 量纲代数：四元组 (M,L,T,Q)，Fraction 精确 =======================
def dim(m=0, l=0, t=0, q=0):
    return (Fr(m), Fr(l), Fr(t), Fr(q))


def dadd(*ds):
    """同量纲项的【加法】：各项必须同量纲，返回该量纲；不齐次时返回 None。
    注意（本册自抓）：首版把加法写成指数逐分量相加，导致 dadd(x,x) 把量纲翻倍
    ⇒ T02/T16/T18/T27 全部误判。加法不改变量纲，乘法（dmul）才是指数相加。"""
    if not ds:
        return (Fr(0), Fr(0), Fr(0), Fr(0))
    base = tuple(ds[0])
    for d in ds[1:]:
        if tuple(d) != base:
            return None
    return base


def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def dmuln(a, n):
    neg = n < 0
    k = abs(int(n))
    out = (Fr(0), Fr(0), Fr(0), Fr(0))
    for _ in range(k):
        out = dmul(out, a)
    if neg:
        out = (-out[0], -out[1], -out[2], -out[3])
    return out


def dpow(a, n):
    return dmuln(a, n)


def dinv(a):
    return (-a[0], -a[1], -a[2], -a[3])


def dsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3])


def dstr(d):
    def f(x):
        return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
    return "M^%s L^%s T^%s Q^%s" % (f(d[0]), f(d[1]), f(d[2]), f(d[3]))


def dim_eq(a, b):
    return tuple(a) == tuple(b)


# ======================= 1. 常量（SI / CODATA 口径，与 r18/r19/r22/r27/r37 同源） =======================
PI = Dc("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899")
G_SI = Dc("6.67430e-11")
C_SI = Dc("299792458")
HBAR = Dc("1.054571817e-34")
QE = Dc("1.602176634e-19")
ALPHA = Dc("7.2973525693e-3")
M_E = Dc("9.1093837015e-31")
M_P = Dc("1.67262192369e-27")
M_PL_KG = Dc("2.176434e-8")
LP = (HBAR * G_SI / (C_SI ** 3)).sqrt()
ANCHOR_C4_8PIG = C_SI ** 4 / (8 * PI * G_SI)

DIM_C = dim(0, 1, -1, 0)
DIM_HBAR = dim(1, 2, -1, 0)
DIM_KAPPA = dim(0, -1, 0, 0)
DIM_TAU = dim(0, -1, 0, 0)
DIM_OMEGA = dim(0, 0, -1, 0)
DIM_G_TRUE = dim(-1, 3, -2, 0)
DIM_RHO = dim(1, -3, 0, 0)
DIM_ACC = dim(0, 1, -2, 0)
DIM_EDENS = dim(1, -1, -2, 0)
DIM_L = dim(0, 1, 0, 0)
DIM_T = dim(0, 0, 1, 0)
DIM_M = dim(1, 0, 0, 0)
DIM_NONE = dim(0, 0, 0, 0)


# ======================= 2. guard 段 0：量纲工具与常量自检（先自检，再用于判定） =======================
def guards_stage0():
    guard("G0-1", dim_eq(dmul(DIM_L, DIM_L), dim(0, 2, 0, 0)), "dmul 必须为指数相加")
    guard("G0-2", dim_eq(dpow(DIM_C, -2), dim(0, -2, 2, 0)), "dpow 负指数")
    guard("G0-3", dim_eq(dmul(DIM_C, dinv(DIM_C)), DIM_NONE), "c*c^-1 无量纲")
    guard("G0-4", dim_eq(dmul(DIM_HBAR, DIM_OMEGA), dim(1, 2, -2, 0)), "hbar*omega = 能量")
    guard("G0-5", dim_eq(dmul(DIM_M, dpow(DIM_C, 2)), dim(1, 2, -2, 0)), "E = m c^2")
    guard("G0-6", dim_eq(dpow(DIM_KAPPA, 2), dim(0, -2, 0, 0)), "[kappa^2] = L^-2")
    guard("G0-7", dim_eq(dsub(dpow(DIM_OMEGA, 2), dpow(DIM_C, 2)), dim(0, -2, 0, 0)),
          "[omega^2/c^2] = L^-2")
    guard("G0-8", dim_eq(dmul(DIM_G_TRUE, DIM_RHO), dim(0, 0, -2, 0)), "[G rho] = T^-2")
    guard("G0-9", dim_eq(dsub(dmul(DIM_G_TRUE, DIM_RHO), dpow(DIM_C, 2)), dim(0, -2, 0, 0)),
          "[G rho/c^2] = L^-2")
    guard("G0-10", dim_eq(dsub(dpow(DIM_C, 4), DIM_G_TRUE), dim(1, 1, -2, 0)), "[c^4/G] = 力")
    guard("G0-11", abs(ANCHOR_C4_8PIG / Dc("4.8154538867224223992518906E+42") - Dc(1)) < Dc("1e-20"),
          "锚点 c^4/(8 pi G) 与库内 r18/r19/r22/r27 逐位一致")
    guard("G0-12", abs(LP / Dc("1.616255e-35") - Dc(1)) < Dc("1e-5"), "普朗克长度量级")
    guard("G0-13", dim_eq(dsub(dmul(DIM_HBAR, DIM_G_TRUE), dpow(DIM_C, 3)), dim(0, 2, 0, 0)),
          "[hbar G/c^3] = L^2 = [l_P^2]")
    guard("G0-14", dim_eq(dmul(DIM_ACC, DIM_NONE), DIM_ACC), "加速度量纲登记")


# ======================= 3. 段 A：符号表与前置恒等式 (1)(2)(3)(4) =======================
def stage_A():
    table = [
        ("c", DIM_C, dim(0, 1, -1, 0)),
        ("hbar", DIM_HBAR, dim(1, 2, -1, 0)),
        ("G_th", DIM_G_TRUE, dim(-1, 3, -2, 0)),
        ("kappa", DIM_KAPPA, dim(0, -1, 0, 0)),
        ("tau", DIM_TAU, dim(0, -1, 0, 0)),
        ("omega", DIM_OMEGA, dim(0, 0, -1, 0)),
        ("rho", DIM_RHO, dim(1, -3, 0, 0)),
        ("g_vec", DIM_ACC, dim(0, 1, -2, 0)),
    ]
    bad = [n for n, a, b in table if not dim_eq(a, b)]
    rec("T01", "PASS" if not bad else "FAIL", "符号表量纲自报核对（8 项）",
        "逐项核对来料符号索引自报量纲：全部与标准 SI 量纲一致（不一致项=%s）。注：G_th 在符号表中"
        "自报为 [L^3 M^-1 T^-2]，但式(4) 的表达式并不给出该量纲（见 T06）。" % (bad or "无"))

    lhs1 = dadd(dpow(DIM_KAPPA, 2), dpow(DIM_TAU, 2))
    rhs1 = dmul(dpow(DIM_OMEGA, 2), dinv(dpow(DIM_C, 2)))
    ok = dim_eq(lhs1, rhs1)
    rec("T02", "PASS" if ok else "FAIL", "式(1) kappa^2+tau^2 = omega^2/c^2 齐次性",
        "左端 %s，右端 %s ⇒ %s。" % (dstr(lhs1), dstr(rhs1), "齐次" if ok else "不齐次"))

    ok = dim_eq(DIM_TAU, DIM_KAPPA)
    rec("T03", "PASS" if ok else "FAIL", "式(2) tau = kappa*cot(theta) 齐次性",
        "theta 无量纲 ⇒ cot(theta) 无量纲 ⇒ 两端同为 %s ⇒ %s。"
        % (dstr(DIM_KAPPA), "齐次" if ok else "不齐次"))

    d_m_a = dmul(dmul(DIM_HBAR, dinv(DIM_C)), dim(0, -1, 0, 0))
    d_m_b = dmul(dmul(DIM_HBAR, DIM_OMEGA), dinv(dpow(DIM_C, 2)))
    ok = dim_eq(d_m_a, DIM_M) and dim_eq(d_m_b, DIM_M)
    rec("T04", "PASS" if ok else "FAIL", "式(3) 质量式两分支各自量纲 = M",
        "分支一（含 sin(theta) 版）%s，分支二（hbar*omega/(2 pi c^2)）%s ⇒ 皆为质量量纲 ⇒ %s。"
        "（分项齐次；两分支是否相容见 T05。）" % (dstr(d_m_a), dstr(d_m_b), "齐次" if ok else "不齐次"))

    omega = Dc("1.0e21")
    maxdev = Dc(0)
    for s_str in ["0.1", "0.3", "0.5", "0.9", "0.999", "1"]:
        s = Dc(s_str)
        cth = (Dc(1) - s * s).sqrt()
        kap = omega / C_SI * s
        tau = omega / C_SI * cth
        m_a = HBAR * s / (2 * PI * C_SI) * ((kap * kap + tau * tau).sqrt())
        m_b = HBAR * omega / (2 * PI * C_SI ** 2)
        r = m_a / m_b
        maxdev = max(maxdev, rel(r, s))
    guard("G-A1", maxdev < Dc("1e-40"), "式(3) 两分支之比数值上严格等于 sin(theta)")
    rec("T05", "FAIL", "【承重】式(1)(2)(3) 联立唯一解为 sin(theta)=1 ⇒ tau == 0",
        "由 (1)(2) 解出 kappa=(omega/c)sin(theta)、tau=(omega/c)cos(theta)，代入式(3) 分支一得 "
        "m_a = hbar*omega*sin(theta)/(2 pi c^2)，分支二给 m_b = hbar*omega/(2 pi c^2)。"
        "两分支相等要求 sin(theta)=1 ⇒ cos(theta)=0 ⇒ **tau 恒等于 0**。机器对拍：m_a/m_b 在 "
        "sin(theta)=0.1/0.3/0.5/0.9/0.999/1 六点上与 sin(theta) 的相对偏差最大 %s（机器零）⇒ "
        "比值恒等于 sin(theta)，唯一相容解 sin(theta)=1。推论：来料整套『挠率引力 / EC 挠率动力学』"
        "在其自身前置恒等式下退化为**零挠率**（即退化为黎曼 GR），与第五部分自评『兼容爱因斯坦-嘉唐』"
        "及末尾待攻坚『g-2 挠率修正』直接冲突。（与 r32 册 Z13『挠率归零退 GR』同型，但本册是"
        "**机器证明**而非两难登记。）" % E(maxdev))
    KEYNUM["T05_ratio_max_dev"] = E(maxdev)

    d_gth = dmul(dpow(DIM_C, 3), dinv(DIM_HBAR))
    gap = dsub(DIM_G_TRUE, d_gth)
    rec("T06", "FAIL", "式(4) G_th = 2 pi c^3/(hbar sin theta) 量纲非齐次（缺 L^2）",
        "表达式给出 %s，引力常数须为 %s ⇒ 缺口 %s = **一个长度平方 L^2**。"
        "这是本库『量纲非齐次』缺陷族**第 8 次复发**，且是整套方程组 c 幂次配错的第一处源头。"
        % (dstr(d_gth), dstr(DIM_G_TRUE), dstr(gap)))
    KEYNUM["G_th_dim"] = dstr(d_gth)
    KEYNUM["G_th_gap"] = dstr(gap)

    gth_min = 2 * PI * C_SI ** 3 / HBAR
    ratio = gth_min / G_SI
    rec("T07", "FAIL", "G_th 数值与 CODATA G 的差距（theta=pi/2 为全域最优情形）",
        "G_th = 2 pi c^3/(hbar sin theta) 在 |sin theta| <= 1 下**最小值** = %s m^3 kg^-1 s^-2"
        "（theta=pi/2）；CODATA G = %s ⇒ 比值 %s。且 sin theta 减小只会使 G_th **更大** ⇒ "
        "实数 theta 全域内 G_th 恒 >= 该值，**方向不可调**，不可能等于 G_exp。"
        % (E(gth_min), E(G_SI), E(ratio)))
    KEYNUM["G_th_min"] = E(gth_min)
    KEYNUM["G_th_over_G_exp"] = E(ratio)

    sin_req = HBAR * G_SI / (2 * PI * C_SI ** 3)
    cot_req = (Dc(1) - sin_req * sin_req).sqrt() / sin_req
    rec("T08", "FAIL", "弱场牛顿还原所需的螺旋升角（闭式反解）",
        "来料自述 ∇·g = 4 pi G_th sin^2(theta)*rho，要求 = 4 pi G_exp*rho ⇒ "
        "G_th sin^2(theta) = G_exp ⇒ sin(theta) = hbar*G_exp/(2 pi c^3) = %s ⇒ cot(theta) = %s。"
        % (E(sin_req), E(cot_req)))
    KEYNUM["sin_theta_newton"] = E(sin_req)
    KEYNUM["cot_theta_newton"] = E(cot_req)

    rec("T09", "FAIL", "【两难定理】牛顿还原与「弱场 tau << kappa」不可兼得",
        "由 (2) tau = kappa*cot(theta)，牛顿还原要求 cot(theta) = %s ⇒ tau/kappa = %s 远大于 1；"
        "而来料第二部分弱场极限自述『挠率很小 tau << kappa』。二者相差约 %s 个数量级 ⇒ 在来料自身"
        "口径下**互斥**。联合 T05（(1)(2)(3) 联立强制 sin(theta)=1，此时 G_th = %s 而非 G_exp）⇒ "
        "前置恒等式、挠率纲领、牛顿还原三者构成**三难**，至多取其二。"
        % (E(cot_req), E(cot_req), E(cot_req.ln() / Dc(10).ln()), E(gth_min)))

    ell = (HBAR * G_SI / (2 * PI * C_SI ** 3)).sqrt()
    gth_lp = 2 * PI * C_SI ** 3 * (LP * LP) / HBAR
    rec("T10", "CORRECTED", "式(4) 最小修复代价：须补一个长度标度 ell^2（新外部输入，不代选）",
        "补 ell^2 后 G_th = 2 pi c^3 ell^2/(hbar sin theta) 量纲齐次。取 sin(theta)=1 时 "
        "ell = sqrt(hbar*G_exp/(2 pi c^3)) = %s m = %s * l_P（l_P = %s m，恰为 l_P/sqrt(2 pi)）。"
        "若取最自然的 ell = l_P，则 G_th = %s = %s * G_exp（恰差 2pi = %s，相对偏差 %s）。"
        "⇒ 修复代价 = **新增 1 个未声明的长度标度**（撞 Ω5「自由常数 <= 1」，须显式登记为外部输入），"
        "且取普朗克标度时仍差 2 pi。本册不代选 ell。" %
        (E(ell), E(ell / LP), E(LP), E(gth_lp), E(gth_lp / G_SI), E(2 * PI), E(rel(gth_lp, G_SI))))
    KEYNUM["ell_required_m"] = E(ell)
    KEYNUM["ell_over_lP"] = E(ell / LP)
    KEYNUM["G_th_with_lP_over_G"] = E(gth_lp / G_SI)


# ======================= 4. 段 B：流形层耦合场方程 (5)(6)(7)(8)(9) =======================
def stage_B():
    d_coef = dmul(DIM_G_TRUE, dinv(dpow(DIM_C, 4)))
    d_rhs = dmul(d_coef, DIM_EDENS)
    ok = dim_eq(d_rhs, dim(0, -2, 0, 0))
    rec("T11", "PASS" if ok else "FAIL", "式(5) 耦合系数 8 pi G/c^4 方向正确（结构层）",
        "8 pi G/c^4 * T_μν 给出 %s = [R_μν] = L^-2 ⇒ %s。与库内 r18 记录的主线约定一致"
        "（区别于 B4 总账的 8 pi G/c^2 反向写法，属本库已登记的 A-07 型台账冲突的另一侧）。"
        "锚点复算 c^4/(8 pi G) = %s，与 r18/r19/r22/r27 逐位一致（第 4 次交叉印证）。"
        % (dstr(d_rhs), "结构正确" if ok else "结构错误", E(ANCHOR_C4_8PIG)))
    KEYNUM["anchor_c4_8piG"] = E(ANCHOR_C4_8PIG)

    rec("T12", "BOUNDARY", "式(5) 左侧嘉唐 Ricci（非对称）配对称 T_μν：约定依赖，不自推",
        "EC 理论中嘉唐 Ricci R_μν 一般非对称；爱因斯坦侧场方程通常写作「黎曼 Ricci + 挠率修正项」"
        "配含自旋的（可非对称）能动张量。来料直接用嘉唐 Ricci 配**对称** T_μν^spiral，存在"
        "「挠率被重复计入」与「对称性不匹配」两重约定风险。标 BOUNDARY，登记为实施前必须固定的约定之一。")

    n_dim = 4
    rank_eps = n_dim
    idx_torsion = 3
    free_after = rank_eps - idx_torsion
    rec("T13", "FAIL", "式(6) T = T^alpha_{mu nu}*epsilon_alpha^{mu nu} 在四维流形上未定义",
        "四维 Levi-Civita 张量秩 = %d；来料写 epsilon_alpha^{mu nu} 仅 **3 个指标** ⇒ 在 4 维流形上"
        "不是合法张量。轴挠率矢量标准定义应为 A^rho ∝ epsilon^{rho alpha beta gamma} T_{alpha beta gamma}"
        "（4 指标缩并 3 个 ⇒ 余 %d 个自由指标 ⇒ 结果是**矢量**，而非来料自称的『主标量迹』）。"
        "机器整数判据：rank(eps)=%d，挠率张量指标数=%d ⇒ 余自由指标 %d ≠ 0 ⇒ 非标量。"
        "⇒ 式(6) 既非法（指标数不足）又自相矛盾（自称标量，标准结果为矢量）。"
        % (rank_eps, free_after, rank_eps, idx_torsion, free_after))
    KEYNUM["levi_civita_rank"] = str(rank_eps)

    d_r = dsub(dpow(DIM_KAPPA, 2), dpow(DIM_TAU, 2))
    omega = Dc("1.0e21")
    maxdev = Dc(0)
    for s_str in ["0.1", "0.5", "0.9"]:
        s = Dc(s_str)
        cth = (Dc(1) - s * s).sqrt()
        kap = omega / C_SI * s
        tau = omega / C_SI * cth
        lhs = kap * kap - tau * tau
        rhs = -(omega * omega / (C_SI * C_SI)) * (cth * cth - s * s)
        maxdev = max(maxdev, rel(lhs, rhs))
    guard("G-B1", maxdev < Dc("1e-30"), "kappa^2-tau^2 = -(omega^2/c^2)cos(2θ) 数值对拍")
    rec("T14", "BOUNDARY", "式(7) R ∝ kappa^2 - tau^2：量纲齐次但范畴混用 + 符号未定",
        "量纲 %s = L^-2 与 Ricci 标量一致 ⇒ 齐次。但 (a) 左端是**流形曲率标量**、右端是"
        "**世界线 Frenet 不变量**，二者属不同数学范畴，来料未给函子/映射；(b) 比例系数未给；"
        "(c) 与 (1)(2) 联立后 R ∝ -(omega^2/c^2)cos(2θ)（对拍偏差 %s），符号随 theta 变而"
        "来料未声明符号约定 ⇒ 无判别力。标 BOUNDARY（不判对错）。" % (dstr(d_r), E(maxdev)))

    d_pref = dmul(DIM_HBAR, dinv(DIM_C))
    d_grad = dmul(d_pref, dmul(dmul(DIM_KAPPA, dinv(DIM_L)), dmul(DIM_KAPPA, dinv(DIM_L))))
    rec("T15", "FAIL", "式(8) 前因子 hbar/(2c) 使梯度项量纲退化为质量密度（缺 c^2）",
        "前因子 [hbar/c] = %s，[(∇kappa)^2] = %s ⇒ 梯度项 %s = **质量密度** M L^-3，"
        "而能动张量须为**能量密度** %s ⇒ 缺 c^2（最小修复：前因子改用 hbar*c）。"
        "与 r37 册 §20.2『3κs^2/32 缺口恰为 c^2』**同族同源**（本库该族第 8 次）。"
        % (dstr(d_pref), dstr(dmul(dinv(DIM_L), DIM_KAPPA)), dstr(d_grad), dstr(DIM_EDENS)))
    KEYNUM["T_spiral_gradient_dim"] = dstr(d_grad)

    d_bracket = dadd(dmul(dpow(DIM_C, 2), dpow(DIM_KAPPA, 2)), dpow(DIM_OMEGA, 2))
    d_V = dpow(d_bracket, 2)
    d_Vterm = dmul(d_pref, d_V)
    gapv = dsub(d_Vterm, d_grad)
    rec("T16", "FAIL", "式(8) 花括号内两项量纲互异 ⇒ T_μν^spiral 不可相加",
        "梯度项 %s，势能项 -V g_μν 给出 %s ⇒ 差 %s（恰为 c^4）⇒ **两项不可相加**。"
        "最小修复：V → V/c^4（或前因子改 hbar*c 并同步重标 V）。注意与 T15 是**两个独立**缺陷："
        "只修前因子不足以让势项齐次，两者必须同时修。" %
        (dstr(d_grad), dstr(d_Vterm), dstr(gapv)))
    KEYNUM["V_term_dim"] = dstr(d_Vterm)
    KEYNUM["V_vs_gradient_gap"] = dstr(gapv)

    mx = Dc(0)
    samples = []
    for k_str, t_str in [("1.0e-6", "3.0e-7"), ("1.0", "0.5"), ("1.0e12", "7.0e11")]:
        kap = Dc(k_str)
        tau = Dc(t_str)
        om = C_SI * ((kap * kap + tau * tau).sqrt())
        scale = (C_SI ** 2) * (kap * kap + tau * tau)
        brk = scale - om * om
        V = Dc("0.5") * brk ** 2
        dVk = 2 * (C_SI ** 2) * kap * brk
        dVt = 2 * (C_SI ** 2) * tau * brk
        # 相对判据（r32 册纪律：绝对残差在 1e40 量级失效，必须用相对机器零）
        rbrk = abs(brk) / scale
        rV = abs(V) / (Dc("0.5") * scale * scale)
        rdV = abs(dVk) / (2 * (C_SI ** 2) * abs(kap) * scale)
        mx = max(mx, rbrk, rV, rdV)
        samples.append("(κ=%s,τ=%s): |V|/特征=%s, |dV/dκ|/特征=%s"
                       % (k_str, t_str, E(rV), E(rdV)))
    guard("G-B2", mx < Dc("1e-50"),
          "ω 由 (1) 代数更新 ⇒ 约束残差、V、∂V/∂κ、∂V/∂τ 相对量 < 1e-50（相对机器零）")
    rec("T17", "FAIL", "【承重】式(9) 约束势 V 恒等于 0 ⇒ 「抑制约束漂移」是空承诺",
        "来料明写『ω 不独立演化，由代数约束 (1) 即时更新 ω = c*sqrt(kappa^2+tau^2)』，代入 (9) 得 "
        "V = 1/2*(c^2(kappa^2+tau^2) - ω^2)^2 ≡ 0。机器对拍三组取值（相对判据，分母取各特征量）："
        "%s ⇒ 相对残差 < 1e-50（**相对机器零**）。⇒ (a) 势导数项在 (10)(11) 中恒为零，"
        "演化退化为纯源驱动波动方程；"
        "(b) 第五部分自评『内置约束势抑制数值漂移』**不成立**——恒零的势不提供任何恢复力；"
        "(c) 约束 C_ω 亦恒为 0 ⇒ 第三部分『监控 |C_ω| 残差』永远读到 0，监控是假的。"
        "若要让 V 真正起作用，必须让 ω 成为**独立演化量**（+1 自由度 +1 方程，代价须登记）。"
        % "; ".join(samples))
    KEYNUM["V_identically_zero"] = "0 (machine exact, 3 sample points)"


# ======================= 5. 段 C：动力学演化与源项 (10)(11)(12) + 弱场极限 =======================
def stage_C():
    d_box_kappa = dmul(dim(0, -2, 0, 0), DIM_KAPPA)
    d_dVdk = dmul(dmul(dpow(DIM_C, 2), DIM_KAPPA),
                  dadd(dmul(dpow(DIM_C, 2), dpow(DIM_KAPPA, 2)), dpow(DIM_OMEGA, 2)))
    gap = dsub(d_dVdk, d_box_kappa)
    rec("T18", "FAIL", "式(10) 左端 □_Γ κ 与右端 ∂V/∂κ 量纲不齐（差 c^-4）",
        "左端 [□κ] = %s；右端 [∂V/∂κ] = %s ⇒ 差 %s ⇒ ∂V/∂κ 须除以 c^4 才齐次"
        "（与 T16 同源：V 的量纲本身错）。另注：来料已展开 ∂V/∂κ = 2c^2κ(c^2(κ^2+τ^2)-ω^2)，"
        "其括号项正是约束 (1) 的左端差 ⇒ 该项恒为零（见 T17），故本条除量纲外还有恒零问题。"
        % (dstr(d_box_kappa), dstr(d_dVdk), dstr(gap)))
    KEYNUM["box_kappa_dim"] = dstr(d_box_kappa)
    KEYNUM["dV_dkappa_dim"] = dstr(d_dVdk)

    d_S_wrong = dmul(dmul(dmul(dpow(DIM_C, 3), dinv(DIM_HBAR)), DIM_RHO), dinv(dpow(DIM_C, 2)))
    d_S_right = dmul(dmul(DIM_G_TRUE, DIM_RHO), dinv(dpow(DIM_C, 2)))
    rec("T19", "FAIL", "式(12) 源项 S_κ 与左端 □κ 差一个长度幂次（独立第二处量纲缺陷）",
        "按来料 (4) 的 G_th 量纲代入口径：[S_κ] = %s；即使换成量纲正确的 G 仍得 %s；"
        "而左端 [□κ] = %s ⇒ 两种口径下都**差一个长度幂次**。⇒ 这一处不能由『G_th 量纲错』"
        "解释，属**独立**缺陷：κ 作为 L^-1 的场，其源项须为 L^-3，而来料的构造只给到 L^-2（或 L^-4）。"
        % (dstr(d_S_wrong), dstr(d_S_right), dstr(d_box_kappa)))
    KEYNUM["S_kappa_dim_with_Gth"] = dstr(d_S_wrong)
    KEYNUM["S_kappa_dim_with_G"] = dstr(d_S_right)

    omega = Dc("1.0e21")
    mx1 = Dc(0)
    mx2 = Dc(0)
    for s_str in ["0.2", "0.5", "0.8"]:
        s = Dc(s_str)
        cth = (Dc(1) - s * s).sqrt()
        cot = cth / s
        kap = omega / C_SI * s
        tau = omega / C_SI * cth
        om = C_SI * ((kap * kap + tau * tau).sqrt())
        brk = (C_SI ** 2) * (kap * kap + tau * tau) - om * om
        dVk = 2 * (C_SI ** 2) * kap * brk
        dVt = 2 * (C_SI ** 2) * tau * brk
        # 用 tau/kappa（而非 cot=cos/sin）比较，避免 Decimal 除法-乘法往返舍入；
        # 并单独核验 tau/kappa == cot(theta) 本身。
        mx1 = max(mx1, rel(dVt, (tau / kap) * dVk), rel(tau / kap, cot))
        rho = Dc("1.0e3")
        Sk = 4 * PI * G_SI * s * rho / (C_SI ** 2)
        St = 4 * PI * G_SI * cth * rho / (C_SI ** 2)
        mx2 = max(mx2, rel(St, cot * Sk))
    guard("G-C1", mx1 < Dc("1e-40"),
          "∂V/∂τ = cotθ·∂V/∂κ 且 τ/κ = cotθ（相对机器零，非绝对零）")
    guard("G-C2", mx2 < Dc("1e-40"), "S_τ = cotθ·S_κ（sinθ/cosθ 之比恰为 cotθ）")
    rec("T20", "FAIL", "【承重】式(11) 恒等于 cot(theta) × 式(10) ⇒ τ 不是独立自由度",
        "因 θ 为常数、(2) 给 τ=κcotθ ⇒ □τ = cotθ·□κ；又 ∂V/∂τ = cotθ·∂V/∂κ（对拍相对差 %s），"
        "S_τ/S_κ = cosθ/sinθ = cotθ（对拍相对差 %s）⇒ 式(11) 两端**同时**是式(10) 的 cotθ 倍 ⇒ "
        "式(11) 不提供任何新信息，是**恒等冗余**。⇒ 第五部分自评『曲率 κ、挠率 τ 双动力学自由度』"
        "**不成立**：实际只有 1 个独立动力学自由度（τ 被 (2) 代数锁定）。"
        % (E(mx1), E(mx2)))
    KEYNUM["tau_redundancy_V_dev"] = E(mx1)
    KEYNUM["tau_redundancy_S_dev"] = E(mx2)

    d_kappa_sol = dmul(dmul(dmul(DIM_G_TRUE, DIM_RHO), dinv(dpow(DIM_C, 2))), dim(0, 2, 0, 0))
    rec("T21", "FAIL", "弱场泊松方程解出的 κ 量纲与符号表自报 [κ]=L^-1 冲突",
        "由 -∇^2κ = 4πGρ/c^2，解的量纲 = [Gρ/c^2]·L^2 = %s（**无量纲**）；而符号表自报 [κ] = %s。"
        "⇒ 若 κ 确为 L^-1 则源项须为 L^-3（既非来料的 L^-4 亦非修正后的 L^-2，见 T19）；"
        "若 κ 实为无量纲（牛顿势 Φ/c^2 的重标）则符号表错。**两口径必居其一，来料未声明**，"
        "而这直接决定 (10)(12) 的源项写法 ⇒ 属阻塞级未声明约定。" %
        (dstr(d_kappa_sol), dstr(DIM_KAPPA)))

    A = Dc("1")
    reads = []
    for r in [Dc("1"), Dc("2"), Dc("10")]:
        div_kappa_rhat = A / (r * r)
        lap_kappa = Dc(0)
        reads.append("r=%s: ∇·(κ r̂)=%s, ∇^2κ=%s" % (str(r), E(div_kappa_rhat), E(lap_kappa)))
    rec("T22", "FAIL", "弱场推导中 ∇·g = -c^2 ∇^2κ 是矢量恒等式错误",
        "来料取 g = -c^2 κ R̂（径向），则 ∇·g = -c^2 ∇·(κ R̂) = -c^2(∂_r κ + 2κ/r)，"
        "而 ∂_rκ + 2κ/r ≠ ∇^2κ = ∂_r^2κ + (2/r)∂_rκ。取球对称 κ = A/r 直接对拍：%s ⇒ "
        "二者**不相等**（来料该行自己也打了问号）。⇒ 弱场极限『自动还原牛顿引力高斯定理』"
        "整段推导不成立；结合 T08/T09 的闭式反解，牛顿还原在数值上亦不成立。"
        % "; ".join(reads))


# ======================= 6. 段 D：ADM-BSSN 3+1 分解 (13)-(18) 与约束集合 =======================
def stage_D():
    rec("T23", "PASS", "3+1 度规分解 ds^2 = -α^2dt^2 + γ_ij(dx^i+β^i dt)(dx^j+β^j dt)",
        "与标准 ADM 分解**逐字一致**（lapse α、shift β^i、三度规 γ_ij），符号与结构正确。")

    rec("T24", "PASS", "BSSN 变量定义 γ̃_ij = γ^(-1/3)γ_ij、Ã_ij、φ = (1/12)ln γ",
        "与标准 BSSN 定义一致（φ = (1/12)ln det γ，γ^{ij} = e^{-4φ}γ̃^{ij}）。结构层正确。")

    d_Pi = dmul(dinv(DIM_T), DIM_KAPPA)
    ok = dim_eq(d_Pi, dim(0, -1, -1, 0))
    rec("T25", "PASS" if ok else "FAIL", "式(13)(14) 共轭动量 Π = (1/α)(∂_t - β^k∂_k)φ",
        "[Π_κ] = %s；β^k∂_k 项量纲 T^-1 与 ∂_t 一致（α 无量纲）⇒ 齐次，为标准 3+1 一阶化形式。"
        % dstr(d_Pi))

    rec("T26", "PASS", "式(15)(16) ∂_t κ = β^k∂_kκ + αΠ_κ（τ 同式）",
        "与 (13)(14) 严格互逆，是标准一阶双曲化写法，形式正确。"
        "（形式正确 ≠ 可用：其配对的动量演化 (17)(18) 见 T27。）")

    d_dt_Pi = dim(0, -1, -2, 0)
    terms = [
        ("β^k∂_kΠ_κ", dmul(dim(0, 1, -1, 0), dim(0, -1, -1, 0))),
        ("α D̃^iD̃_iκ", dmul(dim(0, -2, 0, 0), DIM_KAPPA)),
        ("∂_kα D̃^kκ", dmul(dim(0, -1, 0, 0), dim(0, -1, 0, 0))),
        ("-α ∂V/∂κ", dmul(dmul(dpow(DIM_C, 2), DIM_KAPPA),
                          dadd(dmul(dpow(DIM_C, 2), dpow(DIM_KAPPA, 2)), dpow(DIM_OMEGA, 2)))),
        ("-α S_κ", dmul(dmul(dmul(dpow(DIM_C, 3), dinv(DIM_HBAR)), DIM_RHO), dinv(dpow(DIM_C, 2)))),
    ]
    distinct = set()
    lines = ["左端 [∂_tΠ_κ] = %s" % dstr(d_dt_Pi)]
    for name, d in terms:
        distinct.add(tuple(d))
        lines.append("%s = %s" % (name, dstr(d)))
    rec("T27", "FAIL", "【承重】式(17) 右端五项给出 %d 个互异量纲，且无一项与左端匹配" % len(distinct),
        " | ".join(lines) + " ⇒ 右端各项**彼此不可相加**（即使暂不追究与左端的失配）。"
        "这是本册最强读数：该式在当前写法下**不是合法方程**，RK4/FDTD 数值演化无从谈起。"
        "（τ 方程 (18) 因 T20 的 cotθ 冗余而同病。）")
    KEYNUM["T27_distinct_dims"] = str(len(distinct))

    rec("T28", "BOUNDARY", "式(17)(18) 缺 3+1 标量场演化的 αKΠ 耦合项（约定依赖，不自推系数）",
        "标准弯曲时空标量场 3+1 一阶形式中 Π 的演化含与外曲率迹 K 耦合的项（来自 lapse 与 √γ 的"
        "时间依赖）。来料 (17)(18) 无该项 ⇒ 在 K ≠ 0 的强场/宇宙学情形下与协变式 (10)(11) **不等价**。"
        "本册不自推其系数与符号，标 BOUNDARY，登记为实施前必须核对的第二个约定。")

    rec("T29", "BOUNDARY", "式(17)(18) 用共形导数 D̃^2 作用于标量，缺 e^{-4φ} 因子与联络差项",
        "物理拉普拉斯 γ^{ij}D_iD_jκ = e^{-4φ}γ̃^{ij}(∂_i∂_jκ - Γ^k_ij∂_kκ)，而 "
        "D̃^iD̃_iκ = γ̃^{ij}(∂_i∂_jκ - Γ̃^k_ij∂_kκ)；二者相差 e^{-4φ} 因子与 (Γ-Γ̃) 联络差项"
        "（后者 ∝ ∂φ）。来料直接写 α D̃^iD̃_iκ 而**未补任何共形因子** ⇒ 与其自称的 BSSN 共形分解"
        "不自洽。标 BOUNDARY（系数不自推）。")

    rec("T30", "MISMATCH", "约束 C_H 与标准 BSSN 逐字同（除 G→G_th）⇒ 「EC 版」名不副实",
        "C_H = R^(3) - A_ijA^ij + (2/3)K^2 - 16πG_thρ 的**结构**与标准 BSSN/ADM 哈密顿约束一致 ⇒ "
        "结构层 PASS。但 (a) 代入 G_th（量纲错，见 T06）⇒ 整体不齐次；(b) 来料自称『EC 版』，"
        "而爱因斯坦-嘉唐的哈密顿约束必须含**挠率贡献**（修正的 R^(3) 及自旋项），来料式内"
        "**无任何挠率项** ⇒ 与 GR 版本逐字相同 ⇒ 零挠率内容，与纲领自评矛盾。")

    rec("T31", "MISMATCH", "约束 C_M^i 同样为标准形式且无挠率/自旋流贡献",
        "D̃_j Ã^{ij} - (2/3)D̃^iK - 8πG_th j^i 结构与标准 BSSN 动量约束一致（右端系数 8π 正确），"
        "但同样 (a) G_th 量纲错；(b) 无挠率/自旋流项 ⇒ 与自评『EC 版，含挠率贡献』不符。")

    rec("T32", "FAIL", "约束 C_ω = ω^2 - c^2(κ^2+τ^2) 恒等于 0 ⇒ 约束监控无意义",
        "C_ω 的定义式正是 (1)，而 ω 被来料规定为『由 (1) 代数即时更新』 ⇒ C_ω ≡ 0 恒成立，"
        "与 T17（V ≡ 0）同源。⇒ 第三部分『数值仿真监控 |C_ω|,|C_H|,|C_M| 残差』中的 |C_ω| "
        "一项永远读到 0，不构成任何监控。")


# ======================= 7. 段 E：边界/初值/对照审计/自评 5 条 =======================
def stage_E():
    rec("T33", "PASS", "第四部分外边界 κ,τ,Π_κ,Π_τ → 0 的内部自洽性",
        "κ,τ → 0 ⇒ 由 (1) ω → 0 ⇒ 由 (3) m → 0 ⇒ 渐近平直；且 τ=κcotθ 与之一致；"
        "Π=0 与静态一致。该条在**约束面内自洽**（唯一一条无缺陷的边界设定）。")

    rec("T34", "FAIL", "初始静态数据 Π=0 与 (17) 联立 ⇒ 静态解不存在（在同式量纲失配之上）",
        "Π_κ(t=0)=0 且要求静态 ⇒ ∂_tΠ_κ=0 ⇒ 由 (17)：αD̃^2κ + ∂_kα D̃^kκ - α∂V/∂κ - αS_κ = 0。"
        "但由 T27 这四项量纲互异 ⇒ 该等式本身不成立 ⇒ 第四部分『泊松求解空间初始 κ(x),τ(x)』"
        "没有可用的静态方程可解（且 T21 已证泊松解出的 κ 量纲与符号表冲突）。"
        "⇒ 数值演化的**初始数据方案不可实施**。")

    rec("T35", "FAIL", "θ 为「几何常数」⇒ τ/κ 全域恒定 ⇒ 与 τ,κ 各自充当动力学场矛盾",
        "θ 常数 + (2) ⇒ τ(x,t)/κ(x,t) ≡ cotθ 在**全时空**恒定 ⇒ τ 的空间/时间剖面被 κ 完全决定，"
        "不存在独立的 τ 扰动模式。这与第五部分『双动力学自由度』及源项『物质同时激发曲率与挠率』"
        "的物理图像矛盾：S_τ 与 S_κ 只能按固定比例激发，任何违背该比例的源都会被 (2) 立即抹平"
        "（或使约束破坏）。⇒ 若要真正的双自由度，必须让 θ 成为**动力学场**（+1 自由度 +1 方程）。")

    rec("T36", "INFO", "第五部分对照 1（张祥前）：与库内既有审计口径一致",
        "来料称『张祥前体系只有一个无挠率辅助场、无波动传播、G 为外部输入、无 ADM 分解』。"
        "库内《统一场论核心公式_全目录总结与正确核固化》（2026-10-03）与《张祥前20核心公式元数据_"
        "结构层第一性审计》结论方向一致：正确核 22 条中无新增物理、G 为外部输入、无量纲靶场未给。"
        "本册仅登记一致性，不新增对张祥前体系的判定。")

    rec("T37", "PASS", "第五部分对照 2/3（牛顿静态泊松、GR 零挠率）：陈述正确",
        "牛顿引力为静态泊松方程无动力学传播、GR 为黎曼几何挠率恒为零 —— 两条均为教科书事实，"
        "陈述正确。")

    rec("T38", "FAIL", "【总结】第五部分 5 条自评 ✅ 逐条审计 ⇒ 0/5 成立",
        "①『完整一阶双曲 PDE 组适配 RK4/FDTD/ADM-BSSN』—— 一阶化形式 (15)(16) 正确，"
        "但 (17)(18) 四项互异量纲（T27）⇒ 不成立；②『κ、τ 双动力学自由度』—— "
        "(11) 恒等于 cotθ×(10)（T20）⇒ 实为单自由度，不成立；③『G_th 由 c,hbar,升角第一性导出』—— "
        "量纲缺 L^2（T06）且数值最小为 2.41e70 倍 G_exp（T07）⇒ 不成立；"
        "④『内置约束势抑制数值漂移』—— V ≡ 0（T17）⇒ 不成立；⑤『弱场极限回归牛顿引力』—— "
        "矢量恒等式错（T22）+ 需 sinθ≈4.16e-71 而与 τ≪κ 互斥（T09）⇒ 不成立。"
        "⇒ **5 条自评全部被本册机器否证**。")

    rec("T39", "FAIL", "约束/自由度计数：方程组形式上不闭合（可实施性判定）",
        "未知量：κ,τ（场）+ Π_κ,Π_τ + 度规 BSSN 变量；代数约束：(1)(2) 两条锁定 (ω,τ)；"
        "演化方程：(15)(16)(17)(18) 四条（其中 2 条冗余，见 T20）；椭圆约束：C_H、C_M^i。"
        "⇒ (a) 因 (1)(2) 是代数式而非 PDE，τ 与 ω 均非独立自由度，实际自由度 = 1（κ）；"
        "(b) (17)(18) 量纲失配 ⇒ 演化步不可写；(c) 初始静态方程不可用（T34）。"
        "⇒ 与 r21 册『可实施 ≠ 已过门禁』同构：本册结论更严——**当前写法连可实施都不成立**。")


# ======================= 8. 段 F：两条攻坚路（A/B）可行性预判 + 最小修复清单（不代选） =======================
def stage_F():
    rec("T40", "FAIL", "任务A（250 位高精度 G_th 原型 + χ² 对标 CODATA）当前**不可执行**",
        "χ² = Σ[(G_th - G_exp)/σ]^2 要求两量**同量纲同量纲单位**。而 G_th 的量纲为 %s（T06），"
        "G_exp 为 %s ⇒ 二者在量纲上不可比较 ⇒ 残差无定义、χ² 无定义。"
        "即便强行比数值：G_th 全域最小 %s 是 G_exp 的 %s 倍，且方向不可调 ⇒ "
        "χ² ~ 1e141 量级（无意义）。⇒ 任务 A 的**硬前置**是先修 (4)（见 T10），"
        "修完仍须新增 1 个长度标度并登记为外部输入。本册不代选是否修、选哪个 ℓ。"
        % (KEYNUM.get("G_th_dim"), dstr(DIM_G_TRUE), KEYNUM.get("G_th_min"),
           KEYNUM.get("G_th_over_G_exp")))

    rec("T41", "BOUNDARY", "任务B（g-2 挠率一阶修正）与库内已关窗口的关系（须先声明）",
        "库内既有读数：① TUFT 几何耦合下 a_TUFT = α/(8π) = 2.904e-4 vs a_e(exp) = 1.159652e-3，"
        "偏差 74.96%（r21/r27 册，g-2 窗口已关）；② EDM：d_e 预言超 ACME 2018 上限 1.28e16 倍"
        "（r19/r27 册）。⇒ 任务 B 若要推进，必须先声明它与这两条已关窗口的关系"
        "（是新机制还是同一机制的重算）。本册**不代选** A/B，仅登记该前置。"
        "另注：T05 已证来料前置恒等式强制 τ ≡ 0 ⇒ 在来料自身体系内，任何『挠率 τ 的一阶修正』"
        "**恒等于零** ⇒ 任务 B 在来料当前公设下无输出。")

    rec("T42", "INFO", "最小修复清单（次序不可换，本册不代选是否执行）",
        "M1 修 (4)：补长度标度 ℓ^2（ℓ = %s m 或取 ℓ_P 差 2π），登记为外部输入；"
        "M2 修 (3)：两个等号差 sinθ 因子，须选定其一（选定分支二则 (1)(2)(3) 联立仍强制 τ=0 ⇒ "
        "须同时放弃『θ 为常数』或放弃 (2)）；"
        "M3 修 (8)：前因子 ℏ/(2c) → ℏc 且 V → V/c^4（两处独立，须同时修）；"
        "M4 修 (9)/(10)/(11)：让 ω 独立演化（+1 自由度 +1 方程），否则 V 与 ∂V/∂κ 恒零；"
        "M5 修 (12)：源项须按 κ 的实际量纲（L^-1 ⇒ 源 L^-3）重标；"
        "M6 修 (17)(18)：补 c^2/c^4 因子、补 αKΠ 项、补 e^{-4φ} 共形因子、核对 D̃ 约定；"
        "M7 修 (6)：4 维轴挠率改用 ε^{ραβγ}T_{αβγ}（矢量而非标量）；"
        "M8 修约束集合：补 EC 挠率项，否则「EC 版」名不副实；"
        "M9 修第五部分弱场推导：∇·(κR̂) ≠ ∇^2κ。"
        "⇒ 全部修完后，体系是否仍自称『第一性导出 G』须重新评估（M1 引入了外部长度标度）。"
        % KEYNUM.get("ell_required_m"))

    rec("T43", "INFO", "来料相对库内既有册的定位（不重复造轮子）",
        "同一『光速螺旋 κ,τ,ω』母题在本库已有多册：r18（G 与 c 核心关系三表审计）、"
        "r19（EC 作用量与 ADM 约束审计）、r20（P0 同源化最小闭合集与代价）、"
        "r21（P1 门禁运行与 ADM 可实施性）、r26/r27（EC 合集与 GMUFT）、r32（V4.1 几何势）。"
        "本册新增**此前无人登记**的三条：(i) (1)(2)(3) 联立强制 τ ≡ 0 的**机器证明**（T05）；"
        "(ii) (11) ≡ cotθ×(10) 的**恒等冗余证明**（T20）；(iii) (17) 四项互异量纲（T27）。"
        "r21 册的结论『方程组与初值问题形式上可闭合』针对的是**另一份来料**（31 号册闭合底座），"
        "本册结论更严（连可实施都不成立），**不推翻 r21**，二者对象不同。")

    nsli("式(17)(18) 中 αKΠ 项的系数与符号（T28）：本册不自推。")
    nsli("式(17)(18) 中 D̃^2 作用于标量的共形修正项形式（T29）：本册不自推。")
    nsli("EC 版哈密顿/动量约束的挠率贡献项正确形式（T30/T31）：本册不自推。")
    nsli("式(4) 应补的长度标度 ℓ 取何值（T10/M1）：本册不代选。")


# ======================= 9. 汇总与产物写出 =======================
def main():
    guards_stage0()
    stage_A()
    stage_B()
    stage_C()
    stage_D()
    stage_E()
    stage_F()

    cnt = {}
    for rid, verdict, title, detail in RESULTS:
        cnt[verdict] = cnt.get(verdict, 0) + 1

    guard("G-Z1", len(RESULTS) == len(set(r[0] for r in RESULTS)), "条目编号无重复")
    guard("G-Z2", sum(cnt.values()) == len(RESULTS), "计数自洽")

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base, "数据")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    name = "TUFT-r39_V4-EC-ADMBSSN耦合场方程组_全维审计_2026-10-12"

    payload = {
        "round": "r39",
        "title": "TUFT-V4 完整耦合演化场方程组（EC + ADM-BSSN）全维审计",
        "date": "2026-10-12",
        "items": [{"id": r[0], "verdict": r[1], "title": r[2], "detail": r[3]} for r in RESULTS],
        "counts": cnt,
        "guards": [{"id": g[0], "ok": g[1], "note": g[2]} for g in GUARDS],
        "key_numbers": KEYNUM,
        "not_self_derived": NOT_SELF_DERIVED,
        "verdict_summary": {
            "承重裁定": ["T05 τ≡0 定理", "T17 V≡0 恒零", "T20 (11)≡cotθ·(10) 冗余",
                         "T27 (17) 四项互异量纲", "T38 自评 5 条全否", "T40 任务A 不可执行"],
            "PASS 面": ["T01 符号表", "T02/T03/T04 分项齐次", "T11 爱因斯坦系数方向",
                        "T23/T24/T25/T26 3+1 形式", "T33 边界自洽", "T37 牛顿/GR 对照陈述"],
            "状态": "来料当前写法下：非合法方程组（量纲失配）+ 挠率退化为零 + G 不可导出",
        },
    }
    with open(os.path.join(out_dir, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# %s" % payload["title"])
    lines.append("")
    lines.append("- 轮次：r39　日期：2026-10-12　条目：%d　自检：%d/%d"
                 % (len(RESULTS), sum(1 for g in GUARDS if g[1]), len(GUARDS)))
    lines.append("- 计数：" + " / ".join("%s=%d" % (k, cnt[k]) for k in sorted(cnt)))
    lines.append("")
    for rid, verdict, title, detail in RESULTS:
        lines.append("## %s [%s] %s" % (rid, verdict, title))
        lines.append("")
        lines.append(detail)
        lines.append("")
    lines.append("## 关键读数")
    lines.append("")
    for k in sorted(KEYNUM):
        lines.append("- %s = %s" % (k, KEYNUM[k]))
    lines.append("")
    lines.append("## 不自推登记")
    lines.append("")
    for s in NOT_SELF_DERIVED:
        lines.append("- %s" % s)
    with open(os.path.join(out_dir, name + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    rep = []
    rep.append("TUFT r39 全维审计 · 运行报告")
    rep.append("=" * 70)
    for rid, verdict, title, detail in RESULTS:
        rep.append("[%s] %s  %s" % (verdict, rid, title))
    rep.append("-" * 70)
    for g in GUARDS:
        rep.append("GUARD %s %s  %s" % ("OK " if g[1] else "BAD", g[0], g[2]))
    rep.append("-" * 70)
    for k in sorted(cnt):
        rep.append("%s = %d" % (k, cnt[k]))
    rep.append("GUARD = %d / %d" % (sum(1 for g in GUARDS if g[1]), len(GUARDS)))
    rep.append("TOTAL = %d" % len(RESULTS))
    with open(os.path.join(out_dir, name + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))

    print("\n".join(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())





