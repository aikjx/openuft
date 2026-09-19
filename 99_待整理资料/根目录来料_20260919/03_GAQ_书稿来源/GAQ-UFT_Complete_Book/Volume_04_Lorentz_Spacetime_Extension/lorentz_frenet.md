# 第4卷 洛伦兹时空拓展：3+1维相对论统一场

# 第13章 洛伦兹号差下 Frenet–Serret 活动标架

> 把第1章的欧氏 Frenet–Serret 推广到闵可夫斯基时空。世界线分为类时、类光、类空三类，其“弧长”由度规符号决定，标架构造需改用 Lorentz 内积。

---

## 13.1 类时、类光、类空世界线的 Frenet–Serret 推广

闵可夫斯基度规取号差 $(-,+,+,+)$。世界线 $x^\mu(\lambda)$。定义 Lorentz 范数 $\|v\|^2=\eta_{\mu\nu}v^\mu v^\nu$。

- **类时**（$v^2<0$）：用固有时 $\tau$ 参数化，$\dot x^2=-c^2$，单位切向 $U^\mu=\dot x^\mu$（四速）。
- **类光**（$v^2=0$）：切向自身为零模，Frenet 标架需引入辅助类空矢量构造，曲率定义退化为“类光挠率”类量。
- **类空**（$v^2>0$）：$\dot x^2=+1$。

对类时世界线，仿照欧氏构造：

$$
\frac{D U^\mu}{d\tau}=\kappa\,N^\mu,\qquad
\frac{D N^\mu}{d\tau}=-\kappa\,U^\mu+\tau\,B^\mu,\qquad
\frac{D B^\mu}{d\tau}=-\tau\,N^\mu,
$$

其中 $D/d\tau$ 为沿世界线的协变导数（平直时空即普通导数），$N^\mu,B^\mu$ 与 $U^\mu$ 构成 Lorentz 正交标架（$U\cdot N=U\cdot B=N\cdot B=0,\ N^2=B^2=+1$）。此处 $\kappa$ 为四加速度大小，$\tau$ 描述标架绕四速的进动。

### 13.1.1 类光世界线的 Frenet 标架构造

类光世界线 $\dot x^2=0$，单位切向 $K^\mu=\dot x^\mu$ 满足 $K^2=0$，无法借 $K^\mu K_\mu=1$ 归一。标准处理引入一对辅助类空矢量 $(L^\mu,S^\mu)$ 与 $K^\mu$ 构成部分标架：

