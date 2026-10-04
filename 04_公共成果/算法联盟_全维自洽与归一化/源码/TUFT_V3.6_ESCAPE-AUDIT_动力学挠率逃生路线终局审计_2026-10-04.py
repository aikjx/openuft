# -*- coding: utf-8 -*-
"""TUFT V3.6 · ESCAPE-AUDIT · 动力学挠率逃生路线的终局审计。

上游 判定_TUFT_V3.6_OPEN-MAP 把 OPEN-MAP 判为 CLOSED-IMPOSSIBLE，核心链条是 M6：
    对称物质 ⟹ τ=0 ⟹ θ 恒定 ⟹ Ω 常数 ⟹ 四力切换坍缩
但该册 §6 诚实边界留了一条例外：
    M6 依赖「EC 挠率只由自旋流激发」；若采用非 EC 的动力学挠率理论（含 T² 动能项），
    τ 可在真空传播、未必为 0 ⟹ M6 需重判。

本册把这条逃生路线做实。方法：**让步式论证**——全程接受逃生路线的最强假设
（τ 动力学化、可非零、可随空间变化、允许由此产生的新尺度），在此前提下判定它能否救活机制。

量纲约定（务必先看，全部结论依赖它）：
    取 x⁰ = ct ⟹ 所有坐标量纲 = L ⟹ d⁴x = L⁴、∂_μ = L⁻¹
    作用量 S 以 ħ 为单位无量纲 ⟹ [Lagrange 密度] = L⁻⁴
    自检：[R] = L⁻² ⟹ [1/G] = L⁻² ⟹ [G] = L² （Planck 长度平方）✓

八条判定 E1–E8。纯标准库。
"""
import os, sys, math, json

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)
TAG = "TUFT_V3.6_ESCAPE-AUDIT_动力学挠率逃生路线终局审计_2026-10-04"

def dim(**kw):
    d = {"M": 0, "L": 0, "T": 0}; d.update(kw); return d
def dmul(a, b): return {k: a[k] + b[k] for k in ("M", "L", "T")}
def ddiv(a, b): return {k: a[k] - b[k] for k in ("M", "L", "T")}
def dpow(a, p): return {k: a[k] * p for k in ("M", "L", "T")}
def dfmt(a): return "M^%d L^%d T^%d" % (a["M"], a["L"], a["T"])

# ---------- 量纲基元（本约定下只需 L 指数，M/T 恒为 0） ----------
D_L = dim(L=1)
D_invL = dpow(D_L, -1)                 # 一次导数 / 联络 / 挠率：L⁻¹
D_Lag = dpow(D_L, -4)                  # Lagrange 密度（d⁴x=L⁴，S 无量纲）
D_R = dpow(D_L, -2)                    # Riemann 标量曲率
D_Tors = dpow(D_L, -1)                 # 挠率 T：L⁻¹
D_dTors = dmul(D_invL, D_Tors)         # ∂T：L⁻²
D_dTors2 = dpow(D_dTors, 2)            # (∂T)²：L⁻⁴
D_mass = dpow(D_L, -1)                 # 质量（传播挠率的 Yukawa 尺度）：L⁻¹

VERDICTS, KEYS = [], {}
def add(cid, status, title, detail, numbers=None):
    VERDICTS.append(dict(id=cid, status=status, title=title,
                         detail=detail, numbers=numbers or {}))

