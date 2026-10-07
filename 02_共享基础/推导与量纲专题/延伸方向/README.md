# 延伸方向（A–F）｜求导证明与精算验证

本目录是 [《全套推导与量纲专题》](../README.md) 末尾"下一步可选延伸方向"的**全部展开**（A–F 六项全部完成），
每项都配 **符号求导证明文档** + **脚本化精算验证**。

- 严格区分 **数学定义 / 量纲分析 / 本体论解释**；SI 单位制；签名 \((+,-,-,-)\)。
- 所有"求导证明"均由 `verify_extension_derivation.py`（sympy 符号求导 + mpmath 50 位精算）复算。
- **红线**：本目录是**标准物理框架内的自洽性核验与教学级推导整理**，不含新物理预言，不构成对既有理论的修正。

---

## 1. 目录

| 文件 | 内容 | 精算条目 |
|---|---|---|
| [A_麦克斯韦方程的4维张量形式.md](A_麦克斯韦方程的4维张量形式.md) | \(A^\mu\to F_{\mu\nu}\to\partial_\mu F^{\mu\nu}=\mu_0J^\nu\)、对偶 Bianchi、电荷守恒 | A1–A16 |
| [B_最小耦合原理.md](B_最小耦合原理.md) | \(\partial_\mu\to D_\mu\) 的规范协变性证明、两套约定配对、对易子 = 场强、动量平移 | B1–B8 |
| [C_弱场近似与牛顿泊松方程.md](C_弱场近似与牛顿泊松方程.md) | 迹反转、线性化、谐和规范、\(\nabla^2\Phi=4\pi G\rho\)、测地线 \(\to\) 牛顿第二定律 | C1–C8 |
| [D_普朗克单位的量纲推导.md](D_普朗克单位的量纲推导.md) | 量纲矩阵秩与唯一性、三组解、50 位数值 vs CODATA | D1–D10 |
| [E_黎曼对称性与Bianchi恒等式.md](E_黎曼对称性与Bianchi恒等式.md) | 四条代数对称性、独立分量数、两个 Bianchi 恒等式、两个度规基准 | E1–E18 |
| [F_弯曲时空规范协变导数.md](F_弯曲时空规范协变导数.md) | \(\nabla_\mu\to D_\mu=\nabla_\mu-i\frac{q}{\hbar}A_\mu\)（A8 具体实现）：标量/矢量对易子、弯曲规范协变、动量平移 | F1–F8 |
| `verify_extension_derivation.py` | 精算脚本（sympy + mpmath；标准库 Fraction 做量纲线性代数） | — |
| `verify_extension_derivation_report.txt` | 最近一次运行报告 | — |
| `verify_extension_F_curved_gauge.py` | 方向 F 精算脚本（Schwarzschild 背景规范协变导数） | — |
| `verify_extension_F_curved_gauge_report.txt` | 方向 F 最近一次运行报告 | — |

---

## 2. 精算汇总

```
A–E 聚合：PASS = 60 / FAIL = 0 / BOUNDARY = 3 / INFO = 3   （verify_extension_derivation.py）
F 单独：   PASS =  8 / FAIL = 0 / BOUNDARY = 0 / INFO = 0   （verify_extension_F_curved_gauge.py）
合计：     PASS = 68 / FAIL = 0 / BOUNDARY = 3 / INFO = 3
```

| 组 | PASS | BOUNDARY | INFO | 主题 |
|---|---|---|---|---|
| A | 15 | 0 | 1 | 麦克斯韦方程 4 维形式 |
| B | 7 | 1 | 0 | 最小耦合原理 |
| C | 9 | 1 | 0 | 弱场近似 → 牛顿泊松方程 |
| D | 13 | 1 | 0 | 普朗克单位量纲推导 |
| E | 16 | 0 | 2 | 黎曼对称性与 Bianchi |
| F | 8 | 0 | 0 | 弯曲时空规范协变导数 |
| **合计** | **68** | **3** | **3** | — |

**复跑**：

```
cd 02_共享基础/推导与量纲专题/延伸方向
python -B verify_extension_derivation.py          # A–E（PASS=60 / FAIL=0）
python -B verify_extension_F_curved_gauge.py      # F（PASS=8 / FAIL=0）
```

依赖：`sympy`（符号求导）、`mpmath`（50 位精算）；量纲线性代数用标准库 `fractions.Fraction`（精确有理数，无浮点误差）。
脚本退出码：`FAIL == 0` 时为 0，否则为 1。

---

## 3. 本轮新增的审计项（已同步至 `../量纲审计与修正清单.md`）