- $K^2=0,\ L^2=S^2=+1,\ K\cdot L=K\cdot S=L\cdot S=0$；
- 再取一个与三者正交的类光矢量 $K'^\mu$（$K\cdot K'=1$）构成完整 null tetrad $(K,K',L,S)$。

类光挠率 $\tau_{\mathrm{null}}$ 由 $DK^\mu/d\lambda$ 在 $L,S$ 上的投影定义，曲率记号退化为“切向加速度在横向类空平面内的旋转率”。GAQ‑UFT 在第14章（光锥 Kakeya）用到此结构：类光生成元的“非零类光挠率”对应欧氏分支3 的 $\tau\neq0$ 在洛伦兹情形的类比，是 A1 光锥覆盖的必要条件。

## 13.2 洛伦兹 boost 下螺旋曲率、挠率变换规则

对真空螺旋施加沿轴方向的 boost（速度 $v$）：

$$
\gamma=\frac{1}{\sqrt{1-v^2/c^2}},\qquad z'\to \gamma(z-vt),\quad t'\to\gamma(t-vz/c^2).
$$

螺距沿运动方向被 Lorentz 收缩，导致观测到的升角变化。对**光类纵向**圆柱螺旋（轴沿 $z$，纵向以光速前进）沿其轴做速度 $v=\beta c$ 的 boost，由世界线直接推导（见下）得

$$
\tan\theta' = \frac{\tau'}{\kappa'} = \frac{\tan\theta}{\gamma(1+\beta)}
= \tan\theta\,\gamma(1-\beta).
$$

> ⚠ **交叉验证修正（2026-08-12）**：原稿写为 $\tan\theta'=\tan\theta/\gamma$（收缩因子 $\gamma\approx2.29$ @$0.9c$），
> 该式既非从世界线推导、又差一个因子 $(1+\beta)$。正确结果由 4 维世界线 boost 严格得到：
> $\tan\theta'=\tan\theta/[\gamma(1+\beta)]$，即 $v=0.9c$ 时收缩因子为 $\gamma(1+\beta)\approx4.36$（$\theta:0.418^\circ\to0.096^\circ$）。
> 错误假定已在 `verification_suite.py` T7 与 `cross_check.py` CC-6 中定位并废除。

即**运动参考系中螺旋更“扁”**，几何升角收缩——但这是“几何投影角”的变化，不等同于物理精细结构常数改变：在 GAQ‑UFT 中 $\alpha$ 由**真空静止系**的螺旋内禀几何 $\tan\theta$ 定义；在沿轴 boost 的参考系里，同一根螺旋的几何投影角 $\theta'$ 确实变小（上式），因此 $\tan\theta$ **不是**洛伦兹标量。物理上可观测的 $\alpha$ 在所有惯性系相同，是因为任何局部测量都在**当地真空静止系**内进行。原稿“α 作为洛伦兹标量保持协变”的措辞不严谨，此处更正为“在真空静止系定义”。

### 13.2.1 收缩因子的显式推导（世界线法）

取静止系圆柱螺旋 $\mathbf{r}(\varphi)=(R\cos\varphi,R\sin\varphi,c\varphi)$，轴沿 $z$。参数化 4 维世界线
$x^\mu(\varphi)=(t,R\cos\varphi,R\sin\varphi,ct)$，其中 $t=\varphi/\omega$。沿 $z$ 方向以 $v=\beta c$ boost：

$$
\begin{aligned}
ct' &= \gamma(ct-\beta z)=\gamma ct(1-\beta),\\
z'  &= \gamma(z-\beta ct)=\gamma ct(1-\beta),\\
x'  &= R\cos\varphi,\qquad y'=R\sin\varphi.
\end{aligned}
$$

由 $ct'=\gamma ct(1-\beta)$ 得 $t'= \gamma t(1-\beta)$，故 $x'=R\cos\!\big(\omega t'/\gamma(1-\beta)\big)$，即运动系角频率
$\omega'=\omega/[\gamma(1-\beta)]=\omega\,\gamma(1+\beta)$；且 $z'=ct'$。于是运动系螺旋的螺距
（每弧度轴向推进）$P'=c/\omega'=P/[\gamma(1+\beta)]$，横向半径 $R$ 不变（垂直于运动方向）。
观测升角满足

$$
\tan\theta' = \frac{P'}{R} = \frac{1}{\gamma(1+\beta)}\,\frac{c}{R}
= \frac{\tan\theta}{\gamma(1+\beta)}
= \tan\theta\,\gamma(1-\beta).
$$

交叉验证脚本 `cross_check.py`（CC-6）对 $v=0.9c$ 给出收缩因子 $\gamma(1+\beta)\approx4.36$，与上式一致。

## 13.3 时间膨胀作为螺旋几何推论

螺旋上某点绕轴旋转一周的固有时为 $\Delta\tau_0=2\pi/\Omega_0$（$\Omega_0$ 为内禀角频率）。在相对运动的实验室系，该周期事件的 coordinate 时间为 $\Delta t=\gamma\Delta\tau_0$。这正是标准时间膨胀。GAQ‑UFT 的贡献在于：把“固有时”锚定为**螺旋内禀旋转周期**，使时间膨胀从“螺旋几何的投影效应”自然浮现，而非独立公设。

---

*（本章完。第14章把广义 Kakeya 延伸到光锥方向空间，并论证时空度规如何从螺旋系综涌现。）*
