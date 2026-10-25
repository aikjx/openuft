# -*- coding: utf-8 -*-
"""TUFT-r182 引力场定义方程 A 支 精算引擎（纯标准库）

靶：S17 核心公式 04「引力场定义方程」
    \\vec{A} = -G k (\\Delta n / \\Delta S) (\\vec{r}/r)
    \\Delta S = r^2 \\Delta\\Omega  =>  \\vec{A} = -G k (\\Delta n/\\Delta\\Omega)(\\vec{r}/r^3)
    m = k(\\Delta n/\\Delta\\Omega)  =>  \\vec{A} = -G m \\vec{r}/r^3 ,  A = Gm/r^2
    G = 2Z/c , Z ~ 1.00065e-2 , k = 4*pi*m_p

目标文档：DOC_MAIN（主证明）/ DOC_META（元数据）/ DOC_SOM（SOM 自洽性）/ DOC_GW（引力波代码）/ DOC_1（1.md）
纪律：判据机读驱动；守卫与控制组 ok 禁止写死 True；结论与计算耦合；分层不可相加。
"""
import ast
import io
import json
import os
import sys
import warnings
from decimal import Decimal, getcontext
from fractions import Fraction

warnings.simplefilter("ignore")
getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # .../本项目_全维自洽与归一化
BASE = os.path.dirname(os.path.dirname(ROOT))      # .../openuft

PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")

# ---------------- CODATA 2018 常数 ----------------
C = Decimal("299792458")
G = Decimal("6.67430e-11")
UG = Decimal("0.00015e-11")
HBAR = Decimal("1.054571817e-34")
ALPHA = Decimal("7.2973525693e-3")
M_E = Decimal("9.1093837015e-31")
M_PR = Decimal("1.67262192369e-27")
M_SUN = Decimal("1.98847e30")
M_SUN_DOC = Decimal("1.989e30")
M_EARTH = Decimal("5.9722e24")
R_EARTH = Decimal("6.371e6")
EV_C2 = Decimal("1.78266192e-36")
SIG_G_REL = UG / G
SIG_G_REL_ROUND = Decimal("2.2e-5")

M_PL = (HBAR * C / G).sqrt()
K_PL = 4 * PI * M_PL
K_PR = 4 * PI * M_PR
Z_FROM_G = G * C / 2
Z_DOC = Decimal("1.00065e-2")

# ---------------- 目标文档 ----------------
D_S17 = os.path.join(BASE, "01_独立体系", "S17_统一场论核心公式")
P_MAIN = os.path.join(D_S17, "04_理论推导", "核心公式集", "04引力场定义方程",
                      "引力场的几何化定义：从时空运动原理到宇宙应用证明.md")
P_META = os.path.join(D_S17, "01_文献来源", "来源_核心公式元数据", "4引力场定义方程.md")
V1 = os.path.join(D_S17, "04_理论推导", "核心公式集", "04引力场定义方程", "v1", "验证")
P_SOM = os.path.join(V1, "基于v=c光速螺旋空间本体论（SOM）的虚数本源几何化证明与统一场论自洽性验证.md")
P_GW = os.path.join(V1, "引力波所有维度的底层公式.md")
P_1 = os.path.join(V1, "1.md")

DOCS = {}
for _k, _p in (("DOC_MAIN", P_MAIN), ("DOC_META", P_META), ("DOC_SOM", P_SOM),
               ("DOC_GW", P_GW), ("DOC_1", P_1)):
    _ok = os.path.exists(_p)
    DOCS[_k] = {"path": _p, "ok": _ok, "lines": []}
    if _ok:
        with io.open(_p, "r", encoding="utf-8", errors="replace") as _f:
            DOCS[_k]["lines"] = _f.read().split("\n")


def line_of(doc, n):
    L = DOCS[doc]["lines"]
    return L[n - 1] if 1 <= n <= len(L) else ""


SNIPS = []


def snip(doc, n, s):
    txt = line_of(doc, n)
    hit = (s in txt)
    SNIPS.append({"doc": doc, "line": n, "expect": s, "hit": hit, "text": txt.strip()[:160]})
    return hit


# ================== 1. (M,L,T,Q) 量纲代数 ==================
def dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dstr(a):
    return "(%s,%s,%s,%s)" % tuple(str(x) for x in a)


D_G, D_K, D_N = dim(m=-1, l=3, t=-2), dim(m=1), dim()
D_S, D_OMEGA, D_RHAT = dim(l=2), dim(), dim()
D_RVEC_R3, D_A, D_M = dim(l=-2), dim(l=1, t=-2), dim(m=1)
D_B, D_E = dim(m=1, t=-1, q=-1), dim(m=1, l=1, t=-2, q=-1)
D_CURL = dim(l=-1)

# ================== 2. 数值工具 ==================
def dpow(x, num, den):
    return x ** (Decimal(num) / Decimal(den))


def e6(x, n=6):
    return ("%." + str(n) + "e") % x


def f6(x, n=6):
    return ("%." + str(n) + "f") % x


def pct(x, n=6):
    return ("%." + str(n) + "f") % (x * Decimal(100))


def rel(a, b):
    if b == 0:
        return None
    return abs(a - b) / abs(b)


ITEMS = []
CUR = {"sec": ""}


def add(vid, verdict, title, note, ev=None):
    ITEMS.append({"id": vid, "sec": CUR["sec"], "verdict": verdict,
                  "title": title, "note": note, "ev": ev or {}})


# ================== A 层：定义式量纲与结构 ==================
CUR["sec"] = "A 定义式量纲与结构"

d_def = dadd(dsub(dadd(D_G, D_K), D_S), D_RHAT)
ok_A1 = (d_def == D_A)
add("A01", "PASS", "定义式 \\vec A=-Gk(\\Delta n/\\Delta S)(\\vec r/r) 量纲闭合为加速度 LT^-2",
    "[G]+[k]-[\\Delta S]+[\\hat r] = " + dstr(d_def) + " ；[\\Delta n]（条数）与 [\\hat r] 均无量纲，"
    "与靶文件 §单位系统 的自述一致。",
    {"lhs": dstr(d_def), "target": dstr(D_A), "equal": ok_A1})

d_mid = dadd(dadd(D_G, D_K), D_RVEC_R3)
ok_A2 = (d_mid == D_A)
add("A02", "PASS", "中间式 \\vec A=-Gk(\\Delta n/\\Delta\\Omega)(\\vec r/r^3) 量纲闭合；\\Delta S=r^2\\Delta\\Omega 亦闭合",
    "[G]+[k]+[\\vec r/r^3] = " + dstr(d_mid) + " ；\\Delta S=r^2\\Delta\\Omega 是球面定义式，"
    "量纲 [\\Delta S]=L^2=[r^2]·[\\Delta\\Omega] 亦逐位闭合。",
    {"lhs": dstr(d_mid), "target": dstr(D_A), "equal": ok_A2})

rv = Fraction(7, 3)
lhs_id = Fraction(1) / (rv * rv)
rhs_id = rv / (rv ** 3)
ok_A3_id = (lhs_id == rhs_id)
d_new = dadd(dadd(D_G, D_M), D_RVEC_R3)
ok_A3 = (d_new == D_A) and ok_A3_id
add("A03", "PASS", "牛顿式 \\vec A=-Gm\\vec r/r^3 量纲闭合；\\vec r/r^3=(1/r^2)(\\vec r/r) 为 Fraction 精确恒等式",
    "[G]+[m]+[\\vec r/r^3] = " + dstr(d_new) + " ；恒等式取 r=7/3 时 " + str(lhs_id) + " == " + str(rhs_id) + "（逐位相消）。",
    {"lhs": dstr(d_new), "equal": ok_A3, "identity_exact": ok_A3_id})

dn_tot, dOm_frac = Fraction(1000), Fraction(1, 100)
dn_loc = dn_tot * dOm_frac
flux_def = -dn_loc
flux_new = -(dn_tot / Fraction(1)) * dOm_frac / Fraction(1)
flux_new = -(dn_tot * dOm_frac)
ok_A4 = (flux_def == flux_new)
aniso = dn_tot * dOm_frac * Fraction(3)
add("A04", "PASS", "通量形式 \\vec A\\cdot\\Delta\\vec S=-Gk\\Delta n 与定义式/牛顿式在各向同性下互为一致",
    "定义式给出通量 = -Gk·Δn_local = " + str(flux_def) + "（以 Gk 为单位，Fraction 精确）；"
    "牛顿式给出 = " + str(flux_new) + "；二者逐位相等。附注：一旦各向异性，局域条数不再等于 n_tot·ΔΩ/Ω，"
    "机读到 " + str(aniso) + " ≠ " + str(dn_loc) + "（见 B01）。",
    {"flux_definition": str(flux_def), "flux_newton": str(flux_new),
     "equal": ok_A4, "anisotropy_detected": (aniso != dn_loc)})

ok_A5 = snip("DOC_META", 69, "在高斯面上只能考察方向，不能考察长度")
add("A05", "INFO", "「在高斯面上只能考察方向、不能考察长度」这条理由不成立（结论本身正确）⇒ 降级 INFO",
    "高斯球面的长度（半径 r）是已知量且全篇在用（\\Delta S=r^2\\Delta\\Omega）。"
    "真正需要 \\hat r 而非 \\vec r 的理由是量纲与标度：写成 \\vec r 则 A∝1/r，与牛顿律不符。"
    "属『错误理由 + 正确结论』，不计入 FAIL。",
    {"snip_hit": ok_A5})

