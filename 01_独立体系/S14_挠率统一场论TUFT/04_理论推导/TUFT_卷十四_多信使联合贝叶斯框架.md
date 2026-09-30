# TUFT｜卷十四完整定稿：多信使联合贝叶斯框架

> 归属：`01_独立体系/S14_挠率统一场论TUFT`，生命周期阶段 `04_理论推导`。
> 承接前面所有 RG 流、CMB 双谱、FDTD 黑洞 QNM、多信使联合 MCMC 体系。
> 体系总纲：TUFT（Twisted Unified Field Theory，挠曲统一场论）基于爱因斯坦–嘉唐 EC 复张量几何；拓扑 RG 缺口定理 N 给出原初宇宙拓扑相变；黑洞背景挠率修正 QNM ringdown；CMB 原初非高斯性 $f_\text{NL}$ 阶跃跳变与引力波 ringdown 构成双独立观测通道；联合 MCMC 检验两个通道参数同源性。
> 配套：源码 [`tuft_v14_multimessenger_bayes.py`](../07_计算复现/源码/tuft_v14_multimessenger_bayes.py)；诚实分析与治理裁决见 [`TUFT_卷十四_诚实分析与治理裁决.md`](../11_证伪与反例/TUFT_卷十四_诚实分析与治理裁决.md)。

---

## 卷十四目录

1. 体系回顾与物理假设清单
2. RG 缺口定理 N：拓扑跃迁 RG 流 ODE
3. CMB 原初双谱与 $f_\text{NL}$ 拓扑跳变模型
4. EC 球对称黑洞、挠率势、FDTD-PML QNM 求解器与基准校验
5. $T_B$ 扫描、QNM 线性响应拟合
6. 多信使联合似然与 Numpyro 完整联合 MCMC 模型
7. MCMC 收敛诊断、后验可视化、$t_c-T_B$ 二维 KDE
8. 模型比对：贝叶斯因子 / LOO 交叉验证
9. 全部误差源与模型局限性
10. 完整可证伪判据（实验排除边界）
11. 后续拓展路线图
12. 附录：完整可运行整合代码（JAX+NumPyro+ArviZ+SciPy+Matplotlib）

---

## 1. 体系回顾与物理假设清单

### 基础公理（TUFT）

1. 时空几何为**复值爱因斯坦–嘉唐（EC）流形**，同时携带曲率 $\kappa$ 与挠率 $\tau$；挠率不是物质源的衍生量，是独立几何自由度。
2. RG 流在临界对数能标 $t_c=\ln(\mu_c/M_\text{Pl})$ 发生**拓扑缺口跃迁**：β 函数一阶导数不连续，RG 流非解析（缺口定理 N）。
3. 低能红外（$t\ll t_c$）：拓扑冻结，挠率效应几乎解耦，理论平滑回归标准模型+ΛCDM；不破坏现有低能实验约束。
4. 两个可观测遗迹：
   - 宇宙原初阶段拓扑跃迁：CMB 双谱 $f_\text{NL}(l)$ 出现阶跃跳变；
   - 黑洞内部背景挠率场 $T_B$：修改黑洞拟正则模 QNM 频率与衰减率，体现在引力波 ringdown。
5. 强假设：$t_c$（原初拓扑跃迁能标）与 $T_B$（黑洞背景挠率）来自同一套复张量场动力学，**二者存在统计关联**，这是多信使检验核心。

### 模型近似假设（必须写入局限性章节）

1. CMB：采用局部型 $f_\text{NL}$ 现象学阶跃模型，不完整求解原初曲率扰动传递函数；
2. QNM：小挠率 $T_B\ll10^{-4}$，QNM 频率采用线性近似；基础波形只使用 $l=2$ 四极主导模；
3. 挠率势：指数衰减启发式近似，尚未从完整 TUFT 复张量场方程解析导出；
4. 噪声：观测噪声为高斯、不相关；忽略系统误差、仪器校准残差。

---

## 2. RG 缺口定理 N：拓扑跃迁 RG 流 ODE

对数能标：$t=\ln(\mu/M_\text{Pl})$，$t$ 增大 → 高能趋近普朗克尺度。

