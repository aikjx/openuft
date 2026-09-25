# 附录 E 公式推导补编

> 本附录把正书五处关键推导的完整中间步骤补编成册。每条注明对应的正书公式编号。
> 所有推导均属【推导】层；凡引用标准物理结论处标注【已证实】。

## E.1 dγ/dv 的链式法则三步（对应正书 (3.6)）

**正书结论**：$\dfrac{d\gamma}{dv}=\dfrac{\gamma^3 v}{c^2}$，其中 $\gamma(v)=(1-\beta^2)^{-1/2}$，$\beta=v/c$。

第一步：引入中间函数。令

$$f(v)=1-\frac{v^2}{c^2},\qquad \gamma=f^{-1/2}.$$

对 $f$ 关于 $v$ 求导：

$$\frac{df}{dv}=-\frac{2v}{c^2}. \tag{E.1.1}$$

第二步：幂函数求导。把 $\gamma=f^{-1/2}$ 视作 $f$ 的函数，由幂函数求导公式 $d(x^\alpha)/dx=\alpha x^{\alpha-1}$，

$$\frac{d\gamma}{df}=-\frac{1}{2}f^{-3/2}. \tag{E.1.2}$$

第三步：链式法则相乘。

$$\frac{d\gamma}{dv}=\frac{d\gamma}{df}\cdot\frac{df}{dv}=\left(-\frac{1}{2}f^{-3/2}\right)\left(-\frac{2v}{c^2}\right)=\frac{v}{c^2}f^{-3/2}. \tag{E.1.3}$$

由于 $f^{-1/2}=\gamma$，故 $f^{-3/2}=(f^{-1/2})^3=\gamma^3$，代入得

$$\frac{d\gamma}{dv}=\frac{\gamma^3 v}{c^2}. \tag{E.1.4}$$

数值核对（对应正书 (3.7)–(3.9)）：取 $\beta=0.6$，$\gamma=1/\sqrt{1-0.36}=1/0.8=1.25$，$\gamma^3=1.953125$，故 $d\gamma/dv=1.953125\times0.6/c=1.171875/c\approx3.909\times10^{-9}\ \mathrm{s/m}$。

## E.2 质壳因式分解 $(\not p-m)(\not p+m)=p^2-m^2$（对应正书 (32.29)）

**正书结论**：Dirac 算符 $\not p=\gamma^\mu p_\mu$ 满足

$$(\not p-m)(\not p+m)=p_\rho p^\rho-m^2. \tag{E.2.0}$$

第一步：展开乘积。

$$(\not p-m)(\not p+m)=(\gamma^\mu p_\mu)(\gamma^\nu p_\nu)+m\gamma^\mu p_\mu-m\gamma^\nu p_\nu-m^2. \tag{E.2.1}$$

第二步：线性项相消。含 $m$ 的两项 $m\gamma^\mu p_\mu-m\gamma^\nu p_\nu$ 中，$\mu,\nu$ 都是哑指标，合并后为 $m\gamma^\mu p_\mu-m\gamma^\mu p_\mu=0$。剩下

$$(\not p-m)(\not p+m)=\gamma^\mu\gamma^\nu p_\mu p_\nu-m^2. \tag{E.2.2}$$

第三步：利用 $p_\mu p_\nu$ 对 $\mu,\nu$ 对称。

$$\gamma^\mu\gamma^\nu p_\mu p_\nu=\frac{1}{2}(\gamma^\mu\gamma^\nu+\gamma^\nu\gamma^\mu)p_\mu p_\nu=\frac{1}{2}\{\gamma^\mu,\gamma^\nu\}p_\mu p_\nu. \tag{E.2.3}$$

第四步：代入 Clifford 代数 $\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}$（正书 (32.11)）：

$$\frac{1}{2}\{\gamma^\mu,\gamma^\nu\}p_\mu p_\nu=g^{\mu\nu}p_\mu p_\nu=p_\rho p^\rho. \tag{E.2.4}$$

第五步：代回。

$$(\not p-m)(\not p+m)=p_\rho p^\rho-m^2. \tag{E.2.5}$$

推论：若 $\psi$ 满足 Dirac 方程 $(\not p-m)\psi=0$，则左乘 $(\not p+m)$ 得 $(p^2-m^2)\psi=0$，即 Dirac 解自动满足质壳关系（正书 (32.34)）。

