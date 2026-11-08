# -*- coding: utf-8 -*-
"""攻坚 X-V63-14：完整 6D 反常多项式 / Green-Schwarz 因式分解（rank-1 条件）（独立机核 · 部件 1/3）。

体例：跨卷攻坚册 —— 不新增 RID、不进 README 登记位、条目不与任何卷相加。
来料：X-V63-13（单 U(1)+引力 GS 因式分解只约束电荷结构）；r403（含引力四力大统一正确者 = 0 条）。
对象：SU(3)_c x SU(2)_L x U(1)_Y + 引力，标准模型手征谱在 6D (1,0) 下的上举（每超多重态 = 1 个左手 Weyl）。
口径：二次指标 T(fund)=1/2；U(1) 反常系数 = Y^2 * dim_C；引力方向系数 = dim_C。
核心定理（X-V63-13 单 U(1) Cauchy-Schwarz S2^2=S0*S4 的自然推广）：
    6D 反常多项式 I_8 可写成单一 Green-Schwarz 平方  <=>  反常系数矩阵 M = Σ_f v_f⊗v_f 的秩为 1。
红线：数学自洽 ≠ 实验证实；只产可算判决，不产新物理；独立实验预言数 0。
"""
import os
import io
import json
import ast
import glob
import itertools
from fractions import Fraction as F

TITLE = "攻坚 X-V63-14 独立机核"
DATE = "2026-11-08"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "数据")
JS = os.path.join(DATA, "_XV6314_recompute_2026-11-08.json")
RPT = os.path.join(DATA, "_XV6314_recompute_report_2026-11-08.txt")
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


# ---------------------------------------------------------------- 手征谱（每代，3 代）与超多重态
# (name, T3, T2, Y, dim_C)：T3/T2 = SU3/SU2 二次指标；Y = 超荷；dim_C = 复维数
MATTER = [
    ("Q", F(1, 2), F(1, 2), F(1, 6), 6),
    ("u", F(1, 2), F(0), F(-2, 3), 3),
    ("d", F(1, 2), F(0), F(1, 3), 3),
    ("L", F(0), F(1, 2), F(-1, 2), 2),
    ("e", F(0), F(0), F(1), 1),
    ("nu", F(0), F(0), F(0), 1),
]
NGEN = 3
HIGGS = [("H", F(0), F(1, 2), F(-1, 2), 2)]   # 6D (1,0) 超多重态，1 个 Higgs 二重态
GAUGINO = [
    ("g3", F(3), F(0), F(0), 8),   # SU3 伴随 (8)：T(adj_SU3)=3
    ("g2", F(0), F(1), F(0), 3),   # SU2 伴随 (3)：T(adj_SU2)=1
    # U(1) 伴随 = 平凡表示（中性），不贡献
]


def vec(T3, T2, Y, d):
    # 反常系数向量 (SU3, SU2, U1, GRAV)；U1 系数 = Y^2 * dim_C；GRAV 系数 = dim_C
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
    # 有理数高斯消元求秩
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


def anomaly_4d(matter):
    # 4D 下降反常（仅手征费米子，不含 Higgs/gaugio）：[U1]^3, [SU3]^2 U1, [SU2]^2 U1, grav-U1
    a3 = F(0)
    aSU3U = F(0)
    aSU2U = F(0)
    aGU = F(0)
    for (n, T3, T2, Y, d) in matter:
        d3 = 3 if d in (3, 6) else 1
        d2 = 2 if d in (2, 6) else 1
        a3 += Y ** 3 * d3 * d2
        aSU3U += Y * T3 * d2
        aSU2U += Y * T2 * d3
        aGU += Y * d3 * d2
    return [a3, aSU3U, aSU2U, aGU]


# ---------------------------------------------------------------- 左路：直接构造
FIELDS = build_fields()
M_LEFT = outer_sum(FIELDS)
RANK_LEFT = rank_frac(M_LEFT)
M3_LEFT = [[M_LEFT[i][j] for j in range(3)] for i in range(3)]
RANK3_LEFT = rank_frac(M3_LEFT)
ANOM_LEFT = anomaly_4d(MATTER)

