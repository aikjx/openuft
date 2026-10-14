# -*- coding: utf-8 -*-
"""标准框架·三十二期数值靶：0νββ 判决窗口精算（m_ββ=3.663865 meV 预测 vs 下一代实验灵敏度）
承接二十期（SO(10) 跷跷板：y_ν=1 → M_R=6.11e14 GeV → m_ββ=3.663865 meV；KamLAND-Zen 36-156 meV 不可达）。
本期：用 LEGEND-1000 / nEXO / CUPID 标称灵敏度反推 m_ββ-T1/2 换算因子 K=(m/m_e)^2·T1/2，
scaling 外推（本底主导 α=1/4 与近零本底 α=1/2 双口径）达到 3.66 meV 所需曝光与年数。
mpmath 250 位。来源：legend-exp.org / nEXO overview / CUPID（NSF PAR）/ arXiv:2508.18573。
"""
import mpmath as mp
import json

mp.mp.dps = 250

m_e_MeV = mp.mpf("0.51099895")
mbb_target = mp.mpf("3.663865e-3")  # meV（SO(10) 跷跷板预测，y_ν=1，二十期）

# 实验标称参数（来源标注；m_sens 用文献区间中值）
exps = [
    {"name": "LEGEND-1000", "iso": "Ge-76", "T1_2_sens": mp.mpf("1.4e28"), "m_sens_meV_lo": mp.mpf("9"),
     "m_sens_meV_hi": mp.mpf("21"), "m_sens_meV_mid": mp.mpf("15"), "E0_kg_yr": mp.mpf("1e4"),
     "M_iso_kg": mp.mpf("1000"), "bg": "近零本底", "src": "legend-exp.org: T90=1.4e28yr, m~9-21meV(3σ disc 1.2e28)"},
    {"name": "nEXO", "iso": "Xe-136", "T1_2_sens": mp.mpf("1.35e28"), "m_sens_meV_lo": mp.mpf("5.7"),
     "m_sens_meV_hi": mp.mpf("9.3"), "m_sens_meV_mid": mp.mpf("7.5"), "E0_kg_yr": mp.mpf("5e4"),
     "M_iso_kg": mp.mpf("5000"), "bg": "本底主导", "src": "nEXO overview/arXiv:2204.01733: T=1.35e28yr, m~5.7-9.3meV"},
    {"name": "CUPID", "iso": "Mo-100", "T1_2_sens": mp.mpf("1.8e27"), "m_sens_meV_lo": mp.mpf("12"),
     "m_sens_meV_hi": mp.mpf("15"), "m_sens_meV_mid": mp.mpf("13.5"), "E0_kg_yr": mp.mpf("2.4e3"),
     "M_iso_kg": mp.mpf("240"), "bg": "本底主导", "src": "NSF PAR/CUPID CDR: T=1.8e27yr, 240kg, 10yr, 5keV FWHM"},
]

print("===== 三十二期：0νββ 判决窗口精算（m_ββ=3.663865 meV，250 位）=====")
print("目标：SO(10) 跷跷板预测 m_ββ=3.663865 meV（20 期：y_ν=1、M_R=6.11e14 GeV）")

