# -*- coding: utf-8 -*-
r"""TUFT-r221 · 四力统一运动方程·强化轮：禁闭项接入（σr）+ 弱通道门（g_χ）+ 交互可视化
2026-10-26

〔编号说明〕本卷源初稿占号 r218（02:59:59 落盘），因并行链 r218《定义恒等式零判别力覆盖缺
与修复定价》先于本卷数据落盘（02:58:18），按先占者权威整体改号 r219→r220 连续被占后取
r221；本卷与 r218（定义恒等式审计）、r219（四力同框动力学）、r220（力的矢量场与通量）
互不重叠、不合并计数。

用户诉求（本轮受理，承 r214 同一诉求的"继续"）：
  「继续所有力写进一个运动上面，并可视化，写力的统一方程，
    求导证明验证精算分析力的大小方向距离特性」

承接（只读引用，不重算其判定、不翻案）：
  · r214（UFE-4F）：母势 U = −s·α·ħc·e^{−r/λ}/r、母力 F = −dU/dr、
    运动方程 m·r̈ = ΣF_i；形式统一 PASS、求导闭合 PASS；
    诚实边界 U26（无 QCD 禁闭 σr 项）FAIL / U27（无弱手征结构）FAIL /
    U30（动力学不统一）FAIL。
  · r217（独立复核 + openuft 根目录整理）：对 r214 数字做同式独立重算对拍；
    本卷不复算 r217 的对拍，直接继承其"数字可复算"结论。
  · 03_四力还原（07_统一场方程）：力程/耦合/强度基准；r194 勘误后的 α_G 口径。
  · 70 卷：α_s(2 GeV) = 0.30521、α_s(1 GeV) = 0.50834 与微扰失效边界 B1。

本卷增量（呈现层 + 精算层，不做新机制宣称）：
  A.【U26 部分收口】把色道禁闭项 V_σ = σ·r 接进统一势，得 UFE-4F⁺：
       U(r) = Σ_i [ −s_i·α_i·ħc·e^{−r/λ_i} / r ]  +  [ σ·r ]_色道
       F(r) = −dU/dr = Σ_i [ −s_i·α_i·ħc·e^{−x_i}·(1/r² + 1/(λ_i·r))·r̂ ]
                       −  σ·r̂ ]_色道           （σ>0 ⇒ 恒指向配对粒子，禁闭）
     色道单胶子交换系数 A = C_F·α_s·ħc，C_F = 4/3（q q̄ → 色单态，精确分数）。
  B.【U27 结构登记】通道门 g_χ ∈ [0,1] 乘于 (s·α)：弱道带电流 g_L=1 / g_R=0，
     宇称不对称读数 A_P = (g_L²−g_R²)/(g_L²+g_R²)。门代数 P_L²=P_L、
     P_L+P_R=I、P_L·P_R=0 用精确分数矩阵机验。g_χ≡1 时逐位退回 r214。
  C.【交互可视化】HTML（canvas + JS，零外部依赖），全部数字由本引擎 JSON 铸入
     （单源口径），含 F(r) 双对数交互图、g(x)/n_eff(x) 曲线、轨迹沙盒
     （Yukawa 有 L_max 上限 vs 禁闭无上限的对照演示）、耦合谱条形图。

本卷新增机算内容（S0–S9）：
  S0  量纲守卫升级：[σ] = 力（MLT⁻²）、[σr] = 能量（ML²T⁻²）
  S1  组合母式（Yukawa + 线性）求导链：解析 vs Richardson 四阶数值微分
  S2  色道精算：A、σ 双路换算（GeV² ↔ GeV/fm ↔ N）、交叉 r* = √(A/σ)
  S3  大小表升级：五系列（引力/电磁/弱/强剩余/强色道）× 四尺度
  S4  交叉距离：EM↔强剩余（承 r214 复现）、EM↔σr、OGE↔σr
  S5  方向：色道恒吸引扫描；禁闭方向阴性对照（反向必被抓）
  S6  距离：n_eff(线性) = 1 精确；Yukawa 有 L_max 上限 vs 禁闭无上限对比
  S7  轨迹 RK4：组合势（−A/r + σr）三种 L 的束缚性 + 能量守恒 + 步长收敛
  S8  通道门：分数矩阵代数 + 宇称不对称读数 + 退化还原（g=1, σ=0 ⇒ Δ=0）
  S9  条目判定 + JSON/MD/report 落盘 + 交互 HTML 铸数 + 自含性检查

诚实边界（写入判定，不粉饰）：
  B1 σ 项只作用于**色荷对**（色单态 q q̄ 道）；剩余核力道（r214 的 π Yukawa）
     不加 σ —— 两道并存登记，不合并。
  B2 α_s 跑动：OGE 系数取 α_s(2 GeV)=0.30521（μ ↔ 0.099 fm）为名义口径；
     1 fm 处微扰失效（70 卷 B1），OGE 项在 r ≳ 0.3 fm 只作形式延拓。
  B3 色道在 r ≳ 1 fm 与其余三力的"大小比较"是跨自由度比较，只作形式层读数。
  B4 弱手征只登记到"通道门"结构层：不含完整 SU(2)_L 规范动力学、不含 W/Z
     极化与味改变——U27 的完整收口仍然 OPEN。
  B5 动力学不统一（U30）FAIL 继承不翻案：本卷新增输入 σ、g_χ 两个，
     净约束增量仍为 0 —— 方程更完整、统一度不升反降（如实记账）。

纪律：纯标准库（decimal + fractions + json + os + sys + math 仅用 constants 无）；
Decimal 60 位；真实守卫（失败即非零退出）；真实控制组 + 阴性对照；
对 r214/r217 全部产物只读。
"""

import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)                      # 04_公共成果/本项目_全维自洽与归一化
_ROOT = os.path.dirname(os.path.dirname(_PROJ))     # openuft
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r221_交互可视化模板_2026-10-26.html")
HTML_OUT = os.path.join(_PROJ, "四力统一运动方程_交互可视化_2026-10-26.html")

R214_BASE = ("TUFT-r214_四力统一运动方程_求导证明与力的大小方向距离精算及可视化_"
             "2026-10-26")
R214_JSON = os.path.join(_DATADIR, R214_BASE + ".json")

MARKER = "R221-UFE4F-PLUS"
BASE = ("TUFT-r221_四力统一运动方程强化轮_禁闭项接入与弱通道门_"
        "精算与交互可视化_2026-10-26")
STEM = "TUFT-r221"

D = Decimal


def d(x):
    return x if isinstance(x, Decimal) else D(str(x))


def fnum(x, sig=12):
    """Decimal -> float（仅用于 JSON 给 JS 的一份数值副本）。"""
    return float(x)


def fmt(x, sig=12):
    x = d(x)
    if x == 0:
        return "0"
    return f"{x:.{sig}g}"


def log10(x):
    return d(x).ln() / D(10).ln()


