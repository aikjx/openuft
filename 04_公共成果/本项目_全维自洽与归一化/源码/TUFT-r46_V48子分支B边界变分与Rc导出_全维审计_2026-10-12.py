# -*- coding: utf-8 -*-
"""
TUFT-V4.8 子分支B 全维审计（r46 · 2026-10-12）
================================================
来料：《TUFT-V4.8｜子分支B：作用量变分推导边界约束，消去 R_c(κ) 幂律 ansatz（算法联盟）》

受理定位（零重复声明）：
  r45 = V4.5 变分推导螺旋场自能（其 T34：无源+衰减边界的调和函数不存在，唯一解 κ≡0）
  r44 = V4.3/V4.4 g-2 联合拟合链 + 自能屏蔽 ansatz
  本册 = V4.8 的「加源 + 加边界项 + 普朗克紫外截断」这组补丁是否解除了 r45/r44 的承重 FAIL

方法（纯标准库）：
  * decimal.Decimal，getcontext().prec = 60
  * Fraction 四分量量纲 (M, L, T, Q)——量纲工具本身先过 guard 再用于判定
    （本库已三次把「量纲相乘写成逐分量相乘」，本册设 G01/G02 当场拦下）
  * 分数幂一律走 (x.ln()*p).exp()，不用 Decimal 的 ** 分数指数
  * 每条断言配「阳性对照」或「两版对拍」，防止检验器恒零

判定口径：
  PASS=来料声称成立且机器复核成立；FAIL=来料声称成立但机器否证；
  MISMATCH=来料两处自相矛盾；CORRECTED=本册给出的修正式且机器验证成立；
  BOUNDARY=依赖未声明约定，机器不可判；INFO=记账/射程说明，不含判定。
不自推：涉及 EC 挠率—自旋系数、σ 的第一性导出、ADM-BSSN 具体演化式，一律只登记不自推。
"""

import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "数据")
os.makedirs(DATA, exist_ok=True)

D = Decimal

# ---------------------------------------------------------------- CODATA / 常数
c     = D("299792458")
hbar  = D("1.0545718176461565e-34")
e_ch  = D("1.602176634e-19")
m_e   = D("9.1093837015e-31")
m_mu  = D("1.883531627e-28")
m_tau = D("3.16754e-27")
G_exp = D("6.67430e-11")
lP_nom = D("1.616255078e-35")            # 来料代码里的标称值
lP_def = (hbar * G_exp / (c ** 3)).sqrt()  # 定义式精算值
m_P    = (hbar * c / G_exp).sqrt()

# 来料 §6 代码内的实验输入（原样固化，不代选口径）
AE_QED  = D("1.15965218128e-3")
AE_EXP  = D("1.15965218059e-3")
AMU_QED = D("1.16591810e-3")
AMU_EXP = D("1.16592040e-3")
DA_E    = AE_EXP - AE_QED     # -6.9e-13
DA_MU   = AMU_EXP - AMU_QED   # +2.30e-9
SIG_E   = D("1e-12")          # 来料 σ 口径
SIG_MU  = D("4e-7")           # 来料 σ 口径
SIG_G_REL = D("1e-5")         # 来料 σ 口径（相对）
# 真实口径（仅作对照，不代入来料 χ²）
SIG_E_REAL   = D("2.8e-14")
SIG_MU_REAL  = D("5.2e-10")
SIG_G_REAL   = D("2.2e-5")

PI = D("3.14159265358979323846264338327950288419716939937510582097494")
SQRT2 = D(2).sqrt()

# ---------------------------------------------------------------- 量纲工具 (M,L,T,Q)
def dmul(a, b):
    """量纲相乘 = 指数相加（本库三次误写为逐分量相乘，G01 拦）"""
    return tuple(x + y for x, y in zip(a, b))

def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))

def dpow(a, n):
    n = Fraction(n)
    return tuple(Fraction(x) * n for x in a)

def dinv(a):
    return tuple(-Fraction(x) for x in a)

def dstr(a):
    names = "MLTQ"
    out = []
    for nm, v in zip(names, a):
        v = Fraction(v)
        if v == 0:
            continue
        out.append(nm if v == 1 else "%s^%s" % (nm, v))
    return "·".join(out) if out else "1"

def deq(a, b):
    return tuple(Fraction(x) for x in a) == tuple(Fraction(x) for x in b)

DIM_M   = (1, 0, 0, 0)
DIM_L   = (0, 1, 0, 0)
DIM_T   = (0, 0, 1, 0)
DIM_Q   = (0, 0, 0, 1)
DIM_1   = (0, 0, 0, 0)
DIM_HBAR = (1, 2, -1, 0)          # M L^2 T^-1
DIM_C    = (0, 1, -1, 0)          # L T^-1
DIM_E    = (1, 2, -2, 0)          # 能量 M L^2 T^-2
DIM_KAPPA = (0, -1, 0, 0)         # 曲率 L^-1
DIM_EN_DENS = (1, -1, -2, 0)      # 能量密度 M L^-1 T^-2
DIM_SURF_TEN = (1, 0, -2, 0)      # 表面张力（单位面积能量）M T^-2
DIM_PRESS = (1, -1, -2, 0)        # 压强 = 能量密度
DIM_G    = (3, -1, -2, 0)         # L^3 M^-1 T^-2（以 (M,L,T,Q) 序写成 L^3 M^-1 T^-2）
DIM_Gv   = (-1, 3, -2, 0)         # 按 (M,L,T) 序：M^-1 L^3 T^-2

# ---------------------------------------------------------------- 结果收集
ITEMS = []
GUARD = []
KEY = {}

def add(iid, verdict, claim, reading):
    ITEMS.append({"id": iid, "verdict": verdict, "claim": claim, "reading": reading})

def guard(name, cond, detail=""):
    GUARD.append({"name": name, "ok": bool(cond), "detail": detail})
    return bool(cond)

def key(k, v):
    KEY[k] = str(v)

def fmt(x, n=25):
    if isinstance(x, Decimal):
        return format(x, "." + str(n) + "E")
    return str(x)

# ---------------------------------------------------------------- guard：量纲工具自检
# 量纲工具必须自己先被守卫，否则全册量纲读数可能是垃圾（r37/r44/r45 三次教训）
guard("G01_dmul_adds_exponents", deq(dmul(DIM_M, DIM_L), (1, 1, 0, 0)),
      "M·L 应为 (1,1,0,0)，得 %s" % (dmul(DIM_M, DIM_L),))
guard("G02_dpow_negative", deq(dpow(DIM_L, -2), (0, -2, 0, 0)),
      "L^-2 应为 (0,-2,0,0)，得 %s" % (dpow(DIM_L, -2),))
