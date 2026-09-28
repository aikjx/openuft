# -*- coding: utf-8 -*-
"""
MainAgent audit variant for T08 Line A (low-memory overtone closure).
Runs a MINIMAL subset of the official script's pipeline to verify
reproducibility on the local machine without the full ~100-min run:
  [2] n=0 sanity:  N=90/120/180
  [3] n=1:         N=180, N=240  (monotonic branch endpoints)
  [4] n=2:         N=180, N=240  (unlocalized endpoints)
Imports the official module (no main() side effects) and reuses its
functions verbatim.  Compares against official reference values.
"""
import time, gc
import tuft_t08_lineA_overtone_lowmem as M

t_start = time.time()
print("MA-AUDIT T08 LINE A minimal subset", flush=True)
print("b=%s BETA=%.9f" % (M.B_OPT, M.BETA), flush=True)

# ---- [2] n=0 sanity ------------------------------------------------
print("", flush=True)
print("[2] n=0 SANITY (N=90/120/180, plain s^beta, r=0.005 nc=300)", flush=True)
for N in (90, 120, 180):
    Q0, Q1 = M.tuft_pencil(N)
    w = M.beyn_pole(Q0, Q1, M.TUFT_ANCHOR, radius=0.005, nc=300)
    err = abs(w - M.TUFT_ANCHOR)
    print("    N=%-3d w=% .12f %+.12fi |err|=% .3e" % (N, w.real, w.imag, err), flush=True)
    del Q0, Q1
    gc.collect()

# ---- [3] n=1 endpoints ---------------------------------------------
print("", flush=True)
print("[3] n=1 (N=180, N=240) staged Beyn r=0.02/0.006/0.002 nc=300/500/700", flush=True)
M.clear_cache()
ctr1 = complex(0.570, -0.288)
n1 = {}
for N in (180, 240):
    tN = time.time()
    hist = M.beyn_lowmem(N, ctr1)
    n1[N] = hist[-1]
    print("    N=%3d w=% .12f %+.12fi (stage3; %6.1fs)" % (
        N, hist[-1].real, hist[-1].imag, time.time() - tN), flush=True)
    print("          stages: % .9f%+.9fi -> % .9f%+.9fi -> % .9f%+.9fi" % (
        hist[0].real, hist[0].imag, hist[1].real, hist[1].imag,
        hist[2].real, hist[2].imag), flush=True)
M.clear_cache()

# ---- [4] n=2 endpoints ---------------------------------------------
print("", flush=True)
print("[4] n=2 (N=180, N=240) staged Beyn r=0.02/0.006/0.002 nc=300/500/700", flush=True)
ctr2 = complex(0.490, -0.410)
n2 = {}
for N in (180, 240):
    tN = time.time()
    hist = M.beyn_lowmem(N, ctr2)
    n2[N] = hist[-1]
    print("    N=%3d w=% .12f %+.12fi (stage3; %6.1fs)" % (
        N, hist[-1].real, hist[-1].imag, time.time() - tN), flush=True)
    print("          stages: % .9f%+.9fi -> % .9f%+.9fi -> % .9f%+.9fi" % (
        hist[0].real, hist[0].imag, hist[1].real, hist[1].imag,
        hist[2].real, hist[2].imag), flush=True)
M.clear_cache()

# ---- comparison against official values ------------------------------
off = {
    "n0": {90: 0.434445176644 - 0.056449763641j,
           120: 0.434445176402 - 0.056449764441j,
           180: 0.434445176377 - 0.056449764526j},
    "n1": {180: 0.569959376313 - 0.287683421561j,
           240: 0.569958559840 - 0.287657668455j},
    "n2": {180: 0.499906955875 - 0.406567819775j,
           240: 0.496288359607 - 0.396115697374j},
}
print("", flush=True)
print("[CMP] deviation from official values:", flush=True)
ok = True
for key, d in off.items():
    for N, wv in d.items():
        if key == "n0":
            got = M.beyn_pole(*[None]) if False else None  # recompute below
            # recompute quickly: n0 already printed; recompute for rigor
            Q0, Q1 = M.tuft_pencil(N)
            g = M.beyn_pole(Q0, Q1, M.TUFT_ANCHOR, radius=0.005, nc=300)
            dev = abs(g - wv)
            print("    %s N=%3d |dw|=%.3e" % (key, N, dev), flush=True)
            ok = ok and dev < 1e-10
            del Q0, Q1
        else:
            dev = abs(n1[N] - wv) if key == "n1" else abs(n2[N] - wv)
            print("    %s N=%3d |dw|=%.3e" % (key, N, dev), flush=True)
            ok = ok and dev < 1e-10
print("", flush=True)
print("RESULT: %s" % ("MATCH (all |dw|<1e-10)" if ok else "MISMATCH"), flush=True)
print("wall time: %.1fs" % (time.time() - t_start), flush=True)
