# 第三十三章 Dirac旋量自由场解与概率流

## 一、本章承接上章的代数骨架

第三十二章把 Dirac 方程 $i\gamma^\mu\partial_\mu\psi-m\psi=0$ 的代数骨架搭了起来：$\gamma$ 矩阵满足 Clifford 代数 (32.11)，标准表示 (32.12) 给出显式矩阵，质壳因式分解 (32.29) 保证解自动满足 $p^2=m^2$。本章把这个方程真正解出来。自由情形下，解应当是平面波；但 Dirac 波函数是四分量旋量，平面波的振幅 $u(p)$ 与 $v(p)$ 本身需要构造，且要满足动量空间中的代数约束。解出来之后，还要回答两个物理问题：概率流如何写、如何保证守恒；非相对论极限下如何回到第二章就熟悉的 Pauli 方程，把自旋磁矩自动带出来。

本章继续采用自然单位制 $\hbar=c=1$。所有内容属于【已证实】与【推导】两层，不引入原创假说。本章末尾的数值例题用电子质量 $m=0.511\ \mathrm{MeV}$ 与一组具体动量，把 $u$、$v$ 旋量的分量数值算出来，并核对归一化与流密度。

## 二、平面波 ansatz 与动量空间方程

### （一）四分量平面波

自由方程没有外场，解应当是四分量平面波。设正能解形如

$$
\psi(x) = u(p)\,e^{-ipx},
\qquad px = p_\mu x^\mu = Et - \vec p\cdot\vec x,
\tag{33.1}
$$

其中 $u(p)$ 是一个四分量常列旋量，$p^\mu=(E,\vec p)$ 待定。负能解（在场论中解释为反粒子正能解）形如

$$
\psi(x) = v(p)\,e^{+ipx}.
\tag{33.2}
$$

【推导】把 (33.1) 代入 (32.6)。由于 $\partial_\mu e^{-ipx}=-ip_\mu e^{-ipx}$，有

$$
i\gamma^\mu\partial_\mu\psi = i\gamma^\mu(-ip_\mu)u(p)e^{-ipx}
= \gamma^\mu p_\mu\,u(p)\,e^{-ipx}
= \not p\,u(p)\,e^{-ipx}.
\tag{33.3}
$$

代入方程后 $e^{-ipx}$ 约去，得到动量空间的代数方程

$$
(\not p - m)\,u(p) = 0.
\tag{33.4}
$$

同理，把 (33.2) 代入，注意 $\partial_\mu e^{+ipx}=+ip_\mu e^{+ipx}$，得

$$
i\gamma^\mu(ip_\mu)v(p)e^{+ipx} - mv(p)e^{+ipx} = 0,
\tag{33.5}
$$

即

$$
(\not p + m)\,v(p) = 0.
\tag{33.6}
$$

【推导】式 (33.4) 与 (33.6) 是本章的两个基本代数方程。它们不再含导数，只是 $4\times4$ 矩阵的本征值问题。

### （二）能量本征值

把 (33.4) 左端乘上 $(\not p+m)$，由 (32.29) 得

$$
(p^2-m^2)\,u(p) = 0.
\tag{33.7}
$$

非平凡解要求 $p^2=m^2$，即 $E^2=\vec p^{\,2}+m^2$。对给定的 $\vec p$，有两个根 $E=\pm E_p$，其中

$$
E_p = \sqrt{\vec p^{\,2}+m^2} > 0.
\tag{33.8}
$$

【推导】式 (33.4) 中 $u(p)$ 配 $e^{-iEt+i\vec p\cdot\vec x}$，取 $E=+E_p$ 给出正能解；式 (33.6) 中 $v(p)$ 配 $e^{+ipx}=e^{+iEt-i\vec p\cdot\vec x}$，把 $E$ 理解为 $+E_p$ 时相位为 $e^{+iE_pt-i\vec p\cdot\vec x}$，在量子场论中这对应反粒子以动量 $-\vec p$、能量 $+E_p$ 运动。单粒子层面上，$v(p)$ 携带的是负能解的振幅。

