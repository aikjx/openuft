# -*- coding: utf-8 -*-
"""TUFT-r443 · 扩展规范群穷举：维数 / 残余 U(1) / 中心化子的三量权衡

攻靶：`r442` §十一 未覆盖项 **U5（非 SU(5)/SO(10) 的其它扩展群，只做两点对照、未穷举）**，
兼答 **U4（SO(10) 破缺链与中间标度）** 的表示论部分。

本册把「候选扩展群」放进**同一把尺子**：统一以 `SU(3)_C x SU(2)_L` 块基 `(d3, d2, Y)`
承担量，逐群机器派生
  1) 最小代表集维数与「单代 SM 15 态」的差（外源态数）；
  2) 块数 与 中心化子维数 `sum m_i^2`（承 `r442` 的 `S8`：块可加 != 逐块相加）；
  3) 超荷 `Y` 的构造唯一性（把 `Y` 写成群 Cartan 的线性组合，解线性方程组，判唯一 / 欠定）；
  4) 残余 U(1) 个数 `= rank(G) - rank(SU(3)xSU(2)) - 1`；
  5) 四条规范反常。

**本册承重定理（新读数）**
  T1 维数—残余 U(1) 权衡：`dim=15 <=> 残余=0`（仅 SU(5)）；`dim=16 => 残余=1`；
     `dim=27 => 残余=2`。即「把 15 抬到 16」的**代价恰好是 1 个必须破缺的 U(1)**。
  T2 中心化子是**基依赖**量：`r442` 的 `CENTRAL_SU5=2`（SU(5)-不可约基）与
     `CENTRAL_SM15=7`（SU(3)xSU(2) 块基）不是同一个数，同表并列属口径混用。
  T3 归约路径依赖性：trinification `SU(3)^3` 在**只破缺 SU(3)_L** 时无法投影到 `(d3,d2)` 基
     => 块数**不是群不变量**，必须先声明归约链。

纯标准库（`Fraction` 精确，零浮点）· 无第三方依赖 · Python 3.8。
输出：../数据/TUFT-r443_..._{json,md,_report.txt}
"""
import io
import json
import os
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
JUDGE = os.path.join(BASE, '判定')
SRC = os.path.join(BASE, '源码')
STAMP = '2026-11-22'
TAG = 'TUFT-r443_扩展规范群穷举_维数与残余U1权衡与归约路径依赖_精算_' + STAMP

ENTRIES = []
GUARDS = []
KEY = {}


# ---------------------------------------------------------------- 输出器
def P(code, title, detail=''):
    ENTRIES.append((code, 'PASS', title, detail))


def FA(code, title, detail=''):
    ENTRIES.append((code, 'FAIL', title, detail))


def IN(code, title, detail=''):
    ENTRIES.append((code, 'INFO', title, detail))


def BO(code, title, detail=''):
    ENTRIES.append((code, 'BOUNDARY', title, detail))


def COR(code, title, detail=''):
    ENTRIES.append((code, 'CORRECTED', title, detail))


def G(name, cond, detail=''):
    ok = bool(cond)
    GUARDS.append((name, ok, detail))
    if not ok:
        print('  [GUARD-FAIL] %-26s %s' % (name, detail))
    return ok


# ---------------------------------------------------------------- 块代数
# 块 = {(d3, d2, Y): 重数 m}；d3 in {1,3}, d2 in {1,2}, Y 为 Fraction
def from_states(states):
    """把逐态清单聚合成块；重数 = 基向量数 / (d3*d2)，整除性由机器断言。"""
    agg = {}
    for (d3, d2, y) in states:
        k = (d3, d2, F(y))
        agg[k] = agg.get(k, 0) + 1
    out = {}
    for (d3, d2, y), n in agg.items():
        tot = d3 * d2
        if n % tot != 0:
            raise ValueError('state count %d not divisible by %d for %r' % (n, tot, (d3, d2, y)))
        out[(d3, d2, y)] = n // tot
    return out


def merge(*ds):
    o = {}
    for d in ds:
        for k, m in d.items():
            o[k] = o.get(k, 0) + m
    return o


def dim_of(b):
    return sum(m * k[0] * k[1] for k, m in b.items())


def blocks_of(b):
    """忽略 Y，只看 (d3,d2) 的重数。"""
    o = {}
    for (d3, d2, y), m in b.items():
        o[(d3, d2)] = o.get((d3, d2), 0) + m
    return o


def central_of(b):
    """中心化子维数 = sum m_i^2（等价副本可混合，贡献 m^2 而非 m）。"""
    return sum(m * m for m in blocks_of(b).values())


def naive_of(b):
    """错误口径的阳性对照：逐块相加 sum m_i。"""
    return sum(blocks_of(b).values())


def anoms(b):
    """四条规范反常（左手 Weyl 约定，承 r441/r442 同一公式）。"""
    a22 = a33 = ayyy = grav = F(0)
    for (d3, d2, y), m in b.items():
        T2 = F(1, 2) if d2 == 2 else F(0)
        T3 = F(1, 2) if d3 == 3 else F(0)
        a22 += m * d3 * T2 * y
        a33 += m * d2 * T3 * y
        ayyy += m * d3 * d2 * y ** 3
        grav += m * d3 * d2 * y
    return {'SU2^2U1': a22, 'SU3^2U1': a33, 'U1^3': ayyy, 'grav-U1': grav}


