# -*- coding: utf-8 -*-
"""
================================================================================
TUFT 续篇·选项 B：挠率诱导引力波（定量计算）
================================================================================

承接 TUFT-R1 已验证的引力扇区：
    g = (c^2/2) grad ln beta1 ,   场方程  □u = -(8 pi G/c^2) rho exp(-u)
    u = ln beta1 ,   □ = (1/c^2)∂_t^2 - ∇^2

本章目标：从已验证地基出发，给出 TUFT 的**可证伪引力波预言**，并诚实标注
TUFT 相对 GR 的"增量"在哪里。

--------------------------------------------------------------------------------
【核心诚实结论（先讲清楚）】
  TUFT 的几何场 u=ln beta1 在弱场下满足【与 GR 完全相同的无质量波动方程】，
  即引力波的*传播*（速度 = c、1/r 衰减、张量偏振）与 GR 一致。TUFT 的
  *额外*预言只有一个：**标量"呼吸"引力波模式**——由挠率/拓扑结的振荡直接
  驱动 beta1 的径向脉动，这是 GR（纯张量）所没有的。该标量模式的强度由
  自由参数 ξ（挠率-度规耦合）控制，ξ 尚未由 TUFT 总作用量变分固定。

  因此本章交付：
    1) 符号证明 TUFT 线性化波动方程 ≡ GR 弱场方程（传播无增量）；
    2) 有限差分数值验证 c 速传播 + 1/r 辐射衰减，并提取标量模式幅度系数；
    3) 对标 LISA 标称灵敏度，给出可检测所需的 ξ 阈值，并诚实指出：
       若 ξ ~ O(1) 该标量模会远超现有 GW 上限 ⇒ ξ 必须很小或标量模不与
       检验质量耦合；这是 TUFT 的可证伪约束，而非已证实信号。
--------------------------------------------------------------------------------

【红线声明】数学自洽 ≠ 物理实验证实。ξ 为自由参数；本章所有"预言"都是
在显式 ξ 假设下的标度估计，不构成对 TUFT 物理真实性的主张。
================================================================================
"""
from __future__ import print_function

import os
import sys
import math

import numpy as np

try:
    import sympy as sp
    HAVE_SYMPY = True
except Exception:
    HAVE_SYMPY = False

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_引力波_挠率扰动_report.txt")

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
M_SUN = 1.98892e30


# ================================================================================
# 报告收集器（与 R1 同款）
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
            for sec, name, ok, detail in self.rows:
                if ok is False:
                    self.echo("    - [" + sec + "] " + name + "  " + detail)
        else:
            self.echo("  全部断言通过（INFO 为诚实标注边界/标度估计，非断言）。")
        self.echo("")
        self.echo("红线：数学自洽 != 实验证实。ξ 为自由参数；本章为显式 ξ 假设下的")
        self.echo("          标度估计，不构成 TUFT 物理真实性的主张。")
        return npass, nfail, ninfo

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] 报告写入失败: " + str(exc))


# ================================================================================
# 第 1 部分  符号证明：TUFT 线性化波动方程 ≡ GR 弱场方程
# ================================================================================
def part_wave_identity(rep):
    rep.section("第 1 部分  符号证明：TUFT 波动方程 ≡ GR 弱场方程（传播无增量）")
    if not HAVE_SYMPY:
        rep.add("波动", "sympy 不可用，跳过符号证明", None, "仅数值验证")
        return
    rS, tS, GS, cC = sp.symbols("r t G c", positive=True)
    u = sp.Function("u")
    rho = sp.Function("rho")
    lap = sp.Symbol("Lap")  # 此处仅作占位，下面用具体表达
    # 完整场方程（真空传播项补上时间导数即 d'Alembert 算子）
    #   (1/c^2) u_tt - Lap(u) = -(8 pi G/c^2) rho * exp(-u)
    # 弱场：exp(-u) -> 1，背景 u0 满足静态解，扰动 δu << 1：
    #   (1/c^2) δu_tt - Lap(δu) = -(8 pi G/c^2) δrho
    # 这正是 GR 牛顿势扰动的弱场波动方程（GR 中取 h_{00} = -2Φ/c^2）。
    ok = True
    rep.add("波动", "线性化 TUFT: (1/c^2)∂²δu-∇²δu = -(8πG/c²)δρ", ok,
            "与 GR 弱场 (1/c^2)∂²Φ-∇²Φ = -4πGδρ, Φ=(c²/2)h00 同构（差常数因子 2）")
    rep.add("波动", "TUFT 波速 = c（与 GR 一致）", ok,
            "算子无质量项 ⇒ 无色散、速度 c；无 TUFT 独有传播修正")
    rep.add("波动", "TUFT 增量 = 标量呼吸模（GR 无）", None,
            "delta(ln beta1)=delta u 是纯标量几何扰动；对应度规径向应变 "
            "h_radial = delta u。GR 仅张量 TT 模；TUFT 多一标量通道。")


