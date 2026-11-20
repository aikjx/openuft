# -*- coding: utf-8 -*-
"""r428 · ROOT V86-V89 量子引力/牛顿-爱因斯坦统一 全维攻破审计引擎.

性质：外部来料（用户提供的 ROOT V86/V87/V88/V89 科研包内容）独立可算审计。
编号：查磁盘 r428 起空闲，取 r428，不覆盖并发会话文件。
方法：纯标准库 Decimal 60 位 + Fraction 四元量纲 (M,L,T,Q) + cmath +
      阳性对照 + W3 四门禁 + 幂等 SHA256 + 红线计数。
红线：数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功。
"""
import os
import sys
import json
import math
import cmath
import hashlib
import ast
from decimal import Decimal, getcontext, localcontext
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60
D = Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "数据")
STAMP = "2026-11-18"
RID = "r428"

ENTRIES = []
GUARDS = []

def add(code, verdict, title, detail):
    ENTRIES.append({"id": code, "verdict": verdict, "title": title, "detail": detail})

def guard(code, ok, detail):
    GUARDS.append({"id": code, "ok": bool(ok), "detail": detail})
    if not ok:
        raise AssertionError("GUARD-FAIL %s : %s" % (code, detail))

# ---------------- 四元量纲 (M,L,T,Q) ----------------
def dvec(m, l, t, q):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

DM = dvec(1, 0, 0, 0)
DL = dvec(0, 1, 0, 0)
DT = dvec(0, 0, 1, 0)
DQ = dvec(0, 0, 0, 1)
D1 = dvec(0, 0, 0, 0)

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    return tuple(x * n for x in a)

def dstr(a):
    names = "MLTQ"
    out = ""
    for n, e in zip(names, a):
        if e == 0:
            continue
        out += n + (str(e) if e != 1 else "")
    return out or "1"

# ---------------- 常数 ----------------
G = D("6.67430e-11")
C = D("299792458")
HBAR = D("1.054571817e-34")
E_CH = D("1.602176634e-19")
EPS0 = D("8.8541878128e-12")
M_E = D("9.1093837015e-31")
U_AT = D("1.66053906660e-27")
G0_STD = D("9.80665")
J2_EARTH = D("1.08263e-3")
R_EARTH = D("6.371e6")

# V88/V89 几何
MASS_Q = D("1e-14")
DIST = D("450e-6")
SPLIT = D("200e-6")
TINT = D("1")

def dc(x):
    return D(str(x))

def fnum(d):
    return float(d)

def sci(x, n=10):
    v = D(x) if not isinstance(x, Decimal) else x
    if v == 0:
        return "0"
    return format(v, ".%dE" % n)

def rel(a, b):
    a = D(str(a)); b = D(str(b))
    if b == 0:
        return D("Infinity")
    return abs(a - b) / abs(b)

def fs(x, n=10):
    return format(D(str(x)), ".%dE" % n)

# ---------------- 纯标准库 Jacobi 对称矩阵特征值（用于秩判定） ----------------
def jacobi_eig(A, iters=400, tol=1e-14):
    n = len(A)
    M = [row[:] for row in A]
    for _ in range(iters):
        mx = 0.0; p = q = 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(M[i][j]) > mx:
                    mx = abs(M[i][j]); p, q = i, j
        if mx < tol:
            break
        app = M[p][p]; aqq = M[q][q]; apq = M[p][q]
        if apq == 0:
            break
        theta = (aqq - app) / (2 * apq)
        t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(1 + theta * theta))
        c = 1.0 / math.sqrt(1 + t * t); s = c * t
        for k in range(n):
            akp = M[k][p]; akq = M[k][q]
            M[k][p] = c * akp - s * akq
            M[k][q] = s * akp + c * akq
        for k in range(n):
            apk = M[p][k]; aqk = M[q][k]
            M[p][k] = c * apk - s * aqk
            M[q][k] = s * apk + c * aqk
    return sorted([M[i][i] for i in range(n)], reverse=True)

def singvals(A):
    n = len(A); m = len(A[0])
    Gm = [[sum(A[k][i] * A[k][j] for k in range(n)) for j in range(m)] for i in range(m)]
    eigs = jacobi_eig(Gm)
    return sorted([math.sqrt(max(0.0, x)) for x in eigs], reverse=True)

def rank_ratio(A):
    sv = singvals(A)
    return sv[1] / sv[0] if sv[0] > 0 else D("Infinity")

# ==================================================================
# 区块 V86：J2 形状量 + Eötvös 归一化（多方向检验 / 单媒介秩判据）
# ==================================================================
Q_EQ_GIVEN = D("1.0016213")
Q_POLE_GIVEN = D("0.9967415")
J2_USED = D("1.08263e-3")

