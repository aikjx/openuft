# -*- coding: utf-8 -*-
"""攻坚 X-V63-12：SU(3)_c 中心 Z_3 能否与内部 S^2 涡旋数投影合法联系（独立机核 · 部件 1/3）。

体例：跨卷攻坚册 —— 不新增 RID、不进 README 登记位、条目不与任何卷相加。
来料：无外部来料；输入为 X-V63-10 A08/D04（SU(3)_c 中心确为 Z_3，若与内部
      涡旋投影联系则 B06 需重判）、X-V63-6 的 pi_1=0、X-V63-11 的夹逼边界。
对象：4D SU(3)_c 主丛的 Z_3 t Hooft 磁通、内部 S^2 上 U(1) 线丛的第一陈类。
红线：数学自洽 ≠ 实验证实；只产可算判决，不产新物理；独立实验预言数 0。
纪律：对象错位必须写进变量名；报「不存在」前先列对象全集；
      「不成立」须同时报在哪条线上仍成立；范围内全对须报范围外第一条就错。
"""
import os
import io
import json
import ast
import glob
from fractions import Fraction as F
from math import factorial, gcd

TITLE = "攻坚 X-V63-12 独立机核"
DATE = "2026-11-08"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "数据")
JS = os.path.join(DATA, "_XV6312_recompute_2026-11-08.json")
RPT = os.path.join(DATA, "_XV6312_recompute_report_2026-11-08.txt")
RD = os.path.join(ROOT, "README.md")
P = 3

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
    print("  [GUARD %-4s] %-24s | %s" % ("ok" if ok else "BAD", name, detail))
    return bool(ok)


def fmt_f(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else "%d/%d" % (q.numerator, q.denominator)


def is_int(q):
    return F(q).denominator == 1


print("=" * 78)
print(TITLE + "  " + DATE)
print("=" * 78)
def mat_rank_mod(A, p=P):
    """有限域 F_p 上的矩阵秩，整数高斯消元；用于真算同调维数。"""
    A = [row[:] for row in A]
    if not A:
        return 0
    n, m = len(A), len(A[0])
    r = 0
    for c in range(m):
        piv = None
        for i in range(r, n):
            if A[i][c] % p:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c] % p, p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] % p:
                f = A[i][c] % p
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(m)]
        r += 1
        if r == n:
            break
    return r


print("\n[GUARD] 工具自检（精确有理数 / 有限域矩阵秩，两侧都测）")
guard("FRAC-EXACT", F(1, 3) + F(1, 6) - F(1, 2) == 0, "1/3+1/6-1/2 = 0")
_sing = mat_rank_mod([[1, 2], [2, 1]])
_full = mat_rank_mod([[1, 0], [0, 1]])
guard("MATRIX-RANK-F3-TWO-SIDES",
      _sing == 1 and _full == 2,
      "F_3 上 [[1,2],[2,1]] 秩 %d（须 1）；单位阵秩 %d（须 2）" % (_sing, _full))


# ---------------------------------------------------------------- A 层：上同调账
# S^2 取四面体边界单纯复形：4 顶点 / 6 边 / 4 面，系数 F_3。
VERTS = [0, 1, 2, 3]
EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
FACES = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
_eidx = {e: i for i, e in enumerate(EDGES)}
_fidx = {f: i for i, f in enumerate(FACES)}
D1 = [[0] * len(EDGES) for _ in VERTS]
for (u, v), c in _eidx.items():
    D1[u][c] = (-1) % P
    D1[v][c] = 1 % P
D2 = [[0] * len(FACES) for _ in EDGES]
for (a, b, c), col in _fidx.items():
    for e, s in (((b, c), 1), ((a, c), -1), ((a, b), 1)):
        D2[_eidx[e]][col] = s % P
R1 = mat_rank_mod(D1)
R2 = mat_rank_mod(D2)
KEY["s2_rank_d1"] = R1
KEY["s2_rank_d2"] = R2
KEY["s2_H0"] = len(VERTS) - R1
KEY["s2_H1"] = (len(EDGES) - R1) - R2
KEY["s2_H2"] = len(FACES) - R2
KEY["s2_euler_chain"] = len(VERTS) - len(EDGES) + len(FACES)
KEY["s2_euler_homology"] = KEY["s2_H0"] - KEY["s2_H1"] + KEY["s2_H2"]
_d1d2 = [[sum(D1[i][k] * D2[k][j] for k in range(len(EDGES))) % P
          for j in range(len(FACES))] for i in range(len(VERTS))]
KEY["s2_chain_condition"] = all(v == 0 for row in _d1d2 for v in row)
KEY["s2_d1d2_max"] = max(v for row in _d1d2 for v in row)

# Kunneth：最小 CW 复形（微分全 0），M_4 = S^2 x S^2，X = M_4 x S^2。
CW_S2 = {0: 1, 1: 0, 2: 1}
CW_M4 = {0: 1, 1: 0, 2: 2, 3: 0, 4: 1}
KEY["cw_X"] = {}
for _i, _di in CW_M4.items():
    for _j, _dj in CW_S2.items():
        KEY["cw_X"][_i + _j] = KEY["cw_X"].get(_i + _j, 0) + _di * _dj
KEY["cw_X"] = {str(k): int(v) for k, v in sorted(KEY["cw_X"].items())}
KEY["kunneth_M_part"] = CW_M4[2] * CW_S2[0]
KEY["kunneth_cross_part"] = CW_M4[1] * CW_S2[1]
KEY["kunneth_S_part"] = CW_M4[0] * CW_S2[2]
KEY["kunneth_H2_total"] = KEY["cw_X"]["2"]
KEY["kunneth_cross_driven_by_H1"] = (KEY["s2_H1"] == 0)
KEY["z3_flux_component"] = "H^2(M_4, Z_3)"
KEY["internal_flux_component"] = "H^2(S^2, Z_3)"

# 范围外第一条就错：内部换成 T^2（H^1=2）、时空换成 T^4（H^1=4）。
CW_T2 = {0: 1, 1: 2, 2: 1}
CW_T4 = {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}
KEY["outside_cross_H1M_H1S"] = CW_T4[1] * CW_T2[1]
KEY["outside_T2_H1"] = CW_T2[1]
KEY["outside_T4_H1"] = CW_T4[1]
KEY["baseline_cross"] = KEY["kunneth_cross_part"]

# ---------------------------------------------------------------- B 层：triality
def partitions(n, mx=None):
    if n == 0:
        yield ()
        return
    if mx is None:
        mx = n
    for k in range(min(n, mx), 0, -1):
        for rest in partitions(n - k, k):
            yield (k,) + rest


def hook_prod(lam):
    prod = 1
    for i, row in enumerate(lam):
        for j in range(1, row + 1):
            col = sum(1 for r in lam if r >= j)
            prod *= (row - j) + (col - (i + 1)) + 1
    return prod


def f_specht(lam):
    return factorial(sum(lam)) // hook_prod(lam)


def dim_gl3(lam):
    v = tuple(lam) + (0,) * (3 - len(lam))
    out = F(1)
    for i in range(3):
        for j in range(i + 1, 3):
            out *= F(v[i] - v[j] + (j + 1) - (i + 1), (j + 1) - (i + 1))
    return out


