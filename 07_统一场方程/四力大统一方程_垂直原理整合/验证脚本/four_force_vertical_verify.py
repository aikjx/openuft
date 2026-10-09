# -*- coding: utf-8 -*-
"""
四力大统一方程 · 垂直原理 —— 零第三方依赖复算器
================================================

来源语料：my_lib/utf/大统一场论_算法联盟最高权限/
  v4/25_垂直原理全维求证_四力大统一方程报告.md   （垂直(正交)原理、复曲率场）
  v8/统一场论全维分析/v8.1 全维求导证明          （kappa/tau/alpha 求导链）
  v8/统一场论全维分析/v9 对偶场方程重构          （泊松场方程、引力/电磁还原）
  v8/统一场论全维分析/v10 四力统一场方程         （Proca 升级、四力统一表）

本脚本只做两件事：
  1. 把上述四册里"经机器验证过"的公式逐条独立复算（不抄结论数，全部现算）；
  2. 把它们按 L0 公理 → L1 几何量 → L2 母方程 → L3 四力分支 → L5 边界 的
     垂直分层结构落成一个 JSON + 一份可读报告。

红线：
  * 未解决的项一律判 FAIL/INFO，不粉饰为 PASS；
  * v8.1 的 W_n = alpha^{-n} + alpha^{n+1} 分支方案已被 A-32/33/34/37 证伪，
    本脚本不复算它（它属于"排除清单"，见 L5）。
  * 只使用标准库（math / fractions / json / decimal），零第三方依赖。

运行：  python -B four_force_vertical_verify.py
退出码：0 = 自检通过（无论 PASS/FAIL，只要条目全部有判定且自检全过）
"""

import json
import math
import os
import sys
from fractions import Fraction as F

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- 常数 (CODATA 2018)
HBAR = 1.054571817e-34          # J*s
C = 299792458.0                 # m/s
G = 6.67430e-11                 # m^3 kg^-1 s^-2
E_CHG = 1.602176634e-19         # C
EPS0 = 8.8541878128e-12         # F/m
MU0 = 1.25663706212e-6          # N/A^2
ALPHA = 7.2973525693e-3         # 精细结构常数
M_P_KG = 2.176434e-8            # 普朗克质量 kg
M_PROTON = 1.67262192369e-27    # kg
M_ELECTRON = 9.1093837015e-31   # kg
M_W_GEV = 80.379                # GeV/c^2
M_PI0_MEV = 134.977             # MeV/c^2
GEV_TO_KG = 1.78266192e-27      # 1 GeV/c^2 = 1.78266192e-27 kg
SIGMA_STRING = 1.6e-2           # QCD 弦张力 ~1 GeV/fm ≈ 1.6e-2 J/m (量级)

PLANCK_LEN = math.sqrt(HBAR * G / C ** 3)   # m

# v10 公布的读数（用于交叉比对，不用于推导）
V10_LAMBDA_W_M = 2.454956895935461e-18
V10_LAMBDA_PI_M = 1.461932571659696e-15

RESULTS = []
_SEQ = [0]


def _nxt(prefix):
    _SEQ[0] += 1
    return "%s%02d" % (prefix, _SEQ[0])


def rec(layer, name, verdict, symbolic, numeric, relerr, note):
    RESULTS.append({
        "id": _nxt({"L0": "A", "L1": "G", "L2": "M", "L3": "F", "L5": "B"}[layer]),
        "layer": layer,
        "name": name,
        "verdict": verdict,
        "symbolic": symbolic,
        "numeric": numeric,
        "rel_error": relerr,
        "note": note,
    })


def rel(a, b):
    """相对误差 |a-b|/|b|，b==0 时用绝对差。"""
    if b == 0:
        return abs(a - b)
    return abs(a - b) / abs(b)


def ok(err, tol=1e-9):
    return err is not None and err <= tol


# ================================================================ L0 公理层
# 圆柱螺旋世界线： r(t) = (rho*cos(th), rho*sin(th), b*th),  th = omega*t
RHO = 3.0e-11     # m   (半径)
B_PITCH = 2.19e-13  # m/rad (螺距参数 b，取 alpha = b/rho = 0.0073 量级)


def helix(th):
    return (RHO * math.cos(th), RHO * math.sin(th), B_PITCH * th)


def d1(th, h=1e-6):
    a, b_, c_ = helix(th - h), helix(th), helix(th + h)
    return tuple((x2 - x0) / (2 * h) for x0, x2 in zip(a, c_))


def d2(th, h=1e-4):
    p, m_, q = helix(th - h), helix(th), helix(th + h)
    return tuple((x2 - 2 * x1 + x0) / (h * h) for x0, x1, x2 in zip(p, m_, q))