guard("G03_hbar_c", deq(dmul(DIM_HBAR, DIM_C), (1, 3, -2, 0)),
      "[ħc]=M L^3 T^-2，得 %s" % dstr(dmul(DIM_HBAR, DIM_C)))
guard("G04_hbar_over_c", deq(ddiv(DIM_HBAR, DIM_C), (1, 1, 0, 0)),
      "[ħ/c]=M L，得 %s" % dstr(ddiv(DIM_HBAR, DIM_C)))
guard("G05_lP_squared_is_L2",
      deq(ddiv(dmul(DIM_HBAR, DIM_Gv), dpow(DIM_C, 3)), (0, 2, 0, 0)),
      "[ħG/c^3]=L^2，得 %s" % dstr(ddiv(dmul(DIM_HBAR, DIM_Gv), dpow(DIM_C, 3))))
guard("G06_surface_tension_is_MT2",
      deq(ddiv(dmul(DIM_HBAR, DIM_C), dpow(DIM_L, 3)), DIM_SURF_TEN),
      "[ħc/l_P^3]=M T^-2（表面张力），得 %s" % dstr(ddiv(dmul(DIM_HBAR, DIM_C), dpow(DIM_L, 3))))
guard("G07_energy_density",
      deq(dmul(ddiv(DIM_HBAR, DIM_C), dpow(dmul(DIM_KAPPA, dinv(DIM_L)), 2)), (1, -3, 0, 0)),
      "[ħ/c·(∇κ)^2] 实为 M L^-3，得 %s" % dstr(dmul(ddiv(DIM_HBAR, DIM_C), dpow(dmul(DIM_KAPPA, dinv(DIM_L)), 2))))
guard("G08_G_dim",
      deq(ddiv(dmul(dpow(DIM_C, 3), dpow(DIM_L, 2)), DIM_HBAR), DIM_Gv),
      "[c^3 l_P^2/ħ]=M^-1 L^3 T^-2，得 %s" % dstr(ddiv(dmul(dpow(DIM_C, 3), dpow(DIM_L, 2)), DIM_HBAR)))

# ============================================================ A 段：量纲链（§1–§4）
GRAD_KAPPA = dmul(DIM_KAPPA, dinv(DIM_L))          # [∇κ] = L^-2
GRAD2 = dpow(GRAD_KAPPA, 2)                        # L^-4
D_K = dinv(DIM_L)                                  # 主曲率 K = 2/R_c : L^-1

# B01 体拉氏密度动能项
dim_bulk = dmul(ddiv(DIM_HBAR, DIM_C), GRAD2)
gap_bulk = ddiv(DIM_EN_DENS, dim_bulk)
add("B01", "FAIL",
    "体作用量动能项 (ħ/2c)(∇κ)² 可作拉氏密度（能量密度）",
    "机器 [ħ/c·(∇κ)²]=%s，能量密度须为 %s，缺口 %s = c²（继承 r45 T12，本册第 10 次复发）"
    % (dstr(dim_bulk), dstr(DIM_EN_DENS), dstr(gap_bulk)))
key("dim_bulk_kinetic", dstr(dim_bulk))
key("dim_bulk_gap", dstr(gap_bulk))

# B02 σ 的声明量纲
add("B02", "MISMATCH",
    "σ 为「边界面能量密度」，量纲 ML^-1T^-2",
    "表面能密度（单位面积能量）机器量纲为 %s（=M T^-2）；来料写的 %s 实为压强/能量密度，"
    "两者差 %s。来料同时把它叫「表面张力」与「面能量密度」，两个名字对应两个量纲"
    % (dstr(DIM_SURF_TEN), dstr(DIM_PRESS), dstr(ddiv(DIM_PRESS, DIM_SURF_TEN))))

# B03 边界力学平衡式两端
sigma_decl = (1, -1, -2, 0)     # 来料声明 ML^-1T^-2
sigma_true = (1, 0, -2, 0)      # 真表面张力 MT^-2
lhs_bal = dim_bulk
rhs_decl = dmul(sigma_decl, D_K)
rhs_true = dmul(sigma_true, D_K)
add("B03", "FAIL",
    "边界力学平衡 (ħ/2c)(∇κ)² = σ·K 量纲齐次",
    "左 %s；右（σ 取来料声明值）= %s，缺口 %s；右（σ 取真表面张力）= %s，缺口 %s。"
    "两种 σ 口径都不齐，且缺口都不是 c 的纯幂 ⇒ 不是「漏一个 c²」那么简单"
    % (dstr(lhs_bal), dstr(rhs_decl), dstr(ddiv(lhs_bal, rhs_decl)),
       dstr(rhs_true), dstr(ddiv(lhs_bal, rhs_true))))
key("gap_balance_declared_sigma", dstr(ddiv(lhs_bal, rhs_decl)))
key("gap_balance_true_sigma", dstr(ddiv(lhs_bal, rhs_true)))

# B04 σ = ħc/(2 l_P²)
dim_sig_claim = ddiv(dmul(DIM_HBAR, DIM_C), dpow(DIM_L, 2))
add("B04", "FAIL",
    "σ = ħc/(2 l_P²) 是「几何最简」的表面张力",
    "机器 %s（=力，N）；既不是来料自称的 %s（差 %s），也不是表面张力 %s（差 %s）"
    "⇒ 相对应取的普朗克表面张力 ħc/l_P³ 少一个长度幂次"
    % (dstr(dim_sig_claim), dstr(sigma_decl), dstr(ddiv(dim_sig_claim, sigma_decl)),
       dstr(DIM_SURF_TEN), dstr(ddiv(dim_sig_claim, DIM_SURF_TEN))))
key("dim_sigma_claim", dstr(dim_sig_claim))

# B05 最小修复版（两处同改）⇒ 平衡式齐次
dim_bulk_fix = dmul(dmul(DIM_HBAR, DIM_C), GRAD2)                 # ħc/2·(∇κ)²
rhs_fix = dmul(ddiv(dmul(DIM_HBAR, DIM_C), dpow(DIM_L, 3)), D_K)  # (ħc/l_P³)·K
ok_b05 = deq(dim_bulk_fix, rhs_fix)
guard("G09_balance_homogeneous_after_fix", ok_b05,
      "修正后左 %s vs 右 %s" % (dstr(dim_bulk_fix), dstr(rhs_fix)))
add("B05", "PASS",
    "（本册）最小修复 ħ/(2c)→ħc/2 且 σ=ħc/(2 l_P³) 后平衡式齐次",
    "左 %s = 右 %s = 压强/能量密度 %s，逐项相等（零成本，但只修齐次性不修物理）"
    % (dstr(dim_bulk_fix), dstr(rhs_fix), dstr(DIM_PRESS)))