## E.3 Larmor 积分 $\int\sin^2\theta\,d\Omega=8\pi/3$（对应正书 (31.17)–(31.18)）

**正书结论**：偶极辐射的角分布为 $\propto\sin^2\theta$，对全立体角积分得 $8\pi/3$。

第一步：写出立体角元。在球坐标中 $d\Omega=\sin\theta\,d\theta\,d\phi$。

第二步：分离 $\phi$ 积分。被积函数 $\sin^2\theta$ 与 $\phi$ 无关，

$$\int\sin^2\theta\,d\Omega=\int_0^{2\pi}d\phi\int_0^\pi\sin^2\theta\,\sin\theta\,d\theta=2\pi\int_0^\pi\sin^3\theta\,d\theta. \tag{E.3.1}$$

第三步：计算 $\int_0^\pi\sin^3\theta\,d\theta$。用 $\sin^3\theta=\sin\theta(1-\cos^2\theta)$，令 $u=\cos\theta$，$du=-\sin\theta\,d\theta$：

$$\int_0^\pi\sin^3\theta\,d\theta=\int_{-1}^{1}(1-u^2)\,du=\left[u-\frac{u^3}{3}\right]_{-1}^{1}=\frac{4}{3}. \tag{E.3.2}$$

第四步：合并。

$$\int\sin^2\theta\,d\Omega=2\pi\cdot\frac{4}{3}=\frac{8\pi}{3}. \tag{E.3.3}$$

与 Larmor 公式的衔接（正书 (31.21)）：远场坡印廷矢量大小为

$$\langle S\rangle=\frac{|\ddot{\vec p}(t_r)|^2}{16\pi^2\varepsilon_0 c^3 R^2}\sin^2\theta. \tag{E.3.4}$$

对半径 $R$ 的球面积分：

$$P=\int\langle S\rangle R^2 d\Omega=\frac{|\ddot p|^2}{16\pi^2\varepsilon_0 c^3}\cdot\frac{8\pi}{3}=\frac{|\ddot p|^2}{6\pi\varepsilon_0 c^3}. \tag{E.3.5}$$

对点电荷 $\ddot p=q\vec a$，即得 Larmor 公式 $P=q^2a^2/(6\pi\varepsilon_0 c^3)$。系数 $1/(6\pi)$ 完全来自立体角积分 $8\pi/3$ 与远场 $1/(4\pi)^2$ 的乘积。

## E.4 霍金温度从 Bogoliubov 变换的推导骨架（对应正书 (50.13)–(50.15)）

**正书结论**：史瓦西黑洞霍金温度 $T_H=\kappa/(2\pi k_B)$，其中 $\kappa$ 为表面引力。

第一步：视界附近的 Rindler 近似。史瓦西度规在视界 $r=r_s=2GM/c^2$ 附近展开。令 $r=r_s+\rho$，$\rho\ll r_s$，度规近似为 Rindler 形式

$$ds^2\approx-(c^2\kappa^2\rho^2/c^2)dt^2+d\rho^2, \tag{E.4.1}$$

其中表面引力 $\kappa=c^4/(4GM)$（史瓦西情形）。

第二步：Rindler 真空与惯性真空的 Bogoliubov 变换。自由标量场在惯性坐标系（Minkowski）下的正频模式 $f_k^{\rm M}$ 与 Rindler 坐标系下的正频模式 $f_k^{\rm R}$ 之间由 Bogoliubov 变换联系：

