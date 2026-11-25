# ROOT V139：从光速螺旋、三正交运动到几何规范场的严格推导

版本：2026-11-23。单位：**仅设 c=1，保留 ℏ 与 G 的独立量纲**。本报告属于候选模型的数学审计；不声称证明四种基本力统一。

## 0. 研究命题与适用域

待检验 ROOT 命题：基础光速螺旋与三正交局部标架的运动能否独立导出物理相互作用。

本轮将问题依次拆成：A. 纯几何重建；B. 真实动量变化；C. 内部方向场 Berry 曲率；D. U(1) 局部规范动力学；E. 是否能再现任意电磁场；F. 与标准模型和引力的差距。

## 1. 光速螺旋的正向与逆向证明

在一选定惯性参考系（并非一般协变定义的内部光速）取

\[
\mathbf x(t)=(a\cos\omega t,a\sin\omega t,ut),\quad a>0,\quad \omega>0.
\]

\[
\dot{\mathbf x}=(-a\omega\sin\omega t,a\omega\cos\omega t,u),\quad
\ddot{\mathbf x}=(-a\omega^2\cos\omega t,-a\omega^2\sin\omega t,0).
\]

设空间速度模长为 1（c=1），则

\[
a^2\omega^2+u^2=1.
\]

按曲线微分几何定义

\[
\kappa=\frac{|\dot{\mathbf x}\times\ddot{\mathbf x}|}{|\dot{\mathbf x}|^3}=a\omega^2,
\qquad \tau=\frac{(\dot{\mathbf x}\times\ddot{\mathbf x})\cdot\dddot{\mathbf x}}{|\dot{\mathbf x}\times\ddot{\mathbf x}|^2}=u\omega.
\]

所以 \(\kappa^2+\tau^2=\omega^2\)。反过来，对每对 \(\kappa>0, \tau\in\mathbb R\)：

\[
\boxed{\omega=\sqrt{\kappa^2+\tau^2},\quad
 a=\frac{\kappa}{\kappa^2+\tau^2},\quad
 u=\frac{\tau}{\sqrt{\kappa^2+\tau^2}}},\quad
 p_{\rm turn}=\frac{2\pi\tau}{\kappa^2+\tau^2}.
\]

直接代入验证速度平方为 1、曲率和挠率被原样恢复。此为**运动学恒等式**，无法因此决定任意耦合常数。

## 2. 三方向垂直与达布角速度

在上述非退化轨迹上 Frenet 标架 \(\mathbf T,\mathbf N,\mathbf B\) 相互正交，满足

\[
\frac{d\mathbf T}{ds}=\kappa\mathbf N,\qquad
\frac{d\mathbf N}{ds}=-\kappa\mathbf T+\tau\mathbf B,\qquad
\frac{d\mathbf B}{ds}=-\tau\mathbf N.
\]

因为 \(ds/dt=1\)，标架转动角速度矢量

\[
\boldsymbol\Omega_{\rm FS}=\tau\mathbf T+\kappa\mathbf B=\omega\mathbf e_z,
\qquad |\boldsymbol\Omega_{\rm FS}|^2=\kappa^2+\tau^2.
\]

其三个正交单位矢量**不是**三个必然非零的动力学力。有非零曲率而恒速时 \(\ddot{\mathbf x}=\kappa\mathbf N\) 仅沿法向。

若一个局域光速点状激发的空间动量取 \(\mathbf p=E\mathbf T\)，并保持能量 E 恒定，则

\[
\frac{d\mathbf p}{dt}=E\kappa\mathbf N,\qquad \dot E=\mathbf F\cdot\mathbf v=0.
\]

这个弯曲轨迹需要相互作用或背景，不能把曲率本身算成已导出的引力。平直 Minkowski 时空中它是零间隔但**非自由测地线**。

## 3. 洛伦兹变换一致性：几何频率 ≠ 量子平面波频率

沿轴向以 \(\beta\) boost，\(\gamma=(1-\beta^2)^{-1/2}\)，定义

\[
D=\gamma(1-\beta u),\quad
u'=\frac{u-\beta}{1-\beta u},\quad a'=a,\quad \omega'_{\rm geom}=\omega_{\rm geom}/D.
\]

