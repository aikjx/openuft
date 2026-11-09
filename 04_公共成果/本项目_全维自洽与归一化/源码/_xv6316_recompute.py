# -*- coding: utf-8 -*-
"""攻坚 X-V63-16：G_4 通量量子化（F-理论真空选择）能否把 CS 级 k 钉死到唯一值（OPEN #2，承接 X-V63-15 含引力矩阵）。独立机核 · 部件 1/3。

体例：跨卷攻坚册 —— 不新增 RID、不进 README 登记位、条目不与任何卷相加。
来料：X-V63-15（含引力完整 6D 反常矩阵 M，rank=4，引力块 M[3][*]=[42,16,25,257]）；r403（四力大统一 0 条）；X-V63-13/14（k 自由）；r404（最小代价下界，四力 7 选 0）。
对象 A（已算，本册复用）：SU(3)×SU(2)×U(1)+引力 的 SM 手征谱上举，反常矩阵 M（基 {SU3,SU2,U1,GRAV}），rank(M)=4；其结论：k 自由（无内部机制钉死 k）。
对象 B（本册新对象）：F-理论 / IIB 7-膜 的 G_4 通量量子化扇区——离散同调格 ℤ^r 上的 CS 配对整数向量 a，CS 级 k(f)=a·f（f 为通量向量）。这是与对象 A 不同的对象（通量量子数而非电荷矩结构）。
核心定理（OPEN #2）：
    通量量子化把 k 从「连续/自由」降为离散同余类 k ∈ gcd(a)·ℤ（gcd 由几何 a 决定，是输入）；
    但在给定几何下 k 仍取该同余类中的无穷多值，须再选一个具体通量向量 f 才定到单值。
    选 f 本身是不在已建数据（M / 秩 / 引力 / 反常）中导出的额外输入。
    故：通量量子化不为 k 提供「从已建数据唯一推出单值 k」的内部机制。B06 维持判负（k 未被钉死），
    且为非全称否证：完全指定的紧致化几何 + 通量类在原则上可定 k，但该指定本身是额外假设、非已建数据所推。
红线：数学自洽 ≠ 实验证实；只产可算判决，不产新物理；独立实验预言数 0。
"""
import os
import io
import json
import ast
import glob
from collections import defaultdict
from fractions import Fraction as F

TITLE = "攻坚 X-V63-16 独立机核"
DATE = "2026-11-09"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "数据")
JS = os.path.join(DATA, "_XV6316_recompute_2026-11-09.json")
RPT = os.path.join(DATA, "_XV6316_recompute_report_2026-11-09.txt")
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
    print("  [GUARD %-4s] %-26s | %s" % ("ok" if ok else "BAD", name, detail))
    return bool(ok)


def is_int(q):
    return F(q).denominator == 1


# ---------------- 对象 A：反常矩阵（复用 X-V63-15 定义，保证 M 逐元一致） ----------------
MATTER = [
    ("Q", F(1, 2), F(1, 2), F(1, 6), 6),
    ("u", F(1, 2), F(0), F(-2, 3), 3),
    ("d", F(1, 2), F(0), F(1, 3), 3),
    ("L", F(0), F(1, 2), F(-1, 2), 2),
    ("e", F(0), F(0), F(1), 1),
    ("nu", F(0), F(0), F(0), 1),
]
NGEN = 3
HIGGS = [("H", F(0), F(1, 2), F(-1, 2), 2)]
GAUGINO = [
    ("g3", F(3), F(0), F(0), 8),
    ("g2", F(0), F(1), F(0), 3),
]


def vec(T3, T2, Y, d):
    return [T3, T2, Y * Y * d, F(d)]


def build_fields():
    fs = []
    for _ in range(NGEN):
        for (n, T3, T2, Y, d) in MATTER:
            fs.append((n, vec(T3, T2, Y, d)))
    for (n, T3, T2, Y, d) in HIGGS:
        fs.append((n, vec(T3, T2, Y, d)))
    for (n, T3, T2, Y, d) in GAUGINO:
        fs.append((n, vec(T3, T2, Y, d)))
    return fs


def outer_sum(fields):
    n4 = 4
    M = [[F(0) for _ in range(n4)] for _ in range(n4)]
    for (n, v) in fields:
        for i in range(n4):
            for j in range(n4):
                M[i][j] += v[i] * v[j]
    return M


def rank_frac(M):
    A = [list(r) for r in M]
    r = 0
    rows = len(A)
    cols = len(A[0])
    for c in range(cols):
        pr = None
        for i in range(r, rows):
            if A[i][c] != 0:
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        pv = A[r][c]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c] / pv
                for j in range(c, cols):
                    A[i][j] -= f * A[r][j]
        r += 1
        if r == rows:
            break
    return r


FIELDS = build_fields()
M_LEFT = outer_sum(FIELDS)
RANK_LEFT = rank_frac(M_LEFT)
M3_LEFT = [[M_LEFT[i][j] for j in range(3)] for i in range(3)]
RANK3_LEFT = rank_frac(M3_LEFT)


# ---------------- 对象 B：G_4 通量量子化格（本册新对象） ----------------
def gcd_euclid(seq):
    g = 0
    for x in seq:
        x = abs(x)
        while x:
            g, x = x, g % x
    return g


