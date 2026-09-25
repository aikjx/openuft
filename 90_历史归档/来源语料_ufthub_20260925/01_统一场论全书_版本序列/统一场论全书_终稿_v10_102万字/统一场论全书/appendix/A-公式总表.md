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

## A.11 第三十二章 Dirac 方程构造（(32.1)–(32.42)，含 (32.24a)–(32.24g)）

> 本章取自然单位 $\hbar=c=1$。

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (32.1) | $p_\mu p^\mu=m^2$ | 32.2 | 质壳关系（自然单位） | 已证实 |
| (32.2) | $\partial_\mu\partial^\mu\phi+m^2\phi=0$ | 32.2 | Klein-Gordon 方程 | 已证实 |
| (32.3) | $\phi^*\partial_\mu\partial^\mu\phi-\phi\,\partial_\mu\partial^\mu\phi^*=0$ | 32.2 | KG 流推导第一步 | 推导 |
| (32.4) | $\partial_\mu[\phi^*\partial^\mu\phi-\phi(\partial^\mu\phi)^*]=0$ | 32.2 | KG 四维散度形式 | 推导 |
| (32.5) | $\rho_{\mathrm{KG}}=i(\phi^*\partial_t\phi-\phi\,\partial_t\phi^*)$ | 32.2 | KG 概率密度（含负号困难） | 推导 |
| (32.6) | $(i\gamma^\mu\partial_\mu-m)\psi=0$ | 32.3 | Dirac 方程 | 已证实 |
| (32.7) | $(i\gamma^\mu\partial_\mu+m)(i\gamma^\nu\partial_\nu-m)\psi=0$ | 32.3 | 二次作用验证 | 推导 |
| (32.8) | $(\gamma^\mu\gamma^\nu\partial_\mu\partial_\nu+m^2)\psi=0$ | 32.3 | 展开中间式 | 推导 |
| (32.9) | $\gamma^\mu\gamma^\nu\partial_\mu\partial_\nu=\tfrac12\{\gamma^\mu,\gamma^\nu\}\partial_\mu\partial_\nu$ | 32.3 | 对称化 | 推导 |
| (32.10) | $\tfrac12\{\gamma^\mu,\gamma^\nu\}=g^{\mu\nu}$ | 32.3 | Clifford 条件（中间） | 推导 |
| (32.11) | $\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}I_N$ | 32.3 | Clifford 代数（核心） | 已证实 |
| (32.12) | $\gamma^0=\mathrm{diag}(I_2,-I_2),\ \gamma^i=\begin{pmatrix}0&\sigma_i\\-\sigma_i&0\end{pmatrix}$ | 32.4 | Dirac-Pauli 标准表示 | 推导 |
| (32.13) | $(\gamma^0)^2=I_4$ | 32.4 | 验证 {γ⁰,γ⁰} | 推导 |
| (32.14) | $\gamma^0\gamma^i=\begin{pmatrix}0&\sigma_i\\\sigma_i&0\end{pmatrix}$ | 32.4 | 验证混合反对易 | 推导 |
| (32.15) | $\gamma^i\gamma^0=\begin{pmatrix}0&-\sigma_i\\-\sigma_i&0\end{pmatrix}$ | 32.4 | 反向乘积 | 推导 |
| (32.16) | $\gamma^0\gamma^i+\gamma^i\gamma^0=0$ | 32.4 | 混合反对易成立 | 推导 |
| (32.17) | $\gamma^i\gamma^j=\begin{pmatrix}-\sigma_i\sigma_j&0\\0&-\sigma_i\sigma_j\end{pmatrix}$ | 32.4 | 空间分量乘积 | 推导 |
| (32.18) | $\gamma^j\gamma^i=\begin{pmatrix}-\sigma_j\sigma_i&0\\0&-\sigma_j\sigma_i\end{pmatrix}$ | 32.4 | 交换指标 | 推导 |
| (32.19) | $\gamma^i\gamma^j+\gamma^j\gamma^i=-\mathrm{diag}(\sigma_i\sigma_j+\sigma_j\sigma_i,\cdots)$ | 32.4 | 相加中间式 | 推导 |
| (32.20) | $\{\gamma^i,\gamma^j\}=-2\delta_{ij}I_4=2g^{ij}I_4$ | 32.4 | 空间反对易成立 | 推导 |
| (32.21) | $\gamma^5=i\gamma^0\gamma^1\gamma^2\gamma^3$ | 32.4 | 手征矩阵定义 | 推导 |
| (32.22) | $\gamma^5=\begin{pmatrix}0&I_2\\I_2&0\end{pmatrix}$ | 32.4 | 标准表示下 γ⁵ | 推导 |
| (32.23) | $P_L=(1-\gamma^5)/2,\ P_R=(1+\gamma^5)/2$ | 32.4 | 手征投影算符 | 推导 |
| (32.24) | $\Sigma^i=\mathrm{diag}(\sigma_i,\sigma_i)$ | 32.4 | Dirac 自旋算符 | 推导 |
| (32.24a) | $\psi'(x')=S(\Lambda)\psi(x)$ | 32.4 | 旋量 Lorentz 变换 | 推导 |
| (32.24b) | $S^{-1}\gamma^\mu S=\Lambda^\mu_{\ \nu}\gamma^\nu$ | 32.4 | S 的核心条件 | 推导 |
| (32.24c) | $i\gamma^\mu\partial'_\mu\psi'=i\gamma^\mu\Lambda_\mu^{\ \nu}\partial_\nu S\psi$ | 32.4 | 协变性验算第一步 | 推导 |
| (32.24d) | $=S(i\gamma^\nu\partial_\nu\psi)=m\psi'$ | 32.4 | 协变性验算末步 | 推导 |
| (32.24e) | $S=1-\tfrac{i}{4}\omega_{\mu\nu}\sigma^{\mu\nu},\ \sigma^{\mu\nu}=\tfrac{i}{2}[\gamma^\mu,\gamma^\nu]$ | 32.4 | S 的无穷小形式 | 推导 |
| (32.24f) | $S^{-1}\gamma^\rho S\approx\gamma^\rho+\tfrac{i}{4}\omega_{\mu\nu}[\sigma^{\mu\nu},\gamma^\rho]$ | 32.4 | 展开中间式 | 推导 |
| (32.24g) | $S^{-1}\gamma^\rho S=\gamma^\rho-\omega^\rho_{\ \nu}\gamma^\nu$ | 32.4 | 与 Λ 一致 | 推导 |
| (32.25) | $\mathrm{tr}(\gamma^\mu)=0,\ \mathrm{tr}(\gamma^\mu\gamma^\nu)=4g^{\mu\nu}$ | 32.5 | 迹恒等式 | 推导 |
| (32.26) | $\mathrm{tr}(\gamma^\mu\gamma^\nu\gamma^\rho\gamma^\sigma)=4(g^{\mu\nu}g^{\rho\sigma}-g^{\mu\rho}g^{\nu\sigma}+g^{\mu\sigma}g^{\nu\rho})$ | 32.5 | 四 γ 迹 | 推导 |
| (32.27) | $\gamma_\mu\gamma^\mu=4I_4$ | 32.5 | 缩并恒等式 | 推导 |
| (32.28) | $\gamma_\mu\gamma^\rho\gamma^\mu=-2\gamma^\rho$ | 32.5 | 三 γ 缩并 | 推导 |
| (32.29) | $(\gamma^\mu p_\mu-m)(\gamma^\nu p_\nu+m)=p_\rho p^\rho-m^2$ | 32.6 | 质壳因式分解（核心） | 推导 |
| (32.30) | $(\gamma^\mu p_\mu)(\gamma^\nu p_\nu)+m\gamma^\mu p_\mu-m\gamma^\nu p_\nu-m^2$ | 32.6 | 展开 | 推导 |
| (32.31) | $\gamma^\mu\gamma^\nu p_\mu p_\nu-m^2$ | 32.6 | 线性项抵消后 | 推导 |
| (32.32) | $\gamma^\mu\gamma^\nu p_\mu p_\nu=\tfrac12\{\gamma^\mu,\gamma^\nu\}p_\mu p_\nu=p_\rho p^\rho$ | 32.6 | 对称化代入 | 推导 |
| (32.33) | $(\not p-m)\psi=0$ | 32.6 | 动量空间 Dirac 方程 | 推导 |
| (32.34) | $(p^2-m^2)\psi=0$ | 32.6 | Dirac 解自动满足 KG | 推导 |
| (32.35) | $(\not p-m)(\not p+m)=p^2-m^2=0$ | 32.7 | 静止系数值验证 | 推导 |
| (32.36) | $\not p-m=m\,\mathrm{diag}(0,0,-2,-2)$ | 32.7 | 静止系矩阵 | 推导 |
| (32.37) | $\not p+m=m\,\mathrm{diag}(2,2,0,0)$ | 32.7 | 静止系矩阵 | 推导 |
| (32.38) | $(\not p-m)(\not p+m)=0$ | 32.7 | 乘积验证 | 推导 |
| (32.39) | $\not p=\gamma^0(1.25m)-\gamma^1(0.75m)$ | 32.7 | 运动系 p̸ | 推导 |
| (32.40) | $\not p=m\begin{pmatrix}1.25I_2&-0.75\sigma_1\\0.75\sigma_1&-1.25I_2\end{pmatrix}$ | 32.7 | 运动系矩阵 | 推导 |
| (32.41) | $\not p^{\,2}=m^2\begin{pmatrix}1.25I_2&-0.75\sigma_1\\0.75\sigma_1&-1.25I_2\end{pmatrix}^2$ | 32.7 | 平方中间式 | 推导 |
| (32.42) | $\not p^{\,2}=m^2 I_4$ | 32.7 | 与质壳一致 | 推导 |

