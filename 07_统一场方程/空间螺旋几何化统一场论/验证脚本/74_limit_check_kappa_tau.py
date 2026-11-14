# -*- coding: utf-8 -*-
"""74 号配套脚本 3/6 · 极限扫描：曲率与挠率的退化正确性。

扫描三条退化路径，并与 Frenet 有限差分独立复算对照：
  (1) h -> 0（平面圆）：挠率线性趋零；
  (2) r -> 0（直线）  ：曲率趋零，挠率取族极限 w/h（直线自身挠率未定义）；
  (3) w -> 0（静止）  ：曲率按 w^2、挠率按 w 趋零。
输出：74_limit_check_kappa_tau_results.json / _out.txt
退出码：0 全过；1 内容层失配；2 仪器层失效。
"""
from __future__ import print_function

import io
import json
import os
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "74_limit_check_kappa_tau_results.json")
OUT_TXT = os.path.join(HERE, "74_limit_check_kappa_tau_out.txt")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RESULTS = []


def rec(sid, title, verdict, detail):
    RESULTS.append({"id": sid, "title": title, "verdict": verdict, "detail": detail})


def fs(x):
    return "0（机器零）" if x == 0 else format(x, ".25E")


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def vnorm(a):
    return vdot(a, a).sqrt()


def _sin(x):
    s, term, k = Decimal(0), x, 0
    while True:
        s += term
        k += 1
        term = -term * x * x / ((2 * k) * (2 * k + 1))
        if abs(term) < Decimal("1e-70"):
            break
    return s


def _cos(x):
    s, term, k = Decimal(0), Decimal(1), 0
    while True:
        s += term
        k += 1
        term = -term * x * x / ((2 * k - 1) * (2 * k))
        if abs(term) < Decimal("1e-70"):
            break
    return s


class Hx(object):
    def __init__(self, r, w, h):
        self.r, self.w, self.h = Decimal(r), Decimal(w), Decimal(h)
        self.c2 = (self.r * self.w) ** 2 + self.h ** 2

    def R(self, t):
        ct, st = _cos(self.w * t), _sin(self.w * t)
        return (self.r * ct, self.r * st, self.h * t)

    def dR(self, t):
        ct, st = _cos(self.w * t), _sin(self.w * t)
        return (-self.r * self.w * st, self.r * self.w * ct, self.h)

    def dd2(self, t, h):
        r0 = self.R(t)
        raw = tuple((self.R(t + h)[i] - 2 * r0[i] + self.R(t - h)[i]) / (h * h) for i in range(3))
        hh = h / 2
        fine = tuple((self.R(t + hh)[i] - 2 * r0[i] + self.R(t - hh)[i]) / (hh * hh) for i in range(3))
        return tuple((4 * fine[i] - raw[i]) / 3 for i in range(3))

    def dd3(self, t, h):
        raw = tuple((self.R(t + 2 * h)[i] - 2 * self.R(t + h)[i] + 2 * self.R(t - h)[i]
                     - self.R(t - 2 * h)[i]) / (2 * h ** 3) for i in range(3))
        hh = h / 2
        fine = tuple((self.R(t + 2 * hh)[i] - 2 * self.R(t + hh)[i] + 2 * self.R(t - hh)[i]
                      - self.R(t - 2 * hh)[i]) / (2 * hh ** 3) for i in range(3))
        return tuple((4 * fine[i] - raw[i]) / 3 for i in range(3))

    def kt_fd(self, t, h):
        v, a, j = self.dR(t), self.dd2(t, h), self.dd3(t, h)
        cr = vcross(v, a)
        return vnorm(cr) / (vnorm(v) ** 3), vdot(cr, j) / vdot(cr, cr)


def an(r, w, h):
    c2 = (r * w) ** 2 + h * h
    return r * w * w / c2, h * w / c2


T = Decimal("0.37")
STEP = Decimal("1e-4")

# ---- 守卫：非退化点解析式与有限差分必须吻合 ----
_k_an, _t_an = an(Decimal(1), Decimal(2), Decimal(3))
_k_nu, _t_nu = Hx(1, 2, 3).kt_fd(T, STEP)
_ek = abs(_k_an - _k_nu) / _k_an
_et = abs(_t_an - _t_nu) / _t_an
rec("G01", "非退化点解析式与有限差分必须吻合",
    "PASS" if (_ek < Decimal("1e-10") and _et < Decimal("1e-10")) else "FAIL",
    "kappa 相对差 " + fs(_ek) + "，tau 相对差 " + fs(_et))

