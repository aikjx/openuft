# TUFT 复能动张量协变守恒（EC 含挠率联络）· 全维审订

> 配套机器验证：`tuft_复能动张量协变守恒_EC含挠率.py`（纯标准库，seed=20260930，N_FIELD=12 / N_REG=24）。
> 机器读数：`PASS = 8 · FAIL = 12 · BOUNDARY = 5 · INFO = 3`，见 `tuft_复能动张量协变守恒_report.txt`。
> 红线：数学自洽 ≠ 实验证实。负结论为**边界 / 缺陷判定**，不是对 TUFT 框架的证伪宣告；本册不改任何 claims 状态、不提升任何 L3 计数。

---

## 0. 审订对象与方法

审订对象：来稿《TUFT｜复能动张量协变守恒：完整张量指标推导（EC 含挠率联络）》。

审订方法（为何可纯数值判定）：第一 / 第二 Bianchi 恒等式是"联络值 + 联络一、二阶导数"在某一点的**局部**恒等式。因此只需在一点任意给定 $\Gamma^\lambda{}_{\mu\nu}$、$\partial_\rho\Gamma^\lambda{}_{\mu\nu}$、$\partial_\rho\partial_\sigma\Gamma^\lambda{}_{\mu\nu}$（满足度规相容与导数对称性约束），即可纯数值判定任一候选恒等式是否成立——**无需解场方程、无需给定物质模型**。这是本册最硬的一条判据来源。

---

## 1. 定义层（§1，3 PASS）

挠率反对称 $T^\lambda{}_{\mu\nu}=-T^\lambda{}_{\nu\mu}$、曲率对末两指标反对称 $R^\rho{}_{\sigma[\mu\nu]}$、度规相容 $\nabla_\mu g_{\nu\sigma}=0$ 三项定义自检全部机器零（最大偏差 $0.00\times10^{0}$）。

---

## 2. Bianchi 层（§2）

| 检验项 | 结论 | 残差 |
|---|---|---|
| 第一 Bianchi（三指标全反对称 + 挠率修正） | **PASS（钉死）** | $2.12\times10^{-16}$ |
| 来稿写法（只对 $[\mu\nu]$ 反对称） | FAIL | $1.76\times10^{0}$ |
| 第二 Bianchi（EC 含挠率修正） | BOUNDARY | $5.41\times10^{-1}$ |

**关键发现 1（第一 Bianchi 正确形式）**：在本约定下唯一确定的成立形式为

$$R^\rho{}_{[\sigma\mu\nu]} = -\,\nabla_{[\sigma}T^\rho{}_{\mu\nu]} + T^\alpha{}_{[\sigma\mu}T^\rho{}_{\nu]\alpha},$$

相对残差 $2.12\times10^{-16}$（12 组场）。而来稿只对 $[\mu\nu]$ 反对称的写法，因曲率已对 $[\mu\nu]$ 反对称而退化为 $R^\rho{}_{\sigma\mu\nu}$ 本身，**不是恒等式**（残差 $1.76\times10^{0}$）。

**关键发现 2（第二 Bianchi 未闭合）**：候选挠率项 $\nabla_{[\lambda}R^\rho{}_{|\sigma|\mu\nu]}=s\cdot(\text{T·R 缩并})$ 的**候选族扫描**（4 种标准指标缩并 × $\pm1$ 符号）最小相对残差仍为 $5.41\times10^{-1}$，**未闭合**。即：第一 Bianchi 的挠率项在本约定下唯一确定，而第二 Bianchi 还依赖曲率定义约定，本册**不硬写**其"正确形式"。

---

## 3. 缩并层（§3）—— 本轮深化重点

来稿命题方向（EC 下 $\nabla^\mu G_{\mu\nu}\neq 0$）**正确**：实测 $|D|\in[1.01,10.4]$，且随挠率标度满足 $D(\varepsilon)\propto\varepsilon^{1.83}$（挠率二次项，与 $T\cdot R$ / $\nabla T$ 结构一致，PASS）。

但来稿给出的挠率源项形式

$$U_\nu = T^\alpha{}_{\alpha\beta}R^\beta{}_\nu - T^\alpha{}_{\nu\beta}R^\beta{}_\alpha$$

与实测 $D_\nu$ 相对偏差 $1.12\times10^{0}$，**指标排列 / 符号不成立**（FAIL），不能作为 EC 缩并 Bianchi。

**关键发现 3（残差结构的决定性识别）**：用随机联络场（24 组）做候选基最小二乘回归 $D_\nu\approx\sum_k a_k c_k$，分两级对照：

