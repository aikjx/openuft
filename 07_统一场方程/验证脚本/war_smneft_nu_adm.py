# -*- coding: utf-8 -*-
"""
SMNEFT (n̄γn)(X̄γX) 矢量算符的纯规范对角 ADM 为零 + penguin 混频非零。

按 arXiv:2010.12109 约定（a_ψ=-C₂、a_ψ¹=-y²，见 29A）+ 主公式 γ_ij=-2g²[Σ½a_ψ δ+b_ij]，
自含复现 O_nd 对角 ADM=0（A.21，场强与流-流相消），并推广到全部 6 个 (νν)(XX) 矢量算符
（O_nn,O_ne,O_nd,O_nu,O_ℓn,O_nq —— 即 25A 的 ν 类算符 Q_νν,Q_νe,Q_νu,Q_νd,Q_νl,Q_νq）：
纯规范对角 ADM 均为零（n 是规范单态，X 流-流 b=C₂/y² 恰抵消 X 场强 Σ½a）。
核验 penguin 混频 O_nd→O_nu 非零（A.17/A.22）。零第三方依赖、精确分数。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_smneft_nu_adm.json")

Y = {"q": Fraction(1, 6), "u": Fraction(-2, 3), "d": Fraction(1, 3),
     "l": Fraction(-1, 2), "e": Fraction(1), "n": Fraction(0)}
C2 = {"q": {"3": Fraction(4, 3), "2": Fraction(3, 4)},
      "u": {"3": Fraction(4, 3), "2": Fraction(0)},
      "d": {"3": Fraction(4, 3), "2": Fraction(0)},
      "l": {"3": Fraction(0), "2": Fraction(3, 4)},
      "e": {"3": Fraction(0), "2": Fraction(0)},
      "n": {"3": Fraction(0), "2": Fraction(0)}}
N_C = Fraction(3)


def a_psi(psi, m):
    if m in ("2", "3"):
        return -C2[psi][m]
    if m == "1":
        return -Y[psi] * Y[psi]
    return Fraction(0)


def fs_sum(fields, m):
    """场强分量 Σ(1/2)a_ψ^m（主公式的 δ_ij 部分）。"""
    return sum(Fraction(1, 2) * a_psi(f, m) for f in fields)


def current_b(X, m):
    """(X̄γX) 流-流 b：单规范玻色子在 X 流内交换 → b = C₂_m(R_X)（m=2,3）或 y_X²（m=1）。"""
    if m in ("2", "3"):
        return C2[X][m]
    return Y[X] * Y[X]


def diag_gamma(X, m):
    """(X̄γX)(n̄γn) 对角 ADM：γ = -2[Σ½a_ψ + b_X]，场 = [n,n,X,X]。n 无规范荷，b_X 为 X 流内交换。"""
    fields = ["n", "n", X, X]
    return -2 * (fs_sum(fields, m) + current_b(X, m))


RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- V1 O_nn：总规范单态，γ=0（Ċ_nn=0）----
v1 = (a_psi("n", "1") == 0 and a_psi("n", "2") == 0 and a_psi("n", "3") == 0)
check("V1 O_nn 单态", "n 全规范单态（y=0、C₂=0），O_nn 对角 γ=0（对照主文 Ċ_nn=0）", v1)

# ---- V2 O_nd 复现 A.21 ----
g1_nd = diag_gamma("d", "1")
g3_nd = diag_gamma("d", "3")
v2 = (g1_nd == 0 and g3_nd == 0 and fs_sum(["n", "n", "d", "d"], "1") == -Y["d"] ** 2
      and fs_sum(["n", "n", "d", "d"], "3") == Fraction(-4, 3))
check("V2 O_nd 对角γ=0", "O_nd：场强 g₁=-y_d²/b¹=y_d²、g₃=-4/3/b³=4/3 相消，γ₁=γ₃=0（复现 A.21）",
      v2, f"γ₁={g1_nd}, γ₃={g3_nd}")

# ---- V3-V6 推广到全部 (νν)(XX)：对角 γ=0 ----
def all_zero(psi):
    """(n̄γn)(ψ̄γψ) 在 ψ 带的所有规范群上对角 γ=0。"""
    for m in ("1", "2", "3"):
        g = diag_gamma(psi, m)
        if g != 0:
            return False
    return True

v3 = all_zero("e")
check("V3 O_ne 对角γ=0", "O_ne=(n̄γn)(ēγe)：g₁ 场强 -y_e²/b=y_e² 相消 → γ=0", v3)
v4 = all_zero("u")
check("V4 O_nu 对角γ=0", "O_nu=(n̄γn)(ūγu)：g₁/g₃ 均相消 → γ=0", v4)
v5 = all_zero("l")
check("V5 O_ℓn 对角γ=0", "O_ℓn=(ℓ̄γℓ)(n̄γn)：g₂ 场强 -3/4/b=3/4、g₁ 相消 → γ=0",
      v5, f"γ₂={diag_gamma('l','2')}")
v6 = all_zero("q")
check("V6 O_nq 对角γ=0", "O_nq=(q̄γq)(n̄γn)：g₁/g₂/g₃ 全相消 → γ=0",
      v6, f"γ₂={diag_gamma('q','2')}, γ₃={diag_gamma('q','3')}")

# ---- V7 penguin 混频 O_nd→O_nu 非零（A.17/A.22）----
# b_{nu,nd}^1 = -(2/3)y_d y_u δ N_c；γ₁(nu,nd) = -2(-(2/3)y_d y_u δ N_c) = (4/3)y_d y_u N_c
g_nu_nd = -2 * (-Fraction(2, 3) * Y["d"] * Y["u"] * N_C)   # (4/3)(1/3)(-2/3)(3) = -8/9
v7 = (g_nu_nd != 0 and g_nu_nd == Fraction(-8, 9))
check("V7 penguin 混频非零", "O_nd→O_nu penguin γ₁=(4/3)y_d y_u N_c=-8/9g₁²≠0（A.22）",
      v7, f"γ₁(nu←nd)={g_nu_nd}")

# ---- V8 对 25A 的映射：6 个 ν 类矢量算符对角纯规范 ADM 全零 ----
nu_classes = {"Q_νν": ["n", "n"], "Q_νe": ["e"], "Q_νu": ["u"],
              "Q_νd": ["d"], "Q_νl": ["l"], "Q_νq": ["q"]}
v8 = all(k and all_zero(nu_classes[k][0]) for k in nu_classes)
check("V8 25A ν类映射", "25A 的 6 个 ν 类矢量算符（Q_νν,Q_νe,Q_νu,Q_νd,Q_νl,Q_νq）纯规范对角 ADM 全零；跑动经 penguin 混频", v8)

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_smneft_nu_adm.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "O_nn": {"gamma_all": "0"},
        "O_nd": {"gamma1": str(g1_nd), "gamma3": str(g3_nd)},
        "O_ne_gamma": str(diag_gamma("e", "1")),
        "O_nu_gamma": str(diag_gamma("u", "1")),
        "O_ln_gamma2": str(diag_gamma("l", "2")),
        "O_nq_gamma3": str(diag_gamma("q", "3")),
        "penguin_Ond_to_Onu": str(g_nu_nd),
        "nu_classes_zero_diag": "all",
    },
    "context": {
        "ref": "arXiv:2010.12109 A.8-A.10 场强、A.19-A.21 O_nd 对角、A.17/A.22 penguin 混频、主文 Ċ_nn=0；约定见 29A",
        "boundary": "本卷证明 (νν)(XX) 矢量算符纯规范对角 ADM=0、penguin 混频非零。算符间非 penguin 混频、完整 16×16 ADM、Yukawa 贡献、25A 标准 15 类算符 ADM 未做。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_smneft_nu_adm: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
