# -*- coding: utf-8 -*-
"""_ma_shoot_probe.py — single-point match(w0) diagnosis + coarse scan"""
import numpy as np
import math
import sys, time
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib')
from _ma_tuft_shooting import match, VH, angular_sep_const

w0 = 0.37367168441804166 - 0.08896231568893410j
t0 = time.time()
mm = match(w0, 0.0, -2, 2, 2)
print("|match(w0)| = %.3e   (%.1f s)" % (abs(mm), time.time()-t0))

# coarse scan along real axis near w0
print("\nreal-axis scan  (imag fixed at -0.08896):")
for wr in np.linspace(0.30, 0.45, 16):
    w = complex(wr, w0.imag)
    mm = abs(match(w, 0.0, -2, 2, 2))
    print("  Re=%.3f: |match|=%.3e" % (wr, mm))

print("\nimag-axis scan  (real fixed at 0.37367):")
for wi in np.linspace(-0.12, -0.05, 15):
    w = complex(w0.real, wi)
    mm = abs(match(w, 0.0, -2, 2, 2))
    print("  Im=%.3f: |match|=%.3e" % (wi, mm))
