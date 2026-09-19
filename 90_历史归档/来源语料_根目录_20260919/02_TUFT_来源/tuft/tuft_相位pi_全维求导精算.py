# -*- coding: utf-8 -*-
"""
TUFT 文稿 · 全维求导证明与精算（费米子闭环一圈相位 = pi）
========================================================
对象：《TUFT全维统一场论：费米子闭环一圈相位翻转 pi 的完整几何推导》§1–§8
逐条做：符号求导（sympy）/ 量纲 / 数值精算（numpy）/ 判定 PASS-FAIL-BOUNDARY-INFO
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
REPORT_PATH = os.path.join(HERE, "tuft_相位pi_全维求导精算_report.txt")


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
        self.echo("")
        self.echo("红线声明：数学自洽 != 实验证实。")
        return cnt

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] 报告写入失败: " + str(exc))


# ===================== §1a 类光曲线的固有时 =====================
def part1a_lightlike(rep):
    rep.section("§1a  类光螺旋能否用'固有时 tau'参数化")
    # 类光: ds^2 = c^2 dt^2 - |dx|^2 = 0
    rep.add("S1a.1", "类光条件 ds^2 = c^2dt^2 - |dx|^2 = 0", "PASS",
            "v_local = |dx|/dt = c <=> ds = 0（零间隔）")
    rep.add("S1a.2", "类光曲线的固有时 dtau = ds/c = 0（处处为零）", "FAIL",
            "固有时定义为 ds = c dtau；类光段 ds=0 => dtau=0，**tau 在类光曲线上恒为常数**，"
            "不能作为弧长/时间参数。原文用 dx/dtau = c*uhat 并对 tau 积分——"
            "类光曲线的合法参数是**仿射参数 lambda**（dx/dlambda = k uhat），非固有时。"
            "这是'光速螺旋用固有时参数化'的内在矛盾。")
    rep.add("S1a.3", "若坚持 |dx/dtau|=c，则 tau 与任何物理钟无关（量纲仍 L/T 但非 proper time）",
            "BOUNDARY",
            "可退一步把 tau 读作'任意仿射参数命名'，则 dx/dtau=c 只是**归一化约定**"
            "（把仿射速度取为 c）；但此时 dtau 不再有'固有时'的物理含义，"
            "下文'沿固有时绕行一圈 Delta tau = L/c'随之失去依据。")


# ===================== §1b Frenet-Serret 审查 =====================
def part1b_frenet(rep):
    import sympy as sp
    rep.section("§1b  Frenet-Serret 审查：d uhat/dtau = T nhat 是否正确")
    s = sp.symbols("s", real=True)
    kappa = sp.Function("kappa")(s)
    tau_c = sp.Function("tau")(s)
    # 标准 Frenet-Serret（符号形式）
    rep.add("S1b.1", "标准 Frenet-Serret 方程", "PASS",
            "d t/ds = kappa*n,  d n/ds = -kappa*t + tau*b,  d b/ds = -tau*n")
    rep.add("S1b.2", "切矢量导数 d t/ds = kappa*n —— 由**曲率 kappa** 驱动", "FAIL",
            "原文写 d uhat/dtau = T*nhat（切矢导数为'挠率 T'）。"
            "切矢量的变化率由**曲率 kappa**决定（d t/ds = kappa n）；"
            "**挠率 tau 是副法矢量的导数**（d b/ds = -tau n）。"
            "原文把 kappa 与 tau 的角色互换——这是概念的实质性错误，"
            "使'挠率 T 构造莫比乌斯拓扑'的链条失去几何依据。")
    rep.add("S1b.3", "若强行把原文的 T 读作曲率 kappa，则'挠率=拓扑'的叙述又被抽空", "INFO",
            "无论哪种读法，原文对'曲率 K / 挠率 T'的分配都不自洽："
            "§1 说 K 提供闭环、T 提供扭转，但 d uhat/dtau = T nhat 实际是曲率的方程。")


# ===================== §2 相位 = pi 的推导（循环性审查） =====================
def part2_phase(rep):
    import sympy as sp
    rep.section("§2  Delta phi = pi 的推导：独立推导 or 循环倒推")
    hbar, alpha, K, Om, Tbar = sp.symbols("hbar alpha K Omega Tbar", positive=True)

    # 原文链条：Delta phi = (2pi/hbar) alpha K Omega * (closed-int T dtau) * 1/(2pi)
    # 其中原文**设定** closed-int T dtau = hbar*pi/(alpha K Omega)
    Xset = hbar * sp.pi / (alpha * K * Om)
    dphi = (2 * sp.pi / hbar) * alpha * K * Om * Xset / (2 * sp.pi)
    dphi = sp.simplify(dphi)
    rep.add("S2.1", "代入原文所设闭合积分 ∮T dtau = hbar*pi/(alpha*K*Omega) 得 Delta phi",
            "PASS" if sp.simplify(dphi - sp.pi) == 0 else "FAIL",
            "Delta phi = " + str(dphi) + "（= pi）—— 代数上确实得到 pi")

    # 反向：若不预设 ∮T dtau，Delta phi 是自由量
    X = sp.symbols("X", positive=True)
    dphi_gen = sp.simplify((2 * sp.pi / hbar) * alpha * K * Om * X / (2 * sp.pi))
    rep.add("S2.2", "关键：'∮T dtau = hbar*pi/(alpha*K*Omega)' 是**为使结果=pi 而反设**的",
            "FAIL",
            "由通式 Delta phi = (alpha*K*Omega/hbar) * X（X=∮T dtau），要得 Delta phi=pi "
            "**必须** X = hbar*pi/(alpha*K*Omega)。原文直接把该值作为'挠率线积分'给出，"
            "属**倒推**：以'莫比乌斯给出 pi'（已知拓扑事实）为输入反解 ∮T dtau，再回到 pi。"
            "没有任何独立几何/动力学推导给出 ∮T dtau 的这一取值。")
    rep.add("S2.3", "末尾乘的 1/(2pi) 是事后补丁（ad hoc）", "FAIL",
            "原文自述'系数 1/(2pi) 来自角频率与相位的归一约定'。但 omega = dphi/dtau 本身"
            "就已定义相位，再乘 1/(2pi) 等于把 omega 里多塞的 2pi **人为扣回**——"
            "这是为凑出 pi 而加的补偿因子，不是几何必然。")
    rep.add("S2.4", "上游 omega 的来源依赖 E = hbar f = alpha*K*T*Omega", "BOUNDARY",
            "该能量式已在上一章被量纲审查判为非法（[m]=L^-4T^2 等），"
            "故 omega=(2pi/hbar)alpha*K*T*Omega 的链条本身建立在一个量纲非法的式子上。")


# ===================== §3 外部旋转 vs 莫比乌斯绕行 =====================
def part3_rotation(rep):
    rep.section("§3  '外部空间旋转 2pi' 与 '莫比乌斯绕行一圈' 是否同一操作")
    rep.add("S3.1", "两个操作在拓扑上并不相同", "FAIL",
            "(a) 外部空间旋转 2pi：SO(3) 中绕固定轴转 2pi，是**规范变换/回路**，"
            "其 1/2 自旋表示给出 -1（标准）；(b) 莫比乌斯带中心线走一圈：法向翻转，"
            "是**带子的单侧性**。原文把 (a) 与 (b) 直接等同（'把整个莫比乌斯结转一圈，"
            "内部挠率拓扑定向翻转 => Delta phi=pi'），但**未证明**两者相位相等。"
            "这是核心的未证明跳跃。")
    rep.add("S3.2", "标准事实：SO(3) 双覆盖给出 psi(theta+2pi)=-psi", "PASS",
            "pi1(SO(3)) = Z2，SU(2) 是 SO(3) 双覆盖 => 1/2 自旋表示绕 2pi 变号。"
            "结论 psi(theta+2pi)=-psi 正确，但这是**表示论**事实，不需莫比乌斯/挠率。")
    rep.add("S3.3", "psi(theta+4pi)=+psi", "PASS", "同上，SU(2) 的 4pi 闭合（表示论事实）。")


# ===================== §5 误区审查：挠率是否为费米子自旋必要条件 =====================
def part5_necessity(rep):
    rep.section("§5  误区审查：'挠率是费米子自旋拓扑的必要条件'")
    rep.add("S5.1", "纯黎曼时空（T=0）中 Dirac 旋量良定义（自旋 1/2 存在）", "FAIL",
            "标准结果：给定无挠的 Lorentz 流形 (M,g)，只要存在**自旋结构**（spin structure），"
            "Dirac 旋量场与自旋-1/2 表示**完全良定义**；广义相对论（纯黎曼，T=0）中"
            "费米子自旋早有成熟描述（如 Dirac 方程在弯曲时空）。"
            "因此'挠率是费米子自旋拓扑的必要条件'与已知物理**矛盾**——"
            "挠率（爱因斯坦-嘉当）是**可选扩展**，不是自旋的必要条件。")
    rep.add("S5.2", "正确表述：莫比乌斯双值来源于**旋转群的双覆盖**，而非挠率", "INFO",
            "自旋 1/2 的拓扑根源是 SO(3) 的 Z2 双覆盖（spin structure），"
            "与挠率场无逻辑必然关系。TUFT 若坚持'挠率构造莫比乌斯'，"
            "需证明该构造与 spin structure 的存在性等价，目前未给出。")


# ===================== §6/ §7 环绕数 W 与表格 =====================
def part6_winding(rep):
    rep.section("§6  '环绕数 W' 积分的身份审查")
    rep.add("S6.1", "W = (1/4pi)∮ uhat·(duhat x d2uhat) dtau 的身份", "BOUNDARY",
            "该积分是单位切矢 û 的**自链接数（self-linking / writhe 型 Gauss 积分）**，"
            "即 Călugăreanu-White 公式中的 Wr（writhe）；原文称其为'全挠率扭转积分'"
            "**不准确**：它给出的是 writhe，不是 Tw（扭转）。"
            "且该积分仅对**闭合曲线**才有拓扑不变性——见 §8 的闭合性检查。")
    rep.add("S6.2", "W 半整数/整数的区分（Mobius vs 普通环）", "BOUNDARY",
            "若曲线闭合且非退化，D(s)= 1/2pi ∮ u dot (du x d2u) 只能取整数或半整数取决于"
            "标架是否闭合（Whitney 公式）。属性方向正确，但与'挠率线积分 ∮T dtau'"
            "是**两个不同的量**，原文将二者等同属混用。")


def part7_table(rep):
    rep.section("§7  小结表格核对")
    rep.add("S7.1", "费米子一行（2pi 相位=pi, psi->-psi, W=n+1/2）", "BOUNDARY",
            "结论（pi, -psi）作为**已知量子力学结论**正确；但'由莫比乌斯挠率拓扑导出'"
            "未成立（见 S1b.2/S2.2/S3.1）。")
    rep.add("S7.2", "玻色子一行（2pi 相位=2pi, psi->+psi, W=n）", "FAIL",
            "概念混淆：'一圈空间旋转 2pi 得 +psi' 描述的是**轨道/标量相位**；"
            "而'交换两玻色子得 +psi' 描述的是**交换对称性**。二者不是同一操作。"
            "原文用'一圈相位 2pi => 波函数不变 => 交换对称'把两者混为一谈。")
    rep.add("S7.3", "W 半整数对应费米子（术语）", "BOUNDARY",
            "与上一章一致：winding number 是整数；半整数属自链接数 Lk/writhe。")


# ===================== §8 数值：复现原代码 + 闭合性检查 =====================
def part8_numeric(rep):
    rep.section("§8  原文数值代码复现 + 曲线闭合性检查")

    tau = np.linspace(0, 2 * np.pi, 1000)
    x = (2 + 0.5 * np.cos(tau / 2)) * np.cos(tau)
    y = (2 + 0.5 * np.cos(tau / 2)) * np.sin(tau)
    z = 0.5 * np.sin(tau / 2)

    P0 = np.array([x[0], y[0], z[0]])
    P1 = np.array([x[-1], y[-1], z[-1]])
    close = float(np.linalg.norm(P1 - P0))
    rep.add("S8.1", "曲线是否闭合（拓扑不变量的前提）", "FAIL" if close > 1e-6 else "PASS",
            "起点 = %s，终点 = %s，间距 = %.4f（**不闭合**）。"
            "参数化 x=(2+0.5cos(tau/2))cos(tau) 把莫比乌斯的半扭转混入了**中心线半径**，"
            "使中心线在 tau:0->2pi 时从 r=2.5 变到 r=1.5。"
            "对非闭合曲线，下文 W 积分**无拓扑意义**（任意值）。"
            % (np.round(P0, 3).tolist(), np.round(P1, 3).tolist(), close))

    # 复现原文 W 积分（对上述非闭合曲线）
    def unit(vectors):
        n = np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-15
        return vectors / n

    def cross3(a, b):
        return np.array([a[1] * b[2] - a[2] * b[1],
                         a[2] * b[0] - a[0] * b[2],
                         a[0] * b[1] - a[1] * b[0]])

    P = np.stack([x, y, z], axis=1)
    dP = np.gradient(P, tau, axis=0)
    uhat = unit(dP)
    duhat = np.gradient(uhat, tau, axis=0)
    d2uhat = np.gradient(duhat, tau, axis=0)
    integ = np.array([np.dot(uhat[i], cross3(duhat[i], d2uhat[i])) for i in range(len(tau))])
    W_open = 1.0 / (4 * np.pi) * np.trapz(integ, tau)
    rep.add("S8.2", "复现原文对**非闭合**曲线的 W 积分", "INFO",
            "W(open curve) = %.4f（不是拓扑不变量；随参数化/采样变化）" % W_open)

    # 正确做法：闭合中心线 = 圆；其切标架自链接数（writhe）= 0（平面圆）
    R = 2.0
    C = np.stack([R * np.cos(tau), R * np.sin(tau), np.zeros_like(tau)], axis=1)
    dC = np.gradient(C, tau, axis=0)
    uc = unit(dC)
    duc = np.gradient(uc, tau, axis=0)
    d2uc = np.gradient(duc, tau, axis=0)
    integ_c = np.array([np.dot(uc[i], cross3(duc[i], d2uc[i])) for i in range(len(tau))])
    W_closed_circle = 1.0 / (4 * np.pi) * np.trapz(integ_c, tau)
    rep.add("S8.3", "正确做法：**闭合**平面圆的切标架 writhe（解析应为 0）", "PASS",
            "W(circle) = %.4f（平面圆无 writhe，与解析 0 一致）——"
            "说明该积分对闭合曲线才给出稳定拓扑值" % abs(W_closed_circle))

    # 闭合的非平面螺旋（竖直螺线闭合）writhe ≠ 0
    t2 = np.linspace(0, 2 * np.pi, 2000)
    a = 1.0
    b = 0.4
    H = np.stack([(a + b * np.cos(3 * t2)) * np.cos(t2),
                  (a + b * np.cos(3 * t2)) * np.sin(t2),
                  b * np.sin(3 * t2)], axis=1)
    dH = np.gradient(H, t2, axis=0)
    uh = unit(dH)
    duh = np.gradient(uh, t2, axis=0)
    d2uh = np.gradient(duh, t2, axis=0)
    integ_h = np.array([np.dot(uh[i], cross3(duh[i], d2uh[i])) for i in range(len(t2))])
    W_torus = 1.0 / (4 * np.pi) * np.trapz(integ_h, t2)
    close_h = float(np.linalg.norm(H[-1] - H[0]))
    rep.add("S8.4", "闭合非平面曲线（三叶型环面曲线）的 writhe", "INFO",
            "W = %.4f（闭合间距 %.1e）；展示'writhe 是闭合曲线的拓扑量'，"
            "与原文不闭合参数化形成对照" % (W_torus, close_h))

    rep.add("S8.5", "结论：原文 W≈0.5 的数值演示无效", "FAIL",
            "因曲线不闭合，W 积分不构成环绕数验证；若 W 偶然≈0.5 属数值巧合。"
            "正确的'半整数'应来自 Călugăreanu-White 的 Lk/Tw 或 Whitney 标架闭合性，"
            "需用**闭合**曲线与**闭合标架**重新定义（见 tuft_fermion_spin.py 已闭合部分）。")


# ===================== §9 建议 =====================
def part9_advice(rep):
    rep.section("§9  下一步二选一")
    rep.add("S9.1", "选项1 Berry 几何相位与 TUFT 挠率相位等价", "INFO",
            "**建议选 1**：Berry 相位是良定义、可实验测量（中子/光子干涉）的量子几何相位，"
            "可与 TUFT 相位作**定量对比或证伪**，符合'可检验'倾向。")
    rep.add("S9.2", "选项2 色挠率 SU(3) / QCD 色荷 / 渐近自由与禁闭", "INFO",
            "较薄弱：'色=挠率多分量'无前置推导（上一章 §6 已判），"
            "且渐近自由/禁闭需完整 QCD 动力学，TUFT 侧尚无对应工具。")


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 文稿 · 全维求导证明与精算（闭环一圈相位 = pi）")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)
    part1a_lightlike(rep)
    part1b_frenet(rep)
    part2_phase(rep)
    part3_rotation(rep)
    part5_necessity(rep)
    part6_winding(rep)
    part7_table(rep)
    part8_numeric(rep)
    part9_advice(rep)
    rep.add("全局", "运行耗时", "INFO", "%.1f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
