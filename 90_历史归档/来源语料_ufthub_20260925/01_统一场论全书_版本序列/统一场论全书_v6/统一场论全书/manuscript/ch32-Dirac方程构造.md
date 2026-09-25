# 第三十二章 Dirac方程构造

## 一、本章为何从 Klein—Gordon 方程的困境说起

第二十一章已经从洛伦兹群表示分类的角度说明了电子为何必须用四分量 Dirac 旋量来描述：有质量自旋 $1/2$ 粒子的小群是 $\mathrm{SO}(3)$，其不可约表示要求旋量空间为 $(1/2,0)\oplus(0,1/2)$ 的直和。那一章把这一结论当作群论分类的结果直接引用，并未推导对应的波动方程。本章补上这一环：为什么描述电子的相对论性波动方程必须是一阶的，而不是像 Klein—Gordon 方程那样是二阶的；一阶方程如何强制要求引入 $\gamma$ 矩阵；$\gamma$ 矩阵的代数结构又如何把质壳关系 $p^2=m^2$ 因式分解为两个一阶算符的乘积。

本章与第三十三章共同构成 Dirac 方程的完整构造。本章只处理自由方程的代数骨架：构造动机、$\gamma$ 矩阵代数、标准表示、质壳因式分解；下一章处理平面波解、旋量归一化、概率流与非相对论极限。两章合起来，读者应当能从第二章的振子图像一路走到电子的相对论性波动方程，并理解为什么这个方程的数学结构比 Klein—Gordon 方程更丰富。

为书写简洁，本章与下一章采用高能物理中通用的自然单位制 $\hbar=c=1$。这一约定把第三章中的 $\kappa=mc/\hbar$ 直接简化为 $m$，把质壳关系 $E^2=p^2c^2+m^2c^4$ 简化为 $E^2=\vec p^{\,2}+m^2$。恢复单位时，只需把本章所有公式中的 $m$ 替换为 $mc/\hbar$、把 $x^\mu$ 理解为 $(\vec t,\vec x)$ 即可。本章全部内容属于【已证实】与【推导】两层，不引入原创假说。

## 二、Klein—Gordon 方程的二阶困境

### （一）从质壳关系到二阶波动方程

在第三章中，相对论自由粒子的质壳关系为

$$
p_\mu p^\mu = m^2.
\tag{32.1}
$$

在自然单位制下，四动量 $p^\mu=(E,\vec p)$，度规 $g^{\mu\nu}=\mathrm{diag}(1,-1,-1,-1)$，因此 (32.1) 展开为 $E^2-\vec p^{\,2}=m^2$。量子化替换 $E\to i\partial_t$、$\vec p\to -i\nabla$（即 $p_\mu\to i\partial_\mu$）代入 (32.1)，得到

$$
\partial_\mu\partial^\mu\,\phi + m^2\phi = 0.
\tag{32.2}
$$

这就是第五章已经写过的统一主方程 $(\Box+\kappa^2)\Phi=0$ 在自然单位制下的形式，即 Klein—Gordon 方程。【推导】

### （二）概率密度的非正定性

Klein—Gordon 方程是二阶时间偏微分方程。对它作量子力学解释时，标准做法是构造守恒流。把 (32.2) 乘 $\phi^*$，把复共轭方程乘 $\phi$，两式相减，得到

$$
\phi^*\partial_\mu\partial^\mu\phi - \phi\,\partial_\mu\partial^\mu\phi^* = 0.
\tag{32.3}
$$

改写为四维散度：

$$
\partial_\mu\left[\phi^*\partial^\mu\phi - \phi(\partial^\mu\phi)^*\right] = 0.
\tag{32.4}
$$

于是守恒流的时间分量为

$$
\rho_{\mathrm{KG}} = i\left(\phi^*\partial_t\phi - \phi\,\partial_t\phi^*\right).
\tag{32.5}
$$

