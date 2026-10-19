# -*- coding: utf-8 -*-
"""
TUFT-r110 · α = 1/137.036 的几何身份 —— 四重断言全维审计（2026-10-19）

来料主张：α 有「四重身份」，全部精确相等、残差 ~1e-44：
  1. 长度比（填充比）  α = r_e/λ_C = λ_C/a_0
  2. 速度比            α = v_e/c, v_e = αc ≈ 2.19e6 m/s
  3. 扭转角（TUFT 新发现）τ_e(λ_C) × λ_C = √α ≈ 0.0854 rad ≈ 4.9°，
     且「这个角的正弦等于 √α」
  4. 三个长度层级      r_e = α λ_C = α² a_0
并否定三个猜想：曲率/挠率比 = 3/2、引力/电磁力比 = 4.17e42、引力挠率/电磁挠率 = 2.04e21。

本册只做机器可算的判定：
  - 每条恒等式做「定义式自洽路径」与「公开字面值路径」双路对拍；
  - 对「新发现」条目做定义域/口径/互斥性判定，不自造公式、不代选修法；
  - 所有量纲断言由 Fraction 四元组 (M,L,T,Q) 机器给出（本库纪律：手算量纲必错）。

纯标准库；Decimal 60 位；三角函数自实现（Decimal 无 sin/cos/asin）。
"""

import sys
import os
import json
from decimal import Decimal as D, getcontext
from fractions import Fraction as FR

getcontext().prec = 60

# ---------------------------------------------------------------- 输出守卫
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DATA = os.path.join(BASE, "数据")

# ---------------------------------------------------------------- CODATA（库内口径）
C = D("299792458")
HBAR = D("1.054571817E-34")
E_CH = D("1.602176634E-19")
EPS0 = D("8.8541878128E-12")
ALPHA = D("7.2973525693E-3")
M_E = D("9.1093837015E-31")
G_N = D("6.67430E-11")

# 公开字面值（独立取位，用于「字面路径」对拍）
R_E_LIT = D("2.8179403262E-15")
LAMC_LIT = D("3.8615926796E-13")      # 约化康普顿波长 ħ/(m_e c)
A0_LIT = D("5.29177210903E-11")
LAMC_BAR_LIT = D("2.42631023867E-12")  # 非约化康普顿波长 h/(m_e c)

# ---------------------------------------------------------------- 三角函数（Decimal 自实现）
def datan(x):
    """|x| < 1 的反正切级数（对 1/5、1/239 收敛极快）。"""
    x = D(x)
    term = x
    total = x
    n = 1
    xx = x * x
    while True:
        term = -term * xx
        t = term / D(2 * n + 1)
        if t == 0:
            break
        total += t
        n += 1
        if n > 400:
            break
    return total

PI = 16 * datan(D(1) / D(5)) - 4 * datan(D(1) / D(239))

def dsin(x):
    x = D(x)
    total = x
    term = x
    xx = x * x
    n = 1
    while True:
        term = -term * xx / D((2 * n) * (2 * n + 1))
        if term == 0:
            break
        total += term
        n += 1
        if n > 200:
            break
    return total

def dcos(x):
    x = D(x)
    total = D(1)
    term = D(1)
    xx = x * x
    n = 1
    while True:
        term = -term * xx / D((2 * n - 1) * (2 * n))
        if term == 0:
            break
        total += term
        n += 1
        if n > 200:
            break
    return total

def dasin(x):
    """反正弦级数 asin x = Σ a_n x^(2n+1)，a_n = C(2n,n)/(4^n(2n+1))，
    系数用递推 a_n/a_{n-1} = (2n-1)^2 / (2n(2n+1)) 生成到 x^49。
    （初版只写到 x^13，截断误差 1.5e-17，被 G0-5 守卫当场拦下。）"""
    x = D(x)
    if abs(x) > D("0.9"):
        raise ValueError("dasin 仅用于小数域")
    total = x
    term = x
    xx = x * x
    a = D(1)
    for n in range(1, 25):
        a = a * D((2 * n - 1) * (2 * n - 1)) / D(2 * n * (2 * n + 1))
        term = term * xx
        t = a * term
        if t == 0:
            break
        total += t
    return total

def dsqrt(x):
    return D(x).sqrt()

def deg(rad):
    return D(rad) * D(180) / PI

# ---------------------------------------------------------------- 量纲（Fraction 四元组 M,L,T,Q）
def dmul(a, b):
    return tuple(a[i] + b[i] for i in range(4))

def ddiv(a, b):
    return tuple(a[i] - b[i] for i in range(4))

def dpow(a, k):
    k = FR(k)
    return tuple(a[i] * k for i in range(4))

def dstr(a):
    names = ["M", "L", "T", "Q"]
    out = []
    for i in range(4):
        v = a[i]
        if v == 0:
            continue
        s = names[i]
        if v != 1:
            s += "^" + str(v)
        out.append(s)
    return "1" if not out else "·".join(out)

