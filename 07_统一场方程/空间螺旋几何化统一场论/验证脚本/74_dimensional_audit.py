# -*- coding: utf-8 -*-
"""74 号配套脚本 4/6 · 量纲审计：23 条收录式 + 8 条废弃式。

说明：本脚本是主仪器量纲层的**独立复现**（自实现量纲工具，双通道互校），
不是复制：若两套实现对同一式给出不同结论，本脚本即报 FAIL。

判据：SI 基本量纲四元组 (M, L, T, I)，指数相加。
输出：74_dimensional_audit_results.json / _out.txt
退出码：0 无不齐式；1 存在不齐式（内容层发现）；2 仪器层失效。
"""
from __future__ import print_function

import io
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "74_dimensional_audit_results.json")
OUT_TXT = os.path.join(HERE, "74_dimensional_audit_out.txt")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

IDX = {"M": 0, "L": 1, "T": 2, "I": 3}


def dm(*pairs):
    v = [Fraction(0)] * 4
    for e, b in pairs:
        v[IDX[b]] += Fraction(e)
    return tuple(v)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dinv(a):
    return tuple(-x for x in a)


def dpow(a, n):
    return tuple(x * n for x in a)


def dprod(*dims):
    out = (Fraction(0),) * 4
    for d in dims:
        out = dmul(out, d)
    return out


def dshow(a):
    parts = []
    for name, i in (("M", 0), ("L", 1), ("T", 2), ("I", 3)):
        if a[i] != 0:
            parts.append("%s^%s" % (name, a[i]))
    return "·".join(parts) if parts else "1"


# ---- 守卫：量纲工具自检 ----
_G = dm((-1, "M"), (3, "L"), (-2, "T"))
_C = dm((1, "L"), (-1, "T"))
if not (dmul(dinv(_G), _G) == (Fraction(0),) * 4 and dmul(_C, _C) == dm((2, "L"), (-2, "T"))):
    print("GUARD_FAIL: 量纲工具自检不通过")
    sys.exit(2)

M = dm((1, "M"))
L = dm((1, "L"))
T = dm((-1, "T"))
I = dm((1, "I"))
IT = dm((1, "I"), (1, "T"))
MU0 = dm((1, "M"), (1, "L"), (-2, "T"), (-2, "I"))
EPS0 = dm((-1, "M"), (-3, "L"), (4, "T"), (2, "I"))
ACC = dm((0, "M"), (1, "L"), (-2, "T"))
DL1 = dinv(L)
DL2 = dpow(dinv(L), 2)
DL3 = dpow(dinv(L), 3)
DT1 = dpow(dinv(T), -1)
DT2 = dpow(dinv(T), -2)
TAU = dm((-1, "L"))
AREA = dm((0, "M"), (2, "L"))
SOLID = (Fraction(0),) * 4
EF = dm((1, "M"), (1, "L"), (-3, "T"), (-1, "I"))
BF = dm((1, "M"), (0, "L"), (-2, "T"), (-1, "I"))
AV = dm((1, "M"), (1, "L"), (-2, "T"), (-1, "I"))
ENERGY = dm((1, "M"), (2, "L"), (-2, "T"))
FORCE = dm((1, "M"), (1, "L"), (-2, "T"))
MOM = dm((1, "M"), (1, "L"), (-1, "T"))
ANGM = dm((1, "M"), (2, "L"), (-1, "T"))
PHI = dm((1, "M"), (2, "L"), (-2, "T"), (-1, "I"))
MFLUX = dm((1, "M"), (-1, "L"), (-1, "T"))
QDENS = dprod(IT, DL3)

ENTRIES = []


def chk(sid, title, lhs, rhs):
    gap = tuple(lhs[i] - rhs[i] for i in range(4))
    ok = all(g == 0 for g in gap)
    ENTRIES.append({"id": sid, "title": title, "verdict": "PASS" if ok else "FAIL",
                    "left": dshow(lhs), "right": dshow(rhs), "gap": dshow(gap)})
    return ok


def note(sid, title, verdict, detail):
    ENTRIES.append({"id": sid, "title": title, "verdict": verdict, "detail": detail})


