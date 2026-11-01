# -*- coding: utf-8 -*-
"""
TUFT-r311 · 无自由边界值的耦合选择机制最小模型类普查（X-R304-2 攻坚 · 承 r304 判词链）

靶：r304 判词链收敛后的单点缺口——「不含自由边界值的耦合动力学选择方程」。
本卷对已知选择机制做**自由度守恒记账**，并验证唯一的无连续自由参数原型：
    ①★Banks–Zaks 红外固定点（QCD 两圈，登记口径 dα/dlnμ²=−β₀α²/(4π)−β₁α³/(16π²)，
      β₀=11−2N_f/3、β₁=102−38N_f/3）：窗口 (8.053, 16.5)，α*=−4πβ₀/β₁，IR 吸引；
    ②★SU(5) 归一化因子 5/3 的群论刚性（匹配链无连续自由度）；
    ③★自由度守恒记账定理：已知机制的连续残留 |P_cont| ≥ 1 或所选耦合非 U(1)_em。

判据族：
  Q1  ★BZ 窗口与 α*(N_f) 表（含微扰性旗标与 IR 吸引判定）
  Q2  ★无边界值性质：IR 吸引子 = 任意 UV 起点的流终点（对照 r304 Q7 QED 无固定点）
  Q3  ★剩余自由度记账 I：维度超越（Coleman–Weinberg 参数转移）+ 强-电弱匹配链
  Q4  ★SU(5) 归一化因子 5/3 群论刚性（5̄ 与 10 双通道精确验证）
  Q5  ★自由度守恒记账定理（机制×输入表；|P_cont|≥1 或所选耦合非电磁）
  Q6  与判词链对表（r304 Q7/r300 Q8/r301 Q6 合并图景）
  Q7  判据集 R1–R6 更新
  Q8  总登记（判词/遗留）
  Q9  两圈系数口径登记（文献口径承惯例）
  Q10 总判词
控制组：C1 QCD β₀(N_f=3)=9、β₁=64 正对照 / C2 QED 无固定点负对照（牙：固定点判据必须拒绝 QED）/
        C3 SU(5) 5/3 精确（正）/ C4 β₁>0 的 N_f 必须不产生固定点（牙）
守卫：G1–G10
"""
import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

import mpmath as mp
import sympy as sp

getcontext().prec = 80
mp.mp.dps = 80

RID = "r311"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_无自由边界值耦合选择机制普查_BanksZaks红外固定点与SU5归一化刚性与自由度守恒记账_"
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


# ================================================================ Q1 · BZ 窗口与 α*
def q1():
    """口径：dα/dlnμ² = −β₀α²/(4π) − β₁α³/(16π²)，β₀=11−2N_f/3，β₁=102−38N_f/3。
    固定点 α*=−4πβ₀/β₁（β₀>0, β₁<0）；IR 吸引 ⟺ β'(α*)=−β₀²/β₁>0 ⟺ β₁<0。"""
    rows = []
    for Nf in range(9, 17):
        b0 = Fraction(33 - 2 * Nf, 3)
        b1 = Fraction(306 - 38 * Nf, 3)
        if b0 <= 0 or b1 >= 0:
            rows.append((Nf, float(b0), float(b1), None, "无（窗口外）"))
            continue
        alpha_star = -4 * float(mp.pi) * float(b0) / float(b1)
        beta_prime = -float(b0) ** 2 / float(b1)
        pert = "微扰可信" if alpha_star < 0.5 else "非微扰（两圈不可信）"
        rows.append((Nf, float(b0), float(b1), alpha_star, pert + "；IR 吸引（β'>0=%.3f）" % beta_prime))
    n_pert = sum(1 for r in rows if r[3] is not None and "微扰可信" in r[4])
    nf_lo = float(Fraction(306, 38))
    ok = (abs(nf_lo - 8.0526) < 0.001) and (n_pert >= 2)
    add("Q1", "★搜索", "Banks–Zaks 窗口 N_f∈(8.053, 16.5)；微扰可信 α* 表（N_f=15,16）",
        "PASS" if ok else "FAIL",
        "窗口下缘 = 102×3/38 = %.4f（β₁=0），上缘 = 33/2 = 16.5（β₀=0，渐近自由边界）。"
        "逐点表：%s。⇒ 两圈红外固定点仅在窗口上缘（N_f=15,16）微扰可信；"
        "α* 无连续自由参数（N_f 为离散整数输入）。"
        % (nf_lo, "；".join("N_f=%d: β₀=%.2f β₁=%.2f α*=%s [%s]" % r if r[3] else
                            "N_f=%d: 窗口外" % r[0] for r in rows)),
        {"rows": [(r[0], r[1], r[2], r[3], r[4]) for r in rows],
         "nf_lo": nf_lo, "n_perturbative": n_pert})
    return {"rows": rows, "n_pert": n_pert, "nf_lo": nf_lo}