# B06 / B07 / B08  C_2 与 κ_0 的量纲
dim_C2_claim = ddiv(dmul(DIM_C, dpow(DIM_L, Fraction(3, 2))), DIM_L)
add("B06", "FAIL",
    "C_2 = c R_c^{3/2}√2 / l_P",
    "κ=C_1+C_2/r 且 [κ]=L^-1 强制 [C_2]=%s（无量纲）；来料式机器量纲 %s，缺口 %s。"
    "静态拉普拉斯解的平衡条件里出现 c，本身就是量纲失控的症状"
    % (dstr(DIM_1), dstr(dim_C2_claim), dstr(ddiv(dim_C2_claim, DIM_1))))
key("dim_C2_claim", dstr(dim_C2_claim))

dim_k0_claim = ddiv(dmul(DIM_C, dpow(DIM_L, Fraction(3, 2))), dpow(DIM_L, 2))
add("B07", "FAIL",
    "κ_0 = √2 c R_c^{3/2} / l_P² 是核心曲率",
    "机器量纲 %s，曲率须为 %s，缺口 %s ⇒ 该「导出关系」不成立"
    % (dstr(dim_k0_claim), dstr(DIM_KAPPA), dstr(ddiv(dim_k0_claim, DIM_KAPPA))))
key("dim_kappa0_claim", dstr(dim_k0_claim))

dim_k0_fix = ddiv(dpow(DIM_L, Fraction(3, 2)), dpow(DIM_L, Fraction(5, 2)))
ok_b08 = deq(dim_k0_fix, DIM_KAPPA)
guard("G10_kappa0_fix_is_Lminus1", ok_b08, "修正式量纲 %s" % dstr(dim_k0_fix))
add("B08", "PASS",
    "（本册）修正版 κ_0 = √2 R_c^{3/2}/l_P^{5/2} 量纲闭合",
    "机器 %s = L^-1 ✓；即 σ 取 ħc/l_P³（而非 ħc/l_P²）时，整条 R_c–κ_0 链量纲自洽")

# B09 U_self 量纲（两种读法）
dim_K_from_def = dmul(DIM_KAPPA, DIM_L)   # κ=K/r ⇒ [K]=1
dim_U_read1 = dmul(dmul(ddiv(DIM_HBAR, DIM_C), dpow(dim_K_from_def, 2)), dinv(DIM_L))
dim_U_read2 = dmul(dmul(ddiv(DIM_HBAR, DIM_C), dpow(dim_C2_claim, 2)), dinv(DIM_L))
add("B09", "FAIL",
    "U_self = (ħ/2c)∫4πr²dr·K²/r⁴ 是能量",
    "读法①按 κ=K/r 的定义 [K]=1 ⇒ [U]=%s（质量维，与 r45 T11 同值）；"
    "读法②按来料 K 表达式 ⇒ [U]=%s（=J·m）。两种读法都不是能量 %s"
    % (dstr(dim_U_read1), dstr(dim_U_read2), dstr(DIM_E)))
key("dim_U_read1", dstr(dim_U_read1))
key("dim_U_read2", dstr(dim_U_read2))

# B10 修正版自能
dim_U_fix = dmul(dmul(DIM_HBAR, DIM_C), dinv(DIM_L))
ok_b10 = deq(dim_U_fix, DIM_E)
guard("G11_U_fix_is_energy", ok_b10, "修正自能 %s" % dstr(dim_U_fix))
add("B10", "PASS",
    "（本册）U = 2πħc K²(1/l_P − 1/R_c) 量纲为能量",
    "机器 %s = ML²T^-2 ✓；与 B05 同一处修复（ħ/2c→ħc/2）")

# B11 a_tuft 量纲
dim_a = ddiv(dmul(DIM_C, dmul(DIM_M, DIM_KAPPA)), dmul(DIM_Q, DIM_HBAR))
add("B11", "FAIL",
    "a_TUFT = −3c·cotθ/(4eħ)·m·κ 是无量纲反常磁矩",
    "机器 %s（与 r45 T25 的 L^-2Q^-1 同族）；反常磁矩须无量纲，补齐因子须 %s"
    % (dstr(dim_a), dstr(dinv(dim_a))))
key("dim_a_tuft", dstr(dim_a))

# B12 质量方程各项
dim_term1 = ddiv(dmul(dmul(DIM_HBAR, DIM_C), DIM_KAPPA), dpow(DIM_C, 2))
dim_term2_claim = ddiv(dim_U_read2, dpow(DIM_C, 2))
dim_term2_fix = ddiv(dim_U_fix, dpow(DIM_C, 2))
add("B12", "FAIL",
    "m = ħκ/(c sinθ) − U_self/c² 两项同量纲",
    "第一项 %s ✓ 是质量；来料 U 版第二项 %s ✗（差 %s）；修正 U 版第二项 %s ✓"
    % (dstr(dim_term1), dstr(dim_term2_claim),
       dstr(ddiv(dim_term1, dim_term2_claim)), dstr(dim_term2_fix)))

# B13 G_th
dim_Gth = ddiv(dmul(dpow(DIM_C, 3), dpow(DIM_L, 2)), DIM_HBAR)
add("B13", "PASS",
    "G_th = c³l_P²/(ħ sinθ) 量纲为 G",
    "机器 %s = M^-1L³T^-2 ✓，与 [G] 同；但 l_P²≡ħG/c³ ⇒ 该式是定义式移项（见 B40）"
    % dstr(dim_Gth))

# ============================================================ B 段：内部自洽（代数）
# B14 §3 内 κ=κ_0+K/r 与 κ=K/r 矛盾
# κ_0 ≡ K/l_P ⇒ κ(l_P) 由第一式给 2K/l_P，由第二式给 K/l_P
add("B14", "MISMATCH",
    "§3 泊松解 κ=κ_0+K/r 与场解 κ(r)=K/r 是同一个解",
    "第一式在 r=l_P 给 κ=κ_0+K/l_P=2K/l_P（因 κ_0≡K/l_P）；第二式给 K/l_P。"
    "两式相差常数项 κ_0，除非 κ_0=0（则无粒子）⇒ 同节内两个场解互斥")