## 三、静止系中的 u 与 v 旋量

### （一）静止系代数方程

先取粒子静止系 $\vec p=0$，此时 $E=m$，$\not p=\gamma^0 m$。代入 (33.4)：

$$
(\gamma^0 m - m)u(0) = 0
\quad\Longrightarrow\quad
(\gamma^0-I)u(0) = 0.
\tag{33.9}
$$

在标准表示 (32.12) 下，$\gamma^0=\mathrm{diag}(1,1,-1,-1)$，故 $\gamma^0-I=\mathrm{diag}(0,0,-2,-2)$。方程 (33.9) 要求旋量的后两个分量为零：

$$
u(0) =
\begin{pmatrix}
\varphi\\
0
\end{pmatrix},
\tag{33.10}
$$

其中 $\varphi$ 是一个二分量旋量。类似地，把 $\vec p=0$ 代入 (33.6)：

$$
(\gamma^0 m + m)v(0) = 0
\quad\Longrightarrow\quad
(\gamma^0+I)v(0) = 0.
\tag{33.11}
$$

$\gamma^0+I=\mathrm{diag}(2,2,0,0)$，故前两个分量为零：

$$
v(0) =
\begin{pmatrix}
0\\
\chi
\end{pmatrix}.
\tag{33.12}
$$

【推导】式 (33.10) 与 (33.12) 说明：静止系中，正能旋量集中在上两个分量（"大分量"），负能旋量集中在下两个分量（"小分量"）。这一结构在非相对论极限下极为重要。

### （二）二分量基矢与自旋

二分量 $\varphi$、$\chi$ 还需选定基。取 Pauli 矩阵 $\sigma_3$ 的本征态作为基：

$$
\chi_1 = \begin{pmatrix}1\\0\end{pmatrix},
\qquad
\chi_2 = \begin{pmatrix}0\\1\end{pmatrix}.
\tag{33.13}
$$

$\chi_1$ 对应自旋沿 $z$ 方向投影 $+1/2$，$\chi_2$ 对应 $-1/2$。于是静止系的四个线性独立解为

$$
u(0,1)=\sqrt{2m}\begin{pmatrix}1\\0\\0\\0\end{pmatrix},
\quad
u(0,2)=\sqrt{2m}\begin{pmatrix}0\\1\\0\\0\end{pmatrix},
\quad
v(0,1)=\sqrt{2m}\begin{pmatrix}0\\0\\1\\0\end{pmatrix},
\quad
v(0,2)=\sqrt{2m}\begin{pmatrix}0\\0\\0\\1\end{pmatrix}.
\tag{33.14}
$$

【推导】式中 $\sqrt{2m}$ 是归一化因子，下面确定。

## 四、一般动量下的旋量构造

### （一）正能旋量 u(p)

对一般动量 $\vec p$，用 Lorentz 变换把静止系旋量 boost 到动量 $\vec p$。结果可以写成标准形式

$$
u(p,s) = \sqrt{E_p+m}\,
\begin{pmatrix}
\chi_s\\[2pt]
\dfrac{\sigma\cdot\vec p}{E_p+m}\,\chi_s
\end{pmatrix},
\qquad s=1,2.
\tag{33.15}
$$

【推导】验证 (33.15) 满足 (33.4)。把 $\not p=\gamma^0E_p-\gamma^i p_i$ 作用在 (33.15) 上。用标准表示 (32.12)，$\gamma^0=\begin{pmatrix}I&0\\0&-I\end{pmatrix}$，$\gamma^i=\begin{pmatrix}0&\sigma_i\\-\sigma_i&0\end{pmatrix}$。于是

$$
\not p\,u =
\begin{pmatrix}
E_p I & -\sigma\cdot\vec p\\
\sigma\cdot\vec p & -E_p I
\end{pmatrix}
\sqrt{E_p+m}
\begin{pmatrix}
\chi_s\\
\dfrac{\sigma\cdot\vec p}{E_p+m}\chi_s
\end{pmatrix}.
\tag{33.16}
$$