def tensor_data(k):
    rows, total, singlets = [], F(0), 0
    for lam in partitions(k):
        if len(lam) > 3:
            continue
        v = tuple(lam) + (0,) * (3 - len(lam))
        d = dim_gl3(v)
        f = f_specht(lam)
        is_det = (v[0] == v[1] == v[2])
        rows.append({"lam": str(v), "f": int(f), "dim": int(d),
                     "is_det": bool(is_det)})
        total += f * d
        if is_det:
            singlets += f
    return rows, int(total), int(singlets)


KEY["tensor_table"] = []
for _k in (2, 3, 6):
    _rows, _total, _sing = tensor_data(_k)
    _proj = 3 ** _k if _k % 3 == 0 else 0
    KEY["tensor_table"].append({
        "k": _k, "rows": _rows, "sum_f_dim": _total, "expect": 3 ** _k,
        "singlets": _sing, "z3_projection": _proj,
        "discrim": ("%d/%d" % (_sing, _proj)) if _proj else "0/0",
    })
KEY["singlets_3pow2"] = KEY["tensor_table"][0]["singlets"]
KEY["singlets_3pow3"] = KEY["tensor_table"][1]["singlets"]
KEY["singlets_3pow6"] = KEY["tensor_table"][2]["singlets"]
KEY["z3_proj_3pow3"] = KEY["tensor_table"][1]["z3_projection"]
KEY["z3_discrim_3pow3"] = KEY["tensor_table"][1]["discrim"]

IRREPS = [((0, 0), "1"), ((1, 0), "3"), ((0, 1), "3bar"), ((1, 1), "8"),
          ((2, 0), "6"), ((0, 2), "6bar"), ((3, 0), "10"), ((2, 1), "15")]
KEY["triality_table"] = []
for (_p, _q), _nm in IRREPS:
    _dim = (_p + 1) * (_q + 1) * (_p + _q + 2) // 2
    KEY["triality_table"].append({"name": _nm, "p": _p, "q": _q,
                                  "dim": _dim, "t": (_p + 2 * _q) % 3})
KEY["triality_t_values"] = sorted(set(x["t"] for x in KEY["triality_table"]))
KEY["triality_dim_by_t"] = {str(t): sum(x["dim"] for x in KEY["triality_table"]
                                        if x["t"] == t) for t in (0, 1, 2)}

# CS 级 k 网格：exp(2*pi*i*k*n/3)=1 逼 k*n = 0 mod 3。
KEY["cs_table"] = []
for _k in range(1, 10):
    _nmin = next(n for n in range(1, 10) if (_k * n) % 3 == 0)
    KEY["cs_table"].append({"k": _k, "n_min": _nmin})
KEY["cs_total"] = len(KEY["cs_table"])
KEY["cs_hit3"] = sum(1 for x in KEY["cs_table"] if x["n_min"] == 3)
KEY["cs_hitrate"] = "%d/%d" % (KEY["cs_hit3"], KEY["cs_total"])
KEY["cs_frozen"] = "1/1"
KEY["cs_nmin_distinct"] = len(set(x["n_min"] for x in KEY["cs_table"]))
KEY["cs_k_independent"] = (KEY["cs_nmin_distinct"] == 1)
KEY["cs_k_mod3_zero"] = [x["k"] for x in KEY["cs_table"] if x["k"] % 3 == 0]
KEY["cs_nmin_for_k1"] = KEY["cs_table"][0]["n_min"]
KEY["cs_nmin_for_k3"] = KEY["cs_table"][2]["n_min"]

# ---------------------------------------------------------------- C 层：三条通道
# 通道全集显式列出，避免「报不存在但没列对象」。
KEY["channel_names"] = ["Kunneth 直和", "H^1 上的 Wilson line", "6D CS 级耦合"]
KEY["channel_fixers"] = []
# 通道 1：若交叉项非零则可能有耦合；实测 0。
if KEY["kunneth_cross_part"] > 0:
    KEY["channel_fixers"].append(KEY["channel_names"][0])
# 通道 2：若 H^1(S^2) 非零则可承载 Z_3 holonomy；实测 0。
if KEY["s2_H1"] > 0:
    KEY["channel_fixers"].append(KEY["channel_names"][1])
# 通道 3：只有当 n_min 与自由输入 k 无关且仍命中 3，才算内部机制。
# 判据由全档读数驱动：distinct 为 1 表示结果与 k 脱钩，为 2 表示随输入漂移。
if KEY["cs_k_independent"] and KEY["cs_hit3"] == KEY["cs_total"]:
    KEY["channel_fixers"].append(KEY["channel_names"][2])
KEY["channel_fixers_count"] = len(KEY["channel_fixers"])
KEY["channel_total"] = len(KEY["channel_names"])

# 回代：陈类整数性、I_Q、上一册读数（由该册 JSON 反抄，不手填）。
_chern_table = [(fmt_f(F(n)), n % 1 == 0) for n in (F(1), F(2), F(3),
                                                     F(1, 2), F(3, 2), F(5, 2))]
KEY["chern_table"] = [[a, bool(b)] for a, b in _chern_table]
KEY["chern_int_legal"] = sum(1 for _, b in _chern_table if b)
KEY["chern_half_legal"] = sum(1 for a, b in _chern_table
                              if not is_int(F(a)) and b)
KEY["iq_three_solutions"] = len([(p, q) for p in range(-8, 9) for q in range(-8, 9)
                                 if 2 * (p + q) == 3])

_PREV_JS = os.path.join(DATA, "_XV6310_recompute_2026-11-08.json")
_PREV = json.load(io.open(_PREV_JS, "r", encoding="utf-8"))
KEY["prev_center_all_orders"] = list(_PREV["key_numbers"]["center_all_orders"])
KEY["prev_zk_table"] = [[int(x["k"]), int(x["n_min"])]
                        for x in _PREV["key_numbers"]["zk_table"]]
KEY["prev_internal_fixers_count"] = int(_PREV["key_numbers"]["internal_fixers_count"])
KEY["prev_su3_center_group"] = str(_PREV["key_numbers"]["su3_center_group"])
KEY["prev_rid"] = str(_PREV.get("rid", ""))

# ---------------------------------------------------------------- README 体检
_rb = io.open(RD, "rb").read()
KEY["readme_bytes"] = len(_rb)
KEY["readme_r402_tokens"] = _rb.count(b"TUFT-r402_")
KEY["readme_r403_tokens"] = _rb.count(b"TUFT-r403_")
KEY["r403_files"] = len(glob.glob(os.path.join(ROOT, "**", "*TUFT-r403_*"), recursive=True))


print("\n[ROWS] A 层：上同调账与对象错位")
_a01_ok = (KEY["s2_H0"] == 1 and KEY["s2_H1"] == 0 and KEY["s2_H2"] == 1
           and KEY["s2_rank_d1"] == 3 and KEY["s2_rank_d2"] == 3)