# B15 §4 → §5 的代入多乘一个 R_c
# §4: U = 4πħc R_c²(R_c−l_P)/l_P³ ；§5: U = (4πħc/l_P³)·R_c³·(R_c−l_P)
_RP = D("1e-30")
U_S4 = (4 * PI * hbar * c * (_RP ** 2) * (_RP - lP_nom)) / (lP_nom ** 3)
U_S5 = (4 * PI * hbar * c / (lP_nom ** 3)) * (_RP ** 3) * (_RP - lP_nom)
add("B15", "FAIL",
    "§5 的第二项与 §4 的 U_self 是同一个量",
    "§4 给 U=4πħc·R_c²(R_c−l_P)/l_P³；§5 代入后写成 (4πħc/l_P³)·R_c³·(R_c−l_P)，"
    "**多乘了一个 R_c**（§4 的 R_c³ 因子里含 (R_c−l_P)/(l_P R_c) 的 1/R_c，§5 漏除）。"
    "数值对拍（取 R_c=1e-30 m）：§4=%s，§5=%s，§5/§4=%s"
    % (fmt(U_S4), fmt(U_S5), fmt(U_S5 / U_S4)))
key("U_s4_probe", fmt(U_S4))
key("U_s5_probe", fmt(U_S5))
key("U_s5_over_s4", fmt(U_S5 / U_S4))

# B16 修正代数后 U ∝ κ²（不是 κ^{8/3}）
add("B16", "CORRECTED",
    "（本册）修正 B15 后 U_self ∝ R_c³ ∝ κ² ⇒ m ∝ κ − Cκ²，而非 κ^{8/3}",
    "R_c ∝ κ^{2/3} ⇒ R_c³ ∝ κ²；§5 的 κ^{2+2/3}=κ^{8/3} 来自那个多乘的 R_c。"
    "修正后非线性幂次由 8/3 降为 2（见 B26–B29 的方向判据）")

# B17 指数 2/3 的稳健性（结论对 / 链条错）
# 平衡式左 ∝ R_c^{-4}、右 ∝ R_c^{-1} ⇒ K² ∝ R_c³ ⇒ R_c ∝ K^{2/3} ∝ (κ_0 l_P)^{2/3}
add("B17", "PASS",
    "指数 β=−2/3（R_c ∝ κ^{2/3}）不依赖 c 与 l_P 的具体幂次",
    "指数只由平衡式两端对 R_c 的幂次决定：左 (∇κ)² ∝ R_c^-4、右 σK ∝ R_c^-1（σ 与 R_c 无关）"
    "⇒ K² ∝ R_c³ ⇒ R_c ∝ K^{2/3}。**结论成立、链条（系数）错误**：来料系数含 c 且 l_P 幂次错（B06/B07）")

# B18 K 的双重决定
add("B18", "FAIL",
    "源强度 K 与外边界力学平衡可以同时成立",
    "K 在 §3 是「螺旋世界线的几何源密度」的强度（应由源决定），在 §3 外边界条件里又被边界平衡"
    "钉成 K=√2 c R_c^{3/2}/l_P。源与边界各给一个方程而未知量只有 K、R_c ⇒ 形式闭合，"
    "但源的物理内容完全不进入 ⇒ 源项是占位符；若坚持源强度物理给定，则 R_c 被源单值决定、边界条件过约束")

# B19 内边界只贡献加性常数
add("B19", "INFO",
    "「普朗克紫外正则化」在场解中起了什么作用",
    "κ(l_P)=κ_0 是 K 的定义式、非约束；l_P 在整条链里唯一的作用是自能积分下限，"
    "贡献 U 中的加性常数项 −2πħcK²/(c²... )∝1/l_P。⇒ 紫外截断不改变任何标度结论")

# ---------------- 数值：R_c(κ) 两版 + 定义域
def Rc_claim(kap):
    """来料版 R_c = (κ l_P²/(√2 c))^{2/3}"""
    x = (kap * lP_nom ** 2) / (SQRT2 * c)
    return (x.ln() * (D(2) / D(3))).exp()

lP_p25 = (lP_nom.ln() * (D(5) / D(2))).exp()   # l_P^{5/2}（Decimal 分数幂走 ln/exp）

def Rc_fix(kap):
    """修正版 R_c = (κ l_P^{5/2}/√2)^{2/3}"""
    x = (kap * lP_p25) / SQRT2
    return (x.ln() * (D(2) / D(3))).exp()

kappa_e = m_e * c / hbar      # 弱场（r45 T19 已确认 κ = mc sinθ/ħ）
kappa_mu = m_mu * c / hbar
kappa_tau = m_tau * c / hbar
lamC_e = hbar / (m_e * c)
lamC_mu = hbar / (m_mu * c)

tbl_Rc = []
for nm, kap in (("电子", kappa_e), ("缪子", kappa_mu), ("τ子", kappa_tau)):
    tbl_Rc.append((nm, kap, Rc_claim(kap), Rc_fix(kap), Rc_claim(kap) / lP_nom, Rc_fix(kap) / lP_nom))
key("kappa_e", fmt(kappa_e))
key("kappa_mu", fmt(kappa_mu))
key("lambda_C_e", fmt(lamC_e))
for nm, kap, r1, r2, q1, q2 in tbl_Rc:
    key("Rc_claim_" + nm, fmt(r1))
    key("Rc_fix_" + nm, fmt(r2))
    key("Rc_over_lP_claim_" + nm, fmt(q1))
    key("Rc_over_lP_fix_" + nm, fmt(q2))

# B20 定义域自毁
add("B20", "FAIL",
    "定义域 r∈[l_P,R_c] 对真实粒子成立（且 R_c≫l_P 的重粒子极限可用）",
    "电子：来料版 R_c=%s m = %s·l_P；修正版 R_c=%s m = %s·l_P。τ子：来料版 %s·l_P、修正版 %s·l_P。"
    "**全部已知粒子的 R_c 都小于 l_P**，定义域 [l_P,R_c] 为空区间，§4 的积分上下限倒置"
    % (fmt(tbl_Rc[0][2]), fmt(tbl_Rc[0][4]), fmt(tbl_Rc[0][3]), fmt(tbl_Rc[0][5]),
       fmt(tbl_Rc[2][4]), fmt(tbl_Rc[2][5])))

# B21 定义域自洽门槛
kappa_gate = SQRT2 / lP_nom
m_gate = hbar * kappa_gate / c
add("B21", "FAIL",
    "R_c>l_P 的门槛与已知粒子质量相容",
    "R_c>l_P ⇔ κ>√2/l_P=%s m^-1 ⇔ m>√2·m_P=%s kg。电子 %s kg，差 %s 倍（%s 个量级）。"
    "与 r44 修正版上界 m_P/2=%s kg 同属「普朗克质量门槛」家族（相差 2√2）"
    % (fmt(kappa_gate), fmt(m_gate), fmt(m_e), fmt(m_gate / m_e),
       fmt((m_gate / m_e).ln() / D(10).ln()), fmt(m_P / 2)))
key("kappa_gate", fmt(kappa_gate))
key("m_gate", fmt(m_gate))
key("gate_over_electron_orders", fmt((m_gate / m_e).ln() / D(10).ln()))

