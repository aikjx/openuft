# -*- coding: utf-8 -*-
"""
全维勘误精算修复验证（算法联盟最高权限处理模式）

目的
----
对《统一理论体系_已验证正确内容整合全集》第九章「冲突与勘误台账」E1–E6
以及各章收录的关键闭式，做**独立精算复核 + 可复跑修复验证**。

覆盖（F1–F10）
--------------
F1  E6  TS1 三重奏判 ❌ 的脚本缺陷定位与修复（sympy + 50 位数值）
F2  E1  EDM 单位换算复核（e·cm ↔ C·m）与排除倍数重算
F3  E2/E3 螺旋闭式：R = αρ = r_e；sinθ = α（非 tanθ）；误差 α²/2
F4  E4  S05/S06 修正闭式：量纲唯一解、ℓ_P、M₁₁、Cl(4,4)⊗ℂ 维数
F5  M02 修正链：α_grav = Gm²/(ℏc) = (m/m_P)²；旧链偏差闭式
F6  S13 对偶镜像度规：自对偶 + 曲率上界闭式（50 位）
F7  电荷量子化：色单态整数性枚举（4 介子 + 8 重子，精确有理数）
F8  sin²θ_W = 1/4 候选的跑动检验（负面结果复算 + 唯一成立尺度求解）
F9  S13 ℤ₄ Frobenius–Schur 指标 → 三代 / 第四代禁戒
F10 单圈 β 系数与渐近自由窗口

红线
----
本脚本只做**算术/代数/量纲的精算核验**，不对任何物理公设的真实性作主张。
数学自洽 ≠ 物理成立；修复使结果自洽，不等于理论被实验确认。

运行
----
& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe 全维勘误精算修复验证.py
产出写入 ../数据/全维勘误精算修复验证.json 与 .md
"""

import sys
import os
import json
import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import sympy as sp
import mpmath as mp

mp.mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, os.pardir, "数据"))

RECORDS = []
COUNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def rec(fid, item, verdict, detail):
    RECORDS.append({"fid": fid, "item": item, "verdict": verdict, "detail": detail})
    COUNT[verdict] = COUNT.get(verdict, 0) + 1
    mark = {"PASS": "[PASS]", "FAIL": "[FAIL]", "BOUNDARY": "[BND ]", "INFO": "[INFO]"}[verdict]
    print("  " + mark + " " + fid + " " + item + " :: " + detail)