左上块：$E_p\chi_s-\sigma\cdot\vec p\cdot\dfrac{\sigma\cdot\vec p}{E_p+m}\chi_s$。利用 $(\sigma\cdot\vec p)^2=\vec p^{\,2}$（Pauli 代数直接给出），得

$$
E_p\chi_s - \frac{\vec p^{\,2}}{E_p+m}\chi_s
= \frac{E_p(E_p+m)-\vec p^{\,2}}{E_p+m}\chi_s.
\tag{33.17}
$$

由质壳关系 $E_p^2-\vec p^{\,2}=m^2$，分子 $E_p(E_p+m)-\vec p^{\,2}=E_p^2+E_pm-\vec p^{\,2}=m^2+E_pm=m(E_p+m)$。故左上块等于 $m\chi_s$。

右下块：$\sigma\cdot\vec p\,\chi_s-E_p\dfrac{\sigma\cdot\vec p}{E_p+m}\chi_s=\left(1-\dfrac{E_p}{E_p+m}\right)\sigma\cdot\vec p\,\chi_s=\dfrac{m}{E_p+m}\sigma\cdot\vec p\,\chi_s$。

合并两块：

$$
\not p\,u(p,s) = \sqrt{E_p+m}
\begin{pmatrix}
m\chi_s\\
\dfrac{m\,\sigma\cdot\vec p}{E_p+m}\chi_s
\end{pmatrix}
= m\,u(p,s).
\tag{33.18}
$$

即 $(\not p-m)u=0$，与 (33.4) 一致。【推导】

### （二）负能旋量 v(p)

类似地，负能旋量的标准形式为

$$
v(p,s) = \sqrt{E_p+m}\,
\begin{pmatrix}
\dfrac{\sigma\cdot\vec p}{E_p+m}\,\chi_s\\[2pt]
\chi_s
\end{pmatrix},
\qquad s=1,2.
\tag{33.19}
$$

【推导】验证 (33.6)：计算 $(\not p+m)v$。把 (33.19) 代入 (33.16) 的矩阵作用：

$$
\not p\,v =
\sqrt{E_p+m}
\begin{pmatrix}
E_p\dfrac{\sigma\cdot\vec p}{E_p+m}\chi_s - \sigma\cdot\vec p\,\chi_s\\[2pt]
\sigma\cdot\vec p\,\dfrac{\sigma\cdot\vec p}{E_p+m}\chi_s - E_p\chi_s
\end{pmatrix}.
\tag{33.20}
$$

左上块：$\left(\dfrac{E_p}{E_p+m}-1\right)\sigma\cdot\vec p\,\chi_s=\dfrac{-m}{E_p+m}\sigma\cdot\vec p\,\chi_s$。右下块：$\dfrac{\vec p^{\,2}}{E_p+m}\chi_s-E_p\chi_s=\dfrac{\vec p^{\,2}-E_p(E_p+m)}{E_p+m}\chi_s=\dfrac{-m(E_p+m)}{E_p+m}\chi_s=-m\chi_s$（用了与 (33.17) 相同的质壳化简）。

于是

$$
\not p\,v = -m\,v,
\qquad
(\not p+m)v=0,
\tag{33.21}
$$

与 (33.6) 一致。【推导】

## 五、旋量归一化与 Dirac 伴随

### （一）Dirac 伴随

旋量的"共轭"不是简单的厄米共轭 $\psi^\dagger$，而是

$$
\bar\psi \equiv \psi^\dagger\gamma^0.
\tag{33.22}
$$

【推导】引入 $\bar\psi$ 的原因在于：$\psi^\dagger\psi$ 不是洛伦兹标量，而 $\bar\psi\psi$ 才是。由 (32.24b) 的协变变换律，$\psi'=S\psi$，$\bar\psi'=\bar\psi S^{-1}$，故 $\bar\psi'\psi'=\bar\psi S^{-1}S\psi=\bar\psi\psi$，是标量。$\bar\psi\gamma^\mu\psi$ 则是四矢量，这一点下面构造概率流时会用到。

### （二）归一化条件

