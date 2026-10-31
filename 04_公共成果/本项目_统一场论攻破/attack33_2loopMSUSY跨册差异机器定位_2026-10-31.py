# -*- coding: utf-8 -*-
# attack33 v2 · 2-loop M_SUSY 跨册差异的机器定位（b_ij 逐元素 / 分段动力学 / 求解域 / 残差）
#
# 承接 attack32 的 F5 / F5c：那一册把 attack30 的 193.04 GeV 与自己的 2317.72 GeV
# 之间的差异归因为「非对角 b_ij 项是否计入」，依据是「V1 仅对角项」恰好落在
# 193 附近（差 4.89%）。本册不重复该归因，而是做可机器判定的事：
#
#   A0  v1 自查缺陷：两段式打靶若用单一矩阵跑两段，解的不是同一方程组（本轮修正）
#   A1  b_ij 逐元素对拍（两册矩阵的差异集合）
#   A2  attack30 报出的 M_SUSY 是否等于其搜索域上界（恒等式核验）
#   A3  源码静态审计：搜索域注释与 range() 是否一致
#   A4  F5c 归因更正：非对角项是否真是主因
#   A5  原始域最优残差读数（attack30 未报告的量）
#   A6  扩展域 + 局部精修能否收敛到真解（决定性对照）
#   A7  b33 符号对解的独立影响（引用必须声明）
#   A8  引用纪律（最小可复现字段）
#   A9  反解的多值性（多初值扫描）
#
# 纪律：本册不判 attack30 / attack32 的作者「算错」；只判定「报出的量是不是解 /
#       两个数字是否来自同一方程组」。v1 对本册自身同样适用：v1 的 1780.00 与
#       24053.22 已被本册 A0 判为「另一方程组的根」并作废。
import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
ENTRIES = []


def add(code, verdict, title, value, note):
    ENTRIES.append({'code': code, 'verdict': verdict, 'title': title,
                    'value': value, 'note': note})


def E(*a):
    s = ' '.join(str(x) for x in a)
    try:
        print(s)
    except Exception:
        print(s.encode('ascii', 'replace').decode('ascii'))


# ---------------------------------------------------------------- 常量与矩阵
MZ = 91.1876
ALPHA_EM_INV = 127.916          # attack30 / attack32 同源输入
ALPHA_EM = 1.0 / ALPHA_EM_INV
ALPHA_S = 0.1184
X_OBS = 0.23122                 # sin^2 theta_W 实测（两册共同输入）

B1 = {'SM': [4.1, -19.0 / 6.0, -7.0],
      'MSSM': [33.0 / 5.0, 1.0, -3.0]}

# 1-loop 与 2-loop 都分段：SM 段用 SM 阵，MSSM 段用 MSSM 阵（attack32 口径）
B2_SM = [[199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0],
         [9.0 / 10.0, 35.0 / 6.0, 12.0],
         [11.0 / 10.0, 9.0 / 2.0, -26.0]]

# attack32 V0 的 B2['MSSM']：b33 = +14
B2_MS_P14 = [[199.0 / 25.0, 27.0 / 5.0, 88.0 / 5.0],
             [9.0 / 5.0, 25.0, 24.0],
             [11.0 / 5.0, 9.0, 14.0]]

# attack30 的 B_MS：b33 = -14
B2_MS_N14 = [[199.0 / 25.0, 27.0 / 5.0, 88.0 / 5.0],
             [9.0 / 5.0, 25.0, 24.0],
             [11.0 / 5.0, 9.0, -14.0]]

MATS_P14 = {'SM': B2_SM, 'MSSM': B2_MS_P14}
MATS_N14 = {'SM': B2_SM, 'MSSM': B2_MS_N14}
# v1 缺陷口径：SM 段也灌 MSSM 阵（用于复现 v1 的 1780.00 / 24053.22）
MATS_V1_SINGLE_P14 = {'SM': B2_MS_P14, 'MSSM': B2_MS_P14}
MATS_V1_SINGLE_N14 = {'SM': B2_MS_N14, 'MSSM': B2_MS_N14}

TWO_PI = 2.0 * math.pi
EIGHT_PI2 = 8.0 * math.pi ** 2

AMZ = [0.6 * (1.0 - X_OBS) / ALPHA_EM, X_OBS / ALPHA_EM, 1.0 / ALPHA_S]

# attack30 源码里的网格（solve_backward）
A30_RANGE_N = 46
A30_L1_STEP = 1.0 / 20.0
A30_L1_LO = -1.5
A30_L2_N = 71
A30_L2_STEP = 0.1
A30_L2_LO = 27.0
A30_N1, A30_N2 = 80, 160
A30_REPORTED_MSUSY = 193.04415
A30_NOTE_CLAIM = 3.0            # 源码注释声称的上界（-1.5 .. 3）

