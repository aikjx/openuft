# 全域统一场论 · TUFT 拓扑统一场论（汤川势 + 电磁挠率 + 静态仿真 章 · 全维修复版）

> **版本**：v2.0（2026-09-16）｜**上游**：O9 姊妹篇《从 κ–τ 公理导出麦克斯韦/薛定谔/汤川势》 + 算法联盟总报告
> **状态图例**：🔵 导出（可复算）· 🟠 模型假设（须标注）· 🔴 开放（不可导出/已被排除）
> **本版变更**：依据《全维审校与异常报告》实施 R1–R6 六项修复。校验脚本 `TUFT_汤川势电磁挠率_算法联盟全维校验.py`（25 项判定：PASS 18 / FAIL 2 / OPEN 3 / PARTIAL 1 / INFO 1）。
> **红线声明**：数学自洽 ≠ 物理实证成立。凡未能导出者不称"定理"。

---

## 0. 修复摘要

| 编号 | 原稿问题 | 判定 | 修复（本版） |
|---|---|---|---|
| F1 | 步骤 2 积分错误：声称 ∫c²A·e^{−μr}/r·dr = −c²A·e^{−μr}/r | 🔴 FAIL | R1：改用正确原函数 **V(r)=−c²A·E1(μr)**（E1 势，承继算法联盟 A6） |
| F2 | μ 双重角色（电磁 τ 又带屏蔽） | 🔴 FAIL | R2：**电磁扇区 μ_EM≡0**；μ=10¹⁵ 仅属强作用曲率场 κ（O16 强制） |
| P1 | 仿真数值梯度 150× 系统性误差 | 🟡 PARTIAL | R3：解析导数 dτ/dr=−C_τ·e^{−μr}(μ/r+1/r²) |
| P2 | 符号约定未声明 | ✅ PASS(需声明) | R5：显式 A>0、κ>0（g=−c²κ 指向源，势为负） |
| O-C | 术语 τ 三重含义 | 🟠 OPEN | R4：本章电磁映射场更名 **τ^EM**（拓扑矢势） |
| I1 | "下一步 A"薛定谔推导未衔接 | ℹ️ INFO | R6：引用 O9-5（已闭合），不重复推导 |

---

## 一、强相互作用：曲率场 κ 与短程核力势

### 1.1 物理图像

TUFT 中强相互作用起源于基本粒子拓扑孤子核心区域的曲率场 κ。**按算法联盟 O-LAYER 分层**：孤子自曲率 κ_int 定质量（κ_int=mc/ħ，电子 2.59×10¹² m⁻¹），外场曲率 κ_field 定势；本章的"核力曲率"属于**核心区的 κ_int 级曲率**，其短程衰减给出核力。强作用力是曲率梯度带来的短程力；有质量媒介介子的传递给出短程相互作用势。

**媒介介子质量**（承继 O9-4 康普顿-曲率恒等式，🔵）：
$$ m_\pi = \frac{\hbar}{c}\sqrt{\kappa_X^2+\tau_X^2} = \frac{\hbar\mu}{c},\qquad \mu=\frac1\lambda $$
其中 $\lambda$ 是力程，$\sqrt{\kappa_X^2+\tau_X^2}$ 是交换子的 Frenet 总转动率——**力程不需要额外参数**。

### 1.2 曲率场静态方程与解（🔵，步骤 1 保持正确）

静态达朗贝尔退化为亥姆霍兹方程；孤子核心为局域紧致源，近似点源：
$$ \nabla^2\kappa-\mu^2\kappa=-4\pi\,C_\kappa\,\delta^{(3)}(\boldsymbol r) $$

球对称无源区 $r>0$：$\dfrac1{r^2}\dfrac{d}{dr}\left(r^2\dfrac{d\kappa}{dr}\right)-\mu^2\kappa=0$；令 $u=r\kappa$ 得 $u''-\mu^2u=0$；边界条件舍去 $e^{+\mu r}$：
$$ \boxed{\ \kappa(r)=\frac{A}{r}\,e^{-\mu r}\ } $$
点源归一（通量极限 −4πA 匹配源强，AL-D1-1b PASS）：**A=C_κ**。

