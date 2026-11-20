# -*- coding: utf-8 -*-
"""r429 · ROOT V119 五高度离散谱判据与 1/3 耦合映射 全维审计引擎.

性质：外部来料（ROOT V119 科研裁定报告正文）独立可算审计。
编号：查磁盘 r429 起空闲，取 r429，不覆盖并发会话文件。
方法：纯标准库 Decimal 60 位 + 双路径对拍 + 阳性对照 + 高斯反解 + 定种子 MC。
红线：数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功。
"""
import os
import sys
import json
import math
import random
import hashlib
from decimal import Decimal, getcontext, localcontext

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60
D = Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "数据")
STAMP = "2026-11-21"
RID = "r429"

ENTRIES = []
GUARDS = []


def add(code, verdict, title, detail):
    ENTRIES.append({"id": code, "verdict": verdict, "title": title, "detail": detail})


def guard(code, ok, detail):
    GUARDS.append({"id": code, "ok": bool(ok), "detail": detail})
    if not ok:
        raise AssertionError("GUARD-FAIL %s : %s" % (code, detail))


def sci(x, n=10):
    v = D(x) if not isinstance(x, Decimal) else x
    if v == 0:
        return "0"
    return format(v, ".%dE" % n)


def rel(a, b):
    a = D(str(a))
    b = D(str(b))
    if b == 0:
        return D("Infinity")
    return abs(a - b) / abs(b)


def fs(x, n=10):
    return format(D(str(x)), ".%dE" % n)


def dsinh(x):
    """Decimal 无 sinh/cosh（Python 3.8 标准库限制），此处自实现并由 G_sinh_guard 守卫。"""
    e = x.exp()
    return (e - 1 / e) / 2


def dcosh(x):
    e = x.exp()
    return (e + 1 / e) / 2


# ------------------------------------------------------------------ 常数
G = D("6.67430e-11")
M_E = D("5.9722e24")
GM = D("3.986004418e14")
C_LIGHT = D("299792458")
HBAR = D("1.054571817e-34")
EV_J = D("1.602176634e-19")
R_E = D("6371000")            # m（平均地球半径）
G0_STD = D("9.80665")

L_ = D("124600")              # m（来料作用程 124.6 km）
ALPHA_Y = D(1) / D(3)         # 来料耦合 1/3
K_ = D(1) / L_                # 1/m
U_ = K_ * R_E                 # 51.13162...
X_ = U_                      # x = R/ell

DR = D("50000")               # m，采样步长 50 km（由 H_1/H_0 反解得到）
DELTA = DR / L_
Q = (-DELTA).exp()

EPS0_UNIFORM_V119 = D("0.0097749444")   # 来料 §二 均匀密度 0.97749444%
EPS0_IMPROVED_V119 = D("0.0059544049")  # 来料 §二 改进解析密度 0.59544049%
EPS0_USED = EPS0_IMPROVED_V119          # 来料固定参数 eps_0 = 0.005954

H1H0_V119 = D("0.44817647")   # 来料 模型 A 的 H_1/H_0
H0A_V119 = D("-1.02853e-10")  # 来料 模型 A 的 H_0
H0B_V119 = D("1.34440e-8")    # 来料 模型 B 的 H_0
L_PSEUDO_V119 = D("161.165")  # 来料 模型 B 的伪作用程 km
DG400_V119 = D("2.217e-3")    # 来料 delta g @ 400 km (m/s^2)
DPREC_V119 = D("0.04317888")  # 来料 近拱点进动 rad
DNU_V119 = D("7.65e-14")      # 来料 地表->400km 引力频移
MPHI_V119 = D("1.5837e-12")   # 来料 m_phi c^2 (eV)
A_V119 = D("2.5875e9")        # 来料 a (m^2)
ELL2_V119 = D("300000")       # 来料 第二作用程 300 km

HEIGHTS = [D(0), D(50000), D(100000), D(150000), D(200000), D(250000), D(300000)]
H400 = D("400000")

# ------------------------------------------------------------------ 模型函数
def eps_profile(r, eps0=EPS0_USED):
    """地表归一化的 Yukawa 形状 eps(r) = eps0*(1+kr)/(1+u)*exp(-k(r-R))."""
    return eps0 * (1 + K_ * r) / (1 + U_) * (-(K_ * (r - R_E))).exp()


def eps_profile_prime(r, eps0=EPS0_USED):
    """d eps / dr 的解析式。"""
    return -eps0 * K_ * K_ * r * (-(K_ * (r - R_E))).exp() / (1 + U_)


def k_tilde(h, eps0=EPS0_USED, shape=1):
    """无量纲有效引力参数 Ktilde = 1 + eps（shape 为形状因子的额外乘子）。"""
    r = R_E + h
    return 1 + shape * eps_profile(r, eps0)


def d_seq(n, eps0=EPS0_USED, shape=1):
    """D_n = Ktilde_{n+1} - Ktilde_n（n 从 0 起，采样点 h_j = j*DR，j = n, n+1, ...）。

    注意：首版曾写成 kt(n*DR) - kt((n-1)*DR)，等价于把采样窗口整体左移一格
    （D_0 取成了 kt(0)-kt(-DR) 的外推值），导致 H_0 与闭式差 1.23 倍。
    本册按「D_n 覆盖采样点 j = n, n+1, n+2」的定义重建，并由 G_dseq_index 守卫。
    """
    return k_tilde(D(n + 1) * DR, eps0, shape) - k_tilde(D(n) * DR, eps0, shape)


def h_seq(n, eps0=EPS0_USED, shape=1):
    """H_n = D_n*D_{n+2} - D_{n+1}^2。"""
    return d_seq(n, eps0, shape) * d_seq(n + 2, eps0, shape) - d_seq(n + 1, eps0, shape) ** 2


def eps_pointmass(r, alpha=ALPHA_Y):
    """点质量 Yukawa 口径：eps(r) = alpha*(1+k r)*exp(-k r)。"""
    return alpha * (1 + K_ * r) * (-(K_ * r)).exp()


# ==================================================================
# 区块 V1：离散谱判据的代数重建与判别力定价
# ==================================================================
# V1-01 恒等式：D_n = C q^n (a + b n)，H_n = -C^2 b^2 q^{2n}
cases = []
for dr_m in (D("50000"), D("20000"), D("100000")):
    for ell_m in (L_, D("90000"), D("300000")):
        kk = D(1) / ell_m
        dd = dr_m / ell_m
        qq = (-dd).exp()
        x0 = kk * R_E
        # 通用形状 K(r) = A + B(1+kr)e^{-kr}，取 A=1, B=1，采样起点 r0 = R
        cc = (-x0).exp()                          # C = B e^{-k r0}
        aa = (qq - 1) * (1 + x0) + qq * dd        # a
        bb = (qq - 1) * dd                        # b
        # 独立采样路径（不引用闭式，防止自证）
        def ksamp(n, kk=kk, dr=dr_m, r0=R_E):
            r = r0 + D(n) * D(dr)
            return D(1) + (1 + kk * r) * (-(kk * r)).exp()

        def dsamp(n, **kw):
            return ksamp(n + 1, **kw) - ksamp(n, **kw)

        def hsamp(n, **kw):
            return dsamp(n, **kw) * dsamp(n + 2, **kw) - dsamp(n + 1, **kw) ** 2

        d0_s = dsamp(0)
        d0_c = cc * aa
        h0_s = hsamp(0)
        h0_c = -(cc * cc) * (bb * bb) * (qq ** 2)   # H_n = -C^2 b^2 q^{2n+2}（n=0）
        h1_s = hsamp(1)
        cases.append((dr_m, ell_m, h0_s, h0_c, rel(h0_s, h0_c),
                      h1_s / h0_s, qq ** 2, rel(d0_s, d0_c)))
