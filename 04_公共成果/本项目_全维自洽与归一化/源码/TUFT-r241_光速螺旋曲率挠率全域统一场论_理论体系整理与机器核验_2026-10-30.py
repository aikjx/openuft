# -*- coding: utf-8 -*-
"""TUFT-r241 · 光速螺旋曲率挠率全域统一场论：理论体系整理与机器核验

来料：C:/Users/mo/Downloads 下豆包对话导出（两套各 17 篇 + 一份 5003 行核心方程组）。
受理范围：仅「光速螺旋 + Frenet–Serret 曲率/挠率」体系；按用户指示，
         同批来料中的另一条分支不纳入本册（不整理、不核验、不引用）。

性质：只读整理 + 机器核验。不产生新物理、不修改来料任何字节。
口径：量纲四元组 (M, L, T, Q)，Fraction 精确；数值用 Decimal 60 位。
"""
import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "数据")
NAME = "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30"

# ---------------------------------------------------------------- 量纲工具
def D(m, l, t, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    return tuple(x * Fraction(n) for x in a)

def dstr(a):
    """统一渲染为负指数形式：L^-1、M^1*L^3*T^-2。"""
    sym = ("M", "L", "T", "Q")
    parts = ["%s^%s" % (s, str(e)) for s, e in zip(sym, a) if e != 0]
    return "*".join(parts) if parts else "1"

# 基本量量纲
DIM_C = D(0, 1, -1)
DIM_HBAR = D(1, 2, -1)
DIM_G = D(-1, 3, -2)
DIM_KAPPA = D(0, -1, 0)     # 曲率
DIM_TAU = D(0, -1, 0)       # 挠率
DIM_OMEGA = D(0, 0, -1)     # 角频率
DIM_MASS = D(1, 0, 0)
DIM_FORCE = D(1, 1, -2)
DIM_ENERGY = D(1, 2, -2)
DIM_ENERGY_DENS = D(1, -1, -2)
DIM_LAGR_DENS = D(1, -1, -2)
DIM_EINST_LHS = D(0, -2, 0)  # 爱因斯坦张量量纲

# ---------------------------------------------------------------- 数值常量
def dc(s):
    return Decimal(s)

C_LIGHT = dc("299792458")
HBAR = dc("1.054571817e-34")
G_NEWTON = dc("6.67430e-11")
M_E = dc("9.1093837015e-31")
ALPHA_EXP = dc("7.2973525693e-3")

ENTRIES = []
GUARDS = []

def add(code, status, title, detail, **kw):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail, **kw))

def guard(name, ok, expect, got):
    GUARDS.append(dict(name=name, ok=bool(ok), expect=str(expect), got=str(got)))

def fv(x, n=25):
    """Decimal 定点渲染（避开 quantize 在高位数抛 InvalidOperation）"""
    try:
        return format(Decimal(x), "." + str(n) + "E")
    except Exception:
        return str(x)

def rel(a, b):
    """(a-b)/b"""
    if b == 0:
        return None
    return (Decimal(a) - Decimal(b)) / Decimal(b)

PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")

def two_pi_pow8():
    return (2 * PI) ** 8

# ================================================================ 守卫段 G
# 量纲工具自身必须先过自检（本库纪律：手算量纲必须机器兜底）
guard("G1_dim_kappa_is_Lminus1", dstr(DIM_KAPPA) == "L^-1", "L^-1", dstr(DIM_KAPPA))
guard("G2_dim_hbar_c", dstr(dmul(DIM_HBAR, DIM_C)) == "M^1*L^3*T^-2", "M^1*L^3*T^-2",
      dstr(dmul(DIM_HBAR, DIM_C)))
guard("G3_dim_G", dstr(DIM_G) == "M^-1*L^3*T^-2", "M^-1*L^3*T^-2", dstr(DIM_G))
guard("G4_dim_hbar_over_c_times_kappa_is_mass",
      dstr(dmul(ddiv(DIM_HBAR, DIM_C), DIM_KAPPA)) == "M^1", "M^1",
      dstr(dmul(ddiv(DIM_HBAR, DIM_C), DIM_KAPPA)))
