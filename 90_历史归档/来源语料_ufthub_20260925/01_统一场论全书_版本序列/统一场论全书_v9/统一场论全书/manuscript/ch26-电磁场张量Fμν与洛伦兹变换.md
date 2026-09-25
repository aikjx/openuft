# 第二十六章 电磁场张量 $F_{\mu\nu}$ 与洛伦兹变换

## 一、为何要把电场与磁场打包成张量

第四章在三维语言中把麦克斯韦方程写成 $\nabla\cdot\vec E=0$、$\nabla\cdot\vec B=0$、$\nabla\times\vec E=-\partial_t\vec B$、$\nabla\times\vec B=\mu_0\varepsilon_0\partial_t\vec E$ 四个式子。那一套写法在静电静磁问题中足够好用，但一旦进入狭义相对论的语境，就暴露出两个结构性缺陷。其一，四个方程地位并不对称：两个散度方程与两个旋度方程形式上泾渭分明，看不出它们其实是同一组协变方程在不同分量上的投影。其二，电场 $\vec E$ 与磁场 $\vec B$ 在三维语言中被当作两个独立的矢量场，然而第三章已经证明，一个惯性系中的纯电场在另一个相对运动的惯性系中会自动伴生磁场，反之亦然。既然 $\vec E$ 与 $\vec B$ 会互相"混入"，它们就不应该各自独立地作为三维矢量变换，而应当合并为一个在洛伦兹变换下整体协变的几何对象。

本章的任务就是完成这次合并。我们将从四维势 $A^\mu$ 出发，构造一个 4×4 的二阶反对称张量 $F_{\mu\nu}$，把 $\vec E$ 的三个分量与 $\vec B$ 的三个分量分别填入时间—空间位置与空间—空间位置。然后用这个张量计算两个洛伦兹标量不变量，说明为什么"纯电场"或"纯磁场"在一般情况下并非不变概念。本章末尾再推导沿任意方向 boost 时 $\vec E$、$\vec B$ 的变换公式，并代入一组具体数字验算。

本章全部内容属于标准电动力学与狭义相对论的交叉部分，落在【已证实】与【推导】两层，不引入原创假说。

## 二、从三维势到四维势

### （一）三维势的回顾

在第三章的记号体系中，三维电磁势由标势 $\varphi$ 与矢势 $\vec A$ 组成，场与势的关系为

$$
\vec E = -\nabla\varphi - \frac{\partial\vec A}{\partial t},
\qquad
\vec B = \nabla\times\vec A.
\tag{26.1}
$$

【已证实】这两个式子是电磁学中势与场的标准定义。由 (26.1) 立刻可以验证 $\nabla\cdot\vec B=0$ 与 $\nabla\times\vec E=-\partial_t\vec B$：前者来自 $\nabla\cdot(\nabla\times\vec A)\equiv 0$，后者来自对 $\vec E$ 取旋度时 $\nabla\times\nabla\varphi\equiv 0$ 与时间导数交换。也就是说，齐次麦克斯韦方程 (4.20)、(4.21) 由势的定义自动满足，无需额外假设。

### （二）四维势 $A^\mu$ 的组装

把 $(\varphi,\vec A)$ 组装成一个四维矢量。依照全书记号表中 $x^\mu=(ct,\,x,\,y,\,z)$ 的约定，定义逆变四维势为

$$
A^\mu = \left(\frac{\varphi}{c},\, A_x,\, A_y,\, A_z\right).
\tag{26.2}
$$

【推导】时间分量取 $\varphi/c$ 而不是 $\varphi$，是因为 $x^0=ct$，偏导数 $\partial_0=(1/c)\partial_t$ 中已经含一个 $1/c$ 因子；势的时间分量除以 $c$ 后，$A^\mu$ 与 $x^\mu$ 具有相同的量纲与相同的洛伦兹变换性质。降指标后