【推导】问题出在 (32.5) 的符号上。$\rho_{\mathrm{KG}}$ 正比于 $\partial_t\phi$ 与 $\phi$ 的组合，而 $\partial_t\phi$ 本身没有非负约束。对一个平面波 $\phi\sim e^{-iEt+i\vec p\cdot\vec x}$，代入 (32.5) 得 $\rho_{\mathrm{KG}}\propto 2E\,|\phi_0|^2$。当 $E$ 取负能解 $E=-\sqrt{\vec p^{\,2}+m^2}$ 时，$\rho_{\mathrm{KG}}$ 为负。负概率密度在量子力学中不可接受：概率密度必须处处非负，才能解释为在某点发现粒子的几率。

### （三）负能解与单粒子解释的崩塌

Klein—Gordon 方程的另一困难是负能解。质壳关系 $E^2=\vec p^{\,2}+m^2$ 对每个 $\vec p$ 给出两个根 $E=\pm\sqrt{\vec p^{\,2}+m^2}$。二阶方程 (32.2) 的通解自动包含这两个根。在单粒子量子力学框架下，负能解意味着粒子可以无限级联向下辐射能量而不收敛，理论失去稳定基态。

Dirac 在 1928 年面对的正是这两个困难。他的思路是：如果把质壳关系 (32.1) 因式分解，把二阶方程降为一阶，那么概率密度就可能只含 $\psi^*\psi$ 型的双线性组合，从而自动非负；同时一阶方程对时间只含一次导数，解的能量符号也更容易处理。这一思路直接导致了 Dirac 方程的诞生。【已证实】

需要说明的是，Klein—Gordon 方程并非错误。后来的量子场论表明，它正确描述自旋为零的粒子（如 $\pi$ 介子），只是不能作为单粒子波方程使用。负概率与负能困难在场论框架下被重新解释为反粒子的存在。但在 Dirac 1928 年构造方程的历史语境中，这两个困难确实是驱动一阶化的物理动机。

## 三、一阶化的尝试与 γ 矩阵的引入

### （一）Dirac 的线性化假设

设希望把质壳关系 (32.1) 改写为一阶波动方程。对一个多分量波函数 $\psi$（分量数待定），假设方程形如

$$
\left(i\gamma^\mu\partial_\mu - m\right)\psi = 0,
\tag{32.6}
$$

其中 $\gamma^\mu$ 是待求的 $N\times N$ 常矩阵（$N$ 为分量数），$m$ 是静质量。【推导】

式 (32.6) 对 $\partial_\mu$ 线性依赖，是一阶方程。为了让它的解自动满足质壳关系，把 (32.6) 左端的算符再作用一次：

$$
\left(i\gamma^\mu\partial_\mu + m\right)\left(i\gamma^\nu\partial_\nu - m\right)\psi = 0.
\tag{32.7}
$$

展开乘积：

$$
\left(\gamma^\mu\gamma^\nu\partial_\mu\partial_\nu + m^2\right)\psi = 0.
\tag{32.8}
$$

这里用了 $(i\gamma^\mu\partial_\mu)^2=-\gamma^\mu\gamma^\nu\partial_\mu\partial_\nu$，以及 $i^2=-1$。由于 $\partial_\mu\partial_\nu$ 对 $\mu,\nu$ 对称，乘积中只有 $\gamma^\mu\gamma^\nu$ 的对称部分贡献：

$$
\gamma^\mu\gamma^\nu\partial_\mu\partial_\nu
= \frac{1}{2}\{\gamma^\mu,\gamma^\nu\}\partial_\mu\partial_\nu.
\tag{32.9}
$$

### （二）Clifford 代数的导出

为了让 (32.8) 恰好回到 Klein—Gordon 方程 (32.2)，要求

$$
\frac{1}{2}\{\gamma^\mu,\gamma^\nu\} = g^{\mu\nu},
\tag{32.10}
$$

即

$$
\{\gamma^\mu,\gamma^\nu\} = \gamma^\mu\gamma^\nu + \gamma^\nu\gamma^\mu = 2g^{\mu\nu}I_N.
\tag{32.11}
$$

【推导】式 (32.11) 就是第二十一章 (21.21) 引入的 Clifford 代数。它是一阶化能成功的充要条件：只要 $\gamma^\mu$ 满足 (32.11)，那么对 (32.6) 再作用一次 $(i\gamma^\mu\partial_\mu+m)$，就自动得到 $(\Box+m^2)\psi=0$，与 (32.2) 一致。换言之，Dirac 方程的解必定是 Klein—Gordon 方程的解，但反之不然：Dirac 方程是更强的约束，它额外挑选出满足一阶方程的子集，而这个子集恰好对应自旋 $1/2$ 的粒子。