# ---------------- 收录式 23 条 ----------------
chk("D01", "Eq-09-01 dR/dt = c", dprod(L, DT1), _C)
chk("D02", "Eq-09-02 (r w)^2+h^2=c^2", dprod(L, L, T, T), dmul(_C, _C))
chk("D03", "Eq-09-03 m = (1/4πG)∮τ·dΣ", dprod(dinv(_G), TAU, AREA), M)
chk("D04", "Eq-09-04 g = -GM r̂/r^2", dprod(_G, M, DL2), ACC)
chk("D05", "Eq-09-05 p0 = m0 c0", dprod(M, _C), MOM)
chk("D06", "Eq-09-06 p = m(c-v)", dprod(M, _C), MOM)
chk("D07", "Eq-09-07 F = (c-v)Dm/Dt + mDc/Dt - mDv/Dt", dprod(M, DT1, _C), FORCE)
chk("D08", "Eq-09-08 □L = 0 平直极限", dprod(dpow(_C, -2), DT2, L), dprod(DL2, L))
chk("D09", "Eq-09-09 q = (1/4π)∮ω dΩ", dprod(T, SOLID), IT)
chk("D10", "Eq-09-10 E = γmc^2", dprod(M, _C, _C), ENERGY)
chk("D11", "Eq-09-11 B = (μ0/4π) q v×R/R^3", dprod(MU0, IT, _C, L, DL3), BF)
chk("D12", "Eq-09-12 ∇×A = B", dprod(DL1, AV), BF)
chk("D13", "Eq-09-13 F = (c-v)Dm/Dt", dprod(_C, M, DT1), FORCE)
chk("D14", "Eq-09-14 L = r×mc", dprod(L, M, _C), ANGM)
chk("D15", "Eq-09-15 □A = -4πG J_m", dprod(DL2, AV), dprod(_G, MFLUX))
chk("D16", "Eq-09-16 q = -d/dt ∮τ·dΣ", dprod(DT1, TAU, AREA), IT)
chk("D17", "Eq-09-17 ∇×E = -DB/Dt", dprod(DL1, EF), dprod(DT1, BF))
chk("D18", "Eq-09-18 g = c^-4(DE/Dt×B + E×DB/Dt)", dprod(dpow(_C, -4), DT1, EF, BF), ACC)
note("D19", "Eq-09-19 E = -∇φ - DA/Dt", "FAIL",
     "φ 读电势：[∇φ]=" + dshow(dprod(DL1, PHI)) + " vs [DA/Dt]=" + dshow(dprod(DT1, AV))
     + "（差 T）；φ 读引力势：[∇φ]=" + dshow(dprod(DL1, dm((0, "M"), (2, "L"), (-2, "T"))))
     + "（差 M^-1·T·I^-1）⇒ 两种读法均不可相加")
chk("D20", "Eq-09-20 □g=0,□E=0,□B=0（零取同量纲零）", dprod(DL2, ACC), dprod(DL2, ACC))
chk("D21", "Eq-09-21 q = n e", dprod((Fraction(0),) * 4, IT), IT)
chk("D22", "Eq-09-22 α(μ) = g'^2/(4π)", (Fraction(0),) * 4, (Fraction(0),) * 4)
chk("D23", "Eq-09-23 g_rad = -(q/4πε0c^3)(a×(r×a))/r",
    dprod(IT, dinv(EPS0), dpow(_C, -3), ACC, L, ACC, DL1), ACC)

# ---------------- 废弃式 8 条 ----------------
chk("X01", "废弃 E = r v^2 c^2/G", dprod(L, dmul(_C, _C), dmul(_C, _C), dinv(_G)), ENERGY)
chk("X02", "废弃 m = r v^2/G", dprod(L, dmul(_C, _C), dinv(_G)), M)
note("X03", "废弃 4π^2 r^3 c^2/(t^2 G h v) = 1", "BOUNDARY",
     "按 v=速率、h=长度读：左边量纲 " + dshow(dprod(L, L, L, dmul(_C, _C), DT2, _G, _C, _C))
     + "，非无量纲；原文未附符号表 ⇒ 不判死")
chk("X04", "废弃 q = 4π v^2 r/(cG)", dprod(dmul(_C, _C), L, dinv(_C), dinv(_G)), IT)
note("X05", "废弃 m = η c q", "BOUNDARY", "唯一相容读法 [η]=M^-1；若 η 无量纲则 FAIL ⇒ 须显式声明")
chk("X06", "废弃 G = α^2/ε0 c^2 = α^2 μ0", _G, MU0)
note("X07", "废弃 静止电荷产生磁场", "BOUNDARY", "B ∝ q v ⇒ v=0 ⇒ B≡0，与主张矛盾")
note("X08", "废弃 α = r/h_0", "BOUNDARY", "α 无量纲 ⇒ h_0 必须是长度标度 ⇒ 撞尺度开放项")

# ---------------- 与主仪器的交叉核对 ----------------
EXPECT_FAIL = set(["D03", "D09", "D15", "D16", "D18", "D19", "D23", "X04", "X06"])
_got_fail = set(e["id"] for e in ENTRIES if e["verdict"] == "FAIL")
if _got_fail != EXPECT_FAIL:
    print("GUARD_FAIL: 与主仪器的不齐式集合不一致 got=%s expect=%s"
          % (sorted(_got_fail), sorted(EXPECT_FAIL)))
    sys.exit(2)

summary = {"total": len(ENTRIES)}
for e in ENTRIES:
    summary[e["verdict"]] = summary.get(e["verdict"], 0) + 1
payload = {"meta": {"script": "74_dimensional_audit.py",
                    "role": "主仪器量纲层的独立复现（双通道互校）",
                    "crosscheck": "与主仪器不齐式集合逐项一致"},
           "summary": summary, "entries": ENTRIES}
with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
lines = ["74 配套脚本 4/6 · 量纲审计（23 收录式 + 8 废弃式）",
         "条目 %d：%s" % (len(ENTRIES),
                          " / ".join("%s %d" % (k, v) for k, v in sorted(summary.items()) if k != "total")),
         "交叉核对：与主仪器不齐式集合一致（%s）" % ", ".join(sorted(_got_fail)),
         "-" * 70]
for e in ENTRIES:
    lines.append("[%s] %s %s" % (e["verdict"], e["id"], e["title"]))
    if "gap" in e:
        lines.append("      左 %s | 右 %s | 缺口 %s" % (e["left"], e["right"], e["gap"]))
    else:
        lines.append("      " + e.get("detail", ""))
with io.open(OUT_TXT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
if not ("--quiet" in sys.argv):
    print("\n".join(lines))
if any(e["verdict"] == "FAIL" for e in ENTRIES):
    sys.exit(1)
sys.exit(0)