$$
A_\mu = \eta_{\mu\nu}A^\nu
= \left(\frac{\varphi}{c},\, -A_x,\, -A_y,\, -A_z\right).
\tag{26.3}
$$

这一步与第三章把四速度 $u^\mu=\gamma(c,\vec v)$ 降为 $u_\mu=\gamma(c,-\vec v)$ 同理。

### （三）偏导数构成四维矢量

回顾第四章 (4.1)，四维梯度为

$$
\partial_\mu = \frac{\partial}{\partial x^\mu}
= \left(\frac{1}{c}\frac{\partial}{\partial t},\, \frac{\partial}{\partial x},\, \frac{\partial}{\partial y},\, \frac{\partial}{\partial z}\right).
\tag{26.4}
$$

升指标后

$$
\partial^\mu = \eta^{\mu\nu}\partial_\nu
= \left(\frac{1}{c}\frac{\partial}{\partial t},\, -\frac{\partial}{\partial x},\, -\frac{\partial}{\partial y},\, -\frac{\partial}{\partial z}\right).
\tag{26.5}
$$

【推导】式 (26.5) 与 (4.2) 一致。有了 $\partial_\mu$ 与 $A_\mu$ 这两个四维矢量，下一步要构造的张量必须由它们的二阶导数组成。

## 三、反对称张量 $F_{\mu\nu}$ 的定义

### （四）用势的旋度定义张量

定义

$$
F_{\mu\nu} \equiv \partial_\mu A_\nu - \partial_\nu A_\mu.
\tag{26.6}
$$

【推导】式 (26.6) 是本章的核心定义。右端是两个四维矢量二阶导数的反对称组合。由于交换 $\mu,\nu$ 时整体变号，$F_{\mu\nu}$ 自动满足

$$
F_{\nu\mu} = -F_{\mu\nu},
\qquad F_{\mu\mu}=0.
\tag{26.7}
$$

这是一个二阶反对称张量。在 4 维时空中，独立分量数为 $\binom{4}{2}=6$，恰好对应 $\vec E$ 的三个分量与 $\vec B$ 的三个分量。这一巧合不是偶然：它正是电磁场自由度的协变计数。

### （五）时间—空间分量对应 $\vec E$

把 $\mu=0$、$\nu=i$ 代入 (26.6)。由 (26.4)、(26.3)：

$$
F_{0i} = \partial_0 A_i - \partial_i A_0.
\tag{26.8}
$$

逐项展开：$\partial_0=(1/c)\partial_t$，$A_i=-A_i^{\text{三维}}$（注意此处 $i$ 是四维指标，而 $A_i$ 作为下指标空间分量带负号），$A_0=\varphi/c$。代入：

$$
F_{0i}
= \frac{1}{c}\frac{\partial}{\partial t}(-A_i^{\text{三维}})
- \frac{\partial}{\partial x^i}\left(\frac{\varphi}{c}\right).
\tag{26.9}
$$

整理括号：

$$
F_{0i} = -\frac{1}{c}\left(\frac{\partial A_i^{\text{三维}}}{\partial t} + \frac{\partial\varphi}{\partial x^i}\right).
\tag{26.10}
$$

对照 (26.1) 中 $E_i=-(\partial_i\varphi+\partial_t A_i^{\text{三维}})$，括号内正是 $-E_i$，于是

$$
F_{0i} = \frac{E_i}{c}.
\tag{26.11}
$$

【推导】式 (26.11) 把电场的三个分量安放在张量的时间—空间位置上。$1/c$ 因子来自 $x^0=ct$ 的链式法则，它保证了 $F_{\mu\nu}$ 各分量的量纲统一为 SI 制下的 $T$（特斯拉）：$E/c$ 的单位为 $(\mathrm{V/m})/(\mathrm{m/s})=\mathrm{V\,s/m^2}=\mathrm{T}$，与 $B$ 同量纲。

### （六）空间—空间分量对应 $\vec B$

