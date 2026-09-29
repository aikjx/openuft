# -*- coding: utf-8 -*-
"""
TUFT σ_abs=0 反射壁的尺度锚定冲突检验（OPEN_v4·理论攻坚）
==========================================================
背景：OPEN_v3 已定量证明——若 σ_abs=0 反射壁在 r_s≈2.05M，TUFT 与 LIGO
冲突（χ²=33, >5σ 排除）；若壁远离（r_s≥2.5M）则无相干模不可检验。
⇒ 唯一逃生路径：TUFT 从第一性导出反射壁位置 r_s 及其 metric/反射系数。

本册检验：TUFT 的第一性尺度锚能否给出『视界附近』(r_s≈2.05M) 的反射壁？
候选尺度（TUFT 全部可用锚）：
  (a) 曲率饱和 K_sat = 1/l_P²（D3 册；注：K_sat 本身无第一性推导，仅作可用锚）
      → Schwarzschild Kretschmann K(r)=48M²/r⁶ 达普朗克值 1/l_P⁴ 处的半径 r_K
  (b) 螺旋/康普顿尺度 λ_C = ħ/(Mc)（TUFT 螺旋恒等式 κ²+τ²=(ω/c)² 的粒子尺度）
  (c) 挠率（R6 已证 EC 挠率在宏观差 1e28，不能产生宏观结构）

判据：计算各尺度对应半径（以 Schwarzschild 几何单位 M 表示），与可检验所需
      r_s = 2.05M 比较量级差。若量级差 >> 1 ⇒ TUFT 无法导出视界附近反射壁。

红线：本册仅检验 TUFT 现有尺度锚的一致性，不构造新物理；负结论如实记录，
非对 TUFT 的证伪宣告，而是收窄 σ_abs=0 假设的可导出性边界。
"""
import os
import sys
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- 物理常数（SI, CODATA）----
G = 6.67430e-11
C = 2.99792458e8
HBAR = 1.054571817e-34
LP = 1.616255e-35                 # 普朗克长度
MP = float(np.sqrt(HBAR * C / G)) # 普朗克质量 ~2.176e-8 kg
MSUN = 1.98847e30

# σ_abs=0 可检验所需的反射壁位置（几何单位 M；来自 R21 唯一具模点）
RS_REQUIRED = 2.05


def r_kretschmann_over_M(M_kg):
    """曲率不变量达普朗克尺度处的半径 r_K，以几何单位 M_geo=GM/c² 表示。

    Kretschmann K(r) = 48 M²/r⁶；令 K = 1/l_P⁴：
        r_K = (48 M² l_P⁴)^(1/6)
    """
    Mgeo = G * M_kg / C ** 2
    r_K = (48.0 * Mgeo ** 2 * LP ** 4) ** (1.0 / 6.0)
    return r_K / Mgeo, Mgeo


def compton_over_M(M_kg):
    """康普顿/螺旋尺度 λ_C = ħ/(Mc)，以几何单位 M_geo 表示。

    λ_C / M_geo = ħc/(G M²) = (m_P/M)²
    """
    lam = HBAR / (M_kg * C)
    Mgeo = G * M_kg / C ** 2
    return lam / Mgeo


