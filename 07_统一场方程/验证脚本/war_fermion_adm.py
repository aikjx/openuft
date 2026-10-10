# -*- coding: utf-8 -*-
"""
SM 费米子纯规范场强重整化系数 a_ψ^m 复算（ADM 主公式的场强分量，承接 26A/27A「一圈/RG」）。

ADM 主公式（arXiv:2010.12109 Eq.3.7）：γ_ij = -2 g_m² [ Σ_ψ (1/2)a_ψ^m δ_ij + b_ij^m ]，
其中 (Z_m)_ψ = 1 + (α_m/4π)(1/ε)a_ψ^m 为 MS 费米子场强重整化常数。a_ψ^m = -2 C₂_m(R_ψ)
（对 SU(3)/SU(2)）；U(1) 取 GUT 归一 C₂=y²。C₂(SU3 三重态)=4/3、C₂(SU2 双重态)=3/4。

本卷自含复算全部 SM 费米子（q,u,d,ℓ,e + n=ν_R）在 SU(3)×SU(2)×U(1) 下的 a_ψ^m，
核验：标准 QCD 结果 a_q^3=-8/3、SU(2) 双重态 a=-3/2、单态为零，并给出主公式中
Σ(1/2)a_ψ 的场强贡献对代表算符（Q_qq(1)、Q_qu(1)、Q_uu、Q_ll）的值。零第三方依赖、精确分数。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_fermion_adm.json")

def F(x): return Fraction(x)
def F3(a, b): return Fraction(a, b)

# SM 费米子（左旋化）：C₂(SU3), C₂(SU2), 超荷 Y（物理，GUT 归一 y²=(3/5)Y² 于 U(1) 分支处理）
FERMIONS = {
    "q":  {"C2_3": F3(4, 3), "C2_2": F3(3, 4), "Y": F3(1, 6)},   # Q_L (3,2)_{1/6}
    "u":  {"C2_3": F3(4, 3), "C2_2": F(0),     "Y": F3(2, 3)},   # u^c (3̄,1)_{-2/3}
    "d":  {"C2_3": F3(4, 3), "C2_2": F(0),     "Y": F3(-1, 3)},  # d^c (3̄,1)_{1/3}
    "l":  {"C2_3": F(0),     "C2_2": F3(3, 4), "Y": F3(-1, 2)},  # L_L (1,2)_{-1/2}
    "e":  {"C2_3": F(0),     "C2_2": F(0),     "Y": F(-1)},      # e^c (1,1)_{-1}
    "n":  {"C2_3": F(0),     "C2_2": F(0),     "Y": F(0)},       # ν_R (1,1)_0
}

def a_psi(psi, m):
    """a_ψ^m = -2 C₂_m(R_ψ)；U(1) 用 GUT 归一 C₂=(3/5)Y²。"""
    if m == 3:
        return -2 * FERMIONS[psi]["C2_3"]
    if m == 2:
        return -2 * FERMIONS[psi]["C2_2"]
    if m == 1:
        return -2 * FERMIONS[psi]["Y"] * FERMIONS[psi]["Y"] * F3(3, 5)
    return None

RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- F1 SU(3) 场强系数 ----
f1 = True
for psi in ("q", "u", "d"):
    if a_psi(psi, 3) != F3(-8, 3):
        f1 = False
for psi in ("l", "e", "n"):
    if a_psi(psi, 3) != F(0):
        f1 = False
check("F1 SU(3) a_ψ³", "a_q³=a_u³=a_d³=-8/3（色三重态 2C₂=8/3）；a_ℓ³=a_e³=a_n³=0（单态）", f1)

# ---- F2 SU(2) 场强系数 ----
f2 = True
for psi in ("q", "l"):
    if a_psi(psi, 2) != F3(-3, 2):
        f2 = False
for psi in ("u", "d", "e", "n"):
    if a_psi(psi, 2) != F(0):
        f2 = False
check("F2 SU(2) a_ψ²", "a_q²=a_ℓ²=-3/2（弱双重态 2C₂=3/2）；单态为零", f2)

# ---- F3 U(1) 场强系数（GUT 归一 C₂=(3/5)Y²）----
# a_e¹ = -2(3/5) = -6/5；a_ν¹ = 0；比值关系核验
f3 = True
if a_psi("e", 1) != F3(-6, 5): f3 = False
if a_psi("n", 1) != F(0): f3 = False
if a_psi("q", 1) != F3(-1, 30): f3 = False     # -2(3/5)(1/36) = -6/180 = -1/30
if a_psi("u", 1) != F3(-8, 15): f3 = False     # -2(3/5)(4/9) = -24/45 = -8/15
check("F3 U(1) a_ψ¹(GUT)", "a_e¹=-6/5、a_n¹=0、a_q¹=-1/30、a_u¹=-8/15（GUT 归一 C₂=(3/5)Y²）", f3)

# ---- F4 主公式场强贡献 Σ(1/2)a_ψ^m（对代表四费米算符）----
def fs_contrib(fields, m):
    """主公式场强分量（diag, δ_ij 部分）：-2g²·Σ(1/2)a_ψ = -g²Σa_ψ；返回系数(×α_m/4π, 即 -Σa_ψ)。"""
    return -sum(a_psi(f, m) for f in fields)

# Q_qq(1)=(q̄γq)(q̄γq)：4×q → SU3: -Σ a = -4a_q³ = -4(-8/3) = 32/3
c_qq3 = fs_contrib(["q", "q", "q", "q"], 3)
# Q_uu=(ūγu)(ūγu)：4×u → SU3: -4(-8/3) = 32/3
c_uu3 = fs_contrib(["u", "u", "u", "u"], 3)
# Q_qu(1)=(q̄γq)(ūγu)：2×q+2×u → SU3: -2(-8/3)-2(-8/3) = 32/3
c_qu3 = fs_contrib(["q", "q", "u", "u"], 3)
# Q_ll=(ℓ̄γℓ)(ℓ̄γℓ)：4×ℓ → SU2: -4(-3/2) = 6
c_ll2 = fs_contrib(["l", "l", "l", "l"], 2)
# Q_ll SU3: 0
c_ll3 = fs_contrib(["l", "l", "l", "l"], 3)
f4 = (c_qq3 == F3(32, 3) and c_uu3 == F3(32, 3) and c_qu3 == F3(32, 3)
      and c_ll2 == F(6) and c_ll3 == F(0))
check("F4 主公式场强贡献", "Q_qq(1)/Q_uu/Q_qu(1) 的 SU(3) 场强贡献 = 32/3；Q_ll 的 SU(2) = 6、SU(3) = 0",
      f4, f"Q_qq³={c_qq3}, Q_uu³={c_uu3}, Q_qu³={c_qu3}, Q_ll²={c_ll2}, Q_ll³={c_ll3}")

# ---- F5 标准 QCD 结果交叉核对：γ_q(QCD) = -(8/3)α₃/(4π) ----
# 单色三重态夸克场强反常维数 γ_ψ = -2C₂(3)α₃/(4π) = -(8/3)α₃/(4π)（标准结果）
f5 = (a_psi("q", 3) == F3(-8, 3))
check("F5 QCD 交叉", "夸克场强 γ_q = -(8/3)α₃/4π（标准 QCD 结果，a_q³=-2C₂(3)）", f5)

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_fermion_adm.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "a_psi": {psi: {"a3": str(a_psi(psi, 3)), "a2": str(a_psi(psi, 2)), "a1": str(a_psi(psi, 1))} for psi in FERMIONS},
        "fs_contrib": {"Q_qq(1)³": str(c_qq3), "Q_uu³": str(c_uu3), "Q_qu(1)³": str(c_qu3),
                       "Q_ll²": str(c_ll2), "Q_ll³": str(c_ll3)},
    },
    "context": {
        "ref": "ADM 主公式 arXiv:2010.12109 Eq.(3.7)：γ_ij=-2g²[Σ(1/2)a_ψ δ+b_ij]；a_ψ=-2C₂(R)（MS 场强重整化）",
        "boundary": "本卷只含 ADM 的场强分量（a_ψ^m，自含复算）。算符-算符混频的 b_ij^m（四费米算符的算符重整化，需一循环图）未做；U(1) 用 GUT 归一 C₂=(3/5)Y²。完整 16×16（或 25 类）ADM 需外部矩阵输入。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_fermion_adm: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