## A.12 第三十三章 Dirac 旋量自由场解与概率流（(33.1)–(33.65)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (33.1) | $\psi=u(p)e^{-ipx}$ | 33.2 | 正能平面波 ansatz | 推导 |
| (33.2) | $\psi=v(p)e^{+ipx}$ | 33.2 | 负能平面波 ansatz | 推导 |
| (33.3) | $i\gamma^\mu\partial_\mu\psi=\not p\,u(p)e^{-ipx}$ | 33.2 | 代入求导 | 推导 |
| (33.4) | $(\not p-m)u(p)=0$ | 33.2 | u 旋量代数方程 | 推导 |
| (33.5) | $i\gamma^\mu(ip_\mu)v e^{ipx}-mv e^{ipx}=0$ | 33.2 | 代入 v | 推导 |
| (33.6) | $(\not p+m)v(p)=0$ | 33.2 | v 旋量代数方程 | 推导 |
| (33.7) | $(p^2-m^2)u(p)=0$ | 33.2 | 非平凡解条件 | 推导 |
| (33.8) | $E_p=\sqrt{\vec p^{\,2}+m^2}>0$ | 33.2 | 正能根 | 推导 |
| (33.9) | $(\gamma^0-I)u(0)=0$ | 33.3 | 静止系 u 方程 | 推导 |
| (33.10) | $u(0)=(\varphi,0)^T$ | 33.3 | 静止系 u 结构 | 推导 |
| (33.11) | $(\gamma^0+I)v(0)=0$ | 33.3 | 静止系 v 方程 | 推导 |
| (33.12) | $v(0)=(0,\chi)^T$ | 33.3 | 静止系 v 结构 | 推导 |
| (33.13) | $\chi_1=(1,0)^T,\ \chi_2=(0,1)^T$ | 33.3 | Pauli 基 | 推导 |
| (33.14) | $u(0,1),u(0,2),v(0,1),v(0,2)$ 四个解 | 33.3 | 静止系四解 | 推导 |
| (33.15) | $u(p,s)=\sqrt{E_p+m}\begin{pmatrix}\chi_s\\\frac{\sigma\cdot\vec p}{E_p+m}\chi_s\end{pmatrix}$ | 33.4 | 一般动量 u | 推导 |
| (33.16) | $\not p u=\begin{pmatrix}E_p I&-\sigma\cdot\vec p\\\sigma\cdot\vec p&-E_p I\end{pmatrix}\sqrt{E_p+m}\begin{pmatrix}\chi_s\\\cdots\end{pmatrix}$ | 33.4 | p̸u 矩阵作用 | 推导 |
| (33.17) | $E_p\chi_s-\frac{\vec p^{\,2}}{E_p+m}\chi_s=\frac{E_p(E_p+m)-\vec p^{\,2}}{E_p+m}\chi_s$ | 33.4 | 左上块 | 推导 |
| (33.18) | $\not p\,u(p,s)=m\,u(p,s)$ | 33.4 | 验证 (33.4) | 推导 |
| (33.19) | $v(p,s)=\sqrt{E_p+m}\begin{pmatrix}\frac{\sigma\cdot\vec p}{E_p+m}\chi_s\\\chi_s\end{pmatrix}$ | 33.4 | 一般动量 v | 推导 |
| (33.20) | $\not p v=\sqrt{E_p+m}\begin{pmatrix}\cdots\\\cdots\end{pmatrix}$ | 33.4 | p̸v 矩阵作用 | 推导 |
| (33.21) | $\not p\,v=-m\,v,\ (\not p+m)v=0$ | 33.4 | 验证 (33.6) | 推导 |
| (33.22) | $\bar\psi\equiv\psi^\dagger\gamma^0$ | 33.5 | Dirac 伴随 | 推导 |
| (33.23) | $\bar u u=2m\delta_{rs},\ \bar v v=-2m\delta_{rs}$ | 33.5 | 归一化条件 | 推导 |
| (33.24) | $\bar u u=(E_p+m)[\chi_r^\dagger\chi_s-\chi_r^\dagger\frac{(\sigma\cdot p)^2}{(E_p+m)^2}\chi_s]$ | 33.5 | 归一化计算 | 推导 |
| (33.25) | $\bar u u=(E_p+m)[1-\frac{\vec p^{\,2}}{(E_p+m)^2}]\delta_{rs}$ | 33.5 | 化简 | 推导 |
| (33.26) | $\bar u u=2m\delta_{rs}$ | 33.5 | 归一化结果 | 推导 |
| (33.27) | $\bar u v=0,\ \bar v u=0$ | 33.5 | 正交关系 | 推导 |
| (33.28) | $\sum_s u\bar u=\not p+m,\ \sum_s v\bar v=\not p-m$ | 33.5 | 完备投影算符 | 推导 |
| (33.29) | $j^\mu=\bar\psi\gamma^\mu\psi$ | 33.6 | 概率流定义 | 推导 |
| (33.30) | $\gamma^\mu\partial_\mu\psi=-im\psi$ | 33.6 | Dirac 方程重写 | 推导 |
| (33.31) | $(\partial_\mu\psi^\dagger)(\gamma^\mu)^\dagger=im\psi^\dagger$ | 33.6 | Hermite 共轭 | 推导 |
| (33.32) | $(\partial_\mu\psi^\dagger)\gamma^0\gamma^\mu\gamma^0\gamma^0=im\psi^\dagger\gamma^0$ | 33.6 | 右乘 γ⁰ | 推导 |
| (33.33) | $(\partial_\mu\bar\psi)\gamma^\mu=im\bar\psi$ | 33.6 | 伴随方程 | 推导 |
| (33.34) | $\partial_\mu j^\mu=(\partial_\mu\bar\psi)\gamma^\mu\psi+\bar\psi\gamma^\mu\partial_\mu\psi$ | 33.6 | 散度展开 | 推导 |
| (33.35) | $\partial_\mu j^\mu=im\bar\psi\psi-im\bar\psi\psi=0$ | 33.6 | 代入相消 | 推导 |
| (33.36) | $\partial_\mu j^\mu=0$ | 33.6 | 概率守恒 | 推导 |
| (33.37) | $j^0=u^\dagger u$ | 33.6 | 平面波概率密度 | 推导 |
| (33.38) | $u^\dagger u=(E_p+m)[1+\frac{\vec p^{\,2}}{(E_p+m)^2}]$ | 33.6 | 计算 | 推导 |
| (33.39) | $u^\dagger u=2E_p$ | 33.6 | 结果 | 推导 |
| (33.40) | $\bar u\gamma^i u=2p^i$ | 33.6 | 空间流 | 推导 |
| (33.41) | $j^\mu=2p^\mu$ | 33.6 | 流∝四动量 | 推导 |
| (33.42) | $\psi=e^{-imt}(\varphi,\chi)^T$ | 33.7 | 分离静止能量 | 推导 |
| (33.43) | $i\partial_t(\varphi,\chi)^T=\begin{pmatrix}0&\sigma\cdot p\\-\sigma\cdot p&0\end{pmatrix}(\varphi,\chi)^T+m(\varphi,\chi)^T$ | 33.7 | 分量分解 | 推导 |
| (33.44) | $i\partial_t\varphi=\sigma\cdot p\chi,\ i\partial_t\chi=-\sigma\cdot p\varphi+2m\chi$ | 33.7 | 上下分量方程 | 推导 |
| (33.45) | $\chi=\frac{1}{2m}(\sigma\cdot p\varphi-i\partial_t\chi)$ | 33.7 | 解出小分量 | 推导 |
| (33.46) | $\chi\approx\frac{\sigma\cdot p}{2m}\varphi$ | 33.7 | 非相对论近似 | 推导 |
| (33.47) | $i\partial_t\varphi=\frac{(\sigma\cdot p)^2}{2m}\varphi$ | 33.7 | 代入上分量 | 推导 |
| (33.48) | $(\sigma\cdot a)(\sigma\cdot b)=a\cdot b\,I+i\sigma\cdot(a\times b)$ | 33.7 | Pauli 恒等式 | 已证实 |
| (33.49) | $(\sigma\cdot p)^2=\vec p^{\,2}$ | 33.7 | 自点积 | 推导 |
| (33.50) | $i\partial_t\varphi=\frac{\vec p^{\,2}}{2m}\varphi$ | 33.7 | Schrödinger 方程 | 推导 |
| (33.51) | $(\vec p-q\vec A)\times(\vec p-q\vec A)=iq\hbar\vec B$ | 33.7 | 磁场对易子 | 已证实 |
| (33.52) | $(\sigma\cdot(\vec p-q\vec A))^2=(\vec p-q\vec A)^2-q\vec\sigma\cdot\vec B$ | 33.7 | 代入 Pauli 恒等式 | 推导 |
| (33.53) | $i\partial_t\varphi=[\frac{(\vec p-q\vec A)^2}{2m}-q\phi-\frac{q}{2m}\vec\sigma\cdot\vec B]\varphi$ | 33.7 | Pauli 方程 | 已证实 |
| (33.54) | $\vec\mu_s=\frac{q}{m}\vec S=\frac{q}{m}\frac{\vec\sigma}{2},\ g=2$ | 33.7 | 电子磁矩 | 已证实 |
| (33.55) | $E_p=\sqrt{1+0.2611}\approx1.1230\ \mathrm{MeV}$ | 33.8 | 数值例 E_p | 推导 |
| (33.56) | $E_p+m=1.6340\ \mathrm{MeV}$ | 33.8 | 归一化因子 | 推导 |
| (33.57) | $p_z/(E_p+m)\approx0.6120$ | 33.8 | 分量比 | 推导 |
| (33.58) | $u(p,1)=\sqrt{1.6340}(1,0,0.6120,0)^T$ | 33.8 | u 分量 | 推导 |
| (33.59) | $u(p,1)\approx(1.2783,0,0.7823,0)^T$ | 33.8 | 数值 u | 推导 |
| (33.60) | $u^\dagger u\approx2.2461$ | 33.8 | 归一化核对 | 推导 |
| (33.61) | $\bar u u=1.6341-0.6120=1.0221$ | 33.8 | 应等于 2m | 推导 |
| (33.62) | $j^\mu=(2.2460,0,0,2.0)\ \mathrm{MeV}$ | 33.8 | 概率流数值 | 推导 |
| (33.63) | $j^z/j^0\approx0.890$ | 33.8 | 等于 β | 推导 |
| (33.64) | $p_z/(2m)\approx0.9785$ | 33.8 | 非相对论近似偏差 | 推导 |
| (33.65) | $p_z/(E_p+m)\approx0.0970,\ p_z/(2m)\approx0.0978$ | 33.8 | 0.10 MeV 时近似成立 | 推导 |