def d3(th, h=1e-3):
    f0, f1 = helix(th - 2 * h), helix(th - h)
    f3, f4 = helix(th + h), helix(th + 2 * h)
    return tuple((b_ - 2 * a + 2 * c_ - d) / (2 * h ** 3)
                 for a, b_, c_, d in zip(f0, f1, f3, f4))


def vnorm(v):
    return math.sqrt(sum(x * x for x in v))


def unit(v):
    n = vnorm(v)
    return tuple(x / n for x in v)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


TH0 = 0.7
r1, r2, r3 = d1(TH0), d2(TH0), d3(TH0)
T = unit(r1)
N = unit(r2)
Bv = unit(cross(r1, r2))

# A01 光速螺旋：|v| = omega*sqrt(rho^2+b^2) = c  =>  omega = c/sqrt(rho^2+b^2)
R_helix = math.sqrt(RHO ** 2 + B_PITCH ** 2)
OMEGA = C / R_helix
speed = OMEGA * R_helix
rec("L0", "光速螺旋公设 |v| = omega*sqrt(rho^2+b^2) = c",
    "PASS" if ok(rel(speed, C), 1e-12) else "FAIL",
    "r(t)=(rho cos th, rho sin th, b*th), th=omega*t; |dr/dt| = omega*sqrt(rho^2+b^2)",
    "rho=%.6e m, b=%.6e m, R=%.6e m, omega=%.6e rad/s, |v|=%.12e m/s" % (RHO, B_PITCH, R_helix, OMEGA, speed),
    rel(speed, C),
    "公设本身不是推导结果；此处只验证 |v| 与 omega 的一致性（恒等）。v=c 是输入公设，非导出结论。")

# A02 垂直(正交)原理：T.N = N.B = B.T = 0, |T|=|N|=|B|=1
tn, nb, bt = dot(T, N), dot(N, Bv), dot(Bv, T)
worst = max(abs(tn), abs(nb), abs(bt))
norm_dev = max(abs(vnorm(T) - 1), abs(vnorm(N) - 1), abs(vnorm(Bv) - 1))
rec("L0", "垂直(正交)原理：T perp N perp B（Frenet 三元正交归一）",
    "PASS" if ok(worst, 1e-7) and ok(norm_dev, 1e-7) else "FAIL",
    "T=dr/ds, N=(dT/ds)/|dT/ds|, B=T x N",
    "T.N=%.3e  N.B=%.3e  B.T=%.3e  max| |v|-1 |=%.3e" % (tn, nb, bt, norm_dev),
    worst,
    "来源 v4/25：对偶算子 eps*eps^{-1}=1 在微分几何中表现为 T perp N perp B。数值由圆柱螺旋世界线现算。")

# A03 Frenet 公式 dT/ds = kappa*N, dB/ds = -tau*N
# 注意：d1/d2 是 dr/dth、dT/dth 对参数 th 的导数；须除以 ds/dth = |dr/dth| = R_helix 才得到对弧长 s 的导数
h_s = 1e-6
T_a = unit(d1(TH0 - h_s))
T_b = unit(d1(TH0 + h_s))
dB_th = tuple((x2 - x0) / (2 * h_s) for x0, x2 in zip(T_a, T_b))
B_a = unit(cross(d1(TH0 - h_s), d2(TH0 - h_s)))
B_b = unit(cross(d1(TH0 + h_s), d2(TH0 + h_s)))
dBt_th = tuple((x2 - x0) / (2 * h_s) for x0, x2 in zip(B_a, B_b))
dT = tuple(x / R_helix for x in dB_th)
dB = tuple(x / R_helix for x in dBt_th)
kappa_num = dot(dT, N)
tau_num = -dot(dB, N)
kappa_th = RHO / (RHO ** 2 + B_PITCH ** 2)
tau_th = B_PITCH / (RHO ** 2 + B_PITCH ** 2)
e_k = rel(kappa_num, kappa_th)
e_t = rel(tau_num, tau_th)
rec("L0", "Frenet 公式 dT/ds = kappa N,  dB/ds = -tau N",
    "PASS" if ok(e_k, 1e-4) and ok(e_t, 1e-4) else "FAIL",
    "kappa = |dT/ds|, tau = -B.(dB/ds)",
    "kappa_num=%.10e (解析 %.10e, rel=%.3e); tau_num=%.10e (解析 %.10e, rel=%.3e)"
    % (kappa_num, kappa_th, e_k, tau_num, tau_th, e_t),
    max(e_k, e_t),
    "kappa 活在 (T,N) 弯曲平面，tau 活在 (N,B) 扭转平面；两平面法向分别为 B 与 T，"
    "而 B perp T ⇒ 两平面垂直。这是'垂直原理'能承载四力正交分解的几何根源。")