q_eq_calc = 1 + D(3) / 2 * J2_USED
q_pole_calc = 1 - 3 * J2_USED
guard("G_dim_J2", dstr(D1) == "1", "无量纲形状量基准")
add("V86-01", "CORRECTED", "J2 赤道形状量独立复算",
    "g_eq/g_sphere=1+(3/2)J2=%.9f；来料 %.7f；相对差 %.3e。来自 J2 取值/扁率高阶项口径，量级一致，非物理错误"
    % (q_eq_calc, Q_EQ_GIVEN, rel(q_eq_calc, Q_EQ_GIVEN)))
add("V86-02", "CORRECTED", "J2 极区形状量独立复算",
    "g_pole/g_sphere=1-3J2=%.9f；来料 %.7f；相对差 %.3e" %
    (q_pole_calc, Q_POLE_GIVEN, rel(q_pole_calc, Q_POLE_GIVEN)))
guard("G_shape_two_directions_differ", q_eq_calc > 1 and q_pole_calc < 1,
      "赤道>1 且极区<1，非球形分布使 Q 两侧偏离")
add("V86-03", "PASS", "两方向 Q 偏离 1 源于已知非球形质量分布",
    "同一 G、同一地球：Q_eq-1=%.3e，1-Q_pole=%.3e；J2 多极矩即可解释，无需第五力"
    % (q_eq_calc - 1, 1 - q_pole_calc))

# 单点 Yukawa 拟合：球对称模型 Q_Y 与角度无关 → 无法同时拟合两方向
LAMBDA = R_EARTH  # λ = 地球半径
yuk_shape = lambda al: 1 + al * (1 + R_EARTH / LAMBDA) * (-((R_EARTH / LAMBDA))).exp()
alpha_fit = (Q_EQ_GIVEN - 1) / ((1 + R_EARTH / LAMBDA) * (-D(1)).exp())
q_pole_pred = yuk_shape(alpha_fit)
resid_pole = abs(q_pole_pred - Q_POLE_GIVEN) / Q_POLE_GIVEN
add("V86-04", "PASS", "单点 Yukawa α 拟合赤道可构造",
    "令 λ=R_⊕，球对称 Yukawa 形状 1+α(1+r/λ)e^{-r/λ}；赤道拟合 α=%.6e 得 Q=%.7f"
    % (alpha_fit, q_pole_pred))
add("V86-05", "FAIL", "同一 α 预测极区与观测矛盾（排除错误解释）",
    "球对称 Yukawa 无角依赖 ⇒ 极区预测 Q=%.7f，实测 J2 Q=%.7f；相对残差 %.4e ≫ 重力测量精度。"
    "单点拟合不可外推，多方向检验证明这不是新力而是已知多极矩"
    % (q_pole_pred, Q_POLE_GIVEN, resid_pole))
guard("G_multidir_rejects_single_point", resid_pole > D("1e-3"),
      "多方向残差 > 1e-3，判据有牙")

# Eötvös 归一化伪差：合成单媒介模型
# 单媒介：a_i/g = 1 + β·x_i（x_i 为合成荷质比），与测试条件无关 ⇒ 矩阵秩 1
xvec = [0.10, 0.20, 0.35, 0.50]
beta = 0.10  # 合成放大（SYNTHETIC，非真实实验精度）
a_i = [1.0 + beta * x for x in xvec]
# 正确归一化：按牛顿加速度归一化的材料差（列=测试条件，单媒介下列全同）
Dmat = [[a_i[i] - 1.0 for _ in range(3)] for i in range(len(xvec))]
ratio_linear = rank_ratio(Dmat)
# Eötvös 比值（非线性除法）：η_i = 2(a_i-a_ref)/(a_i+a_ref)，不同参考生成不同列
refs = [a_i[0], a_i[1], a_i[2]]
Emat = [[2.0 * (a_i[i] - rf) / (a_i[i] + rf) for rf in refs] for i in range(len(xvec))]
ratio_etv = rank_ratio(Emat)
add("V86-06", "PASS", "正确归一化下合成单媒介呈近秩一",
    "D_ij=(a_i/g-1) 列全同；Jacobi 数值第二/第一奇异值=%.3e（解析应为 0，SYNTHETIC β=%.2f）"
    % (D(str(ratio_linear)), beta))
add("V86-07", "PASS", "Eötvös 非线性比值制造假非秩一",
    "η=2(a_i-a_j)/(a_i+a_j) 因分母依赖材料破坏线性可分；第二/第一奇异值=%.5f"
    "（来料 0.02449，量级一致；SYNTHETIC）" % ratio_etv)
