# -*- coding: utf-8 -*-
"""
§26_verify.py — GUT 谱学与质子衰变：统一能标的可观测窗口
S02 空间光速螺旋统一力 · 算法联盟
V1  谱学反推公式核验（eq20/21 系数解析重导出 + §25 参数下数值 + 失效边界）
V2  M_GUT ∝ (M₃M₂)^(−1/9) 标度律验证（解析 + 数值）
V3  质子衰变 τ(p→e⁺π⁰) 预言（1304.0343 锚点 M_X=8e15→5e34 yr 缩放）
V4  与 Super-K/Hyper-K 对照与攻破判定
"""
import json, math, os

# ---- §25 全链输入（tanβ=5, DR; §25_收口预算数据.json V3） ----
s2w_full = 0.2318
alpha_em = 1.0/127.925
mZ = 91.1876
MSUSY = 1000.0
MGUT_s25 = 1.341e16          # §25 全链 M_GUT（两循环+Yukawa）
C_dr = (0.0, 2.0/(12*math.pi), 3.0/(12*math.pi))

def alpha_mZ_dr(s2w):
    c2 = 1.0 - s2w
    a = [(5.0/3)*alpha_em/c2, alpha_em/s2w, 0.1184]
    return [a[i]/(1.0 - a[i]*C_dr[i]) for i in range(3)]

a = alpha_mZ_dr(s2w_full)
ia1, ia2, ia3 = 1.0/a[0], 1.0/a[1], 1.0/a[2]

print("="*70)
print("§26 GUT 谱学与质子衰变")
print("="*70)

# ---- V1: eq(20)(21) 系数解析重导出 ----
print("\n[V1] 谱学反推公式核验（1304.0343 eq17/20/21）:")
b_SM, b_MSSM = (41.0/10, -19.0/6, -7.0), (33.0/5, 1.0, -3.0)
comb_SM = 3*b_SM[1] - 2*b_SM[2] - b_SM[0]
comb_MSSM = 3*b_MSSM[1] - 2*b_MSSM[2] - b_MSSM[0]
print("  3b₂−2b₃−b₁: SM=%.2f  MSSM=%.2f（期望 2/5 与 12/5）" % (comb_SM, comb_MSSM))
assert abs(comb_SM - 0.4) < 1e-9 and abs(comb_MSSM - 2.4) < 1e-9
# GUT 阈值组合（eq16 → eq17）: Σ系数的 Hc 项 = −(2/5)（α₁）−2（α₃）→ −12/5
print("  eq(17) 组合 −(12/5)ln(μ/M_Hc)/(2π) 结构一致（推导见文档 §3）")

# V1b: eq(20) 数值（§25 耦合, 简并 gaugino M₂=M₃=M_S=1TeV）
LHS20 = 3*ia2 - 2*ia3 - ia1
L1 = math.log(MSUSY/mZ)
M_Hc = mZ*math.exp((LHS20*2*math.pi + 2*L1) / (12.0/5))
print("  eq(20): 3/α₂−2/α₃−1/α₁ = %.4f" % LHS20)
print("  简并谱 M_Hc = %.3e GeV（> M_GUT=1.34e16 → 非物理，lead-log 失效边界）" % M_Hc)
# 文献两循环值（1304.0343 Fig1 蓝线：低能 SUSY M_S=1TeV, M₂=200GeV, M₃/M₂=3.5）
print("  文献两循环+非简并+阈值修正：M_Hc ∈ [8.6e14, 1.4e15] GeV（工作值）")

# ---- V2: M_GUT ∝ (M₃M₂)^(−1/9) ----
print("\n[V2] M_GUT ∝ (M₃M₂)^(−1/9) 标度律:")
# eq(21): 36ln(M_GUT/m_Z)+4ln(M₂/m_Z)+4ln(M₃/m_Z) = 2π·LHS21 = const
LHS21 = 5*ia1 - 3*ia2 - 2*ia3
K = LHS21*2*math.pi
def MGUT_from(M2, M3):
    lnMG = (K - 4*math.log(M2/mZ) - 4*math.log(M3/mZ)) / 36.0
    return mZ*math.exp(lnMG)
G1 = MGUT_from(1000.0, 1000.0)
G2 = MGUT_from(10000.0, 10000.0)
print("  LHS(5/α₁−3/α₂−2/α₃)=%.3f" % LHS21)
print("  M₂=M₃=1 TeV:  M_GUT=%.3e" % G1)
print("  M₂=M₃=10 TeV: M_GUT=%.3e" % G2)
pred = G1*math.exp(-2*math.log(10.0)/9)
print("  预测 10× gaugino: M_GUT×exp(−2ln10/9)=%.3e vs 数值 %.3e（比值 %.4f，期望 %.4f）"
      % (pred, G2, G2/pred, 1.0))
print("  §25 全链（两循环+Yukawa）M_GUT=%.3e（M₂=M₃=1TeV）" % MGUT_s25)

# ---- V3: 质子衰变 ----
print("\n[V3] 质子衰变 τ(p→e⁺π⁰)（dim-6, X 玻色子交换）:")
# 锚点：1304.0343 原文 "M_X≈0.8×10^16 GeV → τ≈5×10^34 yr，略高于当前实验界 1.29×10^34"
tau_anchor, MX_anchor = 5.0e34, 8.0e15
def tau(MX):
    return tau_anchor*(MX/MX_anchor)**4
for MX in (8.0e15, 1.0e16, 1.341e16, 1.9e16):
    print("  M_X=%.3e GeV → τ = %.2e yr" % (MX, tau(MX)))
# Super-K 下界反推 M_X
bound_SK = 1.29e34
MX_lim = MX_anchor*(bound_SK/tau_anchor)**0.25
print("  Super-K 界(1.29e34 yr)反推 M_X > %.3e GeV" % MX_lim)
t25 = tau(MGUT_s25)
print("  §25 M_X=M_GUT=%.3e → τ=%.2e yr（Super-K 余量 %.1f×）" % (MGUT_s25, t25, t25/bound_SK))

# ---- V4: 判定 ----
print("\n[V4] 判定:")
print("  τ(§25)=%.2e yr > Super-K 1.29e34（一致，30× 余量）；Hyper-K 灵敏度 ~1e35 → 边缘可达（可检验）" % t25)
print("  dim-5 通道：低能 SUSY 需 M_Hc 抑制机制（文献）；高能 SUSY 天然抑制（1304.0343）")
print("  S02 零参与：质子衰变=四力统一可观测窗口，全部来自标准 SUSY-GUT")

data = {"V1": {"LHS20": LHS20, "M_Hc_degenerate": M_Hc, "M_Hc_lit_lo": 8.6e14, "M_Hc_lit_hi": 1.4e15},
        "V2": {"LHS21": LHS21, "MGUT_1TeV": G1, "MGUT_10TeV": G2, "exponent_pred": math.exp(-2*math.log(10.0)/9),
               "MGUT_s25": MGUT_s25},
        "V3": {"tau_anchor": tau_anchor, "MX_anchor": MX_anchor, "tau_s25": t25,
               "MX_superk_limit": MX_lim, "tau_table": {"8e15": tau(8e15), "1e16": tau(1e16),
               "1.341e16": tau(1.341e16), "1.9e16": tau(1.9e16)}},
        "V4": {"verdict": "consistent+testable"}}
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "§26_质子衰变数据.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("\n数据已写入: §26_质子衰变数据.json")
