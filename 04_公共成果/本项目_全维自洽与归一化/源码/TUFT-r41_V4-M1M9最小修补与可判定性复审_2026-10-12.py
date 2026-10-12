# -*- coding: utf-8 -*-
"""
TUFT-r41：V4 耦合演化场方程组 —— M1–M9 最小修补执行与可判定性复审
================================================================================
来料：《TUFT-V4 完整耦合演化场方程组（适配 ADM-BSSN 数值相对论）》
      正本见 数据/TUFT-V4-EC-ADMBSSN耦合演化场方程组_来料全文_2026-10-12.md
前置：r39 全维审计（条目 43，FAIL 21 / PASS 11 / BOUNDARY 5 / MISMATCH 2 /
      CORRECTED 1 / INFO 3），判定册 §五给出最小修复清单 M1–M9 并声明"不代选"。
本轮：用户裁决 = 走 M1–M9 修补路径。本册【执行修补并对每条修补做机器复判】，
      回答唯一问题：修补后方程组是否达到"可判定"（可数值演化 / 可算 χ² / 可谈 τ≠0）。

判定口径（继承 r39 §〇）：
  1. 只判可判定的定量/结构性论断：量纲齐次性、恒等式自洽、指标合法性、数值对标、
     自由度-约束计数、可实施性。
  2. 凡涉及文献系数（(17)(18) 的 αKΠ 系数与符号、D̃² 共形修正项、EC 约束挠率贡献项）
     一律"不自推"，只判结构性缺失并登记。
  3. 所有"残差为零"均为【相对机器零】（分母取该式特征量），不用绝对残差。
  4. 修补 = 修改来料公设/方程，属"修改公设集"层操作；本册不产生新物理，
     只给出【修补形式 + 机器验证 + 诚实代价】。
================================================================================
"""

import os
import sys
import json
from fractions import Fraction as Fr
from decimal import Decimal, getcontext

getcontext().prec = 60

# ---------------------------------------------------------------- 路径
HERE = os.path.dirname(os.path.abspath(__file__))   # .../源码
BASE = os.path.dirname(HERE)                        # .../本项目_全维自洽与归一化
OUT_DIR = os.path.join(BASE, "数据")
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

# ---------------------------------------------------------------- 结果容器
RESULTS = []
GUARDS = []
KEYNUM = {}
NOT_SELF_DERIVED = []


def R(code, verdict, title, detail=""):
    RESULTS.append({"code": code, "verdict": verdict, "title": title, "detail": detail})


def G(code, ok, title, detail=""):
    GUARDS.append({"code": code, "ok": bool(ok), "title": title, "detail": detail})
    return bool(ok)


def K(name, value, note=""):
    KEYNUM[name] = {"value": str(value), "note": note}


def NSD(item, note):
    NOT_SELF_DERIVED.append({"item": item, "note": note})


# ---------------------------------------------------------------- 精确量纲代数 (M, L, T, Q)
def dim(m=0, l=0, t=0, q=0):
    return (Fr(m), Fr(l), Fr(t), Fr(q))


def dmul(a, b):
    """量纲相乘 = 指数相加。"""
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    """量纲相除 = 指数相减。"""
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    """量纲取幂 = 指数乘标量。"""
    n = Fr(n)
    return tuple(x * n for x in a)


def dadd(*ds):
    """同量纲项的【加法】：各项必须同量纲，返回该量纲；不齐次时返回 None。"""
    if not ds:
        return (Fr(0),) * 4
    base = tuple(ds[0])
    for d in ds[1:]:
        if tuple(d) != base:
            return None
    return base


def dgap(a, b):
    """两量纲之差 a-b（用于判"缺什么"）。"""
    return tuple(x - y for x, y in zip(a, b))


def dstr(d):
    if d is None:
        return "NON-HOMOGENEOUS"
    sym = ("M", "L", "T", "Q")
    out = []
    for s, e in zip(sym, d):
        if e == 0:
            continue
        out.append(s + "^" + str(e))
    return "1" if not out else " ".join(out)

# ---------------------------------------------------------------- 常量（SI / CODATA 2018）
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
C_VAL = Decimal("299792458")            # c    [L T^-1]
HBAR = Decimal("1.054571817e-34")       # hbar [M L^2 T^-1]
G_EXP = Decimal("6.67430e-11")          # G    [M^-1 L^3 T^-2]
G_UNC = Decimal("0.00015e-11")          # CODATA u(G)
G_REL_UNC = G_UNC / G_EXP               # 相对不确定度 ~2.247e-5

# ---------------------------------------------------------------- 量纲常量
D_C = dim(0, 1, -1, 0)        # c
D_HBAR = dim(1, 2, -1, 0)     # hbar
D_G = dim(-1, 3, -2, 0)       # G
D_KAPPA = dim(0, -1, 0, 0)    # kappa, tau
D_OMEGA = dim(0, 0, -1, 0)    # omega
D_RHO = dim(1, -3, 0, 0)      # rho 质量密度
D_LEN = dim(0, 1, 0, 0)       # 长度
D_ONE = dim(0, 0, 0, 0)
D_NABLA = dim(0, -1, 0, 0)    # 协变导数
D_ENERGY_DENS = dim(1, -1, -2, 0)   # T_munu 能量密度
D_TIME = dim(0, 0, 1, 0)


def rel(a, b):
    """相对偏差 |a-b| / max(|a|,|b|,tiny)。"""
    a = Decimal(a)
    b = Decimal(b)
    m = max(abs(a), abs(b))
    if m == 0:
        return Decimal(0)
    return abs(a - b) / m


def gfmt(x, n=25):
    return format(Decimal(x), "." + str(n) + "E")


# ================================================================ Stage 0 守卫
def guards_stage0():
    """量纲工具与常量的自检（本册所有判定的地基）。"""
    # G0-1 dmul 是"指数相加"而非相乘
    G("G0-1", dmul(D_C, D_C) == dim(0, 2, -2, 0),
      "dmul 为指数相加（c*c = L^2 T^-2）", str(dstr(dmul(D_C, D_C))))
    # G0-2 dadd 同量纲返回该量纲（kappa^2 与 (omega/c)^2 同为 L^-2）
    d_omc2 = ddiv(dpow(D_OMEGA, 2), dpow(D_C, 2))
    G("G0-2", dadd(dpow(D_KAPPA, 2), d_omc2) == dim(0, -2, 0, 0),
      "dadd 同量纲返回该量纲", "kappa^2 与 (omega/c)^2 同为 " + dstr(d_omc2))
    # G0-3 dadd 异量纲返回 None（阳性对照）
    G("G0-3", dadd(D_KAPPA, D_OMEGA) is None,
      "dadd 异量纲返回 None（阳性对照）", "kappa(L^-1) + omega(T^-1) 必不齐次")
    # G0-4 已知：[G] = M^-1 L^3 T^-2
    G("G0-4", D_G == dim(-1, 3, -2, 0), "[G] = M^-1 L^3 T^-2", dstr(D_G))
    # G0-5 Planck 长度量纲 = L
    d_lp2 = ddiv(dmul(D_HBAR, D_G), dpow(D_C, 3))
    G("G0-5", dpow(d_lp2, Fr(1, 2)) == dim(0, 1, 0, 0),
      "l_P = sqrt(hbar G / c^3) 量纲 = L", dstr(dpow(d_lp2, Fr(1, 2))))
    # G0-6 能量密度量纲
    G("G0-6", dmul(D_RHO, dpow(D_C, 2)) == D_ENERGY_DENS,
      "rho*c^2 = 能量密度 M L^-1 T^-2", dstr(dmul(D_RHO, dpow(D_C, 2))))
    # G0-7 相对机器零判据：对拍一个已知恒等式
    lhs = C_VAL ** 2
    rhs = C_VAL * C_VAL
    G("G0-7", rel(lhs, rhs) < Decimal("1e-55"),
      "相对机器零判据可用（c^2 对拍）", "rel=" + gfmt(rel(lhs, rhs)))
    # G0-8 阳性对照：故意错一个量级应被抓出
    G("G0-8", not (rel(C_VAL, C_VAL * 10) < Decimal("1e-50")),
      "阳性对照：10 倍差异不被判为机器零", "rel=" + gfmt(rel(C_VAL, C_VAL * 10)))
    # G0-9 G 相对不确定度
    G("G0-9", Decimal("1e-6") < G_REL_UNC < Decimal("1e-4"),
      "CODATA u(G)/G 在 1e-6 ~ 1e-4", gfmt(G_REL_UNC))
    # G0-10 锚点交叉印证 c^4/(8 pi G)
    anchor = (C_VAL ** 4) / (Decimal(8) * PI * G_EXP)
    K("anchor_c4_8piG", anchor, "锚点 c^4/(8 pi G)，与 r18/r19/r22/r27/r39 交叉印证")
    G("G0-10", rel(anchor, Decimal("4.8154538867224223992518906E+42")) < Decimal("1e-20"),
      "锚点 c^4/(8piG) 与库内既有册逐位一致", gfmt(anchor))

