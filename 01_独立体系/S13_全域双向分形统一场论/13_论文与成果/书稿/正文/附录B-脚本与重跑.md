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
| `_audit_v26_wronskian.py` | 第14/15/16章（D18） | 实验十六（v26 Wronskian 伪点独立复算，REJECT/Grade D） |
| `_audit_v26_analytic_pole.py` | 第14/16章（D18） | 实验十七（解析 $V_{\rm frac}$ 消对消，Grade C 维持） |

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

【 **D18·v26 Wronskian 伪点独立审计（实验十六）** :`python _audit_v26_wronskian.py`——GR 门三-N $2.72\times10^{-10}$/跨 $b$ $3.1\times10^{-11}$；错误 $1/s$ 边界复现伪根 $0.446860296-0.012798531i$；远场 $b(s_{\rm out})$ 漂移 $1.00\times10^{-2}$ 非单调；GR 自洽门近 QNM 种子+正确 $1/s^2$ 边界 $0.0190$ 随 $s_{\rm out}$ 发散至 $0.232$；与 E450/E452 差 $4.54\times10^{-2}$。判定 REJECT（Grade D）。原始输出 `_audit_v26_wronskian_out.txt`。】

【 **D18·v26 解析 V_frac 路径（实验十七）** :`python _audit_v26_analytic_pole.py`——GR 门 $4.93\times10^{-13}$/$1.6\times10^{-12}$；解析 Laurent $V(s)=\tfrac13 s^{-2}-0.134590\,s^{-4/3}+\cdots$；对消消除 $t_0$ $2.4\times$、N-sweep $4\times$；robust core 仍 $3.02\times10^{-5}$ 未过 $<10^{-6}$。判定 Grade C 维持。原始输出 `_audit_v26_analytic_pole_out.txt`。】

## B.3 结果对照要点

【 **期望输出** :每次运行应与第14章精算总表的数值一致（实验九 $Q: 1 \to 0$、实验十二 $+0.875 \to -0.162$ 是预期的反证输出，不是故障）。】

【 **验证守则** :① 只看原始输出，不看二次转述；② 反例（实验九/十二）的出现说明代码正确复现了理论升级的动机；③ 若数值偏离 $> 10^{-3}$ 量级，先检查 numpy 版本与网格分辨率再质疑结论。】

## B.4 环境说明

【 **版本锁定** :Python 3.14.7、numpy 2.5.2（本书全部数据在该环境产出）；更高版本 numpy 的随机数与 SVD 行为可能引起 $10^{-12}$ 级差异，不影响任何结论判定。】
