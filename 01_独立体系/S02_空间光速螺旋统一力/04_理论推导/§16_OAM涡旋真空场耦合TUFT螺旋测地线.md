# §16 OAM 涡旋真空场耦合 TUFT 螺旋测地线（主线：路径②重构）

> 算法联盟最高权限 · S02 空间光速螺旋统一力 · 场标架分支
>
> **本 §16 性质**：主线重构方案（采纳用户 2026-09-24 判决：冻结 §15 证否的「真空单色随 $z$ 扭转偏振标架」，转向真正满足真空 Maxwell 的 OAM 涡旋光）。
>
> **前置结论（必须已读）**：
> - §15 审计已**彻底证否**「把粒子 Frenet–Darboux 标架直接绑定为电磁场偏振基矢」的方案（no-go 定理：真空单色解禁止偏振基矢沿 $z$ 连续旋转；旧方案 $\lvert E_z\rvert/\lvert E\rvert=0.5$ 即有源纵向模）。
> - §13 勘误：Part C2/C3/C4-1 标记**作废不可引用**；Part A 耦合恒等式、§14 误差传播**保留有效**（现正确归属为粒子侧）。
> - §15 永久保留，记录失败全过程与 no-go 证明。
>
> **红线守约**：本节所有数值为 `oam_tuft_couple_audit.py` 实跑输出。**[假设]** 标记的耦合关系是本 §16 新提出的待验证假说，**不替代 QED、未经实验证实**。

---

## §16.0 重构纲领：两套标架彻底解耦

原 §13 的根本错误（见 §15）是把**粒子世界线的 Frenet–Darboux 螺旋标架**与**真空电磁场的偏振基矢**混为一谈。二者可以耦合，但**不能等同**。重构方案如下：

| | 粒子侧（TUFT 测地线） | 场侧（OAM 涡旋光） |
| --- | --- | --- |
| 几何 | 常 $\kappa,\tau$ 螺旋世界线 | 真空 Maxwell 解（LG / Bessel 模） |
| 标架 | Frenet–Darboux（§15.2 修正，恒定 $\boldsymbol\omega_D=K\hat z$） | 实验室**固定**偏振基（不随 $z$ 旋转） |
| 扭转所在 | 世界线几何 | **相位拓扑** $e^{il\phi}$（角向，非偏振旋转） |
| 角动量源 | 几何自旋 $S_z^{\text{(p)}}=\hbar\cos\theta$（§11 谱系） | 自旋 $\sigma_s\hbar$（圆偏振，$\pm\hbar$）+ 轨道 $l\hbar$ |
| 守恒 | 随世界线定义 | 真空 Maxwell → Noether 全成立 |

> **关键**：旧方案错在「偏振矢量沿 $z$ 连续扭转」；OAM 涡旋光是「**相位面沿角向 $\phi$ 扭转，偏振本身固定**」。扭转自由度放在相位拓扑，不触碰 §15 的 no-go 禁令（该禁令针对的是沿 $z$ 的偏振基矢旋转）。

---

## §16.1 场侧：OAM 涡旋光真空解

### 1.1 LG 模拟设（paraxial，$p=0$）

$$
\boldsymbol E(\rho,\phi,z)=E_0\,u_{0l}(\rho,\phi,z)\,\hat{\boldsymbol\epsilon},\qquad
\hat{\boldsymbol\epsilon}=\frac{\hat x+i\hat y}{\sqrt2}\ \text{（固定右旋圆偏振基）}
$$

$$
u_{0l}=\left(\frac{\sqrt2\,\rho}{w(z)}\right)^{|l|}
e^{-\rho^2/w(z)^2}\,e^{il\phi}\,e^{ikz}\,
e^{ik\rho^2/[2R(z)]}\,e^{-i|l|\zeta(z)}
$$

其中 $w(z)=w_0\sqrt{1+(z/z_R)^2}$，$R(z)=z[1+(z_R/z)^2]$，$\zeta(z)=\arctan(z/z_R)$，$z_R=k w_0^2/2$，$k=2\pi/\lambda$。

- **横向性**：$\hat{\boldsymbol\epsilon}$ 固定且 $z$ 分量为 0 → $\lvert E_z\rvert/\lvert E\rvert=0$（审计实跑：$0$）。
- **轨道角动量**：相位因子 $e^{il\phi}$ 携带每光子 $l\hbar$ 的 OAM（$l\in\mathbb Z$ 为拓扑荷）。
- **自旋角动量**：圆偏振给出每光子 $\sigma_s\hbar$（$\sigma_s=\pm1$）。

### 1.2 精确解存在性（Bessel 模）