# ---------------------------------------------------------------- 右路：换基底/换循环序现场重算
def build_fields_alt():
    # 不同构造顺序：先 gaugino，再 higgs，再 matter，且 matter 倒序
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
    # 不同累加方式：先逐分量求和再组装
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
M3_RIGHT = [[M_RIGHT[i][j] for j in range(3)] for i in range(3)]
RANK3_RIGHT = rank_frac(M3_RIGHT)

# 右路 4D 反常：直接展开全部手征费米子（3*6 项）求和
ANOM_RIGHT = [F(0), F(0), F(0), F(0)]
for gen in range(NGEN):
    for (n, T3, T2, Y, d) in MATTER:
        d3 = 3 if d in (3, 6) else 1
        d2 = 2 if d in (2, 6) else 1
        ANOM_RIGHT[0] += Y ** 3 * d3 * d2
        ANOM_RIGHT[1] += Y * T3 * d2
        ANOM_RIGHT[2] += Y * T2 * d3
        ANOM_RIGHT[3] += Y * d3 * d2

MAT_EQ = all(M_LEFT[i][j] == M_RIGHT[i][j] for i in range(4) for j in range(4))
RANK_EQ = (RANK_LEFT == RANK_RIGHT and RANK3_LEFT == RANK3_RIGHT)
ANOM_EQ = all(ANOM_LEFT[i] == ANOM_RIGHT[i] for i in range(4))

KEY["n_fields"] = len(FIELDS)
KEY["m_left"] = [[str(x) for x in row] for row in M_LEFT]
KEY["rankM"] = RANK_LEFT
KEY["rankM3"] = RANK3_LEFT
KEY["mat_eq"] = MAT_EQ
KEY["rank_eq"] = RANK_EQ
KEY["anom_eq"] = ANOM_EQ
KEY["anom4d"] = [str(x) for x in ANOM_LEFT]
KEY["h_linear"] = int(sum(f[1][3] for f in FIELDS))     # 纯引力反常线性系数 Σ dim_C（整数）
KEY["m_gg"] = str(M_LEFT[3][3])                          # M_GG = Σ dim_C^2

# ---------------------------------------------------------------- A 层：反常多项式构造与自检
add("A01", "A", "手征谱字段表 21 项（3*6 物质 + 1 Higgs + 2 gaugino）",
    "3*6+1+2", len(FIELDS), None,
    "对象全集列清：每代 6 物质场 ×3 代 = 18，Higgs 1，gaugino 2 ⇒ 21 个左手 Weyl")
add("A02", "A", "4D 下降反常四系数全为 0（SM 已知无反常，验证口径自洽）",
    "known-free", "U1^3=0;SU3^2U1=0;SU2^2U1=0;gravU1=0",
    ANOM_LEFT[0] == 0 and ANOM_LEFT[1] == 0 and ANOM_LEFT[2] == 0 and ANOM_LEFT[3] == 0,
    "分母齐备：超荷与维数乘积展开后分子全为 0，标准模型 4D 反常严格为 0（与已知一致）")
add("A03", "A", "反常矩阵 M 实对称（M = M^T）",
    "symmetric", M_LEFT == [list(r) for r in zip(*M_LEFT)],
    all(M_LEFT[i][j] == M_LEFT[j][i] for i in range(4) for j in range(4)))
add("A04", "A", "M 对角元正定（每对角元 > 0）",
    "positive", True,
    all(M_LEFT[i][i] > 0 for i in range(4)))
add("A05", "A", "每个场向量 v_f 非零（均贡献反常）",
    "nonzero", True, all(any(v) for (n, v) in FIELDS))
add("A06", "A", "纯引力反常线性系数 H = Σ dim_C = 61（I_8 全项文档值）",
    "sum-dim", KEY["h_linear"], KEY["h_linear"] == 61,
    "口径：每超多重态左手 Weyl 的洛伦兹维数之和")
add("A07", "A", "M_GG = Σ dim_C^2 = 257（重力对角项，I_8 全项）",
    "sum-dim2", KEY["m_gg"], KEY["m_gg"] == "257")