$$f_k^{\rm M}=\sum_{k'}(\alpha_{kk'} f_{k'}^{\rm R}+\beta_{kk'} f_{k'}^{\rm R*}). \tag{E.4.2}$$

第三步：Wald 定理。对 Rindler 观测者，Bogoliubov 系数满足 $|\alpha|^2-|\beta|^2=1$，且热谱条件要求

$$|\beta_{kk'}|^2/|\alpha_{kk'}|^2=e^{-2\pi\omega/\kappa}. \tag{E.4.3}$$

这一指数比正是 Bose-Einstein 分布 $1/(e^{\hbar\omega/k_BT}-1)$ 的形式。

第四步：读出温度。比较 $e^{-2\pi\omega/\kappa}=e^{-\hbar\omega/(k_B T_H)}$，得

$$\frac{2\pi\omega}{\kappa}=\frac{\hbar\omega}{k_B T_H}\quad\Longrightarrow\quad T_H=\frac{\hbar\kappa}{2\pi k_B}. \tag{E.4.4}$$

自然单位下（$\hbar=k_B=1$）即 $T_H=\kappa/(2\pi)$。对史瓦西黑洞 $\kappa=c^4/(4GM)$，故

$$T_H=\frac{\hbar c^3}{8\pi GM k_B}. \tag{E.4.5}$$

数值核对：取 $M=M_\odot$，$T_H\approx6.17\times10^{-8}\ \mathrm{K}$，远低于宇宙微波背景 $2.7\ \mathrm{K}$，故恒星质量黑洞当前净吸积而非净蒸发。

Bekenstein-Hawking 熵（正书 (50.13)）：由热力学第一定律 $dM=T_H\,dS_{\rm BH}$，积分得 $S_{\rm BH}=k_B c^3A/(4\hbar G)$，其中 $A=4\pi r_s^2$ 为视界面积。系数 $1/4$ 由 Bogoliubov 热谱斜率严格定出，不可从量纲分析猜出。

## E.5 TUFT 主方程 $\kappa\to0$ 极限（对应正书 (TUFT-32)、(TUFT-33)、(TUFT-45)、(TUFT-46)）

TUFT 主方程（正书 (TUFT-32)）：

$$D_\mu\mathcal F^{\mu\nu}+\kappa(x)\mathcal J^\nu+\tau(x)\mathcal K^\nu=\mathcal S^\nu. \tag{E.5.1}$$

第一步：平直弱场极限 $\kappa\to0,\ \tau\to0$。此时 Frenet 标架退化为普通坐标架，分形协变导数 $D_\mu=\partial_\mu+\Gamma_\mu+\mathcal F_\mu$（TUFT-27）退回普通偏导 $\partial_\mu$，场张量 $\mathcal F^{\mu\nu}=\partial^\mu A^\nu-\partial^\nu A^\mu+G^{\mu\nu}$（TUFT-25）退回标准电磁场张量 $F_{\rm em}^{\mu\nu}=\partial^\mu A^\nu-\partial^\nu A^\mu$。

第二步：代入。主方程 (E.5.1) 变为

$$\partial_\mu F_{\rm em}^{\mu\nu}=\mathcal S^\nu. \tag{E.5.2}$$

这正是 Maxwell 方程的协变形式（正书 (TUFT-33)、(TUFT-45)）：$\mathcal S^\nu$ 即四维电流源。

第三步：进一步退到广义相对论。TUFT 修正的 Einstein 方程（TUFT-76）

$$R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}+\tau\mathcal G_{\mu\nu} \tag{E.5.3}$$

在 $\tau\to0$ 时退回

$$R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}, \tag{E.5.4}$$

即标准 Einstein 场方程（正书 (5.20)）。

第四步：自洽性核对。这一退化证明 TUFT 主方程不是与标准物理矛盾的新理论，而是在 $\kappa,\tau$ 小的区域把标准物理作为一阶近似包含进来。低能弱场实验只测量到 Maxwell 与 Einstein 的标准形式，正是因为 $\kappa\sim10^{-23}\ \mathrm{m^{-1}}$（地球表面）到 $\kappa\sim10^{-5}\ \mathrm{m^{-1}}$（恒星级黑洞视界外）的修正项远低于当前探测精度。

## E.6 洛伦兹 boost 矩阵的合成与逆元（对应正书 (3.11)–(3.14)、(52.3)–(52.7)）

**正书结论**：沿 $x$ 方向的纯 boost 矩阵

$$
\Lambda_x(\beta)=\begin{pmatrix}\gamma & -\gamma\beta & 0 & 0\\ -\gamma\beta & \gamma & 0 & 0\\ 0 & 0 & 1 & 0\\ 0 & 0 & 0 & 1\end{pmatrix} \tag{E.6.0}
$$

满足 $\Lambda_x(\beta)\Lambda_x(-\beta)=I$，且两个沿不同轴的 boost 合成一般伴随空间转动（Wigner 转动）。

第一步：验证逆元。把 $\beta$ 换成 $-\beta$，则 $\gamma(-\beta)=\gamma(\beta)=\gamma$（因 $\beta^2$ 不变），故

$$
\Lambda_x(-\beta)=\begin{pmatrix}\gamma & \gamma\beta & 0 & 0\\ \gamma\beta & \gamma & 0 & 0\\ 0 & 0 & 1 & 0\\ 0 & 0 & 0 & 1\end{pmatrix}. \tag{E.6.1}
$$