需要强调 (32.11) 不是人为假设，而是一阶化的代数必然。如果 $\gamma^\mu$ 不满足 (32.11)，那么 (32.8) 中就会留下多余的非对称项 $\frac{1}{2}[\gamma^\mu,\gamma^\nu]\partial_\mu\partial_\nu$，方程就不再等价于质壳关系。(32.11) 的唯一性将在下一小节通过维数论证说明。

### （三）分量数 $N=4$ 的必要性

式 (32.11) 中的 $\gamma^\mu$ 是 $N\times N$ 矩阵。$N$ 最小能取多少？$N=1$ 时 $\gamma^\mu$ 退化为数，反对易子条件 (32.11) 要求两个非零实数互相反号相乘为零，矛盾。$N=2$ 时，三个 Pauli 矩阵加上单位矩阵共张成四维线性空间，但四维闵氏时空需要四个 $\gamma^\mu$，且 Pauli 矩阵的对易关系是 $\mathfrak{su}(2)$ 而非 Clifford 代数，无法同时满足四个指标的反对易条件。$N=4$ 是满足 (32.11) 的最小维数。【已证实】

这一结论与第二十一章的群论分类严格吻合：Dirac 旋量空间是四维复空间，对应 $(1/2,0)\oplus(0,1/2)$ 直和。代数构造（反对易条件要求四维）与群论构造（小群表示分类要求四维）从两条独立路径到达同一结论，这本身就是理论自洽性的一个标志。

## 四、标准表示下的 γ 矩阵

### （一）Dirac—Pauli 标准表示

取 $g^{\mu\nu}=\mathrm{diag}(1,-1,-1,-1)$。满足 (32.11) 的一组显式矩阵为

$$
\gamma^0 =
\begin{pmatrix}
I_2 & 0\\
0 & -I_2
\end{pmatrix},
\qquad
\gamma^i =
\begin{pmatrix}
0 & \sigma_i\\
-\sigma_i & 0
\end{pmatrix},
\tag{32.12}
$$

其中 $I_2$ 是二阶单位矩阵，$\sigma_i$ 是第二十一章 (21.10) 给出的三个 Pauli 矩阵。【推导】下面直接验证 (32.12) 满足反对易条件。

### （二）验证 $\{\gamma^0,\gamma^0\}=2g^{00}$

计算 $\gamma^0$ 的平方：

$$
(\gamma^0)^2 =
\begin{pmatrix}
I_2 & 0\\
0 & -I_2
\end{pmatrix}
\begin{pmatrix}
I_2 & 0\\
0 & -I_2
\end{pmatrix}
=
\begin{pmatrix}
I_2 & 0\\
0 & I_2
\end{pmatrix}
= I_4.
\tag{32.13}
$$

由于 $\gamma^0$ 与自身反对易时等于 $2(\gamma^0)^2$，而 $g^{00}=1$，故 $\{\gamma^0,\gamma^0\}=2I_4=2g^{00}I_4$，符合 (32.11)。【推导】

### （三）验证 $\{\gamma^0,\gamma^i\}=0$

计算 $\gamma^0\gamma^i$：

$$
\gamma^0\gamma^i =
\begin{pmatrix}
I_2 & 0\\
0 & -I_2
\end{pmatrix}
\begin{pmatrix}
0 & \sigma_i\\
-\sigma_i & 0
\end{pmatrix}
=
\begin{pmatrix}
0 & \sigma_i\\
\sigma_i & 0
\end{pmatrix}.
\tag{32.14}
$$

反过来 $\gamma^i\gamma^0$：

$$
\gamma^i\gamma^0 =
\begin{pmatrix}
0 & \sigma_i\\
-\sigma_i & 0
\end{pmatrix}
\begin{pmatrix}
I_2 & 0\\
0 & -I_2
\end{pmatrix}
=
\begin{pmatrix}
0 & -\sigma_i\\
-\sigma_i & 0
\end{pmatrix}.
\tag{32.15}
$$