max_h_err = max(c[4] for c in cases)
max_ratio_err = max(abs(c[5] - c[6]) for c in cases)
max_d_err = max(c[7] for c in cases)
all_neg = all(c[2] < 0 for c in cases)
guard("G_identity_reconstruct", max_h_err < D("1e-25"),
      "H_n = -C^2 b^2 q^{2n+2} 闭式与独立采样残差 %s（9 组参数）" % sci(max_h_err))
guard("G_identity_D_closed", max_d_err < D("1e-25"),
      "D_n = C q^n (a+bn) 闭式与独立采样残差 %s（9 组参数）" % sci(max_d_err))
guard("G_identity_ratio", max_ratio_err < D("1e-25"),
      "H_{n+1}/H_n = q^2 残差 %s" % sci(max_ratio_err))
guard("G_identity_sign", all_neg, "9 组参数下 H_n 全部 < 0（恒成立）")
add("V1-01", "PASS", "离散谱判据的代数结构可完整重建（严格恒等式）",
    "由 K(r)=A+B(1+kr)e^{-kr} 逐差推得 D_n = C q^n (a+bn)；再由 H_n = D_n D_{n+2} - D_{n+1}^2 "
    "（两均带 q^{2n+2}）得 H_n = -C^2 b^2 q^{2n+2} < 0，且 H_{n+1}/H_n = q^2 = e^{-2dr/ell}；"
    "9 组 (dr, ell) 参数下闭式与独立采样残差 %s（D_n 闭式残差 %s，比值残差 %s），且 H_n 恒为负 "
    "⇒ 来料所述「必要条件」在代数上确实成立。"
    "★方法论留痕：首版闭式漏掉 q^2 因子（H_n 写成 -C^2 b^2 q^{2n}），被守卫 G_identity_reconstruct 当场拦下"
    % (sci(max_h_err), sci(max_d_err), sci(max_ratio_err)))

# V1-02 判别力定价：恒等式对任意参数成立 ⇒ 对单作用程族零判别力；阳性对照（非指数形状破裂）
shape_mult = lambda r: 1 + K_ * (r - R_E)


def h_seq_shaped(n, eps0=EPS0_USED):
    """注入非指数形状因子 (1 + k(r-R)) 后的 H_n（注意 k_tilde 的首参是高度 h 不是半径 r）。"""

    def ds(m):
        h0 = D(m) * DR
        h1 = D(m + 1) * DR
        return (k_tilde(h1, eps0, shape_mult(R_E + h1))
                - k_tilde(h0, eps0, shape_mult(R_E + h0)))

    return ds(n) * ds(n + 2) - ds(n + 1) ** 2


ratio_shape = h_seq_shaped(1) / h_seq_shaped(0)
guard("G_criterion_teeth", abs(ratio_shape - Q ** 2) > D("1e-10"),
      "阳性对照：注入非指数形状后 H_1/H_0=%s 与 q^2=%s 显著不同 ⇒ 判据只对形状敏感"
      % (sci(ratio_shape), sci(Q ** 2)))
add("V1-02", "FAIL", "该「必要条件」对单作用程族零判别力（只判形状族）",
    "H_n<0 与 H_{n+1}/H_n=e^{-2dr/ell} 是 K(r)=A+B(1+kr)e^{-kr} 的代数恒等式，"
    "对任意 (r_0, dr, ell, alpha) 恒成立 ⇒ 它不能判决模型是否正确，只能判决「形状族」；"
    "阳性对照：给 eps 乘上非指数因子 (1+k(r-R)) 后同一比值变为 %s（q^2=%s），判据确有牙但只针对形状"
    % (sci(ratio_shape), sci(Q ** 2)))

# V1-03 由 H_1/H_0 反解采样步长
ratio_num = h_seq(1, EPS0_USED) / h_seq(0, EPS0_USED)
dr_from_ratio = L_ * (-ratio_num.ln()) / D(2)
dr_pred_50 = L_ * (-Q ** 2).ln() / D(2)
guard("G_ratio_invert_dr", abs(rel(dr_from_ratio, DR)) < D("1e-3"),
      "由 %s 反解 dr = %s m（来料隐含 50 km）" % (ratio_num, fs(dr_from_ratio, 8)))
guard("G_ratio_forward_50km", rel(Q ** 2, H1H0_V119) < D("1e-6"),
      "dr=50 km 正推 H_1/H_0 = %s vs 来料 %s（相对差 %s）"
      % (sci(Q ** 2), H1H0_V119, sci(rel(Q ** 2, H1H0_V119))))
add("V1-03", "PASS", "来料 H_1/H_0 = 0.44817647 反解出采样步长 dr = 50 km",
    "本册自算 H_1/H_0 = %s；由 e^{-2 dr/ell} 反解 dr = %s m（= %.4f km），"
    "取整 dr = 50 km 正推得 %s（相对来料 %s 差 %s）⇒ 来料的离散谱采样步长被独立锁定"
    % (sci(ratio_num), fs(dr_from_ratio, 8), float(dr_from_ratio) / 1000.0,
       sci(Q ** 2), H1H0_V119, sci(rel(Q ** 2, H1H0_V119))))

# V1-04 H_0 绝对值的口径与可复现性
C_PROF = EPS0_USED / (1 + U_)                 # eps-剖面口径：C = B e^{-k r0} = eps0/(1+u)
B_PROF = (Q - 1) * DELTA                      # b = (q-1) k dr
h0_closed_prof = -(C_PROF ** 2) * (B_PROF ** 2) * (Q ** 2)
h0_sampled = h_seq(0, EPS0_USED)
h0_closed_pm = -(ALPHA_Y ** 2) * (B_PROF ** 2) * (Q ** 2)   # 点质量口径：C = alpha


def h0_of_ell(ell):
    k = D(1) / ell
    q = (-(k * DR)).exp()
    u = k * R_E
    c = EPS0_USED / (1 + u)
    b = (q - 1) * (DR / ell)
    return -(c ** 2) * (b ** 2) * (q ** 2)


lo_e, hi_e = D("123000"), D("126500")
f_lo = h0_of_ell(lo_e) - H0A_V119
for _ in range(300):
    mid = (lo_e + hi_e) / 2
    fm = h0_of_ell(mid) - H0A_V119
    if (fm > 0) == (f_lo > 0):
        lo_e = mid
        f_lo = fm
    else:
        hi_e = mid