guard("G5_dim_GM_over_c2_is_length",
      dstr(ddiv(dmul(DIM_G, DIM_MASS), dpow(DIM_C, 2))) == "L^1", "L^1",
      dstr(ddiv(dmul(DIM_G, DIM_MASS), dpow(DIM_C, 2))))
guard("G6_dim_omega_squared", dstr(dpow(DIM_OMEGA, 2)) == "T^-2", "T^-2",
      dstr(dpow(DIM_OMEGA, 2)))
guard("G6b_dim_schwarz_over_r2_is_Lminus1",
      dstr(ddiv(ddiv(dmul(DIM_G, DIM_MASS), dpow(DIM_C, 2)),
                dpow(D(0, 1, 0), 2))) == "L^-1", "L^-1",
      dstr(ddiv(ddiv(dmul(DIM_G, DIM_MASS), dpow(DIM_C, 2)), dpow(D(0, 1, 0), 2))))
guard("G7_two_pi_pow8_numeric", abs(two_pi_pow8() - dc("2429063.940114066")) < dc("1e-6"),
      "2429063.940114066", fv(two_pi_pow8(), 12))
guard("G8_alpha_inverse_numeric", abs(1 / ALPHA_EXP - dc("137.035999084")) < dc("1e-6"),
      "137.035999084", fv(1 / ALPHA_EXP, 12))

# ================================================================ 条目段 E
# E01 本源不变式 ω² = c²(κ²+τ²)
lhs01 = dpow(DIM_OMEGA, 2)
rhs01 = dmul(dpow(DIM_C, 2), DIM_KAPPA)  # 与 κ² 同量纲 L^-2，乘 c² 得 T^-2
rhs01 = dmul(dpow(DIM_C, 2), dpow(DIM_KAPPA, 2))
ok01 = lhs01 == rhs01
add("E01", "PASS" if ok01 else "FAIL",
    "本源不变式 ω² = c²(κ²+τ²) 量纲齐次",
    "左端 [%s]，右端 [%s]；与库内 S01/S02 三重奏 κ²+τ²=(ω/c)² 为同一式的两种写法。"
    % (dstr(lhs01), dstr(rhs01)),
    lhs=dstr(lhs01), rhs=dstr(rhs01), note="核心不变式非负新物理（库内已固化）")

# E02 圆柱螺旋恒等式数值对拍
R_EX = dc("1.7")   # 示例半径（任意正量，仅验恒等式）
L_EX = dc("0.9")   # 示例螺距参数（任意正量）
den = R_EX * R_EX + L_EX * L_EX
kappa_t = R_EX / den
tau_t = L_EX / den
sq = (kappa_t * kappa_t + tau_t * tau_t).sqrt()
inv_sq = 1 / den.sqrt()
res02 = abs(sq - inv_sq) / inv_sq
add("E02", "PASS" if res02 < dc("1e-40") else "FAIL",
    "圆柱螺旋 √(κ²+τ²) = 1/√(r₀²+l_h²) 恒等式对拍",
    "示例 r₀=%s、l_h=%s 下两条路径残差 %s（机器零）⇒ 该不变式对圆柱螺旋是【几何恒等式】，"
    "不是新增物理断言；它无法区分任何两种相互作用。"
    % (R_EX, L_EX, fv(res02, 6)),
    kappa_t=fv(kappa_t, 12), tau_t=fv(tau_t, 12), rel=float(res02))