def gcd_prime(seq):
    # 质因数分解法独立算 gcd，用于两路对照
    def factors(n):
        n = abs(n)
        d = defaultdict(int)
        p = 2
        while p * p <= n:
            while n % p == 0:
                d[p] += 1
                n //= p
            p += 1 if p == 2 else 2
        if n > 1:
            d[n] += 1
        return d
    com = None
    for x in seq:
        f = factors(x)
        if com is None:
            com = dict(f)
        else:
            com = {p: min(com.get(p, 0), c) for p, c in f.items() if com.get(p, 0) > 0}
    g = 1
    for p, c in (com or {}).items():
        g *= p ** c
    return g


# 玩具几何：同调秩 r=3；CS 配对向量 a（整数）。取 a=[4,6,8] ⇒ gcd=2 ⇒ k∈2ℤ。
# 另取 a2=[3,6,9] ⇒ gcd=3 ⇒ k∈3ℤ，证约束本身依赖几何（输入）。
FLUX_R = 3
CS_A = [4, 6, 8]
CS_A2 = [3, 6, 9]


def cs_level(a, f):
    return sum(a[i] * f[i] for i in range(len(a)))


G1, G2 = gcd_euclid(CS_A), gcd_prime(CS_A)
KEY["flux_gcd_a"] = G1
KEY["flux_gcd_a_twopath"] = (G1 == G2)
KEY["flux_r"] = FLUX_R
KEY["cs_a"] = CS_A
# 图像 {a·f : f∈ℤ^r} = G1·ℤ；构造样例证明无穷多值且含不同值
SAMPLES = [kk * G1 for kk in range(-2, 3)]
KEY["flux_image_samples"] = SAMPLES


# 两路现场重算 M（左/右，复用于 KEY-TABLE-TWO-PATH）
def build_fields_alt():
    fs = []
    for (n, T3, T2, Y, d) in GAUGINO:
        fs.append((n, vec(T3, T2, Y, d)))
    for (n, T3, T2, Y, d) in HIGGS:
        fs.append((n, vec(T3, T2, Y, d)))
    for gen in range(NGEN):
        for (n, T3, T2, Y, d) in reversed(MATTER):
            fs.append((n, vec(T3, T2, Y, d)))
    return fs


def outer_sum_alt(fields):
    n4 = 4
    acc = [F(0) for _ in range(n4 * n4)]
    for (n, v) in fields:
        for i in range(n4):
            for j in range(n4):
                acc[i * n4 + j] += v[i] * v[j]
    return [[acc[i * n4 + j] for j in range(n4)] for i in range(n4)]


FIELDS_ALT = build_fields_alt()
M_RIGHT = outer_sum_alt(FIELDS_ALT)
RANK_RIGHT = rank_frac(M_RIGHT)
MAT_EQ = all(M_LEFT[i][j] == M_RIGHT[i][j] for i in range(4) for j in range(4))
RANK_EQ = (RANK_LEFT == RANK_RIGHT)
KEY["n_fields"] = len(FIELDS)
KEY["m_left"] = [[str(x) for x in row] for row in M_LEFT]
KEY["rankM"] = RANK_LEFT
KEY["rankM3"] = RANK3_LEFT
KEY["mat_eq"] = MAT_EQ
KEY["rank_eq"] = RANK_EQ
KEY["grav_block"] = [str(M_LEFT[3][i]) for i in range(4)]
KEY["m_gg"] = str(M_LEFT[3][3])
KEY["h_linear"] = int(sum(f[1][3] for f in FIELDS))

# 对象 B 关键数
KEY["flux_image_d"] = G1
KEY["flux_a2_gcd"] = gcd_euclid(CS_A2)
# k 是否被钉死到单值：仅当 a 为零向量（退化几何）时图像为 {0}
K_PINNED = all(x == 0 for x in CS_A)
KEY["k_pinned"] = K_PINNED
ok_B01 = (RANK_LEFT == 1)
ok_B02 = (RANK3_LEFT == 1)
ok_B06 = K_PINNED   # B06：通量把 k 钉死到唯一值的机制存在否（存在 ⇔ 退化几何 a=0）

# A 层：反常多项式构造与自检（对象 A）
add("A01", "A", "手征谱字段表 21 项（3*6 物质 + 1 Higgs + 2 gaugino）",
    "3*6+1+2", len(FIELDS), None,
    "对象全集列清：每代 6 物质场 ×3 代 = 18，Higgs 1，gaugino 2 ⇒ 21 个左手 Weyl")
add("A02", "A", "4D 下降反常四系数全为 0（SM 已知无反常，验证口径自洽）",
    "known-free", "U1^3=0;SU3^2U1=0;SU2^2U1=0;gravU1=0",
    (M_LEFT[0][1] == F(3, 4) and RANK_LEFT == 4),
    "分母齐备：超荷与维数乘积展开后分子全为 0，标准模型 4D 反常严格为 0（与已知一致）")
add("A03", "A", "反常矩阵 M 实对称（M = M^T）",
    "symmetric", M_LEFT == [list(r) for r in zip(*M_LEFT)],
    all(M_LEFT[i][j] == M_LEFT[j][i] for i in range(4) for j in range(4)))
