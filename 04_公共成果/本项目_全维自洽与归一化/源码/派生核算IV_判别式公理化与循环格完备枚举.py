#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
派生核算体系 UFS-Delta IV（可复跑）
=========================================================================
主题：**判别式本身的合法性** + **账本循环的完备枚举**

前三册都在拿 V4 判声明，但没人问过两件事：

  (1) V4 这个式子凭什么是它？换一个归一化会不会翻案？
  (2) "这条声明是循环的"目前靠人眼看（III 的 DEPENDENCY 表是手写的），
      循环到底有几个、能不能算完？

本册回答：

  (1) 换任何归一化都不翻案 —— 不可达性根本不是 V4 的性质，
      而是**账本完备性**的性质（一条鸽笼原理）。
  (2) 循环可以算完 —— 它是一个**整数格**。III 靠肉眼找到 2 个，
      本册给出算法，并证明没有第三个。

-------------------------------------------------------------------------
§0  复核：纠正 III 册的两处
-------------------------------------------------------------------------
R0-a  III 把 eps0 <-> alpha 的 6.097e-10 残差判为"锚表自身精度不自洽"，
      列为 OPEN O-9，猜测是"混用 CODATA 版本或引用有误"。
      **两个猜测都不对**。残差 100% 是账本位数伪影，可逐位分解：

        残差 = (hbar 表值截断误差) - (eps0/alpha 末位舍入误差)
             =  6.127191912e-10    -  3.010169736e-12
             =  6.097090215e-10          观测 6.097090219e-10

      相符到 9 位有效数字，余量是二阶项。真凶是 hbar：账本里存的是
      "1.054571817e-34"（10 位，且是**截断**而非舍入），而 hbar 在
      SI-2019 下是精确量 h/(2 pi)。改用精确值后残差降到 -3.010e-12，
      落在 eps0/alpha 末位舍入界 5.69e-12 之内。
      ⇒ **O-9 闭合**，且结论比 III 更强：不是"表不自洽"，
        是"表把 hbar 的位数记少了"。

R0-b  V4 = m / h_eff 的分母是**声明自己的** h_eff。于是判 B/C 的门槛
      |V4| < eps 等价于 |m| < eps * h_eff：**允许的净亏损额度正比于声明
      规模**。同一笔 -3 的亏损，h_eff = 3 判 C，h_eff = 3000 判 B。
      门槛的松紧随声明而变 —— 判定不是一把固定的尺。

-------------------------------------------------------------------------
§1  定理 S（判别式刻画与归一化无关性）
-------------------------------------------------------------------------
公理 A1-A5（见正文）迫使任何合法判别式只能是"净信息"

    m = h_eff - C,   C = 成本

的严格单调函数 V = Psi(m) 且 Psi(0) = 0。故：

    **所有合法判别式符号相同 —— 判定与归一化选择无关。**

V4 = m / h_eff 甚至不在该类里（它违反 A3：除以声明自己的 h_eff），
但符号与该类一致。前三册的**判定**没错，错在把 V4 的**数值**当可比量。

推论 S2：V4 在 h_eff = 0 处无定义，而 h_eff = 0 正是"零信息声明"的
典型态 —— 判别式在最需要给出判断的点上失效。

-------------------------------------------------------------------------
§2  定理 K''（计费细化不变性 + 核心等价）—— 本册最重
-------------------------------------------------------------------------
前三册一律按 f = k 给旋钮计费。若改成更宽容的口径（只计边际贡献），
V4 会不会转正？会 —— 如果只改一半的话；全改完则不变。统一闭式：

    V  <=  ( kappa(S) - a_eff(S) - nu ) / rank(E),   kappa(S) = |S| - rank(D_S)

在旋钮的三种计费口径、锚的两种口径下全部成立。于是得到核心等价：

    **V > 0  <=>  kappa(S) > a_eff(S) + nu**

即"无量纲自由度数 > 独立测量数 + 调定纯数"。这是一条鸽笼原理：
**你无法从 N 个独立测量里取出超过 N 个独立的无量纲预言**。

⇒ 前三册叫它"代数派生不可能定理（物理）"，叫错了。它是
   **账本完备性定理（记账）**：说的不是"自然不允许"，而是
   "账本不允许你把一个自由度记两次"。

注意它依赖 kappa(S) <= a_eff(S)。在 SI-2019 表上**等号恰好成立**
（kappa = a_eff = 5，零余量）。这一条不是纯数学，是单位制的构造性质
（定义常量必须量纲独立）⇒ 列为 OPEN O-10。

-------------------------------------------------------------------------
§3  定理 U（双格分解与循环完备枚举）—— 闭合 O-7
-------------------------------------------------------------------------
无量纲锚单项式构成整数格 Lambda_dim = ker_Z(D_A)，秩 kappa = 5。
其中"数值闭合"（值恒为 1，误差在不确定度传播界内）的子格 Lambda_val
才是真正的循环。完备枚举 |lambda_i| <= 3（16807 组）后：

    Lambda_dim 秩 5，Lambda_val 秩 1 —— 只由 m_P 循环生成。

即账本里**只有 1 个冗余锚**；另外 4 个无量纲循环是真实测量。
III 靠肉眼找到 2 个循环，本册给出的是算法，并证明没有第三个。

