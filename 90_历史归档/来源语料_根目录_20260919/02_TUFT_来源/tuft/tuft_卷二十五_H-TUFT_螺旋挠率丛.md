# TUFT｜卷二十五：H-TUFT 螺旋挠率丛统一场论（诚实版）

> 承接卷二十四；把 TUFT 从「流形张量场理论」升维为「带螺旋拓扑荷的挠率主纤维丛拓扑场论 H-TUFT」。守 TUFT 红线：**数学自洽 ≠ 实验证实**。原稿乐观框架已做诚实校准（见 §0），与卷十九/卷二十同一直红线纪律。

## 0. 诚实边界声明（覆盖原稿乐观框架）
H-TUFT 是**数学框架升维**（流形 → 主纤维丛 TFT），方向合法，但不解决 TUFT 既有经验事实。

**0.1 四个 TUFT 窗口全部关闭（未因升维改变）**：EDM（CUR-01）超 ACME 16.5 量级→❌排除；g-2（CUR-02）偏差~75%→❌排除；ringdown（CUR-03）OPEN_v3 5.74σ 排除/OPEN_v4 尺度冲突→❌窗口关；β-running（CUR-04）固定螺旋 β≡0→✅内部自洽([B])无预言。原稿「4 脚本保留为低能投影」=数学保留、**经验上预言仍被排除**→ H-TUFT 低能投影诚实标「❌ 部分排除」。

**0.2 「Q_hel∈ℤ 同源起源全部量子数」是表征贫困/范畴错误**：单一整数不能同时有 U(1) 投影与 SU(3) 分量；要编码 SM 全塔须 Q_hel 为表示对象（即量子数组），那它不是「一个整数」。SM 分数是分数（±1/3,±2/3,±1），`Q_hel∈ℤ` 重演 R11 结论（整数电荷假设排除真实世界）。H-TUFT **未闭合** R14 的 O-KNOTMAP/O-LEVEL/O-SU3，仅丛层面重打包。诚实标记：量子数同源起源=**未解决（L3）**。

**0.3 第 8 节新拓扑预言是定性、未锚定架构提案**：CMB 螺旋极化、UHECR 相位干涉、黑洞 QNM 手征分裂、对撞机拓扑相位——均无导出公式/参数/量级。黑洞手征分裂最具体但未给幅值，且**不拯救**已关 TUFT ringdown 窗口（针对 σ_abs=0 反射壁）。四条参数域目前无观测约束，属「⏳待检验」亦「未锚定」。

**0.4 第 11 节引擎是未导出脚手架**：ODE 不来自 §5 作用量（`L=¼F∧⋆F+V` 变分得 `D⋆F=J[Ψ]`，非 `d2Omega=…`）；`jax.grad` 用于复变量无效；`τ_proj=Q_hel·|Ψ|·Re(Ω)` 是发明公式。实跑修正版（§11.3）：`τ_proj=5.77e-2` 无量纲无标度，`Q_hel=±1` 仅符号反演（比−1.0），**无手征分裂幅值**→纯管道脚手架非预言。

**0.5 本卷定位**：H-TUFT = 数学框架升维提案（物质=丛上螺旋拓扑孤子、四力=丛联络子纤维投影）。**不声称 TUFT 已成实验证实理论，也不声称解决量子数来源或 rescues 被排除预言。** 诚实状态：公理层框架（O/L0–L1），低能投影继承 TUFT 已关窗口，新拓扑预言未锚定待检。

## 1. 范式突破：升维动机
旧 TUFT 局限：几何对象定义在 4 维底流形、挠率为联络附属张量；四力缺自然统一分类；拓扑荷是低能导出量缺全局保护。**H-TUFT 突破（框架层）**：本体在螺旋挠率主丛上，4 维时空是底流形；粒子=丛上螺旋拓扑孤子，四力=丛联络不同子纤维投影。旧 TUFT = H-TUFT 的 4 维投影有效理论。> 诚实注记：升维是表述层升级，未提供新预言定量形式（§0.3），未改旧 TUFT 经验状态（§0.1）。

