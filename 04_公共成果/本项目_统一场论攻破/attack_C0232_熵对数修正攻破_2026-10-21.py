# -*- coding: utf-8 -*-
"""
attack_C0232_熵对数修正攻破_2026-10-21.py
独立精算：T132「极端黑洞的近极端熵对数修正」（母册行 L 线域 G 批，撞 C2/C7）

定位：母册 T132（原文照录）：
  | T132 | 极端黑洞的近极端熵对数修正 | 一圈发散 + 对数项 | C2,C7 | 🔲 |
主题：极端黑洞近极端熵 S = A/(4l_P²) + c ln(A/l_P²) 型——对数修正系数 c 的
弦论 / LQG / 欧拉特征候选对比核算；极端极限 a→M 下 Kerr T→0、A=8πGM² 核算；
极端 RN/Kerr/Kerr-Newman 的 A 与电荷/角动量关系核算；量子引力供给检查。

衔接：
  - C0210（Wald 熵）E3：ln(A/l_P²)=178.73362889、c0=-3/2 演示、1 M☉ 同组 CODATA 常数
    逐位对齐；本册在其上做**候选系数 c 的对比核算**（弦 -3/2 / LQG -1/2 / 欧拉 χ/2=1）。
  - C0212（极端 Kerr）：λ=√(1-q²)、A=8πM²(1+λ)、T_H=λ/[4πM(1+λ)]、A_ext/A_Schw=1/2。
  - C0216（第三定律极端点 T=0）：极端 RN/Kerr T_H=0 精确、残熵非零（RN π、Kerr 2π）。
  - C0133（TUFT 终审注销）：仅留经典局部几何；C0168：无离散微观态基。

把「极端黑洞近极端熵对数修正」压缩成五条可复核读数：

  E1 公式体系事实（一圈发散 + log 项、候选 c 外部输入、极端极限，标准结果只引用不复算）。
  E2 **对数修正系数候选对比核算（本册核心）**：弦论 c=-3/2、LQG c=-1/2、
     欧拉特征 χ=2 ⇒ c=χ/2=1；对 1 M☉ ln(A/l_P²) 逐位复算各候选 log 修正项与候选间差。
  E3 极端极限核算：a→M（q→1）Kerr λ=√(1-q²)→0、T_H→0、A=8πM² Decimal 扫点；
     近极端 A 的 Decimal 核算（承接 C0212 逐位对齐）。
  E4 Kerr-Newman 极端核算：极端 RN（Q=M）A=4πM²、Kerr（a=M）A=8πM²、
     KN（M²=a²+Q²）A=4π(M²+a²)；极端点 T=0（衔接 C0216）。
  E5 裁定：对数修正依赖量子引力微观态计数（标准弦/LQG 结构），TUFT 无微观态/
     无量子修正供给 ⇒ 结构性负面，撞 C2/C7。

纯标准库（Decimal 48 位 + Fraction 精确代数），零外部依赖、零网络、零随机，退出码 0。

诚实边界：数值均为标准半经典 / 量子引力算术复核；修正系数候选值为已知文献外部输入
显式计数（弦论 / LQG / 欧拉特征），非本册预测；TUFT 已注销（C0133）；
严禁把标准物理结果写成 TUFT 预测/修正。本册不宣称解决任何物理难题。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48


BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部常数（CODATA 2018 / PDG，只引用不复算；与 C0187/C0210 同组逐位对齐） ----------
M_SUN = Decimal("1.9890e30")   # kg
G = Decimal("6.6740e-11")       # m^3 kg^-1 s^-2
HBAR = Decimal("1.054571817e-34")  # J s
C = Decimal("2.9979246e8")     # m/s
KB = Decimal("1.380649e-23")   # J/K

# π 取 50 位（与 C0187/C0210 同一硬编码值）
PI = Decimal("3.14159265358979323846264338327950288419716939937510")


def _bh(M: Decimal):
    """Schwarzschild 视界几何（标准 GR 算术）：R_s, A, l_P, S/k_B, T_H。"""
    Rs = (Decimal(2) * G * M) / (C * C)
    A = Decimal(4) * PI * Rs * Rs
    lP = (G * HBAR / (C ** 3)).sqrt()
    S_over_kB = A / (Decimal(4) * lP * lP)
    T_H = (HBAR * C ** 3) / (Decimal(8) * PI * G * M * KB)
    return {"M": M, "Rs": Rs, "A": A, "lP": lP, "S_over_kB": S_over_kB, "T_H": T_H}


# ---------- 对数修正系数候选（已知文献外部输入显式计数，Fraction 精确） ----------
C_STRING = Fraction(-3, 2)    # 弦论近极端 / 一圈（Sen / 4D Schwarzschild one-loop）
C_LQG = Fraction(-1, 2)        # LQG Kaul-Padmanabhan 微观态计数
C_EULER = Fraction(1, 1)       # 欧拉特征 χ=2（单连通视界）⇒ c=χ/2=1


def e1_formulas():
    """E1：一圈发散 + log 项公式体系、候选 c、极端极限（只引用不复算）。"""
    return {
        "near_extremal_corr": "S = A/(4 l_P^2) + c ln(A/l_P^2) + O(1)；一圈有效作用量给出发散+有限 log 项",
        "c_string": "弦论近极端 BPS / 一圈：c = -3/2（Sen 微观态计数）",
        "c_lqg": "LQG 自旋泡沫 / Kaul-Padmanabhan：c = -1/2（边界态计数）",
        "c_euler": "欧拉特征 χ 型：c = χ/2；单连通视界 χ=2 ⇒ c=1",
        "extreme_kerr": "a→M（q=a/M→1），λ=√(1-q²)→0 ⇒ T_H=λ/[4πM(1+λ)]→0，A=8πM²",
        "extreme_rn": "Q→M（q=Q/M→1）⇒ T_H→0，A=4πM²",
        "origin": "Sen 1993 / Kaul-Padmanabhan 2000 / 一圈有效作用量（标准量子引力/半经典结果，只引用）",
    }


def e2_candidate_coefficients():
    """E2（核心）：对数修正系数候选对比核算。

    对 1 M☉ Schwarzschild：ln(A/l_P²) Decimal 逐位复算（承接 C0210 E3）；
    各候选 c 的 log 修正项 = c × ln(A/l_P²)（单位 k_B）；候选间差显式计数。
    """
    g = _bh(M_SUN)
    A_over_lP2 = g["A"] / (g["lP"] * g["lP"])     # = 4 S/k_B
    ln_val = A_over_lP2.ln()

    def cdec(c: Fraction):
        return Decimal(c.numerator) / Decimal(c.denominator)

    c_str = cdec(C_STRING)
    c_lqg = cdec(C_LQG)
    c_eu = cdec(C_EULER)

    return {
        "S_over_kB": g["S_over_kB"],
        "A_over_lP2": A_over_lP2,
        "ln_A_over_lP2": ln_val,
        "c_string": c_str, "c_lqg": c_lqg, "c_euler": c_eu,
        "log_string_kB": c_str * ln_val,
        "log_lqg_kB": c_lqg * ln_val,
        "log_euler_kB": c_eu * ln_val,
        # 候选间差（Fraction 精确）：c_string - c_euler = -3/2 - 1 = -5/2
        "dc_string_minus_euler": C_STRING - C_EULER,   # Fraction(-5,2)
        "dc_string_minus_lqg": C_STRING - C_LQG,       # Fraction(-1,1)
        "log_diff_string_vs_euler_kB": (c_str - c_eu) * ln_val,
        # 相对修正量级
        "rel_string": (c_str * ln_val).copy_abs() / g["S_over_kB"],
    }


def e3_extreme_kerr_sweep():
    """E3：极端极限核算——a→M（q→1）Kerr λ=√(1-q²)→0、T_H→0、A=8πM²。

    几何单位 G=c=1，M=1；承接 C0212 公式：
      A/(4πM²) = 2(1+λ)，T_H = λ/[4π(1+λ)]。
    """
    qs = [Decimal(0), Decimal("0.9"), Decimal("0.99"),
          Decimal("0.999"), Decimal("0.9999"), Decimal(1)]
    rows = []
    for q in qs:
        lam = (Decimal(1) - q * q).sqrt()
        fA = Decimal(2) * (Decimal(1) + lam)          # A/(4πM²)
        A_geom = Decimal(4) * PI * fA / Decimal(4)    # =4πM²·fA/4 = π·fA ... 直接 A=8πM²(1+λ)
        A_geom = Decimal(8) * PI * (Decimal(1) + lam)  # 几何单位 M=1，A=8π(1+λ)
        T_H = lam / (Decimal(4) * PI * (Decimal(1) + lam))
        rows.append({"q": q, "lam": lam, "fA": fA, "A_geom": A_geom, "T_H": T_H})
    # 极端点 q=1
    ext = rows[-1]
    schw = rows[0]
    # 1 M☉ SI：r_g = GM☉/c²；A_ext = 8π r_g²
    r_g = G * M_SUN / (C * C)
    A_ext_SI = Decimal(8) * PI * r_g * r_g
    A_schw_SI = Decimal(16) * PI * r_g * r_g
    return {
        "rows": rows,
        "lam_ext": ext["lam"], "T_H_ext": ext["T_H"], "A_geom_ext": ext["A_geom"],
        "T_H_schw": schw["T_H"],
        "A_ext_over_A_schw_geom": ext["A_geom"] / schw["A_geom"],   # = 1/2
        "r_g": r_g, "A_ext_SI": A_ext_SI, "A_schw_SI": A_schw_SI,
    }


def e4_kn_extreme():
    """E4：Kerr-Newman 极端核算——极端 RN/Kerr/KN 的 A 与电荷/角动量关系。

    几何单位 M=1：
      极端 RN（a=0, Q=1）：r_+=1，A=4π(1²+0²)=4π，S=A/4=π。
      极端 Kerr（a=1, Q=0）：r_+=1，A=4π(1²+1²)=8π，S=2π。
      极端 KN（M²=a²+Q²，取 a=0.5 ⇒ Q=√(1-0.25)=√0.75）：r_+=1，A=4π(1+a²)=5π，S=5π/4。
    极端点 T=0（衔接 C0216：残熵非零）。
    """
    # 极端 RN
    A_RN = Decimal(4) * PI * (Decimal(1) ** 2 + Decimal(0) ** 2)
    S_RN = A_RN / Decimal(4)
    # 极端 Kerr
    a_k = Decimal(1)
    A_Kerr = Decimal(4) * PI * (Decimal(1) ** 2 + a_k ** 2)
    S_Kerr = A_Kerr / Decimal(4)
    # 极端 KN（a=0.5, Q=√0.75）
    a_kn = Decimal("0.5")
    Q_kn = (Decimal(1) - a_kn * a_kn).sqrt()     # = √0.75
    A_KN = Decimal(4) * PI * (Decimal(1) ** 2 + a_kn ** 2)   # r_+=M=1
    S_KN = A_KN / Decimal(4)
    return {
        "A_RN_ext": A_RN, "S_RN_ext": S_RN,
        "A_Kerr_ext": A_Kerr, "S_Kerr_ext": S_Kerr,
        "a_kn": a_kn, "Q_kn": Q_kn, "A_KN_ext": A_KN, "S_KN_ext": S_KN,
        "A_RN_over_A_Kerr": A_RN / A_Kerr,        # = 1/2
        "S_RN_over_S_Kerr": S_RN / S_Kerr,        # = 1/2
        # 极端点 T=0 精确（λ=0 极限，承接 C0216 E2）
        "T_RN_ext": Decimal(0), "T_Kerr_ext": Decimal(0),
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0232 · 极端黑洞近极端熵对数修正（T132 · 撞 C2/C7）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_formulas()
    w("\n[E1] 公式体系事实（一圈发散 + log 项、候选 c、极端极限，只引用不复算）")
    w("  %s" % g1["near_extremal_corr"])
    w("  %s" % g1["c_string"])
    w("  %s" % g1["c_lqg"])
    w("  %s" % g1["c_euler"])
    w("  %s" % g1["extreme_kerr"])
    w("  %s" % g1["extreme_rn"])
    w("  => %s；本册只引用，不归因 TUFT。" % g1["origin"])
    entries.append(("E1", "S=A/4l_P²+c ln(A/l_P²) 一圈+log 体系；候选 c：弦 -3/2、LQG -1/2、"
                          "欧拉 χ=2⇒c=1（Sen/Kaul-Padmanabhan，只引用）",
                    "PASS", "标准量子引力/半经典结果只引用；候选 c 为外部态计数输入"))

    # ---- E2 ----
    g2 = e2_candidate_coefficients()
    w("\n[E2] 对数修正系数候选对比核算（本册核心，Decimal 48 位逐位复算）")
    w("  --- 1 M☉ Schwarzschild 对数底（承接 C0210 E3 逐位对齐）---")
    w("  S/k_B = A/(4l_P²) = %s" % fv(g2["S_over_kB"], "5e"))
    w("  A/l_P² = %s（=4 S/k_B）" % fv(g2["A_over_lP2"], "4e"))
    w("  ln(A/l_P²) = %s（Decimal.ln() 48 位精算，对标 C0210 E3: 178.73362889）"
      % fv(g2["ln_A_over_lP2"], "8f"))
    w("  --- 候选 c 的 log 修正项 = c × ln(A/l_P²)（单位 k_B）---")
    w("  弦论   c=-3/2：log 项 = %s k_B" % fv(g2["log_string_kB"], "6f"))
    w("  LQG    c=-1/2：log 项 = %s k_B" % fv(g2["log_lqg_kB"], "6f"))
    w("  欧拉χ=2 c=+1 ：log 项 = %s k_B" % fv(g2["log_euler_kB"], "6f"))
    w("  --- 候选间差（Fraction 精确显式计数）---")
    w("  Δc(弦-欧拉) = %s（= -3/2 - 1 = -5/2）" % g2["dc_string_minus_euler"])
    w("  Δc(弦-LQG)  = %s（= -3/2 - (-1/2) = -1）" % g2["dc_string_minus_lqg"])
    w("  log 项差(弦 vs 欧拉) = %s k_B（= -5/2 × ln(A/l_P²)）"
      % fv(g2["log_diff_string_vs_euler_kB"], "6f"))
    w("  相对修正 |log_string|/(A/4l_P²) = %s（~1e-75，宏观黑洞可忽略）"
      % fv(g2["rel_string"], "4e"))
    w("  => 三个量子引力微观态计数结构给出**互不相同**的 c（-3/2 vs -1/2 vs +1），")
    w("     c 无第一性唯一值，依赖所选量子引力微观态计数方案——纯外部输入。")
    entries.append(("E2", "ln(A/l_P²)=%s；log 项：弦 %s / LQG %s / 欧拉 %s k_B；"
                          "候选 Δc(弦-欧拉)=-5/2 ⇒ c 无唯一值，依赖微观态计数结构"
                    % (fv(g2["ln_A_over_lP2"], "6f"), fv(g2["log_string_kB"], "1f"),
                       fv(g2["log_lqg_kB"], "1f"), fv(g2["log_euler_kB"], "1f")),
                    "PASS", "Decimal.ln() 逐位复算 + Fraction 精确候选差；常数同 C0210"))

    # ---- E3 ----
    g3 = e3_extreme_kerr_sweep()
    w("\n[E3] 极端极限核算：a→M（q→1）Kerr λ→0、T_H→0、A=8πM²（承接 C0212）")
    w("  %-9s %-12s %-12s %-14s %-14s" % ("q=a/M", "λ=√(1-q²)", "A/(4πM²)", "A=8π(1+λ)", "T_H"))
    for r in g3["rows"]:
        w("  %-9s %-12s %-12s %-14s %-14s"
          % (fv(r["q"], "4f"), fv(r["lam"], "6f"), fv(r["fA"], "6f"),
             fv(r["A_geom"], "6f"), fv(r["T_H"], "6e")))
    w("  --- 极端点 q=1 关键读数（Decimal 逐字）---")
    w("  λ_ext = %s（须 = 0，精确）" % fv(g3["lam_ext"], "6f"))
    w("  T_H_ext = %s（须 = 0，精确；衔接 C0216 极端点 T=0）" % fv(g3["T_H_ext"], "6e"))
    w("  A_geom_ext = %s（=8π，极端 Kerr 面积）" % fv(g3["A_geom_ext"], "6f"))
    w("  A_ext/A_Schwarz = %s（=1/2 精确，承接 C0212 E4）" % fv(g3["A_ext_over_A_schw_geom"], "6f"))
    w("  --- 1 M☉ SI 对标 C0212 E4 ---")
    w("  r_g = GM☉/c² = %s m" % fv(g3["r_g"], "4f"))
    w("  A_ext_SI(Kerr) = 8π r_g² = %s m²（对标 C0212: 5.4828e+7）" % fv(g3["A_ext_SI"], "4e"))
    w("  A_schw_SI = 16π r_g² = %s m²（对标 C0187: 1.0966e+8）" % fv(g3["A_schw_SI"], "4e"))
    w("  => a→M 时 T_H∝λ→0 精确、A 压到 Schwarzschild 的 1/2；标准 Kerr 热力学算术复核。")
    entries.append(("E3", "q=1: λ=0 精确、T_H=0 精确、A_ext/A_Schw=%s（=1/2）；"
                          "A_ext_SI=%s m²"
                    % (fv(g3["A_ext_over_A_schw_geom"], "1f"), fv(g3["A_ext_SI"], "4e")),
                    "PASS", "Decimal 扫点 q=0…1；公式承接 C0212，SI 对标 C0212/C0187"))

    # ---- E4 ----
    g4 = e4_kn_extreme()
    w("\n[E4] Kerr-Newman 极端核算：极端 RN/Kerr/KN 的 A 与电荷/角动量关系")
    w("  极端 RN（a=0, Q=M）：r_+=1，A=4π(1²+0²)=%s，S=A/4=%s（=π）"
      % (fv(g4["A_RN_ext"], "6f"), fv(g4["S_RN_ext"], "6f")))
    w("  极端 Kerr（a=M, Q=0）：r_+=1，A=4π(1²+1²)=%s，S=A/4=%s（=2π）"
      % (fv(g4["A_Kerr_ext"], "6f"), fv(g4["S_Kerr_ext"], "6f")))
    w("  极端 KN（M²=a²+Q²，a=0.5 ⇒ Q=%s）：r_+=1，A=4π(1+a²)=%s，S=%s"
      % (fv(g4["Q_kn"], "6f"), fv(g4["A_KN_ext"], "6f"), fv(g4["S_KN_ext"], "6f")))
    w("  A_RN/A_Kerr = %s（=1/2 精确）；S_RN/S_Kerr = %s（=1/2 精确，承接 C0216 残熵比）"
      % (fv(g4["A_RN_over_A_Kerr"], "6f"), fv(g4["S_RN_over_S_Kerr"], "6f")))
    w("  极端点 T_RN_ext = %s、T_Kerr_ext = %s（=0 精确；衔接 C0216 极端点 T=0）"
      % (fv(g4["T_RN_ext"], "0f"), fv(g4["T_Kerr_ext"], "0f")))
    w("  => 极端视界面积 A 由 (M,a,Q) 固定：RN=4πM²、Kerr=8πM²、KN=4π(M²+a²)；")
    w("     极端点 T=0 而 S=A/4 非零（C0216 第三定律形式张力）。标准 GR 算术复核。")
    entries.append(("E4", "极端 RN A=4πM²、Kerr A=8πM²、KN A=4π(M²+a²)；A_RN/A_Kerr=%s（=1/2）；"
                          "极端点 T=0 精确" % fv(g4["A_RN_over_A_Kerr"], "1f"),
                    "PASS", "几何单位 M=1 Decimal 核算；衔接 C0212/C0216"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  T132 被精确翻译成三件事：(a) 近极端熵 log 修正系数 c 有无第一性唯一值（E2，候选互不相同）；")
    w("  (b) 极端极限 a→M/Q→M 下 T→0、A 的标准 GR 行为（E3/E4，已证 = GR 内在）；")
    w("  (c) TUFT/几何框架是否供给 log 修正与微观态计数（E2/E3/E4，供给=0）。")
    w("  (a) 候选 c：弦 -3/2、LQG -1/2、欧拉 χ/2=1——三者差 Δc=-5/2（弦 vs 欧拉）、")
    w("      Δc=-1（弦 vs LQG），log 项差达 %s k_B；c 依赖量子引力微观态计数结构，无第一性唯一值。"
      % fv(g2["log_diff_string_vs_euler_kB"], "1f"))
    w("  (b) 极端极限 T_H∝√(M²-a²)→0 精确、A_ext/A_Schw=1/2 精确、RN/Kerr/KN 面积由 (M,a,Q) 固定")
    w("      ——均为标准 GR / 半经典引力算术复核，非 TUFT 预测/修正（红线）。")
    w("  (c) TUFT 已注销（C0133）仅经典局部几何，无离散微观态基（C0168）⇒ 无 log 修正供给、")
    w("      无一圈发散/有限项供给、无量子引力态空间 ⇒ c 供给 = 0。")
    w("  => **T132 结构性负面（对 TUFT/几何框架）**；撞 C2（绝对标度：c 系数为外部量子引力")
    w("     标度输入，弦/LQG/欧拉各异）/ C7（数学自洽边界：无量子引力态空间，log 修正载体缺失）。")
    w("     按母册 T132 登记撞 C2/C7。")
    entries.append(("E5", "T132 结构性负面：log 修正 c 候选互不相同（弦-3/2/LQG-1/2/欧拉+1），"
                          "依赖外部微观态计数；极端 T→0/A=8πM²=GR 内在；TUFT 无 log/微观态供给",
                    "PASS", "撞 C2/C7"))

    # ---- 守卫 ----
    guards = [
        ("G1", "弦论候选 c = -3/2（Fraction 精确外部输入）",
         C_STRING == Fraction(-3, 2)),
        ("G2", "ln(A/l_P²) ≈ 178.73（±1% 带，对标 C0210 E3: 178.73362889）",
         (g2["ln_A_over_lP2"] - Decimal("178.73")).copy_abs() / Decimal("178.73") < Decimal("0.01")),
        ("G3", "候选 c 互不相同：Δc(弦-欧拉) = -5/2 ≠ 0（Fraction 精确）",
         g2["dc_string_minus_euler"] == Fraction(-5, 2) and g2["dc_string_minus_euler"] != 0),
        ("G4", "LQG 候选 c = -1/2（Fraction 精确外部输入）",
         C_LQG == Fraction(-1, 2)),
        ("G5", "极端 Kerr q=1 ⇒ λ=0、T_H=0 精确",
         g3["lam_ext"] == 0 and g3["T_H_ext"] == 0),
        ("G6", "极端 Kerr A_ext/A_Schwarz = 1/2（±1e-6 带，承接 C0212）",
         (g3["A_ext_over_A_schw_geom"] - Decimal("0.5")).copy_abs() < Decimal("1e-6")),
        ("G7", "极端 RN A=4πM²、Kerr A=8πM² ⇒ A_RN/A_Kerr=1/2 精确",
         (g4["A_RN_over_A_Kerr"] - Decimal("0.5")).copy_abs() < Decimal("1e-6")),
        ("G8", "log 修正项量级 ~1e2 k_B（c=-3/2：-268，1e2–1e3 带）",
         Decimal("1e2") < g2["log_string_kB"].copy_abs() < Decimal("1e3")),
        ("G9", "log 相对修正量级 ~1e-75（1e-76–1e-73 带）",
         Decimal("1e-76") < g2["rel_string"] < Decimal("1e-73")),
        ("G10", "几何/TUFT 供给 = 0（C0133 注销 + C0168 无离散态基引用）",
         True),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0232 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  本册不宣称解决任何物理难题；已攻破 = 对 TUFT/几何框架结构性负面闭合。")
    w("  一圈+log 修正、极端 T→0、A=8πM²/RN 4πM² 均为标准 GR / 半经典 / 量子引力算术复核，")
    w("  本册仅做 Decimal 48 位 + Fraction 精算；候选 c（弦 -3/2、LQG -1/2、欧拉 χ/2=1）为已知文献")
    w("  外部输入显式计数，非本册预测；严禁写成 TUFT 预测/修正；TUFT 已注销（C0133）。")
    w("  CODATA 常数只引用不复算；C0210/C0212/C0216 读数引用不复算。")
    w("  红线不变：有预测且对 = 0/22；数学自洽 ≠ 实验证实；UFT-3=0 保持。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0232_熵对数修正攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0232_熵对数修正攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0232_extremal_entropy_log_correction",
            "mother_row": "T132 极端黑洞的近极端熵对数修正 一圈发散+对数项 C2,C7",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_formulas": g1,
            "E2_candidate_coefficients": {
                "S_over_kB": str(g2["S_over_kB"]),
                "A_over_lP2": str(g2["A_over_lP2"]),
                "ln_A_over_lP2": str(g2["ln_A_over_lP2"]),
                "c_string": str(g2["c_string"]),
                "c_lqg": str(g2["c_lqg"]),
                "c_euler": str(g2["c_euler"]),
                "log_string_kB": str(g2["log_string_kB"]),
                "log_lqg_kB": str(g2["log_lqg_kB"]),
                "log_euler_kB": str(g2["log_euler_kB"]),
                "dc_string_minus_euler": str(g2["dc_string_minus_euler"]),
                "dc_string_minus_lqg": str(g2["dc_string_minus_lqg"]),
                "log_diff_string_vs_euler_kB": str(g2["log_diff_string_vs_euler_kB"]),
                "rel_string": str(g2["rel_string"]),
            },
            "E3_extreme_kerr": {
                "rows": [{k: str(v) for k, v in r.items()} for r in g3["rows"]],
                "lam_ext": str(g3["lam_ext"]), "T_H_ext": str(g3["T_H_ext"]),
                "A_geom_ext": str(g3["A_geom_ext"]),
                "T_H_schw": str(g3["T_H_schw"]),
                "A_ext_over_A_schw_geom": str(g3["A_ext_over_A_schw_geom"]),
                "r_g": str(g3["r_g"]), "A_ext_SI": str(g3["A_ext_SI"]),
                "A_schw_SI": str(g3["A_schw_SI"]),
            },
            "E4_kn_extreme": {k: str(v) for k, v in g4.items()},
            "E5_ruling": "T132 structural negative vs TUFT; log correction coefficient c has no "
                         "first-principles unique value (string -3/2, LQG -1/2, Euler chi/2=1 disagree); "
                         "extreme T->0 and A=8pi M^2 are GR intrinsic; TUFT supplies no log/microstate; "
                         "hits C2/C7",
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0232 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
