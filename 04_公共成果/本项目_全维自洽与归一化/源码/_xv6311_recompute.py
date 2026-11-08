# -*- coding: utf-8 -*-
"""攻坚 X-V63-11：涡旋能量泛函与 BPS 剖面能否让能量最小化选 n=3（独立机核 · 部件 1/3）。

体例：跨卷攻坚册 —— 不新增 RID、不进 README 登记位、条目不与任何卷相加。
来料：无外部来料；输入为 X-V63-10 §十二 OPEN 表的 X-V63-11，以及 X-V63-6 的
      绕数器 / 判别力 0 结论、X-V63-1 的陈类整数性口径。
对象：单组分 U(1) Abelian-Higgs 涡旋、临界耦合 beta=1、径向试探剖面。
红线：数学自洽 ≠ 实验证实；只产可算判决，不产新物理；独立实验预言数 0。
纪律：判据反噬自己 + 正负双对照；守卫 ok 禁写死；定义恒等式记 IDENTITY；
      对象错位必须写进变量名；读数支持不了的解读不得写成结论。
"""
import os
import io
import json
import ast
import math
import glob
from fractions import Fraction as F

TITLE = "攻坚 X-V63-11 独立机核"
DATE = "2026-11-08"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "数据")
JS = os.path.join(DATA, "_XV6311_recompute_2026-11-08.json")
RPT = os.path.join(DATA, "_XV6311_recompute_report_2026-11-08.txt")
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
    print("  [GUARD %-4s] %-22s | %s" % ("ok" if ok else "BAD", name, detail))
    return bool(ok)


