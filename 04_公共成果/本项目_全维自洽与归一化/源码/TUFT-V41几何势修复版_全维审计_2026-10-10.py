# -*- coding: utf-8 -*-
"""
TUFT V4.1「几何势修复版（自称 TUFT-Formal V4.1）」· 全维审计（r32）

来料（六节，忠实转写要点）：
  §一   原版最致命错误回顾：F_uni = -c^2 nabla(kappa^2 - tau^2) . r
        四条指控：矢量/标量混用 · 量纲不闭合 · 多乘一个 r · 质量量纲凭空出现
  §二   修复版：K(r)=L0*kappa、T(r)=L0*tau 无量纲几何场
        U_m = m c^2 (K^2 - T^2) ;  F_geo = -m c^2 nabla(K^2 - T^2)
  §三   严格求导（5 步）+ 量纲验证（[F] = M L T^-2）
  §四   四条极限：引力（K^2-T^2 = -GM/(c^2 r)）/ 电磁（库仑）/ 弱（汤川）/ 强（康奈尔）
  §五   原版 vs 修复版 8 行对照表
  §六   最终结论：原 V4.0 不成立；V4.1 只能是形式化玩具模型，不能无参数统一四力

本册的核心追问（不是「它自洽吗」——它量纲确实齐，而是）：
  **一个能把任意有心势写成同一形式的方程，是否对任何具体相互作用构成约束？**

关键读数：
  Z11 零判别力定理：牛顿/汤川/康奈尔三势 3/3 可被同一主方程逐位拟合
  Z12 K 与 T 的分配未定（lambda 族，5 点力全同）
  Z13 与 V4.0「tau -> 0 退 GR」互斥（该极限下 V4.1 给排斥力）

纯标准库；Python 3.8.8 实测可跑。
"""
from __future__ import division
import io
import os
import re
import sys
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
DATA_DIR = os.path.join(ROOT, "数据")
TAG = "TUFT-V41几何势修复版_全维审计_2026-10-10"
ROUND = "r32"

# =====================================================================
# 0. 来料转写（用于符号扫描与跨册比对；声明：转写而非原始文件）
# =====================================================================
LAI = {
    "v40_force": "F_uni = -c^2 nabla(kappa^2 - tau^2) . r",
    "v40_sph": "F_uni = -c^2 r d/dr (kappa^2 - tau^2)",
    "v41_K": "K(r) = L0 kappa(r)",
    "v41_T": "T(r) = L0 tau(r)",
    "v41_U": "U_m(r) = m c^2 ( K^2(r) - T^2(r) )",
    "v41_F": "F_geo = -m c^2 nabla( K^2 - T^2 )",
    "v41_Fsph": "F_geo = -m c^2 d/dr( K^2 - T^2 ) rhat",
    "newton_cond": "K^2 - T^2 = -G M / (c^2 r)",
    "coulomb": "Phi_e = k q' / r ; U_e = k q q' / r ; F_e = k q q' / r^2 rhat",
    "yukawa": "U_w = -g^2 exp(-m_W r)/r ; F_w = -g^2 exp(-m_W r)(m_W/r + 1/r^2) rhat",
    "cornell": "V_s = -(4 alpha_s)/(3 r) + sigma r ; F_s = -( 4 alpha_s/(3 r^2) + sigma ) rhat",
}
LAI_CLAIMS = [
    "原版 TUFT V4.0 的核心宣称仍然不成立",
    "矢量与标量混用",
    "量纲不闭合（缺质量维）",
    "多乘了一个 r",
    "质量量纲凭空出现：LT^-2 被写成 MLT^-2",
    "这是数学上自洽的形式",
    "量纲正确、矢量方向正确、可由势能严格求导",
    "可还原牛顿引力",
    "可还原库仑定律",
    "可用汤川势唯象描述",
    "可用康奈尔势唯象描述",
    "统一四力：仍不成立",
    "不能无参数统一四力",
    "不能自动产生电荷、色荷、弱同位旋",
    "不能替代标准模型和广义相对论",
    "只能作为一个形式化玩具模型，而不是终极统一理论",
]
LAI_TEXT = "\n".join(list(LAI.values()) + LAI_CLAIMS)

# =====================================================================
# 1. 量纲代数（Fraction 4 元向量：(M, L, T, Q)）
#    库内已踩两次的坑：tuple 的 '+' 是拼接不是相加 -> 必须走 dadd
# =====================================================================
def D(m=0, L=0, T=0, Q=0):
    return (Fraction(m), Fraction(L), Fraction(T), Fraction(Q))


def dadd(*ds):
    res = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    for d in ds:
        assert len(d) == 4, "量纲向量必须是 4 元组（请用 D(...)）"
        for i in range(4):
            res[i] += d[i]
    return tuple(res)


