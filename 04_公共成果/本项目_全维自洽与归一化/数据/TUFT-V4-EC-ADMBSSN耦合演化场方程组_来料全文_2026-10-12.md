# 来料正本：TUFT‑V4 完整耦合演化场方程组（适配 ADM‑BSSN 数值相对论）

> 登记日期：2026-10-12　受理轮次：**r39**（判定册见 `判定_TUFT-r39-V4-EC-ADMBSSN耦合场方程组_全维审计_2026-10-12.md`）
> 本件为**来料逐字存档**（公式与文字照录，未作修改），供后续复核与引用。审计结论一律以判定册为准。

---

## 任务书原文（摘要）

**底层公理**：时空流形上每一点存在**光速螺旋本征运动**，切向速率 $v_\text{tangent}=c$；动力学自由度：曲率 $\kappa$、挠率 $\tau$、本征角频率 $\omega$；流形采用**爱因斯坦‑嘉唐 EC 几何（带挠率，非黎曼流形）**，兼容 Frenet‑Serret 曲线几何；目标输出适合 ADM‑BSSN 分解，可直接用于数值演化。

## 符号索引

| 符号 | 含义 | 量纲 |
|---|---|---|
| $c$ | 真空光速 | $[L\,T^{-1}]$ |
| $\hbar$ | 约化普朗克常数 | $[M\,L^2\,T^{-1}]$ |
| $G_\text{th}$ | 理论导出引力常数 | $[L^3 M^{-1} T^{-2}]$ |
| $\kappa$ | 时空螺旋线标量曲率 | $[L^{-1}]$ |
| $\tau$ | 时空螺旋线标量挠率 | $[L^{-1}]$ |
| $\omega$ | 螺旋本征角频率 | $[T^{-1}]$ |
| $\theta$ | 螺旋升角（几何常数） | 无量纲 |
| $g_{\mu\nu}$ | 4 维度度规张量 | 无量纲 |
| $\Gamma^\alpha_{\mu\nu}$ | 带挠率的嘉唐联络 | $[L^{-1}]$ |
| $T^\alpha_{\mu\nu}$ | 挠率张量 | $[L^{-1}]$ |
| $R_{\mu\nu}$ | 嘉唐曲率张量缩并里奇张量 | $[L^{-2}]$ |
| $\rho$ | 质量能量密度 | $[M\,L^{-3}]$ |
| $\vec g$ | 引力加速度场 | $[L\,T^{-2}]$ |
| $\nabla_\mu$ | 嘉唐协变导数（含挠率） | $[L^{-1}]$ |

### 前置恒等式（来自光速螺旋 Frenet‑Serret 约束）

$$\kappa^2+\tau^2=\frac{\omega^2}{c^2}\tag{1}$$
$$\tau=\kappa\cot\theta\tag{2}$$

本源内禀质量（量子驻波条件 $S=\hbar$）：

$$m=\frac{\hbar\sin\theta}{2\pi c}\sqrt{\kappa^2+\tau^2}=\frac{\hbar\omega}{2\pi c^2}\tag{3}$$

理论导出引力常数：

$$G_\text{th}=\frac{2\pi c^3}{\hbar\sin\theta}\tag{4}$$

> 来料说明：(1)(2)(3)(4) 为**代数约束方程**，不是演化方程；每一步时间迭代时强制做约束校验。

---

## 第一部分：流形层面 — 爱因斯坦‑嘉唐耦合场方程（TUFT 本体）

嘉唐场方程：

$$R_{\mu\nu}-\frac12 g_{\mu\nu}R=\frac{8\pi G_\text{th}}{c^4}\big(T_{\mu\nu}^\text{matter}+T_{\mu\nu}^\text{spiral}\big)\tag{5}$$

挠率张量主标量迹（轴挠率）：

$$T=T^\alpha_{\mu\nu}\,\epsilon_\alpha{}^{\mu\nu}\propto\tau\tag{6}$$

曲率标量：

$$R\propto\kappa^2-\tau^2\tag{7}$$

螺旋场能动张量：

$$T_{\mu\nu}^\text{spiral}=\frac{\hbar}{2c}\Big\{\nabla_\mu\kappa\nabla_\nu\kappa+\nabla_\mu\tau\nabla_\nu\tau-\frac12 g_{\mu\nu}\big(\nabla_\alpha\kappa\nabla^\alpha\kappa+\nabla_\alpha\tau\nabla^\alpha\tau\big)-V(\kappa,\tau)g_{\mu\nu}\Big\}\tag{8}$$

势函数：

$$V(\kappa,\tau)=\frac12\big(c^2(\kappa^2+\tau^2)-\omega^2\big)^2\tag{9}$$

> 来料说明：$V$ 是约束势；满足 (1) 时 $V=0$；数值演化中起**约束阻尼**作用，抑制约束漂移（ADM‑BSSN 中约束保持的标准手段）。

---

## 第二部分：标量场动力学演化方程（$\kappa,\tau$ 传播方程）

$$\Box_\Gamma\kappa=\frac{\partial V}{\partial\kappa}+\mathcal S_\kappa[\rho]\tag{10}$$
$$\Box_\Gamma\tau=\frac{\partial V}{\partial\tau}+\mathcal S_\tau[\rho]\tag{11}$$

$$\mathcal S_\kappa=4\pi G_\text{th}\frac{\sin\theta}{c^2}\rho,\qquad \mathcal S_\tau=4\pi G_\text{th}\frac{\cos\theta}{c^2}\rho\tag{12}$$