若假定光速粒子的四动量 \(p^\mu=E(1,\mathbf T)\)，则 \(E'=DE\)。所以

\[
\frac{E'/\omega'_{\rm geom}}{E/\omega_{\rm geom}}=D^2.
\]

例如 \(a=.6,\omega=1,u=.8,\beta=.3\) 时，\(D=0.7966964759086579\)，\(\omega'_{\rm geom}/\omega=1.255183159759139\)，\(E'/E=0.7966964759086579\)。于是**不能不经额外的协变波场构造，直接把轨迹角频率当作 E=ℏω 中的量子频率**。这不否定真正波四矢量的协变相位。

## 4. 从内部方向变化导出一个 U(1) Berry 曲率

令 \(z=(\cos(\theta/2),e^{i\phi}\sin(\theta/2))^T\)，\(z^\dagger z=1\)。此时 \(\mathbf n=z^\dagger\boldsymbol\sigma z\)。定义 Berry 连接

\[
a_\mu=-i z^\dagger\partial_\mu z=\sin^2(\theta/2)\partial_\mu\phi.
\]

取外微分，得

\[
\boxed{f_{\mu\nu}=\frac12\sin\theta(\partial_\mu\theta\partial_\nu\phi-\partial_\nu\theta\partial_\mu\phi)=\frac12\mathbf n\cdot(\partial_\mu\mathbf n\times\partial_\nu\mathbf n)}.
\]

若 \(\theta\) 常数，\(\phi\) 在时间上任意旋转，则 \(f=0\)。但例如 \(\theta(x)=kx,\phi(t)=\Omega t\)，\(f_{xt}=k\Omega\sin(kx)/2\) 可以非零。这是**几何效应的推导，不是 Maxwell 电磁力的来源证明**。

拓扑检验：\(\int_{S^2}f=2\pi n\)，故第一 Chern 数 \((1/2\pi)\int_{S^2}f=n\in\mathbb Z\)。参数空间积分是整体拓扑量，不意味着电磁精细结构常数自动得到 1/137。

## 5. 关键限制：单个方向场不能生成所有电磁场

利用微分形式，\(f=(\sin\theta/2)\,d\theta\wedge d\phi\)。故

\[
\boxed{f\wedge f=0.}
\]

等价于 4 维坐标下的 Pfaffian 为零：

\[
\boxed{f_{01}f_{23}-f_{02}f_{13}+f_{03}f_{12}=0.}
\]

对任意物理电磁场 \(F\)，有 \(F_{\mu\nu}\widetilde F^{\mu\nu}\) 与 \(\mathbf E\cdot\mathbf B\) 成比例。因此这种**单个** Berry 方向场模型只允许 \(\mathbf E\cdot\mathbf B=0\) 的类场强，而实际 Maxwell 方程也允许 \(\mathbf E\parallel\mathbf B\ne0\)。反例取 \(F_{01}=F_{23}=1\) 且其它独立分量为零，此时 Pfaffian=1。该反例表示最小“一个旋转方向场即全部电磁场”的假设失败。

**构造性下一步也得到验证：**让两个独立方向场分别产生 \(f^{(1)}_{01}=1\)、\(f^{(2)}_{23}=1\)，而其余独立分量为零。两者各自的 Pfaffian=0，但总场 \(F=f^{(1)}+f^{(2)}\) 的 Pfaffian=1，因而消除上一段的局部代数障碍。这说明**至少两个独立的简单二形式**可以表示一个非退化 4 维二形式；但并没有自动建立 Maxwell 动力学、全局拓扑与实验耦合值。新增自由度必须有独立物理来源，不能仅为拟合而增加参数。

## 6. 从几何相位到真正动力学：最小 U(1) 作用量

为测试“相位运动是否自动导致物理力”，考虑一个清晰的（既有）Stückelberg 型候选：

\[
S=\int d^4x\sqrt{-g}\left[\frac{R}{16\pi G}
-\frac{\hbar}{4g_A^2}F_{\mu\nu}F^{\mu\nu}
-\frac{\hbar f^2}{2}B_\mu B^\mu\right],\qquad
F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu,\quad B_\mu=\partial_\mu\theta-A_\mu.
\]

在局部变换 \(\theta\mapsto\theta+\chi\)，\(A_\mu\mapsto A_\mu+\partial_\mu\chi\) 下，\(F,B\) 不变。对 \(A_\nu\) 和 \(\theta\) 求变分得到

\[
\boxed{\nabla_\mu F^{\mu\nu}=-g_A^2 f^2 B^\nu,\qquad \nabla_\mu B^\mu=0.}
\]

当 \(\theta=0\) 取规范后，有 \(\nabla_\mu F^{\mu\nu}=(g_A f)^2A^\nu\)。对应质量矢量的逆长度质量 \(\mu_A=|g_Af|\)，色散 \(\omega^2=\mathbf k^2+\mu_A^2\)，能隙 \(\Delta E=\hbar\mu_A\)。若将其认作未破缺的电磁 \(U(1)\)，非零 \(f\) 会赋予光子质量，与无质量 Maxwell 极限不符；因此不能用这项直接宣称获得正确电磁学。可将其作为另一种新矢量场的受检模型。

尤其当 \(A_\mu=\partial_\mu\theta\) 时，\(B=0,F=0\)。故**局部相位旋转自身不保证真实场强或非零源**。反之当仅有 \(\partial\theta\ne0,A=0,f\ne0\)，一般不满足无外源矢量场方程；不能通过截断矢量方程伪造解。

## 7. 量纲检查（c=1，而非 ℏ=1 或 G=1）

选择坐标 \([x^\mu]=L\)，\([\theta]=1\)，\([A_\mu]=L^{-1}\)，\([F_{\mu\nu}]=L^{-2}\)，\([f]=L^{-1}\)，\([g_A]=1\)，\([\hbar]=ML\)，\([G]=L/M=L^2/\hbar\)。每项拉格朗日密度分别具有

\[
\left[\frac R G\right]=\frac{L^{-2}}{L/M}=M L^{-3},\quad
[\hbar F^2]=ML\cdot L^{-4}=ML^{-3},\quad
[\hbar f^2 B^2]=ML\cdot L^{-4}=ML^{-3}.
\]

因而整体作用量的量纲 \([S]=ML=[\hbar]\) 完整一致。

## 8. 引力与规范守恒

上述作用量具有广义协变性。对度规变分可形式上得到 \(G_{\mu\nu}=8\pi G T_{\mu\nu}\)；其应力张量为

\[
T_{\mu\nu}=\frac\hbar{g_A^2}(F_{\mu\alpha}F_\nu{}^\alpha-\frac14g_{\mu\nu}F^2)+\hbar f^2(B_\mu B_\nu-\frac12g_{\mu\nu}B^2).
\]

在全部场方程成立时 \(\nabla_\mu T^{\mu\nu}=0\)。这只是协变理论所需的基本一致性。**此作用量已经假设了引力和 U(1) 的结构，并未从单一螺旋自由度独立推出四力。**

## 9. 多物理场与实验状态

- 地球/月球：V135–V137 的 Yukawa 工作保留为历史基准；没有新的 EGM2008、GOCE、GRACE-FO、GRAIL 原始观测数据拟合。已有约 0.6% 地表额外引力示例受到强烈实验一致性质疑，不应当解释为发现新作用。
- 粒子：仍未推导 SU(3)×SU(2)×U(1) 的规范群、手征费米子表示、质量谱、QCD 禁闭或量子重整化条件。
- 引力：现有 Einstein–Hilbert 项属于**输入**，不是从螺旋几何推导出的引力源。
- 精细结构常数 α：依然缺少独立无参数数值预测。

## 10. V140 的可证伪任务

A. 尝试从独立动力学的两个方向场 \(n_1,n_2\) 组成 \(F=f[n_1]+f[n_2]\)，检验是否允许 \(F\wedge F\ne0\)，并检查自由度、能量正定性及规范守恒。

B. 保持仅 c=1，构造洛伦兹协变微观变量与作用量；不要预设光子沿非测地线的内部真实轨道。

C. 以无自由调参预测为最终标准：恢复 GR/Maxwell 极限、粒子谱、耦合常数以及可与地月/微观实验区分的新观测量。

**结论：**V139 证明了一些螺旋及 Berry 几何恒等式，并发现最小场模型的结构性障碍；未完成四力统一理论。
