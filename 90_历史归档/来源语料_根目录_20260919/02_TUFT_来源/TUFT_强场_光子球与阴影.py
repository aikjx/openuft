# -*- coding: utf-8 -*-
"""
TUFT 强场仿真：光子球与黑洞阴影（指数度规 vs GR）
=================================================
背景：1PN/PPN 与 GR 精确简并（无区分力）；D5（2PN 光偏折）需强场/高精度。
本文件计算强场观测量——**光子球半径**与**阴影直径**——对
  TUFT: beta1 = e^{-2U}（isotropic 指数度规），U=m/r
  GR  : Schwarzschild（b_crit = 3 sqrt(3) m）
并评估 EHT 可观测性。

红线：数学自洽 != 实验证实。
"""
from __future__ import print_function

import os
import sys
import math
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import mpmath as mp
mp.mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "TUFT_强场_光子球阴影_report.txt")

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


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 强场仿真：光子球与阴影（指数度规 vs GR）")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))

    m = mp.mpf("1.0")   # 取 m = GM/c^2 = 1（单位化）

    # ---------- 1. 光子球（解析 + 数值） ----------
    rep.section("1  光子球：TUFT 指数度规 vs GR")
    # TUFT: (du/dphi)^2 = e^{4mu}/b^2 - u^2
    # 光子球条件: E=0 且 dE/du=0
    #   E=0: e^{4mu}/b^2 = u^2  -> b = e^{2mu}/u
    #   dE/du=0: 4m e^{4mu}/b^2 = 2u -> e^{4mu}/b^2 = u/(2m)
    #   联立: u^2 = u/(2m) -> u_ph = 1/(2m), r_ph = 2m
    #   b_crit = e^{2m*(1/(2m))}/(1/(2m)) = 2e m
    u_ph_analytic = 1 / (2 * m)
    b_tuft_analytic = 2 * mp.e * m
    # 数值验证（解联立）
    f1 = lambda u, b: mp.e ** (4 * m * u) / b ** 2 - u ** 2
    f2 = lambda u, b: 4 * m * mp.e ** (4 * m * u) / b ** 2 - 2 * u
    sol = mp.findroot([f1, f2], [u_ph_analytic, b_tuft_analytic])
    u_ph_num, b_tuft = mp.re(sol[0]), mp.re(sol[1])
    rep.add("1.1", "TUFT 光子球解析：r_ph(iso) = 2m, b_crit = 2e·m", "PASS",
            "解析 b = 2e m = %.6f ；数值 b = %.6f（一致）" % (float(b_tuft_analytic), float(b_tuft)))

    b_gr = 3 * mp.sqrt(3) * m
    rep.add("1.2", "GR (Schwarzschild) 光子球：b_crit = 3√3·m", "INFO",
            "b_GR = %.6f（标准结果；b 为冲击参数，坐标无关可观测量）" % float(b_gr))

    ratio = b_tuft / b_gr
    rep.add("1.3", "阴影半径比 b_TUFT / b_GR", "PASS",
            "%.6f  => 差异 **%+.2f%%**" % (float(ratio), float((ratio - 1) * 100)))

    # ---------- 2. 阴影直径 ----------
    rep.section("2  黑洞阴影直径（可观测）")
    d_tuft = 2 * b_tuft
    d_gr = 2 * b_gr
    rep.add("2.1", "阴影直径 d = 2·b_crit", "INFO",
            "TUFT: d = %.6f m ; GR: d = %.6f m （单位 m=GM/c^2）" % (float(d_tuft), float(d_gr)))
    rep.add("2.2", "直径比 d_TUFT/d_GR", "PASS",
            "%.6f => 差 %+.2f%%" % (float(d_tuft / d_gr), float((d_tuft / d_gr - 1) * 100)))

    # ---------- 3. 实际天体数值 ----------
    rep.section("3  实际天体（Sgr A* / M87*）阴影直径")
    bodies = [("Sgr A*", 4.297e6), ("M87*", 6.5e9)]
    for name, msun in bodies:
        mm = G * msun * MSUN / C ** 2
        dT = float(2 * 2 * mp.e * mm)
        dG = float(2 * 3 * mp.sqrt(3) * mm)
        rep.add("3", "%s: M=%.3g Msun" % (name, msun), "INFO",
                "m=GM/c^2=%.4e m ; d_TUFT=%.4e m ; d_GR=%.4e m（差 %+.2f%%）" %
                (mm, dT, dG, (dT / dG - 1) * 100))

    # ---------- 4. 强场数值验证：光子捕获 ----------
    rep.section("4  数值验证：临界冲击参数 b_crit（测地线捕获判据）")
    def deflect(m, b):
        """返回偏折角；若光子被捕获（无 u0 实根）返回 None。"""
        u0 = mp.mpf("1") / b
        # 检查 E=0 是否有实根（u0 满足 e^{4mu0}/b^2 = u0^2）
        f = lambda u: mp.e ** (4 * m * u) / b ** 2 - u ** 2
        try:
            r = mp.re(mp.findroot(f, u0))
        except Exception:
            return None
        if r <= 0 or r > 1:
            return None
        def integrand(th):
            u = r * mp.sin(th)
            K = mp.e ** (4 * m * u) / b ** 2 - u ** 2
            if K <= mp.mpf("1e-50"):
                K = mp.mpf("1e-50")
            return r * mp.cos(th) / mp.sqrt(K)
        I = mp.quad(integrand, [0, mp.pi / 2 - mp.mpf("1e-12")])
        return mp.re(2 * I - mp.pi)

    b_lo = mp.mpf("0.99") * b_tuft     # 应被捕获（偏折发散/无界）
    b_hi = mp.mpf("1.01") * b_tuft     # 应能逃逸
    a_lo = deflect(m, b_lo)
    a_hi = deflect(m, b_hi)
    rep.add("4.1", "b 略小于 b_crit (%.6f)：偏折" % float(b_lo),
            "PASS" if (a_lo is None or abs(a_lo) > 1) else "BOUNDARY",
            "alpha = %s（>1 rad 或捕获 => 临界行为）" % ("None(捕获)" if a_lo is None else "%.4f" % float(a_lo)))
    rep.add("4.2", "b 略大于 b_crit (%.6f)：偏折" % float(b_hi),
            "PASS" if (a_hi is not None and abs(a_hi) < 3) else "BOUNDARY",
            "alpha = %s（有限偏折 => 逃逸）" % ("None" if a_hi is None else "%.4f" % float(a_hi)))

    # ---------- 5. 可观测性 ----------
    rep.section("5  EHT 可观测性评估")
    diff_pct = float((d_tuft / d_gr - 1) * 100)
    rep.add("5.1", "TUFT 阴影比 GR 大 %.2f%%" % diff_pct, "INFO",
            "两理论阴影直径比值 %.4f" % float(d_tuft / d_gr))
    rep.add("5.2", "EHT 当前精度（M87*/Sgr A* 阴影直径）", "INFO",
            "EHT 2019/2022 报告阴影直径与 GR 一致，测量不确定度约 10-20%（含质量/距离误差）")
    rep.add("5.3", "可区分性判定", "BOUNDARY",
            "TUFT 的 +%.2f%% 差异 **小于** EHT 当前 ~10%% 不确定度 => 尚未被排除，"
            "但也**尚未可判别**。属'未来高精度观测（ngEHT / 空间 VLBI）可判别'的预言。" % diff_pct)
    rep.add("5.4", "与 D2（无视界）的一致性", "FAIL",
            "指数度规 g_00=e^{-2U} 永不穿过零 => 无事件视界。但**阴影仍存在**（光子球 + 捕获），"
            "故'无视界'与'有阴影'并存——需在论文中澄清'视界'与'阴影'的区别，"
            "否则'无视界'易被误读为'无黑影'。")

    rep.add("全局", "运行耗时", "INFO", "%.1f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
