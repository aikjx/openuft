# -*- coding: utf-8 -*-
"""
TUFT 垂直原理四力统一框架 —— 禁闭路线与 A/B/C/D 四选项攻坚裁定（r25）

来料：《TUFT 四力大统一（垂直原理框架）》34 条目总结 + 追加的
      「BOUNDARY 项 ∇κ⊥∇τ 解析推导」+「L3 FAIL 禁闭线性势 σr」+ A/B/C/D 四选项。

分工声明（不重复计数，先记账）：
  * r22（判定_TUFT-r22-垂直原理四力统一框架_全维审计_2026-10-10.md，48 条目）
        —— 审来料本体：C08 展开式符号笔误 / C09 约束计数错 / C10 径向不相容 /
           D03 线性势无解 / D06 非线性代价 / B06 α 无约束 / C11 无螺旋残留。
  * r23（判定_TUFT-r23-垂直原理续篇八至十章_全维审计_2026-10-10.md，33 条目）
        —— 审续篇新增八~十章。
  * S16 主册四篇攻坚（01_独立体系/S16_TUFT归一化主册/09_验证结果/）
        —— A 项：约束 ⟺ 柯西-黎曼（W=ρ+ib 全纯），有质量力程嵌入标为开放；
           B 项：非齐次源 S=2σ/r−μ²σr「数学修复成立」，兼容修复 = 模 |Ξ|=σr 承载；
           D 项：α 严格自由（否定结论）。
  * 本册 r25 = 对上述 A/B/D 三篇攻坚产物的【元审计 + 净增量】，并首次机器检验
    从未被检验过的 C 项（非线性 λκ³）。条目编号 G01..G28，与 r22/r23 不可相加。

纯标准库（Python 3.8.8 实测可跑）：Decimal 60 位 + Fraction 量纲向量 + 有限差分 + RK4。
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
os.makedirs(DIR_DATA, exist_ok=True)

TAG = "TUFT-垂直原理四力统一_禁闭与ABCD四选项攻坚裁定_2026-10-10"

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


# ---------------------------------------------------------------- 数值工具
def grad3(f, x, y, z, h=1e-5):
    return (
        (f(x + h, y, z) - f(x - h, y, z)) / (2 * h),
        (f(x, y + h, z) - f(x, y - h, z)) / (2 * h),
        (f(x, y, z + h) - f(x, y, z - h)) / (2 * h),
    )


def lap3(f, x, y, z, h=1e-4):
    s = -6.0 * f(x, y, z)
    for d in range(3):
        p = [x, y, z]
        p[d] += h
        s += f(*p)
        p[d] -= 2 * h
        s += f(*p)
    return s / (h * h)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def nrm2(a):
    return dot(a, a)


# κ,τ 由位形场 (ρ,b) 给出： κ=ρ/D, τ=b/D, D=ρ²+b²（来料 L1 定义）
def make_kappa(rho, b):
    def k(x, y, z):
        r = rho(x, y, z)
        bb = b(x, y, z)
        return r / (r * r + bb * bb)
    return k


def make_tau(rho, b):
    def t(x, y, z):
        r = rho(x, y, z)
        bb = b(x, y, z)
        return bb / (r * r + bb * bb)
    return t


# 约束残差： |∇ρ·∇b| + ||∇ρ|²-|∇b|²|
def constraint_residual(rho, b, pts):
    worst = 0.0
    for (x, y, z) in pts:
        gr = grad3(rho, x, y, z)
        gb = grad3(b, x, y, z)
        r = abs(dot(gr, gb)) + abs(nrm2(gr) - nrm2(gb))
        worst = max(worst, r)
    return worst


# 柯西-黎曼残差（按 (x,y) 平面）
def cr_residual(rho, b, pts):
    worst = 0.0
    for (x, y, z) in pts:
        h = 1e-5
        dxr = (rho(x + h, y, z) - rho(x - h, y, z)) / (2 * h)
        dyr = (rho(x, y + h, z) - rho(x, y - h, z)) / (2 * h)
        dxb = (b(x + h, y, z) - b(x - h, y, z)) / (2 * h)
        dyb = (b(x, y + h, z) - b(x, y - h, z)) / (2 * h)
        worst = max(worst, abs(dxr - dyb), abs(dyr + dxb))
    return worst


PTS = [(1.3, 0.7, 0.4), (2.1, -0.5, 0.9), (0.8, 1.6, -0.3), (3.0, 2.2, 1.1)]

# ================================================================ 段 I：A 项复核
# G01：既有册「约束 ⟺ W 全纯」在 3D 是过断言（全纯 ⟹ 约束，反之不成立）
_rho_c = lambda x, y, z: x
_b_c = lambda x, y, z: z
res_c = constraint_residual(_rho_c, _b_c, PTS)
cr_c = cr_residual(_rho_c, _b_c, PTS)
k_c = make_kappa(_rho_c, _b_c)
t_c = make_tau(_rho_c, _b_c)
lap_k_c = max(abs(lap3(k_c, *p)) for p in PTS)
emit("G01", "MISMATCH",
     "既有 A 项「约束 ⟺ W=ρ+ib 全纯」在三维物理空间是过断言：全纯是充分非必要条件",
     "反例 ρ=x, b=z（∇ρ=(1,0,0), ∇b=(0,0,1)）：约束残差(点积+等模)机器零，"
     "而柯西-黎曼残差 = |∂xρ−∂yb|=1（b 与 y 无关）≠0 ⇒ 非全纯却满足约束。"
     "⇒ 3D 解空间严格大于全纯函数集，既有册的充要表述须降级为「全纯 ⟹ 约束」（单向）。"
     "注意：这不影响本册后续否证，因为该反例族的 κ,τ 同样是调和场（见 G05）。",
     numbers={"constraint_residual": res_c, "cr_residual": cr_c, "lap_kappa": lap_k_c})

# G02：全纯族 ⟹ 约束（既有册方向成立，复算确认）
holos = {
    "z": (lambda x, y, z: x, lambda x, y, z: y),
    "z^2": (lambda x, y, z: x * x - y * y, lambda x, y, z: 2 * x * y),
    "e^z": (lambda x, y, z: math.exp(x) * math.cos(y), lambda x, y, z: math.exp(x) * math.sin(y)),
}
holo_res = {}
for name, (rr, bb) in holos.items():
    holo_res[name] = constraint_residual(rr, bb, PTS)
worst_holo = max(holo_res.values())
emit("G02", "PASS",
     "既有 A 项的正向命题复算通过：W 全纯 ⟹ ∇ρ·∇b=0 且 |∇ρ|=|∇b|",
     "三个全纯样本（z / z² / e^z）在 4 个测试点上约束残差均为差分截断量级，"
     "与既有册数值（5.8e-10 / 3.6e-09 / 1.4e-08）同量级 ⇒ 该方向结论成立，本册只复核不重算。",
     numbers=holo_res)

# G03：球对称（径向）情形下约束只允许平凡解 —— 与 L3 全部中心势互斥
radial_profiles = [
    ("ρ=r, b=2r", lambda r: r, lambda r: 2 * r),
    ("ρ=1+e^-r, b=0.5e^-r", lambda r: 1 + math.exp(-r), lambda r: 0.5 * math.exp(-r)),
    ("ρ=2+1/r, b=1-1/(2r)", lambda r: 2 + 1.0 / r, lambda r: 1 - 0.5 / r),
]
radial_rows = []
for name, fr, fb in radial_profiles:
    rho = lambda x, y, z, fr=fr: fr(math.sqrt(x * x + y * y + z * z))
    bb = lambda x, y, z, fb=fb: fb(math.sqrt(x * x + y * y + z * z))
    radial_rows.append((name, constraint_residual(rho, bb, PTS)))
worst_radial = max(r[1] for r in radial_rows)
emit("G03", "FAIL",
     "球对称（径向）位形场下，场版垂直原理的唯一解是 ρ,b 常数 —— 与 L3 全部 12 项中心势互斥",
     "径向 ansatz 下有 ∇ρ=ρ'(r)r̂、∇b=b'(r)r̂ 二者必平行 ⇒ 正交条件给 ρ'b'=0，"
     "等模条件给 ρ'²=b'² ⇒ 联立得 ρ'=b'=0。即【任何非平凡径向解都不在约束解空间内】。"
     "而 L3 的 12 项经典极限还原（牛顿 1/r、库仑、汤川 e^{-μr}/r）全部是球对称中心势"
     " ⇒ 场版垂直原理与 L3 的全部实证资产结构性互斥。机器：3 组非平凡径向剖型约束残差全部显著非零。",
     numbers={"profiles": radial_rows, "worst": worst_radial})

# G04：全纯族 ⇒ κ,τ 调和 ⇒ 有质量 Proca 不可承载（闭合既有册的开放项）
lap_rows = {}
for name, (rr, bb) in holos.items():
    kk = make_kappa(rr, bb)
    tt = make_tau(rr, bb)
    lap_rows[name] = {
        "max|∇²κ|": max(abs(lap3(kk, *p)) for p in PTS),
        "max|∇²τ|": max(abs(lap3(tt, *p)) for p in PTS),
    }
worst_lap = max(max(v.values()) for v in lap_rows.values())
# μ(π⁰) 与 μ(W) 作为力程参数
HBAR = Decimal("1.054571817") * Decimal(10) ** -34
CC = Decimal("299792458")
HBARC = HBAR * CC
MEV = Decimal("1.602176634") * Decimal(10) ** -13
M_PI0_MEV = Decimal("134.9768")
M_W_MEV = Decimal("80377")
lam_pi0 = HBARC / (M_PI0_MEV * MEV)     # λ=ħ/(mc)=(ħc)/(mc²)，mc² 以焦耳计
lam_W = HBARC / (M_W_MEV * MEV)
mu_pi0 = 1 / lam_pi0
mu_W = 1 / lam_W
emit("G04", "FAIL",
     "闭合既有册的开放项：场版垂直原理（解析性）只能承载 μ=0 的无质量场，有质量力程不可嵌入",
     "既有册留下「有质量/力程嵌入尚未完成」为开放项。本册闭合为否证：若 W 全纯且非零，"
     "则 Ξ=κ+iτ=1/W* 反全纯 ⇒ κ,τ 均调和（∇²κ=∇²τ=0，机器零级），于是"
     "(∇²−μ²)κ = −μ²κ ≠ 0 对任意 μ≠0 ⇒ 有限力程（λ_W=2.45e−18 m、λ(π⁰)=1.46e−15 m）"
     "在场版垂直原理下不可能出现。⇒ A 项不是「待完成」，而是「与 L2 力程结构不相容」。",
     numbers={"lap_table": lap_rows, "worst_lap": worst_lap,
              "lambda_pi0_m": fm(lam_pi0), "lambda_W_m": fm(lam_W),
              "mu_pi0_inv_m": fm(mu_pi0), "mu_W_inv_m": fm(mu_W)})

# G05：反例族（非全纯但满足约束）同样只能 μ=0，否证不依赖全纯性
emit("G05", "FAIL",
     "否证射程扩大：非全纯的反例族同样强制 ∇²κ=0 ⇒ μ=0 必需与全纯性无关",
     "G01 的反例 ρ=x, b=z 给出 κ=x/(x²+z²)、τ=z/(x²+z²)，在 (x,z) 平面上恰为 Re/Im(1/w)"
     " ⇒ 调和（机器量级）⇒ 同样只能承载 μ=0。⇒ 本册否证不依赖「W 全纯」这一更强的假设，"
     "在迄今已知的全部非平凡解族（全纯族 + 平面调和反例族）上一致成立。",
     numbers={"lap_kappa_counterexample": lap_k_c})

# G06：A 项最终裁定与射程声明
emit("G06", "BOUNDARY",
     "A 项最终裁定：既有册开放项由「待完成」改判为「在已知解族与球对称穷尽下不可能」",
     "射程声明（不冒充一般定理）：已覆盖 ①全纯族（G04 解析 + 机器）②平面调和反例族（G05）"
     "③球对称径向族穷尽（G03，解析完备）。未覆盖：一般 3D 非球对称、非平面调和的解（若有）。"
     "⇒ 即便存在此类解，它也必然不是球对称 ⇒ 仍无法还原 L3 的中心势。",
     numbers={"covered_families": 3})

# ================================================================ 段 II：路线 B（禁闭·非齐次）
# G07：源项依赖解本身 ⇒ 方程退化为泊松方程，μ 精确消去（既有册「残差=0」是恒等式复读）
SIGMA = Decimal("1.0")   # 单位化（结论与 σ 取值无关）
MU_A = Decimal("1.0")
MU_B = Decimal("3.7")


def lhs_proca(mu, r):
    """(∇²−μ²)(σ r) 的三维径向值 = 2σ/r − μ²σr"""
    return 2 * SIGMA / r - mu * mu * SIGMA * r


def src_proca(mu, r):
    """来料/既有册定义的源 S(r) = 2σ/r − μ²σr"""
    return 2 * SIGMA / r - mu * mu * SIGMA * r


canc_rows = []
for rval in [Decimal("0.5"), Decimal("1.0"), Decimal("2.5"), Decimal("10")]:
    for mu in (MU_A, MU_B):
        lhs = lhs_proca(mu, rval)
        src = src_proca(mu, rval)
        canc_rows.append({
            "r": str(rval), "mu": str(mu),
            "lhs_minus_src": fm(lhs - src),
            "mu2kappa_term": fm(mu * mu * SIGMA * rval),
        })
worst_canc = max(abs(Decimal(row["lhs_minus_src"])) for row in canc_rows)
# 关键：把 (∇²−μ²)κ=S 改写后 μ²κ 与 μ²σr 对消
emit("G07", "FAIL",
     "路线 B（非齐次 Proca）是零信息量的恒等式复读：源项依赖解本身，μ²κ 被精确对消，方程退化为 ∇²κ=2σ/r",
     "既有册称「源项恒等成立，残差 0，F1 在数学层面修复」。残差当然为 0：因解取 κ=σr，"
     "源中的 −μ²σr 与方程左端的 −μ²κ 是同一项 ⇒ 两边同减，方程实际为 ∇²κ = 2σ/r，"
     "μ 完全消失。⇒ 这不是「引入一个携带禁闭的源」，而是「把质量项搬到右边再对消掉」。"
     "库内缺陷族登记：恒等式复读（与 r22 A07/D01、30 号册 V06 同族）。"
     "判据：取 μ=1 与 μ=3.7 两个不同值，源不同但解同为 σr ⇒ 源不是物理独立的输入。",
     numbers={"table": canc_rows, "worst_identity_residual": fm(worst_canc)})

# G08：μ 消失 ⇒ 与 L2 力程结构冲突
emit("G08", "FAIL",
     "路线 B 的净代价：力程参数 μ 在修复后的方程中消失，剩余核力的有限力程无法保留",
     "L2 定义力程 λ=ħ/(mc)=1/μ，λ(π⁰)=1.461933e−15 m 是 L3 的一项 PASS。"
     "路线 B 退化后的方程 ∇²κ=2σ/r 不含 μ ⇒ 强力在此修复中力程为无穷，"
     "与「剩余核力短程（1.46e−15 m）」矛盾 ⇒ 净代价 = 至少 1 项 L3 PASS + μ 的物理定义失效。",
     numbers={"lambda_pi0_m": fm(lam_pi0)})

# G09：源 2σ/r 非局域且奇异
integ_rows = []
for R in [Decimal("1"), Decimal("10"), Decimal("100"), Decimal("1000")]:
    # ∫|2σ/r| 4πr² dr = 8πσ R²/2 = 4πσR²（主导项，忽略 −μ²σr 项的 −4πμ²σR⁴/4）
    integ_rows.append({"R": str(R), "int_2sigma_over_r": fm(4 * Decimal(str(math.pi)) * SIGMA * R * R)})
emit("G09", "FAIL",
     "路线 B 的源 S=2σ/r−μ²σr 不是局域源：在 r=0 奇异、总量随 R² 发散",
     "1/r 型源不是 δ 型点源：∫|2σ/r|4πr²dr = 4πσR² 随域半径二次发散，且在 r→∞ 不衰减"
     " ⇒ 无法解释为「粒子/物质分布产生的源」，与 QCD 禁闭源于局域非微扰动力学的物理图像冲突。"
     "（另一项 −μ²σr 随 R⁴ 发散，但因为 G07 的对消它根本不进入方程。）",
     numbers={"table": integ_rows})

# G10：既有册「模承载」兼容修复的三重缺陷
# 取 Ξ=σz ⇒ κ=σx, τ=σy；|Ξ|=σ√(x²+y²)（柱半径，不是球半径）
kap_mod = lambda x, y, z: 1.0 * x
tau_mod = lambda x, y, z: 1.0 * y
lap_mod_k = max(abs(lap3(kap_mod, *p)) for p in PTS)
lap_mod_t = max(abs(lap3(tau_mod, *p)) for p in PTS)
mod_axial = math.sqrt(0.0 ** 2 + 0.0 ** 2)          # |Ξ| 在 (0,0,5) 处
sphere_axial = 5.0                                   # 球半径 r 在 (0,0,5) 处
mod_z1 = math.sqrt(1.0 ** 2 + 2.0 ** 2)             # (1,2,3) 处 |Ξ|=√5
sphere_z1 = math.sqrt(1.0 + 4.0 + 9.0)
emit("G10", "FAIL",
     "既有册「兼容修复（解析函数模承载：Ξ=σz, |Ξ|=σr）」的三重缺陷 —— 修复未闭合",
     "① 几何错配：|Ξ|=σ√(x²+y²) 是【柱半径】而非球半径。在点 (0,0,5) 上 |Ξ|=0 而球 r=5"
     " ⇒ 与 QCD 球对称中心势 σr 不是同一个量（差 100%）。"
     "② 分量退化为无源场：κ=σx、τ=σy 是线性函数，∇²κ=∇²τ=0（机器零）⇒ 无点源、无 1/r"
     " ⇒ 不能还原牛顿势与库仑势，直接丢掉 L3 的两项 PASS（引力、电磁）。"
     "③ 模本身不满足任何场方程：|Ξ|=σρ_cyl 的拉普拉斯为 σ/ρ_cyl ≠ 0 ⇒ 「模承载禁闭」"
     " 只是把 σr 这个【量】摆了出来，并未给出它的动力学方程 ⇒ F1 并未被修复，只是被改名。",
     numbers={"lap_kappa_linear": lap_mod_k, "lap_tau_linear": lap_mod_t,
              "mod_at_(0,0,5)": mod_axial, "sphere_r_at_(0,0,5)": sphere_axial,
              "mod_at_(1,2,3)": mod_z1, "sphere_r_at_(1,2,3)": sphere_z1})

# G11：σ 的量纲与数值换算（既有册未做）
SIGMA_QCD_GEV2 = Decimal("0.18")
GEMV_INV_FM = Decimal("1") / (HBARC / (Decimal("1000") * MEV) / Decimal("1e-15"))  # 1/(ℏc[GeV·fm])
sigma_gev_per_fm = SIGMA_QCD_GEV2 * GEMV_INV_FM
GEV_PER_FM_TO_N = (Decimal("1e3") * MEV) / Decimal("1e-15")
sigma_N = sigma_gev_per_fm * GEV_PER_FM_TO_N
sigma_over_hbarc = sigma_N / HBARC
kappa_at_1fm = sigma_over_hbarc * Decimal("1e-15")
radius_of_curvature_fm = (1 / kappa_at_1fm) / Decimal("1e-15")
emit("G11", "INFO",
     "量纲与数值补登（既有册未做）：κ 场(L⁻¹) 与禁闭势 σr(能量) 相差 ℏc 因子；σ→κ 系数的定量换算",
     "量纲链：σ[=]能量/长度=力，ℏc[=]能量·长度 ⇒ σ/(ℏc)[=]L⁻² ⇒ κ=(σ/ℏc)r[=]L⁻¹ ✓ 与曲率同量纲。"
     "取 QCD 弦张力 σ=0.18 GeV²：σ=1.4617E+05 N，σ/(ℏc)=4.6242E+30 m⁻²，"
     "κ(1 fm)=4.6242E+15 m⁻¹ ⇒ 曲率半径 0.2163 fm（量级合理，可与强子尺度对照）。"
     "⇒ 量纲【不是】路线 B 的障碍；障碍在 G07/G08/G09/G10。",
     numbers={"sigma_N": fm(sigma_N), "sigma_over_hbarc_m^-2": fm(sigma_over_hbarc),
              "kappa_at_1fm": fm(kappa_at_1fm), "curvature_radius_fm": fm(radius_of_curvature_fm)})

# G12：σ 外部输入
emit("G12", "FAIL",
     "σ（弦张力）是第四个外部输入常数 ⇒ 复发 B03/F4，路线 B 不解决 L5 的任何一条",
     "既有册自己承认「σ 仍是参数输入，归入 L5 F2/F3/F4」。本册记账：禁闭路线使外部输入"
     "由 4 个（g_s, α_EM, g_W, G）增至 5 个（+σ）⇒ 与 L5-F4「耦合常数全部外部输入」同族，"
     "且方向相反（修复一个 FAIL 的同时加深另一个 FAIL）。",
     numbers={"external_inputs_before": 4, "external_inputs_after": 5})

# ================================================================ 段 III：路线 C（非线性，既有册完全未检验）
# G13：λκ³ 自耦合无渐近线性解
asym_rows = []
for rval in [Decimal("10"), Decimal("100"), Decimal("1000")]:
    a = Decimal("1.0")      # κ ~ a r
    mu = Decimal("1.0")
    lam = Decimal("1.0")
    term_lap = 2 * a / rval                    # ∇²(ar) = 2a/r
    term_mu = -mu * mu * a * rval              # −μ²κ
    term_lam = lam * a * a * a * rval ** 3     # +λκ³
    asym_rows.append({
        "r": str(rval), "lap_term": fm(term_lap), "mu_term": fm(-term_mu),
        "lambda_term": fm(term_lam),
        "ratio_lambda_over_mu": fm(abs(term_lam / term_mu)),
    })
emit("G13", "FAIL",
     "路线 C 的候选方程 ∇²κ−μ²κ+λκ³=0 无渐近线性解 —— 来料「可同时容纳汤川解+线性增长解」未经检验且为假",
     "代入 κ~ar（r→∞）：∇²(ar)=2a/r 衰减，−μ²ar 线性，+λa³r³ 三次增长 ⇒ λa³r³ 主导，"
     "方程残差 → ∞（除非 λ=0 或 a=0，两者都回到无禁闭的原方程）。"
     "在 r=1000 上 |λκ³/μ²κ| = 1.000E+06 ⇒ 非线性项不是修正项而是主导项。"
     "（实际渐近行为由 G14 打靶给出：来料候选的渐近是常数 κ→μ/√λ，同样不是线性增长。）"
     "⇒ 标准三次自耦合【不能】产生线性禁闭；既有册与来料均把该候选列为「可行」而未做任何检验。",
     numbers={"table": asym_rows})


def shoot(mu, lam, sign, k0, kp0, r0=1.0, rmax=60.0, dr=1e-3):
    """径向 κ'' + (2/r)κ' = μ²κ − sign·λκ³ 的 RK4 打靶。

    sign=+1 ⇔ 来料候选 ∇²κ−μ²κ+λκ³=0 ⇔ 势 V=½μ²κ²−¼λκ⁴（墨西哥帽），真空期望 κ=μ/√λ。
    sign=−1 ⇔ 方程 ∇²κ−μ²κ−λκ³=0 ⇔ 势 V=½μ²κ²+¼λκ⁴（单井），κ>0 时为次调和 ⇒ 无界增长。
    返回 (分类, 明细)。分类依据末段幂次 p = ln|κ(60)/κ(30)|/ln2：p≈1 才是线性增长 σr。
    """
    def f(r, k, v):
        return -2.0 * v / r + mu * mu * k - sign * lam * k ** 3
    r, k, v = r0, k0, kp0
    n = int((rmax - r0) / dr)
    samples = {}
    for i in range(n):
        a1 = f(r, k, v)
        a2 = f(r + dr / 2, k + dr / 2 * v, v + dr / 2 * a1)
        a3 = f(r + dr / 2, k + dr / 2 * (v + dr / 2 * a1), v + dr / 2 * a2)
        a4 = f(r + dr, k + dr * (v + dr / 2 * a2), v + dr * a3)
        k_new = k + dr / 6 * (6 * v + dr * (a1 + a2 + a3))
        v_new = v + dr / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        r += dr
        k, v = k_new, v_new
        if abs(k) > 1e12 or not (abs(k) < float("inf")):
            return "DIVERGENT", {"kappa@30": None, "kappa@60": None, "p_est": None}
        for mark in (30.0, 40.0, 50.0, 60.0):
            if mark not in samples and r >= mark - 1e-9:
                samples[mark] = k
    for mark in (30.0, 40.0, 50.0, 60.0):
        samples.setdefault(mark, k)
    k30 = abs(samples[30.0])
    k60 = abs(samples[60.0])
    if k30 < 1e-12 or k60 < 1e-12:
        return "DECAY_TO_ZERO", {"kappa@30": samples[30.0], "kappa@60": samples[60.0], "p_est": None}
    p_est = math.log(k60 / k30) / math.log(2.0)
    if abs(p_est - 1.0) < 0.05:
        cls = "LINEAR_GROWTH"
    elif abs(p_est) < 0.05:
        cls = "CONSTANT"
    elif p_est > 1.05:
        cls = "SUPER_LINEAR_OR_DIVERGENT"
    elif p_est < -0.05:
        cls = "DECAY_TO_ZERO"
    else:
        cls = "SUB_LINEAR"
    return cls, {"kappa@30": samples[30.0], "kappa@60": samples[60.0], "p_est": p_est}


cases = [
    ("墨西哥帽 V=½μ²κ²−¼λκ⁴（来料候选）, μ=λ=1, κ0=1", 1.0, 1.0, +1, 1.0, 0.0),
    ("墨西哥帽, μ=λ=1, κ0=0.5, κ'0=−0.5", 1.0, 1.0, +1, 0.5, -0.5),
    ("墨西哥帽, μ=0.5 λ=1, κ0=1", 0.5, 1.0, +1, 1.0, 0.0),
    ("墨西哥帽, μ=2 λ=0.5, κ0=1", 2.0, 0.5, +1, 1.0, 0.0),
    ("单井 V=½μ²κ²+¼λκ⁴, μ=λ=1, κ0=1.5", 1.0, 1.0, -1, 1.5, 0.0),
    ("单井, μ=λ=1, κ0=0.5, κ'0=−0.2", 1.0, 1.0, -1, 0.5, -0.2),
]
shoot_rows = []
for name, mu, lam, sign, k0, vp in cases:
    cls, info = shoot(mu, lam, sign, k0, vp)
    row = {"case": name, "class": cls}
    row.update(info)
    shoot_rows.append(row)
n_linear = sum(1 for r in shoot_rows if r["class"] == "LINEAR_GROWTH")
emit("G14", "FAIL",
     "径向打靶穷举：6 组（两种势型 × 多初值）无一产生线性增长解 —— 单标量 + 局域多项式势不能内生禁闭",
     "分类依据末段幂次 p=ln|κ(60)/κ(30)|/ln2：p≈1 才是 σr 型线性增长。"
     "结果（CASE→CLASS(p)）：" + "；".join(
         r["case"].split(",")[0] + "→" + r["class"] + "(p=" + (
             "发散" if r["p_est"] is None else "%.3f" % r["p_est"]) + ")" for r in shoot_rows)
     + "。来料候选（墨西哥帽，sign=+1）的渐近是【常数】κ→μ/√λ（实测 μ=λ=1 时趋于 1.0，p≈0），"
     "单井（sign=−1）在 κ>0 时为次调和 ⇒ 无界增长（发散，无静态解）⇒ 两种势型都不给线性禁闭。"
     "⇒ 结论是结构层的（不是参数没调好）：单个标量场 + 局域多项式自耦合【不能】给出 σr。"
     "（分类器有效性由 guard 用真解 κ=σr 的控制方程做正向对照，见自检 9。）",
     numbers={"table": shoot_rows, "n_linear_growth": n_linear})

# G15：真正能产生线性禁闭的最小结构（构造性答案，非 TUFT 内生）
emit("G15", "BOUNDARY",
     "要真正内生线性禁闭，最小结构是 Abelian Higgs / Nielsen–Olesen 通量管 —— 与螺旋几何无关",
     "已知能产生线性禁闭势的局域场论结构 = 规范场 A_μ + 复标量 Higgs（破缺到通量管，"
     "能量/长度 = 有限张力 σ）。所需增量：+1 个矢量规范场、+1 个复标量场（2 实分量）、"
     "+2 个新常数（规范耦合 e、自耦合 λ）。而 κ,τ（螺旋曲率/挠率）在通量管解中【不出现】"
     " ⇒ 与 r22 的 C11「场论层无螺旋几何残留」同型：即便做成，也不是 TUFT 的成就，"
     "而是把标准机制外挂进框架。这是路线 C 唯一未被否证的分支，代价是外挂而非内生。",
     numbers={"new_fields": 2, "new_constants": 2, "kappa_tau_role": "none"})

# G16：λ 的量纲
# [∇²κ] = L⁻²·L⁻¹ = L⁻³；[κ³] = L⁻³ ⇒ [λ] 无量纲
dim_lap_kappa = (Fr(-3), Fr(0), Fr(0))   # (L, M, T) 指数：L^-3
dim_kappa3 = (Fr(-3), Fr(0), Fr(0))
dim_lambda = tuple(a - b for a, b in zip(dim_lap_kappa, dim_kappa3))
emit("G16", "FAIL",
     "λ 为无量纲新常数 ⇒ +1 自由常数，复发 L5-F4（耦合常数外部输入）",
     "[∇²κ]=L⁻³，[κ³]=L⁻³ ⇒ [λ]=L⁰M⁰T⁰（无量纲）。路线 C 在引入一个新自由常数的同时"
     "仍不能产生禁闭（G13/G14）⇒ 付出代价而不得收益。参数账：外部输入 4 → 5。",
     numbers={"dim_lambda_LMT": [str(x) for x in dim_lambda], "external_inputs_after": 5})

# G17：叠加性代价的精密化（修正既有估计）
emit("G17", "CORRECTED",
     "代价精密化：非线性破坏的是「四力线性叠加」这 1 条，不是 L3 的 12 条 —— 既有估计需下修",
     "逐一核对 L3 的 12 项还原：力程 λ=1/μ、F_E/F_G 量级比、库仑/牛顿形式、洛伦兹力不做功、"
     "c²=1/(ε₀μ₀) 等 11 项【均不依赖线性叠加】（它们只依赖单个 Yukawa/库仑解的性质）；"
     "唯一依赖叠加的是「四力可直接相加」这条结构性宣称。⇒ r22 D06 与来料所称"
     "「叠加性破坏的连锁代价」应精确记为 1 项，而非整层失效。代价记账必须精确，不得夸大。",
     numbers={"L3_items": 12, "superposition_dependent": 1, "superposition_independent": 11})

# ================================================================ 段 IV：路线 D（α 锁定候选逐个否证）
ALPHA_EXP = Decimal("7.2973525693") * Decimal(10) ** -3
# 候选 i：驻波闭合 2πρ = n·(2πc/ω) ⇒ ρ = n c/ω；联立 c=ω√(ρ²+b²) ⇒ b²=ρ²(1/n²−1)
cand_i = []
for n in (1, 2, 3):
    coef = Fr(1, 1) / Fr(n * n) - 1      # b²/ρ²
    if coef < 0:
        cand_i.append({"n": n, "b2_over_rho2": str(coef), "verdict": "无实解"})
    elif coef == 0:
        cand_i.append({"n": n, "b2_over_rho2": "0", "alpha": "0", "verdict": "b=0 ⇒ α=0"})
    else:
        cand_i.append({"n": n, "b2_over_rho2": str(coef), "verdict": "正解但需复核"})
emit("G18", "FAIL",
     "D 项候选 i（一圈周长 = n 倍德布罗意波长）被否证：n=1 给 α=0，n≥2 无实解",
     "条件 2πρ = n·2π(c/ω) 与公设 c=ω√(ρ²+b²) 联立 ⇒ (c/ω)²=ρ²/n² 且 (c/ω)²=ρ²+b²"
     " ⇒ b² = ρ²(1/n²−1)。n=1 ⇒ b=0 ⇒ α=b/ρ=0（与观测 α=7.2974E−03 差 100%，且 b=0 使挠率恒零）；"
     "n≥2 ⇒ b²<0 无实解。⇒ 最自然的「驻波量子化」闭合条件不是锁定 α，而是【摧毁螺旋本身】。",
     numbers={"table": cand_i, "alpha_exp": fm(ALPHA_EXP)})

# 候选 ii：螺距闭合 2πb = n·2π(c/ω) ⇒ ρ² = b²(1/n²−1)
cand_ii = []
for n in (1, 2, 3):
    coef = Fr(1, 1) / Fr(n * n) - 1
    if coef < 0:
        cand_ii.append({"n": n, "rho2_over_b2": str(coef), "verdict": "无实解"})
    elif coef == 0:
        cand_ii.append({"n": n, "rho2_over_b2": "0", "verdict": "ρ=0 ⇒ α=∞"})
emit("G19", "FAIL",
     "D 项候选 ii（螺距 = n 倍德布罗意波长）被否证：ρ²=b²(1/n²−1) ≤ 0，无实数螺旋",
     "2πb=n·2π(c/ω) ⇒ b=n c/ω，代入 (c/ω)²=ρ²+b² 得 ρ²=b²(1/n²−1)：n=1 ⇒ ρ=0（圆柱半径为零、α=∞）；"
     "n≥2 ⇒ ρ²<0。⇒ 该候选同样不给 α=1/137，只给退化几何。",
     numbers={"table": cand_ii})

# 候选 iii：一圈弧长 = n 倍康普顿波长 ⇒ n = 2π ∉ ℤ
arc_len_over_lambdaC = 2 * math.pi
emit("G20", "FAIL",
     "D 项候选 iii（一圈弧长 = n 倍康普顿波长）被否证：它要求量子数 n=2π（非整数）",
     "圆柱螺旋一圈弧长 = 2π√(ρ²+b²)；公设给 √(ρ²+b²)=c/ω；康普顿波长 λ_C=ħ/(mc)=c/ω"
     "（因 ω=mc²/ℏ）⇒ 弧长 = 2π·λ_C ⇒ 等式 2πλ_C = nλ_C 要求 n=2π=6.283185307…，非整数"
     " ⇒ 该量子化条件【恒不可满足】（且与 α 无关，根本不含 α）。",
     numbers={"required_n": fm(Decimal(str(arc_len_over_lambdaC))), "n_integer": False})

# 候选 iv：κ=τ 对称点 ⇒ α=1
ratio_1_over_alpha = 1 / ALPHA_EXP
emit("G21", "FAIL",
     "D 项候选 iv（κ=τ 对称点）被否证：给 α=1，与观测差 137.04 倍",
     "若以「曲率=挠率」为几何特权点，则 α=τ/κ=1；观测（本册口径 α=τ/κ≈1/137）为 7.2974E−03"
     " ⇒ 差 1/α = 137.04 倍。且 κ=τ 在几何上无任何特权地位（L1 单位圆对任意 α 成立，见 r22 B06）。",
     numbers={"alpha_candidate": "1", "alpha_exp": fm(ALPHA_EXP),
              "ratio": fm(ratio_1_over_alpha)})

emit("G22", "FAIL",
     "D 项裁定升级：不只是「几何无约束」，而是「所有自然闭合候选一旦施加就破坏自洽或与观测矛盾」",
     "既有 D 项结论（α 严格自由）本册复核通过、不重算。净增量 = 四个最自然的锁定候选"
     "（周长驻波 / 螺距驻波 / 弧长量子化 / κ=τ 对称点）被逐个机器否证：分别给 α=0、无实解、"
     "要求非整数量子数 n=2π、α=1（差 137 倍）。⇒ 路线 D 应从「继续寻找」改判为"
     "「已知候选全部撞墙，继续寻找等价于新增未受支持的公设」⇒ 建议关闭。",
     numbers={"candidates_tested": 4, "candidates_surviving": 0})

# ================================================================ 段 V：四选项代价矩阵与裁决
matrix = [
    {"option": "A 约束嵌入", "new_constants": 0, "L3_lost": "12（全部中心势）",
     "keeps_mu": "否（μ=0 必需）", "superposition": "保留", "verdict": "FAIL"},
    {"option": "B 非齐次源", "new_constants": "1（σ）", "L3_lost": "1（剩余核力力程）+ 引力/电磁（若走模承载）",
     "keeps_mu": "否（μ 被对消）", "superposition": "保留", "verdict": "FAIL（恒等式复读）"},
    {"option": "C 非线性", "new_constants": "1（λ）；真通量管需 2", "L3_lost": "1（四力叠加）",
     "keeps_mu": "是", "superposition": "破坏", "verdict": "FAIL（无线性解）/ 外挂通量管 BOUNDARY"},
    {"option": "D 锁 α", "new_constants": "0（但候选全部撞墙）", "L3_lost": "0",
     "keeps_mu": "是", "superposition": "保留", "verdict": "FAIL（4 候选全否证）"},
]
emit("G23", "INFO",
     "四选项代价矩阵（机器记账，供用户裁决，本册不代选）",
     "逐项给出：新增常数 / 丢失的 L3 项 / 是否保留力程参数 μ / 叠加性 / 判定。"
     "关键交叉：A 与 B 都【不能保留 μ】（前者因解析性强制调和，后者因源项对消）"
     " ⇒ 它们与 L2 的有限力程结构直接冲突，代价远大于来料/既有册的估计。",
     numbers={"matrix": matrix})

emit("G24", "BOUNDARY",
     "唯一未被否证的分支：把禁闭作为【外挂的通量管机制 + 显式登记的外部输入】，并把框架定位为 EFT",
     "四条路线在本册全部撞墙，唯一存活形态不是「修复」，而是【承认边界】："
     "① 把 σ（与 g_s, α_EM, g_W, G 并列）登记为 Wilson 型外部参数；"
     "② 禁闭不作为螺旋几何的内生结果，而明确标注「框架作用域 = 三力 + 一个有效剩余核力」"
     "（与 r23 P01「书名四力不成立」一致）；③ 若要内生禁闭，唯一已知结构是 Abelian Higgs 通量管（G15），"
     "代价是 +2 场 +2 常数且 κ,τ 不参与 ⇒ 属外挂非内生。此为既有 D 项「EFT 定位」建议的独立背书。",
     numbers={"external_inputs": 5, "surviving_branch": "EFT + external confinement"})

emit("G25", "CORRECTED",
     "对既有 S16 四篇攻坚产物的三处订正登记（不擅改他人文件，仅登记）",
     "① A 项「约束 ⟺ W 全纯」过断言（G01：3D 反例 ρ=x,b=z 满足约束但非全纯）⇒ 应降级为单向「全纯 ⟹ 约束」；"
     "② A 项开放项「有质量力程嵌入待完成」改判为不可能（G04/G05，射程见 G06）；"
     "③ B 项「非齐次源修复成立，残差 0」属恒等式复读（G07：源依赖解本身，μ²κ 精确对消）"
     "与「模承载兼容修复」未闭合（G10：柱半径错配 + 分量退化为无源线性场 + 模无场方程）。"
     "⇒ 三条订正均不推翻既有册的诚实方向，但把三处「成立/可行」读数下修为「不成立/未闭合」。",
     numbers={"corrections": 3})

emit("G26", "INFO",
     "若转写论文 Discussion 章节：本册可直接引用的局限/假设/开放问题条目化骨架",
     "局限（硬）：F1 禁闭不在齐次 Proca 体系内；F2 G 循环定义；F3 α 无内部约束且四个自然候选被否证；"
     "F4 耦合常数（+σ）全部外部输入。假设（须显式声明）：类光螺旋公设；场版垂直原理为构造条件而非推论；"
     "κ,τ 由位形场 (ρ,b) 经 κ=ρ/D, τ=b/D 生成。开放问题：有质量力程与垂直原理的相容性（本册判否）、"
     "禁闭的动力学来源（本册判需外挂）、σ 的第一性。⇒ 三节骨架均可直接落到条目，无需再推导。",
     numbers={"sections": 3})

emit("G27", "CORRECTED",
     "本册自抓缺陷：力程公式首版误写 λ=ħc/(mc²) 为 (ħc)/(m/c²) 形式（多除 c²），已修正并加交叉印证 guard",
     "首版写 lam=HBARC/(M*MEV/CC**2) 会小 c²≈8.99e16 倍。修正是必须的：λ=ħ/(mc)=(ħc)/(mc²)，"
     "mc² 以焦耳计。教训复现（库内已多次）：量纲类断言必须由机器 guard 兜底 —— "
     "本册 guard 用 r22/r23 的独立读数 λ(π⁰)=1.461933E−15 m 做交叉印证，正是为此设的。",
     numbers={"lambda_pi0_m": fm(lam_pi0), "lambda_W_m": fm(lam_W)})

emit("G28", "INFO",
     "射程与红线声明",
     "本册全部结论限于「垂直原理框架的 Proca/位形场版本 + 已知解族（全纯族 / 平面调和反例族 / 球对称穷尽）」；"
     "未覆盖一般 3D 非球对称非平面调和解（G06）。数值为机器复算，量纲层用 Fraction 精确算术。"
     "红线：数学自洽 ≠ 实验证实；本册否证的是【修复路线】，不是 QCD 本身（QCD 禁闭是既定事实，"
     "本册只判它不能由该框架的齐次 Proca 内生）。",
     numbers={"known_families": 3})

# ================================================================ 自检（guard）
# 1) 拉普拉斯差分器：调和函数应为 0
g1 = max(abs(lap3(k_c, *p)) for p in PTS)
scale1 = max(abs(k_c(*p)) for p in PTS)
guard("lap_control_harmonic", g1 / scale1 < 1e-4,
      "∇²[x/(x²+z²)] 应为 0（调和）", g1 / scale1)

# 2) 拉普拉斯差分器：∇²r = 2/r
fr = lambda x, y, z: math.sqrt(x * x + y * y + z * z)
errs = []
for p in PTS:
    r = fr(*p)
    errs.append(abs(lap3(fr, *p) - 2.0 / r) / (2.0 / r))
guard("lap_control_sphere_r", max(errs) < 1e-4, "∇²r 应等于 2/r", max(errs))

# 3) 梯度差分器
fg = lambda x, y, z: x * x * y
pg = (1.5, 0.8, 0.3)
gexact = (2 * pg[0] * pg[1], pg[0] ** 2, 0.0)
gdiff = grad3(fg, *pg)
gerr = max(abs(a - b) for a, b in zip(gexact, gdiff)) / max(abs(v) for v in gexact)
guard("grad_control", gerr < 1e-6, "∇(x²y) 与解析值应一致", gerr)

# 4) 全纯族必须满足约束（判据分辨力：不能恒判失败）
guard("holo_satisfies_constraint", worst_holo < 1e-6, "全纯族约束残差应 ~0", worst_holo)

# 5) 随机非全纯场必须违反约束（判据分辨力：不能恒判通过）
_rho_r = lambda x, y, z: 1.0 + 0.3 * x + 0.2 * y * y + 0.1 * z
_b_r = lambda x, y, z: 0.5 + 0.1 * y + 0.4 * z + 0.05 * x * x
res_rand = constraint_residual(_rho_r, _b_r, PTS)
guard("random_violates_constraint", res_rand > 1e-3, "随机场约束残差应显著非零", res_rand)

# 6) G01 反例的 CR 残差必须非零
guard("cr_counterexample_nonzero", cr_c > 0.5, "ρ=x,b=z 的 CR 残差应 =1", cr_c)

# 7) 径向剖型必须违反约束
guard("radial_violates_constraint", worst_radial > 1e-3, "径向非平凡剖型应违反约束", worst_radial)

# 8) G07 的恒等残差确实为 0（残差为 0 恰恰是「零信息量」的证据，不是「修复成功」的证据）
guard("source_identity_is_exact", worst_canc < Decimal("1E-50"),
      "S 与 (∇²−μ²)(σr) 的差应为 0（恒等式）", fm(worst_canc))


# 9) 分类器正向对照：σr 的控制方程必须被识别为 LINEAR_GROWTH
def shoot_control(rmax=60.0, dr=1e-3, r0=1.0, sigma=1.0):
    """控制组：κ''+2κ'/r = 2σ/r 的真解 κ=σr（检验分类器不是恒判 FAIL）"""
    def f(r, k, v):
        return 2.0 * sigma / r - 2.0 * v / r
    r, k, v = r0, sigma * r0, sigma
    n = int((rmax - r0) / dr)
    samples = {}
    for i in range(n):
        a1 = f(r, k, v)
        a2 = f(r + dr / 2, k + dr / 2 * v, v + dr / 2 * a1)
        a3 = f(r + dr / 2, k + dr / 2 * (v + dr / 2 * a1), v + dr / 2 * a2)
        a4 = f(r + dr, k + dr * (v + dr / 2 * a2), v + dr * a3)
        k_new = k + dr / 6 * (6 * v + dr * (a1 + a2 + a3))
        v_new = v + dr / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        r += dr
        k, v = k_new, v_new
        for mark in (30.0, 40.0, 50.0, 60.0):
            if mark not in samples and r >= mark - 1e-9:
                samples[mark] = k / r
    ratios = [samples.get(m, k / r) for m in (30.0, 40.0, 50.0, 60.0)]
    spread = max(ratios) - min(ratios)
    scale = max(abs(x) for x in ratios)
    return ("LINEAR_GROWTH" if spread / scale < 1e-2 else "NOT_DETECTED"), spread / scale


