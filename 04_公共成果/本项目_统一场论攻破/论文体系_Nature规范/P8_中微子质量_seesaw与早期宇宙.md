# P8 · Neutrino Mass, the Type-I Seesaw and Early-Universe Constraints: A Derivation-First Audit

**中文题名：中微子质量、I 型跷跷板与早期宇宙约束——先求导后读数的审计**

**Authors:** Guozi Mo (莫国子)^1,\*

**Affiliation:** ^1 墨行科技（江门 / 佛山），中国；\* Corresponding author.

**Date:** 2026-11-09 · **Series:** Unified-Field Breaching Papers, P8 of 13

---

## Abstract

The type-I seesaw converts a right-handed neutrino mass $M_R$ into a light neutrino mass $m_\nu$ through a single algebraic identity, $m_\nu=y_N^2v^2/(2M_R)$. We derive this identity, fix its scaling exponents analytically, and recompute the mass scale: with $y_N=\sqrt2$, $v=246.22$ GeV and $m_\nu=0.05$ eV, $M_R=1.2125\times10^{15}$ GeV, within 0.5% of the registered adjudication value. We then audit two early-universe anchors: the Big Bang nucleosynthesis helium abundance, $Y_p(0.8\,\mathrm{MeV})=0.2785$ with freeze-out $T_f^*=0.7331$ MeV reproducing $Y_p=0.245$, and the neutron-decay suppression factor $\exp(-180/879.4)=0.8149$; and the freeze-in relic density, which scales exactly as $y^2$ and reproduces $\Omega h^2=0.12$ at $y^*=2.8846\times10^{-11}$. Two honest caveats are recorded: the freeze-in coupling differs from the conventional literature estimate by an order of magnitude and this deviation is logged rather than hidden, and the Kaup boson-star mass quoted in the legacy record has been corrected for a unit error ($m=10^{-5}$ eV gives $1.682\times10^{25}$ kg, not $1.68\times10^{20}$ kg).

**摘要：** I 型跷跷板通过一条代数恒等式把右手中微子质量 $M_R$ 与轻中微子质量 $m_\nu$ 相连：$m_\nu=y_N^2v^2/(2M_R)$。本文给出该恒等式的完整求导与解析标度指数，并重算质量标度：取 $y_N=\sqrt2$、$v=246.22$ GeV、$m_\nu=0.05$ eV，得 $M_R=1.2125\times10^{15}$ GeV，与既有判定登记值相差 0.5% 以内。随后审计两个早期宇宙锚点：大爆炸核合成氦丰度 $Y_p(0.8\,\mathrm{MeV})=0.2785$、冻结温度 $T_f^*=0.7331$ MeV 复现 $Y_p=0.245$，中子衰变抑制因子 $\exp(-180/879.4)=0.8149$；以及 freeze-in 遗迹密度，其严格按 $y^2$ 标度、在 $y^*=2.8846\times10^{-11}$ 处复现 $\Omega h^2=0.12$。两处诚实留痕：freeze-in 耦合与常规文献估计差一个量级，已登记而非隐去；legacy 记录中 Kaup 玻色子星质量存在单位错误，已校正为 $m=10^{-5}$ eV 对应 $1.682\times10^{25}$ kg（原记 $1.68\times10^{20}$ kg 系 $m=1$ eV 参考点）。

---

## 1. Introduction

中微子质量是标准模型唯一需要“新物理”才能解释的自由参数。I 型跷跷板的优点是它只加一个右手单态，把质量生成化为一条两行代数；缺点是它把新物理能标推到 $10^{15}$ GeV，远超对撞机。因此对它的检验只能来自三个方向：轻中微子质量的绝对标度、早期宇宙的丰度、以及新粒子衰变/产生的遗迹丰度。本文把这三条链分别写成可复核的求导结构，并明确标出哪一步是“唯一确定”、哪一步是“口径依赖”。

## 2. Results