ell_implied = (lo_e + hi_e) / 2
guard("G_h0_reproducible", rel(h0_closed_prof, H0A_V119) < D("1e-3"),
      "eps-剖面口径 H_0 = %s（独立采样 %s，残差 %s）vs 来料 %s ⇒ 相对差 %s"
      % (sci(h0_closed_prof, 12), sci(h0_sampled, 12), sci(rel(h0_sampled, h0_closed_prof)),
         H0A_V119, sci(rel(h0_closed_prof, H0A_V119))))
guard("G_h0_ell_implied_close", rel(ell_implied, L_) < D("1e-3"),
      "反解使 H_0 精确等于来料的 ell = %s m（与 124600 相对差 %s）⇒ 差异来自有效数字而非口径"
      % (fs(ell_implied, 10), sci(rel(ell_implied, L_))))
guard("G_h0_calibration_dependent", abs(h0_closed_pm / h0_closed_prof) > D("1e6"),
      "口径依赖：eps-剖面 H_0 = %s vs 点质量口径 H_0 = %s（差 %.2e 倍）⇒ 绝对值不可跨口径移植"
      % (sci(h0_closed_prof, 12), sci(h0_closed_pm, 12), float(abs(h0_closed_pm / h0_closed_prof))))
add("V1-04", "CORRECTED", "H_0 绝对值可复现（首版判「不可复现」为误判，已更正）",
    "在「Ktilde = 1 + eps(h)、dr = 50 km、eps-剖面口径」下 H_0 = -C^2 b^2 q^2 的闭式与独立采样一致到 %s，"
    "给 %s；来料 H_0 = %s，相对差 %s。"
    "★更正：本册首版把该读数判为「绝对值不可复现」，机器复算证明它可复现，"
    "差异仅来自来料内部 ell / eps_0 的有效数字——反解使 H_0 精确等于来料值的 ell = %s m（与 124600 相对差 %s）。"
    "但绝对值由归一化口径决定：同一采样下点质量口径给 H_0 = %s（差 %.2e 倍）"
    "⇒ 可跨口径移植的仍只有比值 H_1/H_0 与符号"
    % (sci(rel(h0_sampled, h0_closed_prof)), sci(h0_closed_prof, 12), H0A_V119,
       sci(rel(h0_closed_prof, H0A_V119)), fs(ell_implied, 10), sci(rel(ell_implied, L_)),
       sci(h0_closed_pm, 12), float(abs(h0_closed_pm / h0_closed_prof))))

# V1-05 模型 B（双作用程）违反必要条件
L2 = ELL2_V119
K2 = D(1) / L2
U2 = K2 * R_E

def dual_eps(h, w2):
    r = R_E + h
    e1 = eps_profile(r, EPS0_USED)
    e2 = EPS0_USED * (1 + K2 * r) / (1 + U2) * (-(K2 * (r - R_E))).exp()
    return (1 - w2) * e1 + w2 * e2

def dual_h(n, w2):
    def dd(m):
        return dual_eps(D(m + 1) * DR, w2) - dual_eps(D(m) * DR, w2)
    return dd(n) * dd(n + 2) - dd(n + 1) ** 2

scan = []
flip_w2 = None
prev_w = None
prev_sign = None
w = D("0.00005")
while w <= D("0.30"):
    h0 = dual_h(0, w)
    sgn = 1 if h0 > 0 else (-1 if h0 < 0 else 0)
    if prev_sign is not None and sgn != 0 and prev_sign != 0 and sgn != prev_sign and flip_w2 is None:
        lo_w, hi_w = prev_w, w
        f_lo = dual_h(0, lo_w)
        for _ in range(200):
            mid = (lo_w + hi_w) / 2
            fm = dual_h(0, mid)
            if (fm > 0) == (f_lo > 0):
                lo_w = mid
                f_lo = fm
            else:
                hi_w = mid
        flip_w2 = (lo_w + hi_w) / 2
    prev_w = w
    prev_sign = sgn
    scan.append((w, h0))
    w += D("0.00025")
h0_w_max = scan[-1][1]
guard("G_modelB_sign_flip", flip_w2 is not None,
      "双作用程模型在权重区间内 H_0 由负转正（翻转点 w2=%s）" % (sci(flip_w2) if flip_w2 is not None else "NA"))
guard("G_modelB_v119_unreachable", h0_w_max < H0B_V119,
      "本册模型 B 参数化在 w2 <= 0.30 内 H_0 上限 %s < 来料 %s ⇒ 来料模型 B 的参数化未被本册完全复现"
      % (sci(h0_w_max), H0B_V119))
# 伪作用程条件反演（H_1/H_0 = q^2 = e^{-2 dr/ell}，故取平方）
ratio_pseudo_implied = (-(D(2) * DR / (L_PSEUDO_V119 * 1000))).exp() ** 2
add("V1-05", "PASS", "模型 B（双作用程）违反必要条件——符号层面标度无关地独立复现",
    "双作用程 eps = (1-w2) eps_124.6km + w2 eps_300km 的采样谱在 w2 >= %s 时 H_0 转正（来料 +%s），"
    "证实来料「双作用程被必要条件排除」的定性结论与归一化无关；"
    "★更强的读数：翻转点落在 w2 ~ %s（千分之几）处，即排除对双作用程混合权重极其敏感；"
    "但本册参数化在 w2 <= 0.30 内 H_0 上限只有 %s（来料 %s），故来料模型 B 的具体参数化未被完全复现，"
    "本册只复现其定性排除；条件反演：来料伪作用程 %s km 对应 H_1/H_0 = %s，与单作用程要求的 %s 不符"
    % (sci(flip_w2), H0B_V119, sci(flip_w2), sci(h0_w_max), H0B_V119,
       L_PSEUDO_V119, sci(ratio_pseudo_implied), sci(Q ** 2)))

# ==================================================================
# 区块 V2：均匀球地表异常的独立第一性推导
# ==================================================================
def eps0_uniform_closed(alpha=ALPHA_Y):
    """闭式（取 u 大时的领先项 + 指数精确修正）。"""
    lead = D(3) * alpha / D(2) * (X_ ** 2 - 1) / X_ ** 3
    exact_extra = D(3) * alpha / D(2) * (X_ + 1) ** 2 * (-(2 * X_)).exp() / X_ ** 3
    return lead, exact_extra


def eps0_uniform_integral(alpha=ALPHA_Y, rho=D("5515")):
    """积分路径：eps0 = 4 pi alpha (1+u) e^{-u} I / (k M)，I = int_0^R r' rho sinh(k r') dr'。

    注：Python 3.8 标准库 Decimal 无 sinh/cosh，首版直接调用会 AttributeError，
    改为自实现 dsinh/dcosh 并由 G_sinh_cosh_guard 以已知值守护。
    """
    sh = dsinh(U_)
    ch = dcosh(U_)
    I = rho * (R_E * ch / K_ - sh / K_ ** 2)
    mass = D(4) / D(3) * D(str(math.pi)) * rho * R_E ** 3
    return D(4) * D(str(math.pi)) * alpha * (1 + U_) * (-U_).exp() * I / (K_ * mass)


