# -*- coding: utf-8 -*-
# attack40 / 攻破㉜ —— 力统一承重前提：阈值 × Yukawa × 质子衰变联合可识别性（2026-11-08）
# 靶：最终达成声明 / P1 论文「SO(10) 最小且唯一最优、单张量、收敛+预言已达成」的承重前提。
# 纯标准库（Fraction + math + json/io/os + ast），无第三方依赖、无随机。
# 红线：攻破的是「零/少参数、唯一、已达成」承重前提，不是否证 MSSM-SO(10) 物理；0/22、UFT-3=0、L3=0 不变。
import os, sys, io, json, math, ast
from fractions import Fraction as F
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'attack40_力统一承重前提_阈值Yukawa联合可识别性_2026-11-08'
P1_REL = os.path.join(HERE, '论文体系_Nature规范', 'P1_力的大统一方程_MSSM-SO10.md')
BILL_REL = os.path.join(HERE, 'SM新物理候选账单_2026-10-21.md')
FINAL_REL = os.path.join(HERE, '统一场论攻破_最终达成声明_2026-10-30.md')
LINES = []
ENTRIES = []
GUARDS = []

def emit(s=''):
    LINES.append(s)
    print(s)

def add(uid, claim, verdict, reading):
    ENTRIES.append({'id': uid, 'claim': claim, 'verdict': verdict, 'reading': reading})
    emit('[%-9s] %s | %s' % (verdict, uid, claim))
    emit('            读数: %s' % reading)

def guard(gid, desc, ok, reading):
    ok = bool(ok)
    GUARDS.append({'id': gid, 'desc': desc, 'ok': ok, 'reading': reading})
    emit('[%s] %s | %s' % ('OK' if ok else 'BAD', gid, desc))
    emit('            读数: %s' % reading)
    return ok

# ---------- [C] 级输入（逐字登记）----------
MZ = 91.1876                    # GeV
AEM_INV = 127.916
AEM = 1.0 / AEM_INV
AS = 0.1184
SW = 0.23122
TWOPI = 2.0 * math.pi
BSM = (F(41, 10), F(-19, 6), F(-7))       # SM 段 beta
BM = (F(33, 5), F(1), F(-3))              # MSSM 段 beta
A_INV = [(3.0 / 5.0) * (1.0 - SW) / AEM, SW / AEM, 1.0 / AS]  # (alpha_1^-1, alpha_2^-1, alpha_3^-1) at M_Z
SK = 2.4e34                    # yr, Super-K 实下限（attack27b M7）
TAU0 = 1.0e35                  # yr, attack27b 工程闭式归一化
M_REF = 2.0e16                 # GeV
AGINV_REF = 35.0
AH_REF = 0.015                 # GeV^3
AH_GRID = [0.0075, 0.015, 0.021]

def coupling_at_gut(i, L1, L2, delta=0.0):
    # alpha_i^-1(M_GUT) = a_i - (b_i^SM L1 + b_i^MSSM L2)/(2pi) + Delta_i
    return A_INV[i] - (float(BSM[i]) * L1 + float(BM[i]) * L2) / TWOPI + delta

def tau_p_of(mgut, aginv, ah):
    # attack27b M2: tau_p = 1e35 (M/2e16)^4 (alpha_GUT_ref/alpha_GUT)^2 (0.015/alpha_H)^2
    # alpha_GUT_ref / alpha_GUT = (1/35) / (1/ag_inv) = ag_inv/35
    return TAU0 * (mgut / M_REF) ** 4 * (aginv / AGINV_REF) ** 2 * (AH_REF / ah) ** 2

def solution(msusy, mgut, aginv, label):
    L1 = math.log(msusy / MZ)
    L2 = math.log(mgut / msusy)
    q = [coupling_at_gut(i, L1, L2, 0.0) for i in range(3)]
    delta = [aginv - q[i] for i in range(3)]
    pred = [q[i] + delta[i] for i in range(3)]
    res = max(abs(pred[i] - aginv) for i in range(3))
    return {'label': label, 'msusy': msusy, 'mgut': mgut, 'aginv': aginv,
            'L1': L1, 'L2': L2, 'q': q, 'delta': delta, 'residual': res,
            'tau_p': tau_p_of(mgut, aginv, AH_REF)}