第二步：矩阵相乘。计算 $\Lambda_x(\beta)\Lambda_x(-\beta)$ 的左上角 $2\times2$ 块：

$$
\begin{pmatrix}\gamma & -\gamma\beta\\ -\gamma\beta & \gamma\end{pmatrix}
\begin{pmatrix}\gamma & \gamma\beta\\ \gamma\beta & \gamma\end{pmatrix}
=\begin{pmatrix}\gamma^2(1-\beta^2) & \gamma^2\beta(1-1)\\ \gamma^2\beta(1-1) & \gamma^2(1-\beta^2)\end{pmatrix}. \tag{E.6.2}
$$

由 $\gamma^2(1-\beta^2)=1$，结果恰为单位阵。

第三步：沿 $x$ 再沿 $y$ 的合成。先 $\Lambda_x(\beta_1)$ 再 $\Lambda_y(\beta_2)$：

$$
\Lambda_y(\beta_2)\Lambda_x(\beta_1)=
\begin{pmatrix}\gamma_1\gamma_2 & -\gamma_1\gamma_2\beta_1 & -\gamma_2\beta_2 & 0\\ -\gamma_1\beta_1 & \gamma_1 & 0 & 0\\ -\gamma_1\gamma_2\beta_2 & \gamma_1\gamma_2\beta_1\beta_2 & \gamma_2 & 0\\ 0 & 0 & 0 & 1\end{pmatrix}. \tag{E.6.3}
$$

把乘积倒过来 $\Lambda_x(\beta_1)\Lambda_y(\beta_2)$，二者在 $(2,3)$ 位置相差 $\gamma_1\gamma_2\beta_1\beta_2$。差矩阵对应的空间转动角

$$
\Omega\approx\beta_1\beta_2 \tag{E.6.4}
$$

（低速近似），这就是 Wigner 转动。它说明 boost 不构成阿贝尔子群，Poincaré 群的非阿贝尔结构由此而来（正书 (20.8)）。

数值核对：取 $\beta_1=\beta_2=0.1$，$\gamma\approx1.00504$，乘积中 $(2,3)$ 元为 $1.00504^2\times0.01\approx0.01010$，与 (E.6.4) 的 $\Omega=0.01$ 弧度在二阶精度内一致。SymPy 脚本见正书 (52.7)。

## E.7 四动量质壳平方的完整展开（对应正书 (3.21)、(5.15)、(52.11)）

**正书结论**：有质粒子的四动量 $p^\mu=(E/c,\vec p)$ 满足

$$
p_\mu p^\mu=\frac{E^2}{c^2}-\vec p^{\,2}=m^2c^2. \tag{E.7.0}
$$

第一步：代入 $E=\gamma mc^2$ 与 $\vec p=\gamma m\vec v$。这两条来自四速度 $u^\mu=\gamma(c,\vec v)$ 乘 $m$：$p^\mu=mu^\mu=(\gamma mc,\gamma m\vec v)$，故 $E/c=\gamma mc$，即 $E=\gamma mc^2$。

第二步：展开 $E^2/c^2$。

$$
\frac{E^2}{c^2}=\gamma^2 m^2 c^2. \tag{E.7.1}
$$

第三步：展开 $\vec p^{\,2}$。

$$
\vec p^{\,2}=\gamma^2 m^2 v^2. \tag{E.7.2}
$$

第四步：相减。

$$
p_\mu p^\mu=\gamma^2 m^2(c^2-v^2)=\gamma^2 m^2 c^2\left(1-\frac{v^2}{c^2}\right). \tag{E.7.3}
$$

第五步：用 $\gamma^2(1-\beta^2)=1$。

$$
p_\mu p^\mu=m^2c^2. \tag{E.7.4}
$$

推论：两边乘 $c^2$ 得 $E^2=p^2c^2+m^2c^4$，即正书 (3.21)。对无质量粒子令 $m=0$，得 $E=pc$。SymPy 复算见正书 (52.11)：令 $\beta=0.6$，$\gamma=1.25$，$p_\mu p^\mu=1.25^2 m^2(c^2-0.36c^2)=1.5625\times0.64\,m^2c^2=m^2c^2$，与解析式一致。

## E.8 Dirac 方程从 KG 方程的一阶因式分解（对应正书 (32.5)–(32.12)、(53.1)–(53.8)）