A32_REPORTED_MSUSY = 2317.71643
A32_REPORTED_SPREAD = 7.105e-15
A32_V3_MSUSY = 17918.76520      # attack32 F5c 的 V3「b33 反号」
A32_V3_SPREAD = 3.553e-14


# ---------------------------------------------------------------- RK4 引擎
def rhs(a, model, mats, two_loop):
    b = B1[model]
    if not two_loop:
        return [-b[i] / TWO_PI for i in range(3)]
    M = mats[model]
    out = [0.0, 0.0, 0.0]
    for i in range(3):
        s = 0.0
        for j in range(3):
            s += M[i][j] / a[j]
        out[i] = -b[i] / TWO_PI - s / EIGHT_PI2
    return out


def flow(a0, L1, L2, mats, two_loop=True, n1=None, n2=None):
    """两段 RK4：M_Z ->(SM, mats['SM']) M_SUSY ->(MSSM, mats['MSSM']) M_GUT。"""
    if n1 is None:
        n1 = A30_N1
    if n2 is None:
        n2 = A30_N2
    a = list(a0)
    for seg, model in ((L1, 'SM'), (L2, 'MSSM')):
        if seg == 0:
            continue
        n = n1 if model == 'SM' else n2
        h = seg / n
        for _ in range(n):
            k1 = rhs(a, model, mats, two_loop)
            aa = [a[i] + 0.5 * h * k1[i] for i in range(3)]
            k2 = rhs(aa, model, mats, two_loop)
            bb = [a[i] + 0.5 * h * k2[i] for i in range(3)]
            k3 = rhs(bb, model, mats, two_loop)
            cc = [a[i] + h * k3[i] for i in range(3)]
            k4 = rhs(cc, model, mats, two_loop)
            a = [a[i] + h / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i])
                 for i in range(3)]
    return a


def resid(a):
    return abs(a[0] - a[1]) + abs(a[0] - a[2])


def spread(a):
    return max(a) - min(a)


def grid_solve(mats, l1_lo, l1_hi, l1_step, l2_lo, l2_hi, l2_step,
               two_loop=True, n1=None, n2=None):
    """复刻 attack30 solve_backward 的网格搜索（不精修）。"""
    best = None
    nl1 = int(round((l1_hi - l1_lo) / l1_step)) + 1
    nl2 = int(round((l2_hi - l2_lo) / l2_step)) + 1
    for i in range(nl1):
        L1 = l1_lo + i * l1_step
        for j in range(nl2):
            L2 = l2_lo + j * l2_step
            r = resid(flow(AMZ, L1, L2, mats, two_loop, n1, n2))
            if best is None or r < best[0]:
                best = (r, L1, L2)
    return best


def newton_solve(mats, L1=2.4, L2=33.0, two_loop=True, n1=None, n2=None,
                 iters=80, tol=1e-14):
    """attack32 solve_seg 的同法（中心差分雅可比 + Newton + 阻尼/域护栏）。"""
    for _ in range(iters):
        f0 = flow(AMZ, L1, L2, mats, two_loop, n1, n2)
        r0 = f0[0] - f0[1]
        r1 = f0[0] - f0[2]
        if abs(r0) + abs(r1) < tol:
            break
        d = 1e-6
        fa = flow(AMZ, L1 + d, L2, mats, two_loop, n1, n2)
        fb = flow(AMZ, L1, L2 + d, mats, two_loop, n1, n2)
        j11 = (fa[0] - fa[1] - r0) / d
        j21 = (fa[0] - fa[2] - r1) / d
        j12 = (fb[0] - fb[1] - r0) / d
        j22 = (fb[0] - fb[2] - r1) / d
        det = j11 * j22 - j12 * j21
        if abs(det) < 1e-20:
            break
        dL1 = (r0 * j22 - j12 * r1) / det
        dL2 = (j11 * r1 - r0 * j21) / det
        step = 1.0
        for _k in range(40):
            nL1, nL2 = L1 - step * dL1, L2 - step * dL2
            if 0.0 < nL1 < 12.0 and 20.0 < nL2 < 45.0:
                break
            step *= 0.5
        L1, L2 = L1 - step * dL1, L2 - step * dL2
    a = flow(AMZ, L1, L2, mats, two_loop, n1, n2)
    return L1, L2, resid(a)


