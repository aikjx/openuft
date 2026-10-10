# -*- coding: utf-8 -*-
"""
SMNEFT 四费米算符纯规范 ADM 复现：场强分量第一性 + 主公式复现权威条目。

按 arXiv:2010.12109 的确切约定（A.8-A.10）：a_{q,u,d}^3=-4/3、a_{q,ℓ}^2=-3/4、
a_ψ^1=-y_ψ²、a_n=0（即 a_ψ^m=-C₂_m(R)，U(1) 用 -y²，注意与 28A 物理约定 -2C₂ 差因子 2）。
用主公式 γ_ij=-2g_m²[Σ_ψ(1/2)a_ψ^m δ_ij+b_ij^m]（Eq.3.7）自含复现论文 O_nedu（A.32-A.33）
与 O_ℓnℓe（A.41-A.43）的纯规范 ADM，并核验主文 Ċ_nedu 公式（§4）与附录一致。零第三方依赖、精确分数。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_smneft_adm.json")

# WCxf/Warsaw 左旋化超荷（与 21A/22A 一致）：q,u,d,ℓ,e,n
Y = {"q": Fraction(1, 6), "u": Fraction(-2, 3), "d": Fraction(1, 3),
     "l": Fraction(-1, 2), "e": Fraction(1), "n": Fraction(0)}
C2 = {"q": {"3": Fraction(4, 3), "2": Fraction(3, 4)},
      "u": {"3": Fraction(4, 3), "2": Fraction(0)},
      "d": {"3": Fraction(4, 3), "2": Fraction(0)},
      "l": {"3": Fraction(0), "2": Fraction(3, 4)},
      "e": {"3": Fraction(0), "2": Fraction(0)},
      "n": {"3": Fraction(0), "2": Fraction(0)}}

def a_psi(psi, m):
    """论文约定 a_ψ^m：a=-C₂(R)（m=2,3）；a=-y²（m=1）；n 全零。"""
    if m in ("2", "3"):
        return -C2[psi][m]
    if m == "1":
        return -Y[psi] * Y[psi]
    return Fraction(0)

def master(fields, m, b_ii):
    """主公式 (3.7) 对角线：γ = -2g²[Σ(1/2)a_ψ δ_ij + b_ij]。"""
    s = sum(Fraction(1, 2) * a_psi(f, m) for f in fields)
    return -2 * (s + b_ii)

RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- G1 论文约定场强系数 ----
g1 = (a_psi("q", "3") == Fraction(-4, 3) and a_psi("u", "3") == Fraction(-4, 3)
      and a_psi("d", "3") == Fraction(-4, 3) and a_psi("l", "3") == Fraction(0)
      and a_psi("e", "3") == Fraction(0)
      and a_psi("q", "2") == Fraction(-3, 4) and a_psi("l", "2") == Fraction(-3, 4)
      and a_psi("u", "2") == Fraction(0) and a_psi("e", "2") == Fraction(0)
      and a_psi("e", "1") == Fraction(-1) and a_psi("n", "1") == Fraction(0))
check("G1 论文场强系数", "a_{q,u,d}³=-4/3、a_{q,ℓ}²=-3/4、a_ψ¹=-y²、a_n=0（对照 A.8-A.10）", g1)

# ---- G2 约定关系：论文 a=-C₂ 与 28A 物理 -2C₂ 差因子 2 ----
g2 = (a_psi("q", "3") * 2 == Fraction(-8, 3))
check("G2 约定差因子2", "论文 a_q³=-4/3=-C₂ 与 28A 物理场约定 -2C₂=-8/3 差因子 2（组装 ADM 须用论文约定）", g2)

# ---- G3 O_nedu 场强分量（fields=n,e,d,u）----
s_3 = sum(Fraction(1, 2) * a_psi(f, "3") for f in ["n", "e", "d", "u"])
s_1 = sum(Fraction(1, 2) * a_psi(f, "1") for f in ["n", "e", "d", "u"])
g3 = (s_3 == Fraction(-4, 3) and s_1 == Fraction(-7, 9))
check("G3 O_nedu 场强分量", "Σ½a_ψ³ = -4/3（d,u 色三重）；Σ½a_ψ¹ = -7/9（y_e=1,y_d=1/3,y_u=-2/3）",
      g3, f"g₃={s_3}, g₁={s_1}")

# ---- G4 O_nedu current-current b（论文 A.32）----
b1_nedu = Y["d"] * Y["u"] - 4 * Y["e"] * Y["u"] + Y["d"] * Y["e"]   # = 25/9
b3_nedu = Fraction(4, 3)
g4 = (b3_nedu == Fraction(4, 3) and b1_nedu == Fraction(25, 9))
check("G4 O_nedu 流-流 b", "b³=4/3、b¹=y_d y_u-4y_e y_u+y_d y_e=25/9（对照 A.32）", g4, f"b¹={b1_nedu}, b³={b3_nedu}")

# ---- G5 O_nedu 完整 ADM 复现 ----
g3_nedu = master(["n", "e", "d", "u"], "3", b3_nedu)   # = 0
g1_nedu = master(["n", "e", "d", "u"], "1", b1_nedu)   # = -4
g5 = (g3_nedu == Fraction(0) and g1_nedu == Fraction(-4))
check("G5 O_nedu ADM 复现", "γ₃_nedu=0、γ₁_nedu=-4g₁²（主公式+论文b 复现 A.33）",
      g5, f"γ₃={g3_nedu}, γ₁={g1_nedu}")

# ---- G6 主文 Ċ_nedu 与附录一致（§4 vs A.33）----
c_main = (Y["d"] - Y["u"]) ** 2 + Y["e"] * (Y["e"] + 8 * Y["u"] - 2 * Y["d"])   # = -4
g6 = (c_main == g1_nedu)
check("G6 主文=附录", "主文 Ċ_nedu=(y_d-y_u)²+y_e(y_e+8y_u-2y_d) = γ₁_nedu = -4（一致性）",
      g6, f"Ċ={c_main}, γ₁={g1_nedu}")

# ---- G7 O_ℓnℓe 完整 ADM 复现（A.41-A.43）----
b1_lnle = 4 * Y["l"] * Y["e"] - 2 * Y["l"] * Y["l"]      # = 4(-1/2)+... = -2-1/2 = -5/2
b2_lnle = Fraction(3, 2)
g1_lnle = master(["l", "n", "l", "e"], "1", b1_lnle)
g2_lnle = master(["l", "n", "l", "e"], "2", b2_lnle)
# 论文 A.43：(γ₁)=-2(-3y_ℓ²-y_e²/2+4y_ℓ y_e)，(γ₂)=-2(-3/4+3/2)=-3/2
a1_expect = -2 * (-3 * Y["l"] * Y["l"] - Y["e"] * Y["e"] / 2 + 4 * Y["l"] * Y["e"])
a2_expect = -2 * (Fraction(-3, 4) + Fraction(3, 2))
g7 = (g1_lnle == a1_expect and g2_lnle == a2_expect and g2_lnle == Fraction(-3, 2))
check("G7 O_ℓnℓe ADM 复现", "γ₁_ℓnℓe=-2(-3y_ℓ²-y_e²/2+4y_ℓy_e)=13/2、γ₂=-3/2g₂²（复现 A.43）",
      g7, f"γ₁={g1_lnle}, γ₂={g2_lnle}")

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_smneft_adm.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "a_psi_paper": {"q3": str(a_psi("q", "3")), "l2": str(a_psi("l", "2")),
                        "e1": str(a_psi("e", "1")), "n0": str(a_psi("n", "1"))},
        "O_nedu": {"fs_g3": str(s_3), "fs_g1": str(s_1), "b3": str(b3_nedu), "b1": str(b1_nedu),
                   "gamma3": str(g3_nedu), "gamma1": str(g1_nedu), "main_text_C": str(c_main)},
        "O_lnle": {"b1": str(b1_lnle), "b2": str(b2_lnle),
                   "gamma1": str(g1_lnle), "gamma2": str(g2_lnle)},
    },
    "context": {
        "ref": "arXiv:2010.12109 Eq.(3.7) 主公式、A.8-A.10 场强系数、A.32-A.33 O_nedu、A.41-A.43 O_ℓnℓe、§4 主文 Ċ",
        "convention": "论文用 a_ψ=-C₂(R)、a_ψ¹=-y²；28A 用物理场约定 -2C₂。组装完整 ADM 须用论文约定。",
        "boundary": "本卷复现论文两个代表性自混条目（场强第一性 + 主公式 + 论文 b）。非对角/算符间混频 b_ij(i≠j)、完整 16×16 ADM 组装、Yukawa 贡献（配套文献）未做。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_smneft_adm: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