# ================================================================ Stage A  M1：修式(4) G_th
def stage_A():
    """M1：G_th = 2 pi c^3 /(hbar sin theta) 量纲缺 L^2 ⇒ 补长度标度 ell^2。"""
    # --- R01 回归 r39 T06/T07：原式的量纲缺口
    d_raw = ddiv(dpow(D_C, 3), D_HBAR)                 # [2 pi c^3 / hbar]
    gap = dgap(D_G, d_raw)                             # 缺什么
    gth_raw = (Decimal(2) * PI * C_VAL ** 3) / HBAR    # sin(theta)=1 取最小
    K("M1_Gth_unpatched", gth_raw, "未修补 G_th 最小值 2 pi c^3/hbar（回归 r39 T06）")
    K("M1_Gth_unpatched_over_Gexp", gth_raw / G_EXP, "未修补 G_th/G_exp（回归 r39 T07）")
    R("R01", "FAIL", "【回归】式(4) 未修补时量纲缺 L^2、数值差 70 量级",
      "[" + dstr(d_raw) + "] 缺口=" + dstr(gap) + "；G_th,min/G_exp=" + gfmt(gth_raw / G_EXP))
    G("G-A1", gap == dim(0, 2, 0, 0), "M1 缺口确为 L^2（与 r39 T06 一致）", dstr(gap))

    # --- R02 修补形式：G_th = 2 pi c^3 ell^2 /(hbar sin theta)
    d_fix = ddiv(dmul(dpow(D_C, 3), dpow(D_LEN, 2)), D_HBAR)
    ok_dim = (d_fix == D_G)
    R("R02", "PASS" if ok_dim else "FAIL", "M1 修补形式量纲闭合：G_th = 2πc³ℓ²/(ħ sinθ)",
      "[" + dstr(d_fix) + "] vs [G]=" + dstr(D_G))
    G("G-A2", ok_dim, "M1 补 ℓ² 后量纲 = [G]", dstr(d_fix))

    # --- R03 候选 ℓ₁：由 G_exp 反解（sinθ=1）
    ell1 = ((G_EXP * HBAR) / (Decimal(2) * PI * C_VAL ** 3)).sqrt()
    gth1 = (Decimal(2) * PI * C_VAL ** 3 * ell1 ** 2) / HBAR
    k1 = rel(gth1, G_EXP)
    K("M1_ell1_m", ell1, "ℓ₁ = sqrt(G hbar /(2π c³))（sinθ=1）")
    K("M1_Gth1_over_Gexp", gth1 / G_EXP, "补 ℓ₁ 后 G_th/G_exp")
    R("R03", "PASS" if k1 < Decimal("1e-50") else "FAIL",
      "M1 候选 ℓ₁：补入后 G_th 与 G_exp 逐位相等",
      "ℓ₁=" + gfmt(ell1) + " m；G_th/G_exp=" + gfmt(gth1 / G_EXP) + "；相对残差=" + gfmt(k1))
    G("G-A3", k1 < Decimal("1e-50"), "ℓ₁ 使 G_th ≡ G_exp（相对机器零）", gfmt(k1))

    # --- R04 ℓ₁ 与普朗克长度的关系
    ell_p = ((HBAR * G_EXP) / (C_VAL ** 3)).sqrt()
    ratio = ell1 / ell_p
    k4 = rel(ratio, Decimal(1) / (Decimal(2) * PI).sqrt())
    K("M1_ell1_over_ellP", ratio, "ℓ₁/ℓ_P")
    K("M1_ellP_m", ell_p, "普朗克长度 ℓ_P")
    R("R04", "PASS" if k4 < Decimal("1e-50") else "FAIL",
      "M1 候选 ℓ₁ 恰为 ℓ_P/√(2π)（非新物理，是 ℓ_P 的 2π 重标度）",
      "ℓ₁/ℓ_P=" + gfmt(ratio) + "；1/√(2π) 对拍相对残差=" + gfmt(k4))
    G("G-A4", k4 < Decimal("1e-50"), "ℓ₁ = ℓ_P/√(2π) 机器零成立", gfmt(k4))

    # --- R05 候选 ℓ₂ = ℓ_P：仍差 2π
    gth2 = (Decimal(2) * PI * C_VAL ** 3 * ell_p ** 2) / HBAR
    k5 = rel(gth2 / G_EXP, Decimal(2) * PI)
    K("M1_Gth_lP_over_Gexp", gth2 / G_EXP, "取 ℓ=ℓ_P 时 G_th/G_exp")
    R("R05", "PASS" if k5 < Decimal("1e-50") else "FAIL",
      "M1 候选 ℓ₂=ℓ_P：比值恰为 2π（相对偏差 84.1%，不可用）",
      "G_th(ℓ_P)/G_exp=" + gfmt(gth2 / G_EXP) + "；与 2π 相对残差=" + gfmt(k5))
    G("G-A5", k5 < Decimal("1e-50"), "ℓ=ℓ_P 时 G_th/G_exp ≡ 2π", gfmt(gth2 / G_EXP))

    # --- R06 【M1 二阶两难 A】：自由常数 vs 循环定标（本册新增）
    #   情形甲：ℓ 为自由常数 ⇒ 外部输入 +1，撞 Ω5；
    #   情形乙：ℓ 由 G_exp 反解 ⇒ G_th ≡ G_exp，χ² ≡ 0 恒成立（不可证伪）。
    chi2_b = ((gth1 - G_EXP) / G_UNC) ** 2
    K("M1_chi2_caseB", chi2_b, "情形乙（ℓ 由 G_exp 定标）的 χ²：恒等于 0")
    R("R06", "FAIL", "【M1 二阶两难 A（本册新增）】补 ℓ 后必落入二者之一："
      "甲=ℓ 为自由常数（外部输入 +1，撞 Ω5）；乙=ℓ 由 G_exp 反解（G_th≡G_exp，χ²≡0 不可证伪）",
      "情形乙 χ²=" + gfmt(chi2_b) + " ⇒ 预测力为零；情形甲需登记 ℓ 为 [C] 级外部输入")
    G("G-A6", chi2_b < Decimal("1e-40"), "情形乙 χ² 恒等于 0（信息量为零）", gfmt(chi2_b))

    # --- R07 修补后任务 A 的可执行性
    R("R07", "BOUNDARY", "修补 M1 后任务 A【可执行但无信息】或【有信息但撞 Ω5】，二者不得混淆",
      "χ² 仅在情形甲（ℓ 带先验）下有判别力；此时 G_th 的「第一性导出」自评失效（见 R08）")

    # --- R08 诚实代价：自评必须改写
    R("R08", "CORRECTED", "M1 后第五部分自评第 3 条须改写：G_th 由 {c,ħ,θ} ⇒ 由 {c,ħ,θ,ℓ} 导出",
      "原文「G_th 由螺旋升角、c、ħ 第一性导出」在修完后不再成立，不得沿用旧措辞")

    # --- R09 M1 与 M2-a 的耦合后果：sinθ 若为场 ⇒ G_th 非常数；量化缓解条件
    rows = []
    for q in ["1e-4", "1e-3", "1e-2", "1e-1", "1"]:
        qq = Decimal(q)
        s = Decimal(1) / (Decimal(1) + qq * qq).sqrt()      # sin(theta)
        # d ln(sinθ) = -q^2/(1+q^2) d ln q  ⇒ |Δq/q| <= (u_G/G)(1+q^2)/q^2
        allow = G_REL_UNC * (Decimal(1) + qq * qq) / (qq * qq)
        rows.append({"q_tau_over_kappa": q, "sin_theta": gfmt(s),
                     "allow_dq_over_q": gfmt(allow),
                     "sin_theta_dev_from_1": gfmt(Decimal(1) - s)})
    K("M1_G_variation_table", rows, "sinθ 变化对 G_th 的约束（q=τ/κ）")
    R("R09", "INFO", "M1×M2-a 耦合：sinθ 为场时 G_th 非常数；约束 |ΔG/G|<u_G 反推 τ/κ 的可变范围",
      "q=1e-4 ⇒ τ/κ 可相对变动 " + rows[0]["allow_dq_over_q"][:12] +
      "；q=1e-3 ⇒ " + rows[1]["allow_dq_over_q"][:12] +
      "；q=1 ⇒ 仅 " + rows[4]["allow_dq_over_q"][:12] + " ⇒ 弱挠率下两难被缓解")
    G("G-A7", all(Decimal(r["allow_dq_over_q"]) > 0 for r in rows),
      "G 变化约束表全部为正（判据有效）", "5 点")