### 1.3 ★ 从曲率场到势能（🔵 修复版——原稿步骤 2 的纠正）

**原稿错误**（AL-D1-1c FAIL）：原稿写"$dV/dr=c^2A\,e^{-\mu r}/r$ 积分得到 $V=-g^2e^{-\mu r}/r$"。但 $\dfrac{d}{dr}\!\left[-c^2A\,\dfrac{e^{-\mu r}}{r}\right]=c^2A\,e^{-\mu r}\!\left(\dfrac{\mu}{r}+\dfrac1{r^2}\right)\neq c^2A\,\dfrac{e^{-\mu r}}{r}$，差因子 $-(\mu r+1)$。**$\int e^{-\mu r}/r\,dr$ 不是 $e^{-\mu r}/r$**。

**正确推导**：设加速度 $g=-c^2\kappa$，保守场 $g=-\nabla V$：
$$ \frac{dV}{dr}=c^2A\,\frac{e^{-\mu r}}{r} \;\Longrightarrow\; \boxed{\ V(r)=-c^2A\,E_1(\mu r)\ } $$
其中 $E_1(z)=\int_z^\infty e^{-t}/t\,dt$ 为指数积分（$dE_1(\mu r)/dr=-e^{-\mu r}/r$，数值核对相对误差 3.9×10⁻¹⁰，AL-D1-1d PASS）。

**E1 势的性质**（AL-D1-1e PASS）：
- 大 r（汤川尾）：$E_1(\mu r)\approx\dfrac{e^{-\mu r}}{\mu r}$ ⇒ $V\approx-\dfrac{c^2A}{\mu}\cdot\dfrac{e^{-\mu r}}{r}$ —— **与标准汤川势长程等价**，有效耦合 $g^2_{\rm eff}=c^2A/\mu$；
- 小 r（对数奇性）：$E_1(\mu r)\approx-\gamma-\ln(\mu r)$ ⇒ $V\approx c^2A(\gamma+\ln\mu r)\to-\infty$ —— **短程对数型，与汤川 1/r 可区分**（算法联盟 A6 的可检验要点）；
- 全程 $V(r)<0$（E1>0，A>0）⇒ **纯吸引**；**不含排斥芯**（R2 开放，见 §四）。

**两种自洽路线（二选一，不可混用）**：
| 路线 | 定义 | 势 | 出处 |
|---|---|---|---|
| A：κ 为势 | κ 满足亥姆霍兹点源方程，V 即 κ 场本身 | V=−g²e^{−μr}/(4πr) | O9-6（🔵） |
| B：κ 为力场 | κ 是加速度场源（g=−c²κ），V=−∫c²κ·dr | **V=−c²A·E1(μr)** | 本章修复版（🔵） |

原稿把两路线的结果混写（路线 B 的 κ 形状 + 路线 A 的势形状），是 F1 的根源。

### 1.4 参数物理对应（🔵）

$\mu=\dfrac{m_\pi c}{\hbar}$，$\lambda=\dfrac1\mu=\dfrac{\hbar}{m_\pi c}$：$m_\pi=139.57$ MeV/c² ⇒ $\lambda=1.4138$ fm（经验核力力程 1.4 fm，偏差 0.99%，AL-D4-4a PASS）；对应 $\mu_\pi=7.07\times10^{14}$ m⁻¹。仿真取 μ=10¹⁵ m⁻¹ ⇔ λ=1 fm ⇔ m≈197.3 MeV/c²，与 π 介子同量级。

### 1.5 🔴 结构性矛盾：光子无质量（O16，本章必须收口）

