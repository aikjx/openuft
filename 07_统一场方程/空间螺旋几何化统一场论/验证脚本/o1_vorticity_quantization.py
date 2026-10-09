# -*- coding: utf-8 -*-
"""涡量量子化 ∮v·dl=h/m: Onsager-Feynman 自洽性 (质荷同源深化 #3)
50号: 磁通普适 Φ_i=Φ₀=h/2e. Φ=f·∮v·dl → ∮v·dl=Φ₀/f_i=h/m_i.
深化: ∮v·dl=h/m_i 是速度场涡量量子化 — 与超流氦 Onsager-Feynman 量子化涡旋 ∮v·dl=n·h/m 一致。
验证数值 + 与超流氦对照。
"""
import numpy as np
h=6.62607015e-34
print("== 涡量量子化 ∮v·dl=h/m ==")
print(f" Φ₀=h/2e, f_i=m_i/2e → ∮v·dl=Φ₀/f_i=(h/2e)/(m_i/2e)=h/m_i")
def vline(m): return h/m
print(f" 电子: ∮v·dl=h/m_e={vline(9.1093837015e-31):.4e} m²/s")
print(f" μ子:  ∮v·dl=h/m_μ={vline(1.883531627e-28):.4e} m²/s")
print(f" 氦⁴:  ∮v·dl=h/m_He4={vline(6.6464731e-27):.4e} m²/s")

print("\n== Onsager-Feynman 量子化涡旋 (超流氦, 标准实验事实) ==")
print(" 超流氦⁴量子化涡旋: ∮v·dl=n·h/m_He4 (n=1,2,...)")
print(" 基态(n=1): ∮v·dl=h/m_He4=9.9735e-8 m²/s (已测, Onsager-Feynman 1949)")
print(" TUFT 电子涡量=h/m_e=7.274e-4 m²/s — 同形式(普适量子化 h/m)")

print("\n== 自洽性 ==")
print(" ① TUFT 磁通普适(50) → ∮v·dl=h/m_i (涡量量子化, m_i 消去后普适)")
print(" ② 与超流氦 Onsager-Feynman ∮v·dl=n·h/m 同构(标准实验事实) — 自洽, 不新增矛盾")
print(" ③ A=v 框架中速度场涡量量子化 = h/m: 磁场量子化(磁通Φ₀) ⇔ 速度场涡量量子化")

print("\n== 电荷量子化关联 ==")
print(" ① 每个磁通量子Φ₀(50号)对应一个涡量量子∮v·dl=h/m_i")
print(" ② 电荷量子化单位 e 关联磁通量子(51号: 2e整相位)")
print(" ③ 涡量量子化是电荷-磁通量子化的动力学实现(质荷同源深化)")

print("\n== 诚实边界 ==")
print(" ① ∮v·dl=Φ₀/f_i=h/m_i 是 50号 的直接推论(✅代数); Onsager-Feynman 是实验事实 — 自洽")
print(" ② 依赖 f_i=m_i/2e + ωρ²=ħ/m_i (🟡); 电荷量子化拓扑机制未独立导出(🟡)")
print(" ③ 超流氦涡旋是中性超流; TUFT 用于带电粒子, 对应关系为同构非等同(🟡)")
print(" ④ L3 仍 0; 未动 claims.csv")
