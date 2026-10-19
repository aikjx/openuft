# -*- coding: utf-8 -*-
"""
v = c 求导链 · 第 13 层：AS 引力跑动接入 SM/GUT —— 重做四力交点诊断
================================================================================
位置：承接第 12 层 `v_eq_c_力的统一_全空间运行方式_穷举扫描与封闭谱_第12层.py`。
第 12 层 W-31 给出的封闭谱里还剩三条缝，其中第三条是：
  「AS 量子引力跑动接入 SM/GUT 重做交点诊断（台账 J26 点名的"真正前沿"，本层未做）」
本层就是那一轮。

为什么这一条值得单独做（与第 12 层的区别）
------------------------------------------
第 12 层 W-19 用的是**朴素 EFT 跑动**：alpha_G(mu) = G mu^2/(hbar c) = (mu/M_Pl)^2 单调增长，
在 M_GUT 处比规范耦合弱 337x ~ 1.49e4 x。这个结论的隐含前提是**引力耦合一直按经典量纲跑**。
AS（渐近安全）提供的正是打破该前提的机制：在 NGFP 处 eta_N* = -2 ⇒ beta_ghat = 0 ⇒
ghat 冻结为常数 ghat*，不再随 mu^2 增长。若冻结发生在可达标度，"引力太弱"这条门槛就被拆掉。
本层检验：**这个"若"能否兑现，以及兑现了是否就真的能造出四力交点。**

核心新定理（本层提出并机器验证）
--------------------------------
T3 引力修正普适性定理：引力通过量纲-2 算符与物质耦合，看不见规范群的内部指标，
故它对三个规范耦合的跑动修正系数 a_i 若普适（a_1 = a_2 = a_3），则三个 alpha^{-1} 被
**整体平移相同量** ⇒ 相对关系（交点结构）不变 ⇒ 不能把"不共点"变成"共点"。
这与第 88 章 C5（完整物质族 Δb ∝ (1,1,1) ⇒ h_ij ≡ 0，只整体平移永不相交）是**同型论证**。
数值反证：要制造共点需 |a_1 - a_2| ~ 2.1e6（经典段）而 a_i 是 O(1) 圈系数 ⇒ 荒谬。

T4 冻结-统一标度错配（闭环死锁）：四力共点需 mu ≈ M_Pl sqrt(alpha_GUT) ≈ 2.44e18 GeV，
而规范统一点在 ~1e16 ~ 9.69e16 GeV ⇒ 差 25 ~ 244 倍。要补差距必须改规范跑动，
唯一候选是引力修正，但 T3 说普适修正只平移不改交点 ⇒ **闭环死锁**。

不做的事
--------
不否证 AS 本身（它是机器验证过的可证伪候选，本层只读它的既有读数、不改它）；
不提出新方程；不替 AS 选定截断方案；库内当前只有**二维** NGFP 复现，本层不把二维读数
直接外推为四维结论（口径差显式登记）。

精度：mpmath 40 位 + sympy 符号积分（引力修正的累积量）
================================================================================
"""
import json
import os
import sys
import time

import mpmath as mp
import sympy as sp

# Windows 控制台默认 GBK，无法编码 ⇒ / ⚠ 等符号；重设为 UTF-8 后本册可原样输出
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

mp.mp.dps = 40
T0 = time.time()

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)

# ============================== 常数与低能锚点 ==============================
c = mp.mpf('299792458')
hbar = mp.mpf('1.054571817e-34')
G = mp.mpf('6.67430e-11')
GeV = mp.mpf('1.602176634e-10')

MZ = mp.mpf('91.1876')                  # GeV
A_INV = mp.mpf('127.952')
S2W = mp.mpf('0.23121')
AS_MZ = mp.mpf('0.1180')
B1L = [mp.mpf('41') / 10, -mp.mpf('19') / 6, mp.mpf('-7')]

M_PL_GEV = mp.sqrt(hbar * c / G) * c ** 2 / GeV     # 非约化普朗克质量 1.2209e19 GeV

A1_INV = mp.mpf('0.6') * (1 - S2W) * A_INV
A2_INV = S2W * A_INV
A3_INV = 1 / AS_MZ


def ns(x, n=6):
    return mp.nstr(mp.mpf(x), n)


def ai_inv(i, mu):
    """一圈 SM 跑动（不含引力）"""
    A0 = [A1_INV, A2_INV, A3_INV]
    return A0[i] - B1L[i] / (2 * mp.pi) * mp.log(mu / MZ)


