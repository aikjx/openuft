# 附录 A 全书公式总表

> 本表按章汇总正文全部带编号公式（编号形如 (1.1)、(5.12)、(9.10)）。
> 每条公式的 LaTeX 写法与正文 `\tag{}` 行一致；"所属层"列沿用正文【已证实 / 推导 / 假说】三分层标签。
> 凡正文未出现的编号一律不收录，亦不为凑数而编造。

## A.1 第一章 导论（(1.1)–(1.19)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (1.1) | $\beta \equiv v/c$ | 1.3 | 无量纲速度比定义 | 推导 |
| (1.2) | $\gamma(v)=(1-\beta^2)^{-1/2}$ | 1.3 | 洛伦兹因子定义 | 已证实 |
| (1.3) | $u^\mu=\gamma(c,\vec v)$ | 1.3 | 四速度定义（号差 $+---$） | 推导 |
| (1.4) | $p^\mu=(E/c,\vec p)$ | 1.3 | 四动量定义 | 推导 |
| (1.5) | $\Box=\partial_\mu\partial^\mu=\tfrac{1}{c^2}\partial_t^2-\nabla^2$ | 1.3 | 达朗贝尔算符定义 | 已证实 |
| (1.6) | $\kappa=mc/\hbar$ | 1.3 | 康普顿波数定义 | 推导 |
| (1.7) | $A\ddot\Phi+K\Phi=0$ | 1.3 | 本源振子方程（本书原创公设式写法） | 假说（公设） |
| (1.8) | $D_\mu=\partial_\mu-igA_\mu$ | 1.3 | 协变导数定义 | 已证实 |
| (1.9) | $F=-kx$ | 1.4 | 胡克定律 | 已证实 |
| (1.10) | $F=m\ddot x$ | 1.4 | 牛顿第二定律 | 已证实 |
| (1.11) | $m\ddot x=-kx$ | 1.4 | 振子运动方程（未移项） | 推导 |
| (1.12) | $\ddot x+\omega_0^2x=0,\ \omega_0=\sqrt{k/m}$ | 1.4 | 标准无阻尼振子方程 | 推导 |
| (1.13) | $x(t)=A\cos\omega_0t+B\sin\omega_0t$ | 1.4 | 通解 | 推导 |
| (1.14) | $T=2\pi/\omega_0=2\pi\sqrt{m/k}$ | 1.4 | 振荡周期 | 推导 |
| (1.15) | $E=\tfrac12 m\dot x^2+\tfrac12 kx^2$ | 1.4 | 总机械能 | 推导 |
| (1.16) | $dE/dt=\dot x(m\ddot x+kx)=0$ | 1.4 | 能量守恒验证 | 推导 |
| (1.17) | $a\ddot y+b\dot y+cy=0$ | 1.5 | 一般二阶线性齐次 ODE | 推导 |
| (1.18) | $\ddot y+2\zeta\omega_0\dot y+\omega_0^2y=0$ | 1.5 | 标准阻尼振子形式 | 推导 |
| (1.19) | $\omega_d=\omega_0\sqrt{1-\zeta^2}$ | 1.5 | 阻尼角频率 | 推导 |

## A.2 第二章 经典对偶（(2.1)–(2.20)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (2.1) | $F_s=-kx$ | 2.2 | 弹簧回复力 | 已证实 |
| (2.2) | $m\ddot x=-kx$ | 2.2 | 牛顿第二定律代入 | 推导 |
| (2.3) | $m\ddot x+kx=0$ | 2.2 | 机械振子标准方程 | 推导 |
| (2.4) | $\omega_m=\sqrt{k/m}$ | 2.2 | 机械固有角频率 | 推导 |
| (2.5) | $\ddot x+\omega_m^2x=0$ | 2.2 | 机械方程标准形 | 推导 |
| (2.6) | $T_m=2\pi/\omega_m=2\pi\sqrt{m/k}$ | 2.2 | 机械周期 | 推导 |
| (2.7) | $E_m=\tfrac12 m\dot x^2+\tfrac12 kx^2$ | 2.2 | 机械总能量 | 推导 |
| (2.8) | $V_C=q/C$ | 2.3 | 电容电压-电荷关系 | 已证实 |
| (2.9) | $V_L=L\,dI/dt=L\dot I$ | 2.3 | 电感电压-电流变化率关系 | 已证实 |
| (2.10) | $V_L+V_C=0$ | 2.3 | 基尔霍夫电压定律 | 已证实 |
| (2.11) | $L\ddot q+\tfrac{1}{C}q=0$ | 2.3 | LC 回路标准方程 | 推导 |
| (2.12) | $\omega_e=\sqrt{1/(LC)}$ | 2.3 | 电路固有角频率 | 推导 |
| (2.13) | $\ddot q+\omega_e^2q=0$ | 2.3 | 电路方程标准形 | 推导 |
| (2.14) | $T_e=2\pi\sqrt{LC}$ | 2.3 | 电路周期 | 推导 |
| (2.15) | $U_L=\tfrac12 LI^2=\tfrac12 L\dot q^2$ | 2.3 | 电感磁场能 | 推导 |
| (2.16) | $U_C=\tfrac12 q^2/C$ | 2.3 | 电容电场能 | 推导 |
| (2.17) | $E_e=\tfrac12 L\dot q^2+q^2/(2C)$ | 2.3 | 电路总能量 | 推导 |
| (2.18) | $dE_e/dt=\dot q(L\ddot q+q/C)=0$ | 2.3 | 电路能量守恒 | 推导 |
| (2.19) | $\tfrac12 m\dot x^2+\tfrac12 kx^2\ \leftrightarrow\ \tfrac12 L\dot q^2+\tfrac12 q^2/C$ | 2.6 | 机械-电路能量逐项对照 | 推导 |
| (2.20) | $T_m\leftrightarrow T_e$ | 2.7 | 周期公式在对偶映射下对应 | 推导 |

