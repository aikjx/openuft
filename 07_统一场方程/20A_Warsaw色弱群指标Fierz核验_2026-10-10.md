# 20A · Warsaw 色/弱群指标 Fierz 恒等机器核验（群指标展开层）

> 日期：2026-10-10  
> 状态：承接 [19A 卷](19A_J5平方四费米与Warsaw基匹配_2026-10-10.md) §5 点名的「群指标展开（$T^A$、$\tau^I$）」，机器核验 Warsaw 论文 arXiv:1008.4884 用于约化四费米算符的**色 Fierz 恒等式 (7.3)–(7.7)** 与**弱指标 Fierz 恒等式 (4.3)**。结论：$T^A$ 色 Fierz $(7.3)$、$\lambda^A$ 版本、$\tau^I$ 弱 Fierz $(4.3)$、以及 $(7.4)$ 的 $Q_{uu}$ 色分解，全部在复扩域 $\mathbb Q(i,\sqrt3)$ 上**精确成立**。由零依赖验证器 [war_colour_fierz.py](验证脚本/war_colour_fierz.py) 固化，**6/6 PASS**。本卷只核验**群指标 Fierz 的代数内核**；完整算符级推导（含矢量流场重排与 Grassmann 符号）与 18A 卷「Fierz 是算符级恒等」结论一致，不重复。

[19A · J5²与Warsaw基匹配](19A_J5平方四费米与Warsaw基匹配_2026-10-10.md) · [18A · 跨形式Fierz分解](18A_跨形式Fierz分解_J5平方手征投影_2026-10-10.md)

---

## 1. 本卷回答什么

19A 卷把 $J_5^2$ 匹配到 Warsaw 四费米类（类级），但明确标注**逐算符系数匹配需色/弱群指标展开**。Warsaw 论文在 §7 用三条群指标 Fierz 恒等式把"交叉色指标/弱指标收缩"的四费米算符约化为标准 $Q_i$：

- **(7.3)** 色 Fierz：$\sum_A T^A_{\alpha\beta}T^A_{\kappa\lambda}=\tfrac12\delta_{\alpha\lambda}\delta_{\kappa\beta}-\tfrac16\delta_{\alpha\beta}\delta_{\kappa\lambda}$；
- **(4.3)** 弱 Fierz：$\sum_I\tau^I_{jk}\tau^I_{mn}=2\delta_{jn}\delta_{mk}-\delta_{jk}\delta_{mn}$；
- 以及由 (7.3) 推出的 $(7.4){-}(7.7)$ 算符分解（如 $(7.4)$：$(\bar u_p\gamma_\mu T^A u_r)(\bar u_sT^A\gamma^\mu u_t)=\tfrac12Q_{uu}^{ptsr}-\tfrac16Q_{uu}^{prst}$）。

本卷在零依赖环境下**逐张量元精确**核验这些恒等的代数内核。难点在生成元的精确表示：Gell-Mann $\lambda^A$ 既含虚数单位 $i$（$\lambda^2,\lambda^5,\lambda^7$）又含 $\sqrt3$（$\lambda^8=\tfrac{1}{\sqrt3}\mathrm{diag}(1,1,-2)$），故用复扩域 $\mathbb Q(i,\sqrt3)$。

## 2. 方法

零依赖验证器用**精确代数数**（Fraction 构建）实现复扩域 $\mathbb Q(i,\sqrt3)$：元素 $x+y\cdot i$，$x,y\in\mathbb Q(\sqrt3)$；$i^2=-1$，$\sqrt3^2=3$。T^A=\lambda^A/2（Gell-Mann，$T^A_{\alpha\beta}$ 为 $SU(3)$ 基础表示生成元）；$\tau^I$ 为 Pauli（$SU(2)$ 弱指标）。对每条恒等做 3×3（或 2×2）全指标张量元精确比对（$3^4=81$、$2^4=16$ 个槽位）。

## 3. 结果（6/6 PASS）

