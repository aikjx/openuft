# -*- coding: utf-8 -*-
"""74 号配套脚本 6/6 · 螺旋参数族的可证伪性（chi^2）判定。

问题：原版的 23 条方程若能给出一个「随螺旋参数 (r, omega, h) 变化」的观测量预测，
则该族可以被数据否证；否则它对该可观测量零信息量。

机器判定：
  * 对电子反常磁矩 a_e（原版体系未给出任何把螺旋参数接入 a_e 的公式）
    => 模型预测与参数无关 => chi^2(lambda) 恒为常数 => dchi^2/dlambda = 0
    => 判定「零判别力 / 不可证伪」。
  * 阳性对照：一个预测确实依赖参数的玩具模型 => chi^2 随参数变化、最优点可定位
    => 证明本脚本的 chi^2 机制本身有效（否则上面的「平坦」不可信）。

输出：74_chi2_unified_fit_results.json / _out.txt
退出码：0 机制自检通过；1 内容层判定为「无判别力」（本体系的实际结论）；2 仪器层失效。
"""
from __future__ import print_function

import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "74_chi2_unified_fit_results.json")
OUT_TXT = os.path.join(HERE, "74_chi2_unified_fit_out.txt")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RESULTS = []


def rec(sid, title, verdict, detail):
    RESULTS.append({"id": sid, "title": title, "verdict": verdict, "detail": detail})


# 可观测量：电子反常磁矩 a_e（实验值 CODATA/PDG 口径）
A_E_EXP = 1159652181.8e-11
A_E_SIGMA = 1.1e-11


def chi2(pred, exp, sig):
    return ((pred - exp) / sig) ** 2


# ---- 模型 M1：原版体系（螺旋参数不进入预测） ----
def model_helix(lam):
    """原版 23 条方程未提供任何把螺旋参数接入 a_e 的公式 ⇒ 预测与 lam 无关。"""
    return A_E_EXP + 0.0 * lam


# ---- 模型 M2：阳性对照（预测确实依赖参数） ----
def model_toy(lam):
    return A_E_EXP + 3.0e-11 * lam


LAMS = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]

rows_m1, chi_m1 = [], []
for lam in LAMS:
    c = chi2(model_helix(lam), A_E_EXP, A_E_SIGMA)
    chi_m1.append(c)
    rows_m1.append("lam=%.2f: chi2=%.6f" % (lam, c))
spread_m1 = max(chi_m1) - min(chi_m1)

rows_m2, chi_m2 = [], []
for lam in LAMS:
    c = chi2(model_toy(lam), A_E_EXP, A_E_SIGMA)
    chi_m2.append(c)
    rows_m2.append("lam=%.2f: chi2=%.6f" % (lam, c))
best = min(zip(chi_m2, LAMS))
spread_m2 = max(chi_m2) - min(chi_m2)

rec("M1", "模型 M1（原版体系）：chi^2 是否随螺旋参数变化", "FAIL",
    " | ".join(rows_m1) + "；跨度 = %.6f" % spread_m1
    + " ⇒ 预测与参数无关 ⇒ 零判别力、不可证伪")
rec("M2", "阳性对照 M2（玩具模型）：chi^2 必须随参数变化", "PASS" if spread_m2 > 1.0 else "FAIL",
    " | ".join(rows_m2) + "；跨度 = %.6f，最优点 lam=%.2f，chi2_min=%.6f"
    % (spread_m2, best[1], best[0]))
rec("M3", "结论", "FAIL",
    "螺旋参数族 (r, omega, h)（在 |v|=c 约束下 2 个自由度）对标准可观测量提供 0 bit；"
    "似然比处处为 1 ⇒ 既不能被数据支持，也不能被数据否证。"
    "这与卷内 S07（旋度扰动只给量纲门槛、不给定量预言）一致。")

summary = {"total": len(RESULTS)}
for e in RESULTS:
    summary[e["verdict"]] = summary.get(e["verdict"], 0) + 1
payload = {"meta": {"script": "74_chi2_unified_fit.py",
                    "observable": "a_e = 1159652181.8e-11 +/- 1.1e-11",
                    "role": "可证伪性判定（零判别力）"},
           "summary": summary,
           "chi2_helix": chi_m1, "chi2_toy": chi_m2,
           "spread_helix": spread_m1, "spread_toy": spread_m2,
           "entries": RESULTS}
with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
lines = ["74 配套脚本 6/6 · 螺旋参数族的可证伪性判定",
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
if any(e["id"] == "M2" and e["verdict"] == "FAIL" for e in RESULTS):
    sys.exit(2)
if any(e["verdict"] == "FAIL" for e in RESULTS):
    sys.exit(1)
sys.exit(0)
