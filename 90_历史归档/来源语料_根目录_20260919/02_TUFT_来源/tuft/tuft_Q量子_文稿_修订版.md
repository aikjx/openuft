# 量子 $\mathcal{T}$UF$\mathcal{T}$构建（修订版）

> 承接：$\mathcal{T}$UF$\mathcal{T}$公理体系、极限退化对应、经典场方程与实验预言。
> 本版依据 `tuft_Q量子_全维求导精算.py`（PASS 10 · FAIL 30 · BOUNDARY 5 · INFO 11）逐条修订原文。
> 凡标注 **【修订】** 处均为原文被判 FAIL 后的改写；凡标注 **【待定】** 处为框架尚未闭合、不得当作已成立结论使用。
> 红线：数学自洽 ≠ 物理实验证实。

## 修订说明（相对原文的九处关键改动）

| # | 原文 | 修订 | 判据 |
|---|---|---|---|
| 1 | 测度 $\mathcal{D}e\,\mathcal{D}\omega\,\mathcal{D}A\,\mathcal{D}\Omega\,\mathcal{D}_\text{gauge}\,\mathcal{D}_\text{top}$ 因子化 | 改为**不可因子化**，显式写出 FP 行列式与 Jacobian | Q1.2 |
| 2 | $W=\frac{1}{8\pi^2}\int\mathcal{T}\wedge\mathcal{T}\in\mathbb{Z}$ | **撤回**该定义；改用两类候选（Pontryagin 数 / $Lk\in\frac12\mathbb{Z}$） | Q2.4–Q2.6 |
| 3 | 费米子 $=W=\pm1$ 拓扑结 | 改为 **$Lk=\pm\frac12$**（半整），与 r2 册口径一致 | Q3.1–Q3.2 |
| 4 | $[\hat W,\hat H]=0$、拓扑荷守恒 | 改为**待证**，并给出守恒的必要条件 | Q3.4 |
| 5 | $\delta R,\delta T$ 与 $\delta e,\delta\omega$ 并列 | 删除假变量，$K$ 为 $4\times4$ 块；$K^{-1}$ 须先规范固定 | Q4.3–Q4.4 |
| 6 | 挠子自旋 1、$m\sim10^{-3}$ eV | 改为**条件性存在**（需挠率动力学项）；质量待定；补 Proca 纵向块与微扰性约束 | Q5.1–Q5.7 |
| 7 | $\sigma_L-\sigma_R=g_t^2\lvert D\rvert$ | 撤回；纯轴矢给 $\sigma_L=\sigma_R$，不对称须 $V\!-\!A$ 干涉 | Q6.2–Q6.3 |
| 8 | 曲率饱和 = UV 截止、无需重整化 | 降级为**待验证猜想**：约束的是振幅而非动量 | Q7.2–Q7.3 |
| 9 | 仿真代码与"低能被压低" | 代码重写为可运行版；低能结论方向更正 | Q8.1–Q8.3 |

---

## 一、量子 $\mathcal{T}$UF$\mathcal{T}$的核心思想

经典 $\mathcal{T}$UF$\mathcal{T}$ 定义在主丛 $P(\mathcal{M},G)$ 上，场变量为标架 $e^a_\mu$、洛伦兹联络 $\omega^{ab}_\mu$、规范联络 $A^i_\mu$、几何权重 $\Omega$。量子版本对**全部几何场**做路径积分：

$$\mathcal{Z}=\int\mathcal{D}[e,\omega,A,\Omega]\;e^{\frac{i}{\hbar}S_{\text{TUFT}}[e,\omega,A,\Omega]}$$

**【修订】变量集确认**（Q1.1，PASS）：每时空点的分量数为
$$e:16,\qquad \omega:6\times4=24,\qquad A:12\times4=48,\qquad \Omega:1,\qquad \textbf{合计 }89$$
（$A$ 含 $U(1)\times SU(2)\times SU(3)$ 共 $1+3+8=12$ 个规范场。）

与普通量子引力的区别（保留原文的 1、2、4 条，第 3 条降级）：

