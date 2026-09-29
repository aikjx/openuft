# -*- coding: utf-8 -*-
"""
TUFT 孤子 τ/κ 锁定的微分方程层面证明（OPEN5c，方向 C）
========================================================
问题：孤子自洽条件为何「强制固定 τ/κ」？是公理 A 锁死的吗？
      若 τ/κ 有自由度，能否靠调它同时满足 g-2 与 EDM 双约束？

推导链：
  公理 A :  κ² + τ² = Ω²   (Ω = ω/c = m_e c/ħ = 1/ƛ_C，康普顿尺度)
  稳态   :  κ ∇_μ κ + τ ∇_μ τ = 0
  映射   :  g-2 = 2τ/κ ； EDM ∝ κτ

本册三步：
  §1 证明 稳态条件 ⇔ 公理A 的微分形式（二者等价，非独立假设）
  §2 圆参数化 κ=Ωcosθ, τ=Ωsinθ ⇒ τ/κ=tanθ 连续自由
     ⇒ 公理A【不】锁定 τ/κ（留 1 个自由度）；具体值来自额外孤子解
  §3 检验该自由度能否调和双约束（关键）：
     g-2 = 2tanθ ； EDM ∝ κτ = (Ω²/2)sin2θ ≈ Ω²·tanθ (小角)
     ⇒ 调 θ 匹配 g-2 时，EDM 按【同一比例】缩放 ⇒ 只改 O(1) 因子
     ⇒ 而 EDM 需压低 16 个量级（其超额来自 Ω² 康普顿尺度，非角度）
     ⇒ θ 自由度救不了 EDM ⇒ 方向2（改孤子/调参）同样不可行

红线：仅做符号推导与可行性判定，不构造新物理。
"""
import os
import sys
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# 基线（与 OPEN5b 一致）
G2_EXP = 0.00231930436
G2_TUFT = 0.00404              # ⇒ τ/κ = 0.00202
EDM_TUFT_ECM = 1.4087e-13      # e·cm（θ0 处）
EDM_ACME_ECM = 1.1e-29         # e·cm
HBAR, C, ME = 1.054571817e-34, 2.99792458e8, 9.1093837015e-31