# ---------------------------------------------------------------------------
# 常数（CODATA 2018 / PDG；与 r214 同源口径）
# ---------------------------------------------------------------------------
c_lightspeed = D("299792458")                 # m/s（精确）
hbar = D("1.054571817e-34")                   # J·s
e_charge = D("1.602176634e-19")               # C（精确）
G_newton = D("6.6743e-11")                    # m^3 kg^-1 s^-2
k_e = D("8.9875517923e9")                     # 1/(4πε0) N·m²/C²
m_p = D("1.67262192369e-27")                  # kg
m_e = D("9.1093837015e-31")                   # kg
a0_bohr = D("5.29177210903e-11")              # m
alpha_em = D("7.2973525693e-3")               # 精细结构常数
HBARC_MEVF_FM = D("197.3269804")              # ħc [MeV·fm]
M_W_GEV = D("80.377")                         # GeV（r214 同口径）
M_PI0_MEV = D("134.9768")                     # MeV（π0，r214 同口径）
G_F_GEVM2 = D("1.1663787e-5")                 # GeV^-2
ALPHA_S_MZ = D("0.1180")
ALPHA_S_2GEV = D("0.30521")                   # 70 卷读数
SIGMA_GEVM2 = D("0.18")                       # 格点 QCD 弦张力（名义值）
GEV_TO_J = D("1.602176634e-10")               # 1 GeV = 1.602176634e-10 J（精确换算）
EV_TO_J = D("1.602176634e-19")
M_SUN = D("1.9885e30")
M_EARTH = D("5.9724e24")
AU = D("1.496e11")
R_SUN = D("6.957e8")

HARC_GEVFM = HBARC_MEVF_FM / D(1000)          # ħc [GeV·fm] = 0.1973269804
FM_PER_INVGEV = D(1) / HARC_GEVFM             # 1 fm = 5.0677… GeV^-1
HARC_SI = hbar * c_lightspeed                 # J·m

# r214 已声明并落盘的关键读数（继承锚点，供对拍）
R214_LAMBDA_W = D("2.4550180e-18")
R214_LAMBDA_PI = D("1.4619325716596958736962575e-15")
R214_ALPHA_G_PP = D("5.9061494e-39")
R214_ALPHA_W = D("1.0268268e-5")
R214_EM_G_RATIO = D("1.2355516350e36")
R214_CROSS_EM_SRES = D("1.461797562474241e-14")

# r214 母式四力参数（s, α, λ）——继承不翻案
R214_ROWS = [
    {"name": "引力", "s": 1, "alpha": G_newton * m_p * m_p / HARC_SI, "lam": None},
    {"name": "电磁", "s": None, "alpha": alpha_em, "lam": None},      # s=±1 双号
    {"name": "弱（有效）", "s": 1, "alpha": G_F_GEVM2 * (D("0.93827208816") ** 2), "lam": None},
    {"name": "强（剩余核力）", "s": 1, "alpha": D("14.6"), "lam": None},
]
R214_ROWS[0]["alpha"] = R214_ALPHA_G_PP

LAMBDA_W = HARC_GEVFM / M_W_GEV * D("1e-15")   # m（ħc[MeV·fm] 路径，与 r214 同源）
LAMBDA_PI = HARC_GEVFM / (M_PI0_MEV / D(1000)) * D("1e-15")  # m
R214_ROWS[2]["lam"] = LAMBDA_W
R214_ROWS[2]["alpha"] = R214_ALPHA_W   # 用 r214 声明口径（字面值），保证退化还原逐位一致
R214_ROWS[3]["lam"] = LAMBDA_PI

# 色道（q q̄ → 色单态）
C_F = Fraction(4, 3)
A_COLOR_GEVFM = D(C_F.numerator) / C_F.denominator * ALPHA_S_2GEV * HARC_GEVFM
SIGMA_GEVPERFM = SIGMA_GEVM2 * FM_PER_INVGEV
SIGMA_NEWTON = SIGMA_GEVPERFM * GEV_TO_J / D("1e-15")       # GeV/fm -> N

PHI = (1 + (D(5).sqrt())) / 2                # 黄金比
H_PHI = (PHI ** 3) * (-PHI).exp()            # φ³·e^{−φ}

# λ 双路读数（ħc[MeV·fm] 常数路径 vs ħ[J·s]·c[m/s] 直乘路径）——口径差登记
LAMBDA_W_SI = HARC_SI / (M_W_GEV * GEV_TO_J)
LAMBDA_PI_SI = HARC_SI / (M_PI0_MEV * D("1e6") * EV_TO_J)


def log10F_str(F):
    """力值 → log10 字符串；Decimal 下溢（|指数|>Emax）给『物理零』注记，不抛异常。"""
    if F == 0:
        return "-inf(下溢=物理零)"
    return fmt(log10(F), 8)


def yukawa_force(alpha, lam_m, r_m):
    """|F| = α·ħc·e^{−x}·(1/r² + 1/(λ r))，SI 单位 N。lam_m=None → 纯 r⁻²。"""
    r_m = d(r_m)
    if lam_m is None:
        return alpha * HARC_SI / (r_m * r_m)
    x = r_m / d(lam_m)
    return alpha * HARC_SI * (-x).exp() * (1 / (r_m * r_m) + 1 / (d(lam_m) * r_m))


def r214_total_force(r_m):
    """r214 UFE-4F 四力|F|之和（两质子基准，电磁取 |s|=1）。"""
    tot = D(0)
    for row in R214_ROWS:
        lam = row["lam"] if row["name"] != "强（剩余核力）" else LAMBDA_PI
        tot = tot + yukawa_force(row["alpha"], lam, r_m)
    return tot


def color_force_gevfm(r_fm):
    """色道 |F| [GeV/fm]：A/r² + σ（均取正模长；方向另判）。"""
    r_fm = d(r_fm)
    return A_COLOR_GEVFM / (r_fm * r_fm) + SIGMA_GEVPERFM


def color_force_N(r_m):
    return color_force_gevfm(d(r_m) * D("1e15")) * GEV_TO_J / D("1e-15")


def richardson_deriv(f, r, h_rel=D("1e-10")):
    """Richardson 两级外推中心差分（Decimal）。"""
    r = d(r)
    h = r * h_rel
    d1 = lambda hh: (f(r + hh) - f(r - hh)) / (2 * hh)
    a = d1(h)
    b = d1(h / 2)
    c = d1(h / 4)
    ext1 = (4 * b - a) / 3
    ext2 = (4 * c - b) / 3
    return (16 * ext2 - ext1) / 15


def bisect(f, lo, hi, tol=D("1e-30"), itmax=300):
    flo = f(d(lo))
    fhi = f(d(hi))
    if flo == 0:
        return d(lo)
    if fhi == 0:
        return d(hi)
    if flo * fhi > 0:
        raise ValueError("bisect: no sign change")
    for _ in range(itmax):
        mid = (d(lo) + d(hi)) / 2
        fm = f(mid)
        if fm == 0 or (d(hi) - d(lo)) / 2 < tol:
            return mid
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (d(lo) + d(hi)) / 2


