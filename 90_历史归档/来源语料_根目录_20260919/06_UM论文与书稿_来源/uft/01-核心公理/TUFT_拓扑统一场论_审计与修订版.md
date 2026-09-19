# TUFT 拓扑统一场论｜全维审计与修订版

- 审计对象：用户提交的《TUFT 拓扑统一场论｜完整正确核心公式与理论总集》（原始文本存在转义污染，`The`→`T\(\boldsymbol h\)eory`、"、"被替换为 `\(\mathcal S_\kappa、\mathcal S_\tau\)` 等，本文件已清洗）
- 审计日期：2026-09-15
- 审计方法：sympy 符号推导 + mpmath 50 位数值实跑（脚本 `TUFT_硬伤H1-H8_精算校验.py`，结果 `TUFT_硬伤H1-H8_校验结果.json`）
- 红线（ROOT）：**数学自洽 ≠ 物理实证**；假设不得粉饰为定理；无法闭合的必须显式标注为开放项，不得伪闭合。

---

## 0. 一句话结论

> 三大公理中，公理Ⅱ（Frenet–Serret）与定理1、定理3、定理7 的真空外解/弱场极限**严格成立且量纲自洽**；
> 但原稿第5部分"✅严格证明"清单中有 **4 条站不住脚**（定理2 自旋恒等式、定理5 符号、定理4/5/7 联立、汤川势推导），
> 另存在 **1 处公理级逻辑冲突**（公理Ⅰ 速率 = c 与有静质量粒子不相容）。
> 共记录 **11 项判定**：确认成立 3 项（T1/T3/T7a）、**FAIL 6 项**（H1/H2/H3/H4/H6/H7）、**结构性缺口 OPEN 1 项**（H5）、**零信息量 INFO 1 项**（H8）。

---

## 1. 结论总表

| 编号 | 涉及条目 | 判定 | 严重度 | 一句话 |
|---|---|---|---|---|
| T1 | 定理1 螺旋恒等式 | PASS | — | $\kappa=\frac{R\omega^2}{c^2},\ \tau=\frac{v_\parallel\omega}{c^2},\ \omega=c\sqrt{\kappa^2+\tau^2}$ 符号恒等，无误 |
| T3 | 定理3 拓扑质量 + 普朗克特例 | PASS | — | $m=\frac{\hbar}{c}\sqrt{\kappa^2+\tau^2}$；$\tau=0,\kappa=1/l_{Pl}\Rightarrow m=m_{Pl}$，残差机器零 |
| T7a | 定理7 真空外解 + 弱场极限 | PASS | — | $\beta_1=e^{2GM/c^2r}\Rightarrow g=-GM/r^2\hat r$；$\varphi=-\frac{c^2}{2}\delta\beta_1\Rightarrow\nabla^2\varphi=4\pi G\rho$ |
| **H1** | 公理Ⅰ vs 定理3/6 | **FAIL** | **P0 公理级** | 速率$=c$ ⇒ 类光 ⇒ 固有时为 0，与静质量 $m>0$、$\frac{d}{d\tau}=c\frac{d}{ds}$ 三者互斥 |
| **H2** | 定理5 符号 vs 定理6 | **FAIL** | P0 | $\boldsymbol g=-c^2\kappa\boldsymbol N$ 指向曲率中心**外侧**（排斥），与 $\boldsymbol F=+mc^2\kappa\boldsymbol N$ 差负号，$\boldsymbol F\neq m\boldsymbol g$ |
| **H3** | 定理4 + 定理5 + 定理7 | **FAIL** | P0 | 三式联立要求"指数律 = 幂律"，实测相差 $10^{9}$ 量级；必须三选二 |
| **H4** | 定理2 自旋恒等式 | **FAIL** | P1 | $s=1/2\Rightarrow \mathrm{Lk}=1/\sqrt2\notin\mathbb Z$，与 Călugăreanu–White 冲突；且 $s=\sin^2\theta$ 无推导 |
| **H5** | 曲线量 → 场量 | OPEN | P0 结构性 | $\kappa(s),\tau(s)$ 定义在单条曲线上；$\boldsymbol\tau(\boldsymbol x),\tau_t$ 的提升映射从未定义 |
| **H6** | 3.3 汤川势推导 | **FAIL** | P1 | Helmholtz 解 $\kappa=Ae^{-\mu r}/r$ 与 $V=-g^2e^{-\mu r}/r$ 不能同时满足 $g=-c^2\kappa$（多出 $1/r^2$ 项） |
| **H7** | 定理7 源区 | **FAIL-局部** | P2 | 点源处 $\beta_1\to\infty$ 与 $\delta^3$ 相乘，方程在分布意义下无点源解；真空外部仍 PASS |
| **H8** | 3.1 齐次麦克斯韦 | INFO | P2 | 势表示下恒成立，零信息量，不能算作"复现麦克斯韦"的证据 |

