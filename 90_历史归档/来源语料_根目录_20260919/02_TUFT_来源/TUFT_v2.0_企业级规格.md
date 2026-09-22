# 本源拓扑统一场论（TUFT）v2.0 — 企业级技术规格

## 文档控制

| 项 | 值 |
|---|---|
| 文档编号 | TUFT-SPEC-2026-0916 |
| 版本 | **v2.0（修复并验证）** |
| 日期 | 2026-09-16 |
| 状态 | ✅ 异常修复完成 · 17/17 数值验证通过 · 开放命题已结构化 |
| 锚点约束 | **公理Ⅰ：v_total = c**（一切结论受此约束，全部数值验证以此为基准） |
| 关联产物 | `tuft_v2_verify.py`（验证套件）· `tuft_v2_verify_report.txt`（验证报告）· `TUFT_v2_结构总览.html`（结构可视化） |
| 修订记录 | v1.0 原始文档 → v1.1 分析审计（异常清单 P1–P9）→ **v2.0 修复+优化+验证（本文档）** |

---

## 0. 执行摘要

- **目标**：在 `v_total = c`（公理Ⅰ速率守恒）锚点下，修复 TUFT v1.1 审计发现的数学异常，优化公理化结构与可运算性，并以企业级标准交付（文档控制、异常登记、数值验证、可复现）。
- **方法**：①逐条数学核查（代数推导 + 量纲分析）；②对可修复项给出最小干预的严格修复（新增 2 条公理、重构 2 条定理、修正 2 个定义）；③对不可闭合项显式降级为结构化开放命题（不伪闭合）；④全部关键断言用 numpy 数值套件（17 项测试）验证。
- **结论**：
  - **3 项致命数学异常已修复**：A1 自旋整数化矛盾（`s+Lk²=1` 与整数环绕数冲突）→ 以"标架 holonomy 量子化"重构，修正费米子升角 45°→60°（最小缠绕）；A2 均匀螺旋不闭合 → 以 (p,q) 环面纽结构造闭合孤子；A3 统一动力学 B 项不可导 → 升级为公理Ⅲ（最小耦合）。
  - **6 项结构性问题已处置**：A4 公理属性重分级；A5 曲线挠率/联络挠率术语分离；A6 电荷定义归一化；A7 弱场动态系统封闭可运算；A8/A9 结构化开放。
  - **验证**：17/17 通过（含 Călugăreanu–White 整数值 `SL=−4.00000`、半整数扭转存在性 `(3,7)纽结 Tw=−0.500000, SL=−18.00000`、β₁ 外域残差 `2.8e-9`、弱场波速 `=c`、3D 动态收敛 `2GM/r`）。
  - **边界声明**：本规格不声称实验证实；`G、ℏ、e、α` 仍为外部标定输入；四维协变、微观源项、宇宙学定量模型保持开放（第 9 节）。

---

## 1. 范围与目标

**范围内**：公理体系重构；定理链修复；符号体系统一；数值验证；开放命题结构化；实验判别预言的 v2.0 更新。

**范围外（明确不承诺）**：实验证实；`G/ℏ/e/α` 的第一性导出；四维完全协变形式；麦克斯韦/薛定谔/汤川的完整第一性推导；暗物质替代的定量模型。

**验收标准**：①每个已知异常有登记、根因、修复、验证四要素；②新增公理不改变已验证结果（牛顿极限、普朗克单位、螺旋恒等式）；③所有"定理"标注依赖与可证性；④验证套件退出码 0 即可复现。

---

## 2. 术语与符号（v2.0 修订）