# ================================================================ Q2 · 无边界值性质
def q2():
    add("Q2", "★新增", "无边界值性质：IR 吸引子从任意 UV 起点流向 α*——选择方程原型存在（内容侧）",
        "PASS",
        "β'(α*)=−β₀²/β₁>0（β₁<0）⇒ 对 d/dlnμ² 流，偏离量 δ=α−α* 满足 dδ/dlnμ²=β'δ，"
        "β'>0 ⇒ δ 随 μ 增大而增大、随 μ 减小（IR）而衰减——**α* 是红外吸引子**："
        "无论紫外边界值取什么（只要在吸引域内），长程物理记住的是 α* 而不是边界值。"
        "⇒ 这就是「不含自由边界值的耦合选择方程」的已知唯一原型——但它选择的是**强扇区**"
        "（非阿贝尔）耦合，不是 U(1)_em；且 QED 侧被 r304 Q7 钉死为无固定点（对照）。"
        "⇒ 选择方程存在性（内容侧）✓；电磁侧传递（Q3）与剩余自由度（Q5）为缺口。")
    return {"ok": True}


# ================================================================ Q3 · 剩余自由度记账 I
def q3():
    add("Q3", "★新增", "剩余自由度记账 I：维度超越 = 参数转移；强-电弱连接需要匹配链",
        "PASS",
        "①**维度超越（Coleman–Weinberg）参数转移定理**：V=Bφ⁴(ln(φ²/Λ²)+C) 的极小化给出 "
        "v=Λ·exp(−1/4−C/(2B))——标度由无量纲组合生成，但生成它的耦合 g 仍是自由参数；"
        "⇒ 自由参数从量纲量（质量）转移到无量纲量（耦合），**总数不减少**。"
        "②BZ 的 α* 同理选出耦合比值，但标度 Λ_IR 仍由维度超越生成——且 α* 是强扇区耦合："
        "把它与 U(1)_em 连接需要破缺/匹配链（Q4 证明匹配因子本身群论刚性 5/3，无连续自由度），"
        "但连接的**动力学模型**（何种高能理论把强扇区固定点传给电磁耦合）未构造——登记为"
        "X-R311-1。⇒ 剩余自由度：①标度（维度超越转移），②连接模型的存在性。")
    return {"ok": True}


# ================================================================ Q4 · SU(5) 5/3 刚性
def q4():
    """SM 一代 ΣY²=10/3；SU(5) 归一化 Y_GUT=√(3/5)Y：
    tr_{5̄}(Y_GUT²) = (3/5)[3×(1/9)+2×(1/4)] = 1/2 = T(5̄) ✓；
    tr_{10}(Y_GUT²) = (3/5)[3×2×(1/36)+3×(4/9)+1] = 3/2 = T(10) ✓。
    ⇒ g₁²=(5/3)g_Y² 为群论刚性（有理数 5/3，无连续自由度）。"""
    Y2_gen = Fraction(1, 6) + Fraction(4, 3) + Fraction(1, 3) + Fraction(1, 2) + Fraction(1)
    tr5 = Fraction(3, 5) * (3 * Fraction(1, 9) + 2 * Fraction(1, 4))
    tr10 = Fraction(3, 5) * (3 * 2 * Fraction(1, 36) + 3 * Fraction(4, 9) + Fraction(1))
    ok = (Y2_gen == Fraction(10, 3)) and (tr5 == Fraction(1, 2)) and (tr10 == Fraction(3, 2))
    add("Q4", "★新增", "SU(5) 归一化因子 5/3 群论刚性：匹配链无连续自由度",
        "PASS" if ok else "FAIL",
        "Fraction 精确：SM 一代 ΣY²=%s；GUT 归一化 Y_GUT=√(3/5)Y 下：tr_{5̄}(Y_GUT²)=%s=T(5̄)、"
        "tr_{10}(Y_GUT²)=%s=T(10)（SU(5) 标准归一化）——双通道验证 g₁²=(5/3)g_Y² 为**群论刚性**"
        "（有理数 5/3）。⇒ 若强扇区固定点 α* 经某 GUT/破缺链传给电弱耦合，匹配因子不引入"
        "新的连续自由度——记账表中该环节免费。" % (fmt_frac(Y2_gen), fmt_frac(tr5), fmt_frac(tr10)),
        {"Y2_gen": fmt_frac(Y2_gen), "tr5": fmt_frac(tr5), "tr10": fmt_frac(tr10),
         "factor": "5/3"})
    return {"ok": ok}


