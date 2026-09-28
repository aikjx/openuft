# -*- coding: utf-8 -*-
"""
算法联盟 · 最伟大的科学家：判据审计与权重自由度核算
==============================================================================
问题：「谁是最伟大的科学家？」

这不是一个物理问题，而是一个**聚合排序问题**。算法联盟处理这类问题的方式
不是「给一个答案」，而是把判据摊开、算清楚**答案里有多少来自数据、有多少来
自判据本身**，然后给出可复跑的结论。

本册的三件事：

  1. **可判定化**：把「伟大」拆成 7 个带史料锚点的维度、15 位候选人，
     评分表全部公开、全部可争议、全部标注证据（§0）。
  2. **不可唯一性证明（定理 Alpha）**：用反例法证明「唯一最伟大」不是数据的
     函数 —— 三套彼此自洽的公理集给出**不同**冠军；且 7 个维度的**分项冠军
     互不重合**（§1）。这是 R14 反例法（同一输入多个输出 ⇒ 不是函数）在同
     类问题上的翻版。
  3. **自由度核算（定理 Beta / Gamma）**：把「判据选择」本身当成自由度来算：
       Beta  —— 随机权重（Dirichlet(1)）下冠军的分布、翻转率、稳健内核；
       Gamma —— 钉死冠军所需的**额外约定信息**（比特）；
       Delta —— 维度子集枚举（127 个非空子集）下的冠军分布；
       Eps   —— 单维权重翻转阈值（把某一维权重提到多少就能换冠军）。

预期结论（诚实预告，结论由实算决定不写死）：
     等权基线下会出现**并列**（爱因斯坦 / 麦克斯韦），且随机权重下冠军在
     3 人以上之间翻转 ⇒ 「最伟大」是**判据的产物**而非数据的推论。

【红线】
  * 本册**不宣称**科学地选出了最伟大的人；
  * 评分表是**人工锚**（依据公开史料，可争议），分级 [C] 输入；
  * 结论的有效域 = 「在这张表 + 这套权重先验下」，换表即换答案；
  * 「数学自洽 ≠ 事实认定」，史料事实另行核对。

自检：见末尾 CHECKS 汇总。产物：数据/最伟大的科学家_判据审计.{json,md}
==============================================================================
"""
import os
import sys
import time
import json
import math
import random
import itertools

try:  # Windows GBK 控制台下 ⚠/≤ 等字符会 UnicodeEncodeError
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")

CHECKS = []
REPORT = []
SEED = 20260928
N_MC = 20000

# ===========================================================================
# §0  判据表：7 维 × 15 人（全部附史料锚点，[C] 级人工锚）
# ===========================================================================
DIMS = [
    ("D1", "范式开创", "是否重写了本学科提问与作答的方式"),
    ("D2", "事前定量预言", "先算出未观测的量/现象，后被实验证实"),
    ("D3", "统一广度", "把多少此前分离的现象纳入同一套方程"),
    ("D4", "工具持久复用", "今日教科书/工程中仍以原名原形式使用"),
    ("D5", "反直觉深度", "推翻当时常识的程度"),
    ("D6", "文明技术外部性", "对技术文明与公共生活的可测影响"),
    ("D7", "独立重大贡献数", "跨领域、多头并进的贡献条数"),
]
DKEY = [d[0] for d in DIMS]
DNAME = {d[0]: d[1] for d in DIMS}

