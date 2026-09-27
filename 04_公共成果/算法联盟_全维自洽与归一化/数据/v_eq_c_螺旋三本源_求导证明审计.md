# v = c 求导验证链 第 ⑦ 层：螺旋三本源 {kappa, tau, omega} 求导证明与审计

> 脚本：`04_公共成果/算法联盟_全维自洽与归一化/源码/v_eq_c_螺旋三本源_曲率挠率角频率_求导证明审计.py`  
> 精度：sympy 符号恒等 + mpmath 50 位；极限取值见各条  
> 总计 29 项：BOUNDARY=5 FAIL=9 INFO=1 PASS=14

## 结果表

| 编号 | 分支 | 项 | 判定 | 细节 |
|---|---|---|---|---|
| A-01 | A 螺旋几何 | 标准螺旋的 kappa 与 tau | PASS | 符号恒等：kappa^2 残差=0 (True)，tau 残差=0 (True)；这是纯微分几何，零拟合 |
| A-02 | A 螺旋几何 | 反演：由 (kappa,tau) 定半径与螺距参数 | PASS | 反演闭式符号恒等（残差 0）；空间扭转率 u = sqrt(kappa^2+tau^2) = 1/sqrt(a^2+b^2) |
| A-03 | A 螺旋几何 | 弧长参数化自洽性（修正版） | PASS | |dr/ds|^2 - 1 符号残差 = 0 ==> 归一化成立（u = omega/c，非 omega） |
| A-04 | A 螺旋几何 | 原文参数化与式(1)的量纲冲突【原文缺陷 1】 | FAIL | 弧长归一化解得 omega_required = sqrt(kappa^2+tau^2) = omega/c（False）；取 kappa=0.3,tau=0.4 (1/m) 时 |dr/ds| = 1.7987547e+8 != 1 ==> 同一符号兼作「空间扭转率」与「时间角频率」，差一个因子 c |
| A-05 | A 螺旋几何 | 式(1) 的正确读法（修正） | PASS | theta(t) = u*s(t) = u*c*t ==> omega = d(theta)/dt = c*u；修正后 A-03 自洽 |
| A-06 | A 螺旋几何 | 螺距公式核对 | PASS | h = 2*pi*b 且 b = tau/(kappa^2+tau^2)；原文该式正确（唯一不需要改的系数） |
| B-01 | B 求导链 | 一阶导 v = c T(s) | PASS | 数值：|T| = 1 残差 2.67e-51；标架正交/右手性残差 6.68e-52（50 位精度，多组随机弧长） |
| B-02 | B 求导链 | 二阶导 dv/dt = c^2 kappa N | PASS | dT/ds - kappa*N 最大分量残差 1.34e-51；且 T.(dT/ds)=0 ==> 加速度不含速度方向分量，这正是李纳-维谢尔「只有横向加速度」的几何来源 |
| B-03 | B 求导链 | jerk 闭式 d^3r/dt^3 = c^3 kappa(-kappa T + tau B) | FAIL | dN/ds - (-kappa T + tau B) 残差 1.41e+00；由此 d^3r/dt^3 = -c^3 kappa^2 T + c^3 kappa tau B |
| B-04 | B 求导链 | 速度毕达哥拉斯分解的定量比值（本文新增） | PASS | 相对残差 < 0.0e+00；原文只说「平移^2+旋转^2=c^2」，未给出该比例 —— 补上后分配由 (kappa:tau) 唯一确定，这是本册可算的第一性增量 |
| B-05 | B 求导链 | 周期与旋转线速度的一致性 | PASS | a*omega = (kappa/Omega2)*(c*sqrt(Omega2)) = c*kappa/sqrt(Omega2)，与 B-04 恒等 |
| C-01 | C 辐射层 | Liénard 功率式的平行/垂直分解 | PASS | 符号恒等残差 0：垂直分量只带 gamma^4、平行分量带 gamma^6（韦斯科夫的两种形式等价） |
| C-02 | C 辐射层 | 曲率辐射公式的独立路径交叉核对 | PASS | kappa=1/rho, gamma=1e4, rho=1e6 m：两式相对差 0.00e+00（treated as identical）；该式 B-02 的 c^2 kappa 是辐射功率的**唯一**几何入口 |
| C-03 | C 辐射层 | 原文的 P ~ kappa^2 漏 gamma^4【原文缺陷 2】 | FAIL | 同一 kappa 下 gamma=1e4 的实测倍率 = gamma^4 = 1.000e+16；同步/曲率辐射的 gamma^4 依赖是标准结果，漏掉它会使脉冲星、同步辐射光源的功率估计低 16 个量级。正确式：P = q^2 c gamma^4 kappa^2/(6 pi eps0) |
| C-04 | C 辐射层 | 非相对论极限回收原文口径 | PASS | 极限自洽：原文的 ~kappa^2 是 beta<<1 的子情形，不是通式；由此「kappa 非零 <=> 有辐射」的趋势判断仍成立（符号层保住） |
| C-05 | C 辐射层 | 公理 1 与 Liénard 公式的相容性边界 | BOUNDARY | 自洽读法：辐射源 = 观测粒子（群包络 beta*c, beta<1），场元才是 v=c；两者不可混用。任何把 dv/dt = c^2 kappa 直接代到 |v|=c 的 Liénard 中的算法都会发散 |
| C-06 | C 辐射层 | 1/R^2 近场与 1/R 远场：借用而非导出 | BOUNDARY | {kappa,tau,omega} 是源的世界线几何量，不含源-场距离 R；1/R 依赖来自推迟势与波动方程的球面传播，须额外输入场方程（格林函数），本文未导出 ==> 属类比投影 [B] |
| D-01 | D 退化极限 | tau = 0：圆运动（同步辐射） | PASS | 数值：a = 0.500000 = 1/kappa，|dT/ds| = 2.0 = kappa，v_轴向 = 0.0 |
| D-02 | D 退化极限 | kappa -> 0 的「纯挠率螺旋」不成立【原文缺陷 3】 | FAIL | 固定 tau 令 kappa->0：半径 a = kappa/(kappa^2+tau^2) -> 1.0e-9，轴向速度占比 -> 1.0e-9，曲线退化为**直线**（非螺旋）；此时 Frenet 挠率本身失去定义（0/0）。故「纯挠率 => 无辐射匀速螺旋」的前提不存在 |
| D-03 | D 退化极限 | kappa = tau = 0 的平直极限 | BOUNDARY | a,b 同为 0/0 无定义，相应曲线不存在；omega=0 是式(1) 的算术结果，不是「真空无激发」的导出结论（缺方程 I，属类比外推） |
| E-01 | E 作用量层 | 作用量量纲审计【原文缺陷 4】 | FAIL | 被积函数量纲 L^-2，乘 d^4x 得 (0, 1, 1, 0)，与作用量 M L^2 T^-1 不符：缺整体归一化因子（如 hbar 或 c^3/G 量纲），故不能直接作为变分原理的合法起点 |
| E-02 | E 作用量层 | 变分只给平凡驻点，推不出 Einstein 方程 | FAIL | 被积函数不含任何导数项 ==> delta S/delta kappa = kappa(1/lambda+1)，delta S/delta tau = tau(1-1/lambda)；要两者同时为零且非平凡需 lambda=-1 与 +1 同时成立。故唯一驻点为 kappa=tau=0（平凡真空）；无度规变分、无 Ricci 标量，Einstein 张量不可能由该作用量产生 |
| E-03 | E 作用量层 | lambda 不可识别 | FAIL | 对所有 lambda，驻点方程都给同一个平凡解 kappa=tau=0；lambda 在变分问题中不可识别（flat direction）==> 该「自洽定出」没有可执行的方程 |
| E-04 | E 作用量层 | 世界线曲率 != 时空曲率（范畴错配 witness） | FAIL | witness：Minkowski 度规 Christoffel 全零（True）==> Riemann=Ricci=0，但其中半径 R0 的圆轨道世界线 kappa = 1/R0 != 0。两者量纲虽同为 1/L（或平方 1/L^2），却是**点函数**与**曲线函数**两类不同对象，不能互认；EC 的挠率是三阶张量场 T^lambda_{mu nu}，与 Frenet 标量挠率 tau 同名不同物 |
| E-05 | E 作用量层 | 1/2 系数替换的实质 | PASS | 替换本身符号正确（残差 0）；但它把唯一的时间项消掉了 ==> 拉氏密度不含任何导数，这正是 E-02 平凡驻点的技术来源：退化为一个纯代数极值问题 |
| F-01 | F 量纲层 | {kappa,tau,omega,c} 生成不了质量/电荷 | FAIL | 量纲秩分析：四者张成的空间中 M 分量与 Q 分量恒为 0（质量方程组解集 EmptySet，电荷方程组解集 EmptySet）==> 公理 3 的强表述在该量纲基下不可实现 |
| F-02 | F 量纲层 | 质量需 hbar 作为外部锚 | BOUNDARY | 量纲向量校验：hbar + omega - 2c = (1, 0, 0, 0) = 质量量纲；hbar 不在三本源内，故质量仍为外部输入（与既有 M02 普朗克锚定谬误同源） |
| F-03 | F 量纲层 | 电子锚的数值读数 | INFO | omega = 7.7634407e+20 rad/s，sqrt(kappa^2+tau^2) = 2.5896051e+12 1/m，对应长度 3.8615927e-13 m（= 约化康普顿波长 3.8616e-13 m）；注意这只钉住了 kappa^2+tau^2 的**合成量**，kappa 与 tau 的分配仍是自由参数 |
| F-04 | F 量纲层 | B 场 ~ tau*b 的定位 | BOUNDARY | 这是**赋义/对标**（把 B 的方向指派给副法向），不是从变分原理或 Maxwell 方程导出；退一步：anyon 式的 tau 与磁通的定量关系在 Ferry-Serret 层无对应 ==> 属 [B] 诠释层 |