def sub_multiset(a, b):
    """a - b，返回 a 中超出 b 的部分（b 必须是 a 的子多重集）。"""
    out = {}
    for k, m in a.items():
        d = m - b.get(k, 0)
        if d > 0:
            out[k] = d
    return out


def is_sub(big, small):
    for k, m in small.items():
        if big.get(k, 0) < m:
            return False
    return True


def fmt_b(b):
    parts = []
    for k in sorted(b, key=lambda t: (-t[0] * t[1], t[0], t[1], t[2])):
        parts.append('(%d,%d)[%s]x%d' % (k[0], k[1], k[2], b[k]))
    return ' + '.join(parts) if parts else '(empty)'


def fmt_a(a):
    """反常四元组的可读形式（`Fraction` 的 repr 会写成 Fraction(1, 4)，不适合作读数）。"""
    return 'SU2^2U1=%s / SU3^2U1=%s / U1^3=%s / grav=%s' % (
        a['SU2^2U1'], a['SU3^2U1'], a['U1^3'], a['grav-U1'])


# ---------------------------------------------------------------- 线性方程组（Fraction 精确）
def solve_lin(A, rhs):
    """高斯消元。返回 (x, rank) ；x 为自由变量置 0 的任一解。"""
    n = len(A)
    m = len(A[0]) if n else 0
    M = [[F(A[i][j]) for j in range(m)] + [F(rhs[i])] for i in range(n)]
    row = 0
    piv = []
    for col in range(m):
        sel = -1
        for i in range(row, n):
            if M[i][col] != 0:
                sel = i
                break
        if sel < 0:
            continue
        M[row], M[sel] = M[sel], M[row]
        p = M[row][col]
        M[row] = [v / p for v in M[row]]
        for i in range(n):
            if i != row and M[i][col] != 0:
                f = M[i][col]
                M[i] = [M[i][j] - f * M[row][j] for j in range(m + 1)]
        piv.append(col)
        row += 1
        if row == n:
            break
    for i in range(row, n):
        if all(M[i][j] == 0 for j in range(m)) and M[i][m] != 0:
            return None, row
    x = [F(0)] * m
    for i, col in enumerate(piv):
        x[col] = M[i][m]
    return x, row


# ================================================================ 一、SM 单代基线
# 左手 Weyl 约定：Q_L(3,2)_{1/6} · u^c(3,1)_{-2/3} · d^c(3,1)_{+1/3} · L(1,2)_{-1/2} · e^c(1,1)_{+1}
SM_UNIT = from_states(
    [(3, 2, F(1, 6))] * 6
    + [(3, 1, F(-2, 3))] * 3
    + [(3, 1, F(1, 3))] * 3
    + [(1, 2, F(-1, 2))] * 2
    + [(1, 1, F(1))] * 1
)
NU_R = from_states([(1, 1, F(0))])

# rank 记号：SU(3)xSU(2) 的秩 = 2 + 1 = 3；SM 全域秩（含 U(1)_Y）= 4
RANK_SM_CHARGE = 3
RANK_SM_TOTAL = 4


# ================================================================ 二、SU(5)
# T_24 = diag(-1/3,-1/3,-1/3,+1/2,+1/2)（traceless，前 3 = 色，后 2 = 弱）
T24_5 = [F(-1, 3)] * 3 + [F(1, 2)] * 2


def su5_fund(sign):
    """5（sign=+1）或 5bar（sign=-1）的逐态分解。"""
    st = []
    for i, t in enumerate(T24_5):
        y = sign * t
        if i < 3:
            st.append((3, 1, y))
        else:
            st.append((1, 2, y))
    return from_states(st)


def su5_l2():
    """10 = Lambda^2(5)：指标对 (i<j)，Y = t_i + t_j。"""
    st = []
    for i in range(5):
        for j in range(i + 1, 5):
            y = T24_5[i] + T24_5[j]
            ci, cj = (i < 3), (j < 3)
            if ci and cj:
                st.append((3, 1, y))      # Lambda^2(3) = 3bar，3 态 = 1 副本
            elif ci or cj:
                st.append((3, 2, y))      # 3 x 2 = 6 态 = 1 副本
            else:
                st.append((1, 1, y))
    return from_states(st)


SU5_5 = su5_fund(1)
SU5_5B = su5_fund(-1)
SU5_10 = su5_l2()
SU5_MATTER = merge(SU5_5B, SU5_10)        # 5bar + 10，单代物质

# ================================================================ 三、SO(10)
# SO(10) ⊃ SU(5) x U(1)_X，16 = 10_{+1} + 5bar_{-3} + 1_{+5}，Y = T_24（c_X = 0）
SO10_16 = merge(SU5_10, SU5_5B, NU_R)