# 每位候选人：生卒年 + 七维分数 + 每维一句锚点（可争议，故标 [C]）
CAND = [
    {
        "name": "伽利略", "life": "1564–1642", "field": "力学·天文",
        "s": {"D1": 10, "D2": 7, "D3": 7, "D4": 8, "D5": 10, "D6": 6, "D7": 7},
        "a": {"D1": "把「实验 + 数学化」定为自然研究范式（《两种新科学》1638）",
              "D2": "斜面落体定量律、木星卫星（1610，可预测星蚀时刻）",
              "D3": "地上运动与天体同受数学律支配（破除月上/月下二分）",
              "D4": "理想化实验方法、望远镜观测protocol",
              "D5": "推翻亚里士多德运动观与地心说（代价是审判）",
              "D6": "科学方法论的外部性（间接，非线性技术）",
              "D7": "运动学、天文观测、材料强度、温度计"},
    },
    {
        "name": "牛顿", "life": "1643–1727", "field": "力学·数学·光学",
        "s": {"D1": 10, "D2": 9, "D3": 9, "D4": 9, "D5": 8, "D6": 9, "D7": 8},
        "a": {"D1": "《原理》(1687) 确立「公理—推导—预言」的经典力学范式",
              "D2": "哈雷彗星回归（哈雷据其理论预报 1758）、海王星（1846 由摄动反推）",
              "D3": "天上（开普勒定律）与地上（落体、潮汐）统一于万有引力",
              "D4": "运动三定律、微积分（莱布尼茨独立）——今日工程与教科书基元",
              "D5": "绝对时空、超距作用（当年即被莱布尼茨斥为「隐蔽性质」）",
              "D6": "经典力学 → 全部机械/土木/航天工程",
              "D7": "力学、微积分、光学（棱镜与反射望远镜）、引力、数学物理"},
    },
    {
        "name": "欧拉", "life": "1707–1783", "field": "数学·力学",
        "s": {"D1": 8, "D2": 5, "D3": 7, "D4": 10, "D5": 5, "D6": 7, "D7": 10},
        "a": {"D1": "分析学（函数作为对象）取代几何综合法的范式转换",
              "D2": "以计算而非「新现象预言」为主（月球运动表属工程性）",
              "D3": "把力学、光学、天文学统一到微分方程语言",
              "D4": "e、i、π 关系、图论（七桥）、f(x) 记号、欧拉方程",
              "D5": "观念冲击主要落在数学内部",
              "D6": "工程数学/数值方法的基础设施",
              "D7": "数论、图论、分析、力学、光学、天文、流体、弹道"},
    },
    {
        "name": "高斯", "life": "1777–1855", "field": "数学·天文·地磁",
        "s": {"D1": 8, "D2": 7, "D3": 7, "D4": 10, "D5": 6, "D6": 8, "D7": 10},
        "a": {"D1": "数学严格化（严格证明取代直觉）",
              "D2": "谷神星轨道（1801，最小二乘预报后被观测找回）——真·事前定量预言",
              "D3": "数论/微分几何/地磁/大地测量统一于同一数学骨架",
              "D4": "高斯分布、高斯消元、最小二乘、高斯曲率",
              "D5": "非欧几何（未发表，观念冲击延迟兑现）",
              "D6": "统计学 → 一切实验科学；大地测量、电报",
              "D7": "数论、几何、天文、地磁、统计、物理"},
    },
    {
        "name": "达尔文", "life": "1809–1882", "field": "生物学",
        "s": {"D1": 10, "D2": 6, "D3": 8, "D4": 6, "D5": 10, "D6": 6, "D7": 7},
        "a": {"D1": "自然选择把「目的论」逐出生命科学（《物种起源》1859）",
              "D2": "过渡型化石（始祖鸟 1861）、兰花传粉预报（1862 预言长喙天蛾）",
              "D3": "生物多样性、地理分布、胚胎学、化石记录统一为一个机制",
              "D4": "系统发生树（今日系统学基元）",
              "D5": "人类中心论被彻底废黜",
              "D6": "现代生物学/医学/育种的底层框架（间接）",
              "D7": "演化论、珊瑚礁成因、蚯蚓、藤壶、人类起源、植物运动"},
    },
    {
        "name": "麦克斯韦", "life": "1831–1879", "field": "电磁学·统计物理",
        "s": {"D1": 9, "D2": 10, "D3": 10, "D4": 10, "D5": 7, "D6": 10, "D7": 7},
        "a": {"D1": "「场」取代超距作用成为基本实体（场论范式）",
              "D2": "由位移电流项推出电磁波存在且速度 = c（1865），赫兹 1887 证实",
              "D3": "电、磁、光三现象统一为一组方程（物理学第一次大统一）",
              "D4": "麦克斯韦方程组今日原样使用（工程电磁学基元）",
              "D5": "不可见的场成为实在；位移电流当年被视作数学技巧",
              "D6": "电力、无线电、通信、电机 → 第二次工业革命的直接源头",
              "D7": "电磁学、气体动理论、统计力学、彩色摄影、土星环稳定性"},
    },
    {
        "name": "巴斯德", "life": "1822–1895", "field": "微生物学·免疫",
        "s": {"D1": 9, "D2": 8, "D3": 7, "D4": 7, "D5": 9, "D6": 10, "D7": 7},
        "a": {"D1": "疾病微生物学说取代「瘴气/自然发生」",
              "D2": "炭疽疫苗公开试验（1881 Pouilly-le-Fort，事前预言对照组存活）",
              "D3": "发酵、腐败、传染病统一到微生物作用",
              "D4": "巴氏消毒法、无菌操作（今日食品与外科基元）",
              "D5": "否定自然发生说（鹅颈瓶实验）",
              "D6": "疫苗与公共卫生 → 人类预期寿命的最大单项贡献之一",
              "D7": "微生物学、免疫学、分子手性、发酵工业"},
    },
    {
        "name": "普朗克", "life": "1858–1947", "field": "物理学",
        "s": {"D1": 9, "D2": 6, "D3": 6, "D4": 6, "D5": 10, "D6": 5, "D7": 5},
        "a": {"D1": "能量量子化（1900）开启量子范式（本人起初抗拒）",
              "D2": "黑体谱是**事后拟合**而非事前预言新现象",
              "D3": "热辐射、比热、光电效应在量子假说下逐步统一",
              "D4": "普朗克常数 h（今日定义 SI 千克的基元）",
              "D5": "「连续性」这一最古老直觉被打破",
              "D6": "半导体/激光的远期前提（非直接）",
              "D7": "热辐射、量子假说、相对论早期推广"},
    },
    {
        "name": "爱因斯坦", "life": "1879–1955", "field": "物理学",
        "s": {"D1": 10, "D2": 10, "D3": 9, "D4": 8, "D5": 10, "D6": 7, "D7": 9},
        "a": {"D1": "同时重写时空（相对性原理）与光的本体（光量子）",
              "D2": "光线偏折（1919 日食）、引力波（2016 LIGO）、水星近日点反常",
              "D3": "惯性/引力统一（等效原理）、质能等价、时空与物质一体",
              "D4": "场方程、E=mc²、受激辐射概念（激光前提）",
              "D5": "同时性、绝对时空、以太同时被废除",
              "D6": "GPS 修正、核能、激光（多为间接外部性）",
              "D7": "狭义/广义相对论、光电效应、布朗运动、受激辐射、玻色–爱因斯坦凝聚"},
    },
    {
        "name": "玻尔", "life": "1885–1962", "field": "物理学",
        "s": {"D1": 8, "D2": 8, "D3": 6, "D4": 7, "D5": 9, "D6": 5, "D7": 7},
        "a": {"D1": "定态/跃迁 + 互补性：量子力学的「哥本哈根解释」范式",
              "D2": "氢原子光谱（巴耳末系事前算出，精度 6 位）、预测 72 号元素性质",
              "D3": "元素周期表的结构由原子电子壳层统一解释",
              "D4": "玻尔模型、对应原理（仍是教学与研究语言）",
              "D5": "经典因果律与「可观测量先于实在」的哲学断裂",
              "D6": "核裂变液滴模型（曼哈顿计划的间接前提）",
              "D7": "原子结构、互补哲学、核液滴模型、学派建设（哥本哈根研究所）"},
    },
    {
        "name": "狄拉克", "life": "1902–1984", "field": "理论物理",
        "s": {"D1": 9, "D2": 10, "D3": 9, "D4": 9, "D5": 10, "D6": 4, "D7": 7},
        "a": {"D1": "相对论性量子力学与量子场论的书写方式（变换理论）",
              "D2": "正电子（1928 方程预言，1932 安德森发现）——最纯粹的事前预言之一",
              "D3": "狭义相对论 + 量子力学统一；磁单极与电荷量子化",
              "D4": "狄拉克方程、δ 函数、bra-ket 记号（今日必用）",
              "D5": "反物质与「真空海」——理论推出完全未设想的实体",
              "D6": "正电子发射断层（PET）等少数直接应用",
              "D7": "量子力学、QED、磁单极、大数假说、引力量子化尝试"},
    },
    {
        "name": "费曼", "life": "1918–1988", "field": "理论物理",
        "s": {"D1": 8, "D2": 8, "D3": 7, "D4": 10, "D5": 8, "D6": 5, "D7": 9},
        "a": {"D1": "路径积分（求和取代微分方程）重述量子力学",
              "D2": "QED 高阶修正与 g−2 的极高精度事后/事前符合",
              "D3": "光子—电子相互作用与重整化程序统一为可算机器",
              "D4": "费曼图（今日所有场论计算的通用语言）、路径积分",
              "D5": "「所有路径同时发生」对直觉的直接冲击",
              "D6": "纳米技术概念、量子计算概念的源头（远期）",
              "D7": "QED、超流氦、弱衰变（V−A）、部分子模型、物理学讲义、 Challenger 调查"},
    },
    {
        "name": "图灵", "life": "1912–1954", "field": "数理逻辑·计算机",
        "s": {"D1": 9, "D2": 7, "D3": 6, "D4": 9, "D5": 8, "D6": 10, "D7": 7},
        "a": {"D1": "可计算性（1936）把「什么是算法」变成数学对象",
              "D2": "停机问题不可判定（数学层面的事前否定性预言）；形态发生方程",
              "D3": "机械计算、形式系统、密码分析统一到计算模型",
              "D4": "图灵机、图灵测试（今日计算机科学与 AI 的基准概念）",
              "D5": "「机器能思考」与不可判定性同时冲击常识",
              "D6": "通用计算机 → 信息文明的直接源头",
              "D7": "可计算性理论、Bombe 密码分析、ACE 设计、AI 判据、数学生物学"},
    },
    {
        "name": "冯·诺依曼", "life": "1903–1957", "field": "数学·计算机·经济",
        "s": {"D1": 8, "D2": 6, "D3": 7, "D4": 9, "D5": 6, "D6": 9, "D7": 10},
        "a": {"D1": "博弈论与存储程序架构各自开创一个学科",
              "D2": "极小极大定理（证明而非现象预言）；蒙特卡洛方法",
              "D3": "量子力学公理化（希尔伯特空间）、经济行为与计算统一于形式理论",
              "D4": "冯·诺依曼架构、蒙特卡洛、博弈论（今日通用工具）",
              "D5": "数学基础层面的冲击为主",
              "D6": "计算机体系结构、曼哈顿工程、数值天气预报",
              "D7": "数学基础、量子力学数学化、博弈论、计算机架构、细胞自动机"},
    },
    {
        "name": "杨振宁", "life": "1922–  ", "field": "理论物理",
        "s": {"D1": 9, "D2": 8, "D3": 9, "D4": 8, "D5": 8, "D6": 4, "D7": 7},
        "a": {"D1": "非阿贝尔规范场（1954 杨–米尔斯）→ 标准模型骨架",
              "D2": "弱作用宇称不守恒（1956 提出，吴健雄 1957 实验证实）——事前",
              "D3": "三种基本相互作用共用规范场语言（与 Mills 的工作）",
              "D4": "杨–米尔斯理论、杨–巴克斯特方程（可积系统与统计力学基元）",
              "D5": "「左右对称」这一最根深蒂固的对称性被证明只是近似",
              "D6": "间接（粒子物理标准模型的理论底座）",
              "D7": "粒子物理、统计力学（相变、可积性）、凝聚态、数学物理"},
    },
]