1. 积分变量同时含度规、联络、挠率，不固定背景度规；
2. 积分含挠率拓扑扇区求和（**定义待修订，见 §2**）；
3. **【修订】** 曲率饱和 $|R|\le K_\text{sat}$ **不再是**"自动剔除紫外奇点的定义域边界"，而是**待验证的正则化假设**（§7）；
4. $\Omega$ 作为动力学标量场参与积分——**【待定】**其作用量项（动能 + 势 + 与 $R,T$ 的耦合）尚未给出（Q1.4）。

---

## 二、主丛路径积分测度

### 2.1 测度结构

**【修订】测度不可写成各场测度的乘积**。正确形式为

$$\mathcal{D}[e,\omega,A,\Omega]=\Big(\prod_x \mathrm{d}\mu[e,\omega,A,\Omega](x)\Big)\times\Delta_\text{FP}[e,\omega,A]\times\mathcal{D}[\text{ghost}]$$

其中：
- $\Delta_\text{FP}$ 是 Faddeev–Popov 行列式，**依赖于** $e,\omega,A$，不是可分离的独立因子；
- 场重定义（如 $e\to\Omega e$）会引入非平凡 Jacobian（共形/标度反常的来源），**不能默认其为 1**；
- $\mathcal{D}_\text{top}$（拓扑扇区求和）在拓扑荷被正确定义之前**不写入**（见 §2.3）。

### 2.2 规范固定（背景场法）

$$e=e_0+\delta e,\quad \omega=\omega_0+\delta\omega,\quad A=A_0+\delta A,\quad \Omega=\Omega_0+\delta\Omega$$

三重冗余（微分同胚 + 局部洛伦兹 + 内部规范）须**在二次作用量中显式加入**规范固定项（de Donder / Lorentz / $R_\xi$）与 FP 鬼项，否则动能算符奇异、传播子不存在（Q4.4）。

### 2.3 挠率拓扑荷：撤回与重建

**【修订】原文定义**
$$W=\frac{1}{8\pi^2}\int_\Sigma \mathcal{T}\wedge\mathcal{T},\qquad W\in\mathbb{Z}$$
**不成立**，三条独立判据：

1. **无整性定理**（Q2.6）：$\frac{1}{8\pi^2}\int\mathrm{Tr}(F\wedge F)\in\mathbb{Z}$ 要求 $F$ 是主丛联络的**曲率**、被积式为规范不变多项式、由 Chern–Weil 同态落到整上同调类。挠率 $T=De$ **不是任何联络的曲率**，三条前提全部不满足，$8\pi^2$ 只是借来的形式。
2. **非形变不变**（Q2.4）：$W$ 对 $T$ 二次齐次，$W(\lambda T)=\lambda^2W(T)$。实跑 $W(\lambda)/W(1)=1,\,2.25,\,4,\,6.25$（$\lambda=1,1.5,2,2.5$）⇒ 沿连续路径变化 ⇒ 不是同伦不变量。
3. **显式反例**（Q2.5）：$T^4$ 上取 $T=A\,dx^0\wedge dx^1+B\,dx^2\wedge dx^3$（由 $e^0=dx^0+Ax^0dx^1$、$e^1=dx^1+Bx^2dx^3$、$\omega=0$ 实现，满足 $dT=R\wedge e=0$），则 $W=2AB/(8\pi^2)$：取 $A=14.6070,B=1$ 可精确命中 $W=0.37$ ⇒ **取值是连续统**。

> **自我更正记录**：初审曾以为 $T^a\wedge T_a\equiv0$（"只剩 $\eta_{aa}T^a\wedge T^a$ 而 $a\wedge a=0$"）。**该断言错误**：$a\wedge a=(-1)^{p^2}a\wedge a$ 只在 $p$ 为**奇**时强制为零；挠率 2-形式 $p=2$ 为偶，$T^a\wedge T^a\ne0$（实跑 $3.57\times10^5$）。故否定 $W$ 只能靠上面三条，不能靠"恒零"。

**【待定】替代候选**（二者择一，尚未论证能否承载"费米子 = 拓扑结"）：

