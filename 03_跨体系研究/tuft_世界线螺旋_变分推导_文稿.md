# 世界线层：常曲率–常挠率作用量 ⇒ 圆柱螺旋（严格变分推导）

> 配套机器核对：`tuft_世界线螺旋_变分推导.py`（sympy，8/8 PASS）。
> 本文是**世界线（1D 曲线）层**的种子推导，与 `07_统一场方程`（4D Einstein–Cartan 场论层）不重叠：07 直接做 4D，本文先把"螺旋为何是变分解"在曲线层面钉死，再谈提升。

---

## 0. 工作假设与参数化

把世界线写成空间曲线 $\mathbf R:[0,L]\to\mathbb R^3$。先**用弧长 $s$ 参数化**，于是

$$
|\mathbf R'(s)|=1,\qquad \prime\equiv\frac{d}{ds}.
$$

物理时间 $t$ 与 $s$ 的关系由"光速约束" $|\dot{\mathbf R}(t)|=c$ 决定。若曲线以弧长匀速扫过，则 $s=ct$，于是 $|\mathbf R'(s)|=1$ 自动给出 $|\dot{\mathbf R}|=c$。这正是要恢复的约束，但现在我们**先不预设**螺旋，而是把它作为变分问题的产物。

---

## 1. 曲率与挠率（弧长型定义）

$$
\kappa(s)=|\mathbf R''(s)|,\qquad
\tau(s)=-\frac{\mathbf R'(s)\times\mathbf R''(s)\cdot\mathbf R'''(s)}{\kappa(s)^2}.
$$

（$\tau$ 的符号只代表手性；本文取标准号使下文螺旋给 $+\tau_0$。）

---

## 2. 几何作用量（"钉扎"型）

$$
S[\mathbf R]=\int_0^L\Big[\alpha\,(\kappa-\kappa_0)^2+\beta\,(\tau-\tau_0)^2\Big]\,ds,
\qquad \alpha,\beta>0,
$$

其中 $\kappa_0,\tau_0$ 是**预设常数**。动能项 $\tfrac12 m|\dot{\mathbf R}|^2$ 在 $s=ct$ 下只是常数 $\tfrac12 mc^2$（因 $|\mathbf R'|=1$），不参与 $\kappa,\tau$ 的极值方程，故省略不影响结论。

> 注：这是"把轨道钉到 $(\kappa_0,\tau_0)$"的作用量，不是"最小化总曲率"。二者的区别是诚实边界 B3 的核心。

---

## 3. 关键引理：把 $\kappa(s),\tau(s)$ 当作独立变分场

**空间曲线基本定理**（do Carmo, *Differential Geometry of Curves and Surfaces*, Chap.1）：给定任意连续函数 $\kappa(s)>0$ 与 $\tau(s)$，存在（至多差一个刚体运动）唯一一条单位速率曲线以它们为曲率与挠率。

由此推出：在正则曲线上，局部变分 $\delta\mathbf R$ 诱导的 $(\delta\kappa,\delta\tau)$ 在 $\kappa>0$ 处**可取任意光滑局部值**（"曲率/挠率映射"是子浸没）。因此第一变分

$$
\delta S=\int_0^L\Big[2\alpha(\kappa-\kappa_0)\,\delta\kappa+2\beta(\tau-\tau_0)\,\delta\tau\Big]\,ds
$$

对**所有** $\delta\kappa,\delta\tau$ 为零，由变分法基本引理：

$$
\boxed{\kappa(s)=\kappa_0,\qquad \tau(s)=\tau_0}\qquad(\text{在内部})
$$

这就是"极值解满足 $\kappa=\kappa_0,\ \tau=\tau_0$"的**严格依据**——不是断言，而是基本定理保证 $\kappa,\tau$ 可独立变分后的直接结果。

---

## 4. 唯一性：从常数 $\kappa_0,\tau_0$ 反解 Frenet 方程

Frenet–Serret 方程（弧长参数）：

$$
\mathbf T'=\kappa_0\mathbf N,\quad
\mathbf N'=-\kappa_0\mathbf T+\tau_0\mathbf B,\quad
\mathbf B'=-\tau_0\mathbf N,\qquad \mathbf T=\mathbf R'.
$$

设 $\Omega\equiv\sqrt{\kappa_0^2+\tau_0^2}$，解为（至多刚体运动）

$$
\boxed{
\mathbf R(s)=\frac{\kappa_0}{\kappa_0^2+\tau_0^2}\cos(\Omega s)\,\mathbf i
+\frac{\kappa_0}{\kappa_0^2+\tau_0^2}\sin(\Omega s)\,\mathbf j
+\frac{\tau_0}{\sqrt{\kappa_0^2+\tau_0^2}}\,s\,\mathbf k
+\mathbf R_0 }.
$$

**机器核对**（脚本 C1–C3）：对该 $\mathbf R(s)$ 直接算得
- $\kappa(s)=\kappa_0$（常数），$\tau(s)=\tau_0$（常数）；
- $|\mathbf R'(s)|=1$。

这正是圆柱螺旋，半径 $r=\kappa_0/(\kappa_0^2+\tau_0^2)$、螺距半宽 $b=\tau_0/(\kappa_0^2+\tau_0^2)$。

> 注意：角频率是 $\Omega=\sqrt{\kappa_0^2+\tau_0^2}$，**不是** $\tau_0$。这是把"常挠率"误读为"绕轴角速度"的常见陷阱。

---

## 5. 回到时间参数：恢复光速分解

令 $s=ct$ 代入第 4 节解：

$$
\mathbf R(t)=r\cos(\Omega c t)\,\mathbf i+r\sin(\Omega c t)\,\mathbf j+(z_0 c)\,t\,\mathbf k,
\quad \omega\equiv\Omega c,\quad p\equiv z_0 c.
$$

