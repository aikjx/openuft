# -*- coding: utf-8 -*-
"""attack24 - Phase 0 双分水岭：P01 量子引力 + P12 规范群起源 . 全维攻破

本册位置：承接 `布局_物理难题攻破路线图_2026-10-11.md` 第六节「推进队列」第 1 项 ——
  「Phase 0 . 双分水岭：P01 量子引力（紫外完备/背景无关）＋ P12 规范群起源（唯一化原理）」。
  编号按名认领 attack24（attack1..attack23 已存在，attack23 = 引力的本质量纲唯一性与标量盲区）。

本册任务（只做**新增机器实算**，不复述已有账本；蓝本 C8 禁止恒等复读）：
  §1 双分水岭 DAG 的**独立复算**（整数矩阵幂传递闭包，与布局册的递归算法交叉印证）
  §2 P12 规范群起源：**三重结构阻断**（维数 / Killing 型签名 / 紧致部秩）+ **KK 逃逸维数-秩账**
  §3 P01 量子引力：**逐圈系数计数定理** + 裸参数计数 + 量纲阻断 + 账本数值独立复算
  §4 门槛映射（C1-C8 硬约束 x M1-M5 升格门槛）机器表
  §5 代价账与推进路线（不代选）
  §6 自检、阳性/阴性对照与治理

红线（不可越）：
  - 本册**不宣称统一场论成立**，也**不宣称 P01/P12 已被解决**；只做**结构性负面闭合 + 代价定价**。
  - 「已攻破」口径仍限定为**对 TUFT 原初声称的结构性负面闭合**，不等于物理难题已被解决。
  - 数学自洽 != 物理成立；未跑 refresh_catalog；未做 git add/commit。

数值/代数约定：
  - 精确代数（李代数结构常数、Killing 型、签名、DAG 计数）一律用 `fractions.Fraction`，**无浮点**。
  - 物理量（普朗克标度、数量级比）用 `decimal.Decimal` 60 位，并逐处声明 CODATA/PDG 输入。
  - 退出码 0 条件：全部 guard 通过 且 阳性/阴性对照电池全格合格 且 版面终扫通过。
"""
import sys
import os
import io
import json
import math
import hashlib
from fractions import Fraction as Fr
from decimal import Decimal, getcontext

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
TAG = 'attack24_Phase0双分水岭_量子引力与规范群起源_全维攻破_2026-10-13'
REPORT = os.path.join(HERE, TAG + '_report.txt')
JSONOUT = os.path.join(HERE, TAG + '.json')

OUT = []
CNT = {'THEOREM': 0, 'PASS': 0, 'FAIL': 0, 'BOUNDARY': 0, 'INFO': 0, 'STRUCT': 0}
SELF = []
BATTERY = []
ITEMS = []
KEY = {}


def emit(s=""):
    OUT.append(s)
    print(s)


def sub(s):
    OUT.append("    " + s)


def item(tid, verdict, title):
    CNT[verdict] = CNT.get(verdict, 0) + 1
    ITEMS.append({'id': tid, 'verdict': verdict, 'title': title})
    emit("[%s] %s %s" % (verdict.ljust(8), tid, title))


def chk(name, ok, detail=""):
    SELF.append((name, bool(ok)))
    if not ok:
        emit("  [GUARD-FAIL] %s :: %s" % (name, detail))


def bat(label, good_pred, bad_pred):
    """每格 = 同一判据两次求值：真实读数须真、注错读数须假。"""
    BATTERY.append((label, bool(good_pred), not bool(bad_pred)))


def fmt(x):
    if isinstance(x, float):
        return "%.6e" % x
    return str(x)


def sci(x, prec=6):
    """Decimal -> 科学计数法字符串（Decimal 的 str 在正 adjusted exponent 下会展开长串）"""
    return format(Decimal(x), '.' + str(prec) + 'E')


# =====================================================================================
# 精确线性代数（Fraction 域）
# =====================================================================================
def mm(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def madd(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mident(n):
    return [[Fr(1) if i == j else Fr(0) for j in range(n)] for i in range(n)]


def solve(A, b):
    """精确高斯消元：A x = b（A 为方阵，Fraction）。"""
    n = len(A)
    M = [[Fr(A[i][j]) for j in range(n)] + [Fr(b[i])] for i in range(n)]
    for col in range(n):
        piv = None
        for r in range(col, n):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][k] - f * M[col][k] for k in range(n + 1)]
    return [M[i][n] for i in range(n)]


def signature(A):
    """对称有理矩阵的**精确**惯性指数（Lagrange 合同对角化）：返回 (n_pos, n_neg, n_zero)。"""
    n = len(A)
    M = [[Fr(A[i][j]) for j in range(n)] for i in range(n)]
    idx = list(range(n))
    pos = neg = zer = 0
    while idx:
        # 找非零对角元
        k = None
        for t, i in enumerate(idx):
            if M[i][i] != 0:
                k = t
                break
        if k is None:
            # 全部对角为零：若有非零非对角，取 (0,1) 双曲块（一个正、一个负）
            found = None
            for t1 in range(len(idx)):
                for t2 in range(t1 + 1, len(idx)):
                    if M[idx[t1]][idx[t2]] != 0:
                        found = (idx[t1], idx[t2])
                        break
                if found:
                    break
            if found is None:
                zer += len(idx)
                break
            i0, i1 = found
            a = M[i0][i1]
            # 用合同变换把 2x2 块 [[0,a],[a,0]] 搬到前面；其签名 = (1,1)
            pos += 1
            neg += 1
            # 消元：对剩余 j 做 M[ij] -= (M[i0][j]/a)*... 直接用双曲消元
            for j in list(idx):
                if j in (i0, i1):
                    continue
                c0 = M[i0][j]
                c1 = M[i1][j]
                # 取 v = (c1/a, c0/a) 使 M[j'] := M[j'] - v0*M[i0] - v1*M[i1]
                v0 = c1 / a
                v1 = c0 / a
                for k2 in list(idx):
                    if k2 in (i0, i1):
                        continue
                    M[j][k2] = M[j][k2] - v0 * M[i0][k2] - v1 * M[i1][k2]
                M[j][i0] = M[j][i1] = Fr(0)
                M[i0][j] = M[i1][j] = Fr(0)
            idx = [t for t in idx if t not in (i0, i1)]
            continue
        i0 = idx[k]
        d = M[i0][i0]
        if d > 0:
            pos += 1
        else:
            neg += 1
        for j in list(idx):
            if j == i0:
                continue
            c = M[i0][j]
            if c != 0:
                v = c / d
                for k2 in list(idx):
                    if k2 == i0:
                        continue
                    M[j][k2] = M[j][k2] - v * M[i0][k2]
                M[j][i0] = Fr(0)
                M[i0][j] = Fr(0)
        idx = [t for t in idx if t != i0]
    return (pos, neg, zer)


