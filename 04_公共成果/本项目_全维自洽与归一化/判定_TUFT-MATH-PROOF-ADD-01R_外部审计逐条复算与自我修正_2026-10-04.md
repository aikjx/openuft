# 判定：TUFT-MATH-PROOF-ADD-01R 外部审计逐条复算与自我修正（第二轮）

- **被审**：`TUFT-MATH-PROOF-ADD-01`（复权重场 Ω + 弱域手征/宇称破缺定量推导 · Part B；误差传播收紧 g-2 / UHECR 区间 · Part C；审计闭环清单 · Part D）
- **审计来源**：外部审计意见（14 节逐条批判，含总审计结论表 16 行）
- **前置**：`整理_TUFT-MATH-PROOF-ADD-01_复权重场与误差传播_交叉审计与分支裁定_2026-10-04`（N1–N5 + 分支裁定）· `突破_TUFT-MATH-PROOF-ADD-02_Omega正瓣重指派_互斥完备划分与耦合匹配_2026-10-04`（λ=α_s=0.1179 归一 + 60° 正瓣分区）
- **已实现分支（本册交叉核对对象）**：`源码/TUFT-MATH-PROOF-ADD-01_自洽性校验_2026-10-04.py`（分支 4，14 guard 全过）· `源码/TUFT-MATH-PROOF-ADD-01_β衰变手征不对称_数值计算_2026-10-04.py`（分支 3，7 guard 全过）
- **引擎**：`源码/判定_TUFT-MATH-PROOF-ADD-01R_外部审计逐条复算与自我修正_2026-10-04.py`（**纯标准库**，零第三方依赖，0.01s）
- **产物**：`数据/TUFT-MATH-PROOF-ADD-01R_外部审计逐条复算与自我修正_2026-10-04.{json,md}`
- **读数**：**条目 41 —— PASS 17 / MISMATCH 10 / FAIL 3 / BOUNDARY 4 / CORRECTED 6 / INFO 1**；**自检 20 / 20 全过**（退出码 0，可作门禁）
- **第十一轮追加（2026-10-04）**：B03 口径自纠（新增 B03b + guard `b03b_unit_amplitude_linear_is_constant`，条目 40→41、自检 19→20）
- **性质**：元审计 / 整理 **+ 自我修正 + 跨册交叉核对**（对外部审计意见做机器复算；对前置 ADD-01 册、ADD-02 册与**已实现的分支 4/3** 做修正）；**非物理层判决**
- **评级**：C / L1

---

## 〇、一句话结论

**外部审计的核心判断成立，且比本仓 ADD-01 整理册更严格——它推翻了 ADD-01 整理册自己的两处过度结论。但本册复算后给出三处比审计意见更强的结果与两处不同意：**

1. **审计方向正确**：`复相位 ⇒ 宇称破缺 ⇒ 手征不对称` 这条链**三处全断**。本册把它精确定位为「**奇相位下 P 守恒（机器零）**；非奇相位下 P 破缺但 $\Delta_P\equiv 0$（纯相位型）**」——不是「说不清」，而是**可算出守恒判据并双向验证**。
2. **比审计更狠的增量（本册独有）**：
   - **可识别性比审计给的更坏**：审计给 $\mathrm{rank}\,H\le 4$，实际 **rank = 3**（引力行 $G=1.484\times10^{-44}\times$ 强核行 $S$，严格成比例，机器验证）⇒ 4 个观测量只给 3 个独立约束；且 $F_p$ 谱跨 $10^{18}$ ⇒ **双精度下可分辨方向仅 1 个**。
   - **跨册一致性缺陷（审计未涉及）**：在 ADD-02 现行正瓣分区下，$\theta\to-\theta$ 把 $D_\text{Weak}(240°)$ 映到 $D_\text{Strong}(120°)$——**P 把弱相互作用配置映到强相互作用配置**，与相位无关地破坏 P 自反性。
   - **UHECR 证伪阈值定量门槛**：需传播/源/成分/探测器合成系统误差 $\ge 0.2762\times10^{19}$ eV（TUFT 自身 $\sigma$ 的 1.32 倍）才可能把 $5.0\times10^{19}$ 纳入区间 ⇒ 该判据在已声明「剥离传播误差」的区间上逻辑不成立。
3. **不同意审计的两点**：
   - 审计「$\tau\to-\tau\Rightarrow\theta\to-\theta$ 除 atan2 支割线外成立」——**该保留不必要**：6560 点扫描例外 **0 个**（含负 $\kappa$ 轴：$\text{atan2}(0,-x)=+\pi$ 与 $\text{atan2}(-0,-x)=-\pi$ 互为相反数），且 $\cos3\pi=\cos(-3\pi)$ ⇒ 对 $\Omega_R$ 零影响。
   - 审计第 11 节「$\sigma$ 需展示 $\partial\Delta a_e/\partial B_i$ 的条件数」方向正确，但**不能**沿用 ADD-01 的「$\sigma$ 应约 $5.1\times10^{-15}$」作为参照值——那是预设单位 Jacobian 的产物；正确门禁是「放大 $\ge 12.65$ 倍」**且**「$F_p$ 可逆」，而后者已被 C01 判否。

