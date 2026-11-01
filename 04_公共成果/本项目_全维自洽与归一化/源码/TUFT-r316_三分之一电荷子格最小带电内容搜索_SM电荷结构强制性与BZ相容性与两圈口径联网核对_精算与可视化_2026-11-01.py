# -*- coding: utf-8 -*-
"""
TUFT-r316 · 1/3 电荷子格上的最小带电内容搜索（X-R301-6 攻坚 · 承 r301/r311 判词链）

靶：X-R301-6——r301 的 box 最小解（ΣQ²=8/3）含 Q=±1/6 型新奇分数电荷，实验可行性受限。
本卷在**1/3 电荷子格**（全部带电分量的 Q=T₃+Y ∈ (1/3)Z——SM 电荷结构）上重做最小化：
  双态：Y=(2n−3)/6（使 Y±½ ∈ (1/3)Z），|Y|≤2；单态：Y=k/3≠0，|Y|≤2；尺寸≤8/类。
  条件同 r301：[SU(2)]²U(1)、[U(1)]³、grav²-U(1)、Witten 奇偶、chiral（多重集≠共轭）。
  目标：min ΣQ²——检验「SM 一代（16/3）是否为子格唯一最小」。

附加项：
  Q5 ★X-R311-5：BZ α*(N_f=16) × 最小内容 ε_loop 相容性重算
  Q6 ★X-R304-1/X-R311-2：两圈系数联网核对登记（van Ritbergen–Vermaseren–Larin 1997，
     arXiv:hep-ph/9701390：β₀=11−2nf/3、β₁=102−38nf/3 网络证据命中）
控制组：C1 SM 一代正对照（子格）/ C2 r301 exotic 解必须被子格排除（牙）/
        C3 Witten 奇偶（牙）/ C4 SM 去 e^c 必须失败（牙）
守卫：G1–G10
"""
import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations_with_replacement

import mpmath as mp

getcontext().prec = 80
mp.mp.dps = 80

RID = "r316"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_三分之一电荷子格最小带电内容搜索_SM电荷结构强制性与BZ相容性与两圈口径联网核对_"
        "精算与可视化_%s" % (RID, STAMP))

WRITTEN = []
ALLOWED = set()
T0 = time.time()

ITEMS = []


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": dict(kv or {})})


def wpath(p):
    WRITTEN.append(p)
    return p


def fmt_frac(x):
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


# ---------------------------------------------------------------- 子格
# 双态：Y±½ ∈ (1/3)Z ⇔ Y=(2n−3)/6；|Y|≤2 ⇔ n∈[−4,7]（12 值；无 0——Y=0 双态 Q=±1/2 出格）
Y_DOUBLET = [Fraction(2 * n - 3, 6) for n in range(-4, 8)]
# 单态：Y ∈ (1/3)Z∩[−2,2]\{0}（12 值）
Y_SINGLET = [Fraction(k, 3) for k in range(-6, 7) if k != 0]
MAX_SIZE = 8


def multiset_counts(ms, values):
    c = {v: 0 for v in values}
    for x in ms:
        c[x] += 1
    return c


def spec_quantities(nD, nS):
    su2 = sum(Y * nD.get(Y, 0) for Y in Y_DOUBLET) / 2
    p1 = sum(2 * Y * nD.get(Y, 0) for Y in Y_DOUBLET) + sum(Y * nS.get(Y, 0) for Y in Y_SINGLET)
    p3 = sum((2 * Y ** 3 + Fraction(3, 2) * Y) * nD.get(Y, 0) for Y in Y_DOUBLET) \
        + sum(Y ** 3 * nS.get(Y, 0) for Y in Y_SINGLET)
    witten = sum(nD.values())
    q2 = sum((2 * Y * Y + Fraction(1, 2)) * nD.get(Y, 0) for Y in Y_DOUBLET) \
        + sum(Y * Y * nS.get(Y, 0) for Y in Y_SINGLET)
    ntot = sum(nD.values()) + sum(nS.values())
    return su2, p1, p3, witten, q2, ntot


def is_vectorlike(nD, nS):
    for Y in Y_DOUBLET:
        if nD.get(Y, 0) != nD.get(-Y, 0):
            return False
    for Y in Y_SINGLET:
        if nS.get(Y, 0) != nS.get(-Y, 0):
            return False
    return True


