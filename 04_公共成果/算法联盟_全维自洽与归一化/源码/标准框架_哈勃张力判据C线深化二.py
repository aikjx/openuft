# -*- coding: utf-8 -*-
"""二十五期·标准框架攻坚 线C深化二 哈勃张力数值靶（2026-10-14）
H0 测量汇总（A 级公开）→ 张力显著性计算（250 位）→ 新物理窗口与判决实验。
"""
import mpmath as mp
mp.mp.dps = 250
mp.pretty = True

print("===== 线C深化二 哈勃张力数值靶（250 位）=====")

# ① H0 测量汇总（A 级公开值）
print("\n① H0 测量汇总（A 级公开）")
meas = [
    ("Planck CMB（2018-2020）", mp.mpf("67.4"), mp.mpf("0.5")),
    ("SH0ES（Cepheid+SNe，2024）", mp.mpf("73.04"), mp.mpf("1.04")),
    ("TRGB（Anand 2024）", mp.mpf("67.96"), mp.mpf("1.18")),
    ("H0LiCOW（透镜时间延迟）", mp.mpf("73.3"), mp.mpf("5.4")),
    ("GW170817 标准汽笛", mp.mpf("70.0"), mp.mpf("12.0")),
]
for n, v, e in meas:
    print("  %-26s H0 = %.2f ± %.2f km/s/Mpc" % (n, v, e))

print("\n② 张力显著性 Δ/σ_comb（250 位）")
def tension(v1, e1, v2, e2):
    d = abs(v1 - v2)
    sc = mp.sqrt(e1*e1 + e2*e2)
    return d, sc, d/sc
pairs = [
    ("Planck", meas[0][1], meas[0][2], "SH0ES", meas[1][1], meas[1][2]),
    ("Planck", meas[0][1], meas[0][2], "TRGB", meas[2][1], meas[2][2]),
    ("SH0ES", meas[1][1], meas[1][2], "TRGB", meas[2][1], meas[2][2]),
    ("Planck", meas[0][1], meas[0][2], "H0LiCOW", meas[3][1], meas[3][2]),
]
for a1, v1, e1, a2, v2, e2 in pairs:
    d, sc, t = tension(v1, e1, v2, e2)
    print("  %s(%.2f±%.2f) vs %s(%.2f±%.2f)：Δ=%.2f，σ_comb=%.3f，张力=%.2fσ%s"
          % (a1, v1, e1, a2, v2, e2, d, sc, t, "  ← 显著" if t > mp.mpf("4") else ("  ← 无张力" if t < mp.mpf("1") else "")))

print("\n③ 口径与系统学（A 级公开）")
print("  SH0ES（Cepheid 校准 SNe Ia）：73.04±1.04 → 与 Planck 张力 ~4.9σ（>4σ 显著）")
print("  TRGB 校准：67.96±1.18 → 与 Planck 无张力（0.4σ），与 SH0ES 分歧 3.2σ——阶梯内部分歧")
print("  JWST 交叉：Cepheid 测距在 JWST 波段仍给出 72-73（2024-2025）——系统学未完全排除")
print("  结论：距离阶梯与 CMB 间 ~5σ 张力真实存在（A 级）；阶梯内 Cepheid/TRGB 分歧 ~3σ")

print("\n④ 新物理窗口与统一场论交叉")
print("  EDE（早期暗能量）：f_EDE~5-10% 可在不损 CMB 前提下抬升 H0 至 70+（B 级模型）")
print("  暗辐射 ΔNeff：~0.3-0.5 缓解；与线C w(z) 交叉：DESI 3.1σ 未达 5σ——ΛCDM 未被排除，但张力暗示缺失物理")
print("  判决实验：H0 独立测量达 ~1% 精度（CMB-S4/交叉校准/新标准汽笛）→ 判定张力真伪")

print("\n-- 结论 --")
print("哈勃张力数值靶落地：Planck vs SH0ES = 4.9σ（显著，A 级）；Planck vs TRGB = 0.4σ（无张力）——")
print("张力是真实的（Cepheid 阶梯与 CMB 冲突），但阶梯内部分歧 3.2σ 提示系统学未排除；")
print("统一场论（含 TUFT）不解决 H0 张力——诚实红线不变：宇宙学缺失物理 ≠ 统一完成。")