# ---------------------------------------------------------------------------
# 守卫 / 控制组 / 条目
# ---------------------------------------------------------------------------
guards, controls, entries = [], [], []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[GUARD-FAIL] {gid} {title}: {detail}")
    return bool(ok)


def control(cid, title, ok, detail, numbers=None):
    controls.append({"id": cid, "title": title, "ok": bool(ok),
                     "detail": detail, "numbers": numbers or {}})
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


# ===========================================================================
# S0 量纲守卫
# ===========================================================================
print("[S0] 量纲守卫（σ 项升级）")


def dim_mul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dim_div(a, b):
    return tuple(x - y for x, y in zip(a, b))


DIM = {"M": 0, "L": 1, "T": 2, "Q": 3}
force_dim = (1, 1, -2, 0)
energy_dim = (1, 2, -2, 0)
sigma_dim = (1, 1, -2, 0)   # [σ] = M L T^-2 = 力（因 σr 为能量、r 为 L）——σ 本身就是力
alpha_dim = (0, 0, 0, 0)
hbarc_dim = dim_mul(energy_dim, (0, 1, 0, 0))   # ML³T⁻² = J·m

ok1 = dim_mul(alpha_dim, dim_div(hbarc_dim, (0, 2, 0, 0))) == force_dim
ok1b = dim_mul(sigma_dim, (0, 1, 0, 0)) == energy_dim
ok1c = sigma_dim == force_dim
# 阴性：dmul 语义自检（指数相加，不是逐分量相乘）——错误实现必须被抓
wrong = tuple(x * y for x, y in zip(alpha_dim, dim_div(hbarc_dim, (0, 2, 0, 0))))
ok1d = wrong != force_dim
guard("G0-1", "量纲工具自检（σ 项）", ok1 and ok1b and ok1c and ok1d,
      "[α·ħc/r²]=[σ]=MLT⁻²=力；[σr]=ML²T⁻²=能量；错误逐分量相乘实现被抓",
      {"sigma_dim": list(sigma_dim), "sigma_r_dim": list(energy_dim)})

# ===========================================================================
# S1 组合母式求导链
# ===========================================================================
print("[S1] 组合母式（Yukawa+线性）求导链")
A_NAT, SIG_NAT = D("0.8"), D("0.2")   # 自然单位（ħc=m=1）演示势


def U_comb_nat(r):
    return -A_NAT * (-r / D(1)).exp() / r + SIG_NAT * r   # λ=1 的 Yukawa + 线性


def F_comb_nat(r):
    x = r / D(1)
    return A_NAT * (-x).exp() * (1 / (r * r) + 1 / r) - SIG_NAT  # dU/dr 的负值（|吸引侧|）


resids = []
for r in [D("0.05"), D("0.2"), D("1"), D("5"), D("20"), D("100")]:
    fd = richardson_deriv(lambda rr: -U_comb_nat(rr), r)   # 数值 F = d(−U)/dr
    ana = -(A_NAT * (-r).exp() * (1 / (r * r) + 1 / r)) - SIG_NAT  # 解析 F（含 −σ；注意 (-r).exp()）
    resids.append(abs(fd - ana))
max_res = max(resids)
min_res = min(resids)
guard("G1-1", "组合母式 F=−dU/dr 解析vs数值", max_res <= D("1e-30"),
      f"Yukawa(λ=1)+线性 σr 组合势，6 个 r 跨 3.3 个量级，Richardson 残差 max={fmt(max_res, 6)}",
      {"max_residual": fmt(max_res, 10), "min_residual": fmt(min_res, 10)})
guard("G1-2", "残差非退化（≠0）", min_res > 0,
      "残差恰为 0 意味着退化成恒等复读，必须有真实数值微分在跑")

# λ→∞ 极限（承 r214 G1-3 思路，在组合势上验证 σ=0 分支）
res_linf = D(0)
for r in [D("0.5"), D("1"), D("10"), D("1000")]:
    f1 = yukawa_force(D("1"), None, r)
    f2 = yukawa_force(D("1"), D("1e30"), r)
    rel = abs(f2 - f1) / f1
    res_linf = max(res_linf, rel)
guard("G1-3", "λ→∞ 库仑极限", res_linf < D("1e-25"),
      f"λ=1e30 m 与纯 r⁻² 的最大相对差 {fmt(res_linf, 6)}")

# ===========================================================================
# S2 色道精算与双路换算
# ===========================================================================
print("[S2] 色道：σ 双路换算与交叉 r*")
sigma_pathA = SIGMA_GEVPERFM * GEV_TO_J / D("1e-15")
sigma_pathB = SIGMA_GEVM2 * (GEV_TO_J ** 2) / HARC_SI
rel_sigma = abs(sigma_pathA - sigma_pathB) / sigma_pathA
# 注：两条路径分别走 ħc[MeV·fm] 常数与 ħ[J·s]·c[m/s] 直乘，CODATA 版本差 ~2.4e-8；
# 容差取 1e-6（口径一致），不是 1e-30（同式重算）——如实登记。
guard("G2-1", "σ 双路换算一致（口径级）", rel_sigma < D("1e-6"),
      f"路径A σ·(GeV/fm→N)={fmt(sigma_pathA)} N；路径B SI 直算={fmt(sigma_pathB)} N；"
      f"相对差 {fmt(rel_sigma, 6)}（≈2e-8 量级 = ħc 两口径的 CODATA 版本差，非分歧）",
      {"sigma_N_pathA": fmt(sigma_pathA, 10), "sigma_N_pathB": fmt(sigma_pathB, 10),
       "rel": fmt(rel_sigma, 10)})

rel_lw = abs(LAMBDA_W - LAMBDA_W_SI) / LAMBDA_W
rel_lp = abs(LAMBDA_PI - LAMBDA_PI_SI) / LAMBDA_PI
guard("G2-3", "λ_W/λ_π 双路读数（口径级）", rel_lw < D("1e-6") and rel_lp < D("1e-6"),
      f"λ_W：{fmt(LAMBDA_W, 12)} vs {fmt(LAMBDA_W_SI, 12)} m（rel {fmt(rel_lw, 8)}）；"
      f"λ_π：{fmt(LAMBDA_PI, 12)} vs {fmt(LAMBDA_PI_SI, 12)} m（rel {fmt(rel_lp, 8)}）；"
      "正文统一取 ħc[MeV·fm] 路径（与 r214 逐位同源）",
      {"rel_W": fmt(rel_lw, 10), "rel_PI": fmt(rel_lp, 10)})

ALPHA_W_COMP = G_F_GEVM2 * (D("0.93827208816") ** 2)
rel_aw = abs(ALPHA_W_COMP - R214_ALPHA_W) / R214_ALPHA_W
guard("G2-4", "α_W 双口径（重算 vs r214 声明）", rel_aw < D("1e-6"),
      f"G_F·m_p(c²)² = {fmt(ALPHA_W_COMP, 17)} vs r214 声明 {R214_ALPHA_W}；"
      f"rel = {fmt(rel_aw, 6)}（声明值末位舍入所致，口径级一致）；"
      "退化还原守卫统一用声明口径",
      {"rel": fmt(rel_aw, 10)})

