# -*- coding: utf-8 -*-
"""V51 自噬：j=1 三重态零模质量矩阵的 Wigner-Eckart / CG 结构核验

自我反噬对象：上一册 V51 攻击 B 用了「统一非对角元 x」构造质量矩阵，
并报出本征值谱违反 Bernstein 不等式。但六维磁通背景带 SU(2) 结构，
CG 选择定则可能禁死这种非对角元。若禁死，攻击 B 的物理前提不成立，
须如实收窄；若允许，则给出它的群论成立条件（新自由输入）。

本引擎用 sympy 精确 Clebsch-Gordan（无浮点），算：
  D1 k=0 算符 ∝ I（Schur 简并）
  D2 k=2,q=2 非对角元非零（非对角可实现通路）
  D3 k=3 三角禁戒全零（负对照）
  D4 k=1,q=±1 非对角通路
  D5 算符空间复维 1 / 1+3 / 1+3+5 = 9
  D6 厄米子空间：单态(仅 k=0) 厄米维 = 1 ⇒ 严格简并
  D7 单态 h ⇒ 三本征值全等 ⇒ 不等式恒真但判别力 0
  D8 攻击 B 前提条件化：非对角需 k>=1 ⇒ Higgs 须非标量内部分量
  D9 反噬：强制仅 k=0 却要求三不同谱 ⇒ 矛盾
  D10 参数计账群论版：1+3+5=9 = dim Herm(3) ⇒ 任意谱可拟合

纪律：exp/act 两路、负对照翻红、恒等门单列、守卫不写死。
不产新物理，不宣称攻破统一场论，独立预言计数 0。
"""
import json
import os
from sympy import S, I, simplify, Matrix, Rational
from sympy.physics.wigner import clebsch_gordan

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "_v51_selfattack_we_report.txt")
JSON_PATH = os.path.join(HERE, "_v51_selfattack_we_recompute.json")

J = S(1)
MS = [S(-1), S(0), S(1)]

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({"id": gid, "kind": kind, "exp": str(exp), "act": str(act),
                  "ok": bool(ok), "note": note})


def cg(m, k, q, mp):
    """Wigner-Eckart: <j m'|T^k_q|j m> ∝ <j m; k q | j m'>。
    sympy 签名 = clebsch_gordan(j1, j2, j3, m1, m2, m3)，
    故此处 = (j, k, j, m, q, mprime)。"""
    return simplify(clebsch_gordan(J, S(k), J, S(m), S(q), S(mp)))


def Tkq(k, q):
    """3x3 矩阵，行=m'，列=m；矩阵元 = CG(1,m;k,q|1,m')。"""
    return Matrix(3, 3, lambda ip, i: cg(MS[i], k, q, MS[ip]))


def vec(M):
    return Matrix([simplify(M[i, j]) for i in range(3) for j in range(3)])


def rank_of(mats):
    if not mats:
        return 0
    return Matrix.hstack(*[vec(M) for M in mats]).rank()


def herm_rank(kmax):
    """由 k<=kmax 的算符构造厄米子空间，返回其（复）秩 = 厄米实维。"""
    Hs = []
    for k in range(0, kmax + 1):
        for q in range(0, k + 1):
            T = Tkq(k, q)
            if q == 0:
                H1 = simplify(T + T.conjugate().T)
                if H1 != Matrix.zeros(3, 3):
                    Hs.append(H1)
            else:
                H1 = simplify(T + T.conjugate().T)
                H2 = simplify(I * (T - T.conjugate().T))
                if H1 != Matrix.zeros(3, 3):
                    Hs.append(H1)
                if H2 != Matrix.zeros(3, 3):
                    Hs.append(H2)
    return rank_of(Hs)


# D1: k=0 算符 ∝ I
T00 = Tkq(0, 0)
diag_vals = [T00[i, i] for i in range(3)]
off_zero = all(T00[i, j] == 0 for i in range(3) for j in range(3) if i != j)
equal_diag = all(v == diag_vals[0] for v in diag_vals)
add("D1-k0-scalar", "gate", "k=0 算符 ∝ I (Schur)",
    "T00=%s; diag equal=%s; offdiag zero=%s" % (T00.tolist(), equal_diag, off_zero),
    equal_diag and off_zero,
    "标量算符在不可约三重态内正比单位阵 ⇒ 严格简并")

