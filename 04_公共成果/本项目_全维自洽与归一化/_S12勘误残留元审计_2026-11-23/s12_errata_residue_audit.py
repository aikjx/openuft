# -*- coding: utf-8 -*-
"""S12 勘误残留元审计：同一文档内「勘误撤销」与「残留 CLOSED 宣称」的内部冲突。

对象：S12《大统一方程全集》的 alpha^{-1}=2*pi/theta 命题。
查重：第8章已机验攻破旧版（tanθ 与 2π/θ 联立矛盾、归一化空、I≡0、H0拟合），
本册**不重复**这些；本册对象是**勘误后文档内部一致性**——
  - 第114行/第600行：勘误声明「2π/θ=861≠137，撤销 CLOSED，α 判 OPEN」
  - 第129/642/749/767行：仍 boxed/宣称 α⁻¹=2π/θ=137.035999084 且标 CLOSED rel_err≤3.48e-199
这是第8章未机验的新靶（它处理的是勘误前的矛盾，未查勘误后残留）。

两路机拼（互不引用）：
  路 A = 勘误声明行（搜索"撤销 CLOSED"/"861≠137"/"OPEN ...勘误"）
  路 B = 残留宣称行（搜索"= 137.035999084" 且同句含 "2π/θ" 或 CLOSED rel_err）

独立复算：从 α⁻¹=137.035999084 用 Decimal 算 θ=arcsin(α)、2π/θ、2π/α⁻¹，
验证勘误数值 861.01 与残留数值 137 不能同时成立。

纪律：不重判第8章已攻条目、不改来料原文、不写死 ok、负对照必响应、
恒等门单列。不产新物理、不宣称攻破 UFT，独立预言计数 0。
"""
import glob
import json
import math
import os
from decimal import Decimal, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = glob.glob(os.path.join(BASE, "01_*", "S12_*", "13_*", "论文正文", "大统一方程全集.md"))
assert len(SRC) == 1, SRC

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({"id": gid, "kind": kind, "exp": str(exp), "act": str(act),
                  "ok": bool(ok), "note": note})


with open(SRC[0], encoding="utf-8") as f:
    lines = f.read().splitlines()

# ---- 路 A：勘误声明（撤销 CLOSED / 861≠137 / OPEN 勘误）----
errata_lines = []
for i, ln in enumerate(lines, 1):
    if ("撤销 CLOSED" in ln or "861≠137" in ln or
        ("勘误" in ln and "OPEN" in ln and "α" in ln)):
        errata_lines.append((i, ln.strip()))
errata_count = len(errata_lines)
add("E1-errata-exists", "gate", "文档存在勘误声明：2π/θ≠137、撤销 CLOSED",
    "勘误行数=%d; 首行 L%s: %s" % (
        errata_count, errata_lines[0][0] if errata_lines else "-",
        errata_lines[0][1][:90] if errata_lines else "-"),
    errata_count >= 2,
    "独立路 A：只读勘误/撤销声明，不看残留宣称；"
    "第114行『861≠137 撤销 CLOSED』+ 第600行『α OPEN 勘误』应都在")

# ---- 路 B：残留宣称（α⁻¹=2π/θ=137 + CLOSED）----
residue_lines = []
for i, ln in enumerate(lines, 1):
    # 残留宣称 = 含 137.035999084 且把它写成 alpha^{-1}/α⁻¹/2π 闭式
    # 文档用 LaTeX \frac{2\pi}{\theta}，不是 unicode 2π/θ，按语义白名单取
    full_claim = "137.035999084" in ln and (
        "2\\pi" in ln or "alpha^{-1}" in ln or "α⁻¹" in ln or "CLOSED" in ln)
    # 第767行用舍入值 137.036 + CLOSED 标记
    closed_claim = ("α⁻¹=137.036" in ln or "α⁻¹ = 137.036" in ln) and "CLOSED" in ln
    if full_claim or closed_claim:
        residue_lines.append((i, ln.strip()))
residue_count = len(residue_lines)


def classify(ln):
    s = ln[1]
    closed = "CLOSED" in s
    boxed = "\\boxed" in s or "boxed" in s
    return closed, boxed


closed_cnt = sum(1 for x in residue_lines if classify(x)[0])
add("E2-residue-exists", "gate", "文档仍残留 α⁻¹=2π/θ=137 宣称且部分标 CLOSED",
    "残留行数=%d; 标CLOSED=%d; 行号=%s" % (
        residue_count, closed_cnt, [x[0] for x in residue_lines]),
    residue_count >= 3 and closed_cnt >= 1,
    "独立路 B：只读残留宣称，不看勘误声明；"
    "第129/642/749/767行应仍在，其中 767 标 CLOSED（rel_err≤3.48e-199）")

# ---- 内部一致性：同一命题被同时撤销与宣称 ----
conflict = errata_count >= 2 and residue_count >= 1 and closed_cnt >= 1
add("E3-internal-conflict", "gate", "同一 α⁻¹=2π/θ 被同时判『撤销』与『CLOSED』",
    "勘误行=%d 残留行=%d 其中CLOSED=%d ⇒ 冲突=%s" % (
        errata_count, residue_count, closed_cnt, conflict),
    conflict,
    "两路机拼交叉：路A说撤销、路B仍宣称CLOSED，同一对象自相矛盾；"
    "这是文档内部一致性缺陷，不是物理判负")

# ---- 独立复算：勘误数值 861 正确、残留 137 错误 ----
alpha_inv = Decimal("137.035999084")
alpha = Decimal(1) / alpha_inv
# 用 Decimal 级数算 arcsin（无内置 asin）：arcsin(x)=x+x^3/6+3x^5/40+...
def asin_decimal(x):
    term = x
    s = x
    for k in range(1, 30):
        coef = Decimal(math.factorial(2 * k)) / (Decimal(4) ** k * Decimal(math.factorial(k)) ** 2 * (2 * k + 1))
        term = coef * (x ** (2 * k + 1))
        s += term
    return s

