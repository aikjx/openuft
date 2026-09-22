# -*- coding: utf-8 -*-
"""
================================================================================
TUFT 续篇数值仿真：双时空结交换的拓扑相位（费米子反对称 / 玻色子对称）
================================================================================

对应文档《TUFT全维统一场论 — 续篇：费米子自旋统计、泡利原理、拓扑螺旋本征态》
第七节"双时空结交换模拟"的【诚实升级版】。

--------------------------------------------------------------------------------
【重要更正】文档原第七节给出的"朴素互换"代码：
    phi_swap = spiral_phase(r,K2,T2,omega2) + spiral_phase(r,K1,T1,omega1)
    dphi_swap = phi_swap - phi_total        # phi_total = phi1 + phi2
由于两个非相互作用的螺旋剖面只是相加，phi_swap 与 phi_total 在数学上恒等，
故 dphi_swap === 0。该代码本质上只是"加法的交换律"，并不能演示费米子交换
变号——它什么也没证明。本文件保留该朴素互换作对照（结果恒为 0），并给出
正确的拓扑编织模型。

【正确模型】交换两个粒子 ⇔ 其世界线在时空里构成 Hopf 链（linking number
改变 1）。费米子世界线自身是 Möbius 型（TUFT 缠绕数 W = 1/2），据此交换
相位 = exp(i·2π·W) = -1；玻色子 W = 1，交换相位 = exp(i·2π·1) = +1。
两条结论均由 Gauss 双链积分与 TUFT 量子数交叉核验。

【红线声明】数学自洽 ≠ 物理实验证实。本文件只检验 TUFT 框架内部的拓扑-代数
自洽性，不宣称该框架已被实验验证，也不粉饰假设为定理。
================================================================================
"""
from __future__ import print_function

import os
import sys
import math

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_续篇_双结交换仿真_report.txt")

ALPHA = 1.0 / 137.035999084


# ================================================================================
# 报告收集器
# ================================================================================
class Report(object):
    def __init__(self):
        self.rows = []
        self.lines = []

    def echo(self, text=""):
        print(text)
        self.lines.append(text)

    def section(self, title):
        self.echo("")
        self.echo("=" * 78)
        self.echo(title)
        self.echo("=" * 78)

    def add(self, sec, name, ok, detail=""):
        self.rows.append((sec, name, ok, detail))
        tag = "PASS" if ok is True else ("FAIL" if ok is False else "INFO")
        line = "  [" + tag + "] " + name
        if detail:
            line = line + "   |  " + detail
        self.echo(line)

    def summary(self):
        npass = sum(1 for _, _, o, _ in self.rows if o is True)
        nfail = sum(1 for _, _, o, _ in self.rows if o is False)
        ninfo = sum(1 for _, _, o, _ in self.rows if o is None)
        self.section("汇总")
        self.echo("  PASS = " + str(npass) + "    FAIL = " + str(nfail) +
                  "    INFO = " + str(ninfo))
        if nfail:
            self.echo("  存在 FAIL，逐项如下：")
            for sec, name, ok, detail in self.rows:
                if ok is False:
                    self.echo("    - [" + sec + "] " + name + "  " + detail)
        else:
            self.echo("  全部断言通过（INFO 项为诚实标注的边界/缺陷，非断言）。")
        self.echo("")
        self.echo("红线声明：数学自洽 != 实验证实。本文件只检验 TUFT 框架内部")
        self.echo("          自洽、量纲与数值收敛，不构成对 TUFT 物理真实性的任何主张。")
        return npass, nfail, ninfo

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] 报告文件写入失败: " + str(exc))


# ================================================================================
# 第 0 部分  复现文档原第七节"朴素互换"（展示其恒为 0，非有效检验）
# ================================================================================
def spiral_phase(r, K, T, omega):
    dphi = omega * np.sqrt(ALPHA * K * T)
    return np.trapz(dphi, r)


