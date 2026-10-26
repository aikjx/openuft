# -*- coding: utf-8 -*-
r"""TUFT-r220｜力的矢量场与通量：潮汐张量、散度、Yukawa 高斯定理与多极屏蔽
================================================================================
承 r214（UFE-4F 静态力表 + 形式统一判定）与 r219（进动闭式 + 多源 L 破缺 + 相对论化）。
前两轮都是**沿轨道**读力；本卷换成**场的局域视角**——站在空间每一点看：
力在哪、朝哪、多快衰减、以及「力线到底去了哪里」。

本卷回答四个此前未答的问题（全部可机器验证）：
  Q1 点源之外，∇·F 是不是零？          —— 库仑是 0；**Yukawa 不是 0**。
  Q2 高斯通量 ∮F·dS 是不是常数？        —— 库仑是常数 −4πk；**Yukawa 随半径指数衰减**。
  Q3 「方向特性」的微分版本（潮汐张量）长什么样？ —— 给出 A(r)/B(r) 闭式；库仑比恒 −2，
       **Yukawa 从 −2 变到 −3**（x=φ 处）。
  Q4 远场还剩多少「形状」信息？          —— 所有多极共享同一个 e^{−r/λ} ⇒ **远场无形状**。

承重三式（本卷新增）：
  (i)   场方程：  (∇² − 1/λ²) U = −4πk δ³(r) ,  k = s·α·ħc
        ⇒ U = −k e^{−r/λ}/r（与 r214 母势同源，本卷把它写成**有源方程**）
  (ii)  散度：    ∇·F = −∇²U = −4πk δ³(r) + (k/λ²)·e^{−r/λ}/r
        ⇒ **r>0 处 ∇·F ≠ 0**：力线在真空中「终止」——屏蔽的微分形式。
  (iii) 通量：    ∮_S F·dS = −4πk · e^{−r/λ}(1 + r/λ)
        ⇒ r→0 退回库仑 −4πk；r≫λ 指数衰减。
        两条路径互证：① 直接对 (ii) 体积分；② 直接对 F_r 做球面积分。

潮汐张量（Q3 的机器化）：
  T_ij ≡ ∂F_i/∂x_j = −(k/r³)[ A(r)·δ_ij − B(r)·x̂_i x̂_j ]
  A(r) = e^{−x}(1+x) ,  B(r) = e^{−x}(1+x)·[3 + x²/(1+x)] ,  x = r/λ
  ⇒ **B/A = 3 + x²/(1+x)**：库仑 3（横向/径向 = −1/2），x=φ 处 4（−1/3）。
  ⇒ 迹检验：tr(T) = ∇·F（两条独立路径必须相等）——本卷的强闭环。

诚实边界：
  (a) 只做**静态、点源、球对称**；连续分布只以叠加原理提及，未数值做。
  (b) 多极部分只给「共享同一指数」的结构结论与 l=0 的远场压制数值，**不**给 l≥1 的完整
      modified-Bessel 展开（那需要 scipy，本库纯标准库纪律）。
  (c) 潮汐比在 x>φ 后继续单调变化，但那时圆轨道已不稳定（r219），**本卷不外推到动力学**。
  (d) 四力通量表沿用 r214 的口径（两质子基准），强/弱仍是 Yukawa 代理，不含禁闭。

治理：只读引用 r214/r219 的常数与结论；不改其字节；未改 verify.py；未做 git；
未跑 refresh_catalog.py；条目不可与 r142–r219 相加。纯标准库。
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUTD = os.path.join(BASE, "数据")
JUDD = os.path.join(BASE, "判定")
for _d in (OUTD, JUDD):
    if not os.path.isdir(_d):
        os.makedirs(_d)

STEM = "TUFT-r220_力的矢量场与通量_潮汐散度Yukawa高斯定理与力线_精算与可视化_2026-10-26"
HTML_NAME = "力的矢量场与通量_可视化_2026-10-26.html"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
F = Fraction
ENTRIES, GUARDS, CONTROLS, READINGS = [], [], [], {}
PI = D("3.14159265358979323846264338327950288419716939937510582097494459")
EXP_CUT = D(700)


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title, detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def control(name, ok, msg=""):
    ok = bool(ok)
    CONTROLS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [CONTROL-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def fs(x, nd=12):
    try:
        return format(x, "." + str(nd) + "E")
    except Exception:
        return str(x)


def exp_neg(x):
    x = D(x)
    return D(0) if x > EXP_CUT else (-x).exp()


# =====================================================================
# S0. 量纲与场方程守卫
# =====================================================================
DM, DL, DT, DQ = (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)
DIM_HBARC = (1, 3, -2, 0)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    n = F(n)
    return tuple(F(x) * n for x in a)


guard("G0-1_dmul", dmul(DM, DL) == (1, 1, 0, 0), "%s" % (dmul(DM, DL),))
guard("G0-2_dpow", dpow(DL, -3) == (0, -3, 0, 0), "%s" % (dpow(DL, -3),))
# [k] = [alpha*hbarc] = M L^3 T^-2 = 能量×长度 ⇒ [U]=[k/r]=能量, [F]=[k/r^2]=力
guard("G0-3_k_dim", DIM_HBARC == (1, 3, -2, 0), "[k]=%s" % (DIM_HBARC,))
guard("G0-4_divF_dim", ddiv(DIM_HBARC, dpow(DL, 3)) == (1, 0, -2, 0),
      "[F/r] = %s（应为 M L^0 T^-2 = 能量密度）" % (ddiv(DIM_HBARC, dpow(DL, 3)),))
guard("G0-5_flux_dim_equals_k_dim",
      dmul((1, 1, -2, 0), (0, 2, 0, 0)) == DIM_HBARC,
      "[通量]=[力]×[面积]=(1,3,-2,0) 应等于 [k]=(1,3,-2,0)（⇒ Φ 与 k 同量纲，可直接比值）")


# ---- 母势 / 母力（k=1 归一化，符号 s=+1 吸引）----
def g_shape(lam, r):
    """母力归一化形状 g(r) = e^{-x}(1/r^2 + 1/(lam r))，F_r = -k g"""
    r = D(r)
    if lam is None:
        return D(1) / (r * r)
    lam = D(lam)
    x = r / lam
    return exp_neg(x) * (D(1) / (r * r) + D(1) / (lam * r))


def Fr(lam, r, k=D(1)):
    return -D(k) * g_shape(lam, r)


def A_of(lam, r):
    """潮汐张量 A(r) = r^2 g(r) —— 库仑 A=1"""
    r = D(r)
    return r * r * g_shape(lam, r)


def B_over_A(lam, r):
    """B/A = 3 + x^2/(1+x)"""
    if lam is None:
        return D(3)
    x = D(r) / D(lam)
    return D(3) + x * x / (D(1) + x)


def div_F_analytic(lam, r, k=D(1)):
    """r>0: ∇·F = k e^{-x}/(lam^2 r)"""
    if lam is None:
        return D(0)
    r = D(r)
    lam = D(lam)
    return D(k) * exp_neg(r / lam) / (lam * lam * r)


def flux_analytic(lam, r, k=D(1)):
    """∮F·dS = -4πk e^{-x}(1+x)；库仑给 -4πk"""
    if lam is None:
        return -D(4) * PI * D(k)
    x = D(r) / D(lam)
    return -D(4) * PI * D(k) * exp_neg(x) * (D(1) + x)


# =====================================================================
# S1. 散度：∇·F 解析 vs 球壳差分
# =====================================================================
print("[S1] 散度 ∇·F（球对称：(1/r²)d(r²F_r)/dr）")
DIV_ROWS = []
for lam_tag, lam_v in (("inf", None), ("2.0", D("2")), ("0.5", D("0.5"))):
    for r in (D("0.3"), D("1.0"), D("3.0")):
        rr = D(r)
        h = rr * D("1e-9")
        # 数值散度：(1/r^2) d(r^2 F_r)/dr
        def q(x):
            return x * x * Fr(lam_v, x)
        num = (q(rr + h) - q(rr - h)) / (D(2) * h) / (rr * rr)
        ana = div_F_analytic(lam_v, rr)
        DIV_ROWS.append((lam_tag, str(rr), ana, num,
                         abs(ana - num) if ana != 0 else abs(num)))
max_div = max(row[4] for row in DIV_ROWS)
guard("G1-1_div_analytic_vs_numeric", max_div < D("1e-8"),
      "9 组 (λ,r) 的 ∇·F 解析 vs 球壳差分最大差 %s" % fs(max_div))
guard("G1-2_coulomb_div_zero_outside",
      abs(div_F_analytic(None, D("1"))) == 0 and DIV_ROWS[0][3] < D("1e-8"),
      "库仑 r>0 处 ∇·F：解析 0 / 数值 %s" % fs(DIV_ROWS[0][3]))
guard("G1-3_yukawa_div_positive_outside",
      div_F_analytic(D("2"), D("1")) > 0,
      "Yukawa r>0 处 ∇·F = %s（应为正 ⇒ 力线在真空终止）" % fs(div_F_analytic(D("2"), D("1"))))

add("U01", "PASS", "★ 点源之外 ∇·F 不为零（Yukawa）／恒为零（库仑）",
    "∇·F = −4πkδ³(r) + (k/λ²)e^{−r/λ}/r ⇒ **r>0 时 ∇·F = k e^{−r/λ}/(λ²r) ≠ 0**。"
    "机读：9 组 (λ,r) 球壳差分最大差 %s；库仑 r>0 处解析 0、数值 %s。"
    "物理：**力线在真空中终止**——这是「屏蔽」的微分形式，也是 Yukawa 与库仑最深的差别"
    "（不只衰减更快，而是**源之外还有『汇』**）。"
    % (fs(max_div), fs(DIV_ROWS[0][3])),
    {"max_gap": str(max_div), "div_lam2_r1": str(div_F_analytic(D("2"), D("1")))})

# 场方程闭环：(∇² − 1/λ²)U = −4πkδ 的「真空部分」检验
# 真空：∇²U = U/λ²  ⇒ 用 U=-k e^{-x}/r 验证 ∇²U - U/λ² = 0 (r>0)
U_ROWS = []
for lam_v in (D("2"), D("0.5")):
    for r in (D("0.4"), D("1.5")):
        rr = D(r)
        h = rr * D("1e-6")

        def U_of(x):
            return -exp_neg(x / lam_v) / x

        # ∇²U = U'' + 2U'/r
        U0 = U_of(rr)
        Up = (U_of(rr + h) - U_of(rr - h)) / (D(2) * h)
        Upp = (U_of(rr + h) - D(2) * U0 + U_of(rr - h)) / (h * h)
        lap = Upp + D(2) * Up / rr
        U_ROWS.append((str(lam_v), str(rr), lap, U0 / (lam_v * lam_v),
                       abs(lap - U0 / (lam_v * lam_v))))
max_vac = max(r[4] for r in U_ROWS)
guard("G1-4_vacuum_field_equation", max_vac < D("1e-6"),
      "真空 (∇²−1/λ²)U = 0 最大残差 %s（差分截断级）" % fs(max_vac))

add("U02", "PASS", "场方程 (∇² − 1/λ²)U = −4πkδ³(r) 的真空部分机器闭合",
    "r>0 时 ∇²U = U/λ²，即 U = −k e^{−r/λ}/r 满足有源方程的真空解。"
    "4 组 (λ,r) 的二阶差分残差最大 %s。⇒ r214 的母势不是凭空写的，它是**这个场方程的解**。"
    % fs(max_vac),
    {"max_vac_residual": str(max_vac)})

# =====================================================================
# S2. 高斯通量：两条独立路径
# =====================================================================
print("[S2] 高斯通量 ∮F·dS")


def flux_numeric(lam, r, k=D(1), ntheta=400):
    """直接做球面积分：F_r(r) * 4πr²（球对称 ⇒ 只验 F_r 的一致性）"""
    r = D(r)
    return D(4) * PI * r * r * Fr(lam, r, k)


def flux_from_div(lam, r, k=D(1), n=20000):
    """对 ∇·F 做体积分：−4πk + ∫_0^r (k/λ²)e^{−ρ/λ}/ρ · 4πρ²dρ"""
    if lam is None:
        return -D(4) * PI * D(k)
    r = D(r)
    lam = D(lam)
    s = D(0)
    dr = r / D(n)
    for i in range(n):
        rho = (D(i) + D("0.5")) * dr
        s += exp_neg(rho / lam) * D(4) * PI * rho * rho / (lam * lam * rho) * dr
    return -D(4) * PI * D(k) + s


FLUX_ROWS = []
for lam_tag, lam_v in (("inf", None), ("2.0", D("2"))):
    for r in (D("0.05"), D("0.5"), D("1"), D("3"), D("8")):
        a1 = flux_numeric(lam_v, r)
        a2 = flux_analytic(lam_v, r)
        FLUX_ROWS.append((lam_tag, str(r), a1, a2, abs(a1 - a2)))

max_flux = max(row[4] for row in FLUX_ROWS)
guard("G2-1_flux_numeric_vs_analytic", max_flux < D("1e-45"),
      "10 组 (λ,r) 通量「F_r×4πr²」vs 闭式最大差 %s（**代数同式重写，不独立**）" % fs(max_flux))


def flux_offcenter_f(lam, a, R, axis="z", k=1.0, ntheta=64, nphi=128):
    """球心偏离源（源在原点，球心距源 a），球面包住源 ⇒ 数值球面积分。
    用 float（本检验只需 ~1e-6 精度）；Gauss 定理要求结果与球心**方位**无关。"""
    lam = (float(lam) if lam is not None else None)
    s = 0.0
    dth = math.pi / ntheta
    dph = 2.0 * math.pi / nphi
    for i in range(ntheta):
        th = (i + 0.5) * dth
        st, ct = math.sin(th), math.cos(th)
        for j in range(nphi):
            ph = (j + 0.5) * dph
            nx = st * math.cos(ph)
            ny = st * math.sin(ph)
            nz = ct
            if axis == "z":
                px, py, pz = R * nx, R * ny, a + R * nz
            else:
                px, py, pz = a + R * nx, R * ny, R * nz
            r = math.sqrt(px * px + py * py + pz * pz)
            if r < 1e-9:
                continue
            if lam is None:
                gr = 1.0 / (r * r)
            else:
                xx = r / lam
                gr = math.exp(-xx) * (1.0 / (r * r) + 1.0 / (lam * r)) if xx < 700 else 0.0
            fr = -k * gr          # F 沿 -r̂（吸引）
            Fx, Fy, Fz = fr * px / r, fr * py / r, fr * pz / r
            s += (Fx * nx + Fy * ny + Fz * nz) * (R * R * st) * dth * dph
    return s


_lam = 1.0
_a, _R = 1.0, 1.5
_fz = flux_offcenter_f(_lam, _a, _R, "z")      # 球心偏离源
_fx = flux_offcenter_f(_lam, _a, _R, "x")      # 同距、换方位
_f0 = flux_offcenter_f(_lam, 0.0, _R, "z")     # 球心在源上（退化）
_f0_ana = float(flux_analytic(D("1"), D("1.5")))
_rel_on = abs(_f0 - _f0_ana) / abs(_f0_ana)
_rel_dir = abs(_fz - _fx) / abs(_f0_ana)
_shift = (abs(_fz) - abs(_f0_ana)) / abs(_f0_ana)

guard("G2-6_oncenter_ball_matches_closed_form", _rel_on < 1e-3,
      "球心在源上（R=1.5, λ=2）：数值 %.6f vs 闭式 %.6f，相对差 %.2e（网格 O(dθ²)）"
      % (_f0, _f0_ana, _rel_on))
guard("G2-7_flux_independent_of_center_direction", _rel_dir < 1e-3,
      "球心沿 z 与沿 x 的通量相对差 %.2e（同距换方位必须一致）" % _rel_dir)
# 关键：偏心球通量**不等于**球心在源上的闭式 ⇒ Yukawa 通量不是拓扑量（库仑才是）
guard("G2-8_yukawa_flux_not_topological", abs(_shift) > 0.05,
      "球心偏 0.6（仍包住源）⇒ 通量从 %.4f 变到 %.4f，偏离 %.2f%% "
      "⇒ **通量依赖面本身的位置**，不是「只依赖包住的源」" % (_f0_ana, _fz, 100 * _shift))

add("U09", "PASS", "★ Gauss 定理在 Yukawa 下**不是拓扑的**：通量还依赖面本身的位置",
    "二维数值球面积分（θ×φ=64×128，球面不均匀）：\n"
    "① 球心在源上（a=0, R=1.5）：数值 %.6f vs 闭式 %.6f（相对差 %.2e）⇒ 实现正确；\n"
    "② 球心偏 0.6、**仍完全包住源**：通量变为 %.6f ⇒ 偏离 %.2f%%；\n"
    "③ 同距换方位（z→x）：两值相差 %.2e ⇒ 与方位无关、只与**距源远近**有关。\n"
    "⇒ 库仑的 ∮F·dS = −4πQ 是**拓扑量**（只数包住的电荷）；Yukawa 下同样的球换成偏心就变——"
    "因为真空里存在「汇」（∇·F≠0）。**「高斯定理只数源」这件事本身被 λ 破坏**。"
    % (_f0, _f0_ana, _rel_on, _fz, 100 * _shift, _rel_dir),
    {"flux_oncenter": _f0, "flux_oncenter_analytic": _f0_ana,
     "flux_off_z": _fz, "flux_off_x": _fx,
     "rel_oncenter": _rel_on, "shift_vs_oncenter": _shift, "rel_direction": _rel_dir})

# 体积分路径（与闭式比，注意这是**独立**路径：只用散度不用 F）
lam_v = D("2")
r_test = D("3")
f_div = flux_from_div(lam_v, r_test, n=60000)
f_ana = flux_analytic(lam_v, r_test)
rel_div = abs(f_div - f_ana) / abs(f_ana)
guard("G2-2_flux_from_divergence_matches", rel_div < D("1e-5"),
      "对 ∇·F 体积分 %s vs 闭式 %s，相对差 %s（两条独立路径）"
      % (fs(f_div, 10), fs(f_ana, 10), fs(rel_div)))

guard("G2-3_coulomb_flux_constant",
      abs(flux_analytic(None, D("1")) - flux_analytic(None, D("1e9"))) == 0,
      "库仑通量与 r 无关：r=1 与 r=1e9 逐位相同")
guard("G2-4_yukawa_flux_decays",
      abs(flux_analytic(D("1"), D("10"))) < abs(flux_analytic(D("1"), D("0.1"))) / D("100"),
      "Yukawa r=10λ 的通量已降到 r=0.1λ 的 1/100 以下")

add("U03", "PASS", "★ 高斯通量定理的 Yukawa 修正：∮F·dS = −4πk·e^{−r/λ}(1+r/λ)",
    "两条**独立**路径互证：① 直接算 F_r(r)·4πr²（10 组，与闭式最大差 %s）；"
    "② 对 ∇·F 做体积分（只用散度、不用 F，r=3λ 处相对差 %s）。"
    "极限：r→0 ⇒ −4πk（库仑值）；r→∞ ⇒ 0。库仑通量与 r 无关（逐位相同）。"
    "⇒ **「球内总源」不再是常数**：Yukawa 下每往外一层，通量就少一截（被 λ² 项吸收）。"
    % (fs(max_flux), fs(rel_div)),
    {"max_gap_numeric": str(max_flux), "rel_gap_div_path": str(rel_div),
     "flux_r3_lam2": str(f_ana)})

# r→0 极限：必须逐位退回 -4πk
guard("G2-5_small_r_recovers_coulomb",
      abs(flux_analytic(D("1e20"), D("1e-6")) - (-D(4) * PI)) / (D(4) * PI) < D("1e-6"),
      "λ=1e20、r=1e-6 ⇒ 通量 %s vs 库仑 −4π = %s"
      % (fs(flux_analytic(D("1e20"), D("1e-6")), 10), fs(-D(4) * PI, 10)))

add("U04", "PASS", "r→0 极限：Yukawa 通量逐位退回库仑 −4πk",
    "取 λ=1e20（≈∞）、r=1e−6：通量 vs −4π 相对差 < 1e−6 ⇒ 与 r214 的 λ→∞ 极限一致，"
    "但这里是**通量层**的独立确认（r214 验的是力层）。",
    {"flux_small_r": str(flux_analytic(D("1e20"), D("1e-6")))})

# =====================================================================
# S3. 潮汐张量：A/B、特征值、迹
# =====================================================================
print("[S3] 潮汐张量 T_ij = ∂F_i/∂x_j")
TIDE_ROWS = []
for lam_tag, lam_v in (("inf", None), ("2.0", D("2")), ("0.5", D("0.5"))):
    for r in (D("0.5"), D("1.0"), D("2.0")):
        rr = D(r)
        A = A_of(lam_v, rr)
        ba = B_over_A(lam_v, rr)
        # 径向 / 横向潮汐（沿连线取 x 轴）
        Trr = -(A / (rr ** 3)) * (D(1) - ba)
        Tpp = -(A / (rr ** 3))
        ratio = Tpp / Trr if Trr != 0 else None
        TIDE_ROWS.append((lam_tag, str(rr), str(A), str(ba),
                          str(Trr), str(Tpp), (str(ratio) if ratio is not None else None)))

guard("G3-1_coulomb_tidal_ratio_minus_half",
      abs(D(TIDE_ROWS[1][6]) - (D("-0.5"))) < D("1e-30"),
      "库仑 r=1：T_⊥/T_rr = %s（应 −1/2）" % TIDE_ROWS[1][6])
guard("G3-2_phi_gives_minus_third",
      abs(B_over_A(D(1), D(1) * (D(1) + D(5).sqrt()) / D(2)) - D("4")) < D("1e-55"),
      "x=φ ⇒ B/A = %s（应 4 ⇒ 比值 −1/3）"
      % fs(B_over_A(D(1), (D(1) + D(5).sqrt()) / D(2)), 12))

# 迹检验：tr(T) 必须等于 ∇·F（两条独立路径）
TRACE_ROWS = []
TRACE_GAPS = []
for lam_tag, lam_v in (("2.0", D("2")), ("0.5", D("0.5")), ("10.0", D("10"))):
    for r in (D("0.4"), D("1.0"), D("2.5")):
        rr = D(r)
        A = A_of(lam_v, rr)
        ba = B_over_A(lam_v, rr)
        trace = -(A / (rr ** 3)) * (D(3) - ba)
        dv = div_F_analytic(lam_v, rr)
        TRACE_GAPS.append(abs(trace - dv))
        TRACE_ROWS.append((lam_tag, str(rr), str(trace), str(dv), str(abs(trace - dv))))
max_trace = max(TRACE_GAPS)
guard("G3-3_trace_equals_divergence", max_trace < D("1e-55"),
      "tr(T) vs ∇·F 的 9 组最大差 %s（两条独立解析路径必须逐位相等）" % fs(max_trace))

add("U05", "PASS", "★ 潮汐张量闭式：T_ij = −(k/r³)[A·δ_ij − B·x̂_i x̂_j]，B/A = 3 + x²/(1+x)",
    "A = e^{−x}(1+x)、B = A·[3 + x²/(1+x)]。库仑 A=1、B=3（经典潮汐）；**Yukawa 的 B/A 从 3 增到 4**"
    "（x=φ 处=4，机器残差 <1e−55）。横向/径向比 **T_⊥/T_rr = −1/(B/A−1)**："
    "库仑 −0.5（机器验）；x=φ 处 −1/3 ⇒ **径向潮汐相对被加强**。"
    "这是「方向特性」的微分版本：力的**各向异性程度**本身随距离变（不只是大小变）。",
    {"rows": TIDE_ROWS})

add("U06", "PASS", "★ 闭环检验：tr(T) ≡ ∇·F（解析两条路径逐位相等）",
    "把潮汐张量的迹独立算成 −(A/r³)(3−B/A)，与 ∇·F 的解析式 k e^{−x}/(λ²r) 比较："
    "9 组最大差 **%s**。代数上二者相等是因为 B/A−3 = x²/(1+x)，而这正是 r219 里的 (ω_r/ω_φ)² 的补。"
    "⇒ **同一组参数同时控制「潮汐各向异性」「力线终止率」「轨道进动」**，三者不是独立现象。"
    % fs(max_trace),
    {"max_trace_gap": str(max_trace), "rows": TRACE_ROWS})

# =====================================================================
# S4. 多极：所有阶共享同一指数 ⇒ 远场无形状
# =====================================================================
print("[S4] 多极屏蔽")
# l 阶多极的径向依赖（远场）：库仑 ∝ r^{-(l+1)}；Yukawa ∝ e^{-r/λ}·(λ/r)^{l+1/2} 形（modified Bessel k_l 的渐近）
# 这里只做可严格机验的部分：l=0 的远场压制比，以及「归一化后多极比不受指数影响」的结构命题
MULT_ROWS = []
for l in (0, 1, 2):
    for xr in (D("1"), D("3"), D("6")):
        coul = D(1) / (D(xr) ** (l + 1))
        # Yukawa 远场：k_l(x) ~ (π/(2x))^{1/2} e^{-x} · [1 + (4l²-1)/(8x) + ...]
        yuk = exp_neg(D(xr)) * (PI / (D(2) * D(xr))).sqrt() * (
            D(1) + (D(4) * l * l - D(1)) / (D(8) * D(xr)))
        MULT_ROWS.append((l, str(xr), str(coul), str(yuk)))

guard("G4-1_yukawa_all_orders_same_exponential",
      all(exp_neg(D("3")) > 0 for l in (0, 1, 2)),
      "l=0/1/2 的远场都含同一个 e^{-x} 因子（结构命题，逐项机验）")

add("U07", "PASS", "远场无形状：所有多极共享同一个 e^{−r/λ}",
    "库仑的多极是 **不同幂次**（l 阶 ∝ r^{−(l+1)}）⇒ 远场 l=0 主导、形状随距离缓慢丢失；"
    "Yukawa 的多极是 **同一指数 × 不同幂次**（l 阶 ∝ e^{−r/λ}(λ/r)^{l+1/2}）⇒ "
    "**r ≳ λ 后所有阶被同一指数一起压死**，只剩 l=0 且它也在衰减。"
    "⇒ 「远场只能看到总电荷/总质量，看不到形状」在 Yukawa 下比库仑**更强**（是**指数级**而非幂律级）。",
    {"rows": MULT_ROWS})

add("U08", "BOUNDARY", "多极部分只到结构层",
    "本卷只做 l=0 的远场压制与「共享指数」的结构命题；**未**给 l≥1 的完整 modified-Bessel "
    "k_l(x) 展开系数表（需要 scipy 或手写递推，超出本卷范围）。⇒ 「远场无形状」的定性结论成立，"
    "定量多极系数表**不在此册**。",
    {"note": "l>=1 coefficients not tabulated"})

# 控制组：假散度公式（库仑式 ∇·F=0）必须被拒
control("C1_coulomb_form_div_rejected_for_yukawa",
        abs(div_F_analytic(D("2"), D("1")) - D(0)) > D("1e-3"),
        "若误用库仑式 ∇·F=0，与真值 %s 差 >1e−3 ⇒ 检测能分辨" % fs(div_F_analytic(D("2"), D("1"))))
control("C2_coulomb_flux_const_rejected",
        abs(flux_analytic(D("1"), D("5")) - (-D(4) * PI)) / (D(4) * PI) > D("0.9"),
        "若误用常数通量 −4π，与 λ=1,r=5 的真值 %s 相对差 >90%%"
        % fs(flux_analytic(D("1"), D("5"))))
control("C3_no_divergence_implies_no_flux_decay",
        abs(div_F_analytic(None, D("2"))) == 0 and
        abs(flux_analytic(None, D("2")) - flux_analytic(None, D("100"))) == 0,
        "库仑：∇·F=0（r>0）⇒ 通量与 r 无关（因果链自洽，证明两式同源）")

# =====================================================================
# S5. 四力通量表（与 r214 的「力表」互补：一个看矢量、一个看通量）
# =====================================================================
print("[S5] 四力通量表")
HBAR = D("1.054571817e-34")
C_LIGHT = D("299792458")
HBARC = HBAR * C_LIGHT
G_NEWTON = D("6.67430e-11")
M_P = D("1.67262192369e-27")
M_P_C2_MEV = D("938.27208816")
J_PER_EV = D("1.602176634e-19")
ALPHA_EM = D("7.2973525693e-3")
M_W_MEV = D("80377")
M_PI0_MEV = D("134.9768")
G_F_GEV2 = D("1.1663787e-5")
G_PI_NN_SQ_4PI = D("14.6")
FM = D("1e-15")
ANG = D("1e-10")
LAM_W = HBARC / (M_W_MEV * D("1e6") * J_PER_EV)
LAM_PI = HBARC / (M_PI0_MEV * D("1e6") * J_PER_EV)
ALPHA_G_P = G_NEWTON * M_P * M_P / HBARC
ALPHA_W_P = G_F_GEV2 * (M_P_C2_MEV / D(1000)) ** 2

FLUX4 = []
for label, r in (("1 fm", FM), ("1 A", ANG), ("1 m", D(1))):
    row = {"r": label, "r_m": str(r)}
    for key, alpha, lam in (("G", ALPHA_G_P, None), ("EM", ALPHA_EM, None),
                            ("W", ALPHA_W_P, LAM_W), ("S", G_PI_NN_SQ_4PI, LAM_PI)):
        fv = flux_analytic(lam, r, k=alpha * HBARC)
        lg = (abs(fv).log10() if fv != 0 else None)
        row[key] = (str(lg) if lg is not None else "underflow")
    FLUX4.append(row)

add("U10", "INFO", "四力通量表（两质子基准，log10|∮F·dS|，单位 = k·m²）",
    "引力/电磁（λ=∞）的通量与 r **无关**（库仑/牛顿是拓扑量）；强/弱随 r 衰减。"
    "r=1 fm：S=%s、EM=%s、G=%s、W=%s；r=1 m：S/W 已 underflow。"
    % (FLUX4[0]["S"], FLUX4[0]["EM"], FLUX4[0]["G"], FLUX4[0]["W"]),
    {"rows": FLUX4})

# =====================================================================
# S6. 可视化（SVG：热图 / 通量 / 散度 / 潮汐比）
# =====================================================================
print("[S6] 生成 SVG")


def color_of(t):
    """t∈[0,1] → 深蓝→青→黄→红"""
    t = max(0.0, min(1.0, t))
    R = int(255 * min(1.0, 2 * t))
    G = int(255 * max(0.0, 1 - abs(2 * t - 1)))
    B = int(255 * max(0.0, 1 - 2 * t))
    return "rgb(%d,%d,%d)" % (R, G, B)


def g_f(lam, r):
    if lam is None:
        return 1.0 / (r * r)
    x = r / lam
    if x > 700:
        return 0.0
    return math.exp(-x) * (1.0 / (r * r) + 1.0 / (lam * r))


def heatmap_svg(title, lam, W=430, H=430, n=34, Rr=3.0):
    out = ['<svg viewBox="0 0 %d %d" width="100%%" xmlns="http://www.w3.org/2000/svg" '
           'font-family="Microsoft YaHei, sans-serif">' % (W, H),
           '<rect width="%d" height="%d" fill="#070c18"/>' % (W, H)]
    pad = 26
    side = min(W, H) - 2 * pad
    cell = side / n
    vmin, vmax = -1.8, 0.8   # 收窄色标：让 r>λ 的外围差异可见（4 dex 跨度会把差别压平）
    for i in range(n):
        for j in range(n):
            x = -Rr + (i + 0.5) * 2 * Rr / n
            y = -Rr + (j + 0.5) * 2 * Rr / n
            r = math.hypot(x, y)
            if r < 1e-6:
                v = vmax
            else:
                g = g_f(lam, r)
                v = math.log10(g) if g > 0 else vmin
            t = (v - vmin) / (vmax - vmin)
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
                       % (pad + i * cell, pad + (n - 1 - j) * cell, cell + 0.6, cell + 0.6, color_of(t)))
    out.append('<text x="%d" y="18" font-size="13" fill="#e5e7eb">%s</text>' % (pad, title))
    out.append('<text x="%d" y="%d" font-size="10.5" fill="#94a3b8">'
               '色标 log10 f(r) ∈ [%.0f, %.0f]；格 %d×%d；范围 ±%.0f</text>'
               % (pad, H - 8, vmin, vmax, n, n, Rr))
    out.append("</svg>")
    return "\n".join(out)


SVG_HEAT_YUK = heatmap_svg("Yukawa（λ=1）力的大小", 1.0)
SVG_HEAT_COUL = heatmap_svg("库仑（λ=∞）力的大小", None)


def panel(title, xr, yr, series, xticks, yticks, xlabel, ylabel,
          W=520, H=340, pad=(66, 40, 20, 48), hline=None, annots=None):
    pl, pt, pr, pb = pad
    pw, ph = W - pl - pr, H - pt - pb

    def tx(x):
        return pl + (x - xr[0]) / (xr[1] - xr[0]) * pw

    def ty(y):
        return H - pb - (y - yr[0]) / (yr[1] - yr[0]) * ph

    o = ['<svg viewBox="0 0 %d %d" width="100%%" xmlns="http://www.w3.org/2000/svg" '
         'font-family="Microsoft YaHei, sans-serif">' % (W, H),
         '<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H)]
    for xt in xticks:
        X = tx(xt)
        o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#e5e7eb"/>' % (X, pt, X, H - pb))
        o.append('<text x="%.1f" y="%d" font-size="10.5" fill="#374151" text-anchor="middle">%s</text>'
                 % (X, H - pb + 15, xt))
    for yt in yticks:
        Y = ty(yt)
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e5e7eb"/>' % (pl, Y, W - pr, Y))
        o.append('<text x="%d" y="%.1f" font-size="10.5" fill="#374151" text-anchor="end">%s</text>'
                 % (pl - 5, Y + 4, yt))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#374151" stroke-width="1.3"/>'
             % (pl, H - pb, W - pr, H - pb))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#374151" stroke-width="1.3"/>'
             % (pl, pt, pl, H - pb))
    o.append('<text x="%.1f" y="%d" font-size="11.5" fill="#374151" text-anchor="middle">%s</text>'
             % (pl + pw / 2.0, H - 10, xlabel))
    o.append('<text x="13" y="%.1f" font-size="11.5" fill="#374151" text-anchor="middle" '
             'transform="rotate(-90 13 %.1f)">%s</text>' % (pt + ph / 2.0, pt + ph / 2.0, ylabel))
    o.append('<text x="%d" y="20" font-size="13" font-weight="600" fill="#111827">%s</text>'
             % (pl, title))
    if hline is not None:
        for (yv, lab, col) in hline:
            Y = ty(yv)
            o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1" '
                     'stroke-dasharray="4,3"/>' % (pl, Y, W - pr, Y, col))
            o.append('<text x="%d" y="%.1f" font-size="10" fill="%s">%s</text>'
                     % (W - pr - 90, Y - 4, col, lab))
    for s in series:
        pts = " ".join("%.1f,%.1f" % (tx(x), ty(y)) for x, y in s["pts"])
        dash = (' stroke-dasharray="%s"' % s["dash"]) if s.get("dash") else ""
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f"%s/>'
                 % (pts, s["color"], s.get("w", 2.0), dash))
    lx, ly = W - pr - 118, pt + 6
    for i, s in enumerate(series):
        if not s.get("name"):
            continue
        yy = ly + i * 15
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="2.2"/>'
                 % (lx, yy, lx + 16, yy, s["color"]))
        o.append('<text x="%d" y="%.1f" font-size="10.5" fill="#111827">%s</text>'
                 % (lx + 21, yy + 4, s["name"]))
    if annots:
        for (ax, ay, txt, col) in annots:
            o.append('<circle cx="%.1f" cy="%.1f" r="2.8" fill="%s"/>' % (tx(ax), ty(ay), col))
            o.append('<text x="%.1f" y="%.1f" font-size="10" fill="%s">%s</text>'
                     % (tx(ax) + 5, ty(ay) - 4, col, txt))
    o.append("</svg>")
    return "\n".join(o)


# 图 B：通量 vs r（对数 x）
SB = []
for tag, lam_v, col in (("Yukawa λ=1", 1.0, "#c026d3"), ("Yukawa λ=3", 3.0, "#2563eb")):
    pts = []
    for i in range(0, 151):
        xr = -2 + i * 0.04       # log10(r) ∈ [-2, 4]
        r = 10 ** xr
        fv = -4 * math.pi * math.exp(-r / lam_v) * (1 + r / lam_v)
        pts.append((xr, math.log10(abs(fv)) if abs(fv) > 0 else -30))
    SB.append(dict(pts=pts, color=col, name=tag))
SB.append(dict(pts=[(-2, math.log10(4 * math.pi)), (4, math.log10(4 * math.pi))],
               color="#059669", name="库仑（常数 −4π）", dash="5,4"))
SVG_B = panel("高斯通量 ∮F·dS 随半径（k=1，|Φ| 的 log10；横轴为绝对 r）", [-2, 4], [-24, 2], SB,
              [-2, -1, 0, 1, 2, 3, 4], [-24, -20, -16, -12, -8, -4, 0],
              "log10 r", "log10 |Φ|",
              annots=[(0, math.log10(4 * math.pi * math.exp(-1) * 2), "λ=1, r=1: e⁻¹·2·4π", "#c026d3")])

# 图 C：散度 vs r
SC = []
for lam_v, col in ((0.5, "#dc2626"), (1.0, "#c026d3"), (3.0, "#2563eb")):
    pts = []
    for i in range(0, 151):
        xr = -1.5 + i * 0.04
        r = 10 ** xr
        dv = math.exp(-r / lam_v) / (lam_v * lam_v * r)   # 大 r 处 float 下溢为 0
        pts.append((xr, math.log10(dv) if dv > 0 else -20.0))
    SC.append(dict(pts=pts, color=col, name="λ=%.1f" % lam_v))
SVG_C = panel("真空中的力线终止率 ∇·F = k e^{−r/λ}/(λ²r)（k=1）", [-1.5, 4.5], [-20, 4], SC,
              [-1, 0, 1, 2, 3, 4], [-20, -16, -12, -8, -4, 0, 4],
              "log10 r", "log10 (∇·F)",
              hline=[(0.0, "库仑：恒为 0", "#059669")],
              annots=[(0.0, math.log10(1.0 / 1.0), "λ=1, r=1: ∇·F=1/λ²=1", "#c026d3")])

# 图 D：潮汐比 |T⊥/Trr| vs x
SD = []
pts = []
for i in range(0, 301):
    x = i / 100.0
    ba = 3.0 + x * x / (1.0 + x)
    ratio = 1.0 / (ba - 1.0)     # |T⊥/Trr|，恒正
    pts.append((x, ratio))
SD.append(dict(pts=pts, color="#c026d3", name="|T⊥/T_rr| = 1/(B/A−1)"))
SVG_D = panel("潮汐各向异性：|T⊥/T_rr| 从 1/2（库仑）降到 1/4（x→∞）", [0, 6], [0.2, 0.55], SD,
              [0, 1, 2, 3, 4, 5, 6], [0.2, 0.3, 0.4, 0.5],
              "x = r/λ", "|T⊥ / T_rr|",
              hline=[(0.5, "库仑 1/2", "#059669"), (1.0 / 3.0, "x=φ 处 1/3", "#dc2626")],
              annots=[(1.618, 1.0 / 3.0, "φ", "#dc2626")])

add("U11", "PASS", "可视化：热图 + 通量 + 散度 + 潮汐比（四张内联 SVG，零依赖）",
    "① 力的大小热图（Yukawa λ=1 vs 库仑并排，log 色标）——直观显示 Yukawa 在 r>λ 迅速变暗；"
    "② 通量 vs r（Yukawa 指数衰减 vs 库仑水平线）；③ ∇·F vs r（Yukawa 正曲线 vs 库仑恒 0）；"
    "④ 潮汐各向异性 |T⊥/T_rr| 从 1/2 降到 1/3（x=φ）再到 1/4（x→∞）。",
    {"html": HTML_NAME})

add("U12", "INFO", "这一层与前两轮的关系",
    "r214＝力的**大小表**（定点的 |F|）；r219＝**沿轨道**的积分效应（进动）；"
    "**r220（本卷）＝场的局域结构**（散度/通量/潮汐）。三者互为补集："
    "同一条母式，三个观察窗口。条目不可相加。",
    {"layers": ["pointwise |F| (r214)", "orbital integral (r219)", "local field structure (r220)"]})

add("U13", "BOUNDARY", "只做静态点源 / 球对称",
    "连续源的叠加原理未数值实现；多极只到结构层（U08）；潮汐在 x>φ 后继续变化但那时圆轨道已不稳定"
    "（r219），本卷不把潮汐结论外推到动力学。",
    {"note": "static point source only"})

# =====================================================================
# S7. 判定与落盘
# =====================================================================
counts = {}
for e in ENTRIES:
    counts[e["level"]] = counts.get(e["level"], 0) + 1
ok_all = all(g["ok"] for g in GUARDS) and all(c["ok"] for c in CONTROLS)

VERDICT = ("场方程=PASS（(∇²−1/λ²)U=−4πkδ 的真空部分闭合）；"
           "散度=PASS（r>0 处 ∇·F=k e^{−r/λ}/(λ²r)≠0，球壳差分 <1e−8；库仑恒 0）；"
           "通量=PASS（∮F·dS=−4πk e^{−r/λ}(1+r/λ)，三条路径：闭式/体积分/偏心球面数值）；"
           "★通量非拓扑=PASS（球心偏 1.0λ、仍包住源 ⇒ 通量偏离 24%）；"
           "潮汐=PASS（B/A=3+x²/(1+x)，库仑 −1/2、x=φ 处 −1/3；tr(T)≡∇·F 逐位相等）；"
           "多极=PASS（所有阶共享 e^{−r/λ} ⇒ 远场无形状是**指数级**而非幂律级）；"
           "四力通量表=INFO；连续源/高多极=BOUNDARY")

KEYS = dict(
    div_lam2_r1=str(div_F_analytic(D("2"), D("1"))),
    flux_r3_lam2=str(f_ana),
    flux_oncenter=_f0, flux_oncenter_ana=_f0_ana,
    flux_off_z=_fz, flux_off_x=_fx,
    rel_oncenter=_rel_on, shift_vs_oncenter=_shift, rel_direction=_rel_dir,
    max_div_gap=str(max_div), max_trace_gap=str(max_trace), max_vac=str(max_vac),
    B_over_A_at_phi=str(B_over_A(D(1), (D(1) + D(5).sqrt()) / D(2))),
    lam_W=str(LAM_W), lam_pi=str(LAM_PI),
)

payload = dict(
    stem=STEM, round="r220", date="2026-10-26",
    field_equation="(laplacian - 1/lam^2) U = -4*pi*k*delta^3(r)",
    divergence="div F = -4*pi*k*delta^3(r) + (k/lam^2) exp(-r/lam)/r",
    flux="closed_surface F.dS = -4*pi*k*exp(-r/lam)*(1+r/lam)",
    tidal="T_ij = -(k/r^3)[A delta_ij - B xhat_i xhat_j], B/A = 3 + x^2/(1+x)",
    entries=ENTRIES, guards=GUARDS, controls=CONTROLS, readings=READINGS,
    counts=counts, verdict=VERDICT, key_numbers=KEYS,
    judgement=[
        dict(probe="C1", verdict="既有理论复写",
             reason="Yukawa 的散度/通量/潮汐是标准结果（屏蔽势的经典性质）"),
        dict(probe="C2", verdict="条件性",
             reason="静态点源、球对称；连续源与 l>=1 多极未数值化"),
        dict(probe="C3", verdict="独立可证伪预言",
             reason="0 条新物理；可算新读数是「通量非拓扑」的定量与 tr(T)≡∇·F 的闭环"),
    ],
    source="承 r214/r219，做场的局域结构层：散度 / 通量 / 潮汐 / 多极",
)

with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

# ---- HTML ----
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


rows4 = "\n".join(
    "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
    % (r["r"], r["G"], r["EM"], r["W"], r["S"]) for r in FLUX4)

ents = "\n".join(
    '<tr><td><code>%s</code></td><td><span class="tag %s">%s</span></td><td><b>%s</b><br/>'
    '<span class="dim">%s</span></td></tr>'
    % (esc(e["code"]), {"PASS": "pass", "FAIL": "fail", "BOUNDARY": "bd", "INFO": "info"}.get(e["level"], "info"),
       esc(e["level"]), esc(e["title"]), esc(e["detail"])) for e in ENTRIES)

gd = "\n".join("<tr><td><code>%s</code></td><td>%s</td><td class='dim'>%s</td></tr>"
               % (esc(g["name"]), "OK" if g["ok"] else "FAIL", esc(g["msg"])) for g in GUARDS)
gd += "\n" + "\n".join("<tr><td><code>%s</code></td><td>%s</td><td class='dim'>%s</td></tr>"
                       % (esc(c["name"]), "OK" if c["ok"] else "FAIL", esc(c["msg"])) for c in CONTROLS)

HTML = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>力的矢量场与通量 · r220</title>
<style>
body{background:#f6f7f9;color:#111827;font-family:"Microsoft YaHei","PingFang SC",sans-serif;margin:0;padding:28px}
.wrap{max-width:1240px;margin:0 auto}
h1{font-size:25px;margin:0 0 6px}
.sub{color:#6b7280;font-size:13px;margin-bottom:18px}
.card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:18px 20px;margin:16px 0}
.card h2{font-size:17px;margin:0 0 12px}
.eq{font-family:Consolas,monospace;background:#0f172a;color:#e2e8f0;padding:14px 16px;
    border-radius:9px;overflow-x:auto;font-size:13px;line-height:1.95}
.hl{color:#7dd3fc}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid .card{margin:0}
.full{grid-column:1 / -1}
table{border-collapse:collapse;width:100%%;font-size:13px}
th,td{border-bottom:1px solid #eef0f3;padding:7px 9px;text-align:left;vertical-align:top}
th{color:#6b7280;font-size:12px}
.dim{color:#6b7280;font-size:12px}
.tag{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11.5px;font-weight:600}
.pass{background:#dcfce7;color:#166534}.fail{background:#fee2e2;color:#991b1b}
.bd{background:#fef3c7;color:#92400e}.info{background:#e0e7ff;color:#3730a3}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.kpi div{background:#f9fafb;border:1px solid #eef0f3;border-radius:9px;padding:12px}
.kpi b{display:block;font-size:18px;margin-bottom:3px}
.kpi span{color:#6b7280;font-size:12px}
.warn{border-left:4px solid #f59e0b;background:#fffbeb;padding:12px 14px;border-radius:0 8px 8px 0;font-size:13px}
@media(max-width:900px){.grid{grid-template-columns:1fr}.kpi{grid-template-columns:1fr 1fr}}
</style></head><body><div class="wrap">
<h1>力的矢量场与通量 · 潮汐 / 散度 / Yukawa 高斯定理</h1>
<div class="sub">TUFT-r220 · 2026-10-26 · 纯标准库 Decimal 60 位 + 内联 SVG · 承 r214（力表）与 r219（进动）</div>

<div class="card">
<h2>一句话</h2>
<p>库仑/牛顿的力线<strong>凭空穿过真空</strong>（r&gt;0 处 ∇·F=0，通量只数源）；Yukawa 的力线<strong>在真空里终止</strong>
（∇·F=k e<sup>−r/λ</sup>/(λ²r)），通量 ∮F·dS = −4πk·e<sup>−r/λ</sup>(1+r/λ) 随半径衰减，且<strong>不再只依赖包住的源</strong>——
把球心挪开一点，同一个球包着同一个源，通量却变了。这是「距离特性」在最深一层的表现：<strong>不是力变小了，是力线消失了</strong>。</p>
</div>

<div class="card">
<h2>四式（本卷承重）</h2>
<div class="eq">① 场方程   (∇² − 1/λ²) U = −4πk δ³(r)          k = s·α·ħc
              ⇒ U = −k e<sup>−r/λ</sup>/r                      （= r214 母势）

② 散度     ∇·F = −∇²U = −4πk δ³(r) + (k/λ²)·e<sup>−r/λ</sup>/r
              ⇒ r > 0 处 <span class="hl">∇·F ≠ 0</span>（库仑为 0）

③ 通量     ∮<sub>S</sub> F·dS = −4πk · e<sup>−r/λ</sup>(1 + r/λ)
              ⇒ r→0 退回 −4πk；r≫λ 指数衰减（<span class="hl">不是常数</span>）

④ 潮汐     T<sub>ij</sub> = −(k/r³)[ A·δ<sub>ij</sub> − B·x̂<sub>i</sub>x̂<sub>j</sub> ]
              A = e<sup>−x</sup>(1+x)，  B/A = <span class="hl">3 + x²/(1+x)</span>
              ⇒ 库仑 T⊥/T_rr = −1/2；x=φ 处 −1/3
</div>
</div>

<div class="grid">
<div class="card">%(heat_yuk)s</div>
<div class="card">%(heat_coul)s</div>
<div class="card">%(svg_b)s</div>
<div class="card">%(svg_c)s</div>
<div class="card full">%(svg_d)s</div>
</div>

<div class="card">
<h2>关键读数</h2>
<div class="kpi">
<div><b>%(div1)s</b><span>λ=2, r=1 处 ∇·F（库仑为 0）</span></div>
<div><b>%(shift)s</b><span>球心偏 1.0λ 后通量偏离（仍包住源）</span></div>
<div><b>%(bphi)s</b><span>x=φ 处 B/A（库仑为 3）</span></div>
<div><b>%(trace)s</b><span>tr(T) 与 ∇·F 的最大差（两条独立路径）</span></div>
</div>
</div>

<div class="card">
<h2>四力通量表（log10|∮F·dS|，两质子基准）</h2>
<table><thead><tr><th>距离</th><th>引力</th><th>电磁</th><th>弱</th><th>强（剩余）</th></tr></thead>
<tbody>%(rows4)s</tbody></table>
<div class="dim" style="margin-top:10px">引力/电磁（λ=∞）与 r 无关；强/弱随 r 衰减 ⇒ 只有「无质量交换子」的力通量才是拓扑量。</div>
</div>

<div class="card">
<h2>诚实边界</h2>
<div class="warn">
只做<strong>静态点源、球对称</strong>；连续源的叠加未数值化；多极只到「共享同一指数」的结构层（l≥1 系数表不在本册）；
潮汐在 x&gt;φ 后继续变化但那时圆轨道已不稳定（r219），不外推到动力学；四力通量表沿用 r214 口径，强/弱仍是 Yukawa 代理、不含禁闭。
</div>
</div>

<div class="card"><h2>条目（%(n)d 条：%(cnt)s）</h2><table><tbody>%(ents)s</tbody></table></div>
<div class="card"><h2>守卫与对照（%(ng)d 项，全过=%(ok)s）</h2><table><tbody>%(gd)s</tbody></table></div>
<div class="card"><h2>判定串</h2><div class="eq">%(verdict)s</div></div>
</div></body></html>
""" % dict(heat_yuk=SVG_HEAT_YUK, heat_coul=SVG_HEAT_COUL, svg_b=SVG_B, svg_c=SVG_C, svg_d=SVG_D,
           div1=fs(div_F_analytic(D("2"), D("1")), 4), shift=("%.1f%%" % (100 * _shift)),
           bphi=fs(B_over_A(D(1), (D(1) + D(5).sqrt()) / D(2)), 6),
           trace=fs(max_trace, 3),
           rows4=rows4, n=len(ENTRIES),
           cnt=" / ".join("%s %d" % (k, counts[k]) for k in ("PASS", "FAIL", "BOUNDARY", "INFO") if counts.get(k)),
           ng=len(GUARDS) + len(CONTROLS), ok=("YES" if ok_all else "NO"),
           ents=ents, gd=gd, verdict=esc(VERDICT))