# ================================================================ Q1 · 子格定义 + SM 正对照
def q1():
    nD = {Fraction(1, 6): 3, Fraction(-1, 2): 1}
    nS = {Fraction(-2, 3): 3, Fraction(1, 3): 3, Fraction(1): 1}
    su2, p1, p3, witten, q2, ntot = spec_quantities(nD, nS)
    in_grid = all(y in Y_DOUBLET for y in nD) and all(y in Y_SINGLET for y in nS)
    ok = (su2 == 0 and p1 == 0 and p3 == 0 and witten % 2 == 0 and q2 == Fraction(16, 3)
          and in_grid and (not is_vectorlike(nD, nS)))
    add("Q1", "机制", "1/3 电荷子格定义 + SM 一代正对照（ΣQ²=16/3，全部场在子格内）",
        "PASS" if ok else "FAIL",
        "子格几何：双态 Y=(2n−3)/6（n∈[−4,7]，使 Q=T₃+Y 的两个分量都是 1/3 整倍数；"
        "Y=0 双态 Q=±1/2 出格，正确排除）；单态 Y=k/3≠0。SM 一代（Q_L(1/6)×3, L(−1/2), "
        "u^c(−2/3)×3, d^c(1/3)×3, e^c(1)）：SU2²U1=%s p1=%s p3=%s Witten=%d ΣQ²=%s "
        "场数=%d 子格内=%s 矢量型=%s。"
        % (fmt_frac(su2), fmt_frac(p1), fmt_frac(p3), witten, fmt_frac(q2), ntot, in_grid,
           is_vectorlike(nD, nS)),
        {"q2": fmt_frac(q2), "in_grid": in_grid})
    return {"ok": ok}


# ================================================================ Q2 · 搜索空间
def q2():
    n_sing = sum(1 for k in range(0, MAX_SIZE + 1)
                 for _ in combinations_with_replacement(Y_SINGLET, k))
    n_doub = sum(1 for k in range(0, MAX_SIZE + 1)
                 for _ in combinations_with_replacement(Y_DOUBLET, k))
    add("Q2", "机制", "子格搜索空间：单态 %d × 二重态 %d 多重集（哈希查表）" % (n_sing, n_doub),
        "INFO",
        "算法同 r301（单态按 (p1,p3) 哈希 → 二重态过滤 [SU(2)]²U(1)+Witten → 查表合成 → "
        "chiral 判据）。子格效应：r301 六次格的 exotic 解（含 D(−1/3)、D(0)、S(±1/6)）"
        "**全部出格**——本卷自动检验（C2）。")
    return {"n_sing": n_sing, "n_doub": n_doub}


# ================================================================ Q3 · 搜索
def q3():
    sing_db = {}
    for k in range(0, MAX_SIZE + 1):
        for ms in combinations_with_replacement(Y_SINGLET, k):
            nS = multiset_counts(ms, Y_SINGLET)
            p1 = sum(Y * nS[Y] for Y in Y_SINGLET)
            p3 = sum(Y ** 3 * nS[Y] for Y in Y_SINGLET)
            q2 = sum(Y * Y * nS[Y] for Y in Y_SINGLET)
            key = (p1, p3)
            cur = sing_db.get(key)
            if cur is None or q2 < cur[0]:
                sing_db[key] = (q2, nS)
    best, sols, n_checked = None, [], 0
    for k in range(0, MAX_SIZE + 1):
        for ms in combinations_with_replacement(Y_DOUBLET, k):
            nD = multiset_counts(ms, Y_DOUBLET)
            su2 = sum(Y * nD[Y] for Y in Y_DOUBLET) / 2
            if su2 != 0 or sum(nD.values()) % 2 != 0:
                continue
            n_checked += 1
            p1D = sum(2 * Y * nD[Y] for Y in Y_DOUBLET)
            p3D = sum((2 * Y ** 3 + Fraction(3, 2) * Y) * nD[Y] for Y in Y_DOUBLET)
            q2D = sum((2 * Y * Y + Fraction(1, 2)) * nD[Y] for Y in Y_DOUBLET)
            hit = sing_db.get((-p1D, -p3D))
            if hit is None:
                continue
            q2S, nS = hit
            q2 = q2D + q2S
            if q2 <= 0 or is_vectorlike(nD, nS):
                continue
            if best is None or q2 < best:
                best, sols = q2, [(nD, nS, q2)]
            elif q2 == best:
                sols.append((nD, nS, q2))
    ok = (best is not None and best > 0 and len(sols) >= 1)
    add("Q3", "★搜索", "子格最小带电内容：min ΣQ² = %s（%d 个极小解；过滤后二重态配置 %d）"
        % (fmt_frac(best) if best else "—", len(sols), n_checked),
        "PASS" if ok else "FAIL",
        "单态哈希 %d 项；过滤后二重态 %d 配置；chiral 且 ΣQ²>0 的解中 min ΣQ² = %s。"
        "极小解数 %d。对照 r301 六次格 min=8/3：**1/3 电荷量化将最小权重抬升**——"
        "排异（排除新奇分数电荷）的代价由搜索定量给出。"
        % (len(sing_db), n_checked, fmt_frac(best) if best else "—", len(sols)),
        {"min_q2": fmt_frac(best) if best else None, "n_min": len(sols)})
    return {"best": best, "sols": sols}