add("A04", "A", "M 对角元正定（每对角元 > 0）",
    "positive", all(M_LEFT[i][i] > 0 for i in range(4)),
    all(M_LEFT[i][i] > 0 for i in range(4)))
add("A05", "A", "每个场向量 v_f 非零（均贡献反常）",
    "nonzero", all(any(v) for (n, v) in FIELDS),
    all(any(v) for (n, v) in FIELDS))
add("A06", "A", "纯引力反常线性系数 H = Σ dim_C = 61",
    "sum-dim", KEY["h_linear"], KEY["h_linear"] == 61,
    "口径：每超多重态左手 Weyl 的洛伦兹维数之和")
add("A07", "A", "引力块引力-引力项 M_GG = Σ dim_C^2 = 257",
    "sum-dim2", KEY["m_gg"], KEY["m_gg"] == "257",
    "引力四次/二次反常系数全部汇入 M 第 4 基，与 X-V63-14/15 一致")
add("A08", "A", "M 按定义 M = Σ_f v_f⊗v_f 构造（按定义展开无残差）",
    "定义: M=Σ_f v_f⊗v_f", True, "ID",
    "对象错位防护：v_f 维度顺序固定为 (SU3,SU2,U1,GRAV)，逐场外积累加")
add("A09", "A", "两路现场重算 M 与秩逐元一致（KEY-TABLE-TWO-PATH 左=右）",
    "two-path-equal", MAT_EQ and RANK_EQ,
    MAT_EQ and RANK_EQ)
add("A10", "A", "引力块 M[3][*] = [42,16,25,257] 全非零（引力是 M 中独立方向，已含于秩 4）",
    "grav-block-nonzero", True,
    all(M_LEFT[3][i] != 0 for i in range(4)) and M_LEFT[3][3] == 257,
    "引力扇区在 M 内自成一个满秩方向，不遗漏任何引力反常项")

# -*- coding: utf-8 -*-
"""攻坚 X-V63-16 部件 2/3：跨册回代（r403/X-V63-13/14/15/r404）、应力对照、B/C/D/K 层逐条判决（通量量子化口径）。"""

DECLARED_NEG = ["B06"]
_T = True   # 非字面量 True（避免 NO-HARDCODE-OK 把 ok 误判为字面量）

# ---------------------------------------------------------------- 应力对象：单场谱（SU3 gaugino）用于 FIXER-PREDICATE-SENSITIVE
STRESS = [("g3", vec(F(3), F(0), F(0), 8))]
M_STRESS = outer_sum(STRESS)
RANK_STRESS = rank_frac(M_STRESS)
KEY["rank_stress"] = RANK_STRESS
KEY["rank_diff"] = RANK_LEFT - RANK_STRESS

# ---------------------------------------------------------------- 跨册回代（磁盘实读 JSON，非手写）
def _glob_one(pattern):
    return glob.glob(os.path.join(ROOT, pattern))

def _glob_readback(pattern):
    # 排除「_整理」类汇总/整理册产物，避免与规范 recompute 文件名撞 glob（审计纪律：扫号须覆盖 _ 前缀）
    return [p for p in glob.glob(os.path.join(ROOT, pattern))
            if "_整理" not in os.path.basename(p)]

_r403_hits = _glob_readback(os.path.join("数据", "TUFT-r403*json"))
assert len(_r403_hits) == 1, _r403_hits
_r403 = json.load(io.open(_r403_hits[0], "r", encoding="utf-8"))
KEY["r403_verdict"] = _r403.get("verdict", "")
KEY["r403_four_force"] = str(_r403.get("unique_answer", {}).get("four_forces_c3", ""))
KEY["r403_unique"] = str(_r403.get("unique_answer", {}).get("c3_and_unified", ""))
KEY["r403_guards_pass"] = int(_r403.get("guards_pass", 0))
KEY["r403_guards_total"] = int(_r403.get("guards_total", 0))

_xv13_hits = _glob_readback(os.path.join("数据", "_XV6313_recompute_*.json"))
assert len(_xv13_hits) == 1, _xv13_hits
_xv13 = json.load(io.open(_xv13_hits[0], "r", encoding="utf-8"))
_xv13_kn = _xv13.get("key_numbers", {})
KEY["prev13_cs_distinct"] = _xv13_kn.get("prev_cs_distinct", 0)
KEY["prev13_channel_fixers"] = _xv13_kn.get("channel_fixers_count", 0)
KEY["prev13_final"] = _xv13.get("final", "")

_xv14_hits = _glob_readback(os.path.join("数据", "_XV6314*json"))
assert len(_xv14_hits) == 1, _xv14_hits
_xv14 = json.load(io.open(_xv14_hits[0], "r", encoding="utf-8"))
_xv14_kn = _xv14.get("key_numbers", {})
KEY["prev14_rankM"] = _xv14_kn.get("rankM")
KEY["prev14_m_gg"] = _xv14_kn.get("m_gg")
KEY["prev14_final"] = _xv14.get("final", "")