$$
\frac{dr}{dt}=\beta_r(r,t)=\lambda(r-r_0)+\Delta\beta_r\cdot H(t-t_c)
$$

- $r_0=0.0918$：低能红外 RG 固定点；
- $\lambda<0$：红外吸引固定点线性斜率；
- $H(t-t_c)$：Heaviside 阶跃函数；$t>t_c$ 高能拓扑相，β 函数出现有限跳变 $\Delta\beta_r$。

耦合到标准模型 RG：

$$
\beta(g,t)=b_0 g^3+b_1 g^5+\delta_\text{TUFT}(r(t)),\quad \delta_\text{TUFT}\propto \frac{dr}{dt}
$$

拓扑跃迁只在 $t\approx t_c$ 附近显著；$t\ll t_c$，$\delta_\text{TUFT}\to0$，回归标准模型 RG。

---

## 3. CMB 原初双谱与 $f_\text{NL}$ 拓扑跳变模型

原初双谱（局部型非高斯）

$$
B_\zeta(k_1,k_2,k_3)=\frac{6 f_\text{NL}}{(2\pi)^2}\frac{\zeta(k_1)\zeta(k_2)\zeta(k_3)}{k_1^2k_2^2k_3^2}\delta(\boldsymbol{k}_1+\boldsymbol{k}_2+\boldsymbol{k}_3)
$$

TUFT 修正：

$$
f_\text{NL}^\text{TUFT}(l)=f_\text{NL}^\Lambda+\Delta f_\text{NL}\cdot H(l-l_c),\quad l_c = \exp(t_c)\cdot \text{scale\_factor},\quad \text{scale\_factor}=12.0
$$

$\chi^2_\text{CMB}=\displaystyle\sum_l\frac{\big(f_\text{NL}^\text{TUFT}(l)-f_{\text{NL,obs},l}\big)^2}{\sigma_l^2}$

---

## 4. EC 球对称黑洞、挠率势、FDTD-PML QNM 求解器与基准校验

乌龟坐标

$$
r_*=r+2M\ln\left|\frac{r}{2M}-1\right|
$$

径向扰动方程：

$$
\frac{d^2\Psi}{dr_*^2}+\big(\omega^2-V_\text{eff}(r,T_B)\big)\Psi=0
$$

有效势

$$
V_\text{eff}(r,T_B)=\left(1-\frac{2M}{r}\right)\left[\frac{l(l+1)}{r^2}+\frac{2M}{r^3}+V_\text{torsion}(r,T_B)\right]
$$

挠率势：

$$
V_\text{torsion}(r,T_B)=T_B\cdot\frac{2M}{r^2}\exp\left(-\frac{r-2M}{2M}\right)
$$

PML 完全匹配层：复坐标拉伸 $\displaystyle\frac{d}{dr_*}\to\frac{1}{1+i\sigma(r_*)}\frac{d}{dr_*}$，消除视界/远场边界反射。
广义本征值问题：$A\Psi=\omega^2 B\Psi$，求解复频率 $\omega=\omega_R+i\omega_I$。

基准：$M=1$, $l=2$, $T_B=0$，参考值 $\omega_\text{ref}=0.37367-0.08896i$。
网格收敛测试：

- $N=400$，误差 $\approx1.2\times10^{-3}$
- $N=800$，误差 $\approx4.1\times10^{-4}$
- $N=1600$，误差 $\approx1.9\times10^{-4}$

---

## 5. $T_B$ 扫描、QNM 线性响应拟合

扫描点：$T_B\in\{0,10^{-5},2\times10^{-5},5\times10^{-5},10^{-4}\}$

| $T_B$ | $\omega_R$ | $\omega_I$ |
|---|---|---|
| $0$ | 0.37352 | -0.08884 |
| $1\times10^{-5}$ | 0.37356 | -0.08887 |
| $2\times10^{-5}$ | 0.37360 | -0.08890 |
| $5\times10^{-5}$ | 0.37372 | -0.08899 |
| $1\times10^{-4}$ | 0.37391 | -0.08914 |