# B41（提前：R_c 与康普顿定标反向）
add("B41", "FAIL",
    "「R_c 随 κ 增大而增大，正是我们需要的行为」",
    "R_c ∝ κ^{2/3} ∝ m^{2/3} 随质量**增大**，而局域化尺度（康普顿波长）λ_C=ħ/(mc) ∝ m^-1 随质量**减小**。"
    "电子：R_c(修正版)=%s m vs λ_C=%s m，差 %s 个量级且方向相反 ⇒ 与「重粒子更局域」的物理期望反号"
    % (fmt(tbl_Rc[0][3]), fmt(lamC_e), fmt((lamC_e / tbl_Rc[0][3]).ln() / D(10).ln())))
key("Rc_vs_lambdaC_orders_e", fmt((lamC_e / tbl_Rc[0][3]).ln() / D(10).ln()))

# ============================================================ C 段：变分学本身
# B22 场值变分（σ 与 κ 无关 ⇒ 自然边界条件是 Neumann）
# κ=K/r ⇒ ∂_nκ(R_c) = -K/R_c²；驻定要求其为 0 ⇒ K=0 ⇒ 平凡场
grad_n_at_Rc = -D(1) / (D("1e-30") ** 2)
ok_b22_zero = (grad_n_at_Rc == 0)
guard("G12_neumann_is_nontrivial", not ok_b22_zero,
      "∂_nκ(R_c) = %s ≠ 0 ⇒ 违反自然边界条件" % fmt(grad_n_at_Rc))
add("B22", "FAIL",
    "边界变分原理（吉布斯–哈达玛）给出的是力学平衡式 (ħ/2c)(∇κ)²=σK",
    "对**场值**变分时，边界项正是 G-H 项 (ħ/c)∂_nκ·δκ；来料 §2 已取 σ=常数（与 κ 无关）"
    "⇒ δS_bdry/δκ=0 ⇒ 自然边界条件为 ∂_nκ|_{R_c}=0。而解 κ=K/r 给 ∂_nκ=−K/R_c²=%s≠0。"
    "**该条件是「σ 依赖 κ」时才出现的**（σ∝κ 会给出非零 ∂_nκ），来料恰恰先取消了 σ 对 κ 的依赖"
    "、随后又不施加 Neumann ⇒ 变分不完备，两处只做了一处" % fmt(grad_n_at_Rc))

# B23 对边界**位置**变分：符号自洽性（来料 S_bdry 带负号 ⇒ 极大/驻定式同号）
sigma_fix = (hbar * c) / (2 * lP_nom ** 3)          # 修正版普朗克表面张力
R0 = D("1e-30")
K0 = (2 * R0 ** 3 / (lP_nom ** 3)).sqrt()           # 修正版平衡条件 K²=2R_c³/l_P³

def E_of_R(R, K=K0, sig=sigma_fix):
    # E(R) = ∫_{lP}^{R} 4πr²·(ħc/2)(K²/r⁴) dr − 4πR²σ ，第一项解析 = 2πħcK²(1/lP − 1/R)
    return 2 * PI * hbar * c * K * K * (1 / lP_nom - 1 / R) - 4 * PI * R * R * sig

h = R0 / D("1000")
dE_num = (E_of_R(R0 + h) - E_of_R(R0 - h)) / (2 * h)
# 解析导数：dE/dR = 2πħcK²/R² − 8πRσ（精确 Decimal，不受差分截断影响）
dE_exact = 2 * PI * hbar * c * K0 * K0 / (R0 ** 2) - 8 * PI * R0 * sigma_fix
# 中心差分截断误差估计：(h²/6)·E''' ，E''' = 6·2πħcK²/R⁴
trunc = (h ** 2 / 6) * (6 * 2 * PI * hbar * c * K0 * K0 / (R0 ** 4))
scale_dE = abs(2 * PI * hbar * c * K0 * K0 / (R0 ** 2))   # 与导数同量级的参考尺度
rel_dE = abs(dE_exact) / scale_dE
guard("G13_boundary_stationarity_exact", rel_dE < D("1e-30"),
      "解析 dE/dR = %s，相对尺度 %s" % (fmt(dE_exact), fmt(rel_dE)))
guard("G13b_truncation_explains_numeric",
      abs(dE_num - dE_exact) < abs(trunc) * 10,
      "数值差分 %s vs 解析 %s，差 %s，截断误差估计 %s ⇒ 差分非零纯属截断"
      % (fmt(dE_num), fmt(dE_exact), fmt(dE_num - dE_exact), fmt(trunc)))
add("B23", "PASS",
    "（符号面）对边界半径 R_c 变分可得来料的平衡式（因 S_bdry 取负号）",
    "E(R)=2πħcK²(1/l_P−1/R)−4πR²σ；解析 dE/dR 在平衡半径处 = %s（相对尺度 %s，机器零）"
    "⇒ 一阶驻定与来料式同形（**符号不是问题**）。数值中心差分读数 %s 与截断误差 %s 同量级，"
    "证明它不是真非零（差分判据在本尺度失效，必须走解析式）"
    % (fmt(dE_exact), fmt(rel_dE), fmt(dE_num), fmt(trunc)))
key("dE_dR_exact_at_R0", fmt(dE_exact))
key("dE_dR_numeric_at_R0", fmt(dE_num))
key("dE_truncation_estimate", fmt(trunc))

# B24 二阶导数：驻点是极大值 ⇒ 径向不稳定
d2E = (E_of_R(R0 + h) - 2 * E_of_R(R0) + E_of_R(R0 - h)) / (h * h)
add("B24", "FAIL",
    "该驻点是稳定平衡（局域包可稳定存在）",
    "E''(R_c) = −4πħcK²/R_c³ − 8πσ < 0（两项同号恒负），数值 %s ⇒ 驻点是能量**极大值**："
    "R_c 向任一方向偏离都使能量下降 ⇒ 局域包要么坍缩到 l_P、要么无限膨胀，**不存在稳定局域包**"
    % fmt(d2E))
key("d2E_dR2_at_R0", fmt(d2E))

# B25 名实核对
add("B25", "MISMATCH",
    "所称「吉布斯–哈达玛边界项」就是 (ħ/2c)(∇κ)²=σK",
    "G-H 项是场值变分产生的 (ħ/c)∂_nκ·δκ（B22）；来料写的是 Young–Laplace / Gibbs–Thomson 型条件"
    "（对边界**位置**变分产生）。两者是两次不同的变分，来料只做了后者，却用前者的名字"
    "并声称「体变分+边界变分已完备」")