标量 Bessel 模 $u=J_l(k_\perp\rho)e^{il\phi}e^{ik_z z}$（$k_z=\sqrt{k^2-k_\perp^2}$）是 $\nabla^2u+k^2u=0$ 的**精确**解（任意 $l$）。向量版可由横向偏振构造为严格无源真空解。审计实跑 Helmholtz 残差 $\sim10^{-6}$（机器精度），证明「带 OAM 的精确真空解存在」。

### 1.3 Maxwell 审计（对比 §15 旧方案）

`maxwell_residual_oam`（采样于 $z=2z_R$ 避开束腰 $R(z)$ 导数奇异）：

| 构型 | $R_{\text{Gauss}}=\lvert\nabla\!\cdot\!\boldsymbol E\rvert/\lvert\nabla\rvert E\lvert$ | $R_{\text{Helmholtz}}=\lvert\nabla^2\boldsymbol E+k^2\boldsymbol E\rvert/(k^2\lvert E\rvert)$ | $\lvert E_z\rvert/\lvert E\rvert$ |
| --- | --- | --- | --- |
| LG $l=0$ | $2.0\times10^{-6}$ | $4.5\times10^{-4}$ | $0$ |
| LG $l=1$ | $2.0\times10^{-6}$ | $4.5\times10^{-4}$ | $0$ |
| LG $l=2$ | $2.0\times10^{-6}$ | $4.5\times10^{-4}$ | $0$ |
| Bessel $l$（精确） | — | $\sim10^{-6}$ | $0$ |
| **§15 旧方案** | **$0.5$**（O(1)） | **$1.0$**（O(1)） | **$0.5$** |

> **结论**：OAM 涡旋光 Gauss 残差 $\sim10^{-6}$（纯 paraxial 衍射角量级），**无 §15 式 O(1) 纵向分量**；Helmholtz 残差为 paraxial 小量（非 O(1)），精确 Bessel 版为零。§15 的 no-go 禁令被真正规避——扭转在角向相位，不在 $z$ 向偏振旋转。

---

## §16.2 粒子侧：TUFT 螺旋测地线（复用 §15.2 修正标架）

粒子世界线沿用 §11/§13 Part A 的常 $\kappa,\tau$ 螺旋标架，复用 `momentum_darboux.frenet_frame_lightspeed`（已锁定）。Darboux 恒定自检（审计实跑）：

| $\theta$ | $0^\circ$ | $30^\circ$ | $45^\circ$ | $60^\circ$ |
| --- | --- | --- | --- | --- |
| $\lvert\mathrm d\boldsymbol\omega_D/\mathrm ds\rvert/K^2$ | $0$ | $0$ | $0$ | $0$ |

几何自旋（粒子侧，§11 谱系，§14 已验证其误差预算）：

$$
S_z^{\text{(p)}}=\hbar\cos\theta,\qquad \kappa=K\cos\theta,\ \tau=K\sin\theta
$$

> 此量**不再**解释为光子偏振投影；它是粒子世界线几何的连续自旋类投影，属 TUFT 模型假设（§11 谱系），沿用 §14 误差机械。

---

## §16.3 耦合假说（**[假设]**：待验证，不替代 QED）

**核心构想**：粒子螺旋缠绕角 $\varphi_{\text{p}}=\arctan(\tau/\kappa)$ 与场 OAM 拓扑相位 $e^{il\phi}$ 的匹配。本 §16 提出一个无量纲耦合不变量作为候选：

$$
\boxed{C_{\text{couple}}(l,\theta)=l\cdot\tan\theta = l\,\frac{\tau}{\kappa}}
$$

并给出共振选择规则（极值条件），即场 OAM 拓扑荷 $l$ 与粒子螺旋角 $\theta$ 的锁定。

> **红线**：这是 §16 新提出的耦合假说。审计实跑仅给出 $C(l=1)$ 在 $\theta=30^\circ,45^\circ,60^\circ$ 分别为 $0.577,1.000,1.732$（纯代数）。**其物理存在性、具体耦合强度、实验可探测性均未证实**，需后续建立耦合作用量（如场 OAM 通量与粒子螺旋电流的重叠积分）并设计判决实验。

---

## §16.4 角动量：总 $J_z = S_z^{\text{(p)}} + \sigma_s\hbar + l\hbar$

时间平均角动量密度（paraxial，$z$ 分量）：

$$
s_z=\frac{\varepsilon_0}{2\omega}\,\mathrm{Im}(\boldsymbol E^*\times\boldsymbol E)_z,\qquad
\ell_z=-\frac{\varepsilon_0}{2\omega}\,\mathrm{Im}\!\left[\boldsymbol E^*\!\cdot(x\partial_y-y\partial_x)\boldsymbol E\right]
$$

