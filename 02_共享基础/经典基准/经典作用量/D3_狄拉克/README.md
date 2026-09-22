# D3 · Dirac 作用量

## 作用量

$$S_{\rm Dirac} = \int d^4x \, \bar{\Psi} (i \gamma^\mu D_\mu - m) \Psi$$

- $\Psi$：Dirac 旋量（4 分量）
- $\bar{\Psi} = \Psi^\dagger \gamma^0$
- $\gamma^\mu$：Dirac 矩阵，满足 $\{\gamma^\mu, \gamma^\nu\} = 2 g^{\mu\nu}$
- $D_\mu = \partial_\mu + i g A_\mu^a T^a$：协变导数

## 场方程（变分 $\delta \bar{\Psi}$）

$$(i \gamma^\mu D_\mu - m) \Psi = 0$$

## 关键性质

- **手征**：$\Psi_L = P_L \Psi$, $\Psi_R = P_R \Psi$，$P_{L/R} = \frac{1}{2}(1 \mp \gamma_5)$
- **CPT 定理**：洛伦兹不变的定域场论必然满足 CPT 对称
- **自旋-统计定理**：半整数自旋服从费米-狄拉克统计

## 与 openuft 体系对照

| 体系 | 恢复情况 |
|---|---|
| 07_统一场方程 (UFE-1) | UFE-1 含 Dirac 费米子项 |
| S06_TCL拓扑手征锁定 | 手征性的拓扑解释 |
| S13_全域双向分形 | 旋量从对偶几何涌现 |