## A.13 第三十四章 最小耦合代换与 Dirac 拉氏量变分（(34.1)–(34.29)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (34.1) | $\{\gamma^\mu,\gamma^\nu\}=2\eta^{\mu\nu}I_4$ | 34.1 | Clifford 代数（重述） | 已证实 |
| (34.2) | $(i\gamma^\mu\partial_\mu-m)\psi=0$ | 34.1 | 自由 Dirac 方程 | 已证实 |
| (34.3) | $\mathcal L_0=\bar\psi(i\gamma^\mu\partial_\mu-m)\psi$ | 34.2 | 自由 Dirac 拉氏量 | 已证实 |
| (34.4) | $D_\mu\equiv\partial_\mu-iqA_\mu$ | 34.3 | 最小耦合代换 | 已证实 |
| (34.5) | $\vec p\to\vec p-q\vec A,\ E\to E-q\phi$ | 34.3 | 经典正则对应 | 推导 |
| (34.6) | $\mathcal L=\bar\psi(i\gamma^\mu D_\mu-m)\psi=\mathcal L_0-q\bar\psi\gamma^\mu\psi A_\mu$ | 34.4 | 完整 Dirac 拉氏量 | 已证实 |
| (34.7) | $\mathcal L_{\mathrm{int}}=-q\bar\psi\gamma^\mu\psi A_\mu$ | 34.4 | 相互作用项 | 推导 |
| (34.8) | $\mathcal L_{\mathrm{int}}\approx-q\varphi\rho+q\vec A\cdot\vec j$ | 34.4 | 非相对论极限 | 推导 |
| (34.9) | $\delta\mathcal L=(i\gamma^\mu D_\mu-m)\psi\,\delta\bar\psi$ | 34.5 | 对 ψ̄ 变分 | 推导 |
| (34.10) | $(i\gamma^\mu D_\mu-m)\psi=0$ | 34.5 | 变分导出方程 | 已证实 |
| (34.11) | $i\gamma^\mu\partial_\mu\psi-q\gamma^\mu A_\mu\psi-m\psi=0$ | 34.5 | 展开 D_μ | 推导 |
| (34.12) | $i\partial_\mu\bar\psi\gamma^\mu+m\bar\psi+iq\bar\psi\gamma^\mu A_\mu=0$ | 34.5 | 伴随方程 | 推导 |
| (34.13) | $i\partial_t\phi=[\frac{(-i\nabla+e\vec A)^2}{2m}+e\phi-\frac{e}{2m}\vec\sigma\cdot\vec B]\phi$ | 34.5 | Pauli 方程（含 g=2） | 已证实 |
| (34.14) | $\psi\to e^{iq\alpha}\psi,\ A_\mu\to A_\mu+\partial_\mu\alpha$ | 34.6 | U(1) 规范变换 | 推导 |
| (34.15) | $D_\mu'\psi'=e^{iq\alpha}D_\mu\psi$ | 34.6 | D_μ 协变性 | 推导 |
| (34.16) | $\mathcal L'=\mathcal L$ | 34.6 | 拉氏量规范不变 | 推导 |
| (34.17) | $\mathcal L_{\mathrm{int}}'=\mathcal L_{\mathrm{int}}-q\bar\psi\gamma^\mu\psi\,\partial_\mu\alpha$ | 34.6 | 看似多余项 | 推导 |
| (34.18) | $j^\mu=q\bar\psi\gamma^\mu\psi$ | 34.6 | 荷电流 | 推导 |
| (34.19) | $\bar\psi i\gamma^\mu\partial_\mu\psi-i\partial_\mu\bar\psi\gamma^\mu\psi=0$ | 34.6 | 方程相减 | 推导 |
| (34.20) | $i\partial_\mu(\bar\psi\gamma^\mu\psi)=0$ | 34.6 | 流守恒 | 已证实 |
| (34.21) | $(i\gamma^\mu D_\mu-m)\psi=0,\ \partial_\mu F^{\mu\nu}=\mu_0 j^\nu$ | 34.6 | QED 经典骨架 | 已证实 |
| (34.22) | $\Delta E=\hbar\omega_c,\ \omega_c=|q|B_0/m$ | 34.7 | Landau 能级间隔 | 已证实 |
| (34.23) | $\omega_c\approx1.759\times10^{11}\ \mathrm{s^{-1}}$ | 34.7 | 回旋频率数值 | 推导 |
| (34.24) | $\Delta E\approx1.856\times10^{-23}\ \mathrm{J}$ | 34.7 | 间隔焦耳 | 推导 |
| (34.25) | $\Delta E\approx1.16\times10^{-4}\ \mathrm{eV}$ | 34.7 | 间隔电子伏 | 推导 |
| (34.26) | $p_\mu^{\mathrm{eff}}=p_\mu-qA_\mu$ | 34.7 | 有效动量 | 推导 |
| (34.27) | $qA_0c=-1.602\times10^{-15}\ \mathrm{J}$ | 34.7 | 静电势数值 | 推导 |
| (34.28) | $\Delta\alpha=q\int_{z_0}^{z_0+\ell}A_x\,dz/\hbar$ | 34.7 | AB 相位 | 推导 |
| (34.29) | $\Delta\alpha\approx1.52\times10^6\ \mathrm{rad}$ | 34.7 | AB 相位数值 | 推导 |