$$\frac{\partial V}{\partial\kappa}=2c^2\kappa\big(c^2(\kappa^2+\tau^2)-\omega^2\big),\qquad
\frac{\partial V}{\partial\tau}=2c^2\tau\big(c^2(\kappa^2+\tau^2)-\omega^2\big)$$

$\omega$ 不独立演化，由 (1) 即时更新：$\omega=c\sqrt{\kappa^2+\tau^2}$。

### 低速弱场非相对论极限校验（来料原文）

弱场 $\kappa,\tau\to0$，$\tau\ll\kappa$，达朗贝尔退化为泊松方程：

$$-\nabla^2\kappa=4\pi G_\text{th}\frac{\sin\theta}{c^2}\rho$$

引力加速度 $\vec g=-c^2\kappa\hat R$，代入：

$$\nabla\cdot\vec g=-c^2\nabla^2\kappa=4\pi G_\text{th}\sin^2\theta\cdot 4\pi?$$

代入 $G_\text{th}=2\pi c^3/(\hbar\sin\theta)$ 结合本源质量定义，自动还原牛顿引力高斯定理 $\nabla\cdot\vec g=-4\pi G_\text{exp}\rho$。

---

## 第三部分：ADM‑BSSN 3+1 时空分解

$$ds^2=-\alpha^2dt^2+\gamma_{ij}\big(dx^i+\beta^idt\big)\big(dx^j+\beta^jdt\big)$$

BSSN 变量：$\tilde\gamma_{ij}=\gamma^{-1/3}\gamma_{ij}$；$\tilde A_{ij}$；$\phi=\frac1{12}\log\gamma$。

> 来料 TUFT 修改点：标准 BSSN 使用黎曼联络；本框架三维超曲面上存在非零空间挠率。

$$\Pi_\kappa=\frac1\alpha\big(\partial_t\kappa-\beta^k\partial_k\kappa\big)\tag{13},\qquad
\Pi_\tau=\frac1\alpha\big(\partial_t\tau-\beta^k\partial_k\tau\big)\tag{14}$$

$$\partial_t\kappa=\beta^k\partial_k\kappa+\alpha\Pi_\kappa\tag{15},\qquad
\partial_t\tau=\beta^k\partial_k\tau+\alpha\Pi_\tau\tag{16}$$

$$\partial_t\Pi_\kappa=\beta^k\partial_k\Pi_\kappa+\alpha\tilde D^i\tilde D_i\kappa+\partial_k\alpha\tilde D^k\kappa-\alpha\frac{\partial V}{\partial\kappa}-\alpha\mathcal S_\kappa[\rho]\tag{17}$$

$$\partial_t\Pi_\tau=\beta^k\partial_k\Pi_\tau+\alpha\tilde D^i\tilde D_i\tau+\partial_k\alpha\tilde D^k\tau-\alpha\frac{\partial V}{\partial\tau}-\alpha\mathcal S_\tau[\rho]\tag{18}$$

### 约束集合

1. $\mathcal C_\omega=\omega^2-c^2(\kappa^2+\tau^2)=0$
2. $\mathcal C_H=R^{(3)}-A_{ij}A^{ij}+\frac23K^2-16\pi G_\text{th}\rho=0$
3. $\mathcal C^i_M=\tilde D_j\big(\tilde A^{ij}\big)-\frac23\tilde D^iK-8\pi G_\text{th}j^i=0$

---

## 第四部分：边界条件与初始数据方案

1. 无穷远外边界：$\kappa,\tau,\Pi_\kappa,\Pi_\tau\to0$，渐近平直；
2. 天体内部源区：给定 $\rho(x)$，由源项激发曲率挠率；
3. 初始条件（静态弱引力）：$\Pi_\kappa(0)=\Pi_\tau(0)=0$，泊松求解初始 $\kappa(x),\tau(x)$。

---

## 第五部分：与旧体系对照审计（来料原文）

1. 张祥前：只有一个无挠率辅助场，没有波动传播，没有场动力学，$G$ 是外部输入，无 ADM 分解，不能做数值演化；
2. 牛顿引力：静态泊松方程，无动力学传播，无挠率；
3. GR：黎曼几何，挠率恒等于 0；
4. TUFT 这套方程组：
   - ✅ 完整一阶双曲偏微分方程组，适配 RK4、FDTD、ADM‑BSSN 数值相对论；
   - ✅ 曲率 $\kappa$、挠率 $\tau$ 双动力学自由度；
   - ✅ $G_\text{th}$ 由螺旋升角、$c,\hbar$ 第一性导出；
   - ✅ 内置约束势抑制数值漂移；
   - ✅ 弱场极限回归牛顿引力；强场/自旋物体自动引入挠率修正，兼容爱因斯坦‑嘉唐理论。

---

## 末尾：待下一步攻坚（接续任务）

1. 写出这套方程组的**250 位高精度 Python/mpmath 代码原型**，计算理论 $G_\text{th}$，对标 CODATA 实验 G 值，做 $\chi^2$ 残差分析（**任务 A**）；
2. 或者，推导电子 g‑2 反常磁矩来自挠率 $\tau$ 的一阶修正表达式（**任务 B**）。

> 来料问：你选择继续 **任务 A** 还是 **任务 B**？

**本册（r39）处置**：不代选。判定册 §五给出两条路的**前置阻塞与代价**，由用户裁决。