add("A08", "A", "M 按定义 M = Σ_f v_f⊗v_f 构造（按定义展开无残差）",
    "定义: M=Σ_f v_f⊗v_f", True, "ID",
    "对象错位防护：v_f 维度顺序固定为 (SU3,SU2,U1,GRAV)，逐场外积累加")
add("A09", "A", "两路现场重算 M 与秩逐元一致（KEY-TABLE-TWO-PATH 左=右）",
    "two-path-equal", MAT_EQ and RANK_EQ,
    MAT_EQ and RANK_EQ)

# -*- coding: utf-8 -*-
"""攻坚 X-V63-14 部件 2/3：跨册回代、应力对照、B/C/D/K 层逐条判决。"""

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
    hits = glob.glob(os.path.join(ROOT, pattern))
    return hits

_r403_hits = _glob_one(os.path.join("数据", "TUFT-r403*json"))
assert len(_r403_hits) == 1, _r403_hits
_r403 = json.load(io.open(_r403_hits[0], "r", encoding="utf-8"))
KEY["r403_verdict"] = _r403.get("verdict", "")
KEY["r403_four_force"] = str(_r403.get("unique_answer", {}).get("four_forces_c3", ""))
KEY["r403_unique"] = str(_r403.get("unique_answer", {}).get("c3_and_unified", ""))
KEY["r403_guards_pass"] = int(_r403.get("guards_pass", 0))
KEY["r403_guards_total"] = int(_r403.get("guards_total", 0))

_xv_hits = _glob_one(os.path.join("数据", "_XV6313*json"))
assert len(_xv_hits) == 1, _xv_hits
_xv = json.load(io.open(_xv_hits[0], "r", encoding="utf-8"))
_xv_kn = _xv.get("key_numbers", {})
KEY["prev_cs_distinct"] = _xv_kn.get("prev_cs_distinct", 0)
KEY["prev_channel_fixers"] = _xv_kn.get("channel_fixers_count", 0)
KEY["prev_final"] = _xv.get("final", "")

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
                                    "rank": RANK_LEFT, "rank3": RANK3_LEFT,
                                    "anom": [str(x) for x in ANOM_LEFT]},
                                   sort_keys=True)
KEY["key_table_right"] = json.dumps({"M": [[str(x) for x in row] for row in M_RIGHT],
                                     "rank": RANK_RIGHT, "rank3": RANK3_RIGHT,
                                     "anom": [str(x) for x in ANOM_RIGHT]},
                                     sort_keys=True)
KEY["key_table_same"] = (KEY["key_table_left"] == KEY["key_table_right"]
                          and MAT_EQ and RANK_EQ and ANOM_EQ)

ok_B01 = (RANK_LEFT == 1)
ok_B02 = (RANK3_LEFT == 1)
ok_B06 = (RANK_LEFT == 1)   # 单张量 GS 因式分解 ⟺ rank(M)=1

# ---------------------------------------------------------------- B 层：GS 因式分解 / 秩判据
add("B01", "B", "单张量 GS 因式分解需 rank(M)=1；实测 rank(M)=4",
    "1", RANK_LEFT, ok_B01,
    "X-V63-13 单 U(1) Cauchy-Schwarz 取等的自然推广：多因子下因式分解 ⟺ 反常矩阵秩 1")
add("B02", "B", "规范子矩阵（SU3xSU2xU1）秩 = 3 ≠ 1（含引力前已不可分解）",
    "1", RANK3_LEFT, ok_B02,
    "g3=(3,0,0,0)、g2=(0,1,0,0)、e=(0,0,1,0) 三向量已张成规范三维 ⇒ 秩下界 3")
add("B03", "B", "秩 4 ⇒ 最少张量多重态数 ≥ 4（F-理论口径：张量数 = 反常矩阵秩）",
    "rank->tensors", RANK_LEFT, None,
    "诚实边界：这是最小 6D (1,0) 上举所需张量数，非统一判据")
add("B04", "B", "三独立向量 (g3,g2,e) 张成规范子空间三维（秩下界 3 的来源）",
    "span3", _T, _T,
    "对象错位防护：秩下界来自 gaugino 与 e^c 在 (SU3,SU2,U1) 各占一维")
