# -*- coding: utf-8 -*-
"""
MainAgent audit variant for T09 Line 2 (low-memory N>=300 Beyn + SVD).
Runs the minimal high-value subset while the organizer's full run finishes:
  [1] n=0 sanity: N=90/120/180 (pipeline reproducibility vs T08)
  [2] n=1:        N=300 single staged Beyn (the key new point: T09 N=300 vs
                  T07 N=300 cross-pipeline agreement at 5.4e-10)
Imports the official module (no main() side effects), reuses functions
verbatim.  Compares against official values from tuft_t09_line2_lowmem_svd_out.txt.
"""
import time, gc
import tuft_t09_line2_lowmem_svd as M

t_start = time.time()
print("MA-AUDIT T09 LINE 2 minimal subset (n=0 sanity + n=1 N=300)", flush=True)
print("b=%s BETA=%.9f" % (M.B_OPT, M.BETA), flush=True)

# ---- [1] n=0 sanity ------------------------------------------------
print("", flush=True)
print("[1] n=0 SANITY (N=90/120/180, plain s^beta, r=0.005 nc=300)", flush=True)
n0 = {}
for N in (90, 120, 180):
    Q0, Q1 = M.tuft_pencil(N)
    w = M.beyn_pole(Q0, Q1, M.TUFT_ANCHOR, radius=0.005, nc=300)
    n0[N] = w
    print("    N=%-3d w=% .12f %+.12fi |err|=% .3e" % (N, w.real, w.imag, abs(w - M.TUFT_ANCHOR)), flush=True)
    del Q0, Q1
    gc.collect()
M.clear_cache()

# ---- [2] n=1 N=300 staged ------------------------------------------
print("", flush=True)
print("[2] n=1 N=300 staged Beyn r=0.02/0.006/0.002 nc=300/500/700", flush=True)
tN = time.time()
hist = M.beyn_lowmem(300, complex(0.570, -0.288))
w300 = hist[-1]
print("    N=300 w=% .12f %+.12fi (stage3; %6.1fs)" % (w300.real, w300.imag, time.time() - tN), flush=True)
print("          stages: % .9f%+.9fi -> % .9f%+.9fi -> % .9f%+.9fi" % (
    hist[0].real, hist[0].imag, hist[1].real, hist[1].imag,
    hist[2].real, hist[2].imag), flush=True)
M.clear_cache()

# ---- comparison -----------------------------------------------------
off_n0 = {90: 0.434445176644 - 0.056449763641j,
          120: 0.434445176402 - 0.056449764441j,
          180: 0.434445176377 - 0.056449764526j}
off_n1_300 = 0.569957939619 - 0.287655030300j
print("", flush=True)
print("[CMP] deviation from official values:", flush=True)
ok = True
for N, wv in off_n0.items():
    dev = abs(n0[N] - wv)
    print("    n0 N=%3d |dw|=%.3e" % (N, dev), flush=True)
    ok = ok and dev < 1e-10
dev1 = abs(w300 - off_n1_300)
print("    n1 N=300 |dw|=%.3e" % dev1, flush=True)
ok = ok and dev1 < 1e-9
print("", flush=True)
print("RESULT: %s" % ("MATCH" if ok else "MISMATCH"), flush=True)
print("wall time: %.1fs" % (time.time() - t_start), flush=True)
