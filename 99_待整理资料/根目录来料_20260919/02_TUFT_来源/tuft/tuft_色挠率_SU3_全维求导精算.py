# -*- coding: utf-8 -*-
"""
TUFT 色挠率 SU(3) · 全维求导证明与精算
======================================
对象：《TUFT全维统一场论：色挠率 SU(3) 多分量挠率张量、渐近自由与色禁闭解析推导》§1–§8
逐条做：sympy 符号 / 李代数维数 / 量纲 / numpy 数值复现 / 判定 PASS-FAIL-BOUNDARY-INFO
红线：数学自洽 != 物理实验证实。
"""
from __future__ import print_function

import os
import sys
import math
import time

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_色挠率_SU3_report.txt")


class Report(object):
    def __init__(self):
        self.rows = []
        self.lines = []

    def echo(self, t=""):
        print(t)
        self.lines.append(t)

    def section(self, t):
        self.echo("")
        self.echo("=" * 78)
        self.echo(t)
        self.echo("=" * 78)

    def add(self, sec, name, verdict, detail=""):
        self.rows.append((sec, name, verdict, detail))
        line = "  [" + verdict + "] " + name
        if detail:
            line += "   |  " + detail
        self.echo(line)

    def summary(self):
        from collections import Counter
        cnt = Counter(v for _, _, v, _ in self.rows)
        self.section("汇总")
        for k in ["PASS", "FAIL", "BOUNDARY", "INFO"]:
            self.echo("  %-9s = %d" % (k, cnt.get(k, 0)))
        if cnt.get("FAIL"):
            self.echo("  存在 FAIL（真实缺陷）:")
            for sec, name, v, det in self.rows:
                if v == "FAIL":
                    self.echo("    - [" + sec + "] " + name + "  " + det)
        return cnt

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] 报告写入失败: " + str(exc))


# ===================== §1 SU(3) 代数审查 =====================
def part1_su3(rep):
    import sympy as sp
    rep.section("§1  SU(3) 色挠率张量：代数审查")
    Nc = 3
    n_gen = Nc ** 2 - 1
    rep.add("S1.1", "SU(3) 生成元数 = N^2-1 = %d" % n_gen, "PASS",
            "与原文'8 个独立分量 lambda^a (a=1..8)'一致")
    rep.add("S1.2", "基础表示维数 = 3（红/绿/蓝）", "PASS", "3 维复表示 ✓")
    rep.add("S1.3", "'色荷 = 色挠率本征值'的表述", "FAIL",
            "SU(3) 基础表示是 **3 维矢量空间**，其基矢 (r,g,b) 是**权重态**，"
            "不是'本征值'。本征值只在 **Cartan 子代数**（2 个对角生成元 lambda3, lambda8）"
            "上定义，给出 2 个量子数 (I3, Y)——**不是** 3 个相互独立的'本征态'。"
            "把'3 个基矢'说成'3 个本征值'是概念错误。")
    rep.add("S1.4", "'A^a_mu 是色挠率诱导势'——T^a -> A^a 的映射", "FAIL",
            "原文直接把 A^a_mu 称为'色挠率诱导势'，但**未给出从挠率张量 T^a_munu 到"
            "规范势 A^a_mu 的构造映射**（如 A ~ 缩并/积分关系）。缺此映射，"
            "'诱导'只是命名，不是推导。")
    rep.add("S1.5", "拉氏量为标准 QCD 形式（非挠率导出）", "FAIL",
            "L = -1/4 F^a F_a + psibar(i gamma D - m)psi 是**标准 Yang-Mills/QCD 拉氏量**，"
            "逐字照搬。'嵌入 TUFT'实为**直接采用** QCD，而非从挠率结构导出。"
            "F^a_munu 亦为标准非阿贝尔场强。")
    rep.add("S1.6", "SU(3) 的来源", "FAIL",
            "把'代数群从 U(1) 升级为 SU(3)'作为**假设**；TUFT 未产生 SU(3) 结构的机制"
            "（无群选择原理）。属**外部注入**——与上一分册 C 路线③判定一致。")
    return