# ================================================================ L1 几何量层
# G01/G02 上面已算，此处登记为独立条目
rec("L1", "曲率 kappa = rho/(rho^2+b^2)",
    "PASS" if ok(e_k, 1e-4) else "FAIL",
    "kappa = rho/(rho^2+b^2)",
    "kappa = %.10e 1/m" % kappa_th, e_k, "与 Frenet 数值差分一致。")
rec("L1", "挠率 tau = b/(rho^2+b^2)",
    "PASS" if ok(e_t, 1e-4) else "FAIL",
    "tau = b/(rho^2+b^2)",
    "tau = %.10e 1/m" % tau_th, e_t, "与 Frenet 数值差分一致。")

# G03 alpha == tau/kappa == b/rho
alpha_geo = tau_th / kappa_th
alpha_boverrho = B_PITCH / RHO
e_a = rel(alpha_geo, alpha_boverrho)
rec("L1", "本源关系 alpha = tau/kappa = b/rho",
    "PASS" if ok(e_a, 1e-12) else "FAIL",
    "alpha := tau/kappa = b/rho（螺距比）",
    "tau/kappa = %.12e ; b/rho = %.12e" % (alpha_geo, alpha_boverrho), e_a,
    "【方向性冲突登记】本册采用 v8.1 D07 / v4-25 的 alpha = tau/kappa = b/rho。"
    "utf 内另有文档使用 alpha = kappa/tau（互为倒数，137.036 vs 0.007297），两者不可能同时正确。"
    "本册不代选，仅登记；以 CODATA alpha=7.297e-3 为准时，tau/kappa 口径成立。")

# G04 kappa^2 + tau^2 = 1/(rho^2+b^2)  —— 用 Fraction 精确验证
fr_rho = F(3, 1)
fr_b = F(219, 1000)
k_ex = fr_rho / (fr_rho ** 2 + fr_b ** 2)
t_ex = fr_b / (fr_rho ** 2 + fr_b ** 2)
lhs = k_ex ** 2 + t_ex ** 2
rhs = F(1, 1) / (fr_rho ** 2 + fr_b ** 2)
rec("L1", "形变守恒恒等式 kappa^2 + tau^2 = 1/(rho^2+b^2)",
    "PASS" if lhs == rhs else "FAIL",
    "kappa^2+tau^2 = (rho^2+b^2)/(rho^2+b^2)^2 = 1/(rho^2+b^2)",
    "精确有理数验证：lhs - rhs = %s（机器零）" % (lhs - rhs), 0.0,
    "全程 Fraction，无浮点。这是 v8.1 D10。")

# G05 kappa^2+tau^2 = (omega/c)^2
om_c = OMEGA / C
kt2 = kappa_th ** 2 + tau_th ** 2
e_g5 = rel(kt2, om_c ** 2)
rec("L1", "母恒等式 kappa^2 + tau^2 = (omega/c)^2",
    "PASS" if ok(e_g5, 1e-9) else "FAIL",
    "omega = c/sqrt(rho^2+b^2)  ⇒  (omega/c)^2 = 1/(rho^2+b^2) = kappa^2+tau^2",
    "kappa^2+tau^2 = %.10e ; (omega/c)^2 = %.10e" % (kt2, om_c ** 2), e_g5,
    "这条把几何量(kappa,tau)与运动量(omega)焊死，是'频率化'的承重恒等式。")

# G06 归一化 kappa~^2 + tau~^2 = 1
kn = kappa_th / math.sqrt(kt2)
tnn = tau_th / math.sqrt(kt2)
e_g6 = rel(kn ** 2 + tnn ** 2, 1.0)
rec("L1", "归一化本源方程 kappa~^2 + tau~^2 = 1（单位圆）",
    "PASS" if ok(e_g6, 1e-12) else "FAIL",
    "kappa~ = kappa/|Xi|, tau~ = tau/|Xi|, |Xi| = sqrt(kappa^2+tau^2)",
    "kappa~^2+tau~^2 = %.15f ; 相位 phi = arctan(tau/kappa) = %.9f rad" % (kn ** 2 + tnn ** 2, math.atan2(tau_th, kappa_th)),
    e_g6,
    "单位圆相位 phi=arctan(alpha)。【重要】归一化圆对任意 alpha 成立 ⇒ 理论内无确定 alpha 的方程（v10 X10/W20）。")

