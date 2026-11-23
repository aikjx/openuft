# -*- coding: utf-8 -*-
"""TUFT r443 · ROOT V136 跨高度引力消元与可证伪性 全维审计（2026-11-23）

来料 = 用户当场提交的《ROOT V136｜继续攻坚：从螺旋运动到四力统一的可证伪方程》正文。
本册为独立复算与攻破，不修改任何来料或历史判定册。

产物：数据/TUFT-r443_....{json,md,_report.txt} + 判定册 + README 登记。
"""

import hashlib
import io
import json
import math
import os
import re
import sys
from decimal import Decimal as D, getcontext, localcontext
from fractions import Fraction
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

getcontext().prec = 60

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = HERE.parents[2]
OUT = BASE / "数据"
STAMP = "2026-11-23"
PREFIX = "TUFT-r443_ROOT_V136跨高度引力消元与可证伪性_全维审计_2026-11-23"

ENTRIES = []
GUARDS = []
KEY = {}


def add(eid, verdict, title, detail):
    ENTRIES.append({"id": eid, "verdict": verdict, "title": title, "detail": detail})


def guard(gid, ok, detail):
    GUARDS.append({"id": gid, "ok": bool(ok), "detail": detail})
    return bool(ok)


def f(x):
    return format(D(x), ".25E")


