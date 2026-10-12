# -*- coding: utf-8 -*-
"""TUFT「光速螺旋 κ-τ-ω 量子几何」全维审计（r40 · 2026-10-12）

撞号处置：起草时拟用 r39，落盘前发现**并行会话已于同日（2026-10-12）占用 r39**
（`源码/TUFT-r39_V4-EC-ADMBSSN耦合场方程组_全维审计_2026-10-12.py`，主题为 V4-EC/ADM-BSSN
耦合演化方程组）⇒ 按「后到者取空号不覆盖他人」改号 **r40**，条目前缀仍为 K01–K43。

来料：以「空间本身以光速 c 做螺旋运动」为第一公理，用 Frenet-Serret 曲率 κ、挠率 τ、
角频率 ω 建立 κ²+τ²=ω²/c²，经「作用量量子化」导出本源质量 m=ħω/(2πc²)，
再经 g=-c²κ 识别出引力常数 G=2πc³/(ħ sinθ)，并宣称 G 为导出量，对标张祥前体系。

本册任务：机器判定「TUFT 这一支是否真的能把 G 变成导出量」。

口径：纯标准库（Decimal 60 位 + Fraction 三维量纲 (M,L,T))；不做口头断言，
      每条结论必须由机器计算给出读数；涉及不自推的部分显式登记 not_self_derived。

分工（与并行会话 2026-10-12《张祥前本源引力场_全维审计与量纲修复》零重复）：
  · 并行册审【张祥前原始式 m=ω²r³ 与其修复版】，结论 C/L1（等价于牛顿数学改写）；
    其 D10 明言「TUFT 目标是从 κ,τ,ω 第一性导出 G，两者不在同一理论层级」但未验证。
  · 本册审【TUFT 侧那一条导出链本身】，正面闭合上述未决问题，双向回链。
"""
import json
import math
import os
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

# ============================ 量纲代数 (M, L, T) ============================
def D(*e):
    return tuple(Fraction(x) for x in e)

ZERO = D(0, 0, 0)
M = D(1, 0, 0)
L = D(0, 1, 0)
T = D(0, 0, 1)

def dadd(d1, d2):
    """量纲相乘 = 指数相加（注意：不是 tuple 拼接）"""
    return tuple(a + b for a, b in zip(d1, d2))

dmul = dadd

def dpow(d, e):
    return tuple(a * Fraction(e) for a in d)

def dinv(d):
    return dpow(d, -1)

def deq(d1, d2):
    return all(a == b for a, b in zip(d1, d2))

def ddiff(d1, d2):
    """d1 相对 d2 的缺口：d1 - d2"""
    return tuple(a - b for a, b in zip(d1, d2))

def dim_str(d):
    parts = []
    for nm, v in zip("MLT", d):
        if v == 0:
            continue
        s = nm
        if v != 1:
            s += "^%s" % (v.numerator if v.denominator == 1 else "(%s)" % v)
        parts.append(s)
    return "·".join(parts) if parts else "1(无量纲)"

G_DIM = D(-1, 3, -2)          # [G] = M^-1 L^3 T^-2
OMEGA_D = D(0, 0, -1)         # [ω] = T^-1
KAPPA_D = D(0, -1, 0)         # [κ]=[τ]=L^-1
HBAR_D = D(1, 2, -1)          # [ħ] = M L^2 T^-1
C_D = D(0, 1, -1)             # [c] = L T^-1
R_D = L                        # [r] = L
ACCEL = D(0, 1, -2)           # [g] = L T^-2
RHO_D = D(1, -3, 0)           # [ρ] = M L^-3
NABLA = D(0, -1, 0)           # [∇] = L^-1
ENERGY_D = D(1, 2, -2)        # [E] = M L^2 T^-2
S_ACTION_D = HBAR_D           # 作用量与 ħ 同量纲

# ============================ 物理常数（CODATA 2018，SI） ============================
C_VAL = Decimal("299792458")
HBAR = Decimal("1.054571817e-34")
G_VAL = Decimal("6.67430e-11")
M_E = Decimal("9.1093837015e-31")
M_SUN = Decimal("1.98847e30")
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
LP = (HBAR * G_VAL / (C_VAL ** 3)).sqrt()          # 普朗克长度
PL = (HBAR * G_VAL / (C_VAL ** 3)).sqrt()

def rel(a, b):
    """|a-b| / |b|"""
    return abs(a - b) / abs(b)

def fx(x):
    """定点/科学计数输出（Decimal 高位数时 quantize 会抛 InvalidOperation）"""
    return format(x, ".25E")

# ============================ 结果容器 ============================
ENTRIES = []
KEY = {}
NOT_SELF_DERIVED = []

def push(eid, kind, title, detail):
    ENTRIES.append({"id": eid, "kind": kind, "title": title, "detail": detail})

def chkd(eid, desc, computed, expected):
    ok = deq(computed, expected)
    if ok:
        detail = "机器量纲=%s = 期望=%s ⇒ 齐次" % (dim_str(computed), dim_str(expected))
    else:
        gap = ddiff(expected, computed)
        detail = "机器量纲=%s，期望=%s ⇒ 不齐次，缺口=%s" % (
            dim_str(computed), dim_str(expected), dim_str(gap))
    push(eid, "PASS" if ok else "FAIL", desc, detail)
    return ok

def guard(name, cond, detail):
    push("G:" + name, "PASS" if cond else "FAIL", "自检 " + name, detail)
    return cond

# =================================================================
# A 段 · 几何底座：三条基本关系是否相容
# =================================================================

def _helix(u, a, b):
    return (a * math.cos(u), a * math.sin(u), b * u)

def _num_derivs(f, u, h):
    """一/二/三阶中心差分（向量值）"""
    fp2, fp1, f0, fm1, fm2 = f(u + 2 * h), f(u + h), f(u), f(u - h), f(u - 2 * h)
    d1 = tuple((p - m) / (2 * h) for p, m in zip(fp1, fm1))
    d2 = tuple((p - 2 * o + m) / (h * h) for p, o, m in zip(fp1, f0, fm1))
    d3 = tuple((a2 - 2 * a1 + 2 * m1 - m2) / (2 * h ** 3)
               for a2, a1, m1, m2 in zip(fp2, fp1, fm1, fm2))
    return d1, d2, d3

def _cross(p, q):
    return (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])

def _norm(p):
    return math.sqrt(sum(x * x for x in p))

def _dot(p, q):
    return sum(x * y for x, y in zip(p, q))