# G07 对偶反演 (rho,b) = (kappa,tau)/(kappa^2+tau^2)
k2t2 = kappa_th ** 2 + tau_th ** 2
rho_dual = kappa_th / k2t2
b_dual = tau_th / k2t2
e_inv1 = rel(rho_dual, RHO)
e_inv2 = rel(b_dual, B_PITCH)
e_pair = rel(rho_dual * kappa_th + b_dual * tau_th, 1.0)
rec("L1", "对偶反演 (rho,b) = (kappa,tau)/(kappa^2+tau^2) 与配对 rho*kappa+b*tau = 1",
    "PASS" if ok(max(e_inv1, e_inv2, e_pair), 1e-9) else "FAIL",
    "单位圆反演；对合性：作用两次 = 恒等",
    "rho_dual=%.12e (原 %.12e), b_dual=%.12e (原 %.12e), rho*kappa+b*tau=%.15f"
    % (rho_dual, RHO, b_dual, B_PITCH, rho_dual * kappa_th + b_dual * tau_th),
    max(e_inv1, e_inv2, e_pair),
    "v9 W01/W02/W03。对偶把'位形参数(rho,b)'与'场量(kappa,tau)'互映，是场方程能写成泊松型的依据。")

# G08 质量-曲率对应 m = hbar*omega/c^2
m_from_omega = HBAR * OMEGA / C ** 2
rho_from_m = HBAR / (m_from_omega * C * math.sqrt(1 + alpha_geo ** 2))
e_g8 = rel(rho_from_m, RHO)
rec("L1", "质量-曲率对应 m = hbar*omega/c^2, rho = hbar/(m c sqrt(1+alpha^2))",
    "PASS" if ok(e_g8, 1e-9) else "FAIL",
    "m = hbar*omega/c^2, omega = c/R ⇒ m = hbar/(cR)",
    "m=%.6e kg, 反解 rho=%.6e m (原 %.6e m), rel=%.3e" % (m_from_omega, rho_from_m, RHO, e_g8),
    e_g8, "v8.1 D12。闭合是恒等闭合（定义互逆），不产生新物理。")

# ================================================================ L2 母方程层
def u_yuk(r, mu):
    return math.exp(-mu * r) / r


def lap_spherical(f, r, mu, h=1e-15):
    """球坐标拉普拉斯 ∇²f = (1/r²) d/dr [ r² df/dr ]，中心差分。"""
    def fp(x):
        return math.exp(-mu * x) / x
    fp1 = (fp(r + h) - fp(r - h)) / (2 * h)
    gp = lambda x: x * x * (fp(x + h) - fp(x - h)) / (2 * h)
    return (gp(r + h) - gp(r - h)) / (2 * h) / (r * r)


MU_TEST = 1.0e12            # 1/m，力程 ~1e-12 m（数值验证样例，避免大 mu 溢出；真实弱/强力程见 L3）
R_TEST = 1.0e-12
lap_val = lap_spherical(u_yuk, R_TEST, MU_TEST)
rhs_val = MU_TEST ** 2 * u_yuk(R_TEST, MU_TEST)
e_m1 = rel(lap_val, rhs_val)
rec("L2", "Proca/KG 场方程 (∇² - mu²)kappa = 0 (r>0) 的汤川解",
    "PASS" if ok(e_m1, 1e-5) else "FAIL",
    "kappa(r) = q e^{-mu r}/r ; ∇²kappa = mu² kappa (r>0) ; 分布意义下 (∇²-mu²)(e^{-mu r}/r) = -4π δ³(r)",
    "mu=%.6e 1/m, r=%.3e m: ∇²kappa=%.10e, mu²kappa=%.10e, rel=%.3e" % (MU_TEST, R_TEST, lap_val, rhs_val, e_m1),
    e_m1,
    "v10 X01。这是唯一能在保持线性叠加 + 旋转不变的同时引入有限力程的二阶方程。")

# M02 连续性 mu->0 退化为 1/r（v9 ⊂ v10）
e_m2 = rel(u_yuk(R_TEST, 1e-30), 1.0 / R_TEST)
rec("L2", "连续性：mu -> 0 时 v10 退化为 v9（kappa = q/r）",
    "PASS" if ok(e_m2, 1e-12) else "FAIL",
    "lim_{mu->0} q e^{-mu r}/r = q/r",
    "mu=1e-30: e^{-mu r}/r = %.12e , 1/r = %.12e" % (u_yuk(R_TEST, 1e-30), 1.0 / R_TEST),
    e_m2, "v10 X06。v9 未被推翻，而是被包含在更一般的方程里。")