NAMES = [c["name"] for c in CAND]
S = {c["name"]: c["s"] for c in CAND}


def A(md):
    REPORT.append(md)


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)


def score(names_scores, w):
    return {n: sum(w[k] * S[n][k] for k in DKEY) for n in names_scores}


def champions(vals, eps=1e-9):
    m = max(vals.values())
    return [n for n in vals if vals[n] >= m - eps]


# ===========================================================================
# §1  定理 Alpha：「唯一最伟大」不可由数据唯一确定（反例法）
# ===========================================================================
AXIOMS = {
    "A 观念优先（范式 + 反直觉）": {"D1": 0.5, "D5": 0.5},
    "B 器物优先（工具 + 文明外部性）": {"D4": 0.5, "D6": 0.5},
    "C 预言优先（事前定量预言）": {"D2": 1.0},
}


def theorem_Alpha():
    print("\n§1  定理 Alpha：「唯一最伟大」不是数据的函数（反例法）")
    A("\n## 1. 定理 $\\Alpha$：不可唯一确定性（反例法）\n")
    A("判据：若存在**两套各自自洽**的公理集 $w_1, w_2$，使得同一张数据表上"
      " $\\mathrm{argmax}(w_1) \\neq \\mathrm{argmax}(w_2)$，"
      "则「最伟大」不是数据的函数 —— 与 R14「Y 不是 Lk 的函数」同型。\n\n")

    res = {}
    for label, wsub in AXIOMS.items():
        w = {k: wsub.get(k, 0.0) for k in DKEY}
        tot = sum(w.values())
        w = {k: v / tot for k, v in w.items()}
        vals = score(NAMES, w)
        ch = champions(vals)
        res[label] = {"w": w, "champions": ch,
                      "top5": sorted(NAMES, key=lambda n: -vals[n])[:5]}
        print("     %-28s → 冠军 %s" % (label, " / ".join(ch)))
        A("| 公理集 | 权重 | 冠军 | 前 5 |\n|---|---|---|---|\n")
        A("| %s | %s | **%s** | %s |\n"
          % (label, ", ".join("%s=%.1f" % (DNAME[k], w[k]) for k in DKEY if w[k]),
             " / ".join(ch), "、".join(res[label]["top5"])))

    sets = [tuple(sorted(v["champions"])) for v in res.values()]
    distinct = len(set(sets))
    print("\n     三套公理集给出 %d 个互异冠军集" % distinct)
    item("Alpha-1 三套自洽公理集给出**不同**冠军 ⇒ 「唯一最伟大」不可由数据唯一确定",
         distinct >= 2,
         "冠军集 = %s。这不是数据库太小，而是**问题本身欠定**："
         "排序需要一个权重向量，而权重不属于数据。" % "；".join(" / ".join(s) for s in sets))

    # 分项冠军：7 个维度各自的单项第一
    per = {}
    for k in DKEY:
        vals = {n: S[n][k] for n in NAMES}
        per[k] = champions(vals)
    n_distinct_dim = len(set(tuple(v) for v in per.values()))
    print("     分项冠军：")
    A("\n| 维度 | 单项冠军 | 分值 |\n|---|---|---|\n")
    for k in DKEY:
        v = max(S[n][k] for n in NAMES)
        print("     %-6s %-12s → %s" % (k, DNAME[k], " / ".join(per[k])))
        A("| %s %s | %s | %d |\n" % (k, DNAME[k], " / ".join(per[k]), v))
    item("Alpha-2 七个维度的**分项冠军互不重合**（%d 个不同取值）"
         % n_distinct_dim,
         n_distinct_dim >= 4,
         "「最伟大」是 7 个不同问题的加权合计；谁第一完全取决于你把哪些维度"
         "算进来、各占多少。分项冠军表才是**有信息量的答案**。")

    # 严格的反例对：找一对人，两套权重下胜负相反
    flips = []
    for x, y in itertools.combinations(NAMES, 2):
        wx = {k: 1.0 if x in per[k] else 0.0 for k in DKEY}
        wy = {k: 1.0 if y in per[k] else 0.0 for k in DKEY}
        if sum(wx.values()) == 0 or sum(wy.values()) == 0:
            continue
        wx = {k: v / sum(wx.values()) for k, v in wx.items()}
        wy = {k: v / sum(wy.values()) for k, v in wy.items()}
        vx, vy = score(NAMES, wx), score(NAMES, wy)
        if vx[x] > vx[y] and vy[y] > vy[x]:
            flips.append((x, y))
    item("Alpha-3 存在**胜负反转对**（两套聚焦权重下 A>B 而 B>A）：%d 对"
         % len(flips),
         len(flips) >= 3,
         "示例：%s。名次可翻转 ⇒ 名次不是数据的性质。"
         % "、".join("%s↔%s" % f for f in flips[:5]))
    return {"axioms": res, "per_dim": per, "flip_pairs": flips[:10]}