def rank_fraction(mat):
    # 精确有理数行秩；输入元素只能是 int / Fraction
    m = [[F(x) for x in row] for row in mat]
    rows = len(m)
    cols = len(m[0]) if rows else 0
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        for i in range(r + 1, rows):
            if m[i][c] != 0:
                fac = m[i][c] / pv
                for j in range(c, cols):
                    m[i][j] -= fac * m[r][j]
        r += 1
        if r == rows:
            break
    return r

# 线性化阈值方向：第 1 个为完整 GUT 多重态 (1,1,1)，其余为可分裂方向；只作可识别性上界，不声称具体表示。
TH_DIRS = [(F(1), F(1), F(1)), (F(1), F(0), F(0)), (F(0), F(1), F(0)),
           (F(0), F(0), F(1)), (F(1), F(-1), F(0)), (F(1), F(1), F(-2))]

def rank_nullity(n):
    # 未知量 [A, L1, L2, ell_1..ell_n]；每行 i 对应一个低能 alpha_i^-1 约束。
    # 列 2.. 末尾共同乘以 1/(2pi) 不改变秩，故用 beta / threshold 整数向量。
    rows = []
    for i in range(3):
        row = [F(1), BSM[i], BM[i]] + [-TH_DIRS[k][i] for k in range(n)]
        rows.append(row)
    r = rank_fraction(rows)
    return r, (3 + n) - r

def diff_rank(direction):
    # 只看两条相对汇合方程 (i=1,2 减 i=3) 的秩；完整多重态应在此投影下为零列。
    rows = []
    for i in (0, 1):
        rows.append([BSM[i] - BSM[2], BM[i] - BM[2], -(direction[i] - direction[2])])
    return rank_fraction(rows)

emit('== attack40 攻破㉜·力统一承重前提：阈值 × Yukawa × 质子衰变联合可识别性 ==')
emit('-- 承接 attack27/27b/28/29/34/38：本册不重做 C38 四门，改判「SO(10) 唯一最优/单张量/已达成」承重前提 --')
emit('-- 输入：[C] 级低能耦合 + 一阶 beta + attack27b tau_p 闭式 + P1/最终声明/候选账单只读文本 --')
emit('-- 边界：阈值方向是线性化可识别性上界，不构造具体 GUT 谱；S2 只作跨分支一致性反例，不是完整 2-loop 阈值推导 --')
# ---------- 一阶两段、无阈值的控制组解（复现 attack29 方法 A）----------
a11, a12 = float(BSM[0] - BSM[2]), float(BM[0] - BM[2])
a21, a22 = float(BSM[1] - BSM[2]), float(BM[1] - BM[2])
r1 = TWOPI * (A_INV[0] - A_INV[2])
r2 = TWOPI * (A_INV[1] - A_INV[2])
det = a11 * a22 - a12 * a21
L1_0 = (r1 * a22 - a12 * r2) / det
L2_0 = (a11 * r2 - r1 * a21) / det
MSUSY0 = MZ * math.exp(L1_0)
MGUT0 = MZ * math.exp(L1_0 + L2_0)
q0 = [coupling_at_gut(i, L1_0, L2_0, 0.0) for i in range(3)]
A0 = sum(q0) / 3.0
q0_spread = max(q0) - min(q0)
TAU0_CENTRAL = tau_p_of(MGUT0, A0, AH_REF)

# 三组显式解：S0 为无阈值反解；S1 同 M_GUT/A/tau_p 但把 M_SUSY 拉到 1 TeV；
# S2 取 attack34 的 2-loop b33=+14 分支，检查阈值能否把它接到同一组低能耦合上。
s0 = solution(MSUSY0, MGUT0, A0, 'S0')
s1 = solution(1000.0, MGUT0, A0, 'S1')
s2 = solution(2317.71643, 1.117972e16, 25.6672, 'S2')