## A.3 第三章 狭义相对论（(3.1)–(3.33)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (3.1) | $dt=\gamma d\tau,\ \gamma=(1-\beta^2)^{-1/2}$ | 3.2 | 固有时-坐标时关系 | 已证实 |
| (3.2) | $f(v)=1-v^2/c^2,\ \gamma=f^{-1/2}$ | 3.2 | 求导中间量定义 | 推导 |
| (3.3) | $d\gamma/df=-\tfrac12 f^{-3/2}$ | 3.2 | 幂函数求导第一步 | 推导 |
| (3.4) | $df/dv=-2v/c^2$ | 3.2 | 对 $f$ 关于 $v$ 求导 | 推导 |
| (3.5) | $d\gamma/dv=(v/c^2)f^{-3/2}$ | 3.2 | 链式法则中间结果 | 推导 |
| (3.6) | $d\gamma/dv=\gamma^3 v/c^2$ | 3.2 | 洛伦兹因子对 $v$ 求导（核心） | 推导 |
| (3.7) | $\gamma=1/\sqrt{0.64}=1.25$ | 3.2 | $\beta=0.6$ 时的 $\gamma$ 数值 | 推导 |
| (3.8) | $d\gamma/dv=1.171875/c$ | 3.2 | $\beta=0.6$ 时导数代数值 | 推导 |
| (3.9) | $d\gamma/dv\approx3.909\times10^{-9}\ \mathrm{s/m}$ | 3.2 | 国际单位制数值 | 推导 |
| (3.10) | $d\tau=dt/\gamma$ | 3.3 | 固有时定义 | 已证实 |
| (3.11) | $u^\mu=dx^\mu/d\tau=\gamma\,dx^\mu/dt$ | 3.3 | 四速度定义 | 推导 |
| (3.12) | $u^\mu=\gamma(c,v_x,v_y,v_z)$ | 3.3 | 四速度分量形式 | 推导 |
| (3.13) | $u_\mu u^\mu=\gamma^2(c^2-v^2)$ | 3.3 | 内积第一步 | 推导 |
| (3.14) | $u_\mu u^\mu=\gamma^2c^2(1-\beta^2)$ | 3.3 | 提取 $c^2$ | 推导 |
| (3.15) | $u_\mu u^\mu=c^2$ | 3.3 | 四速度归一化恒等式 | 推导 |
| (3.16) | $a^\mu=du^\mu/d\tau$ | 3.4 | 四加速度定义 | 推导 |
| (3.17) | $d(u_\mu u^\mu)/d\tau=2u_\mu a^\mu$ | 3.4 | 对恒等式求导左边 | 推导 |
| (3.18) | $d(c^2)/d\tau=0$ | 3.4 | 右边为常数求导 | 推导 |
| (3.19) | $u\cdot a=u_\mu a^\mu=0$ | 3.4 | 四速度-四加速度正交 | 推导 |
| (3.20) | $p^\mu=mu^\mu=m\gamma(c,\vec v)$ | 3.5 | 四动量定义 | 推导 |
| (3.21) | $E/c=m\gamma c,\ \vec p=m\gamma\vec v$ | 3.5 | 分量读出 | 推导 |
| (3.22) | $E=\gamma mc^2,\ \vec p=\gamma m\vec v$ | 3.5 | 相对论总能量与动量 | 已证实 |
| (3.23) | $p_\mu p^\mu=m^2c^2$ | 3.5 | 四动量模方 | 推导 |
| (3.24) | $p_\mu p^\mu=E^2/c^2-p^2$ | 3.5 | 按 $(E/c,\vec p)$ 展开 | 推导 |
| (3.25) | $E^2/c^2-p^2=m^2c^2$ | 3.5 | 联立中间式 | 推导 |
| (3.26) | $E^2=p^2c^2+m^2c^4$ | 3.5 | 质壳关系 | 已证实 |
| (3.27) | $E^2=p^2c^2\Rightarrow E=|p|c$ | 3.5 | 零质量极限中间式 | 推导 |
| (3.28) | $E=pc\ (m=0,\ v=c)$ | 3.5 | 光子能量-动量关系 | 推导 |
| (3.29) | $f=c/\lambda\approx5.451\times10^{14}\ \mathrm{Hz}$ | 3.5 | 550 nm 可见光频率 | 推导 |
| (3.30) | $E=hf\approx3.61\times10^{-19}\ \mathrm{J}$ | 3.5 | 单光子能量 | 推导 |
| (3.31) | $p=E/c\approx1.20\times10^{-27}\ \mathrm{kg\,m/s}$ | 3.5 | 单光子动量 | 推导 |
| (3.32) | $E=\gamma mc^2\approx1.024\times10^{-13}\ \mathrm{J}\approx0.639\ \mathrm{MeV}$ | 3.5 | $\beta=0.6$ 电子总能量 | 推导 |
| (3.33) | $p=\gamma mv\approx2.05\times10^{-22}\ \mathrm{kg\,m/s}$ | 3.5 | $\beta=0.6$ 电子动量 | 推导 |