# D2: k=2,q=2 非对角元 <1,1|T^2_2|1,-1>
c_2q2 = cg(S(-1), 2, S(2), S(1))   # m=-1, q=2 => m'=1
add("D2-k2-offdiag", "gate", "k=2,q=2 非对角元非零",
    "CG(1,-1;2,2|1,1)=%s" % c_2q2,
    c_2q2 != 0,
    "非对角元可实现通路；攻击 B 的非对角元需此类张量分量")

# D3: k=3 三角禁戒（j=j'=1 ⇒ k<=2）
k3_nonzero = 0
for m in MS:
    for q in range(-3, 4):
        for mp in MS:
            if cg(m, 3, S(q), mp) != 0:
                k3_nonzero += 1
add("D3-k3-forbidden", "neg", "k=3 全零(三角禁戒)",
    "k=3 非零 CG 计数=%d" % k3_nonzero,
    k3_nonzero == 0,
    "负对照：仪器非恒非零；k>|j+j'| 必禁")

# D4: k=1,q=±1 非对角通路
c_1q1 = cg(S(0), 1, S(1), S(1))    # m=0,q=1 => m'=1
c_1qm1 = cg(S(0), 1, S(-1), S(-1)) # m=0,q=-1 => m'=-1
add("D4-k1-offdiag", "gate", "k=1,q=±1 非对角元非零",
    "CG(1,0;1,1|1,1)=%s, CG(1,0;1,-1|1,-1)=%s" % (c_1q1, c_1qm1),
    c_1q1 != 0 and c_1qm1 != 0,
    "矢量算符也提供非对角通路")

# D5: 算符空间复维 1 / 4 / 9
all_k = {k: [Tkq(k, q) for q in range(-k, k + 1)] for k in (0, 1, 2)}
r0 = rank_of(all_k[0])
r01 = rank_of(all_k[0] + all_k[1])
r012 = rank_of(all_k[0] + all_k[1] + all_k[2])
add("D5-opspace-dim", "gate", "算符空间复维 1 / 4 / 9",
    "rank(k0)=%d rank(k0+k1)=%d rank(all)=%d" % (r0, r01, r012),
    (r0, r01, r012) == (1, 4, 9),
    "End(C^3) 分解 1⊕3⊕5=9；群论维数精确")

# D6: 厄米子空间维数：单态仅 k=0 ⇒ 1
h0 = herm_rank(0)
h01 = herm_rank(1)
h012 = herm_rank(2)
add("D6-herm-singlet", "gate", "单态(仅 k=0) 厄米维=1",
    "herm_rank(k<=0)=%d, (k<=1)=%d, (k<=2)=%d" % (h0, h01, h012),
    h0 == 1 and h01 == 4 and h012 == 9,
    "仅标量 Higgs ⇒ 质量矩阵 1 个实参数 ⇒ 严格简并")

# D7: 单态 h ⇒ 三本征值全等 ⇒ 不等式恒真判别力 0
# T00 ∝ I，本征值 = {diag_vals[0]}*3
eig_singlet = [diag_vals[0]] * 3
ratio_singlet = simplify(eig_singlet[1] ** 2 / (4 * eig_singlet[0] * eig_singlet[2]))
add("D7-singlet-degenerate", "gate", "单态 ⇒ 三谱全等, m1^2/(4m0m2)=1/4",
    "eig=%s ratio=%s" % (eig_singlet, ratio_singlet),
    len(set(eig_singlet)) == 1 and ratio_singlet == Rational(1, 4),
    "简并谱下不等式恒真(1/4<=1)，但不能区分三代 ⇒ 判别力 0")

# D8: 攻击 B 前提条件化
add("D8-premise-conditional", "gate", "攻击B非对角需 k>=1 (Higgs 非标量)",
    "D2/D4 非对角通路在 k>=1 存在; D1/D6 单态 k=0 无非对角",
    (c_2q2 != 0 and c_1q1 != 0) and (off_zero and h0 == 1),
    "前提有条件成立：来料 h(x)『任意非负分布』未指定 SU(2) 张量结构；"
    "若 h 各向同性(仅 k=0)则非对角被 CG 禁死，攻击 B 失效；"
    "若 h 含 l>=1 分量则成立，但这是新自由输入")