# E03 统一力方程 F = (ℏc/4π)(κn+τb)/√(1+(ω/c)²r²)
prefactor = dmul(DIM_HBAR, DIM_C)            # M L^3 T^-2
with_kappa = dmul(prefactor, DIM_KAPPA)       # M L^2 T^-2 = 能量
denom_dim = dpow(dmul(ddiv(DIM_OMEGA, DIM_C), D(0, 1, 0)), 2)  # (L^-1)^2 = L^-2
denom_dim = dmul(denom_dim, dpow(D(0, 1, 0), 2))               # ×L² ⇒ 无量纲
dimF = with_kappa
gapF = ddiv(dimF, DIM_FORCE)
add("E03", "FAIL",
    "统一力方程左端量纲为能量（J），不是力（N）",
    "ℏc·κ 的量纲 = [%s] = 焦耳；力应为 [%s]。缺口 [%s]（缺一个 L^-1）。"
    "分母 √(1+(ω/c)²r²) 无量纲（自检通过），故问题在前置因子与 κ 的乘积上。"
    "最小修法（不代选）：前置因子乘 1/r（除长度），或把 ℏc 换为 ℏc/r 型核；"
    "在未修好前，该方程的一切「力的大小/方向」读数均无物理单位。"
    % (dstr(dimF), dstr(DIM_FORCE), dstr(gapF)),
    dim_F=dstr(dimF), dim_force=dstr(DIM_FORCE), gap=dstr(gapF),
    denom_dimless=(denom_dim == (0, 0, 0, 0)))

# E04 质量公式 m = (ℏ/c)√(κ²+τ²)
dimM = dmul(ddiv(DIM_HBAR, DIM_C), DIM_KAPPA)
ok04 = dimM == DIM_MASS
add("E04", "PASS" if ok04 else "FAIL",
    "质量公式 m = (ℏ/c)√(κ²+τ²) 量纲正确",
    "量纲 [%s] = 质量 ✓。但与 E=ℏω 配 mc²=ℏω 是同一条的恒等重述（把 ω=c√(κ²+τ²) 代入即得），"
    "与库内 R1/TUFT 已闭合的 m=ℏ√(κ²+τ²)/c 逐字同式 ⇒ 零增量，非负新物理。"
    % dstr(dimM),
    dim=dstr(dimM))

# E05 自旋公式 S = ℏ√(κ²+τ²)/κ 令 S=ℏ/2 ⇒ 无实数解
# √(1+β²) = 1/2 ⇒ β² = -3/4
beta_sq = dc("0.25") - dc("1")
add("E05", "FAIL",
    "自旋 1/2 约束在该自旋式下无实数解（来料自曝，机器确证）",
    "S=ℏ√(κ²+τ²)/κ = ℏ√(1+β²)；令 S=ℏ/2 ⇒ √(1+β²)=1/2 ⇒ 1+β²=1/4 ⇒ β²=%s < 0。"
    "即【该自旋式与自旋 1/2 不相容】。来料在同一篇内据此把自旋式改写成区分切向曲率 κ_t 与"
    "背景曲率 κ 的版本（圆柱螺旋重述），属【被自身矛盾逼出的改写】而非推导。"
    % fv(beta_sq, 6),
    beta_sq=float(beta_sq))

# E06 四维场方程源项 (ℏ/2)(κ²+τ²)u_μu_ν
src = dmul(DIM_HBAR, dpow(DIM_KAPPA, 2))          # M T^-1
rhs06 = dmul(DIM_G, dpow(DIM_C, -4))
rhs06 = dmul(rhs06, src)                          # 乘 8πG/c⁴ 后
need06 = DIM_EINST_LHS
gap06 = ddiv(rhs06, need06)
gap_src = ddiv(src, DIM_ENERGY_DENS)
add("E06", "FAIL",
    "四维统一场方程源项量纲不是能量密度（右端与左端不齐）",
    "源项 (ℏ/2)(κ²+τ²)u_μu_ν 量纲 [%s]，而爱因斯坦方程源位要求的是能量动量张量（能量密度 [%s]），"
    "差 [%s]；乘 8πG/c⁴ 后右端为 [%s]，爱因斯坦张量左端需 [%s]。"
    "⇒ 正确修法是把源项换成【能量密度量纲】的张量，而不是保留 ℏ(κ²+τ²)；"
    "承接：来料自评「量纲是第一道门槛」——本条即该门槛未过。"
    % (dstr(src), dstr(DIM_ENERGY_DENS), dstr(gap_src), dstr(rhs06), dstr(need06)),
    dim_src=dstr(src), dim_rhs=dstr(rhs06), gap=dstr(gap06), gap_src=dstr(gap_src))