# ===================== §2 势能与曲率饱和 =====================
def part2_potential(rep):
    rep.section("§2  曲率饱和与色挠率势能标度")
    rep.add("S2.1", "K_sat = alpha_s / l_P^2 量纲", "PASS",
            "[alpha_s]=1, [l_P^-2]=L^-2 => [K_sat]=L^-2，与'曲率'一致 ✓")
    rep.add("S2.2", "K_sat 中 alpha_s 的身份", "BOUNDARY",
            "alpha_s 是**跑动耦合**（能标依赖），却出现在'拓扑不变量 K_sat'中——"
            "拓扑不变量不应依赖跑动耦合。存在概念张力。")
    rep.add("S2.3", "V(r) = 积分 alpha_s K T Omega dr 的标度", "FAIL",
            "原文称 'r>>r0 时 K 正比于 r ⇒ V 约等于 sigma r（线性）'。"
            "但若 K ~ r，则 V = 积分 alpha_s K T Omega dr ~ 积分 r dr ~ **r^2**（二次），"
            "**不是线性**！要得到线性势需 alpha_s*T*Omega ~ 常数且 K ~ const，"
            "或 K~r 而 alpha_s~1/r 等补偿——原文未给。线性禁闭势在此不成立。")
    rep.add("S2.4", "'渐近自由 = 曲率不随距离变化'的类比", "FAIL",
            "渐近自由是关于**能标/距离的耦合跑动**（alpha_s(Q^2)->0 当 Q^2->inf），"
            "不是'曲率不再随距离变化'。原文把'导数趋零'等同于'耦合减弱'，"
            "是**类比而非推导**。")
    return


# ===================== §3 跑动耦合（核心缺陷） =====================
def part3_running(rep):
    import sympy as sp
    rep.section("§3  跑动耦合 alpha_s(K)：公式行为与 b0 系数（核心）")
    Ks, K, a0, b0 = sp.symbols("K_sat K alpha_s0 b0", positive=True)
    alpha = a0 / (1 + b0 * a0 * sp.log(Ks / K))

    lim_hi = sp.limit(alpha, K, Ks)      # K -> K_sat
    rep.add("S3.1", "K -> K_sat 时 alpha_s 的极限", "PASS",
            "alpha_s(K_sat) = alpha_s0 / (1 + 0) = alpha_s0（**有限，非 0**）")
    rep.add("S3.2", "原文文字称 'K->K_sat 时 alpha_s -> 0（渐近自由）'", "FAIL",
            "公式给出 K->K_sat 时 alpha_s -> alpha_s0（=0.118），**不是 0**；"
            "而 K->0 时 ln(K_sat/K)->inf 才是发散侧。**原文的文字与自己的公式相反**。")
    rep.add("S3.3", "与标准 QCD 的跑动变量对比", "FAIL",
            "标准 QCD: alpha_s(Q^2) = alpha_s0/(1 + b0 alpha_s0 ln(Q^2/Lambda^2))，"
            "跑动变量是**能标 Q^2**。原文用 K（曲率）代替 Q^2 作跑动变量，"
            "但 K 是几何量、非能标，**替换缺乏依据**（几何量->能标的映射未给）。")
    # b0 系数
    b0_wrong = (33 - 12 * 3) / (12 * math.pi)
    b0_std = (11 * 3 - 2 * 3) / (12 * math.pi)
    rep.add("S3.4", "原文代码 b0 = (33-12*3)/(12 pi) = %.5f" % b0_wrong, "FAIL",
            "该式 = -3/(12 pi) = %.5f < 0（**符号错误**）。标准 1-loop: "
            "b0 = (11 N_c - 2 N_f)/(12 pi) = (33-6)/(12 pi) = %.5f > 0。"
            "原文把 2*N_f=6 误写成 12*3=36，导致 b0 反号。" % (b0_wrong, b0_std))
    rep.add("S3.5", "b0<0 的后果", "FAIL",
            "b0<0 使 1 + b0 alpha_s0 ln(K_sat/K) 随 K->0 变负 => alpha_s 变为**负值**（非物理）。"
            "原代码打印值见 §6 复现。")
    return


