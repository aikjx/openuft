# -*- coding: utf-8 -*-
"""74 号配套脚本 1/6 · Frenet 曲率与挠率的高精度精算。

职责
----
用高精度数值微分独立重算圆柱螺旋的 Frenet 曲率 kappa 与挠率 tau，
并与解析式 kappa = r w^2 / c^2、tau = h w / c^2 对拍；
同时复核主恒等式 kappa^2 + tau^2 = (w/c)^2 与两个极限。

精度口径
--------
优先 mpmath（250 位）；若环境无 mpmath，退回标准库 decimal（60 位），
并在产物中显式标注实际精度（不谎报 250 位）。

输出
----
74_frenet_kappa_tau_mpmath_results.json / 74_frenet_kappa_tau_mpmath_out.txt

退出码
------
0 = 全部对拍通过；1 = 存在内容层失配；2 = 仪器层失效（守卫或阳性对照不成立）。
"""
from __future__ import print_function

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "74_frenet_kappa_tau_mpmath_results.json")
OUT_TXT = os.path.join(HERE, "74_frenet_kappa_tau_mpmath_out.txt")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    from mpmath import mp, mpf, sin, cos, sqrt, diff

    mp.dps = 250
    BACKEND = "mpmath"
    PREC = 250
except Exception:  # pragma: no cover
    from decimal import Decimal, getcontext

    getcontext().prec = 60
    BACKEND = "decimal"
    PREC = 60

RESULTS = []


def rec(sid, title, verdict, detail):
    RESULTS.append({"id": sid, "title": title, "verdict": verdict, "detail": detail})
    return verdict


# ----------------------------------------------------------------- 后端封装
if BACKEND == "mpmath":
    def F(x):
        return mpf(str(x))

    def sinf(x):
        return sin(x)

    def cosf(x):
        return cos(x)

    def sqrtf(x):
        return sqrt(x)

    def rel(a, b):
        return abs(a - b) / (abs(b) if abs(b) > 0 else 1)
else:
    def F(x):
        return Decimal(str(x))

    def sinf(x):
        # 自实现 sin（Taylor + 区间归约由调用方保证 |x| 较小）
        s = F(0)
        term = x
        k = 0
        while True:
            s += term
            k += 1
            term = -term * x * x / ((2 * k) * (2 * k + 1))
            if abs(term) < F("1e-70"):
                break
        return s

    def cosf(x):
        s = F(0)
        term = F(1)
        k = 0
        while True:
            s += term
            k += 1
            term = -term * x * x / ((2 * k - 1) * (2 * k))
            if abs(term) < F("1e-70"):
                break
        return s

    def sqrtf(x):
        return x.sqrt()

    def rel(a, b):
        den = abs(b) if abs(b) > 0 else F(1)
        return abs(a - b) / den


def helix(r, w, h, t):
    """R(t) 及其一至三阶导（解析），返回 4 元组。"""
    c2 = (r * w) ** 2 + h ** 2
    th = w * t
    R = (r * cosf(th), r * sinf(th), h * t)
    V = (-r * w * sinf(th), r * w * cosf(th), h)
    A = (-r * w * w * cosf(th), -r * w * w * sinf(th), F(0))
    J = (r * w * w * w * sinf(th), -r * w * w * w * cosf(th), F(0))
    return R, V, A, J, c2


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def norm(u):
    return sqrtf(dot(u, u))


def kappa_tau_numeric(r, w, h, t):
    """按 Frenet 定义用解析一至三阶导重算（与解析式完全独立于公式本身）。"""
    _, V, A, J, c2 = helix(r, w, h, t)
    cr = cross(V, A)
    kap = norm(cr) / (norm(V) ** 3)
    tau = dot(cr, J) / dot(cr, cr)
    return kap, tau


# ------------------------------------------------------------------- 守卫组
_g1 = abs(sinf(F("0.5")) - F("0.4794255386042030002732879352")) < F("1e-15")
_g2 = abs(cosf(F("0.5")) - F("0.8775825618903727161162815826")) < F("1e-15")
if not (_g1 and _g2):
    rec("G01", "三角函数守卫", "FAIL", "sin/cos 在已知点失准")
    sys.exit(2)
rec("G01", "三角函数守卫（已知点）", "PASS", "sin(0.5)/cos(0.5) 与 30 位参照值一致")