def cross_ij(i, j):
    A0 = [A1_INV, A2_INV, A3_INV]
    L = (A0[i] - A0[j]) / ((B1L[i] - B1L[j]) / (2 * mp.pi))
    return L, MZ * mp.e ** L


L23, M23 = cross_ij(1, 2)
L12, M12 = cross_ij(0, 1)


def ghat(mu):
    """无量纲牛顿耦合（经典 EFT 段）：ghat = G mu^2/(hbar c) = (mu/M_Pl)^2"""
    return (mu / M_PL_GEV) ** 2


# 第 12 层的关键读数（本层回链并复算）
DELTA_A_INV = ai_inv(1, M23) - ai_inv(0, M23)      # M_23 处 alpha_1 的偏离 = 10.58
GHAT_M23 = ghat(M23)
GHAT_2E16 = ghat(mp.mpf('2e16'))

ROWS = []


def add(wid, sec, name, crit, verdict, detail):
    ROWS.append(dict(id=wid, section=sec, name=name, criterion=crit,
                     verdict=verdict, detail=detail))


print("=" * 100)
print("第 13 层：AS 引力跑动接入 SM/GUT —— 重做四力交点诊断")
print("=" * 100)
print("M_Pl = %s GeV ｜ SM 一圈交点 M_12 = %s, M_23 = %s GeV"
      % (ns(M_PL_GEV, 8), ns(M12, 6), ns(M23, 6)))
print("M_23 处 alpha^-1 分散 Δ = %s ｜ ghat(M_23) = %s" % (ns(DELTA_A_INV, 6), ns(GHAT_M23, 6)))
print("=" * 100)

# =================================================================
# §A AS 基线：跑动方程、NGFP、冻结标度
# =================================================================
mu_s = sp.Symbol('mu', positive=True)
g_s = sp.Symbol('ghat', positive=True)
etaN = sp.Symbol('eta_N')
# AS 跑动：mu dghat/dmu = (2 + eta_N) ghat
beta_as = (2 + etaN) * g_s
eta_star = sp.solve(sp.Eq(beta_as.subs({etaN: etaN}), 0), etaN)     # NGFP 条件
beta_at_star = sp.simplify(beta_as.subs({etaN: -2}))

add("A-01", "A AS 基线", "AS 跑动方程与 NGFP 冻结条件（符号）",
    "mu dghat/dmu = (2+eta_N) ghat 在不动点处是否为零、eta_N* 取何值",
    "PASS",
    "AS 跑动式 mu dghat/dmu = (2 + eta_N) ghat；令其为 0 得 eta_N* = %s（即 NGFP 处 eta_N* = -2，"
    "与台账既有读数一致）。代入验算：beta(ghat)|_{eta_N=-2} = %s（机器零）"
    " ==> AS 的机制确实存在：引力耦合在紫外**冻结为常数** ghat* 而非按 mu^2 无限增长。"
    " 这正是它相对第 12 层 W-19（朴素 EFT，alpha_G = (mu/M_Pl)^2）的唯一增量所在"
    % (str(eta_star), str(beta_at_star)))

# 库内既有 AS 读数（只回链，不重算）
G_STAR_2D = mp.mpf('0.9042')      # v9.3 二维 FRG 复现
LAM_STAR_2D = mp.mpf('0.1939')
CRIT_EXP_2D = "2.27 ± 0.41i"
G_STAR_4D_LO = mp.mpf('0.1')      # 四维文献区间（方案依赖，仅作量级参考）
G_STAR_4D_HI = mp.mpf('1.0')

add("A-02", "A AS 基线", "库内既有 AS 读数回链（不重算、不改）",
    "本库的 NGFP 读数是什么、是几维的",
    "INFO",
    "回链 `04_公共成果/算法联盟_全维自洽与归一化/数据/OpenUFT统一场论v9.3_二维FRG非高斯不动点复现卷_2026-10-10.md`："
    " **g* = %s、λ* = %s、‖β‖ = 2.2e-16、临界指数 %s、相关维数 = 2**（±15%% 扫描存在性 9/9）；"
    "台账 J21 另记 eta_N* = -2、2 个相关方向、临界指数 2.3525 ± 2.3493i。"
    " ⚠ 口径必须同时引用：这是**二维** toy 的复现，不是四维 AS。"
    " 本层只把它作为'AS 机制在库内已被机器验证过'的证据，**不把它外推为四维的 ghat* 数值**"
    % (ns(G_STAR_2D, 6), ns(LAM_STAR_2D, 6), CRIT_EXP_2D))