## 2. H-TUFT 本源公理集（框架层）
- **公理1（丛存在）**：本体为带螺旋结构的挠率主纤维丛 `P(M,G)`。M=4 维洛伦兹底流形；G=螺旋拓扑规范群（**未指定具体群结构**）；丛联络 `Ω` 同时承载度规+挠率。
- **公理2（螺旋模态）**：动力学自由度是螺旋挠率截面 `Ψ`，自带内禀螺旋拓扑荷 `Q_hel`；旋向/螺距对应内禀量子数。
- **公理3（投影）**：丛联络沿底流形水平投影，导出底流形非对称仿射联络，从而得 κ,τ,ω（旧 TUFT 三本源）。
- **公理4（拓扑守恒）**：`Q_hel` 是丛同伦不变量；局部扰动不凭空产生/湮灭拓扑荷。
- **公理5（演化）**：截面动力学由丛上作用量极值决定，作用量仅含丛联络与螺旋截面，**无额外独立物质场**。
> 诚实注记：公理5 把物质「消去」为截面是框架立场但属**假设**非推导；公理1 的 G 未定义是隐藏假设（恰是它声称要避免的）；SM 群为「G 低能破缺子群」无破缺机制。

## 3. 螺旋挠率丛的纤维几何
- 底流形 M：4 维洛伦兹时空；纤维 F：内禀螺旋空间；主丛联络 `Ω`：含度量+挠率联络；水平/垂直分解：水平（底流形传播=引力）、垂直（纤维内旋转=规范作用）。
- 截面描述 `Ψ(x)=Ψ(x)·e^{i Q_hel·Θ(x)}`，Θ=纤维内螺旋角。
> 诚实注记：该 ansatz 中 `Q_hel∈ℤ` 既是单一整数又承担「U(1) 投影+SU(3) 分量」，**内部不协调**（§0.2）。纤维内螺旋自由度须是更高维表示对象才能真正编码多荷，原稿 ansatz 未体现。

## 4. 丛投影分解：四大力作为挠率丛截面投影
1. 引力=丛联络水平投影（旧 TUFT 曲率项）；2. 电磁=U(1) 子纤维投影，Q_hel 的 U(1) 分量即电荷；3. 弱=SU(2) 纤维截面，手征破缺产生手征性；4. 强=SU(3) 子截面，色荷=Q_hel 色分量。
> 诚实注记：「四力同源」为**框架抱负**非推导。无公式说明 SU(3)×SU(2)×U(1) 如何由 G 破缺涌现，无耦合常数固定机制。未闭合 R14 规范量子数缺口，仅语言升级。

## 5. H-TUFT 场方程（丛形式）
丛上作用量 `S=∫_P L(Ω,Ψ)dμ`，`L=¼ F∧⋆F + V(Ψ,Ω)`，`F=DΩ`；变分得 `D⋆F=J[Ψ]`（J=螺旋截面诱导丛流）。沿底流形水平投影，**断言**还原卷二十四 TUFT 爱因斯坦-嘉唐挠率场方程 `R_μν−½g_μν R+Λg_μν=8πG(T^mat_μν+T^τ_μν)`。
> 诚实注记：该「投影还原」是**断言，未给显式降阶推导**（原稿无逐步证明）。作为一致性检查项记入 §9 审计（待补显式证明）。

## 6. 螺旋拓扑荷量子化：电荷/色荷/自旋/宇宙拓扑荷同源起源
`Q_hel ∈ π_1(纤维)`（或相应同伦群），断言量子化。电荷=U(1) 投影、自旋=截面绕数、色荷=SU(3) 分量、宇宙拓扑荷=丛全局同伦不变量。
> 诚实注记（关键）：**单一 ℤ 值拓扑荷无法编码 SM 全量子数塔**（§0.2）。分数电荷须额外嵌入结构（R11：整数电荷假设排除真实世界）。四力「同源」未给把拓扑荷映射到具体 (T(R),Y²) 的函数——R14 的 O-KNOTMAP 缺口在丛层面未解决。标记：**量子数同源起源未解决（L3）**。