# E07 代入质量后源项 4πGm²/(c²ℏ) 与 E06 同源
dim07 = ddiv(dmul(DIM_G, dpow(DIM_MASS, 2)), dmul(dpow(DIM_C, 2), DIM_HBAR))
add("E07", "FAIL",
    "化简源项 4πGm²/(c²ℏ) 与 E06 同缺（内部自洽但同样不齐）",
    "该式量纲 [%s]，与 E06 右端逐位相同 ⇒ 代入质量的化简【保真】，"
    "因此量纲缺陷未被代入操作掩盖，也未被修复。" % dstr(dim07),
    dim=dstr(dim07), same_as_E06=(dim07 == rhs06))

# E08 拉格朗日密度量纲
kin = dmul(dpow(ddiv(DIM_KAPPA, D(0, 1, 0)), 2), D(0, 0, 0, 0))  # (∂κ)² 以长度求导
kin = dpow(ddiv(DIM_KAPPA, D(0, 1, 0)), 2)                        # L^-4
pot = dpow(ddiv(dpow(DIM_OMEGA, 2), dpow(DIM_C, 2)), 2)           # (L^-2)² = L^-4
ok08_internal = kin == pot
gap08 = ddiv(kin, DIM_LAGR_DENS)
add("E08", "FAIL",
    "拉格朗日密度量纲不是能量密度（动能项与势能项彼此齐次，但整体不齐）",
    "动能项 (∂κ)² 与势能项 (ω²/c²−κ²−τ²)² 同为 [%s]（内部齐次 ✓）；"
    "而 4 维拉氏密度须为能量密度 [%s]，缺口 [%s]（缺 ℏc 一类因子）。"
    "⇒ 由它派生的共轭动量 π=κ̇、哈密顿量、以及后续正则量子化的量纲链条整体失效。"
    % (dstr(kin), dstr(DIM_LAGR_DENS), dstr(gap08)),
    dim_L=dstr(kin), gap=dstr(gap08), internal_homogeneous=bool(ok08_internal))

# E09 曲率场动力学方程 □κ + 2(ω²/c² − κ² − τ²)κ = 0
# □κ = ∂_μ∂^μ κ，对长度二阶导：量纲 = [κ]/L² = L^-3（**不是** (κ/r)² = L^-4）
box_kappa = ddiv(DIM_KAPPA, dpow(D(0, 1, 0), 2))      # □κ = ∂²κ/∂x²：L^-3
pot_kappa = dmul(ddiv(dpow(DIM_OMEGA, 2), dpow(DIM_C, 2)), DIM_KAPPA)  # L^-3
gap09 = ddiv(pot_kappa, box_kappa)
add("E09", "PASS" if gap09 == (0, 0, 0, 0) else "FAIL",
    "曲率场动力学方程两项量纲齐次（缺陷在拉氏密度 E08，不在本方程）",
    "□κ=∂²κ/∂x² 量纲 [%s]，2(ω²/c²−κ²−τ²)κ 量纲 [%s]，两者同量纲 ⇒ 方程两项**可相加、量纲齐次**"
    "（本册先版误把 □κ 算作 (κ/r)²=L⁻⁴ 而误判不齐，此处更正）。"
    "注意：该齐次是『拉氏密度 (∂κ)²=L⁻⁴ 经欧拉-拉格朗日后两侧同为 L⁻³』的齐次；"
    "因拉氏密度本身缺 ℏc 因子（E08），整条量子化链仍须补 ℏc 才对应真实能量动量——缺陷在 E08，不在本方程。"
    % (dstr(box_kappa), dstr(pot_kappa)),
    dim_box=dstr(box_kappa), dim_pot=dstr(pot_kappa), ratio=dstr(gap09))