---

## 2. 逐条精算

### T1（PASS）定理1 螺旋恒等式

取 $\boldsymbol r(u)=(R\cos u,\ R\sin u,\ b u)$，$u=\omega t$，$b=v_\parallel/\omega$，则 $R^2+b^2=\dfrac{R^2\omega^2+v_\parallel^2}{\omega^2}=\dfrac{c^2}{\omega^2}$，代入标准结果 $\kappa=\frac{R}{R^2+b^2},\ \tau=\frac{b}{R^2+b^2}$：

$$\kappa=\frac{R\omega^2}{c^2},\qquad \tau=\frac{v_\parallel\omega}{c^2},\qquad \kappa^2+\tau^2=\frac{\omega^2(R^2\omega^2+v_\parallel^2)}{c^4}=\frac{\omega^2}{c^2}$$

脚本以符号方式验证三项残差全为 0（含 $\tan\theta=\kappa/\tau=v_\perp/v_\parallel$）。**结论：定理1 完全正确。**

### T3（PASS）定理3 拓扑质量

$mc^2=\hbar\omega$ 与 $\omega=c\sqrt{\kappa^2+\tau^2}$ 联立直接给出 $m=\frac{\hbar}{c}\sqrt{\kappa^2+\tau^2}$。
取玻色普朗克孤子 $\tau=0,\ \kappa=1/l_{Pl}$：$m=\dfrac{\hbar}{c\,l_{Pl}}=\sqrt{\dfrac{\hbar c}{G}}=m_{Pl}$，数值相对残差 $<10^{-15}$（机器零）。

### T7a（PASS）定理7 外部解与牛顿极限

$\beta_1=e^{2GM/c^2r}\Rightarrow \ln\beta_1=\frac{2GM}{c^2r}$，$\nabla^2\ln\beta_1=0\ (r>0)$，
$$g=\frac{c^2}{2}\nabla\ln\beta_1=\frac{c^2}{2}\left(-\frac{2GM}{c^2r^2}\right)\hat r=-\frac{GM}{r^2}\hat r\quad(\text{吸引，符号正确})$$
弱场 $\delta\beta_1=\frac{2GM}{c^2r}$，令 $\varphi=-\frac{c^2}{2}\delta\beta_1=-\frac{GM}{r}$，则 $\nabla^2\varphi=4\pi G\rho$ 精确复现牛顿泊松方程。$8\pi G/c^2$ 系数正确。
**这一条原稿做对了，可放心列入"成立"清单。**

### H1（FAIL，P0）公理Ⅰ 与有质量粒子的逻辑冲突

- 定理1 曲线满足 $|d\boldsymbol r/dt|=c$；
- 公理Ⅰ 又规定 $ds=c\,dt$。若 $s$ 是**时空世界线弧长**，则该曲线类光，固有时 $d\tau=dt\sqrt{1-v^2/c^2}=0$；
- 但定理3 给出静质量 $m=\hbar\omega/c^2>0$，定理6 使用 $\frac{d}{d\tau}=c\frac{d}{ds}$ 求导，即要求 $d\tau/dt=1$。

数值对照（脚本实跑）：$v=c$ 时 SR 给出 $d\tau/dt=0$，TUFT 给出 $d\tau/dt=1$，比值发散；$v=0.999999c$ 时 $\gamma\approx707$ 且质量需为 0 才自洽。

**修复路径（二选一，尚未裁决）：**
- (a) 把曲线**降格为空间轨迹**，则"世界线/固有时/$\frac{d}{d\tau}=c\frac{d}{ds}$"全部用语需改写为对坐标时求导 $\frac{d}{dt}=c\frac{d}{ds}$，且必须另找静质量的几何起源；
- (b) 保留世界线解释，则公理Ⅰ 需改为 $|v_{\text{total}}|=c$ 只在**内部周期运动**意义上成立，质心速度 $u<c$，并给出 $m=\hbar\omega/c^2$ 与 $u$ 的关系（此时 $\kappa,\tau$ 是内部螺旋的量，与定理7 的外部引力场 $\kappa$ 必须区分——见 H3）。

### H2（FAIL，P0）定理5 符号错误