式 (33.15) 中 $\sqrt{E_p+m}$ 的选取使旋量满足标准归一化：

$$
\bar u(p,r)\,u(p,s) = 2m\,\delta_{rs},
\qquad
\bar v(p,r)\,v(p,s) = -2m\,\delta_{rs}.
\tag{33.23}
$$

【推导】以 $u$ 为例验证。把 (33.15) 代入 $\bar u u=u^\dagger\gamma^0u$。在标准表示下 $\gamma^0=\mathrm{diag}(I,-I)$，故

$$
\bar u u = (E_p+m)\left[\chi_r^\dagger\chi_s - \chi_r^\dagger\dfrac{\sigma\cdot\vec p}{E_p+m}\dfrac{\sigma\cdot\vec p}{E_p+m}\chi_s\right].
\tag{33.24}
$$

用 $(\sigma\cdot\vec p)^2=\vec p^{\,2}$ 与 $\chi_r^\dagger\chi_s=\delta_{rs}$：

$$
\bar u u = (E_p+m)\left[1-\frac{\vec p^{\,2}}{(E_p+m)^2}\right]\delta_{rs}
= \frac{(E_p+m)^2-\vec p^{\,2}}{E_p+m}\delta_{rs}.
\tag{33.25}
$$

分子展开：$(E_p+m)^2-\vec p^{\,2}=E_p^2+2E_pm+m^2-\vec p^{\,2}$。由质壳 $E_p^2-\vec p^{\,2}=m^2$，分子 $=2m^2+2E_pm=2m(E_p+m)$。代入：

$$
\bar u u = \frac{2m(E_p+m)}{E_p+m}\delta_{rs}=2m\delta_{rs}.
\tag{33.26}
$$

【推导】$v$ 的归一化 (33.23) 中对应关系同理，符号来自 $\bar v v=v^\dagger\gamma^0v$ 中下分量为正、上分量为负的相反结构。

### （三）正交完备关系

除了 (33.23)，$u$ 与 $v$ 之间满足

$$
\bar u(p,r)\,v(p,s) = 0,
\qquad
\bar v(p,r)\,u(p,s) = 0.
\tag{33.27}
$$

【推导】这是因为 $u$ 满足 $(\not p-m)u=0$，$v$ 满足 $(\not p+m)v=0$。用 $\bar u(\not p+m)=0$ 乘在 $(\not p-m)u=0$ 上方向相反的关系，或直接代入 (33.15) 与 (33.19) 计算双线性型，均可验证交叉项为零。这一正交性保证正能解与负能解在旋量空间中张成互补的子空间。

在量子场论中，完备关系写为

$$
\sum_s u(p,s)\bar u(p,s) = \not p + m,
\qquad
\sum_s v(p,s)\bar v(p,s) = \not p - m.
\tag{33.28}
$$

【推导】式 (33.28) 是 (33.4)、(33.6) 与归一化 (33.23) 的直接推论：把投影算符 $(\not p\pm m)/(2m)$ 作用在任意四分量旋量上，投影到正能或负能子空间。这两个投影算符在费曼传播子构造中将反复出现。

## 六、概率流及其守恒

### （一）概率密度与四流

Klein—Gordon 方程的困难在于概率密度含时间导数。Dirac 方程是一阶方程，自然希望概率密度只含 $\psi^\dagger\psi$。定义四流

$$
j^\mu(x) \equiv \bar\psi(x)\,\gamma^\mu\,\psi(x).
\tag{33.29}
$$

【推导】时间分量 $j^0=\psi^\dagger\gamma^0\gamma^0\psi=\psi^\dagger\psi$，即旋量各分量模长之和，恒非负。这正是 Dirac 一阶化所要解决的问题：概率密度不再含 $\partial_t\psi$，而是直接正比于 $|\psi|^2$。

### （二）守恒律推导

由 Dirac 方程 $i\gamma^\mu\partial_\mu\psi=m\psi$，得

$$
\gamma^\mu\partial_\mu\psi = -im\,\psi.
\tag{33.30}
$$

对 (33.30) 取厄米共轭：