最小二乘线性拟合：

$$
\begin{aligned}
\omega_R(T_B) &= 0.37352 + 3.88\, T_B \\
\omega_I(T_B) &= -0.08884 - 3.00\, T_B
\end{aligned}
$$

（注：原文拟合系数写作 `388`/`300` 系复制时的 LaTeX `\(0.0\)` 残留瑕疵，依据上表数据反解斜率分别为 3.88 与 3.00，已修正。）

物理解读：正背景挠率抬高振荡频率，加速衰减；线性区间 $T_B\in[0,10^{-4}]$；超出区间线性近似失效。

Ringdown 单模波形：

$$
h(t)=A e^{\omega_I t}\cos(\omega_R t+\phi)
$$

---

## 6. 多信使联合似然与 Numpyro 完整联合 MCMC 模型

联合对数似然：

$$
\log\mathcal{L}_\text{joint}=\log\mathcal{L}_\text{CMB}(t_c,\Delta f_\text{NL})+\log\mathcal{L}_\text{GW}(T_B,M,A,\phi)
$$

参数全集：

$$
\boldsymbol\theta=\{t_c,\Delta f_\text{NL},\;T_B,M,A,\phi\}
$$

先验：

- $t_c\sim \text{Uniform}(-3,1)$
- $\Delta f_\text{NL}\sim \mathcal{N}(0,0.15)$
- $T_B\sim \text{Uniform}(0,10^{-4})$
- $M\sim \text{Uniform}(0.9,1.1)$
- $A\sim\text{HalfNormal}(1.0)$
- $\phi\sim\text{Uniform}(0,2\pi)$

---

## 7. MCMC 收敛诊断、后验可视化、$t_c-T_B$ 二维 KDE

### 收敛判据（硬性）

1. $\hat R<1.05$；
2. $N_\text{eff(bulk)}>1000$；
3. 迹图无漂移、混合均匀；
4. 有效样本充足，无链分层。

### 后验可视化清单

1. 单参数边际后验直方图：$p(t_c),p(\Delta f_\text{NL}),p(T_B),p(M),p(A),p(\phi)$
2. 二维 KDE 等高图：**$t_c-T_B$（核心图）**，检验同源关联
3. 迹图（trace plot）诊断采样链行为
4. 预测检查：CMB $f_\text{NL}$ 预测带、GW ringdown 波形 90% 置信带

#### $t_c-T_B$ 等高图三种结果判定

1. **椭圆相关（正/负）**：$t_c,T_B$ 统计相关，支持 TUFT 同源几何场猜想；正向证据。
2. **近似圆形无相关云团**：参数独立；模型不自相矛盾，但缺少多信使关联证据。
3. **样本堆积在先验边界**：观测不支持拓扑跃迁/挠率效应；该分支被数据削弱。

---

## 8. 模型比对：贝叶斯因子 / LOO 交叉验证

模型集合：

- $M_0$：基线 ΛCDM，CMB 无 $f_\text{NL}$ 跳变，$T_B\equiv0$ 无挠率；
- $M_1$：单信使 TUFT-CMB，仅 CMB 拓扑跳变；
- $M_2$：多信使联合 TUFT（本模型）。

贝叶斯因子：

$$
B_{20}=e^{\log Z_2-\log Z_0}
$$

贝叶斯证据标尺（Jeffreys）

- $B>100$：强支持 TUFT；
- $10<B<100$：中等支持；
- $1<B<10$：弱支持；
- $B<1$：数据偏好 ΛCDM 基线。

> 高维联合模型下嵌套采样计算 $\log Z$ 数值不稳定；备选方案：LOO 交叉验证，计算 ELPD（expected log predictive density）做模型比较。

```python
import arviz as az
loo_result = az.loo(idata)
print(loo_result)
```

---

## 9. 全部误差源与模型局限性

### 数值误差

1. FDTD：空间网格截断误差；PML 残余边界反射；本征值求解器截断误差；
2. MCMC：有限样本噪声、先验体积效应；

### 物理近似误差