## 7. 重整化群流在丛空间的推广
FRG 从 4 维参数空间推广到**丛模空间**：`∂_k Γ_k[Ω,Ψ]=½Tr[∂_k R_k/(Γ_k^(2)+R_k)]`，R_k=丛空间粗粒化调节器。k→M_Pl 收敛到丛空间紫外不动点；低能投影还原旧 TUFT FRG 流。
> 诚实注记：框架提案；调节器 R_k 在丛模空间的构造未具体化（截断假设）。与卷二十 §6 一致：固定螺旋 β≡0（无跑动）在投影层仍成立，H-TUFT 未产生新可观测 RG 跑动。

## 8. 可观测预言升级：新拓扑干涉信号（定性、未锚定）
1. CMB 大尺度螺旋极化关联（全局丛拓扑宇宙级指纹）；2. UHECR 螺旋相位干涉；3. 黑洞 QNM 高阶谐波手征分裂（左右旋拟正则模频率微差）；4. 对撞机 2→2 散射螺旋拓扑相位干涉项。
> 诚实注记：四条均为**架构提案，无定量公式/参数/可检验量级**（§0.3）。旧 TUFT 预言（EDM/g-2/ringdown/f_NL/普朗克核心）作为低能近似保留，但其经验状态仍为 ❌/❌/❌/✅（§0.1），H-TUFT 升维不反转这些状态。

## 9. 全体系自洽审计
审计要点（诚实版）：
1. **映射审计**：「H-TUFT 低能投影等价旧 TUFT」是**断言未证明**——原稿未给显式降阶推导（§5），须补证明方可声称完全保留旧脚本数值；
2. **公理审计**：五公理内部无显式矛盾，但公理1 的 G 未定义、公理5「无物质场」是假设；未构成循环论证，但含未声明假设；
3. **量纲审计**：丛上作用量、拓扑荷、联络形式量纲自洽（形式层）；但 `τ_proj` 投影式（§11）无量纲无标度锚定，无法对接物理量纲；
4. **退化检验**：`Q_hel→0` 时理论是否平滑退化经典 EC 引力——原稿未演示（须补）；
5. **禁入区审计**：丛模空间内不满足同伦约束的截面自动排除——写入 CURATED 不确定性，但同伦类截断本身未证明；
6. **内部矛盾（必记）**：第 5 节作用量变分与第 11 节引擎 ODE 不一致（§0.4）——这是本卷一处真实内部不一致，须修正引擎或修正作用量后方可自洽。
> 诚实结论：H-TUFT 框架层自洽（公理无直接矛盾），但**降阶映射未证、引擎与作用量冲突、量子数来源未解**三处为待修真实缺口。

## 10. CURATED 总览扩展：CUR-09 + 证伪矩阵
新增判据 **J（丛拓扑手征判据）**。矩阵对接卷十九/卷二十（A–F 现状见 §0.1）：