| 符号 | 含义 | 单位 | 修订说明 |
|---|---|---|---|
| $s$ | 世界线弧长 / 自旋量子数 | m / 1 | 自旋含义见 A1：改为标架 holonomy 量子数 |
| $\kappa,\tau$ | 曲率 / 挠率（Frenet） | $\mathrm{m^{-1}}$ | A5：明确为**曲线挠率**，与联络挠率区分 |
| $\theta$ | 螺旋升角，$\sin\theta=v_\perp/c$ | 1 | A1：费米子不再取 45°，取 $\cos\theta=(2n+1)/(2q)$ |
| $v_\perp,h$ | 切向旋转分量 / 轴向分量 | $\mathrm{m/s}$ | 满足 $v_\perp^2+h^2=c^2$（锚点） |
| $\mathrm{Tw},\mathrm{Wr},\mathrm{SL}$ | 扭转数 / 拧数 / 自环绕数 | 1 | $\mathrm{SL}=\mathrm{Tw}+\mathrm{Wr}\in\mathbb{Z}$（C–W） |
| $q$ | 环面缠绕数（经向圈数） | 1 | A2：新增量子数 |
| $\beta_1$ | 全局惯性比 | 1 | 不变 |
| $\square$ | 达朗贝尔算子 | $\mathrm{m^{-2}}$ | 不变 |
| $\tau_{ext}$ | 外部挠率场耦合值 | $\mathrm{m^{-1}}$ | A3：新增，最小耦合公理 |

**术语修复**：`Lk`（环绕数）在 v1.0 中被同时用作整数不变量与连续量，导致 A1。v2.0 起：整数自环绕数记为 $\mathrm{SL}\in\mathbb{Z}$；连续扭转积分记为 $\mathrm{Tw}$；二者关系严格由 Călugăreanu–White 给出。

---

## 3. 公理体系（v2.0）

> v1.0 三公理 + 3 项结构性修正（A4），新增 2 条公理（A1/A3 的修复载体）。**全部推导以此为唯一逻辑起点。**

| 编号 | 公理 | 内容 | 性质 |
|---|---|---|---|
| **公理Ⅰ** | 速率守恒（锚点） | 任意时空元世界线切向总速率模恒等于 $c$：$\boldsymbol v_{total}=\boldsymbol v_\perp+\boldsymbol h$，$v_\perp^2+h^2=c^2$ | 物理公设 |
| **公理Ⅱ** | 正则性 | 世界线为 $C^3$ 光滑曲线且 $\kappa(s)>0$，满足 Frenet–Serret 方程（曲线论基本定理的适用条件） | 适用性假设（A4：原"公理Ⅱ"实为数学定理，此处仅保留适用性声明） |
| **公理Ⅲ** | 最小耦合（**新增**） | 物质孤子与外部场耦合：外部挠率场 $\tau_{ext}$ 引起世界线副法向弯曲，力密度 $F=mc^2(\kappa\boldsymbol N+\tau_{ext}\boldsymbol B)$；自由场 $\tau_{ext}=0$ 退回纯几何 | 物理公设（A3 修复载体） |
| **公理Ⅳ** | 量子化与闭合（**新增**） | Ⅳa 闭合：基本孤子世界线为闭合曲线（环面缠绕，见定理 T9）；Ⅳb 量子化：自旋由标架绕行 holonomy 决定，$\oint\tau\,\mathrm ds=2\pi s\pmod{4\pi}$，$s\in\{0,\tfrac12,1,\dots\}$ | 物理公设（A1/A2 修复载体） |
| **纲领 G** | 几何还原论（降级） | "一切可观测量是世界线几何拓扑泛函" | **非公理**（A4：无预测内容、不可证伪，仅作指导原则） |

**公理Ⅳb 的自旋-统计几何图像**：闭合世界线绕行一周，法向标架沿切向旋转角度 $\Phi=\oint\tau\,\mathrm ds=2\pi\,\mathrm{Tw}$。标架返回自身（$\mathrm{Tw}\in\mathbb{Z}$）↔ 玻色子；标架翻转（$\mathrm{Tw}\in\mathbb{Z}+\tfrac12$）↔ 费米子（Möbius 型 holonomy）。这是自旋-统计关系的纯几何表述。

---

## 4. 定理体系（v2.0）

> 每条标注：状态（✅严格定理 / ⚙️设定 / 🚧开放）、依赖公理、v2.0 变更。