## A.14 第三十五章 Yang-Mills 非阿贝尔规范场基础（(35.1)–(35.32)，含 (35.6b)(35.6c)(35.27b)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (35.1) | $\psi\to e^{iq\alpha}\psi,\ A_\mu\to A_\mu+\partial_\mu\alpha$ | 35.1 | U(1) 变换（回顾） | 推导 |
| (35.2) | $\Psi\to U(x)\Psi,\ U(x)\in SU(N)$ | 35.1 | 矩阵值相位 | 已证实 |
| (35.3) | $U=1+i\alpha^a T^a+O(\alpha^2)$ | 35.2 | 无穷小展开 | 推导 |
| (35.4) | $[T^a,T^b]\equiv T^aT^b-T^bT^a$ | 35.2 | 对易子定义 | 推导 |
| (35.5) | $[T^a,T^b]=if^{abc}T^c$ | 35.2 | 李代数核心 | 已证实 |
| (35.6) | $f^{abc}=-f^{bac}$ | 35.2 | 前两指标反对称 | 推导 |
| (35.6b) | $[[T^a,T^b],T^c]+[[T^b,T^c],T^a]+[[T^c,T^a],T^b]=0$ | 35.2 | Jacobi 恒等式 | 推导 |
| (35.6c) | $f^{abe}f^{ecd}+f^{bce}f^{ead}+f^{cae}f^{ebd}=0$ | 35.2 | 结构常数 Jacobi | 推导 |
| (35.7) | $\mathrm{Tr}(T^aT^b)=\tfrac12\delta^{ab}$ | 35.2 | 生成元归一化 | 推导 |
| (35.8) | $T^a=\sigma^a/2,\ a=1,2,3$ | 35.3 | SU(2) 生成元 | 已证实 |
| (35.9) | $[T^a,T^b]=\tfrac{i}{2}\varepsilon^{abc}\sigma^c=i\varepsilon^{abc}T^c$ | 35.3 | SU(2) 对易子 | 推导 |
| (35.10) | $f^{abc}=\varepsilon^{abc}$ | 35.3 | SU(2) 结构常数 | 已证实 |
| (35.11) | $A_\mu(x)\equiv A_\mu^a(x)T^a$ | 35.4 | 矩阵值规范场 | 推导 |
| (35.12) | $D_\mu\equiv\partial_\mu-ig\,A_\mu=\partial_\mu-ig\,A_\mu^aT^a$ | 35.4 | 非阿贝尔协变导数 | 已证实 |
| (35.13) | $A_\mu\to U A_\mu U^{-1}+\tfrac{i}{g}(\partial_\mu U)U^{-1}$ | 35.4 | 规范场变换律 | 推导 |
| (35.14) | $D_\mu'\Psi'=U D_\mu\Psi$ | 35.4 | 协变性验算 | 推导 |
| (35.15) | $A_\mu'^a T^a=A_\mu^a T^a+\partial_\mu\alpha^a T^a-ig[\alpha^bT^b,A_\mu^cT^c]$ | 35.4 | 分量展开 | 推导 |
| (35.16) | $A_\mu'^a=A_\mu^a+\partial_\mu\alpha^a+gf^{abc}\alpha^b A_\mu^c$ | 35.4 | 分量变换 | 推导 |
| (35.17) | $F_{\mu\nu}\equiv\frac{i}{g}[D_\mu,D_\nu]$ | 35.5 | 场强定义（对易子） | 推导 |
| (35.18) | $[D_\mu,D_\nu]=[\partial_\mu-igA_\mu,\partial_\nu-igA_\nu]$ | 35.5 | 展开 | 推导 |
| (35.19) | $[D_\mu,D_\nu]=-ig(\partial_\mu A_\nu-\partial_\nu A_\mu)-g^2[A_\mu,A_\nu]$ | 35.5 | 中间式 | 推导 |
| (35.20) | $F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu-ig[A_\mu,A_\nu]$ | 35.5 | 矩阵形式场强 | 推导 |
| (35.21) | $[A_\mu,A_\nu]=i f^{bcd}A_\mu^b A_\nu^c T^d$ | 35.5 | 对易子展开 | 推导 |
| (35.22) | $F^a_{\mu\nu}=\partial_\mu A_\nu^a-\partial_\nu A_\mu^a+gf^{abc}A_\mu^b A_\nu^c$ | 35.5 | 非阿贝尔场强（核心） | 已证实 |
| (35.23) | $F_{\mu\nu}\to U F_{\mu\nu}U^{-1}$ | 35.5 | 场强变换性质 | 推导 |
| (35.24) | $\sigma^1,\sigma^2,\sigma^3$ 矩阵 | 35.5 | Pauli 矩阵数值 | 推导 |
| (35.25) | $\sigma^1\sigma^2=i\sigma^3$ | 35.5 | 乘积数值 | 推导 |
| (35.26) | $\sigma^2\sigma^1=-i\sigma^3$ | 35.5 | 反向乘积 | 推导 |
| (35.27) | $[\sigma^1,\sigma^2]=2i\sigma^3$ | 35.5 | 对易子数值 | 推导 |
| (35.27b) | $f^{147}=f^{246}=f^{257}=f^{345}=\tfrac12,\ f^{458}=f^{678}=\tfrac{\sqrt3}{2}$ | 35.5 | SU(3) 结构常数 | 已证实 |
| (35.28) | $[T^1,T^2]=\tfrac{i}{2}\sigma^3=iT^3$ | 35.5 | 验证 f¹²³=1 | 推导 |
| (35.29) | $A_0^1=1,\ A_i^2=1$ 构型 | 35.5 | 数例 setup | 推导 |
| (35.30) | $F^3_{0i}=g f^{3bc}A_0^b A_i^c$ | 35.5 | 非线性项计算 | 推导 |
| (35.31) | $F^3_{0i}=1.0$ | 35.5 | 数例结果 | 推导 |
| (35.32) | $F^a_{\mu\nu}=\partial_\mu A_\nu^a-\partial_\nu A_\mu^a$ | 35.5 | 阿贝尔退化 | 推导 |

## A.15 第三十六章 Yang-Mills 拉氏量变分（(36.1)–(36.27)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (36.1) | $\mathcal L_{\rm EM}=-\tfrac14 F_{\mu\nu}F^{\mu\nu}$ | 36.1 | Maxwell 拉氏量 | 已证实 |
| (36.2) | $\mathcal L_{\rm YM}=-\tfrac14 F^a_{\mu\nu}F^{a\mu\nu}$ | 36.1 | Yang-Mills 拉氏量 | 已证实 |
| (36.3) | $F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu+gf^{abc}A^b_\mu A^c_\nu$ | 36.1 | 场强（重述） | 已证实 |
| (36.4) | $\delta F^a_{\mu\nu}=\partial_\mu\delta A^a_\nu-\partial_\nu\delta A^a_\mu+gf^{abc}(\delta A^b_\mu A^c_\nu+A^b_\mu\delta A^c_\nu)$ | 36.1 | 场强变分 | 推导 |
| (36.5) | $(D_\mu\chi)^a=\partial_\mu\chi^a+gf^{abc}A^b_\mu\chi^c$ | 36.1 | 伴随表示协变导数 | 推导 |
| (36.6) | $\delta F^a_{\mu\nu}=(D_\mu\delta A_\nu-D_\nu\delta A_\mu)^a$ | 36.1 | 变分协变形式 | 推导 |
| (36.7) | $\delta\mathcal L_{\rm YM}=-\tfrac12 F^{a\mu\nu}\delta F^a_{\mu\nu}$ | 36.2 | 拉氏量变分 | 推导 |
| (36.8) | $\delta\mathcal L_{\rm YM}=-\tfrac12 F^{a\mu\nu}[(D_\mu\delta A_\nu)^a-(D_\nu\delta A_\mu)^a]$ | 36.2 | 代入 (36.6) | 推导 |
| (36.9) | $\delta\mathcal L_{\rm YM}=-F^{a\mu\nu}(D_\mu\delta A_\nu)^a$ | 36.2 | 反对称化 | 推导 |
| (36.10) | $\delta\mathcal L_{\rm YM}=-F^{a\mu\nu}\partial_\mu\delta A^a_\nu-gf^{abc}F^{a\mu\nu}A^b_\mu\delta A^c_\nu$ | 36.2 | 展开 D_μ | 推导 |
| (36.11) | $=\int d^4x\,(\partial_\mu F^{a\mu\nu})\delta A^a_\nu$ | 36.2 | 分部积分后 | 推导 |
| (36.12) | $\partial_\mu F^{c\mu\nu}+gf^{cab}A^a_\mu F^{b\mu\nu}\equiv(D_\mu F)^{c\mu\nu}$ | 36.2 | D_μF 定义 | 推导 |
| (36.13) | $\delta S=\int d^4x\,(D_\mu F^{a\mu\nu})\delta A^a_\nu$ | 36.2 | 作用量变分 | 推导 |
| (36.14) | $D_\mu F^{a\mu\nu}=0$ | 36.2 | Yang-Mills 运动方程 | 已证实 |
| (36.15) | $\partial_\mu F^{a\mu\nu}+gf^{abc}A^b_\mu F^{c\mu\nu}=0$ | 36.2 | 分量展开 | 推导 |
| (36.16) | $D_\mu F^a_{\nu\rho}+D_\nu F^a_{\rho\mu}+D_\rho F^a_{\mu\nu}=0$ | 36.2 | Bianchi 恒等式 | 推导 |
| (36.17) | $D_\mu F^{a\mu\nu}=J^{a\nu}$ | 36.2 | 有源 YM 方程 | 推导 |
| (36.18) | $F^a_{\mu\nu}F^{a\mu\nu}=X^2+2gf^{abc}X A A+g^2f^{abc}f^{ade}A^bA^cA^dA^e$ | 36.3 | 按 A 幂次展开（三/四胶子顶点） | 推导 |
| (36.19) | $\partial_\mu F^{i\mu\nu}+g\epsilon^{ijk}A^j_\mu F^{k\mu\nu}=0$ | 36.3 | SU(2) 分量 | 推导 |
| (36.20) | $f^{abc}=\epsilon^{abc}$ | 36.3 | SU(2) 结构常数 | 已证实 |
| (36.21) | $f^{123}=1,\ f^{147}=\cdots=\tfrac12,\ f^{458}=f^{678}=\tfrac{\sqrt3}{2}$ | 36.3 | SU(3) 数值 | 已证实 |
| (36.22) | $\alpha_s(M_Z)=g_s^2/(4\pi)\approx0.118$ | 36.3 | 强耦合常数 | 已证实 |
| (36.23) | $g_s\approx1.22$ | 36.3 | g_s 数值 | 推导 |
| (36.24) | $T^{\mu\nu}_{\rm YM}=-F^{a\mu\rho}F^{a\nu}{}_\rho+\tfrac14\eta^{\mu\nu}F^a_{\rho\sigma}F^{a\rho\sigma}$ | 36.4 | YM 能量动量张量 | 推导 |
| (36.25) | $q=\frac{g^2}{16\pi^2}\int F^a_{\mu\nu}\tilde F^{a\mu\nu}$ | 36.4 | 瞬子荷 | 已证实 |
| (36.26) | $D_2F^a_{01}+D_0F^a_{12}+D_1F^a_{20}$ | 36.4 | Bianchi 分量 | 推导 |
| (36.27) | $\partial_2(\partial_0A^a_1-\partial_1A^a_0)+\partial_0(\cdots)+\partial_1(\cdots)=0$ | 36.4 | Bianchi 展开为零 | 推导 |