# 冻结标度 vs 统一标度
MU_EQ_25 = M_PL_GEV * mp.sqrt(1 / mp.mpf('25'))
MU_EQ_47 = M_PL_GEV * mp.sqrt(1 / mp.mpf('47'))
MIS_A = MU_EQ_25 / M23                    # 相对 SM 的 M_23
MIS_B = MU_EQ_25 / mp.mpf('2e16')         # 相对典型 SUSY-GUT 统一点

add("A-03", "A AS 基线", "冻结标度与统一标度的错配（数值）",
    "AS 的冻结发生在哪个标度、与规范统一点差多少",
    "FAIL",
    "AS 的过渡（进入 NGFP 吸引域）发生在普朗克标度附近。而四力共点要求 alpha_G = alpha_GUT，"
    "即 ghat = alpha_GUT ⇒ mu = M_Pl sqrt(alpha_GUT)：alpha_GUT = 1/25 给 mu = %s GeV，"
    "1/47 给 mu = %s GeV。"
    " 规范统一点却在 %s GeV（SM 一圈 M_23）或 ~2e16 GeV（典型 SUSY 口径）。"
    " ==> 错配：共点所需标度比规范统一点高 %s 倍（对 M_23）或 %s 倍（对 2e16）。"
    " 也就是说：**在规范力真正统一的标度上，引力还没有冻结**，仍在按 (mu/M_Pl)^2 增长"
    % (ns(MU_EQ_25, 6), ns(MU_EQ_47, 6), ns(M23, 6), ns(MIS_A, 6), ns(MIS_B, 6)))

add("A-04", "A AS 基线", "在统一标度上引力仍未冻结（复算第 12 层 W-19 是否被 AS 改变）",
    "AS 是否拆掉了第 12 层'引力太弱'这条门槛",
    "FAIL",
    "在 M_23 = %s GeV：ghat = (M/M_Pl)^2 = %s，而 alpha_GUT = 1/47 = %s ⇒ 引力弱 %s 倍；"
    "在 2e16 GeV：ghat = %s，对 1/25 = %s ⇒ 弱 %s 倍（与既有台账 C16 的 1.3e4 同量级）。"
    " ==> **AS 没有拆掉这条门槛**：冻结发生在更高标度，在规范统一点上引力仍处于经典增长段，"
    "第 12 层 W-19 的结论（弱 337x ~ 1.49e4 x）在 AS 下**原样成立**。"
    " AS 改变的是 Planck 以上的行为，而门槛卡在 Planck 以下"
    % (ns(M23, 6), ns(GHAT_M23, 6), ns(1 / mp.mpf('47'), 4), ns((1 / mp.mpf('47')) / GHAT_M23, 6),
       ns(GHAT_2E16, 6), ns(1 / mp.mpf('25'), 4), ns((1 / mp.mpf('25')) / GHAT_2E16, 6)))

# =================================================================
# §B 定理 T3：引力修正的普适性 ⇒ 不能制造交点
# =================================================================
# 参数化：引力对 alpha_i^{-1} 跑动的修正  d(alpha_i^{-1})/dln mu |= -(a_i/2 pi) ghat
# 累积（经典段 ghat = (mu/M_Pl)^2）：∫ ghat dln mu = ghat(M)/2  ⇒ Δ(alpha_i^{-1}) = -(a_i/4 pi) ghat(M)
a1, a2, a3 = sp.symbols('a1 a2 a3')
mu_v, Mpl_v = sp.Symbol('mu', positive=True), sp.Symbol('M_Pl', positive=True)
ghat_expr = (mu_v / Mpl_v) ** 2
integ = sp.integrate(ghat_expr / mu_v, (mu_v, sp.Symbol('mu0', positive=True), mu_v))
sym_diff_12 = sp.simplify(-a1 / (2 * mp.pi) * integ - (-a2 / (2 * mp.pi) * integ))

add("B-01", "B 普适性定理 T3", "引力对规范耦合跑动的修正形式与累积量（符号积分）",
    "引力修正如何进入三个 alpha^{-1} 的跑动",
    "PASS",
    "取通用参数化 d(alpha_i^{-1})/d ln mu |_grav = -(a_i/2 pi) ghat（a_i 为圈系数级 O(1) 常数）。"
    "经典段 ghat = (mu/M_Pl)^2，符号积分 ∫ ghat d ln mu = %s ⇒ 累积修正 Δ(alpha_i^{-1}) = -(a_i/4 pi) ghat(M)。"
    " 两耦合之差 = %s"
    " ==> 若 a_1 = a_2 则该差恒为 0：**普适修正不产生任何相对位移**"
    % (str(sp.simplify(integ)), str(sp.factor(sym_diff_12))))

