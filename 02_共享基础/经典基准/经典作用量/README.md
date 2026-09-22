# 经典作用量总览

经典作用量是 openuft 候选体系的**对照基准**。候选体系在相应极限下必须恢复这些已知正确的作用量与场方程。

## 作用量清单

| 编号 | 作用量 | 核心方程 |
|---|---|---|
| [D0](D0_作用量变分求导/README.md) | 变分法通用框架 | Euler-Lagrange 方程 |
| [D1](D1_爱因斯坦希尔伯特/README.md) | Einstein-Hilbert | Einstein 场方程 $G_{\mu\nu} = 8\pi G T_{\mu\nu}$ |
| [D2](D2_杨米尔斯/README.md) | Yang-Mills | $D_\mu F^{\mu\nu} = J^\nu$ |
| [D3](D3_狄拉克/README.md) | Dirac | $(i\gamma^\mu D_\mu - m)\Psi = 0$ |
| [D4](D4_希格斯/README.md) | Higgs | $(\square + m^2 - \lambda |H|^2)H = 0$ |
| [D5](D5_标准模型/README.md) | 标准模型 | SM 完整作用量 |
| [D6](D6_爱因斯坦嘉当/README.md) | Einstein-Cartan | EC 场方程 + 挠率方程 |

## 使用说明

- 各体系在 `05_一致性检查/` 中需对照相应基准
- 经典基准的实验确认不自动转移到候选体系
- 若候选体系在经典极限下无法恢复基准，则登记为冲突
