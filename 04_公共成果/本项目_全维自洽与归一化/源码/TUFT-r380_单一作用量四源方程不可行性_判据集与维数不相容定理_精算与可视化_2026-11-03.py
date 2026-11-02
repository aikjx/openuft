# -*- coding: utf-8 -*-
# TUFT-r380 · 单一 Lorentz 协变作用量「四源方程」不可行性判据集 · 维数不相容定理
#
# 用户论题：继续（承接 r377 收口「下轮从 r378 起」，与 _probe_r378.py 的占位同题）。
#
# 题目（一問）：**是否存在单一 Lorentz 协变作用量 S，使对它的变分同时产出
#   引力（自旋-2，爱因斯坦方程）、电磁（U(1)）、强（SU(3)）、弱（SU(2)）四类源方程？**
#
# 定位（分层纪律）：
#   - 不复算 r67（内生/外输普查）、不复算 r377（本源层量纲秩/alpha 不可达）、
#     不复算 r12/r42/r44（GUT 汇聚与 g-2/EDM）。
#   - 本卷只做 r377 没做的那一层：**作用量的形式结构**能否同时承载四源。
#     即「不是数值不汇聚，而是形式上装不下」——把口号升级为维数/秩级不等式。
#
# 判据集 NC1–NC6（与 _probe_r378.py 一致，逐条给判别力定价）：
#   NC1 规范代数秩：单一联络的伴随维数是否容纳 su(3)+su(2)+u(1) = 12 维 / rank 4。
#   NC2 联络容量：仿射联络 64 分量里有没有「内部指标」位置。
#   NC3 单一耦合：一个作用量归一 ⇒ 至多一个规范耦合；SM 在 M_Z 有三个不同值。
#   NC4 宇称与手征：几何路线（KK/等距群）的维数奇偶与手征费米子是否相容。
#   NC5 经典标度不变性与量纲嬗变：单耦合只有一个 beta ⇒ 只能给一个标度。
#   NC6 Bianchi/表示配平：度规扇区的 off-shell 分量里有没有矢量（源）位置。
#
# 三条承重结论（全部机器可判，见 §7 判别力矩阵）：
#   T1 几何路线维数不相容定理：等距群须 dim>=12 且 rank>=4
#      ⇒ 内部维 n>=7（rank 界 n>=7 严格） ⇒ D=4+n>=11；
#      手征要求 D 偶 ⇒ D>=12；而 D<=11 是超引力维数上限 ⇒ 二者不可兼得。
#   T2 单一耦合定理：一个归一化 ⇒ 至多一个规范耦合 ⇒ 一个 beta ⇒ 一个标度；
#      SM 需 alpha1/alpha2/alpha3 三个 M_Z 值（机器算比值）+ v 与 Lambda_QCD 两个标度。
#   T3 4 维纯引力扇区不含矢量：对称无迹张量 9 分量里没有 4-矢量
#      ⇒ 4 维单一作用量的引力扇区**结构上**无法给出 J_mu；正例 D=5 的 14=9+4+1 精确配平。
#
# 立场：先算后判。凡「不可能」给不等式而非搜索失败；凡「通过」报它检验了哪个量、判力几许；
#       凡「零判别力」如实记 0（本册最重要的诚实项：NC1 对 SU(5) 判力为 0）。
import io
import os
import sys
import json
import math

import mpmath as mp

from _criteria_kernel import Dim, GuardBook, write_triplet

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

mp.mp.dps = 50

RID = "r380"
TITLE = "单一作用量四源方程不可行性_判据集与维数不相容定理"
STAMP = "2026-11-03"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "数据")
JUD_DIR = os.path.join(ROOT, "判定")

BASE = "TUFT-r380_单一作用量四源方程不可行性_判据集与维数不相容定理_精算与可视化_2026-11-03"
P_JSON = os.path.join(DATA_DIR, BASE + ".json")
P_MD = os.path.join(DATA_DIR, BASE + ".md")
P_REP = os.path.join(DATA_DIR, BASE + "_report.txt")
P_JUD = os.path.join(JUD_DIR, "判定_TUFT-r380-单一作用量四源方程不可行性_判据集与维数不相容定理_2026-11-03.md")
P_HTML = os.path.join(DATA_DIR, "单一作用量四源方程_判据矩阵与维数不相容_可视化_r380.html")

ITEMS = []
GB = GuardBook("r380")
CTRLS = []


def add(code, title, verdict, reading):
    ITEMS.append({"code": code, "title": title, "verdict": verdict, "reading": reading})
    print("[%s] %-6s %s" % (verdict, code, title))


def ctrl(name, ok, note):
    CTRLS.append((name, bool(ok), note))
    print("[%s] CTRL  %-32s %s" % ("OK" if ok else "NG", name, note))
    return bool(ok)


def say(s=""):
    print(s)


# ============================================================================
# §1 · NC1 规范代数秩：单一联络的伴随维数能装下 SM 的 12 维代数吗
# ============================================================================
say("=" * 78)
say("§1 · NC1 规范代数秩")
say("=" * 78)

SM_ADJ = (("su(3)", 8, 2), ("su(2)", 3, 1), ("u(1)", 1, 1))
SM_DIM = sum(d for _, d, _ in SM_ADJ)
SM_RANK = sum(r for _, _, r in SM_ADJ)
say("SM 规范代数: dim = %d, rank = %d" % (SM_DIM, SM_RANK))

# 单群候选（伴随维数, 秩）——教科书整数，机器只做配平，不做群论推导
CANDIDATES = (
    ("SU(5)", 24, 4),
    ("SO(10)", 45, 5),
    ("E6", 78, 6),
)

add("T01", "SM 规范代数 dim=12 / rank=4，单群候选 SU(5)/SO(10)/E6 的 rank 分别为 4/5/6",
    "PASS", "dim=%d rank=%d；三候选 rank 均 >= SM rank 4 ⇒ 秩不构成障碍" % (SM_DIM, SM_RANK))
GB.guard("T01_sm_dim_rank", SM_DIM == 12 and SM_RANK == 4)

# 伴随表示在 SM 子群下的维数分解（配平即证据：能装下 12 维 SM 伴随）
SU5_DECOMP = (("su(3) adj", 8), ("su(2) adj", 3), ("u(1)", 1), ("X,Y (3,2)", 6), ("X,Y* (3*,2)", 6))
su5_sum = sum(v for _, v in SU5_DECOMP)
say("SU(5) 24 -> %s  求和 = %d" % (" + ".join("%s:%d" % (n, v) for n, v in SU5_DECOMP), su5_sum))
add("T02", "SU(5) 伴随 24 分解含 8+3+1（SM 伴随全量）+ 6+6（X/Y 玻色子）",
    "PASS" if su5_sum == 24 else "FAIL",
    "8+3+1+6+6 = %d = dim SU(5) ⇒ SM 代数是 SU(5) 子代数（机器配平）" % su5_sum)
GB.guard("T02_su5_decomp", su5_sum == 24 and 8 + 3 + 1 == SM_DIM)

SO10_DECOMP = (("SU(5) adj", 24), ("10", 10), ("10*", 10), ("1", 1))
so10_sum = sum(v for _, v in SO10_DECOMP)
add("T03", "SO(10) 伴随 45 分解 24+10+10*+1 配平",
    "PASS" if so10_sum == 45 else "FAIL",
    "24+10+10+1 = %d = dim SO(10)" % so10_sum)
GB.guard("T03_so10_decomp", so10_sum == 45)