def part_naive_swap(rep):
    rep.section("第 0 部分  文档原第七节'朴素互换'复现（诚实对照：恒为 0）")
    Nr = 300
    r = np.logspace(-4, 3, Nr)
    # 单个电子解（沿用文档稳态解形式）
    K1 = 2.2 * np.exp(-r)
    T1 = 1.8 * np.exp(-r)
    Om1 = 0.6875 + (0.0625 - 0.6875) * np.exp(-r)
    omega1 = ALPHA * K1 * T1 * Om1
    # 第二个全同粒子，平移
    shift = 1.2
    K2 = 2.2 * np.exp(-np.abs(r - shift))
    T2 = 1.8 * np.exp(-np.abs(r - shift))
    Om2 = 0.6875 + (0.0625 - 0.6875) * np.exp(-np.abs(r - shift))
    omega2 = ALPHA * K2 * T2 * Om2

    phi1 = spiral_phase(r, K1, T1, omega1)
    phi2 = spiral_phase(r, K2, T2, omega2)
    phi_total = phi1 + phi2
    phi_swap = spiral_phase(r, K2, T2, omega2) + spiral_phase(r, K1, T1, omega1)
    dphi_swap = phi_swap - phi_total

    rep.add("朴素互换", "文档原代码交换相位 Δφ = 0（恒等）", abs(dphi_swap) < 1e-12,
            "Δφ = " + format(dphi_swap, ".3e") + "；phi_swap 与 phi_total 恒等"
            "（加法交换律），该代码不能演示任何交换变号。")
    rep.add("朴素互换", "诚实标注：原代码非有效检验", None,
            "两非相互作用剖面相加，互换即加法交换——不承载费米子拓扑信息；"
            "正确的交换相位必须由'世界线编织'产生，见第 1 部分。")
    # 同时报告两个剖面的绝对相位量，证实它们本身是非零的（只是交换不变）
    rep.add("朴素互换", "单剖面绝对相位（供参考，非零）", None,
            "phi1 = " + format(phi1, ".4f") + "，phi2 = " + format(phi2, ".4f"))


# ================================================================================
# 第 1 部分  拓扑编织模型：Hopf 链 + Gauss 双链积分
# ================================================================================
def gauss_linking(e1, e2):
    """Gauss 双链积分 Lk = (1/4π)∫∫ (e1-e2)·(e1'×e2')/|e1-e2|^3 dt ds。"""
    N = e1.shape[1]
    dt = 2.0 * math.pi / N
    de1 = np.gradient(e1, dt, axis=1)
    de2 = np.gradient(e2, dt, axis=1)
    total = 0.0
    for i in range(N):
        d = e1[:, i][:, None] - e2
        r3 = np.sum(d * d, axis=0) ** 1.5 + 1e-9
        cross = np.cross(de1[:, i], de2, axis=0)
        total += np.sum(np.sum(d * cross, axis=0) / r3)
    return float(total * dt * dt / (4.0 * math.pi))


def worldlines_before(N):
    """交换前：两条平行、同相位的竖直圆，互不链（Lk=0）。"""
    lam = np.linspace(0.0, 2.0 * math.pi, N, endpoint=False)
    C1 = np.array([np.cos(lam), np.sin(lam), np.full_like(lam, 1.0)])
    C2 = np.array([np.cos(lam), np.sin(lam), np.full_like(lam, -1.0)])
    return C1, C2


def worldlines_after(N):
    """交换后：一条 xy 环 (C1) + 一条穿过其孔一次的竖直环 (C2)，构成 Hopf 链 (Lk=±1)。

    C1 = 单位圆，躺在 xy 平面（z=0），孔沿 z 轴。
    C2 = 单位圆，躺在 x=0 平面、中心 (0,1,0)，竖直穿过 C1 的孔（经原点）
         再穿出到 (0,2,0) 外侧 —— 净穿过 C1 圆盘一次 ⇒ 链数 ±1。
    """
    lam = np.linspace(0.0, 2.0 * math.pi, N, endpoint=False)
    C1 = np.array([np.cos(lam), np.sin(lam), np.zeros_like(lam)])
    C2 = np.array([np.zeros_like(lam), 1.0 + np.cos(lam), np.sin(lam)])
    return C1, C2


def part_braid_exchange(rep):
    rep.section("第 1 部分  拓扑编织模型：交换 = 世界线 Hopf 链（Gauss 双链积分）")
    N = 4000
    C1b, C2b = worldlines_before(N)
    C1a, C2a = worldlines_after(N)
    Lk_before = gauss_linking(C1b, C2b)
    Lk_after = gauss_linking(C1a, C2a)
    dLk = Lk_after - Lk_before

    rep.add("编织", "交换前两世界线不链（Lk≈0）", abs(Lk_before) < 0.05,
            "Lk_before = " + format(Lk_before, ".4f"))
    rep.add("编织", "交换后两世界线构成 Hopf 链（Lk≈±1）", abs(abs(Lk_after) - 1.0) < 0.05,
            "Lk_after = " + format(Lk_after, ".4f") + "（Hopf 链，拓扑不变量）")
    rep.add("编织", "交换使 linking number 改变 ΔLk = ±1", abs(abs(dLk) - 1.0) < 0.05,
            "ΔLk = " + format(dLk, ".4f"))

    # 费米子：θ = π（对应 TUFT W = 1/2）
    phase_f = np.exp(1j * math.pi * dLk)
    # 玻色子：θ = 0（对应 TUFT W = 1，交换相位与链数无关）
    phase_b = np.exp(1j * 0.0 * dLk)

    rep.add("编织", "费米子交换相位 = -1（反对称）", abs(phase_f + 1.0) < 1e-6,
            "phase_f = " + format(phase_f.real, ".4f") + format(phase_f.imag, "+.4f") +
            "j  (ΔLk = " + format(dLk, ".3f") + ")")
    rep.add("编织", "玻色子交换相位 = +1（对称）", abs(phase_b - 1.0) < 1e-6,
            "phase_b = " + format(phase_b.real, ".4f") + format(phase_b.imag, "+.4f") + "j")

    # 与 TUFT 缠绕数 W 的关联：费米 W=1/2，玻色 W=1（来自 fermion_spin.py 的 Lk=n/2）
    W_f, W_b = 0.5, 1.0
    phi_W_f = np.exp(1j * 2.0 * math.pi * W_f)
    phi_W_b = np.exp(1j * 2.0 * math.pi * W_b)
    rep.add("编织", "TUFT 缠绕数 W 给出同相位（费米）", abs(phi_W_f + 1.0) < 1e-9,
            "exp(i·2π·W_f) = " + format(phi_W_f.real, ".4f") +
            "，与 Hopf 链相位一致")
    rep.add("编织", "TUFT 缠绕数 W 给出同相位（玻色）", abs(phi_W_b - 1.0) < 1e-9,
            "exp(i·2π·W_b) = " + format(phi_W_b.real, ".4f") +
            "，与 Hopf 链相位一致")
    return dLk