> **一句话裁定**：**采纳审计的诊断、否决 ADD-01 的补丁**。`A_chiral` 必须删除；`PΩ=Ω*` 必须降级为条件式；$\sigma_{\Delta a_e}$ 与 UHECR 区间必须重算；MCMC 在补足 $\ge 3$ 个独立方程前**不得启动**（零空间 3 维，抽样只会得到沿零空间漂移的退化分布）。
>
> **执行状态更正（对审计建议的排序）**：审计建议「先走分支 4 → 再走分支 3 → 最后 MCMC」。核查仓库现状：**分支 4（自洽性校验）与分支 3（β 衰变数值）已经跑完并各有全过的自检**。因此真实状态不是「该做 4 和 3」，而是「**4 和 3 已做，但两者的结论各自带一个未被察觉的判据错误**」——分支 4 的守恒判据用错（F01/F02），分支 3 在错误前提上把参数账从 6 扩到 7（F04）。**排序因此改为：先修判据（§三 E01/E06），再重跑分支 4，最后才谈分支 1（MCMC）；分支 3 须在 C01 解开后重做。**

---

## 一、总审计结论表 · 逐条复算

| 审计意见条目 | 审计判断 | 本册复算 | 判定 | 证据 |
|---|---|---|---|---|
| $\theta=\text{atan2}(\tau,\kappa a)$，$\tau\to-\tau\Rightarrow\theta\to-\theta$ | 🟢 除支割线外成立 | **严格成立，例外 0 个**；支割线保留不必要 | **不同意（更宽）** | A04/A05 |
| $\cos3\theta$ 转回 $(\kappa a,\tau)$ | 🟢 正确 | 5 组样本相对偏差 $3.05\times10^{-16}$ | ✔ 确认 | A06 |
| 量纲分析（$\lambda$ 无量纲） | 🟢 基本正确 | 未反驳 | ✔ 确认 | — |
| 线性 $\phi(\theta)$ 满足 $\phi(-\theta)=-\phi(\theta)$ | 🔴 一般错误 | $\phi(-t)+\phi(t)\equiv-2\phi_0\theta_{W,c}/\Delta\theta_W$（偏差 $2.2\times10^{-16}$） | ✔ 确认并给闭式 | A01 |
| 弱域边界「相位光滑」 | 🔴 错误 | $\lvert e^{i\phi(\theta_b)}-1\rvert=0.3482\ne0$ ⇒ **不连续**；$\phi'$ 从 $0.0117$ 跳到 $0$ ⇒ 非 $C^1$ | ✔ 确认（比审计更强：连连续都不成立） | A08 |
| $\Omega(-\theta)=\Omega^*(\theta)\Rightarrow P$ 破缺 | 🔴 不成立 | **成立并给出充要判据**：$C_L(\theta)=C_R(-\theta)$；奇相位下残差机器零 ⇒ **P 守恒** | ✔ 确认 + **强化**（可算判据） | B01/B02 |
| $P_L,P_R$ 定义 | 🟢 正确 | 未反驳 | ✔ 确认 | — |
| $g_L=e^{i\phi},g_R=e^{-i\phi}\Rightarrow$ 手征不对称 | 🔴 明确错误 | $\lvert A_\text{chiral}\rvert$ 最大 **0.00e+00**（257 点）；$g_R=\overline{g_L}$ 机器零 | ✔ 确认 | A02/A03 |
| 协方差一阶传播公式 | 🟢 正确 | 未反驳 | ✔ 确认 | — |
| $\sigma_\lambda/\lambda\simeq0.0076$ | 🟡 算术可成立 | $0.0009/0.1179=0.007634$ ✔；但依赖 $\lambda=\alpha_s$（ADD-02 的**约定**，非推导） | ✔ 确认 + 标注为「约定继承」 | C02 |
| $\sigma_{\Delta a_e}=0.65\times10^{-13}$ | 🔴 尚无推导 | 需 Jacobian 放大 **12.65 倍**才成立；且 $F_p$ 不可逆 ⇒ 双重阻塞 | ✔ 确认 + **门禁化** | C04/C01 |
| UHECR $\sigma=0.21\times10^{19}$ eV | 🔴 尚无推导 | 区间算术 ✔；证伪阈值需系统误差 $\ge0.2762\times10^{19}$ eV 才可能成立 | ✔ 确认 + **定量门槛** | C05/C06 |
| 「超出 95% 区间即证伪」 | 🟠 表述过强 | 逻辑冲突已定量（见上）；应改似然比 / 后验预测检验 | ✔ 确认 | C06 |
| 三组观测「独立」 | 🔴 当前不正确 | 共享 $\lambda$ ⇒ $\rho=6.967\times10^{-4}\ne0$ | ✔ 确认 | C07 |
| emcee「嵌套采样」 | 🔴 术语错误 | emcee = ensemble MCMC；nested sampling 惯用 dynesty/UltraNest；另存在数据双重计数风险 | ✔ 确认 | C09 |
| 「复相位 ≠ 手征性」 | （第 5 节结论） | 机器证明：相位只能给出 $\theta$ 无关的常相位型 P 破缺，$\Delta_P\equiv0$（B03/B07） | ✔ **确认并形式化** | B03/B04/B07 |