取 $\mu=i$、$\nu=j$（$i,j$ 均为空间指标）：

$$
F_{ij} = \partial_i A_j - \partial_j A_i.
\tag{26.12}
$$

由于 $A_j=-A_j^{\text{三维}}$、$A_i=-A_i^{\text{三维}}$，代入：

$$
F_{ij}
= \frac{\partial}{\partial x^i}(-A_j^{\text{三维}})
- \frac{\partial}{\partial x^j}(-A_i^{\text{三维}})
= -\left(\frac{\partial A_j^{\text{三维}}}{\partial x^i} - \frac{\partial A_i^{\text{三维}}}{\partial x^j}\right).
\tag{26.13}
$$

利用三维 Levi-Civita 符号 $\varepsilon_{ijk}$ 与 $\vec B=\nabla\times\vec A$ 的分量关系 $B_k=\varepsilon_{klm}\partial_l A_m^{\text{三维}}$，可以验证

$$
F_{ij} = -\varepsilon_{ijk} B_k.
\tag{26.14}
$$

【推导】式 (26.14) 把磁场的三个分量安放在张量的纯空间位置上。具体写出：$F_{12}=-B_z$，$F_{13}=+B_y$，$F_{23}=-B_x$，其余反对称位置由 (26.7) 补全。

### （七）完整矩阵形式

把 (26.11)、(26.14) 汇总，$F_{\mu\nu}$ 的 4×4 矩阵为

$$
F_{\mu\nu} =
\begin{pmatrix}
0 & E_x/c & E_y/c & E_z/c\\
-E_x/c & 0 & -B_z & B_y\\
-E_y/c & B_z & 0 & -B_x\\
-E_z/c & -B_y & B_x & 0
\end{pmatrix}.
\tag{26.15}
$$

【已证实】这就是电磁场张量在 SI 单位制、号差 $(+,-,-,-)$ 下的标准形式。每一行、每一列都满足反对称；对角元恒为零；上三角与下三角互为相反数。

升指标得到 $F^{\mu\nu}=\eta^{\mu\alpha}\eta^{\nu\beta}F_{\alpha\beta}$。由于时间分量经过一次升指标会变号而空间分量不变，结果为

$$
F^{\mu\nu} =
\begin{pmatrix}
0 & -E_x/c & -E_y/c & -E_z/c\\
E_x/c & 0 & -B_z & B_y\\
E_y/c & B_z & 0 & -B_x\\
E_z/c & -B_y & B_x & 0
\end{pmatrix}.
\tag{26.16}
$$

【推导】对比 (26.15) 与 (26.16)，升降指标只翻转了时间—空间块的符号，空间—空间块保持不变。这一差异在后面计算不变量时会反复用到。

从几何上看，$F_{\mu\nu}$ 不是任意的 4×4 矩阵，而是一个二阶反对称张量，在四维几何中对应一个二形式（bivector）。反对称性 (26.7) 意味着它在每一对指标上都像面积元一样有方向感：$F_{\mu\nu}$ 描述的是时空中一个有向小面元上的场通量。6 个独立分量恰好对应四维时空中 6 个独立的坐标面（$x^0x^1$、$x^0x^2$、$x^0x^3$、$x^1x^2$、$x^2x^3$、$x^3x^1$）。前三块是时间—空间面元，对应电场；后三块是纯空间面元，对应磁场。这一几何图像把"电场是时间—空间混合面元、磁场是纯空间面元"说清楚了：洛伦兹变换之所以能把电场变成磁场，正是因为它在这两类面元之间"旋转"。

## 四、两个洛伦兹不变量

### （八）缩并构造不变量 $I_1$

二阶张量的最简单洛伦兹标量是自身的缩并。计算

$$
I_1 \equiv F_{\mu\nu}F^{\mu\nu}.
\tag{26.17}
$$

按指标逐项展开。由于反对称，对角元为零，只需计算 $(0,i)$ 与 $(i,j)$ 两类非零对。