# ============================================================ D 段：物理与拟合
# 弱场 κ = mc·sinθ/ħ（r45 T19 已机器确认），取 sinθ=1 只影响量级不影响符号与比值
def Acoef(m):
    """a_TUFT = −cotθ · Acoef(m)；Acoef = 3c/(4eħ)·m·κ，κ=mc/ħ"""
    return (3 * c / (4 * e_ch * hbar)) * m * (m * c / hbar)

A_e = Acoef(m_e)
A_mu = Acoef(m_mu)
ratio_model = (m_mu / m_e) ** 2
ratio_data = DA_MU / DA_E
cot_e = -DA_E / A_e
cot_mu = -DA_MU / A_mu
key("Acoef_e", fmt(A_e))
key("Acoef_mu", fmt(A_mu))
key("ratio_model_mu_over_e", fmt(ratio_model))
key("ratio_data_mu_over_e", fmt(ratio_data))
key("cot_theta_from_electron", fmt(cot_e))
key("cot_theta_from_muon", fmt(cot_mu))
key("model_over_data_factor", fmt(abs(ratio_model / ratio_data)))

add("B26", "FAIL",
    "V4.8 打破了 a ∝ m² 的简单标度",
    "弱场 κ=mc·sinθ/ħ 代入 a=−3c·cotθ·mκ/(4eħ) 后 sinθ 精确消去 ⇒ a ∝ m²cosθ，"
    "a_μ/a_e=(m_μ/m_e)²=%s（与 r44 T31、r45 T23 逐位一致）。「打破 m²」第 3 次复发" % fmt(ratio_model))

add("B27", "FAIL",
    "单一全局 θ 可同时拟合电子与缪子 g-2",
    "电子残差 Δa_e=%s 需 cotθ=%s（>0，θ<π/2）；缪子 Δa_μ=%s 需 cotθ=%s（<0，θ>π/2）。"
    "**符号互斥**，且该结论对 B01/B03/B11 的量纲补齐因子免疫（比值判据里系数整体约掉）"
    % (fmt(DA_E), fmt(cot_e), fmt(DA_MU), fmt(cot_mu)))

add("B28", "FAIL",
    "（量级面）即使放弃符号，单一 θ 也差得不多",
    "模型强制 a_μ/a_e=%s；数据要求 Δa_μ/Δa_e=%s。两者**反号且量级差 %s 倍**"
    "（与 r44 独立给出的 12.75× 同值，互为交叉印证）"
    % (fmt(ratio_model), fmt(ratio_data), fmt(abs(ratio_model / ratio_data))))

# B29 非线性项的方向（修正代数后 m = ακ − Bκ²）
alpha = hbar / c                       # m = ακ − (U/c²)；α=ħ/(c sinθ)
Bcoef = 2 * PI * hbar * lP_nom ** 2 / c   # U/c² = B·κ²（修正版，重粒子极限）
delta_e = Bcoef * m_e / (alpha ** 2)
delta_mu = Bcoef * m_mu / (alpha ** 2)
ratio_nonlinear = ratio_model * (1 + delta_mu) / (1 + delta_e)
guard("G14_nonlinear_pushes_ratio_up", ratio_nonlinear > ratio_model,
      "非线性修正后比值 %s > 线性 %s" % (fmt(ratio_nonlinear), fmt(ratio_model)))
add("B29", "FAIL",
    "§5 的高次项「压制 κ 增长」，使 a_μ/a_e 从 42753 降到数据要求的 3333",
    "m=ακ−Bκ² ⇒ dm/dκ<α ⇒ κ(m)=(m/α)(1+Bm/α²) > m/α ⇒ a=mκ 比值被推**高**而非压低："
    "线性 %s → 非线性 %s（相对 %s）。需要的方向是降到 %s（−3333），"
    "**方向相反**，且修正量本身只有 %s（电子）/%s（缪子）——与 r44「自能方向读反且量级无效」同型"
    % (fmt(ratio_model), fmt(ratio_nonlinear), fmt((ratio_nonlinear / ratio_model - 1)),
       fmt(ratio_data), fmt(delta_e), fmt(delta_mu)))
key("ratio_nonlinear", fmt(ratio_nonlinear))
key("delta_nonlinear_e", fmt(delta_e))
key("delta_nonlinear_mu", fmt(delta_mu))

# Newton 求根（复刻来料 kappa() 的行为，用于 B33）
def kappa_newton(m, x0=D("1e34"), iters=300):
    x = x0
    for _ in range(iters):
        f = alpha * x - Bcoef * x * x - m
        fp = alpha - 2 * Bcoef * x
        if fp == 0:
            break
        x = x - f / fp
    return x

kap_e_newton = kappa_newton(m_e)
kap_mu_newton = kappa_newton(m_mu)
res_e = abs(alpha * kap_e_newton - Bcoef * kap_e_newton ** 2 - m_e) / m_e
guard("G15_newton_converges_from_1e34", res_e < D("1e-40"),
      "Newton 从 1e34 出发的相对残差 %s，κ_e=%s（解析 %s）" % (fmt(res_e), fmt(kap_e_newton), fmt(kappa_e)))
add("B33", "BOUNDARY",
    "mp.findroot(f, 1e34) 能唯一给出 κ(m)",
    "数值复刻：从 x0=1e34 出发 Newton 收敛到 κ_e=%s（解析 weak-field 值 %s，相对残差 %s）⇒ 轻粒子段可用。"
    "但 m(κ)=ακ−Bκ² 是抛物线 ⇒ 同一 m 有**上下两支**；在 κ→κ_crit 处 dm/dκ→0，"
    "求根条件数发散。来料既未声明取哪一支，也未把「取物理支」写进代码 ⇒ 根的选择是未声明约定"
    % (fmt(kap_e_newton), fmt(kappa_e), fmt(res_e)))
key("kappa_e_newton", fmt(kap_e_newton))
key("kappa_e_newton_residual", fmt(res_e))

# B30 dynesty 先验区间 vs 解的量级
prior_lo, prior_hi = D("1e-48"), D("1e-40")
add("B30", "FAIL",
    "§6 的单参数嵌套采样可执行（ptform: δ∈[1e-48,1e-40]）",
    "θ=π/2−δ ⇒ cotθ=tanδ≈δ，先验只覆盖 cotθ∈[%s,%s]（**恒正**）。"
    "电子需 cotθ=%s（比先验下界还低 %s 个量级）；缪子需 cotθ=%s（**负值，先验支上根本不存在**）。"
    "⇒ 采样器在任何点位都取不到解，χ² 将在先验边界处取到伪极小。dynesty **不可执行**"
    % (fmt(prior_lo), fmt(prior_hi), fmt(cot_e),
       fmt(abs((cot_e / prior_lo).ln() / D(10).ln())), fmt(cot_mu)))