两式相加：

$$
\gamma^0\gamma^i + \gamma^i\gamma^0 =
\begin{pmatrix}
0 & 0\\
0 & 0
\end{pmatrix} = 0.
\tag{32.16}
$$

而 $g^{0i}=0$，故符合 (32.11)。【推导】

### （四）验证 $\{\gamma^i,\gamma^j\}=-2\delta^{ij}I_4$

计算 $\gamma^i\gamma^j$：

$$
\gamma^i\gamma^j =
\begin{pmatrix}
0 & \sigma_i\\
-\sigma_i & 0
\end{pmatrix}
\begin{pmatrix}
0 & \sigma_j\\
-\sigma_j & 0
\end{pmatrix}
=
\begin{pmatrix}
-\sigma_i\sigma_j & 0\\
0 & -\sigma_i\sigma_j
\end{pmatrix}.
\tag{32.17}
$$

交换 $i,j$：

$$
\gamma^j\gamma^i =
\begin{pmatrix}
-\sigma_j\sigma_i & 0\\
0 & -\sigma_j\sigma_i
\end{pmatrix}.
\tag{32.18}
$$

相加：

$$
\gamma^i\gamma^j + \gamma^j\gamma^i
=
\begin{pmatrix}
-(\sigma_i\sigma_j+\sigma_j\sigma_i) & 0\\
0 & -(\sigma_i\sigma_j+\sigma_j\sigma_i)
\end{pmatrix}.
\tag{32.19}
$$

Pauli 矩阵满足 $\sigma_i\sigma_j+\sigma_j\sigma_i=2\delta_{ij}I_2$（这是 Pauli 代数的基本关系，由 (21.10) 直接验算可得）。代入：

$$
\{\gamma^i,\gamma^j\} =
\begin{pmatrix}
-2\delta_{ij}I_2 & 0\\
0 & -2\delta_{ij}I_2
\end{pmatrix}
= -2\delta_{ij}I_4 = 2g^{ij}I_4,
\tag{32.20}
$$

因为 $g^{ij}=-\delta_{ij}$。【推导】式 (32.13)、(32.16)、(32.20) 联合起来，完整验证了 (32.12) 满足 (32.11)。

### （五）其他常用矩阵与 γ⁵

从 $\gamma^\mu$ 可以构造出几个在后续章节频繁使用的矩阵。电荷共轭与手征投影需要 $\gamma^5$：

$$
\gamma^5 \equiv i\gamma^0\gamma^1\gamma^2\gamma^3.
\tag{32.21}
$$

【推导】由 (32.11) 可验证 $(\gamma^5)^2=I_4$ 且 $\{\gamma^5,\gamma^\mu\}=0$，即 $\gamma^5$ 与所有四个 $\gamma^\mu$ 都反对易。在标准表示 (32.12) 下，直接计算给出

$$
\gamma^5 =
\begin{pmatrix}
0 & I_2\\
I_2 & 0
\end{pmatrix}.
\tag{32.22}
$$

$\gamma^5$ 的本征值为 $\pm1$，对应的投影算符

$$
P_L = \frac{1-\gamma^5}{2},\qquad P_R = \frac{1+\gamma^5}{2}
\tag{32.23}
$$

分别把 Dirac 旋量投影为第二十一章讨论的左旋与右旋 Weyl 分量。这一投影在讨论弱相互作用的手征结构时将反复使用。

自旋算符在标准表示下为

$$
\Sigma^i =
\begin{pmatrix}
\sigma_i & 0\\
0 & \sigma_i
\end{pmatrix}.
\tag{32.24}
$$

【推导】$\Sigma^i/2$ 与第二十一章 (21.20) 中的 $J_i$ 一致，生成 Dirac 旋量空间中的空间旋转。自由 Dirac 粒子的自旋算符为 $\vec S=\frac{1}{2}\vec\Sigma$（自然单位制下 $\hbar=1$），其本征值为 $\pm1/2$，这正是自旋 $1/2$ 的代数体现。

### （六）Lorentz 协变性与 S 矩阵