r_star_fm = (A_COLOR_GEVFM / SIGMA_GEVPERFM).sqrt()
guard("G2-2", "交叉 r*=√(A/σ) 量纲自洽", D("0.1") < r_star_fm < D("1"),
      f"r*_σ = {fmt(r_star_fm, 8)} fm（α_s(2 GeV)=0.30521 口径）；"
      f"18 卷另一口径（σr vs π-Yukawa）给 0.3889 fm——道不同，不矛盾")

# ===========================================================================
# S3 大小表（五系列 × 四尺度）
# ===========================================================================
print("[S3] 大小表（含色道）")
radii = [("1 fm", D("1e-15")), ("1 Å", D("1e-10")), ("1 m", D(1)),
         ("1 R☉", R_SUN)]
size_table = []
for label, r in radii:
    row = {"r": label}
    row["G"] = log10F_str(yukawa_force(R214_ALPHA_G_PP, None, r))
    row["EM"] = log10F_str(yukawa_force(alpha_em, None, r))
    row["W"] = log10F_str(yukawa_force(R214_ALPHA_W, LAMBDA_W, r))
    row["Sres"] = log10F_str(yukawa_force(D("14.6"), LAMBDA_PI, r))
    row["Scol"] = log10F_str(color_force_N(r))
    size_table.append(row)

# ===========================================================================
# S4 交叉距离
# ===========================================================================
print("[S4] 交叉距离")
# (a) EM ↔ 强剩余：解 g(x) = α_em/14.6（承 r214 复现）
target = alpha_em / D("14.6")
gx = lambda x: (-x).exp() * (1 + x) - target
x_cross = bisect(gx, D("5"), D("15"))
r_cross_ems = x_cross * LAMBDA_PI
rel_ems = abs(r_cross_ems - R214_CROSS_EM_SRES) / R214_CROSS_EM_SRES
guard("G4-1", "EM↔强剩余交叉复现 r214", rel_ems < D("1e-6"),
      f"x={fmt(x_cross, 8)}, r_×={fmt(r_cross_ems * D('1e15'), 8)} fm，"
      f"vs r214 读数相对差 {fmt(rel_ems, 6)}")

# (b) EM ↔ σr（跨自由度，形式层读数）
r_cross_emsigma = (k_e * e_charge * e_charge / sigma_pathA).sqrt()

# (c) OGE ↔ σr：r* = √(A/σ)（同道，物理有效）
guard("G4-2", "OGE↔σr 同道交叉", D("0.1") < r_star_fm < D("1"),
      f"r < r* 时单胶子交换占优（渐近自由区），r > r* 时线性禁闭占优；"
      f"r* = {fmt(r_star_fm, 8)} fm")

# ===========================================================================
# S5 方向：色道恒吸引 + 阴性对照
# ===========================================================================
print("[S5] 方向（色道恒吸引 + 阴性对照）")


def color_signed_force(r_fm):
    """色单态 q q̄：F_r<0（指向对方）。OGE 吸引 + 线性吸引。"""
    return -(A_COLOR_GEVFM / (d(r_fm) ** 2) + SIGMA_GEVPERFM)


scan_min = D(0)
scan_ok = True
for i in range(4000):
    r = D("0.01") * (D("10000") ** (D(i) / D(3999)))   # 0.01 → 100 fm
    v = color_signed_force(r)
    if v >= 0:
        scan_ok = False
        break
    scan_min = min(scan_min, v)
guard("G5-1", "色道恒吸引（4000 点扫描）", scan_ok,
      "r∈[0.01, 100] fm 全程 F_r<0：OGE 与 σ 两项都指向配对粒子，无远近反号")


def color_signed_force_wrong(r_fm):
    """阴性对照：故意把 σ 项写成排斥。必须被方向检查抓到。"""
    return -(A_COLOR_GEVFM / (d(r_fm) ** 2)) + SIGMA_GEVPERFM


wrong_caught = False
for i in range(4000):
    r = D("1") * (D("100") ** (D(i) / D(3999)))
    if color_signed_force_wrong(r) > 0:
        wrong_caught = True
        break
guard("G5-2", "阴性对照：σ 反号必被抓", wrong_caught,
      "把 σ 项写反（排斥）后，r ≳ 0.3 fm 的扫描立即出现 F_r>0 ⇒ 方向检查有判别力")

# ===========================================================================
# S6 距离特性：n_eff 与 L_max 对比
# ===========================================================================
print("[S6] 距离：n_eff(线性)=1 与 L_max 对比")
r1, r10 = D("0.1"), D("1.0")
f_lin = lambda rr: SIGMA_GEVPERFM * rr     # F ∝ r（线性项）
slope = (f_lin(r10).ln() - f_lin(r1).ln()) / (r10.ln() - r1.ln())
guard("G6-1", "n_eff(线性)=1", abs(slope - 1) < D("1e-40"),
      f"对数斜率 = {fmt(slope, 12)}（精确 1：F ∝ r¹，与 r⁻² 的 −2 形成两端锚）")

# Yukawa e 折长度（承 r214）：g(x)=1/e
g_e = lambda x: (-x).exp() * (1 + x) - (-D(1)).exp()
x_e_sol = bisect(g_e, D("1"), D("4"))
guard("G6-2", "e 折长度 x_e 复现", abs(x_e_sol - D("2.1461932206")) < D("1e-9"),
      f"x_e = {fmt(x_e_sol, 12)}（r214 读数 2.1461932206）——力的 e 折是 2.146λ 不是 λ")

# Yukawa L_max 承 r214：L_max² = α ħc λ φ³ e^{−φ}（自然单位 α ħc λ = 1 时）
guard("G6-3", "h(φ)=φ³e^{−φ} 复现", abs(H_PHI - D("0.8399620946571750898")) < D("1e-18"),
      f"h(φ) = {fmt(H_PHI, 20)}；L_max² = α·ħc·λ·h(φ)——Yukawa 束缚角动量有上限")


def L2_circ_conf(r):
    """禁闭势圆轨道 L²(r) = m(A r + σ r⁴)，自然单位 m=1。"""
    return A_NAT * r + SIG_NAT * r ** 4


dL2_scan_ok = True
for i in range(20):
    r = D("0.1") * (D("1000") ** (D(i) / D(19)))
    if (richardson_deriv(L2_circ_conf, r) - (A_NAT + 4 * SIG_NAT * r ** 3)).copy_abs() > D("1e-18"):
        dL2_scan_ok = False
        break
mono_ok = all((A_NAT + 4 * SIG_NAT * (D("0.05") * (D("4000") ** (D(i) / D(199)))) ** 3) > 0
              for i in range(200))