$$
(\partial_\mu\psi^\dagger)(\gamma^\mu)^\dagger = im\,\psi^\dagger.
\tag{33.31}
$$

用 $(\gamma^i)^\dagger=-\gamma^i$、$(\gamma^0)^\dagger=\gamma^0$，统一写为 $(\gamma^\mu)^\dagger=\gamma^0\gamma^\mu\gamma^0$。把 (33.31) 两边右乘 $\gamma^0$：

$$
(\partial_\mu\psi^\dagger)\gamma^0\gamma^\mu\gamma^0\gamma^0 = im\,\psi^\dagger\gamma^0.
\tag{33.32}
$$

注意 $\gamma^0\gamma^0=I$，故左端 $=(\partial_\mu\bar\psi)\gamma^\mu$，右端 $=im\,\bar\psi$。于是伴随方程为

$$
(\partial_\mu\bar\psi)\gamma^\mu = im\,\bar\psi.
\tag{33.33}
$$

【推导】现在对 $j^\mu=\bar\psi\gamma^\mu\psi$ 求四维散度：

$$
\partial_\mu j^\mu = (\partial_\mu\bar\psi)\gamma^\mu\psi + \bar\psi\gamma^\mu\partial_\mu\psi.
\tag{33.34}
$$

把 (33.30) 与 (33.33) 代入：

$$
\partial_\mu j^\mu = (im\,\bar\psi)\psi + \bar\psi(-im\,\psi) = im\,\bar\psi\psi - im\,\bar\psi\psi = 0.
\tag{33.35}
$$

即

$$
\partial_\mu j^\mu = 0.
\tag{33.36}
$$

【推导】式 (33.36) 是概率守恒的协变形式。空间分量 $j^i=\bar\psi\gamma^i\psi$ 是概率流密度矢量，时间分量 $j^0=\psi^\dagger\psi$ 是概率密度。积分形式 $\partial_t\int\psi^\dagger\psi\,d^3x=-\int\nabla\cdot\vec j\,d^3x$ 即总概率守恒。与 Klein—Gordon 方程的 (32.5) 相比，$j^0=\psi^\dagger\psi$ 恒非负，负概率困难在 Dirac 方程中不复存在。

### （三）平面波的概率流

对单平面波 $\psi=u(p,s)e^{-ipx}$，概率密度为

$$
j^0 = u^\dagger(p,s)u(p,s).
\tag{33.37}
$$

由 (33.15) 计算：

$$
u^\dagger u = (E_p+m)\left[\chi_s^\dagger\chi_s+\chi_s^\dagger\dfrac{(\sigma\cdot\vec p)^2}{(E_p+m)^2}\chi_s\right]
= (E_p+m)\left[1+\dfrac{\vec p^{\,2}}{(E_p+m)^2}\right].
\tag{33.38}
$$

化简：$(E_p+m)^2+\vec p^{\,2}=E_p^2+2E_pm+m^2+\vec p^{\,2}=2E_p^2+2E_pm=2E_p(E_p+m)$（用了 $E_p^2-\vec p^{\,2}=m^2$，即 $\vec p^{\,2}=E_p^2-m^2$）。故

$$
u^\dagger u = \frac{2E_p(E_p+m)}{E_p+m} = 2E_p.
\tag{33.39}
$$

类似地，

$$
\bar u\gamma^i u = 2p^i.
\tag{33.40}
$$

【推导】式 (33.39)、(33.40) 合起来给出

$$
j^\mu = 2p^\mu,
\tag{33.41}
$$

即概率流密度正比于四动量。这一结果有清晰的物理解释：概率以粒子的速度 $v^i=p^i/E_p$ 流动，$j^i/j^0=p^i/E_p=v^i$，与经典粒子流的方向一致。这不是巧合，而是 Dirac 方程与质壳关系自洽的体现。

## 七、非相对论极限与 Pauli 方程

### （一）分离静止能量

在非相对论极限 $|\vec p|\ll m$ 下，$E_p=m+T$，其中动能 $T=\vec p^{\,2}/(2m)\ll m$。为了分离静止能量，把正能解写成