# E10 FRW 方程组：教科书复读
add("E10", "INFO",
    "宇宙学 FRW 方程组为标准弗里德曼方程逐字复读",
    "H²=8πGρ/3−kc²/a²+Λc²/3 与 ä/a=−(4πG/3)(ρ+3P/c²)+Λc²/3 均为教科书标准式；"
    "来料把 Λ 解释为「全局背景螺旋挠率基底」，但方程中 Λ 仍为自由常数，"
    "既未给出 Λ 的数值也未给出由 κ,τ 求 Λ 的式子 ⇒ 解释层进步、方程层零增量。")

# E11 强/弱场方程组：换下标复读
add("E11", "INFO",
    "强、弱两个「场微分方程组」是麦克斯韦组换下标的复读",
    "∇·E_s=ρ_s/ε_s、∇·B_s=0、∇×E_s=−∂B_s/∂t、∇×B_s=μ_s J_s+μ_s ε_s ∂E_s/∂t（弱场同构换 W）。"
    "ε_s、μ_s、ε_W、μ_W 被声明为「几何本征常数」但【未给定义式、未给数值】；"
    "ρ_s/ρ_W（色荷/弱荷密度）与 τ、κ 的映射也未给出 ⇒ 形式齐全而内容为零，不可计算、不可证伪。")

# E12 静态球对称黑洞解
# GM/c² = L；再 /r² ⇒ L^-1
dim_kappa_r = ddiv(ddiv(dmul(DIM_G, DIM_MASS), dpow(DIM_C, 2)), dpow(D(0, 1, 0), 2))
add("E12", "BOUNDARY",
    "无奇点黑洞解：κ(r) 量纲正确，但 λ(r)、τ₀ 未定 ⇒ 结论不可核验",
    "κ(r)=GM e^{−λ(r)}/(c²r²) 量纲 [%s] ✓（曲率）。但 τ(r)=τ₀ e^{−λ(r)}/r 中的 τ₀ 须无量纲且未给；"
    "抑制因子 λ(r) 被声明为「由挠率场决定」却未给方程 ⇒ 循环未定。"
    "「r→0 曲率饱和、无奇点」完全取决于 λ(r) 的形式：若 λ 不发散则 τ∼1/r 本身发散，"
    "与「有限饱和」直接张力 ⇒ 该结论在当前来料内【不可核验】，登记为开放项而非成果。"
    % dstr(dim_kappa_r),
    dim_kappa_r=dstr(dim_kappa_r))

# E13 精细结构常数几何推导：裸值 α₀ = √3/2
r0_claim = HBAR / (2 * M_E * C_LIGHT)          # ℏ/(2 m_e c)
lambda_bar = HBAR / (M_E * C_LIGHT)            # 约化康普顿波长
lambda_C = (2 * PI) * lambda_bar               # 康普顿波长 h/(m_e c)
l_h = (dc("3").sqrt() / 2) * lambda_bar
alpha0 = l_h / ((r0_claim * r0_claim + l_h * l_h).sqrt())
alpha0_exact = dc("3").sqrt() / 2
ratio_alpha = alpha0_exact / ALPHA_EXP
add("E13", "FAIL",
    "精细结构常数几何推导给出裸值 α₀=√3/2≈0.8660，与实验值差 118.7 倍",
    "来料链条：S=m_e c r₀=ℏ/2 ⇒ r₀=ℏ/(2m_ec)=%s m；自洽条件定 l_h=(√3/2)·ℏ/(m_ec)=%s m；"
    "α = l_h/√(r₀²+l_h²) = √3/2 = %s。实验 α=%s ⇒ 比值 %s（差约 %s 倍）。"
    "⇒ 该推导的【几何部分】本身与实验不符，来料随后用屏蔽因子补救（见 E14）。"
    % (fv(r0_claim, 8), fv(l_h, 8), fv(alpha0_exact, 10), fv(ALPHA_EXP, 10),
       fv(ratio_alpha, 10), fv(ratio_alpha, 6)),
    r0=fv(r0_claim, 12), l_h=fv(l_h, 12), alpha0=float(alpha0_exact),
    ratio=float(ratio_alpha))