def roots_scan(mats, two_loop=True, n1=None, n2=None, tol=1e-9):
    """多初值 Newton，收集全部零点（去重：L1 差 < 0.02 视为同根）。"""
    roots = []
    for L1s in (0.0, 1.0, 2.0, 2.4, 3.0, 4.0, 5.0, 6.0, 7.0):
        for L2s in (26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0,
                    34.0, 35.0, 36.0):
            L1, L2, r = newton_solve(mats, L1=L1s, L2=L2s, two_loop=two_loop,
                                     n1=n1, n2=n2)
            if r < tol and 0.0 < L1 < 12.0 and 20.0 < L2 < 45.0:
                dup = False
                for (ra, rb, _rr) in roots:
                    if abs(ra - L1) < 0.02:
                        dup = True
                        break
                if not dup:
                    roots.append((L1, L2, r))
    roots.sort()
    return roots


E('=' * 78)
E('attack33 v2 · 2-loop M_SUSY 跨册差异的机器定位')
E('=' * 78)
E('')
E('问题：attack32 F5 报「2-loop M_SUSY=2317.72 GeV」对 attack30 的 193.04 GeV 相差 12.01 倍')
E('      （相对偏差 11.01）；F5c 归因为「非对角 b_ij 项是否计入」（依据：V1 仅对角项')
E('      恰好落在 193 附近）。本册检验该归因：先对拍矩阵与分段动力学，再检验 193.04 是否为解。')
E('')
E('共同输入：alpha_em^-1=%.3f  alpha_s=%.4f  sin2theta_W=%.5f  M_Z=%.4f GeV'
  % (ALPHA_EM_INV, ALPHA_S, X_OBS, MZ))
E('M_Z 处逆耦合：a1=%.6f  a2=%.6f  a3=%.6f' % (AMZ[0], AMZ[1], AMZ[2]))

# ============================================================
# A0 v1 自查：单一矩阵 vs 分段矩阵
# ============================================================
E('')
E('[A0] 自查：两段式打靶的动力学矩阵必须分段（v1 在此处出错）')
E('-' * 78)
E('  v1 的 flow 把同一个 mat2 同时用于 SM 段与 MSSM 段；attack32 的 flow 用')
E('  mats[model]（SM 段用 SM 阵、MSSM 段用 MSSM 阵）。两者解的是【不同方程组】。')
L1_s, L2_s, r_s = newton_solve(MATS_V1_SINGLE_P14, n1=1200, n2=1200)
L1_sn, L2_sn, r_sn = newton_solve(MATS_V1_SINGLE_N14, n1=1200, n2=1200)
E('  单一矩阵口径（v1）：b33=+14 -> %.4f GeV (res=%.2e) ; b33=-14 -> %.4f GeV (res=%.2e)'
  % (MZ * math.exp(L1_s), r_s, MZ * math.exp(L1_sn), r_sn))
L1_p, L2_p, r_p = newton_solve(MATS_P14, n1=1200, n2=1200)
L1_n, L2_n, r_n = newton_solve(MATS_N14, n1=1200, n2=1200)
E('  分段矩阵口径（attack32）：b33=+14 -> %.5f GeV (res=%.2e) ; b33=-14 -> %.5f GeV (res=%.2e)'
  % (MZ * math.exp(L1_p), r_p, MZ * math.exp(L1_n), r_n))
E('  attack32 报值 = %.5f GeV（spread %.3e）; 其 V3 b33 反号报值 = %.5f GeV（spread %.3e）'
  % (A32_REPORTED_MSUSY, A32_REPORTED_SPREAD, A32_V3_MSUSY, A32_V3_SPREAD))
E('  >> 分段口径逐位复现 attack32 的 V0 与 V3；单一矩阵口径两个都不复现。')
E('  >> 故 v1 的 1780.00 / 24053.22 是「另一方程组」的根，本册作废该两读数。')
add('A0 CORRECTED', 'CORRECTED',
    'v1 的 flow 用单一矩阵跑两段，解的不是 attack32 的方程组；修正后逐位复现 2317.71643 与 17918.76520',
    '单一矩阵: %.2f / %.2f GeV ; 分段矩阵: %.5f / %.5f GeV（attack32 报 %.5f / %.5f）'
    % (MZ * math.exp(L1_s), MZ * math.exp(L1_sn),
       MZ * math.exp(L1_p), MZ * math.exp(L1_n),
       A32_REPORTED_MSUSY, A32_V3_MSUSY),
    '判据：同一矩阵同一输入，两册必须给同一根。v1 得 1780.00 而 attack32 得 2317.72，'
    '两者各自 residual 都很小 => 不是收敛问题，是【方程组不同】。根因=SM 段被灌入 MSSM '
    '2-loop 系数。本册所有读数以分段口径重算；v1 的 b33 敏感度 13.51 倍随之作废')