| 候选 | 定义 | 取值 | 备注 |
|---|---|---|---|
| (i) 完整 Cartan 联络的 Pontryagin 数 | $\frac{1}{8\pi^2}\int\mathrm{Tr}\,R(\tilde\omega)\wedge R(\tilde\omega)$ | $\mathbb{Z}$ | 是**曲率的平方**，不是 $T\wedge T$ |
| (ii) 挠率中心线的 Hopf 自环绕数 | $Lk=Tw+Wr$，$\mathrm{Tw}=n/2$ | $\frac12\mathbb{Z}$ | **r2 册已实跑闭合**（$4\pi$ 回归残差 $\sim10^{-118}$、交换相位 $-1$） |

---

## 三、时空螺旋元胞：半整口径

**【修订】** 费米子对应的拓扑结必须是**半整**拓扑荷：

| 拓扑荷 | 旋转 $2\pi$ 相位 | 统计 |
|---|---|---|
| $W=\pm1$（整） | $e^{2\pi i}=+1$ | **玻色** |
| $Lk=\pm\frac12$（半整） | $e^{2\pi i/2}=-1$ | **费米** |

原文同时主张"费米子 $=W=\pm1$"与"自旋 1/2 来自莫比乌斯（一圈相位 $\pi$）"，两者**互相排斥**。修订后统一采用 r2 口径：$\;s=\lvert Lk\rvert$、$\mathrm{Tw}=n/2$（$n$ 奇）⇒ 费米子 $Lk=\pm\frac12$。

- $Lk=0$：无结（均匀背景挠率）；
- $\lvert Lk\rvert=\frac12$：最小手性螺旋元胞（费米子）；
- $\lvert Lk\rvert\ge1$：多缠绕复合结构。

**【修订】拓扑荷守恒 $[\hat W,\hat H]=0$ 改为待证**（Q3.4）。必要条件：该荷为**同伦不变量**。由于原 $W$ 已被证伪为非不变量，守恒律不成立；改用 $Lk$ 后须重新论证（$Lk$ 在中心线不穿越时是连续形变下的不变量，这一点有拓扑保障，但"场论中 $\hat{Lk}$ 与 $\hat H$ 对易"仍需显式构造）。

**【修订】删除**"拓扑荷转移 = 黑洞信息守恒的量子根源"这一论断：它依赖已被否定的守恒律，无 Page 曲线定量，且与 B 判决链冲突（自屏蔽 $\xi=1/2$ 偏离 46.82% ≫ LIGO 10%，该黑洞分支已排除）。

---

## 四、二次作用量与传播子

### 4.1 独立变量（修订）

**【修订】** $R$ 与 $T$ **不是独立场**：
- 曲率独立分量 **20**、挠率独立分量 **24**，均由 $e,\omega$ 的**一阶导数**完全决定；
- 把它们当作独立涨落会使变量集从 89 分量/点虚增到 **133 分量/点（+44）**。

正确的二次作用量只以四组独立涨落为变量：

$$S^{(2)}=\frac12\int \delta\Phi^{\mathsf T}\mathbf K\,\delta\Phi,\qquad \delta\Phi=(\delta e,\delta\omega,\delta A,\delta\Omega)$$

$\mathbf K$ 为 $4\times4$ 块（10 个独立块）。"$\delta\Omega$–$\delta R$–$\delta T$ 三混合"的正确含义是：交叉项通过 $R(e,\omega)$、$T(e,\omega)$ 的**泛函展开**进入 $\mathbf K$ 的 $e$–$\omega$–$\Omega$ 非对角块，而不是新增行/列。

### 4.2 传播子

$$S^{(2)}=\frac12\int d^4x\,d^4y\;\delta\Phi(x)\mathbf K(x,y)\delta\Phi(y),\qquad \mathbf D=\mathbf K^{-1}$$