# 数值反证：需要多大的 |a1 - a2|
need_da_classic = DELTA_A_INV * 4 * mp.pi / GHAT_M23
need_da_frozen = DELTA_A_INV * 4 * mp.pi / G_STAR_2D

add("B-02", "B 普适性定理 T3", "普适性定理：a_1 = a_2 = a_3 ⇒ 只整体平移、不改交点",
    "引力若普适耦合（看不见内部指标），能否把'不共点'变成'共点'",
    "FAIL",
    "引力通过与 T_{mu nu} 耦合、经由量纲-2 算符进入物质扇区，**看不见规范群的内部指标**"
    "（这正是等效原理/普适耦合的内容）⇒ 自然预期 a_1 = a_2 = a_3 = a。"
    " 此时三个 alpha_i^{-1} 被减去同一个 (a/4 pi) ghat(M) ⇒ 三者的**差不变** ⇒ 交点结构完全不变。"
    " ==> **普适引力修正不能制造交点**。这与第 88 章 C5 同型：那里是完整物质族 Δb ∝ (1,1,1) ⇒ h_ij ≡ 0"
    "（'只整体平移、永不相交'）；这里是引力修正 Δa ∝ (1,1,1) ⇒ 同样只整体平移、永不相交。"
    " 同型论证在两条独立路径上互相印证 ⇒ 该结论不是本层的孤立判词")

add("B-03", "B 普适性定理 T3", "数值反证：要制造共点需多大的 |a_1 - a_2|（决定性）",
    "放弃普适性、让引力分辨内部指标，需要多大的系数分裂",
    "FAIL",
    "M_23 处 alpha_1 与 alpha_2/alpha_3 的差 Δ = %s 必须被引力修正抹平："
    "|Δa| × ghat(M)/(4 pi) = Δ ⇒ |a_1 - a_2| = Δ × 4 pi / ghat(M)。"
    " 经典段（ghat(M_23) = %s）：**|a_1 - a_2| = %s**；"
    " 假设冻结段（取二维 g* = %s 作乐观上限）：**|a_1 - a_2| = %s**。"
    " 而 a_i 是**圈系数级 O(1)** 的量（单圈修正的典型量级）。"
    " ==> 需要的分裂比自然量级大 %s ~ %s 倍 ⇒ 即便放弃普适性，也无法用任何合理的圈系数兑现。"
    " 这是本层最硬的一条数值判据：它不依赖 AS 的截断方案，只依赖 Δ 与 ghat 的量级"
    % (ns(DELTA_A_INV, 6), ns(GHAT_M23, 6), ns(need_da_classic, 6),
       ns(G_STAR_2D, 6), ns(need_da_frozen, 6),
       ns(need_da_frozen / 10, 5), ns(need_da_classic / 10, 5)))

add("B-04", "B 普适性定理 T3", "自由度账本：引力修正的两种用法都不通向预测力",
    "把 a_i 当可调参数会怎样",
    "FAIL",
    "用法一（普适 a）：1 个自由度，但 T3 证明它只整体平移 ⇒ 交点不变 ⇒ **零效果**；"
    "用法二（a_1, a_2, a_3 独立）：3 个自由度对 2 个约束（三耦合共点）+ M_GUT 自由"
    " ⇒ 有无穷多解 ⇒ **可拟合但零预测力**（与第 12 层 T2 分支 (c)、第 8 层 B-03 同型）。"
    " ==> 与第 12 层 T1/T2 合起来看：**'引入一个新机制来救耦合统一'这件事，要么无效、要么零预测力**，"
    " 二者必居其一。这是本层对第 12 层'每闭合一条硬伤至少一个自由度'的一次独立复现")

# =================================================================
# §C ghat* 供需对账（与第 12 层 T2 同法，用于引力侧）
# =================================================================
need_gstar_A = 1 / mp.mpf('25')
need_gstar_B = 1 / mp.mpf('47')
gap_2d_A = G_STAR_2D / need_gstar_A
gap_4dlo_A = G_STAR_4D_LO / need_gstar_A
gap_4dhi_A = G_STAR_4D_HI / need_gstar_A