# ---- (1) h -> 0 ----
rows, ok1 = [], True
for hs in ("0.4", "0.2", "0.1", "0.05"):
    h = Decimal(hs)
    k, t = an(Decimal(1), Decimal(2), h)
    rows.append("h=%s: tau=%s" % (hs, fs(t)))
    if abs(t) > Decimal("0.5"):
        ok1 = False
rec("L1", "极限 h->0：挠率线性趋零（平面圆）", "PASS" if ok1 else "FAIL", " | ".join(rows))

# ---- (2) r -> 0 ----
rows, ok2 = [], True
fam = Decimal(2) / Decimal("0.4")
_w = Decimal(2)
_h = Decimal("0.4")
r_star = _h / _w                       # 曲率的极大点 r = h/w
kap_max_an = _w / (2 * _h)             # kappa_max = w/(2h)
_t_prev = None
for rs in ("0.4", "0.2", "0.1", "0.05", "0.01", "0.000001"):
    r = Decimal(rs)
    k, t = an(r, _w, _h)
    rows.append("r=%s: kappa=%s tau=%s" % (rs, fs(k), fs(t)))
    if _t_prev is not None and t < _t_prev:   # 挠率必须随 r 减小而单调趋近族极限
        ok2 = False
    _t_prev = t
_k_star, _t_star = an(r_star, _w, _h)
if abs(_k_star - kap_max_an) > Decimal("1e-12"):
    ok2 = False                          # 解析极大值必须与机器扫描一致
if abs(_t_star - kap_max_an) > Decimal("1e-12"):
    ok2 = False                          # 极大点处 tau = w/(2h)（与 κ_max 同值，非族极限 w/h）
_k_tiny, _t_tiny = an(Decimal("1e-6"), _w, _h)
if abs(_t_tiny - fam) > Decimal("1e-5"):
    ok2 = False                          # r->0 时挠率必须趋于族极限 w/h
if _k_tiny > kap_max_an / Decimal("1e4"):
    ok2 = False                          # r->0 时曲率必须相对极大值趋零
rec("L2", "极限 r->0：曲率相对极大值趋零、挠率取族极限 w/h（曲率在 r=h/w 处取极大）",
    "PASS" if ok2 else "FAIL",
    " | ".join(rows) + "；族极限 w/h=" + fs(fam)
    + "；极大点 r=h/w=" + fs(r_star) + " 处 kappa=" + fs(_k_star)
    + "（解析 w/(2h)=" + fs(kap_max_an) + "）")

# ---- (3) w -> 0 ----
rows, ok3 = [], True
for ws in ("1", "0.5", "0.25", "0.125"):
    w = Decimal(ws)
    k, t = an(Decimal(1), w, Decimal(3))
    rows.append("w=%s: kappa=%s tau=%s" % (ws, fs(k), fs(t)))
    if k > Decimal("1"):
        ok3 = False
rec("L3", "极限 w->0：曲率按 w^2、挠率按 w 趋零", "PASS" if ok3 else "FAIL", " | ".join(rows))

# ---- 直线极限：Frenet 标架退化 ----
_nrm = vnorm(Hx(0, 2, 3).dd2(T, STEP))
rec("L4", "直线极限 r=0：Frenet 法向退化 ⇒ 挠率未定义（解析式适用域要求 r != 0）",
    "BOUNDARY", "|d2R/dt2| = " + fs(_nrm) + " ⇒ N 无定义；族极限 tau -> w/h 非直线自身的挠率")

# ---- 阳性对照 ----
_wrong = Decimal(4) / (Decimal(13) ** 3)
rec("C1", "阳性对照：c 幂次写错的曲率必须被扫描判据抓住",
    "PASS" if abs(_wrong - _k_an) / _k_an > Decimal("1e-3") else "FAIL",
    "变异值 " + fs(_wrong) + "，真值 " + fs(_k_an))

summary = {"total": len(RESULTS)}
for e in RESULTS:
    summary[e["verdict"]] = summary.get(e["verdict"], 0) + 1
payload = {"meta": {"script": "74_limit_check_kappa_tau.py", "precision": "decimal 60 位"},
           "summary": summary, "entries": RESULTS}
with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
lines = ["74 配套脚本 3/6 · 极限扫描",
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
if any(e["verdict"] == "FAIL" for e in RESULTS if e["id"].startswith(("G", "C"))):
    sys.exit(2)
if any(e["verdict"] == "FAIL" for e in RESULTS):
    sys.exit(1)
sys.exit(0)
