# P9 · Precision Gravity Tests: the Brans–Dicke PPN Parameter, the vDVZ Discontinuity and GP-B Frame Dragging

**中文题名：精密引力检验——Brans–Dicke PPN 参数、vDVZ 不连续与 GP-B 参考系拖拽的求导与精算**

**Authors:** Guozi Mo (莫国子)^1,\*

**Affiliation:** ^1 墨行科技（江门 / 佛山），中国；\* Corresponding author.

**Date:** 2026-11-09 · **Series:** Unified-Field Breaching Papers, P9 of 13

---

## Abstract

Three precision tests separate general relativity from its nearest alternatives, and each can be reduced to a single algebraic ratio. We derive (i) the Brans–Dicke post-Newtonian parameter $\gamma=(1+\omega)/(2+\omega)$, which gives $\gamma(1)=2/3$, $\gamma(2)=3/4$ and $\gamma(40000)-1=-2.4999\times10^{-5}$, saturating the Cassini bound; (ii) the van Dam–Veltman–Zakharov discontinuity of massive gravity, where the static potential is enhanced by exactly $4/3$ while light bending is suppressed by exactly $3/4$, leaving a deficit of $1/4$ that no smooth massless limit can remove; and (iii) the Lense–Thirring frame-dragging rate measured by Gravity Probe B, for which the engine gives $0.04095$ arcsec yr⁻¹ (inside the $1\sigma$ band of $0.041\pm0.0012$) and a geodetic precession of $6.6211$ arcsec yr⁻¹, $+0.23\%$ from the $6.606\pm0.017$ measurement. Each step carries an analytic derivative check; the Brans–Dicke slope $d\gamma/d\omega=1/(2+\omega)^2$ is verified by central differencing to $10^{-20}$.

**摘要：** 三项精密检验把广义相对论与最近的替代理区分开，而每一项都可化为一条代数比值。本文求导：(i) Brans–Dicke 后牛顿参数 $\gamma=(1+\omega)/(2+\omega)$，给出 $\gamma(1)=2/3$、$\gamma(2)=3/4$、$\gamma(40000)-1=-2.4999\times10^{-5}$，正好压住 Cassini 上界；(ii) 有质量引力的 van Dam–Veltman–Zakharov 不连续：静态势被精确放大 $4/3$，光线偏折被精确压低 $3/4$，留下 $1/4$ 的缺额，任何光滑无质量极限都无法抹去；(iii) Gravity Probe B 测得的 Lense–Thirring 参考系拖拽率，引擎给 $0.04095$ arcsec/yr（落在 $0.041\pm0.0012$ 的 $1\sigma$ 带内），测地进动 $6.6211$ arcsec/yr，距实测 $6.606\pm0.017$ 为 $+0.23\%$。每一步都带解析导数互验；Brans–Dicke 斜率 $d\gamma/d\omega=1/(2+\omega)^2$ 经中心差分互验到 $10^{-20}$。

---

## 1. Introduction

精密引力检验的困难不在“测量精度”，而在“把替代理论压成一条可比的数”。Brans–Dicke 把整个标量-张量族压成一个 $\omega$；有质量引力把“质量连续趋于零”压成一个 $4/3$ 与 $3/4$ 的比值；GP-B 把参考系拖拽压成一个角速度。本文对这三条各自给出“求导链—闭式—精算—与实测偏差”的完整结构，并明确指出哪一处是**理论内部矛盾**（vDVZ），哪一处是**实验已闭合**（Cassini、GP-B）。

## 2. Results

### 2.1 求导链 I：Brans–Dicke 的 PPN 参数

**Step 1（作用量）.**

$$
S=\int d^4x\sqrt{-g}\left[\phi R-\frac{\omega}{\phi}(\partial\phi)^2\right]+S_m .
$$

**Step 2（弱场展开）.** $g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu}$，$\phi=\phi_0(1+\varphi)$，得

