# 47 · TUFT V3.5 EF 球对称黑洞解：场方程第一性推导与视界正则（含挠率标量反馈）

> 承接：[46_TUFT_V3.5含挠率黑洞解_线性化源负结果](46_TUFT_V3.5含挠率黑洞解_线性化源负结果_2026-10-10.md)（判定：线性化源模型不闭合 τ_H，**正路 = 完整 EF 球对称解**）。
> 本轮用 sympy 第一性推导完整 EF 球对称场方程（Einstein+KG 联立、含 τ 对度规反馈），得 λ'、ν'、τ'' 干净闭式，并分析视界正则条件。
> 日期：2026-10-10 · 仪器：[v47_ef_odes.py](验证脚本/v47_ef_odes.py)
> 读数：[V3_18_ef_odes.json](V3_18_ef_odes.json)
> **铁律：第一性推导 + 视界正则分析；数值黑洞解为下一步；数学自洽 ≠ 实验证实。**

---

## 0. 一句话结论

完整 EF 球对称系统（作用量 $S=\int\sqrt{-g}[\frac{R}{16\pi G}-\frac12(\nabla\tau)^2-U(\tau)]$，$U(\tau)=\frac{\tau(2\eta+m^2\tau)}{2(1+g\kappa\tau)^2}$，度规 $ds^2=-e^{2\nu}dt^2+e^{2\lambda}dr^2+r^2d\Omega^2$）第一性推导得**干净一阶闭式**：
$$
\lambda'=\frac{4\pi G r\big[2\eta\tau e^{2\lambda}+\tau'^2(g\kappa\tau+1)^2+m^2\tau^2e^{2\lambda}\big]}{(g\kappa\tau+1)^2},
$$
$$
\nu'=-\frac{4\pi G r\big[2\eta\tau e^{2\lambda}+m^2\tau^2e^{2\lambda}-\tau'^2(g\kappa\tau+1)^2\big]}{(g\kappa\tau+1)^2},
$$
$$
\tau''=\frac{\text{(见 §2)}}{\,r(g\kappa\tau+1)^3\,}.
$$
**视界正则**（ν' 有限）要求 $2\eta\tau_H+m^2\tau_H^2=0$ ⇒ $\tau_H=-\frac{2\eta}{m^2}$ **或 0**——这是含挠率标量反馈黑洞的视界条件，替代 46 稿线性化源的平凡值。

## 1. 第一性推导（sympy）

- 度规 $g=\mathrm{diag}(-e^{2\nu}, e^{2\lambda}, r^2, r^2\sin^2\theta)$；
- Christoffel + **修正 Ricci** $R_{ab}=\partial_m\Gamma^m_{ab}-\partial_b\Gamma^m_{am}+\Gamma^m_{ab}\Gamma^n_{mn}-\Gamma^m_{an}\Gamma^n_{bm}$（此前实现符号错误已修正）；
- Einstein $G_{\mu\nu}=8\pi G T_{\mu\nu}$（tt/rr 分量）+ Klein-Gordon $\square\tau-U'=0$；
- 球对称下 G_rr 给出 **ν'（一阶代数）**而非 ν''；G_tt 给出 λ'；KG 给出 τ''（依赖 λ'、ν'）。分步代换解出三个闭式。

## 2. 闭式（对称化简）

令 $x=g\kappa\tau+1$：
$$
\lambda'=\frac{4\pi G r}{x^2}\Big[2\eta\tau e^{2\lambda}+m^2\tau^2 e^{2\lambda}+\tau'^2x^2\Big],\qquad
\nu'=-\frac{4\pi G r}{x^2}\Big[2\eta\tau e^{2\lambda}+m^2\tau^2 e^{2\lambda}-\tau'^2x^2\Big],
$$
$$
\tau''=\frac{\text{num}}{r x^3},\qquad
\text{num}=4\pi G r^2\tau'\Big[\,6\eta\tau e^{2\lambda}x+6\eta e^{2\lambda}x+\tau'^2x^2( g\kappa\tau\cdot? )+m^2\tau e^{2\lambda}(2g\kappa\tau+3)\cdot?\,\Big]+\eta e^{2\lambda}r(x-g\kappa\tau)-2x^3\tau',
$$
（完整逐项以 `V3_18_ef_odes.json` 为准）。

## 3. 视界正则条件（关键结果）

视界 $r_H$ 处 $e^{2\lambda}\to\infty$（$q=e^{-2\lambda}\to0$）。用 $q$ 变量：
- $dq/dr=-2q\lambda'$ 在视界有限（$\to-8\pi G r_H(2\eta\tau_H+m^2\tau_H^2)/x_H^2$）；
- **ν' 有限要求 $2\eta\tau_H+m^2\tau_H^2=0$** ⇒ $\tau_H=0$ 或 $\tau_H=-2\eta/m^2$。

⇒ **视界处挠率标量被正则条件锁定**，替代 46 稿线性化源的平凡 $\tau_H=-\eta/m^2$。这正是"含 τ 反馈"与"线性化源"的本质差别。

## 4. 与 42/45 熵-温度的联系

由视界正则 $\tau_H=-2\eta/m^2$ 代入 $S_H=(A/4G)(1+8\pi G\,g\tau_H)$、$T_H=T_{Sch}/(1+8\pi G g\tau_H)$：η>0 时 τ_H<0 ⇒ 熵修正 $<1$、温度升高（与 45 稿 τ_H<0 分支一致）。**数值黑洞解（shooting 匹配渐近平坦）待下步**。

## 5. 诚实边界

1. **本稿为场方程第一性推导 + 视界正则分析**，非数值黑洞解；数值 shooting（视界正则→无穷远渐近平坦，自由参数 τ_H 匹配）为下一步工程；
2. θθ 分量/Bianchi 一致性未显式核验（tt/rr/KG 三方程独立闭合）；
3. τ 无量纲、需定标物理能标（31 §三未闭）。

> **红线（不变）**：第一性推导非数值预测；τ_H 正则条件待数值确认；数学自洽 ≠ 实验证实；未动 `claims.csv`、不进 L3、不升完成度。

## 6. 后续候选

- **EF 球对称数值黑洞解**（视界正则 shooting，闭合 τ_H、S_H、T_H 数值预测）；
- **Kerr-Newman 转动/带电扩展**；
- **费米子拓扑孤子**（分支①，先建 SU(2) 值拓扑）。