DIM_L = (FR(0), FR(1), FR(0), FR(0))
DIM_T = (FR(0), FR(0), FR(1), FR(0))
DIM_M = (FR(1), FR(0), FR(0), FR(0))
DIM_Q = (FR(0), FR(0), FR(0), FR(1))
DIM_1 = (FR(0), FR(0), FR(0), FR(0))

DIM_HBAR = dmul(dmul(DIM_M, dpow(DIM_L, 2)), ddiv(DIM_1, DIM_T))   # M L^2 T^-1
DIM_C = ddiv(DIM_L, DIM_T)                                          # L T^-1
DIM_EPS0 = ddiv(dmul(dpow(DIM_Q, 2), dpow(DIM_T, 2)),
                dmul(DIM_M, dpow(DIM_L, 3)))                        # Q^2 T^2 M^-1 L^-3

# ---------------------------------------------------------------- 条目登记
ENTRIES = []
GUARDS = []

def add(code, status, title, detail, evidence=None):
    ENTRIES.append({
        "code": code, "status": status, "title": title,
        "detail": detail, "evidence": evidence or {},
    })

def guard(name, cond, info=""):
    GUARDS.append({"name": name, "ok": bool(cond), "info": info})

def rel(a, b):
    """相对偏差 |a-b|/|b|"""
    a, b = D(a), D(b)
    if b == 0:
        return None
    return abs(a - b) / abs(b)

def fv(x, n=25):
    try:
        return format(D(x), "." + str(n) + "E")
    except Exception:
        return str(x)

# ---------------------------------------------------------------- 守卫自检（工具本身必须先过检）
_PI_REF = D("3.14159265358979323846264338327950288419716939937510582097494")
guard("G0-1 高精度 PI 与参照值一致", rel(PI, _PI_REF) < D("1E-50"),
      "PI=%s" % fv(PI))
guard("G0-2 dsin(0)=0", dsin(D(0)) == 0)
guard("G0-3 dsin(PI/6)=1/2", rel(dsin(PI / D(6)), D("0.5")) < D("1E-50"),
      "sin(pi/6)=%s" % fv(dsin(PI / D(6))))
guard("G0-4 dcos(0)=1", dcos(D(0)) == 1)
_xg = D("0.0854245431319360349553926362839858118936482871632080460623179")
guard("G0-5 dasin(dsin(x))=x 自洽（小数域，级数生成至 x^49）",
      rel(dasin(dsin(_xg)), _xg) < D("1E-40"),
      "asin(sin(x))=%s 实测残差=%s（截断误差远小于本册最小判据 1.2e-3）"
      % (fv(dasin(dsin(_xg))), fv(rel(dasin(dsin(_xg)), _xg))))
guard("G0-6 [hbar]=M L^2 T^-1", dstr(DIM_HBAR) == "M·L^2·T^-1", dstr(DIM_HBAR))
guard("G0-7 [hbar/(m_e c)]=L",
      dstr(ddiv(DIM_HBAR, dmul(DIM_M, DIM_C))) == "L",
      dstr(ddiv(DIM_HBAR, dmul(DIM_M, DIM_C))))
guard("G0-8 [alpha]=1（无量纲）",
      dstr(ddiv(dmul(dpow(DIM_Q, 2), DIM_1),
                dmul(DIM_EPS0, dmul(DIM_HBAR, DIM_C)))) == "1",
      dstr(ddiv(dpow(DIM_Q, 2), dmul(DIM_EPS0, dmul(DIM_HBAR, DIM_C)))))
guard("G0-9 [tau*lambda_C]=1 当 [tau]=L^-1",
      dstr(dmul(ddiv(DIM_1, DIM_L), DIM_L)) == "1")
guard("G0-10 度转换 180/pi 自洽", rel(deg(PI), D(180)) < D("1E-50"))

# ================================================================ A 段 α 不是什么
SQRT_A = ALPHA.sqrt()

F_E_EE = (E_CH * E_CH) / (D(4) * PI * EPS0 * LAMC_LIT) if False else None
# 电子-电子：F_E/F_G = (e^2/(4 pi eps0)) / (G m_e^2) = alpha*hbar*c/(G m_e^2)
FE_FG = (ALPHA * HBAR * C) / (G_N * M_E * M_E)
FG_FE = 1 / FE_FG
SQRT_FE_FG = FE_FG.sqrt()

add("A01", "INFO",
    "猜想甲「曲率/挠率比 = 3/2」确不等于 α，但 3/2 来源未声明",
    "机器比对 3/2=1.5 与 α=%s：比值 %s（差 %s 倍）。来料否定方向正确；"
    "但「曲率/挠率比」的定义式与所属几何均未给出，3/2 属未溯源常量 [C]，"
    "故本条只能判「所举数值 ≠ α」，不能判「曲率挠率比不是 α 的身份」。"
    % (fv(ALPHA), fv(D("1.5") / ALPHA), fv(D("1.5") / ALPHA)),
    {"ratio_3_2_over_alpha": fv(D("1.5") / ALPHA)})