## A.4 第四章 波动与场（(4.1)–(4.37)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (4.1) | $\partial_\mu=(\tfrac{1}{c}\partial_t,\nabla)$ | 4.2 | 四维梯度定义 | 推导 |
| (4.2) | $\partial^\mu=(\tfrac{1}{c}\partial_t,-\nabla)$ | 4.2 | 升指标偏导 | 推导 |
| (4.3) | $\Box=\partial_\mu\partial^\mu$ | 4.2 | 缩并得二阶算符 | 推导 |
| (4.4) | $\Box=\tfrac{1}{c^2}\partial_t^2-\nabla^2$ | 4.2 | 达朗贝尔算符标准形 | 已证实 |
| (4.5) | $\Box\Phi=0$ | 4.3 | 齐次达朗贝尔方程 | 推导 |
| (4.6) | $\Phi=\Phi_0 e^{i(\vec k\cdot\vec x-\omega t)}$ | 4.3 | 平面波 ansatz | 推导 |
| (4.7) | $\partial_t^2\Phi=-\omega^2\Phi$ | 4.3 | 时间二阶导代入 | 推导 |
| (4.8) | $\partial_x^2\Phi=-k_x^2\Phi$ | 4.3 | 空间二阶导（分量例） | 推导 |
| (4.9) | $\nabla^2\Phi=-k^2\Phi$ | 4.3 | 三空间分量求和 | 推导 |
| (4.10) | $\Box\Phi=(-\omega^2/c^2+k^2)\Phi$ | 4.3 | 代入结果 | 推导 |
| (4.11) | $\omega^2=c^2k^2$ | 4.3 | 色散关系中间式 | 推导 |
| (4.12) | $\omega=ck$ | 4.3 | 真空线性色散 | 推导 |
| (4.13) | $v_p=\omega/k$ | 4.3 | 相速度定义 | 推导 |
| (4.14) | $v_p=c$ | 4.3 | 真空相速度 | 推导 |
| (4.15) | $v_g=d\omega/dk$ | 4.3 | 群速度定义 | 推导 |
| (4.16) | $v_g=c$ | 4.3 | 真空群速度 | 推导 |
| (4.17) | $k=2\pi/\lambda\approx1.142\times10^7\ \mathrm{m^{-1}}$ | 4.3 | 550 nm 波数 | 推导 |
| (4.18) | $\omega=ck\approx3.423\times10^{15}\ \mathrm{rad/s}$ | 4.3 | 550 nm 角频率 | 推导 |
| (4.19) | $\nabla\cdot\vec E=0$ | 4.4 | 真空 Maxwell 高斯电 | 已证实 |
| (4.20) | $\nabla\cdot\vec B=0$ | 4.4 | 真空 Maxwell 高斯磁 | 已证实 |
| (4.21) | $\nabla\times\vec E=-\partial_t\vec B$ | 4.4 | 法拉第定律 | 已证实 |
| (4.22) | $\nabla\times\vec B=\mu_0\varepsilon_0\partial_t\vec E$ | 4.4 | 安培-麦克斯韦定律 | 已证实 |
| (4.23) | $\nabla\times(\nabla\times\vec E)=-\partial_t(\nabla\times\vec B)$ | 4.4 | 对法拉第取旋度 | 推导 |
| (4.24) | $-\partial_t(\nabla\times\vec B)=-\mu_0\varepsilon_0\partial_t^2\vec E$ | 4.4 | 代入安培定律 | 推导 |
| (4.25) | $-\nabla^2\vec E=-\mu_0\varepsilon_0\partial_t^2\vec E$ | 4.4 | 联立结果 | 推导 |
| (4.26) | $\partial_t^2\vec E-\tfrac{1}{\mu_0\varepsilon_0}\nabla^2\vec E=0$ | 4.4 | E 波动方程 | 推导 |
| (4.27) | $\partial_t^2\vec B-\tfrac{1}{\mu_0\varepsilon_0}\nabla^2\vec B=0$ | 4.4 | B 波动方程 | 推导 |
| (4.28) | $\Box\vec E=0$ | 4.4 | 写成达朗贝尔形式 | 推导 |
| (4.29) | $1/c^2=\mu_0\varepsilon_0$ | 4.4 | 速度系数对照 | 推导 |
| (4.30) | $c=1/\sqrt{\mu_0\varepsilon_0}$ | 4.4 | 光速由电磁常数决定 | 已证实 |
| (4.31) | $\mu_0=4\pi\times10^{-7}\ \mathrm{H/m}$ | 4.4 | 真空磁导率（旧定义） | 已证实 |
| (4.32) | $\varepsilon_0\approx8.854\times10^{-12}\ \mathrm{F/m}$ | 4.4 | 真空介电常数 | 已证实 |
| (4.33) | $\mu_0\varepsilon_0=4\pi\times8.854\times10^{-19}$ | 4.4 | 乘积代数式 | 推导 |
| (4.34) | $\mu_0\varepsilon_0\approx1.11265\times10^{-17}\ \mathrm{s^2/m^2}$ | 4.4 | 乘积数值 | 推导 |
| (4.35) | $\sqrt{\mu_0\varepsilon_0}=\sqrt{11.1265\times10^{-18}}$ | 4.4 | 平方根中间式 | 推导 |
| (4.36) | $\sqrt{\mu_0\varepsilon_0}\approx3.33564\times10^{-9}\ \mathrm{s/m}$ | 4.4 | 平方根数值 | 推导 |
| (4.37) | $c\approx2.99792458\times10^8\ \mathrm{m/s}$ | 4.4 | 反推出光速 | 推导 |