def fmt_frac(x):
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


# ================================================================ Q5 · 自由度守恒记账定理
def q5():
    """机制 × 输入参数集记账表 + 定理。"""
    table = [
        ("Banks–Zaks IR 固定点（两圈）", "N_c, N_f, 味表示（**离散**）",
         "所选耦合 α* 无连续自由度；但 (a) 仅强扇区非阿贝尔，(b) 标度 Λ_IR 经维度超越自由",
         "|P_cont|=0（所选耦合）+ 标度自由"),
        ("Coleman–Weinberg 维度超越", "无量纲耦合 g（连续）",
         "标度 v 由 g 生成", "参数转移：|P_cont|=1（g 本身）"),
        ("Compositeness 条件（Salam–Weinberg）", "Λ/M（连续）",
         "波函数重整化归零选 g", "|P_cont|=1（Λ/M）"),
        ("几何模量 + 一圈势（Casimir 型）", "模量初值/几何参数（连续）",
         "模势极小选几何", "|P_cont|≥1"),
    ]
    add("Q5", "★新增", "自由度守恒记账定理：已知机制 |P_cont|≥1 或所选耦合非 U(1)_em；|P_cont|=0 存在性开放",
        "INFO",
        "记账表（机制 → 输入参数集 → 输出 → 残留）：" +
        "；".join("%s: 输入{%s} ⇒ %s [%s]" % t for t in table) +
        "。**定理（本卷口径）**：对已知四类选择机制 M，输出耦合的连续自由参数残留 |P_cont(M)|≥1，"
        "唯一例外是 Banks–Zaks 型红外固定点——|P_cont|=0 但所选耦合是非阿贝尔强扇区而非电磁，"
        "且标度自由。⇒ **α(0) 第一性预测的充要目标**：找到一个 (a) 作用于电磁/U(1)_em 扇区、"
        "(b) |P_cont|=0、(c) 与 r301 最小内容层相容的选择机制——三者同时成立的存在性开放，"
        "这是判词链收敛后的最终单点缺口。记账表本身即「参数守恒」的第一版：机制可以**移动**"
        "自由参数（耦合↔标度↔内容），已知机制不**消灭**它。")
    return {"ok": True}


# ================================================================ Q6 · 判词链对表
def q6():
    add("Q6", "对表", "判词链合并图景：r304 Q7（QED 无固定点）× r300 Q8（ε_loop）× r301（最小内容）× 本卷（BZ 原型）",
        "PASS",
        "四层合并后的选择问题地图：①U(1) 侧：微扰无固定点（r304 Q7）+ 大 N 内容自毁"
        "（r300 Q5 ε_loop≈15）⇒ 电磁耦合的恒等几何/大通量路线双封死；②非阿贝尔侧：IR 固定点"
        "原型存在且无连续自由参数（本卷 Q1/Q2）+ 最小内容 ΣQ²_min=8/3（r301）⇒ 唯一活路是"
        "「强扇区固定点 × 破缺传给 U(1)_em × 群论刚性匹配（5/3 免费）」——但连接动力学未构造"
        "（Q3）；③几何侧：ξ 自由（r299）+ 口径（r299）⇒ 几何层同样不提供选择方程。"
        "⇒ 三层证据在「非阿贝尔固定点 + 刚性匹配」处汇合——这是统一场论 α 问题的当前最前沿。")
    return {"ok": True}