cls_ctrl, metric_ctrl = shoot_control()
guard("classifier_detects_linear_growth_on_control", cls_ctrl == "LINEAR_GROWTH",
      "分类器等标必须能识别真线性增长解", {"class": cls_ctrl, "metric": metric_ctrl})

# 10) σ 换算两条路径一致
sigma_path2 = SIGMA_QCD_GEV2 / (HBARC / (Decimal("1000") * MEV) / Decimal("1e-15")) * GEV_PER_FM_TO_N
guard("sigma_conversion_two_paths", abs(sigma_N - sigma_path2) / sigma_N < Decimal("1E-40"),
      "σ 的两条换算路径应一致", fm(abs(sigma_N - sigma_path2) / sigma_N))

# 11) λ(π⁰) 与 r22/r23 独立读数交叉印证
LAM_PI0_REF = Decimal("1.461933E-15")
rel = abs(lam_pi0 - LAM_PI0_REF) / LAM_PI0_REF
guard("lambda_pi0_crosscheck_r22_r23", rel < Decimal("1E-5"),
      "λ(π⁰) 应与 r22/r23 读数 1.461933E−15 m 一致", fm(rel))

# 12) 候选 i 的代数（n=1 ⇒ b²/ρ²=0）精确
guard("alpha_candidate_i_algebra", float(cand_i[0].get("b2_over_rho2", "1")) == 0.0,
      "候选 i 的 n=1 分支应给 b²=0", cand_i[0])