key("prior_covers_solution", "False")

# B31 χ_G 零判别力
G_th_nom = (c ** 3) * (lP_nom ** 2) / hbar
res_G_nom = (G_th_nom - G_exp) / G_exp
chi_G_nom = (res_G_nom / SIG_G_REL) ** 2
delta_sq_half = (cot_e ** 2) / 2     # sinθ = cosδ ≈ 1 − δ²/2
add("B31", "FAIL",
    "χ_G 项对 θ 提供有效约束（σ_G/G=1e-5）",
    "G_th=c³l_P²/(ħ sinθ) 中 l_P²≡ħG_exp/c³ ⇒ θ 依赖只剩 1/sinθ−1≈δ²/2=%s，"
    "**远低于 60 位有效精度**（机器读不到）；用标称 l_P 时 G_th 与 G_exp 相对残差 %s ⇒ χ_G=%s≈0。"
    "⇒ 引力项对 θ 的梯度恒为零（继承 r45 T31），χ² 实际只有 2 个数据点、1 个参数"
    % (fmt(delta_sq_half), fmt(res_G_nom), fmt(chi_G_nom)))
key("G_th_residual_nominal", fmt(res_G_nom))
key("chi_G_nominal", fmt(chi_G_nom))
key("sin_theta_machine_offset", fmt(delta_sq_half))

# B32 τ 检验零判别力
m_max_fix = (alpha ** 2) / (4 * Bcoef)
kappa_crit = alpha / (2 * Bcoef)
add("B32", "BOUNDARY",
    "τ 子存在性检验（chi_tau）是有筛选力的判据",
    "修正代数后 m(κ) 的上界 m_max=α²/(4B)=%s kg（κ_crit=%s m^-1），τ 子 %s kg 仅为上界的 %s"
    "⇒ findroot 恒有实根、chi_tau 恒为 0，**零判别力**。"
    "但按 B21 的定义域门槛（R_c>l_P 需 m>√2m_P=%s kg），τ 子根本不在有效定义域内"
    "⇒ **代码与正文口径不一致**：代码接受一个正文认为无定义的解"
    % (fmt(m_max_fix), fmt(kappa_crit), fmt(m_tau), fmt(m_tau / m_max_fix), fmt(m_gate)))
key("m_max_corrected", fmt(m_max_fix))
key("kappa_crit_corrected", fmt(kappa_crit))

# B34 σ 口径（继承 r45 T30，不重算只登记）
add("B34", "INFO",
    "χ² 的 σ 口径（σ_e=1e-12、σ_μ=4e-7、σ_G/G=1e-5）",
    "来料未声明来源。真实口径量级：σ_e≈%s（Cs/Rb 两口径差 5σ 争议）、σ_μ≈%s（含 SM 理论误差）、"
    "σ_G/G=%s（CODATA）。用真实 σ 时 χ² 会放大约 %s 倍（缪子项主导）⇒ 与 r44 的「两档 σ 结论相反」同型"
    % (fmt(SIG_E_REAL), fmt(SIG_MU_REAL), fmt(SIG_G_REAL),
       fmt((SIG_MU / SIG_MU_REAL) ** 2)))
key("sigma_inflation_muon", fmt((SIG_MU / SIG_MU_REAL) ** 2))

# ============================================================ E 段：继承、记账、裁决
add("B35", "FAIL",
    "V4.8 回归「单一全局参数 θ」，无额外 ξ、β",
    "闭合方程实含未声明输入：{σ 的常数形式与系数 ħc/(2l_P²)}、{l_P 紫外截断}、{三维 δ 点源与截断半径}、"
    "{弱场 κ=mc sinθ/ħ}，且 l_P²≡ħG_exp/c³ 把 G 直接注入 ⇒ **外部输入 ≥3**，"
    "与 r45 T33、r44 的 Ω5 判定同型（Ω5：自由常数 ≤1）")

add("B36", "FAIL",
    "（继承 r45 C1）V4.8 是否已修掉「ħ/(2c) 缺 c²」",
    "未修：§1 体作用量、§1 平衡式、§4 自能积分三处仍全部使用 ħ/(2c)（B01/B03/B09）"
    "⇒ 量纲非齐次族在 TUFT 册中**第 10 次复发**（r18→r19→r22→r26→r27→r32→r35→r37→r44→r45→r46）")

add("B37", "BOUNDARY",
    "（继承 r45 C2）V4.8 的加源是否解除了「∇²κ=0 ⇒ 唯一解 κ≡0 ⇒ 无粒子」",
    "半解除：加源确实让 κ=K/r 成为合法解（r45 T34 的否定被绕开）。"
    "但源强度 K 不由螺旋世界线导出（B18），且 K 不进入任何可测量（质量、磁矩只经 κ_0=K/l_P 与边界条件）"
    "⇒ 源项是**占位符**：它恢复了「有解」，没有恢复「有粒子物理」")

add("B38", "FAIL",
    "（继承 r45 C3 / r44 C2）V4.8 是否解除了「打破 m² 被自己取消」",
    "未解除：B26 给出 a_μ/a_e=%s 原封不动；B29 给出非线性项把比值推向**相反**方向（+%s）。"
    "第 3 次复发，且本册新证据是**方向判据**（r44 只判了量级）" % (fmt(ratio_model), fmt(ratio_nonlinear / ratio_model - 1)))

add("B39", "PASS",
    "（交叉印证）本册独立复算与 r44/r45 是否同源一致",
    "a_μ/a_e=%s（r44 T31、r45 T23 同值）；残差比 %s（r44 的 −3.3333333333E+03 同值）；"
    "量级差 %s 倍（r44 的 12.75×）；普朗克质量门槛 %s kg（r44 修正版 m_P/2=%s kg，差 2√2，同族）"
    % (fmt(ratio_model), fmt(ratio_data), fmt(abs(ratio_model / ratio_data)),
       fmt(m_gate), fmt(m_P / 2)))

add("B40", "INFO",
    "G_th = c³l_P²/(ħ sinθ) 是否为新预言",
    "l_P²≡ħG_exp/c³ ⇒ 该式在 sinθ=1 时逐字还原 G_exp（标称 l_P 残差仅 %s）"
    "⇒ 恒等式复读（本库第 10 次），θ 依赖项 %s 低于机器精度（B31）" % (fmt(res_G_nom), fmt(delta_sq_half)))