## A.16 第三十七章 标准模型拉氏量逐项拆解（(37.1)–(37.36)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (37.1) | $G_{\rm SM}=U(1)_Y\times SU(2)_L\times SU(3)_c$ | 37.1 | SM 规范群 | 已证实 |
| (37.2) | $B_\mu,\ W^i_\mu,\ G^a_\mu$ | 37.1 | 三类规范场 | 推导 |
| (37.3) | $\mathcal L_g=-\tfrac14 B_{\mu\nu}B^{\mu\nu}-\tfrac14 W^i_{\mu\nu}W^{i\mu\nu}-\tfrac14 G^a_{\mu\nu}G^{a\mu\nu}$ | 37.1 | 规范场动能项 | 已证实 |
| (37.4) | $B_{\mu\nu}=\partial_\mu B_\nu-\partial_\nu B_\mu$ | 37.1 | U(1) 场强 | 推导 |
| (37.5) | $W^i_{\mu\nu}=\partial_\mu W^i_\nu-\partial_\nu W^i_\mu-g_2\epsilon^{ijk}W^j_\mu W^k_\nu$ | 37.1 | SU(2) 场强 | 推导 |
| (37.6) | $G^a_{\mu\nu}=\partial_\mu G^a_\nu-\partial_\nu G^a_\mu-g_3f^{abc}G^b_\mu G^c_\nu$ | 37.1 | SU(3) 场强 | 推导 |
| (37.7) | $L_L=(\nu_L,e_L),\ Q_L=(u_L,d_L),\ e_R,u_R,d_R$ | 37.2 | 费米子多重态 | 推导 |
| (37.8) | 轻子项（行内公式） | 37.2 | 轻子协变导数 | 推导 |
| (37.9) | $\mathcal L_f=\sum_{\rm gen}(\bar L_L i\slashed D L_L+\bar Q_L i\slashed D Q_L+\bar e_R i\slashed D e_R+\cdots)$ | 37.2 | 费米子拉氏量 | 已证实 |
| (37.10) | $Q=T_3+\tfrac{Y}{2}$ | 37.2 | 电荷-同位旋-超荷关系 | 已证实 |
| (37.11) | $(d',s',b')_L=V_{\rm CKM}(d,s,b)_L$ | 37.2 | CKM 混合矩阵 | 已证实 |
| (37.12) | $\phi=(\phi^+,\phi^0),\ Y_\phi=1$ | 37.3 | Higgs 二重态 | 推导 |
| (37.13) | $\mathcal L_\phi=(D_\mu\phi)^\dagger(D^\mu\phi)$ | 37.3 | Higgs 动能 | 推导 |
| (37.14) | $V(\phi)=-\mu^2\phi^\dagger\phi+\lambda(\phi^\dagger\phi)^2$ | 37.3 | Higgs 势 | 推导 |
| (37.15) | $\langle\phi^\dagger\phi\rangle=\mu^2/(2\lambda)=v^2/2$ | 37.3 | 真空期望值 | 推导 |
| (37.16) | $\langle\phi\rangle=(0,v/\sqrt2),\ v=\sqrt{\mu^2/\lambda}$ | 37.3 | 真空位形 | 推导 |
| (37.17) | $\mathcal L_Y=-y_e\bar L_L\phi e_R-y_d\bar Q_L\phi d_R-y_u\bar Q_L\tilde\phi u_R+\mathrm{h.c.}$ | 37.3 | Yukawa 耦合 | 已证实 |
| (37.18) | $m_e=y_e v/\sqrt2$ | 37.3 | 费米子质量 | 推导 |
| (37.19) | $W^\pm_\mu=(W^1_\mu\mp iW^2_\mu)/\sqrt2$ | 37.4 | W 玻色子定义 | 推导 |
| (37.20) | $A_\mu=\cos\theta_W B_\mu+\sin\theta_W W^3_\mu,\ Z_\mu=-\sin\theta_W B_\mu+\cos\theta_W W^3_\mu$ | 37.4 | 电弱混合 | 推导 |
| (37.21) | $\sin^2\theta_W=g_1^2/(g_1^2+g_2^2)$ | 37.4 | 弱混合角 | 推导 |
| (37.22) | $m_W=g_2 v/2,\ m_Z=m_W/\cos\theta_W$ | 37.4 | W/Z 质量 | 已证实 |
| (37.23) | $m_H^2=2\lambda v^2$ | 37.4 | Higgs 质量 | 推导 |
| (37.24) | $v\approx246.2\ \mathrm{GeV}$ | 37.4 | 真空期望值数值 | 已证实 |
| (37.25) | $m_W\approx80.4\ \mathrm{GeV}$ | 37.4 | W 质量数值 | 已证实 |
| (37.26) | $m_Z\approx91.2\ \mathrm{GeV}$ | 37.4 | Z 质量数值 | 已证实 |
| (37.27) | $y_t\approx0.994$ | 37.4 | 顶 Yukawa 数值 | 推导 |
| (37.28) | $\lambda\approx0.129$ | 37.4 | Higgs 自耦合数值 | 推导 |
| (37.29) | $D_\mu\phi=(\partial_\mu-ig_2\tfrac{\sigma^i}{2}W^i_\mu-ig_1\tfrac{Y}{2}B_\mu)\phi$ | 37.5 | Higgs 协变导数 | 推导 |
| (37.30) | $=(-ig_2 v/(2\sqrt2))(W^1_\mu,0)^T$ | 37.5 | 动能项展开 | 推导 |
| (37.31) | $m_W=g_2 v/2$ | 37.5 | 再得 W 质量 | 推导 |
| (37.32) | $m_Z^2=v^2(g_1^2+g_2^2)/4,\ m_A=0$ | 37.5 | Z/光子质量 | 推导 |
| (37.33) | 第一代费米子 | 37.6 | 第一代 | 推导 |
| (37.34) | 第二、三代费米子 | 37.6 | 二三代 | 推导 |
| (37.35) | $1/\alpha_i(\mu)=1/\alpha_i(M_Z)+\frac{b_i}{2\pi}\ln(\mu/M_Z)$ | 37.6 | 耦合常数跑动 | 推导 |
| (37.36) | $\mathcal L_{\rm SM}=\mathcal L_g+\mathcal L_f+(D_\mu\phi)^\dagger(D^\mu\phi)-V(\phi)+\mathcal L_Y$ | 37.6 | SM 完整拉氏量 | 已证实 |

## A.17 第三十八章 四相互作用映射回机电对偶范式（(38.1)–(38.24)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (38.1) | $m\ddot x+kx=0,\ L\ddot q+\frac{1}{C}q=0$ | 38.1 | 振子-电路同构（重述） | 已证实 |
| (38.2) | $\omega_0^2=K/A=m^2c^4/\hbar^2\Rightarrow\hbar\omega_0=mc^2$ | 38.1 | 本源回环（重述） | 推导 |
| (38.3) | $\Box A_\mu=0$ | 38.2 | 真空 Maxwell 波动方程 | 已证实 |
| (38.4) | $k_\mu k^\mu=0\Rightarrow\omega=ck\Rightarrow\omega/k=c$ | 38.2 | 真空光速 | 推导 |
| (38.5) | $c=1/\sqrt{\mu_0\varepsilon_0}=299792458\ \mathrm{m/s}$ | 38.2 | 光速数值 | 已证实 |
| (38.6) | $(\Box+\kappa_V^2)A^V_\mu=0,\ \kappa_V=m_Vc/\hbar$ | 38.3 | 有质量矢量场方程 | 推导 |
| (38.7) | $\omega^2=c^2(k^2+\kappa_V^2)$ | 38.3 | 有质量色散 | 推导 |
| (38.8) | $v_g=c\sqrt{1-\kappa_V^2/(k^2+\kappa_V^2)}<c$ | 38.3 | 有质量群速 | 推导 |
| (38.9) | $\omega_{0,V}=m_Vc^2/\hbar$ | 38.3 | 本征频率 | 推导 |
| (38.10) | $\omega_{0,W}\approx1.221\times10^{26}\ \mathrm{rad/s}$ | 38.3 | W 玻色子本征频率 | 推导 |
| (38.11) | $D_\mu F^{a\mu\nu}=0,\ F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu+g_s f^{abc}A^b_\mu A^c_\nu$ | 38.4 | YM 方程 | 已证实 |
| (38.12) | $\Box A^a_\mu=0$ | 38.4 | YM 线性化 | 推导 |
| (38.13) | $R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}=\tfrac{8\pi G}{c^4}T_{\mu\nu}$ | 38.5 | Einstein 方程 | 已证实 |
| (38.14) | $\Box\bar h_{\mu\nu}=0$ | 38.5 | 线性化引力波 | 已证实 |
| (38.15) | $t_{\rm dist}\approx4.10\times10^{15}\ \mathrm{s}$ | 38.5 | GW170817 传播时间 | 推导 |
| (38.16) | $\lvert v_{\rm GW}-c\rvert/c\lesssim4.1\times10^{-16}$ | 38.5 | GW 速度约束 | 已证实 |
| (38.17) | $Z_0=\sqrt{\mu_0/\varepsilon_0}$ | 38.6 | 真空阻抗 | 推导 |
| (38.18) | $Z_0\approx376.73\ \Omega$ | 38.6 | 真空阻抗数值 | 已证实 |
| (38.19) | $-\nabla^2 A_0^V+\kappa_V^2 A_0^V=J^0$ | 38.6 | 静态势方程 | 推导 |
| (38.20) | $A_0^V(r)=\frac{g_V}{4\pi}\frac{e^{-\kappa_V r}}{r}$ | 38.6 | Yukawa 势 | 已证实 |
| (38.21) | $G_F/\sqrt2=g^2/(8m_W^2c^4)$ | 38.6 | Fermi 常数关系 | 已证实 |
| (38.22) | $\omega_{0,p}\approx1.426\times10^{24}\ \mathrm{rad/s}$ | 38.6 | 质子本征频率 | 推导 |
| (38.23) | $\tfrac{1}{c^2}\partial_t^2\phi-\partial_x^2\phi+\kappa_V^2\phi=0$ | 38.7 | 一维波动方程 | 推导 |
| (38.24) | $\tfrac{1}{c^2}(\partial_t S)^2-(\partial_x S)^2=0$ | 38.7 | eikonal 方程 | 推导 |

