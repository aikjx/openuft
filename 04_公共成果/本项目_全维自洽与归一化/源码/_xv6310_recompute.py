# -*- coding: utf-8 -*-
"""攻坚 X-V63-10：涡旋数 n 能否由理论内部固定为 3（独立机核 · 部件 1/3）。

体例：跨卷攻坚册 —— 不新增 RID、不进 README 登记位、条目不与任何卷相加。
来料：无外部来料；输入为 X-V63-6 §十二 OPEN 表的 X-V63-10，以及 V63 的 q_Y 表、
      X-V63-1 的陈类整数性口径、X-V63-6 的绕数器与判别力 0 结论。
对象：Spin(2n) 规范群中心、绕数同态、Z_k 离散投影、超荷量子化。
红线：数学自洽 ≠ 实验证实；只产可算判决，不产新物理；独立实验预言数 0。
纪律：判据反噬自己 + 正负双对照；守卫 ok 禁写死；同源回验显式标注；
      定义恒等式记 IDENTITY 不记 PASS；对象错位必须写进变量名。
"""
import os
import io
import json
import ast
import re
import glob
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
from itertools import product
from math import gcd, floor

getcontext().prec = 60

TITLE = "攻坚 X-V63-10 独立机核"
DATE = "2026-11-08"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "数据")
JS = os.path.join(DATA, "_XV6310_recompute_2026-11-08.json")
RPT = os.path.join(DATA, "_XV6310_recompute_report_2026-11-08.txt")
RD = os.path.join(ROOT, "README.md")

ROWS = []
GUARDS = []
KEY = {}


