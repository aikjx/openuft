# -*- coding: utf-8 -*-
"""R 曳力修正方向对比实验：R∝(1+z) vs R∝1/(1+z)，看哪个复现 Planck r_s(z*)=144.43 Mpc"""
import mpmath as mp
mp.mp.dps = 60
c = mp.mpf("2.99792458e8")
H0 = mp.mpf("67.36"); h = H0/100
Obh2 = mp.mpf("0.02237"); Och2 = mp.mpf("0.1200"); zstar = mp.mpf("1089.80")
Ogh2 = mp.mpf("2.4722e-5"); N_eff = mp.mpf("3.046"); Orh2 = Ogh2*(1+mp.mpf("0.2271")*N_eff)
Om = (Obh2+Och2)/h**2; Or = Orh2/h**2; Ol = 1-Om-Or
H0s = H0*1000/mp.mpf("3.085677581491367e22")
R0 = 3*Obh2/(4*Ogh2)
print("R0 = %.1f" % R0)
def rs(Rform):
    return c/H0s*mp.quad(lambda z: 1/mp.sqrt(3*(1+R0*(Rform(z))))/(mp.sqrt(Om*(1+z)**3+Or*(1+z)**4+Ol)), [0, zstar])
r_prop = rs(lambda z: 1+z)        # 脚本当前：R∝(1+z)
r_inv  = rs(lambda z: 1/(1+z))    # 标准推导：R∝1/(1+z)
print("R∝(1+z)   : r_s(z*) = %.4f Mpc" % (r_prop/mp.mpf("3.085677581491367e22")))
print("R∝1/(1+z) : r_s(z*) = %.4f Mpc" % (r_inv/mp.mpf("3.085677581491367e22")))
print("Planck 2018 口径：r_s(z*)≈144.4 Mpc（由 100θ*=1.0411 与 DM(z*)=13881 推得）；r_drag=147.09 Mpc")