机器核对（脚本 C4–C5、C6c）：

$$
|\dot{\mathbf R}|=c,\qquad (r\omega)^2+p^2
=\frac{c^2(\kappa_0^2+\tau_0^2)}{\kappa_0^2+\tau_0^2}=c^2.
$$

**结论**：你原先"人为设定"的螺旋 $\mathbf R(t)=r\cos\omega t\,\mathbf i+r\sin\omega t\,\mathbf j+pt\,\mathbf k$ 连同约束 $(r\omega)^2+p^2=c^2$，现在**不是假设，而是变分问题 $\delta S=0$ 的唯一（刚体等价类）解**。变分结构、欧拉方程、几何唯一性定理三者齐备。

---

## 6. 严格性补充：两条等价路线

- **捷径（本文采用）**：靠基本定理把 $\kappa,\tau$ 视为独立场，EL 立即给出 $\kappa=\kappa_0,\tau=\tau_0$。
- **直路（更繁琐但更"正统"）**：直接对 $L=\alpha(\kappa-\kappa_0)^2+\beta(\tau-\tau_0)^2$ 做高阶变分。因 $\kappa$ 含 $\mathbf R'$ 到二阶、$\tau$ 含到三阶，EL 是 **6 阶**常微分方程；化简后与捷径同解。两条路线一致，捷径只是用几何定理跳过了 6 阶方程的求解。

---

## 7. 诚实边界（红线：数学自洽 ≠ 实验证实）

**B1 — 外部锚定（对应既有 O-SCALE）。** 作用量**不决定** $\kappa_0,\tau_0$；它们是预设常数，$\alpha,\beta$ 只控制"以多快逼近靶"，不改变靶值。故螺旋的**半径与螺距是输入，不是输出**。本变分体系是"把螺旋编码为极值轨道"，不是"从第一性生成螺旋的尺度"。尺度仍需外部锚定——这正是 openuft 反复确认的结论。

**B2 — 退化情形 $\kappa_0=0$。** 此时 $\tau_0$ 无定义，极值轨道退化为直线（即"光沿直线传播"）。螺旋分支**要求 $\kappa_0>0$**，这对应既有框架的"降级端口"：$\kappa=0$ 回到直线极限。

**B3 — "钉扎"与"最小化"不是一回事。** 若只取 $\int\kappa^2ds$（欧拉弹性杆 elastica），固定长度与端点的极值解是**圆**（或直线），**不是螺旋**；螺旋必须同时钉住挠率靶 $\tau=\tau_0$。若想让螺旋从"更动力学"的原理（不预设 $\kappa_0,\tau_0$）涌现，需要额外结构：沿某轴的平移不变性给出的 Noether 守恒量（轴向动量/轴向角动量），即你在第四层提到的"加入轴向动量守恒"。本文的钉扎型作用量是干净的"编码"，但**不免除 B1 的外部输入**。

**B4 — 4D 提升的挠率陷阱。** 你第八层写的 $S=\int(R+T^2)\sqrt{-g}\,d^4x$ 方向正确，但须警告：在 Einstein–Cartan 理论中（见 `07_统一场方程/02_变分推导.md` §1 推论 1.1），挠率方程**是代数方程、不传播**——它只由物质自旋流代数地决定，不是独立传播自由度。因此 4D 里的 $T^2$ 项本质是"自旋–自旋接触项"，不是"传播型挠率场"。要让挠率真正动力学化，必须要么给 coframe/自旋联络加动能项，要么显式耦合费米物质（挠率由自旋源生）。这是真实边界，不是自由断言。

**B5 — 相对论提升的零曲线陷阱。** 你的约束 $|\dot{\mathbf R}|=c$ 使 4-世界线 $(ct,\mathbf R(t))$ 的切矢模长为 $c^2-c^2=0$——它是**零曲线（null curve）**，零曲线的 Minkowski 弧长恒为 0，不能再用"$s=ct$"作 4D 弧长参数。严格说，这里是把 $t$ 当作外部仿射参数、对空间投影做几何变分。把世界线提升为相对论不变形式（类时/类光曲线、含拉格朗日乘子的类光约束）需要另外处理，不可直接照搬 3D 弧长论证。

---

## 8. 结论与下一步

我们已经把"几何螺旋必然性"从哲学陈述，推进为一个**具有变分结构、欧拉方程、几何唯一性定理、且机器核对通过**的 1D 几何动力系统。它比"垂直原理"强，因为它真的从 $\delta S=0$ 推出螺旋。

但它**仍不是第一性理论**：$\kappa_0,\tau_0$ 是外源锚定，且 4D 提升有 B4/B5 两条真实边界。

下一步四条路线（按"最扎实→最大野心"排序）：

1. **严格推导 $\kappa$–$\tau$ 作用量的 6 阶欧拉方程**（直路，验证与捷径一致）——纯数学，零风险；
2. **推广为连续场**：把曲线推广为场，研究是否能从几何极小原理自然产生 $1/r^2$ 势（这是连接"几何螺旋"与引力的关键一跃，风险高）；
3. **动力学化锚定**：用 Noether 守恒量（轴向动量）替代"钉扎 $\tau_0$”，看螺旋能否在最小化总曲率+守恒约束下涌现（部分解决 B1）；
4. **相对论/4D 版本**：处理 B4/B5 后构造类光世界线的相对论不变作用量，再接 `07_统一场方程`。

我建议按 **1 → 3 → 2 → 4** 的顺序推进：先在 1D 把变分方程彻底坐实（路线 1），再用 Noether 电荷替代外部锚定（路线 3），然后才谈场论提升（路线 2、4）。这样既保持严谨，又逐步逼近"尺度由内部动力学决定"的目标。