# ================================================================ Stage B  M2：解 τ≡0
def stage_B():
    """M2：修式(3)。先回归 τ≡0 定理，再升级根因，再判定三条修法分支。"""
    two_pi = Decimal(2) * PI
    # --- R10 回归 r39 T05：(1)(2)(3) 两分支相等 ⇒ sinθ=1 ⇒ τ≡0
    dev_max = Decimal(0)
    rows10 = []
    for s in ["0.1", "0.3", "0.5", "0.9", "0.999", "1"]:
        st = Decimal(s)
        # 取 κ=sinθ, τ=cosθ, ω=c ⇒ (1)(2) 自动满足（κ²+τ²=1=ω²/c²）
        ct = (Decimal(1) - st * st).sqrt()
        kap = st
        tau = ct
        om = C_VAL                                    # ω = c ⇒ κ²+τ² = 1 = ω²/c²
        m_a = HBAR * st * (kap * kap + tau * tau).sqrt() / (two_pi * C_VAL)
        m_b = HBAR * om / (two_pi * C_VAL * C_VAL)
        d = rel(m_a / m_b, st)
        dev_max = max(dev_max, d)
        rows10.append({"sin_theta": s, "m_a_over_m_b": gfmt(m_a / m_b), "dev": gfmt(d)})
    K("M2_T05_regression", rows10, "τ≡0 定理回归（m_a/m_b 恒等于 sinθ）")
    R("R10", "FAIL", "【回归 r39 T05】未修补时 (1)(2)(3) 强制 sinθ=1 ⇒ τ≡0",
      "6 点上 m_a/m_b 与 sinθ 的最大相对偏差=" + gfmt(dev_max))
    G("G-B1", dev_max < Decimal("1e-55"), "τ≡0 定理回归成立（相对机器零）", gfmt(dev_max))

    # --- R11【根因升级，本册新增】分支 a 恒等于 ħκ/(2πc)
    dev11 = Decimal(0)
    rows11 = []
    grid = [("1", "1"), ("1", "0.1"), ("1", "0.001"), ("3", "4"),
            ("1e-6", "1e-9"), ("2.5", "7.5")]
    for ks, ts in grid:
        kap = Decimal(ks)
        tau = Decimal(ts)
        amp = (kap * kap + tau * tau).sqrt()
        st = kap / amp                                # sinθ = κ/√(κ²+τ²)（由(2)反解）
        lhs = st * amp                                # sinθ·√(κ²+τ²)
        d1 = rel(lhs, kap)
        m_a = HBAR * st * amp / (two_pi * C_VAL)
        m_kap = HBAR * kap / (two_pi * C_VAL)
        d2 = rel(m_a, m_kap)
        dev11 = max(dev11, d1, d2)
        rows11.append({"kappa": ks, "tau": ts, "sin_theta": gfmt(st),
                       "dev_sin_amp_eq_kappa": gfmt(d1), "dev_m_a_eq_hbar_kappa": gfmt(d2)})
    K("M2_root_cause", rows11, "根因：sinθ·√(κ²+τ²) ≡ κ ⇒ 分支 a ≡ ħκ/(2πc)")
    R("R11", "PASS", "【根因升级·本册新增】式(3) 分支 a 在 (1)(2) 下恒等于 ħκ/(2πc)",
      "6 组 (κ,τ) 上 sinθ·√(κ²+τ²)=κ 与 m_a=ħκ/(2πc) 的最大相对偏差=" + gfmt(dev11))
    G("G-B2", dev11 < Decimal("1e-50"), "根因恒等式机器零成立", gfmt(dev11))

    # --- R12 实质冲突的重述
    R("R12", "INFO", "式(3) 的实质冲突 = 「m ∝ κ」与「m ∝ √(κ²+τ²)」互斥（差因子 sinθ=κ/√(κ²+τ²)）",
      "分支 a=ħκ/(2πc)；分支 b=ħω/(2πc²)=ħ√(κ²+τ²)/(2πc) ⇒ 二者相等 ⟺ τ=0")

    # --- R13 第一层修补（删 (3) 的一个分支）：τ 可以 ≠0
    rows13 = []
    ok13 = True
    for ks, ct in [("1", "1.7320508075688772935274463415058723669"),   # cotθ=√3, θ=π/6
                   ("1", "1"),                                          # cotθ=1, θ=π/4
                   ("1", "0.5773502691896257645091487805019574556")]:   # cotθ=1/√3, θ=π/3
        kap = Decimal(ks)
        tau = kap * Decimal(ct)
        amp = (kap * kap + tau * tau).sqrt()
        om = C_VAL * amp                              # (1)
        m_b = HBAR * om / (two_pi * C_VAL * C_VAL)
        # 校验 (1) 与 (2) 的自洽性（此时 (3) 只剩一个分支，无矛盾）
        d1 = rel(amp * amp, (om / C_VAL) ** 2)        # (1)
        d2 = rel(tau, kap * Decimal(ct))              # (2)
        ok13 = ok13 and d1 < Decimal("1e-50") and d2 < Decimal("1e-50") and tau != 0
        rows13.append({"cot_theta": ct[:8], "kappa": ks, "tau": gfmt(tau),
                       "m_over_hbar": gfmt(m_b / HBAR), "dev_eq1": gfmt(d1), "dev_eq2": gfmt(d2)})
    K("M2_layer1_table", rows13, "删 (3) 一个分支后 τ≠0 的自洽解")
    R("R13", "PASS", "M2 第一层：删去 (3) 的一个分支后 τ≠0 不再被排除",
      "3 组 (θ=π/6,π/4,π/3) 上 (1)(2) 自洽且 τ≠0；最大相对偏差 < 1e-50")
    G("G-B3", ok13, "第一层修补后 τ≠0 可行且 (1)(2) 自洽", "3 组")

    # --- R14 第二层障碍：θ 常数 ⇒ τ/κ 恒定 ⇒ τ 仍非独立自由度（回归 T35）
    R("R14", "FAIL", "【第二层·回归 r39 T35】θ 为常数 ⇒ τ/κ=cotθ 全域恒定 ⇒ τ 仍是被奴役量",
      "仅删 (3) 分支不足以得到「双动力学自由度」；τ 完全由 κ 决定")

    # --- R15【M2 二阶两难 B（本册新增）】θ 降为场 ⇒ G_th 非常数，并给出量化上限
    #    θ(x)=arctan(κ/τ) ⇒ sinθ=κ/√(κ²+τ²) ⇒ (M1 修补后) G_th(x)=2πc³ℓ²√(κ²+τ²)/(ħκ)
    #    取 ℓ 使 τ=0 时 G_th=G_exp ⇒ G_th(x)=G_exp·√(1+q²)，q=τ/κ
    #    要求 |ΔG/G| = √(1+q²)-1 < u_G ⇒ q < sqrt((1+u_G)²-1)
    u = G_REL_UNC
    q_max = ((Decimal(1) + u) ** 2 - Decimal(1)).sqrt()
    K("M2_q_max", q_max, "由 G 常数性反推的 τ/κ 上限 = sqrt((1+u_G)²-1)")
    K("M2_q2_over_2_at_qmax", (q_max * q_max) / Decimal(2), "该上限处挠率的相对效应量级 q²/2")
    rows15 = []
    for q in ["1e-4", "1e-3", "6.7e-3", "1e-1", "1"]:
        qq = Decimal(q)
        dg = (Decimal(1) + qq * qq).sqrt() - Decimal(1)
        rows15.append({"q": q, "dG_over_G": gfmt(dg), "within_uG": str(dg < u)})
    K("M2_G_variation", rows15, "θ 为场时 G_th 的相对偏离")
    R("R15", "FAIL", "【M2 二阶两难 B（本册新增）】θ 常数 ⇒ τ 非独立；θ 为场 ⇒ G_th 非常数；"
      "且 G 常数性反推 τ/κ ≤ " + gfmt(q_max),
      "q=τ/κ 上限=" + gfmt(q_max) + "（由 u_G/G=" + gfmt(u) + "）；"
      "挠率相对效应上限 q²/2=" + gfmt((q_max * q_max) / Decimal(2)) + " 恰等于 G 的测量不确定度")
    G("G-B4", q_max > 0 and (q_max * q_max) / Decimal(2) < u * Decimal(2),
      "τ/κ 上限与 u_G 自洽", "q_max=" + gfmt(q_max))

    # --- R16 唯一同时保住 {τ 独立, G_th 常数} 的分支 = 弃 (2)（M2-c）
    R("R16", "BOUNDARY", "M2-c（弃式(2)）：唯一同时保住 τ 独立与 G_th 为常数的分支",
      "代价：(i) 式(3) 的 sinθ 失去来源（θ 不再由 τ/κ 定义）；"
      "(ii) τ 与 κ 的几何绑定关系丢失，须给新关系 ⇒ 不自推（见 §六）")

    # --- R17 三条分支代价矩阵
    matrix = [
        {"branch": "M2-a 删分支 b（m=ħκ/2πc）", "tau_nonzero": "是", "tau_independent": "否（θ 常数）",
         "Gth_constant": "是", "cost": "m 与 τ 无关，挠率不影响质量"},
        {"branch": "M2-b 删分支 a（m=ħω/2πc²）", "tau_nonzero": "是", "tau_independent": "否（θ 常数）",
         "Gth_constant": "是", "cost": "同上，且 (4) 的 sinθ 仍须外部给定"},
        {"branch": "M2-c 弃式(2)", "tau_nonzero": "是", "tau_independent": "是",
         "Gth_constant": "是", "cost": "θ 与 sinθ 无定义来源；τ-κ 几何绑定丢失"},
        {"branch": "M2-d θ 降为场", "tau_nonzero": "是", "tau_independent": "是",
         "Gth_constant": "否", "cost": "G_th(x) 非常数，被 u_G 压到 τ/κ≤" + gfmt(q_max)[:8]},
    ]
    K("M2_branch_matrix", matrix, "M2 四条分支的代价矩阵")
    R("R17", "INFO", "M2 四条分支代价矩阵（不代选）", "见 KEYNUM.M2_branch_matrix")

    # --- R18 结论：M2 单独不能达成"双动力学自由度"自评
    R("R18", "FAIL", "M2 修补后：第五部分自评第 2 条「κ、τ 双动力学自由度」"
      "只在 M2-c（弃式(2)）下成立，且该分支引入新的未定义项",
      "M2-a/b 得到的是「κ 单一自由度 + 被奴役的 τ」；M2-d 得到「独立 τ + 非常数 G」")