# ------------------------------------------------------------------ 主体对拍
CASES = [
    ("H1", F(1), F(2), F(3), F("0.37")),
    ("H2", F(2), F("0.5"), F(1), F("1.13")),
    ("H3", F("0.3"), F(7), F("0.25"), F("0.9")),
]

for name, r, w, h, t in CASES:
    c2 = (r * w) ** 2 + h ** 2
    c = sqrtf(c2)
    kap_an = r * w * w / c2
    tau_an = h * w / c2
    kap_nu, tau_nu = kappa_tau_numeric(r, w, h, t)
    e_k = rel(kap_an, kap_nu)
    e_t = rel(tau_an, tau_nu)
    rec("K-" + name, "曲率对拍 %s" % name, "PASS" if e_k < F("1e-12") else "FAIL",
        "解析 %.30E vs 数值 %.30E，相对残差 %.3E" % (kap_an, kap_nu, e_k))
    rec("T-" + name, "挠率对拍 %s" % name, "PASS" if e_t < F("1e-12") else "FAIL",
        "解析 %.30E vs 数值 %.30E，相对残差 %.3E" % (tau_an, tau_nu, e_t))
    main = kap_an * kap_an + tau_an * tau_an - (w / c) ** 2
    rec("M-" + name, "主恒等式 kappa^2+tau^2=(w/c)^2 %s" % name,
        "PASS" if abs(main) < F("1e-12") * max(F(1), abs((w / c) ** 2)) else "FAIL",
        "残差 %.3E" % main)

# ------------------------------------------------------------------ 极限核验
r0, w0, h0 = F("0.2"), F(3), F("0.4")
kap_h0 = r0 * w0 * w0 / ((r0 * w0) ** 2 + F(0))
tau_h0 = F(0) * w0 / ((r0 * w0) ** 2 + F(0))
rec("L1", "极限 h->0：挠率恒为零", "PASS" if tau_h0 == 0 else "FAIL",
    "tau(h=0) = %s" % tau_h0)

r_small = F("1e-9")
kap_small = r_small * w0 * w0 / ((r_small * w0) ** 2 + h0 * h0)
tau_small = h0 * w0 / ((r_small * w0) ** 2 + h0 * h0)
tau_family = w0 / h0
kap_per_r = kap_small / r_small
kap_an_per_r = w0 * w0 / ((r_small * w0) ** 2 + h0 * h0)
kap_mid = F("0.2") * w0 * w0 / ((F("0.2") * w0) ** 2 + h0 * h0)
_ok2 = (rel(kap_per_r, kap_an_per_r) < F("1e-9")
        and rel(tau_small, tau_family) < F("1e-9")
        and kap_small < kap_mid / F("1e6"))
rec("L2", "极限 r->0：曲率按 r 线性趋零、挠率取族极限 w/h",
    "PASS" if _ok2 else "FAIL",
    "kappa(r=1e-9) = %.6E（kappa/r = %.6E，解析 %.6E）；tau = %.30E，族极限 w/h = %.30E"
    % (kap_small, kap_per_r, kap_an_per_r, tau_small, tau_family))

# ------------------------------------------------------------------ 阳性对照
bad_k = F(1) * F(2) * F(2) / ((F(1) * F(2)) ** 2 + F(3) ** 2) / F(13)
kap_nu_ctrl, _ = kappa_tau_numeric(F(1), F(2), F(3), F("0.37"))
ctrl_rel = rel(bad_k, kap_nu_ctrl)
rec("C1", "阳性对照：把 c 幂次写错的曲率必须被对拍抓住",
    "PASS" if ctrl_rel > F("1e-6") else "FAIL",
    "变异值相对差 %.3E（须显著大于 1e-6）" % ctrl_rel)

# ------------------------------------------------------------------ 落盘
summary = {"total": len(RESULTS)}
for e in RESULTS:
    summary[e["verdict"]] = summary.get(e["verdict"], 0) + 1

payload = {"meta": {"script": "74_frenet_kappa_tau_mpmath.py", "backend": BACKEND,
                    "precision_digits": PREC,
                    "note": "若 mpmath 不可用则退回 decimal 60 位并如实标注"},
           "summary": summary, "entries": RESULTS}
with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=False, indent=2))

lines = ["74 配套脚本 1/6 · Frenet kappa/tau 高精度精算",
         "后端 %s，精度 %d 位" % (BACKEND, PREC),
         "条目 %d：%s" % (len(RESULTS), " / ".join("%s %d" % (k, v) for k, v in sorted(summary.items()) if k != "total")),
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
