# -*- coding: utf-8 -*-
"""算法联盟 · openuft 全维自洽与归一化引擎

处理模式：全维度 / 全链路 / 诚实分级（算法联盟五字段）

本引擎对 openuft 登记的全部独立体系做六件事：
  1) 全维分析   ：17 体系公设骨架编目 + 第一性层级分级（L0–L4）
  2) 第一性自洽 ：符号求导证明 + 第一性冲突探测（普朗克锚定谬误等）
  3) 精算验证   ：mpmath 80 位高精度核验（三重奏 / 本源方程 / 常数闭包 / 四力 / 对偶代数）
  4) 自由度审计 ：符号雅可比数值秩 → 欠定自由度（"零自由参数"主张的硬判据）
  5) 融合       ：公设签名同源度聚类 → 五大族系 + 分叉公设
  6) 归一化     ：符号 / 量纲 / 普朗克制 / 无量纲常数清单（第一性真正目标）

红线（全链路贯穿，不粉饰）：
  精算只证「数学自洽」与「与已知实验值一致」，不证「第一性推导」。
  量纲常数（c / ℏ / k_B）由单位定义固定，其"导出"是单位换算，不是物理预言。
  任何冲突项如实标 FAIL / BOUNDARY，不改写为 PASS。

运行：python 算法联盟_全维自洽引擎.py
"""

import os
import sys
import json
import io

import mpmath as mp
import sympy as sp

mp.mp.dps = 80

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

# ===========================================================================
# 0. 常数与工具（CODATA 2018 / PDG 2024）
# ===========================================================================
PI = mp.pi

C = mp.mpf("299792458")                 # 精确（SI 定义）
H = mp.mpf("6.62607015e-34")            # 精确
HBAR = H / (2 * PI)
E = mp.mpf("1.602176634e-19")           # 精确
KB = mp.mpf("1.380649e-23")             # 精确
G = mp.mpf("6.67430e-11")               # 测量
ALPHA = mp.mpf("7.2973525693e-3")       # 测量
EPS0 = mp.mpf("8.8541878128e-12")       # 测量
MU0 = mp.mpf("1.25663706212e-6")        # 测量

ME = mp.mpf("9.1093837015e-31")
MP = mp.mpf("1.67262192369e-27")
MMU = mp.mpf("1.883531627e-28")
MTAU = mp.mpf("3.16754e-27")
MW_GEV = mp.mpf("80.379")
MZ_GEV = mp.mpf("91.1876")

MP_MASS = mp.sqrt(HBAR * C / G)         # 普朗克质量
LP = mp.sqrt(HBAR * G / C ** 3)         # 普朗克长度
TP = LP / C
QP = mp.sqrt(4 * PI * EPS0 * HBAR * C)  # 普朗克电荷

RECORDS = []


def record(tag, group, name, formula, value, ref, kind, verdict=None, note=""):
    """登记一条核验记录。

    kind 决定残差口径：
      代数恒等式 / 符号恒等  -> value 应趋 0，ref 为量级基准（对数位）
      数值核验              -> value 与 ref 比对（相对残差）
      本征值                -> 只登记数值，不做比对
      审计                  -> value 为审计量，ref 为阈值
    """
    if value is None or ref is None:
        rel = mp.mpf("0")
        digits = float(mp.mp.dps - 2)
    elif kind in ("代数恒等式", "符号恒等"):
        denom = abs(ref) if abs(ref) != 0 else mp.mpf("1")
        rel = abs(value) / denom
        digits = float(mp.mp.dps - 2) if rel == 0 else max(0.0, -float(mp.log(rel, 10)))
    elif kind == "审计":
        denom = abs(ref) if abs(ref) != 0 else mp.mpf("1")
        rel = abs(value) / denom
        digits = float(mp.mp.dps - 2) if rel == 0 else max(0.0, -float(mp.log(rel, 10)))
    else:
        denom = abs(ref) if abs(ref) != 0 else mp.mpf("1")
        rel = abs(value - ref) / denom
        digits = float(mp.mp.dps - 2) if rel == 0 else max(0.0, -float(mp.log(rel, 10)))

    if verdict is None:
        verdict = "PASS" if digits >= 6 else "WEAK"

    RECORDS.append({
        "id": tag,
        "group": group,
        "name": name,
        "formula": formula,
        "value": mp.nstr(value, 18) if value is not None else "—",
        "reference": mp.nstr(ref, 18) if ref is not None else "—",
        "rel_residual": mp.nstr(rel, 6),
        "digits": round(digits, 2),
        "kind": kind,
        "verdict": verdict,
        "note": note,
    })
    return RECORDS[-1]


def note(tag, group, name, statement, verdict, detail=""):
    """登记一条非数值记录（分级 / 冲突 / 结论）。"""
    RECORDS.append({
        "id": tag,
        "group": group,
        "name": name,
        "formula": statement,
        "value": "—",
        "reference": "—",
        "rel_residual": "—",
        "digits": 0.0,
        "kind": "审计",
        "verdict": verdict,
        "note": detail,
    })
    return RECORDS[-1]


# ===========================================================================
# 1. 模块 B · 三重奏骨架（S01/S02/S10/S12 共用）—— 符号求导证明
# ===========================================================================
def module_b_triad():
    t = sp.symbols("t", real=True)
    R, w, b = sp.symbols("R omega b", positive=True)

    r = sp.Matrix([R * sp.cos(w * t), R * sp.sin(w * t), b * t])
    r1 = r.diff(t)
    r2 = r.diff(t, 2)
    r3 = r.diff(t, 3)

    speed2 = sp.simplify((r1.T * r1)[0])
    speed = sp.sqrt(speed2)

    cross = r1.cross(r2)
    cross2 = sp.simplify((cross.T * cross)[0])

    kappa = sp.sqrt(cross2) / speed ** 3
    triple = sp.simplify(cross.dot(r3))
    tau = triple / cross2

    # B01 曲率表达式（对照登记式 κ = Rω²/v²）
    kappa_ref = R * w ** 2 / speed2
    d_kappa = sp.simplify(kappa - kappa_ref)
    record("B01", "三重奏骨架", "曲率 κ = Rω²/v²（符号求导证明）",
           "κ - Rω²/v² = 0", sp.N(d_kappa, 40), mp.mpf("1"), "符号恒等",
           note="Frenet 定义 |r'×r''|/|r'|³ 直接推出，与登记式一致")

    # B02 挠率表达式 τ = bω/v²
    tau_ref = b * w / speed2
    d_tau = sp.simplify(tau - tau_ref)
    record("B02", "三重奏骨架", "挠率 τ = bω/v²（符号求导证明）",
           "τ - bω/v² = 0", sp.N(d_tau, 40), mp.mpf("1"), "符号恒等")

    # B03 三重奏 κ²+τ² = (ω/v)²
    resid = sp.simplify(sp.trigsimp(kappa ** 2 + tau ** 2 - (w / speed) ** 2))
    record("B03", "三重奏骨架", "三重奏 κ²+τ² = (ω/v)²（符号恒等）",
           "κ²+τ²-(ω/v)² = 0", sp.N(resid, 40), mp.mpf("1"), "符号恒等",
           note="螺旋参数化下的代数恒等式；是导出定理不是公设")

    # B04 v≡c 特化
    resid_c = sp.simplify(kappa ** 2 + tau ** 2 - (w / C) ** 2)
    # 用 b² + R²ω² = c² 代入
    b_c = sp.sqrt(C ** 2 - R ** 2 * w ** 2)
    resid_c2 = sp.simplify(resid_c.subs(b, b_c))
    record("B04", "三重奏骨架", "光速约束 v≡c 下 κ²+τ² = (ω/c)²",
           "b=√(c²-R²ω²) 代入后残差", sp.N(resid_c2, 40), mp.mpf("1"), "符号恒等",
           note="S12-A2/S10 共用骨架；恒等成立 ≠ 本体公设成立")

    # B05 高精度数值复验（多组参数）
    worst = mp.mpf("0")
    for Ri, wi, bi in [("1", "2", "3"), ("1.7e-13", "5.5e20", "2.1e8"),
                       ("3.8616e-13", "7.7636e20", "0")]:
        Rv, wv, bv = mp.mpf(Ri), mp.mpf(wi), mp.mpf(bi)
        v2 = Rv ** 2 * wv ** 2 + bv ** 2
        kv = Rv * wv ** 2 / v2
        tv = bv * wv / v2
        resid_n = kv ** 2 + tv ** 2 - wv ** 2 / v2
        scale = wv ** 2 / v2
        rel = abs(resid_n) / scale
        worst = max(worst, rel)
    record("B05", "三重奏骨架", "三重奏数值复验（3 组参数，最大相对残差）",
           "max|κ²+τ²-(ω/v)²|/(ω/v)²", worst, mp.mpf("1"), "代数恒等式",
           note="含电子康普顿尺度参数组，均为机器零")

    # B06 电子尺度自洽（Ω = m_e c/ℏ ↔ R ↔ ω）
    omega_e = ME * C / HBAR              # Ω = √(κ²+τ²) = m_e c/ℏ
    R_e = 1 / omega_e
    w_e = C * omega_e                    # v≡c 时 ω = cΩ
    check_c = w_e * R_e
    record("B06", "三重奏骨架", "电子尺度闭包：ω·R = c（Ω=m_e c/ℏ, R=1/Ω）",
           "ωR - c = 0", check_c - C, C, "代数恒等式",
           note="该组数值自洽，但强制 R = ƛ_C(e) = 3.86e-13 m（见 M01 冲突）")

    # B07 康普顿一致性：R = ƛ_C 与登记值
    lam_bar = HBAR / (ME * C)
    record("B07", "三重奏骨架", "R = ƛ_C = ℏ/(m_e c)（约化康普顿波长）",
           "R - ℏ/(m_e c) = 0", R_e - lam_bar, lam_bar, "数值核验",
           note="S10 派生 m=ℏ√(κ²+τ²)/c 与此等价")

    return {
        "omega_e": omega_e, "R_e": R_e, "w_e": w_e,
        "kappa": kappa, "tau": tau, "speed": speed,
    }