### 2.1 求导链 I：跷跷板恒等式与标度指数

**Step 1（拉氏量）.** $\mathcal L\supset -y_N\,\overline{N_R^c}\,L\,\Phi-\tfrac12M_R\,\overline{N_R^c}N_R+h.c.$

**Step 2（对称破缺）.** $\Phi\to (0,v/\sqrt2)^T$，狄拉克质量 $m_D=y_Nv/\sqrt2$。

**Step 3（对角化）.** 质量矩阵

$$
\mathcal M=\begin{pmatrix}0&m_D\\ m_D&M_R\end{pmatrix}
$$

的本征值在 $M_R\gg m_D$ 下为 $m_\nu\simeq m_D^2/M_R$，即

$$
m_\nu=\frac{y_N^2v^2}{2M_R}.
$$

**Step 4（反解能标）.** $M_R=y_N^2v^2/(2m_\nu)$。取 $y_N=\sqrt2$、$v=246.22$ GeV、$m_\nu=5\times10^{-11}$ GeV：

$$
M_R=\frac{2\times(246.22)^2}{2\times5\times10^{-11}}=1.2125\times10^{15}\ \mathrm{GeV}.
$$

**Step 5（标度）.** $d\ln M_R/d\ln m_\nu=-1$（E8.2）：中微子质量每降一个量级，跷跷板能标升一个量级。这是本项唯一的“硬”关系。

### 2.2 求导链 II：核合成氦丰度

**Step 1（冻结）.** 弱相互作用率 $\Gamma_W\sim G_F^2T^5$ 与膨胀率 $H\sim T^2/M_{\rm Pl}$ 相等时冻结，$T_f\simeq0.8$ MeV。

**Step 2（中子衰变抑制）.** 从冻结到核合成的时间窗内，中子按 $e^{-t/\tau_n}$ 衰变，$\tau_n=879.4$ s；取 $t=180$ s，

$$
\mathcal S=e^{-180/879.4}=0.8149 .
$$

**Step 3（丰度）.** $Y_p\approx\frac{2(n/p)}{1+n/p}$，$n/p\propto\mathcal S\,e^{-Q/T_f}$，$Q=1.293$ MeV。

**Step 4（读数）.** 引擎给 $Y_p(0.8\,\mathrm{MeV})=0.2785$；反解复现 $Y_p=0.245$ 的冻结温度为 $T_f^*=0.7331$ MeV（legacy C0399，守卫 9/9）。

**Step 5（导数符号）.** $dY_p/dT_f>0$、$dY_p/d\tau_n>0$、$dY_p/dQ<0$，三符号全部由引擎互验。

### 2.3 求导链 III：freeze-in 遗迹丰度

**Step 1（产生）.** 暗 sector 粒子通过与 SM 的微小耦合 $y$ 产生，产生率 $\propto y^2T$。

**Step 2（玻尔兹曼）.** $\dot Y=(\text{产生})-(\text{湮灭})$；在 freeze-in 区湮灭可忽略。

**Step 3（标度）.** $\Omega h^2\propto y^2$（E8.6），故在 $\Omega h^2=0.12$ 处反解 $y^*=2.8846\times10^{-11}$（legacy C0397，守卫 8/8）。

**Step 4（留痕）.** 该 $y^*$ 与常规文献的 $10^{-12}$ 量级估计相差约一个量级；差异已写入引擎 `note` 与判定册，未做隐藏或重标定。

### 2.4 精算读数表