add("A02", "CORRECTED",
    "猜想乙数值对、标签方向反：4.17e42 是「电磁/引力」比，不是「引力/电磁」比",
    "电子-电子静电力/引力 = αħc/(G m_e²) = %s；其倒数（真·引力/电磁）= %s。"
    "来料写「引力/电磁力比 4.17×10⁴²」，实为电磁/引力比 = %s（相对偏差 %s）。"
    "⇒ 数值正确、标签反向：来料值与真·引力/电磁比 %s 互为倒数。把 4.17e42 读成"
    "「引力比电磁大」会把图像完全颠倒 —— 实为【电磁比引力大 42 个数量级】。"
    % (fv(FE_FG), fv(FG_FE), fv(FE_FG), fv(rel(FE_FG, D("4.17E42"))),
       fv(FG_FE)),
    {"FE_over_FG": fv(FE_FG), "FG_over_FE": fv(FG_FE),
     "claim": "4.17E42", "direction": "reverse"})

add("A03", "CORRECTED",
    "猜想丙同样是反向：2.04e21 = √(电磁/引力比)，且隐含「力 ∝ 挠率²」未声明",
    "√(αħc/(G m_e²)) = %s，与来料 2.04e21 相对偏差 %s ⇒ 来料值为 √(电磁/引力) 同向；"
    "若真按字面「引力挠率/电磁挠率」应为 %s。另：由「力比 = (挠率比)²」反推的"
    "指数关系（力 ∝ 挠率²）来料未声明，属隐含外部输入 [C]。"
    % (fv(SQRT_FE_FG), fv(rel(SQRT_FE_FG, D("2.04E21"))), fv(1 / SQRT_FE_FG)),
    {"sqrt_FE_over_FG": fv(SQRT_FE_FG), "inverse": fv(1 / SQRT_FE_FG)})

add("A04", "PASS",
    "来料两个数同源：2.04e21² 与 4.17e42 逐位自洽，非两条独立证据",
    "(%s)² = %s，与 %s 相对偏差 %s ⇒ 猜想乙、丙是同一个数的两种写法，"
    "「三条否定」的信息量实为 1 条。"
    % (fv(SQRT_FE_FG), fv(SQRT_FE_FG * SQRT_FE_FG), fv(FE_FG),
       fv(rel(SQRT_FE_FG * SQRT_FE_FG, FE_FG))),
    {"square_check": fv(rel(SQRT_FE_FG * SQRT_FE_FG, FE_FG))})

# 阳性对照：检验器能识别「相等」的情形
_pos = rel(ALPHA, ALPHA)
guard("A-POS 检验器非恒真（同值比较判相等）", _pos == 0)

_kappa_over_tau = D(3) / D(2)                 # 来料自称的曲率/挠率比
_tau_over_kappa = 1 / _kappa_over_tau
_sin_theta_A06 = _tau_over_kappa / (1 + _tau_over_kappa * _tau_over_kappa).sqrt()
_alpha_pred_A06 = _sin_theta_A06 * _sin_theta_A06
add("A06", "BOUNDARY",
    "条件性内部冲突：若 3/2 真是该体系的 κ/τ，则与第 3 条公式联立预言 α=4/13",
    "取 κ/τ=3/2 ⇒ sinθ = τλ_C = 2/√13 = %s；代入来料自己的第 3 条 α=(τλ_C)² "
    "⇒ α_pred = 4/13 = %s，与真值 %s 差 %s 倍。⇒ 来料 A 段与 B 段第 3 条在同一几何"
    "内互斥（条件性：3/2 未溯源，本册不代认其为该体系口径）。"
    % (fv(_sin_theta_A06), fv(_alpha_pred_A06), fv(ALPHA),
       fv(_alpha_pred_A06 / ALPHA)),
    {"sin_theta": fv(_sin_theta_A06), "alpha_pred": fv(_alpha_pred_A06),
     "mismatch_times": fv(_alpha_pred_A06 / ALPHA)})

# ================================================================ B 段 四重身份
# --- 第 1 条：长度比（双路对拍）
R_E_DEF = ALPHA * HBAR / (M_E * C)          # 定义式路径
LAMC_DEF = HBAR / (M_E * C)
A0_DEF = HBAR / (M_E * C * ALPHA)

r1_def = R_E_DEF / LAMC_DEF                  # 应恒等 = α
r1_lit = R_E_LIT / LAMC_LIT                  # 字面路径
r2_def = LAMC_DEF / A0_DEF
r2_lit = LAMC_LIT / A0_LIT

add("B01", "CORRECTED",
    "第 1 条 α=r_e/λ_C 是定义式恒等复读；声称的「残差 1e-44」不成立",
    "定义式路径 r_e=αħ/(m_ec)、λ_C=ħ/(m_ec) ⇒ 比值恒等于 α，残差 %s（机器零，"
    "因两式共用同一组符号，非实验验证）；改用各自公开字面值（r_e=%s、λ_C=%s）"
    "⇒ 比值 %s，与 α 相对偏差 %s。⇒ 来料「残差 ~10⁻⁴⁴」在两种口径下都不成立："
    "恒等式残差是 0，字面值残差是 10⁻¹² 量级（取决于取位），1e-44 无从产生。"
    % (fv(rel(r1_def, ALPHA)), fv(R_E_LIT), fv(LAMC_LIT), fv(r1_lit),
       fv(rel(r1_lit, ALPHA))),
    {"def_path_resid": fv(rel(r1_def, ALPHA)), "lit_path_resid": fv(rel(r1_lit, ALPHA)),
     "lit_value": fv(r1_lit)})