# ============ E1  挠率动能项的系数是否需要新「带量纲」常数？ ============
# L ⊃ c_T · (∇T)²，要求 [c_T · (∂T)²] = [L] = L⁻⁴
D_cT = ddiv(D_Lag, D_dTors2)
ok_e1 = (D_cT == dim())                # 无量纲 ⟹ True
KEYS["E1_dim_dT2"] = dfmt(D_dTors2)
KEYS["E1_dim_Lag"] = dfmt(D_Lag)
KEYS["E1_dim_cT"] = dfmt(D_cT)
add("E1", "PASS" if ok_e1 else "FAIL",
    "挠率动能项系数 c_T 的量纲（对逃生路线有利，如实记）",
    "取 x⁰=ct 约定 ⟹ [T] = %s、[∂T] = %s、[(∂T)²] = %s，而 [Lagrange 密度] = %s "
    "⟹ **[(∂T)²] 恰好等于 [L]**，故 [c_T] = %s，**无量纲，不引入新带量纲常数**。"
    "（我原以为 T² 动能项必然要新带量纲常数，机器算下来是错的：它与 Maxwell 的 −¼F² **同构**，"
    "系数地位等同于 −¼。）⟹ 逃生路线在**量纲层**得分，Ω5 不因量纲被破。"
    % (dfmt(D_Tors), dfmt(D_dTors), dfmt(D_dTors2), dfmt(D_Lag), dfmt(D_cT)),
    {"[T]": dfmt(D_Tors), "[(∂T)²]": dfmt(D_dTors2),
     "[L]": dfmt(D_Lag), "[c_T]": dfmt(D_cT)})

# ============ E2  导数阶：是否存在 Ostrogradsky 型高阶导数不稳定 ============
# L ~ (∂T)² ⟹ 一阶导数的平方 ⟹ Euler–Lagrange 给出 2 阶运动方程
order_field_deriv = 1
order_eom = 2 * order_field_deriv
ok_e2 = (order_eom == 2)
KEYS["E2_eom_order"] = order_eom
add("E2", "PASS" if ok_e2 else "FAIL",
    "挠率动能项的导数阶（形式层健康，对逃生路线有利）",
    "L ⊃ c_T(∇T)² 只含场的**一阶**导数 ⟹ Euler–Lagrange 给出 **%d 阶**运动方程 "
    "⟹ **不存在 Ostrogradsky 型高阶导数不稳定**（形式层）。"
    "⚠️ 诚实边界：这不排除 **ghost / tachyon** —— 它们来自动能项的**符号与规范结构**，"
    "不是导数阶；PGT 谱分析需文献支撑，**本册不评估（NOT-ASSESSED）**。"
    % order_eom,
    {"场导数阶": order_field_deriv, "运动方程阶": order_eom})

# ============ E3  新尺度：M8 的 Π 定理封死是否被解除？（自我修正上游） ============
# 传播挠率 ⟹ 波动/汤川型 ⟹ 引入 m_τ（L⁻¹）⟹ 出现「第二个 L⁻¹ 尺度」
# 质量项 m²T²：[m²T²] 需 = L⁻⁴ ⟹ [m] = L⁻¹ ✓
D_m2T2 = dmul(dpow(D_mass, 2), dpow(D_Tors, 2))
ok_e3_dim = (D_m2T2 == D_Lag)
n_scales_before = 1                    # 原公理集：κ、τ 同为 L⁻¹ ⟹ 只构成 1 个独立比值
n_scales_after = 2                     # + m_τ ⟹ 可构造 ρ/m_τ
ok_e3 = ok_e3_dim and (n_scales_after > n_scales_before)
KEYS["E3_dim_m"] = dfmt(D_mass)
KEYS["E3_scales_before"] = n_scales_before
KEYS["E3_scales_after"] = n_scales_after
add("E3", "PASS" if ok_e3 else "FAIL",
    "**自我修正上游 M8**：动力学挠率解除 Π 定理封死（对逃生路线有利）",
    "传播挠率带来质量尺度 m_τ（[m_τ²T²] = %s = [L] ✓，量纲闭合）⟹ 公理集中**出现第二个 L⁻¹ 尺度**，"
    "可构造无量纲比 ρ/m_τ ⟹ Ω 的参数自由度由 **%d 增至 %d** ⟹ "
    "**上游 M8「ρ 依赖被 Π 定理封死」在动力学挠率下不成立，需重判**。"
    "这是本册对上游的**自我修正**，如实记 PASS。"
    % (dfmt(D_m2T2), n_scales_before, n_scales_after),
    {"[m_τ]": dfmt(D_mass), "修正前自由度": n_scales_before, "修正后自由度": n_scales_after})