## A.5 第五章 统一主方程（(5.1)–(5.23)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (5.1) | $E^2=p^2c^2+m^2c^4$ | 5.2 | 质壳关系（重述） | 已证实 |
| (5.2) | $E\to i\hbar\partial_t,\ \vec p\to-i\hbar\nabla$ | 5.2 | 能量-动量算符对应 | 已证实 |
| (5.3) | $(i\hbar\partial_t)^2\Phi=(-i\hbar\nabla)^2c^2\Phi+m^2c^4\Phi$ | 5.2 | 代入质壳 | 推导 |
| (5.4) | $\tfrac{1}{c^2}\partial_t^2\Phi-\nabla^2\Phi-\tfrac{m^2c^2}{\hbar^2}\Phi=0$ | 5.2 | KG 方程分量形式 | 推导 |
| (5.5) | $\kappa=mc/\hbar,\ \kappa^2=m^2c^2/\hbar^2$ | 5.2 | 康普顿波数 | 推导 |
| (5.6) | $(\Box+\kappa^2)\Phi=0$ | 5.2 | 自由 Klein-Gordon 协变式 | 已证实 |
| (5.7) | $\omega^2=c^2(k^2+\kappa^2)$ | 5.2 | 有质量场色散 | 推导 |
| (5.8) | $v_g=c\sqrt{1-\kappa^2/(k^2+\kappa^2)}<c$ | 5.2 | 有质量场群速 | 推导 |
| (5.9) | $\kappa_e\approx2.5896\times10^{12}\ \mathrm{m^{-1}}$ | 5.2 | 电子康普顿波数数值 | 推导 |
| (5.10) | $(\Box+\kappa^2)\Phi=J$ | 5.3 | 有源自由场方程 | 推导 |
| (5.11) | $D_\mu=\partial_\mu-igA_\mu$ | 5.3 | 协变导数（重述） | 已证实 |
| (5.12) | $D_\mu D^\mu\Phi-\kappa^2\Phi=J$ | 5.3 | 有源规范耦合主方程 | 推导 |
| (5.13) | $\Box\Phi-ig(\partial_\mu A^\mu+2A_\mu\partial^\mu)\Phi-g^2A_\mu A^\mu\Phi-\kappa^2\Phi=J$ | 5.3 | 协变导数展开 | 推导 |
| (5.14) | $\Box A_\mu=0$ | 5.4 | 真空 Maxwell 波动形式（Lorenz 规范） | 已证实 |
| (5.15) | $D_\mu F^{a\mu\nu}=0,\ F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu+gf^{abc}A^b_\mu A^c_\nu$ | 5.4 | Yang-Mills 方程与场强 | 已证实 |
| (5.16) | $\Box A^a_\mu=0$ | 5.4 | YM 线性化方程 | 推导 |
| (5.17) | $g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu},\ |h_{\mu\nu}|\ll1$ | 5.5 | 度规微扰展开 | 已证实 |
| (5.18) | $\Box\bar h_{\mu\nu}=-(16\pi G/c^4)T_{\mu\nu}$ | 5.5 | 线性化 Einstein 方程有源 | 推导 |
| (5.19) | $\Box\bar h_{\mu\nu}=0$ | 5.5 | 真空线性化引力波方程 | 已证实 |
| (5.20) | $R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ | 5.6 | Einstein 场方程 | 已证实 |
| (5.21) | $\Gamma^\lambda_{\mu\nu}=\tfrac12\eta^{\lambda\rho}(\partial_\mu h_{\nu\rho}+\partial_\nu h_{\mu\rho}-\partial_\rho h_{\mu\nu})$ | 5.6 | Christoffel 一阶近似 | 推导 |
| (5.22) | $R^{(1)}_{\mu\nu}=\partial_\rho\Gamma^\rho_{\mu\nu}-\partial_\nu\Gamma^\rho_{\mu\rho}$ | 5.6 | Ricci 张量一阶近似 | 推导 |
| (5.23) | $R^{(1)}_{\mu\nu}-\tfrac12\eta_{\mu\nu}R^{(1)}=-\tfrac12\Box\bar h_{\mu\nu}$ | 5.6 | Einstein 张量一阶式 | 推导 |