add("B02", "CORRECTED",
    "第 1 条后半 α=λ_C/a_0 同为恒等复读，字面残差 5.1e-13",
    "a_0=ħ/(m_ecα) ⇒ λ_C/a_0 ≡ α（定义路径残差 %s）；字面路径 %s，相对偏差 %s。"
    % (fv(rel(r2_def, ALPHA)), fv(r2_lit), fv(rel(r2_lit, ALPHA))),
    {"def_path_resid": fv(rel(r2_def, ALPHA)), "lit_path_resid": fv(rel(r2_lit, ALPHA))})

add("B03", "BOUNDARY",
    "λ_C 口径未声明：来料取约化康普顿波长，换非约化口径则第 1 条立刻崩 6.28 倍",
    "来料 λ_C=3.86e-13 m 是约化值 ħ/(m_ec)=%s；若按教科书「康普顿波长」h/(m_ec)=%s，"
    "则 r_e/λ_C = α/(2π) = %s，与 α 差 %s 倍 ⇒ 该恒等式对口径敏感，来料未声明。"
    % (fv(LAMC_DEF), fv(LAMC_BAR_LIT), fv(R_E_LIT / LAMC_BAR_LIT),
       fv(ALPHA / (R_E_LIT / LAMC_BAR_LIT))),
    {"reduced": fv(LAMC_DEF), "nonreduced": fv(LAMC_BAR_LIT),
     "ratio_nonreduced": fv(R_E_LIT / LAMC_BAR_LIT)})

# --- 第 2 条：速度比
V_E = ALPHA * C
add("B04", "BOUNDARY",
    "第 2 条 α=v_e/c 数值正确，但它是玻尔模型氢基态的教科书导出，非电子普适属性",
    "αc = %s m/s，来料 2.19e6 ✓（相对偏差 %s）。但：①v₁=αc 是氢原子基态在玻尔模型"
    "下的结果（第 n 态 v_n=αc/n，其它核为 Zαc/n），把它写成「电子的速度」会失真；"
    "②α 由 e、ε₀、ħ、c 定义在先，v=αc 是导出，方向是 α→v 不是 v→α ⇒ 对 α 的数值"
    "零约束；③真实氢原子无确定轨道速度（量子力学），该式只在玻尔模型内成立。"
    % (fv(V_E), fv(rel(V_E, D("2.19E6")))),
    {"v_e": fv(V_E), "claim": "2.19E6", "resid_vs_claim": fv(rel(V_E, D("2.19E6")))})

# --- 第 3 条：扭转角（来料自称 TUFT 新发现）
SIN_SQRT_A = dsin(SQRT_A)
ASIN_SQRT_A = dasin(SQRT_A)
d_sin_vs_sqrt = rel(SIN_SQRT_A, SQRT_A)
d_asin_vs_sqrt = rel(ASIN_SQRT_A, SQRT_A)
d_sin_vs_asin = rel(SIN_SQRT_A, ASIN_SQRT_A)

add("B05", "FAIL",
    "第 3 条内部互斥：同一句内「扭转角 = √α」与「该角的正弦 = √α」不能同时成立",
    "√α = %s；sin(√α) = %s；asin(√α) = %s rad = %s°。三者两两不等："
    "|sin(√α)−√α|/√α = %s（≈ α/6），|asin(√α)−√α|/√α = %s。"
    "⇒ 若「扭转 4.9°」指角本身 = √α，则 sin(角) = %s ≠ √α；若指 sin(角)=√α，"
    "则角 = %s rad = %s° ≠ √α。来料叙事自称残差 1e-44，而此处自相矛盾达 1.2e-3，"
    "相差 41 个数量级。这是可零成本修复的笔误，但两种读法给出两个不同的预言，"
    "必须先择一（本册不代选）。"
    % (fv(SQRT_A), fv(SIN_SQRT_A), fv(ASIN_SQRT_A), fv(deg(ASIN_SQRT_A)),
       fv(d_sin_vs_sqrt), fv(d_asin_vs_sqrt), fv(SIN_SQRT_A),
       fv(ASIN_SQRT_A), fv(deg(ASIN_SQRT_A))),
    {"sqrt_alpha": fv(SQRT_A), "sin_sqrt_alpha": fv(SIN_SQRT_A),
     "asin_sqrt_alpha": fv(ASIN_SQRT_A), "asin_deg": fv(deg(ASIN_SQRT_A)),
     "sqrt_alpha_deg": fv(deg(SQRT_A)),
     "resid_sin_vs_sqrt": fv(d_sin_vs_sqrt), "resid_asin_vs_sqrt": fv(d_asin_vs_sqrt),
     "resid_sin_vs_asin": fv(d_sin_vs_asin),
     "theoretical_alpha_over_6": fv(ALPHA / D(6))})