# ============ E4  M4（θ 分区 3 < 4）是否依赖 EC 前提？ ============
# 关键独立性检验：即使 τ 动力学化、取遍实数，κ ≥ 0（Frenet 定义）⟹ θ 仍只在半平面
N = 36000
lo, hi = -math.pi / 2.0, math.pi / 2.0
seg = []
for i in range(N):
    th = lo + (hi - lo) * i / (N - 1)
    seg.append(1 if math.cos(3.0 * th) > 0 else -1)
n_inter_half = 1 + sum(1 for i in range(N - 1) if seg[i] != seg[i + 1])

# 额外：直接在 (κ>0, τ∈R) 的大动态范围网格上扫，确认 τ 的取值范围不影响结论
kappa_fix = 1.0
taus = [-10.0 ** e for e in range(6, -7, -1)] + [0.0] + [10.0 ** e for e in range(-6, 7)]
ths = sorted(set(math.atan2(t, kappa_fix) for t in taus))
KEYS["E4_tau_grid_min"] = min(taus)
KEYS["E4_tau_grid_max"] = max(taus)
KEYS["E4_theta_reached_min"] = min(ths)
KEYS["E4_theta_reached_max"] = max(ths)
# τ 跨越 10^-6..10^6（13 个量级）后，θ 仍被夹在半平面内
theta_escape = (min(ths) < -math.pi / 2.0 + 1e-9) or (max(ths) > math.pi / 2.0 - 1e-9)
KEYS["E4_sign_intervals_halfplane"] = n_inter_half
ok_e4 = (n_inter_half >= 4)
add("E4", "PASS" if ok_e4 else "FAIL",
    "M4 独立性：θ 分区不足 4 **不依赖** EC 前提 ⟹ 逃生路线仍死",
    "即使 τ 完全动力学化并跨越 %d 个量级（τ ∈ [%.0e, %.0e]），Frenet **κ ≥ 0 是定义性**的 "
    "⟹ θ = atan2(τ,κ) 仍被夹死在 [%.4f, %.4f] ⟹ cos3θ 只有 **%d 个符号区间**，"
    "体系要求 **4** 个分区 ⟹ **M4 与挠率是否传播无关，逃生路线不能解除它**。"
    % (len(range(-6, 7)), KEYS["E4_tau_grid_min"], KEYS["E4_tau_grid_max"],
       KEYS["E4_theta_reached_min"], KEYS["E4_theta_reached_max"], n_inter_half),
    {"τ 扫描跨度[量级]": 13, "θ 可达下界": KEYS["E4_theta_reached_min"],
     "θ 可达上界": KEYS["E4_theta_reached_max"],
     "半平面符号区间数": n_inter_half, "要求分区数": 4})

# ============ E5  绕过 M4 的唯一办法 ⟹ 废弃 Ω2 与 cos3θ 结构 ============
# 要 4 个分区，θ 不够 ⟹ 只能改用 ρ/m_τ 分区 ⟹ Ω 不再依赖 θ ⟹ Ω2 公理被替换
n_sectors_by_theta = n_inter_half
need_theta_sectors = 4
must_drop_omega2 = n_sectors_by_theta < need_theta_sectors
KEYS["E5_must_drop_Omega2"] = must_drop_omega2
add("E5", "FAIL" if must_drop_omega2 else "PASS",
    "绕过 E4 的唯一办法是废弃 Ω2 与 cos3θ ⟹ 不是「修补 V3.6」而是**替换核心公理**",
    "θ 只能给 %d 个分区而体系要 %d 个 ⟹ 唯一出路是改用 **ρ/m_τ 分区**，即 Ω = Ω(ρ/m_τ)。"
    "但那样 **θ 不再起作用**，V3.6 的「Ω2：Ω 仅依赖 θ」与 cos3θ 四扇区叙事**整体作废** ⟹ "
    "这不是给 V3.6 打补丁，而是**换掉它的核心公理**；按本目录体例，这属于**新体系**，"
    "须重新提交审计，不能在 V3.6 分支内落地。"
    % (n_sectors_by_theta, need_theta_sectors),
    {"θ 可给分区数": n_sectors_by_theta, "需要分区数": need_theta_sectors,
     "必须废弃 Ω2": must_drop_omega2})