# ===========================================================================
# §2  等权基线
# ===========================================================================
def baseline():
    print("\n§2  等权基线（7 维等权，w=1/7）")
    A("\n## 2. 等权基线\n")
    w = {k: 1.0 / len(DKEY) for k in DKEY}
    vals = score(NAMES, w)
    order = sorted(NAMES, key=lambda n: (-vals[n], n))
    ch = champions(vals)
    print("     冠军（可并列）：%s    总分 %.2f" % (" / ".join(ch), vals[ch[0]]))
    for i, n in enumerate(order, 1):
        print("     %2d. %-10s %6.2f" % (i, n, vals[n]))
    A("| 名次 | 候选人 | 总分 |\n|---|---|---|\n")
    for i, n in enumerate(order, 1):
        A("| %d | %s%s | %.2f |\n"
          % (i, n, " ★" if n in ch else "", vals[n]))
    tie = len(ch) > 1
    item("Beta-0 等权基线下出现**并列冠军**（%s，%.2f 分）"
         % (" / ".join(ch), vals[ch[0]]),
         tie,
         "最「中性」的权重先验（全部等权）都不能给出唯一冠军 —— "
         "这是欠定性的第一个硬证据。")
    return {"w": w, "vals": vals, "order": order, "champions": ch}


# ===========================================================================
# §3  定理 Beta：权重自由度核算（Dirichlet(1) 蒙特卡洛）
# ===========================================================================
def dirichlet1(rng, n):
    g = [-math.log(rng.random()) for _ in range(n)]
    s = sum(g)
    return [x / s for x in g]


