# -*- coding: utf-8 -*-
"""
v = c 求导链 · 第 14 层：超对称出口 —— 可实现性与定价审计
================================================================================
位置：承接第 13 层 `v_eq_c_AS引力跑动接入四力交点诊断_第13层.py`。
第 12 层 W-31 剩三条缝，第 13 层关掉了缝③（AS 引力跑动），剩两条：
  ① **超对称**（HLS 绕开 Coleman-Mandula 的唯一既有通道）  ② 涌现规范 / 离散拓扑序
本层攻缝①。

本层与前面几层的根本不同（必须先说清）
--------------------------------------
第 ⑧/⑨/⑫/⑬ 层的判词几乎全是 FAIL。本层会出现**真实的 PASS**：
  一圈 MSSM 下三个规范耦合**真的几乎共点**（max/min = 1.139，对比 SM 的 9384.8），
  且 sin^2 theta_W 的 GUT 预言从非超对称 SU(5) 的 **182 sigma** 降到 **2.32 sigma**。
这是本链第一次有方向在"耦合统一"这一条上真正做到了。必须原样记录，不得因为
"本库不持有超对称"就把成功写成失败；同样也不得因为有了这两条 PASS 就省略代价。

方法
----
只用一圈 RGE（教科书 β 系数 [A]）：SM b=(41/10, -19/6, -7)，MSSM b=(33/5, 1, -3)，
低能锚 α^-1(M_Z)=(59.02, 29.58, 8.47)。用 GUT 关系 α_1=α_2=α_3 反解 sin^2 theta_W：
  s^2 = [(3/5)A + k α_s^{-1}] / [A((8/5)+k)],  k = (b_1-b_2)/(b_2-b_3)。
自校验：该式对 SM 给 0.20756，与既有台账 X16 的 0.20754（182 sigma）吻合 ⇒ 公式与既有口径一致。

诚实边界写在最前
----------------
本层**不提出新方程、不构造超对称模型**；所有超对称读数（β 系数、LHC 下限、参数计数）
均为教科书/实验外部事实 [A]，本层只做代入、对比与定价。
"超对称能做到"不等于"本库做到了" —— 本库现役方程树里超对称只有 2 行构造、LHC 可判谱 0 条。

精度：mpmath 40 位
================================================================================
"""
import json
import os
import sys
import time

import mpmath as mp

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

mp.mp.dps = 40
T0 = time.time()

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "数据")
os.makedirs(DATA, exist_ok=True)

# ============================== 低能锚点 ==============================
MZ = mp.mpf('91.1876')            # GeV
A_INV = mp.mpf('127.952')         # α_em^{-1}(M_Z)
S2W_EXP = mp.mpf('0.23121')       # 实测 sin^2 θ_W (MS-bar)
S2W_SIG = mp.mpf('1.3e-4')        # 与第 12 层 W-20 同口径的不确定度
AS_MZ = mp.mpf('0.1180')          # α_s(M_Z)

A1_INV = mp.mpf('0.6') * (1 - S2W_EXP) * A_INV
A2_INV = S2W_EXP * A_INV
A3_INV = 1 / AS_MZ
A0 = [A1_INV, A2_INV, A3_INV]

# 一圈 β 系数（教科书 [A]）
B_SM = [mp.mpf('41') / 10, -mp.mpf('19') / 6, mp.mpf('-7')]     # SM
B_MSSM = [mp.mpf('33') / 5, mp.mpf('1'), mp.mpf('-3')]          # MSSM

# 引力
hbar = mp.mpf('1.054571817e-34')
c = mp.mpf('299792458')
G = mp.mpf('6.67430e-11')
GeV = mp.mpf('1.602176634e-10')
M_PL_GEV = mp.sqrt(hbar * c / G) * c ** 2 / GeV


def ns(x, n=6):
    return mp.nstr(mp.mpf(x), n)