# ============ E6  hierarchy 搬运（本册决定性、独有） ============
# 即使前面全部放开通行（τ 动力学、新尺度、2 自由度、改用 ρ 分区），
# 四力相对强度跨度 ~10^39 仍必须由某个变量承担 ⟹ 三个载体逐一算所需调参数级
#
# 口径 A（常见教科书，以强 = 1）：
#   强 1 ；电磁 1/137 ；弱 1e-5 ；引力 5.9e-39（质子-质子引力/强力）
# 口径 B（保守替代，检验结论稳健性）：
#   强 1 ；电磁 1e-2 ；弱 1e-13 ；引力 1e-38
CAL = {
    "A": {"强": 1.0, "电磁": 1.0 / 137.0, "弱": 1e-5, "引力": 5.9e-39},
    "B": {"强": 1.0, "电磁": 1e-2, "弱": 1e-13, "引力": 1e-38},
}
sector_width = math.pi / 6.0           # 四扇区等分时的扇区宽（半平面 π 分 6 段）
rows_e6, worst_rel = [], None
for tag, cal in sorted(CAL.items()):
    g_grav = cal["引力"]
    # 载体 1：θ 调参 —— 需 cos3θ = g ⟹ 3θ 与 π/2 的偏差 ≈ g ⟹ Δθ = g/3
    dtheta = g_grav / 3.0
    rel_theta = dtheta / sector_width
    # 载体 2：λ 分层 —— Ω = λcos3θ，|cos3θ|≤1 ⟹ 要 Ω ~ g 需 λ ≲ g
    lambda_needed = g_grav
    # 载体 3：ρ 跨量级 —— Ω = Ω(ρ/m) 要跨 39 量级 ⟹ ρ/m 本身跨 10^39（取 log10 估计）
    decades_rho = abs(math.log10(g_grav))
    rows_e6.append(dict(口径=tag, Δθ_需=dtheta, 相对扇区宽=rel_theta,
                        λ_需=lambda_needed, ρ_跨量级=decades_rho))
    if worst_rel is None or rel_theta < worst_rel:
        worst_rel = rel_theta
KEYS["E6_sector_width"] = sector_width
KEYS["E6_rows"] = rows_e6
KEYS["E6_worst_relative_precision"] = worst_rel
KEYS["E6_decades_min"] = min(r["ρ_跨量级"] for r in rows_e6)
add("E6", "FAIL",
    "hierarchy 搬运（**在「cos3θ 数值直接承载耦合强度」的读法下**致命；见 E9 反驳检验）",
    "让步假设下（τ 动力学 + 新尺度 + 2 自由度 + 改用 ρ 分区）仍要解释四力强度跨度 ~10³⁹。"
    "三个可能的承载体逐一机器计算（两套口径 A/B 结论一致）："
    "① **θ 调参**：需 cos3θ = g_引力 ⟹ 3θ 与 π/2 的偏差 ≈ g ⟹ Δθ ≈ %.1e rad，"
    "而扇区宽 = π/6 = %.4f rad ⟹ 相对精度 **%.1e**，即几何角度须被钉到 10⁻³⁹ 相对精度；"
    "② **λ 分层**：|cos3θ| ≤ 1 ⟹ 要 Ω ~ 10⁻³⁹ 必须 λ ≲ 10⁻³⁹，hierarchy 原封不动留在 λ 里；"
    "③ **ρ 跨量级**：Ω(ρ/m_τ) 跨越 **%.0f 个量级** 才够，等于把 hierarchy 搬进几何曲率尺度。"
    "⟹ **三条路都回到同一个 hierarchy**，V3.6 未解释它，只是换了存放位置。"
    % (rows_e6[0]["Δθ_需"], sector_width, worst_rel, KEYS["E6_decades_min"]),
    {"扇区宽[rad]": sector_width, "最坏相对精度": worst_rel,
     "ρ 需跨量级(最小)": KEYS["E6_decades_min"],
     "口径A Δθ": rows_e6[0]["Δθ_需"], "口径B Δθ": rows_e6[1]["Δθ_需"]})

