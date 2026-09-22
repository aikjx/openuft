# 附录 A 符号表

【 **约定** :全书 LaTeX 行内公式 $ $ 包裹；粗体字母为矩阵/矢量；$\mathsf{T}$ 转置、$*$ 复共轭、$\dagger$ 厄米共轭。】

## 基元与对偶

| 符号 | 含义 |
|---|---|
| $0, 1$ | 不可再分基元（阴/阳） |
| $D$ | 对偶变换，$D^{2} = 1$ |
| $\Theta$ | 对偶算子，$\Theta = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$，$\Theta^{2} = -I$ |
| $\bar{a}$ | $a$ 的阴阳反转 |
| $\Psi^{c}$ | 电荷共轭旋量，$\Psi^{c} = \Theta\Psi^{*}$ |

## 场与规范

| 符号 | 含义 |
|---|---|
| $\Psi$ | 两分量旋量 $\left( \psi_{0}, \psi_{1} \right)^{\mathsf{T}}$ |
| $\hat\Psi$ | 归一化旋量 $\Psi/|\Psi|$ |
| $\sigma^{\mu}$ | 泡利矩阵（$\mu = 0,1,2,3$） |
| $\lambda$ | 对偶耦合常数（量纲=质量） |
| $\zeta$ | 附加耦合（M1 线性项系数） |
| $v$ | 真空期望值，$|\Psi|^{2} = v^{2}$ |
| $\kappa$ | 有效势系数，$V = \kappa\left( |\Psi|^{2} - v^{2} \right)^{2}$ |
| $a_{\mu}$ | 涌现 $U(1)$ 联络 |
| $b_{\mu\nu}$ | $U(1)$ 场强 $\partial_{\mu}a_{\nu} - \partial_{\nu}a_{\mu}$ |
| $\mathcal{E}$ | 对偶帧 $\left( \hat\Psi, \Theta\hat\Psi^{*} \right) \in U(2)$ |
| $\mathcal{A}_{\mu}$ | 对偶帧联络 $\mathcal{E}^{\dagger}\partial_{\mu}\mathcal{E} \in \mathrm{u}(2)$ |
| $m_{H}$ | 希格斯质量，$m_{H} = 2\sqrt{2}\sqrt{\kappa}\,v$ |
| $\theta_{W}$ | 弱混合角（待定） |

## 拓扑与尺度

| 符号 | 含义 |
|---|---|
| $Q$ | 基本拓扑荷，$Q \in \mathbb{Z}$，最小单位 $\pm 1$ |
| $Q_{1D}$ | 1D 绕数（已证伪，§7.2/§15） |
| $Q_{H}$ | 霍普夫荷 $\frac{1}{4\pi^{2}}\int\epsilon^{ijk}a_{i}\partial_{j}a_{k}$ |
| $\pi_{d}\left( S^{2} \right)$ | 同伦群；$\pi_{1}=0$，$\pi_{3}=\mathbb{Z}$ |
| $\beta\left( g \right)$ | $\beta$ 函数，$\mu\frac{\mathrm{d}g}{\mathrm{d}\mu} = \beta\left( g \right)$，奇函数 |
| $g^{*}$ | 不动点，$g^{*} = \pm\sqrt{\varepsilon/c}$ |
| $\gamma$ | 反常维度，$D = 4 - \gamma$ |
| $\ell$ | 对偶最短尺度，$v = \ell^{-1}$ |
| $r_{s}$ | Schwarzschild 半径，$r_{s} = 2GM$ |
| $g^{\mathrm{eff}}$ | 对偶镜像度规，$g^{\mathrm{eff}}\left( r \right) = g^{\mathrm{eff}}\left( \ell^{2}/r \right)$ |
| $R$ | Ricci 标量；$\left| R \right|_{\max} = \frac{\left( 3+2\sqrt{2} \right)GM}{2\ell^{3}}$ |
| $\mathcal{C}, \partial\mathcal{C}$ | 因果畴及其零面边界 |
| $\omega, \Theta$ | 密度 3-形式、通量 2-形式 |
| $\mathbb{Z}_{4}$ | 对偶周期 4 群；实不可约表示 $1, 1, 2$ 维（第22章） |
| $\mathrm{FS}\left( \rho \right)$ | Frobenius–Schur 指标：$+1$ 实型 / $0$ 复型 / $-1$ 四元数型 |
| $J$ | 二维实表示生成元，$J^{2} = -I$（内部复结构） |
| $Q_{L}, u_{R}, d_{R}, L_{L}, e_{R}$ | 每代费米子五场（第22章反常消去表） |
| $\mathbb{CP}^{2}$ | 复射影平面 $= S^{5}/U(1)$；等距群 $SU(3)/\mathbb{Z}_{3}$（第23章） |
| $d_{\mathrm{FS}}$ | Fubini–Study 距离，$\cos d = \left| z^{\dagger}w \right|/\left( \left| z \right|\left| w \right| \right)$ |
| $\lambda_{1} \dots \lambda_{8}$ | 盖尔曼矩阵（$\mathfrak{su}(3)$ 生成元基，$\mathrm{tr}\left( \lambda_{a}\lambda_{b} \right) = 2\delta_{ab}$） |
| $f^{abc}$ | $\mathfrak{su}(3)$ 结构常数，$\left[ T_{a}, T_{b} \right] = i\sum_{c} f^{abc}T_{c}$ |
| $U(2)$ | $\mathbb{CP}^{2}$ 固定点稳定子 $\supset SU(2) \times U(1)$（电弱候选） |
| $s$ | BRST 超导子（$sA = Dc$、$sc = -c^{2}$、$s^{2} = 0$；第24章） |
| $c, \bar c$ | Faddeev–Popov 鬼场（格拉斯曼奇元） |
| $\beta\left( g \right)$ | 耦合 $\beta$ 函数，$\beta\left( -g \right) = -\beta\left( g \right)$（双向对称） |
| $b_{0}$ | 单圈 $\beta$ 系数，$b_{0} = \tfrac{11}{3}C_{2}\left( A \right) - \tfrac{4}{3}T\left( R \right)n_{f}$（$SU(3)$ 纯规范 11） |
| $Q = T_{3} + Y$ | 电荷（第25章：色单态整数性、$\pm 1/3$ 分数化） |

## 参数归并

| 原参数 | 归并后 | 关系 |
|---|---|---|
| $\lambda, \ell, v, \kappa$ | $\tilde{g}, \tilde{\kappa}, \ell$ | $v = \ell^{-1}$，$\lambda = v\tilde{g}$，$\kappa = \tilde{\kappa}$（无量纲） |