以玻色孤子（圆轨道，$\theta=90^\circ$）实算：$\boldsymbol r=R(\cos\theta,\sin\theta,0)$，弧长参数下
$$\boldsymbol T=(-\sin\theta,\cos\theta,0),\quad \frac{d\boldsymbol T}{ds}=-\frac{1}{R}(\cos\theta,\sin\theta,0),\quad \kappa=\frac1R,\quad \boldsymbol N=-\hat r\ (\text{指向圆心})$$
脚本验证 $\boldsymbol N\cdot\hat r=-1$。向心（吸引）方向为 $-\hat r=+\boldsymbol N$，故
$$\boldsymbol F=\frac{d\boldsymbol p}{d\tau}=mc^2\kappa\boldsymbol N\ (\text{向心，正确，与定理6 一致})$$
而定理5 的 $\boldsymbol g=-c^2\kappa\boldsymbol N=+c^2\kappa\hat r$ 是**背离曲率中心**的，即排斥，且 $\boldsymbol F\neq m\boldsymbol g$。

**修订（必须）：** $\boxed{\boldsymbol g=+c^2\kappa\,\boldsymbol N}$。

### H3（FAIL，P0）定理4 / 定理5 / 定理7 三重不自洽

三式联立的推导（纯引力取 $\tau=0$）：

1. 由定理7 外解 + 定理5：$c^2\kappa=\dfrac{GM}{r^2}\Rightarrow \kappa(r)=\dfrac{GM}{c^2r^2}$；
2. 代入定理4 定义：$\beta_1^{\text{(def)}}=\dfrac{\kappa^2}{K_0}=\dfrac{G^2M^2}{c^4r^4K_0}$，其中 $K_0\equiv\langle\kappa_0^2+\tau_0^2\rangle$ 应为**常数**；
3. 定理7 要求：$\beta_1^{\text{(sol)}}=\exp\!\left(\dfrac{2GM}{c^2r}\right)$。

$\beta_1^{\text{(def)}}$ 是幂律 $r^{-4}$，$\beta_1^{\text{(sol)}}$ 是指数，二者不可能对所有 $r$ 相等。脚本以地球参数实算：$K_0$ 反解值在 $r=R_E$ 与 $r=2R_E$ 处相差 **16 倍**（正是 $2^4$，即幂律暴露）。

等价的约束检验：把定理4 代入对数律 $\boldsymbol g=\frac{c^2}{2}\nabla\ln\beta_1$ 得
$$\nabla(\kappa^2+\tau^2)=-2\kappa(\kappa^2+\tau^2)\boldsymbol N\quad\xrightarrow{\ \tau=0\ }\quad \nabla\kappa=-\kappa^2\boldsymbol N$$
以 $\kappa=GM/(c^2r^2)$ 实算：$|\nabla\kappa|/\kappa^2=\dfrac{2c^2r}{GM}\approx 2.9\times10^{9}\neq 1$（地球表面）。**这是一条从未论证的额外场方程。**

**修复路径（三选二，或明确区分两种 $\kappa$）：**
- 放弃"$\beta_1$ 由局域 $\kappa^2+\tau^2$ 定义"与"$\beta_1$ 指数解"之一；
- 或引入**两种曲率**：孤子自曲率 $\kappa_{\text{sol}}$（决定质量、自旋）与外场曲率 $\kappa_{\text{field}}$（决定引力加速度、$\beta_1$），并给出二者的耦合关系（目前完全没有）。

### H4（FAIL，P1）定理2 自旋恒等式破坏环绕数整数性

Călugăreanu–White 定理保证 $\mathrm{Lk}=\mathrm{Tw}+\mathrm{Wr}\in\mathbb Z$。原稿取 $s=\sin^2\theta,\ s+\mathrm{Lk}^2=1$：

| 孤子 | $s$ | $\mathrm{Lk}=\sqrt{1-s}$ | 判定 |
|---|---|---|---|
| 玻色 | 1 | 0 | 整数 ✓ |
| 费米 | 1/2 | $\sqrt2/2\approx0.7071$ | **非整数、非半整数** ✗ |
| $s=0$ 类 | 0 | 1 | 但 $\theta=0$ 是直线，$\kappa=\tau=0$，**不闭合**，违反定理9 第1条 ✗ |

脚本判定：$2\mathrm{Lk}=1.4142\notin\mathbb Z$。此外 $s=\sin^2\theta$ 与恒等式 $s+\mathrm{Lk}^2=1$ 本身**均无推导**（未从 $\mathrm{Tw}=\frac{1}{2\pi}\oint\tau\,ds$ 推出），却被列入"✅严格证明"第2条。

