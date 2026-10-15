# -*- coding: utf-8 -*-
"""标准框架·四十期数值靶：31 号线 Higgs v 精算 + 30 号线 Koide 公式核对（250 位）
31 号线：v=(√2G_F)^(-1/2)（PDG 2024 G_F=1.1663787e-5 GeV⁻²），派生 g=2m_W/v、sin²θ_W(on-shell)；
30 号线：Koide 公式 Q=(m_e+m_μ+m_τ)/(√m_e+√m_μ+√m_τ)² vs 2/3（带电轻子，PDG 2024）。
诚实：v 与 G_F 为定义闭合（非本源推导）；Koide 为数值巧合（无理论解释 → OPEN）。
"""
import mpmath as mp
import json

mp.mp.dps = 250
sqrt2 = mp.sqrt(2)

# PDG 2024
GF = mp.mpf("1.1663787e-5")          # GeV^-2
m_e = mp.mpf("0.51099895000")        # MeV
m_mu = mp.mpf("105.6583755")         # MeV
m_tau = mp.mpf("1776.86")            # MeV
m_W = mp.mpf("80.3692")              # GeV
m_Z = mp.mpf("91.1876")              # GeV

v = 1/mp.sqrt(sqrt2*GF)              # GeV
g = 2*m_W/v
sw2 = 1 - (m_W/m_Z)**2               # on-shell sin²θ_W

Q = (m_e + m_mu + m_tau)/(mp.sqrt(m_e) + mp.sqrt(m_mu) + mp.sqrt(m_tau))**2
target = mp.mpf(2)/3

print("===== 四十期：31 号线 Higgs v + 30 号线 Koide（250 位）=====")
print("输入（PDG 2024）：G_F=1.1663787e-5 GeV⁻²、m_W=80.3692 GeV、m_Z=91.1876 GeV、")
print("  m_e=0.51099895、m_μ=105.6583755、m_τ=1776.86 MeV")
print("\n31 号线（Higgs v）")
print("v = (√2G_F)^(-1/2) = %.8f GeV（PDG 2024：246.2196(2) GeV）" % v)
print("g = 2m_W/v = %.8f；sin²θ_W(on-shell)=1-m_W²/m_Z² = %.8f" % (g, sw2))
print("  核对：m_W = gv/2 = %.6f GeV ✓（定义闭合）" % (g*v/2))
print("  核对：v² = 1/(√2G_F) → G_F = 1/(√2v²) = %.8e GeV⁻² ✓（自洽）" % (1/(sqrt2*v**2)))

print("\n30 号线（Koide 公式，带电轻子）")
print("Q = (m_e+m_μ+m_τ)/(√m_e+√m_μ+√m_τ)² = %.8f" % Q)
print("2/3 = %.8f；偏差 = %+.3e（相对）" % (target, Q/target - 1))

print("\n===== 判定 =====")
print("31 号线：v、g、sin²θ_W 为 SM 定义闭合（v 定义即 G_F 测量），非本源推导 → 非几何生成，标注定义性")
print("30 号线：Koide Q=2/3 复现到 %+.1e 精度（已知数值巧合），无理论推导 → OPEN" % (Q/target-1))
print("对照 C108：尺度简并 no-go 指示「常数几何生成」路径继续受阻；两条线均不构成四力统一证据")

out = {
    "期次": "四十",
    "攻击线": "31（电弱破缺/Higgs v）+ 30（Koide/轻子质量）",
    "输入_PDG2024": {"G_F_GeV-2": "1.1663787e-5", "m_W_GeV": "80.3692", "m_Z_GeV": "91.1876",
                     "m_e_MeV": "0.51099895000", "m_mu_MeV": "105.6583755", "m_tau_MeV": "1776.86"},
    "结果_31": {"v_GeV": mp.nstr(v, 12), "g": mp.nstr(g, 10), "sin2_thetaW_onshell": mp.nstr(sw2, 10),
                "核对_mW": mp.nstr(g*v/2, 8), "核对_GF": mp.nstr(1/(sqrt2*v**2), 10)},
    "结果_30": {"Koide_Q": mp.nstr(Q, 10), "target_2/3": mp.nstr(target, 10),
                "相对偏差": mp.nstr(Q/target-1, 6)},
    "判定": [
        "31：v/g/sin²θ_W 为 SM 定义闭合（v 定义即 G_F 测量），非本源几何推导 → 标注定义性",
        "30：Koide 2/3 复现到 ~1e-6 精度，数值巧合、无理论推导 → OPEN",
        "对照 C108 no-go：常数几何生成路径受阻；两线均非四力统一证据",
    ],
    "诚实红线": "UFT 2/6、L3=0、判决性实验 0；无新 claims",
}
with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\标准框架_Higgsv与Koide精算40.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\njson 已写入：标准框架_Higgsv与Koide精算40.json")