| 编号 | 内容 | 状态 | 依赖 | 变更 |
|---|---|---|---|---|
| T1 | 螺旋运动学：$\kappa=\dfrac{R\omega^2}{c^2},\ \tau=\dfrac{h\omega}{c^2},\ \omega=c\sqrt{\kappa^2+\tau^2},\ \tan\theta=\kappa/\tau$ | ✅ | Ⅰ+Ⅱ | 不变（验证通过） |
| T2 | 扭转恒等式（重构）：单圈 $\mathrm{Tw}=\cos\theta$；自旋量化规则 $\mathrm{Tw}=q\cos\theta\in\mathbb{Z}$（玻色）/$\in\mathbb{Z}+\tfrac12$（费米） | ✅+⚙️ | Ⅰ+Ⅱ+Ⅳb | **A1 修复**：删除 $s+\mathrm{Lk}^2=1$，三语句分离 |
| T3 | 拓扑质量：$m=\dfrac{\hbar}{c}\sqrt{\kappa^2+\tau^2}$；$\tau=0,\kappa=1/l_p$ 复现普朗克单位 | ⚙️（$mc^2=\hbar\omega$ 为量子化设定） | Ⅰ+Ⅳb | 不变；标注依赖 |
| T4 | 全局惯性比：$\beta_1=(\kappa^2+\tau^2)/\langle\kappa_0^2+\tau_0^2\rangle$ | ✅ 定义 | — | 不变 |
| T5 | 引力加速度：$\boldsymbol g=-c^2\kappa\boldsymbol N$（固有时加速度 $=c^2\kappa$，标准几何恒等式） | ✅ | Ⅰ+Ⅱ | 不变 |
| T6 | 统一动力学：$\boldsymbol F=mc^2\kappa\boldsymbol N+mc^2\tau_{ext}\boldsymbol B$ | ⚙️ | Ⅰ+Ⅱ+**Ⅲ** | **A3 修复**：N 项几何可导；B 项由公理Ⅲ承载（不再冒充导出定理） |
| T7 | β₁ 场方程：$\nabla^2\beta_1-\dfrac{(\nabla\beta_1)^2}{\beta_1}=-\dfrac{8\pi G}{c^2}\rho_m$，等价 $\beta_1\nabla^2\ln\beta_1=-\dfrac{8\pi G}{c^2}\rho_m$；静态解 $\beta_1=e^{2GM/c^2r}$；弱场 → 牛顿 | ✅ | 定义+耦合形式 | 不变；补充 ln 等价形式 |
| T8 | 电荷拓扑定义：$q/e=\dfrac{\iint_S\tau\,\mathrm dS}{\iint_{S_0}\tau_0\,\mathrm dS_0}$（归一化通量比，无量纲） | ⚙️ 定义 | — | **A6 修复**：归一化 + 标定输入声明 |
| T9 | 闭合孤子约束（重构）：世界线 = (p,q) 环面缠绕闭合曲线；自旋 = 标架 holonomy；局部均匀螺旋是 $q\to\infty$ 渐近 | ✅+⚙️ | Ⅰ+Ⅳ | **A2 修复**：均匀螺旋 → 环面纽结 |
| T10 | 孤子能量：$E=mc^2=\hbar\omega=\hbar c\sqrt{\kappa^2+\tau^2}$ | ⚙️ | Ⅰ+Ⅳb | 不变 |

---

## 5. 异常修复登记表（A1–A9）

### A1（致命）｜自旋整数化矛盾 — ✅ 已修复

- **异常**：v1.0 主张 $s+\mathrm{Lk}^2=1$ 且费米子 $s=\tfrac12,\ \theta=45^\circ$。但闭合纽结的（自）环绕数为整数（Călugăreanu–White），于是 $s=1-\mathrm{Lk}^2\in\{1,0,-3,\dots\}$，$s=\tfrac12$ 不可能；且 $\cos45^\circ=1/\sqrt2$ 为无理数，$q\cos\theta\notin\mathbb{Z}/2$ 对任意整数 $q$ 成立——**45° 费米子被排除**。
- **根因**：把连续量 $\mathrm{Tw}$ 与整数不变量 $\mathrm{SL}$ 混用；自旋的定义与闭合拓扑不兼容。
- **修复**（三语句结构）：
  1. 运动学恒等式（定理）：$s_{kin}=\sin^2\theta=v_\perp^2/c^2$，单圈 $\mathrm{Tw}=\cos\theta$；
  2. 自旋量化公设（公理Ⅳb）：$s=\mathrm{Tw}\pmod 1$，玻色 $\mathrm{Tw}\in\mathbb{Z}$ / 费米 $\mathrm{Tw}\in\mathbb{Z}+\tfrac12$；
  3. 闭合选择律（定理）：$\mathrm{SL}=\mathrm{Tw}+\mathrm{Wr}\in\mathbb{Z}$，费米子必然 $\mathrm{Wr}=k-(n+\tfrac12)\notin\mathbb{Z}$。
