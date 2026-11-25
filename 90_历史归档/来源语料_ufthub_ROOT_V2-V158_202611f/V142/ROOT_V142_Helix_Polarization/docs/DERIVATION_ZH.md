# ROOT V142：螺旋运动、三正交标架、规范曲率与无质量传播的精确审计

## 0. 结论分类

- **数学定理/标准物理**：Frenet–Serret 几何；纯规范连接的 Maurer–Cartan 恒等式；麦克斯韦的 2 个传播偏振；Proca 场的 3 个偏振。
- **模型内部一致性检验**：两个方向场投影后的几何曲率；标架和麦克斯韦圆偏振的符号计算；无量纲示例的波形残差。
- **未证明的 ROOT 假设**：光速螺旋就是所有相互作用的基础；三正交方向会独立产生四种力；可由这种结构独立决定 \(G,\hbar,\alpha\) 或标准模型耦合常数。

严格只采用 **\(c=1\)**，\(\hbar\) 与 \(G\) 保留量纲。

## 1. 光速螺旋的几何（曲线意义）

\[
\mathbf r(t)=(a\cos\omega t,a\sin\omega t,ut),\qquad
 a^2\omega^2+u^2=1.
\]

\[
\kappa=a\omega^2,\qquad \tau=u\omega,\qquad
\omega^2=\kappa^2+\tau^2.
\]

非退化且 \(\omega>0,a>0\) 时，反解

\[
a=\frac{\kappa}{\kappa^2+\tau^2},\quad
\omega=\sqrt{\kappa^2+\tau^2},\quad
u=\frac{\tau}{\sqrt{\kappa^2+\tau^2}}.
\]

\(\mathbf T,\mathbf N,\mathbf B\) 两两正交是几何定义，不能据此认定三个基本力正交。螺旋是非零加速度的光速曲线，并非平直时空中**自由**零质量粒子的惯性轨迹。这里的螺旋运动学不等于真实光子的额外空间轨道。

## 2. 核心定理：完整的正交标架旋转联络是纯规范

在局部区域 \(U\) 取光滑标架 \(R:U\to SO(3)\)，定义

\[
\Omega=R^{-1}dR.
\]

计算

\[
d(R^{-1})=-R^{-1}(dR)R^{-1},\qquad
 d\Omega=dR^{-1}\wedge dR=-\Omega\wedge\Omega.
\]

故

\[
\boxed{\mathcal F_\Omega=d\Omega+\Omega\wedge\Omega=0}.
\]

如果仅把运动标架的转动定义为场，则局部曲率严格为零，无法通过此式得到真实的非零 Yang–Mills 场。**定理的作用域**是光滑纯规范连接；独立连接、非平凡投影、奇点、边界、非平凡整体拓扑均需要分别研究。不能推出“一切旋转理论不可能产生场强”。

### 可重复的非交换旋转示例

取 \(R(x,y)=R_z(\beta y)R_y(\alpha x)\)，分别计算

\[
\Omega_x=R^T\partial_x R,\quad \Omega_y=R^T\partial_y R.
\]

软件验证矩阵的每个分量满足

\[
\partial_x\Omega_y-\partial_y\Omega_x+[\Omega_x,\Omega_y]=0.
\]

即使 \([\Omega_x,\Omega_y]\ne0\)，导数项与交换子仍准确相消。

## 3. 投影为何能非零？但为什么还不是光子理论？

沿用第二章的场 \(R\)，取 \(\mathbf n=R\hat{\mathbf z}\)，定义

\[
 f_{xy}=\frac12\mathbf n\cdot(\partial_x\mathbf n\times\partial_y\mathbf n).
\]

当 \(\theta=\alpha x,\phi=\beta y\)：

\[
\boxed{ f_{xy}=\frac{\alpha\beta}{2}\sin(\alpha x) }.
\]

这与完整的 \(SO(3)\) 纯规范连接曲率为零不矛盾：\(f\) 是**投影/复合**的 \(U(1)\) 几何曲率，不是完整连接的曲率。若要解释物理电磁场，还须证明独立的传播自由度、作用量、物质耦合、边界条件与实验预言。

## 4. 一对标量预势在常量真空附近的动力学缺陷

设 \(F=dq\wedge dp\)，常量背景

\[
q=q_0+\varepsilon\xi,\qquad p=p_0+\varepsilon\eta.
\]

于是

\[
F=\varepsilon^2 d\xi\wedge d\eta=O(\varepsilon^2),
\quad S_F=-\frac{\hbar}{4g^2}\int F_{\mu\nu}F^{\mu\nu}d^4x=O(\varepsilon^4).
\]

因此在该背景上没有标准的二次自由场传播项。两个或更多的标量对相加仍然是相同阶数。这不是说**任何**非平凡背景都无二次项，而是指出常量真空下无法直接得到麦克斯韦光子。相关简单二形式还满足 \(F\wedge F=0\)；增加标量对可解除局部代数退化，但不会自动修复自由传播的缺陷。

## 5. 修正 V140 电磁平面波的磁场方向