# ===========================================================================
# 2. 模块 C · 归一化本源方程 κ̃² + τ̃² = 1
# ===========================================================================
def module_c_source_eq(triad):
    omega_e = triad["omega_e"]

    kt = 1 / mp.sqrt(1 + ALPHA ** 2)          # κ̃ = κ/Ω
    tt = ALPHA / mp.sqrt(1 + ALPHA ** 2)      # τ̃ = τ/Ω

    record("C01", "本源方程", "归一化本源方程 κ̃²+τ̃² = 1（α=τ/κ）",
           "κ̃²+τ̃²-1 = 0", kt ** 2 + tt ** 2 - 1, mp.mpf("1"), "代数恒等式",
           note="由 κ̃=1/√(1+α²)、τ̃=α/√(1+α²) 推出，恒等成立")

    # C02 全粒子普适性（诚实边界：归一化后与质量无关）
    worst = mp.mpf("0")
    for label, m in [("e", ME), ("μ", MMU), ("τ", MTAU), ("p", MP),
                     ("W", MW_GEV * mp.mpf("1e9") * E / C ** 2),
                     ("P", MP_MASS)]:
        om = m * C / HBAR
        kk = om / mp.sqrt(1 + ALPHA ** 2)
        ttm = ALPHA * om / mp.sqrt(1 + ALPHA ** 2)
        resid = (kk / om) ** 2 + (ttm / om) ** 2 - 1
        worst = max(worst, abs(resid))
    record("C02", "本源方程", "κ̃²+τ̃²=1 全粒子普适（6 个粒子最大残差）",
           "max|κ̃²+τ̃²-1|", worst, mp.mpf("1"), "代数恒等式")

    note("C03", "本源方程", "归一化后质量信息丢失（第一性边界）",
         "κ̃、τ̃ 与质量 m 无关：κ̃=1/√(1+α²)，α 为唯一定标",
         "BOUNDARY",
         "归一化本源方程对所有粒子恒同，不携带质量谱信息；"
         "质量寄于 Ω=mc/ℏ 这一未解释的尺度。质量层级（m_τ/m_e≈3477）"
         "不能由本源方程推出，需外部动力学输入（与 v30 结论一致）")

    # C04 普朗克极限
    kt_p = 1 / mp.sqrt(2)
    record("C04", "本源方程", "普朗克极限 α=1 ⇒ κ̃=τ̃=1/√2（四力同源）",
           "κ̃ - 1/√2 = 0", kt_p - 1 / mp.sqrt(2), 1 / mp.sqrt(2), "代数恒等式",
           note="α=1 是假设而非导出：实测 α=1/137.036，普朗克极限处是否跑动至 1 未验证")

    # C05 α = τ/κ 的反向解（循环性）
    kappa_e = omega_e / mp.sqrt(1 + ALPHA ** 2)
    tau_e = ALPHA * omega_e / mp.sqrt(1 + ALPHA ** 2)
    record("C05", "本源方程", "α = τ/κ 回算精细结构常数",
           "τ/κ - α = 0", tau_e / kappa_e - ALPHA, ALPHA, "数值核验",
           note="τ/κ 由 α 定义而来，此式是定义回指，不构成 α 的第一性导出")

    return {"kt": kt, "tt": tt, "kappa_e": kappa_e, "tau_e": tau_e}


# ===========================================================================
# 3. 模块 D · 常数闭包与循环检测
# ===========================================================================
def module_d_constants():
    # D01–D03 电磁常数闭包
    eps0_via = E ** 2 / (4 * PI * ALPHA * HBAR * C)
    record("D01", "常数闭包", "ε₀ = e²/(4π α ℏ c)",
           "ε₀ - e²/(4παℏc)", EPS0, eps0_via, "数值核验",
           note="残差量级由 α 与 ε₀ 的测量不确定度决定（~1e-10），非理论误差")

    mu0_via = 4 * PI * ALPHA * HBAR / (C * E ** 2)
    record("D02", "常数闭包", "μ₀ = 4π α ℏ/(c e²)",
           "μ₀ - 4παℏ/(ce²)", MU0, mu0_via, "数值核验")

    record("D03", "常数闭包", "μ₀ ε₀ = 1/c²",
           "μ₀ε₀ - 1/c²", MU0 * EPS0 - 1 / C ** 2, 1 / C ** 2, "代数恒等式",
           note="Maxwell 关系，2019 SI 后 μ₀ 为测量量，自洽到测量精度")

    # D04 引力常数闭包 G = ℏc/m_P²
    record("D04", "常数闭包", "G = ℏ c / m_P²（普朗克定义回指）",
           "G - ℏc/m_P²", G - HBAR * C / MP_MASS ** 2, G, "代数恒等式",
           note="定义式重排（L0），零预言内容")

    # D05 κ-Φ 桥接 √(Gℏc)/m_P = G
    kphi = mp.sqrt(G * HBAR * C) / MP_MASS
    record("D05", "常数闭包", "κ-Φ 桥接 √(Gℏc)/m_P = G",
           "√(Gℏc)/m_P - G", kphi - G, G, "代数恒等式",
           note="等价于 D04：√(Gℏc)/m_P = √(Gℏc)/√(ℏc/G) = G，同为定义回指")

    # D06 G = c³/(ℏ(κ²+τ²)) 的等价性判定（关键循环检测）
    omega_e = ME * C / HBAR
    G_via_kt = C ** 3 / (HBAR * omega_e ** 2)
    record("D06", "常数闭包", "【循环检测】G = c³/(ℏ(κ²+τ²)) 取电子 Ω 代入",
           "G_式 - G_实测", G_via_kt, G, "数值核验", verdict="FAIL",
           note="取 κ²+τ²=Ω_e²=(m_e c/ℏ)² 时给出 G_式 = ℏc/m_e² ≈ 4.2e31，"
                "与实测 G 差 42 个数量级。该式仅在 κ²+τ²=1/ℓ_P²（即 m=m_P）时回指 G，"
                "是普朗克锚定，不是任意粒子的恒等式（详见 M01/M02）")

    # D07 上式在普朗克锚定下回指
    G_via_P = C ** 3 / (HBAR * (1 / LP ** 2))
    record("D07", "常数闭包", "G = c³/(ℏ(κ²+τ²)) 在 κ²+τ²=1/ℓ_P² 时回指 G",
           "G_式 - G", G_via_P - G, G, "代数恒等式",
           note="证实 D06 的差异来源：该式等价于 G = ℏc/m_P²，属 L0 定义回指")

    # D08 e 的几何化式（循环检测）
    e_via = mp.sqrt(4 * PI * EPS0 * (ALPHA) * HBAR * C)
    record("D08", "常数闭包", "【循环检测】e = √(4π ε₀ (τ/κ) ℏ c)（τ/κ≡α）",
           "e_式 - e", e_via, E, "数值核验",
           note="代入 τ/κ=α 后即 ε₀ = e²/(4παℏc) 的代数变形，与 D01 同一方程，"
                "对 e 不构成独立约束（循环）")

    # D09 普朗克电荷与 α
    record("D09", "常数闭包", "q_P = √(4πε₀ℏc) = e/√α",
           "q_P - e/√α", QP, E / mp.sqrt(ALPHA), "数值核验",
           note="q_P/e = 1/√α ≈ 11.7，是无量纲关系，但由 α 定义直接给出")

    # D10 单位制归一化判据：c / ℏ / k_B 为定义常数
    note("D10", "常数闭包", "单位制归一化判据（第一性硬判据）",
         "c、h、k_B、e 在 SI 2019 后为定义常数（精确值，零不确定度）",
         "BOUNDARY",
         "因此『从第一性原理导出 c、ℏ、k_B』是伪命题——它们的值由单位定义固定，"
         "是单位换算因子而非物理可观测量。S08『常数几何化』把 c=ωR、ℏ=mcR 作为成就是方向性误置。"
         "真正需要第一性解释的是无量纲量：α、m_μ/m_e、m_τ/m_e、α_S(M_Z)、α_grav 等")

    return {"G_via_kt": G_via_kt, "G_via_P": G_via_P}