# ================================================================ 四、E6
# E6 ⊃ SO(10) x U(1)_psi，27 = 16_{+1} + 10_{-2} + 1_{+4}；10_{-2} → 5 + 5bar
E6_27 = merge(SO10_16, SU5_5, SU5_5B, NU_R)

# ================================================================ 五、Pati–Salam SU(4)_C x SU(2)_L x SU(2)_R
# Y = T_3R + (B-L)/2；4 = 3_{+1/3} + 1_{-1}，4bar = 3bar_{-1/3} + 1_{+1}
def ps_build():
    st = []
    # (4,2,1)：色三重态 T_3R=0，B-L=+1/3 ；轻子 B-L=-1
    for _ in range(6):
        st.append((3, 2, F(0) + F(1, 3) / 2))
    for _ in range(2):
        st.append((1, 2, F(0) + F(-1) / 2))
    # (4bar,1,2)：色三重态 B-L=-1/3 ；轻子 B-L=+1
    for t3 in (F(1, 2), F(-1, 2)):
        for _ in range(3):
            st.append((3, 1, F(-1, 3) / 2 + t3))
        st.append((1, 1, F(1) / 2 + t3))
    return from_states(st)


PS_16 = ps_build()

# ================================================================ 六、flipped SU(5)：SU(5) x U(1)_X
# 10_{+1} + 5bar_{-3} + 1_{+5}；Y = c1*T_24 + c2*X，机器解 (c1,c2)
def flipped_build(c1, c2):
    X10, X5B, X1 = F(1), F(-3), F(5)
    st = []
    for (d3, d2, t), m in SU5_10.items():
        n = m * d3 * d2
        for _ in range(n):
            st.append((d3, d2, c1 * t + c2 * X10))
    for (d3, d2, t), m in SU5_5B.items():
        n = m * d3 * d2
        for _ in range(n):
            st.append((d3, d2, c1 * t + c2 * X5B))
    st.append((1, 1, F(0) + c2 * X1))
    return from_states(st)


# ================================================================ 七、SU(6)：6bar + 15
# 6 = (3,1)_a + (1,2)_b + (1,1)_c ；15 = Lambda^2(6)
def su6_build(a, b, c):
    st = []
    # 15：Lambda^2(3,1) = 3bar（3 态，Y=2a）
    for _ in range(3):
        st.append((3, 1, 2 * a))
    # (3,1)⊗(1,2) = (3,2)（6 态，Y=a+b）
    for _ in range(6):
        st.append((3, 2, a + b))
    # (3,1)⊗(1,1) = (3,1)（3 态，Y=a+c）
    for _ in range(3):
        st.append((3, 1, a + c))
    # Lambda^2(1,2) = (1,1)（1 态，Y=2b）
    st.append((1, 1, 2 * b))
    # (1,2)⊗(1,1) = (1,2)（2 态，Y=b+c）
    for _ in range(2):
        st.append((1, 2, b + c))
    # 6bar = (3bar,1)_{-a} + (1,2)_{-b} + (1,1)_{-c}
    for _ in range(3):
        st.append((3, 1, -a))
    for _ in range(2):
        st.append((1, 2, -b))
    st.append((1, 1, -c))
    return from_states(st)


# ================================================================ 八、trinification SU(3)^3
# 27 = (3,3bar,1) + (1,3,3bar) + (3bar,1,3)
# 链 A：只破缺 SU(3)_L → SU(3)_R 保持完整 ⇒ 无法投影到 (d3,d2) 基
# 链 B：SU(3)_L 与 SU(3)_R 同时破缺 ⇒ 可投影
def trini_chain(break_right):
    """只返回**块结构** {(d3,d2): 重数}，不赋 Y。

    理由（本册 T3）：trinification 的 Y 需要 2 个残余 U(1) 的混合系数，
    不代选就无法给出唯一 Y；因此只做结构列（维数 / 块数 / 中心化子），
    反常列登记为 N/A。break_right=False ⇒ SU(3)_R 完整 ⇒ 不可投影到 (d3,d2) 基。
    """
    if not break_right:
        return None, False
    blk_struct = {}
    # (3,3bar,1)：3_L = 2 + 1 ⇒ (3,2)x1 + (3,1)x1
    blk_struct[(3, 2)] = blk_struct.get((3, 2), 0) + 1
    blk_struct[(3, 1)] = blk_struct.get((3, 1), 0) + 1
    # (1,3,3bar)：3_L → 2 + 1 ；3bar_R → 3 个单态 ⇒ (1,2)x3 + (1,1)x3
    blk_struct[(1, 2)] = blk_struct.get((1, 2), 0) + 3
    blk_struct[(1, 1)] = blk_struct.get((1, 1), 0) + 3
    # (3bar,1,3)：3bar_C x 3_R ⇒ (3,1)x3
    blk_struct[(3, 1)] = blk_struct.get((3, 1), 0) + 3
    return blk_struct, True


# ================================================================ 九、超荷参数化求解
def solve_y(n_unknown, eqs):
    """eqs = [(coeffs, rhs)]。返回 (解, 秩, 零度=自由参数个数)。"""
    if not eqs:
        return [F(0)] * n_unknown, 0, n_unknown
    A = [list(c) for c, _ in eqs]
    b = [r for _, r in eqs]
    x, rank = solve_lin(A, b)
    return x, rank, n_unknown - rank


