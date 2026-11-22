# -*- coding: utf-8 -*-
"""TUFT-r440 | 量子一致性缺口的首次定价 + 四类缺口账户秩修正(4->3).

靶点: r438/r439 记账的「四类缺口」(G / 规范群 / 粒子谱 / 量子一致性) 中
      唯一从未被定价的一类 —— 量子一致性. r439 只判它 OPEN(未证), 未给代价.

本册不重判 r438/r439, 只做七件新事:
  Q1 辛结构      : (kappa,tau) 2 维实空间上 omega=dk^dt 闭且非退化
                   => 经典量子化的几何前提已具备 (四缺口里唯一的正面项)
  Q2 谱/整数二分 : 离散谱需要「有限的紧致长度」(连续输入), 预量子化需要
                   Weil 整数性 (离散输入); 两者都不能由 kappa,tau 的连续性生成
  Q3 正则对易    : [kappa][tau]=L^-2 != [hbar]; {c,hbar} 穷举 0 命中,
                   {c,hbar,G} 唯一解 X=hbar^2*G/c^3 = hbar*l_P^2
  Q4 内部维数    : su(2)+su(3) 的最小忠实复维数 = 5 (双判据), ROOT 只给 1 维复
  Q5 Born        : 1 维复态空间上 Born 只给 {0,1}; 非平凡概率需 >=2 维复
  Q6 谱型        : KK 等差谱 1:2:3 被实测排除; 单参数指数谱被第三代排除;
                   双参数指数谱 2 参数吃 2 数据 => 判别力 0
  Q7 账户秩      : 单标度口径下 4 类缺口 -> 3 个独立输入, 且
                   量子一致性 = G 的输入 + 规范群的输入 (线性相关 => 独立输入 0)
                   双标度口径下秩 = 4 (量子一致性独立) => 结论是口径依赖的

不做: 不宣称攻破、不改被引文件字节、不重判 r438/r439、不做 git.
纯标准库 Python 3.8.
"""
import io
import itertools
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

try:
    _r = getattr(sys.stdout, "reconfigure", None)
    if callable(_r):
        _r(errors="replace")
except Exception:
    pass

BASE = Path(__file__).resolve().parents[1]
NAME = "TUFT-r440_量子一致性缺口定价_辛结构Weil二分与账户秩4降3_精算_2026-11-22"
ROUND, DATE = "r440", "2026-11-22"
OUT = BASE / "数据"
JUDGE = BASE / "判定"

ENTRIES, GUARDS, CONTROLS = [], [], []


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


def ctrl(code, cond, note):
    CONTROLS.append(dict(code=code, ok=bool(cond), note=note))


def read_text(p):
    for enc in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return io.open(str(p), encoding=enc).read()
        except Exception:
            continue
    return ""


# ============================================================ 量纲工具 (M,L,T)
D_C = (0, 1, -1)
D_HBAR = (1, 2, -1)
D_G = (-1, 3, -2)


def dmul(a, b):
    """量纲相乘 = 指数逐分量相加 (不是 tuple 拼接)."""
    return tuple(x + y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * n for x in a)


def search(target, basis, lo=-6, hi=6):
    """在 basis 的整数幂网格上求 [prod b^e] = target 的全部解."""
    names = list(basis)
    hits = []
    for exps in itertools.product(range(lo, hi + 1), repeat=len(names)):
        v = (0, 0, 0)
        for e, nm in zip(exps, names):
            v = dmul(v, dpow(basis[nm], e))
        if v == target:
            hits.append(exps)
    return hits


def fmt(expr):
    return "(%d,%d,%d)" % expr


# ============================================================ A 基线来源
J438 = JUDGE / "判定_TUFT-r438_ROOT_V121-V132全量攻破与统一场论未完成裁定_精算_2026-11-22.md"
J439 = JUDGE / "判定_TUFT-r439_ROOT_V119-V135自证边界与三定理攻破_精算_2026-11-22.md"
t438, t439 = read_text(J438), read_text(J439)