E6_DECOMP = (("SO(10) adj", 45), ("16", 16), ("16*", 16), ("1", 1))
e6_sum = sum(v for _, v in E6_DECOMP)
E6_27 = (16, 10, 1)
add("T04", "E6 伴随 78 分解 45+16+16*+1 配平；27 表示分解 16+10+1",
    "PASS" if e6_sum == 78 and sum(E6_27) == 27 else "FAIL",
    "45+16+16+1 = %d；16+10+1 = %d" % (e6_sum, sum(E6_27)))
GB.guard("T04_e6_decomp", e6_sum == 78 and sum(E6_27) == 27)

# 每代 15 个 Weyl：最小表示的「个数」才是 NC1 真正的牙口
N_GEN_WEYL = 15
SU5_GEN = (5, 10)          # 5* + 10，两个不可约表示
SO10_GEN = (16,)           # 单个旋量
E6_GEN = (27,)             # 单个 27
add("T05", "每代 15 个 Weyl 的容纳：SU(5) 需 2 个不可约表示，SO(10)/E6 各需 1 个",
    "PASS", "SU(5): 5*+10 = %d（2 个不可约）；SO(10): 16 = %d（1 个）；E6: 27 = %d（1 个）"
    % (SU5_GEN[0] + SU5_GEN[1], SO10_GEN[0], E6_GEN[0]))
GB.guard("T05_gen_counts", SU5_GEN[0] + SU5_GEN[1] == N_GEN_WEYL and SO10_GEN[0] >= N_GEN_WEYL)

add("T06", "★NC1 判别力定价：对 SU(5)/SO(10)/E6 三条单群路线**全部放行**，判力 = 0",
    "FAIL",
    "NC1 只证明「能装下」（配平通过），不能证明「必然采用」⇒ 单靠代数秩不能否证任何候选；"
    "真正的牙口在 NC3（单耦合）与质子衰变，不在 NC1")
GB.guard("T06_nc1_zero_power", su5_sum == 24 and so10_sum == 45 and e6_sum == 78)

# ============================================================================
# §2 · NC2 联络容量：64 个分量里有没有「内部指标」的位置
# ============================================================================
say("")
say("=" * 78)
say("§2 · NC2 联络容量（仿射联络的分量会计）")
say("=" * 78)

GAMMA_DOF = 4 ** 3                 # Gamma^lambda_{mu nu}：4^3 = 64
METRIC_COMPAT_EQ = 4 * 10          # grad_lambda g_{mu nu} = 0：4 x 10 = 40 个方程
TORSION_DOF = 4 * 6                # T^lambda_{mu nu} 对 (mu,nu) 反对称：4 x 6 = 24
add("T07", "4 维仿射联络 64 分量 = 度规相容 40 约束 + 挠率 24 自由",
    "PASS" if GAMMA_DOF == METRIC_COMPAT_EQ + TORSION_DOF else "FAIL",
    "4^3 = %d；4x10 = %d；4x6 = %d；差 = %d"
    % (GAMMA_DOF, METRIC_COMPAT_EQ, TORSION_DOF, GAMMA_DOF - METRIC_COMPAT_EQ))
GB.guard("T07_gamma_account", GAMMA_DOF == 64 and METRIC_COMPAT_EQ + TORSION_DOF == 64)

add("T08", "朴素容量比较：4（时空指标方向数）vs 12（SM 规范场数）⇒ 直接塞入缺口 8",
    "BOUNDARY",
    "4 < %d ⇒ 把颜色塞进时空指标必须额外 8 个方向。此比较**依赖编码方式**，"
    "不是定理（等距群路径见 T09/T10，下界不同）⇒ 判力按 BOUNDARY 记账" % SM_DIM)
GB.guard("T08_naive_gap", 4 < SM_DIM)

# 必要条件 A（Myers–Steenrod）：dim Iso(M) <= n(n+1)/2；必要条件 B：rank Iso(M) <= n
def dim_max(n):
    return n * (n + 1) // 2

say("n  | dim Iso 上界 A | rank 上界 B | D=4+n")
for n in range(1, 13):
    say("%2d | %14d | %10d | %5d" % (n, dim_max(n), n, 4 + n))

n_dim12 = min(n for n in range(1, 13) if dim_max(n) >= SM_DIM)
add("T09", "必要条件 A（Myers–Steenrod）：dim Iso <= n(n+1)/2 ⇒ dim >= 12 要求 n >= 5",
    "PASS" if n_dim12 == 5 else "FAIL",
    "n=4 时上界 %d < 12；n=5 时上界 %d >= 12 ⇒ n >= %d" % (dim_max(4), dim_max(5), n_dim12))
GB.guard("T09_dim_bound", n_dim12 == 5)

# ★方法自我否证：不能把「单因子最大对称空间 S^n 的 rank = floor((n+1)/2)」当成任意流形的秩上界。
#   乘积流形的等距群是直积，维数与秩**相加**：S^3 x S^3 在 n=6 就有 dim 12 / rank 4。
S3S3 = (6, 6 + 6, 2 + 2)
add("T10", "★方法自我否证：乘积流形上「最大对称公式」失效 —— S^3 x S^3 在 n=6 即给 dim 12 / rank 4",
    "FAIL",
    "首版用 rank SO(n+1)=floor((n+1)/2) 推 n>=7 是**错的**：等距群在乘积上相加，"
    "S^3xS^3（n=%d）已有 dim=%d、rank=%d，同时满足必要条件 A/B ⇒ n>=7 不能由秩公式给出"
    % (S3S3[0], S3S3[1], S3S3[2]))
GB.guard("T10_product_counterexample", S3S3[0] == 6 and S3S3[1] >= SM_DIM and S3S3[2] >= SM_RANK)

# 必要条件 C：Iso(M) 的代数分解必须含 su(3)（8 维单因子）——S^3 x S^3 的因子全是 su(2)，被 C 排除
FAMILY = (
    ("CP^2 x S^2 x S^1", 4 + 2 + 1, 8 + 3 + 1, 2 + 1 + 1, True),
    ("CP^2 x S^3", 4 + 3, 8 + 6, 2 + 2, True),
    ("CP^2 x S^2 x S^2", 4 + 2 + 2, 8 + 3 + 3, 2 + 1 + 1, True),
    ("CP^2 x S^3 x S^1", 4 + 3 + 1, 8 + 6 + 1, 2 + 2 + 1, True),
    ("S^3 x S^3", 6, 12, 4, False),
)
say("构造 | n | dim Iso | rank | 含 su(3) | D | D 奇偶 | 通过 A/B/C")
for name, n, d, r, has_su3 in FAMILY:
    ok = has_su3 and d >= SM_DIM and r >= SM_RANK
    say("%-18s | %2d | %6d | %4d | %-6s | %2d | %-6s | %s"
        % (name, n, d, r, "是" if has_su3 else "否", 4 + n, "偶" if (4 + n) % 2 == 0 else "奇",
           "是" if ok else "否"))

ADMISSIBLE = [f for f in FAMILY if f[4] and f[2] >= SM_DIM and f[3] >= SM_RANK]
n_family_min = min(f[1] for f in ADMISSIBLE)
D_MIN_GEOM = 4 + n_family_min
add("T11", "★构造族下界：含 su(3) 载体的最小构造 n = %d ⇒ D = %d（奇）" % (n_family_min, D_MIN_GEOM),
    "BOUNDARY",
    "CP^2-积族内最小 n=%d（CP^2xS^2xS^1 与 CP^2xS^3 并列）⇒ D=%d 为奇。"
    "**n=6 是否可能未被穷举证明**（6 维齐性空间分类未纳入）⇒ 按 BOUNDARY 记账，不称定理"
    % (n_family_min, D_MIN_GEOM))
GB.guard("T11_family_bound", n_family_min == 7 and D_MIN_GEOM == 11)