Dirac 方程 (32.6) 写出来之后，一个自然的问题是：它在洛伦兹变换下是否协变？具体地说，设 $x'^\mu={\Lambda^\mu}_{\ \nu}x^\nu$，在新坐标系中方程应当写为 $(i\gamma^\mu\partial'_\mu-m)\psi'(x')=0$。$\psi$ 与 $\psi'$ 之间必须存在一个 $4\times4$ 矩阵 $S(\Lambda)$，使得

$$
\psi'(x') = S(\Lambda)\,\psi(x).
\tag{32.24a}
$$

【推导】协变性要求 $S(\Lambda)$ 满足

$$
S^{-1}(\Lambda)\,\gamma^\mu\,S(\Lambda) = {\Lambda^\mu}_{\ \nu}\gamma^\nu.
\tag{32.24b}
$$

式 (32.24b) 的含义是：在旋量空间中作相似变换 $S$，等价于在矢量指标上作洛伦兹变换 $\Lambda$。由 (32.24b) 可直接验证协变性：

$$
i\gamma^\mu\partial'_\mu\psi'(x')
= i\gamma^\mu{\Lambda_\mu}^{\ \nu}\partial_\nu\,S\psi(x).
\tag{32.24c}
$$

用 (32.24b) 把 $\gamma^\mu{\Lambda_\mu}^{\ \nu}=S\gamma^\nu S^{-1}$ 代入：

$$
i\gamma^\mu{\Lambda_\mu}^{\ \nu}\partial_\nu S\psi
= iS\gamma^\nu S^{-1}S\,\partial_\nu\psi
= S(i\gamma^\nu\partial_\nu\psi)
= Sm\psi = m\,\psi'(x').
\tag{32.24d}
$$

末一步用了原坐标系中的 Dirac 方程。于是 $\psi'(x')$ 满足同样形式的方程，协变成立。【推导】

$S(\Lambda)$ 的显式构造由第二十一章的生成元给出。对无穷小洛伦兹变换 $\Lambda^\mu_{\ \nu}=\delta^\mu_{\ \nu}+\omega^\mu_{\ \nu}$，其中 $\omega_{\mu\nu}=-\omega_{\nu\mu}$，取

$$
S(\Lambda) = 1 - \tfrac{i}{4}\omega_{\mu\nu}\sigma^{\mu\nu},
\qquad
\sigma^{\mu\nu} = \tfrac{i}{2}[\gamma^\mu,\gamma^\nu].
\tag{32.24e}
$$

【推导】把 (32.24e) 代入 (32.24b) 左端，展开到 $\omega$ 的一阶：

$$
S^{-1}\gamma^\rho S \approx \gamma^\rho + \tfrac{i}{4}\omega_{\mu\nu}[\sigma^{\mu\nu},\gamma^\rho].
\tag{32.24f}
$$

利用 $[\sigma^{\mu\nu},\gamma^\rho]=2i(g^{\rho\nu}\gamma^\mu-g^{\rho\mu}\gamma^\nu)$（由 (32.11) 直接化简可得），代入得

$$
S^{-1}\gamma^\rho S = \gamma^\rho - \omega^{\rho}_{\ \nu}\gamma^\nu,
\tag{32.24g}
$$

与 (32.24b) 右端 ${\Lambda^\rho}_{\ \nu}\gamma^\nu=(\delta^\rho_{\ \nu}+\omega^\rho_{\ \nu})\gamma^\nu$ 一致。【推导】这一对号说明 $\sigma^{\mu\nu}$ 正是 Dirac 旋量空间中洛伦兹群的生成元，与第二十章的矢量生成元 $\omega^\mu_{\ \nu}$ 通过 $\gamma$ 矩阵联系起来。

## 五、Clifford 代数的基本恒等式

### （一）迹恒等式

$\gamma$ 矩阵的乘积迹在费曼图计算中频繁出现。几个常用恒等式如下。由 (32.11) 可证

$$
\mathrm{tr}(\gamma^\mu) = 0,
\qquad
\mathrm{tr}(\gamma^\mu\gamma^\nu) = 4g^{\mu\nu},
\tag{32.25}
$$