# ============ E9  反驳检验 + 本册最强论点：四力「相对强度」是能标依赖量 ============
# (a) 对 E6 的反驳：若把 Ω 定义成耦合的「对数」Ω = k·ln g，则 10³⁹ 跨度只需 Ω 变化 ln(10³⁹) 倍
g_grav_A = CAL["A"]["引力"]
omega_span_log = abs(math.log(g_grav_A))
ok_refute = omega_span_log < 1e3      # 需求从「10⁻³⁹ 相对精度」降为「O(10²) 幅度」
KEYS["E9_omega_span_log"] = omega_span_log
# (b) 但引力耦合本身是能标依赖的：α_G(E) = G·E²（自然单位；[G]=L² 与本册约定自洽）
M_Z = 91.1876                          # GeV
E_Pl = 1.2209e19                       # Planck 能标 (GeV)
alpha_G_1GeV = g_grav_A
E_star = math.sqrt(1.0 / alpha_G_1GeV)  # α_G = 1 处的能标
ratio_Pl = E_star / E_Pl
alpha_G_MZ = alpha_G_1GeV * (M_Z ** 2)
# 对照：QCD 一圈跑动 α_s⁻¹(Q) = α_s⁻¹(Q₀) + (b/2π)·ln(Q/Q₀)，b = 11 − 2n_f/3，n_f = 5
b_s = 11.0 - 2.0 * 5.0 / 3.0
alpha_s_1GeV = 0.5
alpha_s_MZ = 1.0 / (1.0 / alpha_s_1GeV + (b_s / (2.0 * math.pi)) * math.log(M_Z))
dec_G = math.log10(alpha_G_MZ / alpha_G_1GeV)
dec_s = math.log10(alpha_s_MZ / alpha_s_1GeV)
KEYS["E9_E_star_GeV"] = E_star
KEYS["E9_ratio_to_Planck"] = ratio_Pl
KEYS["E9_decades_alphaG_1GeV_to_MZ"] = dec_G
KEYS["E9_decades_alphas_1GeV_to_MZ"] = dec_s
KEYS["E9_alpha_s_MZ_1loop"] = alpha_s_MZ
ok_e9 = False
add("E9", "FAIL",
    "**本册最强**：四力「相对强度」是**能标依赖**量 ⟹ 静态几何分区是**范畴错误**",
    "先如实接受对 E6 的反驳：若改令 Ω = k·ln g，则 10³⁹ 跨度只需 Ω 跨越 **%.1f** 个单位 "
    "（而非 10⁻³⁹ 的角精度）⟹ **E6 的精细调参读数在该改法下失效**，故 E6 不自称决定性。"
    "但这条反驳救不了机制，因为被匹配的目标本身就是错的：引力有效耦合 α_G(E) = G·E² 随能标跑动——"
    "由锚点 α_G(1 GeV) = %.1e 反解 α_G = 1 的能标 E★ = %.3e GeV，与 Planck 能标 %.3e GeV 之比为 "
    "**%.4f**（差 6.6%%）⟹ **教科书那张「四力相对强度表」只是 ~GeV 标度的一张快照**。"
    "同一段能标区间（1 GeV → M_Z）内：α_G 涨 **%.2f 个量级**，而 α_s 降 **%.2f 个量级**"
    "（一圈跑动 α_s(M_Z) ≈ %.4f）⟹ **方向相反、幅度悬殊** ⟹ 该表不是基本常数表。"
    "V3.6 公理集**没有能标/跑动概念**，却用**静态**几何分区去匹配一个**能标依赖**的量 ⟹ **范畴错误**。"
    % (omega_span_log, alpha_G_1GeV, E_star, E_Pl, ratio_Pl, dec_G, abs(dec_s), alpha_s_MZ),
    {"Ω 需跨幅度(ln 读法)": omega_span_log, "E★[GeV]": E_star,
     "E★/E_Planck": ratio_Pl, "α_G 涨[量级]": dec_G,
     "α_s 变[量级]": dec_s, "α_s(M_Z)一圈": alpha_s_MZ})