# ---------- 精确秩 / 零空间表 ----------
rank_table = [(n,) + rank_nullity(n) for n in range(7)]
rank_ok = all(r == 3 and nu == n for n, r, nu in rank_table)
d_rank_univ = diff_rank(TH_DIRS[0])
d_rank_split = diff_rank(TH_DIRS[1])
univ_col_zero = (TH_DIRS[0][0] - TH_DIRS[0][2]) == 0
split_col_nonzero = (TH_DIRS[1][0] - TH_DIRS[1][2]) != 0

# ---------- 质子衰变口径分支扫描 ----------
BRANCHES = [('S0_one_loop', MGUT0, A0),
            ('attack27b_1TeV', 1.6899061e16, 25.826977),
            ('attack34_2loop_b33p14', 1.117972e16, 25.6672)]
branch_rows = []
for name, mg, ag in BRANCHES:
    vals = [tau_p_of(mg, ag, ah) for ah in AH_GRID]
    flags = [1 if t >= SK else 0 for t in vals]
    branch_rows.append({'name': name, 'mgut': mg, 'aginv': ag,
                        'tau': vals, 'pass_flags': flags})
flip_branches = sum(1 for b in branch_rows if len(set(b['pass_flags'])) > 1)
pass_cells = sum(sum(b['pass_flags']) for b in branch_rows)

# ---------- 只读事实源：P1 / 最终声明 / 候选账单 ----------
def read_lines(path):
    if os.path.isfile(path):
        return io.open(path, encoding='utf-8').read().splitlines()
    return []

p1_lines = read_lines(P1_REL)
final_lines = read_lines(FINAL_REL)
bill_lines = read_lines(BILL_REL)
w_line = next((x for x in p1_lines if 'W=y_{10}' in x), '')
single_line = next((x for x in p1_lines if '单张量' in x), '')
final_single = sum(1 for x in final_lines if '单张量 y₁₀' in x)
bill_line = next((x for x in bill_lines if '大统一 SU(5)/SO(10)/E6' in x), '')
p1_c10 = w_line.count('y_{10}')
p1_c126 = w_line.count('y_{126}')
p1_conflict = 1 if (p1_c10 >= 1 and p1_c126 >= 1 and '单张量' in single_line) else 0
bill6 = 1 if ('**6**' in bill_line and '阈值修正' in bill_line and 'Yukawa 嵌入' in bill_line) else 0
# ---------- t-b-tau 统一：纯标准库 RK4 复现 attack27b 一阶 Yukawa RGE ----------
# 口径：M_Z 处由树级质量 + tan(beta) 初始化；从 M_Z 直接以 MSSM 一阶 beta 跑到 M_GUT，
# 不含 2-loop、不含 delta_b 阈值、不含完整超伴子谱。只判「单张量/零参数」承重前提。
Y_MGUT = 1.6899061e16
V = 246.22
MT_POLE = 172.76
MB_MB = 4.18
MTAU = 1.77686
K16 = 16.0 * math.pi ** 2
a1_in = AEM / (1.0 - SW) * (5.0 / 3.0)
a2_in = AEM / SW
a3_in = AS
G0 = [math.sqrt(4.0 * math.pi * a1_in), math.sqrt(4.0 * math.pi * a2_in),
      math.sqrt(4.0 * math.pi * a3_in)]

def yuk_init(tanb):
    sb = tanb / math.sqrt(1.0 + tanb ** 2)
    cb = 1.0 / math.sqrt(1.0 + tanb ** 2)
    yt = MT_POLE * math.sqrt(2.0) / (V * sb)
    yb = MB_MB * math.sqrt(2.0) / (V * cb)
    ytau = MTAU * math.sqrt(2.0) / (V * cb)
    return [yt, yb, ytau, G0[0], G0[1], G0[2]]

def yuk_deriv(y):
    yt, yb, ytau, g1, g2, g3 = y
    dyt = yt * (6.0 * yt ** 2 + yb ** 2 - (13.0 / 15.0) * g1 ** 2
                - 3.0 * g2 ** 2 - (16.0 / 3.0) * g3 ** 2) / K16
    dyb = yb * (6.0 * yb ** 2 + yt ** 2 + ytau ** 2 - (7.0 / 15.0) * g1 ** 2
                - 3.0 * g2 ** 2 - (16.0 / 3.0) * g3 ** 2) / K16
    dytau = ytau * (4.0 * ytau ** 2 + 3.0 * yb ** 2
                    - (9.0 / 5.0) * g1 ** 2 - 3.0 * g2 ** 2) / K16
    dg1 = (33.0 / 5.0) * g1 ** 3 / K16
    dg2 = 1.0 * g2 ** 3 / K16
    dg3 = -3.0 * g3 ** 3 / K16
    return [dyt, dyb, dytau, dg1, dg2, dg3]