其中 $\mathrm{tr}$ 表示矩阵迹。【推导】前一式证明如下：$\gamma^\mu=-\gamma^5\gamma^\mu\gamma^5$（因为 $\gamma^5$ 与 $\gamma^\mu$ 反对易），故 $\mathrm{tr}(\gamma^\mu)=-\mathrm{tr}(\gamma^5\gamma^\mu\gamma^5)=-\mathrm{tr}(\gamma^\mu\gamma^5\gamma^5)=-\mathrm{tr}(\gamma^\mu)$，从而为零。后一式由 (32.11)：$\gamma^\mu\gamma^\nu+\gamma^\nu\gamma^\mu=2g^{\mu\nu}I_4$，取迹得 $2\mathrm{tr}(\gamma^\mu\gamma^\nu)=8g^{\mu\nu}$。

四个 $\gamma$ 矩阵乘积的迹为

$$
\mathrm{tr}(\gamma^\mu\gamma^\nu\gamma^\rho\gamma^\sigma)
= 4\left(g^{\mu\nu}g^{\rho\sigma}-g^{\mu\rho}g^{\nu\sigma}+g^{\mu\sigma}g^{\nu\rho}\right).
\tag{32.26}
$$

【推导】式 (32.26) 由反复使用 (32.11) 把相邻两个 $\gamma$ 对换为常数加反对易项得到，最终所有反对易项的迹因奇数个 $\gamma$ 而消失，剩下 (32.26) 的三项组合。这一恒等式在第四十三章计算费曼振幅时将直接引用。

### （二）缩并恒等式

在计算中常需要把相邻两个指标缩并。由 (32.11) 直接得

$$
\gamma_\mu\gamma^\mu = 4I_4,
\tag{32.27}
$$

因为 $\gamma_\mu\gamma^\mu=g_{\mu\nu}\gamma^\nu\gamma^\mu=\frac{1}{2}g_{\mu\nu}\{\gamma^\nu,\gamma^\mu\}=g_{\mu\nu}g^{\nu\mu}=4$。类似地，

$$
\gamma_\mu\gamma^\rho\gamma^\mu = -2\gamma^\rho.
\tag{32.28}
$$

【推导】把 $\gamma^\rho$ 用反对易关系移到中间：$\gamma_\mu\gamma^\rho\gamma^\mu=(2g_\mu^{\ \rho}-\gamma^\rho\gamma_\mu)\gamma^\mu=2\gamma^\rho-\gamma^\rho(\gamma_\mu\gamma^\mu)=2\gamma^\rho-4\gamma^\rho=-2\gamma^\rho$。这一符号因子 $-2$ 是 Dirac 迹计算中最容易出错的地方，使用时需逐次核对。

## 六、质壳因式分解的求导验证

### （一）因式分解的核心恒等式

本章最关键的代数恒等式是

$$
(\gamma^\mu p_\mu - m)(\gamma^\nu p_\nu + m) = p_\rho p^\rho - m^2.
\tag{32.29}
$$

【推导】展开左端：

$$
(\gamma^\mu p_\mu)(\gamma^\nu p_\nu) + m\gamma^\mu p_\mu - m\gamma^\nu p_\nu - m^2.
\tag{32.30}
$$

含 $m$ 的线性项互相抵消（展开式中两处同名求和项合并为 $m\gamma^\mu p_\mu-m\gamma^\nu p_\nu=0$）。剩下

$$
\gamma^\mu\gamma^\nu p_\mu p_\nu - m^2.
\tag{32.31}
$$

由于 $p_\mu p_\nu$ 对 $\mu,\nu$ 对称，$\gamma^\mu\gamma^\nu$ 中只有对称部分贡献：

$$
\gamma^\mu\gamma^\nu p_\mu p_\nu
= \frac{1}{2}\{\gamma^\mu,\gamma^\nu\}p_\mu p_\nu
= g^{\mu\nu}p_\mu p_\nu = p_\rho p^\rho.
\tag{32.32}
$$

代入 (32.31) 即得 (32.29)。【推导】

### （二）与二阶方程的等价性

式 (32.29) 说明：Dirac 算符 $\not p-m$（其中 $\not p\equiv\gamma^\mu p_\mu$ 的标准记号）乘以 $\not p+m$，恰好等于质壳算符 $p^2-m^2$。这正是第三节一阶化的代数核心。

反过来，若 $\psi$ 满足 Dirac 方程