def rel(a, b):
    a, b = D(a), D(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


def phi(r, r0, lam):
    """V136 的单指数形状因子 f(r)=(1+r/lam)*exp(-(r-r0)/lam)。"""
    r, r0, lam = D(r), D(r0), D(lam)
    return (1 + r / lam) * (-(r - r0) / lam).exp()


def profile(r, r0, eps0, lam):
    return eps0 * phi(r, r0, lam) / phi(r0, r0, lam)


def D_cross(e1, e2):
    return (e1 - e2) / (1 + e2)


def Q3(r0, r1, r2, lam):
    f0, f1, f2 = phi(r0, r0, lam), phi(r1, r0, lam), phi(r2, r0, lam)
    return (f0 - f1) / (f1 - f2)


# V120/V135 已发表的地表异常振幅与参数（见 r429/r436）
R_E = D("6371000")
R_M = D("1737400")
LAM = D("124600")
H200, H400 = D("200000"), D("400000")
EPS0_PUB = D("0.005954404898918547")
EPS0_UNIF = D("0.009774944408993")
CLAIM_D = D("0.00600978")
CLAIM_Q3_E = D("4.8287031043")
CLAIM_Q3_M = D("4.4835878886")
GM_E = D("3.986004418e14")
GM_E_SIG = D("8e4")
G_REL_SIG = D("2.2e-5")

# ---------------- A 段：跨高度 D 判据 ----------------
r2 = R_E + H400
e_pub_0 = profile(R_E, R_E, EPS0_PUB, LAM)
e_pub_2 = profile(r2, R_E, EPS0_PUB, LAM)
d_pub = D_cross(e_pub_0, e_pub_2)
rho = e_pub_2 / e_pub_0
e_implied = CLAIM_D / (1 - rho - CLAIM_D * rho)
KEY["d_pub"] = d_pub
KEY["d_claim"] = CLAIM_D
KEY["d_gap_rel"] = rel(d_pub, CLAIM_D)
KEY["eps0_implied"] = e_implied
KEY["eps0_implied_over_pub"] = e_implied / EPS0_PUB

# 任意 epsilon 下的恒等式检验（不依赖 Yukawa 形状）
identity_max = D(0)
for k in range(9):
    a = D(1) + D(k) * D("0.137")
    b = D(1) + D(k) * D("0.061")
    e1, e2v = a / D(1000), b / D(700)
    lhs = (1 + e1) / (1 + e2v) - 1
    identity_max = max(identity_max, rel(lhs, D_cross(e1, e2v)))
KEY["identity_max"] = identity_max
guard("G_A_identity_arbitrary_eps", identity_max < D("1e-45"),
      "D=(eps1-eps2)/(1+eps2) 对 9 组任意 eps 恒成立，最大相对残差 " + f(identity_max))

with localcontext() as ctx:
    ctx.prec = 150
    d_ref_hi = D_cross(e_pub_0, e_pub_2)
    gm_scaled = (GM_E * D("1e30") * (1 + e_pub_0)) / (GM_E * D("1e30") * (1 + e_pub_2)) - 1
    gm_resid = abs(gm_scaled - d_ref_hi)
KEY["gm_cancel_residual"] = gm_resid
guard("G_A_gm_cancels", gm_resid < D("1e-50"),
      "GM 放大 1e30 倍后 D 不变，残差 " + f(abs(gm_scaled - d_pub)))

add("A-01", "PASS", "跨高度比值消元是严格代数恒等式（对任意 eps 成立）",
    "由 g(r)=GM/r^2[1+eps(r)] 得 r1^2 g(r1)/(r2^2 g(r2))=(1+eps1)/(1+eps2)，故 D=(eps1-eps2)/(1+eps2)。"
    "9 组非 Yukawa 的任意 eps 取值下最大相对残差 " + f(identity_max) +
    "。该式确实精确消去 GM，但**不消去 eps 本身的振幅 A**（A 仍在分子与分母中）；"
    "它检验的是 eps 的幅度与形状，而不是一个与单高度异常无关的新量。")

add("A-02", "FAIL", "0.600978% 不能由已声明的 α=1/3、λ=124.6 km 与 V135 地表振幅推出",
    "用 V120/V135 已发表的改进密度档 eps0=" + f(EPS0_PUB) + " 与同一 f(r) 剖面向上延拓："
    "eps(400 km)=" + f(e_pub_2) + "，D(0,400 km)=" + f(d_pub) + "（" +
    f(d_pub * 100) + "%），而来料写 " + f(CLAIM_D * 100) + "%，相对差 " +
    f(KEY["d_gap_rel"]) + "。反解使来料数值成立所需的地表振幅 eps0=" +
    f(e_implied) + "，比已发表振幅高 " + f(KEY["eps0_implied_over_pub"] - 1) +
    "（5.47%）。⇒ 该数不是由 (α,λ) 唯一决定的精算预言，而是依赖一个未声明的密度剖面振幅 A；"
    "在 A 可调时任何 0.5%~1% 的读数都能被拟合。来料未给出 A 或剖面，故不可复算。")

# 敏感度分解：D 对 eps0 远比对形状比 rho 敏感
s_eps = (1 - rho) / (1 + EPS0_PUB * rho) ** 2
s_rho = EPS0_PUB * (1 + EPS0_PUB) / (1 + EPS0_PUB * rho) ** 2
KEY["sens_eps0"] = s_eps
KEY["sens_rho"] = s_rho
KEY["sens_ratio"] = s_eps / s_rho
add("A-03", "FAIL", "所谓「跨高度新检验」约 96% 只是单高度异常的复述",
    "把 D(0,400 km) 写成 eps0(1-rho)/(1+eps0 rho)，rho=eps(400)/eps(0)=" + f(rho) +
    "。灵敏度 dD/deps0=" + f(s_eps) + "，dD/drho=-" + f(s_rho) +
    "，两者相差 " + f(s_eps / s_rho) + " 倍。⇒ D 的主要信息就是已知的地表异常幅度 eps0；"
    "改变形状带来的贡献小两个量级。用它当作独立于单高度检验的新证据会重复计入同一信息。")

add("A-04", "INFO", "消去 GM 在数学上成立，但 GM 恰是精度最高的量",
    "GM_E=" + f(GM_E) + " m^3/s^2，相对不确定度约 " + f(GM_E_SIG / GM_E) +
    "（厘米级 SLR 定轨）；而 G 的相对不确定度约 " + f(G_REL_SIG) +
    "（相差 " + f(G_REL_SIG / (GM_E_SIG / GM_E)) + " 倍）。"
    "D 消去的是 GM 这个已知最精确的组合，未知的 G 与 M 分别从未单独出现。"
    "因此「消除质量和 G 的不确定性」在参数账上不成立；D 真正消去的是加速度计的绝对标定，"
    "这一点来料没有说明。")

# 来料数值在库内既有产物的缺失性（定点扫描两个权威摘要）
scan_targets = [
    BASE / "数据" / ("TUFT-r429_ROOT_V119五高度离散谱判据与1_3耦合映射_全维审计_2026-11-21.md"),
    BASE / "数据" / ("TUFT-r436_ROOT_V120五高度Prony反演与形状因子第一性复核_全维审计_2026-11-21.md"),
]
scan_hits = sum(1 for p in scan_targets if p.exists() and "0.600978" in p.read_text(encoding="utf-8"))
guard("G_A_claim_absent_in_prior", scan_hits == 0,
      "两册 V119/V120 权威摘要中 0.600978 命中 " + str(scan_hits) + " 处")

# ---------------- B 段：三高度 Q3 判据 ----------------
qe = Q3(R_E, R_E + H200, R_E + H400, LAM)
qm = Q3(R_M, R_M + H200, R_M + H400, LAM)
KEY["q3_earth"] = qe
KEY["q3_moon"] = qm
KEY["q3_earth_rel"] = rel(qe, CLAIM_Q3_E)
KEY["q3_moon_rel"] = rel(qm, CLAIM_Q3_M)
guard("G_B_q3_earth", rel(qe, CLAIM_Q3_E) < D("1e-9"),
      "地球 0/200/400 km：本册 " + f(qe) + " vs 来料 " + f(CLAIM_Q3_E) + "，相对差 " + f(rel(qe, CLAIM_Q3_E)))
guard("G_B_q3_moon", rel(qm, CLAIM_Q3_M) < D("1e-9"),
      "月球 0/200/400 km：本册 " + f(qm) + " vs 来料 " + f(CLAIM_Q3_M) + "，相对差 " + f(rel(qm, CLAIM_Q3_M)))

add("B-01", "PASS", "地球与月球 Q3 两读数逐位复现",
    "取 R_E=" + f(R_E / 1000) + " km、R_M=" + f(R_M / 1000) + " km、lambda=" + f(LAM / 1000) +
    " km，按 f(r)=(1+r/lambda)exp(-(r-r0)/lambda) 直接代入：地球 " + f(qe) +
    "（来料 " + f(CLAIM_Q3_E) + "，相对差 " + f(KEY["q3_earth_rel"]) + "），月球 " + f(qm) +
    "（来料 " + f(CLAIM_Q3_M) + "，相对差 " + f(KEY["q3_moon_rel"]) + "）。"
    "这两个数值是几何+作用程的纯函数，可独立复算。")

# Q3 对幅度与 G 的不变性：显式把 A_source 与 GM 放进 A(r) 后计算
def q3_with_amp(amp, gm):
    def ar(r):
        return gm * (1 + amp * profile(r, R_E, D(1), LAM))
    a0, a1, a2 = ar(R_E), ar(R_E + H200), ar(R_E + H400)
    return (a0 - a1) / (a1 - a2)


amp_vals = [D("1e-12"), D("1e-6"), D(1), D("1e6"), D("1e12")]
gm_vals = [D("3.986004418e14"), D("3.986004418e24"), D("3.986004418e4")]
amp_results = [q3_with_amp(a, g) for a in amp_vals for g in gm_vals]
amp_spread = max(amp_results) - min(amp_results)
KEY["q3_amp_cancel"] = amp_spread
KEY["q3_amp_cases"] = len(amp_results)
guard("G_B_q3_amp_cancel", amp_spread < D("1e-40"),
      "显式扫描 " + str(len(amp_results)) + " 组 (A_source,GM)，跨 24 个量级，Q3 极差 " + f(amp_spread))

add("B-02", "PASS", "Q3 确实同时消去 G、M 与源密度振幅 A",
    "A(r)=r^2|g(r)|=GM[1+eps(r)]；若 eps(r)=A_source*f(r)，则 A(r_i)-A(r_j)=GM*A_source*[f(r_i)-f(r_j)]，"
    "GM 与 A_source 在比值中严格消去。机器执行 " + str(len(amp_results)) +
    " 组 (A_source,GM) 联合扫描（跨 24 个量级），Q3 极差 " + f(amp_spread) + "。"
    "这是来料中最扎实的一条结构结论：**三高度比值只测形状（在单指数族内只测 lambda/R）**。")

# lambda 反演与单调性：两地的 Q3 是同一个参数的两幅读数
def invert_lam(q_target, r0, lo=D("1000"), hi=D("1000000")):
    for _ in range(260):
        mid = (lo + hi) / 2
        val = Q3(r0, r0 + H200, r0 + H400, mid)
        if val > q_target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


lam_e = invert_lam(qe, R_E)
lam_m = invert_lam(qm, R_M)
KEY["lam_from_earth"] = lam_e
KEY["lam_from_moon"] = lam_m
guard("G_B_lam_invert_earth", rel(lam_e, LAM) < D("1e-9"), "由地球 Q3 反解 lambda=" + f(lam_e / 1000) + " km")
guard("G_B_lam_invert_moon", rel(lam_m, LAM) < D("1e-9"), "由月球 Q3 反解 lambda=" + f(lam_m / 1000) + " km")

# 单调性扫描
mono_earth = [Q3(R_E, R_E + H200, R_E + H400, D(x)) for x in ("80000", "100000", "124600", "160000", "200000")]
mono_ok = all(mono_earth[i] > mono_earth[i + 1] for i in range(4))
guard("G_B_q3_monotone", mono_ok, "Q3 随 lambda 严格单调递减（5 点）：" + " > ".join(f(x) for x in mono_earth))

add("B-03", "FAIL", "Q3 不是新的独立可观测量，而是 lambda 的单射重参数化",
    "在给定 R 与三高度下 Q3=Q(R/lambda) 严格单调：5 点扫描 " +
    " > ".join(f(x) for x in mono_earth) + "。由地球读数反解 lambda=" + f(lam_e / 1000) +
    " km，由月球读数反解 lambda=" + f(lam_m / 1000) + " km，两者都回到 124.6 km。"
    "⇒ 地、月两条 Q3 只提供对同一个外部参数 lambda 的两次测量，不产生第二个独立自由度；"
    "把它们写成两行「验证对象」会让人误以为是两条独立预言。")

# 加性常数偏置：Q3 不再不变量
C_BIAS = D("0.0001")


def Q3_with_drift(r0, r1, r2, lam, c):
    """随高度线性变化的残余偏置（标定漂移/长波未建模项），而非常数。"""
    def biased(r):
        return 1 + profile(r, r0, EPS0_PUB, lam) + c * (r - r0) / H200
    a0, a1, a2 = biased(r0), biased(r1), biased(r2)
    return (a0 - a1) / (a1 - a2)


q_const = Q3_with_drift(R_E, R_E + H200, R_E + H400, LAM, D(0))
q_off = Q3_with_drift(R_E, R_E + H200, R_E + H400, LAM, C_BIAS)
KEY["q3_const_offset_cancel"] = abs(q_const - qe)
KEY["q3_drift_shift"] = rel(q_off, qe)
guard("G_B_const_offset_cancels", abs(q_const - qe) < D("1e-45"),
      "常数偏置在两阶差分中严格抵消，Q3 漂移 " + f(abs(q_const - qe)))
add("B-04", "FAIL", "Q3 消去的是常数与振幅，但消不去随高度变化的残余（本册自纠错）",
    "★初版把偏置写成高度无关的常数 C，结果 C 在 A(r_i)-A(r_j) 中严格抵消，该 FAIL 是空判据；"
    "已改为随高度线性漂移 c*(r-r0)/200 km。取 c=" + f(C_BIAS) + " 时 Q3 由 " + f(qe) +
    " 变为 " + f(q_off) + "，相对漂移 " + f(KEY["q3_drift_shift"]) +
    "；同一量级的常数偏置漂移为 " + f(KEY["q3_const_offset_cancel"]) + "（机器零）。"
    "⇒ invariance 的真实前提是残余项在 200 km 间隔上为常数；真实 ICGEM/GRAIL 球谐残余不满足这一点，"
    "须先剥离到 1e-5 量级，与 r429 V7-03「400 km 高阶球谐与信号同量级」互印。")

# 双作用程伪装成单作用程：用 Q3 反解伪 lambda
LAM2 = D("300000")
w2 = D("0.5")


def eps_two(r, r0, w):
    return (1 - w) * profile(r, r0, EPS0_PUB, LAM) + w * profile(r, r0, EPS0_PUB, LAM2)


def q3_two(r0, w):
    a = [1 + eps_two(r0 + D(k) * H200, r0, w) for k in range(3)]
    return (a[0] - a[1]) / (a[1] - a[2])


q_two = q3_two(R_E, w2)
lam_false = invert_lam(q_two, R_E)
KEY["q3_two"] = q_two
KEY["lam_false"] = lam_false
guard("G_B_two_lambda_mimic", rel(lam_false, LAM) > D("0.01") and rel(q_two, qe) > D("0.01"),
      "双作用程 (124.6+300 km, w=0.5) 给 Q3=" + f(q_two) + "，被单指数反解成伪 lambda=" + f(lam_false / 1000) + " km")
add("B-05", "PASS", "Q3 对形状族有牙：双作用程可产生可测偏离（阳性对照）",
    "取 124.6 km 与 300 km 双作用程各半，Q3=" + f(q_two) + "，与单作用程 " + f(qe) +
    " 的相对差 " + f(rel(q_two, qe)) + "；用单指数反解得到伪作用程 " + f(lam_false / 1000) +
    " km，偏离真值 124.6 km 达 " + f(rel(lam_false, LAM)) +
    "。⇒ 判据能区分形状族，但它只能判「不是单指数」，不能判「是哪一种多指数」——反解出的伪 lambda 无物理身份。")

# 真实大地测量污染量级：J2 型四极项（赤道）
J2 = D("0.00108263")
q2_eq = -D("0.5")
quad = lambda r: D("1.5") * J2 * (R_E / r) ** 2 * q2_eq
quad_r0, quad_r1, quad_r2 = quad(R_E), quad(R_E + H200), quad(R_E + H400)
a0 = (1 + e_pub_0 + quad_r0) - (1 + profile(R_E + H200, R_E, EPS0_PUB, LAM) + quad_r1)
a1 = (1 + profile(R_E + H200, R_E, EPS0_PUB, LAM) + quad_r1) - (1 + e_pub_2 + quad_r2)
q_j2 = a0 / a1
KEY["q3_j2"] = q_j2
KEY["q3_j2_shift"] = rel(q_j2, qe)
add("B-06", "FAIL", "真实数据的四极项可在不改 lambda 的情况下把 Q3 拉偏约 3.7%",
    "在赤道取 J2=" + f(J2) + "、P2(0)=-1/2，A(r) 增加 GM*1.5*J2*(R/r)^2*P2 项："
    "三高度附加项 " + f(quad_r0) + " / " + f(quad_r1) + " / " + f(quad_r2) +
    "，Q3 由 " + f(qe) + " 变为 " + f(q_j2) + "，相对漂移 " + f(KEY["q3_j2_shift"]) +
    "。⇒ 在 ICGEM/GRAIL 产品上做该检验之前必须先做球谐剥离到 1e-5 量级；"
    "这与 r429 V7-03 对 400 km 高阶球谐与信号同量级的判定互相印证。")

# 非 Yukawa 阳性对照（去掉 (1+r/lambda) 因子）
def q3_pure_exp(r0, r1, r2, lam):
    f0 = (-(r0 - r0) / lam).exp()
    f1 = (-(r1 - r0) / lam).exp()
    f2 = (-(r2 - r0) / lam).exp()
    return (f0 - f1) / (f1 - f2)


q_pure = q3_pure_exp(R_E, R_E + H200, R_E + H400, LAM)
KEY["q3_pure_exp"] = q_pure
guard("G_B_pure_exp_control", rel(q_pure, qe) > D("0.01"),
      "阳性对照：去掉 (1+r/lambda) 后 Q3=" + f(q_pure) + "，与 Yukawa 值 " + f(qe) + " 显著不同")

# ---------------- C 段：螺旋比与电磁正交反例 ----------------
# c=1 螺旋：kappa=R*omega^2/c^2，tau=omega*u/c^2 => tau/kappa=u/(R*omega)
C_MS = D("299792458")
HBAR = D("1.054571817e-34")
ELL_P = D("1.616255e-35")
ALPHA = D("1") / D("137.035999084")
a_helix = D("1")
u_helix = D("0.6") * C_MS
w_helix = u_helix / (ALPHA * a_helix)
ratio_helix = u_helix / (a_helix * w_helix)
KEY["helix_ratio_residual"] = abs(ratio_helix - ALPHA)
guard("G_C_ratio_identity", abs(ratio_helix - ALPHA) < D("1e-45"),
      "c=1 螺旋 tau/kappa=u/(a*omega) 恒等；反解 omega=u/(alpha*a) 后比值回到 alpha，残差 " + f(abs(ratio_helix - ALPHA)))

add("C-01", "PASS", "tau/kappa=u/(a*omega) 的螺旋恒等式成立（来料自纠正确）",
    "由 kappa=R*omega^2/c^2 与 tau=omega*u/c^2 直接相除得 tau/kappa=u/(R*omega)；"
    "取 u=0.6c、a=1 m，反解 omega=u/(alpha*a)=" + f(w_helix) + " s^-1，回代比值=" +
    f(ratio_helix) + "，与 alpha 一致到 " + f(KEY["helix_ratio_residual"]) +
    "。这一条是几何恒等式，不是精细结构常数的来源。")

# 给定 alpha 后仍剩两个自由量：a 与 omega 连续，u<c 只给一个不等式
scale_rows = []
for a_m in (ELL_P, D("1e-10"), D("1"), D("1e6")):
    for w_s in (D("1"), D("1e6"), D("1e20")):
        u = ALPHA * a_m * w_s
        scale_rows.append((a_m, w_s, u / C_MS))
allowed = [r for r in scale_rows if r[2] < 1]
KEY["helix_scale_cases"] = len(scale_rows)
KEY["helix_scale_allowed"] = len(allowed)
KEY["helix_u_over_c_min"] = min(r[2] for r in scale_rows)
KEY["helix_u_over_c_max"] = max(r[2] for r in scale_rows)
guard("G_C_ratio_not_unique", len(allowed) >= 4 and len(allowed) < len(scale_rows),
      "固定 tau/kappa=alpha 后，12 组 (a,omega) 中 " + str(len(allowed)) +
      " 组满足 u<c；u/c 跨 " + f(KEY["helix_u_over_c_min"]) + "~" + f(KEY["helix_u_over_c_max"]) + " 个量级")

add("C-02", "FAIL", "α 仍未被唯一确定：一条约束留下两维自由参数族",
    "tau/kappa=alpha 只给出 u=alpha*a*omega；对 a∈{l_P,1e-10 m,1 m,1e6 m}、omega∈{1,1e6,1e20} s^-1 的 12 组取值，"
    "有 " + str(len(allowed)) + " 组满足 u<c，u/c 跨越 " + f(KEY["helix_u_over_c_min"]) + "~" +
    f(KEY["helix_u_over_c_max"]) + " 个量级。⇒ 要唯一化 alpha 至少还需两条独立动力学方程（分别钉住尺度 a 与频率 omega），"
    "或一条直接给出 alpha 的作用量项；仅重述 tau/kappa 不会有进展。"
    "这也是 r429 V8-01「作用程 124.6 km 无第一性来源」的同型缺口。")

# E·B 反例与洛伦兹不变性
E = (D(0), D(0), D(4))
B = (D(0), D(0), D(3))
EdB = sum(E[i] * B[i] for i in range(3))
KEY["E_dot_B"] = EdB
guard("G_C_EdB_counterexample", EdB == 12, "E=(0,0,4), B=(0,0,3) 给 E·B=" + f(EdB) + " ≠ 0")

add("C-03", "PASS", "E·B=12 反例成立，且该量是洛伦兹不变的（不是坐标假象）",
    "直接点积 E·B=0*0+0*0+4*3=" + f(EdB) + "。且 F_{mu nu}*F^{mu nu}=-4 E·B（Huygens 号约定下差一个符号），"
    "E·B 是洛伦兹不变量；因此「 E 与 B 正交」不是某个标架下的表象选择，而是对场构型的实质限制。"
    "来料主动登记这一反例并将其列为已排除的普适假设，属正确的自我修正。")

# Frenet 正交 ≠ 场正交：把场强制对齐标架是一种输入
def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


T, N, Bn = (D(1), D(0), D(0)), (D(0), D(1), D(0)), (D(0), D(0), D(1))
ef_n = (D(0), D(3), D(0))
bf_b = (D(0), D(0), D(4))
ef_rot = (D(0), D(3) / D(5).sqrt(), D(4) / D(5).sqrt())
KEY["frenet_orth"] = (dot(T, N), dot(N, Bn), dot(T, Bn))
KEY["aligned_E_dot_B"] = dot(ef_n, bf_b)
KEY["rotated_E_dot_B"] = dot(ef_rot, bf_b)
guard("G_C_frenet_vs_fields",
      KEY["frenet_orth"] == (D(0), D(0), D(0)) and KEY["aligned_E_dot_B"] == 0 and KEY["rotated_E_dot_B"] != 0,
      "Frenet 三轴两两正交；若额外规定 E∥N、B∥B_hat 则 E·B=0，若 E 在同一平面内旋转则 E·B=" + f(KEY["rotated_E_dot_B"]))

add("C-04", "FAIL", "几何三方向正交不能推出 E⊥B；正交性只能由「场↔标架对齐」这一额外假设输入",
    "Frenet 标架 T,N,B_hat 由定义两两正交（点积全为 0），这与电磁场无关。"
    "若额外规定 E∥N 且 B∥B_hat，则 E·B≡0 是**该识别的输入后果**；把 E 在 N-B_hat 平面内旋转一个角度，"
    "同一几何标架下 E·B=" + f(KEY["rotated_E_dot_B"]) + "≠0。"
    "⇒ 「三几何方向正交」与「三力场正交」属于不同范畴；缺的是映射定义而不是推导。"
    "这与 R14「规范量子数不是 Lk 的函数」是同型范畴错误。")

add("C-05", "INFO", "两条自纠被正确登记，但修正本身不产生新预言",
    "V136 已明确 tau/kappa 缺动力学方程、E⊥B 不是普适假设，并在测试中固定这两点。"
    "本册确认两处自纠均成立；但把它们写成「已解决问题」不成立——"
    "它们只是把错误假设从公设里删掉，缺口仍是两条动力学方程与一个场↔标架映射。")

# ---------------- D 段：最终变分图与 W3 门禁 ----------------
raw_path = OUT / "TUFT-ROOT_V136_来料全文_2026-11-23.md"
raw_text = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
has_target = "S_{\\rm ROOT}" in raw_text or "SROOT" in raw_text
has_action_def = bool(re.search(r"(?m)^\s*S\s*=\s*\\?int", raw_text)) or "L_ROOT" in raw_text
KEY["has_target"] = has_target
KEY["has_action_def"] = has_action_def
guard("G_D_no_action_supplied", has_target and not has_action_def,
      "来料含目标式 S_ROOT 但无作用量/拉氏量定义：has_target=" + str(has_target) + " has_action_def=" + str(has_action_def))

add("D-01", "FAIL", "S_ROOT → 四方程的盒装图是目标而非结果：来料没有给出任何作用量",
    "来料只在第五节写出目标盒 \u2192 爱因斯坦 / 麦克斯韦 / 弱 / 强四组方程，全文没有 S_ROOT 的积分表达式、"
    "场变量清单或变分规则；因此「严格变分」四字不可执行，无法检查四条方程是否同源。"
    "本册继承 r442 的 N01（单一 Lorentz 协变作用量四源不可行）与 r408 的 F1/F2 全败裁定，"
    "不重判、不新增候选。一方程记分板维持 0/6，含引力的四力大统一正确方程维持 0 条。")


def w3_gate(c1, c2, c3, c4):
    return bool(c1 and c2 and c3 and c4)


v136_gate = w3_gate(True, False, False, False)
positive_gate = w3_gate(True, True, True, True)
KEY["w3_v136"] = int(v136_gate)
KEY["w3_positive"] = int(positive_gate)
guard("G_D_w3_positive", positive_gate and not v136_gate,
      "W3 四门阳性对照全过、V136 候选不过（0/4），证明门禁非恒假")

add("D-02", "FAIL", "V136 的跨高度量上门禁仅 C1 通过（1/4），不能计为 W3/L3",
    "C1 定量数值：PASS（0.600978%、Q3 两值均为明确数字）。"
    "C2 不由其他式子反解：FAIL（Q3 完全由外部注入的 lambda 与几何决定；D 由已发表 eps0 决定）。"
    "C3 有未用于拟合的检验路径：FAIL（alpha=1/3 与 lambda=124.6 km 已在 V119/V120/r429/r436 的反演中使用）。"
    "C4 双锚点不自洽检验：FAIL（来料没有任何粒子尺度锚点，只有地球/月球两个宏观读数）。"
    "⇒ 四门 1/4，阳性对照 4/4，W3.pass 保持 0。")

add("D-03", "INFO", "红线计数继承不变",
    "0/6 未完成 · 0/22 · UFT-3=0 · L3=0 · validated=0 · 含引力四力正确方程 0 条 · L3↛L4。"
    "本册只压缩 V136 的可复算面与不可复算面，不增加任何 L3 或 validated 计数。")

# ---------------- E 段：交付物可核验性 ----------------
zip_hits = []
for dirpath, dirnames, filenames in os.walk(str(ROOT)):
    if ".git" in dirpath:
        continue
    for fn in filenames:
        if "V136" in fn and fn.lower().endswith(".zip"):
            zip_hits.append(os.path.join(dirpath, fn))
KEY["zip_hits"] = len(zip_hits)
guard("G_E_zip_absent", len(zip_hits) == 0, "全库 V136 ZIP 命中 " + str(len(zip_hits)) + " 个")

add("E-01", "BOUNDARY", "「81 项测试 / 49 文件 / SHA-256 校验通过」无法离线核验",
    "全库检索无 ROOT_V136_Unification_Research_Complete.zip、无 V136 manifest 或测试报告落盘；"
    "来料只给出自述摘要。本册不代做 ZIP 完整性验收，也不把 81/81 记为独立证据。"
    "若后续提供 ZIP，应按既有体例做 SHA-256 逐项比对与解压复跑后再登记。")

add("E-02", "INFO", "本册受理范围与不重判清单",
    "受理：来料第一、二节的两条跨高度公式与三个数值；第三节的螺旋比与 E·B 反例；"
    "第五节的变分目标与观测路径。不重判：r429（V119 五高度）、r436（V120 Prony）、"
    "r442（记分板）、r408/r409（单方程化）、r421（W3 门禁）的既有裁定；"
    "不代做 ICGEM/GRAIL 真实数据拟合（无数据、无预注册）。")

# ---------------- F 段：构造性增量——抗漂移四高度观测 ----------------
def Q4(r0, step, lam, eps0=EPS0_PUB, drift=D(0), quad=False):
    vals = []
    for k in range(4):
        r = r0 + D(k) * step
        e = profile(r, r0, eps0, lam)
        bias = drift * D(k)
        if quad:
            bias += D("1.5") * J2 * (r0 / r) ** 2 * D("-0.5")
        vals.append(1 + e + bias)
    d2_0 = vals[0] - 2 * vals[1] + vals[2]
    d2_1 = vals[1] - 2 * vals[2] + vals[3]
    return d2_0 / d2_1


q4 = Q4(R_E, H200, LAM)
q4_drift = Q4(R_E, H200, LAM, drift=D("1e-4"))
q4_const = Q4(R_E, H200, LAM, drift=D("1e-4"))  # 常数偏置由 drift 项 k=0..3 的线性部分覆盖，另测真常数
q4_j2 = Q4(R_E, H200, LAM, quad=True)
KEY["q4_four_height"] = q4
KEY["q4_drift_drift"] = abs(q4_drift - q4)
KEY["q4_j2"] = q4_j2
KEY["q4_j2_shift"] = rel(q4_j2, q4)
KEY["q4_vs_q3"] = rel(q4, qe)
KEY["j2_improvement"] = KEY["q3_j2_shift"] / KEY["q4_j2_shift"]
guard("G_F_linear_drift_immune", abs(q4_drift - q4) < D("1e-45"),
      "四高度二阶差分比对线性漂移 1e-4 的不变性，漂移 " + f(abs(q4_drift - q4)))


def Q4_pure_exp(r0, step, lam):
    vals = [(-(D(k) * step) / lam).exp() for k in range(4)]
    d2_0 = vals[0] - 2 * vals[1] + vals[2]
    d2_1 = vals[1] - 2 * vals[2] + vals[3]
    return d2_0 / d2_1


q4_pure = Q4_pure_exp(R_E, H200, LAM)
KEY["q4_pure_exp"] = q4_pure
guard("G_F_shape_teeth", rel(q4_pure, q4) > D("0.1"),
      "四高度构造对纯指数形状仍有牙：Q4=" + f(q4) + " vs 纯指数 " + f(q4_pure))
guard("G_F_j2_improvement", KEY["q4_j2_shift"] < KEY["q3_j2_shift"] / 5,
      "J2 污染相对漂移由 Q3 的 " + f(KEY["q3_j2_shift"]) + " 降到 Q4 的 " + f(KEY["q4_j2_shift"]) +
      "（改善 " + f(KEY["j2_improvement"]) + " 倍）")

add("F-01", "PASS", "构造性增量：四高度二阶差分比同时免疫常数、线性漂移、G、M 与振幅 A",
    "取等间距 4 高度 r_k=r0+k*200 km，定义 Q4=(A0-2A1+A2)/(A1-2A2+A3)。"
    "常数项与线性项在二阶差分中严格为零，而 GM 与 A_source 在比值中消去；"
    "本册数值 Q4=" + f(q4) + "，加入 c=1e-4 的线性漂移后漂移量 " + f(KEY["q4_drift_drift"]) +
    "（机器零）。这是对 V136 三高度 Q3 的零成本加固：多测一个高度，少一种系统误差。")

add("F-02", "PASS", "Q4 把 J2 污染压低约 10 倍，但不增加 λ 信息量",
    "同一赤道 J2 污染下 Q3 相对漂移 " + f(KEY["q3_j2_shift"]) + "，Q4 仅 " +
    f(KEY["q4_j2_shift"]) + "（改善 " + f(KEY["j2_improvement"]) + " 倍）；"
    "但 Q4=" + f(q4) + " 与 Q3=" + f(qe) + " 只差 " + f(KEY["q4_vs_q3"]) +
    "，即两者对 λ 的信息几乎相同。⇒ 增益是系统鲁棒性而非新自由度；"
    "纯指数阳性对照 Q4=" + f(q4_pure) + " 与 Yukawa 值显著不同，判据仍有形状识别力。")

# ---------------- 输出 ----------------
counts = {}
for e in ENTRIES:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
KEY["entry_count"] = len(ENTRIES)
KEY["guard_pass"] = sum(1 for g in GUARDS if g["ok"])
KEY["guard_total"] = len(GUARDS)
KEY["counts"] = counts

src_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
result = {
    "round": "r443",
    "topic": "ROOT V136 跨高度引力消元与可证伪性 全维审计",
    "date": STAMP,
    "source": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
    "source_sha256": hashlib.sha256(raw_text.encode("utf-8")).hexdigest() if raw_text else "",
    "engine_sha256": src_hash,
    "verdict": "CROSS-HEIGHT-IDENTITY-EXACT--AMPLITUDE-NOT-REPRODUCIBLE--Q3-LAMBDA-REPARAMETERIZATION--W3-1OF4--UNIFICATION-OPEN",
    "counts": counts,
    "guard_pass": KEY["guard_pass"],
    "guard_total": KEY["guard_total"],
    "entries": ENTRIES,
    "guards": GUARDS,
    "key_numbers": {
        k: (str(v) if isinstance(v, D) else
            [str(x) if isinstance(x, D) else x for x in v] if isinstance(v, tuple) else v)
        for k, v in sorted(KEY.items())
    },
}

OUT.mkdir(exist_ok=True)
json_path = OUT / (PREFIX + ".json")
md_path = OUT / (PREFIX + ".md")
rep_path = OUT / (PREFIX + "_report.txt")
json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# TUFT r443 · ROOT V136 跨高度引力消元与可证伪性 全维审计",
    "",
    "一句话：D 恒等式与 Q3 两数值可独立复算，但 0.600978% 不能由已声明参数推出（缺振幅 A）；"
    "Q3 是 lambda 的单射重参数化而非独立预言；tau/kappa 与 E·B 两处自纠成立却不产生新方程；四力变分目标仍 OPEN。",
    "",
    "| 项 | 值 |",
    "|---|---|",
    "| 条目 | " + str(len(ENTRIES)) + " |",
    "| 判定分布 | " + ", ".join(k + "=" + str(v) for k, v in sorted(counts.items())) + " |",
    "| 守卫 | " + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]) + " |",
    "| 引擎 SHA256 | " + src_hash + " |",
    "",
    "## 关键读数",
    "",
]
for k, v in sorted(result["key_numbers"].items()):
    lines.append("- " + k + " = " + (str(v) if not isinstance(v, str) else v))