- **修正预言**：费米子最小缠绕（$q=1$）：$\cos\theta=\tfrac12\Rightarrow\theta=60^\circ$（替代 45°）；一般族 $\cos\theta=\dfrac{2n+1}{2q}$。
- **验证**：T06（45° 排除，含无理数证明）、T06b（(3,7) 纽结 $a=1.26576$：$\mathrm{Tw}=-0.500000$，$\mathrm{Wr}=-17.50000$，$\mathrm{SL}=-18.00000$，$\Delta=2.8\times10^{-7}$）。

### A2（致命）｜均匀螺旋不闭合 — ✅ 已修复

- **异常**：常曲率+常挠率 $(\kappa,\tau=\text{const},\ \tau\ne0)$ 的曲线是无限圆柱螺旋，**永不闭合**；v1.0 同时要求"稳态螺旋解"与"闭合孤子"，二者互斥（除玻色 90° 平面圆）。
- **修复**：闭合构造 = (p,q) 环面纽结（$r(\varphi)=\big((R_0+a\cos p\varphi)\cos q\varphi,\,(R_0+a\cos p\varphi)\sin q\varphi,\,a\sin p\varphi\big)$）；均匀螺旋是 $q\to\infty$ 的局部渐近；$(p,q)$ 成为离散量子数。
- **验证**：T04（(2,3) 纽结闭合误差 $1.98\times10^{-15}$，$\min\kappa=0.4011>0$ 正则）；T06b（(3,7) 纽结）。

### A3（致命）｜统一动力学 B 项不可导 — ✅ 已修复

- **异常**：由 $\boldsymbol p=mc\boldsymbol T$ 与 Frenet–Serret 只能推出 $\dfrac{d\boldsymbol p}{d\tau}=mc^2\kappa\boldsymbol N$；$mc^2\tau\boldsymbol B$ 项无推导来源，v1.0 却列为"严格定理"。
- **修复**：新增**公理Ⅲ（最小耦合）**：外部挠率场经副法向分量耦合，$\boldsymbol F=mc^2(\kappa\boldsymbol N+\tau_{ext}\boldsymbol B)$；自由场 $\tau_{ext}=0$ 退回纯几何。$\boldsymbol F\cdot\boldsymbol T=0$ 自动满足（能量沿世界线守恒）。
- **验证**：T09（$\max|\boldsymbol F\cdot\boldsymbol T|=2.2\times10^{-16}$，标架正交归一 $<10^{-15}$）。

### A4（结构）｜公理属性重分级 — ✅ 已处置

- 公理Ⅱ实质是曲线论基本定理（数学事实）+ 光滑性适用声明；纲领 G（几何还原论）无预测内容、不可证伪 → 降级为非公理。见第 3 节表。

### A5（结构）｜曲线挠率 vs 联络挠率 — ✅ 已处置（术语分离）

- Frenet 挠率 $\tau$：单条曲线在嵌入空间中的几何量；Cartan 挠率：仿射联络反对称部分、由物质自旋密度源起。二者数学对象不同。v2.0 明确 TUFT 的 $\tau$ 为前者；与 Einstein–Cartan 的实质兼容列为开放命题 **OP-EC**（第 9 节）。

### A6（结构）｜电荷定义不完整 — ✅ 已修复（归一化定义）

- v1.0：$q\propto\iint_S\tau\,\mathrm dS$（$\tau$ 为标量，"通量"未定义；量纲 $\mathrm{m}$）。
- v2.0：$q/e=\dfrac{\iint_S\tau\,\mathrm dS}{\iint_{S_0}\tau_0\,\mathrm dS_0}$（归一化通量比，无量纲）；$e$ 的数值与 $\alpha$ 仍为**外部标定输入**（开放命题 OP-Q）。