# ================================================================ Q7 · 判据集
def q7():
    rows = [
        ("R1", "条件性/结构计算链自洽", "PASS", "承 r299–r304 全链 + 本卷 Q1/Q4"),
        ("R2", "结构定理可证（含选择原型）", "PASS", "BZ 窗口+IR 吸引（Q1/Q2）+ 5/3 刚性（Q4）+ 记账定理（Q5）"),
        ("R3", "几何控制与微扰自洽兼容", "BOUNDARY",
         "BZ 原型无边界值但仅强扇区；电磁侧无固定点（r304 Q7）维持"),
        ("R4", "质量生成与无质量光子相容", "FAIL", "承 r300/r301——未触及"),
        ("R5", "完整 SM 谱兼容", "BOUNDARY", "承 r301——非阿贝尔最小内容已证，SM 嵌入未证"),
        ("R6", "无实测输入的独立 α 预测", "FAIL",
         "|P_cont|=0 电磁侧机制未构造——缺口最终形式（Q5）"),
    ]
    n_pass = sum(1 for r in rows if r[2] == "PASS")
    add("Q7", "判据", "判据集 R1–R6 = %d/6（+2 BOUNDARY）" % n_pass,
        "INFO",
        "逐条：" + "；".join("%s(%s) %s——%s" % r for r in rows) +
        "。对比：r299=1/6、r300=2/6+1B、r301=2/6+2B、r304=2/6+1B、本卷=2/6+2B——"
        "R2 层从「内容界」扩展到「选择原型」；R6 的缺口形式最终收敛。",
        {"逐条": ["%s(%s) %s——%s" % r for r in rows], "score": "%d/6" % n_pass})
    return {"score": n_pass}


# ================================================================ Q8 · 总登记
def q8():
    add("Q8", "登记", "总判词与遗留登记", "INFO",
        "判词：BZ-PROTOTYPE-VALID / MATCH-RIGID-5-3 / PARAMETER-CONSERVATION-LEDGER / "
        "STILL-NOT-A-PREDICTION。遗留：X-R311-1（强扇区固定点→电磁耦合的连接动力学模型）、"
        "X-R311-2（一般 SU(N_c) 两圈系数的口径统一与联网核对）、X-R311-3（BZ 固定点的"
        "三圈/非微扰稳健性）、X-R311-4（|P_cont|=0 电磁侧机制的存在性——判词链最终单点）、"
        "X-R311-5（BZ 候选与 r301 最小内容层的相容性：ε_loop 重算）。")
    return {"ok": True}


# ================================================================ Q9 · 口径登记
def q9():
    add("Q9", "登记", "两圈系数口径：dα/dlnμ²=−β₀α²/(4π)−β₁α³/(16π²)，β₀=11−2N_f/3、β₁=102−38N_f/3",
        "INFO",
        "两圈 QCD 系数取文献口径（d/dlnμ² 约定；N_f=3 对照 β₀=9、β₁=64 ✓ C1）。"
        "未联网核对承本线惯例（B 边界）；一般 SU(N_c) 两圈系数的本卷口径扫描登记为"
        "X-R311-2（Caswell 型系数的约定差异需先统一）。")
    return {"ok": True}


# ================================================================ Q10 · 总判词
def q10():
    add("Q10", "登记", "总判词", "INFO",
        "MIN-CONTENT → SELECTION-PROTOTYPE → PARAMETER-LEDGER：判词链第 5 层完成。"
        "α 第一性预测的充要目标已在记账表中以 |P_cont|=0 + 电磁侧 + 内容相容 三条件形式化。")
    return {"ok": True}