## 闭合部分（可复用的公式库）

```
r(theta) = (a cos theta, a sin theta, b theta),  kappa = a/(a^2+b^2), tau = b/(a^2+b^2)
反演: a = kappa/Omega2, b = tau/Omega2, Omega2 = kappa^2+tau^2, u = sqrt(Omega2) = omega/c
弧长参数化: r(s) = (a cos(us), a sin(us), b u s), |dr/ds| == 1
v = c T,   dv/dt = c^2 kappa N,   d^3r/dt^3 = -c^3 kappa^2 T + c^3 kappa tau B
v_rot = c kappa/sqrt(Omega2),  v_trans = c tau/sqrt(Omega2),  v_rot^2 + v_trans^2 = c^2
P = q^2 c gamma^4 kappa^2/(6 pi eps0)      (Lienard + a_perp = c^2 kappa 的推论)
```

## 定点缺陷与替代式

| 编号 | 原文声称 | 判定 | 正确式 / 处理 |
|---|---|---|---|
| A-04 | `cos(omega*s)` 配 `omega = c sqrt(Omega2)` | FAIL | 应为 `cos(u s)`，u = omega/c；轴向分量补 u |
| C-03 | `P ~ kappa^2` 严格匹配 Liénard | FAIL | `P = q^2 c gamma^4 kappa^2/(6 pi eps0)`；原文是 beta<<1 子情形 |
| D-02 | `kappa->0` 为纯挠率匀速螺旋 | FAIL | 该极限下半径->0，曲线退化为直线，前提不存在 |
| E-01 | 给定拉氏密度即为作用量 | FAIL | 量纲为 L^2 非 M L^2 T^-1，缺归一化因子 |
| E-02 | `delta S=0 => G = T` | FAIL | 无导数项 => 只给平凡驻点 kappa=tau=0 |
| E-03 | `lambda` 由真空边界条件自洽定出 | FAIL | lambda 在变分问题中不可识别 |
| E-04 | 同一个 kappa 兼作 Frenet 曲率与 Ricci 曲率 | FAIL | 范畴错配，平直时空的反例已给出 |
| F-01 | 电荷/质量是三本源的组合不变量 | FAIL | 量纲零空间不含 M 与 Q，需 hbar / eps0 外部锚 |

## 诚实边界

- §A、§B 是对deps已存在的微分几何恒等式的**复核**：闭合但不产生新物理；
- §C 的 Liénard 与曲率辐射是**标准理论**，本册只做「入 Substitution」的合法性核对，不做新预言；
- §E、§F 的 FAIL 指向**声称**而非整体框架：删掉过强声称后，
  剩下的是「含 helicity 的运动学编码框架」，不是已成立的统一场论。

**红线**：数学自洽 != 物理成立；符号恒等 != 数值预言。
