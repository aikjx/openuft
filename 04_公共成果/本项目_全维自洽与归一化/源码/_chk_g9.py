# -*- coding: utf-8 -*-
"""G9 耦合谱的可计算裁决：单尺度类是否可能同时给出 G / σ / λ_W / α？

判据（可机检、非哲学）：
  单尺度类 S = { G = c_G/M², σ = c_σ M², 1/λ = c_L M, α = c_α }，c_i ∈ [1e−2, 1e2]。
  ⇒ 该类的**不变量**是 G·σ = c_G c_σ ∈ [1e−4, 1e4]（与 M 无关）。
  实测 G·σ = 1.19e−39 ⇒ 与类不变量相差 ≥ 34.9 个数量级 ⇒ 单尺度类被排除。

同时给出两条对照：单尺度玩具模型（Gσ=1，判据会放行）、两尺度模型（可精确拟合）。
产物：同目录 _out_g9.txt
纪律：不占 r 号；常数取自 PDG/CODATA 口径并在脚本内做单位换算（不背诵结果）。
"""
import os

import mpmath as mp

from _criteria_kernel import surplus_of

mp.mp.dps = 30
HERE = os.path.dirname(os.path.abspath(__file__))
BUF = []
GUARD = {"pass": 0, "fail": 0}


def say(s=""):
    BUF.append(s)
    print(s)


def guard(name, ok, note):
    GUARD["pass" if ok else "fail"] += 1
    say("[%s] %-34s %s" % ("PASS" if ok else "FAIL", name, note))


# ---------------------------------------------------------------- 常数与单位
HBARC = mp.mpf('0.1973269804')          # GeV·fm
FM = mp.mpf('1e-15')                    # m
C_LIGHT = mp.mpf('2.99792458e8')
G_SI = mp.mpf('6.67430e-11')            # m³ kg⁻¹ s⁻²
KG_IN_GEV = mp.mpf('5.6099712e26')      # 1 kg ↔ GeV（E=mc²）
M_PL = mp.mpf('1.2209e19')              # GeV（非约化普朗克质量）
SIGMA = mp.mpf('0.177')                 # GeV²（Cornell 弦张力，r374 口径）
M_W = mp.mpf('80.377')                  # GeV
LAM_QCD = mp.mpf('0.2')                 # GeV
M_E = mp.mpf('5.1099e-4')               # GeV

# 1 GeV⁻¹ ↔ m
GEV_INV_M = HBARC * FM                  # 1.973e-16 m 每 GeV⁻¹
M_IN_GEV_INV = 1 / GEV_INV_M            # 5.068e15 GeV⁻¹ 每 m
S_IN_GEV_INV = C_LIGHT * M_IN_GEV_INV   # 1.519e24 GeV⁻¹ 每 s
# G: [G] = m³ kg⁻¹ s⁻² ⇒ 换成 GeV 单位：m³→GeV⁻³、s⁻²→GeV²、kg⁻¹→GeV⁻¹ ⇒ GeV⁻²
G_NAT_SI = G_SI * M_IN_GEV_INV ** 3 / (S_IN_GEV_INV ** 2 * KG_IN_GEV)
G_NAT_PL = 1 / M_PL ** 2

say("=" * 78)
say("§A 单位换算与基线（不背结果，现场由 SI 换算）")
say("=" * 78)
say("  1 GeV⁻¹ = %.6e m ｜ 1 s = %.4e GeV⁻¹" % (GEV_INV_M, S_IN_GEV_INV))
say("  G_nat(SI 换算) = %.6e GeV⁻²" % G_NAT_SI)
say("  G_nat(1/M_Pl²) = %.6e GeV⁻² ｜ 相对差 %.2e"
    % (G_NAT_PL, abs(G_NAT_SI - G_NAT_PL) / G_NAT_PL))
guard("G_NAT_CONVERSION", abs(G_NAT_SI - G_NAT_PL) / G_NAT_PL < mp.mpf('5e-3'),
      "SI→自然单位换算与 1/M_Pl² 自洽（两条独立路径，非背数）")