# ================================================================ Stage C  M3/M4：式(8)(9) 势与能动张量
def stage_C():
    """M3：式(8) 前因子 ħ/2c → ħc，且 V → V/c⁴；M4：ω 独立演化（否则 V≡0）。"""
    # --- R20 式(9) 自身齐次性
    d_br = dadd(dmul(dpow(D_C, 2), dpow(D_KAPPA, 2)), dpow(D_OMEGA, 2))   # c²κ² 与 ω²
    d_v = dpow(d_br, 2) if d_br is not None else None
    ok20 = (d_br is not None)
    R("R20", "PASS" if ok20 else "FAIL", "式(9) 括号内齐次（c²κ² 与 ω² 同为 T⁻²）",
      "括号内=" + dstr(d_br) + "；[V]=" + dstr(d_v))
    G("G-C1", ok20 and d_v == dim(0, 0, -4, 0), "式(9) [V]=T⁻⁴", dstr(d_v))

    # --- R21 回归 r39 T17：ω 由 (1) 代数更新 ⇒ V≡0
    dev21 = Decimal(0)
    rows21 = []
    for ks, ts in [("1", "1"), ("1", "0.1"), ("1e3", "1e-2"), ("7", "3")]:
        kap = Decimal(ks)
        tau = Decimal(ts)
        om = C_VAL * (kap * kap + tau * tau).sqrt()          # ω = c√(κ²+τ²)，即 (1)
        br = (C_VAL ** 2) * (kap * kap + tau * tau) - om * om
        v = br * br / Decimal(2)
        scale = ((C_VAL ** 2) * (kap * kap + tau * tau)) ** 2
        d = rel(v, Decimal(0)) if scale == 0 else abs(v) / scale
        dev21 = max(dev21, d)
        rows21.append({"kappa": ks, "tau": ts, "V_over_scale": gfmt(d)})
    K("M4_V_zero_regression", rows21, "ω 由 (1) 绑定时 V/特征量（回归 r39 T17）")
    R("R21", "FAIL", "【回归 r39 T17】ω 由 (1) 代数更新 ⇒ V≡0（约束阻尼为空操作）",
      "4 组 (κ,τ) 上 |V|/(c²(κ²+τ²))² 最大值=" + gfmt(dev21))
    G("G-C2", dev21 < Decimal("1e-50"), "V≡0 回归成立（相对机器零）", gfmt(dev21))

    # --- R22 M4：ω 独立演化 ⇒ V≠0（M4 的有效性判据）
    rows22 = []
    ok22 = True
    for f in ["1.01", "1.1", "2"]:
        kap = Decimal("1")
        tau = Decimal("1")
        amp2 = kap * kap + tau * tau
        om = C_VAL * amp2.sqrt() * Decimal(f)                 # 偏离 (1) 因子 f
        br = (C_VAL ** 2) * amp2 - om * om
        v = br * br / Decimal(2)
        scale = ((C_VAL ** 2) * amp2) ** 2
        frac = v / scale
        ok22 = ok22 and frac > Decimal("1e-6")
        rows22.append({"omega_factor": f, "V_over_scale": gfmt(frac)})
    K("M4_V_nonzero", rows22, "M4（ω 独立）后 V 的相对量")
    R("R22", "PASS" if ok22 else "FAIL", "M4（ω 独立演化）⇒ V≠0，势项恢复作用",
      "ω 偏离 (1) 因子 1.01/1.1/2 时 |V|/(c²(κ²+τ²))²=" +
      " / ".join(r["V_over_scale"][:9] for r in rows22))
    G("G-C3", ok22, "M4 使 V 非零（势项复活）", "3 点")

    # --- R23 式(8) 前因子：ħ/c vs ħc
    d_grad2 = dmul(dpow(D_NABLA, 1), D_KAPPA)
    d_grad2 = dmul(d_grad2, d_grad2)                          # (∇κ)(∇κ) = L^-4
    d_pre_old = ddiv(D_HBAR, D_C)                             # ħ/c
    d_pre_new = dmul(D_HBAR, D_C)                             # ħc
    d_term_old = dmul(d_pre_old, d_grad2)
    d_term_new = dmul(d_pre_new, d_grad2)
    ok23 = (d_term_new == D_ENERGY_DENS) and (d_term_old != D_ENERGY_DENS)
    K("M3_prefactor_old", d_term_old, "ħ/c × 梯度项 ⇒ 质量密度（缺 c²）")
    K("M3_prefactor_new", d_term_new, "ħc × 梯度项 ⇒ 能量密度 ✓")
    R("R23", "PASS" if ok23 else "FAIL", "M3 之一：式(8) 前因子 ħ/2c 应为 ħc（梯度项为质量密度 ⇒ 缺 c²）",
      "ħ/c 给 " + dstr(d_term_old) + "（质量密度）；ħc 给 " + dstr(d_term_new) + "（能量密度）")
    G("G-C4", ok23, "ħc 前因子使式(8) 达能量量纲", dstr(d_term_new))

    # --- R24 花括号内两项：∇κ∇κ (L^-4) vs V (T^-4) ⇒ 差 c⁴；修 V→V/c⁴
    d_vc4 = ddiv(d_v, dpow(D_C, 4))
    ok24 = (d_vc4 == d_grad2)
    K("M3_V_over_c4", d_vc4, "V/c⁴ 的量纲")
    R("R24", "PASS" if ok24 else "FAIL", "M3 之二：式(8) 势项应写 V/c⁴（与梯度项相差 c⁴）",
      "[V]=" + dstr(d_v) + "；[V/c⁴]=" + dstr(d_vc4) + "；[∇κ∇κ]=" + dstr(d_grad2))
    G("G-C5", ok24, "V/c⁴ 与梯度项同量纲（L⁻⁴）", dstr(d_vc4))

    # --- R25 修补后式(8) 整体齐次
    d_brace = dadd(d_grad2, d_vc4)
    d_full = dmul(d_pre_new, d_brace) if d_brace is not None else None
    ok25 = (d_full == D_ENERGY_DENS)
    R("R25", "PASS" if ok25 else "FAIL", "M3 修补后式(8) 整体齐次 = 能量密度",
      "[T_spiral]=" + dstr(d_full) + " 与 [T_munu] 一致")
    G("G-C6", ok25, "式(8) 修补后整体齐次", dstr(d_full))

    # --- R26 M3/M4 的连带后果：(10)(11) 的 ∂V/∂κ 须同步改写
    d_dv_dk = ddiv(d_v, D_KAPPA)                              # ∂V/∂κ
    d_dvc4_dk = ddiv(d_vc4, D_KAPPA)                          # ∂(V/c⁴)/∂κ
    K("M3_dV_dkappa", d_dv_dk, "∂V/∂κ 的量纲")
    K("M3_dVc4_dkappa", d_dvc4_dk, "∂(V/c⁴)/∂κ 的量纲")
    R("R26", "INFO", "M3 的连带：式(10)(11) 右端须同步改为 ∂(V/c⁴)/∂κ、∂(V/c⁴)/∂τ",
      "[∂V/∂κ]=" + dstr(d_dv_dk) + "；[∂(V/c⁴)/∂κ]=" + dstr(d_dvc4_dk) + "（后者与 [□κ] 匹配）")