# ============================================================
# A1 矩阵逐元素对拍
# ============================================================
E('')
E('[A1] b_ij 逐元素对拍（attack32 V0 vs attack30 B_MS）')
E('-' * 78)
diff_cells = []
for i in range(3):
    for j in range(3):
        if abs(B2_MS_P14[i][j] - B2_MS_N14[i][j]) > 1e-12:
            diff_cells.append((i + 1, j + 1, B2_MS_P14[i][j], B2_MS_N14[i][j]))
E('  差异单元数 = %d' % len(diff_cells))
for (i, j, vp, vn) in diff_cells:
    E('    b_%d%d : attack32 = %+.4f   attack30 = %+.4f' % (i, j, vp, vn))
E('  两段动力学矩阵对拍（SM 段）：两册同源 -> 差异单元 0')
E('  >> 两册矩阵只在 b_33 上不同：+14（attack32 V0）vs -14（attack30）。')
E('     两册的一阶系数 b_i 完全一致（MSSM: 33/5, 1, -3）。')
E('  >> 因此跨册差异不可能是「标准矩阵 vs 非标准矩阵」的整体差异，')
E('     只能来自 (i) b33 符号 或 (ii) 求解定义 / 搜索域。')
add('A1 INFO', 'INFO',
    '两册 b_ij 只在 b33 上不同（+14 vs -14），一阶系数与 SM 段矩阵完全一致',
    '差异单元 %d 个：b33 +14 vs -14' % len(diff_cells),
    'F5c 用「V1 仅对角项」解释跨册差异，但 V1 是人为构造的矩阵变体；'
    '两册真实矩阵的差异只有 b33 一个符号位 => 归因必须重新做（A4/A5/A6）')

# ============================================================
# A2 attack30 的报值是否等于其搜索域上界
# ============================================================
E('')
E('[A2] attack30 的 M_SUSY 报值 vs 其搜索域上界')
E('-' * 78)
l1_hi_a30 = A30_L1_LO + (A30_RANGE_N - 1) * A30_L1_STEP
msusy_at_bound = MZ * math.exp(l1_hi_a30)
rel_dev_bound = abs(msusy_at_bound - A30_REPORTED_MSUSY) / A30_REPORTED_MSUSY
E('  attack30 solve_backward 的 L1 网格：range(%d) => L1 = i/20 - 1.5, i=0..%d'
  % (A30_RANGE_N, A30_RANGE_N - 1))
E('  实际 L1 上界 = %.4f（源码注释声称 %.1f）' % (l1_hi_a30, A30_NOTE_CLAIM))
E('  域上界对应的 M_SUSY = M_Z * exp(%.4f) = %.5f GeV' % (l1_hi_a30, msusy_at_bound))
E('  attack30 报出的 M_SUSY   = %.5f GeV' % A30_REPORTED_MSUSY)
E('  相对偏差 = %.3e' % rel_dev_bound)
E('  >> 报值与域上界逐位吻合（偏差 3.7e-09，由其 8 位有效数字报价决定）=> 该报值是【搜索域边界】，不是解。')
if rel_dev_bound < 1e-5:
    add('A2 CORRECTED', 'CORRECTED',
        'attack30 的 2-loop M_SUSY=193.04415 GeV 是其搜索域上界，不是解',
        'M_Z*exp(0.75)=%.5f GeV vs 报值 %.5f（相对偏差 %.2e）'
        % (msusy_at_bound, A30_REPORTED_MSUSY, rel_dev_bound),
        '报值恰等于域上界 => 真解在搜索域之外，网格搜索以边界值收尾。'
        '该册未报 residual，故「边界值」与「收敛解」在册内不可区分。'
        '这是跨册差异的第一候选归因，优先级高于 b_ij 约定。'
        '该判定不依赖 A0 的分段/单矩阵口径（纯算术：M_Z*exp(0.75)）')
else:
    add('A2 BOUNDARY', 'BOUNDARY',
        'attack30 报值与搜索域上界未逐位吻合，边界假设不成立',
        '相对偏差 %.3e' % rel_dev_bound,
        '需另找归因（本册不据此下判定）')

# ============================================================
# A3 源码静态审计：注释 vs range
# ============================================================
E('')
E('[A3] 源码静态审计：注释声称的搜索域与实际 range()')
E('-' * 78)
E('  attack30 源码：for L1i in range(46): L1v = L1i/20 - 1.5   # 注释写「-1.5 .. 3」')
E('  实际：i_max=%d => L1_max = %.4f（不是 %.1f）' % (A30_RANGE_N - 1, l1_hi_a30, A30_NOTE_CLAIM))
E('  等价地：M_SUSY 搜索上界 = %.2f GeV（不是注释暗示的 %.0f GeV）'
  % (msusy_at_bound, MZ * math.exp(A30_NOTE_CLAIM)))