def run_unification(b):
    """一圈跑动下两两交点、跨度、平均 M_GUT、α_GUT^{-1}"""
    ms = {}
    for (i, j) in ((0, 1), (0, 2), (1, 2)):
        L = (A0[i] - A0[j]) / ((b[i] - b[j]) / (2 * mp.pi))
        ms[(i, j)] = MZ * mp.e ** L
    vals = list(ms.values())
    spread = max(vals) / min(vals)
    mgut = sum(vals) / 3
    ai_at = [A0[i] - b[i] / (2 * mp.pi) * mp.log(mgut / MZ) for i in range(3)]
    agut_inv = sum(ai_at) / 3
    return ms, spread, mgut, agut_inv, ai_at


def s2_prediction(b):
    """GUT 关系 α_1=α_2=α_3 反解 sin^2 θ_W(M_Z)"""
    k = (b[0] - b[1]) / (b[1] - b[2])
    num = mp.mpf('0.6') * A_INV + k / AS_MZ
    den = A_INV * (mp.mpf('1.6') + k)
    return k, num / den


MS_SM, SP_SM, MG_SM, AGI_SM, _ = run_unification(B_SM)
MS_M, SP_M, MG_M, AGI_M, AI_M = run_unification(B_MSSM)
K_SM, S2_SM = s2_prediction(B_SM)
K_M, S2_M = s2_prediction(B_MSSM)
SIG_SM = abs(S2_SM - S2W_EXP) / S2W_SIG
SIG_M = abs(S2_M - S2W_EXP) / S2W_SIG

A_G_AT_MG = (MG_M / M_PL_GEV) ** 2
WEAK_M = (1 / AGI_M) / A_G_AT_MG

ROWS = []


def add(wid, sec, name, crit, verdict, detail):
    ROWS.append(dict(id=wid, section=sec, name=name, criterion=crit,
                     verdict=verdict, detail=detail))


print("=" * 100)
print("第 14 层：超对称出口 —— 可实现性与定价审计")
print("=" * 100)
print("低能锚 α^-1(M_Z) = (%s, %s, %s)" % (ns(A1_INV, 7), ns(A2_INV, 7), ns(A3_INV, 7)))
print("SM   一圈：跨度 %s ｜ M_GUT %s ｜ α_GUT^-1 %s ｜ sin²θ_W %s (%s σ)"
      % (ns(SP_SM, 6), ns(MG_SM, 6), ns(AGI_SM, 6), ns(S2_SM, 7), ns(SIG_SM, 5)))
print("MSSM 一圈：跨度 %s ｜ M_GUT %s ｜ α_GUT^-1 %s ｜ sin²θ_W %s (%s σ)"
      % (ns(SP_M, 6), ns(MG_M, 6), ns(AGI_M, 6), ns(S2_M, 7), ns(SIG_M, 5)))
print("=" * 100)

# =================================================================
# §S 超对称为何能绕开 Coleman-Mandula
# =================================================================
add("S-01", "S 绕开 CM", "Haag–Łopuszański–Sohnius：超对称为何是唯一绕开 CM 的既有通道",
    "Coleman-Mandula 禁止内部对称与时空对称的非直积融合，超对称如何绕过",
    "PASS",
    "Coleman–Mandula 的论证依赖**普通李代数**的分次结构；Haag–Łopuszański–Sohnius (1975) 证明："
    "把李代数放宽为**分次李代数**（Z_2 分次，含反对易子）后，唯一允许的新对称生成元是"
    "**自旋 1/2 的超荷 Q**（且 {Q, Q̄} = 2σ^μ P_μ，即超荷的反对易子给出平移）。"
    " ⇒ 超对称在**数学上确实**绕开了 CM：这是第 82 章 §82.8.2 列出的四个出口中"
    "**唯一被教科书严格证明可行的那一个**（其余三个：GUT 不撞 CM 但不含引力、弦论靠无限高自旋塔、"
    "演生规范未证）。本条为 [A] 外部教科书结论，本层引用不自推")

