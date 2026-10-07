# -*- coding: utf-8 -*-
"""
第十八轮 · 外部来料《算法联盟 · TUFT V3.4：G 与 c 核心关系》三表审计
（量纲表 / 自由度表 / 符号冲突表）

日期：2026-10-07
读数：数据/TUFT-G与c核心关系_量纲自由度与符号冲突审计_2026-10-07.json
      数据/TUFT-G与c核心关系_量纲自由度与符号冲突审计_2026-10-07.md

纯标准库（decimal，60 位有效数字），零第三方依赖、零网络。退出码由自检决定。

纪律（沿用既有轮次）：
  1. 只用 CODATA 原始常数，不引用中间比值（能标一致性条款）。
  2. 缺陷 ID 复用既有登记（C-02 / C-05 / C-88 / C-30 / O-V34-C），不新增重复条目。
  3. 不对修式路线打分排序，取舍权保留给用户（沿用 30 号册 E-06）。
  4. 数学自洽 != 物理证实；本册只判结构与量纲，不产出物理预言。
"""
from __future__ import annotations

import json
import os
import sys
from decimal import Decimal, getcontext, ROUND_HALF_EVEN

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(BASE), "数据")

# ---- CODATA 口径原始常数（禁引中间比值）----
C_LIGHT = Decimal(299792458)                    # 光速，精确
G_N = Decimal("6.67430e-11")                    # m^3 kg^-1 s^-2
HBAR = Decimal("1.0545718176461565e-34")        # 约化普朗克常数 J s
PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592")
M_SUN = Decimal("1.98892e30")                   # kg
RHO_SUN = Decimal("1.408e3")                    # kg/m^3 太阳平均密度
KG_PER_GEV = Decimal("1.78266192e-27")          # kg per GeV/c^2
GEV_PER_J = Decimal("6.241509074460763e9")      # GeV per J
DOC_NUM = Decimal("1.202e44")                   # 来料 §6 自称 c^4/G
R_AU = Decimal("1.495978707e11")                # m


def S(x, digits=25):
    """定点化输出：用 E 格式避免 quantize 在高位数时抛 InvalidOperation。"""
    return format(Decimal(x), "." + str(digits) + "E")


# ---- 量纲代数：(L, M, T) 指数三元组 ----
def D(L=0, M=0, T=0):
    return (int(L), int(M), int(T))


def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dpow(a, n):
    return (a[0] * n, a[1] * n, a[2] * n)