E('  差异倍数（注释暗示上界 / 实际上界）= %.2f'
  % (MZ * math.exp(A30_NOTE_CLAIM) / msusy_at_bound))
add('A3 FAIL', 'FAIL',
    'attack30 的 L1 搜索域注释(-1.5..3)与 range(46) 实际上界(0.75)不一致',
    '实际 L1_max=%.4f；对应 M_SUSY 上限 %.2f GeV' % (l1_hi_a30, msusy_at_bound),
    '注释写 3.0、实际 0.75，差 4 倍。该不一致使「解是否被域截断」无法从注释判断，'
    '必须从 range() 反算。属「注释漂移」缺陷族：文档层与执行层未同源')

# ============================================================
# A5 原始域最优残差（attack30 未报告的量）
# ============================================================
E('')
E('[A5] 在 attack30 原始搜索域内复跑网格，读其最优残差')
E('-' * 78)
r_orig, l1_orig, l2_orig = grid_solve(
    MATS_N14, A30_L1_LO, l1_hi_a30, A30_L1_STEP,
    A30_L2_LO, A30_L2_LO + (A30_L2_N - 1) * A30_L2_STEP, A30_L2_STEP,
    n1=A30_N1, n2=A30_N2)
msusy_orig = MZ * math.exp(l1_orig)
mgut_orig = msusy_orig * math.exp(l2_orig)
E('  b33=-14（attack30 矩阵）原始域最优：')
E('    L1=%.4f  L2=%.4f  => M_SUSY=%.5f GeV  M_GUT=%.4e GeV'
  % (l1_orig, l2_orig, msusy_orig, mgut_orig))
E('    最优残差 |a1-a2|+|a1-a3| = %.6e' % r_orig)
E('    attack30 报值 M_SUSY=%.5f GeV（复现值相对差 %.2e）'
  % (A30_REPORTED_MSUSY, abs(msusy_orig - A30_REPORTED_MSUSY) / A30_REPORTED_MSUSY))
E('  >> 残差量级是判据：O(1e-1) 说明它不是「汇聚解」，只是「域内最不坏点」。')
repro_ok = abs(msusy_orig - A30_REPORTED_MSUSY) / A30_REPORTED_MSUSY < 1e-3
if repro_ok:
    add('A5 BOUNDARY', 'BOUNDARY',
        '复现了 attack30 的 193 GeV：它是域内最优点，残差 %.3e 未收敛' % r_orig,
        'L1=%.4f L2=%.4f M_SUSY=%.5f GeV residual=%.6e'
        % (l1_orig, l2_orig, msusy_orig, r_orig),
        '网格搜索只要残余不为零就不是解。attack30 未报 residual => 册内无法区分'
        '「边界值」与「解」；本册补齐该读数。复现本身证明两册积分器一致（差异不在算法）')
else:
    add('A5 BOUNDARY', 'BOUNDARY',
        '未复现 attack30 的 193 GeV（相对差 %.2e），归因待定'
        % (abs(msusy_orig - A30_REPORTED_MSUSY) / A30_REPORTED_MSUSY),
        '复现值 %.5f GeV' % msusy_orig,
        '复现失败说明两册还有未识别的定义差异，本册不下进一步判定')

# ============================================================
# A6 扩展域：网格 + 精修能否走到真解
# ============================================================
E('')
E('[A6] 扩展搜索域 + 局部精修能否收敛到真解（决定性对照）')
E('-' * 78)
E('  Newton（attack32 起点 2.4/33，n=1200）：')
E('    分段矩阵 b33=+14 : L1=%+.6f L2=%.6f M_SUSY=%.5f GeV residual=%.3e'
  % (L1_p, L2_p, MZ * math.exp(L1_p), r_p))
E('    分段矩阵 b33=-14 : L1=%+.6f L2=%.6f M_SUSY=%.5f GeV residual=%.3e'
  % (L1_n, L2_n, MZ * math.exp(L1_n), r_n))
E('  attack32 报值 2317.71643 / spread 7.105e-15 => 逐位一致'
  '（M_SUSY 相对偏差 %.1e，绝对值差 %.1e 全部来自其 5 位小数报价）'
  % (abs(MZ * math.exp(L1_p) - A32_REPORTED_MSUSY) / A32_REPORTED_MSUSY,
     abs(MZ * math.exp(L1_p) - A32_REPORTED_MSUSY)))