add("S-02", "S 绕开 CM", "库内超对称的现状（回链既有，不重算）",
    "本库持有多少超对称、是否已实现",
    "INFO",
    "回链对称性定理适用域裁定 §二 裁定 3 / §八 与第 82 章 D6：库内超对称**构造行 = 8**，"
    "落在现役方程树的**只有 2 行**，LHC 可判谱 **0 条**。"
    " ⇒ 超对称在库内是**未被取用（不是被否证）**。本层的最小代价口径沿用既有："
    "在 `07_统一场方程` 写出 {Q, Q̄} = 2σ^μ P_μ 的**实现**（不是复述）+ LHC 可判谱。"
    " 本层不代劳实现，只审计'若取用它能换来什么、要付什么'")

# =================================================================
# §M MSSM 耦合统一（本层决定性计算）
# =================================================================
add("M-01", "M 耦合统一", "一圈 β 系数：SM 与 MSSM 的差别（教科书 [A]）",
    "两者的一圈跑动系数分别是什么",
    "INFO",
    "SM b = (%s, %s, %s)；MSSM b = (%s, %s, %s)。"
    " 关键差别：b_3 由 %s 变为 %s（绝对值变小 ⇒ QCD 的渐近自由被超伴子**减弱**），"
    "b_2 由负转正 ⇒ SU(2) 由渐近自由变为非渐近自由。"
    " 这三者的改变正是三耦合能否共点的全部原因：它们改变了三条跑动直线的**相对斜率**"
    % (ns(B_SM[0], 5), ns(B_SM[1], 5), ns(B_SM[2], 5),
       ns(B_MSSM[0], 5), ns(B_MSSM[1], 5), ns(B_MSSM[2], 5),
       ns(B_SM[2], 5), ns(B_MSSM[2], 5)))

add("M-02", "M 耦合统一", "★ 三耦合是否共点：MSSM vs SM（本层最硬的一条）",
    "一圈跑动下三个两两交点是否重合",
    "PASS",
    "SM：M_12 = %s、M_13 = %s、M_23 = %s GeV ⇒ **跨度 max/min = %s 倍（不共点）**；"
    "MSSM：M_12 = %s、M_13 = %s、M_23 = %s GeV ⇒ **跨度 max/min = %s 倍（几乎共点）**。"
    " ==> 跨度改善 %s 倍。这是本链第一次出现的有力 PASS：**超对称确实让三个规范耦合统一了**，"
    "而且用的是标准教科书 β 系数、标准低能锚，没有任何本库自定义成分。"
    " 判 PASS 的依据是'该机制做到了它声称要做的事'，不是'本库采用了它'"
    % (ns(MS_SM[(0, 1)], 6), ns(MS_SM[(0, 2)], 6), ns(MS_SM[(1, 2)], 6), ns(SP_SM, 6),
       ns(MS_M[(0, 1)], 6), ns(MS_M[(0, 2)], 6), ns(MS_M[(1, 2)], 6), ns(SP_M, 6),
       ns(SP_SM / SP_M, 6)))

add("M-03", "M 耦合统一", "MSSM 的统一能标与统一耦合",
    "共点发生在哪个标度、耦合多强",
    "PASS",
    "M_GUT ≈ %s GeV（三交点均值，三值相差 <14%%）；α_GUT^{-1} ≈ %s ⇒ α_GUT ≈ %s；"
    "在 M_GUT 处三耦合 α^{-1} = (%s, %s, %s)（彼此相差 < 0.06）。"
    " ==> 该标度落在质子衰变实验下限（第 12 层 W-18 外推 %s GeV）**之上**，"
    "即最小 SUSY GUT 的统一点与 Super-K 不冲突（不同于第 12 层里被排除的 SM 的 M_12 = %s GeV）"
    % (ns(MG_M, 6), ns(AGI_M, 6), ns(1 / AGI_M, 6),
       ns(AI_M[0], 6), ns(AI_M[1], 6), ns(AI_M[2], 6),
       ns(mp.mpf('6.1756379e15'), 6), ns(MS_SM[(0, 1)], 6)))

