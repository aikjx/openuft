# -*- coding: utf-8 -*-
"""74 号配套脚本 2/6 · 协变导数展开的独立核验。

复核卷内三条判决：
  (1) Dc/Dt 在 Frenet 标架下的三个分量（T 应为机器零，N = c^2 kappa，B 应为机器零）；
  (2) 原版两版 Dc/Dt 展开式的残差（预期恰为 |w tau| 与 |tau c^2|）；
  (3) 正确的 Frenet--Serret 输运三角表（挠率只出现在 dN/dt 与 dB/dt）。

数值方法：中心差分 + Richardson 四阶外推；截断阶由守卫 G05 自检。
输出：74_unified_force_covariant_deriv_results.json / _out.txt（与脚本同目录）
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
OUT_JSON = os.path.join(HERE, "74_unified_force_covariant_deriv_results.json")
OUT_TXT = os.path.join(HERE, "74_unified_force_covariant_deriv_out.txt")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RESULTS = []


def rec(sid, title, verdict, detail):
    RESULTS.append({"id": sid, "title": title, "verdict": verdict, "detail": detail})


def fs(x):
    return "0（机器零）" if x == 0 else format(x, ".25E")


def vsub(a, b):
    return tuple(a[i] - b[i] for i in range(3))


def vadd(a, b):
    return tuple(a[i] + b[i] for i in range(3))


def vscale(a, s):
    return tuple(a[i] * s for i in range(3))


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def vnorm(a):
    return vdot(a, a).sqrt()


def _sin(x):
    s = Decimal(0)
    term = x
    k = 0
    while True:
        s += term
        k += 1
        term = -term * x * x / ((2 * k) * (2 * k + 1))
        if abs(term) < Decimal("1e-70"):
            break
    return s


def _cos(x):
    s = Decimal(0)
    term = Decimal(1)
    k = 0
    while True:
        s += term
        k += 1
        term = -term * x * x / ((2 * k - 1) * (2 * k))
        if abs(term) < Decimal("1e-70"):
            break
    return s


class Helix(object):
    def __init__(self, r, w, h):
        self.r = Decimal(r)
        self.w = Decimal(w)
        self.h = Decimal(h)
        self.c2 = (self.r * self.w) ** 2 + self.h ** 2
        self.c = self.c2.sqrt()

    def R(self, t):
        t = Decimal(t)
        ct, st = _cos(self.w * t), _sin(self.w * t)
        return (self.r * ct, self.r * st, self.h * t)

    def dR(self, t):
        t = Decimal(t)
        ct, st = _cos(self.w * t), _sin(self.w * t)
        return (-self.r * self.w * st, self.r * self.w * ct, self.h)

    def ddR(self, t):
        t = Decimal(t)
        ct, st = _cos(self.w * t), _sin(self.w * t)
        return (-self.r * self.w ** 2 * ct, -self.r * self.w ** 2 * st, Decimal(0))

    def frame(self, t):
        T = vscale(self.dR(t), Decimal(1) / self.c)
        acc = self.ddR(t)
        n = vnorm(acc)
        N = vscale(acc, Decimal(1) / n) if n > 0 else (Decimal(0),) * 3
        return T, N, vcross(T, N)

    def fd2(self, t, h):
        r0 = self.R(t)
        raw = tuple((self.R(t + h)[i] - 2 * r0[i] + self.R(t - h)[i]) / (h * h) for i in range(3))
        hh = h / 2
        fine = tuple((self.R(t + hh)[i] - 2 * r0[i] + self.R(t - hh)[i]) / (hh * hh) for i in range(3))
        return tuple((4 * fine[i] - raw[i]) / 3 for i in range(3))

    def frame_fd(self, t, h):
        def nth(hh):
            return self.frame(t + hh)[1]

        def bth(hh):
            return self.frame(t + hh)[2]

        dN = tuple((4 * ((nth(h / 2)[i] - nth(-h / 2)[i]) / h) - (nth(h)[i] - nth(-h)[i]) / (2 * h)) / 3
                   for i in range(3))
        dB = tuple((4 * ((bth(h / 2)[i] - bth(-h / 2)[i]) / h) - (bth(h)[i] - bth(-h)[i]) / (2 * h)) / 3
                   for i in range(3))
        return dN, dB


H = Helix(1, 2, 3)
TS = Decimal("0.37")
HS = Decimal("1e-4")
kappa = H.r * H.w ** 2 / H.c2
tau = H.h * H.w / H.c2

_e1 = abs(H.fd2(TS, HS / 2)[1] - H.fd2(TS, HS)[1])
_e2 = abs(H.fd2(TS, HS)[1] - H.fd2(TS, HS * 2)[1])
_ratio = _e1 / _e2
rec("G05", "有限差分截断阶（四阶 Richardson）", "PASS" if Decimal("0.02") < _ratio < Decimal("0.12") else "FAIL",
    "e(h/2)/e(h) = " + fs(_ratio) + "（理论 1/16）")

T, N, B = H.frame(TS)
dc_dt = H.fd2(TS, HS)
cT, cN, cB = vdot(dc_dt, T), vdot(dc_dt, N), vdot(dc_dt, B)
scale = max(abs(cN), Decimal("1e-12"))

rec("K11", "Dc/Dt 的主法向分量 = c^2 kappa", "PASS" if abs(cN - H.c2 * kappa) < Decimal("1e-8") * scale else "FAIL",
    "分量 " + fs(cN) + "，预期 " + fs(H.c2 * kappa))
rec("K12", "Dc/Dt 的切向分量恒为零", "PASS" if abs(cT) < Decimal("1e-10") * scale else "FAIL", "分量 " + fs(cT))
rec("K13", "Dc/Dt 的副法向分量恒为零 ⇒ 挠率项无来源",
    "PASS" if abs(cB) < Decimal("1e-10") * scale else "FAIL", "分量 " + fs(cB))

draft_a = vadd(vscale(N, H.w ** 2 * H.r), vscale(B, H.w * tau))
draft_b = vadd(vscale(N, kappa * H.c2), vscale(B, tau * H.c2))
res_a = vnorm(vsub(dc_dt, draft_a))
res_b = vnorm(vsub(dc_dt, draft_b))
rec("K14", "原版版一 Dc/Dt = w^2 r N + w tau B 的残差", "FAIL" if res_a > Decimal("1e-12") else "PASS",
    "残差 " + fs(res_a) + "（理论预期 |w tau| = " + fs(H.w * tau) + "）")
rec("K15", "原版版二 Dc/Dt = kappa c^2 N + tau c^2 B 的残差", "FAIL" if res_b > Decimal("1e-12") else "PASS",
    "残差 " + fs(res_b) + "（理论预期 |tau c^2| = " + fs(tau * H.c2) + "）")
rec("K16", "原版两版互不相等", "FAIL" if vnorm(vsub(draft_a, draft_b)) > Decimal("1e-12") else "PASS",
    "互差 " + fs(vnorm(vsub(draft_a, draft_b))))

dN_dt, dB_dt = H.frame_fd(TS, HS)
ck = H.c * kappa
ct = H.c * tau
rows = []
tri_ok = True
for name, vec, exp in (("dT/dt", vscale(dc_dt, Decimal(1) / H.c), (Decimal(0), ck, Decimal(0))),
                        ("dN/dt", dN_dt, (-ck, Decimal(0), ct)),
                        ("dB/dt", dB_dt, (Decimal(0), -ct, Decimal(0)))):
    got = (vdot(vec, T), vdot(vec, N), vdot(vec, B))
    err = max(abs(got[i] - exp[i]) for i in range(3)) / scale
    if err > Decimal("1e-9"):
        tri_ok = False
    rows.append("%s: T=%s N=%s B=%s（预期 T=%s N=%s B=%s）归一残差 %s"
                % (name, fs(got[0]), fs(got[1]), fs(got[2]),
                   fs(exp[0]), fs(exp[1]), fs(exp[2]), fs(err)))
rec("K17", "Frenet 输运三角表：挠率只出现在 dN/dt 与 dB/dt",
    "PASS" if tri_ok else "FAIL", " | ".join(rows))

ctrl = vadd(vscale(N, H.w ** 2 * H.r), vscale(B, H.w * tau))
ctrl_err = vnorm(vsub(dc_dt, ctrl))
rec("C1", "阳性对照：挠率项被替换为曲率项后残差必须显著",
    "PASS" if ctrl_err > Decimal("1e-6") else "FAIL", "对照残差 " + fs(ctrl_err))

summary = {"total": len(RESULTS)}
for e in RESULTS:
    summary[e["verdict"]] = summary.get(e["verdict"], 0) + 1
payload = {"meta": {"script": "74_unified_force_covariant_deriv.py",
                    "precision": "decimal 60 位 + Richardson 四阶",
                    "role": "主仪器 K11--K17 的独立复核"},
           "summary": summary, "entries": RESULTS}
with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=False, indent=2))

lines = ["74 配套脚本 2/6 · 协变导数展开独立核验",
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