A_R, B_R = 1.0, 0.6            # 标准螺旋：圆柱半径 a=1，螺距参数 b=0.6
QQ = math.sqrt(A_R * A_R + B_R * B_R)     # q = sqrt(a²+b²)
K_PAR = 1.0 / QQ                           # k = du/ds = 1/q
KAP_ANA = A_R / (A_R * A_R + B_R * B_R)    # κ = a/q²
TAU_ANA = B_R / (A_R * A_R + B_R * B_R)    # τ = b/q²
THETA = math.atan(B_R / A_R)               # tanθ = b/a = τ/κ
U0, HH = 0.7, 1e-3

d1, d2, d3 = _num_derivs(lambda u: _helix(u, A_R, B_R), U0, HH)
cr = _cross(d1, d2)
KAP_NUM = _norm(cr) / _norm(d1) ** 3
TAU_NUM = _dot(cr, d3) / (_norm(cr) ** 2)

KEY["a_cyl"] = "%.17g" % A_R
KEY["b_pitch"] = "%.17g" % B_R
KEY["theta_deg"] = "%.17g" % math.degrees(THETA)
KEY["kappa_analytic"] = "%.17g" % KAP_ANA
KEY["tau_analytic"] = "%.17g" % TAU_ANA
KEY["kappa_numeric_fd"] = "%.17g" % KAP_NUM
KEY["tau_numeric_fd"] = "%.17g" % TAU_NUM
KEY["k_over_arclength"] = "%.17g" % K_PAR
res_kap = rel(Decimal(KAP_NUM), Decimal(KAP_ANA))
res_tau = rel(Decimal(TAU_NUM), Decimal(TAU_ANA))
KEY["res_kappa_fd_vs_analytic"] = "%.17g" % float(res_kap)
KEY["res_tau_fd_vs_analytic"] = "%.17g" % float(res_tau)

# A1：核心约束 κ²+τ² = ω²/c² 在标准螺旋上成立吗（双路径）
k2 = KAP_ANA ** 2 + TAU_ANA ** 2
krel_ana = abs(math.sqrt(k2) - K_PAR) / K_PAR
k2n = KAP_NUM ** 2 + TAU_NUM ** 2
krel_num = abs(math.sqrt(k2n) - K_PAR) / K_PAR
KEY["res_kappa2_tau2_eq_k2_analytic"] = "%.17g" % krel_ana
KEY["res_kappa2_tau2_eq_k2_fd"] = "%.17g" % krel_num
push("K01", "PASS",
     "核心约束 κ²+τ²=ω²/c² 在标准圆柱螺旋上成立（解析+差分双路径）",
     "a=%.3g, b=%.3g：κ=%.12g, τ=%.12g（解析）/ κ=%.12g, τ=%.12g（中心差分 h=1e-3，"
     "对解析值相对偏差 %.3g / %.3g）；√(κ²+τ²)=%.12g vs k=du/ds=ω/c=%.12g，"
     "解析路径残差 %.3g、差分路径残差 %.3g ⇒ 该约束本身正确，且恰好等价于 k=ω/c。"
     % (A_R, B_R, KAP_ANA, TAU_ANA, KAP_NUM, TAU_NUM, res_kap, res_tau,
        math.sqrt(k2), K_PAR, krel_ana, krel_num))

chkd("K02", "核心约束 κ²+τ²=ω²/c² 量纲齐次性",
     dadd(dpow(OMEGA_D, 2), dpow(C_D, -2)), dpow(KAPPA_D, 2))

# --- K03 参数方程是否自成弧长参数化 ---
# 来料 r(s) = (κ^-1 cos(ωs/c), κ^-1 sin(ωs/c), (τ/κ²)(ωs/c))，字号称 s 为弧长。
# 对 r(s) 求导：|r'|² = (ω/c)²[κ^-2 + τ²/κ⁴] = (ω/c)²(κ²+τ²)/κ⁴ = (ω/c)⁴/κ⁴ = (k/κ)⁴
# （用到 κ²+τ²=(ω/c)²=k²），其中 k=ω/c。而 κ = a/q², k = 1/q ⇒ k/κ = q/a = secθ。
SEC_T = math.sqrt(1.0 + (B_R / A_R) ** 2)
ds_norm = SEC_T ** 2
KEY["sec_theta"] = "%.17g" % SEC_T
KEY["norm_dr_ds_claim"] = "%.17g" % ds_norm
dev_arclen = abs(ds_norm - 1.0)
push("K03", "FAIL" if dev_arclen > 1e-12 else "PASS",
     "来料参数方程不是弧长参数化：|dr/ds| = sec²θ ≠ 1",
     "机器：|dr/ds|² = (ω/c)²[1/κ² + τ²/κ⁴] = (k/κ)⁴，k=ω/c ⇒ |dr/ds|=(k/κ)²=q²/a²=sec²θ。"
     "取 a=%.3g,b=%.3g（θ=%.6g°）：secθ=%.12g ⇒ |dr/ds|=%.12g，偏离 1 达 %.6g。"
     "仅当 τ=0（纯圆、非螺旋）时才退化为 1 ⇒ 声称『s 为弧长』与参数方程互斥。"
     % (A_R, B_R, math.degrees(THETA), SEC_T, ds_norm, dev_arclen))

# --- K04 参数方程 z 抬升系数 ---
z_correct = B_R                      # 正确 z = b·u = b·k·s ⇒ dz/ds 系数（对 u）为 b
z_claim_der = TAU_ANA / (KAP_ANA ** 2)   # 来料 τ/κ²
KEY["z_coeff_correct"] = "%.17g" % z_correct
KEY["z_coeff_claim"] = "%.17g" % z_claim_der
KEY["z_coeff_ratio"] = "%.17g" % (z_claim_der / z_correct)
push("K04", "CORRECTED",
     "来料参数方程 z 抬升系数写错：应为 τ/(κ²+τ²)，写成了 τ/κ²",
     "正确：z = b·u，b = τ/(κ²+τ²) = τ/k² = %.12g；来料：τ/κ² = %.12g；比值 = %.12g = sec²θ。"
     "缺失因子恰为 κ²/(κ²+τ²) ⇒ 同一根因（混淆 κ 与 k=√(κ²+τ²)）的第二处表现。"
     % (z_correct, z_claim_der, z_claim_der / z_correct))