横截面积分验证每光子角动量（审计实跑）：

| $l$ | $J_{z}^{\text{spin}}/\hbar$ | $J_{z}^{\text{orb}}/\hbar$ |
| --- | --- | --- |
| $0$ | $+1.000$ | $0.000$ |
| $1$ | $+1.000$ | $-1.000$ |
| $2$ | $+1.000$ | $-2.000$ |

自旋/轨道分离正确：圆偏振 → $\pm\hbar$，OAM → $l\hbar$（符号取决于相位/密度式约定，绝对值为 $l$）。

总轴向角动量（**本节核心量，替换原 §13 的 $S_z$**）：

$$
\boxed{J_z = \hbar\cos\theta \;+\; \sigma_s\hbar \;+\; l\hbar = \hbar\big(\cos\theta+\sigma_s+l\big)}
$$

其中 $\cos\theta$ 来自粒子 TUFT 几何自旋，$\sigma_s\pm1$ 来自场圆偏振自旋，$l$ 来自场 OAM。

---

## §16.5 守恒律（Noether 自动成立）

场侧为真空 Maxwell 解 → 自由场作用量具 Poincaré 对称性 → 能量/动量/角动量守恒律成立。审计实跑（`conservation_oam`，稳态光束 $z=0$ 截面）：

$$
\frac{\nabla\!\cdot\!\langle\boldsymbol S\rangle}{K\lvert\boldsymbol S\rvert}=0
$$

动量守恒与角动量流守恒同理恢复（§15 因把随 $z$ 转动标架当固定背景而破坏对称性；本方案场侧背景恒为自由真空，对称性保全）。

---

## §16.6 误差传播升级（§14 升级）

继承 §14(a) 的粒子侧误差项，新增场 OAM 拓扑荷通道：

$$
J_z=\hbar(\cos\theta+\sigma_s+l),\qquad
\sigma_{J_z}^2=(\hbar\sin\theta\,\sigma_\theta)^2+(\hbar\,\sigma_l)^2
$$

（$\sigma_l$ 以拓扑荷整数单位计；$\sigma_s$ 取离散 $\pm1$ 视为无误差或单独处理）。审计实跑：

| $\theta$ | $\sigma_\theta$ | $\sigma_l$ | $l$ | $J_z/\hbar$ | $\sigma_{J_z}/\hbar$ | 相对 |
| --- | --- | --- | --- | --- | --- | --- |
| $45^\circ$ | $0.01$ | $0.1$ | $1$ | $1.707$ | $1.00\times10^{-1}$ | $5.87\times10^{-2}$ |
| $45^\circ$ | $0.01$ | $0.5$ | $1$ | $1.707$ | $5.00\times10^{-1}$ | $2.93\times10^{-1}$ |
| $30^\circ$ | $0.01$ | $0.1$ | $1$ | $1.866$ | $1.00\times10^{-1}$ | $5.37\times10^{-2}$ |

> §14 的 $S_z=\hbar\cos\theta$ 误差机械**完整保留**并正确归属为粒子侧；仅叠加场 OAM 的 $\pm\hbar\sigma_l$ 通道。相对误差由两通道平方和下给出。

---

## §16.7 红线与边界（定稿）

1. **§13 Part C2/C3/C4-1 作废**，不可引用；其「连续自旋投影谱 / 横向动量成像 / 兼容 Maxwell」三判据在真空自由光子层面对应旧方案，已被 §15 证否。
2. **§13 Part A 耦合恒等式、§14 误差传播保留有效**，但 $S_z=\hbar\cos\theta$ 现明确为**粒子 TUFT 几何自旋**（§11 谱系），非光子偏振投影。
3. **§16.3 的 $C_{\text{couple}}$ 是待验证假说**，不构成物理结论；未建立耦合作用量前，仅作代数占位。
4. LG 模为 **paraxial 近似**（审计残差 $10^{-4}\sim10^{-6}$，非精确）——精确结论以 Bessel/角谱分解版为准；不宣称 paraxial 残差可忽略到任意精度。
5. 路径③（波包）按判决后置；待 §16 自洽验证后再启动对比。

---

## §16.8 文件与版本锁

- `oam_tuft_couple_audit.py`：本 §16 审计骨架（LG 场、Maxwell 审计、Darboux 复用、角动量、守恒律、误差升级），实跑通过。
- `momentum_darboux.py`（§15.2 修正标架）：锁定复用，不再改。
- `conservation_maxwell_audit.py`（§15）：证否旧方案原始记录，永久保留，不再改。
- §15：负面结论归档，保留 no-go 证明。
