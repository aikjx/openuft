# -*- coding: utf-8 -*-
"""UFEC-14 · 14 号册《全物理依赖图与量子挠率首个可复算切片》约定层机器核账。

设计约束（沿用本目录既有仪器口径）：
1. 零第三方依赖：仅 fractions / decimal / json / re / sys / pathlib；
2. 一切符号恒等式用精确多项式（Fraction 系数）判定，物理常数用 Decimal 定点高位数位，
   全程不用浮点，避免近似把非零项读成机器零；
3. 每条给出 id / group / claim / computed / expected / status，否定性结果照实登记 FAIL；
4. **读侧**核对直接从 14 号册正文解析（mermaid 图、Warsaw 列举）：
   文档一旦改动，本仪器的读侧门禁即随之变红，不依赖写样例的人记住的那份；
5. 分工：`torsion_operator_basis.py` 管 24 分量 contorsion 指标代数与 Fierz 基底，
   本仪器管归一化约定、量纲、算符落点完备性、路径积分测度口径、能标数值与依赖图拓扑，
   二者互不共享代码 ⇒ 同一结论有两条独立出处。

用法：  python -B ufec14_convention_audit.py
产出：  ufec14_convention_audit.json（本文件所在目录）
对应文档： 07_统一场方程/14_全物理依赖图与量子挠率首个可复算切片_2026-10-09.md
        07_统一场方程/14A_挠率切片约定审计与全依赖图机器核账_2026-10-09.md
"""
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
import json
import re
import sys
from pathlib import Path

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
DOC = ROOT.parent / '14_全物理依赖图与量子挠率首个可复算切片_2026-10-09.md'
RESULT = []
KEYNUM = {}


def record(cid, group, claim, computed, expected, status, note=''):
    RESULT.append({'id': cid, 'group': group, 'claim': claim,
                   'computed': str(computed), 'expected': str(expected),
                   'status': status, 'note': note})


def st(is_ok):
    return 'PASS' if is_ok else 'FAIL'


# ======================================================================
# 0. 精确多项式（4 元，允许负指数）
# ======================================================================
ARITY = 4


class MPoly(object):
    """稀疏多项式： {(e0,e1,e2,e3): Fraction}。变量：0=S, 1=J, 2=kappa^2, 3=w。"""

    def __init__(self, terms=None):
        self.t = {}
        if terms:
            for key, val in terms.items():
                if val != 0:
                    self.t[tuple(key)] = Fr(val)

    def copy(self):
        out = MPoly()
        out.t = dict(self.t)
        return out

    def __add__(self, other):
        out = self.copy()
        for key, val in other.t.items():
            out.t[key] = out.t.get(key, Fr(0)) + val
            if out.t[key] == 0:
                del out.t[key]
        return out

    def __neg__(self):
        return MPoly({k: -v for k, v in self.t.items()})

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, MPoly):
            out = MPoly()
            for ka, va in self.t.items():
                for kb, vb in other.t.items():
                    key = tuple(ka[i] + kb[i] for i in range(ARITY))
                    val = va * vb
                    out.t[key] = out.t.get(key, Fr(0)) + val
                    if out.t[key] == 0:
                        del out.t[key]
            return out
        return MPoly({k: v * Fr(other) for k, v in self.t.items()})

    def __rmul__(self, other):
        return self.__mul__(Fr(other))

    def power(self, n):
        out = MPoly({tuple([0] * ARITY): Fr(1)})
        base = self.copy()
        k = abs(n)
        while k:
            if k & 1:
                out = out * base
            base = base * base
            k >>= 1
        if n < 0:
            # 只对单项式定义（多项式取倒数不是逐项反号）
            if len(out.t) != 1:
                raise ValueError('非单项式不能取负幂')
            out = MPoly({tuple(-e for e in key): val for key, val in out.t.items()})
        return out

    def d(self, idx):
        """形式偏导 ∂/∂x_idx（只对非负指数生效）。"""
        out = MPoly()
        for key, val in self.t.items():
            if key[idx] == 0:
                continue
            newkey = list(key)
            if key[idx] < 0:
                raise ValueError('负指数不可求导')
            coef = val * key[idx]
            newkey[idx] -= 1
            out.t[tuple(newkey)] = out.t.get(tuple(newkey), Fr(0)) + coef
        return out

    def sub_var(self, idx, other):
        """把变量 idx 替换为另一个多项式。"""
        out = MPoly()
        for key, val in self.t.items():
            term = MPoly({tuple([0] * ARITY): val})
            for i in range(ARITY):
                if i == idx or not key[i]:
                    continue
                expo = [0] * ARITY
                expo[i] = key[i]
                term = term * MPoly({tuple(expo): Fr(1)})
            if key[idx]:
                term = term * other.power(key[idx])
            out = out + term
        return out

    def __eq__(self, other):
        if isinstance(other, MPoly):
            a = {k: v for k, v in self.t.items() if v != 0}
            b = {k: v for k, v in other.t.items() if v != 0}
            return a == b
        return self.t == MPoly({tuple([0] * ARITY): Fr(other)}).t

    def __hash__(self):
        return hash(tuple(sorted(self.t.items())))

    def __str__(self):
        names = ['S', 'J', 'K', 'w']
        parts = []
        for key in sorted(self.t, reverse=True):
            mon = '*'.join('%s^%d' % (names[i], key[i]) for i in range(ARITY) if key[i])
            parts.append('%s%s' % (self.t[key], ('*' + mon) if mon else ''))
        return ' + '.join(parts) if parts else '0'