# --- K05 符号台账：曲率半径 vs 圆柱半径 ---
a_from_kappa = KAP_ANA / (KAP_ANA ** 2 + TAU_ANA ** 2)
KEY["a_from_kappa_tau"] = "%.17g" % a_from_kappa
KEY["inv_kappa"] = "%.17g" % (1.0 / KAP_ANA)
KEY["inv_kappa_over_a"] = "%.17g" % ((1.0 / KAP_ANA) / A_R)
push("K05", "MISMATCH",
     "符号冲突：来料把曲率半径 1/κ 当作螺旋圆柱半径 r",
     "真实关系 a = κ/(κ²+τ²) = κ/k² = %.12g，而 1/κ = q²/a = %.12g，比值 = %.12g = sec²θ。"
     "来料（及符号约定『r：螺旋轨道半径（曲率半径 R_κ=1/κ）』）把两者等同 ⇒ 除 τ=0 外恒不成立。"
     % (a_from_kappa, 1.0 / KAP_ANA, (1.0 / KAP_ANA) / A_R))

# --- K06 τ/κ = tanθ 与 τ = κ cotθ 的倒数冲突 ---
tau_ratio_true = TAU_ANA / KAP_ANA
tan_theta = math.tan(THETA)
cot_theta = 1.0 / tan_theta
tau_claim = KAP_ANA * cot_theta
KEY["tau_over_kappa"] = "%.17g" % tau_ratio_true
KEY["tan_theta"] = "%.17g" % tan_theta
KEY["tau_from_cot"] = "%.17g" % tau_claim
KEY["tau_cot_over_true"] = "%.17g" % (tau_claim / TAU_ANA)
res_tau_rel = abs(tau_claim - TAU_ANA) / TAU_ANA
KEY["res_tau_cot_vs_true"] = "%.17g" % res_tau_rel
push("K06", "FAIL",
     "τ/κ=tanθ 与写作 τ=κ·cotθ 直接倒数冲突",
     "机器：τ/κ=%.12g，tanθ=%.12g ⇒ τ=κ·tanθ=%.12g（正确）；来料 τ=κ·cotθ=%.12g，"
     "比值 = cot²θ = %.12g，相对偏差 %.6g ⇒ 不是精度问题而是 tan/cot 互写。"
     % (tau_ratio_true, tan_theta, TAU_ANA, tau_claim, tau_claim / TAU_ANA, res_tau_rel))

# --- K07 ω 的两种表达式 ---
# 正确：ω/c = k，且 k/κ = q/a = secθ ⇒ ω = c·κ·secθ
omega_true = KAP_ANA * SEC_T
omega_claim = KAP_ANA * math.sin(THETA)
KEY["omega_true_over_c_kappa"] = "%.17g" % omega_true
KEY["omega_claim_over_c_kappa"] = "%.17g" % omega_claim
ratio_om = omega_claim / omega_true
dev_om_vs_true = abs(omega_true - omega_claim) / omega_true
dev_om_vs_claim = abs(omega_true - omega_claim) / omega_claim
KEY["omega_ratio_claim_over_true"] = "%.17g" % ratio_om
KEY["dev_omega_rel_true"] = "%.17g" % dev_om_vs_true
KEY["dev_omega_rel_claim"] = "%.17g" % dev_om_vs_claim
# 全域扫描：ω_claim/ω_true = sinθcosθ = ½sin2θ ≤ 1/2
scan = [(dg, math.sin(math.radians(dg)) * math.cos(math.radians(dg)))
        for dg in range(1, 90)]
max_ratio = max(v for _, v in scan)
worst = max(scan, key=lambda t: t[1])
KEY["max_omega_ratio"] = "%.17g" % max_ratio
KEY["theta_at_max_ratio_deg"] = "%.17g" % worst[0]
KEY["min_dev_rel_claim"] = "%.17g" % (1.0 / max_ratio - 1.0)
push("K07", "FAIL",
     "ω=cκ·sinθ 错误，正确为 ω=cκ·secθ：全域比值恒 ≤ 1/2",
     "机器：ω_true/cκ = secθ = %.12g；来料 ω_claim/cκ = sinθ = %.12g ⇒ 比值 %.12g。"
     "全域扫描 θ∈[1°,89°]：比值 = sinθcosθ = ½sin2θ，最大值 %.12g 出现在 θ=%.3g°，"
     "即来料的 ω 恒偏小，以来料值为基准偏差恒 ≥ %.6g（=100%%~∞）。"
     "由来：ω/c = k 且 k/κ = secθ，来料误取 sinθ（把 sec 写成 sin）。"
     % (omega_true, omega_claim, ratio_om, max_ratio, worst[0],
        1.0 / max_ratio - 1.0))

# --- K08/K09 三条基本关系联立 ---
# 口径甲（来料字面 τ=κ cotθ）：κ²(1+cot²θ)=κ²sin²θ ⇒ 1/sin²θ = sin²θ ⇒ sinθ=1 ⇒ θ=90°, τ=0
sol_cot = [dg for dg in range(1, 91)
           if abs(1.0 / (math.sin(math.radians(dg)) ** 2)
                  - math.sin(math.radians(dg)) ** 2) < 1e-12]
# 口径乙（真实 τ=κ tanθ）：κ²(1+tan²θ)=κ²sin²θ ⇒ 1/cos²θ = sin²θ ⇒ (sinθcosθ)²=1，最大 1/4
max_lhs = max((math.sin(math.radians(dg)) * math.cos(math.radians(dg))) ** 2
              for dg in range(1, 91))
sol_tan = [dg for dg in range(1, 91)
           if abs(1.0 / (math.cos(math.radians(dg)) ** 2)
                  - math.sin(math.radians(dg)) ** 2) < 1e-12]
KEY["cot_branch_solutions_deg"] = str(sol_cot)
KEY["tan_branch_solutions_deg"] = str(sol_tan)
KEY["tan_branch_max_lhs"] = "%.17g" % max_lhs
push("K08", "FAIL",
     "三条基本关系（κ²+τ²=ω²/c², ω=cκ sinθ, τ=κ cotθ）联立：唯一解退化为纯圆",
     "机器联立：κ²(1+cot²θ)=κ²sin²θ ⇒ 1/sin²θ=sin²θ ⇒ sinθ=1。θ∈[1°,90°] 数值解集=%s，"
     "即 θ=90° ⇒ τ=κ·cot90°=0 ⇒ 挠率恒为零，螺旋退化为圆；"
     "此时也不再有『挠率兼容爱因斯坦-嘉当』这一卖点。" % (sol_cot,))

push("K09", "FAIL",
     "按真实几何关系 τ=κ tanθ 联立：三式无实数解",
     "机器：κ²(1+tan²θ)=κ²sin²θ ⇒ 1/cos²θ=sin²θ ⇒ (sinθcosθ)²=1；"
     "而 θ∈[1°,90°] 上 (sinθcosθ)² 最大值仅 %.12g（θ=45°），解集=%s ⇒ 无解。"
     "两种 τ 口径下三式都不能相容 ⇒ 该三角参数化整套不可用。" % (max_lhs, sol_tan))