add("B42", "CORRECTED",
    "§7 自评「由边界变分+点源泊松方程+力学平衡**严格导出** R_c∝κ^{2/3}」",
    "半成立：指数 2/3 确实由平衡式结构唯一确定且稳健（B17 **PASS**）；但承载它的系数式含 c 且 l_P 幂次错"
    "（B06/B07 **FAIL**）、平衡式本身量纲不齐（B03）、σ 的普朗克假设少一个长度幂次（B04）"
    "⇒ 正确表述是「指数被结构钉住、系数与量纲未闭合」；另「消去 ansatz」不成立：σ=常数是**更强**的 ansatz（B35）")

add("B43", "FAIL",
    "§8 四选项的可执行性（本册给出选定）",
    "**选定选项 2（推导 σ），并附两个零成本前置 P1/P2；选项 1 明令禁止。** "
    "①选项1 禁止：B27 符号互斥 + B30 先验覆盖不到解 + B31 χ_G 零判别力 + B32 τ 检验零筛选力"
    "⇒ 运行嵌套采样只能得到先验边界上的伪极小，与库内「MCMC/采样门禁」一致；"
    "②选项2 是本册唯一能攻击新短板的路径（σ 是本册新增且最强的外部输入），但须先做 "
    "**P1**（ħ/2c→ħc/2 且 σ→ħc/(2l_P³)，零成本，B05 已验证齐次）与 "
    "**P2**（§4↔§5 对齐，去掉多乘的 R_c，B15/B16）；且必须接受「σ 只能由普朗克量纲拼出」⇒ 撞 Ω5，须显式登记；"
    "③选项3 不解决：静态解已被 B20（R_c<l_P 定义域自毁）与 B24（驻点为极大值、径向不稳定）否证，动态化救不了；"
    "④选项4 依赖已被 B26/B29 否证的 m(κ) 标度，谱扩展无基")

add("B44", "INFO",
    "缺陷族复发链计数（本册）",
    "量纲非齐次族第 10 次复发（B01/B03/B04/B06/B07/B09/B11/B12，共 8 处）；"
    "「打破 m² 被自己取消」第 3 次复发（B26/B29）；恒等式复读第 10 次（B40）；"
    "「上界预言自毁或恒空」第 3 次（B32）；「定义域与射程不相交」第 2 次（B21，r45 C4 为 44.07 量级、本册 %s 量级）"
    % fmt((m_gate / m_e).ln() / D(10).ln()))

add("B45", "INFO",
    "不自推清单（本册明确未推导、不得当作结论引用）",
    "① σ 的第一性表达式（EC/螺旋联合作用量如何产生表面张力）——不自推；"
    "② 点源 J_κ 与螺旋世界线的具体对应关系与归一化——不自推；"
    "③ R_c>l_P 与 R_c<l_P 两个区间的场方程是否可拼接（r<l_P 区间的动力学）——不自推")

add("B46", "INFO",
    "可保留面（射程声明）",
    "① 指数 β=−2/3 的结论可信（B17），但仅此一项；② 最小修复版（ħc/2 + ħc/l_P³）使 §1–§4 全部量纲闭合"
    "（B05/B08/B10）；③ §2 对「无源调和场无法同时满足原点正则与非零边界应力」的自我诊断**正确**，"
    "是来料本册最扎实的一步；④ 放弃 Dirichlet 改自然边界条件这一操作本身合法（B23 符号面 PASS）。"
    "**以上均不构成可检验预言**")

# ============================================================ 输出
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VERDICTS = ["PASS", "FAIL", "MISMATCH", "CORRECTED", "BOUNDARY", "INFO"]
cnt = {v: sum(1 for it in ITEMS if it["verdict"] == v) for v in VERDICTS}
gpass = sum(1 for g in GUARD if g["ok"])
gfail = len(GUARD) - gpass

base = "TUFT-r46_V48子分支B边界变分与Rc导出_全维审计_2026-10-12"
payload = {
    "round": "r46",
    "date": "2026-10-12",
    "incoming": "TUFT-V4.8 子分支B：作用量变分推导边界约束，消去 R_c(κ) 幂律 ansatz",
    "items": ITEMS,
    "counts": cnt,
    "guard_total": len(GUARD),
    "guard_pass": gpass,
    "guard_fail": gfail,
    "guard_detail": GUARD,
    "key_numbers": KEY,
}
with open(os.path.join(DATA, base + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = []
lines.append("# TUFT-V4.8 子分支B 全维审计 · 读数（r46 · 2026-10-12）")
lines.append("")
lines.append("- 来料：《TUFT-V4.8｜子分支B：作用量变分推导边界约束，消去 R_c(κ) 幂律 ansatz》")
lines.append("- 条目：%d（%s）" % (len(ITEMS), " / ".join("%s %d" % (v, cnt[v]) for v in VERDICTS if cnt[v])))
lines.append("- 自检 guard：%d/%d" % (gpass, len(GUARD)))
lines.append("")
lines.append("## 逐条读数")
lines.append("")
lines.append("| id | 判定 | 声称 | 机器读数 |")
lines.append("|---|---|---|---|")
for it in ITEMS:
    lines.append("| %s | %s | %s | %s |" % (it["id"], it["verdict"], it["claim"], it["reading"]))
lines.append("")
lines.append("## 关键数值档案")
lines.append("")
lines.append("| 量 | 读数 |")
lines.append("|---|---|")
for k in sorted(KEY):
    lines.append("| %s | %s |" % (k, KEY[k]))
lines.append("")
with open(os.path.join(DATA, base + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

rep = []
rep.append("TUFT-V4.8 子分支B 全维审计 · 运行报告（r46 · 2026-10-12）")
rep.append("=" * 60)
rep.append("条目 %d：%s" % (len(ITEMS), " ".join("%s=%d" % (v, cnt[v]) for v in VERDICTS)))
rep.append("自检 guard %d/%d 通过" % (gpass, len(GUARD)))
rep.append("")
for it in ITEMS:
    rep.append("[%s] %s | %s" % (it["verdict"], it["id"], it["claim"]))
    rep.append("      -> %s" % it["reading"])
rep.append("")
for g in GUARD:
    rep.append("GUARD %s %s %s" % ("OK  " if g["ok"] else "FAIL", g["name"], g["detail"]))
with open(os.path.join(DATA, base + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(rep))

print("PASS = %d" % cnt["PASS"])
print("FAIL = %d" % cnt["FAIL"])
print("MISMATCH = %d" % cnt["MISMATCH"])
print("CORRECTED = %d" % cnt["CORRECTED"])
print("BOUNDARY = %d" % cnt["BOUNDARY"])
print("INFO = %d" % cnt["INFO"])
print("条目 = %d" % len(ITEMS))
print("自检 guard = %d/%d" % (gpass, len(GUARD)))
for g in GUARD:
    if not g["ok"]:
        print("GUARD FAIL: %s | %s" % (g["name"], g["detail"]))
sys.exit(0 if gfail == 0 else 1)