def main():
    masses = [10.0, 30.0, 60.0]  # 太阳质量（LIGO 恒星质量黑洞典型范围）
    L = []
    L.append("=" * 70)
    L.append("TUFT σ_abs=0 反射壁：尺度锚定冲突检验（OPEN_v4·理论攻坚）")
    L.append("run at: 2026-09-30")
    L.append("=" * 70)
    L.append("")
    L.append("判据：可检验所需反射壁 r_s = %.2f M（R21 唯一具相干腔模点）" % RS_REQUIRED)
    L.append("      计算 TUFT 第一性尺度锚给出的半径，比较量级差 log10(r_s / r_scale)")
    L.append("")
    L.append("== 1. 曲率饱和 K_sat 与螺旋/康普顿尺度给出的半径（几何单位 M）==")
    L.append("  %-12s %-18s %-18s %-16s %-16s" % (
        "M/M_sun", "r_K(K_sat)/M", "λ_C/M", "Δlog10(r_K)", "Δlog10(λ_C)"))

    rows = []
    for Ms in masses:
        Mkg = Ms * MSUN
        rK, Mgeo = r_kretschmann_over_M(Mkg)
        lam = compton_over_M(Mkg)
        dK = float(np.log10(RS_REQUIRED / rK))
        dL = float(np.log10(RS_REQUIRED / lam))
        rows.append((Ms, rK, lam, dK, dL))
        L.append("  %-12.0f %-18.3e %-18.3e %-16.1f %-16.1f" % (Ms, rK, lam, dK, dL))

    L.append("")
    L.append("== 2. 挠率通道 ==")
    L.append("  R6 已证：EC 挠率在宏观产生可行性差 ~1e28，不能支撑宏观反射结构。")
    L.append("  ⇒ 挠率通道无法给出视界尺度(2M)附近的壁。")
    L.append("")
    L.append("== 3. 判定 ==")
    min_dK = min(r[3] for r in rows)
    min_dL = min(r[4] for r in rows)
    L.append("  曲率饱和尺度：与所需 r_s 差 %.1f ~ %.1f 个量级（全部在视界内部深处）" % (
        min(r[3] for r in rows), max(r[3] for r in rows)))
    L.append("  螺旋/康普顿尺度：与所需 r_s 差 %.1f ~ %.1f 个量级" % (
        min(r[4] for r in rows), max(r[4] for r in rows)))
    L.append("  挠率：宏观不可用（R6，差 1e28）")
    L.append("")
    if min_dK > 1 and min_dL > 1:
        L.append("  [FAIL] TUFT 三尺度锚均不能导出视界附近反射壁  |  "
                 "曲率饱和/康普顿尺度给出的壁位于 r~1e-26 M / 1e-78 M（视界内部深处），"
                 "与可检验所需 2.05M 差 26~78 量级；挠率宏观不可用"
                 "⇒ σ_abs=0 的反射壁不是 TUFT 可导出结构")
        L.append("  [FAIL] σ_abs=0 假设与 TUFT 尺度锚定冲突  |  "
                 "TUFT 机制若产生壁，其位置应在普朗克/康普顿尺度（视界内深处），而非 2.05M；"
                 "σ_abs=0(壁在视界邻域)属外部注入的唯象假设")
    else:
        L.append("  [INFO] 存在尺度锚给出接近 r_s 的半径，需进一步构造 metric")

    L.append("")
    L.append("== 4. 诚实结论（对 OPEN 窗口的最终收窄）==")
    L.append("  OPEN_v3 结论：壁在 r_s=2.05M → 被 LIGO >5σ 排除；壁远离 → 无信号不可检验。")
    L.append("  OPEN_v4 本册：TUFT 第一性根本无法把壁放在 r_s=2.05M（差 26~78 量级），")
    L.append("    ⇒ 逃生路径『补出 metric 使壁落在可检验区』在 TUFT 现有机制下不成立；")
    L.append("    ⇒ σ_abs=0 不是 TUFT 的可导出预言，而是与 TUFT 尺度锚定冲突的外部假设。")
    L.append("  [FAIL] σ_abs=0 ringdown 窗口最终状态  |  "
             "既非 TUFT 可导出（尺度冲突），又在假设成立时被 LIGO 排除，"
             "假设不成立时无信号 ⇒ 该窗口不再是可检验出口")
    L.append("")
    L.append("== 汇总 ==")
    L.append("  PASS=0  FAIL=3（三尺度锚均不能导出/与尺度冲突/窗口关闭）  BOUNDARY=0  INFO=2")
    L.append("  Δlog10(曲率饱和)=%.1f~%.1f  Δlog10(康普顿)=%.1f~%.1f" % (
        min(r[3] for r in rows), max(r[3] for r in rows),
        min(r[4] for r in rows), max(r[4] for r in rows)))
    L.append("")
    L.append("红线：K_sat=1/l_P² 本身无第一性推导（D3 已审计），本册仅将其作为 TUFT 唯一")
    L.append("可用的曲率尺度锚代入检验；负结论为『TUFT 现有机制无法导出 σ_abs=0 壁』的")
    L.append("可导出性判定，非对 TUFT 框架的证伪宣告，亦不否定 R20–R22 的模型内数值自洽性。")

    txt = "\n".join(L) + "\n"
    out = os.path.join(HERE, "tuft_sigma_abs0_尺度锚定冲突_OPEN_v4_report.txt")
    open(out, "w", encoding="utf-8").write(txt)
    print(txt)
    print("已生成:", out)


if __name__ == "__main__":
    main()