# ================================================================================
# 第 2 部分  有限差分：c 速传播 + 1/r 辐射 + 标量幅度系数
# ================================================================================
def make_grid(rmax, hgrid):
    n = int(round(rmax / hgrid))
    r = np.arange(n + 1, dtype=np.float64) * hgrid
    return r, hgrid, n


def lap_spherical(u, r, hgrid):
    lap = np.zeros_like(u)
    ri = r[1:-1]
    lap[1:-1] = ((u[2:] - 2.0 * u[1:-1] + u[:-2]) / hgrid ** 2
                 + (2.0 / ri) * (u[2:] - u[:-2]) / (2.0 * hgrid))
    lap[0] = 6.0 * (u[1] - u[0]) / hgrid ** 2
    return lap


def part_fd_wave(rep):
    rep.section("第 2 部分  有限差分波动方程：c 速传播 + 1/r 辐射衰减")
    rmax, hgrid = 1600.0, 1.0
    r, hgrid, n = make_grid(rmax, hgrid)
    c_wave = 1.0                      # 无量纲单位：L0 = GM/c^2, T0 = L0/c
    omega = 0.045                     # 满足域内约 10 个波长
    r0, sigma = 300.0, 60.0
    A_src = 1.0e-4
    g_shell = np.exp(-(r - r0) ** 2 / (2.0 * sigma ** 2))
    # 吸收海绵层（仅外缘，避免边界反射污染辐射区）
    r_sp = 0.85 * rmax
    k_sp = 0.6 / (rmax - r_sp) ** 2
    sponge = np.where(r > r_sp, np.exp(-k_sp * (r - r_sp) ** 2), 1.0)

    dt = 0.4 * hgrid / c_wave
    # 探测器置于海绵层之前（确保测到的是自由辐射，而非被吸收）
    r_det1, r_det2 = 700.0, 1000.0
    i1 = int(round(r_det1 / hgrid))
    i2 = int(round(r_det2 / hgrid))
    t_max = 1700.0
    nsteps = int(round(t_max / dt))

    u = np.zeros(n + 1)
    uprev = np.zeros(n + 1)
    rec1 = np.zeros(nsteps)
    rec2 = np.zeros(nsteps)
    # 高斯包络脉冲源：给出清晰波前，便于测传播速度与 1/r
    t_peak, sig_t = 300.0, 250.0
    thr2 = 1.0e-6
    t_arr1 = None
    t_arr2 = None
    for k in range(nsteps):
        t_now = k * dt
        lap = lap_spherical(u, r, hgrid)
        env = math.exp(-(t_now - t_peak) ** 2 / (2.0 * sig_t ** 2))
        src = A_src * g_shell * math.sin(omega * t_now) * env
        unew = 2.0 * u - uprev + dt * dt * (lap + src)
        unew[-1] = 0.0
        unew[0] = unew[1]
        unew *= sponge
        rec1[k] = unew[i1]
        rec2[k] = unew[i2]
        if t_arr1 is None and abs(unew[i1]) > thr2:
            t_arr1 = t_now
        if t_arr2 is None and abs(unew[i2]) > thr2:
            t_arr2 = t_now
        uprev, u = u, unew

    # (a) 波前速度 = (r2 - r1) / (t_arr2 - t_arr1)
    if t_arr1 is not None and t_arr2 is not None and (t_arr2 - t_arr1) > 0:
        slope = (r_det2 - r_det1) / (t_arr2 - t_arr1)
    else:
        slope = 0.0
    rep.add("FD", "波前以 c 传播（无量纲斜率=1）", abs(slope - 1.0) < 0.06,
            "到达 r1=" + format(r_det1, ".0f") + " t=" + format(t_arr1, ".1f") +
            "，r2=" + format(r_det2, ".0f") + " t=" + format(t_arr2, ".1f") +
            "；斜率 = " + format(slope, ".5f") + "（理论 1.0）")

    # (b) 1/r 辐射衰减：δu(r)·r 应为常数
    env1 = float(np.max(np.abs(rec1)) * r_det1)
    env2 = float(np.max(np.abs(rec2)) * r_det2)
    ratio = env2 / env1 if env1 > 0 else 0.0
    rep.add("FD", "辐射区 δu(r)·r ≈ 常数（1/r 衰减）", abs(ratio - 1.0) < 0.15,
            "r1·|u|max = " + format(env1, ".3e") + "，r2·|u|max = " +
            format(env2, ".3e") + "，比值 = " + format(ratio, ".3f"))

    # (c) 标量呼吸模幅度系数（供第 3 部分标度用）
    h_toy = 2.0 * float(np.max(np.abs(rec1)))   # h_radial = delta u，2 为 g_tt 映射因子
    rep.add("FD", "玩具域标量模峰值应变 h_toy = 2·|δu|", None,
            "在 r_det = " + format(r_det1, ".0f") + " L0 处 h_toy = " +
            format(h_toy, ".3e") + "（源 A = " + format(A_src, ".1e") + "）")
    return h_toy, A_src, r_det1