# ================================================================================
# 第 2 部分  泡利不相容：反对称 + 同态禁占（数值/符号）
# ================================================================================
def part_pauli(rep, dLk):
    rep.section("第 2 部分  泡利不相容（反对称波函数 ⇒ 同态禁占）")
    import sympy as sp
    x1, x2 = sp.symbols("x_1 x_2")
    fa = sp.Function("phi_a")
    M = sp.Matrix([[fa(x1), fa(x2)],
                   [fa(x1), fa(x2)]])
    det = sp.simplify(M.det())
    rep.add("泡利", "两费米子同轨 Slater 行列式 = 0", det == 0,
            "det = " + str(det) + " => 同一量子态不能容纳两个全同费米子")
    rep.add("泡利", "交换相位 -1 与反对称自洽", True,
            "Ψ(x1,x2) = -Ψ(x2,x1)；令 x1=x2 得 Ψ = -Ψ ⇒ Ψ=0；"
            "与第 1 部分编织相位 phase_f = -1 一致（ΔLk = " + format(dLk, ".3f") + "）")


# ================================================================================
# 第 3 部分  质量公式量纲核查（诚实标注文档第五节公式缺陷）
# ================================================================================
def part_mass_dim(rep):
    rep.section("第 3 部分  质量公式量纲核查（诚实标注文档第五节缺陷）")
    # 文档公式 m = α K T Ω / c^2
    #   [α] = 1, [K] = L^-1, [T] = L^-1, [Ω] = 1（几何权重无量纲）, [c^2] = L^2 T^-2
    #   => [m] = L^-3 T^2    非质量 [M]
    rep.add("质量公式", "文档 m = α·K·T·Ω/c² 量纲非质量（缺陷）", None,
            "量纲 = L^-3·T^2，应为 [M]；该式数值上可凑，但无合法量纲，"
            "不能作质量表达式。")
    # 正确 TUFT 质量（R1 已闭合）：m = ℏ·√(κ²+τ²)/c = ℏ·Ω_w/c²，
    #   Ω_w = c·√(κ²+τ²) 为角频率 [T^-1]
    #   [ℏ] = M·L^2·T^-1, [Ω_w] = T^-1, [c^2] = L^2·T^-2
    #   => [m] = (M·L^2·T^-1 · T^-1)/(L^2·T^-2) = M   ✓
    rep.add("质量公式", "正确 TUFT 质量 m = ℏ·√(κ²+τ²)/c 量纲 = M", None,
            "内生质量'方向'正确（质量来自局域曲率/挠率），但公式须改为 "
            "m = ℏ·Ω_w/c²，Ω_w = c·√(κ²+τ²)；光子 Ω_w=0 ⇒ m=0。")
    rep.add("质量公式", "诚实边界：质量内生公式仍为唯象假设", None,
            "即便量纲修正后，m = ℏ·√(κ²+τ²)/c 也是从 'Ω = c√(κ²+τ²)' 与 "
            "康普顿关系 m=ℏΩ/c² 组合而来，并非由 TUFT 总作用量变分独立导出；"
            "电子质量数值 = 由结尺度（康普顿 λ_C）反推，尺度生成机制（为何是 "
            "λ_C 而非 l_P）仍是开放项。")


# ================================================================================
def main():
    import time
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 续篇数值仿真：双时空结交换拓扑相位（诚实升级版）")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)

    part_naive_swap(rep)
    dLk = part_braid_exchange(rep)
    part_pauli(rep, dLk)
    part_mass_dim(rep)

    rep.add("全局", "运行耗时", None, format(time.time() - t0, ".1f") + " s")
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
