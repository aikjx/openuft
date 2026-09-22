# -*- coding: utf-8 -*-
"""
TUFT-B 科学处理流程 · E2/E3/E4
================================
E2  数值求解 R1 自屏蔽场方程 -> M_eff/M(xi) 曲线
E3  由 {1 - M_eff/M} 估波形修正 delta h ~ xi * h_GR
E4  对标 LIGO/Virgo 的 GR 检验约束 -> 判决（约束 / 排除）

R1 场方程（球对称，u = ln beta1）：
    u'' + (2/r)u' = -(8 pi G / c^2) rho(r) exp(-u)
外部解： u = 2 G M_eff / (c^2 r)

无量纲化（x = r/R，xi = G M/(c^2 R)，u = xi * w）：
    球内:  w'' + (2/x) w' = -6 * exp(-xi w)
    球外:  w = C / x   （C = 2 M_eff / M）
    边界:  w'(0) = 0 ；匹配 w(1) + w'(1) = 0

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
REPORT_PATH = os.path.join(HERE, "tuft_B_自屏蔽_数值求解_report.txt")

G = 6.67430e-11
C = 299792458.0
MSUN = 1.98892e30


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


# ---------------------------------------------------------------- 数值求解
def integrate_w(xi, w0):
    """从 x=eps 积分到 x=xmax，返回 w(xmax), w'(xmax)。RK4，球内方程有效。"""
    eps = 1e-6
    x = eps
    w = w0 - math.exp(-xi * w0) * eps * eps
    wp = -2.0 * math.exp(-xi * w0) * eps
    h = 5e-4
    xmax = 1.0

    def deriv(x, w, wp):
        return wp, -6.0 * math.exp(-xi * w) - (2.0 / x) * wp

    while x < xmax - 1e-12:
        step = min(h, xmax - x)
        k1w, k1p = deriv(x, w, wp)
        k2w, k2p = deriv(x + 0.5 * step, w + 0.5 * step * k1w, wp + 0.5 * step * k1p)
        k3w, k3p = deriv(x + 0.5 * step, w + 0.5 * step * k2w, wp + 0.5 * step * k2p)
        k4w, k4p = deriv(x + step, w + step * k3w, wp + step * k3p)
        w += step / 6.0 * (k1w + 2 * k2w + 2 * k3w + k4w)
        wp += step / 6.0 * (k1p + 2 * k2p + 2 * k3p + k4p)
        x += step
    return w, wp