# E14 屏蔽因子 P₀ 为反解拟合参数
P0 = alpha0_exact / ALPHA_EXP - 1
add("E14", "FAIL",
    "屏蔽因子 P₀ 不是推导量，而是用实验值反解出来的自由参数",
    "来料写 α_obs = α₀/(1+P₀) 并令其等于 1/137.036，反解得 P₀ = α₀/α − 1 = %s。"
    "P₀ 没有独立定义式、没有由 κ,τ 算出的途径、没有能标依赖的定量函数 ⇒ 它是【把实验值塞回去】的旋钮。"
    "这正是来料自己列出的 numerology 判别特征（目标数值已知、反向定系数）。"
    % fv(P0, 10),
    P0=float(P0), alpha0=float(alpha0_exact), alpha_exp=float(ALPHA_EXP))

# E15 康普顿半径命名核验
add("E15", "CORRECTED",
    "「r₀=ℏ/(2m_ec) 正是电子的康普顿半径」——命名不成立",
    "ℏ/(2m_ec) = %s m；约化康普顿波长 ℏ/(m_ec) = %s m；康普顿波长 h/(m_ec) = %s m。"
    "来料值既非康普顿波长、也非约化康普顿波长（恰为其 1/2 与 1/(4π)），"
    "故「正是康普顿半径」的说法须撤回；因 r₀ 直接进 α 表达式，该口径须显式登记。"
    % (fv(r0_claim, 8), fv(lambda_bar, 8), fv(lambda_C, 8)),
    r0=fv(r0_claim, 12), lambda_bar=fv(lambda_bar, 12), lambda_C=fv(lambda_C, 12))

# E16 类光曲线的 Frenet 标架问题（来料自曝）
add("E16", "BOUNDARY",
    "类光世界线套用标准 Frenet–Serret 标架：来料自曝的数学陷阱，未修复",
    "来料的权威自评明确指出：标准 Frenet–Serret 只适用于类时/类空正则曲线，"
    "类光曲线（切矢为零矢量）【没有标准 Frenet 正交标架】，须改用零标架（null frame）重构；"
    "并把它列为「最重要的数学关键点」。但后续全部推导（含质量、自旋、α、黑洞）"
    "仍逐字沿用 ∇_t t=κn 等类时 Frenet 式 ⇒ 该陷阱【被识别而未被处理】，"
    "本册不代为重构，登记为承重开放项。")

# E17 垂直原理：正交性是指派而非推导
add("E17", "INFO",
    "「垂直原理」：Frenet 标架正交是构造性质，E/B 的归属是指派 ⇒ 零判别力",
    "t⊥n⊥b 是 Frenet 标架的定义性构造（正交标架本来就这么造），并非该理论推出的结论；"
    "把电场沿 b、磁场力沿 t×b 是【字典指派】，换任意正交标架同样成立。"
    "⇒ 电磁学正交关系在此得到的是「重述」而非「推导」，对任何两种相互作用无区分力。")

# E18 回溯兼容检验（来料自定判据第 2 条）未执行
add("E18", "FAIL",
    "来料自定的「回溯兼容」入门检验（弱场退化为史瓦西）从未执行",
    "来料《权威层面分析》自列理论体系成立四判据，其中第 2 条为「弱场/低能极限平滑还原 GR」；"
    "并在任务清单任务 2 写明「输出度规、检验远场是否退化为史瓦西度规，不通过则无法描述普通星体引力」。"
    "本册逐篇检索：后续篇章给出的是 FRW 方程组与「无奇点黑洞」ansatz，"
    "【没有】给出静态球对称弱场解、也【没有】做史瓦西远场比对 ⇒ 该自定门槛处于未执行状态。")