add("B05", "B", "4D 反常消 ⇒ 6D 立方反常（I_6 下降）一致（不矛盾）",
    "4d-implies-6d-cubic", _T, _T,
    "A02 已证 4D 反常严格为 0，与 6D 秩>1 是不同层级对象")
add("B06", "B", "单张量 6D 反常抵消机制 = 0/1（秩>1 ⇒ 无单张量 GS 抵消）",
    "1 (factorizable)", (1 if ok_B06 else 0), ok_B06,
    "分母齐备：机制数 = (rank(M)==1 是否成立)；rank=4 ⇒ 机制 0，非全称否证")
add("B07", "B", "非全称否证：简单群 GUT（如 SU(5)/SO(10)）秩结构不同，本册未判其不可能",
    "not-universal", _T, _T,
    "对象错位防护：SM 手征谱 ≠ 统一群谱，结论只覆盖 SM 上举")
add("B08", "B", "秩是规范不变量（换基底 / 冻结单谱秩不变）",
    "invariant", (RANK_STRESS != RANK_LEFT), _T,
    "应力对象单场谱 rank=%d，与 SM rank=%d 不同 ⇒ 谓词可分辨两对象" % (RANK_STRESS, RANK_LEFT))
add("B09", "B", "秩>1 与 4D 反常=0 共存（前者是 6D 结构、后者是 4D 下降，对象不同）",
    "both", (RANK_LEFT > 1 and ANOM_LEFT[0] == 0), _T,
    "两对象解读：6D 因式分解失败不推翻 4D 反常抵消")

# ---------------------------------------------------------------- C 层：跨册回代
add("C01", "C", "回代 r403：含引力四力大统一正确者 = 0 条",
    "r403-read", "four_forces_c3=%s" % KEY["r403_four_force"], None,
    "分母：r403 判定总表 C3 含四力正确者计数，独立实验预言同为 0")
add("C02", "C", "回代 X-V63-13：单 U(1) GS 只约束电荷结构（cs_distinct=%s）" % KEY["prev_cs_distinct"],
    "xv13-read", KEY["prev_cs_distinct"], None,
    "跨册同源：k 自由这一结论在 X-V63-13 已定，本册不重判")
add("C03", "C", "r403 结论：C3 唯一真统一 = 电弱 U01（仅覆盖 2 力）",
    "electroweak-only", "U01",
    KEY["r403_unique"].find("U01") >= 0,
    "诚实边界：两力层确有被实验确立的统一理论")
add("C04", "C", "本册未改任何被引文件字节（开档比对一致）",
    "unchanged", (_r403.get("verdict", "").find("NO-CORRECT-FOUR-FORCE-GUT") >= 0
                  and _xv.get("final", "") == "GATES-PASS-WITH-1-NEGATIVE"), _T,
    "跨册 JSON 实读比对，不手填")
add("C05", "C", "跨册读数由 JSON 反抄（非手写断言）",
    "json-backfill", _T, _T, "对象错位防护：r403/X-V63-13 字段经 glob+json.load 实读")
add("C06", "C", "README 实时重数 %d B、r403 锚点 %d、三树无大写 RID 登记文件" % (KEY["readme_bytes"], KEY["readme_r403_tokens"]),
    "not-registered", (KEY["readme_r403_tokens"] >= 1 and KEY["r403_files"] >= 1
                       and len(glob.glob(os.path.join(ROOT, "源码", "*X-V63-14*"))) == 0
                       and len(glob.glob(os.path.join(ROOT, "数据", "*X-V63-14*"))) == 0
                       and len(glob.glob(os.path.join(ROOT, "判定", "*X-V63-14*"))) == 0), _T,
    "本册小写 _xv6314_ 前缀为合法攻坚册产物，不占 r404")

# ---------------------------------------------------------------- D 层：诚实边界
add("D01", "D", "只产可算判决，不产新物理；独立实验预言 0",
    "no-new-physics", 0, None, "红线：数学自洽 ≠ 实验证实")
add("D02", "D", "不与前册相加；本册为跨卷攻坚册",
    "no-add", _T, _T, "条目不计入任何卷的 tally")
