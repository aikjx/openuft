# -*- coding: utf-8 -*-
"""74 号配套脚本 5/6 · 精细结构常数的 1-loop RG 跑动（纯标准库 RK4）。

用途：给原版 Eq-09-22「α(μ) = g'^2(μ)/(4π)」提供**对照基线**——
说明「跑动」需要三件东西：β 函数、边界条件、能标口径；原版只给了定义式。

口径声明（重要）：
  * 本脚本只跑**标准模型 1-loop**，不含任何 OpenUFT 新增内容；
  * 采用 a_i = α_i/(4π) 约定，β 系数自带符号、无外层负号；
  * 跨册引用时不得与库内能标一致性册的「α_G 全能标跨度 33.325 dex」混称——
    两者对象与口径都不同。

输出：74_rg_alpha_running_results.json / _out.txt
退出码：0 全过；1 内容层失配；2 仪器层失效。
"""
from __future__ import print_function

import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "74_rg_alpha_running_results.json")
OUT_TXT = os.path.join(HERE, "74_rg_alpha_running_out.txt")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RESULTS = []


def rec(sid, title, verdict, detail):
    RESULTS.append({"id": sid, "title": title, "verdict": verdict, "detail": detail})


# 1-loop SM β（a_i = α_i/(4π)，系数自带符号，无外层负号）
C = ((41.0 / 10.0, -19.0 / 6.0, -7.0),
     (-19.0 / 6.0, -19.0 / 6.0, -7.0),
     (-7.0, -7.0, -7.0))

MU_Z = 91.1876          # GeV
A1_MZ = 1.0 / 127.95    # 1-loop 惯例输入
A2_MZ = 1.0 / 59.0
A3_MZ = 1.0 / 37.2


def beta(a):
    return (a[0] * (C[0][0] * a[0] + C[0][1] * a[1] + C[0][2] * a[2]),
            a[1] * (C[1][0] * a[0] + C[1][1] * a[1] + C[1][2] * a[2]),
            a[2] * (C[2][0] * a[0] + C[2][1] * a[1] + C[2][2] * a[2]))


def rk4(a, t, dt):
    k1 = beta(a)
    a2 = tuple(a[i] + 0.5 * dt * k1[i] for i in range(3))
    k2 = beta(a2)
    a3 = tuple(a[i] + 0.5 * dt * k2[i] for i in range(3))
    k3 = beta(a3)
    a4 = tuple(a[i] + dt * k3[i] for i in range(3))
    k4 = beta(a4)
    return tuple(a[i] + dt / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(3))


def run(a0, mu0, mu1, n=4000):
    dt = (math.log(mu1) - math.log(mu0)) / n
    a = a0
    for _ in range(n):
        a = rk4(a, 0.0, dt)
    return a


# ---- 守卫 1：往返一致性（往上跑再跑回来应回到出发点） ----
a_up = run((A1_MZ, A2_MZ, A3_MZ), MU_Z, 1000.0)
a_back = run(a_up, 1000.0, MU_Z)
rel_back = abs(a_back[0] - A1_MZ) / A1_MZ
rec("G01", "守恒往返：从 M_Z 跑到 1 TeV 再跑回 M_Z，应回到出发点",
    "PASS" if rel_back < 1e-10 else "FAIL", "相对偏差 " + ("%.3E" % rel_back))

# ---- 守卫 2：α_em 的高能行为应为渐近自由（α 减小） ----
rec("G02", "方向守卫：α_em 随能标升高而减小（QED 渐近自由）",
    "PASS" if a_up[0] < A1_MZ else "FAIL",
    "α(M_Z)=%.10E → α(1 TeV)=%.10E" % (A1_MZ, a_up[0]))

# ---- 主体：各能标读数 ----
SCALES = [("1 GeV", 1.0), ("10 GeV", 10.0), ("M_Z", MU_Z), ("1 TeV", 1000.0),
          ("100 TeV", 1.0e5), ("1e6 GeV", 1.0e6)]
readings = []
for name, mu in SCALES:
    a = run((A1_MZ, A2_MZ, A3_MZ), MU_Z, mu)
    readings.append({"scale": name, "mu_GeV": mu,
                     "alpha_inv_em": 1.0 / a[0], "alpha_inv_s": 1.0 / a[2]})
    rec("R-" + name, "α_em 在 %s" % name, "INFO",
        "α_em^-1 = %.8f，α_s^-1 = %.8f" % (1.0 / a[0], 1.0 / a[2]))

span = (math.log10(readings[-1]["alpha_inv_em"]) - math.log10(readings[0]["alpha_inv_em"]))
rec("R-SPAN", "α_em^-1 在 1 GeV -- 1e6 GeV 的跨度", "INFO",
    "跨度 %.4f dex（对象为 α_em、口径为 1-loop SM；"
    "不得与库内能标册的 α_G 全能标跨度 33.325 dex 混称）" % span)

rec("R-NOTE", "Eq-09-22 的定位", "INFO",
    "原版 Eq-09-22 只给出 α(μ)=g'^2/(4π) 的定义式；跑动还需 β 函数、边界条件与能标口径。"
    "本脚本给出标准模型 1-loop 基线以示「跑动需要什么」，其中不含任何本体系的新增内容 ⇒ "
    "它不能被记作原版的验证。")

summary = {"total": len(RESULTS)}
for e in RESULTS:
    summary[e["verdict"]] = summary.get(e["verdict"], 0) + 1
payload = {"meta": {"script": "74_rg_alpha_running.py", "loop": "1-loop SM",
                    "convention": "a_i = alpha_i/(4pi)，beta 系数自带符号、无外层负号",
                    "caveat": "只给 SM 基线，不含 OpenUFT 新增内容"},
           "summary": summary, "readings": readings, "entries": RESULTS}
with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
lines = ["74 配套脚本 5/6 · 1-loop SM α 跑动（基线）",
         "条目 %d：%s" % (len(RESULTS),
                          " / ".join("%s %d" % (k, v) for k, v in sorted(summary.items()) if k != "total")),
         "-" * 70]
for e in RESULTS:
    lines.append("[%s] %s %s" % (e["verdict"], e["id"], e["title"]))
    lines.append("      " + e["detail"])
with io.open(OUT_TXT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
if not ("--quiet" in sys.argv):
    print("\n".join(lines))
if any(e["verdict"] == "FAIL" for e in RESULTS if e["id"].startswith("G")):
    sys.exit(2)
if any(e["verdict"] == "FAIL" for e in RESULTS):
    sys.exit(1)
sys.exit(0)