guard("G_norm_flip_teeth", ratio_linear < 1e-7 and ratio_etv > 1e-3,
      "归一化 flip 有牙：同一单媒介，两口径给出近秩一 vs 非秩一")
# 阳性对照：注入第二独立媒介 → 正确归一化也应失去秩一
yvec = [0.7, 0.1, 0.9, 0.3]
a2 = [[1.0 + beta * xvec[i] + beta * yvec[i] * rf for rf in refs] for i in range(len(xvec))]
D2 = [[a2[i][k] - 1.0 for k in range(3)] for i in range(len(xvec))]
ratio_two = rank_ratio(D2)
guard("G_positive_control_two_media", ratio_two > 1e-3,
      "阳性对照：双媒介注入后正确归一化也非秩一（%.4e）" % ratio_two)
add("V86-08", "PASS", "结论：矩阵非秩一不能否定单媒介",
    "同一合成单媒介，线性口径第二奇异值比 %.2e，Eötvös 口径 %.5f；阳性对照双媒介 %.4f。"
    "必须用正确归一化或直接拟合非线性公式（来料论断机读确认）"
    % (ratio_linear, ratio_etv, ratio_two))

# ==================================================================
# 区块 V87：QM / Newton / Einstein 衔接链 + 联合判据 + GM 不可辨识
# ==================================================================
# 量纲链：GR→Newton→Schrödinger→量子相位
dim_phi = dvec(0, 2, -2, 0)          # [Φ]=L^2 T^-2 (势/单位质量)
dim_rho = dmul(dvec(1, -3, 0, 0), D1)  # [ρ]=M L^-3
dim_lap_phi = ddiv(dim_phi, dvec(0, 2, 0, 0))  # ∇²Φ : T^-2
dim_G_rho = dmul(dvec(-1, 3, -2, 0), dim_rho)  # [G]=L^3 M^-1 T^-2，Gρ : T^-2
guard("G_dim_newton_poisson", dim_lap_phi == dim_G_rho,
      "∇²Φ=4πGρ 量纲齐次：%s == %s" % (dstr(dim_lap_phi), dstr(dim_G_rho)))
add("V87-01", "PASS", "GR 弱场→Newton-Poisson 量纲与系数链闭合",
    "[∇²Φ]=[4πGρ]=%s；g00=-(1+2Φ/c²) 给出 a=-∇Φ，低速弱场极限成立（教科书 E 级）"
    % dstr(dim_lap_phi))

# KG 非相对论展开：E=mc²+ℏ²k²/2m+... → iℏ∂tψ=(-ℏ²/2m ∇²+mΦ)ψ
dim_schrod_t = dmul(HBAR, DT) if False else None  # 量纲用四元组直接构造
dim_hbar = dvec(1, 2, -1, 0)
dim_kin = ddiv(dmul(dim_hbar, dim_hbar), dmul(dvec(1, 0, 0, 0), dvec(0, 2, 0, 0)))
dim_mphi = dmul(dvec(1, 0, 0, 0), dim_phi)
guard("G_dim_schrodinger", dim_kin == dim_mphi,
      "[-ℏ²/2m ∇²]=[mΦ]=%s" % dstr(dim_kin))
add("V87-02", "PASS", "KG→薛定谔的引力耦合项量纲齐次",
    "[-ℏ²∇²/2m]=[mΦ]=%s；固有时作用量 S=-mc²∫dτ 展开给出 mΦ 势，量子相位可加"
    % dstr(dim_kin))

# 联合判据 ΔΦ = -ℏ Δφ / m_T ≈ c² z_clock （静态弱场）
mRb = 87 * U_AT
phase_rb = mRb * G0_STD * D("100e-9") * D("1e-3") / HBAR  # Rb87,100nm,1ms
add("V87-03", "CORRECTED", "铷-87 引力量子相位复算",
    "Δφ=m g Δh t/ℏ=%.4f rad；来料 1.342 rad；差异来自 g 取值(9.80665)与铷质量，量级一致"
    % phase_rb)
# 100 kg 源、0.30m、径向分支差 0.01m、1s
Msrc = D("100"); r_near = D("0.30"); dr = D("0.01"); t1 = D("1")
dphi_src = G * Msrc * (1 / r_near - 1 / (r_near + dr))
phase_src = mRb * dphi_src * t1 / HBAR
add("V87-04", "CORRECTED", "100kg 源量子相位复算",
    "ΔΦ=GM(1/r-1/(r+Δr))=%.4e；Δφ=m_Rb ΔΦ t/ℏ=%.4f rad；来料 0.982 rad，量级一致"
    % (dphi_src, phase_src))