质量公式 $m=\frac{\hbar}{c}\sqrt{\kappa^2+\tau^2}>0$ 使任何孤子都有正质量。若把电磁挠率场 τ^EM 也当作带屏蔽参数的场（μ≠0），则电磁力程有限。由实验上限 $m_\gamma<10^{-18}$ eV/c² 反推：
$$ \sqrt{\kappa^2+\tau^2}\big|_\gamma < 5.07\times10^{-12}\ \mathrm{m^{-1}} \;\Longrightarrow\; R_\gamma>1.32\ \mathrm{AU} $$
（AL-D4-4d PASS，与 O9 §5.3 一致）。**结论（R2 修复）**：**屏蔽参数 μ 只能属于强作用曲率场 κ；电磁扇区 μ_EM≡0（退化为长程库仑）**。仿真中的"屏蔽汤川型"演示应标注为 **κ 场类比**，不得直接命名为电磁 τ 场。

---

## 二、电磁：矢量挠率场 τ^EM 与能量-动量张量

### 2.1 术语澄清（R4 修复，🟠）

| 符号 | 含义 | 体系 |
|---|---|---|
| τ_w | 孤子世界线 Frenet 挠率（螺旋几何，定质量/自旋） | O9 / 主论 |
| **τ^EM** | **本章电磁映射场**（拓扑矢势，∝A_μ） | 本章（原稿"挠率场 τ"更名） |
| T_μ | 引力挠率（=κS_μ，自旋-挠率耦合，挠子 ~10⁻³ eV） | 白皮书 P9/P10 |

三者物理意义不同，混用会导致 P10 挠子亚毫米约束被错误套用到电磁场。

### 2.2 映射与张量（🔵 结构层）

电磁势 $A_\mu\propto\tau^{\rm EM}_\mu$（A_μ 的几何构造为 🟠 假设 C，见 O9 §2.2）。映射：
$$ \boldsymbol B = k\,\nabla\times\boldsymbol\tau^{\rm EM},\qquad \boldsymbol E = -k\left(c\,\nabla\tau^{\rm EM}_t+\frac{\partial\boldsymbol\tau^{\rm EM}}{\partial t}\right) $$
场张量（AL-D5-5a/5b PASS，符号自洽）：
$$ F^{0i}=-\frac{E_i}{c}=k\left(\nabla_i\tau^{\rm EM}_t+\frac1c\partial_t\tau^{\rm EM}_i\right),\qquad F^{ij}=-\varepsilon^{ijk}B_k $$
能量-动量张量（与标准 SI 形式同构）：
$$ T^{\mu\nu}_{\ \tau}= \mathcal{E}_\tau\left(F^{\mu\alpha}F^{\nu}_{\ \alpha}-\frac14\eta^{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}\right) $$
三维分解（静态 ∂_t=0）：$u_\tau=\frac12\left(\mathcal{E}_\tau|\boldsymbol E|^2+\frac1{\mathcal{M}_\tau}|\boldsymbol B|^2\right)$；$c^2=1/(\mathcal{E}_\tau\mathcal{M}_\tau)$（定义保持）。

> ⚠️ **边界**：本节给出的是**结构**（齐次部分可由 F=∂A 纯数学导出，见 O9-2 🔵），给不出**标度**——$\varepsilon_0$、$e$、$\alpha$ 不可由三公理导出（O15 🔴）。$\mathcal{E}_\tau,\mathcal{M}_\tau,k$ 为模型标定参数（🟠）。

### 2.3 静态极限（🔵）

球对称纯径向 τ^EM：∇×τ^EM=0 ⇒ **B≡0**（AL-D5-5c PASS，符合静电学）；E=−kc∇τ^EM_t；能量密度 u=½ε_τE²。

---

## 三、Python 静态挠率场仿真（修复版）

### 3.1 修复说明

| # | 原稿问题 | 修复 |
|---|---|---|
| 1 | 同一行双 import（SyntaxError） | 分行 |
| 2 | **数值梯度 150× 系统性误差**（log 网格，AL-D6-6b PARTIAL） | 解析导数 dτ/dr=−C_τ·e^{−μr}(μ/r+1/r²) |
| 3 | `mu`（屏蔽）与 `mu_tau`（磁导率）命名冲突 | 屏蔽参数更名 `mu_shield` |
| 4 | 无保存输出 | 增加 savefig + 中文字体配置 |
| 5 | μ 双重角色（F2） | 注释明确：屏蔽演示为 **κ 场类比**，电磁扇区 μ=0 |

