# 附录B 关键公式大全与推导索引

> 本附录按编整理全书关键公式。每条标注：方程名 / LaTeX / 来源公设 / 推导步数 / 所在章节。
> 推导步数来自各体系 postulates.md 与书稿；缺口留空。

## B.1 螺旋几何公式（S01/S02/S07/S10/S12）

| 方程名 | LaTeX | 来源公设 | 推导步数 | 章节 |
|---|---|---|---|---|
| 三重奏恒等式 | $\kappa^2+\tau^2=(\omega/v)^2$ | S01-A1+A2 | 2 | 第2章 / S01 |
| D 维推广 | $\sum_{i=1}^{D-1}\kappa_i^2=-\mathrm{tr}(A^2)/(2v^2)$ | S01-A3 | R9 已证 | 第2章 |
| Planck 重组 | $\kappa\ell_P=E/E_P=\ell_P/\lambda_C$ | 恒等重写 | S4 已验证（250 位，5 粒子 ≤1×10⁻²⁵¹） | 第2章 |
| 量纲修复式 | $(\kappa\ell_P)^2+(\tau\ell_P)^2=(\omega\ell_P/c)^2$ | 修复原式 70 数量级断裂 | 1 | 第2章 |
| v=c 特化 | $\kappa^2+\tau^2=(\Omega/c)^2$ | S02 借用 S01 | param_sweep 13 点误差 <2×10⁻¹⁶ | 第7章 |
| Darboux 标架 | $\boldsymbol\omega_D=\tau\boldsymbol T+\kappa\boldsymbol B$ | S02 | $|\omega_D|=\Omega/c$ | 第7章 |
| S12 核心恒等式 | $\kappa^2+\tau^2=(\omega/c)^2$ | S12-A1–A3 | 6 步（本质即 S01 定理） | 第8章 |
| S07 G2 | $\kappa=\rho/(\rho^2+b^2),\ \tau=b/(\rho^2+b^2)$ | S07-A1–A3 | 约 6 步（叉积微分） | 第14章 |
| S07 G3 | $\kappa^2+\tau^2=1/R^2$ | S07-A3 | 1 步对偶不变量 | 第14章 |

## B.2 GAQ 恒等式与常数关系（S03/S07/S08）

| 方程名 | LaTeX | 来源公设 | 推导步数 | 章节 |
|---|---|---|---|---|
| T1 Planck 乘积 | $M_p c L_p=\hbar$ | S03-A1+A4+A5 | 1（定义式代入） | 第6章 |
| T2 G 重排 | $G=\hbar c/M_p^2$ | S03-T1 | 定义重排 | 第6章 |
| T3 E=mc² | $E=Mc^2$ | S03 | 定义重排 | 第6章 |
| T5 场方程 | $G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G T_{\mu\nu}$ | S03-A3 张量化 | 1 步 | 第6章 |
| T6 α 定义 | $\alpha=(e/q_p)^2$ | S03 | 定义式改写 | 第6章 |
| T9 黑洞熵 | $S_{BH}=k_B A/(4L_p^2)$ | Bekenstein-Hawking | 引用结果 | 第6章 |
| S07 G4 α | $\alpha=\tau/\kappa=b/\rho=7.297353\times10^{-3}$ | S07 | 数值由 α 回代 | 第14章 |
| S07 P1 m | $m=\hbar/(cR)=\hbar\sqrt{\kappa^2+\tau^2}/c$ | S07 | 2 步（E=ħω=mc²） | 第14章 |
| S07 P2 G | $G=c^3R^2/\hbar=c^3/[\hbar(\kappa^2+\tau^2)]$ | S07 | 1 步（令 m_P≡m_R） | 第14章 |
| S07 W6 色散 | $\omega^2=c^2k^2[1-\alpha(l_Pk)^2]$ | S07 §6.1 | 唯一带新参数可证伪式 | 第14/26章 |
| S07 P3 MOND | $a_0=cH_0/2\pi$ | S07 | 可证伪 | 第14/26章 |
| S08 A3 c | $c=\omega R=2\pi R/T$ | S08 §2.1 | 1 步（§9 自承同义反复） | 第15章 |
| S08 A4 ħ | $\hbar=mcR=\frac1{2\pi}\oint\boldsymbol p\cdot d\boldsymbol s$ | S08 §3.1 | 2 步（§9 自承同义反复） | 第15章 |
| S08 A5 e | $e=\sqrt{4\pi\varepsilon_0\tau\kappa^{-1}\hbar c}$ | S08 §4.1 | 1 步（由 α SI 定义反解） | 第15章 |

## B.3 信息熵引力公式（S04）

| 方程名 | LaTeX | 来源公设 | 推导步数 | 章节 |
|---|---|---|---|---|
| I1 信息流 | $G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G T_{\mu\nu}\iff\nabla^\mu J_{\mu\nu}^{\rm info}=0$ | S04-A1 | Bianchi 恒等重述 | 第11章 |
| I2 IEG 作用量 | $S_{\rm IEG}=S_{\rm EH}-\frac12\int(\nabla\rho)^2$ | S04 | 变分多出梯度项 | 第11章 |
| I3 泊松修正 | $\nabla^2\phi=4\pi G\rho_M-\rho_{\rm info}^{\rm excess}$ | S04-A3 | 牛顿方程+未定义修正 | 第11章 |