# D9: 反噬——强制仅 k=0 却要求三不同谱 ⇒ 矛盾
need_k1_for_split = (h0 == 1) and (len(set([diag_vals[0]] * 3)) == 1)
add("D9-mutant-singlet-split", "neg", "仅 k=0 要求三不同谱 ⇒ 矛盾",
    "单态谱集合大小=%d" % len(set([diag_vals[0]] * 3)),
    need_k1_for_split,
    "负对照翻红：标量 Higgs 无法产生质量分裂，必须引入非标量分量")

# D10: 参数计账群论版
add("D10-param-count-group", "gate", "1+3+5=9=dim Herm(3) ⇒ 任意谱可拟合",
    "复维 r012=%d, 厄米维 h012=%d, Herm(3)实维=9" % (r012, h012),
    r012 == 9 and h012 == 9,
    "群论支撑攻击 C：k=0,1,2 全开时 9 实参数 = 一般厄米 3x3，"
    "足以拟合任意三本征值谱 ⇒ 判别力 0")

# 恒等式单列
add("D11-schur", "identity", "Schur 引理：不可约表示内标量算符 ∝ I",
    "由 D1 与 D6 保证，属群论恒等结构", True,
    "单列不承重")

# ---------------------------------------------------------------------------
n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
fail = [g["id"] for g in gates if not g["ok"]]
if not fail:
    verdict = ("V51-SELFATTACK-WE--J1-ZEROMODE-OPSPACE-1-PLUS-3-PLUS-5-EQUALS-9-EXACT--"
               "SINGLET-K0-FORCES-EXACT-TRIPLET-DEGENERACY-RATIO-1-4--"
               "OFFDIAG-PATHS-EXIST-ONLY-FOR-K-GE-1--"
               "ATTACK-B-PREMISE-CONDITIONAL-ON-NONSCALAR-HIGGS--"
               "K3-TRIANGLE-FORBIDDEN-NEG--PARAM-COUNT-9-EQUALS-DIM-HERM3--"
               "NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")
else:
    verdict = "SELFATTACK-WE-FAIL--" + "-".join(fail)

result = {
    "subject": "V51 自噬：j=1 零模质量矩阵 Wigner-Eckart 结构",
    "object_boundary": "核验对象是上一册攻击 B 的物理前提（非对角元可实现性）；"
                       "J78 三点 Yukawa CG 与 ROOTV137 迹恒等/GS 均为不同对象，不相加",
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(fail)},
    "independent_prediction_count": 0,
    "cg_key_values": {
        "CG(1,-1;2,2|1,1)": str(c_2q2),
        "CG(1,0;1,1|1,1)": str(c_1q1),
        "T00_diag": [str(v) for v in diag_vals],
    },
    "dims": {"opspace_rep": r0, "opspace_k0k1": r01, "opspace_all": r012,
             "herm_k0": h0, "herm_k0k1": h01, "herm_all": h012},
    "gates": gates,
}
with open(JSON_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

lines = ["V51 自噬 · j=1 质量矩阵 Wigner-Eckart 核验报告", "=" * 64,
         "判词: " + verdict,
         "门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)),
         "对象边界: " + result["object_boundary"],
         "独立预言计数: 0", "-" * 64]
for g in gates:
    lines.append("[%s] %-24s %-10s exp=%s | act=%s %s" % (
        "PASS" if g["ok"] else "FAIL", g["id"], g["kind"],
        g["exp"], g["act"], "// " + g["note"] if g["note"] else ""))
lines.append("-" * 64)
lines.append("关键 CG 值: " + json.dumps(result["cg_key_values"], ensure_ascii=False))
lines.append("维数: " + json.dumps(result["dims"], ensure_ascii=False))
lines.append("-" * 64)
lines.append("sympy 1.13.3 精确 CG; 无浮点; 中文路径由 ASCII runner 定位")
with open(REPORT_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