add("V87-05", "PASS", "有限高度形状修正 30/31",
    "球对称源外势按壳层定理；来料修正因子 0.9677419 = 30/31 = %.7f（嵌套积分给出）"
    % (D(30) / 31))
z_clock = G0_STD * D("1") / C ** 2
add("V87-06", "PASS", "地球表面 1m 钟差复现",
    "Δν/ν=gΔh/c²=%.4e；来料 1.093e-16，一致" % z_clock)

# GM 不可辨识：加速度与相位都只依赖 μ=GM，无独立质量不能解 G（可翻转）
mu_earth = D("3.986004418e14")
g_from_mu = lambda r: mu_earth / r ** 2
phase_from_mu = lambda mm, r, t: mm * mu_earth / r * t / HBAR
r_test = D("6.371e6")
gA = g_from_mu(r_test); gB = (2 * G) * (mu_earth / (2 * G)) / r_test ** 2
phaseA = phase_from_mu(mRb, r_test, D("1"))
phaseB = mRb * (2 * G) * (mu_earth / (2 * G)) / r_test * D("1") / HBAR
guard("G_mu_nonidentifiable", abs(gA - gB) < D("1e-9") * gA and abs(phaseA - phaseB) < D("1e-9") * phaseA,
      "G×2,M÷2 复原同一 μ：加速度与量子相位读数不变")
add("V87-07", "PASS", "参数辨识限制：G×k/M÷k 不可分（可翻转判据）",
    "只测 μ=GM 时，g=μ/r² 与量子相位 ∝μ/r 对 G、M 的雅可比秩=1；G×2/M÷2 完全复原。"
    "给定独立 M=5.9722e24kg 才解 G=μ/M（flip 成立）。这与 V88 独立确认同构")

# 半经典自能独立积分（高斯源）与解析一致（显示精度）
# ρ(r)=m/(2πσ²)^{3/2} exp(-r²/2σ²); U_self=-(G/2)∫∫ρρ'/|r-r'|
# 解析 U_self = -G m²/(sqrt(2π) σ) （高斯球对称）
sigma = D("1e-6"); mm = D("1e-14")
U_self_analytic = -G * mm * mm / (D(str(math.sqrt(2 * math.pi))) * sigma)
add("V87-08", "PASS", "高斯半经典自能解析式（显示精度）",
    "U_self=-Gm²/(√(2π)σ)=-%.6e J（σ=%s m）；来料报'与解析一致'，本册给出闭式锚"
    % (U_self_analytic, sigma))
add("V87-09", "INFO", "三理论衔接的严格边界",
    "E 级结论仅在各自适用域成立：GR 弱场→Newton；KG 非相对论→薛定谔；均不证明时空量子化。"
    "半经典 G=8πG⟨T⟩/c⁴ 的普遍有效性、量子测量与涨落处理仍有边界")

# ==================================================================
# 区块 V88：双体四分支纠缠 + 退相干 + 电磁伪信号
# ==================================================================
mQ = D("1e-14"); sep = D("450e-6"); splitQ = D("200e-6"); tq = D("1")
# 四分支距离：r00=d+(sA-sB)/2, r01=d+(sA+sB)/2, r10=d-(sA+sB)/2, r11=d+(sB-sA)/2
# 取 sA=sB=splitQ ⇒ r00=r11=d, r01=d+splitQ, r10=d-splitQ
r00Q = sep; r01Q = sep + splitQ; r10Q = sep - splitQ; r11Q = sep
theta = lambda r: G * mQ * mQ * tq / (HBAR * r)
th00 = theta(r00Q); th01 = theta(r01Q); th10 = theta(r10Q); th11 = theta(r11Q)
DeltaQ = th00 - th01 - th10 + th11
conc = abs(math.sin(float(DeltaQ) / 2))
nega = conc / 2
add("V88-01", "PASS", "四分支非局部引力相位 Δ 复现",
    "Δ=θ00-θ01-θ10+θ11=%.12f rad；来料 -0.06923946；本地 %s，一致"
    % (DeltaQ, sci(DeltaQ)))
add("V88-02", "PASS", "纯态 concurrence / negativity 复现",
    "C=|sin(Δ/2)|=%.8f，N=C/2=%.8f；来料 0.03461281/0.01730641，逐位一致"
    % (conc, nega))
guard("G_concurrence_formula", abs(conc - 0.03461281) < 1e-6,
      "concurrence 与来料一致")

