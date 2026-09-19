# -*- coding: utf-8 -*-
"""
TUFT 四大相互作用完整规范群统一结构 · 全维求导证明与精算
对象：《四大相互作用完整规范群统一结构》§1-§8
方法：sympy 矩阵代数 + Fraction 精确反常 + numpy 1-loop RG + 观测对标
红线：数学自洽 != 物理实验证实。
"""
from __future__ import print_function
import os
import sys
import math
import time
from fractions import Fraction as F
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_四力统一_report.txt")


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
                    self.echo("    - [" + sec + "] " + name)
        return cnt

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] report write failed: " + str(exc))


def part1_algebra(rep):
    import sympy as sp
    rep.section("§1  统一关系 T = T^(0) + T^i sigma^i/2 + T^a lambda^a/2：类型审查")
    rep.add("S1.1", "U(1)xSU(2)xSU(3) 生成元数 = 1+3+8 = 12", "PASS",
            "dim u(1)=1, su(2)=3, su(3)=8，合计 12 个生成元 ✓")
    rep.add("S1.2", "三项**直接相加** (1x1 + 2x2 + 3x3)", "FAIL",
            "sigma^i/2 是 2x2 矩阵、lambda^a/2 是 3x3 矩阵、T^(0) 是 1x1 标量；"
            "三者维数不同，**矩阵加法在类型上无定义**。"
            "正确必须先取张量积：sigma^i/2 (x) 1_3、1_2 (x) lambda^a/2。"
            "原文把不同内禀子空间的分量写成一个张量的相加，属类型错误。")
    rep.add("S1.3", "正确内禀结构 (1 (+) 2) (x) 3 的维数核对", "PASS",
            "q_L: 2(x)3 = 6; u_R/d_R: 1(x)3 = 3; l_L: 2(x)1 = 2; e_R/nu_R: 1。"
            "单代 2(x)3+3+3+2+1 = 15（SM，不含 nu_R），加 nu_R = 16 —— 与标准模型一致 ✓。"
            "但这是**重述标准模型表示论**，不构成从挠率导出该结构。")
    rep.add("S1.4", "T^lambda_munu 的内禀指标未显式分离", "BOUNDARY",
            "挠率 (lambda,mu,nu) 是时空张量指标；谈内禀代数分量须写成 "
            "T^lambda_munu = T^{lambda,A}_munu rho_A（A 为内禀指标）。原文混写时空与内禀指标，可修补但未给。")
    rep.add("S1.5", "表格引力行：'挠率内禀代数 = 曲率联络 Gamma'", "FAIL",
            "(1) 联络 Gamma 不是曲率（R 才是）；(2) Gamma 非张量、非李代数值；"
            "(3) 局部洛伦兹 SO(1,3) 的代数张成的是自旋联络 omega^{ab}_mu（取值 so(1,3)），"
            "不是仿射联络 Gamma^lambda_munu。该行应写 so(1,3)（6 个生成元）。")
    rep.add("S1.6", "dim so(1,3) = 4*3/2 = 6", "PASS", "3 转动 + 3 boost ✓")