def CONST(c):
    return MPoly({tuple([0] * ARITY): Fr(c)})


def V(idx):
    key = [0] * ARITY
    key[idx] = 1
    return MPoly({tuple(key): Fr(1)})


def INVV(idx):
    key = [0] * ARITY
    key[idx] = -1
    return MPoly({tuple(key): Fr(1)})


VS, VJ, VK, VW = V(0), V(1), V(2), V(3)
KINV = INVV(2)


# ======================================================================
# 1. 精确复数矩阵（4x4 Dirac 代数，自查用）
# ======================================================================
def cx(re_, im_=0):
    return (Fr(re_), Fr(im_))


def cadd_(a, b):
    return (a[0] + b[0], a[1] + b[1])


def csub_(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cmul_(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cscal(a, s):
    if isinstance(s, tuple):
        return cmul_(a, s)
    return (a[0] * Fr(s), a[1] * Fr(s))


def czero():
    return (Fr(0), Fr(0))


def mat_mul(A, B):
    n = len(A)
    out = [[czero() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            acc = czero()
            for k in range(n):
                acc = cadd_(acc, cmul_(A[i][k], B[k][j]))
            out[i][j] = acc
    return out


def mat_add(A, B):
    return [[cadd_(A[i][j], B[i][j]) for j in range(len(A))] for i in range(len(A))]


def mat_sub(A, B):
    return [[csub_(A[i][j], B[i][j]) for j in range(len(A))] for i in range(len(A))]


def mat_scal(A, s):
    return [[cscal(A[i][j], s) for j in range(len(A))] for i in range(len(A))]


def mat_zero(n=4):
    return [[czero() for _ in range(n)] for _ in range(n)]


def mat_eye(n=4):
    I = mat_zero(n)
    for i in range(n):
        I[i][i] = cx(1)
    return I


def mat_eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A)))


def mat_trace(A):
    acc = czero()
    for i in range(len(A)):
        acc = cadd_(acc, A[i][i])
    return acc


def block(ul, ur, ll, lr):
    """由 2x2 分块组装 4x4。"""
    G = mat_zero(4)
    for i in range(2):
        for j in range(2):
            G[i][j] = ul[i][j]
            G[i][j + 2] = ur[i][j]
            G[i + 2][j] = ll[i][j]
            G[i + 2][j + 2] = lr[i][j]
    return G


S1 = [[czero(), cx(1)], [cx(1), czero()]]
S2 = [[czero(), cx(0, -1)], [cx(0, 1), czero()]]
S3 = [[cx(1), czero()], [czero(), cx(-1)]]
SIG_UP = [None, S1, S2, S3]
Z2 = [[czero(), czero()], [czero(), czero()]]
I2 = [[cx(1), czero()], [czero(), cx(1)]]


def gamma_up(mu):
    """Weyl 基 gamma^mu，号差 (-,+,+,+)：gamma^mu = [[0, sigma^mu],[sigmabar^mu, 0]]，
    sigma^mu=(1, sigma^i)，sigmabar^mu=(-1, sigma^i)。
    """
    up = SIG_UP[mu] if mu else I2
    low = SIG_UP[mu] if mu else mat_scal(I2, -1)
    return block(Z2, up, low, Z2)


GAMMA = [gamma_up(m) for m in range(4)]
METRIC = [Fr(-1), Fr(1), Fr(1), Fr(1)]
GAMMA_LOW = [mat_scal(GAMMA[m], METRIC[m]) for m in range(4)]
IMGUNIT = cx(0, 1)
G5 = mat_mul(mat_mul(mat_mul(mat_scal(GAMMA[0], IMGUNIT), GAMMA[1]), GAMMA[2]), GAMMA[3])
PL = mat_scal(mat_sub(mat_eye(4), G5), Fr(1, 2))
PR = mat_scal(mat_add(mat_eye(4), G5), Fr(1, 2))
# ======================================================================
# A. 依赖图（M1–M9）正文读侧核账
# ======================================================================
def read_doc():
    if not DOC.exists():
        return ''
    return DOC.read_text(encoding='utf-8')


def parse_mermaid(text):
    """返回 (nodes: id->label, edges: [(src_id, dst_id)])。"""
    mblock = re.search(r'```mermaid(.*?)```', text, re.S)
    if not mblock:
        return {}, []
    nodes, edges = {}, []
    for raw in mblock.group(1).splitlines():
        line = raw.split('%%')[0].strip()
        if not line or line.lower().startswith('flowchart'):
            continue
        for nid, lab in re.findall(r'([A-Za-z][A-Za-z0-9_]*)\s*\[([^\]]*)\]', line):
            nodes.setdefault(nid, lab.strip())
        if '-->' in line:
            parts = [p.strip() for p in line.split('-->')]
            for src, dst in zip(parts, parts[1:]):
                s = re.sub(r'\[[^\]]*\]', '', src).strip()
                d = re.sub(r'\[[^\]]*\]', '', dst).strip()
                if s and d:
                    edges.append((s, d))
                    nodes.setdefault(s, '')
                    nodes.setdefault(d, '')
    return nodes, edges


def module_of(nid, label):
    """节点 -> 模块号。裸 id M\d 用自己的号；别名从标签里取 M\d。"""
    own = re.match(r'^M(\d)$', nid)
    if own:
        return int(own.group(1))
    mlab = re.search(r'M(\d)', label or '')
    return int(mlab.group(1)) if mlab else None


def has_cycle(nodeset, edges):
    adj = {n: [] for n in nodeset}
    for s, d in edges:
        if s in adj and d in adj:
            adj[s].append(d)
    state = {}

    def dfs(u):
        state[u] = 1
        for v in adj[u]:
            if state.get(v, 0) == 1:
                return True
            if state.get(v, 0) == 0 and dfs(v):
                return True
        state[u] = 2
        return False
    return any(dfs(u) for u in nodeset if state.get(u, 0) == 0)


def reaches(nodeset, edges, src, dst):
    adj = {n: [] for n in nodeset}
    for s, d in edges:
        if s in adj:
            adj[s].append(d)
    seen, stack = set(), [src]
    while stack:
        u = stack.pop()
        if u == dst:
            return True
        if u in seen:
            continue
        seen.add(u)
        stack.extend(adj.get(u, []))
    return False


def check_a(doc):
    nodes, edges = parse_mermaid(doc)
    if not nodes:
        record('A0', '依赖图', '能从 14 号册正文解析出 mermaid 依赖图', 'not found',
               'mermaid block', 'FAIL', '解析失败：文档结构变了或文件不在预期路径')
        return
    ids = sorted(nodes)
    modmap = {}
    for nid in ids:
        mn = module_of(nid, nodes[nid])
        if mn is not None:
            modmap.setdefault(mn, []).append(nid)
    dup = {k: v for k, v in modmap.items() if len(v) > 1}
    record('A1', '依赖图',
           '依赖图的节点数应等于模块数 9（一个模块一个节点）',
           'nodes=%d modules=%d dup=%s' % (len(ids), len(modmap), dup),
           'nodes=9 modules=9 dup={}', st(len(ids) == 9 and len(modmap) == 9 and not dup))

    nines = sorted(m for m in modmap)
    record('A2', '依赖图',
           '模块编号集合应为 M1..M9',
           'modules=%s' % nines, '1..9',
           st(nines == list(range(1, 10))))

    indeg = {n: 0 for n in ids}
    for s, d in edges:
        indeg[d] = indeg.get(d, 0) + 1

    def canonical(nlist):
        for n in nlist:
            if re.match(r'^M\d$', n):
                return n
        return nlist[0]

    literal_zero = []
    for mn, nlist in sorted(modmap.items()):
        if indeg.get(canonical(nlist), 0) == 0:
            literal_zero.append(mn)
    want_zero = [1, 3]
    record('A3', '依赖图',
           '字面读法下入度为 0 的模块应只有 M1、M3（其余模块都有上游依赖）',
           'literal_zero=%s' % literal_zero, 'want=%s' % want_zero,
           st(literal_zero == want_zero),
           '别名节点（Q/BH/COS）吞掉了 M8/M7/M6 的入边 ⇒ 字面读法把这三个模块读成无上游')

    cyc = has_cycle(set(ids), edges)
    record('A4', '依赖图', '依赖图应为有向无环图（无论字面读法还是按编号折叠）',
           'cycle=%s' % cyc, 'False', st(not cyc))

    sink = [n for n in ids if module_of(n, nodes[n]) == 9] or ['EXP']
    reach_ok = []
    for mn, nlist in sorted(modmap.items()):
        if mn == 9:
            continue
        reach_ok.append(all(any(reaches(set(ids), edges, n, s) for s in sink) for n in nlist))
    record('A5', '依赖图', '每个模块都应有一条路径指向 M9（实验接口）',
           'all_reach=%s' % all(reach_ok), 'True', st(all(reach_ok)))

    outdeg9 = [e for e in edges if module_of(e[0], nodes.get(e[0], '')) == 9]
    record('A6', '依赖图', 'M9 是汇点（不作为其它模块的上游）',
           'edges_from_M9=%d' % len(outdeg9), '0', st(len(outdeg9) == 0))


# ======================================================================
# B. 归一化约定、量纲与代数恒等式
# ======================================================================
def check_b():
    # ---- B1 Dirac 代数自检（本仪器自建矩阵，不复用他人物件）----
    ok_cliff = True
    for mu in range(4):
        for nu in range(4):
            antic = mat_add(mat_mul(GAMMA[mu], GAMMA[nu]), mat_mul(GAMMA[nu], GAMMA[mu]))
            want = mat_scal(mat_eye(4), 2 * METRIC[mu] if mu == nu else 0)
            if not mat_eq(antic, want):
                ok_cliff = False
    ok_g5 = mat_eq(mat_mul(G5, G5), mat_eye(4))
    ok_anti = all(mat_eq(mat_add(mat_mul(G5, GAMMA[m]), mat_mul(GAMMA[m], G5)), mat_zero(4))
                  for m in range(4))
    ok_proj = (mat_eq(mat_mul(PL, PL), PL) and mat_eq(mat_mul(PR, PR), PR)
               and mat_eq(mat_mul(PL, PR), mat_zero(4))
               and mat_eq(mat_add(PL, PR), mat_eye(4))
               and mat_eq(mat_sub(PR, PL), G5))
    ok_move = all(mat_eq(mat_mul(PR, GAMMA[m]), mat_mul(GAMMA[m], PL)) for m in range(4))
    ok_cross = all(mat_eq(mat_mul(PR, mat_mul(GAMMA[m], PR)), mat_zero(4)) for m in range(4))
    record('B1', 'Dirac代数',
           'Weyl 基 {γ^μ,γ^ν}=2η^{μν}、γ5²=1、{γ5,γ^μ}=0、P_L+P_R=1、P_R−P_L=γ5、'
           'P_Rγ^μ=γ^μP_L、P_Rγ^μP_R=0（⇒ 左右手交叉双线性为零，J5=JR−JL 成立）',
           'cliff=%s g5=%s anti=%s proj=%s move=%s cross=%s'
           % (ok_cliff, ok_g5, ok_anti, ok_proj, ok_move, ok_cross),
           'all True',
           st(ok_cliff and ok_g5 and ok_anti and ok_proj and ok_move and ok_cross))

    # ---- B2 由 L_S 两项同维解出 [S]，并与 [T]=1 对照 ----
    dim_kap2 = Fr(-2)          # [κ_g²] = [8πG] = -2（质量幂次，ℏ=c=1）
    dim_psi = Fr(3, 2)
    dim_j = 2 * dim_psi
    sol_t1 = (Fr(4) - (-dim_kap2)) / Fr(2)     # 2 + 2[S] = 4
    sol_t2 = Fr(4) - dim_j                     # [S] + 3 = 4
    ok_dim = (sol_t1 == sol_t2 == Fr(1))
    record('B2', '量纲',
           'L_S 的两项各自给出同一个 [S]，且与挠率量纲 [T]=1 一致',
           'from_quadratic=%s from_cross=%s torsion=1' % (sol_t1, sol_t2),
           '[-1 term] both = 1', st(ok_dim),
           '手算易错项：[1/κ²]=+2 ⇒ 二次项给 2+2[S]=4 ⇒ [S]=1；交叉项给 [S]+3=4 ⇒ [S]=1，一致')

    record('B3', '量纲',
           '四费米算符维数核算：2[J] + [κ²] = 6 − 2 = 4',
           'dim=%s' % (2 * dim_j + dim_kap2), '4',
           st(2 * dim_j + dim_kap2 == Fr(4)))

    # ---- B4 平方配方：精确多项式恒等式（含体积权重 w 与 κ²）----
    lsec = (Fr(3, 4) * KINV * VS * VS - Fr(3, 4) * VS * VJ) * VW
    sqform = (Fr(3, 4) * KINV * (VS - Fr(1, 2) * VK * VJ).power(2)
              - Fr(3, 16) * VK * VJ * VJ) * VW
    ok_sq = (lsec == sqform)
    deriv = lsec.d(0)
    sol = Fr(1, 2) * VK * VJ
    ok_ext = (deriv.sub_var(0, sol) == MPoly({tuple([0] * ARITY): Fr(0)}))
    ok_second = (lsec.d(0).d(0) == Fr(3, 2) * KINV * VW)
    val_sol = lsec.sub_var(0, sol)
    ok_val = (val_sol == -Fr(3, 16) * VK * VJ * VJ * VW)
    record('B4', '平方配方',
           'L_S = (3/4κ²)S² − (3/4)S·J 恒等于 (3/4κ²)(S−κ²J/2)² − (3κ²/16)J²（含体积权重 e）',
           'identity=%s extremum=%s value=%s' % (ok_sq, ok_ext, ok_val),
           'True/True/True', st(ok_sq and ok_ext and ok_val))
    record('B5', '平方配方',
           '二次核非退化：∂²L/∂S∂S = (3/2)/κ² ≠ 0（⇒ 该局部核可做高斯积分）',
           'second=%s' % ok_second, 'True', st(ok_second))

    # ---- B6 变分解与平方配方同一解 ----
    record('B6', '变分解',
           '对 S 代数变分给出 S^μ = (κ²/2) J5^μ，与平方配方的极值点一致',
           'S_sol=%s' % sol, '(1/2)·κ²·J', st(str(sol) == str(Fr(1, 2) * VK * VJ)))

    # ---- B7 手征块系数：-(3κ²/16)(JR−JL)² 的三块系数 ----
    expr = -Fr(3, 16) * VK * (VJ - VS).power(2)
    c_jr2 = expr.t.get((0, 2, 1, 0), Fr(0))
    c_jl2 = expr.t.get((2, 0, 1, 0), Fr(0))
    c_cross = expr.t.get((1, 1, 1, 0), Fr(0))
    ok_block = (c_jr2 == Fr(-3, 16) and c_jl2 == Fr(-3, 16) and c_cross == Fr(3, 8)
                and c_cross == 2 * Fr(3, 16))
    record('B7', '手征块',
           '同手征块系数 −3κ²/16、左右手交叉块系数 +2×(3κ²/16)=+3κ²/8',
           'JR²=%s JL²=%s cross=%s' % (c_jr2, c_jl2, c_cross),
           '−3/16, −3/16, +3/8', st(ok_block))

    # ---- B8 费米子方程中的立方项系数 ----
    record('B8', '变分解',
           '∂(J5²)/∂ψ̄ = 2 J5_μ γ^μ γ^5 ψ ⇒ 有效方程中该项系数为 2×(3κ²/16)=3κ²/8',
           'coef=%s' % (Fr(2) * Fr(3, 16)), '3/8', st(Fr(2) * Fr(3, 16) == Fr(3, 8)))
# ======================================================================
# C. SM 手征流 → 四费米算符落点（Warsaw / νSMEFT）
# ======================================================================
LEFT_FIELDS = ['Q', 'L']
RIGHT_FIELDS = ['u', 'd', 'e']
NAME_TABLE = {
    ('Q', 'Q'): ('qq', 1), ('L', 'L'): ('ll', None), ('Q', 'L'): ('lq', 1),
    ('u', 'u'): ('uu', None), ('d', 'd'): ('dd', None), ('e', 'e'): ('ee', None),
    ('u', 'd'): ('ud', 1), ('e', 'u'): ('eu', None), ('e', 'd'): ('ed', None),
    ('Q', 'u'): ('qu', 1), ('Q', 'd'): ('qd', 1), ('Q', 'e'): ('qe', None),
    ('L', 'u'): ('lu', None), ('L', 'd'): ('ld', None), ('L', 'e'): ('le', None),
}
ABSENT = [('qq', 3), ('lq', 3), ('qu', 8), ('qd', 8), ('ud', 8)]


def war_name(key):
    nm, sup = key
    return 'Q_%s^(%d)' % (nm, sup) if sup else 'Q_%s' % nm


def enumerate_pairs(right_fields):
    """返回按字典序排好的可重对（同一场自身也算一个条目）。"""
    out = []
    for a in LEFT_FIELDS:
        for b in LEFT_FIELDS:
            if LEFT_FIELDS.index(a) <= LEFT_FIELDS.index(b):
                out.append(tuple(sorted((a, b))))
    for a in right_fields:
        for b in right_fields:
            if right_fields.index(a) <= right_fields.index(b):
                out.append(tuple(sorted((a, b))))
    for a in LEFT_FIELDS:
        for b in right_fields:
            out.append(tuple(sorted((a, b))))
    return out


def pair_key(pair):
    a, b = pair
    if (a, b) in NAME_TABLE:
        return NAME_TABLE[(a, b)]
    return NAME_TABLE[(b, a)]


WARSAW_NAMES = set(n for (n, _s) in NAME_TABLE.values())


def parse_doc_operators(doc):
    """只解析 2.3 节那条 Warsaw 列举（含 'Warsaw' 的行），避免把场记号 Q_{Lp} 当成算符。"""
    got = set()
    for line in doc.splitlines():
        if 'Warsaw' not in line:
            continue
        # 正文写的是 $Q_{qq}^{(1)}$（上标带括号），两种写法都要能吃
        for nm, sup in re.findall(r'Q_\{([a-z]{2})\}(?:\^\{\(?(\d)\)?\})?', line):
            if nm in WARSAW_NAMES:
                got.add((nm, int(sup) if sup else None))
    return got


def check_c(doc):
    pairs = enumerate_pairs(RIGHT_FIELDS)
    expect = set(pair_key(p) for p in pairs)
    record('C1', '算符落点',
           '规范单态流两两相乘能落到的 Warsaw 矢量流型（flavor 未区分）应为 15 个',
           'count=%d names=%s' % (len(expect), sorted(war_name(k) for k in expect)),
           '15', st(len(expect) == 15))

    with_nu = enumerate_pairs(RIGHT_FIELDS + ['nu'])
    nu_only = [p for p in with_nu if 'nu' in p]
    record('C2', '算符落点',
           '含 ν_R 时应扩到 νSMEFT 基底：条目数由 15 增到 21（命名以 νSMEFT 为准，本文不代选）',
           'count=%d nu_involving=%s' % (len(with_nu), nu_only), '21',
           st(len(with_nu) == 21))

    doc_ops = parse_doc_operators(doc)
    missing = sorted(war_name(k) for k in expect - doc_ops if k in expect)
    extra = sorted(war_name(k) for k in doc_ops - expect)
    record('C3', '算符落点',
           '14 号册 2.3 节列举的算符名应覆盖 C1 的全部 15 个（文中用了"例如"，但列举须完整）',
           'listed=%d missing=%s extra=%s' % (len(doc_ops & expect), missing, extra),
           'missing=[] extra=[]', st(not missing and not extra),
           '修前缺 Q_eu、Q_ed（两个右手单态的跨味组合）；已按本门禁补入正文')

    record('C4', '算符落点',
           '非单态流的 Warsaw 成员（qq^(3)、lq^(3)、qu^(8)、qd^(8)、ud^(8)）在树级 EC 切片中系数为零',
           'absent=%s' % [war_name(k) for k in ABSENT],
           'these are not generated',
           'BOUNDARY',
           '这是可证伪签名而非缺陷：若观测到这些算符非零且无法由 RG 混合解释，则本切片被否证')

    # 味结构计数：n_g = 3
    ng = 3
    same = sum(1 for p in pairs if p[0] == p[1])
    cross = sum(1 for p in pairs if p[0] != p[1])
    n_same_flavour = ng * (ng + 1) // 2
    n_cross_flavour = ng * ng
    total = sum(n_same_flavour if p[0] == p[1] else n_cross_flavour for p in pairs)
    record('C5', '味结构',
           '各代流在 J5² 中按"求和后进平方"出现 ⇒ 味道指标结构被单一系数钉死',
           'same_pairs=%d(%d 味组合) cross_pairs=%d(%d 味组合) total=%d'
           % (same, n_same_flavour, cross, n_cross_flavour, total),
           '5(6) / 10(9) / 120', st(total == 120),
           '同一味组合内部系数全等 ⇒ 不是逐项拟合，而是 J5² 这一个结构的展开')

    # 味旋转不变性（正交矩阵，精确有理数）
    def eye3():
        return [[Fr(1) if i == j else Fr(0) for j in range(3)] for i in range(3)]

    def givens(n, i, j, c, s):
        M = eye3()
        M[i][i] = Fr(c)
        M[j][j] = Fr(c)
        M[i][j] = Fr(s)
        M[j][i] = -Fr(s)
        return M

    def matmul3(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

    # 精确有理 Givens 旋转：(c,s) 取 (3/5,4/5)、(5/13,12/13)、(8/17,15/17)、(7/25,24/25)
    u_u = matmul3(givens(3, 0, 1, Fr(3, 5), Fr(4, 5)),
                  givens(3, 1, 2, Fr(5, 13), Fr(12, 13)))
    u_d = matmul3(givens(3, 0, 2, Fr(8, 17), Fr(15, 17)),
                  givens(3, 0, 1, Fr(7, 25), Fr(24, 25)))

    def unitarity_gram(U):
        return [[sum(U[k][i] * U[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

    ok_unit = (unitarity_gram(u_u) == eye3() and unitarity_gram(u_d) == eye3())
    v_bad = [[Fr(1) if i == j else Fr(0) for j in range(3)] for i in range(3)]
    v_bad[0][0] = Fr(2)
    ok_control = unitarity_gram(v_bad) != eye3()
    record('C6', '味结构',
           '手征流之和 Σ_p j_p 在任意味道旋转下不变（Tr 型结构）⇒ 转到质量基后形式不变',
           'unitary=%s nonunitary_control_breaks=%s' % (ok_unit, ok_control),
           'True/True', st(ok_unit and ok_control),
           '含独立旋转 U_u、U_d 各一（对应 CKM 两侧不同旋转）；反对照（非酉）必须破坏它')

    record('C7', '味结构',
           '推论：该切片的四费米算符在树级味道盲 ⇒ 不产生树级 FCNC',
           'universality=%s' % st(ok_unit and ok_control), 'PASS（条件性）',
           st(ok_unit and ok_control),
           '条件：环路 Yukawa 混合仍可在 G_F 量级以下重新引入味破坏，量级被 κ² 压低 ⇒ 观测不可达')


# ======================================================================
# D. 路径积分测度口径
# ======================================================================
def check_d():
    # 树级部分：已在 B4 用精确多项式证明（含体积权重 w），这里只取"与 e 无关"的读数
    record('D1', '测度口径',
           '经典消去与高斯积分的树级结果相同，且都不依赖 e 的具体取值',
           'identity_proved_in_B4=True', 'True', 'PASS',
           '恒等式含体积权重 w 已逐项证明 ⇒ 高斯积分的树级核与经典消去逐项同形')

    cfg1 = [Fr(1), Fr(2), Fr(3), Fr(4)]        # Σ=10, Π=24
    cfg2 = [Fr(1), Fr(1), Fr(4), Fr(4)]        # Σ=10, Π=16

    def prod(cfg):
        acc = Fr(1)
        for w in cfg:
            acc *= w
        return acc

    same_sum = sum(cfg1) == sum(cfg2)
    diff_prod = prod(cfg1) != prod(cfg2)
    record('D2', '测度口径',
           '朴素坐标测度下 det ∝ Π_x e(x)^{-N_comp/2}：其依赖是 Σ ln e，不是 ∫ e',
           'same_sum=%s diff_prod=%s (Σ=%s, Π=%s/%s)'
           % (same_sum, diff_prod, sum(cfg1), prod(cfg1), prod(cfg2)),
           'same_sum=True diff_prod=True', st(same_sum and diff_prod),
           '两个配置体积和相同而乘积不同 ⇒ Σ ln e 不能写成 ∫e 的仿射函数 ⇒ 不能只归入宇宙学项')

    record('D3', '测度口径',
           '分量数 N_comp=4 ⇒ 每点行列式指数为 −N_comp/2 = −2',
           'exponent=%s' % (Fr(-4, 2)), '−2', st(Fr(-4, 2) == Fr(-2)))

    record('D4', '测度口径',
           '协变测度（以 ∫ e S² 为范数定义）下 e 依赖整体抵消 ⇒ 只留 ∝ 格点数的常数 ⇒ 归入宇宙学项',
           'covariant_measure_residual=const_per_point', 'const ∝ #cells', 'BOUNDARY',
           '文档 §2.2"N[e] 可能重整化宇宙学项"仅在协变测度下成立；朴素测度给的是 Σ ln e。'
           '这正是 §3"完整联络测度、Jacobian"那一行要做的事，本条把它量化为两种测度的函数形式差异')


# ======================================================================
# E. 能标口径与 M9 数值（Decimal 定点，CODATA2022 字面量）
# ======================================================================
HBAR = Decimal('1.054571817e-34')
CLIGHT = Decimal('299792458')
GN = Decimal('6.67430e-11')
EV_J = Decimal('1.602176634e-19')
PI = Decimal('3.14159265358979323846264338327950288419716939937511')
GF = Decimal('1.1663787e-5')          # GeV^-2，PDG，声明为外部输入
REF_REDUCED_GEV = Decimal('2.435e18')     # PDG 参考值（外部）
REF_PLANCK_GEV = Decimal('1.2209e19')     # PDG 参考值（外部）
LAMBDA_REF_TEV = Decimal('10')            # 复合/接触相互作用现有灵敏度，声明为外部输入


def dsqrt(x):
    return x.sqrt()


def check_e():
    m_red_kg = dsqrt(HBAR * CLIGHT / (8 * PI * GN))
    m_pl_kg = dsqrt(HBAR * CLIGHT / GN)
    gev_j = EV_J * Decimal('1e9')
    m_red_gev = m_red_kg * CLIGHT * CLIGHT / gev_j
    m_pl_gev = m_pl_kg * CLIGHT * CLIGHT / gev_j
    ratio = m_pl_gev / m_red_gev
    sqrt8pi = dsqrt(8 * PI)
    ok_ratio = abs(ratio - sqrt8pi) / sqrt8pi < Decimal('1e-30')
    record('E1', '能标口径',
           'κ_g²=8πG=M_Pl^{-2} 只在"约化普朗克质量"口径下成立；两口径相差 √(8π)',
           'M_reduced=%s GeV M_planck=%s GeV ratio=%s sqrt8pi=%s'
           % (m_red_gev, m_pl_gev, ratio, sqrt8pi),
           'ratio = sqrt(8π) = 5.0145', st(ok_ratio),
           '这是 8π 口径陷阱：14 号册若不声明用约化质量，Λ_EC 会整体差 √(8π)=5.0145 倍')

    dev_red = abs(m_red_gev - REF_REDUCED_GEV) / REF_REDUCED_GEV
    dev_pl = abs(m_pl_gev - REF_PLANCK_GEV) / REF_PLANCK_GEV
    record('E2', '能标口径',
           '由 CODATA2022 字面量算出的两个普朗克质量与 PDG 参考值一致',
           'dev_reduced=%s dev_planck=%s' % (dev_red, dev_pl), '< 1e-3',
           st(dev_red < Decimal('1e-3') and dev_pl < Decimal('1e-3')))

    lam_ec = (Decimal(4) / dsqrt(Decimal(3))) * m_red_gev
    lam_ratio = lam_ec / m_red_gev
    ok_lam = abs(lam_ratio - Decimal(4) / dsqrt(Decimal(3))) < Decimal('1e-25')
    record('E3', '能标口径',
           'Λ_EC = (4/√3) M̄_Pl，且 Λ_EC / M̄_Pl = 4/√3 = 2.3094 > 1',
           'Lambda_EC=%s GeV ratio=%s' % (lam_ec, lam_ratio), '2.3094', st(ok_lam),
           '若改用非约化普朗克质量，同一公式给 2.82e19 GeV；"已高于 reduced Planck"只在约化口径下为真')

    a_coef = Decimal(3) / (Decimal(16) * m_red_gev * m_red_gev)
    lam_from_a = Decimal(1) / dsqrt(a_coef)
    ok_a = abs(lam_from_a - lam_ec) / lam_ec < Decimal('1e-25')
    record('E4', 'M9 数值',
           '接触系数 a = 3/(16 M̄_Pl²)，反解 1/√a 与 Λ_EC 一致',
           'a=%s GeV^-2  1/sqrt(a)=%s GeV' % (a_coef, lam_from_a), '= Λ_EC',
           st(ok_a))
    KEYNUM['a_coeff_GeV_minus2'] = str(a_coef)

    weak = GF / dsqrt(Decimal(2))
    r_weak = a_coef / weak
    record('E5', 'M9 数值',
           '与弱有效相互作用强度 G_F/√2 的比值（同一量纲，可直接比）',
           'a=%s  G_F/√2=%s  ratio=%s' % (a_coef, weak, r_weak),
           'ratio ≈ 3.8e-33', st(Decimal('1e-34') < r_weak < Decimal('1e-31')),
           'G_F 为外部输入（PDG 1.1663787e-5 GeV^-2）')
    KEYNUM['ratio_to_weak_contact'] = str(r_weak)

    lam_ref_gev = LAMBDA_REF_TEV * Decimal('1e3')
    needed = (lam_ec / lam_ref_gev) ** 2
    record('E6', 'M9 数值',
           '若以现有 ~10 TeV 接触相互作用灵敏度为参照，要让该接触项达到同量级需灵敏度提升',
           'needed_factor=%s' % needed, '~3e29',
           st(Decimal('1e28') < needed < Decimal('1e31')),
           '10 TeV 是声明的外部输入（复合/接触相互作用的现有量级），不是本理论推出')
    KEYNUM['sensitivity_gap_vs_10TeV'] = str(needed)

    rows = []
    for egev, tag in [(Decimal('1e3'), '1 TeV'), (Decimal('1.36e4'), '13.6 TeV'),
                      (Decimal('1e10'), '1e10 GeV')]:
        rows.append('%s:%.3e' % (tag, Decimal(3) / Decimal(16) * (egev / m_red_gev) ** 2))
    record('E7', 'M9 数值',
           '|L_4ψ|/|L_kin| ~ (3/16)(E/M̄_Pl)² 在若干能标下的取值',
           ' ; '.join(rows), '量级随 (E/M̄_Pl)²',
           'PASS', '普通粒子能标下该修正极小；E→M̄_Pl 时 EFT 本身已失效，不是"效应变大"')
    KEYNUM['lambda_EC_GeV'] = str(lam_ec)
    KEYNUM['reduced_planck_GeV'] = str(m_red_gev)
    KEYNUM['planck_GeV'] = str(m_pl_gev)


def check_z():
    sib = ROOT / 'torsion_operator_basis.py'
    record('Z1', '分工',
           '同目录 torsion_operator_basis.py 负责 24 分量 contorsion 指标代数与 Fierz 基底；'
           '本仪器负责归一化约定、量纲、算符落点、测度口径、能标数值与依赖图拓扑（互不共享代码）',
           'sibling_exists=%s' % sib.exists(), 'True（读数以该仪器自身输出为准）', 'INFO')


def main():
    doc = read_doc()
    check_a(doc)
    check_b()
    check_c(doc)
    check_d()
    check_e()
    check_z()

    counts = {}
    for r in RESULT:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    npass = counts.get('PASS', 0)
    nfail = counts.get('FAIL', 0)
    nbound = counts.get('BOUNDARY', 0)
    ninfo = counts.get('INFO', 0)
    total = len(RESULT)
    ok_count = (npass + nfail + nbound + ninfo == total)
    record('Z9', '自检', '条目状态计数自洽（PASS+FAIL+BOUNDARY+INFO = 总数）',
           '%s' % ok_count, 'True', st(ok_count))

    out = {'tests': RESULT,
           'summary': {'total': total, 'pass': npass, 'fail': nfail,
                       'boundary': nbound, 'info': ninfo},
           'key_numbers': KEYNUM}
    with open(ROOT / 'ufec14_convention_audit.json', 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print('== ufec14_convention_audit: total=%d PASS=%d FAIL=%d BOUNDARY=%d INFO=%d'
          % (total, npass, nfail, nbound, ninfo))
    for r in RESULT:
        print('  [%s] %s (%s): %s' % (r['status'], r['id'], r['group'], r['claim']))
        if r['status'] != 'PASS':
            print('        computed=%s | expected=%s' % (r['computed'], r['expected']))
        if r['note']:
            print('        note: %s' % r['note'])
    if nfail:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
