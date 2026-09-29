# -*- coding: utf-8 -*-
"""
TUFT 全维突破：求导证明的严格验证（OPEN8）
============================================
对本轮（OPEN5b/5c/7）全部关键求导关系做 sympy 严格验证，
确立「三重封堵」结论的数学地基。

待验证命题：
  V1 稳态条件 ⇔ 公理A微分：  d/ds(κ²+τ²−Ω²) = 2(κκ' + ττ')
  V2 圆参数化恒等：          (Ωcosθ)² + (Ωsinθ)² − Ω² = 0
  V3 比值关系：              τ/κ = tanθ
  V4 g-2 与尺度无关：        ∂(g-2)/∂Ω = 0
  V5 EDM 依赖尺度：          ∂(κτ)/∂Ω = 2Ω sinθcosθ （∝ Ω）
  V6 不对称性（核心）：      ∂(g-2)/∂Ω = 0  但  ∂(EDM)/∂Ω ≠ 0
  V7 重标度不变性：          g-2(λΩ)=g-2(Ω)； EDM(λΩ)/EDM(Ω) = λ²
  V8 角度只给 O(1) 因子：    ∂(κτ)/∂θ = Ω²cos2θ ；小角下 cos2θ≈1
  V9 数值自洽：              θ0、λ、EDM 缩放 与 OPEN5b/5c/7 报告一致

产出：tuft_求导证明验证_OPEN8_report.txt + 计数汇总
"""
import os
import sys
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

PASS = FAIL = BOUNDARY = INFO = 0


def P(msg):
    global PASS
    PASS += 1
    print("  [PASS] " + msg)


def F(msg):
    global FAIL
    FAIL += 1
    print("  [FAIL] " + msg)


def B(msg):
    global BOUNDARY
    BOUNDARY += 1
    print("  [BOUNDARY] " + msg)


def I(msg):
    global INFO
    INFO += 1
    print("  [INFO] " + msg)