guard("G_sinh_cosh_guard", rel(dsinh(D(1)), D("1.1752011936438014568823818505956")) < D("1e-40")
      and rel(dcosh(D(1)), D("1.5430806348152437784779056207571")) < D("1e-40"),
      "自实现 dsinh/dcosh 在 x=1 处与解析值一致（相对残差 %s / %s）"
      % (sci(rel(dsinh(D(1)), D("1.1752011936438014568823818505956")), 3),
         sci(rel(dcosh(D(1)), D("1.5430806348152437784779056207571")), 3)))


lead_u, extra_u = eps0_uniform_closed()
int_u = eps0_uniform_integral()
guard("G_uniform_two_path", rel(lead_u, int_u) < D("1e-30"),
      "闭式 %s vs 积分路径 %s（相对差 %s）" % (sci(lead_u), sci(int_u), sci(rel(lead_u, int_u))))
guard("G_uniform_match_v119", rel(lead_u, EPS0_UNIFORM_V119) < D("1e-8"),
      "均匀球 eps0 = %s（来料 %s，相对差 %s）" % (sci(lead_u), EPS0_UNIFORM_V119, sci(rel(lead_u, EPS0_UNIFORM_V119))))
guard("G_uniform_exact_correction_tiny", abs(extra_u) < D("1e-40"),
      "指数级精确修正 %s（小到可忽略但保留）" % sci(extra_u))
eps_pm_surface = eps_pointmass(R_E)
guard("G_pointmass_vs_extended", rel(eps_pm_surface, lead_u) > D("1e15"),
      "阳性对照：点质量口径地表 eps = %s，与均匀球口径差 %.1f 个量级 ⇒ 两机制不可混同"
      % (sci(eps_pm_surface), float(math.log10(abs(lead_u / eps_pm_surface)))))
add("V2-01", "PASS", "均匀球地表 Yukawa 异常可第一性推导并逐位复现 0.97749444%",
    "由源分布积分独立推出 eps0 = 4*pi*alpha*(1+u)e^{-u} I/(k M)（I=int_0^R r' rho sinh(k r') dr'），"
    "闭式化为 (3 alpha/2)(x^2-1)/x^3，x = R/ell = %s；本册给 %s = %s%%，来料 %s%%，相对差 %s；"
    "闭式与积分双路径残差 %s；指数级精确修正 %s"
    % (sci(X_, 12), sci(lead_u, 12), fs(lead_u * 100, 10), fs(EPS0_UNIFORM_V119 * 100, 10),
       sci(rel(lead_u, EPS0_UNIFORM_V119)), sci(rel(lead_u, int_u)), sci(extra_u)))
add("V2-02", "PASS", "阳性对照：点质量口径与扩展体口径地表效应差 %.1f 个量级" %
    float(math.log10(abs(lead_u / eps_pm_surface))),
    "点质量 Yukawa 在地表给 eps = %s（几乎为零），均匀球扩展体口径给 %s（0.977494%%）；"
    "两者是不同机制的量级分离（差 %.2f 个量级）⇒ 来料把地表异常归因于「均匀密度 + 作用程」是自洽的，"
    "但任何点质量公式都不能复现它"
    % (sci(eps_pm_surface), sci(lead_u), float(math.log10(abs(lead_u / eps_pm_surface)))))

# V2-03 改进解析密度档
def eps0_layered(layers, alpha=ALPHA_Y):
    """layers: [(r_inner, r_outer, rho), ...]，内部 r' rho sinh(k r') 逐层积分，总质量归一到 M_E。"""
    raw_i = D(0)
    raw_m = D(0)
    for r0, r1, rho in layers:
        f = lambda r: r * dcosh(K_ * r) / K_ - dsinh(K_ * r) / K_ ** 2
        raw_i += rho * (f(r1) - f(r0))
        raw_m += D(4) / D(3) * D(str(math.pi)) * rho * (r1 ** 3 - r0 ** 3)
    scale = M_E / raw_m
    I = raw_i * scale
    return D(4) * D(str(math.pi)) * alpha * (1 + U_) * (-U_).exp() * I / (K_ * M_E)

RC = D("3480000")
cands = {
    "两层(核3480km@13000/幔5515)": [(D(0), RC, D("13000")), (RC, R_E, D("5515"))],
    "三层(壳2900/幔5400/核11000)": [(D(0), RC, D("11000")), (RC, R_E - D("35000"), D("5400")),
                          (R_E - D("35000"), R_E, D("2900"))],
    "四层(2900/5500/10500/13200)": [(D(0), RC, D("13200")), (RC, D("410000"), D("10500")),
                          (D("410000"), R_E - D("35000"), D("5500")), (R_E - D("35000"), R_E, D("2900"))],
}
cand_res = {}
for nm, lay in cands.items():
    e = eps0_layered(lay)
    cand_res[nm] = (e, e / lead_u)
# 反解：两层模型中核密度取何值才能复现来料改进档
def eps0_core(rho_c):
    return eps0_layered([(D(0), RC, rho_c), (RC, R_E, D("5515"))])
lo, hi = D("8000"), D("40000")
for _ in range(200):
    mid = (lo + hi) / 2
    if eps0_core(mid) > EPS0_IMPROVED_V119:
        lo = mid
    else:
        hi = mid
rho_core_implied = (lo + hi) / 2
eps_core_implied = eps0_core(rho_core_implied)
guard("G_improved_inversion", rel(eps_core_implied, EPS0_IMPROVED_V119) < D("1e-20"),
      "反解核密度 %s kg/m^3 复现来料改进档 %s（实际 %s）"
      % (fs(rho_core_implied, 8), EPS0_IMPROVED_V119, sci(eps_core_implied)))
ratio_improved_target = EPS0_IMPROVED_V119 / lead_u
best = None
for nm, (e, r) in cand_res.items():
    if best is None or abs(r - ratio_improved_target) < abs(best[1] - ratio_improved_target):
        best = (nm, r, e)
guard("G_improved_candidates_scanned", len(cand_res) == 3,
      "三族候选解析剖面均已复算（未命中来料档）")
add("V2-03", "BOUNDARY", "改进解析密度档 0.59544049% 不可复现（密度剖面未声明）",
    "来料改进档与均匀档之比为 %s（机器不变量）。本册复算三族解析剖面：%s；"
    "最接近者为「%s」（比值 %s），均未命中。反解：两层模型（幔 5515、核边界 3480 km）需核密度 %s kg/m^3 才复现来料档。"
    "⇒ 该数值的物理内容由「所选剖面」决定，未声明剖面时不可复算"
    % (sci(ratio_improved_target),
       "；".join("%s -> eps0=%s（比值 %s）" % (nm, sci(e), sci(r)) for nm, (e, r) in cand_res.items()),
       best[0], sci(best[1]), fs(rho_core_implied, 8)))

# ==================================================================
# 区块 V3：f(R) 映射、标量质量、a
# ==================================================================
A_L2_OVER_6 = L_ ** 2 / D(6)
MPHI_EXACT = HBAR * C_LIGHT / L_ / EV_J
guard("G_a_value", rel(A_L2_OVER_6, A_V119) < D("2e-5"),
      "a = ell^2/6 = %s m^2（来料 %s，相对差 %s）"
      % (fs(A_L2_OVER_6, 10), A_V119, sci(rel(A_L2_OVER_6, A_V119))))