对 $(0,i)$ 类：$F_{0i}F^{0i}=(E_i/c)(-E_i/c)=-E_i^2/c^2$，而 $(i,0)$ 给出相同的一项，合计 $-2E_i^2/c^2$。对三个 $i$ 求和，贡献为 $-2E^2/c^2$。

对 $(i,j)$ 类：利用 (26.14) 与 (26.16)，$F_{ij}F^{ij}=(-\varepsilon_{ijk}B_k)(-\varepsilon_{ijl}B_l)$。对 $i,j$ 求和时使用恒等式 $\sum_i\varepsilon_{ijk}\varepsilon_{ijl}=2\delta_{kl}$，得到空间—空间贡献 $2B^2$。

两类合并：

$$
I_1 = F_{\mu\nu}F^{\mu\nu} = 2\left(B^2 - \frac{E^2}{c^2}\right).
\tag{26.18}
$$

【推导】式 (26.18) 是本书采用的号差与张量定义下的洛伦兹不变量之一，记作 $I_1$。部分教材采用相反的整体符号约定，会把同一结果写作 $-2(B^2-E^2/c^2)$；两种写法相差一个整体负号，物理内容相同。本书统一采用 (26.18) 的写法。

值得强调的是，$I_1$ 的量纲是 $(\mathrm{V/m})^2/(\mathrm{m/s})^2=\mathrm{T}^2$，与 $B^2$ 同量纲。这说明 $E/c$ 与 $B$ 在张量中确实处于同等地位：它们都进入同一个平方项，只不过在号差 $(+,-,-,-)$ 下 $E/c$ 带负号、$B$ 带正号。这种"负电正磁"的符号安排，正是第三章号差约定在场张量上的直接投影。

### （九）构造对偶张量

为得到另一个独立不变量，引入对偶张量

$$
\tilde F^{\mu\nu} \equiv \frac{1}{2}\varepsilon^{\mu\nu\rho\sigma}F_{\rho\sigma},
\tag{26.19}
$$

其中 $\varepsilon^{\mu\nu\rho\sigma}$ 是四维全反对称符号，取 $\varepsilon^{0123}=-1$ 以与号差 $(+,-,-,-)$ 配套。

【推导】对偶操作的几何意义是把 $F_{\mu\nu}$ 的电部分与磁部分互换。代入 (26.15) 逐项计算可得

$$
\tilde F^{\mu\nu} =
\begin{pmatrix}
0 & -B_x & -B_y & -B_z\\
B_x & 0 & E_z/c & -E_y/c\\
B_y & -E_z/c & 0 & E_x/c\\
B_z & E_y/c & -E_x/c & 0
\end{pmatrix}.
\tag{26.20}
$$

对比 (26.16)：$\tilde F$ 的时间—空间块是 $-\vec B$，空间—空间块则把 $\vec B$ 的位置换成 $\vec E/c$。这正是"电↔磁"对偶的张量写法。

### （十）不变量 $I_2=F_{\mu\nu}\tilde F^{\mu\nu}$

计算

$$
I_2 \equiv F_{\mu\nu}\tilde F^{\mu\nu}.
\tag{26.21}
$$

仍按 $(0,i)$ 与 $(i,j)$ 分类。对 $(0,i)$：$F_{0i}\tilde F^{0i}=(E_i/c)(-B_i)=-E_iB_i/c$，$(i,0)$ 重复一次，合计 $-2\vec E\cdot\vec B/c$。对 $(i,j)$：$F_{ij}\tilde F^{ij}=(-\varepsilon_{ijk}B_k)(-\varepsilon_{ijl}E_l/c)$，求和后同样给出 $-2\vec E\cdot\vec B/c$。两类合并：

$$
I_2 = F_{\mu\nu}\tilde F^{\mu\nu} = -\frac{4}{c}\,\vec E\cdot\vec B.
\tag{26.22}
$$