> **A01 的适用边界（诚实标注）**：闭式 $\phi(-t)+\phi(t)\equiv-2\phi_0\theta_{W,c}/\Delta\theta_W$ 只在 **$\theta$ 与 $-\theta$ 同处弱域内**（线性段）成立。来料是**分段定义**（域内线性、域外 $\phi=0$），因此当 $-\theta$ 落在弱域外时实际有 $\phi(-\theta)=0$，此时 $\phi(-\theta)+\phi(\theta)=\phi(\theta)$——这正是 F02 分支 4 实例的情形（$\theta=225°\Rightarrow\phi=-0.125$；$-\theta=135°\Rightarrow\phi=0$）。两种情形都指向同一结论：**$\phi$ 非奇 ⇒ 破缺，且破缺归因是「相位非奇 + 弱域非自反」，与「复相位」无关**。

### 本册不同意 / 需精确化的两点

| 项 | 审计意见 | 本册裁定 |
|---|---|---|
| atan2 支割线 | 「除支割线外成立」 | **例外集为空**：$\text{atan2}(-y,x)=-\text{atan2}(y,x)$ 对一切 $(x,y)\ne(0,0)$ 在双精度下严格成立；唯一残留是 $\theta=+\pi$ 处的**表示跳变**，而 $\cos3\pi=\cos(-3\pi)$ ⇒ 对 $\Omega_R$ 零影响（A04/A05） |
| $\sigma_{\Delta a_e}$ 的「正确答案」 | 「须展示 $\partial\Delta a_e/\partial B_i$ 具有如此大的条件数」 | 方向对，但**不能**默认 $5.1\times10^{-15}$ 是正确答案（ADD-01 已默认之）。$J$ 本身依赖 $\Sigma_p$，而 $\Sigma_p$ 因 C01 不可逆 ⇒ 顺序必须是「先解可识别性 → 再算 $J$ → 再谈 $\sigma$」（C01/C04） |

---

## 二、本册的独立增量（审计未涉及 / 结论更强）

### 2.1 B01/B02 · 宇称守恒的充要判据与显式反例（核心）

在系数层实现审计第 5 节给出的判据（对 $V/A/S/T$ 各 Lorentz 结构，$P$ 交换 $O_L\leftrightarrow O_R$）：

$$\mathcal L_\text{TUFT}=C_L(\theta)\,\mathcal O_L+C_R(\theta)\,\mathcal O_R+\text{h.c.},\qquad
\boxed{\;P\ \text{守恒}\iff C_L(\theta)=C_R(-\theta)\;}$$

代入来料定义 $C_L=|\Omega|e^{+i\phi}$、$C_R=|\Omega|e^{-i\phi}$：

- **奇相位**（$\phi(-\theta)=-\phi(\theta)$，如 bump 窗或 $\theta_{W,c}=0$）：$C_R(-\theta)=|\Omega|e^{-i\phi(-\theta)}=|\Omega|e^{+i\phi(\theta)}=C_L(\theta)$
  ⇒ 残差 **0.00e+00**（5 点机器零）⇒ **P 守恒**。
- **非奇相位**（$\theta_{W,c}\ne0$）：残差 $=2\left|\sin(\phi_0\theta_{W,c}/\Delta\theta_W)\right|=0.4624$，且**与 $\theta$ 无关**（5 点散布 $1.11\times10^{-16}$，与解析预期逐位一致）⇒ P 破缺，但 $\Delta_P$ 恒为 $1.11\times10^{-16}\equiv0$。

> **⚠ B03 的口径限定（第十一轮自纠，B03b）**：上面「与 $\theta$ 无关」只在**三个条件同时成立**时有效 ——
> **①单位幅值**（B03 的 $C_L/C_R$ 用默认 $amp=1$，未乘 $\lvert\lambda\cos3\theta\rvert$）**②全域线性** $\phi(-\theta)$ 仍按 $\phi_0(-\theta-\theta_{W,c})/\Delta\theta$ 求（**来料是分段定义**：域外 $\phi=0$）**③$\theta_{W,c}=20°$**（B03 用例参数，非 ADD-02 的 240°）。
> 三口径机器并列：
>
> | 口径 | 残差 | spread |
> |---|---|---|
> | ①单位幅值 + 全域线性（B03 原口径） | 恒 **0.4624** | **5.6e−17**（常数成立） |
> | ②真实幅值 $\lvert\lambda\cos3\theta\rvert$ + 全域线性 | 随 $\theta$ 变 | 3.86e−02 |
> | ③真实幅值 + **分段定义**（来料原文） | 随 $\theta$ 变 | **1.65e−01** |
>
> ⇒ **B03 的核心裁定不变**（三口径都给出「残差 $\ne0$ ⇒ P 破缺」且 $\Delta_P\equiv0$ ⇒ 纯相位型），
> **但「常数」这一数值表述不适用于来料的分段定义与真实幅值**。分支4 已按口径③重写为
> `parity_residual_nonzero_in_weak_domain`（实测 min=0.0402 / max=0.0883，spread=4.81e−02，恒 $\ne0$）。

**因此来料模型的真实身份是**：

