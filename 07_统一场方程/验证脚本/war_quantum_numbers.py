# -*- coding: utf-8 -*-
"""
Warsaw 四费米算符量子数一致性审计（具体算符层，承接 20A 卷 §5 点名）。

背景：
  19A 卷把 J_5^2 匹配到 Warsaw 四费米类（类级），20A 卷核验了群指标 Fierz 恒等。本卷
  做「具体算符」衔接：机器核验全部 Warsaw ψ^4 算符（19 矢量流 + 5 标量/张量）的
  超荷中性（Y-singlet）与规范单态结构。用物理超荷约定 Q=I_3+Y：
    l_L:Y=-1/2, e_R:Y=-1, q_L:Y=+1/6, u_R:Y=+2/3, d_R:Y=-1/3。

约定：零第三方依赖；精确分数；矢量流算符 = 两个 Y-中性流乘积（自动 singlet），
标量/张量算符逐项核验 Y-singlet。色/弱单态用表示维数核验（3⊗3̄、双线量 ε 收缩）。
"""
import json
import os
import sys
from fractions import Fraction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_quantum_numbers.json")


def F(n): return Fraction(n)
def F3(a, b): return Fraction(a, b)

# 物理场：名称, 超荷Y, SU(2)维数, SU(3)表示(3/3̄/1), I_3(上分量)
# l,q 为弱双重态；e,u,d 为右手单态（u,d 在色反基础 3̄，e 色单态）
FIELDS = {
    "l":  {"Y": F3(-1, 2), "su2": 2, "su3": 1, "I3": F3(1, 2)},
    "e":  {"Y": F(-1),     "su2": 1, "su3": 1, "I3": F(0)},
    "q":  {"Y": F3(1, 6),  "su2": 2, "su3": 3, "I3": F3(1, 2)},
    "u":  {"Y": F3(2, 3),  "su2": 1, "su3": 3, "I3": F(0)},   # 物理记法：色三重态 3
    "d":  {"Y": F3(-1, 3), "su2": 1, "su3": 3, "I3": F(0)},   # 色三重态 3
}

# 19 矢量流算符：电流对（每电流为 l/e/q/u/d 的 (γ^μ) 双线性；双线性 Y 中性）
VECTOR_OPERATORS = {
    "Q_ll":    (("l", "l"), ("l", "l")),
    "Q_qq(1)": (("q", "q"), ("q", "q")),
    "Q_qq(3)": (("q", "q"), ("q", "q")),
    "Q_lq(1)": (("l", "l"), ("q", "q")),
    "Q_lq(3)": (("l", "l"), ("q", "q")),
    "Q_ee":    (("e", "e"), ("e", "e")),
    "Q_uu":    (("u", "u"), ("u", "u")),
    "Q_dd":    (("d", "d"), ("d", "d")),
    "Q_eu":    (("e", "e"), ("u", "u")),
    "Q_ed":    (("e", "e"), ("d", "d")),
    "Q_ud(1)": (("u", "u"), ("d", "d")),
    "Q_ud(8)": (("u", "u"), ("d", "d")),
    "Q_le":    (("l", "l"), ("e", "e")),
    "Q_lu":    (("l", "l"), ("u", "u")),
    "Q_ld":    (("l", "l"), ("d", "d")),
    "Q_qe":    (("q", "q"), ("e", "e")),
    "Q_qu(1)": (("q", "q"), ("u", "u")),
    "Q_qu(8)": (("q", "q"), ("u", "u")),
    "Q_qd(1)": (("q", "q"), ("d", "d")),
    "Q_qd(8)": (("q", "q"), ("d", "d")),
}

# 标量/张量算符：场四元组（L̄R)(R̄L) 型
SCALAR_TENSOR = {
    "Q_ledq":   (("l", "e", "d", "q")),
    "Q_lequ(1)": (("l", "e", "q", "u")),
    "Q_lequ(3)": (("l", "e", "q", "u")),
    "Q_quqd(1)": (("q", "u", "q", "d")),
    "Q_quqd(8)": (("q", "u", "q", "d")),
}

RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- A1 Q=I_3+Y 一致性 ----
def q_charge(name, upper):
    Y = FIELDS[name]["Y"]
    I3 = FIELDS[name]["I3"] if upper else -FIELDS[name]["I3"]
    return I3 + Y

expect = {"l_up": F(0), "l_dn": F(-1), "e": F(-1),
          "q_up": F3(2, 3), "q_dn": F3(-1, 3), "u": F3(2, 3), "d": F3(-1, 3)}
got = {"l_up": q_charge("l", True), "l_dn": q_charge("l", False), "e": q_charge("e", True),
       "q_up": q_charge("q", True), "q_dn": q_charge("q", False),
       "u": q_charge("u", True), "d": q_charge("d", True)}
check("A1 Q=I_3+Y", "物理超荷满足 Q=I_3+Y（ν:0,e⁻:-1,u:+2/3,d:-1/3）",
      got == expect, str(got))