add("M-04", "M 耦合统一", "★ sin²θ_W：从 182σ 降到 2.32σ（含自校验）",
    "GUT 关系对弱角的预言在 SM 与 MSSM 下分别与实测差多少",
    "PASS",
    "由 GUT 关系 α_1=α_2=α_3 反解：s² = [(3/5)A + k α_s^{-1}]/[A((8/5)+k)]，k=(b_1−b_2)/(b_2−b_3)。"
    " SM：k = %s ⇒ **s² = %s**（实测 %s）⇒ 差 %s；"
    "MSSM：k = %s ⇒ **s² = %s** ⇒ 差 %s。"
    " **自校验：本式对 SM 给 %s，与既有台账 X16/X7 的非超对称 SU(5) 读数 0.20754（−182σ）吻合**"
    "（相对差 %s）⇒ 本层公式与既有口径一致，不是新造的尺子。"
    " ==> 这是超对称出口**第二个真实 PASS**：弱角预言由 182σ 改善到 %s σ（改善 %s 倍）。"
    " ⚠ 口径必须同时引用：一圈理想化（所有超伴子置于 M_Z）；真实谱的阈值修正会带来 ~10^-3 量级移动，"
    "故 2.32σ 应读作'一圈量级符合'而非精确预言"
    % (ns(K_SM, 6), ns(S2_SM, 8), ns(S2W_EXP, 6), ns(SIG_SM, 6),
       ns(K_M, 6), ns(S2_M, 8), ns(SIG_M, 6),
       ns(S2_SM, 8), ns(abs(S2_SM / mp.mpf('0.20754') - 1), 3),
       ns(SIG_M, 5), ns(SIG_SM / SIG_M, 5)))

add("M-05", "M 耦合统一", "引力仍未并入：只统一了三个规范力",
    "MSSM 的统一点是否也包含引力",
    "FAIL",
    "在 MSSM 的 M_GUT = %s GeV 处 α_G = (M/M_Pl)² = %s，而 α_GUT = %s ⇒ **引力仍弱 %s 倍**"
    "（与既有台账 C16 的 1.3×10⁴ 同量级，交叉验证通过）。"
    " ==> **超对称统一的是三个规范力，不含引力**。这与第 82 章的能力边界一致"
    "（GUT 不撞 Coleman-Mandula，因为它统一的是内部因子彼此，与 Poincaré 直积）；"
    "也与第 13 层 A-04 同源：引力并入的门槛在**普朗克标度**，而规范统一点在 %s GeV（低约 %s 倍）。"
    " ⇒ 四力统一（含引力）在 MSSM 下**仍未达成**"
    % (ns(MG_M, 6), ns(A_G_AT_MG, 6), ns(1 / AGI_M, 6), ns(WEAK_M, 6),
       ns(MG_M, 6), ns(M_PL_GEV / MG_M, 5)))

# =================================================================
# §T 代价定价
# =================================================================
N_MSSM_SOFT = 105          # MSSM 一般软破缺参数数（教科书 [A]）
N_SU5_MIN = 4              # 直接公设最小 SU(5)：群 1 + 耦合 1 + 破缺表示 1 + 阈值 1

add("T-01", "T 代价定价", "自由度账本：+105 vs 直接公设内部群（验证第 82 章断言）",
    "取用超对称要付多少自由度，与'直接公设一个内部规范群'相比如何",
    "FAIL",
    "MSSM 的一般软破缺参数数 **%d** 个（3 个 gaugino 质量 + 各代标量质量平方 + 3 个 3×3 的 A 项矩阵"
    " + Bμ 等，**含全部味混合与 CP 相位**；教科书口径）。"
    "约束版本 CMSSM/mSUGRA 把它压到 5 个：m_0, m_{1/2}, A_0, tanβ, sign μ。"
    " 对照'直接公设一个内部规范群'（最小 SU(5)）：群 1 + 耦合 1 + 破缺表示 1 + 阈值 1 ≈ **%d** 个。"
    " ==> 代价比 = %s 倍。第 82 章 §82.8.2 的断言"
    "「每个出口的新结构重量都不小于直接公设一个内部规范群」在本层被**定量证实且远超**："
    "超对称是三条缝里最贵的那一条（即便用约束版本 5 个，仍不低于直接公设的 4 个）"
    % (N_MSSM_SOFT, N_SU5_MIN, ns(mp.mpf(N_MSSM_SOFT) / N_SU5_MIN, 5)))

