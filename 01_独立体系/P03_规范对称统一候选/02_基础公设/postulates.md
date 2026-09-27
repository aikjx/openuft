# P03 基础公设 · 规范对称统一候选（内部群 GUT 路线·第一次公设建模）

- 体系编号：`p03_gauge_unification`
- hypothesis_revision：`gut-first-formulation`（2026-09-26 首次公设化）
- 状态：`candidate_framework` / `unreviewed`
- 配套精算：[`../07_计算复现/源码/p03_gut_first_formulation.py`](../07_计算复现/源码/p03_gut_first_formulation.py)（纯标准库，exit 0）
- 立项依据：[`../00_研究立项/立项评估.md`](../00_研究立项/立项评估.md)
- 边界依据：本书第79章（定理 Q，Coleman–Mandula 直积）、第82章（能力边界白皮书）

> 本文件把 P03 从"方向占位（unformulated，postulates=[]）"升级为**有明确群、表示、破缺链、作用量骨架与可对标量的待完备理论框架**。
> **隔离声明**：本公设集**不继承** S07/S08/S09/S10 已标 falsified 的"常数几何化"派生链，不使用普朗克锚定，不声称由螺旋/曲率/挠率第一性导出规范群。统一**只在与时空直积的内部因子内进行**（定理 Q）。

---

## A1　内部–时空直积边界公设

统一作用量的规范部分定义在与时空对称群直积的内部因子上：

$$
\mathcal G_{\rm total}=\mathcal P_{\rm Poincar\acute e}\times G,\qquad [T_{\rm spacetime},T_G]=0 .
$$

**陈述**：$G$ 是紧致半单内部李群；其生成元不带时空指标，时空几何量（曲率 $\kappa$、挠率 $\tau$、涡量 $\omega$、螺旋频率）不出现在 $G$ 的定义中。
**依据**：Coleman–Mandula 定理（1967）在 4D 局域非平凡散射下唯一自洽安排（第79章 定理 Q，Jacobi 机器检验）。
**边界**：本公设主动放弃"把强/弱力几何化为 4D 时空曲率"的路线——该路线已被定理 Q 封死。

## A2　单群统一公设

存在单一紧致半单群 $G$ 包含标准模型规范群，并在大统一能标处三耦合相等：

$$
G\supset G_{\rm SM}=SU(3)_c\times SU(2)_L\times U(1)_Y,\qquad g_1(M_{\rm GUT})=g_2(M_{\rm GUT})=g_3(M_{\rm GUT})\equiv g_G .
$$

**候选序列**：$SU(5)\subset SO(10)\subset E_6$。$M_{\rm GUT}$ 由耦合跑动决定，不是手写输入。
**精算**：脚本第 3 段，1 圈 SM 三耦合**不汇聚**（$1$–$2$ 交汇 $1.0\times10^{13}$ GeV 处与 $\alpha_3$ 散布 **5.58**）；MSSM 在 $2.0\times10^{16}$ GeV 汇聚（散布 **0.078**）。

## A3　表示填充与无反常公设

每代费米子（左手 Weyl）填入 $G$ 的无反常不可约表示：

- **SU(5)**：$\bar{\mathbf 5}\oplus\mathbf{10}$。分解
  $\bar{\mathbf5}=d^c(\mathbf3,\mathbf1,+\tfrac13)\oplus L(\mathbf1,\mathbf2,-\tfrac12)$，
  $\mathbf{10}=Q(\mathbf3,\mathbf2,+\tfrac16)\oplus u^c(\bar{\mathbf3},\mathbf1,-\tfrac23)\oplus e^c(\mathbf1,\mathbf1,+1)$。
  维度 $3+2+6+3+1=15$（即第76章 S06 审计的单代 15 个左手 Weyl）；
  $\sum{\rm dim}\,Y=0$、$\sum{\rm dim}\,Y^3=0$（脚本用有理数精确为 0）；
  SU(5) 三角反常指数 $A(\bar{\mathbf5})+A(\mathbf{10})=-1+1=0$。
- **SO(10)**：单个 $\mathbf{16}=\bar{\mathbf5}\oplus\mathbf{10}\oplus\mathbf1$，多出的单态 $\mathbf1=\nu^c$（右手中微子），天然容纳轻中微子。三代复制三次。

## A4　自发对称破缺公设

$G$ 经 Higgs 表示的真空期望值逐级破缺：