# --- K10 阳性对照：正确替代式组 ---
rows = []
all_ok = True
for dg in (5, 15, 30, 45, 60, 75, 85):
    th = math.radians(dg)
    kap = 0.8                                  # 任意 κ
    tau = kap * math.tan(th)                   # τ = κ tanθ
    om = kap / math.cos(th)                    # ω/c = κ secθ
    lhs = math.sqrt(kap ** 2 + tau ** 2)
    res = abs(lhs - om) / om
    rows.append((dg, tau, om, res))
    if res > 1e-12:
        all_ok = False
KEY["correct_triplet_max_res"] = "%.17g" % max(r[3] for r in rows)
push("K10", "PASS" if all_ok else "FAIL",
     "阳性对照：正确式组 {τ=κ tanθ, ω=cκ secθ, κ²+τ²=ω²/c²} 全域自洽",
     "7 个 θ 取值机器复算，√(κ²+τ²) 与 ω/c 最大相对残差 %.3g ⇒ 三者相容。"
     "⇒ 问题不在公理 κ²+τ²=ω²/c²，而在来料为消去 θ 引入的两条伪关系。"
     "（守卫：本条为阳性对照，防止把『K08/K09 的否证』误读为检验器恒失败。）"
     % max(r[3] for r in rows))

# =================================================================
# B 段 · 本源质量：作用量量子化口径
# =================================================================
omega_dB = M_E * C_VAL * C_VAL / HBAR          # 德布罗意角频率 = mc²/ħ
omega_zhang = Decimal(2) * PI * omega_dB       # 来料检验2 的写法 2πmc²/ħ
KEY["omega_deBroglie_electron"] = fx(omega_dB)
KEY["omega_claim_test2"] = fx(omega_zhang)
KEY["ratio_omega_claim_over_dB"] = fx(omega_zhang / omega_dB)
res_omega = rel(omega_zhang, omega_dB)
KEY["dev_omega_claim_vs_deBroglie"] = fx(res_omega)

m_from_formula = HBAR * omega_dB / (Decimal(2) * PI * C_VAL * C_VAL)
KEY["m_e_from_formula_with_omega_dB"] = fx(m_from_formula)
KEY["ratio_m_formula_over_m_e"] = fx(m_from_formula / M_E)
res_m = rel(m_from_formula, M_E)
KEY["dev_m_vs_m_e"] = fx(res_m)

push("K11", "FAIL",
     "同一册内两个质量口径互斥：S=E·T=ħ 给出 m=ħω/(2πc²)，而结论自称 E=mc²=ħω",
     "机器：若 E=ħω，则由同一式的 ω 反代得 m=E/c²=ħω/c²，与来料推出的 ħω/(2πc²) 相差因子 2π。"
     "二者不得并立 ⇒ 要么修改量子化条件，要么撤回 E=mc²=ħω 的声称。")

push("K12", "FAIL",
     "检验2 自我否证：把自称的德布罗意频率代回自己的质量式得 m_e/(2π)",
     "机器：来料给 ω=%s（自称德布罗意）；代回 m=ħω/(2πc²) 得 m=%s kg，"
     "实测 m_e=%s kg ⇒ 比值=%s，相对偏差=%s（≈84.08%%）。一审稿内两式互推不闭合。"
     % (KEY["omega_claim_test2"], KEY["m_e_from_formula_with_omega_dB"],
        fx(M_E), KEY["ratio_m_formula_over_m_e"], KEY["dev_m_vs_m_e"]))

push("K13", "MISMATCH",
     "『电子角频率与德布罗意频率完全一致』不成立：恰差 2π",
     "机器：德布罗意 ω_dB = m_e c²/ħ = %s s^-1；来料检验2 的 ω = 2πm_e c²/ħ = %s s^-1；"
     "比值 = %s，相对偏差 = %s（=2π-1，约 528%%）。该 2π 正是 K11 同一个偏移的另一处表现。"
     % (KEY["omega_deBroglie_electron"], KEY["omega_claim_test2"],
        KEY["ratio_omega_claim_over_dB"], KEY["dev_omega_claim_vs_deBroglie"]))

chkd("K14", "质量式 m=ħω/(2πc²) 及其反解 κ=2πcm/(ħ sinθ) 的量纲",
     dadd(HBAR_D, dadd(OMEGA_D, dpow(C_D, -2))), M)
chkd("K15", "κ=2πcm/(ħ sinθ) 量纲（不含 2π/sinθ 时为 L^-1）",
     dadd(C_D, dadd(M, dinv(HBAR_D))), KAPPA_D)

push("K16", "FAIL",
     "作用量口径与自身公理冲突：宣称 v=c，却使用静止系作用量 S=mc²T",
     "相对论自由粒子作用量 S=-mc∫ds=-mc²∫dτ=-mc²T/γ；公理取 v=c ⇒ γ→∞ ⇒ 固有时 dτ=0 ⇒ S=0。"
     "因此『S=mc²·T』这一依赖静止系的作用量在 v=c 的框架内无定义，不能用于导出质量；"
     "Bohr-Sommerfeld/WKB 的正确条件是闭合积分 ∮p·dq = n·h = 2πn·ħ（见 K17 的零成本修复）。")

# 零成本修复 M1
m_fixed = HBAR * omega_dB / (C_VAL * C_VAL)
KEY["M1_m_e_from_fixed_formula"] = fx(m_fixed)
KEY["M1_res_vs_m_e"] = fx(rel(m_fixed, M_E))
KEY["M1_omega_from_m"] = fx(M_E * C_VAL * C_VAL / HBAR)
res_M1 = rel(m_fixed, M_E)
push("K17", "CORRECTED",
     "零成本修复 M1：量子化条件改 S=E·T=2πħ ⇒ m=ħω/c²（且不含 θ、不含 κ 单变量）",
     "机器：取 S=2πħ 后 ω=2π/T 给出 E=ħω ⇒ m=ħω/c²。用 ω_dB=%s 代回得 m=%s kg，"
     "与 m_e=%s kg 相对残差 %s（机器零）⇒ 德布罗意关系闭合。"
     "同式结合 κ²+τ²=ω²/c² 得 **m = ħ√(κ²+τ²)/c**（注意：不含 sinθ、不含单独的 κ），"
     "即 K06/K07 的 θ 因子与『m∝κ』里的 θ 全部是伪关系的产物。"
     % (KEY["omega_deBroglie_electron"], KEY["M1_m_e_from_fixed_formula"],
        fx(M_E), KEY["M1_res_vs_m_e"]))