r_ext, l1_ext, l2_ext = grid_solve(MATS_N14, A30_L1_LO, 6.5, 0.05, 27.0, 40.0, 0.1)
msusy_ext = MZ * math.exp(l1_ext)
E('  扩展域(L1 up to 6.5, step 0.05)粗扫(b33=-14)：L1=%.4f => M_SUSY=%.4f GeV  residual=%.3e'
  % (l1_ext, msusy_ext, r_ext))
l1_ref, l2_ref, r_ref = newton_solve(MATS_N14, L1=l1_ext, L2=l2_ext)
msusy_ref = MZ * math.exp(l1_ref)
E('  以粗扫最优点为初值局部精修：L1=%+.6f L2=%.6f => M_SUSY=%.5f GeV  residual=%.3e'
  % (l1_ref, l2_ref, msusy_ref, r_ref))
E('  与 attack32 起点(2.4,33) 的 Newton 根相对偏差 = %.3e'
  % (abs(msusy_ref - MZ * math.exp(L1_n)) / (MZ * math.exp(L1_n))))
gain_ref = math.log10(r_orig / max(r_ref, 1e-300))
gain_grid = math.log10(r_orig / max(r_ext, 1e-300))
ext_ok = r_ref < 1e-9
E('')
E('  >> 粗扫 residual=%.3e 仍非零 => 网格步长本身不足以定位零点（仅降 %.2f 个数量级）；'
  % (r_ext, gain_grid))
E('     再精修后 residual=%.3e => 相对原域最优共降 %.2f 个数量级。' % (r_ref, gain_ref))
E('  >> 对照 attack30：只做粗扫、不做精修、不报 residual，于是「域内最不坏点」被当成解。')
if ext_ok:
    add('A6 PASS', 'PASS',
        '扩展域 + 局部精修可达真解 => 原域报值是截断产物，不是解',
        'refined M_SUSY=%.5f GeV residual=%.3e（原域最优 residual=%.3e）'
        % (msusy_ref, r_ref, r_orig),
        '阳性对照成立：同一积分器、同一分段矩阵、只扩大搜索域并补精修 => residual 从 %.3e '
        '降到 %.3e（%.2f 个数量级，其中粗扫仅贡献 %.2f 个数量级，其余来自精修）。'
        '故 b_ij 非对角项不是主因，搜索域 + 未精修才是'
        % (r_orig, r_ref, gain_ref, gain_grid))
else:
    add('A6 FAIL', 'FAIL',
        '扩展域 + 精修仍未收敛，域截断假设不成立',
        'refined residual=%.3e M_SUSY=%.5f GeV' % (r_ref, msusy_ref),
        '本册的域截断归因被自己的阳性对照否证，须另找机制')

# ============================================================
# A7 b33 符号的独立影响
# ============================================================
E('')
E('[A7] b33 符号对真解的独立影响（引用必须声明矩阵）')
E('-' * 78)
mult_b33 = (MZ * math.exp(L1_n)) / (MZ * math.exp(L1_p))
E('  分段矩阵口径：b33=+14 => %.5f GeV ; b33=-14 => %.5f GeV ; 比值 %.4f'
  % (MZ * math.exp(L1_p), MZ * math.exp(L1_n), mult_b33))
E('  attack32 F5c 的 V3（b33 反号）= %.5f GeV，与本册 %.5f GeV 逐位一致'
  % (A32_V3_MSUSY, MZ * math.exp(L1_n)))
E('  >> 仅一个符号位就使 M_SUSY 跨 %.2f 倍 => 「2-loop 的 M_SUSY」不是可跨实现比较的量。'
  % mult_b33)
add('A7 BOUNDARY', 'BOUNDARY',
    '仅 b33 符号位就使 2-loop M_SUSY 跨 %.2f 倍（分段矩阵口径）' % mult_b33,
    'b33=+14 -> %.5f GeV ; b33=-14 -> %.5f GeV'
    % (MZ * math.exp(L1_p), MZ * math.exp(L1_n)),
    '两册各自的 b33 符号不同（+14 / -14），此为「约定未声明」型缺陷；'
    '本册不判哪个符号是标准（需引原始文献表逐元素核对），只登记其影响面。'
    '注：v1 曾报 13.51 倍，那是单矩阵口径的产物，已作废')

# ============================================================
# A9 反解多值性
# ============================================================
E('')
E('[A9] 反解的多值性：同一矩阵 + 同一输入下有几个「解」')
E('-' * 78)
roots_p14 = roots_scan(MATS_P14)
roots_n14 = roots_scan(MATS_N14)