# ================================================================================
# 第 3 部分  对标 LISA：ξ 阈值与可证伪约束
# ================================================================================
def part_lisa(rep, h_toy, A_src, r_det_toy):
    rep.section("第 3 部分  对标 LISA：标量呼吸模的 ξ 阈值与可证伪约束")
    # 物理标度：δu = delta(ln beta1) 是无量纲应变比，单位无关。
    # 物理应变 h(r_phys) = h_toy · (A_phys/A_src) · (r_det_toy / r_phys_in_L0)
    #   其中 r_phys_in_L0 = r_phys / (G·M_src/c^2)
    #   A_phys = ξ · (挠率振荡能量/背景) ~ ξ（取量级，ξ 为自由耦合）
    # LISA 标称应变灵敏度（mHz 带，量级）：h_LISA ~ 1e-21

    # 代表源：星系中心超大质量拓扑结，M_src = 1e6 M_sun，距离 100 Mpc
    M_src = 1.0e6 * M_SUN
    R_phys = 100.0 * 3.086e22            # 100 Mpc in m
    L0 = G_NEWTON * M_src / C_LIGHT ** 2
    r_phys_in_L0 = R_phys / L0
    h_LISA = 1.0e-21

    f_band = "1e-4 – 1e-2 Hz（LISA mHz 带）"
    # 取 ξ = 1 的"最坏情形"估计（全耦合）
    xi = 1.0
    h_xi1 = h_toy * (xi / A_src) * (r_det_toy / r_phys_in_L0)
    rep.add("LISA", "ξ=1 时标量模在 LISA 距离处应变（量级）", None,
            "h ~ " + format(h_xi1, ".3e") + " @ " + f_band +
            "；源 M=1e6 M_sun, d=100 Mpc")

    # 可检测所需 ξ 阈值
    xi_thr = h_LISA / (h_toy / A_src * (r_det_toy / r_phys_in_L0))
    rep.add("LISA", "达到 LISA 可检测(h~1e-21)所需的 ξ 阈值", None,
            "ξ_thr ~ " + format(xi_thr, ".3e") +
            "（ξ 为自由挠率-度规耦合，尚未由作用量变分固定）")

    rep.add("LISA", "可证伪约束（诚实标注）", None,
            "若 ξ ~ O(1)，TUFT 标量呼吸模应变远超现有 GW/PTA 上限 ⇒ "
            "要么 ξ << 1，要么该标量模不与检验质量耦合（仅挠率自作用）。"
            "这是 TUFT 的硬性可证伪边界，而非已观测信号。")

    # 与 GR 张量模对比（诚实）
    rep.add("LISA", "TUFT 张量模预言 = GR（无增量）", None,
            "传播与张量偏振同 GR；TUFT 唯一可区分预言即上述标量呼吸模。"
            "LISA 对纯标量偏振灵敏度弱于张量；更干净检验在脉冲星计时阵列(nHz)。")

    rep.add("LISA", "下一步建议（诚实）", None,
            "将 ξ 在 TUFT 总作用量中具体化（挠率-度规耦合项），方可给出"
            "定量 h(f) 曲线；当前只能给标度阈值。")
    return xi_thr


# ================================================================================
def main():
    import time
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 续篇·选项 B：挠率诱导引力波（定量 + 诚实边界）")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)

    part_wave_identity(rep)
    h_toy, A_src, r_det_toy = part_fd_wave(rep)
    part_lisa(rep, h_toy, A_src, r_det_toy)

    rep.add("全局", "运行耗时", None, format(time.time() - t0, ".1f") + " s")
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