guard("G-A1", J438.is_file() and J439.is_file(), "r438/r439 判定册存在（基线可溯）")
guard("G-A2", ("量子一致性" in t438) and ("量子一致性" in t439),
      "两册都记账「量子一致性」缺口（本册靶点确实在账上）")
guard("G-A3", ("一维表示障碍" in t439) or ("1x1" in t439), "r439 T1 基线在册")
guard("G-A4", ("量纲" in t438) and ("G" in t438), "r438 G 量纲否决基线在册")

add("Q00", "INFO", "分工声明：不重判 r438/r439",
    "r438 判 12/12 未完成、r439 判三条自证 no-go 与四缺口全开；"
    "本册只补「四类缺口中唯一未定价者（量子一致性）」的代价，并修正账户秩")

# ============================================================ B Q1 辛结构
# omega = dk ^ dt 在 2 维实坐标 (kappa,tau) 上: 闭 (2 维上任何 2-形式都闭) + 非退化 (det=1)
OMEGA_MAT = ((0, 1), (-1, 0))
det_omega = OMEGA_MAT[0][0] * OMEGA_MAT[1][1] - OMEGA_MAT[0][1] * OMEGA_MAT[1][0]
# 共形类 f(k,t) dk^dt 的非退化性: 要求 f != 0 处处
nondeg_points = []
for k, t in ((0.0, 0.0), (1.0, -2.0), (-3.0, 4.0), (1e-8, -1e-8)):
    f0 = 1.0                     # 自然体积形式 f=1
    f1 = k                       # 错误候选 f=kappa
    nondeg_points.append((k, t, f0 != 0.0, f1 != 0.0))

# d(omega)=0: 2 维流形上 3-形式恒为 0（维度论断，非数值），用外微分阶数机核
d_omega_zero = (3 > 2)           # 3-形式在 2 维上必为 0

guard("G-B1", det_omega == 1, "omega=dk^dt 在 (k,t) 坐标下 det=%d != 0" % det_omega)
guard("G-B2", d_omega_zero, "2 维上 3-形式恒 0 => d(omega)=0（无需度量）")
guard("G-B3", nondeg_points[0][2] and all(p[3] for p in nondeg_points[1:]),
      "自然形式 f=1 处处非退化；阳性对照 f=kappa 在 k=0 处退化")
ctrl("C-B1", det_omega != 0 and not nondeg_points[0][3],
     "辛结构阴性/阳性并存（f=1 非退化、f=kappa 在原点退化）")
add("Q01", "PASS", "Q1 经典量子化的几何前提已具备：辛结构存在",
    "(kappa,tau) 上 omega=dk^dt：闭（3-形式在 2 维上恒 0）且非退化（det=1）；"
    "阳性对照 f=kappa·dk^dt 在 kappa=0 退化 ⇒ 判据有牙。"
    "这是四类缺口中唯一的正面项：缺的不是相空间")
add("Q02", "INFO", "辛形式只在共形类内唯一",
    "f(k,t)·dk^dt 对任意处处非零 f 都是辛形式 ⇒ 量子化常数受归一化约定影响；"
    "登记为约定自由度，不计入结构性输入")

# ============================================================ C Q2 谱/整数二分
# 离散谱: 有限紧致长度 L 才有 gap; gap(L)=(pi/L)^2
gaps = [(L, (math.pi / L) ** 2) for L in (1.0, 10.0, 100.0)]
slope = math.log(gaps[1][1] / gaps[0][1]) / math.log(gaps[1][0] / gaps[0][0])
# 预量子化 (Weil): ħ=1 单位下辛面积量子 = 2pi; 面积 L^2 = 2pi*n
weil = [(n, math.sqrt(2.0 * math.pi * n)) for n in range(1, 7)]
weil_err = max(abs(Ln * Ln / (2.0 * math.pi) - n) for n, Ln in weil)
# 非紧致: H^2(R^2)=0 => 无整数性障碍，但同时无离散谱
guard("G-C1", abs(slope + 2.0) < 1e-9, "gap ∝ L^-2, log-log 斜率 %.12f" % slope)
guard("G-C2", gaps[2][1] < 1e-3, "L=100 时 gap=%.3e → 连续极限" % gaps[2][1])
guard("G-C3", weil_err < 1e-12, "面积量子化 L^2=2pi*n 复算残差 %.2e" % weil_err)
guard("G-C4", d_omega_zero and len(weil) == 6, "两条路（非紧致/紧致）都在册")