$$
SU(5)\xrightarrow{\ \langle\mathbf{24}\rangle\ }SU(3)_c\times SU(2)_L\times U(1)_Y\xrightarrow{\ \langle\mathbf5\rangle\ }SU(3)_c\times U(1)_{\rm em} .
$$

伴随 $\mathbf{24}$ 破缺出现的大统一矢量玻色子 $X/Y$（携带色与弱荷，介导夸克↔轻子）获得质量 $M_X\sim M_{\rm GUT}$；电弱破缺由 $\mathbf5$ 给出费米子质量。

## A5　耦合统一重整化群公设

规范耦合按 1（可推进至 2）圈 $\beta$ 函数跑动：

$$
\alpha_i^{-1}(\mu)=\alpha_i^{-1}(M_Z)-\frac{b_i}{2\pi}\ln\frac{\mu}{M_Z},\quad
\begin{cases}b^{\rm SM}=(41/10,-19/6,-7)\\ b^{\rm MSSM}=(33/5,1,-3)\end{cases}
$$

$M_Z$ 边界取实测 $\alpha_{\rm EM}^{-1}=127.951$、$\sin^2\theta_W=0.23122$、$\alpha_s=0.1179$。统一条件 $g_1=g_2=g_3$ 给出 $M_{\rm GUT}$ 与对 $\sin^2\theta_W$ 的预言，供实验对标。

## A6　几何本体零贡献元公设（边界声明）

**曲率 $\kappa$、挠率 $\tau$、涡量 $\omega$、螺旋频率在 $G$ 的选择、表示填充、破缺势、汇聚尺度的任何判据中出现次数为 0（脚本第 6 段实测 0/5）。** 选群依据仅为：① 单代费米子的表示容纳度；② 三角反常抵消；③ 三耦合汇聚；④ $\sin^2\theta_W$ 与质子衰变的实验对标；⑤ 内部群分支律。

**含义**：P03 是一个**独立、健康的内部群研究纲领**，不是 openuft 螺旋/空间本体的推导产物；它的成立既不支持、也不依赖"四力皆空间螺旋几何"的主张（该主张作为推导性统一已被定理 Q 否决）。

---

## 五字段元数据（关键量）

| 符号 | 定义 | 来源 | 量纲 | 数值（脚本） | 状态 |
|---|---|---|---|---|---|
| $\bar{\mathbf5}\oplus\mathbf{10}$ | SU(5) 单代表示 | A3 | 维 15 | ΣY=ΣY³=0，A=0 | 标准结果 [A]，脚本 verified |
| $\mathbf{16}$ | SO(10) 单代表示 | A3 | 维 16 | 含 ν^c | [A] |
| $b^{\rm SM},b^{\rm MSSM}$ | 一圈 β 系数 | A5 | 无量纲 | (4.1,−3.17,−7)/(6.6,1,−3) | [A] |
| $M_{\rm GUT}$ | 三耦合并拢尺度 | A5 | 能量 | SM 不汇聚；MSSM 2.0e16 GeV | [A] 数值，本库复算 |
| $\sin^2\theta_W$ | SU(5) 树级/实测 | A5 | 无量纲 | 0.375 / 0.23122 | [A] |
| $\tau_p(e^+\pi^0)$ | 质子寿命 | A4 推论 | 时间 | 最小SU5 1e29–31；SK>1.6e34 | 最小SU5 被排除 |
| $n_{\rm geo}$ | 几何本体输入数 | A6 | 计数 | **0/5** | 定理 Q 推论 |

## 诚实边界

- 具体群 $SU(5)/SO(10)/E_6$ 的选择、Higgs 破缺势参数、全部 Yukawa 耦合仍自由（数量不少于标准模型自由参数）；耦合统一只约束 3 个规范耦合的关系，**不第一性给出 $\alpha$ 绝对值或费米子质量谱**。
- **最小非 SUSY SU(5) 已被质子衰变实验排除**（见 [`../11_证伪与反例/最小SU5质子衰变排除记录.md`](../11_证伪与反例/最小SU5质子衰变排除记录.md)）；耦合汇聚良好的 MSSM 需要整套超对称，而 LHC 至今零超粒子证据。
- 本框架**不统一引力**（引力是时空因子，按 A1 与内部群直积），不改变 UFT 联盟层 2/6，不产生 openuft 已统一四力的结论。
- 全部体系身份仍为 unreviewed；脚本为 1 圈演示级，2 圈与阈值修正未做。