**修订：降级为开放命题 O-T2。** 若要保留 $\mathrm{Lk}\in\mathbb Z$，则允许的自旋值只能是 $s=1-n^2\ (n\in\mathbb Z)$，即 $\{1,0,-3,\dots\}$，与物理自旋 $\{0,\frac12,1\}$ 不匹配 ⇒ 该恒等式需整体重构（例如改取 $s$ 为半整数归一、或改为 $\mathrm{Lk}$ 与 $\theta$ 的其他关系）。**本审计不提供替代方案，明确留白。**

### H5（OPEN，P0 结构性）曲线量 → 场量的提升映射缺失

Frenet 的 $\kappa(s),\tau(s)$ 定义在**单条曲线**上；而定理8、3.1、3.2、3.5 全部把它们当成空间场 $\kappa(\boldsymbol x),\boldsymbol\tau(\boldsymbol x)$，还引入时间分量 $\tau_t$ 组成四势 $(\tau_t,\boldsymbol\tau)$。

未定义的关键点：
1. $\tau$ 在原稿中有时是标量模、有时是矢量场 $\boldsymbol\tau$，矢量方向从何而来（Frenet 挠率是带符号标量，不是矢量）；
2. 单条曲线的参数 $s$ 如何变为空间坐标 $\boldsymbol x$；
3. $\tau_t$ 与空间 $\boldsymbol\tau$ 构成洛伦兹四矢的证明（原稿缺四维协变，已列为开放项7，但这是**前提**而非后续）。

**判定：无此映射，第三部分全部悬空。** 建议单列为"公理候选 C1：场化提升公设"，或明确降级为唯象映射。

### H6（FAIL，P1）汤川势推导不自洽

Helmholtz 方程 $\nabla^2\kappa-\mu^2\kappa=-4\pi C_\kappa\delta^{(3)}(\boldsymbol r)$ 的球对称无源解确为 $\kappa=A\frac{e^{-\mu r}}{r}$（脚本验证 $(\nabla^2-\mu^2)\kappa=0$）。但原稿同时要求
$$g_r=-\frac{dV}{dr}=-c^2\kappa(r)$$
代入 $V=-g^2\frac{e^{-\mu r}}{r}$：
$$-\frac{dV}{dr}=-g^2e^{-\mu r}\left(\frac{\mu}{r}+\frac{1}{r^2}\right)\ \neq\ -c^2A\frac{e^{-\mu r}}{r}$$
多出的 $1/r^2$ 项无法由常数吸收：等式要求 $A=\dfrac{g^2(\mu r+1)}{c^2r}$，脚本验证 $\dfrac{dA}{dr}=-\dfrac{g^2}{c^2r^2}\neq0$，即 $A$ 只能是 $r$ 的函数（除非 $g^2=0$，平凡解）。
反过来看：与汤川势相容的曲率 $\kappa_{\text{Yuk}}=\frac{g^2}{c^2}e^{-\mu r}\!\left(\frac{\mu}{r}+\frac{1}{r^2}\right)$ **不是** Helmholtz 方程的解（脚本以 $r=\mu=g^2=c=1$ 数值代入，$(\nabla^2-\mu^2)\kappa_{\text{Yuk}}=1.4715\neq0$；径向解空间只有 $(Ae^{-\mu r}+Be^{\mu r})/r$）。

**修订（择一，均需重新论证）：**
- (a) 保留 Helmholtz 场方程 ⇒ 势应为 $\displaystyle V(r)=-c^2 m A\,E_1(\mu r)$，其中 $E_1(x)=\int_x^\infty \frac{e^{-u}}{u}du$ 为指数积分（由 $\frac{dV}{dr}=c^2\kappa$ 精确积分），**不再是汤川型**；
- (b) 保留汤川势 ⇒ 需另写一条能产生 $e^{-\mu r}(\mu/r+1/r^2)$ 的场方程（不再是 Helmholtz），并解释 $\mu$ 的屏蔽机制。

### H7（FAIL-局部，P2）定理7 在点源处不自洽

注意恒等式 $\nabla^2\beta_1-\frac{(\nabla\beta_1)^2}{\beta_1}=\beta_1\nabla^2\ln\beta_1$。取 $\rho_m=M\delta^3(\boldsymbol r)$，$\ln\beta_1=\frac{2GM}{c^2r}$，则 $\nabla^2\ln\beta_1=-\frac{8\pi GM}{c^2}\delta^3(\boldsymbol r)$，于是
$$\text{LHS}=\beta_1(r)\cdot\left(-\frac{8\pi GM}{c^2}\right)\delta^3(\boldsymbol r),\qquad \text{RHS}=-\frac{8\pi G}{c^2}M\delta^3(\boldsymbol r)$$
两者相差因子 $\beta_1(0)=\infty$。以正则化 $1/r\to1/\sqrt{r^2+\varepsilon^2}$ 实算（地球参数）：$\lg\beta_1(0)$ 在 $\varepsilon=10^{-1},10^{-3},10^{-6},10^{-9}$ 处依次为 $0.0385,\ 3.85,\ 3.85\times10^{3},\ 3.85\times10^{6}$，单调发散，确认无点源解（Yilmaz 型非线性引力理论的已知问题）。真空外部 $r>0$ 两侧恒为 0，该部分仍 PASS。

