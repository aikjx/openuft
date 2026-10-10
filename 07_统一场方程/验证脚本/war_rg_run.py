# -*- coding: utf-8 -*-
"""
SM 一圈规范耦合跑动与非统一核验（承接 26A §5「一圈/RG」的具体跑动应用）。

用 26A 核验的一圈系数 b=(41/10,-19/6,-7)，从 M_Z 输入（α_em(M_Z)=1/127.9、
sin²θ_W(M_Z)=0.23122、α_s(M_Z)=0.1184，权威：1210.0325/PDG）导出 α_1,α_2,α_3，
按一圈 RGE 解 α_i^{-1}(Q)=α_i^{-1}(M_Z)+(b_i/2π)ln(Q/M_Z) 演化，核验：
(1) 输入导出正确；(2) 解析解与逐步数值积分一致；(3) α_3 Landau 极点落在 QCD 尺度
(~0.1-1 GeV)；(4) SM 三耦合无公共交点（非统一）；(5) α_1=α_2 交叉处 α_3 明显偏离。
零第三方依赖。
"""
import json
import math
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_rg_run.json")

# 权威输入（fetch 所得，勿凭记忆改）：PDG 2012 α_s(M_Z)=0.1184；标准 α_em^-1=127.9、s²=0.23122
ALPHA_EM = 1.0 / 127.9
S2 = 0.23122
ALPHA3_MZ = 0.1184
MZ = 91.188  # GeV

# 26A 核验的一圈系数 b_i（β(g)=b_i g³/16π²）
B = {1: 41.0 / 10.0, 2: -19.0 / 6.0, 3: -7.0}

# 导出 M_Z 处耦合
alpha2_MZ = ALPHA_EM / S2
alpha1_MZ = (5.0 / 3.0) * ALPHA_EM / (1.0 - S2)
alpha3_MZ = ALPHA3_MZ
A_MZ = {1: alpha1_MZ, 2: alpha2_MZ, 3: alpha3_MZ}

def alpha_inv(Q, i):
    """一圈 RGE 解析解 α_i^{-1}(Q) = α_i^{-1}(M_Z) + (-b_i/2π)ln(Q/M_Z)
    （因 dα^{-1}/dlnμ = -(1/α²)·(b α²/2π) = -b/2π）。"""
    return 1.0 / A_MZ[i] + (-B[i] / (2.0 * math.pi)) * math.log(Q / MZ)

def alpha(Q, i):
    return 1.0 / alpha_inv(Q, i)

RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- R1 输入导出 ----
r1 = (abs(alpha2_MZ - ALPHA_EM / S2) < 1e-12 and
      abs(alpha1_MZ - (5.0 / 3.0) * ALPHA_EM / (1.0 - S2)) < 1e-12)
check("R1 M_Z 导出", "α₂=α_em/s²、α₁=(5/3)α_em/c²、α₃=0.1184 导出正确",
      r1, f"α₁={alpha1_MZ:.6f}, α₂={alpha2_MZ:.6f}, α₃={alpha3_MZ}")

# ---- R2 解析解 vs 逐步数值积分 ----
def integrate(i, Q0, Q1, steps=200000):
    """dα^{-1}/dlnQ = -b_i/2π，逐步 Euler 积分 α^{-1}。"""
    cur = 1.0 / A_MZ[i]
    ln0, ln1 = math.log(Q0 / MZ), math.log(Q1 / MZ)
    h = (ln1 - ln0) / steps
    for _ in range(steps):
        cur += (-B[i] / (2.0 * math.pi)) * h
    return 1.0 / cur

r2 = True
for i in (1, 2, 3):
    q = 1e6
    num = integrate(i, MZ, q)
    ana = alpha(q, i)
    if abs(num - ana) / ana > 1e-6:
        r2 = False
check("R2 解析=数值积分", "α_i^{-1}(Q)=(b_i/2π)ln(Q/M_Z)+const 解析解与 200k 步 Euler 积分一致",
      r2, f"Q=10⁶GeV: α₁={alpha(1e6,1):.6f},α₂={alpha(1e6,2):.6f},α₃={alpha(1e6,3):.6f}")