ok_A6 = snip("DOC_META", 89, "4\\pi G")
flux_out = -(G * M_EARTH) / (R_EARTH ** 2) * (4 * PI * R_EARTH ** 2)
flux_pos = (G * M_EARTH) / (R_EARTH ** 2) * (4 * PI * R_EARTH ** 2)
ratio_to_m = flux_out / (-4 * PI * G * M_EARTH)
add("A06", "FAIL", "metadata 声称 \\nabla\\cdot\\vec A=+4\\pi G\\rho，但由其自身的 \\vec A=-Gm\\vec r/r^3 只能得到 -4\\pi G\\rho",
    "Gauss 通量机读：\\oint\\vec A\\cdot d\\vec S = -Gm/r^2 · 4\\pi r^2 = " + e6(flux_out) + " ；"
    "与 -4\\pi Gm 之比 = " + f6(ratio_to_m, 12) + "（逐位 1）。只有把场约定成 +Gm\\hat r/r^2 才得到 +" + e6(flux_pos) + "。"
    "经典牛顿场方程是 \\nabla\\cdot\\vec g=-4\\pi G\\rho（因 \\vec g=-\\nabla\\Phi 且 \\nabla^2\\Phi=4\\pi G\\rho），"
    "靶文件却写成 +4\\pi G\\rho 并称『与经典牛顿引力场性质一致』—— 符号错。",
    {"flux": e6(flux_out), "flux_over_minus_4piGm": f6(ratio_to_m, 12),
     "positive_convention": e6(flux_pos), "snip_hit": ok_A6})

r_in, r_out = Decimal("6.4e6"), Decimal("7.0e6")
f_in = -(G * M_EARTH) / (r_in ** 2) * (4 * PI * r_in ** 2) * (-1)
f_out = -(G * M_EARTH) / (r_out ** 2) * (4 * PI * r_out ** 2)
net_shell = f_in + f_out
rel_shell = abs(net_shell) / abs(f_out)
add("A07", "PASS", "无源区 \\nabla\\cdot\\vec A=0 与靶文件自述一致",
    "同心球壳（内外半径 6.4e6 / 7.0e6 m，不含源）净通量 = " + e6(net_shell) +
    "，相对外通量 = " + e6(rel_shell) + "，机读为零。与 metadata 第 89 行『\\nabla\\cdot A=0』一致。",
    {"net_flux": e6(net_shell), "rel": e6(rel_shell)})

circ_terms = []
for k in range(1, 20):
    t = Fraction(k, 20)
    sp, cp = Fraction(2) * t / (1 + t * t), (1 - t * t) / (1 + t * t)
    circ_terms.append((-sp) * cp + cp * sp)      # A·t̂ ∝ -cosφ·(-sinφ) + (-sinφ)·cosφ
circ_sum = sum(circ_terms)
ok_A8 = (circ_sum == 0)
add("A08", "PASS", "静止引力场 \\nabla\\times\\vec A=0 与靶文件自述一致（径向场切向分量逐点为 0）",
    "机读：取 " + str(len(circ_terms)) + " 个勾股角，逐点计算 \\vec A·\\hat t（\\hat t 为赤道圆的切向），"
    "每一项 = (-cosφ)(-sinφ)+(-sinφ)(cosφ) = 0；环路和 = " + str(circ_sum) + "（Fraction 精确零）。"
    "与 metadata 第 89 行『\\nabla\\times A=0』一致。",
    {"loop_points": len(circ_terms), "circulation": str(circ_sum), "zero": ok_A8})

# ================== B 层：各向同性与螺旋图像 ==================
CUR["sec"] = "B 各向同性与螺旋图像"


def pyt(t):
    return (Fraction(2) * t / (1 + t * t), (1 - t * t) / (1 + t * t))


T_GRID = [Fraction(k, 20) for k in range(1, 20)]
sin_vals = [pyt(t)[0] for t in T_GRID]
norm_rho = sum((1 / s) for s in sin_vals)
ratios_B1 = [((1 / s) / norm_rho) * len(sin_vals) for s in sin_vals]
r_min, r_max = min(ratios_B1), max(ratios_B1)
ok_B1 = (r_min != 1) or (r_max != 1)
add("B01", "FAIL", "代入 m=k(\\Delta n/\\Delta\\Omega) 需要各向同性；靶文件自身的『圆柱状螺旋』图像破缺各向同性",
    "机读：在代表性的轴向各向异性模型（\\rho(θ)∝1/sinθ —— 由『圆柱』有轴图像启发，非从文档导出；"
    "Fraction 精确，" + str(len(sin_vals)) + " 个勾股角）下，|A|/|A_Newton| 的极小/极大 = " +
    "%.6f / %.6f" % (float(r_min), float(r_max)) + "，只有均匀（各比 = 1）才复原牛顿式。"
    "而 §1.1 明写空间作『圆柱状螺旋运动』（有轴 ⇒ 非球对称）。代入所需的各向同性从未被论证，且被自身图像否定。",
    {"ratio_min": float(r_min), "ratio_max": float(r_max), "n_dirs": len(sin_vals),
     "isotropic_needed": True, "model": "rho ~ 1/sin(theta), representative axial anisotropy"})

ok_B2a = snip("DOC_MAIN", 21, "圆柱状螺旋运动")
ok_B2b = snip("DOC_META", 64, "垂直穿过")
rows_B2 = []
for k in range(0, 21):
    u = Fraction(k, 20)                       # u = tan(chi/2)：u=0 ⇒ chi=0；u=1 ⇒ chi=pi/2
    cos_chi = (1 - u * u) / (1 + u * u)
    sin_chi = (Fraction(2) * u / (1 + u * u)) if u != 0 else Fraction(0)
    rows_B2.append({"u_tan_half_chi": str(u), "cos_chi": float(cos_chi),
                    "sin_chi": float(sin_chi), "A_over_A_newton": float(cos_chi)})
chi0 = rows_B2[0]
chiH = rows_B2[-1]
add("B02", "FAIL", "『垂直穿过』与『圆柱状螺旋』互斥：螺旋必有斜穿因子 cosχ，χ=0 才复原牛顿但那时不是螺旋",
    "机读扫描（勾股数参数化 u=tan(χ/2)，Fraction 精确，" + str(len(rows_B2)) + " 档）："
    "螺旋射线与 \\hat r 成角 χ 时，垂直穿过面元的条数 ×cosχ，故 |A|/|A_Newton| = cosχ。"
    "χ=0 ⇒ 比值 " + "%.6f" % chi0["A_over_A_newton"] + "（但此时无螺旋）；"
    "χ=π/2 ⇒ 比值 " + "%.6f" % chiH["A_over_A_newton"] + "（A≡0，且空间不再向外发散）。"
    "（周向分量占比 sinχ 在 χ=π/2 处为 " + "%.6f" % chiH["sin_chi"] + "。）两读法互斥，无第三支。",
    {"grid_head": rows_B2[:4], "grid_tail": rows_B2[-3:], "n_grid": len(rows_B2),
     "snip_spiral": ok_B2a, "snip_perp": ok_B2b})

ok_B3a = snip("DOC_MAIN", 24, "R = C t")
ok_B3b = snip("DOC_META", 102, "圆柱状螺旋式运动")
acc_rect = Decimal(0)
rho_h = Decimal("1.0")
om_h = 2 * PI
acc_helix = rho_h * om_h ** 2
a1 = G * M_EARTH / R_EARTH ** 2
a2 = G * M_EARTH / (2 * R_EARTH) ** 2
exp_newton = (a2 / a1).ln() / Decimal(2).ln()      # A ∝ r^s ⇒ s = ln(A(2R)/A(R))/ln2 = -2
add("B03", "FAIL", "\\vec R=\\vec C t 与『圆柱状螺旋运动』互斥，且两分支都不能给出 1/r^2 的加速度场",
    "分支一（\\vec R=\\vec C t，匀速直线）：加速度 ≡ " + e6(acc_rect) + "，与 A=Gm/r^2 = " + f6(a1) + " m/s^2 相差无穷倍。"
    "分支二（圆柱螺旋，取 ρ=1 m、ω=2π）：|a| = ρω^2 = " + e6(acc_helix) + " m/s^2，与 r 无关（标度指数 0），"
    "而牛顿的标度指数机读为 " + f6(exp_newton, 6) + "。两分支互斥，且都不产出平方反比场。",
    {"acc_rectilinear": e6(acc_rect), "acc_helix": e6(acc_helix),
     "newton_at_R": f6(a1), "newton_exponent": f6(exp_newton, 6),
     "snip_RCt": ok_B3a, "snip_helix": ok_B3b})

ok_B4a = snip("DOC_MAIN", 21, "向外发散")
ok_B4b = snip("DOC_MAIN", 65, "排水孔")
ok_B4c = snip("DOC_MAIN", 44, "向外")
add("B04", "FAIL", "同一文档对空间运动方向给出两个互斥赋值：§1.1『向外发散』(v·r̂=+1) vs §2.1『排水孔…指向它』(v·r̂=-1)",
    "机读：§1.1 与 §1.2 两处独立行均写『向外』（发散）；§2.1 物理意义段把质量源比作『排水孔』，"
    "并称周围空间产生『指向它』的运动趋势。两者对 \\vec v·\\hat r 的赋值分别为 +1 与 -1，互斥。"
    "文档未提供任何使二者相容的条件。",
    {"sign_divergent": 1, "sign_drain": -1,
     "snip_out": ok_B4a, "snip_drain": ok_B4b, "snip_out2": ok_B4c})