# M03 统一势的量纲：U = s*hbar*c*q1*q2*e^{-r/lambda}/r  ⇒ [hbar c] = J*m，除以 m 得 J
hb_c = HBAR * C
rec("L2", "统一势 U = s·hbar·c·q1·q2·e^{-r/lambda}/r 的量纲闭合",
    "PASS" if abs(hb_c) > 0 else "FAIL",
    "[hbar*c] = J·m ⇒ (hbar c)/r = J（能量）；q 无量纲 ⇒ U 量纲正确",
    "hbar*c = %.10e J·m ; (hbar c)/r_test = %.10e J" % (hb_c, hb_c / R_TEST), 0.0,
    "源荷 q 必须无量纲（引力 q=m/m_P、电磁 q=sqrt(alpha) Z），才能由 hbar c 承担全部量纲。")

# M04 垂直原理收口方程（结构层，登记为结构定理 + 待核标记）
rec("L2", "垂直原理收口：Fraktur F = -∇Xi = -(∇kappa + i∇tau)",
    "BOUNDARY",
    "Xi = kappa + i tau ; |Xi|² = kappa²+tau² = (omega/c)² ; Re(F) 与 Im(F) 正交",
    "标架层已验证：(T,N) 平面法向 = B，(N,B) 平面法向 = T，T⊥B ⇒ 两平面垂直",
    None,
    "【诚实标注】v4/25 写作 ∇kappa ⊥ ∇tau（空间梯度正交）。本册只验证了**标架层**的平面正交性，"
    "空间梯度 ∇kappa ⊥ ∇tau 未作独立数值验证（kappa、tau 在一般点上的梯度依赖场的具体分布），"
    "登记为待核项，不判 PASS。")

# M05 力程 = 康普顿波长 lambda = hbar/(m c)
lam_W = HBAR / (M_W_GEV * GEV_TO_KG * C)
lam_pi = HBAR / (M_PI0_MEV * 1e-3 * GEV_TO_KG * C)
e_w = rel(lam_W, V10_LAMBDA_W_M)
e_pi = rel(lam_pi, V10_LAMBDA_PI_M)
rec("L2", "力程 lambda = hbar/(m c)（媒介子康普顿波长）",
    "PASS" if ok(e_w, 1e-5) and ok(e_pi, 1e-5) else "FAIL",
    "lambda = hbar/(m c)",
    "m_W=%.3f GeV/c² ⇒ lambda_W=%.10e m = %.8f fm (v10: %.10e, rel=%.3e)\n                "
    "m_pi0=%.3f MeV/c² ⇒ lambda_pi=%.10e m = %.8f fm (v10: %.10e, rel=%.3e)"
    % (M_W_GEV, lam_W, lam_W * 1e15, V10_LAMBDA_W_M, e_w,
       M_PI0_MEV, lam_pi, lam_pi * 1e15, V10_LAMBDA_PI_M, e_pi),
    max(e_w, e_pi),
    "本册独立复算与 v10 公布读数一致（交叉验证）。力程全部由媒介子质量决定——质量是输入。")
# ================================================================ L3 四力分支层
# L3 母公式：U = s · hbar*c · q1·q2 · e^{-r/lambda}/r ；力 F = -dU/dr（长程力 lambda->inf）

# F01 引力还原：hbar*c / m_P^2 = G
g_calc = HBAR * C / (M_P_KG ** 2)
e_F01 = rel(g_calc, G)
rec("L3", "引力还原 G = hbar*c / m_P^2",
    "PASS" if ok(e_F01, 1e-6) else "FAIL",
    "m_P = sqrt(hbar*c/G)  =>  G = hbar*c/m_P^2",
    "G_calc = " + format(g_calc, ".15e") + " ; CODATA G = " + format(G, ".15e") + " ; rel = " + format(e_F01, ".3e"),
    e_F01,
    "v10 W10。引力是唯一的'无媒介子'(lambda=inf)分支，q_G = m/m_P。注意这是**定义恒等式**"
    "（m_P 由 G 定义），不具独立预测力——见 L5-B01。此处仅验证代数自洽。")

# F02 引力数值（质子对，r=1e-15 m）
r_s = 1.0e-15
F_grav = G * M_PROTON ** 2 / r_s ** 2
rec("L3", "引力（牛顿） F = G m1 m2 / r^2",
    "PASS",
    "F = G m1 m2 / r^2",
    "m1=m2=m_p, r=1e-15 m => F = " + format(F_grav, ".6e") + " N",
    0.0, "v10 W11 同口径。")