def rk4_step(y, h):
    k1 = yuk_deriv(y)
    y2 = [y[i] + h / 2.0 * k1[i] for i in range(6)]
    k2 = yuk_deriv(y2)
    y3 = [y[i] + h / 2.0 * k2[i] for i in range(6)]
    k3 = yuk_deriv(y3)
    y4 = [y[i] + h * k3[i] for i in range(6)]
    k4 = yuk_deriv(y4)
    return [y[i] + h / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) for i in range(6)]

def run_yukawa(tanb, N, mgut):
    y = yuk_init(float(tanb))
    T = math.log(mgut / MZ)
    h = T / N
    blown = 0
    for _ in range(N):
        y = rk4_step(y, h)
        if any((v > 100.0 or not math.isfinite(v)) for v in y[:3]):
            blown = 1
            break
    if blown == 1:
        return {'tanb': tanb, 'blown': 1, 'yt': float('nan'), 'yb': float('nan'),
                'ytau': float('nan'), 'ratio_tb': float('nan'),
                'ratio_btau': float('nan'), 'maxdev': float('nan')}
    yt, yb, ytau = y[0], y[1], y[2]
    rtb = yt / yb
    rbtau = yb / ytau
    maxdev = max(abs(rtb - 1.0), abs(ytau / yb - 1.0))
    return {'tanb': tanb, 'blown': 0, 'yt': yt, 'yb': yb, 'ytau': ytau,
            'ratio_tb': rtb, 'ratio_btau': rbtau, 'maxdev': maxdev}

TANB_GRID = [2, 5, 10, 20, 30, 50]
yuk_scan = [run_yukawa(t, 600, Y_MGUT) for t in TANB_GRID]
yuk_finite = [r for r in yuk_scan if r['blown'] == 0]
yuk_best = min(yuk_finite, key=lambda r: r['maxdev']) if yuk_finite else {'maxdev': float('nan'), 'tanb': -1}
yuk_triple_hits = [r for r in yuk_finite if r['maxdev'] < 0.30]
yuk_self = abs(run_yukawa(10, 1200, Y_MGUT)['ratio_btau'] - run_yukawa(10, 600, Y_MGUT)['ratio_btau'])
tan50_blown = (yuk_scan[-1]['blown'] == 1)
def fmt_vec(v, fmt='%.6f'):
    return '[' + ', '.join(fmt % x for x in v) + ']'

def sanitize(x):
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x

def clean_dict(d):
    return {k: sanitize(v) for k, v in d.items()}

# ---------- 条目 ----------
add('T01', '控制组：纯标准库复现 attack29 一阶反解与 attack27b tau_p 闭式', 'PASS',
    'M_SUSY=%.6f GeV（attack29 54.384716）；M_GUT=%.6e GeV（attack29 2.3214509e16）；alpha_G^-1=%.6f；q0_spread=%.3e；tau_p(0.015)=%.4e yr'
    % (MSUSY0, MGUT0, A0, q0_spread, TAU0_CENTRAL))

rank_read = '；'.join('n=%d rank=%d nullity=%d' % (n, r, nu) for n, r, nu in rank_table)
add('T02', '阈值线性系统 rank=3、nullity=n：每增 1 个阈值对数即多 1 个零空间方向', 'FAIL',
    'n=0..6 精确秩/nullity：%s；3 条低能耦合约束面对 3+n 个未知量 ⇒ 零参数唯一性从 n>=1 起失效' % rank_read)