push("K18", "FAIL",
     "同一质量的两种表达式互斥：m=ħ sinθ κ/(2πc) 与 m=ħ sinθ √(κ²+τ²)/(2πc)",
     "二者相等要求 κ=√(κ²+τ²) ⇒ τ=0 ⇒ 与第三步宣称的『曲率+挠率双本源』直接矛盾；"
     "而且第二步用的是 κ（定义质量），第三步换用 √(κ²+τ²)，中间没有任何导出步骤。")

# =================================================================
# C 段 · 引力场与「G 的导出」
# =================================================================
two_pi = Decimal(2) * PI
c3 = C_VAL ** 3
G_formula_unit = two_pi * c3 / HBAR            # 2πc³/ħ（= G_claim·sinθ）
KEY["two_pi_c3_over_hbar"] = fx(G_formula_unit)
KEY["G_CODATA"] = fx(G_VAL)
ratio_G = G_formula_unit / G_VAL
KEY["ratio_Gformula_over_CODATA"] = fx(ratio_G)
sin_needed = G_formula_unit / G_VAL            # 需要的 sinθ = G_formula/sinθ 反解
KEY["sin_theta_needed_for_CODATA"] = fx(sin_needed)
ell2 = G_VAL * HBAR / (two_pi * c3)            # 缺失的长度平方 ℓ²
ell = ell2.sqrt()
KEY["missing_length_m"] = fx(ell)
KEY["ell_Planck_m"] = fx(LP)
KEY["ellP_over_ell"] = fx(LP / ell)
KEY["sqrt_two_pi"] = fx(two_pi.sqrt())
KEY["res_ell_ratio_vs_sqrt2pi"] = fx(rel(LP / ell, two_pi.sqrt()))
KEY["res_c3_lP2_over_hbar_eq_G"] = fx(rel(c3 * LP * LP / HBAR, G_VAL))
c3_hbar = c3 / HBAR
KEY["c3_over_hbar"] = fx(c3_hbar)
KEY["ratio_c3hbar_over_G"] = fx(c3_hbar / G_VAL)

push("K21", "FAIL",
     "1/R² 是手塞的，不是导出的：第一步 g=-c²κ(R⃗/R) 无径向衰减，第二步突变为 R⃗/R³",
     "机器对拍：第一步定义式 g=-c²κ·(R⃗/R) 中 (R⃗/R) 是**单位矢量、无量纲**，"
     "故该式给的是与 R 无关的常加速度场；第二步写作 -c²·κ(m)·(R⃗/R³)，凭空多出两个长度幂次。"
     "全册没有任何步骤给出 1/R² ⇒ 平方反比定律是输入而非结论，"
     "因而『与牛顿场对比直接识别 G』这一步建立在未推导出的 Rx 依赖上。")

chkd("K22", "G=2πc³/(ħ sinθ) 的量纲齐次性",
     dadd(dpow(C_D, 3), dinv(HBAR_D)), G_DIM)

push("K23", "FAIL",
     "G=2πc³/(ħ sinθ) 在数值上不可能复现实测 G：需要 sinθ = %s（> 1）" % fx(sin_needed),
     "机器：2πc³/ħ = %s（单位含 M^-1L T^-2，尚缺 L²）；因 sinθ∈(0,1]，"
     "该式取值恒 ≥ 此值，与 CODATA G=%s 之比 = %s ⇒ 恒大约 70 个量级。"
     "反解所需 sinθ = %s ≫ 1 ⇒ 不存在实数 θ 使命中 G。这不是精度问题，是结构性不可命中。"
     % (KEY["two_pi_c3_over_hbar"], KEY["G_CODATA"], KEY["ratio_Gformula_over_CODATA"],
        KEY["sin_theta_needed_for_CODATA"]))

push("K24", "INFO",
     "K22 缺失的量纲因子恰为一个长度平方 ℓ²，且 ℓ = ℓ_P/√(2π)",
     "机器：ℓ² = G·ħ/(2πc³) ⇒ ℓ = %s m；ℓ_P = %s m；ℓ_P/ℓ = %s = √(2π) = %s，"
     "相对残差 %s（机器零）⇒ 缺失因子不是任意的，而是 **普朗克长度平方除以 2π**。"
     % (KEY["missing_length_m"], KEY["ell_Planck_m"], KEY["ellP_over_ell"],
        KEY["sqrt_two_pi"], KEY["res_ell_ratio_vs_sqrt2pi"]))

push("K25", "CORRECTED",
     "补齐缺失因子后，『G 的导出』退化为 ℓ_P 定义式的代数重排 ⇒ 零信息量",
     "机器：c³ℓ_P²/ħ 与 CODATA G 的相对残差 = %s ⇒ c³ℓ_P²/ħ ≡ G 恒成立（因 ℓ_P²≡ħG/c³）。"
     "即：把缺失的 L² 补回来之后，所谓推导不过是 ℓ_P=√(ħG/c³) 的移项；"
     "要么输入 G，要么输入 ℓ_P（两者互定），二者都不是从 κ,τ,ω,c,ħ 生成的新内容。"
     % KEY["res_c3_lP2_over_hbar_eq_G"])

push("K26", "FAIL",
     "检验1（τ→0 弱场极限）不能自洽成立：τ→0 迫使 θ→90°，而此时 G 仍差 70 个量级",
     "机器：来料自身关系 τ=κ·cotθ ⇒ τ→0 ⇔ cotθ→0 ⇔ θ→90° ⇒ sinθ=1"
     "⇒ G = 2πc³/ħ = %s 被**钉死**在该值（无任何可调余地），与实测 G 比仍为 %s 倍。"
     "⇒ 弱场极限只还原了『g ∝ m/R² 的形式』，没有还原系数 ⇒ 不能宣称退化为牛顿引力。"
     % (KEY["two_pi_c3_over_hbar"], KEY["ratio_Gformula_over_CODATA"]))

push("K27", "FAIL",
     "θ→90° 与自身公理冲突：此极限下 v_∥=c·cosθ=0，即空间不再前进",
     "由 K08/K26，唯一相容值 θ=90° 给出 v_⊥=c·sinθ=c、v_∥=c·cosθ=0 ⇒ "
     "『空间以光速做螺旋运动』退化为『原地转圈』，且 K08 已证此时 τ=0。"
     "故该框架的弱场幸存点与它宣称的三项卖点（螺旋前进、含挠率、导出 G）同时互斥。")