add("A01", "A", "S^2 四面体边界单纯复形在 F_3 上的同调维数",
    "H^0 须为 1、H^1 须为 0、H^2 须为 1，且两个边缘映射的秩须真算出",
    "rank d1=%d / rank d2=%d；H^0=%d H^1=%d H^2=%d"
    % (KEY["s2_rank_d1"], KEY["s2_rank_d2"],
       KEY["s2_H0"], KEY["s2_H1"], KEY["s2_H2"]),
    _a01_ok, "H^1 的零，分母是链维数 6 减 d1 秩 3 再减 d2 秩 3；用有限域矩阵秩实算，不抄球面上同调结论")

_a02_ok = (KEY["s2_chain_condition"] and KEY["s2_d1d2_max"] == 0
           and KEY["s2_euler_chain"] == KEY["s2_euler_homology"])
add("A02", "A", "链条件与欧拉示性数两路交叉验证",
    "d1 复合 d2 须为零映射，链层欧拉数须等于同调层欧拉数",
    "d1 复合 d2 最大元 %d；链欧拉数 %d 对同调欧拉数 %d"
    % (KEY["s2_d1d2_max"], KEY["s2_euler_chain"], KEY["s2_euler_homology"]),
    _a02_ok, "两路独立：一个是矩阵乘法，一个是维数交替和")

_a03_ok = (KEY["kunneth_H2_total"] == 3
           and KEY["kunneth_M_part"] == 2
           and KEY["kunneth_cross_part"] == 0
           and KEY["kunneth_S_part"] == 1
           and KEY["kunneth_cross_driven_by_H1"])
add("A03", "A", "Kunneth 分解把 H^2(M_4 x S^2) 拆成直和，交叉项为零",
    "总维数须等于 M 分量加交叉项加 S 分量，且交叉项须由 H^1(S^2)=0 驱动",
    "H^2 总维数 %d = M 分量 %d + 交叉 %d + S 分量 %d；链维数表 %s；交叉由 H^1=0 驱动=%s"
    % (KEY["kunneth_H2_total"], KEY["kunneth_M_part"],
       KEY["kunneth_cross_part"], KEY["kunneth_S_part"],
       str(KEY["cw_X"]), KEY["kunneth_cross_driven_by_H1"]),
    _a03_ok, "交叉项的零，分母是 H^1(M_4) 乘 H^1(S^2) 张量积的链维数；Z_3 色磁通落 M 分量，内部 U(1) 磁通落 S 分量，二者不混合")

_a04_ok = (KEY["outside_cross_H1M_H1S"] > 0
           and KEY["outside_cross_H1M_H1S"] != KEY["baseline_cross"]
           and KEY["outside_T2_H1"] == 2 and KEY["outside_T4_H1"] == 4)
add("A04", "A", "范围外第一条就错：内部换 T^2、时空换 T^4 则交叉项非零",
    "换内部空间后 H^1 须非零，交叉项须从基线值变到非零值",
    "基线 S^2 交叉项 %d；T^2 的 H^1=%d、T^4 的 H^1=%d ⇒ 交叉项 %d"
    % (KEY["baseline_cross"], KEY["outside_T2_H1"],
       KEY["outside_T4_H1"], KEY["outside_cross_H1M_H1S"]),
    _a04_ok, "证明 A03 测的确实是内部空间 H^1，而不是恒真谓词")

_a05_ok = (KEY["z3_flux_component"] != KEY["internal_flux_component"]
           and KEY["kunneth_cross_part"] == 0)
add("A05", "A", "对象错位刀：色 Z_3 磁通与内部涡旋数属于不同直和分量",
    "两个对象所属的上同调分量须显式写出且不同",
    "Z_3 磁通属于 %s；内部磁通属于 %s；交叉项 %d"
    % (KEY["z3_flux_component"], KEY["internal_flux_component"],
       KEY["kunneth_cross_part"]),
    _a05_ok, "把色群中心搬来当内部空间投影正是把不同分量相加")

add("A06", "A", "与标准 Kunneth 定理一致，但本册读数是胞腔链复形实算所得",
    "同源一致性不得冒充独立证据",
    "本册独立实算单纯复形秩 %d / %d、最小 CW 链维数表 %d 档；教科书结论仅作对照"
    % (KEY["s2_rank_d1"], KEY["s2_rank_d2"], len(KEY["cw_X"])),
    None, "同源回验抓不到同源错误；由 SAME-SOURCE-TAGGED 守卫强制")

add("A07", "A", "最小 CW 复形微分全零时 H^2 维数等于 C_2 维数是定义恒等式",
    "展开后无残差可算，按定义恒等式纪律不记 PASS",
    "C_2 维数 %d 直接给出 H^2 维数 %d；这是规定不是推导"
    % (KEY["kunneth_H2_total"], KEY["kunneth_H2_total"]),
    "ID", "配 NOT-ALL-GREEN 守卫防首跑全绿；同调内容由 A01 的单纯复形提供")

_a08_ok = (KEY["s2_H1"] == 0 and KEY["kunneth_cross_part"] == 0)
add("A08", "A", "Wilson line 通道：内部空间无一阶上同调承载 Z_3 holonomy",
    "H^1(S^2, Z_3) 须为零，故离散 holonomy 通道维数须为零",
    "H^1(S^2,F_3)=%d；离散 holonomy 通道维数 %d"
    % (KEY["s2_H1"], KEY["s2_H1"]),
    _a08_ok, "零的分母是 H^1 链维数 6 减 d1 秩 3 再减 d2 秩 3；把对象名写进读数：这是内部空间的 H^1，不是 4D 时空的 H^1")

_nmod3 = [(n, n % 3) for n in range(1, 10)]
_a09_ok = (sorted(set(r for _, r in _nmod3)) == [0, 1, 2]
           and sum(1 for _, r in _nmod3 if r == 0) == 3)
add("A09", "A", "内部磁通 n 模 3 的三种余数全部可达，Z_3 投影不逼 n 为 3 的倍数",
    "九档 n 的余数集合须恰为 0、1、2，且命中 0 的档数须显式报出",
    "余数表 %s；余数集合 %s；命中 0 的 %d 档"
    % (str(_nmod3), sorted(set(r for _, r in _nmod3)),
       sum(1 for _, r in _nmod3 if r == 0)),
    _a09_ok, "把 n 模 3 为零读成被理论强制，是把可达类读成选择定则")

print("\n[ROWS] B 层：triality、色单态正对照与唯一真判负")
_b01_ok = (KEY["triality_t_values"] == [0, 1, 2]
           and len(KEY["triality_table"]) == 8
           and [x for x in KEY["triality_table"] if x["name"] == "3"][0]["t"] == 1
           and [x for x in KEY["triality_table"] if x["name"] == "3bar"][0]["t"] == 2)
add("B01", "B", "A_2 triality t=(p+2q) mod 3 把 SU(3) 不可约表示分三类",
    "八个最低表示的 t 集合须为 0、1、2，且 3 与 3bar 的 t 须不同",
    "triality 表 %s；t 集合 %s；按 t 的维数和 %s"
    % ([(x["name"], x["t"]) for x in KEY["triality_table"]],
       KEY["triality_t_values"], KEY["triality_dim_by_t"]),
    _b01_ok, "SU(3)_c 中心确为 Z_3，这是上一册 A08 的同口径回代")