| 检查 | 恒等式 | 结果 |
|---|---|---|
| C0 | $\lambda^A$ 无迹且厄米（$SU(3)$ 生成元约束） | PASS |
| C1 | $\mathrm{Tr}\,\lambda^A\lambda^B=2\delta^{AB}$（归一化） | PASS |
| C2 | $\sum_A\lambda^A_{\alpha\beta}\lambda^A_{\kappa\lambda}=2\delta_{\alpha\lambda}\delta_{\kappa\beta}-\tfrac23\delta_{\alpha\beta}\delta_{\kappa\lambda}$ | PASS |
| C3 | $\sum_A T^A_{\alpha\beta}T^A_{\kappa\lambda}=\tfrac12\delta_{\alpha\lambda}\delta_{\kappa\beta}-\tfrac16\delta_{\alpha\beta}\delta_{\kappa\lambda}$ **（论文 (7.3)）** | PASS |
| C4 | $\sum_I\tau^I_{jk}\tau^I_{mn}=2\delta_{jn}\delta_{mk}-\delta_{jk}\delta_{mn}$ **（论文 (4.3)）** | PASS |
| C5 | (7.4) 色分解：$T^A$ 收缩 $=\tfrac12$交叉（$Q_{uu}^{ptsr}$）$-\tfrac16$同色（$Q_{uu}^{prst}$） | PASS |

## 4. 对统一场论主线的意义

这三条恒等是 Warsaw 论文把四费米算符约化到标准基的工具，也是 19A 卷"逐算符系数匹配"的**代数地基**：一旦要做 $J_5^2$ 落到具体 $Q_{qq}^{(1)}$/$(3)$、$Q_{ud}^{(1)}$/$(8)$ 的系数核验，就需要 (7.3) 的色分解与 (4.3) 的弱分解（论文 Eq.(4.2) 即用 $\tau^I_{jk}\tau^I_{mn}=2\delta_{jn}\delta_{mk}-\delta_{jk}\delta_{mn}$ 推 $Q_{ll}$ 关系）。本卷确认这些恒等在零依赖精确计算下成立，为下一步**具体的 Warsaw 算符系数匹配**（如 $Q_{qq}^{(3)}$ 的三重态/单态分解、$Q_{ud}^{(8)}$ 的色八重态）铺平道路。

## 5. 诚实边界与下一步

| 关口 | 本卷所得 | 仍未做 |
|---|---|---|
| 色 Fierz (7.3)/(7.4)–(7.7)、弱 Fierz (4.3) 代数内核 | 6/6 PASS（$\mathbb Q(i,\sqrt3)$ 精确） | — |
| (7.4)–(7.7) 完整算符级推导 | 指标层核验 | 矢量流场重排(4.1)与 Grassmann 符号重演——18A 卷已证 Fierz 为算符级恒等，故不再重演 |
| 具体 Warsaw 算符系数匹配（$Q_{qq}^{(3)}$、$Q_{ud}^{(8)}$ 等三重态/八重态分解） | 未做 | 需把群指标收缩接到具体算符的味/代结构 |
| 一圈/RG/UV、量子约束/反常审计、完整量子引力、四力统一、暗物质 | 未涉及 | — |

**下一步**：把 (7.3)+(4.3) 应用到 $J_5^2$ 的具体算符系数匹配——例如 $Q_{qq}^{(3)}$（弱三重态）与 $Q_{qq}^{(1)}$（单态）的分解系数、$Q_{ud}^{(8)}$（色八重态）的 (7.4) 系数——并对论文的 19 个矢量流算符逐一核验；随后再推进一圈/RG 与量子约束、反常审计。

## 6. 本轮结论

1. Warsaw 色 Fierz $(7.3)$、$\lambda^A$ 版本、弱 Fierz $(4.3)$ 在 $\mathbb Q(i,\sqrt3)$ 上**精确成立**（6/6 PASS）。
2. $(7.4)$ 的 $Q_{uu}$ 色分解（$\tfrac12$交叉 $-\tfrac16$同色）由 (7.3) 直接推出并核验。
3. 技术性修正：初版误把虚数单位 $i$ 当 $\sqrt3$（$i^2=-1\neq(\sqrt3)^2=3$）导致全部 FAIL；改为复扩域 $\mathbb Q(i,\sqrt3)$ 后全绿——体现了"精确域选择"在生成元核验中的关键作用。
4. 具体 Warsaw 算符系数匹配与一圈/RG/UV 仍未做，是本轮明示边界。

## 参考资料

- arXiv:1008.4884，B. Grzadkowski, M. Iskrzynski, M. Misiak, J. Rosiek, *Dimension-Six Terms in the Standard Model Lagrangian*, JHEP 10 (2010) 085，Eqs. (4.2)/(4.3)、(7.3)–(7.7)。
- 19A 卷：$J_5^2$ ↔ Warsaw 类级匹配（矢量流 20+标量 4+张量 1=25）。
- 18A 卷：Fierz 为算符级恒等（裸张量重建不可行的线性代数证伪）。