## A.18 第三十九章 标准模型缺陷与 TUFT 切入（(39.1)–(39.13)）

| 编号 | 公式（LaTeX） | 出处 | 一句话物理含义 | 所属层 |
|---|---|---|---|---|
| (39.1) | $R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}=\tfrac{8\pi G}{c^4}T_{\mu\nu}$ | 39.1 | Einstein 方程（重述） | 已证实 |
| (39.2) | $\rho(r)\propto1/[r(r+a)^2]$ | 39.1 | NFW 暗物质密度轮廓 | 已证实 |
| (39.3) | $\ddot a/a=-\frac{4\pi G}{3c^2}(\rho+3p)+\Lambda c^2/3$ | 39.1 | Friedmann 方程 | 已证实 |
| (39.4) | $\rho_\Lambda=\Lambda c^2/(8\pi G)\approx5.96\times10^{-27}\ \mathrm{kg/m^3}$ | 39.1 | 暗能量密度 | 已证实 |
| (39.5) | $\rho_{\rm vac}^{\rm QFT}\sim10^{112}\ \mathrm{erg/cm^3}$ | 39.1 | QFT 真空能估算 | 推导 |
| (39.6) | $\rho_{\rm vac}^{\rm QFT}/\rho_\Lambda\sim10^{120}$ | 39.1 | 宇宙学常数问题 | 推导 |
| (39.7) | $\Delta m_{21}^2\approx7.5\times10^{-5}\ \mathrm{eV^2},\ \lvert\Delta m_{31}^2\rvert\approx2.5\times10^{-3}\ \mathrm{eV^2}$ | 39.1 | 中微子质量平方差 | 已证实 |
| (39.8) | $m_{\rm tor}c^2\sim2\pi R\,\mu$ | 39.2 | 环面涡旋暗物质质量估计 | 假说 |
| (39.9) | $\rho_n\propto L_n^{-4}b^{-\beta n}$ | 39.2 | 分形真空能贡献 | 假说 |
| (39.10) | $\rho_{\rm eff}\propto L_0^{-4}\sum_{n=0}^{N}b^{-(4+\beta n)}$ | 39.2 | 等比重整级数 | 假说 |
| (39.11) | $\ell_p=\sqrt{\hbar G/c^3}\approx1.616\times10^{-35}\ \mathrm{m}$ | 39.1 | 普朗克长度 | 已证实 |
| (39.12) | $\rho_\Lambda=\rho_{\rm vac}^{\rm QFT}-\rho_{\rm cancel}\approx10^{-9}\ \mathrm{erg/cm^3}$ | 39.1 | 精细抵消图景 | 假说 |
| (39.13) | $m_\nu\approx m_D^2/M_R$ | 39.1 | Seesaw 机制 | 推导 |

## A.19 TUFT 原创公式分区（(TUFT-1)–(TUFT-81)，含子号）

> 本分区收录第四十章至第四十七章 TUFT 原创公式，**全部为【TUFT假说】层**，数学自洽但未经实验证实。预言子标号 P-TUFT-19a–e、P-TUFT-20a–c、P-TUFT-21a–r 是正文中的预言子标号（非方程 \tag），一并登记以便交叉引用。

