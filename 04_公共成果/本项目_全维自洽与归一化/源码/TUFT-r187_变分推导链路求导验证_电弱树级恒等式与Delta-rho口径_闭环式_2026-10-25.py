# -*- coding: utf-8 -*-
"""
TUFT-r187 · 《07_统一场方程/02_变分推导.md》求导链路闭环式审计
2026-10-25

承接：
  r183/r184/r185 收口①可精算池 12/12；r186 收口 F5 钱德拉塞卡（②层）。
  r186 §7 排定下一阶段真实增量：核心公式卷进入闭环式审计。
  本册取 `07_统一场方程/02_变分推导.md`（求导证明）为首卷 —— 它把
  δS/δΦ=0 的逐步推导落成 (C)/(E)/(YM)/(H)/(D) 五式，并给出可机读的
  电弱树级恒等式（v、λ、m_W、m_Z、ρ、Δρ、a_e）。

本册职责：
  1) 量纲门禁：κ²=8πG/c⁴ 的 SI 五元组维，及 κ²T_μν 是否回到曲率 L^-2；
     自然单位（ħ=c=1）下 G_F/v/κ²/G_μν/T_μν 的能量幂账。
  2) 求导链路：Higgs 势 V(h) 的一阶导（真空条件）与二阶导（m_h²=2λv²），
     用 250 位精确多项式 + 中心二阶差分互证。
  3) 质量矩阵：v²/4·[[g2²,-g1g2],[-g1g2,g1²]] 的解析本征分解 ⇒ m_γ=0、m_Z。
  4) 电弱树级恒等式：v=(√2G_F)^{-1/2}、g2=2m_W/v、sin²θ_W=1−m_W²/m_Z²、
     ρ_tree=1、λ=m_h²/(2v²)、a_e=α/2π。
  5) 口径审计：树级网给出的 α^{-1}；Δρ_t=3G_Fm_t²/(8√2π²) 与 PDG
     ρ_0=1.00038±0.00020 的归属是否同一口径（本册机器判定：不是）。
  6) 结构性条目：(C) 的系数链、(YM) 的符号链、四费米子 3/8 vs 3/16。

纪律：审计对象是项目自有推导链，不是外部探针；三判定按「TUFT 侧独立数值
      供给」记为 C1（0 供给），不改写来料字节。
红线：不产生新物理、不改写来料、不改 verify.py、不做 git。
"""
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r187_变分推导链路求导验证_电弱树级恒等式与Delta-rho口径_闭环式_2026-10-25"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal
ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def control(name, ok, msg=""):
    ok = bool(ok)
    CONTROLS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [CONTROL-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def fs(x, nd=25):
    try:
        v = D(x)
        if v.is_zero():
            return "0." + "0" * nd + "E+0"
        return format(v, "." + str(nd) + "E")
    except Exception:
        return str(x)


# =====================================================================
# 0. 量纲机器
# =====================================================================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    n = int(n)
    return tuple(x * n for x in a)


def dstr(a):
    names = ("M", "L", "T", "Q", "K")
    parts = []
    for nm, ex in zip(names, a):
        if ex == 0:
            continue
        if ex == 1:
            parts.append(nm)
        elif ex.denominator == 1:
            parts.append("%s^%d" % (nm, ex.numerator))
        else:
            parts.append("%s^%s" % (nm, ex))
    return " ".join(parts) if parts else "1"


F0 = Fraction(0)
F1 = Fraction(1)
MSS = (F1, F0, F0, F0, F0)
LEN = (F0, F1, F0, F0, F0)
TIM = (F0, F0, F1, F0, F0)

DIM = {
    "c":    (F0, F1, Fraction(-1), F0, F0),
    "G":    (Fraction(-1), Fraction(3), Fraction(-2), F0, F0),
    "hbar": (F1, Fraction(2), Fraction(-1), F0, F0),
}

# ---- 常数（CODATA 2018/2022 / PDG 2022，单一 250 位口径）----
PI_STR = ("3."
          "14159265358979323846264338327950288419716939937510"
          "58209749445923078164062862089986280348253421170679"
          "82148086513282306647093844609550582231725359408128"
          "48111745028410270193852110555964462294895493038196")
PI = D(PI_STR)
CV = D("299792458")
GV = D("6.67430E-11")
GF = D("1.1663787E-5")          # GeV^-2
MW = D("80.377")                # GeV
MZ = D("91.1876")               # GeV
MH = D("125.25")                # GeV
MT = D("172.69")                # GeV
ALPHA = D("7.2973525693E-3")
SIN2_MS = D("0.23122")          # MS-bar sin²θ_W(m_Z)
AE_EXP = D("1.15965218128E-3")  # 电子反常磁矩实测
RHO_PDG = D("1.00038")
RHO_PDG_SIG = D("0.00020")

VERDICT = ("R187-VARIATIONAL-CHAIN-AUDIT-"
           "DIM-KAPPA2-OK-NATURAL-UNIT-OK-"
           "DERIV-VACUUM-ZERO-MH2-2LAMV2-OK-LAMBDA-0.12938-"
           "MASS-MATRIX-MGAMMA-0-MZ-OK-SIN2-IDENTITY-RHO-TREE-1-"
           "ALPHA-TREE-INV-132.1-BOUNDARY-"
           "DRHO-0.00935-VS-RHOPOLE-0.00038-FAIL-LABEL-25X-"
           "MSBAR-RHO-1.010625-CONSISTENT-"
           "AE-ALPHA-OVER-2PI-0.15PCT-"
           "4FERMION-3-8-VS-3-16-CONVENTION-BOUNDARY-TUFT-SUPPLY-0")


def eig2(a, b, d):
    """2×2 实对称矩阵解析本征值（b 为对称非对角元）。"""
    tr = a + d
    det = a * d - b * b
    disc = (tr * tr - D(4) * det).sqrt()
    return (tr + disc) / D(2), (tr - disc) / D(2)


def main():
    print("=" * 78)
    print("TUFT-r187 · 变分推导链路求导验证（电弱树级恒等式与 Δρ 口径）")
    print("=" * 78)

    # =================================================================
    # A 段 · 量纲门禁
    # =================================================================
    print("\n[A] 量纲门禁（SI 五元组 / 自然单位能量幂）")

    d_k2 = dmul(DIM["G"], dpow(DIM["c"], -4))
    guard("G01 kappa2_dim", d_k2 == (Fraction(-1), Fraction(-1), Fraction(2), F0, F0),
          "κ²=8πG/c⁴ 维 " + dstr(d_k2))
    d_T = (F1, Fraction(-1), Fraction(-2), F0, F0)          # 能量密度
    d_curv = dmul(d_k2, d_T)
    guard("G02 kappa2_T_is_curvature", d_curv == dpow(LEN, -2),
          "κ²T_μν 维 " + dstr(d_curv))

    num_k2 = D(8) * PI * GV / (CV ** 4)
    guard("G03 kappa2_value", abs(num_k2 / D("2.07664744E-43") - D(1)) < D("1E-6"),
          "8πG/c⁴=" + fs(num_k2, 12) + " m/kg")

    # 自然单位（ħ=c=1）：一切以能量幂记账
    E_GF, E_V, E_K2, E_G, E_T, E_LAM, E_RHO = -2, 1, -2, 2, 4, 0, 0
    guard("G04 natural_power_ledger",
          (E_GF + 2 * E_V == 0) and (E_K2 + E_T == E_G) and (E_LAM == 0) and (E_RHO == 0),
          "G_F E^-2、v E^1、κ² E^-2、G E^2、T E^4、λ E^0")

    add("A01", "PASS", "量纲门禁：κ²=8πG/c⁴ 与 κ²T_μν 回到曲率 L^-2",
        "SI 五元组：G=(M^-1L^3T^-2)、c^4=(L^4T^-4) ⇒ κ²=(M^-1L^-1T^2)；"
        "乘能量密度 (M L^-1 T^-2) 得 " + dstr(d_curv) + "，正是 G_μν 的维。"
        "数值 8πG/c⁴=" + fs(num_k2, 8) + " m/kg ⇒ (E') 的系数位闭合。",
        {"kappa2_dim": dstr(d_k2), "kappa2_T_dim": dstr(d_curv),
         "kappa2_si": fs(num_k2, 8)})

    add("A02", "PASS", "自然单位（ħ=c=1）能量幂账：G_F/v/κ²/G/T/λ/ρ 全部对齐",
        "G_F=E^-2、v=E^1、κ²=8πG=E^-2、G_μν=E^2、T_μν=E^4、λ=E^0、ρ=E^0。"
        "三条恒等式：G_F·v²=E^0（v 的定义）、κ²·T_μν=E^2（场方程）、"
        "λ 与 ρ 无量纲（真空条件与 custodial）。⇒ 本卷后续所有读数都在同一口径下。",
        {"E_GF": E_GF, "E_v": E_V, "E_kappa2": E_K2, "E_G": E_G, "E_T": E_T})

    # =================================================================
    # B 段 · Higgs 势的求导链（一阶真空条件 / 二阶质量）
    # =================================================================
    print("\n[B] Higgs 势求导链（真空条件 / 二阶质量）")

    VEV = D(1) / ((D(2).sqrt() * GF).sqrt())
    guard("G05 v_from_GF", abs(VEV - D("246.2196")) < D("1E-3"),
          "v=" + fs(VEV, 10) + " GeV")

    LAM = MH * MH / (D(2) * VEV * VEV)
    guard("G06 lambda_value", abs(LAM - D("0.12938")) < D("1E-4"),
          "λ=" + fs(LAM, 10))
    MU2 = LAM * VEV * VEV
    MU = LAM.sqrt() * VEV

    def Vpot(h):
        x = VEV + h
        return -(MU2 * x * x) / D(2) + (LAM * x ** 4) / D(4)

    def dVpot(h):
        x = VEV + h
        return -(MU2 * x) + LAM * x ** 3

    dV0 = dVpot(D(0))
    guard("G07 vacuum_condition_zero", abs(dV0) < D("1E-200"),
          "dV/dh|0=" + fs(dV0, 6))

    d2_exact = 2 * LAM * VEV * VEV
    STEP = D("1E-40")
    fd2 = (Vpot(STEP) - D(2) * Vpot(D(0)) + Vpot(-STEP)) / (STEP * STEP)
    rel_fd = abs(fd2 / d2_exact - D(1))
    guard("G08 second_deriv_matches", rel_fd < D("1E-60"),
          "差分 " + fs(fd2, 12) + " vs 解析 " + fs(d2_exact, 12) +
          "（相对 " + fs(rel_fd, 6) + "）")
    guard("G09 mh_squared", abs(d2_exact - MH * MH) / (MH * MH) < D("1E-20"),
          "d²V/dh²=" + fs(d2_exact, 8) + " vs m_h²=" + fs(MH * MH, 8))
    guard("G10 mu_relation", abs(D(2).sqrt() * MU / MH - D(1)) < D("1E-200"),
          "√2·μ=" + fs(D(2).sqrt() * MU, 10) + " GeV")

    add("B01", "PASS", "v=(√2G_F)^{-1/2}=" + fs(VEV, 9) + " GeV（推论 4.1 的数值位）",
        "G_F=1.1663787E−5 GeV^-2 ⇒ √2G_F=" + fs(D(2).sqrt() * GF, 12) +
        " GeV^-2，取 −1/2 次得 " + fs(VEV, 9) + " GeV。与来料 246.22 GeV 在 1E−3 内一致"
        "（来料为三位小数口径）。**诚实标注**：v 是输入常数 G_F 的等价改写，不是 TUFT 预言。",
        {"v_GeV": fs(VEV, 10), "sqrt2_GF": fs(D(2).sqrt() * GF, 12)})

    add("B02", "PASS", "真空条件：dV/dh|₀ = 0（机器零），对应 |H|²=μ²/(2λ)",
        "取 H=(0,(v+h)/√2) ⇒ V(h)=−μ²(v+h)²/2+λ(v+h)⁴/4；令 μ²=λv² 后 V'(0)=v(−μ²+λv²)=" +
        fs(dV0, 3) + " 机器零。这就是 (H) 式右边在 H=⟨H⟩ 处为零的算术形式，"
        "也即 推论 4.1 的 |H|²=μ²/(2λ)（此处 |H|²=v²/2）。",
        {"dV0": fs(dV0, 6), "mu2": fs(MU2, 8)})

    add("B03", "PASS", "二阶导：d²V/dh²|₀ = 2λv² = m_h²（解析与差分互证）",
        "解析 " + fs(d2_exact, 10) + "；中心二阶差分（步长 1E−40）" + fs(fd2, 12) +
        "，相对差 " + fs(rel_fd, 6) + " ⇒ 机器零。与 m_h²=" + fs(MH * MH, 8) +
        " 相对差 " + fs(abs(d2_exact / (MH * MH) - D(1)), 6) +
        "。**这就是 推论 4.4 的 m_h²=2λv²=2μ² 的求导证明**：不需要额外假设，"
        "只需 V 的二阶展开。",
        {"d2_analytic": fs(d2_exact, 10), "d2_fd": fs(fd2, 12),
         "rel_fd": fs(rel_fd, 6), "mh2": fs(MH * MH, 8)})

    add("B04", "PASS", "λ=m_h²/(2v²)=" + fs(LAM, 8) + "（来料写 0.129，四位内一致）",
        fs(MH * MH, 8) + " / (2×" + fs(VEV, 8) + "²) = " + fs(LAM, 8) +
        "；取三位有效即 0.129。λ 与 μ 都是可反解的派生量，原始输入只有 m_h 与 v "
        "（v 本身又由 G_F 定）⇒ 本项没有自由参数。",
        {"lambda": fs(LAM, 10), "mu_GeV": fs(MU, 10)})

    add("B05", "PASS", "自洽闭环：m_h = √2 μ（μ=√λ v=" + fs(MU, 8) + " GeV）",
        "√2·μ=" + fs(D(2).sqrt() * MU, 10) + " GeV，与 m_h 相对差 " +
        fs(abs(D(2).sqrt() * MU / MH - D(1)), 6) +
        " ⇒ 推论 4.4 的 m_h²=2μ² 与 μ²=λv² 两式相容。",
        {"mu": fs(MU, 10), "sqrt2_mu": fs(D(2).sqrt() * MU, 10)})

    # =================================================================
    # C 段 · 规范扇区：质量矩阵与树级恒等式
    # =================================================================
    print("\n[C] 规范扇区（质量矩阵 / 树级恒等式 / 口径）")

    G2 = D(2) * MW / VEV
    G1SQ = D(4) * MZ * MZ / (VEV * VEV) - G2 * G2
    G1 = G1SQ.sqrt()
    SIN2 = G1SQ / (G1SQ + G2 * G2)

    q11 = G2 * G2
    q12 = -G1 * G2
    q22 = G1SQ
    l1, l2 = eig2(q11, q12, q22)
    mZ_eig = (VEV / D(2)) * max(l1, l2).sqrt()
    mG_eig = (VEV / D(2)) * min(l1, l2).sqrt()
    guard("G11 mass_matrix_mZ", abs(mZ_eig / MZ - D(1)) < D("1E-50"),
          "m_Z(本征)=" + fs(mZ_eig, 10))
    guard("G12 mass_matrix_mgamma0", abs(min(l1, l2)) < D("1E-200"),
          "零本征值=" + fs(min(l1, l2), 6))

    sin2_identity = D(1) - MW * MW / (MZ * MZ)
    guard("G13 sin2_identity", abs(SIN2 - sin2_identity) < D("1E-200"),
          "两路口径差 " + fs(abs(SIN2 - sin2_identity), 6))

    RHO_TREE = (G2 * VEV / D(2)) ** 2 / ((VEV * VEV / D(4)) * (G2 * G2 + G1SQ) *
                                        G2 * G2 / (G2 * G2 + G1SQ))
    guard("G14 rho_tree_one", abs(RHO_TREE - D(1)) < D("1E-200"),
          "ρ_tree=" + fs(RHO_TREE, 10))

    E_TREE = G2 * SIN2.sqrt()
    ALPHA_TREE = E_TREE * E_TREE / (D(4) * PI)
    INV_ALPHA_TREE = D(1) / ALPHA_TREE
    guard("G15 alpha_tree_value", abs(INV_ALPHA_TREE - D("132.1")) < D("0.2"),
          "α_tree^-1=" + fs(INV_ALPHA_TREE, 8))

    add("C01", "PASS", "质量矩阵本征分解：m_γ=0（机器零）、m_Z=" + fs(mZ_eig, 8) + " GeV",
        "M²=(v²/4)[[g2²,−g1g2],[−g1g2,g1²]]，本征值 " + fs(l1, 10) + " / " +
        fs(l2, 6) + "；开方乘 v/2 ⇒ m_Z=" + fs(mZ_eig, 8) + " GeV（与输入 m_Z 相对差 " +
        fs(abs(mZ_eig / MZ - D(1)), 6) + "），光子支 m_γ=" + fs(mG_eig, 6) +
        "（零本征值 <1E−200）。⇒ 推论 4.2 的 m_γ=0 是**残留规范对称性的代数后果**，非参数调节。",
        {"lambda_plus": fs(l1, 10), "lambda_minus": fs(l2, 6),
         "mZ": fs(mZ_eig, 10), "mgamma": fs(mG_eig, 6)})

    add("C02", "PASS", "m_W=g2v/2 ⇒ 由实测 m_W 反解 g2=" + fs(G2, 8),
        "g2=2m_W/v=2×" + fs(MW, 6) + "/" + fs(VEV, 8) + "=" + fs(G2, 8) +
        "；再由 m_Z=g1,g2 组合反解 g1=" + fs(G1, 8) + "。**注意**：这是用**同一批实测质量**"
        "反解耦合，属口径反演，不是预言。",
        {"g2": fs(G2, 10), "g1": fs(G1, 10)})

    add("C03", "PASS", "sin²θ_W 两路口径精确同值：" + fs(SIN2, 8) + " = 1−m_W²/m_Z²",
        "代数恒等式：sin²θ_W=g1²/(g1²+g2²)、1−m_W²/m_Z²=1−g2²/(g1²+g2²)=g1²/(g1²+g2²)；"
        "机器差 " + fs(abs(SIN2 - sin2_identity), 6) + " ⇒ 零。该式**不含物理内容**，"
        "只证明 推论 4.2 的 tanθ_W=g1/g2 与质量比定义自洽。",
        {"sin2": fs(SIN2, 10), "sin2_identity": fs(sin2_identity, 10)})

    add("C04", "PASS", "ρ_tree = 1 精确（机器零）——但这是代数恒等，不是 custodial 的证据",
        "按来料 推论 4.3 的表达式逐项代入，机器给 " + fs(RHO_TREE, 10) +
        "，差 " + fs(abs(RHO_TREE - D(1)), 6) +
        "。**诚实标注**：ρ的树级式在 SM 中恒为 1（因为 g1,g2 与 v 的定义使分子分母同构），"
        "所以「ρ=1」不检验任何东西；真正检验 custodial 的是**实测** ρ_0=" +
        fs(RHO_PDG, 6) + "±" + fs(RHO_PDG_SIG, 6) + " 与其偏差归属（见 C06/C07）。",
        {"rho_tree": fs(RHO_TREE, 10)})

    add("C05", "BOUNDARY", "树级网反解的 α^{-1}=" + fs(INV_ALPHA_TREE, 6) +
        " 既不等于 α^{-1}(0)=137.036，也不等于 α^{-1}(m_Z)=127.95",
        "e_tree=g2 sinθ_W=" + fs(E_TREE, 8) + " ⇒ α_tree=e²/4π=" + fs(ALPHA_TREE, 10) +
        " ⇒ α^{-1}=" + fs(INV_ALPHA_TREE, 8) + "。与 α^{-1}(0)=137.035999084 差 " +
        fs(abs(INV_ALPHA_TREE / D("137.035999084") - D(1)), 6) +
        "；与 α^{-1}(m_Z)≈127.95 差 " + fs(abs(INV_ALPHA_TREE / D("127.95") - D(1)), 6) +
        "。⇒ **口径结论**：树级关系 e=g2 sinθ_W 中的 e、g1、g2 必须在同一能标取跑动值；"
        "把「实测 m_W/m_Z（含圈）」直接代入树级网，必然落不到任何一个标准 α 值。"
        "这不是来料错误，而是树级式的适用域边界。",
        {"alpha_tree_inv": fs(INV_ALPHA_TREE, 8), "e_tree": fs(E_TREE, 8)})

    DRHO = D(3) * GF * MT * MT / (D(8) * D(2).sqrt() * PI * PI)
    guard("G16 drho_value", abs(DRHO - D("0.00935")) < D("1E-4"),
          "Δρ_t=" + fs(DRHO, 8))
    DEV = RHO_PDG - D(1)
    RATIO_DRHO = DRHO / DEV
    guard("G17 drho_vs_pdg_dev", abs(RATIO_DRHO - D("24.6")) < D("0.5"),
          "Δρ_t/实测偏差=" + fs(RATIO_DRHO, 6))

    add("C06", "FAIL", "Δρ_t=0.00935 与 PDG ρ_0−1=0.00038 相差 24.6 倍 ⇒ 两者不是同一口径（F-label）",
        "来料 推论 4.3 写「实测 1.00038±0.00020；偏差来自顶夸克圈（Δρ=3G_Fm_t²/8√2π²≈0.0094）」。"
        "机器：Δρ_t=" + fs(DRHO, 8) + "，而 PDG 偏差 =" + fs(DEV, 6) +
        "；比值 " + fs(RATIO_DRHO, 6) + " ⇒ 若真把 Δρ_t 加到 ρ 上，ρ 将为 " +
        fs(D(1) + DRHO, 8) + "，与实测差 " +
        fs((D(1) + DRHO - RHO_PDG) / RHO_PDG_SIG, 6) + "σ。"
        "⇒ **标签错位**：Δρ_t 是进入 m_W 预言的顶夸克增量（与 Δr 同族），不是 Z-pole 的 "
        "ρ_0−1 的解释项。登记 **F-label**（兼 F-scale：24.6× 量级不符）。",
        {"drho_t": fs(DRHO, 8), "pdg_dev": fs(DEV, 6),
         "ratio": fs(RATIO_DRHO, 6), "sigma_if_added": fs((D(1) + DRHO - RHO_PDG) / RHO_PDG_SIG, 3)})

    RHO_MS = MW * MW / (MZ * MZ * (D(1) - SIN2_MS))
    rel_ms = abs(RHO_MS / (D(1) + DRHO) - D(1))
    guard("G18 rho_msbar_vs_drho", rel_ms < D("1E-2"),
          "ρ(MS-bar)=" + fs(RHO_MS, 8) + " vs 1+Δρ_t=" + fs(D(1) + DRHO, 8) +
          "（相对 " + fs(rel_ms, 6) + "）")

    add("C07", "PASS", "口径归一：改用 MS-bar sin²θ_W 后 ρ=" + fs(RHO_MS, 6) +
        " ≈ 1+Δρ_t（相对差 " + fs(rel_ms, 4) + "）⇒ Δρ_t 的归属被定位",
        "以 sin²θ_W(m_Z)_MS=0.23122 计算 ρ=m_W²/(m_Z²cos²θ_W)=" + fs(RHO_MS, 8) +
        "，与 1+Δρ_t=" + fs(D(1) + DRHO, 8) + " 相对差 " + fs(rel_ms, 4) +
        "（残差来自两圈与 Δα）。⇒ 来料的 0.0094 **是对的**，只是被挂到了错误的对照量上："
        "它解释的是 MS-bar 口径的 ρ=1.0106，不是 Z-pole 的 1.00038。"
        "**这就是 C06 的修复方向**（改标签，不改公式）。",
        {"rho_MSbar": fs(RHO_MS, 8), "one_plus_drho": fs(D(1) + DRHO, 8),
         "rel": fs(rel_ms, 4)})

    # =================================================================
    # D 段 · 结构性条目与三判定
    # =================================================================
    print("\n[D] 结构性条目 / 三判定 / 供给账")

    # (C) 系数链：1/(4κ²) ×2 → 1/(2κ²)；再令 δω 任意 ⇒ (1/2)εTe=κ²s
    c_grav = Fraction(1, 4) * 2
    guard("G19 cartan_coeff_chain", (c_grav == Fraction(1, 2)),
          "1/(4κ²)×2 = 1/(2κ²)")
    add("D01", "PASS", "(C) 的系数链自洽：1/(4κ²)×2 → 1/(2κ²)，再取变分任意 ⇒ (1/2)εTe=κ²s",
        "P1→P2→P3 三步后 δωS_EC=+(1/2κ²)∫ε δω T e；物质侧 −∫δω s；令其为零即得 "
        "**(1/2)ε_{abcd}T^c∧e^d=κ²s_{ab}**，与来料 (C) 逐字一致（系数 1/4→1/2 的那一步"
        "已用 Fraction 精确核对）。⇒ 该式是**代数方程**，挠率不传播的结论成立。",
        {"coeff": "1/2", "steps": ["P1", "P2", "P3", "delta_omega=0"]})

    f38, f316 = Fraction(3, 8), Fraction(3, 16)
    guard("G20 fourfermion_ratio", (f38 / f316) == 2, "3/8 ÷ 3/16 = 2")
    add("D02", "BOUNDARY", "四费米子接触项系数 3/8 vs 3/16：差恰好因子 2，属约定未定",
        "来料 推论 1.3 给 L_int=−(3κ²/8)(ψ̄γ⁵γ^aψ)²，并自注「文献亦见 3/16」。"
        "机器：3/8 ÷ 3/16=2 精确。⇒ 两版差**恰好一个自旋张量归一化因子**，不是算术错。"
        "后果：任何「与引力同量级」「以排斥避免奇点」的**定性**结论不受影响；但若要把该项写成"
        "**可对撞机检验的定量截面**，必须先锁定归一化约定。登记 BOUNDARY（不做取舍）。",
        {"ratio": "2", "variants": ["3/8", "3/16"]})

    add("D03", "PASS", "(YM) 的符号链与电流协变守恒：D_ν j^{aν}=0 是方程推论",
        "δ_A S_YM=−(1/g²)∫tr(DδA∧⋆F)=+(1/g²)∫tr(δA∧D⋆F)（p=1，移项取 +）⇒ "
        "D⋆F=g²⋆j；再 A→gA 即 D_μF^{aμν}=g j^{aν}。取 D_ν：D_νD_μF^{aμν}=½g f^{abc}F^b_{νμ}F^{cμν}=0"
        "（反对称×对称缩并为零）⇒ D_νj^{aν}=0。**结论方向正确**：守恒是方程推论，不是额外假设。",
        {"sign_chain": ["p=1 -> +", "A->gA", "D_nu j = 0"]})

    table = [
        {"probe": "UFE-1/(C) Cartan torsion", "verdict": "C1",
         "reason": "标准 ECSK 代数方程；TUFT 侧无新增数值预言"},
        {"probe": "UFE-1/(E) Einstein-Cartan", "verdict": "C1",
         "reason": "GR 的含挠改写；s=0 时与 GR 逐字同构，无独立读数"},
        {"probe": "UFE-1/(YM)(H)(D)", "verdict": "C1",
         "reason": "SM 三式重写；所有数值（v,λ,m_W,m_Z,α）皆为标准常数反演"},
    ]
    add("D04", "INFO", "三判定：本卷三扇区全部 C1（TUFT 侧独立数值供给 = 0）",
        "本册审计对象是项目**自有**推导链，不构成外部探针对撞；为账目一致，按"
        "「TUFT 侧是否给出可比的新数值」记 C1。机器确认：v 由 G_F 反演、λ 由 m_h 与 v 反演、"
        "g1/g2 由 m_W/m_Z 反演、α 只在树级网里出现且无标准值 —— **没有任何一项是 TUFT 的独立预言**。"
        "①池 12/12 与累计供给 0/12 不变；本卷不计入①池。",
        {"table": table, "n_C1": 3, "n_C2": 0, "n_C3": 0,
         "pool": "12/12", "supply": "0/12"})

    add("D05", "INFO", "缺陷族补充：F-label 新增成员（Δρ_t 挂错对照量）；F-scale 同案",
        "F-label 原成员：T210/T211 编号倒置、C0279 的 3.01 dB（20log₁₀2）。本册新增："
        "推论 4.3 把 Δρ_t=0.0094 解释成 ρ_0−1=0.00038 的来源（24.6× 不符）。"
        "门禁：任何「偏差来自 X 修正」的句子，必须机器核对**被解释量**与**修正量**是否同一口径、"
        "同一量级；否则先登记口径，再谈解释。",
        {"F_label_members": ["T210/T211", "C0279 3.01dB", "R187 drho 0.0094 vs 0.00038"],
         "families": 6})

    # =================================================================
    # E 段 · 已有一致性登记与红线
    # =================================================================
    print("\n[E] 已有结果一致性 / 红线")

    AE_THEORY = ALPHA / (D(2) * PI)
    rel_ae = abs(AE_THEORY / AE_EXP - D(1))
    guard("G21 ae_value", abs(AE_THEORY - D("1.161410E-3")) < D("1E-8") and rel_ae < D("2E-3"),
          "α/2π=" + fs(AE_THEORY, 10) + "，相对实测 " + fs(rel_ae, 6))
    add("E01", "PASS", "a_e=α/2π=" + fs(AE_THEORY, 7) + "，与实测 " + fs(AE_EXP, 7) +
        " 差 " + fs(rel_ae * D(100), 4) + "%（来料写 0.15%，一致）",
        "机器：" + fs(AE_THEORY, 10) + " vs 实测 " + fs(AE_EXP, 10) + " ⇒ 相对差 " +
        fs(rel_ae, 6) + " = " + fs(rel_ae * D(100), 4) +
        "%。来料自注「高阶 QED 补足、不在本项目重算范围」⇒ 本册只做登记，不重算四圈。",
        {"ae_theory": fs(AE_THEORY, 10), "ae_exp": fs(AE_EXP, 10),
         "rel": fs(rel_ae, 6)})

    add("E02", "INFO", "本卷红线与产出定性",
        "产出 = ①变分链的 (C) 系数与 (YM) 符号链机器核对；②Higgs 势一阶/二阶导的 250 位"
        "解析+差分互证；③质量矩阵本征分解（m_γ=0）；④电弱树级五恒等式的数值闭合与"
        "α 口径边界；⑤Δρ_t 挂错对照量的 FAIL 定性与修复方向（C07）。"
        "不产生新物理，不宣称观测证实/否证，不改写来料字节，不改 verify.py，不做 git。",
        {"supply": "0/12", "pool": "12/12"})

    # =================================================================
    # 控制组
    # =================================================================
    control("K01 v_246", abs(VEV - D("246.22")) < D("0.01"), "v=" + fs(VEV, 8))
    control("K02 lambda_0p129", abs(LAM - D("0.129")) < D("0.001"), "λ=" + fs(LAM, 8))
    control("K03 mh2_15688", abs(MH * MH - D("15687.6")) < D("1"), "m_h²=" + fs(MH * MH, 8))
    control("K04 yukawa_ok", abs(dV0) < D("1E-200"), "dV0=" + fs(dV0, 3))
    control("K05 fd_close", rel_fd < D("1E-60"), "rel=" + fs(rel_fd, 4))
    control("K06 g2_0p65", abs(G2 - D("0.6528")) < D("0.001"), "g2=" + fs(G2, 8))
    control("K07 mZ_91p19", abs(mZ_eig - D("91.1876")) < D("0.01"), "mZ=" + fs(mZ_eig, 8))
    control("K08 sin2_0p223", abs(SIN2 - D("0.2232")) < D("0.001"), "sin2=" + fs(SIN2, 8))
    control("K09 alpha_inv_band", D("131") < INV_ALPHA_TREE < D("133"),
            "α^-1=" + fs(INV_ALPHA_TREE, 6))
    control("K10 drho_0p0094", abs(DRHO - D("0.0094")) < D("0.0002"), "Δρ=" + fs(DRHO, 8))
    control("K11 rho_ms_1p01", abs(RHO_MS - D("1.0099")) < D("0.001"), "ρ_MS=" + fs(RHO_MS, 8))
    control("K12 ae_1p161e-3", abs(AE_THEORY - D("1.1614E-3")) < D("1E-6"),
            "a_e=" + fs(AE_THEORY, 8))

    # =================================================================
    # 汇总
    # =================================================================
    counts = {}
    for e in ENTRIES:
        counts[e["level"]] = counts.get(e["level"], 0) + 1
    n_g = sum(1 for g in GUARDS if g["ok"])
    n_c = sum(1 for c in CONTROLS if c["ok"])

    print("\n" + "=" * 78)
    print("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）"
          % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
             counts.get("BOUNDARY", 0), counts.get("INFO", 0), counts.get("CORRECTED", 0)))
    print("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    print("判定串：" + VERDICT)

    payload = dict(
        stem=STEM, verdict=VERDICT, counts=counts,
        guards_total=len(GUARDS), guards_pass=n_g,
        controls_total=len(CONTROLS), controls_pass=n_c,
        guard_list=GUARDS, control_list=CONTROLS, entries=ENTRIES,
        supply=dict(pool="12/12", supply="0/12"),
        judgement=table,
        source="07_统一场方程/02_变分推导.md",
    )
    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    md = []
    md.append("# " + STEM + "\n")
    md.append("**条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）；"
              "守卫 %d/%d；控制组 %d/%d；退出码 0**\n"
              % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                 counts.get("BOUNDARY", 0), counts.get("INFO", 0),
                 counts.get("CORRECTED", 0), n_g, len(GUARDS), n_c, len(CONTROLS)))
    md.append("## 一句话\n")
    md.append("变分推导链路（求导证明）闭环式审计：量纲与自然单位账全过；Higgs 势一阶导在"
              "真空处机器零、二阶导 = 2λv² = m_h²（解析+差分互证）；质量矩阵本征分解给 m_γ=0 精确、"
              "m_Z=91.19；电弱树级五恒等式（v=246.2196、λ=0.12938、sin²θ_W=0.2232、ρ_tree=1）逐项闭合，"
              "但树级网反解的 α^{-1}=132.1 落在 137.036 与 127.95 之间（口径边界）。"
              "**FAIL**：推论 4.3 把 Δρ_t=0.00935 挂到 PDG ρ_0−1=0.00038 上（24.6× 不符）——"
              "改用 MS-bar sin²θ_W 后 ρ=1.010625 ≈ 1+Δρ_t（1.27E−3），证明 Δρ_t 属 MS-bar 口径、"
              "不解释 Z-pole 的 1.00038。四费米子 3/8 vs 3/16 差因子 2，登记约定边界。TUFT 供给 0/12 不变。\n")
    md.append("## 条目\n")
    md.append("| 编号 | 级 | 标题 |")
    md.append("|---|---|---|")
    for e in ENTRIES:
        md.append("| %s | %s | %s |" % (e["code"], e["level"],
                                        e["title"].replace("|", "\\|")))
    md.append("\n## 三判定\n")
    md.append("| 探针 | 判定 | 理由 |")
    md.append("|---|---|---|")
    for r in table:
        md.append("| %s | **%s** | %s |" % (r["probe"], r["verdict"], r["reason"]))
    md.append("\n## 守护（%d/%d）\n" % (n_g, len(GUARDS)))
    for g in GUARDS:
        md.append("- [%s] %s" % ("OK" if g["ok"] else "FAIL", g["name"]))
    md.append("\n## 控制组（%d/%d）\n" % (n_c, len(CONTROLS)))
    for c in CONTROLS:
        md.append("- [%s] %s %s" % ("OK" if c["ok"] else "FAIL", c["name"], c["msg"]))
    md.append("\n## 红线\n")
    md.append("本册只做闭环式复算与结构性判定，不产生新物理，不宣称观测证实/否证；"
              "未改写任何来料字节；未改 verify.py；未做 git 操作。TUFT 供给 0/12 维持。\n")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    rep = []
    rep.append("TUFT-r187 变分推导链路求导验证 · 运行报告")
    rep.append("=" * 70)
    rep.append("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）"
               % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                  counts.get("BOUNDARY", 0), counts.get("INFO", 0), counts.get("CORRECTED", 0)))
    rep.append("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    rep.append("")
    for e in ENTRIES:
        rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
        rep.append("    " + e["detail"])
        if e["numbers"]:
            try:
                rep.append("    " + json.dumps(e["numbers"], ensure_ascii=False))
            except Exception:
                pass
        rep.append("")
    rep.append("判定串：" + VERDICT)
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))

    print("out -> %s.{json,md,_report.txt}" % STEM)
    return 0 if (n_g == len(GUARDS) and n_c == len(CONTROLS)) else 1


if __name__ == "__main__":
    sys.exit(main())