_b02_ok = (all(x["sum_f_dim"] == x["expect"] for x in KEY["tensor_table"])
           and KEY["singlets_3pow2"] == 0 and KEY["singlets_3pow3"] == 1
           and KEY["singlets_3pow6"] == 5)
add("B02", "B", "Schur-Weyl 分解给出 3 的张量幂里的真色单态数",
    "三档 k 的维数和须分别等于 9、27、729，单态数须为 0、1、5",
    "k=2 和 %d 单态 %d；k=3 和 %d 单态 %d；k=6 和 %d 单态 %d"
    % (KEY["tensor_table"][0]["sum_f_dim"], KEY["singlets_3pow2"],
       KEY["tensor_table"][1]["sum_f_dim"], KEY["singlets_3pow3"],
       KEY["tensor_table"][2]["sum_f_dim"], KEY["singlets_3pow6"]),
    _b02_ok, "用钩子长公式与钩内容公式实算，不抄张量积分解表")

_b03_ok = (KEY["z3_proj_3pow3"] == 27 and KEY["singlets_3pow3"] == 1
           and KEY["z3_discrim_3pow3"] == "1/27")
add("B03", "B", "Z_3 中心投影对 3 的三次张量幂判别力仅 1/27",
    "投影保留维数须为 27，真单态须为 1，两者之比须报出",
    "Z_3 投影保留 %d/%d；真色单态 %d；判别力 %s"
    % (KEY["z3_proj_3pow3"], 27, KEY["singlets_3pow3"],
       KEY["z3_discrim_3pow3"]),
    _b03_ok, "一个 100 通过百分比的谓词判别力为 0；中心只给 triality 不给单态")

_b04_ok = (len(set((x["z3_projection"], x["singlets"])
                   for x in KEY["tensor_table"])) == 3
           and KEY["tensor_table"][0]["z3_projection"] == 0
           and KEY["tensor_table"][2]["z3_projection"] == 729)
add("B04", "B", "三档张量幂的 Z_3 投影读数两两不同",
    "k=2、3、6 三档须给出 0、全保留、全保留且单态数不同的读数",
    "投影/单态 %s"
    % ([(x["k"], x["z3_projection"], x["singlets"]) for x in KEY["tensor_table"]],),
    _b04_ok, "两侧都测：k 不被 3 整除时投影为空，被 3 整除时投影全通过")

_b05_ok = (KEY["singlets_3pow2"] == 0 and KEY["singlets_3pow3"] == 1
           and KEY["singlets_3pow6"] == 5)
add("B05", "B", "在哪条线上仍成立：Z_3 确实给 4D 色单态选择定则",
    "3 的二次幂无单态、三次幂恰一个单态、六次幂给五个单态",
    "3x3 单态 %d；3x3x3 单态 %d；6 次幂单态 %d"
    % (KEY["singlets_3pow2"], KEY["singlets_3pow3"], KEY["singlets_3pow6"]),
    _b05_ok, "本册判负的是「与内部涡旋数投影的联系」，不是「Z_3 无用」")

_b06_ok = (KEY["channel_fixers_count"] > 0)
add("B06", "B", "唯一真判负：Z_3 色中心能否与内部涡旋数投影建立不新增输入的合法联系",
    "须存在不依赖新输入的内部机制把两者联系起来",
    "%d 条通道中合法机制 %d 个 %s；通道全集 %s；交叉项 %d；H^1(S^2) %d；CS 级命中 %s 且 k 是输入"
    % (KEY["channel_total"], KEY["channel_fixers_count"],
       str(KEY["channel_fixers"]), str(KEY["channel_names"]),
       KEY["kunneth_cross_part"], KEY["s2_H1"], KEY["cs_hitrate"]),
    _b06_ok, "判负已登记；问的是「是否存在」，故 ok 由机制个数大于零驱动")

_b07_ok = (KEY["cs_total"] == 9 and KEY["cs_hit3"] == 6
           and KEY["cs_frozen"] != KEY["cs_hitrate"])
add("B07", "B", "6D CS 级 k 能给 n_min=3，但 k 是作用量里的新输入",
    "九档 k 须给不同 n_min，命中 3 的档数与冻结一档的读数须不同",
    "CS 级表 %s；命中 3 的 %s；冻结 %s"
    % ([(x["k"], x["n_min"]) for x in KEY["cs_table"]],
       KEY["cs_hitrate"], KEY["cs_frozen"]),
    _b07_ok, "自由度从 n 转移到 k、再到 CS 级，与 X-V63-10 的 n 转移到 k 同族")

_b08_ok = (KEY["cs_k_mod3_zero"] == [3, 6, 9]
           and KEY["cs_nmin_for_k3"] == 1 and KEY["cs_nmin_for_k1"] == 3)
add("B08", "B", "两侧都测：k 为 3 的倍数时约束消失",
    "k=3、6、9 须给 n_min=1，而 k=1 须给 n_min=3",
    "k 为 3 的倍数的档 %s 给 n_min=%d；k=1 给 n_min=%d"
    % (KEY["cs_k_mod3_zero"], KEY["cs_nmin_for_k3"], KEY["cs_nmin_for_k1"]),
    _b08_ok, "显式报约束消失的档，避免把六档命中读成全称规律")

_b09_ok = (KEY["prev_internal_fixers_count"] == 0
           and KEY["prev_su3_center_group"] == "Z3"
           and KEY["prev_rid"] == "NONE-NO-RID")
add("B09", "B", "回代 X-V63-10：Z_k 的 k=3 给 n_min=3，但 k 是输入",
    "反抄读数须给上一册内部固定机制 0、色群中心 Z3",
    "上一册内部固定机制 %d；色群中心 %s；Z_k 表 %s；rid %s"
    % (KEY["prev_internal_fixers_count"], KEY["prev_su3_center_group"],
       str(KEY["prev_zk_table"]), KEY["prev_rid"]),
    _b09_ok, "跨册读数只作输入回代，不与本册条目相加")

print("\n[ROWS] C 层：对象边界与回代")
add("C01", "C", "回代 X-V63-6：V63 实标量真空离散使 pi_1=0",
    "上一册 256 个离散环路中连续且非常值 0 个；本册 H^1=0 是同口径不同对象",
    "pi_1=0 的环路读数 0 个；本册 H^1(S^2,F_3) 维数 0；两者不相加",
    None, "两个零的分母分别是 256 个离散环路集合与 H^1 的链维数 3；基本群与上同调是两个对象；显式标注口径回代")

add("C02", "C", "回代 X-V63-11：能量层已严格排除 n=3",
    "上一册的夹逼读数只作输入，不重数条目",
    "上一册 L(3) 大于 U(1) 给 E(3) 大于 E(1)；本册不重算能量泛函",
    None, "能量层与色群层不相加")

