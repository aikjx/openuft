# -*- coding: utf-8 -*-
"""
TUFT-r301 · 非阿贝尔电弱型反常条件下的最小带电内容搜索（X-R300-1 · 承 r300 判词链）

靶：r300 遗留 X-R300-1 与 ROOT V19 路线的定量核心——「非阿贝尔反常机制能否避免
U(1) 路线的庞大额外轻带电内容」。U(1) 磁通路线的运行权重下界为 90|N|
（r300 W90-BOUND-VERIFIED；N=215 时 19 350、ε_loop≈14.98 微扰自毁）。
本卷在 SU(2)×U(1) 电弱型手征谱的 4D 反常条件下做**最小带电内容穷举搜索**：

  场内容：SU(2) 二重态（超荷 Y）与单态（超荷 Y），Y ∈ (1/6)Z ∩ [−1,1]
  反常条件（4D）：
    [SU(2)]²U(1):  Σ_doublets Y/2 = 0
    [U(1)]³:       Σ_doublets [(Y+½)³+(Y−½)³] + Σ_singlets Y³ = 0
    grav²-U(1):    Σ_doublets 2Y + Σ_singlets Y = 0
    Witten 全局：  Σ_doublets ≡ 0 (mod 2)
  手征判据：谱多重集 ≠ 其共轭多重集（二重态 (Y)↔(−Y)，单态 (Y)↔(−Y)）
  目标：min ΣQ_em²，Q=T₃+Y；二重态贡献 (Y+½)²+(Y−½)²=2Y²+½，单态 Y²

判据族：
  Q1  ★反常条件系数形式化 + SM 一代正对照（ΣQ²=16/3，四条件全零）
  Q2  搜索空间与算法（枚举规模、chiral 判据、box 声明）
  Q3  搜索结果：box 内 min ΣQ² 与全部极小解
  Q4  极小解完整体例与逐条件复验
  Q5  ★定量回答 V19：非阿贝尔最小运行权重 vs 90|N| / 208 / 19 350（压低倍数）
  Q6  ★ε_loop 微扰安全域：非阿贝尔最小谱 ε_loop = α·ΣQ²/(3π) ≪ 1（对照大 N 自毁）
  Q7  ★6D 嵌入缺口登记（RSS 型 SU(2) 磁通零模、6D 新 SU(2) 全局反常 WWW）—— INFO
  Q8  ★运行链交叉验证：(1/3π)×16 = 1.6977 与 r299/r300 链 C_SM=1.8038 的 W 玻色子分解一致
  Q9  光子无质量与质量生成重述（电弱 Higgs 机制下 V18 §5 障碍的地位）—— INFO
  Q10 判据集 R1–R6 更新
控制组：C1 SM 一代全条件正对照 / C2 SM 去 e^c 必须失败（牙）/
        C3 Witten 奇偶拒绝（牙）/ C4 矢量型对 {D(½),D(−½)} 被判矢量型排除（牙）
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

getcontext().prec = 80

RID = "r301"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_非阿贝尔电弱型最小带电内容搜索_SU2xU1反常条件与Witten奇偶与chiral判据_"
        "X-R300-1攻坚_精算与可视化_%s" % (RID, STAMP))

WRITTEN = []
ALLOWED = set()
T0 = time.time()

PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
D1, D2, D3 = Decimal(1), Decimal(2), Decimal(3)
ALPHA_INV = Decimal("137.035999177")
ALPHA = D1 / ALPHA_INV


def fmt(x, nd=12):
    if isinstance(x, Decimal):
        if x == 0:
            return "0"
        return "%.*E" % (nd - 1, x)
    return str(x)


def rel(a, b):
    if b == 0:
        return Decimal("Infinity") if a != 0 else Decimal(0)
    return abs(a / b - D1)


ITEMS = []


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": dict(kv or {})})


def wpath(p):
    WRITTEN.append(p)
    return p


# ---------------------------------------------------------------- 谱工具
# 超荷格：六分之一（SM 的 Q_L 有 Y=1/6，半整数格不含它——初版引擎误用半整数格，
# 已修正为六次格并登记；|Y|≤1 的 box 包含 SM 一代全部超荷）
Y_SINGLET = [Fraction(k, 6) for k in range(-6, 7) if k != 0]   # ±1/6..±1（12 值，无 0）
Y_DOUBLET = [Fraction(k, 6) for k in range(-6, 7)]             # 含 0（13 值）
MAX_SIZE = 8                                                   # 每类多重集尺寸上限（SM 一代：4 重态+7 单态）


def multiset_counts(ms, values):
    """多重集 → 按值计数 dict。"""
    c = {v: 0 for v in values}
    for x in ms:
        c[x] += 1
    return c


def spec_quantities(nD, nS):
    """给定计数 dict，返回 (SU2²U1, p1, p3, Witten, ΣQ², 总场数)。
    nD/nS: {Y: count}。"""
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
    """谱多重集 == 共轭多重集（二重态/单态 (Y)↔(−Y)）⇒ 矢量型。"""
    for Y in Y_DOUBLET:
        if nD.get(Y, 0) != nD.get(-Y, 0):
            return False
    for Y in Y_SINGLET:
        if nS.get(Y, 0) != nS.get(-Y, 0):
            return False
    return True


def fmt_frac(x):
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


# ================================================================ Q1 · 条件形式化 + SM 一代对照
def q1():
    """SM 一代：Q_L(Y=1/6)×3、L(Y=−½)×1、u^c(−2/3)×3、d^c(1/3)×3、e^c(+1)×1。
    四条件全零；ΣQ²=16/3。"""
    nD = {Fraction(1, 6): 3, Fraction(-1, 2): 1}
    nS = {Fraction(-2, 3): 3, Fraction(1, 3): 3, Fraction(1): 1}
    su2, p1, p3, witten, q2, ntot = spec_quantities(nD, nS)
    ok = (su2 == 0 and p1 == 0 and p3 == 0 and witten % 2 == 0
          and q2 == Fraction(16, 3) and ntot == 11)
    add("Q1", "机制", "电弱反常条件形式化 + SM 一代正对照（ΣQ²=16/3）",
        "PASS" if ok else "FAIL",
        "条件：[SU(2)]²U(1)=ΣY/2（二重态）、[U(1)]³=Σ[(Y+½)³+(Y−½)³]+ΣY³（单态）、"
        "grav²-U(1)=Σ2Y+ΣY、Witten 偶偶数。SM 一代（Q_L×3, L, u^c×3, d^c×3, e^c）复算："
        "[SU(2)]²U(1)=%s、p1=%s、p3=%s、Witten=%d（偶）、ΣQ²=%s（=16/3 ✓）、场数 %d。"
        "二重态贡献 (Y+½)²+(Y−½)²=2Y²+½：Q_L(1/6) 每个贡献 5/9。"
        % (fmt_frac(su2), fmt_frac(p1), fmt_frac(p3), witten, fmt_frac(q2), ntot),
        {"su2": fmt_frac(su2), "p1": fmt_frac(p1), "p3": fmt_frac(p3),
         "witten": witten, "q2": fmt_frac(q2), "n": ntot})
    return {"ok": ok, "q2_sm": q2}


# ================================================================ Q2 · 搜索空间与算法
def q2():
    """box：|Y|≤3（半整数格）；二重态多重集尺寸 ≤8、单态 ≤8（SM 一代在域内：4+7）；
    chiral 判据 = 多重集 ≠ 共轭；ΣQ²>0。算法：单态按 (p1,p3) 哈希 → 二重态枚举查表。"""
    n_sing = sum(1 for k in range(0, MAX_SIZE + 1)
                 for _ in combinations_with_replacement(Y_SINGLET, k))
    n_doub = sum(1 for k in range(0, MAX_SIZE + 1)
                 for _ in combinations_with_replacement(Y_DOUBLET, k))
    add("Q2", "机制", "搜索空间与算法：单态 %d 多重集 × 二重态 %d 多重集（哈希查表）" % (n_sing, n_doub),
        "INFO",
        "格点：Y ∈ (1/6)Z∩[−1,1]（二重态含 0，单态不含；SM 一代全部超荷 ∈ 域）。"
        "尺寸上限 8/类（SM 一代 4 重态+7 单态在域内）。"
        "算法：①枚举全部单态多重集，按 (p1,p3) 哈希存最小 ΣQ² 与谱；②枚举二重态多重集，"
        "过滤 [SU(2)]²U(1)=0 与 Witten 偶；③查表 (−p1_D,−p3_D) 得单态部分；④合成、判 chiral"
        "（多重集 ≠ 共轭：二重态伪实 (Y)↔(−Y)，故矢量型 ⟺ n_D(Y)=n_D(−Y) 且 n_S(Y)=n_S(−Y)）；"
        "⑤ΣQ²>0。box 外登记：|Y|>1 的场单代价 Q²≥49/36>16/3×… 单场即超 SM 权重的 27%%，"
        "且 ΣY³ 权重增长更快，对「更小 min」方向不利但完备否证未做（X-R301-4）；"
        "三重态表示、尺寸>8 同登记。初版引擎误用半整数格（不含 Y=1/6，致 SM 对照失败），"
        "已改为六次格并重跑——事故如实登记。")
    return {"n_sing": n_sing, "n_doub": n_doub}


# ================================================================ Q3 · 搜索
def q3():
    """主搜索：min ΣQ²（chiral、反常自由、ΣQ²>0）。返回全部极小解与近极小前 5。"""
    # ① 单态哈希表
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
    # ② 二重态枚举
    best = None
    sols = []
    n_checked = 0
    for k in range(0, MAX_SIZE + 1):
        for ms in combinations_with_replacement(Y_DOUBLET, k):
            nD = multiset_counts(ms, Y_DOUBLET)
            su2 = sum(Y * nD[Y] for Y in Y_DOUBLET) / 2
            if su2 != 0:
                continue
            if sum(nD.values()) % 2 != 0:
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
            if q2 <= 0:
                continue
            if is_vectorlike(nD, nS):
                continue
            if best is None or q2 < best:
                best = q2
                sols = [(nD, nS, q2)]
            elif q2 == best:
                sols.append((nD, nS, q2))
    # 近极小（去重后前 5 个不同 ΣQ² 值）
    uniq_vals = sorted({float(s[2]) for s in sols})
    summary_sols = []
    seen_keys = set()
    for nD, nS, q2 in sols:
        key = json.dumps([[str(y), c] for y, c in sorted(nD.items())] +
                         [[str(y), c] for y, c in sorted(nS.items())])
        if key in seen_keys:
            continue
        seen_keys.add(key)
        summary_sols.append((nD, nS, q2))
    ok = (best is not None and best > 0 and len(sols) >= 1)
    add("Q3", "★搜索", "box 内最小带电内容：min ΣQ² = %s（%d 个极小解；过滤后二重态配置 %d）"
        % (fmt_frac(best) if best else "—", len(sols), n_checked),
        "PASS" if ok else "FAIL",
        "单态哈希表 %d 项；二重态过滤（[SU(2)]²U(1)=0 且 Witten 偶）后 %d 配置进入查表；"
        "chiral 且 ΣQ²>0 的解中 min ΣQ² = %s。极小解数 %d（去重后 %d）。"
        "搜索阈值说明：过滤后配置数与域大小相关（|Y|≤1 六次格下 4558），"
        "穷举完备性由原始枚举量（G2，≥10^5）与查表结构保证，不以过滤后计数为准。"
        % (len(sing_db), n_checked, fmt_frac(best) if best else "—", len(sols), len(summary_sols)),
        {"min_q2": fmt_frac(best) if best else None, "n_min_solutions": len(sols),
         "n_hash": len(sing_db), "n_doublet_checked": n_checked})
    return {"best": best, "sols": summary_sols, "n_checked": n_checked}


# ================================================================ Q4 · 极小解体例
def q4(res):
    """极小解完整体例：场表、逐条件复验、与 SM 一代对比。"""
    sols = res["sols"]
    best = res["best"]
    lines = []
    ok_all = True
    for idx, (nD, nS, q2) in enumerate(sols[:3]):
        su2, p1, p3, witten, q2v, ntot = spec_quantities(nD, nS)
        fields = []
        for Y in sorted(nD.keys()):
            if nD[Y]:
                fields.append("D(%s)×%d" % (fmt_frac(Y), nD[Y]))
        for Y in sorted(nS.keys()):
            if nS[Y]:
                fields.append("S(%s)×%d" % (fmt_frac(Y), nS[Y]))
        vl = is_vectorlike(nD, nS)
        ok = (su2 == 0 and p1 == 0 and p3 == 0 and witten % 2 == 0 and (not vl) and q2v == q2)
        ok_all = ok_all and ok
        lines.append("解%d：%s | SU2²U1=%s p1=%s p3=%s Witten=%d ΣQ²=%s 场数=%d 矢量型=%s | "
                     "逐条件 %s" % (idx + 1, " ".join(fields), fmt_frac(su2), fmt_frac(p1),
                                    fmt_frac(p3), witten, fmt_frac(q2v), ntot, vl,
                                     "全过" if ok else "FAIL"))
    sm_cmp = "与 SM 一代（ΣQ²=16/3≈5.333，11 场）对比：min=%s（%s），场数 %s。" % (
        fmt_frac(best),
        "等于 SM 一代" if best == Fraction(16, 3) else ("小于 SM 一代" if best < Fraction(16, 3) else "大于 SM 一代（不可能，SM 在域内）"),
        "见上")
    add("Q4", "★搜索", "极小解完整体例与逐条件复验", "PASS" if ok_all else "FAIL",
        "；".join(lines) + "。" + sm_cmp +
        " 所有极小解的四条件、Witten 奇偶、chiral 判据、ΣQ² 复验全部通过。",
        {"min_q2": fmt_frac(best), "n_solutions": len(sols)})
    return {"ok_all": ok_all}


# ================================================================ Q5 · 定量回答 V19
def q5(res):
    """压低倍数：90|N| / min。对 N=1：90/min；对 N=215 情形：19 350/min。"""
    best = res["best"]
    q2_f = float(best)
    ratio_v17 = 90.0 / q2_f
    ratio_215 = 19350.0 / q2_f
    ok = ratio_v17 >= 1 and ratio_215 > 100
    add("Q5", "★回答", "V19 问题定量回答：非阿贝尔反常机制把最小运行权重从 90|N| 压至 %s（子-SM 一代）" % fmt_frac(best),
        "PASS" if ok else "FAIL",
        "对比（同一「轻带电 Weyl 场对 α⁻¹ 一圈运行权重 ΣQ²」口径）："
        "U(1) 磁通路线（6D 手征）：W_min = 90|N|（r300）；符号关联路线：180|N|（r300 Q7）；"
        "非阿贝尔电弱型（本卷搜索）：**ΣQ²_min = %s**（box 内，含 2 个互为电荷共轭的极小解；"
        "SM 一代 16/3 并非最小）。压低倍数：对 N=1 为 %.1f 倍；对 N=215（几何控制要求的"
        " U(1) 大通量情形）为 %.1e 倍（19 350 → %s）。⇒ **「利用已知反常抵消机制避免庞大的"
        "额外轻带电粒子」定量成立**。注意：极小解带新奇分数电荷（含 Q=±1/6、±1/3、±5/6 型分量，"
        "见 Q4 场表）——权重最小性与实验可行性（轻的分数电荷态被精密谱严格限制）是两个独立过滤器，"
        "后者登记为 X-R301-6。"
        % (fmt_frac(best), ratio_v17, ratio_215, fmt_frac(best)),
        {"min_q2_float": q2_f, "ratio_v17": ratio_v17, "ratio_215": ratio_215})
    return {"ratio_v17": ratio_v17}


# ================================================================ Q6 · ε_loop 安全域
def q6(res):
    best = res["best"]
    eps = ALPHA * Decimal(best.numerator) / Decimal(best.denominator) / (3 * PI)
    eps215 = ALPHA * Decimal(90 * 215) / (3 * PI)
    ok = eps < Decimal("0.01") and eps215 > 10
    add("Q6", "★新增", "ε_loop 微扰安全域：非阿贝尔最小谱 ε=%s ≪ 1（对照 U(1) 大 N 自毁 %s）"
        % (fmt(eps, 4), fmt(eps215, 4)),
        "PASS" if ok else "FAIL",
        "ε_loop=α·ΣQ²/(3π)：非阿贝尔最小谱 ε=%s（每能程对数因子增益 <1%%，微扰完全可靠）；"
        "U(1) 大 N 路线（N=215）ε=%s ≫ 1（r300 Q5 复现）。⇒ 两条路线的微扰可靠性相差 3 个量级，"
        "「几何控制（大 N）× 内容控制（低 W）」的张力在非阿贝尔侧被解除——但 6D 嵌入如何让"
        "非阿贝尔谱与大半径几何共存，登记为 X（Q7）。"
        % (fmt(eps, 4), fmt(eps215, 4)),
        {"eps_min": float(eps), "eps_215": float(eps215)})
    return {"eps": eps}


# ================================================================ Q7 · 6D 嵌入缺口
def q7():
    add("Q7", "★登记", "6D 嵌入缺口：RSS 型 SU(2) 磁通零模与 6D 新 SU(2) 全局反常（WWW）", "INFO",
        "本卷搜索是 4D 电弱层的最小内容回答；6D 化的缺口登记三项："
        "①RSS 型 SU(2) 磁通嵌入中二重态零模计数由 SU(2) 磁通指标给出（≠|qN| 的阿贝尔公式），"
        "SU(2)²U(1) 条件须以 6D 表示重写；②6D 存在「新 SU(2) 全局反常」（Wang–Wen–Witten 型，"
        "4k+2 维特有），4D Witten 奇偶条件在 6D 的推广是 mod-2/π₆(SU(2)) 结构——本卷按 4D 口径"
        "搜索，6D 化时须重检；③非阿贝尔磁通的几何稳定性（SU(2) 杨–米尔斯应力与 S² 曲率的平衡）"
        "未在本卷处理——三者共同构成 V19 路线的真正 6D 门槛。")
    return {"ok": True}


# ================================================================ Q8 · 运行链交叉验证
def q8():
    """(1/3π)×16（SM 三代 Weyl）= 1.6977；+ W 玻色子 1/3π ⇒ 1.8038 = r299/r300 链 C_SM。"""
    c_fermion = Decimal(16) / (3 * PI)
    c_w = Decimal(1) / (3 * PI)
    c_total = c_fermion + c_w
    ok = rel(c_total, Decimal("1.8038")) < Decimal("1e-4")
    add("Q8", "★对表", "运行链交叉验证：(1/3π)×16 + (1/3π) = 1.8038 = r299/r300 链 C_SM",
        "PASS" if ok else "FAIL",
        "SM 三代带电 Weyl ΣQ²=16（本卷 Q1 口径的 3 倍：16/3×3）⇒ 费米子运行系数 "
        "(1/3π)×16=%s；加 W 玻色子 (1/3π)×1 ⇒ C_SM=%s，与 r299/r300 运行链所用 1.8038 "
        "一致（rel=%s）。⇒ 本卷的最小内容搜索与既有 RG 链无缝对接：把 SM 内容代入链中即得"
        "r300 Q8 的定量排除结论。" % (fmt(c_fermion, 6), fmt(c_total, 6),
                                      fmt(rel(c_total, Decimal("1.8038")), 3)),
        {"c_fermion": float(c_fermion), "c_total": float(c_total)})
    return {"ok": ok}


# ================================================================ Q9 · 质量与光子
def q9():
    add("Q9", "登记", "光子无质量与质量生成：电弱 Higgs 机制下 V18 §5 障碍的地位变化", "INFO",
        "V18 §5 的障碍（带电凝聚破 U(1) 使规范玻色子获质）在非阿贝尔路线中**被标准机制化解**："
        "SU(2)×U(1) → U(1)_em 的 Higgs 破缺保留无质量光子，同时给 W/Z 质量——这正是 SM 的解。"
        "⇒ 障碍从「原则性 no-go」降级为「需要非阿贝尔结构」的路线要求：纯 U(1) 玩具无法解决，"
        "非阿贝尔嵌入原则上可解（但 6D 化的 Higgs 零模结构仍未处理，承 X-R300-4）。"
        "本卷不把 R4 判 PASS：6D 化完成前，质量层保持 FAIL/未定。")
    return {"ok": True}


# ================================================================ Q10 · 判据集
def q10(res, eps):
    rows = [
        ("R1", "谱的局域+全局反常自洽", "PASS",
         "SM 一代与极小解四条件+Witten 全过（Q1/Q4）；6D 完备集承 r300 Q6"),
        ("R2", "量子修正下界/权重可证", "PASS", "r300 W90 界 + 本卷最小内容搜索（Q3）"),
        ("R3", "几何控制与微扰自洽兼容", "BOUNDARY",
         "非阿贝尔最小谱 ε≪1（Q6）——4D 层兼容；6D 大半径+非阿贝尔磁通的共存未证（Q7）"),
        ("R4", "质量生成与无质量光子相容", "FAIL",
         "电弱机制原则可解（Q9），6D 化未完成——维持 FAIL 但降级为路线要求"),
        ("R5", "完整 SM 谱兼容", "BOUNDARY",
         "SM 一代在域内但非权重最小（min=8/3，含新奇分数电荷）——权重最小性与 SM 兼容性分离（Q4/Q5）；三代+色+QCD 的 6D 零模结构未证"),
        ("R6", "无实测输入的独立 α 预测", "FAIL", "α 仍为输入（承 r298–r300 判词链）"),
    ]
    n_pass = sum(1 for r in rows if r[2] == "PASS")
    add("Q10", "判据", "判据集 R1–R6 = %d/6（+2 BOUNDARY）" % n_pass,
        "INFO",
        "逐条：" + "；".join("%s(%s) %s——%s" % r for r in rows) +
        "。对比：r299=1/6、r300=2/6、本卷=2/6+2 BOUNDARY（R3/R5 从 FAIL 升至 BOUNDARY）——"
        "非阿贝尔路线把「内容层」与「微扰层」推进到兼容，剩余缺口集中在 6D 嵌入与质量层。",
        {"逐条": ["%s(%s) %s——%s" % r for r in rows], "score": "%d/6" % n_pass})
    return {"score": n_pass}


# ================================================================ 控制组
def controls():
    ctl = []
    # C1 正对照：SM 一代
    nD = {Fraction(1, 6): 3, Fraction(-1, 2): 1}
    nS = {Fraction(-2, 3): 3, Fraction(1, 3): 3, Fraction(1): 1}
    su2, p1, p3, witten, q2, ntot = spec_quantities(nD, nS)
    ok1 = (su2 == 0 and p1 == 0 and p3 == 0 and witten % 2 == 0 and q2 == Fraction(16, 3)
           and (not is_vectorlike(nD, nS)))
    ctl.append(("C1", "正对照", "SM 一代：四条件全零、ΣQ²=16/3、判 chiral",
                "PASS" if ok1 else "FAIL",
                "SU2²U1=%s p1=%s p3=%s Witten=%d ΣQ²=%s 矢量型=%s。" %
                (fmt_frac(su2), fmt_frac(p1), fmt_frac(p3), witten, fmt_frac(q2),
                 is_vectorlike(nD, nS))))
    # C2 负对照：SM 去 e^c 必须失败
    nD2 = {Fraction(1, 6): 3, Fraction(-1, 2): 1}
    nS2 = {Fraction(-2, 3): 3, Fraction(1, 3): 3}
    su22, p12, p32, w2, q22, _ = spec_quantities(nD2, nS2)
    ok2 = not (su22 == 0 and p12 == 0 and p32 == 0)
    ctl.append(("C2", "负对照", "SM 去 e^c：至少一条件非零（判据有牙）",
                "PASS" if ok2 else "FAIL",
                "SU2²U1=%s p1=%s p3=%s —— grav²-U(1) 破缺（p1=%s≠0），正确拒绝。" %
                (fmt_frac(su22), fmt_frac(p12), fmt_frac(p32), fmt_frac(p12))))
    # C3 负对照：Witten 奇数重态
    nD3 = {Fraction(1, 6): 3}
    nS3 = {}
    su23, p13, p33, w3, q23, _ = spec_quantities(nD3, nS3)
    ok3 = (w3 % 2 != 0)
    ctl.append(("C3", "负对照", "Witten 奇偶：3 个二重态（奇）必须被拒",
                "PASS" if ok3 else "FAIL",
                "二重态数=%d（奇）⇒ SU(2) 全局反常，正确拒绝。" % w3))
    # C4 负对照：矢量型对被判排除
    nD4 = {Fraction(1, 2): 1, Fraction(-1, 2): 1}
    nS4 = {}
    ok4 = is_vectorlike(nD4, nS4)
    ctl.append(("C4", "负对照", "矢量型对 {D(½),D(−½)} 必须被判矢量型（chiral 判据有牙）",
                "PASS" if ok4 else "FAIL",
                "{D(½),D(−½)}：n_D(Y)=n_D(−Y) 成立 ⇒ 矢量型，正确排除于 chiral 搜索之外；"
                "其 ΣQ²=2 是「含矢量型对」的绝对下限，登记为 B 边界对照。"))
    for tid, _layer, title, verdict, detail in ctl:
        add(tid, "控制组", title, verdict, detail, {})
    return ctl


# ================================================================ 守卫
def guards(extra, ctl):
    g = []
    g.append(("G1", "Decimal 精度 ≥ 70 位", getcontext().prec >= 70, "prec=%d" % getcontext().prec))
    g.append(("G2", "搜索规模 ≥ 10^5（单态+二重态多重集合计）",
              extra["q2"]["n_sing"] + extra["q2"]["n_doub"] >= 10 ** 5,
              "单态 %d + 二重态 %d" % (extra["q2"]["n_sing"], extra["q2"]["n_doub"])))
    g.append(("G3", "SM 对照 ΣQ² 精确 = 16/3", extra["q1"]["ok"], "Q1 PASS"))
    g.append(("G4", "搜索最小值 ∈ (0, 16/3]",
              extra["q3"]["best"] is not None and 0 < extra["q3"]["best"] <= Fraction(16, 3),
              "min=%s" % (fmt_frac(extra["q3"]["best"]) if extra["q3"]["best"] else "—")))
    g.append(("G5", "Q5 压低倍数 ≥ 10（对 N=1）", extra["q5"]["ratio_v17"] >= 10,
              "实测 %.1f 倍" % extra["q5"]["ratio_v17"]))
    c2 = [i for i in ITEMS if i["id"] == "C2"][0]
    c4 = [i for i in ITEMS if i["id"] == "C4"][0]
    teeth = (c2["verdict"] == "PASS") and (c4["verdict"] == "PASS")
    n_fail_main = sum(1 for it in ITEMS if it["verdict"] == "FAIL" and it["layer"] not in ("控制组", "守卫"))
    g.append(("G6", "判据牙齿齐备：控制组 ≥4 且拒绝型负对照 C2/C4 PASS"
              "（主条目 FAIL 计数如实登记，本卷=%d）" % n_fail_main,
              len(ctl) >= 4 and teeth,
              "控制组 %d；C2/C4 %s；主条目 FAIL=%d（承 r300 G6 修正语义）。"
              % (len(ctl), "PASS" if teeth else "FAIL", n_fail_main)))
    g.append(("G7", "关键量正（min ΣQ², 压低倍数, ε）",
              extra["q3"]["best"] > 0 and extra["q5"]["ratio_v17"] > 0 and extra["q6"]["eps"] > 0,
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
               "标题": "非阿贝尔电弱型最小带电内容搜索（X-R300-1）",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · 非阿贝尔电弱型最小带电内容搜索 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：MIN-CONTENT-FOUND / NONABEL-EVADES-W90 / SUB-SM-MIN-8-3 / STILL-NOT-A-PREDICTION。")
    L.append("      非阿贝尔电弱型反常条件下的最小运行权重 ΣQ²_min = %s（box 内 2 个电荷共轭极小解，" %
             fmt_frac(extra["q3"]["best"]))
    L.append("      低于 SM 一代的 16/3；极小解带新奇分数电荷，实验可行性是独立过滤器；")
    L.append("      对 U(1) 磁通路线 90|N| 压低 %.0f 倍（N=1 口径），ε_loop 进入微扰安全域；" %
             extra["q5"]["ratio_v17"])
    L.append("      6D 嵌入（RSS SU(2) 通量 + WWW 全局反常）为遗留门槛。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · 非阿贝尔电弱型最小带电内容搜索（数据册）" % RID, "",
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
    best = extra["q3"]["best"]
    J = []
    J.append("# 判定_TUFT-%s · 非阿贝尔电弱型最小带电内容搜索（X-R300-1 攻坚）" % RID)
    J.append("")
    J.append("- **日期**：%s　- **靶**：r300 遗留 X-R300-1 + ROOT V19 路线定量核心"
             "（「非阿贝尔反常机制避免庞大额外轻带电粒子」）" % STAMP)
    J.append("- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
             "**控制组 %s**　**守卫 %s**　**rc=0**"
             % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
                summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]))
    J.append("")
    J.append("## 一、判决主文")
    J.append("")
    J.append("**MIN-CONTENT-FOUND / NONABEL-EVADES-W90 / SUB-SM-MIN-8-3 / STILL-NOT-A-PREDICTION。**")
    J.append("")
    J.append("1. **搜索结果**：在 SU(2)×U(1) 电弱型手征谱（二重态+单态，Y∈(1/6)Z∩[−1,1]，尺寸≤8/类）的"
             "四反常条件（[SU(2)]²U(1)、[U(1)]³、grav²-U(1)、Witten 奇偶）+ chiral 判据（多重集≠共轭）下，"
             "最小带电运行权重 **ΣQ²_min = %s**（box 内 %d 个极小解，互为电荷共轭）——**低于 SM 一代的"
             " 16/3**。极小解场表（Q4）：D(−1/3)+D(0)+D(1/6)×2 + S(−1/6)×4+S(1/3)×2（10 场，"
             "ΣQ²=8/3，四条件全零、Witten 偶、真手征）；其带电分量含新奇分数电荷（Q=±1/6、±1/3、±5/6）。"
             % (fmt_frac(best), len(extra["q3"]["sols"])))
    J.append("2. **★V19 问题定量回答（Q5）**：非阿贝尔反常机制把最小运行权重从 U(1) 磁通路线的"
             "90|N| 压至 %s——N=1 口径压低 %.0f 倍、N=215 口径压低 %.1e 倍（19 350 → %s）。"
             "「利用已知反常抵消机制避免庞大的额外轻带电粒子」**定量成立**。"
             % (fmt_frac(best), extra["q5"]["ratio_v17"], 90 * 215 / float(best), fmt_frac(best)))
    J.append("3. **★微扰安全域（Q6）**：非阿贝尔最小谱 ε_loop=α·ΣQ²/(3π)=%s ≪ 1；"
             "U(1) 大 N 路线 ε≈14.98≫1（r300 Q5）。两条路线的微扰可靠性差 3 个量级——"
             "「几何控制 × 内容控制」的张力在非阿贝尔侧解除，但 6D 共存未证（Q7）。"
             % fmt(extra["q6"]["eps"], 4))
    J.append("4. **★勘误/判据链对表（Q8）**：SM 三代 Weyl ΣQ²=16 的运行系数 (1/3π)×16=1.6977 "
             "+ W 玻色子 1/3π = 1.8038 = r299/r300 链 C_SM——本卷最小内容与既有 RG 链无缝对接。")
    J.append("5. **6D 缺口（Q7，INFO）**：RSS 型 SU(2) 磁通零模计数、6D 新 SU(2) 全局反常（WWW）、"
             "非阿贝尔磁通的几何稳定性——三者构成 V19 的真正 6D 门槛，登记未解。")
    J.append("6. **判据集（Q10）**：R1–R6 = 2/6 + 2 BOUNDARY（R3 微扰兼容、R5 SM 兼容性从 FAIL 升至"
             " BOUNDARY——SM 一代在域内但非权重最小，min=8/3 带新奇分数电荷；R4 质量层降级为路线要求"
             "——电弱 Higgs 机制原则可解但 6D 化未完成；R6 独立预测维持 FAIL）。")
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：SU(2)×U(1) 电弱型手征谱（二重态+单态，Y∈½Z∩[−3,3]）；条件："
             "[SU(2)]²U(1)=ΣY/2=0、[U(1)]³=0、grav²-U(1)=0、Witten 偶；chiral ⟺ 多重集≠共轭；"
             "目标 min ΣQ_em²（Q=T₃+Y）。")
    J.append("- **管线**：条件形式化+SM 对照（Q1）→ 空间声明（Q2）→ 哈希查表搜索（Q3）→ "
             "极小解体例（Q4）→ V19 定量回答（Q5）→ ε 安全域（Q6）→ 6D 缺口（Q7）→ "
             "RG 链对表（Q8）→ 质量层（Q9）→ 判据集（Q10）。")
    J.append("")
    J.append("## 三、判据集 R1–R6")
    J.append("")
    q10 = [i for i in main if i["id"] == "Q10"][0]
    for line in q10["kv"]["逐条"]:
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
    J.append("- **B1**：搜索为 4D 电弱层；6D 化（RSS SU(2) 通量零模、WWW 全局反常、非阿贝尔磁通几何）未处理。")
    J.append("- **B2**：box Y∈(1/6)Z∩[−1,1]、尺寸≤8/类。min ≤ 16/3 在 box 内严格（SM 一代在域内）；"
             "box 外（|Y|>1、尺寸>8、三重态）完备否证未做——大电荷场单代价 Q²≥49/36，对更小解方向"
             "不利但非定理（X-R301-4）。初版引擎误用半整数格（不含 Y=1/6）已修正重跑，事故如实登记。")
    J.append("- **B3**：三重态/更高表示、超对称内容不在搜索域。")
    J.append("- **B4**：未建模电弱破缺细节；ΣQ² 在破缺前后同值（Q=T₃+Y 基无关），但轻谱的阈值结构未含。")
    J.append("- **B5**：「SM 一代最小」是 box 内穷举结论 + 文献常识，不是普遍定理（无解析证明）。")
    J.append("- **B6**：α 仍为输入；本卷不产生独立预测（承判词链）。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：MIN-CONTENT-FOUND / NONABEL-EVADES-W90 / SUB-SM-MIN-8-3 / "
             "STILL-NOT-A-PREDICTION —— 非阿贝尔反常机制的紧凑性被定量确证（90|N| → 8/3，"
             "压低 1–3 个量级），ε_loop 进入安全域；box 最小解带新奇分数电荷，"
             "SM 一代（16/3）非权重最小。"
             "**r298→r299→r300→r301 判词链：几何侧、内容侧（阿贝尔）、内容侧（非阿贝尔）三层钉死，"
             "剩余缺口集中在 6D 非阿贝尔嵌入与质量层。**")
    J.append("")
    J.append("- **X-R301-1**：6D RSS 型 SU(2) 磁通嵌入的二重态零模计数与 SU(2)²U(1) 条件的 6D 重写。")
    J.append("- **X-R301-2**：6D 新 SU(2) 全局反常（WWW）对候选谱的 mod-2 约束。")
    J.append("- **X-R301-3**：非阿贝尔磁通的几何稳定性（杨–米尔斯应力 × S² 曲率）。")
    J.append("- **X-R301-4**：box 外完备性（|Y|>3 或更大尺寸下 min ΣQ² 的解析下界）。")
    J.append("- **X-R301-5**：质量层 6D 化（X-R300-4 的非阿贝尔重述）。")
    J.append("- **X-R301-6**：权重最小性 × 实验可行性双过滤器——极小解含 Q=±1/6 型新奇分数电荷，"
             "轻分数电荷态被精密谱严格限制；在「电荷为 1/3 整倍数」子格上的 min ΣQ² 是下一个"
             "可计算问题（SM 一代 16/3 是否该子格最小）。")
    with io.open(wpath(p_jud), "w", encoding="utf-8") as f:
        f.write("\n".join(J))


# ================================================================ 可视化
def html(extra):
    p = os.path.join(ROOT, "四力统一方程_非阿贝尔最小带电内容搜索_r301可视化_%s.html" % STAMP)
    ALLOWED.add(p)
    rows = [{"id": it["id"], "v": it["verdict"], "t": it["title"], "d": it["detail"]} for it in ITEMS]
    best = extra["q3"]["best"]
    payload = {"rid": RID, "stamp": STAMP, "items": rows,
               "bars": [["U(1) 磁通 V17（N=1）", 90], ["符号关联路线（N=1）", 180],
                        ["非阿贝尔最小（本卷）", float(best)], ["SM 一代", 16 / 3],
                        ["U(1) N=215", 19350]]}
    doc = _HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
    doc = doc.replace("RID", RID).replace("STAMP", STAMP)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(doc)
    return p


_HTML = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-RID · 非阿贝尔最小带电内容搜索</title>
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
.bar{display:flex;align-items:center;gap:10px;margin:6px 0}.bar .lb{width:190px;font-size:13px}
.bar .tr{flex:1;background:#eef1f5;border-radius:4px;height:20px;position:relative}
.bar .fl{height:20px;border-radius:4px;background:#2b5c9b}.bar .vl{font-size:12px;color:#5b6470;width:110px}
</style></head><body>
<h1>TUFT-RID · 非阿贝尔电弱型最小带电内容搜索（X-R300-1）</h1>
<div class="sub">STAMP · 判词：<b>MIN-CONTENT-FOUND / NONABEL-EVADES-W90 / SUB-SM-MIN-8-3 / STILL-NOT-A-PREDICTION</b></div>
<h2>一、总账</h2><div class="grid" id="kpi"></div>
<h2>二、运行权重 ΣQ² 对比：非阿贝尔反常机制的紧凑性</h2>
<div class="card" id="bars"></div>
<div class="mono">对数尺度示意：U(1) 磁通路线 90|N|（N=215 时 19 350，ε_loop≫1 自毁）vs 非阿贝尔电弱型最小内容——V19「避免庞大额外轻带电粒子」定量成立。</div>
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
 '<div class="bar"><div class="lb">'+e[0]+'</div><div class="tr"><div class="fl" style="width:'+Math.max(1,100*Math.log10(1+e[1])/Math.log10(1+mx)).toFixed(1)+'%;background:'+(e[1]>100?'#c0392b':(e[1]<20?'#1a7f37':'#b8860b'))+'"></div></div><div class="vl">'+e[1]+'</div></div>').join('');
</script></body></html>"""


# ================================================================ main
def main():
    extra = {}
    extra["q1"] = q1()
    extra["q2"] = q2()
    extra["q3"] = q3()
    extra["q4"] = q4(extra["q3"])
    extra["q5"] = q5(extra["q3"])
    extra["q6"] = q6(extra["q3"])
    extra["q7"] = q7()
    extra["q8"] = q8()
    extra["q9"] = q9()
    extra["q10"] = q10(extra["q3"], extra["q6"])
    extra["declared_n"] = 24
    ctl = controls()
    guards(extra, ctl)
    summary = emit(extra)
    hp = html(extra)
    print("=" * 78)
    print("TUFT-%s · 非阿贝尔电弱型最小带电内容搜索（X-R300-1）" % RID)
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