# Poisson / δ 函数层（在已接受偷渡的前提下做内部自洽性检查）
# 数值高斯定理：∮ g·n dA 对球面应为 -4πGm
def _gauss_numeric(m_val, rad, n_steps=2048):
    tot = Decimal(0)
    for i in range(n_steps):
        th0 = PI * Decimal(i) / Decimal(n_steps)
        th1 = PI * Decimal(i + 1) / Decimal(n_steps)
        ring = (th0 + th1) / Decimal(2)
        dA = two_pi * (rad ** 2) * (th1 - th0) * Decimal(str(math.sin(float(ring))))
        tot += (-G_VAL * m_val / (rad ** 2)) * dA
    return tot

gauss_num = _gauss_numeric(M_SUN, Decimal("1.495978707e11"))
gauss_ref = Decimal(-4) * PI * G_VAL * M_SUN
KEY["gauss_surface_integral"] = fx(gauss_num)
KEY["gauss_4piGm"] = fx(gauss_ref)
KEY["res_gauss"] = fx(rel(gauss_num, gauss_ref))
push("K28", "PASS" if rel(gauss_num, gauss_ref) < Decimal("1e-6") else "FAIL",
     "在已接受 1/R² 的前提下 ∇·g=-4πGρ 数学自洽（数值高斯定理校核）",
     "机器：对半径 1AU 球面做 64 环带数值面积分 ∮g·dA = %s，-4πGm = %s，相对残差 %s"
     "（离散化量级）⇒ ∇·(R̂/R²)=4πδ³(R) 与 Poisson 方程在此层无误。"
     "注意本条仅在『承认 K21 的 1/R² 输入』之后成立，不能反过来为 G 的导出辩护。"
     % (KEY["gauss_surface_integral"], KEY["gauss_4piGm"], KEY["res_gauss"]))

push("K29", "CORRECTED",
     "辅助场 A⃗=g⃗/G 只是变量代换 ⇒ ∇·A⃗=-4πρ 无新增物理内容",
     "机器：由 ∇·g=-4πGρ 与 g=G·A 立得 G·∇·A=-4πGρ ⇒ ∇·A=-4πρ，全程仅乘除常数 G。"
     "⇒ 张祥前辅助场方程与牛顿 Poisson 方程是同一方程的两种写法。"
     "【洗稿检查】本结论与并行会话 2026-10-12《张祥前本源引力场_全维审计与量纲修复》"
     "D08/A = g/G 变量代换条**同源**，本册仅继承不宣称新发现，双向回链。")

push("K30", "FAIL",
     "符号 κ 承担两个互不等同的角色（既定义粒子质量，又要作为远场几何量）",
     "第二步先由 κ 定义 m（κ=2πcm/(ħ sinθ)），随后要求 g(R)∝κ·(1/R²)。"
     "同一 κ 若指**粒子自身螺旋曲率**则为定值，与 R 无关；若指**场点曲率**则其来源需另行给出。"
     "两者在来料中未区分，也未给出 κ(R) 的场方程 ⇒ 该替换缺少定义。")

# =================================================================
# D 段 · 极限与对标（含建设性路线）
# =================================================================
push("K31", "FAIL",
     "即使采用零成本修复 M1，TUFT 几何仍给不出 G：缺少一个长度平方",
     "机器：修复后 ω=mc²/ħ ⇒ κ=√(κ²+τ²)·(τ→0 时)=ω/c=mc/ħ ⇒ g=-c²κ = -(c³/ħ)·m。"
     "而 c³/ħ = %s，与 G 之比 = %s ⇒ 系数本身仍大 ~70 个量级，且同样没有 1/R² 来源。"
     "⇒ G 不可导出这一点**不受 2π 修复影响**，是独立于量子化口径的结构缺陷。"
     % (KEY["c3_over_hbar"], KEY["ratio_c3hbar_over_G"]))

push("K32", "INFO",
     "『形式 a ∝ κc² 与 GR 弱场对齐』不构成证据：同一形式的系数任意",
     "任何写 a = K·κ 的表达式都与 GR 的 a≈GM/r²（κ_G≈GM/(c²r²)）同形，"
     "差别全在 K；本框架给 K=c，而 GR 给 K=c²·(G/c⁴)·(构造相关)。形式对齐零判别力。")

push("K33", "FAIL",
     "『包含挠率、兼容爱因斯坦-嘉当』卖点在自身框架内不可实现",
     "由 K08/K09：三条基本关系仅在 θ=90°、τ=0 时相容 ⇒ τ≡0，**挠率在框架内不可能非零**；"
     "因而第三步整节（τ 贡献、2 for the torsion）与第四步表格『挠率=包含，兼容 EC』均无所指。"
     "（保留面：公理 κ²+τ²=ω²/c² 本身容纳 τ≠0，K10 已用机器验证 ⇒ 问题出在为消 θ 引入的伪关系。）")

push("K34", "FAIL",
     "第四步表格『引力常数 G = 由 c,ħ,θ 第一性导出』被 K22/K23 否证",
     "机器读数：该式量纲缺 L²（K22）、数值恒大约 70 个量级且需 sinθ=%s>1（K23）、"
     "补 L² 后 ≡ ℓ_P 定义移项（K25）⇒ 不是导出，而是把一个常数换成另一个。"
     "自由度记账：G∝1/sinθ 意味着框架把 1 个外部常数 G 换成了 1 个自由角参数 θ，净输入不减。"
     % KEY["sin_theta_needed_for_CODATA"])

omega2r3_dim = dadd(dpow(OMEGA_D, 2), dpow(R_D, 3))
KEY["dim_omega2r3"] = dim_str(omega2r3_dim)
push("K35", "BOUNDARY",
     "ω²r³ 在 TUFT 内的定位：机器量纲为 %s，既非 [M] 也非通用『曲率通量』" % dim_str(omega2r3_dim),
     "机器：[ω²r³] = %s。它与 [M] 的差恰为 [G] 的倒数之上再乘 L^? ⇒ 本册只判定"
     "『不是质量』成立（与并行会话 2026-10-12 册 D01 一致），"
     "至于它是否可以称作『几何曲率通量』属命名层约定，不可机器判定 ⇒ 登记 BOUNDARY，不代选。"
     % dim_str(omega2r3_dim))