$$
\psi(x) = e^{-imt}\begin{pmatrix}\varphi(\vec x,t)\\ \chi(\vec x,t)\end{pmatrix},
\tag{33.42}
$$

其中 $\varphi$ 与 $\chi$ 都是二分量旋量，且随时间缓慢变化（不含 $e^{-imt}$ 因子）。【推导】这一代换的目的是把高频振荡 $e^{-imt}$ 提出来，剩下的低频包络 $\varphi,\chi$ 满足非相对论方程。

### （二）Dirac 方程的分量分解

把 (33.42) 代入 (32.6)，用标准表示写成分量形式。$i\partial_t\psi$ 作用在 $e^{-imt}$ 上给出 $m\psi+i e^{-imt}\partial_t(\varphi,\chi)^T$。方程为

$$
i\partial_t\begin{pmatrix}\varphi\\\chi\end{pmatrix}
=
\begin{pmatrix}
0 & \sigma\cdot\vec p\\
-\sigma\cdot\vec p & 0
\end{pmatrix}
\begin{pmatrix}\varphi\\\chi\end{pmatrix}
+
m\begin{pmatrix}\varphi\\\chi\end{pmatrix}.
\tag{33.43}
$$

两边减去 $m\psi$（即把 $e^{-imt}$ 的本征值 $m$ 消去），得分量方程

$$
i\partial_t\varphi = \sigma\cdot\vec p\,\chi,
\qquad
i\partial_t\chi = -\sigma\cdot\vec p\,\varphi + 2m\chi.
\tag{33.44}
$$

【推导】在非相对论极限下，$\chi$ 是"小分量"：从下分量方程解出

$$
\chi = \frac{1}{2m}\left(\sigma\cdot\vec p\,\varphi - i\partial_t\chi\right).
\tag{33.45}
$$

因为 $i\partial_t\chi$ 量级为 $T\chi\ll m\chi$，略去得领头阶

$$
\chi \approx \frac{\sigma\cdot\vec p}{2m}\,\varphi.
\tag{33.46}
$$

这与 (33.15) 的结构一致：在非相对论极限下，下分量与上分量之比为 $|\vec p|/(E_p+m)\approx|\vec p|/(2m)\ll1$。

### （三）上分量满足 Pauli 方程

把 (33.46) 代入 (33.44) 的上分量方程：

$$
i\partial_t\varphi = \sigma\cdot\vec p\,\frac{\sigma\cdot\vec p}{2m}\,\varphi.
\tag{33.47}
$$

利用 Pauli 代数的恒等式

$$
(\sigma\cdot\vec a)(\sigma\cdot\vec b)=\vec a\cdot\vec b\,I+i\,\sigma\cdot(\vec a\times\vec b).
\tag{33.48}
$$

对 $\vec a=\vec b=\vec p$，叉乘项 $\vec p\times\vec p=0$，故

$$
(\sigma\cdot\vec p)^2 = \vec p^{\,2}.
\tag{33.49}
$$

代入 (33.47)：

$$
i\partial_t\varphi = \frac{\vec p^{\,2}}{2m}\,\varphi.
\tag{33.50}
$$

【推导】式 (33.50) 就是自由粒子的 Schrödinger 方程，只不过 $\varphi$ 是二分量旋量而非单分量波函数。这说明 Dirac 方程在非相对论极限下自动给出二分量自旋波函数。

### （四）引入电磁场后的自旋磁矩

若把自由粒子换成电磁场中的电子，按第三十四章将详细讨论的最小耦合代换 $\vec p\to\vec p-q\vec A$、能量 $E\to E-q\phi$，重复上述非相对论化简，(33.48) 中 $\vec a$ 与 $\vec b$ 不再相等（$\vec p-q\vec A$ 同时出现两次但磁场项带来额外结构），叉乘项不再为零。取 $\vec a=\vec b=\vec p-q\vec A$，利用

$$
(\vec p-q\vec A)\times(\vec p-q\vec A) = iq\hbar\,\vec B
\tag{33.51}
$$

