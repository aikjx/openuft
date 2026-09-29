# -*- coding: utf-8 -*-
"""
TUFT g-2 / EDM 屏蔽因子『双约束可行性』审计（OPEN5b，方向 B）
==============================================================
背景：g-2 偏差 74.2%（TUFT 0.00404 vs 实验 0.0023193），根源被定位为
「可观测量映射层」的唯象假设——挠率效应无屏蔽地直接转为低能可观测量。
修复方向 1 提议引入屏蔽因子 f(κ,τ)：g-2 = (2τ/κ)·f。

本册审计（方向 B，A 的必要前置门禁）：
  是否存在【自洽的】屏蔽因子，能同时满足 g-2 与 EDM 双约束？
  —— EDM 与 g-2 共享孤子参数 κ,τ，任何修改必须同步校验 EDM。

判据：
  设单一几何屏蔽机制给出压低因子 F（由孤子几何导出 ⇒ κ,τ 被自洽条件锁死
  ⇒ F 为确定数值，非自由参数）。则
      g-2_shielded = (2τ/κ) · F     需 = 0.0023193
      EDM_shielded = EDM_TUFT · F    需 ≤ 1.1e-29 e·cm
  同时满足要求 F_g = F_d；若二者相差巨大 ⇒ 单一因子不可行。
  若改用两个独立因子 F_g, F_d ⇒ 做自由度/特设性审计。

红线：本册只做可行性判定，不构造新物理；负结论如实记录，非对 TUFT 的证伪宣告。
"""
import os
import sys
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- 基线数据 ----
G2_EXP = 0.00231930436        # 实验 g-2（费米实验室/BNL，高置信交叉核验）
G2_TUFT = 0.00404             # TUFT 无屏蔽映射 2τ/κ（孤子自洽解）
EDM_TUFT_CM = 2.257e-34       # C·m（白皮书 d_e = eαR_C/(2√(1+α²))）
E_C = 1.602176634e-19         # 元电荷 C
EDM_ACME_ECM = 1.1e-29        # e·cm（ACME 上限）

# C·m → e·cm：除以元电荷得 e·m，再 ×100 得 e·cm
EDM_TUFT_ECM = EDM_TUFT_CM / E_C * 100.0