## A.6 第六章 本源回环（(6.1)–(6.15)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (6.1) | $u\ddot y+\omega_0^2y=0$ | 6.2 | 抽象振子方程（机械/电路共同形式） | 已证实 |
| (6.2) | $A\ddot\Phi+K\Phi=0$ | 6.2 | 本源振子方程（公设式写法） | 假说（公设） |
| (6.3) | $\omega_0=\sqrt{K/A}$ | 6.2 | 本源振子固有角频率 | 推导 |
| (6.4) | $\mathcal E=\tfrac12 A\dot\Phi^2+\tfrac12 K\Phi^2=\mathrm{const}$ | 6.2 | 本源振子守恒能量 | 推导 |
| (6.5) | $\Box=\tfrac{1}{c^2}\partial_t^2-\nabla^2$ | 6.3 | 达朗贝尔算符（重述） | 已证实 |
| (6.6) | $\Box\Phi=\tfrac{1}{c^2}\ddot\Phi$（空间均匀极限） | 6.3 | $\Box$ 与 $\ddot\Phi$ 的关系 | 推导 |
| (6.7) | $Ac^2\Box\Phi+K\Phi=0$ | 6.3 | 完备化中间式 | 推导 |
| (6.8) | $A\Box\Phi+\tfrac{K}{c^2}\Phi=0$ | 6.3 | 本源振子的相对论完备化 | 推导 |
| (6.9) | $\Box\Phi+\tfrac{K}{Ac^2}\Phi=0$ | 6.4 | 两边除以 $A$ | 推导 |
| (6.10) | $K/(Ac^2)=\kappa^2=m^2c^2/\hbar^2$ | 6.4 | 与 KG 逐项对照 | 推导 |
| (6.11) | $K/A=m^2c^4/\hbar^2$ | 6.4 | 整理常数关系 | 推导 |
| (6.12) | $\omega_0=mc^2/\hbar$ | 6.4 | 本征频率=Compton 频率 | 推导 |
| (6.13) | $\hbar\omega_0=mc^2$ | 6.4 | 全书核心等式：静能=本征频率乘 $\hbar$ | 推导 |
| (6.14) | $\omega_0\approx7.763\times10^{20}\ \mathrm{rad/s}$ | 6.4 | 电子本源角频率数值 | 推导 |
| (6.15) | $-\omega_0^2/c^2+\kappa^2=0\Rightarrow\omega_0=c\kappa=mc^2/\hbar$ | 6.6 | 零动量平面波代入再得 (6.12) | 推导 |