【推导】式 (26.22) 记作 $I_2$。与 (26.18) 一样，不同教材的整体符号可能不同，但 $\vec E\cdot\vec B$ 在洛伦兹变换下不变这一物理结论是共通的。$I_2$ 的量纲为 $(V/m)(T)/(m/s)=T^2$，与 $I_1$ 一致。

### （十一）不变量的物理含义

(26.18) 与 (26.22) 给出两个不随惯性系变换的标量。它们的物理含义可以从三类极端情形读出。

只含电场的情形：在某个惯性系中 $\vec B=0$。此时 $I_1=-2E^2/c^2<0$，$I_2=0$。负的 $I_1$ 说明这是一个"类电"场——在任何 boost 下 $I_1$ 保持负号，因此不可能通过参考系变换把它变成纯磁场（纯磁场的 $I_1=2B^2>0$）。

只含磁场的情形：在某个惯性系中 $\vec E=0$。此时 $I_1=2B^2>0$，$I_2=0$。正的 $I_1$ 说明这是"类磁"场。

辐射场的情形：$\vec E\perp\vec B$ 且 $E=cB$。此时 $I_1=0$ 且 $I_2=0$，两个不变量同时为零。这正是平面电磁波的场结构——真空中的自由电磁场在任何惯性系中都满足 $E=cB$ 与 $\vec E\perp\vec B$，两个不变量都消失。第四章 (4.19)–(4.22) 给出的平面波解，在张量语言下就是 $I_1=I_2=0$ 的场。

【已证实】这两条判据（$I_1$ 的符号区分类电/类磁，$I_1=I_2=0$ 对应辐射场）是狭义相对论电磁学的标准结论。它们解释了为什么"纯电场"不能通过 boost 变成"纯磁场"：不变量 $I_1$ 的符号在变换下守恒。

## 五、Boost 下 $\vec E$ 与 $\vec B$ 的变换

### （十二）张量变换法则

二阶张量在洛伦兹变换 $x'^\mu=\Lambda^\mu{}_\nu x^\nu$ 下按

$$
F'^{\mu\nu} = \Lambda^\mu{}_\alpha\Lambda^\nu{}_\beta F^{\alpha\beta}
\tag{26.23}
$$

变换。【推导】这是张量变换的一般规则：每个指标各自乘一个 $\Lambda$。由于 $F^{\alpha\beta}$ 只有 6 个独立分量，(26.23) 实际给出 6 个方程，分别对应 $\vec E$、$\vec B$ 的 6 个分量在新参考系中的表达式。

### （十三）沿 $x$ 方向的 boost

设 $S'$ 系相对 $S$ 系以速度 $v$ 沿 $+x$ 方向运动，$\beta=v/c$，$\gamma=(1-\beta^2)^{-1/2}$。洛伦兹矩阵为

$$
\Lambda =
\begin{pmatrix}
\gamma & \gamma\beta & 0 & 0\\
\gamma\beta & \gamma & 0 & 0\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1
\end{pmatrix}.
\tag{26.24}
$$

把 (26.24) 代入 (26.23)，逐项计算 $F'^{\mu\nu}$ 的各分量，再按 (26.16) 的对应关系还原为 $\vec E'$、$\vec B'$。

### （十四）平行分量与垂直分量

把 $\vec E$、$\vec B$ 分别分解为平行于 boost 方向（$x$ 方向）与垂直于 boost 方向（$y,z$ 平面）的部分。记 $\parallel$ 表示沿 $x$，$\perp$ 表示 $y,z$ 平面。计算结果为

$$
E'_\parallel = E_\parallel,
\qquad
B'_\parallel = B_\parallel,
\tag{26.25}
$$

$$
\vec E'_\perp = \gamma\left(\vec E_\perp + \vec v\times\vec B\right),
\tag{26.26}
$$

$$
\vec B'_\perp = \gamma\left(\vec B_\perp - \frac{1}{c^2}\vec v\times\vec E\right).
\tag{26.27}
$$

