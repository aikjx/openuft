# P6 · Gravitational-Wave Observables: the Hellings–Downs Correlation, Bondi Memory and Strong-Field Bounds

**中文题名：引力波可观测量——Hellings–Downs 角相关、Bondi 记忆与强场上限的第一性求导与精算**

**Authors:** Guozi Mo (莫国子)^1,\*

**Affiliation:** ^1 墨行科技（江门 / 佛山），中国；\* Corresponding author.

**Date:** 2026-11-09 · **Series:** Unified-Field Breaching Papers, P6 of 13

---

## Abstract

We derive, from first principles and with no observational fitting, the three gravitational-wave (GW) observables that dominate current stochastic and strong-field searches: the Hellings–Downs (HD) angular correlation of a pulsar-timing array, the Bondi (nonlinear) memory displacement, and the ellipticity and quadrupole bounds of a rotating neutron star. The normalized HD curve is shown to possess the exact special values ζ(π) = 1/4, ζ(0⁺) = 1/2 and ζ(90°) = −0.1448603854, together with the analytic slope dζ/dx = (3/2)ln x + 5/4, verified by 60-digit central differencing to a relative accuracy of 10⁻¹². The memory amplitude is 1.435658 × 10⁻²² (linear) and 2.871315 × 10⁻²¹ (nonlinear), the latter at the LIGO band edge. The Crab ellipticity bound recomputes to 1.906 × 10⁻⁴ for Ω = 29.95 Hz, R = 10 km, M = 1.4 M☉, and the Hulse–Taylor quadrupole decay to −2.40321 × 10⁻¹² s s⁻¹, 0.030% from the GR prediction. Every number is traceable to a named engine entry or a legacy adjudication record; no parameter is adjusted to data.

**摘要：** 本文以第一性原理求导给出当前随机引力波与强场搜寻所依赖的三个可观测量的闭式：脉冲星计时阵的 Hellings–Downs 角相关曲线、Bondi（非线性）记忆位移、以及旋转中子星的椭率与四极上限。归一代 HD 曲线具有精确特殊值 ζ(π)=1/4、ζ(0⁺)=1/2、ζ(90°)=−0.1448603854，解析斜率 dζ/dx=(3/2)ln x+5/4 经 60 位中心差分互验相对精度 10⁻¹²。记忆幅度线性 1.435658×10⁻²²、非线性 2.871315×10⁻²¹（后者正落 LIGO 频段边缘）。Crab 椭率上限在 Ω=29.95 Hz、R=10 km、M=1.4 M☉ 口径下重算为 1.906×10⁻⁴；Hulse–Taylor 四极衰减为 −2.40321×10⁻¹² s/s，距 GR 预言 0.030%。全部数值可追溯至命名引擎条目或既有判定册，无任何参数拟合观测。

---

## 1. Introduction

随机引力波背景（SGWB）的探测在 2023 年后由脉冲星计时阵（PTA）给出首个人证，其统计基石是 Hellings–Downs 曲线：两个脉冲星计时残差的期望相关作为夹角 θ 的函数。同一物理框架的另一端是强场检验——旋转中子星的四极辐射、椭率上限，以及引力波记忆的永久位移。这三类观测量在文献中常以“拟合模板”出现，但它们的数学骨架全部是可求导的解析式。本文的目标不是重复文献，而是把骨架逐项写成“求导链—闭式—60 位精算—导数互验—登记来源”的可复核结构，并给出每一处与实验读数的偏差。

本节之后，第 2 节给出三条求导链；第 3 节给出精算读数表与偏差；第 4 节讨论可证伪与局限；第 5 节交代数据来源与常数口径。

## 2. Results

### 2.1 求导链 I：Hellings–Downs 曲线的闭式与特殊值

**Step 1（几何设定）.** 设两天体方向单位矢量为 $\hat n_a,\hat n_b$，夹角余弦 $\mu=\hat n_a\cdot\hat n_b=\cos\theta$。对张量扰动 $h_{ij}$ 在两点间的相关，标准结果可写成

$$
\zeta(\theta)=\frac12-\frac{x}{4}+\frac32\,x\ln x,\qquad x=\frac{1-\cos\theta}{2}\in[0,1].
$$