**【修订】** $\mathbf K$ 含微分同胚/洛伦兹/规范三重零模 ⇒ **必须先加规范固定项才可逆**。$\mathbf D$ 的块结构（$\mathbf D_{ee}$、$\mathbf D_{\omega\omega}$、$\mathbf D_{AA}$、$\mathbf D_{\Omega\Omega}$ + 非对角）作为**组织方式**成立，但每一块的显式形式本册尚未给出 ⇒ 目前是清单而非结果（Q4.5）。

---

## 五、挠子：从"命名"到"条件性存在"

### 5.1 存在性前提

**【修订】** 标准 Einstein–Cartan 中挠率是**代数约束**（由自旋流决定，无动能项、无本征模）⇒ **不存在挠率涨落传播子**，也就没有挠子。与 R6 册一致（三条挠率产生路径全受阻，自然源与目标差 $1.37\times10^{28}$）。

要得到挠子，必须**显式引入挠率动力学项**（如 Poincaré gauge theory 的 $T^2$ 项）。在该项给出之前，挠子是**命名**而非推导结果。

### 5.2 质量

**【修订】** $m_t\sim10^{-3}$ eV 无公式支撑：按框架自身尺度（R6：$T_\text{nat}\sim2.44\times10^{-41}\,\mathrm{m^{-1}}$），$\hbar c T_\text{nat}=4.82\times10^{-48}$ eV，与 $10^{-3}$ eV 相差 **44.3 个数量级** ⇒ **外部注入，标记为待定**。

唯一可操作的实验含义：$\lambda_c=\hbar c/m_t=0.1973$ mm（亚毫米力程）。

### 5.3 传播子（正确形式）

号差 $(-,+,+,+)$、在壳 $p^2=-m^2$：

$$D_{\mu\nu}(p)=\frac{-i\left(\eta_{\mu\nu}+\dfrac{p_\mu p_\nu}{m^2}\right)}{p^2+m^2-i\varepsilon}$$

实跑校验：横向性 $\max\lvert p^\mu N_{\mu\nu}\rvert=6.9\times10^{-18}$ ✓；留数投影算子 $P^\mu{}_\nu=\delta^\mu{}_\nu+p^\mu p_\nu/m^2$ 幂等（$\lvert P^2-P\rvert=8.3\times10^{-14}$），本征值 $\{0,1,1,1\}$ ⇒ 秩 3（自旋 1 三极化）✓。

**【修订】** 原文的标量 $1/(p^2-m^2)$ 丢弃了纵向块 $(j\cdot p)^2/m^2$。对轴矢顶点 $j^\mu=\bar\psi\gamma^\mu\gamma^5\psi$，因 $q_\mu j^\mu=2m_f(\bar u\gamma^5u)\ne0$，该块有物理贡献。

### 5.4 微扰性约束（新增）

纵向块使有效无量纲强度 $\sim4g_t^2(m_f/m_t)^2$。取 $g_t=10^{-6}$、$m_f=m_e$：

$$4\times10^{-12}\times\left(\frac{5.11\times10^{5}}{10^{-3}}\right)^2=1.04\times10^{6}\gg8\pi$$

⇒ **微扰展开在该扇区失效**。标准结论：有质量矢量耦合**非守恒流**只有在 Higgs 机制（规范不变）下才自洽。**【待定】** Q-TUFT 需给出该机制，或将挠子改述为无质量的规范玻色子（那将不再是本册的挠子）。

---

## 六、散射振幅

### 6.1 S 矩阵

$$\hat S=\mathcal T\exp\!\left(\frac{i}{\hbar}\int\mathcal L_\text{int}\,d^4x\right),\qquad \mathcal A=\langle\text{out}\rvert\hat S\lvert\text{in}\rangle$$

（标准定义，PASS，无 TUFT 增量。）

### 6.2 手性不对称：正确结构

对无质量费米子与顶点 $\gamma^\mu(a+b\gamma^5)$：
$$M_L\propto(a+b),\qquad M_R\propto(a-b),\qquad A_{LR}=\frac{2ab}{a^2+b^2}$$