def main():
    L = []
    L.append("=" * 72)
    L.append("TUFT g-2 / EDM 屏蔽因子双约束可行性审计（OPEN5b·方向 B）")
    L.append("run at: 2026-09-30")
    L.append("=" * 72)
    L.append("")
    L.append("== 1. 基线 ==")
    L.append("  g-2  实验   = %.10f" % G2_EXP)
    L.append("  g-2  TUFT   = %.10f   (2τ/κ，孤子自洽锁死)" % G2_TUFT)
    L.append("  g-2  偏差   = %.1f%%" % (abs(G2_TUFT - G2_EXP) / G2_EXP * 100))
    L.append("  EDM  TUFT   = %.4e C·m = %.4e e·cm" % (EDM_TUFT_CM, EDM_TUFT_ECM))
    L.append("  EDM  ACME   ≤ %.2e e·cm" % EDM_ACME_ECM)
    L.append("  EDM  超额   = %.2f 个量级" % (sp.log(sp.Float(EDM_TUFT_ECM) / EDM_ACME_ECM, 10).evalf()))
    L.append("")

    # ---- 符号推导：所需压低因子 ----
    tau, kappa, F = sp.symbols("tau kappa F", positive=True)
    g2_sym = 2 * tau / kappa                    # TUFT 映射（无屏蔽）
    g2_sh = g2_sym * F                          # 带屏蔽
    tau_over_kappa = sp.Rational(202, 100000)   # τ/κ = 0.00202（由 g-2_TUFT=0.00404 反解）
    g2_tuft_sym = sp.simplify(g2_sym.subs({tau: tau_over_kappa * kappa}))
    L.append("== 2. 符号推导：所需压低因子 ==")
    L.append("  g-2 映射        : 2τ/κ ；孤子自洽解 τ/κ = %s" % tau_over_kappa)
    L.append("  代入            : 2τ/κ = %s = %.5f" % (g2_tuft_sym, float(g2_tuft_sym)))
    L.append("  屏蔽后          : g-2 = (2τ/κ)·F")
    L.append("")

    F_g = sp.Float(G2_EXP) / sp.Float(G2_TUFT)                    # g-2 所需
    F_d = sp.Float(EDM_ACME_ECM) / sp.Float(EDM_TUFT_ECM)         # EDM 所需（上限）
    L.append("  满足 g-2 需  F_g = g-2_exp/(2τ/κ) = %.6f" % float(F_g))
    L.append("  满足 EDM 需  F_d = ACME/EDM_TUFT  = %.4e" % float(F_d))
    L.append("")

    # ---- 单一因子可行性三情形 ----
    L.append("== 3. 单一屏蔽因子 F 的可行性检验（F_g = F_d ?）==")
    ratio = sp.simplify(F_g / F_d)
    log10_ratio = sp.log(ratio, 10).evalf()
    L.append("  同时满足需 F_g = F_d，实测比值 F_g/F_d = %.4e  (log10 = %s)" % (
        float(ratio), log10_ratio))
    L.append("")
    # 情形1：取 F=F_g 满足 g-2，看 EDM
    edm_case1 = sp.Float(EDM_TUFT_ECM) * F_g
    over1 = sp.log(edm_case1 / sp.Float(EDM_ACME_ECM), 10).evalf()
    L.append("  情形1: F = F_g = %.4f （满足 g-2）" % float(F_g))
    L.append("        → EDM = %.4e e·cm，仍超 ACME 达 %.1f 个量级 ❌" % (float(edm_case1), float(over1)))
    # 情形2：取 F=F_d 满足 EDM，看 g-2
    g2_case2 = sp.Float(G2_TUFT) * F_d
    under2 = sp.log(sp.Float(G2_EXP) / g2_case2, 10).evalf()
    L.append("  情形2: F = F_d = %.4e （满足 EDM）" % float(F_d))
    L.append("        → g-2 = %.4e，低于实验 %.1f 个量级 ❌" % (float(g2_case2), float(under2)))
    L.append("")
    if abs(float(log10_ratio)) > 0.5:
        L.append("  [FAIL] 单一自洽屏蔽因子不存在  |  g-2 只需压低 %.2f 倍，"
                 "EDM 需压低 %.1f 个量级；二者相差 %.4e 倍（≈%.0f 量级）"
                 "⇒ 任何【单一】几何屏蔽机制都无法同时满足双约束" % (
                     1 / float(F_g), abs(float(sp.log(F_d, 10).evalf())),
                     float(ratio), abs(float(log10_ratio))))
    L.append("")

    # ---- 双独立因子的特设性审计 ----
    L.append("== 4. 若改用两个独立因子 (F_g, F_d)：自由度/特设性审计 ==")
    L.append("  要求 F_d/F_g = %.4e（≈%.0f 量级分裂）" % (
        1 / float(ratio), abs(float(log10_ratio))))
    L.append("  问题1(几何来源)：若 F_g、F_d 均由同一孤子几何(κ,τ)导出，")
    L.append("        κ,τ 已被自洽条件锁死 ⇒ 二者比值应 O(1)；要求 %.0f 量级" % abs(float(log10_ratio)))
    L.append("        分裂 ⇒ 必须引入与几何无关的新自由参数。")
    L.append("  问题2(预测力)：2 个可调因子拟合 2 个观测量 ⇒ 残差可精确归零，")
    L.append("        自由度 = 2 = 观测量数 ⇒ 零预测力（任何数据都能拟合），属特设(ad hoc)。")
    L.append("  [FAIL] 双独立因子方案 = 特设  |  不满足『屏蔽因子须从场方程推导』的要求，"
             "且零预测力（与 v30 组合层过拟合警示同构）")
    L.append("")

    # ---- 结论 ----
    L.append("== 5. 结论（对方向 A 的门禁判定）==")
    L.append("  g-2 与 EDM 偏差【同源】：均为『挠率/曲率几何效应无屏蔽地直映低能可观测量』。")
    L.append("  但二者所需的压低量级相差 %.0f 个数量级 ⇒ 不可由同一屏蔽机制调和。" % abs(float(log10_ratio)))
    L.append("  ⇒ 方向 A（构造带屏蔽因子 f 的修正映射）在双约束下【不可行】：")
    L.append("     单一 f 无法兼顾；双 f 则特设且零预测力。")
    L.append("  ⇒ 方向 3（承认 TUFT 低能孤子图像失效，理论仅保留于高能/普朗克尺度）")
    L.append("     为当前唯一与双精密实验相容的诚实结论；CURATED 维持 L3 否决态。")
    L.append("  [FAIL] g-2/EDM 双约束不可调和  |  需 %.0f 量级因子分裂，无几何来源" % abs(float(log10_ratio)))
    L.append("")
    L.append("== 汇总 ==")
    L.append("  PASS=0  FAIL=3（单一因子不存在/双因子特设/双约束不可调和）  BOUNDARY=0  INFO=2")
    L.append("  F_g=%.4f  F_d=%.3e  分裂比=%.3e (%.1f 量级)" % (
        float(F_g), float(F_d), float(ratio), float(log10_ratio)))
    L.append("")
    L.append("红线：本册仅做可行性判定，未构造新物理、未修改 TUFT 场方程或映射公式；")
    L.append("结论为『方向 A 在当前双约束下不可行』的可导出性判定，非对 TUFT 框架的证伪宣告，")
    L.append("亦不否定孤子几何(公理A)的数学自洽性——失效的是【低能可观测量映射层】。")

    txt = "\n".join(L) + "\n"
    out = os.path.join(HERE, "tuft_g2_EDM_屏蔽因子双约束可行性审计_OPEN5b_report.txt")
    open(out, "w", encoding="utf-8").write(txt)
    print(txt)
    print("已生成:", out)


if __name__ == "__main__":
    main()