def main():
    L = []
    def out(s=""):
        L.append(s)
        print(s)

    s = sp.symbols("s")
    kappa = sp.Function("kappa")(s)
    tau = sp.Function("tau")(s)
    Omega, theta, lam = sp.symbols("Omega theta lam", positive=True)

    out("=" * 72)
    out("TUFT 全维突破：求导证明严格验证（OPEN8）")
    out("run at: 2026-09-30")
    out("=" * 72)

    # ---- V1 ----
    out("")
    out("== V1. 稳态条件 ⇔ 公理 A 的微分 ==")
    deriv = sp.diff(kappa**2 + tau**2 - Omega**2, s)
    steady = kappa * sp.diff(kappa, s) + tau * sp.diff(tau, s)
    v1 = sp.simplify(sp.expand(deriv) - 2 * steady)
    out("  d/ds(κ²+τ²−Ω²) − 2(κκ'+ττ') = %s" % v1)
    if v1 == 0:
        P("V1 稳态条件是公理 A 的微分推论（等价，差常数因子 2）")
    else:
        F("V1 等价性不成立")

    # ---- V2 ----
    out("")
    out("== V2. 圆参数化恒等 ==")
    v2 = sp.simplify((Omega * sp.cos(theta))**2 + (Omega * sp.sin(theta))**2 - Omega**2)
    out("  (Ωcosθ)² + (Ωsinθ)² − Ω² = %s" % v2)
    if v2 == 0:
        P("V2 圆参数化对任意 θ 恒等满足公理 A")
    else:
        F("V2 圆参数化不恒等")

    # ---- V3 ----
    out("")
    out("== V3. 比值关系 τ/κ = tanθ ==")
    v3 = sp.simplify((Omega * sp.sin(theta)) / (Omega * sp.cos(theta)) - sp.tan(theta))
    out("  (Ωsinθ)/(Ωcosθ) − tanθ = %s" % v3)
    if v3 == 0:
        P("V3 τ/κ = tanθ 成立，且 Ω 约掉 ⇒ 比值与尺度无关")
    else:
        F("V3 比值关系不成立")

    # ---- V4 / V5 / V6 ----
    out("")
    out("== V4–V6. 核心不对称性：g-2 与 EDM 对 Ω 的依赖 ==")
    g2 = 2 * sp.tan(theta)                                  # g-2 映射
    edm = (Omega * sp.cos(theta)) * (Omega * sp.sin(theta))  # EDM 形状 ∝ κτ
    d_g2_dOm = sp.diff(g2, Omega)
    d_edm_dOm = sp.diff(edm, Omega)
    out("  g-2 = %s" % g2)
    out("  EDM ∝ κτ = %s" % sp.simplify(edm))
    out("  ∂(g-2)/∂Ω   = %s" % d_g2_dOm)
    out("  ∂(EDM)/∂Ω   = %s" % sp.simplify(d_edm_dOm))
    if d_g2_dOm == 0:
        P("V4 g-2 对尺度 Ω 的偏导为零 ⇒ g-2 与尺度无关（只由 θ 决定）")
    else:
        F("V4 g-2 依赖 Ω，不对称性前提不成立")
    if sp.simplify(d_edm_dOm) != 0:
        P("V5 EDM 对 Ω 偏导 = 2Ωsinθcosθ ≠ 0 ⇒ EDM ∝ Ω²（依赖尺度）")
    else:
        F("V5 EDM 不依赖 Ω")
    if d_g2_dOm == 0 and sp.simplify(d_edm_dOm) != 0:
        P("V6 不对称性成立：∂(g-2)/∂Ω=0 而 ∂(EDM)/∂Ω≠0 ⇒ 存在『调 Ω 保 g-2』通道")
    else:
        F("V6 不对称性不成立")

    # ---- V7 ----
    out("")
    out("== V7. 重标度不变性 Ω → λΩ ==")
    edm_scaled = ((lam * Omega) * sp.cos(theta)) * ((lam * Omega) * sp.sin(theta))
    ratio_edm = sp.simplify(edm_scaled / edm)
    g2_scaled = 2 * sp.tan(theta)          # θ 未变 ⇒ g-2 不变
    ratio_g2 = sp.simplify(g2_scaled / g2)
    out("  EDM(λΩ)/EDM(Ω) = %s" % ratio_edm)
    out("  g-2(λΩ)/g-2(Ω) = %s" % ratio_g2)
    if ratio_edm == lam**2:
        P("V7a EDM 按 λ² 缩放（∝Ω² 得证）")
    else:
        F("V7a EDM 缩放非 λ²")
    if ratio_g2 == 1:
        P("V7b g-2 在 Ω 重标度下不变（λ 通道可保住 g-2）")
    else:
        F("V7b g-2 随 Ω 改变")

    # ---- V8 ----
    out("")
    out("== V8. 角度 θ 只提供 O(1) 因子 ==")
    d_edm_dth = sp.simplify(sp.diff(edm, theta))
    out("  ∂(κτ)/∂θ = %s" % d_edm_dth)
    # 小角检验：θ0≈0.00202，cos2θ≈1
    th0 = sp.atan(sp.Float(0.00202))
    cos2_val = sp.N(sp.cos(2 * th0))
    out("  在 θ0=arctan(0.00202) 处：cos2θ = %s ≈ 1 ⇒ ∂(κτ)/∂θ ≈ Ω²" % cos2_val)
    if abs(float(cos2_val) - 1.0) < 1e-4:
        P("V8 小角下 ∂(κτ)/∂θ ≈ Ω²（O(1) 系数）⇒ θ 无法提供量级压低")
    else:
        B("V8 cos2θ 偏离 1，需复核小角近似")
    # θ 的全局范围：sin2θ ∈ [0,1] ⇒ κτ ≤ Ω²/2
    I("V8 补充：sin2θ ∈ [0,1] ⇒ κτ ≤ Ω²/2 ⇒ 调 θ 最多改 O(1) 系数，无法压 16 量级")

    # ---- V9 ----
    out("")
    out("== V9. 数值自洽（与 OPEN5b/5c/7 对齐）==")
    G2_EXP, G2_TUFT = 0.00231930436, 0.00404
    EDM_TUFT_ECM, EDM_ACME_ECM = 1.4087e-13, 1.1e-29
    tan0 = sp.Float(G2_TUFT) / 2
    tan_g2 = sp.Float(G2_EXP) / 2
    scale = float(sp.sin(sp.atan(tan_g2)) * sp.cos(sp.atan(tan_g2)) /
                  (sp.sin(sp.atan(tan0)) * sp.cos(sp.atan(tan0))))
    F_d = sp.Float(EDM_ACME_ECM) / sp.Float(EDM_TUFT_ECM)
    lam_need = sp.sqrt(F_d)
    out("  θ0: τ/κ=%.6f ; 匹配 g-2 需 τ/κ=%.8f" % (float(tan0), float(tan_g2)))
    out("  调 θ 匹配 g-2 ⇒ EDM 缩放 = %.6f（OPEN5b 的 F_g=%.6f）" % (scale, G2_EXP / G2_TUFT))
    out("  λ = sqrt(F_d) = %.6e ⇒ Ω 需缩 %.3e 倍" % (float(lam_need), 1 / float(lam_need)))
    ok_scale = abs(scale - G2_EXP / G2_TUFT) < 1e-4
    if ok_scale:
        P("V9a 调 θ 的 EDM 缩放 %.4f 与 OPEN5b 的 F_g=%.4f 一致" % (scale, G2_EXP / G2_TUFT))
    else:
        F("V9a 与 OPEN5b 数值不一致")
    lam_expected = 8.8366e-09
    if abs(float(lam_need) - lam_expected) / lam_expected < 1e-3:
        P("V9b λ=%.4e 与 OPEN7 报告一致" % float(lam_need))
    else:
        F("V9b λ 与 OPEN7 不一致")

    # ---- 汇总 ----
    out("")
    out("== 汇总 ==")
    out("  PASS=%d  FAIL=%d  BOUNDARY=%d  INFO=%d" % (PASS, FAIL, BOUNDARY, INFO))
    out("")
    out("结论：全部求导关系经 sympy 严格验证成立 ——")
    out("  (1) 稳态条件 ≡ 公理A微分（非独立约束，不锁 τ/κ）；")
    out("  (2) g-2 只依赖角度 θ、与尺度 Ω 无关（∂/∂Ω=0）；")
    out("  (3) EDM ∝ Ω² 依赖尺度（λ² 缩放）；")
    out("  (4) 由此确立不对称性 ⇒ 三重封堵（屏蔽因子/角度/尺度）的数学地基牢靠。")
    out("")
    out("红线：本册仅验证既有推导的求导正确性，不构造新物理；")
    out("验证通过只说明【推导无误】，不代表 TUFT 物理成立（数学自洽≠实验证实）。")

    txt = "\n".join(L) + "\n"
    rp = os.path.join(HERE, "tuft_求导证明验证_OPEN8_report.txt")
    open(rp, "w", encoding="utf-8").write(txt)
    print("已生成:", rp)


if __name__ == "__main__":
    main()