add('T03', '显式双解：同一组低能耦合、同一 M_GUT/A/tau_p，可由不同 M_SUSY 与阈值实现', 'FAIL',
    'S0 M_SUSY=%.6f GeV delta=%s；S1 M_SUSY=%.1f GeV delta=%s；两者 M_GUT 与 alpha_G^-1 逐位相同、tau_p 相同，统一残差 %.3e / %.3e'
    % (s0['msusy'], fmt_vec(s0['delta']), s1['msusy'], fmt_vec(s1['delta']),
       s0['residual'], s1['residual']))

add('T04', '第三解：阈值可把 2-loop 被排除分支接到同一低能耦合上', 'FAIL',
    'S2 M_SUSY=%.5f GeV / M_GUT=%.6e GeV / alpha_G^-1=%.4f；delta=%s；tau_p=%.4e yr < SK %.3e；统一残差 %.3e'
    % (s2['msusy'], s2['mgut'], s2['aginv'], fmt_vec(s2['delta']),
       s2['tau_p'], SK, s2['residual']))

add('T05', 't-b-tau 三重统一：tanβ 扫描下无一阶 RGE 命中，tanβ=50 发散', 'BOUNDARY',
    'tanβ=%s；best=tanβ %d maxdev=%.4f；triple_hits=%d；tanβ=50 blown=%d；N=600/1200 自收敛 %.3e（一阶、无 delta_b、无完整谱，标 BOUNDARY）'
    % (TANB_GRID, yuk_best['tanb'], yuk_best['maxdev'], len(yuk_triple_hits),
       1 if tan50_blown else 0, yuk_self))

add('T06', 'P1 超势自证「单张量」口径冲突：W 含 y_{10} 与 y_{126} 两个独立张量', 'FAIL',
    'W line: y_{10}×%d, y_{126}×%d；P1 单张量行=%d 命中，最终声明「单张量 y₁₀」行=%d 命中；同一来源给出 2 与 1 两种口径'
    % (p1_c10, p1_c126, 1 if '单张量' in single_line else 0, final_single))

add('T07', '外部输入账：GUT 行已登记 6 项，阈值/Yukawa 又展开为连续自由度', 'FAIL',
    'SM新物理候选账单 GUT 行 **6** 命中=%d；本册显式展开 n 个阈值对数 + tanβ + y10/y126 + delta_b + 谱；「零参数/单张量」不成立于此账本' % bill6)

branch_read = '；'.join('%s flags=%s tau0=%.3e' % (b['name'], b['pass_flags'], b['tau'][1]) for b in branch_rows)
add('T08', '质子衰变口径分支数：3 分支 × 3 alpha_H 给出混合判决', 'FAIL',
    '%s；pass_cells=%d/9；alpha_H 内部翻转分支=%d ⇒ 单一「已与实验相容」结论不成立' % (branch_read, pass_cells, flip_branches))

add('T09', '联合可行域：物理域与 tau_p 下限可同时满足，也可被阈值改写成不满足', 'INFO',
    'S1 M_SUSY=%.1f GeV >= M_Z 且 tau_p=%.4e yr >= SK；S2 M_SUSY=%.1f GeV 但 tau_p=%.4e yr < SK；两者统一残差均 <1e-9 ⇒ 缺的是谱输入而非推导' 
    % (s1['msusy'], s1['tau_p'], s2['msusy'], s2['tau_p']))

add('T10', '总裁定：FAIL（作为「MSSM-SO(10) 可作最终大统一攻破」的承重前提）', 'INFO',
    '四路读数：秩欠定、显式双解、Yukawa 自由度、单张量口径冲突；攻破的是「零/少参数、唯一最优、已达成」，不否证 MSSM-SO(10) 物理；红线 0/22、UFT-3=0、L3=0、validated=0 不变')

# ---------- 守卫 ----------
guard('G40-1', '基线锚逐位复现 attack29 / attack27b',
      abs(MSUSY0 - 54.384716) < 0.01 and abs(MGUT0 / 2.3214509e16 - 1.0) < 0.001
      and abs(A0 - 23.9547) < 0.05 and q0_spread < 1e-9,
      'MSUSY=%.6f / MGUT=%.6e / A=%.6f / qspread=%.3e' % (MSUSY0, MGUT0, A0, q0_spread))
