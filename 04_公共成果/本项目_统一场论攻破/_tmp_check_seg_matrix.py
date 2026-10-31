# -*- coding: utf-8 -*-
# 临时核验 2：attack33 的 flow 用【单一矩阵】跑两段，
# attack32 的 flow 用【SM 阵跑 SM 段、MSSM 阵跑 MSSM 段】——是否为全部差异来源
import math
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

MZ = 91.1876
AEM = 1.0 / 127.916
AS = 0.1184
SW = 0.23122
A0 = [0.6 * (1.0 - SW) / AEM, SW / AEM, 1.0 / AS]
B1 = {'SM': [4.1, -19.0 / 6.0, -7.0], 'MSSM': [33.0 / 5.0, 1.0, -3.0]}
B2 = {'SM': [[199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0],
             [9.0 / 10.0, 35.0 / 6.0, 12.0],
             [11.0 / 10.0, 9.0 / 2.0, -26.0]],
      'MSSM': [[199.0 / 25.0, 27.0 / 5.0, 88.0 / 5.0],
               [9.0 / 5.0, 25.0, 24.0],
               [11.0 / 5.0, 9.0, 14.0]]}
B2['MSSM_n14'] = [list(r) for r in B2['MSSM']]
B2['MSSM_n14'][2][2] = -14.0
TP = 2.0 * math.pi
EP2 = 8.0 * math.pi ** 2


def rhs(a, model, mssm_key):
    b = B1[model]
    M = B2['SM'] if model == 'SM' else B2[mssm_key]
    return [-b[i] / TP - sum(M[i][j] / a[j] for j in range(3)) / EP2
            for i in range(3)]


def flow(a0, L1, L2, mssm_key, n=1200):
    a = list(a0)
    for seg, model in ((L1, 'SM'), (L2, 'MSSM')):
        if seg == 0:
            continue
        h = seg / n
        for _ in range(n):
            k1 = rhs(a, model, mssm_key)
            aa = [a[i] + 0.5 * h * k1[i] for i in range(3)]
            k2 = rhs(aa, model, mssm_key)
            bb = [a[i] + 0.5 * h * k2[i] for i in range(3)]
            k3 = rhs(bb, model, mssm_key)
            cc = [a[i] + h * k3[i] for i in range(3)]
            k4 = rhs(cc, model, mssm_key)
            a = [a[i] + h / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
                 for i in range(3)]
    return a


def metrics(L1, L2, key, n=1200):
    a = flow(A0, L1, L2, key, n)
    return max(a) - min(a), abs(a[0] - a[1]) + abs(a[0] - a[2]), sum(a) / 3.0


def newton(key, L1=2.4, L2=33.0, n=1200, iters=60):
    for _ in range(iters):
        f0 = flow(A0, L1, L2, key, n)
        r0, r1 = f0[0] - f0[1], f0[0] - f0[2]
        if abs(r0) + abs(r1) < 1e-13:
            break
        d = 1e-6
        fa = flow(A0, L1 + d, L2, key, n)
        fb = flow(A0, L1, L2 + d, key, n)
        j11 = (fa[0] - fa[1] - r0) / d
        j21 = (fa[0] - fa[2] - r1) / d
        j12 = (fb[0] - fb[1] - r0) / d
        j22 = (fb[0] - fb[2] - r1) / d
        det = j11 * j22 - j12 * j21
        if abs(det) < 1e-18:
            break
        dL1 = (r0 * j22 - j12 * r1) / det
        dL2 = (j11 * r1 - r0 * j21) / det
        L1 -= dL1
        L2 -= dL2
    return L1, L2


for key in ('MSSM', 'MSSM_n14'):
    L1, L2 = newton(key)
    sp, ab, ginv = metrics(L1, L2, key)
    print('%-10s L1=%+9.6f L2=%9.6f M_SUSY=%12.5f M_GUT=%.6e aGUT^-1=%.4f spread=%.3e |r1|+|r2|=%.3e'
          % (key, L1, L2, MZ * math.exp(L1), MZ * math.exp(L1 + L2), ginv, sp, ab))

print('')
print('对照：attack33 报值点（单矩阵口径）在【分段矩阵】口径下的残差')
for (L1, L2, tag) in ((2.971449, 29.591003, 'attack33 b33=+14'),
                      (3.235419, 29.204540, 'attack32 V0'),
                      (5.575, 26.1737, 'attack33 b33=-14')):
    sp, ab, ginv = metrics(L1, L2, 'MSSM')
    print('  %-18s spread=%.3e |r1|+|r2|=%.3e aGUT^-1=%.4f'
          % (tag, sp, ab, ginv))

print('')
print('b33=-14 用分段矩阵重新 Newton：')
L1, L2 = newton('MSSM_n14')
sp, ab, ginv = metrics(L1, L2, 'MSSM_n14')
print('  L1=%+9.6f L2=%9.6f M_SUSY=%12.5f M_GUT=%.6e aGUT^-1=%.4f spread=%.3e'
      % (L1, L2, MZ * math.exp(L1), MZ * math.exp(L1 + L2), ginv, sp))

print('')
print('attack30 原始域上界 L1=0.75 在【分段矩阵 + b33=-14】口径下的残差：')
best = None
for i in range(46):
    for j in range(71):
        L1 = -1.5 + i * 0.05
        L2 = 27.0 + j * 0.1
        sp, ab, _ = metrics(L1, L2, 'MSSM_n14', n=80)
        if best is None or ab < best[0]:
            best = (ab, L1, L2)
print('  最优 L1=%.4f L2=%.4f |r1|+|r2|=%.6e M_SUSY=%.5f'
      % (best[1], best[2], best[0], MZ * math.exp(best[1])))