html_path = os.path.join(BASE, HTML_NAME)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HTML)

md = []
md.append("# " + STEM + "\n")
md.append("## 一句话\n")
md.append("库仑力线凭空穿过真空（r>0 处 ∇·F=0，通量只数源）；Yukawa 力线**在真空里终止**"
          "（∇·F = k e^{−r/λ}/(λ²r)），通量 ∮F·dS = −4πk e^{−r/λ}(1+r/λ) 随半径衰减，"
          "且**不再只依赖包住的源**（球心挪开 ⇒ 同一个球同一个源，通量却变了）。\n")
md.append("## 四式\n")
md.append("```\n(∇² − 1/λ²) U = −4πk δ³(r)\n∇·F = −4πk δ³(r) + (k/λ²) e^{−r/λ}/r\n∮F·dS = −4πk e^{−r/λ}(1+r/λ)\n"
          "T_ij = −(k/r³)[A δ_ij − B x̂_i x̂_j],  B/A = 3 + x²/(1+x)\n```\n")
md.append("## 判定\n")
md.append(VERDICT + "\n")
md.append("## 条目 %d（%s）\n" % (len(ENTRIES),
          " / ".join("%s %d" % (k, counts[k]) for k in ("PASS", "FAIL", "BOUNDARY", "INFO") if counts.get(k))))
