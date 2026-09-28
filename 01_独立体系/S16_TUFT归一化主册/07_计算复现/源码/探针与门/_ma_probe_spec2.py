# -*- coding: utf-8 -*-
"""_ma_probe_spec2.py — diagnose spectral matrix at true pole"""
import numpy as np
import sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib')
import _ma_tuft_spin_spectral as m

w0 = 0.37367168441804166 - 0.08896231568893410j
for NN in (40, 50, 60):
    M = m.assemble(w0, 0.0, -2, 2, 2, NN, complex(4.0, 0.5))
    s = np.linalg.svd(M, compute_uv=False)
    print('N=%d: sigma_min=%.3e  sigma_max=%.3e  cond=%.3e  |det|=%.3e' % (
        NN, s[-1], s[0], s[0]/s[-1], abs(np.linalg.det(M))))
    # 也看偏离点
    M2 = m.assemble(w0+0.01, 0.0, -2, 2, 2, NN, complex(4.0, 0.5))
    s2 = np.linalg.svd(M2, compute_uv=False)
    print('    off-pole: sigma_min=%.3e  |det|=%.3e' % (s2[-1], abs(np.linalg.det(M2))))