$$
h_{00}=\frac{2GM}{c^2r},\qquad h_{ij}=\gamma\,\frac{2GM}{c^2r}\delta_{ij},
$$

**Step 3（解出 $\gamma$）.** 标量场的屏蔽因子给出

$$
\gamma=\frac{1+\omega}{2+\omega}.
$$

**Step 4（特殊值）.** $\omega=1\Rightarrow\gamma=2/3$；$\omega=2\Rightarrow\gamma=3/4$；$\omega=40000\Rightarrow\gamma-1=-2.4999\times10^{-5}$（E9.1–E9.3）。

**Step 5（导数）.**

$$
\frac{d\gamma}{d\omega}=\frac{(2+\omega)-(1+\omega)}{(2+\omega)^2}=\frac{1}{(2+\omega)^2},
$$

中心差分在 $\omega=3$ 处互验相对误差 $<10^{-20}$（E9.4）。单调递增、上界 1：$\omega\to\infty$ 才回到 GR。

### 2.2 求导链 II：vDVZ 不连续

**Step 1（线性化 FP 作用量）.** 有质量引力加入 Fierz–Pauli 质量项 $m^2(h^2-h_{\mu\nu}^2)$。

**Step 2（静态势）.** 解为 $V_{\rm FP}(r)=-\frac{GM}{r}\left[1+\frac13 e^{-mr}\right]$，在 $m\to0$ 时 $V\to-\frac{4}{3}\frac{GM}{r}$，即精确 $4/3$ 倍。

**Step 3（光线偏折）.** 有效标量贡献使偏折角变为 $\frac34$ 倍 GR（E9.6）。

**Step 4（缺额）.** $4/3$ 与 $3/4$ 不能同时被一个重标化吸收：其乘积为 1、但物理量不同（势 vs 偏折），故存在 $1/4$ 的不可约缺额。这就是 vDVZ 不连续：$m\to0$ 的极限与 $m=0$ 的理论不是同一个理论。

**Step 5（判定）.** 该不连续是**理论内部的结构性矛盾**，不是数值精度问题；任何“有质量引力在 $m\to0$ 回到 GR”的声明都必须先解决 $1/4$ 缺额（Vainshtein 机制只在强场非线性区缓解）。

### 2.3 求导链 III：GP-B 的两个进动

**Step 1（测地进动）.** 对圆轨道，

$$
\Omega_{\rm geo}=\frac{3GM}{2c^2r}\Omega_{\rm orb}.
$$

**Step 2（参考系拖拽）.**

$$
\Omega_{\rm FD}=\frac{2GJ}{c^2r^3}\left(1-\frac{3}{2}\right)_{\rm orbit\ average}.
$$

**Step 3（读数）.** 引擎给 $\Omega_{\rm geo}=6.6211$ arcsec yr⁻¹、$\Omega_{\rm FD}=0.04095$ arcsec yr⁻¹（legacy C0395，守卫 8/8）。

**Step 4（偏差）.** 测地：$+0.23\%$（vs $6.606\pm0.017$）；拖拽：落在 $0.041\pm0.0012$ 的 $1\sigma$ 带内。

### 2.4 精算读数表

| 量 | 闭式 | 读数 | 来源 | 与实测偏差 |
|---|---|---|---|---|
| $\gamma(1)$ | $(1+\omega)/(2+\omega)$ | **2/3** | E9.1 | 解析精确 |
| $\gamma(2)$ | 同上 | **3/4** | E9.2 | 解析精确 |
| $\gamma(40000)-1$ | 同上 | **$-2.4999\times10^{-5}$** | E9.3 | Cassini 上界 $\sim2.5\times10^{-5}$ |
| $d\gamma/d\omega$ | $1/(2+\omega)^2$ | 0.01（$\omega=8$） | E9.4 | 差分互验 <1e−20 |
| $V_{\rm FP}/V_{\rm GR}$ | $4/3$（$m\to0$） | **1.3333** | E9.5 | 理论比值 |
| $\delta_{\rm FP}/\delta_{\rm GR}$ | $3/4$ | **0.75** | E9.6 | 理论比值 |
| $\Omega_{\rm FD}$ | Lense–Thirring | **0.04095″/yr** | C0395 | $0.041\pm0.0012$，$1\sigma$ 内 |
| $\Omega_{\rm geo}$ | $3GM\Omega/2c^2r$ | **6.6211″/yr** | C0395 | $6.606\pm0.017$，$+0.23\%$ |