# 13) 物理对照：墨西哥帽分支的渐近值应等于解析真空期望 μ/√λ（证明积分器与势型归属都正确）
vev_cmp = []
for row, (name, mu, lam, sign, k0, vp) in zip(shoot_rows, cases):
    if row.get("kappa@60") is not None and row["class"] in ("CONSTANT", "DECAY_TO_ZERO"):
        vev = mu / math.sqrt(lam)
        vev_cmp.append({"case": name, "vev_analytic": round(vev, 9),
                        "kappa60": round(row["kappa@60"], 9),
                        "rel": abs(abs(row["kappa@60"]) - vev) / vev})
worst_vev = max(c["rel"] for c in vev_cmp) if vev_cmp else 1.0
guard("vacuum_expectation_matches_analytic", worst_vev < 0.05,
      "墨西哥帽分支的 κ(60) 应趋近解析真空期望 μ/√λ（趋近中，容差 5%）",
      {"worst_rel": worst_vev, "table": vev_cmp})
KEY["vev_comparison"] = vev_cmp

# 14) 条目编号唯一
ids = [e["id"] for e in ENTRIES]
guard("entry_ids_unique", len(ids) == len(set(ids)), "条目编号不得重复", len(ids))

# ================================================================ 汇总与落盘
counts = {}
for e in ENTRIES:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
n_guard_ok = sum(1 for g in GUARDS if g["ok"])