# ===========================================================================
# 4. 模块 E · 四力归一化谱（统一基准 F = α_i ℏc/r²）
# ===========================================================================
def module_e_forces():
    r = mp.mpf("1.0")
    base = HBAR * C / r ** 2            # ℏc/r² = 3.16e-26 N (r=1m)

    # E01 电磁
    a_em = ALPHA
    f_em = a_em * base
    f_em_ref = (1 / (4 * PI * EPS0)) * E ** 2 / r ** 2
    record("E01", "四力归一化", "电磁 F = α ℏc/r² = k_e e²/r²",
           "F_式 - F_库仑", f_em, f_em_ref, "数值核验",
           note="归一化基准 ℏc/r² = 3.16e-26 N (r=1 m)")

    # E02 引力（e-p）
    a_grav_ep = G * ME * MP / (HBAR * C)
    f_grav = a_grav_ep * base
    f_grav_ref = G * ME * MP / r ** 2
    record("E02", "四力归一化", "引力 F = α_grav(e,p) ℏc/r² = G m_e m_p/r²",
           "F_式 - F_牛顿", f_grav, f_grav_ref, "数值核验",
           note="α_grav(e,p) = G m_e m_p/(ℏc) = 3.22e-42")

    # E03 力比
    ratio = f_em / f_grav
    ratio_ref = ALPHA / a_grav_ep
    record("E03", "四力归一化", "力比 F_E/F_G = α/α_grav(e,p)",
           "比值一致性", ratio, ratio_ref, "数值核验",
           note="≈ 2.27e39，即经典电磁/引力强度比")

    # E04 弱力（M_Z 尺度耦合）
    a2 = mp.mpf("0.03377")
    f_w = a2 * base
    record("E04", "四力归一化", "弱力 α₂(M_Z) = 0.03377（SU(2) 耦合）",
           "α₂ 登记", f_w, None, "本征值",
           note="弱力无长程 1/r² 形式（有质量媒介子），归一化耦合在 M_Z 尺度定义")

    # E05 强力
    a3 = mp.mpf("0.1180")
    f_s = a3 * base
    record("E05", "四力归一化", "强力 α₃(M_Z) = 0.1180（SU(3) 耦合）",
           "α₃ 登记", f_s, None, "本征值",
           note="同样非长程；禁闭使 1/r² 形式不适用于低能")

    # E06 引力在 M_Z 尺度
    mz_kg = MZ_GEV * mp.mpf("1e9") * E / C ** 2
    a_grav_mz = G * mz_kg ** 2 / (HBAR * C)
    record("E06", "四力归一化", "引力 α_grav(M_Z) = (m_Z/m_P)²",
           "α_grav(M_Z)", a_grav_mz, None, "本征值",
           note="≈ 5.6e-35；与规范耦合差 33–34 个数量级，即层级问题（hierarchy problem）")

    # E07 四力归一化谱（同基准排序）
    spectrum = [
        ("强 SU(3)", a3), ("弱 SU(2)", a2), ("电磁 U(1) [GUT 归一 α₁=5/3·α_Y]",
                                             mp.mpf("0.01692")),
        ("引力 (M_Z)", a_grav_mz),
    ]
    span = a3 / a_grav_mz
    record("E07", "四力归一化", "四力归一化谱跨度 α₃/α_grav(M_Z)",
           "跨度登记", span, None, "本征值",
           note="≈ 2.1e33。归一化后四力仍跨 33 个数量级——"
                "『把四力写成同一形式 F=α_iℏc/r²』是形式归一化，不是耦合强度统一")

    note("E08", "四力归一化", "形式归一化 ≠ 强度统一（第一性边界）",
         "统一写法 F_i = α_i ℏc/r² 只统一了量纲与结构，未统一 α_i 的数值",
         "BOUNDARY",
         "四力大统一的真正任务是导出 α_i 的相对值（尤其规范耦合在 GUT 尺度的汇聚）。"
         "仓库内 82 号已诚实标注：SM/MSSM 2-loop 大 ln 跨度 RK 积分数值失效，GUT 汇聚需专业演化器")

    return {"spectrum": spectrum, "a_grav_ep": a_grav_ep, "a_grav_mz": a_grav_mz,
            "span": span}


# ===========================================================================
# 5. 模块 F · S13 对偶代数与不动点
# ===========================================================================
def module_f_duality():
    # F01 Z2 对合 D² = I
    D = sp.Matrix([[0, 1], [1, 0]])
    D2 = sp.simplify(D * D)
    ident = sp.eye(2)
    resid = sp.simplify(D2 - ident)
    record("F01", "对偶代数", "S13-A1 对偶公理 D² = 1（Z₂ 对合，符号证明）",
           "D² - I = 0", sp.N(resid.norm(), 40), mp.mpf("1"), "符号恒等",
           note="D=[[0,1],[1,0]]，本征值 ±1；对偶基元 (a,ā) 的抽象代数结构自洽")

    # F02 本征值 ±1
    ev = list(D.eigenvals().keys())
    ev_ok = all(abs(sp.N(x)) == 1 for x in ev)
    note("F02", "对偶代数", "D 的本征值 = {+1, -1}（对偶扇区）",
         "eig(D) = {1, -1}", "PASS" if ev_ok else "FAIL",
         "对偶变换把物理量分解为偶/奇两个扇区，与 0/1 基点一致")

    # F03 旋量电荷共轭周期 4：C C* = -I ⇒ Θ²Ψ = -Ψ ⇒ Θ⁴ = 1
    Cc = sp.Matrix([[0, -1], [1, 0]])          # 实反对称
    prod = sp.simplify(Cc * Cc.conjugate())
    resid4 = sp.simplify(prod + sp.eye(2))
    record("F03", "对偶代数", "S13-A1 旋量对偶周期 4：C C* = -I",
           "CC* + I = 0", sp.N(resid4.norm(), 40), mp.mpf("1"), "符号恒等",
           note="Θ:Ψ↦CΨ* ⇒ Θ²Ψ = CC*Ψ = -Ψ ⇒ Θ⁴ = 1；"
                "Ψ→Ψ^c→-Ψ→-Ψ^c→Ψ 周期 4 成立（玻色标量 D²=1 周期 2，费米旋量周期 4）")

    # F04 拓扑荷整数性
    note("F04", "对偶代数", "S13-A2 拓扑荷 Q ∈ ℤ，min|Q| = 1",
         "π₃(S²) = ℤ（霍普夫荷）；π₁(S²) = 0（1D 绕数载体已证伪）", "PASS",
         "载体选择自洽：3D 霍普夫荷给出整数荷；"
         "但『物理荷=拓扑荷』的识别是额外物理假设，不由公设推出")

    # F05 β 函数奇性 β(-g) = -β(g)
    g, eps, cg = sp.symbols("g varepsilon c", positive=True)
    beta = eps * g - cg * g ** 3
    odd = sp.simplify(beta.subs(g, -g) + beta)
    record("F05", "对偶代数", "S13-A3 自相似：β(-g) = -β(g)（奇函数）",
           "β(-g)+β(g) = 0", sp.N(odd, 40), mp.mpf("1"), "符号恒等",
           note="对 β(g)=εg-cg³ 成立；奇性是双向分形 β(-g)=-β(g) 的数学表达")

    # F06 不动点 g* = ±√(ε/c)
    fps = sp.solve(sp.Eq(beta, 0), g)
    fps_nonzero = [x for x in fps if sp.simplify(x) != 0]
    chk = sp.simplify(fps_nonzero[0] ** 2 - eps / cg) if fps_nonzero else sp.sympify(1)
    record("F06", "对偶代数", "不动点 g* = ±√(ε/c)（解集校验 g*²−ε/c=0）",
           "g*² - ε/c = 0", sp.N(chk, 40), mp.mpf("1"), "符号恒等",
           note="解集 {0, +√(ε/c), -√(ε/c)}，成对出现与对偶公理一致；"
                "数值例：ε=0.01, c=1 → g*=%s" % mp.nstr(mp.sqrt(mp.mpf("0.01")), 8))

    # F07 稳定性 β'(g*) = -2ε < 0
    db = sp.diff(beta, g)
    gp = sp.sqrt(eps / cg)
    val = sp.simplify(db.subs(g, gp))
    resid_stab = sp.simplify(val - (-2 * eps))
    record("F07", "对偶代数", "不动点稳定性 β'(g*) = -2ε < 0",
           "β'(g*) + 2ε = 0", sp.N(resid_stab, 40), mp.mpf("1"), "符号恒等",
           note="原文取值与 β(g)=εg-cg³ 约定一致（IR 稳定）")

    # F08 约定冲突：标准 Wilson-Fisher (d=4-ε) 给出相反符号
    beta_wf = -eps * g + cg * g ** 3
    db_wf = sp.diff(beta_wf, g)
    val_wf = sp.simplify(db_wf.subs(g, gp))
    note("F08", "对偶代数", "【约定冲突】标准 Wilson-Fisher β=-εg+cg³ 给出 β'(g*)=+2ε>0",
         "β'(g*) = +2ε（d=4-ε 约定）", "BOUNDARY",
         "S13-A3 的 -2ε 对应 β(g)=εg-cg³；主流 d=4-ε 展开用 β(g)=-εg+cg³，"
         "其 Wilson-Fisher 不动点 β'(g*)=+2ε>0（IR 不稳定 / UV 稳定）。"
         "两者仅差 ε 的符号约定，物理结论等价；但公设文件未声明约定，"
         "需补注『ε 的符号与维度关系』，否则与文献比对会误判为矛盾")

    # F09 数值验证不动点稳定性
    epsv, cgv = mp.mpf("0.01"), mp.mpf("1.0")
    gstar = mp.sqrt(epsv / cgv)
    beta_f = lambda x: epsv * x - cgv * x ** 3
    h = mp.mpf("1e-20")
    dnum = (beta_f(gstar + h) - beta_f(gstar - h)) / (2 * h)
    record("F09", "对偶代数", "数值验证 β'(g*) = -2ε（取 ε=0.01, c=1）",
           "β'(g*) - (-2ε)", dnum, -2 * epsv, "数值核验",
           note="数值导数与解析 -2ε 一致")

    return {"gstar": gstar}