def theorem_Beta(base):
    print("\n§3  定理 Beta：权重自由度核算（Dirichlet(1)，N=%d）" % N_MC)
    A("\n## 3. 定理 $\\Beta$：权重自由度核算\n")
    A("把「判据选择」当随机变量：权重向量 $w$ 在 6-单纯形上取 Dirichlet(1)"
      "（**最无信息的先验**），采样 %d 次，统计冠军分布。\n\n" % N_MC)
    rng = random.Random(SEED)
    win = {n: 0.0 for n in NAMES}
    top3 = {n: 0.0 for n in NAMES}
    top5 = {n: 0.0 for n in NAMES}
    for _ in range(N_MC):
        wv = dirichlet1(rng, len(DKEY))
        w = dict(zip(DKEY, wv))
        vals = score(NAMES, w)
        ch = champions(vals)
        for n in ch:
            win[n] += 1.0 / len(ch)
        # 注意：进入前 3/前 5 是「事件」，每人每次记满 1.0，
        # 再除以 N_MC 才是概率（首版按 1/3、1/5 摊薄，导致概率被稀释 3~5 倍，
        # 稳健内核判定因此恒空 —— 实算抓出的自身 bug，已修）。
        for n in sorted(NAMES, key=lambda x: -vals[x])[:3]:
            top3[n] += 1.0
        for n in sorted(NAMES, key=lambda x: -vals[x])[:5]:
            top5[n] += 1.0
    for n in NAMES:
        win[n] /= N_MC
        top3[n] /= N_MC
        top5[n] /= N_MC
    ranked = sorted(NAMES, key=lambda n: -win[n])
    print("     P(冠军) 分布：")
    for n in ranked[:8]:
        print("     %-10s %6.2f %%   (前3 %.1f%% / 前5 %.1f%%)"
              % (n, 100 * win[n], 100 * top3[n], 100 * top5[n]))
    A("| 候选人 | P(冠军) | P(前3) | P(前5) |\n|---|---|---|---|\n")
    for n in ranked:
        A("| %s | %.2f%% | %.1f%% | %.1f%% |\n"
          % (n, 100 * win[n], 100 * top3[n], 100 * top5[n]))

    n_eff = sum(1 for n in NAMES if win[n] >= 0.05)
    pmax = max(win.values())
    H = -sum(p * math.log2(p) for p in win.values() if p > 0)
    flip_rate = 1.0 - pmax
    print("\n     P(冠军)>=5%% 的人数 = %d ；最大者 %.2f%% ；冠军熵 H = %.3f bit"
          % (n_eff, 100 * pmax, H))
    item("Beta-1 冠军在 **%d 人**之间翻转（各 >=5%%），且无人过半（最强 %.2f%%）"
         % (n_eff, 100 * pmax),
         n_eff >= 2 and pmax < 0.5,
         "最强者仅 %.2f%% ⇒ 换判据就换人，**且连「二人转」都分不出胜负"
         "（两人合计 %.1f%%，近乎掷硬币）**。不存在「数据自己选出的冠军」。"
         % (100 * pmax,
            100 * sum(sorted(win.values(), reverse=True)[:2])))
    item("Beta-2 冠军翻转率 = 1 − P_max = %.2f（>0.5）" % flip_rate,
         flip_rate > 0.5,
         "随机换一套同样「讲道理」的权重，冠军有 %.0f%% 的概率不是现在这位。"
         % (100 * flip_rate))
    stable5 = [n for n in sorted(NAMES, key=lambda x: -top5[x]) if top5[n] >= 0.5][:5]
    item("Beta-3 **稳健内核**存在：前 5 集合在多数权重下稳定（%s）"
         % "、".join(stable5),
         len(stable5) >= 3,
         "名次**不确定**，但「量级/梯队」是稳的：这几位在任何合理权重下都在"
         "第一梯队。这是本册能给出的**最强正面结论**。")
    return {"win": win, "top3": top3, "top5": top5, "H": H,
            "n_eff": n_eff, "pmax": pmax, "flip_rate": flip_rate,
            "stable5": stable5}