**修订：** 明确声明"该场方程仅在真空外部（$r>0$）成立，源区需改用有限半径源或边界条件"，并将"点粒子"列入开放项。

### H8（INFO，P2）齐次麦克斯韦零信息量

$\boldsymbol B=k\nabla\times\boldsymbol\tau,\ \boldsymbol E=-k(c\nabla\tau_t+\partial_t\boldsymbol\tau)$ 就是标准势表示 $(\phi,\boldsymbol A)$。脚本代入**任意**函数 $\phi(x,y,z,t),\boldsymbol A(x,y,z,t)$ 实算：$\nabla\cdot\boldsymbol B=0$、$\nabla\times\boldsymbol E+\partial_t\boldsymbol B=0$ 恒等于 0。

**结论：这不能作为"TUFT 复现麦克斯韦"的证据**，它只说明写法是势表示。应改写为开放项（真正的任务是**非齐次**方程与源项 $\mathcal S_\tau$）。

---

## 3. 修订版核心公式集（可直接引用）

> 标记说明：`[成]` 严格成立（已实跑）；`[修]` 本次修订；`[降]` 由"已证明"降级为开放；`[开]` 原本即开放。

### 公理层

| 公理 | 内容 | 状态 |
|---|---|---|
| Ⅰ | $\boldsymbol v_{\text{total}}=\boldsymbol v_\perp+\boldsymbol v_\parallel,\ v_\perp^2+v_\parallel^2=c^2$ | `[修]` 需声明曲线是空间轨迹还是世界线（H1） |
| Ⅱ | Frenet–Serret：$\frac{d\boldsymbol T}{ds}=\kappa\boldsymbol N,\ \frac{d\boldsymbol N}{ds}=-\kappa\boldsymbol T+\tau\boldsymbol B,\ \frac{d\boldsymbol B}{ds}=-\tau\boldsymbol N$ | `[成]` |
| Ⅲ | 可观测物理量 = 曲率/挠率/角频率/拓扑不变量的泛函 | `[开]` 纲领性，非可证伪命题 |

### 定理层

| 定理 | 修订后表述 | 状态 |
|---|---|---|
| 1 | $\kappa=\dfrac{R\omega^2}{c^2},\ \tau=\dfrac{v_\parallel\omega}{c^2},\ \tan\theta=\dfrac{\kappa}{\tau},\ \omega=c\sqrt{\kappa^2+\tau^2}$ | `[成]` |
| 2 | $\mathrm{Lk}=\mathrm{Tw}+\mathrm{Wr},\ \mathrm{Tw}=\dfrac{1}{2\pi}\oint\tau\,ds$ | `[成]` |
| 2b | ~~$s=\sin^2\theta,\ s+\mathrm{Lk}^2=1$~~ | `[降]` 开放 O-T2（H4：破坏 $\mathrm{Lk}\in\mathbb Z$ 且无推导） |
| 3 | $m=\dfrac{\hbar}{c}\sqrt{\kappa^2+\tau^2},\ E=mc^2=\hbar\omega$；$\tau=0,\kappa=1/l_{Pl}\Rightarrow m_{Pl}$ | `[成]` |
| 4 | $\beta_1\equiv\dfrac{\kappa^2+\tau^2}{\langle\kappa_0^2+\tau_0^2\rangle}$ | `[成]` 作为定义；与 5/7 联立见 H3 |
| 5 | $\boxed{\boldsymbol g=+c^2\kappa\,\boldsymbol N}$（原稿负号错误） | `[修]` |
| 6 | $\boldsymbol F=mc^2\kappa\boldsymbol N+mc^2\tau\boldsymbol B$ | `[成]`（与修订后定理5 一致） |
| 7 | $\nabla^2\beta_1-\dfrac{(\nabla\beta_1)^2}{\beta_1}=-\dfrac{8\pi G}{c^2}\rho_m$；真空外解 $\beta_1=e^{2GM/c^2r}$；$\boldsymbol g=\dfrac{c^2}{2}\nabla\ln\beta_1$；弱场 $\nabla^2\delta\beta_1=-\dfrac{8\pi G}{c^2}\rho_m$ | `[成]` 外部/弱场；`[修]` 源区失效声明（H7） |
| 8 | $q\propto\iint_{\mathcal S}\boldsymbol\tau\cdot d\boldsymbol S,\ \rho_e\propto\nabla\cdot\boldsymbol\tau,\ \boldsymbol J_e\propto\partial_t\boldsymbol\tau$ | `[成]` 形式自洽（连续性方程恒成立）；依赖 H5 场化 |
| 9 | 闭合纽结 + $\oint p\,dq=2\pi n\hbar$ + 玻色 $90^\circ$/费米 $45^\circ$ | `[降]` 后两项依赖 O-T2 |

