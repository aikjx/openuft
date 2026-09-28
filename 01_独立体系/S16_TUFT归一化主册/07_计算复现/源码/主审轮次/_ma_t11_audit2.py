# -*- coding: utf-8 -*-
"""MainAgent T11 final audit variant.
Line1: n=0 shooting Sm=40 vs official 0.430352451005-0.100230156674i
Line2: n=1 shooting t=20 vs official 0.513402121318-0.285869774501i
Writes _ma_t11_audit2_out.txt.
"""
import importlib, time, io, gc

out_path = r'D:\a10\aikjx\code\my_lib\_ma_t11_audit2_out.txt'
buf = io.StringIO()

def log(s=''):
    print(s)
    buf.write(s + '\n')

t0 = time.time()

# ---------------- Line 1: n=0 shooting Sm=40 ----------------
log('=' * 70)
log('T11 MA-AUDIT2 line1: n=0 shooting Sm=40 (tail-fitted, final version)')
log('=' * 70)
L1 = importlib.import_module('tuft_t11_line1_complex_shooting')
# official root from out: 0.430352451005-0.100230156674i ; reproduce via resid_lead+scan+newton
t1 = time.time()
resid = lambda w: L1.resid_lead(w, 40.0)
seed, smin = L1.coarse_scan(resid, complex(0.40, -0.09), half=0.08, n=10)
w1, r1, it1, c1 = L1.complex_newton(resid, seed)
off1 = complex(0.430352451005, -0.100230156674)
log('official : 0.430352451005-0.100230156674i')
log('local    : %.12f %+.12fi |R|=%.3e iters=%d conv=%s (wall %.1fs)' % (w1.real, w1.imag, r1, it1, c1, time.time() - t1))
log('|dw|     : %.3e  MATCH=%s' % (abs(w1 - off1), 'YES' if abs(w1 - off1) < 1e-9 else 'NO'))

# ---------------- Line 2: n=1 shooting t=20 ----------------
log('')
log('=' * 70)
log('T11 MA-AUDIT2 line2: n=1 shooting t_match=20')
log('=' * 70)
L2 = importlib.import_module('tuft_t11_line2_n1_adjudication')
t2 = time.time()
try:
    ts_a, rhov_a, Vv_a = L2.build_traj(40.0)
    res2 = L2.run_overtone('MA n=1 t=20', complex(0.510, -0.288), 20.0, ts_a, Vv_a, half=0.08, s0_abs=0.02)
    w2 = res2['w']; r2 = res2['res']; c2 = res2['conv']
    off2 = complex(0.513402121318, -0.285869774501)
    log('official : 0.513402121318-0.285869774501i')
    log('local    : %.12f %+.12fi |R|=%.3e conv=%s (wall %.1fs)' % (w2.real, w2.imag, r2, c2, time.time() - t2))
    log('|dw|     : %.3e  MATCH=%s' % (abs(w2 - off2), 'YES' if abs(w2 - off2) < 1e-9 else 'NO'))
except Exception as e:
    log('line2 rerun failed: %s' % e)

log('')
log('total wall: %.1fs' % (time.time() - t0))
with io.open(out_path, 'w', encoding='utf-8', newline='') as f:
    f.write(buf.getvalue())
print('[written] %s' % out_path)
