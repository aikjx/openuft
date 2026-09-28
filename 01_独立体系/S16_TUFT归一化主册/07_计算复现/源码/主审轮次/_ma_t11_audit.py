# -*- coding: utf-8 -*-
"""MainAgent T11 audit variant: official-module minimal reruns.
Line1: n=0 complex-contour shooting |s_end|=40 t0=1e-4 vs official 0.428500140403-0.107029401762i
Line3: F-pencil N=480 Beyn vs official 0.434445176596-0.056449764639i (anchor reinforcement)
Writes _ma_t11_audit_out.txt.
"""
import importlib, time, io, gc

out_path = r'D:\a10\aikjx\code\my_lib\_ma_t11_audit_out.txt'
buf = io.StringIO()

def log(s=''):
    print(s)
    buf.write(s + '\n')

t0 = time.time()

# ---------------- Line 1: n=0 shooting |s_end|=40 ----------------
log('=' * 70)
log('T11 MA-AUDIT line1: n=0 complex-contour shooting |s_end|=40 t0=1e-4')
log('=' * 70)
L1 = importlib.import_module('tuft_t11_line1_complex_shooting')
t1 = time.time()
res = L1.run_n0('MA n=0 |s_end|=40 t0=1e-4', 40.0, 1e-4, complex(0.40, -0.09), half=0.07)
w1 = res['w']; r1 = res['res']; c1 = res['conv']
off1 = complex(0.428500140403, -0.107029401762)
log('official : 0.428500140403-0.107029401762i |R|=4.194e-11 conv=True')
log('local    : %.12f %+.12fi |R|=%.3e conv=%s  (wall %.1fs)' % (w1.real, w1.imag, r1, c1, time.time() - t1))
log('|dw|     : %.3e  MATCH=%s' % (abs(w1 - off1), 'YES' if abs(w1 - off1) < 1e-9 else 'NO'))

# ---------------- Line 3: F-pencil N=480 ----------------
log('')
log('=' * 70)
log('T11 MA-AUDIT line3: F-pencil N=480 Beyn vs extrap anchor')
log('=' * 70)
L3 = importlib.import_module('tuft_t11_line3_cross_validation')
# import the frob pencil builder from T10/T09 lineage if present in module
if hasattr(L3, 'tuft_pencil_frob'):
    t3 = time.time()
    Q0, Q1 = L3.tuft_pencil_frob(480)
    w3 = L3.beyn_pole(Q0, Q1, complex(0.434445176207, -0.056449764436), radius=0.005, nc=200)
    del Q0, Q1; gc.collect()
    off3 = complex(0.434445176596, -0.056449764639)
    log('official N=480 : 0.434445176596-0.056449764639i |w480-extrap|=4.387e-10')
    log('local   N=480 : %.12f %+.12fi' % (w3.real, w3.imag))
    log('|dw| vs official: %.3e  (wall %.1fs)' % (abs(w3 - off3), time.time() - t3))
    log('|w480-extrap.anchor| : %.3e' % abs(w3 - complex(0.434445176207, -0.056449764436)))
    log('MATCH          : %s' % ('YES' if abs(w3 - off3) < 1e-12 else 'NO'))
else:
    log('L3 has no tuft_pencil_frob attr -- fallback import from T10 module')
    L10 = importlib.import_module('tuft_t10_line2_frobenius_overtone')
    t3 = time.time()
    Q0, Q1 = L10.tuft_pencil_frob(480)
    w3 = L10.beyn_pole(Q0, Q1, complex(0.434445176207, -0.056449764436), radius=0.005, nc=200)
    del Q0, Q1; gc.collect()
    off3 = complex(0.434445176596, -0.056449764639)
    log('official N=480 : 0.434445176596-0.056449764639i')
    log('local   N=480 : %.12f %+.12fi' % (w3.real, w3.imag))
    log('|dw| vs official: %.3e  (wall %.1fs)' % (abs(w3 - off3), time.time() - t3))
    log('MATCH          : %s' % ('YES' if abs(w3 - off3) < 1e-12 else 'NO'))

log('')
log('total wall: %.1fs' % (time.time() - t0))
with io.open(out_path, 'w', encoding='utf-8', newline='') as f:
    f.write(buf.getvalue())
print('[written] %s' % out_path)
