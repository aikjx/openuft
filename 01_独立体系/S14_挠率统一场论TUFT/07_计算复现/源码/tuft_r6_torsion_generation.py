# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R6  阶段0：挠率产生机制的第一性可行性判定
================================================================================
背景：TUFT-R5 修复版 §8 指出——地面挠率探测方案的可行性完全依赖
      「人工挠率谐振腔可产生 T ~ 1e-4 s^-1」这一未证前提（与 EC 自然耦合差 ~1e28）。

本文件对该前提做第一性判定，回答三问：
  A. 源方程：实验室自发挠率的自然量级是多少？（爱因斯坦-嘉当代数约束）
  B. 传播性：挠率能否传播？—— 这是「谐振腔」成立的前提。
  C. 共振放大：谐振放大能否桥接 1e28 缺口？（Q 因子上限）
  D. 所需耦合：若要 T=1e-4，需多大耦合 κ_new？是否被现有实验排除？
  E. 结论：可行性清单（要证明什么，才能宣布可执行）

红色声明：本文件只做量纲/量级/可传播性的第一性判定，不主张 TUFT 成立或证伪。
================================================================================
"""
import os
import sys
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "tuft_r6_report.txt")

# 常数
C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054571817e-34
MUB = 9.2740100783e-24
NA = 6.02214076e23
M_FE = 55.845e-3
RHO_FE = 7874.0
EV = 1.602176634e-19

OUT = []


def sec(t):
    OUT.append("\n" + "=" * 78)
    OUT.append("  " + t)
    OUT.append("=" * 78)


def put(s=""):
    OUT.append(s)


def rec(name, ok, detail):
    OUT.append("  %s %s  |  %s" % ("[PASS]" if ok else "[FAIL]", name, detail))


def info(name, detail):
    OUT.append("  [INFO] %s  |  %s" % (name, detail))


def main():
    sec("TUFT-R6 阶段0：挠率产生机制的第一性可行性判定")
    put("  目标：判定『人工挠率谐振腔产生 T~1e-4 s^-1』是否可行")
    put("  标尺：爱因斯坦-嘉当（EC）自然耦合 = 现有实验允许的『标准』上限")

    # ======================= A. 源方程与实验室量级 =======================
    sec("A. 源方程：实验室自发挠率的自然量级")
    n_fe = RHO_FE / M_FE * NA
    s_spin = n_fe * 1.1 * HBAR                     # 自旋密度 kg/(m·s)
    info("A", "Fe 自旋密度 n=%.3e /m^3, s=1.1ħ·n=%.3e kg/(m·s)" % (n_fe, s_spin))
    kappa_EC_len = G / C ** 3                       # T[m^-1] = (G/c^3)·s
    kappa_EC_freq = G / C ** 2                      # 频率单位（×c）
    T_EC_len = kappa_EC_len * s_spin
    T_EC_freq = kappa_EC_freq * s_spin
    info("A", "EC 耦合系数：G/c^3=%.4e（长度制）; G/c^2=%.4e（频率制）"
         % (kappa_EC_len, kappa_EC_freq))
    rec("A: 实验室自发挠率（EC）",
        True,
        "T_EC = %.3e m^-1 = %.3e s^-1（10g Fe 充分偏振）" % (T_EC_len, T_EC_freq))
    T_target = 1e-4
    gap = T_target / T_EC_freq
    rec("A: 与目标 T=1e-4 s^-1 的缺口", False,
        "相差 %.2e 倍（≈10^%.1f）；需自旋密度 %.3e kg/(m·s)（超核密度 1e13 倍）"
        % (gap, math.log10(gap), T_target / kappa_EC_freq))
    n_nuc = 1e44
    T_nuc = kappa_EC_freq * (n_nuc * 1.1 * HBAR)
    info("A", "即便用核物质密度（n~%.0e/m^3），T_EC 仍仅 ~%.1e s^-1，差目标 ~10^%.0f 倍"
         % (n_nuc, T_nuc, math.log10(T_target / T_nuc)))

    # ======================= B. 传播性判定 =======================
    sec("B. 传播性判定（谐振的前提）")
    put("  谐振腔成立的必要条件：挠率场有【动能项】→ 有波动方程 → 有本征频率。")
    put("")
    put("  B1. 爱因斯坦-嘉当（EC）：作用量仅含 R（无 T^2 项）")
    put("      ⇒ 挠率方程是【代数约束】T = f(自旋)，无 ∂T 项 ⇒ **不传播、无波、无本征模**。")
    rec("B1: EC 挠率是否可驱动谐振?", False,
        "代数约束场没有自由度，不能被『泵浦』到共振——『挠率谐振腔』在 EC 框架内不存在")
    put("")
    put("  B2. 动力学挠率（Poincaré 规范 / f(T) / Einstein-Cartan-Proca）：需给 T 加动能项")
    put("      此时挠率有质量 m_T，Compton 波长 λ_T = ħ/(m_T c)。")
    for lam in [1e-2, 1.0, 1e3]:
        m_T = HBAR / (C * lam)
        m_T_eV = m_T * C * C / EV
        info("B2", "λ_T=%.0e m ⇒ m_T=%.3e kg = %.3e eV" % (lam, m_T, m_T_eV))
    put("      判据 5 要求 λ_T 在实验室尺度（~cm–m）可分辨 ⇒ m_T ~ 1e-5–1e-7 eV。")
    rec("B2: 如此轻的挠率场是否自由?", False,
        "λ_T~cm–m ⇒ m_T~1e-5–1e-7 eV；该质量区的『引力强度第五力』已被 Casimir/原子/中子实验严厉约束，"
        "除非耦合远弱于引力（那又无法产生 1e-4 s^-1）")
    put("")
    put("  ⇒ B 结论：EC 内无谐振；动力学挠率可以传播，但（i）需显式构造动能项与质量，")
    put("     （ii）实验可及的 λ_T 对应已被约束的轻场。**『挠率谐振腔』在两条路径上都未被建立。**")

    # ======================= C. 共振放大上限 =======================
    sec("C. 共振放大能桥接 1e28 缺口吗？（Q 因子上限）")
    put("  受迫谐振子在共振时的放大倍数 A ≈ Q（品质因子）。")
    Qs = [("超导射频腔", 1e10), ("光学微腔", 1e11), ("石英机械振子", 1e9),
          ("原子钟/光学晶格", 1e15)]
    for name, Q in Qs:
        info("C", "%s：Q ~ %.0e" % (name, Q))
    Q_max = 1e15
    rec("C: 需要 Q~1e28 才能放大 1e28", False,
        "现有最佳 Q ~ 1e15 ⇒ 缺口仍 10^%.0f 倍——**共振原理不可能桥接 1e28**" % math.log10(gap / Q_max))
    put("  注：即便 Q=1e15（比最佳腔高 4 个量级），也只补 15 个数量级，缺口仍有 13 个数量级。")

    # ======================= D. 所需新耦合 κ_new =======================
    sec("D. 若要 T=1e-4 s^-1，需多大耦合？是否被排除？")
    kappa_new = T_target / s_spin                  # 频率制：T[s^-1]=κ_new·s
    ratio = kappa_new / kappa_EC_freq              # 相对 EC
    info("D", "所需耦合 κ_new = T/s = %.3e（频率制，m/kg）" % kappa_new)
    info("D", "对比 EC 耦合 G/c^2 = %.3e ⇒ κ_new/κ_EC = %.2e" % (kappa_EC_freq, ratio))
    rec("D: κ_new 是否被现有实验排除?", False,
        "放大 %.0e 倍的挠率耦合会显著改变自旋-自旋力、自旋进动与等效原理检验；"
        "自旋陀螺仪/EP 实验对挠率耦合的约束 ≲ O(1)×EC ⇒ κ_new~1e28×EC **被排除**" % ratio)
    put("")
    put("  ⇒ D 结论：要合法地产生 T=1e-4 s^-1，必须给出一个**非 G 抑制、且不被现有实验排除**的耦合机制——")
    put("     这正是 TUFT 至今【缺失】的核心推导。")

    # ======================= E. 可行性清单 =======================
    sec("E. 结论：可行性清单（要证明什么，才能宣布可执行）")
    put("  当前判定：『人工挠率谐振腔产生 T~1e-4 s^-1』——**可行性未建立**，三条独立路径均受阻：")
    put("    (A) EC 自然源：T~1e-33 s^-1，差 1e28（需自旋密度 1e57 /m^3，超核密度 1e13 倍）。")
    put("    (B) 谐振放大：需 Q~1e28，现有最佳 ~1e15，差 1e13（且 EC 挠率根本不传播）。")
    put("    (C) 新耦合：需 κ~1e28×EC，被自旋/EP 实验排除。")
    put("")
    put("  要推翻上述判定，TUFT 必须提供【至少一项】：")
    put("    1. 挠率的动力学作用量（动能项 + 质量项），显式给出 m_T 与 λ_T；")
    put("    2. 一个非引力强度（κ ≫ G/c²）的产生机制，并证明其不被自旋-自旋/EP 实验排除；")
    put("    3. 或指出 T 与自旋密度无关的第三种源（如拓扑荷、额外维度投影），并给出量级。")
    put("")
    put("  在提供上述任一项之前，本实验方案应维持『预研』定位，其灵敏度结论（§2–§7）虽自洽，")
    put("  但对应的是一个**尚未证明可被激发的信号**。")
    put("")
    put("红线声明：本文件为量级/可传播性的第一性判定，不主张 TUFT 成立或证伪；")
    put("         判定基于 EC 标准耦合与公开实验约束，若 TUFT 提出新机制，应以新机制重做本清单。")

    txt = "\n".join(OUT) + "\n"
    print(txt)
    try:
        with open(REPORT, "w", encoding="utf-8") as fh:
            fh.write(txt)
        print("[报告已写入] " + REPORT)
    except Exception as exc:
        print("[warn] " + str(exc))


if __name__ == "__main__":
    main()