$$\boxed{\ \text{奇相位} \Rightarrow P\ \textbf{守恒}\ ;\qquad
\text{非奇相位} \Rightarrow P\ \textbf{破缺但纯相位型（CKM/CP 型），}\Delta_P\equiv0\ }$$

这与「SM 的 $V-A$ 破坏 $P$」是**两种不同机制**：后者源于左右手 Lorentz 结构不等价（$\mathcal L$ 只含 $W_L$ 流），与复相位无关。**「复相位 ⇒ 手征性」在机器层面被彻底切断**（B03/B04/B07：手征不对称 $\Delta_P=2\varepsilon/(1+\varepsilon^2)$ 只能来自幅值自由度 $\varepsilon$）。

**反例强度**：$\theta=18°$ 处 $\mathrm{Im}\,\Omega=0.0164\ne0$（复场）且 $\Omega(-\theta)=\Omega^*(\theta)$ 逐位成立，**同一模型 $P$ 守恒** ⇒ 直接证伪「$\Omega^*\ne\Omega\Rightarrow P$ 破缺」。

### 2.2 B05 · 整体相位只改率、不改角不对称度

若 $\mathcal M_\text{TUFT}=c\,e^{i\phi}\mathcal M_\text{SM}$，则 $\mathcal M_\text{tot}=(1+ce^{i\phi})\mathcal M_\text{SM}$。注入 $f=1+0.1e^{0.5i}$：

| 量 | 前 | 后 | 结论 |
|---|---|---|---|
| $\lvert f\rvert^2$ | 1 | **1.18552** | 总率 **+18.55%** |
| $A_{GT}=(\lvert M_G\rvert^2-\lvert M_T\rvert^2)/(\lvert M_G\rvert^2+\lvert M_T\rvert^2)$ | 0.0582524272 | **0.0582524272** | **逐位不变**（差 $3.2\times10^{-16}$） |

$\Rightarrow$ 若 TUFT 振幅只是 SM 振幅乘整体相位，$\delta\mathcal A_\text{TUFT}\equiv0$。**$\delta\mathcal A$ 在 Part B.3 中根本未被定义**（D03 列出五项前置条件）。

### 2.3 B06 · 跨册一致性缺陷：P 把弱域映到强域（本册独有）

ADD-02 突破册的现行分区为 $\cos3\theta>0$ 的三个 $60°$ 锥（EM $0°$ / Strong $120°$ / Weak $240°$）。在 $\theta\to-\theta$ 下：

| 扇区 | 中心 | 反演像 | 落入 |
|---|---|---|---|
| $D_\text{EM}$ | $0°$ | $0°$ | 自身 ✔ |
| $D_\text{Strong}$ | $120°$ | $240°$ | $D_\text{Weak}$ ✘ |
| $D_\text{Weak}$ | $240°$ | $120°$ | $D_\text{Strong}$ ✘ |

**这不是「相位造成的手征破缺」，而是分区几何把不同相互作用互相对换。** 后果有两层，必须分开说：

1. **若坚持 $P$ 是理论对称性**：现行分区下 $P$ **根本不是**对称性（它把弱流映成强流），与相位取值无关 ⇒ 「宇称破缺由弱域复相位导出」这句话必须删除；
2. **若 $\Omega$ 只是强度编码的参数化标签、不声称 $P$ 为对称性**：则逻辑自洽，但**宇称破缺成为外部输入**（CKM 相位），D-03 退回未闭合状态。

无论取哪一层，**D-02（弱力方向可证伪）的因果链都不能靠当前分区建立**——你无法在「$P$ 交换强/弱相互作用」的框架里把 $\beta$ 衰变的手征不对称归因于弱相互作用的相位。

### 2.4 C01 · 可识别性比审计给的更坏（rank 3 而非 4，且双精度只剩 1 个方向）

$q=(\alpha_G,\alpha,\alpha_s,\alpha_W)$，$p=(\lambda,\phi_0,B_1..B_4)$，$H=\partial q/\partial p$：

- $\partial\alpha_k/\partial\lambda=\cos3\theta_k$（$\lambda=\alpha_s$ 归一，ADD-02 读数）；$\partial\alpha_k/\partial\phi_0=\mathbf 0$（**整列零** ⇒ $\phi_0$ 完全不可识别）；$\partial\alpha_k/\partial B_i$ 取 ADD-02 敏感度（Weak 0.36、EM 0.84、Strong/G 0）。
- **结构性行相关（机器验证）**：$G=1.484\times10^{-44}\times S$（两行只在 $\lambda$ 列非零，严格成比例）⇒ $\mathrm{rank}(H)=3$，**低于审计给的上界 4**。
- $F_p=H^\mathsf{T}\Sigma_q^{-1}H$：严格零特征值 **3** 个（零空间 3 维）；按相对 $10^{-12}$ 判据数值零 5 个；**双精度下可分辨的非零方向仅 1 个**（谱跨 $\sim10^{18}$ > $10^{16}$）。

$$\boxed{\ \mathrm{rank}\,H=3<6\ \Rightarrow\ F_p^{-1}\ \text{不存在}\ \Rightarrow\ \text{六参数协方差不可由四个耦合得到}\ }$$