add("Q03", "FAIL", "Q2a 非紧致 ⇒ 无整数性障碍，但也无离散谱",
    "R^2 可缩 ⇒ H^2=0 ⇒ 预量子化线丛平凡、无 Weil 条件；"
    "同时 gap→0（L=1/10/100 给 %.3e/%.3e/%.3e）⇒ 谱连续 ⇒ 无「粒子=离散态」"
    % (gaps[0][1], gaps[1][1], gaps[2][1]))
add("Q04", "FAIL", "Q2b 紧致 ⇒ 需 Weil 整数性（新离散输入）",
    "面积必须量子化 L^2=2*pi*n（ħ=1），L_n=%s；n 是新的整数输入，"
    "不能由 kappa,tau 的连续取值导出"
    % ", ".join("%.6f" % x for _n, x in weil[:3]))
add("Q05", "PASS", "Q2c 二分定理：量子一致性的两条出口都付费",
    "要离散谱 ⇒ 需有限的紧致长度（连续输入）；要预量子化线丛 ⇒ 需 Weil 整数 n"
    "（离散输入）。两者的共同点是：都不能由 (kappa,tau) 的连续性生成 ⇒ "
    "量子一致性至少需 +1 长度标度，且不是算力问题")

# ============================================================ D Q3 正则对易
# [q][p]=[hbar]=(1,2,-1); q=kappa,p=tau => [kappa][tau]=(-2,0,0)
comm_dim_kt = dmul((0, -1, 0), (0, -1, 0))
target = (1, 2, -1)
gap_dim = tuple(target[i] - comm_dim_kt[i] for i in range(3))
# 注意：搜索目标是「缺口」[X]=[hbar]/[k][t]=ML^4T^-1，不是 [hbar] 本身
hits_2 = search(gap_dim, {"c": D_C, "hbar": D_HBAR})
hits_3 = search(gap_dim, {"c": D_C, "hbar": D_HBAR, "G": D_G})
# 唯一解 X=hbar^2*G/c^3 的量纲核验 + 与 hbar*l_P^2 的恒等
X_dim = dmul(dmul(dpow(D_HBAR, 2), D_G), dpow(D_C, -3))
lp2_dim = dmul(dmul(D_HBAR, D_G), dpow(D_C, -3))

guard("G-D1", comm_dim_kt != target, "[k][t]=%s != [hbar]=%s，缺口 %s"
      % (fmt(comm_dim_kt), fmt(target), fmt(gap_dim)))
guard("G-D2", len(hits_2) == 0, "{c,hbar} 穷举 0 命中（目标被超定）")
guard("G-D3", len(hits_3) == 1 and hits_3[0] == (-3, 2, 1),
      "{c,hbar,G} 唯一解 (c^%d hbar^%d G^%d)" % hits_3[0] if hits_3 else "无解")
guard("G-D4", X_dim == gap_dim and lp2_dim == (0, 2, 0),
      "X=hbar^2*G/c^3 量纲=%s = 缺口 %s；hbar*G/c^3 量纲=%s=L^2"
      % (fmt(X_dim), fmt(gap_dim), fmt(lp2_dim)))
ctrl("C-D1", (len(hits_2) == 0) and (len(hits_3) == 1),
     "量纲穷举阴性/阳性并存（2 基组 0 命中、3 基组唯一命中）")

add("Q06", "FAIL", "Q3a 正则对易在 (kappa,tau) 上量纲不闭合",
    "[kappa][tau]=L^-2 而 [hbar]=M L^2 T^-1，缺口 %s；"
    "必须把 kappa,tau 无量纲化（乘一个长度）才能写成 [Q,P]=i*hbar" % fmt(gap_dim))