def part2_ew(rep):
    import sympy as sp
    rep.section("§2  电弱统一：theta_W 的'几何定值'与量纲审查")
    th = sp.symbols("theta_W", real=True)
    M = sp.Matrix([[sp.cos(th), sp.sin(th)], [-sp.sin(th), sp.cos(th)]])
    rep.add("S2.1", "A/Z 混合矩阵正交性 det=1", "PASS",
            "det = %s，M^T M = I（标准二维旋转）✓（标准电弱混合，无 TUFT 增量）" % sp.simplify(M.det()))
    rep.add("S2.2", "tan(theta_W) = g'/g", "PASS", "这是弱混合角的**定义式**，不是推导结论。")
    rep.add("S2.3", "tan(theta_W) = T^(Y)/T^(3)（挠率分量之比）", "FAIL",
            "未给出 T^(Y)、T^(3) 与 g'、g 的映射 -> 等式右端无独立定义，'几何混合角'只是命名。")

    mW, mZ = 80.377, 91.1876
    sin2_on = 0.22305
    r_meas, r_pred = mW / mZ, math.sqrt(1.0 - sin2_on)
    rep.add("S2.4", "m_W/m_Z = cos(theta_W) 数值核对", "PASS",
            "m_W/m_Z = %.6f；cos(theta_W) = %.6f（on-shell），相对偏差 %.1e ✓（标准模型重述）"
            % (r_meas, r_pred, abs(r_meas - r_pred) / r_pred))

    sin2_obs = 0.23122
    rep.add("S2.5", "'维度比 3:1 决定 sin^2 theta_W'：数值检验", "FAIL",
            "3:1 的自然读数 g'^2/g^2 = 1/3 -> sin^2 theta_W = 1/4 = 0.250，"
            "实测 sin^2 theta_W(M_Z) = %.5f，偏差 %.2f%%。"
            "原文写出 '≈0.231 与实验吻合'，但 0.231 **不是**维度比 3:1 的结果，"
            "而是 M_Z 处 RG 演化后的测量值 -> 尺度混淆 + 循环论证。"
            % (sin2_obs, 100.0 * (0.25 - sin2_obs) / sin2_obs))
    rep.add("S2.6", "几何/统一处的 sin^2 theta_W 下界", "INFO",
            "SU(5) 归一化树图给 3/8 = 0.375；任何'几何/统一'起点值 >= 0.25。"
            "M_Z 的 0.23122 只能由**跑动**得到，不是几何定值。")

    MZ = 91.1876
    aem_inv = 127.95
    aem = 1.0 / aem_inv
    i1 = (3.0 / 5.0) * (1.0 - sin2_obs) / aem
    i2 = sin2_obs / aem
    b1, b2 = 41.0 / 10.0, -19.0 / 6.0
    c1, c2 = b1 / (2.0 * math.pi), b2 / (2.0 * math.pi)

    def t_for_ratio(k):
        # sin^2 = X/(X+Y), X=(3/5)/inv1, Y=1/inv2 ; inv1=i1-c1*t, inv2=i2-c2*t
        coef = 0.6 * (1.0 - k) / k
        return (i1 - coef * i2) / (c1 - coef * c2)

    mu_q = MZ * math.exp(t_for_ratio(0.25))
    mu_su5 = MZ * math.exp(t_for_ratio(3.0 / 8.0))
    rep.add("S2.7", "1-loop SM 中 sin^2 theta_W = 1/4 与 3/8 的能标", "FAIL",
            "1-loop 跑动（b1=%.3f, b2=%.4f）：sin^2=1/4 出现在 mu = %.3e GeV；"
            "sin^2=3/8 出现在 mu = %.3e GeV。二者都不是 M_Z -> "
            "'维度比给出 0.231' 在能标上不可能成立。"
            % (b1, b2, mu_q, mu_su5))

    rep.add("S2.8", "<T> = v ~ 246 GeV 的量纲", "FAIL",
            "若 <T> 为挠率/联络量纲 [L^-1]，则 [<T>]=L^-1 != [v]=M（能量）；"
            "若声明挠率无量纲，则 v 是**外部输入**（v=(sqrt(2)G_F)^(-1/2)=246.22 GeV）。"
            "两种读法都不成立：没有给出 246 GeV 的独立几何来源。")
    rep.add("S2.9", "希格斯 = 挠率真空形变的径向激发", "BOUNDARY",
            "作用量中无挠率自相互作用项 V(T)，故'真空形变 -> 径向激发'无法推导，只有命名。")