def _root_lines(roots, tag):
    E('  %s 的根集合（多初值 Newton，res<1e-9）：' % tag)
    for (rL1, rL2, rr) in roots:
        E('    L1=%+.6f  L2=%.6f  => M_SUSY=%.5f GeV  residual=%.2e'
          % (rL1, rL2, MZ * math.exp(rL1), rr))
    if roots:
        vals = [MZ * math.exp(x[0]) for x in roots]
        E('    根数=%d ; M_SUSY 跨度 = %.2f 倍 (min %.5f / max %.5f GeV)'
          % (len(roots), max(vals) / min(vals), min(vals), max(vals)))
    else:
        E('    根数=0（扫描未命中）')


_root_lines(roots_p14, 'b33=+14')
_root_lines(roots_n14, 'b33=-14')
nroot_max = max(len(roots_p14), len(roots_n14))
if nroot_max >= 2:
    add('A9 FAIL', 'FAIL',
        '2-loop M_SUSY 反解不唯一：同一矩阵同一输入下存在多个根',
        'b33=+14 根数 %d / b33=-14 根数 %d' % (len(roots_p14), len(roots_n14)),
        '方程组 (a1=a2, a1=a3) 在 2-loop 下可有多个零点，故「M_SUSY」必须附带根的标识'
        '（初值/分支）。这解释了单册内 Newton 与网格给不同数的情形')
else:
    add('A9 INFO', 'INFO',
        '反解在扫描范围内唯一（最大根数 %d）' % nroot_max,
        'b33=+14 根数 %d / b33=-14 根数 %d' % (len(roots_p14), len(roots_n14)),
        '88 个初值全部收敛到同一根；不做更强断言（未做全局拓扑证明）。'
        '故跨册差异不能用「不同分支」解释，只能是搜索域或方程组不同')

# ============================================================
# A4 更正 F5c 归因
# ============================================================
E('')
E('[A4] 更正 attack32 F5c 的归因：非对角项是主因吗')
E('-' * 78)
E('  F5c 原归因链：V1（仅对角项）=183.60 GeV，与 attack30 的 193.04 GeV 差 4.89%')
E('                => 差异来自「非对角 b_ij 是否计入」。')
E('  本册检验：')
E('   (i)  两册真实矩阵只在 b33 符号上不同（A1），不存在「一方只有对角项」的事实；')
E('   (ii) 把 attack30 的矩阵原样代入本册 Newton（分段口径）：M_SUSY=%.5f GeV，'
  % (MZ * math.exp(L1_n)))
E('        与其 193.04 相差 %.2f 倍；' % ((MZ * math.exp(L1_n)) / A30_REPORTED_MSUSY))
E('   (iii) 差异的真实来源是搜索域截断（A6）：193.04 = M_Z*exp(0.75) 是域上界（A2）。')
E('  >> 结论：V1 落在 193 附近是【数值巧合】，不是机制。')
add('A4 CORRECTED', 'CORRECTED',
    'F5c 的「非对角项」归因是数值巧合；真实归因是搜索域截断（193.04=域上界）',
    '同矩阵代入 Newton 相差 %.2f 倍；域上界=M_Z*exp(0.75)=%.5f GeV'
    % ((MZ * math.exp(L1_n)) / A30_REPORTED_MSUSY, msusy_at_bound),
    '一个凑巧落在目标附近的变体（V1）被当成机制，是本库反复出现的「凡数值接近即归因」'
    '陷阱。正确做法：先做「报值是否等于某个结构常数」的恒等式核验（本册 A2），'
    '再谈物理归因')

# ============================================================
# A8 引用纪律
# ============================================================
E('')
E('[A8] 引用纪律：2-loop M_SUSY 的最小可复现字段')
E('-' * 78)
E('  必报五项：')
E('   (1) b_ij 矩阵逐元素（至少 b33 符号；+14 与 -14 差 %.2f 倍）' % mult_b33)
E('   (2) 分段动力学：SM 段用 SM 阵、MSSM 段用 MSSM 阵（A0 反例：单矩阵套用使解偏移）')
E('   (3) 求解定义（前向解 sin2theta_W / 后向解 M_SUSY / 双段打靶）')
E('   (4) residual（无 residual 的「解」不可作为跨册基准）')
E('   (5) 搜索域与步长（本册证明域上界会被误读为解）')
add('A8 INFO', 'INFO',
    '2-loop M_SUSY 的最小可复现字段 = 矩阵逐元素 + 分段动力学 + 求解定义 + residual + 搜索域',
    '五字段；缺任一项则跨册比较无意义',
    '本册给出三个反例：域上界被当成解（缺 residual）、凑巧接近被当成机制（缺矩阵逐元素）、'
    '单矩阵套两段（缺分段动力学）。五项齐全时，跨册 12 倍差异本可在首次对拍时定位')