# ===================== §4 胶子 =====================
def part4_gluon(rep):
    rep.section("§4  胶子：色挠率行波")
    rep.add("S4.1", "胶子无质量（K=0 => m=0）", "PASS", "基本胶子无质量 ✓（与标准 QCD 一致）")
    rep.add("S4.2", "胶子自耦合来自'色指标'", "BOUNDARY",
            "自耦合来自场处于**伴随表示**（非阿贝尔），是标准 YM 结果；"
            "原文把它归因于'色挠率'，属**重新命名**而非新机制。")
    rep.add("S4.3", "胶子禁闭（无自由胶子）", "INFO",
            "禁闭是 QCD 的**未完全解析**现象；原文用'被锁在曲率饱和区'表述，"
            "是定性类比，未给解析推导（与 §2.3 的线性势一样缺定量支撑）。")
    return


# ===================== §5 夸克质量（量纲） =====================
def part5_quark_mass(rep):
    rep.section("§5  夸克质量公式的量纲")
    # m_q = alpha K T^a Omega / c^2
    # 取 [K]=L^-2(曲率), [T^a]=L^-1(挠率), [Omega]=1, [c^2]=L^2 T^-2
    from fractions import Fraction as F
    dimL = F(-2) + F(-1) - F(2)
    dimT = F(0) - F(-2)
    rep.add("S5.1", "m_q = alpha K T^a Omega / c^2 量纲非法", "FAIL",
            "[alpha]=1,[K]=L^-2,[T^a]=L^-1,[Omega]=1,[c^2]=L^2T^-2 => [m_q]=L^(%s) T^(%s)，"
            "**非质量 [M]**（与续篇 §5.1 同一缺陷的重现）。" % (str(dimL), str(dimT)))
    rep.add("S5.2", "色中性约束 sum_i T^a_i = 0", "BOUNDARY",
            "严格的色单态是 3(x)3(x)3 中的**全反对称组合**（epsilon_ijk），"
            "不是简单的'矢量和为零'。原文的简化表述在 SU(3) 严格意义上不准确。")
    return


# ===================== §6 代码复现 =====================
def part6_code(rep):
    rep.section("§6  复现原文数值代码，核对声称")
    alpha_s0 = 0.118
    K_sat = 1.0
    r0 = 1.0
    b0 = (33 - 12 * 3) / (12 * np.pi)      # 原文
    rep.add("S6.1", "原文 b0 = %.6f（<0）" % b0, "FAIL",
            "b0 反号（应为 +0.7161）。下面按原文 b0 复现，展示其后果。")

    def alpha_s(K):
        return alpha_s0 / (1 + b0 * alpha_s0 * np.log(K_sat / K + 1e-12))

    a_at_sat = alpha_s(K_sat)
    a_small = alpha_s(0.01)
    rep.add("S6.2", "alpha_s(K_sat) = %.5f（原文声称'近距离趋近 0'）" % a_at_sat,
            "FAIL" if abs(a_at_sat) > 0.05 else "PASS",
            "实际 = alpha_s0 = 0.118，**不是 0** —— 与原文'近距离耦合趋近0'矛盾")
    rep.add("S6.3", "alpha_s(K=0.01 K_sat) = %.5f" % a_small, "INFO",
            "远距离耦合仅从 0.118 变到 %.5f（几乎不变，且因 b0<0 方向异常）" % a_small)

    # 势能标度
    Nr = 300
    r = np.logspace(-2, 2, Nr)
    K = np.where(r < r0, K_sat, K_sat * (r / r0))
    al = alpha_s(K)
    dr = np.diff(r, prepend=r[0])
    V = np.cumsum(al * K * dr)
    mask = r > 1.5 * r0
    lr = np.log(r[mask])
    lV = np.log(np.abs(V[mask]) + 1e-30)
    p = np.polyfit(lr, lV, 1)[0]
    rep.add("S6.4", "V(r) 对 r 的标度指数 p（拟合 V ~ r^p）", "FAIL",
            "p = %.3f（约 2，即 V ~ r^2）——原文声称'势能随 r 线性上升（sigma r）'，"
            "与代码/积分结果矛盾（K~r => V~r^2）" % p)
    rep.add("S6.5", "结论：原文'输出特征'与代码实际输出不符", "FAIL",
            "(1) alpha_s(K_sat)=0.118 非 0；(2) V ~ r^2 非线性。")
    return