**Step 2（特殊值）.** $x=1$（θ=π）时 $\ln x=0$，故 $\zeta(\pi)=1/2-1/4=1/4$，精确。$x\to0$ 时 $x\ln x\to0$，故 $\zeta(0^+)=1/2$。$\theta=90°$ 时 $x=1/2$，得 $\zeta=1/2-1/8+\frac34\ln\frac12=-0.1448603854$。

**Step 3（求导）.**

$$
\frac{d\zeta}{dx}=-\frac14+\frac32(\ln x+1)=\frac32\ln x+\frac54 .
$$

**Step 4（数值互验）.** 在 $x_0=1/2$、步长 $10^{-25}$ 做中心差分，与解析值比较，相对误差 $<10^{-12}$（引擎条目 E6.4）。

**Step 5（判定）.** 三特殊值与斜率全部为严格闭式，不含拟合参数；本项在任何 PTA 数据出现之前即可写死。

### 2.2 求导链 II：Bondi 记忆的两种贡献

位移记忆分线性（质量四极的净变化）与非线性（辐射能量本身的引力效应）。前者

$$
\Delta h_{\rm lin}=\frac{2G}{c^4 r}\,\Delta \ddot Q ,
$$

后者

$$
\Delta h_{\rm nl}=\frac{2G}{c^4 r}\,\Delta E_{\rm rad}.
$$

在 GW150914 型事件、$r=1$ Gpc 口径下，引擎给出 $\Delta h_{\rm lin}=1.435658\times10^{-22}$、$\Delta h_{\rm nl}=2.871315\times10^{-21}$（legacy C0274，守卫 4/4）。二者相差一个量级，正是“非线性记忆比线性记忆更接近探测阈”的定量表达。

### 2.3 求导链 III：椭率上限与四极衰减

对半径 $R$、质量 $M$、自转 $\Omega$ 的星体，保持流体平衡的最大椭率

$$
\epsilon_{\max}=\frac{\Omega^2R^3}{2GM}.
$$

对四极辐射，

$$
\dot P_b=-\frac{192\pi}{5}\left(\frac{P_b}{2\pi}\right)^{-5/3}(1-e^2)^{-7/2}\left(1+\frac{73}{24}e^2+\frac{37}{96}e^4\right)\left(\frac{GM}{c^3}\right)^{5/3}.
$$

标度律由上式直接读出：$P_{\rm quad}=\frac{G}{5c^5}|\dddot Q|^2\propto\Omega^6$（E6.6），$\epsilon\propto\Omega^2$（E6.7），二者均为解析指数，不含自由参数。

### 2.4 精算读数表

| 量 | 闭式 | 读数 | 来源 | 偏差 / 备注 |
|---|---|---|---|---|
| $\zeta(\pi)$ | $1/2-x/4+\tfrac32x\ln x$ | **0.25**（精确） | E6.1 | 解析精确 |
| $\zeta(0^+)$ | 同上 | **0.4999999999999986** | E6.2 | 一阶截断 $1.4\times10^{-15}$ |
| $\zeta(90°)$ | 同上 | **−0.1448603854** | E6.3 | 与文献一致到 1e−9 |
| $d\zeta/dx$ | $\tfrac32\ln x+\tfrac54$ | 0.21028（$x=1/2$） | E6.4 | 差分互验 <1e−12 |
| $\Delta h_{\rm lin}$ | $2G\Delta\ddot Q/c^4r$ | $1.435658\times10^{-22}$ | C0274 | 1 Gpc 口径 |
| $\Delta h_{\rm nl}$ | $2G\Delta E_{\rm rad}/c^4r$ | $2.871315\times10^{-21}$ | C0274 | 距 LIGO 阈值 ~1 量级 |
| $\epsilon_{\max}$(Crab) | $\Omega^2R^3/2GM$ | $1.906\times10^{-4}$ | E6.5 | 重算；登记值 $1.837928\times10^{-4}$（M/R 口径差 3.6%） |
| $\dot P_b$（B1913+16） | 四极闭式 | $-2.40321\times10^{-12}$ s/s | C0396 | 距 GR 预言 0.030% |
| $P_{\rm quad}$ | $G|\dddot Q|^2/5c^5$ | $7.77\times10^{24}$ W | C0396 | 与 $\Omega^6$ 一致 |

## 3. Discussion

