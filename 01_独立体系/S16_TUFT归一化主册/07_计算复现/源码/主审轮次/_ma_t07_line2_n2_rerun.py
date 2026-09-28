# -*- coding: utf-8 -*-
"""_ma_t07_line2_n2_rerun.py — 审计降载复跑：仅 n=2 候选段（原模块函数原样复用）"""
import io, math, time
import importlib.util

spec = importlib.util.spec_from_file_location(
    't7l2', r'D:\a10\aikjx\code\my_lib\tuft_t07_line2_overtone_close.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

out = []
def o(s=''):
    out.append(str(s))
    print(s, flush=True)

t0 = time.time()
o('[audit-reduced] n=2 candidate only, plain s^beta peel, N=180/240/300/360 + Beyn refine')
ctr = complex(0.490, -0.410)
poles = {}
for N in (180, 240, 300, 360):
    hist = M.beyn_refine(N, ctr)
    w = hist[-1]
    poles[N] = w
    o('    N=%3d  w=% .12f %+.12fi' % (N, w.real, w.imag))
d1 = abs(poles[240]-poles[300]); d2 = abs(poles[300]-poles[360])
o('    |dw| N240-300=%.3e  N300-360=%.3e' % (d1, d2))
o('    -> ' + ('CONVERGED' if (d1<=1e-9 and d2<=1e-9) else 'OPEN: multi-pole'))
o('  wall time: %.1fs' % (time.time()-t0))

txt = '\n'.join(out) + '\n'
io.open(r'D:\a10\aikjx\code\my_lib\_ma_t07_line2_n2_rerun.txt', 'w', encoding='utf-8').write(txt)
print('[written] _ma_t07_line2_n2_rerun.txt')
