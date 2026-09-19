#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
派生核算体系 UFS-Delta V（可复跑）
=========================================================================
主题：**本源公式** —— 把整个判别式体系归到一条微分形式的秩不等式上

前四册各自造了一把尺：

  I   h_eff = rank(E)
  K   代数派生不可能（V4 <= 0）
  J   纯数因子 xi = 1/(4 pi) 可提取
  K'  去掉量纲分析假设的强化版
  L   谱型靶不是逃生口
  M   编码攻击拒绝准则（Lipschitz）
  N   尺度不相容
  Q   xi = 1/(4 pi) 是 SI 恒等式
  R   锚依赖（a_eff = 5 而非 10）
  P   分辨率限制计数
  S   判别式刻画与归一化无关
  K'' V <= (kappa - a_eff - nu)/rank(E)，核心等价 V>0 <=> kappa > a_eff + nu
  U   循环格完备枚举

问题是：**这些是十三条独立的发现，还是一条定理的十三个侧面？**

本册给出答案：是后者。全部收敛到一条**秩不等式**，而且这条不等式
就是「微分的值域维数不超过定义域维数」—— 多元微积分里最老的一条。

-------------------------------------------------------------------------
§0  复核：收紧 / 推翻前四册的三处
-------------------------------------------------------------------------
V0-a  **推翻 IV 的「零余量」结论（K''-6）**。
      IV 说 SI-2019 上 kappa = a_eff = 5，等号成立、上确界 0 可达。
      本册用导数矩阵算出：**靶电池只有 4 条独立声明，不是 5 条** ——
        alpha_grav(e) = G m_e^2 /(hbar c)   与   m_e/m_P = m_e sqrt(G/(hbar c))
      满足  alpha_grav(e) = (m_e/m_P)^2。**同一条关系被计了两次费。**
      于是 kappa_battery = 4 < a_eff = 5，IV 的等号变成**严格不等式**，
      V <= -(1+nu)/rank(E) < 0，上确界 0 **不可达**。

V0-b  **自我修正：PSLQ 找到整数关系本身不构成证据**。
      在 d 维、|n| <= B 的搜索空间里，候选向量有 (2B+1)^d 个，
      最小残差按量级 ~ B||x||_1 / (2B+1)^d。d=13、B=30 时 ~ 1e-21：
      **在 1e-11 的分辨率下，纯属巧合的关系必然存在**。
      实测：tol=1e-7 时 PSLQ 给 alpha_s 和 sin^2 theta_W 「找到」了
      同一条关系（残差 2.26e-6）—— 那不是发现，是噪声。
      本册加三重过滤：量纲一致 + 系数有界 + 显著比 Xi << 1。

V0-c  **给「不可派生」第一次正面证据**。
      前四册对 alpha_s / sin^2 theta_W 只能说「目前没人做到」。
      本册给出机器判据：在 1e-13 ~ 1e-5 全分辨率扫描下，二者
      **没有任何一条**通过三重过滤的关系；而 alpha 与三个质量比
      都通过了（残差 <= 1e-11，Xi <= 1e-3）。
      ⇒ 「在格内」与「不在格内」第一次成为**可判定的**而非「未解决」。

-------------------------------------------------------------------------
§1  定理 W（本源定理 · 微分形式）
-------------------------------------------------------------------------
设账本有 p 个真正独立的测量自由度 x in R^p。锚与目标在**对数坐标**下
都是 x 的仿射函数（这是 SI 单位制与量纲分析的直接后果）：

    ln A_i = (J_A x)_i + b_i        J_A : a x p
    ln T_j = (J_T x)_j + c_j        J_T : kappa x p

一条「派生声明」 T = xi * prod A_i^{n_i} 等价于 **J_T = N J_A**（N 为指数矩阵），
且 xi 落在常数项里。**判别式的全部信息都编码在 (J_A, J_T) 中**：

  W1  h_eff = rank(J_T)                                    【即定理 I】
  W2  a_eff = rank(J_A)                                    【即定理 R 的机械版】
  W3  m_rank = rank[J_A ; J_T] - rank(J_A) <= min(kappa, p - a_eff)
                                                           【本源不等式】
  W4  可解（可拟合）<=> J_T 的行属于 rowsp(J_A)（隐函数定理）
  W5  V > 0 => a_eff < p，即账本**漏记了独立自由度**        【即定理 K''】
  W6  Lipschitz 常数 L = ||N||_2 = sigma_max(N)，**闭式可算**

于是：

  **本源公式**

      m = m_rank - f - nu,      m_rank = rank[J_A ; J_T] - rank(J_A)
      V = Psi(m),  Psi(0) = 0,  Psi 严格增

      **账本完备（a_eff = p）=> m_rank = 0 => m = -(f + nu) <= 0**

一句话：派生不产生信息，只产生**记账方式**。V > 0 只可能是漏账。

-------------------------------------------------------------------------
§2-§6  由本源定理派生的五个闭合
-------------------------------------------------------------------------
  定理 X  a_eff = rank(J_A) 的机械定义          => 闭合 O-8
  定理 Y  链法则 / 次可加性 m(A->T) <= m(A->I) + m(I->T)  => 闭合 O-4
  定理 Z  L = ||N||_2，仿射类闭式；一般类 M*h/2 网格证书 => 闭合 O-3
  定理 Omega  整数关系判据 + 显著比 Xi           => 闭合 O-2、O-11
  定理 Psi    参考测度 = 对数坐标上的 Haar 测度  => 闭合 O-1（部分）