add("C-01", "C ghat* 供需对账", "供给侧：四力共点需要 ghat* 取什么值",
    "若引力冻结，其常数值必须落在哪里",
    "INFO",
    "四力共点要求 alpha_G = alpha_GUT ⇒ ghat* = alpha_GUT："
    "口径 A（alpha_GUT = 1/25）需 ghat* = %s；口径 B（1/47）需 ghat* = %s。"
    " ==> 需求侧是一个 O(10^-2) 的纯数" % (ns(need_gstar_A, 4), ns(need_gstar_B, 4)))

add("C-02", "C ghat* 供需对账", "供需对比：库内/文献的 g* 与需求的差距（口径依赖，诚实列区间）",
    "AS 给出的 g* 是否恰好落在需求值上",
    "BOUNDARY",
    "供给：库内二维复现 g* = %s；四维文献取量级区间 %s ~ %s（**方案/截断依赖**，本层不作单一取值）。"
    " 与需求 ghat* = %s 相比：二维口径差 %s 倍；四维区间给 %s ~ %s 倍。"
    " ==> 判 BOUNDARY 而非 FAIL：**差距只有约 1~2 个量级，且 g* 本身是方案依赖量**，"
    " 不能据此断言'AS 的 g* 与统一需求不相容'；能断言的只是'库内没有四维读数，无法对该对账下判词'。"
    " ⚠ 关键提醒：即便 g* 恰好落在需求值上，A-03/A-04 的**标度错配**仍然独立成立"
    "（冻结发生在 Planck 以上，而统一点在 Planck 以下）⇒ g* 数值匹配并不自动给出四力共点"
    % (ns(G_STAR_2D, 6), ns(G_STAR_4D_LO, 4), ns(G_STAR_4D_HI, 4), ns(need_gstar_A, 4),
       ns(gap_2d_A, 5), ns(gap_4dlo_A, 5), ns(gap_4dhi_A, 5)))

add("C-03", "C ghat* 供需对账", "若把 ghat* 当作可调输入：退化为拟合",
    "用 g* 去凑统一会怎样",
    "FAIL",
    "若允许 ghat* 自由取值以匹配 alpha_GUT，则它是 1 个自由度对 1 个观测量（引力-规范相对强度）"
    " ⇒ 与第 12 层 T2 分支 (c) 同型：**自由度 1 对观测量 1 且满射 = 零预测力**。"
    " 更严重的是：g* 在 AS 中本应是**由 FRG 算出来的输出**（方案依赖但非自由），"
    " 把它当输入等于把 AS 的可证伪内容（'能否算出正确的 g*'）直接取消。"
    " ==> 这条出路付的代价是**取消 AS 本身的科学内容**，账比第 12 层任何一条都贵")

# =================================================================
# §D 闭环死锁（本层的核心综合论证）
# =================================================================
TAU_SK = mp.mpf('2.4e34')
TAU_X9 = mp.mpf('1.65e31')
M_GUT_MIN = mp.mpf('1e15') * (TAU_SK / TAU_X9) ** mp.mpf('0.25')
tau_at_mueq = TAU_X9 * (MU_EQ_25 / mp.mpf('1e15')) ** 4

add("D-01", "D 闭环死锁", "四步闭环：含引力的四力共点为何死锁",
    "从'要共点'出发，逐步推出必要条件，看是否自相矛盾",
    "FAIL",
    "① 含引力共点 ⇒ alpha_G(M) = alpha_GUT ⇒ M = M_Pl sqrt(alpha_GUT) = %s GeV（A-03）；"
    "② 但规范耦合一圈跑动的交点在 %s GeV ⇒ 规范力**在该标度并不统一**（差 %s 倍）；"
    "③ 要让规范力在 %s GeV 统一，必须修改规范跑动 ⇒ 引入引力修正（唯一可用机制）；"
    "④ 但引力修正若普适 ⇒ 只整体平移、不改交点（T3）；若非普适 ⇒ 需 |Δa| ~ %s（B-03）远超圈系数量级。"
    " ==> **闭环死锁**：每一步的唯一出路都被下一步堵死。这不是参数没调好，是四个必要条件互不相容"
    % (ns(MU_EQ_25, 6), ns(M23, 6), ns(MIS_A, 6), ns(MU_EQ_25, 6), ns(need_da_classic, 5)))