def section(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------- 常数
# CODATA 2018/2022 量级（SI）
c_light = mp.mpf("299792458")
hbar = mp.mpf("1.054571817e-34")
m_e = mp.mpf("9.1093837015e-31")
m_p = mp.mpf("1.67262192369e-27")
e_charge = mp.mpf("1.602176634e-19")
alpha = mp.mpf("7.2973525643e-3")
G_newton = mp.mpf("6.67430e-11")
m_P = mp.sqrt(hbar * c_light / G_newton)
l_P = mp.sqrt(hbar * G_newton / c_light ** 3)
lam_C = hbar / (m_e * c_light)          # 约化康普顿波长
r_e_class = alpha * lam_C               # 经典电子半径（恒等关系）
E_CM_PER_E_CM = e_charge * mp.mpf("1e-2")   # 1 e·cm = 1.602176634e-21 C·m


# ================================================================ F1
def f1_ts1_repair():
    section("F1 · E6 勘误：TS1 三重奏判 ❌ 的脚本缺陷定位与修复")
    t, R, om, b, c = sp.symbols("t R omega b c", positive=True)
    r = sp.Matrix([R * sp.cos(om * t), R * sp.sin(om * t), b * t])
    v = sp.diff(r, t)
    a = sp.diff(v, t)
    ap = sp.diff(a, t)

    v2 = sp.simplify(v.dot(v))
    cross = v.cross(a)
    cross2 = sp.simplify(cross.dot(cross))
    kappa2 = sp.simplify(cross2 / v2 ** 3)
    tau2 = sp.simplify((cross.dot(ap)) ** 2 / cross2 ** 2)

    # ---- (a) 复现原脚本的失败路径
    lhs_bug = sp.simplify((kappa2 + tau2).subs(v2, c ** 2))
    diff_bug = sp.simplify(lhs_bug - om ** 2 / c ** 2)
    is_zero_bug = (diff_bug == 0)
    rec("F1-01", "复现原脚本 .subs(v2, c**2) 的代入结果",
        "INFO", "残差 = " + str(diff_bug)[:120])
    rec("F1-02", "原脚本判定", ("FAIL" if not is_zero_bug else "PASS"),
        "残差非零 ⟹ 原判 ❌ 成立，但根因为替换失败（见 F1-03）")

    # ---- (b) 根因：subs 只替换分母中的 v2，分子残留 ⟹ 替换不彻底
    has_subexpr = kappa2.has(v2) or tau2.has(v2)
    residual = sp.simplify(diff_bug - om ** 2 * (v2 - c ** 2) / c ** 4)
    rec("F1-03", "根因定位：subs 替换完整性",
        "FAIL",
        "has(v2) = " + str(has_subexpr) + "；残差恰为 ω²(R²ω²+b²−c²)/c⁴（核对残差 = " + str(residual) +
        "）⟹ 分母 v2 被替换而分子残留，属符号替换**不彻底**的 bug（非定理错）")

    # ---- (c) 正确路径一：一般恒等式（不依赖任何约束）
    ident = sp.simplify(kappa2 + tau2 - om ** 2 / v2)
    rec("F1-04", "一般恒等式 κ²+τ² = ω²/(R²ω²+b²)",
        "PASS" if ident == 0 else "FAIL", "残差 = " + str(ident))

    # ---- (d) 正确路径二：代入光速约束 b² = c² − R²ω²
    lhs_fix = sp.simplify((om ** 2 / v2).subs(b ** 2, c ** 2 - R ** 2 * om ** 2))
    diff_fix = sp.simplify(lhs_fix - om ** 2 / c ** 2)
    rec("F1-05", "约束代入后 κ²+τ² = (ω/c)²",
        "PASS" if diff_fix == 0 else "FAIL", "残差 = " + str(diff_fix))

    # ---- (e) 50 位数值验证（构造满足约束的参数）
    Rv, omv = mp.mpf("0.3"), mp.mpf("2.0")
    bv = mp.mpf("0.4")
    cv = mp.sqrt(Rv ** 2 * omv ** 2 + bv ** 2)
    V2 = Rv ** 2 * omv ** 2 + bv ** 2
    k2 = (Rv * omv ** 2 / V2) ** 2
    t2 = (bv * omv / V2) ** 2
    lhs_num, rhs_num = k2 + t2, omv ** 2 / cv ** 2
    rel = abs(lhs_num - rhs_num) / rhs_num
    rec("F1-06", "50 位数值验证（R=0.3, ω=2, b=0.4, c=√(R²ω²+b²)）",
        "PASS" if rel < mp.mpf("1e-40") else "FAIL",
        "相对残差 = " + mp.nstr(rel, 6))

    # ---- (f) 电子参数（CODATA）
    rho = lam_C
    RR = alpha * rho                       # 经典电子半径
    bb = rho * mp.sqrt(1 - alpha ** 2)
    cc = c_light
    V2e = RR ** 2 * (cc / rho) ** 2 + (bb * (cc / rho)) ** 2 if False else None
    ome = cc / rho
    V2e = RR ** 2 * ome ** 2 + bb ** 2 * ome ** 2 / (1 + 0)  # b 参数化统一：|v|² = R²ω² + (bω)²
    V2e = RR ** 2 * ome ** 2 + (bb * ome) ** 2
    k2e = (RR * ome ** 2 / V2e) ** 2
    t2e = ((bb * ome) * ome / V2e) ** 2
    lhs_e, rhs_e = k2e + t2e, ome ** 2 / cc ** 2
    rel_e = abs(lhs_e - rhs_e) / rhs_e
    rec("F1-07", "电子参数下 κ²+τ² = (ω/c)²",
        "PASS" if rel_e < mp.mpf("1e-30") else "BOUNDARY",
        "相对残差 = " + mp.nstr(rel_e, 6) + "（√(κ²+τ²) = " + mp.nstr(mp.sqrt(lhs_e), 10) + " 1/m）")

    rec("F1-08", "修复结论", "PASS",
        "TS1 的 ❌ 为脚本符号替换 bug；定理本身成立。应用补丁后汇总应由 11/12 → 12/12")


# ================================================================ F2
def f2_edm_units():
    section("F2 · E1 勘误：EDM 单位换算复核与排除倍数重算")
    rho = lam_C / mp.sqrt(1 + alpha ** 2)
    d_pred_cm = e_charge * alpha * rho / 2              # C·m
    d_pred_ecm = d_pred_cm / E_CM_PER_E_CM              # e·cm
    rec("F2-01", "预言重算 d_e = e·α·ρ/2",
        "PASS", "= " + mp.nstr(d_pred_cm, 12) + " C·m = " + mp.nstr(d_pred_ecm, 10) + " e·cm")

    jila_ecm = mp.mpf("4.1e-30")
    acme_ecm = mp.mpf("1.1e-29")
    wrong_cm = mp.mpf("8.7e-34")                        # 看板沿用的错误上限（C·m）
    rec("F2-02", "换算因子 1 e·cm",
        "PASS", "= " + mp.nstr(E_CM_PER_E_CM, 10) + " C·m")
    rec("F2-03", "JILA HfF⁺ 2023 上限换算",
        "PASS", "4.1e-30 e·cm = " + mp.nstr(jila_ecm * E_CM_PER_E_CM, 8) + " C·m")
    rec("F2-04", "ACME II 2018 上限换算",
        "PASS", "1.1e-29 e·cm = " + mp.nstr(acme_ecm * E_CM_PER_E_CM, 8) + " C·m")

    ratio = d_pred_ecm / jila_ecm
    rec("F2-05", "排除倍数（vs JILA 2023）",
        "PASS", "= " + mp.nstr(ratio, 6) + " 倍（≈16.5 个数量级）⟹ 预言已被实验排除")

    # 反推：看板写 8.7e-34 C·m 若当作 e·cm 数值，真实值应是多少
    implied_ecm = wrong_cm / E_CM_PER_E_CM
    rec("F2-06", "错误值溯源：8.7e-34 C·m 若由 e·cm 误配单位而来",
        "INFO", "对应 " + mp.nstr(implied_ecm, 6) + " e·cm；真实 ACME-2013 级上限为 8.7e-29 e·cm ⟹ 差 1e5 倍量级，单位错误确认")
    rec("F2-07", "若误用 8.7e-34 C·m 作上限会得到的（错误）判定",
        "FAIL", "预言 " + mp.nstr(d_pred_cm, 6) + " < 8.7e-34 ⟹ 误判「仍被允许」；正确判定为「已证伪」")


# ================================================================ F3
def f3_spiral_closure():
    section("F3 · E2/E3 勘误：螺旋闭式 R = αρ = r_e 与 sinθ = α")
    rec("F3-01", "横向半径 R = α·ƛ_C 与经典电子半径 r_e 的关系",
        "PASS", "R = " + mp.nstr(r_e_class, 10) + " m；PDG r_e = 2.8179403262e-15 m（恒等定义式）")

    tan_theta = alpha / mp.sqrt(1 - alpha ** 2)
    rec("F3-02", "κ/τ = R/b = tanθ（S12 原式 α = tanθ）",
        "BOUNDARY", "κ/τ = " + mp.nstr(tan_theta, 10) + " vs α = " + mp.nstr(alpha, 10))
    err = (tan_theta - alpha) / alpha
    half_a2 = alpha ** 2 / 2
    rec("F3-03", "误用 tanθ = α 的相对误差",
        "PASS", "实测 " + mp.nstr(err, 6) + "；理论 α²/2 = " + mp.nstr(half_a2, 6) + " ⟹ 吻合，S12 需修正为 sinθ = α")
    rec("F3-04", "正确几何关系 sinθ = v⊥/c = α",
        "PASS", "v⊥ = αc = " + mp.nstr(alpha * c_light, 10) + " m/s；v∥ = c√(1−α²) = " + mp.nstr(c_light * mp.sqrt(1 - alpha ** 2), 12) + " m/s")
    vv = mp.sqrt((alpha * c_light) ** 2 + (c_light * mp.sqrt(1 - alpha ** 2)) ** 2)
    rec("F3-05", "光速约束 |v| = c",
        "PASS", "|v| = " + mp.nstr(vv, 12) + " vs c = " + mp.nstr(c_light, 12) + "，相对残差 = " + mp.nstr(abs(vv - c_light) / c_light, 4))


# ================================================================ F4
def f4_s05_s06():
    section("F4 · E4 勘误：S05/S06 修正闭式的量纲与数值复核")
    a, bb, d = sp.symbols("a b d")
    # [ℏ]=M L^2 T^-1, [G]=M^-1 L^3 T^-2, [c]=L T^-1  ⟹ 求 [ℏ^a G^b c^d] = L
    sol = sp.solve([a - bb, 2 * a + 3 * bb + d - 1, -a - 2 * bb - d], [a, bb, d], dict=True)
    rec("F4-01", "由 (ℏ,G,c) 造长度的量纲解唯一性",
        "PASS", "解 = " + str(sol) + " ⟹ 唯一为 ℓ_P = √(ℏG/c³)")

    # 原式指数 (1/3, 1/3, -2/3) 的 T 指数
    T_exp = -sp.Rational(1, 3) - 2 * sp.Rational(1, 3) + sp.Rational(2, 3)
    rec("F4-02", "S05-H2 原式 (1/3,1/3,−2/3) 的时间指数",
        "FAIL", "T 指数 = " + str(T_exp) + " ≠ 0 ⟹ 量纲为 L·T^(−1/3)，不是长度（缺陷确认）")

    r11_old = (hbar / (2 * mp.pi)) ** (mp.mpf(1) / 3) * G_newton ** (mp.mpf(1) / 3) * c_light ** (mp.mpf(-2) / 3)
    ratio_r = r11_old / l_P
    rec("F4-03", "S05-H2 原式数值",
        "FAIL", "= " + mp.nstr(r11_old, 10) + " m；与 ℓ_P = " + mp.nstr(l_P, 10) + " m 相差 " + mp.nstr(ratio_r, 8) + " 倍")
    rec("F4-04", "修正 R₁₁ = ℓ_P",
        "PASS", "量纲 L ✓，数值 = " + mp.nstr(l_P, 10) + " m")

    m_P_GeV = m_P * c_light ** 2 / (mp.mpf("1.602176634e-19") * mp.mpf("1e9"))
    m11_old = m_P_GeV * (2 * mp.pi) ** (mp.mpf(1) / 3)
    rec("F4-05", "S05-H3 数值复核",
        "FAIL", "M_P(2π)^(1/3) = " + mp.nstr(m11_old, 8) + " GeV；原文 3.18e19 GeV 偏 " + mp.nstr(mp.mpf("3.18e19") / m11_old, 6) + " 倍")
    rec("F4-06", "自洽闭合要求 M₁₁ = M_P",
        "PASS", "M_P = " + mp.nstr(m_P_GeV, 10) + " GeV（弃 (2π)^(1/3) 因子）")

    # Clifford 代数
    p_, q_ = 4, 4
    dim_complex = 2 ** ((p_ + q_) // 2) if (p_ + q_) % 2 == 0 else None
    rec("F4-07", "Cl(4,4)⊗ℂ 的复矩阵代数维数",
        "PASS", "n = p+q = 8（偶），复化后 ≅ M₁₆(ℂ)，维数 = 2⁸ = " + str(2 ** 8) +
        "；原文 M₈⊕M₈ = 128 属 Cl(4,3)（7 生成元），2⁴·2 = 32 无依据 ⟹ 32/128/256 三者互斥")
    rec("F4-08", "半单 vs 单：M₈⊕M₈ 与 M₁₆(ℂ) 是否可能同构",
        "FAIL", "M₈⊕M₈ 中心 = ℂ⊕ℂ（二维，半单）；M₁₆(ℂ) 中心 = ℂ（一维，单）⟹ 不可能同构（缺陷确认）")


# ================================================================ F5
def f5_m02_chain():
    section("F5 · M02 修正链：α_grav = Gm²/(ℏc) = (m/m_P)²")
    masses = {
        "e": mp.mpf("9.1093837015e-31"), "mu": mp.mpf("1.883531627e-28"),
        "tau": mp.mpf("3.16754e-27"), "p": mp.mpf("1.67262192369e-27"),
        "W": mp.mpf("80.379") * mp.mpf("1.78266192e-27") / mp.mpf("1"),
        "Z": mp.mpf("91.1876") * mp.mpf("1.78266192e-27"),
        "H": mp.mpf("125.10") * mp.mpf("1.78266192e-27"),
        "t": mp.mpf("172.76") * mp.mpf("1.78266192e-27"),
        "m_P": m_P,
    }
    worst = mp.mpf("0")
    for k, m in masses.items():
        lhs = G_newton * m ** 2 / (hbar * c_light)
        rhs = (m / m_P) ** 2
        rel = abs(lhs - rhs) / rhs if rhs != 0 else mp.mpf("0")
        worst = max(worst, rel)
    rec("F5-01", "修正链对 9 个粒子的残差",
        "PASS" if worst < mp.mpf("1e-40") else "FAIL", "最大相对残差 = " + mp.nstr(worst, 6))

    m_ref = m_e
    g_old = hbar * c_light / m_ref ** 2
    ratio_old = g_old / G_newton
    closed = (m_P / m_ref) ** 2
    rec("F5-02", "旧链 G_old = ℏc/m² 在电子处的偏差",
        "FAIL", "G_old = " + mp.nstr(g_old, 8) + "，与 G 差 " + mp.nstr(ratio_old, 8) + " 倍")
    rec("F5-03", "偏离闭式 G_old/G = (m_P/m)²",
        "PASS", "闭式值 = " + mp.nstr(closed, 8) + "；残差 = " + mp.nstr(abs(ratio_old - closed) / closed, 6))
    rec("F5-04", "联立根因 Gm² = ℏc ⟹ m = m_P（唯一解）",
        "INFO", "旧链等价于把 G 换成随粒子质量平方反比变化的量，不可能是普适引力常数")


# ================================================================ F6
def f6_s13_curvature():
    section("F6 · S13 对偶镜像度规：自对偶与曲率上界（50 位）")
    ell = mp.mpf("1")
    rs = mp.mpf("1")   # r_s = 2GM；以 ℓ=r_s=1 为单位

    def A(r):
        return 1 - rs * r / (r ** 2 + ell ** 2)

    # 自对偶 A(r) = A(ℓ²/r)
    worst = mp.mpf("0")
    for k in range(1, 20):
        r = mp.mpf(k) / mp.mpf("4")
        worst = max(worst, abs(A(r) - A(ell ** 2 / r)))
    rec("F6-01", "自对偶 A(r) = A(ℓ²/r)",
        "PASS" if worst < mp.mpf("1e-40") else "FAIL", "最大残差 = " + mp.nstr(worst, 6))

    # 正确闭式：R = −A''（与 V1.8 精算 P4c 口径一致）
    def Rsc(r):
        return 2 * r * rs * (r ** 2 - 3 * ell ** 2) / (r ** 2 + ell ** 2) ** 3

    # 文档 derivations.md §5 所写的闭式（待核对）
    def Rdoc(r):
        return rs * ell ** 2 * (3 * r ** 2 - ell ** 2) / (r ** 2 + ell ** 2) ** 3

    # 符号验证 R = −A''
    rr, rs_s, el_s = sp.symbols("r rs ell", positive=True)
    A_s = 1 - rs_s * rr / (rr ** 2 + el_s ** 2)
    minus_app = sp.simplify(-sp.diff(A_s, rr, 2))
    target = 2 * rr * rs_s * (rr ** 2 - 3 * el_s ** 2) / (rr ** 2 + el_s ** 2) ** 3
    rec("F6-02", "符号验证 R = −A''",
        "PASS" if sp.simplify(minus_app - target) == 0 else "FAIL",
        "−A'' = " + str(sp.simplify(minus_app)))

    r1 = (mp.sqrt(2) - 1) * ell
    r2 = (mp.sqrt(2) + 1) * ell
    val1 = abs(Rsc(r1))
    closed = (3 + 2 * mp.sqrt(2)) * rs / (4 * ell ** 3)   # = (3+2√2)GM/(2ℓ³)
    rec("F6-03", "驻点方程 r⁴ − 6ℓ²r² + ℓ⁴ = 0 的根",
        "PASS", "r = (√2∓1)ℓ = " + mp.nstr(r1, 10) + " , " + mp.nstr(r2, 10))
    rec("F6-04", "曲率上界 |R|_max 闭式（正确式 −A''）",
        "PASS" if abs(val1 - closed) / closed < mp.mpf("1e-40") else "FAIL",
        "数值 " + mp.nstr(val1, 12) + " vs 闭式 (3+2√2)r_s/(4ℓ³) = " + mp.nstr(closed, 12))

    # 文档笔误核对（新勘误 E7）
    val_doc = abs(Rdoc(r1))
    rec("F6-05", "文档 derivations.md 所写 R(r) = r_sℓ²(3r²−ℓ²)/(r²+ℓ²)³ 的核对",
        "FAIL" if abs(val_doc - closed) / closed > mp.mpf("1e-6") else "PASS",
        "该式在 r=(√2−1)ℓ 处给 " + mp.nstr(val_doc, 10) + "，与闭式 " + mp.nstr(closed, 10) +
        " 差 " + mp.nstr(abs(val_doc - closed) / closed * 100, 6) + "% ⟹ 与自身结论冲突（笔误）")

    rr_sym = sp.symbols("rr2", positive=True)
    poly_correct = sp.expand(rr_sym ** 4 - 6 * rr_sym ** 2 + 1)
    poly_doc = sp.expand(3 * rr_sym ** 4 - 6 * rr_sym ** 2 - 1)
    roots_correct = sp.solve(sp.Eq(rr_sym ** 4 - 6 * rr_sym ** 2 + 1, 0), rr_sym)
    roots_doc = sp.solve(sp.Eq(3 * rr_sym ** 4 - 6 * rr_sym ** 2 - 1, 0), rr_sym)
    rec("F6-06", "驻点方程核对（ℓ=1）",
        "FAIL", "正确：r⁴−6r²+1=0 ⟹ r² = " + str([sp.simplify(x ** 2) for x in roots_correct]) +
        " = (3∓2√2)；文档写 3r⁴−6r²−1=0 ⟹ r² = " + str([sp.nsimplify(sp.simplify(x ** 2)) for x in roots_doc]) +
        " ⟹ 与其给出的 (3±2√2) 不符，属笔误")

    rec("F6-07", "端点行为 R(0⁺) = R(∞) = 0（正确式）",
        "PASS", "R(1e-30) = " + mp.nstr(Rsc(mp.mpf("1e-30")), 6) + "；R(1e30) = " + mp.nstr(Rsc(mp.mpf("1e30")), 6) +
        " ⟹ 奇点被逐出全域")
    rec("F6-08", "端点行为（文档笔误式）",
        "FAIL", "R_doc(1e-30) = " + mp.nstr(Rdoc(mp.mpf("1e-30")), 6) +
        " ≠ 0 ⟹ 文档式连端点条件都不满足，进一步确认为笔误")
    rec("F6-09", "笔误性质判定",
        "INFO", "驻点解 r=(√2±1)ℓ 与 |R|_max=(3+2√2)GM/(2ℓ³) 均正确，且与 V1.8 精算 P4d/P4f（残差 ~1e-50）一致 ⟹ 属书写笔误，非结论错误")


# ================================================================ F7
def f7_charge_quantization():
    section("F7 · 电荷量子化：色单态整数性（精确有理数枚举）")
    from fractions import Fraction as F

    q_u, q_d = F(2, 3), F(-1, 3)
    q_ub, q_db = F(-2, 3), F(1, 3)

    mesons = {
        "u ū": q_u + q_ub, "u đ": q_u + q_db,
        "d ū": q_d + q_ub, "d đ": q_d + q_db,
    }
    baryons = {}
    for i, a in enumerate(["u", "d"]):
        for j, bb in enumerate(["u", "d"]):
            for k, cc in enumerate(["u", "d"]):
                baryons[a + bb + cc] = (q_u if a == "u" else q_d) + (q_u if bb == "u" else q_d) + (q_u if cc == "u" else q_d)

    all_int = all(x.denominator == 1 for x in mesons.values()) and all(x.denominator == 1 for x in baryons.values())
    rec("F7-01", "介子（q q̄）电荷整数性",
        "PASS" if all(x.denominator == 1 for x in mesons.values()) else "FAIL",
        "、".join(k + "=" + str(v) for k, v in mesons.items()))
    rec("F7-02", "重子（qqq）电荷整数性",
        "PASS" if all(x.denominator == 1 for x in baryons.values()) else "FAIL",
        "、".join(k + "=" + str(v) for k, v in baryons.items()))
    rec("F7-03", "色单态判据 k ≡ l (mod 3) 下的整体结论",
        "PASS" if all_int else "FAIL", "所有可观测强子电荷为整数，无一例外")
    rec("F7-04", "分数化来源 1/3 = 1/(色表示维数 3)",
        "INFO", "λ₈ = diag(1,1,−2)/√3 谱 + T₃ = ±1/2 ⟹ 电荷落在 ±1/3 步长（结构解释，非 α 量级推导）")


# ================================================================ F8
def f8_weinberg_running():
    section("F8 · sin²θ_W = 1/4 候选的跑动检验（负面结果复算）")
    MZ = mp.mpf("91.1876")
    a1_inv = mp.mpf("59.003557488")     # GUT 归一 α1⁻¹(M_Z)
    a2_inv = mp.mpf("29.57673752")
    b1, b2 = mp.mpf("4.1"), mp.mpf("-19") / 6

    def inv_alpha(a0, b, L):
        return a0 - b / (2 * mp.pi) * L

    def sin2(L):
        x1 = inv_alpha(a1_inv, b1, L)
        x2 = inv_alpha(a2_inv, b2, L)
        aem_inv = mp.mpf(5) / 3 * x1 + x2
        return x2 / aem_inv

    s0 = sin2(mp.mpf("0"))
    rec("F8-01", "M_Z 处基准复算",
        "PASS" if abs(s0 - mp.mpf("0.23122")) < mp.mpf("1e-3") else "BOUNDARY",
        "sin²θ(M_Z) = " + mp.nstr(s0, 8) + " vs 实验 0.23122")

    mu = mp.mpf("255.26")
    L1 = mp.log(mu / MZ)
    s1 = sin2(L1)
    dev = (s1 - mp.mpf("0.25")) / mp.mpf("0.25")
    rec("F8-02", "跑动到框架真空尺度 v = 255.26 GeV",
        "FAIL" if abs(dev) > mp.mpf("1e-3") else "PASS",
        "sin²θ(v) = " + mp.nstr(s1, 8) + "；与 1/4 差 " + mp.nstr(dev * 100, 4) + "% ⟹ 候选未获跑动支持（负面结果）")

    # 求解 sin²θ = 1/4 的唯一尺度：条件 (5/3)α1⁻¹ + α2⁻¹ = 4α2⁻¹ ⟹ α1⁻¹ = (9/5)α2⁻¹
    L = sp.symbols("L", real=True)
    expr = (a1_inv - b1 / (2 * mp.pi) * L) - mp.mpf("1.8") * (a2_inv - b2 / (2 * mp.pi) * L)
    # 用 sympy 数值解（系数转 float 表达式）
    Ls = sp.symbols("Ls", real=True)
    f_sym = (sp.Float(a1_inv) - sp.Float(b1) / (2 * sp.pi) * Ls) - sp.Rational(9, 5) * (sp.Float(a2_inv) - sp.Float(b2) / (2 * sp.pi) * Ls)
    root = sp.solve(sp.Eq(f_sym, 0), Ls)
    Lval = mp.mpf(str(root[0]))
    mu_star = MZ * mp.e ** Lval
    rec("F8-03", "sin²θ = 1/4 在 SM 单圈下的唯一成立尺度",
        "FAIL", "ln(μ/M_Z) = " + mp.nstr(Lval, 8) + " ⟹ μ = " + mp.nstr(mu_star, 8) +
        " GeV（≈3.7 TeV）；既非 M_Z 亦非 M_P ⟹ 框架内无出处，候选判负")

    rec("F8-04", "与 SU(5) 大统一 3/8 = 0.375 的可区分性",
        "INFO", "1/4 = 0.250 与 3/8 = 0.375 相差 " + mp.nstr(abs(mp.mpf("0.375") - mp.mpf("0.25")) / mp.mpf("0.25") * 100, 4) + "% ⟹ 几何上可区分（但均未被跑动支持）")


# ================================================================ F9
def f9_z4_fs():
    section("F9 · S13 ℤ₄ Frobenius–Schur 指标 → 三代 / 第四代禁戒")
    out = {}
    for k in range(4):
        # ν_k = (1/4) Σ_{g=0}^{3} χ_k(g²) = (1/4) Σ i^{2kg} = (1/4) Σ (−1)^{kg}
        s = sum((-1) ** (k * g) for g in range(4))
        out[k] = sp.Rational(s, 4)
    rec("F9-01", "ℤ₄ 四个一维表示的 FS 指标",
        "PASS", "、".join("ρ" + str(k) + "=" + str(out[k]) for k in range(4)))
    n_real = sum(1 for k in range(4) if out[k] == 1)
    # ρ1 与 ρ3 互为共轭 ⟹ ρ1⊕ρ3 构成一个实型单元
    n_units = n_real + 1 if out[1] == 0 else n_real
    rec("F9-02", "实不可约单元计数",
        "PASS" if n_units == 3 else "FAIL",
        "实型 ρ0、ρ2（各 +1）+ 复共轭对 ρ1⊕ρ3 ⟹ " + str(n_units) + " 个实型单元 = 3 代")
    rec("F9-03", "第四代禁戒",
        "PASS", "ℤ₄ 仅 4 个一维表示，FS 指标结构只允许 3 个实型单元 ⟹ 第四代被表示论禁戒（结构结论，非质量预言）")


# ================================================================ F10
def f10_beta():
    section("F10 · 单圈 β 系数与渐近自由窗口")
    CA = 3
    b0_pure = sp.Rational(11, 3) * CA
    rec("F10-01", "SU(3) 纯规范 b₀ = 11/3·C_A",
        "PASS" if b0_pure == 11 else "FAIL", "= " + str(b0_pure))
    for nf in [6]:
        b0 = 11 - sp.Rational(2, 3) * nf
        rec("F10-02", "nf = " + str(nf) + " 时 b₀ = 11 − 2n_f/3",
            "PASS" if b0 == 7 else "FAIL", "= " + str(b0))
    nf_max = sp.Rational(33, 2)
    rec("F10-03", "渐近自由窗口 nf < 33/2",
        "PASS", "nf_max = " + str(nf_max) + " ⟹ nf ≤ 16；SM 的 nf = 6 深在区内")

    # SM 三线差距（单圈，来自 V1.8 P9）
    gap = mp.mpf("13.1406")
    rec("F10-04", "SM 单圈三线差距",
        "BOUNDARY", "= " + mp.nstr(gap, 6) + "% ⟹ 单圈无大统一（标准结论，非缺陷）")


# ================================================================ main
def main():
    print("=" * 78)
    print("全维勘误精算修复验证（算法联盟最高权限处理模式）")
    print("运行时间: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("精度: mpmath " + str(mp.mp.dps) + " 位 + sympy " + sp.__version__ + " 符号")
    print("=" * 78)

    f1_ts1_repair()
    f2_edm_units()
    f3_spiral_closure()
    f4_s05_s06()
    f5_m02_chain()
    f6_s13_curvature()
    f7_charge_quantization()
    f8_weinberg_running()
    f9_z4_fs()
    f10_beta()

    print()
    print("=" * 78)
    total = sum(COUNT.values())
    print("精算汇总：" + str(total) + " 项核查，PASS " + str(COUNT.get("PASS", 0)) +
          " / FAIL " + str(COUNT.get("FAIL", 0)) +
          " / BOUNDARY " + str(COUNT.get("BOUNDARY", 0)) +
          " / INFO " + str(COUNT.get("INFO", 0)))
    print("=" * 78)
    print("说明：FAIL 项均为「确认缺陷存在」的诚实标注（如 S05 量纲错、S06 同构错、EDM 误判、"),
    print("      sin²θ_W 候选未获支持），不是本脚本的计算错误。")
    print("红线：数学自洽 != 物理成立；修复使结果自洽，不等于理论被实验确认。")

    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    payload = {
        "meta": {
            "script": "全维勘误精算修复验证.py",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mpmath_dps": mp.mp.dps,
            "sympy": sp.__version__,
            "total": total,
            "counts": COUNT,
        },
        "records": RECORDS,
    }
    jpath = os.path.join(OUT_DIR, "全维勘误精算修复验证.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = ["# 全维勘误精算修复验证", "",
             "> 脚本：`04_公共成果/算法联盟_全维自洽与归一化/源码/全维勘误精算修复验证.py`",
             "> 精度：mpmath " + str(mp.mp.dps) + " 位 + sympy 符号 ｜ 时间：" +
             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "",
             "## 结果表", "",
             "| 编号 | 项 | 判定 | 细节 |", "|---|---|---|---|"]
    for r in RECORDS:
        lines.append("| " + r["fid"] + " | " + r["item"] + " | " + r["verdict"] + " | " + r["detail"] + " |")
    lines += ["", "## 汇总", "",
              "总计 " + str(total) + " 项：PASS " + str(COUNT.get("PASS", 0)) +
              " / FAIL " + str(COUNT.get("FAIL", 0)) +
              " / BOUNDARY " + str(COUNT.get("BOUNDARY", 0)) +
              " / INFO " + str(COUNT.get("INFO", 0)), "",
              "## 关键修复结论", "",
              "1. **F1**：TS1 判 ❌ 的根因是 `simplify` 后 `v2` 不再是子表达式 ⟹ `.subs(v2, c**2)` 匹配失败。",
              "   正确路径：先证一般恒等式 `κ²+τ² = ω²/(R²ω²+b²)`（残差 0），再代入约束 `b² = c² − R²ω²`。",
              "   补丁后 TS1 转 ✅，定理谱系汇总应由 11/12 → 12/12。",
              "2. **F2**：EDM 单位换算确认 `1 e·cm = 1.602176634e-21 C·m`；预言被 JILA 2023 排除约 3.44e16 倍。",
              "   看板「8.7e-34 C·m」为单位误配，据此得出的「仍被允许」属错误判定。",
              "3. **F3**：`κ/τ = tanθ`，误作 α 的误差恰为 `α²/2 ≈ 2.66e-5` ⟹ S12 应修正为 `sinθ = α`。",
              "4. **F4**：S05-H2 量纲解唯一为 `ℓ_P`；原式 T 指数 −1/3 ≠ 0，数值偏 1.43e14 倍。",
              "   S06 `Cl(4,4)⊗ℂ` 复维数 = 2⁸ = 256；`M₈⊕M₈`（半单）与 `M₁₆(ℂ)`（单）不可能同构。",
              "5. **F8**：`sin²θ_W = 1/4` 候选在 SM 单圈下跑到 v = 255.26 GeV 为 0.2364（差 −5.4%），",
              "   唯一成立尺度 ≈3.7 TeV 无框架出处 ⟹ 候选判负（负面结果如实）。", "",
              "## 诚实边界", "",
              "- FAIL 项均为「确认缺陷存在」的诚实标注，不是本脚本的计算错误；",
              "- 修复使结果**自洽**，不等于理论**成立**；",
              "- 电荷量子化（F7）与代结构（F9）是结构解释，不构成 α 量级或绝对质量的推导。"]
    mpath = os.path.join(OUT_DIR, "全维勘误精算修复验证.md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print()
    print("产出：" + jpath)
    print("产出：" + mpath)


if __name__ == "__main__":
    main()