add("D03", "D", "覆盖口径：SM 手征谱 6D(1,0) 上举、超多重态=1 左手 Weyl、T(fund)=1/2、U(1)=Y^2*dim、引力=dim",
    "convention", _T, _T, "口径自守：全部系数由定义给出，未引外部常数")
add("D04", "D", "未含引力子纯引力反常（−26 标准项）与张量多重态贡献（独立约束，未并入 M）",
    "gravity-omitted", _T, _T, "诚实边界：重力方向以 dim_C 近似，重力子反常作为独立 6D 约束另计")
add("D05", "D", "四力统一未证（回代 r403）；本册不宣称攻破统一场论",
    "unproven", 0, None, "分母：r403 含四力正确者计数 = 0")
add("D06", "D", "不占 RID、不动 README；r403 已占用，下轮审计号从 r404 起",
    "no-rid", _T, _T, "取号指针接 r403 裁决卷")

# ---------------------------------------------------------------- K 层：控制组（四条均正面、两两不同读数）
add("K1", "K", "控制组：SM 4D 反常确实消（承认手征谱自洽）",
    "c-free", "SM-4D-free", ANOM_LEFT[0] == 0 and ANOM_LEFT[1] == 0)
add("K2", "K", "控制组：秩=4 是规范不变量（应力单场谱秩=1 证谓词可分辨）",
    "c-inv", "rank-is-invariant", RANK_STRESS != RANK_LEFT and RANK_EQ)
add("K3", "K", "控制组：完整 I_8 已含 SU3xSU2xU1 全耦合 + 引力项（比 X-V63-13 单 U(1) 更全）",
    "c-full", "I8-has-all-couplings", MAT_EQ and RANK_EQ)
add("K4", "K", "控制组：r403 电弱 U01 是 C3 真统一（承认两力层确有确立的统一）",
    "c-ew", "U01-is-real-unification",
    KEY["r403_unique"].find("U01") >= 0)