### 形式推论层

| 条目 | 修订后表述 | 状态 |
|---|---|---|
| 3.1 | $\boldsymbol A\propto\boldsymbol\tau,\ \phi\propto c\tau_t,\ \boldsymbol B=k\nabla\times\boldsymbol\tau,\ \boldsymbol E=-k(c\nabla\tau_t+\partial_t\boldsymbol\tau)$ | `[开]` 齐次方程零信息量（H8），非齐次源项未闭合 |
| 3.2 | $T^{\mu\nu}_\tau=\varepsilon_\tau\!\left(F^{\mu\alpha}F^{\nu}_{\ \alpha}-\frac14\eta^{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}\right)$，$c^2=1/(\varepsilon_\tau\mu_\tau)$ | `[开]` 待标定 |
| 3.3 | 汤川：**二选一** —— (a) Helmholtz + $V=-c^2mA\,E_1(\mu r)$；(b) $V=-g^2e^{-\mu r}/r$ + 新场方程 | `[修]` 原推导不自洽（H6） |
| 3.4 | $i\hbar\partial_t\Psi=\hat H_{\text{TUFT}}\Psi,\ \hat H=-\frac{\hbar^2}{2m}\nabla^2+U_\kappa+U_\tau$ | `[开]` 低能形式映射 |
| 3.5 | $\square\kappa=\mathcal S_\kappa,\ \square\boldsymbol\tau=\mathcal S_\tau$ | `[开]` 源项开放 + 依赖 H5 |

---

## 4. 修订后的分级表

### A 级：严格成立（已实跑、量纲自洽）
1. Frenet–Serret 全套微分几何与圆柱螺旋恒等式（定理1）；
2. Călugăreanu–White 分解 $\mathrm{Lk}=\mathrm{Tw}+\mathrm{Wr}$ 与 $\mathrm{Tw}=\frac{1}{2\pi}\oint\tau\,ds$；
3. 拓扑质量 $m=\frac{\hbar}{c}\sqrt{\kappa^2+\tau^2}$、$E=\hbar\omega$、普朗克单位代数复现（定理3）；
4. 修订后引力加速度 $\boldsymbol g=+c^2\kappa\boldsymbol N$ 与统一动力学力分解（定理5/6）；
5. $\beta_1$ 场方程的**真空外部解**与**弱场→牛顿泊松方程**（定理7 部分）；
6. 电荷作为挠率通量的拓扑定义及由此自动成立的电荷守恒（定理8）。

### B 级：降级为开放（原标"已证明"，实为假设/不自洽）
- O-T2：自旋拓扑数 $s=\sin^2\theta$ 与 $s+\mathrm{Lk}^2=1$，玻色/费米孤子分类（H4）；
- O-βκτ：$\beta_1$ 定义与 $\beta_1$ 场方程解、$\boldsymbol g$–$\kappa$ 关系的三者联立（H3）；
- O-SRC：$\beta_1$ 场方程在点源处的有效性（H7）；
- O-YUK：汤川势的推导路径（H6）；
- O-MWH：齐次麦克斯韦"成立"的表述（H8）。

### C 级：结构性缺口（本审计新增，优先级最高）
- **C1 场化提升**：曲线量 $(\kappa(s),\tau(s))\to$ 场量 $(\kappa(\boldsymbol x),\boldsymbol\tau(\boldsymbol x),\tau_t)$ 的映射未定义（H5）；
- **C2 运动学自洽**：公理Ⅰ 的 $|v|=c$ 与有静质量粒子、固有时求导的矛盾（H1）。