【推导】式 (26.25)–(26.27) 是本章最实用的结果。平行于 boost 方向的场分量不变；垂直分量则被 $\gamma$ 放大，并混入来自另一个场的贡献。特别地，即使在 $S$ 系中 $\vec B=0$，只要 $\vec E$ 有垂直于 $\vec v$ 的分量，$S'$ 系中就会出现磁场

$$
\vec B' = -\gamma\frac{\vec v\times\vec E}{c^2}.
\tag{26.28}
$$

反过来，即使在 $S$ 系中 $\vec E=0$，只要 $\vec B$ 有垂直分量，$S'$ 系中就会出现电场 $\vec E'=\gamma\vec v\times\vec B$。这正是"电场与磁场是同一张量的两个侧面"这一论断的定量表述。

### （十五）不变量自检

用 (26.25)–(26.27) 直接代入，可以验证 (26.18)、(26.22) 在 boost 下不变。以 $I_1$ 为例展开计算。把 $I_1$ 分解为平行项与垂直项：

$$
I_1 = 2\left(B_\parallel^2+B_\perp^2 - \frac{E_\parallel^2+E_\perp^2}{c^2}\right).
\tag{26.28a}
$$

boost 后平行项原样保留：$E'_\parallel=E_\parallel$，$B'_\parallel=B_\parallel$。垂直项按 (26.26)、(26.27) 变换：

$$
E_\perp'^2 = \gamma^2\left(\vec E_\perp+\vec v\times\vec B\right)^2
= \gamma^2\left(E_\perp^2 + 2\vec E_\perp\cdot(\vec v\times\vec B) + v^2 B_\perp^2 - v^2(\vec B_\perp\cdot\hat v)^2\right).
\tag{26.28b}
$$

由于 $\vec v\perp\vec E_\perp$、$\vec v\perp\vec B_\perp$，混合项 $2\vec E_\perp\cdot(\vec v\times\vec B)=2\vec B\cdot(\vec v\times\vec E_\perp)$ 不为零，但在与 $B_\perp'^2$ 的对应项配对时恰好相消。把 (26.26)、(26.27) 代入 $E_\perp'^2/c^2-B_\perp'^2$，经过代数整理得到