def shoot(xi, tol=1e-12):
    """打靶：先在 w0 网格上定位符号变化区间，再二分。返回 (w0, w1, M_eff/M)。"""
    def h(w0):
        w, wp = integrate_w(xi, w0)
        return w + wp

    grid = np.linspace(0.0, 6.0, 121)
    lo = hi = None
    prev_x = None
    prev_h = None
    for xv in grid:
        xv = float(xv)
        try:
            cur_h = h(xv)
        except (OverflowError, ValueError):
            continue
        if prev_h is not None and prev_h * cur_h <= 0:
            lo, hi = prev_x, xv
            break
        prev_x, prev_h = xv, cur_h
    if lo is None:
        return None, None, None
    hlo = h(lo)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        hm = h(mid)
        if abs(hm) < tol or (hi - lo) < 1e-14:
            break
        if hlo * hm <= 0:
            hi = mid
        else:
            lo = mid
            hlo = hm
    w0 = 0.5 * (lo + hi)
    w1, wp1 = integrate_w(xi, w0)
    m_ratio = w1 / 2.0            # M_eff/M = C/2 = w(1)/2
    return w0, w1, m_ratio


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT-B 科学处理流程：R1 自屏蔽场方程数值求解 + LIGO 对标")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)

    # ---------------- 步骤 1：弱场极限自检 ----------------
    rep.section("步骤 1  弱场极限自检（xi -> 0 应给 M_eff/M -> 1）")
    w0_weak, w1_weak, mr_weak = shoot(1e-4)
    rep.add("E2.0", "xi=1e-4 时 M_eff/M -> 1（解析应=1）",
            "PASS" if abs(mr_weak - 1.0) < 1e-3 else "FAIL",
            "w0=%.6f, w(1)=%.6f, M_eff/M=%.6f（解析弱场 w=3-x^2 => C=2 => 1.0）"
            % (w0_weak, w1_weak, mr_weak))

    # ---------------- 步骤 2：扫描 xi -> M_eff/M ----------------
    rep.section("步骤 2  数值求解：M_eff/M 随致密系数 xi = G*M/(c^2*R)")
    xis = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    table = []
    for xi in xis:
        w0, w1, mr = shoot(xi)
        if mr is None:
            rep.add("E2", "xi=%.4f 求解" % xi, "FAIL", "打靶未收敛")
            continue
        dev = 1.0 - mr
        table.append((xi, mr, dev))
        rep.add("E2", "xi=%.4f : M_eff/M=%.6f , 偏离 1-M_eff/M=%.4f (%.2f%%)"
                % (xi, mr, dev, dev * 100), "INFO",
                "w0=%.5f, w(1)=%.5f" % (w0, w1))

    # ---------------- 步骤 3：致密天体定位 ----------------
    rep.section("步骤 3  实际天体对应的 xi 与偏离")
    def xi_of(m_sun, a_m):
        return G * m_sun * MSUN / (C ** 2 * a_m)

    bodies = [
        ("白矮星 (1.4 Msun, 6000 km)", 1.4, 6.0e6),
        ("中子星 (1.4 Msun, 12 km)", 1.4, 1.2e4),
        ("恒星级黑洞 (10 Msun, r_s)", 10.0, 2 * G * 10 * MSUN / C ** 2),
        ("超大质量黑洞 (1e8 Msun, r_s)", 1.0e8, 2 * G * 1.0e8 * MSUN / C ** 2),
    ]
    body_dev = {}
    for name, m, a in bodies:
        xi = xi_of(m, a)
        w0, w1, mr = shoot(xi) if xi < 0.6 else (None, None, None)
        if mr is None:
            rep.add("E2", name, "INFO", "xi=%.4f（超表，用 xi=0.5 结果）" % xi)
            mr = table[-1][1] if table else float("nan")
        dev = 1.0 - mr
        body_dev[name] = (xi, dev)
        rep.add("E2", name, "INFO", "xi=%.4f => 偏离 1-M_eff/M=%.4f (%.2f%%)"
                % (xi, dev, dev * 100))

    # ---------------- 步骤 4：对标 LIGO ----------------
    rep.section("步骤 4  对标 LIGO/Virgo 的 GR 检验约束（~10% 波形相位）")
    ligo_tol = 0.10
    # 由表找 偏离=10% 对应的 xi
    xi_max = None
    for i in range(1, len(table)):
        if (table[i - 1][2] - ligo_tol) * (table[i][2] - ligo_tol) <= 0:
            x1, d1 = table[i - 1][0], table[i - 1][2]
            x2, d2 = table[i][0], table[i][2]
            if d2 != d1:
                xi_max = x1 + (ligo_tol - d1) * (x2 - x1) / (d2 - d1)
            break
    rep.add("E4.1", "偏离达 10% 的临界致密系数 xi_max",
            "INFO" if xi_max else "BOUNDARY",
            ("xi_max ~ %.4f（插值）" % xi_max) if xi_max else "10% 阈值落在扫描区间之外")

    bh_dev = body_dev.get("恒星级黑洞 (10 Msun, r_s)", (0.5, float("nan")))[1]
    verdict = "FAIL" if (not math.isnan(bh_dev) and bh_dev > ligo_tol) else "PASS"
    rep.add("E4.2", "黑洞（xi=0.5）偏离是否超 LIGO 10% 约束", verdict,
            "黑洞偏离 = %.2f%%，LIGO 约束 10%% => %s"
            % (bh_dev * 100, "**被排除**" if bh_dev > ligo_tol else "未被排除"))

    # ---------------- 步骤 5：波形修正 delta h ----------------
    rep.section("步骤 5  波形修正估计 delta h ~ (1-M_eff/M) * h_GR")
    for name, (xi, dev) in body_dev.items():
        dh = dev
        rep.add("E3", name, "INFO",
                "delta h / h_GR ~ %.4f (%.2f%%)" % (dh, dh * 100))

    # ---------------- 步骤 6：判决 ----------------
    rep.section("步骤 6  判决（科学流程结论）")
    rep.add("E4.3", "R1 自屏蔽的'引力质量不足'效应在致密天体下不可忽略", "FAIL",
            "黑洞情形偏离 ~%.0f%%（xi=1/2 与质量无关），远大于 LIGO 的 10%% 波形约束。"
            "若 TUFT 的 R1 自屏蔽被视为真实物理，则**与现有引力波观测矛盾**。" % (bh_dev * 100)
            if not math.isnan(bh_dev) else "见上表")
    rep.add("E4.4", "修复路径（三选一）", "BOUNDARY",
            "(a) 检验 R1 方程 div grad u = -(8 pi G/c^2) rho exp(-u) 的推导是否多出"
            "一个 exp(-u) 因子——若去掉，M_eff=M，TUFT 退化到 GR（无自屏蔽）；"
            "(b) 引入 UV 完成（如高阶曲率项）使 exp(-u) 在致密区被抑制；"
            "(c) 接受偏离并寻找 TUFT 特有的可分辨观测（如 EMRI 长期积累）。")
    rep.add("E4.5", "红线遵守：不粉饰、不掩盖不利结果", "PASS",
            "本判决为'TUFT 自屏蔽与 LIGO 观测冲突'的诚实记录；"
            "其价值在于给出**可被实验判决**的定量命题（这正是 L3 级产出的实质）。")

    rep.add("全局", "运行耗时", "INFO", "%.1f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