$$
(\not p - m)\psi = 0,
\tag{32.33}
$$

那么两边左乘 $(\not p+m)$，由 (32.29) 得

$$
(p^2-m^2)\psi = 0.
\tag{32.34}
$$

即 Dirac 方程的解自动满足质壳关系。这保证了 Dirac 粒子的能量—动量关系与狭义相对论一致，不会偏离第三章的运动学框架。【推导】

### （三）因式分解的物理意义

式 (32.29) 的物理含义值得细究。Klein—Gordon 方程把 $p^2-m^2=0$ 当作一个不可分解的二阶约束，而 Dirac 方程把它"打开"为两个一阶因子的乘积。这一打开不是平凡的代数游戏：它使得概率密度可以写为 $\bar\psi\gamma^\mu\psi$（下一章详细推导），而非 Klein—Gordon 方程中的 $\phi^*\partial_t\phi-\phi\,\partial_t\phi^*$ 型组合。概率密度从"含时间导数"变为"不含时间导数"，正是一阶方程解决负概率困难的代数根源。

从本书统一主方程的角度看，(32.29) 还说明了一件事：自旋 $1/2$ 粒子的场方程与自旋 $0$ 粒子的场方程共用同一个二阶质壳算符 $p^2-m^2$，差别只在于 Dirac 方程把这个二阶算符因式分解到了旋量空间上。这与第五章"诸场共用同一二阶协变算符"的论断一致，只是 Dirac 场额外携带了旋量指标。

## 七、数值例题

### （一）题设

取一个静止系中的电子，四动量 $p^\mu=(m,0,0,0)$，其中电子质量 $m=0.511\ \mathrm{MeV}$（自然单位制）。直接计算 $\not p=\gamma^\mu p_\mu=\gamma^0 m$，并验证

$$
(\not p-m)(\not p+m) = p^2-m^2 = 0.
\tag{32.35}
$$

### （二）计算 $\not p-m$ 与 $\not p+m$

在标准表示 (32.12) 下，$\gamma^0 m=m\cdot\mathrm{diag}(1,1,-1,-1)$。因此

$$
\not p - m =
m\begin{pmatrix}
1 & 0 & 0 & 0\\
0 & 1 & 0 & 0\\
0 & 0 & -1 & 0\\
0 & 0 & 0 & -1
\end{pmatrix}
-
m\begin{pmatrix}
1 & 0 & 0 & 0\\
0 & 1 & 0 & 0\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1
\end{pmatrix}
=
m\begin{pmatrix}
0 & 0 & 0 & 0\\
0 & 0 & 0 & 0\\
0 & 0 & -2 & 0\\
0 & 0 & 0 & -2
\end{pmatrix}.
\tag{32.36}
$$

类似地，

$$
\not p + m =
m\begin{pmatrix}
2 & 0 & 0 & 0\\
0 & 2 & 0 & 0\\
0 & 0 & 0 & 0\\
0 & 0 & 0 & 0
\end{pmatrix}.
\tag{32.37}
$$

### （三）乘积验证

把 (32.36) 与 (32.37) 相乘。注意 (32.36) 只在第 $3,4$ 行非零，(32.37) 只在第 $1,2$ 列非零，两者的行与列不重叠：

$$
(\not p-m)(\not p+m) =
m^2
\begin{pmatrix}
0 & 0 & 0 & 0\\
0 & 0 & 0 & 0\\
0 & 0 & -2 & 0\\
0 & 0 & 0 & -2
\end{pmatrix}
\begin{pmatrix}
2 & 0 & 0 & 0\\
0 & 2 & 0 & 0\\
0 & 0 & 0 & 0\\
0 & 0 & 0 & 0
\end{pmatrix}
= 0.
\tag{32.38}
$$

另一方面，$p^2=p_\mu p^\mu=m^2$，故 $p^2-m^2=0$。两者严格相等，数值验证了 (32.29)。【推导】

### （四）非静止系的验算

再取一个沿 $x$ 方向运动的电子，$\beta=0.6$，$\gamma=1.25$。四动量 $p^\mu=(\gamma m,\gamma m\beta,0,0)=(1.25m,0.75m,0,0)$。计算

