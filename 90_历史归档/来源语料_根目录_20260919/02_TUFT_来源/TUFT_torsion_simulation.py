# -*- coding: utf-8 -*-
"""
TUFT 拓扑统一场论 —— 静态球对称挠率场仿真
=============================================
模型演示代码（非真实物理实验）。
静态（∂t=0），点源，球对称：
  tau(r) = (C_tau / r) * exp(-mu_shield * r)
映射：E = -k*c*grad(tau_t)，B = k*curl(tau) = 0（纯径向场旋度为零）
能量密度：u = 0.5*(eps_tau*E^2 + B^2/mu_tau)

相对原始粘贴版本的修复：
  1. 拆分同一行双 import（原代码 SyntaxError）
  2. 用解析导数 dtau/dr = -C_tau*e^{-mu r}*(mu/r + 1/r^2)
     替代 np.gradient(r_arr) 的数值梯度用法（log 采样下更精确）
  3. 屏蔽参数改名 mu_shield，避免与拓扑磁导率 mu_tau 命名冲突
  4. 增加 plt.savefig 输出 PNG
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 中文字体配置（Windows）
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "SimSun"]
plt.rcParams["axes.unicode_minus"] = False

# ===================== 仿真全局参数（TUFT 模型标定参数，非 CODATA 物理真值） =====================
k = 1.0               # 拓扑电磁耦合常数 k_e = k_m = k
mu_shield = 1.0e15    # 挠率场屏蔽参数；mu=0 退化为长程库仑，mu>0 短程汤川
C_tau = 1.0           # 挠率点源强度
c = 299792458.0
eps_tau = 1.0         # TUFT 拓扑等效介电常数
mu_tau = 1.0 / (c**2 * eps_tau)  # 拓扑等效磁导率（满足 c^2 = 1/(eps*mu)）

# 径向坐标采样（对数均匀）
r_min, r_max, Nr = 1e-16, 2e-14, 800
r_arr = np.logspace(np.log10(r_min), np.log10(r_max), Nr)

# ===================== 静态球对称挠率场亥姆霍兹解 =====================
# 无源区解 tau(r) = (C_tau / r) * exp(-mu_shield * r)，点源归一 A = C_tau
def tau_field(r):
    return C_tau / r * np.exp(-mu_shield * r)

tau_arr = tau_field(r_arr)

# 解析导数：dtau/dr = -C_tau * e^{-mu r} * (mu/r + 1/r^2)
dtau_dr = -C_tau * np.exp(-mu_shield * r_arr) * (mu_shield / r_arr + 1.0 / r_arr**2)

# 静态场：∂t=0；球对称只有径向 tau，∇×tau=0 ⇒ B=0
# 映射：E = -k*c*∇tau_t；B = k*∇×tau = 0
E_arr = -k * c * dtau_dr
B_arr = np.zeros_like(r_arr)  # 纯径向场旋度为零，磁场为 0

# 电磁能量密度 u = 0.5*(eps*E^2 + B^2/mu)
u_em = 0.5 * (eps_tau * E_arr**2 + B_arr**2 / mu_tau)

# ===================== 绘图输出 =====================
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
ax1, ax2, ax3, ax4 = axes.flatten()

ax1.loglog(r_arr, np.abs(tau_arr))
ax1.set_title(r"挠率场 $|\tau(r)|$ (静态点源)")
ax1.set_xlabel("$r$ [m]")
ax1.set_ylabel(r"$|\tau|$")
ax1.grid(True, alpha=0.3)

ax2.loglog(r_arr, np.abs(E_arr))
ax2.set_title(r"映射电场 $|E(r)|$")
ax2.set_xlabel("$r$ [m]")
ax2.set_ylabel("$|E|$")
ax2.grid(True, alpha=0.3)

ax3.loglog(r_arr, u_em)
ax3.set_title(r"TUFT 电磁能量密度 $u_\tau(r)$")
ax3.set_xlabel("$r$ [m]")
ax3.set_ylabel(r"$u_\tau$")
ax3.grid(True, alpha=0.3)

# 对比：关闭屏蔽 mu=0，库仑 1/r 场
tau_coul = C_tau / r_arr
dtau_coul_dr = -C_tau / r_arr**2
E_coul = -k * c * dtau_coul_dr
ax4.loglog(r_arr, np.abs(E_arr), label=rf"$\mu$={mu_shield:.2e} 短程汤川屏蔽")
ax4.loglog(r_arr, np.abs(E_coul), label=r"$\mu$=0 长程库仑", linestyle="--")
ax4.set_title("电场对比：屏蔽 vs 无屏蔽库仑")
ax4.set_xlabel("$r$ [m]")
ax4.set_ylabel("$|E|$")
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("TUFT_torsion_simulation.png", dpi=150)
print("PNG saved.")

# 打印部分采样点数据
idx_list = [0, Nr // 4, Nr // 2, 3 * Nr // 4, -1]
print(f"{'r[m]':<12}{'tau':<14}{'|E|':<14}{'u_em':<14}")
for i in idx_list:
    print(f"{r_arr[i]:12.3e}{tau_arr[i]:14.3e}{abs(E_arr[i]):14.3e}{u_em[i]:14.3e}")