| 编号 | 公式（LaTeX） | 出处章 | 一句话含义 | 所属层 |
|---|---|---|---|---|
| (TUFT-1) | $\mathcal M_4\mapsto\{g_{\mu\nu},T^\mu,N^\mu,B^\mu,\kappa(x),\tau(x)\}$ | 40 | 公理一：时空涡旋基底 | TUFT假说 |
| (TUFT-2) | $v_{\rm phase}(\omega)=c,\ \forall\omega$ | 40 | 公理二：v=c 不变对偶 | TUFT假说 |
| (TUFT-2a) | $\varepsilon_{\rm eff}=\varepsilon_0(1+\eta\,\kappa^2\ell_p^2)$ | 40 | 曲率对介电常数修正 | TUFT假说 |
| (TUFT-3) | $DQ_{\mathcal T}/d\tau=0$ | 40 | 公理三：拓扑荷协变守恒 | TUFT假说 |
| (TUFT-4) | $D_\mu\mathcal J^\mu=0$ | 40 | 拓扑荷流守恒 | TUFT假说 |
| (TUFT-5) | $\mathcal L[bx]=b^{-\alpha}\mathcal L[x]$ | 40 | 公理四：分形自相似 | TUFT假说 |
| (TUFT-6) | $\mathcal F^{\mu\nu}=\mathcal F^{\mu\nu}(g_{\rho\sigma},\kappa,\tau),\ \kappa=\kappa(\mathcal F),\ \tau=\tau(\mathcal F)$ | 40 | 公理五：场-几何双向耦合 | TUFT假说 |
| (TUFT-7) | $T'(s)=\kappa(s)N(s),\ \kappa=\lvert T'\rvert,\ N=T'/\kappa$ | 41 | Frenet：T 的导数 | 推导（几何标准） |
| (TUFT-8) | $B'(s)=-\tau(s)N(s)$ | 41 | Frenet：B 的导数 | 推导 |
| (TUFT-9) | $N'=-\kappa T+\tau B$ | 41 | Frenet：N 的导数 | 推导 |
| (TUFT-10) | Frenet-Serret 三式联立 | 41 | F-S 方程组 | 推导 |
| (TUFT-11) | $\frac{d}{ds}(T,N,B)^T=\Omega\begin{pmatrix}T\\N\\B\end{pmatrix}$ | 41 | 3×3 矩阵形式 | 推导 |
| (TUFT-12) | $DT^\mu/d\tau=\kappa_1 N_1^\mu+\kappa_2 N_2^\mu+\kappa_3 N_3^\mu$ | 41 | 四维提升：T 的导数 | TUFT假说 |
| (TUFT-13) | $DN_i^\mu/d\tau=-\kappa_i T^\mu+\sum_j\tau_{ij}N_j^\mu$ | 41 | 四维提升：N_i 的导数 | TUFT假说 |
| (TUFT-14) | 4×4 矩阵形式 $(T,N_1,N_2,N_3)$ | 41 | 四维 F-S 矩阵 | TUFT假说 |
| (TUFT-15) | $\nabla_\mu e_\beta=\Omega_\mu{}^\alpha{}_\beta e_\alpha$ | 41 | 标架联络 | 推导 |
| (TUFT-16) | $\mathcal R_{\mu\nu}{}^\alpha{}_\beta=\partial_\mu\Omega_\nu-\partial_\nu\Omega_\mu+\Omega_\mu\Omega_\nu-\Omega_\nu\Omega_\mu$ | 41 | 曲率张量 | 推导 |
| (TUFT-17) | $\mathcal D_{[\lambda}\mathcal R_{\mu\nu]}{}^\alpha{}_\beta=0$ | 41 | 曲率 Bianchi | 推导 |
| (TUFT-18) | $\boldsymbol B'=-\tau\boldsymbol N$ | 42 | 矢量 B 的导数 | 推导 |
| (TUFT-19) | $\Omega=\begin{pmatrix}0&\kappa&0\\-\kappa&0&\tau\\0&-\tau&0\end{pmatrix}$ | 42 | 涡旋联络矩阵 | TUFT假说 |
| (TUFT-20) | $g_{\mu\nu}B^\mu B^\nu=-1,\ g_{\mu\nu}R^\mu R^\nu=1$ | 42 | 伪正交归一 | TUFT假说 |
| (TUFT-21) | $\nabla_s B^\mu=-\tau N^\mu$ | 42 | 沿世界线 B 的协变导数 | TUFT假说 |
| (TUFT-22) | $\partial_t\boldsymbol\omega-\nabla\times(\boldsymbol v\times\boldsymbol\omega)=0$ | 42 | 涡旋量演化（无黏） | 推导 |
| (TUFT-23) | $\nabla\cdot\boldsymbol\omega=0$ | 42 | 涡旋量无散 | 推导 |
| (TUFT-24) | $F_{\rm em}^{\mu\nu}=\partial^\mu A^\nu-\partial^\nu A^\mu$ | 42 | 标准电磁场张量 | 已证实 |
| (TUFT-25) | $\mathcal F^{\mu\nu}=\partial^\mu A^\nu-\partial^\nu A^\mu+G^{\mu\nu}(\kappa,\tau)$ | 42 | TUFT 场张量（含 G 修正） | TUFT假说 |
| (TUFT-26) | $G^{\mu\nu}=\kappa(x)T^{[\mu}R^{\nu]}+\tau(x)N^{[\mu}B^{\nu]}$ | 42 | G 的构造 | TUFT假说 |
| (TUFT-27) | $D_\mu=\partial_\mu+\Gamma_\mu+\mathcal F_\mu$ | 42 | 分形协变导数 | TUFT假说 |
| (TUFT-28) | $D_\mu V^\nu=\partial_\mu V^\nu+\Gamma_{\mu\alpha}{}^\nu V^\alpha+\mathcal F_{\mu\alpha}{}^\nu V^\alpha$ | 42 | 逆变分量作用 | TUFT假说 |
| (TUFT-29) | $D_\mu\omega_\nu=\partial_\mu\omega_\nu-\Gamma_{\mu\nu}{}^\alpha\omega_\alpha-\mathcal F_{\mu\nu}{}^\alpha\omega_\alpha$ | 42 | 协变分量作用 | TUFT假说 |
| (TUFT-30) | $D_\mu\mathcal F^{\mu\nu}=\partial_\mu\mathcal F^{\mu\nu}+\Gamma\cdots+\mathcal F\cdots$ | 42 | D_μF 展开 | TUFT假说 |
| (TUFT-31) | $D_\lambda G_{\mu\nu}+D_\mu G_{\nu\lambda}+D_\nu G_{\lambda\mu}=0$ | 42 | G 的 Bianchi | TUFT假说 |
| (TUFT-32) | $D_\mu\mathcal F^{\mu\nu}+\kappa\mathcal J^\nu+\tau\mathcal K^\nu=\mathcal S^\nu$ | 42 | **TUFT 主方程** | TUFT假说 |
| (TUFT-33) | $\partial_\mu F_{\rm em}^{\mu\nu}=\mathcal S^\nu$ | 42 | 低能退化到 Maxwell | 推导 |
| (TUFT-34) | $\partial_\lambda F_{\mu\nu}+\partial_\mu F_{\nu\lambda}+\partial_\nu F_{\lambda\mu}=0$ | 43 | 标准 Bianchi | 已证实 |
| (TUFT-35) | $D_\lambda\mathcal F_{\mu\nu}+D_\mu\mathcal F_{\nu\lambda}+D_\nu\mathcal F_{\lambda\mu}=0$ | 43 | TUFT Bianchi | TUFT假说 |
| (TUFT-36) | $D_\mu D_\nu\mathcal F^{\mu\nu}-D_\nu D_\mu\mathcal F^{\mu\nu}=[D_\mu,D_\nu]\mathcal F^{\mu\nu}$ | 43 | 对易子展开 | 推导 |
| (TUFT-37) | $D_\mu D_\nu\mathcal F^{\mu\nu}=0$ | 43 | Bianchi 推论 | TUFT假说 |
| (TUFT-38) | $D_\mu\mathcal F^{\mu\nu}=-\kappa\mathcal J^\nu-\tau\mathcal K^\nu+\mathcal S^\nu$ | 43 | 主方程移项 | TUFT假说 |
| (TUFT-39) | $D_\nu(\kappa\mathcal J^\nu)=(\partial_\nu\kappa)\mathcal J^\nu+\kappa D_\nu\mathcal J^\nu$ | 43 | Leibniz 展开 | 推导 |
| (TUFT-40) | $D_\nu(\tau\mathcal K^\nu)=(\partial_\nu\tau)\mathcal K^\nu+\tau D_\nu\mathcal K^\nu$ | 43 | Leibniz 展开 | 推导 |
| (TUFT-41) | $(\partial_\nu\kappa)\mathcal J^\nu+\kappa D_\nu\mathcal J^\nu+(\partial_\nu\tau)\mathcal K^\nu+\tau D_\nu\mathcal K^\nu=D_\nu\mathcal S^\nu$ | 43 | 散度主方程 | TUFT假说 |
| (TUFT-42) | $\kappa D_\nu\mathcal J^\nu+\tau D_\nu\mathcal K^\nu=0$ | 43 | 交叉项约束 | TUFT假说 |
| (TUFT-43) | $D_\nu\mathcal J^\nu=0$ | 43 | 拓扑荷流守恒 | TUFT假说 |
| (TUFT-44) | $Q_{\mathcal T}=\int_\Sigma\mathcal J^\nu d\Sigma_\nu$ | 43 | 拓扑荷定义 | TUFT假说 |
| (TUFT-45) | $\partial_\mu F_{\rm em}^{\mu\nu}=\mathcal S^\nu$ | 43 | 低能 Maxwell | 推导 |
| (TUFT-46) | $R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}^{\rm eff}$ | 43 | 低能广义相对论 | 推导 |
| (TUFT-47) | $\mathcal F^{\mu\nu}=\partial^\mu A^\nu-\partial^\nu A^\mu+G^{\mu\nu}(\kappa,\tau)$ | 44 | 主方程场张量（重述） | TUFT假说 |
| (TUFT-48) | $G^{\mu\nu}=\alpha_g(\kappa\,\varepsilon^{\mu\nu\rho\sigma}T_\rho B_\sigma+\tau\,\varepsilon^{\mu\nu\rho\sigma}T_\rho N_\sigma)$ | 44 | G 的显式构造 | TUFT假说 |
| (TUFT-49) | $\partial_{[\lambda}\mathcal F_{\mu\nu]}=\partial_{[\lambda}G_{\mu\nu]}$ | 44 | Bianchi 约束 | TUFT假说 |
| (TUFT-50) | $\mathcal D_\mu(\partial^\mu A^\nu-\partial^\nu A^\mu+G^{\mu\nu})+\kappa\mathcal J^\nu+\tau\mathcal K^\nu=\mathcal S^\nu$ | 44 | 完整主方程 | TUFT假说 |
| (TUFT-51) | $d\kappa/d\tau=\alpha_\kappa(I_1-\langle I_1\rangle_0)+\beta_\kappa(I_2-\langle I_2\rangle_0)$ | 44 | 曲率反作用方程 | TUFT假说 |
| (TUFT-52) | $d\tau/d\tau=\alpha_\tau(I_2-\langle I_2\rangle_0)+\beta_\tau(I_1-\langle I_1\rangle_0)$ | 44 | 挠率反作用方程 | TUFT假说 |
| (TUFT-53) | 闭合四方程组（场方程+反作用×2） | 44 | 自治系统 | TUFT假说 |
| (TUFT-54) | $G^{\mu\nu}\approx\alpha_g(\delta\kappa\,\varepsilon T_\rho B_\sigma+\delta\tau\,\varepsilon T_\rho N_\sigma)$ | 44 | 线性化 G | TUFT假说 |
| (TUFT-55) | $h_{\mu\nu}\approx\eta_{\mu\rho}\eta_{\nu\sigma}G^{\rho\lambda}G_\lambda{}^\sigma/\kappa_c^2$ | 44 | 度规修正 | TUFT假说 |
| (TUFT-56) | $A_n\Box_n\Phi_n+\frac{K_n}{c^2}\Phi_n=J_n$ | 45 | 层级 n 上的场方程 | TUFT假说 |
| (TUFT-57) | $\Psi_{n'}=\mathcal P_{n\to n'}\Phi_n=\frac{1}{\sqrt{V}}\int\Phi_n(y)\mu(y,x)d^4y$ | 45 | 投影算子 | TUFT假说 |
| (TUFT-58) | $\tilde\Phi_n=\mathcal P^\dagger_{n'\to n}\Psi_{n'}$ | 45 | 反投影算子 | TUFT假说 |
| (TUFT-58a) | $\mu(y,x)=\frac{1}{(2\pi\sigma^2)^2}\exp(-(y-x)^2/(2\sigma^2))$ | 45 | 投影核（高斯） | TUFT假说 |
| (TUFT-58b) | $\mu(y,x)\to\mu(\boldsymbol y,\boldsymbol x)\Theta(t_y-t_x)$ | 45 | 推迟核（因果） | TUFT假说 |
| (TUFT-59) | $A_n\mathcal P\Box_n\Phi_n+\frac{K_n}{c^2}\mathcal P\Phi_n=\mathcal P J_n$ | 45 | 投影主方程 | TUFT假说 |
| (TUFT-60) | $A_n\Box_{n'}\Psi_{n'}+\frac{K_n}{c^2}\Psi_{n'}=\mathcal P J_n$ | 45 | 投影后方程 | TUFT假说 |
| (TUFT-61) | $\Box_{n'}\Psi_{n'}+\frac{K_n}{A_n c^2}\Psi_{n'}=0$ | 45 | 自由投影方程 | TUFT假说 |
| (TUFT-62) | $\hbar\omega_{n,n'}=m_{n,n'}c^2+\Delta_{n\to n'}(t)$ | 45 | 分形修正质量关系 | TUFT假说 |
| (TUFT-63) | $\omega_{n',c}=\frac{m_{n'}c^2}{\hbar}=\omega_0\alpha^{-n'/2}Z_{n\to n'}$ | 45 | 频率塔 | TUFT假说 |
| (TUFT-64) | 对偶闭合方程组（case 形式） | 45 | 场-粒子对偶闭合 | TUFT假说 |
| (TUFT-65) | $\partial_\mu j_n^\mu=0,\ j_n^\mu=\frac{i}{2}(\Phi_n^*\partial^\mu\Phi_n-\Phi_n\partial^\mu\Phi_n^*)$ | 45 | 层级流守恒 | TUFT假说 |
| (TUFT-66) | $\omega_{0,c}=m_e c^2/\hbar\approx7.76\times10^{20}\ \mathrm{rad/s}$ | 45 | 电子 Compton 频率 | 推导 |
| (TUFT-67) | $Z_{n\to n'}\approx\exp(-l_{n\to n'}^2/(4\sigma^2))$ | 45 | 投影重整化因子 | TUFT假说 |
| (TUFT-68) | $\mathcal I_b[\Phi](x)=b^{\Delta_\Phi}\Phi(bx)$ | 46 | 迭代算子定义 | TUFT假说 |
| (TUFT-69) | $m(b)=b\,m_0$ | 46 | 质量标度律 | TUFT假说 |
| (TUFT-70) | $\mathcal I_b\mathcal L\mathcal I_b^{-1}=b^2\mathcal L$ | 46 | 拉氏量自相似 | TUFT假说 |
| (TUFT-71) | $G_{\rm eff}(l)=G_0(l/l_0)^\delta$ | 46 | 有效引力常数标度 | TUFT假说 |
| (TUFT-72) | $\mathcal P_b[\psi](X)=\int K_b(X-x)\psi(x)d^4x$ | 46 | 块自旋变换 | 推导 |
| (TUFT-73) | $m_n=m_0 b^n$ | 46 | 离散质量塔 | TUFT假说 |
| (TUFT-74) | $\mathcal I_b[\mathcal S](x)=b^{4+\Delta_\mathcal S}\mathcal S(bx)$ | 46 | 源项标度 | TUFT假说 |
| (TUFT-75) | $\mathcal D_\tau:g_{\mu\nu}\leftrightarrow\mathcal F^{\mu\nu},\ \tau\neq0$ | 47 | 引力-场对偶映射 | TUFT假说 |
| (TUFT-76) | $R_{\mu\nu}-\tfrac12 Rg_{\mu\nu}+\Lambda g_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}+\tau\mathcal G_{\mu\nu}$ | 47 | 修正 Einstein 方程 | TUFT假说 |
| (TUFT-77) | $d\sigma/d\Omega|_{\rm TUFT}=d\sigma/d\Omega|_{\rm SM}[1+\alpha_\tau f_\tau(E_{\rm cm}/\Lambda_\tau)]$ | 47 | 散射截面修正 | TUFT假说 |
| (TUFT-78) | $(g-2)_{\rm TUFT}/2=a_{\rm SM}/2+\Delta a_\tau,\ \Delta a_\tau\sim(\alpha_\tau/\pi)(m/\Lambda_\tau)^2$ | 47 | 反常磁矩修正 | TUFT假说 |
| (TUFT-79) | $P(k)=P_{\rm CDM}(k)[1+\beta_\delta\ln(k/k_0)]$ | 47 | 功率谱对数修正 | TUFT假说 |
| (TUFT-80) | $A_S/A_+\sim\tau/\kappa,\ A_V/A_+\sim\tau/\kappa$ | 47 | 标量/矢量振幅比 | TUFT假说 |
| (TUFT-81) | $\omega_n=\omega_0 b^{n/2},\ n=1,2,3,\ldots$ | 47 | 离散频率塔 | TUFT假说 |