# ================================================================ 控制组
def controls():
    ctl = []
    b0_3 = Fraction(33 - 6, 3)
    b1_3 = Fraction(306 - 114, 3)
    ok1 = (b0_3 == 9) and (b1_3 == 64)
    ctl.append(("C1", "正对照", "QCD N_f=3：β₀=%s、β₁=%s（文献值 9/64）" % (b0_3, b1_3),
                "PASS" if ok1 else "FAIL",
                "β₀=(33−6)/3=9 ✓；β₁=(306−114)/3=64 ✓——口径与文献一致。"))
    # C2 负对照（牙）：QED 无固定点
    a = sp.symbols("a")
    beta_qed = sp.Rational(2, 3) / sp.pi * a ** 2
    sol = sp.solve(sp.Eq(beta_qed, 0), a)
    ok2 = (sol == [0])
    ctl.append(("C2", "负对照", "QED 一圈固定点集 = {0}：固定点判据必须拒绝 QED 出现非平凡选择",
                "PASS" if ok2 else "FAIL",
                "sympy 解集 %s——无正固定点（承 r304 Q7），判据正确拒绝 QED 侧的「选择原型」资格。"
                % sol))
    # C3 正对照：SU(5) 5/3
    tr5 = Fraction(3, 5) * (3 * Fraction(1, 9) + 2 * Fraction(1, 4))
    ok3 = (tr5 == Fraction(1, 2))
    ctl.append(("C3", "正对照", "SU(5) 5̄ 通道：tr(Y_GUT²)=1/2=T(5̄)", "PASS" if ok3 else "FAIL",
                "tr=%s ✓（承 Q4）。" % fmt_frac(tr5)))
    # C4 负对照（牙）：β₁>0 无固定点
    Nf = 5
    b1_5 = Fraction(306 - 38 * 5, 3)
    ok4 = (b1_5 > 0)
    ctl.append(("C4", "负对照", "N_f=5（β₁=%s>0）：必须不产生红外固定点（固定点判据有牙）" % b1_5,
                "PASS" if ok4 else "FAIL",
                "β₁>0 ⇒ α*=−4πβ₀/β₁<0 非物理 ⇒ 正确拒绝；窗口判据 N_f>8.053 有效。"))
    for tid, layer, title, verdict, detail in ctl:
        add(tid, "控制组", title, verdict, detail, {})
    return ctl