add("D-02", "D 闭环死锁", "质子衰变门槛在 AS-GUT 下是否仍成立（错配的另一面）",
    "若强行把统一点抬到 Planck 附近，质子衰变是否放行",
    "INFO",
    "统一点抬到 %s GeV 后，tau_p ∝ M^4 ⇒ 以 X9 标定外推 tau = %s yr，"
    "远超 Super-K 下限 %s yr ⇒ **质子衰变这条门槛会放行**（不再是障碍）。"
    " 但另一条更硬：实验下限只要求 M_GUT > %s GeV，而共点需要 M = %s GeV（高 %s 倍）"
    " ⇒ 门槛放行与'规范耦合是否真的在该标度统一'是两件事：实验不禁止，但**跑动不支持**。"
    " ==> 本条判 INFO：质子衰变不构成 AS-GUT 的障碍，障碍来自耦合跑动本身（D-01）"
    % (ns(MU_EQ_25, 6), ns(tau_at_mueq, 6), ns(TAU_SK, 4), ns(M_GUT_MIN, 6),
       ns(MU_EQ_25, 6), ns(MU_EQ_25 / M_GUT_MIN, 5)))

add("D-03", "D 闭环死锁", "sin^2 theta_W 的 182 sigma 是否被 AS 改动",
    "引力修正能否救最小 SU(5) 的弱角预言",
    "FAIL",
    "第 12 层 W-20：GUT 预言 sin^2 theta_W = 0.20754 vs 实测 0.23121，差 %s sigma。"
    " 弱角是两个规范耦合之比的函数 ⇒ 只有**改变 alpha_1 与 alpha_2 的相对关系**才能改动它；"
    "而 T3 证明普适引力修正**恰好不改变相对关系**（只整体平移）。"
    " ==> AS 引力修正在普适情形下对 sin^2 theta_W 的贡献为**精确零**，182 sigma 原样保留。"
    " 这一条是 T3 的独立佐证：它把'普适 ⇒ 无相对位移'从理论论证变成了可观测量的直接判词"
    % (ns(mp.mpf('182.08'), 6)))

# =================================================================
# §E 判决与封闭谱更新
# =================================================================
add("E-01", "E 判决", "AS 出口能否攻克力统一（本层总判）",
    "把 AS 跑动接入 SM/GUT 后，四力能否共点",
    "FAIL",
    "三方面独立否决：① 标度错配（A-03/A-04）：冻结在 Planck 以上、统一点在 Planck 以下 ⇒ 引力在统一点仍弱 337x~1.49e4x；"
    "② 普适性定理 T3（B-02/B-03）：引力修正看不见内部指标 ⇒ 只整体平移、不改交点，强行分裂需 |Δa| ~ %s；"
    "③ sin^2 theta_W 的 182 sigma 不受影响（D-03）。"
    " ==> **AS 出口不能攻克力统一**。但这个 FAIL 的对象是'AS 作为力统一出口'，不是 AS 本身"
    % (ns(need_da_classic, 5)))

add("E-02", "E 判决", "AS 本身的状态：未被否证，且本层不动它（诚实区分）",
    "AS 作为量子引力候选是否与'作为统一出口'同命运",
    "BOUNDARY",
    "AS 是**机器验证过的可证伪候选**：库内 v9.3 已独立复现二维 NGFP（g*=%s、λ*=%s、‖β‖=2.2e-16、"
    "临界指数 %s、±15%% 扫描存在性 9/9）；台账 J21 记 eta_N*=-2、2 个相关方向。"
    " 本层**没有否证、也没有重算**这些读数，只引用。"
    " 判 BOUNDARY 的理由：AS 作为量子引力（UV 完备）候选仍开放，它在本层被否定的只是"
    "**'它能顺带解决力统一'这一附带主张**。"
    " 附带一条既有边界：AS 的 Higgs 126 GeV 接触点已被 J22/J23 判为条件性事后拟合"
    "（是带不是点，126.0~133.4 GeV，实测 125.18 落亚稳区）⇒ AS 与 SM 的接触点本身就还很脆弱"
    % (ns(G_STAR_2D, 6), ns(LAM_STAR_2D, 6), CRIT_EXP_2D))