补足条件（可执行）：需 $\ge3$ 个**独立**方程/先验（例如：额外的 $\beta$ 衰变观测量 + 至少一个与 $\lambda$ 无关的独立长度/质量比 + 弱扇区几何的直接测量），或对 $B_1..B_4$ 施加单调性/对称性先验降维。**在此之前 MCMC 不得启动**。

### 2.5 C06 · UHECR 证伪阈值的定量门槛

判据取中心值形式 $\lvert E_\text{obs}-E_\text{pred}\rvert\le1.96\,\sigma_\text{comb}$：

$$1.96\,\sigma_\text{comb}\ \ge\ 0.68\times10^{19}\ \text{eV}\ \Rightarrow\ \sigma_\text{comb}\ge0.3469\times10^{19}$$
$$\Rightarrow\ \sigma_\text{prop+src+comp+det}\ \ge\ \sqrt{0.3469^2-0.21^2}\ =\ \boxed{0.2762\times10^{19}\ \text{eV}}\ (=1.32\times\sigma_\text{TUFT})$$

即：**只有当传播/源/成分/探测器合成系统误差达到 TUFT 自身 $\sigma$ 的 1.32 倍时，$5.0\times10^{19}$ 才可能落进预测区间**。既然来料已声明「95% 区间剥离宇宙传播系统误差」，则 $E_\text{cutoff}\ge5.0\times10^{19}$ **不能作为单点证伪条件**。正确形式：

$$-2\ln\frac{L_\text{TUFT,max}}{L_\text{reference,max}}\quad\text{或}\quad \text{posterior predictive }p\text{-value / Bayes factor}$$

（并把传播、源分布、源最大刚度、成分、探测器作为 nuisance parameters 在完整似然中边缘化。）

### 2.6 C07 · 理论相关性使「三重独立交叉检验」不成立

$\Delta a_e$ 与 $\Delta E_\text{GZK}$ 共享 $\lambda$（示意线性模型 $J=\partial y/\partial\lambda=y/\lambda$）：

$$\text{Cov}=J_e\Sigma_p J_\text{GZK}^\mathsf{T}\big|_{\lambda\lambda}=9.51\times10^{1}\ \text{(eV)}^2,\qquad
\boxed{\ \rho=6.967\times10^{-4}\ne0\ }$$

正确表述：**三组数据来源不同、实验误差可近似独立；但 TUFT 预测经共享参数产生理论相关性，必须联合拟合。**（若 $B_i$ 也同时进入两个预测，相关系数进一步上升。）

### 2.7 与已实现分支 4 / 分支 3 的交叉核对（本册独有）

审计意见建议「先做分支 4 → 再做分支 3 → 最后 MCMC」，但核查仓库发现**分支 4 与分支 3 都已经跑完且自检全过**。若不核对，本册会与既有产物脱节。逐条结果：

**分支 4（`TUFT-MATH-PROOF-ADD-01_自洽性校验`，14 guard 全过）——13 条与外部审计一致，1 条判据错误：**

| guard | 与审计关系 | 裁定 |
|---|---|---|
| `chiral_asymmetry_identically_zero` | 与 A02 一致 | ✔ 正面确认 |
| `interference_deltaA_nonzero`（$\delta A\propto-2\lvert\Omega\rvert c_I\sin\phi$） | 与审计第 4 节同向 | ✔ 方向正确，但引入新自由参数 $c_I$（见 F04） |
| `parity_omega_star_needs_odd_phase` | 与 A01 一致 | ✔ 且它已用分段定义算出 $\phi(-225°)=0$（出弱域），比审计更贴近来料原文 |
| **`parity_breaking_holds_POmega_ne_Omega`** | **判据错误** | ✘ 见 F01/F02 |
| `sigma_delta_a_mismatch` | 与 C04 同向 | ⚠ 方向对，但「应为 $5.13\times10^{-15}$」是 ADD-01 的过度主张（见 E02） |
| `alpha_scale_repeat` | 与 C08 一致 | ✔ |
| `gz_interval_arithmetic`（含 SM 基线 $3.64\times10^{19}$ 未交代） | 与 C05 一致且更细 | ✔ 增量 |
| `gz_falsify_window_narrow` | 与 C06 同向 | ⚠ 只说「窄窗口」，C06 给出定量门槛 $0.2762\times10^{19}$ eV |
| `cos3theta_identity` / `omega_dimensionless_under_scaling` / `real_omega_parity_even` / `parity_theta_flips` | — | ✔ 正面（`real_omega_parity_even` 是新增：$\Omega_R$ 是 $\theta$ 的偶函数 ⇒ 实部 $P$-偶） |
| `amplitude_continuous_at_weak_boundary` | — | ✔ 幅值确实连续（连续性来自 $\lambda\cos3\theta$） |
| `phase_discontinuous_at_weak_boundary`（跳变 $0.2500=\phi_0/2$） | 与 A08 一致 | ✔ **该册比外部审计更早发现相位不连续**；A08 把它定量为 $\lvert e^{i\phi}-1\rvert=0.3482$ |

**F01 · 「$P\Omega\ne\Omega$」作为判据零信息量（本册推翻分支 4 的核心 guard）**

