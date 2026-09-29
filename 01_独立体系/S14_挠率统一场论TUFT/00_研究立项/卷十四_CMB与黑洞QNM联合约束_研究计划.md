# 卷十四 · CMB 嵌套采样后验诊断 + 黑洞 QNM 基准校验（并行执行）

> 状态：规划 / 设计稿（代码骨架待落地）。
> 红线：数学自洽 ≠ 物理实验证实。贝叶斯因子仅对比该现象学 $f_\text{NL}$ 阶跃模型，不是 TUFT 本体公理的证伪。
> 依赖：Python 3.8 + numpy + sympy（既有）；numpyro / arviz / jax（新增，用于嵌套采样与诊断）。

## 0. 卷十四归档条目规划

| 条目 | 内容 | 状态 |
|---|---|---|
| 14.1 | 复 EC 张量守恒约束 | 规划（未展开） |
| 14.2 | RG 缺口定理 N，ODE 与贝叶斯模型 | 规划（未展开） |
| 14.3 | CMB 原初非高斯双谱，嵌套采样与模型比对 | 主线 A（设计完成，待采样） |
| 14.4 | 球对称 EC 黑洞，PML-FDTD QNM 求解 | 主线 B（框架完成，待基准） |
| 14.5 | 基准校验、参数扫描、LIGO ringdown 约束 | 主线 B（见 §B.1–B.2） |
| 14.6 | 多信使联合约束 | 见 §跨分支 |
| 14.7 | 可证伪性与实验排除边界 | 规划（未展开） |
| 14.8 | 与 No‑Go III / No‑Go VI 的自洽性核验 | 规划（未展开） |

---

## 主线 A：CMB 拓扑跃迁模型｜后验收敛诊断与贝叶斯因子计算

### A.1 收敛判据（MCMC 标准诊断）

采样器：`numpyro.infer.NestedSampler`
核心收敛指标：

1. $\hat R$（潜在尺度缩减因子）：$\hat R < 1.05$ 判定收敛；
2. $N_\text{eff}$ 有效样本数：$N_\text{eff} > 1000$；
3. 迹图（trace plot）：无漂移、无分层，混合均匀；
4. 对数证据 $\log Z$ 误差：$\Delta\log Z < 0.5$。

```python
# 承接上一段 numpyro 代码，后验诊断函数
import arviz as az

def diagnostics(ns):
    # 转为 arviz 数据结构
    idata = az.from_numpyro(ns)
    # 计算 Rhat 与有效样本
    rhat = az.rhat(idata)
    neff = az.ess_bulk(idata)
    print("Rhat:\n", rhat)
    print("Effective sample size:\n", neff)
    # 迹图
    az.plot_trace(idata, compact=True)
    # 后验分布直方图
    az.plot_posterior(idata)
    # 对数证据
    logZ = ns.get_log_marginal_likelihood()
    logZ_err = ns.get_log_marginal_likelihood_error()
    print(f"logZ = {logZ:.3f} +/- {logZ_err:.3f}")
    return idata, logZ, logZ_err
```

### A.2 ΛCDM 基线模型 $M_0$（无拓扑跳变，$\Delta f_\text{NL}=0$）

```python
def lcdm_cmb_model(obs_l, obs_fnl, obs_sigma=None):
    # 无跳变，仅固定 ΛCDM f_NL
    fnl_model = fnl_lcdm
    with numpyro.plate("obs", len(obs_l)):
        numpyro.sample("obs_fnl", dist.Normal(fnl_model, obs_sigma), obs=obs_fnl)
```

运行嵌套采样得到 $\log Z_0$。

贝叶斯因子：
$$B_{10}=\exp\left(\log Z_1-\log Z_0\right)$$

判定标尺：

- $B_{10}>100$：强证据支持 TUFT 拓扑跃迁模型；
- $10<B_{10}<100$：中等证据；
- $1<B_{10}<10$：弱证据；
- $B_{10}<1$：数据偏好 ΛCDM，TUFT 该分支被削弱。

> **重要边界**：贝叶斯因子仅对比该现象学 $f_\text{NL}$ 阶跃模型，不是 TUFT 本体公理的证伪。就算 $B_{10}\ll 1$，仅排除「原初拓扑跃迁产生 $f_\text{NL}$ 跳变」这个预言，复张量 EC 几何公理框架保留。

### A.3 RG 参数映射后验投影

采样得到的后验 $p(t_c,\Delta f_\text{NL}|data)$，可投影回 RG 流：

- 取后验样本的 $t_c$，代入 RG ODE，重建 $r(t)$ 轨迹；
- 提取拓扑跃迁处 $\Delta\beta_r$ 的后验分布；
- 生成 2D 联合后验等高线图：$t_c$ vs $\Delta f_\text{NL}$。

```python
# 从 t_c 后验样本重建 RG 流轨迹
def reconstruct_rg_trajectory(samples):
    t_c_samples = samples["t_c"]
    traj_set = []
    for tc in t_c_samples:
        t_arr, sol = integrate_rg(p=(tc, 0.01, -0.02))
        traj_set.append(sol)
    return t_arr, jnp.array(traj_set)
```