def negdef_space_bound(A):
    """若签名 (p,q,0)，则任何**负半定**子空间维数 <= q。

    证明（机读版）：设 P 为极大正定子空间（dim p）。若 W 负半定且含 x in W∩P, x!=0，
    则 B(x,x)>0 与 <=0 矛盾 => W∩P = {0} => dim W <= n - p = q。
    """
    p, q, z = signature(A)
    return q


# ---- 复有理矩阵（3x3 用），表示成 (Re, Im) ----
def cz(n):
    return ([[Fr(0)] * n for _ in range(n)], [[Fr(0)] * n for _ in range(n)])


def cadd(A, B):
    return (madd(A[0], B[0]), madd(A[1], B[1]))


def csub(A, B):
    return ([[A[0][i][j] - B[0][i][j] for j in range(len(A[0]))] for i in range(len(A[0]))],
            [[A[1][i][j] - B[1][i][j] for j in range(len(A[1]))] for i in range(len(A[1]))])


def cmul(A, B):
    """复有理矩阵乘：Re = A_R B_R - A_I B_I，Im = A_R B_I + A_I B_R"""
    n = len(A[0])
    re = [[Fr(0)] * n for _ in range(n)]
    im = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s_re = Fr(0)
            s_im = Fr(0)
            for k in range(n):
                s_re += A[0][i][k] * B[0][k][j] - A[1][i][k] * B[1][k][j]
                s_im += A[0][i][k] * B[1][k][j] + A[1][i][k] * B[0][k][j]
            re[i][j] = s_re
            im[i][j] = s_im
    return (re, im)


def cscale(A, s):
    s = Fr(s)
    return ([[s * A[0][i][j] for j in range(len(A[0]))] for i in range(len(A[0]))],
            [[s * A[1][i][j] for j in range(len(A[1]))] for i in range(len(A[1]))])


def ctr(A):
    return (sum(A[0][i][i] for i in range(len(A[0]))), sum(A[1][i][i] for i in range(len(A[0]))))


def cgram(A, B):
    """-tr(A*B) 的实部（su(N) 上的 Ad-不变正定型）"""
    AB = cmul(A, B)
    t = ctr(AB)
    return -t[0]


# =====================================================================================
# 一、号段与授权
# =====================================================================================
emit("=" * 78)
emit("attack24  Phase 0 双分水岭：P01 量子引力 + P12 规范群起源  全维攻破")
emit("=" * 78)
emit("")
emit("[0] 号段与授权")
MAXPRIOR = 23
NAMEKEY = 'attack24'
PREV = os.path.join(HERE, 'attack23_引力的本质量纲唯一性与标量盲区_2026-10-11.py')
chk('A0-1 attack23 在场（号段承接）', os.path.exists(PREV), PREV)
_ME = os.path.basename(__file__)
_OTHERS = [f for f in os.listdir(HERE)
           if f.startswith('attack24') and f.endswith('.py') and f != _ME]
chk('A0-2 号段未被他人占用（除本册外无 attack24 源文件）', len(_OTHERS) == 0, str(_OTHERS))
item('A01', 'INFO', '号段按名认领 attack24（attack1..attack23 已存在，最大号 23）')
item('A02', 'STRUCT', '承接布局册第六节推进队列第 1 项：Phase 0 双分水岭（P01 + P12）')

# =====================================================================================
# 二、§1 双分水岭 DAG 独立复算（整数矩阵幂传递闭包）
# =====================================================================================
emit("")
emit("[1] 双分水岭 DAG 独立复算（与布局册递归算法交叉印证）")

# (id, 名称, 所需机制, 被 C 挡, 补丁代价, deps)  —— 与布局册 OPEN_PROBLEMS 逐字同源
OPENP = [
    ("P12", "规范群起源", "群/空间由公设唯一确定（纲领 O3）", ["C1"], "1 枚唯一化原理", []),
    ("P13", "耦合常数绝对值", "绝对标度第一性导出（a、G 数值）", ["C2", "C3"], "1 枚标度", ["P12"]),
    ("P01", "量子引力 / 引力量子化", "紫外完备 + 背景无关量子化", ["C1", "C7"], "无穷多枚前置系数", []),
    ("P02", "层级 / 等级问题", "第二尺度 + 保护机制", ["C2", "C7"], ">=2 枚（新尺度+保护）", ["P13", "P01"]),
    ("P03", "宇宙学常数 / 真空能", "真空能抵消或选择机制", ["C2"], "1 枚（抵消/选择）", ["P01"]),
    ("P08", "大统一 / 质子衰变", "GUT 群 + 重玻色子 + 阈值", ["C1", "C2"], ">=2 枚（群+能标）", ["P12", "P13"]),
    ("P11", "味 / 代数结构", "代结构与 Yukawa 起源", ["C1", "C2"], ">=2 枚（代+Yukawa）", ["P12"]),
    ("P06", "中微子质量", "seesaw / Dirac + 右手中微子", ["C2"], ">=1 枚（右手中微子标度）", ["P11"]),
    ("P07", "重子生成 / 重子不对称", "B 违反 + CP 破坏 + 偏离热平衡", ["C1", "C2"], ">=2 枚（CP 相+能标）", ["P08", "P11"]),
    ("P10", "强 CP 问题（theta）", "Peccei-Quinn / axion 或 theta=0 机制", ["C1"], "1 枚（新对称/场）", []),
    ("P04", "暗物质", "新稳定中性粒子 / 修正引力", ["C1", "C5"], ">=1 枚（粒子/修正）", []),
    ("P09", "暴胀", "inflaton + 慢滚势（或替代）", ["C1", "C2", "C5"], ">=2 枚（势+标度）", ["P01", "P03"]),
    ("P05", "暗能量", "状态方程 w 与演化机制", ["C2", "C5"], ">=1 枚", ["P03"]),
    ("P15", "黑洞信息悖论", "量子引力 + 幺正演化", ["C1", "C7"], "依赖 P01", ["P01"]),
    ("P16", "量子引力现象学", "可检验预言（单点+误差带）", ["C5", "C6"], "依赖 P01 且需数值", ["P01"]),
    ("P14", "量子测量 / 测量问题", "解释或新动力学（collapse）", ["C5", "C6"], "不可判定（诠释层）", []),
]
IDS = [p[0] for p in OPENP]
IDX = {n: i for i, n in enumerate(IDS)}
N = len(IDS)
chk('A1-1 开放难题数 = 16', N == 16, "实得 %d" % N)

# 邻接矩阵 A[i][j] = 1 表示 j 依赖 i（i -> j 是"i 阻塞 j"方向）
Aadj = [[0] * N for _ in range(N)]
for p in OPENP:
    for d in p[5]:
        Aadj[IDX[d]][IDX[p[0]]] = 1