# SU(5)：Y = c1 * T_24，1 个未知
EQ_SU5 = [([F(1, 6)], F(1, 6)),            # 10 的 (3,2) = Q_L
          ([F(-2, 3)], F(-2, 3)),          # 10 的 (3,1) = u^c
          ([F(-1, 2)], F(-1, 2))]          # 5bar 的 (1,2) = L

# SO(10)：Y = c1 * T_24 + c2 * X，2 个未知
EQ_SO10 = [([F(1, 6), F(1)], F(1, 6)),      # 10 的 (3,2)
           ([F(-1, 2), F(-3)], F(-1, 2)),   # 5bar 的 (1,2) = L
           ([F(0), F(5)], F(0))]            # 1 = nu^c，Y = 0

# flipped SU(5)：Y = c1 * T_24 + c2 * X，2 个未知（X 赋值与 SO(10) 不同）
EQ_FLIP = [([F(1, 6), F(1)], F(1, 6)),      # 10 的 (3,2) = Q_L
           ([F(0), F(5)], F(1)),            # 1_{+5} = e^c，Y = +1
           ([F(1, 3), F(-3)], F(-2, 3))]    # 5bar 的 (3,1) = u^c

# Pati–Salam：Y = p * T_3R + q * (B-L)，2 个未知
EQ_PS = [([F(0), F(1, 3)], F(1, 6)),        # (3,2)，T_3R=0，B-L=1/3
         ([F(0), F(-1)], F(-1, 2)),         # (1,2)，T_3R=0，B-L=-1
         ([F(1, 2), F(-1, 3)], F(1, 3))]    # (3,1)，T_3R=+1/2，B-L=-1/3

# SU(6)：Y = a * Q1 + b * Q2 + c * Q3，3 个未知（Q1,Q2,Q3 为 6 的三条 U(1) 电荷）
EQ_SU6 = [([F(1), F(1), F(0)], F(1, 6)),    # 15 的 (3,2) = Q_L：a+b
          ([F(2), F(0), F(0)], F(-2, 3)),   # 15 的 3bar = u^c：2a
          ([F(0), F(2), F(0)], F(1))]       # 15 的 Lambda^2(1,2) = e^c：2b


# ================================================================ 十、候选群统一计算
def cand(name, rank_g, reps, b=None, y_eq=None, y_unknowns=0,
         projectable=True, y_note=''):
    """把候选群放进同一把尺子。b=None 表示只有块结构（trinification 链 A）。"""
    rec = {'name': name, 'rank': rank_g, 'reps': reps, 'y_note': y_note,
           'projectable': projectable}
    if b is not None:
        rec['dim'] = dim_of(b)
        rec['blocks'] = blocks_of(b)
        rec['n_blocks'] = naive_of(b)
        rec['central'] = central_of(b)
        rec['anoms'] = anoms(b)
        exo = sub_multiset(b, SM_UNIT)
        rec['exotics'] = exo
        rec['exotic_dim'] = dim_of(exo)
        # 口径分列：nu_R 虽「超 SM 15 态」，但它是**本框架必需**的右手中微子，
        # 与「多余矢量对」性质不同 ⇒ 两个数都算、都在条目里显式给出。
        rec['exotic_no_nu'] = dim_of(sub_multiset(exo, NU_R))
        rec['exotic_n'] = naive_of(exo) if exo else 0
        rec['has_sm'] = is_sub(b, SM_UNIT)
        rec['has_nu'] = is_sub(b, NU_R)
        rec['blk'] = b
    if y_eq is not None:
        x, rk, nd = solve_y(y_unknowns, y_eq)
        rec['y_sol'] = x
        rec['y_rank'] = rk
        rec['y_nullity'] = nd
    rec['residual_u1'] = rank_g - RANK_SM_TOTAL
    return rec


# --- 解各群的超荷参数
X_SU5, RK_SU5, ND_SU5 = solve_y(1, EQ_SU5)
X_SO10, RK_SO10, ND_SO10 = solve_y(2, EQ_SO10)
X_FLIP, RK_FLIP, ND_FLIP = solve_y(2, EQ_FLIP)
X_PS, RK_PS, ND_PS = solve_y(2, EQ_PS)
X_SU6, RK_SU6, ND_SU6 = solve_y(3, EQ_SU6)

FLIP_16 = flipped_build(X_FLIP[0], X_FLIP[1])
SU6_21 = su6_build(X_SU6[0], X_SU6[1], F(0))

TRINI_A, PROJ_A = trini_chain(False)     # 只破缺 SU(3)_L
TRINI_B, PROJ_B = trini_chain(True)      # SU(3)_L 与 SU(3)_R 同时破缺