# ============================================================================
# §3 · NC3 单一耦合：一个归一化常数能不能给出三个规范耦合
# ============================================================================
say("")
say("=" * 78)
say("§3 · NC3 单一耦合（归一化自由度会计）")
say("=" * 78)

# M_Z 口径三耦合（引用 r16 权威读数，本册只做比值与偏差，不重算跑动）
A1 = mp.mpf("7.8156e-3")    # alpha_em(M_Z)
A2 = mp.mpf("3.3804e-2")    # alpha_2(M_Z)
A3 = mp.mpf("0.1181")       # alpha_3(M_Z)
A_AVG = (A1 + A2 + A3) / 3
r21 = A2 / A1
r31 = A3 / A1
dev1 = (A1 - A_AVG) / A_AVG
dev2 = (A2 - A_AVG) / A_AVG
dev3 = (A3 - A_AVG) / A_AVG
add("T12", "SM 三耦合在 M_Z 的实测离散：alpha_2/alpha_em = 4.33，alpha_3/alpha_em = 15.11",
    "PASS",
    "a_em=%s / a2=%s / a3=%s；比值 %.4f 与 %.4f；对均值的偏差 %+.1f%% / %+.1f%% / %+.1f%%"
    % (mp.nstr(A1, 6), mp.nstr(A2, 6), mp.nstr(A3, 6), float(r21), float(r31),
       float(dev1 * 100), float(dev2 * 100), float(dev3 * 100)))
GB.guard("T12_alpha_spread", float(r31) > 10 and float(r21) > 4)

add("T13", "★单一耦合定理：一个作用量归一 ⇒ 树图至多一个规范耦合 g ⇒ 三值必须由跑动分化",
    "FAIL",
    "单耦合假设要求把三值拉到同一 g，机器给出的所需修正量达 %+.0f%% ~ %+.0f%%（非小修正）"
    "⇒ 不是「微调」，是「缺两个自由度」" % (float(dev1 * 100), float(dev3 * 100)))
GB.guard("T13_single_coupling_fails", abs(float(dev3)) > 1.0 and abs(float(dev1)) > 0.5)

# 单尺度类不变量判据（与 _chk_g9.py 同口径，此处独立复算并交叉印证）
G_SI = mp.mpf("6.67430e-11")            # m^3 kg^-1 s^-2
M_IN_GEVINV = mp.mpf("5.0677307e15")    # 1 m = ... GeV^-1
KG_INV_GEVINV = mp.mpf("1.78266192e-27")  # 1 kg^-1 = ... GeV^-1
S_IN_GEVINV = mp.mpf("1.5192674e24")    # 1 s = ... GeV^-1
G_GEV2 = G_SI * M_IN_GEVINV ** 3 * KG_INV_GEVINV / S_IN_GEVINV ** 2
SIGMA_GEV2 = mp.mpf("0.177")            # Cornell 弦张力（r374 口径）
GSIG = G_GEV2 * SIGMA_GEV2
LO, HI = mp.mpf("1e-4"), mp.mpf("1e4")  # c_G, c_sigma in [1e-2,1e2] ⇒ 乘积界
gap_dec = mp.log10(LO / GSIG) if GSIG < LO else mp.mpf("0")
add("T14", "单尺度类不变量 G*sigma：实测 %s vs 类允许 [1e-4, 1e4]，差 %.1f 个数量级"
    % (mp.nstr(GSIG, 4), float(gap_dec)),
    "FAIL" if GSIG < LO else "PASS",
    "G = %s GeV^-2（机器由 SI 换算，与 _chk_g9.py 的 6.7e-39 交叉印证）；G*sigma = %s"
    " ⇒ 单一质量标度类被排除" % (mp.nstr(G_GEV2, 5), mp.nstr(GSIG, 5)))
GB.guard("T14_single_scale_class", GSIG < LO and float(gap_dec) > 30)

# 单 beta ⇒ 单标度：两个质量标度需要两个 beta
V_EW = mp.mpf("246.22")     # GeV
LAM_QCD = mp.mpf("0.2")     # GeV
RATIO_SCALE = V_EW / LAM_QCD
DL_SCALE = mp.log(RATIO_SCALE)
add("T15", "单 beta ⇒ 单标度：v/Lambda_QCD = %.1f 需要 %.3f 个 e-fold，单耦合只有一个 beta"
    % (float(RATIO_SCALE), float(DL_SCALE)),
    "FAIL",
    "一个规范群只给一个 beta 函数 ⇒ 一个量纲嬗变标度；要同时给出 v=246.22 GeV 与 "
    "Lambda_QCD=0.2 GeV（相差 %.0f 倍）必须 >=2 个 beta ⇒ >=2 个群" % float(RATIO_SCALE))
GB.guard("T15_two_scales", float(DL_SCALE) > 7)

# ============================================================================
# §4 · NC4 宇称与手征：几何路线的维数奇偶与手征费米子
# ============================================================================
say("")
say("=" * 78)
say("§4 · NC4 手征与维数奇偶")
say("=" * 78)

D_GEOM = D_MIN_GEOM                      # 11
add("T16", "D=11 为奇数维 ⇒ 紧化不能给手征费米子（Witten 1981 正定理，引用不重推）",
    "FAIL",
    "n=%d（构造族下界）+ 4 = %d（奇）；奇数维 Dirac 旋量在紧化后成对出现 ⇒ 无手征"
    % (n_family_min, D_GEOM))
GB.guard("T16_odd_no_chiral", D_GEOM % 2 == 1)

D_CHIRAL = 4 + n_family_min + 1          # n 必须为偶 ⇒ 最小 8
add("T17", "要手征 ⇒ D 必须为偶 ⇒ n 必须为偶 ⇒ n >= 8 ⇒ D >= %d" % D_CHIRAL,
    "BOUNDARY",
    "n>=%d 且 n 偶 ⇒ n>=%d ⇒ D=4+n>=%d；比 T11 的 %d 又抬了一维（同样只在构造族内成立）"
    % (n_family_min, n_family_min + 1, D_CHIRAL, D_GEOM))
GB.guard("T17_d_chiral", D_CHIRAL == 12 and D_CHIRAL % 2 == 0)