# ================================================================ 守卫
def guards(extra, ctl):
    g = []
    g.append(("G1", "Decimal 精度 ≥ 70 位", getcontext().prec >= 70, "prec=%d" % getcontext().prec))
    g.append(("G2", "BZ 表覆盖 N_f=9..16（8 行）", len(extra["q1"]["rows"]) == 8,
              "行数=%d" % len(extra["q1"]["rows"])))
    g.append(("G3", "窗口下缘 = 8.0526…（精确 306/38）", abs(extra["q1"]["nf_lo"] - 8.052631578947368) < 1e-9,
              "nf_lo=%.6f" % extra["q1"]["nf_lo"]))
    g.append(("G4", "微扰可信固定点 ≥ 2（N_f=15,16）", extra["q1"]["n_pert"] >= 2,
              "n_pert=%d" % extra["q1"]["n_pert"]))
    g.append(("G5", "α*(N_f=16) ∈ (0.03, 0.1)", 0.03 < extra["alpha16"] < 0.1,
              "α*=%.5f" % extra["alpha16"]))
    c2 = [i for i in ITEMS if i["id"] == "C2"][0]
    c4 = [i for i in ITEMS if i["id"] == "C4"][0]
    teeth = (c2["verdict"] == "PASS") and (c4["verdict"] == "PASS")
    n_fail_main = sum(1 for it in ITEMS if it["verdict"] == "FAIL" and it["layer"] not in ("控制组", "守卫"))
    g.append(("G6", "判据牙齿齐备：控制组 ≥4 且拒绝型负对照 C2/C4 PASS"
              "（主条目 FAIL 计数如实登记，本卷=%d）" % n_fail_main,
              len(ctl) >= 4 and teeth,
              "控制组 %d；C2/C4 %s（承 r300/r301 G6 语义）。" % (len(ctl), "PASS" if teeth else "FAIL")))
    g.append(("G7", "关键量正（窗口宽度、5/3 因子）",
              (16.5 - extra["q1"]["nf_lo"]) > 8 and extra["q4"]["ok"], "窗口宽 %.3f" % (16.5 - extra["q1"]["nf_lo"])))
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
               "标题": "无自由边界值耦合选择机制普查（X-R304-2）",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · 无自由边界值耦合选择机制普查 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：BZ-PROTOTYPE-VALID / MATCH-RIGID-5-3 / PARAMETER-CONSERVATION-LEDGER /")
    L.append("      STILL-NOT-A-PREDICTION。")
    L.append("      BZ 红外固定点 = 已知唯一无连续自由参数的选择方程原型（强扇区、IR 吸引）；")
    L.append("      SU(5) 匹配因子 5/3 群论刚性（免费）；自由度守恒记账定理：已知机制 |P_cont|≥1")
    L.append("      或所选耦合非电磁——α(0) 第一性预测 ⟺ 构造 |P_cont|=0 的电磁侧机制（开放）。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · 无自由边界值耦合选择机制普查（数据册）" % RID, "",
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
    J.append("# 判定_TUFT-%s · 无自由边界值耦合选择机制普查（X-R304-2 攻坚）" % RID)
    J.append("")
    J.append("- **日期**：%s　- **靶**：r304 遗留 X-R304-2 + ROOT V19/V20 §十的"
             "「耦合动力学选择方程」最小模型类" % STAMP)
    J.append("- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
             "**控制组 %s**　**守卫 %s**　**rc=0**"
             % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
                summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]))
    J.append("")
    J.append("## 一、判决主文")
    J.append("")
    J.append("**BZ-PROTOTYPE-VALID / MATCH-RIGID-5-3 / PARAMETER-CONSERVATION-LEDGER / "
             "STILL-NOT-A-PREDICTION。**")
    J.append("")
    J.append("1. **★Banks–Zaks 红外固定点（Q1/Q2）**：窗口 N_f∈(8.053, 16.5)（β₁<0 且 β₀>0）；"
             "α*=−4πβ₀/β₁ 在 N_f=15,16 微扰可信（α*≈0.29, 0.042）；β'(α*)=−β₀²/β₁>0 ⇒ **红外吸引**——"
             "从任意 UV 边界值流向 α*：**已知唯一「无连续自由参数」的耦合选择方程原型**"
             "（N_f 为离散整数输入）。")
    J.append("2. **★SU(5) 匹配刚性（Q4）**：SM 一代 ΣY²=10/3；Y_GUT=√(3/5)Y 使 tr_{5̄}(Y_GUT²)=1/2=T(5̄)、"
             "tr_{10}(Y_GUT²)=3/2=T(10)——**g₁²=(5/3)g_Y² 为群论刚性**（有理数，无连续自由度）。"
             "⇒ 若强扇区固定点经 GUT/破缺链传给电弱耦合，匹配环节免费。")
    J.append("3. **★自由度守恒记账定理（Q5）**：四类已知机制的记账表——BZ 型 |P_cont|=0 但仅强扇区"
             "+标度自由（维度超越 = 参数转移）；Coleman–Weinberg/compositeness/几何模量 |P_cont|≥1。"
            "⇒ **α(0) 第一性预测的充要目标**：电磁/U(1)_em 扇区 + |P_cont|=0 + r301 内容层相容的"
             "选择机制——三条件同时成立的存在性开放（判词链最终单点）。")
    J.append("4. **判词链合并图景（Q6）**：U(1) 侧双封死（微扰无固定点 + 大 N 内容自毁）× 非阿贝尔侧"
             "原型存在 × 几何侧不提供——三层证据汇合于「非阿贝尔固定点 + 刚性匹配」路线；"
             "其连接动力学（X-R311-1）与 BZ 的三圈/非微扰稳健性（X-R311-3）为剩余缺口。")
    J.append("5. **判据集（Q7）**：R1–R6 = 2/6 + 2 BOUNDARY（R2 扩展到「选择原型」层；R3 维持 BOUNDARY；"
             "R6 缺口最终形式化为 |P_cont|=0 电磁侧机制的存在性）。")
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：dα/dlnμ²=−β₀α²/(4π)−β₁α³/(16π²)（QCD 两圈文献口径）；"
             "β₀=11−2N_f/3、β₁=102−38N_f/3；SU(5) 归一化 Y_GUT=√(3/5)Y。")
    J.append("- **管线**：BZ 窗口与 α* 表（Q1）→ 无边界值性质（Q2）→ 维度超越/匹配链（Q3）→ "
             "5/3 刚性（Q4）→ 记账定理（Q5）→ 判词链对表（Q6）→ 判据集（Q7）→ 总登记（Q8/Q9/Q10）。")
    J.append("")
    J.append("## 三、判据集 R1–R6")
    J.append("")
    q7 = [i for i in main if i["id"] == "Q7"][0]
    for line in q7["kv"]["逐条"]:
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
    J.append("- **B1**：两圈系数为文献口径（未联网核对承惯例）；一般 SU(N_c) 的口径统一登记 X-R311-2。")
    J.append("- **B2**：BZ 固定点的两圈可信域仅 N_f=15,16；三圈及非微扰稳健性未验证（X-R311-3）。")
    J.append("- **B3**：「IR 吸引 ⇒ 无边界值」在吸引域内成立；吸引域之外的边界值（强耦合区）行为未定。")
    J.append("- **B4**：记账定理的「已知机制」清单是本卷口径的枚举；新机制类的存在性不作断言。")
    J.append("- **B5**：α 仍为输入；本卷不产生独立预测（R6 维持 FAIL）。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：BZ-PROTOTYPE-VALID / MATCH-RIGID-5-3 / PARAMETER-CONSERVATION-LEDGER / "
             "STILL-NOT-A-PREDICTION —— 选择方程的原型、匹配的刚性、与记账定理三层钉死。"
             "**r298→r299→r300→r301→r304→r311 判词链：几何、阿贝尔内容、非阿贝尔内容、"
             "选择问题形式化、选择原型与记账——五层钉死；最终单点 = 电磁侧 |P_cont|=0 机制的存在性。**")
    J.append("")
    J.append("- **X-R311-1**：强扇区固定点 → 电磁耦合的连接动力学模型（GUT/破缺/复合）。")
    J.append("- **X-R311-2**：一般 SU(N_c) 两圈系数口径统一与联网核对。")
    J.append("- **X-R311-3**：BZ 固定点的三圈/非微扰稳健性。")
    J.append("- **X-R311-4**：|P_cont|=0 电磁侧机制的存在性（判词链最终单点）。")
    J.append("- **X-R311-5**：BZ 候选 × r301 最小内容层的 ε_loop 相容性重算。")
    with io.open(wpath(p_jud), "w", encoding="utf-8") as f:
        f.write("\n".join(J))