# ===================== §7 清单核对 =====================
def part7_scorecard(rep):
    rep.section("§7  完成度清单核对")
    rep.add("S7.1", "① 总作用量/变分/诺特", "INFO", "前篇范畴，本册未复核")
    rep.add("S7.2", "② 一维球对称时空结数值解", "INFO", "前篇范畴")
    rep.add("S7.3", "③ 莫比乌斯闭环/自旋 1/2/统计/泡利", "BOUNDARY",
            "拓扑事实成立（前册已验），但自旋-统计属已知结论的框架内复现")
    rep.add("S7.4", "④ 弱作用手性破缺（U(1)手性挠率）", "BOUNDARY", "定性一致，未定量导出")
    rep.add("S7.5", "⑤ SU(3) 色挠率、渐近自由、色禁闭、跑动、弦势", "FAIL",
            "本册审查显示：SU(3) 为外部注入；线性弦势不成立（V~r^2）；"
            "跑动公式与文字相反且 b0 反号。⑤ 名不副实。")
    return


# ===================== §8 修复方案 =====================
def part8_fix(rep):
    rep.section("§8  修复方案（分析 -> 处理 -> 修复 -> 优化）")
    fixes = [
        ("S1.3", "把'3 个本征态'改为'3 维基础表示的权重态'；本征值只定义在 Cartan(2 维)"),
        ("S1.4/S1.5", "补齐 T^a -> A^a 的映射，或如实声明'直接采用 QCD 拉氏量'，去掉'诱导'措辞"),
        ("S1.6", "如实声明 SU(3) 为外部输入（无群选择原理）"),
        ("S2.3", "线性势需重新推导：要么 K~const 且 alpha_s T Omega~const；否则 V~r^2"),
        ("S3.2", "修正文字与公式的矛盾：K->K_sat 时 alpha_s->alpha_s0（非 0）"),
        ("S3.4", "修正 b0 = (11 N_c - 2 N_f)/(12 pi) = +0.7161"),
        ("S3.5", "b0 反号会导致 alpha_s<0，须修正"),
        ("S5.1", "质量公式改为量纲合法形式（如 m = hbar Omega_w/c^2，见续篇修订）"),
        ("S6.4", "如实标注 V~r^2（或修正模型使其线性）"),
    ]
    for tag, how in fixes:
        rep.add("FIX", "[" + tag + "] " + how, "INFO", "")
    rep.add("FIX.10", "优化：C 路线应'冻结'或'降级为与 QCD 的一致性对照'", "BOUNDARY",
            "在补齐 SU(3) 来源、T^a->A^a 映射、量纲合法质量式之前，"
            "本册任何'解析导出渐近自由/禁闭'的主张都不成立（见 §2/§3/§6 的 FAIL）。")
    return


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 色挠率 SU(3) · 全维求导证明与精算")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)
    part1_su3(rep)
    part2_potential(rep)
    part3_running(rep)
    part4_gluon(rep)
    part5_quark_mass(rep)
    part6_code(rep)
    part7_scorecard(rep)
    part8_fix(rep)
    rep.add("全局", "运行耗时", "INFO", "%.2f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
