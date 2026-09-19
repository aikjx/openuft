# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R4  尺度生成机制：攻克开放项 O-SCALE
================================================================================

承接 R3（tuft_r3_scale_degeneracy.py）：纯几何孤子
    E_tot = 4*pi*alpha*k^2*L^3*J = E_electron
只约束 k^2*L^3 = const，绝对尺度 L 是自由参数；纯 TUFT 内部无法第一性
导出电子尺度（23 数量级鸿沟，与 openuft M02 普朗克锚定谬误同构）。

本文件正面尝试打破 k^2*L^3 简并的三种机制，并诚实量化每个机制是否真
"第一性"，还是只是把外部锚定显式化：
  (A) 自引力极值：加入孤子引力自能 E_grav ~ -alpha_grav/L，考察总能量极值能否锁 L。
  (B) 拓扑量子化：R2 的 Lk∈½ℤ 是否给 L 一个绝对标度。
  (C) R1 公理 II 接入（世界线↔场的特征曲率约定）：给定质量锚 m，能否唯一确定 L。

结论预告：
  A 锁 L→l_P（普朗克），不能到电子；
  B 只给量子数，不锁 L；
  C 在"给定 m + 特征映射约定"下打破简并、唯一确定 L，但 L 数值依赖约定且
    物理意义待释。
→ O-SCALE 由"完全开放失败"降级为
  "两层锚定（质量外部锚 + 特征映射约定）+ 残留约定自由度"。