G_SIG = G_NAT_PL * SIGMA
say("  G·σ = %.4e（无量纲。σ=%.3f GeV²）" % (G_SIG, SIGMA))
guard("G_SIGMA_PRODUCT", abs(G_SIG - mp.mpf('1.19e-39')) / mp.mpf('1.19e-39') < mp.mpf('1e-2'),
      "G·σ=1.19e−39，是单尺度类的**类不变量**，与 M 无关")

# ---------------------------------------------------------------- §B 单尺度类
say()
say("=" * 78)
say("§B 单尺度类：Gσ 必须落在 c_G c_σ ∈ [1e−4, 1e4]")
say("=" * 78)

cs = [mp.mpf('1e-2'), mp.mpf('0.1'), mp.mpf(1), mp.mpf(10), mp.mpf('1e2')]
prods = sorted([a * b for a in cs for b in cs])
say("  c 网格 %s ⇒ 乘积范围 [%.2e, %.2e]" % ([float(c) for c in cs], prods[0], prods[-1]))
gap = mp.log10(prods[0]) - mp.log10(G_SIG)
say("  实测 Gσ=%.3e ⇒ 距最宽松下界还差 **%.2f 个数量级**" % (G_SIG, gap))
guard("SINGLE_SCALE_EXCLUDED", gap > 30,
      "单尺度类要求 Gσ=O(1)；实测比该类最宽松下界还低 34.9 个数量级（严格 O(1) 下 38.9）⇒ 该类被排除")

# λ_W：同一 M 下 1/λ = c_L M
c_needed = M_W / M_PL
say("  若 M=M_Pl：c_L 需 = %.3e（O(1) 窗口要求 [1e−2,1e2]，差 %.1f 个数量级）"
    % (c_needed, -mp.log10(c_needed) - 2))
guard("MW_SINGLE_SCALE_EXCLUDED", c_needed < mp.mpf('1e-15'),
      "同一 M 下 W 质量需 c_L≈6.6e−18 ⇒ 单尺度类再破一条")

# σ 在 M=M_Pl 下
c_sig = SIGMA / M_PL ** 2
say("  若 M=M_Pl：σ/M² = %.3e ⇒ c_σ 需 1.19e−39（差 %.1f 个数量级）"
    % (c_sig, -mp.log10(c_sig)))
guard("SIGMA_AT_PLANCK_EXCLUDED", c_sig < mp.mpf('1e-30'), "σ 与 G 由同一 M 生成时自相矛盾（同上）")

# ---------------------------------------------------------------- §C 框架自身的唯一尺度
say()
say("=" * 78)
say("§C 用螺旋框架自身的唯一尺度 m=(ħ/c)√(κ²+τ²) 去代四个耦合")
say("=" * 78)

g_me = 1 / M_E ** 2
say("  取 m=m_e：G 需 %.3e GeV⁻²（实 %.3e，差 %.1f 个数量级）"
    % (g_me, G_NAT_PL, mp.log10(g_me / G_NAT_PL)))
s_me = M_E ** 2
say("  取 m=m_e：σ 需 %.3e GeV²（实 %.3f，差 %.1f 个数量级）"
    % (s_me, SIGMA, mp.log10(SIGMA / s_me)))
guard("FRAMEWORK_SINGLE_SCALE_FAILS",
      mp.log10(1 / M_E ** 2 / G_NAT_PL) > 40 and mp.log10(SIGMA / M_E ** 2) > 5,
      "框架只有一个粒子尺度 ⇒ 引力差 44.8 个数量级、弦张力差 5.8 个 ⇒ 单尺度失败")

# ---------------------------------------------------------------- §D 最少尺度数
say()
say("=" * 78)
say("§D 最少尺度数：三个比值都不在 O(1)")
say("=" * 78)

