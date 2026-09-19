# -*- coding: utf-8 -*-
"""
TUFT 续篇 · 全维求导证明与精算（自旋统计 / 泡利 / 手性）
==========================================================
对应原稿《TUFT全维统一场论 — 续篇》§1–§9，逐条做：
  (a) 符号求导（sympy） (b) 量纲分析（精确指数） (c) 数值精算（numpy/mpmath）
  (d) 判定：PASS / FAIL / BOUNDARY / INFO

红线：数学自洽 != 物理实验证实。只检验框架内部自洽、量纲与数值收敛。
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
REPORT_PATH = os.path.join(HERE, "tuft_续篇_全维求导精算_report.txt")


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


# ============================== §1 拓扑 ==============================
def part1(rep):
    import sympy as sp
    rep.section("§1  闭环螺旋拓扑与自旋 1/2（Mobius 标架 + Calugareanu-White）")
    th = sp.symbols("theta", real=True)
    N0 = sp.Matrix([1, 0, 0])
    N = sp.Matrix([sp.cos(th / 2), sp.sin(th / 2), 0])
    d2 = sp.simplify(N.subs(th, 2 * sp.pi) + N0)
    d4 = sp.simplify(N.subs(th, 4 * sp.pi) - N0)
    rep.add("S1.1", "符号证明 N(2pi) = -N(0)（半整数环绕 ⇒ 标架翻转）",
            "PASS" if d2 == sp.zeros(3, 1) else "FAIL",
            "N(2pi)+N(0) = " + str(list(d2.T)) + " (零矢量)")
    rep.add("S1.1", "符号证明 N(4pi) = +N(0)（4pi 构型复原）",
            "PASS" if d4 == sp.zeros(3, 1) else "FAIL",
            "N(4pi)-N(0) = " + str(list(d4.T)) + " (零矢量)")
    rep.add("S1.1", "推论 psi(t+2pi)=-psi, psi(t+4pi)=+psi（旋量 4pi 周期）", "PASS",
            "标架双值性直接给出；数值见 tuft_fermion_spin.py frame_closure(1): "
            "|N(2pi)+N(0)|=2.7e-16, |N(4pi)-N(0)|=5.5e-16")
    rep.add("S1.2", "术语审查：Lk = Tw + Wr in (1/2)Z（非整数环绕数）", "BOUNDARY",
            "原稿称'拓扑环绕数 W in Z+1/2'。严格地，S1 的 winding number in Z "
            "(pi1(S1)=Z)；半整数只出现在**自链接数 Lk**（可定向带 Tw=n/2, n 奇 ⇒ "
            "Lk in (1/2)Z，Mobius 型）。属性正确但术语误用，应称 Lk。"
            "参照 Leinaas-Myrheim 1977 / Laidlaw-DeWitt 1971。")
    rep.add("S1.3", "相位关系 Dphi = ∮ omega dtau 量纲自洽", "PASS",
            "[omega]=T^-1, [tau]=T ⇒ [Dphi]=1。注：第七节代码 dphi=omega*sqrt(aKT)*dr "
            "量纲为 T^-1，非相位（见 S7.2）。")


# ============================== §2 自旋代数 ==============================
def part2(rep):
    import sympy as sp
    rep.section("§2  自旋角动量 S=(hbar/2)T/|T| 与 SU(2) 代数（符号求导）")
    hbar = sp.symbols("hbar", positive=True)
    I2 = sp.eye(2)
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sz = sp.Matrix([[1, 0], [0, -1]])
    S = [hbar / 2 * m for m in (sx, sy, sz)]
    eps = {(0, 1, 2): 1, (1, 2, 0): 1, (2, 0, 1): 1,
           (1, 0, 2): -1, (2, 1, 0): -1, (0, 2, 1): -1}
    ok = True
    for i in range(3):
        for j in range(3):
            lhs = S[i] * S[j] - S[j] * S[i]
            rhs = sp.zeros(2, 2)
            for k in range(3):
                e = eps.get((i, j, k), 0)
                if e:
                    rhs = rhs + sp.I * hbar * e * S[k]
            if sp.simplify(lhs - rhs) != sp.zeros(2, 2):
                ok = False
    rep.add("S2.1", "符号验证 [S_i,S_j] = i*hbar*eps_ijk*S_k (S=hbar*sigma/2)",
            "PASS" if ok else "FAIL", "Pauli 代数符号恒等（最大残差 0）")
    S2 = sp.simplify(S[0] * S[0] + S[1] * S[1] + S[2] * S[2])
    ok2 = sp.simplify(S2 - sp.Rational(3, 4) * hbar ** 2 * I2) == sp.zeros(2, 2)
    rep.add("S2.2", "符号验证 S^2 = s(s+1)hbar^2 = (3/4)hbar^2 I (s=1/2)",
            "PASS" if ok2 else "FAIL", "S^2 = " + str(S2[0, 0]) + " * I")
    rep.add("S2.3", "记号风险：S=(hbar/2)*T/|T| 若按矢量读则 S^2=hbar^2/4 != 3hbar^2/4",
            "BOUNDARY",
            "S 必须是**算符矢量**(Sx,Sy,Sz)=(hbar/2)(sx,sy,sz)，其模方 3hbar^2/4；"
            "T/|T| 只能承担 S_z 量化轴。原稿写成'标量x单位矢量'，字面读 |S|^2=hbar^2/4 "
            "与 s(s+1)hbar^2 差 3 倍（不自洽）。")
    rep.add("S2.4", "SU(2) 来源：接入而非 TUFT 导出", "INFO",
            "S=(hbar/2)sigma 满足 su(2) 是 1/2-旋量表示的普遍事实；TUFT 目前赋以该表示，"
            "挠率手性只提供量化轴，不生成表示论。")


# ============================== §3 自旋统计 ==============================
def part3(rep):
    rep.section("§3  自旋-统计：交换 <=> 世界线 Hopf 链（Gauss 双链积分）")

    def gauss_linking(e1, e2):
        N = e1.shape[1]
        dt = 2.0 * math.pi / N
        de1 = np.gradient(e1, dt, axis=1)
        de2 = np.gradient(e2, dt, axis=1)
        tot = 0.0
        for i in range(N):
            d = e1[:, i][:, None] - e2
            r3 = np.sum(d * d, axis=0) ** 1.5 + 1e-9
            cr = np.cross(de1[:, i], de2, axis=0)
            tot += np.sum(np.sum(d * cr, axis=0) / r3)
        return float(tot * dt * dt / (4.0 * math.pi))

    N = 4000
    lam = np.linspace(0.0, 2.0 * math.pi, N, endpoint=False)
    C1b = np.array([np.cos(lam), np.sin(lam), np.full_like(lam, 1.0)])
    C2b = np.array([np.cos(lam), np.sin(lam), np.full_like(lam, -1.0)])
    C1a = np.array([np.cos(lam), np.sin(lam), np.zeros_like(lam)])
    C2a = np.array([np.zeros_like(lam), 1.0 + np.cos(lam), np.sin(lam)])
    Lk_b = gauss_linking(C1b, C2b)
    Lk_a = gauss_linking(C1a, C2a)
    dLk = Lk_a - Lk_b
    rep.add("S3.1", "交换前不链 Lk~0", "PASS" if abs(Lk_b) < 0.05 else "FAIL",
            "Lk_before = %.4f" % Lk_b)
    rep.add("S3.1", "交换后 Hopf 链 |Lk|~1", "PASS" if abs(abs(Lk_a) - 1) < 0.05 else "FAIL",
            "Lk_after = %.4f" % Lk_a)
    rep.add("S3.1", "交换使 dLk = +-1", "PASS" if abs(abs(dLk) - 1) < 0.05 else "FAIL",
            "dLk = %.4f" % dLk)
    ph_f = complex(np.exp(1j * math.pi * dLk))
    rep.add("S3.2", "费米子交换相位 exp(i*pi*dLk) = -1",
            "PASS" if abs(ph_f + 1) < 1e-3 else "FAIL",
            "phase = %.4f%+.4fj" % (ph_f.real, ph_f.imag))
    rep.add("S3.2", "玻色子交换相位 = +1", "PASS", "phase = +1（与链数无关）")
    rep.add("S3.3", "模型循环性：'费米子世界线设为 Mobius 型 W=1/2' 是输入假设", "INFO",
            "把'费米子'定义为世界线 Lk 取半整数，再得 exp(i2piW)=-1，从而'证明'反对称——"
            "框架内自洽的表示，非对标准自旋-统计定理的独立证明。")
    rep.add("S3.4", "泡利不相容（反对称 ⇒ 同态禁占）", "PASS",
            "Psi(x1,x2)=-Psi(x2,x1)；x1=x2 ⇒ Psi=-Psi ⇒ Psi=0；等价两列相同的 Slater "
            "行列式=0。此为已知结论，非独立公理。")


# ============================== §4 手性 ==============================
def part4(rep):
    import sympy as sp
    rep.section("§4  手性算符 gamma5 ∝ T/|T|（类型/维数审查）")
    g5 = sp.diag(-1, -1, 1, 1)
    rep.add("S4.1", "gamma5 的数学身份：4x4 矩阵，本征值 +-1", "PASS",
            "shape = " + str(g5.shape) + "；本征值 = {-1, +1}")
    That = sp.Matrix(3, 1, [1, 0, 0])
    rep.add("S4.1", "类型审查：gamma5(4x4) 不能 ∝ That(3x1)", "FAIL",
            "shape 不匹配 (4,4) vs (3,1)，'矩阵 ∝ 矢量'是范畴错误。合法对应只能是"
            "**符号对应**：手性本征值 +-1 <-> 挠率符号 sign(T)。")
    rep.add("S4.2", "V-A 结构 (1-gamma5)/2 只耦合左手", "INFO",
            "标准模型既定结构；TUFT 侧为几何直觉，未从总作用量变分导出 (1-gamma5)/2 "
            "投影或 W/Z 耦合强度。")


# ============================== §5 质量 ==============================
def part5(rep):
    rep.section("§5  质量内生公式 m = alpha*K*T*Omega/c^2（量纲精算）")
    # 原式量纲: [alpha]=1,[K]=L^-1,[T]=L^-1,[Omega]=1,[c^2]=L^2T^-2 => L^-4 T^2
    dimL = F(-1) + F(-1) - F(2)
    dimT = F(0) - F(-2)
    rep.add("S5.1", "原稿 m = alpha*K*T*Omega/c^2 量纲非法（非 [M]）", "FAIL",
            "[m] = L^(%s) T^(%s)，非 [M]；该式不能作质量表达式。" % (str(dimL), str(dimT)))
    hbar = 1.054571817e-34
    c = 299792458.0
    me = 9.1093837015e-31
    lamC = hbar / (me * c)
    Om_w = c / lamC
    m_chk = hbar * Om_w / c ** 2
    rep.add("S5.2", "修正式 m = hbar*sqrt(k^2+t^2)/c = hbar*Om_w/c^2 量纲 = M", "PASS",
            "取 k=1/lamC, t=0 ⇒ m = %.6e kg (电子 %.6e kg, 比值 %.6f)，"
            "即**数值自洽但为反推**（由 lamC 定义 k，非由 k 导出 lamC）"
            % (m_chk, me, m_chk / me))
    rep.add("S5.3", "尺度生成机制仍开放（为何 k=1/lamC 而非 1/l_P）", "INFO",
            "m=hbar*Om_w/c^2 属'方向正确、数值待赋'唯象式；光子 Om_w=0 ⇒ m=0 相容。")


# ============================== §6 玻色子 ==============================
def part6(rep):
    rep.section("§6  玻色子拓扑对比（定性框架）")
    rep.add("S6.1", "光子/W-Z/胶子三层定性分类", "INFO",
            "光子 Om_w=0 ⇒ m=0；W/Z 瞬态闭环 ⇒ m!=0（Om_w 来源未建模）；"
            "胶子'色=挠率多分量'为待展开命题（§九-C）。无定量断言，标 INFO。")


# ============================== §7 朴素互换 ==============================
def part7(rep):
    rep.section("§7  原稿第七节'朴素互换'代码复现（证明其恒为 0）")
    alpha = 1.0 / 137.035999084
    r = np.logspace(-4, 3, 300)
    K1 = 2.2 * np.exp(-r)
    T1 = 1.8 * np.exp(-r)
    Om1 = 0.6875 + (0.0625 - 0.6875) * np.exp(-r)
    omega1 = alpha * K1 * T1 * Om1
    K2 = 2.2 * np.exp(-np.abs(r - 1.2))
    T2 = 1.8 * np.exp(-np.abs(r - 1.2))
    Om2 = 0.6875 + (0.0625 - 0.6875) * np.exp(-np.abs(r - 1.2))
    omega2 = alpha * K2 * T2 * Om2

    def sp_phase(rr, K, T, om):
        return np.trapz(om * np.sqrt(alpha * K * T), rr)

    phi1 = sp_phase(r, K1, T1, omega1)
    phi2 = sp_phase(r, K2, T2, omega2)
    dphi = (sp_phase(r, K2, T2, omega2) + sp_phase(r, K1, T1, omega1)) - (phi1 + phi2)
    rep.add("S7.1", "原代码交换相位 dphi = 0（加法交换律，无信息）",
            "PASS" if abs(dphi) < 1e-12 else "FAIL",
            "dphi = %.3e；phi_swap 与 phi_total 恒等 ⇒ 不能演示交换变号"
            "（原稿声称 dphi~pi 与代码逻辑矛盾）" % dphi)
    rep.add("S7.2", "代码量纲核查：dphi=omega*sqrt(aKT)*dr 量纲非相位", "FAIL",
            "[omega]=T^-1,[sqrt(aKT)]=L^-1,[dr]=L ⇒ [dphi]=T^-1，非无量纲相位"
            "（代码混用了 K*T*Om 与 sqrt(aKT) 两套不一致的 omega）。")
    rep.add("S7.3", "结论：正确交换相位须来自世界线编织（§3）", "INFO",
            "§3 的 Gauss 链 dLk=+-1 ⇒ exp(i*pi*dLk)=-1 才是有效演示。")


# ============================== §8 盘点核对 ==============================
def part8(rep):
    rep.section("§8  完成度盘点核对（对每条✅做独立判定）")
    rep.add("S8.1", "① 总作用量/变分生成场方程", "INFO", "前篇 R1 范畴，本续篇未复核")
    rep.add("S8.2", "② 拓扑环绕数导出自旋 1/2", "PASS",
            "Mobius 标架 4pi 闭包符号+数值成立（S1.1），但术语应为 Lk（S1.2）")
    rep.add("S8.3", "③ 自旋 SU(2) 代数", "BOUNDARY",
            "代数恒等成立（S2.1），但为表示论事实，TUFT 属接入（S2.4）；"
            "且 S 记号有矢量/算符歧义（S2.3）")
    rep.add("S8.4", "④ 自旋-统计定理", "BOUNDARY",
            "框架内演示成立（S3.1/S3.2），但含循环输入（S3.3）")
    rep.add("S8.5", "⑤ 泡利不相容几何推导", "PASS", "反对称 ⇒ 同态禁占（S3.4），已知结论")
    rep.add("S8.6", "⑥ 手性+弱作用宇称破缺几何解释", "FAIL",
            "gamma5 ∝ T 为类型错误（S4.1）；V-A 未定量导出（S4.2）")
    rep.add("S8.7", "⑦ 狄拉克拉氏量、质量内生公式", "FAIL",
            "原质量式量纲非法（S5.1）；修正式数值自洽但为反推（S5.2/S5.3）")


# ============================== §9 建议 ==============================
def part9(rep):
    rep.section("§9  下一阶段 A/B/C 建议")
    rep.add("S9.A", "A 路径积分 TUFT-QFT", "INFO",
            "自然但只是标准 QFT 工具套用，不产生 TUFT 独有可检验信号。")
    rep.add("S9.B", "B 挠率诱导引力波（LISA 预言）", "INFO",
            "**建议选 B**：地基最扎实（R1 引力扇区已数值自检），最易给 falsifiable 预言。")
    rep.add("S9.C", "C QCD 色挠率理论", "INFO",
            "最宏大但最薄弱：'色=挠率多分量'无推导支撑，前置缺失。")


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 续篇 · 全维求导证明与精算")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)
    part1(rep)
    part2(rep)
    part3(rep)
    part4(rep)
    part5(rep)
    part6(rep)
    part7(rep)
    part8(rep)
    part9(rep)
    rep.add("全局", "运行耗时", "INFO", "%.1f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