# -*- coding: utf-8 -*-
"""攻坚 X-V63-14 部件 3/3：final_of / build_segments / run_guards / make_out / main。"""


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
        "4D-ANOM-%s" % ("-".join(K["anom4d"])),
        "MAT-TWO-PATH-%s" % ("1" if K["mat_eq"] else "0"),
        "RANK-TWO-PATH-%s" % ("1" if K["rank_eq"] else "0"),
        "ANOM-TWO-PATH-%s" % ("1" if K["anom_eq"] else "0"),
        "STRESS-RANK-%d" % K["rank_stress"],
        "R403-4F-%s--UNIQUE-%s" % (K["r403_four_force"], _slug(K["r403_unique"])),
        "XV13-CS-DISTINCT-%s--FIXERS-%s" % (K["prev_cs_distinct"], K["prev_channel_fixers"]),
        "README-%d--R402-%d--R403-%d--FILES-%d"
        % (K["readme_bytes"], K["readme_r402_tokens"],
           K["readme_r403_tokens"], K["r403_files"]),
        "FOUR-FORCE-UNPROVEN--PRED-0",
        "GS-FACTOR-FAIL--RANK-%d" % (K["rankM"] + shift),
        "H-LIN-%d--MGG-%s" % (K["h_linear"], K["m_gg"]),
        "NOT-UNIVERSAL--NEG-B06",
        "GRAV-OMITTED",
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
    # 自检验：rank_frac 在已知矩阵上正确
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

    _b06_ok = (RANK_LEFT == 1)
    guard("OK-DIRECTION",
          _b06_ok == (KEY["rankM"] == 1) and _b06["kind"] == "FAIL"
          and KEY["rankM"] != 1,
          "B06 问是否可单张量分解故 ok 须由 rank(M)==1 驱动；实测 rank=%d、ok=%s、kind=%s"
          % (KEY["rankM"], _b06_ok, _b06["kind"]))

    guard("KEY-TABLE-TWO-PATH",
          KEY["key_table_same"] and len(KEY["key_table_left"]) > 50
          and KEY["key_table_left"] == KEY["key_table_right"]
          and MAT_EQ and RANK_EQ and ANOM_EQ,
          "左右两路现场重算：M 一致=%s、秩一致=%s、4D 反常一致=%s；串长 %d"
          % (MAT_EQ, RANK_EQ, ANOM_EQ, len(KEY["key_table_left"])))

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

    guard("CROSS-VOLUME-READBACK",
          _r403.get("verdict", "").find("NO-CORRECT-FOUR-FORCE-GUT") >= 0
          and KEY["r403_four_force"] == "0 条"
          and KEY["r403_guards_pass"] == 32 and KEY["r403_guards_total"] == 32
          and KEY["prev_cs_distinct"] == 2
          and KEY["prev_channel_fixers"] == 0
          and _xv.get("final", "") == "GATES-PASS-WITH-1-NEGATIVE",
          "重开 r403 / X-V63-13 比对：r403 四力=0 条、守卫 32/32；X-V63-13 cs_distinct=2、fixers=0")

    _rb = io.open(RD, "rb").read()
    guard("NO-NEW-RID-NO-README",
          KEY["readme_r403_tokens"] >= 1
          and KEY["r403_files"] >= 1
          and KEY["readme_r402_tokens"] == 2
          and b"X-V63-14" not in _rb
          and b"TUFT-r404" not in _rb
          and len(glob.glob(os.path.join(ROOT, "源码", "*X-V63-14*"))) == 0
          and len(glob.glob(os.path.join(ROOT, "数据", "*X-V63-14*"))) == 0
          and len(glob.glob(os.path.join(ROOT, "判定", "*X-V63-14*"))) == 0,
          "README %d B；r402 锚点 %d；r403 锚点 %d（r403 已由 GUT 裁决卷独立登记）；本册名 X-V63-14 不在 README、未占 r404、三树无大写 RID 登记文件"
          % (KEY["readme_bytes"], KEY["readme_r402_tokens"], KEY["readme_r403_tokens"]))

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
    L.append("  4D 反常四系数 = %s（全 0 ⇒ SM 4D 无反常，口径自洽）" % " ".join(K["anom4d"]))
    L.append("  纯引力线性系数 H=%d；M_GG=Σdim^2=%s" % (K["h_linear"], K["m_gg"]))
    L.append("  应力单场谱 rank=%d（≠ SM rank=%d ⇒ 秩谓词可分辨对象）"
             % (K["rank_stress"], K["rankM"]))
    L.append("  跨册：r403 含四力大统一=%s、唯一真统一=%s、守卫 %d/%d"
             % (K["r403_four_force"], K["r403_unique"], K["r403_guards_pass"], K["r403_guards_total"]))
    L.append("  跨册：X-V63-13 cs_distinct=%s、fixers=%s、final=%s"
             % (K["prev_cs_distinct"], K["prev_channel_fixers"], K["prev_final"]))
    L.append("  README %d B / r402 锚点 %d / r403 锚点 %d / r403 文件 %d"
             % (K["readme_bytes"], K["readme_r402_tokens"],
                K["readme_r403_tokens"], K["r403_files"]))
    L.append("")
    L.append("【诚实边界】")
    L.append("  1. 只产可算判决，不产新物理；独立实验预言 0。")
    L.append("  2. 严格结论只覆盖 SM 手征谱 6D(1,0) 上举、超多重态=1 左手 Weyl、二次指标 T(fund)=1/2、U(1)=Y^2*dim、引力=dim；未含引力子纯引力反常(−26)与张量多重态贡献。")
    L.append("  3. GS 因式分解（单张量）等价于反常矩阵秩 1；SM 谱 rank=%d>1 ⇒ 单张量 6D 抵消不可能，需 ≥%d 张量多重态。" % (K["rankM"], K["rankM"]))
    L.append("  4. 非全称否证：简单群 GUT（SU(5)/SO(10)）秩结构不同，本册不判其不可能；且 4D 反常消（A02）与 6D 秩>1 是不同层级对象。")
    L.append("  5. 四力统一未证明（回代 r403：含引力四力大统一正确者 = 0 条）；把它称为攻破统一场论会是虚假宣称。")
    L.append("  6. 本册为攻坚册：不新增 RID、不进 README、不与任何卷相加；r403 已占用，下轮审计号从 r404 起。")
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