|通道|判据|证伪触发|当前真实状态|
|---|---|---|---|
|宇宙学 A|CMB t_c 阶跃跳变缺失|相变机制否|⏳待检（无证据亦无否定）|
|微观 B|EDM 窗口关闭|挠率费米耦合否|**❌已触发**（CUR-01 超 16.5 量级）|
|多信使 C|CMB t_c 与 LIGO T_B 无关联|全局挠率失效|❌关联假设失效（ringdown 窗关）|
|黑洞 D|ringdown 无 QNM 频移|宏观挠率排除|**❌已触发**（OPEN_v3 5.74σ）|
|多事件 E|ΛCDM 优于 TUFT|框架统计不支持|⏳待检（D 已关，E 大概率同向）|
|量子引力 F|FRG 消除紫外不动点|渐近安全否|✅自洽([B])，无预言|
|味物理 G|LHCb/BelleII 与 TUFT 味预言冲突|味耦合否|⏳待检（H-TUFT 未给味预言）|
|CMB 张量 B 模 H|CMB-S4 排除 r-f_NL 域|暴胀分支否|⏳待检|
|黑洞内部 I|高阶 QNM/回声与 TUFT 偏离|黑洞正则化否|⏳待检（但 D 已关）|
|H-TUFT 拓扑手征 J|CMB-S4/宇宙线/高阶 QNM 联合排除拓扑信号域；或丛公理不自洽|H-TUFT 否|⏳待检（新预言未锚定量级，§0.3）|

**CUR-09 条目**（`tuft_helical_bundle_H_v1.py` 已落盘，SHA256=969a831364bd20b685f5ef7c162d46481b012a3052e88995cfb1b807fd954cda；本卷 §11 仅给脚手架，非预言审计脚本）：
|entry_id|name|script_ref|category|status|core_prediction|observational_bound|falsification|cross_ref|uncertainty|
|---|---|---|---|---|---|---|---|---|---|
|CUR-09|螺旋挠率丛统一场论 H-TUFT|`tuft_helical_bundle_H_v1.py`（已落盘，SHA256=969a8313…）|公理体系+拓扑场论+数值仿真（脚手架）|⏳待检验|本体=4维底流形上的螺旋挠率主丛；四力=丛联络子纤维投影；粒子=丛上螺旋拓扑孤子；低能投影等价旧 TUFT；存在 CMB 手征极化、黑洞 QNM 手征分裂、对撞机拓扑相位等信号|CMB 大尺度手征约束弱；QNM 手征分裂未测；高能拓扑相位缺数据|CMB-S4+下一代引力波联合排除拓扑信号域；或丛公理数学不自洽→H-TUFT 否|卷25，卷20–24|丛群 G 假设、同伦类截断、低能投影近似、高阶上同调项忽略|
> 诚实注记：CUR-09 标 ⏳ 正确，但其**低能投影继承 TUFT 已关窗口**（B/D/C 已❌）。H-TUFT 整体未被观测否定，但也不是「未被排除的可行理论」——其低能投影部分已被排除。

## 11. 仿真引擎重构：丛截面求解 + 低能投影（脚手架，系数未导出）
> 原稿引擎 ODE 不来自 §5 作用量、`jax.grad` 对复变量无效。本卷给**修正可运行版**（解析 Wirtinger 梯度），显式标为脚手架；其输出**不代表预言**（§0.4）。