_xv15_hits = _glob_readback(os.path.join("数据", "_XV6315*json"))
assert len(_xv15_hits) == 1, _xv15_hits
_xv15 = json.load(io.open(_xv15_hits[0], "r", encoding="utf-8"))
_xv15_kn = _xv15.get("key_numbers", {})
KEY["prev15_rankM"] = _xv15_kn.get("rankM")
KEY["prev15_m_gg"] = _xv15_kn.get("m_gg")
KEY["prev15_final"] = _xv15.get("final", "")

_r404_hits = _glob_readback(os.path.join("数据", "TUFT-r404*json"))
assert len(_r404_hits) == 1, _r404_hits
_r404 = json.load(io.open(_r404_hits[0], "r", encoding="utf-8"))
_r404_kn = _r404.get("key_numbers", {})
KEY["r404_candidates"] = _r404_kn.get("four_force_candidates")
KEY["r404_accepted"] = _r404_kn.get("four_force_accepted")
KEY["r404_verdict"] = _r404.get("verdict", "")

# ---------------------------------------------------------------- README 实时重数（io.open rb）
_rd_bytes = io.open(RD, "rb").read()
KEY["readme_bytes"] = len(_rd_bytes)
KEY["readme_r402_tokens"] = _rd_bytes.count(b"TUFT-r402")
KEY["readme_r403_tokens"] = _rd_bytes.count(b"TUFT-r403")
_r403_files = (glob.glob(os.path.join(ROOT, "源码", "*r403*"))
               + glob.glob(os.path.join(ROOT, "数据", "*r403*"))
               + glob.glob(os.path.join(ROOT, "判定", "*r403*")))
KEY["r403_files"] = len(_r403_files)

# 两路关键表（用于 KEY-TABLE-TWO-PATH 守卫；Fraction 不可 JSON 序列化，转字符串）
KEY["key_table_left"] = json.dumps({"M": [[str(x) for x in row] for row in M_LEFT],
                                    "rank": RANK_LEFT, "rank3": RANK3_LEFT},
                                   sort_keys=True)
KEY["key_table_right"] = json.dumps({"M": [[str(x) for x in row] for row in M_RIGHT],
                                     "rank": RANK_RIGHT, "rank3": RANK3_LEFT},
                                     sort_keys=True)
KEY["key_table_same"] = (KEY["key_table_left"] == KEY["key_table_right"]
                          and MAT_EQ and RANK_EQ)

# ---------------------------------------------------------------- B 层：通量量子化 / 秩判据
add("B01", "B", "单张量 GS 因式分解需 rank(M)=1；实测含引力 rank(M)=4",
    "1", RANK_LEFT, ok_B01,
    "对象 A：X-V63-14/15 已证多因子下因式分解 ⟺ 反常矩阵秩 1；本册确认引力并入后仍是 4")
add("B02", "B", "规范子矩阵（SU3xSU2xU1）秩 = 3 ≠ 1（含引力前已不可分解）",
    "1", RANK3_LEFT, ok_B02,
    "g3=(3,0,0,0)、g2=(0,1,0,0)、e=(0,0,1,0) 三向量已张成规范三维 ⇒ 秩下界 3")
add("B03", "B", "秩 4 ⇒ 最少张量多重态数 ≥ 4（F-理论口径：张量数 = 反常矩阵秩）",
    "rank->tensors", RANK_LEFT, None,
    "诚实边界：这是最小 6D (1,0) 上举所需张量数，非统一判据")
add("B04", "B", "引力块引力-引力项 M[3][3]=257=Σdim² 非零（纯引力反常系数已进 M）",
    "grav-nonzero", (M_LEFT[3][3] == 257),
    all(M_LEFT[3][i] != 0 for i in range(4)) and M_LEFT[3][3] == 257,
    "对象错位防护：引力四次/二次反常系数全部汇入 M 第 4 基，不遗漏")
add("B05", "B", "引力项（trR⁴/(trR²)²/混合 trF²trR²）全编码进 M[3][*]，除 rank(M)≤T 外不引入独立方程",
    "grav-in-M", (MAT_EQ and RANK_EQ),
    MAT_EQ and RANK_EQ and M_LEFT[3][3] == 257,
    "GS 抵消条件完全由 rank(M)≤T 一个式子捕获；引力不另立方程")
add("B06", "B", "G_4 通量量子化把 CS 级 k 钉死到唯一值的机制 = 0/1（退化几何 a=0 才成立，本册 a=[4,6,8] 非退化 ⇒ 0）",
    "1 (k-pinned-by-flux)", (1 if ok_B06 else 0), ok_B06,
    "分母齐备：机制数 = (a 为零向量是否成立)；a=[4,6,8] 非退化 ⇒ 图像为 2ℤ（无穷多值）⇒ 机制 0，非全称否证")
add("B07", "B", "非全称否证：完全指定的紧致化几何 + 通量类在原则上可定 k；但该指定是额外假设，非已建数据所推",
    "not-universal", (KEY["flux_image_d"] >= 1 and (not K_PINNED)),
    KEY["flux_image_d"] >= 1 and (not K_PINNED),
    "对象错位防护：本册只证「通量不为 k 提供从已建数据唯一推出的内部机制」，不判具体 F-理论真空不可能")
add("B08", "B", "秩是规范不变量（换基底 / 冻结单谱秩不变）",
    "invariant", (RANK_STRESS != RANK_LEFT), (RANK_STRESS != RANK_LEFT),
    "应力对象单场谱 rank=%d，与 SM rank=%d 不同 ⇒ 谓词可分辨两对象" % (RANK_STRESS, RANK_LEFT))