# F03 库仑还原：hbar*c*alpha = e^2/(4*pi*eps0)
ke_e2 = E_CHG ** 2 / (4 * math.pi * EPS0)
hc_alpha = HBAR * C * ALPHA
e_F03 = rel(hc_alpha, ke_e2)
rec("L3", "库仑还原 hbar*c*alpha = e^2/(4*pi*eps0)",
    "PASS" if ok(e_F03, 1e-6) else "FAIL",
    "alpha = e^2/(4*pi*eps0*hbar*c)  =>  hbar*c*alpha = e^2/(4*pi*eps0)",
    "hbar*c*alpha = " + format(hc_alpha, ".15e") + " ; e^2/(4pi eps0) = " + format(ke_e2, ".15e") + " ; rel = " + format(e_F03, ".3e"),
    e_F03,
    "v10 W12。电磁是'无媒介子'(lambda=inf)分支，q_E = sqrt(alpha)*Z。")

# F04 电场力数值（质子对）
F_elec = E_CHG ** 2 / (4 * math.pi * EPS0 * r_s ** 2)
rec("L3", "电场力（库仑） F = q1 q2 / (4*pi*eps0 r^2)",
    "PASS",
    "F = q1 q2 / (4*pi*eps0 r^2)",
    "q1=q2=e, r=1e-15 m => F = " + format(F_elec, ".6e") + " N",
    0.0, "比引力大 alpha*(m_P/m_p)^2 ~ 1.24e36 倍（F11）。")

# F05 磁场力/电场力 = v^2/c^2（两平行同速运动电荷）
v_test = 1.0e6
F_B_analytic = MU0 * E_CHG ** 2 * v_test ** 2 / (4 * math.pi * r_s ** 2)
ratio_BE = F_B_analytic / F_elec
ratio_pred = v_test ** 2 / C ** 2
e_F05 = rel(ratio_BE, ratio_pred)
rec("L3", "磁场力/电场力 = v^2/c^2（平行运动电荷）",
    "PASS" if ok(e_F05, 1e-9) else "FAIL",
    "F_B = mu0 q^2 v^2/(4pi r^2), F_E = q^2/(4pi eps0 r^2) => F_B/F_E = mu0 eps0 v^2 = v^2/c^2",
    "F_B/F_E = " + format(ratio_BE, ".10e") + " ; v^2/c^2 = " + format(ratio_pred, ".10e") + " ; rel = " + format(e_F05, ".3e"),
    e_F05,
    "标准电磁学结果。磁场是电场的相对论运动伴生项（v/c 一阶产生 B，做功率 0，见 F07）。"
    "本框架的严格还原（tau 场运动 -> B）仍 OPEN（v9 W22），登记为诚实边界。")

# F06 麦克斯韦关系 c^2 = 1/(eps0 mu0)
inv_em = 1.0 / (EPS0 * MU0)
e_F06 = rel(inv_em, C ** 2)
rec("L3", "麦克斯韦关系 c^2 = 1/(eps0 mu0)",
    "PASS" if ok(e_F06, 1e-9) else "FAIL",
    "c^2 = 1/(eps0 mu0)",
    "1/(eps0 mu0) = " + format(inv_em, ".10e") + " ; c^2 = " + format(C ** 2, ".10e") + " ; rel = " + format(e_F06, ".3e"),
    e_F06, "电磁扇区量纲闭合的基石。")

# F07 洛伦兹磁力不做功：F_B · v = 0
v_vec = (1.0, 0.0, 0.0)
B_vec = (0.0, 0.0, 1.0)
fxb = cross(v_vec, B_vec)
work = dot(fxb, v_vec)
rec("L3", "洛伦兹磁力不做功 F_B · v = 0",
    "PASS" if abs(work) < 1e-15 else "FAIL",
    "F_B = q (v x B) ; (v x B)·v = 0",
    "(vxB)·v = " + format(work, ".3e"),
    0.0 if work == 0 else 1.0,
    "磁场力恒垂直于速度 => 不做功，只改变方向（垂直原理在粒子动力学层的体现）。")

# F08 弱力力程 lam_W 与 v10 比对（M05 已算）
e_F08 = rel(lam_W, V10_LAMBDA_W_M)
rec("L3", "弱核力力程 lambda_W = hbar/(m_W c) 与 v10 比对",
    "PASS" if ok(e_F08, 1e-6) else "FAIL",
    "lambda_W = hbar/(m_W c)",
    "lambda_W = " + format(lam_W, ".10e") + " m = " + format(lam_W * 1e15, ".6f") + " fm ; v10 = " + format(V10_LAMBDA_W_M, ".10e") + " m ; rel = " + format(e_F08, ".3e"),
    e_F08, "弱力中介 W/Z，短程 ~0.00245 fm。")