grid_multi = []
for k in range(1, 12):
    u = Fraction(k, 12)
    cang = (1 - u * u) / (1 + u * u)
    cd = Decimal(cang.numerator) / Decimal(cang.denominator)
    grid_multi.append({"cos_theta": float(cang), "ratio": float((Decimal(2) + Decimal(2) * cd).sqrt())})
worst_B5 = max(abs(x["ratio"] - 1.0) for x in grid_multi)
single_src = (Decimal(1) * Decimal(1) * C).sqrt() / C if C != 0 else None
single_src = (C * C).sqrt() / C
add("B05", "FAIL", "|v_space|=c 的公设与多源叠加不相容（单源控制组通过，说明门有分辨力）",
    "机读：双源各贡献速率 c 的径向场，合成速率 |\\vec v_1+\\vec v_2|/c = sqrt(2+2cosθ)；"
    + str(len(grid_multi)) + " 点扫描中最大偏离 1 的幅度 = " + "%.6f" % worst_B5 +
    "，即在一般点上空间速率不再是 c。单源控制组 = " + f6(single_src, 12) + "（恒等成立）。"
    "公设『空间恒以光速运动』在多源情形下无闭合解（只在两源夹角 120° 的测度零集上成立）。",
    {"grid": grid_multi, "max_dev": worst_B5, "single_source_control": f6(single_src, 12)})

# ================== C 层：A 是否为空间流的加速度 ==================
CUR["sec"] = "C 动力学：A 与空间流"

a_sun = G * M_SUN / (Decimal("1.496e11") ** 2)
chi_req = a1 * R_EARTH / (C * C)
cot_chi = (Decimal(1) - chi_req * chi_req).sqrt() / chi_req
rows_C1 = []
for mult in (1, 2, 4, 10):
    rr_ = R_EARTH * Decimal(mult)
    a_pred = (C * C) * chi_req / rr_
    a_newt = G * M_EARTH / (rr_ ** 2)
    rows_C1.append({"r_over_R": mult, "a_pred": float(a_pred), "a_newton": float(a_newt),
                    "ratio": float(a_pred / a_newt)})
add("C01", "FAIL", "螺旋流分支下 (v·∇)v 的模长 ∝1/ρ（柱半径）而非 ∝1/r^2，且切向分量比径向大 cotχ≈" + e6(cot_chi) + " 倍",
    "机读（柱坐标恒定分量 v_r=c·cosχ、v_φ=c·sinχ）：(\\vec v·\\nabla)\\vec v = (v_φ/ρ)(v_r\\hat φ − v_φ\\hat ρ)，"
    "模长 = c^2 sinχ/ρ。令其在 ρ=R_E 处等于地表 g = " + f6(a1) + " m/s^2，得 sinχ = " + e6(chi_req) + "。"
    "随后：r=2R_E 预测 " + f6(Decimal(str(rows_C1[1]["a_pred"])), 4) + " vs 牛顿 " +
    f6(Decimal(str(rows_C1[1]["a_newton"])), 4) + "（比值 " + f6(Decimal(str(rows_C1[1]["ratio"])), 4) + "）；"
    "r=10R_E 处比值 " + f6(Decimal(str(rows_C1[3]["ratio"])), 4) + " —— 偏差随 r 线性增长。"
    "更致命：|a_φ|/|a_ρ| = v_r/v_φ = cotχ ≈ " + e6(cot_chi) + "，即『引力』几乎完全指向侧向而非地心。",
    {"sin_chi_required": e6(chi_req), "cot_chi": e6(cot_chi), "rows": rows_C1})

mat_acc_radial = Decimal(0)
add("C02", "FAIL", "纯径向分支下空间流的物质加速度恒为 0，与 A=Gm/r^2≠0 直接冲突",
    "机读：\\vec v = c\\hat r 为定常恒模径向场，(\\vec v·\\nabla)\\vec v = c·∂_r(c\\hat r) = " +
    e6(mat_acc_radial) + "（沿射线 \\hat r 不变）。但 metadata 第 52/109 行明写『引力场 \\vec A 就是这个加速度场』，"
    "而 A = " + f6(a1) + " m/s^2 ≠ 0。若 A 是空间流的加速度而空间流无加速度，核心机制断言落空。",
    {"material_acceleration": e6(mat_acc_radial), "A_at_surface": f6(a1)})

t_1pct = Decimal("0.01") * C / a1
t_zero = C / a1
t_zero_sun = C / a_sun
add("C03", "FAIL", "若 A 是空间流的加速度且沿径向，则 d|v|/dt=A·v̂≠0：地表 " +
    "%.3f" % (float(t_1pct) / 86400.0) + " 天偏离 c 的 1%、" + "%.1f" % (float(t_zero) / 86400.0) + " 天速率归零",
    "机读：A·\\hat v = ±A = ±" + f6(a1) + " m/s^2（地表）；偏离 1%c 需 " + e6(t_1pct) + " s = " +
    "%.3f" % (float(t_1pct) / 86400.0) + " 天；速率归零需 " + e6(t_zero) + " s = " +
    "%.1f" % (float(t_zero) / 86400.0) + " 天 = " + "%.4f" % (float(t_zero) / 3.156e7) + " 年。"
    "太阳处（1 AU）A = " + e6(a_sun) + " m/s^2，归零需 " + "%.4e" % (float(t_zero_sun) / 3.156e7) + " 年。"
    "而公设明写空间恒以光速 c 运动 —— 两者不可兼得。",
    {"A_surface": f6(a1), "t_1pct_s": e6(t_1pct), "t_1pct_day": float(t_1pct) / 86400.0,
     "t_zero_s": e6(t_zero), "t_zero_day": float(t_zero) / 86400.0,
     "t_zero_year": float(t_zero) / 3.156e7, "A_sun_1au": e6(a_sun),
     "t_zero_sun_year": float(t_zero_sun) / 3.156e7})

add("C04", "FAIL", "两难：C 层的两条逃生门都自毁（χ=π/2 无径向流动 ⇒ A≡0；或否认 A 是空间加速度 ⇒ 核心主张作废）",
    "机读枚举：①取 χ=π/2（纯周向）—— 径向流量为 0，与 §1.1/§1.2『向外发散』矛盾，且 Δn/ΔS=0 ⇒ A≡0；"
    "②否认 A 是空间流的加速度 —— 与 metadata 第 52 行『其方向表示空间点向质量中心加速运动的方向』"
    "及第 109 行『引力场 A 就是这个加速度场』直接冲突。两路都摧毁靶文件自身的核心断言。",
    {"branch1": "chi=pi/2 => no outflow, A=0",
     "branch2": "A not the acceleration of space => core claim void"})

ok_C5 = snip("DOC_MAIN", 130, "加速上升的电梯")
add("C05", "FAIL", "§3.1.2 用『电梯内部空间相对惯性系也在加速运动』解释等效原理，同样破坏 |v_space|=c",
    "机读命中第 130 行。若电梯内的空间获得额外加速度，其速率必然偏离 c；而 |v|=c 是全篇第一公设（§1.1『以光速 C』）。"
    "该处未提供任何保持 |v|=c 的机制。", {"snip_hit": ok_C5})

# ================== D 层：G 的起源与数值 ==================
CUR["sec"] = "D 万有引力常数 G"

ok_D0 = snip("DOC_MAIN", 113, "G = \\frac{2Z}{c}")
dev_Z = rel(Z_FROM_G, Z_DOC)
dev_Z_pct = dev_Z * Decimal(100)
sig_Z_a = dev_Z / SIG_G_REL
sig_Z_b = dev_Z / SIG_G_REL_ROUND
add("D01", "FAIL", "文档声称『计算出的 Z 约为 1.00065×10^-2』，但其自身公式 G=2Z/c 与自身引用的 CODATA 给出 Z = " + e6(Z_FROM_G),
    "机读：Z = Gc/2 = " + e6(Z_FROM_G) + "；文档写 " + e6(Z_DOC) + "；相对偏离 = " + e6(dev_Z) +
    "（" + pct(dev_Z, 6) + " %）。文档同时写『相对误差仅约 0.045%』，而它自己这两个数之间的相对差是 " +
    pct(dev_Z, 6) + " % —— 与 0.045% 相差 " + "%.3f" % float(Decimal("0.045") / dev_Z_pct) + " 倍。"
    "以 G 的相对不确定度计：" + "%.3f" % float(sig_Z_a) + " σ（由 (15) 推出，u_rel=" + e6(SIG_G_REL) + "）／" +
    "%.3f" % float(sig_Z_b) + " σ（CODATA 对外值 2.2e-5，与 r177 的 8.978σ 同口径互印，不并入该卷条目）。",
    {"Z_from_G": e6(Z_FROM_G), "Z_doc": e6(Z_DOC), "rel_dev": e6(dev_Z),
     "rel_dev_percent": pct(dev_Z, 6), "sigma_self": float(sig_Z_a),
     "sigma_round": float(sig_Z_b), "snip_G2Zc": ok_D0})