def main():
    L = []
    L.append("=" * 72)
    L.append("TUFT 孤子 τ/κ 锁定的微分方程层面证明（OPEN5c·方向 C）")
    L.append("run at: 2026-09-30")
    L.append("=" * 72)

    s = sp.symbols("s")                       # 世界线参数
    kappa = sp.Function("kappa")(s)
    tau = sp.Function("tau")(s)
    Omega = sp.symbols("Omega", positive=True)
    theta = sp.symbols("theta")

    # ---- §1 稳态条件 ⇔ 公理A 微分 ----
    L.append("")
    L.append("== 1. 稳态条件与公理 A 的等价性 ==")
    L.append("  公理 A : κ² + τ² = Ω²")
    L.append("  稳态   : κ∇_μκ + τ∇_μτ = 0")
    deriv = sp.diff(kappa**2 + tau**2 - Omega**2, s)      # d/ds(κ²+τ²−Ω²)
    steady = kappa * sp.diff(kappa, s) + tau * sp.diff(tau, s)
    diff_check = sp.simplify(sp.expand(deriv) - 2 * steady)
    L.append("  d/ds(κ²+τ²−Ω²) = %s" % sp.expand(deriv))
    L.append("  2×(稳态式)      = %s" % sp.expand(2 * steady))
    L.append("  差值            = %s  ⇒ 二者等价（仅差常数因子 2）" % diff_check)
    if diff_check == 0:
        L.append("  [PASS] 稳态条件是公理 A 的微分推论  |  Ω 为常数时自动成立，"
                 "不是独立假设，也不额外约束 τ/κ")
    L.append("")

    # ---- §2 圆参数化与自由度 ----
    L.append("== 2. 圆参数化：公理 A 是否锁定 τ/κ？==")
    k_par = Omega * sp.cos(theta)
    t_par = Omega * sp.sin(theta)
    axiom_res = sp.simplify(k_par**2 + t_par**2 - Omega**2)
    ratio = sp.simplify(t_par / k_par)
    L.append("  参数化 κ=Ωcosθ, τ=Ωsinθ")
    L.append("  代入公理A: κ²+τ²−Ω² = %s  ⇒ 恒等成立（任意 θ）" % axiom_res)
    L.append("  τ/κ = %s  ⇒ θ 连续 ⇒ τ/κ ∈ (0,∞) 连续" % ratio)
    L.append("  自由度审计: 变量(κ,τ) 2 个 − 约束(公理A) 1 个 = 1 个自由度(θ)")
    L.append("  [INFO] 公理 A 不锁定 τ/κ  |  它只把 (κ,τ) 限制在半径 Ω 的圆上，"
             "角度 θ 自由；τ/κ=0.00202 是【额外孤子解】选定的，非公理 A 必然")
    L.append("")

    # ---- §3 该自由度能否调和双约束 ----
    L.append("== 3. 检验：θ 自由度能否同时满足 g-2 与 EDM？==")
    # 当前孤子解 θ0
    tan0 = sp.Float(G2_TUFT) / 2                     # τ/κ = 0.00202
    th0 = sp.atan(tan0)
    # 匹配 g-2 所需 θ
    tan_g2 = sp.Float(G2_EXP) / 2                    # 0.00115965
    th_g2 = sp.atan(tan_g2)
    L.append("  当前孤子: τ/κ = 2τ/κ ÷ 2 = %.6f  ⇒ θ0 = %.6f rad" % (float(tan0), float(th0)))
    L.append("  匹配 g-2: 需 2tanθ = %.10f ⇒ tanθ = %.8f ⇒ θ = %.8f rad" % (
        G2_EXP, float(tan_g2), float(th_g2)))
    L.append("")
    L.append("  EDM ∝ κτ = Ω² sinθcosθ = (Ω²/2)sin2θ")
    # κτ 的比值（θ_g2 vs θ0）
    prod0 = sp.sin(th0) * sp.cos(th0)
    prod_g2 = sp.sin(th_g2) * sp.cos(th_g2)
    scale = sp.simplify(prod_g2 / prod0)
    L.append("  调 θ 至匹配 g-2 时，EDM 缩放因子 = sinθcosθ|_g2 / sinθcosθ|_0 = %.6f" % float(scale))
    L.append("  （小角下 sinθcosθ≈tanθ ⇒ 缩放因子 ≈ tanθ_g2/tanθ0 = g-2_exp/g-2_TUFT = %.6f）"
             % (G2_EXP / G2_TUFT))
    edm_after = sp.Float(EDM_TUFT_ECM) * scale
    over_after = sp.log(edm_after / sp.Float(EDM_ACME_ECM), 10).evalf()
    L.append("  → 调 θ 匹配 g-2 后：EDM = %.4e e·cm，仍超 ACME %.1f 个量级 ❌" % (
        float(edm_after), float(over_after)))
    L.append("")
    # 反向：若强行压低 EDM
    need_scale = sp.Float(EDM_ACME_ECM) / sp.Float(EDM_TUFT_ECM)
    L.append("  反向检验：要把 EDM 压到 ACME 以内需 κτ 缩放 ≤ %.3e" % float(need_scale))
    L.append("  即 sin2θ 需缩小 %.0f 量级 ⇒ θ→0 或 θ→π/2" % abs(float(sp.log(need_scale, 10).evalf())))
    L.append("  但 θ→0 ⇒ g-2=2tanθ→0；θ→π/2 ⇒ g-2→∞ ⇒ 均严重偏离实验 0.0023193 ❌")
    L.append("")
    L.append("  [FAIL] θ(即 τ/κ)自由度无法调和双约束  |  "
             "EDM 的 16 量级超额来自 Ω²=1/ƛ_C²（康普顿尺度 ~%.2e m^-2）本身，"
             "角度 θ 只能提供 O(1) 系数(sin2θ≤1)；调 θ 匹配 g-2 时 EDM 仅按同比例(%.3f)缩放"
             % (float((ME * C / HBAR) ** 2), float(scale)))
    L.append("")

    # ---- 结论 ----
    L.append("== 4. 结论（对三个修复方向的最终裁定）==")
    L.append("  (1) 稳态条件是公理 A 的微分推论，非独立约束；公理 A 留给 τ/κ 一个连续自由度 θ。")
    L.append("      ⇒ 严格说『τ/κ 被孤子自洽锁死』应修正为：『τ/κ 由额外孤子解选定』，")
    L.append("         公理 A 本身不锁死（这为『调参』留了名义空间）。")
    L.append("  (2) 但该自由度【无用】：EDM 的超额量级由 Ω²（康普顿尺度）决定，")
    L.append("     θ 只能给 O(1) 因子；调 θ 匹配 g-2 ⇒ EDM 仍超 %.1f 量级；" % float(over_after))
    L.append("     压 EDM 至达标 ⇒ g-2 归零/发散。与 OPEN5b 的结论一致（16 量级分裂）。")
    L.append("  ⇒ 方向2（改孤子稳态条件/调 τ/κ）同样【不可行】；")
    L.append("  ⇒ 方向1（单一屏蔽因子）已被 OPEN5b 否；方向2 本册否；")
    L.append("  ⇒ 方向3（承认低能孤子图像失效，理论仅适用于高能/普朗克尺度）为唯一诚实结论。")
    L.append("  [FAIL] 三方向仅剩方向3  |  低能映射层失效，非孤子几何(公理A)之过")
    L.append("")
    L.append("== 汇总 ==")
    L.append("  PASS=1（稳态⇔公理A微分）  FAIL=2（θ自由度无效/方向2不可行）  BOUNDARY=1（τ/κ非锁死）  INFO=2")
    L.append("  θ0=%.6f  θ_g2=%.8f  EDM缩放=%.4f  残留超额=%.1f 量级" % (
        float(th0), float(th_g2), float(scale), float(over_after)))
    L.append("")
    L.append("红线：本册仅做符号推导与判定；未构造新物理、未修改 TUFT 方程。")
    L.append("『τ/κ 非公理A锁死』是对流行表述的精确化，非为调参开后门——")
    L.append("本册已证即便利用该自由度仍无法调和双约束。")

    txt = "\n".join(L) + "\n"
    out = os.path.join(HERE, "tuft_孤子τκ锁定_微分方程证明_OPEN5c_report.txt")
    open(out, "w", encoding="utf-8").write(txt)
    print(txt)
    print("已生成:", out)


if __name__ == "__main__":
    main()