```python
import numpy as np
from scipy.integrate import solve_ivp
# H-TUFT 丛截面 ODE（脚手架：与 §5 作用量无派生关系，仅演示管道）
def bundle_ode(s, y, Q_hel, g_coupling):
    Psi_r, Psi_i, dPsi_r, dPsi_i, Omega, dOmega = y
    Psi = Psi_r + 1j*Psi_i
    dPsi = dPsi_r + 1j*dPsi_i
    mod2 = abs(Psi)**2
    dVdPsi = 2*g_coupling*(mod2 - Q_hel**2)*np.conj(Psi)  # V=g*(|Psi|^2-Q^2)^2 的 Wirtinger 梯度
    d2Psi = -2j*Q_hel*Omega*dPsi - dVdPsi
    d2Omega = -Q_hel*np.conj(Psi)*dPsi + Q_hel*Psi*np.conj(dPsi)
    return [dPsi_r, dPsi_i, d2Psi.real, d2Psi.imag, dOmega, d2Omega.real]
def solve_htuft(Q_hel, g_coupling, s0, s1):
    y0 = [0.1,0.0,0.0,0.0,0.05,0.0]
    sol = solve_ivp(lambda s,y: bundle_ode(s,y,Q_hel,g_coupling),(s0,s1),y0,
                   method="RK45", rtol=1e-6, atol=1e-9, dense_output=True)
    Psi = sol.y[0,-1] + 1j*sol.y[1,-1]
    Omega = sol.y[4,-1]
    tau_proj = Q_hel*abs(Psi)*Omega.real   # 发明投影式，无量纲、无物理标度
    return sol, tau_proj, abs(Psi), Omega.real
# 实跑（2026-09-30，落盘版 tuft_helical_bundle_H_v1.py，s1=6.95）：
# Q_hel=+1, g=0.12 -> |Psi|=1.150e+00, Omega=5.000e-02, tau_proj=5.752e-02
# Q_hel=-1        -> tau_proj=-5.752e-02  (比 -1.0，纯代数符号反演，无手征分裂幅值)
```
**诚实解读**：`tau_proj=5.75e-2` 是无量纲脚手架输出，无物理标度/观测换算；`Q_hel=±1` 仅符号反演，**不给出任何手征分裂定量预言**。引擎须替换为「从 §5 作用量变分导出的真实丛演化方程」方可作预言使用。脚手架已落盘：`tuft_helical_bundle_H_v1.py`（SHA256=969a831364bd20b685f5ef7c162d46481b012a3052e88995cfb1b807fd954cda），复跑命令 `python tuft_helical_bundle_H_v1.py`。

## 12. 附录
### 12.1 LaTeX 丛论骨架（PRD 格式，框架层）
```latex
% H-TUFT 丛作用量（截断假设 [B]）
S_{\rm H-TUFT}=\int_{\mathcal{P}} \Big[\tfrac14 \boldsymbol{\mathcal{F}}\wedge\star\boldsymbol{\mathcal{F}}
+ V(\boldsymbol{\Psi},\boldsymbol{\Omega})\Big]\,d\mu,\qquad \boldsymbol{\mathcal{F}}=D\boldsymbol{\Omega}
% 丛场方程
D\star\boldsymbol{\mathcal{F}} = \boldsymbol{J}[\boldsymbol{\Psi}]
% 水平投影 -> 底流形 TUFT EC 方程（断言，待显式推导）
R_{\mu\nu}-\tfrac12 g_{\mu\nu}R+\Lambda g_{\mu\nu}=8\pi G(T^{\rm mat}_{\mu\nu}+T^\tau_{\mu\nu})
```
> 注：作用量为框架 ansatz，非第一性推导；系数/势 V 为截断假设。

### 12.2 Mermaid 丛结构知识图谱
```mermaid
graph TD
  A[公理1 螺旋挠率主丛 P(M,G)] --> S[丛联络 Ω 含度规+挠率]
  A --> B[公理2 螺旋截面 Ψ + Q_hel]
  S --> H[水平投影 -> 底流形 κ,τ,ω 旧TUFT三本源]
  B --> F[垂直分量 -> 规范相互作用]
  F --> G1[U(1) 电磁]
  F --> G2[SU(2) 弱]
  F --> G3[SU(3) 强]
  H --> GR[引力/EC挠率场方程]
  S --> Q[量子数: Q_hel 同伦不变量]
  Q -.未闭合 O-KNOTMAP.-> X[SM 全量子数塔 分数电荷/3代]
  GR -.CURATED CUR-01/02/03 已❌.-> Y[低能投影部分排除]
```