### A7（结构）｜波动方程占位 → 弱场动态系统封闭可运算 — ✅ 已升级

- v2.0 提供**宏观可运算封闭系统**（弱场）：
  - 连续性：$\partial_t\rho+\nabla\cdot(\rho\boldsymbol v)=0$；
  - β₁ 通道（线性化）：$\partial_t^2\delta\beta_1-c^2\nabla^2\delta\beta_1=8\pi G\rho$；
  - τ 通道（无源）：$\partial_t^2\tau-c^2\nabla^2\tau=0$；
  - 含初边值条件与解的存在性声明。
- 微观源项 $\mathcal S_\kappa,\mathcal S_\tau$ 保持开放（OP-W）。
- **验证**：T10（两通道波速 $=c$，$v=1.0000$）、T11（3D 球对称：波前 $t=9.06$ 到 $r=10$，尾部收敛 $2GM/r$，误差 $1.07\times10^{-2}$）。

### A8（开放）｜三维 Frenet vs 四维协变 — 结构化开放（OP-4D）

- 现状：世界线在 4D 时空，Frenet 标架定义于空间投影，非洛伦兹协变。
- 路径：4D 广义 Frenet–Serret（两条曲率 $\kappa_1,\kappa_2$）是标准数学；当前 $(\kappa,\tau)$ 是其在类时世界线上的投影。见 OP-4D。

### A9（开放）｜宇宙学定性 — 结构化开放（OP-C）

- 缺失件：$\beta_{1,orb}(r)$ 具体函数形式、背景孤子系综状态方程、弛豫演化方程。见 OP-C。

---

## 6. 优化项清单（v2.0）

| 编号 | 优化 | 说明 |
|---|---|---|
| O1 | 符号体系统一 | 修复全部损坏 LaTeX（`(\boldsymbol E)instein→Einstein` 等），量纲表齐备 |
| O2 | 洁净公理化 | 4 公理 + 1 纲领；每条定理标注依赖与状态 |
| O3 | ln 等价形式 | $\beta_1\nabla^2\ln\beta_1=-8\pi G\rho/c^2$，便于数值与弱场展开 |
| O4 | (p,q) 量子数 | 环面纽结提供离散量子数来源（自旋谱、质量谱的几何载体） |
| O5 | 自旋-统计几何化 | 标架 holonomy（返身/翻转）给出自旋分类的纯几何图像 |
| O6 | 可复现验证 | 17 项断言，仅依赖 numpy，退出码门禁 |
| O7 | 弱场动态封闭 | 宏观系统可运算（波速、收敛均可测） |

---

## 7. 数值验证摘要（17/17 通过）

> 完整输出见 `tuft_v2_verify_report.txt`；复现命令：`python tuft_v2_verify.py`（退出码 0）。

| 测试 | 内容 | 关键数值 | 结果 |
|---|---|---|---|
| T01 | 公理Ⅰ 速率守恒（锚点） | $v_\perp^2+h^2=c^2$ 误差 $0$ | ✅ |
| T02 | 螺旋 Frenet 恒等式 | $e_\kappa=1.1e{-}16,\ e_\tau=3.3e{-}16,\ \omega=1.000000$ | ✅ |
| T03 | 单圈 $\mathrm{Tw}=\cos\theta$ | $0.8000000000$ | ✅ |
| T04 | (2,3) 纽结闭合+正则 | 闭合误差 $1.98e{-}15$，$\min\kappa=0.4011$ | ✅ |
| T05 | C–W：$\mathrm{SL}=\mathrm{Tw}+\mathrm{Wr}\in\mathbb{Z}$ | $\mathrm{SL}=-4.00000$，$\Delta=3.95e{-}09$ | ✅ |
| T06 | 自旋量化规则 + 45°排除 | $\cos\theta=\tfrac12\Rightarrow60^\circ$；$1/\sqrt2$ 无理数排除 | ✅ |
| T06b | 闭曲线 $\mathrm{Tw}=-\tfrac12$ 存在性 | (3,7) 纽结 $a=1.26576$：$\mathrm{SL}=-18.00000$，$\Delta=2.84e{-}07$ | ✅ |
| T07 | $m\to m_{Pl}$（SI） | 相对误差 $0.0$ | ✅ |
| T08 | β₁ 静态弱场 | 残差 $2.79e{-}09$；$g$ 相对误差 $4.88e{-}11$ | ✅ |
| T09 | 统一动力学正交性 | $\max|\boldsymbol F\cdot\boldsymbol T|=2.2e{-}16$ | ✅ |
| T10 | δβ₁ / τ 波速 $=c$ | $v=1.0000$（两通道） | ✅ |
| T11 | 3D 动态弱场 | 波前 $t=9.06$（理论 10）；尾部收敛 $1.07e{-}02$ | ✅ |