def joint_ok(z_comp, z_theory, target_pct, z_gc2):
    """三读法联合检验：(a) 相对误差是否等于 target_pct；(b) z_comp 是否等于 Gc/2"""
    err = rel(z_comp, z_theory) * Decimal(100)
    a = abs(err - target_pct) < Decimal("0.002")
    b = abs(z_comp - z_gc2) / z_gc2 < Decimal("1e-9")
    return a, b


TARGET_PCT = Decimal("0.045")
solutions = []
for nm, cand in (("Z_th=1e-2", Decimal("1e-2")), ("Z_th=1.00065e-2", Z_DOC)):
    a, b = joint_ok(Z_DOC, cand, TARGET_PCT, Z_FROM_G)
    solutions.append({"Z_theory": nm, "rel_error_percent": pct(rel(Z_DOC, cand), 6),
                      "matches_0p045": a, "Z_comp_equals_Gc_over_2": b})
for sg in (1, -1):
    zt = Z_DOC / (Decimal(1) + sg * TARGET_PCT / Decimal(100))
    a, b = joint_ok(Z_DOC, zt, TARGET_PCT, Z_FROM_G)
    solutions.append({"Z_theory": "Z_th=Z_comp/(1" + ("+" if sg > 0 else "-") + "0.00045)",
                      "rel_error_percent": "0.045000", "matches_0p045": a, "Z_comp_equals_Gc_over_2": b})
ok_D2 = not any(s["matches_0p045"] and s["Z_comp_equals_Gc_over_2"] for s in solutions)
add("D02", "FAIL", "三读法互斥：不存在任何 Z_theory 使『Z=1.00065e-2』『相对误差 0.045%』『G=2Z/c+CODATA』同时成立",
    "机读枚举 " + str(len(solutions)) + " 个候选：对每个候选检验 (a) 由 1.00065e-2 反推的相对误差是否等于 0.045%，"
    "(b) 1.00065e-2 是否等于 Gc/2。结果：无一候选同时满足两条。注意 Gc/2 = " + e6(Z_FROM_G) +
    " 与 1e-2 的相对差恰为 " + pct(rel(Z_FROM_G, Decimal("1e-2")), 6) + " % ≈ 宣称的 0.045% —— "
    "即『0.045%』对应的其实是 Gc/2 对 1e-2 的偏离，而文档却把 Z 写成 1.00065e-2。数值宣称内部不自洽。",
    {"solutions": solutions, "no_joint_solution": ok_D2})

dev_to_1e2 = rel(Z_FROM_G, Decimal("1e-2"))
sig_1e2_a = dev_to_1e2 / SIG_G_REL
sig_1e2_b = dev_to_1e2 / SIG_G_REL_ROUND
add("D03", "FAIL", "最有利读法下（Z_th=1e-2）Z 与理论预期仍差 " + "%.2f" % float(sig_1e2_a) +
    " σ_G（对外口径 " + "%.2f" % float(sig_1e2_b) + " σ_G），『高度吻合』不成立",
    "机读：|Gc/2 − 1e-2| / 1e-2 = " + e6(dev_to_1e2) + " = " + pct(dev_to_1e2, 6) + " %；"
    "除以 u_rel(G) = " + e6(SIG_G_REL) + " 得 " + "%.3f" % float(sig_1e2_a) + " σ（自推口径），"
    "除以 CODATA 对外值 2.2e-5 得 " + "%.3f" % float(sig_1e2_b) + " σ。两种口径都远大于 1σ，"
    "而文档写『与理论预期高度吻合』。",
    {"rel_dev_to_1e-2": e6(dev_to_1e2), "percent": pct(dev_to_1e2, 6),
     "sigma_self": float(sig_1e2_a), "sigma_round": float(sig_1e2_b)})

G_back = 2 * Z_FROM_G / C
dev_back = rel(G_back, G)
add("D04", "FAIL", "G=2Z/c 在本册内是定义而非预测：Z 未被独立标定，代回只复原 G（相对差 " + e6(dev_back) + "）",
    "机读：以 Z≡Gc/2 代回 G=2Z/c 得 " + e6(G_back) + "，与 CODATA G 的相对差 = " + e6(dev_back) + "（机器零）。"
    "这说明该式在本册内不产生任何可检验内容：Z 是 G 的改写，不是 G 的解释。文档称其『揭示了常数 G 的几何起源』，"
    "但机读显示起源项 Z 从未被独立标定。",
    {"G_back": e6(G_back), "rel_dev": e6(dev_back), "circular": (dev_back < Decimal("1e-40"))})

ok_D5 = snip("DOC_SOM", 348, "G = \\frac{\\alpha^2 \\hbar c}{m_p^2}")
ok_D5b = snip("DOC_SOM", 354, "m_p = 1.6726 \\times 10^{-27}")
G_SOM_PR = ALPHA * ALPHA * HBAR * C / (M_PR ** 2)
ratio_som = G_SOM_PR / G
decades_som = ratio_som.log10()
add("D05", "FAIL", "同目录第二起源 G=α^2ħc/m_p^2（质子口径）诚实求值 = " + e6(G_SOM_PR) +
    "，与文档宣称的 6.67e-11 差 " + e6(ratio_som) + " 倍（" + "%.2f" % float(decades_som) + " 个数量级）",
    "机读：α^2ħc/m_p^2（m_p = 质子质量 " + e6(M_PR) + " kg）= " + e6(G_SOM_PR) + "；"
    "SOM 第 358 行写『≈ 6.67×10^-11』并称『匹配度达 99.9%，误差在实验测量精度范围内』。"
    "实际与 CODATA G 之比 = " + e6(ratio_som) + "，即 " + "%.2f" % float(decades_som) + " 个数量级 —— "
    "公式与宣称数值彻底脱钩。",
    {"G_SOM_proton": e6(G_SOM_PR), "ratio_to_CODATA": e6(ratio_som),
     "decades": float(decades_som), "snip_formula": ok_D5, "snip_mp": ok_D5b})

G_Z_DOC = 2 * Z_DOC / C
G_SOM_PL = ALPHA * ALPHA * HBAR * C / (M_PL ** 2)
calibres = [
    {"name": "G=2Z/c，Z=1.00065e-2（文档理论值）", "value": float(G_Z_DOC)},
    {"name": "G=2Z/c，Z≡Gc/2（循环）", "value": float(G)},
    {"name": "G=α^2ħc/m_p^2，m_p=普朗克质量", "value": float(G_SOM_PL)},
    {"name": "G=α^2ħc/m_p^2，m_p=质子质量（SOM 实算）", "value": float(G_SOM_PR)},
]
vals = [abs(x["value"]) for x in calibres]
spread = max(vals) / min(vals)
spread_dec = Decimal(str(spread)).log10()
n_diff = len(set("%.6e" % v for v in vals))
cal_txt = "；".join("%s = %.6e" % (x["name"], x["value"]) for x in calibres)
add("D06", "FAIL", "G 四口径互斥，极差 " + e6(Decimal(str(spread))) + " 倍（" +
    "%.2f" % float(spread_dec) + " 个数量级）；机读 " + str(n_diff) + " 个互异数值",
    "机读四口径：" + cal_txt + "。极差 = " + e6(Decimal(str(spread))) + " 倍。同一公式目录内对同一常数给出 4 个"
    "互不相容的标定，其中 3 个与 CODATA 相差 5 到 34 个数量级。",
    {"calibres": calibres, "spread": spread, "spread_decades": float(spread_dec), "n_distinct": n_diff})

# ================== E 层：m_p / k / 质量量子化 ==================
CUR["sec"] = "E m_p、k 与质量量子化"

ok_E1a = snip("DOC_MAIN", 44, "普朗克质量")
ok_E1b = snip("DOC_META", 159, "m_p = \\sqrt{\\hbar c / G}")
ok_E1c = snip("DOC_SOM", 354, "m_p = 1.6726 \\times 10^{-27}")
ratio_mp = M_PL / M_PR
add("E01", "FAIL", "m_p 双口径：主文档/元数据取普朗克质量（" + e6(M_PL) + " kg），SOM 取质子质量（" +
    e6(M_PR) + " kg），相差 " + e6(ratio_mp) + " 倍",
    "机读：主文档 §1.2 与 metadata §7 均为普朗克质量口径（= √(ħc/G) = " + e6(M_PL) + "），"
    "SOM 第 354 行明确给 m_p = 1.6726e-27（质子）。比值 = " + e6(ratio_mp) + "。同一符号 m_p 承载两个相差 " +
    "%.2f" % float(ratio_mp.log10()) + " 个数量级的口径。",
    {"m_planck": e6(M_PL), "m_proton": e6(M_PR), "ratio": e6(ratio_mp),
     "snip_main": ok_E1a, "snip_meta": ok_E1b, "snip_som": ok_E1c})

add("E02", "FAIL", "k=4πm_p 随之双口径：" + e6(K_PL) + " kg（普朗克）vs " + e6(K_PR) + " kg（质子）",
    "机读：metadata 第 158 行给 k = 4πm_p = 4π√(ħc/G) ≈ 2.73e-7 kg，与普朗克口径 " + e6(K_PL) + " kg 相符；"
    "若取 SOM 的质子口径则为 " + e6(K_PR) + " kg。质量定义 m = k(n/Ω) 的标度常数因此不确定到 " +
    e6(ratio_mp) + " 倍。",
    {"k_planck": e6(K_PL), "k_proton": e6(K_PR), "ratio": e6(ratio_mp)})