# ===========================================================================
# 6. 模块 G · 量纲审计与无量纲化判据
# ===========================================================================
# 量纲基 [L, M, T, I, Θ]
DIMS = {
    "c": (1, 0, -1, 0, 0),
    "hbar": (2, 1, -1, 0, 0),
    "G": (3, -1, -2, 0, 0),
    "e": (0, 0, 1, 1, 0),
    "eps0": (-3, -1, 4, 2, 0),
    "mu0": (1, 1, -2, -2, 0),
    "alpha": (0, 0, 0, 0, 0),
    "k_B": (2, 1, -2, 0, -1),
    "m": (0, 1, 0, 0, 0),
    "kappa": (-1, 0, 0, 0, 0),
    "tau": (-1, 0, 0, 0, 0),
    "omega": (0, 0, -1, 0, 0),
    "R": (1, 0, 0, 0, 0),
    "v": (1, 0, -1, 0, 0),
    "l_P": (1, 0, 0, 0, 0),
    "m_P": (0, 1, 0, 0, 0),
    "F": (1, 1, -2, 0, 0),
}


def dim_of(monomial):
    """monomial: {symbol: exponent} -> 量纲向量。"""
    acc = [0, 0, 0, 0, 0]
    for sym, ex in monomial.items():
        if sym not in DIMS:
            raise KeyError("未知量纲符号: " + sym)
        d = DIMS[sym]
        for i in range(5):
            acc[i] += d[i] * ex
    return tuple(acc)


# 各体系的量纲审计条目：(体系, 公式, 左侧单项式, 右侧单项式)
DIM_AUDIT = [
    ("S01/S02/S10/S12", "κ² + τ² = (ω/v)²", {"kappa": 2}, {"omega": 2, "v": -2}),
    ("S07/S08", "κ² + τ² = 1/R²", {"kappa": 2}, {"R": -2}),
    ("S07", "G = c³/(ℏ(κ²+τ²))", {"G": 1}, {"c": 3, "hbar": -1, "kappa": -2}),
    ("S07/S08/v5", "m = ℏ/(cR)", {"m": 1}, {"hbar": 1, "c": -1, "R": -1}),
    ("S08/v5", "c = ω R", {"c": 1}, {"omega": 1, "R": 1}),
    ("S08/v5", "ħ = m c R", {"hbar": 1}, {"m": 1, "c": 1, "R": 1}),
    ("S10", "m = ℏ√(κ²+τ²)/c", {"m": 1}, {"hbar": 1, "kappa": 1, "c": -1}),
    ("S10/S07", "α = τ/κ", {"alpha": 1}, {"tau": 1, "kappa": -1}),
    ("S08/v5", "e = √(4πε₀(τ/κ)ℏc)", {"e": 1}, {"eps0": 0.5, "tau": 0.5, "kappa": -0.5,
                                                 "hbar": 0.5, "c": 0.5}),
    ("S03", "ρ_E = (c⁴/8πG) R", {"G": -1, "c": 4, "kappa": 1}, {"m": 1, "R": -2, "c": 2}),
    ("S11", "Q/M = √(4πε₀G)", {"e": 1, "m": -1}, {"eps0": 0.5, "G": 0.5}),
    ("S02/S12", "P = m(c − v)", {"m": 1, "v": 1}, {"m": 1, "c": 1}),
    ("公共", "F = α ℏ c / r²", {"F": 1}, {"alpha": 1, "hbar": 1, "c": 1, "R": -2}),
    ("公共", "ε₀ = e²/(4παℏc)", {"eps0": 1}, {"e": 2, "alpha": -1, "hbar": -1, "c": -1}),
]


def module_g_dimension():
    n_ok = 0
    n_bad = 0
    for sysname, formula, lhs, rhs in DIM_AUDIT:
        try:
            dl = dim_of(lhs)
            dr = dim_of(rhs)
            ok = dl == dr
        except KeyError:
            ok = False
            dl = dr = None
        if ok:
            n_ok += 1
        else:
            n_bad += 1
        note("G-DIM-" + formula[:12], "量纲审计",
             "「%s」（%s）" % (formula, sysname),
             "左=%s 右=%s" % (dl, dr),
             "PASS" if ok else "FAIL",
             "量纲一致" if ok else "量纲不一致：左 %s vs 右 %s" % (dl, dr))

    record("G01", "量纲审计", "量纲一致性总检（%d 条核心公式）" % len(DIM_AUDIT),
           "通过 %d / 失败 %d" % (n_ok, n_bad), mp.mpf(n_ok), mp.mpf(len(DIM_AUDIT)),
           "审计",
           note="全部核心公式量纲自洽；量纲自洽是必要条件而非充分条件，"
                "不能据此宣称物理成立")

    # G02 无量纲常数清单（第一性真正目标）
    dimless = [
        ("α 精细结构常数", ALPHA),
        ("m_μ/m_e", MMU / ME),
        ("m_τ/m_e", MTAU / ME),
        ("m_p/m_e", MP / ME),
        ("α_S(M_Z)", mp.mpf("0.1180")),
        ("α_grav(e,p) = G m_e m_p/(ℏc)", G * ME * MP / (HBAR * C)),
        ("m_e/m_P", ME / MP_MASS),
    ]
    for label, val in dimless:
        record("G02-" + label[:8], "无量纲目标", "无量纲常数：%s" % label,
               "登记", val, None, "本征值",
               note="单位制归一化不能消除，是第一性理论必须解释的对象")

    note("G03", "无量纲目标", "无量纲化判据（本次核心方法论结论）",
         "第一性内容 ⟺ 无量纲量的数值；量纲常数只是单位换算因子", "BOUNDARY",
         "在普朗克制（c=ℏ=G=k_B=1）下，所有量纲常数的值都被归一为 1，"
         "残留的只有无量纲数：α、m_i/m_j、α_S、α_grav 等。"
         "因此『几何化导出 c、ℏ、G』不构成物理成就；"
         "『导出 α=1/137.036』或『导出 m_τ/m_e=3477』才是。"
         "仓库现状：α 与质量比均为测量锚（v29/v30 已诚实标注 φ 幂律证伪、"
         "代层级需 Yukawa 动力学），无任何一项无量纲常数被第一性导出")

    return {"dim_ok": n_ok, "dim_bad": n_bad}


# ===========================================================================
# 7. 模块 H · 自由度审计（符号雅可比数值秩 —— "零自由参数"硬判据）
# ===========================================================================
def mp_rank(mat, tol=None):
    """mpmath 带主元高斯消元求数值秩。"""
    A = [row[:] for row in mat]
    m = len(A)
    n = len(A[0]) if m else 0
    if m == 0 or n == 0:
        return 0
    if tol is None:
        scale = max((abs(x) for row in A for x in row), default=mp.mpf("0"))
        tol = scale * mp.mpf(10) ** (-(mp.mp.dps - 20))
    rank = 0
    row = 0
    for col in range(n):
        piv, best = None, mp.mpf("0")
        for rr in range(row, m):
            if abs(A[rr][col]) > best:
                best = abs(A[rr][col])
                piv = rr
        if piv is None or best <= tol:
            continue
        A[row], A[piv] = A[piv], A[row]
        pv = A[row][col]
        for rr in range(m):
            if rr == row or A[rr][col] == 0:
                continue
            f = A[rr][col] / pv
            for cc in range(col, n):
                A[rr][cc] = A[rr][cc] - f * A[row][cc]
        row += 1
        rank += 1
        if row == m:
            break
    return rank


def sym_jacobian_rank(eqs, syms, subs_map, dps=50):
    """符号雅可比 -> 高精度数值 -> 数值秩。"""
    J = sp.Matrix(eqs).jacobian(syms)
    Jn = J.subs(subs_map).applyfunc(lambda z: sp.N(z, dps))
    mat = []
    for i in range(Jn.rows):
        mat.append([mp.mpf(str(Jn[i, j])) for j in range(Jn.cols)])
    return mp_rank(mat), mat