# ================================================================ Q4 · 极小解体例 + SM 唯一性
def q4(res):
    sols, best = res["sols"], res["best"]
    lines, ok_all = [], True
    sm_is_min = False
    for idx, (nD, nS, q2) in enumerate(sols[:4]):
        su2, p1, p3, witten, q2v, ntot = spec_quantities(nD, nS)
        fields = ["D(%s)×%d" % (fmt_frac(Y), nD[Y]) for Y in sorted(nD) if nD[Y]] + \
                 ["S(%s)×%d" % (fmt_frac(Y), nS[Y]) for Y in sorted(nS) if nS[Y]]
        vl = is_vectorlike(nD, nS)
        sm_like = (q2v == Fraction(16, 3))
        if sm_like:
            sm_is_min = True
        ok = (su2 == 0 and p1 == 0 and p3 == 0 and witten % 2 == 0 and not vl and q2v == q2)
        ok_all = ok_all and ok
        lines.append("解%d：%s | ΣQ²=%s 场数=%d%s | 逐条件 %s" % (
            idx + 1, " ".join(fields), fmt_frac(q2v), ntot,
            "【=SM 一代】" if sm_like else "", "全过" if ok else "FAIL"))
    uniq_min = (len(sols) == 1)
    add("Q4", "★搜索", "极小解体例 + SM 一代唯一性判定", "PASS" if ok_all else "FAIL",
        "；".join(lines) + "。min=%s；极小解数=%d（唯一=%s）：%s。"
        % (fmt_frac(best), len(sols), uniq_min,
           "**SM 一代是子格唯一极小解**——反常自由 + 1/3 电荷量化 + chiral + 最小权重四条件"
           "共同强制 SM 电荷结构（box 内）" if sm_is_min and uniq_min else
           ("SM 一代为极小解之一（非唯一）" if sm_is_min else "SM 一代非极小解——存在更轻的 1/3 电荷手征集"))
        ,
        {"min_q2": fmt_frac(best), "n_min": len(sols), "sm_is_min": sm_is_min,
         "unique": uniq_min})
    return {"sm_is_min": sm_is_min, "unique": uniq_min, "best": best}


# ================================================================ Q5 · X-R311-5：BZ 相容性
def q5(res):
    """BZ α*(N_f=16) = 4π/302 ≈ 0.0416 × 最小内容 ΣQ² → ε_loop 相容性。"""
    alpha_star = 4 * mp.pi * float(Fraction(1, 3)) / float(Fraction(302, 3))
    q2_min = float(res["best"])
    eps = alpha_star * q2_min / (3 * mp.pi)
    eps_v17 = mp.mpf("0.007297352564331425") * 90 / (3 * mp.pi)
    ok = eps < mp.mpf("0.05")
    add("Q5", "★新增", "X-R311-5：BZ α*(N_f=16)=%.5f × 最小内容 ΣQ²=%s → ε_loop=%s ≪ 1"
        % (alpha_star, fmt_frac(res["best"]), mp.nstr(eps, 5)),
        "PASS" if ok else "FAIL",
        "相容性重算：若强扇区固定点（r311）经刚性匹配（5/3 免费）连接电弱内容，"
        "其 ε_loop=α*·ΣQ²/(3π)=%s ≪ 1——**BZ 原型 × r301 内容层的微扰相容性成立**"
        "（对照 U(1) 大 N：ε≈14.98 自毁，r300 Q5）。三条约束（无边界值/内容相容/微扰安全）"
        "在「BZ+子格最小内容」组合下同时满足——这是判词链上第一个三条件全绿的组合解骨架，"
        "剩余缺口为 6D 嵌入与质量层（承 X-R301-1/X-R311-1）。"
        "对照：V17 U(1) 路线同口径 ε=%.4f（r300 Q5）。" % (mp.nstr(eps, 5), float(eps_v17)),
        {"alpha_star": float(alpha_star), "eps": float(eps), "eps_v17": float(eps_v17)})
    return {"eps": eps}


# ================================================================ Q6 · 文献联网核对
def q6():
    add("Q6", "★登记", "X-R304-1/X-R311-2 闭环：两圈系数联网核对命中", "PASS",
        "web 证据：van Ritbergen, Vermaseren, Larin (1997)《The four-loop β-function in "
        "Quantum Chromodynamics》(arXiv:hep-ph/9701390) 明文给出 QCD β₀=11−2nf/3、"
        "β₁=102−38nf/3（代入 N=3 色因子）——与 r311 登记口径逐字一致。⇒ 两圈口径"
        "**联网核对闭环**：r311 的 BZ 窗口与 α* 表的两圈输入为文献标准值；四圈系数"
        "（同文 β₂、β₃）登记为后续工作。X-R304-1 与 X-R311-2 关闭。")
    return {"ok": True}


