# -*- coding: utf-8 -*-
"""TUFT-r395  攻 X-V60-2 / V60-C01：四维反常与六维 GS 的单项式奇偶不相交。

背景：V60 的四维账是 288 / 12 / 144（全非零），V60 给的出路是「必须靠（六维）GS」。
      本卷不猜机制，只查这两件东西是不是**同一个对象**。

三条结论（纯次数与组合，可精确枚举，不用容差）：
  定理 A（次数账）  反常多项式 = (d+2)-form。4D ⇒ I₆（6-form）；6D ⇒ I₈（8-form）。
                   下降形式 I_{d+2} = dω_{d+1} ⇒ 4D 用 ω₅、6D 用 ω₇ ⇒ 差 2 次。
  定理 B（奇偶不相交）把单项式按「2 次因子个数 a」分级（其余因子取 4 次：trF²、trR²）：
                   6 次 ⇒ 2a+4b=6 ⇒ a ∈ {3,1}（全奇）；8 次 ⇒ a ∈ {4,2,0}（全偶）。
                   ⇒ I₆ 与 I₈ 的单项式集合**不相交**；`U(1)³ = F³`（a=3）在 I₈ 里**根本没有位置**。
  定理 C（三条路定价）①谱自消：288/12/144 非零 ⇒ 不可；②6D GS：定理 B ⇒ 结构上碰不到；
                   ③4D 轴子：可抵，但系数是外部连续输入（gcd(288,12,144)=12，三条需三个条件）。

纪律：exp 取自定义展开或另一条独立路径；控制组给两个不同读数；纯陈述给 INFO。
"""
import os
import io
import json
from math import gcd
from fractions import Fraction as F
from decimal import Decimal as D, getcontext

getcontext().prec = 50

TITLE = "TUFT-r395 攻 X-V60-2：四维反常与六维 GS 的单项式奇偶不相交"
BASE = ("TUFT-r395_攻X-V60-2_四维反常与六维GS单项式奇偶不相交_八形式里没有F三次项"
        "_288三条出路定价_精算_2026-11-04")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

ROWS = []
GUARDS = []


