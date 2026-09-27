# 延伸方向 C｜弱场近似：爱因斯坦场方程 \(\to\) 牛顿泊松方程 \(\nabla^2\Phi=4\pi G\rho\)

> 全程严格区分 **数学定义 / 量纲分析 / 本体论解释**；SI 单位制；签名 \((+,-,-,-)\)。
> 本文全部结论由 `verify_extension_derivation.py` 的 **C 组**符号求导 + 高精度复算（见文末 C.10）。
> **红线**：本文是**框架内的自洽推导验证**，不构成对广义相对论的任何修正或新预言。

---

## C.0 弱场展开与记号

**假设（前提，非结论）**：存在坐标系使得

\[
g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu},\qquad |h_{\mu\nu}|\ll1
\]

且 \(h_{\mu\nu}\) 及其导数的一阶项保留、二阶及以上丢弃。指标用 \(\eta\) 升降（一阶精度）。

定义**迹反转扰动**：

\[
\bar h_{\mu\nu}\equiv h_{\mu\nu}-\frac12\eta_{\mu\nu}h,\qquad
h\equiv\eta^{\alpha\beta}h_{\alpha\beta}
\]

（注意 \(\bar h\) 的迹 \(\bar h=-h\)，故该变换是对合的：\(\bar{\bar h}_{\mu\nu}=h_{\mu\nu}\)。）

---

## C.1 迹反转形式：从 \(G_{\mu\nu}\) 到 \(R_{\mu\nu}\)

场方程（任务 1）：

\[
G_{\mu\nu}=R_{\mu\nu}-\frac12g_{\mu\nu}R=\kappa T_{\mu\nu},\qquad
\kappa\equiv\frac{8\pi G}{c^4}
\]

**取迹**（乘 \(g^{\mu\nu}\)，4 维中 \(g^{\mu\nu}g_{\mu\nu}=4\)）：

\[
R-2R=\kappa T\;\Longrightarrow\;R=-\kappa T
\]

**代回**：

\[
\boxed{R_{\mu\nu}=\kappa\Big(T_{\mu\nu}-\frac12g_{\mu\nu}T\Big)}
\]

（脚本 C1 用符号代数验证：PASS。）

**量纲核验**：\([\kappa]=\frac{[G]}{[c^4]}=\frac{\mathrm{M}^{-1}\mathrm{L}^3\mathrm{T}^{-2}}{\mathrm{L}^4\mathrm{T}^{-4}}
=\mathrm{M}^{-1}\mathrm{L}^{-1}\mathrm{T}^{2}\)；\([T_{\mu\nu}]\)（能量动量张量，\(\mathrm{J/m^3}=\mathrm{M}\,\mathrm{L}^{-1}\mathrm{T}^{-2}\)）；
乘积 \(=\mathrm{L}^{-2}=[R_{\mu\nu}]\) ✔

---

## C.2 线性化 Ricci 张量（求导）

把 \(g=\eta+h\) 代入 \(R_{\mu\nu}\) 并只保留 \(h\) 的一阶项（Christoffel 是一阶量，其乘积是二阶量 ⇒ 曲率中 \(\partial\Gamma\) 保留、\(\Gamma\Gamma\) 丢弃）：

\[
\Gamma^\rho_{\mu\nu}=\frac12\eta^{\rho\delta}
\big(\partial_\mu h_{\delta\nu}+\partial_\nu h_{\mu\delta}-\partial_\delta h_{\mu\nu}\big)+O(h^2)
\]

\[
\boxed{R^{(1)}_{\mu\nu}=\frac12\Big(
\partial_\rho\partial_\mu h^\rho_{\ \nu}
+\partial_\rho\partial_\nu h^\rho_{\ \mu}
-\Box h_{\mu\nu}
-\partial_\mu\partial_\nu h\Big)}
\]

其中 \(\Box\equiv\eta^{\alpha\beta}\partial_\alpha\partial_\beta=\frac{1}{c^2}\partial_t^2-\nabla^2\)。

**规范项分离（恒等式，脚本 C2 验证 PASS）**：