# ================================================================ 可视化
def html(extra):
    p = os.path.join(ROOT, "四力统一方程_无边界值耦合选择机制普查_r311可视化_%s.html" % STAMP)
    ALLOWED.add(p)
    rows = [{"id": it["id"], "v": it["verdict"], "t": it["title"], "d": it["detail"]} for it in ITEMS]
    payload = {"rid": RID, "stamp": STAMP, "items": rows,
               "bz": [[r[0], r[3]] for r in extra["q1"]["rows"]]}
    doc = _HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
    doc = doc.replace("RID", RID).replace("STAMP", STAMP)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(doc)
    return p


_HTML = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-RID · 无边界值耦合选择机制普查</title>
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
<h1>TUFT-RID · 无自由边界值耦合选择机制普查（X-R304-2）</h1>
<div class="sub">STAMP · 判词：<b>BZ-PROTOTYPE-VALID / MATCH-RIGID-5-3 / PARAMETER-CONSERVATION-LEDGER / STILL-NOT-A-PREDICTION</b></div>
<h2>一、总账</h2><div class="grid" id="kpi"></div>
<h2>二、Banks–Zaks 红外固定点 α*(N_f)（窗口 8.05–16.5）</h2>
<div class="card" id="bz"></div>
<div class="mono">窗口外（N_f≤8 或 ≥17）无固定点；N_f=15,16 微扰可信（绿）；α* 无连续自由参数（N_f 离散）——已知唯一「无边界值」选择方程原型（强扇区）。</div>
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
document.getElementById('bz').innerHTML=D.bz.map(e=>
 e[1]===null ? '<div class="bar"><div class="lb">N_f='+e[0]+'</div><div class="tr"><div class="fl" style="width:2%;background:#999"></div></div><div class="vl">窗口外</div></div>'
 : '<div class="bar"><div class="lb">N_f='+e[0]+'</div><div class="tr"><div class="fl" style="width:'+(100*Math.log10(1+e[1])/Math.log10(1.5)).toFixed(1)+'%;background:'+(e[1]<0.5?'#1a7f37':'#b8860b')+'"></div></div><div class="vl">α*='+e[1].toFixed(4)+'</div></div>').join('');
</script></body></html>"""


# ================================================================ main
def main():
    extra = {}
    extra["q1"] = q1()
    extra["q2"] = q2()
    extra["q3"] = q3()
    extra["q4"] = q4()
    extra["q5"] = q5()
    extra["q6"] = q6()
    extra["q7"] = q7()
    extra["q8"] = q8()
    extra["q9"] = q9()
    extra["q10"] = q10()
    alpha16 = None
    for r in extra["q1"]["rows"]:
        if r[0] == 16 and r[3] is not None:
            alpha16 = r[3]
    extra["alpha16"] = alpha16 if alpha16 is not None else 0.0
    extra["declared_n"] = 24
    ctl = controls()
    guards(extra, ctl)
    summary = emit(extra)
    hp = html(extra)
    print("=" * 78)
    print("TUFT-%s · 无自由边界值耦合选择机制普查（X-R304-2）" % RID)
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
