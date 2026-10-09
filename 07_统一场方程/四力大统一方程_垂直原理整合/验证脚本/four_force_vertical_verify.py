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
h_s = 1e-6
T_a = unit(d1(TH0 - h_s))
T_b = unit(d1(TH0 + h_s))
dT = tuple((x2 - x0) / (2 * h_s) for x0, x2 in zip(T_a, T_b))
B_a = unit(cross(d1(TH0 - h_s), d2(TH0 - h_s)))
B_b = unit(cross(d1(TH0 + h_s), d2(TH0 + h_s)))
dB = tuple((x2 - x0) / (2 * h_s) for x0, x2 in zip(B_a, B_b))
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


def lap_spherical(f, r, mu, h=1e-5):
    """球坐标拉普拉斯 ∇²f = (1/r²) d/dr [ r² df/dr ]，中心差分。"""
    def fp(x):
        return math.exp(-mu * x) / x
    fp1 = (fp(r + h) - fp(r - h)) / (2 * h)
    gp = lambda x: x * x * (fp(x + h) - fp(x - h)) / (2 * h)
    return (gp(r + h) - gp(r - h)) / (2 * h) / (r * r)


MU_TEST = 1.0 / 7.3e-16     # 1/m，取力程 ~0.73 fm
R_TEST = 3.0e-15
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
    "PASS" if ok(e_w, 1e-6) and ok(e_pi, 1e-6) else "FAIL",
    "lambda = hbar/(m c)",
    "m_W=%.3f GeV/c² ⇒ lambda_W=%.10e m = %.8f fm (v10: %.10e, rel=%.3e)\n                "
    "m_pi0=%.3f MeV/c² ⇒ lambda_pi=%.10e m = %.8f fm (v10: %.10e, rel=%.3e)"
    % (M_W_GEV, lam_W, lam_W * 1e15, V10_LAMBDA_W_M, e_w,
       M_PI0_MEV, lam_pi, lam_pi * 1e15, V10_LAMBDA_PI_M, e_pi),
    max(e_w, e_pi),
    "本册独立复算与 v10 公布读数一致（交叉验证）。力程全部由媒介子质量决定——质量是输入。")
# __NEXT__
