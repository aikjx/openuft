# -*- coding: utf-8 -*-
"""
算法联盟 · 统一场论攻破 · 弦标度→GUT 标度衔接精算（49 期）
==========================================================
日期   : 2026-10-24
对标   : hep-th/9602045v3 / hep-th/0001093 (异质弦统一) + OpenUFT 48 期 GUT 跑动
引擎   : mpmath dps=60

攻破对象: 48 期 OPEN 项——M_string/M_GUT=23.3（log10=1.37）需 ~1.4 数量级阈值修正。
核心攻破: 48 期同时用「α_GUT⁻¹=24.3 精确对齐」（隐含 g_string=√(4π/24.3)=0.719）
          与「M_string=5.27e17」（隐含 g_string=1）——两假设不自洽。
          正确异质弦统一关系 g²·k = g_string² 要求一旦 α_GUT 对齐，g_string 被锁定，
          M_string 必须重算。本脚本给出两种约定的自洽 M_string 与标度差，并扫描
          Kac-Moody level / 超荷归一 / 阈值修正三通道，判定弦标度问题真实量级。

约定说明:
  [粒子物理约定] α_GUT = g²/(4π)，α_GUT⁻¹≈24.3 → g_string=√(4π/24.3)=0.719
  [弦论约定    ] α_GUT = g_string²        ，α_GUT⁻¹≈24.3 → g_string=√(1/24.3)=0.203
  48 期 M_string=5.27e17 对应 g_string=1（不随 α_GUT 对齐自洽）。
"""
import json, math
import mpmath as mp
mp.mp.dps = 60
mpp = mp.mpf

# ---- 输入 ----
MPlanck = mpp('1.2209e19')       # GeV 非约化普朗克质量 √(1/G_N)
gamma_E = mpp('0.5772156649015328606')
MGUT = mpp('2.26e16')            # 48 期 MSSM 一阶统一点
alpha_GUT_inv = mpp('24.2873')   # 48 期一阶统一点（粒子物理约定）
alpha_GUT = mpp(1)/alpha_GUT_inv

# 异质弦常数
C_het = mp.e**((1-gamma_E)/2) * mpp(3)**mpp('-0.75') / (4*mp.pi)
print("异质弦常数 C_het =", mp.nstr(C_het, 12), "(应≈0.043133)")

def M_string_for(g):   # GeV
    return C_het * g * MPlanck

def spread_log10(Ms):
    return mp.log10(Ms/MGUT)

results = {"meta": {"date":"2026-10-24","engine":"mpmath dps=60","basis":"hep-th/9602045v3 + OpenUFT48"},
           "het_const": mp.nstr(C_het,12), "MPlanck": mp.nstr(MPlanck,6), "MGUT_48": mp.nstr(MGUT,6),
           "alpha_GUT_inv": mp.nstr(alpha_GUT_inv,6)}

# ---- A. 三种 g 假设下的 M_string 与标度差 ----
print("\n===== A. 异质弦标度：g 假设 vs 标度差 =====")
cases = {
  "48期(隐含g=1)":   mpp('1.0'),
  "粒子物理(g=√4π/24.3)": mp.sqrt(4*mp.pi*alpha_GUT),
  "弦论约定(g=√1/24.3)":  mp.sqrt(alpha_GUT),
}
case_out = {}
for name, g in cases.items():
    Ms = M_string_for(g)
    s = spread_log10(Ms)
    case_out[name] = {"g_string": mp.nstr(g,8), "M_string_GeV": mp.nstr(Ms,6),
                      "M/M_GUT": mp.nstr(Ms/MGUT,5), "log10_spread": mp.nstr(s,5)}
    print("  %-28s g=%-10s M_string=%-12s M/M_GUT=%-8s log10=%.4f" % (name, mp.nstr(g,6), mp.nstr(Ms,5), mp.nstr(Ms/MGUT,5), float(s)))
results["A_Mstring_by_g"] = case_out

# ---- B. Kac-Moody level 扫描：g_string²=4π·α_GUT/k ----
print("\n===== B. Kac-Moody level k：对 M_string 与所需修正的影响 =====")
km_out = {}
for k in [1,2,3,4,5,6,8,10]:
    g2 = 4*mp.pi*alpha_GUT/k
    g = mp.sqrt(g2)
    Ms = M_string_for(g)
    s = spread_log10(Ms)
    km_out[str(k)] = {"g_string": mp.nstr(g,6), "M_string": mp.nstr(Ms,5), "log10_spread": mp.nstr(s,4)}
    print("  k=%2d  g_string=%-8s M_string=%-11s log10(Ms/MGUT)=%.3f" % (k, mp.nstr(g,5), mp.nstr(Ms,5), float(s)))