## B.4 高维紧致化公式（S05，含 H2 矛盾标注）

| 方程名 | LaTeX | 来源公设 | 推导步数 | 章节 |
|---|---|---|---|---|
| H1 | $M_{11}cL_{11}=2\pi\hbar$ | S05-A1 | 0 步公设 | 第12章 |
| **H2** | $R_{11}=(\hbar/2\pi)^{1/3}G^{1/3}c^{-2/3}$ | S05-A2 | **量纲疑 L·T⁻¹ᐟ³ 非长度；数值差 13 数量级，矛盾** | 第12/27章 |
| H3 | $M_{11}=M_p(2\pi)^{1/3}$ | S05 | 把已知 M_p 乘几何因子 | 第12章 |
| H4 | $G_4=G_{11}/(2\pi R_{11})$ | Kaluza-Klein | 标准约化，结构已证 | 第12章 |

## B.5 拓扑手征公式（S06/S09）

| 方程名 | LaTeX | 来源公设 | 推导步数 | 章节 |
|---|---|---|---|---|
| Cl(4,4) 复化 | $\mathrm{Cl}(4,4)\otimes\mathbb{C}\cong M_8(\mathbb{C})\oplus M_8(\mathbb{C})$ | S06-A1 | 代数恒等 | 第13章 |
| T1 计数 | $\pi_3(\mathrm{SU}(3))\times\mathbb{Z}_2^{\rm chiral}\to 3\times2=6$ | S06-A2 | 约 2 步（**12 vs 6 矛盾待修**） | 第13/27章 |
| T4 手征锁定 | $V_+\to(1/2,0),\ V_-\to(0,1/2)$ | S06 | 对应 V-A 结构 | 第13章 |
| T2 中微子 | $m_\nu=m_{\rm boundary}e^{-L_3/\xi}$ | S06-A3 | 参数未定义，待建模 | 第13章 |
| S09 定理1 | 三代 = SO(3) 三轴投影 | S09-A1 | 0 步（诠释层） | 第16章 |
| S09 定理2 | $\pi_3(\mathrm{SU}(3))\cong\mathbb{Z}\Rightarrow n\in\{1,2,3\}$ | S09-A2 | 数学事实 1 步，物理截断待建 | 第16章 |

## B.6 质量谱公式与失败记录（S09）

| 公式 | 理论值 | 实验值 | 偏差 | 章节 |
|---|---|---|---|---|
| $m_p/m_e=\alpha^{-3}$ | 2570 | 1836.15 | 差 40%（**失败**） | 第16/27章 |
| $m_p/m_e=6\pi^5/\alpha$ | — | 1836.15 | 差 2000%（**失败**） | 第16/27章 |
| 三代轻子比 $n/n^2/e^n$ | — | 206.77 / 3477.15 | 全错（**失败**） | 第16/27章 |
| $m_f=y_f v/\sqrt2$ | 13 个 y_f 无几何化 | — | 未解 | 第16章 |
| $L_{ij}=4\pi\hbar c E/\Delta m_{ij}^2$ | 标准式 | Δm²₁₂=7.53×10⁻⁵ eV² | 实验输入 | 第16章 |

## B.7 GMUFT 四自由度公式（S11）

| 方程名 | LaTeX | 来源公设 | 推导步数 | 章节 |
|---|---|---|---|---|
| 圆轨道 | $GM/r^2=r\omega^2\Rightarrow\omega=\sqrt{GM/r^3}$ | 牛顿+开普勒 | 2 步 | 第10章 |
| 曲率桥梁 | $\omega^2=(c^2/2)R_{\rm eff}$ | GR 弱场 | 唯象 R_eff | 第10章 |
| Lense-Thirring | $\omega_{\rm drag}=2GJ/(c^2r^3)\propto\Omega$ | GR 弱场 | 已知 | 第10章 |
| 对偶荷质比 | $Q/M=\sqrt{4\pi\varepsilon_0 G}=8.6175\times10^{-11}$ | 令 F_G=F_e | 不对应已知粒子，未解 | 第10章 |

## B.8 S13 六方程 M1–M6 全集与七定理