guard("B05-G 三种读法必须两两不等（检验器非恒真）",
      d_sin_vs_sqrt > D("1E-6") and d_asin_vs_sqrt > D("1E-6")
      and d_sin_vs_asin > D("1E-6"))

# τ_e 反解与三种自然定义
TAU_E_BACK = SQRT_A / LAMC_DEF               # 若 τ λ_C = √α 成立所需的 τ
TORS_LEN = 1 / TAU_E_BACK

_candidates = []
# (a) 每 Compton 波长转一圈
_candidates.append(("tau=2*pi/lambda_C（每波长一整圈）", D(2) * PI / LAMC_DEF))
# (b) 挠率 = 1/λ_C
_candidates.append(("tau=1/lambda_C", 1 / LAMC_DEF))
# (c) 由 κ²+τ²=1/λ_C² 且 τ/κ=α（库内常见口径）
_s = ALPHA / (1 + ALPHA * ALPHA).sqrt()
_candidates.append(("tau/κ=α 且 κ²+τ²=(1/λ_C)²", _s / LAMC_DEF))

_cand_lines = []
for _nm, _t in _candidates:
    _x = _t * LAMC_DEF
    _ap = _x * _x
    _cand_lines.append("%s ⇒ τλ_C=%s ⇒ 按来料公式预言 α=%s（为真值的 %s 倍）"
                       % (_nm, fv(_x), fv(_ap), fv(_ap / ALPHA)))

add("B06", "FAIL",
    "第 3 条不可证伪：τ_e 无定义式，三种自然定义给出的 α 预言全部落空",
    "来料未给 τ_e(λ_C) 的定义式，故该断言当前不可核验、不可证伪（[C] 外部输入）。"
    "反解：若 τλ_C=√α 成立，则 τ_e = √α/λ_C = %s m⁻¹（扭转长度 1/τ = %s m = %s λ_C）。"
    "代入三种最自然的 τ 定义：%s。⇒ 三条全部给出错值，说明 τ_e 只能被「反解定义」，"
    "即该式不是预言而是命名。"
    % (fv(TAU_E_BACK), fv(TORS_LEN), fv(TORS_LEN / LAMC_DEF), "；".join(_cand_lines)),
    {"tau_e_backsolve": fv(TAU_E_BACK), "torsion_length_m": fv(TORS_LEN),
     "torsion_length_over_lamC": fv(TORS_LEN / LAMC_DEF),
     "candidates": _cand_lines})

# --- 与 τ/κ = α 口径的代数互斥定理
_min_lhs = None
for _k in range(1, 2001):
    _a = D(_k) / D(2000)
    _v = _a + 1 / _a
    if _min_lhs is None or _v < _min_lhs:
        _min_lhs = _v
add("B07", "FAIL",
    "互斥定理：来料第 3 条与「α=τ/κ」口径在任何 α 下都不能同时成立（无实解）",
    "设 x≡τλ_C、y≡κλ_C，库内几何恒等式 κ²+τ²=(ω/c)²=1/λ_C² 给出 x²+y²=1。"
    "来料第 3 条给出 x=√α ⇒ y=√(1−α)；若同时要求 τ/κ=x/y=α，则 y=x/α=1/√α，"
    "联立得 α+1/α=1。而 α>0 时 α+1/α ≥ 2（机器扫描 α∈(0,1] 最小值 = %s），"
    "故方程无实解（等价 α²−α+1=0，判别式 −3<0）。⇒ 两口径代数互斥，与 α 取值无关，"
    "本册不代选谁对，但二者不可并引。"
    % (fv(_min_lhs)),
    {"min_of_alpha_plus_inv": fv(_min_lhs), "discriminant": "-3",
     "equation": "alpha^2 - alpha + 1 = 0"})

guard("B07-G α+1/α 在 (0,1] 的最小值须 ≥ 2", _min_lhs >= D(2))

# --- 与 A 段 3/2 的联立冲突（第 3 条自洽版）
_y = (1 - ALPHA).sqrt()
_cot = _y / SQRT_A
add("B08", "BOUNDARY",
    "第 3 条自洽版给出 κ/τ = √((1−α)/α) = 11.66，与 A 段自称的 κ/τ=3/2 差 7.8 倍",
    "由 x²+y²=1 且 x=√α ⇒ y=κλ_C=√(1−α)=%s ⇒ κ/τ=y/x=%s。来料 A 段称曲率/挠率比"
    "为 3/2，二者相差 %s 倍 ⇒ 若 3/2 属同一体系，则来料前后两段互相否证"
    "（条件性：3/2 未溯源）。"
    % (fv(_y), fv(_cot), fv(_cot / (D(3) / D(2)))),
    {"kappa_lamC": fv(_y), "kappa_over_tau": fv(_cot),
     "vs_3_2": fv(_cot / (D(3) / D(2)))})
