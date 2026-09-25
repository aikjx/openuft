# -*- coding: utf-8 -*-
"""引力本源跨尺度精算：牛顿/GR 源、各星体 g、微观质量构成、力的比值"""
G = 6.67430e-11
c = 2.99792458e8

def g_surf(M, R):
    return G*M/R**2

ME, RE = 5.9722e24, 6.371e6
MS, RS = 1.98847e30, 6.957e8
bodies = [
    ("地球", ME, RE),
    ("太阳", MS, RS),
    ("白矮星(1Msun, R=地球)", MS, RE),
    ("中子星(1.4Msun, R=12km)", 1.4*MS, 12e3),
]
print("=== 表面重力加速度 g = GM/R^2 ===")
for n,M,R in bodies:
    g = g_surf(M,R)
    print("  %-26s g = %.3e m/s^2  (相对地球 %.2e 倍)" % (n, g, g/9.80665))

print()
print("=== 史瓦西黑洞视界'表面引力'(1 Msun) ===")
g_h = c**4/(4*G*MS)
print("  g_horizon = c^4/(4GM) = %.2e m/s^2" % g_h)

print()
print("=== 微观：氢原子内 库仑力 vs 万有引力 ===")
ke = 8.9875517923e9
e = 1.602176634e-19
mp, me = 1.67262192369e-27, 9.1093837015e-31
a0 = 5.29177210903e-11
Fe = ke*e**2/a0**2
Fg = G*mp*me/a0**2
print("  库仑力 = %.3e N, 万有引力 = %.3e N, 比值 Fe/Fg = %.2e" % (Fe, Fg, Fe/Fg))
print("  两个质子(相距1m): Fe/Fg = %.2e" % (ke*e**2/(G*mp**2)))

print()
print("=== 重子质量的构成（引力质量从哪来）===")
m_proton = 938.272  # MeV/c^2
u_d_current = 2.2+4.7
print("  质子质量 938.272 MeV; u+d 流质量约 %.1f MeV -> 占比 %.2f%% (Higgs)" % (u_d_current, 100*u_d_current/m_proton))
print("  QCD 胶子/夸克动能+结合能占比约 %.1f%% (E=mc^2)" % (100*(1-u_d_current/m_proton)))

print()
print("=== 结合能造成的质量（引力质量）减少 ===")
print("  氘核结合能 2.224 MeV / 1875.6 = %.4f%%" % (100*2.224/1875.6))
print("  铁核每核子 8.79 MeV / 931.5 = %.3f%%" % (100*8.79/931.5))
frac_E = 3*G*ME/(5*RE*c**2)
print("  地球引力自束缚能/Mc^2 = 3GM/(5Rc^2) = %.2e" % frac_E)

print()
print("=== GR 主动引力密度 rho + 3p/c^2 ===")
print("  普通物质 p~0: 等于 rho")
print("  辐射 p=rho c^2/3: rho+3p/c^2 = 2 rho (引力加倍)")
print("  暗能量 p=-rho c^2: rho+3p/c^2 = -2 rho (净排斥 -> 加速膨胀)")