| 候选基组 | 相对残差 | 系数 |
|---|---|---|
| 纯 $T\cdot R$ 代数基（$c_1$–$c_5$） | $8.30\times10^{-1}$ | $[+1.1679,+0.1377,-0.1377,+0.1445,+0.0738]$ |
| $+$ $\nabla T$ 协变导数基（$c_6$–$c_8$） | **$8.27\times10^{-1}$（几乎未降）** | 8 项 |

补入 $\nabla T$ 型基后残差**几乎不降**（$8.30\to8.27\times10^{-1}$）。这说明真实的 EC 缩并残差**无法仅由挠率及其一阶协变导数（$T\cdot R+\nabla T$）的局部结构张成**，还含 $\mathrm{d}\mathrm{d}\Gamma\cdot\Gamma$ 等**联络二阶导数的耦合项**。

其几何含义：要写出 $\nabla^\mu G_{\mu\nu}$ 的挠率**闭式**，必须借助 Bianchi 恒等式把 $\mathrm{d}\mathrm{d}\Gamma$ 项**重组合掉**——这也正是「守恒命题 $\Leftrightarrow$ 残差置零」的几何根源。来稿「只用挠率-曲率代数约束即可归零残差」的思路在结构上**完全不成立**。

---

## 4. 复推广层（§4）

| 检验项 | 结论 |
|---|---|
| "复解析延拓"术语 | BOUNDARY：$\mathfrak{R}=R+i\mathcal{S}$ 是两实张量的**复线性组合**，恒等式的复推广靠复线性（实部、虚部各自成立），不存在"解析延拓"这一步 |
| 虚部张量 $\mathcal{S}^\rho{}_{\sigma\mu\nu}$ 未定义 | FAIL：来稿未给出 $\mathcal{S}$ 构造；若直接搬挠率（$[\mathrm{L}^{-1}]$）与 $R$（$[\mathrm{L}^{-2}]$）不同量纲，复和非法 |
| 守恒命题的逻辑性质 | BOUNDARY：场方程下 $\nabla^\mu\mathfrak{M}_{\mu\nu}=0\Leftrightarrow$ 残差 $=0$ 严格等价 ⇒ 把残差置零是**公设化约束**（降自由度），非从 Bianchi 推出的守恒律 |
| 低能极限 | BOUNDARY：$T\to0$ 时残差自动 $\to0$，实部单独已守恒 ⇒ "靠虚部抵消才守恒"机制在低能可省，唯一作用区是高能处的一条约束 |

---

## 5. 量纲层（§5，自建 SI 指数向量）

| 检验项 | 结论 | 说明 |
|---|---|---|
| $\mathfrak{R}\equiv g^{\mu\nu}\mathfrak{R}_{\mu\nu}=\kappa+i\tau$ | FAIL | 左 $[\mathrm{L}^{-2}]$ vs 右 $[\mathrm{L}^{-1}]$，差一长度因子 |
| $\omega_I=c\,T_B$ | **PASS** | $c\,T_B=[\mathrm{T}^{-1}]$，量纲合法 |
| $\omega_R=c\,R_B$ | FAIL | $c\,R_B=[\mathrm{L}^{-1}\mathrm{T}^{-1}]$，非频率（须 $\omega_R\sim c\sqrt{R_B}$ 或 $c/\ell$） |
| 复 EC 场方程 | FAIL | 复和合法要求 $\mathcal{S}_{\mu\nu}$ 与 $R_{\mu\nu}$ 同为 $[\mathrm{L}^{-2}]$，须由挠率构造曲率型量（$\nabla T$ 或 $T\cdot T$），来稿未给出 |

量纲合法的**唯一一条**是 $\omega_I=c\,T_B$。

---

## 6. 物理对接层（§6）

| 检验项 | 结论 | 残差 / 依据 |
|---|---|---|
| 来稿球对称挠率分量 $T^r{}_{t\theta},T^r{}_{t\varphi}$ | FAIL | SO(3) 协变性残差 $7.60\times10^{-1}$（裸 $\theta/\varphi$ 指标不具球对称性） |
| 对照：标准球对称矢量挠率 $n^\lambda(t_\mu n_\nu-n_\mu t_\nu)$ | PASS | $2.81\times10^{-16}$ ⇒ 真正的球对称挠率只允许由 $n^\lambda,t_\mu,g_{\mu\nu}$ 构造 |
| $\alpha^{-1}=2\pi/\theta$ 与 $r=\tau/\kappa=\tan\theta$ | FAIL | $\theta=2\pi\alpha\Rightarrow r=0.045883$；$\alpha=\tau/\kappa\Rightarrow0.007297$；$\alpha=\kappa/\tau\Rightarrow137.036$ ⇒ 三式互不自洽 |
| 缺口定理 N（$\beta_r$ 有限跳变） | FAIL | 与既有读数 `tuft_beta_running_缺口_定理N实例化.py` 冲突：$g=\kappa/\tau$ 常 $\Rightarrow\beta\equiv0\Rightarrow\Delta\beta_r=0$（属冲突登记，非本次新算） |
| CMB 双谱通道 $\Delta B_\zeta$ | BOUNDARY | 若 $\mathrm{d}r/\mathrm{d}t\equiv0$ 则阶跃 $H$ 无源 $\Rightarrow$ 零信号 |
| 黑洞 QNM 通道 | FAIL | OPEN_v3：墙在 $r_s=2.05M$ 被 LIGO 联合排除 $\chi^2=33.00\,(\mathrm{df}=2),\,p\approx5.74\sigma$；OPEN_v4：TUFT 三尺度锚与所需 $2.05M$ 差 $26.0{\sim}26.5$ / $78.2{\sim}79.8$ 量级 |

