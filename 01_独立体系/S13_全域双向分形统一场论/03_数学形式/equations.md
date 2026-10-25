# 数学形式：全域主方程系统（六方程闭环 M1–M6）

> 体系：全域双向分形统一场论（S13）· 假设版本 v1.2-20260911
> 出处：理论总纲 V1.2 第二节；书稿第 5–11 章
> 状态：方程已冻结并给出依赖链；每条方程的验证记录见 [09_验证结果](../09_验证结果/README.md)。

## 一、六方程闭环

| 编号 | 方程 | 物理角色 |
|---|---|---|
| M1 | 约束旋量方程 $\sigma^{\mu}\partial_{\mu}\Psi = \lambda\,\Theta\,\Psi^{*} + \mathrm{i}\,\zeta\,\Psi$，真空约束 $|\Psi|^{2} = v^{2}$ | 一切场的基元方程；阴生阳、阳生阴 |
| M2 | 涌现规范场 $a_{\mu} = \frac{\mathrm{i}}{2}\left( \hat\Psi^{\dagger}\partial_{\mu}\hat\Psi - \partial_{\mu}\hat\Psi^{\dagger}\hat\Psi \right)$；对偶帧联络 $\mathcal{A}_{\mu} = \mathcal{E}^{\dagger}\partial_{\mu}\mathcal{E}$，$\mathcal{E} = \left( \hat\Psi,\ \Theta\hat\Psi^{*} \right) \in U(2)$ | 规范结构从旋量相位几何自涌现 |
| M3 | 霍普夫拓扑荷 $Q_{H} = \frac{1}{4\pi^{2}}\int_{\mathbb{R}^{3}}\epsilon^{ijk}a_{i}\partial_{j}a_{k}\,\mathrm{d}^{3}x \in \mathbb{Z}$ | 拓扑守恒，整数、可计算、受保护 |
| M4 | 双向 $\beta$ 流 $\mu\,\frac{\mathrm{d}g}{\mathrm{d}\mu} = \beta\left( g \right)$，$\beta\left( -g \right) = -\beta\left( g \right)$ | 尺度维：紫外与红外互为镜像 |
| M5 | 对偶镜像度规 $g^{\mathrm{eff}}\left( r \right) = g^{\mathrm{eff}}\left( \ell^{2}/r \right)$ | 奇点化解：最短尺度 ℓ 处自对偶，曲率有界 |
| M6 | 因果畴通量 $\frac{\mathrm{d}}{\mathrm{d}t}\int_{\mathcal{C}}\omega = \oint_{\partial\mathcal{C}}\Theta$ | 全域演化收拢：畴内变化率恒等于穿壁通量 |

## 二、依赖链

```
M1 → M2 → M3（场生规范，规范载拓扑）
M1 真空约束 → 希格斯结构（真空流形 S³ = U(2)/U(1)，模式谱 {0,0,0,8κv²}）
M4 ↔ M5（尺度维两面镜像）
M6（全域总账房，收拢 M1 的流守恒）
六方程、一闭环，无一外挂
```

## 三、核心公式体系（五大板块）

**板块一（旋量对偶方程）**：$\sigma^{\mu}\partial_{\mu}\Psi = \lambda\,\Theta\,\Psi^{*}$，$\Theta = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$，对偶周期 4。

**板块二（拓扑荷）**：1D 绕数 $\frac{1}{2\pi\mathrm{i}}\oint\mathrm{d}z/z$ 已被证伪（$\pi_{1}\left( S^{2} \right) = 0$，见 11_证伪与反例）；正版为 3D 霍普夫荷 $Q_{H}$（$\pi_{3}\left( S^{2} \right) = \mathbb{Z}$）。

**板块三（双向重整化群）**：不动点 $g^{*} = \sqrt{\varepsilon/c}$，质量标度律 $m\left( \mu \right) = m_{0}\left( \mu/\mu_{0} \right)^{-\gamma}$，分形维度 $D = 4 - \gamma$。

**板块四（奇点化解）**：有效度规自对偶，曲率上界闭式 $\left| R \right|_{\max} = \frac{\left( 3 + 2\sqrt{2} \right)GM}{2\ell^{3}}$，极值位置 $r = \left( \sqrt{2} \pm 1 \right)\ell$。