add("E-03", "E 判决", "第 12 层封闭谱的更新：三条缝现在剩几条",
    "本层做完后，力的统一的剩余出口清单",
    "FAIL",
    "第 12 层 W-31 剩三条缝：① 超对称 ② 涌现规范/离散拓扑序 ③ **AS 引力跑动（本层）**。"
    " 本层结论：缝③已被判死（E-01），但**不是以'AS 错了'的方式**，而是以"
    "'即便 AS 成立，它也不能制造四力交点'的方式 ⇒ 该缝关闭，AS 本身转列 BOUNDARY（E-02）。"
    " ==> 封闭谱更新为：**超对称（唯一绕开 Coleman-Mandula 的既有通道，库内 0 条实现）** 与"
    " **涌现规范/离散拓扑序（本库零建模）** 两条，外加一条非本层范围的观察项："
    " AS 与 SM 的接触点（Higgs 质量带）本身仍待独立验证（J22/J23）。"
    " 两条缝的共同特征不变：新结构重量都不小于直接公设一个内部规范群")

# =================================================================
# 输出
# =================================================================
print()
for r in ROWS:
    print("[%s] %-5s | %-36s | %s" % (r["verdict"], r["id"], r["name"][:36],
                                      r["detail"][:140].replace("\n", " ")))
print()
n_fail = sum(1 for r in ROWS if r["verdict"] == "FAIL")
n_pass = sum(1 for r in ROWS if r["verdict"] == "PASS")
n_bd = sum(1 for r in ROWS if r["verdict"] == "BOUNDARY")
n_info = sum(1 for r in ROWS if r["verdict"] == "INFO")
print("=" * 100)
print("汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d" % (len(ROWS), n_pass, n_fail, n_bd, n_info))
print("总耗时 %.1fs" % (time.time() - T0))
print("=" * 100)

# =================================================================
# 不可回退基线自检
# =================================================================
GUARD = [
    ("M_Pl 落在 1.2209e19±0.1%", abs(M_PL_GEV / mp.mpf('1.2209e19') - 1) < mp.mpf('1e-3')),
    ("alpha^-1(M_Z) 三值在标准区间",
     abs(A1_INV - mp.mpf('59.0')) < mp.mpf('0.5') and abs(A2_INV - mp.mpf('29.6')) < mp.mpf('0.5')
     and abs(A3_INV - mp.mpf('8.47')) < mp.mpf('0.1')),
    ("M_23 落在 1e16~1e17", mp.mpf('1e16') < M23 < mp.mpf('1e17')),
    ("Δ(alpha^-1) at M_23 落在 5~20", mp.mpf('5') < DELTA_A_INV < mp.mpf('20')),
    ("ghat(M_23) 落在 1e-6~1e-4", mp.mpf('1e-6') < GHAT_M23 < mp.mpf('1e-4')),
    ("NGFP 条件给出 eta_N* = -2（符号）", eta_star == [-2]),
    ("beta|_{eta_N=-2} = 0（机器零）", beta_at_star == 0),
    ("引力弱倍数（M_23 口径）落在 1e2~1e5",
     mp.mpf('1e2') < (1 / mp.mpf('47')) / GHAT_M23 < mp.mpf('1e5')),
    ("共点所需标度 MU_EQ 落在 1e18~1e19", mp.mpf('1e18') < MU_EQ_25 < mp.mpf('1e19')),
    ("标度错配 > 20 倍", MIS_A > 20),
    ("所需 |Δa|（经典段）> 1e5", need_da_classic > mp.mpf('1e5')),
    ("所需 |Δa|（冻结乐观段）> 100", need_da_frozen > mp.mpf('100')),
    ("质子衰变 M_GUT 下限 > 1e15", M_GUT_MIN > mp.mpf('1e15')),
    ("库内二维 g* = 0.9042 未被本层改写", abs(G_STAR_2D - mp.mpf('0.9042')) < mp.mpf('1e-10')),
    ("普适修正的两耦合之差在 a1=a2 时恒零（符号）",
     sp.simplify(sym_diff_12.subs({a1: a2})) == 0),
]
bad = [g[0] for g in GUARD if not g[1]]
for name, ok in GUARD:
    if not ok:
        print("[GUARD-FAIL] %s" % name)
if bad:
    print("[自检] %d/%d 在位，%d 条失守：%s" % (len(GUARD) - len(bad), len(GUARD), len(bad), bad))
else:
    print("[自检] %d 条不可回退基线全部在位" % len(GUARD))

