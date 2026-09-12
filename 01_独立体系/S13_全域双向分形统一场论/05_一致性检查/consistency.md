# 一致性检查：参数归并、量纲自洽与奥卡姆判据

> 体系：全域双向分形统一场论（S13）· 假设版本 v1.2-20260911
> 出处：理论总纲 V1.2 第六节；书稿第 17、20 章；`dimension_unify_verify.py`

## 一、参数归并（奥卡姆）

原始自由参数：带量纲的 $\left\{ \lambda, \ell, v \right\}$。归并关系：

$$
v = \ell^{-1}, \qquad \lambda = v\,\tilde{g}, \qquad \kappa = \tilde{\kappa}
$$

归并后：两个无量纲 $\left\{ \tilde{g}, \tilde{\kappa} \right\}$ + 一个标度 $\ell$（共 3 个自由度）。大白话：最短尺度、真空值、对偶耦合本是同一把尺子的三面，砍掉一半参数。

## 二、量纲自洽（验证 A/B，`dimension_unify_verify.py`）

自然单位 $c = \hbar = 1$ 下（L=ℓ, T=ℓ, M=ℓ⁻¹）：

| 常数 | 量纲 $[\cdot] = \ell^{n}$ | 检查 |
|---|---|---|
| $c$, $\hbar$, $\alpha$ | $\ell^{0}$ | 无量纲 |
| $G$ | $\ell^{+2}$ | — |
| $\Lambda$ | $\ell^{-2}$ | — |
| $m_{H}$, $m_{W}$, $v$, $\lambda$ | $\ell^{-1}$ | $v = \ell^{-1}$ ✓；$\lambda = v\tilde{g}$ → $\ell^{-1}$ ✓ |
| $\kappa$ | $\ell^{0}$ | $\kappa$ 直接无量纲（修正）✓ |
| $\ell$ | $\ell^{+1}$ | 标度 |
| $\tilde{g}$, $\tilde{\kappa}$ | $\ell^{0}$ | 无量纲 |

数值自洽：$m_{H}^{2} = 8\kappa v^{2}$（海森谱闭式）与 $m_{H} = 2\sqrt{2}\sqrt{\tilde{\kappa}}/\ell$（公式）在随机参数下差 $\sim 10^{-16}$（机器一致）。

## 三、常数关联（可检验性，V1.3.1 统一口径）

统一生成元归一化（$\tau/2$，与第21章验证D一致）后：

$$
\frac{m_{H}}{m_{W}} = \frac{4\sqrt{2}\,\sqrt{\tilde{\kappa}}}{\tilde{g}}, \qquad
\frac{m_{Z}}{m_{W}} = \sqrt{1 + \frac{\tilde{g}'^{2}}{\tilde{g}^{2}}} = \frac{1}{\cos\theta_{W}}
$$

比例由 $\left\{ \tilde{g}, \tilde{g}', \tilde{\kappa} \right\}$ 唯一决定，与 $\ell$ 无关——常数之间可检验关联的存在性。（V1.3.1 勘误：此前 $m_{H}/m_{W}$ 写作 $2\sqrt{2}\sqrt{\tilde{\kappa}}/\tilde{g}$，系 $\tau$ 归一化约定，统一为 $\tau/2$ 后因子为 $4\sqrt{2}$。）

## 四、依赖图一致性（验证 D）

主系统 M1–M6 依赖图的传递闭包：**公理全可达、零环**（M1→M2→M3；M1 约束→希格斯；M4↔M5；M6 收拢）。无循环论证。

## 五、归一化（验证 E）

$\hat\Psi^{\dagger}\hat\Psi = 1$ 残差 $5.6\times10^{-16}$；$g^{\mathrm{eff}}$ 自对偶残差 $3.3\times10^{-16}$——机器精度。

## 六、口径闭合（V1.3.1，`consistency_verify.py`）

① 弱混合角：$e = \tilde{g}\sin\theta_{W} = \tilde{g}'\cos\theta_{W}$（差 $5.6\times10^{-17}$），$m_{Z} = m_{W}/\cos\theta_{W}$（差 $0$）；② 新口径 $m_{H}/m_{W} = 4\sqrt{2}\sqrt{\tilde{\kappa}}/\tilde{g}$ 与质量值精确一致（差 $0$）；③ 四观测 $\left\{ m_{W}, m_{Z}, m_{H}, \alpha \right\}$ 反解四未知 $\left\{ v, \tilde{g}, \tilde{g}', \tilde{\kappa} \right\}$，三组随机参数最大误差 $\sim 10^{-16}$——参数系统完全钉死，无多余自由度。

## 诚实边界

量纲自洽与参数归并是**理论内部一致性**检查，不构成对理论本体的实验认证。