定义 \(S_\nu\equiv\partial_\rho h^\rho_{\ \nu}-\frac12\partial_\nu h\)（即"谐和（洛伦兹）规范条件"的左端），则

\[
\boxed{R^{(1)}_{\mu\nu}+\frac12\Box h_{\mu\nu}=\frac12\big(\partial_\mu S_\nu+\partial_\nu S_\mu\big)}
\]

这是对**任意** \(h_{\mu\nu}\) 成立的恒等式，不依赖任何规范选择。

---

## C.3 谐和规范与线性化场方程

利用微分同胚自由度（坐标变换 \(x^\mu\to x^\mu+\xi^\mu\) 使 \(h\to h-\partial\xi-\partial\xi\)），可选**谐和（洛伦兹）规范**：

\[
\partial_\mu\bar h^{\mu\nu}=0\quad\Longleftrightarrow\quad S_\nu=0
\]

在此规范下（由 C.2 恒等式）：

\[
R^{(1)}_{\mu\nu}=-\frac12\Box h_{\mu\nu},\qquad
R^{(1)}=-\frac12\Box h
\]

\[
G^{(1)}_{\mu\nu}=R^{(1)}_{\mu\nu}-\frac12\eta_{\mu\nu}R^{(1)}
=-\frac12\Box\Big(h_{\mu\nu}-\frac12\eta_{\mu\nu}h\Big)
\]

\[
\boxed{G^{(1)}_{\mu\nu}=-\frac12\Box\bar h_{\mu\nu}}
\]

代入场方程 \(G^{(1)}_{\mu\nu}=\kappa T_{\mu\nu}\)：

\[
\boxed{\Box\bar h_{\mu\nu}=-\frac{16\pi G}{c^4}T_{\mu\nu}}
\]

（脚本 C3 验证了含规范项的一般恒等式，抽样 8 组 PASS：
\(G^{(1)}_{\mu\nu}+\frac12\Box\bar h_{\mu\nu}
-\frac12(\partial_\mu S_\nu+\partial_\nu S_\mu)+\frac12\eta_{\mu\nu}\partial_\rho S^\rho=0\)。）

**量纲核验**：\(\bar h\) 无量纲（\(h\) 是度规微扰，度规分量无量纲）；\([\Box]=\mathrm{L}^{-2}\)；
\(\frac{16\pi G}{c^4}T_{\mu\nu}\) 的量纲 \(=\mathrm{M}^{-1}\mathrm{L}^{-1}\mathrm{T}^2\cdot\mathrm{M}\mathrm{L}^{-1}\mathrm{T}^{-2}=\mathrm{L}^{-2}\) ✔

---

## C.4 牛顿极限：从波动方程到泊松方程

**牛顿极限的三条物理假设（明确列出）**：

1. **静态**：\(\partial_t\bar h_{\mu\nu}=0\Rightarrow\Box\to-\nabla^2\)；
2. **低速源**：\(T_{00}=\rho c^2\) 远大于 \(T_{0i},T_{ij}\)（即 \(\rho c^2\gg p\)，压强可忽略）；
3. **弱场**：\(|h|\ll1\) 已含于前提。

由 C.3：

\[
-\nabla^2\bar h_{\mu\nu}=-\frac{16\pi G}{c^4}T_{\mu\nu}
\;\Longrightarrow\;
\nabla^2\bar h_{00}=\frac{16\pi G}{c^4}\,\rho c^2=\frac{16\pi G\rho}{c^2}
\]

**求 \(\bar h_{00}\) 与 \(h_{00}\) 的关系**：由 \(T_{ij}\approx0\Rightarrow\nabla^2\bar h_{ij}\approx0\Rightarrow\bar h_{ij}\approx0\)，
即 \(h_{ij}=\frac12\eta_{ij}h=-\frac12\delta_{ij}h\)。取空间迹：\(h_{ii}\) 求和 \(=-\frac32h\)。
又 \(h=\eta^{00}h_{00}+\eta^{ij}h_{ij}=h_{00}-\sum_i h_{ii}=h_{00}+\frac32h\)，
故 \(h=-2h_{00}\)，于是