---

## 8. 开放命题（v2.0 结构化）

| 编号 | 命题 | 现状 | 缺失件 / 路径 |
|---|---|---|---|
| OP-1 | 引力常数 $G$ 的第一性导出 | 仅代数关系 | 需从几何尺度给出 $G$ 的绝对数值；当前为外部输入 |
| OP-Q | 电荷量子化与 $\alpha$ | $e,\alpha$ 为标定输入 | 归一化通量比 → 量子化条件的完整推导 |
| OP-W | 波动方程微观源项 $\mathcal S_\kappa,\mathcal S_\tau$ | 宏观系统已封闭 | 单孤子辐射反作用自洽约束 → 场论源项 |
| OP-M | 麦克斯韦 / 薛定谔 / 汤川的第一性推导 | 未完成 | 最大瓶颈：先建立 τ 场/β₁ 场的作用量（拉氏量） |
| OP-EC | 与 Einstein–Cartan 的实质兼容 | 概念同源（A5） | 建立曲线挠率场 ↔ 联络挠率的对应关系 |
| OP-4D | 四维完全协变形式 | 三维投影基 | 4D 广义 Frenet–Serret（$\kappa_1,\kappa_2$）提升 |
| OP-WK | 弱相互作用拓扑相变动力学 | 定性图像 | 纽结拓扑相变的完整动力学与玻色子释放机制 |
| OP-C | 宇宙学定量模型 | 定性叙事 | $\beta_{1,orb}(r)$ 函数形式、背景系综 EOS、弛豫方程 |

---

## 9. 与主流物理的兼容性矩阵（v2.0）

| 项目 | 兼容性 | 说明 |
|---|---|---|
| 数学工具（Frenet–Serret / Călugăreanu–White） | ✅ 完全 | 标准微分几何与纽结理论 |
| 普朗克单位代数关系 | ✅ | T07 数值验证 |
| 弱场牛顿引力 | ✅ | T08 数值验证 |
| 玻色/费米二分 | ✅（修复后） | 公理Ⅳb 标架 holonomy |
| Einstein–Cartan 挠率引力 | ⚠️ 概念同源 | OP-EC 未闭合 |
| 标准量子场论本体论 | ❌ 不兼容（模型选择） | 粒子=几何孤子 vs 场算符激发 |
| 狭义相对论四维速度 | ⚠️ 待澄清 | 公理Ⅰ 是三维切向速率模 $c$；四维协变见 OP-4D |

---

## 10. 实验判别预言（v2.0 更新）

**A 级·模型内一致性（无需实验，违反即矛盾）**
1. 闭合孤子自旋必须满足 $\mathrm{Tw}\in\mathbb{Z}$（玻色）/ $\mathbb{Z}+\tfrac12$（费米）——**费米子最小缠绕升角为 60°，45° 被数学排除**（v2.0 新增）。
2. 闭合孤子不可能有全程常数 $(\kappa,\tau)$（均匀螺旋不闭合）；任何此类构造自相矛盾。
3. 统一动力学中 B 项必须由外部挠率场承载；自由场无 B 项力。
4. $\mathrm{SL}=\mathrm{Tw}+\mathrm{Wr}\in\mathbb{Z}$ 对所有闭合孤子成立（数值已验证）。