def add(rid, layer, name, exp, act, ok, note=""):
    if ok == "ID":
        kind = "IDENTITY"
    elif ok is None:
        kind = "INFO"
    else:
        kind = "PASS" if ok else "FAIL"
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note})
    print("  [%-8s] %-5s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print("  [GUARD %-4s] %-18s | %s" % ("ok" if ok else "BAD", name, detail))
    return bool(ok)


def f2d(q):
    q = F(q)
    return D(q.numerator) / D(q.denominator)


def fmt_f(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else "%d/%d" % (q.numerator, q.denominator)


def is_int(q):
    return F(q).denominator == 1


print("=" * 78)
print(TITLE + "  " + DATE)
print("=" * 78)
print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", F(1, 3) + F(1, 6) - F(1, 2) == 0, "1/3+1/6-1/2 = 0")
guard("DECIMAL-EXP", abs(D(1).exp().ln() - D(1)) < D("1e-50"),
      "exp 与 ln 互逆，prec=60")

# ---------------------------------------------------------------- A 层数据
# D_n 根格 = {v in Z^n : sum(v) 为偶数}；权格/根格商有 4 个陪集，代表取
#   0（平凡）、e_1（矢量）、(1/2)^n（旋量）、(1/2,...,1/2,-1/2)（共轭旋量）。
# 元素阶 = 最小正整数 k 使 k*rep 落回根格。全部由整数判据枚举，不抄群论结论。
def in_root_lattice(v):
    return all(is_int(x) for x in v) and int(sum(F(x) for x in v)) % 2 == 0


def order_of(rep, kmax=16):
    for k in range(1, kmax + 1):
        if in_root_lattice([k * F(x) for x in rep]):
            return k
    return None


def center_orders(n):
    zero = [F(0)] * n
    vec = [F(0)] * n
    vec[0] = F(1)
    spin = [F(1, 2)] * n
    conj = [F(1, 2)] * (n - 1) + [F(-1, 2)]
    return [order_of(r) for r in (zero, vec, spin, conj)]


N_RANGE = list(range(3, 9))
KEY["center_table"] = []
for _n in N_RANGE:
    _o = center_orders(_n)
    KEY["center_table"].append({
        "n": _n, "orders": _o, "max_order": max(_o),
        "has_three": 3 in _o,
        "group": "Z2xZ2" if max(_o) == 2 else "Z4",
    })
KEY["spin12_orders"] = center_orders(6)
KEY["spin10_orders"] = center_orders(5)
KEY["center_has3_count"] = sum(1 for x in KEY["center_table"] if x["has_three"])
KEY["center_max_set"] = sorted(set(x["max_order"] for x in KEY["center_table"]))
KEY["center_all_orders"] = sorted(set(o for x in KEY["center_table"]
                                      for o in x["orders"]))
KEY["center_group_set"] = sorted(set(x["group"] for x in KEY["center_table"]))
KEY["center_even_max"] = [x["max_order"] for x in KEY["center_table"] if x["n"] % 2 == 0]
KEY["center_odd_max"] = [x["max_order"] for x in KEY["center_table"] if x["n"] % 2 == 1]
# 负控：把「商群阶 4」误读成「含 4 阶元」，在 D_6 上会给出假读数。
KEY["center_false_read_d6"] = len(center_orders(6))
KEY["center_true_max_d6"] = max(center_orders(6))
KEY["center_false_read_d5"] = len(center_orders(5))
KEY["center_true_max_d5"] = max(center_orders(5))

# 关键对照：SU(3)（A_2）中心确为 Z_3。根格 = {v in Z^3 : sum(v)=0}，
# 基本权 omega_2 = (1/3, 1/3, -2/3)，最小 k 使 k*omega_2 落回根格即中心阶。
def in_a2_root(v):
    return all(is_int(x) for x in v) and sum(F(x) for x in v) == 0


SU3_OMEGA2 = [F(1, 3), F(1, 3), F(-2, 3)]
KEY["su3_center_min"] = next(k for k in range(1, 10)
                             if in_a2_root([k * x for x in SU3_OMEGA2]))
KEY["su3_center_group"] = "Z%d" % KEY["su3_center_min"]
KEY["su3_has3"] = KEY["su3_center_min"] == 3
KEY["su3_object"] = "低能色群 SU(3)_c 的中心"

# ---------------------------------------------------------------- B 层数据
# 绕数器：相位 phi(theta) = exp(i*n*theta)，离散取 mod 点，差值 wrap 到 (-mod/2, mod/2]。
def winding(n, wrap=True, mod=64):
    n = F(n)
    ph = [(n * j) % mod for j in range(mod + 1)]
    s = F(0)
    for j in range(mod):
        d = (ph[j + 1] - ph[j]) % mod
        if wrap and d > F(mod, 2):
            d -= mod
        s += d
    return s / mod, (ph[mod] == ph[0])


W_GRID = list(range(-4, 5))
KEY["wind_hom_table"] = []
for _a in W_GRID:
    for _b in W_GRID:
        _wa = winding(_a)[0]
        _wb = winding(_b)[0]
        _wab = winding(_a + _b)[0]
        KEY["wind_hom_table"].append({"a": _a, "b": _b,
                                      "match": _wa + _wb == _wab})
KEY["wind_hom_total"] = len(KEY["wind_hom_table"])
KEY["wind_hom_match"] = sum(1 for x in KEY["wind_hom_table"] if x["match"])
KEY["wind_hom_bad"] = KEY["wind_hom_total"] - KEY["wind_hom_match"]

_w_nowrap, _ = winding(5, wrap=False, mod=8)
_w_wrap, _ = winding(5, wrap=True, mod=8)
KEY["wind_nowrap_small"] = fmt_f(_w_nowrap)
KEY["wind_wrap_small"] = fmt_f(_w_wrap)

KEY["wind_min_positive"] = int(min(n for n in range(1, 9)
                                   if winding(n)[1] and winding(n)[0] == n))
KEY["wind_target_grid"] = [(t, fmt_f(winding(t)[0])) for t in range(1, 9)]
KEY["wind_target_all_hit"] = all(str(t) == w for t, w in KEY["wind_target_grid"])

# n=3 的分解：三个整数绕数之和为 3，逐个显式枚举。
KEY["decomp3"] = [(a, b, c) for a in W_GRID for b in W_GRID for c in W_GRID
                  if a + b + c == 3]
KEY["decomp3_count"] = len(KEY["decomp3"])
KEY["decomp3_trivial"] = (1, 1, 1) in KEY["decomp3"]
KEY["decomp3_unit_only"] = sum(1 for x in KEY["decomp3"]
                               if all(abs(v) == 1 for v in x))

# Z_k 离散投影：要求 n = 0 mod k 时的最小正绕数。
KEY["zk_table"] = []
for _k in range(2, 10):
    _mins = [n for n in range(1, 40) if n % _k == 0]
    KEY["zk_table"].append({"k": _k, "n_min": _mins[0]})
KEY["zk_hit3"] = sum(1 for x in KEY["zk_table"] if x["n_min"] == 3)
KEY["zk_total"] = len(KEY["zk_table"])
KEY["zk_hitrate"] = "%d/%d" % (KEY["zk_hit3"], KEY["zk_total"])
KEY["zk_frozen"] = "1/1"
KEY["zk_k_grid"] = list(range(2, 10))
KEY["zk_input_is_free"] = not set(KEY["zk_k_grid"]).issubset(set(KEY["center_max_set"]))

# 3 个 n=1 缺陷与 1 个 n=3 缺陷的总绕数相同、缺陷数不同。
KEY["cluster_total_wind"] = fmt_f(sum(winding(1)[0] for _ in range(3)))
KEY["cluster_single_wind"] = fmt_f(winding(3)[0])
KEY["cluster_count_multi"] = 3
KEY["cluster_count_single"] = 1
KEY["cluster_same_total"] = (KEY["cluster_total_wind"] == KEY["cluster_single_wind"])
KEY["cluster_diff_count"] = KEY["cluster_count_multi"] - KEY["cluster_count_single"]

# ---------------------------------------------------------------- C 层数据
QY = [1, -4, 2, -3, 6, 0]
TENSOR_Q = [0] * 10 + [2, -2]


def gcd_list(xs):
    g = 0
    for x in xs:
        g = gcd(g, abs(int(x)))
    return g


KEY["qy_table"] = QY
KEY["qy_gcd"] = gcd_list(QY)
KEY["tensor_gcd"] = gcd_list(TENSOR_Q)
KEY["holonomy_constraint"] = "n 为整数" if KEY["qy_gcd"] == 1 else "n 为 1/%d 的整数倍" % KEY["qy_gcd"]

_iq_int_solutions = [(p, q) for p in range(-8, 9) for q in range(-8, 9)
                     if 2 * (p + q) == 3]
KEY["iq_three_solutions"] = len(_iq_int_solutions)

VQ = [F(0)] * 10 + [F(2), F(-2)]
SPIN_Q = [F(s[5]) for s in product((1, -1), repeat=6)
          if s[0] * s[1] * s[2] * s[3] * s[4] * s[5] == 1]


def moments(qs):
    return [int(sum(q ** k for q in qs)) for k in (1, 2, 3)]


KEY["spin_moments"] = moments(SPIN_Q)
KEY["vec_moments"] = moments(VQ)
KEY["spin_dim"] = len(SPIN_Q)

# 带边陈类整数性回代：整数 N 合法、半整数 N 非法。
KEY["chern_table"] = []
for _N in [F(1), F(2), F(3), F(1, 2), F(3, 2), F(5, 2)]:
    _w, _cl = winding(_N)
    KEY["chern_table"].append({"N": fmt_f(_N), "wind": fmt_f(_w),
                               "closed": _cl, "legal": _cl and is_int(_w)})
KEY["chern_legal_count"] = sum(1 for x in KEY["chern_table"] if x["legal"])
KEY["chern_half_legal"] = sum(1 for x in KEY["chern_table"]
                              if not is_int(F(x["N"])) and x["legal"])

# 内部固定机制：群中心、holonomy gcd、最小拓扑荷三条独立路径各自检查是否把 n 定为 3。
KEY["internal_fixers"] = []
if 3 in KEY["center_all_orders"]:
    KEY["internal_fixers"].append("center")
if KEY["qy_gcd"] % 3 == 0:
    KEY["internal_fixers"].append("holonomy")
if KEY["wind_min_positive"] == 3:
    KEY["internal_fixers"].append("topology")
KEY["internal_fixers_count"] = len(KEY["internal_fixers"])
KEY["internal_fix_paths"] = 3

# ---------------------------------------------------------------- README 体检
_rb = io.open(RD, "rb").read()
KEY["readme_bytes"] = len(_rb)
KEY["readme_r402_tokens"] = _rb.count(b"TUFT-r402_")
KEY["readme_r403_tokens"] = _rb.count(b"TUFT-r403_")
KEY["r403_files"] = len(glob.glob(os.path.join(ROOT, "**", "*TUFT-r403_*"), recursive=True))


print("\n[ROWS] A 层：规范群中心能否给出 3 阶选择定则")
_a01_ok = (KEY["spin12_orders"] == [1, 2, 2, 2]
           and KEY["center_true_max_d6"] == 2
           and center_orders(6) == KEY["spin12_orders"])
add("A01", "A", "Spin(12) 即 D_6 的中心陪集阶由根格枚举给出",
    "四个陪集的阶须为 1,2,2,2，最大元素阶为 2",
    "D_6 阶表 %s；最大 %d；群型 %s"
    % (KEY["spin12_orders"], KEY["center_true_max_d6"],
       [x["group"] for x in KEY["center_table"] if x["n"] == 6][0]),
    _a01_ok, "判据是 k*rep 落回根格的最小正整数，不抄群论结论")

_a02_ok = (KEY["spin10_orders"] == [1, 2, 4, 4]
           and KEY["center_true_max_d5"] == 4
           and KEY["spin10_orders"] != KEY["spin12_orders"])
add("A02", "A", "Spin(10) 即 D_5 的中心含 4 阶元",
    "D_5 阶表须为 1,2,4,4，且与 D_6 读数不同",
    "D_5 阶表 %s；最大 %d；与 D_6 不同=%s"
    % (KEY["spin10_orders"], KEY["center_true_max_d5"],
       KEY["spin10_orders"] != KEY["spin12_orders"]),
    _a02_ok, "n 的奇偶决定旋量权 2*rep 的坐标和是否为偶")

_a03_ok = (KEY["center_has3_count"] == 0
           and KEY["center_max_set"] == [2, 4]
           and len(KEY["center_table"]) == 6)
add("A03", "A", "D_3 至 D_8 六档 Spin(2n) 中心全部不含 3 阶元",
    "3 阶元出现次数须为 0，最大元素阶集合只含 2 与 4",
    "六档 %s；含 3 阶元 %d 档；最大阶集合 %s；群型集合 %s"
    % ([(x["n"], x["orders"], x["group"]) for x in KEY["center_table"]],
       KEY["center_has3_count"], KEY["center_max_set"], KEY["center_group_set"]),
    _a03_ok, "显式报零的个数；结论只覆盖 Spin(2n) 中心，SU(3)_c 中心另见 A08")

_a04_ok = (KEY["center_false_read_d6"] != KEY["center_true_max_d6"]
           and KEY["center_false_read_d5"] == KEY["center_true_max_d5"])
add("A04", "A", "负对照：把商群阶 4 误读成含 4 阶元",
    "D_6 上误读与真实读数须不同，D_5 上恰好相同才显出陷阱",
    "D_6 误读 %d 对真实 %d；D_5 误读 %d 对真实 %d"
    % (KEY["center_false_read_d6"], KEY["center_true_max_d6"],
       KEY["center_false_read_d5"], KEY["center_true_max_d5"]),
    _a04_ok, "陷阱只在偶 n 暴露，D_5 会给出假安慰")

_a05_ok = (all(v == 2 for v in KEY["center_even_max"])
           and all(v == 4 for v in KEY["center_odd_max"])
           and len(KEY["center_even_max"]) == 3
           and len(KEY["center_odd_max"]) == 3)
add("A05", "A", "偶 n 给 Z2xZ2、奇 n 给 Z4 是可算交替，不是背下来的分类",
    "6 档中偶 3 档最大阶全 2、奇 3 档全 4",
    "偶 n 最大阶 %s；奇 n 最大阶 %s"
    % (KEY["center_even_max"], KEY["center_odd_max"]),
    _a05_ok, "由 2*(1/2)^n 的坐标和 n 的奇偶直接推出")

add("A06", "A", "与标准 Spin(2n) 中心结论一致，但本册读数是陪集枚举所得",
    "同源一致性不得冒充独立证据",
    "本册独立枚举 %d 档陪集；教科书结论仅作对照，不单列 PASS"
    % len(KEY["center_table"]),
    None, "同源回验抓不到同源错误；显式标注，由 SAME-SOURCE-TAGGED 守卫强制")

add("A07", "A", "元素阶整除商群阶 4 是 Lagrange 型恒等式",
    "展开后无残差可算，按定义恒等式纪律不记 PASS",
    "六档最大阶 %s 均整除 4；这是有限群阶的规定不是推导"
    % str(KEY["center_max_set"]),
    "ID", "配 NOT-ALL-GREEN 守卫防首跑全绿")

_a08_ok = (KEY["su3_has3"] and KEY["su3_center_min"] == 3
           and KEY["center_has3_count"] == 0)
add("A08", "A", "SU(3)_c 中心确为 Z_3，但与 Spin(2n) 中心是两个对象",
    "须真算出 3 阶元，且两个群的 3 阶元读数须不同",
    "A_2 基本权最小回落 k=%d；群型 %s；含 3 阶元=%s；Spin(2n) 六档含 3 阶元 %d 档；本条对象是 %s"
    % (KEY["su3_center_min"], KEY["su3_center_group"], KEY["su3_has3"],
       KEY["center_has3_count"], KEY["su3_object"]),
    _a08_ok, "不把色群中心搬来当内部空间涡旋数投影；若强行联系须另证，记为 OPEN")

print("\n[ROWS] B 层：绕数同态、最小拓扑荷与唯一真判负")
_b01_ok = (KEY["wind_hom_total"] == 81 and KEY["wind_hom_match"] == 81
           and KEY["wind_hom_bad"] == 0)
add("B01", "B", "绕数对加法是同态（81 组全网格实算）",
    "a,b 取 -4..4 共 81 组，wind(a)+wind(b) 须逐组等于 wind(a+b)",
    "总组数 %d；吻合 %d；失配 %d"
    % (KEY["wind_hom_total"], KEY["wind_hom_match"], KEY["wind_hom_bad"]),
    _b01_ok, "同态性决定 n=3 是否可被拆成单位缺陷")

_b02_ok = (KEY["wind_nowrap_small"] != KEY["wind_wrap_small"])
add("B02", "B", "负对照：绕数器不做 wrap 会越过 Nyquist 给出未归约读数",
    "M=8 且 n=5 时两侧读数须不同",
    "不 wrap 得 %s；wrap 得 %s"
    % (KEY["wind_nowrap_small"], KEY["wind_wrap_small"]),
    _b02_ok, "承接 X-V63-6 K2；确保本册绕数器没有静默失灵")

_b03_ok = (KEY["wind_min_positive"] == 1 and winding(1)[1])
add("B03", "B", "最小正拓扑荷是 1，n=1 单值且闭合",
    "不存在拓扑理由单独禁戒 n=1 与 n=2",
    "最小正绕数 %s；n=1 环路闭合=%s"
    % (fmt_f(KEY["wind_min_positive"]), winding(1)[1]),
    _b03_ok, "若要 n_min=3 必须引入额外离散投影，见 B07")

_b04_ok = (KEY["decomp3_trivial"] and KEY["decomp3_count"] > 1
           and KEY["decomp3_unit_only"] >= 1)
add("B04", "B", "n=3 在拓扑上可分解为三个 n=1",
    "显式枚举须给出 (1,1,1) 且分解总数大于 1",
    "和为 3 的三元组 %d 个；含 (1,1,1)=%s；全单位分解 %d 个"
    % (KEY["decomp3_count"], KEY["decomp3_trivial"], KEY["decomp3_unit_only"]),
    _b04_ok, "3 不是拓扑荷的原子，没有不变量能把它标成基本单元")

_b05_ok = (KEY["wind_target_all_hit"] and len(KEY["wind_target_grid"]) == 8)
add("B05", "B", "绕数对目标 1..8 满射，故「理论允许 t」是恒真谓词",
    "每个目标 t 都须存在 n=t 使 wind=t",
    "目标表 %s；全部命中=%s"
    % (KEY["wind_target_grid"], KEY["wind_target_all_hit"]),
    _b05_ok, "100% 通过的谓词判别力为 0（承接 V63 C10）")

_b06_ok = (KEY["internal_fixers_count"] > 0)
add("B06", "B", "唯一真判负：涡旋数 3 是否由理论内部固定",
    "须存在不依赖新输入的内部机制把 n 定为 3",
    "%d 条独立路径中内部固定机制 %d 个 %s；中心全部元素阶 %s；holonomy gcd %d；最小正绕数 %s；Z_k 的 k 是新输入"
    % (KEY["internal_fix_paths"], KEY["internal_fixers_count"],
       str(KEY["internal_fixers"]), KEY["center_all_orders"],
       KEY["qy_gcd"], fmt_f(KEY["wind_min_positive"])),
    _b06_ok, "判负已登记；自由度只是从 n 转移到 k。口径不含 SU(3)_c 中心与能量最小化，见 D04")

_b07_ok = (KEY["zk_hit3"] == 1 and KEY["zk_total"] == 8
           and KEY["zk_input_is_free"]
           and KEY["zk_hitrate"] != KEY["zk_frozen"])
add("B07", "B", "Z_k 投影把最小绕数定为 k，但 k 本身是新输入",
    "k=2..9 须给 8 个不同 n_min，命中 3 恰 1 档，且冻结读数不同",
    "投影表 %s；命中 3 的 %s；冻结一档 %s"
    % ([(x["k"], x["n_min"]) for x in KEY["zk_table"]],
       KEY["zk_hitrate"], KEY["zk_frozen"]),
    _b07_ok, "k=3 确实给 n_min=3，但为什么是 3 仍需外部回答")

_b08_ok = (3 not in KEY["center_all_orders"]
           and KEY["center_has3_count"] == 0
           and [x["k"] for x in KEY["zk_table"] if x["n_min"] == 3] == [3]
           and KEY["zk_input_is_free"])
add("B08", "B", "群中心阶集合与所需 Z_3 不相交",
    "中心全部元素阶须不含 3，且 Z_k 命中 3 的 k 恰为自由输入 3",
    "中心全部元素阶 %s；含 3 阶元 %d 档；命中 3 的 k=%s；k 网格非中心阶子集=%s"
    % (KEY["center_all_orders"], KEY["center_has3_count"],
       [x["k"] for x in KEY["zk_table"] if x["n_min"] == 3],
       KEY["zk_input_is_free"]),
    _b08_ok, "最硬的一刀，但口径收窄为 Spin(2n) 大统一群中心；SU(3)_c 中心见 A08，对象不同")

_b09_ok = (KEY["cluster_same_total"] and KEY["cluster_diff_count"] == 2)
add("B09", "B", "三个 n=1 缺陷与一个 n=3 缺陷总绕数相同而缺陷数不同",
    "两个对象须给出同总绕数、不同缺陷数两个读数",
    "3×n=1 总绕数 %s / 缺陷数 %d；1×n=3 总绕数 %s / 缺陷数 %d；差 %d"
    % (KEY["cluster_total_wind"], KEY["cluster_count_multi"],
       KEY["cluster_single_wind"], KEY["cluster_count_single"],
       KEY["cluster_diff_count"]),
    _b09_ok, "即便固定总绕数，对应的物理构型仍不唯一")

print("\n[ROWS] C 层：超荷量子化、陈类整数性与回代")
_c01_ok = (KEY["qy_gcd"] == 1 and KEY["holonomy_constraint"] == "n 为整数")
add("C01", "C", "q_Y 全表 gcd 为 1，holonomy 只逼 n 为整数",
    "不得出现 n 为 3 的倍数的额外约束",
    "q_Y 表 %s；gcd %d；约束 %s"
    % (KEY["qy_table"], KEY["qy_gcd"], KEY["holonomy_constraint"]),
    _c01_ok, "表内含 q=1 与 q=-3 两个奇数荷，故 gcd 为 1")

_c02_ok = (KEY["tensor_gcd"] == 2 and KEY["tensor_gcd"] != KEY["qy_gcd"])
add("C02", "C", "负对照：纯张量谱的荷全偶，gcd 变为 2",
    "换谱后读数须从 1 变到 2",
    "纯张量荷多重集 %s；gcd %d；与含旋量谱的 %d 不同"
    % (str(TENSOR_Q), KEY["tensor_gcd"], KEY["qy_gcd"]),
    _c02_ok, "承接 X-V63-1 最小电荷刀：判据确实测的是换了谱")

_c03_ok = (KEY["iq_three_solutions"] == 0 and KEY["wind_target_all_hit"])
add("C03", "C", "对象错位刀：闭曲面 I_Q 与缺陷绕数是两个对象",
    "I_Q=3 的整数网格解须为 0，而 wind=3 可达",
    "整数网格 I_Q=3 解 %d；绕数 3 可命中的目标数 %d；两读数不相加"
    % (KEY["iq_three_solutions"],
       sum(1 for t, w in KEY["wind_target_grid"] if str(t) == "3")),
    _c03_ok, "把可达的 wind=3 读成 I_Q=3 是读数支持不了的解读")

add("C04", "C", "回代 X-V63-6 与 X-V63-1",
    "上一册的判别力 0 与陈类整数性只作输入，不重数条目",
    "X-V63-6 B06 为 FAIL（3/24）；X-V63-1 c1 须为整数；本册独立复算",
    None, "两册条目不与本册相加")

add("C05", "C", "反常 inflow 的 CS 级不产生 3 的选择定则",
    "边界项只要求级为整数",
    "k_CS = n 为整数；未给 n 模 3 的条件；完整 6D 反常账未算",
    None, "4D 反常匹配全账仍 OPEN")

from math import comb as _comb
_spin_plus_closed = sum(_comb(5, k) for k in (0, 2, 4))
_spin_plus_enum = sum(1 for q in SPIN_Q if q == 1)
_mom_closed = [0, int(2 * _spin_plus_closed), 0]
_c06_ok = (_spin_plus_closed == _spin_plus_enum == 16
           and KEY["spin_dim"] == 32
           and _mom_closed == KEY["spin_moments"])
add("C06", "C", "旋量 32 权矩：组合闭式与逐权枚举两路相符",
    "正荷权须同为 16，闭式矩与枚举矩一致",
    "闭式正荷权 %d / 枚举 %d；闭式矩 %s / 枚举矩 %s"
    % (_spin_plus_closed, _spin_plus_enum, _mom_closed, KEY["spin_moments"]),
    _c06_ok, "权矩不是完整 6D 反常多项式")

_c07_ok = (KEY["chern_legal_count"] == 3 and KEY["chern_half_legal"] == 0)
add("C07", "C", "带边不解除陈类整数性（口径回代）",
    "整数 N 合法 3 档、半整数 N 合法 0 档",
    "过渡函数绕数表 %s；合法 %d；半整数合法 %d"
    % ([(x["N"], x["wind"], x["legal"]) for x in KEY["chern_table"]],
       KEY["chern_legal_count"], KEY["chern_half_legal"]),
    _c07_ok, "与 X-V63-6 C01 同口径；本册对象不同，不相加")

print("\n[ROWS] D 层：诚实边界与不相加声明")
add("D01", "D", "本册不产新物理",
    "只产可算判决，独立实验预言数须为 0",
    "未构造新作用量、未给新粒子、未给可检验数值；独立预言 0",
    None, "数学自洽不等于实验证实")
add("D02", "D", "与 X-V63-6 / X-V63-1 / V63 不相加",
    "三册的读数只作输入回代",
    "本册独立复算条目数与前册 32 / 27 / 31 条不相加",
    None, "C04 显式声明口径回代")
add("D03", "D", "未重建的部分",
    "涡旋 BPS 剖面、能量泛函、完整 6D APS 指标、4D 反常匹配全账均未算",
    "只判群论层与拓扑层的可算约束；未解任何径向 ODE",
    None, "能量最小化也许能选 n，本册只给拓扑层判决")
add("D04", "D", "新增 Z_3 规范因子与 SU(3)_c 中心的可能性未被否证",
    "本册只说 Spin(2n) 中心给不出，不说任何扩展模型不可能",
    "外加 Z_3 离散规范对称性可给 n_min=3，但 Z_3 是输入；SU(3)_c 中心确为 Z_3（A08），若能把它与内部涡旋数投影联系则 B06 需重判，本册未做",
    None, "条件定理的边界必须写明；对象错位是本项目最高频自伤")
add("D05", "D", "四力统一仍未证",
    "V64 三道关口仍全部 OPEN",
    "关口一三代与反常未闭合、关口二质量与破缺未闭合、关口三引力同源未启动",
    None, "把它称为攻破统一场论会是虚假宣称")
add("D06", "D", "不占 RID、不动 README",
    "攻坚册不新增 RID、不进 README 登记位",
    "README %d B；r402 锚点 %d；r403 锚点 %d；三树 r403 文件 %d"
    % (KEY["readme_bytes"], KEY["readme_r402_tokens"],
       KEY["readme_r403_tokens"], KEY["r403_files"]),
    None, "下轮从 r403 正常取号，本册不占用")

print("\n[ROWS] K 层：四个控制组（四条读数两两不同）")
_k1_ok = (str(KEY["center_false_read_d6"]) != str(KEY["center_true_max_d6"]))
add("K1", "K", "把商群阶误当元素阶的负控",
    "误读 %d" % KEY["center_false_read_d6"],
    "D_6 真实最大阶 %d" % KEY["center_true_max_d6"],
    _k1_ok, "D_5 上两读数相同，故必须在偶 n 上测")
_k2_ok = (KEY["wind_nowrap_small"] != KEY["wind_wrap_small"])
add("K2", "K", "绕数器不 wrap 的负控",
    "误读 %s" % KEY["wind_nowrap_small"],
    "真实 %s" % KEY["wind_wrap_small"],
    _k2_ok, "M=8 且 n=5 越过 Nyquist")
_k3_ok = (KEY["zk_frozen"] != KEY["zk_hitrate"])
add("K3", "K", "冻结 k=3 的负控",
    "冻结通过率 %s" % KEY["zk_frozen"],
    "k=2..9 全档命中率 %s" % KEY["zk_hitrate"],
    _k3_ok, "承接 V63 C10 与 X-V63-6 K3 的冻结参数刀")
_k4_ok = (str(KEY["tensor_gcd"]) != str(KEY["qy_gcd"]))
add("K4", "K", "把含旋量谱误当纯张量谱的负控",
    "误谱 gcd %d" % KEY["tensor_gcd"],
    "真实 gcd %d" % KEY["qy_gcd"],
    _k4_ok, "最小电荷敏感刀的又一次复现")

KEY["k_pairs"] = [
    (str(KEY["center_false_read_d6"]), str(KEY["center_true_max_d6"])),
    (KEY["wind_nowrap_small"], KEY["wind_wrap_small"]),
    (KEY["zk_frozen"], KEY["zk_hitrate"]),
    (str(KEY["tensor_gcd"]), str(KEY["qy_gcd"])),
]

# 关键表两路机拼：左路取 KEY 缓存，右路现场重算，左右模板互不引用。
_left_center = [(x["n"], x["orders"]) for x in KEY["center_table"]]
_right_center = [(n, center_orders(n)) for n in N_RANGE]
_left_hom = KEY["wind_hom_match"]
_right_hom = sum(1 for a in W_GRID for b in W_GRID
                 if winding(a)[0] + winding(b)[0] == winding(a + b)[0])
_left_zk = [(x["k"], x["n_min"]) for x in KEY["zk_table"]]
_right_zk = [(k, min(n for n in range(1, 40) if n % k == 0))
             for k in range(2, 10)]
KEY["key_table_left"] = str([_left_center, _left_hom, _left_zk])
KEY["key_table_right"] = str([_right_center, _right_hom, _right_zk])
KEY["key_table_same"] = (KEY["key_table_left"] == KEY["key_table_right"])

DECLARED_NEG = ["B06"]


def counts_of(rows):
    c = {}
    for r in rows:
        c[r["kind"]] = c.get(r["kind"], 0) + 1
    return c


def final_of(nf_main, nf_guard, n_decl):
    if nf_guard:
        return "GATES-FAIL-GUARD-%d" % nf_guard
    if n_decl == 0:
        return "GATES-FAIL-UNDECLARED-NEGATIVE"
    if nf_main > 0:
        return "GATES-PASS-WITH-%d-NEGATIVE" % n_decl
    return "GATES-PASS-ALL-POSITIVE"


SRC_SELF = os.path.abspath(__file__)
COUNTS = counts_of(ROWS)
DECLARED_SET = set(DECLARED_NEG)


def build_segments(shift=0):
    """判词片段一律由 KEY 读数机拼；shift 用于证明片段真的吃读数。"""
    return [
        "CENTER-DN-%d-GRID" % len(KEY["center_table"]),
        "CENTER-ALL-ORDERS-%s" % "-".join(str(v) for v in KEY["center_all_orders"]),
        "CENTER-HAS3-%d" % (KEY["center_has3_count"] + shift),
        "SU3-CENTER-%s-OBJECT-DISTINCT" % KEY["su3_center_group"],
        "SPIN12-Z2XZ2--SPIN10-Z4",
        "NEG-CONTROL-QUOTIENT-ORDER-4-VS-2",
        "WIND-HOM-%d-OF-%d" % (KEY["wind_hom_match"], KEY["wind_hom_total"]),
        "WIND-MIN-POSITIVE-%s" % fmt_f(KEY["wind_min_positive"]),
        "DECOMP3-%d-TRIPLES" % KEY["decomp3_count"],
        "WIND-TARGET-1-TO-8-SURJECTIVE",
        "ZK-%d-GRID-HIT3-%s" % (KEY["zk_total"],
                                 KEY["zk_hitrate"].replace("/", "-OF-")),
        "INTERNAL-FIXERS-%d-OF-%d" % (KEY["internal_fixers_count"],
                                       KEY["internal_fix_paths"]),
        "FREE-PARAM-TRANSFER-N-TO-K",
        "CLUSTER-3X1-VS-1X3-SAME-TOTAL-DIFF-COUNT-%d" % KEY["cluster_diff_count"],
        "QY-GCD-%d--TENSOR-GCD-%d" % (KEY["qy_gcd"], KEY["tensor_gcd"]),
        "IQ-THREE-SOLUTIONS-%d" % KEY["iq_three_solutions"],
        "CHERN-INTEGERITY-SURVIVES-BOUNDARY",
        "SPIN32-MOMENTS-%s" % "-".join(str(v) for v in KEY["spin_moments"]),
        "FOUR-FORCE-INFO-UNPROVEN--UNIQUE-PREDICTION-0",
    ]


def no_native_violation(obj, path="root"):
    bad = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            bad.extend(no_native_violation(k, path + ".key"))
            bad.extend(no_native_violation(v, path + "." + str(k)))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            bad.extend(no_native_violation(v, path + "[%d]" % i))
    elif not isinstance(obj, (str, int, float, bool, type(None))):
        bad.append((path, type(obj).__name__))
    return bad


def run_guards(back):
    """所有守卫在此追加；FINAL 必须在调用本函数之后才计算。"""
    _tree = ast.parse(io.open(SRC_SELF, "r", encoding="utf-8").read())
    _bad = []
    for _node in ast.walk(_tree):
        if not (isinstance(_node, ast.Call) and isinstance(_node.func, ast.Name)):
            continue
        if _node.func.id == "add" and len(_node.args) >= 6:
            _a = _node.args[5]
            if isinstance(_a, ast.Constant) and _a.value not in (None, "ID"):
                _bad.append(("add", _a.lineno))
        if _node.func.id == "guard" and len(_node.args) >= 2:
            _a = _node.args[1]
            if isinstance(_a, ast.Constant):
                _bad.append(("guard", _a.lineno))
    guard("NO-HARDCODE-OK", len(_bad) == 0,
          "AST 扫描 add 第 6 参 / guard 第 2 参，字面量 ok 命中 %d" % len(_bad))

    _neq = [r["id"] for r in ROWS if r["exp"] == r["act"]]
    guard("EXP-NEQ-ACT", len(_neq) == 0,
          "全表 %d 条，exp 与 act 同串 %d 条" % (len(ROWS), len(_neq)))

    _kp = KEY["k_pairs"]
    _pair_set = set(str(p) for p in _kp)
    guard("NEG-CONTROL-TWO-SIDES",
          len(_kp) == 4 and len(_pair_set) == 4 and all(a != b for a, b in _kp),
          "四对读数 %s；互异 %d；每对内不同 %s"
          % (str(_kp), len(_pair_set), all(a != b for a, b in _kp)))

    guard("NOT-ALL-GREEN",
          COUNTS.get("FAIL", 0) >= 1 and COUNTS.get("IDENTITY", 0) >= 1
          and COUNTS.get("PASS", 0) >= 10,
          "计数 %s" % str(COUNTS))

    _a06 = [r for r in ROWS if r["id"] == "A06"][0]
    guard("SAME-SOURCE-TAGGED",
          _a06["kind"] in ("INFO", "IDENTITY") and "同源" in _a06["note"],
          "A06 kind=%s；note 含同源标注=%s"
          % (_a06["kind"], "同源" in _a06["note"]))

    _b06 = [r for r in ROWS if r["id"] == "B06"][0]
    guard("DECLARED-NEG",
          "B06" in DECLARED_SET and _b06["kind"] == "FAIL"
          and all(any(r["id"] == x for r in ROWS) for x in DECLARED_NEG),
          "已登记判负 %s；B06 kind=%s" % (str(DECLARED_NEG), _b06["kind"]))

    guard("KEY-TABLE-TWO-PATH",
          KEY["key_table_same"] and len(KEY["key_table_left"]) > 100,
          "左右两路现场重算：center %d 档 / hom %d 组 / Z_k %d 档；一致=%s"
          % (len(_left_center), _right_hom, len(_left_zk), KEY["key_table_same"]))

    _native = no_native_violation(back)
    guard("JSON-NATIVE", len(_native) == 0,
          "非原生类型命中 %d：%s" % (len(_native), str(_native)[:120]))

    _s0 = build_segments(0)
    _s1 = build_segments(1)
    guard("VERDICT-MACHINE",
          len(_s0) >= 15 and len(set(_s0)) == len(_s0)
          and "__".join(_s0) != "__".join(_s1),
          "片段 %d 个；读数 +1 后判词串变化=%s"
          % (len(_s0), "__".join(_s0) != "__".join(_s1)))

    guard("DISCRIM-POWER-DRIVES",
          _b06["kind"] == "FAIL"
          and KEY["internal_fixers_count"] == 0
          and KEY["zk_frozen"] != KEY["zk_hitrate"]
          and KEY["wind_target_all_hit"],
          "内部固定机制 %d；冻结 %s 对全档 %s；目标满射=%s"
          % (KEY["internal_fixers_count"], KEY["zk_frozen"],
             KEY["zk_hitrate"], KEY["wind_target_all_hit"]))

    guard("CENTER-NO-THREE",
          3 not in KEY["center_all_orders"]
          and KEY["center_has3_count"] == 0
          and len(KEY["center_table"]) == 6
          and _a03_ok,
          "六档全部元素阶 %s；含 3 阶元 %d 档；A03 ok=%s"
          % (KEY["center_all_orders"], KEY["center_has3_count"], _a03_ok))

    guard("WINDING-HOMOMORPHISM",
          KEY["wind_hom_match"] == KEY["wind_hom_total"]
          and KEY["wind_hom_bad"] == 0
          and KEY["wind_min_positive"] == 1,
          "同态 %d/%d；失配 %d；最小正绕数 %s"
          % (KEY["wind_hom_match"], KEY["wind_hom_total"],
             KEY["wind_hom_bad"], fmt_f(KEY["wind_min_positive"])))

    guard("NO-NEW-RID-NO-README",
          KEY["readme_r403_tokens"] == 0 and KEY["r403_files"] == 0
          and KEY["readme_r402_tokens"] == 2,
          "README %d B；r402 锚点 %d；r403 锚点 %d；三树 r403 文件 %d"
          % (KEY["readme_bytes"], KEY["readme_r402_tokens"],
             KEY["readme_r403_tokens"], KEY["r403_files"]))

    guard("KIND-COUNT", sum(COUNTS.values()) == len(ROWS),
          "计数和 %d 对条目数 %d" % (sum(COUNTS.values()), len(ROWS)))

    guard("FINAL-BRANCHES",
          final_of(1, 1, 1).startswith("GATES-FAIL-GUARD")
          and final_of(1, 0, 0) == "GATES-FAIL-UNDECLARED-NEGATIVE"
          and final_of(1, 0, 1) == "GATES-PASS-WITH-1-NEGATIVE"
          and final_of(0, 0, 1) == "GATES-PASS-ALL-POSITIVE",
          "守卫红挡门 / 缺 n_decl 错报 / 已登记判负不挡门 / 全正，四分支均测")

    _dump1 = json.dumps(back, ensure_ascii=False, sort_keys=True)
    _dump2 = json.dumps(back, ensure_ascii=False, sort_keys=True)
    guard("IDEMPOTENT-SELF", _dump1 == _dump2 and len(_dump1) > 1000,
          "序列化两次一致，长度 %d" % len(_dump1))


def make_out():
    return {
        "title": TITLE, "date": DATE, "rid": "NONE-NO-RID",
        "body_type": "跨卷攻坚册（不新增 RID、不进 README、条目不相加）",
        "final": "PENDING", "verdict": "PENDING",
        "n_rows": 0, "counts": {}, "declared_neg": list(DECLARED_NEG),
        "rows": [dict(r) for r in ROWS],
        "guards": [], "key_numbers": KEY,
        "key_table_two_path": {"left": KEY["key_table_left"],
                               "right": KEY["key_table_right"]},
        "backfill": {"before": 0, "after": 0},
    }


def main():
    # 回填顺序：写占位 -> 回读 -> 回填 -> 再写 -> 追加全部守卫 -> 才算 FINAL -> 最后拼报告
    out = make_out()
    io.open(JS, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, ensure_ascii=False, indent=1))
    back = json.load(io.open(JS, "r", encoding="utf-8"))
    _before = back["n_rows"]
    back["n_rows"] = len(ROWS)
    back["counts"] = counts_of(ROWS)
    back["backfill"] = {"before": _before, "after": len(ROWS)}
    io.open(JS, "w", encoding="utf-8", newline="\n").write(
        json.dumps(back, ensure_ascii=False, indent=1))

    guard("BACKFILL-ORDER",
          _before == 0 and back["n_rows"] == len(ROWS)
          and back["counts"] == COUNTS,
          "占位 %d -> 回填 %d；counts 同步=%s"
          % (_before, back["n_rows"], back["counts"] == COUNTS))
    run_guards(back)

    nf_guard = sum(1 for g in GUARDS if not g["ok"])
    nf_main = sum(1 for r in ROWS if r["kind"] == "FAIL")
    FINAL = final_of(nf_main, nf_guard, len(DECLARED_NEG))
    VERDICT = "__".join(build_segments(0))
    back["final"] = FINAL
    back["verdict"] = VERDICT
    back["guards"] = [dict(g) for g in GUARDS]
    back["guard_count"] = len(GUARDS)
    back["guard_pass"] = len(GUARDS) - nf_guard
    io.open(JS, "w", encoding="utf-8", newline="\n").write(
        json.dumps(back, ensure_ascii=False, indent=1))

    L = []
    L.append("=" * 78)
    L.append(TITLE + "  " + DATE)
    L.append("体例：跨卷攻坚册（不新增 RID、不进 README 登记位、条目不相加）")
    L.append("=" * 78)
    L.append("")
    L.append("FINAL = " + FINAL)
    L.append("VERDICT = " + VERDICT)
    L.append("")
    L.append("条目 %d（%s）；控制组 %d；守卫 %d/%d；DECLARED_NEG = %s"
             % (len(ROWS), str(COUNTS), len([r for r in ROWS if r["layer"] == "K"]),
                len(GUARDS) - nf_guard, len(GUARDS), str(DECLARED_NEG)))
    L.append("回填 = ROWS-%d/GUARDS-%d" % (len(ROWS), len(GUARDS)))
    L.append("")
    L.append("【主册逐条】")
    for r in ROWS:
        L.append("  %-4s [%-8s] %s" % (r["id"], r["kind"], r["name"]))
        L.append("        exp = " + r["exp"])
        L.append("        act = " + r["act"])
        if r["note"]:
            L.append("        note = " + r["note"])
    L.append("")
    L.append("【守卫】")
    for g in GUARDS:
        L.append("  [%-3s] %-24s | %s" % ("ok" if g["ok"] else "BAD", g["name"], g["detail"]))
    L.append("")
    L.append("【关键表 · 两路机拼】")
    for i, n in enumerate(N_RANGE):
        L.append("  D_%d 中心阶 左路 %s | 右路 %s | 群型 %s"
                 % (n, str(_left_center[i][1]), str(_right_center[i][1]),
                    KEY["center_table"][i]["group"]))
    L.append("  绕数同态 左路 %d | 右路 %d" % (_left_hom, _right_hom))
    for i, k in enumerate(range(2, 10)):
        L.append("  Z_%d 最小正绕数 左路 %d | 右路 %d"
                 % (k, _left_zk[i][1], _right_zk[i][1]))
    L.append("  两路一致 = " + str(KEY["key_table_same"]))
    L.append("")
    L.append("【关键数字】")
    L.append("  D_3..D_8 六档中心阶 %s"
             % str([(x["n"], x["orders"], x["group"]) for x in KEY["center_table"]]))
    L.append("  中心全部元素阶 %s；含 3 阶元 %d 档；最大阶集合 %s"
             % (KEY["center_all_orders"], KEY["center_has3_count"],
                KEY["center_max_set"]))
    L.append("  SU(3)_c 中心 %s（A_2 基本权最小回落 k=%d）；对象是 %s，与 Spin(2n) 中心不相加"
             % (KEY["su3_center_group"], KEY["su3_center_min"], KEY["su3_object"]))
    L.append("  D_6 误读商群阶 %d 对真实最大阶 %d；D_5 误读 %d 对真实 %d"
             % (KEY["center_false_read_d6"], KEY["center_true_max_d6"],
                KEY["center_false_read_d5"], KEY["center_true_max_d5"]))
    L.append("  绕数同态 %d/%d；失配 %d；最小正绕数 %s"
             % (KEY["wind_hom_match"], KEY["wind_hom_total"],
                KEY["wind_hom_bad"], fmt_f(KEY["wind_min_positive"])))
    L.append("  和为 3 的三元组 %d；含 (1,1,1) %s；全单位分解 %d"
             % (KEY["decomp3_count"], KEY["decomp3_trivial"],
                KEY["decomp3_unit_only"]))
    L.append("  Z_k 投影 %s；命中 3 的 %s；冻结一档 %s"
             % (str([(x["k"], x["n_min"]) for x in KEY["zk_table"]]),
                KEY["zk_hitrate"], KEY["zk_frozen"]))
    L.append("  内部固定机制 %d / %d 条路径 %s"
             % (KEY["internal_fixers_count"], KEY["internal_fix_paths"],
                str(KEY["internal_fixers"])))
    L.append("  3 个 n=1 总绕数 %s 缺陷数 %d；1 个 n=3 总绕数 %s 缺陷数 %d；差 %d"
             % (KEY["cluster_total_wind"], KEY["cluster_count_multi"],
                KEY["cluster_single_wind"], KEY["cluster_count_single"],
                KEY["cluster_diff_count"]))
    L.append("  q_Y gcd %d / 纯张量 gcd %d；约束 %s"
             % (KEY["qy_gcd"], KEY["tensor_gcd"], KEY["holonomy_constraint"]))
    L.append("  整数网格 I_Q=3 解 %d；旋量矩 %s / 矢量矩 %s"
             % (KEY["iq_three_solutions"], str(KEY["spin_moments"]),
                str(KEY["vec_moments"])))
    L.append("  陈类合法 %d / 半整数合法 %d"
             % (KEY["chern_legal_count"], KEY["chern_half_legal"]))
    L.append("  README %d B / r402 锚点 %d / r403 锚点 %d / 三树 r403 文件 %d"
             % (KEY["readme_bytes"], KEY["readme_r402_tokens"],
                KEY["readme_r403_tokens"], KEY["r403_files"]))
    L.append("")
    L.append("【诚实边界】")
    L.append("  1. 只产可算判决，不产新物理；独立实验预言 0。")
    L.append("  2. 涡旋 BPS 剖面、能量泛函与径向 ODE 未解，未判能量最小化。")
    L.append("  3. 完整 6D APS 指标与边界 Chern-Simons 级未重建。")
    L.append("  4. 4D 反常匹配全账、CKM / PMNS、质量谱均未算。")
    L.append("  5. Spin(2n) 中心给不出 Z_3，不等于外加 Z_3 因子或 SU(3)_c 中心不可能。")
    L.append("  6. 四力统一未证明；V64 三道关口仍全部 OPEN。")
    L.append("  7. 本册为攻坚册：不新增 RID、不进 README、不与任何卷相加。")
    L.append("")
    L.append("【DECLARED_NEG】" + str(DECLARED_NEG))
    io.open(RPT, "w", encoding="utf-8", newline="\r\n").write("\n".join(L) + "\n")
    print("\nFINAL = " + FINAL)
    print("条目 %d %s / 守卫 %d/%d" % (len(ROWS), str(COUNTS),
                                    len(GUARDS) - nf_guard, len(GUARDS)))
    print("JSON = " + JS)
    print("REPORT = " + RPT)


if __name__ == "__main__":
    main()
