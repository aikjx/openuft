# 附录A 核心方程速查表

## A.1 三大本源公理

| 公理 | 表达式 |
|------|--------|
| Ⅰ 速率守恒 | $v_\perp^2 + h^2 = c^2$ |
| Ⅱ Frenet-Serret | $d\boldsymbol{T}/ds=\kappa\boldsymbol{N},\ d\boldsymbol{N}/ds=-\kappa\boldsymbol{T}+\tau\boldsymbol{B},\ d\boldsymbol{B}/ds=-\tau\boldsymbol{N}$ |
| Ⅲ 拓扑-物理对应 | 全部物理量 = $\mathcal{F}[\kappa, \tau, \omega, \mathrm{Lk}, \mathrm{Tw}, \mathrm{Wr}]$ |

## A.2 圆柱螺旋几何

| 物理量 | 表达式 |
|--------|--------|
| 参数方程 | $\boldsymbol{r}(t) = (R\cos\omega t, R\sin\omega t, ht)$ |
| 切向速率 | $v_\perp = R\omega$ |
| 曲率 | $\kappa = R\omega^2/c^2 = (\omega/c)\sin\theta$ |
| 挠率 | $\tau = h\omega/c^2 = (\omega/c)\cos\theta$ |
| 升角 | $\sin\theta = v_\perp/c,\ \cos\theta = h/c$ |
| 核心恒等式1 | $\tan\theta = \kappa/\tau$ |
| 核心恒等式2 | $\omega = c\sqrt{\kappa^2+\tau^2}$ |

## A.3 拓扑自旋

| 物理量 | 表达式 |
|--------|--------|
| 扭转数 | $\mathrm{Tw} = (1/2\pi)\oint \tau\,ds = \cos\theta$ |
| Călugăreanu-White | $\mathrm{Lk} = \mathrm{Tw} + \mathrm{Wr}$ |
| 自旋拓扑数 | $s = \sin^2\theta$ |
| 拓扑恒等式 | $s + \mathrm{Lk}^2 = 1$ |
| 玻色子孤子 | $s=1 \Rightarrow \theta=90^\circ,\ \tau=0$ |
| 费米子孤子 | $s=1/2 \Rightarrow \theta=45^\circ,\ \kappa=\tau$ |

## A.4 拓扑质量

| 物理量 | 表达式 |
|--------|--------|
| 孤子量子化 | $mc^2 = \hbar\omega$ |
| 拓扑质量 | $m = (\hbar/c)\sqrt{\kappa^2+\tau^2}$ |
| 普朗克质量 | $m_{Pl} = \sqrt{\hbar c/G}$ |
| 普朗克长度 | $l_{Pl} = \sqrt{\hbar G/c^3}$ |
| 普朗克时间 | $t_{Pl} = \sqrt{\hbar G/c^5}$ |

## A.5 引力理论

| 物理量 | 表达式 |
|--------|--------|
| 全局惯性比 | $\beta_1 = (\kappa^2+\tau^2)/\langle\kappa_0^2+\tau_0^2\rangle$ |
| 引力对数律 | $\boldsymbol{g} = (c^2/2)\nabla\ln\beta_1$ |
| 场方程 | $\nabla^2\beta_1 - (\nabla\beta_1)^2/\beta_1 = -8\pi G\rho_m/c^2$ |
| 静态球对称解 | $\beta_1(r) = \exp(2GM/c^2 r)$ |
| 弱场极限 | $\nabla^2\Phi = 4\pi G\rho_m$（牛顿引力） |

## A.6 统一动力学

| 物理量 | 表达式 |
|--------|--------|
| 拓扑动量 | $\boldsymbol{p} = mc\boldsymbol{T}$ |
| 统一动力学 | $\boldsymbol{F} = mc^2\kappa\boldsymbol{N} + mc^2\tau\boldsymbol{B}$ |
| 引力分量 | $F_g = mc^2\kappa$（主法向） |
| 电磁分量 | $F_{em} = mc^2\tau$（副法向） |

## A.7 电磁理论

| 物理量 | 表达式 |
|--------|--------|
| 矢量势 | $\boldsymbol{A} = k\boldsymbol{\tau}$ |
| 标量势 | $\phi = kc\tau_t$ |
| 磁场 | $\boldsymbol{B} = k\nabla\times\boldsymbol{\tau}$ |
| 电场 | $\boldsymbol{E} = -k(c\nabla\tau_t + \partial_t\boldsymbol{\tau})$ |
| 电荷 | $q = k_q \oiint_S \boldsymbol{\tau}\cdot d\boldsymbol{S}$ |
| 电荷密度 | $\rho_e = k_q\nabla\cdot\boldsymbol{\tau}$ |
| 高斯磁定律 | $\nabla\cdot\boldsymbol{B} = 0$（恒等式） |
| 法拉第定律 | $\nabla\times\boldsymbol{E} = -\partial_t\boldsymbol{B}$ |
| 挠率波动方程 | $\square\boldsymbol{\tau} = \mathcal{S}_\tau$ |

## A.8 强相互作用

| 物理量 | 表达式 |
|--------|--------|
| 亥姆霍兹方程 | $\nabla^2\kappa - \mu^2\kappa = -4\pi C_\kappa\delta^{(3)}(\boldsymbol{r})$ |
| 曲率场解 | $\kappa(r) = A e^{-\mu r}/r$ |
| 汤川势 | $V(r) = -g^2 e^{-\mu r}/r$ |
| 屏蔽参数 | $\mu = m_\pi c/\hbar$ |
| 力程 | $\lambda = 1/\mu = \hbar/(m_\pi c)$ |

## A.9 量子力学

| 物理量 | 表达式 |
|--------|--------|
| 动量算符 | $\hat{\boldsymbol{p}} = -i\hbar\nabla$ |
| 能量算符 | $\hat{E} = i\hbar\partial_t$ |
| 哈密顿量 | $\hat{H} = -\hbar^2/(2m)\nabla^2 + V_{\mathrm{topo}}(\kappa,\tau,\boldsymbol{r})$ |
| 薛定谔方程 | $i\hbar\partial_t\psi = \hat{H}\psi$ |
| 玻尔半径 | $a_0 = 4\pi\epsilon_0\hbar^2/(m_e e^2)$ |
| 氢原子基态 | $E_0 = -m_e e^4/(8\epsilon_0^2 h^2) = -13.6$ eV |

## A.10 四力统一总结

| 相互作用 | 几何本源 | 方向 | 力程 | 相对强度 | 媒介 |
|----------|----------|------|------|----------|------|
| 引力 | 曲率场 $\kappa$ | 主法向 $\boldsymbol{N}$ | 长程 | $10^{-38}$ | 引力子 |
| 电磁力 | 挠率场 $\tau$ | 副法向 $\boldsymbol{B}$ | 长程 | $10^{-2}$ | 光子 |
| 强相互作用 | 核心曲率暴涨 | 主法向（核心） | ~1 fm | 1 | 胶子/π介子 |
| 弱相互作用 | 拓扑相变 | 拓扑跃迁 | ~$10^{-18}$m | $10^{-5}$ | W/Z玻色子 |