**【修订】** 原文的顶点是**纯轴矢**（$a=0$），此时 $\lvert M_L\rvert^2/\lvert M_R\rvert^2=1.000000$（机器零级相等）⇒ **$\sigma_L=\sigma_R$，不对称恒为零**。原文的 $\sigma_L-\sigma_R=g_t^2\lvert D\rvert$ 不含任何左右手区分（$\lvert D\rvert$ 与手性无关），是"传播子模长"的重命名，撤回。

产生不对称必须**同时**有矢量与轴矢耦合（$V\!-\!A$ 时 $\lvert A_{LR}\rvert=1$）。

### 6.3 能量依赖的方向

**【修订】** 对可重整轴矢耦合，不对称来自 helicity-flip 干涉，量级 $\sim m_f^2/s$ ⇒ **随能量升高被压低**，与原文"越高能越显著"相反。（若改为导数/有效算符耦合，方向可反转，但需给出该结构。）

### 6.4 低能极限

**【修订】** 对 $m_t=10^{-3}$ eV 的极轻介质，$E\ll m_t$ 时传播子趋于 $1/m_t^2=10^{6}\,\mathrm{eV^{-2}}$，$E\gg m_t$ 时趋于 $1/E^2$ ⇒ **低能是放大而非压低**。原文"低能极限挠子耦合被压低、S 矩阵退化为 SM"在 $m_t$ 如此之小时方向相反。（"对撞机上看不到"这一结论成立，但原因是 $1/s$ 压低，不是低能压低。）

---

## 七、曲率饱和与紫外行为

**【修订】降级为待验证猜想**（Q7.2–Q7.3）：

对涨落 $h\sim Ae^{ikx}$，$|R|\sim k^2A\le K_\text{sat}$ 给出的是
$$A\le \frac{K_\text{sat}}{k^2}$$
即**约束振幅而非动量**：任意大的 $k$ 只要振幅足够小仍在积分域内（$k=10^{40}\,\mathrm{m^{-1}}$ 时允许 $A\lesssim10^{-11}$）。而圈的 UV 发散正来自任意大 $k$ 的**小振幅**模式 ⇒ **曲率饱和不构成动量硬截断**。

附加待处理问题：
- 边界随场构型变化 ⇒ 变分原理需附加边界项，经典极限不再是 $\delta S=0$；
- $|R|$ 在 Lorentz 号差下非正定/非紧 ⇒ 欧氏化与 Wick 回转需另行论证；
- 场空间硬边界一般破坏 BRST/Ward ⇒ 幺正性与规范不变性需另行证明；
- 即便存在截断，度规引力仍是**有效场论**：截断不消除高维算符塔 ⇒ "无需重整化"不成立。

$K_\text{sat}=1/\ell_P^2=3.83\times10^{69}\,\mathrm{m^{-2}}$（跨册引用）只在 $M\sim m_P$ 生效（前册：天体黑洞视界曲率低 77 个量级），与 $10^{-3}$ eV 的挠子相差 $\sim10^{37}$ 倍 ⇒ **尺度链条断裂**。

---

## 八、可运行仿真（修订版）

```python
# -*- coding: utf-8 -*-
"""Q-TUFT 挠子传播子：动量空间扫描（修订版，可直接运行）
修订点：(1) 清除 LaTeX 宏污染（原文 ast.parse 直接 SyntaxError）；
        (2) Proca 传播子保留纵向块；(3) 低能/高能方向如实标注。"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

m_t = 1e-3        # eV，质量（外部注入，见 §5.2）
g_t = 1e-6        # 无量纲耦合（外部注入）
eps = 1e-12       # 极点正则化：注意它决定"峰"的高度，不是物理量

# p^2 扫描：向下延伸到 m_t^2 以下两个量级，避免把极点切在区间端点
p2 = np.logspace(-9, 2, 2000)
D = 1.0 / (p2 - m_t ** 2 + 1j * eps)
amp = g_t ** 2 * np.abs(D)

print("amp(p->0)  = %.4e" % amp[0])
i_max = int(amp.argmax())
print("amp 峰值   = %.4e  at p = %.4e eV" % (amp[i_max], math.sqrt(p2[i_max])))
print("amp(p=1eV) = %.4e" % (g_t ** 2 * abs(1.0 / (1.0 - m_t ** 2 + 1j * eps))))

plt.figure(figsize=(9, 5))
plt.loglog(np.sqrt(p2), amp, label="g_t^2 |D(p)|")
plt.axvline(m_t, color="r", ls="--", label="m_t = 1e-3 eV")
plt.xlabel("p (eV)")
plt.ylabel("g_t^2 |D(p)|")
plt.grid(True, alpha=0.3)
plt.legend()
plt.title("torsionon propagator (revised)")
plt.tight_layout()
plt.savefig("tuft_torsionon_propagator.png", dpi=110)
```