_c03_ok = (KEY["chern_int_legal"] == 3 and KEY["chern_half_legal"] == 0)
add("C03", "C", "陈类整数性不因引入 Z_3 色磁通而松绑",
    "整数磁通合法 3 档、半整数合法 0 档",
    "磁通表 %s；整数合法 %d；半整数合法 %d"
    % (KEY["chern_table"], KEY["chern_int_legal"], KEY["chern_half_legal"]),
    _c03_ok, "与 X-V63-1 同口径；色群层结论不替代拓扑层条件")

_c04_ok = (KEY["iq_three_solutions"] == 0)
add("C04", "C", "整数网格 I_Q=3 解 0 个，与色空间 triality 不相加",
    "I_Q=3 的整数网格解须为 0",
    "I_Q=3 解 %d；色单态读数 %d 是另一对象"
    % (KEY["iq_three_solutions"], KEY["singlets_3pow3"]),
    _c04_ok, "可达的 n 模 3 为零不等于 I_Q=3；两个读数不互相替代")

_c05_ok = (KEY["prev_center_all_orders"] == [1, 2, 4]
           and KEY["prev_su3_center_group"] == "Z3"
           and KEY["prev_rid"] == "NONE-NO-RID")
add("C05", "C", "跨册读数由上一册机核 JSON 反抄，不手填",
    "反抄的三项须与上一册判定一致",
    "Spin(2n) 中心阶 %s；色群中心 %s；rid %s；来源 _XV6310_recompute_2026-11-08.json"
    % (KEY["prev_center_all_orders"], KEY["prev_su3_center_group"], KEY["prev_rid"]),
    _c05_ok, "读数来自引擎输出而非记忆；上一册条目不与本册相加")

add("C06", "C", "条件式边界：本册不重判 X-V63-10 的 B06",
    "「若联系成立需重判」的前提须由本册读数检验",
    "本册三通道合法机制 %d/%d ⇒ 前提不成立 ⇒ B06 维持判负；若未来引入额外耦合项须重判"
    % (KEY["channel_fixers_count"], KEY["channel_total"]),
    None, "不是全称否证：只覆盖明示的三条通道与 S^2 内部空间口径")

print("\n[ROWS] D 层：诚实边界与不相加声明")
add("D01", "D", "本册不产新物理",
    "只产可算判决，独立实验预言数须为 0",
    "未构造新作用量、未给新粒子、未给可检验数值；独立预言 0",
    None, "数学自洽不等于实验证实")
add("D02", "D", "与 X-V63-11 / X-V63-10 / X-V63-6 / X-V63-1 / V63 不相加",
    "前册读数只作输入回代",
    "本册 34 条独立复算，不与前册 34 / 34 / 32 / 27 / 31 条相加",
    None, "C01 / C02 / C05 显式声明口径回代")
add("D03", "D", "严格结论的覆盖口径",
    "只覆盖 4D M_4=S^2xS^2、内部空间 S^2、F_3 系数、最小 CW 链复形",
    "A04 已显示换成 T^2 与 T^4 时交叉项变 8；非平凡内部丛、非 Abel 涡旋、引力均未算",
    None, "不声称任何统一模型都不可能把色中心与内部磁通联系")
add("D04", "D", "未重建的部分",
    "完整 6D 反常账、边界 CS 级的动力学来源、Spin 结构与 Wilson line 全账未算",
    "CS 级 k 只作为自由输入枚举，未由作用量推导",
    None, "k 若由理论内部给出，B06 需重判")
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
_k1_exp = str(KEY["baseline_cross"])
_k1_act = str(KEY["outside_cross_H1M_H1S"])
_k1_ok = (_k1_exp != _k1_act and KEY["outside_cross_H1M_H1S"] > 0)
add("K1", "K", "换内部空间使交叉项从零变非零的负控",
    "S^2 基线交叉项 " + _k1_exp,
    "T^2 与 T^4 交叉项 " + _k1_act,
    _k1_ok, "范围外第一条就错；判据确实由 H^1 驱动")
_k2_exp = str(KEY["z3_proj_3pow3"])
_k2_act = str(KEY["singlets_3pow3"])
_k2_ok = (_k2_exp != _k2_act and KEY["z3_proj_3pow3"] > KEY["singlets_3pow3"])
add("K2", "K", "把 Z_3 投影当色单态判据的负控",
    "投影保留 " + _k2_exp,
    "真单态 " + _k2_act,
    _k2_ok, "投影全通过而单态只有一个，判别力 1/27")
_k3_ok = (KEY["cs_frozen"] != KEY["cs_hitrate"])
add("K3", "K", "冻结 CS 级一档的负控",
    "冻结通过率 " + KEY["cs_frozen"],
    "全档命中率 " + KEY["cs_hitrate"],
    _k3_ok, "承接 V63 C10 起的冻结参数刀，第五次复现")
_k4_exp = str(KEY["cs_nmin_for_k1"])
_k4_act = str(KEY["cs_nmin_for_k3"])
_k4_ok = (_k4_exp != _k4_act)
add("K4", "K", "CS 级 k=1 对 k=3 的负控",
    "k=1 的 n_min " + _k4_exp,
    "k=3 的 n_min " + _k4_act,
    _k4_ok, "两档给两个不同读数，判据不是恒真")

KEY["k_pairs"] = [
    (_k1_exp, _k1_act), (_k2_exp, _k2_act),
    (KEY["cs_frozen"], KEY["cs_hitrate"]), (_k4_exp, _k4_act),
]

# 关键表两路机拼：左路取 KEY 缓存，右路现场重算，左右模板数据源互不引用。
_left_triality = [(x["name"], x["t"]) for x in KEY["triality_table"]]
_right_triality = [(nm, ((p + 2 * q) % 3)) for (p, q), nm in IRREPS]
_left_tensor = [(x["k"], x["sum_f_dim"], x["singlets"], x["z3_projection"])
                for x in KEY["tensor_table"]]
_right_tensor = []
for _k in (2, 3, 6):
    _rr, _tt, _ss = tensor_data(_k)
    _pp = 3 ** _k if _k % 3 == 0 else 0
    _right_tensor.append((_k, _tt, _ss, _pp))
_left_cs = [(x["k"], x["n_min"]) for x in KEY["cs_table"]]
_right_cs = [(k, next(n for n in range(1, 10) if (k * n) % 3 == 0))
             for k in range(1, 10)]
_left_kunneth = [KEY["kunneth_M_part"], KEY["kunneth_cross_part"],
                 KEY["kunneth_S_part"], KEY["kunneth_H2_total"]]
_S2 = {0: 1, 1: 0, 2: 1}
_M4 = {0: 1, 1: 0, 2: 2, 3: 0, 4: 1}
_right_kunneth = [_M4[2] * _S2[0], _M4[1] * _S2[1], _M4[0] * _S2[2],
                  _M4[2] * _S2[0] + _M4[1] * _S2[1] + _M4[0] * _S2[2]]
KEY["key_table_left"] = str([_left_triality, _left_tensor, _left_cs, _left_kunneth])
KEY["key_table_right"] = str([_right_triality, _right_tensor, _right_cs, _right_kunneth])
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


def _slug(s):
    return "".join(ch if ch.isalnum() else "-" for ch in str(s)).strip("-")