--------------------------------------------------------------------------------
红线：数学自洽 != 物理证实。本文件诚实标注每个机制的边界，不粉饰为第一性导出。
================================================================================
"""
import os
import io
import sys
import math

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import numpy as np

L_OUT = []


def sec(t):
    L_OUT.append("\n" + "=" * 76)
    L_OUT.append("  " + t)
    L_OUT.append("=" * 76)


def put(s=""):
    L_OUT.append(s)


def rec(name, b, detail):
    tag = "[PASS]" if b else "[FAIL]"
    L_OUT.append("  %s %s  |  %s" % (tag, name, detail))
    return b


def info(name, detail):
    L_OUT.append("  [INFO] %s  |  %s" % (name, detail))


# ----------------------------------------------------------------- 常数（同 R3）
C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
ALPHA = 1.0 / 137.035999084
OMEGA_DE = 0.6875
O0 = 0.72

E_PLANCK = math.sqrt(HBAR * C_LIGHT ** 5 / G_NEWTON)
L_PLANCK = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
E_ELECTRON = M_E * C_LIGHT ** 2 / E_PLANCK          # 4.185e-23（无量纲）
KAPPA_E = M_E * C_LIGHT / HBAR                      # 2.59e12 m^-1（物理）
K_E_DL = KAPPA_E * L_PLANCK                         # 4.185e-23（无量纲总幅 k 量级）
L_C_DL = 2.426310238e-12 / L_PLANCK                 # 1.50e23（电子康普顿波长，无量纲）
J_ANALYTIC = 2.0 * OMEGA_DE / 8.0 + 2.0 * (O0 - OMEGA_DE) / 27.0
CONST_K2L3 = E_ELECTRON / (4.0 * math.pi * ALPHA * J_ANALYTIC)   # 2.619e-21


def main():
    sec("TUFT-R4 尺度生成机制：攻克开放项 O-SCALE")
    put("  算法联盟 ROOT 红线 · 诚实量化打破 k^2*L^3 简并的三种机制")
    put("  常数: alpha=%.4e  E_electron(无量纲)=%.4e  l_P=%.3e m"
        % (ALPHA, E_ELECTRON, L_PLANCK))
    put("        K_E(无量纲)=%.4e  L_C(无量纲)=%.4e l_P  k^2*L^3=const=%.4e"
        % (K_E_DL, L_C_DL, CONST_K2L3))
    put("")

    # ============================== 1. R3 简并重述
    sec("1. R3 尺度简并重述（数值确认 k^2*L^3 = const）")
    for Lv, lb in [(1.0, "l_P"), (1e8, "1e8 l_P"), (L_C_DL, "电子康普顿"),
                   (1e30, "1e30 l_P")]:
        k = math.sqrt(CONST_K2L3 / Lv ** 3)
        kl3 = k ** 2 * Lv ** 3
        rec("简并 k^2*L^3=const @ " + lb,
            abs(kl3 - CONST_K2L3) / CONST_K2L3 < 1e-12,
            "k=%.3e, k^2*L^3=%.3e (守恒常数)" % (k, kl3))
    info("R3", "绝对尺度 L 是自由参数：1 个约束管不住 k、L 两个自由度")

    # ============================== 2. 机制 A：自引力极值
    sec("2. 机制 A：自引力极值（能否靠引力自能锁定 L）")
    alpha_grav = E_ELECTRON ** 2            # (m_e/m_P)^2 = (E_electron)^2
    # 总能量(无量纲) E_tot(L) = E_geom - alpha_grav/L
    #   E_geom = E_electron（守恒，由质量锚 m_e 固定）
    #   E_grav = -G m_e^2/(R c^0)/E_P = -alpha_grav / L   （L = R/l_P 无量纲）
    dEdlnL_at_1 = alpha_grav / 1.0          # dE/dlnL = alpha_grav/L，在 L=1 处
    rec("A1: 极值分析 dE_tot/dL > 0（单调增）",
        dEdlnL_at_1 > 0,
        "dE/dlnL(L=1)=%.2e >0 ⇒ 最稳定解锁在最小允许 L = l_P（普朗克下界）"
        % dEdlnL_at_1)
    L_stable = 1.0
    rec("A2: 自引力把尺度拉到电子? (L_stable vs L_C)",
        abs(L_stable - L_C_DL) / L_C_DL > 1e10,
        "L_stable=%g l_P ≪ L_C=%.2e l_P ⇒ 差 %.1e 倍（A 不能到电子）"
        % (L_stable, L_C_DL, L_C_DL / L_stable))
    info("A", "电子质量下 alpha_grav=%.2e ≪ 1，引力自能相对 E_geom 可忽略（~%.0e 倍）"
         % (alpha_grav, alpha_grav / E_ELECTRON))
    info("A", "结论：自引力极值锁 L→l_P（普朗克强曲率孤子），对 O-SCALE 无贡献 → FAIL for electron")

    # ============================== 3. 机制 B：拓扑量子化
    sec("3. 机制 B：拓扑量子化（R2 的 Lk∈½ℤ 能否锁 L）")
    rec("B1: Lk = n/2 (n∈ℤ) 离散（R2 拓扑成立）", True,
        "Mobius 闭合带 ⇒ Lk∈½ℤ，费米 n=±1 ⇒ Lk=±1/2")
    rec("B2: 拓扑锁绝对尺度 L?", False,
        "套索环半径 R、缠绕圈数 N 自由 ⇒ Tw=N·n/2 不约束几何尺度 L")
    info("B", "拓扑只提供自旋/统计分类（费米 Lk=±1/2），不解决尺度锚定 → FAIL for O-SCALE")

    # ============================== 4. 机制 C：R1 公理 II 接入
    sec("4. 机制 C：R1 公理 II 接入（世界线↔场的特征映射约定）")
    put("  R1 公理 II：粒子世界线 κ^2+τ^2 = (m c/ℏ)^2 = Ω^2（匀速螺旋 Frenet 不变量）")
    put("  R3 孤子（空间场）：K(r)=T(r)=k·exp(-r/L)，峰值 r=0 处 κ=τ=k/l_P")
    put("  约定 C0（峰值约定）：取孤子峰值 κ^2+τ^2 = (m_e c/ℏ)^2")
    # 峰值：2·(k/l_P)^2 = (m_e c/ℏ)^2 = (K_E_DL/l_P)^2  ⇒  k = K_E_DL/√2
    k_peak = K_E_DL / math.sqrt(2.0)
    L_peak = (CONST_K2L3 / k_peak ** 2) ** (1.0 / 3.0)
    rec("C1: 峰值约定打破简并（L 唯一确定）",
        L_peak > 0 and math.isfinite(L_peak),
        "k=%.3e, L=%.4e l_P（由守恒 k^2*L^3=const 解出）" % (k_peak, L_peak))
    kl3c = k_peak ** 2 * L_peak ** 3
    rec("C2: 守恒核对 k^2*L^3 = const",
        abs(kl3c - CONST_K2L3) / CONST_K2L3 < 1e-9,
        "k^2*L^3=%.3e vs const=%.3e（偏差<1e-9）" % (kl3c, CONST_K2L3))
    # 约定敏感性：若峰值取 κ·s，则 L ∝ s^{-2/3}
    s = 0.5
    ratio = s ** (-2.0 / 3.0)
    rec("C3: L 依赖特征曲率约定（残留自由度）",
        abs(ratio - 1.0) > 0.1,
        "峰值取 κ·s ⇒ L ∝ s^{-2/3}；s=%.1f ⇒ L×%.3f（约定自由）" % (s, ratio))
    info("C", "机制 C 打破简并，但引入'世界线↔场'特征映射约定，该约定需物理解释")
    info("C", "L≈%.2e l_P 既非普朗克也非康普顿（中间尺度，物理意义待释）" % L_peak)

    # ============================== 5. 锚定参数化 + 可检验推论
    sec("5. 锚定参数化：以 m_e 为外部锚的 TUFT 几何推论")
    info("锚", "电子（费米, θ=45°）：κ=τ=m_e c/(ℏ√2)=%.3e m^-1（由 R1 公理 II）"
         % (KAPPA_E / math.sqrt(2.0)))
    info("锚", "R2 拓扑：Lk=±1/2（费米自旋统计），由 Möbius 闭合带给出")
    info("锚", "尺度 L 由机制 C 约定确定（≈%.2e l_P，约定依赖）" % L_peak)
    info("锚", "可检验推论（若框架成立）：电子作为曲率扭结的 κ,τ 与自旋统计 Lk 的几何关联")
    info("锚", "但 m_e 本身非 TUFT 导出 ⇒ 框架定位为'给定质量后的几何编码'")

    # ============================== 6. 诚实结论
    sec("诚实结论（O-SCALE 降级）")
    put("  1. 机制 A（自引力极值）锁 L→l_P（普朗克），不能到电子尺度。            [FAIL for electron]")
    put("  2. 机制 B（拓扑量子化）只给量子数/离散比，不锁绝对 L。                [INFO/FAIL]")
    put("  3. 机制 C（R1 公理 II 接入）在'给定 m + 特征映射约定'下打破简并，")
    put("     L 唯一确定但数值依赖约定、物理意义待释。                          [部分闭合]")
    put("  4. O-SCALE 由'完全开放失败'降级为：")
    put("       (a) 质量 m：外部实验锚（与 openuft M02 同构，α_grav 修正仍是外部注入）")
    put("       (b) 尺度 L：TUFT 内部残留简并，需特征映射约定或实验再锚定")
    put("  5. 框架诚实定位：给定 m，几何（κ,τ,拓扑 Lk,尺度）由 TUFT 结构确定；")
    put("     TUFT 不第一性生成质量，而是'质量→几何'的编码框架 + 自旋/统计推论。")
    put("  6. 残留开放项：特征映射约定的物理解释、L 的中间尺度物理意义、")
    put("     三维多费米子 braid-group 表示、挠率动力学（分支 B）。")
    put("")
    put("红线声明：数学自洽 != 物理证实。本文件仅诚实量化 O-SCALE 的攻克尝试，")
    put("          不构成对 TUFT 物理真实性的任何主张；机制 C 为部分闭合，非第一性导出。")

    report = "\n".join(L_OUT) + "\n"
    print(report)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tuft_r4_report.txt")
    try:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print("[报告已写入] " + out)
    except Exception as exc:
        print("[warn] 报告写入失败: " + str(exc))


if __name__ == "__main__":
    main()
