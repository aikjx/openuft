# D6 · Einstein-Cartan 作用量

## 作用量

$$S_{\rm EC} = \frac{1}{16\pi G} \int d^4x \, e \, e^\mu_a e^\nu_b R^{ab}_{\mu\nu}(\omega)$$

- $e^a_\mu$：标架（vierbein）
- $\omega^{ab}_\mu$：自旋联络
- $R^{ab}_{\mu\nu}$：曲率 2-形式
- 独立变量：$e^a_\mu$ 与 $\omega^{ab}_\mu$（Palatini 形式）

## 场方程

**变分 $\delta e^a_\mu$**（Einstein 方程）：

$$R^\mu_\nu - \frac{1}{2} e^\mu_a e^a_\nu R = 8\pi G T^\mu_\nu$$

**变分 $\delta \omega^{ab}_\mu$**（挠率方程）：

$$D_\mu e^\nu_a + D_\nu e^\mu_a = 8\pi G S^{\mu\nu}_a$$

其中 $S^{\mu\nu}_a$ 为自旋密度，挠率 $T^a = de^a + \omega^a_b \wedge e^b \neq 0$。

## 关键性质

- 挠率由物质的**内禀自旋**产生
- 无自旋物质时，挠率为零，EC 退化为 GR
- 挠率可能避免奇点（硬核反弹）

## 与 openuft 体系对照

| 体系 | 恢复情况 |
|---|---|
| 07_统一场方程 (UFE-1) | UFE-1 即 EC + SM 规范场 |
| S14_TUFT | 挠率统一场论，含 EC 挠率 |
| S11_GMUFT | 曲率、挠率、拖拽自由度 |