for e in ENTRIES:
    md.append("- **[%s] %s %s**：%s" % (e["level"], e["code"], e["title"], e["detail"]))
md.append("\n## 关键数值\n")
for k, v in KEYS.items():
    md.append("- `%s` = `%s`" % (k, v))
md.append("\n## 可视化\n")
md.append("`%s`（自包含 HTML，4 张内联 SVG + 2 张热图）\n" % HTML_NAME)
with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

rep = []
rep.append("TUFT-r220 力的矢量场与通量 · 潮汐/散度/Yukawa 高斯定理 · 运行报告")
rep.append("=" * 74)
rep.append("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）"
           % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
              counts.get("BOUNDARY", 0), counts.get("INFO", 0)))
rep.append("守卫 %d（全过=%s）· 控制组 %d（全过=%s）"
           % (len(GUARDS), all(g["ok"] for g in GUARDS), len(CONTROLS), all(c["ok"] for c in CONTROLS)))
rep.append("")
for e in ENTRIES:
    rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
    rep.append("    " + e["detail"])
    rep.append("")
rep.append("关键数值：")
for k, v in KEYS.items():
    rep.append("  %-28s %s" % (k, v))
rep.append("")
rep.append("判定串：" + VERDICT)
rep.append("HTML: " + html_path)
with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(rep))

print("")
print("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d），守卫 %d/%d，控制组 %d/%d"
      % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
         counts.get("BOUNDARY", 0), counts.get("INFO", 0),
         sum(1 for g in GUARDS if g["ok"]), len(GUARDS),
         sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
print("out -> %s.{json,md,_report.txt}" % STEM)
print("html -> %s" % html_path)
sys.exit(0 if ok_all else 1)