rows = []
for e in exps:
    name = e["name"]
    K = (e["m_sens_meV_mid"] / 1e3 / m_e_MeV) ** 2 * e["T1_2_sens"]  # (m/m_e)^2·T1/2 = 1/(G·M^2)
    T_target = K / (mbb_target / m_e_MeV) ** 2
    # scaling：E_req = E0·(m_mid/m_target)^(1/α)，α=1/4 本底主导，α=1/2 近零本底
    E_req_q = e["E0_kg_yr"] * (e["m_sens_meV_mid"] / (mbb_target * 1e3)) ** 4    # α=1/4
    E_req_h = e["E0_kg_yr"] * (e["m_sens_meV_mid"] / (mbb_target * 1e3)) ** 2    # α=1/2
    t_req_q = E_req_q / e["M_iso_kg"] / 10 * 10   # 年（同位素质量固定）
    t_req_h = E_req_h / e["M_iso_kg"]
    ratio = e["m_sens_meV_mid"] / (mbb_target * 1e3)  # 灵敏度与目标之比
    print("\n%s（%s）| T1/2 灵敏度=%.2e yr | m_ββ 灵敏度=%.1f meV（%.1f-%.1f）| K=%.3e" %
          (name, e["iso"], e["T1_2_sens"], e["m_sens_meV_mid"], e["m_sens_meV_lo"], e["m_sens_meV_hi"], K))
    print("  m_ββ=3.663865 meV ↔ T1/2(预测)=%.3e yr（%s NME 口径）" % (T_target, e["iso"]))
    print("  灵敏度/目标比 = %.2f 倍" % ratio)
    print("  达到 3.66 meV 所需曝光：本底主导(α=1/4)=%.3e kg·yr（=%.1f t·yr）；近零本底(α=1/2)=%.3e kg·yr（=%.1f t·yr）"
          % (E_req_q, E_req_q / 1e3, E_req_h, E_req_h / 1e3))
    print("  对应运行年数（同位素质量固定）：本底主导=%.1f 年；近零本底=%.1f 年" % (t_req_q, t_req_h))
    rows.append({
        "实验": name, "同位素": e["iso"], "T1_2_sens_yr": mp.nstr(e["T1_2_sens"], 6),
        "m_sens_meV_mid": mp.nstr(e["m_sens_meV_mid"], 4), "m_sens_meV_range": "[%.1f,%.1f]" % (e["m_sens_meV_lo"], e["m_sens_meV_hi"]),
        "K_factor": mp.nstr(K, 6), "T1_2_target_yr": mp.nstr(T_target, 6),
        "E_req_kg_yr_alpha1over4": mp.nstr(E_req_q, 8), "E_req_kg_yr_alpha1over2": mp.nstr(E_req_h, 8),
        "t_req_yr_alpha1over4": mp.nstr(t_req_q, 6), "t_req_yr_alpha1over2": mp.nstr(t_req_h, 6),
        "背景模式": e["bg"], "来源": e["src"],
    })

# 判决窗口
print("\n===== 判决窗口判定 =====")
print("下一代实验 10 年标称灵敏度：LEGEND-1000 m~9-21 meV | nEXO m~5.7-9.3 meV | CUPID m~12-15 meV")
print("目标 m_ββ=3.66 meV：低于全部下一代实验 10 年灵敏度下限（最低 nEXO 5.7 meV 仍高 1.6 倍）")
print("→ 10 年窗口无法触及；若 2030s-2040s 无信号排除至 ~6 meV，正常序 3.66 meV 预测仍存活")
print("→ 达到 3.66 meV：本底主导口径需曝光 4.4e5-2.8e6 kg·yr（≈440-2800 t·yr），近零本底口径 3.3e4-2.1e5 kg·yr（≈33-210 t·yr）")
print("→ 等效运行年数（同位素质量固定，本底主导）：nEXO(5t) ~176 年 / LEGEND-1000(1t) ~2809 年 / CUPID(240kg) ~1843 年")
print("→ 判决时间窗估计：2040s-2050s（下一代之后 + 零本底升级/百吨级 LXe）")
print("倒序质量区（m_ββ≥~15-50 meV）：LEGEND-1000 10 年即可覆盖——下一代实验判定的是倒序 vs 混合，不是正常序 3.66")

out = {
    "期次": "三十二",
    "目标": "m_ββ=3.663865 meV（SO(10) 跷跷板 y_ν=1，二十期）",
    "换算公式": "K=(m/m_e)^2·T1/2=1/(G·M^2)，每实验用标称中值反推；scaling E_req=E0·(m_mid/m_t)^(1/α)，α=1/4 本底主导/α=1/2 近零本底",
    "实验参数": rows,
    "判决": [
        "下一代实验 10 年灵敏度（5.7-21 meV）全部高于 3.66 meV，无法触及正常序预测",
        "若 2030s-2040s 无信号排除至 ~6 meV，正常序 3.66 meV 仍存活",
        "达到 3.66 meV 需曝光（本底主导 α=1/4）：4.4e5-2.8e6 kg·yr（≈440-2800 t·yr）；近零本底 α=1/2：3.3e4-2.1e5 kg·yr（≈33-210 t·yr）",
        "等效运行年数（本底主导）：nEXO(5t) ~176 年 / LEGEND-1000(1t) ~2809 年 / CUPID(240kg) ~1843 年",
        "判决时间窗：2040s-2050s；下一代实验先判倒序质量区（m_ββ≥~15-50 meV）",
    ],
    "诚实边界": "scaling 为文献标准幂律近似；K 因子依赖核矩阵元（phenom. NME 口径），质量换算不确定度 ±2 倍量级",
}
with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\标准框架_0vbb判决窗口精算32.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\njson 已写入：标准框架_0vbb判决窗口精算32.json")