# ============ E7  常数计数：c_T（及 m_τ）与 Ω5 的口径依赖 ============
# Ω5 限定「2 个全局常数」。c_T 无量纲（E1）、m_τ 带量纲（E3）⟹ 是否冲突取决于 Ω5 的限额口径
n_const_orig = 2
n_const_escape = 4                     # 原 2 个 + c_T + m_τ
KEYS["E7_const_before"] = n_const_orig
KEYS["E7_const_after"] = n_const_escape
add("E7", "BOUNDARY",
    "常数计数：与 Ω5 冲突与否**取决于限额口径**，本册不作为决定性依据",
    "动力学挠率至少带入 **c_T（无量纲）+ m_τ（L⁻¹）** 两个新常数 ⟹ 全局常数由 **%d 增至 %d**。"
    "若 Ω5 限额的是**带量纲**常数，则只增 1 个（m_τ），冲突；若限额**全部**常数，则增 2 个，冲突更重。"
    "由于 E1 已证 c_T 无量纲，本册把此项记为 **BOUNDARY**：它是**计数层**的代价，"
    "**不作推翻逃生路线的决定性依据**（决定性依据是 E4 + E6）。"
    % (n_const_orig, n_const_escape),
    {"原常数数": n_const_orig, "逃生后常数数": n_const_escape})

# ============ E8  终局裁定 ============
independent_blockers = ["E4（θ 分区不足：κ≥0 是定义性的，与挠率动力学无关）",
                        "E9（四力相对强度是能标依赖量：静态几何分区是范畴错误）"]
conditional_blocker = "E6（hierarchy 搬运；cos3θ 直接承载强度时致命，ln 读法可规避，见 E9）"
ok_e8 = False
KEYS["E8_independent_blockers"] = independent_blockers
KEYS["E8_conditional_blocker"] = conditional_blocker
add("E8", "FAIL",
    "终局：逃生路线**不救** V3.6；OPEN-MAP 结论由「依赖 M6 的 EC 前提」升级为 **M6-独立**",
    "让步式审计结果：逃生路线在 **E1/E2/E3 三条得分**（量纲不需新带量纲常数、无 Ostrogradsky、"
    "Π 定理封死被解除 ⟹ 上游 M8 需重判），但被 **E4** 与 **E9** 两条**不依赖 EC 前提**的阻塞独立封死："
    "E4 是关于 κ≥0 的**定义性**计数问题，E9 是关于被匹配目标（四力强度比）**本体**的问题，"
    "二者都与挠率是否传播无关。E6 为**条件性**增强项（ln 读法可规避，已如实记于 E9）。"
    "⟹ **即使 M6 被推翻，OPEN-MAP = CLOSED-IMPOSSIBLE 的结论不变**；"
    "分支①终局维持**不可达**；建议维持「放弃 Ω(θ) + 四扇区投影机制」。"
    "⚠️ 本册同时修正上游：M8 在动力学挠率下**需重判**（已记 E3 PASS），"
    "上游判定册应据此加注，但**不影响终局**。",
    {"独立阻塞": independent_blockers, "条件性阻塞": conditional_blocker,
     "M6 仍需重判": False, "终局": "不可达"})

# ---------------- 自检 guard ----------------
GUARDS = []
def guard(name, cond):
    GUARDS.append(dict(name=name, ok=bool(cond)))