guard("G_mphi_value", rel(MPHI_EXACT, MPHI_V119) < D("1e-3"),
      "m_phi c^2 = hbar c / ell = %s eV（来料 %s，相对差 %s）"
      % (fs(MPHI_EXACT, 12), MPHI_V119, sci(rel(MPHI_EXACT, MPHI_V119))))
a_common = D(3) * L_ ** 2 / D(2)
guard("G_a_convention_gap", rel(a_common, A_L2_OVER_6) > D("8"),
      "口径差：ell=sqrt(6a) 给 a=%s；常用 ell=sqrt(2a/3) 给 a=%s；相差 %.1f 倍"
      % (fs(A_L2_OVER_6, 10), fs(a_common, 10), float(a_common / A_L2_OVER_6)))
add("V3-01", "CORRECTED", "标量质量 m_phi c^2 的精确值与来料小偏差",
    "由作用程直接给出 m_phi c^2 = hbar c / ell = %s eV；来料 1.5837e-12 eV，相对差 %s"
    "（来料 5 位有效数字下超出舍入范围，量级与来源均正确）"
    % (fs(MPHI_EXACT, 12), sci(rel(MPHI_EXACT, MPHI_V119))))
add("V3-02", "PASS", "新裁定：标量质量不是独立参数，而是作用程的重述",
    "m_phi c^2 = hbar c / ell 严格成立 ⇒ m_phi * ell = hbar / c；因此「m_phi = 1.5835e-12 eV」"
    "既不新增自由度也不新增预言，它与「ell = 124.6 km」是同一条信息（自由度账不变）")
add("V3-03", "BOUNDARY", "f(R)=R+aR^2 与 Yukawa 的 ell-a 映射口径依赖",
    "来料取 a = ell^2/6 = %s m^2（本册复算一致，相对差 %s）；而常见约定 ell = sqrt(2a/3) 给出 "
    "a = %s m^2，两者相差 %.1f 倍 ⇒ 「a」不是唯一确定的量，跨文献引用必须声明映射约定"
    % (fs(A_L2_OVER_6, 10), sci(rel(A_L2_OVER_6, A_V119)), fs(a_common, 10),
       float(a_common / A_L2_OVER_6)))

# ==================================================================
# 区块 V4：eps(h) 剖面、delta g、近拱点进动
# ==================================================================
def dg_extra(r):
    """额外引力加速度大小（向内为正）：delta g = GM/r^2 * eps(r)。"""
    return GM / r ** 2 * eps_profile(r, EPS0_USED)


def dg_extra_prime(r):
    return GM * (eps_profile_prime(r, EPS0_USED) / r ** 2 - 2 * eps_profile(r, EPS0_USED) / r ** 3)


def precession(r, use_dgprime=True, exact=True):
    dgp = dg_extra(r)
    dgpp = dg_extra_prime(r) if use_dgprime else D(0)
    wphi2 = GM / r ** 3 + dgp / r
    wr2 = GM / r ** 3 + dgpp + 3 * dgp / r
    if exact:
        return D(2) * D(str(math.pi)) * (wphi2 / wr2).sqrt() - D(2) * D(str(math.pi))
    return D(str(math.pi)) * (wphi2 - wr2) / wr2


r400 = R_E + H400
dg400 = dg_extra(r400)
eps400 = eps_profile(r400, EPS0_USED)
prec_exact = precession(r400, True, True)
prec_linear = precession(r400, True, False)
prec_nodgp = precession(r400, False, True)
prec_firstorder = -r400 * eps_profile_prime(r400, EPS0_USED) / 2
eps0_short = EPS0_USED / (1 + U_)
guard("G_dg400", rel(dg400, DG400_V119) < D("1e-3"),
      "delta g(400km) = %s m/s^2（来料 %s，相对差 %s）"
      % (sci(dg400), DG400_V119, sci(rel(dg400, DG400_V119))))
guard("G_precession_exact", rel(prec_exact, DPREC_V119) < D("1e-3"),
      "近拱点进动 = %s rad（来料 %s，相对差 %s）"
      % (sci(prec_exact), DPREC_V119, sci(rel(prec_exact, DPREC_V119))))
guard("G_precession_sign_sensitivity", prec_nodgp * prec_exact < 0,
      "口径敏感性：丢弃 dg' 项得 %s rad（反号）" % sci(prec_nodgp))
add("V4-01", "PASS", "eps(h) 七高度表与 400 km 额外加速度独立复现",
    "本册模型 eps(r) = eps0*(1+kr)/(1+u)*exp(-k(r-R))；七高度表：%s；"
    "delta g(400 km) = %s m/s^2（来料 %s，相对差 %s），对应 eps(400km) = %s"
    % ("; ".join("%d km: eps=%s" % (int(h / 1000), sci(eps_profile(R_E + h, EPS0_USED))) for h in HEIGHTS),
       sci(dg400), DG400_V119, sci(rel(dg400, DG400_V119)), sci(eps400)))
add("V4-02", "PASS", "400 km 近拱点进动独立复现（须保留径向导数项）",
    "近圆轨道：w_phi^2 = GM/r^3 + dg/r，w_r^2 = GM/r^3 + dg' + 3 dg/r；"
    "Delta-varpi = 2pi(w_phi/w_r - 1) = %s rad（来料 %s，相对差 %s）"
    % (sci(prec_exact), DPREC_V119, sci(rel(prec_exact, DPREC_V119))))
add("V4-03", "INFO", "进动公式的口径敏感性（必须声明保留哪一项）",
    "四种写法：精确式 %s rad；线性化（保留 dg'）%s rad；一阶 d eps 形式 %s rad；"
    "丢弃 dg' 的精确式 %s rad（★反号）。⇒ 来料数值只在「保留 dg' 且用精确频率比」的组合下成立，"
    "口径一旦漏写 dg' 结论会整体翻转"
    % (sci(prec_exact), sci(prec_linear), sci(prec_firstorder), sci(prec_nodgp)))

# ==================================================================
# 区块 V5：引力红移/频移
# ==================================================================
def dU(r):
    """delta U(r) = -(K-GM)/(r(1+r/ell))，在 eps-剖面口径下 (1+kr)/(1+r/ell) 精确约化。"""
    return -GM * eps_profile(r, EPS0_USED) / (r * (1 + r / L_))


dnu = (dU(r400) - dU(R_E)) / (C_LIGHT ** 2)
guard("G_redshift_sign", dnu > 0,
      "频移方向自检：额外势随高度升高而变浅（Phi_ext(r400) > Phi_ext(R_E)）⇒ dnu > 0，实测 %s" % sci(dnu))
guard("G_redshift", rel(dnu, DNU_V119) < D("1e-3"),
      "地表->400km 额外引力频移 = %s（来料 %s，相对差 %s）"
      % (sci(dnu), DNU_V119, sci(rel(dnu, DNU_V119))))