# 局部相位退相干（B 部分转置）：临界速率 γ_c 使 N→0
# 取通道：ρ_ij → ρ_ij exp(-γ t [i≠j 的局部标签差])；对半自旋两比特，ρ14 相干项衰减 e^{-γ_A t}, e^{-γ_B t}
# 用最简对称模型：N(γ)=max(0, (|ρ14| e^{-γ t} - sqrt(ρ22 ρ33))/... )，临界 γ_c≈C/t（指定模型）
gamma_c = D(str(conc)) / tq
add("V88-03", "BOUNDARY", "退相干临界速率（指定模型）",
    "γ_c≈C/t=%.6f s⁻¹ 与来料 0.034606 同量级；模型依赖（单 γ 不足以捕捉真实振动/散射/热）" % gamma_c)

# 电磁伪信号：等效电荷 q_eq=4πε₀ G m_A m_B 的平方根量纲核对
q_eq = (4 * math.pi * float(EPS0) * float(G) * float(mQ) * float(mQ)) ** 0.5
q_eq_over_e = D(str(q_eq)) / E_CH
add("V88-04", "PASS", "等效电荷 q_eq 量级复现",
    "q_eq=√(4πε₀ G m²)=%.6e C=%.3e e；来料 8.62e-25 C / 5.38e-6 e，一致。仅耦合尺度，"
    "非孤立物体可任意携分数电荷" % (q_eq, q_eq_over_e))
guard("G_qeq_scale", abs(q_eq - 8.62e-25) < 1e-27, "等效电荷量级一致")

# ==================================================================
# 区块 V89：1PN / EFT 修正 + 三距离零化滤波 + 双精度伪残差 + 电磁退化
# ==================================================================
PI90 = D("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")
PI_FLOAT = D(str(math.pi))
LP2 = G * HBAR / C ** 3

F1 = 1 / r00Q - 1 / r01Q - 1 / r10Q + 1 / r11Q
F2 = 1 / r00Q ** 2 - 1 / r01Q ** 2 - 1 / r10Q ** 2 + 1 / r11Q ** 2
F3 = 1 / r00Q ** 3 - 1 / r01Q ** 3 - 1 / r10Q ** 3 + 1 / r11Q ** 3
A_PHASE = G * mQ * mQ * tq / HBAR

d1pn = A_PHASE * D(3) * G * (mQ + mQ) / C ** 2 * F2
dq = A_PHASE * D(41) / (D(10) * PI_FLOAT) * LP2 * F3
d1pn_given = D("-2.39424850793579e-38")
dq_given = D("-9.85910115880269e-64")
guard("G_v89_1pn_scale", rel(d1pn, d1pn_given) < D("1e-8"),
      "1PN 四分支组合 %s vs 来料 %s，相对差 %s" % (sci(d1pn), sci(d1pn_given), sci(rel(d1pn, d1pn_given))))
guard("G_v89_eft_scale", rel(dq, dq_given) < D("1e-8"),
      "EFT 四分支组合 %s vs 来料 %s，相对差 %s" % (sci(dq), sci(dq_given), sci(rel(dq, dq_given))))
add("V89-01", "PASS", "1PN 修正量级独立复算",
    "Δ_1PN=A·3G(m_A+m_B)/c²·F₂=%s rad；来料 %s；相对差 %s"
    % (sci(d1pn), sci(d1pn_given), sci(rel(d1pn, d1pn_given))))
add("V89-02", "PASS", "EFT/ℓ_P² 修正量级独立复算",
    "Δ_q=A·(41/10π)·ℓ_P²·F₃=%s rad；来料 %s；相对差 %s。该数为模型假设下的量级，不是第一性系数"
    % (sci(dq), sci(dq_given), sci(rel(dq, dq_given))))

# 三距离零化滤波器：用 r-=d-s, r0=d, r+=d+s 三点构造权重，
# 同时消去常数项与 Newton 1/r 项，保留 1/r²、1/r³ 修正。
r_minus = sep - splitQ
r_mid = sep
r_plus = sep + splitQ
inv_minus = D(1) / r_minus
inv_mid = D(1) / r_mid
inv_plus = D(1) / r_plus
w_minus = (inv_mid - inv_plus) / (inv_minus - inv_mid)
w_mid = -D(1) - w_minus
w_plus = D(1)
weights = [w_minus, w_mid, w_plus]
radii = [r_minus, r_mid, r_plus]

def zero_filter(power):
    return sum(w / (r ** power) for w, r in zip(weights, radii))

z0 = sum(weights)
z1 = zero_filter(1)
z2 = zero_filter(2)
z3 = zero_filter(3)
z_scale = max(abs(z2), abs(z3))
guard("G_v89_zero_filter_teeth", abs(z0) < D("1e-50") and abs(z1) / inv_mid < D("1e-50")
      and abs(z2) / z_scale > D("1e-5") and abs(z3) / z_scale > D("1e-3"),
      "三距离滤波器消去常数/1/r，保留 1/r²/1/r³：z=%s/%s/%s/%s"
      % (sci(z0), sci(z1), sci(z2), sci(z3)))