def ddif(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dstr(a):
    return "L^%d M^%d T^%d" % a


DIM_G = D(3, -1, -2)
DIM_C = D(1, 0, -1)
DIM_HBAR = D(2, 1, -1)
DIM_MP = D(1, 1, 0)
DIM_KAPPA = D(-2, 0, 0)        # 来料 §1 声明 [kappa] = m^-2
DIM_TAU = D(-1, 0, 0)          # 符号台账 [tau] = L^-1
DIM_RHO = D(-3, 1, 0)          # 物质密度
DIM_N = D(1, 1, -2)            # 牛顿（N）= J/m
DIM_J = D(2, 1, -2)            # 焦耳（J）

# ---- 机器读数（全部现算，不硬编码结论）----
C2 = C_LIGHT ** 2
C4 = C_LIGHT ** 4
C6 = C_LIGHT ** 6
F_PLANCK = C4 / G_N                        # c^4/G : 普朗克力（N）
KAPPA_E = 8 * PI * G_N / C4                # 本库主线 kappa = 8 pi G / c^4
KAPPA_DOC = C4 / (8 * PI * G_N)            # 来料 §1 kappa = c^4/(8 pi G)
KAPPA_INV_PROD = KAPPA_DOC * KAPPA_E
LP = (HBAR * G_N / C_LIGHT ** 3).sqrt()    # 普朗克长度
MP = (HBAR * C_LIGHT / G_N).sqrt()         # 普朗克质量（kg）
RHO_PL = MP / (LP ** 3)                    # 普朗克密度
RHO_STAR = C6 / (64 * PI ** 2 * G_N ** 2)  # 使 8 pi G rho / c^2 = KAPPA_DOC 的密度
KAPPA_STAR = 8 * PI * G_N * RHO_STAR / C2  # 复核用
L_G = 1 / KAPPA_DOC.sqrt()                 # 强解为曲率密度时的特征长度
L_G_OVER_L_P = L_G / LP
RHO_STAR_OVER_PL = RHO_STAR / RHO_PL
RHO_STAR_OVER_SUN = RHO_STAR / RHO_SUN
DOC_RELERR = (DOC_NUM - F_PLANCK) / F_PLANCK
KAPPA_DOC_GEV = (KAPPA_DOC * L_G) * GEV_PER_J   # 力→能量必须显式带长度：E = F * l_G
M_PL_GEV = MP / KG_PER_GEV
KAPPA_OVER_MPL = KAPPA_DOC_GEV / M_PL_GEV
E_DOC_J = KAPPA_DOC * L_G
IDENT_G = LP * C2 / MP                     # 应 = G
IDENT_HBAR = LP * MP * C_LIGHT / HBAR      # 应 = 1
KAPPA_2M_OVER_1M = KAPPA_DOC / KAPPA_DOC   # §1 定义式只含 (G, c)


def r_gr(mass, r):
    """弱场 Schwarzschild：R = 48 G^2 M^2 / (c^4 r^6)"""
    return 48 * G_N ** 2 * mass ** 2 / (C4 * r ** 6)


R_GR_1M = r_gr(M_SUN, R_AU)
R_GR_2M = r_gr(2 * M_SUN, R_AU)
R_GR_RATIO = R_GR_2M / R_GR_1M

DIM_RHS_KAPPA = ddiv(dpow(DIM_C, 4), DIM_KAPPA)
DIM_GAP_KAPPA = ddif(DIM_RHS_KAPPA, DIM_G)
DIM_KAPPA_E = ddiv(DIM_G, dpow(DIM_C, 4))
DIM_KAPPA_DOC = ddiv(dpow(DIM_C, 4), DIM_G)
DIM_INV_PROD = dmul(DIM_KAPPA_DOC, DIM_KAPPA_E)
DIM_TAUC = dmul(DIM_TAU, DIM_C)
DIM_X_TAU = ddiv(DIM_KAPPA, DIM_TAUC)
DIM_X_TAU_KE = ddiv(DIM_KAPPA_E, DIM_TAUC)
DIM_DUST = dmul(dmul(DIM_G, DIM_RHO), dpow(DIM_C, -2))
DIM_TAUC_TXT = dstr(DIM_TAUC)
DIM_RHS_TXT = dstr(DIM_RHS_KAPPA)
DIM_GAP_TXT = dstr(DIM_GAP_KAPPA)
DIM_DOC_TXT = dstr(DIM_KAPPA_DOC)
DIM_KE_TXT = dstr(DIM_KAPPA_E)
DIM_INV_PROD_TXT = dstr(DIM_INV_PROD)
DIM_X_TAU_TXT = dstr(DIM_X_TAU)
DIM_X_TAU_KE_TXT = dstr(DIM_X_TAU_KE)
DIM_DUST_TXT = dstr(DIM_DUST)
KAPPA_DOC_TXT = S(KAPPA_DOC)
KAPPA_E_TXT = S(KAPPA_E)
F_PLANCK_TXT = S(F_PLANCK)
IDENT_G_TXT = S(IDENT_G)
IDENT_HBAR_TXT = S(IDENT_HBAR)
IDENT_G_REL = abs(IDENT_G - G_N) / G_N
IDENT_HBAR_REL = abs(IDENT_HBAR - 1)
KAPPA_STAR_REL = abs(KAPPA_STAR - KAPPA_DOC) / KAPPA_DOC


def search_monomial(target, lo=-3, hi=3):
    """穷举 hbar^b * c^d * mP^e 的量纲指数向量，命中即框架内可构造。"""
    hits = []
    for b in range(lo, hi + 1):
        for d in range(lo, hi + 1):
            for e in range(lo, hi + 1):
                vec = (2 * b + d + e, b + e, -b - d)   # (L, M, T)
                if vec == target:
                    hits.append((b, d, e))
    return hits


TARGET_X_TAU = (0, -2, 1)      # 台账 kappa 口径下补齐因子所需量纲
TARGET_X_TAU_KE = (-1, -1, 3)  # 改按 kappa_E 口径
HITS_X_TAU = search_monomial(TARGET_X_TAU)
HITS_X_TAU_KE = search_monomial(TARGET_X_TAU_KE)

ITEMS = [
    ("A-01", "FAIL", "a01_kappa_declared_vs_rhs",
     "来料 §1 声明 [kappa]=m^-2，则右端 c^4/(8*pi*kappa) 量纲 = %s，而 [G] = %s，差 Δ = %s ⇒ 缺一个质量因子，式子不成立" % (DIM_RHS_TXT, dstr(DIM_G), DIM_GAP_TXT)),
    ("A-02", "FAIL", "a02_doc_selfcheck_arithmetic",
     "来料自带量纲核验段写「右侧量纲 m^2 s^-4」：c^4 为 m^4，除以 m^-2 应为 m^6（把除法当乘法，指数错 3）；即便修正为 m^6 仍与 [G] 不匹配 ⇒ 文内第一处自相矛盾"),
    ("A-03", "FAIL", "a03_inverse_of_library_kappa",
     "来料 kappa = c^4/(8*pi*G) 是本库主线 kappa_E = 8*pi*G/c^4 的数值倒数：乘积 = %s（机器零）；但乘积量纲 = %s != 1 ⇒ 「互为倒数」只在数值层成立，量纲层不成立" % (S(KAPPA_INV_PROD), DIM_INV_PROD_TXT)),
    ("A-04", "FAIL", "a04_missing_matter_source",
     "要让 [kappa]=m^-2 成立，8*pi*G 唯一自然补齐项是物质密度：8*pi*G*rho/c^2 量纲 = %s（正是 [kappa]）；反解所需 rho* = c^6/(64*pi^2 G^2) = %s kg/m^3 ⇒ 缺的是物质源项（结构项）而非笔误，零成本修法不存在" % (DIM_DUST_TXT, S(RHO_STAR))),
    ("A-05", "FAIL", "a05_kappa_mass_decoupling",
     "来料 §2 给 r_s ∝ M，§1 给 kappa 与 M 无关：kappa(2M)/kappa(M) = %s，而 GR 同一处 Ricci 标量 ∝ M^2、比值 = %s ⇒ 曲率与质量脱钩，与 §2 组合后自相矛盾" % (S(KAPPA_2M_OVER_1M), S(R_GR_RATIO))),
    ("A-06", "BOUNDARY", "a06_implied_scale",
     "若强行按 [kappa]=m^-2 解读：特征长度 1/sqrt(kappa) = %s m = %s lp；隐含密度 rho* = %s rho_Pl = %s rho_sun ⇒ 若真存在需宇宙学级输入，且落在强场/量子引力区" % (S(L_G), S(L_G_OVER_L_P), S(RHO_STAR_OVER_PL), S(RHO_STAR_OVER_SUN))),
    ("B-07", "PASS", "b07_schwarzschild_ok",
     "§2 史瓦西式 GM/c^2 = r_s/2 逐位标准（[G]=L^3M^-1T^-2、[c^2]=L^2T^-2、[r_s]=L 相容）；其自由元集合 {G,c,M,r_s} 不含 kappa ⇒ 对 kappa 的约束数 = 0，不能用作 §1 的支持证据"),
    ("B-08", "PASS", "b08_planck_two_identities",
     "§3 两条普朗克式均为标准式，且机器验证恰为 2 条定义式恒等式：lp*c^2/mP = %s（应 = G，相对偏差 %s）、lp*mP*c/hbar = %s ⇒ 5 个量秩为 3、亏 2 ⇒ 「G 与 c 是同一场两个分量」是定义式重述，非新的统一结论" % (IDENT_G_TXT, S(IDENT_G_REL), IDENT_HBAR_TXT)),
    ("B-09", "CORRECTED", "b09_doc_numeric_relerr",
     "§6 数值 c^4/G 应为 %s，来料写 1.202e44 ⇒ 相对误差 %s；4 位有效数字口径应写 1.210e44（普朗克力，单位 N）" % (F_PLANCK_TXT, S(DOC_RELERR))),
    ("B-10", "FAIL", "b10_unit_refutes_own_claim",
     "§6 自己给出的单位 kg*m^-1*s^-2 = N，而 c^4/G 的量纲指数 = %s（力）⇒ 力不是曲率密度 ⇒ §6 的单位直接否证 §1 的 [kappa]=m^-2，这是文内第二处自相矛盾" % DIM_DOC_TXT),
    ("B-11", "INFO", "b11_archive_reuse",
     "数值不新增：c^4/G = 普朗克力已在 数据/空间螺旋修复版_第一性审计.json 的 planck_force_newton 归档，本轮 60 位值与其逐位一致 ⇒ 回链复用，不重复登记"),
    ("B-12", "CORRECTED", "b12_selfcaught_force_to_energy",
     "自抓本册首版缺陷：曾把 1 N 当 1 J 直接换算（隐含隐藏长度 1 m）⇒ 已改为显式 E = kappa*l_G（E = %s J = %s GeV = %s M_Pl），并加自检 newton_is_joule_per_meter；此条与 §6 单位批判互为一体：来料缺的正是这个长度" % (S(E_DOC_J), S(KAPPA_DOC_GEV), S(KAPPA_OVER_MPL))),
    ("C-12", "FAIL", "c12_torsion_sum_illegal",
     "§4 的 kappa + tau*c 不可加：[tau*c] = %s != [kappa] = %s ⇒ 复发已判 FAIL 的 C-02 / O-V34-C（30 号册 kappa=Lambda_0-c*tau 同型）" % (DIM_TAUC_TXT, dstr(DIM_KAPPA))),
    ("C-13", "FAIL", "c13_torsion_fix_needs_external_length",
     "补齐 §4 所需因子量纲 = %s（台账 kappa 口径）或 %s（kappa_E 口径）；在 hbar/c/mP 三标度上穷举单项式 b,d,e ∈ [-3,3]，命中数分别为 %d / %d ⇒ 框架内不存在可构造的长度标度，与 O-SCALE 锚定定理同构" % (DIM_X_TAU_TXT, DIM_X_TAU_KE_TXT, len(HITS_X_TAU), len(HITS_X_TAU_KE))),
    ("C-14", "FAIL", "c14_kappa_const_vs_field",
     "§5「能量注入后曲率 kappa 上升」与 §1 硬矛盾：G、c 是常数 ⇒ kappa ≡ %s 恒定（对 (G,c) 的 spread = 0）⇒ §1 与 §5 不能同时成立" % KAPPA_DOC_TXT),
    ("C-15", "INFO", "c15_no_dynamical_content",
     "自由度口径：kappa 由 (G,c) 完全决定 ⇒ 新增自由度 0；「替代能动张量本源项」属 L1 恒等重述；按 Ω5 口径（连续常数 1 / 节点 0）形式 PASS 但动力学内容为零"),
    ("C-16", "FAIL", "c16_symbol_ledger_conflict",
     "符号台账冲突：本库主线 kappa = 8*pi*G/c^4（21 号册 B5 表、31 号册 §二、V3.2_gravity_sector.py:15）vs 来料 kappa = c^4/(8*pi*G)，同一符号两义且互为倒数 ⇒ A-07 型台账冲突，代入场方程前必须先裁决口径"),
    ("C-17", "INFO", "c17_defect_family_recurrence",
     "缺陷族复发计数 = 5：总账 B4（2026/6/9，标题已自标量纲非齐次）/ claims C88+C30（falsified）/ 30 号册 V03+V04（FAIL，已修）/ 30 号册 C-02（FAIL）/ 本册 ⇒ 建议体例门禁新增「爱因斯坦系数方向」条款：凡 G_munu = 系数 * T_munu，机器核对系数为 8*pi*G/c^4"),
    ("D-18", "BOUNDARY", "d18_route_r1",
     "路线 R1（零成本）：把 §1 改写为 G = c^4*T_munu/(8*pi*G_munu)（尘埃情形 G = c^2*rho/(8*pi*kappa)）⇒ 可同时关闭 A-01/A-04/A-05/C-14；代价 0，收益 = 消除 4 条 FAIL，但不再有「本源项」宣称"),
    ("D-19", "BOUNDARY", "d19_route_r2",
     "路线 R2：声明 kappa ≡ %s 为定值场并删除 §5；若改走「跑动 G」路线则代价 = +1 自由度，且与 G 的实验测量精度（相对约 1.5e-4）冲突" % KAPPA_DOC_TXT),
    ("D-20", "BOUNDARY", "d20_route_r3",
     "路线 R3（真挠率修正）：走 31 号册已验证的 ECSK 标准式 (1/2) g_tau * tau * R，kappa 保持 8*pi*G/c^4 不动 ⇒ 代价 = 新增 2 个自由参数 (g_tau, m_tau)，违反 Ω5 除非登记为外部输入"),
    ("D-21", "INFO", "d21_no_route_scored",
     "本册未对 R1/R2/R3 打分、排序或推荐（沿用 30 号册 E-06 纪律）；取舍权保留给用户"),
]

CHECKS = []


def chk(name, ok, detail):
    CHECKS.append((name, "PASS" if ok else "FAIL", detail))


chk("kappa_inverse_machine_zero", abs(KAPPA_INV_PROD - 1) <= Decimal("1e-50"),
    "kappa_doc * kappa_E - 1 = %s" % S(KAPPA_INV_PROD - 1))
chk("doc_relerr_in_band", Decimal("-0.007") < DOC_RELERR < Decimal("-0.006"),
    "doc 1.202e44 vs 机器值 相对误差 = %s" % S(DOC_RELERR))
chk("kappa_doc_is_force_not_curvature", DIM_KAPPA_DOC == (1, 1, -2) and DIM_KAPPA_DOC != DIM_KAPPA,
    "dim(c^4/G) = %s, dim(kappa 声明) = %s" % (DIM_DOC_TXT, dstr(DIM_KAPPA)))
chk("kappa_e_is_inverse_force", DIM_KAPPA_E == (-1, -1, 2), "dim(8*pi*G/c^4) = %s" % DIM_KE_TXT)
chk("dust_term_closes_to_L2", DIM_DUST == (-2, 0, 0), "dim(8*pi*G*rho/c^2) = %s" % DIM_DUST_TXT)
chk("rho_star_reproduces_kappa_doc", KAPPA_STAR_REL <= Decimal("1e-50"),
    "相对偏差 = %s" % S(KAPPA_STAR_REL))
chk("planck_identity_g_machine_zero", IDENT_G_REL <= Decimal("1e-50"),
    "lp*c^2/mP = %s（相对偏差 %s）" % (IDENT_G_TXT, S(IDENT_G_REL)))
chk("planck_identity_hbar_machine_zero", IDENT_HBAR_REL <= Decimal("1e-50"),
    "lp*mP*c/hbar = %s" % IDENT_HBAR_TXT)
chk("gr_curvature_scales_quadratic", abs(R_GR_RATIO - 4) <= Decimal("1e-40"),
    "R(2Msun)/R(Msun) = %s" % S(R_GR_RATIO))
chk("kappa_independent_of_mass", KAPPA_2M_OVER_1M == 1, "kappa(2M)/kappa(M) = %s" % S(KAPPA_2M_OVER_1M))
chk("no_internal_length_scale", len(HITS_X_TAU) == 0 and len(HITS_X_TAU_KE) == 0,
    "穷举 hbar^b c^d mP^e 命中数 = %d / %d" % (len(HITS_X_TAU), len(HITS_X_TAU_KE)))
_d1, _d2 = S(C4 / (8 * PI * G_N)), S((HBAR * G_N / C_LIGHT ** 3).sqrt())
chk("determinism_readouts", _d1 == KAPPA_DOC_TXT and _d2 == S(LP), "复算读数逐位一致")
chk("newton_is_joule_per_meter", ddiv(DIM_N, DIM_J) == (-1, 0, 0),
    "dim(N/J) = %s ⇒ 1 N = 1 J/m，力→能量必须显式乘一个长度（本册取 l_G）" % dstr(ddiv(DIM_N, DIM_J)))

VERDICTS = {}
for _id, _v, _slug, _detail in ITEMS:
    VERDICTS[_v] = VERDICTS.get(_v, 0) + 1
N_FAIL = sum(1 for c in CHECKS if c[1] == "FAIL")

KEY = {
    "force_planck": F_PLANCK_TXT,
    "kappa_doc": KAPPA_DOC_TXT,
    "kappa_E": KAPPA_E_TXT,
    "kappa_inverse_product": S(KAPPA_INV_PROD),
    "doc_relerr": S(DOC_RELERR),
    "l_G_m": S(L_G),
    "l_G_over_l_P": S(L_G_OVER_L_P),
    "rho_star_kgm3": S(RHO_STAR),
    "rho_star_over_rho_Pl": S(RHO_STAR_OVER_PL),
    "rho_star_over_rho_sun": S(RHO_STAR_OVER_SUN),
    "kappa_lG_energy_J": S(E_DOC_J),
    "kappa_lG_energy_GeV": S(KAPPA_DOC_GEV),
    "kappa_lG_energy_over_MPl": S(KAPPA_OVER_MPL),
    "lp_m": S(LP),
    "mp_kg": S(MP),
    "MPl_GeV": S(M_PL_GEV),
    "gr_curv_ratio_2M_1M": S(R_GR_RATIO),
    "hits_x_tau": len(HITS_X_TAU),
    "hits_x_tau_kappaE": len(HITS_X_TAU_KE),
    "dims": {
        "G": dstr(DIM_G), "c": dstr(DIM_C), "kappa_declared": dstr(DIM_KAPPA),
        "tau": dstr(DIM_TAU), "rho": dstr(DIM_RHO),
        "rhs_c4_over_kappa": DIM_RHS_TXT, "gap": DIM_GAP_TXT,
        "kappa_E": DIM_KE_TXT, "kappa_doc": DIM_DOC_TXT,
        "inverse_product": DIM_INV_PROD_TXT, "tau_times_c": DIM_TAUC_TXT,
        "fix_factor_tau": DIM_X_TAU_TXT, "fix_factor_tau_kappaE": DIM_X_TAU_KE_TXT,
        "dust_8piG_rho_c2": DIM_DUST_TXT,
    },
}

PAYLOAD = {
    "round": "r18",
    "date": "2026-10-07",
    "title": "外部来稿《TUFT V3.4：G 与 c 核心关系》量纲 / 自由度 / 符号冲突三表审计",
    "counts": {"items": len(ITEMS), "checks": len(CHECKS), "check_fail": N_FAIL},
    "verdicts": VERDICTS,
    "items": [{"id": i, "verdict": v, "slug": s, "detail": d} for i, v, s, d in ITEMS],
    "selfcheck": [{"name": n, "verdict": v, "detail": d} for n, v, d in CHECKS],
    "key_numbers": KEY,
    "reused_defect_ids": ["C-02", "C-05", "C-88", "C-30", "O-V34-C", "O-V34-C/O-SCALE"],
    "sibling_products": [
        "数据/TUFT-V3.4四模块审计与路线选址前置_2026-10-07.json",
        "../../../07_统一场方程/空间螺旋几何化统一场论/30_外部来稿审计_自标V3.4能量动量守恒与挠子量子场_2026-10-07.md",
        "../../../07_统一场方程/空间螺旋几何化统一场论/31_外部来稿V3.4修复版_结构修正与能标窗口_2026-10-07.md",
    ],
}


def write_outputs():
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    stem = "TUFT-G与c核心关系_量纲自由度与符号冲突审计_2026-10-07"
    with open(os.path.join(DATA, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(PAYLOAD, f, ensure_ascii=False, indent=2)
    lines = []
    lines.append("# %s" % PAYLOAD["title"])
    lines.append("")
    lines.append("日期：%s · 轮次：%s · 条目 %d（%s）· 自检 %d/%d · 退出码 %d"
                 % (PAYLOAD["date"], PAYLOAD["round"], len(ITEMS),
                    " / ".join("%s=%d" % (k, VERDICTS[k]) for k in sorted(VERDICTS)),
                    len(CHECKS) - N_FAIL, len(CHECKS), 1 if N_FAIL else 0))
    lines.append("")
    lines.append("复算仪器：`源码/TUFT-G与c核心关系_量纲自由度与符号冲突审计_2026-10-07.py`（纯标准库 decimal 60 位）")
    lines.append("")
    lines.append("## 条目")
    lines.append("")
    for i, v, s, d in ITEMS:
        lines.append("- **[%s] %s** `%s` —— %s" % (v, i, s, d))
    lines.append("")
    lines.append("## 自检")
    lines.append("")
    for n, v, d in CHECKS:
        lines.append("- [%s] %s —— %s" % (v, n, d))
    lines.append("")
    lines.append("## 关键数值")
    lines.append("")
    lines.append("```")
    lines.append(json.dumps(KEY, ensure_ascii=False, indent=2))
    lines.append("```")
    with open(os.path.join(DATA, stem + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    write_outputs()
    print("items=%d  checks=%d  check_fail=%d" % (len(ITEMS), len(CHECKS), N_FAIL))
    print("verdicts: %s" % json.dumps(VERDICTS, ensure_ascii=False))
    print("kappa_doc = %s  kappa_E = %s  product = %s" % (KAPPA_DOC_TXT, KAPPA_E_TXT, S(KAPPA_INV_PROD)))
    print("c^4/G = %s N   doc 1.202e44 relerr = %s" % (F_PLANCK_TXT, S(DOC_RELERR)))
    for n, v, d in CHECKS:
        if v == "FAIL":
            print("SELFCHECK-FAIL %s :: %s" % (n, d))
    return 1 if N_FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