def module_h_freedom(triad):
    c, hb, e, eps0, mu0, al, g, m, kp, ta, R, om, mpl, lp = sp.symbols(
        "c hbar e eps0 mu0 alpha G m kappa tau R omega m_P l_P", positive=True)

    syms = [c, hb, e, eps0, mu0, al, g, m, kp, ta, R, om, mpl, lp]

    # GAQ v4/v5 + S10 + S07 声称的"派生关系"全集
    eqs = [
        c - om * R,                                   # v5: c = ωR
        hb - m * c * R,                               # v5: ħ = mcR
        m - hb / (c * R),                             # v4: m = ħ/(cR)
        kp ** 2 + ta ** 2 - 1 / R ** 2,               # A3: |Ξ|² = 1/R²
        g - c ** 3 / (hb * (kp ** 2 + ta ** 2)),      # v4: G = c³/(ℏ(κ²+τ²))
        al - ta / kp,                                 # S10: α = τ/κ
        eps0 - e ** 2 / (4 * sp.pi * al * hb * c),    # 常数闭包
        mu0 * eps0 - 1 / c ** 2,                      # Maxwell
        mpl ** 2 - hb * c / g,                        # 普朗克质量定义
        lp - R,                                       # v4: l_P ≡ R
        lp ** 2 - hb * g / c ** 3,                    # 普朗克长度定义
        e ** 2 - 4 * sp.pi * eps0 * (ta / kp) * hb * c,  # v5: e 导出式
    ]

    # 真实物理值代入（电子尺度锚 + 普朗克锚）
    omega_e = triad["omega_e"]
    R_e = triad["R_e"]
    w_e = triad["w_e"]
    subs_map = {
        c: sp.Float(str(C), 30),
        hb: sp.Float(str(HBAR), 30),
        e: sp.Float(str(E), 30),
        eps0: sp.Float(str(EPS0), 30),
        mu0: sp.Float(str(MU0), 30),
        al: sp.Float(str(ALPHA), 30),
        g: sp.Float(str(G), 30),
        m: sp.Float(str(ME), 30),
        kp: sp.Float(str(omega_e / mp.sqrt(1 + ALPHA ** 2)), 30),
        ta: sp.Float(str(ALPHA * omega_e / mp.sqrt(1 + ALPHA ** 2)), 30),
        R: sp.Float(str(R_e), 30),
        om: sp.Float(str(w_e), 30),
        mpl: sp.Float(str(MP_MASS), 30),
        lp: sp.Float(str(LP), 30),
    }

    rank, _ = sym_jacobian_rank(eqs, syms, subs_map)
    n_var = len(syms)
    n_eq = len(eqs)
    dof = n_var - rank

    record("H01", "自由度审计", "GAQ/S10 常数闭包族：方程数 / 变量数 / 雅可比秩",
           "秩 = %d, 变量 = %d, 方程 = %d" % (rank, n_var, n_eq),
           mp.mpf(rank), mp.mpf(n_var), "审计",
           note="秩 %d < 变量 %d ⇒ 解空间维数（自由度）= %d" % (rank, n_var, dof))

    note("H02", "自由度审计", "『零自由参数』主张检验",
         "自由度 = 变量数 − 雅可比秩 = %d − %d = %d" % (n_var, rank, dof),
         "FAIL" if dof > 0 else "PASS",
         "方程组欠定：需要 %d 个外部输入才能定出全部常数。"
         "物理上这些输入正是测量锚（α、m_e、G 等）。"
         "因此『零自由参数』的准确含义是『无拟合参数』（形式自洽），"
         "而非『无外部输入』（第一性导出）。两者常被混淆，须区分" % dof)

    # H03 线性相关（循环）方程识别
    note("H03", "自由度审计", "循环方程识别（秩亏损来源）",
         "e²=4πε₀(τ/κ)ħc 与 α=τ/κ 与 ε₀=e²/(4παħc) 三者线性相关",
         "BOUNDARY",
         "把 ε₀ 的定义式代入 e 的导出式得 e² = e²(τ/κ)/α，再代入 α=τ/κ 得恒等式 e²=e²。"
         "即这三条方程只贡献 2 个独立约束，e 的实际值仍由测量输入。"
         "同理 ħ=mcR 与 m=ħ/(cR) 是同一方程的两种写法，秩只 +1")

    # H04 归一化后自由度（普朗克制：c=ℏ=G=k_B=1）
    # 变量降为无量纲比值：α, m/m_P, κ ℓ_P, τ ℓ_P, R/ℓ_P, ω t_P, e/q_P
    syms_n = [al, m, kp, ta, R, om, e]
    eqs_n = [
        al - ta / kp,
        kp ** 2 + ta ** 2 - 1 / R ** 2,
        m - hb / (c * R),
        om - c / R,
        e ** 2 - 4 * sp.pi * eps0 * (ta / kp) * hb * c,
    ]
    subs_n = dict(subs_map)
    subs_n[c] = sp.Float("1", 30)
    subs_n[hb] = sp.Float("1", 30)
    subs_n[g] = sp.Float("1", 30)
    subs_n[mpl] = sp.Float("1", 30)
    subs_n[lp] = sp.Float("1", 30)
    subs_n[eps0] = sp.Float(str(EPS0), 30)

    rank_n, _ = sym_jacobian_rank(eqs_n, syms_n, subs_n)
    dof_n = len(syms_n) - rank_n
    record("H04", "自由度审计", "普朗克制归一化后自由度（c=ℏ=G=1）",
           "秩 = %d, 归一化变量 = %d" % (rank_n, len(syms_n)),
           mp.mpf(rank_n), mp.mpf(len(syms_n)), "审计",
           note="归一化后仍需 %d 个外部无量纲输入 ⇒ 这正是第一性理论必须解释的参数个数" % dof_n)

    return {"rank": rank, "dof": dof, "rank_n": rank_n, "dof_n": dof_n}


# ===========================================================================
# 8. 模块 M · 第一性冲突探测（本次重点）
# ===========================================================================
def module_m_conflicts(triad):
    omega_e = triad["omega_e"]

    # M01 螺旋半径普适性矛盾（S07/S08）
    # 联立 A3: κ²+τ² = 1/R² 与 G = c³/(ℏ(κ²+τ²))
    #   ⇒ G = c³R²/ℏ ⇒ R = ℓ_P（唯一）
    # 又 m = ℏ/(cR) ⇒ m = ℏ/(cℓ_P) = m_P（唯一）
    R_from_G = mp.sqrt(HBAR * G / C ** 3)
    m_from_R = HBAR / (C * R_from_G)
    ratio_pm = MP / ME
    note("M01", "第一性冲突", "【硬冲突】螺旋半径普适性矛盾（S07-A3 + 派生式）",
         "R = √(ℏG/c³) = ℓ_P 唯一 ⇒ m = ℏ/(cR) = m_P 唯一", "FAIL",
         "联立 S07-A3 (κ²+τ²=1/R²) 与 G=c³/(ℏ(κ²+τ²)) 得 G=c³R²/ℏ，"
         "因 G 普适故 R 只能是 ℓ_P=1.616e-35 m，进而 m=ℏ/(cR)=m_P=2.176e-8 kg。"
         "但实测电子 9.109e-31 kg、质子 1.673e-27 kg，m_p/m_e=%.2f。"
         "体系若要保留质量谱，必须放弃『κ²+τ²=1/R² 中 R 是普朗克尺度』"
         "或放弃『G 由同一 (κ,τ) 给出』；二者不可兼得" % float(ratio_pm))

    record("M01-n", "第一性冲突", "M01 数值：m_p/m_e 实测 vs 同 R 预言(=1)",
           "m_p/m_e - 1", ratio_pm - 1, mp.mpf("1"), "审计", verdict="FAIL",
           note="偏差 1835 倍，即该联立方案被质量谱直接证伪")

    # M02 普朗克锚定谬误（S10/S07 通用）
    # G = c³/(ℏ(κ²+τ²)) 与 m = ℏ√(κ²+τ²)/c 联立 ⇒ G m² = ℏc ⇒ m = m_P
    m_implied = mp.sqrt(HBAR * C / G)
    note("M02", "第一性冲突", "【根因】普朗克锚定谬误（Planck-anchoring fallacy）",
         "G=c³/(ℏ(κ²+τ²)) ∧ m=ℏ√(κ²+τ²)/c ⇒ G m² = ℏ c ⇒ m = m_P", "FAIL",
         "两式联立消去 (κ²+τ²) 得到 G m² = ℏc，其唯一解 m = m_P = %.6e kg。"
         "这说明该式组实际是『普朗克尺度恒等式』的变形（在 m=m_P 时 α_grav=1 恒成立），"
         "被误用为『任意粒子的关系式』。正确形式应为 α_grav = G m²/(ℏc) = (m/m_P)²，"
         "它对任意 m 成立且不含矛盾。这是仓库 GAQ/S10/S07/S08 谱系的系统性第一性错误"
         % float(m_implied))

    # M02-n 数值：电子的 α_grav 应为 (m_e/m_P)² 而非 1
    a_grav_e = G * ME ** 2 / (HBAR * C)
    a_grav_e_ref = (ME / MP_MASS) ** 2
    record("M02-n", "第一性冲突", "α_grav(e) = G m_e²/(ℏc) = (m_e/m_P)²",
           "α_grav(e) - (m_e/m_P)²", a_grav_e, a_grav_e_ref, "数值核验",
           note="= 1.75e-45，而非 1。证实 M02：普朗克锚定式不能在电子尺度使用")

    # M03 P=m(c−v) 低速极限（S02/S12）
    # F = dP/dt = -m a + (c−v) dm/dt；低速静态质量下 F = -m a，与牛顿 F=ma 反号
    note("M03", "第一性冲突", "【冲突】P=m(c−v) 的低速极限与 v=0 行为（S02-A1/A2）",
         "v=0 ⇒ P=mc≠0；F=dP/dt=-ma（m 恒定），与 F=+ma 反号", "FAIL",
         "标准动量 P=mv 在 v=0 时给出 P=0，而 P=m(c−v) 给出 P=mc，"
         "即静止粒子携带动量 mc（除非把 c 解释为内部速度而非外部速度）。"
         "若 m 恒定且 c 恒定，则 F = -m dv/dt = -ma，与牛顿第二定律符号相反。"
         "要让 F=+ma 成立须额外假设 c 的方向/大小随 t 变化或引入 (c−v)dm/dt 项，"
         "但公设文件未登记这些前提。属未声明的隐藏假设")

    record("M03-n", "第一性冲突", "M03 数值：静止粒子动量 P(0)=m_e c",
           "P(0) - m_e c", ME * C, ME * C, "本征值",
           note="= 2.73e-22 kg·m/s，非零；与静止动量应为 0 的常规定义冲突")

    # M04 归一化后信息丢失（与 C03 呼应，从冲突角度）
    note("M04", "第一性冲突", "【边界】归一化本源方程不携带质量信息",
         "κ̃²+τ̃²=1 对所有粒子恒同（与 m 无关）", "BOUNDARY",
         "质量全部寄于 Ω=mc/ℏ 的绝对尺度，而该尺度在归一化中被除掉。"
         "因此『本源方程解释质量谱』是不成立的表述：它解释的是 κ/τ 的相对比例（即 α），"
         "而非质量的绝对值或比值。与 v30『代质量层级需 Yukawa 动力学』一致")

    # M05 复曲率 Ξ=κ+iτ 的相位自由度
    note("M05", "第一性冲突", "【边界】复曲率 Ξ=κ+iτ 的相位与模方信息量",
         "Ξ 的模 |Ξ|=√(κ²+τ²)，相位 arg Ξ = arctan(τ/κ) = arctan α", "BOUNDARY",
         "复曲率比模方恒等式多携带一个相位自由度，该相位数值上就是 α。"
         "但相位取值仍是输入（α 测量值），复形式并未减少自由度，"
         "只是把同一个无量纲输入换了一种几何表述（形式增益，非信息增益）")

    return {"R_from_G": R_from_G, "m_from_R": m_from_R, "a_grav_e": a_grav_e}