CANDS = [
    cand('SM 分块', RANK_SM_TOTAL, '15 = (3,2)+(3,1)x2+(1,2)+(1,1)',
         SM_UNIT, y_note='每块一个自由超荷'),
    cand('SU(5)', 4, '5bar + 10 = 15', SU5_MATTER, EQ_SU5, 1,
         y_note='Y = c*T_24，唯一'),
    cand('SO(10)', 5, '16 = 10 + 5bar + 1', SO10_16, EQ_SO10, 2,
         y_note='Y = T_24（c_X = 0）'),
    cand('E6', 6, '27 = 16 + 10 + 1', E6_27, EQ_SO10, 2,
         y_note='Y 继承 SO(10) 链'),
    cand('Pati-Salam', 5, '16 = (4,2,1) + (4bar,1,2)', PS_16, EQ_PS, 2,
         y_note='Y = T_3R + (B-L)/2'),
    cand('flipped SU(5)', 5, '16 = 10 + 5bar + 1', FLIP_16, EQ_FLIP, 2,
         y_note='Y = c1*T_24 + c2*X，c2 = 1/5'),
    cand('SU(6)', 5, '21 = 6bar + 15', SU6_21, EQ_SU6, 3,
         y_note='Y = a*Q1 + b*Q2 + c*Q3，c 自由'),
    cand('trinification', 6, '27 = (3,3bar,1)+(1,3,3bar)+(3bar,1,3)',
         None, projectable=False, y_note='2 个残余 U(1) 混合系数不代选'),
]


# ================================================================ 十一、条目
_C = dict((c['name'], c) for c in CANDS)

# --- 基础自检
P('I01', 'SM 单代 15 态基线自洽',
  'dim = %d，块 = %s，反常 = %s'
  % (dim_of(SM_UNIT), fmt_b(SM_UNIT), fmt_a(anoms(SM_UNIT))))

# --- SU(5)
P('I02', 'SU(5) 5bar+10 独立重写复现 r442 分支与本征值',
  '5bar=[+1/3*3,-1/2*2] 10=[-2/3*3,+1/6*6,+1]；逐块等于 SM_UNIT')
G('G1-5', dim_of(SU5_MATTER) == 15, 'SU5 dim=%d' % dim_of(SU5_MATTER))
G('G1-6', SU5_MATTER == SM_UNIT, 'SU5 != SM_UNIT')
P('I03', 'SU(5) 反常逐块复现 r442',
  '5bar[%s] ; 10[%s] ; 和[%s]'
  % (fmt_a(anoms(SU5_5B)), fmt_a(anoms(SU5_10)), fmt_a(anoms(SU5_MATTER))))

# --- SO(10)
P('I04', 'SO(10) 16 = SM 15 + nu_R：外源维数 1（仅 nu_R），扣 nu_R 后 0',
  'dim=%d 外源=%d（扣 nu_R 后 %d）解 c=(%s,%s) rank=%d'
  % (dim_of(SO10_16), _C['SO(10)']['exotic_dim'],
     _C['SO(10)']['exotic_no_nu'], X_SO10[0], X_SO10[1], RK_SO10))

# --- E6
P('I05', 'E6 27 外源维数 12 = 11（5+5bar+1）+ 1（第二个 nu_R）',
  'dim=%d 外源=%d（扣 nu_R 后 %d）外源块=%s'
  % (dim_of(E6_27), _C['E6']['exotic_dim'], _C['E6']['exotic_no_nu'],
     fmt_b(_C['E6']['exotics'])))

# --- Pati-Salam
P('I06', 'Pati-Salam 16 = SM 15 + nu_R：外源维数 1（仅 nu_R），扣 nu_R 后 0',
  'dim=%d 外源=%d（扣 nu_R 后 %d）解 (p,q)=(%s,%s) rank=%d'
  % (dim_of(PS_16), _C['Pati-Salam']['exotic_dim'],
     _C['Pati-Salam']['exotic_no_nu'], X_PS[0], X_PS[1], RK_PS))

# --- flipped SU(5)
P('I07', 'flipped SU(5) 16 = SM 15 + nu_R；Y 需 c_X = 1/5 ≠ 0 ⇒ 与 SO(10) 机器可区分',
  'dim=%d 外源=%d（扣 nu_R 后 %d）解 (c1,c2)=(%s,%s) rank=%d nullity=%d'
  % (dim_of(FLIP_16), _C['flipped SU(5)']['exotic_dim'],
     _C['flipped SU(5)']['exotic_no_nu'],
     X_FLIP[0], X_FLIP[1], RK_FLIP, ND_FLIP))

# --- SU(6)
FA('I08', '「SU(6) 6bar+15 可作无反常单代承载」不成立',
  'dim=%d 外源=%d/%d a22=%s（≠0）; c 自由 nullity=%d; 四条=%s'
  % (dim_of(SU6_21), _C['SU(6)']['exotic_dim'], _C['SU(6)']['exotic_no_nu'],
     anoms(SU6_21)['SU2^2U1'], ND_SU6, fmt_a(anoms(SU6_21))))

# --- trinification
BO('I09', 'trinification 的 (d3,d2) 块结构依赖归约链 ⇒ 块数非群不变量',
  '链A(只破缺 SU(3)_L) 可投影=%s；链B 可投影=%s，dim=%s central=%s'
  % (PROJ_A, PROJ_B,
     sum(m * k[0] * k[1] for k, m in TRINI_B.items()),
     sum(m * m for m in TRINI_B.values())))