$$
\not p = \gamma^0(1.25m) - \gamma^1(0.75m).
\tag{32.39}
$$

由 (32.12)，$\gamma^1=\begin{pmatrix}0&\sigma_1\\-\sigma_1&0\end{pmatrix}$，$\sigma_1=\begin{pmatrix}0&1\\1&0\end{pmatrix}$。代入：

$$
\not p = m\begin{pmatrix}
1.25I_2 & -0.75\sigma_1\\
+0.75\sigma_1 & -1.25I_2
\end{pmatrix}.
\tag{32.40}
$$

计算 $\not p^{\,2}$：

$$
\not p^{\,2} = m^2
\begin{pmatrix}
1.25I_2 & -0.75\sigma_1\\
0.75\sigma_1 & -1.25I_2
\end{pmatrix}^2.
\tag{32.41}
$$

左上块：$(1.25)^2I_2+(-0.75)(0.75)\sigma_1^2=1.5625I_2-0.5625I_2=1.0I_2$。右下块同理。非对角块互相抵消。因此

$$
\not p^{\,2}=m^2 I_4.
\tag{32.42}
$$

质壳给出 $p^2=(\gamma m)^2-(\gamma\beta m)^2=\gamma^2m^2(1-\beta^2)=m^2$。$\not p^{\,2}=p^2I_4$，与 (32.29) 一致。【推导】这组数字还顺带验证了第三章的 $\gamma^2(1-\beta^2)=1$：$\gamma=1.25$，$1-\beta^2=0.64$，$\gamma^2(1-\beta^2)=1.5625\times0.64=1.0$。

### （五）量纲核对

在自然单位制下所有量纲为 $1$，恢复单位时需要核对。$m=0.511\ \mathrm{MeV}$ 是能量单位，$\not p=\gamma^\mu p_\mu$ 中 $p_\mu$ 的量纲也是能量，故 $\not p$ 量纲为能量，与 $m$ 相减有量纲意义。若恢复 $\hbar=c=1$ 以外的单位，则 Dirac 方程应写为 $i\gamma^\mu\hbar\partial_\mu\psi-mc\,\psi=0$ 或等价地 $i\gamma^\mu\partial_\mu\psi-\frac{mc}{\hbar}\psi=0$，与第二十一章 (21.22) 一致。本章为简洁起见统一用自然单位，读者在实际计算带电粒子在电磁场中的问题时，可按此替换恢复单位。

## 八、本章小结

本章从 Klein—Gordon 方程的两个困境（负概率与负能解）出发，引入 Dirac 的一阶化假设 (32.6)。为了让一阶方程的解自动满足质壳关系，$\gamma$ 矩阵必须满足 Clifford 代数 (32.11)。在标准表示 (32.12) 下，通过 (32.13)、(32.16)、(32.20) 三组直接验算，确认该表示确实满足反对易条件。由此导出的迹恒等式 (32.25)、(32.26) 与缩并恒等式 (32.27)、(32.28) 是后续量子场论计算的代数工具。

本章最核心的结果是质壳因式分解 (32.29)：$(\not p-m)(\not p+m)=p^2-m^2$。这一等式把二阶质壳约束打开为两个一阶算符的乘积，既是 Dirac 方程与 Klein—Gordon 方程之间的桥梁，也是概率密度从含时间导数变为不含时间导数的代数根源。数值例题在静止系与 $\beta=0.6$ 运动系两种情形下分别验证了这一恒等式，矩阵乘法逐项展开，结果与质壳关系严格吻合。

至此，Dirac 方程的代数骨架已经搭好：方程 (32.6) 写下来了，$\gamma$ 矩阵的显式形式给出了，质壳因式分解验证完毕。下一章将求解这个自由方程：构造平面波解 $u(p)e^{-ipx}$ 与 $v(p)e^{ipx}$，给出旋量归一化，推导概率流 $j^\mu=\bar\psi\gamma^\mu\psi$ 的守恒，并在非相对论极限下还原 Pauli 方程，从而把 Dirac 方程与第三章的相对论运动学、第二十一章的自旋 $1/2$ 表示正式对接。

> **本章分层占比**：已证实 30% / 推导 70% / 假说 0%（合计100%）