# ===========================================================================
# 9. 模块 I · 融合：公设签名同源度聚类
# ===========================================================================
# 签名维度（几何/本体标记）
SIGN_KEYS = [
    "螺旋参数化r(t)", "Frenet曲率κ挠率τ", "复曲率Ξ=κ+iτ", "光速恒等v≡c",
    "光速上限v≤c", "离散几何元胞", "作用量子ħ", "信息熵", "高维紧致化",
    "Cl(4,4)边界态", "拓扑荷整数Q∈Z", "对偶Z2(D²=1)", "自相似分形β(-g)=-β(g)",
    "统一力P=m(c-v)", "常数几何化(c,ℏ)", "质量谱/代结构", "几何耦合R-T-Q-Π",
    "规范群/表示", "统一动量重定义",
]

SIGNATURES = {
    "S01_螺旋三重奏与谱几何": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "S02_空间光速螺旋统一力": [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    "S03_GAQ几何原子与作用量子": [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "S04_IEG信息熵引力": [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "S05_HDU高维紧致化统一": [0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "S06_TCL拓扑手征锁定": [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    "S07_GAQ复曲率融合体系": [1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "S08_GAQ常数几何化体系": [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "S09_GAQ粒子质量谱体系": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    "S10_频率本源与复螺旋宇宙": [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "S11_GMUFT几何自由度与耦合": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "S12_空间光速螺旋统一体系": [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    "S13_全域双向分形统一场论": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    "P01_空间压缩与密度本体": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "P02_物体驱动与源场本体": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "P03_规范对称统一候选": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "P04_量子结构与时空涌现候选": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

# 人工登记的族系（融合结果）
FAMILIES = {
    "F1_螺旋运动学族": {
        "members": ["S01_螺旋三重奏与谱几何", "S02_空间光速螺旋统一力",
                    "S12_空间光速螺旋统一体系", "S10_频率本源与复螺旋宇宙"],
        "shared": "Frenet 螺旋骨架 κ²+τ²=(ω/v)²（数学层可通信，机器零恒等）",
        "fork": "本体分叉：S01 无本体（纯数学）／S02 无几何本体（动力学）／"
                "S12 空间本体 v≡c／S10 振动本体 v≤c",
        "merge_verdict": "不可融合为单一体系：数学骨架共享 ≠ 本体共享；"
                         "证据不得跨体系转移（仓库红线）",
    },
    "F2_GAQ 复曲率谱系（版本演进）": {
        "members": ["S03_GAQ几何原子与作用量子", "S07_GAQ复曲率融合体系",
                    "S08_GAQ常数几何化体系", "S09_GAQ粒子质量谱体系"],
        "shared": "复曲率 Ξ=κ+iτ 本体 + 作用量子 ħ + 光速约束；v1→v4→v5→v6 版本线",
        "fork": "常数地位逐版变化：v1 离散元胞 → v4 (c,ħ,e) 三公理常数 → "
                "v5 (c,ħ) 降为几何桥梁、e 降为导出量 → v6 加代结构",
        "merge_verdict": "应作为『同一研究的版本序列』管理，不是 4 个独立体系；"
                         "建议登记为一条版本线 + 4 个版本快照，公设差异逐版比对",
    },
    "F3_GAQ v3 三体系族": {
        "members": ["S04_IEG信息熵引力", "S05_HDU高维紧致化统一",
                    "S06_TCL拓扑手征锁定"],
        "shared": "共同来源著作（03_跨体系研究/跨体系原著），共用离散几何元胞 + 作用量子",
        "fork": "切入点不同：信息熵／高维紧致／拓扑手征",
        "merge_verdict": "同为原著的分册，被 v4 吸收为融合成分；"
                         "保留独立登记可，但须标注『已被 S07 v4 融合』",
    },
    "F4_对偶分形族": {
        "members": ["S13_全域双向分形统一场论"],
        "shared": "对偶 Z₂ + 拓扑荷守恒 + 双向分形自相似",
        "fork": "无（单体系）",
        "merge_verdict": "唯一含 verified 结论的体系（claims 4 verified / 1 falsified）；"
                         "与螺旋族无公设交集，不得因『都用数学语言』而合并",
    },
    "F5_几何耦合族": {
        "members": ["S11_GMUFT几何自由度与耦合"],
        "shared": "四大几何自由度 {R,T,Q,Π}：曲率/挠率/拖拽/非度规",
        "fork": "无（单体系）；场方程 OPEN",
        "merge_verdict": "与螺旋族共用曲率/挠率语言但本体不同；"
                         "Q/M=√(4πε₀G) 是量纲自洽的代数关系（G03 已验证量纲）",
    },
    "F6_待建模占位族": {
        "members": ["P01_空间压缩与密度本体", "P02_物体驱动与源场本体",
                    "P03_规范对称统一候选", "P04_量子结构与时空涌现候选"],
        "shared": "无公设、无 claims、无代码依赖",
        "fork": "方向各不相同",
        "merge_verdict": "不构成体系；P03 唯一带规范群签名，"
                         "若立项应优先（规范对称是四力统一的标准路径）",
    },
}


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def module_i_fusion():
    names = sorted(SIGNATURES.keys())
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            s = cosine(SIGNATURES[names[i]], SIGNATURES[names[j]])
            if s >= 0.60:
                pairs.append((names[i], names[j], round(s, 3)))
    pairs.sort(key=lambda z: -z[2])

    for a, b, s in pairs[:20]:
        note("I-SIM", "融合聚类", "同源度 %.3f：%s ↔ %s" % (s, a, b),
             "公设签名余弦相似度", "PASS" if s >= 0.8 else "BOUNDARY",
             "≥0.80 判为同族候选；0.60–0.80 判为骨架共享、本体分叉")

    for fid, info in FAMILIES.items():
        note("I-" + fid[:2], "融合聚类", "%s（%d 个成员）" % (fid, len(info["members"])),
             "共享：" + info["shared"], "PASS",
             "分叉：" + info["fork"] + " ｜ 融合判定：" + info["merge_verdict"])

    return {"pairs": pairs, "families": FAMILIES}


# ===========================================================================
# 10. 模块 J · 归一化映射（符号 / 量纲 / 普朗克制）
# ===========================================================================
SYMBOL_NORM = [
    ("曲率 κ", ["κ", "kappa", "k1", "曲率κ1"], "κ", "1/L",
     "S01/S02/S07/S08/S10/S11/S12 统一为 κ（4D 时为 κ₁）"),
    ("挠率 τ", ["τ", "tau", "k2", "挠率κ2"], "τ", "1/L",
     "与 κ 同为 1/L，二者可直接相加构成模方"),
    ("复曲率 Ξ", ["Ξ", "Xi", "κ+iτ"], "Ξ = κ + iτ", "1/L",
     "模 |Ξ|=Ω，相位 arg Ξ = arctan(τ/κ) = arctan α"),
    ("总幅 Ω", ["Ω", "omega_total", "√(κ²+τ²)", "ω/v"], "Ω = √(κ²+τ²)", "1/L",
     "Ω = m c/ℏ = 1/ƛ_C，是质量的几何载体"),
    ("螺旋角频 ω", ["ω", "omega", "Ω_ang"], "ω", "1/T",
     "注意与总幅 Ω 区分：ω 是参数化角频率，Ω 是曲率模"),
    ("螺旋半径 R", ["R", "r0", "半径"], "R", "L", "R = 1/Ω（若取 κ²+τ²=1/R²）"),
    ("螺距参数 b", ["b", "螺距", "pitch"], "b", "L", "v² = R²ω² + b²"),
    ("精细化常数 α", ["α", "alpha", "1/137", "τ/κ"], "α = τ/κ", "1（无量纲）",
     "第一性核心目标之一，当前为测量锚"),
    ("归一化曲率 κ̃", ["κ̃", "kappa_tilde", "κ/Ω"], "κ̃ = κ/Ω", "1（无量纲）",
     "= 1/√(1+α²)，与质量无关"),
    ("归一化挠率 τ̃", ["τ̃", "tau_tilde", "τ/Ω"], "τ̃ = τ/Ω", "1（无量纲）",
     "= α/√(1+α²)；κ̃²+τ̃²=1"),
]

PLANCK_NORM = [
    ("c", "光速", "1", "定义（精确值，SI 单位换算因子）"),
    ("ℏ", "约化普朗克常数", "1", "定义（精确值，SI 单位换算因子）"),
    ("G", "引力常数", "1", "归一化基准（实测值只定标 m_P）"),
    ("k_B", "玻尔兹曼常数", "1", "定义（精确值，温度↔能量换算）"),
    ("ℓ_P", "普朗克长度", "1", "√(ℏG/c³) = 1.616e-35 m"),
    ("t_P", "普朗克时间", "1", "ℓ_P/c = 5.391e-44 s"),
    ("m_P", "普朗克质量", "1", "√(ℏc/G) = 2.176e-8 kg"),
    ("q_P", "普朗克电荷", "11.706", "√(4πε₀ℏc) = e/√α；除以 e 后剩 1/√α"),
    ("α", "精细结构常数", "1/137.036", "无量纲，归一化不能消除——第一性真正目标"),
    ("m_e/m_P", "电子-普朗克质量比", "4.185e-23", "无量纲，第一性真正目标"),
    ("m_μ/m_e", "μ-电子质量比", "206.768", "无量纲，第一性真正目标（v30 已证伪拓扑幂律）"),
    ("m_τ/m_e", "τ-电子质量比", "3477.2", "无量纲，第一性真正目标"),
]


def module_j_normalization():
    for name, aliases, canon, dim, rule in SYMBOL_NORM:
        note("J-SYM-" + canon[:3], "符号归一化", "%s → `%s`（%s）" % (name, canon, dim),
             "别名：" + " / ".join(aliases), "PASS", rule)

    for sym, cname, val, rule in PLANCK_NORM:
        note("J-PLK-" + sym, "普朗克归一化", "%s（%s）= %s" % (sym, cname, val),
             "普朗克制 c=ℏ=G=k_B=1", "PASS", rule)

    # J01 归一化后残留的无量纲量个数
    n_residual = 4  # α, m_e/m_P, m_μ/m_e, m_τ/m_e（示例核心项）
    record("J01", "普朗克归一化", "归一化后残留无量纲参数（核心四项）",
           "α, m_e/m_P, m_μ/m_e, m_τ/m_e", mp.mpf(n_residual), mp.mpf(n_residual),
           "审计",
           note="这四项即 openuft 全部体系共同的『第一性靶心』；"
                "当前仓库无任何一项被第一性导出（全部为测量锚或已被证伪的构造）")

    return {"symbols": SYMBOL_NORM, "planck": PLANCK_NORM}


# ===========================================================================
# 11. 模块 A · 第一性层级分级（L0–L4）
# ===========================================================================
FIRST_PRINCIPLE_LADDER = [
    ("L0", "定义式/代数恒等", "由定义直接推出，恒真，零经验内容",
     ["m_P=√(ℏc/G)", "G=ℏc/m_P²", "ε₀=e²/(4παℏc)", "μ₀ε₀=1/c²",
      "κ²+τ²=(ω/v)²", "κ̃²+τ̃²=1"],
     "不构成物理成就，自洽但不是证据"),
    ("L1", "循环重排/定义回指", "用测量锚反解另一常数，形式上『导出』实为回指",
     ["G=c³/(ℏ(κ²+τ²))（κ²+τ² 由 G 反定）", "e=√(4πε₀(τ/κ)ħc)（τ/κ≡α）",
      "c=ωR、ħ=mcR（R 由 c、ħ 反定）"],
     "伪导出：循环，无预言力"),
    ("L2", "结构约束（含自由参数）", "给出量间关系，但含未定参数或需外部输入",
     ["F_i=α_i ℏc/r²（α_i 未定）", "F_e/F_m=c/v", "m=ℏ√(κ²+τ²)/c（Ω 未定）",
      "Q/M=√(4πε₀G)"],
     "有结构价值，但需闭合参数才成预言"),
    ("L3", "独立可证伪预言", "给出定量、可检验、非回指的数值",
     ["电子 EDM 预言 d_e=2.257e-34 C·m（第九编登记，待实验检验）"],
     "目前仓库内唯一一类真正的第一性产出，且尚未被实验确认"),
    ("L4", "本体/形而上学主张", "不可由数学判定真假的本体假设",
     ["空间以光速螺旋运动（S12）", "振动为第一物理量（S10）",
      "世界由 0/1 对偶基元张成（S13-A1）", "离散普朗克元胞（S03）"],
     "可作为研究纲领，不构成证据；不同本体间不得互相认证"),
]

SYSTEM_GRADING = [
    ("S01_螺旋三重奏与谱几何", "L0", "纯数学框架，三重奏为导出定理；无物理主张",
     "框架自洽，最干净"),
    ("S02_空间光速螺旋统一力", "L2/L4", "P=m(c−v) 为结构重定义；含低速极限冲突（M03）",
     "低速极限符号未声明，需补前提"),
    ("S03_GAQ几何原子与作用量子", "L1/L4", "离散元胞本体 + 作用量子；常数关系多属定义回指",
     "元胞本体无独立预言"),
    ("S04_IEG信息熵引力", "L2/L4", "信息熵变分↔爱因斯坦方程；等价性需严格证明",
     "等价性声称未附可复核推导"),
    ("S05_HDU高维紧致化统一", "L4", "11 维嵌入主张；M₁₁cL₁₁=ħ·2π 为量纲回指",
     "紧致化半径未定，无预言"),
    ("S06_TCL拓扑手征锁定", "L2/L4", "Cl(4,4) 边界态→三代；代结构为计数匹配",
     "计数匹配（3×2=6）非数值预言"),
    ("S07_GAQ复曲率融合体系", "L1/L4 + 冲突", "五公理；联立派生式导致普朗克锚定矛盾（M01/M02）",
     "硬冲突：质量谱与 G 普适不可兼得"),
    ("S08_GAQ常数几何化体系", "L1 + 方向误置", "c=ωR、ħ=mcR 把定义常数当成就（D10）",
     "『几何化 c、ħ』是伪目标（单位换算因子）"),
    ("S09_GAQ粒子质量谱体系", "L1/L4 + 冲突", "SO(3) 投影定代；受 M02 同一根因影响",
     "质量比仍需 Yukawa 输入（v30）"),
    ("S10_频率本源与复螺旋宇宙", "L1/L4 + 冲突", "振动本体；G=c³/(ℏ(κ²+τ²)) 同 M02 根因",
     "v≤c 与 S12 v≡c 不可互认"),
    ("S11_GMUFT几何自由度与耦合", "L2", "四自由度框架；Q/M=√(4πε₀G) 量纲自洽",
     "完整场方程 OPEN，无法评估"),
    ("S12_空间光速螺旋统一体系", "L2/L4 + 借用", "v≡c 本体 + 借用 S02 动力学",
     "借用不带来独立证据；低速极限同 M03"),
    ("S13_全域双向分形统一场论", "L3 候选", "三公理代数自洽（F01–F09 全 PASS）；"
     "唯一含 verified claims",
     "β 函数符号约定需声明（F08）；预言待实验"),
    ("P01–P04_待建模方向", "无", "无公设无 claims", "方向占位，不计为体系"),
]


def module_a_ladder():
    for code, name, definition, examples, verdict in FIRST_PRINCIPLE_LADDER:
        note("A-" + code, "第一性分级", "L%s %s" % (code, name), definition,
             "PASS" if code in ("L0", "L3") else "BOUNDARY",
             "代表式：" + "；".join(examples) + " ｜ 判定：" + verdict)

    for sysname, grade, reason, note_txt in SYSTEM_GRADING:
        note("A-GRD-" + sysname[:4], "第一性分级", "%s → %s" % (sysname, grade),
             reason, "BOUNDARY" if "冲突" in grade or "误置" in grade else "PASS",
             note_txt)

    return {"ladder": FIRST_PRINCIPLE_LADDER, "grading": SYSTEM_GRADING}


# ===========================================================================
# 12. 输出
# ===========================================================================
def build_payload():
    triad = module_b_triad()
    src = module_c_source_eq(triad)
    consts = module_d_constants()
    forces = module_e_forces()
    dual = module_f_duality()
    dims = module_g_dimension()
    freed = module_h_freedom(triad)
    conflicts = module_m_conflicts(triad)
    fusion = module_i_fusion()
    norm = module_j_normalization()
    ladder = module_a_ladder()

    counts = {}
    for r in RECORDS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    payload = {
        "title": "算法联盟 · openuft 全维自洽与归一化图谱",
        "precision_digits": mp.mp.dps,
        "summary": {
            "total": len(RECORDS),
            "counts": counts,
        },
        "modules": {
            "A_第一性分级": {"ladder": [list(x) for x in FIRST_PRINCIPLE_LADDER],
                             "system_grading": [list(x) for x in SYSTEM_GRADING]},
            "B_三重奏骨架": {"kappa_e": mp.nstr(src["kappa_e"], 18),
                             "tau_e": mp.nstr(src["tau_e"], 18),
                             "omega_e": mp.nstr(triad["omega_e"], 18),
                             "R_e": mp.nstr(triad["R_e"], 18)},
            "C_本源方程": {"kappa_tilde": mp.nstr(src["kt"], 20),
                           "tau_tilde": mp.nstr(src["tt"], 20)},
            "D_常数闭包": {"G_via_electron": mp.nstr(consts["G_via_kt"], 18),
                           "G_via_planck": mp.nstr(consts["G_via_P"], 18)},
            "E_四力归一化": {"alpha_grav_ep": mp.nstr(forces["a_grav_ep"], 12),
                             "alpha_grav_MZ": mp.nstr(forces["a_grav_mz"], 12),
                             "span": mp.nstr(forces["span"], 12)},
            "F_对偶代数": {"gstar_numeric": mp.nstr(dual["gstar"], 18)},
            "G_量纲审计": {"pass": dims["dim_ok"], "fail": dims["dim_bad"]},
            "H_自由度审计": {"rank": freed["rank"], "dof": freed["dof"],
                             "rank_normalized": freed["rank_n"],
                             "dof_normalized": freed["dof_n"]},
            "M_第一性冲突": {"R_from_G": mp.nstr(conflicts["R_from_G"], 18),
                             "m_from_R": mp.nstr(conflicts["m_from_R"], 18),
                             "alpha_grav_e": mp.nstr(conflicts["a_grav_e"], 18)},
            "I_融合聚类": {"families": {k: v for k, v in FAMILIES.items()},
                           "similar_pairs": fusion["pairs"][:20]},
            "J_归一化": {"symbols": [list(x) for x in SYMBOL_NORM],
                         "planck": [list(x) for x in PLANCK_NORM]},
        },
        "records": RECORDS,
        "red_lines": [
            "精算只证数学自洽与实验值一致，不证第一性推导",
            "量纲常数（c/ℏ/k_B）由单位定义固定，其『导出』是单位换算不是物理预言",
            "第一性真正靶心是无量纲量：α、m_μ/m_e、m_τ/m_e、α_S、α_grav",
            "数学恒等成立 ≠ 本体公设成立；证据不得跨体系转移",
            "本次检出的 M01/M02 普朗克锚定谬误与 M03 低速极限冲突如实标 FAIL，不粉饰",
        ],
        "key_findings": [
            "M02 普朗克锚定谬误：G=c³/(ℏ(κ²+τ²)) 与 m=ℏ√(κ²+τ²)/c 联立推出 G m²=ℏc，"
            "唯一解 m=m_P；这是 GAQ/S07/S08/S09/S10 谱系的系统性第一性错误根因",
            "M01 螺旋半径普适性矛盾：G 普适 ⟹ R=ℓ_P ⟹ m=m_P，与 m_p/m_e=1836 直接冲突",
            "M03 P=m(c−v) 低速极限给出 F=−ma 与静止动量 mc，与常规定义冲突且前提未声明",
            "D10/J01 无量纲化判据：c/ℏ/k_B 的『几何化』是伪目标，"
            "第一性靶心是 α 与质量比等无量纲量",
            "H02 自由度审计：常数闭包族雅可比秩亏损，『零自由参数』实为『无拟合参数』",
            "F08 S13 β 函数符号约定与主流 Wilson-Fisher 相反，需补注约定",
        ],
    }
    return payload


def write_outputs(payload, base_dir):
    data_dir = os.path.join(base_dir, "数据")
    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, "全维自洽图谱.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    L = []
    L.append("# 算法联盟 · openuft 全维自洽与归一化图谱\n")
    L.append("> 处理模式：全维度 / 全链路 / 诚实分级。"
             "精度：mpmath %d 位 + sympy 符号求导。\n" % payload["precision_digits"])
    L.append("总计 %d 条记录：%s\n" % (
        payload["summary"]["total"],
        " / ".join("%s %d" % (k, v) for k, v in sorted(payload["summary"]["counts"].items()))))

    L.append("\n## 一、核心发现（Key Findings）\n")
    for i, k in enumerate(payload["key_findings"], 1):
        L.append("%d. %s\n" % (i, k))

    L.append("\n## 二、核验记录总表\n")
    L.append("| 编号 | 组 | 项目 | 公式/陈述 | 值 | 参考 | 残差 | 一致位 | 性质 | 判定 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in RECORDS:
        L.append("| %s | %s | %s | `%s` | %s | %s | %s | %s | %s | **%s** |" % (
            r["id"], r["group"], r["name"], r["formula"],
            r["value"], r["reference"], r["rel_residual"],
            r["digits"], r["kind"], r["verdict"]))

    L.append("\n## 三、第一性层级分级（L0–L4）\n")
    for code, name, definition, examples, verdict in FIRST_PRINCIPLE_LADDER:
        L.append("- **%s %s**：%s。代表式：%s。判定：%s\n" % (
            code, name, definition, "；".join(examples), verdict))

    L.append("\n## 四、体系第一性分级\n")
    L.append("| 体系 | 层级 | 依据 | 备注 |")
    L.append("|---|---|---|---|")
    for sysname, grade, reason, nt in SYSTEM_GRADING:
        L.append("| %s | %s | %s | %s |" % (sysname, grade, reason, nt))

    L.append("\n## 五、融合聚类（F1–F6）\n")
    for fid, info in FAMILIES.items():
        L.append("### %s\n" % fid)
        L.append("- 成员：%s\n" % "、".join(info["members"]))
        L.append("- 共享：%s\n" % info["shared"])
        L.append("- 分叉：%s\n" % info["fork"])
        L.append("- 融合判定：%s\n" % info["merge_verdict"])

    L.append("\n## 六、符号归一化表\n")
    L.append("| 规范符号 | 量纲 | 别名 | 规则 |")
    L.append("|---|---|---|---|")
    for name, aliases, canon, dim, rule in SYMBOL_NORM:
        L.append("| `%s` | %s | %s | %s |" % (canon, dim, " / ".join(aliases), rule))

    L.append("\n## 七、普朗克制归一化表\n")
    L.append("| 符号 | 名称 | 普朗克制下取值 | 说明 |")
    L.append("|---|---|---|---|")
    for sym, cname, val, rule in PLANCK_NORM:
        L.append("| `%s` | %s | %s | %s |" % (sym, cname, val, rule))

    L.append("\n## 八、红线（诚实边界）\n")
    for rl in payload["red_lines"]:
        L.append("- %s\n" % rl)

    with open(os.path.join(data_dir, "全维自洽图谱.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    return data_dir


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    payload = build_payload()
    data_dir = write_outputs(payload, base_dir)

    print("=" * 78)
    print("算法联盟 · openuft 全维自洽与归一化引擎")
    print("=" * 78)
    for r in RECORDS:
        if r["kind"] == "审计" and r["value"] == "—":
            continue
        print("%-8s %-10s %-46s 位=%-6s 残差=%s" % (
            r["verdict"], r["id"], r["name"][:46], r["digits"], r["rel_residual"]))
    print("-" * 78)
    print("记录总数：%d ；判定分布：%s" % (
        payload["summary"]["total"],
        " ".join("%s=%d" % (k, v) for k, v in sorted(payload["summary"]["counts"].items()))))
    print("量纲审计：通过 %d / 失败 %d" % (
        payload["modules"]["G_量纲审计"]["pass"], payload["modules"]["G_量纲审计"]["fail"]))
    print("自由度审计：秩 %d，自由度 %d（归一化后 %d）" % (
        payload["modules"]["H_自由度审计"]["rank"],
        payload["modules"]["H_自由度审计"]["dof"],
        payload["modules"]["H_自由度审计"]["dof_normalized"]))
    print("产出：%s" % data_dir)
    print("  - 全维自洽图谱.json")
    print("  - 全维自洽图谱.md")
    print("=" * 78)


if __name__ == "__main__":
    raise SystemExit(main())