add("T-02", "T 代价定价", "LHC 现状与自然性张力（外部实验事实 [A]）",
    "超伴子被观测到了吗、自然性窗口如何",
    "BOUNDARY",
    "LHC Run 2（ATLAS/CMS，简化模型口径）：gluino 质量下限约 **~2.3 TeV**、"
    "第一代 squark 约 ~1.8–2 TeV、stop 约 ~1.2 TeV 量级（具体值随衰变道与假设变，本层只读量级）。"
    " 而'自然性'（不 fine-tune 地得到 125 GeV Higgs）通常期望超伴子在 **~1 TeV 或更低**。"
    " ==> **little hierarchy（小等级）张力**：实验下限已压到 TeV 之上，自然窗口显著收缩。"
    " 判 BOUNDARY 而非 FAIL 的理由：**超对称未被证伪**——质量上限提高不等于排除，"
    "split SUSY / high-scale SUSY 等分支仍活着（代价是放弃自然性解释）。"
    " ⚠ 本层不代判'超对称是否已被排除'，那是实验进展与理论取舍共同决定的，且属科学哲学层")

add("T-03", "T 代价定价", "质子衰变 dim-5 通道（回链既有，不重算）",
    "SUSY GUT 是否撞质子衰变",
    "FAIL",
    "回链第 84 章 §84.6 / 第 88 章 §88.6：dim-5（色三重态 Higgs 交换）主导的 p → K⁺ ν̄ 通道"
    "依赖未观测的 sfermion 谱与色三重态 Yukawa，**须再抑制 10^-4 ~ 10^-3** 才不撞 Super-K；"
    "GMSB 等具体模型可达 τ ~ 10^34 yr 落入 Hyper-K/DUNE 区，但那是**模型相关的赌注**，"
    "不是公设 A1–A6 的必然预言。 ==> 超对称虽把 M_GUT 抬到 proton-safe 区（M-03），"
    "但**抬标度只解决了 dim-6（重规范玻色子交换），没解决 dim-5** ⇒ 该代价仍在账上")

add("T-04", "T 代价定价", "μ 问题与破缺机制：无第一性来源",
    "超对称自身的两个内部结构问题是否解决",
    "FAIL",
    "① **μ 问题**：MSSM 超势中的 μ H_u H_d 项，μ 应为 TeV 量级（ phenomenology 要求），"
    "但它是一个**超势里的质量参数**，与软破缺标度无关 ⇒ '为何 μ ~ M_SUSY 而非 M_Pl' 无第一性答案"
    "（NMSSM/Giudice–Masiero 等是**机制提案**，各自再引入新输入）。"
    " ② **破缺机制**：SUSY 必须在低能破缺（未观测到超伴子简并），但破缺机制"
    "（gravity / gauge / anomaly mediation …）**无第一性选择**，不同机制给出不同谱与不同代价。"
    " ==> 这两条合起来说明：超对称**把'耦合统一'做成了，但没有把它变成免费的**——"
    "它把问题从'耦合为何不统一'搬到了'μ 与破缺机制从哪来'")

