# -*- coding: utf-8 -*-
"""ROOT V62 独立复算：SU(5) GUT 超荷 / 双磁通手征指标 / 792 表示分解 / D6 根系 / 16_0 不存在。

原则：不抄来料公式，用 Spin(12) 的权向量从零枚举，再与来料的断言比对。
  A 层（Fraction 精确）：SU(5) 超荷自洽、双磁通手征指标表、N_Y=0 被迫、792=C(12,5)、
                        维数账、5-form 的 U(1)_F 荷划分、D6 60 根、32 旋量权、16_0 不存在、抵消代数
  B 层（一致性）       ：14 = dim(SU3_c x SU2_L x U1_Y x U1_X x U1_F)、46 = dim(SO10 x U1_F)
  C 层（判定）        ：双磁通失败是代数事实、792-126 路线未证、492 计数不可独立核、四力未统一、18/20 不可重建
纪律：条目不可相加；纯陈述给 INFO；判据由报价/定义推导，不用任意 10 的幂；引用教科书结论 = 没算（一律 INFO）。
注：控制台避免 U+21D2(U+2192) 箭头字，防 GBK 终端 UnicodeEncodeError（承接 v61 复跑教训）。
"""
import os
import io
import json
from itertools import combinations, product
from fractions import Fraction as F

TITLE = "ROOT V62 独立复算"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

ROWS = []
GUARDS = []


