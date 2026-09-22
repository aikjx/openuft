# 附录 B 验证脚本与重跑方法

## B.1 脚本清单

全部脚本位于 `D:\a10\aikjx\code\my_lib\`，与本书配套，可原样运行（Python 3.14.7 + numpy 2.5.2 验证）。

| 脚本 | 覆盖章节 | 实验 |
|---|---|---|
| `verify_unified_theory.py` | 第12/14章 | 实验一–八（流守恒、β、分形、度规、曲率、畴） |
| `diagnose_winding.py` | 第15章 | 实验九诊断（绕数崩溃、$\int J^{0}$、$\lambda=0$ 对照） |
| `hopf_verify.py` | 第7/14章 | 实验十/十一（霍普夫荷收敛、整数谱、形变保护） |
| `hopf_control.py` | 第7/15章 | 实验十二对照（平方映射高分辨率、自由场 3D 不保护） |
| `higgs_verify.py` | 第8/14章 | 实验十三–十五（对偶帧酉性、模式谱、未破缺 $U(1)$） |
| `dimension_unify_verify.py` | 第17/19/20章 | 验证A–E（量纲谱、参数自洽、常数比例、依赖图可达性、四重归一化） |
| `yang_mills_verify.py` | 第21章 | 验证A–D（联络结构、几何曲率、格点规范不变性、希格斯–金哈质量谱） |

## B.2 重跑命令

【 **核心体系** :`python verify_unified_theory.py`——输出实验一至八全部数据。】

【 **反证诊断** :`python diagnose_winding.py`——输出绕数崩溃时刻、$\int J^{0}$ 守恒、$\lambda = 0$ 对照（$Q = 0.998$ 恒定）。】

【 **霍普夫荷** :`python hopf_verify.py`——盒尺寸收敛（$0.9028 \to 0.9683$）、平方映射 $Q_{H} \approx 3.79$、形变 $\Delta Q$、3D 动力学（$+0.875 \to -0.162$）。】

【 **对照实验** :`python hopf_control.py`——高分辨率平方映射 $Q_{H} \approx 3.89$、自由场 3D $Q_{H} \to -0.271$。】

【 **希格斯突破** :`python higgs_verify.py`——对偶帧酉性 $8.9\times10^{-16}$、三真空点谱 $[0,0,0,8]$、零空间维数 $1$。】

【 **量纲·归一化·全关联** :`python dimension_unify_verify.py`——量纲谱（$\ell^{n}$ 表）、参数归约自洽（$m_{H}$ 双路一致 $0$/$2.2\times10^{-16}$）、常数比例 $m_{H}/m_{W} = 4\sqrt{2}\sqrt{\tilde{\kappa}}/\tilde{g}$（V1.3.1 统一 $\tau/2$ 口径）、依赖图"公理全可达+零环"、四重归一化残差（场 $5.6\times10^{-16}$、度规 $3.3\times10^{-16}$）。】

【 **口径闭合（V1.3.1 新增）** :`python consistency_verify.py`——三项数值验证全过：① 弱混合角 $e = \tilde{g}\sin\theta_{W} = \tilde{g}'\cos\theta_{W}$ 差 $5.6\times10^{-17}$、$m_{Z} = m_{W}/\cos\theta_{W}$ 差 $0$；② 新口径 $m_{H}/m_{W} = 4\sqrt{2}\sqrt{\tilde{\kappa}}/\tilde{g}$ 与质量值精确一致；③ 四观测 $\left\{ m_{W}, m_{Z}, m_{H}, \alpha \right\}$ 反解四未知 $\left\{ v, \tilde{g}, \tilde{g}', \tilde{\kappa} \right\}$ 三组随机参数最大误差 $\sim10^{-16}$——参数系统完全钉死，无多余自由度。】

【 **拼图二·代结构（V1.4 新增）** :`python fermion_family_verify.py`——验证A：$\mathbb{Z}_{4}$ 实不可约表示 Frobenius–Schur 指标 $+1, 0, +1, 0$ → 三实表示（$1, 1, 2$ 维）；验证B：每代六反常（$\left[ SU(3) \right]^{3}$、$\left[ SU(2) \right]^{3}$、$\left[ SU(3) \right]^{2}U(1)$、$\left[ SU(2) \right]^{2}U(1)$、$U(1)^{3}$、$\mathrm{grav}^{2}U(1)$）全部精确消去；验证C：二维实表示生成元 $J^{2} = -I$（内部复结构）；验证D：无第四实表示——第四代被表示论禁戒。全过。】

【 **拼图三·色 SU(3)（V1.5 新增）** :`python color_su3_verify.py`——验证A：$\mathfrak{su}(3)$ 李代数（8 生成元、$f^{abc}$ 全反对称、Jacobi 残差 $3.3\times10^{-16}$、秩 2）；验证B：$\mathbb{CP}^{2}$ 的 $SU(3)$ 等距（Fubini–Study 距离不变 $3.3\times10^{-16}$）+ 稳定子 $U(2)$（200/200）；验证C：色单态判据 $k \equiv l \pmod 3$（介子 1/重子 1/四夸克 2/双夸克 0/五夸克 3/反重子 1，生成元共同核机器精度）；验证D：$\mathbf{3}\big|_{SU(2) \times U(1)} = \mathbf{2} \oplus \mathbf{1}$（超荷比例 $1/3, 1/3, -2/3$）；验证E：$S^{5} \to \mathbb{CP}^{2}$ 纤维化（纤维 $S^{1}$）。全过（数学确定部分；禁闭 OPEN）。】

【 **量子化层（V1.6 新增）** :`python quantum_brst_verify.py`——验证A：BRST 幂零 $s^{2}A = s^{2}c = 0$（格拉斯曼矩阵表示，残差精确 $0$）；验证B：单圈 $\beta$ 系数 $b_{0}$（$SU(3)$ 纯规范 11，$n_{f}=6$ 时 7）；验证C：$\beta\left( -g \right) = -\beta\left( g \right)$ 精确成立（第9章公理的量子层对应）；验证D：渐近自由窗口 $n_{f} \le 16$。全过（形式化层；质量间隙 OPEN）。】

【 **拼图四·常数统一（V1.6 新增）** :`python constant_unify_verify.py`——验证A：参数对接（PDG 常数 → $\left\{ v, \tilde{g}, \tilde{g}', \tilde{\kappa} \right\}$，回代 $m_{Z}$ 差 $0.53\%$ = 跑动）；验证B：电荷量子化（介子/重子电荷全整数，机器枚举）；验证C：$\pm 1/3$ 分数化（$\lambda_{8}$ 谱）；验证D：$\sin^{2}\theta_{W} = 1/4$ 树级候选预言（$\mathbb{CP}^{2}$ 稳定子嵌入，vs 实验 $0.231$）；验证E：$\Lambda$ 差距 $10^{122}$ 如实 OPEN。部分通过。】

【 **统一跑动检验（V1.7 新增）** :`python running_unify_verify.py`——验证A：$M_{Z}$ 处三规范耦合（GUT 归一化）；验证B：SM 单圈三线不汇聚（差距 $13.1\%$，标准结论）；验证C：CP² 候选 $\sin^{2}\theta = 1/4$ 跑动检验（电弱尺度差 $5.4\%$，唯一尺度 $3.7$ TeV 无出处——负面结果如实）；验证D：MSSM 对照（统一 $M \approx 2\times10^{16}$ GeV、$\alpha_{GUT} \approx 1/24$、真预测 $\sin^{2}\theta_{W}(M_{Z}) = 0.2309$ vs $0.23122$，差 $0.12\%$——对偶周期四↔超对称的候选锚点）；验证E：判定与边界。全过。】

【 **动力学作用量（拼图一）** :`python yang_mills_verify.py`——联络反厄米性 $1.9\times10^{-5}$；霍普夫几何曲率 $\max|b| = 7.82$；plaquette 规范不变性相对差 $1.18\times10^{-16}$；质量谱 $[0, 0.0625, 0.0625, 0.085]$ 与 $\{0, m_{W}^{2}, m_{W}^{2}, m_{Z}^{2}\}$ 精确一致。】

## B.2b v8–v15 反射壁/QNM 精算脚本（v15 回写新增）

【 **说明** :以下脚本与本书主体环境（Python 3.14.7）不同，跑在 `D:\a10\aikjx\code\my_lib\.venv\Scripts\python.exe`（Python 3.12.9 + mpmath/scipy）。它们对应第14章实验十六–二十一与第15章三轮否定定理；联盟脚本与 MainAgent 独立审计脚本分列，**结论以独立复算为准**。】

| 脚本 | 覆盖实验 | 期望输出对照 |
|---|---|---|
| `tuft_v10_*.py` / `_ma_v10_indep_scalar.py` | 实验十六 | 标量 $s=0$ 三模 55 位：$0.1104549391-0.1048957171i$ 等，与 qnm 库一致 |
| `tuft_v12_line1_rw.py` / `_ma_v12_indep_rw.py` | 实验十七 | 引力 $s=-2$ $l=2$ $n=0$ $0.37367168441804166-0.08896231568893410i$（14 位） |
| `tuft_v13_*.py` / `_ma_v13_indep_audit.py` | 实验十八 + 第15章 15.6 | 联盟 6 壁根随 $s_{out}$ 漂移；独立审计示 GR 上不收敛（E359/#18） |
| `tuft_v14_*.py` / `_ma_v14_indep_audit.py` | 第15章 15.7 | 向内积分 GR 上 $1.2$–$2.6$ 漂根；两外推根系垒顶散射簇（E365/#19） |
| `_ma_v15_hp_gate1/2/3.py` | 第15章 15.8 | 45 位三闸：稳定错误根 $0.414499-0.183171i$、真值种子牛顿仍错 $0.669936-0.063684i$ |
| `_ma_v15_real_phase.py` | 实验十九/二十一 | 实频 IVP 机器精度 $\||r|-1\|\le1.1\times10^{-16}$、flux$\equiv0$、无窄壁腔线 |
| `_audit_v15_real_phase_indep.py`（输出 `_out.txt`） | 实验二十 | dps=45、63 点、$h=0.02$：$\||r|-1\|\le8.8\times10^{-47}$；$\arg r=-1.559\to-1.571$ 平坦 |
| `_diag_phase_convention.py` | 第15/14章相位分歧裁决 | organizer 独立 float64 诊断复现原始相位表（$s_{out}=80/120$ 差 $0.003$–$0.02$） |

【 **重跑命令与判定** :用 `.venv` 的 Python 逐脚本运行；**期望输出不是"根收敛得漂亮"**——实验十九/二十要的是 $\||r|-1\|$ 与 flux 的机器精度零；`_ma_v13/v14/v15_*` 要的正是"在 GR 已知答案上不收敛/收敛到错误根"这一**否定性**输出，出现它说明方法复现了事故，不是故障。详细延迟/可观测性数值已随势修正降级（勘误 #20–#22），以主册最新口径为准。】

## B.2c v19 三子任务脚本（v19 收口新增，E430–E432）

【 **说明** :以下三个脚本跑在同一 `.venv`（Python 3.12.9 + mpmath dps=40 + scipy），对应第14章实验二十二/二十三/二十四与第15章 §15.9；原始输出同名 `_out.txt`，数字 organizer 已抽查照抄。】

| 脚本（+同名 `_out.txt`） | 覆盖实验/定理 | 期望输出对照 |
|---|---|---|
| `_v19_series_matcher.py` | 实验二十二 / 第15章 §15.9（E430 否定） | 两端级数/Wronskian 匹配 dps=40：已知真根处 $W(s_m=2.4)=-6.29-2.13i\neq0$；粗糙初值 Newton 残差 577；scipy DOP853 伪根 $0.370744-0.050913i$；加深边界 $-25/40\to-100/150$ 虚部卡 $-0.04\sim-0.055$（**要的就是"GR 门 FAIL"这一否定输出**） |
| `_v19_ringdown_snr.py` | 实验二十三（E431 条件 MEASURABLE） | 时域注入 $\varepsilon=|R_B|=0.729$：表观 FFT 峰 GR $0.365\to$ TUFT $0.318$（$\delta\omega_r/\omega_r=-12.9412\%$）；表观 $\tau_d$ $10.58\to35.81M$；$\rho_{\mathrm{frac}}=0.814790$；理论最优区分 SNR≈1.23；O4 9.8→3.5 Gpc / Voy 3.2× |
| `_v19_tau_complex.py` | 实验二十四（E432） | 复步长 $h=10^{-5}$：TUFT $\|R\|^2=1$ 全频、$\tau$ 拱峰 $\omega^\*=0.440$/$\tau_{\max}=33.906M$、高频尾 $0.94\to2.04M$；GR 门 FAIL（$0$ 位，$\|D\|\approx1.89\times10^{-5}$ 地板） |

【 **重跑命令与判定** :与 B.2b 同环境。`_v19_series_matcher.py` 的"正确"输出是**不收敛到 GR 真根**（否定性复现 v15 gate1/gate3）；`_v19_ringdown_snr.py` 的表观 $\delta\omega/\delta\tau$ 须与 **ε 处方 caveat** 一起读（$\varepsilon=0.729$ 垒顶反射幅系理论上界，严格双程穿垒 $|T_B|^2\approx0.22$）；`_v19_tau_complex.py` 的 TUFT $\tau$ 数值稳定、GR 侧不收敛（待 Leaver 连分数）。】

## B.2d v20 两数值子任务脚本（E443/E444）

【 **环境（v20）** :同 B.2c（`.venv`，Python 3.12.9 + mpmath dps=45 + scipy）。两脚本均独立重写、不引用联盟旧码；原始输出同名 `_out.txt`，数字 organizer 已抽查照抄。】

| 脚本（+同名 `_out.txt`） | 覆盖实验/定理 | 期望输出对照 |
|---|---|---|
| `_v20_mixed_bc_spectrum.py` | 实验二十五 / 第15章 §15.10（E443） | ① GR 门硬资产 dps=45：RW $s=-2$ $n0$ $0.37367168441804-0.08896231568894i$（15 位，$1.6\times10^{-15}$）、$n1$ 14 位（$8\times10^{-14}$）、标量 $s=0,l=0$ 11 位（$3.1\times10^{-11}$）；② TUFT 几何 $\rho_h=0.6099$/外垒 $\sqrt{V_{\max}}=0.3854@R\approx3.27$/$L\approx6.97M$；③ 有限盒自证门 $|\det M(w^\*)|=2.0\times10^{-8}(N=12)\to4.4\times10^{-7}(N=20)$ 随 $N$ 增大非趋零（**要的就是"自证门 FAIL"这一否定输出**，不报 TUFT 根） |
| `_v20_virtual_waveguide_snr.py` | 实验二十六（E444 条件/临界） | 反事实公设：核侧 $V=0$ 虚拟平坦波导、仅留外垒真实势；流守恒残差 max $2.5\times10^{-10}$、互易残差 max $9.0\times10^{-10}$；GR 隔离门 @0.3737=0.53135；TUFT $|r_b|^2@0.3737=0.3250$；严格双程 $\varepsilon=(1-|r_b|^2)^2=0.4557$；条件 SNR $Q=2.10$、$\rho(60M_\odot,1\,\mathrm{Gpc},O4,face-on)=1.91$；$D_{\max}(|\delta\omega/\omega|=2\%)$ O4 ~0.04 Gpc / Voy ~0.11 Gpc |

【 **重跑命令与判定** :与 B.2c 同环境（dps=45）。`_v20_mixed_bc_spectrum.py` 的 GR 三模复现位数应 ≥11–15 位；有限盒自证门的"正确"输出是 **$\det M$ 不趋零/无 CAP 本征值**（第 5 墙否定，非收敛根）。`_v20_virtual_waveguide_snr.py` 的 $r_b=0.325$ 系**反事实公设值**，须与 E444 降级 caveat 同读（非 TUFT 真实腔内值、$\delta\omega$ 未实测）。】

## B.2e v21 两谱路线脚本（E445/E446）

【 **环境（v21）** :同 B.2d（`.venv`，Python 3.12.9 + mpmath dps=45 + scipy）。两脚本均独立重写；原始输出同名 `_out.txt`（`_v21_envelope_spectrum_out.txt` 末尾 85–131 行含 R1 诚实改判段、`_v21_essential_singularity_out.txt`），数字 organizer 已抽原始输出照抄。**特别注意：R1 原判 PASS 已被 organizer 独立核验纠正为 FAIL。**】

| 脚本（+同名 `_out.txt`） | 覆盖实验/定理 | 期望输出对照 |
| `_v21_envelope_spectrum.py` | 实验二十七 / 第15章 §15.11（E445，GR 门 FAIL 第 6 墙） | 原判"PASS"后接诚实改判：$n0$ 根 $0.1117/0.1536/0.3313$ 仅 ~1 位、$n1$ 实部 $5.58\times10^{-10}$、跨 $s_{\max}$ $0.207/0.154/0.136$；$|\det M(w^\*)|$ $1.8\times10^{-8}(N24)\to2.6\times10^{21}(N60)$ 条件数爆炸；corrected $O(1/s^2)$ 出射 Robin $1.37\times10^{-2}(N16)\to1.6\times10^{-6}(N48)$ vs bare 饱和 $8.8\times10^{-4}$；深盒+双侧 WKB 残差地板 $\sim10^{-6}$、伪本征值 $0.2797-0.2234i$（$|R|=1.1\times10^{-61}$）（**要的就是"误标纠正 + GR 门 FAIL"这一否定输出**，不报 TUFT 根） |
| `_v21_essential_singularity.py` | 实验二十八 / 第15章 §15.11（E446，GR 门 PASS + TUFT 结构墙） | GR 门 dps=45（N=100/200/400/1000 三值收敛）：RW $s=-2$ $n0$ $0.3736716844180418-0.0889623156889357i$（15 位，$1.6\times10^{-15}$）、$n1$ 14 位（$8.0\times10^{-14}$）、标量 $s=0,l=0$ 11 位（$3.1\times10^{-11}$）；TUFT 结构墙——$u$-方程残留本质指数为动能项 $\omega^2 e^{4/\rho}P$（不被 $e^{-2/\rho}$ 消）；$\rho_h=0.6099$ Frobenius 半径 $R_{\mathrm{series}}\approx0.81$（$P=\rho^3+c\rho+d$ 根 $-0.4099/-0.2/0.6099$）仅延到 $\rho\approx1.42$、递推 $c[60]\sim1.68\times10^{105}$ 爆炸（**GR 门 PASS 硬资产 + TUFT 结构墙严格，不报 TUFT 根**） |

【 **重跑命令与判定** :与 B.2d 同环境（dps=45）。`_v21_envelope_spectrum.py` 的"正确"输出是**误标纠正 + GR 门 FAIL**（第 6 墙否定：$n0$ 根仅 ~1 位/行列式条件数爆炸/伪本征值劫持），不是"根收敛"；其 corrected $O(1/s^2)$ Robin 随 $N$ 收敛 $1.37\times10^{-2}\to1.6\times10^{-6}$ 是**方向被证有效**的正面收获。`_v21_essential_singularity.py` 的 GR 三模复现应 11–15 位；TUFT 侧 Frobenius 半径仅 $\sim0.81$ 够不到无穷远出射边界（结构墙），不报 TUFT 根。】

## B.2f v22 两路脚本（E449/E450）

【 **环境（v22）** :同 B.2e（`.venv`，Python 3.12.9 + mpmath + scipy）。两脚本均独立重写；原始输出同名 `_out.txt`（`_v22_compact_eig_out.txt` / `_v22_multiseg_frobenius_out.txt`），数字 organizer 已抽原始输出照抄。**编号顺延说明**：开工前重读磁盘权威头部，主册已被并行 MainAgent 线推进至 v2.7、E447/E448 已占用（E447=v22 壁 Frobenius 严格引理/勘误#28；E448=v23 线性谱两端渐近三要件/勘误#29），故任务原拟 E447/E448 **顺延为 E449/E450**；版本 v2.7→v2.8；勘误保持 #29（本轮无新勘误；不回退 #28/#29 与任何否定定理）。两路均 GR 门 FAIL 诚实否定、均未报 TUFT 根。】

| 脚本（+同名 `_out.txt`） | 覆盖实验/定理 | 期望输出对照 |
|---|---|---|
| `_v22_compact_eig.py` | 实验二十九 / 第15章 §15.12（E449，GR 门 FAIL 第 7 墙） | dps=45（PART1 Gauss 内点）/dps=42（PART2 Lobatto 端点节点+端点 Robin 行，$L=5.5$）。自洽复现 Leaver 基准 RW $s=-2$ $n0$ $0.3736716844180418-0.0889623156889357i$（$|d\text{-}\mathrm{cat}|=1.60\times10^{-15}$）；PART1 $x=\tanh(s/L)$ 拼接因子 companion 一次 eig $n0$ 随 $L=4/5.5/7$、$N=10$–$22$ 不收敛、$n1$ 模式跳变、标量 $l=0$ 漂移；PART2 $n0$ $N=18/26/34$ $0.3787-0.1049i/0.3508-0.0941i/0.3363-0.0884i$（$|d|$ $1.68\times10^{-2}/2.34\times10^{-2}/3.73\times10^{-2}$ 非单调恶化）、$n1$ 模式跳变、$s0$ 伪本征值平台 $-0.1818i$；诊断——tortoise 紧化端点 $V L^2/(1-x^2)$ 指数发散（伪谱自洽非物理）、proper-r $r=2/(1-x)$ 初版漏 $(A')^2$ 项（已修正 $\sigma_{\min}$ $27\to7$）仍条件数 $10^6$–$10^9$＋本质奇点 $e^{2i\omega/(1-x)}$、有限盒 $O(1/s^2)$ 修正 Robin $N=40=0.368-0.080$（$10^{-6}$ 地板）（**要的就是"GR 门 FAIL 第 7 墙"这一否定输出**，不报 TUFT 根） |
| `_v22_multiseg_frobenius.py` | 实验三十 / 第15章 §15.12（E450，GR 门 FAIL 镜像条件数墙） | dps=50，墙钟 21.8s。方案 A 单端 Robin $F=yp/y-k_{\mathrm{out}}(r_{\mathrm{end}})$ 大 $r_{\mathrm{end}}=200/400/800$：$|F|=5.18\times10^{-6}/6.52\times10^{-7}/8.17\times10^{-8}$ 渐近尾平坦、findroot 伪根 $0.859-0.014i$（偏离 0.49）；方案 B 双侧 $(y,yp)$ Wronskian：右解向内传播数值入射成分指数增长（反向条件数墙），$r=40$ $|ld-k_{\mathrm{out}}|=7.94\times10^{-1}$ 两侧不匹配；方案 C Riccati 双侧：垒区节点 $u=y'/y$ 极点、Taylor 级数溢出（$|F|=\infty$）不可用；三方案无一达 $\ge8$ 位/残差 $\ge10^{-8}$（**要的就是"镜像条件数墙"这一否定输出**，不报 TUFT 根） |

【 **重跑命令与判定** :与 B.2e 同环境（dps=42–50）。`_v22_compact_eig.py` 的"正确"输出是 **GR 门 FAIL（第 7 墙）**——$n0$ 非单调恶化（$1.68\times10^{-2}\to3.73\times10^{-2}$）、$n1$ 模式跳变、$s0$ 伪平台 $-0.1818i$，不是"根收敛"；其有限盒 $O(1/s^2)$ Robin $N=40=0.368-0.080$ 是最接近方向但仍受 $10^{-6}$ 地板限。`_v22_multiseg_frobenius.py` 的"正确"输出是 **GR 门 FAIL（镜像条件数墙）**——三方案 $|F|$ 渐近尾平坦/$|ld-k_{\mathrm{out}}|$ 涨到 O(1)/Riccati 极点溢出。两路均不报 TUFT 根（不硬造）；与 E448 互补（MainAgent 判 A 路为可修实现要件非原理墙，不回退）。下一步：紧化须解决端点指数条件数，$z=1/r$ 紧化吸收出射因子为权仍待试。】


## B.2g v23 独立审计两脚本（E451/E452）

【 **环境（v23）** :同 B.2f（`.venv`，Python 3.12.9 + mpmath + scipy）。两脚本均**独立重写、不 import 任何 v24 脚本、粗糙初值**；原始输出同名 `_out.txt`（`_audit_v23_gr_gate_out.txt` / `_audit_v23_tuft_pole_out.txt`），数字 organizer 已抽原始输出照抄。本轮为**确认轮**（GR 门 PASS + TUFT 候选 Grade C 维持），非新否定墙；勘误保持 #30（本轮无新勘误）。】

| 脚本（+同名 `_out.txt`） | 覆盖实验/定理 | 期望输出对照 |
|---|---|---|
| `_audit_v23_gr_gate.py` | 实验三十一 / 第15章 §15.13（E451，GR 门独立复算 PASS） | 另写紧化+剥离+复 $b$ 围道（不 import v24）；微分阵自检 $D z-1=2.27\times10^{-13}$/$D^2 z^2-2=3.64\times10^{-12}$/$D^2 z^3-6z=4.77\times10^{-11}$。$n0$ $N=30/35/40$ 三值差 $6.59\times10^{-13}$（~12 位）、对目录 $4.62\times10^{-13}$、跨 23 复 $b$ $2.88\times10^{-12}$（~11.5 位）；$n1$ 三值差 $7.13\times10^{-9}$（~8 位）、对目录 $8.1\times10^{-10}$、跨 $b$ $1.88\times10^{-8}$（~7.7 位，弱模/平台窄/$N\ge40$ 漂移）。证实勘误#30 口径（Jansen $7.47\times10^{-14}$ 系相邻-N 本征值间距，本复算 $4.18\times10^{-13}$ 同量级）（**要的就是"GR 门 PASS、12/8 位"这一确认输出**） |
| `_audit_v23_tuft_pole.py` | 实验三十二 / 第15章 §15.13（E452，TUFT 极点 RQI 精修 Grade C） | 粗糙初值 $0.42-0.04i$（非 v24 锚点）；GR 门 PASS $5.21\times10^{-10}$（$N=25/30/40/50$ 四值稳、跨 $b$ 不变、微分阵自检 $4.55\times10^{-13}$/$5.82\times10^{-11}$）。复算 $w=0.434443861-0.056450281i$（vs v24 `tuft_poles` $0.434445371-0.056448086i$ 差 $2.66\times10^{-6}$ 散布内）；RQI+Newton 迹法一致 $4.02\times10^{-12}$（排除伪本征值劫持）、mpmath dps=40 vs 双精度 $6.9\times10^{-14}$（排除舍入）；robust core $6.12\times10^{-6}$（v24 $2.1\times10^{-5}$ 改善 3.4×）仍 $>10^{-6}$ 门、WORST $2.87\times10^{-5}$；根因近壁分数幂 $s\sim(\rho-\rho_h)^{3/2}$ Chebyshev 代数收敛（非指数）、$N\ge80$ 才聚拢、$b_I\ge0.5$ 必要（**Grade C/~5 位，$<10^{-6}$ 门未达**） |

【 **重跑命令与判定** :与 B.2f 同环境。`_audit_v23_gr_gate.py` 的"正确"输出是 **GR 门 PASS**（$n0$ 12 位/$n1$ 8 位、跨 23 复 $b$ 不变）；其 $n1$ 弱模、$N\ge40$ 漂移是预期的弱模指纹，非 bug。`_audit_v23_tuft_pole.py` 的"正确"输出是 **Grade C 候选**（$w=0.434443861-0.056450281i$，robust core $6.1\times10^{-6}$ 仍 $>10^{-6}$ 门）；RQI 与 Newton 迹法须一致到 $\sim10^{-12}$、mpmath dps=40 与双精度差 $\sim10^{-13}$。两路线（`tuft_poles` 物理势 / `jansen_complex` GR）互证无冲突；Grade C→A 须多域/分数阶基函数解决近壁分数幂代数收敛。】

## B.2h v25 两路收口两脚本（E453/E454；勘误 #31 保持）

【 **环境（v25）** :同 B.2g（`.venv`，Python 3.12.9 + mpmath + scipy）。两脚本原始输出同名 `_out.txt`（`_audit_v25_pole_gate_out.txt` / `_audit_v25_resonance_out.txt`），数字 organizer 已抽原始输出照抄。本轮为**两路收口**（A 路 Grade C→A 冲门未达、B 路共振位置第二通道背书），非新否定墙；勘误保持 #31（本轮无新勘误）。】

| 脚本（+同名 `_out.txt`） | 覆盖实验/定理 | 期望输出对照 |
|---|---|---|
| `_audit_v25_pole_gate.py` | 实验三十三 / 第15章 §15.14（E453，Grade C→A 冲门未达） | GR 门 PASS（标准 Jansen 紧化 $N=30/35/40$ 三-N spread $4.93\times10^{-13}$/~12.3 位、跨 8 复 $b$ $1.60\times10^{-12}$）；TUFT 标准映射 warm-continuation（anchor $0.434-0.056i$）复算 $w=0.434445295-0.056449613i$（与 E450/E452 一致）；robust core $3.51\times10^{-5}$（local-$b$ 3.5e-5/近壁 $t_0$ 1.8e-5/Frobenius-$\beta$ 1.6e-5，worst N-sweep 1.66e-4、宽 b 1.44e-4），<1e-6 门未达。主流程跑标准映射 Stage1/2；分数映射（`tuft_eig_frac`）与 Jacobi$(-1/2,\gamma)$ 权为已实现但失败的两条升 A 路线（**正确输出＝尾行 "GATE NOT ACHIEVED: robust core 3.5e-05 >= 1e-6. E450 维持 Grade C"**） |
| `_audit_v25_resonance.py` | 实验三十四 / 第15章 §15.14（E454，共振位置第二通道背书） | GR 门 PASS $5.207\times10^{-10}$（三-N $4.93\times10^{-13}$、跨 $b$ $1.14\times10^{-12}$；微分阵自检 $D z-1=2.27\times10^{-13}$/$D^2 z^2-2=3.64\times10^{-12}$）。相位/Wigner 残差峰跨 9 窗/阶 $w_0=0.4351$–$0.4401$（包住极点 Re=0.4344）；HWHM $g=0.0227$–$0.0388$（$Q=5.67$–$9.62$）漂移$\neq|w_i|=0.0564$；$|R|^2=1$ 实测 $|a_{in}-b_{out}^*|/|a_{in}|=0$（平凡恒等式，#31-i）；近壁斜率 1.2628（$\beta=1.26376$，rel 0.08%）、节点 0、远场 $\log|\psi|=+0.0357\approx+|w_i|$（#31-iii）；仅 0.434 主峰+1.274 弱特征（$w/\pi/L=2.827$ 非整数）单模；toy 60M☉ $f=201.2$→$234.0$ Hz（+16.26%）（**要的就是"位置第二通道复现、阻尼/泛音/SNR 仍 OPEN"这一输出**） |

【 **重跑命令与判定** :与 B.2g 同环境。`_audit_v25_pole_gate.py` 的"正确"输出是 **Grade C 维持、GATE NOT ACHIEVED**（robust core $3.5\times10^{-5}\ge10^{-6}$）；分数映射/Jacobi 权跑出特征值跳错/越界是**预期失败**，非 bug。`_audit_v25_resonance.py` 的"正确"输出是 **位置第二通道背书 + 阻尼 OPEN**（$w_0$ 包住 0.4344、近壁斜率 1.2628、远场 +0.0357）；$|R|^2=1$ 恒为 0 是平凡恒等式（#31-i），不载反射核信息。两脚本与 E450/E452、勘误 #31 一致，不回退。】

## B.2i v27 破解轮两路 Grade A 收口两脚本（E457/E458；勘误 #35 保持/本轮无新勘误）

【 **环境（v27 破解轮）** :同 B.2h（`.venv`，Python 3.12.9 + mpmath + scipy）。两脚本原始输出同名 `_out.txt`（`_audit_v27_beyn_out.txt` / `_audit_v27_multidomain_out.txt`），数字 organizer 已抽原始输出照抄。本轮为**两路 Grade A 收口**（A 路 Beyn 围道独立审计、B 路多域谱元独立交叉），非新否定墙；勘误保持 #35（本轮无新勘误，不回退 #35/#34）。】

| 脚本（+同名 `_out.txt`） | 覆盖实验/定理 | 期望输出对照 |
|---|---|---|
| `_audit_v27_beyn.py` | 实验三十五 / 第15章 §15.15（E457，Beyn 围道独立审计 Grade A） | GR 门 PASS（Jansen 紧化 N=80 最佳 \|err\|=**5.198e-10**、跨 b 3.627e-13，逐位勘误 #34）；Beyn rank-1 稳定聚 **0.434445174−0.056449760i**（9 配置 Re span 1.36e-9/Im span 1.55e-9、S1/S0~0、seed 散度 1.2e-11）；对照同 pencil direct-GEP 在 N=100/K=12 选错模 **0.429914639−0.062717110i**（\|direct−Beyn\|~7.7e-3，围道投影绕开选模污染）；修正近壁窗 s∈[1e-3,0.30]（U1=1.284e-2/a5=1.961e-4/a6=−2.704e-6）后甜点 N=60/70×K=2/4/6/8×seed n=33：**Re span 3.959e-7、Im span 2.312e-7、robust core=3.161e-7<1e-6**；中位极 **0.434445178−0.056449760i**（距 #34 仅 2.47e-9）、\|ω_i\|=0.056450、τ=17.7149M（**要的就是"Grade A、谱通道数值精度闭合"这一输出**；物理阻尼 OPEN 不变） |
| `_audit_v27_multidomain.py` | 实验三十六 / 第15章 §15.15（E458，多域谱元独立交叉 Grade A） | GR 门 PASS（\|err\|~5.2e-10、三-N 4.932e-13、跨 b 6.605e-13）；标准 Jansen 紧化不越界；Chebyshev-Lobatto + s^β Frobenius peel（K=2 吸收近壁 s⁻⁴ᐟ³）；双子域界面 ψ/ψ′ 匹配失败（界面行 w-无关 pencil 奇异）→ 单元素 Lobatto+全局 peel 达同等精度；TUFT 复算 **w=0.434445220−0.056449703i**，N 散度 1.670e-7/b 散度 1.602e-7，**robust core=1.670e-7<1e-6**；K 扫 K=0 1.938e-5 离群/K=2 最优 ~2e-7/K≥8 数值噪声（K=8=1.28e-6）；**vs Beyn \|B−Beyn\|=6.968e-8<1e-6**（两独立离散化互证）（**要的就是"Grade A、两路线互证 6.97e-8"这一输出**；按 #35 非物理独立阻尼通道，物理阻尼 OPEN 不变） |

【 **重跑命令与判定** :与 B.2h 同环境。`_audit_v27_beyn.py` 的"正确"输出是 **Grade A**（GR 门 5.198e-10、Beyn rank-1 稳定 0.434445174−0.056449760i、甜点 robust core 3.161e-7<1e-6）；direct-GEP 选错模是**预期对照指纹**，非 bug。`_audit_v27_multidomain.py` 的"正确"输出是 **Grade A + 互证**（w=0.434445220−0.056449703i、robust core 1.670e-7<1e-6、\|B−Beyn\|=6.968e-8<1e-6）；双子域界面奇异退回单元素是**预期的方法学记录**。两脚本互证的是极点位置（谱通道数值精度 Grade A 闭合），**不等于物理阻尼闭合**——勘误 #35 恒等式（同一 Q0/Q1 算子谱提法）原样保留，D18 维持 CONDITIONAL 不闭合；不回退 #35/#34。】


## B.3 结果对照要点

【 **期望输出** :每次运行应与第14章精算总表的数值一致（实验九 $Q: 1 \to 0$、实验十二 $+0.875 \to -0.162$ 是预期的反证输出，不是故障）。】

【 **验证守则** :① 只看原始输出，不看二次转述；② 反例（实验九/十二）的出现说明代码正确复现了理论升级的动机；③ 若数值偏离 $> 10^{-3}$ 量级，先检查 numpy 版本与网格分辨率再质疑结论。】

## B.4 环境说明

【 **版本锁定** :Python 3.14.7、numpy 2.5.2（本书全部数据在该环境产出）；更高版本 numpy 的随机数与 SVD 行为可能引起 $10^{-12}$ 级差异，不影响任何结论判定。】
