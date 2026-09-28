# -*- coding: utf-8 -*-
"""MainAgent T10 audit variant: import official modules, minimal single-point reruns.
Line1: N=180 F-pencil + Beyn vs official 0.434445180747-0.056449766805i
Line2: Gate-A N=300 frob + Beyn vs official 0.434445177295-0.056449765004i (|w-W0_NEW|=4.447e-10)
Line3: n=0 Smatch=40 shooting vs official 0.411848556867+0.039242326370i
Writes _ma_t10_audit_out.txt (script self-written, no PowerShell BOM artifacts).
"""
import importlib, time, io, gc

out_path = r'D:\a10\aikjx\code\my_lib\_ma_t10_audit_out.txt'
buf = io.StringIO()

def log(s=''):
    print(s)
    buf.write(s + '\n')

t0 = time.time()

# ---------------- Line 1: N=180 single point ----------------
log('=' * 70)
log('T10 MA-AUDIT line1: N=180 F-pencil + Beyn single point')
log('=' * 70)
L1 = importlib.import_module('tuft_t10_line1_anchor_upgrade')
t1 = time.time()
Q0, Q1 = L1.tuft_pencil_frob(180)
w1 = L1.beyn_pole(Q0, Q1, L1.OLD_ANCHOR, radius=0.005, nc=250)
del Q0, Q1; gc.collect()
off1 = complex(0.434445180747, -0.056449766805)
log('official N=180 : 0.434445180747-0.056449766805i')
log('local   N=180 : %.12f %+.12fi' % (w1.real, w1.imag))
log('|dw|          : %.3e   (wall %.1fs)' % (abs(w1 - off1), time.time() - t1))
log('MATCH         : %s' % ('YES' if abs(w1 - off1) < 1e-12 else 'NO'))

# ---------------- Line 2: Gate-A N=300 single point ----------------
log('')
log('=' * 70)
log('T10 MA-AUDIT line2: Gate-A N=300 frob + Beyn single point')
log('=' * 70)
L2 = importlib.import_module('tuft_t10_line2_frobenius_overtone')
t2 = time.time()
Q0, Q1 = L2.tuft_pencil_frob(300)
w2 = L2.beyn_pole(Q0, Q1, L2.W0_NEW, radius=0.005, nc=250)
del Q0, Q1; gc.collect()
off2 = complex(0.434445177295, -0.056449765004)
log('official N=300 : 0.434445177295-0.056449765004i |w-W0_NEW|=4.447e-10')
log('local   N=300 : %.12f %+.12fi' % (w2.real, w2.imag))
log('|dw| vs official: %.3e   (wall %.1fs)' % (abs(w2 - off2), time.time() - t2))
log('|w-W0_NEW|     : %.3e' % abs(w2 - L2.W0_NEW))
log('MATCH          : %s' % ('YES' if abs(w2 - off2) < 1e-12 else 'NO'))

# ---------------- Line 3: n=0 Smatch=40 shooting ----------------
log('')
log('=' * 70)
log('T10 MA-AUDIT line3: n=0 Smatch=40 outward shooting single config')
log('=' * 70)
L3 = importlib.import_module('tuft_t10_line3_wkb_shooting')
t3 = time.time()
res = L3.run_overtone('MA n=0 (Smatch=40,s0=2e-2)', complex(0.40, -0.09),
                      Smatch=40.0, s0=2e-2, half=0.12)
w3 = res['w']
off3 = complex(0.411848556867, 0.039242326370)
log('official n=0   : 0.411848556867+0.039242326370i  |R|=7.194e-10 iters=8 conv=True')
log('local   n=0   : %.12f %+.12fi  |R|=%.3e  conv=%s  (wall %.1fs)' % (
    w3.real, w3.imag, res['res'], res['conv'], time.time() - t3))
log('|dw| vs official: %.3e' % abs(w3 - off3))
log('MATCH          : %s' % ('YES' if abs(w3 - off3) < 1e-9 else 'NO'))

log('')
log('total wall: %.1fs' % (time.time() - t0))
with io.open(out_path, 'w', encoding='utf-8', newline='') as f:
    f.write(buf.getvalue())
print('[written] %s' % out_path)