# ================================================================ C 段 零信息量与计数
# C01：零判别力定理 —— 把 α 换成任意值，第 1 条仍然「精确成立」
_alphas = [ALPHA, D("0.01"), D("0.02"), D("0.05"), D("0.5"), D("0.9")]
_zero_rows = []
for _ap in _alphas:
    _re = _ap * HBAR / (M_E * C)
    _a0 = HBAR / (M_E * C * _ap)
    _q1 = _re / LAMC_DEF          # 应为 α'
    _q2 = LAMC_DEF / _a0          # 应为 α'
    _q3 = _re / _a0               # 应为 α'^2（阳性对照，不应等于 α'）
    _zero_rows.append((fv(_ap), fv(rel(_q1, _ap)), fv(rel(_q2, _ap)),
                       fv(_q3 / _ap)))
_max_resid = max(max(D(_r[1]), D(_r[2])) for _r in _zero_rows)
guard("C01-G 换 α 后第 1 条仍恒等（残差机器零）",
      _max_resid < D("1E-50"),
      "max_resid=%s rows=%d" % (fv(_max_resid), len(_zero_rows)))
guard("C01-G2 阳性对照：r_e/a_0 不等于 α（检验器非恒真）",
      all(abs(D(_r[3]) - 1) > D("1E-6") for _r in _zero_rows if D(_r[0]) != D("1")))

add("C01", "FAIL",
    "零判别力定理：第 1、2、4 条对 α 的数值零约束 —— 换任何 α 都「精确成立」",
    "把 α 换成 α′ ∈ {1/137.036, 0.01, 0.02, 0.05, 0.5, 0.9} 并重算 r_e′=α′ħ/(m_ec)、"
    "a_0′=ħ/(m_ec α′)：r_e′/λ_C 与 λ_C/a_0′ 相对 α′ 的残差恒 ≤ %s（机器零，6/6 全过）。"
    "阳性对照：同一批数据下 r_e′/a_0′ 与 α′ 之比分别为 %s（均显著 ≠1）⇒ 检验器能识别"
    "非恒等式，不是恒真判据。⇒ 这三条「身份」描述的是 α 的【记账方式】，不是 α 的"
    "【数值来源】：α 为何是 1/137.036 在本来料中完全没有被解释。"
    % (fv(_max_resid), ",".join(_r[3] for _r in _zero_rows)),
    {"alpha_grid": [r[0] for r in _zero_rows],
     "resid_re_lamC": [r[1] for r in _zero_rows],
     "resid_lamC_a0": [r[2] for r in _zero_rows],
     "positive_control_ratio": [r[3] for r in _zero_rows]})

add("C02", "CORRECTED",
    "r_e、λ_C、a_0 不是三个独立观测量 —— 「四重相等」不构成实验验证",
    "三者全部由同一组 {α, ħ, m_e, c} 代数复合而成：r_e=αħ/(m_ec)、λ_C=ħ/(m_ec)、"
    "a_0=ħ/(m_ecα)。故「α = r_e/λ_C = λ_C/a_0」是同一定义式的两种写法，"
    "「三者精确相等」是记账恒真，不是对自然的测量。把它表述为「α 的四重身份」"
    "会把重述误读为解释。",
    {"independent_observables": 0})

add("C03", "CORRECTED",
    "「残差 ~10⁻⁴⁴」在三种口径下都不成立：恒等路径为 0、字面路径为 10⁻¹²、实验路径不存在",
    "①定义式路径：残差 %s（严格 0，因为消掉了全部公共因子）；②公开字面值路径："
    "r_e/λ_C 与 α 差 %s、λ_C/a_0 与 α 差 %s（取位差异，非物理）；③实验路径："
    "因三个量非独立（C02），不存在独立的实验残差。⇒ 10⁻⁴⁴ 这个数字既非恒等式残差"
    "也非实验精度，属叙事性数值，建议删除或改为「恒等式，残差恒为 0」。"
    % (fv(rel(r1_def, ALPHA)), fv(rel(r1_lit, ALPHA)), fv(rel(r2_lit, ALPHA))),
    {"def": fv(rel(r1_def, ALPHA)), "lit1": fv(rel(r1_lit, ALPHA)),
     "lit2": fv(rel(r2_lit, ALPHA))})

add("C04", "CORRECTED",
    "「四重身份」的有效计数是 2 条，不是 4 条",
    "第 4 条 r_e=αλ_C=α²a_0 是第 1 条的直接推论（机器核验：α²a_0=%s 与 r_e=%s 相对偏差 "
    "%s），不构成独立身份；第 2 条是教科书玻尔模型结果（B04）；第 3 条未定义 τ_e（B06）"
    "且自身互斥（B05）。⇒ 有效身份 = 长度比链（第 1+4 合并）+ 速度比 = 2 条，"
    "其中真正标注为「TUFT 新发现」的 1 条当前不可核验。"
    % (fv(ALPHA * ALPHA * A0_LIT), fv(R_E_LIT),
       fv(rel(ALPHA * ALPHA * A0_LIT, R_E_LIT))),
    {"alpha2_a0": fv(ALPHA * ALPHA * A0_LIT), "r_e": fv(R_E_LIT),
     "resid": fv(rel(ALPHA * ALPHA * A0_LIT, R_E_LIT)), "effective_count": 2})