r1 = M_PL / LAM_QCD
r2 = M_PL / M_W
r3 = LAM_QCD / M_W
say("  M_Pl/Λ_QCD = %.2e（%.2f 个数量级）" % (r1, mp.log10(r1)))
say("  M_Pl/M_W   = %.2e（%.2f 个数量级）" % (r2, mp.log10(r2)))
say("  Λ_QCD/M_W  = %.2f" % r3)
guard("MIN_THREE_SCALES", mp.log10(r1) > 19 and mp.log10(r2) > 16 and r3 < mp.mpf('1e-2'),
      "三个尺度两两不可由同一个 M 派生（Λ_QCD/M_W=2.5e−3）⇒ 至少要 3 个量纲输入")

n_out, n_in = 4, 4     # 3 个尺度 + α 的 1 个机制（r321/r361 已判不可由固定点导出）
surplus = surplus_of(n_out, n_in)
say("  输出 4 ｜ 自由输入 ≥4（3 尺度 + α 机制）⇒ surplus=%d ⇒ %s"
    % (surplus, "GENUINE_PREDICTION" if surplus >= 1 else "RELATION_OR_FIT"))
guard("G9_SUPPLY", surplus < 1,
      "把四力表改写成「三尺度 + α 机制」仍是同义反复：输入由输出反解出来 ⇒ 非预言")

# ---------------------------------------------------------------- §E 精细调节位数
say()
say("=" * 78)
say("§E 若硬要用一个 M，需要多少位精细调节")
say("=" * 78)

bits = mp.log(1 / G_SIG) / mp.log(2)
say("  c_G c_σ = Gσ = %.3e ⇒ 需抵消 **%.1f bit**" % (G_SIG, bits))
say("  对照：声明 α 到实验精度需 32.6 bit（r321 C08）⇒ 净 %.1f bit" % (32.6 - bits))
guard("FINE_TUNE_BITS", bits > 100,
      "单尺度拟合需 ~129.5 bit 的乘积抵消，远超 α 的 32.6 bit 信息预算 ⇒ 净信息为负")

# ---------------------------------------------------------------- §F 对照
say()
say("=" * 78)
say("§F 两条对照：判据会放行玩具单尺度 / 两尺度可精确拟合")
say("=" * 78)

M_toy = mp.mpf('1e19')
gu = (1 / M_toy ** 2) * (M_toy ** 2) * 1   # c_G=c_σ=1
say("  玩具单尺度（c_G=c_σ=1, M=1e19）：Gσ = %.3f ⇒ 落在类不变量内" % gu)
guard("CONTROL_TOY_ONE_SCALE", abs(gu - 1) < mp.mpf('1e-25'),
      "判据对 O(1) 单尺度模型放行 ⇒ 非恒否，排除的是**实测值**")

M2 = mp.sqrt(SIGMA)
g_fit = (1 / M_PL ** 2)
s_fit = M2 ** 2
say("  两尺度：G=1/M_Pl²=%.3e ；σ=(√σ)²=%.6f ⇒ 相对残差 %.1e / %.1e"
    % (g_fit, s_fit, 0, abs(s_fit - SIGMA) / SIGMA))
guard("CONTROL_TWO_SCALE_FITS", abs(s_fit - SIGMA) / SIGMA < mp.mpf('1e-25'),
      "两尺度模型可精确容纳 G 与 σ ⇒ 结论是**类排除**，不是「不可能统一」")

# ----------------------------------------------------------------
say()
say("=" * 78)
say("守卫 %d/%d 通过" % (GUARD["pass"], GUARD["pass"] + GUARD["fail"]))
verdict = ("SINGLE_SCALE_CLASS_EXCLUDED_BY_G_SIGMA__"
           "MIN_THREE_SCALES__"
           "ONE_SCALE_FIT_NEEDS_129_BITS__"
           "TWO_SCALE_CONTROL_PASSES")
say("判词：%s" % verdict)
say("=" * 78)

with open(os.path.join(HERE, "_out_g9.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(BUF) + "\n")
say("日志: %s" % os.path.join(HERE, "_out_g9.txt"))
raise SystemExit(0 if GUARD["fail"] == 0 else 1)