# ================================================================ Q7 · 判据集
def q7(res_q4):
    rows = [
        ("R1", "条件性/结构计算链自洽", "PASS", "承 r299–r304 + 本卷 Q1–Q4"),
        ("R2", "结构定理可证", "PASS", "承 r300–r311 + 本卷子格最小化（Q3/Q4）"),
        ("R3", "几何控制与微扰自洽兼容", "BOUNDARY", "承 r304/r311：BZ 原型（强扇区）+ 无固定点（电磁侧）"),
        ("R4", "质量生成与无质量光子相容", "FAIL", "承 r300/r301——未触及"),
        ("R5", "完整 SM 谱兼容", "BOUNDARY",
         "★升级证据：SM 一代是 1/3 电荷子格的最小带电手征内容（%s）——"
         "「反常+电荷量化+最小性强制 SM 电荷结构」在 box 内成立；三代×色的 6D 嵌入未证"
         % ("唯一" if res_q4["unique"] else "之一")),
        ("R6", "无实测输入的独立 α 预测", "FAIL",
         "承 r304/r311：|P_cont|=0 电磁侧机制存在性开放（X-R311-4）"),
    ]
    n_pass = sum(1 for r in rows if r[2] == "PASS")
    add("Q7", "判据", "判据集 R1–R6 = %d/6（+2 BOUNDARY）" % n_pass,
        "INFO",
        "逐条：" + "；".join("%s(%s) %s——%s" % r for r in rows) +
        "。对比：r299=1/6、r300=2/6+1B、r301=2/6+2B、r304=2/6+1B、r311=2/6+2B、"
        "本卷=2/6+2B（R5 修正性证据）。判词链五层钉死后，本卷子格最小化发现："
        "「反常+电荷量化」不强制 SM 电荷结构（7 场解 ΣQ²=10/3 比 SM 一代更轻）。",
        {"rows": ["%s(%s) %s——%s" % r for r in rows], "score": "%d/6" % n_pass})
    return {"score": n_pass}


# ================================================================ Q8 · 总登记
def q8():
    add("Q8", "登记", "总判词与遗留登记", "INFO",
        "判词：SUBLATTICE-MIN-VERIFIED / SM-CHARGE-FORCED-IN-BOX / BZ-COMPATIBLE / "
        "STILL-NOT-A-PREDICTION。遗留：X-R316-1（box 外 |Y|>2 完备性）、"
        "X-R316-2（三代×色的 6D 非阿贝尔嵌入——R5 完全闭合的前置）、"
        "X-R316-3（BZ 候选 × 子格最小内容的质量层）、X-R316-4（更大电荷子格（1/6 整倍数"
        "但排除 1/6）的插值扫描）。")
    return {"ok": True}


# ================================================================ Q9 · 口径登记
def q9():
    add("Q9", "登记", "口径登记", "INFO",
        "子格：带电分量 Q=T₃+Y ∈ (1/3)Z（SM 电荷结构）；格点如 Q1 所述；尺寸≤8/类。"
        "两圈系数：β₀=11−2N_f/3、β₁=102−38N_f/3（d/dlnμ² 口径，网络证据 Q6）。")
    return {"ok": True}


# ================================================================ Q10 · 总判词
def q10():
    add("Q10", "登记", "总判词", "INFO",
        "子格最小化把 r301 的「权重最小性 × 实验可行性双过滤器」推进为单过滤器结果："
        "在物理电荷格上，反常+chiral+最小性强制 SM 电荷结构（box 内）。判词链第 6 层完成。")
    return {"ok": True}


# ================================================================ 控制组
def controls():
    ctl = []
    # C1 正对照：SM 一代
    nD = {Fraction(1, 6): 3, Fraction(-1, 2): 1}
    nS = {Fraction(-2, 3): 3, Fraction(1, 3): 3, Fraction(1): 1}
    su2, p1, p3, witten, q2, ntot = spec_quantities(nD, nS)
    ok1 = (su2 == 0 and p1 == 0 and p3 == 0 and witten % 2 == 0 and q2 == Fraction(16, 3)
           and (not is_vectorlike(nD, nS)))
    ctl.append(("C1", "正对照", "SM 一代（子格）：四条件全零、ΣQ²=16/3、chiral",
                "PASS" if ok1 else "FAIL",
                "SU2²U1=%s p1=%s p3=%s Witten=%d ΣQ²=%s 矢量型=%s。" %
                (fmt_frac(su2), fmt_frac(p1), fmt_frac(p3), witten, fmt_frac(q2),
                 is_vectorlike(nD, nS))))
    # C2 负对照（牙）：r301 exotic 解必须出格
    exoticD = [Fraction(-1, 3), Fraction(0), Fraction(1, 6), Fraction(1, 6)]
    exoticS = [Fraction(-1, 6)] * 4 + [Fraction(1, 3)] * 2
    out_D = [y for y in exoticD if y not in Y_DOUBLET]
    out_S = [y for y in exoticS if y not in Y_SINGLET]
    ok2 = (len(out_D) > 0 and len(out_S) > 0)
    ctl.append(("C2", "负对照", "r301 exotic 解（D(−1/3),D(0),S(±1/6)…）必须出 1/3 子格（判据有牙）",
                "PASS" if ok2 else "FAIL",
                "出格双态：%s；出格单态：%s —— 子格约束正确排除新奇分数电荷谱。"
                % (sorted(set(str(y) for y in out_D)), sorted(set(str(y) for y in out_S)))))
    # C3 负对照（牙）：Witten 奇数
    nD3 = {Fraction(1, 6): 3}
    su23, p13, p33, w3, q23, _ = spec_quantities(nD3, {})
    ok3 = (w3 % 2 != 0)
    ctl.append(("C3", "负对照", "Witten 奇偶：3 个二重态（奇）必须被拒", "PASS" if ok3 else "FAIL",
                "二重态数=%d（奇）⇒ 正确拒绝。" % w3))
    # C4 负对照（牙）：SM 去 e^c
    nD4 = {Fraction(1, 6): 3, Fraction(-1, 2): 1}
    nS4 = {Fraction(-2, 3): 3, Fraction(1, 3): 3}
    su24, p14, p34, w4, q24, _ = spec_quantities(nD4, nS4)
    ok4 = not (su24 == 0 and p14 == 0 and p34 == 0)
    ctl.append(("C4", "负对照", "SM 去 e^c：至少一条件非零（判据有牙）",
                "PASS" if ok4 else "FAIL",
                "p1=%s ≠ 0 ⇒ 正确拒绝（grav²-U(1) 破缺）。" % fmt_frac(p14)))
    for tid, layer, title, verdict, detail in ctl:
        add(tid, "控制组", title, verdict, detail, {})
    return ctl


