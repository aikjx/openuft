# 方向 F · 弯曲时空的规范协变导数：$D_\mu=\nabla_\mu-i\frac{q}{\hbar}A_\mu$

> 对应 [README §5](../README.md) 的延伸方向 F（新增），**具体实现并检验审计项 A8**（「规范协变导数不限于平直时空」）。
> 核验脚本 [`verify_extension_F_curved_gauge.py`](verify_extension_F_curved_gauge.py)，运行报告
> [`verify_extension_F_curved_gauge_report.txt`](verify_extension_F_curved_gauge_report.txt)。
> 结果：**PASS = 8 / FAIL = 0 / BOUNDARY = 0 / INFO = 0**。

---

## 背景与目标

[T5](../T5_三种导数数学与本体论对比.md) 声明规范协变导数 $D_\mu=\partial_\mu-i\frac{q}{\hbar}A_\mu$，并给出修正项 A8：$D_\mu$ **不限于平直时空**，弯曲时空可作 $\partial_\mu\to\nabla_\mu$ 的最小替换。但此前只声明、未验证。本方向在 **Schwarzschild 背景**上具体实现

$$D_\mu=\nabla_\mu-i\frac{q}{\hbar}A_\mu=\nabla_\mu-ig A_\mu,\qquad g\equiv\frac{q}{\hbar}$$

并证明、验证两类场（标量 / 矢量）的对易子结构——这是 A8 的具体落地，也是规范场论与广义相对论并存的正确表述。

**背景**：Schwarzschild 度规 $g_{\mu\nu}=\mathrm{diag}\!\left(1-\frac{2M}{r},\;-\left(1-\frac{2M}{r}\right)^{-1},\;-r^2,\;-r^2\sin^2\theta\right)$，列维-奇维塔联络 $\Gamma^\rho_{\ \sigma\mu}$ 由无挠 + 度规相容唯一确定（复用 E 组的联络/曲率机器）。

**规范场**：静态电势 $A_\mu=(\Phi(r),0,0,0)$，场强 $F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu$，非零分量 $F_{0r}=-\Phi'(r)$。

---

## 求导（三类场的最小替换）

**标量场** $\psi$：标量协变导数等于偏导（无联络项），
$$\nabla_\mu\psi=\partial_\mu\psi \;\Longrightarrow\; D_\mu\psi=\partial_\mu\psi-igA_\mu\psi$$

**矢量场** $V^\rho$：
$$\nabla_\mu V^\rho=\partial_\mu V^\rho+\Gamma^\rho_{\ \sigma\mu}V^\sigma \;\Longrightarrow\; D_\mu V^\rho=\partial_\mu V^\rho+\Gamma^\rho_{\ \sigma\mu}V^\sigma-igA_\mu V^\rho$$

**动量平移**（最小耦合算子实现）：$-i\hbar D_\mu=-i\hbar\nabla_\mu-qA_\mu$（即 $p_\mu\to p_\mu-qA_\mu$）。

---

## 证明（核心命题）

### 命题 F-1：标量对易子与度规无关

$$[D_\mu,D_\nu]\psi=-ig\,F_{\mu\nu}\psi$$

推导：$D_\mu=\partial_\mu-igA_\mu$（标量上 $\nabla_\mu=\partial_\mu$），
$$[D_\mu,D_\nu]\psi=-ig(\partial_\mu A_\nu-\partial_\nu A_\mu)\psi=-igF_{\mu\nu}\psi$$

**含义**：标量场携带电荷时，弯曲时空**不改变**阿贝尔规范对易子——曲率不进入标量场的最小耦合。

### 命题 F-2：矢量对易子含曲率项

$$[D_\mu,D_\nu]V^\rho=R^\rho_{\ \sigma\mu\nu}V^\sigma-ig\,F_{\mu\nu}V^\rho$$

推导：$[D_\mu,D_\nu]=[\nabla_\mu-igA_\mu,\nabla_\nu-igA_\nu]$，展开得
$$[\nabla_\mu,\nabla_\nu]V^\rho=R^\rho_{\ \sigma\mu\nu}V^\sigma,\quad
[\nabla_\mu,A_\nu]V^\rho=(\partial_\mu A_\nu)V^\rho,\quad
[A_\mu,\nabla_\nu]V^\rho=-(\partial_\nu A_\mu)V^\rho,\quad
[A_\mu,A_\nu]=0$$

**含义**：矢量场（或一般张量/旋量）最小耦合时，曲率项 $R$ 与场强项 $F$ **同时**出现——这是规范场论与 GR 并存的关键结构，也是标量与矢量在弯曲规范理论的本质区别。

