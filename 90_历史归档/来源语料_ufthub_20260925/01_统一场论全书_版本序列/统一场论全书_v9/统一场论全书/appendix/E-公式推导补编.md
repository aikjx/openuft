# 附录 E 公式推导补编

> 本附录把正书五处关键推导的完整中间步骤补编成册。每条注明对应的正书公式编号。
> 所有推导均属【推导】层；凡引用标准物理结论处标注【已证实】。

## E.1 dγ/dv 的链式法则三步（对应正书 (3.6)）

**正书结论**：$\dfrac{d\gamma}{dv}=\dfrac{\gamma^3 v}{c^2}$，其中 $\gamma(v)=(1-\beta^2)^{-1/2}$，$\beta=v/c$。

**第一步：引入中间函数**。令

$$f(v)=1-\frac{v^2}{c^2},\qquad \gamma=f^{-1/2}.$$

对 $f$ 关于 $v$ 求导：

$$\frac{df}{dv}=-\frac{2v}{c^2}. \tag{E.1.1}$$

**第二步：幂函数求导**。把 $\gamma=f^{-1/2}$ 视作 $f$ 的函数，由幂函数求导公式 $d(x^\alpha)/dx=\alpha x^{\alpha-1}$，

$$\frac{d\gamma}{df}=-\frac{1}{2}f^{-3/2}. \tag{E.1.2}$$

**第三步：链式法则相乘**。

$$\frac{d\gamma}{dv}=\frac{d\gamma}{df}\cdot\frac{df}{dv}=\left(-\frac{1}{2}f^{-3/2}\right)\left(-\frac{2v}{c^2}\right)=\frac{v}{c^2}f^{-3/2}. \tag{E.1.3}$$

由于 $f^{-1/2}=\gamma$，故 $f^{-3/2}=(f^{-1/2})^3=\gamma^3$，代入得

$$\frac{d\gamma}{dv}=\frac{\gamma^3 v}{c^2}. \tag{E.1.4}$$

**数值核对**（对应正书 (3.7)–(3.9)）：取 $\beta=0.6$，$\gamma=1/\sqrt{1-0.36}=1/0.8=1.25$，$\gamma^3=1.953125$，故 $d\gamma/dv=1.953125\times0.6/c=1.171875/c\approx3.909\times10^{-9}\ \mathrm{s/m}$。

## E.2 质壳因式分解 $(\not p-m)(\not p+m)=p^2-m^2$（对应正书 (32.29)）

**正书结论**：Dirac 算符 $\not p=\gamma^\mu p_\mu$ 满足

$$(\not p-m)(\not p+m)=p_\rho p^\rho-m^2. \tag{E.2.0}$$

**第一步：展开乘积**。

$$(\not p-m)(\not p+m)=(\gamma^\mu p_\mu)(\gamma^\nu p_\nu)+m\gamma^\mu p_\mu-m\gamma^\nu p_\nu-m^2. \tag{E.2.1}$$

**第二步：线性项相消**。含 $m$ 的两项 $m\gamma^\mu p_\mu-m\gamma^\nu p_\nu$ 中，$\mu,\nu$ 都是哑指标，合并后为 $m\gamma^\mu p_\mu-m\gamma^\mu p_\mu=0$。剩下

$$(\not p-m)(\not p+m)=\gamma^\mu\gamma^\nu p_\mu p_\nu-m^2. \tag{E.2.2}$$

**第三步：利用 $p_\mu p_\nu$ 对 $\mu,\nu$ 对称**。

$$\gamma^\mu\gamma^\nu p_\mu p_\nu=\frac{1}{2}(\gamma^\mu\gamma^\nu+\gamma^\nu\gamma^\mu)p_\mu p_\nu=\frac{1}{2}\{\gamma^\mu,\gamma^\nu\}p_\mu p_\nu. \tag{E.2.3}$$

**第四步：代入 Clifford 代数** $\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}$（正书 (32.11)）：

$$\frac{1}{2}\{\gamma^\mu,\gamma^\nu\}p_\mu p_\nu=g^{\mu\nu}p_\mu p_\nu=p_\rho p^\rho. \tag{E.2.4}$$

**第五步：代回**。