KEY.update({
    "lambda_pi0_m": fm(lam_pi0),
    "lambda_W_m": fm(lam_W),
    "sigma_N": fm(sigma_N),
    "sigma_over_hbarc_m^-2": fm(sigma_over_hbarc),
    "kappa_at_1fm": fm(kappa_at_1fm),
    "curvature_radius_fm": fm(radius_of_curvature_fm),
    "cr_residual_counterexample": cr_c,
    "constraint_residual_counterexample": res_c,
    "worst_radial_violation": worst_radial,
    "n_linear_growth_found": n_linear,
    "alpha_exp": fm(ALPHA_EXP),
    "one_over_alpha": fm(ratio_1_over_alpha),
    "required_n_arc": fm(Decimal(str(arc_len_over_lambdaC))),
})

payload = {
    "meta": {
        "tag": TAG, "round": "r25", "date": "2026-10-10",
        "engine": os.path.basename(__file__),
        "python": sys.version.split()[0],
        "stdlib_only": True,
        "scope": "垂直原理四力统一：禁闭路线 + A/B/C/D 四选项攻坚裁定（对既有 S16 攻坚的元审计 + 净增量）",
        "not_additive_with": ["r22（48 条目）", "r23（33 条目）"],
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

lines = []
lines.append("# TUFT 垂直原理四力统一 · 禁闭与 A/B/C/D 四选项攻坚裁定（r25）· 数据产物")
lines.append("")
lines.append("- 条目 %d：%s" % (len(ENTRIES), " / ".join("%s %d" % (k, v) for k, v in sorted(counts.items()))))
lines.append("- 自检：%d/%d" % (n_guard_ok, len(GUARDS)))
lines.append("")
for e in ENTRIES:
    lines.append("## %s [%s] %s" % (e["id"], e["verdict"], e["title"]))
    lines.append(e["detail"])
    lines.append("")
lines.append("## 自检")
for g in GUARDS:
    lines.append("- [%s] %s（%s）" % ("OK" if g["ok"] else "NG", g["name"], g["value"]))
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
sys.exit(0)