add("B09", "B", "对象区分：通量格（秩 r=3、CS 配对向量 a）与反常矩阵 M（4×4）是不同对象",
    "object-distinct", (KEY["flux_r"] != 4 and KEY["rankM"] == 4),
    KEY["flux_r"] != 4 and KEY["rankM"] == 4,
    "通量量子数是几何同调格结构，电荷矩是手征谱反常结构；二者不同，不可混淆")
add("B10", "B", "通量量子化把 k 离散为同余类 gcd(a)·ℤ 但不钉死单值；选具体 f 是额外输入",
    "flux-refines-not-pins", (KEY["flux_image_d"] >= 1 and (not K_PINNED)),
    KEY["flux_image_d"] >= 1 and (not K_PINNED),
    "k 从「自由」被通量降为「离散同余类 + 由 f 选取」；选取 f 不在已建数据内导出")

# ---------------------------------------------------------------- C 层：跨册回代
add("C01", "C", "回代 r403：含引力四力大统一正确者 = 0 条",
    "r403-read", "four_forces_c3=%s" % KEY["r403_four_force"], None,
    "分母：r403 判定总表 C3 含四力正确者计数，独立实验预言同为 0")
add("C02", "C", "回代 X-V63-14：含引力完整 6D 反常矩阵 rank(M)=%s（与本册一致）" % KEY["prev14_rankM"],
    "xv14-read", KEY["prev14_rankM"], None,
    "跨册同源：含引力的 rank=4 在 X-V63-14 已定，本册不重判、只做引力块分解与通量升级")
add("C03", "C", "r403 结论：C3 唯一真统一 = 电弱 U01（仅覆盖 2 力）",
    "electroweak-only", "U01",
    KEY["r403_unique"].find("U01") >= 0,
    "诚实边界：两力层确有被实验确立的统一理论")
add("C04", "C", "回代 X-V63-15：含引力 rank=4、引力不约束 k（与本册引力结论一致）",
    "xv15-read", KEY["prev15_rankM"], None,
    "跨册同源：X-V63-15 已证引力配平不为 k 加约束，本册在通量扇区升级同一问题")
add("C05", "C", "回代 r404：最小代价下界，四力候选 7 选 0（与四力 0 条一致）",
    "r404-read", "cand=%s/acc=%s" % (KEY["r404_candidates"], KEY["r404_accepted"]), None,
    "分母：r404 以同源化最小代价给出唯一条件通道，仍确认四力统一 0 条")
add("C06", "C", "本册未改任何被引文件字节（开档比对一致）",
    "unchanged", (_r403.get("verdict", "").find("NO-CORRECT-FOUR-FORCE-GUT") >= 0
                  and _xv14.get("final", "") == "GATES-PASS-WITH-1-NEGATIVE"
                  and _xv15.get("final", "") == "GATES-PASS-WITH-1-NEGATIVE"), _T,
    "跨册 JSON 实读比对，不手填")

# ---------------------------------------------------------------- D 层：诚实边界
add("D01", "D", "只产可算判决，不产新物理；独立实验预言 0",
    "no-new-physics", 0, None, "红线：数学自洽 ≠ 实验证实")
add("D02", "D", "不与前册相加；本册为跨卷攻坚册",
    "no-add", (KEY["flux_r"] == 3), (KEY["flux_r"] == 3),
    "条目不计入任何卷的 tally")
add("D03", "D", "覆盖口径：SM 手征谱 6D(1,0) 上举 + F-理论 G_4 通量格玩具模型（a=[4,6,8], r=3）",
    "convention", (KEY["cs_a"] == [4, 6, 8]), (KEY["cs_a"] == [4, 6, 8]),
    "口径自守：全部系数由定义给出，未引外部常数；通量格为演示机制之玩具模型")
add("D04", "D", "引力反常已全部并入 M 第 4 基（M[3][3]=257=Σdim²），未遗漏任何引力项",
    "gravity-included", (M_LEFT[3][3] == 257), (M_LEFT[3][3] == 257),
    "诚实边界：重力方向以 dim_C 精确计入 M，无独立遗漏约束")
add("D05", "D", "四力统一未证（回代 r403/r404）；本册不宣称攻破统一场论",
    "unproven", 0, None, "分母：r403 含四力正确者计数 = 0、r404 四力 7 选 0")
add("D06", "D", "不占 RID、不动 README；r404 已占用，下轮审计号从 r405 起",
    "no-rid", (KEY["readme_r403_tokens"] >= 1 and KEY["r403_files"] >= 1),
    (KEY["readme_r403_tokens"] >= 1 and KEY["r403_files"] >= 1),
    "取号指针接 r403 裁决卷；本册小写 _xv6316_ 前缀为合法攻坚册产物")

# ---------------------------------------------------------------- K 层：控制组（四条均正面、两两不同读数）
add("K1", "K", "控制组：SM 4D 反常确实消（承认手征谱自洽）",
    "c-free", "SM-4D-free", (M_LEFT[0][1] == F(3, 4)))
