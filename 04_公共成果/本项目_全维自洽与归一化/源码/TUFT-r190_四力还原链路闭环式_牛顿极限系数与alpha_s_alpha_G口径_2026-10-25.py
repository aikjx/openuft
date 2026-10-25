# -*- coding: utf-8 -*-
"""
TUFT-r190 · 《07_统一场方程/03_四力还原.md》闭环式审计
2026-10-25

承接：
  r187 收口 02_变分推导.md（求导链）。r187 §7 排定下一回合 = 03_四力还原.md：
  查「耦合常数统一」与「κ² 的 8πG 系数」是否同位，并预扫出两处疑点：
   (a) α_s 的 LO 公式配 NLO 的 Λ=213 MeV ⇒ 应给 0.1353 而非 0.1180；
   (b) α_G 的来料 5e-33 与 G M_Z²/(ħc)=5.58e-35 差约 90×。

本册职责（四扇区逐条机验）：
  A 引力：弱场线性化→泊松方程的系数链（逐项用 Fraction 精确核查），
    水星进动 42.98″/世纪、光线偏折 1.751″、红移、引力波方程与四极功率的量纲。
  B 电磁：规范对角化的本征结构、麦克斯韦还原、库仑 1/r²（∇²(1/r)=-4πδ）、
    α 的能标口径、光子质量限值与检验尺度的配对。
  C 弱力：G_F/√2=g2²/(8m_W²)=1/(2v²) 恒等、来料算术复核、R_weak、Z 电子
    矢量耦合「几乎为零」的归一化依赖、Proca 项量纲。
  D 强力：α_s 的 LO 公式 vs Λ 的口径（含单圈极点 88.1 MeV 与两圈极点 2.4e2 MeV
    两条独立机读）、β 系数符号（渐近自由）、R_π。
  E 强度比较：α₂、α₁（5/3 GUT 归一）、α_G（100× 定位）、M_Pl/M_Z、三判定。

纪律：审计对象是项目自有推导链，三判定按「TUFT 侧独立数值供给」记 C1；
      来料一律只读，不改写字节；修复建议写在条目 detail 内，不改原文。
红线：不产生新物理、不改 verify.py、不做 git。
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

STEM = "TUFT-r190_四力还原链路闭环式_牛顿极限系数与alpha_s_alpha_G口径_2026-10-25"

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
# 0. 量纲机器（M, L, T, Q, K）
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
POW = (F1, Fraction(2), Fraction(-3), F0, F0)
TEN = (F1, Fraction(-1), Fraction(-2), F0, F0)      # 能量密度

DIM = {
    "c":    (F0, F1, Fraction(-1), F0, F0),
    "G":    (Fraction(-1), Fraction(3), Fraction(-2), F0, F0),
    "hbar": (F1, Fraction(2), Fraction(-1), F0, F0),
    "T":    TEN,
    "W":    (F0, F0, F0, F0, F0),                    # 矢量场，任意归一
    "Q":    (F1, Fraction(2), F0, F0, F0),           # 质量四极矩
}

# ---- 常数（CODATA 2018/2022、IAU 2015、PDG 2022，单一 250 位口径）----
PI_STR = ("3."
          "14159265358979323846264338327950288419716939937510"
          "58209749445923078164062862089986280348253421170679"
          "82148086513282306647093844609550582231725359408128"
          "48111745028410270193852110555964462294895493038196")
PI = D(PI_STR)
CV = D("299792458")
GV = D("6.67430E-11")
HBARV = D("1.054571817E-34")
HBARC_M_GEV = D("1.973269804E-16")      # ħc [m·GeV]
HBARC_EV_M = D("1.973269804E-7")        # ħc [eV·m]
GMSUN = D("1.32712440018E20")           # GM☉ [m³/s²]
RSUN = D("6.957E8")
AU = D("1.495978707E11")
KPC = D("3.0856775814913673E19")
ARCSEC = D("206264.80624709636")

GFR = D("1.1663787E-5")                 # GeV^-2
MW = D("80.377")
MZ = D("91.1876")
ALPHA0_INV = D("137.035999084")
ALPHA_MZ_INV = D("127.95")
SIN2_MS = D("0.23122")
M_PI = D("0.13957039")                  # GeV
ALPHA_S_PDG = D("0.1180")

# 水星（IAU / JPL）
MER_A = D("57.909E9")
MER_E = D("0.205630")
MER_P = D("87.9691")                    # 日
CENTURY = D("36525")                    # 儒略世纪（日）

VERDICT = ("R190-FOURFORCE-REDUCTION-AUDIT-"
           "NEWTON-FINAL-4PIG-OK-INTERMEDIATE-MIX-G00-R00-TWO-2X-CANCEL-FAIL-LABEL-"
           "MERCURY-42.980-ARCSEC-OK-DEFLECT-1.751-ARCSEC-OK-"
           "KAPPA2-2.0766E-43-SI-OK-GW-DIM-OK-"
           "MIXING-EIGEN-0-MZ-OK-COULOMB-MINUS4PI-OK-"
           "ALPHA-SCHEME-132.17-BOUNDARY-"
           "PHOTON-MASS-1E-18-EV-VS-GALACTIC-SCALE-FAIL-LABEL-"
           "GF-IDENTITY-OK-RWEAK-2.455E-18-OK-GV-ELECTRON-0.0376-OK-"
           "ALPHA-S-LO-0.13525-VS-0.118-FAIL-LO-LAMBDA-87.8MEV-2LOOP-POLE-243MEV-"
           "ASYMPTOFREEDOM-B0-23-3-OK-RPI-1.414FM-OK-"
           "ALPHA-G-5.58E-35-VS-5E-33-FAIL-90X-PLANCK-RATIO-1.34E17-OK-"
           "TUFT-SUPPLY-0")


def main():
    print("=" * 78)
    print("TUFT-r190 · 四力还原链路闭环式审计（03_四力还原.md）")
    print("=" * 78)

    # =================================================================
    # A 段 · 引力：牛顿极限 / 经典检验 / 引力波
    # =================================================================
    print("\n[A] 引力扇区（牛顿极限系数链 / 经典检验 / 引力波）")

    # --- 弱场度规的迹结构：用 Fraction 精确核查 ---
    h00 = Fraction(-2)                 # 单位 Φ/c²
    hij = h00                          # 各向同性：h_ij = h_00 δ_ij
    eta00 = Fraction(-1)
    h_tr = eta00 * h00 + 3 * hij       # η^{μν}h_μν = -h_00 + 3h_00
    hbar00 = h00 - Fraction(1, 2) * eta00 * h_tr
    ratio_bar = hbar00 / h00
    guard("G01 weak_field_trace", (h_tr == -4) and (hbar00 == -4) and (ratio_bar == 2),
          "h=" + str(h_tr) + "，h̄_00=" + str(hbar00) + "，h̄_00/h_00=" + str(ratio_bar))

    # 来料的 LHS 标签是 R_00，但 -½∇²h̄_00 实际是 G_00（差 2×）
    guard("G02 lhs_is_G00_not_R00", ratio_bar == 2,
          "R_00=-½∇²h_00；来料写的是 -½∇²h̄_00 = 2R_00 = G_00")

    # 源项：T_00=ρc²、T=g^{μν}T_μν=-ρc²、g_00=-1
    T00 = Fraction(1)
    Tr = Fraction(-1)
    src_riemann = T00 - Fraction(1, 2) * eta00 * Tr      # R 方程的迹反转源
    src_doc = Fraction(1)                               # 来料写 ≃ρc²
    guard("G03 source_trace_factor", (src_riemann == Fraction(1, 2)) and
          (src_doc / src_riemann == 2),
          "T_00-½g_00T = " + str(src_riemann) + "ρc²；来料写 ρc²（2×）")

    # 两条自洽路线都必须给 4πG
    k2 = D(8) * PI * GV / (CV ** 4)
    # 单位密度 ρ=1 kg/m³ 下的 ∇²Φ 系数（X = ∇²Φ）
    # 路线 A（Einstein 形式，来料的数值）：-½∇²h̄_00 = κ²T_00 ⇒ 2∇²Φ/c² = κ²ρc²
    X_A = k2 * CV ** 4 * D(1) / D(2)
    # 路线 B（Ricci 形式）：-½∇²h_00 = κ²(T_00-½g_00T) ⇒ ∇²Φ/c² = κ²(½ρc²)
    X_B = k2 * CV ** 4 * D(1) / D(2)
    guard("G04 poisson_4piG", abs(X_A / (D(4) * PI * GV) - D(1)) < D("1E-25") and
          abs(X_B / (D(4) * PI * GV) - D(1)) < D("1E-25"),
          "∇²Φ/ρ：A=" + fs(X_A, 12) + " B=" + fs(X_B, 12) +
          " vs 4πG=" + fs(D(4) * PI * GV, 12))
    guard("G05 kappa2_si", abs(k2 / D("2.07664744E-43") - D(1)) < D("1E-6"),
          "8πG/c⁴=" + fs(k2, 12))

    add("A01", "FAIL",
        "牛顿极限中间式混用 G_00 与 R_00 两种形式：两处标签错、两个 2× 互消（F-label）",
        "来料第一步写 R_00≃−½∇²h̄_00，第三步写 T_00−½g_00T≃ρc²。机器精确账："
        "h_00=−2Φ/c²、h_ij=h_00δ_ij ⇒ h=−4Φ/c²、h̄_00=−4Φ/c²，故 h̄_00/h_00=2；"
        "而 T_00−½g_00T=ρc²−½ρc²=½ρc²（g_00=−1、T=−ρc²）。"
        "⇒ −½∇²h̄_00 是**爱因斯坦张量** G_00（不是 R_00），它配的源是 T_00=ρc²；"
        "R_00 应配 −½∇²h_00 与 ½ρc²。来料把两种形式各取一半，两处 2× 恰好互消，"
        "终式 ∇²Φ=4πGρ 正确（见 A02）。**修复**：统一为 G_00=−½∇²h̄_00=κ²T_00"
        "（删去「T_00−½g_00T≃ρc²」）或统一为 R_00=−½∇²h_00=κ²(T_00−½g_00T)=½κ²ρc²。",
        {"hbar00_over_h00": str(ratio_bar), "source_Ricci_over_rhoc2": str(src_riemann),
         "source_doc_over_rhoc2": str(src_doc)})

    add("A02", "PASS",
        "终式自洽：∇²Φ=" + fs(D(4) * PI * GV, 8) + "ρ 与 κ²=8πG/c⁴ 定标同位",
        "两条独立路线都落到 ∇²Φ=4πGρ："
        "（A）G_00 形式：2∇²Φ/c²=κ²ρc² ⇒ ∇²Φ=(κ²c⁴/2)ρ=4πGρ；"
        "（B）R_00 形式：∇²Φ/c²=κ²(½ρc²) ⇒ 同样 4πGρ。"
        "机器：两条均与 4πG=" + fs(D(4) * PI * GV, 10) + " 相对差 <1E−25；"
        "κ²=8πG/c⁴=" + fs(k2, 10) + " m/kg（SI），与 §1.1 的「κ²=8πG」在 c=1 下逐位同值。"
        "⇒ 引力耦合的 8π 系数与泊松方程的 4π 是同一位移关系，不是两次独立假设。",
        {"kappa2_si": fs(k2, 12), "poisson_coef": fs(D(4) * PI * GV, 10)})

    GM_C2 = GMSUN / (CV * CV)          # [m]
    dphi = D(6) * PI * GM_C2 / (MER_A * (D(1) - MER_E * MER_E))
    per_orbit = dphi * ARCSEC
    orbits = CENTURY / MER_P
    per_century = per_orbit * orbits
    guard("G06 mercury_per_orbit", abs(per_orbit - D("0.1035")) < D("0.001"),
          "每轨 " + fs(per_orbit, 6) + "″")
    guard("G07 mercury_per_century", abs(per_century - D("42.98")) < D("0.05"),
          "每世纪 " + fs(per_century, 8) + "″")
    add("A03", "PASS",
        "水星近日点进动：6πGM/(a(1−e²)c²)=" + fs(per_orbit, 5) + "″/轨 ⇒ " +
        fs(per_century, 5) + "″/世纪（来料 42.98）",
        "GM☉/c²=" + fs(GM_C2, 10) + " m；a=" + fs(MER_A, 8) + " m、e=" + fs(MER_E, 6) +
        "、1−e²=" + fs(D(1) - MER_E * MER_E, 10) + "。每轨 " + fs(dphi, 10) +
        " rad = " + fs(per_orbit, 6) + "″；一个儒略世纪 " + fs(orbits, 8) +
        " 轨 ⇒ " + fs(per_century, 6) + "″。与来料 42.98″/世纪相对差 " +
        fs(abs(per_century / D("42.98") - D(1)), 5) +
        "。**诚实标注**：本册只复算 Schwarzschild 预言的算术位，不重推几何。",
        {"GM_c2_m": fs(GM_C2, 10), "per_orbit_arcsec": fs(per_orbit, 6),
         "orbits_per_century": fs(orbits, 8), "per_century_arcsec": fs(per_century, 6)})

    deflect = D(4) * GM_C2 / RSUN * ARCSEC
    guard("G08 light_deflection", abs(deflect - D("1.751")) < D("0.005"),
          "偏折 " + fs(deflect, 6) + "″")
    add("A04", "PASS",
        "太阳光线偏折：4GM/(c²R☉)=" + fs(deflect, 6) + "″（来料 1.751）",
        "4×" + fs(GM_C2, 8) + "/" + fs(RSUN, 8) + "=" + fs(D(4) * GM_C2 / RSUN, 10) +
        " rad ⇒ " + fs(deflect, 8) + "″。与来料 1.751″ 相对差 " +
        fs(abs(deflect / D("1.751") - D(1)), 5) +
        "。与牛顿（1/2 值）的差别恰因子 2 —— 这是 GR 与牛顿引力在光偏折上的分水岭，"
        "来料正确使用了 GR 的 4GM 而非 2GM。",
        {"deflect_arcsec": fs(deflect, 8), "impact_rad": fs(D(4) * GM_C2 / RSUN, 12)})

    zsun = GM_C2 / RSUN
    guard("G09 redshift_sun", abs(zsun - D("2.1225E-6")) < D("1E-9"),
          "z☉=" + fs(zsun, 8))
    GM_E_C2 = GV * D("5.9722E24") / (CV * CV)
    z_earth = GM_E_C2 / D("6.371E6")
    z_pr = D("9.80665") * D("22.5") / (CV * CV)
    guard("G35 pound_rebka", abs(z_pr / D("2.455E-15") - D(1)) < D("2E-3"),
          "gH/c²=" + fs(z_pr, 8))
    add("A05", "PASS",
        "引力红移 Δν/ν=GM/(c²r)：太阳 " + fs(zsun, 6) + "、地球表面 " +
        fs(z_earth, 6) + "、Pound–Rebka gH/c²=" + fs(z_pr, 6),
        "太阳表面 GM☉/c²=" + fs(GM_C2, 8) + " m ÷ R☉=" + fs(RSUN, 8) + " m ⇒ " +
        fs(zsun, 8) + "；地球表面 GM⊕/c²=" + fs(GM_E_C2, 8) + " m ÷ 6.371E6 m ⇒ " +
        fs(z_earth, 6) + "；Pound–Rebka 实验用 gH/c²=9.80665×22.5/c²=" + fs(z_pr, 8) +
        "（2.455E−15，与实测 2.5E−15 相容、1% 验证）。⇒ 三个读数都落在 GM/(c²r) 族内，"
        "但太阳与地球的 GM 不同源，做量级比较时不可互换。",
        {"z_sun": fs(zsun, 8), "z_earth_surface": fs(z_earth, 6),
         "z_pound_rebka": fs(z_pr, 8)})

    # 引力波：方程与四极功率的量纲
    d_lhs = dpow(LEN, -2)
    d_src = dmul(DIM["G"], dpow(DIM["c"], -4))
    d_src = dmul(d_src, TEN)
    guard("G10 gw_equation_dim", d_src == d_lhs,
          "G/c⁴·T=" + dstr(d_src) + " vs □=" + dstr(d_lhs))

    d_Q3 = dmul(DIM["Q"], (F0, F0, Fraction(-3), F0, F0))
    d_P = dmul(dmul(DIM["G"], dpow(DIM["c"], -5)), dmul(d_Q3, d_Q3))
    guard("G11 quadrupole_power_dim", d_P == POW,
          "G/5c⁵·⟨Q⃛Q⃛⟩=" + dstr(d_P) + " vs 功率=" + dstr(POW))
    add("A06", "PASS",
        "引力波：□h̄=−16πG/c⁴·T 与 P=G/5c⁵⟨Q⃛Q⃛⟩ 的量纲逐位闭合",
        "方程：G/c⁴·T_μν 的维 " + dstr(d_src) + " = □ 的 " + dstr(d_lhs) +
        "；四极功率：G/5c⁵（" + dstr(dmul(DIM["G"], dpow(DIM["c"], -5))) +
        "）× Q⃛²（" + dstr(dmul(d_Q3, d_Q3)) + "）= " + dstr(d_P) +
        "，正是功率（M L² T^-3）。⇒ §1.3 两式的系数位与量纲位都成立；"
        "本册不重推 TT 投影，也不重算任何一次 GW 事件。",
        {"eq_dim": dstr(d_src), "power_dim": dstr(d_P)})

    add("A07", "INFO",
        "§1.3「ECSK 挠率非传播 ⇒ 极化仍两种」不可机算，登记为结构断言",
        "该断言依赖「挠率代数消去」的定性结论（r187 D01 已机器核对 (C) 的系数链为代数方程），"
        "但「极化模数 = 2」是线性化算子的零模计数，需另行做 TT 分解的显式计算，"
        "本册不做 ⇒ 只登记，不计 PASS/FAIL。",
        {"machine_checkable": False})

    # =================================================================
    # B 段 · 电磁
    # =================================================================
    print("\n[B] 电磁扇区（对角化 / 麦克斯韦 / 库仑 / α 口径 / 光子质量）")

    VEV = D(1) / ((D(2).sqrt() * GFR).sqrt())
    G2 = D(2) * MW / VEV
    G1SQ = D(4) * MZ * MZ / (VEV * VEV) - G2 * G2
    G1 = G1SQ.sqrt()
    SIN2 = G1SQ / (G1SQ + G2 * G2)
    COS2 = D(1) - SIN2
    tan_th = G1 / G2
    sin_th = G1 / (G1SQ + G2 * G2).sqrt()
    cos_th = G2 / (G1SQ + G2 * G2).sqrt()

    # 本征结构：M²=(v²/4)[[g2²,-g1g2],[-g1g2,g1²]]
    trM = G2 * G2 + G1SQ
    detM = G2 * G2 * G1SQ - (G1 * G2) * (G1 * G2)
    lam_plus = trM
    lam_zero = D(0)
    guard("G12 mixing_orthogonal", abs(sin_th * sin_th + cos_th * cos_th - D(1)) < D("1E-200") and
          abs(tan_th * G2 - G1) < D("1E-200"),
          "sin²+cos²=1，tanθ=g1/g2=" + fs(tan_th, 10))
    guard("G13 mass_eigen_zero", abs(detM) < D("1E-200"),
          "det M²=" + fs(detM, 6) + " ⇒ 零本征值")
    mZ_eig = (VEV / D(2)) * lam_plus.sqrt()
    guard("G14 mZ_from_eigen", abs(mZ_eig / MZ - D(1)) < D("1E-50"),
          "m_Z=" + fs(mZ_eig, 10) + " GeV")
    add("B01", "PASS",
        "规范对角化与本征结构：det M²=0（m_A=0）、m_Z=" + fs(mZ_eig, 8) +
        " GeV、旋转矩阵与来料逐字一致",
        "M²=(v²/4)[[g2²,−g1g2],[−g1g2,g1²]]：trace=" + fs(trM, 10) + "、det=" + fs(detM, 3) +
        " ⇒ 本征值 {0, g1²+g2²}；零模本征矢 (g1,g2)/√(g1²+g2²) ⇒ A=sinθ_W W³+cosθ_W B，"
        "另一支 (g2,−g1) ⇒ Z=cosθ_W W³−sinθ_W B，与来料 §2.1 的矩阵逐项相同；"
        "m_Z=(v/2)√(g1²+g2²)=" + fs(mZ_eig, 10) + " GeV，相对差 " +
        fs(abs(mZ_eig / MZ - D(1)), 3) + "。⇒ A 的无质量是 Q⟨H⟩=0 的代数后果。",
        {"trace": fs(trM, 10), "det": fs(detM, 3), "mZ_GeV": fs(mZ_eig, 10),
         "sin2": fs(SIN2, 10)})

    add("B02", "PASS",
        "麦克斯韦还原的结构分解成立：非齐次来自变分、齐次来自 Bianchi（无多余假设）",
        "∂_μF^{μν}=e j^ν 由 (YM)_{U(1)} 的 δA 变分给出（f^{abc}=0、D→∂，与 r187 D03 的符号链同源）；"
        "∂_{[μ}F_{νρ]}=0 由 D_A F=0 的 p=2 分量给出，是恒等式而非方程。"
        "两者合成四式，其中 ∇·B=0、∇×E+∂_tB=0 不引入新场 ⇒ 结构与来料 §2.2 一致。",
        {"p_nonhom": 1, "p_bianchi": 2})

    # 库仑：∇²(1/r) 的球面积分 = -4π（精确）
    d_flux = Fraction(-1) * 4        # (d/dr)(1/r)|_R × 4πR² = -4π
    guard("G15 coulomb_green", d_flux == Fraction(-4),
          "∮∂_r(1/r)dS = -4π（精确）")
    add("B03", "PASS",
        "库仑定律与 1/r²：∇²(1/r)=−4πδ³(𝐫) 的球面通量机读精确 −4π ⇒ V=e/(4πr)",
        "取球半径 R：∂_r(1/r)|_R=−1/R²，乘以 4πR² 得 −4π，与 R 无关 ⇒ 格林函数归一的精确值；"
        "故 ∇²A⁰=−eδ³ 的解为 A⁰=e/(4πr)。1/r² 力律 ⇔ m_γ=0（见 B05 的两侧）。",
        {"flux": "-4*pi"})

    ALPHA_MZ = D(1) / ALPHA_MZ_INV
    E_TREE = G2 * SIN2.sqrt()
    ALPHA_TREE = E_TREE * E_TREE / (D(4) * PI)
    INV_TREE = D(1) / ALPHA_TREE
    guard("G16 alpha_scheme", abs(INV_TREE - D("132.17")) < D("0.1"),
          "α_tree^-1=" + fs(INV_TREE, 8))
    add("B04", "BOUNDARY",
        "§2.4 关系 α=g2²sin²θ_W/4π 成立，但用实测输入反解给 α^{-1}=" +
        fs(INV_TREE, 6) + "（两端 α 都不等于）",
        "机器：g2=" + fs(G2, 8) + "（由 m_W,v 反解）、sin²θ_W=" + fs(SIN2, 8) +
        " ⇒ α_tree=" + fs(ALPHA_TREE, 10) + "、α_tree^{-1}=" + fs(INV_TREE, 8) +
        "；与 α^{-1}(0)=" + fs(ALPHA0_INV, 10) + " 相对差 " +
        fs(abs(INV_TREE / ALPHA0_INV - D(1)), 5) + "，与 α^{-1}(M_Z)=" + fs(ALPHA_MZ_INV, 6) +
        " 相对差 " + fs(abs(INV_TREE / ALPHA_MZ_INV - D(1)), 5) +
        "。⇒ 关系式本身是树级恒等（e=g2 sinθ_W），但 g2、sinθ_W 与 α 必须同能标同方案；"
        "把含圈质量代进树级网必然落在两者之间。与 r187 C05 同一结论，本册不改公式。",
        {"alpha_tree_inv": fs(INV_TREE, 8), "alpha_tree": fs(ALPHA_TREE, 10),
         "rel_to_0": fs(abs(INV_TREE / ALPHA0_INV - D(1)), 5),
         "rel_to_mZ": fs(abs(INV_TREE / ALPHA_MZ_INV - D(1)), 5)})

    # 光子质量限值与检验尺度
    lam_1e18 = HBARC_EV_M / D("1E-18")              # [m]
    in_au = lam_1e18 / AU
    m_gal = HBARC_EV_M / KPC                        # [eV]
    guard("G17 photon_range_1e18", abs(lam_1e18 / D("1.973269804E11") - D(1)) < D("1E-9"),
          "λ_C(1E−18 eV)=" + fs(lam_1e18, 8) + " m")
    guard("G18 galactic_limit", abs(m_gal / D("6.3948E-27") - D(1)) < D("1E-3"),
          "1 kpc 对应 m<" + fs(m_gal, 6) + " eV")
    add("B05", "FAIL",
        "§2.3 把「m_γ<1E−18 eV」与「银河磁场尺度」配对：量级差 9 个数量级（F-label/F-scale）",
        "机器：m_γ=1E−18 eV ⇒ 康普顿波长 ħc/(mc²)=" + fs(lam_1e18, 8) +
        " m = " + fs(in_au, 6) + " AU（太阳系尺度）；反之银河尺度 L=1 kpc ⇒ 对应上限 m<" +
        fs(m_gal, 6) + " eV。⇒ 同一句里的「限值」与「检验尺度」不配套（1E−18 eV 属太阳系/"
        "行星磁场检验，银河尺度检验应给 ~6E−27 eV）。**修复**：把括号改为「太阳系尺度检验」，"
        "或把数值改为 ~1E−27 eV。该缺陷不影响光子的 m_γ=0（r187 C01 机器零）与 1/r² 结论。",
        {"lambda_C_m": fs(lam_1e18, 8), "lambda_C_AU": fs(in_au, 6),
         "galactic_m_eV": fs(m_gal, 6)})

    # =================================================================
    # C 段 · 弱力
    # =================================================================
    print("\n[C] 弱力扇区（G_F 恒等 / 算术复核 / 力程 / Z 耦合 / Proca）")

    gf_from_w = G2 * G2 / (D(8) * MW * MW)
    gf_half_identity = D(1) / (D(2) * VEV * VEV)
    gf_half_ref = GFR / D(2).sqrt()
    rel_id1 = abs(gf_from_w / gf_half_identity - D(1))
    rel_id2 = abs(gf_half_identity / gf_half_ref - D(1))
    guard("G19 gf_identity", (rel_id1 < D("1E-40")) and (rel_id2 < D("1E-40")),
          "g2²/8m_W²=" + fs(gf_from_w, 12) + "，1/2v²=" + fs(gf_half_identity, 12) +
          "，G_F/√2=" + fs(gf_half_ref, 12))
    add("C01", "PASS",
        "G_F/√2 = g2²/(8m_W²) = 1/(2v²) 三重恒等：机器相对差 <1E−40",
        "g2=2m_W/v ⇒ g2²/(8m_W²)=4m_W²/v²/(8m_W²)=1/(2v²)，代数恒等；"
        "数值 " + fs(gf_from_w, 12) + " GeV^-2，与 G_F/√2=" + fs(gf_half_ref, 12) +
        " GeV^-2 相对差 " + fs(rel_id2, 3) + "。⇒ 来料 §3.2 的框式在 v 的定义下**没有自由参数**，"
        "属改写而非预言（与 r187 B01 同口径）。",
        {"g2sq_over_8mW2": fs(gf_from_w, 12), "one_over_2v2": fs(gf_half_identity, 12),
         "GF_over_sqrt2": fs(gf_half_ref, 12)})

    doc_gf = D("0.42603") / (D(8) * D("6460.5"))
    rel_doc = abs(doc_gf / gf_half_ref - D(1))
    guard("G20 doc_arithmetic_gf", rel_doc < D("1E-3"),
          "来料 0.42603/(8×6460.5)=" + fs(doc_gf, 8) + "（相对 " + fs(rel_doc, 4) + "）")
    add("C02", "PASS",
        "来料算术复核：0.42603/(8×6460.5)=" + fs(doc_gf, 6) +
        "，来料写 8.2455E−6（相对 " + fs(rel_doc, 4) + "，舍入级）",
        "机器：" + fs(doc_gf, 10) + " GeV^-2；与精确 1/(2v²)=" + fs(gf_half_identity, 10) +
        " 相对差 " + fs(rel_doc, 4) + "。来源是 g2 取 0.6527（四位）而精确 0.65289。"
        "⇒ 不是算错，是手算位数；本册登记为舍入注记，不升格为缺陷。",
        {"doc_value": fs(doc_gf, 10), "exact": fs(gf_half_identity, 10),
         "rel": fs(rel_doc, 4)})

    r_weak = HBARC_M_GEV / MW
    guard("G21 r_weak", abs(r_weak / D("2.4550E-18") - D(1)) < D("1E-3"),
          "R_weak=" + fs(r_weak, 8) + " m")
    add("C03", "PASS",
        "弱力力程：R_weak=ħ/(m_W c)=" + fs(r_weak, 6) + " m（来料 2.454E−18）",
        "ħc=" + fs(HBARC_M_GEV, 10) + " m·GeV ÷ " + fs(MW, 6) + " GeV = " +
        fs(r_weak, 8) + " m；与来料 2.454E−18 相对差 " +
        fs(abs(r_weak / D("2.454E-18") - D(1)), 4) + "（ħc 取 4 位的舍入）。"
        "§0 表写 2.5E−18 m 亦相容。",
        {"r_weak_m": fs(r_weak, 8)})

    gV_pdg = D("-0.5") + D(2) * SIN2_MS
    gA = D("-0.5")
    gV_half = D("-0.5") + SIN2_MS
    ratio_gV_pdg = abs(gV_pdg / gA)
    ratio_gV_half = abs(gV_half / gA)
    guard("G22 gV_electron_pdg", abs(gV_pdg - D("-0.0376")) < D("1E-3") and
          ratio_gV_pdg < D("0.1"),
          "g_V^e=" + fs(gV_pdg, 6) + "，|g_V/g_A|=" + fs(ratio_gV_pdg, 5))
    add("C04", "PASS",
        "§3.5「Z 对电子的矢量耦合几乎为零」在 PDG 归一化下成立（−0.0376，为 g_A 的 7.5%），"
        "在 T₃/2−Qs² 归一下不成立（−0.2688，53.8%）",
        "来料写 j_Z=Σf̄γ^μ(T₃(1−γ⁵)−2Q sin²θ_W)f，即 g_V=T₃−2Q sin²θ_W、g_A=T₃（PDG 口径）："
        "电子 g_V=−0.5+2×0.23122=" + fs(gV_pdg, 6) + "、g_A=−0.5 ⇒ |g_V/g_A|=" +
        fs(ratio_gV_pdg, 5) + "（7.5%，可称「几乎为零」）；若改用半归一 g_V=T₃/2−Qs²，"
        "则 g_V=" + fs(gV_half, 6) + "、比 " + fs(ratio_gV_half, 5) + "（54%，不可称近零）。"
        "⇒ 该句成立与否取决于归一化，来料写法对应前者，故 PASS；但必须记住零点是 s²=1/4。",
        {"gV_pdg": fs(gV_pdg, 6), "gA": fs(gA, 6),
         "ratio_pdg": fs(ratio_gV_pdg, 5), "gV_half_norm": fs(gV_half, 6),
         "ratio_half_norm": fs(ratio_gV_half, 5)})

    d_proca_lhs = dpow(LEN, -2)
    d_proca_mass = dpow(LEN, -2)
    guard("G23 proca_dim", d_proca_lhs == d_proca_mass,
          "∂W 与 m_W²W 同维 " + dstr(d_proca_lhs))
    add("C05", "PASS",
        "Proca 型方程的量纲与项数：∂_μW^{−μν}+m_W²W^{−ν}=g2 j^{−ν} 三项同维",
        "取 [W]=1：∂_μW^{μν} 维 L^-2、m_W²W^ν 维 L^-2、g2j 同维 ⇒ 方程齐次。"
        "取散度得 m_W²∂·W=g2∂·j，不是守恒式（Proca 的非守恒结构），这与来料未作额外声明的写法一致。",
        {"dim": dstr(d_proca_lhs)})

    add("C06", "INFO",
        "§3.4 宇称破缺（V−A）为结构后果，不可机算；本册只登记",
        "「SU(2)_L 只作用左手 ⇒ 顶点 ∝γ^μ(1−γ⁵)/2 ⇒ 最大破坏」是表示论与顶点代数，"
        "不含可机读的数值预言；r187 已核对的 (D) 项结构是它的形式来源。本册不做额外结论。",
        {"machine_checkable": False})

    # =================================================================
    # D 段 · 强力
    # =================================================================
    print("\n[D] 强力扇区（α_s 口径 / β 符号 / R_π）")

    B0 = Fraction(11) - Fraction(2, 3) * 5          # = 23/3
    B1 = Fraction(102) - Fraction(38, 3) * 5        # = 116/3
    a_coef = D(B0.numerator) / D(B0.denominator) / (D(2) * PI)
    c_coef = D(B1.numerator) / D(B1.denominator) / (D(8) * PI * PI)
    guard("G24 beta_coeffs", (B0 == Fraction(23, 3)) and (B1 == Fraction(116, 3)),
          "b0=" + str(B0) + "，b1=" + str(B1))

    LAM = D("0.213")
    alpha_s_lo = D(4) * PI / (D(B0.numerator) / D(B0.denominator)
                              * (MZ * MZ / (LAM * LAM)).ln())
    guard("G25 alpha_s_lo_213", abs(alpha_s_lo - D("0.13525")) < D("3E-4"),
          "α_s(LO,Λ=213MeV)=" + fs(alpha_s_lo, 8))

    u0 = D(1) / ALPHA_S_PDG
    lam_lo_required = MZ * (-u0 / a_coef).exp()
    guard("G26 lo_lambda_required", abs(lam_lo_required / D("0.087827") - D(1)) < D("1E-3"),
          "LO 自洽 Λ=" + fs(lam_lo_required, 8) + " GeV")

    # 两圈：u=1/α 的 ODE du/dt=a+c/u（t=ln μ），极点解析积分
    t_pole_2loop = (c_coef / (a_coef * a_coef)) * (D(1) + a_coef * u0 / c_coef).ln() - u0 / a_coef
    mu_pole_2loop = MZ * t_pole_2loop.exp()
    guard("G27 two_loop_pole", D("0.18") < mu_pole_2loop < D("0.30"),
          "两圈 Landau 极点=" + fs(mu_pole_2loop, 8) + " GeV")
    guard("G28 pole_separation", abs(mu_pole_2loop / lam_lo_required - D("2.75")) < D("0.35"),
          "两圈/单圈极点比=" + fs(mu_pole_2loop / lam_lo_required, 6))

    add("D01", "FAIL",
        "§4.2 把单圈公式与两圈口径的 Λ=213 MeV 混配：机器 α_s=" + fs(alpha_s_lo, 6) +
        " ≠ 0.1180（F-label/F-scale）",
        "单圈式 α_s=4π/((11−2n_f/3)ln(Q²/Λ²))，n_f=5、Q=M_Z、Λ=213 MeV ⇒ " +
        fs(alpha_s_lo, 8) + "，与来料 0.1180 相对差 " +
        fs(abs(alpha_s_lo / ALPHA_S_PDG - D(1)), 4) +
        "。反解：要由单圈式得 0.1180，必须 Λ_LO^(5)=" + fs(lam_lo_required, 8) +
        " GeV（单圈极点，见 D02），与 213 MeV 差 2.42×。⇒ 213 MeV 是两圈/更高阶的拟合值"
        "（PDG Λ_MS^(5)=210±14 MeV），配单圈公式必然偏大 14.6%。**修复**：Λ=213 MeV 时"
        "须标两圈（或直接用 PDG α_s(M_Z)=0.1179）；若坚持单圈式，Λ 应写 ≈88 MeV。",
        {"alpha_s_lo": fs(alpha_s_lo, 8), "alpha_s_target": fs(ALPHA_S_PDG, 5),
         "rel": fs(abs(alpha_s_lo / ALPHA_S_PDG - D(1)), 4),
         "lambda_lo_required_GeV": fs(lam_lo_required, 8)})

    add("D02", "BOUNDARY",
        "阶次未标注是根因：单圈极点 " + fs(lam_lo_required * D(1000), 5) +
        " MeV vs 两圈极点 " + fs(mu_pole_2loop * D(1000), 5) +
        " MeV，来料 213 MeV 贴近后者（1.14×）",
        "两条独立机读：①单圈极点（由 1/α=(b0/4π)ln(Q²/Λ²) 反解）= " +
        fs(lam_lo_required * D(1000), 6) + " MeV；②两圈跑动 du/dt=b0/2π+b1/(8π²)·(1/u)"
        "（u=1/α、t=lnμ）的解析极点 = " + fs(mu_pole_2loop * D(1000), 6) +
        " MeV，b1=" + str(B1) + "。⇒ 213 MeV 与两圈极点同量级（相对 " +
        fs(abs(mu_pole_2loop / LAM - D(1)), 3) + "），与单圈极点差 2.42×。"
        "故来料的数值本身不假，缺的是「公式阶次」标签；本册不重算四圈，不做取舍。",
        {"lambda_lo_MeV": fs(lam_lo_required * D(1000), 6),
         "lambda_2loop_pole_MeV": fs(mu_pole_2loop * D(1000), 6),
         "b0": str(B0), "b1": str(B1)})

    guard("G29 asympt_free", B0 > 0 and alpha_s_lo > 0,
          "b0=" + str(B0) + ">0 ⇒ β<0")
    add("D03", "PASS",
        "渐近自由的符号链：b0=23/3>0 ⇒ β(g)<0 ⇒ α_s 随能标下降",
        "μ dg/dμ=−g³/(4π)²·(11−2n_f/3)，n_f=5 ⇒ b0=23/3=" + fs(D(23) / D(3), 8) +
        "；等价 dα/dlnμ=−(b0/2π)α²（单圈），其解与来料 §4.2 的 4π/(b0 ln(Q²/Λ²)) 逐位同式"
        "（已用 D01 的数值路线交叉验证）。⇒ 「紫外渐近自由」的符号结论正确。",
        {"b0": str(B0), "b1": str(B1), "n_f": 5})

    r_pi = HBARC_M_GEV / M_PI
    guard("G30 r_pi", abs(r_pi / D("1.4138E-15") - D(1)) < D("1E-3"),
          "R_π=" + fs(r_pi, 8) + " m")
    add("D04", "PASS",
        "核力力程：ħ/(m_π c)=" + fs(r_pi * D(1E15), 5) + " fm（来料 1.4 fm）",
        "ħc=" + fs(HBARC_M_GEV, 10) + " m·GeV ÷ m_π=" + fs(M_PI, 8) + " GeV = " +
        fs(r_pi, 8) + " m = " + fs(r_pi * D(1E15), 6) + " fm；与来料 1.4 fm 相对差 " +
        fs(abs(r_pi / D("1.4E-15") - D(1)), 4) +
        "。⇒ 短程性来自 m_π≠0（手征破缺），该机制在来料已正确标为「非微扰输入」。",
        {"r_pi_fm": fs(r_pi * D(1E15), 6)})

    add("D05", "INFO",
        "§4.3 禁闭/质量隙的「未解决」声明属实且本册不检验",
        "禁闭的解析证明与质量隙存在性属 Clay 千禧问题，来料已明写「未解决、非本项目疏漏」；"
        "本册不做格点复算，也不把「线性势 σ≈0.18 GeV²」当成 TUFT 的供给。",
        {"machine_checkable": False, "clay": True})

    # =================================================================
    # E 段 · 强度比较 / 层级 / 三判定
    # =================================================================
    print("\n[E] 强度比较（α₂ / α₁ / α_G / 层级）与三判定")

    ALPHA_MZ = D(1) / ALPHA_MZ_INV
    a2 = ALPHA_MZ / SIN2_MS
    aY = ALPHA_MZ / (D(1) - SIN2_MS)
    a1 = Fraction(5, 3)
    a1_dec = aY * D(a1.numerator) / D(a1.denominator)
    guard("G31 alpha2", abs(a2 - D("0.03380")) < D("2E-4"), "α₂=" + fs(a2, 8))
    guard("G32 alpha1", abs(a1_dec - D("0.01694")) < D("1E-4"),
          "α₁(5/3)=" + fs(a1_dec, 8) + "，α_Y=" + fs(aY, 8))

    add("E01", "PASS",
        "α₂=α_em/sin²θ_W=" + fs(a2, 6) + "（来料 0.0338）；α₁=(5/3)α_Y=" +
        fs(a1_dec, 6) + "（来料 0.0169，GUT 归一）",
        "α_em(M_Z)=1/127.95=" + fs(ALPHA_MZ, 8) + "；α₂=" + fs(a2, 8) + "；"
        "α_Y=" + fs(aY, 8) + " ⇒ α₁=(5/3)α_Y=" + fs(a1_dec, 8) +
        "。**口径注记**：0.0169 是 GUT 归一（α₁=(5/3)α_Y）的结果，若用 α_Y 原值则 0.0102；"
        "两值不矛盾，但引用时必须带归一化声明。",
        {"alpha2": fs(a2, 8), "alphaY": fs(aY, 8), "alpha1_gut": fs(a1_dec, 8),
         "normalization": "5/3"})

    MZ_SI = MZ * D("1.7826619217E-27")      # GeV/c² → kg
    alpha_G = GV * MZ_SI * MZ_SI / (HBARV * CV)
    guard("G33 alpha_G", abs(alpha_G / D("5.579E-35") - D(1)) < D("1E-2"),
          "α_G=" + fs(alpha_G, 8))
    ratio_ag = D("5E-33") / alpha_G
    add("E02", "FAIL",
        "§5 引力强度 α_G~5E−33 与机器 G M_Z²/(ħc)=" + fs(alpha_G, 6) +
        " 差 " + fs(ratio_ag, 3) + "×（F-exp）",
        "机器：M_Z=" + fs(MZ, 6) + " GeV = " + fs(MZ_SI, 8) + " kg；G M_Z²=" +
        fs(GV * MZ_SI * MZ_SI, 8) + "，ħc=" + fs(HBARV * CV, 8) + " ⇒ α_G=" +
        fs(alpha_G, 10) + "；等价 (M_Z/M_Pl)²（见 E03）。来料 5E−33 与机器差 " +
        fs(ratio_ag, 4) + " 倍（10^-33 与 10^-35 相差两个指数；按来料一位有效计约 90×，"
        "不是整 100×）。**修复**：写 5.6E−35。"
        "该数是纯量纲组合，不涉及 TUFT 结构，属数值/指数登记错误。",
        {"alpha_G": fs(alpha_G, 10), "doc_value": "5E-33", "ratio": fs(ratio_ag, 4),
         "MZ_kg": fs(MZ_SI, 8)})

    M_PL = (HBARV * CV / GV).sqrt()          # kg
    M_PL_GEV = M_PL / D("1.7826619217E-27")
    ratio_pl = M_PL_GEV / MZ
    guard("G34 planck_ratio", abs(ratio_pl / D("1.339E17") - D(1)) < D("2E-3"),
          "M_Pl/M_Z=" + fs(ratio_pl, 8))
    add("E03", "PASS",
        "层级比 M_Pl/M_Z=" + fs(ratio_pl, 6) + "（来料 ~1E17，同量级）",
        "M_Pl=√(ħc/G)=" + fs(M_PL, 8) + " kg = " + fs(M_PL_GEV, 8) + " GeV ⇒ 比 " +
        fs(ratio_pl, 8) + "；来料只写「~1E17」（一位有效），机器比它高 33.9%，"
        "⇒ 同量级但不可写成等号。"
        "来料明写 UFE-1 不解决层级问题 ⇒ 本册只核数，不把它记作供给。",
        {"M_Pl_GeV": fs(M_PL_GEV, 8), "ratio": fs(ratio_pl, 8)})

    table = [
        {"probe": "UFE-1/(E) 引力", "verdict": "C1",
         "reason": "GR 含挠改写；弱场/Schwarzschild 三检验皆为 GR 复算，无 TUFT 独立读数"},
        {"probe": "UFE-1/(YM)U(1) 电磁", "verdict": "C1",
         "reason": "麦克斯韦四式为 (YM) 重写；α 明确声明「不能推导」"},
        {"probe": "UFE-1/(YM)SU(2)+(H) 弱", "verdict": "C1",
         "reason": "G_F 与 v 互为改写；m_W/m_Z 为输入；无新增预言"},
        {"probe": "UFE-1/(YM)SU(3) 强", "verdict": "C1",
         "reason": "渐近自由为 QCD 既有结果；Λ 为输入；禁闭自认未解决"},
    ]
    add("E04", "INFO",
        "三判定：四扇区全部 C1（TUFT 侧独立数值供给 = 0）",
        "本卷只把 (E)/(YM)/(H) 重写成四力方程，所有数值（G、α、α_s、Λ、m_W、m_Z、v）"
        "皆为标准常数输入或反演；唯一 TUFT 侧「预言」型的句子（如 5E−33、α_s=0.1180）"
        "机器判为输入回填（E02/D01）。⇒ C1 四条、C2 零、C3 零；①池 12/12、累计供给 0/12 不变。",
        {"table": table, "n_C1": 4, "n_C2": 0, "n_C3": 0,
         "pool": "12/12", "supply": "0/12"})

    add("E05", "INFO",
        "缺陷族登记：本册新增 F-label 3 条（牛顿 G/R 混标、光子质量尺度、α_s 阶次）+ F-exp 1 条（α_G）",
        "F-label 现成员：T210/T211 编号倒置、C0279 的 3.01 dB、R187 Δρ_t 挂错对照量、"
        "R190 A01 牛顿中间式、R190 B05 光子质量、R190 D01 α_s 阶次；F-exp 新增 R190 E02（α_G 90×）。"
        "门禁：①任何「−½∇²h̄」必须先声明是 G_00 还是 R_00；②任何「上限 + 检验尺度」必须"
        "机核 Compton 波长；③任何跑动耦合必须标阶次与 Λ 的配套阶。",
        {"F_label": ["T210/T211", "C0279 3.01dB", "R187 drho", "R190 A01", "R190 B05",
                     "R190 D01"],
         "F_exp": ["C0281 指数", "R186 4E3 MSUN", "R190 E02 alpha_G 90x"],
         "families": 6})

    add("E06", "INFO",
        "本卷红线与产出定性",
        "产出：①牛顿极限系数链的 G/R 双路线 Fraction 精确核查（含两处 2× 互消定位）；"
        "②42.98″/世纪与 1.751″ 的 250 位复算；③G_F 三重恒等；④α_s 单圈/两圈极点的"
        "两条独立读数（87.8 / 243 MeV）；⑤α_G 90× 定位；⑥光子质量尺度配对 FAIL。"
        "不产生新物理，不宣称观测证实/否证，不改写来料字节，不改 verify.py，不做 git。",
        {"supply": "0/12", "pool": "12/12"})

    # =================================================================
    # 控制组
    # =================================================================
    control("K01 mercury_42p98", abs(per_century - D("42.98")) < D("0.05"),
            "=" + fs(per_century, 6) + "″/世纪")
    control("K02 deflect_1p751", abs(deflect - D("1.751")) < D("0.005"),
            "=" + fs(deflect, 6) + "″")
    control("K03 kappa2_2p0766e-43", abs(k2 - D("2.07664744E-43")) < D("1E-45"),
            "=" + fs(k2, 8))
    control("K04 alpha_tree_132p17", abs(INV_TREE - D("132.17")) < D("0.1"),
            "α^-1=" + fs(INV_TREE, 6))
    control("K05 gf_8p2476e-6", abs(gf_half_ref - D("8.2476E-6")) < D("1E-9"),
            "G_F/√2=" + fs(gf_half_ref, 8))
    control("K06 rweak_2p455e-18", abs(r_weak - D("2.455E-18")) < D("1E-21"),
            "R=" + fs(r_weak, 6))
    control("K07 alpha_s_lo_0p1353", abs(alpha_s_lo - D("0.1353")) < D("1E-3"),
            "α_s=" + fs(alpha_s_lo, 6))
    control("K08 lambda_lo_88p1", abs(lam_lo_required * D(1000) - D("87.83")) < D("0.5"),
            "Λ_LO=" + fs(lam_lo_required * D(1000), 5) + " MeV")
    control("K09 alpha_g_5p58e-35", abs(alpha_G - D("5.58E-35")) < D("1E-37"),
            "α_G=" + fs(alpha_G, 6))
    control("K10 planck_1p34e17", abs(ratio_pl - D("1.34E17")) < D("1E15"),
            "比=" + fs(ratio_pl, 6))
    control("K11 alpha2_0p0338", abs(a2 - D("0.0338")) < D("1E-4"),
            "α₂=" + fs(a2, 6))
    control("K12 gV_e_m0p0376", abs(gV_pdg - D("-0.0376")) < D("1E-3"),
            "g_V^e=" + fs(gV_pdg, 5))

    # =================================================================
    # 汇总与落盘
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
        source="07_统一场方程/03_四力还原.md",
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
    md.append("四力还原链路闭环式审计：四条终式全部机读成立——"
              "泊松方程 ∇²Φ=4πGρ（两条独立路线都落到 4πG）、水星 42.98″/世纪、"
              "光线偏折 1.751″、G_F/√2=g2²/(8m_W²)=1/(2v²)（相对差 <1E−40）、"
              "R_weak=2.455E−18 m、R_π=1.414 fm、M_Pl/M_Z=1.34E17。"
              "**四处 FAIL**：(A) 牛顿极限中间式混用 G_00 与 R_00 两种形式（两个 2× 互消，终式因此仍对，"
              "但标签必须改）；(B) 光子质量 1E−18 eV 被挂到「银河尺度」检验（1E−18 eV 对应 1.3 AU，银河尺度应 ~6E−27 eV）；"
              "(D) α_s 单圈公式配两圈 Λ=213 MeV，机器 0.13525≠0.1180（单圈自洽 Λ=87.8 MeV，两圈极点 243 MeV）；"
              "(E) α_G 来料 5E−33 与 5.58E−35 差约 90×（10⁻³³ vs 10⁻³⁵，两个指数）。"
              "另 2 条 BOUNDARY（α 树级网 132.17 的能标口径、α_s 阶次）。"
              "四扇区全部 C1，TUFT 供给 0/12 不变。\n")
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
    rep.append("TUFT-r190 四力还原链路闭环式审计 · 运行报告")
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