# ================================================================ Stage D  M5 + 式(10)(11)
def stage_D():
    """M5：源项量纲重标；并判定式(11) 冗余能否被修补解除。"""
    two_pi = Decimal(2) * PI
    # --- R30 回归 r39 T18：□κ 与 ∂V/∂κ 差 c⁴
    d_box = dim(0, -2, 0, 0)                                  # □
    d_boxk = dmul(d_box, D_KAPPA)                             # □κ = L^-3
    d_v = dim(0, 0, -4, 0)                                    # [V]
    d_dv_dk = ddiv(d_v, D_KAPPA)                              # ∂V/∂κ = L T^-4
    gap30 = dgap(d_boxk, d_dv_dk)
    R("R30", "FAIL", "【回归 r39 T18】[□κ]=L⁻³ 与 [∂V/∂κ]=LT⁻⁴ 差 c⁴",
      "缺口=" + dstr(gap30))
    G("G-D1", gap30 == dim(0, -4, 4, 0), "缺口确为 c⁻⁴（即 ∂V/∂κ 须除 c⁴）", dstr(gap30))

    # --- R31 修：□κ = ∂(V/c⁴)/∂κ ⇒ 齐次
    d_dvc4_dk = ddiv(ddiv(d_v, dpow(D_C, 4)), D_KAPPA)
    ok31 = (d_dvc4_dk == d_boxk)
    R("R31", "PASS" if ok31 else "FAIL", "M3/M5 联立修补：□κ = ∂(V/c⁴)/∂κ + S 齐次",
      "[∂(V/c⁴)/∂κ]=" + dstr(d_dvc4_dk) + " = [□κ]=" + dstr(d_boxk))
    G("G-D2", ok31, "∂(V/c⁴)/∂κ 与 □κ 同量纲", dstr(d_dvc4_dk))

    # --- R32 回归 r39 T19：源项差一个长度幂次（独立缺陷，与 c 无关）
    d_s = ddiv(dmul(D_G, D_RHO), dpow(D_C, 2))                # 4πGρ/c²
    gap32 = dgap(d_boxk, d_s)
    # dgap(□κ, S) = L^-3 / L^-2 = L^-1 ⇒ 源项比左端【多】一个长度幂次（须除长度或乘 L^-1 量纲的量）
    R("R32", "FAIL", "【回归 r39 T19】源项 [4πGρ/c²]=L⁻² 比 [□κ]=L⁻³ 多一个长度幂次（与 c 无关）",
      "□κ/S_κ=" + dstr(gap32) + " ⇒ 源项须除一个长度（或乘 κ 等 L⁻¹ 量纲量）；"
      "独立缺陷，不能靠补 c 的幂次解决")
    G("G-D3", gap32 == dim(0, -1, 0, 0), "源项比左端多一个 L（非 c 的幂次）", dstr(gap32))

    # --- R33 M5 修补候选（只给量纲可行类，具体形式不自推）
    d_a = dmul(d_s, D_KAPPA)                                  # S ∝ Gρκ/c²
    d_b = ddiv(d_s, D_LEN)                                    # S ∝ Gρ/(c²ℓ_s)
    ok33 = (d_a == d_boxk) and (d_b == d_boxk)
    K("M5_candidate_a", d_a, "候选甲：S_κ ∝ 4πGρκ/c²（无需新常数）")
    K("M5_candidate_b", d_b, "候选乙：S_κ ∝ 4πGρ/(c²ℓ_s)（需新长度 ℓ_s）")
    R("R33", "BOUNDARY", "M5 修补：两条量纲可行路径，代价互斥（不自推选哪条）",
      "甲=S∝Gρκ/c²（量纲 " + dstr(d_a) + "，零新常数但源项 ∝κ 使方程在 κ=0 处退化）；"
      "乙=S∝Gρ/(c²ℓ_s)（量纲 " + dstr(d_b) + "，需再引入 1 个长度 ⇒ 外部输入 +1）")
    G("G-D4", ok33, "两条候选均达 L⁻³", dstr(d_a) + " / " + dstr(d_b))

    # --- R34【本册新增定理】源项比值恒为 cotθ ⇒ 源项永远不解除 (11) 的冗余
    dev34 = Decimal(0)
    for cs in ["0.2", "0.5", "1", "2", "5"]:
        ct = Decimal(cs)
        st = Decimal(1) / (Decimal(1) + ct * ct).sqrt()
        cth = ct / (Decimal(1) + ct * ct).sqrt()
        sk = Decimal(4) * PI * G_EXP * st
        stau = Decimal(4) * PI * G_EXP * cth
        dev34 = max(dev34, rel(stau / sk, ct))
    K("M5_source_ratio", dev34, "S_τ/S_κ 与 cotθ 的最大相对偏差")
    R("R34", "FAIL", "【本册新增】式(12) 使 S_τ/S_κ ≡ cotθ（与 (1)(2) 无关）⇒ 源项永远不解除 (11) 的冗余",
      "5 个 θ 上 S_τ/S_κ 与 cotθ 的最大相对偏差=" + gfmt(dev34))
    G("G-D5", dev34 < Decimal("1e-50"), "源项比值恒等于 cotθ", gfmt(dev34))

    # --- R35【本册新增定理】(11) 冗余的解除 = 两个独立条件的合取
    #    冗余残差 = [(τ/κ) − cotθ] · ∂(V/c⁴)/∂κ
    kap = Decimal("1")
    tau = Decimal("0.5")
    amp2 = kap * kap + tau * tau
    rows35 = []
    for tag, f, cot_theta in [("来料原样(1)+(2)", "1.0", "0.5"),
                              ("仅 M4(ω独立)", "1.1", "0.5"),
                              ("仅 M2-c(弃(2))", "1.0", "1.0"),
                              ("M4+M2-c 联合", "1.1", "1.0")]:
        om = C_VAL * amp2.sqrt() * Decimal(f)
        br = (C_VAL ** 2) * amp2 - om * om                    # 括号
        dvdk = Decimal(2) * (C_VAL ** 2) * kap * br / (C_VAL ** 4)   # ∂(V/c⁴)/∂κ
        resid = ((tau / kap) - Decimal(cot_theta)) * dvdk
        scale = abs(Decimal(2) * (C_VAL ** 2) * kap * (C_VAL ** 2) * amp2 / (C_VAL ** 4))
        rows35.append({"case": tag, "omega_factor": f, "cot_theta": cot_theta,
                       "dVc4_dkappa": gfmt(dvdk),
                       "redundancy_residual_over_scale": gfmt(abs(resid) / scale)})
    K("M5_redundancy_table", rows35, "(11)−cotθ·(10) 的冗余残差（相对特征量）")
    r35_ok = Decimal(rows35[3]["redundancy_residual_over_scale"]) > Decimal("1e-6")
    R("R35", "PASS" if r35_ok else "FAIL",
      "【本册新增定理】式(11) 冗余的解除需要【M4 ∧ M2-c】两个条件同时成立",
      "残差 = (τ/κ − cotθ)·∂(V/c⁴)/∂κ：仅 M4 时第一因子为 0；仅 M2-c 时第二因子为 0（V≡0）；"
      "联合后相对残差=" + rows35[3]["redundancy_residual_over_scale"][:10])
    G("G-D6", r35_ok, "M4 ∧ M2-c 联合后方解除冗余", rows35[3]["redundancy_residual_over_scale"][:12])

    # --- R36 修补后 (10)(11) 的形式登记
    R("R36", "INFO", "修补后 (10)(11) 的形式：□κ=∂(V/c⁴)/∂κ+S_κ，□τ=∂(V/c⁴)/∂τ+S_τ（S 按 R33 重标）",
      "且 (1) 不再作为恒等式强制（改为 C_ω 动力学约束），否则 V≡0 使两式退化为同一式")