# E19 能量条件检验（来料自列风险）未执行
add("E19", "BOUNDARY",
    "能量条件（NEC/SEC）检验：来料自列为核心风险，同样未执行",
    "来料自评「很多几何引力模型在这里违反能量条件，造成病态物理解」，但未做该项计算。"
    "在本册 E06/E07 已判源项量纲不齐的前提下，能量条件检验【无法开始】（量纲未定时无从判正负）"
    "⇒ 该风险项既不通过也不解除，登记为阻塞依赖。")

# E20 外部输入账
free_items = ["ε_s", "μ_s", "ε_W", "μ_W", "ρ_s", "ρ_W", "P₀(μ)", "τ₀", "λ(r)", "Λ", "m(κ,τ 标度)"]
add("E20", "FAIL",
    "外部输入/自由量清单与「无拟合、无凑数、无人工参数」的自评冲突",
    "本册清点来料中【已声明但无定义式、无数值、无来源】的量，共 %d 项：%s。"
    "其中 P₀ 用于把 α 调回实验值、τ₀/λ(r) 决定黑洞是否无奇点、ε/μ 三族决定强弱耦合强度 —— "
    "均为理论输出的关键旋钮。⇒「唯一核心方程、无自由参数」的表述与方程集的实际自由度内容不符，须登记。"
    % (len(free_items), "、".join(free_items)),
    count=len(free_items), items=free_items)

# E21 与库内既有体系的同源性
add("E21", "INFO",
    "核心两式与本库既有体系同源：非负新物理",
    "① ω²=c²(κ²+τ²) ⇔ 本库 S01/S02 螺旋三重奏 κ²+τ²=(ω/c)²（同一式的两种写法，已固化多册）；"
    "② m=(ℏ/c)√(κ²+τ²) ⇔ 本库 R1/TUFT 已闭合的 m=ℏ√(κ²+τ²)/c（由 E=ℏω 与质能关系直接等价）。"
    "⇒ 本册可核验的【正面】部分全部落在库内既有读数上；本册新增的是量纲与闭合性读数，不是新方程。")

# E22 可证伪预言清点
claims = ["无奇点黑洞（λ(r) 未定）", "暗物质挠率晕（无旋转曲线数值）",
          "α 能标跑动（P(μ) 无函数形式）", "大统一固定点（无能标/无耦合值）",
          "粒子质量谱（κ,τ 逐粒子未给）", "自旋几何（式与 1/2 不相容）",
          "哈勃张力（未算）"]
add("E22", "FAIL",
    "可证伪预言清点：7 条宣称，0 条带可算数值",
    "逐条清点来料宣称的可验证输出：%s。"
    "全部缺少「代入即出数」的闭合链条 ⇒ 当前可证伪预言数为 0。"
    "按本库既有口径，这等价于该体系仍处于【数学构想 / 玩具模型】档（来料情景 B 的自评与此一致）。"
    % "；".join(claims),
    claims=claims, n_claim=len(claims), n_falsifiable=0)

# ================================================================ E23 来料完整性扫描
SRC_DIR = r"C:/Users/mo/Downloads"
TARGET_HEADS = ["螺旋几何本征关系", "统一场动力学核心方程", "频率", "低维投影约化方程",
                "跑动耦合演化基础式"]