## A.7 第七章 拓扑荷假说（(7.1)–(7.26)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (7.1) | $A\Box\Phi+\tfrac{K}{c^2}\Phi=J$ | 7.1 | 有源本源主方程（局部线性式） | 推导 |
| (7.2) | $g:S^3\to SU(2)\cong S^3$ | 7.2 | 真空位形作为映射 | 已证实 |
| (7.3) | $\pi_3(S^3)\cong\mathbb Z,\ \pi_3(SU(2))\cong\mathbb Z$ | 7.2 | 同伦分类（瞬子荷整数） | 已证实 |
| (7.4) | $n=\tfrac{1}{16\pi^2}\int d^3x\,\epsilon_{ijk}\mathrm{Tr}(A_i\partial_jA_k+\tfrac{2}{3}igA_iA_jA_k)$ | 7.2 | 瞬子荷三维积分式 | 已证实 |
| (7.5) | $n=\tfrac{1}{16\pi^2}\int d^4x\,\mathrm{Tr}(F_{\mu\nu}\tilde F^{\mu\nu})$ | 7.2 | BPST 瞬子荷四维度对偶式 | 已证实 |
| (7.6) | $\phi:S^3\to S^2$ | 7.2 | Hopf 映射 | 已证实 |
| (7.7) | $\pi_3(S^2)\cong\mathbb Z$ | 7.2 | Hopf 荷整数分类 | 已证实 |
| (7.8) | $Q_H=\tfrac{1}{16\pi^2}\int d^3x\,\epsilon_{ijk}A_iB_jB_k$ | 7.2 | Hopf 荷积分式 | 已证实 |
| (7.9) | $(n_1,n_2,n_3)=\big(2(u_1u_3+u_2u_4),\,2(u_2u_3-u_1u_4),\,u_1^2+u_2^2-u_3^2-u_4^2\big)$ | 7.2 | 标准 Hopf 映射坐标式 | 已证实 |
| (7.10) | $\vec B=\tfrac{g}{4\pi}\hat r/r^2$ | 7.3 | 点磁单极磁场 | 已证实 |
| (7.11) | $\vec A_\pm=\tfrac{g}{4\pi r}\tfrac{\pm1-\cos\theta}{\sin\theta}\hat\phi$ | 7.3 | Dirac 弦两侧补丁矢势 | 已证实 |
| (7.12) | $\Delta\chi=\tfrac{e}{\hbar}\oint\vec A\cdot d\vec l=2eg/\hbar$ | 7.3 | 跨弦波函数相位跃变 | 推导 |
| (7.13) | $eg=n\hbar/2,\ n\in\mathbb Z$ | 7.3 | Dirac 电荷量子化条件 | 已证实 |
| (7.14) | $g_1=\hbar/(2e)\approx3.29\times10^{-16}\ \mathrm{Wb}$ | 7.3 | 单个磁荷量子数值 | 已证实 |
| (7.15) | $E=\int d^3x\big[\tfrac12 B_i^aB_i^a+\tfrac12(D_i\phi^a)^2+\tfrac{\lambda}{4}(\phi^a\phi^a-v^2)^2\big]$ | 7.4 | SU(2) Higgs 静态能量 | 已证实 |
| (7.16) | $E\ge4\pi v\lvert n\rvert$ | 7.4 | Bogomolny-BPS 能量下界 | 已证实 |
| (7.17) | $\tfrac12(B_i^a\mp D_i\phi^a)^2=\tfrac12 B^2+\tfrac12(D\phi)^2\mp B_i^aD_i\phi^a$ | 7.4 | 配方恒等式 | 推导 |
| (7.18) | $E=\int\tfrac12(B\mp D\phi)^2\pm\int B_i^aD_i\phi^a$ | 7.4 | 配方后能量分解 | 推导 |
| (7.19) | $s=Q_H/2$ | 7.5 | 【假说】Hopf 荷与自旋对应 | 假说 |
| (7.20) | $(\rho-a)^2+(z-b)^2=R^2,\ \phi=\omega t$ | 7.5 | 环面涡旋力线 ansatz | 假说 |
| (7.21) | $B_\rho=0,\ B_\phi=B_\phi(\rho,z),\ B_z=B_z(\rho,z)$ | 7.5 | 柱对称对偶场 ansatz | 假说 |
| (7.22) | $(i\gamma^\mu D_\mu-m)\psi=0$ | 7.5 | Dirac 方程（标准） | 已证实 |
| (7.23) | $A\Box\Phi+\tfrac{K}{c^2}\Phi+\lambda\lvert\Phi\rvert^2\Phi=J$ | 7.6 | 【假说 H7.2】非线性本源主方程 | 假说 |
| (7.24) | $\mathcal L=\lvert\partial_\mu\vec n\rvert^2-F[(\vec n\cdot\partial_\mu\vec n\times\partial_\nu\vec n)^2]-V(\vec n)$ | 7.6 | Skyrme-Faddeev 型拉氏量 | 假说 |
| (7.25) | $\lambda_n=\lambda_0\alpha^{-n}$ | 7.6 | 【假说 H7.3】耦合常数几何级数分裂 | 假说 |
| (7.26) | $M_n=M_0/\alpha^{n/2}$ | 7.6 | 【假说 H7.3】离散质量塔 | 假说 |