**正书结论**：Klein-Gordon 方程 $(\Box+\kappa^2)\psi=0$ 是二阶的，存在负能解与负概率密度困难。Dirac 要求把它分解为两个一阶方程的乘积

$$
(\gamma^\mu p_\mu-mc)(\gamma^\nu p_\nu+mc)\psi=0. \tag{E.8.0}
$$

第一步：把 KG 写成 $p_\mu p^\mu-m^2c^2/\hbar^2=0$。在自然单位 $\hbar=c=1$ 下即 $p^2-m^2=0$。

第二步：假设一阶因式分解。令

$$
p^2-m^2=(\gamma^\mu p_\mu-m)(\gamma^\nu p_\nu+m). \tag{E.8.1}
$$

右边展开（与 E.2 相同）得 $\gamma^\mu\gamma^\nu p_\mu p_\nu-m^2$。

第三步：要求恒等式成立。

$$
\gamma^\mu\gamma^\nu p_\mu p_\nu=p_\mu p^\mu=g^{\mu\nu}p_\mu p_\nu. \tag{E.8.2}
$$

第四步：利用 $p_\mu p_\nu$ 的对称性。$\gamma^\mu\gamma^\nu$ 的反对称部分乘 $p_\mu p_\nu$ 自动为零，故只需

$$
\frac12(\gamma^\mu\gamma^\nu+\gamma^\nu\gamma^\mu)=g^{\mu\nu}I_4. \tag{E.8.3}
$$

这就是 Clifford 代数 $\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}$（正书 (32.11)）。

第五步：读出 Dirac 方程。只要 $\psi$ 满足一阶方程 $(\gamma^\mu p_\mu-m)\psi=0$，它自动满足二阶 KG。把 $p_\mu=i\hbar\partial_\mu$ 换回微分算符，得

$$
i\hbar\gamma^\mu\partial_\mu\psi-mc\,\psi=0. \tag{E.8.4}
$$

第六步：$\gamma$ 矩阵的维数。Clifford 代数 (E.8.3) 在四维 Minkowski 时空中的最小不可约表示维数为 $4$，故 $\psi$ 为四分量旋量。这与第三十二章的构造一致。SymPy 对 (E.8.3) 的矩阵范数复算见正书 (53.8)。

## E.9 Yang-Mills 场强的 Bianchi 恒等式（对应正书 (35.18)–(35.21)、(53.15)）

**正书结论**：非阿贝尔场强

$$
F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu+g f^{abc}A^b_\mu A^c_\nu \tag{E.9.0}
$$

满足协变 Bianchi 恒等式

$$
D_{[\lambda}F^a_{\mu\nu]}=0. \tag{E.9.1}
$$

第一步：写出协变导数。$(D_\lambda F^a)_{\mu\nu}=\partial_\lambda F^a_{\mu\nu}+g f^{abc}A^b_\lambda F^c_{\mu\nu}$。

第二步：对 $\lambda,\mu,\nu$ 完全反对称化。(E.9.1) 展开为

$$
\partial_{[\lambda}F^a_{\mu\nu]}+g f^{abc}A^b_{[\lambda}F^c_{\mu\nu]}=0. \tag{E.9.2}
$$

第三步：先看线性部分。把 (E.9.0) 的线性项代入 $\partial_{[\lambda}F^a_{\mu\nu]}$：

$$
\partial_{[\lambda}\partial_\mu A^a_{\nu]}-\partial_{[\lambda}\partial_\nu A^a_{\mu]}=0, \tag{E.9.3}
$$

因为偏导可交换，三项循环求和后相消。这与 Maxwell 情形的 Bianchi 恒等式 $\partial_{[\lambda}F_{\mu\nu]}=0$ 相同。