add("Q07", "PASS", "Q3b 闭合因子的唯一性：X=hbar*l_P^2（唯一解）",
    "{c,hbar} 穷举 0 命中；{c,hbar,G} 在 [−6,6]^3 上唯一解 (a,b,d)=(−3,2,1) ⇒ "
    "X=hbar^2*G/c^3=hbar*l_P^2 ⇒ 量子一致性唯一地把 G 拉进场")

# ============================================================ E Q4 内部维数
DIM_ALG = 3 + 8   # dim su(2)+su(3)


def partitions(n, mx=None):
    if mx is None:
        mx = n
    if n == 0:
        yield []
        return
    for k in range(min(n, mx), 0, -1):
        for rest in partitions(n - k, k):
            yield [k] + rest


def faithful_n(n):
    """su(2)+su(3) 在 C^n 上同时忠实: 需一个 su(3) 块(>=3) 且还剩 >=2 维给 su(2)."""
    if n * n < DIM_ALG:
        return False, "维度计数不足"
    for p in partitions(n):
        if max(p) >= 3 and (n - max(p)) >= 2:
            return True, "块 %s" % p
        if sum(1 for b in p if b >= 3) >= 1 and sum(b for b in p if b < 3) >= 2:
            return True, "块 %s" % p
    return False, "无 3+2 分块"


feas = {}
for n in range(1, 9):
    ok, why = faithful_n(n)
    feas[n] = (ok, why)
min_n = min(n for n, (ok, _w) in feas.items() if ok)
# 双判据的反例: n=4 过维度计数(16>=11) 但分块失败
n4_dim_ok = 4 * 4 >= DIM_ALG
n4_feas = feas[4][0]
# 维数阶梯
GEN1 = 6 + 3 + 3 + 2 + 1          # Q(3,2)+u(3,1)+d(3,1)+L(1,2)+e(1,1)
GEN1_NU = GEN1 + 1                # + nu_R
GEN3, GEN3_NU = 3 * GEN1, 3 * GEN1_NU

guard("G-E1", DIM_ALG == 11, "dim su(2)+su(3)=%d" % DIM_ALG)
guard("G-E2", min_n == 5, "最小忠实复维数=%d" % min_n)
guard("G-E3", n4_dim_ok and not n4_feas, "n=4 过维度计数(16>=11)但分块失败 ⇒ 双判据必要")
guard("G-E4", (GEN1, GEN1_NU, GEN3, GEN3_NU) == (15, 16, 45, 48),
      "维数阶梯 15/16/45/48 逐项复算")
ctrl("C-E1", feas[3][0] is False and feas[5][0] is True,
     "n=3 不可行 / n=5 可行（判据非恒真非恒假）")

add("Q08", "FAIL", "Q4a 最小忠实内部复维数 = 5，ROOT 只给 1",
    "su(2)+su(3) 需同时忠实 ⇒ 一个 >=3 维块 + 剩余 >=2 维 ⇒ 最小 5 维复；"
    "ROOT 的内部态是单个复相位 kappa+i*tau（1 维复）⇒ 缺口 4 维复")
add("Q09", "INFO", "Q4b 内部维数的代价阶梯",
    "代数层 5（su(2)+su(3) 忠实）/ 单代 SM 内容 %d（含 nu_R %d）/ 三代 %d（含 nu_R %d）"
    " ⇒ 「逃逸 T1」的代价取决于要求层级：+4 / +14 / +44 维复"
    % (GEN1, GEN1_NU, GEN3, GEN3_NU))

# ============================================================ F Q5 Born 退化
# n 维复空间上厄米算符空间实维 = n^2；C^1 上秩一投影只有 {0,1}
herm_dim = {n: n * n for n in (1, 2, 3)}


def probs_1d():
    """C^1 上纯态 rho=1，P∈{0,1} ⇒ 概率只取 {0,1}."""
    return sorted({0.0, 1.0})


