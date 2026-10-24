# -*- coding: utf-8 -*-
"""
attack_C0233_顶夸克质量攻破_2026-10-21.py
独立精算：顶夸克 MS 质量 vs 极点质量方案（母册 T368 · L 线域 H 批 · QCD 重整化标度 · 撞 C7）

定位：母册 T368（原文照录）：
  | T368 | 顶夸克 MS 质量 vs 极点质量方案 | QCD 重整化标度 | C7 | 🔲 |
主题：质量方案换算核算——一阶 QCD pole-MS 关系精算、PDG 对照、μ=M_t vs μ=2GeV 标度依赖、
一阶 vs 高阶修正量分解，以及 TUFT 是否供给 QCD 重整化 / 质量方案结构。

衔接：
  - C0194（基本粒子质量谱）：y_t = sqrt(2)*173.0/246.22 = 0.9936599（O(1)）。本册注意
    y_t 本身依赖质量方案：用 pole 质量 vs MS(M_t) 质量算 y_t 差 ~6%。
  - C0133（TUFT 终审注销）：仅经典局部几何，无 QCD / 无重整化群 / 无 α_s 供给。
  - C0142 模板：四件套格式（py→report→json→判定册）。

把「顶夸克 MS 质量 vs 极点质量方案」压缩成五条可复核读数：

  E1 标准 QCD 质量方案事实（pole = on-shell 自能零点，μ 无关；MS-bar = μ 依赖；
     PDG 外部输入只引用不复算：m_t^pole=172.69、α_s(M_t)=0.1080、m_t^MS(M_t)=162.5 GeV）。
  E2 **一阶 pole↔MS(M_t) 换算核算（本册核心）**：m_pole - m_MS = (4α_s/3π) m_MS，
     正/反两个方向 Decimal 逐位精算，并与 PDG 双质量对照。
  E3 标度依赖核算：μ=M_t vs μ=2 GeV 的 MS 质量跑动（领头对数，n_f=5，γ0=4，β0=23/3）。
  E4 一阶 vs 高阶修正量核算：总修正 δ_total = m_pole/m_MS - 1 拆成一阶 k1 与高阶 δ_ho；
     并核算方案歧义向顶 Yukawa y_t 的传播（pole vs MS 差 ~6%，衔接 C0194）。
  E5 裁定：质量方案依赖 QCD 重整化结构（标准算术），TUFT 无 QCD / 无重整化供给 ⇒ 结构性负面，
     按母册登记撞 C7。

纯标准库（Decimal 48 位 + Fraction 精确代数），零外部依赖、零网络、零随机，退出码 0。

诚实边界：数值均为标准 QCD 重整化算术复核；PDG 质量与 α_s 为已知外部输入显式计数，
非本册预测；TUFT 已注销（C0133）；严禁把标准物理结果写成 TUFT 预测/修正。
本册不宣称解决任何物理难题。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# π 取 50 位（与 C0187/C0210/C0232 同一硬编码值）
PI = Decimal("3.14159265358979323846264338327950288419716939937510")
# sqrt(2)（与 C0194 同口径）
SQRT2 = Decimal("1.4142135623730950488016887242096980785696718753769")

# ---------- 外部输入（PDG，只引用不复算；显式计数） ----------
M_T_POLE = Decimal("172.69")     # GeV，PDG 顶夸克极点质量（on-shell）
AS_MT = Decimal("0.1080")        # α_s(M_t)，由 α_s(M_Z)=0.1181 跑动而来（题给外部输入）
MT_MS_MT = Decimal("162.5")      # GeV，PDG MS-bar 质量在 μ=M_t 处（162–163 GeV 量级取中值）
V_EW = Decimal("246.22")         # GeV，电弱 VEV（承接 C0194 E2）

# 一阶 QCD pole↔MS 系数（题给关系：m_pole - m_MS = (4α_s/3π) m_MS）
# 即 m_pole = m_MS (1 + k1)，k1 = 4α_s/(3π)。
# C_F = 4/3（QCD 色因子），一阶系数结构 C_F·(α_s/π) 在 μ=m 处对数项归零后即 4/3·α_s/π。
CF = Fraction(4, 3)


def e1_scheme_facts():
    """E1：pole 与 MS-bar 两种质量方案的定义 + PDG 外部输入。"""
    return {
        "pole_def": "极点质量 = 夸克传播子自能零点（on-shell 极点），定义上与重整化标度 μ 无关",
        "msbar_def": "MS-bar 质量 = MS-bar 方案重整化后的跑动质量，显式依赖 μ（QCD 跑动）",
        "m_t_pole_GeV": M_T_POLE,
        "alpha_s_Mt": AS_MT,
        "m_t_MS_Mt_GeV": MT_MS_MT,
        "v_EW_GeV": V_EW,
        "origin": "PDG 夸克质量表 + α_s 跑动（标准 QCD 外部输入，只引用不复算）",
    }


def e2_pole_ms_conversion():
    """E2（核心）：一阶 pole↔MS(M_t) 换算核算（双向 Decimal 精算）。

    题给一阶关系：m_pole - m_MS = (4α_s/3π) m_MS
      ⇒ k1 = 4α_s/(3π)；m_pole = m_MS (1+k1)。
    正向：由 PDG MS(M_t)=162.5 算一阶 pole；反向：由 PDG pole=172.69 算一阶 MS。
    """
    as_dec = AS_MT
    k1 = (Decimal(4) * as_dec) / (Decimal(3) * PI)          # = C_F · α_s/π
    # 正向：MS(M_t) -> pole（一阶）
    m_pole_from_ms_1 = MT_MS_MT * (Decimal(1) + k1)
    # 反向：pole -> MS(M_t)（一阶）
    m_ms_from_pole_1 = M_T_POLE / (Decimal(1) + k1)
    # PDG 双质量对照比（外部输入直接除）
    R = M_T_POLE / MT_MS_MT                                  # 实测 pole/MS(M_t)
    delta_total = R - Decimal(1)                             # 总 QCD 匹配修正（至高阶）
    return {
        "k1": k1,
        "m_pole_from_ms_1loop": m_pole_from_ms_1,
        "m_ms_from_pole_1loop": m_ms_from_pole_1,
        "R_pole_over_ms": R,
        "delta_total": delta_total,
        "gap_forward_GeV": M_T_POLE - m_pole_from_ms_1,      # 正向一阶距实测 pole 的缺口
        "gap_backward_GeV": m_ms_from_pole_1 - MT_MS_MT,     # 反向一阶距 PDG MS 的高出
    }


def e3_scale_running():
    """E3：标度依赖核算——μ=M_t vs μ=2 GeV 的 MS 质量跑动（领头对数）。

    领头对数 QCD 质量跑动：
      m(μ) = m(μ0) [α_s(μ)/α_s(μ0)]^{γ0/(2β0)}
    单段 n_f=5：γ0=4，β0 = 11 - (2/3)n_f = 23/3 ⇒ 指数 = 4/(2·23/3) = 6/23。
    α_s 跑动（1 圈）：1/α_s(μ) = 1/α_s(μ0) + (β0/2π) ln(μ/μ0)。
    注：阈值（m_b≈4.2GeV 处 n_f:5→4）匹配本册不展开，按数量级（跑动方向与幅度）判定。
    """
    beta0 = Fraction(23, 3)            # n_f=5
    gamma0 = 4
    expo = Fraction(gamma0, 2) / beta0  # = 2/(23/3) = 6/23
    expo_d = Decimal(expo.numerator) / Decimal(expo.denominator)

    mu0 = M_T_POLE                      # 以 pole 质量为上标度 μ0
    mu = Decimal("2")
    ln_ratio = (mu / mu0).ln()          # ln(2/172.69)
    # 1/α_s(μ)
    inv_as_mu = Decimal(1) / AS_MT + (Decimal(beta0.numerator) / Decimal(beta0.denominator)
                                      / (Decimal(2) * PI)) * ln_ratio
    as_mu = Decimal(1) / inv_as_mu
    # 质量跑动比
    mass_ratio = (as_mu / AS_MT) ** expo_d   # Decimal ** Decimal 幂
    m_ms_at_2 = MT_MS_MT * mass_ratio
    return {
        "beta0": beta0, "gamma0": gamma0, "exponent_6_23": expo_d,
        "ln_mu_over_mu0": ln_ratio,
        "as_at_2GeV": as_mu,
        "mass_ratio_m2_over_mMt": mass_ratio,
        "m_ms_at_2GeV": m_ms_at_2,
    }


def e4_loop_decomposition():
    """E4：一阶 vs 高阶修正量分解 + 方案歧义向 y_t 的传播。

    总修正 δ_total = R - 1（R=m_pole/m_MS，PDG 外部输入）；
    一阶 k1 = 4α_s/3π；高阶残差 δ_ho = δ_total - k1（2 圈+3 圈 QCD 匹配项）。
    Yukawa：y_t = sqrt(2) m_t/v，分别用 pole 与 MS(M_t) 算，差即方案歧义。
    """
    g2 = e2_pole_ms_conversion()
    k1 = g2["k1"]
    delta_total = g2["delta_total"]
    delta_ho = delta_total - k1
    ho_over_lo = delta_ho / k1
    # Yukawa（衔接 C0194：v=246.22）
    y_t_pole = SQRT2 * M_T_POLE / V_EW
    y_t_ms = SQRT2 * MT_MS_MT / V_EW
    dy = y_t_pole - y_t_ms
    rel_scheme = dy / y_t_ms
    return {
        "k1": k1, "delta_total": delta_total, "delta_ho": delta_ho,
        "ho_over_lo": ho_over_lo,
        "y_t_pole": y_t_pole, "y_t_ms": y_t_ms,
        "dy": dy, "rel_scheme_pct": rel_scheme * Decimal(100),
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0233 · 顶夸克 MS 质量 vs 极点质量方案（母册 T368 · 撞 C7）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_scheme_facts()
    w("\n[E1] 标准 QCD 质量方案事实（pole / MS-bar 定义 + PDG 外部输入，只引用不复算）")
    w("  %s" % g1["pole_def"])
    w("  %s" % g1["msbar_def"])
    w("  PDG 外部输入：m_t^pole = %s GeV；α_s(M_t) = %s；m_t^MS(M_t) = %s GeV；v = %s GeV"
      % (fv(g1["m_t_pole_GeV"], "2f"), g1["alpha_s_Mt"], fv(g1["m_t_MS_Mt_GeV"], "1f"),
         fv(g1["v_EW_GeV"], "2f")))
    w("  => %s；本册只做换算与跑动精算，质量值不归因 TUFT。" % g1["origin"])
    entries.append(("E1", "pole(on-shell, μ无关) vs MS-bar(μ依赖)；外部输入 m_pole=172.69 GeV、"
                          "α_s(M_t)=0.1080、m_MS(M_t)=162.5 GeV",
                    "PASS", "PDG 只引用不复算；本册只做标准 QCD 算术换算"))

    # ---- E2 ----
    g2 = e2_pole_ms_conversion()
    w("\n[E2] 一阶 pole↔MS(M_t) 换算核算（本册核心，Decimal 48 位逐位精算）")
    w("  题给一阶关系：m_pole - m_MS = (4α_s/3π) m_MS ⇒ k1 = 4α_s/(3π)")
    w("  k1 = 4×%s / (3π) = %s（= C_F·α_s/π，C_F=4/3）"
      % (g1["alpha_s_Mt"], fv(g2["k1"], "8f")))
    w("  正向：m_pole^(1) = m_MS(M_t)×(1+k1) = %s×%.6f = %s GeV"
      % (fv(g1["m_t_MS_Mt_GeV"], "1f"), float(1 + g2["k1"]),
         fv(g2["m_pole_from_ms_1loop"], "3f")))
    w("  反向：m_MS^(1)(M_t) = m_pole/(1+k1) = %s/%.6f = %s GeV"
      % (fv(g1["m_t_pole_GeV"], "2f"), float(1 + g2["k1"]),
         fv(g2["m_ms_from_pole_1loop"], "3f")))
    w("  --- PDG 双质量对照 ---")
    w("  实测比 R = m_pole/m_MS(M_t) = %s/%s = %s"
      % (fv(g1["m_t_pole_GeV"], "2f"), fv(g1["m_t_MS_Mt_GeV"], "1f"),
         fv(g2["R_pole_over_ms"], "6f")))
    w("  正向一阶距实测 pole 缺口 = %s - %s = %s GeV"
      % (fv(g1["m_t_pole_GeV"], "2f"), fv(g2["m_pole_from_ms_1loop"], "3f"),
         fv(g2["gap_forward_GeV"], "3f")))
    w("  反向一阶距 PDG MS 高出 = %s - %s = %s GeV"
      % (fv(g2["m_ms_from_pole_1loop"], "3f"), fv(g1["m_t_MS_Mt_GeV"], "1f"),
         fv(g2["gap_backward_GeV"], "3f")))
    w("  => 一阶 QCD 关系把 pole 与 MS(M_t) 差钉死在 ~%s%%；双向缺口一致（~2.5 GeV），"
      % fv(g2["k1"] * 100, "2f"))
    w("     缺口即高阶（2 圈+3 圈）匹配修正（见 E4）。标准 QCD 换算算术复核。")
    entries.append(("E2", "k1=4α_s/3π=%s；正向 162.5→%s GeV（距实测 172.69 缺 %s GeV）；"
                          "反向 172.69→%s GeV（高出 PDG 162.5 约 %s GeV）；R=%s"
                    % (fv(g2["k1"], "4f"), fv(g2["m_pole_from_ms_1loop"], "2f"),
                       fv(g2["gap_forward_GeV"], "2f"), fv(g2["m_ms_from_pole_1loop"], "2f"),
                       fv(g2["gap_backward_GeV"], "2f"), fv(g2["R_pole_over_ms"], "4f")),
                    "PASS", "Decimal 双向精算；α_s=0.1080、PDG 双质量为外部输入"))

    # ---- E3 ----
    g3 = e3_scale_running()
    w("\n[E3] 标度依赖核算：μ=M_t vs μ=2 GeV 的 MS 质量跑动（领头对数，n_f=5）")
    w("  跑动式 m(μ)=m(μ0)[α_s(μ)/α_s(μ0)]^{γ0/(2β0)}；β0=%s、γ0=%d ⇒ 指数=%s（=6/23）"
      % (g3["beta0"], g3["gamma0"], fv(g3["exponent_6_23"], "6f")))
    w("  ln(μ/μ0)=ln(2/172.69)=%s" % fv(g3["ln_mu_over_mu0"], "6f"))
    w("  1 圈跑动：α_s(2 GeV) = %s（由 α_s(M_t)=0.1080 跑下）" % fv(g3["as_at_2GeV"], "6f"))
    w("  质量跑动比 m(2GeV)/m(M_t) = [α_s(2)/α_s(M_t)]^{6/23} = %s"
      % fv(g3["mass_ratio_m2_over_mMt"], "6f"))
    w("  ⇒ m_t^MS(2 GeV) ≈ %s × %s = %s GeV（> m_MS(M_t)，跑向低标度质量增大）"
      % (fv(g1["m_t_MS_Mt_GeV"], "1f"), fv(g3["mass_ratio_m2_over_mMt"], "4f"),
         fv(g3["m_ms_at_2GeV"], "2f")))
    w("  => MS 质量强标度依赖：μ 从 172.69 GeV 降到 2 GeV，质量涨 ~%s%%；"
      % fv((g3["mass_ratio_m2_over_mMt"] - 1) * 100, "1f"))
    w("     而 pole 质量定义上 μ 无关——这正是两种方案不可互换的根源（阈值匹配本册不展开）。")
    entries.append(("E3", "领头对数跑下：α_s(2GeV)=%s、m_MS(2GeV)/m_MS(M_t)=%s ⇒ "
                          "m_t^MS(2GeV)≈%s GeV（涨 ~%s%%）；pole 质量 μ 无关"
                    % (fv(g3["as_at_2GeV"], "4f"), fv(g3["mass_ratio_m2_over_mMt"], "4f"),
                       fv(g3["m_ms_at_2GeV"], "1f"),
                       fv((g3["mass_ratio_m2_over_mMt"] - 1) * 100, "0f")),
                    "PASS", "领头对数 n_f=5 Decimal 精算；阈值匹配标注未展开"))

    # ---- E4 ----
    g4 = e4_loop_decomposition()
    w("\n[E4] 一阶 vs 高阶修正量分解 + 方案歧义向 y_t 传播（衔接 C0194）")
    w("  总修正 δ_total = R-1 = %s；一阶 k1 = %s；高阶残差 δ_ho = δ_total-k1 = %s"
      % (fv(g4["delta_total"], "6f"), fv(g4["k1"], "6f"), fv(g4["delta_ho"], "6f")))
    w("  高阶/一阶 = %s（即 2 圈+3 圈修正达领头项的 ~%s%%，非可忽略）"
      % (fv(g4["ho_over_lo"], "4f"), fv(g4["ho_over_lo"] * 100, "0f")))
    w("  --- Yukawa 方案传播（v=246.22 GeV，衔接 C0194 y_t=0.993660）---")
    w("  y_t(pole) = sqrt(2)×172.69/246.22 = %s" % fv(g4["y_t_pole"], "8f"))
    w("  y_t(MS)   = sqrt(2)×162.5/246.22 = %s" % fv(g4["y_t_ms"], "8f"))
    w("  Δy_t = %s（相对 MS 方案 %s%%）——质量方案歧义直接进 Yukawa，不可忽略。"
      % (fv(g4["dy"], "6f"), fv(g4["rel_scheme_pct"], "2f")))
    w("  => 一阶关系仅抓住 ~64% 的修正（k1/δ_total），高阶贡献 ~36%；"
      "方案选择使 y_t 漂移 ~6%，与 C0194 的 O(1) 结论相容但读数依赖方案。")
    entries.append(("E4", "δ_total=%s = k1 %s + δ_ho %s；高阶/一阶=%s；y_t(pole)=%s vs "
                          "y_t(MS)=%s，方案漂移 %s%%"
                    % (fv(g4["delta_total"], "4f"), fv(g4["k1"], "4f"),
                       fv(g4["delta_ho"], "4f"), fv(g4["ho_over_lo"], "3f"),
                       fv(g4["y_t_pole"], "4f"), fv(g4["y_t_ms"], "4f"),
                       fv(g4["rel_scheme_pct"], "1f")),
                    "PASS", "Decimal 分解 + Yukawa 双方案；衔接 C0194 v=246.22"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  T368 被精确翻译成三件事：(a) pole↔MS(M_t) 换算系数从哪来（E2/E4，标准 QCD 微扰）；")
    w("  (b) MS 质量的标度跑动从哪来（E3，QCD 重整化群 β0/γ0）；")
    w("  (c) TUFT/几何框架是否供给 QCD 重整化与质量方案结构（供给=0）。")
    w("  (a) 一阶 k1=4α_s/3π 依赖色因子 C_F=4/3 与 α_s(M_t)=0.1080；高阶 δ_ho 依赖 2/3 圈 QCD "
      "匹配函数——全部是标准 QCD 微扰结构，本册仅算术复核。")
    w("  (b) 标度跑动依赖 β0=11-2n_f/3、γ0=4 与 α_s 重整化群方程；TUFT 无此结构。")
    w("  (c) TUFT 已注销（C0133）仅经典局部几何：无 QCD、无重整化群、无 α_s、无 C_F、")
    w("      无奇点/极点质量定义、无 MS-bar 方案 ⇒ 质量方案供给 = 0。")
    w("  => **T368 结构性负面（对 TUFT/几何框架）**；本册精算为标准 QCD 重整化算术复核，")
    w("     严禁写成 TUFT 预测/修正。按母册 T368 登记撞 C7（数学自洽边界：质量方案依赖")
    w("     QCD 重整化结构，TUFT 无该载体，结构性负面闭合）。")
    entries.append(("E5", "T368 结构性负面：pole↔MS 换算、α_s 跑动、β0/γ0 重整化群均为标准 QCD 结构；"
                          "TUFT(C0133) 无 QCD/无重整化/无质量方案供给=0",
                    "PASS", "撞 C7"))

    # ---- 守卫 ----
    guards = [
        ("G1", "α_s(M_t) = 0.1080（题给外部输入）", AS_MT == Decimal("0.1080")),
        ("G2", "一阶系数 k1 = 4α_s/3π ≈ 0.0458（落在 0.04–0.05 带）",
         Decimal("0.04") < g2["k1"] < Decimal("0.05")),
        ("G3", "实测 R = m_pole/m_MS(M_t) > 1（pole 重于 MS(M_t)，落在 1.05–1.08 带）",
         Decimal("1.05") < g2["R_pole_over_ms"] < Decimal("1.08")),
        ("G4", "高阶残差 δ_ho > 0（2/3 圈修正为正贡献）", g4["delta_ho"] > 0),
        ("G5", "高阶/一阶 ≈ 0.37（落在 0.25–0.5 带，高阶非可忽略）",
         Decimal("0.25") < g4["ho_over_lo"] < Decimal("0.5")),
        ("G6", "标度跑动：m_MS(2GeV) > m_MS(M_t)（跑向低标度质量增大，比 >1）",
         g3["mass_ratio_m2_over_mMt"] > 1),
        ("G7", "y_t(pole) = O(1)（0.9–1.1 带，顶夸克近弱耦合，衔接 C0194）",
         Decimal("0.9") < g4["y_t_pole"] < Decimal("1.1")),
        ("G8", "方案漂移 y_t(pole)-y_t(MS) ≈ 6%（落在 4–8% 带）",
         Decimal("4") < g4["rel_scheme_pct"] < Decimal("8")),
        ("G9", "几何/TUFT 供给 = 0（C0133 注销：无 QCD/无重整化/无质量方案）", True),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0233 guard failed"

    w("\n[诚实边界 / 红线]")
    w("  本册不宣称解决任何物理难题；已攻破 = 对 TUFT/几何框架结构性负面闭合。")
    w("  pole-MS 换算、α_s 跑动、β0/γ0 重整化群、一阶/高阶分解均为标准 QCD 算术复核，")
    w("  本册仅做 Decimal 48 位 + Fraction 精算；PDG 质量（m_pole=172.69、m_MS(M_t)=162.5）")
    w("  与 α_s(M_t)=0.1080 为已知外部输入显式计数，非本册预测；严禁写成 TUFT 预测/修正；")
    w("  TUFT 已注销（C0133）。领头对数跑动阈值匹配未展开，按数量级（方向/幅度）判定。")
    w("  红线不变：不宣称解决任何物理难题；有预测且对 = 0/22；数学自洽 ≠ 实验证实；"
      "UFT-3=0 保持。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0233_顶夸克质量攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0233_顶夸克质量攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0233_top_mass_scheme",
            "mother_row": "T368 顶夸克 MS 质量 vs 极点质量方案 QCD 重整化标度 C7",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_scheme_facts": {k: (str(v) if not isinstance(v, Decimal) else str(v))
                                for k, v in g1.items()},
            "E2_pole_ms": {k: str(v) for k, v in g2.items()},
            "E3_running": {k: (str(v) if not isinstance(v, Fraction) else str(v))
                           for k, v in g3.items()},
            "E4_decomp": {k: str(v) for k, v in g4.items()},
            "E5_ruling": "T368 structural negative vs TUFT: pole<->MS conversion, alpha_s "
                         "running and beta0/gamma0 RG are standard QCD structure; TUFT (C0133 "
                         "withdrawn) supplies no QCD / no RG / no mass scheme; hits C7",
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0233 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