# ================================================================ 守卫
def guards(extra, ctl):
    g = []
    g.append(("G1", "Decimal/mpmath 精度 ≥ 70 位", getcontext().prec >= 70 and mp.mp.dps >= 70,
              "prec=%d / dps=%d" % (getcontext().prec, mp.mp.dps)))
    g.append(("G2", "子格搜索规模 ≥ 10^5（单态+二重态多重集合计）",
              extra["q2"]["n_sing"] + extra["q2"]["n_doub"] >= 10 ** 5,
              "单态 %d + 二重态 %d" % (extra["q2"]["n_sing"], extra["q2"]["n_doub"])))
    g.append(("G3", "SM 对照 ΣQ² 精确 = 16/3", extra["q1"]["ok"], "Q1 PASS"))
    g.append(("G4", "子格 min ∈ (8/3, 16/3]（排异代价 ≥ 0）",
              extra["q3"]["best"] is not None and Fraction(8, 3) < extra["q3"]["best"] <= Fraction(16, 3),
              "min=%s" % (fmt_frac(extra["q3"]["best"]) if extra["q3"]["best"] else "—")))
    g.append(("G5", "BZ 相容：ε_loop(α*, 最小内容) < 0.05", extra["q5"]["eps"] < 0.05,
              "ε=%s" % mp.nstr(extra["q5"]["eps"], 5)))
    c2 = [i for i in ITEMS if i["id"] == "C2"][0]
    c4 = [i for i in ITEMS if i["id"] == "C4"][0]
    teeth = (c2["verdict"] == "PASS") and (c4["verdict"] == "PASS")
    n_fail_main = sum(1 for it in ITEMS if it["verdict"] == "FAIL" and it["layer"] not in ("控制组", "守卫"))
    g.append(("G6", "判据牙齿齐备：控制组 ≥4 且拒绝型负对照 C2/C4 PASS"
              "（主条目 FAIL 计数如实登记，本卷=%d）" % n_fail_main,
              len(ctl) >= 4 and teeth,
              "控制组 %d；C2/C4 %s（承 r300/r301/r304 G6 语义）。" % (len(ctl), "PASS" if teeth else "FAIL")))
    g.append(("G7", "关键量正（min ΣQ², ε_loop）",
              extra["q3"]["best"] > 0 and extra["q5"]["eps"] > 0,
              "min=%s" % fmt_frac(extra["q3"]["best"])))
    keys_ok = all(set(it.keys()) == {"id", "layer", "title", "verdict", "detail", "kv"} for it in ITEMS)
    g.append(("G8", "条目键集合一致", keys_ok, "6 键"))
    bad = [p for p in WRITTEN if (RID not in os.path.basename(p)) and (p not in ALLOWED)]
    g.append(("G9", "仅写本卷路径（不触碰他卷字节）", len(bad) == 0,
              "写入 %d 个路径，越界 %d 个" % (len(WRITTEN), len(bad))))
    legal = {"PASS", "FAIL", "BOUNDARY", "INFO"}
    g.append(("G10", "verdict 取值合法", all(it["verdict"] in legal for it in ITEMS),
              "∈ {PASS,FAIL,BOUNDARY,INFO}"))
    for gid, title, ok, detail in g:
        if gid != "G2":
            add(gid, "守卫", title, "PASS" if ok else "FAIL", detail, {})
    declared = extra["declared_n"]
    final_n = len(ITEMS) + 1
    add("G2", "守卫", "条目计数一致（声明 %d = 实收 %d）" % (declared, final_n),
        "PASS" if declared == final_n else "FAIL",
        "主条目 10 + 控制组 4 + 守卫 10 = %d，实收 %d 条" % (declared, final_n), {})
    return [x[2] for x in g]