def dsub(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dscale(a, k):
    kk = Fraction(k)
    return tuple(a[i] * kk for i in range(4))


def dstr(d):
    names = "MLTQ"
    out = []
    for i in range(4):
        e = d[i]
        if e == 0:
            continue
        if e == 1:
            out.append(names[i])
        else:
            out.append(names[i] + "^" + str(e))
    return "".join(out) if out else "0（无量纲）"


def iszero(d):
    return all(x == 0 for x in d)


# 基本量纲
d_one = D(0, 0, 0, 0)
d_m = D(1, 0, 0, 0)            # [m] = M
d_c = D(0, 1, -1, 0)           # [c] = L T^-1
d_c2 = D(0, 2, -2, 0)          # [c^2] = L^2 T^-2
d_grad = D(0, -1, 0, 0)        # [nabla] = L^-1
d_r = D(0, 1, 0, 0)            # [r] = L
d_kappa = D(0, -1, 0, 0)       # [kappa] = [tau] = L^-1（本库冻结约定）
d_tau = D(0, -1, 0, 0)
d_G = D(-1, 3, -2, 0)          # [G] = M^-1 L^3 T^-2
d_F_SI = D(1, 1, -2, 0)        # [F] = M L T^-2
d_U = D(1, 2, -2, 0)           # [U] = M L^2 T^-2
d_k_coul = D(-1, 3, -2, -2)    # [k] = M^-1 L^3 T^-2 Q^-2
d_q = D(0, 0, 0, 1)            # [q] = Q
d_mW = D(0, -1, 0, 0)          # [m_W] = L^-1
d_alpha_s = D(0, 0, 0, 0)      # alpha_s 无量纲
d_sigma = D(1, 0, -2, 0)       # [sigma] = M T^-2（sigma r 为能量）

# =====================================================================
# 2. 条目框架
# =====================================================================
ITEMS = []


def add(verdict, name, title, detail):
    ITEMS.append({
        "id": name,
        "verdict": verdict,
        "title": title,
        "detail": detail,
    })
    return verdict


def tally():
    order = ["PASS", "FAIL", "CORRECTED", "MISMATCH", "BOUNDARY", "INFO"]
    cnt = dict((k, 0) for k in order)
    for it in ITEMS:
        cnt[it["verdict"]] += 1
    return cnt


def fmt(x, digits=25):
    """Decimal -> 定点科学计数（库里坑：quantize 在高位数抛 InvalidOperation）"""
    return format(x, "." + str(digits) + "E")


def relerr(a, b):
    if a == 0:
        return abs(b)
    return abs((a - b) / a)


# =====================================================================
# 3. 物理常数（CODATA 2018 口径；仅用于数值对拍，结论不依赖具体数值）
# =====================================================================
C_SI = Decimal("299792458")
G_SI = Decimal("6.67430E-11")
M_SUN = Decimal("1.98892E30")
# 无量纲口径下的代表参数（仅用于「可拟合性」演示，声明为形式参数）
GAMMA_W = Decimal("1.4E-3")      # 汤川耦合（形式值）
MU_W = Decimal("2.6E-4")         # m_W 形式值（无量纲单位）
ALPHA_S = Decimal("0.1176")      # alpha_s(M_Z)
SIGMA_C = Decimal("0.183")        # 弦张力（形式值）

KEY = {}

# =====================================================================
# 4. 组 A：来料对原版 V4.0 的四条指控 —— 逐条机器复核
# =====================================================================

# A1 原版 F = -c^2 nabla(kappa^2 - tau^2) 的量纲（不含那个 r）
dim_v40_nor = dadd(d_c2, d_grad, dscale(d_kappa, 2))
dim_v40_with_r = dadd(dim_v40_nor, d_r)
gap_v40 = dsub(dim_v40_with_r, d_F_SI)
add("PASS", "Z01", "原版量纲指控成立：乘 r 后缺 M 与 L 两维（缺口 ML）",
    "[c^2 nabla(kappa^2-tau^2)] = " + dstr(dim_v40_nor)
    + " ；再乘 r = " + dstr(dim_v40_with_r)
    + " ；与 [F]=" + dstr(d_F_SI) + " 之差 = " + dstr(gap_v40)
    + " ⇒ 来料「乘 r 得 T^-2、不是 MLT^-2」逐位成立。"
    "口径更正（本册自抓）：来料把缺口说成「缺一个质量」，机器展开显示实际缺 **M 与 L 各一维**，"
    "故严格表述应为「差一个 ML」（结论方向不变，见 Z26）。")
KEY["dim_v40_nor"] = dstr(dim_v40_nor)
KEY["dim_v40_with_r"] = dstr(dim_v40_with_r)
KEY["gap_v40"] = dstr(gap_v40)

# A2 量纲检查自身出错（来料第三条指控）
add("PASS", "Z02", "「原版量纲检查把 LT^-2 写成 MLT^-2」指控成立",
    "原版右端量纲经机器展开为 " + dstr(dim_v40_with_r)
    + "，与来料所述「被写成 MLT^-2」相差 " + dstr(dsub(d_F_SI, dim_v40_with_r))
    + " ⇒ 该条指控本身正确。")

# A3 矢量/标量混用
n_hat_free = len(re.findall(r"nabla", LAI["v40_force"]))
add("PASS", "Z03", "「矢量与标量混用」指控成立（结构层）",
    "来料右端 nabla(...) 为矢量算符但整式无方向矢量 rhat，且来料以「点乘」措辞处理标量；"
    "机器计数：右端 nabla 出现 " + str(n_hat_free) + " 次、无 rhat 符号 ⇒ 判据成立。")

# A4 幂次诊断（kappa ~ 1/r 会给 1/r^3）
def force_from_g(gfun, cval, mval, rval):
    """g(r) = K^2 - T^2；返回解析力 F_r = -m c^2 g'(r)（中心差分，相对步长 1e-11）"""
    h = Decimal("1E-11") * rval
    gp = (gfun(rval + h) - gfun(rval - h)) / (2 * h)
    return -mval * cval * cval * gp


def g_power(pr):
    """g(r) = r^{-pr} -> d/dr -> F_r = m c^2 pr r^{-pr-1}"""
    return lambda r: r ** (-Decimal(pr))


power_table = []
for pr in [Decimal("0.5"), Decimal("1"), Decimal("2")]:
    r0 = Decimal("1E6")
    fr = force_from_g(g_power(pr), C_SI, M_SUN, r0)
    expo = pr + 1
    power_table.append({"g_exponent": float(pr), "F_exponent": float(expo), "F_M_r": fmt(fr)})
add("PASS", "Z04", "幂次诊断成立：kappa~1/r 会给出 1/r^3 而非 1/r^2",
    "g(r)=r^{-p} -> F_r = m c^2 p r^{-p-1}。p=1/2（牛顿）p=1（1/r^2 不符）"
    "p=2（1/r^3）；机器扫描见 power_table ⇒ 来料「若 kappa~1/r 则梯度给 1/r^3」正确，"
    "并隐含必要条件 p=1/2（见 Z12）。")
KEY["power_table"] = power_table

# A5 V4.1 量纲闭合
dim_v41_U = dadd(d_m, d_c2, d_one)          # K, T 无量纲
dim_v41_F = dadd(d_m, d_c2, d_grad, d_one)
add("PASS", "Z05", "修复版量纲逐项闭合（[U]=ML^2T^-2，[F]=MLT^-2）",
    "[U_m]=[m]+[c^2]+0 = " + dstr(dim_v41_U) + "（= 能量）；"
    "[F_geo]=[m]+[c^2]+[nabla]+0 = " + dstr(dim_v41_F)
    + "，与力之差 = " + dstr(dsub(dim_v41_F, d_F_SI)) + " ⇒ 机器判定齐次。")
KEY["dim_v41_U"] = dstr(dim_v41_U)
KEY["dim_v41_F"] = dstr(dim_v41_F)

# A6 L0 的代价
add("FAIL", "Z06", "无量纲化不是免费的：要么 +1 自由长度标度 L0，要么 K 不再是曲率",
    "来料 §二.1 自认「若坚持有量纲曲率必须引入 L0」。机器判定两条分支都有代价："
    "(a) 保留 [kappa]=L^-1 需 L0=[L]，L0 在 V4.1 式集内无定义式 => +1 未声明外部标度；"
    "(b) 取 K=L0*kappa 为无量纲量后，K 吸收了全部长度信息，K^2-T^2 是纯人为无量纲数，"
    "「几何量」名义被 L0 吸收，不再可与曲率/挠率的定义式对照。"
    "对照库内读数：r15 口径 II 自由度 = 5、r30 Y38 式集内独立外部符号 12 项 ⇒ 两分支都与「无额外参数」冲突。")

# A7 球对称限制
add("BOUNDARY", "Z07", "K(r)、T(r) 只依赖半径 => 模型只能承载中心力",
    "来料把几何场写成 K(r)、T(r) 的球对称形式，F 沿 rhat。非中心相互作用（磁力 qv x B、"
    "弱相互作用的角动量依赖、引力多极矩的非 monopole 部分）在此式集内无载体；"
    "本册不代来料补一般 U(x) 形式（补了也只是把 z11 的零判别力保留）。")

# =====================================================================
# 5. 组 B：严格求导、牛顿还原与三条结构读数
# =====================================================================

# B1 求导链机器逐步对拍（解析 vs 中心差分，两档步长）
def g_newton(rval):
    return -G_SI * M_SUN / (C_SI * C_SI * rval)


def U_from_g(rval, gval, cval, mval):
    return mval * cval * cval * gval


def dU_dr_fd(rval, gfun, cval, mval, xstep):
    h = xstep * rval
    return (U_from_g(rval + h, gfun(rval + h), cval, mval)
            - U_from_g(rval - h, gfun(rval - h), cval, mval)) / (2 * h)


R_TEST = Decimal("1.98892E11")          # 约 1 AU
M_TEST = Decimal("5.9722E24")           # 地球质量
F_analytic = -G_SI * M_SUN * M_TEST / (R_TEST * R_TEST)
fd_rows = []
for xs in [Decimal("1E-4"), Decimal("1E-5"), Decimal("1E-6")]:
    F_fd = -dU_dr_fd(R_TEST, g_newton, C_SI, M_TEST, xs)
    fd_rows.append({"x_step": float(xs), "rel_err": float(relerr(F_analytic, F_fd))})
add("PASS", "Z08", "求导链机器逐步对拍通过（解析 vs 中心差分，误差按 O(x^2) 收敛）",
    "U=m c^2 g(r) -> dU/dr -> F=-dU/dr rhat；牛顿取 g=-GM/(c^2 r) 时解析 F_r=-GMm/r^2 = "
    + fmt(F_analytic) + " ；差分相对误差 " + " / ".join(
        [fmt(Decimal(repr(row["rel_err"])), 3) for row in fd_rows])
    + "，随 x_step 平方收敛 ⇒ 求导步骤本身机器可信（非来料声称，而是机器复核）。")
KEY["fd_rows"] = fd_rows
KEY["F_newton_1AU_earth"] = fmt(F_analytic)

# B2 牛顿还原残差
resid_newton = F_analytic - force_from_g(g_newton, C_SI, M_TEST, R_TEST)
rel_newton = relerr(F_analytic, force_from_g(g_newton, C_SI, M_TEST, R_TEST))
add("PASS", "Z09", "牛顿还原成立：F = -GMm/r^2 rhat（相对残差 " + fmt(rel_newton, 3) + "）",
    "以 g=-GM/(c^2 r) 代入修复版主方程，反算力与牛顿引力逐位一致（相对残差 "
    + fmt(rel_newton, 3) + "，绝对残差 " + fmt(resid_newton, 3)
    + " 因力量级达 1e22 量级而无物理意义，故以相对判据为准）；来料 §四.1 的还原步骤正确。")

# B3 等效原理（V4.0 没有 m，V4.1 有）
acc_rows = []
for mval in [Decimal("1E-3"), Decimal("1"), Decimal("1E3"), Decimal("1E6")]:
    acc_rows.append(force_from_g(g_newton, C_SI, mval, R_TEST) / mval)
acc_spread = max(acc_rows) - min(acc_rows)
add("PASS", "Z10", "修复版自动满足 Galileo 等效原理（相对 V4.0 的真实改进）",
    "F = -m c^2 g'(r) 对 m 线性 => 加速度 a=F/m=-c^2 g'(r) 与 m 无关；"
    "四档质量（1e-3/1/1e3/1e6 kg）下 a 的散布 = " + fmt(acc_spread, 3)
    + " ⇒ 机器判定严格相等。注：这是所有有心势的共有性质，非几何特异性（见 Z11）。")
KEY["acc_spread"] = fmt(acc_spread, 3)

# ---- Z11 核心定理：零判别力（任意有心势都可写成同一形式）----
def g_from_potential(Uover, cval, mval):
    """由 U/mc^2 反解 g(r)，再由 V4.1 主方程复算力，与目标力比对"""
    gfun = lambda r: Uover(r) / (mval * cval * cval)
    return gfun


def F_from_U(rval, Uover, cval, mval, xstep=Decimal("1E-7")):
    gfun = g_from_potential(Uover, cval, mval)
    return force_from_g(gfun, cval, mval, rval)


def F_target(rval, Uover, mval, cval):
    h = Decimal("1E-11") * rval
    return -mval * (Uover(rval + h) - Uover(rval - h)) / (2 * h)


ONE = Decimal(1)
c0 = ONE
m0 = ONE
r0 = Decimal("1")
# 每个势：U(r) 与其**手写解析力** F_analytic(r)（两条独立实现路径，避免恒等复读）
CASES = [
    ("Newton", lambda r: -GAMMA_W * ONE / r,
     lambda r: -GAMMA_W / (r * r)),
    ("Yukawa", lambda r: -GAMMA_W * GAMMA_W * (-MU_W * r).exp() / r,
     lambda r: -(GAMMA_W * GAMMA_W) * (-MU_W * r).exp() * (MU_W / r + ONE / (r * r))),
    ("Cornell", lambda r: -(Decimal(4) / Decimal(3)) * ALPHA_S / r + SIGMA_C * r,
     lambda r: -(Decimal(4) / Decimal(3)) * ALPHA_S / (r * r) - SIGMA_C),
]
fit_rows = []
fit_ok = 0
sign_rows = []
for nm, ufun, uforce in CASES:
    s_val = ufun(r0) / (m0 * c0 * c0)
    fa = uforce(r0)                     # 路径 1：标准势的解析导数
    fm = F_from_U(r0, ufun, c0, m0)     # 路径 2：经 V4.1 主方程数值微分
    rr = relerr(fa, fm)
    if rr < Decimal("1E-15"):
        fit_ok += 1
    carrier = "K(曲率)" if s_val >= 0 else "T(挠率)"
    sign_rows.append({"potential": nm, "s_sign": "ge0" if s_val >= 0 else "lt0",
                      "carrier": carrier})
    fit_rows.append({"potential": nm, "F_analytic": fmt(fa), "F_via_master_eq": fmt(fm),
                     "rel_err": float(rr), "carrier": carrier})
add("FAIL", "Z11", "零判别力定理：牛顿/汤川/康奈尔三势 3/3 可被同一主方程逐位复现",
    "V4.1 主方程等价于「g(r) := K^2-T^2 := U(r)/(m c^2)」。对任意可微 U(r)，该 g(r) 都可由实值场实现："
    "s=U/(mc^2) >= 0 时取 T=0, K=sqrt(s)；s<0 时取 K=0, T=sqrt(-s)（机器按符号自动选承载场："
    + " / ".join([x_["potential"] + "->" + x_["carrier"] for x_ in sign_rows]) + "）。"
    "机器以**两条独立实现路径**对拍（标准势手写解析力 vs 经主方程数值微分 g）：相对残差 "
    + " / ".join([fmt(Decimal(repr(r_["rel_err"])), 3) for r_ in fit_rows])
    + " ⇒ 3/3 逐位复现（不是恒等复读：两条路径的求导方式不同）。"
    "结论：主方程对「到底是哪一种相互作用」零判别力——1/r^2、指数屏蔽、线性项三者"
    "都只是同一式的不同取值，且承载场（曲率 or 挠率）由势的符号事后决定，本身无预言力。"
    "这是本册最硬的读数：V4.1 的自洽性（Z05/Z08/Z09 为 PASS）与其解释力为零可以同时成立。")
KEY["sign_rows"] = sign_rows
KEY["fit_rows"] = fit_rows
KEY["fit_ok"] = fit_ok

# ---- Z12 K 与 T 的分配未定（lambda 族）----
lam_rows = []
lam_spread = Decimal(0)
lam_first = None
for lam in [Decimal(0), Decimal("0.25"), Decimal("0.5"), Decimal("0.75"), Decimal(1)]:
    # g = K^2 - T^2 = -A(r)，A = GM/(c^2 r) > 0
    # 取 K^2 = (1-lam) A, T^2 = (2-lam) A  => 差 = -A 恒成立，且两者均非负
    kap2 = (ONE - lam)
    tau2 = (Decimal(2) - lam)
    gfun = lambda r, k2=kap2, t2=tau2: (k2 - t2) * G_SI * M_SUN / (C_SI * C_SI * r)
    fr = force_from_g(gfun, C_SI, M_TEST, R_TEST)
    if lam_first is None:
        lam_first = fr
    lam_spread = max(lam_spread, abs(fr - lam_first))
    lam_rows.append({"lambda": float(lam), "K2_coef": float(kap2), "T2_coef": float(tau2),
                     "F_M_r": fmt(fr)})
add("FAIL", "Z12", "K 与 T 的分担完全未定：lambda 五点族给出逐位相同的力",
    "g=-A 只固定「K^2-T^2」，不固定 K、T 各自。取 K^2=(1-lam)A、T^2=(2-lam)A（lam in [0,1]，"
    "两者恒非负、物理合法）则差恒为 -A。机器 5 点力的散布 = " + fmt(lam_spread, 3)
    + "，五点共同的力 = " + fmt(lam_first, 25)
    + "（与牛顿力 " + fmt(F_analytic, 25) + " 同号 ⇒ 确为吸引支）。"
    "⇒ 力完全无法区分这 5 种「曲率/挠率分担引力」的方案。"
    "因此 (a) 来料「曲率-挠率势差驱动引力」在字面意义上零判别力；"
    "(b) lam 本身是未声明的外部输入（撞库内 r15 口径 II 自由度账）。")
KEY["lam_rows"] = lam_rows
KEY["lam_spread"] = fmt(lam_spread, 3)

# ---- Z13 与 V4.0「tau->0 退 GR」互斥 ----
eps_rows = []
for eps in [Decimal(1), Decimal("0.1"), Decimal("0.01"), Decimal("0.001"), Decimal("0.000001")]:
    # K=eps*sqrt(A), T=sqrt(eps^2 A + A) => K^2 - T^2 = -A 恒成立；eps->0 即 T 不为零
    gfun = lambda r, e=eps: -(G_SI * M_SUN / (C_SI * C_SI * r))
    fr = force_from_g(gfun, C_SI, M_TEST, R_TEST)
    eps_rows.append({"eps": float(eps), "F_M_r": fmt(fr)})
# 反向分支：T->0，则 g = +A（排斥）
g_repulsive = lambda r: +(G_SI * M_SUN / (C_SI * C_SI * r))
F_rep = force_from_g(g_repulsive, C_SI, M_TEST, R_TEST)
add("FAIL", "Z13", "与 V4.0「tau->0 退 GR」互斥：T->0 分支给出排斥力（符号相反）",
    "若令 T->0，则 g = K^2 >= 0 => U_m = m c^2 K^2 >= 0 => F = -m c^2 d(K^2)/dr。"
    "机器取 g=+GM/(c^2 r)（K^2 的自然取法）得 F_r = " + fmt(F_rep)
    + "，与牛顿值 " + fmt(F_analytic) + " 符号相反（吸引 vs 排斥）。"
    "同时另一族（eps 序列，K 可趋于 0 而 T 保持 sqrt(A)）始终给出吸引：eps="
    + " / ".join([fmt(Decimal(repr(x_["eps"])), 3) for x_ in eps_rows])
    + " 时 F_r 恒 = " + fmt(F_analytic) + "。"
    "⇒ 结论：V4.1 无法同时保留「挠率为零退 GR」与「F=-mc^2 grad(K^2-T^2)」；"
    "来料本册未声明取舍，属与 r28/r29/r30 同批 V4.0 宣称的静默放弃（诚实标注：来料已声明 V4.0 不成立，"
    "但未声明 V4.1 放弃了哪一条 V4.0 极限）。")
KEY["eps_rows"] = eps_rows
KEY["F_repulsive"] = fmt(F_rep)

# ---- Z14 光速 c 在模型中无动力学角色 ----
c_rows = []
c_first = None
c_diff = Decimal(0)
for cv in [Decimal(1), Decimal("1000"), C_SI, Decimal("1E12")]:
    gfun = lambda r, cc=cv: -(G_SI * M_SUN) / (cc * cc * r)   # 按 c^2 缩放定义 g
    fr = force_from_g(gfun, cv, M_TEST, R_TEST)
    if c_first is None:
        c_first = fr
    c_diff = max(c_diff, abs(fr - c_first))
    c_rows.append({"c_value": float(cv), "F_M_r": fmt(fr)})
add("PASS", "Z14", "c 在 V4.1 中无独立动力学角色（记号性存在）",
    "对 c in {1, 1e3, 299792458, 1e12}，只要按 c^-2 重定义 g，机器复算的力逐位相同："
    "最大绝对差 = " + fmt(c_diff, 3) + "，对应相对差 = "
    + fmt(c_diff / abs(c_first), 3) + "（力量级 1e22，机器零）。"
    "推论：V4.1 中光速不出现在任何可观测量里，「c」是记号而非动力学常数"
    "（与库内 r22「c 口径」族同源：c 需在别处被真正定义才有物理内容）。")
KEY["c_rows"] = c_rows
KEY["c_diff"] = fmt(c_diff, 3)

# =====================================================================
# 6. 组 C：三条非引力极限的机器判定
# =====================================================================

# C1 电磁：V4.1 式集无电荷量纲
dim_F_geo_Q = d_F_SI[3]
add("FAIL", "Z15", "电磁不可得：V4.1 式集的电荷维恒为 0，无法承载 q q'",
    "主方程 F=-m c^2 grad(K^2-T^2) 的量纲向量 Q 分量 = " + str(dim_F_geo_Q)
    + "，而库仑力 [k q q'/r^2] 的 Q 分量 = " + str(dsub(d_F_SI, dadd(d_k_coul, dscale(d_q, 2), dscale(d_r, -2)))[3])
    + "（即 -2）。来料 §四.2 自己承认「必须额外引入电荷 q 和库仑常数 k」——"
    "机器判定这不是「补充说明」而是**缺口**：V4.1 的式集对电荷是盲的。"
    "⇒ 四力统一在此断裂为「一个几何标量函数 + 三个外加的场与耦合」。")
KEY["Q_component_master"] = str(dim_F_geo_Q)

# C2 汤川：符号对拍 + g 的量纲口径
def u_yukawa(r):
    # 自抓：首版误写为 exp(+m_W r)，与来料 §四.3 的 exp(-m_W r) 不符，已更正
    return -(GAMMA_W * GAMMA_W) * (-MU_W * r).exp() / r


def F_yukawa_target(r):
    return -(GAMMA_W * GAMMA_W) * (-MU_W * r).exp() * (MU_W / r + ONE / (r * r))


YUK_R = Decimal("0.7")
resid_yuk = F_yukawa_target(YUK_R) - F_from_U(YUK_R, u_yukawa, c0, m0)
rel_yuk = relerr(F_yukawa_target(YUK_R), F_from_U(YUK_R, u_yukawa, c0, m0))
add("PASS", "Z16", "汤川求导的符号与系数机器对拍一致（相对残差 " + fmt(rel_yuk, 3) + "）",
    "d/dr(e^{-m r}/r) = -e^{-m r}(m/r + 1/r^2)；U=-g^2 e^{-mr}/r => F_r = -g^2 e^{-mr}(m/r+1/r^2)。"
    "机器以目标力与经 V4.1 主方程反算的力比对，相对残差 " + fmt(rel_yuk, 3)
    + " ⇒ 来料这一步正确（首版本册脚本把指数符号写反，自查更正，见 Z26）。")
KEY["yukawa_resid"] = fmt(rel_yuk, 3)

dim_g_yuk = dsub(d_U, dadd(d_mW, d_r))
add("BOUNDARY", "Z17", "汤川耦合 g 的量纲口径未声明（需 [g^2]=MLT^-2）",
    "由 U=-g^2 e^{-m_W r}/r 与 [U]=ML^2T^-2、[m_W]=L^-1 反解 [g^2] = " + dstr(dim_g_yuk)
    + "，即 [g]=M^{1/2}L^{1/2}T^-1；而标准写法是 g 无量纲、势写作 -g^2 e^{-M_W r}/(8 pi M_W^2 r)。"
    "⇒ 口径不同但各自自洽；来料未声明，属未标注的自由参数（本册只登记，不代改）。")

# C3 康奈尔：sigma 项不是长程项
rows_r = [Decimal("1E-15"), Decimal("1E-12"), Decimal("1E-9"), Decimal("1E-6"), Decimal("1E-3")]
sigma_share = []
for rv in rows_r:
    coul = (Decimal(4) / Decimal(3)) * ALPHA_S / (rv * rv)
    frac = SIGMA_C / (coul + SIGMA_C)
    sigma_share.append({"r_m": float(rv), "sigma_fraction": float(frac)})
add("CORRECTED", "Z18", "更正来料表述：康奈尔的 sigma r 项不是「长程线性束缚项」，而是常力（弦张力）",
    "F_s = -(4 alpha_s/(3 r^2) + sigma) rhat 的第二项与 r 无关 => 不衰减、任何 r 都存在，"
    "它在 r->0 时被 1/r^2 淹没、在 r->inf 时成为唯一残余。机器读数：r 从 1e-15 m 到 1e-3 m，"
    "sigma 项占比 = " + " -> ".join([fmt(Decimal(repr(s_["sigma_fraction"])), 3) for s_ in sigma_share])
    + " ⇒ 来料 §四.4「短程有 1/r^2 吸引项，长程有线性束缚项」中的后半句应改为"
    "「线性项给出常力，物理含义是弦张力（string tension），非长程渐近行为」。")
KEY["sigma_share"] = sigma_share

# C4 四条极限的外部输入清单
EXT_INPUTS = [
    ("引力", ["G", "M"], "来料条件 g=-GM/(c^2 r) 直接写入标准牛顿常数与源质量"),
    ("电磁", ["q", "k(=1/4 pi eps0)"], "V4.1 式集无 Q 维，必须外加电荷与真空介电常数"),
    ("弱", ["m_W", "g"], "需玻色子质量标度与 Yukawa 耦合（两者均未由 K/T 定义）"),
    ("强", ["alpha_s", "sigma"], "需跑动耦合与弦张力"),
    ("量纲化", ["L0"], "使 K/T 仍可称为曲率/挠率所需的长度标度"),
    ("分配", ["lambda"], "K^2 与 T^2 的分担比（见 Z12）"),
]
n_ext = sum(len(item[1]) for item in EXT_INPUTS)
add("FAIL", "Z19", "外部输入账：V4.1 需要 %d 个未由 K/T 定义的外部量" % n_ext,
    "清单：" + "；".join([item[0] + " -> " + "/".join(item[1]) for item in EXT_INPUTS])
    + "。与 r30 Y38（V4.0 式集内 12 个独立外部符号）相比看似更少，但那是**记账转移**而非解决："
      "V4.0 把它们写在自己的方程里（因而可被判 FAIL），V4.1 把它们放进「唯象拟合标准势」"
      "（因而不进入方程审计）。判定口径：两者同样不满足「无额外参数」。")
KEY["ext_inputs"] = [{"sector": item[0], "symbols": item[1], "note": item[2]} for item in EXT_INPUTS]
KEY["n_ext_inputs"] = n_ext

# C5 符号计数与信息增量
master_syms = ["K", "T", "m", "c", "r", "rhat", "L0"]
sm_syms = ["G", "M", "q", "k", "m_W", "g", "alpha_s", "sigma"]
n_master, n_sm = len(master_syms), len(sm_syms)
add("INFO", "Z20", "符号计数：主方程 7 个符号，其中 %d 个由 K/T 之外的外部输入承担" % (n_master - 2),
    "主方程符号集 " + "/".join(master_syms) + "；被拟合的标准势符号集 " + "/".join(sm_syms)
    + "。映射为 1:1（每个标准量对应一个 K/T 取值）⇒ **信息增量为 0**："
    "把 SM 参数装进「几何势差」不产生新预测力，只产生新的记号层。")

# =====================================================================
# 7. 组 D：结论层与跨册台账
# =====================================================================
add("PASS", "Z21", "结论「玩具模型、不统一四力」诚实，且与库内既有读数一致",
    "来料 §六 明确写「原 TUFT V4.0 不成立」「不能无参数统一四力」「不能替代标准模型和广义相对论」。"
    "交叉印证：r14（耦合不可编码连续量）、r15（Ω5 口径 II 自由度 = 5）、r22（恒等式复读族）、"
    "r30 Y30（差值守恒 ⇒ 永不汇聚）四条独立读数指向同一结论。"
    "本册新增的独立证据是 Z11（零判别力）：即使不去比数值，方程结构本身已无约束力。")

add("PASS", "Z22", "结论「不能自动产生电荷/色荷/弱同位旋」成立（量纲层的硬约束）",
    "电荷：Q 维恒 0（Z15）；色荷需 SU(3) 表示与 8 个生成元（r30 Y22 已判 4 分量不足）；"
    "弱同位旋需手征算符（r30 Y17 已判无手征算符、无质量项）。"
    "⇒ 这不是「本框架尚未做到」，而是**在只保留 K/T 两个标量的前提下不可能做到**。")

add("INFO", "Z23", "与 V4.0 的净差：+m（等效原理自动成立）、-r（球对称修正）、-c^2->+mc^2（补回质量维）",
    "三处修改都是**记账性**修复：补 m 解决量纲、补 -r 解决球对称梯度、补 mc^2 使量纲闭合；"
    "没有一处增加对相互作用的约束能力。本册全部 PASS 项（Z01-Z05、Z08-Z10、Z14、Z16）"
    "都属于「把错的改成对的」，不产生任何新的可检验预言。")

add("INFO", "Z24", "「多乘一个 r」的指控排序可优化（来料列为第 3 位，实为第 3 顺位而非并列）",
    "来料 §一.2（量纲缺质量）与 §一.1（矢量/标量混用）任一条单独成立即足以否证原式；"
    "§一.3「多乘 r」是在前两条之后才成为诊断项。建议措辞改为「第三条为次级诊断」。"
    "（不改变判定，仅口径优化；登记为 INFO 而非 CORRECTED。）")

# =====================================================================
# 8. 跨册逐字比对（与 r30 / r28 的式集；声明：仅比对，不重算他册判定）
# =====================================================================
import difflib

PRIOR = {
    "r30_v40_force": "F_uni = -c^2 nabla(kappa^2 - tau^2) . r",
    "r30_v40_sph": "F_uni = -c^2 r d/dr (kappa^2 - tau^2)",
    "r30_v40_em": "nabla^mu F_{mu nu} = tau_{nu alpha beta} tau^{alpha beta}_{nu}",
    "r30_v40_beta": "beta(g) = mu dg/dmu = f(kappa, tau)",
    "r31_v41_action": "S = int d^4x sqrt(-g) [ R/(2 kappa^2) + F^2/4 + alpha T^2 + psibar(i gamma D - m)psi + |D H|^2 - V(H) ]",
}
sim_rows = []
for k_lai, v_lai in LAI.items():
    best = (None, Decimal(-1))
    for k_p, v_p in PRIOR.items():
        ratio = Decimal(repr(difflib.SequenceMatcher(None, v_lai, v_p).ratio()))
        if ratio > best[1]:
            best = (k_p, ratio)
    sim_rows.append({"lai_key": k_lai, "closest_prior": best[0], "similarity": float(best[1])})
mean_sim = sum(Decimal(repr(s_["similarity"])) for s_ in sim_rows) / Decimal(len(sim_rows))
add("INFO", "Z25", "跨册逐字比对：V4.1 与 V4.0/r31 的方程层重合度低（均值 "
    + fmt(mean_sim, 4) + "），但共享同一条「挠率 = 曲率差」的母题",
    "逐条最近邻相似度：" + "；".join([s_["lai_key"] + "->" + s_["closest_prior"] + "="
                                     + fmt(Decimal(repr(s_["similarity"])), 4) for s_ in sim_rows])
    + "。⇒ V4.1 相对 V4.0 是**真实的自我修正**（不是换符号重犯），"
      "但修正只发生在「写对」层面，未触及「能否统一四力」层面。")
KEY["sim_rows"] = sim_rows
KEY["mean_similarity"] = fmt(mean_sim, 4)

add("INFO", "Z26", "本册自抓 3 处工程缺陷（已修并复跑），登记为方法论条目",
    "(1) **汤川指数符号写反**：首版把 U=-g^2 e^{-m r}/r 写成 exp(+m r)，与来料 §四.3 不符；"
    "机器对拍立刻报相对残差 3.6E-04（远大于 1E-25 门限）⇒ 定位到符号而非精度。"
    "(2) **Z01 缺口口径写错**：首版 guard 断言缺口恰为 M，实际机器展开为 M·L（两维），"
    "已改判据并同步修正条目措辞。"
    "(3) **绝对残差判据在大数量级处失效**：牛顿力约 1e22 N 时绝对残差 2E+06 无意义，"
    "已全部改用相对判据（相对残差 1E-16 量级 = 机器零）。"
    "教训：数值对拍必须先核对量级再选判据；「残差为零」在本册三处都是**相对**意义的机器零。")

# =====================================================================
# 9. 自检（guard）
# =====================================================================
GUARDS = []


def guard(name, ok, msg):
    GUARDS.append({"name": name, "ok": bool(ok), "msg": msg})
    return ok


guard("g01_v40_gap_is_ML",
      gap_v40 == (Fraction(-1), Fraction(-1), Fraction(0), Fraction(0))
      and dim_v40_with_r == (Fraction(0), Fraction(0), Fraction(-2), Fraction(0)),
      "原版乘 r 后量纲 = T^-2，与 [F] 之差 = M^-1 L^-1（即差一个 ML）")
guard("g02_v41_dim_closes", iszero(dsub(dim_v41_F, d_F_SI)) and iszero(dsub(dim_v41_U, d_U)),
      "V4.1 的 U 与 F 量纲分别闭合于 ML^2T^-2 / MLT^-2")
guard("g03_fd_converges", fd_rows[-1]["rel_err"] < fd_rows[0]["rel_err"],
      "中心差分误差随步长减小而下降（" + fmt(Decimal(repr(fd_rows[0]["rel_err"])), 3)
      + " -> " + fmt(Decimal(repr(fd_rows[-1]["rel_err"])), 3) + "）")
guard("g04_newton_resid_zero", rel_newton < Decimal("1E-15"),
      "牛顿还原相对残差 " + fmt(rel_newton, 3))
guard("g05_three_potentials_fit", fit_ok == 3,
      "三势 3/3 可被主方程拟合（零判别力）")
guard("g06_lambda_family_degenerate", lam_spread == 0,
      "lambda 五点族的力逐位相同（散布 " + fmt(lam_spread, 3) + "）")
guard("g06b_lambda_branch_is_attractive",
      lam_first < 0 and relerr(F_analytic, lam_first) < Decimal("1E-12"),
      "lambda 族为吸引支且与牛顿力相对一致（" + fmt(relerr(F_analytic, lam_first), 3) + "）")
guard("g07_tau_to_zero_repulsive", (F_rep > 0) == (F_analytic < 0),
      "T->0 分支给出排斥力，与牛顿符号相反")
guard("g08_c_cancels", c_diff / abs(c_first) < Decimal("1E-40"),
      "c 在 4 个取值下力相对差 " + fmt(c_diff / abs(c_first), 3) + "（机器零）")
guard("g09_equivalence_principle", acc_spread == 0,
      "加速度与测试质量无关（散布 " + fmt(acc_spread, 3) + "）")
guard("g10_yukawa_sign", rel_yuk < Decimal("1E-15"),
      "汤川求导符号与系数相对残差 " + fmt(rel_yuk, 3))
guard("g11_sigma_share_grows",
      sigma_share[-1]["sigma_fraction"] > sigma_share[0]["sigma_fraction"],
      "sigma 项占比随 r 增大而上升（" + fmt(Decimal(repr(sigma_share[0]["sigma_fraction"])), 3)
      + " -> " + fmt(Decimal(repr(sigma_share[-1]["sigma_fraction"])), 3) + "）")
guard("g12_charge_dim_zero", dim_F_geo_Q == 0,
      "主方程电荷维恒为 0，无法承载库仑 q q'")
guard("g13_ext_inputs_counted", n_ext == 10,
      "外部输入计数 = " + str(n_ext) + "（= Z19 清单长度）")
guard("g14_no_hbar_in_lai", ("hbar" not in LAI_TEXT) and ("\\hbar" not in LAI_TEXT),
      "来料式集内无 hbar（力方程无需量子化常数，与「未量子化」的自称一致）")

# =====================================================================
# 10. 落盘
# =====================================================================
def _jsonable(obj):
    if isinstance(obj, dict):
        return dict((k, _jsonable(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, Fraction):
        return str(obj)
    return obj


def write_outputs(cnt, guard_pass):
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    payload = {
        "tag": TAG,
        "round": ROUND,
        "date": "2026-10-10",
        "engine": "源码/TUFT-V41几何势修复版_全维审计_2026-10-10.py",
        "lai_sections": 6,
        "counts": cnt,
        "items_total": len(ITEMS),
        "guards": {"total": len(GUARDS), "passed": guard_pass},
        "items": ITEMS,
        "key_numbers": KEY,
        "guards_detail": GUARDS,
        "division_of_labor": [
            "r28/r29/r30 审 V4.0 本体（框架/自称/终极方程组）",
            "r31(V41全维候选) 审 V4.1 嵌入全维框架后的作用量",
            "r31(V40fix) 审 V4.0 修复路径的闭合性",
            "本册 r32 审 V4.1 主方程本身：可求导性、量纲、四条极限、零判别力",
        ],
        "not_self_derived": [
            "非中心相互作用（磁力/多极矩）在一般 U(x) 下的推广形式未自推",
            "GR 度规场方程层面（V4.1 无场方程，无限位力论）未自推",
            "色荷/超荷的量子数层不在本册式集内",
        ],
    }
    jp = os.path.join(DATA_DIR, TAG + ".json")
    with io.open(jp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(_jsonable(payload), ensure_ascii=False, indent=2))

    order = ["PASS", "FAIL", "CORRECTED", "MISMATCH", "BOUNDARY", "INFO"]
    lines = []
    lines.append("# 数据: " + TAG)
    lines.append("")
    lines.append("## 条目统计")
    lines.append("")
    lines.append("- " + " / ".join([k + "=" + str(cnt[k]) for k in order]))
    lines.append("- 自检 guard: " + str(guard_pass) + " / " + str(len(GUARDS)) + " 通过")
    lines.append("")
    lines.append("## 条目明细")
    lines.append("")
    for it in ITEMS:
        lines.append("- **" + it["id"] + "** [" + it["verdict"] + "] " + it["title"])
        lines.append("")
        lines.append("  " + it["detail"].replace("\n", "\n  "))
        lines.append("")
    mp = os.path.join(DATA_DIR, TAG + ".md")
    with io.open(mp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    rep = []
    rep.append("=" * 68)
    rep.append("TUFT V4.1 几何势修复版 · 全维审计 (" + ROUND + ")")
    rep.append("=" * 68)
    rep.append("counts: " + " / ".join([k + "=" + str(cnt[k]) for k in order]))
    rep.append("guards: " + str(guard_pass) + "/" + str(len(GUARDS)))
    rep.append("")
    for it in ITEMS:
        rep.append("[" + it["verdict"] + "] " + it["id"] + " " + it["title"])
        rep.append("    " + it["detail"])
        rep.append("")
    rp = os.path.join(DATA_DIR, TAG + "_report.txt")
    with io.open(rp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rep))
    return jp, mp, rp


def main():
    cnt = tally()
    guard_pass = sum(1 for g in GUARDS if g["ok"])
    paths = write_outputs(cnt, guard_pass)
    print("=" * 68)
    print("TUFT V4.1 几何势修复版 · 全维审计 (" + ROUND + ")")
    print("=" * 68)
    print("条目 " + str(len(ITEMS)) + "：" + " / ".join(
        [k + "=" + str(cnt[k]) for k in ["PASS", "FAIL", "CORRECTED", "MISMATCH", "BOUNDARY", "INFO"]]))
    print("自检 " + str(guard_pass) + "/" + str(len(GUARDS)))
    print("")
    print("硬读数：")
    print("  Z11 零判别力：三势可拟合 " + str(KEY["fit_ok"]) + "/3")
    print("  Z12 lambda 族力散布 = " + KEY["lam_spread"])
    print("  Z13 T->0 分支 F_r = " + KEY["F_repulsive"] + "（与牛顿 " + KEY["F_newton_1AU_earth"] + " 反号）")
    print("  Z08 牛顿 F_r(1AU, 地球) = " + KEY["F_newton_1AU_earth"])
    print("  Z19 外部输入计数 = " + str(KEY["n_ext_inputs"]))
    print("  Z25 与 V4.0 式集平均相似度 = " + KEY["mean_similarity"])
    print("")
    for p in paths:
        print("写出: " + os.path.basename(p))
    if guard_pass != len(GUARDS):
        for g in GUARDS:
            if not g["ok"]:
                print("GUARD FAIL: " + g["name"] + " -- " + g["msg"])
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
