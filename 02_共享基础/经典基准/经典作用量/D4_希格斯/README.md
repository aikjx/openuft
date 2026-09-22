# D4 · Higgs 作用量

## 作用量

$$S_{\rm Higgs} = \int d^4x \left( |D_\mu H|^2 - \mu^2 |H|^2 + \lambda |H|^4 \right)$$

- $H$：复标量二重态（$SU(2)_L$）
- $\mu^2 < 0$：触发对称破缺
- $\lambda > 0$：自耦合

## 真空期望值

$$\langle H \rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 0 \\ v \end{pmatrix}, \quad v = \sqrt{\frac{-\mu^2}{\lambda}} \approx 246 \text{ GeV}$$

## 质量生成

- 规范玻色子：$m_W = \frac{g v}{2}$, $m_Z = \frac{v}{2}\sqrt{g^2 + g'^2}$
- 费米子：$m_f = \frac{y_f v}{\sqrt{2}}$（Yukawa 耦合 $y_f$）
- Higgs 玻色子：$m_H = \sqrt{2\lambda} v \approx 125$ GeV

## 与 openuft 体系对照

| 体系 | 恢复情况 |
|---|---|
| 07_统一场方程 (UFE-1) | UFE-1 含 Higgs 场与对称破缺 |
| S08_GAQ常数几何化体系 | 常数几何化尝试，已登记 M02 冲突 |
| S13_全域双向分形 | 真空约束 $|\Psi|^2 = v^2$ |