def part3_bundle(rep):
    rep.section("§3  主丛统一框架与'最终作用量'")
    rep.add("S3.1", "结构群 G = SO(1,3) x U(1) x SU(2) x SU(3)", "FAIL",
            "这是**笛卡尔直积**，不是单群。直积意味着四个**独立**耦合常数，"
            "群论上不能减少参数、不能统一任何东西（只是把四个理论打包）。"
            "真正统一需单群/semi-simple（SU(5)/SO(10)/E6），或先把 U(1)_Y 嵌入 SU(2)。"
            "故'最终归一'在群论层面不成立。")
    rep.add("S3.2", "维数核算：直积 18 vs SU(5) 单群 24", "INFO",
            "6+1+3+8 = 18；SU(5) dim=24（含 12 个新规范玻色子）。直积模型不要求也不排除新玻色子。")
    rep.add("S3.3", "统一联络 A = Gamma + A + W + G 相加", "FAIL",
            "(1) 四项属于不同李代数（仿射联络 / u(1) / su(2) / su(3)），相加前须取直和并指定表示，原文未做；"
            "(2) Gamma 是仿射联络（非张量）不能与规范势混加；(3) 混合后引力/规范力分界反而模糊。")
    rep.add("S3.4", "F_munu = d_mu A_nu - d_nu A_mu + [A_mu,A_nu]", "PASS", "标准非阿贝尔场强定义 ✓")
    rep.add("S3.5", "把 R^lambda_munu rho 写成 F^(grav)_munu", "BOUNDARY",
            "黎曼张量 4 指标 vs 场强 2 时空 + 2 内禀指标；正确写法 R^{ab}_munu（SO(1,3) 值 2-形式）。形式上可修补。")
    rep.add("S3.6", "'统一作用量' = EH + YM + Dirac 逐字照搬", "FAIL",
            "R 项、-1/4 F^2 项、psi-bar(i gamma D - m)psi 均是教科书 SM+GR 作用量，逐项照搬；"
            "**无任何 TUFT 特有项**（无挠率动能 T^2、无曲率平方、无非最小耦合、无 Omega 场作用量）。"
            "称'这是 TUFT 最终拉格朗日量'= 重新命名。")
    rep.add("S3.7", "D_mu 含全部相互作用", "PASS", "是标准 SM 协变导数 ✓（作为重述成立）")
    tot = 3 + 1 + 2 + 9 + 4
    rep.add("S3.8", "自由参数计数：与 SM 同构", "FAIL",
            "SM（不含 nu 质量）自由参数 %d 个（g1,g2,g3 / theta_QCD / m_H,v / 9 个 Yukawa / CKM 4）。"
            "TUFT 作用量与 SM 逐项相同 -> 继承同一组参数，无一被几何量替代。" % tot)
    rep.add("S3.9", "'几何算符自带普朗克截断 -> 无紫外发散'", "FAIL",
            "power counting：[G]=M^-2，引力相互作用为维度 5 的不可重整化算子；"
            "4D EH+SM 不可重整化是已知结果。原文未给截断构造/无 power counting 证据/无可算紫外行为。")
    rep.add("S3.10", "引力在 M_P 加入统一", "BOUNDARY",
            "alpha_grav = (m/m_P)^2 在 m=m_P 时为 1 属量纲恒等；"
            "'曲率与挠率耦合强度相等'需挠率独立耦合常数，而 TUFT 作用量中挠率无动能项、无耦合常数 -> 无定义对象。")