相位窗内（$\lvert\theta\rvert<30°$，59 点）扫描：$P\Omega\ne\Omega$ 成立 **98.3%**（唯一例外 $\theta=0$ 相位为零），而作用量守恒判据 $C_L(\theta)=C_R(-\theta)$ **同时成立 100.0%**。

$$\boxed{\ P\Omega\ne\Omega\ \text{是破缺的必要非充分条件：复场自动满足它，而它与「是否守恒」零相关}\ }$$

分支 4 的结论句「但破缺本身（$P\Omega\ne\Omega$）成立」必须改写为作用量判据表述。

**F02 · 分支 4 实例的作用量判据复算（$\theta_{W,c}=240°,\ \Delta\theta_W=60°,\ \phi_0=0.5,\ \theta=225°$）**

$\phi(225°)=-0.1250$（域内），$\phi(-225°)=\phi(135°)=0.0000$（**出弱域，落强域**）⇒ 守恒残差 $\lvert C_L-C_R(-\theta)\rvert=0.0104$（归一化 $0.1249$，与分支 4 的 $\lvert\Omega\rvert=0.7071$ 口径逐位一致）$\ne0$ ⇒ 按作用量判据 **P 破缺**。

**但归因是「相位非奇 + 弱域非 $P$-自反」，不是「复相位」**——这与 B06（弱域反演落强域）同源。分支 4 与外部审计都把破缺归到「复相位/弱域相位」，属**归因错误**。

**分支 3（`TUFT-MATH-PROOF-ADD-01_β衰变手征不对称_数值计算`，7 guard 全过）——结论方向正确，但引入两个新账：**

- **F04 · 参数账恶化**：为写出干涉虚部引入 $c_I$ ⇒ 参数由 **6 → 7**（$\lambda,\phi_0,B_1..B_4,c_I$），观测量仍 4（$+1$ 个 $\beta$ 不对称 $A$）⇒ $\mathrm{rank}\,H\le4<7$，且 $c_I$ **完全无输入来源**（分支 3 自述「$c_I$ 由模型未定」）⇒ C01 的可识别性阻塞**加剧**。分支 3 自己也承认「$\delta A_\text{TUFT}$ 实为 $(c_I,\rho,\phi_0)$ 三维族，非唯一数值预言」。
- **F05 / F06 · 定价性质与口径**：存活门禁 $\rho_\text{crit}=\Delta A/2=5.00\times10^{-4}$，自然 $\rho=0.0261$ ⇒ 倍数 **52.2** ✔ 自洽；$\phi_0$ 存活占比 guard 记 **1.3%** 而该册结论文字写「~2%」⇒ **同册两处口径不一致**。更本质地：β 通道要存活须把 $\rho$ 压低 **52 倍**，这与 ADD-02 的 OPEN-ΩH「耦合层级不被解释、被转移为精细调节」**同构**；且 $g_\text{SM}$ 归一化是新增外锚，违反 $\Omega5$ 单常数约束的同类问题。

---

## 三、自我修正（对前置册的过度结论）

| # | 目标 | 旧说法 | 本册修正 | 证据 |
|---|---|---|---|---|
| **E01** | ADD-01 §3.4 | 「破缺本身（$P\Omega\ne\Omega$）成立」 | 须检验作用量：守恒判据 $C_L(\theta)=C_R(-\theta)$；奇相位 + 共轭 $g_L/g_R$ 下残差机器零 ⇒ **$P$ 守恒**。B.2/B.3 的等式是过度声称 | B01/B02 |
| **E02** | ADD-01 §3.5 | 「$\sigma$ 应约 $5.1\times10^{-15}$」 | 该值预设了单位 Jacobian，**不是唯一正确答案**；正确门禁 = 放大 $\ge12.65$ 倍 **且** $F_p$ 可逆；而 C01 判 $F_p$ 不可逆 ⇒ 两个缺陷耦合，$5.1\times10^{-15}$ 只能当下界参考 | C01/C04 |
| **E03** | ADD-01 §3.4 | 只给了奇偶条件 $\theta_{W,c}=0$ | 补**第二个独立条件**：弱域须 $P$-自反（$\mathcal D_W\Leftrightarrow-\theta\in\mathcal D_W$）。在 ADD-02 现行分区下（弱域中心 $240°$）两条件**同时不成立** | D01/B06 |
| **E04** | ADD-02 §五 | 「D-02/D-03 开放，受 ADD-01 N1 阻塞」 | 升级为**双重阻塞**：① $A_\text{chiral}\equiv0$（无手征强度不对称）② $P$ 破缺判据缺失，且现行分区下 $P$ 交换强/弱瓣（B06） | A02/B06 |
| **E05** | ADD-01 §3.2 | 「跨弱域边界幅值连续、相位光滑 ✔️」 | 线性相位下 $\lvert e^{i\phi(\theta_b)}-1\rvert\ne0$ ⇒ 一般**不连续**；$\phi'$ 跳变 ⇒ 连 $C^1$ 都不成立。改 bump 窗可同时得奇性与 $C^\infty$ | A08/A09 |
| **E06** | 分支 4 guard `parity_breaking_holds_POmega_ne_Omega` + 结论「破缺本身成立」 | 以 $P\Omega\ne\Omega$ 判破缺 | 换判据为 $C_L(\theta)=C_R(-\theta)$；相位窗内 $P\Omega\ne\Omega$ 成立 98.3% 而守恒 100% ⇒ 前者**零信息量**。且分支 4 实例的破缺应归因于「相位非奇 + 弱域非自反」 | F01/F02 |
| **E07** | 分支 3（$\beta$ 衰变数值） | 「$\delta A_\text{TUFT}$ 是 $(c_I,\rho,\phi_0)$ 三维族」被当作诚实的免责声明 | 引入 $c_I$ 使参数 6→7、观测量仍 4 ⇒ 可识别性**恶化**；$c_I$ 无输入来源 ⇒ 该族不是「待定参数」，而是**不可解族**。须在 C01 解开后重做 | F04 |