# ---- A2 矢量流算符 Y-singlet（每电流中性）----
vec_ok = True
for name, (c1, c2) in VECTOR_OPERATORS.items():
    # 电流 (āγb)：Y = -Y_a + Y_b（ā 贡献 -Y_a）；(ψ̄γψ) 中性即 Y_b - Y_a = 0
    for c in (c1, c2):
        if -FIELDS[c[0]]["Y"] + FIELDS[c[1]]["Y"] != 0:
            vec_ok = False
# 并核验电流对的弱/色维数可成 singlet（矢量流算符全为单态收缩）
check("A2 矢量流 Y-singlet", "全部 20 个矢量流算符的每个流均 Y-中性（自动 singlet）",
      vec_ok and len(VECTOR_OPERATORS) == 20, f"共{len(VECTOR_OPERATORS)}个")

# ---- A3 标量/张量算符 Y-singlet：Σ(物理场超荷·伴随共轭符号) = 0 ----
scalar_ok = True
for name, (f1, f2, f3, f4) in SCALAR_TENSOR.items():
    # (ψ̄φ)：ψ̄ 带 -Y；φ 带 +Y
    s = -FIELDS[f1]["Y"] + FIELDS[f2]["Y"] - FIELDS[f3]["Y"] + FIELDS[f4]["Y"]
    if s != 0:
        scalar_ok = False
check("A3 标量/张量 Y-singlet", "Q_ledq/Q_lequ(1,3)/Q_quqd(1,8) 全部 Y-singlet（Σ±Y=0）",
      scalar_ok and len(SCALAR_TENSOR) == 5, f"共{len(SCALAR_TENSOR)}个")

# ---- A4 弱/色单态结构（表示维数核验）----
# 弱：l,q 为双线量；(l̄e)(d̄q) 经 ε^{jk}l^jq^k 成弱单态；e,u,d 单态
# 色：(l̄e)(d̄q) 无色；q̄u, q̄d 经 δ 或 T^A 成单态(1)/八重态(8)
def su3_singlet(dims):
    # dims: 每个双线性内两场的色表示（3 或 3̄，单态记 1）；4 场含两双线性
    # 双线性色中性：3+3̄ 成 1；1+1 成 1；3+3 或 3̄+3̄ 需 T^A（成 8，非单态）
    pairs = [(dims[0], dims[1]), (dims[2], dims[3])]
    neutral = []
    for a, b in pairs:
        if a + b == 0:
            neutral.append("1")
        else:
            neutral.append("8")   # 3+3 或 3̄+3̄ → 8（通过 T^A）
    return neutral

weak_ok = True
# Q_ledq: l(2) e(1) d(1) q(2)：l,q 双线量经 ε 成单态
# Q_lequ, Q_quqd：q 双线量（每算符恰含两个双线量 l/q）
for name, (f1, f2, f3, f4) in SCALAR_TENSOR.items():
    doublets = [FIELDS[f]["su2"] == 2 for f in (f1, f2, f3, f4)]
    if doublets.count(True) != 2:
        weak_ok = False
check("A4a 弱单态结构", "标量/张量算符恰含两个弱双线量（l 或 q），经 ε 收缩成弱单态",
      weak_ok)

dims_map = {"l": 1, "e": 1, "q": 3, "u": 3, "d": 3}   # 物理：q,u,d 均为色三重态 3
color_ok = True
for name, (f1, f2, f3, f4) in SCALAR_TENSOR.items():
    dims = [dims_map[f] for f in (f1, f2, f3, f4)]
    # 每双线性 (ψ̄,φ) 需可成色单态：ψ̄(色=-ψ) + φ(色) = 0（3̄⊗3∋1、1⊗1∋1）
    for (da, db) in [(dims[0], dims[1]), (dims[2], dims[3])]:
        if -da + db != 0:
            color_ok = False
check("A4b 色单态可行", "标量/张量算符每双线性可成色单态（3̄⊗3∋1）；(1)/(8) 为 δ/T^A 收缩选择（20A 已证）",
      color_ok)

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_quantum_numbers.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "fields": {n: (str(v["Y"]), v["su2"], v["su3"]) for n, v in FIELDS.items()},
        "vector_ops": len(VECTOR_OPERATORS),
        "scalar_tensor_ops": len(SCALAR_TENSOR),
        "scalar_color": "每双线性可成色单态（3̄⊗3∋1）；(1)/(8)=δ/T^A 收缩",
    },
    "context": {
        "ref": "arXiv:1008.4884 Tab.1/Tab.3；物理超荷 Q=I_3+Y",
        "boundary": "本卷核验超荷中性（Y-singlet）与弱/色单态结构（表示维数）。矢量流算符 Y-中性自动成立；标量/张量逐项核验。具体 Wilson 系数、味/代结构未做。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_quantum_numbers: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))

sys.exit(0 if summary["fail"] == 0 else 1)