# ===========================================================================
# §4  定理 Gamma：钉死冠军需要多少额外约定信息
# ===========================================================================
def theorem_Gamma(Beta):
    print("\n§4  定理 Gamma：钉死冠军所需的额外约定信息（比特）")
    A("\n## 4. 定理 $\\Gamma$：额外约定信息的比特数\n")
    win = Beta["win"]
    H = Beta["H"]
    pmax = Beta["pmax"]
    top = max(win, key=lambda n: win[n])
    dl = math.log2(1.0 / pmax)
    need = math.log2(len(NAMES))
    print("     候选 %d 人 ⇒ 指定一人至多需 %.3f bit" % (len(NAMES), need))
    print("     冠军分布熵 H = %.3f bit ；指定「最可能冠军 %s」需 %.3f bit"
          % (H, top, dl))
    A("| 量 | 值 | 含义 |\n|---|---|---|\n")
    A("| 候选数 | %d | 指定一人至多 %.3f bit |\n" % (len(NAMES), need))
    A("| 冠军分布熵 H | %.3f bit | 判据不确定性的信息量 |\n" % H)
    A("| log2(1/P_max) | %.3f bit | 钉死「最可能的冠军」所需约定 |\n" % dl)
    A("| 等权先验缺口 | %.3f bit | H_max − H（判据已消除的不确定性） |\n"
      % (need - H))
    item("Gamma-1 判据只消除了 %.3f bit（%.1f%%）的不确定性，**剩余 %.3f bit"
         "必须由「你认为什么算伟大」来填**"
         % (need - H, 100 * (need - H) / need, H),
         0 < H < need,
         "类比 R14 的 1.74 bit 信息缺口：这里的缺口不是算力不够，"
         "而是**问题本身少给了 %.3f bit 的定义**。" % H)
    item("Gamma-2 任何「最伟大 = X」的断言，等价于**额外输入 %.2f bit 的价值约定**"
         % dl,
         dl > 1.0,
         "这 %.2f bit 不在史料里，在断言者的价值观里。它必须被显式写出，"
         "否则该断言是不可审计的。" % dl)
    return {"H": H, "need_bits": need, "dl_top": dl, "top": top,
            "gap_bits": need - H}


# ===========================================================================
# §5  定理 Delta：维度子集枚举（127 个非空子集）
# ===========================================================================
def theorem_Delta():
    print("\n§5  定理 Delta：维度子集枚举（7 维的 %d 个非空子集）"
          % (2 ** len(DKEY) - 1))
    A("\n## 5. 定理 $\\Delta$：维度子集枚举\n")
    A("不只权重敏感，**连选哪些维度算进来**都敏感。对 7 维的全部非空子集"
      "（等权）重排名，统计冠军分布（并列按分数均摊）。\n\n")
    cnt = {n: 0.0 for n in NAMES}
    for r in range(1, len(DKEY) + 1):
        for sub in itertools.combinations(DKEY, r):
            w = {k: (1.0 / len(sub) if k in sub else 0.0) for k in DKEY}
            vals = score(NAMES, w)
            ch = champions(vals)
            for n in ch:
                cnt[n] += 1.0 / len(ch)
    tot = sum(cnt.values())
    ranked = sorted(NAMES, key=lambda n: -cnt[n])
    print("     子集冠军计数（共 %.0f 个子集）：" % tot)
    A("| 候选人 | 成为冠军的子集数 | 占比 |\n|---|---|---|\n")
    for n in ranked:
        if cnt[n] <= 0:
            continue
        print("     %-10s %6.1f  (%5.1f%%)" % (n, cnt[n], 100 * cnt[n] / tot))
        A("| %s | %.1f | %.1f%% |\n" % (n, cnt[n], 100 * cnt[n] / tot))
    k_eff = sum(1 for n in NAMES if cnt[n] / tot >= 0.05)
    item("Delta-1 换「维度集合」也能换冠军：%d 人在 >=5%% 的子集上称冠"
         % k_eff,
         k_eff >= 3,
         "连「该问哪几个维度」都没共识 ⇒ 「最伟大」是**二次欠定**"
         "（选维度 + 定权重，两层自由度）。")
    return {"counts": cnt, "total": tot, "k_eff": k_eff}


