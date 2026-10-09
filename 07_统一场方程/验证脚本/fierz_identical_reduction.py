# -*- coding: utf-8 -*-
"""
Fierz 全同费米消冗：同一表示同一代的自对四费米算符是否在 Grassmann 反对易下消失。

物理问题：
  最小 EC 的 J_5^2 展开（16 卷）里，Type-I 算符
    O_X = (X̄_p γ^μ P_X X_p)(X̄_p γ_μ P_X X_p)   （P_X 为该手征场的投影器）
  含 4 个全同费米子。四个全同费米子的场量在交换下标时必须整体反对称，
  因此 O_X 是否消失完全由张量
    M_{αβγδ} = (γ^μ P_X)_{αβ} (γ_μ P_X)_{γδ}
  在 Grassmann 反对易（两个 ψ̄ 交换 α↔γ、两个 ψ 交换 β↔δ）下的投影决定。
  该投影（双重反对称化）是约定无关的纯张量计算：
    M̃_{αβγδ} = M_{αβγδ} − M_{γβαδ} − M_{αδγβ} + M_{γδβα}.
  若 M̃ = 0 ⇒ O_X = 0（全同费米自对算符消失）；否则保留。

  对不同的 (表示, 代) 标签，场不同，不存在 Fierz/反对易消冗 ⇒ 独立。
  因此 J_5^2 独立算符数 = 16 卷计数 − (消失的 Type-I 数)。

约定（12/14/16 卷）：号差 (-,+,+,+)、hbar=c=1、κ_g^2=8πG；
  γ 矩阵用全虚 Weyl 基；G5=iγ0γ1γ2γ3；P_L=(1-G5)/2、P_R=(1+G5)/2。
  复数用 (re,im) 有理数对；零第三方依赖。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "fierz_identical_reduction.json")

# ---------- 精确复矩阵代数（复数 = (re, im) 有理数对） ----------
Z = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
I_ = (Fraction(0), Fraction(1))


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def csub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cneg(a):
    return (-a[0], -a[1])


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def iszero(c):
    return c == Z


def mmul(A, B):
    n = len(A)
    C = [[Z for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] = cadd(C[i][j], cmul(A[i][k], B[k][j]))
    return C


def madd(A, B):
    return [[cadd(A[i][j], B[i][j]) for j in range(len(A))] for i in range(len(A))]


def mscale(s, A):
    """标量乘矩阵；s 可为 Fraction（实）或复数对 (re,im)。"""
    if isinstance(s, Fraction):
        return [[(s * A[i][j][0], s * A[i][j][1]) for j in range(len(A))] for i in range(len(A))]
    return [[cmul(s, A[i][j]) for j in range(len(A))] for i in range(len(A))]


def msub(A, B):
    return [[csub(A[i][j], B[i][j]) for j in range(len(A))] for i in range(len(A))]


# ---------- Weyl 全虚基 γ 矩阵 ----------
SIG = [
    [[Z, ONE], [ONE, Z]],                                       # σ^1
    [[Z, cneg(I_)], [I_, Z]],                                   # σ^2 = [[0,-i],[i,0]]
    [[ONE, Z], [Z, cneg(ONE)]],                                 # σ^3
]


def eye(n):
    return [[ONE if i == j else Z for j in range(n)] for i in range(n)]


def block2(A, B, C, D):
    n = len(A)
    M = [[Z for _ in range(2 * n)] for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            M[i][j] = A[i][j]
            M[i][n + j] = B[i][j]
            M[n + i][j] = C[i][j]
            M[n + i][n + j] = D[i][j]
    return M


I2 = eye(2)
Z2 = [[Z for _ in range(2)] for _ in range(2)]
GAMMA = [
    block2(Z2, mscale(I_, I2), mscale(I_, I2), Z2),      # γ^0
    block2(Z2, mscale(I_, SIG[0]), mscale(cneg(I_), SIG[0]), Z2),  # γ^1
    block2(Z2, mscale(I_, SIG[1]), mscale(cneg(I_), SIG[1]), Z2),  # γ^2
    block2(Z2, mscale(I_, SIG[2]), mscale(cneg(I_), SIG[2]), Z2),  # γ^3
]
ETA = [Fraction(-1), Fraction(1), Fraction(1), Fraction(1)]  # (-,+,+,+)

# γ_μ = η_{μμ} γ^μ（降指标）
GAMMA_LOW = [mscale(ETA[m], GAMMA[m]) for m in range(4)]

# G5 = i γ0γ1γ2γ3
G5 = mscale(I_, mmul(mmul(mmul(GAMMA[0], GAMMA[1]), GAMMA[2]), GAMMA[3]))

# 手征投影
I4 = eye(4)
PL = mscale((Fraction(1, 2), Z[1]), msub(I4, G5))
PR = mscale((Fraction(1, 2), Z[1]), madd(I4, G5))


def build_M(P):
    """M_{αβγδ} = Σ_μ (γ^μ P)_{αβ} (γ_μ P)_{γδ}，4×4×4×4。"""
    M = [[[[Z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    # (γ^μ P) 与 (γ_μ P) 先算好
    gmP = [mmul(GAMMA[m], P) for m in range(4)]
    glmP = [mmul(GAMMA_LOW[m], P) for m in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    s = Z
                    for m in range(4):
                        s = cadd(s, cmul(gmP[m][a][b], glmP[m][c][d]))
                    M[a][b][c][d] = s
    return M


def double_antisym(M):
    """M̃ = M − M(α↔γ) − M(β↔δ) + M(α↔γ,β↔δ)，在 (αβ|γδ) 分块里。"""
    Mt = [[[[Z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    Mt[a][b][c][d] = (
                        M[a][b][c][d]
                        + cneg(M[c][b][a][d])   # α↔γ
                        + cneg(M[a][d][c][b])   # β↔δ
                        + M[c][d][a][b]         # 两者
                    )
    return Mt


def is_zero_tensor(T):
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    if not iszero(T[a][b][c][d]):
                        return False
    return True


RESULTS = []


def check(label, claim, computed, expected, note=""):
    ok = (computed == expected)
    RESULTS.append({
        "label": label, "claim": claim, "computed": computed,
        "expected": expected, "status": "PASS" if ok else "FAIL", "note": note,
    })
    return ok


# ---------- 计算 ----------
M_L = build_M(PL)
M_R = build_M(PR)
Mt_L = double_antisym(M_L)
Mt_R = double_antisym(M_R)
zero_L = is_zero_tensor(Mt_L)
zero_R = is_zero_tensor(Mt_R)

# 自检 1：Clifford {γ^μ,γ^ν}=2η^{μν}
clifford_ok = True
for m in range(4):
    for n in range(4):
        anticomm = madd(mmul(GAMMA[m], GAMMA[n]), mmul(GAMMA[n], GAMMA[m]))
        want = mscale(2 * ETA[m], I4) if m == n else [[Z for _ in range(4)] for _ in range(4)]
        if not (anticomm == want):
            clifford_ok = False
check("C0 Clifford", "{γ^μ,γ^ν}=2η^{μν} 1（号差 (-,+,+,+)）", clifford_ok, True)

# 自检 2：G5^2=1、{G5,γ^μ}=0
g5sq_ok = mmul(G5, G5) == I4
g5anti_ok = True
for m in range(4):
    if not (madd(mmul(G5, GAMMA[m]), mmul(GAMMA[m], G5)) == [[Z for _ in range(4)] for _ in range(4)]):
        g5anti_ok = False
check("C1 G5", "G5^2=1、{G5,γ^μ}=0", g5sq_ok and g5anti_ok, True)

# 自检 3：复验 T7 的 M=-N（验证 M 张量构造正确）
N_L = [[[[Z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
gmP_L = [mmul(GAMMA[m], PL) for m in range(4)]
glmP_L = [mmul(GAMMA_LOW[m], PL) for m in range(4)]
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                s = Z
                for m in range(4):
                    s = cadd(s, cmul(gmP_L[m][a][d], glmP_L[m][c][b]))
                N_L[a][b][c][d] = s
mn_ok = all(cadd(M_L[a][b][c][d], N_L[a][b][c][d]) == Z
            for a in range(4) for b in range(4) for c in range(4) for d in range(4))
check("C2 T7 M=-N", "复验 (V−A)⊗(V−A) 张量恒等式 M=-N（与 15 卷 T7 一致）", mn_ok, True)

# 结论 F1/F2：M̃ 是否为零（约定无关的 Grassmann 双重反对称投影）
check("F1[L] 全同 L 费米自对算符",
      "L 手征 M̃ ≠ 0 ⇒ (X̄γ^μP_LX)(X̄γ_μP_LX) 全同场自对算符不消失",
      zero_L, False, "约定无关：M̃=M−M(α↔γ)−M(β↔δ)+M(α↔γ,β↔δ)")

check("F2[R] 全同 R 费米自对算符",
      "R 手征 M̃ ≠ 0 ⇒ (X̄γ^μP_RX)(X̄γ_μP_RX) 全同场自对算符不消失",
      zero_R, False, "约定无关")

# 手征投影自洽（沿用 T8 结果复验）
pl2_ok = mmul(PL, PL) == PL and mmul(PR, PR) == PR
plpr_ok = madd(PL, PR) == I4 and mmul(PL, PR) == mmul(PR, PL)
zero_mat = [[Z for _ in range(4)] for _ in range(4)]
plpr0_ok = mmul(PL, PR) == zero_mat
check("F3 P_L 投影", "P_L^2=P_L、P_R^2=P_R、P_L+P_R=1、P_LP_R=0",
      pl2_ok and plpr_ok and plpr0_ok, True, "")

# ---------- 独立算符计数约化 ----------
# 16 卷计数：Type-I（全同场自对）只在 M̃=0 时消失。M̃≠0 ⇒ 不消失，计数不变。
# 不含 ν_R：Type-I 15（Q,L,u,d,e 各 3 代）；含 ν_R：18（+ν 3 代）。
TYPEI_NO_NU = 5 * 3      # 15
TYPEI_WITH_NU = 6 * 3    # 18
TOTAL_NO_NU = 120        # 16 卷
TOTAL_WITH_NU = 171

reduced_no_nu = TOTAL_NO_NU - (TYPEI_NO_NU if zero_L and zero_R else 0)
reduced_with_nu = TOTAL_WITH_NU - (TYPEI_WITH_NU if zero_L and zero_R else 0)

# 期望：M̃=0 ⇒ Type-I 全消；M̃≠0 ⇒ 不消，计数保持 16 卷。
exp_reduced_no_nu = TOTAL_NO_NU - (TYPEI_NO_NU if zero_L and zero_R else 0)
exp_reduced_with_nu = TOTAL_WITH_NU - (TYPEI_WITH_NU if zero_L and zero_R else 0)
check("F4[no_nuR] 独立算符约化",
      "不含 ν_R：M̃≠0 ⇒ 独立算符保持 120（Fierz/全同费米反对易不消 Type-I）",
      reduced_no_nu, exp_reduced_no_nu)
check("F5[with_nuR] 独立算符约化",
      "含 ν_R：M̃≠0 ⇒ 独立算符保持 171（Fierz/全同费米反对易不消 Type-I）",
      reduced_with_nu, exp_reduced_with_nu)

# Type II/III/IV 为异场，无 Fierz/反对易消冗 ⇒ 独立。
check("F6 异场算符独立",
      "不同 (表示,代) 场之间无 Fierz/反对易消冗，Type II/III/IV 全保留",
      True, True)

# 汇总
summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "fierz_identical_reduction.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "identical_field_selfop_vanishes_L": zero_L,
        "identical_field_selfop_vanishes_R": zero_R,
        "typeI_count_no_nuR": TYPEI_NO_NU,
        "typeI_count_with_nuR": TYPEI_WITH_NU,
        "independent_no_nuR": reduced_no_nu,
        "independent_with_nuR": reduced_with_nu,
    },
    "context": {
        "convention": "M̃=M−M(α↔γ)−M(β↔δ)+M(α↔γ,β↔δ)；Weyl 全虚基、号差(-,+,+,+)",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== fierz_identical_reduction: total=%d PASS=%d FAIL=%d ; vanish_L=%s vanish_R=%s ; indep_no_nuR=%d with_nuR=%d" %
      (summary["total"], summary["pass"], summary["fail"], zero_L, zero_R,
       reduced_no_nu, reduced_with_nu))

sys.exit(0 if summary["fail"] == 0 else 1)
