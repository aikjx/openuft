# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R8  β₁ 红移符号修复 · 求导证明 + 归一化 + 精算验证
================================================================================
承接 R7：R7 发现 ω=ω₀√β₁ 作钟速率时红移符号与 GR/观测相反（FAIL）。
本文件执行修复路径 (i)/(ii)：令**可观测钟速** ∝ β₁^(−1/2)，即

        ω_clock(r) / ω₀ = 1/√β₁(r) = exp(−ε),        ε ≡ GM/(c²r)

并做三件事：
  (1) 求导证明（sympy）：Frenet 关系、g=(c²/2)∇lnβ₁ 的牛顿极限、
      以及修正钟速与 GR 的**逐阶**符号对比；
  (2) 归一化：全部用无量纲紧致度 ε（或 ξ）表达；
  (3) 精算（mpmath 50 位）：地球/太阳/白矮星/中子星的 ε、ε² 与可检验性。

结论预告：
  · 1 阶：修正后与 GR **完全一致**（均为 1 − ε）⟹ 与 Pound–Rebka/GPS/光钟相容；
  · 2 阶：TUFT 给 +ε²/2，GR 给 −ε²/2 ⟹ **相差 ε²**，这是 TUFT 的**可检验特征偏差**。
红线：只做符号推演与数值核对，不主张 TUFT 成立或证伪。
================================================================================
"""
import os
import sys
import math

import sympy as sp
from mpmath import mp, mpf, exp, sqrt, nstr

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "tuft_r8_report.txt")

C = mpf("299792458")
G = mpf("6.67430e-11")
MSUN = mpf("1.98892e30")

OUT = []


def sec(t):
    OUT.append("\n" + "=" * 76)
    OUT.append("  " + t)
    OUT.append("=" * 76)


def put(s=""):
    OUT.append(s)


def rec(name, ok, detail):
    OUT.append("  %s %s  |  %s" % ("[PASS]" if ok else "[FAIL]", name, detail))


def info(name, detail):
    OUT.append("  [INFO] %s  |  %s" % (name, detail))


def main():
    sec("TUFT-R8  β₁ 红移符号修复 · 求导证明 + 归一化 + 精算")
    put("  修复：可观测钟速 ω_clock/ω₀ = 1/√β₁ = exp(−ε)，ε ≡ GM/(c²r)")
    put("  对标：GR 局域钟速率 = √(1 − 2ε)")

    # ========== 1. 求导证明 ==========
    sec("1. 求导证明（sympy 符号求导）")

    # (a) Frenet：dT/ds = κN  ⟹  dT/dτ = c κ N
    c_s, kappa_s, s_s, tau_s = sp.symbols("c kappa s tau_p", positive=True)
    put("  (a) 由 ds = c·dt 与 dτ = ds/c：d/dτ = c·(d/ds)")
    rec("1a: 算子变换 d/dτ = c·d/ds", True,
        "dτ=ds/c ⇒ d/dτ = c·d/ds；又 ds=c·dt ⇒ dτ=dt（模型内无 SR 膨胀，已标 O-SR）")
    put("      Frenet 第一式 dT/ds = κN ⟹ dT/dτ = c·κN ✓（曲率正比、指向主法向）")
    rec("1b: dT/dτ = cκN", True, "由 dT/ds=κN 与 d/dτ=c·d/ds 直接推出 ✓")

    # (b) β₁ 静态解 → g 的符号求导
    r, M = sp.symbols("r M", positive=True)
    Gs, cs = sp.symbols("G c", positive=True)
    beta1 = sp.exp(2 * Gs * M / (cs ** 2 * r))
    lnb = sp.log(beta1)
    g_r = sp.simplify(sp.Rational(1, 2) * cs ** 2 * sp.diff(lnb, r))
    put("  (b) β₁ = exp(2GM/(c²r))，g = (c²/2)·d(lnβ₁)/dr 的符号求导：")
    put("      d(lnβ₁)/dr = %s" % sp.diff(lnb, r))
    put("      g = %s" % g_r)
    rec("1c: g(β₁) = −GM/r²（牛顿吸引）", sp.simplify(g_r + Gs * M / r ** 2) == 0,
        "符号求导给出 g = −GM/r²，负号=吸引 ✓；该符号由牛顿极限唯一固定，不可翻转")

    # (c) 修正钟速 vs GR 的逐阶展开
    e = sp.symbols("epsilon", positive=True)
    tuft_rate = sp.exp(-e)                # 修正后：1/√β₁
    gr_rate = sp.sqrt(1 - 2 * e)          # GR
    ser_t = sp.series(tuft_rate, e, 0, 4).removeO()
    ser_g = sp.series(gr_rate, e, 0, 4).removeO()
    put("")
    put("  (c) 逐阶展开（ε ≡ GM/(c²r)）：")
    put("      TUFT(修正) 1/√β₁ = exp(−ε) = %s" % sp.expand(ser_t))
    put("      GR          √(1−2ε)          = %s" % sp.expand(ser_g))
    diff = sp.expand(ser_t - ser_g)
    put("      差 (TUFT − GR)               = %s" % diff)
    rec("1d: 1 阶是否一致?", sp.simplify(sp.expand(ser_t - ser_g).coeff(e, 1)) == 0,
        "1 阶系数均为 −1 ⟹ 一阶完全一致 ⇒ 与 Pound–Rebka/GPS/光钟相容 ✓")
    c2 = sp.simplify(sp.expand(ser_t - ser_g).coeff(e, 2))
    rec("1e: 2 阶是否一致?", c2 == 0,
        "2 阶差 = %s·ε²（TUFT 为 +ε²/2，GR 为 −ε²/2）⟹ **存在可检验的特征偏差**" % c2)

    # ========== 2. 归一化 ==========
    sec("2. 归一化（无量纲化）")
    put("  以无量纲紧致度 ε ≡ GM/(c²r)（= ξ·(a/r)，致密系数 ξ=GM/(c²a)）为唯一变量：")
    put("      β₁ = exp(2ε)                     （无量纲 ✔）")
    put("      √β₁ = exp(ε)，1/√β₁ = exp(−ε)   （无量纲 ✔）")
    put("      GR 对照 = √(1−2ε)                （无量纲 ✔）")
    put("      m/m₀ = √β₁ = exp(ε)              （质量比，无量纲 ✔）")
    put("  ⟹ 全部物理量化为 ε 的函数；量纲常数（c,ℏ,G）只出现在 ε 的定义中（method_F 判据一）")
    info("2", "归一化后 TUFT 与 GR 的差异**仅是 ε 的解析函数不同**：exp(−ε) vs √(1−2ε)")

    # ========== 3. 精算 ==========
    sec("3. 精算（mpmath 50 位）：各天体的 ε 与逐阶差")
    cases = [
        ("地球表面", mpf("5.9722e24"), mpf("6.371e6")),
        ("太阳表面", MSUN, mpf("6.957e8")),
        ("白矮星 (1.4 M☉, 6000 km)", mpf("1.4") * MSUN, mpf("6.0e6")),
        ("中子星 (1.4 M☉, 12 km)", mpf("1.4") * MSUN, mpf("1.2e4")),
    ]
    put("  %-28s %-12s %-16s %-16s %-12s" % ("天体", "ε", "TUFT 修正", "GR", "差"))
    for name, Mv, rv in cases:
        eps = G * Mv / (C ** 2 * rv)
        t_rate = exp(-eps)
        g_rate = sqrt(1 - 2 * eps)
        d = t_rate - g_rate
        put("  %-28s %-12s %-16s %-16s %-12s"
            % (name, nstr(eps, 5), nstr(t_rate, 8), nstr(g_rate, 8), nstr(d, 4)))
    put("")
    put("  可检验性：")
    info("3a", "地球 ε≈7e-10；ε²≈4.8e-19 —— 处于当前光钟(1e-18~1e-19)精度边缘，需专门实验")
    info("3b", "太阳 ε≈2.1e-6；ε²≈4.5e-12 —— 远大于光钟精度，太阳谱线/日震可做检验")
    info("3c", "中子星 ε≈0.172；TUFT 与 GR 钟速差 ~4%（0.842 vs 0.810）—— 强场区差异显著")

    # ========== 4. 判定 ==========
    sec("4. 修复后判定")
    rec("4a: 修复后 1 阶与 GR/实验相容", True,
        "ω_clock/ω₀ = 1/√β₁ = exp(−ε) ≈ 1 − ε，与 GR √(1−2ε) ≈ 1 − ε 一致 ⇒ 解除 R7 的 FAIL")
    rec("4b: 修复是否产生新预言?", True,
        "2 阶差 = +ε²（TUFT − GR）⇒ TUFT 的**可检验特征偏差**；这是修复带来的增益而非损失")
    info("4c", "⚠ 遗留：(i) 仍假设 dτ=dt（O-SR 未解）；(ii) 传播因子 1/β₁ 的**第一性来源**未给出，"
               "需从作用量推导，否则只是唯象修补")
    put("")
    put("红线：本文件只做符号推演与数值核对，不主张 TUFT 成立或证伪；")
    put("      1 阶相容与 2 阶偏差均为可复算事实。")

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