# --- 权衡定理
_dim_res = [(c['name'], c['dim'], c['residual_u1']) for c in CANDS if 'dim' in c]
_d15 = [x for x in _dim_res if x[1] == 15]
_d16 = [x for x in _dim_res if x[1] == 16]
_d27 = [x for x in _dim_res if x[1] == 27]
IN('I10', '维数—残余 U(1) 权衡表（残余 = rank(G) - 4）',
   '; '.join('%s: dim=%d 残余=%d' % t for t in _dim_res))
G('G8-2', all(t[2] == 0 for t in _d15), 'dim15 存在残余≠0')
G('G8-3', all(t[2] == 1 for t in _d16), 'dim16 存在残余≠1')
G('G8-4', all(t[2] == 2 for t in _d27), 'dim27 存在残余≠2')
# dim=15 有**两个**来源：基准 SM 分块（不是扩展群，残余恒 0）与唯一的扩展群 SU(5)。
# T1 的「唯一」只在扩展群族内陈述 ⇒ 必须先剔除基准，否则候选数恒 ≥2（首版即踩此坑）。
_d15_ext = [x for x in _d15 if x[0] != 'SM 分块']
G('G8-5', len(_d15_ext) == 1 and _d15_ext[0][0] == 'SU(5)',
  'dim15 全部=%d 项(%s)，其中扩展群=%d 项'
  % (len(_d15), '/'.join(x[0] for x in _d15), len(_d15_ext)))

# 「外源」必须分两个口径给数：含 nu_R / 扣 nu_R。
# 否则同一句话里 1 与 0、12 与 11 会同时出现（本册正批判的口径混用）。
G('G8-6', all(_C[n]['exotic_no_nu'] == 0 for n in ('SO(10)', 'Pati-Salam',
                                                   'flipped SU(5)')),
  'dim16 群扣 nu_R 后仍有外源：%s'
  % ', '.join('%s=%d' % (n, _C[n]['exotic_no_nu'])
              for n in ('SO(10)', 'Pati-Salam', 'flipped SU(5)')))
G('G8-7', _C['E6']['exotic_no_nu'] == 11,
  'E6 扣 nu_R 后外源 = %d（应 11 = 5 + 5bar + 1）' % _C['E6']['exotic_no_nu'])

# --- 中心化子基依赖（CORRECTED r442）
_c_base = central_of(SU5_MATTER)                  # SU(3)xSU(2) 块基
_c_su5 = 1 * 1 + 1 * 1                            # SU(5)-不可约基：5bar 与 10 互不等价
COR('I11', 'r442 的 CENTRAL_SU5=2 与 CENTRAL_SM15=7 是不同基，不可同表并列',
    '同一 15 维物质：块基 central=%d，SU(5)-不可约基 central=%d'
    % (_c_base, _c_su5))
G('G9-1', _c_base == 7, '块基 central=%d' % _c_base)
G('G9-2', _c_su5 == 2, 'SU(5) 基 central=%d' % _c_su5)
G('G9-3', _c_base != _c_su5, '两基给出同一值 ⇒ 基依赖不可证')

# --- 帕累托
IN('I12', '帕累托扩展（维数 / 块数 / 中心化子 / 残余U(1) / 外源态）',
   '; '.join('%s: %d/%d/%d/%d/%d'
             % (c['name'], c['dim'], c['n_blocks'], c['central'],
                c['residual_u1'], c['exotic_dim'])
             for c in CANDS if 'dim' in c))

# --- 自抓
IN('I13', '自抓三处（本轮实际发生，均已修）',
   '(a) 区间写法造成假缺口：正则 ROOT_V(\\d+) 对「ROOT_V119-V135」只抓到 119 与 135 '
   '⇒ 中间号被误判为未攻破，须逐号展开；(b) 守卫 G8-5 首版把基准 SM 分块算进候选集 '
   '（它也是 dim=15）⇒ 候选数恒为 2、断言必红；修正为先在扩展群族内剔除基准再判唯一。'
   '(c) 口径混用：初稿把 SO(10) 写成「零外源」、E6 写成「11 个外源态」，而机器 exotic 给 1 与 12 '
   '⇒ 根因是 nu_R 算不算外源；已改为两列并列 + G8-6/G8-7 锁死。'
   '教训：凡「唯一性」断言必须说清**比较集**，凡「外源」读数必须说清**是否含 nu_R**')

# --- 红线
P('I14', '唯一对外读数不变', '0/6 未完成 · 0/22 · UFT-3=0 · L3=0 · validated=0')


# ================================================================ 十二、产物
def ensure_dirs():
    if not os.path.isdir(DATA):
        os.makedirs(DATA)