---

## 主线 B：黑洞 QNM｜基准校验（$T_B=0$，退化为 Schwarzschild）

目标：当 $T_B=0$，模型输出必须复现标准 Schwarzschild 黑洞 QNM，作为数值求解器的基准校验。
$(M=1)$，$(l=2)$（四极模，引力波 ringdown 主导模），标准参考值：
$$\omega_\text{ref}\approx 0.37367 - 0.08896i$$
实部为振荡频率，虚部绝对值为衰减率。

### B.1 校验流程

1. 令 $T_B=0$，关闭挠率势；
2. 网格收敛测试：逐步加密 $(N=400,800,1600)$，检查 $\omega$ 收敛性；
3. 残差判据：$|\omega_\text{num}-\omega_\text{ref}| < 10^{-4}$，判定求解器基准通过；
4. 基准通过后，再开启 $T_B$ 扫描。

```python
def benchmark_schwarzschild():
    # TB=0，纯 Schwarzschild 基准
    TB_test = 0.0
    rstar = jnp.linspace(-20, 20, 1600)
    sigma_pml = jnp.zeros_like(rstar)
    sigma_pml[:160] = 2.0
    sigma_pml[-160:] = 2.0
    A, B = build_fdtd_matrix(rstar, TB_test, sigma_pml)
    vals, vecs = eigs(A, M=B, k=6, sigma=0.37 - 0.09j)
    omega = jnp.sqrt(vals)
    # 筛选 l=2 基频模
    omega_sorted = sorted(omega, key=lambda x: jnp.abs(x.real - 0.37367))
    omega0 = omega_sorted[0]
    print(f"Numerical omega (TB=0): {omega0:.6f}")
    print(f"Reference omega: 0.37367 - 0.08896i")
    err = jnp.abs(omega0 - (0.37367 - 0.08896j))
    print(f"Absolute error: {err:.2e}")
    return omega0, err
```

> 基准校验通过后，进入参数扫描区间：
> $$T_B \in [0,\ 10^{-4}]$$
> 取离散采样点：$0,\ 10^{-5},2\times10^{-5},5\times10^{-5},10^{-4}$
> 对每个 $T_B$ 求解 $\omega(T_B)$，输出数据表，拟合两个响应函数：
> $$\omega_R(T_B)=\omega_R^{(0)} + k_R\, T_B,\qquad \omega_I(T_B)=\omega_I^{(0)} + k_I\, T_B$$
> $k_R,k_I$ 为挠率对频率、衰减率的线性耦合系数。

### B.2 LIGO ringdown 波形模型

QNM 叠加波形（单模近似，$(l=2)$）
$$h(t)=A e^{-\omega_I t}\cos\left(\omega_R t + \phi\right)$$
$A$ 振幅，$\phi$ 初相位。

损失函数：
$$\chi^2_\text{grav}(T_B,M,A,\phi)=\int \frac{|h_\text{model}(t)-h_\text{obs}(t)|^2}{S_n(f)} df$$
可嵌入 Numpyro 做引力波单源 MCMC，约束 $T_B$ 的 90% 置信上限。

---

## 跨分支联合约束（多信使，CMB + 引力波）

构建联合似然：
$$\log\mathcal{L}_\text{joint}=\log\mathcal{L}_\text{CMB}+\log\mathcal{L}_\text{GW}$$
采样参数集：$\{t_c,\Delta f_\text{NL},T_B,M,A,\phi\}$。

> 物理关联：$t_c$ 是普朗克尺度拓扑跃迁能标；$T_B$ 是黑洞时空背景挠率。TUFT 本体假设二者同源，由同一套复曲率几何支配；联合采样可以检验两个预言通道参数是否自洽兼容。

---

## 当前状态

- CMB 模块：模型定义完成，后验诊断工具就绪，等待采样运行；
- QNM 模块：PML-FDTD 框架完成，**待执行 Schwarzschild 基准校验**。

### 下一步执行顺序

1. 运行 `benchmark_schwarzschild()` 完成黑洞求解器基准验证；
2. 基准通过后，扫描 $T_B$ 生成 $\omega_R,\omega_I$ 数据表；
3. 并行执行 CMB 嵌套采样，计算后验与贝叶斯因子。

---

## 待落地依赖（代码骨架引用的未实现函数）

- `build_fdtd_matrix(rstar, TB, sigma_pml)`：PML-FDTD 复曲率-挠率波动方程的矩阵装配（主线 B）；
- `integrate_rg(p)`：RG 流 ODE 数值积分（主线 A.3）；
- `fnl_lcdm` / `fnl_model`：CMB $f_\text{NL}$ 预言映射（主线 A.2）。

> 上述函数为设计占位，基准校验与采样运行前须先实现。代码骨架见
> `07_计算复现/源码/tuft_卷十四_CMB嵌套采样_后验诊断.py` 与
> `07_计算复现/源码/tuft_卷十四_黑洞QNM_PMLFDTD基准校验.py`。