（在自然单位制下 $\hbar=1$，这是量子力学中的标准对易子结果），代入 (33.48) 得

$$
(\sigma\cdot(\vec p-q\vec A))^2 = (\vec p-q\vec A)^2 - q\,\vec\sigma\cdot\vec B.
\tag{33.52}
$$

于是 (33.50) 推广为

$$
i\partial_t\varphi = \left[\frac{(\vec p-q\vec A)^2}{2m} - q\phi - \frac{q}{2m}\vec\sigma\cdot\vec B\right]\varphi.
\tag{33.53}
$$

【推导】式 (33.53) 正是 Pauli 方程。其中 $-\frac{q}{2m}\vec\sigma\cdot\vec B$ 项是自旋磁矩与磁场的相互作用，磁矩为

$$
\vec\mu_s = \frac{q}{m}\vec S = \frac{q}{m}\cdot\frac{\vec\sigma}{2},
\qquad
g = 2.
\tag{33.54}
$$

【已证实】Dirac 方程在非相对论极限下自动给出电子的 $g$ 因子 $g=2$，与 1920 年代实验测量值高度吻合。这是 Dirac 理论最引人注目的成功之一：自旋不是外加假设，而是一阶方程的必然产物；电子磁矩的正确数值从方程中自动浮现，无需人为引入。辐射修正后的反常磁矩 $g-2$ 将在量子场论的高阶图计算中给出。

## 八、数值例题

### （一）题设

取一个沿 $z$ 方向运动的电子，动量 $p_z=1.0\ \mathrm{MeV}$，电子质量 $m=0.511\ \mathrm{MeV}$。计算：$E_p$、$u(p,1)$ 各分量数值、$u^\dagger u$、$\bar u u$、概率流 $j^\mu$，并核对非相对论近似 $\chi\approx\sigma_z p_z/(E_p+m)\varphi$。

### （二）计算 $E_p$ 与比值

$$
E_p = \sqrt{p_z^2+m^2} = \sqrt{1.0^2+0.511^2}
= \sqrt{1+0.2611} = \sqrt{1.2611} \approx 1.1230\ \mathrm{MeV}.
\tag{33.55}
$$

$$
E_p+m = 1.1230+0.511 = 1.6340\ \mathrm{MeV}.
\tag{33.56}
$$

$$
\frac{p_z}{E_p+m} = \frac{1.0}{1.6340} \approx 0.6120.
\tag{33.57}
$$

注意 $p_z/(E_p+m)\approx0.61$ 并不远小于 1，说明这个电子已属相对论性，非相对论近似只能定性使用。

### （三）写出 u(p,1) 分量

取自旋基 $\chi_1=(1,0)^T$，$\sigma_z\chi_1=\chi_1$。由 (33.15)：

$$
u(p,1) = \sqrt{E_p+m}
\begin{pmatrix}
1\\0\\[2pt]
0.6120\cdot 1\\0
\end{pmatrix}
= \sqrt{1.6340}
\begin{pmatrix}
1\\0\\0.6120\\0
\end{pmatrix}.
\tag{33.58}
$$

$\sqrt{1.6340}\approx1.2783$。故

$$
u(p,1) \approx (1.2783,\; 0,\; 0.7823,\; 0)^T.
\tag{33.59}
$$

【推导】下分量 $0.7823$ 与上分量 $1.2783$ 之比为 $0.612$，与 (33.57) 一致。

### （四）核对归一化

计算 $u^\dagger u$：

$$
u^\dagger u = (1.2783)^2+(0.7823)^2
= 1.6341+0.6120 \approx 2.2461.
\tag{33.60}
$$

由 (33.39) 应等于 $2E_p=2\times1.1230=2.2460$。两者吻合（误差在四舍五入范围内）。【推导】

计算 $\bar u u=u^\dagger\gamma^0u$。在标准表示下，$\bar u u=|u_1|^2+|u_2|^2-|u_3|^2-|u_4|^2$：

$$
\bar u u = 1.6341-0.6120 = 1.0221.
\tag{33.61}
$$