def part4_gut(rep):
    rep.section("§4  耦合常数统一与 GUT 汇聚（1-loop RG 实算）")
    sin2 = 0.23122
    aem_inv = 127.95
    aem = 1.0 / aem_inv
    a_s = 0.1181
    g1 = math.sqrt(4.0 * math.pi * (5.0 / 3.0) * aem / (1.0 - sin2))
    g2 = math.sqrt(4.0 * math.pi * aem / sin2)
    g3 = math.sqrt(4.0 * math.pi * a_s)
    rep.add("S4.1", "g1 = sqrt(5/3) e/cos(theta_W)", "PASS",
            "SU(5) 归一化标准关系 ✓（g1 = %.5f, g2 = %.5f, g3 = %.5f）" % (g1, g2, g3))
    rep.add("S4.2", "排序 g1 < g2 < g3", "PASS", "M_Z 实算：%.4f < %.4f < %.4f ✓ 与原文单调序一致" % (g1, g2, g3))
    dims = np.array([1.0, 3.0, 8.0])
    gs = np.array([g1, g2, g3])
    slope = np.polyfit(np.log(dims), np.log(gs), 1)[0]
    rep.add("S4.3", "'耦合强度由内禀维度决定'：定量检验", "BOUNDARY",
            "3 点 2 参幂律拟合指数 = %.3f（g propto sqrt(dim) 应为 0.5）。"
            "若强读 g propto sqrt(dim)（比值 1:1.732:2.828），实测为 1:%.3f:%.3f（偏差 -18.4%%/-6.6%%）。"
            "只有**单调序**被支持，'由维度定量决定'无定式（3 点拟合 2 参，自由度 1）。"
            % (slope, g2 / g1, g3 / g1))

    MZ = 91.1876
    inv0 = np.array([(3.0 / 5.0) * (1.0 - sin2) / aem, sin2 / aem, 1.0 / a_s])
    bs = np.array([41.0 / 10.0, -19.0 / 6.0, -7.0])

    def inv_at(mu, bvec):
        t = math.log(mu / MZ)
        return inv0 - (bvec / (2.0 * math.pi)) * t

    def cross(i, j, bvec):
        return (inv0[i] - inv0[j]) / ((bvec[i] - bvec[j]) / (2.0 * math.pi))

    rep.add("S4.4", "1-loop SM 输入", "INFO",
            "M_Z=%.4f；1/alpha_em=%.2f；sin^2=%.5f；alpha_s=%.4f；b=(%.4f,%.4f,%.4f)"
            % (MZ, aem_inv, sin2, a_s, bs[0], bs[1], bs[2]))
    pts = []
    for tag, i, j in [("a1=a2", 0, 1), ("a1=a3", 0, 2), ("a2=a3", 1, 2)]:
        t = cross(i, j, bs)
        mu = MZ * math.exp(t)
        pts.append((tag, mu, inv_at(mu, bs)[i]))
    rep.add("S4.5", "SM 三耦合的**两两交点**（1-loop 实算）", "FAIL",
            "%s: mu=%.3e, 1/alpha=%.3f | %s: mu=%.3e, 1/alpha=%.3f | %s: mu=%.3e, 1/alpha=%.3f。"
            "三点不重合（1/alpha 最大-最小 = %.1f），构成'三角形'而非一点 —— 非 SUSY 的 SM 不汇聚。"
            % (pts[0][0], pts[0][1], pts[0][2], pts[1][0], pts[1][1], pts[1][2],
               pts[2][0], pts[2][1], pts[2][2],
               max(p[2] for p in pts) - min(p[2] for p in pts)))
    v16 = inv_at(1.0e16, bs)
    rep.add("S4.6", "原文：M_GUT ~ 1e16 GeV 处 g1=g2=g3", "FAIL",
            "1e16 GeV 实算 1/alpha = (%.3f, %.3f, %.3f) -> alpha = (%.5f, %.5f, %.5f)；"
            "alpha 最大/最小 = %.3f（%.1f%% 分散）。'三耦合在 1e16 GeV 汇聚'被数值否证。"
            % (v16[0], v16[1], v16[2], 1.0 / v16[0], 1.0 / v16[1], 1.0 / v16[2],
               max(1.0 / v16) / min(1.0 / v16), 100.0 * (max(1.0 / v16) / min(1.0 / v16) - 1.0)))
    bs_m = np.array([33.0 / 5.0, 1.0, -3.0])
    pts_m = []
    for tag, i, j in [("a1=a2", 0, 1), ("a1=a3", 0, 2), ("a2=a3", 1, 2)]:
        t = cross(i, j, bs_m)
        mu = MZ * math.exp(t)
        pts_m.append((mu, inv_at(mu, bs_m)[i]))
    rep.add("S4.7", "对照：MSSM 1-loop 才汇聚", "INFO",
            "MSSM(b=33/5,1,-3) 交点 log10(mu/GeV) = (%.2f, %.2f, %.2f)，1/alpha = (%.2f, %.2f, %.2f) -> 显著靠拢。"
            "即 GUT 汇聚是**超对称**结果，非 TUFT 几何结果；TUFT 作用量(=SM)继承的是'不汇聚'。"
            % (math.log10(pts_m[0][0]), math.log10(pts_m[1][0]), math.log10(pts_m[2][0]),
               pts_m[0][1], pts_m[1][1], pts_m[2][1]))
    rep.add("S4.8", "借用 SU(5) 归一化却未承认嵌入前提", "FAIL",
            "把 U(1)xSU(2)xSU(3) 嵌入单群需给出嵌入映射（5bar = d_R^c (+) l_L, 10 = q_L (+) u_R^c (+) e_R^c）"
            "与 sqrt(3/5) 归一化。原文用了 g1=sqrt(5/3)e/cos(theta_W) 却未给嵌入映射。")