def add(rid, layer, name, exp, act, ok, note=""):
    kind = "INFO" if ok is None else ("PASS" if ok else "FAIL")
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note})
    print("  [%-4s] %-5s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print("  [GUARD %-4s] %-12s | %s" % ("ok" if ok else "BAD", name, detail))
    return ok


# ================================================================ Spin(12) 权结构
# 12 维矢量的 12 个权：第 a 个坐标 -> Cartan 指标 i=(a+1)//2、符号 [+1,-1]
# U(1)_F 荷：a<=10 为 0；a=11 为 +2；a=12 为 -2（v60 归一：矢量归一）
def vec_weights():
    out = []
    for a in range(1, 13):
        i = (a + 1) // 2 - 1
        s = F(1) if a % 2 == 1 else F(-1)
        q = F(0) if a <= 10 else (F(2) if a == 11 else F(-2))
        out.append((i, s, q, a))
    return out


def dot(w, H):
    """w 是 6 维 Cartan 坐标的稀疏权 (i,s) 列表"""
    return sum(s * H[i] for i, s in w)


VW = vec_weights()
CART = [(i, s) for (i, s, q, a) in VW]          # 12 个矢量权（稀疏）
Q_OF = [q for (i, s, q, a) in VW]

# Lambda^2 的 66 个权（仅用于自检）
LAM2 = []
for a, b in combinations(range(12), 2):
    i1, s1 = CART[a]
    i2, s2 = CART[b]
    w = [] if i1 == i2 else [(i1, s1), (i2, s2)]
    q = Q_OF[a] + Q_OF[b]
    LAM2.append((w, q, a, b))

# 32 维旋量（even 手征）：6 个 +-1/2，符号乘积 = +1；U(1)_F 荷 = s[5]（v60 归一）
SPIN = []
for s in product((1, -1), repeat=6):
    if s[0] * s[1] * s[2] * s[3] * s[4] * s[5] != 1:
        continue
    w = [(i, F(s[i], 2)) for i in range(6)]
    q = F(s[5])                                  # v60 归一：旋量荷 = s[5] = +-1
    SPIN.append((w, q, s))

print("=" * 78)
print(TITLE)
print("=" * 78)

print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", (F(1, 3) + F(1, 6) - F(1, 2)) == 0, "1/3+1/6-1/2 = 0")
guard("DIM-66", len(LAM2) == 66, "Lambda^2(12) 维数 = %d" % len(LAM2))
guard("DIM-32", len(SPIN) == 32, "even 旋量维数 = %d" % len(SPIN))
_H = [F(1, 3), F(-2, 5), F(3, 7), F(1, 11), F(-2, 13), F(5, 17)]
_t12 = sum(dot([(i, sg)], _H) ** 2 for (i, sg, q, a) in VW)
guard("TR-VEC", _t12 == 2 * sum(x * x for x in _H),
      "tr_12 F^2 = 2 sum H^2 : %s vs %s" % (_t12, 2 * sum(x * x for x in _H)))

# ================================================================ A 层
print("\n[A] 精确群论：SU(5) 超荷 / 双磁通指标 / 792 分解 / 根系 / 16_0")

# A01  SU(5) GUT 超荷自洽：6 个 SM 多重态的 q_Y=6Y（Georgi-Glashow 标准值）
# 约定 Q = T3 + Y，超荷以 6Y 整数归一（与来料 (62-1) 同口径）
sm_qy = {"Q": F(1), "u^c": F(-4), "d^c": F(2), "L": F(-3), "e^c": F(6), "nu^c": F(0)}
# 内部自洽：全 SM 分量 q_Y 加权求和 = 0（GUT 生成元无迹）
#   Q: 6 分量 q=1；u^c: 3 分量 q=-4；d^c: 3 分量 q=2；L: 2 分量 q=-3；e^c: 1 q=6；nu^c: 1 q=0
weights = [("Q", 6, F(1)), ("u^c", 3, F(-4)), ("d^c", 3, F(2)),
           ("L", 2, F(-3)), ("e^c", 1, F(6)), ("nu^c", 1, F(0))]
sum_q = sum(n * q for (_, n, q) in weights)
# 5 表示 (62-1) diag(-2,-2,-2,3,3) 无迹
five = [F(-2), F(-2), F(-2), F(3), F(3)]
sum_five = sum(five)
add("A01", "A",
    "SU(5) GUT 超荷：6 个 SM 多重态 q_Y=6Y 为整数归一且整体无迹；5 表示 diag(-2,-2,-2,3,3) 无迹",
    "sum_q=0 且 sum(5)=0",
    "sum_q=%s ; sum(5)=%s ; q_Y 表 %s" % (sum_q, sum_five, {k: int(v) for k, v in sm_qy.items()}),
    sum_q == 0 and sum_five == 0,
    "=> 来料 q_Y 表与 5 表示都是无迹 SU(5) 生成元；注意 5 表示 diag 与物质量表 d^c/L 异号"
    "(5 vs 5bar 约定)，不影响 N_Y=0 结论（该结论用 10 部分的 Q=1,u^c=-4）")

# A02  双磁通手征指标表（N_F=3），报告 N_Y=1 时各分量净手征数
NF = F(3)
idx_NY1 = {k: (NF + v) for k, v in sm_qy.items()}
add("A02", "A",
    "双磁通手征指标 ind D_f = N_F + q_Y(f) N_Y（N_F=3）：N_Y=1 时各分量净手征数",
    "Q:4 u^c:-1 d^c:5 L:0 e^c:9 nu^c:3",
    "Q:%d u^c:%d d^c:%d L:%d e^c:%d nu^c:%d"
    % tuple(int(idx_NY1[k]) for k in ["Q", "u^c", "d^c", "L", "e^c", "nu^c"]),
    all(idx_NY1[k] == v for k, v in
        {"Q": 4, "u^c": -1, "d^c": 5, "L": 0, "e^c": 9, "nu^c": 3}.items()),
    "=> 非零 N_Y 把各 SM 分量拆成不同手征数（与来料表逐格一致）；只有 N_Y=0 才全为 3")

# A03  N_Y=0 被迫：令 ind(Q)=ind(u^c) => 3+N_Y = 3-4 N_Y => 5 N_Y=0 => N_Y=0（唯一）
coef = F(1) - F(-4)                            # 1 - (-4) = 5
forced = (NF + F(1) * F(0) == NF + F(-4) * F(0)) and F(0) == 0
add("A03", "A",
    "N_Y=0 被迫：令 ind(Q)=ind(u^c) => 3+N_Y = 3-4 N_Y => 5 N_Y=0 => N_Y=0（唯一解）",
    "N_Y=0 且唯一",
    "解 N_Y=%s ; 系数差 1-(-4)=%s (非0 => 唯一)" % (F(0), coef),
    forced and coef != 0,
    "=> 双磁通方案若要求 Q 与 u^c 同时恰为 3 代，则 N_Y 必为 0；任意非零 N_Y 破坏三代均等"
    "(来料 (62-4) 精确成立)")

# A04  792 = C(12,5)（SO(12) 的 5-形式反对称张量）
from math import comb
dim792 = comb(12, 5)
add("A04", "A", "792 维表示 = SO(12) 的 5-形式（反对称 5 张量），维数 C(12,5)",
    "792", "%d" % dim792, dim792 == 792,
    "=> 来料「792 维反对称张量」即 Lambda^5(R^12)，维数账精确成立（注：2-形式只有 66，非 792）")

# A05  维数账 126+126+210+210+120 = 792
dims = {"126": 126, "126bar": 126, "210+": 210, "210-": 210, "120": 120}
s = sum(dims.values())
add("A05", "A", "792 = 126_0 + 126bar_0 + 210_{+2} + 210_{-2} + 120_0：维数相加",
    "792", "%d (=126+126+210+210+120)" % s, s == 792,
    "=> 维数账精确成立；SO(10) 不可约标签（126/210/120）属引文结论，本册另用荷划分核验 (A08)")

# A06  D6 根系 60 条
nroots = 2 * 6 * (6 - 1)
add("A06", "A", "Spin(12)=D6 的根数 = 2*rank*(rank-1)",
    "60", "%d" % nroots, nroots == 60,
    "=> 来料「60 条根枚举」精确成立（rank=6）")

# A07  32 旋量权
add("A07", "A", "even 旋量权数 = 32",
    "32", "%d" % len(SPIN), len(SPIN) == 32,
    "=> 来料「32 个权核验」精确成立")

# A08  5-form 在 U(1)_F 下的荷划分（首原计算：12 个矢量权挑 5 个不同求和）
charge_count = {F(-2): 0, F(0): 0, F(2): 0}
for combo in combinations(range(12), 5):
    q = sum(Q_OF[c] for c in combo)
    charge_count[q] = charge_count.get(q, 0) + 1
cc0 = charge_count.get(F(0), 0)
ccp = charge_count.get(F(2), 0)
ccm = charge_count.get(F(-2), 0)
add("A08", "A",
    "5-form 在 U(1)_F 下的荷划分（按权枚举 12 选 5，荷 = 各矢量权 q 之和）",
    "q=0:372, q=+2:210, q=-2:210（与 126+126+120 / 210 / 210 维数吻合）",
    "q=0:%d, q=+2:%d, q=-2:%d ; 总和 %d" % (cc0, ccp, ccm, cc0 + ccp + ccm),
    cc0 == 372 and ccp == 210 and ccm == 210 and (cc0 + ccp + ccm) == 792,
    "=> 来料 792 的 U(1)_F 荷结构（+-2 各 210、0 有 372）从权枚举独立复现；"
    "每个 5-子集给出唯一和 => 权无重数 => 权数即维数，372 = 126+126+120 维数吻合"
    "（SO(10) 不可约标签仍属引文）")

# A09  16_0 不存在：Spin(12) -> SO(10) x U(1)_F 中 even 旋量荷只取 +-1（v60 归一），无 0
qs = set(q for (w, q, s) in SPIN)
has0 = any(q == 0 for (w, q, s) in SPIN)
add("A09", "A",
    "Spin(12) 的 16 (even 旋量) 在 U(1)_F 下荷只取非零值，不存在 16_0",
    "无 q=0 旋量权",
    "旋量 q 集合 %s ; 含 q=0 的权数 %d" % (sorted(int(x) for x in qs), sum(1 for (w, q, s) in SPIN if q == 0)),
    (not has0) and (F(1) in qs) and (F(-1) in qs),
    "=> SO(10) 旋量 16 的 U(1)_F 荷必非零（此处 +-1，矢量归一则是 +-2），故 §四 的「需要 16_0」"
    "在 Spin(12) 嵌入下不可得（来料第四点精确成立）；这迫使 §四 的抵消法走不通")

# A10  §四 抵消代数：I_f = (3 + q_Y N_Y) - q_Y N_Y = 3（任意 q_Y, N_Y）
okA10 = True
for q in sm_qy.values():
    for N in (F(1), F(2, 3), F(-1, 2)):
        if (3 + q * N - q * N) != 3:
            okA10 = False
add("A10", "A",
    "§四 抵消法代数：I_f = (3+q_Y N_Y) - q_Y N_Y = 3（对任意 q_Y 与 N_Y 采样）",
    "3", "化简恒等：6 个 q_Y x 3 个 N_Y 采样均得 3 = %s" % okA10,
    okA10,
    "=> 代数成立，但 §四 自己指出它仍留 10 个额外矢量对且 16_0 不可得 => 抵消法在本嵌入下失效"
    "（来料诚实记录；本册新增 A09 给出「16_0 不可能」的硬核）")

# ================================================================ B 层
print("\n[B] 一致性：未破缺规范维数")

# B01  N_Y=+-1 时未破缺维数 14 = dim(SU3_c x SU2_L x U1_Y x U1_X x U1_F)
d14 = 8 + 3 + 1 + 1 + 1
add("B01", "B",
    "N_Y=+-1 时未破缺规范维数 14 = dim(SU(3)_c)+dim(SU(2)_L)+3 x U(1)",
    "14", "%d (=8+3+1+1+1)" % d14, d14 == 14,
    "=> 与来料「14 个生成元、多两个 U(1)」维数一致；但 14 的具体生成元集合依赖超荷磁通嵌入定义"
    "（本册未重建，见 C05）")

# B02  N_Y=0 时未破缺维数 46 = dim(SO(10) x U(1)_F) = 45 + 1
d46 = 45 + 1
add("B02", "B",
    "N_Y=0 时未破缺规范维数 46 = dim(SO(10)) + dim(U(1)_F)",
    "46", "%d (=45+1)" % d46, d46 == 46,
    "=> 仅家族磁通时未破缺群恰为 SO(10) x U(1)_F（与 v60 A01 的 45_0+1_0 一致）；"
    "来料「46 个生成元、对称性过多」精确成立")

# ================================================================ C 层
print("\n[C] 判定")

add("C01", "C", "双磁通方案能否同时保持每分量恰 3 代",
    "不能（N_Y 被迫为 0，回到单磁通仍少破缺）",
    "N_Y=0 被迫 (A03)；非零 N_Y 拆裂各分量手征数 (A02)", False,
    "=> 来料核心否定结论成立：最简单双磁通修复 V60-V61 不可行；但只排除一个方案，"
    "不排除所有高维 GUT（不同内部空间/多种磁通/其他表示可能改变结论）")

add("C02", "C", "792-126 规范破缺路线是否已证可行",
    "应证 126_0 稳定凝聚 + GS/Stuckelberg 处理剩余规范玻色子",
    "未证：126_0 稳定凝聚、GS 能否给超荷无质量均未证（来料自己列）", None,
    "=> INFO：本路线是有文献先例的候选，非已证结果；本册只核验其维数账 (A04/A05) 与荷结构 (A08)")

add("C03", "C", "来料「492/492 通过」可否视为独立科学验证",
    "应给可独立复跑的逐项清单",
    "未给逐项清单（只给分类表与「492 项程序断言」）；来料自承「不能视为 492 项独立发现」", None,
    "=> INFO：本册以独立复算的 %d 条替代 492 这个计数，不追该数" % len(ROWS))

add("C04", "C", "四力统一（完整收敛）是否已证",
    "应同时得 SM 规范群 + 三代 + 量子一致 + 引力同一真空",
    "未证：来料第五节明写「完整四力统一：未证明」", None,
    "=> INFO：本轮最重要诚实边界——找到障碍与候选路线 != 统一已证")

add("C05", "C", "N_Y=+-2,+-3 的未破缺生成元 18/20 能否独立复算",
    "应给超荷磁通在 Lie 代数中的确切 Cartan 嵌入",
    "来料只给计数；超荷磁通嵌入未给出，本册无法重建 18/20", None,
    "=> INFO：18/20 随 N_Y 非单调（18<20）的物理解释需来料补嵌入定义；14 与 46 已可独立核验 (B01/B02)")

# ================================================================ 守卫与汇总
guard("DIM-PARTITION", (cc0 + ccp + ccm) == 792 and cc0 == 372 and ccp == 210 and ccm == 210,
      "5-form U(1)_F 荷划分 = 372/210/210 且总和 792")
guard("DIM-SUM-792", s == 792, "126+126+210+210+120 = 792")
guard("NO-16-0", (not has0), "旋量无 q=0 权重（16_0 不存在）")
guard("ENTRY-ACT", all(r["act"].strip() for r in ROWS), "%d 条均有 act 读数" % len(ROWS))

cnt = {}
for r in ROWS:
    cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1
gok = sum(1 for g in GUARDS if g["ok"])
print("\n" + "=" * 78)
print("条目 %d：%s" % (len(ROWS), ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt))))
print("守卫 %d/%d" % (gok, len(GUARDS)))
print("=" * 78)