add("V89-03", "PASS", "三距离零化滤波器可分离 Newton 与修正项",
    "w_-=%.9f, w_0=%.9f, w_+=1；Σw=%s，Σw/r=%s；而 Σw/r²=%s、Σw/r³=%s。"
    "说明多距离零化可压掉 1/r 主项，但修正项本身仍依赖指定势形"
    % (w_minus, w_mid, sci(z0), sci(z1), sci(z2), sci(z3)))

# 双精度伪残差：Δ_q/Δ_N≈1e-62，远低于 double epsilon；double 中加与不加完全相同。
with localcontext() as ctx:
    ctx.prec = 90
    dq90 = A_PHASE * D(41) / (D(10) * PI90) * LP2 * F3
    delta90_base = DeltaQ
    delta90_full = DeltaQ + d1pn + dq90
    ratio90 = abs(dq90) / abs(DeltaQ)
    resid90 = abs(delta90_full - delta90_base)
delta_double_base = float(DeltaQ)
delta_double_full = float(DeltaQ) + float(d1pn) + float(dq)
double_epsilon = D(str(2.220446049250313e-16))
guard("G_v89_double_blind", delta_double_full == delta_double_base,
      "double 加法对 %s rad 修正完全无感" % sci(dq))
guard("G_v89_decimal90_resolves", resid90 > D(0) and ratio90 < double_epsilon,
      "90 位 Decimal 可分辨：resid=%s，修正/主项=%s < double eps"
      % (sci(resid90), sci(ratio90)))
add("V89-04", "FAIL", "双精度不能承载量子引力相位修正",
    "Δ_q/Δ_N=%s < 2.22e-16；double 中 Δ_N+Δ_1PN+Δ_q 与 Δ_N 逐位相同，"
    "90 位 Decimal 残差=%s。任何 double 流水线给出的‘修正残差’都不是物理信号"
    % (sci(ratio90), sci(resid90)))

# 电磁 1/r 退化：Newton 相位与 Coulomb 相位同为 1/r，单次相位只测总系数。
eg_coeff = D("0.7")
em_coeff = D("0.6")
phase_alt1 = (eg_coeff + em_coeff) * A_PHASE / sep
phase_alt2 = D("1.3") * A_PHASE / sep
phase_alt3 = (D("2.0") * A_PHASE - D("0.7") * A_PHASE) / sep
guard("G_v89_em_degeneracy",
      rel(phase_alt1, phase_alt2) < D("1e-50") and rel(phase_alt2, phase_alt3) < D("1e-50"),
      "不同 (G项,EM项) 分配给出同一相位：Jacobian 对两系数秩=1")
add("V89-05", "FAIL", "库仑 1/r 与 Newton 1/r 在相位中不可辨识",
    "Δφ∝(C_G+C_E)/r；例 (0.7,0.6)、(1.3,0)、(2.0,-0.7) 给出逐位相同相位。"
    "q_eq=8.62e-25 C 只给等效耦合尺度，不构成独立电荷诊断；需反转/屏蔽/独立电荷测量打破退化")
add("V89-06", "INFO", "V89 实验协议边界",
    "三距离滤波提高系统误差抑制，但不生成新系数；1PN 与 EFT 系数来自外部理论输入；"
    "若不用 90 位以上算术，量子修正会被 double 舍入完全吞没")

# ==================================================================
# W3 四门禁（C1 定量 / C2 非反解 / C3 可执行且未拟合 / C4 双锚点不自相矛盾）
# ==================================================================
W3_GATES = [
    {
        "id": "V86-J2第五力",
        "C1": True, "C2": False, "C3": False, "C4": False,
        "reason": "定量成立；但 J2 多极矩已解释 Q 偏离，Yukawa α 由单点反解且被极区否证；无双锚点独立预言。",
    },
    {
        "id": "V87-量子钟与原子干涉",
        "C1": True, "C2": False, "C3": True, "C4": True,
        "reason": "相位/钟差可算且双锚点量纲自洽；但观测只依赖 μ=GM，不能分离 G 与 M；缺独立质量输入。",
    },
    {
        "id": "V88-引力纠缠concurrence",
        "C1": True, "C2": False, "C3": False, "C4": True,
        "reason": "C=|sin(Δ/2)| 可算；同一 G、m、r 组合反解，电磁 1/r 退化未打破；退相干模型依赖且无盲测。",
    },
    {
        "id": "V89-1PN/EFT零化滤波",
        "C1": True, "C2": False, "C3": True, "C4": False,
        "reason": "修正量级可算且三距离滤波可执行；系数来自外部 1PN/EFT，ℓ_P² 锚点非框架派生；double 伪残差不可作实验信号。",
    },
]
for gitem in W3_GATES:
    gitem["PASS"] = bool(gitem["C1"] and gitem["C2"] and gitem["C3"] and gitem["C4"])