add("C05", "INFO",
    "「填充效率 / 只拧了 √α 而不是 360°」是隐喻叙事，无可证伪内容",
    "该叙事不含方程、不含边界条件、不含测量协议：任何「不是 360°」的角都可套用，"
    "无法被任何观测否证（对照 D01：若真要求转满 360°，其自身公式给出 α=4π²，"
    "与真值差 5410 倍 ⇒ 叙事的对照面反而不成立）。建议改标注为「图像化说明，非判据」。",
    {"falsifiable": False})

# ================================================================ D 段 附加读数
_alpha_360 = (D(2) * PI) * (D(2) * PI)
add("D01", "BOUNDARY",
    "叙事对照面自查：若「转满 360°」，来料自身公式给出 α = 4π² = 39.48（差 5410 倍）",
    "来料叙事以「而不是 360°」作对照。按它自己的第 3 条公式 α=(τλ_C)²，取 τλ_C=2π "
    "⇒ α = 4π² = %s，与真值 %s 差 %s 倍。⇒ 该对照不是可选的另一种物理，而是被"
    "排除 5410 倍的情形；叙事用它作修辞可以，但不能当作「填充效率」的定量定义。"
    % (fv(_alpha_360), fv(ALPHA), fv(_alpha_360 / ALPHA)),
    {"alpha_360": fv(_alpha_360), "mismatch": fv(_alpha_360 / ALPHA)})

add("D02", "PASS",
    "α 的无量纲性机器确认（唯一不涉及来料几何的正面项）",
    "α = e²/(4πε₀ħc)：[e²]=%s、[4πε₀ħc]=%s ⇒ [α]=%s（无量纲）。这是全册唯一"
    "无条件成立且非重述的读数；但它对 α 的【数值】同样零约束（C01）。"
    % (dstr(dpow(DIM_Q, 2)), dstr(dmul(DIM_EPS0, dmul(DIM_HBAR, DIM_C))),
       dstr(ddiv(dpow(DIM_Q, 2), dmul(DIM_EPS0, dmul(DIM_HBAR, DIM_C))))),
    {"dim_alpha": dstr(ddiv(dpow(DIM_Q, 2), dmul(DIM_EPS0, dmul(DIM_HBAR, DIM_C))))})

_r_from_tau = TAU_E_BACK * TAU_E_BACK * LAMC_DEF * LAMC_DEF * LAMC_DEF
add("D03", "FAIL",
    "第 3 条与第 1 条互为恒等重排：一旦定义 τ_e=√α/λ_C，即有 r_e = τ_e² λ_C³（零新增信息）",
    "τ_e²λ_C³ = (√α/λ_C)²·λ_C³ = αλ_C = r_e。机器核验：τ_e²λ_C³ = %s，r_e = %s，"
    "相对偏差 %s（残差恒为 0，因为两式同源）。量纲：[τ²λ³] = %s，与 [r_e]=L 一致 ✓。"
    "⇒ 第 3 条并没有提供 α 的独立几何来源，它只是把第 1 条改写成含 τ 的形式；"
    "「新发现」的实质是【给 α 换了一个符号外衣】。"
    % (fv(_r_from_tau), fv(R_E_DEF), fv(rel(_r_from_tau, R_E_DEF)),
       dstr(dmul(dpow(ddiv(DIM_1, DIM_L), 2), dpow(DIM_L, 3)))),
    {"tau2_lam3": fv(_r_from_tau), "r_e": fv(R_E_DEF),
     "resid": fv(rel(_r_from_tau, R_E_DEF))})

add("D04", "INFO",
    "外部输入账：本页共 4 项未声明输入（其中 1 项为函数级）",
    "①τ_e(λ_C) 的定义式（缺失 ⇒ 第 3 条不可证伪）；②λ_C 的约化/非约化口径；"
    "③κ/τ 的取值（A 段自称 3/2，与第 3 条自洽版 11.66 冲突）；④「力 ∝ 挠率²」的"
    "指数关系（由 A03 反推，未声明）。⇒ 若沿用本库 Ω5（自由常数 ≤1）口径，"
    "本页至少需登记 3 项外部输入；第 ① 项属定义缺失而非常数，无法用「登记常数」解决。",
    {"external_inputs": ["tau_e_definition", "lambda_C_convention",
                         "kappa_over_tau_value", "force_torsion_exponent"],
     "count": 4})

add("D05", "CORRECTED",
    "最小修法候选（本册不代选，按代价升序）",
    "M1（零成本）把 λ_C 显式声明为约化康普顿波长，并把 r_e/λ_C、λ_C/a_0 标注为"
    "「定义式恒等重排，非 α 的来源」；M2（零成本、必做）在第 3 条中二选一："
    "保留「扭转角 = √α」或保留「sin(扭角) = √α」，删除另一句（B05）；"
    "M3（代价：+1 定义）给出 τ_e 的定义式与测量方案，使第 3 条可证伪（B06）；"
    "M4（代价：放弃一条口径）在「α=τ/κ」与「α=(τλ_C)²」之间择一（B07 已证二者"
    "代数互斥，不可并引）。",
    {"candidates": ["M1 declare reduced lambda_C",
                    "M2 drop one of the two mutually exclusive readings",
                    "M3 supply tau_e definition",
                    "M4 choose between alpha=tau/kappa and alpha=(tau*lambda_C)^2"]})

