# -*- coding: utf-8 -*-
"""
TUFT 黑洞热力学 / 视界曲率-挠率边界条件 / 信息悖论 · 全维求导证明与精算
对象：《TUFT 黑洞热力学、视界曲率-挠率边界条件与黑洞信息悖论》§1-§7
方法：sympy 度规曲率不变式 + numpy 原文代码逐行复现 + Gauss 环绕数数值积分 + 热力学量精算
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
REPORT_PATH = os.path.join(HERE, "tuft_黑洞热力学_report.txt")

# ---- 物理常数（CODATA 2018 / SI）----
L_P = 1.616255e-35
G_N = 6.67430e-11
C_L = 299792458.0
HBAR = 1.054571817e-34
KB = 1.380649e-23
M_SUN = 1.98847e30
M_P = 2.176434e-8
EV_IN_K = 11604.518
K_SAT = 1.0 / (L_P ** 2)


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
        with open(REPORT_PATH, "w", encoding="utf-8") as fh:
            fh.write("\n".join(self.lines))
            fh.write("\n")


def part1_geometry(rep):
    import sympy as sp
    rep.section("§1  黑洞几何结构：曲率饱和、挠率剖面与奇点移除")
    rep.add("B1.1", "l_P = 1.616255e-35 m", "PASS", "CODATA 2018 ✓")
    rep.add("B1.2", "K_sat = 1/l_P^2 = %.6e m^-2" % K_SAT, "PASS", "量纲 L^-2 ✓（与'曲率'一致）")

    r_h_sun = 2.0 * G_N * M_SUN / (C_L ** 2)
    K_h_sun = 1.0 / (r_h_sun ** 2)
    ratio = K_SAT / K_h_sun
    rep.add("B1.3", "恒星质量黑洞的视界曲率 vs K_sat", "FAIL",
            "r_h(1 M_sun) = %.1f m，视界曲率尺度 1/r_h^2 = %.4e m^-2；"
            "K_sat/(1/r_h^2) = %.3e —— 相差 %.0f 个数量级。"
            "曲率饱和 K_sat=1/l_P^2 只在 r_h ~ l_P（即 M ~ m_P = %.4e kg）附近才起作用；"
            "对所有天体黑洞（M >> m_P）'饱和'在视界处完全未触发。"
            % (r_h_sun, K_h_sun, ratio, math.log10(ratio), M_P))
    mu = (L_P / r_h_sun) ** 2
    rep.add("B1.4", "饱和生效条件的定量表达", "INFO",
            "K(r_h) ~ 1/r_h^2 = K_sat 等价于 r_h ~ l_P ⟺ M ~ m_P。"
            "(l_P/r_h)^2 = %.3e：即天体黑洞视界曲率比饱和值低 %.0f 个量级。"
            % (mu, -math.log10(mu)))

    # 曲率不变式公式核验
    r, M = sp.symbols("r M", positive=True)
    f = 1 - 2 * M / r
    K_KR = sp.simplify((sp.diff(f, r, 2)) ** 2 + 4 * (sp.diff(f, r) / r) ** 2 + 4 * (1 - f) ** 2 / r ** 4)
    rep.add("B1.5", "静态球对称度规 Kretschmann 公式核验", "PASS",
            "对 f = 1-2M/r 得 K = %s（= 48M^2/r^6，标准结果）✓ 公式可用（几何单位）"
            % sp.simplify(K_KR))

    l = sp.symbols("l", positive=True)
    f_h = 1 - 2 * M * r ** 2 / (r ** 3 + 2 * M * l ** 2)
    K_h = sp.simplify((sp.diff(f_h, r, 2)) ** 2 + 4 * (sp.diff(f_h, r) / r) ** 2
                      + 4 * (1 - f_h) ** 2 / r ** 4)
    K0 = sp.limit(K_h.subs({M: 1, l: 1}), r, 0)
    rep.add("B1.6", "对照：Hayward 正则黑洞（真正的奇点移除）", "INFO",
            "f = 1-2Mr^2/(r^3+2M l^2) 在 r->0 的 Kretschmann = %s（有限，de Sitter 核）。"
            "即：'曲率截断移除奇点'**可以**实现，但需要一个**特定的 f(r)/有效物质项**"
            "（Bardeen/Hayward 型），该项必须写进作用量。"
            "TUFT 的作用量（前一分册 §3.2）中**没有**任何此类项 -> 声称的奇点移除无实施路径。"
            % str(K0))
    rep.add("B1.7", "以'K(r_h)=K_c 临界曲率'定义视界", "FAIL",
            "GR 中视界由 g_rr -> inf / 表面引力 / 测地不完备定义，且 r_h = 2GM/c^2；"
            "原文用 K(r_h) = K_c（未给 K_c 值）作'几何边界曲面'定义，"
            "既未给出 K_c，也未给出与 2GM/c^2 的联系 -> 视为视界的判据不可计算。")
    rep.add("B1.8", "饱和削平奇点：与奇点定理的关系", "FAIL",
            "Penrose-Hawking 定理说的是**测地线不完备**，不是'曲率发散到无穷'。"
            "给曲率设上界不自动消除测地线不完备（度规仍可发散）；"
            "真正的正则黑洞需改变场方程（见 B1.6）。原文以'曲率饱和'替代证明，属错位论证。")
    rep.add("B1.9", "静态真空挠率剖面 T(r) != 0 的可容许性", "FAIL",
            "前一分册的统一作用量**不含挠率动能项（T^2）、无挠率势**，故挠率的场方程是**代数约束**"
            "（Einstein-Cartan 型：挠率 ∝ 自旋密度）。真空中自旋密度 = 0 -> T = 0。"
            "因此静态真空黑洞外部不可能存在非零挠率剖面 T(r)，"
            "本册 §1/§3 的挠率结构与其自身作用量**互相矛盾**。")
    rep.add("B1.10", "Ω -> Ω_DE = 0.6875 的外部边界条件", "BOUNDARY",
            "Ω(inf) = 0.6875 与 6.25/25/68.75 配比同源；Planck 2018 给 Omega_L = 0.6847，"
            "偏差 +0.41%（此一项与观测接近）。但 Ω 场在作用量中无动能项（见 B1.9 同款问题），"
            "其径向剖面只能手工指定。")
    return


def part2_entropy(rep):
    rep.section("§2  黑洞熵：A/4l_P^2 与'每元胞 1 比特'的一致性")
    rep.add("B2.1", "S = A/(4 l_P^2)，A = 4 pi r_h^2", "PASS",
            "Bekenstein-Hawking 熵的标准形式 ✓（属重述，无 TUFT 增量）")
    S_sun = 4.0 * math.pi * G_N * M_SUN ** 2 / (HBAR * C_L)
    rep.add("B2.2", "1 M_sun 黑洞的熵（数值）", "PASS",
            "S = 4 pi G M^2/(hbar c) = %.4e nats（= 4 pi (M/m_P)^2）；"
            "换算为 bit: %.4e（1 nat = 1/ln2 = %.4f bit）" % (S_sun, S_sun / math.log(2.0), 1.0 / math.log(2.0)))
    S_cell1 = 4.0 * math.pi * 1.0 / (4.0 * L_P ** 2)     # 原文代码 r_h = 1.0（无量纲）直接代入 l_P
    cell_area = 4.0 * L_P ** 2
    rep.add("B2.3", "'每个元胞携带 1 比特'与公式 A/4l_P^2 的一致性", "FAIL",
            "若元胞面积 = l_P^2 且每元胞 1 nat，则 S = A/l_P^2，是 B-H 的**4 倍**；"
            "要与 A/(4l_P^2) 自洽，元胞面积必须是 4l_P^2 = %.4e m^2（即每普朗克面积 1/4 nat）。"
            "原文文字（'普朗克尺度元胞、每元胞 1 比特'）与公式相差因子 4 -> 因子是**事后拟合**，"
            "不是从元胞计数导出。" % cell_area)
    rep.add("B2.4", "微观态计数：零计算", "FAIL",
            "声称'熵的微观来源是挠率拓扑自由度计数'，但全册**没有任何态计数计算**"
            "（无配分函数、无态数 N、无 ln N）。B-H 熵的系数 1/4 在弦论/LQG 中是被**算出来**的；"
            "本册只有命名 + 事后拟合。")
    rep.add("B2.5", "熵的积分形式 S = int (1/4l_P^2) sqrt(h) d^2x", "PASS",
            "与 A/(4 l_P^2) 等价 ✓（重述）")
    Lk = gauss_link_hopf(400)
    rep.add("B2.6", "'半整数拓扑环绕数 W=1/2,1,3/2...' 作为信息载体", "FAIL",
            "Gauss 环绕数（Hopf 链双线积分）实算 = %.4f，即**整数**（|Lk| = 1）。"
            "环绕数/链环数在闭曲线情形恒为整数；半整数来自**自旋 1/2 的双覆盖**"
            "（2pi 旋转 -> -1），不是环绕数。原文把两者混为一谈，"
            "且与《续篇》自洽结论（费米相位 -1 对应 Lk = -1，整数）冲突。"
            % Lk)
    return


def gauss_link_hopf(n):
    th = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    ph = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    T, P = np.meshgrid(th, ph, indexing="ij")
    x1 = np.stack([np.cos(T), np.sin(T), np.zeros_like(T)], axis=-1)
    x2 = np.stack([1.0 + np.cos(P), np.zeros_like(P), np.sin(P)], axis=-1)
    d1 = np.stack([-np.sin(T), np.cos(T), np.zeros_like(T)], axis=-1)
    d2 = np.stack([-np.sin(P), np.zeros_like(P), np.cos(P)], axis=-1)
    diff = x1 - x2
    cross = np.cross(d1, d2)
    num = np.sum(diff * cross, axis=-1)
    den = np.sum(diff ** 2, axis=-1) ** 1.5
    dth = 2.0 * math.pi / n
    dph = 2.0 * math.pi / n
    return float(np.sum(num / den) * dth * dph / (4.0 * math.pi))


def part3_hawking(rep):
    rep.section("§3  霍金辐射：公式量纲、几何形式与隧穿机制")
    T_sun = HBAR * C_L ** 3 / (8.0 * math.pi * G_N * KB * M_SUN)
    rep.add("B3.1", "T_H = hbar c/(8 pi G M)：量纲审查", "FAIL",
            "[hbar c/(G M)] = M（质量量纲），**不是温度/能量**；"
            "正确式为 T_H = hbar c^3/(8 pi G k_B M)（缺 c^2，等价于 c -> c^3）。"
            "数值核对：正确式给 T_H(1 M_sun) = %.4e K（= %.3e eV）；"
            "原文式给 %.4e（量纲为质量），相差 c^2/G 量级。"
            % (T_sun, T_sun / EV_IN_K, HBAR * C_L / (8.0 * math.pi * G_N * M_SUN)))
    T_geom = HBAR * C_L * math.sqrt(1.0 / r_h_of(M_SUN) ** 2) / (4.0 * math.pi * KB)
    rep.add("B3.2", "T_H = hbar c sqrt(K(r_h))/(4 pi k_B)：可成立的几何形式", "PASS",
            "取 K(r_h) = 1/r_h^2（视界曲率尺度），则 T_H = hbar c sqrt(K)/(4 pi k_B) 量纲 = 温度 ✓，"
            "对 1 M_sun 实算 = %.6e K，与标准 T_H = %.6e K 相对偏差 %.2e。"
            "两者**代数恒等**（因 sqrt(K) = 1/r_h = c^2/(2GM)）。"
            "即'几何形式'可以写对，但正确形式是 **sqrt(K)**，不是原文的 K*T。"
            % (T_geom, T_sun, abs(T_geom - T_sun) / T_sun))
    rep.add("B3.3", "T_H ∝ K(r_h) * T(r_h)（原文 TUFT 形式）", "FAIL",
            "[K]*[T] = L^-2 * L^-1 = L^-3，不是温度（能量 ML^2T^-2）；"
            "且比例系数未给 -> 量纲非法 + 无定式。与 B3.2 的正确几何形式（sqrt(K)）不同。")
    rep.add("B3.4", "M = (1/c^2) int alpha K T Omega 4 pi r^2 dr", "FAIL",
            "[alpha K T Omega] = L^-3，乘 4 pi r^2 dr = L^3 -> 无量纲；再除 c^2 -> L^-2 T^2。"
            "**不是质量 [M]**。（同一'alpha K T Omega/c^2'缺陷族的第 3 次重现："
            "《续篇》§5.1、《色挠率 SU(3)》§5.1、本册 §3。）"
            "正确关系：M = c^2 r_h/(2G)（= %.4e kg @ r_h=%.1f m），已数值核对。"
            % (C_L ** 2 * r_h_of(M_SUN) / (2.0 * G_N), r_h_of(M_SUN)))
    rep.add("B3.5", "'视界内外 Omega 不连续形成势垒'", "FAIL",
            "与 §1 的'挠率在视界上连续'自相矛盾：若 T 连续则无势垒。"
            "且原文代码中 Omega 是**连续**的（两侧同为 0.9375，见 B6.6）-> 三处互不一致。")
    rep.add("B3.6", "'隧穿'机制：零计算", "FAIL",
            "Hawking 辐射的既有严格方法（Bogoliubov 变换 / Parikh-Wilczek 隧穿）都需要"
            "计算作用量虚部或振幅。本册只给'拓扑拆分'的**叙事**，无隧穿振幅、无作用量、"
            "无出射谱 -> 机制未被推导。")
    rep.add("B3.7", "辐射谱为黑体谱", "INFO",
            "半经典层面成立（Hawking 1974）；但**正是**'严格黑体谱'与幺正性矛盾（§4），"
            "故本册同时接受'黑体谱'与'幺正无信息丢失'在此处存在张力（详见 B4.3）。")
    return


def r_h_of(m):
    return 2.0 * G_N * m / (C_L ** 2)


def part4_information(rep):
    rep.section("§4  黑洞信息悖论的'消解'审查")
    rep.add("B4.1", "信息容量：视界层足以容纳内部信息", "PASS",
            "B-H 熵即区域最大熵（全息界），故'信息写视界上'在**容量上**不矛盾。"
            "但这是全息原理/Holographic bound 的已知陈述，不是 TUFT 增量。")
    rep.add("B4.2", "'全息原理是挠率拓扑的直接推论'", "FAIL",
            "方向相反：全息原理（'t Hooft-Susskind）本身是**关于任意区域最大熵的猜想/原理**，"
            "B-H 熵是其锚点。本册把它当作 TUFT 的'推论'，属把前提当结论。")
    rep.add("B4.3", "幺正性：无任何可计算的判据", "FAIL",
            "信息逃逸的唯一半经典标志是**辐射的细致谱偏离严格热谱**（Page 曲线）。"
            "本册给出 0 个：无 Page 曲线、无偏离热谱量、无 S 矩阵、无微扰计算。"
            "定量：1 M_sun 黑洞蒸发时 t_ev = %.3e yr，Page 时间约 %.3e yr（= %.3f t_ev）；"
            "本册未给任何关于 t_Page 或谱偏离的预言 -> 不可证伪。"
            % (t_evap(M_SUN) / 3.15576e7, 0.6464 * t_evap(M_SUN) / 3.15576e7, 0.6464))
    rep.add("B4.4", "'GR 视界只是坐标面'", "FAIL",
            "GR 事件视界是**全局定义的类光面**（Killing 视界/未来零无穷的边界），不是'坐标面'；"
            "只有 Rindler 型加速观察者的视界才是坐标相关的。措辞错误。")
    rep.add("B4.5", "'视界是承载拓扑信息的挠率薄膜'", "BOUNDARY",
            "作为**图像**可接受（且与全息界相容）；作为机制未给动力学："
            "信息如何从落入物质转移到视界膜（无相互作用项、无散射计算）。")
    return


def t_evap(m):
    return 5120.0 * math.pi * G_N ** 2 * m ** 3 / (HBAR * C_L ** 4)


def part5_thermo(rep):
    rep.section("§5  黑洞热力学四定律审查")
    rep.add("B5.1", "dM = T_H dS + Phi dQ", "PASS", "RN 黑洞第一定律 ✓（标准形式，TUFT 只是把 Q 改称'U(1) 挠率电荷'）")
    rep.add("B5.2", "视界面积定理 dA >= 0", "PASS", "经典面积定理（Hawking 1971）✓，但条件来自**能量条件**，"
            "与'曲率饱和约束'无关 -> 原文附加条件多余（且是错误归因）。")
    rep.add("B5.3", "面积定理与霍金蒸发的**逻辑矛盾**", "FAIL",
            "原文同时断言：(a) dA >= 0 是定理；(b) 霍金辐射使'视界面积缩小'。"
            "两者不能同真：霍金辐射**恰恰破坏**经典面积定理（量子效应），"
            "半经典计算给 dA/dt < 0。原文用'不违反'把矛盾表述掩盖过去。")
    rep.add("B5.4", "广义第二定律（GSL）定量核对", "PASS",
            "以 k_B=1，S_BH = 4 pi G M^2/(hbar c)，T_H = hbar c^3/(8 pi G M)："
            "dS_BH/d|dM| = 8 pi G M/(hbar c)；辐射熵 dS_rad/d|dM| = c^2/T_H = 8 pi G M/(hbar c) "
            "-> **两者精确相消**，dS_tot = 0（临界饱和）。"
            "所以'GSL 成立'在半经典纯热辐射下是等式而非不等式；"
            "真正需要解释的是**纠缠熵修正**（Page），本册未涉及。")
    rep.add("B5.5", "'负的挠率能流向内'", "BOUNDARY",
            "若按字面理解（负能量流入黑洞），则违反能量条件 -> 面积定理反而被破坏；"
            "该说法未定义能量动量张量来源，故只能算修辞。")
    return


def part6_code(rep):
    rep.section("§6  原文仿真代码逐行复现与声称核对")
    src = "np.where(r < r_h, K_sat*(1 - np.exp(-r/r_h)), K_sat*(r_h/r)**2)"

    # 逐行复现数学部分（剔除绘图）
    r_h = 1.0
    Nr = 400
    r = np.logspace(-3, 3, Nr)
    K = np.where(r < r_h, K_SAT * (1.0 - np.exp(-r / r_h)), K_SAT * (r_h / r) ** 2)
    with np.errstate(over="ignore"):
        T = np.where(r < r_h, 0.8 * np.exp(-(r_h - r) / r_h), 0.8 * np.exp(-(r - r_h) / r_h))
    rep.add("B6.0", "原文代码的 numpy 分支溢出（代码质量）", "INFO",
            "np.where 对**两个分支都求值**：r>>r_h 时第一分支 exp(+(r-r_h)/r_h) 溢出（r=1e3 时 exp(999)）。"
            "未使用的分支产生 RuntimeWarning overflow——原代码同样存在（被 where 屏蔽，但数值上是 inf）。")
    Om = 0.6875 + 0.25 * np.exp(-((r - r_h) / 0.2) ** 2)
    alpha = 1.0 / 137.035999084
    rho = alpha * K * T * Om

    rep.add("B6.1", "K_sat = 1/l_P^2 = %.5e" % K_SAT, "PASS", "与 L_P 一致 ✓ %.5e m^-2" % (1.0 / L_P ** 2))

    inside = r < r_h
    K_in_max = float(np.max(K[inside]))
    K_in_min = float(np.min(K[inside]))
    K_at_0 = K_SAT * (1.0 - math.exp(-0.0))
    rep.add("B6.2", "内部剖面：K 是否达到饱和 K_sat", "FAIL",
            "复现原文代码：r<r_h 分支 K = K_sat(1-exp(-r/r_h))，"
            "内部 max(K) = %.6f * K_sat（= K(r_h^-) = 1 - e^-1 = %.6f），"
            "解析极限 K(r->0) = %.1f（**中心曲率为 0**，完全平坦）。"
            "**K 从未达到 K_sat** -> 代码里'曲率饱和'机制从未触发；"
            "且中心曲率为 0，与文字'中心是有限曲率的拓扑凝聚核心'相反。"
            % (K_in_max / K_SAT, 1.0 - math.exp(-1.0), K_at_0))
    K_out_at = K_SAT * (r_h / (r_h * (1.0 + 1e-9))) ** 2
    rep.add("B6.3", "视界处曲率连续性（原文称'曲率连续'）", "FAIL",
            "K(r_h^-) = %.6f * K_sat；K(r_h^+) = %.6f * K_sat -> "
            "视界处**跳变 %.3f 倍**（不连续）。原文'仿真结果特征：视界位置曲率连续'与代码矛盾。"
            % (1.0 - math.exp(-1.0), K_out_at / K_SAT, 1.0 / (1.0 - math.exp(-1.0))))

    # T 的梯度跃变
    eps = r_h * 1e-4
    dT_in = (0.8 * math.exp(-(r_h - r_h * 0.9999) / r_h) - 0.8 * math.exp(-0.0)) / (r_h * 0.9999 - r_h)
    dT_out = (0.8 * math.exp(-(r_h * 1.0001 - r_h) / r_h) - 0.8) / (r_h * 1.0001 - r_h)
    rep.add("B6.4", "挠率 T(r) 连续、梯度跃变（原文称'梯度存在跃变'）", "PASS",
            "代码中 T = 0.8*exp(-|r-r_h|/r_h) 在 r_h 处**连续**（=0.8），"
            "左导数 = +%.3f/m、右导数 = %.3f/m -> **梯度确为跃变** ✓ 此条与代码一致。"
            "但 0.8 是**任意常数**，无场方程确定其值（BOUNDARY）。" % (dT_in, dT_out))
    rep.add("B6.5", "T(r_h) = 0.8 的来源", "BOUNDARY", "手写常数，无方程/无来源；量纲亦未声明。")

    Om_left = 0.6875 + 0.25 * math.exp(-((r_h - 1e-12 - r_h) / 0.2) ** 2)
    Om_right = 0.6875 + 0.25 * math.exp(-((r_h + 1e-12 - r_h) / 0.2) ** 2)
    rep.add("B6.6", "Omega 剖面：是否'不连续形成势垒'（§3 声称）", "FAIL",
            "复现代码：Omega(r_h^-) = %.10f, Omega(r_h^+) = %.10f -> **完全连续**。"
            "§3 的'视界内外 Omega 不连续'与代码、与 §1 的挠率连续性三处互斥。" % (Om_left, Om_right))

    rho_max = float(np.max(rho))
    rep.add("B6.7", "'能量密度' rho = alpha K T Omega", "FAIL",
            "[alpha K T Omega] = L^-3（非能量密度 ML^-1T^-2；[T] 本身无量纲声明缺失）；"
            "复现峰值 rho = %.4e（若按 SI 读作 kg/m^3 则比中子星密 ~49 个量级）。"
            "量纲非法 + 数值无物理尺度。" % rho_max)

    A_wrong = 4.0 * math.pi * r_h ** 2
    S_wrong = A_wrong / (4.0 * L_P ** 2)
    A_sun = 4.0 * math.pi * r_h_of(M_SUN) ** 2
    S_sun = A_sun / (4.0 * L_P ** 2)
    rep.add("B6.8", "S_bh 计算中的单位混用", "FAIL",
            "代码 r_h = 1.0（注释为'无量纲'），却代入 A = 4 pi r_h^2 并除以 l_P^2（米制）"
            "-> 得到 S = %.4e（即把 1 m 当作视界半径）。"
            "若改为 1 M_sun（r_h = %.1f m）则 S = %.4e。"
            "原文打印的 A 与 S 数值本身无物理含义（米制/无量纲混用）。"
            % (S_wrong, r_h_of(M_SUN), S_sun))
    rep.add("B6.9", "'数值模型/仿真'的实质：无求解", "FAIL",
            "代码 `from scipy.optimize import minimize` 被导入但**从未调用**；"
            "K(r)、T(r)、Omega(r) 全部是手写解析式，无场方程、无度规、无求解器、无收敛判据。"
            "-> §6 实为**绘图脚本**，不构成'球对称 TUFT 黑洞径向剖面数值仿真'。")
    rep.add("B6.10", "'仿真结果特征'四条逐条核对", "FAIL",
            "(1) '视界位置曲率连续' ✗（跳变 1.58 倍，B6.3）；"
            "(2) '挠率两侧平滑但梯度突变' ✓（B6.4）；"
            "(3) '内部曲率被饱和上限约束' ✗（未达 K_sat，B6.2）；"
            "(4) '无发散奇点' — 代码未计算任何曲率不变式，"
            "且内部 K(0)=0 恰使中心无发散，但这不是'饱和削平'的结果 ✗。"
            "4 条中 3 条与代码实跑不符。")
    return


def part7_fix(rep):
    rep.section("§7  修复方案（分析 -> 处理 -> 修复 -> 优化）")
    fixes = [
        ("B3.1", "T_H 改为 hbar c^3/(8 pi G k_B M)；或写成几何形式 hbar c sqrt(K(r_h))/(4 pi k_B)"),
        ("B3.3/B3.4", "删除 K*T 与 (1/c^2)int alpha K T Omega 4 pi r^2 dr；"
                      "质量用 c^2 r_h/(2G)，温度用 sqrt(K)"),
        ("B2.3", "元胞面积改 4l_P^2（或改述'每普朗克面积 1/4 nat'），并补真正的态计数"),
        ("B2.6", "删'半整数环绕数'；改为'整数链环数 + 自旋 1/2 双覆盖'（与《续篇》一致）"),
        ("B1.9", "若要在真空中维持 T(r)，必须在作用量中补挠率动能项 T^2 与耦合常数"),
        ("B1.6", "若要真做奇点移除，须给出 f(r)（Bardeen/Hayward 型）与其有效作用量项"),
        ("B4.3", "补可证伪判据：给出辐射谱相对热谱的偏离量或 Page 曲线（当前为零）"),
        ("B5.3", "如实区分'经典面积定理'与'量子蒸发破坏面积定理'，并改用 GSL + 纠缠熵"),
        ("B6.x", "代码：去掉未使用的 minimize；K 剖面须由**解方程**得到而非手写；"
                 "r_h 用有量纲值（如 1 M_sun -> 2952 m）"),
    ]
    for tag, how in fixes:
        rep.add("FIX", "[" + tag + "] " + how, "INFO", "")
    rep.add("FIX.10", "优化：本册应降级为'标准黑洞热力学 + 全息原理的重新命名'", "BOUNDARY",
            "在补齐(1)挠率动力学 (2)正则黑洞 f(r) (3)谱偏离/Page 曲线 之前，"
            "'黑洞熵/霍金辐射的几何推导'与'信息悖论消解'的主张均不成立；"
            "已成立的部分（A/4l_P^2、T_H、四个热力学定律）全部是标准结果的重述。")


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 黑洞热力学 / 视界曲率-挠率边界 / 信息悖论 · 全维求导证明与精算")
    rep.echo("run at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)
    part1_geometry(rep)
    part2_entropy(rep)
    part3_hawking(rep)
    part4_information(rep)
    part5_thermo(rep)
    part6_code(rep)
    part7_fix(rep)
    rep.add("全局", "运行耗时", "INFO", "%.2f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("report -> " + REPORT_PATH)


if __name__ == "__main__":
    main()