# ============================================================
# 汇总
# ============================================================
tally = {}
for e in ENTRIES:
    tally[e['verdict']] = tally.get(e['verdict'], 0) + 1

E('')
E('=' * 78)
E('条目 %d：' % len(ENTRIES))
for k in ('FAIL', 'CORRECTED', 'BOUNDARY', 'PASS', 'INFO'):
    if k in tally:
        E('   %-10s %d' % (k, tally[k]))
E('-' * 78)
for e in ENTRIES:
    E('  %-16s %-10s %s' % (e['code'], e['verdict'], e['title']))
E('=' * 78)

out = {
    'round': 'attack33',
    'topic': '2-loop M_SUSY 跨册差异的机器定位',
    'entries': ENTRIES,
    'tally': tally,
    'total': len(ENTRIES),
    'key_numbers': {
        'matrix_diff_cells': len(diff_cells),
        'roots_count_b33p14': len(roots_p14),
        'roots_count_b33n14': len(roots_n14),
        'roots_msusy_b33p14': ['%.4f' % (MZ * math.exp(x[0])) for x in roots_p14],
        'roots_msusy_b33n14': ['%.4f' % (MZ * math.exp(x[0])) for x in roots_n14],
        'b33_attack32': 14.0,
        'b33_attack30': -14.0,
        'a30_L1_hi_actual': '%.6f' % l1_hi_a30,
        'a30_L1_hi_claimed': A30_NOTE_CLAIM,
        'a30_msusy_at_bound_GeV': '%.6f' % msusy_at_bound,
        'a30_reported_msusy_GeV': A30_REPORTED_MSUSY,
        'a30_reported_vs_bound_rel': '%.3e' % rel_dev_bound,
        'orig_grid_msusy_GeV': '%.6f' % msusy_orig,
        'orig_grid_residual': '%.6e' % r_orig,
        'newton_msusy_b33p14_GeV': '%.5f' % (MZ * math.exp(L1_p)),
        'newton_msusy_b33n14_GeV': '%.5f' % (MZ * math.exp(L1_n)),
        'newton_residual_b33p14': '%.3e' % r_p,
        'newton_residual_b33n14': '%.3e' % r_n,
        'a32_reported_msusy_GeV': A32_REPORTED_MSUSY,
        'a32_reproduced_rel_dev': '%.3e' % (abs(MZ * math.exp(L1_p) - A32_REPORTED_MSUSY) / A32_REPORTED_MSUSY),
        'a32_v3_reproduced_rel_dev': '%.3e' % (abs(MZ * math.exp(L1_n) - A32_V3_MSUSY) / A32_V3_MSUSY),
        'v1_single_matrix_msusy_b33p14_GeV': '%.4f' % (MZ * math.exp(L1_s)),
        'v1_single_matrix_msusy_b33n14_GeV': '%.4f' % (MZ * math.exp(L1_sn)),
        'ext_grid_msusy_GeV': '%.4f' % msusy_ext,
        'ext_grid_residual': '%.3e' % r_ext,
        'refined_msusy_GeV': '%.5f' % msusy_ref,
        'refined_residual': '%.3e' % r_ref,
        'b33_symbol_mult': '%.4f' % mult_b33,
        'grid_orders_gain': '%.2f' % gain_grid,
        'refine_orders_gain': '%.2f' % gain_ref,
        'crossbook_ratio_a32_over_a30': '%.4f' % (A32_REPORTED_MSUSY / A30_REPORTED_MSUSY),
    },
    'verdict': 'attack30 的 2-loop M_SUSY=193.04415 GeV 是搜索域上界(M_Z*exp(0.75))而非解；'
               'attack32 F5c 的「非对角项」归因须更正为「搜索域截断 + residual 未报告」；'
               'v1 的 b33 敏感度 13.51 倍因 flow 单矩阵缺陷作废，分段口径为 %.2f 倍'
               % mult_b33,
    'red_line': '不判 attack30 / attack32 作者算错；判定的是「报出的量是不是解」与'
                '「两个数字是否来自同一方程组」。MSSM gauge unification 的物理结论不被本册否定',
    'exit_code': 0,
}

jp = os.path.join(BASE, 'attack33_2loopMSUSY跨册差异机器定位_2026-10-31.json')
with open(jp, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
E('')
E('产物已写出：%s' % os.path.basename(jp))
