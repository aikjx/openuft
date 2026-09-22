# D1 · Einstein-Hilbert 作用量

## 作用量

$$S_{\rm EH} = \frac{1}{16\pi G_N} \int d^4x \sqrt{-g} \left( R - 2\Lambda \right) + S_{\rm matter}$$

- $R$：Ricci 标量
- $\Lambda$：宇宙学常数
- $G_N$：牛顿引力常数

## 场方程（变分 $\delta g^{\mu\nu}$）

$$G_{\mu\nu} + \Lambda g_{\mu\nu} = 8\pi G_N T_{\mu\nu}$$

其中 $G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}R g_{\mu\nu}$ 为 Einstein 张量，$T_{\mu\nu} = -\frac{2}{\sqrt{-g}} \frac{\delta S_{\rm matter}}{\delta g^{\mu\nu}}$ 为能动量张量。

## 关键常数

| 常数 | 符号 | CODATA 值 |
|---|---|---|
| 牛顿引力常数 | $G_N$ | $6.67430(15) \times 10^{-11}$ m³ kg⁻¹ s⁻² |
| 宇宙学常数 | $\Lambda$ | $\sim 1.1 \times 10^{-52}$ m⁻²（观测） |

## 与 openuft 体系对照

| 体系 | 恢复情况 |
|---|---|
| 07_统一场方程 (UFE-1) | UFE-1 含 EC 引力，$\Lambda=0$ 极限下恢复 EH |
| S04_IEG信息熵引力 | Einstein 方程重述 |
| S02_空间光速螺旋统一力 | 低速极限冲突（M03），未恢复 |