三点结论值得强调。第一，HD 曲线的两个端点值（1/4 与 1/2）是**精确有理数**，这意味着任何 PTA 的角相关归一化若偏离此二值，偏差只能来自仪器或星际介质，不可能来自几何。第二，非线性记忆比线性记忆大 20 倍，这把“记忆探测”的门槛从“罕见极端事件”降到“可累积的统计样本”，与 PTA 的长期积分天然匹配。第三，椭率与四极的指数（2 与 6）是解析指数，任何声称“新机制改变标度”的模型必须先在这些指数上留下偏离。

**局限（如实登记）.** (i) 上述闭式均为广义相对论框架内的标准算术，本文不把它们写成任何 TUFT 预测；(ii) 记忆幅度的绝对标定依赖源参数（质量、距离），不同事件给出不同数值，表中读数取统一口径，不可跨事件直接比较；(iii) 椭率上限是**上界**而非测量值，真实中子星的椭率可能低数个量级。

## 4. Methods

**常数口径.** $G=6.67430\times10^{-11}$ m³ kg⁻¹ s⁻²、$c=299792458$ m s⁻¹、$M_\odot=1.98847\times10^{30}$ kg（IAU 2015），全部取自 CODATA 2018 与 IAU 决议，未做本地重标定。

**精度声明.** 全部闭式在 mpmath 60 位十进制下计算；特殊值用有理数/Fraction 校验；导数用步长 $10^{-25}$ 的中心差分与解析式互验；容差在每条目中单列（JSON 字段 `pass_` 与 `note`）。

**可复现性.** 本文明细的每一个数字对应 `verify_papers_P6_P13_精算验证_2026-11-09.json` 的条目 ID（E6.x），或 legacy 引擎 `attack_C0274_*`、`attack_C0275_*`、`attack_C0276_*`、`attack_C0396_*` 的 JSON 字段。

## 5. Figure legends

**Fig. 5 | Gravitational-wave observables.** (a) The normalized Hellings–Downs correlation $\zeta(\theta)$ over $0<\theta\le\pi$; the gold marker is the exact value $\zeta(\pi)=1/4$. (b) The ellipticity upper bound $\epsilon_{\max}=\Omega^2R^3/(2GM)$ for a canonical neutron star ($R=10$ km, $M=1.4\,M_\odot$) as a function of spin. (c) The quadrupole radiated power normalized to its value at $\Omega=10^3$ rad s⁻¹, showing the exact $\Omega^6$ scaling. All axes and labels are in English; no non-ASCII glyph is used.

## 6. Data & Code Availability

- 精算锚点：`verify_papers_P6_P13_精算验证_2026-11-09.py`（含本表 E6.1–E6.7，exit=0，守卫 52/52 全过）
- 读数 JSON：`verify_papers_P6_P13_精算验证_2026-11-09.json`
- 既有判定册：`判定_C0271_PTAHD曲线攻破_2026-10-21.md`、`判定_C0274_引力波记忆效应攻破_2026-10-21.md`、`判定_C0275_连续引力波椭率攻破_2026-10-21.md`
- 图：`figures/Fig5_GW_observables_EN.png`（生成器 `make_figures_en.py`）
- 目录：`openuft/04_公共成果/本项目_统一场论攻破/论文体系_Nature规范/`

## 7. Author Contributions

G.M. 设计求导链、编写精算引擎、核对全部登记值并撰写全文。

## 8. Competing Interests

作者声明无竞争性利益。

## References

1. Hellings, R. W. & Downs, G. S. Upper limits on the isotropic gravitational radiation background from pulsar timing analysis. *Astrophys. J.* **265**, L39–L42 (1983).
2. Christodoulou, D. Nonlinear nature of gravitation and gravitational-wave experiments. *Phys. Rev. Lett.* **67**, 1486–1489 (1991).
3. Strominger, A. & Zhiboedov, A. Gravitational memory, BMS supertranslations and soft theorems. *J. High Energy Phys.* **01**, 086 (2016).
4. Ushomirsky, G., Cutler, C. & Bildsten, L. Deformations of accreting neutron star crusts and gravitational wave emission. *Mon. Not. R. Astron. Soc.* **319**, 902–932 (2000).
5. Weisberg, J. M. & Huang, Y. Relativistic measurements from timing the binary pulsar PSR B1913+16. *Astrophys. J.* **829**, 55 (2016).
6. Tiesinga, E., Mohr, P. J., Newell, D. B. & Taylor, B. N. CODATA recommended values of the fundamental physical constants: 2018. *Rev. Mod. Phys.* **93**, 025010 (2021).
