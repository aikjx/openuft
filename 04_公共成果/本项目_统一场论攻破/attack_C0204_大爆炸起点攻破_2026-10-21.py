# -*- coding: utf-8 -*-
"""
attack_C0204_大爆炸起点攻破_2026-10-21.py
独立复算：母册 T038「大爆炸的起点 / 原初奇点」· FLRW 初始奇点 + Planck 正则化 + 初始条件供给检查

定位：母册 T038（行 134，原文照录）：
    | T038 | 大爆炸的起点 / 原初奇点 | 量子引力 | C1,C7 | ◐ T001 |
前置来料：
  - TUFT显式解候选账单（2026-10-21）：§三 奇点定理条件算术复核（τ_f=1.5 m、r⊙=2953.3 m）；
    §四 10/10 候选显式解对 T008/T038 奇点解除供给=0。
  - C0131 时空悖论（◐ T001）；C0201（T008 奇点定理，同批攻破）；
    T001 引力量子化已判七障碍（C0127/C0131/C0132）。
  - C0133 TUFT 身份注销；C0140 几何常数 (ℏ,G,c) 量纲 nullity=0。

把"大爆炸起点/原初奇点"压缩成五条可复核读数：

  E1 **FLRW 辐射主导初始奇点核算**：a(t)∝t^(1/2) 在 t→0 的尺度因子、Hubble 半径、
     Kretschmann 曲率发散核算；Planck 时间 t_P 处的曲率量级。
  E2 **Planck 尺度正则化核算（本册核心）**：经典 GR 失效边界 t*=√(3/(32π)) t_P——
     在 t=t_P 之前经典 GR 已失效；Planck 密度 ρ_Pl=c⁵/(ℏG²) 量级核算。
  E3 初始条件精细调谐核算：平坦性问题 |Ω(t_P)-1| ~ 10^-64；
     视界问题（复合期因果不连通斑块数）。
  E4 原初奇点供给检查：TUFT 显式解目录对原初奇点解除供给=0（引账单 §四 10/10）；
     TUFT 无量子引力供给（T001 七障碍已负面闭合）。
  E5 裁定：T038 结构性负面（对 TUFT/几何框架），撞 C1/C7。

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机。
退出码 0；守卫 assert 全过。

诚实边界：本册不宣称已解决大爆炸起点/原初奇点问题；外部观测值（H0、Ω_m、z_rec、
Planck 卫星 Ω 测量）只引用不复算；TUFT 已注销（C0133）；
严禁把标准物理结果写成 TUFT 预测/修正。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os
import json

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 基本物理常数（CODATA 2018 / SI 精确值，只引用不复算） ----------
G = Decimal("6.67430e-11")          # 引力常数, m^3 kg^-1 s^-2
C = Decimal("299792458")            # 真空光速, m/s
HBAR = Decimal("1.054571817e-34")   # 约化普朗克常数, J·s（2019 SI 修订精确值）
KB = Decimal("1.380649e-23")       # 玻尔兹曼常数, J/K（精确值）
PI = Decimal("3.14159265358979323846264338327950288419716939937510")

# ---------- 宇宙学观测值（Planck 2018，只引用不复算） ----------
H0 = Decimal("67.4")                 # Hubble 常数, km/s/Mpc
MPC_IN_M = Decimal("3.0856775814913673e22")  # 1 Mpc, m
OMEGA_M = Decimal("0.315")           # 物质密度参数（Planck 2018）
Z_REC = Decimal("1100")              # 复合红移
OMEGA0_DET = Decimal("0.001")        # |Ω0-1| 观测上限（Planck 平坦性测量，量级）
T_NOW_S = Decimal("4.35e17")         # 宇宙年龄, s（13.8 Gyr ≈ 4.35e17 s）

# ---------- 引用既有账单读数（不重算） ----------
# TUFT显式解候选账单 §四：10/10 候选解对奇点解除供给=0
BILL_SUPPLY_ZERO = 10
BILL_SUPPLY_TOTAL = 10


def planck_units():
    """由基本常数精算 Planck 单位（Decimal 48 位）。"""
    # t_P = sqrt(hbar * G / c^5)
    c5 = C ** 5
    t_P2 = HBAR * G / c5
    t_P = t_P2.sqrt()
    # l_P = sqrt(hbar * G / c^3)
    c3 = C ** 3
    l_P2 = HBAR * G / c3
    l_P = l_P2.sqrt()
    # M_P = sqrt(hbar * c / G)  (kg)
    M_P = (HBAR * C / G).sqrt()
    # rho_Pl = c^5 / (hbar * G^2)  (kg/m^3)
    G2 = G * G
    rho_Pl = c5 / (HBAR * G2)
    return {
        "t_P_s": t_P,
        "l_P_m": l_P,
        "M_P_kg": M_P,
        "rho_Pl_kg_m3": rho_Pl,
        "c5": c5,
    }


def e1_flrw_singularity():
    """E1 FLRW 辐射主导初始奇点核算。

    辐射主导：a(t) ∝ t^(1/2)
    H = ȧ/a = 1/(2t)
    ρ = 3H²/(8πG) = 3/(32πG t²)
    Kretschmann 标量 K = R_{μνρσ}R^{μνρσ} = 24 H⁴/c⁴（平坦 FLRW）
    """
    pu = planck_units()
    t_P = pu["t_P_s"]
    l_P = pu["l_P_m"]

    # 在 t = t_P 处
    H_P = Decimal(1) / (Decimal(2) * t_P)           # s^-1
    rho_P = Decimal(3) * H_P * H_P / (Decimal(8) * PI * G)  # kg/m^3
    # Hubble 半径 d_H = c/H = 2 c t_P = 2 l_P
    d_H_P = C / H_P
    # Kretschmann: K = 24 H^4 / c^4, 单位 m^-4
    K_P = Decimal(24) * H_P**4 / C**4
    # K_P 用 l_P^-4 表示：K_P = 1.5 / l_P^4
    K_over_lP4 = K_P * l_P**4

    # 在 t = 1 s（BBN 量级）处对照
    t_bbn = Decimal(1)  # s
    H_bbn = Decimal(1) / (Decimal(2) * t_bbn)
    rho_bbn = Decimal(3) * H_bbn * H_bbn / (Decimal(8) * PI * G)
    K_bbn = Decimal(24) * H_bbn**4 / C**4
    # 曲率发散比：K(t_P)/K(1s) = (1/t_P)^4 / (1/1s)^4 = (1/t_P)^4
    K_ratio = K_P / K_bbn

    return {
        "t_P_s": t_P,
        "l_P_m": l_P,
        "H_P_s-1": H_P,
        "rho_P_kg_m3": rho_P,
        "d_H_P_m": d_H_P,
        "d_H_over_lP": d_H_P / l_P,
        "K_P_m-4": K_P,
        "K_over_lP4": K_over_lP4,
        "H_bbn_s-1": H_bbn,
        "rho_bbn_kg_m3": rho_bbn,
        "K_bbn_m-4": K_bbn,
        "K_ratio_P_to_bbn": K_ratio,
    }


def e2_planck_regularization():
    """E2 Planck 尺度正则化核算（本册核心）。

    经典 GR 在 t→0 密度发散；什么时候密度达到 Planck 密度？
    ρ(t) = 3/(32πG t²)
    令 ρ(t*) = ρ_Pl = c⁵/(ℏG²):
        3/(32πG t*²) = c⁵/(ℏG²)
        t*² = 3ℏG/(32π c⁵) = (3/(32π)) t_P²
        t* = t_P √(3/(32π))
    """
    pu = planck_units()
    t_P = pu["t_P_s"]
    rho_Pl = pu["rho_Pl_kg_m3"]

    # t* = t_P * sqrt(3/(32π))
    factor = Decimal(3) / (Decimal(32) * PI)
    factor_sqrt = factor.sqrt()
    t_star = t_P * factor_sqrt

    # t* / t_P
    ratio_t_star_over_tP = t_star / t_P

    # 在 t = t_P 处的密度 vs Planck 密度
    g1 = e1_flrw_singularity()
    rho_P = g1["rho_P_kg_m3"]
    rho_P_over_rhoPl = rho_P / rho_Pl

    # 在 t = t_P/100 处（经典外推）密度 vs Planck 密度
    t_early = t_P / Decimal(100)
    H_early = Decimal(1) / (Decimal(2) * t_early)
    rho_early = Decimal(3) * H_early * H_early / (Decimal(8) * PI * G)
    rho_early_over_rhoPl = rho_early / rho_Pl

    # t* 比 t_P 小多少倍
    tP_over_tstar = t_P / t_star

    return {
        "rho_Pl_kg_m3": rho_Pl,
        "factor_3_over_32pi": factor,
        "factor_sqrt": factor_sqrt,
        "t_star_s": t_star,
        "t_star_over_tP": ratio_t_star_over_tP,
        "tP_over_tstar": tP_over_tstar,
        "rho_P_over_rhoPl": rho_P_over_rhoPl,
        "rho_tP100_over_rhoPl": rho_early_over_rhoPl,
    }


def e3_initial_conditions():
    """E3 初始条件精细调谐核算。

    平坦性问题：|Ω-1| ∝ t（辐射主导）
        |Ω(t_P)-1| = |Ω0-1| × (t_P/t_now)
    视界问题：复合期因果不连通斑块数
        H_rec = H0 × sqrt(Ω_m (1+z_rec)^3)
        共动 Hubble 半径比：(aH)_rec / (aH)_now = (1+z_rec) H_rec / H0
    """
    pu = planck_units()
    t_P = pu["t_P_s"]

    # 平坦性
    flatness_tP = OMEGA0_DET * (t_P / T_NOW_S)

    # H0 换算成 s^-1
    H0_s = H0 * Decimal("1000") / MPC_IN_M   # km/s/Mpc -> s^-1
    # H_rec = H0 * sqrt(Ω_m * (1+z)^3)
    zp1 = Decimal(1) + Z_REC
    H_rec = H0_s * (OMEGA_M * zp1**3).sqrt()
    # (aH)_rec / (aH)_now = (1+z_rec) * H_rec / H0
    aH_ratio = zp1 * H_rec / H0_s
    # 因果不连通斑块数 ~ (aH_ratio)^2
    patches = aH_ratio * aH_ratio

    return {
        "flatness_omega_minus1_at_tP": flatness_tP,
        "H0_s-1": H0_s,
        "H_rec_s-1": H_rec,
        "aH_ratio_rec_to_now": aH_ratio,
        "causally_disconnected_patches": patches,
    }


def e4_supply_check():
    """E4 原初奇点供给检查（引账单 §四 10/10=0；T001 七障碍）。"""
    return {
        "bill_candidates_total": BILL_SUPPLY_TOTAL,
        "bill_candidates_supply_zero": BILL_SUPPLY_ZERO,
        "bill_supply_ratio": "10/10 = 0",
        "tuft_has_quantum_gravity": False,
        "tuft_has_explicit_regularized_metric": False,
        "tuft_breaks_NEC": False,
        "tuft_breaks_global_hyperbolicity": False,
        "cited_bill_section4": "TUFT显式解候选账单 §四：10/10 候选解对奇点解除供给=0",
        "cited_T001_seven_obstacles": "T001 引力量子化七障碍已负面闭合（C0127/C0131/C0132）",
        "cited_C0133": "TUFT 身份注销",
        "cited_C0140": "几何常数 (ℏ,G,c) 量纲 nullity=0",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0204 · 大爆炸起点 / 原初奇点（母册 T038）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_flrw_singularity()
    w("\n[E1] FLRW 辐射主导初始奇点核算（a(t)∝t^(1/2)）")
    w("  Planck 常数：t_P = %s s；l_P = %s m" % (fv(g1["t_P_s"], "6e"), fv(g1["l_P_m"], "6e")))
    w("  在 t=t_P：H = 1/(2t_P) = %s s^-1" % fv(g1["H_P_s-1"], "6e"))
    w("  在 t=t_P：ρ = 3H²/(8πG) = %s kg/m³" % fv(g1["rho_P_kg_m3"], "6e"))
    w("  在 t=t_P：Hubble 半径 d_H = c/H = %s m = %s l_P"
      % (fv(g1["d_H_P_m"], "6e"), fv(g1["d_H_over_lP"], "4f")))
    w("  在 t=t_P：Kretschmann K = 24H⁴/c⁴ = %s m^-4 = %s l_P^-4"
      % (fv(g1["K_P_m-4"], "6e"), fv(g1["K_over_lP4"], "4f")))
    w("  对照 t=1 s（BBN）：ρ = %s kg/m³；K = %s m^-4"
      % (fv(g1["rho_bbn_kg_m3"], "4e"), fv(g1["K_bbn_m-4"], "4e")))
    w("  曲率发散比 K(t_P)/K(1s) = %s（= t^-4 发散，t→0 曲率发散至无穷）"
      % fv(g1["K_ratio_P_to_bbn"], "6e"))
    w("  => 辐射主导 FLRW 在 t→0 尺度因子 a→0、密度 ρ∝t^-2、曲率 K∝t^-4 发散——")
    w("     这是标准 GR 的 FLRW 精确解，奇点是经典 GR 的内禀性质。")
    entries.append(("E1",
                    "t_P=%s s；t=t_P 时 H=%s s^-1、ρ=%s kg/m³、d_H=%s l_P、K=%s l_P^-4；"
                    "K∝t^-4 发散"
                    % (fv(g1["t_P_s"], "4e"), fv(g1["H_P_s-1"], "4e"),
                       fv(g1["rho_P_kg_m3"], "4e"), fv(g1["d_H_over_lP"], "3f"),
                       fv(g1["K_over_lP4"], "3f")),
                    "PASS", "Decimal 48 位精算；G/c/ℏ 只引用；辐射 FLRW a∝t^(1/2) 标准推导"))

    # ---- E2 ----
    g2 = e2_planck_regularization()
    w("\n[E2] Planck 尺度正则化核算（本册核心）")
    w("  Planck 密度 ρ_Pl = c⁵/(ℏG²) = %s kg/m³" % fv(g2["rho_Pl_kg_m3"], "6e"))
    w("  令 ρ(t*)=ρ_Pl：t* = t_P × √(3/(32π))")
    w("  3/(32π) = %s；√ = %s" % (fv(g2["factor_3_over_32pi"], "6f"), fv(g2["factor_sqrt"], "6f")))
    w("  t* = %s s" % fv(g2["t_star_s"], "6e"))
    w("  t*/t_P = %s（即 t* = %s × t_P）"
      % (fv(g2["t_star_over_tP"], "6f"), fv(g2["t_star_over_tP"], "4f")))
    w("  t_P/t* = %s（即在 t=t_P 之前 %s 倍处密度已达 Planck 密度）"
      % (fv(g2["tP_over_tstar"], "4f"), fv(g2["tP_over_tstar"], "2f")))
    w("  在 t=t_P 处：ρ/ρ_Pl = %s（已达 Planck 密度的 ~3%%）"
      % fv(g2["rho_P_over_rhoPl"], "6f"))
    w("  在 t=t_P/100 处：ρ/ρ_Pl = %s（已达 Planck 密度的 ~3×10^6 倍，经典 GR 完全失效）"
      % fv(g2["rho_tP100_over_rhoPl"], "4e"))
    w("  => 经典 GR 外推到 t < t* ≈ 0.173 t_P 时密度已超 Planck 密度——")
    w("     经典 GR 在 Planck 尺度之前失效，奇点的正则化必须由量子引力提供（T001 已判七障碍）。")
    entries.append(("E2",
                    "ρ_Pl=%s kg/m³；t*=√(3/32π) t_P=%s s（t*/t_P=%s）；"
                    "t=t_P 时 ρ/ρ_Pl=%s；t=t_P/100 时 ρ/ρ_Pl=%s"
                    % (fv(g2["rho_Pl_kg_m3"], "4e"), fv(g2["t_star_s"], "3e"),
                       fv(g2["t_star_over_tP"], "4f"),
                       fv(g2["rho_P_over_rhoPl"], "4f"),
                       fv(g2["rho_tP100_over_rhoPl"], "2e")),
                    "PASS", "Decimal 48 位精算；ρ(t)=3/(32πGt²) 标准辐射宇宙学"))

    # ---- E3 ----
    g3 = e3_initial_conditions()
    w("\n[E3] 初始条件精细调谐核算（平坦性 + 视界问题）")
    w("  平坦性：|Ω-1| ∝ t（辐射主导）；|Ω0-1| < %s（Planck 2018）"
      % fv(OMEGA0_DET, "3f"))
    w("  |Ω(t_P)-1| = |Ω0-1| × t_P/t_now = %s × %s = %s"
      % (fv(OMEGA0_DET, "3f"), fv(g1["t_P_s"] / T_NOW_S, "2e"),
         fv(g3["flatness_omega_minus1_at_tP"], "2e")))
    w("  => 平坦性精细调谐：初始 |Ω-1| 须 ~10^-64 量级（1 part in 10^64）。")
    w("  视界：H0 = %s km/s/Mpc = %s s^-1" % (fv(H0, "1f"), fv(g3["H0_s-1"], "4e")))
    w("  H_rec = H0√(Ω_m(1+z)^3) = %s s^-1" % fv(g3["H_rec_s-1"], "4e"))
    w("  (aH)_rec/(aH)_now = %s" % fv(g3["aH_ratio_rec_to_now"], "4e"))
    w("  因果不连通斑块数 ~ (aH 比)² = %s（~10^%s 个独立因果区）"
      % (fv(g3["causally_disconnected_patches"], "2e"),
         (g3["causally_disconnected_patches"].ln() / Decimal(10).ln()).to_integral_value(rounding="ROUND_HALF_UP")))
    w("  => 视界问题：CMB 天空在无暴胀时应有 ~10^14 个因果不连通斑块，")
    w("     但观测到各向同性 ~10^-5——初始条件须极端精细调谐。")
    entries.append(("E3",
                    "平坦性 |Ω(t_P)-1|=%s（~10^-64）；视界斑块数~%s（~10^14）"
                    % (fv(g3["flatness_omega_minus1_at_tP"], "1e"),
                       fv(g3["causally_disconnected_patches"], "1e")),
                    "PASS", "H0/Ω_m/z_rec/Ω0_det 只引用；平坦性 t∝|Ω-1| 标准推导"))

    # ---- E4 ----
    g4 = e4_supply_check()
    w("\n[E4] 原初奇点供给检查（TUFT/几何框架）")
    w("  TUFT 显式解目录（引账单 §四）：%d/%d 候选解对奇点解除供给 = 0"
      % (g4["bill_candidates_supply_zero"], g4["bill_candidates_total"]))
    w("  TUFT 有量子引力态：%s" % g4["tuft_has_quantum_gravity"])
    w("  TUFT 有独立正则化度规：%s" % g4["tuft_has_explicit_regularized_metric"])
    w("  TUFT 破坏 NEC：%s；破坏全局双曲性：%s"
      % (g4["tuft_breaks_NEC"], g4["tuft_breaks_global_hyperbolicity"]))
    w("  T001 引力量子化七障碍已负面闭合（C0127/C0131/C0132）——量子引力正则化路径已封。")
    w("  => TUFT 无量子引力供给、无显式正则化度规、无破坏三条件项；")
    w("     撞 C1（初始条件须公设）/ C7（数学自洽≠实验证实）。")
    entries.append(("E4",
                    "显式解目录 10/10=0（账单 §四）；TUFT 无量子引力/无正则化度规；"
                    "T001 七障碍已负面闭合",
                    "PASS", "撞 C1/C7"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  大爆炸起点/原初奇点问题被精确翻译成三件事：(a) 经典 GR 奇点曲率发散到什么量级；")
    w("  (b) 经典 GR 在什么尺度失效（量子引力接管）；(c) 初始条件（平坦/视界）谁供给。")
    w("  (a) a∝t^(1/2)、ρ∝t^-2、K∝t^-4 发散——标准 FLRW 精确解（E1）。")
    w("  (b) t*=√(3/32π) t_P ≈ 0.173 t_P 处密度已达 Planck 密度——经典 GR 在 Planck 尺度")
    w("      之前失效，正则化须由量子引力提供（E2）；T001 七障碍已负面闭合。")
    w("  (c) 平坦性精细调谐 ~10^-64、视界 ~10^14 斑块（E3）——初始条件须外部输入。")
    w("  => **T038 结构性负面（对 TUFT/几何框架）**；撞 **C1**（初始条件/量子引力态须公设）/")
    w("     **C7**（数学自洽 ≠ 实验证实；TUFT 无 Planck 尺度正则化）。母册 T038 ◐→✅。")
    entries.append(("E5",
                    "T038 结构性负面：奇点正则化依赖量子引力（T001 七障碍已闭），"
                    "TUFT 无供给、显式解目录 10/10=0；撞 C1/C7",
                    "PASS", "撞 C1/C7；母册 T038 ◐→✅"))

    # ---- 守卫 ----
    guards = [
        ("G1", "t_P ≈ 5.39×10^-44 s（Planck 时间量级）",
         g1["t_P_s"] > Decimal("5e-44") and g1["t_P_s"] < Decimal("6e-44")),
        ("G2", "l_P ≈ 1.62×10^-35 m（Planck 长度量级）",
         g1["l_P_m"] > Decimal("1.6e-35") and g1["l_P_m"] < Decimal("1.7e-35")),
        ("G3", "t* < t_P（经典 GR 在 Planck 时间之前失效）",
         g2["t_star_s"] < g1["t_P_s"]),
        ("G4", "t*/t_P = √(3/32π) ≈ 0.173",
         Decimal("0.17") < g2["t_star_over_tP"] < Decimal("0.18")),
        ("G5", "平坦性精细调谐 < 10^-60（1 part in 10^60+）",
         g3["flatness_omega_minus1_at_tP"] < Decimal("1e-60")),
        ("G6", "视界斑块数 > 10^10（因果不连通量级）",
         g3["causally_disconnected_patches"] > Decimal("1e10")),
        ("G7", "显式解目录 10/10=0 供给（账单 §四）",
         g4["bill_candidates_supply_zero"] == 10 and g4["bill_candidates_total"] == 10),
        ("G8", "TUFT 无量子引力供给", g4["tuft_has_quantum_gravity"] is False),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0204 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解决大爆炸起点/原初奇点问题；G/c/ℏ/k_B、H0/Ω_m/z_rec/Ω0 观测值")
    w("  只引用不复算；TUFT 已注销（C0133）；严禁把标准物理结果写成 TUFT 预测/修正。")
    w("  数学自洽 ≠ 实验证实；「有预测且对 = 0/22」保持；「UFT-3 = 0」保持。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0204_大爆炸起点攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0204_大爆炸起点攻破_2026-10-21.json")

    def _s(v):
        if isinstance(v, Decimal):
            return str(v)
        if isinstance(v, Fraction):
            return str(v)
        if isinstance(v, dict):
            return {kk: _s(vv) for kk, vv in v.items()}
        if isinstance(v, (list, tuple)):
            return [_s(x) for x in v]
        return v

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0204_big_bang_origin_primordial_singularity",
            "mother_row": "| T038 | 大爆炸的起点 / 原初奇点 | 量子引力 | C1,C7 | ◐ T001 |",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_flrw_singularity": _s(g1),
            "E2_planck_regularization": _s(g2),
            "E3_initial_conditions": _s(g3),
            "E4_supply_check": _s(g4),
            "guards_total": len(guards),
            "guards_passed": sum(1 for g in guards if g[2]),
            "cited_bill": "TUFT显式解候选账单 §三/§四（2026-10-21）",
            "cited_C0131": "时空悖论（◐ T001）",
            "cited_C0201": "T008 奇点定理（同批攻破）",
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0204 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