# 恰好闭合所需 k：M_string=MGUT → g=MGUT/(C_het·MPlanck)
g_close = MGUT/(C_het*MPlanck)
k_close = 4*mp.pi*alpha_GUT/(g_close*g_close)
print("  → 恰好闭合(M_string=MGUT)需 g=%.4f, 即 Kac-Moody level k≈%.1f (不现实)" % (float(g_close), float(k_close)))
results["B_KacMoody"] = km_out
results["B_k_close"] = mp.nstr(k_close,4)

# ---- C. 阈值修正 Δα 的量级：把 α_GUT 有效值平移多少可闭合 ----
print("\n===== C. 阈值修正量级（粒子物理约定 g=0.719） =====")
# 一阶跑动：α_i⁻¹(MZ)=α_GUT⁻¹ −(b_i/2π)ln(M_GUT/MZ)。
# 若要 M_string 成为统一点，需 M_string 处 α_i 也统一 → 需 Δα_i 修正。
# 估算: 阈值修正 Δ(α⁻¹) ~ (b/2π)·ln(M_string/M_GUT)
g_pp = mp.sqrt(4*mp.pi*alpha_GUT)
Ms_pp = M_string_for(g_pp)
b1,b2,b3 = mpp('33')/5, mpp('1'), mpp('-3')   # MSSM
ln_ratio = mp.log(Ms_pp/MGUT)
for bi,name in [(b1,"b1"),(b2,"b2"),(b3,"b3")]:
    d = bi*ln_ratio/(2*mp.pi)
    print("  Δα_%s⁻¹(M_string→M_GUT) ≈ %s" % (name, mp.nstr(d,5)))
    # 若统一点从 M_GUT 移到 M_string，α_GUT⁻¹ 需改动量
print("  → 粒子物理约定需 ~%.2f 个数量级阈值修正" % float(spread_log10(Ms_pp)))
print("  → 弦论约定需 ~%.2f 个数量级阈值修正" % float(spread_log10(M_string_for(mp.sqrt(alpha_GUT)))))
results["C_threshold"] = {"g_pp": mp.nstr(g_pp,6), "M_string_pp": mp.nstr(Ms_pp,5),
                          "log10_pp": mp.nstr(spread_log10(Ms_pp),4),
                          "log10_string_conv": mp.nstr(spread_log10(M_string_for(mp.sqrt(alpha_GUT))),4)}

# ---- D. 判定 ----
print("\n===== D. 判定 =====")
log10_48 = float(spread_log10(mpp('5.27e17')))
log10_pp = float(spread_log10(Ms_pp))
log10_sc = float(spread_log10(M_string_for(mp.sqrt(alpha_GUT))))
print("  48期(隐含g=1):    log10(Ms/MGUT)=%.3f 需 ~%.2f 数量级修正" % (log10_48, log10_48))
print("  粒子物理自洽g:    log10(Ms/MGUT)=%.3f 需 ~%.2f 数量级修正" % (log10_pp, log10_pp))
print("  弦论约定自洽g:    log10(Ms/MGUT)=%.3f 需 ~%.2f 数量级修正" % (log10_sc, log10_sc))
print("\n  攻破结论：")
print("  1) 48期 M_string=5.27e17 与 α_GUT=24.3 对齐不自洽（g=1 vs g=0.719）。")
print("  2) 粒子物理约定自洽 M_string=%.3e GeV（g=0.719），标度差从 1.37 收窄到 %.3f。" % (float(Ms_pp), log10_pp))
print("  3) 弦论约定自洽 M_string=%.3e GeV（g=0.203），标度差仅 %.3f——已落在标准阈值修正可覆盖量级。" % (float(M_string_for(mp.sqrt(alpha_GUT))), log10_sc))
print("  4) Kac-Moody level k=2~5 可把所需修正降到 ~0.9~1.0 数量级，仍不闭合；k≈%.0f 才恰好闭合（不现实）。" % float(k_close))
print("  5) 诚实：弦标度问题在弱耦合异质弦框架内未第一性闭合；本卷为口径修正+通道量化，非新物理。")

results["D_verdict"] = {
  "48期_log10": mp.nstr(log10_48,4),
  "粒子物理_log10": mp.nstr(log10_pp,4),
  "弦论_log10": mp.nstr(log10_sc,4),
  "结论": "48期口径不自洽；自洽后标度差收窄；弦论约定下 ~0.7 数量级可被标准阈值修正覆盖；纯Kac-Moody level不闭合；弦标度问题仍OPEN但量级被纠正"
}

with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\算法联盟_弦标度衔接精算49_2026-10-24.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\njson 已写入：算法联盟_弦标度衔接精算49_2026-10-24.json")