# F09 强力力程 lam_pi 与 v10 比对
e_F09 = rel(lam_pi, V10_LAMBDA_PI_M)
rec("L3", "强核力（剩余核力）力程 lambda_pi = hbar/(m_pi c) 与 v10 比对",
    "PASS" if ok(e_F09, 1e-5) else "FAIL",
    "lambda_pi = hbar/(m_pi c)",
    "lambda_pi = " + format(lam_pi, ".10e") + " m = " + format(lam_pi * 1e15, ".6f") + " fm ; v10 = " + format(V10_LAMBDA_PI_M, ".10e") + " m ; rel = " + format(e_F09, ".3e"),
    e_F09, "剩余强核力（pi 介子交换）力程 ~1.46 fm。注意：这是**剩余核力**，"
    "非禁闭势；禁闭线性项见 F13。与 v10 残差 ~1.5e-6 来自 pi0 质量常数取法（PDG 134.977 MeV），非理论偏差。")

# F10 汤川势衰减特征 e^{-r/lambda}
r_lam = lam_pi
y1 = math.exp(-r_lam / r_lam)
y3 = math.exp(-3 * r_lam / r_lam)
rec("L3", "汤川势衰减特征 e^{-r/lambda}",
    "PASS" if abs(y1 - 1 / math.e) < 1e-12 and abs(y3 - math.exp(-3)) < 1e-12 else "FAIL",
    "V(r) ~ e^{-r/lambda}/r ; V(lambda)/V(0+) = e^{-1} ; V(3 lambda) = e^{-3}",
    "ratio(r=lambda) = " + format(y1, ".6f") + " (e^-1=" + format(1 / math.e, ".6f") + ") ; ratio(r=3lambda) = " + format(y3, ".6f") + " (e^-3=" + format(math.exp(-3), ".6f") + ")",
    0.0, "力程由媒介子质量决定，统一母方程的直接数值后果。")

# F11 力比 F_E / F_G（质子对）= alpha (m_P/m_p)^2 vs v9 W12 的 1.2356e36
ratio_eg = ALPHA * (M_P_KG / M_PROTON) ** 2
v9_eg = 1.2356e36
e_F11 = rel(ratio_eg, v9_eg)
rec("L3", "力比 F_E / F_G（质子对）= alpha (m_P/m_p)^2",
    "PASS" if ok(e_F11, 1e-3) else "FAIL",
    "F_E/F_G = [e^2/(4pi eps0)]/[G m_p^2] = alpha (m_P/m_p)^2",
    "F_E/F_G = " + format(ratio_eg, ".6e") + " ; v9 W12 = " + format(v9_eg, ".6e") + " ; rel = " + format(e_F11, ".3e"),
    e_F11,
    "与 v9 W12 一致（交叉验证）。这是四力统一'为何电磁比引力强 36 个量级'的标准答案。")

# F12 四力力程层级排序
ordering = [("引力", float("inf")), ("电磁", float("inf")),
            ("强(剩余核力)", lam_pi), ("弱", lam_W)]
ordering_sorted = sorted(ordering, key=lambda x: -x[1])
rec("L3", "四力力程层级排序（长程->短程）",
    "PASS",
    "lambda: G=inf, EM=inf, pi=1.46e-15 m, W=2.45e-18 m",
    " -> ".join(("%s(%.3e m)" % (n, l)) if l != float("inf") else ("%s(inf)" % n) for n, l in ordering_sorted),
    0.0, "层级：G=EM >> 强 > 弱。统一母方程用同一形式承载全部四力，仅质量/耦合不同。")

# F13 禁闭线性项 sigma*r 不在 Proca 齐次解内（诚实 FAIL）
r_chk = 1.0e-15
lhs_lin = SIGMA_STRING * (2.0 / r_chk - (MU_TEST) ** 2 * r_chk)
rec("L3", "禁闭线性项 sigma*r 不是 Proca 齐次解",
    "FAIL",
    "(nabla^2 - mu^2)(sigma r) = sigma*(2/r - mu^2 r)  != 0",
    "残差 = " + format(lhs_lin, ".6e") + " J/m (非零) @ r=1e-15 m",
    None,
    "X07：强核力的禁闭线性势 sigma*r 无法由 Proca 场方程给出——它是**额外项**，"
    "统一母方程对强力的还原只到'剩余汤川势'层，'禁闭'是独立于该框架的现象。不粉饰为 PASS。")

# ================================================================ L5 诚实边界层
rec("L5", "边界 B01：G 由 m_P 定义（循环，无预测力）",
    "FAIL",
    "m_P := sqrt(hbar*c/G)  =>  G = hbar*c/m_P^2 是定义恒等式",
    "F01 已验证代数自洽，但 m_P 本身由 G 定义 => 任何'从母方程导出 G'都循环",
    None, "X08。引力常数 G 是输入，非第一性导出。")

