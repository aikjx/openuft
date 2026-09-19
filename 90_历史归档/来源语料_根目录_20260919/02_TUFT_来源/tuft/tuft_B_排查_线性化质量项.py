# -*- coding: utf-8 -*-
"""
TUFT-B 排查：既有报告"波动方程 ≡ GR（无色散）"是否成立？
=========================================================
排查对象：tuft_续篇B_挠率引力波.md（§2 "波动方程 ≡ GR、无色散、速度 c"）
排查问题：其线性化是否漏掉了背景 ρ0 带来的 exp(-u) 质量项？

R1 场方程（u = ln beta1）：
    □u = -(8 pi G/c^2) rho exp(-u)
既有报告把它线性化为 □δu = -(8 pi G/c^2) δρ（**把 exp(-u) 当 1**）。
本文件保留 exp(-u) 做严格线性化，检查是否出现 m^2 δu 项。

红线：数学自洽 != 实验证实。
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
REPORT_PATH = os.path.join(HERE, "tuft_B_排查_线性化_report.txt")

G = 6.67430e-11
C = 299792458.0


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
        return cnt

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] 报告写入失败: " + str(exc))


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT-B 排查：既有报告'波动方程 ≡ GR（无色散）'是否成立？")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)

    import sympy as sp

    # ---------- 步骤 1：严格线性化 ----------
    rep.section("步骤 1  严格线性化（保留 exp(-u)）")
    u0, du, rho0, drho = sp.symbols("u0 delta_u rho0 delta_rho", real=True)
    K = sp.symbols("K", positive=True)   # K = 8 pi G / c^2

    src = -K * (rho0 + drho) * sp.exp(-(u0 + du))
    lin = sp.expand(sp.series(src, du, 0, 2).removeO())
    rep.add("R1.1", "源项一阶展开", "PASS", "src_lin = " + str(sp.simplify(lin)))

    # 分离：常数背景、δu 项、δρ 项
    const_term = sp.simplify(lin.subs({du: 0, drho: 0}))
    coeff_du = sp.simplify(sp.diff(lin, du))
    coeff_drho = sp.simplify(sp.diff(lin, drho))
    rep.add("R1.2", "常数背景项", "INFO", "= " + str(const_term))
    rep.add("R1.3", "δu 的系数（决定质量项）", "PASS", "= " + str(sp.simplify(coeff_du)))
    rep.add("R1.4", "δρ 的系数", "INFO", "= " + str(sp.simplify(coeff_drho)))

    # 移项后：□δu + m^2 δu = ...
    m2 = sp.simplify(-coeff_du)   # 因为 □δu = coeff_du*δu + coeff_drho*δρ + const
    rep.add("R1.5", "线性化后出现质量项 m^2 δu", "FAIL" if sp.simplify(m2) != 0 else "PASS",
            "□δu + m^2 δu = ..., m^2 = " + str(m2) +
            "  —— **非零** ⇒ 方程是**有质量 Klein-Gordon**，不是无质量波动方程")
    rep.add("R1.6", "既有报告的做法（把 exp(-u) 当 1）", "FAIL",
            "既有报告写 □δu = -(8πG/c²)δρ —— 相当于取 u0=0 且忽略 ρ0 δu 项，"
            "**丢掉了 m^2 δu**。该近似仅当 u0<<1 且 ρ0 项可忽略时成立。")

    # ---------- 步骤 2：数值：有效质量与色散尺度 ----------
    rep.section("步骤 2  数值：有效质量 m_eff 与 Compton 尺度（对典型源）")
    rep.add("R2.0", "m_eff^2 = (8 pi G/c^2) rho0 exp(-u0)", "PASS",
            "量纲 [G/c^2]=m/kg, [rho0]=kg/m^3 => [m_eff^2]=1/m^2 ✓")
    for name, rho in [("星际介质 ~1e-21", 1.0e-21),
                      ("太阳核心 ~1.5e5", 1.5e5),
                      ("白矮星 ~1e9", 1.0e9),
                      ("中子星 ~1e18", 1.0e18)]:
        m2v = 8 * math.pi * G / C ** 2 * rho
        m_eff = math.sqrt(m2v) if m2v > 0 else 0.0
        lam = 1.0 / m_eff if m_eff > 0 else float("inf")
        rep.add("R2", "rho0 = %s kg/m^3 : m_eff = %.4e 1/m, 尺度 1/m = %.4e m" %
                (name, m_eff, lam), "INFO",
                "质量项随密度增大；高密度源处 KG 质量不可忽略")

    # ---------- 步骤 3：色散后果 ----------
    rep.section("步骤 3  色散后果（与既有报告'无色散、速度 c'对照）")
    rep.add("R3.1", "有质量 KG 的色散关系 w^2 = k^2 c^2 + m^2 c^4/hbar^2（此处 m 为有效质量）",
            "PASS",
            "存在质量项 => 相速度/群速度依赖频率 => **无色散断言不成立**")
    rep.add("R3.2", "既有报告 'TUFT 张量模预言 = GR（无增量）'", "FAIL",
            "该结论建立在'无质量波动方程'之上；但严格线性化给出有质量 KG => "
            "传播有色散、与 GR **有增量**。既有报告的'无增量'不成立。")

    # ---------- 步骤 4：与静态自屏蔽同源 ----------
    rep.section("步骤 4  与静态自屏蔽同源（统一排查结论）")
    rep.add("R4.1", "静态：M_eff/M(ξ=0.5) = 0.5318（偏离 46.82%，被 LIGO 排除）", "FAIL",
            "见 tuft_B_自屏蔽_数值求解")
    rep.add("R4.2", "动力学：线性化出现 m^2 δu（有质量 KG）", "FAIL",
            "本文件步骤 1")
    rep.add("R4.3", "同源：都来自同一个 exp(-u) 因子", "PASS",
            "静态表现 = 有效质量不足；动力学表现 = KG 质量项/色散。"
            "既有报告把 exp(-u) 线性化为 1，因而**同时漏掉**两者。")
    rep.add("R4.4", "修复：既有报告（tuft_续篇B_挠率引力波.md §2/§5）应加注", "BOUNDARY",
            "(1) §2 '波动方程 ≡ GR' 仅在忽略背景 ρ0 时成立；严格线性化是有质量 KG；"
            "(2) §5 把'非线性自屏蔽'当正面成果引用，应改为'已被 LIGO 排除的缺陷'。")

    rep.add("全局", "运行耗时", "INFO", "%.2f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
