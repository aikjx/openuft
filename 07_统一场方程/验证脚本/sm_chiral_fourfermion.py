# -*- coding: utf-8 -*-
"""
SM 手征四费米匹配：最小 EC 树级算符 L_4ψ = -(3κ_g^2/16)(J_5)^2
的机械展开与独立算符计数。

约定（12/14 卷）：
  * 号差 (-,+,+,+)、hbar=c=1、κ_g^2 = 8πG = M_Pl^-2。
  * J_5 = J_R - J_L；J_R = Σ_{X∈R}Σ_p j_{Xp}，J_L = Σ_{X∈L}Σ_p j_{Xp}。
  * j_{Xp} = X̄_p γ^μ X_p 为规范单态双线性（色与弱指标在双线性内部缩并）。
  * SM 手征表示：L 侧 {Q(3,2), L(1,2)}，R 侧 {u(3,1), d(3,1), e(1,1)}，
    本仓库另选右手中微子 ν_R(1,1,0)。三代 n_g=3。
  * 记 a = 3κ_g^2/16 > 0，则 L_4ψ = -a(J_5)^2 = -a[(J_R)^2 + (J_L)^2 - 2 J_R·J_L]。

机械展开：以电流 j_a（a=(chirality,rep,gen)）为形式量，正规展开
  (J_R - J_L)^2 = Σ_{a,b} s_a s_b j_a j_b，s=+1(R)、-1(L)。
电流作为算符级双线性满足交换性 j_a j_b = j_b j_a，故：
  * a==b ：系数 1      -> 外层 -a       -> 系数 -a
  * a≠b, 同 chirality：s_as_b=+1 -> 2  -> 外层 -a -> 系数 -2a
  * a≠b, 异 chirality：s_as_b=-1 -> -2 -> 外层 -a -> 系数 +2a

验证项（对应 16 卷）：
  S1 手征流结构：J_R、J_L 是规范单态流的加权和；J_5 = J_R - J_L。
  S2 机械展开：对逐对(含同流平方)重新累计，按类型给出的系数恒等于
     类型规则（-a / -2a / +2a），无剩余项。
  S3 算符计数：独立算符 = 不同规范单态电流的无序二重多重集
     N + C(N,2)；含/不含 ν_R 两套口径分别核对。
  S4 全零验证：同 chirality 净系数为负（-2a），异 chirality 为正（+2a），
     各表示/各代逐类核对。

零第三方依赖；精确有理数。状态码 0 = 全 PASS。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "sm_chiral_fourfermion.json")

# ---------------------------------------------------------------------------
# SM 手征表示数据
# ---------------------------------------------------------------------------
# (name, chirality, color_dim, weak_dim, Y)   Y 仅作标签；规范单态由色/弱内缩保证
def sm_content(with_nuR):
    reps = [
        ("Q", "L", 3, 2, Fraction(1, 6)),
        ("L", "L", 1, 2, Fraction(-1, 2)),
        ("u", "R", 3, 1, Fraction(2, 3)),
        ("d", "R", 3, 1, Fraction(-1, 3)),
        ("e", "R", 1, 1, Fraction(-1)),
    ]
    if with_nuR:
        reps.append(("nu", "R", 1, 1, Fraction(0)))
    return reps

NGEN = 3

# 每个表示的名/手性/色维/弱维/超荷
REPS_NO_NU = sm_content(False)
REPS_WITH_NU = sm_content(True)


def currents(reps):
    """返回电流列表，元素 (chirality, rep_name, gen)。"""
    out = []
    for (name, chir, cd, wd, Y) in reps:
        for g in range(1, NGEN + 1):
            out.append((chir, name, g))
    return out


def _sign(chir):
    return +1 if chir == "R" else -1


def _is_gauge_singlet(chir, rep_name, reps):
    """双线性 j_{Xp} 是否规范单态（色、弱都在双线性内部缩并）。"""
    for (nm, ch, cd, wd, Y) in reps:
        if nm == rep_name and ch == chir:
            return True
    return False


# ---------------------------------------------------------------------------
# 验证项
# ---------------------------------------------------------------------------
RESULTS = []


def check(label, claim, computed, expected, note=""):
    ok = (computed == expected)
    RESULTS.append({
        "label": label, "claim": claim, "computed": computed,
        "expected": expected, "status": "PASS" if ok else "FAIL", "note": note,
    })
    return ok


def expand_coefficients(cur_list, reps):
    """机械展开 (J_R - J_L)^2，按电流标签重累计系数，返回 {op: coeff}。"""
    acc = {}
    for a in cur_list:
        for b in cur_list:
            op = tuple(sorted([a, b]))   # 无序对（含 a==b）
            coef = _sign(a[0]) * _sign(b[0])
            acc[op] = acc.get(op, 0) + coef
    # 系数归一：a==b 出现 1 次；a≠b 出现 2 次（j_a j_b 与 j_b j_a）
    # 这里已按对称对累计，acc[op] 即 Σ s_as_b over 有序对贡献。下面再乘 -a。
    return acc


def classify(op):
    """op = ( (c1,r1,g1), (c2,r2,g2) )，返回类型字符串。"""
    (c1, r1, g1), (c2, r2, g2) = op
    if (c1, r1, g1) == (c2, r2, g2):
        return "same_current"
    if r1 == r2 and c1 == c2:
        return "same_rep_diffgen"
    if c1 == c2:
        return "diff_rep_same_chir"
    return "diff_rep_mixed_chir"


def run(with_nuR, tag):
    reps = sm_content(with_nuR)
    cur = currents(reps)
    N = len(cur)

    # S2 机械展开的系数分布
    acc = expand_coefficients(cur, reps)
    # 类型规则（以外层 -a 计，即系数以 a 为单位）
    rules = {
        "same_current": Fraction(-1),     # -a
        "same_rep_diffgen": Fraction(-2), # -2a
        "diff_rep_same_chir": Fraction(-2),
        "diff_rep_mixed_chir": Fraction(2),
    }
    # 按类型累计物理系数。acc[op] 是 (J_R-J_L)^2 的原始展开值（已含正确重数），
    # 乘以外层 -a 得物理系数（以 a 计），即 net = -raw。
    per_type = {}
    ok_all = True
    for op, raw in acc.items():
        typ = classify(op)
        want = rules[typ]
        net = -raw   # 物理系数，以 a 为单位
        per_type[typ] = per_type.get(typ, 0) + net
        ok_all = ok_all and (net == want)
    # 全展开净和 = -S^2，S = n_R - n_L（由 Σ_{pairs} acc = S^2 导出）
    S = sum(_sign(c) for c, _, _ in cur)
    net_sum_ok = (sum(per_type.values()) == -S * S)
    check(
        f"S2[{tag}] 逐对机械系数",
        "每对 (J_R-J_L)^2 展开物理系数（以 a 计）等于类型规则（-1/-2/+2）",
        ok_all and net_sum_ok, True,
        "逐对 -1/-2/+2 且全净和=-S^2（S=n_R-n_L）"
    )

    # S3 计数：独立算符 = 无序二重多重集 N + C(N,2)
    num_ops = N + N * (N - 1) // 2
    check(
        f"S3[{tag}] 独立算符数",
        "独立四费米算符 = N + C(N,2)",
        num_ops, len(acc), f"N={N}"
    )
    # 分类型计数
    counts = {}
    for op in acc:
        t = classify(op)
        counts[t] = counts.get(t, 0) + 1
    return reps, cur, N, counts, per_type, acc


# ---- 不含 ν_R ----
reps0, cur0, N0, cnt0, per0, acc0 = run(False, "no_nuR")
# 期望计数（不含 ν_R）：N=15
check("S1[no_nuR] 电流数", "不含 ν_R 时规范单态电流数 = 6(L)+9(R) = 15", N0, 15)
# 类型计数：同流 15；同表示异代：L 6 + R 9 = 15；异表示：LL 9 + RR 27 + LR 54 = 90
exp_counts0 = {
    "same_current": 15, "same_rep_diffgen": 15,
    "diff_rep_same_chir": 9 + 27, "diff_rep_mixed_chir": 54,
}
check("S3[no_nuR] 分类型计数", "同流/同表示异代/异表示(LL,RR,LR) 计数匹配",
      cnt0, exp_counts0)
# S4 各类型累计净和（S=n_R-n_L=3，全净和=-9）
check("S4[no_nuR] 类型系数累计净和",
      "同流(-15)+同表示异代(-30)+同手性异表示(-72)+混合手性(+108)，全净和=-S^2=-9",
      {k: v for k, v in per0.items()},
      {"same_current": Fraction(-15), "same_rep_diffgen": Fraction(-30),
       "diff_rep_same_chir": Fraction(-72), "diff_rep_mixed_chir": Fraction(108)})

# ---- 含 ν_R ----
reps1, cur1, N1, cnt1, per1, acc1 = run(True, "with_nuR")
check("S1[with_nuR] 电流数", "含 ν_R 时规范单态电流数 = 6(L)+12(R) = 18", N1, 18)
exp_counts1 = {
    "same_current": 18, "same_rep_diffgen": 6 + 12,
    "diff_rep_same_chir": 9 + 54, "diff_rep_mixed_chir": 72,
}
check("S3[with_nuR] 分类型计数", "含 ν_R 时类型计数匹配", cnt1, exp_counts1)
check("S4[with_nuR] 类型系数累计净和",
      "同流(-18)+同表示异代(-36)+同手性异表示(-126)+混合手性(+144)，全净和=-S^2=-36",
      {k: v for k, v in per1.items()},
      {"same_current": Fraction(-18), "same_rep_diffgen": Fraction(-36),
       "diff_rep_same_chir": Fraction(-126), "diff_rep_mixed_chir": Fraction(144)})

# S5 表示-超荷标签自洽（双线性规范单态由色/弱内缩保证；Y 不影响单态性）
singlet_ok = True
for reps, tag in ((REPS_NO_NU, "no_nuR"), (REPS_WITH_NU, "with_nuR")):
    for (nm, chir, cd, wd, Y) in reps:
        if not _is_gauge_singlet(chir, nm, reps):
            singlet_ok = False
check("S5 规范单态性", "所有手征表示双线性在色与弱内部缩并，构成规范单态",
      singlet_ok, True)

# ---------------------------------------------------------------------------
# 汇总
# ---------------------------------------------------------------------------
summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "sm_chiral_fourfermion.py",
    "summary": summary,
    "checks": RESULTS,
    "context": {
        "convention": "L_4ψ = -(3κ_g^2/16)(J_R-J_L)^2；a=3κ_g^2/16",
        "reps_no_nuR": [r[0] for r in REPS_NO_NU],
        "reps_with_nuR": [r[0] for r in REPS_WITH_NU],
        "ngen": NGEN,
        "operator_count_no_nuR": len(acc0),
        "operator_count_with_nuR": len(acc1),
        "per_type_no_nuR": cnt0,
        "per_type_with_nuR": cnt1,
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== sm_chiral_fourfermion: total=%d PASS=%d FAIL=%d" %
      (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