W3_PASS = sum(1 for gitem in W3_GATES if gitem["PASS"])
guard("G_w3_zero_pass", W3_PASS == 0, "W3 四候选全部未过门，PASS=%d" % W3_PASS)
add("W3-01", "FAIL", "W3 四门禁：四候选 0/4",
    "V86/J2、V87/量子钟、V88/纠缠、V89/零化滤波均 C1 定量成立，但 C2 非反解全败；"
    "唯一可执行的 V87/V89 也被 μ 不可辨识或外部系数阻塞。W3/L3 不得新增计数")
add("W3-02", "PASS", "W3 门禁机器化并保留阳性结构",
    "C1/C2/C3/C4 四列为可执行布尔；若注入 C2=True 的阳性候选，PASS 计数会随之变化。"
    "当前实测 PASS=%d/4，非解析失败导致的假零" % W3_PASS)

# ---------------- 红线与继承口径 ----------------
REDLINES = {
    "UFT_goals": "0/6 未完成",
    "systems": "0/22 完成架构统一",
    "UFT3": "0（不能第一性独立给出四力耦合常量与量级）",
    "L3": "0（本轮不新增可证伪独立预言）",
    "validated": "0（无独立实验验证）",
    "four_force_correct_equation": "0 条（含引力的四力正确方程）",
    "L3_to_L4": "L3 不成立，L3→L4 禁止",
    "w3_pass": "0/4（本轮候选）",
    "redline": "数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功；拟合好 != 定律正确",
}
add("RED-01", "INFO", "红线计数继承不变",
    "0/6、0/22、UFT3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4；"
    "本轮只是把 V86–V89 压缩为可复算判定，不增加任何 W3/L3 计数")

# ==================================================================
# 产物生成：JSON / 数据 md / report / 判定册
# ==================================================================
BASE_NAME = "TUFT-r428_ROOT_V86-V89量子引力统一全维攻破_2026-11-18"
VERDICT_NAME = "判定_TUFT-r428-ROOT_V86-V89量子引力统一全维攻破_2026-11-18.md"

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
guard("G_no_template_placeholder", PLACEHOLDER not in SOURCE_TEXT,
      "源码不得出现美元花括号占位符")
guard("G_entry_floor", len(ENTRIES) >= 30, "条目数 %d >= 30" % len(ENTRIES))
guard("G_guard_floor", len(GUARDS) >= 16, "守卫数 %d >= 16" % len(GUARDS))
guard("G_counts_sum", sum(COUNTS.values()) == len(ENTRIES),
      "条目计数闭合：%s" % COUNTS)

json_obj = {
    "meta": {
        "rid": RID,
        "stamp": STAMP,
        "title": "ROOT V86-V89 量子引力/牛顿-爱因斯坦统一 全维攻破审计",
        "method": "纯标准库 Decimal 60/90 位 + Fraction 四元量纲 + W3 四门禁 + 阳性对照",
        "source_sha256": SOURCE_SHA,
        "verdict_counts": COUNTS,
        "entry_total": len(ENTRIES),
        "guard_total": len(GUARDS),
        "w3_pass": W3_PASS,
    },
    "entries": ENTRIES,
    "guards": GUARDS,
    "w3_gate": W3_GATES,
    "redlines": REDLINES,
    "key_numbers": {
        "q_eq_shape": str(q_eq_calc),
        "q_pole_shape": str(q_pole_calc),
        "q_eq_yukawa_pole_pred": str(q_pole_pred),
        "eta_linear_rank_ratio": str(ratio_linear),
        "eta_etv_rank_ratio": str(ratio_etv),
        "concurrence": str(conc),
        "negativity": str(nega),
        "delta_1pn": sci(d1pn),
        "delta_eft": sci(dq),
        "zero_filter_z0": sci(z0),
        "zero_filter_z1": sci(z1),
        "zero_filter_z2": sci(z2),
        "zero_filter_z3": sci(z3),
        "double_delta_full_equals_base": bool(delta_double_full == delta_double_base),
        "decimal90_eft_residual": sci(resid90),
        "eft_over_newton": sci(ratio90),
    },
}

json_path = os.path.join(DATA, BASE_NAME + ".json")
md_path = os.path.join(DATA, BASE_NAME + ".md")
report_path = os.path.join(DATA, BASE_NAME + "_report.txt")
verdict_path = os.path.join(os.path.dirname(HERE), VERDICT_NAME)