第四步：看二次项与联络项。(E.9.0) 中的二次项 $g f^{abc}A^b_\mu A^c_\nu$ 代入 $\partial_{[\lambda}$，得到

$$
g f^{abc}\partial_{[\lambda}(A^b_\mu A^c_{\nu]}). \tag{E.9.4}
$$

与 (E.9.2) 第二项合并后，剩三次项

$$
g^2 f^{abc}f^{cde}A^b_{[\lambda}A^d_\mu A^e_{\nu]}. \tag{E.9.5}
$$

第五步：用 Jacobi 恒等式。李代数结构常数满足

$$
f^{abc}f^{cde}+f^{adc}f^{ceb}+f^{aec}f^{cbd}=0. \tag{E.9.6}
$$

对 $\lambda,\mu,\nu$ 完全反对称化后，(E.9.5) 的三项两两配对相消，最终为零。这就证明了 (E.9.1)。

与 Maxwell 的对比：U(1) 情形 $f^{abc}=0$，Bianchi 恒等式退化为纯偏导形式，自动成立。非阿贝尔情形多出的联络项与三次项相互抵消，本质是 Jacobi 恒等式在起作用。SymPy 符号复算见正书 (53.15)。

## E.10 Higgs 机制的质量生成（对应正书 (37.14)–(37.22)）

**正书结论**：复标量场 $\phi$ 与 $SU(2)$ 规范场 $W^a_\mu$ 的耦合中，当势 $V(\phi)$ 在 $\phi\neq0$ 处取最小值时，规范玻色子通过吃掉 Goldstone 模获得质量。

第一步：写出势与真空。取

$$
V(\phi)=\mu^2\phi^\dagger\phi+\lambda(\phi^\dagger\phi)^2,\qquad \mu^2<0,\ \lambda>0. \tag{E.10.0}
$$

$\partial V/\partial(\phi^\dagger\phi)=0$ 给出 $|\phi_0|^2=-\mu^2/(2\lambda)\equiv v^2/2$，故真空期望值 $\langle\phi\rangle=(0,v/\sqrt{2})^T$。

第二步：绕真空展开。写

$$
\phi(x)=\frac{1}{\sqrt{2}}\begin{pmatrix}\phi_1+i\phi_2\\ v+h(x)+i\phi_3\end{pmatrix}. \tag{E.10.1}
$$

$\phi_{1,2,3}$ 为 Goldstone 模，$h$ 为物理 Higgs 粒子。

第三步：代入协变导数。$D_\mu=\partial_\mu-i g\tau^a W^a_\mu/2-i g' B_\mu/2$。动能项 $|D_\mu\phi|^2$ 在真空展开后含

$$
\left|-\frac{i g}{2}\tau^a W^a_\mu\frac{v}{\sqrt{2}}\right|^2=\frac{g^2 v^2}{8}W^a_\mu W^{a\mu}. \tag{E.10.2}
$$

第四步：组合到物理质量本征态。定义

$$
W^\pm_\mu=\frac{1}{\sqrt{2}}(W^1_\mu\mp iW^2_\mu),\quad
Z_\mu=\frac{-g' B_\mu+g W^3_\mu}{\sqrt{g^2+g'^2}},\quad
A_\mu=\frac{g B_\mu+g' W^3_\mu}{\sqrt{g^2+g'^2}}. \tag{E.10.3}
$$

代入 (E.10.2) 得