| 编号 | LaTeX | 来源公理 | 验证状态 | 章节 |
|---|---|---|---|---|
| M1 | $\sigma^\mu\partial_\mu\Psi=\lambda\Theta\Psi^*+\mathrm{i}\zeta\Psi$ | 公理一+最小一阶算子 | 流守恒 verified C0001 | 第18章 |
| M2 U(1) 联络 | $a_\mu=\frac{\mathrm i}{2}(\hat\Psi^\dagger\partial_\mu\hat\Psi-\partial_\mu\hat\Psi^\dagger\hat\Psi)$ | M1 归一化 | 结构已统一 | 第18章 |
| M2 对偶帧联络 | $\mathcal A_\mu=\mathcal E^\dagger\partial_\mu\mathcal E\in\mathfrak u(2)=\mathfrak{su}(2)\oplus\mathfrak u(1)$ | M1+酉帧 | 电弱自涌现 | 第18章 |
| M3 | $Q_H=\frac{1}{4\pi^2}\int\epsilon^{ijk}a_i\partial_j a_k\,d^3x\in\mathbb{Z}$ | π₃(S²)=ℤ | verified C0003 | 第18章 |
| M4 | $\mu\,dg/d\mu=\beta(g),\ \beta(-g)=-\beta(g)$ | 公理三 | 不动点 verified 实验三 | 第19章 |
| M5 | $g^{\rm eff}(r)=g^{\rm eff}(\ell^2/r)$ | 公理三 | 曲率有界 verified C0002 | 第19章 |
| M5 曲率上界 | $\lvert R\rvert_{\max}=(3+2\sqrt2)GM/(2\ell^3)$ | M5 | 解析 2.9142135624 vs 数值 2.9142135543 | 第19章 |
| M6 | $\frac{d}{dt}\int_\mathcal C\omega=\oint_{\partial\mathcal C}\Theta$ | M1+M5 | verified 实验八 | 第19章 |
| 希格斯质量 | $m_H=2\sqrt{2\tilde\kappa}\,v$（V1.3.1 修正 4√2 因子） | M1+真空约束 | verified C0004 | 第18章 |
| W/Z 质量 | $m_W=\tilde g v/2,\ m_Z=m_W/\cos\theta_W$ | M2 | 结构涌现 | 第18章 |

## B.9 推导索引说明

- 标注"恒等"的公式，推导步数为 1–2 步，本质是定义式重排，**不构成新物理**。
- 标注"测量锚"的公式，数值"符合"依赖 CODATA 反算，**不是前向预测**。
- 标注"矛盾"/"失败"/"待修"的公式，见第27章诚实档案。
- S13 的七定理证明链见 `13_论文与成果/书稿/` 第四卷 ch13。

## B.10 TUFT 动力学本征值路线公式索引（2026-09-19 追加）

> 本节为 TUFT 攻坚全量归一化合并追加，只追加不覆盖前文。数值照抄 SSOT v3.7（E1–E459 / 勘误 #35）。详见第十二编第65–67章。

| 方程名 | LaTeX | 来源 | 验证 | 章节 |
|---|---|---|---|---|
| TUFT 度规 | $A=e^{-2/\rho}$；$B=e^{2/\rho}(1+c_m/\rho^2+d/\rho^3)$，$c_m=-0.29$、$d=-0.05$ | 严格面积势（勘误 #22） | [A] | 第65章 |
| 反射壁 | $\rho_h=0.6099M$（$B=0$，$P=\rho^3+c_m\rho+d=0$） | sympy | [A] | 第65章 |
| 外垒 | $R=3.268M$；$V_{\max}=0.148709$；$\sqrt V=0.38563$ | 严格求导 | [A] | 第65章 |
| 龟坐标 | $ds/d\rho=\sqrt{B/A}$；$L=6.9694M$ | 积分 | [A] | 第65章 |
| 面积势 | $V=3A(1+e^{-2\lambda})/R^2$ | sympy 严格求导 | [A] | 第65章 |
| 近壁势展开 | $V=\frac13 s^{-2}-0.134590\,s^{-4/3}+O(s^{-2/3})$ | 无拟合平台+拟合双确认 | [A] | 第65章 |
| Frobenius 指标 | $\beta(\beta-1)=1/3\Rightarrow\beta=1.263762616$ | 代数 | [A] | 第65章 |
| GR 门禁基准 | $n_0=0.37367168441804166-0.08896231568893410i$（RW $s=-2$ $l=2$） | Leaver/Jansen | [A] | 第66章 |
| TUFT 基频极点 | $\omega=0.4344452-0.0564498i$；$\tau=17.7149M$ | Beyn+谱元两路互证 $6.97\times10^{-8}$ | [A] 谱通道 Grade A | 第66章 |
| 实频幺正 | $\||S|-1\|=6.66\times10^{-16}$ | IVP | [A]（恒等式解读 [B]，#31） | 第65/67章 |
| 群延迟拱峰 | $\omega^*=0.440$；$\tau_{\max}=33.9M$ | 复步长解析导数 | [A] | 第65章 |
| 外垒 S 矩阵隔离 | $\varepsilon=(1-\|r_b\|^2)^2=0.4557$ | 流守恒残差 $2.5e-10$ | [A] | 第65章 |
| Blaschke 极-零 | $S=C e^{ia(\omega-\omega_c)}(\omega-p^*)/(\omega-p)$；$p=0.43738-0.056724i$ | 拟合 RMS $3.36e-3$、$\|C\|=0.999994$ | [B] CONDITIONAL | 第67章 |

**口径**：谱通道 Grade A（第66章）与物理阻尼 CONDITIONAL/OPEN（第67章 D18）之别见 §B.10 注与 SSOT 勘误 #35；TUFT 物理四态 $35/61/18/27$ 不变。