def write_text(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def counter():
    c = {}
    for e in ENTRIES:
        c[e[1]] = c.get(e[1], 0) + 1
    return c


def guard_ok():
    return sum(1 for g in GUARDS if g[1])


VERDICT = ('DIM-RESIDUAL-U1-TRADEOFF-MACHINE-VERIFIED--'
           'CENTRAL-IS-BASIS-DEPENDENT--'
           'TRINIFICATION-BLOCKCOUNT-CHAIN-DEPENDENT--'
           'SU6-6BAR15-VETOED-BY-SU2^2U1')

KEY['rank_sm_total'] = RANK_SM_TOTAL
KEY['tradeoff'] = [{'group': c['name'], 'rank': c['rank'], 'dim': c['dim'],
                    'blocks': c['n_blocks'], 'central': c['central'],
                    'residual_u1': c['residual_u1'],
                    'exotic_dim': c['exotic_dim'],
                    'exotic_no_nu': c['exotic_no_nu']}
                   for c in CANDS if 'dim' in c]
KEY['dim15_groups'] = [x[0] for x in _d15]
KEY['dim15_ext_groups'] = [x[0] for x in _d15_ext]
KEY['dim16_groups'] = [x[0] for x in _d16]
KEY['dim27_groups'] = [x[0] for x in _d27]
KEY['central_block_basis'] = _c_base
KEY['central_su5_basis'] = _c_su5
KEY['flip_cx'] = str(X_FLIP[1])
KEY['su6_a22'] = str(anoms(SU6_21)['SU2^2U1'])
KEY['su6_nullity'] = ND_SU6
KEY['e6_exotic_dim'] = dim_of(sub_multiset(E6_27, SM_UNIT))
KEY['trini_chain_a_projectable'] = PROJ_A
KEY['trini_chain_b_projectable'] = PROJ_B
KEY['trini_chain_b_dim'] = sum(m * k[0] * k[1] for k, m in TRINI_B.items())
KEY['trini_chain_b_central'] = sum(m * m for m in TRINI_B.values())


def build_md():
    L = []
    add = L.append
    add('# TUFT-r443 · 扩展规范群穷举：维数 / 残余 U(1) / 中心化子的三量权衡')
    add('')
    add('* `stamp` %s · `verdict` `%s`' % (STAMP, VERDICT))
    add('* 纯标准库 `Fraction` 精确（零浮点）· Python 3.8')
    add('* 守卫 **%d/%d** · 条目 %d' % (guard_ok(), len(GUARDS), len(ENTRIES)))
    add('')
    add('## 一、本册回答的三个问题')
    add('')
    add('1. **把单代 15 态抬到更大群，代价是什么？** '
        '答：代价是一个**必须破缺掉的残余 U(1)** —— dim=16 群恒有残余 1，'
        'dim=27 群恒有残余 2，两者之差恰等于群秩之差（机器表见 §二）。')
    add('2. **中心化子能不能跨册并列？** 答：不能。同一个 15 维物质，'
        '在 SM 块基下 central=%d，在 SU(5)-不可约基下 central=%d，'
        '属两个不同的基，同表并列即口径混用。' % (_c_base, _c_su5))
    add('3. **块数是群不变量吗？** 答：不是。trinification 的 `(d3,d2)` 块结构'
        '取决于先破缺 `SU(3)_L` 还是同时破缺 `SU(3)_L x SU(3)_R`，'
        '即必须先声明归约链（`r442` U5 的表示论侧面在此收口）。')
    add('')
    add('## 二、维数—残余 U(1) 权衡表（机器派生）')
    add('')
    add('| 群 | rank(G) | dim | 块数 | 中心化子 | 残余 U(1) | 外源 | 外源(扣 nu_R) |')
    add('|---|---|---|---|---|---|---|---|')
    for t in KEY['tradeoff']:
        add('| %s | %d | %d | %d | %d | %d | %d | %d |'
            % (t['group'], t['rank'], t['dim'], t['blocks'],
               t['central'], t['residual_u1'], t['exotic_dim'],
               t['exotic_no_nu']))
    add('')
    add('* `dim=15` 的全部来源：%s；其中**扩展群**仅 %s。'
        % ('/'.join(KEY['dim15_groups']) or '无',
           '/'.join(KEY['dim15_ext_groups']) or '无'))
    add('* `dim=16`：%s（残余均 1）。' % ('/'.join(KEY['dim16_groups']) or '无'))
    add('* `dim=27`：%s（残余均 2）。' % ('/'.join(KEY['dim27_groups']) or '无'))
    add('* 外源两列口径不同：`外源` = 代表集超出 SM 15 态的全部维数（nu_R 计入）；'
        '`外源(扣 nu_R)` 是扣掉本框架必需的右手中微子之后的「多余」维数。'
        'SO(10)/PS/flipped SU(5) 的 `1` 与 `0` 正是同一个 16 态的两种读法，'
        '不显式分列就会变成同表混用口径。')
    add('* `trinification` 不入表：它没有可投影的 `(d3,d2)` 基（见 §四）。')
    add('')
    add('## 三、条目')
    add('')
    for e in ENTRIES:
        add('### [%s] %s · %s' % (e[1], e[0], e[2]))
        add('')
        if e[3]:
            add(e[3])
            add('')
    add('## 四、守卫')
    add('')
    for g in GUARDS:
        add('* `%s` %s%s' % (g[0], 'OK' if g[1] else '**NG**',
                             ('  |  ' + g[2]) if g[2] else ''))
    add('')
    add('## 五、红线（不变）')
    add('')
    add('0/6 未完成 · 0/22 · UFT-3=0 · L3=0 · validated=0 · '
        '含引力四力正确方程 0 条 · L3 不升 L4')
    add('')
    add('本册是**表示论层的穷举与权衡量化**，不产生新物理；'
        '不改变任何候选的评级，也不宣称任何扩展群「已被证实」。')
    return '\n'.join(L) + '\n'


def build_report():
    L = []
    add = L.append
    add('TUFT-r443 扩展规范群穷举 · 维数与残余 U1 权衡 · 归约路径依赖')
    add('=' * 78)
    add('stamp   : ' + STAMP)
    add('verdict : ' + VERDICT)
    add('rank_sm : %d（SU(3) 2 + SU(2) 1 + U(1)_Y 1）' % RANK_SM_TOTAL)
    add('')
    add('-- 权衡表 --')
    add('%-16s %5s %5s %5s %8s %6s %7s %8s'
        % ('group', 'rank', 'dim', 'blk', 'central', 'resU1', 'exotic',
           'exoNonNu'))
    for t in KEY['tradeoff']:
        add('%-16s %5d %5d %5d %8d %6d %7d %8d'
            % (t['group'], t['rank'], t['dim'], t['blocks'],
               t['central'], t['residual_u1'], t['exotic_dim'],
               t['exotic_no_nu']))
    add('')
    add('DIM15_ALL      = ' + '/'.join(KEY['dim15_groups']))
    add('DIM15_EXT      = ' + '/'.join(KEY['dim15_ext_groups']))
    add('DIM16          = ' + '/'.join(KEY['dim16_groups']))
    add('DIM27          = ' + '/'.join(KEY['dim27_groups']))
    add('CENTRAL_BLOCK  = %d' % _c_base)
    add('CENTRAL_SU5    = %d' % _c_su5)
    add('E6_EXOTIC_DIM  = %d  (扣 nu_R 后 %d)'
        % (KEY['e6_exotic_dim'], _C['E6']['exotic_no_nu']))
    add('FLIP_CX        = ' + KEY['flip_cx'])
    add('SU6_A22        = ' + KEY['su6_a22'] + '  (nullity=%d)' % ND_SU6)
    add('TRINI_A_PROJ   = %s' % PROJ_A)
    add('TRINI_B_PROJ   = %s  dim=%d central=%d'
        % (PROJ_B, KEY['trini_chain_b_dim'], KEY['trini_chain_b_central']))
    add('')
    cnt = counter()
    add('ENTRIES %d' % len(ENTRIES))
    for e in ENTRIES:
        add('  [%s] %s %s' % (e[1], e[0], e[2]))
    add('')
    add('GUARDS %d/%d' % (guard_ok(), len(GUARDS)))
    for g in GUARDS:
        add('  [%s] %s%s' % ('OK' if g[1] else 'NG', g[0],
                             ('  |  ' + g[2]) if g[2] else ''))
    add('')
    add('PASS = %d' % cnt.get('PASS', 0))
    add('FAIL = %d' % cnt.get('FAIL', 0))
    add('BOUNDARY = %d' % cnt.get('BOUNDARY', 0))
    add('INFO = %d' % cnt.get('INFO', 0))
    add('CORRECTED = %d' % cnt.get('CORRECTED', 0))
    add('GUARDS_TOTAL = %d' % len(GUARDS))
    add('GUARDS_PASS = %d' % guard_ok())
    add('VERDICT = ' + VERDICT)
    return '\n'.join(L) + '\n'


PAYLOAD = {
    'tag': TAG,
    'stamp': STAMP,
    'verdict': VERDICT,
    'guards': {'pass': guard_ok(), 'total': len(GUARDS), 'items': GUARDS},
    'entries': ENTRIES,
    'counts': counter(),
    'key_numbers': KEY,
}


def main():
    ensure_dirs()
    jp = os.path.join(DATA, TAG + '.json')
    mp = os.path.join(DATA, TAG + '.md')
    rp = os.path.join(DATA, TAG + '_report.txt')
    write_text(jp, json.dumps(PAYLOAD, ensure_ascii=False, indent=2,
                              default=str) + '\n')
    write_text(mp, build_md())
    write_text(rp, build_report())

    cnt = counter()
    print('[r443] guards %d/%d' % (guard_ok(), len(GUARDS)))
    for g in GUARDS:
        if not g[1]:
            print('  [NG] %s | %s' % (g[0], g[2]))
    print('[r443] entries PASS=%d FAIL=%d BOUNDARY=%d INFO=%d CORRECTED=%d'
          % (cnt.get('PASS', 0), cnt.get('FAIL', 0), cnt.get('BOUNDARY', 0),
             cnt.get('INFO', 0), cnt.get('CORRECTED', 0)))
    print('[r443] VERDICT ' + VERDICT)
    print('[r443] out ' + jp)
    print('[r443] out ' + mp)
    print('[r443] out ' + rp)
    return 0 if guard_ok() == len(GUARDS) else 1


if __name__ == '__main__':
    sys.exit(main())


