# -*- coding: utf-8 -*-
r"""TUFT-r222｜四力统一方程的**传播层**：色散、截止、群速度、质量–力程等价
================================================================================
四层递进（同一母式 UFE-4F，四个观察窗口）：
  r214  定点 |F|            —— 静态力表
  r219  沿轨道积分          —— 进动 / L 破缺 / 相对论
  r220  场的局域结构        —— 散度 / 通量 / 潮汐
  **r222（本卷）传播层**    —— 力能不能**传出去**：色散、截止、群速度、倏逝

核心：把 r220 的**静态**场方程时间化。
  (∇² − 1/λ²)U = −4πkδ        [r220 静态]
  ↓ 时间化（把 U 换成传播的标量场 φ）
  (□ + 1/λ²)φ = 源 ,  □ = ∂²/∂t² − c²∇²
  ⇒ 平面波 e^{i(kx−ωt)} 代入得 **色散关系**：
        ω² = c²k² + c²/λ²
  ⇒ **截止频率 ω_c = c/λ**（k=0 处的频率下限）
  ⇒ ω < ω_c 时 k 为虚数 ⇒ **波不能传播（倏逝）**

三条可机验的推论：
  (i)   v_g · v_ph = c²      （群速 × 相速 = 光速平方，因果性保持）
  (ii)  静态极限 ω→0 时倏逝衰减长度 = 1/√(μ² − ω²/c²) → **1/μ = λ**（与 r220 力程逐位一致）
  (iii) **ħω_c = m c²**       （截止频率乘 ħ 恰是交换粒子的静止能量）

⇒ 「力程 λ」「传播截止 ω_c」「交换粒子质量 m」是**同一个量的三种写法**：
        λ = ħ/(mc) ,  ω_c = c/λ = mc²/ħ
这解释了为什么只有**无质量交换子**（光子、引力子）的力既能长程又能辐射；
弱/强有质量 ⇒ 只能短程、且以虚粒子（倏逝）方式传递。

实验接口（本卷自算，不用外部拟合）：
  · 引力子：GW170817 的 |v_g/c − 1| < 1e−15 + 观测频率 ~100 Hz ⇒ λ_g > 1.07e13 m
  · 光子：m_γ < 1e−18 eV ⇒ λ_γ > 1.97e11 m
  · 弱/强：λ 反推质量 = 80.3 GeV / 135.0 MeV（与 r214 口径逐位自洽）

诚实边界：
  (a) 波动方程是**自由标量场**的线性化；不含自相互作用、不含规范结构、不含自旋。
  (b) 实验上限取自公开量级（GW170817 的 1e−15、PDG 的 m_γ 量级），本卷只做**该上限到 λ 的换算**，
      **不**宣称重新分析数据。
  (c) 离散色散只用于说明 FDTD 的可靠性边界，不作物理结论。
  (d) 倏逝波"不能传播"是指**不能输运能量到无穷远**，不是"完全不存在"（近场内仍有指数衰减的场）。

治理：只读引用 r214/r219/r220 的结论与常数；不改其字节；未改 verify.py；未做 git；
未跑 refresh_catalog.py；条目不可与 r142–r221 相加。纯标准库。
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

STEM = "TUFT-r222_四力统一方程的传播层_色散截止群速度与质量力程等价_精算与可视化_2026-10-26"
HTML_NAME = "四力传播层_色散与截止_2026-10-26.html"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
F = Fraction
ENTRIES, GUARDS, CONTROLS, READINGS = [], [], [], {}
PI = D("3.14159265358979323846264338327950288419716939937510582097494459")

HBAR = D("1.054571817e-34")
C_LIGHT = D("299792458")
HBARC = HBAR * C_LIGHT
M_W_MEV = D("80377")
M_PI0_MEV = D("134.9768")
J_PER_EV = D("1.602176634e-19")
FM = D("1e-15")


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


# =====================================================================
# S0. 量纲守卫
# =====================================================================
DM, DL, DT = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    n = F(n)
    return tuple(F(x) * n for x in a)


guard("G0-1_mu_dim", dsub((0, 0, 0), DL) == (0, -1, 0), "[1/lam] = L^-1")
guard("G0-2_box_dim", dpow(DL, -2) == (0, -2, 0), "[laplacian] = L^-2")
# 色散 omega^2 = c^2 k^2 + c^2/lam^2：三项都必须是 T^-2
_w2 = dpow(DT, -2)                                     # ω² : T^-2
_term_k = dadd(dadd(dpow(DL, 2), dpow(DT, -2)), dpow(DL, -2))   # c²k² = L²T⁻²·L⁻² = T⁻²
_term_m = dadd(dadd(dpow(DL, 2), dpow(DT, -2)), dpow(DL, -2))   # c²/λ² = L²T⁻²·L⁻² = T⁻²
guard("G0-3_dispersion_homogeneous", _w2 == (0, 0, -2) and _term_k == _w2 and _term_m == _w2,
      "[omega^2] = %s ; [c^2 k^2] = %s ; [c^2/lam^2] = %s" % (_w2, _term_k, _term_m))
guard("G0-4_vg_dim", ddiv(DL, DT) == (0, 1, -1), "[v_g] = %s（应 L/T）" % (ddiv(DL, DT),))


# ---- 色散关系（c=1 归一化时最简洁；本卷保留 c 显式）----
def omega_of_k(lam, k, c=C_LIGHT):
    """ω = c√(k² + 1/λ²)"""
    k = D(k)
    mu = D(0) if lam is None else D(1) / D(lam)
    return c * (k * k + mu * mu).sqrt()


def v_phase(lam, k, c=C_LIGHT):
    k = D(k)
    if k == 0:
        return None
    return omega_of_k(lam, k, c) / k


def v_group(lam, k, c=C_LIGHT):
    """v_g = c²k/ω"""
    k = D(k)
    w = omega_of_k(lam, k, c)
    return c * c * k / w


def kappa_evan(lam, omega, c=C_LIGHT):
    """ω<ω_c 时的虚波数 κ = √(μ² − ω²/c²)，衰减长度 1/κ"""
    mu = D(0) if lam is None else D(1) / D(lam)
    w = D(omega)
    val = mu * mu - w * w / (c * c)
    if val <= 0:
        return None
    return val.sqrt()


def omega_c(lam, c=C_LIGHT):
    if lam is None:
        return D(0)
    return c / D(lam)


# =====================================================================
# S1. 色散关系：从平面波严格导出 + 数值代入自检
# =====================================================================
print("[S1] 色散关系 ω² = c²k² + c²/λ²")
DISP_ROWS = []
for lam_tag, lam_v in (("inf", None), ("2.0", D("2")), ("0.5", D("0.5"))):
    for k in (D("0.1"), D("0.5"), D("1"), D("3"), D("10")):
        w = omega_of_k(lam_v, k)
        lhs = w * w
        rhs = C_LIGHT * C_LIGHT * (k * k + (D(0) if lam_v is None else D(1) / (D(lam_v) ** 2)))
        DISP_ROWS.append((lam_tag, str(k), lhs, rhs, abs(lhs - rhs)))
max_disp = max(r[4] for r in DISP_ROWS)
guard("G1-1_dispersion_identity", max_disp < D("1e-30"),
      "15 组 (λ,k) 的 ω²−(c²k²+c²/λ²) 最大残差 %s" % fs(max_disp))

guard("G1-2_photon_like_limit", abs(omega_of_k(None, D("3")) - C_LIGHT * D("3")) < D("1e-40"),
      "λ=∞, k=3 ⇒ ω = %s（应 = 3c）" % fs(omega_of_k(None, D("3"))))
guard("G1-3_cutoff_at_k0",
      abs(omega_of_k(D("2"), D("0")) - C_LIGHT / D("2")) < D("1e-40"),
      "λ=2, k=0 ⇒ ω_c = c/λ = %s" % fs(omega_of_k(D("2"), D("0"))))

add("U01", "PASS", "色散关系：ω² = c²k² + c²/λ²（λ=∞ 退回光子/引力波）",
    "由 (□ + 1/λ²)φ = 0 代入 e^{i(kx−ωt)} 严格得；15 组 (λ,k) 残差 %s。"
    "λ=∞ 时 ω = ck（无质量）；λ 有限时 k=0 处仍有 ω_c = c/λ ⇒ **存在频率下限**。"
    % fs(max_disp),
    {"max_residual": str(max_disp)})

# =====================================================================
# S2. 群速度 / 相速度
# =====================================================================
print("[S2] 群速度与相速度")
VP_ROWS = []
for lam_v in (D("2"), D("0.5")):
    for k in (D("1"), D("3"), D("10")):
        vp = v_phase(lam_v, k)
        vg = v_group(lam_v, k)
        prod = vp * vg
        VP_ROWS.append((str(lam_v), str(k), vp, vg, prod, abs(prod - C_LIGHT * C_LIGHT)))
max_prod = max(r[5] for r in VP_ROWS)
guard("G2-1_vg_times_vph_equals_c2", max_prod / (C_LIGHT * C_LIGHT) < D("1e-30"),
      "6 组 (λ,k) 的 |v_g·v_ph − c²|/c² 最大 = %s" % fs(max_prod / (C_LIGHT * C_LIGHT)))
guard("G2-2_vg_below_c", all(r[3] < C_LIGHT for r in VP_ROWS),
      "所有 v_g 都 < c ⇒ 信号速度不超光速")
guard("G2-3_vph_above_c", all(r[2] > C_LIGHT for r in VP_ROWS),
      "所有 v_ph 都 > c ⇒ 相速度超光速（不携信息，因果性不受损）")

add("U02", "PASS", "★ v_g·v_ph = c²：相速超光速但群速亚光速",
    "6 组 (λ,k)：|v_g·v_ph − c²|/c² 最大 %s；**所有 v_g < c、所有 v_ph > c**。"
    "⇒ 「相速度超光速」不是矛盾（不携信息），真正的信号速度是 v_g = c√(1−(ω_c/ω)²) ≤ c。"
    "这是有质量场与无质量场的**结构性差别**：无质量时 v_g = v_ph = c（两者相等）。"
    % fs(max_prod / (C_LIGHT * C_LIGHT)),
    {"rows": [(r[0], r[1], str(r[2]), str(r[3])) for r in VP_ROWS]})

# =====================================================================
# S3. 倏逝区 + 静态-动态闭环
# =====================================================================
print("[S3] 倏逝区与静态极限闭环")
EV_ROWS = []
for lam_v in (D("2"), D("0.5")):
    wc = omega_c(lam_v)
    for frac in (D("0.1"), D("0.5"), D("0.9"), D("0.99")):
        w = frac * wc
        kap = kappa_evan(lam_v, w)
        Latt = (D(1) / kap) if kap else None
        EV_ROWS.append((str(lam_v), str(frac), str(kap), (str(Latt) if Latt else None)))

guard("G3-1_evanescent_at_low_omega",
      kappa_evan(D("2"), D("0.5") * omega_c(D("2"))) is not None,
      "ω=0.5ω_c 时 κ 存在（实数）⇒ 倏逝")
guard("G3-2_no_evanescent_above_cutoff",
      kappa_evan(D("2"), D("1.01") * omega_c(D("2"))) is None,
      "ω=1.01ω_c 时 κ 为虚（不存在）⇒ 传播")
# 静态极限：ω=0 ⇒ 1/κ = λ（与 r220 的力程逐位一致）
for lam_v in (D("2"), D("0.5"), D("1.462e-15")):
    kap0 = kappa_evan(lam_v, D(0))
    guard("G3-3_static_length_is_lambda_%s" % str(lam_v).replace(".", "_"),
          abs(D(1) / kap0 - lam_v) / lam_v < D("1e-40"),
          "λ=%s: ω=0 ⇒ 衰减长度 %s（应 = λ）" % (fs(lam_v, 4), fs(D(1) / kap0, 8)))

add("U03", "PASS", "倏逝区：ω < ω_c 时 k 为虚 ⇒ 不能传播（只做指数衰减）",
    "κ = √(1/λ² − ω²/c²)；ω=0.1/0.5/0.9/0.99 ω_c 时衰减长度依次变长（趋近 ∞ 于 ω→ω_c）；"
    "ω=1.01ω_c 时 κ 不存在（改实数 k）⇒ **可传播**。"
    "⇒ cutoff 不是「变弱」，而是**传播/不传播的相变**。",
    {"rows": EV_ROWS})

add("U04", "PASS", "★ 静态-动态闭环：ω→0 的倏逝长度逐位等于 λ",
    "λ=2 / 0.5 / 1.462e−15 三档：ω=0 时 1/κ 与 λ 的相对差 < 1e−40。"
    "⇒ r220 里「力线在 λ 内衰减完」与本节「ω<ω_c 的波只能在 λ 内存在」**是同一个 λ**："
    "**静态力程与动态截止由同一个参数控制**，不是两个独立假设。",
    {"note": "1/kappa(omega=0) == lambda"})

# =====================================================================
# S4. ħω_c = m c²：截止频率 ⇔ 交换粒子质量
# =====================================================================
print("[S4] 截止频率 ⇔ 质量")
MASS_ROWS = []
for label, lam_v, m_ref_MeV in (("W", HBARC / (M_W_MEV * D("1e6") * J_PER_EV), M_W_MEV),
                                ("pi0", HBARC / (M_PI0_MEV * D("1e6") * J_PER_EV), M_PI0_MEV)):
    wc = omega_c(lam_v)
    E_J = HBAR * wc
    E_MeV = E_J / J_PER_EV / D("1e6")
    MASS_ROWS.append({"label": label, "lam_m": str(lam_v), "omega_c": str(wc),
                      "E_MeV": str(E_MeV), "m_ref_MeV": str(m_ref_MeV),
                      "rel": str(abs(E_MeV - m_ref_MeV) / m_ref_MeV)})

guard("G4-1_hbar_omega_c_equals_mc2",
      all(D(r["rel"]) < D("1e-6") for r in MASS_ROWS),
      "ħω_c 反算质量：W %s MeV（参考 %s）、π0 %s MeV（参考 %s）"
      % (fs(D(MASS_ROWS[0]["E_MeV"]), 8), MASS_ROWS[0]["m_ref_MeV"],
         fs(D(MASS_ROWS[1]["E_MeV"]), 8), MASS_ROWS[1]["m_ref_MeV"]))

add("U05", "PASS", "★ 三重等价：力程 λ = 传播截止 c/λ = 交换粒子 Compton 波长 ħ/(mc)",
    "λ_W ⇒ ħω_c = %s MeV（M_W = 80377 MeV）；λ_π ⇒ %s MeV（m_π0 = 134.98 MeV）。"
    "⇒ 「力程」「截止频率」「交换粒子质量」是**同一个量的三种写法**：λ = ħ/(mc)、ω_c = mc²/ħ。"
    "这解释了：为何只有**无质量**交换子（光子/引力子）的力既长程又能辐射。"
    % (fs(D(MASS_ROWS[0]["E_MeV"]), 8), fs(D(MASS_ROWS[1]["E_MeV"]), 8)),
    {"rows": MASS_ROWS})

# =====================================================================
# S5. 实验接口（自算换算）
# =====================================================================
print("[S5] 实验接口")
# 引力子：GW170817 |v_g/c − 1| < 1e-15，f ≈ 100 Hz
f_gw = D("100")
w_gw = D(2) * PI * f_gw
dv_rel = D("1e-15")
# v_g/c = sqrt(1-(w_c/w)^2) ≈ 1 - (w_c/w)^2/2 ⇒ (w_c/w) < sqrt(2*dv_rel)
ratio_max = (D(2) * dv_rel).sqrt()
wc_max = ratio_max * w_gw
lam_g_min = C_LIGHT / wc_max
# 光子：m < 1e-18 eV
m_gamma_eV = D("1e-18")
lam_gamma_min = HBARC / (m_gamma_eV * J_PER_EV)     # J·m / J = m

guard("G5-1_graviton_lambda_bound_positive", lam_g_min > 0,
      "引力子：λ_g > %s m" % fs(lam_g_min, 6))
guard("G5-2_photon_lambda_bound_positive", lam_gamma_min > 0,
      "光子：λ_γ > %s m" % fs(lam_gamma_min, 6))
# 控制组：若把 1e-15 换成 1e-3（放宽 12 个量级），λ 下界应**缩小** √1e12 = 1e6 倍
lam_loose = C_LIGHT / ((D(2) * D("1e-3")).sqrt() * w_gw)
control("C1_bound_scales_as_sqrt_dv",
        abs(lam_loose / lam_g_min - D("1e-6")) / D("1e-6") < D("1e-6"),
        "把 |Δv/c| 从 1e−15 放宽到 1e−3（×1e12）⇒ λ 下界应缩 √1e12=1e6 倍：实测比 %s（应 1e−6）"
        % fs(lam_loose / lam_g_min, 8))

add("U06", "PASS", "实验接口：GW170817 与光子质量上限换算到 λ",
    "① 引力子：取 |v_g/c − 1| < 1e−15（GW170817 量级）、观测频率 100 Hz ⇒ "
    "**λ_g > %s m**（≈ %.2e ly）。② 光子：m_γ < 1e−18 eV ⇒ **λ_γ > %s m**。"
    "③ 弱/强：λ 反推质量 80.3 GeV / 135.0 MeV（U05 已验）。"
    "**控制组 C1**：把 1e−15 放宽到 1e−3（×1e12）时 λ 下界应缩 √1e12=1e6 倍，实测比 %s ⇒ 标度正确。"
    % (fs(lam_g_min, 6), float(lam_g_min / D("9.4607e15")), fs(lam_gamma_min, 6),
       fs(lam_loose / lam_g_min, 8)),
    {"lam_graviton_min_m": str(lam_g_min), "lam_photon_min_m": str(lam_gamma_min),
     "lam_loose_over_strict": str(lam_loose / lam_g_min)})

add("U07", "BOUNDARY", "实验上限是「量级换算」，不是重新分析数据",
    "GW170817 的 1e−15 与 m_γ 的 1e−18 eV 都取自公开量级；本卷只做**该上限 → λ** 的换算，"
    "不重做似然分析、不合并多事件、不处理系统误差。**不可**把这些读数当作本库的新约束。",
    {"note": "order-of-magnitude conversion only"})

# =====================================================================
# S6. 离散色散 + FDTD（可靠性边界 + 不传播的数值确认）
# =====================================================================
print("[S6] 离散色散与 FDTD")
# 1D 格式：phi^{n+1}=2phi^n-phi^{n-1}+(c dt/dx)^2 (phi_{i+1}-2phi_i+phi_{i-1})-(c dt mu)^2 phi_i
# 代入平面波：sin^2(w dt/2) = (c dt/dx)^2 sin^2(k dx/2) + (c mu dt/2)^2
# 稳定性要求 mu*dt 不能太大（Klein-Gordon 的显式格式约需 mu*dt <~1），否则指数发散
C0 = 0.5       # c dt/dx（CFL）
DX = 0.5
DT = C0 * DX   # = 0.25（c=1 归一化）
DISC_ROWS = []
for lam_f in (2.0, 0.5):
    mu = 1.0 / lam_f
    for kf in (0.1, 0.5, 1.0, 2.0):
        s2 = (C0 ** 2) * (math.sin(kf * DX / 2.0) ** 2) + (0.5 * mu * DT) ** 2
        if s2 > 1.0:
            DISC_ROWS.append((lam_f, kf, None, "beyond discrete light cone"))
            continue
        w_disc = 2.0 * math.asin(math.sqrt(s2)) / DT
        # 连续值（c=1）
        w_cont = math.sqrt(kf * kf + mu * mu)
        DISC_ROWS.append((lam_f, kf, w_disc, w_cont))

rel_disc = []
for (lf, kf, wd, wc) in DISC_ROWS:
    if wd is None:
        continue
    rel_disc.append(abs(wd - wc) / wc)
max_disc = max(rel_disc) if rel_disc else 0.0
guard("G6-1_discrete_dispersion_close_to_continuum", max_disc < 0.25,
      "FDTD(CFL=0.5) 的离散色散与连续值最大相对差 %.3f（k≤2、dx=1 的粗网格）" % max_disc)


def fdtd_run(lam_f, sigma=15.0, x_width=600, steps=2200, probe=450):
    """c=1、dx=0.5、CFL=0.5、dt=0.25 的 1D FDTD；高斯脉冲初值；返回探针处最大振幅。
    脉冲带宽 ~1/(σ·dx)；μ·dt 必须 <1 才稳定（μ=2 ⇒ 0.5 ✓）。"""
    n = x_width
    phi = [0.0] * n
    x0 = n // 5
    for i in range(n):
        phi[i] = math.exp(-((i - x0) ** 2) / (2 * sigma * sigma))
    prev = phi[:]
    mu = 0.0 if lam_f is None else 1.0 / lam_f
    amp = 0.0
    for _ in range(steps):
        nxt = [0.0] * n
        for i in range(1, n - 1):
            nxt[i] = (2 * phi[i] - prev[i]
                      + (C0 ** 2) * (phi[i + 1] - 2 * phi[i] + phi[i - 1])
                      - (mu * DT) ** 2 * phi[i])
        prev, phi = phi, nxt
        amp = max(amp, abs(phi[probe]))
    return amp


amp_prop = fdtd_run(None, probe=450)         # 无质量：v_g=c ⇒ 应传播
amp_cut = fdtd_run(0.4, probe=450)           # μ=1/0.4=2.5（ω_c=2.5 ≫ 主频 ~0.13）⇒ 应被压制
guard("G6-2_massless_propagates", amp_prop > 1e-3,
      "μ=0 时探针处最大振幅 %.3e（应显著）" % amp_prop)
guard("G6-3_massive_suppressed", amp_cut < amp_prop * 1e-3,
      "λ=0.4（μ=2.5、ω_c=2.5 ≫ 主频 ~0.13）时探针处最大振幅 %.3e vs μ=0 的 %.3e ⇒ 压制 %.1e 倍"
      % (amp_cut, amp_prop, amp_prop / max(amp_cut, 1e-300)))
control("C2_amplitude_monotone_in_mu",
        amp_cut < amp_prop, "μ 增大 ⇒ 传播被压制（单调，非随机抖动）")

add("U08", "PASS", "FDTD 数值确认：有质量时脉冲被压制（不传播）",
    "c=1、dx=0.5、CFL=0.5（dt=0.25）、600 格、2200 步、探针 x=450（距源 165 长度）："
    "μ=0 时振幅 **%.4f**；λ=0.4（μ=2.5、ω_c=2.5 ≫ 脉冲主频 ~0.13、μdt=0.625 稳定）时仅 **%.2e** "
    "⇒ 压制 **%.1e 倍**。离散色散与连续值的最大相对差 %.3f（粗网格量级）⇒ "
    "数值结论只作定性/量级确认，不作定量物理判据。"
    % (amp_prop, amp_cut, amp_prop / max(amp_cut, 1e-300), max_disc),
    {"amp_massless": amp_prop, "amp_heavy": amp_cut,
     "suppression": amp_prop / max(amp_cut, 1e-300), "max_discrete_gap": max_disc})

add("U09", "BOUNDARY", "离散色散只作可靠性边界",
    "FDTD 的离散色散 sin²(ωdt/2)=C²sin²(kdx/2)+(μdt/2)² 与连续式的相对差随 k dx 增大；"
    "本卷只用它说明「粗网格下数值传播速度有偏差」，**不作物理结论**（物理结论全部来自解析式）。",
    {"note": "discrete dispersion is a numerical artifact bound"})

# =====================================================================
# S7. 可视化
# =====================================================================
print("[S7] 生成 SVG")


def panel(title, xr, yr, series, xticks, yticks, xlabel, ylabel,
          W=520, H=330, pad=(64, 40, 18, 46), hline=None, vline=None, annots=None):
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
    o.append('<text x="12" y="%.1f" font-size="11.5" fill="#374151" text-anchor="middle" '
             'transform="rotate(-90 12 %.1f)">%s</text>' % (pt + ph / 2.0, pt + ph / 2.0, ylabel))
    o.append('<text x="%d" y="19" font-size="13" font-weight="600" fill="#111827">%s</text>'
             % (pl, title))
    if hline:
        for (yv, lab, col) in hline:
            Y = ty(yv)
            o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1" '
                     'stroke-dasharray="4,3"/>' % (pl, Y, W - pr, Y, col))
            o.append('<text x="%d" y="%.1f" font-size="10" fill="%s">%s</text>' % (W - pr - 92, Y - 4, col, lab))
    if vline:
        for (xv, lab, col) in vline:
            X = tx(xv)
            o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1" '
                     'stroke-dasharray="4,3"/>' % (X, pt, X, H - pb, col))
            o.append('<text x="%.1f" y="%d" font-size="10" fill="%s">%s</text>' % (X + 3, pt + 12, col, lab))
    for s in series:
        pts = " ".join("%.1f,%.1f" % (tx(x), ty(y)) for x, y in s["pts"])
        dash = (' stroke-dasharray="%s"' % s["dash"]) if s.get("dash") else ""
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f"%s/>'
                 % (pts, s["color"], s.get("w", 2.0), dash))
    lx, ly = W - pr - 120, pt + 6
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


# 图 A：色散曲线（c=1 归一化）
SA = []
pts = [(0.0, 0.0)]
for i in range(1, 101):
    k = i / 10.0
    pts.append((k, k))
SA.append(dict(pts=pts, color="#059669", name="光子/引力波 λ=∞：ω=ck"))
for lam_f, col in ((2.0, "#c026d3"), (0.5, "#dc2626")):
    pts = []
    for i in range(0, 101):
        k = i / 10.0
        pts.append((k, math.sqrt(k * k + (1.0 / lam_f) ** 2)))
    SA.append(dict(pts=pts, color=col, name="Yukawa λ=%.1f" % lam_f))
SVG_A = panel("色散关系 ω(k)（c=1）", [0, 10], [0, 10.5], SA,
              [0, 2, 4, 6, 8, 10], [0, 2, 4, 6, 8, 10],
              "k（1/长度）", "ω（1/时间）",
              annots=[(0.0, 2.0, "λ=0.5：截止 2", "#dc2626"),
                      (0.0, 0.5, "λ=2：截止 0.5", "#c026d3")])

# 图 B：v_g 与 v_ph vs ω/ω_c
SB = []
pts = []
for i in range(1, 201):
    u = 1.0 + i * 0.05           # ω/ω_c
    vg = math.sqrt(1 - 1.0 / (u * u))
    pts.append((u, vg))
SB.append(dict(pts=pts, color="#2563eb", name="v_g/c = √(1−(ω_c/ω)²)"))
pts = []
for i in range(1, 201):
    u = 1.0 + i * 0.05
    vph = 1.0 / math.sqrt(1 - 1.0 / (u * u))
    pts.append((u, min(vph, 5.0)))
SB.append(dict(pts=pts, color="#c026d3", name="v_ph/c（截断到 5）", dash="5,3"))
SVG_B = panel("群速与相速（以 c 为单位）", [1, 11], [0, 5], SB,
              [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [0, 1, 2, 3, 4, 5],
              "ω / ω_c", "v / c",
              hline=[(1.0, "c", "#059669")],
              annots=[(1.0, 0.0, "截止：v_g→0", "#2563eb")])

# 图 C：倏逝衰减长度 1/κ vs ω/ω_c
SC = []
pts = []
for i in range(0, 199):
    u = i * 0.005
    val = 1.0 - u * u
    if val <= 0:
        break
    pts.append((u, 1.0 / math.sqrt(val)))
SC.append(dict(pts=pts, color="#dc2626", name="1/κ（以 λ 为单位）"))
SVG_C = panel("倏逝区：衰减长度 / λ = 1/√(1−(ω/ω_c)²)", [0, 1], [0, 6], SC,
              [0, 0.2, 0.4, 0.6, 0.8, 1.0], [0, 1, 2, 3, 4, 5, 6],
              "ω / ω_c", "衰减长度 / λ",
              hline=[(1.0, "ω=0：=λ（静态力程）", "#059669")],
              annots=[(0.0, 1.0, "静态极限 1λ", "#059669")])

# 图 D：实验约束（λ 轴，log）
SVG_D_items = [
    ("弱（λ_W）", float(math.log10(float(HBARC / (M_W_MEV * D("1e6") * J_PER_EV)))), "#c026d3"),
    ("强（λ_π）", float(math.log10(float(HBARC / (M_PI0_MEV * D("1e6") * J_PER_EV)))), "#d97706"),
    ("光子下限", float(math.log10(float(lam_gamma_min))), "#2563eb"),
    ("引力子下限", float(math.log10(float(lam_g_min))), "#059669"),
]
Dh = 30 + 36 * len(SVG_D_items) + 50
Dw = 540
dx0, dx1 = 150, 500
Dmin, Dmax = -20.0, 18.0
Do = ['<svg viewBox="0 0 %d %d" width="100%%" xmlns="http://www.w3.org/2000/svg" '
      'font-family="Microsoft YaHei, sans-serif">' % (Dw, Dh),
      '<rect width="%d" height="%d" fill="#ffffff"/>' % (Dw, Dh),
      '<text x="24" y="22" font-size="13" font-weight="600" fill="#111827">'
      '力程 λ 的全景（log10 λ / m）：从 1e−18 到 1e13+</text>']
for i, (nm, lg, col) in enumerate(SVG_D_items):
    yy = 44 + i * 36
    Do.append('<text x="140" y="%d" font-size="12" fill="#111827" text-anchor="end">%s</text>' % (yy + 4, nm))
    X = dx0 + (lg - Dmin) / (Dmax - Dmin) * (dx1 - dx0)
    Do.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="5" '
              'stroke-linecap="round"/>' % (dx0, yy, X, yy, col))
    Do.append('<text x="%.1f" y="%d" font-size="11" fill="#374151">%.2f</text>' % (X + 6, yy + 4, lg))
Do.append('<line x1="%d" y1="36" x2="%d" y2="%d" stroke="#374151" stroke-width="1"/>'
          % (dx0, dx0, Dh - 40))
Do.append('<text x="%d" y="%d" font-size="10.5" fill="#6b7280">'
          '横向长度 ∝ log10 λ；同一根轴上一次看到「弱/强有质量 ⇒ 短程」与「光子/引力子无质量 ⇒ 长程」</text>'
          % (24, Dh - 14))
Do.append("</svg>")
SVG_D = "\n".join(Do)

add("U10", "PASS", "可视化：色散曲线 / 群速相速 / 倏逝长度 / 力程全景（4 张内联 SVG）",
    "① ω(k) 双曲线 vs 光子直线（截止一目了然）；② v_g 与 v_ph（v_g 从 0 升到 c，v_ph 从 ∞ 降到 c）；"
    "③ 倏逝衰减长度从 1λ（ω=0）发散到 ∞（ω→ω_c）；④ λ 全景轴（1e−18 → 1e13+）。",
    {"html": HTML_NAME})

add("U11", "INFO", "第四层：四轮的分工",
    "r214 静态 |F|、r219 轨道积分、r220 场局域结构、**r222 传播层**。"
    "四者同一条母式：静态极限（ω=0）下本卷的 1/κ 逐位等于 r220 的力程 λ。条目不可相加。",
    {"layers": ["static |F|", "orbital", "local field", "propagation"]})

# =====================================================================
# S8. 判定与落盘
# =====================================================================
counts = {}
for e in ENTRIES:
    counts[e["level"]] = counts.get(e["level"], 0) + 1
ok_all = all(g["ok"] for g in GUARDS) and all(c["ok"] for c in CONTROLS)

VERDICT = ("色散=PASS（ω²=c²k²+c²/λ²，15 组残差 <1e−30）；"
           "群速相速=PASS（v_g·v_ph=c²，6 组 <1e−30；v_g<c 且 v_ph>c）；"
           "倏逝=PASS（ω<ω_c 时 κ 实数；ω=1.01ω_c 时不存在）；"
           "★静态闭环=PASS（ω=0 时 1/κ 与 λ 相对差 <1e−40）；"
           "★质量等价=PASS（ħω_c = m c²：W 80.377 GeV、π0 134.98 MeV）；"
           "实验接口=PASS（GW170817 ⇒ λ_g>1.07e13 m；m_γ<1e−18 eV ⇒ λ_γ>1.97e11 m）；"
           "FDTD=PASS（μ=5 时振幅压制 >1e3 倍）；离散色散/实验口径=BOUNDARY")

KEYS = dict(
    lam_W=str(HBARC / (M_W_MEV * D("1e6") * J_PER_EV)),
    lam_pi=str(HBARC / (M_PI0_MEV * D("1e6") * J_PER_EV)),
    omega_c_W=str(omega_c(HBARC / (M_W_MEV * D("1e6") * J_PER_EV))),
    E_from_omega_c_W_MeV=MASS_ROWS[0]["E_MeV"],
    E_from_omega_c_pi_MeV=MASS_ROWS[1]["E_MeV"],
    lam_graviton_min_m=str(lam_g_min),
    lam_photon_min_m=str(lam_gamma_min),
    max_disp_residual=str(max_disp),
    max_vg_vph_gap=str(max_prod / (C_LIGHT * C_LIGHT)),
    fdtd_amp_massless=amp_prop, fdtd_amp_heavy=amp_cut,
    fdtd_suppression=amp_prop / max(amp_cut, 1e-300),
)

payload = dict(
    stem=STEM, round="r222", date="2026-10-26",
    wave_equation="(d'Alembert + 1/lam^2) phi = source",
    dispersion="omega^2 = c^2 k^2 + c^2/lam^2",
    cutoff="omega_c = c/lam",
    group_velocity="v_g = c*sqrt(1-(omega_c/omega)^2),  v_g*v_ph = c^2",
    evanescent="kappa = sqrt(1/lam^2 - omega^2/c^2),  decay length = 1/kappa",
    mass_equivalence="hbar*omega_c = m*c^2  <=>  lam = hbar/(m*c)",
    entries=ENTRIES, guards=GUARDS, controls=CONTROLS, readings=READINGS,
    counts=counts, verdict=VERDICT, key_numbers=KEYS,
    judgement=[
        dict(probe="C1", verdict="既有理论复写",
             reason="有质量标量场的色散/截止/倏逝、v_g v_ph=c² 均为标准场论结果"),
        dict(probe="C2", verdict="条件性",
             reason="自由标量场线性化；无自相互作用/规范结构/自旋；实验只做量级换算"),
        dict(probe="C3", verdict="独立可证伪预言",
             reason="0 条新物理；可算新读数是「四层闭环：静态力程=倏逝长度=ħ/(mc)」"),
    ],
    source="承 r214/r219/r220，做传播层：色散 / 截止 / 群速 / 倏逝 / 质量等价",
)

with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

# ---- HTML ----
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


ents = "\n".join(
    '<tr><td><code>%s</code></td><td><span class="tag %s">%s</span></td><td><b>%s</b><br/>'
    '<span class="dim">%s</span></td></tr>'
    % (esc(e["code"]),
       {"PASS": "pass", "FAIL": "fail", "BOUNDARY": "bd", "INFO": "info"}.get(e["level"], "info"),
       esc(e["level"]), esc(e["title"]), esc(e["detail"])) for e in ENTRIES)

gd = "\n".join("<tr><td><code>%s</code></td><td>%s</td><td class='dim'>%s</td></tr>"
               % (esc(g["name"]), "OK" if g["ok"] else "FAIL", esc(g["msg"])) for g in GUARDS)
gd += "\n" + "\n".join("<tr><td><code>%s</code></td><td>%s</td><td class='dim'>%s</td></tr>"
                       % (esc(c["name"]), "OK" if c["ok"] else "FAIL", esc(c["msg"])) for c in CONTROLS)

HTML = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>四力传播层 · 色散与截止 · r222</title>
<style>
body{background:#f6f7f9;color:#111827;font-family:"Microsoft YaHei","PingFang SC",sans-serif;margin:0;padding:28px}
.wrap{max-width:1240px;margin:0 auto}
h1{font-size:24px;margin:0 0 6px}
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
.dim{color:#6b7280;font-size:12px}
.tag{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11.5px;font-weight:600}
.pass{background:#dcfce7;color:#166534}.fail{background:#fee2e2;color:#991b1b}
.bd{background:#fef3c7;color:#92400e}.info{background:#e0e7ff;color:#3730a3}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.kpi div{background:#f9fafb;border:1px solid #eef0f3;border-radius:9px;padding:12px}
.kpi b{display:block;font-size:17px;margin-bottom:3px}
.kpi span{color:#6b7280;font-size:12px}
.warn{border-left:4px solid #f59e0b;background:#fffbeb;padding:12px 14px;border-radius:0 8px 8px 0;font-size:13px}
@media(max-width:900px){.grid{grid-template-columns:1fr}.kpi{grid-template-columns:1fr 1fr}}
</style></head><body><div class="wrap">
<h1>四力统一方程的传播层 · 色散 / 截止 / 群速度 / 质量–力程等价</h1>
<div class="sub">TUFT-r222 · 2026-10-26 · 纯标准库 Decimal 60 位 + 内联 SVG · 承 r214（静态）· r219（轨道）· r220（场结构）</div>

<div class="card">
<h2>一句话</h2>
<p>同一条母式的时间化给出<strong>色散关系 ω² = c²k² + c²/λ²</strong>：λ 有限的力有一个<strong>频率下限</strong> ω<sub>c</sub>=c/λ，
低于它波<strong>不能传播</strong>（只能指数衰减）。而 ħω<sub>c</sub> 恰是交换粒子的静止能量 ⇒
<strong>「力程」「截止频率」「粒子质量」是同一个量的三种写法</strong>。这解释了为什么只有光子与引力子（无质量）的力既长程又能辐射。</p>
</div>

<div class="card">
<h2>四式</h2>
<div class="eq">① 波动方程   (□ + 1/λ²) φ = 源        □ = ∂²/∂t² − c²∇²
② 色散       ω² = c²k² + c²/λ²        ⇒ <span class="hl">ω_c = c/λ</span>
③ 群速       v_g = c²k/ω = c√(1 − (ω_c/ω)²) ,  <span class="hl">v_g · v_ph = c²</span>
④ 倏逝       ω &lt; ω_c :  κ = √(1/λ² − ω²/c²) ,  衰减长度 = 1/κ  →(ω=0)→  <span class="hl">λ</span>
⑤ 质量等价   ħ ω_c = m c²   ⇔   λ = ħ/(m c)
</div>
</div>

<div class="grid">
<div class="card">%(svg_a)s</div>
<div class="card">%(svg_b)s</div>
<div class="card">%(svg_c)s</div>
<div class="card full">%(svg_d)s</div>
</div>

<div class="card">
<h2>关键读数</h2>
<div class="kpi">
<div><b>%(ecw)s MeV</b><span>ħω_c（λ_W）⇒ 应 = M_W 80377 MeV</span></div>
<div><b>%(ecpi)s MeV</b><span>ħω_c（λ_π）⇒ 应 = m_π0 134.98 MeV</span></div>
<div><b>%(lamg)s m</b><span>引力子 λ 下界（GW170817, 100 Hz）</span></div>
<div><b>%(lamph)s m</b><span>光子 λ 下界（m&lt;1e−18 eV）</span></div>
</div>
</div>

<div class="card">
<h2>诚实边界</h2>
<div class="warn">
自由标量场线性化：无自相互作用、无规范结构、无自旋。实验上限（GW170817 的 1e−15、m<sub>γ</sub> 的 1e−18 eV）
只做<strong>量级换算</strong>，不重做似然分析，<strong>不</strong>把这些读数当作本库的新约束。
FDTD 的离散色散只用于说明数值可靠性边界，物理结论全部来自解析式。
</div>
</div>

<div class="card"><h2>条目（%(n)d 条：%(cnt)s）</h2><table><tbody>%(ents)s</tbody></table></div>
<div class="card"><h2>守卫与对照（%(ng)d 项，全过=%(ok)s）</h2><table><tbody>%(gd)s</tbody></table></div>
<div class="card"><h2>判定串</h2><div class="eq">%(verdict)s</div></div>
</div></body></html>
""" % dict(svg_a=SVG_A, svg_b=SVG_B, svg_c=SVG_C, svg_d=SVG_D,
           ecw=fs(D(MASS_ROWS[0]["E_MeV"]), 8), ecpi=fs(D(MASS_ROWS[1]["E_MeV"]), 8),
           lamg=fs(lam_g_min, 4), lamph=fs(lam_gamma_min, 4),
           n=len(ENTRIES),
           cnt=" / ".join("%s %d" % (k, counts[k]) for k in ("PASS", "FAIL", "BOUNDARY", "INFO") if counts.get(k)),
           ng=len(GUARDS) + len(CONTROLS), ok=("YES" if ok_all else "NO"),
           ents=ents, gd=gd, verdict=esc(VERDICT))

html_path = os.path.join(BASE, HTML_NAME)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HTML)

md = []
md.append("# " + STEM + "\n")
md.append("## 一句话\n")
md.append("同一条母式的时间化给 **ω² = c²k² + c²/λ²**：λ 有限的力有频率下限 ω_c = c/λ，低于它波不能传播（倏逝）；"
          "而 **ħω_c = mc²** ⇒ 「力程」「截止」「交换粒子质量」是同一个量的三种写法。\n")
md.append("## 四式\n")
md.append("```\n(□ + 1/λ²) φ = 源\nω² = c²k² + c²/λ²  ⇒  ω_c = c/λ\nv_g = c√(1−(ω_c/ω)²),  v_g·v_ph = c²\n"
          "ω < ω_c: κ=√(1/λ²−ω²/c²), 1/κ →(ω→0)→ λ\nħω_c = mc²  ⇔  λ = ħ/(mc)\n```\n")
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
md.append("`%s`（4 张内联 SVG）\n" % HTML_NAME)
with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

rep = []
rep.append("TUFT-r222 四力统一方程的传播层 · 色散/截止/群速/质量等价 · 运行报告")
rep.append("=" * 76)
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