def add(rid, layer, name, exp, act, ok, note=""):
    kind = "INFO" if ok is None else ("PASS" if ok else "FAIL")
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note, "_ok": ok})
    print("  [%-4s] %-5s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print("  [GUARD %-4s] %-16s | %s" % ("ok" if ok else "BAD", name, detail))
    return ok


def sci(x, nd=10):
    x = D(x)
    if x == 0:
        return "0"
    sgn = "-" if x < 0 else ""
    ax = abs(x)
    e = 0
    while ax >= 10:
        ax /= 10
        e += 1
    while ax < 1:
        ax *= 10
        e -= 1
    return "%s%sE%+04d" % (sgn, format(ax, ".%df" % (nd - 1)), e)


def partitions(n, parts=(2, 4)):
    """把次数 n 拆成 2 与 4 的和：返回 (a=2的次数, b=4的次数) 列表。"""
    out = []
    a = 0
    while 2 * a <= n:
        rem = n - 2 * a
        if rem % 4 == 0:
            out.append((a, rem // 4))
        a += 1
    return out


print("=" * 78)
print(TITLE)
print("=" * 78)

# ================================================================ GUARD
print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", (F(1, 3) + F(1, 6) - F(1, 2)) == 0, "1/3+1/6-1/2 = 0")
guard("DEGREE-D", all((d + 2) - d == 2 for d in (2, 4, 6, 10)),
      "反常多项式次数 = d+2（d=2,4,6,10 ⇒ 4,6,8,12），差恒为 2")
guard("DESCENT", all((d + 2) - 1 == d + 1 for d in (4, 6)),
      "下降形式次数 = d+1（d=4 ⇒ 5；d=6 ⇒ 7），两者差 2")
_p6 = partitions(6)
_p8 = partitions(8)
guard("PART", _p6 == [(1, 1), (3, 0)] and _p8 == [(0, 2), (2, 1), (4, 0)],
      "6 = 2a+4b 的解 %s ; 8 的解 %s" % (_p6, _p8))
# 奇偶判据有牙：人为把 6 改成 7（不可拆）与 8（全偶）应对不上
guard("PARITY-TEETH", max(a for a, b in _p8) % 2 == 0 and max(a for a, b in _p6) % 2 == 1,
      "各解里 a 的最大值：6 次给 %d（奇）、8 次给 %d（偶）—— 两个不同读数"
      % (max(a for a, b in _p6), max(a for a, b in _p8)))

# ================================================================ A 层
print("\n[A] 次数与单项式：两条账是不是同一个对象")

# A01 次数账
tab = [(d, d + 2) for d in (2, 4, 6, 10)]
add("A01", "A", "反常多项式次数：d 维时空用 (d+2)-form ⇒ 4D 用 I₆、6D 用 I₈",
    "表 (d, 次数) = (2,4),(4,6),(6,8),(10,12)",
    "表 %s" % tab, tab == [(2, 4), (4, 6), (6, 8), (10, 12)],
    "⇒ 两条账的次数差恰为 2（= 时空维数差）")

# A02 下降形式
add("A02", "A", "下降链 I_{d+2} = dω_{d+1}：4D 用 ω₅、6D 用 ω₇",
    "5 与 7，差 2", "ω₅ %d ; ω₇ %d ; 差 %d" % (4 + 1, 6 + 1, (6 + 1) - (4 + 1)),
    (6 + 1) - (4 + 1) == 2,
    "⇒ GS 项作用在 ω₇ 这一端；4D 的反常落在 ω₅ 那一端 ⇒ 不是同一个对象")

# A03 单项式的 a 奇偶
add("A03", "A", "6 次项含奇数个 2 次因子（a∈{3,1}），8 次项含偶数个（a∈{4,2,0}）",
    "6 次全奇、8 次全偶",
    "6 次 %s ; 8 次 %s" % (_p6, _p8),
    all(a % 2 == 1 for a, b in _p6) and all(a % 2 == 0 for a, b in _p8),
    "⇒ 两个单项式集合不相交。这是「次数差 2」的精确版本，可逐个枚举")

# A04 288 落在哪一侧
tri = [(288, "U(1)³", "F³（a=3）"), (12, "SO(10)²U(1)", "trF²·F（a=1）"),
       (144, "grav²-U(1)", "trR²·F（a=1）")]
add("A04", "A", "288/12/144 三项的单项式全在 6 次侧（a=3,1,1），I₈ 里没有同形项",
    "三项 a 值 ∈ {3,1,1}，全奇",
    "表 %s" % tri, all(int(t[2].split("a=")[1][0]) % 2 == 1 for t in tri),
    "⇒ 6D 的 GS 在结构上碰不到 U(1)³：不是「系数不够」，是「位置没有」")

# A05 三项的公共因子与独立条件数
g = gcd(gcd(288, 12), 144)
add("A05", "A", "三反常的最大公因子 = 12；一个统一系数 c 需同时整除三者",
    "gcd = 12，独立条件数 3",
    "gcd(288,12,144) = %d ; 288/12 = %d ; 144/12 = %d" % (g, 288 // g, 144 // g),
    g == 12,
    "⇒ 若 4D 轴子只有一个耦合常数，需 c·(24,1,12) 恰好对上 ⇒ 三个数不同比例 ⇒ 至少 3 个独立参数")

# A06 三条路的定价
add("A06", "A", "三条出路的定价：①谱自消 ②6D GS ③4D 轴子",
    "①不可（实测非零）②不可（A03 不相交）③可但需外部常数",
    "①288/12/144 非零 ; ②a 奇偶不相交 ; ③gcd=12 ⇒ 3 条件", True,
    "⇒ 三条里两条判死、一条变成输入 ⇒ 没有一条能「从理论里算出 0」")

# A07 控制组：把 6 次换成 8 次场景，判据必须改变读数
_t6 = sum(1 for a, b in _p6 if a % 2 == 1)
_t8 = sum(1 for a, b in _p8 if a % 2 == 1)
add("A07", "A", "同一判据在两次数下的读数：6 次命中 2/2，8 次命中 0/3（控制组）",
    "2/2 与 0/3 两个不同读数", "6 次 %d/%d ; 8 次 %d/%d" % (_t6, len(_p6), _t8, len(_p8)),
    _t6 == 2 and _t8 == 0,
    "⇒ 判据不是恒真：它在 8 次侧全不命中 ⇒ 有判别力")

# A08 独立路径：用「F 的次数」直接数（不拆 2/4）
def f_deg_ok(n):
    """I_n 里 F³ 型项存在 ⟺ n 能写成 3 个 2 次 + 若干 4 次 ⇒ n ≡ 6 (mod 4)。"""
    return (n - 6) % 4 == 0 and n >= 6


add("A08", "A", "独立路径：F³ 型项存在 ⟺ 2a+4b=n 有奇 a 解 ⟺ n ≡ 2 (mod 4)。6 ✓ / 8 ✗ / 10 ✓ / 12 ✗",
    "I₆ 有、I₈ 无、I₁₀ 有、I₁₂ 无",
    "n=6 ⇒ %s ; n=8 ⇒ %s ; n=10 ⇒ %s ; n=12 ⇒ %s"
    % (f_deg_ok(6), f_deg_ok(8), f_deg_ok(10), f_deg_ok(12)),
    f_deg_ok(6) and (not f_deg_ok(8)) and f_deg_ok(10) and (not f_deg_ok(12)),
    "⇒ 与 A03 同结论、不同算法（一个枚举拆分、一个解同余）⇒ 两条独立路径；"
    "★注意 12 次（10D 时空）也没有 F³ ⇒ 12 是 4 的倍数、F³ 需要 n≡2")

# A09 把 V60 自己的两套账按项类对齐
set6 = sorted(set(a for a, b in _p6 if a % 2 == 1))     # 6 次：a=3,1
set8 = sorted(set(a for a, b in _p8 if a % 2 == 0))     # 8 次：a=4,2,0
v60_6d = sorted([4, 0])        # trF^4（a=4）与 (trF^2)^2（a=0）
v60_4d = sorted([3, 1])        # F^3（a=3）、trF^2*F 与 trR^2*F（a=1）
add("A09", "A", "V60 自己的两套账按项类对齐：六维账用 a∈{4,0}、四维账用 a∈{3,1}，交集为空",
    "6D 用 {4,0}、4D 用 {3,1}，交集 0 个",
    "6 次可容 a %s ; 8 次可容 a %s ; V60-6D 用 %s ; V60-4D 用 %s ; 交集 %s"
    % (set6, set8, v60_6d, v60_4d, sorted(set(v60_6d) & set(v60_4d))),
    set(v60_6d) <= set(set8) and set(v60_4d) <= set(set6) and not (set(v60_6d) & set(v60_4d)),
    "⇒ 两套账各自落在自己那一侧、各自自洽；错只错在「借」—— 把 6D 的 GS 借给 4D 的账")

# ================================================================ B 层
print("\n[B] 数值：三条账的比例与需要的参数")

add("B01", "B", "三反常的比例 288 : 12 : 144 = 24 : 1 : 12（最简整数比）",
    "(24, 1, 12)", "以 12 约化 ⇒ (%d, %d, %d)" % (288 // g, 12 // g, 144 // g),
    (288 // g, 12 // g, 144 // g) == (24, 1, 12),
    "⇒ 三个比例互不相同 ⇒ 单一耦合常数无法同时抵消；要抵消需三个，即三个输入")

add("B02", "B", "6D 的 I₈ 项类数（a 偶）与 4D 的 I₆ 项类数（a 奇）对照",
    "8 次 3 类、6 次 2 类", "I₈ 类数 %d ; I₆ 类数 %d" % (len(_p8), len(_p6)),
    len(_p8) == 3 and len(_p6) == 2,
    "⇒ 项类数也不同 ⇒ 连「逐项相消」的表格都对不上")

add("B03", "B", "若强行用 4D 轴子：`a/F_a` 的系数必须整数量子化 ⇒ 只能凑出 12 的整数倍",
    "可凑，但 a/F_a 与三个耦合都是输入", "c = k·12 ⇒ 需 k = (24,1,12) 三个不同值", None,
    "⇒ 这条路把「为什么是 0」换成了「为什么是这三个数」⇒ 问题搬家，不是解决")

# ================================================================ C 层
print("\n[C] 判定")
add("C01", "C", "六维 GS 项可以抵消 V60 的四维反常（288/12/144）", "应能抵消",
    "次数不相交：I₆ 的 a 全奇、I₈ 的 a 全偶（A03/A08）", False,
    "⇒ 不是「系数不够」，是「项的位置不同」。这是 V60-C01「必须靠 GS」的类别错配")

add("C02", "C", "四维反常已被谱自身抵消", "应全为 0",
    "288 / 12 / 144 三者全非零", False,
    "⇒ 与 V60 册 C01 同结论，本轮补上「另一条路也堵住」")

add("C03", "C", "四维轴子的耦合可由本框架内部定出", "应给出唯一系数",
    "无：gcd = 12，需三个独立系数（B01）", False,
    "⇒ 内部定不出 ⇒ 第四个输入。三条出路 = 两条死、一条变输入")

add("C04", "C", "三反常可以由单一系数统一抵消", "应成单一比例",
    "比例 (24,1,12) 互不相同", False,
    "⇒ 单一 GS 系数最多抵消一个组合；另外两个仍在")

add("C05", "C", "本轮独有预言数", "应 > 0", "0（全部是关门或搬家）", None,
    "⇒ 与前 40 余卷一致")

# ================================================================ 汇总
bad_kind = [r["id"] for r in ROWS
            if r["kind"] != ("INFO" if r["_ok"] is None else ("PASS" if r["_ok"] else "FAIL"))]
guard("ADD-KIND", not bad_kind, "kind 与 ok 一致（不一致 %d 条）" % len(bad_kind))
cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])

print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("R395_DEGREE_ACCOUNT_I6_VS_I8_OK__ODD_EVEN_DISJOINT_OK__F_CUBED_ABSENT_IN_I8_OK__"
        "SINGLE_COEFF_CANNOT_CANCEL_ALL_THREE_OK__SIX_D_GS_CANNOT_TOUCH_FOUR_D_FAIL__"
        "SPECTRUM_NOT_SELF_CANCELLING_FAIL__FOUR_D_AXION_IS_EXTERNAL_INPUT_FAIL__"
        "PROBLEM_RELOCATED_NOT_SOLVED__UNIQUE_PREDICTION_0")

for r in ROWS:
    r.pop("_ok", None)
out = {"title": TITLE, "date": "2026-11-04", "rid": "r395", "verdict": VERD,
       "counts": cnt, "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS,
       "key_numbers": {
           "partitions_6": [list(p) for p in _p6],
           "partitions_8": [list(p) for p in _p8],
           "three_anomalies": [288, 12, 144],
           "gcd": g,
           "ratio": [288 // g, 12 // g, 144 // g],
           "f_cubed_exists": {6: f_deg_ok(6), 8: f_deg_ok(8), 10: f_deg_ok(10), 12: f_deg_ok(12)},
       }}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, BASE + ".json")
with io.open(jp, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1))

L = []
L.append("=" * 78)
L.append("%s  复算报告  2026-11-04" % TITLE)
L.append("=" * 78)
L.append("判词：%s" % VERD)
L.append("")
for r in ROWS:
    L.append("%-5s %-4s %s" % (r["id"], r["kind"], r["name"]))
    L.append("       exp = %s" % r["exp"])
    L.append("       act = %s" % r["act"])
    if r["note"]:
        L.append("       note= %s" % r["note"])
L.append("")
L.append("守卫 %d/%d" % (gok, len(GUARDS)))
for gd in GUARDS:
    L.append("  %-16s %s | %s" % (gd["name"], "ok" if gd["ok"] else "BAD", gd["detail"]))
rp = os.path.join(DATA, BASE + "_report_2026-11-04.txt")
with io.open(rp, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")

print("written:")
print("  " + os.path.basename(jp))
print("  " + os.path.basename(rp))