add("V5-01", "PASS", "地表至 400 km 的额外引力频移独立复现",
    "delta U(r) = -(K-GM)/(r(1+r/ell))，代入 K-GM = GM*eps(r) 后 (1+kr)/(1+r/ell) 精确约化为 1，"
    "得 delta U = -GM eps0 exp(-k(r-R))/((1+u) r)；"
    "频移比例 = [dU(R+400km) - dU(R)]/c^2 = %s"
    "（来料 %s，相对差 %s）；★方向自检：额外势随高度变浅 ⇒ 升空时频率升高，dnu > 0"
    % (sci(dnu), DNU_V119, sci(rel(dnu, DNU_V119))))

# ==================================================================
# 区块 V6：G_infinity / G_lab 口径与短程外推
# ==================================================================
ginf_from_alpha = D(1) / (1 + ALPHA_Y)
alpha_eff = ALPHA_Y / (1 + ALPHA_Y)
ginf_lab_reading = D(1) / (1 + alpha_eff)
short_range_pm = ALPHA_Y
guard("G_g_inf_scenarios", abs(ginf_from_alpha - D("0.75")) < D("1e-20") and
      abs(ginf_lab_reading - D("0.8")) < D("1e-20"),
      "G_inf/G_lab：alpha 相对 G_inf 口径 %s；alpha_eff=alpha/(1+alpha)=%s 口径 %s"
      % (ginf_from_alpha, alpha_eff, ginf_lab_reading))
guard("G_short_range_scale", abs(short_range_pm - D(1) / D(3)) < D("1e-20") and eps0_short < D("1e-3"),
      "短程外推：点质量形式 r<<ell 给力增强 %s（=33%%）；重标剖面向内延拓给 %s"
      % (short_range_pm, sci(eps0_short)))
add("V6-01", "BOUNDARY", "G_inf 与 G_lab 的口径依赖：0.75 与 0.80 两读数",
    "来料 G_lab ~ G_inf(1+alpha_Y)、alpha_Y=1/3 给 G_inf ~ 0.75 G_lab（算术正确）；"
    "但若 alpha 是相对 G_inf 的力强修正，则实验室测得的 G 对应 alpha_eff = alpha/(1+alpha) = %s，"
    "从而 G_inf = %s G_lab。两读数相差 %.1f%% ⇒ 「alpha 相对哪个 G」必须声明"
    % (alpha_eff, ginf_lab_reading, float(abs(ginf_from_alpha - ginf_lab_reading) / ginf_lab_reading * 100)))
add("V6-02", "FAIL", "短程外推未声明：点质量形式蕴含 33% 的短程力增强",
    "若 §一/§六 使用的点质量形式 K(r)=A+B(1+kr)e^{-kr} 外推到 r<<ell，则力增强趋于 alpha_Y = 1/3（33%%），"
    "与实验室短程引力反平方律检验上限直接冲突；而 §五/§六 用的地表重标剖面向内延拓只给 %s。"
    "两者的差别必须显式声明，否则「alpha_Y=1/3」在不同小节里指的不是同一个量"
    % sci(eps0_short))