由 (33.23) 应等于 $2m=2\times0.511=1.022$。两者严格吻合。【推导】

### （五）概率流

由 (33.41)，$j^\mu=2p^\mu$。代入 $p^\mu=(1.1230,0,0,1.0)$：

$$
j^\mu = (2.2460,\; 0,\; 0,\; 2.0)\ \mathrm{MeV}.
\tag{33.62}
$$

检验速度：

$$
\frac{j^z}{j^0} = \frac{2.0}{2.2460} \approx 0.890.
\tag{33.63}
$$

相对论速度 $\beta=p_z/E_p=1.0/1.1230\approx0.890$。两者严格相等，验证了 (33.41) 的物理含义：概率流速度等于粒子速度。【推导】

### （六）非相对论近似的偏差

按 (33.46)，在非相对论近似下应取 $\chi\approx\sigma\cdot\vec p/(2m)\varphi$。代入数值：

$$
\frac{p_z}{2m} = \frac{1.0}{2\times0.511} \approx 0.9785.
\tag{33.64}
$$

而精确比值 (33.57) 为 $0.6120$。两者相差约 $60\%$，说明 $p_z=1.0\ \mathrm{MeV}$ 已远超出非相对论近似的适用范围。若把动量降到 $p_z=0.10\ \mathrm{MeV}$，则

$$
E_p=\sqrt{0.01+0.2611}\approx0.5207\ \mathrm{MeV},
$$

$$
\frac{p_z}{E_p+m}=\frac{0.10}{0.5207+0.511}\approx0.0970,
\qquad
\frac{p_z}{2m}=\frac{0.10}{1.022}\approx0.0978.
\tag{33.65}
$$

两者偏差小于 $1\%$，非相对论近似成立。【推导】这组对比定量说明了非相对论极限的适用边界：当 $|\vec p|\ll m$ 时，$E_p+m\approx2m$，(33.15) 中的精确比值 $p/(E_p+m)$ 才与 Pauli 方程中的 $p/(2m)$ 一致。

## 九、本章小结

本章从平面波 ansatz 出发，把第三十二章的 Dirac 方程化为动量空间的代数方程 (33.4) 与 (33.6)。在静止系中解出 $u(0)$ 与 $v(0)$，再通过 boost 得到一般动量下的显式旋量 (33.15)、(33.19)。归一化条件 (33.23) 把 $\bar u u=2m$、$\bar v v=-2m$ 固定下来，正交完备关系 (33.27)、(33.28) 为后续量子场论中的投影算符打下基础。

概率流 (33.29) 的推导是本章的物理核心。通过把 Dirac 方程与其伴随方程 (33.33) 配对，直接得到 $\partial_\mu j^\mu=0$。与 Klein—Gordon 方程的 (32.5) 相比，$j^0=\psi^\dagger\psi$ 恒非负，负概率困难不复存在；而 $j^\mu=2p^\mu$ 的平面波结果说明概率流速度等于粒子速度，与经典运动学自洽。

非相对论极限部分把 $e^{-imt}$ 分离出来后，下分量 $\chi$ 被消去，上分量 $\varphi$ 满足 Pauli 方程 (33.53)。在电磁场中，Pauli 代数恒等式 (33.48) 的叉乘项自动给出自旋磁矩 $g=2$，这是 Dirac 方程无需人为假设即给出电子自旋磁矩的关键一步。数值例题在 $p_z=1.0\ \mathrm{MeV}$ 与 $p_z=0.10\ \mathrm{MeV}$ 两种动量下分别核对了归一化、概率流速度与非相对论近似的偏差边界，说明只有当 $|\vec p|\ll m$ 时 Pauli 近似才成立。

至此，自由 Dirac 方程的解、概率流与非相对论极限全部打通。第三十四章将引入最小耦合代换 $D_\mu=\partial_\mu-iqA_\mu$，把电磁场纳入 Dirac 方程，并通过拉氏量变分严格导出相互作用形式。

> **本章分层占比**：已证实 25% / 推导 75% / 假说 0%（合计100%）