$$
\frac{g^2v^2}{4}W^+_\mu W^{-\mu}+\frac{(g^2+g'^2)v^2}{8}Z_\mu Z^\mu. \tag{E.10.4}
$$

与有质量矢量场拉氏量 $-\frac14 F^2+\frac12 m^2 V_\mu V^\mu$ 比较，读出

$$
m_W=\frac{gv}{2},\qquad m_Z=\frac{v}{2}\sqrt{g^2+g'^2}=\frac{m_W}{\cos\theta_W},\qquad m_A=0. \tag{E.10.5}
$$

第五步：Goldstone 模的去向。$\phi_{1,2,3}$ 在单位制规范下被 $W^\pm,Z$ "吃掉"，成为它们的纵向极化分量；光子 $A_\mu$ 无质量，因为 $U(1)_{\rm em}$ 未破缺。这就是 2012 年 LHC 上 ATLAS 与 CMS 共同观测到的 $125\ \mathrm{GeV}$ Higgs 玻色子的机制（正书 (62.28)）。

## E.11 霍金温度 Bogoliubov 模式函数的完整比对（对应正书 (50.13)–(50.18)）

E.4 已给出温度 $T_H=\hbar\kappa/(2\pi k_B)$ 的骨架。本条补出模式函数层面的关键一步，使读者可独立验算指数比 $|\beta/\alpha|^2=e^{-2\pi\omega/\kappa}$ 的来源。

第一步：Rindler 度规。令 $\rho$ 为距视界的固有距离，$\eta$ 为 Rindler 时间，度规

$$
ds^2=-(\kappa\rho)^2d\eta^2+d\rho^2. \tag{E.11.0}
$$

自由标量场方程在 Rindler 坐标下为

$$
\left[-\frac{1}{(\kappa\rho)^2}\partial_\eta^2+\partial_\rho^2+\frac{1}{\rho}\partial_\rho\right]f_\omega^{\rm R}(\rho,\eta)=0. \tag{E.11.1}
$$

第二步：分离变量。设 $f_\omega^{\rm R}=e^{-i\omega\eta}\,R_\omega(\rho)$，径向方程

$$
\rho^2 R''+\rho R'+\frac{\omega^2}{\kappa^2}R=0. \tag{E.11.2}
$$

这是欧拉方程，解为 $R_\omega\propto\rho^{\pm i\omega/\kappa}$。

第三步：Minkowski 正频模式的解析延拓。在惯性坐标 $(t,x)$ 中，Minkowski 正频模式 $e^{-i\omega(t+x)}$ 对应 Rindler 坐标下的组合。关键一步是把 $t+x$ 在复平面上做解析延拓：越过视界时 $t+x$ 取复值

$$
t+x=\rho\,e^{i\theta},\qquad \theta\in[0,2\pi). \tag{E.11.3}
$$

绕视界一周，相位增加 $2\pi$，而 $R_\omega\propto\rho^{i\omega/\kappa}$ 乘上 $e^{i\omega/\kappa\cdot 2\pi}=e^{2\pi\omega/\kappa}$。

第四步：读出 Bogoliubov 系数比。Minkowski 模式在 Rindler 左右楔片中分别展开为

$$
f_\omega^{\rm M}=\alpha\,f_\omega^{\rm R}+\beta\,(f_\omega^{\rm R})^*. \tag{E.11.4}
$$

解析延拓一周给出两个楔片系数的相对相位

$$
\frac{\beta}{\alpha}=-e^{-\pi\omega/\kappa}. \tag{E.11.5}
$$

第五步：热谱。$|\alpha|^2-|\beta|^2=1$ 与 (E.11.5) 联立，得

$$
|\beta|^2=\frac{1}{e^{2\pi\omega/\kappa}-1}. \tag{E.11.6}
$$

这正是 Bose-Einstein 分布，比较 $e^{2\pi\omega/\kappa}=e^{\hbar\omega/k_BT_H}$ 即得 $T_H=\hbar\kappa/(2\pi k_B)$。关键：指数 $2\pi/\kappa$ 完全来自 Rindler 径向方程的幂指数 $i\omega/\kappa$ 与解析延拓一圈的相位 $2\pi$，量纲分析无法猜出。

## E.12 TUFT 主方程的 Bianchi 缩并与源守恒（对应正书 (TUFT-25)、(TUFT-32)、(42.18)）

【TUFT假说】以下推导在 TUFT 原创场张量定义下进行，凡引用标准 Bianchi 恒等式处仍标【推导】。

TUFT 场张量（正书 (TUFT-25)）：

$$
\mathcal F^{\mu\nu}=\partial^\mu\mathcal A^\nu-\partial^\nu\mathcal A^\mu+G^{\mu\nu}, \tag{E.12.0}
$$

其中 $G^{\mu\nu}$ 为分形修正项。TUFT 主方程（正书 (TUFT-32)）为

$$
D_\mu\mathcal F^{\mu\nu}+\kappa(x)\mathcal J^\nu+\tau(x)\mathcal K^\nu=\mathcal S^\nu. \tag{E.12.1}
$$

第一步：对 (E.12.1) 取 $\partial_\nu$。

$$
\partial_\nu D_\mu\mathcal F^{\mu\nu}+\partial_\nu(\kappa\mathcal J^\nu+\tau\mathcal K^\nu-\mathcal S^\nu)=0. \tag{E.12.2}
$$

第二步：协变 Bianchi 恒等式。在标准 Yang-Mills 情形（E.9），$D_\mu F^{\mu\nu}$ 的完全反对称协变导数为零。TUFT 把联络推广为 $\mathcal F_\mu$（正书 (TUFT-27)），Bianchi 恒等式相应推广为

$$
D_\nu D_\mu\mathcal F^{\mu\nu}=0. \tag{E.12.3}
$$

这一步在【TUFT假说】层作为公理引入，其合理性由 $\kappa\to0$ 退回标准 Yang-Mills Bianchi 恒等式验证。

第三步：代入 (E.12.2)，第一项消失，剩

$$
\partial_\nu(\kappa\mathcal J^\nu+\tau\mathcal K^\nu-\mathcal S^\nu)=0. \tag{E.12.4}
$$

第四步：物理诠释。(E.12.4) 是 TUFT 框架下推广的电荷守恒律。当 $\tau\to0$、$\kappa$ 为常数时，它退回标准的 $\partial_\nu\mathcal J^\nu=0$（正书 (5.18)）。当 $\kappa(x)$ 为空间变量时，额外出现 $\mathcal J^\nu\partial_\nu\kappa$ 项，这正是 TUFT 预言在分形基底上电荷不严格守恒的数学来源（正书 (42.18)）。

第五步：低能退化核对。地球表面 $\kappa\sim10^{-23}\ \mathrm{m^{-1}}$，$\partial_\nu\kappa/\kappa$ 的相对量级在实验室尺度下小于 $10^{-20}$，远低于当前电荷守恒检验精度（$10^{-21}$，来自质子寿命约束）。这与第四十七章给出的 P-TUFT 约束区间自洽。

## E.13 P-TUFT 可证伪条件的数学表述（对应正书 (47.9)、(64.1)–(64.6)）

【TUFT假说】本条把第四十七章给出的五条可证伪预言写成可计算的统计判据。

第一步：以 P-TUFT-1 为例。第六十四章 (64.1) 给出四偏振叠加

$$
h_{\rm GW}(t)=A_+h_+(t)+A_\times h_\times(t)+A_Sh_S(t)+A_Vh_V(t). \tag{E.13.0}
$$

GR 预言 $A_S=A_V=0$；TUFT 预言在 $\tau\neq0$ 时 $A_S,A_V$ 非零。

第二步：似然比。设事件数据 $d$，GR 假设 $\mathcal H_0$ 与 TUFT 假设 $\mathcal H_1$ 的似然分别为

$$
p(d|\mathcal H_0)=\int d\theta\,p(\theta)\,p(d|\theta,A_S=A_V=0), \tag{E.13.1}
$$

$$
p(d|\mathcal H_1)=\int d\theta\,p(\theta)\,p(d|\theta,A_S,A_V). \tag{E.13.2}
$$

Bayes 因子 $B_{10}=p(d|\mathcal H_1)/p(d|\mathcal H_0)$。

第三步：可证伪判据。若在 SNR $\geq20$ 的 $N$ 个并合事件联合分析中，90% 置信区间

$$
\log B_{10}\subset[-1,1] \tag{E.13.3}
$$

与零相容，则 P-TUFT-1 被证伪。理由：$\tau$ 量级在第六十四章先验估计为 $10^{-17}\ \mathrm{m^{-1}}$，对应 $A_S/A_+\sim\tau r_s$，对恒星级黑洞约 $3\times10^{-13}$；LIGO 第五次运行设计灵敏度在 $250\ \mathrm{Hz}$ 处可分辨 $10^{-30}$ 应变残差，足够把 $3\times10^{-13}$ 量级的偏振泄漏与噪声分开。

第四步：其余四条预言的同型判据。P-TUFT-2 在超导临界温度 $T_c$ 以下高阶模频率偏移 $\Delta\omega/\omega$ 的 $5\sigma$ 检验；P-TUFT-3 在对撞机微分截面尾部 $|p_T|^{-n}$ 指数 $n$ 的偏差超过 QCD 误差棒；P-TUFT-4 在大尺度结构功率谱对数斜率 $d\ln P(k)/d\ln k$ 偏离 Harrison-Zel'dovich 标度不变谱 $n_s=0.965$ 超过 Planck 2018 误差棒 $0.004$；P-TUFT-5 在黑洞铃宕 ringdown 中检测到第四种偏振。每条判据都写成"观测量 ± 误差棒"形式，使实验家可直接套用。

## E.14 小结

本附录补编的十三条推导分别对应：相对论运动学骨架（E.1、E.6、E.7）、Dirac 方程代数骨架（E.2、E.8）、经典辐射理论（E.3）、规范场与电弱对称破缺（E.9、E.10）、黑洞热力学（E.4、E.11）、TUFT 低能退化与 Bianchi 缩并（E.5、E.12）、可证伪判据（E.13）。每条推导的中间步骤均可独立验算；与正书编号的一一对应保证读者可在正书对应段落找到上下文。