def scan_formula_loss():
    """统计来料导出件中「核心动力学方程组」5 个小节公式被剥离的情况。"""
    hits, miss, files_scanned = 0, 0, 0
    detail = []
    if not os.path.isdir(SRC_DIR):
        return hits, miss, files_scanned, detail
    for fn in sorted(os.listdir(SRC_DIR)):
        if not fn.endswith(".md"):
            continue
        files_scanned += 1
        try:
            txt = io.open(os.path.join(SRC_DIR, fn), "r", encoding="utf-8",
                          errors="replace").read()
        except Exception:
            continue
        lines = txt.splitlines()
        for i, ln in enumerate(lines):
            s = ln.strip()
            if not s.startswith("#"):
                continue
            if not any(h in s for h in TARGET_HEADS):
                continue
            body = []
            for nxt in lines[i + 1:]:
                if nxt.strip().startswith("#"):
                    break
                body.append(nxt)
            seg = "\n".join(body).strip()
            # 判据：小节正文去掉中文后是否仍含 ASCII 字母/数字（公式痕迹）
            ascii_part = "".join(ch for ch in seg if ord(ch) < 128)
            has_formula = any(ch.isalnum() for ch in ascii_part)
            hits += 1
            if not has_formula:
                miss += 1
                detail.append("%s :: %s" % (fn, s.lstrip("#").strip()))
    return hits, miss, files_scanned, detail

_h, _m, _f, _d = scan_formula_loss()
add("E23", "BOUNDARY",
    "来料完整性：标题为「核心动力学方程组」的章节在导出件中公式被剥离",
    "扫描 %d 份导出件，命中目标小节 %d 处，其中 %d 处正文【不含任何公式痕迹】（仅剩中文叙述）。"
    "⇒ 该章节（公理层方程组：螺旋本征关系 / 动力学核心方程 / ω-κ-τ 约束 / 低维投影 / 跑动耦合）"
    "在导出件内【文本性缺失】，本册能核验的公式来自同一对话其它篇保留的 LaTeX 版本。"
    "整理册据此把「方程组正文」标为来料缺口，不代为补写。" % (_f, _h, _m),
    files=_f, sections=_h, missing=_m, samples=_d[:8])

# ================================================================ 输出
def main():
    counts = {}
    for e in ENTRIES:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])
    lines = []
    lines.append("TUFT-r241 · 光速螺旋曲率挠率全域统一场论 · 理论体系整理与机器核验")
    lines.append("=" * 78)
    for e in ENTRIES:
        lines.append("[%s] %s · %s" % (e["status"], e["code"], e["title"]))
        lines.append("    %s" % e["detail"])
    lines.append("-" * 78)
    lines.append("守卫 %d/%d" % (g_ok, len(GUARDS)))
    for g in GUARDS:
        if not g["ok"]:
            lines.append("  [GUARD FAIL] %s expect=%s got=%s" % (g["name"], g["expect"], g["got"]))
    summary = ("条目 %d  PASS=%d FAIL=%d BOUNDARY=%d CORRECTED=%d INFO=%d"
               % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                  counts.get("BOUNDARY", 0), counts.get("CORRECTED", 0),
                  counts.get("INFO", 0)))
    lines.append(summary)
    lines.append("守卫 %d/%d" % (g_ok, len(GUARDS)))
    lines.append("退出码 0")
    txt = "\n".join(lines)
    print(txt)

    payload = dict(
        round="r241",
        title="光速螺旋曲率挠率全域统一场论：理论体系整理与机器核验",
        date="2026-10-30",
        source="C:/Users/mo/Downloads 豆包对话导出（光速螺旋体系部分）",
        entries=ENTRIES,
        guards=GUARDS,
        counts=counts,
        summary=summary,
        key_numbers=dict(
            alpha0=float(alpha0_exact), alpha_exp=float(ALPHA_EXP),
            ratio_alpha0_over_alpha=float(ratio_alpha), P0=float(P0),
            r0_claim_m=float(r0_claim), lambda_bar_m=float(lambda_bar),
            lambda_C_m=float(lambda_C), l_h_m=float(l_h),
            formula_sections=_h, formula_missing=_m, files_scanned=_f,
        ),
        scope_excluded="同批来料中另一条分支按用户指示不纳入（不整理、不核验、不引用）",
    )
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    with io.open(os.path.join(OUT, NAME + ".json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
    with io.open(os.path.join(OUT, NAME + ".md"), "w", encoding="utf-8") as fh:
        fh.write("# %s\n\n" % payload["title"])
        fh.write("```\n%s\n```\n" % txt)
    with io.open(os.path.join(OUT, NAME + "_report.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