### D 级：原本即开放（保留原稿 8 项，并补充）
引力常数 $G$ 绝对值；源项 $\mathcal S_\kappa,\mathcal S_\tau$；耦合常数 $k,\varepsilon_\tau,\mu_\tau,g^2,\mu$；非齐次麦克斯韦与薛定谔的第一性推导；真空基准 $\langle\kappa_0^2+\tau_0^2\rangle$ 的宇宙学起源；弱相互作用拓扑突变动力学；四维协变形式；可判别定量预言与实验验证。**新增：C1、C2、O-T2、O-βκτ、O-SRC、O-YUK、O-MWH。**

---

## 5. 修复优先级

- **P0（不动则体系不能自洽）**：H1（公理Ⅰ 运动学口径）、H2（定理5 符号，一行改动）、H3（$\beta_1$–$\kappa$–$\boldsymbol g$ 三选二）、H5（场化提升公设）
- **P1（影响核心结论）**：H4（自旋/费米子分类重构）、H6（汤川势路径二选一）
- **P2（表述与边界）**：H7（源区声明）、H8（齐次麦克斯韦表述）

---

## 6. 复现方式

```bash
python uft/01-核心公理/TUFT_硬伤H1-H8_精算校验.py
```

输出逐条 `[PASS]/[FAIL]/[OPEN]/[INFO]` 与关键数值，并写出 `TUFT_硬伤H1-H8_校验结果.json`。

本次实跑汇总（2026-09-15）：`PASS=3, FAIL=6, OPEN=1, INFO=1`；其中 PASS 为 T1/T3/T7a，FAIL 为 H1/H2/H3/H4/H6/H7，OPEN 为 H5，INFO 为 H8。
脚本红线：只原样记录计算所得判定，不篡改、不粉饰；未闭合项一律标 OPEN。

---

## 7. 算法联盟正面攻击 · 修复结论（2026-09-15）

> 对 H1–H7 的**修复方案**由算法联盟（G/R/F/T/P/X 六专家，平行会诊 + 红队证伪 + 规则化加权融合）实跑验证。
> 攻击脚本与结果：`TUFT_算法联盟/T01_运动学与引力层修复_正面攻击.py`、`./T02_拓扑与唯象层修复_正面攻击.py`、`./T03_红队复检与联盟融合裁决.py` 及对应 `核验结果.json`；总报告见 `TUFT_算法联盟/TUFT_算法联盟_总报告.md`。
> **红线**：所有判定来自脚本实跑，未闭合项标 OPEN/PARTIAL，不粉饰"方案可行"为"理论已证"。

### 7.1 采纳的修复方案（写入本修订版）

**(A1｜H1 采纳) 共动系双分解** — 公理Ⅰ 改写为「**共动系内**时空元速率模 = c」。内部周期运动在质心静止系以速率 c 走闭合环（类光），质心以 $u<c$ 运动（类时）。实跑：内部半径 $R=\hbar/(mc)$（约化康普顿波长），四速归一 $U^\mu U_\mu=c^2$ 残差 0；共动系内部\|v\|=c 经任意惯性系洛伦兹变换后仍为 c（相对论速度叠加自检通过），与质心 $u<c$ 并存，公理Ⅰ 冲突消解。

**(A2｜H2 采纳) 引力符号** — 定理5 改为
$$\boldsymbol g = +\,c^2\kappa\,\boldsymbol N$$
修订后 $\|g\|=c^2\kappa$ 与定理6、牛顿极限一致（圆轨道 $\boldsymbol N\cdot\hat r=-1$ 即指向曲率中心=吸引）。

**(A3｜H3 有条件采纳) 双 β 分层** — 把"同一 κ"拆开：
$$\beta_1^{\text{(pot)}}\equiv\exp\!\bigl(-\tfrac{2\Phi}{c^2}\bigr),\qquad \kappa_{\text{field}}\equiv\frac{\|\nabla\Phi\|}{c^2},\qquad \beta_1^{\text{(loc)}}\equiv\frac{\kappa^2+\tau^2}{\langle\kappa_0^2+\tau_0^2\rangle}$$
$\beta_1^{\text{(loc)}}$ 保留为"局域激发强度"，**不参与**引力对数律。实跑：外部解 / 弱场 / 路径积分三项残差 0。代价：惯性比概念一分为二（见 O-βbridge）。

**(A4｜H7 有条件采纳) 连续密度源** — 点源处 $\beta_1(0)=\infty$ 致源区失效；改用连续密度源后弱场残差 $=(8\pi G\rho/c^2)(1-\beta_1)$，地球/太阳量级可忽略、中子星中心 $\beta_1(0)=1.677$（+67.7%）⇒ 记为**候选预言 P-C1**（尚非完成预言，需先建强场球对称解）。注意：若改方程为 $\nabla^2\ln\beta_1=-(8\pi G/c^2)\rho$（去掉 β 因子）则退化为严格牛顿，太阳光线偏折预言 $0.876''$ vs 观测 $1.751''$ ⇒ 被证伪，故只能取保留 β 因子的原路径。