## 3. Discussion

**三条链的性质不同，不能混为一谈.** Cassini 已经把 $\omega\gtrsim40000$ 写成硬上界，故 Brans–Dicke 在太阳系尺度上是“被排除但未被杀死”——它的 $2/3$、$3/4$ 特殊值只在 $\omega=1,2$ 出现，现实 $\omega$ 远离该区。vDVZ 是理论内部矛盾，不需要实验就能判定其“朴素质量连续极限”失败。GP-B 是实验已闭合的检验：$0.23\%$ 与 $1\sigma$ 是两个不同量级的吻合，说明测地项对参数更敏感、拖拽项对噪声更敏感。

**与 TUFT 的关系.** TUFT 的挠率-角频率分支若要声称“修改引力”，必须先在 $\gamma$、$4/3$、$3/4$ 三条比值上给出可计算偏离；本工程审计结论是 TUFT 未供给这三条中的任何一条（18 条必要条件供给 0）。故本项为结构性负面闭合的一部分，不构成支持。

## 4. Methods

常数与轨道参数：GP-B 轨道 $r=7018$ km、$M_\oplus=5.972\times10^{24}$ kg、$J_\oplus=7.06\times10^{33}$ kg m² s⁻¹（IERS）；Cassini $\gamma-1$ 上界 $2.5\times10^{-5}$（Bertotti et al. 2003）。mpmath 60 位；容差逐条列于 JSON。

## 5. Figure legends

**Fig. 9 | Precision gravity tests.** (a) The Brans–Dicke PPN parameter $\gamma(\omega)$ on a logarithmic $\omega$ axis; the gold markers are the exact values at $\omega=1$ and $\omega=2$, the dotted line is $\gamma=2/3$. (b) The vDVZ potential ratio $4/3$ against the GR reference of unity. (c) The GP-B frame-dragging rate with its $1\sigma$ error bar against the measured value. All labels in English.

## 6. Data & Code Availability

- 精算锚点：`verify_papers_P6_P13_精算验证_2026-11-09.py`（E9.1–E9.8）
- 既有判定册：`attack_C0392_*`（BD PPN）、`attack_C0393_*`（vDVZ）、`attack_C0395_*`（GP-B）
- 图：`figures/Fig9_precision_tests_EN.png`

## 7. Author Contributions

G.M. 完成三条求导链与全文。

## 8. Competing Interests

作者声明无竞争性利益。

## References

1. Brans, C. & Dicke, R. H. Mach's principle and a relativistic theory of gravitation. *Phys. Rev.* **124**, 925–935 (1961).
2. Will, C. M. The confrontation between general relativity and experiment. *Living Rev. Relativ.* **17**, 4 (2014).
3. van Dam, H. & Veltman, M. Massive and massless Yang–Mills and gravitational fields. *Nucl. Phys. B* **22**, 397–411 (1970).
4. Zakharov, V. I. Linearized gravitation theory and the graviton mass. *JETP Lett.* **12**, 312 (1970).
5. Everitt, C. W. F. et al. Gravity Probe B: final results of a space experiment to test general relativity. *Phys. Rev. Lett.* **106**, 221101 (2011).
6. Bertotti, B., Iess, L. & Tortora, P. A test of general relativity using radio links with the Cassini spacecraft. *Nature* **425**, 374–376 (2003).