**板块五（因果畴）**：零面围成因果畴，穿壁对偶翻转 $\Psi \to \Psi^{c}$、$Q \to -Q$，全时空总荷守恒。

## 四、参数系统（奥卡姆归并）

自由参数由带量纲的 $\left\{ \lambda, \ell, v \right\}$ 归并为两个无量纲 $\left\{ \tilde{g}, \tilde{\kappa} \right\}$ + 一个标度 $\ell$：

$$
v = \ell^{-1}, \qquad \lambda = v\,\tilde{g}, \qquad \kappa = \tilde{\kappa}
$$

大白话：最短尺度、真空值、对偶耦合本是同一把尺子的三面。

## 五、状态与诚实边界

六方程中 M1–M3、M5、M6 及 M4 的数值行为已实跑验证（见 09_验证结果）。M2 的动力学已定型（V1.3，拼图一：Yang–Mills 作用量、质量谱精确复现）。费米子代结构层完成（V1.4，第22章：$\mathbb{Z}_{4}$ 三实表示、第四代禁戒、六反常消去）。色 $SU(3)$ 候选框架（V1.5，第23章：$\mathbb{CP}^{2}$ 等距、稳定子电弱、色单态判据）。量子化形式化层（V1.6，第24章：BRST 幂零、单圈 $\beta$、双向对称量子对应）；常数统一部分推进（V1.6，第25章：对接闭环、电荷量子化、$\sin^{2}\theta_{W}=1/4$ 候选预言）；统一跑动检验（V1.7，第25.8节：CP² 候选电弱尺度差 5.4% 负面结果如实，MSSM 对照 $\sin^{2}\theta_{W}$ 预测差 0.12% 为对偶周期四↔超对称的候选锚点）。仍属 OPEN 项、不得当作已确立事实：$\alpha$ 量级与 $\Lambda$、代内量子数分配与质量层级、色禁闭与质量间隙（千禧年问题）、胶子动力学、全阶重整化、统一尺度的几何指定。


---

## 【r189 口径归一化勘误｜2026-10-25】

> 审计侧附加标注；**正文原始数字一字未改**（不静默改写）。
> 依据：`04_公共成果/本项目_全维自洽与归一化/判定/判定_TUFT-r189_S13口径归一化修复与归属审计_2026-10-25.md`。

- P1｜§四 参数系统 `v = \ell^{-1}` 的 ℓ 是**电弱长度** `ℓ_EW = ħc/v = 7.7305e-19 m`（由 PDG v 反解），不是 Planck 长度 `ℓ_P = 1.616255e-35 m`（两者相差 4.78e16 倍）。M5 的「最短尺度 ℓ」应另记为 `ℓ_sd`（自对偶尺度），其数值无框架输出 ⇒ OPEN。`v ↔ ℓ_EW` 是自然单位互锁，**不构成对 ℓ_P 的推导**。


---

## 【r195 尺度秩不变性与归一化条件名实勘误｜2026-10-25】

> 审计侧附加标注；**正文/原记录一字未改**（只追加，不静默改写）。
> 依据：`04_公共成果/本项目_全维自洽与归一化/数据/判定_TUFT-r195_尺度秩不变性定理_M5尺度简并与归一化条件名实审计_精算_2026-10-25.md`。

- P1｜§四 参数系统 + M5：对偶镜像条件 g^eff(r)=g^eff(ℓ²/r) 的解析族 g_ℓ(r)=1−r_s r/(r²+ℓ²) 对**任意** ℓ 恒成立（有理精确残差 0）⇒ M5 只固定**形状**、不固定 ℓ 的数值（一参数族，归一化秩 0）。`dimension_unify_verify.py` 验证 E 的 `ĥ†ĥ=1` 是**无量纲单位化**，`g^eff` 残差是**形状检查**（L=0.5 与 L=5.0 双通过），该文件自述「参数(1个标度+2无量纲)」⇒ 所谓「归一化条件」不是尺度设定方程（F-label/F-rank）。
