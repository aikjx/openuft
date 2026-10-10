# -*- coding: utf-8 -*-
"""
含 ν_R 的 J_5^2 → Warsaw+ν 扩展算符完整 Wilson 系数表（承接 24A §5「ν_R 扩展」）。

16 卷含 ν_R 口径：18 个单态流（Q,L,u,d,e,ν 各三代）× 无序对 → 171 个独立算符。
本卷把 171 对映射到扩展算符基 = 标准 15 个 (1)-型 Warsaw 类（24A，非 ν 对不变）
+ 6 个 ν 惰性类（Q_νν, Q_νe, Q_νu, Q_νd, Q_νl, Q_νq），聚合出完整系数表。
关键：总系数 = -S² = -36（S = n_R - n_L = 12 - 6 = 6）。零第三方依赖、纯整数。
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(SCRIPT_DIR, "war_wilson_coeffs_nu.json")

# 手征表示：名称, 手性(±1)。ν_R 为 R 侧惰性单态。
CHIRAL = {"Q": -1, "L": -1, "u": +1, "d": +1, "e": +1, "nu": +1}
GEN = 3
CURRENTS = []
for X in CHIRAL:
    for p in range(1, GEN + 1):
        CURRENTS.append((X, p))
N = len(CURRENTS)   # 18

# 标准 15 类（不含 ν）+ 6 个 ν 扩展类
def warsaw_class(X, Y):
    if "nu" in (X, Y):
        # ν 惰性类：νν / νe / νu / νd / νl / νq
        if X == Y: return "Q_nunu"
        other = X if X != "nu" else Y
        if other == "e": return "Q_nue"
        if other == "u": return "Q_nuu"
        if other == "d": return "Q_nud"
        if other == "L": return "Q_nul"
        if other == "Q": return "Q_nuq"
        return None
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
    X, p = a
    Y, q = b
    if X == Y and p == q:
        return -1
    if X == Y or CHIRAL[X] == CHIRAL[Y]:
        return -2
    return +2

PAIRS = []
for i in range(N):
    for j in range(i, N):
        PAIRS.append((CURRENTS[i], CURRENTS[j]))

RESULTS = []


def check(label, claim, ok, note=""):
    RESULTS.append({"label": label, "claim": claim, "status": "PASS" if ok else "FAIL", "note": note})
    return ok


# ---- N1 逐对系数规则 + 计数 ----
n1 = True
cnt = {"I": 0, "II": 0, "III": 0, "IV": 0}
for (a, b) in PAIRS:
    X, p = a
    Y, q = b
    same_flow = (X == Y and p == q)
    same_type = (X == Y)
    same_chir = (CHIRAL[X] == CHIRAL[Y])
    exp = -1 if same_flow else (-2 if (same_type or same_chir) else +2)
    if pair_coef(a, b) != exp:
        n1 = False
    if same_flow: cnt["I"] += 1
    elif same_type: cnt["II"] += 1
    elif same_chir: cnt["III"] += 1
    else: cnt["IV"] += 1
check("N1 逐对系数+计数", "171 对均满足 I:-1/II,III:-2/IV:+2；I:18/II:18/III:63/IV:72",
      n1 and len(PAIRS) == 171 and cnt == {"I": 18, "II": 18, "III": 63, "IV": 72},
      f"共{len(PAIRS)}对, {cnt}")

# ---- N2 映射到扩展算符基（15 标准 + 6 ν 类，无 None）----
n2 = True
classes_used = set()
for (a, b) in PAIRS:
    X, _ = a
    Y, _ = b
    cls = warsaw_class(X, Y)
    if cls is None:
        n2 = False
    else:
        classes_used.add(cls)
STD_CLASSES = {"Q_qq(1)", "Q_ll", "Q_lq(1)", "Q_uu", "Q_dd", "Q_ee",
               "Q_ud(1)", "Q_eu", "Q_ed", "Q_qu(1)", "Q_qd(1)", "Q_qe",
               "Q_lu", "Q_ld", "Q_le"}
NU_CLASSES = {"Q_nunu", "Q_nue", "Q_nuu", "Q_nud", "Q_nul", "Q_nuq"}
ALL_CLASSES = STD_CLASSES | NU_CLASSES
check("N2 映射扩展基", "171 对全部映射到 15 标准类 + 6 ν 类，无落空",
      n2 and classes_used == ALL_CLASSES, f"共{len(classes_used)}类")

# ---- N3 完整系数表（聚合）----
table = {cls: 0 for cls in ALL_CLASSES}
for (a, b) in PAIRS:
    X, _ = a
    Y, _ = b
    table[warsaw_class(X, Y)] += pair_coef(a, b)

# 手算期望：标准类同 24A；ν 类 Q_nunu:-9, Q_nue/nuu/nud:-18, Q_nul/nuq:+18
EXPECT = {
    "Q_qq(1)": -9, "Q_ll": -9, "Q_lq(1)": -18,
    "Q_uu": -9, "Q_dd": -9, "Q_ee": -9,
    "Q_ud(1)": -18, "Q_eu": -18, "Q_ed": -18,
    "Q_qu(1)": +18, "Q_qd(1)": +18, "Q_qe": +18,
    "Q_lu": +18, "Q_ld": +18, "Q_le": +18,
    "Q_nunu": -9, "Q_nue": -18, "Q_nuu": -18, "Q_nud": -18,
    "Q_nul": +18, "Q_nuq": +18,
}
n3 = table == EXPECT
check("N3 完整系数表", "含 ν_R 的完整系数表精确（标准 15 类 + ν 6 类）", n3, str(table))

# ---- N4 总系数 = -S² = -36 ----
total = sum(table.values())
std_total = sum(table[k] for k in STD_CLASSES)
nu_total = sum(table[k] for k in NU_CLASSES)
check("N4 总系数=-S²", "总系数 -36 = -S²（S=n_R-n_L=12-6=6）；标准部分 -9、ν 部分 -27",
      total == -36 and std_total == -9 and nu_total == -27,
      f"总={total}, 标准={std_total}, ν={nu_total}")

# ---- N5 标准类系数与 24A 一致（非 ν 对不变）----
n5 = True
STD_24A = {"Q_qq(1)": -9, "Q_ll": -9, "Q_lq(1)": -18,
           "Q_uu": -9, "Q_dd": -9, "Q_ee": -9,
           "Q_ud(1)": -18, "Q_eu": -18, "Q_ed": -18,
           "Q_qu(1)": +18, "Q_qd(1)": +18, "Q_qe": +18,
           "Q_lu": +18, "Q_ld": +18, "Q_le": +18}
for k in STD_24A:
    if table[k] != STD_24A[k]:
        n5 = False
check("N5 标准类不变", "非 ν 对的标准 15 类系数与 24A 完全一致（ν 不干扰）", n5)

summary = {"total": len(RESULTS),
           "pass": sum(1 for r in RESULTS if r["status"] == "PASS"),
           "fail": sum(1 for r in RESULTS if r["status"] == "FAIL")}
out = {
    "script": "war_wilson_coeffs_nu.py",
    "summary": summary,
    "checks": RESULTS,
    "result": {
        "num_currents": N,
        "num_pairs": len(PAIRS),
        "coeff_table": {k: table[k] for k in sorted(table)},
        "total_coeff": total,
        "std_total": std_total,
        "nu_total": nu_total,
        "unit": "a = 3κ_g²/16",
    },
    "context": {
        "ref": "16 卷含 ν_R 口径（N=18、171 算符）；24A 卷标准 15 类；ν_R 为惰性单态扩展类",
        "boundary": "ν_R 为新增惰性类（非标准 Warsaw 25 类）。标准 15 类系数与 24A 一致。无圈结构；ν_R 的动力学（质量/跷跷板）未做。",
    },
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

for r in RESULTS:
    print("  [%s] %s: %s" % (r["status"], r["label"], r["claim"]))
print("== war_wilson_coeffs_nu: total=%d PASS=%d FAIL=%d" % (summary["total"], summary["pass"], summary["fail"]))
for k in sorted(table):
    print("     %-10s %+3d" % (k, table[k]))

sys.exit(0 if summary["fail"] == 0 else 1)