$$
\frac{E_\perp'^2}{c^2}-B_\perp'^2
= \gamma^2\left(1-\beta^2\right)\left(\frac{E_\perp^2}{c^2}-B_\perp^2\right)
= \frac{E_\perp^2}{c^2}-B_\perp^2.
\tag{26.28c}
$$

这里用到 $\gamma^2(1-\beta^2)=1$。平行项与垂直项各自不变，故 $I_1$ 整体不变。$I_2=\vec E'\cdot\vec B'/c$ 的验证同理：平行部分 $E_\parallel B_\parallel$ 不变，垂直部分的交叉项经 $\gamma^2(1-\beta^2)=1$ 因子后还原原式。这一自检说明 (26.25)–(26.27) 与 (26.18)、(26.22) 是自洽的【推导】。

### （十六）任意方向 boost 的紧凑形式

把沿 $x$ 方向的结果推广到 boost 方向任意单位矢量 $\hat n$ 的情形。令 $\vec v=v\hat n$，把 $\vec E,\vec B$ 分解为沿 $\hat n$ 与垂直 $\hat n$ 两部分。(26.25)–(26.27) 的矢量写法为

$$
\vec E' = \vec E_\parallel + \gamma\left(\vec E_\perp + \vec v\times\vec B\right),
\qquad
\vec B' = \vec B_\parallel + \gamma\left(\vec B_\perp - \frac{1}{c^2}\vec v\times\vec E\right).
\tag{26.28d}
$$

其中 $\vec E_\parallel=(\vec E\cdot\hat n)\hat n$，$\vec E_\perp=\vec E-\vec E_\parallel$。这一形式不依赖于坐标系取向，可直接用于任意方向的参考系变换。当 $\vec v$ 与 $\vec E$ 或 $\vec B$ 既不平行也不垂直时，平行分量原样保留、垂直分量按 (26.28d) 变换，两者相加即得新场【推导】。

## 六、数值例题

### （十六）题设

在惯性系 $S$ 中存在一个均匀电场

$$
\vec E = (0,\, 1000\ \mathrm{V/m},\, 0),
\qquad
\vec B = (0,\, 0,\, 0).
\tag{26.29}
$$

惯性系 $S'$ 沿 $+x$ 方向以 $\beta=0.6$ 相对 $S$ 运动。求 $S'$ 系中的 $\vec E'$、$\vec B'$，并验算两个不变量是否守恒。

### （十七）计算 $\gamma$ 与 $\vec E'$、$\vec B'$

由 $\beta=0.6$：

$$
\gamma = \frac{1}{\sqrt{1-0.36}} = \frac{1}{0.8} = 1.25.
\tag{26.30}
$$

电场沿 $y$ 方向，垂直于 boost 方向。由 (26.26)：

$$
E'_y = \gamma(E_y + (\vec v\times\vec B)_y) = \gamma E_y = 1.25\times 1000 = 1250\ \mathrm{V/m}.
\tag{26.31}
$$

$E'_x=E_x=0$，$E'_z=0$。

磁场在 $S$ 系为零，但 (26.27) 给出

$$
B'_z = \gamma\left(B_z - \frac{1}{c^2}(\vec v\times\vec E)_z\right).
\tag{26.32}
$$

$\vec v=v\hat x$，$\vec E=E_y\hat y$，故 $\vec v\times\vec E=vE_y(\hat x\times\hat y)=vE_y\hat z$，$(\vec v\times\vec E)_z=vE_y$。代入：

$$
B'_z = -\gamma\frac{vE_y}{c^2}
= -\gamma\beta\frac{E_y}{c}.
\tag{26.33}
$$

数值：

$$
B'_z = -1.25\times 0.6\times\frac{1000}{2.9979\times 10^8}
\approx -2.502\times 10^{-6}\ \mathrm{T}.
\tag{26.34}
$$

其余分量 $B'_x=B'_y=0$。

【推导】式 (26.34) 的量级约为 $2.5\ \mu\mathrm T$，大约是地球表面地磁场（约 $50\ \mu\mathrm T$）的二十分之一。这说明即使在实验室中可以忽略磁场的问题里，只要观测者以 $0.6c$ 运动，磁场就不再小到可以忽略。

值得做一个反向验算：如果从 $S'$ 系看 $S$ 系，$S$ 系相对 $S'$ 以 $-v$ 沿 $x$ 方向运动。把 (26.26)、(26.27) 中的 $\vec v$ 换成 $-\vec v$，$\gamma$ 不变，应能还原 $E_y=1000\ \mathrm{V/m}$、$B_z=0$。代入 $E'_y=1250$、$B'_z=-2.502\times10^{-6}$：

$$
E_y = \gamma(E'_y + (-\vec v)\times\vec B')_y.
\tag{26.34a}
$$

$(-\vec v)\times\vec B'=(-v\hat x)\times(B'_z\hat z)=-vB'_z(\hat x\times\hat z)=+vB'_z\hat y$。于是 $E_y=\gamma(E'_y+vB'_z)=1.25(1250+0.6c\times(-2.502\times10^{-6}))$。括号内后一项 $0.6\times2.9979\times10^8\times(-2.502\times10^{-6})\approx-450.2$，故括号内为 $1250-450.2=799.8$，乘 $1.25$ 得 $999.7\approx1000$，还原成功。这一互逆验算说明 (26.26)、(26.27) 构成自逆的变换对【推导】。

### （十八）不变量验算

在 $S$ 系中：