# =================================================================
# 落盘
# =================================================================
out = {
    "meta": {
        "layer": "第 13 层：AS 引力跑动接入 SM/GUT —— 四力交点诊断",
        "precision": "mpmath 40 位 + sympy 符号积分",
        "counts": {"total": len(ROWS), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bd, "INFO": n_info},
        "guard": {"total": len(GUARD), "passed": len(GUARD) - len(bad), "failed": bad},
    },
    "anchors": {
        "M_Pl_GeV": ns(M_PL_GEV, 10),
        "M_23_GeV": ns(M23, 10), "M_12_GeV": ns(M12, 10),
        "delta_alpha_inv_at_M23": ns(DELTA_A_INV, 10),
        "ghat_at_M23": ns(GHAT_M23, 10), "ghat_at_2e16": ns(GHAT_2E16, 10),
        "alpha_G_weaker_at_M23": ns((1 / mp.mpf('47')) / GHAT_M23, 8),
        "alpha_G_weaker_at_2e16": ns((1 / mp.mpf('25')) / GHAT_2E16, 8),
        "mu_needed_for_4force_meeting_GeV": {"alpha_GUT_1_25": ns(MU_EQ_25, 8),
                                             "alpha_GUT_1_47": ns(MU_EQ_47, 8)},
        "scale_mismatch_vs_M23": ns(MIS_A, 8),
        "scale_mismatch_vs_2e16": ns(MIS_B, 8),
        "need_abs_da_classic_segment": ns(need_da_classic, 8),
        "need_abs_da_frozen_optimistic": ns(need_da_frozen, 8),
        "gstar_2d_library": ns(G_STAR_2D, 8), "lambda_star_2d_library": ns(LAM_STAR_2D, 8),
        "gstar_needed_for_unification": {"alpha_GUT_1_25": ns(need_gstar_A, 6),
                                         "alpha_GUT_1_47": ns(need_gstar_B, 6)},
        "M_GUT_lower_bound_GeV": ns(M_GUT_MIN, 8),
        "tau_p_at_mu_eq_yr": ns(tau_at_mueq, 8),
        "eta_N_star": -2,
    },
    "rows": ROWS,
}
jp = os.path.join(DATA, "v_eq_c_AS引力四力交点诊断_第13层.json")
with open(jp, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

L = []
L.append("# 第 13 层：AS 引力跑动接入 SM/GUT —— 四力交点诊断")
L.append("")
L.append("> 精度：mpmath 40 位 + sympy 符号积分 ｜ 判据 %d 条（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）"
         % (len(ROWS), n_pass, n_fail, n_bd, n_info))
L.append("> guard 自检：%d/%d 条不可回退基线在位" % (len(GUARD) - len(bad), len(GUARD)))
L.append("")
L.append("## 关键锚点")
L.append("")
L.append("| 量 | 值 |")
L.append("|---|---|")
for k, v in out["anchors"].items():
    L.append("| %s | %s |" % (k, v))
L.append("")
L.append("## 判据明细")
L.append("")
cur = None
for r in ROWS:
    if r["section"] != cur:
        cur = r["section"]
        L.append("")
        L.append("### %s" % cur)
        L.append("")
    L.append("**[%s] %s ｜ %s**" % (r["verdict"], r["id"], r["name"]))
    L.append("")
    L.append("- 判据：%s" % r["criterion"])
    L.append("- 结论：%s" % r["detail"])
    L.append("")
L.append("## 诚实边界")
L.append("")
L.append("- **本层否证的是'AS 作为力统一出口'，不是 AS 本身**：AS 是机器验证过的可证伪量子引力候选，"
         "库内 v9.3 复现的二维 NGFP 本层只引用、未重算、未改；")
L.append("- 库内**只有二维** NGFP 读数（g*=0.9042 / λ*=0.1939）。四维 g* 是方案/截断依赖量，"
         "本层只给量级区间 0.1~1 并判 BOUNDARY，**未把二维读数外推为四维结论**；")
L.append("- B-01 的引力修正形式 d(α_i^{-1})/dlnμ = -(a_i/2π)ĝ 是通用参数化，"
         "不同 AS 文献的系数归一化与符号约定不同（引力贡献的符号在文献中本身有争议），"
         "但 B-02 的普适性结论**只依赖 a_i 相等**，与具体归一化无关；")
L.append("- D-02 的质子衰变外推用 τ ∝ M⁴ 并以台账 X9 标定，应读作量级而非精确寿命；")
L.append("- 超对称与涌现规范两条缝本层**未做**，不得因本层结论而记为已关闭。")

mp_path = os.path.join(DATA, "v_eq_c_AS引力四力交点诊断_第13层.md")
with open(mp_path, "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("已写出：数据/%s + .json" % os.path.basename(mp_path))