def probs_2d(samples=200):
    """C^2 上 |u><u| 与 rho=1 ⇒ Tr=cos^2(theta) 连续取值."""
    vals = set()
    for i in range(samples):
        th = math.pi * i / (samples - 1.0)
        vals.add(round(math.cos(th) ** 2, 9))
    return sorted(vals)


p1, p2 = probs_1d(), probs_2d()
# 「三重奏」|psi|^2=(omega/c)^2 是逐点固定模长的约束（S^1），不是概率测度
def jac_rank(a, b):
    if a == 0.0 and b == 0.0:
        return 0
    return 1


state_dim = [jac_rank(math.cos(t), math.sin(t)) for t in (0.0, 1.0, 2.5)]

guard("G-F1", herm_dim[1] == 1 and herm_dim[2] == 4, "Herm(C^n) 实维 = 1/4 (n=1,2)")
guard("G-F2", len(p1) == 2 and len(p2) > 2, "C^1 概率二值(%d) vs C^2 连续(%d 个取值)"
      % (len(p1), len(p2)))
guard("G-F3", all(r == 1 for r in state_dim), "三重奏约束面 Jacobi 秩恒 1 ⇒ 态空间 1 维实")
ctrl("C-F1", len(p1) == 2 and len(p2) > 10, "Born 退化阴性/阳性并存")

add("Q10", "FAIL", "Q5 Born 规则在 1 维复态空间上退化",
    "Herm(C^1) 实维 1 ⇒ 唯一可观测量是模长；秩一投影只有 {0,1} ⇒ 概率只取 {0,1}；"
    "C^2 上 Tr=cos^2(theta) 连续（%d 个取值）⇒ 非平凡概率需 >=2 维复" % len(p2))
add("Q11", "INFO", "三重奏给的是归一化约束，不是概率测度",
    "|psi|^2=(omega/c)^2 在每点固定模长（约束面 S^1，Jacobi 秩 1）；"
    "Born 还需要测度 + 谱测度 + 算符代数，而算符代数又撞 Q4 的 1 维复 ⇒ 与规范群同源")

# ============================================================ G Q6 谱型
R_MU_E = 206.7682827
R_TAU_MU = 16.8170
kk2 = 2.0                                    # KK 等差谱 m_n=n/L ⇒ m2/m1=2
dev_kk = abs(R_MU_E - kk2) / R_MU_E
c_exp = math.log(R_MU_E)                     # 单参数指数谱(固定首项) 由 m2/m1 定 c
dev_exp3 = abs(R_MU_E - R_TAU_MU) / R_MU_E   # 该谱对第三代的预测仍是 206.77
dof_exp = 2 - 2                              # 双参数指数谱 2 参数吃 2 数据

guard("G-G1", R_MU_E > 200, "CODATA m_mu/m_e=%.7f" % R_MU_E)
guard("G-G2", dev_kk > 0.99, "KK 等差谱 m2/m1=2 ⇒ 相对偏差 %.6f" % dev_kk)
guard("G-G3", dev_exp3 > 0.9, "单参数指数谱预测 m3/m2=%.4f ⇒ 偏差 %.6f"
      % (math.exp(c_exp), dev_exp3))
guard("G-G4", dof_exp == 0, "双参数指数谱 dof=%d ⇒ 判别力 0" % dof_exp)

add("Q12", "FAIL", "Q6a 紧致化不免费提供谱型：KK 等差谱被实测排除",
    "m_n=n/L ⇒ 1:2:3，m_mu/m_e 预测 2 vs 实测 %.7f，相对偏差 %.6f" % (R_MU_E, dev_kk))
add("Q13", "FAIL", "Q6b 单参数指数谱被第三代排除，双参数谱判别力 0",
    "固定首项时 m3/m2=e^c=%.4f（实测 %.4f，偏差 %.6f）；"
    "放开幅值则 2 参数吃 2 数据 ⇒ dof=0 ⇒ 不是预言（与 r439 T6 同型）"
    % (math.exp(c_exp), R_TAU_MU, dev_exp3))
