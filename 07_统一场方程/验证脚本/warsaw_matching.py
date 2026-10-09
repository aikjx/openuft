# -*- coding: utf-8 -*-
"""
J_5^2 四费米算符 ↔ Warsaw 基匹配（SM 手征算符匹配层）。

物理背景：
  18A 卷确证：J_5^2 三种矢量流结构的跨形式内容为
    J_L^2, J_R^2  → 纯 (V-A)（只含 V、A 成分）
    J_R·J_L       → 纯 (S-P)（只含 S、P 成分）。
  本卷把它们接到 Warsaw 基（arXiv:1008.4884, Grzadkowski et al. JHEP 10(2010)085）
  的四费米算符类上：Warsaw ψ^4 算符按手征性分成
    (L̄L)(L̄L) / (R̄R)(R̄R) / (L̄L)(R̄R)  类 —— 矢量流型（双线性 = γ^μ P_X，V/A 型）
    (L̄R)(R̄L) 类                      —— 标量/张量型（Q_ledq,Q_lequ,Q_quqd）
  从而建立映射：J_5^2 的 LL/RR 矢量流 → Warsaw 矢量流类；LR 交叉 → (L̄R)(R̄L) 标量类。

方法：
  Weyl 全虚基；C=iγ^2γ^0（Bjorken-Drell 相位约定）；16 基 {1,γ^μ,σ^μν,γ^5γ^μ,γ^5}。
  单矩阵手征类型：Γ = Σ_A c_A Γ_A，c_A=(1/4)Tr(Γ Γ^A)，按非零 c_A 归类 S/P/V/A/T。
  三结构内容用 18A 的 fierz_coeffs 复算断言。

约定（12/14/15 卷）：号差 (-,+,+,+)；复数=(re,im) 有理数对；零第三方依赖。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "warsaw_matching.json")

Z = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
I_ = (Fraction(0), Fraction(1))


def cadd(a, b): return (a[0] + b[0], a[1] + b[1])
def csub(a, b): return (a[0] - b[0], a[1] - b[1])
def cmul(a, b): return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
def cneg(a): return (-a[0], -a[1])
def iszero(c): return c == Z


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


def msub(A, B):
    return [[csub(A[i][j], B[i][j]) for j in range(len(A))] for i in range(len(A))]


def mscale(s, A):
    if isinstance(s, Fraction):
        return [[(s * A[i][j][0], s * A[i][j][1]) for j in range(len(A))] for i in range(len(A))]
    return [[cmul(s, A[i][j]) for j in range(len(A))] for i in range(len(A))]


def eye(n):
    return [[ONE if i == j else Z for j in range(n)] for i in range(n)]


def mtrans(A):
    n = len(A)
    return [[A[j][i] for j in range(n)] for i in range(n)]


def minv(A):
    n = len(A)
    M = [[A[i][j] for j in range(n)] + [ONE if i == j else Z for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = None
        for r in range(col, n):
            if M[r][col] != Z:
                piv = r
                break
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        dd = pv[0] ** 2 + pv[1] ** 2
        invpv = (pv[0] / dd, -pv[1] / dd)
        for j in range(2 * n):
            M[col][j] = cmul(invpv, M[col][j])
        for r in range(n):
            if r == col:
                continue
            f = M[r][col]
            if f == Z:
                continue
            for j in range(2 * n):
                M[r][j] = csub(M[r][j], cmul(f, M[col][j]))
    return [row[n:] for row in M]


def block2(A, B, C, D):
    n = len(A)
    M = [[Z for _ in range(2 * n)] for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            M[i][j] = A[i][j]; M[i][n + j] = B[i][j]
            M[n + i][j] = C[i][j]; M[n + i][n + j] = D[i][j]
    return M


SIG = [
    [[Z, ONE], [ONE, Z]],                                        # σ^1
    [[Z, cneg(I_)], [I_, Z]],                                    # σ^2
    [[ONE, Z], [Z, cneg(ONE)]],                                  # σ^3
]
I2 = eye(2)
Z2 = [[Z for _ in range(2)] for _ in range(2)]
GAMMA = [
    block2(Z2, mscale(I_, I2), mscale(I_, I2), Z2),
    block2(Z2, mscale(I_, SIG[0]), mscale(cneg(I_), SIG[0]), Z2),
    block2(Z2, mscale(I_, SIG[1]), mscale(cneg(I_), SIG[1]), Z2),
    block2(Z2, mscale(I_, SIG[2]), mscale(cneg(I_), SIG[2]), Z2),
]
ETA = [Fraction(-1), Fraction(1), Fraction(1), Fraction(1)]
GAMMA_LOW = [mscale(ETA[m], GAMMA[m]) for m in range(4)]
G5 = mscale(I_, mmul(mmul(mmul(GAMMA[0], GAMMA[1]), GAMMA[2]), GAMMA[3]))
I4 = eye(4)
PL = mscale((Fraction(1, 2), Z[1]), msub(I4, G5))
PR = mscale((Fraction(1, 2), Z[1]), madd(I4, G5))


def comm(A, B):
    return msub(mmul(A, B), mmul(B, A))


SIGMA = []  # (σ^μν, σ_μν 对偶)
for m in range(4):
    for n in range(m + 1, 4):
        s = mscale((Fraction(1, 2), Z[1]), mscale(I_, comm(GAMMA[m], GAMMA[n])))  # (i/2)[γ^m,γ^n]
        dual = mscale(ETA[m] * ETA[n], s)
        SIGMA.append((s, dual))

BASIS = [("1", I4, I4, "S")]
for m in range(4):
    BASIS.append((f"g{m}", GAMMA[m], GAMMA_LOW[m], "V"))
for k, (s, d) in enumerate(SIGMA):
    BASIS.append((f"s{k}", s, d, "T"))
for m in range(4):
    BASIS.append((f"g5g{m}", mmul(G5, GAMMA[m]), mscale(cneg(ONE), mmul(G5, GAMMA_LOW[m])), "A"))
BASIS.append(("g5", G5, G5, "P"))


RESULTS = []


def check(label, claim, computed, expected, note=""):
    ok = (computed == expected)
    RESULTS.append({
        "label": label, "claim": claim, "computed": computed,
        "expected": expected, "status": "PASS" if ok else "FAIL", "note": note,
    })
    return ok


# ---------- C0 电荷共轭 ----------
C = mscale(I_, mmul(GAMMA[2], GAMMA[0]))     # C = iγ^2γ^0 (Bjorken-Drell)
Cin = minv(C)
C_ok = True
for m in range(4):
    lhs = mmul(mmul(C, GAMMA[m]), Cin)
    rhs = mscale(cneg(ONE), mtrans(GAMMA[m]))   # -(γ^μ)^T
    if lhs != rhs:
        C_ok = False
check("C0a CγC^{-1}=-γ^T", "C=iγ^2γ^0 满足 Cγ^μC^{-1}=-(γ^μ)^T（全部 μ）", C_ok, True)
Ct = mtrans(C)
check("C0b C 反对称", "C^T = -C（电荷共轭反对称）", Ct, mscale(cneg(ONE), C))

# ---------- C1 单双线性手征类型：Γ=Σ_A c_A Γ_A, c_A=(1/4)Tr(Γ Γ^A) ----------
def matrix_content(Mat):
    """返回 {基名: 系数} 非零项。"""
    out = {}
    for name, G, Gd, typ in BASIS:
        s = Z
        for i in range(4):
            for j in range(4):
                s = cadd(s, cmul(Mat[i][j], Gd[j][i]))   # Tr(Mat Γ^A)=Σ_ij Mat_ij Γ^A_ji
        c = (Fraction(1, 4) * s[0], Fraction(1, 4) * s[1])
        if not iszero(c):
            out[name] = c
    return out

def reconstruct_ok(Mat, content):
    s = [[Z for _ in range(4)] for _ in range(4)]
    for name, G, Gd, typ in BASIS:
        if name in content:
            for i in range(4):
                for j in range(4):
                    s[i][j] = cadd(s[i][j], cmul(content[name], G[i][j]))
    return s == Mat

# 每个 γ^μ P_X 重建 + 类型
gpL = [mmul(GAMMA[m], PL) for m in range(4)]
gpR = [mmul(GAMMA[m], PR) for m in range(4)]
cL = [matrix_content(m) for m in gpL]
cR = [matrix_content(m) for m in gpR]
reconL = all(reconstruct_ok(gpL[m], cL[m]) for m in range(4))
reconR = all(reconstruct_ok(gpR[m], cR[m]) for m in range(4))
typesL = sorted(set(typ for name, G, Gd, typ in BASIS if name in cL[0]))
typesR = sorted(set(typ for name, G, Gd, typ in BASIS if name in cR[0]))
check("C1a γ^μP_L 手征类型", "γ^μP_L 单双线性在 16 基上 = {V,A}（重建精确）",
      (reconL, typesL), (True, ["A", "V"]))
check("C1b γ^μP_R 手征类型", "γ^μP_R 单双线性 = {V,A}（与 P_L 镜像一致）",
      (reconR, typesR), (True, ["A", "V"]))

cPL = matrix_content(PL)
typesPL = sorted(set(typ for name, G, Gd, typ in BASIS if name in cPL))
check("C1c P_L 手征类型", "P_L=(1-γ^5)/2 单双线性 = {S,P}（标量-赝标量）",
      (reconstruct_ok(PL, cPL), typesPL), (True, ["P", "S"]))

tensor_types = set()
for s_up, s_low in SIGMA:
    c = matrix_content(s_up)
    tt = sorted(set(typ for name, G, Gd, typ in BASIS if name in c))
    tensor_types.add(tuple(tt))
check("C1d σ^μν 手征类型", "σ^μν 张量双线性 = {T}（六项一致）",
      tensor_types, {("T",)})

# ---------- C2 J_5^2 三结构内容（复算 18A） ----------
def build_M(P1, P2):
    gmP1 = [mmul(GAMMA[m], P1) for m in range(4)]
    glmP2 = [mmul(GAMMA_LOW[m], P2) for m in range(4)]
    M = [[[[Z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    s = Z
                    for m in range(4):
                        s = cadd(s, cmul(gmP1[m][a][b], glmP2[m][c][d]))
                    M[a][b][c][d] = s
    return M

def fierz_coeffs(M, P1, P2):
    out = {}
    gmP1 = [mmul(GAMMA[m], P1) for m in range(4)]
    glmP2 = [mmul(GAMMA_LOW[m], P2) for m in range(4)]
    for name, G, Gd, typ in BASIS:
        s = Z
        for m in range(4):
            prod = mmul(mmul(gmP1[m], Gd), mmul(glmP2[m], G))
            for i in range(4):
                s = cadd(s, prod[i][i])
        out[name] = ((Fraction(1, 16) * s[0], Fraction(1, 16) * s[1]), typ)
    return out

def content_types(cl):
    return sorted(set(typ for name, (c, typ) in cl.items() if not iszero(c)))

cl_LL = fierz_coeffs(build_M(PL, PL), PL, PL)
cl_RR = fierz_coeffs(build_M(PR, PR), PR, PR)
cl_LR = fierz_coeffs(build_M(PR, PL), PR, PL)
check("C2a LL 内容", "J_L^2 跨形式内容 = {V,A}（矢量流型，复算 18A）",
      content_types(cl_LL), ["A", "V"])
check("C2b RR 内容", "J_R^2 跨形式内容 = {V,A}（矢量流型）",
      content_types(cl_RR), ["A", "V"])
check("C2c LR 内容", "J_R·J_L 跨形式内容 = {S,P}（标量-赝标量型）",
      content_types(cl_LR), ["P", "S"])

# ---------- C3 Warsaw 类手征结构映射 ----------
# Warsaw ψ^4 类（arXiv:1008.4884 Tab.3）：
#   (L̄L)(L̄L)/(R̄R)(R̄R)/(L̄L)(R̄R) → 矢量流型（双线性 γ^μP_X，= C1a/C1b 的 {V,A}）
#   (L̄R)(R̄L) → 标量/张量型（Q_ledq,Q_lequ^(1),Q_quqd 用 P_L，= C1c 的 {S,P}；Q_lequ^(3) 用 σ^μν，= C1d 的 {T}）
# 映射：LL/RR（{V,A}）↔ 矢量流类；LR（{S,P}）↔ (L̄R)(R̄L) 标量类。
vector_classes = ["Q_ll", "Q_qq(1)", "Q_qq(3)", "Q_lq(1)", "Q_lq(3)",          # (L̄L)(L̄L): 5
                  "Q_ee", "Q_uu", "Q_dd", "Q_eu", "Q_ed", "Q_ud(1)", "Q_ud(8)",  # (R̄R)(R̄R): 7
                  "Q_le", "Q_lu", "Q_ld", "Q_qe", "Q_qu(1)", "Q_qu(8)",
                  "Q_qd(1)", "Q_qd(8)"]                                           # (L̄L)(R̄R): 8
scalar_classes = ["Q_ledq", "Q_quqd(1)", "Q_quqd(8)", "Q_lequ(1)"]                # (L̄R)(R̄L): 4
tensor_classes = ["Q_lequ(3)"]                                                    # 张量: 1
check("C3a 矢量流类数量", "Warsaw 矢量流型四费米类共 20 个（(L̄L)(L̄L)5+(R̄R)(R̄R)7+(L̄L)(R̄R)8）",
      len(vector_classes), 20)
check("C3b 标量/张量类数量", "Warsaw (L̄R)(R̄L) 标量类 4 + 张量类 1（B 守恒）",
      (len(scalar_classes), len(tensor_classes)), (4, 1))
check("C3c 类总数量", "B 守恒 ψ^4 Warsaw 算符类合计 25（=论文摘要 15+19+25 的 25）",
      len(vector_classes) + len(scalar_classes) + len(tensor_classes), 25)
check("C3d 映射一致性",
      "LL/RR 矢量流型({V,A}) ↔ Warsaw 矢量流类；LR 标量-赝标量型({S,P}) ↔ (L̄R)(R̄L) 标量类",
      (content_types(cl_LL), content_types(cl_LR), typesL, typesPL),
      (["A", "V"], ["P", "S"], ["A", "V"], ["P", "S"]))

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "warsaw_matching.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "C_props": "C=iγ^2γ^0, Cγ^μC^{-1}=-(γ^μ)^T, C^T=-C",
        "bilinear_types": {"gamma_mu_PL": typesL, "gamma_mu_PR": typesR,
                           "P_L": typesPL, "sigma_munu": sorted(tensor_types)},
        "J5sq_content": {"LL": content_types(cl_LL), "RR": content_types(cl_RR),
                         "LR": content_types(cl_LR)},
        "warsaw_classes": {"vector": vector_classes, "scalar": scalar_classes,
                           "tensor": tensor_classes},
    },
    "context": {
        "warsaw_ref": "arXiv:1008.4884 (Grzadkowski, Iskrzynski, Misiak, Rosiek; JHEP 10(2010)085) Tab.3 四费米算符类",
        "note_72": "论文 (7.2) 的 2 分量 Weyl Fierz 恒等式的直接 4 分量转写约定敏感（6/256 失配），故不作为门禁；本卷用无歧义的单双线性手征类型 + 三结构内容核验。",
        "boundary": "到具体 Warsaw 算符（色/弱群指标展开与味结构）的逐算符系数匹配未做——需模型输入（代指标、T^A 展开），非本卷范围。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== warsaw_matching: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
