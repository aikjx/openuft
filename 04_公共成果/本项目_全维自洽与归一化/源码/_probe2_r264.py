# -*- coding: utf-8 -*-
r"""r264 前置探测 2：真机复算 42.3 参数字典总表（8 粒子 x 8 量纲）与 44.3 定义式表"""
import io
import os
from decimal import Decimal as D, getcontext

getcontext().prec = 60

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
BOOK = r"D:\a10\aikjx\code\my_lib\TUFT_四力大统一_垂直原理螺旋统一场论_定稿全书.md"

HBARC = D("197.3269804")       # MeV fm
ALPHA = D("7.2973525693e-3")

# 42.3 表：粒子, m(MeV), kappa_A, tau_A, rho_A, b_A, R_c^A, omega/c, lambda
T423 = [
    ("e-", "0.51099895", "2.5895361e-3", "1.8896758e-5", "386.1489865",
     "2.8178653", "386.1695495", "2.5896051e-3", "386.1592678"),
    ("p", "938.27208816", "4.7549103", "3.46978e-2", "0.21030333",
     "1.5346576e-3", "0.21030386", "4.7549098", "0.21030389"),
    ("n", "939.5654205", "4.7481951", "3.46487e-2", "0.21001491",
     "1.53255e-3", "0.21001547", "4.7479947", "0.21001541"),
    ("pi+", "139.57039", "0.31969968", "2.33297e-3", "3.1251341",
     "2.28043e-2", "3.1279680", "0.31951116", "1.4138169"),
    ("pi0", "134.9768", "0.33056338", "2.41224e-3", "3.0218617",
     "2.20516e-2", "3.0246347", "0.33041480", "1.4619326"),
    ("W", "80377.0", "5.55073e-4", "4.05047e-6", "1.8004477e-2",
     "1.31388e-4", "1.8019279", "5.54905e-4", "2.4550180e-3"),
    ("Z", "91187.6", "4.89191e-4", "3.56998e-6", "2.0424790e-2",
     "1.49045e-4", "2.0442688", "4.89037e-4", "2.1639647e-3"),
    ("H", "125250.0", "3.56183e-4", "2.59922e-6", "2.8047607e-2",
     "2.04680e-4", "2.8075080", "3.56059e-4", "1.5754564e-3"),
]


def rel(a, b):
    if b == 0:
        return D(0) if a == 0 else D("1e99")
    return abs(a - b) / abs(b)


def f(x, n=6):
    return "%.*e" % (n, x)


print("=" * 100)
print("42.3 参数字典总表：六条恒等式逐行真机复算（HBARC=197.3269804 MeV fm）")
print("=" * 100)
SQ = (D(1) + ALPHA * ALPHA).sqrt()
hdr = ("%-5s %-12s %-12s %-12s %-12s %-12s %-12s"
       % ("粒", "kA vs 1/lamC", "rho vs lC/SQ", "b vs a*rho",
          "Rc vs 1/kA", "om/c vs 1/lam", "lam vs hbarc/m"))
print(hdr)
worst = {}
for row in T423:
    nm, m, kA, tA, rA, bA, Rc, oc, lam = row
    m = D(m); kA = D(kA); tA = D(tA); rA = D(rA)
    bA = D(bA); Rc = D(Rc); oc = D(oc); lam = D(lam)
    lamC = HBARC / m                    # 约化康普顿波长 fm
    e1 = rel(kA, (D(1) / lamC) / SQ)    # kappa_A = kappa_0/sqrt(1+a^2)
    e2 = rel(rA, lamC / SQ)             # rho_A = lamC/sqrt(1+a^2)
    e3 = rel(bA, ALPHA * rA)            # b = alpha rho
    e4 = rel(Rc, D(1) / kA)             # R_c = 1/kappa
    e5 = rel(oc, D(1) / lam)            # omega/c = kappa_0 = 1/lam
    e6 = rel(lam, lamC)                 # lambda = hbar/(mc)
    print("%-5s %-12s %-12s %-12s %-12s %-12s %-12s"
          % (nm, f(e1, 3), f(e2, 3), f(e3, 3), f(e4, 3), f(e5, 3), f(e6, 3)))
    worst[nm] = max(e1, e2, e3, e4, e5, e6)

print()
print("每行最坏相对偏差：")
for nm, v in worst.items():
    print("   %-5s %s" % (nm, f(v, 4)))

print()
print("=" * 100)
print("44.3 定义式表：lambda x (omega/c) 是否 = 1")
print("=" * 100)
for row in T423:
    nm = row[0]; lam = D(row[8]); oc = D(row[7])
    print("   %-5s lam=%-14s om/c=%-14s lam*om/c=%-14s  1/(lam*om/c)=%s"
          % (nm, f(lam, 6), f(oc, 6), f(lam * oc, 6), f(D(1) / (lam * oc), 6)))

# 额外：kappa_A * HBARC 应等于 m（若 kappa_A = m c/hbar）
print()
print("=" * 100)
print("自洽性交叉：kappa_A*HBARC 应 = m/sqrt(1+a^2) ~ m")
print("=" * 100)
for row in T423:
    nm = row[0]; m = D(row[1]); kA = D(row[2])
    print("   %-5s m=%-14s kA*HBARC=%-14s 比=%s"
          % (nm, f(m, 6), f(kA * HBARC, 6), f(kA * HBARC / m, 6)))

# rho_A / R_c^A 应 = 1/(1+a^2) = 0.99994675
print()
print("=" * 100)
print("rho_A / R_c^A 应 = 1/(1+a^2) = %s" % f(D(1) / (D(1) + ALPHA * ALPHA), 10))
print("=" * 100)
for row in T423:
    nm = row[0]; rA = D(row[4]); Rc = D(row[6])
    print("   %-5s ratio=%s" % (nm, f(rA / Rc, 8)))