在 \((+---)\) 惯性系中取 \(\varphi=k(t-z)\)，\(k>0\)，真空电磁场

\[
\mathbf E=E_0(\cos\varphi,\sin\varphi,0),\quad
\mathbf B=E_0(-\sin\varphi,\cos\varphi,0).
\]

检验：

\[
\partial_t\mathbf B+\nabla\times\mathbf E=0,\quad
\partial_t\mathbf E-\nabla\times\mathbf B=0,\quad
\nabla\cdot\mathbf E=\nabla\cdot\mathbf B=0.
\]

\[
\mathbf E\cdot\mathbf B=0,\quad |\mathbf E|=|\mathbf B|,\quad
\mathbf E\times\mathbf B=E_0^2\hat z.
\]

V140 陈述的相反磁场符号 \(\mathbf B_{\rm old}=E_0(\sin\varphi,-\cos\varphi,0)\) 给出

\[
\partial_t\mathbf B_{\rm old}+\nabla\times\mathbf E
=2k E_0(\cos\varphi,\sin\varphi,0)\ne0,
\]

\[
\partial_t\mathbf E-\nabla\times\mathbf B_{\rm old}
=2k E_0(-\sin\varphi,\cos\varphi,0)\ne0.
\]

**结论**：对相位 \(t-z\)，必须采用本轮磁场方向，才能同时满足真空麦克斯韦方程及 \(+z\) 能流。电场/磁场矢量的旋转并不等于单个光子的空间轨迹为螺旋。

## 6. 两种矢量场的真实自由度

麦克斯韦作用量：

\[
S_M=-\frac{\hbar}{4g^2}\int d^4x F_{\mu\nu}F^{\mu\nu},\quad F=dA.
\]

规范冗余 \(A_\mu\to A_\mu+\partial_\mu\chi\)，Hamilton 形式拥有 8 个相空间变量，初级约束 \(\pi^0=0\)，次级 Gauss 约束 \(\partial_i\pi^i=0\)，均为一级约束：

\[
\boxed{N_M=\frac{8-2(2)}2=2}.
\]

在平面波 \(k^\mu=(k,0,0,k)\) 的壳上，Lorenz 规范约束 \(k\cdot\epsilon=0\)，仍可利用 \(\epsilon\to\epsilon+c k\) 删除一个纯规范方向，剩下 \(\epsilon_x,\epsilon_y\) 两种横向偏振。

Proca 质量项使规范对称性消失。初级及次级约束为一对二级约束，因此

\[
\boxed{N_P=\frac{8-2}{2}=3}.
\]

从“空间螺旋”出发，如不能独立建立恰当的作用量/约束结构，就不能推导出正确的光子偏振数。

## 7. 只采用 c=1 的量纲审计

\[
[x]=[t]=L,\ [m]=M,\ [\hbar]=ML,\ [G]=L/M,
\quad[\omega]=[\kappa]=[\tau]=L^{-1}.
\]

取 \([A_\mu]=L^{-1},[F_{\mu\nu}]=L^{-2}\)，无量纲规范耦合 \(g\)，引力作用量与 Maxwell 作用量可以明确写为

\[
\boxed{
S=\int d^4x\sqrt{-g}
\left[\frac{R}{16\pi G}-\frac{\hbar}{4g^2} F^2+\mathcal L_{\mathrm{matter}}\right]
}
\]

上式是**已知引力 + 已知电磁动力学的组合**，并非来自螺旋的独立推导。因此不能视为四力统一。

## 8. 可证伪的后续任务（优先级）

1. 给出螺旋的基本协变变量以及**独立于 Maxwell 势 \(A\)** 的作用量，并计算二阶涨落 Hessian；必须出现正确的无质量自旋 1 模式与稳定传播。
2. 证明完整连接存在非零、非纯规范的场强，而非仅通过局部重新定义隐藏麦克斯韦势。
3. 对所有背景检查洛伦兹协变性、能量正定性、超光速/梯度不稳定性及规范约束闭合。
4. 计算具体预言（例如双折射、光子色散、静电库仑律修正），给出不会随重新标定参数消失的观测量。
5. 独立导出 \(SU(3)\)、\(SU(2)\)、\(U(1)\) 的规范结构和耦合；检验引力及能量动量守恒。不得仅指定为初始条件。

## 9. 研究判定

本轮得到严格的**构造限制与符号方向修复**，不是四力统一证明；真实实验数据的联合拟合也未在本轮实施。

## 10. 参考背景

- D. Tong, *Quantum Field Theory*, §6.1, https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S6.html （电磁场物理偏振）
- P. Michor et al., Cartan connections, https://www.mat.univie.ac.at/~michor/cartan.pdf （Maurer–Cartan 平坦性）
- Gralla & Jacobson, *Spacetime approach to force-free magnetospheres*, https://doi.org/10.1093/mnras/stu1690 （简单二形式/ Euler 势）
- NASA Scientific Visualization Studio, *Electromagnetic Waves and Polarization*, https://svs.gsfc.nasa.gov/4580/ （偏振）
