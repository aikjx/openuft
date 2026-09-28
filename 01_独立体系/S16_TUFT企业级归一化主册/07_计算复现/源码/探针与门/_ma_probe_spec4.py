# -*- coding: utf-8 -*-
"""_ma_probe_spec4.py — re-diagnose after A0 fix; scan det along real axis near pole"""
import numpy as np
import sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib')
import _ma_tuft_spin_spectral as m

w0 = 0.37367168441804166 - 0.08896231568893410j
NN = 60
b = complex(4.0, 0.5)

# sigma_min at true pole
M = m.assemble(w0, 0.0, -2, 2, 2, NN, b)
s_ = np.linalg.svd(M, compute_uv=False)
print('at w0: sigma_min=%.3e cond=%.2e' % (s_[-1], s_[0]/s_[-1]))

# scan real axis
for dw in (0.0, 0.01, 0.05, 0.1, 0.2):
    w = w0 + dw
    M = m.assemble(w, 0.0, -2, 2, 2, NN, b)
    s_ = np.linalg.svd(M, compute_uv=False)
    print('w=%+.3f: sigma_min=%.3e' % (dw, s_[-1]))
