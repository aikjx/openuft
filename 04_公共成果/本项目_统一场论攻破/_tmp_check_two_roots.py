# -*- coding: utf-8 -*-
# 临时核验：attack32 的 2317.72 与 attack33 的 1780.00 是否同为 b33=+14 的根
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
B2P14 = [[199.0 / 25.0, 27.0 / 5.0, 88.0 / 5.0],
         [9.0 / 5.0, 25.0, 24.0],
         [11.0 / 5.0, 9.0, 14.0]]
TP = 2.0 * math.pi
EP2 = 8.0 * math.pi ** 2


def rhs(a, model, M):
    b = B1[model]
    return [-b[i] / TP - sum(M[i][j] / a[j] for j in range(3)) / EP2
            for i in range(3)]


def flow(a0, L1, L2, M, n=1200):
    a = list(a0)
    for seg, model in ((L1, 'SM'), (L2, 'MSSM')):
        if seg == 0:
            continue
        h = seg / n
        for _ in range(n):
            k1 = rhs(a, model, M)
            aa = [a[i] + 0.5 * h * k1[i] for i in range(3)]
            k2 = rhs(aa, model, M)
            bb = [a[i] + 0.5 * h * k2[i] for i in range(3)]
            k3 = rhs(bb, model, M)
            cc = [a[i] + h * k3[i] for i in range(3)]
            k4 = rhs(cc, model, M)
            a = [a[i] + h / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
                 for i in range(3)]
    return a


def resid_at(L1, L2, M, n=1200):
    a = flow(A0, L1, L2, M, n)
    return abs(a[0] - a[1]) + abs(a[0] - a[2])


def newton_plain(L1=2.4, L2=33.0, M=B2P14, n=1200, iters=60):
    for _ in range(iters):
        f0 = flow(A0, L1, L2, M, n)
        r0, r1 = f0[0] - f0[1], f0[0] - f0[2]
        if abs(r0) + abs(r1) < 1e-13:
            break
        d = 1e-6
        fa = flow(A0, L1 + d, L2, M, n)
        fb = flow(A0, L1, L2 + d, M, n)
        j11 = (fa[0] - fa[1] - r0) / d
        j21 = (fa[0] - fa[2] - r1) / d
        j12 = (fb[0] - fb[1] - r0) / d
        j22 = (fb[0] - fb[2] - r1) / d
        det = j11 * j22 - j12 * j21
        if abs(det) < 1e-20:
            break
        dL1 = (r0 * j22 - j12 * r1) / det
        dL2 = (j11 * r1 - r0 * j21) / det
        L1 -= dL1
        L2 -= dL2
    a = flow(A0, L1, L2, M, n)
    return L1, L2, abs(a[0] - a[1]) + abs(a[0] - a[2])


print('A0 =', A0)
for (L1, L2, tag) in ((2.9714, 29.5910, 'attack33 报值'),
                      (3.235419, 29.204540, 'attack32 报值')):
    for n in (800, 1200, 2400, 4800):
        print('  %-14s L1=%.6f L2=%.6f n=%-5d resid=%.3e M_SUSY=%.4f'
              % (tag, L1, L2, n, resid_at(L1, L2, B2P14, n), MZ * math.exp(L1)))
print('')
print('attack32 式无阻尼 Newton（初值 2.4/33）：')
L1, L2, r = newton_plain()
print('  L1=%.6f L2=%.6f resid=%.3e M_SUSY=%.4f M_GUT=%.6e'
      % (L1, L2, r, MZ * math.exp(L1), MZ * math.exp(L1 + L2)))
print('')
print('多初值无阻尼 Newton 扫描（查是否存在第二根）：')
roots = []
for L1s in (0.0, 1.0, 2.0, 2.4, 3.0, 3.5, 4.0, 5.0, 6.0):
    for L2s in (26.0, 28.0, 30.0, 32.0, 33.0, 35.0, 37.0):
        L1, L2, r = newton_plain(L1s, L2s)
        if r < 1e-9 and 0.0 < L1 < 12.0 and 20.0 < L2 < 45.0:
            dup = any(abs(x[0] - L1) < 0.02 for x in roots)
            if not dup:
                roots.append((L1, L2, r, L1s, L2s))
roots.sort()
for (L1, L2, r, L1s, L2s) in roots:
    print('  root L1=%.6f L2=%.6f resid=%.2e M_SUSY=%.4f  (from %.1f/%.1f)'
          % (L1, L2, r, MZ * math.exp(L1), L1s, L2s))
print('  根数 =', len(roots))
