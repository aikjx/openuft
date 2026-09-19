# -*- coding: utf-8 -*-
"""
================================================================================
TUFT-R7  拓扑统一场论「证明链」关键关系精算与符号审查
================================================================================
对象：《TUFT拓扑统一场论》第四部分（固有时 / β₁ / 引力红移）+ 第五部分（统计涌现）。
约定（用户给定）：
    s 世界线弧长，ds = c dt；dτ = ds/c；d/ds = (1/c) d/dt
    β₁ = (κ²+τ²)/⟨κ₀²+τ₀²⟩；□ = ∇² − (1/c²)∂_t²
    m = (ℏ/c)√(κ²+τ²)；ω = c√(κ²+τ²)；β₁ 静态解 = exp(2GM/(c²r))

本文件做三件事（红线：如实标 FAIL，不粉饰）：
  (1) 量纲审查：β₁ / m / ω / g / □ 是否自洽；
  (2) 弱场审查：由 β₁ 静态解反推 g，核对是否给出牛顿引力（吸引）；
  (3) 符号审查（关键）：把 ω=ω₀√β₁ 作为「局域时钟速率」时，与 GR 及
      Pound–Rebka / GPS / 光钟观测的**符号**对比。

结论预告：量纲全部自洽、弱场吸引正确；但**红移符号与 GR/观测相反**
（TUFT 给 +GM/(c²r)，GR/观测给 −GM/(c²r)），这是必须澄清的关键点。
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
REPORT = os.path.join(HERE, "tuft_r7_report.txt")

C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054571817e-34
MSUN = 1.98892e30
MEARTH = 5.9722e24
REARTH = 6.371e6

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
    sec("TUFT-R7 拓扑UFT 证明链 · 量纲与符号审查")
    put("  约定：ds=c dt, dτ=ds/c, β₁=(κ²+τ²)/⟨κ₀²+τ₀²⟩, m=(ℏ/c)√(κ²+τ²), ω=c√(κ²+τ²)")

    # ---------- 1. 量纲审查 ----------
    sec("1. 量纲审查（符号推演）")
    put("  设 [κ]=[τ]=L⁻¹  ⟹ [κ²+τ²]=L⁻²")
    put("  β₁ = (κ²+τ²)/⟨κ₀²+τ₀²⟩  ⟹ [β₁]=L⁻²/L⁻²=1（无量纲）✓")
    rec("1a: β₁ 无量纲", True, "分子/分母同为 L⁻² ⟹ 无量纲 ✓")
    put("  m = (ℏ/c)√(κ²+τ²)：[ℏ/c]= (J·s)/(m/s)= kg·m ；×L⁻¹ ⟹ kg ✓")
    rec("1b: m 量纲 = 质量", True, "[ℏ/c]·L⁻¹ = (kg·m)·m⁻¹ = kg ✓")
    put("  ω = c√(κ²+τ²)：[(m/s)·L⁻¹] = s⁻¹ ✓")
    rec("1c: ω 量纲 = 频率", True, "(m/s)·m⁻¹ = s⁻¹ ✓")
    put("  g = (c²/2)∇lnβ₁：[c²]=L²/T²，[∇]=L⁻¹ ⟹ L/T²（加速度）✓")
    rec("1d: g 量纲 = 加速度", True, "(L²/T²)·L⁻¹ = L/T² ✓")
    put("  □ = ∇² − (1/c²)∂_t²：两项同为 L⁻² ✓")
    rec("1e: □ 量纲自洽", True, "∇²=L⁻²；(1/c²)∂_t² = (T²/L²)·T⁻² = L⁻² ✓")
    put("")
    put("  注（如实标注）：dτ = ds/c 且 ds = c·dt ⟹ **dτ = dt**。")
    put("     即本模型的『固有时』恒等于坐标时，**模型内不含狭义相对论的时间膨胀**（γ 因子缺失）。")
    info("1f", "dτ=dt ⟹ 无 SR 时间膨胀；模型的时钟快慢改由 ω(β₁) 承担")

    # ---------- 2. 弱场：β₁ 静态解 → g ----------
    sec("2. 弱场审查：β₁ 静态解 → 引力加速度")
    put("  静态球对称解：β₁ = exp(2GM/(c²r))； ln β₁ = 2GM/(c²r)")
    put("  g = (c²/2)·d(lnβ₁)/dr · r̂ = (c²/2)·(−2GM/(c²r²)) r̂ = −(GM/r²) r̂")

    def g_num(M, r):
        return -(C ** 2 / 2.0) * (2 * G * M / (C ** 2 * r ** 2))

    g_earth = g_num(MEARTH, REARTH)
    g_newton = -G * MEARTH / REARTH ** 2
    rec("2a: g(β₁) 与牛顿 g=−GM/r² 一致",
        abs(g_earth - g_newton) / abs(g_newton) < 1e-12,
        "g=%.6f m/s²；牛顿=%.6f m/s²（负号=指向地心，吸引 ✓）" % (g_earth, g_newton))
    info("2b", "β₁=exp(+2GM/(c²r)) 给出吸引；若取负号则 g 变排斥 ⟹ 该符号由牛顿极限唯一固定")

    # ---------- 3. 关键：红移符号审查 ----------
    sec("3. 符号审查（关键）：ω=ω₀√β₁ 作为局域时钟速率 vs GR/观测")
    put("  TUFT：ω(r)/ω_∞ = √β₁(r) = exp(GM/(c²r)) ≈ 1 + GM/(c²r)")
    put("  GR  ：局域钟速率 / 无穷远钟速率 = √(1 − 2GM/(c²r)) ≈ 1 − GM/(c²r)")
    put("  ⟹ 一阶**量值相同、符号相反**。")
    put("")
    cases = [
        ("地球表面", MEARTH, REARTH),
        ("太阳表面", MSUN, 6.957e8),
    ]
    for name, M, r in cases:
        x = 2.0 * G * M / (C ** 2 * r)
        tuft = math.sqrt(math.exp(x))      # √β₁
        gr = math.sqrt(1.0 - x)            # GR 钟速率
        put("  【%s】 2GM/(c²r)=%.4e" % (name, x))
        put("     TUFT ω/ω_∞ = √β₁      = 1 %+.4e" % (tuft - 1.0))
        put("     GR   钟速率比         = 1 %+.4e" % (gr - 1.0))
        put("     两者之差              = %.4e（符号相反）" % ((tuft - 1.0) - (gr - 1.0)))
    rec("3a: TUFT 与 GR 红移一阶符号一致?",
        False,
        "TUFT 为 +GM/(c²r)（深势处钟**更快**）；GR/观测为 −GM/(c²r)（更慢）。符号相反 ⇒ 冲突")
    put("")
    put("  实验判决：Pound–Rebka、GPS、光学原子钟均确认『深势处钟更慢』（即 GR 符号）。")
    put("  ⟹ 若把 ω 直接解释为**局域时钟速率**，TUFT 该式已被现有实验排除。")
    put("")
    put("  可能的澄清路径（三选一，须在模型中显式声明）：")
    put("    (i)  ω 不是钟速率，而是『单位坐标时间内的本征振荡数』，观测频率需另乘传播因子 1/β₁")
    put("         ⟹ ω_obs = ω₀/√β₁ ≈ 1 − GM/(c²r) 与 GR 一致；")
    put("    (ii) β₁ 与本征频率的关系应为 ω = ω₀/√β₁（即 ω∝β₁^(−1/2)）；")
    put("    (iii) 承认差异并给出可检验区分（但当前实验已倾向 GR）。")
    info("3b", "推荐 (i)/(ii)：使钟速率 ∝ β₁^(−1/2)，方与弱场 GR 及 Pound–Rebka/GPS 相容")

    # ---------- 4. 统计涌现的形式一致性 ----------
    sec("4. 第五部分：统计涌现的形式一致性（微观→宏观）")
    put("  定义：⟨κ²+τ²⟩_macro = (1/N)Σ_i (κ_i²+τ_i²)（系综平均）")
    put("  则 β₁_macro = ⟨κ²+τ²⟩_macro / ⟨κ₀²+τ₀²⟩")
    put("  ⟹ m_macro 与 ω_macro 由同一 β₁_macro 决定：m=m₀√β₁, ω=ω₀√β₁（形式不变）✓")
    rec("4a: 宏观 β₁ 与微观同形式", True,
        "β₁ 为比值 ⟹ 取系综平均后形式不变，m/ω 关系可平移到宏观 ✓（形式层面）")
    bnd = ("粗粒化是否保持 β₁ 的场方程（即 ⟨□β₁⟩ = □⟨β₁⟩ 是否成立）——"
           "非线性场方程下一般**不成立**，需重整化/闭合假设；属开放命题")
    info("4b", "⚠ " + bnd)

    # ---------- 汇总 ----------
    sec("5. 判定汇总")
    put("  [量纲层]  PASS —— β₁ 无量纲、m 为质量、ω 为频率、g 为加速度、□ 自洽。")
    put("  [弱场层]  PASS —— β₁=exp(2GM/(c²r)) 给出吸引的牛顿 g（符号由牛顿极限唯一固定）。")
    put("  [符号层]  FAIL（关键）—— ω=ω₀√β₁ 作钟速率时与 GR/观测红移符号相反；需按 (i)/(ii) 澄清。")
    put("  [涌现层]  BOUNDARY —— 形式平移 PASS；非线性粗粒化闭合属开放命题。")
    put("")
    put("红线：本文件只做量纲/数值/符号核对，不主张 TUFT 成立或证伪；")
    put("      符号冲突是可复算的事实，澄清路径由模型给出后重做本审查。")

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