guard('G40-2', '精确秩/nullity 表 n=0..6 全部 rank=3、nullity=n', rank_ok, rank_read)
guard('G40-3', '完整多重态阳性对照：差分矩阵不增秩，分裂方向列非零',
      d_rank_univ == 2 and d_rank_split == 2 and univ_col_zero and split_col_nonzero,
      'diff_rank(universal)=%d / diff_rank(split)=%d；universal_zero=%s / split_nonzero=%s'
      % (d_rank_univ, d_rank_split, univ_col_zero, split_col_nonzero))
guard('G40-4', 'S0/S1 双解有牙：同 M_GUT/A/tau_p、不同 M_SUSY/delta、残差机器零',
      max(s0['residual'], s1['residual']) < 1e-9 and abs(s1['mgut'] - s0['mgut']) < 1e-6
      and abs(s1['aginv'] - s0['aginv']) < 1e-12 and s1['msusy'] > MZ
      and max(abs(d) for d in s1['delta']) > 1e-3,
      'res %.3e/%.3e；S1 delta=%s' % (s0['residual'], s1['residual'], fmt_vec(s1['delta'])))
guard('G40-5', 'S2 第三解有牙：精确汇合但 tau_p 被排除',
      s2['residual'] < 1e-9 and s2['tau_p'] < SK and s2['msusy'] >= MZ
      and max(abs(d) for d in s2['delta']) > 1e-3,
      'res=%.3e tau=%.4e delta=%s' % (s2['residual'], s2['tau_p'], fmt_vec(s2['delta'])))
tau_ratio = tau_p_of(2.0 * MGUT0, A0, AH_REF) / TAU0_CENTRAL
guard('G40-6', 'tau_p 真读 M_GUT：M_GUT×2 ⇒ tau_p×16', abs(tau_ratio - 16.0) < 1e-9,
      'ratio=%.12f' % tau_ratio)
guard('G40-7', 'Yukawa RK4 自收敛且 tanβ=50 发散守卫生效',
      yuk_self < 1e-6 and tan50_blown,
      'self=%.3e tan50_blown=%d' % (yuk_self, 1 if tan50_blown else 0))
guard('G40-8', 't-b-tau 三重统一无一阶命中，且 best maxdev 显著大于容差',
      len(yuk_triple_hits) == 0 and yuk_best['maxdev'] > 0.5,
      'hits=%d best_tanb=%d best_maxdev=%.6f' % (len(yuk_triple_hits), yuk_best['tanb'], yuk_best['maxdev']))
guard('G40-9', '只读事实源扫描有牙：P1 双张量 / 最终声明单张量 / 账单 6 项同时命中',
      p1_conflict == 1 and bill6 == 1 and final_single >= 1,
      'p1_c10=%d p1_c126=%d p1_single=%d final_single=%d bill6=%d'
      % (p1_c10, p1_c126, 1 if '单张量' in single_line else 0, final_single, bill6))
SRC = io.open(os.path.join(HERE, BASE + '.py'), encoding='utf-8').read()
TREE = ast.parse(SRC)
true_consts = [n.lineno for n in ast.walk(TREE)
               if isinstance(n, ast.Constant) and isinstance(n.value, bool) and n.value == (1 == 1)]
guard('G40-10', '书写式守卫：本引擎源码无 Python 字面量 true 常量', len(true_consts) == 0,
      'literal_true_consts=%d；红线文本=%s' % (len(true_consts), '0/22、UFT-3=0、L3=0' in SRC))

# ---------- 汇总 / 产物 ----------
npass = sum(1 for e in ENTRIES if e['verdict'] == 'PASS')
nfail = sum(1 for e in ENTRIES if e['verdict'] == 'FAIL')
nbnd = sum(1 for e in ENTRIES if e['verdict'] == 'BOUNDARY')
ninfo = sum(1 for e in ENTRIES if e['verdict'] == 'INFO')
nok = sum(1 for g in GUARDS if g['ok'])
emit('== 汇总：条目 %d；PASS %d / FAIL %d / BOUNDARY %d / INFO %d；守卫 %d/%d =='
     % (len(ENTRIES), npass, nfail, nbnd, ninfo, nok, len(GUARDS)))