\[
\bar h_{00}=h_{00}-\frac12h=h_{00}+h_{00}=2h_{00}
\]

**牛顿势的识别**：弱场中 Schwarzschild 的 \(g_{00}=1-\frac{2GM}{c^2r}=1+\frac{2\Phi}{c^2}\)（\(\Phi=-\frac{GM}{r}\)），故

\[
h_{00}=\frac{2\Phi}{c^2}
\]

代入：

\[
\nabla^2(2h_{00})=\frac{4}{c^2}\nabla^2\Phi=\frac{16\pi G\rho}{c^2}
\]

\[
\boxed{\nabla^2\Phi=4\pi G\rho}
\]

（脚本 C4 用符号代数逐步验证：PASS。）

**量纲核验**：\([\nabla^2\Phi]=\mathrm{L}^{-2}\cdot\mathrm{L}^2\mathrm{T}^{-2}=\mathrm{T}^{-2}\)；
\([4\pi G\rho_{\text{mass}}]=\mathrm{M}^{-1}\mathrm{L}^3\mathrm{T}^{-2}\cdot\mathrm{M}\mathrm{L}^{-3}=\mathrm{T}^{-2}\) ✔（脚本 C6a）

---

## C.5 点源自洽检验（散度定理）

对点质量 \(M\) 位于原点：\(\Phi=-\dfrac{GM}{r}\)。

**(1) 真空区（\(r>0\)）**：

\[
\nabla^2\Big(-\frac{GM}{r}\Big)=0\qquad(r>0)
\]

符号计算确认（脚本 C5a，PASS）。

**(2) 高斯通量**（\(r=\sqrt{X^2+Y^2+Z^2}\)）：

\[
\frac{d}{dr}\Big(-\frac{GM}{r}\Big)=\frac{GM}{r^2},\qquad
\oint\nabla\Phi\cdot d\boldsymbol S=\frac{GM}{r^2}\cdot4\pi r^2=4\pi GM
\]

由散度定理 \(\int_V\nabla^2\Phi\,dV=\oint\nabla\Phi\cdot d\boldsymbol S=4\pi GM\)，
而 \(\int_V\rho\,dV=M\)，故

\[
\nabla^2\Phi=4\pi G\,M\,\delta^{(3)}(\boldsymbol r)=4\pi G\rho
\]

**与 C.4 严格一致**（脚本 C5b，PASS）。这是牛顿极限的一次**闭环自洽检验**。

---

## C.6 测地线段：从"时空弯曲"到"牛顿第二定律"

弱场低速粒子的测地线方程：

\[
\frac{d^2x^\mu}{d\tau^2}+\Gamma^\mu_{\alpha\beta}\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau}=0
\]

低速极限下 \(\frac{dx^\mu}{d\tau}\approx(c,0,0,0)\)，\(d\tau\approx dt\)：

\[
\frac{d^2x^i}{dt^2}=-c^2\,\Gamma^i_{00}
\]

对 \(g_{00}=1+\frac{2\Phi}{c^2},\ g_{ij}=-\big(1-\frac{2\Phi}{c^2}\big)\delta_{ij}\)：

\[
\Gamma^i_{00}=\frac12g^{i\delta}\big(2\partial_0g_{\delta0}-\partial_\delta g_{00}\big)
=-\frac12g^{ij}\partial_jg_{00}
=\frac{\delta^{ij}\partial_j\Phi}{c^2}=\frac{\partial^i\Phi}{c^2}
\]

\[
\boxed{\frac{d^2x^i}{dt^2}=-\partial^i\Phi}
\]

**即牛顿第二定律（单位质量）**：\(\ddot{\boldsymbol x}=-\nabla\Phi\)。
（脚本 C8 用带小参数 \(\epsilon\) 的弱场度规做一阶符号展开验证：\(\Gamma^i_{00}\) 的一阶系数 \(=\partial^i\Phi/c^2\)，PASS。）

> **本体论**："引力是一种力"（牛顿图像）与"引力是时空曲率"（GR 图像）**在弱场低速极限下给出完全相同的运动方程**——牛顿引力是 GR 的极限理论，而非错误理论。