### A.19.1 TUFT 预言子标号登记（P-TUFT-19a–e、P-TUFT-20a–c、P-TUFT-21a–r）

> 以下为正文中的预言子标号（非方程 \tag{}），登记以便交叉引用。

| 子标号 | 出处章 | 一句话内容 | 所属层 |
|---|---|---|---|
| P-TUFT-19a | 44 | $\alpha_g$ 取值被太阳系与脉冲星观测夹逼 | TUFT假说 |
| P-TUFT-19b | 44 | 曲率涡旋激发阈值 $E_c$ | TUFT假说 |
| P-TUFT-19c | 44 | 赝标量 $I_2$ 仅在非平凡 E·B 构型非零 | TUFT假说 |
| P-TUFT-19d | 44 | 闭合方程组对初值敏感（混沌） | TUFT假说 |
| P-TUFT-19e | 44 | 曲率梯度牵引拓扑荷流（喷流偏差） | TUFT假说 |
| P-TUFT-20a | 44 | 普朗克曲率附近 G 项主导（CMB B 模） | TUFT假说 |
| P-TUFT-20b | 44 | 挠率累积致引力波相位漂移 | TUFT假说 |
| P-TUFT-20c | 44 | 几何-场余振延迟引力波尾 | TUFT假说 |
| P-TUFT-21a | 45 | 跨层级场涨落在散射截面留尾巴 | TUFT假说 |
| P-TUFT-21b | 45 | 投影损失信息=真空涨落 | TUFT假说 |
| P-TUFT-21c | 45 | 投影源项频谱分形自相似 | TUFT假说 |
| P-TUFT-21d | 45 | 静质量时间漂移 | TUFT假说 |
| P-TUFT-21e | 45 | 分形质量比 $m_{n'}/m_n=\alpha^{(n-n')/2}Z$ | TUFT假说 |
| P-TUFT-21f | 45 | 高能旋量双线性型修正 | TUFT假说 |
| P-TUFT-21g | 45 | 场涨落↔粒子凝聚循环 | TUFT假说 |
| P-TUFT-21h | 45 | 粒子数分形长程关联 | TUFT假说 |
| P-TUFT-21i | 45 | 宏观层级集体振荡频率（超流） | TUFT假说 |
| P-TUFT-21j | 45 | 三窗口联合检验 | TUFT假说 |
| P-TUFT-21k | 45 | 投影核宽度 $\sigma_{n\to n'}=\sigma_0\alpha^{\lvert n-n'\rvert/2}$ | TUFT假说 |
| P-TUFT-21l | 45 | 推迟核致时间反演微小破坏 | TUFT假说 |
| P-TUFT-21m | 45 | 场涨落谱=粒子产生谱（对偶） | TUFT假说 |
| P-TUFT-21n | 45 | 隔层投影效应应远小于相邻层 | TUFT假说 |
| P-TUFT-21o | 45 | 超导 LC 高阶集体振荡模 | TUFT假说 |
| P-TUFT-21p | 45 | 拓扑荷/分形/因果畴交叉验证 | TUFT假说 |
| P-TUFT-21q | 45 | 跨层级投影致质量比漂移 | TUFT假说 |
| P-TUFT-21r | 45 | 量子化后散射振幅修正 | TUFT假说 |

## A.20 统计小结

- **正书 ch01–ch10 收录**：19+20+33+37+23+15+26+19+13+2 = **207** 条。
- **ch32–ch39 补录**：49（ch32，含 32.24a–g）+ 65（ch33）+ 29（ch34）+ 35（ch35，含 35.6b/c、35.27b）+ 27（ch36）+ 36（ch37）+ 24（ch38）+ 13（ch39）= **278** 条。
- **TUFT 原创分区**：(TUFT-1)–(TUFT-81) 共 **81** 条主公式，含子号 (TUFT-2a)、(TUFT-58a)、(TUFT-58b) 共 **3** 条子式；预言子标号 P-TUFT-19a–e、P-TUFT-20a–c、P-TUFT-21a–r 共 **26** 条。
- **合计登记**：207 + 278 + 81 + 3 + 26 = **595** 条。
- 分层：【已证实】与【推导】覆盖 ch01–ch39 全部标准物理；【TUFT假说】覆盖 ch40–ch47 全部 TUFT 公式及 ch39 中 (39.8)–(39.10)、(39.12) 等本书早期假说。
- 编号 (8.15a/b)、(32.24a–g)、(35.6b/c)、(35.27b)、(TUFT-2a)、(TUFT-58a/b) 均为正文主编号之下的子式，单独列出以便交叉引用。

> 本总表与正文 `manuscript/chNN-*.md` 一一对应；如正文后续修订编号，本表应同步更新。