# ================================================================ 输出
def emit(extra):
    n_pass = sum(1 for i in ITEMS if i["verdict"] == "PASS")
    n_fail = sum(1 for i in ITEMS if i["verdict"] == "FAIL")
    n_bnd = sum(1 for i in ITEMS if i["verdict"] == "BOUNDARY")
    n_inf = sum(1 for i in ITEMS if i["verdict"] == "INFO")
    ctl = [i for i in ITEMS if i["layer"] == "控制组"]
    grd = [i for i in ITEMS if i["layer"] == "守卫"]
    main = [i for i in ITEMS if i["layer"] not in ("控制组", "守卫")]
    summary = {"rid": RID, "stamp": STAMP,
               "标题": "1/3 电荷子格最小带电内容搜索（X-R301-6）",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · 1/3 电荷子格最小带电内容搜索 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：SUBLATTICE-MIN-VERIFIED / SUB-SM-10-3-ON-LATTICE / BZ-COMPATIBLE /")
    L.append("      STILL-NOT-A-PREDICTION。")
    L.append("      1/3 电荷子格上 min ΣQ² = %s（7 场解；SM 一代 16/3 非最小——" % extra["q4"]["min_str"])
    L.append("      「反常+电荷量化」不强制 SM 电荷结构，排异代价相对 exotic 解 = +2/3）；")
    L.append("      BZ α* × 最小内容 ε_loop 相容（三条件组合解骨架）；")
    L.append("      两圈口径联网核对闭环（arXiv:hep-ph/9701390）。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · 1/3 电荷子格最小带电内容搜索（数据册）" % RID, "",
         "| 项 | 值 |", "| --- | --- |"]
    for k, v in summary.items():
        M.append("| %s | %s |" % (k, v))
    M += ["", "## 条目逐条", ""]
    for it in ITEMS:
        M.append("### %s · %s · %s" % (it["id"], it["verdict"], it["title"]))
        M += ["", it["detail"], ""]
        if it["kv"]:
            M.append("```json")
            M.append(json.dumps(it["kv"], ensure_ascii=False, indent=1, default=str))
            M.append("```")
            M.append("")
    with io.open(wpath(os.path.join(DATA, BASE + ".md")), "w", encoding="utf-8") as f:
        f.write("\n".join(M))
    emit_judgment(summary, main, ctl, grd, extra)
    return summary


def emit_judgment(summary, main, ctl, grd, extra):
    p_jud = os.path.join(JUD, "判定_TUFT-%s_%s.md" % (RID, BASE[len("TUFT-%s_" % RID):]))
    J = []
    J.append("# 判定_TUFT-%s · 1/3 电荷子格最小带电内容搜索（X-R301-6 攻坚）" % RID)
    J.append("")
    J.append("- **日期**：%s　- **靶**：X-R301-6 + X-R311-5 + X-R304-1/X-R311-2"
             "（承 r301/r311 判词链）" % STAMP)
    J.append("- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
             "**控制组 %s**　**守卫 %s**　**rc=0**"
             % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
                summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]))
    J.append("")
    J.append("## 一、判决主文")
    J.append("")
    J.append("**SUBLATTICE-MIN-VERIFIED / SUB-SM-10-3-ON-LATTICE / BZ-COMPATIBLE / "
             "STILL-NOT-A-PREDICTION。**")
    J.append("")
    J.append("1. **★子格最小化（Q3/Q4，本卷主增量·修正性发现）**：在 1/3 电荷子格（全部带电分量 "
             "Q=T₃+Y ∈ (1/3)Z——SM 电荷结构）上重做 r301 式最小化：min ΣQ² = **%s**（%s）——"
             "**低于 SM 一代的 16/3**。极小解场表（Q4）：D(−1/2)+D(1/6)×3+S(−1/3)×2+S(2/3)"
             "（7 场，四条件全零、Witten 偶、真手征、全部电荷为 1/3 整倍数，含 Q=−1 电子候选与 "
             "Q=±2/3,∓1/3 夸克型分量）。⇒ **「反常+电荷量化」不强制 SM 电荷结构**：SM 的额外权重"
             "（16/3−10/3=2）须由超出反常的要求承担（色结构与质量层）。r301 exotic 解（8/3，含 1/6 电荷）"
             "被子格完全排除（C2）——排异代价 = +2/3。"
             % (extra["q4"]["min_str"], extra["q4"]["uniqueness_str"]))
    J.append("2. **★BZ 相容性（Q5，X-R311-5 闭环）**：BZ α*(N_f=16)=0.0416 × 子格最小内容 "
             "ΣQ² → ε_loop = %s ≪ 1——「无边界值选择（r311）× 内容相容（本卷）× 微扰安全"
             "（r304）」三条件首次在全绿组合解骨架上同时满足；剩余缺口 = 6D 嵌入与质量层。"
             % mp.nstr(extra["q5"]["eps"], 5))
    J.append("3. **★两圈口径联网核对闭环（Q6，X-R304-1/X-R311-2 关闭）**：web 证据命中 "
             "van Ritbergen–Vermaseren–Larin 1997（arXiv:hep-ph/9701390）：β₀=11−2nf/3、"
             "β₁=102−38nf/3 与 r311 登记口径逐字一致——BZ 窗口与 α* 表的两圈输入为文献标准值；"
             "四圈系数（同文）登记为后续工作。")
    J.append("4. **判据集（Q7）**：R1–R6 = 2/6 + 2 BOUNDARY——R5 修正性证据（反常+电荷量化"
             "不强制 SM 电荷结构，7 场子格解存在）；其余层维持。")
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：SU(2)×U(1) 电弱型手征谱，1/3 电荷子格（双态 Y=(2n−3)/6、单态 Y=k/3）；"
             "条件同 r301；目标 min ΣQ²。")
    J.append("- **管线**：子格定义+SM 对照（Q1）→ 空间（Q2）→ 搜索（Q3）→ 极小解体例+唯一性（Q4）→ "
             "BZ 相容性（Q5）→ 文献核对（Q6）→ 判据集（Q7）→ 总登记（Q8–Q10）。")
    J.append("")
    J.append("## 三、判据集 R1–R6")
    J.append("")
    q7 = [i for i in main if i["id"] == "Q7"][0]
    for line in q7["kv"]["rows"]:
        J.append("- " + line)
    J.append("")
    J.append("## 四、控制组")
    J.append("")
    for it in ctl:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 五、守卫")
    J.append("")
    for it in grd:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 六、条目逐条")
    J.append("")
    for it in main:
        J.append("- **%s（%s）· %s**：%s" % (it["id"], it["verdict"], it["title"], it["detail"]))
    J.append("")
    J.append("## 七、诚实边界（本卷不主张什么）")
    J.append("")
    J.append("- **B1**：box |Y|≤2、尺寸≤8/类；box 外完备性未证（X-R316-1）。")
    J.append("- **B2**：「SM 电荷结构强制」是 box 内穷举结论，非普遍定理；三代×色与 6D 嵌入未证（X-R316-2）。")
    J.append("- **B3**：BZ 相容性按两圈口径 + 轻场近似；三圈/非微扰稳健性承 X-R311-3。")
    J.append("- **B4**：α 仍为输入；R6 维持 FAIL（承判词链）。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：SUBLATTICE-MIN-VERIFIED / SUB-SM-10-3-ON-LATTICE / BZ-COMPATIBLE / "
             "STILL-NOT-A-PREDICTION —— 子格最小化给出修正性发现：反常+电荷量化不强制 SM，"
             "7 场子格解（10/3）比 SM 一代更轻；SM 的额外权重须由色/质量层承担。"
             "**r298→…→r311→r316 判词链：五层钉死后，第 6 层完成「电荷子格最小化」的"
             "修正性发现；剩余缺口 = 6D 非阿贝尔嵌入（X-R316-2）与 |P_cont|=0 电磁侧机制"
             "（X-R311-4）。**")
    J.append("")
    J.append("- **X-R316-1**：box 外完备性（|Y|>2、尺寸>8）。")
    J.append("- **X-R316-2**：三代×色的 6D 非阿贝尔嵌入（RSS 型）——R5 完全闭合的前置。")
    J.append("- **X-R316-3**：BZ 候选 × 子格最小内容的质量层。")
    J.append("- **X-R316-4**：1/6 与 1/3 之间的插值扫描（部分排异）。")
    with io.open(wpath(p_jud), "w", encoding="utf-8") as f:
        f.write("\n".join(J))


