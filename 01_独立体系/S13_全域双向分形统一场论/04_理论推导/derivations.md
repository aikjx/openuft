# 理论推导：全域微分结构

> 体系：全域双向分形统一场论（S13）· 假设版本 v1.2-20260911
> 出处：验证精算报告 V1.2 第一节；书稿第 12 章
> 状态：五组完整求导推导，全部可在 [07_计算复现](../07_计算复现/README.md) 脚本中复现。

## 推导 1（旋量对偶 → 流守恒）

$J^{\mu} = \Psi^{\dagger}\sigma^{\mu}\Psi$，取全微分：

$$
\partial_{\mu}J^{\mu} = 2\,\mathrm{Re}\left( \Psi^{\dagger}\sigma^{\mu}\partial_{\mu}\Psi \right) = 2\lambda\,\mathrm{Re}\left( \Psi^{\dagger}\Theta\,\Psi^{*} \right)
$$

配对项 $\Psi^{\dagger}\Theta\Psi^{*} = \psi_{0}^{*}\left( -\psi_{1}^{*} \right) + \psi_{1}^{*}\psi_{0}^{*} = 0$，实部恒零：

$$
\partial_{\mu}J^{\mu} = 0
$$

**结论**：连续方程是代数恒等式，与 $\lambda$ 无关（数值漂移 $2.1\times10^{-13}$）。

## 推导 2（对偶协变性 → 对偶周期 4）

$\Psi^{c} = \Theta\Psi^{*}$ 再求导，利用 $\Theta$ 实矩阵与 $\Theta^{2} = -I$：

$$
\sigma^{\mu}\partial_{\mu}\Psi^{c} = \Theta\left( \lambda\Theta\Psi^{*} \right)^{*} = \lambda\Theta^{2}\Psi = -\lambda\Psi
$$

两轮共轭得 $-\Psi$——对偶周期 4 的微分证明。

## 推导 3（拓扑荷时间导数：1D 绕数 vs 霍普夫荷）

**1D 绕数**：$Q_{1D} = \frac{1}{2\pi\mathrm{i}}\oint \frac{\mathrm{d}z}{z}$，时间导数在 $z$ 过零处发散——跳变（$t\approx0.2$ 处 $1\to0$，实验九）。**不守恒，因为维度错（$\pi_{1}(S^{2}) = 0$）。**

**霍普夫荷**：$Q_{H} = \frac{1}{4\pi^{2}}\int\epsilon^{ijk}a_{i}\partial_{j}a_{k}$，时间导数：

$$
\frac{\mathrm{d}Q_{H}}{\mathrm{d}t} = \frac{1}{4\pi^{2}}\int\epsilon^{ijk}\partial_{j}\left( a_{i}\partial_{t}a_{k} \right) = 0
$$

分部积分后是全导数，边界为零（无穷远场归一化）——**拓扑上自动守恒**。

## 推导 4（双向 β 流 → 不动点对与稳定性）

$\beta\left( g \right) = \varepsilon g - cg^{3}$，令导数为零：$g^{*} = \pm\sqrt{\varepsilon/c}$。

不动点处 $\beta'\left( g^{*} \right) = \varepsilon - 3c\,g^{*2} = -2\varepsilon < 0$——成对稳定不动点，双向往返由奇对称 $\beta\left( -g \right) = -\beta\left( g \right)$ 保证。

## 推导 5（对偶镜像度规 → 曲率闭式）

$g^{\mathrm{eff}}\left( r \right) = 1 - \frac{r_{s}r}{r^{2}+\ell^{2}}$，Ricci 标量：

> **【2026-09-18 修正 · 勘误 E7】** 原式写作
> $R\left( r \right) = \dfrac{r_{s}\,\ell^{2}\left( 3r^{2} - \ell^{2} \right)}{\left( r^{2} + \ell^{2} \right)^{3}}$
> 与 $3r^{4} - 6\ell^{2}r^{2} - \ell^{4} = 0$ 均为**书写笔误**：前者在驻点 $r=(\sqrt{2}-1)\ell$ 处给 $0.3018$，
> 与下方 $|R|_{\max}$ 闭式差 $79.29\%$，且 $R(0^{+}) = -1 \neq 0$（违反端点条件）；
> 后者的解为 $r^{2}=\left(1+\tfrac{2\sqrt{3}}{3}\right)\ell^{2}\approx 2.1547\ell^{2}$，与其自身给出的 $\left(3\pm2\sqrt{2}\right)$ 不符。
> 正确式如下（已由 `全维勘误精算修复验证.py` F6 组以 sympy + 50 位数值核验，并与本体系
> `09_验证结果/验证精算报告_V1.8.md` P4c/P4d/P4f 的 $\sim 10^{-50}$ 残差一致）。
> **注**：驻点解 $r=\left(\sqrt{2}\pm1\right)\ell$ 与 $|R|_{\max}$ 闭式原本正确，本次仅修正其推导过程中的表达式。

$$
R\left( r \right) = -\frac{\mathrm{d}^{2}}{\mathrm{d}r^{2}}g^{\mathrm{eff}}
= \frac{2\,r_{s}\,r\left( r^{2} - 3\ell^{2} \right)}{\left( r^{2} + \ell^{2} \right)^{3}}
$$

驻点条件 $r^{4} - 6\ell^{2}r^{2} + \ell^{4} = 0 \Rightarrow r^{2} = \left( 3 \pm 2\sqrt{2} \right)\ell^{2}$，代回得：

$$
\left| R \right|_{\max} = \frac{\left( 3 + 2\sqrt{2} \right)GM}{2\ell^{3}}, \qquad r = \left( \sqrt{2}\pm 1 \right)\ell
$$

端点 $R\left( 0^{+} \right) = R\left( \infty \right) = 0$——奇点被逐出全域。

## 推导 6（因果畴通量 → 畴守恒）

$$
\frac{\mathrm{d}}{\mathrm{d}t}\int_{\mathcal{C}}\omega = \int_{\mathcal{C}}\mathrm{d}\left( \mathrm{i}_{v}\omega \right) - \int_{\mathcal{C}}\partial_{\mu}J^{\mu} = \oint_{\partial\mathcal{C}}\Theta
$$

末步用推导 1 的 $\partial_{\mu}J^{\mu} = 0$。零面上对偶翻转 $\Psi \to \Theta\Psi^{*}$ 是保度规变换，$Q \to -Q$ 但 $|Q|$ 不变——总荷守恒。

## 诚实边界

全部推导是**代数/解析恒等式**，不引入实验输入；"推导成立"不等于"理论被实验确认"，实验确认属于第 6、9 阶段的预言与验证。