# ================================================================ Stage E  M6：式(17)(18)
def stage_E():
    """M6：修式(17)(18) 的 c 幂次、源/势项同 (10) 同源、共形因子与 αKΠ 项。"""
    D_PI_K = dim(0, -1, -1, 0)        # [Π_κ] = L^-1 T^-1
    D_LHS = dmul(D_PI_K, dim(0, 0, -1, 0))   # [∂_t Π_κ] = L^-1 T^-2
    D_BETA = dim(0, 1, -1, 0)

    # --- R40 回归 r39 T27：五项量纲
    t1 = dmul(dmul(D_BETA, dim(0, -1, 0)), D_PI_K)            # β^k ∂_k Π_κ
    t2 = dmul(dmul(dim(0, -1, 0), dim(0, -1, 0)), D_KAPPA)    # α D̃^i D̃_i κ
    t3_a = dmul(dim(0, -1, 0), dmul(dim(0, -1, 0), D_KAPPA))  # (∂_k α)(D̃^k κ)，α 无量纲
    t3_b = dmul(dim(0, 0, 0), dmul(dim(0, -1, 0), D_KAPPA))   # 若 [α]=L ⇒ ∂_kα 无量纲
    t4 = ddiv(dim(0, 0, -4, 0), D_KAPPA)                      # α ∂V/∂κ
    t5 = ddiv(dmul(D_G, D_RHO), dpow(D_C, 2))                 # α S_κ（用正确 G）
    terms = {"β∂Π": dstr(t1), "αD̃²κ": dstr(t2), "∂_kα D̃κ(α=1)": dstr(t3_a),
             "∂_kα D̃κ([α]=L)": dstr(t3_b), "α∂V/∂κ": dstr(t4), "αS_κ": dstr(t5)}
    K("M6_terms_dims", terms, "式(17) 六项量纲（含 α 两种口径）")
    # 互异量纲数依赖两个口径：[α] 是否无量纲、G 是否已按 M1 修补（未修补时 αS_κ=L^-4 ⇒ 5 个互异）
    uniq = set([t1, t2, t3_a, t4, t5])
    n_mis = sum(1 for t in [t2, t3_a, t4, t5] if t != D_LHS)
    R("R40", "FAIL", "【回归 r39 T27】式(17) 右端 4 项与左端不齐次（平流项除外）；"
      "互异量纲数随口径在 4~5 间变动，但结论不依赖口径",
      "左端=" + dstr(D_LHS) + "；各项=" + " / ".join(terms.values()) +
      "；互异数（α 无量纲 + M1 修补 G）=" + str(len(uniq)) + "；不齐次项数=" + str(n_mis) +
      "；r39 的 5 个互异 = [α]=L 口径 + 未修补 G_th（αS_κ=L⁻⁴）")
    G("G-E1", len(uniq) >= 4 and n_mis == 4, "式(17) ≥4 个互异量纲且 4 项不齐次（口径无关）",
      "互异=" + str(len(uniq)) + " 不齐次=" + str(n_mis))

    # --- R41 修补形式：空间导数项、势项、源项统一乘 c²，且势/源须取修补后的 L⁻³ 形式
    D_C2 = dpow(D_C, 2)
    p2 = dmul(D_C2, t2)
    p3 = dmul(D_C2, t3_a)
    p4 = dmul(D_C2, ddiv(ddiv(dim(0, 0, -4, 0), dpow(D_C, 4)), D_KAPPA))   # c² ∂(V/c⁴)/∂κ
    p5 = dmul(D_C2, dmul(t5, D_KAPPA))                                     # c² · (S∝Gρκ/c²)
    ok41 = (t1 == D_LHS) and (p2 == D_LHS) and (p3 == D_LHS) and (p4 == D_LHS) and (p5 == D_LHS)
    K("M6_patched_dims", {"β∂Π": dstr(t1), "c²αD̃²κ": dstr(p2), "c²∂_kα D̃κ": dstr(p3),
                          "c²α∂(V/c⁴)/∂κ": dstr(p4), "c²αS_κ": dstr(p5)}, "修补后式(17) 各项量纲")
    R("R41", "PASS" if ok41 else "FAIL",
      "M6 修补形式：∂_tΠ_κ = β^k∂_kΠ_κ + c²[αD̃²κ + ∂_kα D̃κ − α∂(V/c⁴)/∂κ − αS_κ] 全部齐次",
      "五项（修补后）均 = " + dstr(D_LHS))
    G("G-E2", ok41, "修补后式(17) 五项齐次（全部 L⁻¹T⁻²）", dstr(D_LHS))

    # --- R42 项3 的 α 口径不敏感性（两种口径都需 c²）
    ok42 = (t3_a != D_LHS) and (t3_b != D_LHS)
    R("R42", "PASS" if ok42 else "FAIL", "项3 的量纲依赖 [α] 口径，但两种口径下都不匹配左端 ⇒ 结论不依赖口径",
      "[α] 无量纲 ⇒ " + dstr(t3_a) + "；[α]=L ⇒ " + dstr(t3_b) + "；左端=" + dstr(D_LHS))
    G("G-E3", ok42, "项3 在两种 α 口径下均不齐次", dstr(t3_a) + " / " + dstr(t3_b))

    # --- R43 (17) 与 (10) 的结构对应：空间部分 = c² × (10) 的空间部分
    R("R43", "PASS", "修补后 (17) 与 (10) 同源：空间导数/势/源三项均为 c²×(10) 的对应项",
      "⇒ (17) 不是独立方程，而是 (10) 的一阶（Π）形式；两者不得独立计数自由度")
    G("G-E4", dmul(D_C2, dim(0, -3, 0, 0)) == D_LHS, "c²×L⁻³ = L⁻¹T⁻²（结构对应成立）", dstr(D_LHS))

    # --- R44 缺 αKΠ 项与 D̃² 共形因子（不自推）
    NSD("(17)(18) 中 αKΠ 项的系数与符号",
        "依赖 lapse/√γ 时间依赖的约定，须核对原文献；本册只判结构性缺失")
    NSD("(17)(18) 中 D̃² 作用于标量的共形修正项（e^{-4φ} 因子与联络差项）",
        "只判缺失，不给具体式子")
    R("R44", "BOUNDARY", "M6 残余：(17)(18) 仍缺 αKΠ 项与 D̃² 的共形修正（e^{-4φ}、联络差）⇒ 不自推",
      "补完 R41 的 c 幂次只解决量纲齐次，不解决共形/约束耦合的正确性")

    # --- R45 修补后可数值化？
    R("R45", "BOUNDARY", "修补后 (17)(18) 量纲齐次 ⇒ 形式上进 RK4/FDTD；"
      "但 αKΠ 与共形项未定 ⇒ 数值结果不可作为物理结论",
      "可数值化 ≠ 可判定（r21 册同款纪律）")