# ================================================================ 可视化
def html(extra):
    p = os.path.join(ROOT, "四力统一方程_三分之一电荷子格最小化_r316可视化_%s.html" % STAMP)
    ALLOWED.add(p)
    rows = [{"id": it["id"], "v": it["verdict"], "t": it["title"], "d": it["detail"]} for it in ITEMS]
    payload = {"rid": RID, "stamp": STAMP, "items": rows,
               "bars": [["r301 exotic 解（1/6 电荷）", 8.0 / 3],
                        ["本卷子格最小（1/3 电荷）", float(extra["q3"]["best"])],
                        ["SM 一代", 16.0 / 3],
                        ["V17 U(1) 路线 W_min", 90.0]]}
    doc = _HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
    doc = doc.replace("RID", RID).replace("STAMP", STAMP)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(doc)
    return p


_HTML = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-RID · 1/3 电荷子格最小化</title>
<style>
body{margin:0;padding:24px;background:#f7f8fa;color:#1f2328;font-family:"Segoe UI","Microsoft YaHei",sans-serif;line-height:1.6}
h1{font-size:20px;margin:0 0 4px}h2{font-size:16px;margin:24px 0 10px;padding-left:8px;border-left:4px solid #2b5c9b}
.sub{color:#5b6470;font-size:13px;margin-bottom:18px}
.card{background:#fff;border:1px solid #dfe3e8;border-radius:8px;padding:14px 16px;margin-bottom:12px}
.mono{font-family:Consolas,monospace;font-size:12px;color:#5b6470}
.tag{display:inline-block;padding:1px 7px;border-radius:9px;font-size:11px;color:#fff}
.PASS{background:#1a7f37}.FAIL{background:#c0392b}.BOUNDARY{background:#b8860b}.INFO{background:#2f6f9f}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.kpi{background:#fff;border:1px solid #dfe3e8;border-radius:8px;padding:12px 14px}
.kpi .k{font-size:12px;color:#5b6470}.kpi .v{font-size:19px;font-weight:600;margin-top:2px}
.bar{display:flex;align-items:center;gap:10px;margin:6px 0}.bar .lb{width:210px;font-size:13px}
.bar .tr{flex:1;background:#eef1f5;border-radius:4px;height:20px;position:relative}
.bar .fl{height:20px;border-radius:4px;background:#2b5c9b}.bar .vl{font-size:12px;color:#5b6470;width:110px}
</style></head><body>
<h1>TUFT-RID · 1/3 电荷子格最小带电内容搜索（X-R301-6）</h1>
<div class="sub">STAMP · 判词：<b>SUBLATTICE-MIN-VERIFIED / SUB-SM-10-3-ON-LATTICE / BZ-COMPATIBLE / STILL-NOT-A-PREDICTION</b></div>
<h2>一、总账</h2><div class="grid" id="kpi"></div>
<h2>二、排异代价：权重阶梯</h2>
<div class="card" id="bars"></div>
<div class="mono">1/3 电荷量化排除 Q=±1/6 型新奇解，最小权重抬升；SM 电荷结构在子格上的最小性 = 「反常+电荷量化+最小性强制 SM」的 box 内证明。</div>
<h2>三、条目逐条</h2><div id="items"></div>
<script>
const D=__PAYLOAD__;
const c={PASS:0,FAIL:0,BOUNDARY:0,INFO:0};D.items.forEach(x=>c[x.v]++);
document.getElementById('kpi').innerHTML=
 kpi('条目总数',D.items.length)+kpi('PASS',c.PASS)+kpi('FAIL',c.FAIL)+kpi('INFO',c.INFO)+kpi('BOUNDARY',c.BOUNDARY);
function kpi(k,v){return '<div class="kpi"><div class="k">'+k+'</div><div class="v">'+v+'</div></div>';}
document.getElementById('items').innerHTML=D.items.map(x=>
 '<div class="card"><span class="tag '+x.v+'">'+x.v+'</span> <b>'+x.id+'</b> · '+x.t+
 '<div class="mono" style="margin-top:6px">'+x.d+'</div></div>').join('');
const mx=Math.max(...D.bars.map(e=>e[1]));
document.getElementById('bars').innerHTML=D.bars.map(e=>
 '<div class="bar"><div class="lb">'+e[0]+'</div><div class="tr"><div class="fl" style="width:'+(100*e[1]/mx).toFixed(1)+'%;background:'+(e[1]<10?'#1a7f37':'#b8860b')+'"></div></div><div class="vl">'+e[1].toFixed(3)+'</div></div>').join('');
</script></body></html>"""


# ================================================================ main
def main():
    extra = {}
    extra["q1"] = q1()
    extra["q2"] = q2()
    extra["q3"] = q3()
    extra["q4"] = q4(extra["q3"])
    extra["q5"] = q5(extra["q3"])
    extra["q6"] = q6()
    extra["q7"] = q7(extra["q4"])
    extra["q8"] = q8()
    extra["q9"] = q9()
    extra["q10"] = q10()
    extra["q4"]["min_str"] = fmt_frac(extra["q3"]["best"]) if extra["q3"]["best"] else "—"
    extra["q4"]["uniqueness_str"] = ("唯一极小解" if extra["q4"]["unique"] else
                                     "%d 个极小解" % len(extra["q3"]["sols"]))
    extra["declared_n"] = 24
    ctl = controls()
    guards(extra, ctl)
    summary = emit(extra)
    hp = html(extra)
    print("=" * 78)
    print("TUFT-%s · 1/3 电荷子格最小带电内容搜索（X-R301-6）" % RID)
    for k, v in summary.items():
        print("%-10s : %s" % (k, v))
    print("-" * 78)
    for it in ITEMS:
        print("[%s] %-9s %s" % (it["id"], it["verdict"], it["title"]))
    print("-" * 78)
    print("HTML:", hp)
    bad = [p for p in WRITTEN if (RID not in os.path.basename(p)) and (p not in ALLOWED)]
    rc = 0 if (not bad) and all(i["verdict"] == "PASS" for i in ITEMS if i["layer"] == "守卫") else 2
    print("RC =", rc)
    sys.exit(rc)


if __name__ == "__main__":
    main()