def fmt_f(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else "%d/%d" % (q.numerator, q.denominator)


def is_int(q):
    return F(q).denominator == 1


print("=" * 78)
print(TITLE + "  " + DATE)
print("=" * 78)
print("\n[GUARD] 工具自检（精确有理数层，不依赖数值引擎）")
guard("FRAC-EXACT", F(1, 3) + F(1, 6) - F(1, 2) == 0, "1/3+1/6-1/2 = 0")
guard("RATIONAL-CLAMP-EXACT",
      F(3, 2) > F(1, 2) + F(1, 25) and not (F(1, 2) > F(1, 2) + F(1, 25)),
      "L(3)=3/2 大于 0.54 而上界侧 L(1)=1/2 不大于；两侧都测")

# ---------------------------------------------------------------- 数值引擎
# 径向 Abelian-Higgs 能量（已除以 2*pi），B = n*a'/r：
#   E/(2*pi) = int r dr [ B^2/2 + f'^2/2 + n^2 (1-a)^2 f^2/(2 r^2)
#                          + beta (1-f^2)^2/8 ]
# Bogomolny 平方和（beta=1 时与上式逐项配平）：
#   E/(2*pi) = boundary(R) + S,  S >= 0,
#   boundary(R) = n*sqrt(beta)/2 * [ (1-a)(1-f^2) ]_{r=R}^{r=0}
# 对试探剖面 (1-a)(1-f^2) = (alpha^2/(r^2+alpha^2))^2。
# ★ R 有限时 boundary(R) 不等于 n/2；漏掉修正会产生约 1e-7 的假残差。
R_CUT = 60.0
N_SIMPSON = 4000
ALPHA_GRID = (0.5, 1.0, 1.5, 2.0, 3.0)
BETA_GRID = (0.25, 0.5, 1.0, 2.0, 4.0)
N_GRID_LOWER = (1, 2, 3, 4, 8)
N_GRID_CLAMP = list(range(1, 9))
TAIL_GRID = (20.0, 40.0, 60.0, 100.0)
SIMPSON_GRID = (1000, 2000, 4000, 8000)
DISCRETE_GRID = (100, 200, 400, 800, 1600)
LAMBDA_GRID = (F(0), F(1, 8), F(1, 4), F(1, 2), F(3, 4), F(1))


def simpson(fn, a, b, n):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = fn(a) + fn(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * fn(a + i * h)
    return s * h / 3.0


# Simpson 1/3 自检：用精确有理数，不设任何 10 的幂门限。
# 二次多项式误差须精确为 0（定义性质）；四次多项式误差须非零，
# 且网格加密一倍后误差恰好缩小 16 倍（h^4 收敛，闭式为 -4h^4/15）。
def simpson_frac(fn, a, b, n):
    h = F(b - a, n)
    s = fn(F(a)) + fn(F(b))
    for i in range(1, n):
        s += (4 if i % 2 else 2) * fn(F(a) + i * h)
    return s * h / F(3)


_sq2 = simpson_frac(lambda x: x * x, 0, 2, 40)
_sq4 = simpson_frac(lambda x: x ** 4, 0, 2, 40)
_sq4_fine = simpson_frac(lambda x: x ** 4, 0, 2, 80)
_e4 = F(32, 5) - _sq4
_e4_fine = F(32, 5) - _sq4_fine
guard("SIMPSON-SELFTEST",
      _sq2 == F(8, 3) and _e4 != 0 and _e4 / _e4_fine == 16,
      "int_0^2 x^2 误差 0；int_0^2 x^4 误差 %s 与 %s，比值 %s（须为 16）"
      % (str(_e4), str(_e4_fine), str(_e4 / _e4_fine)))


def simpson_N(R):
    """尾截断放大 R 时同步加密网格，使步长不超过 R=60 的基准步长。"""
    n = max(N_SIMPSON, int(N_SIMPSON * R / 60.0))
    return n + (n % 2)


def profile(r, alpha):
    d = r * r + alpha * alpha
    f = r / math.sqrt(d)
    a = r * r / d
    fp = alpha * alpha / (d ** 1.5)
    ap = 2.0 * r * alpha * alpha / (d * d)
    return f, a, fp, ap


def E_trial(n, alpha, beta, R, N):
    """显式试探剖面给出的严格能量上界（任意剖面能量都不低于真实最小值）。"""
    def dens(r):
        if r <= 0.0:
            return 0.0
        f, a, fp, ap = profile(r, alpha)
        B = n * ap / r
        return r * (B * B / 2.0 + fp * fp / 2.0
                    + n * n * (1.0 - a) ** 2 * f * f / (2.0 * r * r)
                    + beta * (1.0 - f * f) ** 2 / 8.0)
    return simpson(dens, 0.0, R, N)


def S_res(n, alpha, beta, R, N):
    """Bogomolny 平方和残差 S >= 0；sqrt(beta) 放进第一项。"""
    sb = math.sqrt(beta)
    def dens(r):
        if r <= 0.0:
            return 0.0
        f, a, fp, ap = profile(r, alpha)
        B = n * ap / r
        return r * ((B - sb * (1.0 - f * f) / 2.0) ** 2 / 2.0
                    + (fp - n * (1.0 - a) * f / r) ** 2 / 2.0)
    return simpson(dens, 0.0, R, N)


def boundary_term(n, alpha, beta, R):
    """有限 R 的边界项；R -> 无穷时趋于 n*sqrt(beta)/2。"""
    sb = math.sqrt(beta)
    gR = (alpha * alpha / (R * R + alpha * alpha)) ** 2
    return n * sb / 2.0 * (1.0 - gR)


def discrete_energy(n, alpha, beta, R, N):
    """与 _probe_xv6311.py 相同的中点差分格式，但剖面固定、不做变分。"""
    h = R / N
    f = [0.0] * (N + 1)
    a = [0.0] * (N + 1)
    for i in range(N + 1):
        r = i * h
        if r > 0.0:
            f[i], a[i], _, _ = profile(r, alpha)
    t = 0.0
    for j in range(N):
        r = (j + 0.5) * h
        fp = (f[j + 1] - f[j]) / h
        ap = (a[j + 1] - a[j]) / h
        fm = 0.5 * (f[j] + f[j + 1])
        am = 0.5 * (a[j] + a[j + 1])
        t += r * h * (n * n * ap * ap / (2.0 * r * r) + fp * fp / 2.0
                      + n * n * (1.0 - am) ** 2 * fm * fm / (2.0 * r * r)
                      + beta * (1.0 - fm * fm) ** 2 / 8.0)
    return t


def n_min_of_lambda(lam, ns=N_GRID_CLAMP):
    """E_lam(n) = n/2 + lam*(n-3)^2 的最小能量涡旋数；精确有理数。"""
    vals = [(n, F(n, 2) + lam * (n - 3) ** 2) for n in ns]
    m = min(v[1] for v in vals)
    return [n for n, v in vals if v == m], m

# ---------------------------------------------------------------- A 层读数
# A: 平方和两路相符（5 档 alpha），并显式记录漏边界项的假残差。
KEY["alpha_table"] = []
for _al in ALPHA_GRID:
    _e = E_trial(1, _al, 1.0, R_CUT, N_SIMPSON)
    _s = S_res(1, _al, 1.0, R_CUT, N_SIMPSON)
    _b = boundary_term(1, _al, 1.0, R_CUT)
    KEY["alpha_table"].append({
        "alpha": _al, "E": _e, "S": _s, "boundary": _b,
        "res_corrected": abs(_e - _b - _s),
        "res_naive": abs(_e - 0.5 - _s),
    })
KEY["alpha_max_res_corrected"] = max(x["res_corrected"] for x in KEY["alpha_table"])
KEY["alpha_max_res_naive"] = max(x["res_naive"] for x in KEY["alpha_table"])

# A: 有限 R 边界修正，四档 R。
KEY["tail_boundary_table"] = []
for _R in TAIL_GRID:
    _N = simpson_N(_R)
    _e = E_trial(1, 1.5, 1.0, _R, _N)
    _s = S_res(1, 1.5, 1.0, _R, _N)
    _b = boundary_term(1, 1.5, 1.0, _R)
    KEY["tail_boundary_table"].append({
        "R": _R, "N": _N, "E": _e, "S": _s, "boundary": _b,
        "res_corrected": abs(_e - _b - _s),
        "res_naive": abs(_e - 0.5 - _s),
        "missing": 0.5 - _b,
    })
KEY["boundary_R60_missing"] = [x for x in KEY["tail_boundary_table"] if x["R"] == 60.0][0]["missing"]

# A: beta 配平性。交叉项系数 sqrt(beta)/2 与 1/2 只有在 beta=1 相等。
KEY["beta_table"] = []
for _be in BETA_GRID:
    _e = E_trial(1, 1.5, _be, R_CUT, N_SIMPSON)
    _s = S_res(1, 1.5, _be, R_CUT, N_SIMPSON)
    _b = boundary_term(1, 1.5, _be, R_CUT)
    KEY["beta_table"].append({
        "beta": _be, "E": _e, "mismatch": abs(_e - _b - _s),
        "coef": math.sqrt(_be) / 2.0,
    })
KEY["beta_flat_count"] = sum(1 for x in KEY["beta_table"]
                             if abs(x["mismatch"]) < 1e-7)
KEY["beta_bad_min"] = min(x["mismatch"] for x in KEY["beta_table"]
                          if x["beta"] != 1.0)
KEY["beta_mismatch_b1"] = [x for x in KEY["beta_table"] if x["beta"] == 1.0][0]["mismatch"]

# A: L(n) = n/2 在 5 档 n 上由两路相符给出（S >= 0 是结构性的，不是拟合）。
KEY["lower_bound_table"] = []
for _n in N_GRID_LOWER:
    _e = E_trial(_n, 1.5, 1.0, R_CUT, N_SIMPSON)
    _s = S_res(_n, 1.5, 1.0, R_CUT, N_SIMPSON)
    _b = boundary_term(_n, 1.5, 1.0, R_CUT)
    KEY["lower_bound_table"].append({
        "n": _n, "L": _n / 2.0, "E": _e, "S": _s,
        "boundary": _b, "res": abs(_e - _b - _s),
        "S_nonneg": _s >= 0.0,
    })
KEY["lower_max_res"] = max(x["res"] for x in KEY["lower_bound_table"])
KEY["lower_all_S_nonneg"] = all(x["S_nonneg"] for x in KEY["lower_bound_table"])

# A: 显式上界 U(1)：五档 alpha 里取最小；与探算 b 版一致。
_best = min(KEY["alpha_table"], key=lambda x: x["E"])
KEY["alpha_best"] = _best["alpha"]
KEY["U1"] = _best["E"]
KEY["U1_S"] = _best["S"]
KEY["L1"] = 0.5
KEY["L3"] = 1.5
KEY["clamp_gap_L3_minus_U1"] = KEY["L3"] - KEY["U1"]
KEY["three_U1"] = 3.0 * KEY["U1"]
KEY["split_overlap"] = KEY["three_U1"] > KEY["L3"]

# A: 数值收敛（Simpson 网格 + 尾截断）。
KEY["simpson_grid"] = [(n, E_trial(1, KEY["alpha_best"], 1.0, R_CUT, n))
                       for n in SIMPSON_GRID]
KEY["simpson_deltas"] = [abs(KEY["simpson_grid"][i + 1][1] - KEY["simpson_grid"][i][1])
                         for i in range(len(KEY["simpson_grid"]) - 1)]
KEY["simpson_delta_shrinks"] = all(KEY["simpson_deltas"][i + 1] < KEY["simpson_deltas"][i]
                                   for i in range(len(KEY["simpson_deltas"]) - 1))
KEY["tail_grid"] = [(r, E_trial(1, KEY["alpha_best"], 1.0, r, N_SIMPSON))
                    for r in TAIL_GRID]
KEY["tail_deltas"] = [abs(KEY["tail_grid"][i + 1][1] - KEY["tail_grid"][i][1])
                      for i in range(len(KEY["tail_grid"]) - 1)]
KEY["tail_delta_shrinks"] = all(KEY["tail_deltas"][i + 1] < KEY["tail_deltas"][i]
                                for i in range(len(KEY["tail_deltas"]) - 1))

# B: 夹逼表 n=1..8。范围外第一条（n=1）必须不成立，否则是恒真谓词。
KEY["clamp_table"] = [{"n": n, "L": n / 2.0, "gt_U1": n / 2.0 > KEY["U1"]}
                      for n in N_GRID_CLAMP]
KEY["clamp_true_count"] = sum(1 for x in KEY["clamp_table"] if x["gt_U1"])
KEY["clamp_n1_false"] = not KEY["clamp_table"][0]["gt_U1"]

# C: 自由参数族。lambda 是输入；冻结一档会给出 1/1 的假绿。
KEY["lambda_table"] = []
for _lam in LAMBDA_GRID:
    _arg, _m = n_min_of_lambda(_lam)
    KEY["lambda_table"].append({
        "lambda": fmt_f(_lam), "n_min": _arg,
        "unique": len(_arg) == 1, "E1": fmt_f(F(1, 2) + _lam * 4),
        "E3": fmt_f(F(3, 2)),
    })
KEY["lambda_total"] = len(KEY["lambda_table"])
KEY["lambda_hit3_unique"] = sum(1 for x in KEY["lambda_table"]
                                if x["n_min"] == [3])
KEY["lambda_hit3_including_tie"] = sum(1 for x in KEY["lambda_table"]
                                       if 3 in x["n_min"])
KEY["lambda_hitrate"] = "%d/%d" % (KEY["lambda_hit3_unique"], KEY["lambda_total"])
KEY["lambda_frozen"] = "1/1"
KEY["lambda_tie_count"] = sum(1 for x in KEY["lambda_table"] if not x["unique"])
KEY["lambda_zero_nmin"] = KEY["lambda_table"][0]["n_min"]
KEY["lambda_threequarters_nmin"] = [x["n_min"] for x in KEY["lambda_table"]
                                    if x["lambda"] == "3/4"][0]

# C: 离散格式（固定剖面）收敛；变分探算发散只记为被弃用的外部读数。
KEY["discrete_grid"] = [(n, discrete_energy(1, 1.5, 1.0, 18.0, n))
                        for n in DISCRETE_GRID]
KEY["discrete_deltas"] = [abs(KEY["discrete_grid"][i + 1][1] - KEY["discrete_grid"][i][1])
                          for i in range(len(KEY["discrete_grid"]) - 1)]
KEY["discrete_delta_shrinks"] = all(KEY["discrete_deltas"][i + 1] < KEY["discrete_deltas"][i]
                                    for i in range(len(KEY["discrete_deltas"]) - 1))
KEY["variational_probe_divergent_sequence"] = "1.57390409 / 1.91680342 / 2.30388291"
KEY["variational_probe_object"] = "外部探算 _probe_xv6311.py 的变分最小化 E(3)"

# C: 回代 X-V63-10 B09 / X-V63-6 / X-V63-1，两个对象不相加。
KEY["cluster_total_wind"] = 3
KEY["cluster_count_multi"] = 3
KEY["cluster_count_single"] = 1
KEY["cluster_diff_count"] = KEY["cluster_count_multi"] - KEY["cluster_count_single"]
_iq_int_solutions = [(p, q) for p in range(-8, 9) for q in range(-8, 9)
                     if 2 * (p + q) == 3]
KEY["iq_three_solutions"] = len(_iq_int_solutions)

# 跨册回代：X-V63-10 的读数由该册机核 JSON 反抄，不手填、不重数条目。
_PREV_JS = os.path.join(DATA, "_XV6310_recompute_2026-11-08.json")
_PREV = json.load(io.open(_PREV_JS, "r", encoding="utf-8"))
KEY["prev_center_all_orders"] = list(_PREV["key_numbers"]["center_all_orders"])
KEY["prev_zk_table"] = [(int(x["k"]), int(x["n_min"]))
                        for x in _PREV["key_numbers"]["zk_table"]]
KEY["prev_internal_fixers_count"] = int(_PREV["key_numbers"]["internal_fixers_count"])
KEY["prev_rid"] = str(_PREV.get("rid", ""))

# 唯一真判负：能量最小化能否由理论内部（不新增参数）把 n 定为 3。
# 三条路径逐一真算；每条的「是否固定 3」判据都由本册/上一册读数驱动。
KEY["energy_fixers"] = []
# 路径 1：原始能量夹逼。若 L(3) < U(1) 则能量层会选 3；实测相反。
if KEY["clamp_gap_L3_minus_U1"] < 0:
    KEY["energy_fixers"].append("原始能量夹逼")
# 路径 2：BPS 线性简并。若 3*L(1) 严格小于 L(3) 才算给出偏好；实测相等。
_bps_3L1 = 3.0 * KEY["L1"]
_bps_L3 = KEY["L3"]
if _bps_3L1 < _bps_L3 - 1e-12:
    KEY["energy_fixers"].append("BPS 线性")
# 路径 3：离散投影 Z_k。若 3 阶元由群中心内部给出才算固定；反抄读数里没有 3。
if 3 in KEY["prev_center_all_orders"]:
    KEY["energy_fixers"].append("离散投影 Z_k")
KEY["bps_3L1"] = _bps_3L1
KEY["bps_L3"] = _bps_L3
KEY["bps_degenerate"] = abs(_bps_3L1 - _bps_L3) < 1e-12
KEY["zk_hit3_from_prev"] = [k for k, nmin in KEY["prev_zk_table"] if nmin == 3]
KEY["energy_fixers_count"] = len(KEY["energy_fixers"])
KEY["energy_fix_paths"] = 3
KEY["energy_fix_path_names"] = ["原始能量夹逼", "BPS 线性简并", "离散投影 Z_k"]

# ---------------------------------------------------------------- README 体检
_rb = io.open(RD, "rb").read()
KEY["readme_bytes"] = len(_rb)
KEY["readme_r402_tokens"] = _rb.count(b"TUFT-r402_")
KEY["readme_r403_tokens"] = _rb.count(b"TUFT-r403_")
KEY["r403_files"] = len(glob.glob(os.path.join(ROOT, "**", "*TUFT-r403_*"), recursive=True))


print("\n[ROWS] A 层：Bogomolny 严格下界与数值口径")
_a01_ok = (KEY["alpha_max_res_corrected"] < 1e-6
           and len(KEY["alpha_table"]) == len(ALPHA_GRID)
           and all(x["E"] >= x["boundary"] - 1e-9 for x in KEY["alpha_table"]))
add("A01", "A", "平方和恒等式两路相符：E = boundary(R) + S",
    "五档 alpha 上直接积分与平方和加边界项须逐档相符，且 S 非负",
    "五档修正后残差 %s；最大 %.3e；直接能量均不小于边界项"
    % (["%.3e" % x["res_corrected"] for x in KEY["alpha_table"]],
       KEY["alpha_max_res_corrected"]),
    _a01_ok, "下界不是拟合出来的：S 是两个平方的积分，结构性非负")

_alpha15 = [x for x in KEY["alpha_table"] if x["alpha"] == 1.5][0]
_a02_ok = (all(x["res_corrected"] < x["res_naive"] for x in KEY["tail_boundary_table"])
           and KEY["boundary_R60_missing"] > 1e-8
           and len(KEY["tail_boundary_table"]) == len(TAIL_GRID))
add("A02", "A", "有限截断 R 的边界修正不可漏，漏项会造假残差",
    "四档 R 上带修正的残差须逐档小于当作 n/2 的朴素残差",
    "R=60 漏项 %.3e；alpha=1.5 时朴素残差 %.3e 对修正后残差 %.3e；四档修正全更小=%s"
    % (KEY["boundary_R60_missing"], _alpha15["res_naive"],
       _alpha15["res_corrected"],
       all(x["res_corrected"] < x["res_naive"] for x in KEY["tail_boundary_table"])),
    _a02_ok, "残差不随网格下降时先怀疑闭式少项，而不是放宽门限")

_a03_ok = (KEY["beta_flat_count"] == 1
           and KEY["beta_bad_min"] > 1e-2
           and KEY["beta_mismatch_b1"] < 1e-7
           and len(KEY["beta_table"]) == len(BETA_GRID))
add("A03", "A", "Bogomolny 配平方只在 beta=1 成立，这是口径边界不是结论",
    "五档 beta 中恰一档失配小于 1e-7，其余失配须大于 1e-2",
    "失配表 %s；配平 %d 档；非 1 档最小失配 %.6f；beta=1 失配 %.3e"
    % ([(x["beta"], round(x["mismatch"], 9)) for x in KEY["beta_table"]],
       KEY["beta_flat_count"], KEY["beta_bad_min"], KEY["beta_mismatch_b1"]),
    _a03_ok, "交叉项系数 sqrt(beta)/2 与 1/2 只在 beta=1 相等；beta 不等于 1 的档本册不判")

_a04_ok = (KEY["lower_max_res"] < 1e-6 and KEY["lower_all_S_nonneg"]
           and len(KEY["lower_bound_table"]) == len(N_GRID_LOWER)
           and all(abs(x["L"] - x["n"] / 2.0) < 1e-12 for x in KEY["lower_bound_table"]))
add("A04", "A", "严格下界 L(n)=n/2 在五档 n 上由两路相符给出",
    "S 须逐档非负，且 E 减边界项减 S 的残差须小于 1e-6",
    "五档 %s；最大残差 %.3e；S 全非负=%s"
    % ([(x["n"], x["L"], round(x["S"], 9)) for x in KEY["lower_bound_table"]],
       KEY["lower_max_res"], KEY["lower_all_S_nonneg"]),
    _a04_ok, "这是本册唯一能称为严格的能量下界；不依赖 BPS 方程解出没有")

_a05_ok = (KEY["alpha_best"] in ALPHA_GRID
           and KEY["U1"] > KEY["L1"]
           and KEY["U1"] < KEY["L1"] + 0.1
           and KEY["U1"] == min(x["E"] for x in KEY["alpha_table"]))
add("A05", "A", "显式试探剖面给出 n=1 的严格能量上界 U(1)",
    "五档 alpha 取最小，且 U(1) 须落在 L(1) 与 L(1)+0.1 之间",
    "最优 alpha %.2f；U(1) %.9f；L(1) %.1f；超出下界 %.9f"
    % (KEY["alpha_best"], KEY["U1"], KEY["L1"], KEY["U1"] - KEY["L1"]),
    _a05_ok, "任意剖面的能量都是真实最小值的上界，故 U(1) 不小于 E(1)")

_a06_ok = (KEY["simpson_delta_shrinks"] and KEY["tail_delta_shrinks"]
           and len(KEY["simpson_grid"]) == 4 and len(KEY["tail_grid"]) == 4
           and KEY["simpson_deltas"][-1] < 1e-8)
add("A06", "A", "Simpson 网格与尾截断双向收敛",
    "四档网格与四档截断的相邻差须逐档缩小，最细网格差小于 1e-8",
    "网格 %s；相邻差 %s；截断 %s；相邻差 %s"
    % ([(n, round(v, 10)) for n, v in KEY["simpson_grid"]],
       ["%.3e" % d for d in KEY["simpson_deltas"]],
       [(r, round(v, 10)) for r, v in KEY["tail_grid"]],
       ["%.3e" % d for d in KEY["tail_deltas"]]),
    _a06_ok, "步长自适应与量级 sanity 同时做；尾截断差随 R 递减")

add("A07", "A", "与临界耦合 BPS 涡旋的标准结论一致，但本册读数是平方和实算所得",
    "同源一致性不得冒充独立证据",
    "本册独立实算 %d 档 alpha、%d 档 n、%d 档 beta；教科书结论仅作对照，不单列 PASS"
    % (len(KEY["alpha_table"]), len(KEY["lower_bound_table"]), len(KEY["beta_table"])),
    None, "同源回验抓不到同源错误；显式标注，由 SAME-SOURCE-TAGGED 守卫强制")

add("A08", "A", "交叉项系数 sqrt(beta)/2 与 f-prime 侧系数 1/2 的相等是配平方的规定",
    "展开后无残差可算，按定义恒等式纪律不记 PASS",
    "beta=1 时两系数同为 0.5；beta 不等于 1 时失配由 A03 真算出",
    "ID", "配 NOT-ALL-GREEN 守卫防首跑全绿；恒等式不提供判别力")

_a09_ok = (KEY["discrete_delta_shrinks"]
           and len(KEY["discrete_grid"]) == len(DISCRETE_GRID)
           and KEY["discrete_deltas"][-1] < 1e-5)
add("A09", "A", "固定剖面的离散格式确实收敛，故发散不来自被积函数",
    "五档网格的相邻差须逐档缩小且末档差小于 1e-5",
    "离散序列 %s；相邻差 %s"
    % ([(n, round(v, 10)) for n, v in KEY["discrete_grid"]],
       ["%.3e" % d for d in KEY["discrete_deltas"]]),
    _a09_ok, "与变分探算的发散读数属于两个对象，不相加；见 C05 与 D04")

print("\n[ROWS] B 层：严格夹逼、判别力边界与唯一真判负")
_b01_ok = (KEY["clamp_gap_L3_minus_U1"] > 0
           and KEY["L3"] > KEY["U1"] > KEY["L1"]
           and KEY["lower_all_S_nonneg"])
add("B01", "B", "严格夹逼：E(3) 不小于 L(3)=3/2，而 U(1) 小于 3/2",
    "L(3) 减 U(1) 须严格为正，且 U(1) 须大于 L(1) 才不是平凡",
    "L(3)=%.9f；U(1)=%.9f；L(1)=%.9f；夹逼间隙 %.9f"
    % (KEY["L3"], KEY["U1"], KEY["L1"], KEY["clamp_gap_L3_minus_U1"]),
    _b01_ok, "由 E(3) >= L(3) > U(1) >= E(1) 得 E(3) > E(1)，无需解任何 ODE")

_b02_ok = (KEY["clamp_true_count"] == 7 and KEY["clamp_n1_false"]
           and len(KEY["clamp_table"]) == 8)
add("B02", "B", "n=2..8 全部被夹逼排除，范围外第一条 n=1 不成立",
    "八档中恰七档成立，且第一档必须不成立",
    "夹逼表 %s；成立 %d/8；n=1 不成立=%s"
    % ([(x["n"], x["L"], x["gt_U1"]) for x in KEY["clamp_table"]],
       KEY["clamp_true_count"], KEY["clamp_n1_false"]),
    _b02_ok, "范围内全对必须报范围外第一条就错；七档全过的谓词单独看判别力为 0")

_b03_ok = (KEY["bps_degenerate"] and KEY["bps_3L1"] == KEY["bps_L3"]
           and KEY["cluster_diff_count"] == 2)
add("B03", "B", "临界耦合下 3 个 n=1 与 1 个 n=3 的 BPS 能量简并",
    "三倍 L(1) 须等于 L(3)，且两个构型的缺陷数读数须不同",
    "3 乘 L(1)=%.9f 对 L(3)=%.9f；简并=%s；缺陷数 %d 对 %d，差 %d"
    % (KEY["bps_3L1"], KEY["bps_L3"], KEY["bps_degenerate"],
       KEY["cluster_count_multi"], KEY["cluster_count_single"],
       KEY["cluster_diff_count"]),
    _b03_ok, "能量线性只说明 BPS 饱和，不说明哪个构型被选中")

_b04_ok = (KEY["split_overlap"] and KEY["three_U1"] > KEY["L3"]
           and KEY["three_U1"] - KEY["L3"] > 1e-2)
add("B04", "B", "读数支持不了的解读：夹逼不能判定分裂成 3 个 n=1 是否有利",
    "上界侧 3 乘 U(1) 须大于 L(3)，使两个能量区间重叠",
    "E(1) 区间 [%.9f, %.9f]；3 乘 E(1) 上界 %.9f；E(3) 下界 %.9f；重叠=%s"
    % (KEY["L1"], KEY["U1"], KEY["three_U1"], KEY["L3"], KEY["split_overlap"]),
    _b04_ok, "把 3 乘 U(1) 当成 3 乘 E(1) 会算出 1 个 n=3 更省，那是用上界当下界")

_b05_ok = (KEY["lambda_total"] == 6 and KEY["lambda_hit3_unique"] == 2
           and KEY["lambda_hit3_including_tie"] == 3
           and KEY["lambda_frozen"] != KEY["lambda_hitrate"]
           and KEY["lambda_tie_count"] == 1)
add("B05", "B", "加一项 lambda 乘 (n-3) 的平方即可让能量最小选 3，但 lambda 是输入",
    "六档 lambda 须给不同 n_min，命中 3 的档数与冻结一档的读数须不同",
    "n_min 表 %s；唯一命中 3 的 %s；含并列 %d 档；并列档 %d；冻结 %s"
    % ([(x["lambda"], x["n_min"]) for x in KEY["lambda_table"]],
       KEY["lambda_hitrate"], KEY["lambda_hit3_including_tie"],
       KEY["lambda_tie_count"], KEY["lambda_frozen"]),
    _b05_ok, "自由度从 n 转移到 lambda，与 X-V63-10 的 n 转移到 k 同族")

_b06_ok = (KEY["energy_fixers_count"] > 0)
add("B06", "B", "唯一真判负：能量最小化能否由理论内部把 n 固定为 3",
    "须存在不依赖新输入的内部机制把 n 定为 3",
    "%d 条路径中内部固定机制 %d 个 %s；夹逼间隙 %.9f；BPS 简并=%s；中心阶 %s；Z_k 命中 3 的 k=%s 是输入"
    % (KEY["energy_fix_paths"], KEY["energy_fixers_count"],
       str(KEY["energy_fixers"]), KEY["clamp_gap_L3_minus_U1"],
       KEY["bps_degenerate"], KEY["prev_center_all_orders"],
       str(KEY["zk_hit3_from_prev"])),
    _b06_ok, "判负已登记；问的是「是否存在」，故 ok 由机制个数大于零驱动")

_b07_ok = (KEY["lambda_zero_nmin"] != KEY["lambda_threequarters_nmin"]
           and KEY["lambda_zero_nmin"] == [1]
           and KEY["lambda_threequarters_nmin"] == [3])
add("B07", "B", "负对照：lambda=0 给 n_min=1，lambda=3/4 给 n_min=3",
    "两档须给出两个不同读数",
    "lambda=0 的 n_min %s；lambda=3/4 的 n_min %s"
    % (KEY["lambda_zero_nmin"], KEY["lambda_threequarters_nmin"]),
    _b07_ok, "证明判据测的确实是换了参数，而不是算出一个固定值")

_b08_ok = (KEY["lambda_tie_count"] == 1
           and [x["n_min"] for x in KEY["lambda_table"] if x["lambda"] == "1/2"] == [[2, 3]])
add("B08", "B", "lambda=1/2 给并列最小，退化重复不等于多解",
    "并列档须恰一档，且并列读数须同时含 2 与 3",
    "并列档数 %d；lambda=1/2 的 n_min %s"
    % (KEY["lambda_tie_count"],
       [x["n_min"] for x in KEY["lambda_table"] if x["lambda"] == "1/2"]),
    _b08_ok, "显式报零的个数与并列个数，避免把简并读成两个解")

_b09_ok = (KEY["zk_hit3_from_prev"] == [3]
           and 3 not in KEY["prev_center_all_orders"]
           and KEY["prev_internal_fixers_count"] == 0
           and KEY["prev_rid"] == "NONE-NO-RID")
add("B09", "B", "离散投影回代：k=3 给 n_min=3，但 k 与 lambda 都是新输入",
    "反抄读数须给 k=3、中心阶不含 3、上一册内部固定机制 0",
    "Z_k 命中 3 的 k %s；中心全部元素阶 %s；上一册内部固定机制 %d；上一册 rid %s"
    % (KEY["zk_hit3_from_prev"], KEY["prev_center_all_orders"],
       KEY["prev_internal_fixers_count"], KEY["prev_rid"]),
    _b09_ok, "跨册读数只作输入回代，不与本册条目相加")

print("\n[ROWS] C 层：对象边界与回代")
add("C01", "C", "回代 X-V63-10 B09：3 个 n=1 与 1 个 n=3 总绕数同为 3",
    "上一册的缺陷数差只作输入，不重数条目",
    "总绕数 %d；缺陷数 %d 对 %d，差 %d；本册新增的是能量层读数，两者不相加"
    % (KEY["cluster_total_wind"], KEY["cluster_count_multi"],
       KEY["cluster_count_single"], KEY["cluster_diff_count"]),
    None, "拓扑层与能量层是两个对象")

add("C02", "C", "回代 X-V63-6：V63 实标量真空离散使 pi_1=0，无拓扑涡旋",
    "本册能量泛函须新增带电复标量，属于新输入",
    "上一册 256 个离散环路中连续且非常值 0 个；本册单组分 U(1) 涡旋是新增设定",
    None, "若把能量层判决读成 V63 原模型的结论就是对象错位")

_chern_table = [(fmt_f(F(n)), n % 1 == 0) for n in (F(1), F(2), F(3),
                                                     F(1, 2), F(3, 2), F(5, 2))]
_c03_ok = (KEY["iq_three_solutions"] == 0
           and sum(1 for _, legal in _chern_table if legal) == 3
           and sum(1 for _, legal in _chern_table if not legal) == 3)
add("C03", "C", "整数网格 I_Q=3 解 0 个，与绕数层不相加",
    "整数网格解须为 0，且整数磁通合法 3 档、半整数 0 档",
    "I_Q=3 解 %d；磁通合法表 %s"
    % (KEY["iq_three_solutions"], _chern_table),
    _c03_ok, "可达的 wind=3 不等于 I_Q=3；两个读数不互相替代")

_c04_ok = (KEY["prev_center_all_orders"] == [1, 2, 4]
           and KEY["prev_internal_fixers_count"] == 0
           and KEY["prev_rid"] == "NONE-NO-RID")
add("C04", "C", "跨册读数由上一册机核 JSON 反抄，不手填",
    "反抄的三项须与上一册判定一致",
    "中心阶 %s；内部固定机制 %d；rid %s；来源 _XV6310_recompute_2026-11-08.json"
    % (KEY["prev_center_all_orders"], KEY["prev_internal_fixers_count"],
       KEY["prev_rid"]),
    _c04_ok, "读数来自引擎输出而非记忆；上一册条目不与本册相加")

_c05_ok = (KEY["discrete_delta_shrinks"] and KEY["variational_probe_object"] != "")
add("C05", "C", "变分探算与固定剖面是两个对象：前者发散，后者收敛",
    "固定剖面序列须收敛，变分侧只记录弃用决定不冒充证据",
    "固定剖面相邻差 %s 递减；变分侧 %s 单调递增故弃用"
    % (["%.3e" % d for d in KEY["discrete_deltas"]],
       KEY["variational_probe_divergent_sequence"]),
    _c05_ok, "变分侧是外部探算输出，本册机核未重算，D04 显式标注不作证据")

_c06_ok = (sum(1 for _, legal in _chern_table if legal) == 3
           and sum(1 for _, legal in _chern_table if not legal) == 3)
add("C06", "C", "能量最小化不改变陈类整数性约束",
    "整数磁通合法 3 档、半整数合法 0 档",
    "磁通表 %s；整数合法 3、半整数合法 0"
    % (_chern_table,),
    _c06_ok, "与 X-V63-1 同口径；能量层结论不松绑拓扑层条件")

print("\n[ROWS] D 层：诚实边界与不相加声明")
add("D01", "D", "本册不产新物理",
    "只产可算判决，独立实验预言数须为 0",
    "未构造新作用量、未给新粒子、未给可检验数值；独立预言 0",
    None, "数学自洽不等于实验证实")
add("D02", "D", "与 X-V63-10 / X-V63-6 / X-V63-1 / V63 不相加",
    "前册读数只作输入回代",
    "本册 34 条独立复算，不与前册 34 / 32 / 27 / 31 条相加",
    None, "C01 / C02 / C04 显式声明口径回代")
add("D03", "D", "严格结论的覆盖口径",
    "只覆盖单组分 U(1) Abelian-Higgs、临界耦合 beta=1、径向试探剖面",
    "beta 不等于 1 时平方和不配平（A03）；多组分、非 Abel 涡旋、引力、超对称、theta 项均未算",
    None, "不声称任何能量泛函都不可能选出 3")
add("D04", "D", "变分探算已弃用，其读数不作证据",
    "外部探算网格细化下发散，未在本册机核重算",
    "对象 %s；序列 %s 单调递增；本册只用它说明弃用决定"
    % (KEY["variational_probe_object"],
       KEY["variational_probe_divergent_sequence"]),
    None, "外部探算、未重算、不作证据；三项标注缺一不可")
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
_k1_exp = "%.9e" % _alpha15["res_naive"]
_k1_act = "%.9e" % _alpha15["res_corrected"]
_k1_ok = (_alpha15["res_corrected"] < _alpha15["res_naive"] and _k1_exp != _k1_act)
add("K1", "K", "漏掉有限 R 边界项的负控",
    "朴素残差 " + _k1_exp,
    "带修正残差 " + _k1_act,
    _k1_ok, "两者相差约两个量级，是闭式少项不是数值误差")
_k2_exp = "%.10f" % KEY["simpson_grid"][0][1]
_k2_act = "%.10f" % KEY["simpson_grid"][-1][1]
_k2_ok = (_k2_exp != _k2_act and KEY["simpson_delta_shrinks"])
add("K2", "K", "Simpson 网格粗细的负控",
    "N=1000 给 " + _k2_exp,
    "N=8000 给 " + _k2_act,
    _k2_ok, "相邻差逐档缩小，读数确实随网格变化")
_k3_ok = (KEY["lambda_frozen"] != KEY["lambda_hitrate"])
add("K3", "K", "冻结 lambda 一档的负控",
    "冻结通过率 " + KEY["lambda_frozen"],
    "全档命中率 " + KEY["lambda_hitrate"],
    _k3_ok, "承接 V63 C10、X-V63-6 K3、X-V63-10 K3 的冻结参数刀")
_k4_exp = str(KEY["lambda_zero_nmin"])
_k4_act = str(KEY["lambda_threequarters_nmin"])
_k4_ok = (_k4_exp != _k4_act)
add("K4", "K", "lambda=0 对 lambda=3/4 的负控",
    "lambda=0 的 n_min " + _k4_exp,
    "lambda=3/4 的 n_min " + _k4_act,
    _k4_ok, "两个不同参数给两个不同读数，判据不是恒真")

KEY["k_pairs"] = [
    (_k1_exp, _k1_act), (_k2_exp, _k2_act),
    (KEY["lambda_frozen"], KEY["lambda_hitrate"]), (_k4_exp, _k4_act),
]

# 关键表两路机拼：左路取 KEY 缓存，右路现场重算，左右模板数据源互不引用。
_left_alpha = [(x["alpha"], round(x["E"], 10), round(x["S"], 10),
                "%.3e" % x["res_corrected"]) for x in KEY["alpha_table"]]
_right_alpha = []
for _al in ALPHA_GRID:
    _e = E_trial(1, _al, 1.0, R_CUT, N_SIMPSON)
    _s = S_res(1, _al, 1.0, R_CUT, N_SIMPSON)
    _b = boundary_term(1, _al, 1.0, R_CUT)
    _right_alpha.append((_al, round(_e, 10), round(_s, 10),
                         "%.3e" % abs(_e - _b - _s)))
_left_beta = [(x["beta"], round(x["mismatch"], 9)) for x in KEY["beta_table"]]
_right_beta = []
for _be in BETA_GRID:
    _e = E_trial(1, 1.5, _be, R_CUT, N_SIMPSON)
    _s = S_res(1, 1.5, _be, R_CUT, N_SIMPSON)
    _b = boundary_term(1, 1.5, _be, R_CUT)
    _right_beta.append((_be, round(abs(_e - _b - _s), 9)))
_left_lambda = [(x["lambda"], x["n_min"]) for x in KEY["lambda_table"]]
_right_lambda = []
for _lam in LAMBDA_GRID:
    _arg, _ = n_min_of_lambda(_lam)
    _right_lambda.append((fmt_f(_lam), _arg))
_right_U1 = min(E_trial(1, _al, 1.0, R_CUT, N_SIMPSON) for _al in ALPHA_GRID)
_left_clamp = [(x["n"], x["gt_U1"]) for x in KEY["clamp_table"]]
_right_clamp = [(n, n / 2.0 > _right_U1) for n in N_GRID_CLAMP]
KEY["key_table_left"] = str([_left_alpha, _left_beta, _left_lambda, _left_clamp])
KEY["key_table_right"] = str([_right_alpha, _right_beta, _right_lambda, _right_clamp])
KEY["key_table_same"] = (KEY["key_table_left"] == KEY["key_table_right"])
KEY["key_table_U1_left"] = KEY["U1"]
KEY["key_table_U1_right"] = _right_U1

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


def _micro(x):
    """把浮点读数整数化到百万分之一，供判词片段机拼，避免浮点串格式漂移。"""
    return int(round(float(x) * 1000000))


def build_segments(shift=0):
    """判词片段一律由 KEY 读数机拼；shift 用于证明片段真的吃读数。"""
    return [
        "BOGOMOLNY-TWO-PATH-%d-ALPHA" % len(KEY["alpha_table"]),
        "FINITE-R-MISSING-%d-NANO" % int(round(KEY["boundary_R60_missing"] * 1e9)),
        "BETA-FLAT-%d-OF-%d" % (KEY["beta_flat_count"], len(KEY["beta_table"])),
        "L-N-EQUALS-N-OVER-2--S-NONNEG-%s" % str(KEY["lower_all_S_nonneg"]).upper(),
        "U1-MICRO-%d--ALPHA-MICRO-%d" % (_micro(KEY["U1"]), _micro(KEY["alpha_best"])),
        "SIMPSON-%d-GRID--TAIL-%d-GRID"
        % (len(KEY["simpson_grid"]), len(KEY["tail_grid"])),
        "CLAMP-GAP-MICRO-%d" % _micro(KEY["clamp_gap_L3_minus_U1"]),
        "N-GRID-%d-OF-8--OUTSIDE-N1-FALSE" % KEY["clamp_true_count"],
        "BPS-3L1-MICRO-%d-EQ-L3-MICRO-%d"
        % (_micro(KEY["bps_3L1"]), _micro(KEY["bps_L3"])),
        "SPLIT-OVERLAP-3U1-MICRO-%d-GT-L3-MICRO-%d"
        % (_micro(KEY["three_U1"]), _micro(KEY["L3"])),
        "LAMBDA-%d-GRID-HIT3-%s"
        % (KEY["lambda_total"], KEY["lambda_hitrate"].replace("/", "-OF-")),
        "FROZEN-1-OF-1-VS-FULL-%s" % KEY["lambda_hitrate"].replace("/", "-OF-"),
        "FREE-PARAM-TRANSFER-N-TO-LAMBDA",
        "DISCRETE-FIXED-PROFILE-CONVERGES-%s"
        % str(KEY["discrete_delta_shrinks"]).upper(),
        "VARIATIONAL-PROBE-DIVERGES-DISCARDED",
        "ENERGY-FIXERS-%d-OF-%d" % (KEY["energy_fixers_count"] + shift,
                                    KEY["energy_fix_paths"]),
        "IQ-THREE-SOLUTIONS-%d" % KEY["iq_three_solutions"],
        "CROSS-VOLUME-CENTER-%s"
        % "-".join(str(v) for v in KEY["prev_center_all_orders"]),
        "README-%d--R403-%d" % (KEY["readme_bytes"], KEY["readme_r403_tokens"]),
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

    guard("OK-DIRECTION",
          _b06_ok == (KEY["energy_fixers_count"] > 0)
          and _b06["kind"] == "FAIL"
          and KEY["energy_fixers_count"] == 0,
          "B06 问「是否存在」故 ok 须由 fixers 大于零驱动；实测 fixers=%d、ok=%s、kind=%s"
          % (KEY["energy_fixers_count"], _b06_ok, _b06["kind"]))

    guard("KEY-TABLE-TWO-PATH",
          KEY["key_table_same"] and len(KEY["key_table_left"]) > 100
          and abs(KEY["key_table_U1_left"] - KEY["key_table_U1_right"]) < 1e-12,
          "左右两路现场重算：alpha %d 档 / beta %d 档 / lambda %d 档 / clamp %d 档；一致=%s"
          % (len(_left_alpha), len(_left_beta), len(_left_lambda),
             len(_left_clamp), KEY["key_table_same"]))

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
          and KEY["energy_fixers_count"] == 0
          and KEY["lambda_frozen"] != KEY["lambda_hitrate"]
          and KEY["clamp_n1_false"],
          "内部固定机制 %d；冻结 %s 对全档 %s；n=1 档不成立=%s"
          % (KEY["energy_fixers_count"], KEY["lambda_frozen"],
             KEY["lambda_hitrate"], KEY["clamp_n1_false"]))

    guard("BOGOMOLNY-TWO-PATH",
          KEY["alpha_max_res_corrected"] < 1e-6
          and KEY["lower_max_res"] < 1e-6
          and KEY["lower_all_S_nonneg"] and _a01_ok and _a04_ok,
          "alpha 档最大残差 %.3e；n 档最大残差 %.3e；S 全非负=%s"
          % (KEY["alpha_max_res_corrected"], KEY["lower_max_res"],
             KEY["lower_all_S_nonneg"]))

    guard("FINITE-R-BOUNDARY",
          all(x["res_corrected"] < x["res_naive"]
              for x in KEY["tail_boundary_table"])
          and KEY["boundary_R60_missing"] > 1e-8
          and len(KEY["tail_boundary_table"]) == 4 and _a02_ok,
          "四档 R 修正后残差全更小；R=60 漏项 %.3e；网格随 R 加密保步长"
          % KEY["boundary_R60_missing"])

    guard("BETA-UNIQUE-FLAT",
          KEY["beta_flat_count"] == 1 and KEY["beta_bad_min"] > 1e-2
          and KEY["beta_mismatch_b1"] < 1e-7 and _a03_ok,
          "五档中配平 %d 档；非 1 档最小失配 %.6f；beta=1 失配 %.3e"
          % (KEY["beta_flat_count"], KEY["beta_bad_min"],
             KEY["beta_mismatch_b1"]))

    guard("CLAMP-STRICT-TWO-SIDES",
          KEY["clamp_gap_L3_minus_U1"] > 0 and KEY["clamp_true_count"] == 7
          and KEY["clamp_n1_false"] and _b01_ok and _b02_ok,
          "L(3) 减 U(1) = %.9f；n=2..8 成立 7 档；n=1 不成立"
          % KEY["clamp_gap_L3_minus_U1"])

    _b04 = [r for r in ROWS if r["id"] == "B04"][0]
    guard("OVERLAP-TAGGED",
          KEY["split_overlap"] and _b04_ok and "上界" in _b04["note"],
          "3 乘 U(1)=%.9f 大于 L(3)=%.9f；B04 note 含上界标注=%s"
          % (KEY["three_U1"], KEY["L3"], "上界" in _b04["note"]))

    _d04 = [r for r in ROWS if r["id"] == "D04"][0]
    guard("PROBE-DISCARD-TAGGED",
          _d04["kind"] == "INFO"
          and all(w in _d04["note"] for w in ("外部探算", "未重算", "不作证据")),
          "D04 kind=%s；三项标注齐备=%s"
          % (_d04["kind"],
             all(w in _d04["note"] for w in ("外部探算", "未重算", "不作证据"))))

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
    for i, x in enumerate(KEY["alpha_table"]):
        L.append("  alpha=%.2f E/S/res 左路 %s | 右路 %s"
                 % (x["alpha"], str(_left_alpha[i]), str(_right_alpha[i])))
    for i, x in enumerate(KEY["beta_table"]):
        L.append("  beta=%.2f 失配 左路 %s | 右路 %s"
                 % (x["beta"], str(_left_beta[i]), str(_right_beta[i])))
    for i, x in enumerate(KEY["lambda_table"]):
        L.append("  lambda=%-4s n_min 左路 %s | 右路 %s"
                 % (x["lambda"], str(_left_lambda[i][1]), str(_right_lambda[i][1])))
    for i, x in enumerate(KEY["clamp_table"]):
        L.append("  n=%d L(n)>U(1) 左路 %s | 右路 %s"
                 % (x["n"], str(_left_clamp[i][1]), str(_right_clamp[i][1])))
    L.append("  两路一致 = " + str(KEY["key_table_same"]))
    L.append("")
    L.append("【关键数字】")
    L.append("  平方和两路五档 alpha 最大修正残差 %.3e；当作 n/2 的最大朴素残差 %.3e"
             % (KEY["alpha_max_res_corrected"], KEY["alpha_max_res_naive"]))
    L.append("  R=60 漏掉的边界项 %.9e；四档 R 修正后残差 %s"
             % (KEY["boundary_R60_missing"],
                ["%.3e" % x["res_corrected"] for x in KEY["tail_boundary_table"]]))
    L.append("  beta 五档失配 %s；配平 %d 档；非 1 档最小失配 %.6f"
             % ([(x["beta"], round(x["mismatch"], 9)) for x in KEY["beta_table"]],
                KEY["beta_flat_count"], KEY["beta_bad_min"]))
    L.append("  下界表 %s；最大残差 %.3e；S 全非负=%s"
             % ([(x["n"], x["L"], round(x["S"], 9)) for x in KEY["lower_bound_table"]],
                KEY["lower_max_res"], KEY["lower_all_S_nonneg"]))
    L.append("  U(1) = %.9f（alpha=%.2f）；L(1) = %.9f；L(3) = %.9f；夹逼间隙 %.9f"
             % (KEY["U1"], KEY["alpha_best"], KEY["L1"], KEY["L3"],
                KEY["clamp_gap_L3_minus_U1"]))
    L.append("  3 乘 U(1) = %.9f 大于 L(3) = %.9f；区间重叠=%s"
             % (KEY["three_U1"], KEY["L3"], KEY["split_overlap"]))
    L.append("  Simpson 网格 %s；相邻差 %s"
             % ([(n, round(v, 10)) for n, v in KEY["simpson_grid"]],
                ["%.3e" % d for d in KEY["simpson_deltas"]]))
    L.append("  尾截断 %s；相邻差 %s"
             % ([(r, round(v, 10)) for r, v in KEY["tail_grid"]],
                ["%.3e" % d for d in KEY["tail_deltas"]]))
    L.append("  夹逼表 %s；成立 %d/8；n=1 不成立=%s"
             % ([(x["n"], x["L"], x["gt_U1"]) for x in KEY["clamp_table"]],
                KEY["clamp_true_count"], KEY["clamp_n1_false"]))
    L.append("  BPS 简并：3 乘 L(1) = %.9f 对 L(3) = %.9f；简并=%s"
             % (KEY["bps_3L1"], KEY["bps_L3"], KEY["bps_degenerate"]))
    L.append("  lambda 族 %s；唯一命中 3 的 %s；含并列 %d 档；并列档 %d；冻结 %s"
             % ([(x["lambda"], x["n_min"]) for x in KEY["lambda_table"]],
                KEY["lambda_hitrate"], KEY["lambda_hit3_including_tie"],
                KEY["lambda_tie_count"], KEY["lambda_frozen"]))
    L.append("  离散格式固定剖面 %s；相邻差 %s"
             % ([(n, round(v, 10)) for n, v in KEY["discrete_grid"]],
                ["%.3e" % d for d in KEY["discrete_deltas"]]))
    L.append("  变分探算（弃用、不作证据）%s 序列 %s"
             % (KEY["variational_probe_object"],
                KEY["variational_probe_divergent_sequence"]))
    L.append("  内部固定机制 %d / %d 条路径 %s；路径清单 %s"
             % (KEY["energy_fixers_count"], KEY["energy_fix_paths"],
                str(KEY["energy_fixers"]), str(KEY["energy_fix_path_names"])))
    L.append("  跨册反抄：中心阶 %s；Z_k 命中 3 的 k %s；上一册内部固定机制 %d；rid %s"
             % (KEY["prev_center_all_orders"], str(KEY["zk_hit3_from_prev"]),
                KEY["prev_internal_fixers_count"], KEY["prev_rid"]))
    L.append("  I_Q=3 整数网格解 %d；3 个 n=1 对 1 个 n=3 缺陷数差 %d"
             % (KEY["iq_three_solutions"], KEY["cluster_diff_count"]))
    L.append("  README %d B / r402 锚点 %d / r403 锚点 %d / 三树 r403 文件 %d"
             % (KEY["readme_bytes"], KEY["readme_r402_tokens"],
                KEY["readme_r403_tokens"], KEY["r403_files"]))
    L.append("")
    L.append("【诚实边界】")
    L.append("  1. 只产可算判决，不产新物理；独立实验预言 0。")
    L.append("  2. 严格结论只覆盖单组分 U(1) Abelian-Higgs、beta=1 临界耦合、径向试探剖面。")
    L.append("  3. beta 不等于 1 时 Bogomolny 平方和不配平；多组分、非 Abel、引力、超对称、theta 项未算。")
    L.append("  4. 夹逼只判 E(3) 大于 E(1)，不能判 3 个 n=1 与 1 个 n=3 谁更省。")
    L.append("  5. 变分探算网格细化下发散，已弃用；其读数不作证据、未在本册重算。")
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