---

## 四、可采纳的修复（本册验证通过）

### 4.1 D01 · bump 相位窗（审计第 6 节建议 ⇒ 采纳）

$$\mathcal D_W=|\theta|<\Delta,\qquad
w(\theta)=\begin{cases}\exp\!\big[-1/(1-(\theta/\Delta)^2)\big],&|\theta|<\Delta\\ 0,&|\theta|\ge\Delta\end{cases},
\qquad \phi(\theta)=\phi_0\frac{\theta}{\Delta}\frac{w(\theta)}{w(0)}$$

- **奇性**：$w$ 偶 ⇒ $\phi(-\theta)=-\phi(\theta)$，199 点偏差 **0.00e+00**（机器零，非平凡）；
- **$C^\infty$**：$C^\infty$ 由解析速率证——$u=1-(\theta/\Delta)^2\to0^+$ 时 $\lvert dg/du\rvert$ 从 $u=0.5$ 的 $2.7\times10^{-1}$ 单调降至 $u=0.01$ 的 $1.9\times10^{-40}$（衰减 $1.46\times10^{39}$ 倍），高阶同构；
- **诚实边界**：双精度下 $|\theta|>\Delta(1-1.2\times10^{-3})$ 时 $w$ 下溢为 0，故「数值导数为 0」是下溢而非独立证据，本册以解析速率表为准（A09）。

### 4.2 D02 · 正确的闭合形式（审计第 5 节 ⇒ 采纳并机器验证）

$$\mathcal L_\text{TUFT}=C_L(\theta)\mathcal O_L+C_R(\theta)\mathcal O_R+\text{h.c.},\quad
\mathcal O_{L,R}=\bar\psi_{L,R}\Gamma\psi_{L,R},\quad
\Delta_P(\theta)=\frac{\lvert C_L\rvert^2-\lvert C_R(-\theta)\rvert^2}{\lvert C_L\rvert^2+\lvert C_R(-\theta)\rvert^2}$$

- $P$ 交换 $O_L\leftrightarrow O_R$ ⇒ 守恒条件 $C_L(\theta)=C_R(-\theta)$（B01）；
- $\Delta_P\ne0$ **必须**引入幅值自由度 $\varepsilon$：$\lvert C_L\rvert=g(1+\varepsilon)$、$\lvert C_R\rvert=g(1-\varepsilon)$ ⇒ $\Delta_P=2\varepsilon/(1+\varepsilon^2)$，$\varepsilon=0.10$ 时数值 $0.198020$ = 解析 $0.198020$（B04）；此时守恒残差 $\ne0$ ⇒ 显式 $P$ 破缺（D02）。

**代价必须如实登记**：$\varepsilon$ 是**新增自由度**，违反 ADD-02「单常数 $\lambda$」约束（与 OPEN-ΩH 的层级定价同源）⇒ 若采纳，手征不对称与「单常数最简」二者不可兼得。

### 4.3 D03 · $\delta\mathcal A_\text{TUFT}$ 的五项前置

1. 指定 $\mathcal O_\text{TUFT}$ 属 $V/A/S/T$ 哪一种 Lorentz 结构；
2. 存在**两个独立振幅** $\mathcal M_1,\mathcal M_2$；
3. 干涉项 $2\operatorname{Re}(\mathcal M_1^*\mathcal M_2)$ 含 $\cos\phi/\sin\phi$；
4. 固定 SM 参照 $A_\text{SM}$ 口径（核素/中子、$A$ 的定义约定）；
5. 排除整体相位情形（B05 已证明其 $\delta A\equiv0$）。

⇒ 五项未闭合前，$\delta\mathcal A_\text{TUFT}$ **不可计算**。

---

## 五、D 部分状态表更新（对照审计建议）

| 审计项 | 审计建议状态 | **本册更严的裁定** | 依据 |
|---|---|---|---|
| D-02 弱力方向不可证伪 | 🟡 部分推进：已确定 β 衰变为可观测通道，但未给出明确 Lorentz 算符 | **🟡 部分推进（收紧）**：可观测通道已确定，但 (i) $\delta A$ 不可计算（D03 五项前置）；(ii) 现行分区下 $P$ 交换强/弱瓣（B06）⇒ 归因链不成立 | D03/B06 |
| D-03 宇称不守恒概念错配 | 🔴 尚未修复 | **🔴 尚未修复（本册给出可算判据与双向验证）**：$\Omega\to\Omega^*$ 不等价于 $P$ 破缺；且当前 $g_L,g_R$ 给出 $A_\text{chiral}\equiv0$；奇相位下反而 $P$ 守恒 | B01/B02/A02 |
| F-02 可证伪预言数量 = 0 | 🟡 已有 3 个候选可检验量，但数值区间未推导 | **🟡 同一裁定 + 追加第 4 条阻塞**：三条通道的输入端全部受 C01（可识别性）阻塞；UHECR 另受 C06（证伪表述）阻塞 ⇒ 现阶段**没有任何一条可进入 MCMC** | C01/C06 |

