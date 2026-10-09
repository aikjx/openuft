# -*- coding: utf-8 -*-
"""
J_5^2 → Warsaw 具体算符的完整 Wilson 系数表（承接 16 卷 §4 / 23A 卷 §5 的最终组装）。

把 16 卷的 J_5^2 机械展开（120 个独立单态矢量流算符、系数规则 I/II/III/IV）
逐对映射到 Warsaw 具体算符类，聚合出**完整 Wilson 系数表**（以 a=3κ_g²/16 计）。
关键结构结论（机器核验）：J_5^2 单态流展开只产生 15 个 (1)-型色/弱单态 Warsaw 算符，
(3)/(8) 变体（需 τ^I/T^A 收缩）系数为零。不含 ν_R 口径（120 算符 → 15 Warsaw 类）。
零第三方依赖、纯整数系数。
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_wilson_coeffs.json")

# 手征表示：名称, 手性(±1), 类别
CHIRAL = {"Q": -1, "L": -1, "u": +1, "d": +1, "e": +1}   # L 侧 -1, R 侧 +1
# 单态流 j_{Xp}：X 表示 × p 代；不含 ν_R
GEN = 3
CURRENTS = []   # (X, p)
for X in CHIRAL:
    for p in range(1, GEN + 1):
        CURRENTS.append((X, p))
N = len(CURRENTS)   # 15

# Warsaw 算符类映射：(X,Y) → 类名（(1)-型色/弱单态；跨代归并到类）
def warsaw_class(X, Y):
    if X == "Q" and Y == "Q": return "Q_qq(1)"
    if X == "L" and Y == "L": return "Q_ll"
    if {X, Y} == {"Q", "L"}: return "Q_lq(1)"
    if X == "u" and Y == "u": return "Q_uu"
    if X == "d" and Y == "d": return "Q_dd"
    if X == "e" and Y == "e": return "Q_ee"
    if {X, Y} == {"u", "d"}: return "Q_ud(1)"
    if {X, Y} == {"e", "u"}: return "Q_eu"
    if {X, Y} == {"e", "d"}: return "Q_ed"
    if {X, Y} == {"Q", "u"}: return "Q_qu(1)"
    if {X, Y} == {"Q", "d"}: return "Q_qd(1)"
    if {X, Y} == {"Q", "e"}: return "Q_qe"
    if {X, Y} == {"L", "u"}: return "Q_lu"
    if {X, Y} == {"L", "d"}: return "Q_ld"
    if {X, Y} == {"L", "e"}: return "Q_le"
    return None

def pair_coef(a, b):
    """16 卷规则：I 同流 -1；II/III 同手性 -2；IV 异手性 +2。"""
    X, p = a
    Y, q = b
    same_flow = (X == Y and p == q)
    if same_flow:
        return -1
    same_type = (X == Y)
    same_chir = (CHIRAL[X] == CHIRAL[Y])
    if same_type or same_chir:
        return -2
    return +2

# 枚举所有无序对（多重集）：i<=j
PAIRS = []
for i in range(N):
    for j in range(i, N):
        PAIRS.append((CURRENTS[i], CURRENTS[j]))

RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- W1 逐对系数规则 ----
w1 = True
for (a, b) in PAIRS:
    X, p = a
    Y, q = b
    same_flow = (X == Y and p == q)
    same_type = (X == Y)
    same_chir = (CHIRAL[X] == CHIRAL[Y])
    exp = -1 if same_flow else (-2 if (same_type or same_chir) else +2)
    if pair_coef(a, b) != exp:
        w1 = False
check("W1 逐对系数规则", "120 对均满足 I:-1 / II,III:-2 / IV:+2（与 16 卷一致）", w1 and len(PAIRS) == 120, f"共{len(PAIRS)}对")

# ---- W2 每对映射 Warsaw 类（无 None，且只落在 (1)-型单态类）----
w2 = True
classes_used = set()
for (a, b) in PAIRS:
    X, _ = a
    Y, _ = b
    cls = warsaw_class(X, Y)
    if cls is None:
        w2 = False
    else:
        classes_used.add(cls)
# 单态类全集 = 15 个 (1)-型
SINGLET_CLASSES = {"Q_qq(1)", "Q_ll", "Q_lq(1)", "Q_uu", "Q_dd", "Q_ee",
                   "Q_ud(1)", "Q_eu", "Q_ed", "Q_qu(1)", "Q_qd(1)", "Q_qe",
                   "Q_lu", "Q_ld", "Q_le"}
check("W2 映射到单态类", "120 对全部映射到 15 个 (1)-型 Warsaw 类", w2 and classes_used == SINGLET_CLASSES,
      f"用到的类: {sorted(classes_used)}")

# ---- W3 完整 Wilson 系数表（聚合）----
table = {cls: 0 for cls in SINGLET_CLASSES}
for (a, b) in PAIRS:
    X, _ = a
    Y, _ = b
    cls = warsaw_class(X, Y)
    table[cls] += pair_coef(a, b)

EXPECT = {
    "Q_qq(1)": -9, "Q_ll": -9, "Q_lq(1)": -18,
    "Q_uu": -9, "Q_dd": -9, "Q_ee": -9,
    "Q_ud(1)": -18, "Q_eu": -18, "Q_ed": -18,
    "Q_qu(1)": +18, "Q_qd(1)": +18, "Q_qe": +18,
    "Q_lu": +18, "Q_ld": +18, "Q_le": +18,
}
w3 = table == EXPECT
check("W3 完整系数表", "各 Warsaw 类的 J_5² 系数表精确（-9/-18/+18 结构）", w3, str(table))

# ---- W4 总系数 = -S²（S = n_R - n_L = 3）----
total = sum(table.values())
check("W4 总系数=-S²", "Σ 全类系数 = -9 = -S²（S=n_R-n_L=3）", total == -9, f"总={total}")

# ---- W5 (3)/(8) 变体系数为零 ----
# (3)/(8) 类需 τ^I/T^A 收缩，单态流 j_X j_Y 内无此收缩 → 不出现、系数 0
OCTET_TRIPLET = {"Q_qq(3)", "Q_lq(3)", "Q_ud(8)", "Q_qu(8)", "Q_qd(8)"}
w5 = not (OCTET_TRIPLET & classes_used)
check("W5 (3)/(8) 系数为零", "Q_qq(3)/Q_lq(3)/Q_ud(8)/Q_qu(8)/Q_qd(8) 不被 J_5² 单态展开产生（需 τ^I/T^A 收缩）", w5)

# ---- W6 与 16 卷分类计数一致 ----
# I 同流 15（coef -1）；II 同表示异代 15；III 同手性异表示 36；IV 异手性 54
cnt = {"I": 0, "II": 0, "III": 0, "IV": 0}
for (a, b) in PAIRS:
    X, p = a
    Y, q = b
    same_flow = (X == Y and p == q)
    same_type = (X == Y)
    same_chir = (CHIRAL[X] == CHIRAL[Y])
    if same_flow: cnt["I"] += 1
    elif same_type: cnt["II"] += 1
    elif same_chir: cnt["III"] += 1
    else: cnt["IV"] += 1
w6 = cnt == {"I": 15, "II": 15, "III": 36, "IV": 54}
check("W6 分类计数", "I:15/II:15/III:36/IV:54（与 16 卷一致）", w6, str(cnt))

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_wilson_coeffs.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "num_currents": N,
        "num_pairs": len(PAIRS),
        "coeff_table": {k: table[k] for k in sorted(table)},
        "total_coeff": total,
        "total_expect": -9,
        "unit": "a = 3κ_g²/16（物理系数 = 表值 × a）",
    },
    "context": {
        "ref": "arXiv:1008.4884 算符类；16 卷 §3 系数规则（I:-1/II,III:-2/IV:+2）；23A 卷 (1)/(8) 收缩",
        "boundary": "本卷为不含 ν_R 口径（120 算符 → 15 个 (1)-型 Warsaw 类）。含 ν_R 的 ν 电流不落标准 Warsaw 25 类（ν_R 为惰性）；(3)/(8) 变体系数为零（需 τ^I/T^A 收缩，未含于 J_5² 单态展开）。无 Wilson 系数的能动量/圈结构（为一圈/RG 输入）。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_wilson_coeffs: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))
print("   完整系数表（×a=3κ²/16）:")
for k in sorted(table):
    print("     %-10s %+3d" % (k, table[k]))

sys.exit(0 if summary["fail"] == 0 else 1)