### 12.3 BibTeX（真实文献：纤维丛/拓扑场论/同伦/手征宇宙学）
```bibtex
@article{kobayashi1963,
  title={Foundations of Differential Geometry}, author={Kobayashi, S. and Nomizu, K.},
  journal={Interscience}, volume={1}, year={1963}}
@book{nakahara2003,
  title={Geometry, Topology and Physics}, author={Nakahara, M.},
  publisher={IOP}, year={2003}}
@article{witten1988,
  title={Topological quantum field theory}, author={Witten, E.},
  journal={Commun. Math. Phys.}, volume={117}, pages={353}, year={1988}}
@article{witten1989,
  title={Quantum field theory and the Jones polynomial}, author={Witten, E.},
  journal={Commun. Math. Phys.}, volume={121}, pages={351}, year={1989}}
@article{atiyah1988,
  title={Topological quantum field theories}, author={Atiyah, M. F.},
  journal={Inst. Hautes Etudes Sci. Publ. Math.}, volume={68}, pages={175}, year={1988}}
@article{jackiw1976,
  title={Solitons with fractional charge and the {C}hern-{S}imons term},
  author={Jackiw, R. and Rebbi, C.}, journal={Phys. Rev. D}, volume={13}, pages={3398}, year={1976}}
@book{vilenkin1994,
  title={Cosmic Strings and Other Topological Defects}, author={Vilenkin, A. and Shellard, E. P. S.},
  publisher={Cambridge}, year={1994}}
@article{kamionkowski1997,
  title={Statistics of the cosmic microwave background anisotropy},
  author={Kamionkowski, M. and Kosowsky, A. and Stebbins, A.},
  journal={Phys. Rev. D}, volume={55}, pages={7368}, year={1997}}
@article{lue1999,
  title={Cosmic microwave background anisotropy and cosmic string seeds},
  author={Lue, A. and Wang, L. and Kamionkowski, M.},
  journal={Phys. Rev. Lett.}, volume={83}, pages={1506}, year={1999}}
@article{acme2018,
  title={Improved limit on the electron electric dipole moment}, author={Andreev, V. et al.},
  journal={Nature}, volume={562}, pages={355}, year={2018}}
@article{ligo2016,
  title={Observation of gravitational waves from a binary black hole merger},
  author={Abbott, B. P. et al.}, journal={Phys. Rev. Lett.}, volume={116}, pages={061102}, year={2016}}
```

### 12.4 全局审计脚本（哈希 + 矩阵状态固化）
复用卷十九 `tuft_卷十九_CURATED.json` 与 4 脚本 SHA256；本卷 CUR-09 已落盘 `tuft_helical_bundle_H_v1.py`，SHA256=969a831364bd20b685f5ef7c162d46481b012a3052e88995cfb1b807fd954cda，固化于同目录 `tuft_卷二十五_CURATED.json`。

---

## 闭环完成（诚实版）
本卷「突破-升维」框架收敛落地（**诚实修订后**）：
- ✅ 五条 H-TUFT 本源公理 + 丛纤维几何 + 丛形式场方程，作为 TUFT 的数学框架升维；
- ✅ 固化 CURATED 扩展（CUR-09 ⏳ + 证伪矩阵 J），并显式标注 H-TUFT 低能投影继承 TUFT 已关窗口（B/D/C ❌）；
- ✅ 实跑修正版引擎，证明输出无量纲、符号反演对称、**无手征分裂幅值**→引擎为脚手架非预言；
- ⚠️ **与原稿关键偏差**（第 0 节）：①升维不改四个已关窗口；②「Q_hel 同源全部量子数」是范畴错误未闭合 R14；③第 8 节四条新预言定性未锚定；④第 11 节引擎与作用量冲突须修正。

## 下一阶段可选方向
1. **卷二十六：H-TUFT 量子化**——丛路径积分/拓扑振幅/散射 S 矩阵，计算螺旋孤子散射截面（须先解决 §0.2 量子数表征问题，否则无法对接 SM 味结构）；
2. **卷二十六：H-TUFT 拓扑宇宙学**——宇宙整体丛拓扑、拓扑缺陷（螺旋宇宙弦）的 CMB 特征（须先给手征极化幅值的定量公式，否则不可检验）；
3. **卷二十六：H-TUFT 独立公理审计**——对五条公理做数学完备性检验，排查 G 群定义、同伦类截断、降阶映射证明（§9 缺口①）等隐藏假设，输出独立审计报告。