VERD = ("ROOTV62_SU5_GUT_HYPERCHARGE_CANONICAL_OK__DOUBLE_FLUX_KILLS_3GEN_ALGEBRA_CONFIRMED__"
        "NY_FORCED_ZERO_UNIQUE_OK__792_EQ_C12_5_OK__DIM_SUM_126x2_210x2_120_EQ_792_OK__"
        "5FORM_U1F_PARTITION_372_210_210_OK__D6_ROOTS_60_OK__SPINOR_WEIGHTS_32_OK__"
        "NO_16_0_IN_SPIN12_OK__CANCEL_ALGEBRA_OK_BUT_FIX_FAILS__"
        "UNBROKEN_DIM_14_EQ_SMxU1xU1_OK__UNBROKEN_DIM_46_EQ_SO10xU1F_OK__"
        "DOUBLE_FLUX_SIMPLE_FIX_IMPOSSIBLE_FAIL__792_126_ROUTE_CITED_UNPROVEN_INFO__"
        "COUNT_492_UNREPRODUCED_INFO__FOUR_FORCE_NOT_PROVEN_INFO__N_Y_18_20_UNRECONSTRUCTABLE_INFO__"
        "NO_NEW_PROCESSING_LOGIC__UNIQUE_PREDICTION_0")

out = {"title": TITLE, "date": "2026-11-06", "verdict": VERD,
       "counts": cnt, "n_rows": len(ROWS),
       "guards": {"n_ok": gok, "n_total": len(GUARDS), "rows": GUARDS},
       "rows": ROWS,
       "key_numbers": {
           "sm_qy": {k: int(v) for k, v in sm_qy.items()},
           "chiral_index_NY1": {k: int(v) for k, v in idx_NY1.items()},
           "dim792": dim792,
           "dim_sum_decomp": s,
           "fiveform_charge_partition": {"q=0": cc0, "q=+2": ccp, "q=-2": ccm},
           "d6_roots": nroots,
           "spinor_weights": len(SPIN),
           "unbroken_dim_NY0": d46,
           "unbroken_dim_NY1": d14,
       }}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, "_ROOTV62_recompute_2026-11-06.json")
with io.open(jp, "w", encoding="utf-8") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1))

L = []
L.append("=" * 78)
L.append("%s  复算报告  2026-11-06" % TITLE)
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
for g in GUARDS:
    L.append("  %-16s %s | %s" % (g["name"], "ok" if g["ok"] else "BAD", g["detail"]))
rp = os.path.join(DATA, "_ROOTV62_recompute_report_2026-11-06.txt")
with io.open(rp, "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\n".join(L) + "\n")

print("\nwritten:\n  %s\n  %s" % (os.path.basename(jp), os.path.basename(rp)))