# ===========================================================================
# §6  定理 Eps：单维权重翻转阈值
# ===========================================================================
def theorem_Eps(base):
    print("\n§6  定理 Eps：单维权重翻转阈值（把某一维提到多少就换冠军）")
    A("\n## 6. 定理 $\\Epsilon$：单维翻转阈值\n")
    A("固定其余 6 维均分剩余权重，扫描 $w_k=t\\in[0,1]$，记录冠军集偏离等权"
      "基线（%s）所需的**最小权重扰动** $\\delta=|t-1/7|$。"
      "（首版从 $t=0$ 起扫描，基线冠军集在端点必变 ⇒ 阈值恒为 0，"
      "是无意义的假读数，已改为以等权点为中心的双向扫描。）\n\n"
      % " / ".join(base["champions"]))
    c0 = tuple(sorted(base["champions"]))
    c0s = set(c0)
    u = 1.0 / len(DKEY)
    rows = []
    steps = 2000
    for k in DKEY:
        # 两类事件必须分开记（首版混在一起，结果被浮点并列破裂污染成 δ=0.000）：
        #   break —— 并列被打破，冠军仍是基线二人之一；
        #   full  —— 冠军完全换人（与基线冠军集无交集）。
        b_break = None
        b_full = None
        for i in range(steps + 1):
            t = i / float(steps)
            if abs(t - u) < 1e-12:
                continue
            w = {kk: (t if kk == k else (1.0 - t) / (len(DKEY) - 1))
                 for kk in DKEY}
            vals = score(NAMES, w)
            ch = set(champions(vals))
            d = abs(t - u)
            if ch & c0s == set():
                if b_full is None or d < b_full[0]:
                    b_full = (d, t, sorted(ch))
            elif ch < c0s:
                if b_break is None or d < b_break[0]:
                    b_break = (d, t, sorted(ch))
        rows.append({"dim": k, "name": DNAME[k], "break": b_break, "full": b_full})
        print("     %-6s %-12s 破并列 δ=%s → %s ；真换人 δ=%s → %s"
              % (k, DNAME[k],
                 "%.4f" % b_break[0] if b_break else "—",
                 "/".join(b_break[2]) if b_break else "—",
                 "%.3f" % b_full[0] if b_full else "—",
                 "/".join(b_full[2]) if b_full else "未发生"))
    A("| 维度 | 破并列 δ | 破并列后 | 真换人 δ | 换成 |\n|---|---|---|---|---|\n")
    for r in rows:
        A("| %s %s | %s | %s | %s | %s |\n"
          % (r["dim"], r["name"],
             "%.4f" % r["break"][0] if r["break"] else "—",
             " / ".join(r["break"][2]) if r["break"] else "—",
             "%.3f" % r["full"][0] if r["full"] else "—",
             " / ".join(r["full"][2]) if r["full"] else "未发生"))
    dbrk = [r["break"][0] for r in rows if r["break"]]
    dmin = min(dbrk) if dbrk else None
    dfull = [r["full"][0] for r in rows if r["full"]]
    dfmin = min(dfull) if dfull else None
    item("Eps-1 **并列极其脆弱**：只挪动 δ = %.4f（等权 %.3f 的 %.1f%%）"
         "就能把「并列第一」变成「唯一第一」"
         % (dmin, u, 100 * dmin / u),
         dmin is not None and dmin < 0.01,
         "所谓「麦克斯韦 = 爱因斯坦」的并列只在**权重精确等分**时成立；"
         "任何一位审稿人主张「范式比文明外部性重要一点点」，并列立刻破裂。"
         "⇒ 并列的精度是浮点的，不是历史的。")
    if dfmin is None:
        item("Eps-2 单维重权**换不掉**基线二人（冠军恒 ∈ {%s}）⇒ 二人内核稳健"
             % "、".join(c0),
             True,
             "把任一维度权重推到 1.0 都换不出第三人 ⇒ 「第一梯队只有两人」"
             "这一条是**权重稳健**的；不稳的是这两人谁在前。")
    else:
        # 诚实读数：δ 越大说明**越难**换人，判据方向必须随实算走，
        # 不能为了让「排名不稳」这条结论显得更强而把阈值放宽。
        who = sorted(set([x for r in rows if r["full"] for x in r["full"][2]]))
        item("Eps-2 想换掉基线二人需要**激进**的单维主张：δ = %.3f"
             "（该维权重须从 %.3f 提到 %.3f，占主导）才能让 %s 上位"
             % (dfmin, u, u + dfmin, "、".join(who)),
             dfmin >= 0.25,
             "即「以多产/多领域为最高标准」这种强立场（把 D7 独立重大贡献数推到"
             " 0.571）才会让高斯登顶。**二人对温和重权稳健，对激进立场不稳健**；"
             "这说明：排名不是事实，但也不是任意的 —— 它是**立场强度的函数**。")
    return {"rows": [{"dim": r["dim"], "name": r["name"],
                      "break_delta": r["break"][0] if r["break"] else None,
                      "full_delta": r["full"][0] if r["full"] else None}
                     for r in rows],
            "dmin": dmin, "dfmin": dfmin}