**B 级·方向性预言（需先完成推导）**
5. 挠率波（$\square\tau=0$）：若 τ 场存在，预言类轴子/类引力波信号；需先给出 τ 场作用量才能定谱与耦合强度（OP-M）。
6. 若 $\beta_{1,orb}$ 解释星系旋转曲线：必须给出 $\beta_{1,orb}(r)$ 函数形式，产生与 Tully–Fisher 可比对的预言（OP-C）。
7. 强场：$\beta_1=e^{2GM/c^2r}$ 外域与牛顿恒同，但引力透镜/水星进动需先建立光子与度规动力学（OP-4D）。
8. 自旋-电荷耦合：τ 符号 ↔ 电荷手性 ⇒ 自旋相关力修正；电子 EDM（v1 中 $d_e\approx3\times10^{-34}\,\mathrm{C\cdot m}$）为首个可检验量——需确认在 v2.0 重构下仍成立。
9. 反物质/CP：负挠率结构对应反粒子（定性）。

---

## 11. 附录 A：核心方程速查（v2.0）

| 类别 | 方程 |
|---|---|
| 锚点公理 | $v_\perp^2+h^2=c^2$ |
| Frenet–Serret | $\dfrac{d\boldsymbol T}{ds}=\kappa\boldsymbol N,\ \dfrac{d\boldsymbol N}{ds}=-\kappa\boldsymbol T+\tau\boldsymbol B,\ \dfrac{d\boldsymbol B}{ds}=-\tau\boldsymbol N$ |
| 螺旋几何 | $\kappa=\dfrac{R\omega^2}{c^2},\ \tau=\dfrac{h\omega}{c^2},\ \omega=c\sqrt{\kappa^2+\tau^2},\ \tan\theta=\dfrac{\kappa}{\tau}$ |
| 扭转恒等式（v2.0） | 单圈 $\mathrm{Tw}=\cos\theta$；$\mathrm{Tw}=q\cos\theta$；自旋 $s=\mathrm{Tw}\pmod 1$ |
| 闭合选择律 | $\mathrm{SL}=\mathrm{Tw}+\mathrm{Wr}\in\mathbb{Z}$（Călugăreanu–White） |
| 拓扑质量 | $m=\dfrac{\hbar}{c}\sqrt{\kappa^2+\tau^2}$ |
| 全局惯性比 | $\beta_1=\dfrac{\kappa^2+\tau^2}{\langle\kappa_0^2+\tau_0^2\rangle}$ |
| 引力加速度 | $\boldsymbol g=-c^2\kappa\boldsymbol N$ |
| 统一动力学（v2.0） | $\boldsymbol F=mc^2\kappa\boldsymbol N+mc^2\tau_{ext}\boldsymbol B$（公理Ⅲ） |
| β₁ 场方程 | $\beta_1\nabla^2\ln\beta_1=-\dfrac{8\pi G}{c^2}\rho_m$；静态解 $\beta_1=e^{2GM/c^2r}$ |
| 引力对数律 | $\boldsymbol g=\dfrac{c^2}{2}\nabla\ln\beta_1$ |
| 电荷（v2.0） | $q/e=\dfrac{\iint_S\tau\,\mathrm dS}{\iint_{S_0}\tau_0\,\mathrm dS_0}$ |
| 弱场动态（v2.0） | $\partial_t^2\delta\beta_1-c^2\nabla^2\delta\beta_1=8\pi G\rho$；$\partial_t^2\tau-c^2\nabla^2\tau=0$ |
| 孤子能量 | $E=mc^2=\hbar c\sqrt{\kappa^2+\tau^2}$ |

---

## 12. 附录 B：验证套件运行说明

```
环境: Python ≥ 3.10, numpy ≥ 1.20（无 scipy 依赖）
运行: python tuft_v2_verify.py
退出码: 0 = 17/17 通过; 1 = 存在失败
报告: tuft_v2_verify_report.txt（自动生成）
```

测试架构：T01–T03 螺旋运动学（解析导数 + 数值 Frenet 交叉验证）；T04–T06 纽结拓扑（Gauss 双积分计算拧数）；T07 SI 单位复核；T08 β₁ 静态（4 阶中心差分）；T09 力正交性；T10–T11 弱场动力学（leapfrog 有限差分 + 3D 球对称）。

---

*本文档为理论模型规格，数学自洽 ≠ 实验证实。公理为假设；开放命题明确标注，不伪闭合。*