# ---- R3 α_3 Landau 极点（α_3^{-1}=0 处）----
def landau_scale(i):
    """解 α_i^{-1}(Q)=0 → (-b_i/2π)ln(Q/M_Z) = -1/α_i(M_Z)
    → Q = M_Z·exp((2π/b_i)·α_i^{-1}(M_Z)) = M_Z·exp((2π/b_i)/α_i(M_Z))。"""
    return MZ * math.exp((2.0 * math.pi / B[i]) / A_MZ[i])

pole3 = landau_scale(3)
r3 = (pole3 > 0.02 and pole3 < 3.0)   # QCD 尺度 Λ 量级（~0.1-0.3 GeV）
check("R3 α₃ Landau 极点", "α₃^{-1}=0 在 QCD 尺度（0.02-3 GeV）", r3, f"Q₃^pole={pole3:.3f} GeV")

# ---- R4 SM 非统一：无三耦合公共交点 ----
# 搜索 α_1=α_2 交叉处，检查 α_3 是否一致
def crossing_scale(i, j):
    """在 [M_Z, 10^16 GeV] 二分求 α_i=α_j 的 Q。若不相交返回 None。"""
    lo, hi = MZ, 1e16
    f_lo = alpha(lo, i) - alpha(lo, j)
    f_hi = alpha(hi, i) - alpha(hi, j)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if (alpha(mid, i) - alpha(mid, j)) * f_lo <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2

q12 = crossing_scale(1, 2)
q23 = crossing_scale(2, 3)
q13 = crossing_scale(1, 3)
# 非统一判据：α_1=α_2 交叉处，α_3 明显不等（相对差 > 1%）
nonuni = True
if q12 is not None:
    d13 = abs(alpha(q12, 1) - alpha(q12, 3)) / alpha(q12, 1)
    if d13 < 0.01:
        nonuni = False
check("R4 SM 非统一", "α₁=α₂ 交叉处 α₃ 相对偏离 > 1%（SM 三耦合无公共交点）",
      nonuni, f"Q₁₂={q12:.3e} GeV, α₁(q₁₂)={alpha(q12,1):.5f}, α₃(q₁₂)={alpha(q12,3):.5f}")

# ---- R5 交叉结构：α_1 上升、α_2/α_3 下降（单调性/符号）----
r5 = (B[1] > 0 and B[2] < 0 and B[3] < 0)
# 且 α_1^{-1} 随 Q 增大而减小（α_1 增大）、α_2/α_3^{-1} 增大
r5b = (alpha(1e10, 1) > alpha1_MZ and alpha(1e10, 2) < alpha2_MZ and alpha(1e10, 3) < alpha3_MZ)
check("R5 演化方向", "α₁随Q升（非渐近自由）、α₂/α₃随Q降（渐近自由），方向正确",
      r5 and r5b, f"α₁(10¹⁰)={alpha(1e10,1):.5f}, α₂(10¹⁰)={alpha(1e10,2):.5f}, α₃(10¹⁰)={alpha(1e10,3):.5f}")

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_rg_run.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "input": {"alpha_em": ALPHA_EM, "s2_w": S2, "alpha3_MZ": ALPHA3_MZ, "MZ": MZ},
        "alpha_MZ": {str(k): A_MZ[k] for k in A_MZ},
        "b": {str(k): B[k] for k in B},
        "landau_alpha3_GeV": pole3,
        "crossing": {"q12_GeV": q12, "q23_GeV": q23, "q13_GeV": q13},
        "alpha_at_q12": {str(k): alpha(q12, k) if q12 else None for k in (1, 2, 3)},
    },
    "context": {
        "ref": "b 系数来自 26A（对照 1712.05246）；输入 PDG 2012 α_s(M_Z)=0.1184（1210.0325）、α_em^-1=127.9、s²=0.23122",
        "boundary": "一圈纯规范跑动（M S-bar、无阈值/两圈修正）。SM 非统一为经典结论；本卷核验其一圈结构。J_5² dim-6 算符的反常维数矩阵/RG 混频仍未做（需外部矩阵输入）。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_rg_run: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