$$
I_1(S) = 2\left(0 - \frac{1000^2}{c^2}\right)
= -\frac{2\times 10^6}{(2.9979\times 10^8)^2}
\approx -2.225\times 10^{-11}\ \mathrm{T^2}.
\tag{26.35}
$$

$$
I_2(S) = -\frac{4}{c}\vec E\cdot\vec B = 0.
\tag{26.36}
$$

在 $S'$ 系中，$E'=1250\ \mathrm{V/m}$，$B'=2.502\times 10^{-6}\ \mathrm{T}$：

$$
\frac{E'^2}{c^2} = \frac{1250^2}{c^2} = \frac{1.5625\times 10^6}{8.9876\times 10^{16}}
\approx 1.739\times 10^{-11}\ \mathrm{T^2},
\tag{26.37}
$$

$$
B'^2 = (2.502\times 10^{-6})^2 \approx 6.260\times 10^{-12}\ \mathrm{T^2}.
\tag{26.38}
$$

于是

$$
I_1(S') = 2\left(B'^2 - \frac{E'^2}{c^2}\right)
= 2(6.260\times 10^{-12} - 1.739\times 10^{-11})
\approx -2.226\times 10^{-11}\ \mathrm{T^2}.
\tag{26.39}
$$

(26.39) 与 (26.35) 在四舍五入误差内一致。$I_2(S')=-(4/c)E'_yB'_z$：虽然 $E'$ 与 $B'$ 都非零，但 $\vec E'\parallel\hat y$、$\vec B'\parallel\hat z$，二者垂直，$\vec E'\cdot\vec B'=0$，故 $I_2(S')=0$，与 (26.36) 一致【推导】。

### （十九）例题的结论

这组数字说明：一个在 $S$ 系中看似纯粹的电场，在 $S'$ 系中同时包含了电场与磁场。$E'$ 从 $1000\ \mathrm{V/m}$ 增大到 $1250\ \mathrm{V/m}$（$\gamma$ 倍），而 $B'$ 从 $0$ 增大到 $2.5\ \mu\mathrm T$。但两个不变量 $I_1$、$I_2$ 在两系中严格相同。这正是把 $\vec E,\vec B$ 打包为 $F_{\mu\nu}$ 的意义：变换的是分量，不变的是张量本身。

## 七、本章小结

本章完成了以下推导链：

$$
(\varphi,\vec A)
\xrightarrow{\text{组装 }A^\mu=(\varphi/c,\vec A)}
A_\mu
\xrightarrow{\partial_\mu A_\nu-\partial_\nu A_\mu}
F_{\mu\nu}
\xrightarrow{\text{填入 }E,B}
\text{4×4 反对称矩阵}
\xrightarrow{\text{缩并}}
I_1=2(B^2-E^2/c^2),\; I_2=-(4/c)\vec E\cdot\vec B
\xrightarrow{\Lambda^\mu{}_\alpha\Lambda^\nu{}_\beta}
E'_\parallel=E_\parallel,\; \vec E'_\perp=\gamma(\vec E_\perp+\vec v\times\vec B),\;\vec B'_\perp=\gamma(\vec B_\perp-\vec v\times\vec E/c^2).
$$

本章的关键结论是：电场与磁场不是两个独立的三维矢量，而是同一个二阶反对称张量 $F_{\mu\nu}$ 在不同指标上的投影。观测者换一个惯性系，看到的是这个张量在新坐标系下的不同分量组合，但两个洛伦兹标量 $I_1$、$I_2$ 保持不变。这一结论把第三章的时空观与第四章的电磁观缝合在一起：$v=c$ 公设不仅约束了质点运动，也约束了场的分量如何在参考系之间重新分配。下一章将把麦克斯韦方程本身也写成协变形式，说明四个三维方程如何被 $F_{\mu\nu}$ 的两个散度方程所囊括，并把洛伦兹力改写为四元力的协变形式。

> **本章分层占比**：已证实 35% / 推导 60% / 假说 5%（合计100%）