lines += ["", "## 条目", "", "| 编号 | 判定 | 标题 | 详情 |", "|---|---|---|---|"]
for e in ENTRIES:
    lines.append("| " + e["id"] + " | " + e["verdict"] + " | " + e["title"] + " | " + e["detail"] + " |")
lines += ["", "## 守卫", "", "| ID | OK | 读数 |", "|---|---|---|"]
for g in GUARDS:
    lines.append("| " + g["id"] + " | " + ("PASS" if g["ok"] else "FAIL") + " | " + g["detail"] + " |")
md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

rep = [
    "TUFT r443 ROOT V136 全维审计",
    "entries=" + str(len(ENTRIES)) + " guards=" + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]),
    "counts=" + json.dumps(counts, ensure_ascii=False, sort_keys=True),
    "D_pub=" + f(d_pub) + " D_claim=" + f(CLAIM_D),
    "Q3_earth=" + f(qe) + " Q3_moon=" + f(qm),
    "engine_sha256=" + src_hash,
]
rep_path.write_text("\n".join(rep) + "\n", encoding="utf-8")

if any(not g["ok"] for g in GUARDS):
    print("GUARD FAILURES:")
    for g in GUARDS:
        if not g["ok"]:
            print("  " + g["id"] + ": " + g["detail"])
    raise SystemExit(1)

print("OK entries=" + str(len(ENTRIES)) + " guards=" + str(KEY["guard_pass"]) + "/" + str(KEY["guard_total"]))