guard("本约定下 [Lagrange 密度] = L^-4", D_Lag == {"M": 0, "L": -4, "T": 0})
guard("自检 EH：[1/G]=L^-2 ⟹ [G]=L^2", ddiv(D_Lag, D_R) == {"M": 0, "L": -2, "T": 0})
guard("[(∂T)^2] = L^-4（E1 的根）", D_dTors2 == D_Lag)
guard("E1 判为 c_T 无量纲", ok_e1)
guard("E3 判为自由度增加", ok_e3)
guard("θ 扫描未越出半平面（κ>0 时 atan2 夹逼）", not theta_escape)
guard("半平面符号区间 < 4", n_inter_half < 4)
guard("两套口径的 ρ 跨量级均 >= 30", KEYS["E6_decades_min"] >= 30)
guard("最坏相对精度 < 1e-30", worst_rel < 1e-30)
guard("arccos(ε) ≈ π/2 - ε 数值自检（中心差分斜率≈-1）",
      abs(((math.acos(1e-9) - math.acos(-1e-9)) / (2e-9)) + 1.0) < 1e-6)
guard("E9：对 E6 的 ln 读法反驳成立（Ω 只需跨 O(10^2) 幅度）", ok_refute)
guard("E9：E★ 与 Planck 能标同量级（比值 ∈ [0.5, 2]）", 0.5 <= ratio_Pl <= 2.0)
guard("E9：α_G 从 1GeV 到 M_Z 跨越 > 3 个量级", dec_G > 3.0)
guard("E9：α_s 同期变化 < 1 个量级（与 α_G 形成对照）", abs(dec_s) < 1.0)
guard("判定条目 >= 9", len(VERDICTS) >= 9)

n_pass = sum(1 for v in VERDICTS if v["status"] == "PASS")
n_fail = sum(1 for v in VERDICTS if v["status"] == "FAIL")
n_bnd = sum(1 for v in VERDICTS if v["status"] == "BOUNDARY")
g_ok = sum(1 for g in GUARDS if g["ok"])

out = dict(tag=TAG, verdicts=VERDICTS, guards=GUARDS, key_numbers=KEYS,
           counts=dict(PASS=n_pass, FAIL=n_fail, BOUNDARY=n_bnd,
                       guard_ok=g_ok, guard_total=len(GUARDS)))
with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

L = ["# %s（判定产物）" % TAG, ""]
L.append("计数：PASS %d / FAIL %d / BOUNDARY %d ；自检 %d/%d"
         % (n_pass, n_fail, n_bnd, g_ok, len(GUARDS)))
L.append("")
for v in VERDICTS:
    L.append("## %s [%s] %s" % (v["id"], v["status"], v["title"]))
    L.append(v["detail"]); L.append("")
with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("=" * 78)
print("TUFT V3.6 · ESCAPE-AUDIT · 动力学挠率逃生路线终局审计")
print("=" * 78)
print("计数：PASS %d / FAIL %d / BOUNDARY %d ；自检 %d/%d"
      % (n_pass, n_fail, n_bnd, g_ok, len(GUARDS)))
print("-" * 78)
for v in VERDICTS:
    print("  %-4s %-9s %s" % (v["id"], v["status"], v["title"]))
print("-" * 78)
for k in ["E1_dim_cT", "E3_scales_before", "E3_scales_after",
          "E4_sign_intervals_halfplane", "E4_theta_reached_min",
          "E4_theta_reached_max", "E6_sector_width",
          "E6_worst_relative_precision", "E6_decades_min",
          "E9_omega_span_log", "E9_E_star_GeV", "E9_ratio_to_Planck",
          "E9_decades_alphaG_1GeV_to_MZ", "E9_decades_alphas_1GeV_to_MZ",
          "E9_alpha_s_MZ_1loop",
          "E7_const_before", "E7_const_after"]:
    print("  %-30s %s" % (k, KEYS[k]))
print("-" * 78)
for r in rows_e6:
    print("  口径 %s：Δθ=%.3e  相对精度=%.3e  λ≤%.1e  ρ跨%.0f 量级"
          % (r["口径"], r["Δθ_需"], r["相对扇区宽"], r["λ_需"], r["ρ_跨量级"]))
print("=" * 78)
for g in GUARDS:
    if not g["ok"]:
        print("  [GUARD FAIL] %s" % g["name"])
sys.exit(0 if g_ok == len(GUARDS) else 1)
