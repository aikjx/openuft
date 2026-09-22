# 实现方式档案：UFE-1 统一场方程

[实现方式总览](../README.md) · 归属：[候登记_ufe1](../../体系坐标系/体系坐标表.md) · 理论正文：[07_统一场方程](../../../07_统一场方程/README.md)

- **形态**：M1 符号推导 · M2 数值验算 · M6 论文
- **位置**：`openuft/07_统一场方程/`（11 篇正文 + 2 个 CSV + 1 个生成器 + 1 个验证器）
- **状态**：active（自证完备，外部校准未做）

## 主张与本体

主方程取自单一总联络 $\mathcal A$ 的曲率：

$$\frac{\delta S}{\delta\Phi}=0,\quad \Phi=(e,\mathcal A,H,\Psi);\qquad
\star D_{\mathcal A}\!\star\mathcal F=\mathcal J,\quad \mathcal F=d\mathcal A+\mathcal A\wedge\mathcal A$$

"四种力写在一个方程"的机制是**李代数直和分解**：

$$\mathfrak g=\mathfrak{so}(1,3)\oplus\mathfrak{su}(3)\oplus\mathfrak{su}(2)\oplus\mathfrak u(1)$$

四种力是同一曲率沿四个因子的分量，不是四个并列项。麦克斯韦齐次方程来自统一比安基恒等式
$D_{\mathcal A}\mathcal F\equiv0$，不来自变分。

## 诚实评级

| 项 | 结论 |
|---|---|
| 理论实质 | **Einstein–Cartan（含挠率）引力 + 标准模型**，非新提出的替代物理 |
| 已完成 | 五组变分（$\delta\omega,\delta e,\delta A,\delta H,\delta\Psi$）逐步展开；四力还原；反常消除精确有理计算 |
| 关键推算 | 由 $G_F,\alpha,m_Z,m_t$ 算出 $m_W=80.409$ GeV，实测 $80.377\pm0.012$，**偏差 0.04%** |
| 主要缺陷 | **19 个输入参数**（含 $\alpha$ 的数值、质量谱、代数、$\Lambda$ 全部为输入）；无右手中微子致 $m_
u=0$，与振荡实验矛盾 |
| 未解决 | 禁闭无解析证明（Clay 问题）、引力量子化、层级问题、强 CP、暗物质 |

**与既有体系的区别**：S14（TUFT）同样以主丛与联络为骨架，但其多项 claims 已登记为 falsified
（挠率多分量相加为类型错误、$\sin^2\theta_W$ 尺度混淆、单圈三耦合不汇聚）。UFE-1 不重复这些错误：
挠率在本体中是**代数**方程（不传播、不产生第五种力），$\sin^2\theta_W$ 与耦合统一作为**检验项**而非结论登记。

## 验证方式与结果

`07_统一场方程/验证脚本/verify_core.py` —— **零第三方依赖**（纯 `fractions` + `math`），可复跑：

```bash
cd openuft/07_统一场方程/验证脚本 && python -B verify_core.py
```

**47 项：PASS 38 / FAIL 3 / INFO 6。** 三项 FAIL 是如实登记的否定结果：
SM 单圈三耦合不统一（$\alpha^{-1}$ 最小散布 3.66，MSSM 对照 0.049）、无右手中微子。

## 待裁定事项

1. **编号归属未定**：本板块现为顶层 section，未进入 `01_独立体系/` 的 `sNN` 注册。
   是否改登记为 `s15`、是否补 `system.json` + 17 阶段 + `claims.csv`，需维护者裁定。
   在此之前，坐标表中以 `候登记_ufe1` 记录。
2. **外部校准未做**：UFT-1…UFT-6 判据未与标准模型之外的其他路线做定量计分（路线图 D3）。
3. **C8=19 未被优化**：参数数目未做任何自然性论证。