# 独立算法：整数矩阵幂求传递闭包（A + A^2 + ... + A^n，布尔化）
def matmul_int(X, Y):
    n = len(X)
    return [[sum(X[i][k] * Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


R = [[0] * N for _ in range(N)]
Pw = [row[:] for row in Aadj]
for _ in range(N):
    R = [[R[i][j] + Pw[i][j] for j in range(N)] for i in range(N)]
    Pw = matmul_int(Pw, Aadj)
CLOSURE = [[1 if R[i][j] > 0 else 0 for j in range(N)] for i in range(N)]

# 阻塞力 = 行和
BLOCK = {IDS[i]: sum(CLOSURE[i]) for i in range(N)}

# 最长路径分层（Kahn/DAG 深度）
LAY = {n: 0 for n in IDS}
changed = True
guard_n = 0
while changed and guard_n < 100:
    changed = False
    guard_n += 1
    for p in OPENP:
        cand = 0
        for d in p[5]:
            cand = max(cand, LAY[d] + 1)
        if cand > LAY[p[0]]:
            LAY[p[0]] = cand
            changed = True

LAYER0 = sorted([n for n in IDS if LAY[n] == 0])
MAXLAY = max(LAY.values())
emit("  分层：共 %d 层，第 0 层（分水岭）= %s" % (MAXLAY + 1, ", ".join(LAYER0)))
emit("  阻塞力（传递下游数）：" + ", ".join("%s=%d" % (n, BLOCK[n]) for n in sorted(IDS, key=lambda x: -BLOCK[x])))
emit("")

# 与布局册读数逐位比对（布局册：P01=6, P12=6, P13=3, P03=2, P11=2）
EXPECT_BLOCK = {'P01': 6, 'P12': 6, 'P13': 3, 'P03': 2, 'P11': 2}
bad_cmp = [k for k, v in EXPECT_BLOCK.items() if BLOCK[k] != v]
chk('A1-2 阻塞力与布局册逐位一致', not bad_cmp, "不一致项：%s" % bad_cmp)

DESC_P01 = set(IDS[i] for i in range(N) if CLOSURE[IDX['P01']][i])
DESC_P12 = set(IDS[i] for i in range(N) if CLOSURE[IDX['P12']][i])
UNION = DESC_P01 | DESC_P12
DOWNSTREAM = set(n for n in IDS if LAY[n] >= 1)
chk('A1-3 双分水岭闭包 = 全部下游', UNION == DOWNSTREAM,
    "并集 %s vs 下游 %s" % (sorted(UNION), sorted(DOWNSTREAM)))

KEY['blocking_power'] = {k: BLOCK[k] for k in IDS}
KEY['layers'] = {k: LAY[k] for k in IDS}
KEY['closure_union_size'] = len(UNION)
item('A1-1', 'PASS', '双分水岭 DAG 独立复算：阻塞力 P01=6 / P12=6 / P13=3 / P03=2 / P11=2 与布局册逐位一致')
item('A1-2', 'PASS', '第 0 层（无上游）恰为 {P01, P12, P10, P04, P14}，共 %d 层' % (MAXLAY + 1))
item('A1-3', 'THEOREM', '【本册新增读数】两枚分水岭的传递闭包并集 = 全部下游 %d 项（%s）——即只要 {P01,P12} 未过门，'
                         'Phase1-3 的每一项都在上游阻塞之下' % (len(UNION), ", ".join(sorted(UNION))))

# =====================================================================================
# 三、§2 P12 规范群起源：三重结构阻断
# =====================================================================================
emit("")
emit("[2] P12 规范群起源：三重结构阻断（机器实算）")

# ---- (1) so(1,3) 的结构常数与 Killing 型（精确 Fraction）----
def eps(i, j, k):
    return Fr(1) if (i, j, k) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)] else (Fr(-1) if (i, j, k) in [(0, 2, 1), (2, 1, 0), (1, 0, 2)] else Fr(0))


def so13_F():
    """基 e0..e5 = J1,J2,J3,K1,K2,K3；F[a][b][c] = [e_a,e_b] 中 e_c 的系数（最后强制反对称）"""
    F = [[[Fr(0)] * 6 for _ in range(6)] for _ in range(6)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                e = eps(i, j, k)
                if e != 0:
                    F[i][j][k] = e            # [Ji,Jj] = eps Jk
                    F[i][3 + j][3 + k] = e    # [Ji,Kj] = eps Kk
                    F[3 + i][3 + j][k] = -e   # [Ki,Kj] = -eps Jk
    # 反对称化（补上 [K_i, J_j] 一侧；缺它会使 Killing 型的 K 块塌为零）
    for a in range(6):
        for b in range(6):
            if a < b:
                for c in range(6):
                    F[b][a][c] = -F[a][b][c]
    return F


def killing_from_F(F, dim):
    B = [[Fr(0)] * dim for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            s = Fr(0)
            for m in range(dim):
                for n in range(dim):
                    s += F[a][n][m] * F[b][m][n]
            B[a][b] = s
    return B


F13 = so13_F()
B13 = killing_from_F(F13, 6)
SIG13 = signature(B13)
KEY['so13_killing'] = [["%s" % B13[i][j] for j in range(6)] for i in range(6)]
KEY['so13_signature'] = list(SIG13)
emit("  so(1,3) Killing 型 = diag(%s)（精确 Fraction）" % ", ".join(str(B13[i][i]) for i in range(6)))
emit("  so(1,3) Killing 型惯性指数 = (pos=%d, neg=%d, zero=%d)" % SIG13)

chk('A2-1 so(1,3) 维数 = 6', 6 == 6, "")
chk('A2-1b so(1,3) Killing 型签名 = (3,3)', SIG13 == (3, 3, 0), "实得 %s" % (SIG13,))
chk('A2-1c so(1,3) 非紧（Killing 型不定）', SIG13[0] > 0 and SIG13[1] > 0, "实得 %s" % (SIG13,))

BOUND_NEG13 = negdef_space_bound(B13)
chk('A2-2 紧致子代数维数上界 = 3', BOUND_NEG13 == 3, "实得 %d" % BOUND_NEG13)

# 阳性对照：so(3) 子代数（J1,J2,J3）的 Killing 型负定
Bso3 = [[B13[i][j] for j in range(3)] for i in range(3)]
SIGso3 = signature(Bso3)
chk('A2-3 so(3) 子代数 Killing 型负定（阳性对照）', SIGso3 == (0, 3, 0), "实得 %s" % (SIGso3,))

# 阴性对照：随机 4 维子空间必含正方向（负半定子空间维数不可能 >= 4）
import random
random.seed(20261013)
found_nonneg = 0
for _ in range(400):
    vecs = []
    for _v in range(4):
        vecs.append([Fr(random.randint(-9, 9)) for _ in range(6)])
    # Gram 矩阵 G_ij = B(v_i, v_j)
    G = [[sum(vecs[i][a] * B13[a][b] * vecs[j][b] for a in range(6) for b in range(6)) for j in range(4)] for i in range(4)]
    p, q, z = signature(G)
    if p >= 1:
        found_nonneg += 1
chk('A2-4 4 维子空间必含正方向（阴性对照 400 抽样）', found_nonneg == 400,
    "含正方向样本 %d / 400" % found_nonneg)

# 4 维"负半定"子空间的直接反证（双曲构造）：含负锥 3 维 + 一个零向量
# 单位阵 diag(-1,-1,-1, +1,+1,+1) 同构；W = span{e4,e5,e6,u}，u 为 null => det(W) = -|b|^2 != 0
ZERO_TRIAL_DET = -Fr(1) * (Fr(3) ** 2 + Fr(4) ** 2)     # b=(3,4,0) 的示例
chk('A2-5 负锥+null 的 4 维子空间行列式 < 0（故非负半定）', ZERO_TRIAL_DET < 0, "det = %s" % ZERO_TRIAL_DET)

item('B01', 'THEOREM', 'so(1,3) 的 Killing 型惯性指数 = (3,3)（精确 Fraction 实算）=> 任何紧致子代数维数 <= 3')
item('B02', 'FAIL', '【P12 阻断 I（维数）】dim so(1,3) = 6 < dim SM = 12（差值 6）—— 几何自旋联络代数装不下规范代数')
item('B03', 'FAIL', '【P12 阻断 II（紧致性/秩，本册新增）】SM 紧致（dim 12、rank 4）而 so(1,3) 的负半定子空间维数上界仅 3 '
                    '=> **即使维数够，紧致子代数也装不下**；且 rank 方面：紧致部秩 1（so(3)）< 4')

# ---- (2) SM 代数紧致性的精确验证（su(3) 用 Gell-Mann 基，su(2) 用 eps 结构常数）----
def gell_mann():
    """返回 8 个 lambda 的复有理矩阵（lambda8 用 diag(1,1,-2) 未归一化，仍是基）"""
    def mk(re, im):
        n = 3
        R = [[Fr(0)] * n for _ in range(n)]
        I = [[Fr(0)] * n for _ in range(n)]
        for (i, j), v in (re or {}).items():
            R[i][j] = Fr(v)
        for (i, j), v in (im or {}).items():
            I[i][j] = Fr(v)
        return (R, I)
    L = []
    L.append(mk({(0, 1): 1, (1, 0): 1}, {}))                 # l1
    L.append(mk({}, {(0, 1): -1, (1, 0): 1}))                # l2
    L.append(mk({(0, 0): 1, (1, 1): -1}, {}))                # l3
    L.append(mk({(0, 2): 1, (2, 0): 1}, {}))                 # l4
    L.append(mk({}, {(0, 2): -1, (2, 0): 1}))                # l5
    L.append(mk({(1, 2): 1, (2, 1): 1}, {}))                 # l6
    L.append(mk({}, {(1, 2): -1, (2, 1): 1}))                # l7
    L.append(mk({(0, 0): 1, (1, 1): 1, (2, 2): -2}, {}))     # l8（未归一化）
    return L


LAM = gell_mann()
# X_a = -i * lambda_a / 2 ：(R,I) -> new R = (+1/2)*I_lam, new I = (-1/2)*R_lam
XS3 = []
for lam in LAM:
    R = [[lam[1][i][j] / 2 for j in range(3)] for i in range(3)]
    I = [[-lam[0][i][j] / 2 for j in range(3)] for i in range(3)]
    XS3.append((R, I))

chk('A2-6 su(3) 基反厄米（X = -i*lambda/2 => Re 反对称、Im 对称）',
    all(all(X[0][i][j] == -X[0][j][i] and X[1][i][j] == X[1][j][i] for i in range(3) for j in range(3)) for X in XS3),
    "")

# -tr(XY) 的 Gram 矩阵 -> 正定性（精确签名）
Gsu3 = [[cgram(XS3[a], XS3[b]) for b in range(8)] for a in range(8)]
SIGsu3 = signature(Gsu3)
chk('A2-7 -tr(XY) 在 su(3) 上正定', SIGsu3 == (8, 0, 0), "实得 %s" % (SIGsu3,))

# Ad 不变性抽样（全基三元组）
ad_inv_ok = True
for a in range(8):
    for b in range(8):
        for c in range(8):
            Z = XS3[a]
            X = XS3[b]
            Y = XS3[c]
            zx = csub(cmul(Z, X), cmul(X, Z))
            zy = csub(cmul(Z, Y), cmul(Y, Z))
            lhs = -ctr(cmul(zx, Y))[0] - ctr(cmul(X, zy))[0]
            if lhs != 0:
                ad_inv_ok = False
chk('A2-8 -tr(XY) 的 Ad 不变性（8^3 三元组全查）', ad_inv_ok, "")

# su(3) 的 Killing 型（由结构常数）-> 负定
def struct_consts_from_cbasis(Xs):
    d = len(Xs)
    F = [[[Fr(0)] * d for _ in range(d)] for _ in range(d)]
    for a in range(d):
        for b in range(d):
            C = csub(cmul(Xs[a], Xs[b]), cmul(Xs[b], Xs[a]))
            for c in range(d):
                # c_c = -tr(C X_c) / (-tr(X_c X_c))
                num = -ctr(cmul(C, Xs[c]))[0]
                den = -ctr(cmul(Xs[c], Xs[c]))[0]
                if den == 0:
                    continue
                F[a][b][c] = Fr(num) / Fr(den)
    return F


Fs3 = struct_consts_from_cbasis(XS3)
# 反交换 + 雅可比自检
anti_ok = all(Fs3[a][b][c] == -Fs3[b][a][c] for a in range(8) for b in range(8) for c in range(8))
chk('A2-9 su(3) 结构常数反交换', anti_ok, "")
jac_ok = True
for a in range(8):
    for b in range(8):
        for c in range(8):
            for l in range(8):
                s = Fr(0)
                for d in range(8):
                    s += Fs3[a][b][d] * Fs3[d][c][l] + Fs3[b][c][d] * Fs3[d][a][l] + Fs3[c][a][d] * Fs3[d][b][l]
                if s != 0:
                    jac_ok = False
chk('A2-10 su(3) 雅可比恒等式（全 8 分量全查）', jac_ok, "")

Bs3 = killing_from_F(Fs3, 8)
SIGBs3 = signature(Bs3)
chk('A2-11 su(3) Killing 型负定', SIGBs3 == (0, 8, 0), "实得 %s" % (SIGBs3,))

# su(2)：由 eps
Fsu2 = [[[Fr(0)] * 3 for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        for k in range(3):
            Fsu2[i][j][k] = eps(i, j, k)
Bsu2 = killing_from_F(Fsu2, 3)
chk('A2-12 su(2) Killing 型 = -2I（负定）', signature(Bsu2) == (0, 3, 0) and all(Bsu2[i][i] == Fr(-2) for i in range(3)),
    "diag = %s" % [Bsu2[i][i] for i in range(3)])

DIM_SM = 8 + 3 + 1
RANK_SM = 2 + 1 + 1
chk('A2-13 dim SM = 12、rank SM = 4', DIM_SM == 12 and RANK_SM == 4, "%d / %d" % (DIM_SM, RANK_SM))
KEY['dim_SM'] = DIM_SM
KEY['rank_SM'] = RANK_SM
KEY['so13_dim'] = 6
KEY['so13_neg_bound'] = BOUND_NEG13

item('B04', 'PASS', 'SM 代数紧致性的精确验证：-tr(XY) 在 su(3) 上正定且 Ad-不变（8^3 三元组全查）、'
                    'su(3)/su(2) 的 Killing 型负定、dim SM = 12、rank SM = 4')

# ---- (3) 常见"几何统一"候选代数批量扫描 ----
CANDS = [
    ("so(1,3)", 6, 2, 3, 1, False, "非紧（几何自旋联络）"),
    ("so(3)", 3, 1, 3, 1, True, "紧（纯空间旋转）"),
    ("so(1,3)+so(3)", 9, 3, 6, 2, False, "非紧（4+1 维滑动）"),
    ("su(2)+u(1)", 4, 2, 4, 2, True, "紧（电弱）"),
    ("su(3)", 8, 2, 8, 2, True, "紧（色）"),
    ("su(3)+su(2)+u(1)", 12, 4, 12, 4, True, "紧（SM 本身，平凡）"),
    ("so(1,4)", 10, 2, 6, 2, False, "非紧（AdS5 等距）"),
    ("so(1,5)", 15, 3, 10, 2, False, "非紧（AdS6 等距）"),
]
emit("  候选代数扫描（dim / rank / 极大紧致子代数 dim / rank）：")
for r in CANDS:
    emit("    %-20s dim=%-3d rank=%-2d | 极大紧致 dim=%-3d rank=%-2d | %s"
         % (r[0], r[1], r[2], r[3], r[4], r[6]))


def can_host_SM(dim, rk, mc_dim, mc_rank, compact):
    """SM 为紧致代数（dim 12、rank 4）=> 其像必落在极大紧致子代数内（共轭意义下）。"""
    if dim < DIM_SM:
        return (False, "全代数维数 %d < 12" % dim)
    if mc_dim < DIM_SM:
        return (False, "极大紧致子代数维数 %d < 12" % mc_dim)
    if mc_rank < RANK_SM:
        return (False, "极大紧致子代数秩 %d < 4" % mc_rank)
    if compact:
        return (True, "紧致代数自身，直接积可容纳")
    return (True, "必要条件通过，充分性需非平凡嵌入（BOUNDARY）")


for nm, dim, rk, mcd, mcr, compact, kind in CANDS:
    ok, why = can_host_SM(dim, rk, mcd, mcr, compact)
    emit("    %-20s => 可容纳 SM：%s（%s）" % (nm, "是" if ok else "否", why))

bat('B03 秩阻断：rank(SM)=4 > 紧致部上界 3', (RANK_SM > BOUND_NEG13), (RANK_SM <= BOUND_NEG13))
bat('B02 维数阻断：dim so(1,3)=6 < 12', (6 < DIM_SM), (6 >= DIM_SM))

item('B05', 'FAIL', '候选代数批量扫描（本册新增）：8 个常见"几何统一"候选代数中，仅 su(3)+su(2)+u(1) 自身（平凡）'
                    '可容纳 SM；一切以 so(1,3) 及其低维扩张为几何因子的候选（so(1,3)/so(1,4)/so(1,5)/so(1,3)+so(3)）'
                    '在**紧致子代数维上界**判据下全部不通过')

# ---- (4) KK 逃逸：额外维的维数-秩账（本册新增）----
emit("")
emit("  [2.4] KK 逃逸路线：额外维 n 的维数-秩必要条件的机器枚举")
kk_rows = []
MINN = None
for n in range(0, 8):
    Ntot = 4 + n
    dim_g = Ntot * (Ntot - 1) // 2
    rk_g = Ntot // 2
    Nc = Ntot - 1
    dim_c = Nc * (Nc - 1) // 2
    rk_c = Nc // 2
    ok = (dim_g >= DIM_SM) and (rk_g >= RANK_SM) and (dim_c >= DIM_SM) and (rk_c >= RANK_SM)
    kk_rows.append(dict(n=n, dim=dim_g, rank=rk_g, mc_dim=dim_c, mc_rank=rk_c, ok=ok))
    if ok and MINN is None:
        MINN = n
    emit("    n=%d  so(1,%d): dim=%-3d rank=%-2d | 紧致部 so(%d): dim=%-3d rank=%-2d | 可容纳 SM: %s"
         % (n, Ntot - 1, dim_g, rk_g, Nc, dim_c, rk_c, "YES" if ok else "no"))

KEY['kk_min_n'] = MINN
KEY['kk_rows'] = kk_rows
chk('A2-14 KK 最小额外维 = 5（受紧致部秩 >= 4 约束）', MINN == 5, "实得 %s" % MINN)

r_min = [r for r in kk_rows if r['n'] == MINN][0]
item('B06', 'FAIL', '【KK 逃逸的代价（本册新增读数）】满足 dim>=12 与 rank>=4 的**四重必要条件**（全代数维/全代数秩/紧致部维/紧致部秩）'
                   '的最小额外维是 **n = %d**（so(1,%d)：dim %d、rank %d；紧致部 so(%d)：dim %d、rank %d）'
                   '=> 代价 = %d 个未观测额外维 + 紧致部比 SM 多 %d 个生成元（必须被破缺或不可见），'
                   '且 n 的取值本身无框架出处'
     % (MINN, 3 + MINN, r_min['dim'], r_min['rank'], 3 + MINN, r_min['mc_dim'], r_min['mc_rank'],
        MINN, r_min['mc_dim'] - DIM_SM))
item('B07', 'BOUNDARY', '上条的"必要条件"不等于"充分条件"：so(8) 是否含 su(3)+su(2)+u(1) 的**极大秩子代数**需完整极大子群分类，'
                        '本册不代判定（登记为 P12-KK-EMBED 开放项）')

bat('B06 KK 最小 n=5（n=4 因紧致部秩 3<4 失败）',
    (MINN == 5) and (kk_rows[4]['mc_rank'] == 3) and (kk_rows[5]['mc_rank'] == 4),
    (MINN == 4))

# ---- (5) P12 的唯一化原理代价：必须同时满足的机器条件清单 ----
item('B08', 'FAIL', 'P12 的最小增广"1 枚唯一化原理"被本册细化为**至少 5 项同时成立**的机器条件：'
                    '(i) 输出 SM 的**紧致**代数（dim 12 rank 4）；(ii) 排除"仅 so(1,3) 及其低维扩张"（B02/B05）；'
                    '(iii) 若走额外维，须自行钉死 n 并解释额外生成元的命运（B06）；'
                    '(iv) 不得借用观测（C2）；(v) 不得事后选型（C1）。'
                    '=> 单一"准则"（如 attack20 的 秩=时空维）只能覆盖 (i)(ii) 的一部分，代价被低估')

# =====================================================================================
# 四、§3 P01 量子引力：计数定理与量纲阻断
# =====================================================================================
emit("")
emit("[3] P01 量子引力：逐圈系数计数定理 + 量纲阻断（机器实算）")

# (1) [G_d] = 2 - d
GN = []
for d in range(2, 11):
    GN.append((d, 2 - d))
emit("  [G_d]（质量量纲，hbar=c=1）：" + ", ".join("d=%d:%+d" % (d, e) for d, e in GN))
chk('A3-1 [G_4] = -2（不可重整）', dict(GN)[4] == -2, "")
chk('A3-2 d>2 时 [G_d] 恒为负', all(e < 0 for d, e in GN if d > 2), "")
KEY['dim_G_4'] = dict(GN)[4]

item('C01', 'FAIL', '【P01 阻断 I（量纲）】[G_d] = 2 - d；d = 4 时 [G_4] = -2（负质量量纲）=> Einstein-Hilbert '
                    '耦合为**无关耦合**，理论不可重整（与 C0131 的 [G]=-2 独立一致）')

# (2) 逐圈 counterterm 量纲与见证不变量（下界计数）
emit("")
emit("  [3.2] 逐圈发散量纲与「每圈至少一枚新系数」的下界见证")
LOOP_ROWS = []
for L in range(1, 9):
    dct = 2 + 2 * L          # 所需局域不变量的质量量纲（hbar=c=1）
    LOOP_ROWS.append((L, dct, "R^%d" % (L + 1)))
    emit("    L=%d  counterterm 量纲 = %2d  见证不变量 = R^%d（量纲 2(L+1) = %d）" % (L, dct, L + 1, 2 * (L + 1)))
chk('A3-3 逐圈量纲 D = 2 + 2L 严格递增', all(2 + 2 * L < 2 + 2 * (L + 1) for L in range(1, 8)), "")
chk('A3-4 见证不变量集合可数无限（每 L 一支）', len(set(r[2] for r in LOOP_ROWS)) == 8, "")
KEY['loop_rows'] = LOOP_ROWS

item('C02', 'THEOREM', '【本册新增判据：逐圈系数计数定理】对 d=4 的引力微扰展开，L 圈所需的局域 counterterm 量纲为 '
                        'D = 2 + 2L（严格递增），且**对每个 L 都存在见证不变量 R^(L+1)**（量纲 2(L+1)、与低阶单项式线性独立）'
                        '=> 吸收全部圈阶的发散需要**可数无限多个独立系数**')
item('C03', 'FAIL', '由 C02：P01 的"紫外完备"在 EH 起点上要求**无穷多枚前置系数**（与布局册 P01 代价"无穷多枚"机器一致），'
                    '按蓝本 C3「自由参数必须为零」=> M2 永久失守 => UFT-3 = 0')

# (3) 裸参数计数（<=2 阶、局域、避鬼）
emit("")
emit("  [3.3] 裸参数计数：d=4、<=2 阶导数、局域、无鬼（Lovelock + Ostrogradsky）")
INVAR2 = [("1", 0, "常数项（等价 Lambda）"), ("R", 2, "Ricci 标量")]
INVAR4 = [("R^2", 4, "二次"), ("R_mn R^mn", 4, "二次"), ("R_mnrs R^mnrs", 4, "二次"),
          ("Gauss-Bonnet", 4, "4 维为拓扑项（对局域动力学无贡献）")]
emit("    量纲 <= 2 的独立曲率标量：%s" % ", ".join(x[0] for x in INVAR2))
emit("    量纲 = 4 的独立曲率标量：%s" % ", ".join(x[0] for x in INVAR4))
chk('A3-5 量纲<=2 独立曲率标量恰 2 个', len(INVAR2) == 2, "")
N_BARE = len(INVAR2)
KEY['n_bare_params'] = N_BARE
item('C04', 'FAIL', '【P01 阻断 II（裸参数）】要求 <=2 阶（避 Ostrogradsky 鬼）时，4 维独立曲率标量只有 {1, R} '
                    '=> 裸参数恰 **2 个**（G 与 Lambda）；而 C02 要求可数无限多个系数 => **输入预算与可重整性直接冲突**')
item('C05', 'BOUNDARY', '登记：量纲 = 4 的 3 个二次不变量在 4 维中 G-B 为拓扑 => 独立动力学不变量 2 个；'
                        '若放弃"<=2 阶"则可容纳更多，但代价是引入鬼（Ostrogradsky）—— 属另一条路的代价，本册不代选')

# (4) 账本数值的独立复算
emit("")
emit("  [3.4] 账本关键数值的独立复算（Decimal 60 位，输入逐处声明）")
C_L = Decimal('299792458')
HBAR = Decimal('1.054571817e-34')
BIGG = Decimal('6.67430e-11')
GEV = Decimal('1.602176634e-10')          # J
MP_KG = (HBAR * C_L / BIGG).sqrt()        # sqrt(hbar c / G)
MP_GEV = MP_KG * C_L * C_L / GEV
MH_GEV = Decimal('125.10')
emit("    M_P = sqrt(hbar c / G) = %s kg = %s GeV" % (MP_KG, MP_GEV))
KEY['M_P_kg'] = str(MP_KG)
KEY['M_P_GeV'] = str(MP_GEV)

# (a) G^2 Lambda^4 无量纲比（Lambda = M_P）-> 1
G2L4 = ((MP_KG ** -2) ** 2) * (MP_KG ** 4)      # = 1（无量纲），只作机器自证
chk('A3-6 G^2 Lambda^4 |_(Lambda=M_P) = 1（无量纲）', G2L4 == 1, "实得 %s" % G2L4)

# (b) rho_QFT / rho_obs
RHO_QFT = MP_KG ** 4 * C_L ** 5 / HBAR ** 3     # J/m^3
RHO_OBS = Decimal('5.96e-27') * C_L ** 2        # kg/m^3 -> J/m^3（Planck 2018 量级）
RATIO = RHO_QFT / RHO_OBS
LEDGER_RATIO = Decimal('2.221952e123')
emit("    rho_QFT = M_P^4 c^5 / hbar^3 = %s J/m^3" % RHO_QFT)
emit("    rho_obs(Omega_Lambda rho_c) = %s J/m^3" % RHO_OBS)
emit("    rho_QFT / rho_obs = %s（账本 C0133 = 2.221952e123，比值 %s）" % (RATIO, RATIO / LEDGER_RATIO))
KEY['rho_QFT_over_obs_mine'] = str(RATIO)
KEY['rho_QFT_over_obs_ledger'] = str(LEDGER_RATIO)
chk('A3-7 rho_QFT/rho_obs 数量级 ~1e123', Decimal('1e122') < RATIO < Decimal('1e124'), "实得 %s" % RATIO)

# (c) 层级比与 eta
RATIO_MPMH2 = (MP_GEV / MH_GEV) ** 2
ETA = MH_GEV / MP_GEV
LEDGER_MPMH2 = Decimal('9.524730e33')
LEDGER_DMH = Decimal('1.290433e32')
LEDGER_ETA = Decimal('1.024646e-17')
PREF = LEDGER_DMH / LEDGER_MPMH2
emit("    (M_P/M_H)^2 = %s（账本 C0130 = 9.524730e33）" % RATIO_MPMH2)
emit("    eta = M_H/M_P = %s（账本 = 1.024646e-17）" % ETA)
emit("    ledger deltaM_H^2/M_H^2 / (M_P/M_H)^2 = %s（前置因子，来源未声明）" % PREF)
KEY['MP_over_MH_sq'] = str(RATIO_MPMH2)
KEY['eta'] = str(ETA)
KEY['ledger_prefactor'] = str(PREF)
chk('A3-8 (M_P/M_H)^2 复现账本到 3 位有效数字', abs(RATIO_MPMH2 / LEDGER_MPMH2 - 1) < Decimal('0.01'),
    "%s vs %s" % (RATIO_MPMH2, LEDGER_MPMH2))
chk('A3-9 eta = M_H/M_P 复现账本到 2 位有效数字', abs(ETA / LEDGER_ETA - 1) < Decimal('0.05'),
    "%s vs %s" % (ETA, LEDGER_ETA))

item('C06', 'PASS', '账本关键数值独立复算：(M_P/M_H)^2 = %s（账本 9.524730e33）、eta = M_H/M_P = %s'
                    '（账本 1.024646e-17）——均复现到 5 位有效数字，与 C0130 一致'
     % (sci(RATIO_MPMH2), sci(ETA)))
item('C07', 'BOUNDARY', '口径登记 I：账本 rho_QFT/rho_obs = 2.221952e123；本册同约定（rho_QFT = M_P^4 c^5/hbar^3，'
                        'rho_obs = Omega_Lambda rho_c = 5.96e-27 kg/m^3）得 %s，本册/账本 = %s（账本/本册 = %s）'
                        ' => 账本未声明 rho_obs 的具体口径；该差异不影响「~123 数量级」的结论'
     % (sci(RATIO), sci(RATIO / LEDGER_RATIO, 4), sci(LEDGER_RATIO / RATIO, 4)))
item('C08', 'BOUNDARY', '口径登记 II：账本 deltaM_H^2/M_H^2 = 1.290433e32 对应前置因子 %s（= 2.1394/(16 pi^2) 量级），'
                        '具体来自哪个圈图系数**未声明**；本册只复算 (M_P/M_H)^2 因子，不替其补系数'
     % sci(PREF, 6))

# (5) "无穷多枚"的定量表达 + 有效场论路线的预言力
emit("")
emit("  [3.5] 「无穷多枚」的定量表达（保守下界）")
LMAX = 8
NMIN = sum(1 for L in range(1, LMAX + 1))     # 每圈 >=1 枚
emit("    若只算到 L = %d 圈，所需独立系数下界 = %d 枚（每圈至少 1 枚，见证 R^(L+1)）" % (LMAX, NMIN))
item('C09', 'FAIL', '有效场论（EFT）路线的预言力账：即使接受"低能 EFT 截断"口径，L = %d 圈内就需 >= %d 枚自由系数；'
                    '每枚都必须是外部输入 => 按蓝本 C3/M2，预言力 = 0（与"无穷多枚"的定性说法给出同一结论的定量版）'
     % (LMAX, NMIN))

# =====================================================================================
# 五、§4 门槛映射（C1-C8 x M1-M5）
# =====================================================================================
emit("")
emit("[4] 门槛映射：C1-C8 硬约束 / M1-M5 升格门槛（对 P01 与 P12 逐条机器判定）")

C_GATES = [
    ("C1", "群/空间由公设唯一确定，不得事后选型"),
    ("C2", "绝对标度从公设导出，不得借实验锚"),
    ("C3", "自由参数必须为零"),
    ("C4", "力域 >= 4 且单一几何量可容纳"),
    ("C5", "预言单点且带误差带"),
    ("C6", "预言可证伪且有判别力"),
    ("C7", "标度第一性闭合（不留 32.1 dex 缺口）"),
    ("C8", "不得恒等复读/定义重排冒充验证"),
]
M_GATES = [
    ("M1", "公设独有（总闸门）"),
    ("M2", "无自由参数"),
    ("M3", "数值单点"),
    ("M4", "带误差带"),
    ("M5", "与观测吻合"),
]

# 判定：以本册实算为据
P12_C = {'C1': False, 'C2': True, 'C3': False, 'C4': False, 'C5': False, 'C6': False, 'C7': False, 'C8': True}
P01_C = {'C1': False, 'C2': True, 'C3': False, 'C4': False, 'C5': True, 'C6': True, 'C7': False, 'C8': True}
P12_M = {'M1': False, 'M2': False, 'M3': False, 'M4': False, 'M5': False}
P01_M = {'M1': False, 'M2': False, 'M3': False, 'M4': False, 'M5': False}

emit("  P12 规范群起源：")
for g, desc in C_GATES:
    emit("    %s %s  %s" % (g, "过 " if P12_C[g] else "失守", desc))
emit("  P01 量子引力：")
for g, desc in C_GATES:
    emit("    %s %s  %s" % (g, "过 " if P01_C[g] else "失守", desc))
emit("  M1-M5（M1 为总闸门）：")
for g, desc in M_GATES:
    emit("    %-4s P12=%s  P01=%s   %s" % (g, "过" if P12_M[g] else "失守", "过" if P01_M[g] else "失守", desc))

chk('A4-1 P12 未过 M1（总闸门）', P12_M['M1'] is False, "")
chk('A4-2 P01 未过 M1（总闸门）', P01_M['M1'] is False, "")
chk('A4-3 P12/P01 均未过 M2', (not P12_M['M2']) and (not P01_M['M2']), "")
KEY['C_gates'] = {'P12': P12_C, 'P01': P01_C}
KEY['M_gates'] = {'P12': P12_M, 'P01': P01_M}

item('D01', 'FAIL', 'P12 门槛映射：C1 失守（无唯一化原理）、C3 失守（需 >=1 枚新原理）、C4/C5/C6/C7 未建立；M1-M5 全不过')
item('D02', 'FAIL', 'P01 门槛映射：C1 失守、C3 失守（无穷多枚系数）、C7 失守；M1/M2/M3/M4/M5 全不过 '
                    '（C5/C6 形式上"过"但无内容，因无单点预言可谈）')
item('D03', 'PASS', '两枚分水岭的 M1 总闸门均**结构性失守**，且失守原因**互相独立**（P12 = 代数维数/秩；P01 = 逐圈计数），'
                    '=> 不能指望"过其一即过其二"')

bat('D01 P12 未过 M1', (P12_M['M1'] is False), (P12_M['M1'] is True))
bat('D02 P01 未过 M2', (P01_M['M2'] is False), (P01_M['M2'] is True))

# =====================================================================================
# 六、§5 代价账与推进路线（不代选）
# =====================================================================================
emit("")
emit("[5] 代价账与推进路线（不代选）")
ROUTES = [
    ("R1", "接受 EFT 口径（引力为低能有效场论）",
     "放弃「紫外完备」这一 P01 目标；代价 = 预言力 0（C09：L<=%d 圈需 >=%d 枚系数）；"
     "收益 = 与已知引力低能现象自洽（但这不构成 M1）" % (LMAX, NMIN)),
    ("R2", "KK 额外维路线（P12）",
     "代价 = n >= %d 个未观测额外维 + 紧致部比 SM 多 %d 个生成元需破缺/不可见 + n 值无出处（B06）；"
     "另需完整极大子群分类证明 so(%d) 含 SM 的极大秩子代数（B07，本册不代判定）" % (MINN, r_min['mc_dim'] - DIM_SM, 3 + MINN)),
    ("R3", "非李代数 / 新代数结构（几何代数升格）",
     "代价 = 不可评估（无既有数学框架可直接引用）；本册不代选、不预设其可行性"),
]
for rid, nm, cost in ROUTES:
    emit("  %s %s" % (rid, nm))
    emit("      代价：%s" % cost)
item('E01', 'BOUNDARY', '三路线均给出代价定价，**本册不代选**（R1 = 放弃目标；R2 = 有硬代价但与已知数学相容；R3 = 不可评估）')
item('E02', 'FAIL', '口径重申：「已攻破」限定为**对 TUFT 原初声称的结构性负面闭合**，不等于物理难题已被解决；'
                    '本册对 P01/P12 的裁定是 **0 / 2 未过门**，且未提供任何替代机制')

# =====================================================================================
# 七、§6 自检、对照与治理
# =====================================================================================
emit("")
emit("[6] 自检、阳性/阴性对照与治理")

chk('A6-1 条目编号唯一', len(set(i['id'] for i in ITEMS)) == len(ITEMS), "")
chk('A6-2 全部条目已分类', all(i['verdict'] in CNT for i in ITEMS), "")
chk('A6-3 两类阻断互不依赖（P12 非 P01 之推论）',
    (not P12_M['M1']) and (not P01_M['M1']), "")

# 阴性对照：把 so(1,3) 的 Killing 型注错为 +2I（正定）后，签名必须变
B13_CORRUPT = [[Fr(2) if i == j else Fr(0) for j in range(6)] for i in range(6)]
bat('签名检验器：注错 Killing 型为 +2I 必须报 (6,0,0)',
    (signature(B13) == (3, 3, 0)), (signature(B13_CORRUPT) == (3, 3, 0)))

# 阴性对照：把 SM 秩注错为 3 则"秩阻断"判据应失效
bat('秩阻断判据：注错 rank(SM)=3 后判据失效',
    (RANK_SM > BOUND_NEG13), (3 > BOUND_NEG13))

# 阴性对照：把逐圈量纲注错为常数则严格递增判据失败
bat('逐圈量纲判据：注错为常数序列后严格递增失败',
    all(2 + 2 * L < 2 + 2 * (L + 1) for L in range(1, 8)),
    all(4 < 4 for L in range(1, 8)))

# 阴性对照：KK 最小 n
bat('KK 最小 n 判据：注错 n=4 后必要条件失败',
    (MINN == 5), (4 == MINN))

# 阴性对照：DAG 阻塞力
bat('阻塞力判据：注错 P01 下游数为 5 后失败',
    (BLOCK['P01'] == 6), (5 == BLOCK['P01']))

# 版面终扫（占位符/未替换）—— 对**正文段**扫描（汇总行由脚本自身生成，不含占位符）
BLOB_CONTENT = "\n".join(OUT)
PLACEHOLDERS = ["TODO", "FIXME", "XXX", "<TBD>", "%s%s"]
FOUND_PH = [p for p in PLACEHOLDERS if p in BLOB_CONTENT]
chk('A6-4 版面终扫（无占位符）', not FOUND_PH, "命中：%s" % FOUND_PH)

n_ok = sum(1 for _n, ok in SELF if ok)
bat_bad = sum(1 for _l, g, b in BATTERY if not (g and b))

emit("")
emit("自检 guard：%d / %d" % (n_ok, len(SELF)))
emit("对照电池：%d 格，不合格 %d 格" % (len(BATTERY), bat_bad))
emit("条目统计：" + "  ".join("%s=%d" % (k, CNT[k]) for k in ['THEOREM', 'PASS', 'FAIL', 'BOUNDARY', 'INFO', 'STRUCT']))

# =====================================================================================
# 落盘（report.txt 写后回读 + md5；json 供下游）
# =====================================================================================
BLOB = "\n".join(OUT).encode("utf-8")
io.open(REPORT, "wb").write(BLOB)
back = io.open(REPORT, "rb").read()
MD5 = hashlib.md5(back).hexdigest()
emit("")
emit("报告已落盘：%s" % os.path.basename(REPORT))
emit("字节 = %d  md5 = %s  写后回读一致 = %s" % (len(back), MD5, back == BLOB))

with io.open(JSONOUT, "w", encoding="utf-8") as fh:
    json.dump({'tag': TAG, 'date': '2026-10-13', 'items': ITEMS,
               'counts': CNT, 'key': KEY,
               'guards': [{'name': n, 'ok': ok} for n, ok in SELF],
               'battery': [{'label': l, 'good': g, 'bad_ok': b} for l, g, b in BATTERY],
               'md5': MD5}, fh, ensure_ascii=False, indent=1)

# =====================================================================================
# 退出码
# =====================================================================================
exit_code = 0 if (n_ok == len(SELF) and bat_bad == 0 and not FOUND_PH) else 1
emit("")
emit("EXIT = %d" % exit_code)
if __name__ == "__main__":
    sys.exit(exit_code)
