# -*- coding: utf-8 -*-
"""
SM 规范反常消去条件的精确核验（反常审计层，承接 15 卷 §7.3 点名）。

背景：
  15 卷 §7.3 点名「量子约束与反常审计」为开放项。本卷做其中第一性原理可严格计算的
  核心：核验 UFE 耦合的 SM 费米子内容（每代 l,e^c,q,u^c,d^c）满足全部三角反常消去
  条件（U(1)^3、U(1)-SU(2)^2、U(1)-SU(3)^2、引力混合、SU(2)^3）。无需外部 β 系数，
  全部用精确分数核验。

约定：零第三方依赖；超荷 Y 约定（Warsaw Tab.1）：l:Y=-1/2, e^c:Y=+1, q:Y=+1/6,
u^c:Y=-2/3, d^c:Y=+1/3；多重度（色×弱）：l:2, e^c:1, q:6, u^c:3, d^c:3。
反常系数精确分数计算：A_YYY=Σ n_f Y_f^3、A_YSU2=Σ_双线量 n Y、A_YSU3=Σ_夸克 n Y、
A_grav=Σ_全 n Y。
SU(2)^3 用 Pauli 精确核验 Tr(σ^a{σ^b,σ^c})=0（SU(2) 无三阶 Casimir，基础表示伪实）。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "sm_anomaly.json")


def F(n): return Fraction(n)
def F3(a, b): return Fraction(a, b)


# (name, 多重度 n_f, 超荷 Y)
FERMIONS = [
    ("l",  2, F3(-1, 2)),   # 弱双重态：2 分量
    ("e^c", 1, F(1)),
    ("q",  6, F3(1, 6)),    # 色3×弱2 = 6
    ("u^c", 3, F3(-2, 3)),
    ("d^c", 3, F3(1, 3)),
]

RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- A1 U(1)_Y^3 反常：Σ n_f Y^3 = 0 ----
ayyy = sum(n * y**3 for _, n, y in FERMIONS)
check("A1 U(1)^3", "Σ n_f Y_f^3 = 0（超荷三次反常消去）", ayyy == 0, f"Σ nY^3={ayyy}")

# ---- A2 U(1)_Y-SU(2)_L^2 混合反常：Σ_弱双重态 n Y = 0 ----
aysu2 = 2 * F3(-1, 2) + 6 * F3(1, 6)     # l + q 的弱双重态
check("A2 U(1)SU(2)^2", "Σ_{弱双重态} n Y = 0（超荷-弱混合反常）", aysu2 == 0, f"Σ={aysu2}")

# ---- A3 U(1)_Y-SU(3)_c^2 混合反常：Σ_夸克 n Y = 0 ----
aysu3 = 6 * F3(1, 6) + 3 * F3(-2, 3) + 3 * F3(1, 3)   # q + u^c + d^c
check("A3 U(1)SU(3)^2", "Σ_{夸克} n Y = 0（超荷-色混合反常）", aysu3 == 0, f"Σ={aysu3}")

# ---- A4 U(1)_Y-引力 混合反常：Σ_全部 n Y = 0 ----
agrav = sum(n * y for _, n, y in FERMIONS)
check("A4 引力混合", "Σ_{全部} n Y = 0（超荷-引力反常）", agrav == 0, f"Σ nY={agrav}")

# ---- A5 非平凡消去（各 nY^3 非零而总和为零；单代）----
nontrivial = any(n * y**3 != 0 for _, n, y in FERMIONS)
# 每代 A2/A3 单独消去（弱双重态、夸克各自为零）
gen_a2 = 2 * F3(-1, 2) + 6 * F3(1, 6)
gen_a3 = 6 * F3(1, 6) + 3 * F3(-2, 3) + 3 * F3(1, 3)
gen_ok = nontrivial and gen_a2 == 0 and gen_a3 == 0 and ayyy == 0 and agrav == 0
check("A5 非平凡消去", "各 nY^3 非零而单代总和为零（A1-A4 为真实消去非空设）",
      gen_ok, f"nontrivial={nontrivial}, A2={gen_a2}, A3={gen_a3}")

# ---- A6 SU(2)_L^3 反常：Tr(σ^a{σ^b,σ^c})=0（Pauli 精确）----
S0 = (F(0), F(0))
def cmul(a, b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def cadd(a, b): return (a[0]+b[0], a[1]+b[1])
def cmat(A, B):
    C = [[S0, S0], [S0, S0]]
    for i in range(2):
        for k in range(2):
            for j in range(2):
                C[i][j] = cadd(C[i][j], cmul(A[i][k], B[k][j]))
    return C
PAULI = [
    [[S0, (F(1), F(0))], [(F(1), F(0)), S0]],
    [[S0, (F(0), F(-1))], [(F(0), F(1)), S0]],
    [[(F(1), F(0)), S0], [S0, (F(-1), F(0))]],
]
def anticomm(A, B):
    return [[cadd(cmat(A, B)[i][j], cmat(B, A)[i][j]) for j in range(2)] for i in range(2)]
su2_ok = True
for a in range(3):
    for b in range(3):
        for c in range(3):
            M = anticomm(PAULI[b], PAULI[c])
            T = cmat(PAULI[a], M)
            tr = cadd(T[0][0], T[1][1])
            if tr != S0:
                su2_ok = False
check("A6 SU(2)^3", "Tr(σ^a{σ^b,σ^c})=0（SU(2) 基础伪实，无三阶反常）", su2_ok)

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "sm_anomaly.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "content": {name: (n, str(y)) for name, n, y in FERMIONS},
        "A1_U1Y3": str(ayyy), "A2_U1SU2": str(aysu2),
        "A3_U1SU3": str(aysu3), "A4_grav": str(agrav),
        "A5_per_gen": gen_ok, "A6_SU2_3": su2_ok,
    },
    "context": {
        "ref": "Warsaw Tab.1 超荷约定；标准三角反常消去条件",
        "boundary": "本卷核验 U(1)-型（超荷）与 SU(2)^3 反常消去（精确分数）。SU(3)^3 与 SU(2)^3 中 SU(3)^3 由 QCD 矢量性在每代内消去（标准结果，未用 d-符号显式计算以免约定歧义）；一圈 RG/β 函数、完整量子约束仍未做。",
        "ufe_note": "UFE 的 J_5^2 四费米算符为树级；其对反常的贡献需一圈级（三角图），不在本卷范围。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== sm_anomaly: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