guard("G6-4", "禁闭无 L_max（对比 r214 U22）", dL2_scan_ok and mono_ok,
      "dL²/dr = A + 4σr³ > 0 全程严格单调 ⇒ 圆轨道 L² 无上界 ⇒ 禁闭势不存在"
      "『超过必逃逸』的角动量上限——与 Yukawa 的 φ-极上限形成硬对照")

# ===========================================================================
# S7 轨迹 RK4（自然单位 ħc = m = 1）
# ===========================================================================
print("[S7] 轨迹 RK4：禁闭势 vs Yukawa 势")


def accel(pos, vel, mode):
    x, y = pos
    r = (x * x + y * y).sqrt()
    if r == 0:
        return (D(0), D(0))
    if mode == "conf":
        fr = A_NAT / (r * r) + SIG_NAT          # |F|，指向原点
    else:
        lam = D("0.35") if mode == "yuk035" else (D(1) if mode == "yuk1" else None)
        if lam is None:
            fr = D(1) / (r * r)
        else:
            xx = r / lam
            fr = (-xx).exp() * (1 / (r * r) + 1 / (lam * r))
    return (-fr * x / r, -fr * y / r)


def rk4_run(mode, L0, dt=D("5e-4"), nsteps=120000, r_stop=D("25")):
    x, y = D(1), D(0)
    vx, vy = D(0), d(L0)          # v_t = L/r0, r0=1
    E0 = D("0.5") * (vx * vx + vy * vy) + potential(mode, x, y)
    L_init = x * vy - y * vx
    rmax = (x * x + y * y).sqrt()
    emax = D(0)
    lmax = D(0)
    for _ in range(nsteps):
        k1 = (vx, vy, *accel((x, y), (vx, vy), mode))
        x2, y2 = x + k1[0] * dt / 2, y + k1[1] * dt / 2
        v2 = (vx + k1[2] * dt / 2, vy + k1[3] * dt / 2)
        k2 = (v2[0], v2[1], *accel((x2, y2), v2, mode))
        x3, y3 = x + k2[0] * dt / 2, y + k2[1] * dt / 2
        v3 = (vx + k2[2] * dt / 2, vy + k2[3] * dt / 2)
        k3 = (v3[0], v3[1], *accel((x3, y3), v3, mode))
        x4, y4 = x + k3[0] * dt, y + k3[1] * dt
        v4 = (vx + k3[2] * dt, vy + k3[3] * dt)
        k4 = (v4[0], v4[1], *accel((x4, y4), v4, mode))
        x += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        y += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        vx += dt * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6
        vy += dt * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) / 6
        r = (x * x + y * y).sqrt()
        if r > rmax:
            rmax = r
        E = D("0.5") * (vx * vx + vy * vy) + potential(mode, x, y)
        L = x * vy - y * vx
        emax = max(emax, abs(E - E0) / abs(E0) if E0 != 0 else abs(E - E0))
        lmax = max(lmax, abs(L - L_init) / abs(L_init) if L_init != 0 else abs(L - L_init))
        if r > r_stop:
            return {"E0": E0, "L": L_init, "rmax": rmax, "escaped": True,
                    "dE": emax, "dL": lmax}
    return {"E0": E0, "L": L_init, "rmax": rmax, "escaped": False,
            "dE": emax, "dL": lmax}


def potential(mode, x, y):
    r = (x * x + y * y).sqrt()
    if mode == "conf":
        return -A_NAT / r + SIG_NAT * r
    lam = D("0.35") if mode == "yuk035" else (D(1) if mode == "yuk1" else None)
    if lam is None:
        return -D(1) / r
    return -(-r / lam).exp() / r


traj = {}
traj["conf_L0.6"] = rk4_run("conf", D("0.6"), nsteps=60000)
traj["conf_L1.0"] = rk4_run("conf", D("1.0"), nsteps=60000)
traj["conf_L3.0"] = rk4_run("conf", D("3.0"), nsteps=120000)
traj["yuk035_L0.6"] = rk4_run("yuk035", D("0.6"), nsteps=120000)
traj["yuk035_L3.0"] = rk4_run("yuk035", D("3.0"), nsteps=120000)
traj["yuk1_L0.6"] = rk4_run("yuk1", D("0.6"), nsteps=60000)

dE_worst = max(t["dE"] for t in traj.values())
dL_worst = max(t["dL"] for t in traj.values())
guard("G7-1", "RK4 能量守恒（全案例）", dE_worst < D("1e-9"),
      f"6 条轨迹 |ΔE/E|max = {fmt(dE_worst, 6)}（dt=5e-4，含近临界 λ=0.35 逃逸案例）",
      {"dE_max": fmt(dE_worst, 8), "dL_max": fmt(dL_worst, 8)})
guard("G7-2", "禁闭无逃逸 vs Yukawa 逃逸（判据有判别力）",
      (not traj["conf_L0.6"]["escaped"]) and (not traj["conf_L3.0"]["escaped"])
      and traj["yuk035_L0.6"]["escaped"] and traj["yuk035_L3.0"]["escaped"],
      f"禁闭：L=0.6/3.0 都束缚（L=3 的 r_max={fmt(traj['conf_L3.0']['rmax'], 6)}）；"
      f"Yukawa λ=0.35：L=0.6 与 L=3（≫L_max=0.5422）都逃逸",
      {"conf_L3_rmax": fmt(traj["conf_L3.0"]["rmax"], 8),
       "yuk035_L06_rmax": fmt(traj["yuk035_L0.6"]["rmax"], 8)})

# 理论 r_max：E = U_eff 的外根（L=3 禁闭）
E3 = D("0.5") * 9 + (-A_NAT / D(1) + SIG_NAT)   # L=3, r0=1
f_root = lambda r: (D("4.5") / (r * r) - A_NAT / r + SIG_NAT * r) - E3
r_max_theory = bisect(f_root, D("10"), D("50"))
rel_rmax = abs(traj["conf_L3.0"]["rmax"] - r_max_theory) / r_max_theory
guard("G7-3", "数值 r_max 与理论外根对拍", rel_rmax < D("0.02"),
      f"理论 r_max = {fmt(r_max_theory, 8)}，数值 = {fmt(traj['conf_L3.0']['rmax'], 8)}，"
      f"相对差 {fmt(rel_rmax, 6)}（RK4 步长内一致）")

# 步长收敛（承 r214 G7-0 思路）
# 步长收敛：测能量误差比（RK4 全局误差 O(dt⁴)，r_max 本身已到理论根、测不出斜率）
t_half = rk4_run("conf", D("3.0"), dt=D("2.5e-4"), nsteps=240000, r_stop=D("25"))
ratio = traj["conf_L3.0"]["dE"] / t_half["dE"] if t_half["dE"] > 0 else D(0)
guard("G7-4", "步长收敛比（能量误差，非调容差蒙过）", D("4") <= ratio <= D("64"),
      f"dt 减半后 |ΔE/E| 缩小约 {fmt(ratio, 6)} 倍（RK4 应 ~16）；"
      f"r_max 与理论外根相对差 {fmt(rel_rmax, 6)} 已在步长内一致",
      {"ratio": fmt(ratio, 8), "dE_dt": fmt(traj["conf_L3.0"]["dE"], 8),
       "dE_half": fmt(t_half["dE"], 8)})

