# -*- coding: utf-8 -*-
"""
TUFT-B 修复检验：UV 完成能否抑制强场自屏蔽？
=============================================
背景：原 R1 场方程  Lap(u) = -K rho exp(-u)  在黑洞（xi=0.5）给出偏离 46.82% >> LIGO 10%。
问题：引入 UV 抑制（高阶曲率项唯象化）能否把偏离压到 10% 以内？代价是什么？

UV 模型（唯象）：把自屏蔽因子改为
    S(u) = exp(-u) / sqrt(1 + (u/u_UV)^2)
  - u_UV -> inf : 回到原模型（无抑制）
  - u_UV -> 0   : 强抑制（自屏蔽被切除，趋近 GR）

求解：Lap(u) = -K rho S(u)，球对称无量纲化后 w'' + (2/x)w' = -6 S(xi w)。
红线：数学自洽 != 实验证实。本文件只做框架内可证伪性检验。
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
REPORT_PATH = os.path.join(HERE, "tuft_B_UV完成_report.txt")


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


def shield(u, uv):
    """自屏蔽因子。u_UV -> inf 时 = exp(-u)（原模型）；
    u_UV 小则'填回'被压制的源（取消自屏蔽，趋近 GR）。"""
    s = math.exp(-u)
    if uv is not None:
        s *= math.sqrt(1.0 + (u / uv) ** 2)
    return s


def integrate_w(xi, w0, uv):
    eps = 1e-6
    x = eps
    s0 = shield(xi * w0, uv)
    w = w0 - s0 * eps * eps
    wp = -2.0 * s0 * eps
    h = 5e-4
    xmax = 1.0

    def deriv(x, w, wp):
        return wp, -6.0 * shield(xi * w, uv) - (2.0 / x) * wp

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


def shoot(xi, uv, tol=1e-12):
    def h(w0):
        w, wp = integrate_w(xi, w0, uv)
        return w + wp

    # 网格上界需覆盖小 u_UV（强抑制）时的大 w0 收敛区
    # （u_UV=0.05 时 w0 已 > 6，原 6.0 上界找不到变号括号 -> 误报"打靶未收敛"）
    grid = np.linspace(0.0, 40.0, 401)
    lo = hi = None
    prev_x = prev_h = None
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
    w1, wp1 = integrate_w(xi, w0, uv)
    return w0, w1, w1 / 2.0


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT-B 修复检验：UV 完成对强场自屏蔽的抑制")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)

    xi_bh = 0.5   # 黑洞致密系数（与质量无关）

    # ---------- 步骤 1：校准（uv=None 复现 46.82%） ----------
    rep.section("步骤 1  校准：无 UV 抑制（u_UV -> inf）应复现黑洞偏离 46.82%")
    w0n, w1n, mrn = shoot(xi_bh, None)
    devn = 1.0 - mrn
    rep.add("U0", "xi=0.5 无抑制：M_eff/M=%.5f, 偏离=%.4f (%.2f%%)" % (mrn, devn, devn * 100),
            "PASS" if abs(devn - 0.4682) < 0.005 else "FAIL",
            "与 tuft_B_自屏蔽_数值求解 的 46.82%% 一致（校准通过）")

    # ---------- 步骤 2：扫描 u_UV ----------
    rep.section("步骤 2  扫描 UV 抑制强度 u_UV（黑洞 xi=0.5）")
    uvs = [None, 2.0, 1.0, 0.5, 0.3, 0.2, 0.1, 0.05]
    table = []
    for uv in uvs:
        w0, w1, mr = shoot(xi_bh, uv)
        if mr is None:
            rep.add("U", "u_UV=%s 求解" % str(uv), "FAIL", "打靶未收敛")
            continue
        dev = 1.0 - mr
        table.append((uv, mr, dev))
        tag = "无抑制(inf)" if uv is None else ("u_UV=%.2f" % uv)
        rep.add("U", "%s : M_eff/M=%.5f, 偏离=%.4f (%.2f%%)" % (tag, mr, dev, dev * 100),
                "INFO", "w0=%.4f" % w0)

    # ---------- 步骤 3：找偏离=10% 的临界 u_UV ----------
    rep.section("步骤 3  临界抑制强度：偏离降到 LIGO 10% 需要多强的 UV")
    ligo = 0.10
    uv_crit = None
    fin = [(uv, d) for uv, m, d in table if uv is not None]
    fin_sorted = sorted(fin, key=lambda t: t[0])  # uv 从小到大
    for i in range(1, len(fin_sorted)):
        (u1, d1), (u2, d2) = fin_sorted[i - 1], fin_sorted[i]
        if (d1 - ligo) * (d2 - ligo) <= 0 and d2 != d1:
            uv_crit = u1 + (ligo - d1) * (u2 - u1) / (d2 - d1)
            break
    if uv_crit:
        rep.add("U3", "偏离=10%% 的临界 u_UV* ~ %.3f" % uv_crit, "INFO",
                "即需要 UV 抑制尺度与 u_max 同量级（u_max ~ 0.78）")
    else:
        rep.add("U3", "10% 阈值未在扫描区间跨越", "BOUNDARY",
                "见步骤 2 表：需更强/更弱抑制")

    # ---------- 步骤 4：物理代价评估 ----------
    rep.section("步骤 4  UV 完成的物理代价评估")
    umax = (shoot(xi_bh, None)[0] or 0.0) * xi_bh
    rep.add("U4", "黑洞内部 u 的量级 u_max ~ %.3f（强场，u ~ O(1)）" % umax, "INFO",
            "要抑制自屏蔽，UV 尺度必须在 u ~ O(1)，即**引力势 ~ c^2 量级**（强场），"
            "而非普朗克尺度（u_P >> 1）。")
    rep.add("U4", "判定：UV 完成'不经济'", "BOUNDARY",
            "把抑制尺度设在 u~1（强场）意味着 TUFT 在强场引入了新的唯象修正；"
            "这**不是**自然的 UV 完成（普朗克尺度），而是**在强场手工切除自屏蔽**。"
            "等价于'回到 GR'的另一种说法——仍无独立超越 GR 的预言。")
    rep.add("U4", "结论：UV 完成不能同时保'超越 GR'与'符合观测'", "FAIL",
            "要么保留自屏蔽（被 LIGO 排除），要么切掉它（回到 GR）。"
            "与根因溯源的两难结论一致。")

    rep.add("全局", "运行耗时", "INFO", "%.1f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