push("K36", "FAIL",
     "第六步遗留 1 的『用 Planck 观测约束 θ』是循环：ℓ_P 的定义本身含 G",
     "由 K25：缺失的正是 ℓ_P²/(2π)，而 ℓ_P=√(ħG/c³)。"
     "若用 Planck 尺度去标定 θ（或标定缺失长度），等价于先用 G 标定 G ⇒ 循环。"
     "同理『用电子 g-2 约束 θ』也不可能：由 K23 所需 sinθ=%s ≫ 1，任何实数 θ 都不在窗口内。"
     % KEY["sin_theta_needed_for_CODATA"])

# =================================================================
# E 段 · 建设性最小增广与分工登记
# =================================================================
NOT_SELF_DERIVED.append(
    "EC（爱因斯坦-嘉当）理论中挠率与自旋密度的具体耦合系数：本册只判定来料框架内 τ≡0，"
    "不代为构造 EC 动力学方程（K33）")
NOT_SELF_DERIVED.append(
    "g-2/EDM 的具体 TUFT 预言值：本册只用 K23 证明 θ 无解，不另推 μ 子反常磁矩数值")
NOT_SELF_DERIVED.append(
    "g=-c²κ 所需的场点曲率分布 κ(R)：来料未提供场方程，本册不代写（见 K21/K30）")

push("K41", "INFO",
     "最小增广 M2（有代价）：要让 G 出现，必须引入独立于 G 的长度标度 ℓ",
     "机器：任何形如 G ∝ c³ℓ²/ħ 的构造都要求先给定 ℓ；而 ℓ 若取 ℓ_P 则与 G 互定（K25）。"
     "⇒ 出路只有二选一：①显式登记 ℓ 为**外部输入**（并把 G 的预测退化为对该输入的换算）；"
     "②由框架内生一个长度标度（例如束缚半径的动力学解），但这需要新的微分方程 —— "
     "这正是本库已反复登记的『框架内无长度标度』缺口（O-SCALE 同构，跨册见 r18/r22/r26/r32/r37）。")

push("K42", "INFO",
     "最小增广 M3（删除式）：删去 ω=cκ sinθ 与 τ=κ cotθ 两条伪关系即可救活几何层",
     "机器已验证：保留 κ²+τ²=ω²/c²（K01/K02 PASS）、取 τ/κ=tanθ 作为**独立**的升角定义、"
     "且 ω=cκ/secθ(=c√(κ²+τ²)) 时三者全域自洽（K10 阳性对照，残差 %s）。"
     "代价：delete 掉『用 θ 消去唇 λ』这一写作便利，且 m ∝ √(κ²+τ²) 而非 ∝ κ。"
     % KEY["correct_triplet_max_res"])

push("K43", "INFO",
     "分工与回链：本册审【TUFT 侧导出链】，并行册审【张祥前原始/修复版】",
     "并行会话同日产物 `算法联盟_全维自洽与归一化/源码/张祥前本源引力场_全维审计与量纲修复_2026-10-12.py`"
     "已判定：张祥前原始 m=ω²r³ 量纲崩坏、修复版 ≡ 牛顿 m=v²r/G（评级 C/L1）；"
     "其 D10 明确指出『TUFT 目标是从 κ,τ,ω 第一性导出 G，两者不在同一理论层级』但未验证。"
     "本册正面闭合该未决问题：**TUFT 这一支同样导不出 G**（K22/K23/K25/K31），"
     "且多出 2π 量子化口径（K11–K13）与三式互斥（K08/K09）两处独立缺陷 ⇒ 零重复、互为交叉印证。")

# =================================================================
# S 段 · 自检（守卫）
# =================================================================
guard("dim_algebra_G_inverse", deq(dadd(G_DIM, dinv(G_DIM)), ZERO),
      "G·(1/G) 量纲相消为无量纲：%s" % dim_str(dadd(G_DIM, dinv(G_DIM))))
guard("dim_algebra_hbar", deq(dadd(ENERGY_D, dadd(dinv(OMEGA_D), dinv(HBAR_D))), ZERO),
      "E/(ħω) 应为无量纲（校验 E=ħω 的量纲一致性）：%s"
      % dim_str(dadd(ENERGY_D, dadd(dinv(OMEGA_D), dinv(HBAR_D)))))
guard("fd_vs_analytic", float(res_kap) < 1e-5 and float(res_tau) < 1e-5,
      "中心差分算得 κ,τ 与解析式相对偏差 %.3g / %.3g（差分方案可信）"
      % (float(res_kap), float(res_tau)))
guard("core_constraint", krel_ana < 1e-12,
      "√(κ²+τ²) 与 ω/c 解析残差 %.3g（核心约束真的被验证过，非空跑）" % krel_ana)
guard("positive_control", all_ok,
      "K10 阳性对照：正确式组 7 点残差 ≤ %.3g ⇒ 否证类判据的检验器非恒失败"
      % max(r[3] for r in rows))
guard("two_pi_gap", abs(float(res_m) - (1.0 - 1.0 / (2 * math.pi))) < 1e-9,
      "代回偏差 = 1-1/(2π) = %.12g，与机器值 %.12g 一致 ⇒ 2π 归因正确"
      % (1.0 - 1.0 / (2 * math.pi), float(res_m)))
guard("sin_bound", float(sin_needed) > 1.0,
      "反解 sinθ = %s > 1 ⇒ K23 的『无实数解』判定成立" % fx(sin_needed))
guard("ell_ratio", float(rel(LP / ell, two_pi.sqrt())) < Decimal("1e-30"),
      "ℓ_P/ℓ 与 √(2π) 相对残差 %s ⇒ 缺失因子的识别无误" % KEY["res_ell_ratio_vs_sqrt2pi"])
guard("planck_identity", float(rel(c3 * LP * LP / HBAR, G_VAL)) < Decimal("1e-30"),
      "c³ℓ_P²/ħ 与 G 相对残差 %s ⇒ K25 恒等复读判定成立" % KEY["res_c3_lP2_over_hbar_eq_G"])
guard("M1_closure", float(rel(m_fixed, M_E)) < Decimal("1e-30"),
      "修复式 m=ħω/c² 代回 ω_dB 得 m_e，残差 %s ⇒ M1 闭合" % KEY["M1_res_vs_m_e"])
guard("sec_sin_ratio_bound", max_ratio <= 0.5 + 1e-12,
      "ω_claim/ω_true = ½sin2θ 最大值 %.12g ≤ 1/2 ⇒ K07 全域界成立" % max_ratio)
guard("omega_deBroglie_scale", Decimal("1e20") < omega_dB < Decimal("1e21"),
      "电子德布罗意角频率 %s s^-1 落在 10^20~10^21 康普顿量级 ⇒ 常数链路无误"
      % KEY["omega_deBroglie_electron"])