emit('== 总裁定：FAIL（作为「MSSM-SO(10) 可作最终大统一攻破」的承重前提）；攻破的是零/少参数、唯一最优、已达成 ==')
emit('红线：数学/机器自洽 ≠ 物理成立；不否证 MSSM-SO(10) 物理；0/22、UFT-3=0、L3=0、validated=0 不变；未改治理事实源、未跑 refresh_catalog。')

payload = {
    'round': 'attack40_攻破㉜_力统一承重前提_阈值Yukawa联合可识别性',
    'date': '2026-11-08',
    'engine': BASE + '.py',
    'entries': ENTRIES,
    'summary': {'PASS': npass, 'FAIL': nfail, 'BOUNDARY': nbnd, 'INFO': ninfo},
    'guards': GUARDS,
    'guard_pass': '%d/%d' % (nok, len(GUARDS)),
    'readings': {
        'baseline': {'M_SUSY_GeV': MSUSY0, 'M_GUT_GeV': MGUT0, 'alpha_G_inv': A0,
                     'L1': L1_0, 'L2': L2_0, 'q_spread': q0_spread, 'tau_p_central_yr': TAU0_CENTRAL},
        'rank_table': [{'n': n, 'rank': r, 'nullity': nu} for n, r, nu in rank_table],
        'solutions': {k: clean_dict(s) for k, s in [('S0', s0), ('S1', s1), ('S2', s2)]},
        'proton_branches': branch_rows,
        'proton_pass_cells': pass_cells,
        'proton_flip_branches': flip_branches,
        'yukawa_scan': [clean_dict(r) for r in yuk_scan],
        'yukawa_best': clean_dict(yuk_best),
        'yukawa_self_convergence': yuk_self,
        'tan50_blown': 1 if tan50_blown else 0,
        'p1_static': {'y10_count': p1_c10, 'y126_count': p1_c126,
                      'single_claim_line': single_line, 'final_single_y10_lines': final_single},
        'bill_static': {'gut_row': bill_line, 'six_inputs_hit': bill6},
        'tau_p_double_M_GUT_ratio': tau_ratio,
    },
    'self_corrections': [],
    'boundaries': [
        '阈值方向是线性化可识别性上界；只证明「给自由谱阈值即零空间增加」，不构造具体 GUT 多重态谱',
        'S2 取 attack34 的 2-loop b33=+14 分支作为外部锚，阈值拟合仍走一阶线性方程；只作跨分支一致性反例，不是完整 2-loop 阈值推导',
        'Yukawa RGE 与 attack27b 同口径：一阶、从 M_Z 直接用 MSSM beta、无 delta_b、无完整超伴子谱；t-b-tau 结论标 BOUNDARY',
        'tau_p 是 attack27b 工程闭式，绝对标度带 O(1) 系数不确定度；本册只用其分支翻转与 M_GUT 四次方依赖',
    ],
    'methodology_notes': [
        'G40-10 用 1 == 1 的比较式检查布尔字面量，避免守卫自身写入被 AST 扫描命中',
        '精确秩表用 Fraction 高斯消元；列共同缩放 1/(2pi) 不改变秩',
    ],
    'cross_refs': [
        '判定_attack29_M8候选关系穷举与判决_2026-10-31.md',
        '判定_attack27b_零代价修法修正引擎_2026-10-30.md',
        '判定_attack34_b33符号物理后果_tau_p与物理域判定_2026-10-31.md',
        '判定_attack38_攻破㉚_力统一候选C38四门机验_2026-11-07.md',
        '判定_attack39_攻破㉛_omega自由函数防线_四路封死与定量互斥_2026-11-08.md',
        '统一场论攻破_最终达成声明_2026-10-30.md',
        '论文体系_Nature规范/P1_力的大统一方程_MSSM-SO10.md',
        'SM新物理候选账单_2026-10-21.md',
        '../状态看板.md',
    ],
    'redlines': {'zero_of_22': 'unchanged', 'UFT-3': 0, 'L3': 0, 'validated': 0},
    'candidate_verdict': 'FAIL',
    'exit': 0 if nok == len(GUARDS) else 1,
}
with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
with io.open(os.path.join(HERE, BASE + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(LINES) + '\n')
sys.exit(0 if nok == len(GUARDS) else 1)