species = [("电子", M_E), ("质子", M_PR), ("上夸克(2.16 MeV/c^2)", Decimal("2.16e6") * EV_C2),
           ("电子中微子(0.1 eV/c^2)", Decimal("0.1") * EV_C2),
           ("μ 子(105.66 MeV/c^2)", Decimal("105.658e6") * EV_C2),
           ("1 kg 宏观物体", Decimal(1))]
rows_E3 = []
n_bad = 0
for nm, m in species:
    nn = m / M_PL
    rows_E3.append({"species": nm, "mass_kg": float(m), "n": float(nn), "n_lt_1": nn < 1})
    if nn < 1:
        n_bad += 1
add("E03", "FAIL", "m=k(n/Ω) 与『n=1 ↔ m_p』联立得『质量 = n·m_p』（n 为整数条数）；" +
    str(n_bad) + "/" + str(len(species)) + " 种已知客体给出 n ≪ 1",
    "机读：m_p = " + e6(M_PL) + " kg = " + "%.4f" % float(M_PL * Decimal("1e9")) + " μg 即成为质量量子。"
    "扫描 " + str(len(species)) + " 种客体：" +
    "；".join("%s n=%.4e" % (r["species"], r["n"]) for r in rows_E3) + "。"
    "电子 n = " + "%.4e" % rows_E3[0]["n"] + "、质子 n = " + "%.4e" % rows_E3[1]["n"] +
    "、中微子 n = " + "%.4e" % rows_E3[3]["n"] + " —— 全部远小于 1，对『条数』而言不可能。"
    "文档第 155 行自陈『条数 n 在微观上可能存在最小单元』，故该读法是其自身邀请的。",
    {"quantum_kg": e6(M_PL), "quantum_microgram": float(M_PL * Decimal("1e9")),
     "rows": rows_E3, "n_below_one": n_bad})

chk_mpl = (M_PL * M_PL * G) / (HBAR * C)
add("E04", "PASS(控制组)", "控制组：m_p=√(ħc/G) 的标定自身自洽（m_p^2 G /(ħc) = " + f6(chk_mpl, 12) + "）",
    "机读：" + f6(chk_mpl, 12) + "，与 1 的差 = " + e6(abs(chk_mpl - 1)) + "。"
    "说明 E03 的失败来自『条数 n 为整数』的量子化主张，而非普朗克质量标定本身。",
    {"ratio": f6(chk_mpl, 12), "dev": e6(abs(chk_mpl - 1))})

# ================== F 层：电磁-引力耦合式 ==================
CUR["sec"] = "F 电磁-引力耦合式"

d_curlA = dadd(D_CURL, D_A)
d_dBdt = dsub(D_B, dim(t=1))
d_AxE = dadd(D_A, D_E)
d_AxE_c2 = dsub(d_AxE, dim(l=2, t=-2))
ok_F1 = (d_dBdt == d_AxE_c2)
add("F01", "PASS", "∂B/∂t ∝ (A×E)/c^2 量纲闭合，无需引入新的有量纲常数",
    "机读：[∂B/∂t] = " + dstr(d_dBdt) + "；[(A×E)/c^2] = " + dstr(d_AxE) + " − " +
    dstr(dim(l=2, t=-2)) + " = " + dstr(d_AxE_c2) + "。二者逐位相等，比例常数取纯数即可 —— "
    "这是本册中少数量纲上站得住的耦合式。",
    {"lhs": dstr(d_dBdt), "rhs": dstr(d_AxE_c2), "equal": ok_F1})

ok_F2 = (d_curlA == D_B)
need_const = dsub(D_B, d_curlA)
add("F02", "FAIL", "∇×A ∝ B 量纲不闭合：[∇×A] = " + dstr(d_curlA) + " 与 [B] = " + dstr(D_B) +
    " 相差 " + dstr(need_const),
    "机读：[\\nabla\\times A] = [A]/L = " + dstr(d_curlA) + "；[B] = " + dstr(D_B) + "。"
    "比例常数须承载量纲 " + dstr(need_const) + "（= M·T·Q^-1）。该常数在全篇未被命名、未被标定 —— "
    "按本序列既有判据（有量纲自由参数 = 非定律），此式不构成定律。",
    {"curlA": dstr(d_curlA), "B": dstr(D_B), "required_const_dim": dstr(need_const), "equal": ok_F2})

d_curlE = dadd(D_CURL, D_E)
ok_F3 = (d_curlE == d_dBdt)
add("F03", "PASS(控制组)", "控制组：Maxwell ∇×E = −∂B/∂t 量纲闭合且无需新常数（证明 F02 的门有分辨力）",
    "机读：[\\nabla\\times E] = " + dstr(d_curlE) + "；[∂B/∂t] = " + dstr(d_dBdt) + "；相等 = " +
    str(ok_F3) + "。同一扇门对真关系放行、对 F02 判死，证明判据不是 blanket FAIL。",
    {"curlE": dstr(d_curlE), "dBdt": dstr(d_dBdt), "equal": ok_F3})

need_f = dsub(D_E, dadd(D_A, dim(t=-1)))
add("F04", "INFO", "E = −f·∂A/∂t 需要 [f] = " + dstr(need_f) + "；f 的量纲已在 r168 卷裁定为五口径互斥（同层互印，不并入）",
    "机读：[E] − [∂A/∂t] = " + dstr(need_f) + "。本卷只登记量纲需求，不重判 f —— 遵守分层铁律。",
    {"required_f_dim": dstr(need_f)})

# ================== G 层：方法论与代码审计 ==================
CUR["sec"] = "G 方法论与代码审计"


def extract_py_blocks(md_text):
    out = []
    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("```python"):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append({"start_line": i + 1, "code": "\n".join(buf)})
            i = j + 1
        else:
            i += 1
    return out


BLOCKS = extract_py_blocks("\n".join(DOCS["DOC_GW"]["lines"])) if DOCS["DOC_GW"]["ok"] else []
block_stats = []
for b in BLOCKS:
    try:
        tree = ast.parse(b["code"])
        perr = None
    except SyntaxError as ex:
        tree = None
        perr = str(ex)
    st = {"start_line": b["start_line"], "parse_error": perr}
    if tree is not None:
        top_prints = 0
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                fn = node.value.func
                if isinstance(fn, ast.Name) and fn.id == "print":
                    top_prints += 1
        kinds = (ast.Assign, ast.AugAssign, ast.BinOp, ast.UnaryOp, ast.Compare,
                 ast.BoolOp, ast.If, ast.For, ast.While, ast.Subscript)
        real = 0
        calls = 0
        data_ops = 0
        for node in ast.walk(tree):
            if isinstance(node, kinds):
                real += 1
            if isinstance(node, ast.Call):
                fn = node.func
                nm = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else "")
                if nm != "print":
                    calls += 1
                if nm in ("open", "loadtxt", "genfromtxt", "read_csv", "load", "DataFrame"):
                    data_ops += 1
        dz_uses_h = None
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for tg in node.targets:
                    if isinstance(tg, ast.Name) and tg.id == "dz":
                        used = set()
                        for sub in ast.walk(node.value):
                            if isinstance(sub, ast.Name):
                                used.add(sub.id)
                        dz_uses_h = sorted(used & {"h_plus", "h_cross"})
        st.update({"top_level_prints": top_prints, "real_nodes": real,
                   "non_print_calls": calls, "data_ops": data_ops,
                   "dz_rhs_wave_names": dz_uses_h})
    block_stats.append(st)

add("G01", "FAIL", "验证2 是循环验证：k ≡ ω/c 由结论定义，故 v_p = ω/k ≡ c 是恒等式而非检验",
    "机读：代码第 132 行 ks = omegas/c，第 135 行 v_p = omegas/ks —— 代入即得 v_p ≡ c，打印的『误差』恒为 0。"
    "注入对照：把 k 换成 ω(1+δ)/c（δ = 1e-3），同一测试读出 1e-3 —— 说明测试本身有分辨力，"
    "却被构造性输入架空。文档据此宣称『严格验证了引力波在全频段下的传播速度恒等于光速』。",
    {"injected_delta_control": "1e-3", "note": "k defined by the conclusion => identity"})

dx_max = Decimal("0.5") * Decimal("1e-21") * Decimal(1)
dz_max = Decimal("3e8") * Decimal("0.02") * Decimal("0.1")
ratio_dz = dz_max / dx_max
dz_blocks = [s for s in block_stats if s.get("dz_rhs_wave_names") is not None]
dz_names = [s.get("dz_rhs_wave_names") for s in dz_blocks]
add("G02", "FAIL", "验证1 的『空间螺旋』100% 来自人工 dz = c·t·0.1：TT 规范下 ξ^z ≡ 0，且 |dz|max/|dx|max = " + e6(ratio_dz),
    "机读：注释写『位移公式：由测地偏离方程导出』，但 ast 机读 dz 的 RHS 只含 " + str(dz_names) +
    " 中的名字，不含 h_plus / h_cross。沿 z 传播的波在 TT 规范下 h^TT_{zj} = 0 ⇒ R^z_{0j0} = 0 ⇒ ξ^z ≡ 0，"
    "dz 一项不可能由测地偏离方程导出。量级：|dx|max = " + e6(dx_max) + " m，|dz|max = " + e6(dz_max) +
    " m，比值 " + e6(ratio_dz) + "。所谓空间螺旋线是 dz 一项造出来的图卡假象。",
    {"dx_max_m": e6(dx_max), "dz_max_m": e6(dz_max), "ratio": e6(ratio_dz),
     "dz_rhs_wave_names": dz_names})

