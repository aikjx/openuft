# -*- coding: utf-8 -*-
"""
SM 一圈规范耦合 β 系数自含复算（承接 24A/25A §5「一圈/RG」的规范扇区起点）。

按权威公式 β_i = -(11/3)C₂(G_i) + (2/3)Σ_Weyl [dim(其他规范)×S₂(R_i)] + (1/3)Σ_scalar [dim×S₂(R_i)]
（Weyl κ=1/2；S₂(fund)=1/2；C₂(SU3)=3、C₂(SU2)=2），从 SM 场内容（21A 超荷 ×3 代）复算
b_3、b_2、β_Y，并核验 β_1=(3/5)β_Y 与权威值 (41/10, -19/6, -7)。
公式/数值来源：arXiv:2402.15124 (6)式 + Tab.1；arXiv:1712.05246 b_i^(SM)=(41/10,-19/6,-7)。
零第三方依赖、精确分数。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_beta_sm.json")

def F(x): return Fraction(x)
def F3(a, b): return Fraction(a, b)

NG = 3   # 三代
# 场内容：名称, SU(3)维数, SU(2)维数, S₂(SU3), S₂(SU2), 超荷Y, Weyl(1)或标量(0)
# fermions (Weyl, ×NG)；scalar H (1)
FERMIONS = [
    ("Q_L", 3, 2, F3(1,2), F3(1,2), F3(1,6)),   # (3,2)_{1/6}
    ("u^c", 3, 1, F3(1,2), 0,     F3(-2,3)),     # (3̄,1)_{-2/3}
    ("d^c", 3, 1, F3(1,2), 0,     F3(1,3)),      # (3̄,1)_{1/3}
    ("L_L", 1, 2, 0,     F3(1,2), F3(-1,2)),     # (1,2)_{-1/2}
    ("e^c", 1, 1, 0,     0,      F(-1)),         # (1,1)_{-1}
]
SCALARS = [
    ("H", 1, 2, 0, F3(1,2), F3(-1,2)),           # (1,2)_{-1/2}
]
C2_SU3 = 3
C2_SU2 = 2

RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- B1 逐场 SU(3) 贡献 ----
b3_f = 0
rows3 = []
for (name, d3, d2, s3, s2, y) in FERMIONS:
    c = NG * d2 * s3 * F3(2, 3)      # 3 代 × dim(SU2) × S₂(SU3) × (2/3)
    b3_f += c
    rows3.append((name, c))
b3 = -C2_SU3 * F3(11, 3) + b3_f
# 期望逐场（含 3 代）：Q_L 2, u^c 1, d^c 1（权威 Tab.1）
exp3 = {"Q_L": F(2), "u^c": F(1), "d^c": F(1), "L_L": F(0), "e^c": F(0)}
b1_ok = all(rows3[i][1] == exp3[rows3[i][0]] for i in range(len(rows3)))
check("B1 SU(3) 逐场+总计", "逐场 β₃ = (2,1,1,0,0)×3代；b₃ = -11 + 4 = -7",
      b1_ok and b3 == F(-7), f"b₃={b3}, 逐场={rows3}")

# ---- B2 逐场 SU(2) 贡献 ----
b2_f = 0
rows2 = []
for (name, d3, d2, s3, s2, y) in FERMIONS:
    c = NG * d3 * s2 * F3(2, 3)
    b2_f += c
    rows2.append((name, c))
b2_s = 0
for (name, d3, d2, s3, s2, y) in SCALARS:
    c = d3 * s2 * F3(1, 3)
    b2_s += c
b2 = -C2_SU2 * F3(11, 3) + b2_f + b2_s
exp2 = {"Q_L": F(3), "u^c": F(0), "d^c": F(0), "L_L": F(1), "e^c": F(0)}
b2_ok = all(rows2[i][1] == exp2[rows2[i][0]] for i in range(len(rows2)))
check("B2 SU(2) 逐场+总计", "逐场 β₂ = (3,0,0,1,0)×3代 + H(1/6)；b₂ = -22/3 + 4 + 1/6 = -19/6",
      b2_ok and b2 == F3(-19, 6), f"b₂={b2}, 逐场={rows2}, H={b2_s}")

# ---- B3 U(1) 逐场贡献（未归一 β_Y，后转 β_1=(3/5)β_Y）----
by_f = 0
rows1 = []
for (name, d3, d2, s3, s2, y) in FERMIONS:
    c = NG * d3 * d2 * y * y * F3(2, 3)
    by_f += c
    rows1.append((name, c))
by_s = 0
for (name, d3, d2, s3, s2, y) in SCALARS:
    c = d3 * d2 * y * y * F3(1, 3)
    by_s += c
by = by_f + by_s
b1 = by * F3(3, 5)   # β_1 = (3/5)β_Y（GUT 归一）
# 权威逐场（未归一）：q 1/3, u 8/3, d 2/3, l 1, e 2, H 1/6
exp1 = {"Q_L": F3(1, 3), "u^c": F3(8, 3), "d^c": F3(2, 3), "L_L": F(1), "e^c": F(2)}
b3_ok = all(rows1[i][1] == exp1[rows1[i][0]] for i in range(len(rows1)))
check("B3 U(1) 逐场+归一", "逐场 β_Y = (1/3,8/3,2/3,1,2)×3代 + H(1/6)；β₁=(3/5)β_Y = 41/10",
      b3_ok and by == F3(41, 6) and b1 == F3(41, 10), f"β_Y={by}, β₁={b1}, 逐场={rows1}, H={by_s}")

# ---- B4 权威对照：(41/10, -19/6, -7) ----
check("B4 权威对照", "b = (β₁, b₂, b₃) = (41/10, -19/6, -7) 与权威值一致",
      b1 == F3(41, 10) and b2 == F3(-19, 6) and b3 == F(-7),
      f"({b1}, {b2}, {b3})")

# ---- B5 总费米子 β_Y 与 ΣY² 关系 ----
# β_Y(fermion) = (2/3)·3·Σ₍场,代₎dim·Y²；Σ₍场,代₎dim·Y² = 10（含色/弱多重度）
fermion_y2 = sum(NG * d3 * d2 * y * y for (name, d3, d2, s3, s2, y) in FERMIONS)
check("B5 费米Σ(dim·Y²)=10", "含多重度的费米子 Σ dim·Y² = 10（三代），β_Y(fermion)=(2/3)·10=20/3",
      fermion_y2 == F(10) and by_f == F3(20, 3), f"Σ={fermion_y2}, β_Y^f={by_f}")

# ---- B6 反常复述（用 21A 左旋化共轭超荷：e^c:+1）----
# 多重度 n × 左旋化超荷：l:2,Y=-1/2; e^c:1,Y=+1; q:6,Y=+1/6; u^c:3,Y=-2/3; d^c:3,Y=+1/3
ANO = [("l", 2, F3(-1, 2)), ("e^c", 1, F(1)), ("q", 6, F3(1, 6)),
       ("u^c", 3, F3(-2, 3)), ("d^c", 3, F3(1, 3))]
a3 = sum(n * y**3 for (_, n, y) in ANO)   # Σ n Y³
a1 = sum(n * y for (_, n, y) in ANO)      # Σ n Y
check("B6 反常复述", "Σ n Y³ = 0（U(1)³）且 Σ n Y = 0（U(1)-grav），用左旋化超荷与 21A 一致",
      a3 == F(0) and a1 == F(0), f"ΣnY³={a3}, ΣnY={a1}")

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_beta_sm.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "b1": str(b1), "b2": str(b2), "b3": str(b3),
        "beta_Y": str(by), "beta_Y_fermion": str(by_f), "beta_Y_higgs": str(by_s),
        "per_field_3": [str(x) for x in rows3],
        "per_field_2": [str(x) for x in rows2],
        "per_field_1": [str(x) for x in rows1],
        "au": "(41/10, -19/6, -7)",
    },
    "context": {
        "ref": "arXiv:2402.15124 (6)式+Tab.1（SM 行）；arXiv:1712.05246 b_i^(SM)=(41/10,-19/6,-7)",
        "boundary": "一圈规范耦合 β（M S-bar 方案、单 Higgs 双线量）。本卷为该扇区的尺度跑动环境；J_5² dim-6 算符的完整一圈反常维数矩阵/RG 混频（需外部矩阵输入）未做；Yukawa 与 Higgs 自耦合对 β 的高阶贡献未做。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_beta_sm: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))
print("   b1=%s  b2=%s  b3=%s" % (b1, b2, b3))

sys.exit(0 if summary["fail"] == 0 else 1)