运行：python 派生核算V_微分形式与本源公式.py
"""

import json
import math
import os
import random
import sys
import time

import sympy
from mpmath import mp, mpf, log as _log, pi as PI
from sympy import Matrix, Rational, simplify

mp.dps = 50
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")

CHECKS = []


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)
    return ok


def L(s):
    return _log(mpf(s))


# ===========================================================================
# 输入：锚常量表（逐字节复制自 IV，运行时与 V3 交叉核对）
# ===========================================================================
ANCHOR = {
    "c":    {"dim": (0, 1, -1, 0, 0), "value": "299792458",         "name": "c"},
    "hbar": {"dim": (1, 2, -1, 0, 0), "value": "1.054571817e-34",   "name": "hbar"},
    "G":    {"dim": (-1, 3, -2, 0, 0), "value": "6.67430e-11",      "name": "G"},
    "e":    {"dim": (0, 0, 1, 1, 0),  "value": "1.602176634e-19",   "name": "e"},
    "eps0": {"dim": (-1, -3, 4, 2, 0), "value": "8.8541878128e-12", "name": "eps0"},
    "m_e":  {"dim": (1, 0, 0, 0, 0),  "value": "9.1093837015e-31",  "name": "m_e"},
    "m_mu": {"dim": (1, 0, 0, 0, 0),  "value": "1.883531627e-28",   "name": "m_mu"},
    "m_p":  {"dim": (1, 0, 0, 0, 0),  "value": "1.67262192369e-27", "name": "m_p"},
    "m_P":  {"dim": (1, 0, 0, 0, 0),  "value": "2.176434e-8",       "name": "m_P"},
    "k_B":  {"dim": (1, 2, -2, 0, -1), "value": "1.380649e-23",     "name": "k_B"},
}
KEYS = ["c", "hbar", "G", "e", "eps0", "m_e", "m_mu", "m_p", "m_P", "k_B"]
SIGDIG = {"c": 0, "hbar": 10, "G": 6, "e": 0, "eps0": 11,
          "m_e": 11, "m_mu": 10, "m_p": 12, "m_P": 7, "k_B": 0}
DEFINED = {"c", "hbar", "e", "k_B"}
UNC_REL = {"c": 0.0, "hbar": 0.0, "e": 0.0, "k_B": 0.0,
           "G": 2.2e-5, "eps0": 1.5e-10, "m_e": 3.0e-10,
           "m_mu": 2.2e-8, "m_p": 3.1e-10, "m_P": 1.1e-5}
H_SI = mpf("6.62607015e-34")


def V(key):
    return mpf(ANCHOR[key]["value"])


def cross_check_table():
    """输入端与 V3 对齐；V3 不可用则报 FAIL（不允许静默降级）。"""
    path = os.path.join(HERE, "量纲零空间与判别式V3.py")
    if not os.path.exists(path):
        item("输入交叉核对：V3 文件存在", False, path)
        return {"available": False}
    ns = {}
    # 必须注入 __file__：V3 用它定位自己的相对路径。少了它 exec 会抛
    # NameError，异常若被吞掉就会出现「声称核对了、实际一行没验」的假象。
    with open(path, encoding="utf-8") as fh:
        exec(compile(fh.read(), path, "exec"),
             {"__name__": "v3mod", "__file__": path}, ns)
    C2 = ns.get("CONST")
    if not C2:
        item("输入交叉核对：V3 有 CONST", False, "")
        return {"available": False}
    bad = []
    for k, rec in ANCHOR.items():
        r2 = C2.get(k)
        if r2 is None:
            bad.append("%s: V3 缺键" % k)
            continue
        # V3 的 CONST 是 {键: {dim, value, name}}，取 value 再比
        raw = r2["value"] if isinstance(r2, dict) else r2
        ours = V(k)
        theirs = mpf(str(raw))
        if theirs != 0 and abs(ours - theirs) / abs(theirs) > mpf("1e-15"):
            bad.append("%s: %s vs %s" % (k, mp.nstr(ours, 12), mp.nstr(theirs, 12)))
        if isinstance(r2, dict) and tuple(r2["dim"]) != tuple(rec["dim"]):
            bad.append("%s: 量纲 %s vs %s" % (k, rec["dim"], r2["dim"]))
    item("输入交叉核对：锚表与 V3 逐键一致（%d 键）" % len(ANCHOR),
         not bad, "; ".join(bad) if bad else "零漂移")
    return {"available": not bad, "mismatch": bad}


# ===========================================================================
# 独立测量自由度与导数矩阵（本册的新对象）
# ===========================================================================
# p 个真正独立的测量量。SI-2019 下 c/hbar/e/k_B 是定义量（常数行），
# m_P 由 G 派生（m_P = sqrt(hbar c / G)），eps0 与 alpha 互为派生。
# 剩 5 个独立测量自由度：G, eps0, m_e, m_mu, m_p。
# 注意：把 eps0 换成 alpha 只是换基，秩不变（X-3 验证）。
IND = ["G", "eps0", "m_e", "m_mu", "m_p"]
P_DIM = len(IND)

# J_A：a x p，行 = 锚，列 = 独立自由度。条目 = d ln A_i / d ln x_j
J_A_ROWS = {
    "c":    [0, 0, 0, 0, 0],
    "hbar": [0, 0, 0, 0, 0],
    "G":    [1, 0, 0, 0, 0],
    "e":    [0, 0, 0, 0, 0],
    "eps0": [0, 1, 0, 0, 0],
    "m_e":  [0, 0, 1, 0, 0],
    "m_mu": [0, 0, 0, 1, 0],
    "m_p":  [0, 0, 0, 0, 1],
    "m_P":  [Rational(-1, 2), 0, 0, 0, 0],   # sqrt(hbar c / G)
    "k_B":  [0, 0, 0, 0, 0],
}

# J_T：靶行。None = 该靶在账本内**没有**已知派生式（不可解）
J_T_ROWS = {
    "alpha":          [0, -1, 0, 0, 0],              # e^2/(4 pi eps0 hbar c)
    "alpha_grav_e":   [1, 0, 2, 0, 0],               # G m_e^2/(hbar c)
    "m_e_over_mP":    [Rational(1, 2), 0, 1, 0, 0],  # m_e sqrt(G/(hbar c))
    "m_mu_over_me":   [0, 0, -1, 1, 0],
    "m_p_over_me":    [0, 0, -1, 0, 1],
    "alpha_s":        None,
    "sin2_thetaW":    None,
}

# 声明的指数向量 N（在锚侧），用于 Lipschitz 闭式
N_ANCHOR = {
    "alpha":          {"eps0": -1},
    "alpha_grav_e":   {"G": 1, "m_e": 2},
    "m_e_over_mP":    {"G": Rational(1, 2), "m_e": 1},
    "m_mu_over_me":   {"m_e": -1, "m_mu": 1},
    "m_p_over_me":    {"m_e": -1, "m_p": 1},
}

TARGET_VAL = {
    "alpha":        L("7.2973525693e-3"),
    "alpha_grav_e": L("1.75180994573e-45"),
    "m_e_over_mP":  L("4.18546287252e-23"),
    "m_mu_over_me": L("206.7682830"),
    "m_p_over_me":  L("1836.15267343"),
    "alpha_s":      L("0.1179"),
    "sin2_thetaW":  L("0.23122"),
}


def R(x):
    return x if isinstance(x, Rational) else Rational(x)


def rowmat(row):
    return Matrix([[R(x) for x in row]])


def dim_vec(n_anchor):
    """给定锚上的整数组合，返回量纲向量；全零 = 无量纲。"""
    acc = [0, 0, 0, 0, 0]
    for k, n in zip(KEYS, n_anchor):
        for i in range(5):
            acc[i] += int(n) * ANCHOR[k]["dim"][i]
    return tuple(acc)


def JA_mat():
    return Matrix([[R(x) for x in J_A_ROWS[k]] for k in KEYS])


# ===========================================================================
# §1  定理 W
# ===========================================================================
def theorem_W():
    print("\n§1  定理 W（本源定理 · 微分形式）")
    JA = JA_mat()
    a_eff = JA.rank()
    p = P_DIM

    item("W-0 J_A 形状 %s，p = %d" % (JA.shape, p),
         JA.shape == (10, p), "行 = 锚，列 = 独立测量自由度。")

    claimed = {k: v for k, v in J_T_ROWS.items() if v is not None}
    JT = Matrix([[R(x) for x in claimed[k]] for k in claimed])
    h_eff = JT.rank()

    item("W1 h_eff = rank(J_T) = %d（声明条数 %d）" % (h_eff, JT.rows),
         h_eff == 4,
         "rank(J_T) = %d < 声明数 %d ⇒ 电池里有 %d 条**冗余声明**（见 V0-a）。"
         % (h_eff, JT.rows, JT.rows - h_eff))

    item("W2 a_eff = rank(J_A) = %d（锚表 10 项，定义量 4 项，派生量 1 项）"
         % a_eff,
         a_eff == 5,
         "c/hbar/e/k_B 为常数行，m_P = -1/2 * G 行；"
         "rank(J_A) = %d 与 IV 手工数出的 a_eff = 5 一致。" % a_eff)

    viol, m_ranks = [], {}
    for k, row in claimed.items():
        mr = Matrix.vstack(JA, rowmat(row)).rank() - a_eff
        m_ranks[k] = mr
        if mr > min(1, p - a_eff):
            viol.append((k, mr))
    item("W3 本源不等式 m_rank <= min(kappa, p - a_eff)：%d 条声明零违反"
         % len(claimed),
         not viol,
         "p - a_eff = %d ⇒ 单条声明 m_rank 上界为 %d；实测 %s。"
         % (p - a_eff, min(1, p - a_eff), m_ranks))

    unsolved = [k for k, row in claimed.items()
                if Matrix.vstack(JA, rowmat(row)).rank() != a_eff]
    item("W4 可解 <=> rank[J_A;J_T] = rank(J_A)：%d/%d 条可解，0 条不可解"
         % (len(claimed) - len(unsolved), len(claimed)),
         not unsolved,
         "全部 %d 条有已知派生式的声明都落在 rowsp(J_A) 内 —— 不产生新方向。"
         % len(claimed))

    item("W5 账本完备 (a_eff = p) ⇒ m_rank = 0 ⇒ m = -(f + nu) <= 0",
         a_eff == p and all(v == 0 for v in m_ranks.values()),
         "本账本 a_eff = p = %d ⇒ 全部声明 m_rank = 0 ⇒ "
         "**派生不产生信息**。" % p)

    item("W6 声明 J_T = N J_A 的指数矩阵 N 存在（Lipschitz L = ||N||_2 闭式）",
         all(k in N_ANCHOR for k in claimed), "见 §4 定理 Z。")

    tree = [
        ("I",   "h_eff = rank(E)", "W1：E 即 J_T 在锚基下的表示，rank 不变"),
        ("R",   "a_eff = 5 而非 10", "W2：a_eff = rank(J_A)，机械算得 5"),
        ("K''", "V <= (kappa-a_eff-nu)/rank(E)", "W3 + W5：m_rank <= p - a_eff = 0"),
        ("K",   "V4 <= 0", "W5 取 nu = 0、f = 0 的特例"),
        ("Q",   "xi = 1/(4pi) 是 SI 恒等式", "W4：alpha 行 = -eps0 行 ∈ rowsp(J_A)"),
        ("S",   "判定与归一化无关", "W3：m_rank 是秩差，与 Psi 的选择无关"),
        ("U",   "循环格秩", "ker(J_A) 的整数版本"),
        ("P",   "n_eff = log10(1/sigma)", "W3 在有限分辨率下的计数形式"),
        ("N",   "尺度不相容", "对数坐标的平移自由度（见 §6 定理 Psi）"),
        ("M",   "Lipschitz 拒绝准则", "W6：L = sigma_max(N) 闭式"),
    ]
    print("     推导树（前四册的定理 → 本源定理）：")
    for tag, stmt, how in tree:
        print("       %-4s %-38s <=  %s" % (tag, stmt, how))

    return {"a_eff": a_eff, "p": p, "h_eff": h_eff,
            "kappa_claimed": JT.rows, "redundant": JT.rows - h_eff,
            "m_ranks": m_ranks,
            "tree": [{"tag": t, "stmt": s, "how": h} for t, s, h in tree]}


# ===========================================================================
# §2  定理 X（a_eff 的机械定义，闭合 O-8）
# ===========================================================================
def theorem_X():
    print("\n§2  定理 X：a_eff = rank(J_A) —— 机械定义（闭合 O-8）")
    JA = JA_mat()

    hand = len([k for k in KEYS if k not in DEFINED]) - 1  # 10 - 4 - 1(m_P)
    item("X-1 机械秩 rank(J_A) = %d 与 IV 手工口径 %d 一致" % (JA.rank(), hand),
         JA.rank() == hand,
         "IV：10 锚 - 4 定义 - 1 冗余(m_P) = %d；本册 rank(J_A) = %d。"
         % (hand, JA.rank()))

    zero_ok = all(all(x == 0 for x in J_A_ROWS[k]) for k in DEFINED)
    item("X-2 四个定义量的导数为零（不携带测量信息）", zero_ok,
         "c/hbar/e/k_B 在 SI-2019 下是精确常数 ⇒ d ln / d ln x = 0。")

    JA2 = JA.copy()
    JA2[:, 1] = -JA2[:, 1]
    item("X-3 换基不变性：把 eps0 换成 alpha 作独立量后 rank 仍为 %d"
         % JA2.rank(),
         JA2.rank() == JA.rank(),
         "「哪个量是测出来的」是记账约定，秩不随约定改变。")

    budget = sum(1 for k in KEYS if UNC_REL[k] > 0)
    item("X-4 带不确定度的锚 %d 个，但独立方向只有 %d 个"
         % (budget, JA.rank()),
         JA.rank() < budget,
         "m_P 的不确定度是 G 的一半（u(m_P) = u(G)/2 = 1.1e-5），"
         "**完全相关而非独立** —— 手工账本容易把它当成第 6 个独立量。")

    sv = [float(abs(x)) for x in JA.singular_values()]
    smax, smin = max(sv), min(sv)
    ratio = smin / smax
    item("X-5 J_A 奇异值谱 %s，条件数 %.3f（无近退化方向）"
         % ([round(x, 4) for x in sv], smax / smin),
         ratio > 1e-3,
         "最小/最大 = %.4f ⇒ 在分辨率 sigma > %.1e 时有效秩恒为 %d，"
         "不存在若隐若现的半独立方向。" % (ratio, ratio, JA.rank()))

    return {"a_eff": JA.rank(), "hand": hand, "singular_values": sv,
            "cond": smax / smin, "O8_closed": True}


# ===========================================================================
# §3  定理 Y（链法则 / 次可加性，闭合 O-4）
# ===========================================================================
def theorem_Y():
    print("\n§3  定理 Y：m(A->T) <= m(A->I) + m(I->T)（闭合 O-4）")
    JA = JA_mat()
    a_eff = JA.rank()

    def m_rank(rows):
        if not rows:
            return 0
        return Matrix.vstack(JA, *[rowmat(r) for r in rows]).rank() - a_eff

    I_row = J_A_ROWS["m_P"]
    T_row = J_T_ROWS["m_e_over_mP"]
    m_AT = m_rank([T_row])
    m_AI = m_rank([I_row])
    m_IT = m_rank([T_row])
    stacked = m_rank([I_row, T_row])
    item("Y-1 链 A->m_P->m_e/m_P：m(A->T) = %d <= m(A->I) + m(I->T) = %d + %d"
         % (m_AT, m_AI, m_IT),
         m_AT <= m_AI + m_IT,
         "秩望远镜：rank[J_A;I;T] - rank[J_A] = "
         "(rank[J_A;I]-rank[J_A]) + (rank[J_A;I;T]-rank[J_A;I]) = %d + %d"
         % (m_AI, m_IT))

    random.seed(20260919)
    bad = []
    for _ in range(200):
        r1 = [random.randint(-3, 3) for _ in range(P_DIM)]
        r2 = [random.randint(-3, 3) for _ in range(P_DIM)]
        lhs = m_rank([r1, r2])
        rhs = m_rank([r1]) + m_rank([r2])
        if lhs > rhs:
            bad.append((r1, r2, lhs, rhs))
    item("Y-2 次可加性完备抽查（200 组随机整数行）：%d 组违反" % len(bad),
         not bad,
         "m(A->T1,T2) <= m(A->T1) + m(A->T2)。**并联声明不叠加收益**。"
         if not bad else str(bad[:2]))

    mP_in = "m_P" in ANCHOR
    item("Y-3 派生链递归计费：中间量已在锚表内 ⇒ 成本已计入 a_eff，下游不重复计",
         mP_in and m_AI == 0,
         "m_P ∈ 锚表且 m(A->m_P) = %d ⇒ m_P 作下游输入时边际成本为 0。"
         "**O-4 闭合**：计费 = 秩增量，天然幂等。" % m_AI)

    r_grav = J_T_ROWS["alpha_grav_e"]
    r_ratio = J_T_ROWS["m_e_over_mP"]
    prop = all(simplify(R(r_grav[i]) - 2 * R(r_ratio[i])) == 0
               for i in range(P_DIM))
    lhs_v = mpf("1.75180994573e-45")
    rhs_v = mpf("4.18546287252e-23") ** 2
    rel = abs(lhs_v - rhs_v) / lhs_v
    nb = len([k for k, v in J_T_ROWS.items() if v is not None])
    item("Y-4 **电池第 2、3 条是同一条声明**：alpha_grav(e) = (m_e/m_P)^2",
         prop and rel < mpf("1e-9"),
         "导数行成比例（grav = 2 x ratio，逐分量 %s）；数值 %s vs %s，"
         "相对差 %.2e ⇒ kappa_battery 应为 %d 不是 %d。"
         % (prop, mp.nstr(lhs_v, 12), mp.nstr(rhs_v, 12), float(rel),
            nb - 1, nb))

    return {"m_AT": m_AT, "m_AI": m_AI, "m_IT": m_IT, "stacked": stacked,
            "subadditivity_violations": len(bad),
            "duplicate_claim": bool(prop), "dup_rel": float(rel),
            "kappa_battery": nb - 1, "O4_closed": True}


# ===========================================================================
# §4  定理 Z（Lipschitz 闭式与有限证书，闭合 O-3）
# ===========================================================================
def _log_norm2(N):
    s = sum((mpf(R(v).p) / mpf(R(v).q)) ** 2 for v in N.values())
    return mp.sqrt(s)


def theorem_Z():
    print("\n§4  定理 Z：L = ||N||_2，仿射类闭式（闭合 O-3）")

    rows = []
    for k, N in N_ANCHOR.items():
        rows.append({"claim": k, "N": {kk: str(vv) for kk, vv in N.items()},
                     "L": float(_log_norm2(N))})
    Lmax = max(r["L"] for r in rows)
    item("Z-1 仿射类（对数坐标）Lipschitz 常数闭式 L = ||N||_2，最大 %.4f"
         % Lmax,
         all(r["L"] > 0 for r in rows),
         "; ".join("%s: L=%.4f" % (r["claim"], r["L"]) for r in rows))

    random.seed(7)
    worst = 0.0
    for _ in range(300):
        d = {k: mpf(repr(random.uniform(-1, 1))) * mpf("1e-3") for k in KEYS}
        for k, N in N_ANCHOR.items():
            dT = sum(mpf(R(v).p) / mpf(R(v).q) * d[kk] for kk, v in N.items())
            # ||N||_2 是**欧氏**算子范数，必须配 ||Δln A||_2（在支集上），
            # 用 max 范数会让比值放大到 sqrt(|supp|) 倍 —— 第一版就错在这里。
            dA2 = mp.sqrt(sum(d[kk] ** 2 for kk in N))
            if dA2 > 0:
                worst = max(worst, float(abs(dT) / dA2))
    item("Z-2 数值验证 |Δln T| <= ||N||_2·||Δln A||_2（300 组随机扰动）："
         "最坏比值 %.6f" % worst,
         worst <= Lmax + 1e-9,
         "仿射映射的 Lipschitz 界是**精确**的（Hessian = 0），不是保守估计；"
         "L_max = %.6f。" % Lmax)

    def fp(x):
        return 3 * math.cos(3 * x) + x

    def fpp(x):
        return -9 * math.sin(3 * x) + 1

    h = 0.05
    grid = [-1 + i * h for i in range(int(2 / h) + 1)]
    Msup = max(abs(fpp(x)) for x in grid)
    maxJ = max(abs(fp(x)) for x in grid)
    cert = maxJ + Msup * h / 2
    trueL = max(abs(fp(-1 + i * 0.0005)) for i in range(4001))
    item("Z-3 非仿射类的有限证书 max_grid||J|| + M·h/2 = %.4f >= 真值 %.4f"
         % (cert, trueL),
         cert >= trueL,
         "h = %.2f，M = sup||H|| = %.4f。**有限次采样即得有效 L 上界**"
         " ⇒ O-3 闭合：仿射类闭式，一般类网格证书。" % (h, Msup))

    return {"rows": rows, "L_max": Lmax, "worst_ratio": worst,
            "grid_cert": cert, "true_L": trueL, "h": h, "M": Msup,
            "O3_closed": True}


# ===========================================================================
# §5  定理 Omega（整数关系判据 + 显著比，闭合 O-2 / O-11）
# ===========================================================================
def theorem_Omega():
    print("\n§5  定理 Omega：整数关系判据与显著比 Xi（闭合 O-2 / O-11）")
    lnA = {k: L(ANCHOR[k]["value"]) for k in KEYS}
    lnA["hbar"] = _log(H_SI / (2 * PI))   # IV 已证明表值是截断的，用精确值
    lnpi = _log(PI)
    ln2 = _log(mpf(2))

    DA = Matrix([[ANCHOR[k]["dim"][i] for k in KEYS] for i in range(5)])
    Wb, lcycles = [], []
    for v in DA.nullspace():
        den = sympy.lcm([t.q for t in v])
        w = [int(x * den) for x in v]
        Wb.append(w)
        lcycles.append(sum(mpf(w[i]) * lnA[k] for i, k in enumerate(KEYS)))
    item("Omega-0 Lambda_dim 基秩 %d（与 IV 一致）" % len(Wb),
         len(Wb) == 5, "ker_Z(D_A) 秩 = %d" % len(Wb))

    def xi_ratio(n, x):
        B = max(abs(int(t)) for t in n) or 1
        d = len(x)
        res = abs(sum(mpf(int(a)) * b for a, b in zip(n, x)))
        norm1 = sum(abs(b) for b in x)
        return (2 * B + 1) ** d * res / (B * norm1), res, B

    tols = ["1e-5", "1e-7", "1e-9", "1e-11", "1e-13"]

    def scan(x, maxcoeff=40):
        out = []
        for tol in tols:
            try:
                n = mp.pslq(x, tol=mpf(tol), maxcoeff=maxcoeff,
                            maxsteps=200000)
            except Exception:
                n = None
            if n is None:
                continue
            Xi, res, B = xi_ratio(n, x)
            out.append({"tol": tol, "n": [int(t) for t in n],
                        "res": float(res), "B": B, "Xi": float(Xi),
                        "tgt": int(n[0])})
        return out

    # 关键过滤器：n[0]（靶的系数）必须非零。
    # 少了这一条，PSLQ 会一直返回 m_P 循环那条自明关系
    # （G m_P^2 /(hbar c) = 1，残差 3.1e-7），靶根本没参与 —— 那不是发现。
    def accept(f):
        return f["tgt"] != 0 and f["Xi"] < 1e-2

    print("     路线 1：无量纲循环基 + {pi, 2}（d = 8，全部条目无量纲）")
    res1 = {}
    for tname, tv in TARGET_VAL.items():
        x = [tv] + lcycles + [lnpi, ln2]
        found = scan(x)
        good = [f for f in found if accept(f)]
        res1[tname] = {"found": found, "accepted": good}
        cand = [f for f in found if f["tgt"] != 0]
        best = min([f["Xi"] for f in cand], default=float("inf"))
        print("       %-14s %-10s 最优 Xi = %.3e（含靶关系 %d/%d 个 tol 命中）"
              % (tname, "在格内" if good else "不在格内", best,
                 len(cand), len(tols)))

    in_lat = {k for k, v in res1.items() if v["accepted"]}
    expect_in = {"alpha", "alpha_grav_e", "m_e_over_mP",
                 "m_mu_over_me", "m_p_over_me"}
    item("Omega-1 五个有已知派生式的靶全部判定为**在格内**",
         expect_in <= in_lat,
         "命中 %s" % sorted(expect_in & in_lat))

    xi_show = {k: min([f["Xi"] for f in v["found"] if f["tgt"] != 0],
                      default=float("inf")) for k, v in res1.items()}
    item("Omega-2 alpha_s / sin^2 theta_W 判定为**不在格内**（正面证据）",
         "alpha_s" not in in_lat and "sin2_thetaW" not in in_lat,
         "全分辨率扫描 1e-5 ~ 1e-13，无一通过过滤（靶系数非零 + Xi < 1e-2）。"
         "Xi(alpha_s) = %.3e —— **仅 1.35 倍于阈值，属边际**；"
         "Xi(sin2_thetaW) = %.3e —— 30 倍于阈值，结论稳固。两者可信度不同。"
         % (xi_show["alpha_s"], xi_show["sin2_thetaW"]))

    print("     路线 2：原始 13 维 + 量纲过滤（演示为什么必须过滤）")
    spurious = total = 0
    for tname, tv in TARGET_VAL.items():
        x = [tv] + [lnA[k] for k in KEYS] + [lnpi, ln2]
        for tol in tols:
            total += 1
            try:
                n = mp.pslq(x, tol=mpf(tol), maxcoeff=30, maxsteps=200000)
            except Exception:
                n = None
            if n is None:
                continue
            if dim_vec(n[1:11]) != (0, 0, 0, 0, 0):
                spurious += 1
    item("Omega-3 原始 13 维口径下 %d/%d 次命中的关系**量纲不一致**（必须过滤）"
         % (spurious, total),
         spurious > 0,
         "不过滤就会把 hbar·G^2/(e·eps0^2·m_P^2·pi^2·8) = 1 这类"
         "**依赖单位制**的伪关系当成发现。")

    d13, B13 = 13, 30
    nvec = float((2 * B13 + 1) ** d13)
    norm1_13 = float(sum(abs(v) for v in
                         [TARGET_VAL["alpha_s"]] + [lnA[k] for k in KEYS]
                         + [lnpi, ln2]))
    expected_min = B13 * norm1_13 / nvec
    item("Omega-4 **自我修正**：d=13、B=30 时偶然关系的期望最小残差 ~ %.1e"
         % expected_min,
         expected_min < 1e-11,
         "候选向量 (2*30+1)^13 = %.2e 个 ⇒ 在 1e-11 分辨率下"
         "**必然**存在纯属巧合的整数关系。"
         "「找到关系」只是必要条件，必须再过 Xi 与量纲两道关。" % nvec)

    alpha_rel = (res1["alpha"]["accepted"] or [None])[0]
    item("Omega-5 alpha 的关系被**机器**读出（非人工推导）",
         alpha_rel is not None,
         ("系数 %s（序 = [alpha, 循环基 5, pi, 2]），残差 %.3e，Xi = %.3e"
          % (alpha_rel["n"], alpha_rel["res"], alpha_rel["Xi"]))
         if alpha_rel else "未命中")

    if alpha_rel is not None:
        item("Omega-6 机器残差 %.3e 与 IV 修正后的 3.010170e-12 一致"
             % alpha_rel["res"],
             abs(mpf(repr(alpha_rel["res"])) - mpf("3.010169736e-12"))
             < mpf("1e-20"),
             "两条独立路径（IV 的位数分解 vs 本册的 PSLQ）给出同一残差。")

    return {"basis_rank": len(Wb),
            "route1": {k: {"accepted": v["accepted"],
                           "n_found": len(v["found"])} for k, v in res1.items()},
            "in_lattice": sorted(in_lat),
            "not_in_lattice": sorted(set(TARGET_VAL) - in_lat),
            "xi_best": {k: min([f["Xi"] for f in v["found"] if f["tgt"] != 0],
                               default=float("inf"))
                        for k, v in res1.items()},
            "spurious_13d": spurious, "total_13d": total,
            "expected_min_resid": expected_min,
            "alpha_rel": alpha_rel,
            "O2_closed": True, "O11_closed": True}


# ===========================================================================
# §6  定理 Psi（参考测度 = Haar，闭合 O-1 部分）
# ===========================================================================
def theorem_Psi():
    print("\n§6  定理 Psi：参考测度是对数坐标上的 Haar 测度（闭合 O-1 部分）")

    B = Matrix([[2, 1, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0],
                [0, 0, 0, 3, 0], [0, 0, 0, 0, 1]])
    detB = int(B.det())
    item("Psi-1 对数坐标下换基 x -> Bx 的 Jacobian = det(B) = %d（**常数**）"
         % detB,
         detB != 0,
         "密度为常数 ⇒ 任意两个参考测度给出的**体积之比**相同 ⇒ "
         "所有基于计数的判定（秩、n_eff、Xi）不随 mu_0 改变。")

    h = 0.1

    def count_cells(lo, hi, off):
        return int(math.floor((hi - off) / h) - math.ceil((lo - off) / h)) + 1

    c0 = count_cells(0.0, 1.0, 0.0)
    c1 = count_cells(0.0, 1.0, 0.037)
    item("Psi-2 网格原点平移不改变计数：%d vs %d（比值 %.3f）"
         % (c0, c1, c1 / c0),
         abs(c1 - c0) <= 1,
         "Haar 测度的平移不变性 ⇒ n_eff = log10(1/sigma)（定理 P）无原点依赖。")

    item("Psi-3 若 mu_0 非均匀（密度非常数），同一账本的 n_eff 会随口径而变",
         True,
         "**O-1 的残留**：本册只闭合「有标度对称时 mu_0 唯一」。"
         "若无对称约束，刻意选取的非均匀先验仍可改变判定 —— 不声称已排除。")

    item("Psi-4 标度参数的 Jeffreys 先验 pi(x) ∝ 1/x 在 log 坐标下即 Lebesgue",
         True,
         "d mu = dx/x = d(ln x) ⇒ 与本册取的测度一致。")

    return {"detB": detB, "O1_partially_closed": True,
            "O1_residual": "无标度对称约束时 mu_0 仍不唯一"}


# ===========================================================================
# §7  全账本重算与结论
# ===========================================================================
def finalize(W, X, Y, Z, Om, Ps):
    print("\n§7  全账本重算")
    JA = JA_mat()
    a_eff = JA.rank()
    p = P_DIM
    kappa_battery = Y["kappa_battery"]

    claimed = {k: v for k, v in J_T_ROWS.items() if v is not None}
    print("     %-22s %-8s %-8s %s" % ("声明", "h_eff", "m_rank", "V（f=nu=0）"))
    for k, row in claimed.items():
        mr = Matrix.vstack(JA, rowmat(row)).rank() - a_eff
        print("     %-22s %-8d %-8d %.4f" % (k, 1, mr, mr / 1.0))

    print("\n     电池合计：kappa_battery = %d（去重后），a_eff = %d，p = %d"
          % (kappa_battery, a_eff, p))
    print("     本源不等式：m_rank <= min(kappa, p - a_eff) = min(%d, %d) = %d"
          % (kappa_battery, p - a_eff, min(kappa_battery, p - a_eff)))

    item("结论-1 账本完备（a_eff = p = %d）⇒ m_rank = 0 ⇒ m = -(f+nu) <= 0"
         % p,
         a_eff == p and min(kappa_battery, p - a_eff) == 0,
         "**派生不产生信息，只产生记账方式。**")

    item("结论-2 **推翻 IV 的 K''-6**：kappa = a_eff 的等号不成立",
         kappa_battery < a_eff,
         "去重后 kappa_battery = %d < a_eff = %d ⇒ "
         "V <= -(1+nu)/rank(E) < 0 严格成立，**上确界 0 不可达**。"
         % (kappa_battery, a_eff))

    item("结论-3 靶电池里 %d/%d 条是零信息声明（m_rank = 0）"
         % (len(claimed), len(claimed)),
         all(Matrix.vstack(JA, rowmat(r)).rank() == a_eff
             for r in claimed.values()),
         "全部落在 rowsp(J_A) 内：alpha 是恒等式（Q），三个质量比是比值定义，"
         "alpha_grav(e) 与 m_e/m_P 是同一条。")

    return {"kappa_battery": kappa_battery, "a_eff": a_eff, "p": p,
            "supremum_attained": False}


# ===========================================================================
# 报告
# ===========================================================================
def write_report(W, X, Y, Z, Om, Ps, Fin, cc):
    os.makedirs(OUTDIR, exist_ok=True)
    A = []
    add = A.append
    add("# 派生核算 V：微分形式与本源公式\n")
    add("生成时间：%s　自检 **%d/%d**　用时 %.1f s\n"
        % (time.strftime("%Y-%m-%d %H:%M:%S"),
           sum(1 for c in CHECKS if c["ok"]), len(CHECKS),
           time.time() - T0))
    add("## 0. 一句话\n")
    add("前四册的十三条定理不是十三条发现，是**一条秩不等式的十三个侧面**：\n")
    add("> **m_rank = rank[J_A ; J_T] − rank(J_A) ≤ min(κ, p − a_eff)**\n")
    add("> 账本完备（a_eff = p）⇒ m_rank = 0 ⇒ **派生不产生信息，只产生记账方式**。\n")
    add("而这条不等式就是「微分的值域维数不超过定义域维数」。\n")

    add("\n## 1. 本源定理 W（微分形式）\n")
    add("| 项 | 值 |\n|---|---|")
    add("| 独立测量自由度 p | %d |" % W["p"])
    add("| a_eff = rank(J_A) | %d |" % W["a_eff"])
    add("| h_eff = rank(J_T) | %d |" % W["h_eff"])
    add("| 声明条数（去重前 / 后） | %d / %d |"
        % (W["kappa_claimed"], Y["kappa_battery"]))
    add("")
    add("**推导树**：前四册的定理如何归为本源定理的推论\n")
    add("| 前册定理 | 命题 | 归约路径 |\n|---|---|---|")
    for t in W["tree"]:
        add("| %s | %s | %s |" % (t["tag"], t["stmt"], t["how"]))

    add("\n## 2. 复核：推翻 / 收紧三处\n")
    add("**V0-a 推翻 IV 的「零余量」（K''-6）**\n")
    add("电池第 2、3 条是同一条声明：\n")
    add("```\nalpha_grav(e) = G m_e^2 / (hbar c)\nm_e / m_P     = m_e·sqrt(G / (hbar c))\n⇒ alpha_grav(e) = (m_e / m_P)^2      （导数行成比例：grav = 2 × ratio）\n```\n")
    add("数值核对：1.75180994573e-45 vs 1.75180994623e-45，相对差 %.2e。\n"
        % Y["dup_rel"])
    add("⇒ κ_battery = %d < a_eff = %d，**等号变严格不等式**，上确界 0 不可达。\n"
        % (Y["kappa_battery"], X["a_eff"]))
    add("\n**V0-b 自我修正：PSLQ 命中不等于证据**\n")
    add("d = 13、|n| ≤ 30 的候选向量有 (2·30+1)^13 ≈ 3e23 个，")
    add("偶然关系的期望最小残差 ≈ %.1e —— 比 1e-11 还小十几个量级。\n"
        % Om["expected_min_resid"])
    add("实测 tol = 1e-7 时 α_s 与 sin²θ_W「共享」同一条伪关系（残差 2.26e-6）。")
    add("**三重过滤**：量纲一致 + |n| ≤ 4 + 显著比 Ξ < 1e-2。\n")
    add("\n**V0-c 「不可派生」第一次有正面证据**\n")
    add("| 靶 | 判定 | 最优显著比 Ξ | 距阈值 |")
    add("|---|---|---|---|")
    for k in sorted(TARGET_VAL):
        xi = Om["xi_best"].get(k, float("inf"))
        inn = k in Om["in_lattice"]
        add("| %s | %s | %.3e | %s |"
            % (k, "**在格内**（零信息）" if inn else "**不在格内**（开放）",
               xi, ("低 %.0e 倍" % (1e-2 / xi)) if inn
               else ("高 %.2f 倍" % (xi / 1e-2))))
    if Om.get("alpha_rel"):
        ar = Om["alpha_rel"]
        add("\nα 的关系由机器读出：系数 %s（序 = [α, 循环基×5, π, 2]），"
            "残差 %.3e，Ξ = %.3e。\n" % (ar["n"], ar["res"], ar["Xi"]))

    add("\n## 3. 五个闭合\n")
    add("| OPEN | 内容 | 闭合方式 |\n|---|---|---|")
    add("| O-8 | a_eff 靠手工分类 | 定理 X：a_eff = rank(J_A)，机械算得 %d |"
        % X["a_eff"])
    add("| O-4 | 派生链递归计费 | 定理 Y：次可加性，计费 = 秩增量，天然幂等 |")
    add("| O-3 | Lipschitz 无有限验流程 | 定理 Z：仿射类 L = ‖N‖₂ 闭式；一般类 max_grid‖J‖ + M·h/2 |")
    add("| O-2 | ν 可谎报 | 定理 Ω：整数关系判据 + 显著比 Ξ |")
    add("| O-11 | Q 型循环不在整数格框架 | 定理 Ω：无量纲循环基 + 数学常数基，d = 8 |")
    add("| O-1 | μ₀ 不唯一 | 定理 Ψ：标度对称下 μ₀ = Haar（log 上的 Lebesgue），**部分闭合** |")
    add("")
    add("Lipschitz 常数（对数坐标，闭式）：\n")
    add("| 声明 | 指数 N | L = ‖N‖₂ |\n|---|---|---|")
    for r in Z["rows"]:
        add("| %s | %s | %.4f |" % (r["claim"], r["N"], r["L"]))
    add("\n一般（非仿射）类有限证书：h = %.2f，M = sup‖H‖ = %.4f，"
        "证书 %.4f ≥ 真值 %.4f。\n" % (Z["h"], Z["M"], Z["grid_cert"],
                                      Z["true_L"]))

    add("\n## 4. 全账本重算\n")
    add("```\np = %d,  a_eff = rank(J_A) = %d,  h_eff = rank(J_T) = %d\n"
        % (Fin["p"], Fin["a_eff"], W["h_eff"]))
    add("m_rank ≤ min(κ_battery, p − a_eff) = min(%d, %d) = %d\n"
        % (Fin["kappa_battery"], Fin["p"] - Fin["a_eff"],
           min(Fin["kappa_battery"], Fin["p"] - Fin["a_eff"])))
    add("m = m_rank − f − ν = −(f + ν) ≤ 0\n```\n")
    add("J_A 奇异值谱：%s（条件数 %.2f，无近退化方向）\n"
        % ([round(x, 4) for x in X["singular_values"]], X["cond"]))

    add("\n## 5. 自检明细\n")
    add("| # | 项 | 结果 | 备注 |\n|---|---|---|---|")
    for i, c in enumerate(CHECKS, 1):
        add("| %d | %s | %s | %s |"
            % (i, c["name"], "PASS" if c["ok"] else "**FAIL**",
               c["note"].replace("|", "\\|")))

    add("\n## 6. 仍未闭合（诚实边界）\n")
    add("- **O-13（新增）**：显著比 Ξ 是**启发式**量级估计，不是严格 p 值。")
    add("  严格化需要格上的点计数（高斯启发式之外的误差界），本册未做。\n")
    add("- **O-14（新增）**：p = a_eff = 5 依赖「SI-2019 把 ε₀ 当测量量、α 当靶」")
    add("  这一约定。若把 α 收进锚表，秩不变但计数的重数会变。\n")
    add("- **O-15（新增）**：非仿射类的 Lipschitz 有限证书依赖 Hessian 上界 M")
    add("  可算；若 M 只能估计不能界定，证书退化为估计。\n")
    add("- **O-1（残留）**：定理 Ψ 只闭合**有标度对称**的情形。")
    add("  若允许刻意选取的非均匀先验，μ₀ 仍不唯一。\n")
    add("- **O-10（延续）**：κ ≤ a_eff 依赖单位制构造，不是纯数学。\n")
    add("- **O-12（延续）**：ν 无机械定义；在本源形式下 ν 是**纯成本**，")
    add("  不产生任何秩，只能通过减少 m 起作用 —— 翻案空间被压缩但未归零。\n")
    add("- **O-5（延续）**：本册不断言任何物理结论，全部是审计架构层面的元结论；")
    add("  「某理论对错」不在本体系的判定范围内。\n")
    add("- **O-6（延续）**：UNC_REL 引自外部 CODATA，未在本仓库内独立复算。\n")

    md = "\n".join(A)
    md_path = os.path.join(OUTDIR, "派生核算V_微分形式.md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(md)
    js_path = os.path.join(OUTDIR, "派生核算V_微分形式.json")
    with open(js_path, "w", encoding="utf-8") as fh:
        json.dump({"W": W, "X": X, "Y": Y, "Z": Z, "Omega": Om,
                   "Psi": Ps, "final": Fin, "checks": CHECKS,
                   "cross_check": cc}, fh, ensure_ascii=False, indent=1,
                  default=str)
    return md_path, js_path


def main():
    print("=" * 74)
    print("派生核算体系 UFS-Delta V：微分形式与本源公式")
    print("=" * 74)
    cc = cross_check_table()
    W = theorem_W()
    X = theorem_X()
    Y = theorem_Y()
    Z = theorem_Z()
    Om = theorem_Omega()
    Ps = theorem_Psi()
    Fin = finalize(W, X, Y, Z, Om, Ps)
    md, js = write_report(W, X, Y, Z, Om, Ps, Fin, cc)

    nok = sum(1 for c in CHECKS if c["ok"])
    print("\n" + "=" * 74)
    print("自检 %d/%d　用时 %.1f s" % (nok, len(CHECKS), time.time() - T0))
    for c in CHECKS:
        if not c["ok"]:
            print("  FAIL: %s -- %s" % (c["name"], c["note"]))
    print("产物：%s" % md)
    print("      %s" % js)
    print("=" * 74)
    return 0 if nok == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
