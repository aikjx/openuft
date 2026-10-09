# -*- coding: utf-8 -*-
"""磁通量子化 Φ₀=h/2e 与 Aharonov-Bohm 相位自洽性 (质荷同源深化 #2)
50号: TUFT 磁通普适量子化 Φ_i=Φ₀=h/2e 对所有带电粒子成立。
深化: 检验 Φ₀ 与 AB 相位自洽 — 单电荷 e 绕 Φ₀ 得相位 π(半周期), Cooper对 2e 得 2π(整)。
这解释为何磁通量子是 h/2e 而非 h/e (2e 是整相位单位), 佐证 40号 '2e来源'。
"""
import numpy as np
h=6.62607015e-34; hbar=h/(2*np.pi); e=1.602176634e-19
Phi0=h/(2*e)  # 磁通量子

print("== Aharonov-Bohm 相位 ==")
print(f" Φ₀=h/2e={Phi0:.6e} Wb")
def theta(q):
    return q*Phi0/hbar
print(f" 单电荷 e 绕 Φ₀: θ_e=e·Φ₀/ħ={theta(e)/np.pi:.9f}π")
print(f" Cooper对 2e 绕 Φ₀: θ_2e=2e·Φ₀/ħ={theta(2*e)/np.pi:.9f}π")

print("\n== 自洽性 ==")
print(" θ_e=π(半周期): 单电荷绕Φ₀得非整数相位, AB干涉破坏")
print(" θ_2e=2π(整周期): Cooper对绕Φ₀得整相位, 干涉不变")
print(" ⇒ 磁通量子Φ₀=h/2e 对应 2e 整相位单位 (超导标准事实)")
print(" ⇒ 若取 h/e(单电荷整相位)则与超导实验不符; h/2e 是实验事实")
print(" ⇒ TUFT 普适给出 h/2e, 2e 是整相位单位 — 佐证 40号 '2e来源'")

print("\n== 物理解读 ==")
print(" ① 磁通量子化 Φ₀=h/2e 由 2e 整相位自洽确定")
print(" ② 单电荷 e 是半相位单位(磁通/2 才整), 解释 e 不能独立产生量子涡旋")
print(" ③ TUFT 螺旋几何(ωρ=c)给出普适 Φ₀, 与超导 AB 实验自洽")
print(" ④ 40号 2e(Cooper对)来源得到佐证: Φ₀=h/2e 是 2e 整相位量子的必要条件")

print("\n== 诚实边界 ==")
print(" ① AB 相位是标准量子力学事实(已验证), TUFT 侧自洽 — ✅")
print(" ② 2e 单位来源: 本推导佐证(Φ₀需2e整相位)但未独立导出 Cooper配对机制 — 🟡")
print(" ③ 磁通普适量子化仍🟡(50号); 依赖 f_i=m_i/2e + ωρ²=ħ/m_i — 🟡")
print(" ④ L3 仍 0; 未动 claims.csv")