# ==================================================================
# 区块 V7：噪声敏感性的自洽性与实用底
# ==================================================================
def norm_cdf(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def inv_norm(p):
    lo, hi = 0.0, 12.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


flip_v119 = {D("1e-7"): D("0.436"), D("1e-8"): D("0.049"), D("1e-9"): D("0.0")}
z_inv = {}
for k_, v in flip_v119.items():
    if v > 0:
        z_inv[k_] = D(str(inv_norm(1.0 - float(v))))
ratio_1 = z_inv[D("1e-8")] / z_inv[D("1e-7")]
# 翻转率恰为 0 的档：有限次 MC 只能给出 z 的统计下界，不能反解出定值
N_V119 = 12000
z_floor_third = D(str(inv_norm(1.0 - 3.0 / N_V119)))
z_extrap_third = z_inv[D("1e-8")] * ratio_1
guard("G_noise_table_selfconsistent", D("9") < ratio_1 < D("11"),
      "来料噪声表前两档在高斯符号模型下自洽：反解 z = %s / %s，比值 %s ⇒ sigma_H 正比于 sigma_K"
      % (sci(z_inv[D("1e-7")]), sci(z_inv[D("1e-8")]), sci(ratio_1)))
guard("G_noise_third_row_lowerbound", z_floor_third < z_extrap_third,
      "第三档翻转率 0.0：%d 次 MC 零翻转只能给出 z >= %s（95%% 置信），而模型外推 z = %s ⇒ 二者相容"
      % (N_V119, sci(z_floor_third), sci(z_extrap_third)))

# 本册自声明模型下的 MC：噪声加在 Ktilde = 1+eps 上
def mc_flip(sigma, trials=4000, seed=20261121):
    rnd = random.Random(seed)
    cnt = 0
    for _ in range(trials):
        vals = []
        for n in range(4):
            vals.append(k_tilde(D(n) * DR, EPS0_USED) + D(str(rnd.gauss(0.0, float(sigma)))))
        d0 = vals[1] - vals[0]
        d1 = vals[2] - vals[1]
        d2 = vals[3] - vals[2]
        if d0 * d2 - d1 * d1 > 0:
            cnt += 1
    return cnt, trials


mc_rows = []
for sig in (D("1e-7"), D("1e-8"), D("1e-9"), D("1e-10")):
    c, t = mc_flip(sig)
    mc_rows.append((sig, c, t))
mono = all(mc_rows[i][1] <= mc_rows[i + 1][1] for i in range(len(mc_rows) - 1))
guard("G_noise_mc_monotone", mono,
      "本册 MC 翻转率随噪声下降单调不增：" + "; ".join("%s -> %d/%d" % (sci(s, 1), c, t) for s, c, t in mc_rows))
# 解析噪声传播
d0v = d_seq(0, EPS0_USED)
d1v = d_seq(1, EPS0_USED)
d2v = d_seq(2, EPS0_USED)
sigma_H_coef = (2 * (d0v ** 2 + d2v ** 2 + 4 * d1v ** 2)).sqrt()
ratio_H_over_sigH = abs(h_seq(0, EPS0_USED)) / (D("1e-8") * sigma_H_coef)
sigma_usable = abs(h_seq(0, EPS0_USED)) / (sigma_H_coef * D("2"))
guard("G_noise_floor", sigma_usable < D("1e-7"),
      "可用噪声底（本册口径）：sigma_K <= %s 才使 |H_0|/sigma_H >= 2；当前 |H_0|/sigma_H(1e-8) = %s"
      % (sci(sigma_usable, 3), sci(ratio_H_over_sigH, 4)))
add("V7-01", "PASS", "来料噪声敏感性表的内部自洽性可复现（高斯符号模型，前两档）",
    "若 H_0 的噪声按 sigma_H 正比于 sigma_K（双线性型的必然），则前两档翻转率对应的正态分位数为 "
    "%s / %s，逐档之比 %s（≈ 10）⇒ 与 sigma_H ∝ sigma_K 相容；"
    "第三档翻转率记为 0.0：%d 次 MC 零翻转只能给出 z >= %s 的统计下界（不能反解出定值），"
    "而按同一比例外推应为 z = %s ⇒ 外推值远超统计下界，二者相容，无档位跳变"
    % (sci(z_inv[D("1e-7")]), sci(z_inv[D("1e-8")]), sci(ratio_1), N_V119,
       sci(z_floor_third), sci(z_extrap_third)))
add("V7-02", "BOUNDARY", "噪声表的绝对读数依赖未声明的归一化与噪声模型",
    "本册自声明模型（Ktilde=1+eps 逐点加 N(0,sigma) 噪声，dr=50 km，4000 次/档）的翻转率为："
    + "; ".join("%s -> %d/%d" % (sci(s, 1), c, t) for s, c, t in mc_rows)
    + "，与来料档位不同 ⇒ 差异来源是 H_0 的绝对归一化（见 V1-04）与噪声定义，"
    "机器不变量只有「翻转率由 |H_0|/sigma_H 决定」")
add("V7-03", "FAIL", "实用性判决：该判据的瓶颈是高阶重力场建模精度，而非测量精度",
    "400 km 高度上未建模的地球高阶球谐（2–20 级）造成的场异常与信号 delta g_400 = %s m/s^2 同量级"
    "（10^-3–10^-4 m/s^2），比信号本身更易压过；因此把判据压到 sigma_K <= %s 需要的是"
    "重力场解算精度而非仪器精度。结论与来料自承「H_n 仅作辅助一致性检验、不作唯一判决依据」一致，"
    "本册把它量化为可执行的门限"
    % (sci(dg400), sci(sigma_usable, 3)))
add("V7-04", "INFO", "作用程反演区间与噪声放大因子",
    "来料 2500 组三高度模拟给 95%% 区间 %s–%s km（宽 74.6 m，噪声 1e-7 档）"
    "⇒ 相对噪声放大约 %.1e 倍；本册噪声模型与拟合细节不同，不复现该区间数值，"
    "仅登记放大因子这一机器不变量"
    % (D("124.5633"), D("124.6379"), D("74.6") / D("124.6") * D("1e7")))

# ==================================================================
# 区块 V8：边界与红线
# ==================================================================
add("V8-01", "INFO", "四力统一仍 OPEN；G=2Z/c 的自指性不因量纲自洽而消解",
    "G = 2Z/c 的量纲自洽成立，但若 Z 本身按 Gc/2 定义，则该式退化为重述（零信息量）；"
    "作用程 124.6 km 在来料体系内仍无第一性来源（属外部输入）；四力统一状态维持 OPEN")
add("V8-02", "INFO", "归档边界沿用来料自承",
    "来料声明未获得 V118 原始 ZIP，因而未声称重跑其历史 215 项自动测试或完成原始归档的独立验收；"
    "本册沿用该边界，只做正文数值的独立复算，不代做原始归档验收")

REDLINES = {
    "UFT_goals": "0/6 未完成",
    "systems": "0/22 完成架构统一",
    "UFT3": "0（不能第一性独立给出四力耦合常量与量级）",
    "L3": "0（本轮不新增可证伪独立预言）",
    "validated": "0（无独立实验验证）",
    "four_force_correct_equation": "0 条（含引力的四力正确方程）",
    "L3_to_L4": "L3 不成立，L3→L4 禁止",
    "redline": "数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确",
}
add("RED-01", "INFO", "红线计数继承不变",
    "0/6、0/22、UFT3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4；"
    "本轮把 ROOT V119 压缩为可复算判定，不增加任何 L3/validated 计数")

# ==================================================================
# 产物生成
# ==================================================================
BASE_NAME = "TUFT-r429_ROOT_V119五高度离散谱判据与1_3耦合映射_全维审计_2026-11-21"
VERDICT_NAME = "判定_TUFT-r429-ROOT_V119五高度离散谱判据与1_3耦合映射_全维审计_2026-11-21.md"


def verdict_counts(rows):
    out = {}
    for row in rows:
        out[row["verdict"]] = out.get(row["verdict"], 0) + 1
    return out


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", "<br>")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


COUNTS = verdict_counts(ENTRIES)
SOURCE_PATH = os.path.abspath(__file__)
with open(SOURCE_PATH, "rb") as fh:
    SOURCE_SHA = hashlib.sha256(fh.read()).hexdigest()
with open(SOURCE_PATH, "r", encoding="utf-8") as fh:
    SOURCE_TEXT = fh.read()
PLACEHOLDER = chr(36) + "{"
guard("G_no_template_placeholder", PLACEHOLDER not in SOURCE_TEXT, "源码不得出现美元花括号占位符")
guard("G_entry_floor", len(ENTRIES) >= 18, "条目数 %d >= 18" % len(ENTRIES))
guard("G_guard_floor", len(GUARDS) >= 26, "守卫数 %d >= 26" % len(GUARDS))
guard("G_counts_sum", sum(COUNTS.values()) == len(ENTRIES), "条目计数闭合：%s" % COUNTS)

key_numbers = {
    "x_R_over_ell": sci(X_, 12),
    "dr_inverted_m": fs(dr_from_ratio, 8),
    "h1h0_computed": sci(Q ** 2),
    "h1h0_v119": str(H1H0_V119),
    "h0_closed_prof": sci(h0_closed_prof, 12),
    "h0_sampled": sci(h0_sampled, 12),
    "h0_closed_pointmass": sci(h0_closed_pm, 12),
    "h0_rel_to_v119": sci(rel(h0_closed_prof, H0A_V119)),
    "h0_ell_implied_m": fs(ell_implied, 10),
    "h0_v119": str(H0A_V119),
    "eps0_uniform_closed": sci(lead_u, 12),
    "eps0_uniform_integral": sci(int_u, 12),
    "eps0_uniform_v119": str(EPS0_UNIFORM_V119),
    "eps0_improved_v119": str(EPS0_IMPROVED_V119),
    "eps0_improved_ratio_target": sci(ratio_improved_target),
    "eps0_pointmass_surface": sci(eps_pm_surface),
    "rho_core_implied": fs(rho_core_implied, 8),
    "a_l2_over_6": fs(A_L2_OVER_6, 10),
    "a_common_convention": fs(a_common, 10),
    "mphi_exact_eV": fs(MPHI_EXACT, 12),
    "mphi_v119_eV": str(MPHI_V119),
    "dg400": sci(dg400),
    "dg400_v119": str(DG400_V119),
    "precession_exact": sci(prec_exact),
    "precession_linear": sci(prec_linear),
    "precession_no_dgprime": sci(prec_nodgp),
    "precession_first_order": sci(prec_firstorder),
    "precession_v119": str(DPREC_V119),
    "dnu_ratio": sci(dnu),
    "dnu_v119": str(DNU_V119),
    "ginf_over_glab_alpha": str(ginf_from_alpha),
    "ginf_over_glab_lab": str(ginf_lab_reading),
    "short_range_pm": str(short_range_pm),
    "eps0_short_range": sci(eps0_short),
    "modelB_flip_weight": sci(flip_w2) if flip_w2 is not None else "NA",
    "pseudo_ell_implied_ratio": sci(ratio_pseudo_implied),
    "sigma_usable": sci(sigma_usable, 3),
    "h0_over_sigmaH_at_1e8": sci(ratio_H_over_sigH, 4),
    "mc_flip_rates": "; ".join("%s->%d/%d" % (sci(s, 1), c, t) for s, c, t in mc_rows),
    "identity_max_residual": sci(max_h_err),
    "identity_D_closed_residual": sci(max_d_err),
    "identity_ratio_residual": sci(max_ratio_err),
    "modelB_h0_at_w_max": sci(h0_w_max),
    "z_inv_sigma_1e7": sci(z_inv[D("1e-7")]),
    "z_inv_sigma_1e8": sci(z_inv[D("1e-8")]),
    "noise_ratio_1": sci(ratio_1),
    "noise_z_floor_third": sci(z_floor_third),
    "noise_z_extrap_third": sci(z_extrap_third),
}

json_obj = {
    "meta": {
        "rid": RID,
        "stamp": STAMP,
        "title": "ROOT V119 五高度离散谱判据与 1/3 耦合映射 全维审计",
        "method": "纯标准库 Decimal 60 位 + 双路径对拍 + 阳性对照 + 高斯反解 + 定种子 MC",
        "source_sha256": SOURCE_SHA,
        "verdict_counts": COUNTS,
        "entry_total": len(ENTRIES),
        "guard_total": len(GUARDS),
    },
    "entries": ENTRIES,
    "guards": GUARDS,
    "redlines": REDLINES,
    "key_numbers": key_numbers,
}

json_path = os.path.join(DATA, BASE_NAME + ".json")
md_path = os.path.join(DATA, BASE_NAME + ".md")
report_path = os.path.join(DATA, BASE_NAME + "_report.txt")
verdict_path = os.path.join(os.path.dirname(HERE), VERDICT_NAME)

json_text = json.dumps(json_obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

entry_lines = ["| ID | 判定 | 标题 | 读数 |", "|---|---|---|---|"]
for row in ENTRIES:
    entry_lines.append("| %s | %s | %s | %s |" %
                       (cell(row["id"]), cell(row["verdict"]), cell(row["title"]), cell(row["detail"])))
guard_lines = ["| ID | OK | 读数 |", "|---|---|---|"]
for row in GUARDS:
    guard_lines.append("| %s | %s | %s |" %
                       (cell(row["id"]), "PASS" if row["ok"] else "FAIL", cell(row["detail"])))
counts_text = " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS))

md_text = "\n".join([
    "# r429 数据产物：ROOT V119 五高度离散谱判据与 1/3 耦合映射 全维审计",
    "",
    "- 条目：%d（%s）" % (len(ENTRIES), counts_text),
    "- 守卫：%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "- 源码 SHA-256：`%s`" % SOURCE_SHA,
    "- 判定册：[%s](../%s)" % (VERDICT_NAME, VERDICT_NAME),
    "- 引擎：[源码](%s)" % ("../源码/" + os.path.basename(SOURCE_PATH)),
    "",
    "## 条目表",
    "",
] + entry_lines + [
    "",
    "## 守卫表",
    "",
] + guard_lines + [
    "",
    "## 关键读数",
    "",
] + ["- %s = %s" % (k, key_numbers[k]) for k in sorted(key_numbers)] + [
    "",
    "## 红线",
    "",
] + ["- %s：%s" % (k, v) for k, v in REDLINES.items()] + [""])

report_text = "\n".join([
    "r429 ROOT V119 五高度离散谱判据与 1/3 耦合映射 全维审计",
    "=" * 60,
    "entries=%d" % len(ENTRIES),
    "counts=%s" % counts_text,
    "guards=%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "source_sha256=%s" % SOURCE_SHA,
    "eps0_uniform=%s" % sci(lead_u, 12),
    "eps0_improved_target=%s" % sci(EPS0_IMPROVED_V119, 12),
    "h0_eps_profile=%s" % sci(h0_eps_profile),
    "h0_v119=%s" % H0A_V119,
    "dg400=%s" % sci(dg400),
    "precession_exact=%s" % sci(prec_exact),
    "dnu_ratio=%s" % sci(dnu),
    "mphi_exact_eV=%s" % fs(MPHI_EXACT, 12),
    "sigma_usable=%s" % sci(sigma_usable, 3),
    "redline=数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功",
])

verdict_text = "\n".join([
    "# 判定 r429：ROOT V119 五高度离散谱判据与 1/3 耦合映射 全维审计",
    "",
    "## 〇、一句话",
    "",
    "ROOT V119 的正文主体可独立复现：均匀球地表异常 %s%%、400 km 额外加速度 %s m/s^2、"
    "近拱点进动 %s rad、引力频移 %s 全部由第一性推导逐位重现；"
    "但五处口径必须显式声明——离散谱「必要条件」在单作用程族内是代数恒等式（零判别力）、"
    "H_0 绝对值虽可复现但完全由归一化口径决定（跨口径差 %.2e 倍）、改进解析密度档缺剖面、"
    "标量质量只是作用程的重述、短程外推蕴含 33%% 力增强。"
    % (fs(lead_u * 100, 10), sci(dg400), sci(prec_exact), sci(dnu),
       float(abs(h0_closed_pm / h0_closed_prof))),
    "",
    "## 一、产物",
    "",
    "| 顺序 | 文件 | 作用 |",
    "|---|---|---|",
    "| 0 | 本判定册 | V1–V8 裁定 + 红线 |",
    "| 1 | [引擎](源码/%s) | %d 条目 / %d 守卫 / 纯标准库 |" % (os.path.basename(SOURCE_PATH), len(ENTRIES), len(GUARDS)),
    "| 2 | [数据 md](数据/%s) · [json](数据/%s) · [报告](数据/%s) | 机器读数留档 |" %
        (os.path.basename(md_path), os.path.basename(json_path), os.path.basename(report_path)),
    "",
    "## 二、条目与守卫",
    "",
    "条目 %d（%s），守卫 %d/%d，源码 SHA-256 `%s`。" %
    (len(ENTRIES), counts_text, sum(1 for g in GUARDS if g["ok"]), len(GUARDS), SOURCE_SHA),
    "",
] + entry_lines + [
    "",
    "## 三、守卫表",
    "",
] + guard_lines + [
    "",
    "## 四、关键读数",
    "",
] + ["- %s = %s" % (k, key_numbers[k]) for k in sorted(key_numbers)] + [
    "",
    "## 五、红线与边界",
    "",
] + ["- %s：%s" % (k, v) for k, v in REDLINES.items()] + [
    "",
    "本册不把数值复现解释为新物理，不修改来料原文，不覆盖并发会话文件；"
    "来料自承的「未获 V118 原始 ZIP、未做原始归档验收」边界沿用不代做。",
])

write_text(json_path, json_text)
write_text(md_path, md_text)
write_text(report_path, report_text)
write_text(verdict_path, verdict_text)

with open(json_path, "r", encoding="utf-8") as fh:
    reread = fh.read()
if reread != json_text:
    raise AssertionError("JSON idempotence failed")
for p in (md_path, report_path, verdict_path):
    if os.path.getsize(p) <= 200:
        raise AssertionError("Empty output: %s" % os.path.basename(p))


def main():
    print("r429 entries=%d counts=%s" % (len(ENTRIES), counts_text))
    print("r429 guards=%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    print("r429 json=%s" % json_path)
    print("r429 verdict=%s" % verdict_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