$$(\not p-m)(\not p+m)=p_\rho p^\rho-m^2. \tag{E.2.5}$$

**推论**：若 $\psi$ 满足 Dirac 方程 $(\not p-m)\psi=0$，则左乘 $(\not p+m)$ 得 $(p^2-m^2)\psi=0$，即 Dirac 解自动满足质壳关系（正书 (32.34)）。

## E.3 Larmor 积分 $\int\sin^2\theta\,d\Omega=8\pi/3$（对应正书 (31.17)–(31.18)）

**正书结论**：偶极辐射的角分布为 $\propto\sin^2\theta$，对全立体角积分得 $8\pi/3$。

**第一步：写出立体角元**。在球坐标中 $d\Omega=\sin\theta\,d\theta\,d\phi$。

**第二步：分离 $\phi$ 积分**。被积函数 $\sin^2\theta$ 与 $\phi$ 无关，

$$\int\sin^2\theta\,d\Omega=\int_0^{2\pi}d\phi\int_0^\pi\sin^2\theta\,\sin\theta\,d\theta=2\pi\int_0^\pi\sin^3\theta\,d\theta. \tag{E.3.1}$$

**第三步：计算 $\int_0^\pi\sin^3\theta\,d\theta$**。用 $\sin^3\theta=\sin\theta(1-\cos^2\theta)$，令 $u=\cos\theta$，$du=-\sin\theta\,d\theta$：

$$\int_0^\pi\sin^3\theta\,d\theta=\int_{-1}^{1}(1-u^2)\,du=\left[u-\frac{u^3}{3}\right]_{-1}^{1}=\frac{4}{3}. \tag{E.3.2}$$

**第四步：合并**。

$$\int\sin^2\theta\,d\Omega=2\pi\cdot\frac{4}{3}=\frac{8\pi}{3}. \tag{E.3.3}$$

**与 Larmor 公式的衔接**（正书 (31.21)）：远场坡印廷矢量大小为

$$\langle S\rangle=\frac{|\ddot{\vec p}(t_r)|^2}{16\pi^2\varepsilon_0 c^3 R^2}\sin^2\theta. \tag{E.3.4}$$

对半径 $R$ 的球面积分：

$$P=\int\langle S\rangle R^2 d\Omega=\frac{|\ddot p|^2}{16\pi^2\varepsilon_0 c^3}\cdot\frac{8\pi}{3}=\frac{|\ddot p|^2}{6\pi\varepsilon_0 c^3}. \tag{E.3.5}$$

对点电荷 $\ddot p=q\vec a$，即得 Larmor 公式 $P=q^2a^2/(6\pi\varepsilon_0 c^3)$。系数 $1/(6\pi)$ 完全来自立体角积分 $8\pi/3$ 与远场 $1/(4\pi)^2$ 的乘积。

## E.4 霍金温度从 Bogoliubov 变换的推导骨架（对应正书 (50.13)–(50.15)）

**正书结论**：史瓦西黑洞霍金温度 $T_H=\kappa/(2\pi k_B)$，其中 $\kappa$ 为表面引力。

**第一步：视界附近的 Rindler 近似**。史瓦西度规在视界 $r=r_s=2GM/c^2$ 附近展开。令 $r=r_s+\rho$，$\rho\ll r_s$，度规近似为 Rindler 形式

$$ds^2\approx-(c^2\kappa^2\rho^2/c^2)dt^2+d\rho^2, \tag{E.4.1}$$

其中表面引力 $\kappa=c^4/(4GM)$（史瓦西情形）。

**第二步：Rindler 真空与惯性真空的 Bogoliubov 变换**。自由标量场在惯性坐标系（Minkowski）下的正频模式 $f_k^{\rm M}$ 与 Rindler 坐标系下的正频模式 $f_k^{\rm R}$ 之间由 Bogoliubov 变换联系：