### 3.2 代码（修复版，已实机运行验证）

```python
# -*- coding: utf-8 -*-
"""TUFT 静态球对称挠率场仿真（v2 修复版）——屏蔽演示为 κ 场类比；电磁扇区 μ_EM=0"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "SimSun"]
plt.rcParams["axes.unicode_minus"] = False

k = 1.0               # 拓扑电磁耦合常数（τ^EM 映射用；模型标定参数）
mu_shield = 1.0e15    # 屏蔽参数：仅代表强作用曲率场 κ 的短程衰减；电磁扇区必须取 0
C_tau = 1.0           # 场源强度（模型标定参数）
c = 299792458.0
eps_tau = 1.0
mu_tau = 1.0 / (c**2 * eps_tau)

r_min, r_max, Nr = 1e-16, 2e-14, 800
r_arr = np.logspace(np.log10(r_min), np.log10(r_max), Nr)

tau_arr = C_tau / r_arr * np.exp(-mu_shield * r_arr)
# 解析导数（替代数值梯度，消除 log 网格 ~150x 误差）
dtau_dr = -C_tau * np.exp(-mu_shield * r_arr) * (mu_shield / r_arr + 1.0 / r_arr**2)

E_arr = -k * c * dtau_dr
B_arr = np.zeros_like(r_arr)          # 纯径向场旋度为零 ⇒ B=0
u_em = 0.5 * (eps_tau * E_arr**2 + B_arr**2 / mu_tau)

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
ax1, ax2, ax3, ax4 = axes.flatten()
ax1.loglog(r_arr, np.abs(tau_arr)); ax1.set_title(r"挠率场 $|\tau(r)|$ (静态点源)")
ax1.set_xlabel("$r$ [m]"); ax1.set_ylabel(r"$|\tau|$"); ax1.grid(True, alpha=0.3)
ax2.loglog(r_arr, np.abs(E_arr)); ax2.set_title(r"映射电场 $|E(r)|$")
ax2.set_xlabel("$r$ [m]"); ax2.set_ylabel("$|E|$"); ax2.grid(True, alpha=0.3)
ax3.loglog(r_arr, u_em); ax3.set_title(r"TUFT 电磁能量密度 $u_\tau(r)$")
ax3.set_xlabel("$r$ [m]"); ax3.set_ylabel(r"$u_\tau$"); ax3.grid(True, alpha=0.3)
tau_coul = C_tau / r_arr
dtau_coul_dr = -C_tau / r_arr**2
E_coul = -k * c * dtau_coul_dr
ax4.loglog(r_arr, np.abs(E_arr), label=rf"$\mu$={mu_shield:.2e} 短程汤川屏蔽")
ax4.loglog(r_arr, np.abs(E_coul), label=r"$\mu$=0 长程库仑", linestyle="--")
ax4.set_title("电场对比：屏蔽 vs 无屏蔽库仑")
ax4.set_xlabel("$r$ [m]"); ax4.set_ylabel("$|E|$"); ax4.legend(); ax4.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("TUFT_torsion_simulation.png", dpi=150)
plt.show()

idx_list = [0, Nr // 4, Nr // 2, 3 * Nr // 4, -1]
print(f"{'r[m]':<12}{'tau':<14}{'|E|':<14}{'u_em':<14}")
for i in idx_list:
    print(f"{r_arr[i]:12.3e}{tau_arr[i]:14.3e}{abs(E_arr[i]):14.3e}{u_em[i]:14.3e}")
```

### 3.3 数值结果（实机运行，AL-D6-6a 与解析值逐位一致）

| 采样点 | r [m] | τ(r) | \|E(r)\| | u_τ(r) |
|---|---|---|---|---|
| 0 | 1.00×10⁻¹⁶ | 9.048×10¹⁵ | 2.984×10⁴⁰ | 4.452×10⁸⁰ |
| 200 | 3.77×10⁻¹⁶ | 1.822×10¹⁵ | 1.996×10³⁹ | 1.992×10⁷⁸ |
| 400 | 1.42×10⁻¹⁵ | 1.705×10¹⁴ | 8.716×10³⁷ | 3.798×10⁷⁵ |
| 600 | 5.34×10⁻¹⁵ | 8.930×10¹¹ | 3.178×10³⁵ | 5.050×10⁷⁰ |
| 799 | 2.00×10⁻¹⁴ | 1.031×10⁵ | 3.244×10²⁸ | 5.262×10⁵⁶ |