def part5_spectrum(rep):
    rep.section("§5  粒子谱量子数与反常消除（Fraction 精确）")
    # Q = T3 + Y 核对（用各组分的 T3）
    checks = [
        ("u_L", F(1, 2), F(1, 6), F(2, 3)),
        ("d_L", F(-1, 2), F(1, 6), F(-1, 3)),
        ("u_R", F(0, 1), F(2, 3), F(2, 3)),
        ("d_R", F(0, 1), F(-1, 3), F(-1, 3)),
        ("nu_L", F(1, 2), F(-1, 2), F(0, 1)),
        ("e_L", F(-1, 2), F(-1, 2), F(-1, 1)),
        ("e_R", F(0, 1), F(-1, 1), F(-1, 1)),
        ("H+", F(1, 2), F(1, 2), F(1, 1)),
        ("H0", F(-1, 2), F(1, 2), F(0, 1)),
    ]
    bad = []
    for nm, t3, y, q in checks:
        if t3 + y != q:
            bad.append(nm)
    rep.add("S5.1", "Q = T3 + Y 逐项核对（9 项）", "PASS" if not bad else "FAIL",
            "已核对 u_L/d_L/u_R/d_R/nu_L/e_L/e_R/H+/H0 共 9 项，全部满足 Q = T3 + Y ✓"
            if not bad else "不符项：" + ",".join(bad))

    # 反常系数（左旋 Weyl 场约定；右手场以共轭计入，符号取反）
    # A_U1 = sum Y * mult ; A_U1^3 = sum Y^3 * mult ; A_SU2^2 U1 = sum_{doublets} Y*color
    # A_SU3^2 U1 = sum_{color triplets} (2*Y per isospin comp) ; A_SU3^3 propto sum color-anomaly
    # 以左旋 Weyl 场计入（右手粒子取共轭 -> Y 反号）
    fields = [
        ("q_L", 6, F(1, 6), "3", 2),
        ("u_R", 3, F(-2, 3), "3bar", 1),
        ("d_R", 3, F(1, 3), "3bar", 1),
        ("l_L", 2, F(-1, 2), "1", 2),
        ("e_R", 1, F(1, 1), "1", 1),
        ("nu_R", 1, F(0, 1), "1", 1),
    ]
    A_grav = sum(F(m) * y for nm, m, y, c, w in fields)
    # SU(3)^3 反常：色三重态计 +1，色反三重态计 -1（q_L 含 2 个同位旋分量）
    A_333 = 2 * 1 + 1 * (-1) + 1 * (-1)
    rep.add("S5.2", "U(1)-引力混合反常 sum(Y) = 0", "PASS" if A_grav == 0 else "FAIL",
            "sum over 单代 = %s -> 精确为 0 ✓（Fraction 精确算）" % str(A_grav))
    A_u1cub = sum(F(m) * y ** 3 for nm, m, y, c, w in fields)
    rep.add("S5.3", "U(1)^3 反常 sum(Y^3) = 0", "PASS" if A_u1cub == 0 else "FAIL",
            "sum mult*Y^3 = %s（各分量 6*1/216, 3*(-8/27), 3*(1/27), 2*(-1/8), 1）-> 精确为 0 ✓"
            % str(A_u1cub))
    A_22u1 = F(3) * F(1, 6) + F(-1, 2)
    rep.add("S5.4", "SU(2)^2 U(1) 反常 = 0", "PASS" if A_22u1 == 0 else "FAIL",
            "only doublets contribute: 3*(1/6) + (-1/2) = %s -> 0 ✓" % str(A_22u1))
    A_33u1 = (F(2) * F(1, 6)) + F(-2, 3) + F(1, 3)
    rep.add("S5.5", "SU(3)^2 U(1) 反常 = 0", "PASS" if A_33u1 == 0 else "FAIL",
            "per color triplet: 2*(1/6) + (-2/3) + (1/3) = %s -> 0 ✓" % str(A_33u1))
    rep.add("S5.6", "SU(3)^3 反常 = 0（2 个 3 与 2 个 3bar）", "PASS",
            "q_L 含 2 个色三重态分量、u_R^c/d_R^c 为 3bar：2*(+1) + (-1) + (-1) = 0 ✓")
    rep.add("S5.7", "结论：量子数表与反常消除全对，但属**继承**", "INFO",
            "9 项 Q=T3+Y 与 5 类反常全部精确为 0 —— 这是标准模型费米子表的内禀性质，"
            "TUFT 的贡献是**照抄该表**，不是导出该表（表中'几何本质'列无构造、无独立预言）。")
    rep.add("S5.8", "'几何本质'列（带色左手挠率闭环 等）", "BOUNDARY",
            "全部是命名/隐喻：未给出挠率配置 -> 量子数（Y, I3, 色）的映射，故不可计算、不可证伪。")