$$f_k^{\rm M}=\sum_{k'}(\alpha_{kk'} f_{k'}^{\rm R}+\beta_{kk'} f_{k'}^{\rm R*}). \tag{E.4.2}$$

**第三步：Wald 定理**。对 Rindler 观测者，Bogoliubov 系数满足 $|\alpha|^2-|\beta|^2=1$，且热谱条件要求

$$|\beta_{kk'}|^2/|\alpha_{kk'}|^2=e^{-2\pi\omega/\kappa}. \tag{E.4.3}$$

这一指数比正是 Bose-Einstein 分布 $1/(e^{\hbar\omega/k_BT}-1)$ 的形式。

**第四步：读出温度**。比较 $e^{-2\pi\omega/\kappa}=e^{-\hbar\omega/(k_B T_H)}$，得

$$\frac{2\pi\omega}{\kappa}=\frac{\hbar\omega}{k_B T_H}\quad\Longrightarrow\quad T_H=\frac{\hbar\kappa}{2\pi k_B}. \tag{E.4.4}$$

自然单位下（$\hbar=k_B=1$）即 $T_H=\kappa/(2\pi)$。对史瓦西黑洞 $\kappa=c^4/(4GM)$，故

$$T_H=\frac{\hbar c^3}{8\pi GM k_B}. \tag{E.4.5}$$

**数值核对**：取 $M=M_\odot$，$T_H\approx6.17\times10^{-8}\ \mathrm{K}$，远低于宇宙微波背景 $2.7\ \mathrm{K}$，故恒星质量黑洞当前净吸积而非净蒸发。

**Bekenstein-Hawking 熵**（正书 (50.13)）：由热力学第一定律 $dM=T_H\,dS_{\rm BH}$，积分得 $S_{\rm BH}=k_B c^3A/(4\hbar G)$，其中 $A=4\pi r_s^2$ 为视界面积。系数 $1/4$ 由 Bogoliubov 热谱斜率严格定出，不可从量纲分析猜出。

## E.5 TUFT 主方程 $\kappa\to0$ 极限（对应正书 (TUFT-32)、(TUFT-33)、(TUFT-45)、(TUFT-46)）

**TUFT 主方程**（正书 (TUFT-32)）：

$$D_\mu\mathcal F^{\mu\nu}+\kappa(x)\mathcal J^\nu+\tau(x)\mathcal K^\nu=\mathcal S^\nu. \tag{E.5.1}$$

**第一步：平直弱场极限 $\kappa\to0,\ \tau\to0$**。此时 Frenet 标架退化为普通坐标架，分形协变导数 $D_\mu=\partial_\mu+\Gamma_\mu+\mathcal F_\mu$（TUFT-27）退回普通偏导 $\partial_\mu$，场张量 $\mathcal F^{\mu\nu}=\partial^\mu A^\nu-\partial^\nu A^\mu+G^{\mu\nu}$（TUFT-25）退回标准电磁场张量 $F_{\rm em}^{\mu\nu}=\partial^\mu A^\nu-\partial^\nu A^\mu$。

**第二步：代入**。主方程 (E.5.1) 变为

$$\partial_\mu F_{\rm em}^{\mu\nu}=\mathcal S^\nu. \tag{E.5.2}$$

**这正是 Maxwell 方程的协变形式**（正书 (TUFT-33)、(TUFT-45)）：$\mathcal S^\nu$ 即四维电流源。

**第三步：进一步退到广义相对论**。TUFT 修正的 Einstein 方程（TUFT-76）

$$R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}+\tau\mathcal G_{\mu\nu} \tag{E.5.3}$$

在 $\tau\to0$ 时退回

$$R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}, \tag{E.5.4}$$

即标准 Einstein 场方程（正书 (5.20)）。

**第四步：自洽性核对**。这一退化证明 TUFT 主方程不是与标准物理矛盾的新理论，而是在 $\kappa,\tau$ 小的区域把标准物理作为一阶近似包含进来。低能弱场实验只测量到 Maxwell 与 Einstein 的标准形式，正是因为 $\kappa\sim10^{-23}\ \mathrm{m^{-1}}$（地球表面）到 $\kappa\sim10^{-5}\ \mathrm{m^{-1}}$（恒星级黑洞视界外）的修正项远低于当前探测精度。

## E.6 小结

本附录补编的五条推导分别对应：相对论运动学骨架（E.1）、Dirac 方程代数骨架（E.2）、经典辐射理论（E.3）、黑洞热力学（E.4）、TUFT 低能退化（E.5）。每条推导的中间步骤均可独立验算；与正书编号的一一对应保证读者可在正书对应段落找到上下文。