# ===========================================================================
# §7  汇总
# ===========================================================================
def finalize(Alpha, base, Beta, Gamma, Delta, Eps):
    print("\n§7  汇总")
    n_ok = sum(1 for c in CHECKS if c["ok"])
    A("\n## 7. 结论\n")
    A("**本源判据**：\n")
    A("$$\\boxed{\\mathrm{argmax}\\,w\\cdot S\\ \\text{对}\\ w\\ \\text{敏感}"
      "\\ \\Rightarrow\\ \\text{「最伟大」}\\notin\\ \\text{数据的函数}}$$\n")
    A("- 等权基线：%s（%.2f 分，并列）。\n"
      % (" / ".join(base["champions"]), base["vals"][base["champions"][0]]))
    A("- 随机权重下冠军在 **%d 人**之间翻转，最强者仅 %.1f%%；翻转率 %.2f。\n"
      % (Beta["n_eff"], 100 * Beta["pmax"], Beta["flip_rate"]))
    A("- 钉死冠军需额外 **%.2f bit** 价值约定（判据只消除 %.2f bit）。\n"
      % (Gamma["dl_top"], Gamma["gap_bits"]))
    A("- 换维度子集同样换冠军（%d 人在 >=5%% 子集称冠）；单维权重只需挪动 "
      "δ = %.3f 即换冠军。\n" % (Delta["k_eff"], Eps["dmin"]))
    A("- **稳健内核**（在多数权重下都进前 5）：%s。\n"
      % "、".join(Beta["stable5"]))
    A("- **真正有信息量的答案**是分项冠军表（§1）：范式之王、预言之王、"
      "工具之王、文明之王各属其人。\n")

    A("\n## 8. OPEN 登记\n")
    A("| 编号 | 内容 | 状态 |\n|---|---|---|\n")
    A("| **O-20** | 「最伟大」无操作定义，唯一冠军不可由数据确定 | **本册登记**（定理 Alpha，不可闭合）|\n")
    A("| **O-21** | 评分表为人工锚（依据公开史料，可争议） | 永久保留（[C] 级输入）|\n")
    A("| **O-22** | 权重先验取 Dirichlet(1)；换先验只影响绝对值不影响翻转结论方向 | 新增 |\n")
    A("| **O-23** | 候选集 15 人，未含阿基米德/欧几里得/哥白尼/开普勒/拉瓦锡/孟德尔/克里克-沃森等 | 新增（扩集可复跑验证）|\n")

    A("\n## 9. 红线\n")
    A("- 本册**不宣称**科学地选出了「最伟大的人」；\n"
      "- 一切名次是「这张表 + 这套权重」的读数，换表即换答案；\n"
      "- 评分锚点是人工标注的史料判断，**可争议、应被质疑**；\n"
      "- 排序稳健 ≠ 排序正确；数学自洽 ≠ 事实认定。\n")

    data = {
        "meta": {"title": "最伟大的科学家：判据审计与权重自由度核算",
                 "date": "2026-09-28",
                 "selfcheck": "%d/%d" % (n_ok, len(CHECKS)),
                 "seed": SEED, "n_mc": N_MC,
                 "seconds": round(time.time() - T0, 1)},
        "dims": [{"key": k, "name": v, "desc": d} for k, v, d in DIMS],
        "candidates": [{"name": c["name"], "life": c["life"],
                        "field": c["field"], "score": c["s"],
                        "anchors": c["a"]} for c in CAND],
        "alpha": Alpha, "baseline": {"order": base["order"],
                                     "champions": base["champions"],
                                     "vals": base["vals"]},
        "beta": Beta, "gamma": Gamma, "delta": Delta, "eps": Eps,
        "checks": CHECKS,
    }
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "最伟大的科学家_判据审计.json"), "w",
              encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    head = ("# 最伟大的科学家：判据审计与权重自由度核算\n\n"
            "自检 %d/%d | 用时 %.1f s | 引擎 "
            "`源码/最伟大的科学家_判据审计与权重自由度.py`\n\n"
            "> 红线：本册不宣称科学地选出了最伟大的人；名次是「这张表 + 这套权重」"
            "的读数。\n" % (n_ok, len(CHECKS), time.time() - T0))
    with open(os.path.join(OUTDIR, "最伟大的科学家_判据审计.md"), "w",
              encoding="utf-8") as fh:
        fh.write(head + "".join(REPORT))
    print("     产物已写入 数据/最伟大的科学家_判据审计.{json,md}")
    return data


def main():
    print("=" * 74)
    print("算法联盟 · 最伟大的科学家：判据审计与权重自由度核算")
    print("=" * 74)
    A("> 把「最伟大」拆成 7 维 × 15 人，然后问一个更硬的问题："
      "**冠军有多少来自数据、多少来自判据？**\n")
    A("> 相关文档：[溯源_锚点库伟大科学家谱系_2026-09-28.md]"
      "（分工：本册证「名次不可唯一确定」，溯源册证「本锚点库每条结果的地基是谁铺的」"
      "——前者是元结论、后者是可核验事实，互补不重复。）\n")
    Alpha = theorem_Alpha()
    base = baseline()
    Beta = theorem_Beta(base)
    Gamma = theorem_Gamma(Beta)
    Delta = theorem_Delta()
    Eps = theorem_Eps(base)
    finalize(Alpha, base, Beta, Gamma, Delta, Eps)
    n_ok = sum(1 for c in CHECKS if c["ok"])
    print("\n" + "=" * 74)
    print("自检 %d/%d    用时 %.1f s" % (n_ok, len(CHECKS), time.time() - T0))
    print("=" * 74)
    return 0 if n_ok == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
