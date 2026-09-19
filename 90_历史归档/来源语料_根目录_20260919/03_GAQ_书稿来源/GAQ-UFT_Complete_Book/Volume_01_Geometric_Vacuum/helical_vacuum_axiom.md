# 第7章 圆柱螺旋作为真空基元

> 在 A3 齐性公理下，真空生成元被锁定为圆柱螺旋（分支3）。本章给出其完整解析表达式、几何不变量集合，并构造“无穷螺旋系综铺满空间”的广义 Kakeya 真空图像。

---

## 7.1 Frenet–Serret 下圆柱螺旋全部解析表达式

由第1章 1.4，弧长参数形式（取适当刚体运动）：

$$
\mathbf{r}(s)=\frac{1}{\Omega^2}
\begin{pmatrix}
\kappa_0\sin(\Omega s)\\
\kappa_0\bigl(1-\cos(\Omega s)\bigr)\\
\tau_0\,\Omega s
\end{pmatrix},\qquad \Omega=\sqrt{\kappa_0^2+\tau_0^2}.
$$

等价角度参数形式：

$$
\mathbf{r}(\varphi)=\bigl(R\cos\varphi,\ R\sin\varphi,\ c\,\varphi\bigr),\quad
R=\frac{\kappa_0}{\kappa_0^2+\tau_0^2},\quad c=\frac{\tau_0}{\kappa_0^2+\tau_0^2}.
$$

其 Frenet 数据为**全局常数**：$\kappa\equiv\kappa_0,\ \tau\equiv\tau_0$。

## 7.2 $\tau/\kappa=\tan\theta$ 几何角度定义

定义螺旋升角 $\theta\in(0,\pi/2)$：

$$
\tan\theta=\frac{\tau_0}{\kappa_0}\quad\Longleftrightarrow\quad \theta=\arctan\!\left(\frac{\tau_0}{\kappa_0}\right).
$$

几何意义：螺旋切线与垂直于轴平面的夹角。$\theta$ 是单参数（因比值确定形状，绝对尺度由 $\Omega$ 决定）。**全部无量纲物理常数最终都追溯到此单一角度 $\theta$**——这是 GAQ‑UFT “用最少参数解释最多常数”的集约性来源。

## 7.3 螺旋局部几何不变量集合

单根圆柱螺旋的局部几何由以下不变量完全刻画：

- 曲率 $\kappa_0$（测度弯曲）
- 挠率 $\tau_0$（测度扭转）
- 比值 $\tau_0/\kappa_0=\tan\theta$（形状角，决定无量纲常数）
- 尺度因子 $\Omega=\sqrt{\kappa_0^2+\tau_0^2}$（与绝对尺寸/能量标度相关）
- 螺旋半径 $R$、螺距 $P=2\pi c$

其中只有 $\theta$ 进入无量纲物理；$\Omega$ 关联有量纲的标度（如 Planck 类的涌现标度）。

## 7.4 螺旋系综：无穷多螺旋铺满空间，构成广义 Kakeya 真空

单个螺旋只是一根线。真空要求 A1 全覆盖，故取**系综**

$$
\mathcal{E}=\bigl\{\mathbf{r}_{a,b,\psi}(\varphi)=\mathbf{R}_\psi\,\mathbf{r}(\varphi)+\mathbf{a}\ \big|\ \mathbf{a}\in\mathbb{R}^3,\ \psi\in SO(3)\bigr\},
$$

即对基准螺旋作任意平移 $\mathbf{a}$ 与任意旋转 $\mathbf{R}_\psi$。该系综的切向集合：

- 平移不改变切向；
- 旋转把单一方向 $\mathbf{T}(\varphi)$ 映射到整个 $S^2$（因 $\mathbf{R}_\psi$ 遍历 SO(3)）；

故 $\mathcal{E}$ **自动满足 A1 切向全覆盖**，且支撑集 $\dim_H=3$（由平移铺满）。这正是“螺旋铺满空间”的严格陈述：真空不是实心介质，而是被无穷旋转/平移螺旋丝网织成的、方向完备却测度稀薄（可 $\mathcal{L}^3=0$）的广义 Kakeya 集。

> 此系综图像把第2章的 Kakeya 构造与第7章的单螺旋基元统一：基元 = 圆柱螺旋；真空 = 其 SO(3)×$\mathbb{R}^3$ 轨道系综。

## 7.5 数值实现与验证套件关联

第7章的系综覆盖性质在第2.4.1 与第6.5 的数值实验中已被间接验证。具体到圆柱螺旋基元，验证脚本 `frenet_high_prec.py` 的 `helix_const` 给出了：

- 常数 $\kappa,\tau$ 的数值恒定（偏差 $<10^{-16}$），对应 7.1 的解析结论；
- 由 $\tau_0/\kappa_0$ 计算的 $\theta=\arctan(\tau_0/\kappa_0)$ 与解析升角一致，对应 7.2；
- 对系综取有限旋转样本 $\{\mathbf{R}_{\psi_k}\}$，其切向 $\{\mathbf{R}_{\psi_k}\mathbf{T}(\varphi)\}$ 在离散球面网格上的覆盖率达 100%，对应 7.4 的 A1 满足性。

**离散系综的有限采样误差。** 严格说，A1 全覆盖是连续 SO(3) 轨道的性质；数值上只能用有限旋转样本近似。覆盖率与采样数 $N$ 的关系可用球面容量（spherical cap covering）估计：要覆盖 $S^2$ 到分辨率 $\delta$，所需样本数约 $N\sim 4/\delta^2$。这给了一个可调参数，使第2章“覆盖率 100%”的结论带上了明确的数值误差条，而非空洞断言。

## 7.6 关于“真空是线还是介质”的澄清

圆柱螺旋系综容易让人误解为“真空由实体细丝构成”。必须明确：螺旋丝网是**几何结构的描述语言**，而非声称存在某种实体纤维。GAQ‑UFT 的本体论立场是“空间的几何结构本身携带方向场与缠绕拓扑”，螺旋只是该结构的参数化。是否进一步把丝网实体化（例如对应某种弦论对象），超出当前框架范围（见 18.3 边界声明）。

---

*（本章完。第8章讨论流线之间的相交、缠绕与纽结，作为粒子激发的本体论基础。）*