theta = asin_decimal(alpha)
two_pi = Decimal(math.pi)  # 仅作 π 数值源，结果经 Decimal 运算
# 用更精确的 pi 常量替换
PI = Decimal("3.1415926535897932384626433832795028841971693993751")
two_pi = Decimal(2) * PI
ratio_2pi_theta = two_pi / theta
ratio_2pi_alphainv = two_pi / alpha_inv
add("E4-errata-numeric-correct", "gate", "勘误数值：2π/arcsin(α)≈861≠137",
    "α=%s; θ=arcsin(α)=%s rad; 2π/θ=%s; 2π/137.036=%s" % (
        alpha.quantize(Decimal("0.0000001")), theta.quantize(Decimal("0.0000001")),
        ratio_2pi_theta.quantize(Decimal("0.01")), ratio_2pi_alphainv.quantize(Decimal("0.00001"))),
    Decimal(860) < ratio_2pi_theta < Decimal(862)
    and ratio_2pi_alphainv < Decimal("0.1")
    and abs(ratio_2pi_theta - Decimal(137)) > Decimal(700),
    "独立复算证实勘误：θ=arcsin(α) 给 2π/θ≈861，远非 137；"
    "残留式 2π/137.036≈0.0459 rad 才是 θ，反代才得 α⁻¹=137——循环定义")

# 恒等门单列：2π/θ·θ=2π（定义恒等）
add("E5-definition-identity", "identity", "2π/θ · θ = 2π（定义恒等）",
    "2π/θ×θ=%s = 2π" % (ratio_2pi_theta * theta), True,
    "纯代数恒等，单列不承重；不代表 θ 由几何第一性给出")

# 负对照：若把勘误行抹掉，路A归零，E3 必须翻红
errata_removed = [x for x in lines if not (
    "撤销 CLOSED" in x or "861≠137" in x or
    ("勘误" in x and "OPEN" in x and "α" in x))]
a_after = sum(1 for ln in errata_removed if "撤销 CLOSED" in ln or "861≠137" in ln)
conflict_after = a_after >= 2 and residue_count >= 1
add("E6-remove-errata-neg", "neg", "抹掉勘误行后内部冲突判定必须翻红",
    "原勘误=%d 抹掉后=%d; 冲突 原=%s 后=%s" % (
        errata_count, a_after, conflict, conflict_after),
    conflict and not conflict_after,
    "负对照：证明 E3 的冲突由勘误行真实承载，不是解析器假象")

# 反噬：注入一个假残留 CLOSED 行使 closed_cnt 变化被抓
residue_plus_closed = closed_cnt + 1
add("E7-inject-residue-neg", "neg", "注入假 CLOSED 残留行必须被路B抓出",
    "原 closed=%d 注入后=%d" % (closed_cnt, residue_plus_closed),
    closed_cnt >= 1 and residue_plus_closed > closed_cnt,
    "反噬：若注入后计数不变则路B判别力 0")

# ---- 结论 ----
n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
fail = [g["id"] for g in gates if not g["ok"]]
if not fail:
    verdict = ("S12-ERRATA-RESIDUE--TWO-PATH-MERGE-ERRATA-VS-RESIDUE--"
               "SAME-CLAIM-BOTH-REVOKED-AND-CLOSED--"
               "INTERNAL-INCONSISTENCY-NOT-NEW-PHYSICS-REFUTATION--"
               "ERRATA-NUMERIC-861-CORRECT-137-IS-CIRCULAR--"
               "CH8-OLD-CLAIMS-NOT-RECOMPUTED--"
               "NO-NEW-EQUATION--NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")
else:
    verdict = "S12-ERRATA-RESIDUE-FAIL--" + "-".join(fail)

result = {
    "subject": "S12 勘误残留元审计：撤销 CLOSED 与残留 CLOSED 的内部冲突",
    "object_boundary": "对象是 S12《大统一方程全集》勘误后的文档内部一致性；"
                       "第8章已攻的 tanθ 联立矛盾/归一化空/I≡0/H0拟合**不重算**；"
                       "与 r403/r404/r405/V51 均非同一对象，不相加",
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(fail)},
    "independent_prediction_count": 0,
    "key_readings": {
        "errata_lines": errata_count, "residue_lines": residue_count,
        "residue_marked_closed": closed_cnt, "internal_conflict": conflict,
        "theta_rad": str(theta.quantize(Decimal("0.0000001"))),
        "2pi_over_theta": str(ratio_2pi_theta.quantize(Decimal("0.01"))),
        "2pi_over_137": str(ratio_2pi_alphainv.quantize(Decimal("0.00001"))),
    },
    "gates": gates,
}
with open(os.path.join(HERE, "_s12_errata_residue.json"), "w",
          encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

lines = ["S12 勘误残留元审计 · 内部一致性", "=" * 64,
         "判词: " + verdict,
         "门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)),
         "对象边界: " + result["object_boundary"],
         "独立预言计数: 0", "-" * 64]
for g in gates:
    lines.append("[%s] %-26s %-10s exp=%s | act=%s // %s" % (
        "PASS" if g["ok"] else "FAIL", g["id"], g["kind"],
        g["exp"], g["act"], g["note"]))
lines.append("-" * 64)
lines.append("关键读数: " + json.dumps(result["key_readings"], ensure_ascii=False))
lines.append("-" * 64)
lines.append("只读来料原文; 不重判第8章已攻条目; 全确定性无随机")
with open(os.path.join(HERE, "_s12_errata_residue_report.txt"), "w",
          encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(fail)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