# =================================================================
# §V 五判据总评（第 75 章口径）+ 总判
# =================================================================
five = [
    ("判据 1 单一规范结构", "BOUNDARY",
     "SUSY-GUT（如 SUSY SU(5)/SO(10)）确能给**单一**规范群 ⇒ 这一条成立；"
     "但成立的前提是**同时引入两个新结构**（超对称 + GUT 群），而不是其中一个 ⇒ 不给 PASS"),
    ("判据 2 单一或更少裸耦合", "PASS",
     "**本层核心成功**：一圈 MSSM 三耦合跨度 %s 倍（SM 为 %s 倍）⇒ 三个低能耦合可由"
     "单一 α_GUT 经跑动导出。这是本链第一次有力 PASS"
     % (ns(SP_M, 5), ns(SP_SM, 6))),
    ("判据 3 产生跨力关系", "PASS",
     "**本层第二个成功**：GUT 关系给出 sin²θ_W 预言 %s，与实测 %s 差 %s σ"
     "（非超对称 SU(5) 为 %s σ），且本层公式经 SM 口径自校验（%s vs 既有 0.20754）"
     % (ns(S2_M, 7), ns(S2W_EXP, 6), ns(SIG_M, 5), ns(SIG_SM, 5), ns(S2_SM, 7))),
    ("判据 4 减少独立输入常数", "FAIL",
     "**明确失败且方向相反**：MSSM 一般软破缺 %d 个参数 ⇒ 相对 SM 的 19（含中微子约 26）"
     "是**净增加** %d 个，而非减少。判据 4 问的是'是否减少独立输入'，超对称在这一条上是负分"
     % (N_MSSM_SOFT, N_MSSM_SOFT - 19)),
    ("判据 5 可独立证伪的新预言", "BOUNDARY",
     "超伴子谱是**真正的可证伪预言**（这一点优于前几层所有方向：它给出了'在 TeV 量级找什么'）；"
     "但 LHC Run 2 **零信号**，自然窗口收缩（T-02）⇒ 判 BOUNDARY："
     "预言存在且可检验，尚未被兑现，也尚未被证伪"),
]
for i, (nm, vd, det) in enumerate(five):
    add("V-%02d" % (i + 1), "V 五判据总评", nm, "第 75 章五条硬判据之 %d" % (i + 1), vd, det)

add("V-06", "V 五判据总评", "超对称出口总判：可行、很贵、不含引力、未被证伪也未被兑现",
    "把两条 PASS 与三条代价放在一起，超对称出口的定位是什么",
    "BOUNDARY",
    "**得到的**：判据 2（三耦合共点，跨度 %s vs SM %s）+ 判据 3（sin²θ_W %s σ vs %s σ）"
    " ⇒ **力统一（三个规范力）在超对称下是真的可行的**，这一点必须承认。"
    " **付出的**：判据 4 净增 %d 个参数、μ 问题与破缺机制无第一性（T-04）、dim-5 质子衰变仍需抑制（T-03）、"
    "LHC 零信号与自然窗口收缩（T-02）。"
    " **仍未得到的**：引力不并入（M-05，弱 %s 倍）⇒ 这是'三力统一'不是'四力统一'。"
    " ==> 定位 BOUNDARY：**超对称是三条缝里唯一被证明真能做到的，也是唯一仍在实验判决窗口内的**，"
    "但它把代价从'耦合不统一'搬到了'参数爆炸 + μ/破缺机制未知 + 超伴子未现'。"
    " 这与第 12 层 T1（维度-自由度守恒）、第 13 层 B-04（要么无效要么零预测力）**不矛盾**："
    "超对称是第三条路 —— **有效，但用参数与未观测实体付费**"
    % (ns(SP_M, 5), ns(SP_SM, 6), ns(SIG_M, 5), ns(SIG_SM, 5),
       N_MSSM_SOFT - 19, ns(WEAK_M, 5)))

add("V-07", "V 五判据总评", "第 13 层封闭谱的再更新：两条缝现在剩几条",
    "本层做完后剩余出口清单",
    "BOUNDARY",
    "第 12 层三条缝 → 第 13 层关掉 AS（缝③）→ 本层攻缝①（超对称）后："
    " **缝①超对称：判 BOUNDARY，不关闭也不通过** —— 它已被证明'能统一规范力'（两条 PASS），"
    " 但代价与未观测状态使其不能记为'已解决'，且它仍需外部输入（μ、破缺机制、谱）。"
    " **缝②涌现规范 / 离散拓扑序：仍完全开放**（本库零建模，须先证低能恢复 GR+SM）。"
    " ==> 现状：力的统一**在三个规范力层面已被证明可行（超对称）**，"
    " 而在'含引力 + 减少常数'层面**仍无解**；两条缝各自明码标价，"
    " 且**没有任何一条通向'四力统一'** —— 这是一个必须如实写下的结论")