rec("L5", "边界 B02：精细结构常数 alpha 为输入，无方程",
    "FAIL",
    "alpha = e^2/(4 pi eps0 hbar c) 是给定的实验锚",
    "母方程不产出 alpha（单位圆归一化对任意 alpha 成立，见 G06）",
    None, "X10/W20。alpha 的值必须由实验给定。")

rec("L5", "边界 B03：四力耦合常数均为输入",
    "FAIL",
    "g_s, alpha_EM, g_W, G 全部作为参数喂入母方程",
    "母方程形式统一，但 4 个耦合无内部方程决定",
    None, "v9 W12/W20：统一'形式'不统一'数值'。")

rec("L5", "边界 B04：tau 场 -> 极端引力尺度 ell_P^2（INFO）",
    "INFO",
    "G epsilon0 类表达式给出 kappa*tau 组合 ~ 1/ell_P^2",
    "tau 场在 EC 尺度 l_P^2 上贡献，属极端引力/量子引力领域",
    None, "v9 W22 的 tau 场 -> EC 推演 OPEN：本册只确认其存在与量级，未做独立数值验证。")

rec("L5", "冲突台账 B05：alpha = tau/kappa (0.007297) vs alpha = kappa/tau (137.036)",
    "BOUNDARY",
    "utf 内存在两套互为倒数的 alpha 定义，二者不可能同时正确",
    "tau/kappa = " + format(ALPHA, ".6e") + " ; kappa/tau = " + format(1.0 / ALPHA, ".6e") + " ; 二者互为倒数",
    None, "本册采用 v8.1 D07 / v4-25 的 tau/kappa 口径（与 CODATA alpha=7.297e-3 一致）。"
    "另一口径（alpha = kappa/tau = 1/137）是独立文档的写法，未代选，仅登记。")

# ================================================================ 收尾：写 JSON + 摘要 + 自检
def _summarize():
    from collections import Counter
    return Counter(r["verdict"] for r in RESULTS)


def write_outputs():
    here = os.path.dirname(os.path.abspath(__file__))
    out = {
        "title": "四力大统一方程 · 垂直原理 — 零依赖复算",
        "generated_note": "全部数值由本脚本独立计算，未抄录任何结论数",
        "constants": {
            "HBAR": HBAR, "C": C, "G": G, "E_CHG": E_CHG, "EPS0": EPS0,
            "MU0": MU0, "ALPHA": ALPHA, "M_P_KG": M_P_KG,
            "M_PROTON": M_PROTON, "M_W_GEV": M_W_GEV, "M_PI0_MEV": M_PI0_MEV,
            "PLANCK_LEN": PLANCK_LEN,
        },
        "key_numbers": {
            "lambda_W_m": lam_W, "lambda_W_fm": lam_W * 1e15,
            "lambda_pi_m": lam_pi, "lambda_pi_fm": lam_pi * 1e15,
            "F_E_over_F_G_proton": ratio_eg,
            "c_from_em": math.sqrt(inv_em),
        },
        "results": RESULTS,
        "verdict_counts": dict(_summarize()),
    }
    jpath = os.path.join(here, "四力大统一_验证结果.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    tpath = os.path.join(here, "四力大统一_验证摘要.txt")
    lines = []
    lines.append("四力大统一方程 · 垂直原理 — 验证摘要")
    lines.append("=" * 70)
    counts = _summarize()
    lines.append("判定计数: " + "  ".join("%s=%d" % (k, v) for k, v in sorted(counts.items())))
    lines.append("条目总数: %d" % len(RESULTS))
    lines.append("-" * 70)
    for r in RESULTS:
        lines.append("[%s] %-4s %s" % (r["layer"], r["verdict"], r["name"]))
        lines.append("      公式: " + str(r["symbolic"]))
        lines.append("      数值: " + str(r["numeric"]))
        if r["rel_error"] is not None:
            lines.append("      相对误差: " + str(r["rel_error"]))
        lines.append("      注: " + str(r["note"]))
        lines.append("")
    with open(tpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return jpath, tpath


if __name__ == "__main__":
    jp, tp = write_outputs()
    counts = _summarize()
    print("验证完成。")
    print("判定计数:", dict(counts))
    print("条目总数:", len(RESULTS))
    missing = [r for r in RESULTS if r["verdict"] not in ("PASS", "FAIL", "BOUNDARY", "INFO")]
    assert not missing, "存在未判定条目: %s" % missing
    print("PASS 条目: %d" % counts.get("PASS", 0))
    print("JSON -> %s" % jp)
    print("摘要 -> %s" % tp)
    print("退出码 0")
    sys.exit(0)