| 量 | 闭式 | 读数 | 来源 | 备注 |
|---|---|---|---|---|
| $M_R$ | $y_N^2v^2/2m_\nu$ | **$1.2125\times10^{15}$ GeV** | E8.1 | 登记值 $1.21249\times10^{15}$ |
| $d\ln M_R/d\ln m_\nu$ | 解析 | **−1** | E8.2 | 硬关系 |
| 抑制因子 | $e^{-180/879.4}$ | **0.8149** | E8.3 | $\tau_n=879.4$ s |
| $Y_p(0.8\,\mathrm{MeV})$ | 冻结+衰变 | **0.2785** | C0399 | 守卫 9/9 |
| $T_f^*(Y_p=0.245)$ | 反解 | **0.7331 MeV** | C0399 | — |
| $y^*$ | $\Omega h^2\propto y^2$ | **$2.8846\times10^{-11}$** | C0397 | 与文献差 ~1 量级，已留痕 |
| $M_{\rm Kaup}(10^{-5}\,\mathrm{eV})$ | Kaup 闭式 | **$1.682\times10^{25}$ kg** | C0398 | 已校正单位错误；$\approx8.4568\times10^{-6}M_\odot$ |

## 3. Discussion

跷跷板恒等式的价值在于“可反解”：给定任一轻中微子质量与任一 $y_N$，$M_R$ 唯一确定。这使得它成为检验“新物理能标”的最廉价工具——不需要对撞机。核合成链条的价值在于“可反查”：$Y_p$ 与 $T_f$ 是一一映射，任何声称改变弱相互作用强度的模型都必须先解释 $0.2785$ 与 $0.245$ 之间的差。freeze-in 的价值在于“可定标”：$y^*$ 与 $\Omega h^2$ 的平方关系使耦合的微小变化被放大，因而对暗 sector 参数极敏感。

**诚实登记.** C0397 的 $y^*$ 与文献差一个量级，本文不把它写成“预言”，只写成“在本引擎口径下的反解值”；C0398 的 Kaup 质量单位错误已在引擎 JSON 与判定册中留下修正记录，本文按校正值引用。

## 4. Methods

常数：$G_F=1.1663787\times10^{-5}$ GeV⁻²、$\tau_n=879.4$ s、$Q=1.293$ MeV、$v=246.22$ GeV（CODATA/PDG 2020）。精度 mpmath 60 位；容差逐条列于 JSON。

## 5. Figure legends

**Fig. 8 | Early-universe constraints.** (a) Helium mass fraction $Y_p$ versus freeze-out temperature $T_f$; the two gold markers are the engine anchors $(0.8\,\mathrm{MeV},0.2785)$ and $(0.7331\,\mathrm{MeV},0.245)$. (b) Freeze-in relic density $\Omega h^2$ versus coupling $y$ on log–log axes, showing the exact $y^2$ scaling and the solution $y^*=2.8846\times10^{-11}$ at $\Omega h^2=0.12$.

## 6. Data & Code Availability

- 精算锚点：`verify_papers_P6_P13_精算验证_2026-11-09.py`（E8.1–E8.7）
- 既有判定册 / 引擎：`attack_C0397_*`（freeze-in）、`attack_C0398_*`（Kaup）、`attack_C0399_*`（BBN）
- 图：`figures/Fig8_neutrino_BBN_EN.png`

## 7. Author Contributions

G.M. 完成三条求导链、单位错误复核与全文。

## 8. Competing Interests

作者声明无竞争性利益。

## References

1. Minkowski, P. μ→eγ at a rate of one out of 10⁹ muon decays? *Phys. Lett. B* **67**, 421–428 (1977).
2. Yanagida, T. Horizontal gauge symmetry and masses of neutrinos. *Conf. Proc. C* **7902131**, 95–99 (1979).
3. Mohapatra, R. N. & Pati, J. C. Seesaw scale and CP violation. *Phys. Rev. D* **54**, 5835 (1996).
4. Fields, B. D. et al. The cosmological standard model. *Nucl. Phys. A* **1011**, 1–74 (2020).
5. Hall, L. J., Jedamzik, K., March-Russell, J. & West, S. M. Freeze-in production of FIMP dark matter. *J. High Energy Phys.* **03**, 080 (2010).
6. Kaup, D. J. Klein–Gordon geons. *Phys. Rev.* **172**, 1331–1342 (1968).