**(A5｜H4 有条件采纳) Writhe 补偿** — 单圈闭合螺旋 $\mathrm{Tw}_1=\cos\theta$（已补齐推导）；令
$$\mathrm{Lk}=\cos\theta+\mathrm{Wr}\in\mathbb Z$$
Wr 由孤子非平面几何提供。实跑（Gauss 二重积分，非纽环面曲线）：Wr 随构象连续可调，费米(45°) 的 $\mathrm{Wr}=n-1/\sqrt2$ 在 $n=0$ 时于 $a/R\approx0.287$ 取得。代价：**Wr 构象依赖 ⇒ 修复恢复整数性但无可证伪内容**（记 O-Wr）。

**(A6｜H6 有条件采纳) E1 势替代汤川** — 保留 Helmholtz 方程，势取
$$V(r) = -c^2 m A\,E_1(\mu r),\qquad E_1(x)=\int_x^\infty\frac{e^{-u}}{u}\,du$$
实跑：$(\nabla^2-\mu^2)\kappa=0$ 与 $dV/dr=c^2 m\kappa$ 残差均 0；与汤川势 $V=-g^2e^{-\mu r}/r$ 对比，长程衰减率均 $\to1$（指数衰减一致），短程 $E_1\sim-\ln x$ 对数发散 vs $1/x$ 幂发散可区分 ⇒ 构成 B 级可检验预言（低能核子-核子散射相移比对）。

### 7.2 优化产出（联盟新发现）

**(O-GEO) 孤子几何封闭解** — 由 $(m,\theta)$ 唯一确定全部几何量（符号全恒等，实跑 5 项残差 0）：
$$\kappa=\frac{mc}{\hbar}\sin\theta,\quad \tau=\frac{mc}{\hbar}\cos\theta,\quad \omega=\frac{mc^2}{\hbar},\quad R=\frac{\hbar}{mc}\sin\theta,\quad \text{螺距}=2\pi\frac{\hbar}{mc}\cos\theta$$
（修正原 T01 表格：费米子 $\kappa=\tau=mc/(\sqrt2\,\hbar)$，非 $mc/\hbar$。）

**(O-LAYER) 曲率三重分层** — 为双 β 提供**物理**依据：κ_int（自曲率，定质量）、κ_cm（质心世界线曲率，定动力学）、κ_field（外场曲率，定势）。电子 κ_int=2.59×10¹² m⁻¹，地球表面 κ_field=1.09×10⁻¹⁶ m⁻¹，相差 $10^{28.4}$；中子星表面相差 $10^{17.3}$。原稿把二者当同一 κ 是量级错误。

### 7.3 红队未闭合项 → 新增开放项

| 编号 | 内容 | 裁定 |
|---|---|---|
| O-Wr | H4 修复后 Lk=cosθ+Wr，费米取 n=0 则 Lk=0 与玻色相同，分类信息转嫁至 $(\theta,\mathrm{Wr})$；且 Wr 构象可调 ⇒ 无可证伪内容 | OPEN |
| R2 | E1 势与汤川势均缺 r≲0.5 fm 核力排斥芯 | OPEN |
| O-βbridge | 双 β 分层后"惯性比"被分裂，二者为何分离需机制说明（O-LAYER 量级差可作候选解释，未构成推导） | OPEN |
| O-Sτsrc | 非齐次 Maxwell 源项 $S_\tau$ 动力学系数仍无法纯拓扑定出（原稿开放项 2 未变） | OPEN |
| R5（已规避） | 定理6 的 d/dτ 必须指明对质心世界线（κ=κ_cm），已由 O-LAYER 隔离 | PASS（主文档须写明） |
| P-C1 | 中子星 +67.7% 强场偏离，需先建强场球对称解方可成预言 | OPEN（候选） |

### 7.4 更新后的"✅ 严格证明"清单

**保留 ✅**：定理1；定理3 + 普朗克特例；定理7 真空外解与弱场牛顿极限。

**改为 🚧（已修复但带条件）**：公理Ⅰ 运动学（A1）；定理5 符号（A2）；定理4/5/7 联立（A3 双 β）；定理2 自旋恒等式（A5，附 O-Wr）；汤川势（A6）；定理7 源区（A4，附 P-C1）。

**维持 🚧（未闭合）**：H5 场化提升（候选公设 C1）；H8 齐次 Maxwell 零信息量。