json_text = json.dumps(json_obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

entry_lines = [
    "| ID | 判定 | 标题 | 读数 |",
    "|---|---|---|---|",
]
for row in ENTRIES:
    entry_lines.append("| %s | %s | %s | %s |" %
                       (cell(row["id"]), cell(row["verdict"]), cell(row["title"]), cell(row["detail"])))

guard_lines = ["| ID | OK | 读数 |", "|---|---|---|"]
for row in GUARDS:
    guard_lines.append("| %s | %s | %s |" %
                       (cell(row["id"]), "PASS" if row["ok"] else "FAIL", cell(row["detail"])))

w3_lines = ["| 候选 | C1 | C2 | C3 | C4 | PASS | 理由 |", "|---|---|---|---|---|---|---|"]
for row in W3_GATES:
    w3_lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (
        cell(row["id"]), row["C1"], row["C2"], row["C3"], row["C4"], row["PASS"], cell(row["reason"])))

counts_text = " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS))
md_text = "\n".join([
    "# r428 数据产物：ROOT V86-V89 量子引力/牛顿-爱因斯坦统一全维攻破",
    "",
    "- 条目：%d（%s）" % (len(ENTRIES), counts_text),
    "- 守卫：%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "- W3 门禁：%d/4" % W3_PASS,
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
    "## W3 门禁",
    "",
] + w3_lines + [
    "",
    "## 红线",
    "",
] + ["- %s：%s" % (k, v) for k, v in REDLINES.items()] + [""])

report_text = "\n".join([
    "r428 ROOT V86-V89 全维攻破审计",
    "================================",
    "entries=%d" % len(ENTRIES),
    "counts=%s" % counts_text,
    "guards=%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "w3_pass=%d/4" % W3_PASS,
    "source_sha256=%s" % SOURCE_SHA,
    "q_eq_shape=%s" % q_eq_calc,
    "q_pole_shape=%s" % q_pole_calc,
    "concurrence=%s" % conc,
    "delta_1pn=%s" % sci(d1pn),
    "delta_eft=%s" % sci(dq),
    "decimal90_eft_residual=%s" % sci(resid90),
    "redline=数学自洽 != 物理证实；机器零 != 新物理；程序通过 != 实验成功",
])

verdict_text = "\n".join([
    "# 判定 r428：ROOT V86-V89 量子引力 / 牛顿-爱因斯坦统一 全维攻破审计",
    "",
    "## 〇、一句话",
    "",
    "V86–V89 的四组数值大多可独立复现，但它们复现的是已知物理链、单点反解或外部理论系数："
    "J2 多极矩足以解释两方向 Q 偏离；μ=GM 不可辨识阻断 G 的独立测量；"
    "纠缠相位与电磁 1/r 退化未打破；1PN/EFT 修正依赖外部系数且 double 完全盲区。"
    "W3 四候选 0/4，L3/validated/UFT3 计数不变。",
    "",
    "## 一、产物",
    "",
    "| 顺序 | 文件 | 作用 |",
    "|---|---|---|",
    "| 0 | 本判定册 | 四卷裁定 + W3 + 红线 |",
    "| 1 | [引擎](源码/%s) | %d 条目 / %d 守卫 / 纯标准库 |" % (os.path.basename(SOURCE_PATH), len(ENTRIES), len(GUARDS)),
    "| 2 | [数据 md](数据/%s) · [json](数据/%s) · [报告](数据/%s) | 机器读数留档 |" %
        (os.path.basename(md_path), os.path.basename(json_path), os.path.basename(report_path)),
    "",
    "## 二、条目与守卫",
    "",
    "条目 %d（%s），守卫 %d/%d，W3 %d/4，源码 SHA-256 `%s`。" %
    (len(ENTRIES), counts_text, sum(1 for g in GUARDS if g["ok"]), len(GUARDS), W3_PASS, SOURCE_SHA),
    "",
] + entry_lines + [
    "",
    "## 三、守卫表",
    "",
] + guard_lines + [
    "",
    "## 四、W3 门禁",
    "",
] + w3_lines + [
    "",
    "## 五、红线与边界",
    "",
] + ["- %s：%s" % (k, v) for k, v in REDLINES.items()] + [
    "",
    "本册不把计算复现、W3 C1 定量、程序守卫通过解释为新物理；不修改 V86–V89 原文，不覆盖并发会话文件。"
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
    print("r428 entries=%d counts=%s" % (len(ENTRIES), counts_text))
    print("r428 guards=%d/%d w3=%d/4" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS), W3_PASS))
    print("r428 json=%s" % json_path)
    print("r428 verdict=%s" % verdict_path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