# ================================================================ 输出
SECTIONS = [
    ("一、α 不是什么（来料否定的三条猜想）", ["A01", "A06"]),
    ("二、四重身份逐条核验", ["B01", "B08"]),
    ("三、零信息量与计数更正", ["C01", "C05"]),
    ("四、附加读数与最小修法", ["D01", "D05"]),
]

def _in_range(code, rng):
    return (rng[0] <= code <= rng[1]) or (code in rng)

def main():
    lines = []
    lines.append("=" * 78)
    lines.append("TUFT-r110 · α = 1/137.036 的几何身份 —— 四重断言全维审计")
    lines.append("=" * 78)
    counts = {}
    for e in ENTRIES:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    lines.append("条目 %d：%s" % (len(ENTRIES),
                 " / ".join("%s=%d" % (k, counts[k]) for k in sorted(counts))))
    gok = sum(1 for g in GUARDS if g["ok"])
    lines.append("守卫 %d/%d" % (gok, len(GUARDS)))
    for g in GUARDS:
        if not g["ok"]:
            lines.append("  [GUARD-FAIL] %s %s" % (g["name"], g["info"]))
    lines.append("")
    for name, rng in SECTIONS:
        lines.append("-" * 78)
        lines.append(name)
        lines.append("-" * 78)
        for e in ENTRIES:
            if _in_range(e["code"], rng):
                lines.append("[%s] %s · %s" % (e["status"], e["code"], e["title"]))
                lines.append("    %s" % e["detail"])
                lines.append("")
    lines.append("=" * 78)
    lines.append("关键读数")
    lines.append("=" * 78)
    for k, v in [("alpha", fv(ALPHA)), ("sqrt(alpha)", fv(SQRT_A)),
                 ("sin(sqrt(alpha))", fv(SIN_SQRT_A)),
                 ("asin(sqrt(alpha)) rad", fv(ASIN_SQRT_A)),
                 ("asin(sqrt(alpha)) deg", fv(deg(ASIN_SQRT_A))),
                 ("sqrt(alpha) deg", fv(deg(SQRT_A))),
                 ("r_e/lambda_C (literal)", fv(r1_lit)),
                 ("lambda_C/a_0 (literal)", fv(r2_lit)),
                 ("v_e = alpha*c (m/s)", fv(V_E)),
                 ("tau_e backsolve (m^-1)", fv(TAU_E_BACK)),
                 ("F_E/F_G (e-e)", fv(FE_FG)), ("F_G/F_E (e-e)", fv(FG_FE)),
                 ("sqrt(F_E/F_G)", fv(SQRT_FE_FG))]:
        lines.append("  %-28s %s" % (k, v))
    txt = "\n".join(lines)
    print(txt)

    os.makedirs(OUT_DATA, exist_ok=True)
    stem = "TUFT-r110_alpha几何身份_四重断言全维审计_2026-10-19"
    with open(os.path.join(OUT_DATA, stem + "_report.txt"), "w",
              encoding="utf-8") as f:
        f.write(txt + "\n")
    with open(os.path.join(OUT_DATA, stem + ".json"), "w",
              encoding="utf-8") as f:
        json.dump({"round": "r110", "date": "2026-10-19",
                   "entries": ENTRIES, "guards": GUARDS,
                   "counts": counts,
                   "key_numbers": {
                       "alpha": fv(ALPHA), "sqrt_alpha": fv(SQRT_A),
                       "sin_sqrt_alpha": fv(SIN_SQRT_A),
                       "asin_sqrt_alpha": fv(ASIN_SQRT_A),
                       "asin_sqrt_alpha_deg": fv(deg(ASIN_SQRT_A)),
                       "sqrt_alpha_deg": fv(deg(SQRT_A)),
                       "re_over_lamC_def_resid": fv(rel(r1_def, ALPHA)),
                       "re_over_lamC_lit_resid": fv(rel(r1_lit, ALPHA)),
                       "lamC_over_a0_lit_resid": fv(rel(r2_lit, ALPHA)),
                       "v_e_m_per_s": fv(V_E),
                       "tau_e_backsolve": fv(TAU_E_BACK),
                       "FE_over_FG_ee": fv(FE_FG), "FG_over_FE_ee": fv(FG_FE),
                       "sqrt_FE_over_FG": fv(SQRT_FE_FG)}},
                  f, ensure_ascii=False, indent=2)

    md = ["# TUFT-r110 · α 的几何身份 四重断言 · 数据产物", "",
          "条目 %d（%s），守卫 %d/%d。" % (len(ENTRIES),
          " / ".join("%s=%d" % (k, counts[k]) for k in sorted(counts)),
          gok, len(GUARDS)), ""]
    for e in ENTRIES:
        md.append("## [%s] %s %s" % (e["status"], e["code"], e["title"]))
        md.append("")
        md.append(e["detail"])
        md.append("")
    with open(os.path.join(OUT_DATA, stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    return 0 if gok == len(GUARDS) else 1

if __name__ == "__main__":
    sys.exit(main())