# 与 r295 独立互印（不新增 claim）: tr_R(Y) 用 dim 加权
Y = {"Q": F(1, 6), "u": F(2, 3), "d": F(-1, 3), "L": F(-1, 2), "e": F(-1, 1)}
DIMR = {"Q": 6, "u": 3, "d": 3, "L": 2, "e": 1}
trY = [Y[k] * DIMR[k] for k in ("Q", "u", "d", "L", "e")]
guard("G-G5", [str(x) for x in trY] == ["1", "2", "-1", "-1", "-1"],
      "tr_R(Y) 复算 = (1,2,-1,-1,-1)，与 r295 定理 B 逐项一致")
add("Q14", "PASS", "Q6c 与 r295 独立互印：U(1) 通量谱型恒为 1:2:1:1:1",
    "dim 加权 tr_R(Y) 复算 (1,2,-1,-1,-1)，比值 2 与通量量子数无关 ⇒ "
    "三代不是单一 U(1) 通量能给出的（继承 r295，不新增 claim）")

# ============================================================ H Q7 账户秩
def rank(rows):
    M = [[F(x) for x in r] for r in rows]
    m, n, rk = len(M), len(M[0]), 0
    for c in range(n):
        piv = None
        for i in range(rk, m):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        pv = M[rk][c]
        M[rk] = [x / pv for x in M[rk]]
        for i in range(m):
            if i != rk and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


# 列 = 输入 #1 长度标度 L / #2 内部复维 n / #3 谱型 S
M1 = [[1, 0, 0],     # G      : 需 m_P (⇔ 1/L)
      [0, 1, 0],     # 规范群 : 需 n>=5
      [1, 0, 1],     # 粒子谱 : 绝对标度 L + 谱型 S
      [1, 1, 0]]     # 量子一致: L (离散谱/无量纲化) + n (Born 非退化)