# ================================================================ Stage F  M7/M8/M9
def stage_F():
    """M7 挠率指标合法性；M8 约束集的 EC 挠率项；M9 弱场推导的矢量恒等式。"""
    # --- R50 M7：式(6) 的 ε 指标
    d_eps4 = D_ONE                                   # Levi-Civita 张量无量纲
    d_tors = D_KAPPA                                 # [T^α_μν] = L^-1
    d_fixed = dmul(d_eps4, d_tors)
    ok50 = (d_fixed == D_KAPPA)
    R("R50", "PASS" if ok50 else "FAIL",
      "M7：式(6) 应写 T^ρ = ε^{ραβγ}T_{αβγ}（四指标 ⇒ 矢量），原写 ε_α{}^{μν} 三指标未定义",
      "修补后量纲 " + dstr(d_fixed) + " 与 [τ]=L⁻¹ 一致")
    G("G-F1", ok50, "M7 修补后为矢量且量纲= L⁻¹", dstr(d_fixed))

    # --- R51 M8：约束集合缺 EC 挠率项
    NSD("EC 版哈密顿/动量约束的挠率贡献项正确形式",
        "只判「与标准 BSSN 逐字同 ⇒ 无挠率内容」，不给具体式子")
    R("R51", "MISMATCH", "M8：C_H 与 C_M^i 与标准 BSSN 逐字同 ⇒ 「EC 版约束」无挠率/自旋流内容（不自推）",
      "修补须引入挠率贡献项与自旋流 j^i 的挠率部分；具体形式依赖 EC 约定 ⇒ 不代写")

    # --- R52 M9：∇·(κ r̂) ≠ ∇²κ（解析 + 数值双路径对拍）
    lam = Decimal("2")
    rows52 = []
    dev52 = Decimal(0)
    for r in ["1", "3", "5", "7"]:
        rr = Decimal(r)
        e = (-(rr / lam)).exp()                       # e^{-r/λ}，A=1
        divk = e * (Decimal(-1) / lam + Decimal(2) / rr)      # ∂_rκ + 2κ/r
        lapk = e * (Decimal(1) / (lam * lam) - Decimal(2) / (lam * rr))  # ∂_r²κ + 2∂_rκ/r
        ratio = divk / lapk
        dev52 = max(dev52, rel(ratio, -lam))
        rows52.append({"r": r, "div_kappa_rhat": gfmt(divk), "lap_kappa": gfmt(lapk),
                       "ratio": gfmt(ratio)})
    K("M9_div_vs_lap", rows52, "κ=e^{-r/λ} 时 ∇·(κ r̂) 与 ∇²κ 的对比（λ=2）")
    R("R52", "PASS" if dev52 < Decimal("1e-40") else "FAIL",
      "M9：∇·(κ r̂) = −λ ∇²κ（λ=2 四点对拍）⇒ 两者不可互换（差一个长度）",
      "比值与 −λ 的最大相对偏差=" + gfmt(dev52))
    G("G-F2", dev52 < Decimal("1e-40"), "∇·(κr̂) = −λ∇²κ 机器成立", gfmt(dev52))

    # --- R53 量纲判据
    d_divk = dmul(dim(0, -1, 0, 0), D_KAPPA)                       # ∇·(κ r̂) = L^-2
    d_lapk = dmul(dim(0, -2, 0, 0), D_KAPPA)                       # ∇²κ = L^-3
    d_grho = dmul(D_G, D_RHO)                                      # Gρ = T^-2
    ok53 = (dmul(dpow(D_C, 2), d_divk) == d_grho) and (dmul(dpow(D_C, 2), d_lapk) != d_grho)
    R("R53", "PASS" if ok53 else "FAIL",
      "M9 量纲判据：c²∇·(κ r̂) = [Gρ] = T⁻² 齐次；c²∇²κ = L⁻¹T⁻² 不齐次",
      "[∇·(κr̂)]=" + dstr(d_divk) + "；[∇²κ]=" + dstr(d_lapk) + "；[Gρ]=" + dstr(d_grho))
    G("G-F3", ok53, "牛顿还原须用 ∇·(κ r̂) 形式（∇²κ 形式量纲不成立）", dstr(d_grho))

    # --- R54 来料弱场式的内部矛盾（sinθ 幂次）
    gth_sin = (Decimal(2) * PI * C_VAL ** 3) / HBAR    # G_th·sinθ（用(4) 代入后 sinθ 消去）
    K("M9_Gth_times_sin", gth_sin, "G_th·sinθ = 2πc³/ħ（sinθ 被消去）")
    R("R54", "FAIL", "来料式(90) 用 G_th·sinθ、式(94) 用 G_th·sin²θ ⇒ 同一次推导内 sinθ 幂次自相矛盾；"
      "且 G_th·sinθ = 2πc³/ħ = " + gfmt(gth_sin)[:12] + "（比 G 大 70 量级）",
      "⇒ 修补 M9 前，弱场段的系数在量级与幂次两处同时不成立")

    # --- R55【本册新增】阶数不匹配：牛顿解不满足 (10) 的静态真空极限
    #     一阶方程 ∂_rκ + 2κ/r = 4πGρ/c² 的真空解 κ = A/r²（A = GM/c²）
    #     ∇²(A/r²) = 2A/r⁴ ≠ 0 ⇒ 与"静态真空下 (10) 齐次"冲突
    rows55 = []
    for r in ["1", "2", "5", "10"]:
        rr = Decimal(r)
        A = Decimal("1")
        first = Decimal(-2) * A / rr ** 3 + Decimal(2) * (A / (rr * rr)) / rr   # ∂_rκ + 2κ/r
        lap = Decimal(2) * A / rr ** 4                                          # ∇²(A/r²)
        rows55.append({"r": r, "first_order_vacuum": gfmt(first), "lap_A_over_r2": gfmt(lap)})
    K("M9_order_mismatch", rows55, "κ=A/r² 的一阶方程残差与拉普拉斯")
    R("R55", "BOUNDARY", "【本册新增】牛顿真空解 κ=GM/(c²r²) 满足一阶方程 ∂_rκ+2κ/r=0，"
      "但其拉普拉斯 ∇²κ=2GM/(c²r⁴)≠0 ⇒ 与 (10) 的静态真空极限冲突",
      "⇒ 弱场牛顿还原与二阶传播方程对 κ 的要求不同，须择一；"
      "若保留 M4（V≠0）则势项或可吸收该残留，但牛顿还原将不再由源驱动 ⇒ 不代选")
    G("G-F4", all(Decimal(r["first_order_vacuum"]) == 0 for r in rows55)
      and all(Decimal(r["lap_A_over_r2"]) > 0 for r in rows55),
      "κ=A/r² 满足一阶真空方程但 ∇²κ≠0", "4 点")

    # --- R56 外部输入总账
    ledger = [
        {"item": "ℓ（修式(4) 所需长度标度）", "source": "M1", "kind": "外部常数", "count": 1},
        {"item": "τ–κ 的新几何关系（弃式(2) 后）", "source": "M2-c", "kind": "外部关系式", "count": 1},
        {"item": "ℓ_s（若源项走候选乙）", "source": "M5-乙", "kind": "外部常数", "count": 1},
        {"item": "ω 的独立演化方程与初值", "source": "M4", "kind": "演化场+方程", "count": 1},
        {"item": "EC 约束的挠率贡献项", "source": "M8", "kind": "不自推", "count": 0},
    ]
    K("external_input_ledger", ledger, "修补后外部输入总账（Ω5「自由常数 ≤1」）")
    R("R56", "FAIL", "修补后外部输入 ≥ 2（ℓ + τ–κ 新关系），撞 Ω5「自由常数 ≤1」",
      "来料自评「G_th 第一性导出」隐含 0 外部输入；修补后至少 +2 ⇒ 须改口径或显式登记")

