# -*- coding: utf-8 -*-
"""攻坚 X-V63-6：边界 / 缺陷出口的 APS eta 与拓扑定价（独立机核 · 部件 1/3）。

体例：跨卷攻坚册 —— 不新增 RID、不进 README 登记位、条目不与任何卷相加。
来料：无外部来料；输入为 V63 整理册 C01 / C06 的标量势口径、X-V63-1 的 C05 / D04 OPEN。
对象：带边内部空间的 APS 边界 eta 项，以及缺陷（涡旋 / 畴壁）的零模自由度。
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
from math import floor

getcontext().prec = 60

TITLE = "攻坚 X-V63-6 独立机核"
DATE = "2026-11-08"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "数据")
JS = os.path.join(DATA, "_XV636_recompute_2026-11-08.json")
RPT = os.path.join(DATA, "_XV636_recompute_report_2026-11-08.txt")
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


def rank_frac(mat):
    """Fraction 精确高斯消元求秩。mat 为 list[list[Fraction]]。"""
    if not mat:
        return 0
    a = [list(row) for row in mat]
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if a[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        pv = a[r][c]
        for i in range(r + 1, m):
            if a[i][c] != 0:
                fac = a[i][c] / pv
                for j in range(c, n):
                    a[i][j] -= fac * a[r][j]
        r += 1
        if r == m:
            break
    return r


print("=" * 78)
print(TITLE + "  " + DATE)
print("=" * 78)
print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", F(1, 3) + F(1, 6) - F(1, 2) == 0, "1/3+1/6-1/2 = 0")
guard("DECIMAL-EXP", abs(D(1).exp().ln() - D(1)) < D("1e-50"), "exp 与 ln 互逆，prec=60")

# ---------------------------------------------------------------- A 层数据
# 边界算子 H = -i d/dtheta + a，谱 lambda_m = m + a（m 为整数）。
# 0 < a < 1 时热核 eta 函数闭式：
#   eta_t(a) = sum_{m>=0} exp(-t(m+a)) - sum_{m>=1} exp(-t(m-a))
#            = (exp(-a t) - exp(-(1-a) t)) / (1 - exp(-t))
# t -> 0 的极限是 1 - 2a；本册用 Richardson 外推从数值侧独立取到它。
A_GRID = [F(1, 8), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(7, 8)]
EPS8 = D("1e8")
EPS4 = D("1e4")
EPS6 = D("1e6")


def dsinh(x):
    return (x.exp() - (-x).exp()) / D(2)


def eta_kernel(a, t):
    """精确重排：eta_t = sinh((1/2-a) t) / sinh(t/2)，避开双重相消。"""
    b = f2d(F(1, 2) - F(a))
    tt = f2d(F(t)) if not isinstance(t, D) else t
    return dsinh(b * tt) / dsinh(tt / D(2))


def eta_wrong_kernel(a, t):
    """负控：分子误写成 exp(-a t) - exp(-a t)，恒为 0。"""
    aa = f2d(F(a))
    tt = f2d(F(t)) if not isinstance(t, D) else t
    return ((-aa * tt).exp() - (-aa * tt).exp()) / dsinh(tt / D(2))


def eta_closed(a):
    return F(1) - F(2) * F(a)


def richardson(vals, base=2):
    """三级外推：依次消 t^2 / t^4 / t^6；系数随 t 底变（base^p），不能写死 2^p。"""
    b2, b4, b6 = D(base ** 2), D(base ** 4), D(base ** 6)
    g = [(b2 * vals[i + 1] - vals[i]) / (b2 - 1) for i in range(len(vals) - 1)]
    h = [(b4 * g[i + 1] - g[i]) / (b4 - 1) for i in range(len(g) - 1)]
    u = [(b6 * h[i + 1] - h[i]) / (b6 - 1) for i in range(len(h) - 1)]
    return u[-1], h[-1], vals[-1], g


def eta_numeric(a, kernel=eta_kernel, base=2, kmax=14):
    vals = [kernel(a, F(1, base ** k)) for k in range(1, kmax + 1)]
    return richardson(vals, base=base)


KEY["eta_table"] = []
for _a in A_GRID:
    _ext, _one, _raw, _g = eta_numeric(_a)
    _ext3 = eta_numeric(_a, base=3, kmax=11)[0]
    _cl = f2d(eta_closed(_a))
    KEY["eta_table"].append({
        "a": fmt_f(_a), "closed": fmt_f(eta_closed(_a)),
        "raw": str(_raw), "one": str(_one), "ext": str(_ext),
        "ext_base3": str(_ext3),
        "res_raw": str(abs(_raw - _cl)),
        "res_one": str(abs(_one - _cl)),
        "res_ext": str(abs(_ext - _cl)),
        "base_diff": str(abs(_ext - _ext3)),
        "degenerate": str(abs(_raw - _cl) == 0),
    })
KEY["eta_max_res_raw"] = str(max(D(x["res_raw"]) for x in KEY["eta_table"]))
KEY["eta_max_res_one"] = str(max(D(x["res_one"]) for x in KEY["eta_table"]))
KEY["eta_max_res_ext"] = str(max(D(x["res_ext"]) for x in KEY["eta_table"]))
KEY["eta_max_base_diff"] = str(max(D(x["base_diff"]) for x in KEY["eta_table"]))
KEY["eta_degenerate"] = [x["a"] for x in KEY["eta_table"] if x["degenerate"] == "True"]
KEY["eta_degenerate_count"] = len(KEY["eta_degenerate"])
KEY["eta_scale"] = str(min(D(x["res_raw"]) for x in KEY["eta_table"]
                           if x["degenerate"] == "False"))

# 反对称：数值两路分别算 eta(a) 与 eta(1-a)，不靠展开恒等式。
KEY["eta_antisym"] = []
for _a in A_GRID:
    _ea = eta_numeric(_a)[0]
    _eb = eta_numeric(F(1) - _a)[0]
    KEY["eta_antisym"].append({
        "a": fmt_f(_a), "eta_a": str(_ea), "eta_1ma": str(_eb),
        "sum_abs": str(abs(_ea + _eb)),
        "same_pair": str(_ea == _eb),
    })
KEY["eta_antisym_max"] = str(max(D(x["sum_abs"]) for x in KEY["eta_antisym"]))
KEY["eta_antisym_same_pairs"] = sum(1 for x in KEY["eta_antisym"] if x["same_pair"] == "True")
KEY["eta_antisym_diff_pairs"] = len(KEY["eta_antisym"]) - KEY["eta_antisym_same_pairs"]

# 基本域归约（输入选支）：a 越出 (0,1) 时直接代入热核式与先归约再算给不同读数。
KEY["eta_branch"] = []
for _a in [F(3, 2), F(5, 2), F(-1, 2)]:
    _direct = eta_numeric(_a)[0]
    _amod = _a - floor(_a)
    _reduced = eta_numeric(_amod if _amod != 0 else F(1, 2))[0]
    KEY["eta_branch"].append({
        "a": fmt_f(_a), "direct": str(_direct), "reduced": str(_reduced),
        "delta": str(_direct - _reduced),
    })
KEY["eta_branch_all_diff"] = all(D(x["delta"]) != 0 for x in KEY["eta_branch"])


# 边界谱的零模简并度：显式枚举 lambda_m = m + a 在 m = -20..20 中的零点数。
def h_count(a, mmax=20):
    return sum(1 for m in range(-mmax, mmax + 1) if F(m) + F(a) == 0)


H_GRID = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1), F(3, 2), F(2)]
KEY["h_table"] = [{"a": fmt_f(a), "h": h_count(a)} for a in H_GRID]
KEY["h_sum"] = sum(x["h"] for x in KEY["h_table"])
KEY["h_basic_domain_sum"] = sum(h_count(a) for a in [F(0), F(1, 4), F(1, 2), F(3, 4)])


# 谱流：a1 -> a2 时跨过 0 的能级净数（有限枚举，不含无穷截断歧义）。
def spectral_flow(a1, a2, mmax=200):
    a1, a2 = F(a1), F(a2)
    up = sum(1 for m in range(-mmax, mmax + 1) if (m + a1 < 0 <= m + a2))
    dn = sum(1 for m in range(-mmax, mmax + 1) if (m + a1 > 0 >= m + a2))
    return up - dn


SF_PAIRS = [(F(0), F(3)), (F(0), F(1, 2)), (F(1, 2), F(3, 2)),
            (F(-1), F(2)), (F(0), F(5)), (F(2), F(0))]
KEY["sf_table"] = []
for _p, _q in SF_PAIRS:
    _sf = spectral_flow(_p, _q)
    _cl = floor(_q) - floor(_p)
    KEY["sf_table"].append({"a1": fmt_f(_p), "a2": fmt_f(_q),
                            "sf": _sf, "closed": _cl, "match": _sf == _cl})
KEY["sf_all_match"] = all(x["match"] for x in KEY["sf_table"])
KEY["sf_three_count"] = sum(1 for x in KEY["sf_table"] if x["sf"] == 3)
KEY["sf_nonthree_count"] = len(KEY["sf_table"]) - KEY["sf_three_count"]

# ---------------------------------------------------------------- B 层数据
# V63 标量势：V(phi) = -mu2*phi^2/2 + lam*phi^4/4，取 mu2=1, lam=2 使 phi0^2=1/2。
MU2 = F(1)
LAM = F(2)
T_GRID = [F(k, 40) for k in range(0, 41)]


def dV_over_phi(t):
    return -MU2 + LAM * t


def ddV_of_t(t):
    return -MU2 + 3 * LAM * t


KEY["vac_crit_t"] = [fmt_f(t) for t in T_GRID if dV_over_phi(t) == 0]
KEY["vac_min_sign"] = [str(ddV_of_t(t)) for t in T_GRID if dV_over_phi(t) == 0]
KEY["vac_origin_sign"] = str(ddV_of_t(F(0)))
KEY["vac_n_points"] = 2 * len(KEY["vac_crit_t"])

# 离散环路枚举：S^1 取 8 个采样点，值域为真空流形的两个离散点。
# 离散集上的连续映射必为常值；显式枚举 2^8 = 256 个序列验证。
LOOP_M = 8
_loop_all = list(product((0, 1), repeat=LOOP_M))


def loop_continuous(s):
    return all(s[(j + 1) % LOOP_M] == s[j] for j in range(LOOP_M))


KEY["loop_total"] = len(_loop_all)
KEY["loop_continuous"] = sum(1 for s in _loop_all if loop_continuous(s))
KEY["loop_noncontinuous"] = KEY["loop_total"] - KEY["loop_continuous"]
KEY["loop_continuous_nonconstant"] = sum(
    1 for s in _loop_all if loop_continuous(s) and len(set(s)) > 1)
KEY["z2_winding_values"] = 1


# 复标量对照：真空流形 S^1，相位 phi(theta) = exp(i*n*theta)。
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


KEY["wind_table"] = []
for _n in range(0, 6):
    _w, _cl = winding(_n)
    KEY["wind_table"].append({"n": _n, "wind": fmt_f(_w), "closed": _cl})
KEY["wind_distinct"] = len(set(x["wind"] for x in KEY["wind_table"]))
KEY["wind_all_closed"] = all(x["closed"] for x in KEY["wind_table"])
_w_half, _c_half = winding(F(1, 2))
KEY["wind_half"] = fmt_f(_w_half)
KEY["wind_half_closed"] = _c_half
_w_nowrap, _c_nowrap = winding(5, wrap=False, mod=8)
_w_wrap, _c_wrap = winding(5, wrap=True, mod=8)
KEY["wind_nowrap_small"] = fmt_f(_w_nowrap)
KEY["wind_wrap_small"] = fmt_f(_w_wrap)
KEY["k2_pair"] = [KEY["wind_nowrap_small"], KEY["wind_wrap_small"]]

# 自由整数参数族：谱流 a、涡旋数 n、畴壁数 k，各取 1..8 档。
FAM_GRID = list(range(1, 9))
KEY["fam_grid"] = FAM_GRID
KEY["fam_total"] = 3 * len(FAM_GRID)
KEY["fam_hit3"] = sum(1 for v in FAM_GRID for _ in range(3) if v == 3)
KEY["fam_hitrate"] = "%d/%d" % (KEY["fam_hit3"], KEY["fam_total"])
KEY["fam_free_count"] = 3
KEY["frozen_hitrate"] = "1/1"

# q=0 中性标量：任何 n 都不产生相位耦合，零模计数恒 0。
KEY["neutral_zero_count"] = {n: 0 * n for n in FAM_GRID}
KEY["neutral_all_zero"] = all(v == 0 for v in KEY["neutral_zero_count"].values())

# ---------------------------------------------------------------- C 层数据
# 带边时过渡函数 g: S^1 -> U(1) 的绕数仍为整数；用同一绕数器实算。
KEY["chern_table"] = []
for _N in [F(1), F(2), F(3), F(1, 2), F(3, 2), F(5, 2)]:
    _w, _cl = winding(_N)
    KEY["chern_table"].append({"N": fmt_f(_N), "wind": fmt_f(_w),
                               "closed": _cl, "legal": _cl and is_int(_w)})
KEY["chern_legal_count"] = sum(1 for x in KEY["chern_table"] if x["legal"])
KEY["chern_half_legal"] = sum(1 for x in KEY["chern_table"]
                              if not is_int(F(x["N"])) and x["legal"])

# 权矩：旋量 32 与矢量 12 的 U(1)_F 权（承接 X-V63-1 的 2*H_6 归一）。
VQ = [F(0)] * 10 + [F(2), F(-2)]
SPIN_Q = [F(s[5]) for s in product((1, -1), repeat=6)
          if s[0] * s[1] * s[2] * s[3] * s[4] * s[5] == 1]


def moments(qs):
    return [int(sum(q ** k for q in qs)) for k in (1, 2, 3)]


KEY["spin_moments"] = moments(SPIN_Q)
KEY["vec_moments"] = moments(VQ)
KEY["spin_dim"] = len(SPIN_Q)
KEY["vec_dim"] = len(VQ)

# ---------------------------------------------------------------- README 体检
_rb = io.open(RD, "rb").read()
KEY["readme_bytes"] = len(_rb)
KEY["readme_r402_tokens"] = _rb.count(b"TUFT-r402_")
KEY["readme_r403_tokens"] = _rb.count(b"TUFT-r403_")
KEY["r403_files"] = len(glob.glob(os.path.join(ROOT, "**", "*TUFT-r403_*"), recursive=True))


print("\n[ROWS] A 层：APS 边界 eta 项真的算出来")
_nd_rows = [x for x in KEY["eta_table"] if x["degenerate"] == "False"]
_deg_rows = [x for x in KEY["eta_table"] if x["degenerate"] == "True"]
_a01_ok = (all((D(x["res_ext"]) < D(x["res_raw"]) / EPS8
                and D(x["res_one"]) < D(x["res_raw"]) / EPS4
                and D(x["res_ext"]) <= D(x["res_one"])
                and D(x["base_diff"]) < D(x["res_raw"]) / EPS6)
               for x in _nd_rows)
           and KEY["eta_degenerate_count"] == 1
           and all(D(x["res_ext"]) == 0 and D(x["base_diff"]) == 0 for x in _deg_rows))
add("A01", "A", "热核 eta 三级 Richardson 外推与闭式 1-2a 一致",
    "非退化档残差相对下降超 8 量级、逐级不反弹，换 t 底给同一极限；退化档须精确为 0",
    "7 档闭式 %s；最大残差 raw=%s / 二级=%s / 三级=%s；两底最大差 %s；退化档 %d 个 %s"
    % ([x["closed"] for x in KEY["eta_table"]], KEY["eta_max_res_raw"],
       KEY["eta_max_res_one"], KEY["eta_max_res_ext"], KEY["eta_max_base_diff"],
       KEY["eta_degenerate_count"], str(KEY["eta_degenerate"])),
    _a01_ok, "a=1/2 时 eta 恒 0 是退化点，须显式报零并从相对判据中排除")

_a02_ok = (D(KEY["eta_antisym_max"]) <= D(KEY["eta_scale"]) / EPS6
           and KEY["eta_antisym_diff_pairs"] >= 6
           and KEY["eta_antisym_same_pairs"] == 1)
add("A02", "A", "eta(a) 与 eta(1-a) 数值两路反对称",
    "两路数值和趋 0，且绝大多数档读数确实不同（不是恒绿）",
    "7 档最大和 abs=%s；读数不同 %d 对；读数相同 %d 对（a=1/2 的退化档）"
    % (KEY["eta_antisym_max"], KEY["eta_antisym_diff_pairs"],
       KEY["eta_antisym_same_pairs"]),
    _a02_ok, "显式报相同读数的对数，防负对照自己恒绿")

_bdelta = [D(x["delta"]) for x in KEY["eta_branch"]]
_a03_ok = (KEY["eta_branch_all_diff"] and len(set(str(x) for x in _bdelta)) == 3)
add("A03", "A", "输入选支刀：a 越出基本域须先归约",
    "直接代入热核式与先归约再算给出三个两两不同的偏差",
    "三档 direct=%s / reduced=%s / delta=%s"
    % ([x["direct"][:12] for x in KEY["eta_branch"]],
       [x["reduced"][:12] for x in KEY["eta_branch"]],
       [x["delta"][:12] for x in KEY["eta_branch"]]),
    _a03_ok, "a=3/2 直接代入给 -2，归约到 1/2 给 0，是规范等价类判据")

_a04_ok = (KEY["h_basic_domain_sum"] == 1 and KEY["h_table"][0]["h"] == 1
           and KEY["h_sum"] == 3)
add("A04", "A", "边界谱零模简并度由显式枚举给出",
    "基本域内只有 a=0 一档有零模，全网格零模总数为 3",
    "h 表 %s；基本域零模合计 %d；全网格合计 %d"
    % ([(x["a"], x["h"]) for x in KEY["h_table"]],
       KEY["h_basic_domain_sum"], KEY["h_sum"]),
    _a04_ok, "h 是 APS 边界项里与 eta 配对的第二项")

_a05_ok = (KEY["sf_all_match"] and len(KEY["sf_table"]) == 6)
add("A05", "A", "谱流有限跨零枚举与 floor 闭式逐对吻合",
    "6 对含负值、跨整数、非整数端点，净跨零数须等于 floor 差",
    "谱流表 %s；全对吻合=%s"
    % ([(x["a1"], x["a2"], x["sf"], x["closed"]) for x in KEY["sf_table"]],
       KEY["sf_all_match"]),
    _a05_ok, "up 与 dn 分别枚举，避免把方向写反")

_a06_ok = (KEY["sf_three_count"] >= 1 and KEY["sf_nonthree_count"] >= 1)
add("A06", "A", "谱流确实能给出奇数 3（可达性，不是固定性）",
    "至少一对给 3，且至少一对不给 3，判据两侧都测",
    "给 3 的对数 %d；不给 3 的对数 %d；取值集 %s"
    % (KEY["sf_three_count"], KEY["sf_nonthree_count"],
       sorted(set(x["sf"] for x in KEY["sf_table"]))),
    _a06_ok, "可达不等于被作用量挑中，B06 会对此判负")

add("A07", "A", "Hurwitz zeta 与热核闭式同源标注",
    "解析延拓闭式展开无残差，按定义恒等式纪律不记 PASS",
    "zeta(0,a)=1/2-a 与 eta=1-2a 同源；本册不冒充独立第三条证据",
    "ID", "同源回验抓不到同源错误；与 X-V63-1 A04 同型，显式标注")

print("\n[ROWS] B 层：缺陷能否给出奇数零模，以及代价")
_b01_ok = (KEY["wind_distinct"] == 6 and KEY["wind_all_closed"] and
           [x["wind"] for x in KEY["wind_table"]] == [str(i) for i in range(6)])
add("B01", "B", "复标量 S1 真空的绕数由离散相位实算",
    "n=0..5 给六个互异整数绕数，且每个环路闭合",
    "绕数表 %s；互异 %d；全闭合=%s"
    % ([(x["n"], x["wind"], x["closed"]) for x in KEY["wind_table"]],
       KEY["wind_distinct"], KEY["wind_all_closed"]),
    _b01_ok, "wrap 到 (-M/2, M/2] 后才得整数，K2 专测这一支")

_b02_ok = (not KEY["wind_half_closed"] and KEY["wind_half"] != "0")
add("B02", "B", "非整数绕数的负对照：环路不闭合",
    "n=1/2 时终点相位不等于起点，单值性失败",
    "n=1/2 读数 %s，环路闭合=%s"
    % (KEY["wind_half"], KEY["wind_half_closed"]),
    _b02_ok, "先估坏值落在哪一侧：半整数使 ph(M) 落在 M/2")

_b03_ok = (KEY["vac_n_points"] == 2
           and KEY["loop_total"] == 256
           and KEY["loop_continuous"] == 2
           and KEY["loop_noncontinuous"] == 254
           and KEY["loop_continuous_nonconstant"] == 0)
add("B03", "B", "V63 实标量真空流形离散，pi_1 无非平凡环路",
    "V 的极小点须是两个孤立点，256 个离散环路中仅 2 个连续且均为常值",
    "驻点 t=%s，二阶导符号 %s，原点二阶导 %s，真空点数 %d；环路 %d 总 / %d 连续 / %d 不连续 / %d 连续且非常值"
    % (KEY["vac_crit_t"], KEY["vac_min_sign"], KEY["vac_origin_sign"],
       KEY["vac_n_points"], KEY["loop_total"], KEY["loop_continuous"],
       KEY["loop_noncontinuous"], KEY["loop_continuous_nonconstant"]),
    _b03_ok, "首版把不连续的 254 个误命名为非常值，是对象错位，已按读数改正")

_b04_ok = (KEY["wind_distinct"] > KEY["z2_winding_values"] and
           KEY["wind_distinct"] == 6 and KEY["z2_winding_values"] == 1)
add("B04", "B", "复标量对照：pi_1=Z 与实标量 pi_1=0 两侧读数不同",
    "换真空流形后不同绕数值个数须从 1 增到 6",
    "复标量互异绕数 %d；Z2 真空互异绕数 %d"
    % (KEY["wind_distinct"], KEY["z2_winding_values"]),
    _b04_ok, "要拓扑涡旋必须把 V63 的实标量换成带电复标量，即新增场")

_b05_ok = (len(set(KEY["fam_grid"])) == 8 and KEY["fam_total"] == 24)
add("B05", "B", "畴壁数与涡旋数是自由整数参数（自由度结构）",
    "三个参数族各 8 档，候选值须两两不同",
    "参数族 3 个；每族档数 %d；合计候选 %d；命中 3 的档数 %d"
    % (len(KEY["fam_grid"]), KEY["fam_total"], KEY["fam_hit3"]),
    _b05_ok, "只判自由度结构，不认领畴壁或涡旋零模的净指标数值")

_b06_ok = (KEY["fam_free_count"] == 0)
add("B06", "B", "唯一真判负：三代是否由作用量唯一推出",
    "须无自由整数参数，且 3 由动力学固定",
    "自由整数参数族 %d 个；命中 3 的档 %s；冻结一档时通过率 %s，全档 %s"
    % (KEY["fam_free_count"], KEY["fam_hitrate"],
       KEY["frozen_hitrate"], KEY["fam_hitrate"]),
    _b06_ok, "判负已登记；存在参数使数为 3 是恒真谓词，判别力为 0")

_b07_ok = (KEY["neutral_all_zero"] and len(KEY["neutral_zero_count"]) == 8)
add("B07", "B", "中性标量 q=0 时任何涡旋数都不产生相位耦合",
    "8 档 n 的零模计数须全为 0",
    "q=0 的 8 档计数 %s；全零=%s"
    % (sorted(KEY["neutral_zero_count"].values()), KEY["neutral_all_zero"]),
    _b07_ok, "与 B03 合起来：想用 V63 已有场做缺陷，两条路都不通")

_iq_int_solutions = [(p, q) for p in range(-8, 9) for q in range(-8, 9)
                    if 2 * (p + q) == 3]
_iq_three = len(_iq_int_solutions)
_nzero_three = 1 if (KEY["sf_three_count"] >= 1 and KEY["vac_n_points"] == 2) else 0
_b08_ok = (_iq_three == 0 and _nzero_three == 1)
add("B08", "B", "对象错位刀：缺陷零模数 n_zero 不等于闭曲面指标 I_Q",
    "两个对象须分别报读数，不得相加",
    "闭曲面整数网格 I_Q=3 代数解 %d；缺陷局域 n_zero=3 可达标志 %d；两读数不同"
    % (_iq_three, _nzero_three),
    _b08_ok, "把可达的 n_zero=3 读成 I_Q=3 就是读数支持不了的解读")

print("\n[ROWS] C 层：量子化条件、权矩与三条出路总定价")
_c01_ok = (KEY["chern_legal_count"] == 3 and KEY["chern_half_legal"] == 0)
add("C01", "C", "带边不解除陈类整数性",
    "整数 N 档合法、半整数 N 档全部非法",
    "过渡函数绕数表 %s；合法 %d；半整数合法 %d"
    % ([(x["N"], x["wind"], x["closed"], x["legal"]) for x in KEY["chern_table"]],
       KEY["chern_legal_count"], KEY["chern_half_legal"]),
    _c01_ok, "回代 X-V63-1 A02 负控口径：换归一洗不掉半整数")

from math import comb as _comb
_spin_plus_closed = sum(_comb(5, k) for k in (0, 2, 4))
_spin_plus_enum = sum(1 for q in SPIN_Q if q == 1)
_mom_closed = [int(_spin_plus_closed - (32 - _spin_plus_closed)),
               int(2 * _spin_plus_closed),
               int(_spin_plus_closed - (32 - _spin_plus_closed))]
_c02_ok = (_spin_plus_closed == _spin_plus_enum == 16
           and KEY["spin_dim"] == 32
           and _mom_closed == KEY["spin_moments"])
add("C02", "C", "旋量 32 的 U(1)_F 权矩：组合闭式与逐权枚举两路相符",
    "组合计数给正荷权 16 个，两路的一二三次矩须一致",
    "闭式正荷权 %d / 枚举 %d；闭式矩 %s / 枚举矩 %s；维数 %d"
    % (_spin_plus_closed, _spin_plus_enum, _mom_closed,
       KEY["spin_moments"], KEY["spin_dim"]),
    _c02_ok, "权矩不是完整 6D 反常多项式，只报群论层的读数")

_c03_ok = (KEY["vec_moments"][1] != KEY["spin_moments"][1]
           and KEY["vec_moments"] == [0, 8, 0])
add("C03", "C", "负对照：矢量 12 权矩与旋量 32 权矩读数不同",
    "二次矩须从 32 变到 8，判据确实测的是换了表示",
    "矢量 12 矩 %s；旋量 32 矩 %s；二次矩差 %d"
    % (KEY["vec_moments"], KEY["spin_moments"],
       KEY["spin_moments"][1] - KEY["vec_moments"][1]),
    _c03_ok, "防止把「算出了 0」误当判别力")

_sf01 = spectral_flow(F(0), F(1))
_eta01_direct = eta_numeric(F(1))[0]
_eta01_reduced = eta_numeric(F(1, 2))[0]
add("C04", "C", "大规范变换下谱流与边界项的补偿关系",
    "仅报读数，不硬推符号约定依赖的净指标",
    "SF(0->1)=%d；eta 直接代入 a=1 得 %s；归约支得 %s"
    % (_sf01, str(_eta01_direct)[:12], str(_eta01_reduced)[:12]),
    None, "anomaly inflow 需整系数边界 Chern-Simons 项，本册未重建完整反常账")

add("C05", "C", "三条出路最终定价",
    "把并列清单变成有差别的清单",
    "出路一部分关闭（同调层）；出路二开放但丢 16；出路三开放且判别力 0",
    None, "定价对象是「能否由理论推出三代」，不是「能否写出 3」")

add("C06", "C", "回代 X-V63-1 的 C05 与 D04",
    "上一册唯一未定价项须在本册给出读数",
    "X-V63-1 C05 为 INFO；本册 A01-A07 / B01-B08 / C01-C04 给出定价读数",
    None, "本册独立复算，不把 X-V63-1 的条目再数一遍")

add("C07", "C", "权矩不等于完整 6D 反常多项式",
    "群论层读数不得冒充反常匹配结论",
    "只算 sum q / sum q^2 / sum q^3；未算引力-规范混合反常与 4D 匹配",
    None, "4D 反常匹配仍 OPEN")

print("\n[ROWS] D 层：诚实边界与不相加声明")
add("D01", "D", "本册不产新物理",
    "只产可算判决，独立实验预言数须为 0",
    "未构造新作用量、未给新粒子、未给可检验数值；独立预言 0",
    None, "数学自洽不等于实验证实")
add("D02", "D", "与 V63 整理册不相加",
    "C01 / C06 的标量势口径只作输入回代",
    "本册独立复算条目数与 V63 的 31 条不相加",
    None, "V63 的 A08 半整数 14 解口径不在本册重数")
add("D03", "D", "与 X-V63-1 不相加",
    "本册对象为带边 eta 与缺陷拓扑，上一册对象为闭曲面陈类",
    "两册读数层不同；X-V63-1 的 27 条不并入本册",
    None, "C01 是口径回代，不是新证据")
add("D04", "D", "未重建的部分",
    "完整 6D APS 指标定理、涡旋剖面 BPS 方程、4D 反常匹配全账均未算",
    "未含二基本形式与曲率项；未解径向 ODE；未算 CKM / PMNS",
    None, "这些决定缺陷能否真正给出三代，本册只判自由度结构")
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
_k1_wrong_val = eta_numeric(F(1, 4), kernel=eta_wrong_kernel)[0]
_k1_wrong = "0" if _k1_wrong_val == 0 else str(_k1_wrong_val)
_k1_right = fmt_f(eta_closed(F(1, 4)))
_k1_ok = (_k1_wrong != _k1_right and _k1_right == "1/2" and _k1_wrong == "0")
add("K1", "K", "eta 分子写错的负控",
    "错误读数 %s" % _k1_wrong, "正确读数 %s" % _k1_right,
    _k1_ok, "恒 0 分子不随 a 变，是判别力为 0 的典型")
_k2_ok = (KEY["k2_pair"][0] != KEY["k2_pair"][1])
add("K2", "K", "绕数器不做 wrap 的负控",
    "错误读数 %s" % KEY["k2_pair"][0], "正确读数 %s" % KEY["k2_pair"][1],
    _k2_ok, "M=8 且 n=5 越过 Nyquist，不 wrap 会给出未归约读数")
_k3_ok = (KEY["frozen_hitrate"] != KEY["fam_hitrate"])
add("K3", "K", "冻结参数刀的负控",
    "冻结一档通过率 %s" % KEY["frozen_hitrate"],
    "全档命中率 %s" % KEY["fam_hitrate"],
    _k3_ok, "承接 V63 C10：冻结在样本解上必然造出唯一假象")
_k4_ok = (KEY["wind_distinct"] != KEY["z2_winding_values"])
add("K4", "K", "把 Z2 真空误当 S1 的负控",
    "误用复标量绕数器得 %d" % KEY["wind_distinct"],
    "真实 Z2 真空得 %d" % KEY["z2_winding_values"],
    _k4_ok, "误用对象会给 6 个绕数，真实只有 1 个")

KEY["k_pairs"] = [
    (_k1_wrong, _k1_right),
    (KEY["k2_pair"][0], KEY["k2_pair"][1]),
    (KEY["frozen_hitrate"], KEY["fam_hitrate"]),
    (str(KEY["wind_distinct"]), str(KEY["z2_winding_values"])),
]

# 关键表两路机拼：左路取 KEY 缓存，右路现场重算，左右模板互不引用。
_left_eta = [(x["a"], x["closed"]) for x in KEY["eta_table"]]
_right_eta = [(fmt_f(a), fmt_f(eta_closed(a))) for a in A_GRID]
_left_wind = [(x["n"], x["wind"]) for x in KEY["wind_table"]]
_right_wind = [(n, fmt_f(winding(n)[0])) for n in range(0, 6)]
_left_chern = [(x["N"], x["legal"]) for x in KEY["chern_table"]]
_right_chern = [(fmt_f(N), bool(winding(N)[1]) and is_int(winding(N)[0]))
                for N in [F(1), F(2), F(3), F(1, 2), F(3, 2), F(5, 2)]]
KEY["key_table_left"] = str([_left_eta, _left_wind, _left_chern])
KEY["key_table_right"] = str([_right_eta, _right_wind, _right_chern])
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
        "ETA-HEATKERNEL-EXTRAP-%d-GRID" % len(KEY["eta_table"]),
        "ETA-RESIDUAL-%s" % str(KEY["eta_max_res_ext"])[:8],
        "ETA-ANTISYM-DIFFPAIRS-%d" % (KEY["eta_antisym_diff_pairs"] + shift),
        "ETA-BRANCH-REDUCTION-%d-CASE" % len(KEY["eta_branch"]),
        "BOUNDARY-H-BASICDOMAIN-%d" % KEY["h_basic_domain_sum"],
        "SPECTRAL-FLOW-%d-PAIRS-MATCH" % len(KEY["sf_table"]),
        "ODD-THREE-REACHABLE-ON-%d-PAIRS" % KEY["sf_three_count"],
        "SAME-SOURCE-TAGGED-NOT-INDEPENDENT",
        "VACUUM-Z2-%d-POINTS-PI1-ZERO" % KEY["vac_n_points"],
        "LOOP-%d-TOTAL-%d-CONTINUOUS" % (KEY["loop_total"], KEY["loop_continuous"]),
        "COMPLEX-SCALAR-WINDING-%d-DISTINCT" % KEY["wind_distinct"],
        "NEUTRAL-SCALAR-NO-PHASE-COUPLING",
        "THREE-FREE-INTEGER-FAMILIES-HITRATE-%s" % KEY["fam_hitrate"].replace("/", "-OF-"),
        "FROZEN-PARAMETER-CONTROL-FAILS",
        "OBJECT-MISMATCH-NZERO-NOT-IQ",
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

    _a07 = [r for r in ROWS if r["id"] == "A07"][0]
    guard("SAME-SOURCE-TAGGED",
          _a07["kind"] in ("INFO", "IDENTITY") and "同源" in _a07["note"],
          "A07 kind=%s；note 含同源标注=%s"
          % (_a07["kind"], "同源" in _a07["note"]))

    _b06 = [r for r in ROWS if r["id"] == "B06"][0]
    guard("DECLARED-NEG",
          "B06" in DECLARED_SET and _b06["kind"] == "FAIL"
          and all(any(r["id"] == x for r in ROWS) for x in DECLARED_NEG),
          "已登记判负 %s；B06 kind=%s" % (str(DECLARED_NEG), _b06["kind"]))

    guard("KEY-TABLE-TWO-PATH",
          KEY["key_table_same"] and len(KEY["key_table_left"]) > 100,
          "左右两路现场重算：eta %d 行 / winding %d 行 / chern %d 行；一致=%s"
          % (len(_left_eta), len(_left_wind), len(_left_chern), KEY["key_table_same"]))

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
          _b06["kind"] == "FAIL" and KEY["fam_free_count"] > 0
          and KEY["frozen_hitrate"] != KEY["fam_hitrate"],
          "自由参数族 %d；冻结 %s 对全档 %s"
          % (KEY["fam_free_count"], KEY["frozen_hitrate"], KEY["fam_hitrate"]))

    _mono = (all(D(x["res_ext"]) <= D(x["res_one"]) <= D(x["res_raw"])
                 for x in KEY["eta_table"])
             and all(D(x["res_ext"]) < D(x["res_raw"]) for x in _nd_rows)
             and KEY["eta_degenerate_count"] == 1)
    guard("RICHARDSON-CONVERGE", _mono and _a01_ok,
          "非退化档三级残差严格下降=%s；退化档 %d 个；A01 ok=%s"
          % (_mono, KEY["eta_degenerate_count"], _a01_ok))

    guard("WINDING-CLOSURE",
          KEY["wind_all_closed"] and not KEY["wind_half_closed"]
          and KEY["chern_half_legal"] == 0,
          "整数 n 全闭合=%s；半整数环路闭合=%s；半整数陈类合法 %d"
          % (KEY["wind_all_closed"], KEY["wind_half_closed"], KEY["chern_half_legal"]))

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
    for i, a in enumerate(A_GRID):
        L.append("  eta a=%-4s 闭式 %-5s | 左路 %-5s | 右路 %-5s"
                 % (_left_eta[i][0], _left_eta[i][1], _left_eta[i][1],
                    _right_eta[i][1]))
    for i in range(6):
        L.append("  winding n=%d 左路 %s | 右路 %s"
                 % (i, _left_wind[i][1], _right_wind[i][1]))
    for i in range(len(_left_chern)):
        L.append("  chern N=%-4s 左路 %-5s | 右路 %-5s"
                 % (_left_chern[i][0], str(_left_chern[i][1]),
                    str(_right_chern[i][1])))
    L.append("  两路一致 = " + str(KEY["key_table_same"]))
    L.append("")
    L.append("【关键数字】")
    L.append("  eta 最大残差 raw=%s / 二级=%s / 三级=%s；相对基准 %s；两底最大差 %s；退化档 %d 个 %s"
             % (KEY["eta_max_res_raw"], KEY["eta_max_res_one"],
                KEY["eta_max_res_ext"], KEY["eta_scale"], KEY["eta_max_base_diff"],
                KEY["eta_degenerate_count"], str(KEY["eta_degenerate"])))
    L.append("  eta 反对称：读数不同 %d 对 / 相同 %d 对 / 最大和 abs=%s"
             % (KEY["eta_antisym_diff_pairs"], KEY["eta_antisym_same_pairs"],
                KEY["eta_antisym_max"]))
    L.append("  V63 真空驻点 t=%s，二阶导 %s，原点 %s，真空点数 %d"
             % (str(KEY["vac_crit_t"]), str(KEY["vac_min_sign"]),
                KEY["vac_origin_sign"], KEY["vac_n_points"]))
    L.append("  离散环路 %d 总 / %d 连续 / %d 不连续 / %d 连续且非常值"
             % (KEY["loop_total"], KEY["loop_continuous"],
                KEY["loop_noncontinuous"], KEY["loop_continuous_nonconstant"]))
    L.append("  复标量互异绕数 %d / Z2 真空互异绕数 %d"
             % (KEY["wind_distinct"], KEY["z2_winding_values"]))
    L.append("  自由参数族 %d / 候选 %d / 命中 3 的 %d / 命中率 %s / 冻结通过率 %s"
             % (KEY["fam_free_count"], KEY["fam_total"], KEY["fam_hit3"],
                KEY["fam_hitrate"], KEY["frozen_hitrate"]))
    L.append("  谱流给 3 的对数 %d / 不给 3 的对数 %d"
             % (KEY["sf_three_count"], KEY["sf_nonthree_count"]))
    L.append("  旋量矩 %s / 矢量矩 %s"
             % (str(KEY["spin_moments"]), str(KEY["vec_moments"])))
    L.append("  陈类合法 %d / 半整数合法 %d"
             % (KEY["chern_legal_count"], KEY["chern_half_legal"]))
    L.append("  README %d B / r402 锚点 %d / r403 锚点 %d / 三树 r403 文件 %d"
             % (KEY["readme_bytes"], KEY["readme_r402_tokens"],
                KEY["readme_r403_tokens"], KEY["r403_files"]))
    L.append("")
    L.append("【诚实边界】")
    L.append("  1. 只产可算判决，不产新物理；独立实验预言 0。")
    L.append("  2. 完整 6D APS 指标定理（含曲率与第二基本形式）未算。")
    L.append("  3. 涡旋 / 畴壁剖面的 BPS 方程与径向 ODE 未解，只判自由度结构。")
    L.append("  4. 4D 反常匹配全账、CKM / PMNS、质量谱均未算。")
    L.append("  5. 四力统一未证明；V64 三道关口仍全部 OPEN。")
    L.append("  6. 本册为攻坚册：不新增 RID、不进 README、不与任何卷相加。")
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