1. QNM：仅保留 $l=2$ 主导模；忽略高阶 $l=3,4$ 谐波；小 $T_B$ 线性近似；
2. 挠率势：启发式指数形式，未从 TUFT 场方程严格导出；
3. CMB：简化阶跃 $f_\text{NL}$，不是完整原初扰动传递函数；
4. 引力波：忽略自旋耦合、轨道进动、多模干涉。

### 观测误差

1. Planck CMB 分箱噪声；
2. LIGO 探测器噪声；忽略仪器系统误差、校准不确定性。

> **重要声明**：即使本模型所有预言被实验排除，TUFT 复张量 EC 几何框架本身不会被证伪；仅排除“拓扑缺口跃迁+黑洞挠率修正 QNM”这个特定低能分支。

---

## 10. 完整可证伪判据（实验排除边界）

### 判据 A：CMB 通道

高分辨率 CMB 双谱观测：在所有可观测多极区间 $l\in[20,500]$，**不存在 $f_\text{NL}$ 显著阶跃跳变** → 排除本拓扑跃迁分支。

### 判据 B：引力波 Ringdown 通道

大量 LIGO/Virgo/KAGRA ringdown 事件统计：黑洞 QNM 频率偏移上限严格压低，**$T_B$ 在 90% 置信度下与 0 无差异** → 排除黑洞挠率 QNM 修正分支。

### 判据 C：多信使联合判据

若 CMB 允许非零 $\Delta f_\text{NL}$（存在 $f_\text{NL}$ 跳变），但大量 ringdown 事件一致给出 $T_B=0$；后验 $t_c-T_B$ 完全无关联，且贝叶斯因子 $B_{20}<1$ → 本多信使同源假设被证伪。

---

## 11. 后续拓展路线图

1. QNM 升级：加入 $l=3,l=4$ 高阶角向模；放弃线性近似，MCMC 内部直接调用 FDTD 求解器（代价：计算量暴涨）；
2. 挠率势替换：从 TUFT 复张量场方程解析推导 $V_\text{torsion}$，替代当前启发式形式；
3. CMB 升级：替换阶跃 $f_\text{NL}$，接入完整原初曲率扰动功率谱+双谱传递函数；
4. 增加宇宙学第三观测通道：原初引力波 B 模偏振；
5. 拓展到旋转（Kerr）EC 黑洞，研究自旋–挠率耦合；
6. 并行开发：RG 流全局相图，完整拓扑相变相图，寻找更多固定点与 RG 流吸引子。

---

## 12. 附录：完整整合可运行代码

完整可运行整合代码（JAX+NumPyro+ArviZ+SciPy+Matplotlib）见源码文件
[`tuft_v14_multimessenger_bayes.py`](../07_计算复现/源码/tuft_v14_multimessenger_bayes.py)。

该代码已对原稿中的复制瑕疵做如下修订，以便实际运行与核验：

- 拟合系数 `388`/`300` 修正为表值一致的 `3.88`/`3.00`（见第 5 节说明）；
- 原稿 `h_obs` 被置为全零，导致 GW 似然在 $A\to0$ 处退化、无法约束 $T_B$（见诚实分析文档 §B-3）；代码改为**注入已知 $T_B$ 的合成 ringdown 信号 + 高斯噪声**，使 MCMC 能实际检验参数恢复；
- 核心数值（FDTD-PML 基准 + $T_B$ 扫描 + 线性拟合 + 信号恢复）改用 NumPy+SciPy 实现，可脱离 JAX/NumPyro 独立运行与核验；NumPyro 联合 MCMC 模型保留为可选模块（需安装 `numpyro`、`arviz`、`jax`）。

---

*本卷为 S14 体系下「多信使联合贝叶斯框架」分册。其方法学（联合似然 + NUTS + 收敛诊断 + 模型比较）属标准贝叶斯统计，正确；其物理主张（特别是 $t_c$–$T_B$ 同源关联与挠率 QNM 修正）的实证状态与 TUFT 既有审计结论的关系，见 [`TUFT_卷十四_诚实分析与治理裁决.md`](../11_证伪与反例/TUFT_卷十四_诚实分析与治理裁决.md)。登记不表示理论已成立。*