---

## C.7 记号歧义审计（重要）

\[
\nabla^2\Phi=4\pi G\rho
\]

中的 \(\rho\) 是**质量密度** \([\rho]=\mathrm{M}\,\mathrm{L}^{-3}\)；
而麦克斯韦方程 \(\nabla\cdot\boldsymbol E=\rho/\varepsilon_0\) 中的 \(\rho\) 是**电荷密度** \([\rho]=\mathrm{I}\,\mathrm{T}\,\mathrm{L}^{-3}\)。

**同一符号 \(\rho\)，两种不同量纲**——代入错误时量纲立刻报警：

\[
[G\rho_{\text{em}}]=\mathrm{M}^{-1}\mathrm{L}^3\mathrm{T}^{-2}\cdot\mathrm{I}\,\mathrm{T}\,\mathrm{L}^{-3}
=\mathrm{M}^{-1}\mathrm{T}^{-1}\mathrm{I}\neq\mathrm{T}^{-2}
\]

（脚本 C6b 显式核验：PASS。登记为审计项 A10。）

---

## C.8 物理边界（严格标注）

1. **C.4 中的 \(\bar h_{ij}\approx0\) 是额外假设**（静态 + 无空间应力），不是场方程的推论。对引力波（辐射区 \(T_{\mu\nu}=0\) 但 \(h_{ij}\neq0\)）该假设失效 ⇒ 牛顿极限不适用（脚本 C7，BOUNDARY）。
2. **牛顿极限只覆盖 \(g_{00}\) 与 \(\Phi\) 的对应**。GR 还有牛顿理论没有的效应：光线偏折（\(2\times\) 牛顿值）、近日点进动、引力红移、引力波——这些是"超出牛顿极限"的可检验预言。
3. **谐和规范的存在性**依赖于求解规范条件（是线性偏微分方程），在渐近平直时空中可行；一般时空需另作处理。
4. **不自称新物理**：本文仅为标准推导的符号复算与量纲闭环核验，无新预言。

---

## C.9 结论

\[
\boxed{
g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu}
\;\xrightarrow{\ \text{线性化}\ }\;
\Box\bar h_{\mu\nu}=-\frac{16\pi G}{c^4}T_{\mu\nu}
\;\xrightarrow[\text{低速}]{\ \text{静态}\ }\;
\nabla^2\Phi=4\pi G\rho
\;\xrightarrow{\ \text{测地线}\ }\;
\ddot{\boldsymbol x}=-\nabla\Phi
}
\]

这条链条把 **时空几何**（左）与 **牛顿引力**（右）严格连接，且每一步都有精确的量纲与符号核验。

---

## C.10 精算结论（脚本 C 组）

| 条目 | 核验内容 | 结论 |
|---|---|---|
| C1 | 迹反转 \(R_{\mu\nu}=\kappa(T_{\mu\nu}-\frac12g_{\mu\nu}T)\) | PASS |
| C2 | 线性化 Ricci 恒等式（含 \(S_\nu\) 规范项，全 16 分量） | PASS |
| C3 | 一般线性化 Einstein 张量恒等式（抽样 8 组） | PASS |
| C4 | 牛顿极限 \(\nabla^2\Phi=4\pi G\rho\) | PASS |
| C5a | \(\Phi=-GM/r\) 在 \(r>0\) 处 \(\nabla^2\Phi=0\) | PASS |
| C5b | 高斯通量 \(=4\pi GM\)（散度定理闭环） | PASS |
| C6a | \([\nabla^2\Phi]=[4\pi G\rho_{\text{mass}}]=\mathrm{T}^{-2}\) | PASS |
| C6b | 记号歧义核验：电荷密度代入 \(G\rho\) 量纲不匹配 | PASS |
| C8 | 弱场 \(\Gamma^i_{00}\) 一阶 \(=\partial^i\Phi/c^2\Rightarrow\) 牛顿第二定律 | PASS |
| C7 | 静态/低速额外假设 | BOUNDARY |

**复跑方式**：

```
cd 02_共享基础/推导与量纲专题/延伸方向
python -B verify_extension_derivation.py
```