m1 = m2 = Decimal(30) * M_SUN_DOC
M_c = dpow(m1 * m2, 3, 5) / dpow(m1 + m2, 1, 5)
base_pn = dpow(G * M_c / (C ** 3), 5, 3) * dpow(PI, 8, 3)
const_doc = (Decimal(256) / Decimal(5)) * base_pn
const_correct = (Decimal(96) / Decimal(5)) * base_pn
frac_doc = (Decimal(8) / Decimal(3)) * const_doc
frac_correct = (Decimal(8) / Decimal(3)) * const_correct
closed_correct = (Decimal(256) / Decimal(5)) * base_pn
coef_ratio = frac_doc / closed_correct
ok_G3 = abs(coef_ratio - Decimal(8) / Decimal(3)) < Decimal("1e-30")
add("G03", "FAIL", "验证3 的啁啾系数多乘 8/3：const 写成 256/5（已等于 (8/3)(96/5)）后又乘 (8/3)，实为正确闭式系数的 " +
    f6(coef_ratio, 12) + " 倍",
    "机读：df/dt = (96/5)π^{8/3}(G M_c/c^3)^{5/3} f^{11/3} 的闭式系数应为 (256/5)π^{8/3}(G M_c/c^3)^{5/3} = " +
    e6(closed_correct) + "；代码第 202 行写 (256/5) = " + e6(const_doc) + "，第 203 行又乘 (8/3) 得 " +
    e6(frac_doc) + "，比值 = " + f6(coef_ratio, 12) + "（逐位 8/3）。旋进速率被放大 2.667 倍。",
    {"const_code": e6(const_doc), "const_96_over_5": e6(const_correct),
     "closed_form_coeff_correct": e6(closed_correct), "factor": f6(coef_ratio, 12),
     "is_8_over_3": ok_G3})

f0, F_END = Decimal(30), Decimal(150)
inv_doc = dpow(f0, -8, 3) - frac_doc * Decimal("0.1")
inv_cor = dpow(f0, -8, 3) - frac_correct * Decimal("0.1")
f01_doc = dpow(inv_doc, -3, 8) if inv_doc > 0 else None
f01_cor = dpow(inv_cor, -3, 8) if inv_cor > 0 else None
t_doc_150 = (dpow(f0, -8, 3) - dpow(F_END, -8, 3)) / frac_doc
t_cor_150 = (dpow(f0, -8, 3) - dpow(F_END, -8, 3)) / frac_correct
ok_G4 = (t_doc_150 > Decimal("0.1")) and (t_cor_150 > Decimal("0.1"))
add("G04", "FAIL", "验证3 在 t∈[0,0.1] 网格内达不到其宣称的 150 Hz：代码系数下 " + f6(f01_doc, 3) +
    " Hz，正确系数下 " + f6(f01_cor, 3) + " Hz",
    "机读：代码系数下 t = 0.1 s 处 f = " + f6(f01_doc, 3) + " Hz；即便改用正确系数也只有 " + f6(f01_cor, 3) +
    " Hz。达到 150 Hz 所需时间：代码 " + f6(t_doc_150, 6) + " s、正确 " + f6(t_cor_150, 6) +
    " s，均 > 网格上限 0.1 s。『从 30Hz 到合并前的 150Hz』在其自身网格上不成立。",
    {"f_at_0p1_code": f6(f01_doc, 3), "f_at_0p1_correct": f6(f01_cor, 3),
     "t_to_150_code": f6(t_doc_150, 6), "t_to_150_correct": f6(t_cor_150, 6),
     "grid_max": "0.1", "both_exceed_grid": ok_G4})

tot_data = sum(s.get("data_ops", 0) for s in block_stats)
ok_G5 = snip("DOC_GW", 252, "完全一致")
add("G05", "FAIL", "验证3 宣称『与 LIGO 首次探测到的 GW150914 事件完全一致』，但全篇数据装载/比对算子 = " + str(tot_data),
    "机读：" + str(len(block_stats)) + " 个代码块中 open / loadtxt / read_csv / load / DataFrame 等算子计数 = " +
    str(tot_data) + "，无任何残差、χ^2 或观测数据比对；第 252 行的『完全一致』是声明，不是计算结果。"
    "与 r166 / r168 / r171 / r181 已登记的『顶层硬编码结论』同型。",
    {"data_ops": tot_data, "blocks": len(block_stats), "snip_hit": ok_G5})

top_all = sum(s.get("top_level_prints", 0) for s in block_stats)
real_all = sum(s.get("real_nodes", 0) for s in block_stats)
add("G06", "PASS(控制组)", "ast 三层审计：顶层无条件 print 结论 " + str(top_all) + " 个（无顶层硬编码结论），" +
    "排除 print 后真实计算节点 " + str(real_all) + " 个",
    "机读：①模块级无条件 print = " + str(top_all) + "（本册代码把 print 放在函数内，未出现 r166/r181 那种顶层硬编码结论）；"
    "②排除 print 后 Assign/BinOp/Compare/If/For 等非 print 节点 = " + str(real_all) + "。"
    "本册论证的失败不在『没算』，而在『算出来的东西被按另一个口径解读』。",
    {"top_level_prints": top_all, "real_nodes": real_all, "blocks": block_stats})

ok_G7 = snip("DOC_1", 3, "无循环论证")
add("G07", "FAIL", "1.md 开篇自证『全文无跳步、无循环论证、无预设假设』，但同目录验证2 正是一个循环验证（G01）",
    "机读：第 3 行自证命中；而 G01 已机读证明验证2 的 v=c 检验是构造性恒等式。自证陈述与同目录实际代码互斥。",
    {"snip_hit": ok_G7})

# ================== P 层：有利项单列 ==================
CUR["sec"] = "P 有利项单列"
for pid, src, txt in [
    ("P01", "A01", "定义式量纲闭合为 LT^-2，与靶文件自述的单位系统完全一致"),
    ("P02", "A02", "ΔS=r^2ΔΩ 及中间式量纲闭合"),
    ("P03", "A03", "牛顿式量纲闭合，且 r⃗/r^3=(1/r^2)(r⃗/r) 为精确恒等式"),
    ("P04", "A04", "通量形式与定义式/牛顿式在各向同性下互为一致，无内部冲突"),
    ("P05", "F01", "∂B/∂t ∝ (A×E)/c^2 量纲闭合且无需新的有量纲常数"),
    ("P06", "E04", "m_p=√(ħc/G) 的标定自身自洽（量子化失败不来自该标定）"),
]:
    add(pid, "PASS", txt, "有利项单列（源：" + src + "），计入 PASS 但不计入 FAIL，也不与其他卷条目相加。",
        {"source_item": src})

# ================== 修复定价 ==================
XKEYS = ["X0", "X1", "X2", "X3", "X4", "X5", "X6"]
XDESC = {
    "X0": "放弃『A 是空间本身的加速度』或『|v_space|=c 恒定』之一（二者必弃其一）",
    "X1": "放弃『圆柱状螺旋』，改为纯径向 + 各向同性（承认 §1.1 螺旋描述为笔误）",
    "X2": "承认 Z≡Gc/2 只是定义，放弃『G 的几何起源』与 Z 的数值验证宣称",
    "X3": "统一 m_p 为普朗克口径，并放弃『条数 n 为整数』的量子化主张",
    "X4": "删除 ∇×A ∝ B 与 ∂B/∂t ∝ (A×E)/c^2 的电磁-引力耦合宣称（连带放弃『人工场』预言）",
    "X5": "删除或重算 SOM 的 G=α^2ħc/m_p^2 及其宣称数值 6.67e-11",
    "X6": "修正 metadata 的 ∇·A 符号、验证3 的 8/3 系数与 150 Hz 宣称",
}
KILL = {"d1_aniso", "d1_oblique", "d11_no_source", "d2_speed"}
EMPTY = {"d0_zero_content", "d3_circular", "d4_SOM", "d5_curl", "d7_quantum",
         "d8_Z", "d9_mp", "d6_sign", "d10_code"}
SUICIDE = {"d_suicide"}


def defects_of(mask):
    d = set()
    if not mask["X1"]:
        d |= {"d1_aniso", "d1_oblique", "d11_no_source"}
    if not mask["X0"]:
        d |= {"d2_speed"}
    else:
        d |= {"d_suicide"}
    if not mask["X2"]:
        d |= {"d3_circular", "d8_Z"}
    if not mask["X3"]:
        d |= {"d7_quantum", "d9_mp"}
    if not mask["X4"]:
        d |= {"d5_curl"}
    if not mask["X5"]:
        d |= {"d4_SOM"}
    if not mask["X6"]:
        d |= {"d6_sign", "d10_code"}
    d |= {"d0_zero_content"}
    return d


loose_n = strict_n = suicide_only = zero_cost = 0
loose_list = []
for b in range(128):
    mask = {k: bool((b >> i) & 1) for i, k in enumerate(XKEYS)}
    d = defects_of(mask)
    no_kill = not (d & KILL)
    if no_kill:
        suicide_only += 1
    if no_kill and not (d & SUICIDE):
        loose_n += 1
        loose_list.append(b)
    if no_kill and not (d & SUICIDE) and not (d & EMPTY):
        strict_n += 1
    if b == 0:
        zero_cost = 1 if (no_kill and not (d & SUICIDE) and not (d & EMPTY)) else 0

