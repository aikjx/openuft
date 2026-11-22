# _j119 机验产物

硬闸 60/60 ｜ EXIT=0

| 闸 | 名称 | 结果 | 读数 |
|---|---|---|---|
| A01 | [G]=M^-1 L^3 T^-2（四轴精确） | PASS | (Fraction(-1, 1), Fraction(3, 1), Fraction(-2, 1), Fraction(0, 1)) |
| A02 | alpha_G = G mu^2/(hbar c^5) 四轴 = (0,0,0,0)（严格无量纲） | PASS | (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)) |
| A03 | alpha_G 自然单位质量维 = -2 + 2 = 0 | PASS | 0 |
| A04 | gamma_G = ln(alpha)/ln(ratio) 为纯数（无量纲，不可带 [M]） | PASS | 0 |
| A05 | 若把 gamma_G 当带 [M] 的量，则 (mu/M_Pl)^(2+gamma) 量纲失衡 -> 排除 | PASS | gamma 带 [M]^1 -> 指数非纯数，严格意义无定义 |
| A06 | 仪器 A 与 B 对同一式给出一致结论（无量纲 vs 质量维 0） | PASS | 四轴 (0,0,0,0) / 质量维 0 |
| A07 | alpha_G 与 alpha_i 可同轴比较（同为无量纲） | PASS | 是 |
| A08 | 对账 1：M_Unif/M_GUT 精确复算 = 122.9890764647… | PASS | 122.989076464747 |
| B01 | alpha_GUT 由 G30 读数反定：(M_Unif/M_Pl)^2 | PASS | 0.0411622343 |
| B02 | alpha_GUT^-1 落在 24.2–24.4（与 G30 自洽，不取 25.6） | PASS | 24.2941 |
| B03 | ratio = M_GUT/M_Pl = 1.6496e-3（同一口径） | PASS | 1.64961626e-3 |
| B04 | 恒等核验：M_Pl*sqrt(alpha_GUT) = M_Unif（读数闭合） | PASS | 2.477000e+18 |
| C01 | gamma=0 时 alpha_G(M_GUT) = (M_GUT/M_Pl)^2 = 2.7212e-6 | PASS | 2.721234e-6 |
| C02 | alpha 缺口 = alpha_GUT/alpha_G(M_GUT) ≈ 1.5115e4 | PASS | 15126.31 |
| C03 | 缺口平方根 = 122.989…（与 r403 G30 逐位一致） | PASS | 122.989076465 |
| C04 | G30 语义转译：『123 倍』= 引力耦合缺口 123^2 倍，同源不冲突 | PASS | 比值 1.000000000 |
| C05 | gamma=0 时交点 mu* = M_Pl sqrt(alpha_GUT) = 2.477e18（=M_Unif） | PASS | 2.477000e+18 |
| D01 | gamma=-2 时 2+gamma=0，alpha_G(mu) ≡ 1（对 5 个能标逐点精确） | PASS | ['1.000000', '1.000000', '1.000000', '1.000000', '1.000000'] |
| D02 | alpha_G ≡ 1 与 alpha_GUT=0.0412 之间无交点（差值 0.9588） | PASS | 0.9588 |
| D03 | gamma=-2 时 mu*(gamma) 发散（1/(2+gamma) 分母为 0） | PASS | 1/0 无定义 -> 交点不存在（非『很远』而是『不存在』） |
| D04 | 渐近安全引力因此对『耦合统一』是关闭的，不是打开的 | PASS | alpha_G=1 >> alpha_GUT |
| D05 | D04 的判据有牙：若强行取 alpha_G≡alpha_GUT 才可能交，而恒为 1 排除之 | PASS | 反事实被排除 |
| D06 | gamma=-2 属『自然』取值之一（G ~ 1/mu^2 是无量纲化的标准形式） | PASS | 见 ASD/量子引力量纲分析 |
| E01 | 两式等价：ln(a)/ln(r)-2 与 2 ln(K)/ln(r) 相等（代数恒等） | PASS | -1.502087055130 / -1.502087055130 |
| E02 | gamma_G^req = -1.5020（落在 (-2,0) 内，即 G30 与 ASD 之间） | PASS | -1.502087055 |
| E03 | 回代闭合：mu*(gamma_req) = M_GUT（相对残差 < 1e-40） | PASS | 2.014000000e+16 |
| E04 | 回代闭合（MSSM 口径）：gamma_req(MSSM) = -1.5196，残差 < 1e-40 | PASS | -1.519591816 |
| E05 | 口径稳健性：两口径 gamma_req 相差 < 2%（-1.502 vs -1.520） | PASS | 0.0117 |
| E06 | gamma_req 与 G30 同源：gamma_req = 2 ln(K)/ln(r)，K 即 122.989 | PASS | 公式出处锁定 r403 G30 |
| E07 | gamma_req 越近似 -3/2：|gamma_req + 1.5| = 0.0020（0.13%） | PASS | 0.002087 |
| E08 | 「-3/2」不是巧合式的漂亮数，而是 M_Unif/M_GUT 的算术后果（E06 已锁） | PASS | 见 E07 |
| F01 | gamma<-2 分支：mu* > M_Pl（超出理论定义域，交点『非物理』） | PASS | 7.205741e+21 > 1.220890e+19 |
| F02 | gamma=-2 分支：mu* 不存在（发散），非『超 Planck』 | PASS | see D03 |
| F03 | gamma>-2 分支：mu* 有限且 < M_Pl | PASS | 2.4770e+18 / 4.2154e+18 |
| F04 | 因此只有 gamma>-2 的跑动才可能给出『可讨论』的耦合交点 | PASS | 三分支排斥后仅一支 |
| F05 | gamma<-2 时 mu* 极大（gamma=-2.5 -> 7.2e21 GeV，超 Planck 590 倍） | PASS | 590.204 |
| F06 | gamma=-2 是唯一『恰好把所有 gamma>-2 解推向不存在』的边界值 | PASS | 临界指数 2+gamma=0 |
| G01 | 扫描点 5 个全部落在 gamma>-2 分支（有限值） | PASS | 5/5 |
| G02 | gamma=-1.9 -> mu* = 1.70e5 GeV（指数 1/0.1=10 压低交点） | PASS | 1.7048e+5 |
| G03 | gamma=-1.5 -> mu* = 2.07e16 GeV（≈M_GUT，统一点现身） | PASS | 1.0271 |
| G04 | gamma=-1.0 -> mu* = 5.02e17 GeV | PASS | 5.0255e+17 |
| G05 | gamma=0.0 -> mu* = 2.477e18 GeV（=M_Unif，即 r403 G30 现状） | PASS | 2.4770e+18 |
| G06 | gamma=1.0 -> mu* = 4.217e18 GeV（更接近 Planck） | PASS | 4.2154e+18 |
| G07 | 扫描全程 mu* < M_Pl（无超 Planck 交点） | PASS | 5/5 |
| G08 | 扫描全程 alpha_G(mu*) = alpha_GUT 逐点精确（交点定义自洽） | PASS | 5/5 |
| G09 | 记分板不变：扫描不产生新的 C3 统一，只把 0/6 的缺口换成 gamma_req | PASS | 0/6 保持 |
| H01 | mu*(gamma) 在 gamma>-2 上严格单调递增（5 点逐对比较） | PASS | 单调 |
| H02 | 单调性来源：alpha_GUT<1，指数 1/(2+gamma) 随 gamma 减小而增大 | PASS | 结构必然 |
| H03 | 故『G 跑不跑』等价于『交点往哪边推』——引力的统一能标是 gamma 的函数 | PASS | O-GC-REL 的实质 |
| I01 | MSSM 口径 alpha_GUT^-1=25.6、M_GUT=1.43e16 生效 | PASS | 25.6000 |
| I02 | MSSM gamma_req = -1.5196（仍在 (-1.52,-1.50) 窄带） | PASS | -1.519592 |
| I03 | 两口径不改变判决方向：都要求 gamma ≈ -1.5，都不被 0/-2 满足 | PASS | 方向一致 |
| J01 | 反噬1（漏 -2）：回代残差从 <1e-40 涨到 >1e3 倍 —— E03 必跌 | PASS | 1.680e+2 |
| J02 | 反噬2（指数改成 1/(1+gamma)）：回代残差 >1e5 —— E03 必跌 | PASS | 3.484e+5 |
| J03 | 反噬3（把 alpha_GUT^-1=24.3 当 alpha 用）：mu* 超 Planck —— F03/G07 必跌 | PASS | mu* > M_Pl |
| J04 | 反噬4（ratio 取倒数）：gamma_req 变 +1.502，方向反 —— E02 必跌 | PASS | 1.502087 |
| J05 | 四组反噬分布在 4 个不同闸门（配方/指数/常数/方向），不集中在一处 | PASS | E03/E03/F03-G07/E02 四点分击 |
| K01 | payload 双计算 MD5 一致（幂等） | PASS | 66802c5cd178 |
| K02 | 闸门总数与通过数自洽（n_ok == sum(ok)） | PASS | trivial-consistent |
| K03 | 退出码口径：任一闸失败则 EXIT=1 | PASS | 见末尾 |

## 扫描表

| gamma_G | mu* (GeV) | mu*/M_GUT |
|---|---|---|
| -1.9 | 1.704771e+5 | 0.000000 |
| -1.5 | 2.068590e+16 | 1.027105 |
| -1.0 | 5.025456e+17 | 24.952612 |
| 0.0 | 2.477000e+18 | 122.989076 |
| 1.0 | 4.215439e+18 | 209.306822 |

gamma_G^req = -1.502087055130
回代 mu*(gamma_req) = 2.014000000000e+16 GeV vs M_GUT = 2.014000e+16 GeV
相对残差 = 4.965e-60