def part6_selfcheck(rep):
    rep.section("§6  自洽性五条 + 完成清单逐条判定")
    rep.add("S6.1", "① 低能还原为 GR+SM", "PASS",
            "成立，但因为作用量**逐项就是** GR+SM，这是恒等而非校验（无信息量）。")
    rep.add("S6.2", "② 高能统一（M_P 处四力归一）", "FAIL",
            "群论上直积（§3.1）不统一；数值上 SM 三耦合不汇聚（§4.5/§4.6）。")
    rep.add("S6.3", "③ 无发散（几何算符自带截断）", "FAIL", "见 S3.9：无构造，且 4D 引力不可重整化。")
    rep.add("S6.4", "④ 参数内生（耦合/混合角/质量比由几何拓扑决定）", "FAIL",
            "sin^2 theta_W 维度比给 0.25 vs 实测 0.23122（差 8.1%）；"
            "v=246.22 GeV、g1/g2/g3、Yukawa 全部为外部输入（§2.5/§2.8/§3.8）。")
    rep.add("S6.5", "⑤ 观测匹配（暗物质暗能量配比 6.25/25/68.75）", "FAIL",
            "Planck 2018（TT,TE,EE+lowE+lensing）：Omega_b=0.0493, Omega_dm=0.2645, Omega_L=0.6847。"
            "对比 6.25/25/68.75 -> 重子 +26.8%、暗物质 -5.5%、暗能量 +0.4%。"
            "重子偏差 ~27% 远超观测误差，不构成'吻合'。")
    rep.add("S6.6", "§8 总览表 11 行全标 ✅", "FAIL",
            "名不副实：强相互作用一行已在《色挠率 SU(3)》分册判 FAIL 16 项"
            "（SU(3) 外部注入、b0 反号、V~r^2、质量式量纲非法）；"
            "本分册的'统一/归一'亦被 §3/§4 否证。")
    rep.add("S6.7", "'唯一公理 v_total = c'与作用量参数量的张力", "BOUNDARY",
            "若唯一公理成立，则 g1,g2,g3,v,Yukawa 应被公理固定；实测/框架中它们全是自由参数 -> "
            "两者不能同时为真，需明确'公理'的实际适用范围（仅几何运动学？）。")
    rep.add("S6.8", "§6 逻辑链图（曲率->引力 / 挠率->U(1)/SU(2)/SU(3)）", "BOUNDARY",
            "链图是**分类命名**，每一条箭头（如'挠率 -> SU(3)')都缺映射；"
            "链条的可检验内容仅是'低能=GR+SM'（恒等）。")


def part7_fix(rep):
    rep.section("§7  修复方案（分析 -> 处理 -> 修复 -> 优化）")
    fixes = [
        ("S1.2", "把相加改为张量积：(1 (+) 2) (x) 3；内禀指标显式化 T^{lambda,A}_munu"),
        ("S1.5", "引力行改 so(1,3)（6 生成元）与自旋联络 omega^{ab}_mu；Gamma 与 R 区分"),
        ("S2.3/S2.5", "删除'theta_W 由维度比决定'；如实写'theta_W 与 g'/g 是定义关系'"),
        ("S2.8", "删除'<T>=v'；如实声明 v=(sqrt(2)G_F)^(-1/2)=246.22 GeV 属外部输入"),
        ("S3.1", "如实声明结构群是**直积**（不是单群），故不构成'归一'"),
        ("S3.6", "如实声明作用是 SM+GR 照搬；若要 TUFT 化须补挠率动能项与 Omega 场作用量"),
        ("S4.6", "删除'M_GUT 汇聚'；如实标注 SM 不汇聚（MSSM 才汇聚）"),
        ("S6.6", "§8 总览表按分册实际判定降级 ✅ -> ❌/⚠️"),
    ]
    for tag, how in fixes:
        rep.add("FIX", "[" + tag + "] " + how, "INFO", "")
    rep.add("FIX.9", "优化：本分册应降级为'与 SM+GR 的一致性对照'", "BOUNDARY",
            "在补齐(1)群选择原理 (2)挠率->耦合映射 (3)TUFT 特有项之前，"
            "'四大相互作用完整统一/最终归一'的主张不成立；",
            )
    return


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 四大相互作用完整规范群统一结构 · 全维求导证明与精算")
    rep.echo("run at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)
    part1_algebra(rep)
    part2_ew(rep)
    part3_bundle(rep)
    part4_gut(rep)
    part5_spectrum(rep)
    part6_selfcheck(rep)
    part7_fix(rep)
    rep.add("全局", "运行耗时", "INFO", "%.2f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("report -> " + REPORT_PATH)


if __name__ == "__main__":
    main()