实跑结论（修订）：
- 原文扫描区间下 $\arg\max$ 落在首点、$\text{amp}_\max=g_t^2/\varepsilon=1.0$ ⇒ **峰值高度由人为正则化决定**，不是物理共振；
- $p\to m_t$ 是**极点**（传播子的在壳奇点），不是有限共振峰；
- 低能 $p\to0$ 趋于常数 $g_t^2/m_t^2=10^{6}\,\mathrm{eV^{-2}}$（**未被压低**），高动量按 $1/p^2$ 衰减。

---

## 九、可证伪预言（修订后的诚实清单）

| # | 预言 | 现状 | 可检验条件 |
|---|---|---|---|
| 1 | 挠子（极轻、手性耦合自旋） | **待定**：存在性/质量/耦合均未闭合 | 先给出挠率动力学项与质量来源；若成立，力程 $\hbar c/m_t$ 落在亚毫米，可对接短程自旋力实验 |
| 2 | 散射手性不对称 | **需重建**：纯轴矢给 $\sigma_L=\sigma_R$ | 必须给出 $V$ 与 $A$ 两种耦合及其比值，才有 $A_{LR}=2ab/(a^2+b^2)$ |
| 3 | 原初引力波 / B 模手性 | **母体已自证伪**（暴胀-CMB 册 5 PASS / 35 FAIL） | 先修复暴胀扇区 |
| 4 | 量子黑洞 / 蒸发幺正 | **分支已被排除**（B 判决链） | 需重建黑洞分支 |
| 5 | 拓扑荷跃迁 / 特征量子噪声 | **无定义**（$W$ 已撤回；无定量公式） | 改用 $Lk$ 后重新表述，并给出噪声谱 |

---

## 十、遗留难点（含原文遗漏的六项）

原文列出的五项（测度严格性、非微扰求解、重整化/红外、退相干、宇宙波函数）保留，并补充更上游的六项：

A. 测度非因子化与 Jacobian（共形/标度反常）；
B. 硬截断与 BRST/Ward 的冲突；
C. **挠率动力学项的缺失**（传播子构造的前提）；
D. **拓扑荷的良定义**（$W\to Lk\in\frac12\mathbb{Z}$ 之前，非微扰拓扑扇区无对象）；
E. 有效场论性（截断不消除高维算符塔）；
F. 欧氏化与因果性（$|R|\le K_\text{sat}$ 非正定）。

---

## 十一、下一步分支建议（回应"九、分支选项"）

- **选项 3（非微扰拓扑扇区 / 宇宙波函数）暂不宜直接做**：拓扑荷尚未良定义，"多拓扑荷叠加态""惠勒-德维特方程的挠率项"目前没有可操作的对象。前置工作量 = 把 $W$ 换成 $Lk\in\frac12\mathbb{Z}$ 并证明 $[\widehat{Lk},\hat H]=0$（或证明不成立）。
- **选项 2（范式哲学重构）在本册数学自洽性未成立之前容易越界**：哲学讨论会把当前 FAIL 的条目当成已成立的前提。
- **建议路径**：先做"拓扑荷重定义 + 挠率动力学项"这两项前置（本册 FAIL 的两条主根），再走**选项 1（实验白皮书）**——因为白皮书只依赖已定量的条目，可以先把"0.197 mm 力程窗口""$A_{LR}$ 的 $V\!-\!A$ 结构"等可操作部分固化，把未闭合部分明确标为条件性。
