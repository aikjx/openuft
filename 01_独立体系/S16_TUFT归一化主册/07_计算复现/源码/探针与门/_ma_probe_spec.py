# -*- coding: utf-8 -*-
"""_ma_probe_spec.py — probe cheb indices and assemble matrix finite"""
import numpy as np
import sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib')
import _ma_tuft_spin_spectral as m

z, D, D2 = m.cheb_gauss(40)
print('N=40 argmin(z)=', np.argmin(z), 'z_min=%.10f' % z[np.argmin(z)])
print('N=40 argmax(z)=', np.argmax(z), 'z_max=%.10f' % z[np.argmax(z)])
w0 = 0.37367168441804166 - 0.08896231568893410j
M = m.assemble(w0, 0.0, -2, 2, 2, 40, complex(4.0, 0.5))
print('assemble ok, shape', M.shape, 'finite', np.all(np.isfinite(M)))
print('det sign check |M| =', abs(np.linalg.det(M)))