---

## 六、分支门禁（**现状已核**——4 与 3 已跑完，故重排为「修判据 → 重跑 → 才谈 MCMC**」）

| 分支 | 仓库现状 | 本册裁定的下一步 |
|---|---|---|
| **4 自洽性校验** | ✅ **已跑**（14 guard 全过，退出码 0） | **须重跑**：14 条中 13 条与审计一致可保留；`parity_breaking_holds_POmega_ne_Omega` 判据错误（E06）必须换成 $C_L(\theta)=C_R(-\theta)$，并补 F01/F02/F03 三条 guard |
| **3 β 衰变数值** | ✅ **已跑**（7 guard 全过，退出码 0） | **须重做**：现版本在 7 参数、$c_I$ 无输入、$\rho$ 需压低 52 倍的前提下给出「非唯一预言」（E07）。重做前置 = ① 删 $A_\text{chiral}$ ② 指定 $\mathcal O_\text{TUFT}$ 结构 ③ 定弱扇区几何 ④ 定 $A_\text{SM}$ 参照 ⑤ 排除整体相位（B05） |
| **1 MCMC** | ❌ 未跑（正确） | **暂缓**：必须先解 C01（补 $\ge3$ 个独立方程/先验使 $F_p$ 可逆，且 $c_I$ 必须有输入来源）；否则抽样沿 $\ge3$ 维零空间漂移，输出漂亮图形但无统计意义。另须修术语（emcee ≠ nested sampling）与数据双重计数 |
| **2 场渲染** | ❌ 未跑（正确） | 最后做，且无判别力（相似度只证两图一致，不证图与实验一致） |
| **0（本册新增）判据层** | — | **真正排在最前**：把「$P$ 破缺判据」写成可执行函数（本册已给出 `parity_residual` / `delta_P`），任何后续增补直接调用复核；这是唯一能防止同类判据错误复发的门禁 |

---

## 七、红线

1. **本册是元审计 / 整理 + 自我修正，不是物理判决**：只核验文本内部一致性、量纲、跨册一致性与统计口径；不替代实验。
2. **不构造新物理**：只给守恒判据、修复模板与前置门禁，不拟合常数、不给新的力/力程公式、不新增预言。
3. **数学自洽 ≠ 物理真实**：即便 B01–B07 全部修好，$\delta\mathcal A_\text{TUFT}$、$\Delta a_e$、$\Delta E_\text{GZK}$ 三条通道仍需真实实验裁决。
4. **审计意见本身也被审计**：A04（支割线）与 C04（$\sigma$ 的「正确答案」）两处本册给出更宽/更严的裁定，**以来源标注区分「审计意见」与「本册裁定」**，不合并陈述。
5. **有效域**：针对 ADD-01 增补 + ADD-02 分区这一组文本。若来料按本册修正后重发，须重跑本引擎（尤其 C01 的 $H$ 结构与 B06 的分区映射）。
6. **数值诚实**：C01 的「双精度可分辨方向 1 个」依赖本册选定的输入误差（$\alpha$ 取 $1.5\times10^{-10}$ 相对、$\alpha_G$ 取 2% 相对）；换误差假设会改变可分辨方向数，但**不改变 $\mathrm{rank}(H)=3<6$ 与 $F_p$ 不可逆的结论**。

---

## 附：复现

```bash
# 纯标准库，零依赖；退出码 0 = 16 条自检全过
cd "04_公共成果/本项目_全维自洽与归一化"
C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe "源码/判定_TUFT-MATH-PROOF-ADD-01R_外部审计逐条复算与自我修正_2026-10-04.py"
# 产物：数据/TUFT-MATH-PROOF-ADD-01R_...{json,md}
```

关键口径：$\lambda=\alpha_s=0.1179$（ADD-02 最大幅值原则）· 弱扇区主算例 $(\theta_{W,c},\Delta\theta_W)=(20°,60°)$、$\phi_0=0.7$ · bump 窗 $\Delta=30°$ · 正瓣分区 $0°/120°/240°$、半宽 $30°$ · $\Delta a_e=2.4\times10^{-13}$、$\sigma=0.65\times10^{-13}$ · $\Delta E=0.68\times10^{19}$ eV、$\sigma=0.21\times10^{19}$ eV、$E_0=5.00\times10^{19}$ eV。

方法论备注（供后续复用）：**「宇称是否破缺」只能在系数/算符层判定，不能在场的复共轭关系上判定**；复共轭配对 $C_R=\overline{C_L}$ 恰恰是 $P$ **守恒**的常见形式。本册把这一判据写成可执行函数（`parity_residual` / `delta_P`），任何后续增补可直接调用复核。
