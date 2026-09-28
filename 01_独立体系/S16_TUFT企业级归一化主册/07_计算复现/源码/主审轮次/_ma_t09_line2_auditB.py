# -*- coding: utf-8 -*-
"""
MainAgent audit variant B for T09 Line 2 -- SINGLE-STAGE N=300 check.
The full 3-stage N=300 run was killed externally (exit -1, no traceback;
system healthy).  This variant verifies the N=300 pencil + Beyn numerics
with ONE stage (r=0.02, nc=300), which is stage 1 of the official staged
run.  Official stage-1 value: 0.569957933-0.287655042i (centre after stage1
in tuft_t09_line2_lowmem_svd_out.txt N=300 line).
"""
import time, gc
import tuft_t09_line2_lowmem_svd as M

t_start = time.time()
print("MA-AUDIT T09 LINE2 variant-B: n=1 N=300 single stage (r=0.02 nc=300)", flush=True)
Q0, Q1 = M.tuft_pencil(300)
w = M.beyn_pole(Q0, Q1, complex(0.570, -0.288), radius=0.02, nc=300)
print("    w=% .12f %+.12fi" % (w.real, w.imag), flush=True)
off = 0.569957933 - 0.287655042j
print("    official stage1 centre value ~ % .12f %+.12fi" % (off.real, off.imag), flush=True)
print("    |dw| vs official stage1 = %.3e" % abs(w - off), flush=True)
del Q0, Q1
gc.collect()
M.clear_cache()
print("wall time: %.1fs" % (time.time() - t_start), flush=True)