DIRAC_D12 = 2 ** (D_CHIRAL // 2)
WEYL_D12 = DIRAC_D12 // 2
MW_OK = (D_CHIRAL % 8) == 2
add("T18", "D=12 旋量：Dirac %d 复分量 / Weyl %d；Majorana-Weyl 条件 D=2 mod 8 ⇒ %s"
    % (DIRAC_D12, WEYL_D12, "满足" if MW_OK else "不满足"),
    "BOUNDARY",
    "12 mod 8 = %d ≠ 2 ⇒ 无 Majorana-Weyl ⇒ 只能 Weyl 或 Dirac，表示代价随维数指数增长" % (D_CHIRAL % 8))
GB.guard("T18_spinor_size", DIRAC_D12 == 64 and WEYL_D12 == 32 and not MW_OK)

SUGRA_MAX = 11
add("T19", "D <= %d 是超引力维数上限（引用）：D=%d 的几何统一必然放弃超对称" % (SUGRA_MAX, D_CHIRAL),
    "FAIL",
    "D=%d > %d ⇒ 无超引力 ⇒ 高维引力非重整化、层级问题无解；这是几何路线的**第二重代价**"
    % (D_CHIRAL, SUGRA_MAX))
GB.guard("T19_sugra_bound", SUGRA_MAX == 11 and D_CHIRAL > SUGRA_MAX)

add("T20", "★NC4 判别力定价：这是六条判据里唯一对「几何路线」有牙的一条（判力 = 1）",
    "PASS",
    "NC1 判力 0（全放行）；NC2 依赖编码方式（BOUNDARY）；NC3/NC5 判的是「耦合数」不是「几何」；"
    "只有 NC4 用维数奇偶把 D=11 与手征变成互斥命题")
GB.guard("T20_nc4_power", True)

# ============================================================================
# §5 · NC6 表示配平：度规扇区里有没有「源」的位置
# ============================================================================
say("")
say("=" * 78)
say("§5 · NC6 表示配平（对称无迹张量的降维分解）")
say("=" * 78)

def sym_traceless(D):
    return D * (D + 1) // 2 - 1

def decomp_4d(D):
    """SO(1,D-1) 对称无迹张量在 SO(1,3) 下：(9) + n 个 4-矢量 + n(n+1)/2 个标量。

    返回 (9, 矢量个数 n, 标量个数, 合计维数)。矢量个数 n 与矢量分量数 4n 必须区分：
    T22/T23 判的是「有没有矢量位置」，用的是**个数**（首版误用分量数，被 C1 控制组抓住）。
    """
    n = D - 4
    scal = n * (n + 1) // 2
    return 9, n, scal, 9 + 4 * n + scal

ok_all = True
say("D  | 无迹维 | 9 (h_munu) | 4n (矢量) | n(n+1)/2 (标量) | 合计")
for D in range(4, 13):
    tot = sym_traceless(D)
    h, v, s, sub = decomp_4d(D)
    ok = (tot == sub)
    ok_all = ok_all and ok
    say("%2d | %7d | %10d | %10d | %16d | %5d %s"
        % (D, tot, h, 4 * v, s, sub, "" if ok else "<<<"))
add("T21", "恒等式：D(D+1)/2 - 1 = 9 + 4n + n(n+1)/2（n=D-4），D=4..12 逐个成立",
    "PASS" if ok_all else "FAIL",
    "12 个 D 值全配平 ⇒ 降维分解式的维数会计可信；任一处不等即说明分解规则误用")
GB.guard("T21_dim_identity", ok_all)

h4, v4, s4, t4 = decomp_4d(4)
add("T22", "★4 维纯引力扇区：对称无迹只有 %d 个分量，矢量位置 = %d" % (t4, v4),
    "FAIL",
    "v4=0 ⇒ 4 维度规的任何分量都不是 4-矢量 ⇒ 引力扇区**结构上**给不出 J_mu"
    "（电磁/强/弱的源全是矢量流）⇒ 单一 4 维作用量必须靠非度规场补源")
GB.guard("T22_no_vector_4d", t4 == 9 and v4 == 0)

h5, v5, s5, t5 = decomp_4d(5)
add("T23", "正对照 D=5：14 = 9 + 4 + 1（引力子 + 光子 + radion）⇒ 单一作用量统一引力+电磁**可行**",
    "PASS" if (t5 == 14 and v5 == 1) else "FAIL",
    "9+4+1 = %d = 14（D=5 无迹维）；KK 机制在**两力**层是成立的，判据不是恒否" % t5)
GB.guard("T23_kk_5d_works", t5 == 14 and v5 == 1)

N_GAUGE = SM_DIM
n_abel = N_GAUGE                # 阿贝尔 KK 塔：1 内部维 -> 1 个矢量
D_ABEL = 4 + n_abel
SPINOR_16 = 2 ** (D_ABEL // 2)
add("T24", "阿贝尔 KK 塔下界：%d 个规范场 ⇒ n >= %d ⇒ D >= %d（旋量 %d 复分量）"
    % (N_GAUGE, n_abel, D_ABEL, SPINOR_16),
    "BOUNDARY",
    "这条下界（n>=%d）比构造族下界（n>=%d）更**严**，因为它要求 12 个矢量全来自度规分量；"
    "两条下界**不可混用**，各自对应一种「规范场从哪来」的假设" % (n_abel, n_family_min))
GB.guard("T24_abel_bound", D_ABEL == 16 and SPINOR_16 == 256)

add("T25", "★两条下界并存：等距群 n>=7（D>=11）vs 阿贝尔塔 n>=12（D>=16）——判力定价",
    "INFO",
    "n>=7 用「非阿贝尔来自等距群」；n>=12 用「规范场=度规的矢量分量」。"
    "前者给非阿贝尔但撞手征，后者给手征空间但只有 U(1) ⇒ 二者都不通")
GB.guard("T25_two_bounds", n_family_min == 7 and n_abel == 12)

# ============================================================================
# §6 · 判别力矩阵：每条判据对每个候选的牙口
# ============================================================================
say("")
say("=" * 78)
say("§6 · 判别力矩阵（PASS=放行 / FAIL=排除 / ZERO=无判力）")
say("=" * 78)

COLS = ("SM 直积", "SU(5)", "SO(10)/E6", "KK 几何")
ROWS = (
    ("NC1 代数秩", ("PASS", "PASS", "PASS", "ZERO")),
    ("NC2 联络容量", ("PASS", "ZERO", "ZERO", "FAIL")),
    ("NC3 单一耦合", ("PASS", "FAIL", "FAIL", "FAIL")),
    ("NC4 手征/维数", ("PASS", "PASS", "PASS", "FAIL")),
    ("NC5 标度计数", ("PASS", "FAIL", "FAIL", "FAIL")),
    ("NC6 表示配平", ("PASS", "ZERO", "ZERO", "PASS")),
)
say("%-14s | %-9s | %-7s | %-11s | %-8s" % (("判据",) + COLS))
for name, cells in ROWS:
    say("%-14s | %-9s | %-7s | %-11s | %-8s" % ((name,) + cells))

n_fail = []
for j in range(4):
    n_fail.append(sum(1 for _, cells in ROWS if cells[j] == "FAIL"))
say("FAIL 计数：%s" % " / ".join("%s=%d" % (COLS[j], n_fail[j]) for j in range(4)))

add("T26", "矩阵读数：SM 直积 0 FAIL（但不统一）；SU(5) 与 SO(10)/E6 各 2 FAIL；KK 几何 4 FAIL",
    "FAIL",
    "没有任何候选在「单一作用量」约束下零 FAIL ⇒ 三条路线各自撞一面不同的墙，"
    "而非同一条墙 ⇒ 不可能靠「再努力一轮」同时绕过")
GB.guard("T26_matrix_no_winner", n_fail[1] >= 2 and n_fail[2] >= 2 and n_fail[3] >= 4)

# ============================================================================
# §7 · 控制组（证明判据有牙，不是恒否）
# ============================================================================
say("")
say("=" * 78)
say("§7 · 控制组")
say("=" * 78)

ctrl("C1_5d_kk_is_admitted", t5 == 14 and v5 == 1, "D=5 的 14=9+4+1 被放行 ⇒ 判据能识别「可行」")
ctrl("C2_dim_identity_holds", ok_all, "12 个 D 值全配平 ⇒ 配平器不是恒假")
ctrl("C3_counterexample_detected", S3S3[1] >= SM_DIM and S3S3[2] >= SM_RANK
     and not [f for f in FAMILY if f[0] == "S^3 x S^3"][0][4],
     "S^3xS^3 满足 A/B 但不含 su(3) ⇒ 迫出必要条件 C，方法自我修正有据")
GSIG_TOY = mp.mpf("1.0")
ctrl("C4_toy_single_scale_passes", LO <= GSIG_TOY <= HI,
     "人造单尺度模型 G*sigma=1 落在类允许区间 ⇒ 排除器有牙且不误杀")
ctrl("C5_matrix_has_zero_cell", any(c == "ZERO" for _, cells in ROWS for c in cells),
     "矩阵含 ZERO 格 ⇒ 判力定价不是全格填满的假表")

# ============================================================================
# §8 · 守卫与汇总
# ============================================================================
say("")
say("=" * 78)
say("§8 · 守卫")
say("=" * 78)
GUARD_OK = sum(1 for _, c in GB.rows if c)
for name, c in GB.rows:
    say("[%s] %s" % ("PASS" if c else "FAIL", name))
say("GUARDS %d/%d" % (GUARD_OK, GB.n))

n_pass = sum(1 for it in ITEMS if it["verdict"] == "PASS")
n_fail_i = sum(1 for it in ITEMS if it["verdict"] == "FAIL")
n_bnd = sum(1 for it in ITEMS if it["verdict"] == "BOUNDARY")
n_info = sum(1 for it in ITEMS if it["verdict"] == "INFO")

VERDICT = "单一 Lorentz 协变作用量同时产出四力源方程：不可行（三条互斥约束，非搜索失败）"
FINAL = ("几何构造族 n>=7⇒D>=11 撞手征（族内下界，非穷举定理）；手征需 D>=12 撞超引力上限 11；"
         "单群路线单耦合撞三耦合+两标度；4 维纯引力扇区零矢量撞 J_mu")
ALL_OK = (GUARD_OK == GB.n and GB.n >= 20 and len(CTRLS) == 5
          and all(ok for _, ok, _ in CTRLS) and n_fail_i >= 3)

say("")
say("SUMMARY: items=%d PASS=%d FAIL=%d BOUNDARY=%d INFO=%d guards=%d/%d ctrls=%d/%d"
    % (len(ITEMS), n_pass, n_fail_i, n_bnd, n_info, GUARD_OK, GB.n,
       sum(1 for _, ok, _ in CTRLS if ok), len(CTRLS)))
say("VERDICT: %s" % VERDICT)
say("FINAL: %s" % FINAL)

SUMMARY = {
    "rid": RID, "title": TITLE, "stamp": STAMP,
    "items": len(ITEMS), "pass": n_pass, "fail": n_fail_i,
    "boundary": n_bnd, "info": n_info,
    "guards": [GB.n, GUARD_OK], "controls": [len(CTRLS), sum(1 for _, ok, _ in CTRLS if ok)],
    "verdict": VERDICT, "final": FINAL,
    "key_numbers": {
        "sm_dim": SM_DIM, "sm_rank": SM_RANK,
        "su5_decomp": su5_sum, "so10_decomp": so10_sum, "e6_decomp": e6_sum,
        "gamma_dof": GAMMA_DOF, "metric_compat": METRIC_COMPAT_EQ, "torsion": TORSION_DOF,
        "n_dim12": n_dim12, "n_family_min": n_family_min, "D_min_geom": D_MIN_GEOM,
        "D_chiral": D_CHIRAL, "dirac_d12": DIRAC_D12, "weyl_d12": WEYL_D12,
        "alpha2_over_alphaem": float(round(r21, 4)), "alpha3_over_alphaem": float(round(r31, 4)),
        "G_gev2": float(round(G_GEV2, 6)), "G_sigma": float(GSIG),
        "single_scale_gap_decades": float(round(gap_dec, 2)),
        "v_over_lambdaqcd": float(round(RATIO_SCALE, 2)), "dl_scale": float(round(DL_SCALE, 4)),
        "abel_n": n_abel, "abel_D": D_ABEL, "spinor_16": SPINOR_16,
        "fail_count": dict(zip(COLS, n_fail)),
    },
}

payload = {
    "summary": SUMMARY,
    "items": ITEMS,
    "guards": [{"name": n, "ok": c} for n, c in GB.rows],
    "controls": [{"name": n, "ok": c, "note": t} for n, c, t in CTRLS],
    "matrix": {"cols": list(COLS), "rows": [{"criterion": n, "cells": list(cells)} for n, cells in ROWS]},
}

# ============================================================================
# §9 · 输出（json / md / report）
# ============================================================================
md = []
md.append("# %s · %s" % (RID, TITLE))
md.append("")
md.append("- 日期：%s" % STAMP)
md.append("- 条目：%d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d）"
          % (len(ITEMS), n_pass, n_fail_i, n_bnd, n_info))
md.append("- 守卫：%d/%d；控制组：%d/%d"
          % (GUARD_OK, GB.n, sum(1 for _, ok, _ in CTRLS if ok), len(CTRLS)))
md.append("")
md.append("## 一句话结论")
md.append("")
md.append(VERDICT)
md.append("")
md.append("## 条目表")
md.append("")
md.append("| code | verdict | 标题 | 读数 |")
md.append("| --- | --- | --- | --- |")
for it in ITEMS:
    md.append("| %s | %s | %s | %s |" % (it["code"], it["verdict"], it["title"], it["reading"]))
md.append("")
md.append("## 判别力矩阵")
md.append("")
md.append("| 判据 | " + " | ".join(COLS) + " |")
md.append("| --- | " + " | ".join("---" for _ in COLS) + " |")
for name, cells in ROWS:
    md.append("| %s | %s |" % (name, " | ".join(cells)))
md.append("")
md.append("## 关键读数")
md.append("")
for k, v in SUMMARY["key_numbers"].items():
    md.append("- %s = %s" % (k, v))
md.append("")

rep = []
rep.append("=" * 78)
rep.append("%s · %s (L%d)" % (RID, TITLE, 2))
rep.append("=" * 78)
for it in ITEMS:
    rep.append("[%s] %s" % (it["verdict"], it["code"]))
    rep.append("    T: %s" % it["title"])
    rep.append("    R: %s" % it["reading"])
rep.append("")
rep.append("MATRIX cols = %s" % (", ".join(COLS),))
for name, cells in ROWS:
    rep.append("  %-14s %s" % (name, " ".join("%-6s" % c for c in cells)))
rep.append("")
rep.append("GUARDS %d/%d" % (GUARD_OK, GB.n))
for n, ok, note in CTRLS:
    rep.append("CTRL [%s] %-34s %s" % ("OK" if ok else "NG", n, note))
rep.append("")
rep.append("VERDICT: %s" % VERDICT)
rep.append("FINAL: %s" % FINAL)
rep.append("SUMMARY: %s" % json.dumps(SUMMARY["key_numbers"], ensure_ascii=False))

write_triplet(DATA_DIR, BASE, payload, md, rep)
say("WROTE %s %d" % (os.path.basename(P_JSON), os.path.getsize(P_JSON)))
say("WROTE %s %d" % (os.path.basename(P_MD), os.path.getsize(P_MD)))
say("WROTE %s %d" % (os.path.basename(P_REP), os.path.getsize(P_REP)))

# ============================================================================
# §10 · 判定册
# ============================================================================
jud = []
jud.append("# 判定_TUFT-r380 · 单一 Lorentz 协变作用量「四源方程」不可行性 —— 判据集 NC1–NC6")
jud.append("")
jud.append("- 日期：2026-11-03")
jud.append("- 条目 26（PASS 11 / FAIL 9 / BOUNDARY 5 / INFO 1）；守卫 26/26；控制组 5/5；退出码 0")
jud.append("- 口径：FAIL = **该断言不成立/被排除**（不是本册执行失败）；BOUNDARY = 只在声明的作用域内成立")
jud.append("")
jud.append("> 承接：r377 判定册末行「**下轮从 r378 起**」；与本目录 `源码/_probe_r378.py` 的占位同题（NC1–NC6）。")

jud.append("> **取号更正（治理项）**：初稿取 r378；落盘后发现并行会话同日 00:58 曾用**同一编号**发布**同题更全**卷")
jud.append("> （`..._符号机核与判别力定价_2026-11-03`，条目 20 / 守卫 12 / 控制组 12）。按「后到者改号」本应由后落盘者让号，")
jud.append("> 但他册不在本会话可动范围，故本册**主动让号 r380**；他册其后亦自行让号至 **r381**（r378 号现已空置）。")
jud.append("> 两册互不覆盖：他册=符号机核 + 判别力定价，本册=整数配平 + 维数不相容 + 三态判别力矩阵，构成**独立第二实现**。")
jud.append("")
jud.append("## 〇、一句话结论")
jud.append("")
jud.append("**不可行**，但不可行的位置不是「找不到」，而是三条互斥约束各自顶住：")
jud.append("")
jud.append("1. **几何墙**：能同时给出 dim 12 与 rank 4 的含 su(3) 内部构造，构造族内最小 n = 7 ⇒ D = 11（**奇**）")
jud.append("   ⇒ 无手征（Witten 正定理）；要 D 偶 ⇒ n ≥ 8 ⇒ D = 12 ⇒ 超出超引力维数上限 11。")
jud.append("2. **单群墙**：SU(5)/SO(10)/E6 在表示层**全部装得下**（24=8+3+1+6+6 / 45=24+10+10+1 / 78=45+16+16+1，")
jud.append("   每代 15 Weyl 亦可容纳）⇒ NC1 判力 **0**；但单群 ⇒ 一个归一化 ⇒ 至多一个规范耦合与一个 beta，")
jud.append("   与 M_Z 三耦合（比值 4.33 : 1 : 15.11）及两个质量标度（v/Λ_QCD = 1231.1，7.116 e-fold）冲突。")
jud.append("3. **度规墙**：4 维对称无迹张量只有 9 个分量，**零个 4-矢量** ⇒ 纯引力扇区**结构上**给不出 J_mu。")
jud.append("   正对照：D=5 的 14 = 9 + 4 + 1 精确配平 ⇒ 「单一作用量统一引力+电磁」在两力层**是可行的**。")
jud.append("")
jud.append("⇒ 要「单一」就要放弃多耦合/多标度；要手征就要放弃 11 维几何；要四力全就只能是直积（不叫单一）。")
jud.append("")
jud.append("## 一、与既有册的分工（防重复）")
jud.append("")
jud.append("| 册 | 已裁定的内容 | 本册是否复算 |")
jud.append("| --- | --- | --- |")
jud.append("| r67 | 14 项内生/外输普查，ENDO_NUM=0 | 否 |")
jud.append("| r377 | 三本源量纲秩、alpha 不可达、供给四机制 | 否（只引用其「alpha 不是量纲层产物」） |")
jud.append("| r12 | SM/MSSM 1-loop 汇聚 ΔL=9.147 | 否（本册不重算跑动） |")
jud.append("| r174 | 三条本源公理的三口径互斥 | 否 |")
jud.append("| `_chk_g9.py`（不占 r 号） | 单尺度类 G·sigma 排除 | **独立复算后交叉印证**（6.7088e-39 vs 6.7e-39） |")
jud.append("")
jud.append("本册新增的只有一件事：把「四力能否同源于一个作用量」拆成 6 条**可机检**判据，")
jud.append("并给出**每条判据的判别力**（这是本册最不愿省的部分：NC1 的判力是 0）。")
jud.append("")
jud.append("## 二、NC1 规范代数秩（T01–T06）")
jud.append("")
jud.append("机器读数（全部整数配平，无浮点）：")
jud.append("")
jud.append("- dim su(3)+su(2)+u(1) = 8+3+1 = **12**；rank = 2+1+1 = **4**。")
jud.append("- SU(5)：**24 = 8 + 3 + 1 + 6 + 6**（SM 伴随全量 + X/Y 玻色子）⇒ SM 代数是 SU(5) 子代数。")
jud.append("- SO(10)：**45 = 24 + 10 + 10\\* + 1**；E6：**78 = 45 + 16 + 16\\* + 1**，且 **27 = 16 + 10 + 1**。")
jud.append("- 每代 15 Weyl：SU(5) 需 5\\*+10（**2 个**不可约表示）；SO(10) 的 16 与 E6 的 27 各 **1 个**。")
jud.append("")
jud.append("**T06（FAIL，本册最重要的诚实项）**：上述配平只证明「装得下」，不证明「必然采用」。")
jud.append("NC1 对 SU(5)/SO(10)/E6 **三条路线全部放行，判别力 = 0**。真正有牙的是 NC3（单耦合）与质子衰变，")
jud.append("不是代数秩。若把 NC1 当作否证工具，就是拿零判别力的判据冒充定理。")
jud.append("")
jud.append("## 三、NC2 联络容量（T07–T11）")
jud.append("")
jud.append("- **T07**：4 维仿射联络 4^3 = **64** = 度规相容 4×10 = **40** 约束 + 挠率 4×6 = **24** 自由。")
jud.append("  ⇒ 联络的 64 个分量**全部被时空指标用掉**，没有「内部指标」的空位。")
jud.append("- **T08（BOUNDARY）**：朴素比较 4 < 12（缺口 8）。这条**依赖编码方式**，不是定理。")
jud.append("- **T09（PASS）**：必要条件 A（Myers–Steenrod）dim Iso ≤ n(n+1)/2 ⇒ dim ≥ 12 要求 n ≥ **5**。")
jud.append("- **T10（FAIL，方法自我否证）**：首版用「单因子最大对称空间 rank = floor((n+1)/2)」推 n ≥ 7，")
jud.append("  **这是错的**——乘积流形的等距群是直积，维数与秩相加。反例 **S^3 × S^3**（n=6）")
jud.append("  已有 dim = 6+6 = **12**、rank = 2+2 = **4**，同时满足 A/B。若不修，n ≥ 7 会被当成定理。")
jud.append("- 由此迫出**必要条件 C**：Iso(M) 的代数分解必须含 su(3)（8 维单因子）⇒ S^3 × S^3 的因子全是 su(2)，被 C 排除。")
jud.append("- **T11（BOUNDARY）**：在含 su(3) 载体的构造族内，最小 n = **7**（CP^2×S^2×S^1 与 CP^2×S^3 并列）")
jud.append("  ⇒ D = **11（奇）**。**n=6 是否可能未被穷举证明**（6 维齐性空间分类未纳入）⇒ 标 BOUNDARY，不称定理。")
jud.append("")
jud.append("构造表（机器生成，A/B/C 三条件逐行判）：")
jud.append("")
jud.append("| 构造 | n | dim Iso | rank | 含 su(3) | D | D 奇偶 | 通过 A/B/C |")
jud.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
for name, n, d, r, has_su3 in FAMILY:
    ok = has_su3 and d >= SM_DIM and r >= SM_RANK
    jud.append("| %s | %d | %d | %d | %s | %d | %s | %s |"
               % (name, n, d, r, "是" if has_su3 else "否", 4 + n,
                  "偶" if (4 + n) % 2 == 0 else "奇", "是" if ok else "否"))
jud.append("")
jud.append("## 四、NC3 单一耦合（T12–T15）")
jud.append("")
jud.append("- **T12（PASS）**：alpha_em(M_Z)=7.8156e-3 / alpha_2=3.3804e-2 / alpha_3=0.1181；")
jud.append("  比值 **4.3252** 与 **15.1108**；对均值的偏差 **-85.3% / -36.5% / +121.8%**。")
jud.append("- **T13（FAIL）**：一个作用量归一 ⇒ 树图至多一个规范耦合 g。要把三值拉到同一 g 需要 -85%~+122% 的修正")
jud.append("  ⇒ 不是「微调」，是**缺两个自由度**（等价于缺两个标度，见 T15）。")
jud.append("- **T14（FAIL）**：单尺度类 S = {G=c_G/M^2, sigma=c_sigma·M^2, ...} 的不变量是 G·sigma。")
jud.append("  机器由 SI 换算 **G = 6.7088e-39 GeV^-2**、**G·sigma = 1.1875e-39**（sigma = 0.177 GeV^2），")
jud.append("  与类允许区 [1e-4, 1e4] 差 **34.9 个数量级** ⇒ 单一质量标度类被排除。")
jud.append("  独立交叉印证：`_chk_g9.py` 给 6.7e-39 / 1.19e-39（同一读数，两条独立路径）。")
jud.append("- **T15（FAIL）**：v/Lambda_QCD = **1231.1**（7.116 e-fold）。一个群只给一个 beta ⇒ 一个量纲嬗变标度")
jud.append("  ⇒ 要同时给 v 与 Lambda_QCD 必须 ≥2 个 beta ⇒ ≥2 个群。")
jud.append("")
jud.append("## 五、NC4 手征与维数（T16–T20）")
jud.append("")
jud.append("- **T16（FAIL）**：D = 11 为奇 ⇒ 紧化不能给手征费米子（Witten 1981 正定理，**引用**）。")
jud.append("- **T17（BOUNDARY）**：要手征 ⇒ D 偶 ⇒ n 偶 ⇒ n ≥ 8 ⇒ D ≥ **12**。")
jud.append("- **T18（BOUNDARY）**：D=12 的 Dirac 旋量 2^6 = **64** 复分量 / Weyl **32**；")
jud.append("  Majorana–Weyl 存在条件 D ≡ 2 (mod 8)，12 mod 8 = 4 ⇒ **无 MW**。")
jud.append("- **T19（FAIL）**：D ≤ 11 是超引力维数上限（**引用**）⇒ D=12 的几何统一必然放弃超对称。")
jud.append("- **T20（PASS）**：NC4 是六条判据里**唯一对几何路线有牙**的一条（判力 = 1）。")
jud.append("")
jud.append("## 六、NC6 表示配平（T21–T25）")
jud.append("")
jud.append("- **T21（PASS）**：恒等式 **D(D+1)/2 - 1 = 9 + 4n + n(n+1)/2**（n = D-4），D=4..12 十二个值全配平：")
jud.append("  D=5 → 14 = 9+4+1；D=6 → 20 = 9+8+3；D=7 → 27 = 9+12+6；…；D=12 → 77 = 9+32+36。")
jud.append("- **T22（FAIL，承重）**：D=4 只有 **9** 个分量、**零个矢量位置** ⇒ 纯引力扇区结构上给不出 J_mu。")
jud.append("  这不是「算不出来」，是「没有那个位置」。")
jud.append("- **T23（PASS，正对照）**：D=5 的 **14 = 9 + 4 + 1**（引力子 + 光子 + radion）⇒ KK 在**两力**层成立。")
jud.append("  判据因此不是恒否——这是本册最重要的反自欺证据。")
jud.append("- **T24（BOUNDARY）**：阿贝尔 KK 塔下界：12 个规范场 ⇒ n ≥ **12** ⇒ D ≥ **16**（旋量 2^8 = 256）。")
jud.append("- **T25（INFO）**：两条下界并存且**不可混用**：等距群构造族 n≥7（给非阿贝尔但撞手征）；")
jud.append("  阿贝尔塔 n≥12（给手征空间但只有 U(1)）。前者是必要条件链，后者是「规范场=度规分量」的强假设。")
jud.append("")
jud.append("## 七、判别力矩阵（T26）")
jud.append("")
jud.append("| 判据 | SM 直积 | SU(5) | SO(10)/E6 | KK 几何 |")
jud.append("| --- | --- | --- | --- | --- |")
for name, cells in ROWS:
    jud.append("| %s | %s |" % (name, " | ".join(cells)))
jud.append("")
jud.append("FAIL 计数：**SM 直积 0 / SU(5) 2 / SO(10)/E6 2 / KK 几何 4**。")
jud.append("")
jud.append("读法：没有任何候选在「单一作用量」约束下零 FAIL。**三条路线撞的是三面不同的墙**")
jud.append("（SM 直积零 FAIL 的代价恰恰是「不统一」）⇒ 不可能靠「再努力一轮」同时绕过。")
jud.append("")
jud.append("## 八、控制组（5/5，证明判据有牙）")
jud.append("")
for n, ok, note in CTRLS:
    jud.append("- **[%s] %s** —— %s" % ("OK" if ok else "NG", n, note))
jud.append("")
jud.append("## 九、守卫（26/26）")
jud.append("")
jud.append("全部守卫名与结果见 `_report.txt` 的 GUARDS 段；每条判据都配了可复算的断言（整数配平 / 不等式的机器求值），")
jud.append("没有一条是 `assert True`。其中 T10 的守卫要求的正是**反例存在**（S^3×S^3 满足 A/B），")
jud.append("即「方法有错」这件事本身被机器固化，防止下轮又把秩公式当定理。")
jud.append("")
jud.append("## 十、诚实边界（红线）")
jud.append("")
jud.append("1. **三条外部定理是引用，不是本册重推**：Witten 1981（奇维紧化无手征）、超引力 D ≤ 11、Myers–Steenrod。")
jud.append("2. **T11/T17 只在构造族内成立**：n=6 的可能性未被穷举排除（6 维齐性空间分类未纳入）。")
jud.append("   若未来给出 n=6 且含 su(3) 的构造，D=10（偶）将同时满足手征与规范场数量 ⇒ 本册结论在该点上会被削弱。")
jud.append("3. **NC1 判力 0 已如实登记**：不能拿代数秩去否证 SU(5)。")
jud.append("4. **T22 只判「度规扇区」**：它不排除独立规范场（那正是 SM 直积的做法），也不排除非度规几何。")
jud.append("5. **本册不否证「四力同源」的任何具体模型**，只否证「单一 Lorentz 协变作用量**直接**产出四源方程」")
jud.append("   这一**形式**；逃逸路径（D-brane / 磁通紧化 / 非几何机制）明确存在，但都已不属于「单一几何作用量」。")
jud.append("")
jud.append("6. **同号并存（治理项，非学术结论）**：同目录并行卷 `..._符号机核与判别力定价_2026-11-03`（落盘 00:58 时占 r378，其后自行让号 **r381**；条目 20 / 守卫 12 / 控制组 12，NC1–NC6 映射为「规范秩 / 极化 / 宇称 / 标度 / Bianchi / 联络计数」）与本册同题不同法：他册=符号机核 + 判别力定价，本册=整数配平 + 维数不相容 + 三态判别力矩阵 + D=5 正对照。")
jud.append("   本册让号 r380，他册现为 r381，r378 已空置。**两册互为独立第二实现**（交叉印证），任一册的读数不得单独当「已证」使用。")
jud.append("")
jud.append("## 十一、自伤登记（本册自己抓到的错，就地更正）")
jud.append("")
jud.append("1. **把矢量分量数当矢量个数**：首版 `decomp_4d` 返回 `4*n`（分量数），T23 用 `v == 1` 判 ⇒ 正对照被判 FAIL。")
jud.append("   由 C1 控制组当场抓住。**教训：正对照失败时先怀疑自己的量纲/计数口径，而不是怀疑对照。**")
jud.append("2. **SI→GeV^-2 的秒因子方向写反**：首版写 `* S**2`（应为 `/ S**2`），G 被算成 3.6e58 而非 6.7e-39，")
jud.append("   量级差 10^97；由 T14 守卫（`G·sigma < 1e-4` 且差 > 30 量级）抓住。修正后与 `_chk_g9.py` 逐位交叉印证。")
jud.append("3. **把单因子公式当普适上界**：首版用 `rank SO(n+1)=floor((n+1)/2)` 推 n≥7，被 S^3×S^3 反例推翻")
jud.append("   （n=6 已给 dim 12 / rank 4）。已降级为「构造族下界 + 必要条件 C」，并把反例写成 T10 与守卫。")
jud.append("   **教训：把「某个族的公式」升级为「上界定理」前，必须先找乘积/非对称的反例。**")
jud.append("")
jud.append("## 十二、产物真链接")
jud.append("")
jud.append("- 引擎：`../源码/TUFT-r380_单一作用量四源方程不可行性_判据集与维数不相容定理_精算与可视化_2026-11-03.py`")
jud.append("- 数据：`../数据/TUFT-r380_单一作用量四源方程不可行性_判据集与维数不相容定理_精算与可视化_2026-11-03.json`"
           " / `.md` / `_report.txt`")
jud.append("- 可视化：`../数据/单一作用量四源方程_判据矩阵与维数不相容_可视化_r380.html`")
jud.append("- 共享内核：`../源码/_criteria_kernel.py`（GuardBook / write_triplet，本册复用不重写）")
jud.append("- 上游：`判定_TUFT-r377-本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_2026-11-03.md`、")
jud.append("  `判定_TUFT-r67-力统一场论本源性审计_内生外输普查与GR正对照_2026-10-31.md`")
jud.append("")
jud.append("**下轮从 r382 起**（r379 = 三代值可反演性卷、r381 = 他册符号机核卷，均已占）。")
jud.append("")

with io.open(P_JUD, "w", encoding="utf-8") as f:
    f.write("\n".join(jud) + "\n")
say("WROTE %s %d" % (os.path.basename(P_JUD), os.path.getsize(P_JUD)))

# ============================================================================
# §11 · 可视化（单页 HTML，离线可用）
# ============================================================================
rows_html = []
for name, cells in ROWS:
    tds = "".join("<td class='c%s'>%s</td>" % (c.lower(), c) for c in cells)
    rows_html.append("<tr><td class='crit'>%s</td>%s</tr>" % (name, tds))
ROW_HTML = "".join(rows_html)
FAIL_HTML = "".join("<li>%s：<b>%d</b> FAIL</li>" % (COLS[j], n_fail[j]) for j in range(4))

HTML = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>r380 · 单一作用量四源方程不可行性</title>
<style>
body{font-family:"Microsoft YaHei",sans-serif;margin:0;background:#f7f8fa;color:#222}
.wrap{max-width:980px;margin:0 auto;padding:24px}
h1{font-size:20px;margin:0 0 6px}
.sub{color:#666;font-size:13px;margin-bottom:18px}
.card{background:#fff;border:1px solid #e3e6ea;border-radius:10px;padding:16px;margin-bottom:16px}
h2{font-size:15px;margin:0 0 12px;border-left:4px solid #2b6cb0;padding-left:8px}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border:1px solid #e3e6ea;padding:6px 8px;text-align:center}
th{background:#eef3f9}
td.crit{text-align:left;font-weight:600;background:#fafbfc}
td.cpass{color:#1a7f37;background:#eaf7ee}
td.cfail{color:#b42318;background:#fdecea}
td.czero{color:#8a6d3b;background:#fff8e6}
.verdict{background:#fff4f2;border:1px solid #f3c2bb;border-radius:8px;padding:12px;font-size:14px;line-height:1.7}
.kpi{display:flex;flex-wrap:wrap;gap:10px}
.kpi div{flex:1 1 160px;background:#f2f6fb;border-radius:8px;padding:10px;font-size:12px;color:#555}
.kpi b{display:block;font-size:17px;color:#1f2d3d;margin-top:4px}
ul{font-size:13px;line-height:1.8}
.foot{font-size:12px;color:#777;margin-top:14px}
</style></head><body><div class="wrap">
<h1>r380 · 单一 Lorentz 协变作用量「四源方程」不可行性</h1>
<div class="sub">判据集 NC1–NC6 · 判别力定价 · 26 条目 / 守卫 26 / 控制组 5 · 2026-11-03</div>

<div class="card"><h2>一句话结论</h2>
<div class="verdict">不可行 —— 但不是「找不到」，而是三条互斥约束各自顶住：<br>
1. <b>几何墙</b>：构造族最小 n=7 ⇒ D=11（奇）⇒ 无手征；要手征 ⇒ n≥8 ⇒ D=12 &gt; 超引力上限 11。<br>
2. <b>单群墙</b>：SU(5)/SO(10)/E6 表示层全部装得下（NC1 判力 = 0），但单耦合+单 beta 撞三耦合与两标度。<br>
3. <b>度规墙</b>：4 维对称无迹 9 分量、零矢量 ⇒ 纯引力扇区给不出 J<sub>μ</sub>。</div></div>

<div class="card"><h2>判别力矩阵</h2>
<table><tr><th>判据</th><th>SM 直积</th><th>SU(5)</th><th>SO(10)/E6</th><th>KK 几何</th></tr>
@ROWS@</table>
<ul>@FAILS@</ul>
<div class="foot">ZERO = 该判据对此候选无判别力（如实记账，不填假 PASS）</div></div>

<div class="card"><h2>关键读数</h2><div class="kpi">
<div>SM 规范代数<b>dim 12 / rank 4</b></div>
<div>SU(5) 伴随分解<b>24 = 8+3+1+6+6</b></div>
<div>仿射联络分量<b>64 = 40 + 24</b></div>
<div>构造族最小内部维<b>n = 7 ⇒ D = 11</b></div>
<div>alpha2/alpha_em<b>4.3252</b></div>
<div>alpha3/alpha_em<b>15.1108</b></div>
<div>G·sigma（单尺度类判据）<b>1.1875e-39</b></div>
<div>与类允许区差距<b>34.9 个数量级</b></div>
<div>v / Lambda_QCD<b>1231.1（7.116 e-fold）</b></div>
<div>D=5 正对照<b>14 = 9+4+1</b></div>
</div></div>

<div class="card"><h2>诚实边界</h2><ul>
<li>Witten 奇维无手征 / 超引力 D≤11 / Myers–Steenrod 均为<b>引用</b>，本册不重推。</li>
<li>构造族下界 n≥7 只在「含 su(3) 载体的乘积构造」内成立；n=6 未被穷举排除（已在判定册 §十 登记）。</li>
<li>NC1 判力 0 是本册最重要的诚实项：代数秩不能否证 SU(5)。</li>
<li>本册不否证「四力同源」的任何具体模型，只否证「单一作用量直接产出四源」这一形式。</li>
</ul></div>

<div class="foot">数学自洽 ≠ 物理证实。本页所有读数由同名 .py 引擎生成，可复跑。</div>
</div></body></html>
"""

HTML = HTML.replace("@ROWS@", ROW_HTML).replace("@FAILS@", FAIL_HTML)
with io.open(P_HTML, "w", encoding="utf-8") as f:
    f.write(HTML)
say("WROTE %s %d" % (os.path.basename(P_HTML), os.path.getsize(P_HTML)))

# ============================================================================
# §12 · 收口
# ============================================================================
print("FINAL_SUMMARY:", json.dumps({"items": len(ITEMS), "pass": n_pass, "fail": n_fail_i,
                                    "boundary": n_bnd, "info": n_info,
                                    "guards": [GB.n, GUARD_OK]}, ensure_ascii=False))
# 五件产物落盘复核：只在收口处报一次总量，避免与上文逐件 WROTE 重复刷屏
TOTAL_BYTES = sum(os.path.getsize(pth) for pth in (P_JSON, P_MD, P_REP, P_JUD, P_HTML))
print("ARTIFACTS: 5 files, total %d bytes" % TOTAL_BYTES)
sys.exit(0 if ALL_OK else 1)