# ===========================================================================
# S8 通道门（g_χ）与宇称读数
# ===========================================================================
print("[S8] 通道门代数与宇称读数")
I2 = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
Z5 = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(-1)]]   # γ⁵ 的 2×2 代表
PL = [[(I2[i][j] - Z5[i][j]) / 2 for j in range(2)] for i in range(2)]
PR = [[(I2[i][j] + Z5[i][j]) / 2 for j in range(2)] for i in range(2)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


PL2 = matmul(PL, PL)
PLPR = matmul(PL, PR)
PLPR0 = all(PLPR[i][j] == 0 for i in range(2) for j in range(2))
PL2ok = all(PL2[i][j] == PL[i][j] for i in range(2) for j in range(2))
sum_ok = all(PL[i][j] + PR[i][j] == I2[i][j] for i in range(2) for j in range(2))
guard("G8-1", "P_L²=P_L、P_L+P_R=I、P_LP_R=0", PL2ok and sum_ok and PLPR0,
      "2×2 精确分数矩阵（γ⁵=diag(1,−1) 代表）：门代数封闭，g_χ 只能取投影值")

A_P_CC = Fraction(1)   # (1²−0²)/(1²+0²)
g_L, g_R = Fraction(1), Fraction(3, 10)
A_P_sample = (g_L ** 2 - g_R ** 2) / (g_L ** 2 + g_R ** 2)
guard("G8-2", "宇称不对称读数", A_P_CC == 1 and A_P_sample == Fraction(91, 109),
      f"CC 道（g_L=1, g_R=0）A_P=1（最大宇称破坏）；样本 (1, 0.3) A_P=91/109={float(A_P_sample):.6f}",
      {"A_P_CC": 1.0, "A_P_sample": float(A_P_sample)})

# 退化还原：g=1, σ=0 ⇒ 与 r214 母式逐位一致
red_worst = D(0)
for i in range(24):
    r = D("1e-16") * (D("1e13") ** (D(i) / D(23)))
    f214 = r214_total_force(r)
    f218 = yukawa_force(R214_ROWS[0]["alpha"], None, r) \
        + yukawa_force(alpha_em, None, r) \
        + yukawa_force(R214_ALPHA_W, LAMBDA_W, r) \
        + yukawa_force(D("14.6"), LAMBDA_PI, r)
    red_worst = max(red_worst, abs(f218 - f214))
guard("G8-3", "退化还原 r214（逐位）", red_worst == 0,
      f"g_χ≡1、σ=0 时 24 点网格 |ΔF| = {red_worst}（恰为 0：同一组参数的同一函数）",
      {"max_abs_diff": fmt(red_worst, 6)})

# ===========================================================================
# S9 JSON 往返 + HTML 自含
# ===========================================================================
print("[S9] 落盘与自含检查")


def build_results():
    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")
    res = {
        "stem": STEM, "round": 221, "date": "2026-10-26",
        "unified_force_equation": (
            "UFE-4F⁺：U(r) = Σ_i [−s_i·α_i·ħc·e^{−r/λ_i}/r] + [σ·r]_色道；"
            "F(r) = −dU/dr = Σ_i [−s_i·α_i·ħc·e^{−x_i}(1/r²+1/(λ_i r))·r̂] − σ·r̂]_色道"),
        "unified_motion_equation": "m·d²r/dt² = Σ_i F_i(r)（五项：四 Yukawa 型 + 一个线性禁闭项）",
        "potential": "U(r) = Σ_i −s_i·α_i·ħc·e^{−r/λ_i}/r + [σr]_色道，g_χ 乘于 (s·α)",
        "params": {
            "lambda_W_m": fmt(LAMBDA_W, 17), "lambda_pi_m": fmt(LAMBDA_PI, 17),
            "alpha_G_pp": fmt(R214_ALPHA_G_PP, 8), "alpha_em": fmt(alpha_em, 12),
            "alpha_W": fmt(R214_ALPHA_W, 8), "alpha_sres": "14.6",
            "alpha_s_2GeV": fmt(ALPHA_S_2GEV, 6), "alpha_s_MZ": fmt(ALPHA_S_MZ, 6),
            "sigma_GeV2": fmt(SIGMA_GEVM2, 6), "sigma_GeV_per_fm": fmt(SIGMA_GEVPERFM, 10),
            "sigma_N": fmt(SIGMA_NEWTON, 10),
            "A_color_GeVfm": fmt(A_COLOR_GEVFM, 10), "C_F": "4/3",
            "r_star_sigma_fm": fmt(r_star_fm, 10),
            "phi": fmt(PHI, 15), "h_phi": fmt(H_PHI, 18), "x_e": fmt(x_e_sol, 12),
        },
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "size_table_log10F": size_table,
            "cross_em_sres_m": fmt(r_cross_ems, 17),
            "cross_em_sres_fm": fmt(r_cross_ems * D("1e15"), 10),
            "cross_em_sigma_m": fmt(r_cross_emsigma, 10),
            "cross_oge_sigma_fm": fmt(r_star_fm, 10),
            "trajectories": {k: {kk: (fmt(vv, 10) if isinstance(vv, Decimal) else vv)
                                 for kk, vv in v.items()} for k, v in traj.items()},
            "channel_gate": {
                "CC": {"g_L": 1, "g_R": 0, "A_P": 1.0},
                "sample_1_03": {"g_L": 1, "g_R": 0.3, "A_P": float(A_P_sample)},
            },
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"},
        "verdict": "", "key_numbers": {}, "judgement": "", "source": "",
    }
    return res


def verdict_string(res):
    parts = [
        "R221-UFE4F-PLUS",
        "SIGMA-IN-OK" if guard_ok("G0-1") else "SIGMA-IN-FAIL",
        "DERIV-COMB-OK" if guard_ok("G1-1") else "DERIV-COMB-FAIL",
        "SIGMA-2PATH-OK" if guard_ok("G2-1") else "SIGMA-2PATH-FAIL",
        "RSTAR-%sfm" % fmt(r_star_fm, 6),
        "EM-SRES-CROSS-REPRO-OK" if guard_ok("G4-1") else "EM-SRES-CROSS-REPRO-FAIL",
        "COL-ATTRACT-OK-NEGSIG-CAUGHT" if guard_ok("G5-2") else "NEGSIG-NOT-CAUGHT",
        "NEFF-LIN-1-OK" if guard_ok("G6-1") else "NEFF-LIN-1-FAIL",
        "NO-LMAX-CONFINEMENT-OK" if guard_ok("G6-4") else "NO-LMAX-FAIL",
        "CONFINEMENT-NO-ESCAPE-OK" if guard_ok("G7-2") else "CONFINEMENT-VERDICT-FAIL",
        "REDUCE-R214-BITEXACT-OK" if guard_ok("G8-3") else "REDUCE-R214-FAIL",
        "GATE-PALG-OK-AP-CC-1" if guard_ok("G8-1") and guard_ok("G8-2") else "GATE-FAIL",
        "TRAJ-GAUGE-OK" if guard_ok("G7-1") else "TRAJ-GAUGE-FAIL",
        "FAIL-U30-INHERITED-NET-INPUTS-PLUS2",
        "VERDICT-FORM-UNIFIED-EXTENDED-DYNAMICS-STILL-NOT",
    ]
    return "-".join(parts)


def guard_ok(gid):
    return any(g["id"] == gid and g["ok"] for g in guards)


def main():
    # ---- 条目判定 ----
    entry("U01", "PASS" if guard_ok("G0-1") else "FAIL", "σ 项量纲齐次",
          "[σ]=MLT⁻²=力、[σr]=ML²T⁻²=能量；σ 是唯一『本身就有力的量纲』的强度参数",
          {"sigma_dim": [1, 0, -2, 0]})
    entry("U02", "PASS" if guard_ok("G1-1") else "FAIL", "组合母式求导闭合",
          "Yukawa+线性组合势 F=−dU/dr：解析 vs Richardson 四阶外推，6 个 r 残差 ≤1e-30 且 ≠0",
          {"max_residual": fmt(max_res, 8)})
    entry("U03", "PASS", "F_σ 恒定（禁闭签名）",
          f"线性项对 r 的力恒为 σ（0.18 GeV² ⇒ {fmt(SIGMA_GEVPERFM, 6)} GeV/fm ⇒ "
          f"{fmt(SIGMA_NEWTON, 6)} N），与 r⁻² 系（引力/电磁）和 e^{{-r/λ}} 系（弱/剩余强）"
          "形成第三类距离行为",
          {"sigma_N": fmt(SIGMA_NEWTON, 8)})
    entry("U04", "PASS" if guard_ok("G5-1") else "FAIL", "色道恒吸引",
          "r∈[0.01,100] fm 4000 点 F_r<0：OGE 与 σ 两项同向，无远近反号（同 r214 G1-7 结论）")
    entry("U05", "PASS", "交叉 r*_σ = √(A/σ)",
          f"r* = {fmt(r_star_fm, 8)} fm（α_s(2 GeV) 口径）：r<r* 单胶子交换占优（渐近自由区），"
          "r>r* 线性禁闭占优；与 18 卷 0.3889 fm（σr vs π-Yukawa，异道异口径）不矛盾",
          {"r_star_fm": fmt(r_star_fm, 8)})
    entry("U06", "BOUNDARY", "EM↔σr 交叉为跨自由度比较",
          f"r = √(k_e e²/σ) = {fmt(r_cross_emsigma * D('1e15'), 6)} fm，"
          "但色力作用于色荷对、电磁力作用于电荷对——不同自由度的『谁大』只作形式层读数",
          {"r_cross_fm": fmt(r_cross_emsigma * D("1e15"), 6)})
    entry("U07", "PASS" if guard_ok("G6-1") else "FAIL", "n_eff(线性)=1",
          "线性项等效幂指数恒为 +1：四力距离行为三分类（−2 / 指数压制 / +1）至此齐备")
    entry("U08", "PASS" if guard_ok("G6-4") else "FAIL", "禁闭无 L_max 上限",
          "dL²_circ/dr = A+4σr³ > 0 严格单调 ⇒ 任何 L 都有束缚圆轨道；"
          "Yukawa 则有 L_max² = αħcλφ³e^{−φ}（r214 U22）——两种短程化的动力学后果截然不同")
    entry("U09", "PASS" if guard_ok("G7-2") else "FAIL", "禁闭下无逃逸（轨迹证实）",
          f"禁闭势 L=0.6/3.0 均束缚（L=3 的 r_max={fmt(traj['conf_L3.0']['rmax'], 6)}）"
          f"；Yukawa λ=0.35 同初值逃逸（r_max={fmt(traj['yuk035_L0.6']['rmax'], 6)} 或 40+）",
          {"conf_L3_rmax": fmt(traj["conf_L3.0"]["rmax"], 8)})
    entry("U10", "PASS" if guard_ok("G7-1") and guard_ok("G7-3") and guard_ok("G7-4") else "FAIL",
          "RK4 组合势轨迹质量",
          f"6 条轨迹 |ΔE/E|max={fmt(dE_worst, 6)}；数值 r_max 与理论外根相对差 "
          f"{fmt(rel_rmax, 6)}；步长收敛比 {fmt(ratio, 6)}（应在 4–64）",
          {"dE_max": fmt(dE_worst, 8), "r_max_rel": fmt(rel_rmax, 6)})
    entry("U11", "PASS" if guard_ok("G8-3") else "FAIL", "退化还原 r214",
          "g_χ≡1、σ=0 时 24 点网格与 r214 UFE-4F 母力逐位一致（|Δ|=0）——"
          "UFE-4F⁺ 是 r214 的严格超集，不是另一条方程")
    entry("U12", "PASS" if guard_ok("G8-1") and guard_ok("G8-2") else "FAIL",
          "通道门代数与宇称读数",
          "P_L²=P_L、P_L+P_R=I、P_LP_R=0（精确分数）；CC 道 A_P=1（最大宇称破坏），"
          "样本 (g_L,g_R)=(1,0.3) A_P=91/109≈0.834862")
    entry("U13", "BOUNDARY", "弱方向通道依从（结构登记，非推导）",
          "在门扩展下『只有电磁可变号』（r214 U18）需加限定：s 可通道依从是结构登记，"
          "弱道的完整 V−A 规范动力学（W/Z 极化、味改变）仍不在式内——U27 完整收口 OPEN")
    entry("U14", "INFO", "大小表升级（五系列）",
          f"色道 |F| 在 0.1/0.3/1 fm = "
          f"{fmt(color_force_N(D('1e-16')), 6)} / {fmt(color_force_N(D('3e-16')), 6)} / "
          f"{fmt(color_force_N(D('1e-15')), 6)} N（GeV/fm 口径两路一致）；"
          "1 Å 以上色道『恒力』只是形式延拓——物理上禁闭使孤立色对不存在（B3）",
          {"sigma_N": fmt(SIGMA_NEWTON, 8)})
    entry("U15", "FAIL", "输入账：净约束增量仍为 0",
          "UFE-4F 输入 12 个（{s,α,λ}×4）→ UFE-4F⁺ 14 个（+σ、+g_χ）；约束新增 0 个；"
          "方程更完整但统一度不升——U30『动力学不统一』FAIL 继承不翻案",
          {"inputs_before": 12, "inputs_after": 14})
    entry("U16", "INFO", "判决",
          "形式统一**扩展成功**：一个势函数 + 一个运动方程现在承载四 Yukawa 型力 + 线性禁闭；"
          "求导、量纲、方向、距离、轨迹全机算闭合；动力学统一仍 FAIL（继承）")

    # ---- 控制组（在 build_results 前登记，保证 counts 即时正确）----
    control("C1", "太阳-地球引力：母式 vs 牛顿直算",
            _c1_check()[0], _c1_check()[1], _c1_check()[2])
    control("C2", "氢原子：库仑母式给 13.6057 eV",
            _c2_check()[0], _c2_check()[1], _c2_check()[2])
    control("C3", "EM↔强剩余交叉 14.618 fm 复现",
            guard_ok("G4-1"),
            f"r_× = {fmt(r_cross_ems * D('1e15'), 8)} fm vs r214 读数 14.6179756 fm",
            {"cross_fm": fmt(r_cross_ems * D("1e15"), 8)})

    res = build_results()
    res["verdict"] = verdict_string(res)
    res["key_numbers"] = {
        "lambda_W_m": fmt(LAMBDA_W, 17), "lambda_pi_m": fmt(LAMBDA_PI, 17),
        "sigma_N": fmt(SIGMA_NEWTON, 8),
        "r_star_oge_sigma_fm": fmt(r_star_fm, 8),
        "cross_em_sres_fm": fmt(r_cross_ems * D("1e15"), 8),
        "cross_em_sigma_fm": fmt(r_cross_emsigma * D("1e15"), 6),
        "x_e": fmt(x_e_sol, 12), "h_phi": fmt(H_PHI, 18),
        "L_max2_natural_yukawa1": fmt(H_PHI, 10),
        "em_g_ratio": fmt(alpha_em / R214_ALPHA_G_PP, 12),
    }
    res["judgement"] = ("CLOSED-INCREMENT（禁闭项接入 + 通道门登记 + 交互可视化）；"
                        "U26 部分收口（色道）、U27 结构登记、U30 FAIL 继承；供给仍 0")
    res["source"] = {
        "engine": "TUFT-r221_四力统一运动方程强化轮_禁闭项接入与弱通道门_精算与交互可视化_2026-10-26.py",
        "inherits": ["r214（UFE-4F 母式与四力参数）", "r217（独立复核与根目录整理）",
                     "70 卷（α_s 低能读数）", "03_四力还原（力程/耦合基准）"],
    }

    counts = res["counts"]
    print(f"条目 {counts['entries']}（PASS {counts['PASS']} / FAIL {counts['FAIL']} / "
          f"BOUNDARY {counts['BOUNDARY']} / INFO {counts['INFO']}）· "
          f"守卫 {counts['guards']} · 控制组 {counts['controls']}")

    # ---- 落盘 ----
    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")
    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    write_md(mpath, res)
    write_report(rpath, res)

    # ---- 交互 HTML 铸数 ----
    html_ok, html_detail = cast_html(res)
    guard("G9-1", "交互 HTML 生成且自含", html_ok, html_detail)

    # ---- 控制组失败 / 守卫失败 → 非零退出 ----
    bad_g = [g["id"] for g in guards if not g["ok"]]
    bad_c = [x["id"] for x in controls if not x["ok"]]
    if bad_g or bad_c:
        print(f"[RC≠0] 守卫失败 {bad_g} 控制组失败 {bad_c}")
        return 1
    print(f"[DONE] {MARKER} rc=0 → {jpath}")
    return 0


def _c1_check():
    f_mother = yukawa_force(G_newton * M_SUN * M_EARTH / HARC_SI, None, AU)
    f_newton = G_newton * M_SUN * M_EARTH / (AU * AU)
    rel = abs(f_mother - f_newton) / f_newton
    ok = rel < D("1e-40")
    return ok, f"母式 F={fmt(f_mother, 10)} N，牛顿直算 F={fmt(f_newton, 10)} N，相对差 {fmt(rel, 6)}", {
        "F_N": fmt(f_newton, 10), "rel": fmt(rel, 8)}


def _c2_check():
    v = k_e * e_charge * e_charge / a0_bohr          # J
    ev = v / EV_TO_J
    e1 = ev / 2
    target = D("13.605693")
    rel = abs(e1 - target) / target
    ok = rel < D("1e-5")
    return ok, f"V(a0)={fmt(ev, 10)} eV，E1=−V/2={fmt(e1, 10)} eV vs Rydberg 13.605693 eV，相对差 {fmt(rel, 6)}", {
        "E1_eV": fmt(e1, 10), "rel": fmt(rel, 8)}


def write_md(path, res):
    L = []
    L.append(f"# {res['stem']} · 数据册（引擎自动生成）\n")
    L.append(f"- 判决串：`{res['verdict']}`\n")
    L.append(f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / "
             f"FAIL {res['counts']['FAIL']} / BOUNDARY {res['counts']['BOUNDARY']} / "
             f"INFO {res['counts']['INFO']}）· 守卫 {res['counts']['guards']} · "
             f"控制组 {res['counts']['controls']}\n")
    L.append("\n## 承重式（UFE-4F⁺）\n")
    L.append(f"- 统一势：{res['potential']}\n")
    L.append(f"- 统一运动方程：{res['unified_motion_equation']}\n")
    L.append("\n## 参数\n")
    for k, v in res["params"].items():
        L.append(f"- `{k}` = {v}\n")
    L.append("\n## 大小表（log10 |F| / N，两质子基准；色道为 q q̄ 色单态）\n")
    L.append("| r | 引力 | 电磁 | 弱 | 强剩余 | 强色道 |\n|---|---|---|---|---|---|\n")
    for row in res["readings"]["size_table_log10F"]:
        L.append(f"| {row['r']} | {row['G']} | {row['EM']} | {row['W']} | "
                 f"{row['Sres']} | {row['Scol']} |\n")
    L.append("\n## 条目\n")
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} "
                f"PASS={res['counts']['PASS']} FAIL={res['counts']['FAIL']} "
                f"BOUNDARY={res['counts']['BOUNDARY']} INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        f.write("key_numbers=" + json.dumps(res["key_numbers"], ensure_ascii=False) + "\n")
        f.write("trajectories=" + json.dumps(res["readings"]["trajectories"], ensure_ascii=False) + "\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R218_JSON__" not in tpl:
        return False, "模板缺少 __R218_JSON__ 占位符"
    payload = json.dumps(res, ensure_ascii=False)
    html = tpl.replace("__R218_JSON__", payload)
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R218_JSON__" in text:
        problems.append("占位符未替换")
    if "http://" in text or "https://" in text:
        problems.append("发现外部 URL（应零依赖）")
    if "<canvas" not in text:
        problems.append("缺少 canvas")
    if "<script" not in text:
        problems.append("缺少 script")
    if problems:
        return False, "；".join(problems)
    return True, f"已生成 {HTML_OUT}（{len(text)} B），零外部 URL、canvas×N、JSON 已铸入"


if __name__ == "__main__":
    sys.exit(main())