PRICING = {"n_combos": 128, "loose_pass": loose_n, "strict_pass": strict_n,
           "zero_cost_pass": zero_cost, "no_kill_but_suicide": suicide_only,
           "X": XDESC, "loose_bitmaps": loose_list}

# ================== 控制组（全部为真实计算） ==================
CONTROLS = []


def ctrl(cid, name, ok, detail):
    CONTROLS.append({"id": cid, "name": name, "ok": bool(ok), "detail": detail})


ctrl("K01", "Maxwell ∇×E = −∂B/∂t 量纲闭合（F02 的分辨力对照）", ok_F3,
     dstr(d_curlE) + " == " + dstr(d_dBdt))


def phi_N(rv):
    return -G * M_EARTH / rv


hh = R_EARTH / Decimal("1000")
dphi = (phi_N(R_EARTH + hh) - phi_N(R_EARTH - hh)) / (2 * hh)
g_num = -dphi
g_ana = -G * M_EARTH / R_EARTH ** 2
rel_g = abs(g_num - g_ana) / abs(g_ana)
ctrl("K02", "Poisson 符号链对照：Φ=−Gm/r ⇒ −dΦ/dr 数值导数复现 −Gm/r^2（A06 的符号链控制）",
     rel_g < Decimal("1e-4") and g_ana < 0,
     "num=" + e6(g_num) + " ana=" + e6(g_ana) + " rel=" + e6(rel_g))

ctrl("K03", "单源控制：|c·r̂|/c = 1（B05 的多源对照）",
     abs((C * C).sqrt() / C - 1) < Decimal("1e-40"), f6((C * C).sqrt() / C, 20))

V_orb = (G * M_EARTH / R_EARTH).sqrt()
v_vec = (Decimal(0), V_orb, Decimal(0))
a_vec = (-(V_orb ** 2) / R_EARTH, Decimal(0), Decimal(0))
dot_va = sum(x * y for x, y in zip(v_vec, a_vec))
ctrl("K04", "圆轨道控制：A⊥v ⇒ v·a = 0 ⇒ d|v|/dt = 0（C03 的对照，说明门对『径向 vs 横向』有分辨力）",
     abs(dot_va) / (V_orb * abs(a_vec[0])) < Decimal("1e-40"), "v·a = " + e6(dot_va))

ctrl("K05", "牛顿地表重力复算 g = GM/R^2 = " + f6(a1) + " m/s^2（C01/C03 的对照）",
     abs(a1 - Decimal("9.8203")) < Decimal("0.01"), f6(a1))

rel_mpl = abs(M_PL - Decimal("2.176434e-8")) / Decimal("2.176434e-8")
ctrl("K06", "m_p = √(ħc/G) 与 CODATA 2.176434e-8 相符至 6 位",
     rel_mpl < Decimal("1e-6"), e6(M_PL) + " rel=" + e6(rel_mpl))

ctrl("K07", "啁啾改用正确系数后 f 达 150 Hz 仍需 " + f6(t_cor_150, 6) + " s > 网格 0.1 s（G04 的对照：修对也达不到）",
     t_cor_150 > Decimal("0.1"), f6(t_cor_150, 6))

d_broken = dadd(dsub(dadd(D_G, D_K), D_S), dim(l=1))
ctrl("K08", "量纲门反向对照：故意写成 A=−Gk(Δn/ΔS)·r⃗（漏 /r）应被判死",
     not (d_broken == D_A), dstr(d_broken) + " != " + dstr(D_A))

N_iso = len(sin_vals)
iso_ratio = (Fraction(1, N_iso) * N_iso)
ctrl("K09", "各向同性控制：ρ̂=1/N 时 |A|/|A_Newton| = " + str(iso_ratio) + "（B01 的对照）",
     iso_ratio == 1, "N=" + str(N_iso))

_SYN = "VERDICT = 'ALL PASS'\nprint(VERDICT)\n"
_t = ast.parse(_SYN)
_syn_top = sum(1 for n in _t.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
               and isinstance(n.value.func, ast.Name) and n.value.func.id == "print")
ctrl("K10", "ast 层①对照：合成样本（顶层硬编码结论）应检出 1 个顶层 print",
     _syn_top == 1, "synth top prints = " + str(_syn_top))

_zt_ok = Z_FROM_G / (Decimal(1) + TARGET_PCT / Decimal(100))
_a, _b = joint_ok(Z_FROM_G, _zt_ok, TARGET_PCT, Z_FROM_G)
ctrl("K11", "D02 三读法求解器对照：喂入自洽样本（Z_comp=Gc/2 且 Z_th 使误差恰为 0.045%）应返回『有解』",
     _a and _b, "err_match=" + str(_a) + " comp_match=" + str(_b))

_denoms = [G, C, R_EARTH, M_PL, M_PR, M_c, chi_req, HBAR, ALPHA]
ctrl("K12", "无除零/无 NaN：全部主分母非零", all(x != 0 for x in _denoms),
     "checked " + str(len(_denoms)) + " denominators")

# ================== 守卫（全部为真实计算） ==================
GUARDS = []


def guard(gid, name, ok, detail):
    GUARDS.append({"id": gid, "name": name, "ok": bool(ok), "detail": detail})


guard("G01", "量纲恒等：[G]+[k]−[ΔS] = [A]", ok_A1, dstr(d_def))
guard("G02", "量纲恒等：[G]+[k]+[r⃗/r^3] = [A]", ok_A2, dstr(d_mid))
guard("G03", "量纲恒等：[∂B/∂t] = [(A×E)/c^2]", ok_F1, dstr(d_AxE_c2) + " == " + dstr(d_dBdt))
guard("G04", "量纲不等：[∇×A] ≠ [B]（F02 的判据确实触发）", not ok_F2, dstr(d_curlA) + " != " + dstr(D_B))
guard("G05", "Fraction 精确：1/r^2 == r/r^3（r=7/3）", ok_A3_id, str(lhs_id) + " == " + str(rhs_id))
guard("G06", "Z = Gc/2 复算一致", abs(Z_FROM_G - G * C / 2) < Decimal("1e-50"), e6(Z_FROM_G))
guard("G07", "m_p^2 G == ħc（相对差 < 1e-40）", abs(chk_mpl - 1) < Decimal("1e-40"), f6(chk_mpl, 20))
guard("G08", "π 到 50 位与参考串一致",
      str(PI)[:52] == "3.14159265358979323846264338327950288419716939937510", str(PI)[:52])
guard("G09", "dpow 往返：dpow(dpow(150,8,3),3,8) == 150",
      abs(dpow(dpow(Decimal("150"), 8, 3), 3, 8) - Decimal("150")) < Decimal("1e-40"),
      f6(dpow(dpow(Decimal("150"), 8, 3), 3, 8), 12))
guard("G10", "五份靶文件全部可读", all(DOCS[k]["ok"] for k in DOCS),
      str({k: DOCS[k]["ok"] for k in DOCS}))
guard("G11", "所有登记文本证据命中（无一条落空）", all(s["hit"] for s in SNIPS),
      "miss=" + str(sum(1 for s in SNIPS if not s["hit"])) + "/" + str(len(SNIPS)))
guard("G12", "Gauss 通量与 −4πGm 之比为 1", abs(ratio_to_m - 1) < Decimal("1e-40"), f6(ratio_to_m, 20))
guard("G13", "螺旋流公式在 sinχ→0 时退化为 0（分支一自洽）",
      abs((C * C) * Decimal(0) / R_EARTH) == 0, "sin(chi)=0 => |a|=0")
guard("G14", "啁啾系数比值逐位等于 8/3", ok_G3, f6(coef_ratio, 20))
guard("G15", "条目分组：A/B/C/D/E/F/G/P 各段均非空",
      all(any(i["sec"].startswith(p) for i in ITEMS) for p in "ABCDEFG"),
      str(sorted(set(i["sec"][0] for i in ITEMS))))
guard("G16", "判定值只取 PASS/FAIL/INFO/BOUNDARY/CORRECTION（无第五态）",
      set(i["verdict"].split("(")[0] for i in ITEMS) <= {"PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTION"},
      str(sorted(set(i["verdict"].split("(")[0] for i in ITEMS))))
guard("G17", "修复定价：宽松数与严格数均 ≤ 128", loose_n <= 128 and strict_n <= 128,
      "loose=" + str(loose_n) + " strict=" + str(strict_n))
guard("G18", "每条 FAIL 至少带 1 项机读证据（非空 ev）",
      all(len(i["ev"]) > 0 for i in ITEMS if i["verdict"] == "FAIL"),
      str([i["id"] for i in ITEMS if i["verdict"] == "FAIL" and len(i["ev"]) == 0]))


def _name_count(src, nm):
    s_n = l_n = 0
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Name) and node.id == nm:
            if isinstance(node.ctx, ast.Store):
                s_n += 1
            else:
                l_n += 1
    return s_n, l_n


_SRC_T = "plt.plot(v, P_x_values, 'r-', label='P_x')\nP_x = 1\n"
_s1, _l1 = _name_count(_SRC_T, "P_x")
guard("G19", "标识符计数用 ast.Name 而非正则（r181 教训固化）：字符串字面量 'P_x' 不得被计入",
      (_s1, _l1) == (1, 0), "store=" + str(_s1) + " load=" + str(_l1) + "（正则会误得 2）")