---

## 7. 记号冲突层（§7，INFO）

来稿中符号 $\mathfrak{T}$ 三义（挠率迹 $\mathfrak{T}^\alpha{}_{\alpha\beta}$、复能动张量 $\mathfrak{T}_{\mu\nu}$、复曲率虚部 $\mathfrak{T}^{(\mathrm{geo})}_{\mu\nu}$）共用一个符号；文稿已改名：挠率 $T^\lambda{}_{\mu\nu}$、复曲率虚部 $\mathcal{S}^\rho{}_{\sigma\mu\nu}$、复能动张量 $\mathfrak{M}_{\mu\nu}$。

---

## 8. 计数与红线

```
PASS = 8   FAIL = 12   BOUNDARY = 5   INFO = 3
```

核心结论：

1. EC 下 $\nabla^\mu G_{\mu\nu}\neq0$ 的**方向判断正确**（残差 $\propto$ 挠率二次），但来稿引用的「第一 Bianchi」实为第二 Bianchi（微分 Bianchi），且其两指标写法不是恒等式；来稿挠率源项与实测残差相对偏差 $1.12\times10^{0}$，不成立。
2. 守恒命题在场方程下与「残差置零」**严格等价** ⇒ 是公设化约束（降自由度），非守恒定理；且**纯 $T\cdot R$ 代数型约束不足以闭合残差**（纯 $T\cdot R$ 回归残差 $8.30\times10^{-1}$；补 $\nabla T$ 协变导数基后仍 $8.27\times10^{-1}$，还含 $\mathrm{d}\mathrm{d}\Gamma\cdot\Gamma$ 耦合项）。
3. 量纲三处非法：$\mathfrak{R}=\kappa+i\tau$（$[\mathrm{L}^{-2}]$ vs $[\mathrm{L}^{-1}]$）、$\omega_R=cR_B$（非频率）、复场方程虚部未定；仅 $\omega_I=cT_B$ 合法。
4. 来稿球对称挠率分量不满足 SO(3) 协变（残差 $7.60\times10^{-1}$）；$\alpha$ 三式内部冲突。
5. 两个「下一步」通道按本仓既有读数均为零信号 / 已关闭：CMB（$\beta\equiv0$ ⇒ 无跳变源）、QNM（$5.74\sigma$ 排除 + 尺度锚差 $26{\sim}78$ 量级）。

**红线**：数学自洽 ≠ 实验证实。本册只做几何 / 量纲 / 一致性审计，不主张 TUFT 物理真实性，负结论为边界判定而非证伪宣告。

---

## 9. 开放项登记（O 项）

| 编号 | 内容 | 状态 |
|---|---|---|
| O-EC-BIANCHI2 | EC 第二 Bianchi 的正确挠率项形式在本约定下未钉死（4 缩并 × $\pm1$ 符号族最小残差 $5.41\times10^{-1}$），须按所用曲率 / 挠率符号约定另行标定 | 开放 |
| O-EC-DIVG | $\nabla^\mu G_{\mu\nu}$ 的挠率**闭式**（含 $\mathrm{d}\mathrm{d}\Gamma$ 项重组合）未给出；本册仅证明「纯 $T\cdot R$ 局部结构不足」 | 开放 |
| O-CONSERVE | 守恒命题的物理内容 = 一条高能约束（非定理），其可检验性未定 | 开放 |

> 本册与既有读数的一致性：它与 `tuft_beta_running_缺口_定理N实例化.py`（$\beta\equiv0$）、`tuft_EDM_实验对接_OPEN6.py`、ringdown `OPEN_v3/v4`（QNM 通道关闭）共同构成 TUFT 的可检验边界画像——**四个实验窗口（$g{-}2$、EDM、$\beta$ 跑动、ringdown）均已关闭**，本册新增的贡献是把「复能动张量协变守恒」这一来稿的核心命题，从"代数约束可闭合"降为"局部结构不充分、需 $\mathrm{d}\mathrm{d}\Gamma$ 重组合"。