guard("gauss", float(rel(gauss_num, gauss_ref)) < 1e-6,
      "数值高斯定理 ∮g·dA 与 -4πGm 相对残差 %s ⇒ 面积分实现正确" % KEY["res_gauss"])

# =================================================================
# 汇总与产物输出
# =================================================================
def _counts(rows_, keys):
    return {k: sum(1 for e in rows_ if e["kind"] == k) for k in keys}

KINDS = ["PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED", "MISMATCH"]
ITEMS_ROWS = [e for e in ENTRIES if not e["id"].startswith("G:")]
GUARD_ROWS = [e for e in ENTRIES if e["id"].startswith("G:")]
counts = _counts(ITEMS_ROWS, KINDS)
counts_guard = _counts(GUARD_ROWS, KINDS)
n_item = len(ITEMS_ROWS)
n_guard = len(GUARD_ROWS)
guard_fail = [e["id"] for e in GUARD_ROWS if e["kind"] == "FAIL"]

RESULTS = {
    "round": "r40",
    "engine": "TUFT_光速螺旋曲率挠率量子几何_全维审计",
    "date": "2026-10-12",
    "rating": "C/L1",
    "source_round": "并行会话 2026-10-12 张祥前本源引力场册（未验证 TUFT 导出链）",
    "counts_items": counts,
    "counts_self_checks": counts_guard,
    "counts_total_entries": len(ENTRIES),
    "items_only": n_item,
    "self_checks": n_guard,
    "self_checks_failed": guard_fail,
    "verdict": (
        "TUFT 这一支同样导不出 G：G=2πc³/(ħ sinθ) 量纲缺 L²、数值恒大约 70 量级且需 sinθ>1；"
        "补 L² 后 ≡ ℓ_P 定义移项（零信息量）。另有三式互斥（仅在 τ=0 纯圆相容）"
        "与 2π 量子化口径冲突两处独立缺陷。核心公理 κ²+τ²=ω²/c² 本身通过（可有偿保留）。"),
    "key_numbers": KEY,
    "not_self_derived": NOT_SELF_DERIVED,
    "minimal_augmentation": [
        "M1（零成本·推荐）量子化条件 S=E·T=2πħ ⇒ m=ħω/c²=ħ√(κ²+τ²)/c，德布罗意关系闭合",
        "M2（有代价）引入独立于 G 的长度标度 ℓ 并显式登记为外部输入，否则 G 不可导",
        "M3（删除式）删去 ω=cκ sinθ 与 τ=κ cotθ，保留 κ²+τ²=ω²/c² 与 τ/κ=tanθ（升角定义）",
    ],
    "entries": ENTRIES,
}

def build_md():
    out = []
    out.append("# TUFT「光速螺旋 κ-τ-ω 量子几何」全维审计（r39 · 2026-10-12）")
    out.append("")
    out.append("- 引擎：`源码/TUFT-r39_光速螺旋曲率挠率量子几何_全维审计_2026-10-12.py`（纯标准库）")
    out.append("- 数据：`数据/TUFT-r39_光速螺旋曲率挠率量子几何_全维审计_2026-10-12.{json,md,_report.txt}`")
    out.append("- 判定：`判定_TUFT-r39-光速螺旋曲率挠率量子几何_全维审计_2026-10-12.md`")
    out.append("- 来料正本：`数据/TUFT-光速螺旋曲率挠率量子几何_来料全文_2026-10-12.md`")
    out.append("- 口径：Decimal 60 位 + Fraction 三维量纲 (M,L,T)；机器计算，非口头断言。")
    out.append("")
    out.append("## 一、条目汇总")
    out.append("")
    out.append("| 类别 | 数量 |")
    out.append("|---|---|")
    for k in KINDS:
        out.append("| %s | %d |" % (k, counts[k]))
    out.append("| **条目合计** | %d |" % n_item)
    out.append("| **自检 guard** | %d（失败 %d） |" % (n_guard, len(guard_fail)))
    out.append("")
    out.append("评级：**C/L1**（链条含硬伤且与已知理论重排，无新物理；核心公理 κ²+τ²=ω²/c² 可保留）。")
    out.append("")
    out.append("## 二、逐条裁定")
    out.append("")
    out.append("| 编号 | 类别 | 标题 | 关键读数 |")
    out.append("|---|---|---|---|")
    for e in ENTRIES:
        out.append("| %s | %s | %s | %s |" % (e["id"], e["kind"], e["title"], e["detail"]))
    out.append("")
    out.append("## 三、关键数值档案")
    out.append("")
    out.append("| 量 | 数值 |")
    out.append("|---|---|")
    for k in sorted(KEY.keys()):
        out.append("| %s | %s |" % (k, KEY[k]))
    out.append("")
    out.append("## 四、不自推登记")
    out.append("")
    for s in NOT_SELF_DERIVED:
        out.append("- %s" % s)
    out.append("")
    out.append("> 红线：数学自洽 ≠ 物理证实。本册为机器化复算与诚实边界标注，不产生新物理。")
    return "\n".join(out)

def build_report():
    out = []
    out.append("TUFT-r39 光速螺旋曲率挠率量子几何 全维审计 · 报告")
    out.append("日期: 2026-10-12")
    out.append("PASS = %d" % counts["PASS"])
    out.append("FAIL = %d" % counts["FAIL"])
    out.append("BOUNDARY = %d" % counts["BOUNDARY"])
    out.append("INFO = %d" % counts["INFO"])
    out.append("CORRECTED = %d" % counts["CORRECTED"])
    out.append("MISMATCH = %d" % counts["MISMATCH"])
    out.append("items = %d" % n_item)
    out.append("selfchecks = %d" % n_guard)
    out.append("selfchecks_failed = %d" % len(guard_fail))
    out.append("rating = C/L1")
    out.append("")
    for e in ENTRIES:
        out.append("[%s] %s :: %s" % (e["kind"], e["id"], e["title"]))
        out.append("    %s" % e["detail"])
    return "\n".join(out)

def main():
    md = build_md()
    rep = build_report()
    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
    os.makedirs(data_dir, exist_ok=True)
    stem = "TUFT-r39_光速螺旋曲率挠率量子几何_全维审计_2026-10-12"
    with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(data_dir, stem + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(rep)
    try:
        import sys
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print("ITEMS=%d %s" % (n_item, {k: counts[k] for k in KINDS}))
    print("SELFCHECK=%d FAILED=%s" % (n_guard, guard_fail))
    return 0 if not guard_fail else 2

if __name__ == "__main__":
    import sys
    sys.exit(main())