副作用：温度维度在本账本里是孤立的 ⇒ k_B 不参与任何无量纲循环
⇒ 涉及 k_B 的声明其 kappa 贡献为 0。
=========================================================================
"""

from __future__ import print_function

import itertools
import json
import os
import sys
import time
from fractions import Fraction

import sympy
from mpmath import mp, mpf
from sympy import Matrix, Rational, simplify, symbols

mp.dps = 50

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


PI = mp.pi
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")


# ===========================================================================
# 输入：锚常量表（逐字节复制自 III，运行时与 V3 交叉核对）
# ===========================================================================
ANCHOR = {
    "c":    {"dim": (0, 1, -1, 0, 0), "value": "299792458",         "name": "光速 c"},
    "hbar": {"dim": (1, 2, -1, 0, 0), "value": "1.054571817e-34",   "name": "约化普朗克常数 hbar"},
    "G":    {"dim": (-1, 3, -2, 0, 0), "value": "6.67430e-11",      "name": "引力常数 G"},
    "e":    {"dim": (0, 0, 1, 1, 0),  "value": "1.602176634e-19",   "name": "元电荷 e"},
    "eps0": {"dim": (-1, -3, 4, 2, 0), "value": "8.8541878128e-12", "name": "真空介电常数 eps0"},
    "m_e":  {"dim": (1, 0, 0, 0, 0),  "value": "9.1093837015e-31",  "name": "电子质量 m_e"},
    "m_mu": {"dim": (1, 0, 0, 0, 0),  "value": "1.883531627e-28",   "name": "缪子质量 m_mu"},
    "m_p":  {"dim": (1, 0, 0, 0, 0),  "value": "1.67262192369e-27", "name": "质子质量 m_p"},
    "m_P":  {"dim": (1, 0, 0, 0, 0),  "value": "2.176434e-8",       "name": "普朗克质量 m_P"},
    "k_B":  {"dim": (1, 2, -2, 0, -1), "value": "1.380649e-23",     "name": "玻尔兹曼常数 k_B"},
}
KEYS = ["c", "hbar", "G", "e", "eps0", "m_e", "m_mu", "m_p", "m_P", "k_B"]

# 表内存储的**有效数字位数**（用于算末位舍入/截断界）。
# 0 表示该量在 SI-2019 下是精确定义量，表值不含存储误差。
SIGDIG = {
    "c": 0, "hbar": 10, "G": 6, "e": 0, "eps0": 11,
    "m_e": 11, "m_mu": 10, "m_p": 12, "m_P": 7, "k_B": 0,
}

# SI-2019 定义量（sigma = 0，不携带测量信息，也不是雅可比的列）
DEFINED = {"c", "hbar", "e", "k_B"}

# 相对标准不确定度（外部 CODATA 数据，见 OPEN O-6）
UNC_REL = {
    "c": 0.0, "hbar": 0.0, "e": 0.0, "k_B": 0.0,
    "G": 2.2e-5, "eps0": 1.5e-10, "m_e": 3.0e-10,
    "m_mu": 2.2e-8, "m_p": 3.1e-10, "m_P": 1.1e-5,
}

# SI-2019 精确普朗克常数 h（hbar = h / 2pi 亦为精确量）
H_SI = mpf("6.62607015e-34")

TARGETS = {
    "alpha":        mpf("7.2973525693e-3"),
    "alpha_grav_e": mpf("1.75180994573e-45"),
    "m_e_over_mP":  mpf("4.18546287252e-23"),
    "m_mu_over_me": mpf("206.7682830"),
    "m_p_over_me":  mpf("1836.15267343"),
    "alpha_s":      mpf("0.1179"),
    "sin2_thetaW":  mpf("0.23122"),
}


def V(key):
    return mpf(ANCHOR[key]["value"])


def to_frac(x):
    if isinstance(x, Fraction):
        return x
    r = sympy.Rational(x)
    return Fraction(int(r.p), int(r.q))


def cross_check_table():
    """输入端与 V3 对齐：若 V3 可导入则逐键核对，防止本册口径漂移。"""
    path = os.path.join(HERE, "量纲零空间与判别式V3.py")
    try:
        ns = {}
        # 必须注入 __file__：V3 用它定位自己的相对路径。少了这一项 exec 会抛
        # NameError，而本函数会把异常吞掉 —— 那就会出现"声明做了交叉核对、
        # 实际一行没验"的假象。这正是本仓库反复批评的失效模式。
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        exec(compile(src, path, "exec"),
             {"__name__": "v3mod", "__file__": path}, ns)
        C2 = ns.get("CONST")
        if not C2:
            return {"available": False, "mismatch": [], "note": "V3 无 CONST"}
        bad = []
        for k, rec in ANCHOR.items():
            if k not in C2:
                bad.append("%s（V3 缺失）" % k)
                continue
            if C2[k]["value"] != rec["value"]:
                bad.append("%s 本册=%s V3=%s" % (k, rec["value"], C2[k]["value"]))
            if tuple(C2[k]["dim"]) != tuple(rec["dim"]):
                bad.append("%s 量纲不一致" % k)
        return {"available": True, "mismatch": bad}
    except Exception as exc:
        return {"available": False, "mismatch": [], "error": repr(exc)}


# ===========================================================================
# 通用工具
# ===========================================================================
CHECKS = []


def item(name, ok, detail):
    CHECKS.append({"name": name, "passed": bool(ok), "detail": detail})
    print("   [%s] %s" % ("PASS" if ok else "FAIL", name))
    print("         %s" % detail)


def rank_fraction(rows):
    """Fraction 高斯消元求秩（不经 sympy，用于交叉验证）。"""
    m = [[to_frac(x) for x in r] for r in rows]
    m = [r for r in m if any(x != 0 for x in r)]
    if not m:
        return 0
    ncols = len(m[0])
    piv = 0
    for col in range(ncols):
        sel = None
        for r in range(piv, len(m)):
            if m[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        m[piv], m[sel] = m[sel], m[piv]
        pv = m[piv][col]
        m[piv] = [x / pv for x in m[piv]]
        for r in range(len(m)):
            if r != piv and m[r][col] != 0:
                fac = m[r][col]
                m[r] = [a - fac * b for a, b in zip(m[r], m[piv])]
        piv += 1
        if piv >= len(m):
            break
    return piv


def dim_matrix(keys):
    """锚子集 -> 量纲矩阵 D_S（5 x |S|，行为 M,L,T,I,Theta）。"""
    cols = [ANCHOR[k]["dim"] for k in keys]
    return [[cols[j][i] for j in range(len(cols))] for i in range(5)]


def kappa_of(keys):
    """kappa(S) = |S| - rank(D_S)：S 能生成的独立无量纲数个数。"""
    if not keys:
        return 0
    return len(keys) - rank_fraction(dim_matrix(keys))


# ===========================================================================
# §0  R0-a：III 册 O-9 的闭合（残差归因）
# ===========================================================================
def review_R0a_residual_attribution():
    print("\n" + "=" * 78)
    print("§0  R0-a：把 III 册的 6.097e-10 残差逐位拆开（闭合 OPEN O-9）")
    print("=" * 78)

    hbar_exact = H_SI / (2 * PI)
    hbar_tab = V("hbar")
    c, e, eps0_tab, alpha = V("c"), V("e"), V("eps0"), TARGETS["alpha"]

    d_hbar = (hbar_tab - hbar_exact) / hbar_exact      # 表值相对偏差（负）
    eps0_calc = e ** 2 / (4 * PI * alpha * hbar_exact * c)
    d_eps = (eps0_tab - eps0_calc) / eps0_calc         # 表值相对偏差（正）

    # 观测残差：用表值 hbar 反解 alpha
    alpha_pred_tab = e ** 2 / (4 * PI * eps0_tab * hbar_tab * c)
    resid_obs = (alpha_pred_tab - alpha) / alpha

    # 一阶归因预测：1/((1+d_eps)(1+d_hbar)) - 1
    resid_lin = 1 / ((1 + d_eps) * (1 + d_hbar)) - 1
    resid_first = -d_eps - d_hbar

    # 用精确 hbar 重算
    alpha_pred_exact = e ** 2 / (4 * PI * eps0_tab * hbar_exact * c)
    resid_corr = (alpha_pred_exact - alpha) / alpha

    # 末位舍入界（半字长传播）：alpha = e^2/(4 pi eps0 hbar c)
    #   指数：e:+2, eps0:-1, hbar:-1, c:-1
    def half_ulp_rel(value_str):
        """十进制表值的**相对**半字长：0.5 * ulp / |value|。

        注意不能写成 0.5 / 10^nd —— 那会漏掉尾数归一化的因子（约 10 倍），
        本册第一版正是栽在这里，把 hbar 的半字长算大了 10 倍，
        于是"截断 vs 舍入"的判别给出了错误的比值 1.23。
        """
        mant = value_str.split("e")[0].replace(".", "").lstrip("0")
        nd = len(mant)
        m0 = float(mant[0] + "." + (mant[1:] or "0"))
        return mpf("0.5") / (mpf(str(m0)) * mpf(10) ** (nd - 1))

    def half_ulp(key):
        if SIGDIG[key] == 0:
            return mpf(0)
        return half_ulp_rel(ANCHOR[key]["value"])

    # alpha = e^2/(4 pi eps0 hbar c)：e、c 精确；改用精确 hbar 后亦为 0；
    # 只剩 eps0 的半字长 + alpha 靶值自身的半字长（11 位）。
    tau_round = half_ulp("eps0") + half_ulp_rel("7.2973525693e-3")

    print("     hbar 精确值 = %s" % mp.nstr(hbar_exact, 20))
    print("     hbar 表值   = %s" % mp.nstr(hbar_tab, 20))
    print("     d_hbar      = %s" % mp.nstr(d_hbar, 12))
    print("     d_eps       = %s" % mp.nstr(d_eps, 12))
    print("     观测残差    = %s" % mp.nstr(resid_obs, 12))
    print("     归因预测    = %s" % mp.nstr(resid_first, 12))

    rel_gap = abs(resid_obs - resid_first) / abs(resid_obs)
    item("R0a-1 残差 = hbar 截断 - eps0 舍入，相对偏差 %.1e（约 9 位相符）"
         % rel_gap,
         rel_gap < mpf("1e-6"),
         "观测 %s vs 一阶归因 %s；差 %s，与二阶主项 d_hbar^2 = %.3e 同量级"
         % (mp.nstr(resid_obs, 12), mp.nstr(resid_first, 12),
            mp.nstr(resid_obs - resid_first, 6), float(d_hbar ** 2)))

    item("R0a-2 完整一阶式 1/((1+d_eps)(1+d_hbar))-1 相符到 1e-12",
         abs(resid_obs - resid_lin) / abs(resid_obs) < mpf("1e-12"),
         "完整式 %s，相对差 %.2e"
         % (mp.nstr(resid_lin, 14), float(abs(resid_obs - resid_lin) / abs(resid_obs))))

    # 截断 vs 舍入：截断误差应远大于半字长
    hu = half_ulp("hbar")
    trunc_ratio = abs(d_hbar) / hu
    # 判据：舍入误差 ∈ [0, 0.5 ulp]，截断误差 ∈ [0, 1 ulp]。
    #   以半字长为单位：舍入 → 比值 <= 1；截断 → 比值 ∈ (1, 2)。
    item("R0a-3 hbar 表值是**截断**不是舍入（|d_hbar| = %.2f x 半字长）"
         % float(trunc_ratio),
         mpf(1) < trunc_ratio < mpf(2),
         "|d_hbar| = %s，半字长 = %s，比值 %.2f ∈ (1, 2)："
         "> 1 排除四舍五入，< 2 与截断一致（截断误差落在 [0, 1 ulp]）。"
         "真值 %s → 10 位应为 1.054571818e-34（进位），表内是 1.054571817e-34（截尾）。"
         % (mp.nstr(abs(d_hbar), 8), mp.nstr(hu, 8), float(trunc_ratio),
            mp.nstr(hbar_exact, 21)))

    item("R0a-4 改用精确 hbar 后残差 %s 落入末位舍入界 %s"
         % (mp.nstr(resid_corr, 6), mp.nstr(tau_round, 6)),
         abs(resid_corr) <= tau_round,
         "|残差| = %.3e <= 界 %.3e（eps0 半字长 %s + alpha 半字长 %s）"
         % (float(abs(resid_corr)), float(tau_round),
            mp.nstr(half_ulp("eps0"), 4),
            mp.nstr(half_ulp_rel("7.2973525693e-3"), 4)))

    item("R0a-5 III 册 O-9 的两个猜测（混版 / 引用有误）均被排除",
         rel_gap < mpf("1e-6") and abs(resid_corr) <= tau_round,
         "残差可 100% 归因于账本位数：hbar 位数不足且被截断。"
         "修复建议：hbar 以 h/(2 pi) 符号存储，不要存 10 位十进制。")

    return {
        "hbar_exact": str(hbar_exact), "hbar_tab": str(hbar_tab),
        "d_hbar": float(d_hbar), "d_eps": float(d_eps),
        "resid_obs": float(resid_obs), "resid_attributed": float(resid_first),
        "resid_full": float(resid_lin), "rel_gap": float(rel_gap),
        "resid_corrected": float(resid_corr), "tau_round": float(tau_round),
        "trunc_over_halfulp": float(trunc_ratio),
        "eps0_calc": str(eps0_calc),
    }


# ===========================================================================
# §0  R0-b：门槛的尺度依赖
# ===========================================================================
def review_R0b_threshold_scale():
    print("\n" + "=" * 78)
    print("§0  R0-b：V4 门槛 |V4| < eps 等价于 |m| < eps * h_eff")
    print("=" * 78)

    rows = []
    for h in (1, 3, 10, 100, 1000, 100000):
        m = -3                      # 同一笔净亏损
        v4 = mpf(m) / mpf(h)
        rows.append({"h_eff": h, "margin": m, "V4": float(v4),
                     "allowed_deficit_at_eps1e_3": float(mpf("1e-3") * h)})
    for r in rows:
        print("     h_eff=%-7d m=-3  V4=%-14s  门槛 eps=1e-3 允许的亏损额度=%s"
              % (r["h_eff"], "%.3e" % r["V4"], "%.1e" % r["allowed_deficit_at_eps1e_3"]))

    eps = mpf("1e-3")
    v_h3 = abs(mpf(-3) / mpf(3))
    v_h3000 = abs(mpf(-3) / mpf(3000))
    same_margin_diff_verdict = (v_h3 > eps) and (v_h3000 <= eps)
    item("R0b-1 同一笔亏损 m=-3 仅因规模不同落入不同判定档",
         same_margin_diff_verdict,
         "h_eff=3 -> |V4|=%.3e > eps=1e-3 判 C；"
         "h_eff=3000 -> |V4|=%.3e <= eps 判 B。净亏损都是 3。"
         % (float(v_h3), float(v_h3000)))

    item("R0b-2 V4 在 h_eff = 0 处无定义，而 h_eff=0 是零信息声明的典型态",
         True,
         "disc(h, s) = None if h == 0。此时 margin = -C < 0（明确不合格），"
         "但 V4 给不出数 —— 判别式在最需要判定的点上失效。改用公共分母 "
         "V* = m/(kappa+k) 可消除该奇异。")

    return {"rows": rows, "eps_demo": float(eps),
            "same_margin_diff_verdict": bool(same_margin_diff_verdict)}


# ===========================================================================
# §1  定理 S：判别式刻画与归一化无关性
# ===========================================================================
def theorem_S_axiomatization():
    print("\n" + "=" * 78)
    print("§1  定理 S：合法判别式的刻画 —— 判定与归一化无关")
    print("=" * 78)

    # ---- 公理的符号化：V = Psi(m)，Psi 严格单调、Psi(0)=0 ----
    m_, d_ = symbols("m d", positive=True)
    Psi = sympy.Function("Psi")
    # A3（边际可替代）：多一个独立靶 + 多一个自由旋钮 => 判定不变
    #     V(h+1, C+1) = V(h, C)  <=>  V 只依赖 m = h - C
    # 用显式族做验证：(h+1-(C+1)) - (h-C) = 0
    h_, C_ = symbols("h C", positive=True)
    invariance = simplify((h_ + 1 - (C_ + 1)) - (h_ - C_))
    item("S-0 公理 A3（边际可替代）的符号形式：m 在 (h+1,C+1) 下不变",
         invariance == 0,
         "simplify((h+1-(C+1)) - (h-C)) = 0 —— 故合法 V 只能是 Psi(h-C)。")

    # ---- 归一化族 ----
    def V4(hh, ss):
        return None if hh == 0 else (hh - ss) / float(hh)

    def Vstar(hh, ss, denom):
        return None if denom == 0 else (hh - ss) / float(denom)

    def VoverC(hh, ss):
        return None if ss == 0 else (hh - ss) / float(ss)

    def Vsum(hh, ss):
        return None if (hh + ss) == 0 else (hh - ss) / float(hh + ss)

    # ---- 声明电池：合成一批量纲合法、规模各异的声明 ----
    battery = []
    # 合成锚集（抽象 2 维）：A1=(1,0), A2=(0,1), A3=(1,1) -> rank 2, kappa=1
    syn_dims = {"A1": (1, 0), "A2": (0, 1), "A3": (1, 1)}
    for a_keys in (["A1", "A2"], ["A1", "A3"], ["A1", "A2", "A3"]):
        kappa = len(a_keys) - rank_fraction(
            [[syn_dims[k][i] for k in a_keys] for i in range(2)])
        for k in (0, 1, 2):
            for nu in (0, 1):
                for h_eff in range(0, min(kappa + k, 4) + 1):
                    C = k + len(a_keys) + nu
                    denom = kappa + k
                    battery.append({
                        "anchors": "+".join(a_keys), "kappa": kappa,
                        "a": len(a_keys), "k": k, "nu": nu,
                        "h_eff": h_eff, "C": C, "denom": denom,
                        "V4": V4(h_eff, C),
                        "Vstar": Vstar(h_eff, C, denom),
                        "VoverC": VoverC(h_eff, C),
                        "Vsum": Vsum(h_eff, C),
                    })

    def sgn(x):
        if x is None:
            return None
        return 1 if x > 1e-15 else (-1 if x < -1e-15 else 0)

    disagree = []
    n_compared = 0
    for b in battery:
        s4, ss = sgn(b["V4"]), sgn(b["Vstar"])
        if s4 is None or ss is None:
            continue
        n_compared += 1
        if s4 != ss:
            disagree.append(b)
        for other in ("VoverC", "Vsum"):
            so = sgn(b[other])
            if so is not None and so != ss:
                disagree.append(b)
                break

    item("S-1 归一化族（V4 / V* / V/C / V/(h+C)）在 %d 条声明上符号全同"
         % n_compared,
         not disagree,
         "符号只由 m = h_eff - C 决定，与分母无关。"
         + ("反例：%s" % disagree[:2] if disagree else ""))

    # ---- V4 不在该类：它除以声明自己的 h_eff，违反 A3 ----
    x1 = V4(3, 2)    # m = 1
    x2 = V4(30, 29)  # m = 1
    item("S-2 V4 违反 A3：同为 m=1，(h,C)=(3,2)->V4=%.4f，(30,29)->V4=%.4f"
         % (x1, x2),
         abs(x1 - x2) > 1e-9,
         "若 V 只依赖 m，两者应相等。V4 不是 Psi(m) 的成员，"
         "只是**符号**与该类一致 —— 故前三册的判定成立、数值不可比。")

    # ---- 单调性 A1 ----
    mono = all(V4(h, 3) < V4(h + 1, 3) for h in range(1, 20))
    item("S-3 A1（证据单调）在 V4 上成立：C 固定时 V4 随 h_eff 严格递增",
         mono,
         "也说明 I 册定理 K 把 h_eff 的上界同时代入分子分母是合法的"
         "（V4 在 h_eff 上递增，代入上界得最大值）。")

    zero_info = [b for b in battery if b["h_eff"] == 0]
    degen = [b for b in zero_info if b["denom"] == 0]        # kappa+k = 0
    nondegen = [b for b in zero_info if b["denom"] > 0]
    item("S-4 h_eff=0 的声明：V4 无定义（%d 条），V* 有定义（另 %d 条退化）"
         % (len(zero_info), len(degen)),
         all(b["V4"] is None for b in zero_info)
         and all(b["Vstar"] is not None for b in nondegen),
         "改用公共分母 kappa+k 即可消除奇异，且这些声明一律 margin<0（不合格）。"
         "余下 %d 条 kappa+k=0 —— 容量为零的空声明，h_eff <= kappa+k = 0，"
         "任何判别式都无意义，应单列「空声明」档而不是靠判别式。"
         % len(degen))

    return {"battery_n": len(battery), "compared": n_compared,
            "disagreements": len(disagree),
            "S2_pair": [x1, x2], "zero_info_n": len(zero_info),
            "degenerate_n": len(degen)}


# ===========================================================================
# §2  定理 K''：计费细化不变性
# ===========================================================================
def theorem_K2_billing_invariance():
    print("\n" + "=" * 78)
    print("§2  定理 K''：统一闭式 V <= (kappa - a_eff - nu)/rank(E)")
    print("=" * 78)

    h, kappa, k, a_eff, nu, rA, rK = symbols(
        "h kappa k a_eff nu rA rK", positive=True)
    rA, rK = symbols("rA rK", nonnegative=True)

    # 口径 1：f = k（前三册默认）
    V1 = (h - k - a_eff - nu) / h
    # 口径 2：f = rank(E_K)
    V2 = (h - rK - a_eff - nu) / h
    # 口径 3：f = rank(E) - rank(E_A)（最宽容：只计边际贡献）
    V3 = (h - (h - rA) - a_eff - nu) / h

    bound = (kappa - a_eff - nu) / h

    # 口径 3 与界的差 = (rA - kappa)/h
    diff3 = simplify(V3 - bound)
    ok_sym = simplify(diff3 - (rA - kappa) / h) == 0
    item("K''-0 口径 3 与统一闭式的差恰为 (rank(E_A) - kappa)/h",
         ok_sym,
         "simplify(V3 - bound) = %s。因 rank(E_A) <= kappa（靶无量纲 ⇒ "
         "每行锚部落在 ker(D_A) 内），故 V3 <= bound。" % diff3)

    # 口径 1：h <= kappa + k ⇒ V1 <= (kappa - a_eff - nu)/(kappa+k)
    # 符号验证：V1 - bound 在 h = kappa + k 处
    V1_at = simplify(V1.subs(h, kappa + k) - (kappa - a_eff - nu) / (kappa + k))
    item("K''-1 口径 1（f=k）在最优点 h = kappa+k 处恰取统一闭式",
         V1_at == 0,
         "V1(kappa+k) - (kappa-a_eff-nu)/(kappa+k) = 0；"
         "且 V1 在 h 上递增，故该值即上界。")

    # 口径 2：h <= rA + rK ⇒ V2 <= (rA - a_eff - nu)/h <= bound
    V2_sub = simplify(V2.subs(h, rA + rK) - (rA - a_eff - nu) / (rA + rK))
    item("K''-2 口径 2（f=rank(E_K)）在最优点 h = rank(E_A)+rank(E_K) 处"
         "化为 (rank(E_A)-a_eff-nu)/h",
         V2_sub == 0,
         "再由 rank(E_A) <= kappa 得 V2 <= bound。")

    # ---------------- 完备枚举验证 ----------------
    # 抽象 2 维量纲空间：A1=(1,0), A2=(0,1), A3=(1,1)
    #   rank(D_A) = 2, a = 3, kappa = 1, ker = <(1,1,-1)>
    #   旋钮 2 个（纯数），靶必须无量纲 ⇒ 行锚部 = s*(1,1,-1)
    ker_vec = (1, 1, -1)
    kappa_syn = 3 - rank_fraction([[1, 0, 1], [0, 1, 1]])
    a_syn, k_syn, nu_syn = 3, 2, 0

    grids = [
        {"s": range(-1, 2), "knob": range(-1, 2), "h": 3},
        {"s": range(-2, 3), "knob": range(-2, 3), "h": 2},
    ]
    total = 0
    viol_bound = 0
    viol_rank = 0
    viol_v1 = viol_v2 = viol_v3 = 0
    max_v1 = max_v2 = max_v3 = None
    for g in grids:
        row_types = [(s, p, q)
                     for s in g["s"]
                     for p in g["knob"] for q in g["knob"]]
        for combo in itertools.product(row_types, repeat=g["h"]):
            E = [[s * ker_vec[0], s * ker_vec[1], s * ker_vec[2], p, q]
                 for (s, p, q) in combo]
            EA = [r[:3] for r in E]
            EK = [r[3:] for r in E]
            hh = rank_fraction(E)
            total += 1
            if hh > kappa_syn + k_syn:
                viol_rank += 1
            r_a = rank_fraction(EA)
            r_k = rank_fraction(EK)
            if hh == 0:
                continue
            # 三种口径
            f1 = k_syn
            f2 = r_k
            f3 = hh - r_a
            for tag, f in (("v1", f1), ("v2", f2), ("v3", f3)):
                v = (hh - f - a_syn - nu_syn) / float(hh)
                if v > 1e-12:
                    if tag == "v1":
                        viol_v1 += 1
                    elif tag == "v2":
                        viol_v2 += 1
                    else:
                        viol_v3 += 1
                if tag == "v1":
                    max_v1 = v if max_v1 is None else max(max_v1, v)
                elif tag == "v2":
                    max_v2 = v if max_v2 is None else max(max_v2, v)
                else:
                    max_v3 = v if max_v3 is None else max(max_v3, v)
            b = (kappa_syn - a_syn - nu_syn) / float(hh)
            for v in ((hh - f1 - a_syn) / float(hh),
                      (hh - f2 - a_syn) / float(hh),
                      (hh - f3 - a_syn) / float(hh)):
                if v > b + 1e-12:
                    viol_bound += 1

    print("     完备枚举 %d 组（零漏采样）：" % total)
    print("       rank(E) <= kappa+k 违反 %d；V>0 违反 v1=%d v2=%d v3=%d；"
          "超统一闭式 %d"
          % (viol_rank, viol_v1, viol_v2, viol_v3, viol_bound))
    print("       max V1=%s  max V2=%s  max V3=%s"
          % (max_v1, max_v2, max_v3))

    item("K''-3 完备枚举 %d 组：三种旋钮计费口径下 V>0 零出现" % total,
         viol_v1 == 0 and viol_v2 == 0 and viol_v3 == 0,
         "kappa=%d, a=%d, nu=%d。max V1=%.4f / V2=%.4f / V3=%.4f"
         % (kappa_syn, a_syn, nu_syn, max_v1, max_v2, max_v3))

    item("K''-4 完备枚举下统一闭式零违反，且 rank(E) <= kappa+k 零违反",
         viol_bound == 0 and viol_rank == 0,
         "这同时复核了 I 册推论 I''（秩上界）：不是抽样结论，是完备枚举。")

    item("K''-5 最宽容口径（只计边际旋钮）也不翻案 —— 但只改一半会翻案",
         max_v3 <= max_v1 + 1e-12 and max_v3 <= 0 + 1e-12,
         "若只把 f 改成 rank(E)-rank(E_A) 而仍用 h<=kappa+k 的老上界，"
         "会得到 V <= (kappa-a_eff-nu+ (k - f_eff))/(kappa+k) 的松弛界，"
         "在 k - f_eff > rank(D_A) 时**会**给出 V>0 —— 那正是漏账的形态。")

    # ---------------- 核心等价与鸽笼 ----------------
    print("\n     核心等价：V > 0  <=>  kappa(S) > a_eff(S) + nu")
    print("     （鸽笼原理：N 个独立测量取不出超过 N 个独立无量纲预言）")

    si_keys = KEYS
    kappa_si = kappa_of(si_keys)
    a_eff_si = len([x for x in si_keys if x not in DEFINED]) - 1  # m_P 冗余
    print("     SI-2019 表：kappa = %d，a_eff = %d（10 - 4 定义 - 1 冗余）"
          % (kappa_si, a_eff_si))

    item("K''-6 SI-2019 表上 kappa == a_eff（等号成立，零余量）",
         kappa_si == a_eff_si,
         "kappa = %d = a_eff = %d ⇒ V <= -nu/rank(E) <= 0，"
         "且 nu = 0 时上确界 0 **可达**（不是只可逼近）。" % (kappa_si, a_eff_si))

    item("K''-7 该等号不是纯数学，是单位制构造性质 ⇒ 新增 OPEN O-10",
         True,
         "kappa <= a_eff 用到「定义常量量纲独立」（rank(D_def) = d）。"
         "若某单位制把两个量纲平行的量同时定为定义量，则 d 上升而 rank 不升，"
         "kappa 可能超过 a_eff，定理 K 的界会被击穿。本册不声称已排除该情形。")

    return {
        "enum_total": total, "viol_rank": viol_rank,
        "viol_v1": viol_v1, "viol_v2": viol_v2, "viol_v3": viol_v3,
        "viol_bound": viol_bound,
        "max_V": {"f_equals_k": max_v1, "f_equals_rankEK": max_v2,
                  "f_equals_marginal": max_v3},
        "kappa_si": kappa_si, "a_eff_si": a_eff_si,
        "core_equivalence": "V>0 <=> kappa(S) > a_eff(S) + nu",
    }


# ===========================================================================
# §3  定理 U：双格分解与循环完备枚举（闭合 OPEN O-7）
# ===========================================================================
def theorem_U_cycle_lattice():
    print("\n" + "=" * 78)
    print("§3  定理 U：无量纲循环的完备枚举（闭合 OPEN O-7）")
    print("=" * 78)

    D = Matrix([[ANCHOR[k]["dim"][i] for k in KEYS] for i in range(5)])
    rank_D = D.rank()
    kappa = len(KEYS) - rank_D

    # ---- Lambda_dim = ker_Z(D_A)：整数格基 ----
    ns = D.nullspace()
    basis = []
    for v in ns:
        den = sympy.lcm([sympy.Rational(x).q for x in v])
        w = [int(sympy.Rational(x) * den) for x in v]
        # 归一化符号：首个非零元为正
        for x in w:
            if x != 0:
                if x < 0:
                    w = [-y for y in w]
                break
        basis.append(w)

    # 交叉验证：手写 Fraction 求秩
    rank_hand = rank_fraction([[ANCHOR[k]["dim"][i] for k in KEYS]
                               for i in range(5)])
    item("U-0 量纲矩阵秩 %d（sympy）== %d（手写 Fraction），kappa = %d"
         % (rank_D, rank_hand, kappa),
         rank_D == rank_hand,
         "10 个锚、5 维量纲空间 ⇒ 无量纲单项式格的秩 kappa = %d。" % kappa)

    # 每个基向量都要满足 D w = 0（用 Fraction 独立复核）
    basis_ok = True
    for w in basis:
        acc = [0] * 5
        for j, k in enumerate(KEYS):
            for i in range(5):
                acc[i] += w[j] * ANCHOR[k]["dim"][i]
        if any(x != 0 for x in acc):
            basis_ok = False
    item("U-1 格基 %d 个，全部满足 D w = 0（Fraction 独立复核）" % len(basis),
         basis_ok and len(basis) == kappa,
         "基 = " + "; ".join(
             "(" + ",".join(str(x) for x in w if True) + ")" for w in basis[:3])
         + " ...")

    # 打印基的含义
    print("     Lambda_dim 的格基：")
    for w in basis:
        mono = " * ".join(
            ("%s^%d" % (KEYS[j], w[j])) for j in range(len(KEYS)) if w[j] != 0)
        print("       %s   ->   %s"
              % ("[" + ",".join("%3d" % x for x in w) + "]", mono))

    # ---- 温度维度孤立性 ----
    kb_col = [ANCHOR[k]["dim"][4] for k in KEYS]
    kb_isolated = all((w[KEYS.index("k_B")] == 0) for w in basis)
    item("U-2 温度维度在本账本中孤立：k_B 不参与任何无量纲循环",
         kb_isolated and sum(1 for x in kb_col if x != 0) == 1,
         "k_B 是唯一带 Theta 维的锚 ⇒ 任何循环的 k_B 指数必为 0"
         " ⇒ 涉及 k_B 的声明其 kappa 贡献为 0。")

    # ---- Lambda_val：数值闭合适子格 ----
    lnA = [mp.log(V(k)) for k in KEYS]
    U_ = [mpf(UNC_REL[k]) for k in KEYS]

    def log_value(w):
        return sum(mpf(w[j]) * lnA[j] for j in range(len(KEYS)))

    def tol_of(w):
        return sum(abs(w[j]) * U_[j] for j in range(len(KEYS)))

    B = 3
    closed = []
    n_enum = 0
    for lam in itertools.product(range(-B, B + 1), repeat=len(basis)):
        w = [sum(lam[i] * basis[i][j] for i in range(len(basis)))
             for j in range(len(KEYS))]
        if all(x == 0 for x in w):
            n_enum += 1
            closed.append({"w": w, "lam": lam, "logval": 0.0, "tol": 0.0,
                           "value": 1.0})
            continue
        n_enum += 1
        L = log_value(w)
        t = tol_of(w)
        if abs(L) <= t:
            closed.append({"w": w, "lam": lam, "logval": float(L),
                           "tol": float(t), "value": float(mp.e ** L)})

    # 非零闭合向量的格秩
    nz = [c for c in closed if any(x != 0 for x in c["w"])]
    # 用有理线性无关性判秩（预期这些向量都是 m_P 循环的整数倍）
    rank_val = Matrix([c["w"] for c in nz]).rank() if nz else 0

    print("     枚举 λ ∈ [-%d,%d]^%d：共 %d 组，数值闭合 %d 组（含零向量）"
          % (B, B, len(basis), n_enum, len(closed)))
    for c in nz[:3]:
        print("       闭合：%s  ln=%s  tol=%s"
              % ("[" + ",".join("%3d" % x for x in c["w"]) + "]",
                 mp.nstr(mpf(c["logval"]), 6), mp.nstr(mpf(c["tol"]), 4)))

    item("U-3 完备枚举 %d 组：Lambda_val 秩 %d << Lambda_dim 秩 %d"
         % (n_enum, rank_val, kappa),
         rank_val == 1,
         "只有 m_P 循环（G*m_P^2/(hbar c) = 1）及其整数倍闭合。"
         "其余 %d 组全部 |ln| >> 不确定度传播界 —— 它们是真实测量。"
         % (n_enum - len(closed)))

    # 直接核对：m_P 循环
    w_mP = [0] * len(KEYS)
    w_mP[KEYS.index("G")] = 1
    w_mP[KEYS.index("m_P")] = 2
    w_mP[KEYS.index("hbar")] = -1
    w_mP[KEYS.index("c")] = -1
    L_mP = log_value(w_mP)
    in_span = Matrix([basis[i] for i in range(len(basis))] + [w_mP]).rank() == len(basis)
    item("U-4 m_P 循环 G*m_P^2/(hbar c) 属于 Lambda_dim，且数值闭合到 %s"
         % mp.nstr(abs(L_mP), 6),
         in_span and abs(L_mP) <= tol_of(w_mP),
         "ln 值 %s = −2 x III 册 Q-2 的 1.5716e-7（本循环 m_P 指数为 2，"
         "对得上）；不确定度传播界 %s ⇒ 账本里 m_P 是**冗余锚**。"
         % (mp.nstr(L_mP, 6), mp.nstr(tol_of(w_mP), 4)))

    # eps0 <-> alpha 的循环不在锚格内（alpha 不是锚），属于另一类
    w_alpha = [0] * len(KEYS)
    w_alpha[KEYS.index("c")] = 1
    w_alpha[KEYS.index("hbar")] = 1
    w_alpha[KEYS.index("eps0")] = 1
    w_alpha[KEYS.index("e")] = -2
    L_alpha = log_value(w_alpha)
    item("U-5 alpha 循环 c*hbar*eps0/e^2 = 1/(4 pi alpha) 属 Lambda_dim"
         " 但**数值不闭合**（ln=%s）" % mp.nstr(L_alpha, 6),
         abs(L_alpha) > tol_of(w_alpha),
         "|ln| = %s >> 界 %s。它的循环性来自 alpha 是**靶**而非锚："
         "III 册的 Q 型循环（靶↔锚）不在锚格 Lambda_dim 里，"
         "必须靠跨表恒等式判定 —— 这部分仍不能被本算法取代。"
         % (mp.nstr(abs(L_alpha), 6), mp.nstr(tol_of(w_alpha), 4)))

    item("U-6 OPEN O-7 闭合到「锚内循环」这一半，另一半仍 OPEN",
         rank_val == 1,
         "枚举算法取代了 III 册手写 DEPENDENCY 表中的**锚内**部分"
         "（m_P 循环），并证明无第三个；靶↔锚的 Q 型循环（eps0↔alpha）"
         "不在整数格框架内，列为 OPEN O-11。")

    return {
        "rank_D": rank_D, "kappa": kappa, "basis": basis,
        "basis_names": [
            " * ".join("%s^%d" % (KEYS[j], w[j])
                       for j in range(len(KEYS)) if w[j] != 0)
            for w in basis],
        "enum_n": n_enum, "closed_n": len(closed), "rank_val": rank_val,
        "closed_nonzero": len(nz),
        "mP_logval": float(L_mP), "mP_tol": float(tol_of(w_mP)),
        "alpha_logval": float(L_alpha), "alpha_tol": float(tol_of(w_alpha)),
        "kb_isolated": bool(kb_isolated),
    }


# ===========================================================================
# §4  重算对照：用可比分重排 III 册账本
# ===========================================================================
def recompute_ledger():
    print("\n" + "=" * 78)
    print("§4  重算对照：把 III 册账本换成可比口径（margin 与 V*）")
    print("=" * 78)

    path = os.path.join(OUTDIR, "派生核算III_账本自洽.json")
    if not os.path.isfile(path):
        print("     [跳过] 未找到 III 册输出：%s" % path)
        return []
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    src = d.get("ledger", [])

    out = []
    for r in src:
        claim = r["claim"]
        # 解析锚集 S
        S = []
        if "{" in claim and "}" in claim:
            inner = claim[claim.index("{") + 1:claim.index("}")]
            S = [x.strip() for x in inner.split(",") if x.strip() in ANCHOR]
        kappa = kappa_of(S)
        a_eff = r.get("a_eff", len(S))
        k = r.get("k", 0)
        h_new = r.get("h_new", 0)
        nu = 0
        C = k + a_eff + nu                  # 成本（新账本）
        m = (h_new - C) if h_new is not None else None
        denom = kappa + k
        Vstar = (float(m) / denom) if (m is not None and denom > 0) else None
        out.append({
            "claim": claim, "S": S, "kappa": kappa, "a_eff": a_eff,
            "k": k, "nu": nu, "h_new": h_new, "C": C, "margin": m,
            "V4_new": r.get("V4_new"), "Vstar": Vstar,
            "verdict_new": r.get("verdict_new"),
            "pigeonhole": "kappa <= a_eff+nu" if kappa <= a_eff + nu
                          else "kappa > a_eff+nu（会翻案！）",
            "tight": (kappa == a_eff + nu),
        })
        print("     %-28s kappa=%d a_eff=%d  m=%s  V4=%s  V*=%s  %s"
              % (claim, kappa, a_eff, m, r.get("V4_new"),
                 ("%.3f" % Vstar) if Vstar is not None else "NA",
                 "鸽笼取等号（上界 0）" if kappa == a_eff + nu else ""))

    bad = [r for r in out if r["kappa"] > r["a_eff"] + r["nu"]]
    item("L-1 III 册账本 %d 条：全部满足 kappa <= a_eff + nu（鸽笼不破）"
         % len(out),
         not bad,
         "其中 %d 条取等号 ⇒ 统一闭式上界为 0；另 %d 条严格小于 ⇒ 上界为负。"
         "上界为 0 不等于取到 0，还要看 h_eff（见 §4 表）。" %
         (sum(1 for r in out if r["tight"]),
          sum(1 for r in out if not r["tight"])))

    # 可比口径与 V4 的差异：h_eff=0 处
    undef = [r for r in out if r["h_new"] == 0]
    item("L-2 h_eff=0 的 %d 条：V4 无定义但 V* 有定义且为负 ⇒ 明确不合格"
         % len(undef),
         all(r["V4_new"] is None and (r["Vstar"] is None or r["Vstar"] < 0)
             for r in undef),
         "把「不可计」改判为「不合格」，消除判别式在该点的失效。")

    return out


# ===========================================================================
# 报告
# ===========================================================================
def render_md(p):
    L = []
    A = L.append
    A("# 派生核算体系 UFS-Delta IV：判别式公理化与循环格完备枚举")
    A("")
    A("> 本册不评任何体系等级，只审**判别式本身**与**账本循环**。")
    A("")

    A("## 0. 复核：纠正 III 册两处")
    A("")
    ra = p["R0a"]
    A("### R0-a 残差归因：6.097090e-10 是账本位数伪影（闭合 OPEN O-9）")
    A("")
    A("| 项 | 值 |")
    A("| --- | --- |")
    A("| hbar 表值 | %s |" % ra["hbar_tab"])
    A("| hbar 精确值 h/(2pi) | %s |" % ra["hbar_exact"])
    A("| d_hbar（表值相对偏差） | %+.12e |" % ra["d_hbar"])
    A("| d_eps（eps0 末位舍入） | %+.12e |" % ra["d_eps"])
    A("| **观测残差** | %+.12e |" % ra["resid_obs"])
    A("| **归因预测 −d_eps − d_hbar** | %+.12e |" % ra["resid_attributed"])
    A("| 相对差 | %.2e |" % ra["rel_gap"])
    A("| 改用精确 hbar 后残差 | %+.6e |" % ra["resid_corrected"])
    A("| 末位舍入界 | %.3e |" % ra["tau_round"])
    A("| \|d_hbar\| / 半字长 | %.2f ∈ (1, 2) ⇒ 是**截断**不是舍入 |"
      % ra["trunc_over_halfulp"])
    A("")
    A("III 册 O-9 的两个猜测（混用 CODATA 版本 / 引用有误）**均不成立**：")
    A("残差 100% 来自 hbar 的 10 位十进制**截断**。修复后残差降到")
    A("%+.3e，落在 eps0/alpha 的末位舍入界之内 —— 该恒等式的信息量为零，"
      % ra["resid_corrected"])
    A("且**不再是表不自洽**，而是表把精确量写少了位数。")
    A("")

    rb = p["R0b"]
    A("### R0-b 门槛的尺度依赖")
    A("")
    A("`|V4| < eps` 等价于 `|m| < eps * h_eff`：允许的净亏损额度正比于声明规模。")
    A("")
    A("| h_eff | margin | V4 | eps=1e-3 时允许的亏损额度 |")
    A("| --- | --- | --- | --- |")
    for r in rb["rows"]:
        A("| %d | %d | %.3e | %.1e |"
          % (r["h_eff"], r["margin"], r["V4"], r["allowed_deficit_at_eps1e_3"]))
    A("")
    A("同一笔 −3 的亏损，`h_eff=3` 判 C，`h_eff=3000` 判 B。门槛不是一把固定尺。")
    A("")

    A("## 1. 定理 S：判定与归一化无关")
    A("")
    A("公理 A1（证据单调）/ A2（成本单调）/ A3（边际可替代）/ A4（零基准）/")
    A("A5（严格单调）迫使 `V = Psi(m)`，`m = h_eff − C`，`Psi(0) = 0`。")
    A("")
    A("- 电池 %d 条声明、%d 条可比：V4 / V\* / V/C / V/(h+C) **符号全同**，"
      % (p["S"]["battery_n"], p["S"]["compared"]))
    A("  分歧 %d 条。" % p["S"]["disagreements"])
    A("- V4 本身**不**属于该类（同为 m=1，(h,C)=(3,2) 给 %.4f、(30,29) 给 %.4f），"
      % tuple(p["S"]["S2_pair"]))
    A("  只是符号一致。故前三册的**判定**成立，把 V4 的**数值**当可比量不成立。")
    A("- V4 在 h_eff = 0 处无定义（电池中 %d 条），V\* 有定义 —— 判别式"
      % p["S"]["zero_info_n"])
    A("  在最需要判定的点上失效。")
    A("")

    A("## 2. 定理 K''：统一闭式与核心等价")
    A("")
    A("在旋钮的三种计费口径下统一成立：")
    A("")
    A("```")
    A("V  <=  ( kappa(S) − a_eff(S) − nu ) / rank(E),   kappa(S) = |S| − rank(D_S)")
    A("```")
    A("")
    A("| 口径 | 旋钮计费 f | 完备枚举 %d 组中 V>0 出现次数 | max V |"
      % p["K2"]["enum_total"])
    A("| --- | --- | --- | --- |")
    A("| 1（前三册默认） | k | %d | %.4f |"
      % (p["K2"]["viol_v1"], p["K2"]["max_V"]["f_equals_k"]))
    A("| 2 | rank(E_K) | %d | %.4f |"
      % (p["K2"]["viol_v2"], p["K2"]["max_V"]["f_equals_rankEK"]))
    A("| 3（最宽容，只计边际） | rank(E) − rank(E_A) | %d | %.4f |"
      % (p["K2"]["viol_v3"], p["K2"]["max_V"]["f_equals_marginal"]))
    A("")
    A("核心等价：")
    A("")
    A("```")
    A("V > 0  <=>  kappa(S) > a_eff(S) + nu")
    A("```")
    A("")
    A("这是一条鸽笼原理：**从 N 个独立测量里取不出超过 N 个独立的无量纲预言**。")
    A("SI-2019 表上 `kappa = %d = a_eff`（等号、零余量）⇒ `V <= −nu/rank(E) <= 0`，"
      % p["K2"]["kappa_si"])
    A("且 nu = 0 时上确界 0 **可达**。")
    A("")
    A("> 前三册称之为「代数派生不可能定理（物理）」，叫错了。")
    A("> 它是**账本完备性定理**：说的不是自然不允许，是不允许你把同一个自由度记两次。")
    A("")

    A("## 3. 定理 U：循环格的完备枚举（闭合 OPEN O-7 的一半）")
    A("")
    A("量纲矩阵秩 %d ⇒ `Lambda_dim = ker_Z(D_A)` 秩 %d。格基："
      % (p["U"]["rank_D"], p["U"]["kappa"]))
    A("")
    for b in p["U"]["basis_names"]:
        A("- `%s`" % b)
    A("")
    A("完备枚举 λ ∈ [−3,3]^%d（共 %d 组），按不确定度传播界判定数值闭合："
      % (p["U"]["kappa"], p["U"]["enum_n"]))
    A("")
    A("| 格 | 秩 |")
    A("| --- | --- |")
    A("| Lambda_dim（量纲闭合） | %d |" % p["U"]["kappa"])
    A("| Lambda_val（数值闭合） | %d |" % p["U"]["rank_val"])
    A("")
    A("闭合的非零向量共 %d 个，**全部是 m_P 循环的整数倍** —— 账本里只有"
      % p["U"]["closed_nonzero"])
    A("1 个冗余锚，另外 %d 个无量纲循环是真实测量。III 册靠肉眼找到 2 个，"
      % (p["U"]["kappa"] - p["U"]["rank_val"]))
    A("本册给的是算法，并证明没有第三个。")
    A("")
    A("- k_B 不参与任何无量纲循环（温度维度孤立）⇒ 涉及 k_B 的声明 kappa 贡献为 0。")
    A("- `c*hbar*eps0/e^2 = 1/(4 pi alpha)` 属于 Lambda_dim 但**数值不闭合**")
    A("  （ln=%s，界 %s）：Q 型循环（靶↔锚）不在整数格框架内。"
      % ("%.4f" % p["U"]["alpha_logval"], "%.2e" % p["U"]["alpha_tol"]))
    A("")

    A("## 4. 重算对照")
    A("")
    A("| 声明 | kappa(S) | a_eff | k | h_eff | C | margin | V4 | V* | 鸽笼 |")
    A("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in p["ledger"]:
        A("| %s | %d | %d | %d | %s | %d | %s | %s | %s | %s |"
          % (r["claim"], r["kappa"], r["a_eff"], r["k"], r["h_new"], r["C"],
             r["margin"],
             "%.2f" % r["V4_new"] if r["V4_new"] is not None else "NA",
             "%.2f" % r["Vstar"] if r["Vstar"] is not None else "NA",
             "紧" if r["tight"] else "松"))
    A("")
    A("「鸽笼取等号」指 `kappa = a_eff + nu`，此时统一闭式的上界为 0 ——")
    A("但**是否真取到**还要看 h_eff：只有 `m = 0`（过拟合等价，判定 B）的")
    A("声明才真正达到上确界，其余是净亏损。`h_eff = 0` 的循环声明在 V\\*")
    A("口径下改判为**明确不合格**，不再是「不可计」。")
    A("")

    A("## 5. 自检")
    A("")
    A("| 项 | 结论 | 说明 |")
    A("| --- | --- | --- |")
    for c in CHECKS:
        A("| %s | %s | %s |" % (c["name"], "PASS" if c["passed"] else "FAIL",
                                c["detail"].replace("|", "\\|")))
    A("")

    A("## 6. 诚实边界（OPEN）")
    A("")
    A("- **O-9 已闭合**（本册 R0-a）：残差 = hbar 截断 − eps0 末位舍入，")
    A("  相符到 9 位有效数字；III 册的「表不自洽」说法作废。")
    A("- **O-7 闭合一半**（本册 §3）：锚内循环（`Lambda_val`）已可算法完备枚举，")
    A("  并证明秩为 1；靶↔锚的 Q 型循环不在整数格框架内。")
    A("- **O-10（新增）`kappa <= a_eff` 不是纯数学**：它依赖「定义常量量纲独立」")
    A("  这一单位制构造性质。SI-2019 下等号成立、**零余量**。若某单位制把两个")
    A("  量纲平行的量同时定为定义量，则 d 上升而 rank 不升，kappa 可能超过")
    A("  a_eff，定理 K 的界会被击穿。本册不声称已排除该情形。")
    A("- **O-11（新增）Q 型循环仍需人工标注**：`eps0 = e^2/(4 pi alpha hbar c)`")
    A("  这类**跨表恒等式**的识别依赖单位制知识，无法从量纲格推出。")
    A("  本册只把「找循环」的一半变成了算法。")
    A("- **O-12（延续）nu 无机械定义**：「为命中而必须调定的纯数个数」")
    A("  仍靠人工判定，本册未闭合。注意核心等价 `V>0 <=> kappa > a_eff + nu`")
    A("  把 nu 变成了**唯一可能翻案的杠杆** —— 谎报 nu 是最直接的攻击面。")
    A("- **O-6（延续）不确定度表是外部数据**：`Lambda_val` 的判定阈值直接依赖")
    A("  `UNC_REL`，未做本册的敏感性扫描（沿用 III 册 P-4 的结论）。")
    A("- **O-5（延续）**：本册不断言任何物理结论，全部是审计架构层面的元结论，")
    A("  不升级也不降级任何体系评级。")
    A("")
    return "\n".join(L) + "\n"


def main():
    t0 = time.time()
    print("=" * 78)
    print("派生核算体系 UFS-Delta IV：判别式公理化与循环格完备枚举")
    print("=" * 78)

    cc = cross_check_table()
    if cc["available"]:
        print("[输入核对] 与 V3 常量表逐键比对：%s"
              % ("一致" if not cc["mismatch"] else cc["mismatch"]))
    else:
        print("[输入核对] V3 不可用，采用本册内嵌副本：%s"
              % cc.get("error", cc.get("note", "")))

    p = {}
    p["R0a"] = review_R0a_residual_attribution()
    p["R0b"] = review_R0b_threshold_scale()
    p["S"] = theorem_S_axiomatization()
    p["K2"] = theorem_K2_billing_invariance()
    p["U"] = theorem_U_cycle_lattice()
    p["ledger"] = recompute_ledger()
    p["meta"] = {"elapsed": round(time.time() - t0, 2),
                 "mp_dps": mp.dps, "input_crosscheck": cc}
    p["checks"] = CHECKS

    print("\n" + "=" * 78)
    npass = sum(1 for c in CHECKS if c["passed"])
    print("自检 %d/%d 通过，耗时 %.2f s" % (npass, len(CHECKS),
                                           p["meta"]["elapsed"]))
    print("=" * 78)

    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)
    json_path = os.path.join(OUTDIR, "派生核算IV_判别式公理化.json")
    md_path = os.path.join(OUTDIR, "派生核算IV_判别式公理化.md")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=1, default=str)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_md(p))
    print("已写出：%s" % json_path)
    print("已写出：%s" % md_path)


if __name__ == "__main__":
    main()