**行为**：r≪1/μ 时 E∝1/r²（库仑区，斜率 −2）、u∝r⁻⁴；r≳1/μ 时指数衰减主导（屏蔽曲线弯折下坠，库仑参考线保持斜率 −2）；B≡0。

---

## 四、开放缺口总表（修复后）

| 编号 | 内容 | 状态 | 来源 |
|---|---|---|---|
| O15 | ε₀ / e / α 的几何本源（非齐次 Maxwell 第一性导出） | 🔴 开放 | O9 §2.4；本章 ε_τ、μ_τ、k 待定 |
| O16 | 无质量规范玻色子在螺旋孤子类中的容身处 | 🔴 开放 | O9 §5.3；本章 μ_EM=0 强制（R2） |
| R2 | 核力排斥芯（r≲0.5 fm 强排斥） | 🔴 开放 | 算法联盟 R2；续篇 26.3 前置 1 |
| — | 质量项 μ²κ 为模型假设 | 🟠 假设 | 原稿；非公理推论 |
| — | μ、g²_eff 需拓扑孤子散射标定 | 🟠 假设 | 原稿；O-SCALE 尺度简并支持（k²L³=const，绝对尺度自由） |
| — | A_μ 的几何构造（τ^EM∝A_μ） | 🟠 假设 C | O9 §2.2 |
| — | τ^EM 场动力学方程（等效 Maxwell 源项） | 🔴 开放 | 本章/原稿；源系数无法纯拓扑定出（联盟 R4） |
| — | 强场球对称解（TOV 类比） | 🔴 开放 | 联盟 R6 / P-C1 |

---

## 五、与 O9 / 算法联盟 / 白皮书衔接

| 本章条目 | 上游对应 | 关系 |
|---|---|---|
| §1.2 亥姆霍兹解 | O9-6 E1/E2（残差 0、δ 归一） | 同解，A=C_κ=g/4π 重标定 |
| §1.3 E1 势 | 算法联盟 A6（E1 势替代汤川） | 本审计独立复现（F1 解析出处） |
| §1.4 力程-质量 | O9-4 康普顿-曲率恒等式 | μ=√(κ²+τ²) 无需额外参数 |
| §1.5 光子矛盾 | O9 §5.3 / O16 | 本章收口为 μ_EM=0 |
| §2 电磁张量 | O9-2（齐次 Maxwell 🔵）、O9-2.2（A_μ 🟠）、O9-2.4（标度 🔴） | 结构/标度分层一致 |
| §3 仿真 | O9 §9 路线 2 大纲 | 无量纲化基准 ℓ₀=1/√(κ₀²+τ₀²) 待接入 |
| 薛定谔方程 | O9-5（已闭合） | 本章不重复推导，直接引用 |

---

## 六、下一步（修复后重排）

1. **E1 势接入仿真**：对比 E1 势（短程对数）与汤川势（1/r）的 |E(r)| 曲线，产出 B 级可检验差异图（对应 A6 建议 3：低能 NN 相移比对）；
2. **排斥芯推导**（R2）：目标给出 r≲0.5 fm 的强排斥，衔接 2M_⊙ 中子星状态方程（续篇 26.3 前置 1）；
3. **强场球对称解**（P-C1 升级）：TOV 类比，把中子星质量-半径/潮汐形变从"候选"升级为"可检验预言"；
4. **全体系术语更名表**：τ_w / τ^EM / T_μ 三区命名，防止预言交叉污染。

---
*修复依据：《全域统一场论_TUFT汤川势电磁挠率章_全维审校与异常报告.md》；校验脚本及产物：`TUFT_汤川势电磁挠率_算法联盟全维校验.{py,json,txt}`。*