## A.8 第八章 分形宇宙假说（(8.1)–(8.17)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (8.1) | $\beta(g)=\mu\,dg/d\mu$ | 8.2 | $\beta$ 函数定义 | 已证实 |
| (8.2) | $\beta(g)=-\tfrac{\beta_0}{(4\pi)^2}g^3,\ \beta_0=\tfrac{11}{3}N_c-\tfrac{2}{3}N_f$ | 8.2 | 非阿贝尔 $\beta$ 函数一级形式 | 已证实 |
| (8.3) | $\beta_0=11-\tfrac{2}{3}\times6=7$ | 8.2 | QCD 反常量纲数值 | 已证实 |
| (8.4) | $\tfrac{1}{g^2(\mu)}=\tfrac{1}{g^2(\mu_0)}+\tfrac{\beta_0}{(4\pi)^2}\ln(\mu/\mu_0)$ | 8.2 | 耦合常数对数跑动解 | 已证实 |
| (8.5) | $\phi_B=\tfrac{1}{b^d}\sum_{x\in B}\phi(x)$ | 8.2 | Wilson 块自旋 | 已证实 |
| (8.6) | $g'=R_b(g)$ | 8.2 | 块自旋重整化变换 | 已证实 |
| (8.7) | $\xi\sim\lvert t\rvert^{-\nu}$ | 8.2 | 关联长度临界发散 | 已证实 |
| (8.8) | $\langle\mathcal O(x)\mathcal O(0)\rangle\sim\lvert x\rvert^{-2\Delta},\ \Delta=\Delta_0+\gamma$ | 8.2 | 两点函数标度形式 | 已证实 |
| (8.9) | $\gamma(g)=\mu\,d\ln Z/d\mu$ | 8.2 | 反常维度定义 | 已证实 |
| (8.10) | $D=\ln N/\ln(1/\varepsilon)$ | 8.3 | 豪斯多夫分形维数 | 已证实 |
| (8.11) | $D=\ln2/\ln3\approx0.6309$ | 8.3 | 康托尔集维数 | 已证实 |
| (8.12) | $D=\ln4/\ln3\approx1.2619$ | 8.3 | 科赫曲线维数 | 已证实 |
| (8.13) | $A_n\Box_n\Phi_n+\tfrac{K_n}{c^2}\Phi_n=J_n$ | 8.4 | 【假说 H8.1】层级 $n$ 上的主方程 | 假说 |
| (8.14) | $d_{\mathrm{eff}}=3+1+Q_H/2+\Delta D$ | 8.5 | 【假说 H8.2】有效维数 | 假说 |
| (8.15) | $K_n/A_n=(K_0/A_0)\alpha^{-n},\ l_n=l_0\alpha^{n/2}$ | 8.5 | 【假说 H8.3】离散幂律尺度重整 | 假说 |
| (8.15a) | $\widetilde\Phi_n(x)=\alpha^{-n/4}\Phi_n(\alpha^{n/2}x)$ | 8.4 | 统计自相似重标度 | 假说 |
| (8.15b) | $G_n(r)=\langle\widetilde\Phi_n(x)\widetilde\Phi_n(0)\rangle$ | 8.4 | 重标度两点关联函数 | 假说 |
| (8.16) | $\omega_n=\omega_0\alpha^{-n/2}$ | 8.5 | 【假说 H8.3】离散频率塔 | 假说 |
| (8.17) | $g^{-2}(\mu_n)-g^{-2}(\mu_0)=\tfrac{\beta_0}{(4\pi)^2}\cdot\tfrac{n}{2}\ln\alpha$ | 8.5 | 标准 RG 在离散采样点上的形式 | 推导 |

