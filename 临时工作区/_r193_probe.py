# -*- coding: utf-8 -*-
from decimal import Decimal as D, getcontext
getcontext().prec = 60
pi = D("3.14159265358979323846264338327950288419716939937510582097494")
G = D("6.67430e-11")
c = D("2.99792458e8")
hbar = D("1.054571817e-34")
GMsun = D("1.3271244e20")
Rsun = D("6.957e8")
Msun = D("1.9885e30")
mp = D("1.67262192369e-27")
me = D("9.1093837015e-31")
kappa2 = 8*pi*G/c**4
print("kappa2_SI =", kappa2)
print("4piG =", 4*pi*G)
print("8piG =", 8*pi*G)
# toc doc formula m^2 c^2/(hbar^2 kappa2)
for name, m in (("p", mp), ("e", me)):
    val = m*m*c*c/(hbar*hbar*kappa2)
    print("doc_formula[%s] = %s kg/m3" % (name, val))
# correct criterion: kappa2*(hbar n/2)^2 = m n c^2
n_t = 4*mp*c*c/(kappa2*hbar*hbar)
rho_t = mp*n_t
print("n_torsion =", n_t, " rho_torsion =", rho_t)
print("n_torsion / 1e52 =", n_t/D("1e52"))
# neutron star
rho_ns = D("5e17")
n_ns = rho_ns/mp
s_ns = hbar*n_ns/2
print("ns: n=%s  kappa2 s^2 = %s  rho=%s ratio=%s" % (n_ns, kappa2*s_ns*s_ns, rho_ns, kappa2*s_ns*s_ns/(rho_ns*c*c)))
# T threshold rho^{1/4}
import math
rho_t_f = float(rho_t)
gev4 = rho_t_f/2.085e35  # Pa -> GeV^4
print("rho_t Pa=", rho_t_f, " GeV^4=", gev4, " T_GeV=", gev4**0.25)
print("rho_P=", 5.155e96)
# mercury
a = D("5.7909e10"); e = D("0.205630")
per_orbit = 6*pi*GMsun/(a*(1-e*e)*c*c)
arcsec = per_orbit*D("206264.806247096355156473357330")
orb = D("36525")/D("87.969")
print("mercury per_orbit rad=", per_orbit, " arcsec=", arcsec, " orbits=", orb, " century=", arcsec*orb)
print("doc 415.2 ->", arcsec*D("415.2"))
# deflection
dth = 4*GMsun/(c*c*Rsun)
print("deflect rad=", dth, " arcsec=", dth*D("206264.806247096355156473357330"))
# rs sun
rs_sun = 2*GMsun/c**2
print("rs_sun m=", rs_sun, " km=", rs_sun/1000)
# M87*
M87 = D("6.5e9")*Msun
rs = 2*G*M87/c**2
print("M87 rs=", rs, " 1.2e13/rs=", D("1.2e13")/rs)
sqrt27 = D(27).sqrt()
print("sqrt27*rg=", sqrt27*rs/2, " 5.196rs=", D("5.196")*rs)
# shadow 42 uas at 16.8 Mpc
d = D("16.8")*D("3.0856775814913673e22")
ang = D("42e-6")/D("206264.806247096355156473357330")
size = ang*d
print("shadow m=", size, " /rs=", size/rs)
# GW150914
dE = D("3.1")*Msun*c*c
print("dE J=", dE, " vs 5.4e47 ratio=", dE/D("5.4e47"))
c5g = c**5/G
print("c5/G=", c5g, " 3.6e49 frac=", D("3.6e49")/c5g)