### 命题 F-3：弯曲背景规范协变性

$D_\mu$ 在弯曲时空仍是规范协变的：对 $\psi'=e^{-ig\lambda}\psi$、$A'_\mu=A_\mu-\partial_\mu\lambda$（$\lambda$ 为标量，$\partial_\mu\lambda=\nabla_\mu\lambda$），有
$$D'_\mu\psi'=e^{-ig\lambda}D_\mu\psi$$

---

## 验证（脚本逐项，PASS=8）

| 项 | 命题 | 判定 |
|---|---|---|
| F1 | 标量 $[D_\mu,D_\nu]\psi=-igF_{\mu\nu}\psi$（Schwarzschild，5 组抽样） | ✅ 符号恒等 |
| F2 | 矢量 $[D_\mu,D_\nu]V^\rho=R^\rho_{\ \sigma\mu\nu}V^\sigma-igF_{\mu\nu}V^\rho$（4 组×4 分量） | ✅ 曲率项出现 |
| F3 | 弯曲背景规范协变 $D'\psi'=e^{-ig\lambda}D\psi$（4 分量） | ✅ |
| F4 | 动量平移 $-i\hbar D_\mu=-i\hbar\partial_\mu-qA_\mu$（4 分量，$g=q/\hbar$） | ✅ |
| F5 | $[(q/\hbar)A_\mu]=\mathrm{L}^{-1}=[D_\mu]$（弯曲时空仍成立） | ✅ |
| F6 | $[D_\mu]=\mathrm{L}^{-1}$（弯曲不改变微分算子量纲） | ✅ |
| F7 | 标量对易子（含具体势 $\Phi=Q_0/r$）符号恒等 | ✅ |
| F8 | 标量对易子数值残差（$r=4M$，$\Phi=Q_0/r$） | ✅ 残差 $0.000e+00$ |

**实现要点**：矢量对易子的嵌套协变导数须含偏导项（中间矢量分量依赖坐标）；标量用偏导（$\nabla_\mu\psi=\partial_\mu\psi$）；动量平移须代入 $g=q/\hbar$ 关联。

---

## 精算（50 位）

F8 在 Schwarzschild $r=4M$、$\Phi=Q_0/r$ 处对标量对易子做数值代入，**残差 = 0.000e+00**（精确零，优于 $10^{-20}$）。方向 F 其余项为符号恒等，无数值需求。

---

## 边界与口径

- **A8 落地**：本方向证实 $D_\mu=\nabla_\mu-igA_\mu$ 在弯曲时空是良定义的规范协变算子，且保持 $[D_\mu]=\mathrm{L}^{-1}$。
- **标量 vs 矢量**：标量对易子无曲率项（F1），矢量对易子有曲率项（F2）——这是两类场的最小耦合结构差异，非近似而是精确恒等。
- **记号**：$g\equiv q/\hbar$ 为 SI 规范耦合；弯曲时空 $\partial_\mu\to\nabla_\mu$ 与规范场引入是**并行**的最小替换，不互为因果。
- **范围**：本方向限于 Schwarzschild 静态背景与阿贝尔 $U(1)$ 规范场；非阿贝尔（Yang-Mills）弯曲规范协变导数（含李代数结构常数项）为后续延伸。

---

## 与其他条目的对照

| 条目 | 关系 |
|---|---|
| [T5](../T5_三种导数数学与本体论对比.md) | 本方向是其修正项 A8 的具体实现与数值检验 |
| [延伸方向 A](求导证明验证精算分析.md) | A 组在平直时空的 $F_{\mu\nu}$；本方向推广到弯曲时空 |
| [延伸方向 E](求导证明验证精算分析.md) | 复用其 Schwarzschild 联络/曲率机器（$R^\rho_{\ \sigma\mu\nu}$） |
| [经典作用量 D2 杨-米尔斯](../../经典基准/经典作用量/D2_杨米尔斯/README.md) | 非阿贝尔弯曲规范协变导数为其后续推广对象 |

---

## 复现

```bash
python verify_extension_F_curved_gauge.py
# 结果：PASS = 8 / FAIL = 0（报告固化于 verify_extension_F_curved_gauge_report.txt）
```

依赖：sympy（符号）+ mpmath（50 位）；量纲用标准库 Fraction。

---

*本文档对应延伸方向 F，按「求导 / 证明 / 验证 / 精算」四件套展开，具体实现审计项 A8（规范协变导数不限于平直时空），与 `verify_extension_F_curved_gauge.py` 逐项对应。*
