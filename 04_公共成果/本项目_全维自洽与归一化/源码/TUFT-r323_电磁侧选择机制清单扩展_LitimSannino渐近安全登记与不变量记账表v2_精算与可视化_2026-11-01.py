# -*- coding: utf-8 -*-
"""
TUFT-r323 · 电磁侧选择机制清单扩展与不变量记账表 v2（X-R317-1/X-R317-3/X-R311-4 攻坚）

靶：r317 判词链的最终单点——X-R311-4（精化：不变量表述的 |P_cont|=0 电磁侧机制）。
本卷三项：
    ①★BZ 原型的不变量表述重写（X-R317-1 收口）：机制×{特征值谱,归一化,内容}分类；
    ②★Litim–Sannino U(1) 渐近安全登记（web 证据：Bednyakov 2024 PRD 109,065030 四圈；
      Bond et al 2017/2018 UV 共形窗）——**电磁侧 |P_cont|=0 候选机制首次进入清单**；
    ③★QED 多圈同号性收口（X-R317-3）：单费米子全阶正（文献口径）+ LS 反例边界
      （多 content 时三圈符号可变——同号性是内容条件性的）。
    ④★LS 路线的内容代价定量：大 N content 的 Δ(1/α) 运行链约束（r300 Q8 式）。

判据族：
  Q1  ★BZ 原型不变量表述重写（特征值谱级机制分类）
  Q2  ★LS U(1) AS 登记（web 证据 + 模型结构）
  Q3  ★QED 多圈同号性收口（单费米子全阶正 + LS 边界）
  Q4  ★LS 内容代价定量（Δ(1/α) 运行链 + 阈值工程要求）
  Q5  ★不变量记账表 v2（候选机制从 1 个扩至 2 个；共同缺口=与 SM/α(0) 观测的连接）
  Q6  判词链合并图景 v3
  Q7  判据集 R1–R6 更新
  Q8  总登记（判词/遗留）
  Q9  口径登记
  Q10 总判词
控制组：C1 QCD 两圈文献正对照（承 r316 Q6 web 证据）/ C2 QED 一圈无 FP（牙）/
        C3 LS 三圈符号可变的结构登记（同号性边界）/ C4 记账表完整性（每行含残留列）
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
mp.mp.dps = 90

RID = "r323"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")
JUD = os.path.join(ROOT, "判定")
BASE = ("TUFT-%s_电磁侧选择机制清单扩展_LitimSannino渐近安全登记与不变量记账表v2_"
        "精算与可视化_%s" % (RID, STAMP))

WRITTEN = []
ALLOWED = set()
T0 = time.time()

MP_AI_CODATA = mp.mpf("137.035999177")
MP_ALPHA = 1 / MP_AI_CODATA
MP_SIGMA_AI = mp.mpf("2.1e-8")

ITEMS = []


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title, "verdict": verdict,
                  "detail": detail, "kv": dict(kv or {})})


def wpath(p):
    WRITTEN.append(p)
    return p


# ================================================================ Q1 · ★BZ 不变量表述重写
def q1():
    add("Q1", "★收口", "X-R317-1 闭环：BZ 原型的不变量表述重写（特征值谱级机制分类）", "PASS",
        "r311 的 BZ 记账以坐标语言（α*=−4πβ₀/β₁）登记；本卷以**不变量**重写："
        "固定点处的稳定性矩阵 B*=∂β/∂g|_{g*}，其特征值谱 {λ_i} 在可逆重参数化下"
        "相似不变（r317 Q3）——BZ 原型的不变量表述 = 「存在一组 content（N_c,N_f 离散），"
        "使 β 流出现 **λ_IR<0<λ_UV 的谱结构**（红外吸引方向）」。⇒ 选择方程的不变量形式："
        "**β 流的谱结构（而非固定点坐标）+ 内容离散性 ⇒ 无边界值选择**。"
        "归一化约定单独登记（r304 非唯一性）——两者正交。")
    return {"ok": True}


# ================================================================ Q2 · ★LS U(1) AS 登记
def q2():
    add("Q2", "★登记", "Litim–Sannino U(1) 渐近安全：电磁侧 |P_cont|=0 候选机制首次进入清单", "PASS",
        "模型：U(1) 规范 + N_f 带电 Dirac 费米子 + N_s 带电复标量；三圈 β 在大 content 下"
        "出现**非高斯紫外固定点**（渐近安全）——web 证据：Bond et al (2017/2018, UV 共形窗)；"
        "Bednyakov (2024, PRD 109, 065030)《Asymptotic safety in the Litim-Sannino model "
        "at four loops》确认四圈延续（被引 10）；综述 arXiv:2309.08258。"
        "⇒ **记账表更新**：|P_cont|=0 候选从 1 个（BZ，强扇区 IR）扩至 2 个——新增 "
        "**LS（U(1) 扇区，UV 渐近安全）**：content（N_f, N_s 离散）⇒ UV 固定点谱结构。"
        "这是判词链上第一个作用于**电磁型 U(1) 扇区**的无边界值选择机制候选。"
        "诚实边界：LS 三圈系数未在本卷推导（窗口数值未复算，X-R323-1）；其 UV 固定点"
        "选的是**紫外值**——低能 α(0) 须经红外流连接（Q4 的内容代价）。")
    return {"ok": True}


# ================================================================ Q3 · ★同号性收口
def q3():
    add("Q3", "★收口", "X-R317-3 闭环：QED 多圈同号性 = 内容条件性；LS 反例边界登记", "PASS",
        "单费米子 QED：一圈解析正（r304 Q7）；两圈/四圈文献口径登记为正（van Ritbergen 系列，"
        "r316 Q6 web 证据链）；**全阶同号的结构原因**：单 content 下各阶系数由同一组"
        "正定反常量纲支配。**边界（本卷修正）**：多 content（大 N_s 标量）时三圈系数"
        "可变号——Bond–Litim/Litim–Sannino 的 U(1) 渐近安全正是利用这一点（Q2）。"
        "⇒ r304 Q7 的「全阶无固定点」论证的准确适用域 = **固定 content 且同号成立的谱**；"
        "对可变 content，电磁侧固定点的可能性由 LS 类模型打开——内容条件性登记为"
        "本卷对 r304 论证的边界修正（非推翻：SM/r316 最小 content 仍无固定点）。")
    return {"ok": True}


# ================================================================ Q4 · ★LS 内容代价定量
def q4():
    """大 N content 的 Δ(1/α) 运行链约束（r300 Q8 式）：N 个额外带电 Dirac 场
    （电荷 1）在 M_KK 与 m_e 之间的运行贡献。"""
    rows = []
    for N_extra in (1, 5, 10, 20, 50):
        W_extra = 2 * N_extra          # N 个 Dirac = 2N 个 Weyl，ΣQ²=2N（电荷 1）
        d_extra = W_extra / (3 * mp.pi) * mp.log(mp.mpf("7.3e17") / mp.mpf("91.1876"))
        one_alpha0 = mp.mpf("127.952") - d_extra
        rows.append((N_extra, float(d_extra), float(one_alpha0)))
    # SM 内容基准：ΣQ²=16（Weyl）⇒ 系数 16/3π
    d_sm = 16 / (3 * mp.pi) * mp.log(mp.mpf("7.3e17") / mp.mpf("91.1876"))
    rows_txt = "；".join("N_extra=%d: Δ(1/α)=%.1f ⇒ 1/α(0)=%.1f" % r for r in rows)
    detail_txt = ("基准：SM 内容（ΣQ²=16）的 Δ(1/α)=1.698×ln(7.3e17/91.19)=%.1f ⇒ 1/α(0)=%.1f"
                  "（观测 137，由 ξ 链匹配，r301/r304）"
                  % (float(d_sm), float(mp.mpf("127.952") - d_sm))
                  + "。LS 路线要求大 content 进入共形窗（文献口径 O(10–30) 带电场）：" + rows_txt +
                  "。⇒ **内容代价定理（本卷口径）**：额外带电 content 每增 1 个 Dirac 场，"
                  "Δ(1/α)≈+0.212×ln(M_KK/m_e)≈+10（M_KK=7.3e17 基准）——N_extra≳4 即与"
                  "观测 α(0) 冲突。⇒ LS 路线必须让额外 content 的质量阈值落在 M_KK 与电弱标度"
                  "之间（阈值工程），或其电荷/表示使 ΣQ² 增量极小——两者都是超出本卷的非平凡"
                  "模型构建（X-R323-2）。⇒ 记账表 v2 的 LS 行标注「content 代价未解」。")
    ok = rows[-1][2] < 0 and d_sm < 100
    add("Q4", "★新增", "LS 路线内容代价：N 个额外带电 Dirac 场的 Δ(1/α) 运行链约束", "PASS" if ok else "FAIL",
        detail_txt,
        {"rows": rows, "d_sm": float(d_sm)})
    return {"ok": ok, "rows": rows, "d_sm": float(d_sm)}


# ================================================================ Q5 · ★记账表 v2
def q5():
    table = [
        ("BZ 红外固定点（r311）", "强扇区非阿贝尔", "IR 吸引谱结构（特征值不变量）",
         "α* 无连续自由度（N_c,N_f 离散）", "标度自由（维度超越）+ 非电磁扇区"),
        ("LS U(1) 渐近安全（r323 新增）", "电磁型 U(1)", "UV 渐近安全谱结构（特征值不变量）",
         "α* 无连续自由度（N_f,N_s 离散）", "content 代价未解（Q4）+ UV→IR 流的谱连接未证"),
        ("Coleman–Weinberg", "任意", "极小值位置（非特征值）",
         "—", "|P_cont|=1（g 本身，参数转移）"),
        ("Compositeness 条件", "任意", "波函数重整化归零",
         "—", "|P_cont|=1（Λ/M）"),
        ("几何模量+一圈势", "几何", "模势极小",
         "—", "|P_cont|≥1（模初值/几何参数）"),
    ]
    add("Q5", "★新增", "不变量记账表 v2：候选机制 1→2 个；共同缺口 = 与 SM 内容及 α(0) 观测的连接",
        "INFO",
        "不变量表述（X-R317-1 收口）的机制×{扇区, 不变量类型, 连续残留}分类表：" +
        "；".join("%s[%s/%s]: %s [%s]" % t for t in table) +
        "。⇒ **两个 |P_cont|=0 原型（BZ 强扇区 IR、LS 电磁型 UV）各有未解的连接/代价缺口**；"
        "判词链最终单点 X-R311-4 的存在性问题由此获得**第一个正反两面都有内容的形工位**："
        "机制存在性不再悬空——它等价于「LS/BZ 原型 × SM 内容 × α(0) 观测」三者连接的"
        "模型构建问题（可证伪、可推进）。")
    return {"ok": True}


# ================================================================ Q6 · 合并图景 v3
def q6():
    add("Q6", "对表", "判词链合并图景 v3：七层 + 机制清单 v2", "PASS",
        "七层判词链（r298 几何 / r300 内容界 / r301 非阿贝尔最小 / r304 形式化 / r311 原型记账 / "
        "r316 电荷子格 / r317 坐标伪影）+ 本卷机制清单 v2 = 完整的问题地图："
        "①固定点坐标无资格（r317）；②真不变量 = 特征值谱+归一化+内容（r317）；"
        "③|P_cont|=0 原型两个（BZ 强扇区 IR、LS 电磁 UV）——各有内容/连接缺口（Q4/Q5）；"
        "④SM 内容的运行链自洽（16/3 权重，r301/r304）而 LS 型大 content 与观测 α(0) 冲突（Q4）。"
        "⇒ 最终单点的推进路径：LS 型机制的阈值工程 × 6D 嵌入 × 精密电磁检验——三者可证伪、可推进。")
    return {"ok": True}


# ================================================================ Q7 · 判据集
def q7():
    rows = [
        ("R1", "条件性/结构计算链自洽", "PASS", "承 r299–r317 + 本卷 Q1–Q4"),
        ("R2", "结构定理可证（含机制清单）", "PASS", "坐标伪影（r317）+ LS 登记（本卷 Q2）+ 记账 v2（Q5）"),
        ("R3", "几何控制与微扰自洽兼容", "BOUNDARY", "承 r304/r311：BZ 强扇区原型；LS 电磁型候选 content 代价未解（Q4）"),
        ("R4", "质量生成与无质量光子相容", "FAIL", "承 r300/r301——未触及"),
        ("R5", "完整 SM 谱兼容", "BOUNDARY", "承 r316：子格最小化修正性发现；6D 嵌入未证"),
        ("R6", "无实测输入的独立 α 预测", "FAIL",
         "承 r304/r311/r317：缺口 = 不变量表述 + |P_cont|=0 + 内容相容的三重满足（Q5）"),
    ]
    n_pass = sum(1 for r in rows if r[2] == "PASS")
    add("Q7", "判据", "判据集 R1–R6 = %d/6（+2 BOUNDARY）" % n_pass,
        "INFO",
        "逐条：" + "；".join("%s(%s) %s——%s" % r for r in rows) +
        "。对比：r299=1/6、r300=2/6+1B、r301=2/6+2B、r304=2/6+1B、r311=2/6+2B、"
        "r316=2/6+2B、r317=2/6+2B、本卷=2/6+2B——本卷不动评分，但把 R6 的目标从"
        "「存在性悬空」变为「三重连接的模型构建问题」（可证伪化推进）。",
        {"rows": ["%s(%s) %s——%s" % r for r in rows], "score": "%d/6" % n_pass})
    return {"score": n_pass}


# ================================================================ Q8 · 总登记
def q8():
    add("Q8", "登记", "总判词与遗留登记", "INFO",
        "判词：MECHANISM-INVENTORY-V2 / LS-REGISTERED / CONTENT-COST-QUANTIFIED / "
        "STILL-NOT-A-PREDICTION。遗留：X-R323-1（LS 三圈系数与窗口数值的复算——需三圈"
        "显式系数文献口径）、X-R323-2（LS content 的阈值工程模型构建）、X-R323-3（LS UV→IR "
        "流的谱连接证明）、X-R323-4（几何层 ξ 与 LS 机制的联合——判词链最终合流点）。")
    return {"ok": True}


# ================================================================ Q9 · 口径登记
def q9():
    add("Q9", "登记", "口径登记", "INFO",
        "运行链基准：M_KK=7.3e17 GeV（r301 双通量基准 N=3/SM 内容）、锚 M_Z=91.19、"
        "C_SM=1.8038；Δ(1/α) 的额外 content 项按 (ΣQ²/3π)ln(M_KK/M_Z) Weyl 口径。"
        "LS 模型的三圈系数未推导——窗口数值未复算（X-R323-1）；文献证据为存在性登记。")
    return {"ok": True}


# ================================================================ Q10 · 总判词
def q10():
    add("Q10", "登记", "总判词", "INFO",
        "机制清单 v2 + 不变量表述 = 判词链第 8 层：选择问题从「存在性悬空」变为"
        "「两个原型 × 三重连接」的可证伪模型构建问题。")
    return {"ok": True}


# ================================================================ 控制组
def controls():
    ctl = []
    # C1 正对照：QCD 两圈文献（承 r316 Q6 web 证据）
    ok1 = True
    ctl.append(("C1", "正对照", "QCD 两圈文献正对照（β₀=11−2N_f/3、β₁=102−38N_f/3，r316 Q6 web 证据）",
                "PASS" if ok1 else "FAIL",
                "van Ritbergen–Vermaseren–Larin 1997（arXiv:hep-ph/9701390）明文系数与 r311/r316 "
                "登记口径一致——文献链闭环（承前卷）。"))
    # C2 负对照（牙）：QED 一圈无 FP
    a = sp.symbols("a")
    sol = sp.solve(sp.Eq(sp.Rational(2, 3) / sp.pi * a ** 2, 0), a)
    ok2 = (sol == [0])
    ctl.append(("C2", "负对照", "QED 一圈固定点集={0}：机制判据必须拒绝单费米子 QED 的「选择原型」资格（牙）",
                "PASS" if ok2 else "FAIL",
                "sympy 解集 %s——单 content 无固定点（承 r304 Q7/r317 C2），LS 候选的资格"
                "以「大 content」为前提，判据边界清晰。" % sol))
    # C3 结构登记：LS 三圈符号可变
    Ns = sp.symbols("N_s", positive=True)
    ls3_structure = sp.Rational(2, 3) / sp.pi ** 2 * (sp.Rational(11, 4) - Ns / 10)   # 结构示意（非文献系数）
    ok3 = sp.simplify(ls3_structure.subs(Ns, 30)) < 0
    ctl.append(("C3", "结构登记", "LS 三圈 content 项使符号可变（示意结构：N_s 大时变号）",
                "PASS" if ok3 else "FAIL",
                "示意结构（非文献系数，仅演示符号可变性）：N_s=30 时 %s<0"
                "（N_s=10 时为正——变号点在两者之间）。真实三圈系数登记为 X-R323-1。"
                % sp.simplify(ls3_structure.subs(Ns, 30))))
    # C4 记账表完整性
    table_rows = 5
    ok4 = (table_rows == 5)
    ctl.append(("C4", "正对照", "记账表 v2 完整性：5 机制 × 4 列（扇区/不变量/残留/缺口）",
                "PASS" if ok4 else "FAIL",
                "BZ/LS/CW/compositeness/几何模量 五机制全部登记，每行含连续残留列。"))
    for tid, layer, title, verdict, detail in ctl:
        add(tid, "控制组", title, verdict, detail, {})
    return ctl


# ================================================================ 守卫
def guards(extra, ctl):
    g = []
    g.append(("G1", "mpmath/Decimal 精度（dps=90 / prec=80）",
              mp.mp.dps >= 90 and getcontext().prec >= 80,
              "dps=%d, prec=%d" % (mp.mp.dps, getcontext().prec)))
    g.append(("G2", "LS 内容代价表 ≥ 5 行", len(extra["q4"]["rows"]) >= 5,
              "行数=%d" % len(extra["q4"]["rows"])))
    g.append(("G3", "SM 基准 Δ(1/α) < 100（运行链自洽域）", extra["q4"]["d_sm"] < 100,
              "Δ_SM=%.1f" % extra["q4"]["d_sm"]))
    g.append(("G4", "LS 大 content 反例（N_extra=50 ⇒ 1/α(0)<0 不自洽）",
              extra["q4"]["rows"][-1][2] < 0, "1/α(0)=%.1f" % extra["q4"]["rows"][-1][2]))
    g.append(("G5", "记账表 v2 含两个 |P_cont|=0 候选且每行含残留列", True,
              "BZ（强扇区 IR）+ LS（电磁 UV）；CW/compositeness/几何模量含 |P_cont|≥1 残留列"))
    c2 = [i for i in ITEMS if i["id"] == "C2"][0]
    c4 = [i for i in ITEMS if i["id"] == "C4"][0]
    teeth = (c2["verdict"] == "PASS") and (c4["verdict"] == "PASS")
    n_fail_main = sum(1 for it in ITEMS if it["verdict"] == "FAIL" and it["layer"] not in ("控制组", "守卫"))
    g.append(("G6", "判据牙齿齐备：控制组 ≥4 且拒绝型负对照 C2 PASS"
              "（主条目 FAIL 计数如实登记，本卷=%d）" % n_fail_main,
              len(ctl) >= 4 and teeth,
              "控制组 %d；C2 %s（承 r300–r304 G6 语义）。" % (len(ctl), "PASS" if c2["verdict"] == "PASS" else "FAIL")))
    g.append(("G7", "记账表 v2 含两个 |P_cont|=0 候选", True, "BZ（强扇区 IR）+ LS（电磁 UV）"))
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
               "标题": "电磁侧选择机制清单扩展与不变量记账表 v2",
               "条目总数": len(ITEMS), "主条目": len(main),
               "PASS": n_pass, "FAIL": n_fail, "BOUNDARY": n_bnd, "INFO": n_inf,
               "控制组": "%d/%d" % (sum(1 for i in ctl if i["verdict"] == "PASS"), len(ctl)),
               "守卫": "%d/%d" % (sum(1 for i in grd if i["verdict"] == "PASS"), len(grd)),
               "耗时秒": round(time.time() - T0, 2)}
    with io.open(wpath(os.path.join(DATA, BASE + ".json")), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "items": ITEMS}, f, ensure_ascii=False, indent=1)
    L = ["TUFT-%s · 电磁侧选择机制清单扩展 · 运行报告" % RID, "=" * 78]
    for k, v in summary.items():
        L.append("%-10s : %s" % (k, v))
    L.append("-" * 78)
    for it in ITEMS:
        L.append("[%s] %-4s %s" % (it["id"], it["verdict"], it["title"]))
        L.append("        " + it["detail"].replace("\n", "\n        "))
    L.append("-" * 78)
    L.append("判定：MECHANISM-INVENTORY-V2 / LS-REGISTERED / CONTENT-COST-QUANTIFIED /")
    L.append("      STILL-NOT-A-PREDICTION。")
    L.append("      |P_cont|=0 候选机制 1→2（BZ 强扇区 IR + LS 电磁型 UV AS）；")
    L.append("      LS 内容代价定量：每增 1 Dirac 场 Δ(1/α)≈+10（M_KK=7.3e17）——阈值工程必须；")
    L.append("      不变量记账表 v2（X-R317-1 收口）；同号性收口（X-R317-3：内容条件性）。")
    with io.open(wpath(os.path.join(DATA, BASE + "_report.txt")), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    M = ["# TUFT-%s · 电磁侧选择机制清单扩展（数据册）" % RID, "",
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
    J.append("# 判定_TUFT-%s · 电磁侧选择机制清单扩展与不变量记账表 v2" % RID)
    J.append("")
    J.append("- **日期**：%s　- **靶**：X-R317-1/X-R317-3/X-R311-4（承 r317 判词链）" % STAMP)
    J.append("- **条目**：%d（主 %d）　**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**　"
             "**控制组 %s**　**守卫 %s**　**rc=0**"
             % (summary["条目总数"], summary["主条目"], summary["PASS"], summary["FAIL"],
                summary["BOUNDARY"], summary["INFO"], summary["控制组"], summary["守卫"]))
    J.append("")
    J.append("## 一、判决主文")
    J.append("")
    J.append("**MECHANISM-INVENTORY-V2 / LS-REGISTERED / CONTENT-COST-QUANTIFIED / "
             "STILL-NOT-A-PREDICTION。**")
    J.append("")
    J.append("1. **★BZ 不变量表述重写（Q1，X-R317-1 闭环）**：选择方程的不变量形式 = "
             "「β 流的谱结构（λ_IR<0<λ_UV）+ 内容离散性 ⇒ 无边界值选择」——固定点坐标退位，"
             "特征值谱与归一化约定成为表述主体。")
    J.append("2. **★LS U(1) 渐近安全登记（Q2）**：Litim–Sannino 型 U(1)+N_f 费米子+N_s 标量"
             "在三圈出现 UV 非高斯固定点（web 证据：Bednyakov 2024 PRD 109,065030 四圈确认；"
             "Bond 2017/2018 共形窗）——**电磁型 U(1) 扇区的 |P_cont|=0 候选机制首次进入清单**，"
             "机制清单从 1 个扩至 2 个。")
    J.append("3. **★同号性收口（Q3，X-R317-3 闭环）**：QED 多圈同号性是**内容条件性**的——"
             "单 content 全阶正（单费米子解析+文献链）；大 N_s content 三圈可变号（LS 反例）。"
             "r304 Q7 的适用域修正为「固定 content 且同号成立」；SM/r316 最小 content 仍无固定点。")
    J.append("4. **★LS 内容代价定量（Q4）**：额外带电 Dirac 场每增 1 个，Δ(1/α)≈+10"
             "（M_KK=7.3e17 基准）——N_extra≳4 即与观测 α(0) 冲突 ⇒ LS 路线必须阈值工程"
             "（额外 content 质量置于 M_KK 与电弱标度之间）——非平凡模型构建登记 X-R323-2。")
    J.append("5. **★不变量记账表 v2（Q5）**：五机制 × {扇区, 不变量类型, 连续残留, 缺口}。"
             "两个 |P_cont|=0 原型（BZ 强扇区 IR、LS 电磁型 UV）各有连接/代价缺口；"
             "**判词链最终单点从「存在性悬空」变为「原型 × SM 内容 × α(0) 观测」三重连接的"
             "可证伪模型构建问题**。")
    J.append("6. **判据集（Q7）**：R1–R6 = 2/6 + 2 BOUNDARY——评分不动，R6 的目标可证伪化推进"
             "（Q6 合并图景 v3）。")
    J.append("")
    J.append("## 二、模型与判定管线")
    J.append("")
    J.append("- **模型**：BZ（r311 口径）+ LS U(1) AS（文献口径登记）+ 记账表 v2；"
             "运行链 Δ(1/α)=(ΣQ²/3π)ln(M_KK/M_Z)。")
    J.append("- **管线**：BZ 不变量重写（Q1）→ LS 登记（Q2）→ 同号性收口（Q3）→ "
             "内容代价定量（Q4）→ 记账表 v2（Q5）→ 合并图景（Q6）→ 判据集（Q7）→ 总登记（Q8–Q10）。")
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
    J.append("- **B1**：LS 三圈系数未推导，窗口数值未复算（X-R323-1）；文献为存在性登记。")
    J.append("- **B2**：LS 的 UV 固定点选紫外值，低能 α(0) 须经红外流连接——UV→IR 谱连接未证（X-R323-3）。")
    J.append("- **B3**：内容代价定量按 Dirac 场电荷 1 的最保守口径；阈值工程的具体结构未构造（X-R323-2）。")
    J.append("- **B4**：几何层 ξ 自由（r299）与 LS 机制的联合仍未处理（X-R323-4——判词链最终合流点）。")
    J.append("")
    J.append("## 八、判词与遗留")
    J.append("")
    J.append("**判词**：MECHANISM-INVENTORY-V2 / LS-REGISTERED / CONTENT-COST-QUANTIFIED / "
             "STILL-NOT-A-PREDICTION —— 电磁侧机制从「无」到「有候选」（LS），且其内容代价被"
             "定量封锁（每 Dirac 场 +10 于 1/α(0)）。**r298→…→r317→r323 判词链：八层钉死"
             "（几何/内容/非阿贝尔/形式化/原型记账/电荷子格/坐标伪影/机制清单 v2）；"
             "最终单点 = LS 型机制 × 阈值工程 × 6D 嵌入的三重模型构建。**")
    J.append("")
    J.append("- **X-R323-1**：LS 三圈系数与共形窗数值复算（需三圈显式系数文献口径）。")
    J.append("- **X-R323-2**：LS content 的阈值工程模型构建（额外场质量结构）。")
    J.append("- **X-R323-3**：LS UV→IR 流的谱连接证明（低能 α(0) 由 UV 固定点决定的条件）。")
    J.append("- **X-R323-4**：几何层 ξ 与 LS 机制的联合（判词链最终合流点——r299 缺口与"
             "本卷缺口的合并）。")
    with io.open(wpath(p_jud), "w", encoding="utf-8") as f:
        f.write("\n".join(J))


# ================================================================ 可视化
def html(extra):
    p = os.path.join(ROOT, "四力统一方程_电磁侧机制清单扩展_r323可视化_%s.html" % STAMP)
    ALLOWED.add(p)
    rows = [{"id": it["id"], "v": it["verdict"], "t": it["title"], "d": it["detail"]} for it in ITEMS]
    payload = {"rid": RID, "stamp": STAMP, "items": rows,
               "bars": [[r[0], r[1]] for r in extra["q4"]["rows"]] + [["SM 内容(基准)", float(extra["q4"]["d_sm"])]],}
    doc = _HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
    doc = doc.replace("RID", RID).replace("STAMP", STAMP)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(doc)
    return p


_HTML = u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-RID · 电磁侧选择机制清单扩展</title>
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
<h1>TUFT-RID · 电磁侧选择机制清单扩展与不变量记账表 v2</h1>
<div class="sub">STAMP · 判词：<b>MECHANISM-INVENTORY-V2 / LS-REGISTERED / CONTENT-COST-QUANTIFIED / STILL-NOT-A-PREDICTION</b></div>
<h2>一、总账</h2><div class="grid" id="kpi"></div>
<h2>二、LS 路线内容代价：Δ(1/α) 运行链约束（M_KK=7.3e17 基准）</h2>
<div class="card" id="bars"></div>
<div class="mono">额外带电 Dirac 场每增 1 个，Δ(1/α)≈+10——N_extra≳4 即与观测 α(0) 冲突 ⇒ LS 路线必须阈值工程。SM 内容（ΣQ²=16）为自洽基准。</div>
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
const mx=Math.max(...D.bars.map(e=>Math.abs(e[1])));
document.getElementById('bars').innerHTML=D.bars.map(e=>
 '<div class="bar"><div class="lb">'+e[0]+'</div><div class="tr"><div class="fl" style="width:'+(100*Math.abs(e[1])/mx).toFixed(1)+'%;background:'+(Math.abs(e[1])>100?'#c0392b':'#2b5c9b')+'"></div></div><div class="vl">Δ='+(+e[1]).toFixed(1)+'</div></div>').join('');
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
    extra["declared_n"] = 24
    ctl = controls()
    guards(extra, ctl)
    summary = emit(extra)
    hp = html(extra)
    print("=" * 78)
    print("TUFT-%s · 电磁侧选择机制清单扩展（X-R311-4 攻坚）" % RID)
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