def build_segments(shift=0):
    """判词片段一律由 KEY 读数机拼；shift 只加在合法机制数上，用于证明片段真吃读数。"""
    K = KEY
    return [
        "S2-RANKS-%d-%d--H%d-%d-%d"
        % (K["s2_rank_d1"], K["s2_rank_d2"],
           K["s2_H0"], K["s2_H1"], K["s2_H2"]),
        "D1D2-MAX-%d--EULER-%d-VS-%d"
        % (K["s2_d1d2_max"], K["s2_euler_chain"], K["s2_euler_homology"]),
        "CW-X-%d-CELLS--H2-%d" % (len(K["cw_X"]), K["kunneth_H2_total"]),
        "KUNNETH-M%d-CROSS%d-S%d-TOTAL%d"
        % (K["kunneth_M_part"], K["kunneth_cross_part"],
           K["kunneth_S_part"], K["kunneth_H2_total"]),
        "OUTSIDE-CROSS-%d-VS-BASE-%d"
        % (K["outside_cross_H1M_H1S"], K["baseline_cross"]),
        "FLUX-Z3-%s--INTERNAL-%s"
        % (_slug(K["z3_flux_component"]), _slug(K["internal_flux_component"])),
        "TRIALITY-T-%s--IRREPS-%d--DIMSUM-%d"
        % ("-".join(str(t) for t in K["triality_t_values"]),
           len(K["triality_table"]), sum(K["triality_dim_by_t"].values())),
        "SCHUR-WEYL-%s"
        % "-".join("K%d-SUM%d-SING%d" % (x["k"], x["sum_f_dim"], x["singlets"])
                   for x in K["tensor_table"]),
        "SINGLETS-K2-%d-K3-%d-K6-%d"
        % (K["singlets_3pow2"], K["singlets_3pow3"], K["singlets_3pow6"]),
        "Z3-KEEPS-%d--TRUE-%d--DISCRIM-%s"
        % (K["z3_proj_3pow3"], K["singlets_3pow3"],
           K["z3_discrim_3pow3"].replace("/", "-OF-")),
        "CS-%d-LEVELS--HIT3-%s"
        % (K["cs_total"], K["cs_hitrate"].replace("/", "-OF-")),
        "CS-FROZEN-%s-VS-FULL-%s"
        % (K["cs_frozen"].replace("/", "-OF-"),
           K["cs_hitrate"].replace("/", "-OF-")),
        "CS-K-MULT3-%s--DISTINCT-NMIN-%d"
        % ("-".join(str(v) for v in K["cs_k_mod3_zero"]),
           K["cs_nmin_distinct"]),
        "CHANNELS-%d--FIXERS-%d"
        % (K["channel_total"], K["channel_fixers_count"] + shift),
        "CHANNEL-UNIVERSE-%d-NAMES--LEN-%s"
        % (len(K["channel_names"]),
           "-".join(str(len(n)) for n in K["channel_names"])),
        "CHERN-INT-%d--HALF-%d--TABLE-%d"
        % (K["chern_int_legal"], K["chern_half_legal"], len(K["chern_table"])),
        "IQ3-SOLUTIONS-%d--PREV-FIXERS-%d"
        % (K["iq_three_solutions"], K["prev_internal_fixers_count"]),
        "CROSS-VOLUME-CENTER-%s--SU3-%s--RID-%s"
        % ("-".join(str(v) for v in K["prev_center_all_orders"]),
           K["prev_su3_center_group"], K["prev_rid"]),
        "PREV-ZK-K3-NMIN-%d--TABLE-%d"
        % (next(b for a, b in K["prev_zk_table"] if a == 3),
           len(K["prev_zk_table"])),
        "README-%d--R402-%d--R403-%d--FILES-%d"
        % (K["readme_bytes"], K["readme_r402_tokens"],
           K["readme_r403_tokens"], K["r403_files"]),
        "FOUR-FORCE-UNPROVEN--UNIQUE-PREDICTION-0",
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

    _a07 = [r for r in ROWS if r["id"] == "A07"][0]
    guard("IDENTITY-KIND",
          _a07["kind"] == "IDENTITY" and "定义" in _a07["exp"]
          and COUNTS.get("IDENTITY", 0) == 1,
          "A07 kind=%s；exp 含定义=%s；IDENTITY 共 %d 条"
          % (_a07["kind"], "定义" in _a07["exp"], COUNTS.get("IDENTITY", 0)))

    _b06 = [r for r in ROWS if r["id"] == "B06"][0]
    guard("DECLARED-NEG",
          "B06" in DECLARED_SET and _b06["kind"] == "FAIL"
          and all(any(r["id"] == x for r in ROWS) for x in DECLARED_NEG),
          "已登记判负 %s；B06 kind=%s" % (str(DECLARED_NEG), _b06["kind"]))

    guard("OK-DIRECTION",
          _b06_ok == (KEY["channel_fixers_count"] > 0)
          and _b06["kind"] == "FAIL"
          and KEY["channel_fixers_count"] == 0,
          "B06 问是否存在故 ok 须由 fixers 大于零驱动；实测 fixers=%d、ok=%s、kind=%s"
          % (KEY["channel_fixers_count"], _b06_ok, _b06["kind"]))

    guard("KEY-TABLE-TWO-PATH",
          KEY["key_table_same"] and len(KEY["key_table_left"]) > 100
          and len(_left_triality) == len(_right_triality) == 8
          and len(_left_tensor) == len(_right_tensor) == 3
          and len(_left_cs) == len(_right_cs) == 9
          and _left_triality == _right_triality
          and _left_tensor == _right_tensor
          and _left_cs == _right_cs
          and _left_kunneth == _right_kunneth,
          "左右两路现场重算：triality %d 行 / 张量幂 %d 档 / CS %d 档 / Kunneth 4 项；一致=%s"
          % (len(_left_triality), len(_left_tensor), len(_left_cs),
             KEY["key_table_same"]))

    _native = no_native_violation(back)
    guard("JSON-NATIVE", len(_native) == 0,
          "非原生类型命中 %d：%s" % (len(_native), str(_native)[:120]))

    _s0 = build_segments(0)
    _s1 = build_segments(1)
    guard("VERDICT-MACHINE",
          len(_s0) >= 15 and len(set(_s0)) == len(_s0)
          and "__".join(_s0) != "__".join(_s1),
          "片段 %d 个；读数加一后判词串变化=%s"
          % (len(_s0), "__".join(_s0) != "__".join(_s1)))

    _zero = [r for r in ROWS if "=0" in r["act"]]
    guard("ZERO-READOUT-DENOMINATOR",
          len(_zero) >= 1
          and all(("分母" in r["note"] or "维数" in r["note"]) for r in _zero),
          "act 含零读数 %d 条 %s；分母或维数标注齐备=%s"
          % (len(_zero), [r["id"] for r in _zero],
             all(("分母" in r["note"] or "维数" in r["note"]) for r in _zero)))

    guard("CHAIN-COMPLEX-EXACT",
          KEY["s2_chain_condition"] and KEY["s2_d1d2_max"] == 0
          and KEY["s2_euler_chain"] == KEY["s2_euler_homology"]
          and (KEY["s2_H0"], KEY["s2_H1"], KEY["s2_H2"]) == (1, 0, 1)
          and (KEY["s2_rank_d1"], KEY["s2_rank_d2"]) == (3, 3)
          and _a01_ok and _a02_ok,
          "F_3 上 d1 秩 %d / d2 秩 %d；d1 复合 d2 最大元 %d；链欧拉数 %d 对同调欧拉数 %d"
          % (KEY["s2_rank_d1"], KEY["s2_rank_d2"], KEY["s2_d1d2_max"],
             KEY["s2_euler_chain"], KEY["s2_euler_homology"]))

    _cross_recomputed = CW_M4[1] * CW_S2[1]
    guard("KUNNETH-CROSS-DRIVEN-BY-H1",
          KEY["kunneth_cross_part"] == _cross_recomputed
          and KEY["kunneth_M_part"] + _cross_recomputed + KEY["kunneth_S_part"]
          == KEY["kunneth_H2_total"] == 3
          and KEY["kunneth_cross_driven_by_H1"]
          and KEY["s2_H1"] == 0
          and KEY["outside_cross_H1M_H1S"] == 8
          and _a03_ok and _a04_ok and _a05_ok,
          "交叉项 %d 由 H^1(M_4) 乘 H^1(S^2) 现场重算得 %d；换 T^2 与 T^4 后为 %d"
          % (KEY["kunneth_cross_part"], _cross_recomputed,
             KEY["outside_cross_H1M_H1S"]))

    _cross_sens = (CW_M4[1] + 1) * (CW_S2[1] + 1)
    guard("PREDICATE-SENSITIVITY",
          _cross_recomputed == 0 and _cross_sens == 1
          and _cross_sens != _cross_recomputed,
          "给两侧 H^1 各添一个生成元，交叉项从 %d 变 %d；判据不是结构恒零"
          % (_cross_recomputed, _cross_sens))

    _dim_indep = sum((p + 1) * (q + 1) * (p + q + 2) // 2
                     for (p, q), _nm in IRREPS)
    guard("TRIALITY-THREE-CLASSES",
          KEY["triality_t_values"] == [0, 1, 2]
          and sum(KEY["triality_dim_by_t"].values()) == _dim_indep == 52
          and [x for x in KEY["triality_table"] if x["name"] == "3"][0]["t"] == 1
          and [x for x in KEY["triality_table"] if x["name"] == "3bar"][0]["t"] == 2
          and _b01_ok,
          "八个最低表示 t 集合 %s；维数和现场重算 %d 对缓存 %d；3 与 3bar 的 t 分属两类"
          % (KEY["triality_t_values"], _dim_indep,
             sum(KEY["triality_dim_by_t"].values())))

    _sum_recomputed = all(
        sum(r["f"] * r["dim"] for r in x["rows"]) == x["sum_f_dim"] == 3 ** x["k"]
        for x in KEY["tensor_table"])
    guard("SCHUR-WEYL-SUM",
          _sum_recomputed and KEY["singlets_3pow2"] == 0
          and KEY["singlets_3pow3"] == 1 and KEY["singlets_3pow6"] == 5
          and _b02_ok,
          "三档 f 乘 dim 逐行回代 %s；单态数 %s"
          % (_sum_recomputed,
             [x["singlets"] for x in KEY["tensor_table"]]))

    guard("Z3-DISCRIM-POWER",
          KEY["z3_proj_3pow3"] == 27 and KEY["singlets_3pow3"] == 1
          and KEY["z3_discrim_3pow3"] == "1/27"
          and KEY["z3_proj_3pow3"] > KEY["singlets_3pow3"]
          and _b03_ok and _b04_ok and _b05_ok and _k2_ok,
          "Z_3 投影保留 %d 而真单态 %d；判别力 %s；三档投影读数两两不同"
          % (KEY["z3_proj_3pow3"], KEY["singlets_3pow3"],
             KEY["z3_discrim_3pow3"]))

    guard("CS-TWO-SIDES",
          KEY["cs_total"] == 9 and KEY["cs_hit3"] == 6
          and KEY["cs_nmin_distinct"] == 2
          and not KEY["cs_k_independent"]
          and KEY["cs_frozen"] != KEY["cs_hitrate"]
          and KEY["cs_k_mod3_zero"] == [3, 6, 9]
          and KEY["cs_nmin_for_k1"] == 3 and KEY["cs_nmin_for_k3"] == 1
          and _b07_ok and _b08_ok and _k3_ok and _k4_ok,
          "九档 k 给 n_min 两种取值；命中 3 的 %s，冻结一档 %s；k 为 3 的倍数时约束消失"
          % (KEY["cs_hitrate"], KEY["cs_frozen"]))

    _names = KEY["channel_names"]
    guard("CHANNEL-UNIVERSE-LISTED",
          len(_names) == 3 and len(set(_names)) == 3
          and KEY["channel_total"] == 3
          and str(_names) in _b06["act"]
          and KEY["kunneth_cross_part"] == 0
          and KEY["s2_H1"] == 0
          and not KEY["cs_k_independent"]
          and KEY["channel_fixers_count"] == 0
          and KEY["channel_fixers"] == [],
          "报不存在前先列对象全集 %s；三条通道的关闭条件分别为交叉项 %d、H^1 %d、n_min 随 k 取 %d 种值"
          % (str(_names), KEY["kunneth_cross_part"], KEY["s2_H1"],
             KEY["cs_nmin_distinct"]))

    _alt_cross = CW_T4[1] * CW_T2[1]
    _alt_fixers = (int(_alt_cross > 0) + int(CW_T2[1] > 0)
                   + int(KEY["cs_k_independent"]
                         and KEY["cs_hit3"] == KEY["cs_total"]))
    guard("FIXER-PREDICATE-SENSITIVE",
          _alt_cross == 8 and _alt_fixers == 2
          and KEY["channel_fixers_count"] == 0
          and _alt_fixers != KEY["channel_fixers_count"],
          "换成 T^2 与 T^4 后交叉项 %d、H^1 %d ⇒ 合法机制数由 %d 变 %d；零结论不是写死"
          % (_alt_cross, CW_T2[1], KEY["channel_fixers_count"], _alt_fixers))

    guard("CHERN-INTEGRALITY",
          KEY["chern_int_legal"] == 3 and KEY["chern_half_legal"] == 0
          and len(KEY["chern_table"]) == 6
          and KEY["iq_three_solutions"] == 0
          and _c03_ok and _c04_ok,
          "磁通表 %s；整数合法 %d、半整数合法 %d；I_Q=3 整数网格解 %d"
          % (KEY["chern_table"], KEY["chern_int_legal"],
             KEY["chern_half_legal"], KEY["iq_three_solutions"]))

    _prev2 = json.load(io.open(_PREV_JS, "r", encoding="utf-8"))
    guard("CROSS-VOLUME-READBACK",
          _prev2["key_numbers"]["center_all_orders"] == KEY["prev_center_all_orders"]
          and _prev2["key_numbers"]["su3_center_group"] == KEY["prev_su3_center_group"]
          and _prev2["key_numbers"]["internal_fixers_count"]
          == KEY["prev_internal_fixers_count"] == 0
          and _prev2["rid"] == KEY["prev_rid"] == "NONE-NO-RID"
          and [x for x in KEY["prev_zk_table"] if x[0] == 3] == [[3, 3]]
          and len(KEY["prev_zk_table"]) == 8
          and _b09_ok and _c05_ok,
          "重新打开上一册 JSON 独立比对：中心阶 %s、色群中心 %s、内部机制 %d、Z_k 表 %d 档中 k=3 给 n_min=3"
          % (KEY["prev_center_all_orders"], KEY["prev_su3_center_group"],
             KEY["prev_internal_fixers_count"], len(KEY["prev_zk_table"])))

    _c06 = [r for r in ROWS if r["id"] == "C06"][0]
    _d03 = [r for r in ROWS if r["id"] == "D03"][0]
    guard("NOT-UNIVERSAL-TAGGED",
          _c06["kind"] == "INFO" and "不是全称否证" in _c06["note"]
          and "不声称任何统一模型" in _d03["note"]
          and KEY["channel_total"] == 3,
          "C06 note 含不是全称否证=%s；D03 note 含不声称任何统一模型=%s"
          % ("不是全称否证" in _c06["note"], "不声称任何统一模型" in _d03["note"]))

    _rd_bytes = io.open(RD, "rb").read()
    guard("NO-NEW-RID-NO-README",
          KEY["readme_r403_tokens"] == 0 and KEY["r403_files"] == 0
          and KEY["readme_r402_tokens"] == 2
          and b"X-V63-12" not in _rd_bytes
          and b"TUFT-r403_" not in _rd_bytes,
          "README %d B；r402 锚点 %d；r403 锚点 %d；三树 r403 文件 %d；本册未登记"
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

    K = KEY
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
        L.append("  [%-3s] %-30s | %s" % ("ok" if g["ok"] else "BAD", g["name"], g["detail"]))
    L.append("")
    L.append("【关键表 · 两路机拼】")
    for i, x in enumerate(K["triality_table"]):
        L.append("  triality %-5s t=%d dim=%d 左路 %s | 右路 %s"
                 % (x["name"], x["t"], x["dim"],
                    str(_left_triality[i]), str(_right_triality[i])))
    for i, x in enumerate(K["tensor_table"]):
        L.append("  张量幂 k=%d 和/单态/投影 左路 %s | 右路 %s"
                 % (x["k"], str(_left_tensor[i]), str(_right_tensor[i])))
    for i, x in enumerate(K["cs_table"]):
        L.append("  CS 级 k=%d n_min 左路 %s | 右路 %s"
                 % (x["k"], str(_left_cs[i]), str(_right_cs[i])))
    L.append("  Kunneth M/交叉/S/总 左路 %s | 右路 %s"
             % (str(_left_kunneth), str(_right_kunneth)))
    L.append("  两路一致 = " + str(K["key_table_same"]))
    L.append("")
    L.append("【关键数字】")
    L.append("  S^2 四面体边界单纯复形：d1 秩 %d / d2 秩 %d；H^0=%d H^1=%d H^2=%d；链条件最大元 %d"
             % (K["s2_rank_d1"], K["s2_rank_d2"], K["s2_H0"],
                K["s2_H1"], K["s2_H2"], K["s2_d1d2_max"]))
    L.append("  最小 CW 链维数表 %s；H^2 总维数 %d = M 分量 %d + 交叉 %d + S 分量 %d"
             % (K["cw_X"], K["kunneth_H2_total"], K["kunneth_M_part"],
                K["kunneth_cross_part"], K["kunneth_S_part"]))
    L.append("  色 Z_3 磁通属于 %s；内部 U(1) 磁通属于 %s；交叉项 %d"
             % (K["z3_flux_component"], K["internal_flux_component"],
                K["kunneth_cross_part"]))
    L.append("  范围外：T^2 的 H^1=%d、T^4 的 H^1=%d ⇒ 交叉项 %d（基线 %d）"
             % (K["outside_T2_H1"], K["outside_T4_H1"],
                K["outside_cross_H1M_H1S"], K["baseline_cross"]))
    L.append("  triality 表 %s；t 集合 %s；按 t 的维数和 %s"
             % ([(x["name"], x["t"]) for x in K["triality_table"]],
                K["triality_t_values"], K["triality_dim_by_t"]))
    L.append("  Schur-Weyl 三档 %s；真色单态 %s"
             % ([(x["k"], x["sum_f_dim"], x["singlets"]) for x in K["tensor_table"]],
                [x["singlets"] for x in K["tensor_table"]]))
    L.append("  Z_3 中心投影保留 %d/%d；真单态 %d；判别力 %s"
             % (K["z3_proj_3pow3"], 27, K["singlets_3pow3"],
                K["z3_discrim_3pow3"]))
    L.append("  CS 级表 %s；命中 n_min=3 的 %s；冻结一档 %s；n_min 取值 %d 种"
             % ([(x["k"], x["n_min"]) for x in K["cs_table"]],
                K["cs_hitrate"], K["cs_frozen"], K["cs_nmin_distinct"]))
    L.append("  k 为 3 的倍数的档 %s 给 n_min=%d；k=1 给 n_min=%d"
             % (K["cs_k_mod3_zero"], K["cs_nmin_for_k3"], K["cs_nmin_for_k1"]))
    L.append("  通道全集 %s；合法机制 %d/%d；关闭条件读数交叉项 %d、H^1 %d、CS 级随 k 漂移=%s"
             % (str(K["channel_names"]), K["channel_fixers_count"],
                K["channel_total"], K["kunneth_cross_part"], K["s2_H1"],
                not K["cs_k_independent"]))
    L.append("  陈类表 %s；整数合法 %d、半整数合法 %d；I_Q=3 整数网格解 %d"
             % (K["chern_table"], K["chern_int_legal"],
                K["chern_half_legal"], K["iq_three_solutions"]))
    L.append("  跨册反抄：Spin(2n) 中心阶 %s；色群中心 %s；Z_k 表 %s；内部机制 %d；rid %s"
             % (K["prev_center_all_orders"], K["prev_su3_center_group"],
                str(K["prev_zk_table"]), K["prev_internal_fixers_count"],
                K["prev_rid"]))
    L.append("  README %d B / r402 锚点 %d / r403 锚点 %d / 三树 r403 文件 %d"
             % (K["readme_bytes"], K["readme_r402_tokens"],
                K["readme_r403_tokens"], K["r403_files"]))
    L.append("")
    L.append("【诚实边界】")
    L.append("  1. 只产可算判决，不产新物理；独立实验预言 0。")
    L.append("  2. 严格结论只覆盖 4D M_4=S^2xS^2、内部空间 S^2、F_3 系数、最小 CW 链复形三条明示通道。")
    L.append("  3. 非平凡内部丛、非 Abel 涡旋、Spin 结构与 Wilson line 全账、完整 6D 反常账未算。")
    L.append("  4. CS 级 k 只作自由输入枚举，未由作用量推导；若 k 由理论内部给出，B06 需重判。")
    L.append("  5. 不是全称否证：不声称任何统一模型都不可能把色中心与内部磁通联系。")
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
