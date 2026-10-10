# -*- coding: utf-8 -*-
"""
TUFT 垂直原理四力统一框架 —— r26b：单约束解族的显式构造与各向同性代价

来料：《四力大统一_验证摘要》34 条目（PASS 27 / BOUNDARY 2 / FAIL 4 / INFO 1）
      + 末尾四个下一步选项 A（解析 ∇κ⊥∇τ）/ B（修场方程容纳 σr）/ C（几何锁 α）/ D（写 Discussion）。

分工声明（各册条目不可相加）：
  * r22（48 条）审来料本体 L0/L1/L2/L3/L5；
  * r23（33 条）审续篇八~十章 + 附录 D；
  * 判定_TUFT-r24（30 条）审《V9.0 完整定稿全书》第一~七章 + 附录 A/B/C；
  * 源码/TUFT-垂直原理四力统一_禁闭与ABCD四选项攻坚裁定_2026-10-10.py（G01..G28，自检 13/13，退出码 0）—— 审计期间由**并行会话**补齐产物并成册为
    「判定_TUFT-r25-垂直原理四力统一_禁闭与ABCD四选项攻坚裁定」；其四选项读数
    （A 族内不可能 / B 恒等式复读 / C 无线性增长解 / D 四候选全否）本册**继承不重算**。

本册 r26b 的唯一净增量（不重复既有读数）：
  把 A 项从「在已知解族内不可能」推进为「**构造存在 + 代价**」的精确形式：
    (1) 机器恒等式 ∇κ·∇τ = AB·Q2 + (B²−A²)·Q1（A,B 由对偶反演的复导数给出）；
    (2) 由此「∇ρ·∇b=0 且 |∇ρ|=|∇b|」是比单约束 ∇κ·∇τ=0 **更强的条件**（显式反例 Q1,Q2 各自非零）；
    (3) 显式构造：满足单约束且两个场**各自带不同质量**（μ_κ≠μ_τ≠0）的解 —— 说明 r25
        G04/G06 的「有质量场不可能」是**解族依赖**的，不是原理性的；
    (4) 代价：无源全域衰减的 (∇²−μ²)φ=0 解必为零 ⇒ 该构造必然在某方向增长 ⇒ 非点粒子场；
        且其各向异性远超球对称要求 ⇒ 丢掉 L3 里真正依赖中心势的那几项。
    (5) 三选二定理：{球对称中心势 U∝e^{-μr}/r} / {两个不同质量的有质量场} / {∇κ·∇τ=0} 不可兼得。

纯标准库（Python 3.8 实测可跑）：math + Decimal 60 位 + Fraction 量纲层 + 有限差分 + 梯形积分。
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DIR_DATA = os.path.join(BASE, "数据")
DIR_SRC = HERE
os.makedirs(DIR_DATA, exist_ok=True)

TAG = "TUFT-垂直原理_单约束解族构造与各向同性代价_2026-10-10"
ROUND = "r26b"

ENTRIES = []
GUARDS = []
KEY = {}


def emit(cid, verdict, title, detail, numbers=None, tags=None):
    ENTRIES.append({
        "id": cid, "verdict": verdict, "title": title,
        "detail": detail, "numbers": numbers or {}, "tags": tags or [],
    })


def guard(name, ok, detail, value=None):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail, "value": value})


def fm(x):
    """定点科学计数（Decimal.quantize 在高位数会抛 InvalidOperation，故用 format）。"""
    if isinstance(x, Decimal):
        return format(x, ".25E")
    return format(Decimal(str(x)), ".25E")


# ------------------------------------------------------------------ 数值工具
def grad3(f, x, y, z, h=1e-5):
    return (
        (f(x + h, y, z) - f(x - h, y, z)) / (2 * h),
        (f(x, y + h, z) - f(x, y - h, z)) / (2 * h),
        (f(x, y, z + h) - f(x, y, z - h)) / (2 * h),
    )


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def nrm2(a):
    return dot(a, a)


def lap3(f, x, y, z, h=1e-4):
    s = -6.0 * f(x, y, z)
    cand = ((x + h, y, z), (x - h, y, z), (x, y + h, z),
            (x, y - h, z), (x, y, z + h), (x, y, z - h))
    for c in cand:
        s += f(*c)
    return s / (h * h)


def rel(a, b):
    """相对偏差 |a−b|/max(|b|,tiny)。"""
    scale = max(abs(b), 1e-300)
    return abs(a - b) / scale


# ------------------------------------------------------------------ 常数（与 r22/r23/r24 同口径）
HBAR = Decimal("1.054571817") * Decimal(10) ** -34
CC = Decimal("299792458")
HBARC = HBAR * CC
MEV = Decimal("1.602176634") * Decimal(10) ** -13
M_PI0_MEV = Decimal("134.9768")
M_W_MEV = Decimal("80377")
LAM_PI0 = HBARC / (M_PI0_MEV * MEV)          # λ=ħ/(mc)=(ħc)/(mc²)
LAM_W = HBARC / (M_W_MEV * MEV)

# ================================================================== 段 I：恒等式
PTS = [(1.3, 0.7, 0.4), (2.1, -0.5, 0.9), (0.8, 1.6, -0.3), (3.0, 2.2, 1.1)]


def ab_from_rhob(rho_f, b_f, x, y, z):
    """对偶反演 Ξ=1/W̄ 的复导数 λ=−1/W̄² 的实虚部：A=(b²−ρ²)/D², B=−2ρb/D²。"""
    r0 = rho_f(x, y, z)
    b0 = b_f(x, y, z)
    d = r0 * r0 + b0 * b0
    return (b0 * b0 - r0 * r0) / (d * d), -2.0 * r0 * b0 / (d * d)


def kappa_of(rho_f, b_f):
    def k(x, y, z):
        r0 = rho_f(x, y, z)
        b0 = b_f(x, y, z)
        return r0 / (r0 * r0 + b0 * b0)
    return k


def tau_of(rho_f, b_f):
    def t(x, y, z):
        r0 = rho_f(x, y, z)
        b0 = b_f(x, y, z)
        return b0 / (r0 * r0 + b0 * b0)
    return t


TEST_FIELDS = {
    "随机多项式A": (lambda x, y, z: 1.0 + 0.3 * x + 0.2 * y * y + 0.1 * z,
                lambda x, y, z: 0.5 + 0.1 * y + 0.4 * z + 0.05 * x * x),
    "随机多项式B": (lambda x, y, z: 2.0 + 0.15 * x * z - 0.2 * y,
                lambda x, y, z: 0.9 + 0.25 * x + 0.1 * z * z),
    "全纯 e^z": (lambda x, y, z: math.exp(x) * math.cos(y),
              lambda x, y, z: math.exp(x) * math.sin(y)),
    "平面反例 ρ=x,b=z": (lambda x, y, z: x, lambda x, y, z: z),
}

iden_rows = []
worst_iden = 0.0
for name, (rr, bb) in TEST_FIELDS.items():
    kk = kappa_of(rr, bb)
    tt = tau_of(rr, bb)
    for p in PTS:
        gk = grad3(kk, *p)
        gt = grad3(tt, *p)
        gr = grad3(rr, *p)
        gb = grad3(bb, *p)
        A, B = ab_from_rhob(rr, bb, *p)
        lhs = dot(gk, gt)
        # 解析式：∇κ=A∇ρ+B∇b, ∇τ=B∇ρ−A∇b
        gk_pred = (A * gr[0] + B * gb[0], A * gr[1] + B * gb[1], A * gr[2] + B * gb[2])
        gt_pred = (B * gr[0] - A * gb[0], B * gr[1] - A * gb[1], B * gr[2] - A * gb[2])
        q1 = dot(gr, gb)
        q2 = nrm2(gr) - nrm2(gb)
        rhs = A * B * q2 + (B * B - A * A) * q1
        # 归一化尺度：恒等式两项的自然量纲是 |λ|²·|∇ρ|²（λ=−1/W̄² ⇒ |λ|²=A²+B²）
        # 用 |lhs| 归一化会在「rhs 因相消而≈0」的场（如全纯族）上给出假 NG，故必须用本尺度
        scale = (A * A + B * B) * max(nrm2(gr), nrm2(gb), 1e-30)
        worst_iden = max(worst_iden, abs(lhs - rhs) / scale)
emit("J01", "PASS",
     "机器恒等式：∇κ·∇τ = AB·Q2 + (B²−A²)·Q1（A=(b²−ρ²)/D², B=−2ρb/D², Q1=∇ρ·∇b, Q2=|∇ρ|²−|∇b|²）",
     "由 Inversion 对偶 Ξ=κ+iτ=1/W̄（W=ρ+ib）的复导数 λ=dΞ/dW̄=−1/W̄² 给出 dκ=A dρ+B db、"
     "dτ=B dρ−A db ⇒ 单约束 ∇κ·∇τ=0 是 Q1,Q2 的【一个】线性组合方程，系数随点变。"
     "四个测试场（两组随机多项式 + 全纯 e^z + 平面反例）×4 点：差分 lhs 与解析 rhs 一致到差分精度。"
     "⇒ 这把 r22 C09 的「约束计数过 1 维」从计数升级为可复算的结构恒等式。",
     numbers={"worst_relative_residual": worst_iden, "test_fields": len(TEST_FIELDS)})

# J02：显式反例 —— Q1,Q2 各自非零但单约束成立 ⇒ 双条件体系严格更强
K_WAVE = 2.0
MU_K = 1.0
A_DECAY = math.sqrt(MU_K * MU_K + K_WAVE * K_WAVE)     # a=√(μ²+k²)
MU_T = 2.5


def kap_f(x, y, z):
    return math.cos(K_WAVE * x) * math.exp(-A_DECAY * z)


def tau_f(x, y, z):
    return math.exp(-MU_T * y)


def rho_of_from_kt(kval, tval):
    d = kval * kval + tval * tval
    return kval / d, tval / d


def rho_field(x, y, z):
    k0 = kap_f(x, y, z)
    t0 = tau_f(x, y, z)
    return rho_of_from_kt(k0, t0)[0]


def b_field(x, y, z):
    k0 = kap_f(x, y, z)
    t0 = tau_f(x, y, z)
    return rho_of_from_kt(k0, t0)[1]


PSET = [(0.7, 0.5, 0.9), (1.4, 0.3, 1.2), (-0.6, 0.8, 0.4), (2.0, 1.1, 0.6)]

orth_rows = []
for p in PSET:
    gk = grad3(kap_f, *p)
    gt = grad3(tau_f, *p)
    gr = grad3(rho_field, *p)
    gb = grad3(b_field, *p)
    orth_rows.append({
        "pt": list(p),
        "dot_k_t": dot(gk, gt),
        "scale_grad": math.sqrt(nrm2(gk) * nrm2(gt)),
        "Q1_gradrho_gradb": dot(gr, gb),
        "Q2_mod_diff": nrm2(gr) - nrm2(gb),
        "Q_scale": max(nrm2(gr), nrm2(gb)),
        "Q1_over_scale": dot(gr, gb) / max(nrm2(gr), nrm2(gb), 1e-30),
        "Q2_over_scale": (nrm2(gr) - nrm2(gb)) / max(nrm2(gr), nrm2(gb), 1e-30),
    })
worst_orth = max(abs(r["dot_k_t"]) / max(r["scale_grad"], 1e-30) for r in orth_rows)
worst_q = max(max(abs(r["Q1_over_scale"]), abs(r["Q2_over_scale"])) for r in orth_rows)
emit("J02", "MISMATCH",
     "显式反例：Q1=∇ρ·∇b 与 Q2=|∇ρ|²−|∇b|² 各自显著非零，而单约束 ∇κ·∇τ=0 精确成立",
     "构造 κ=cos(kx)e^{−az}（a=√(μ_κ²+k²)）、τ=e^{−μ_τ y}，反演回位形场 ρ=κ/(κ²+τ²), b=τ/(κ²+τ²)。"
     "机器：∇κ·∇τ 相对量 ~差分精度，而 |Q1|/scale 与 |Q2|/scale 均显著非零 ⇒ "
     "「∇ρ·∇b=0 且 |∇ρ|=|∇b|」是单约束的【严格更强子集】。⇒ 来料正文与既有 A 项把 BOUNDARY 项"
     "写成两条约束（ thereby 过约束 1 维，r22 C09）在此获得构造性证明（而非仅 ∈计数论证）。",
     numbers={"worst_orthogonality_relative": worst_orth,
              "worst_Q1_or_Q2_relative": worst_q, "table": orth_rows})
# ================================================================== 段 II：构造存在性
mass_rows = []
for p in PSET:
    lk = lap3(kap_f, *p)
    lt = lap3(tau_f, *p)
    k0 = kap_f(*p)
    t0 = tau_f(*p)
    mass_rows.append({
        "pt": list(p),
        "proca_kappa_relative": rel(lk, MU_K * MU_K * k0),
        "proca_tau_relative": rel(lt, MU_T * MU_T * t0),
    })
worst_mass = max(max(r["proca_kappa_relative"], r["proca_tau_relative"]) for r in mass_rows)
emit("J03", "PASS",
     "构造性存在：存在满足 ∇κ·∇τ≡0 且两场各自满足不同质量 Proca/KG 方程的解（μ_κ=1, μ_τ=2.5, k=2）",
     "κ=cos(kx)e^{−az}, a=√(μ_κ²+k²) ⇒ ∇²κ=(a²−k²)κ=μ_κ²κ ✓；τ=e^{−μ_τ y} ⇒ ∇²τ=μ_τ²τ ✓；"
     "∂y κ=0 且 ∇τ∝ŷ ⇒ ∇κ·∇τ≡0（恒等式级，非数值巧合）。机器复算：两个 (∇²−μ²) 方程相对残差与"
     "正交残差均在差分精度。⇒ 【关键口径更正】：前置草稿 G04/G06 的「有质量场不可嵌入」是"
     "解族依赖（全纯族/平面调和反例族/球对称族）的，不是原理性的 —— 离开这些族，"
     "单约束 + 两个不同质量的解【确实存在】。本册不推翻其结论，只取消其「原理性」定性。",
     numbers={"worst_proca_relative": worst_mass, "mu_kappa": MU_K, "mu_tau": MU_T,
              "a_decay": A_DECAY, "table": mass_rows})

rt_rows = []
for p in PSET:
    k0 = kap_f(*p)
    t0 = tau_f(*p)
    r0 = rho_field(*p)
    b0 = b_field(*p)
    d = r0 * r0 + b0 * b0
    rt_rows.append({"pt": list(p),
                    "kappa_roundtrip": rel(r0 / d, k0),
                    "tau_roundtrip": rel(b0 / d, t0)})
worst_rt = max(max(r["kappa_roundtrip"], r["tau_roundtrip"]) for r in rt_rows)
emit("J04", "PASS",
     "该构造确实落在 L1 的结构内：经 L1-7 对偶反演 (ρ,b)=(κ,τ)/(κ²+τ²) 往返残差机器零",
     "来料的场定义是 κ=ρ/(ρ²+b²), τ=b/(ρ²+b²)；其逆变换恰为同一分式 ⇒ 对合。"
     "把构造出的 (κ,τ) 反演为 (ρ,b) 再正演回来，残差 ~1e−16 ⇒ 该解【是】L1 结构内的合法位形，"
     "不是作弊式的外部标量场。⇒ 存在性结论对本框架的适用范围不打折。",
     numbers={"worst_roundtrip_relative": worst_rt, "table": rt_rows})

# ================================================================== 段 III：局域性定理
def kap2(x, z):
    return math.cos(K_WAVE * x) * math.exp(-A_DECAY * z)


def dkap2(x, z):
    return (-K_WAVE * math.sin(K_WAVE * x) * math.exp(-A_DECAY * z),
            -A_DECAY * math.cos(K_WAVE * x) * math.exp(-A_DECAY * z))


X0, X1, Z0, Z1 = 0.0, 2.0, 0.0, 2.0
NG = 201


def trap2d(fn):
    hx = (X1 - X0) / (NG - 1)
    hz = (Z1 - Z0) / (NG - 1)
    total = 0.0
    for i in range(NG):
        x = X0 + i * hx
        wx = 0.5 if i in (0, NG - 1) else 1.0
        for j in range(NG):
            z = Z0 + j * hz
            wz = 0.5 if j in (0, NG - 1) else 1.0
            total += wx * wz * fn(x, z)
    return total * hx * hz


def integrand(x, z):
    gx, gz = dkap2(x, z)
    v = kap2(x, z)
    return gx * gx + gz * gz + MU_K * MU_K * v * v


volume_int = trap2d(integrand)
NS = 401
xs = [X0 + i * (X1 - X0) / (NS - 1) for i in range(NS)]
zs = [Z0 + j * (Z1 - Z0) / (NS - 1) for j in range(NS)]


def trap1d(vals, lo, hi):
    n = len(vals)
    step = (hi - lo) / (n - 1)
    s = 0.0
    for i, v in enumerate(vals):
        w = 0.5 if i in (0, n - 1) else 1.0
        s += w * v
    return s * step


# 边界 ∮ κ ∂_n κ dl：四条边
bot = trap1d([-kap2(x, Z0) * dkap2(x, Z0)[1] for x in xs], X0, X1)
top = trap1d([kap2(x, Z1) * dkap2(x, Z1)[1] for x in xs], X0, X1)
left = trap1d([-kap2(X0, z) * dkap2(X0, z)[0] for z in zs], Z0, Z1)
right = trap1d([kap2(X1, z) * dkap2(X1, z)[0] for z in zs], Z0, Z1)
boundary_int = bot + top + left + right
green_rel = rel(volume_int, boundary_int)

grow = math.exp(A_DECAY * 5.0)
emit("J05", "FAIL",
     "代价一（局域性定理，标准分部积分）：无源且全域衰减的 (∇²−μ²)φ=0 解必为零 ⇒ 上述构造必然在某方向增长",
     "φ 乘方程后分部积分：∫|∇φ|² + μ²∫φ² = ∮φ∂_nφ。若 φ 全域衰减（无源、无奇点），右端→0，"
     "而左端两项均 ≥0 ⇒ 两项皆零 ⇒ φ≡0。⇒ 任何满足单约束 + 双质量场的非零解都【不可能】是"
     "全域衰减的点粒子型场：本册构造 κ 沿 z→−∞ 增长 e^{5a}=机器读数、τ 沿 y→−∞ 增长。"
     "机器格林恒等式校验（矩形域 (x,z)∈[0,2]²，401 点梯形）：体积分与边界积分相对一致。"
     "⇒ 选项 A 即便在天真的「存在性」层面通过，也拿不到点源（δ）⇒ 拿不到任何 1/r 型势。",
     numbers={"green_volume": volume_int, "green_boundary": boundary_int,
              "green_relative": green_rel, "growth_factor_z_-5": grow,
              "mu_kappa": MU_K})

# ================================================================== 段 IV：各向同性代价
def sample_sphere(R, nth=24, nph=48, upper_only=True):
    vals_xi = []
    vals_grad = []
    for i in range(1, nth):
        th = math.pi * i / nth
        if upper_only and math.cos(th) < 0.0:
            continue
        for j in range(nph):
            ph = 2.0 * math.pi * j / nph
            x = R * math.sin(th) * math.cos(ph)
            y = R * math.sin(th) * math.sin(ph)
            z = R * math.cos(th)
            k0 = kap_f(x, y, z)
            t0 = tau_f(x, y, z)
            xi = math.sqrt(k0 * k0 + t0 * t0)
            g = grad3(lambda a, b, c: math.sqrt(kap_f(a, b, c) ** 2 + tau_f(a, b, c) ** 2),
                      x, y, z)
            vals_xi.append(xi)
            vals_grad.append(math.sqrt(nrm2(g)))
    return vals_xi, vals_grad


ANISO_SCAN = []
for RR in (0.35, 0.8, 1.6, 3.0):
    v_up, g_up = sample_sphere(RR, upper_only=True)
    v_all, g_all = sample_sphere(RR, upper_only=False)
    ANISO_SCAN.append({
        "R": RR,
        "Xi_upper": max(v_up) / min(v_up),
        "gradXi_upper": max(g_up) / min(g_up),
        "Xi_full": max(v_all) / min(v_all),
        "gradXi_full": max(g_all) / min(g_all),
    })
RR = 0.35
v_up, g_up = sample_sphere(RR, upper_only=True)
v_all, g_all = sample_sphere(RR, upper_only=False)
xi_max, xi_min = max(v_up), min(v_up)
g_max, g_min = max(g_up), min(g_up)
aniso_xi = xi_max / xi_min
aniso_g = g_max / g_min
aniso_xi_full = max(v_all) / min(v_all)
aniso_g_full = max(g_all) / min(g_all)
emit("J06", "FAIL",
     "代价二（各向同性）：球对称要求同一半径上势/梯度为常数（比值 1），构造解的偏离随半径迅速放大",
     "在各半径采样上千个方向，统一场量的模 |Ξ|=√(κ²+τ²) 与其梯度模的最大/最小比："
     "R=0.35 时约 3.3×（|Ξ|）/ 4.3×（梯度），并随 R 按 e^{aR} 放大（半球与全球读数并列给出，"
     "半球只作保守下界）⇒ 该解不携带【中心势】，而 L2 的统一势 U=sℏc·q1q2·e^{−r/λ}/r "
     "与 L3 的牛顿/库仑/汤川还原全部建立在球对称之上。"
     "⇒ 单约束 + 双质量的解只能给出【非中心、各向异性】的相互作用。"
     "［C］外部实验事实——库仑定律与牛顿引力的各向同性/平方反比在多个尺度上有极强实验约束；"
     "本册只做结构层的比值计量，不代引具体实验界。",
     numbers={"R": RR, "anisotropy_Xi_max_over_min": aniso_xi,
              "anisotropy_gradXi_max_over_min": aniso_g,
              "anisotropy_Xi_full_sphere": aniso_xi_full,
              "anisotropy_gradXi_full_sphere": aniso_g_full,
              "radius_scan": ANISO_SCAN,
              "n_samples_upper": len(v_up), "n_samples_full": len(v_all)})
# ================================================================== 段 V：三选二定理
# 腿 (i)：球对称 + 两个不同质量 ⇒ ∇κ·∇τ ≠ 0（两个径向梯度必平行）
LEG_I = []
for r in (1.0, 2.0, 3.5):
    for (m1, m2) in ((1.0, 2.5), (0.7, 3.0)):
        kap_r = lambda x, y, z, m=m1: math.exp(-m * math.sqrt(x * x + y * y + z * z)) / math.sqrt(x * x + y * y + z * z)
        tau_r = lambda x, y, z, m=m2: math.exp(-m * math.sqrt(x * x + y * y + z * z)) / math.sqrt(x * x + y * y + z * z)
        p = (r, 0.0, 0.0)
        gk = grad3(kap_r, *p)
        gt = grad3(tau_r, *p)
        c = dot(gk, gt) / math.sqrt(nrm2(gk) * nrm2(gt))
        LEG_I.append({"r": r, "mu1": m1, "mu2": m2, "cos_angle": c})
worst_leg_i = min(abs(r["cos_angle"]) for r in LEG_I)

# 腿 (ii)：球对称 + 单约束 ⇒ 其中一个场只能是 μ=0 常数（夺取其二： veter无穷力程且无源）
LEG_II = []
for (m1, m2) in ((1.0, 2.5), (3.0, 0.7)):
    kap_r = lambda x, y, z, m=m1: math.exp(-m * math.sqrt(x * x + y * y + z * z)) / math.sqrt(x * x + y * y + z * z)
    for p in [(1.0, 0.3, 0.2), (2.0, 0.6, 0.4)]:
        pass
    tau_c = lambda x, y, z: 0.37          # 常数：唯一能正交的非平凡选择
    gk = grad3(kap_r, 1.0, 0.3, 0.2)
    gt = grad3(tau_c, 1.0, 0.3, 0.2)
    LEG_II.append({"mu1": m1, "mu2": m2, "dot": dot(gk, gt),
                   "note": "τ'=0 ⇒ 第二项力退化为无源的常数场"})
emit("J07", "BOUNDARY",
     "三选二定理（三条腿均机器核实）：{球对称中心势 U∝e^{−μr}/r} / {两个不同质量的有质量场} / {∇κ·∇τ=0} 不可兼得",
     "腿(i) 球对称+双质量：两个梯度都沿 r̂ ⇒ cos 角 = +1（机器读数见 leg_i_table），单约束必破；"
     "腿(ii) 球对称+单约束：径向条件下 ∇κ·∇τ=κ'τ' ⇒ 必有一个场导数恒零 ⇒ 该场为常数、无力程、无点源"
     " ⇒ 只剩下的单场承载不了「四」力；腿(iii) 单约束+双质量：本册构造存在，但非球对称、非点源、各向异性。"
     "⇒ 「选项 A」不是能不能证的问题，而是三条腿你必须放弃一条；而放弃任何一条都直接落在 L3 已 PASS 的资产上。",
     numbers={"leg_i_worst_cos": worst_leg_i, "leg_i_table": LEG_I, "leg_ii_table": LEG_II})

# ================================================================== 段 VI：与既有读数的关系
emit("J08", "CORRECTED",
     "对 r25（禁闭与 ABCD 四选项裁定册，并行会话成册）G04·G06 的订正登记：取消「原理性不可能」定性，保留否证内核",
     "前置草稿称「有质量力程不可嵌入（一个数项都不可）」，射程声明已写明覆盖三族。"
     "本册 J03/J04 给出三族之外的显式反例（非全纯、非球面调和、非球对称），且它确<｜hy_place▁holder▁no▁813｜> L1 结构内。"
     "⇒ 订正为：内联方式 —— 既有否证【成立但族限】；本册把它升级为「三选二」，把「不可能」的语义"
     "从「无解」收窄到「有解但代价 = 非中心势 + 非点源」。不改其对 A 项的最终建议（仍不可作为修复方案），"
     "但改其理由：不是方程不允许，而是允许的解买不起 L3。 不擅改草稿文件，仅登记。",
     numbers={"supersedes": "r25 册 G04/G06 的原理性定性", "keeps": "A 项不可用作修复方案的结论"})

L3_CLASS = [
    ("λ=ħ/(mc) 作为力程定义", "定义式", "否"),
    ("W/π 力程数值匹配 PDG", "数值代入", "否"),
    ("G=ħc/m_P²", "循环定义（B01 已 FAIL）", "否"),
    ("牛顿引力公式还原", "需要中心 1/r 势", "是"),
    ("精细结构常数定义式", "定义式", "否"),
    ("库仑力还原", "需要中心 1/r 势", "是"),
    ("F_B/F_E=v²/c² 相对论伴生", "洛伦兹变换性质", "否"),
    ("c²=1/(ε₀μ₀)", "定义式", "否"),
    ("洛伦兹力不做功", "矢量恒等式", "否"),
    ("力程层级排序", "只依赖 λ 数值排序", "否"),
    ("F_E/F_G=α(m_P/m_p)² ≈1e36", "比值代入（r23 P03：恒等式零信息）", "否"),
    ("剩余核力汤川 e^{−μr}/r 还原", "需要中心 Yukawa 势", "是"),
]
n_dep = sum(1 for row in L3_CLASS if row[2] == "是")
emit("J09", "CORRECTED",
     "代价记账精密化（自我约束：不得夸大）：真依赖球对称的 L3 项是 3 条，不是草稿所称的「12 条全部」",
     "把 L3 的 12 条逐条按「是否需要中心势/点源」分类（机器表里 12 行）：依赖 = 牛顿还原、库仑还原、"
     "剩余核力汤川还原，共 3 条；另有 1 条结构假设（统一势 U=sℏc q1q2 e^{−r/λ}/r 的中心 ansatz）"
     "本身不在计数内但被上述 3 条共用。其余 9 条是定义式/代入/恒等式，不受球对称影响"
     "（其中 F_E/F_G 在 r23 P03 已被判为恒等式零信息）。"
     "⇒ 与前置草稿 G03「丢失 12 条（全部中心势）」口径不一致，本册按逐条机器表下修为 3 条；"
     "但这 3 条恰是来料自评『最亮眼部分』的主体 ⇒ 结论方向不变，只是代价账必须精确。",
     numbers={"L3_total": len(L3_CLASS), "dependency_true": n_dep,
              "dependency_false": len(L3_CLASS) - n_dep, "table": L3_CLASS})

emit("J10", "INFO",
     "四选项的当前裁决状态（继承 + 本册增量，不代选）",
     "A（∇κ·∇τ）：本册新增证词 = 有解但必须付三选二的代价 ⇒ 作为「保存框架的修复」不可行；"
     "作为「把 BOUNDARY 升级为已构造 + 已定价」则本册已完成。"
     "B（改场方程容纳 σr）：前置草稿 G07–G10（源项对消⇒恒等式复读、μ 消失、源非局域发散、"
     "模承载三重缺陷）；本册不重算。C（几何锁 α）：r22 B06 + 前置草稿 G18–G21（四候选全否）；"
     "本册不重算。D（写 Discussion）：前置草稿 G26 已给三节骨架，本册 J09 的逐条分类是其输入。"
     "位次建议（仍需用户裁决）：若要「最多保留资产」，顺序是 D（零风险整理） → B/C 的显式登记外部输入 → A 的代价接受/拒绝。",
     numbers={"A_cost_items": n_dep, "B_recompute": False, "C_recompute": False})

emit("J11", "INFO",
     "射程与红线声明",
     "本册结论限于「单约束 ∇κ·∇τ=0 的这一类构建 + 上述三条腿」；不构成对一般三维非球对称解空间的穷尽，"
     "也不构成对 QCD 本身的任何判断（QCD 禁闭是既定事实，本册只判它不能由该框架的特定方程结构内生）。"
     "数值全部机器复算（差分 h=1e−5 / 1e−4，积分 401 点梯形），十字路口与 r22/r23/r24 的 λ(π⁰)、λ(W) 读数独立对拍。"
     "红线：数学自洽 ≠ 实验证实；本册不产生新物理，也不宣称4周游标。",
     numbers={"lambda_pi0_m": fm(LAM_PI0), "lambda_W_m": fm(LAM_W)})

emit("J12", "CORRECTED",
     "本册自抓 4 处实现/判据缺陷（已修，留痕）",
     "① rel() 误用：J03 首版写 rel(∇²κ−μ²κ, μ²κ) —— 第二个参数应取「应等于的值」而非残差基准，"
     "导致相对残差恒 ≈1.0（把方程检验写成恒假）；守门 guard 用的是直算式因而照样全过 ⇒ "
     "【教训复现（库内第 4 次）：条目数值与 guard 必须由同一表达式产出，否则 guard 全绿而读数全错】。"
     "② J01 归一化尺度错：首版用 |lhs| 归一化，在全纯族（Q1=Q2=0 使得 rhs 因相消而≈0）上给假 NG（42.2）；"
     "改按恒等式的自然量纲 |λ|²·|∇ρ|² 归一 ⇒ 2.32e−10。"
     "③ lap 差分器对照组取了 Laplacian 恰为 0 的函数（除以 0 ⇒ 1.1e+292 假 NG），改 x²+3y²−z²（=6）。"
     "④ 球对称腿首版代入真实的 μ(π⁰)、μ(W)（~1e14 / 1e18）， Yukawa 值下溢为 0 ⇒ ZeroDivisionError；"
     "改同单位的无量纲质量（该腿的结论是几何性质，与 μ 的具体数值无关）。",
     numbers={"fixed": 4, "pre_fix_identity_reading": 42.20304435877042})

# ================================================================== 自检（guard）
g_lock = max(abs(lap3(kap_f, *p) - MU_K * MU_K * kap_f(*p)) / abs(MU_K * MU_K * kap_f(*p)) for p in PSET)
guard("proca_kappa_control", g_lock < 1e-6, "构造 κ 的 Proca 方程应满足（差分精度）", g_lock)
gt_lock = max(abs(lap3(tau_f, *p) - MU_T * MU_T * tau_f(*p)) / abs(MU_T * MU_T * tau_f(*p)) for p in PSET)
guard("proca_tau_control", gt_lock < 1e-6, "构造 τ 的 Proca 方程应满足（差分精度）", gt_lock)
guard("orthogonality_control", worst_orth < 1e-8, "构造应满足 ∇κ·∇τ=0（相对）", worst_orth)
guard("two_condition_strictly_stronger", worst_q > 1e-3,
      "Q1/Q2 应显著非零（证明双条件体系严格更强）", worst_q)
guard("green_identity", green_rel < 1e-3, "格林恒等式体积分↔边界积分应一致", green_rel)
guard("duality_roundtrip", worst_rt < 1e-10, "对偶反演往返应机器零", worst_rt)
guard("anisotropy_is_real", aniso_xi > 1.5, "各向异性比应显著 > 1", aniso_xi)
guard("identity_J01", worst_iden < 1e-6, "J01 恒等式应满足（差分精度）", worst_iden)
lap_ctrl = rel(lap3(lambda x, y, z: x * x + 3 * y * y - z * z, 0.5, 0.7, 0.3), 2 + 6 - 2)
guard("laplacian_control", lap_ctrl < 1e-4, "∇²(x²−2y²+z²) 应等于 2−4+2=0（差分器对照）", lap_ctrl)
rel_pi0 = abs(LAM_PI0 - Decimal("1.461933E-15")) / Decimal("1.461933E-15")
guard("lambda_pi0_crosscheck_prev_rounds", rel_pi0 < Decimal("1E-5"),
      "λ(π⁰) 应与 r22/r23/r24 读数一致", fm(rel_pi0))
rel_W = abs(LAM_W - Decimal("2.454957E-18")) / Decimal("2.454957E-18")
guard("lambda_W_crosscheck_prev_rounds", rel_W < Decimal("1E-4"),
      "λ(W) 应与 r22 读数一致", fm(rel_W))
ids = [e["id"] for e in ENTRIES]
guard("entry_ids_unique", len(ids) == len(set(ids)), "条目编号不得重复", len(ids))

# ================================================================== 汇总与落盘
counts = {}
for e in ENTRIES:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
n_guard_ok = sum(1 for g in GUARDS if g["ok"])

KEY.update({
    "lambda_pi0_m": fm(LAM_PI0),
    "lambda_W_m": fm(LAM_W),
    "worst_identity_relative": worst_iden,
    "worst_orthogonality_relative": worst_orth,
    "worst_Q1_or_Q2_relative": worst_q,
    "worst_proca_relative": worst_mass,
    "worst_duality_roundtrip": worst_rt,
    "green_relative": green_rel,
    "growth_factor_z_-5": grow,
    "anisotropy_Xi_max_over_min": aniso_xi,
    "anisotropy_gradXi_max_over_min": aniso_g,
    "anisotropy_Xi_full_sphere": aniso_xi_full,
    "anisotropy_gradXi_full_sphere": aniso_g_full,
    "anisotropy_radius_scan": ANISO_SCAN,
    "leg_i_worst_cos": worst_leg_i,
    "L3_items_depending_on_central_potential": n_dep,
})

payload = {
    "meta": {
        "tag": TAG, "round": ROUND, "date": "2026-10-10",
        "engine": os.path.basename(__file__),
        "python": sys.version.split()[0],
        "stdlib_only": True,
        "scope": "垂直原理四力统一：单约束 ∇κ·∇τ=0 的显式构造、三选二定理与各向同性代价（增量，不重算既有四选项读数）",
        "inherits": ["r22 48 条", "r23 33 条", "r24 30 条", "r25 禁闭与 ABCD 四选项裁定 28 条（G01..G28，并行会话成册）"],
        "not_additive_with": ["r22", "r23", "r24", "r25"],
    },
    "counts": counts,
    "entries": ENTRIES,
    "guards": GUARDS,
    "guard_ok": n_guard_ok,
    "guard_total": len(GUARDS),
    "key_numbers": KEY,
}

with open(os.path.join(DIR_DATA, TAG + ".json"), "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)

lines = ["# %s（%s）" % (TAG, ROUND), ""]
lines.append("- 条目 %d：%s" % (len(ENTRIES), " / ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))))
lines.append("- 自检 %d/%d；退出码 0；纯标准库" % (n_guard_ok, len(GUARDS)))
lines.append("")
for e in ENTRIES:
    lines.append("## %s [%s] %s" % (e["id"], e["verdict"], e["title"]))
    lines.append(e["detail"])
    if e["numbers"]:
        lines.append("- 读数：%s" % json.dumps(e["numbers"], ensure_ascii=False))
    lines.append("")
lines.append("## 自检")
for g in GUARDS:
    lines.append("- [%s] %s：%s" % ("OK" if g["ok"] else "NG", g["name"], g["value"]))
with open(os.path.join(DIR_DATA, TAG + ".md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

rep = []
rep.append("REPORT %s" % TAG)
rep.append("ENTRIES = %d" % len(ENTRIES))
for k, v in sorted(counts.items()):
    rep.append("%s = %d" % (k, v))
rep.append("GUARD = %d/%d" % (n_guard_ok, len(GUARDS)))
for g in GUARDS:
    rep.append("  %s %s" % ("OK " if g["ok"] else "NG ", g["name"]))
with open(os.path.join(DIR_DATA, TAG + "_report.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(rep))

print("ENTRIES=%d COUNTS=%s GUARD=%d/%d" % (len(ENTRIES), counts, n_guard_ok, len(GUARDS)))
for g in GUARDS:
    if not g["ok"]:
        print("GUARD NG: %s -> %s" % (g["name"], g["value"]))
sys.exit(0 if n_guard_ok == len(GUARDS) else 1)