# ================================================================ Stage G  总账与结论
def stage_G():
    """修补后的自由度计数、自评重审、A/B 解锁状态与结论。"""
    # --- R60 自由度计数（物质扇区）
    dof_before = 1        # κ 独立（τ 被 (2) 奴役、(11) 冗余）
    dof_after = 3         # κ,τ,ω 三独立场（M2-c + M4），C_ω 由 V 阻尼而非投影
    K("dof_scalar_sector", {"before": dof_before, "after_M2c_M4": dof_after},
      "物质扇区物理自由度（相空间 = 2×DOF）")
    R("R60", "INFO", "修补后物质扇区自由度 1 ⇒ 3（κ,τ,ω 三独立标量场，C_ω 由势阻尼而非投影）",
      "代价：+1 演化场 +1 方程 +1 初值组；若 C_ω 改回投影约束则自由度降为 2.5（奇数，不可物理）")

    # --- R61 第五部分 5 条自评的修补后重审
    review = [
        {"no": 1, "claim": "完整一阶双曲 PDE 组，适配 RK4/FDTD/ADM-BSSN",
         "r39": "不成立", "patched": "部分成立",
         "why": "量纲已齐次（R41），但 αKΠ 与共形项未定（R44）⇒ 可数值化不可判定"},
        {"no": 2, "claim": "κ、τ 双动力学自由度",
         "r39": "不成立", "patched": "成立（需 M2-c）",
         "why": "仅删 (3) 分支不够（τ 仍奴役）；须弃 (2) 并给新关系（R16–R18）"},
        {"no": 3, "claim": "G_th 由螺旋升角、c、ħ 第一性导出",
         "r39": "不成立", "patched": "不成立",
         "why": "M1 后须补 ℓ ⇒ 导出集变为 {c,ħ,θ,ℓ}（R08）"},
        {"no": 4, "claim": "内置约束势抑制数值漂移",
         "r39": "不成立（V≡0）", "patched": "成立（需 M4）",
         "why": "ω 独立演化后 V≠0（R22），势项与 C_ω 阻尼机制方成立"},
        {"no": 5, "claim": "弱场极限回归牛顿引力",
         "r39": "不成立", "patched": "不成立/存疑",
         "why": "M9 后须用 ∇·(κ r̂) 一阶方程（R53），与 (10) 静态二阶极限冲突（R55）"},
    ]
    K("self_claim_review_patched", review, "第五部分 5 条自评的修补后重审")
    R("R61", "CORRECTED", "修补后自评 5 条：成立 1（第 4 条）、条件成立 2（第 1、2 条）、仍不成立 2（第 3、5 条）",
      "相对 r39 的 0/5 有实质改善，但代价是外部输入 ≥2 与一条新存疑项（R55）")

    # --- R62 A/B 解锁状态
    R("R62", "BOUNDARY", "修补后：任务 A【可执行但无判别力】（χ² 要么 ≡0 要么依赖 ℓ 先验）；"
      "任务 B【可执行但须先声明窗口关系】",
      "A：M1 后 G_th 可算，但情形乙 χ²≡0、情形甲撞 Ω5（R06–R07）；"
      "B：M2 后 τ≠0 可行，但 M2-d 路线 τ/κ≤" + KEYNUM["M2_q_max"]["value"][:10] +
      " ⇒ 挠率效应 ≤u_G；M2-c 路线 θ 无来源；且库内 g‑2/EDM 窗口已关（r19/r27）")

    # --- R63 结论
    R("R63", "FAIL", "【总结】M1–M9 修补后方程组【量纲齐次、τ 可非零、势项复活】，"
      "但代价为外部输入 ≥2（撞 Ω5）+ 一条新的弱场存疑（R55）+ 自评第 3/5 条仍不成立",
      "⇒ 修补路径本身可行，但达成「可判定」须再接受 2 个外部输入并放弃「第一性导出 G」的宣称；"
      "是否接受由用户裁决，本册不代选")


# ================================================================ main
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    guards_stage0()
    stage_A()
    stage_B()
    stage_C()
    stage_D()
    stage_E()
    stage_F()
    stage_G()

    cnt = {}
    for r in RESULTS:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    g_pass = sum(1 for g in GUARDS if g["ok"])
    g_all = len(GUARDS)

    payload = {
        "round": "r41",
        "date": "2026-10-12",
        "title": "TUFT-V4 耦合演化场方程组 M1–M9 最小修补与可判定性复审",
        "source_material": "数据/TUFT-V4-EC-ADMBSSN耦合演化场方程组_来料全文_2026-10-12.md",
        "predecessor": "判定_TUFT-r39-V4-EC-ADMBSSN耦合场方程组_全维审计_2026-10-12.md",
        "items": len(RESULTS),
        "verdict_count": cnt,
        "guards": {"pass": g_pass, "total": g_all},
        "results": RESULTS,
        "guard_list": GUARDS,
        "key_numbers": KEYNUM,
        "not_self_derived": NOT_SELF_DERIVED,
    }

    stamp = "TUFT-r41_V4-M1M9最小修补与可判定性复审_2026-10-12"
    p_json = os.path.join(OUT_DIR, stamp + ".json")
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(_jsonable(payload), f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# 数据：TUFT-r41 V4 耦合演化场方程组 M1–M9 最小修补与可判定性复审")
    lines.append("")
    lines.append("- 轮次：r41（撞号处置：r40 已被并行会话占用 ⇒ 取空号 r41，条目前缀 R01–R63）")
    lines.append("- 日期：2026-10-12")
    lines.append("- 条目：" + str(len(RESULTS)) + "　自检：" + str(g_pass) + "/" + str(g_all))
    lines.append("")
    lines.append("## 逐条判定")
    lines.append("")
    lines.append("| 条目 | 判定 | 标题 | 读数 |")
    lines.append("|---|---|---|---|")
    for r in RESULTS:
        lines.append("| " + r["code"] + " | " + r["verdict"] + " | " + r["title"] +
                     " | " + r["detail"].replace("|", "/") + " |")
    lines.append("")
    lines.append("## 自检守卫")
    lines.append("")
    for g in GUARDS:
        lines.append("- " + g["code"] + " " + ("PASS" if g["ok"] else "**BAD**") +
                     " — " + g["title"] + "（" + g["detail"] + "）")
    lines.append("")
    lines.append("## 不自推登记")
    lines.append("")
    for n in NOT_SELF_DERIVED:
        lines.append("- " + n["item"] + "：" + n["note"])
    lines.append("")
    p_md = os.path.join(OUT_DIR, stamp + ".md")
    with open(p_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    rep = []
    rep.append("TUFT-r41 M1–M9 最小修补与可判定性复审")
    rep.append("PASS=" + str(cnt.get("PASS", 0)) + " FAIL=" + str(cnt.get("FAIL", 0)) +
               " BOUNDARY=" + str(cnt.get("BOUNDARY", 0)) +
               " MISMATCH=" + str(cnt.get("MISMATCH", 0)) +
               " CORRECTED=" + str(cnt.get("CORRECTED", 0)) +
               " INFO=" + str(cnt.get("INFO", 0)))
    rep.append("ITEMS=" + str(len(RESULTS)) + " GUARDS=" + str(g_pass) + "/" + str(g_all))
    p_rep = os.path.join(OUT_DIR, stamp + "_report.txt")
    with open(p_rep, "w", encoding="utf-8") as f:
        f.write("\n".join(rep))

    print("条目 " + str(len(RESULTS)) + "：" + " ".join(k + "=" + str(v) for k, v in sorted(cnt.items())))
    print("自检 " + str(g_pass) + "/" + str(g_all))
    print("产物：" + p_json)
    print("产物：" + p_md)
    print("产物：" + p_rep)
    return 0 if g_pass == g_all else 1


def _jsonable(o):
    """把 Fraction / Decimal 转为可序列化对象。"""
    if isinstance(o, dict):
        return dict((k, _jsonable(v)) for k, v in o.items())
    if isinstance(o, (list, tuple)):
        return [_jsonable(x) for x in o]
    if isinstance(o, Fr):
        return str(o)
    if isinstance(o, Decimal):
        return str(o)
    return o


if __name__ == "__main__":
    sys.exit(main())