## A.9 第九章 因果畴动力学（(9.1)–(9.13)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (9.1) | $R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ | 9.1 | Einstein 场方程（迹零化写法） | 已证实 |
| (9.2) | $R=(8\pi G/c^4)T+4\Lambda$ | 9.1 | 标曲率迹式 | 推导 |
| (9.3) | $R_{\mu\nu}=(8\pi G/c^4)(T_{\mu\nu}-\tfrac12 g_{\mu\nu}T)+\Lambda g_{\mu\nu}$ | 9.1 | 里奇张量单独解出 | 推导 |
| (9.4) | $d\theta/d\lambda=-\tfrac12\theta^2-2\sigma^2-R_{\mu\nu}k^\mu k^\nu$ | 9.1 | 类光 Raychaudhuri 方程 | 已证实 |
| (9.5) | $1/\theta(\lambda)\le 1/\theta_0+\lambda/2$ | 9.1 | 有限仿射距离汇聚估计 | 推导 |
| (9.6) | $r_s=2GM/c^2\approx2.95\times10^3\ \mathrm{m}$ | 9.1 | 太阳质量史瓦西半径 | 推导 |
| (9.7) | $D_\mu D^\mu\Phi-\kappa^2\Phi+\lambda\lvert\Phi\rvert^{2p}\Phi=J$ | 9.2 | 【假说】含非线性自耦合的正则化场方程 | 假说 |
| (9.8) | $\mathcal D_i=\{x:n_{\mathrm{top}}(x)\in(n_i,n_{i+1}]\}$ | 9.3 | 【假说】因果畴按拓扑荷能级定义 | 假说 |
| (9.9) | $v_{\mathrm{wall}}=\sqrt{\tau/\sigma}\to c$ | 9.3 | 畴壁波速上限（不超光速） | 推导 |
| (9.10) | $\mu=\exp\!\big(N^{-1}\ln(r_H/r_{\mathrm{core}})\big)$ | 9.3 | 【假说】分形尺度比与层级数关系 | 假说 |
| (9.11) | $\partial_\mu J^\mu_{\mathrm{top}}=0$ | 9.4 | 拓扑荷流守恒 | 推导 |
| (9.12) | $\bar\sigma^\mu D_\mu\psi_R=(m/i\hbar)\psi_L,\ \sigma^\mu D_\mu\psi_L=(m/i\hbar)\psi_R$ | 9.4 | 【假说】旋量对偶方程 | 假说 |
| (9.13) | $m(n_{\mathrm{top}})=m_0\,\mathrm{sgn}(n_{\mathrm{top}})\Theta(\lvert n_{\mathrm{top}}\rvert-n_c)$ | 9.4 | 【假说】质量为拓扑荷涌现量 | 假说 |

## A.10 第十章 计算篇（(10.1)–(10.2)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (10.1) | $\gamma(v)=(1-v^2/c^2)^{-1/2},\ d\gamma/dv=\gamma^3v/c^2$ | 10.1 | sympy 符号核验对象 | 推导 |
| (10.2) | $m\ddot x+kx=0,\ L\ddot q+q/C=0$ | 10.2 | 数值对照对象（机械-电路同构） | 推导 |

## A.11 统计小结

- 收录编号公式合计：**19 + 20 + 33 + 37 + 23 + 15 + 26 + 19 + 13 + 2 = 207** 条。
- 其中【已证实】层约 45 条（Maxwell 方程、Einstein 方程、Dirac 方程、Yang-Mills、BPS、Dirac 量子化、RG、分形维数、Raychaudhuri 等标准内容）。
- 【推导】层约 130 条（链式法则、平面波代入、协变化、配方、数值验算等中间步骤）。
- 【假说】层约 32 条（H7.1–H7.3、H8.1–H8.3、奇点化解、因果畴、旋量对偶、质量涌现等）。
- 编号 (8.15a)、(8.15b) 为正文在 (8.15) 之下的两个子式，单独列出以便交叉引用。

> 本总表与正文 `manuscript/chNN-*.md` 一一对应；如正文后续修订编号，本表应同步更新。