# =================================================================
# 输出
# =================================================================
print()
for r in ROWS:
    print("[%s] %-5s | %-34s | %s" % (r["verdict"], r["id"], r["name"][:34],
                                      r["detail"][:130].replace("\n", " ")))
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
    ("α^-1(M_Z) 三值在标准区间",
     abs(A1_INV - mp.mpf('59.0')) < mp.mpf('0.5') and abs(A2_INV - mp.mpf('29.6')) < mp.mpf('0.5')
     and abs(A3_INV - mp.mpf('8.47')) < mp.mpf('0.1')),
    ("SM 三耦合不共点：跨度 > 1000 倍", SP_SM > 1000),
    ("MSSM 三耦合几乎共点：跨度 < 1.5 倍（本层承重）", SP_M < mp.mpf('1.5')),
    ("跨度改善 > 1000 倍", SP_SM / SP_M > 1000),
    ("MSSM 的 M_GUT 落在 1e16~1e17 GeV", mp.mpf('1e16') < MG_M < mp.mpf('1e17')),
    ("MSSM 的 α_GUT^-1 落在 20~30", mp.mpf('20') < AGI_M < mp.mpf('30')),
    ("本式对 SM 的 sin²θ_W 预测与既有 0.20754 相对差 < 1e-3（自校验）",
     abs(S2_SM / mp.mpf('0.20754') - 1) < mp.mpf('1e-3')),
    ("SM 弱角偏差 > 100σ（复算既有 −182σ）", SIG_SM > 100),
    ("MSSM 弱角偏差 < 5σ（本层第二个承重读数）", SIG_M < 5),
    ("MSSM 统一点高于质子衰变下限 6.18e15 GeV", MG_M > mp.mpf('6.1756379e15')),
    ("引力在 MSSM 统一点仍弱 1e3~1e5 倍", mp.mpf('1e3') < WEAK_M < mp.mpf('1e5')),
    ("MSSM 的 |b_3| < SM 的 |b_3|（超伴子减弱渐近自由）", abs(B_MSSM[2]) < abs(B_SM[2])),
    ("MSSM 参数代价 > 直接公设 SU(5)（105 > 4）", N_MSSM_SOFT > N_SU5_MIN),
    ("M_Pl 落在 1.2209e19±0.1%", abs(M_PL_GEV / mp.mpf('1.2209e19') - 1) < mp.mpf('1e-3')),
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
        "layer": "第 14 层：超对称出口 —— 可实现性与定价审计",
        "precision": "mpmath 40 位（一圈 RGE，教科书 β 系数 [A]）",
        "counts": {"total": len(ROWS), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bd, "INFO": n_info},
        "guard": {"total": len(GUARD), "passed": len(GUARD) - len(bad), "failed": bad},
        "self_note": "本层出现真实 PASS（判据 2/3），不得因本库不持有超对称而改写；"
                     "亦不得因有 PASS 而省略代价（判据 4 为 FAIL）",
    },
    "anchors": {
        "alpha_inv_MZ": [ns(A1_INV, 10), ns(A2_INV, 10), ns(A3_INV, 10)],
        "b_SM": [ns(x, 8) for x in B_SM], "b_MSSM": [ns(x, 8) for x in B_MSSM],
        "SM_M12_GeV": ns(MS_SM[(0, 1)], 8), "SM_M13_GeV": ns(MS_SM[(0, 2)], 8),
        "SM_M23_GeV": ns(MS_SM[(1, 2)], 8), "SM_spread": ns(SP_SM, 8),
        "MSSM_M12_GeV": ns(MS_M[(0, 1)], 8), "MSSM_M13_GeV": ns(MS_M[(0, 2)], 8),
        "MSSM_M23_GeV": ns(MS_M[(1, 2)], 8), "MSSM_spread": ns(SP_M, 8),
        "spread_improvement_factor": ns(SP_SM / SP_M, 8),
        "MSSM_M_GUT_GeV": ns(MG_M, 10), "MSSM_alpha_GUT_inv": ns(AGI_M, 10),
        "MSSM_alpha_GUT": ns(1 / AGI_M, 10),
        "sin2thetaW_pred_SM": ns(S2_SM, 10), "sin2thetaW_sigma_SM": ns(SIG_SM, 6),
        "sin2thetaW_pred_MSSM": ns(S2_M, 10), "sin2thetaW_sigma_MSSM": ns(SIG_M, 6),
        "sin2thetaW_exp": ns(S2W_EXP, 8),
        "selfcheck_SM_pred_vs_ledger_0.20754_rel": ns(abs(S2_SM / mp.mpf('0.20754') - 1), 4),
        "MSSM_alpha_G_at_MGUT": ns(A_G_AT_MG, 10),
        "MSSM_gravity_weaker_factor": ns(WEAK_M, 8),
        "MSSM_soft_params": N_MSSM_SOFT, "minimal_SU5_inputs": N_SU5_MIN,
        "cost_ratio": ns(mp.mpf(N_MSSM_SOFT) / N_SU5_MIN, 6),
    },
    "rows": ROWS,
}
jp = os.path.join(DATA, "v_eq_c_超对称出口定价_第14层.json")
with open(jp, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

L = []
L.append("# 第 14 层：超对称出口 —— 可实现性与定价审计")
L.append("")
L.append("> 精度：mpmath 40 位（一圈 RGE，教科书 β 系数 [A]）｜ 判据 %d 条（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）"
         % (len(ROWS), n_pass, n_fail, n_bd, n_info))
L.append("> guard 自检：%d/%d 条不可回退基线在位" % (len(GUARD) - len(bad), len(GUARD)))
L.append("")
L.append("> ⚠ **本层出现真实 PASS（判据 2 / 判据 3）**：一圈 MSSM 三耦合跨度 %s（SM 为 %s），"
         "sin²θ_W 由 %s σ 改善到 %s σ。这与前几层几乎全 FAIL 的判词不同，须原样记录。"
         % (ns(SP_M, 5), ns(SP_SM, 6), ns(SIG_SM, 5), ns(SIG_M, 5)))
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
L.append("- **本层不提出新方程、不构造超对称模型**；β 系数 (SM: 41/10, −19/6, −7；"
         "MSSM: 33/5, 1, −3)、LHC 质量下限、参数计数 105 全部为教科书/实验外部事实 [A]，本层只做代入与定价；")
L.append("- **一圈理想化**：M-02/M-03/M-04 假设全部超伴子置于 M_Z（单一阈值）。真实谱的阈值修正会带来"
         " ~10^-3 量级移动，故 sin²θ_W 的 2.32σ 应读作「一圈量级符合」而非精确预言；")
L.append("- **LHC 数字只读量级**（gluino ~2.3 TeV、squark ~1.8–2 TeV、stop ~1.2 TeV），"
         "具体值随衰变道与简化模型假设而变，本层不作精确断言；")
L.append("- **超对称未被证伪也未被兑现**：质量上限提高 ≠ 排除（split / high-scale SUSY 仍活），"
         "本层不代判「超对称是否已被排除」，那属实验进展与科学哲学层；")
L.append("- **「超对称能做到」≠「本库做到了」**：库内现役方程树超对称仅 2 行构造、LHC 可判谱 0 条（S-02），"
         "取用它的最小代价仍是写出 {Q, Q̄}=2σ^μ P_μ 的实现 + 可判谱；")
L.append("- 涌现规范 / 离散拓扑序（缝②）本层**未做**，不得因本层结论记为已关闭。")

mp_path = os.path.join(DATA, "v_eq_c_超对称出口定价_第14层.md")
with open(mp_path, "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("已写出：数据/%s + .json" % os.path.basename(mp_path))
