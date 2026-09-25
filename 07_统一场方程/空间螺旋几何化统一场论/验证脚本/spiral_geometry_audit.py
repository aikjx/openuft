# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · 数值独立复算（openuft 诚实审计口径）

定位
----
本脚本对 `00_核心理论体系总纲.md` / `01_全维评级与诚实边界.md` 中登记的公式做
**独立复算**，不引用原文献的任何结论数值，只引用 CODATA 常数与纯数学恒等式。

红线（必须遵守）
----------------
1. 保留全部原始矛盾输出，**不做任何美化、不把 FAIL 降为 PASS**。
2. 只判定「数值/量纲是否自洽」，**不判定物理真伪**；数学自洽 != 实验证实。
3. 区分「恒等式（无物理信息）」与「独立推导（有信息）」，前者一律标 INFO。

依赖：仅标准库（math / csv / json），无 sympy / mpmath。
运行：python spiral_geometry_audit.py
"""

import math
import os
import sys

# Windows GBK 控制台保护：下标/希腊字母等字符会导致 UnicodeEncodeError
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- 常数（CODATA 2018 / SI 2019）
C = 299792458.0                 # c   m/s   （精确定义）
HBAR = 1.054571817e-34          # ℏ   J·s
QE = 1.602176634e-19            # e   C     （精确定义）
EPS0 = 8.8541878128e-12         # ε₀  F/m
MU0 = 1.25663706212e-6          # μ₀  H/m
G = 6.67430e-11                 # G   m³·kg⁻¹·s⁻²
ALPHA = 7.2973525693e-3         # α   精细结构常数
ME = 9.1093837015e-31           # m_e kg
MP = 1.67262192369e-27          # m_p kg
MPL = 2.176434e-8               # m_P kg
LPL = 1.616255e-35              # ℓ_P m

ALPHA_INV = 1.0 / ALPHA
ALPHA_137 = 1.0 / 137.0         # 文献多处采用的取整值

# ---------------------------------------------------------------- 结果收集
RESULTS = []


def rec(sid, sec, title, verdict, detail):
    RESULTS.append({
        "id": sid,
        "sec": sec,
        "title": title,
        "verdict": verdict,
        "detail": detail,
    })


def P(sid, sec, title, detail):
    rec(sid, sec, title, "PASS", detail)


def F(sid, sec, title, detail):
    rec(sid, sec, title, "FAIL", detail)


def BO(sid, sec, title, detail):
    rec(sid, sec, title, "BOUNDARY", detail)


def IN(sid, sec, title, detail):
    rec(sid, sec, title, "INFO", detail)


def rel(a, b):
    """相对偏差"""
    if b == 0:
        return float("nan")
    return abs(a - b) / abs(b)


def g(x, n=6):
    return "%.*g" % (n, x)


# ---------------------------------------------------------------- 量纲工具 (M, L, T, I)
D_M = (1, 0, 0, 0)
D_L = (0, 1, 0, 0)
D_T = (0, 0, 1, 0)
D_I = (0, 0, 0, 1)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * n for x in a)


def dfmt(d):
    names = ("M", "L", "T", "I")
    parts = []
    for nm, e in zip(names, d):
        if e == 0:
            continue
        parts.append(nm + ("^" + str(e) if e != 1 else ""))
    return "·".join(parts) if parts else "1（无量纲）"


D_C = (0, 1, -1, 0)             # c
D_HBAR = (1, 2, -1, 0)          # ℏ
D_G = (-1, 3, -2, 0)            # G
D_EPS0 = (-1, -3, 4, 2)         # ε₀
D_MU0 = (1, 1, -2, -2)          # μ₀
D_LEN = D_L
D_FORCE = (1, 1, -2, 0)         # N
D_POWER = (1, 2, -3, 0)         # W


# ================================================================
# S1 · 体系一 空间螺旋几何本体论
# ================================================================
def section_s1():
    sec = "S1 几何本体论"
    rho = 3.33e-9        # 螺旋半径（文献由 G 反解，此处仅作几何样例）
    b = rho * ALPHA      # 由 α = b/ρ 定义

    l2 = rho * rho + b * b
    ell = math.sqrt(l2)
    kap = rho / l2
    tau = b / l2

    # S1-01 κ²+τ² = 1/(ρ²+b²)
    lhs = kap * kap + tau * tau
    rhs = 1.0 / l2
    P("S1-01", sec, "κ²+τ² = 1/(ρ²+b²) 恒等",
      "κ=" + g(kap) + " m⁻¹, τ=" + g(tau) + " m⁻¹; LHS=" + g(lhs) +
      ", RHS=" + g(rhs) + ", 相对偏差=" + g(rel(lhs, rhs), 3))

    # S1-02 ℓ = 1/√(κ²+τ²) = √(ρ²+b²)
    ell_from_k = 1.0 / math.sqrt(kap * kap + tau * tau)
    P("S1-02", sec, "ℓ = 1/√(κ²+τ²) = √(ρ²+b²)",
      "ℓ_直接=" + g(ell) + " m, ℓ_由κτ=" + g(ell_from_k) + " m, 相对偏差=" +
      g(rel(ell, ell_from_k), 3) + "（标准 Frenet 公式，数学恒等）")

    # S1-03 速度约束
    omega = C / ell
    speed = omega * ell
    P("S1-03", sec, "速度约束 ω√(ρ²+b²)=c",
      "由约束反解 ω=c/ℓ=" + g(omega) + " s⁻¹, 回代 ωℓ=" + g(speed) +
      " m/s, 与 c 相对偏差=" + g(rel(speed, C), 3) + "（定义式，无独立信息）")

    IN("S1-04", sec, "量纲审计：[κ]=[τ]=L⁻¹，[ℓ]=L",
       "几何定义层自洽；本层不含任何物理推导，故为 L1 而非 L3。")


# ================================================================
# S2 · 体系二 α 几何化与拓扑本源
# ================================================================
def section_s2():
    sec = "S2 α 几何化"

    # S2-01 α = τ/κ = b/ρ = tanθ
    rho = 3.33e-9
    b = rho * ALPHA
    ratio = b / rho
    P("S2-01", sec, "α = τ/κ = b/ρ = tanθ 恒等",
      "b/ρ=" + g(ratio) + " vs α=" + g(ALPHA) + "，相对偏差=" +
      g(rel(ratio, ALPHA), 3) + "（恒等，但属 L1 参数化：把已知常数换成几何比值）")

    # S2-02 α 取整值精度
    d = rel(ALPHA_137, ALPHA)
    IN("S2-02", sec, "文献 α=1/137 与 CODATA α 的偏差",
       "1/137=" + g(ALPHA_137) + ", CODATA=" + g(ALPHA) + ", 相对偏差=" +
       g(d, 4) + "（0.026%）。该偏差在 S3 会被 N∝α⁻² 放大约 2 倍。")

    # S2-03 α = sin(1/(N+Δ_top)) 反解 Δ_top
    asin_a = math.asin(ALPHA)
    n_plus = 1.0 / asin_a
    d_top = n_plus - 137.0
    P("S2-03", sec, "α=sin(1/(N+Δ_top)) 反解 Δ_top（N=137 手填）",
      "asin(α)=" + g(asin_a) + " → N+Δ_top=" + g(n_plus, 10) +
      " → Δ_top=" + g(d_top, 4) + "（文献称 ≈0.036，复算一致）。" +
      "注意：N=137 是**输入**不是输出，本式对 α 的本源零贡献。")

    # S2-04 tanθ = √N vs α = 1/137
    tan_from_sqrt = math.sqrt(137.0)
    tan_from_alpha = 1.0 / 137.0
    factor = tan_from_sqrt / tan_from_alpha
    F("S2-04", sec, "【X5 复核】tanθ=√N 与 α=tanθ=1/137 数值矛盾",
      "拓扑绕数路径 tanθ=√137=" + g(tan_from_sqrt) +
      "；主体路径 α=tanθ=1/137=" + g(tan_from_alpha) +
      "；矛盾因子=" + g(factor) + " ≈ 137^1.5。" +
      "两条路径互斥：若 tanθ=√137 则 α=11.7（与观测 α 差 1604 倍），" +
      "若 α=1/137 则拓扑绕数式不成立。文献内部未清理。")

    # S2-05 N_twist 链条
    ntw_geom = ALPHA * ALPHA / (1.0 + ALPHA * ALPHA)     # b²/(ρ²+b²) with b/ρ=α
    ntw_claim = 137.0 / 138.0                            # N/(N+1)
    ntw_geom_alt = 137.0 / 138.0                         # 若 tanθ=√N 则 b²/(ρ²+b²)=N/(N+1)
    alpha_alt = math.sqrt(137.0)
    ntw_geom_alt2 = alpha_alt * alpha_alt / (1.0 + alpha_alt * alpha_alt)
    F("S2-05", sec, "【X5 延伸】N_twist = b²/(ρ²+b²) = N/(N+1) 链条不自洽",
      "取 α=b/ρ=1/137 时 b²/(ρ²+b²)=α²/(1+α²)=" + g(ntw_geom) +
      "，而 N/(N+1)=137/138=" + g(ntw_claim) + "，差 " +
      g(ntw_claim / ntw_geom) + " 倍。" +
      "该等式**仅在 tanθ=√N 分支成立**（验算：tanθ=√137 时 α²/(1+α²)=" +
      g(ntw_geom_alt2) + "=N/(N+1) ✓）。" +
      "⇒ b²/(ρ²+b²)=N/(N+1) 与 α=1/137 不能同时为真，体系二两条推导路径互相排斥。")

    # S2-06 ρ_C
    rho_c_e = HBAR / (ME * C)
    IN("S2-06", sec, "量子相位闭合 m=ℏ/(cρ_C) 的电子 ρ_C",
       "ρ_C(e⁻)=ℏ/(m_e c)=" + g(rho_c_e) + " m（=约化康普顿波长）。" +
       "该值与体系五由 G 反解的 ρ 相差约 8.6e3 倍，见 S5-06。")


# ================================================================
# S3 · 体系三 力系归一化
# ================================================================
def section_s3():
    sec = "S3 力系归一化"

    def n_a(al):
        return 1.0 / (al * al * (1.0 - al))

    def n_b(al):
        return 1.0 / (al * al) + 1.0 / al + 1.0 + al

    na_c = n_a(ALPHA)
    nb_c = n_b(ALPHA)
    na_137 = n_a(ALPHA_137)
    nb_137 = n_b(ALPHA_137)

    P("S3-01", sec, "定义 A：N=1/[α²(1−α)]",
      "N_A(CODATA α)=" + g(na_c, 10) + "，文献称 ≈18916.90839，相对偏差=" +
      g(rel(na_c, 18916.90839), 3))

    P("S3-02", sec, "定义 B：N=1/α²+1/α+1+α",
      "N_B(α=1/137)=" + g(nb_137, 8) + "，文献称 ≈18907，相对偏差=" +
      g(rel(nb_137, 18907.0), 4))

    # S3-03 差异分解（本轮关键量化）
    gap_obs = na_c - nb_137
    gap_def = na_c - nb_c          # 同一 α 下两个定义的真实差异
    gap_alpha = nb_c - nb_137      # 同一定义下 α 取值差异
    tail = ALPHA * ALPHA / (1.0 - ALPHA)   # Σ_{n≥2} αⁿ
    BO("S3-03", sec, "【X1 量化分解】N 两定义差值 ≈9.9 的真实来源",
       "观测差值 N_A(18916.9) − N_B(18907.0) = " + g(gap_obs, 8) + "。分解：" +
       "①同 α 下定义差异 N_A−N_B = Σ_{n≥2}αⁿ = α²/(1−α) = " + g(gap_def, 4) +
       "（仅 5.4e-5）；②α 取值差异（CODATA vs 1/137）贡献 " + g(gap_alpha, 6) +
       "。⇒ 所谓『两定义冲突 18907 vs 18916.9』中 **99.5% 来自 α 取整精度（0.026%）**" +
       "，定义本身的差异只有 " + g(tail, 4) + "。严重度应由『中』下调为『低（口径漂移）』，" +
       "但文献把两种 α 混用仍属未清理的内部不一致。")

    # S3-04 四力归一化
    fg = 1.0 / (ALPHA_137 * ALPHA_137)
    fs = 1.0 / ALPHA_137
    fw = 1.0
    fe = ALPHA_137
    tot = fg + fs + fw + fe
    P("S3-04", sec, "四力归一化 ΣF̂=1（定义 B 口径）",
      "1/α²=" + g(fg) + ", 1/α=" + g(fs) + ", α⁰=1, α=" + g(fe) +
      "；N_B=" + g(tot, 10) + "；占比 " + g(fg / tot * 100, 5) + "% / " +
      g(fs / tot * 100, 4) + "% / " + g(fw / tot * 100, 3) + "% / " +
      g(fe / tot * 100, 3) + "%，与文献 99.27% / 0.7246% / 5.29e-5 / 3.86e-7 一致")

    # S3-05 定义 A 分母下的四力和
    sum4_over_na = tot / na_c
    F("S3-05", sec, "【新增 X13】分母取 N_A 时四力之和 ≠ 1",
      "四力（定义 B 口径）之和 / N_A = " + g(sum4_over_na, 8) +
      "，缺额 " + g(1.0 - sum4_over_na, 4) + "。" +
      "⇒ 定义 A（无穷级数）与『四力归一化=1』**不能同时成立**：" +
      "无穷级数含 α²,α³,… 高阶项，四力只占 99.9477%，余量即体系七命名的暗能量/暗物质/量子涨落。" +
      "文献在体系三用 N_A 陈述、在体系三表格用 N_B 归一化，属口径混用。")

    # S3-06 几何级数恒等
    s = 0.0
    for n in range(-2, 200):
        s += ALPHA ** n
    P("S3-06", sec, "Σ_{n=-2}^{∞} αⁿ = 1/[α²(1−α)] 恒等",
      "截断 n≤200 部分和=" + g(s, 12) + "，闭式=" + g(na_c, 12) +
      "，相对偏差=" + g(rel(s, na_c), 3) + "（数学恒等，无物理信息）")


# ================================================================
# S4 · 体系四 阴阳平衡
# ================================================================
def section_s4():
    sec = "S4 阴阳平衡"
    yin = 1.0 / (1.0 + ALPHA_137 * ALPHA_137)
    yang = ALPHA_137 * ALPHA_137 / (1.0 + ALPHA_137 * ALPHA_137)
    P("S4-01", sec, "cos²θ+sin²θ=1 与 阴/阳 分配",
      "阴=1/(1+α²)=" + g(yin, 10) + ", 阳=α²/(1+α²)=" + g(yang, 6) +
      ", 和=" + g(yin + yang, 12) + "（三角恒等，L0；映射为阴阳属 L1 语义诠释，不可证伪）")


# ================================================================
# S5 · 体系五 全常数几何化字典
# ================================================================
def section_s5():
    sec = "S5 常数字典"

    # S5-01 ε₀μ₀c²
    val = EPS0 * MU0 * C * C
    IN("S5-01", sec, "ε₀μ₀ = 1/c²",
       "ε₀μ₀c²=" + g(val, 12) + "（相对偏差 " + g(rel(val, 1.0), 3) + "）。" +
       "SI 2019 后 ε₀ 由 μ₀ 与 c 定义，**这是定义式而非物理推导**，无信息量。")

    # S5-02 e²
    e2_direct = QE * QE
    e2_geo = 4.0 * math.pi * EPS0 * HBAR * C * ALPHA
    P("S5-02", sec, "e² = 4πε₀ℏc·α",
      "e²=" + g(e2_direct) + ", 4πε₀ℏcα=" + g(e2_geo) + ", 相对偏差=" +
      g(rel(e2_direct, e2_geo), 3) + "（由 α 定义直接反推，恒等式）")

    # S5-03 G = ℏc/m_P²
    g_planck = HBAR * C / (MPL * MPL)
    P("S5-03", sec, "G = ℏc/m_P²",
      "ℏc/m_P²=" + g(g_planck) + " vs G=" + g(G) + ", 相对偏差=" +
      g(rel(g_planck, G), 4) + "（普朗克质量定义式，非独立推导）")

    # S5-04 【关键】 G = α²μ₀c²ρ² 量纲审计
    d_coef = dpow(D_MU0, 1)          # μ₀
    d_coef = dmul(d_coef, dpow(D_C, 2))  # μ₀c²
    d_rhs_len = dmul(d_coef, dpow(D_LEN, 2))  # μ₀c²ρ²（ρ 按长度）
    d_need_rho2 = ddiv(D_G, d_coef)
    d_need_rho = tuple(x / 2.0 for x in d_need_rho2)
    F("S5-04", sec, "【新增 X8·严重】G = α²μ₀c²ρ² 量纲不自洽",
      "LHS [G]=" + dfmt(D_G) + "；RHS 取 ρ 为长度时 [α²μ₀c²ρ²]=" + dfmt(d_rhs_len) +
      "，二者不等。若强制量纲一致，则要求 [ρ]=" + dfmt(d_need_rho) +
      "（= 电荷/质量，C·kg⁻¹），与『ρ 是螺旋半径（长度）』**直接冲突**。" +
      "⇒ 该式不是物理推导；其 SI 数值吻合只是单位制下的数值巧合（见 S5-05）。")

    # S5-05 ρ 反解复现
    coef = ALPHA * ALPHA * MU0 * C * C
    rho_fit = math.sqrt(G / coef)
    coef137 = ALPHA_137 * ALPHA_137 * MU0 * C * C
    rho_fit137 = math.sqrt(G / coef137)
    P("S5-05", sec, "ρ = √(G/(α²μ₀c²)) 反解复现",
      "ρ(CODATA α)=" + g(rho_fit) + " m；ρ(α=1/137)=" + g(rho_fit137) +
      " m；文献称 ρ≈3.33e-9 m，相对偏差=" + g(rel(rho_fit, 3.33e-9), 3) +
      "。数值吻合，但这是**由 G 反解 ρ 的代数恒等式**（原文献第六章已自陈），零预测力。")

    # S5-06 两个 ρ 的冲突
    rho_c_e = HBAR / (ME * C)
    ratio = rho_fit / rho_c_e
    BO("S5-06", sec, "【新增 X9】体系五 ρ 与体系二 ρ_C 不是同一个量",
      "ρ_G（由 G 反解）=" + g(rho_fit) + " m；ρ_C(e⁻)=ℏ/(m_e c)=" + g(rho_c_e) +
      " m；比值=" + g(ratio) + " 倍。" +
      "两者在全文献中**共用符号 ρ 却相差 4 个数量级**，" +
      "且各自都无独立测量来源 ⇒ 体系二『m=ℏ/(cρ_C)』与体系五『G=α²μ₀c²ρ²』无法联立求解。")

    # S5-07 E, p
    ell = 1.0 / (ME * C / HBAR)   # 电子约化康普顿波长作 ℓ 样例
    e_geo = HBAR * C / ell
    e_mass = ME * C * C
    IN("S5-07", sec, "E=ℏc/ℓ=ℏω 与 p=ℏ/ℓ 量纲自洽",
      "取 ℓ=ℏ/(m_e c)：E=ℏc/ℓ=" + g(e_geo) + " J，m_e c²=" + g(e_mass) +
      " J，相对偏差=" + g(rel(e_geo, e_mass), 3) +
      "。量纲自洽且闭合，但 ℓ 本身无独立测定 ⇒ 属『几何+量子』的 L2 闭合，非 L3。")


# ================================================================
# S6 · 体系六 频率控制与第五力
# ================================================================
def section_s6():
    sec = "S6 频率控制"

    rho = 3.33e-9
    b = rho * ALPHA
    l2 = rho * rho + b * b
    ell = math.sqrt(l2)
    kap = rho / l2
    tau = b / l2

    # S6-01 ω 两式
    w_geo = C / ell                       # 由速度约束
    w_form = C * (kap * kap + tau * tau) / kap   # 由体系六公式
    ratio = w_form / w_geo
    BO("S6-01", sec, "【新增 X10】ω 的两个表达式不自洽",
      "速度约束给 ω=c/ℓ=" + g(w_geo) + " s⁻¹；体系六公式 ω=c(κ²+τ²)/κ 化简为 c/ρ=" +
      g(w_form) + " s⁻¹（因 (κ²+τ²)/κ=1/ρ）；比值=" + g(ratio, 10) +
      " = √(1+α²)，差 " + g((ratio - 1.0) * 100, 4) + "%。" +
      "量级微小但属**定义层互斥**：两者仅当 b=0（α=0，退化螺旋）时才相等。")

    # S6-02 A 量纲
    d_A = dmul(ddiv(dmul(D_HBAR, dpow(D_T, -2)), dmul(D_M, D_C)),
               ddiv(D_LEN, dpow(D_LEN, -2)))
    # κ/(κ²+τ²) 量纲 = L⁻¹ / L⁻² = L
    d_kappa_ratio = ddiv(dpow(D_LEN, -1), dpow(D_LEN, -2))
    d_A = dmul(ddiv(dmul(D_HBAR, dpow(D_T, -2)), dmul(D_M, D_C)), d_kappa_ratio)
    d_acc = (0, 1, -2, 0)
    F("S6-02", sec, "【新增 X14】A=ℏω²/(mc)·κ/(κ²+τ²) 量纲不是加速度",
      "[ℏω²/(mc)]=" + dfmt(ddiv(dmul(D_HBAR, dpow(D_T, -2)), dmul(D_M, D_C))) +
      "，[κ/(κ²+τ²)]=" + dfmt(d_kappa_ratio) + "，故 [A]=" + dfmt(d_A) +
      "。若 A 为引力场加速度，应为 " + dfmt(d_acc) + "；**多出一个长度量纲**。" +
      "除非 ρ 无量纲或隐藏了未声明的量纲因子，否则该式量纲不自洽。")

    # S6-03 F_G,max
    # c⁵/(ℏ ω² (κ²+τ²)) ，代入 ω=c/ℓ, κ²+τ²=1/ℓ²  → c³ℓ⁴/ℏ
    d_fmax = ddiv(dmul(dpow(D_C, 3), dpow(D_LEN, 4)), D_HBAR)
    fmax_lp = (C ** 3) * (LPL ** 4) / HBAR
    fmax_known = C ** 4 / (4.0 * G)
    F("S6-03", sec, "【新增 X15】F_G,max = c⁵/(ℏω²(κ²+τ²)) 量纲不是力",
      "代入 ω=c/ℓ, κ²+τ²=1/ℓ² 化简为 c³ℓ⁴/ℏ，量纲=" + dfmt(d_fmax) +
      "，而力应为 " + dfmt(D_FORCE) + "。" +
      "数值对照（取 ℓ=ℓ_P）：" + g(fmax_lp) + " vs 已知上限力 c⁴/(4G)=" +
      g(fmax_known) + " N，相差 " + g(fmax_known / fmax_lp) + " 倍 ⇒ 量纲错误非数值取整问题。")

    # S6-04 第五力量纲
    d_f5 = dmul(D_HBAR, dpow(D_T, -2))   # ℏ · dω/dt (s⁻²)
    F("S6-04", sec, "【新增 X11】第五力 F₅=(ℏ/2)dω/dt 量纲是功率不是力",
      "[ℏ]=" + dfmt(D_HBAR) + ", [dω/dt]=T⁻² ⇒ [F₅]=" + dfmt(d_f5) +
      " = 瓦特(W)。力应为 " + dfmt(D_FORCE) + "。" +
      "⇒ 所谓『第五力』在量纲层面不成立；若要成立须补一个 T/L⁻¹·… 类的量纲因子（新假设）。")

    # S6-05 κ_drive
    d_kd = ddiv(dmul(D_LEN, dpow(D_T, -2)), dpow(D_C, 2))
    P("S6-05", sec, "κ_drive = ρω²/c² 量纲自洽",
      "[ρω²/c²]=" + dfmt(d_kd) + " = L⁻¹，确为曲率量纲 ✓（但物理机制未给出，属几何类比）")


# ================================================================
# S7 · 体系七 高阶力系
# ================================================================
def section_s7():
    sec = "S7 高阶力系"
    na = 1.0 / (ALPHA * ALPHA * (1.0 - ALPHA))
    s = 0.0
    for n in range(-2, 300):
        s += (ALPHA ** n) / na
    P("S7-01", sec, "Σ_{n=-2}^{∞} αⁿ/N_A = 1",
      "截断 n≤300 部分和=" + g(s, 12) + "（数学恒等）")

    f5 = ALPHA ** 2 / na
    f6 = ALPHA ** 3 / na
    f7 = ALPHA ** 4 / na
    IN("S7-02", sec, "高阶项占比（仅供参考，无可观测支撑）",
      "α²/N=" + g(f5) + "（暗能量力）, α³/N=" + g(f6) +
      "（暗物质力）, α⁴/N=" + g(f7) + "（量子涨落力）。" +
      "这些项的存在由级数定义保证，但**命名不构成物理发现**，体系七为 L1/INFO。")


# ================================================================
# S9 · 体系九 引力「最大 vs 最小」悖论
# ================================================================
def section_s9():
    sec = "S9 引力悖论"

    # S9-01 归一化占比
    fg = 1.0 / (ALPHA_137 * ALPHA_137)
    nb = fg + 1.0 / ALPHA_137 + 1.0 + ALPHA_137
    share = fg / nb * 100.0
    P("S9-01", sec, "引力归一化占比 99.27%",
      "(1/α²)/N_B=" + g(share, 6) + "%，与文献 99.27% 一致（用 CODATA α 同为 " +
      g((1.0 / (ALPHA * ALPHA)) / (1.0 / (ALPHA * ALPHA) + 1.0 / ALPHA + 1.0 + ALPHA) * 100, 6) +
      "%，对该口径不敏感）")

    # S9-02 表观强度比
    k_e2 = QE * QE / (4.0 * math.pi * EPS0)
    r_pp = G * MP * MP / k_e2
    r_ep = G * ME * MP / k_e2
    P("S9-02", sec, "表观强度比（质子-质子）~10⁻³⁶",
      "G m_p²/(e²/4πε₀)=" + g(r_pp) + "，文献称 ~10⁻³⁶，同量级 ✓")

    IN("S9-03", sec, "表观强度比（电子-质子）",
      "G m_e m_p/(e²/4πε₀)=" + g(r_ep) + "。" +
      "⇒ 『引力最弱』的倍数依赖所选粒子对（8e-37 vs 4e-40），文献取 ~10⁻³⁶ 是质子口径。")


# ================================================================
# S10 · 体系十 18917 素数锚点
# ================================================================
def _sieve(n):
    flag = [True] * (n + 1)
    flag[0] = flag[1] = False
    i = 2
    while i * i <= n:
        if flag[i]:
            for j in range(i * i, n + 1, i):
                flag[j] = False
        i += 1
    return flag


def _factor(n):
    out = []
    m = n
    d = 2
    while d * d <= m:
        while m % d == 0:
            out.append(d)
            m //= d
        d += 1
    if m > 1:
        out.append(m)
    return out


def section_s10():
    sec = "S10 18917 锚点"
    flag = _sieve(25000)
    idx_18917 = sum(1 for i in range(2, 18918) if flag[i])
    is_p_18917 = flag[18917]
    is_p_2153 = flag[2153]

    P("S10-01", sec, "18917 的素数性与素数序号",
      "18917 是素数=" + str(is_p_18917) + "；π(18917)=" + str(idx_18917) +
      "（文献称第 2153 个素数，复算一致=" + str(idx_18917 == 2153) + "）")

    P("S10-02", sec, "2153 的素数性",
      "2153 是素数=" + str(is_p_2153) + "；18907=7×37×73=" +
      str(_factor(18907)) + "（**定义 B 的整数 18907 是合数**）")

    na = 1.0 / (ALPHA * ALPHA * (1.0 - ALPHA))
    nb137 = 137.0 * 137.0 + 137.0 + 1.0 + 1.0 / 137.0
    IN("S10-03", sec, "【新增 X12】18917 是 round(N_A) 的性质，且对 α 精度极敏感",
      "N_A(CODATA α)=" + g(na, 8) + " → round=" + str(int(round(na))) +
      "；N_B(α=1/137)=" + g(nb137, 6) + " → round=" + str(int(round(nb137))) +
      "（合数）。⇒ 『18917 是素数』依赖两件事：①取定义 A ②取 CODATA 精度 α。" +
      "α 改用 1/137 时锚点数变成 18907（非素数），**素数/卦象/历史年份整套诠释随之失效**。" +
      "又：N 的真值 18916.908 非整数，素数性是取整后才有的性质，属 L1 诠释，不可证伪。")


# ================================================================
def run():
    RESULTS[:] = []
    section_s1()
    section_s2()
    section_s3()
    section_s4()
    section_s5()
    section_s6()
    section_s7()
    section_s9()
    section_s10()
    return RESULTS


def counts():
    c = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        c[r["verdict"]] = c.get(r["verdict"], 0) + 1
    return c


def render():
    lines = []
    lines.append("# 空间螺旋几何化统一场论 · 数值独立复算报告")
    lines.append("")
    lines.append("> 生成脚本：`spiral_geometry_audit.py`（仅标准库，CODATA 2018 / SI 2019）")
    lines.append("> 本报告**保留全部原始矛盾输出**，不做美化修正。")
    lines.append("")
    c = counts()
    lines.append("## 汇总")
    lines.append("")
    lines.append("| 判定 | 计数 |")
    lines.append("|------|------|")
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        lines.append("| " + k + " | " + str(c.get(k, 0)) + " |")
    lines.append("")
    lines.append("| 条目 | 判定 | 结论 |")
    lines.append("|------|------|------|")
    for r in RESULTS:
        lines.append("| " + r["id"] + " | " + r["verdict"] + " | " +
                     r["title"].replace("|", "/") + " |")
    lines.append("")
    lines.append("## 逐条明细")
    lines.append("")
    cur = None
    for r in RESULTS:
        if r["sec"] != cur:
            cur = r["sec"]
            lines.append("### " + cur)
            lines.append("")
        lines.append("**" + r["id"] + " · [" + r["verdict"] + "] " + r["title"] + "**")
        lines.append("")
        lines.append(r["detail"])
        lines.append("")
    return "\n".join(lines)


def main():
    run()
    print(render())
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spiral_audit_report.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render())
    print("")
    print("[written] " + out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