| 编号 | 类型 | 内容 | 处置 |
|---|---|---|---|
| **A9** | 表述不完整 | 任务 4 给出 \(A_\mu\) 的规范变换，任务 5 给出 \(D_\mu=\partial_\mu-i\frac{q}{\hbar}A_\mu\)，但**两者未构成完整约定对**：缺少物质场相位 \(\psi\to e^{-iq\lambda/\hbar}\psi\)。两套约定必须成对使用（见延伸 B 的 B.3 表） | 已在延伸 B 补全两套完整约定对并符号验证（B1/B2） |
| **A10** | 记号歧义 | 同一符号 \(\rho\) 在电磁学中表示**电荷密度**（\(\mathrm{I\,T\,L^{-3}}\)），在牛顿泊松方程中表示**质量密度**（\(\mathrm{M\,L^{-3}}\)）。代入错误时量纲立即报警：\([G\rho_{\mathrm{em}}]=\mathrm{M}^{-1}\mathrm{T}^{-1}\mathrm{I}\neq\mathrm{T}^{-2}\) | 延伸 C 显式核验（C6a/C6b）；建议在跨领域文档中为 \(\rho\) 加下标 \(\rho_m/\rho_q\) |
| **A11** | 口径声明 | \(\partial_\mu\) 的"分量异构"问题：3 维视角下 \(\partial_t\sim\mathrm{s}^{-1}\)、\(\nabla\sim\mathrm{m}^{-1}\)；4 维相对论视角下取 \(x^0=ct\) 后四分量统一为 \(\mathrm{L}^{-1}\)。二者不矛盾，但混用会产生量纲错误 | 已在延伸 A 的 A.0 与脚本 A16 显式声明 |

分级说明：A9–A11 均为**表述/记号层面**问题，**不是**量纲数值错误，与清单中 A1–A8 的实质缺陷（如 \(D_\mu\) 缺 \(\frac{1}{\hbar}\)、\(\mathrm{T\cdot m}\) 单位错误、\(F^{\mu\nu}\) 指标错置）分级不同。

---

## 4. 各延伸项的一句话结论

- **A**：\(\boldsymbol E\) 与 \(\boldsymbol B\) 不是两个实体，而是同一个 2-形式 \(F_{\mu\nu}\) 的分量；高斯定律与安培–麦克斯韦定律是**同一个** 4 维方程 \(\partial_\mu F^{\mu\nu}=\mu_0J^\nu\) 的 \(\nu=0\) 与 \(\nu=i\) 分量；\(\nabla\cdot\boldsymbol B=0\) 与法拉第定律是**同一条**恒等式 \(\mathrm{d}F=\mathrm{d}^2A=0\) 的两个分量。
- **B**：最小耦合 \(\partial_\mu\to D_\mu\) 的物理内容是**动量平移** \(p_\mu\to p_\mu-qA_\mu\)；\(-i\hbar\) 乘进去后 \(\hbar\) 精确消去，两侧量纲同为 \(\mathrm{M\,L\,T^{-1}}\)——这反过来印证了 \(D_\mu=\partial_\mu-i\frac{q}{\hbar}A_\mu\) 的形式正确。
- **C**：\(g=\eta+h\Rightarrow\Box\bar h_{\mu\nu}=-\frac{16\pi G}{c^4}T_{\mu\nu}\Rightarrow\nabla^2\Phi=4\pi G\rho\Rightarrow\ddot{\boldsymbol x}=-\nabla\Phi\)，链条两端由**牛顿势 \(\Phi=-GM/r\) 的散度定理**（通量 \(4\pi GM\)）闭环核验。
- **D**：\(\{\hbar,G,c\}\) 的量纲矩阵 \(\det=-2\neq0\) ⇒ 普朗克质量/长度/时间的形式**唯一**，且**不存在**非平凡无量纲组合 ⇒ 纯量纲分析**不能**判定"引力何时必须量子化"。
- **E**：四条代数对称性 + 两个 Bianchi 恒等式都是**定义层的数学恒等式**（不含物理假设）；4 维时空曲率有 **20 个独立分量**，其中 10 个由 Weyl 张量承载——真空中的引力自由度（引力波、潮汐）就活在那里。
- **F**：A8 的具体实现——在 Schwarzschild 背景上 $D_\mu=\nabla_\mu-igA_\mu$ 良定义且保持 $[D_\mu]=\mathrm{L}^{-1}$；**标量**对易子 $[D_\mu,D_\nu]\psi=-igF_{\mu\nu}\psi$ 与度规无关（曲率不进入标量最小耦合），**矢量**对易子 $[D_\mu,D_\nu]V^\rho=R^\rho_{\ \sigma\mu\nu}V^\sigma-igF_{\mu\nu}V^\rho$（曲率项出现）——这是弯曲时空规范理论中标量与矢量场的最小耦合结构差异。