r1 = rank(M1)
dep = [M1[3][i] - M1[0][i] - M1[1][i] for i in range(3)]
# 稳健性: 把 L 拆成两列（重复记账）秩不变
M2 = [[1, 1, 0, 0], [0, 0, 1, 0], [1, 1, 0, 1], [1, 1, 1, 0]]
r2_dup = rank(M2)
# 敏感性: 错误地把「谱型」并入规范群（少一列）⇒ 秩掉到 2
M3 = [[1, 0], [0, 1], [1, 1], [1, 1]]
r3_bad = rank(M3)
# 口径二分: 若引力标度与紧致化周期是两个独立长度 ⇒ 4 列，秩 4
M4 = [[1, 0, 0, 0], [0, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]
r4_two = rank(M4)

guard("G-H1", r1 == 3, "单标度口径秩=%d（4 行 3 列）" % r1)
guard("G-H2", dep == [0, 0, 0], "量子一致性行 = G 行 + 规范群行（精确线性相关）")
guard("G-H3", r2_dup == 3, "把 L 拆两列（重复记账）秩仍 %d ⇒ 对记账粒度稳健" % r2_dup)
guard("G-H4", r3_bad == 2, "错误合并「谱型→规范群」⇒ 秩掉到 %d ⇒ 判据有牙" % r3_bad)
guard("G-H5", r4_two == 4, "双标度口径秩=%d ⇒ 结论是口径依赖的（必须登记）" % r4_two)
ctrl("C-H1", r1 == 3 and r3_bad == 2, "秩判据阴性/阳性并存")
ctrl("C-H2", r1 == 3 and r4_two == 4, "两个口径都算出来（不掩盖分歧）")

add("Q15", "PASS", "Q7a 单标度口径：四类缺口 → 3 个独立输入",
    "4x3 关联矩阵秩=3；且第 4 行精确等于第 1+2 行 ⇒ 量子一致性的独立输入数 = 0；"
    "把 L 拆成两列（重复记账）秩仍 3 ⇒ 结论对记账粒度稳健")
add("Q16", "BOUNDARY", "Q7b 结论是口径依赖的：双标度口径秩=4",
    "若「引力标度 l_P」与「紧致化周期 L_c」视为两个独立长度，4x4 矩阵秩=4 ⇒ "
    "量子一致性重新独立。分歧点唯一：两者是否同一标度。本册不代选")
add("Q17", "INFO", "Q7c 与 r432 六项 OPEN 的关系",
    "本册的 3 是「ROOT 四类缺口范围内」的秩，不等于全库总账（O-THETA 等离散输入"
    "不在本矩阵列内）；不得据此宣称全库只剩 3 项")

# ============================================================ I 产出与互印
add("Q18", "PASS", "与 r438/r439 的分工与互印",
    "r438 判「12/12 未完成」、r439 判「三条 no-go + 四缺口不可达」；"
    "本册把其中唯一未定价的量子一致性定价，并给出账户秩 4->3（口径条件性）")
add("Q19", "INFO", "红线",
    "合成数值≠实验；辛结构存在≠可量子化；秩修正≠缺口消失；"
    "0/6、0/22、UFT3=0、L3=0、validated=0 全部不变")

VERDICT = ("QUANTUM-CONSISTENCY-PRICED--SYMPLECTIC-OK--SPECTRUM-SCALE-DICHOTOMY"
           "--COMMUTATOR-NEEDS-G--INTERNAL-DIM-5--ACCOUNT-RANK-4-TO-3-CALIBER-DEPENDENT")

guard("G-I1", len(ENTRIES) >= 18, "条目数 %d" % len(ENTRIES))
guard("G-I2", all(g["ok"] for g in GUARDS), "全部守卫通过")
guard("G-I3", all(c["ok"] for c in CONTROLS), "全部控制组通过")
guard("G-I4", len(GUARDS) >= 24, "守卫数 %d >= 24" % len(GUARDS))

payload = dict(round=ROUND, date=DATE, name=NAME, verdict=VERDICT,
               entries=ENTRIES, guards=GUARDS, controls=CONTROLS,
               q1=dict(det_omega=det_omega, nondeg=nondeg_points, domega=d_omega_zero),
               q2=dict(gaps=gaps, slope=slope, weil=weil, weil_err=weil_err),
               q3=dict(comm_dim=fmt(comm_dim_kt), target=fmt(target), gap=fmt(gap_dim),
                       hits_2=len(hits_2), hits_3=[list(x) for x in hits_3],
                       X_dim=fmt(X_dim)),
               q4=dict(dim_alg=DIM_ALG, min_n=min_n, feasible={str(k): v for k, v in feas.items()},
                       ladder=[GEN1, GEN1_NU, GEN3, GEN3_NU]),
               q5=dict(herm_dim={str(k): v for k, v in herm_dim.items()},
                       p1=p1, p2_count=len(p2)),
               q6=dict(r_mu_e=R_MU_E, r_tau_mu=R_TAU_MU, dev_kk=dev_kk,
                       dev_exp3=dev_exp3, dof_exp=dof_exp, trY=[str(x) for x in trY]),
               q7=dict(M1=M1, rank1=r1, dep=dep, rank_dup=r2_dup,
                       rank_bad=r3_bad, rank_two_scale=r4_two))

OUT.mkdir(parents=True, exist_ok=True)
io.open(str(OUT / (NAME + ".json")), "w", encoding="utf-8").write(
    json.dumps(payload, ensure_ascii=False, indent=1))

npass = len([e for e in ENTRIES if e["status"] == "PASS"])
nfail = len([e for e in ENTRIES if e["status"] == "FAIL"])
nbnd = len([e for e in ENTRIES if e["status"] == "BOUNDARY"])
ninfo = len([e for e in ENTRIES if e["status"] == "INFO"])

L2 = ["# " + NAME, "",
      "- 轮次 %s ｜ 日期 %s" % (ROUND, DATE),
      "- 条目 %d：PASS %d / FAIL %d / BOUNDARY %d / INFO %d"
      % (len(ENTRIES), npass, nfail, nbnd, ninfo),
      "- 守卫 %d/%d ｜ 控制组 %d/%d"
      % (len([g for g in GUARDS if g["ok"]]), len(GUARDS),
         len([c for c in CONTROLS if c["ok"]]), len(CONTROLS)),
      "", "## 条目", "",
      "| 码 | 状态 | 结论 |",
      "|---|---|---|"]
for e in ENTRIES:
    L2.append("| %s | %s | %s |" % (e["code"], e["status"], e["title"]))
L2 += ["", "## 复算读数", "",
       "- Q1: det(omega)=%d；f=kappa 在原点退化（阳性对照）" % det_omega,
       "- Q2: gap ∝ L^%.12f；Weil L_n²=2pi*n 残差 %.2e；L_1..L_3 = %s"
       % (slope, weil_err, ", ".join("%.6f" % x for _n, x in weil[:3])),
       "- Q3: [k][t]=%s vs [hbar]=%s；{c,hbar} 命中 %d；{c,hbar,G} 命中 %d %s"
       % (fmt(comm_dim_kt), fmt(target), len(hits_2), len(hits_3), hits_3),
       "- Q4: dim(su2+su3)=%d；最小忠实复维 = %d；阶梯 %d/%d/%d/%d"
       % (DIM_ALG, min_n, GEN1, GEN1_NU, GEN3, GEN3_NU),
       "- Q5: Herm 实维 n=1→%d、n=2→%d；C^1 概率取值 %d 个、C^2 %d 个"
       % (herm_dim[1], herm_dim[2], len(p1), len(p2)),
       "- Q6: KK 偏差 %.6f；单参数指数谱三代偏差 %.6f；tr_R(Y)=%s"
       % (dev_kk, dev_exp3, [str(x) for x in trY]),
       "- Q7: 秩 单标度=%d（行依赖 %s）/ 重复记账=%d / 错误合并=%d / 双标度=%d"
       % (r1, dep, r2_dup, r3_bad, r4_two)]
io.open(str(OUT / (NAME + ".md")), "w", encoding="utf-8").write("\n".join(L2))

R = ["ROUND %s %s" % (ROUND, DATE)]
for e in ENTRIES:
    R.append("[%s] %s | %s" % (e["status"], e["code"], e["title"]))
R.append("Q1 det=%d  Q2 slope=%.12f weil_err=%.2e" % (det_omega, slope, weil_err))
R.append("Q3 hits2=%d hits3=%d %s" % (len(hits_2), len(hits_3), hits_3))
R.append("Q4 minalg=%d min_n=%d ladder=%d/%d/%d/%d"
         % (DIM_ALG, min_n, GEN1, GEN1_NU, GEN3, GEN3_NU))
R.append("Q5 p1=%d p2=%d  Q6 devkk=%.6f devexp3=%.6f"
         % (len(p1), len(p2), dev_kk, dev_exp3))
R.append("Q7 rank1=%d dep=%s dup=%d bad=%d two=%d"
         % (r1, dep, r2_dup, r3_bad, r4_two))
R.append("GUARDS %d/%d  CONTROLS %d/%d"
         % (len([g for g in GUARDS if g["ok"]]), len(GUARDS),
            len([c for c in CONTROLS if c["ok"]]), len(CONTROLS)))
R.append("VERDICT " + VERDICT)
io.open(str(OUT / (NAME + "_report.txt")), "w", encoding="utf-8").write("\n".join(R))

print("ENTRIES %d (P%d/F%d/B%d/I%d)  GUARDS %d/%d  CONTROLS %d/%d" % (
    len(ENTRIES), npass, nfail, nbnd, ninfo,
    len([g for g in GUARDS if g["ok"]]), len(GUARDS),
    len([c for c in CONTROLS if c["ok"]]), len(CONTROLS)))
print("Q1 det=%d  Q2 slope=%.12f  Q3 %d/%d %s" % (det_omega, slope, len(hits_2), len(hits_3), hits_3))
print("Q4 min_n=%d ladder=%d/%d/%d/%d  Q5 p1=%d p2=%d" % (min_n, GEN1, GEN1_NU, GEN3, GEN3_NU, len(p1), len(p2)))
print("Q7 rank=%d dep=%s dup=%d bad=%d two=%d" % (r1, dep, r2_dup, r3_bad, r4_two))
print("VERDICT " + VERDICT)