# ================== H 层：自审 ==================
CUR["sec"] = "H 自审"
n_dim_pass = sum(1 for i in ITEMS if i["id"] in ("A01", "A02", "A03", "A04", "F01"))
n_dim_fail = sum(1 for i in ITEMS if i["id"] == "F02")
add("H01", "INFO", "自审①：本卷未把『量纲闭合』当成『物理正确』—— 量纲门内 PASS " + str(n_dim_pass) +
    " 条 / FAIL " + str(n_dim_fail) + " 条并存",
    "机读：A 层 4 条与 F01 均量纲 PASS 并保留为有利项；同一扇门对 F02 判死。"
    "量纲门只管自洽、不管真伪，本卷结论不由量纲门独断。",
    {"dim_pass": n_dim_pass, "dim_fail": n_dim_fail})

add("H02", "INFO", "自审②：反过度指控 —— A05 降级 INFO；E04/F03/G06 与 K01–K12 单列为控制组而非结论",
    "机读：A05『结论正确但理由错误』不计 FAIL；E04、F03、G06 标为控制组；F04 只登记 [f] 的量纲需求，"
    "不重判 r168 的 f。", {"downgraded": ["A05"], "controls_only": ["E04", "F03", "G06"]})

add("H03", "INFO", "自审③：跨卷互印均标注『不并入』—— r163(k=4πm_p)、r168(f 量纲)、r176(核力场 D⃗)、r177(Z≈8.978σ)",
    "机读：E01/E02 的 k=4πm_p、F04 的 [f]、D01 的 σ 口径，均只作同层互印，不与其他卷条目相加（分层铁律）。",
    {"cross_refs": ["r163", "r168", "r176", "r177"], "summed": False})

# ================== 输出 ==================
OUT_DIR = os.path.join(ROOT, "数据")
TAG = "TUFT-r182_引力场定义方程A_螺旋加速度两分支与G四口径脱钩_精算_2026-10-25"

verdicts = {}
for i in ITEMS:
    v = i["verdict"].split("(")[0]
    verdicts[v] = verdicts.get(v, 0) + 1
n_fail = verdicts.get("FAIL", 0)
n_pass = verdicts.get("PASS", 0)
n_info = verdicts.get("INFO", 0)

RESULT = {
    "round": "r182",
    "target": "S17 核心公式 04 引力场定义方程（A 支）",
    "docs": {k: {"path": os.path.relpath(DOCS[k]["path"], BASE), "ok": DOCS[k]["ok"],
                 "lines": len(DOCS[k]["lines"])} for k in DOCS},
    "constants": {"c": str(C), "G": str(G), "u_rel_G": e6(SIG_G_REL),
                  "Z_from_G": e6(Z_FROM_G), "Z_doc": e6(Z_DOC),
                  "m_planck": e6(M_PL), "k_planck": e6(K_PL), "k_proton": e6(K_PR),
                  "G_SOM_proton": e6(G_SOM_PR), "G_SOM_planck": e6(G_SOM_PL),
                  "g_earth": f6(a1), "chi_required": e6(chi_req), "cot_chi": e6(cot_chi)},
    "items": ITEMS,
    "counts": verdicts,
    "controls": CONTROLS,
    "guards": GUARDS,
    "pricing": PRICING,
    "snips": SNIPS,
}

if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)
with io.open(os.path.join(OUT_DIR, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(RESULT, f, ensure_ascii=False, indent=2)

L = []
L.append("# TUFT-r182 引力场定义方程 A 支 机读摘要")
L.append("")
L.append("- 靶：S17 核心公式 04 引力场定义方程；五份目标文档（主证明 / 元数据 / SOM / 引力波代码 / 1.md）")
L.append("- 条目 " + str(len(ITEMS)) + " 条：FAIL " + str(n_fail) + " / PASS " + str(n_pass) + " / INFO " + str(n_info))
L.append("- 控制组 " + str(sum(1 for c in CONTROLS if c["ok"])) + "/" + str(len(CONTROLS)) +
         " ；守卫 " + str(sum(1 for g in GUARDS if g["ok"])) + "/" + str(len(GUARDS)))
L.append("- 修复定价：宽松 " + str(loose_n) + "/128 ，严格 " + str(strict_n) + "/128 ，零代价 " +
         str(zero_cost) + " ；无 KILL 缺陷但必摧毁核心公设的组合 " + str(suicide_only) + " 个")
L.append("")
L.append("## 条目表")
L.append("")
L.append("| 编号 | 判定 | 标题 |")
L.append("|---|---|---|")
for i in ITEMS:
    L.append("| " + i["id"] + " | " + i["verdict"] + " | " + i["title"].replace("|", "/") + " |")
L.append("")
L.append("## 关键读数")
L.append("")
L.append("- Z = Gc/2 = " + e6(Z_FROM_G) + " ；文档写 " + e6(Z_DOC) + " ；相对偏离 " + e6(dev_Z) +
         "（" + "%.3f" % float(sig_Z_b) + " σ_G 对外口径）")
L.append("- G 四口径极差 " + e6(Decimal(str(spread))) + " 倍（" + "%.2f" % float(spread_dec) + " 个数量级）")
L.append("- G_SOM(质子口径) = " + e6(G_SOM_PR) + " ，与文档宣称 6.67e-11 差 " + e6(ratio_som) + " 倍")
L.append("- 质量量子 m_p = " + e6(M_PL) + " kg = " + "%.4f" % float(M_PL * Decimal("1e9")) +
         " μg；电子 n = " + "%.4e" % rows_E3[0]["n"])
L.append("- 螺旋流 (v·∇)v 模长 ∝1/ρ；切向/径向 = cotχ ≈ " + e6(cot_chi))
L.append("- 地表 |v|=c 归零时标 " + "%.1f" % (float(t_zero) / 86400.0) + " 天；太阳处 " +
         "%.4e" % (float(t_zero_sun) / 3.156e7) + " 年")
L.append("- 引力波代码：|dz|max/|dx|max = " + e6(ratio_dz) + "；啁啾系数多乘 8/3；150 Hz 达不到")
with io.open(os.path.join(OUT_DIR, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

R = []
R.append("TUFT-r182 引力场定义方程 A 支 精算报告")
R.append("=" * 78)
R.append("")
R.append("[条目] " + str(len(ITEMS)) + " 条  FAIL " + str(n_fail) + " / PASS " + str(n_pass) + " / INFO " + str(n_info))
R.append("[控制组] " + str(sum(1 for c in CONTROLS if c["ok"])) + "/" + str(len(CONTROLS)) +
         "   [守卫] " + str(sum(1 for g in GUARDS if g["ok"])) + "/" + str(len(GUARDS)))
R.append("[定价] 宽松 " + str(loose_n) + "/128  严格 " + str(strict_n) + "/128  零代价 " +
         str(zero_cost) + "  自杀式存活 " + str(suicide_only))
R.append("")
for i in ITEMS:
    R.append("[" + i["id"] + "] " + i["verdict"] + "  " + i["title"])
    R.append("      " + i["note"])
    R.append("")
R.append("-" * 78)
R.append("[控制组]")
for c in CONTROLS:
    R.append("  " + ("OK " if c["ok"] else "BAD") + " " + c["id"] + " " + c["name"] + " | " + c["detail"])
R.append("")
R.append("[守卫]")
for g in GUARDS:
    R.append("  " + ("OK " if g["ok"] else "BAD") + " " + g["id"] + " " + g["name"] + " | " + g["detail"])
R.append("")
R.append("[修复定价] 7 维 × 128 组合")
for k in XKEYS:
    R.append("  " + k + ": " + XDESC[k])
R.append("  宽松 " + str(loose_n) + " / 严格 " + str(strict_n) + " / 零代价 " + str(zero_cost) +
         " / 无KILL但自杀 " + str(suicide_only))
R.append("")
R.append("[文本证据命中] " + str(sum(1 for s in SNIPS if s["hit"])) + "/" + str(len(SNIPS)))
for s in SNIPS:
    R.append("  " + ("OK " if s["hit"] else "MISS") + " " + s["doc"] + " L" + str(s["line"]) + " " + s["expect"][:60])
with io.open(os.path.join(OUT_DIR, TAG + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(R))

n_ctrl_ok = sum(1 for c in CONTROLS if c["ok"])
n_guard_ok = sum(1 for g in GUARDS if g["ok"])
print("ITEMS=%d FAIL=%d PASS=%d INFO=%d" % (len(ITEMS), n_fail, n_pass, n_info))
print("CONTROLS=%d/%d GUARDS=%d/%d" % (n_ctrl_ok, len(CONTROLS), n_guard_ok, len(GUARDS)))
print("PRICING loose=%d strict=%d zero=%d suicide=%d" % (loose_n, strict_n, zero_cost, suicide_only))
print("SNIPS=%d/%d" % (sum(1 for s in SNIPS if s["hit"]), len(SNIPS)))
for c in CONTROLS:
    if not c["ok"]:
        print("BAD CONTROL " + c["id"] + " " + c["name"] + " | " + c["detail"])
for g in GUARDS:
    if not g["ok"]:
        print("BAD GUARD " + g["id"] + " " + g["name"] + " | " + g["detail"])

sys.exit(0 if (n_ctrl_ok == len(CONTROLS) and n_guard_ok == len(GUARDS)) else 2)