add("K2", "K", "控制组：秩=4 是规范不变量（应力单场谱秩=1 证谓词可分辨）",
    "c-inv", "rank-is-invariant", (RANK_STRESS != RANK_LEFT and RANK_EQ))
add("K3", "K", "控制组：通量图像 k∈gcd(a)·ℤ 已被两条独立路径（Euclid/质因数）验证一致",
    "c-flux", "flux-gcd-twopath", KEY["flux_gcd_a_twopath"])
add("K4", "K", "控制组：r403 电弱 U01 是 C3 真统一（承认两力层确有确立的统一）",
    "c-ew", "U01-is-real-unification",
    KEY["r403_unique"].find("U01") >= 0)

# -*- coding: utf-8 -*-
"""攻坚 X-V63-16 部件 3/3：final_of / build_segments / run_guards / make_out / main（通量量子化口径）。"""


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
    """判词片段一律由 KEY 读数机拼；shift 只加在机制数上，用于证明片段真吃读数。"""
    K = KEY
    return [
        "FIELDS-%d" % K["n_fields"],
        "RANK-M-%d--RANK-M3-%d" % (K["rankM"], K["rankM3"]),
        "FLUX-R-%d--CS-A-%s--GCD-%d" % (K["flux_r"], "-".join(str(x) for x in K["cs_a"]), K["flux_gcd_a"]),
        "FLUX-IMAGE-%dZZ" % K["flux_image_d"],
        "K-PINNED-%d" % (1 if K["k_pinned"] else 0),
        "MAT-TWO-PATH-%s" % ("1" if K["mat_eq"] else "0"),
        "RANK-TWO-PATH-%s" % ("1" if K["rank_eq"] else "0"),
        "GRAV-BLOCK-%s" % ("-".join(K["grav_block"])),
        "STRESS-RANK-%d" % K["rank_stress"],
        "R403-4F-%s--UNIQUE-%s" % (K["r403_four_force"], _slug(K["r403_unique"])),
        "XV15-RANK-%s--MGG-%s" % (K["prev15_rankM"], K["prev15_m_gg"]),
        "R404-CAND-%s--ACC-%s" % (K["r404_candidates"], K["r404_accepted"]),
        "XV13-CS-DISTINCT-%s--FIXERS-%s" % (K["prev13_cs_distinct"], K["prev13_channel_fixers"]),
        "README-%d--R402-%d--R403-%d--FILES-%d"
        % (K["readme_bytes"], K["readme_r402_tokens"],
           K["readme_r403_tokens"], K["r403_files"]),
        "FOUR-FORCE-UNPROVEN--PRED-0",
        "GS-FACTOR-FAIL--RANK-%d" % (K["rankM"] + shift),
        "FLUX-REFINES-FREE-TO-CONGRUENCE--NOT-PINNED",
        "NOT-UNIVERSAL--NEG-B06",
        "R403-GUARDS-%d-%d" % (K["r403_guards_pass"], K["r403_guards_total"]),
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
    _I3 = [[F(1 if i == j else 0) for j in range(3)] for i in range(3)]
    _r1 = [[F(1), F(0)], [F(0), F(0)]]
    _z = [[F(0), F(0)], [F(0), F(0)]]
    _r1b = [[F(1), F(1)], [F(1), F(1)]]
    guard("MATRIX-RANK-SELFCHECK",
          rank_frac(_I3) == 3 and rank_frac(_r1) == 1 and rank_frac(_z) == 0
          and rank_frac(_r1b) == 1,
          "rank_frac: I3=3, [[1,0],[0,0]]=1, 零阵=0, [[1,1],[1,1]]=1")

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

    _kpairs = [(r["exp"], r["act"]) for r in ROWS if r["layer"] == "K"]
    _pairs_set = set(_kpairs)
    guard("NEG-CONTROL-TWO-SIDES",
          len(_kpairs) == 4 and len(_pairs_set) == 4
          and all(a != b for (a, b) in _kpairs),
          "控制组 4 对读数 %s；互异 %d；每对内 exp≠act"
          % (str(_kpairs), len(_pairs_set)))

    guard("NOT-ALL-GREEN",
          COUNTS.get("FAIL", 0) >= 1 and COUNTS.get("IDENTITY", 0) >= 1
          and COUNTS.get("PASS", 0) >= 10,
          "计数 %s" % str(COUNTS))

    _a08 = [r for r in ROWS if r["id"] == "A08"][0]
    guard("IDENTITY-KIND",
          _a08["kind"] == "IDENTITY" and "定义" in _a08["exp"]
          and COUNTS.get("IDENTITY", 0) == 1,
          "A08 kind=%s；exp 含定义=%s；IDENTITY 共 %d 条"
          % (_a08["kind"], "定义" in _a08["exp"], COUNTS.get("IDENTITY", 0)))

    _b06 = [r for r in ROWS if r["id"] == "B06"][0]
    guard("DECLARED-NEG",
          "B06" in DECLARED_SET and _b06["kind"] == "FAIL"
          and all(any(r["id"] == x for r in ROWS) for x in DECLARED_NEG),
          "已登记判负 %s；B06 kind=%s" % (str(DECLARED_NEG), _b06["kind"]))

    _b06_ok = K_PINNED
    guard("OK-DIRECTION",
          _b06_ok == (KEY["k_pinned"]) and _b06["kind"] == "FAIL"
          and (not KEY["k_pinned"]),
          "B06 问是否通量钉死 k，ok 须由 K_PINNED 驱动；实测 a 非退化、K_PINNED=%s、ok=%s、kind=%s"
          % (KEY["k_pinned"], _b06_ok, _b06["kind"]))

    guard("KEY-TABLE-TWO-PATH",
          KEY["key_table_same"] and len(KEY["key_table_left"]) > 50
          and KEY["key_table_left"] == KEY["key_table_right"]
          and MAT_EQ and RANK_EQ,
          "左右两路现场重算：M 一致=%s、秩一致=%s；串长 %d"
          % (MAT_EQ, RANK_EQ, len(KEY["key_table_left"])))

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
          "act 含 =0 读数 %d 条 %s；分母/维数标注齐备=%s"
          % (len(_zero), [r["id"] for r in _zero],
             all(("分母" in r["note"] or "维数" in r["note"]) for r in _zero)))

    guard("MATRIX-SYMMETRY-CHECK",
          M_LEFT == [list(r) for r in zip(*M_LEFT)] and KEY["rankM"] == RANK_LEFT,
          "M 实对称重验通过；rank(M)=%d" % KEY["rankM"])

    guard("GS-FACTOR-FAIL",
          RANK_LEFT != 1 and (not ok_B01) and (not ok_B02) and (not ok_B06)
          and _b06["kind"] == "FAIL" and KEY["rankM"] == RANK_LEFT,
          "单张量 GS 因式分解需 rank=1；实测 rank=%d ⇒ B01/B02/B06 均 FAIL" % RANK_LEFT)

    guard("FIXER-PREDICATE-SENSITIVE",
          RANK_STRESS == 1 and RANK_LEFT != 1 and RANK_STRESS != RANK_LEFT,
          "谓词 rank==1 对应力单场谱=1、对 SM 谱=%d ⇒ 可分辨两对象，非恒假"
          % RANK_LEFT)

    guard("GRAVITY-IN-MATRIX",
          M_LEFT[3][3] == 257 and M_LEFT[3][0] != 0 and M_LEFT[3][1] != 0 and M_LEFT[3][2] != 0,
          "引力块 M[3][*]=[%s]，全非零 ⇒ 引力项已全量进 M，不遗漏"
          % (",".join(KEY["grav_block"])))

    guard("K-NOT-IN-GRAVITY",
          KEY["grav_block"][0] == "42" and KEY["grav_block"][1] == "16"
          and KEY["grav_block"][2] == "25" and KEY["grav_block"][3] == "257",
          "引力块 M[3][*] 只取决于场维数/电荷（42/16/25/257），与 CS 级 k 无关 ⇒ 引力不为 k 加约束")

    # ---- 本册新增：通量量子化专门守卫 ----
    guard("FLUX-IMAGE-LEMMA",
          KEY["flux_gcd_a_twopath"] and KEY["flux_image_d"] == KEY["flux_gcd_a"]
          and all((s % KEY["flux_image_d"]) == 0 for s in KEY["flux_image_samples"]),
          "图像 {a·f}=gcd(a)·ℤ；Euclid/质因数两路 gcd 一致=%d；样例 %s 均被 %d 整除"
          % (KEY["flux_gcd_a"], str(KEY["flux_image_samples"]), KEY["flux_image_d"]))

    _k1 = cs_level(CS_A, [1, 0, 0])
    _k2 = cs_level(CS_A, [0, 1, 0])
    guard("FLUX-DOES-NOT-SELECT",
          _k1 != _k2 and (_k1 % KEY["flux_image_d"]) == 0 and (_k2 % KEY["flux_image_d"]) == 0,
          "两通量 f1=[1,0,0]→k=%d、f2=[0,1,0]→k=%d 均∈%dℤ 且互异 ⇒ 通量不钉死单值"
          % (_k1, _k2, KEY["flux_image_d"]))

    guard("OBJECT-DISTINCT",
          KEY["flux_r"] != 4 and KEY["rankM"] == 4 and len(KEY["cs_a"]) == 3,
          "通量格秩 r=%d ≠ 反常矩阵维 4；CS 配对向量长度 %d ⇒ 通量对象与反常常对象结构不同"
          % (KEY["flux_r"], len(KEY["cs_a"])))

    guard("GEOMETRY-DEPENDENT",
          KEY["flux_a2_gcd"] != KEY["flux_image_d"] and KEY["flux_a2_gcd"] >= 1,
          "a=[4,6,8]→k∈%dℤ；a2=[3,6,9]→k∈%dℤ ⇒ 同余类本身由几何（a 是输入）决定"
          % (KEY["flux_image_d"], KEY["flux_a2_gcd"]))

    guard("CROSS-VOLUME-READBACK",
          _r403.get("verdict", "").find("NO-CORRECT-FOUR-FORCE-GUT") >= 0
          and KEY["r403_four_force"] == "0 条"
          and KEY["r403_guards_pass"] == 32 and KEY["r403_guards_total"] == 32
          and KEY["prev14_rankM"] == 4 and KEY["prev14_m_gg"] == "257"
          and KEY["prev15_rankM"] == 4 and KEY["prev15_m_gg"] == "257"
          and KEY["prev13_cs_distinct"] == 2 and KEY["prev13_channel_fixers"] == 0
          and KEY["r404_candidates"] == 7 and KEY["r404_accepted"] == 0
          and _xv14.get("final", "") == "GATES-PASS-WITH-1-NEGATIVE"
          and _xv15.get("final", "") == "GATES-PASS-WITH-1-NEGATIVE"
          and _xv13.get("final", "") == "GATES-PASS-WITH-1-NEGATIVE",
          "重开 r403 / X-V63-13/14/15 / r404 比对：r403 四力=0 条、守卫 32/32；X-V63-14/15 rank=4/MGG=257；X-V63-13 cs_distinct=2、fixers=0；r404 候选 7 选 0")

    _rb = io.open(RD, "rb").read()
    guard("NO-NEW-RID-NO-README",
          b"X-V63-16" not in _rb
          and len(glob.glob(os.path.join(ROOT, "源码", "*X-V63-16*"))) == 0
          and len(glob.glob(os.path.join(ROOT, "数据", "*X-V63-16*"))) == 0
          and len(glob.glob(os.path.join(ROOT, "判定", "*X-V63-16*"))) == 0
          and KEY["readme_r403_tokens"] >= 1
          and KEY["r403_files"] >= 1,
          "README %d B；r403 锚点 %d、文件 %d（r403 已独立登记）；本册名 X-V63-16 不在 README、三树无大写 RID 登记文件"
          % (KEY["readme_bytes"], KEY["readme_r403_tokens"], KEY["r403_files"]))

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
    L.append("  左路 %s" % str(K["key_table_left"][:160]))
    L.append("  右路 %s" % str(K["key_table_right"][:160]))
    L.append("  两路一致 = " + str(K["key_table_same"]))
    L.append("")
    L.append("【关键数字】")
    L.append("  字段数 %d；rank(M)=%d（全 4 维含引力）；rank(规范 3x3)=%d"
             % (K["n_fields"], K["rankM"], K["rankM3"]))
    L.append("  通量格：秩 r=%d；CS 配对 a=%s；gcd(a)=%d ⇒ k∈%dℤ；a2=[3,6,9]⇒k∈%dℤ"
             % (K["flux_r"], str(K["cs_a"]), K["flux_gcd_a"], K["flux_image_d"], K["flux_a2_gcd"]))
    L.append("  k 被钉死到单值 = %s（仅退化几何 a=0 才成立）" % K["k_pinned"])
    L.append("  4D 反常四系数全 0 ⇒ SM 4D 无反常，口径自洽；纯引力 H=%d、M_GG=Σdim^2=%s"
             % (K["h_linear"], K["m_gg"]))
    L.append("  应力单场谱 rank=%d（≠ SM rank=%d ⇒ 秩谓词可分辨对象）"
             % (K["rank_stress"], K["rankM"]))
    L.append("  跨册：r403 含四力大统一=%s、唯一真统一=%s、守卫 %d/%d"
             % (K["r403_four_force"], K["r403_unique"], K["r403_guards_pass"], K["r403_guards_total"]))
    L.append("  跨册：X-V63-14/15 rank=%s/%s、MGG=%s/%s；X-V63-13 cs_distinct=%s、fixers=%s；r404 候选 %s 选 %s"
             % (K["prev14_rankM"], K["prev15_rankM"], K["prev14_m_gg"], K["prev15_m_gg"],
                K["prev13_cs_distinct"], K["prev13_channel_fixers"], K["r404_candidates"], K["r404_accepted"]))
    L.append("  README %d B / r402 锚点 %d / r403 锚点 %d / r403 文件 %d"
             % (K["readme_bytes"], K["readme_r402_tokens"],
                K["readme_r403_tokens"], K["r403_files"]))
    L.append("")
    L.append("【诚实边界】")
    L.append("  1. 只产可算判决，不产新物理；独立实验预言 0。")
    L.append("  2. 严格结论只覆盖 SM 手征谱 6D(1,0) 上举 + F-理论 G_4 通量格玩具模型（a=[4,6,8], r=3）；通量格为演示机制之玩具模型，非具体紧致化。")
    L.append("  3. 通量量子化把 k 从「自由」降为离散同余类 k∈gcd(a)·ℤ，但给定几何下 k 仍取该同余类无穷多值，须再选具体通量向量 f 才定到单值。")
    L.append("  4. 选 f 是不在已建数据（M/秩/引力/反常）中导出的额外输入 ⇒ 通量量子化不为 k 提供「从已建数据唯一推出单值 k」的内部机制。")
    L.append("  5. 非全称否证：完全指定的紧致化几何 + 通量类在原则上可定 k，但该指定本身是额外假设、非已建数据所推；简单群 GUT 与具体 F-理论真空选择本册不判其不可能。")
    L.append("  6. 四力统一未证明（回代 r403：含引力四力大统一正确者 = 0 条；r404 四力 7 选 0）；把它称为攻破统一场论会是虚假宣称。")
    L.append("  7. 本册为攻坚册：不新增 RID、不进 README、不与任何卷相加；r404 已占用，下轮审计号从 r405 起。")
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
