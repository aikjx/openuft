# -*- coding: utf-8 -*-
"""r235 probe: cosmology numbers before writing the engine."""
import sys
from math import sqrt, pi, log10, exp, log

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

C = 2.99792458e8
G = 6.67430e-11
MPC = 3.0856775814913673e22
GYR = 3.15576e16  # s
KM = 1000.0

H0_KM = 67.4
H0 = H0_KM * KM / MPC
OM = 0.3153
OR = 9.15e-5
OL = 1.0 - OM - OR


def E_a(a):
    return sqrt(OM / a ** 3 + OR / a ** 4 + OL)


def E_z(z):
    return sqrt(OM * (1 + z) ** 3 + OR * (1 + z) ** 4 + OL)


def simpson(f, a, b, n):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n, 2):
        s += 4.0 * f(a + i * h)
    for i in range(2, n, 2):
        s += 2.0 * f(a + i * h)
    return s * h / 3.0


def t0():
    # a 积分（a→0 端 integrand ~ a/√Ωr，取 1e−10 下限，尾贡献 <1e−20）
    return simpson(lambda a: 1.0 / (a * E_a(a)), 1e-10, 1.0, 200000) / H0


def t0x():
    return simpson(lambda x: 1.0 / E_a(exp(-x)), 0.0, 30.0, 60000) / H0


def t_of_z(z):
    az = 1.0 / (1.0 + z)
    return simpson(lambda a: 1.0 / (a * E_a(a)), 1e-10, az, 100000) / H0


def dc(z):
    return C / H0 * simpson(lambda x: 1.0 / E_z(x), 0.0, z, 20000)


def dcx(z):
    L = log(1.0 + z)
    return C / H0 * simpson(lambda x: exp(x) / E_z(exp(x) - 1.0), 0.0, L, 20000)


print("H0_s=%.6e" % H0)
print("t0=%.6f Gyr  t0x=%.6f  rel=%.2e" % (t0() / GYR, t0x() / GYR, abs(t0() / t0x() - 1)))
print("t(z=1)=%.6f Gyr" % (t_of_z(1.0) / GYR))
q0 = 0.5 * OM - OL + OR
print("q0=%.9f" % q0)
print("Lambda=%.6e m^-2" % (3.0 * OL * H0 ** 2 / C ** 2))
rho_c = 3.0 * H0 ** 2 / (8.0 * pi * G)
print("rho_c=%.6e kg/m3  rhoL=%.6e  rhoL*c2=%.6e J/m3" % (rho_c, OL * rho_c, OL * rho_c * C ** 2))
for z in (0.001, 0.1, 0.5, 1.0, 2.0, 1100.0):
    D = dc(z)
    D2 = dcx(z)
    dL = (1 + z) * D
    mu = 5.0 * log10(dL / (10.0 * 3.0856775814913673e16))  # 10 pc in m
    print("z=%8.4f DC=%.6e Mpc (%.6f Gpc) rel2=%.2e dL=%.4f Mpc mu=%.4f"
          % (z, D / MPC, D / MPC / 1000.0, abs(D / D2 - 1), dL / MPC, mu))
print("DC(1100)/Gpc=%.6f" % (dc(1100.0) / MPC / 1000.0))
print("DC(1100)x/Gpc=%.6f" % (dcx(1100.0) / MPC / 1000.0))
Tcmb = 2.7255
print("Tcmb(z=1100)=%.4f K" % (Tcmb * 1101.0))

# --- S18 ---
H0s_KM = 70.0
H0s = H0s_KM * KM / MPC
rho0 = 8.27e-10
alpha = 1.87
rhoc_s = 1e-9
K = -3.0 * alpha * rho0 / (2.0 * rhoc_s)
print("\nS18 K=%.9f q=%.6f" % (K, 1.0 - K))
f_now = -3.0 * alpha / (2.0 * rhoc_s) * rho0 ** 2 / rho0
print("S18 f_now=%.9f q=%.9f" % (f_now, 1.0 - f_now))
H2s = H0s ** 2
print("S18 adotdot/a=%.6e H2=%.6e" % ((f_now - 1.0) * H2s, H2s))
R_ours = 6.0 * ((f_now - 1.0) * H2s + H2s) / C ** 2
R_gr = 8.0 * pi * G * rho0 / C ** 2
print("S18 R=%.6e  R_GR=%.6e  ratio=%.4e" % (R_ours, R_gr, R_ours / R_gr))


def E_s18_a(a):
    lnH = K / 3.0 * (1.0 - a ** -3) - 2.0 * log(a)
    if lnH > 700.0:
        return float("inf")
    return exp(lnH)


def t0_s18():
    return simpson(lambda a: 1.0 / (a * E_s18_a(a)), 1e-6, 1.0, 200000) / H0s


print("S18 age=%.6f Gyr (H0=70)  GR matter=%.6f" % (t0_s18() / GYR, (2.0 / (3.0 * H0s)) / GYR))


def E_s18_z(z):
    a = 1.0 / (1.0 + z)
    return E_s18_a(a)


def E_grm_z(z):
    return (1.0 + z) ** 1.5


def dc_s18(z):
    return C / H0s * simpson(lambda x: 1.0 / E_s18_z(x), 0.0, z, 40000)


def dc_grm(z):
    return C / H0s * simpson(lambda x: 1.0 / E_grm_z(x), 0.0, z, 40000)


zs = 1100.0
DA_s18 = dc_s18(zs) / (1.0 + zs)
DA_grm = dc_grm(zs) / (1.0 + zs)
print("S18 DC(1100)=%.4e Mpc  GR=%.4e Mpc  DA_ratio=%.6f" %
      (dc_s18(zs) / MPC, dc_grm(zs) / MPC, DA_s18 / DA_grm))

# --- Lambda channel ---
MS = 1.9885e30
Lam = 3.0 * OL * H0 ** 2 / C ** 2
print("\nLambda=%.6e" % Lam)
for name, M in (("Sun", MS), ("Earth", 5.972e24), ("MilkyWay", 1.0e11 * MS),
                ("Cluster", 1.0e15 * MS)):
    rstar = (3.0 * G * M / (Lam * C ** 2)) ** (1.0 / 3.0)
    print("%s r*=%.6e m = %.6f Mpc = %.3f pc" % (name, rstar, rstar / MPC, rstar / 3.0856775814913673e16))
r_1au = 1.495978707e11
ratio = Lam * C ** 2 * r_1au ** 3 / (3.0 * G * MS)
print("Sun 1AU ratio=%.6e" % ratio)
print("rhoP/rhoL=%.6e log10=%.4f" % ((C ** 5 / (1.054571817e-34 * G ** 2)) / (OL * rho_c), log10((C ** 5 / (1.054571817e-34 * G ** 2)) / (OL * rho_c))))
