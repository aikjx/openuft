# -*- coding: utf-8 -*-
"""S11 GMUFT 联合场方程：量纲账本 / 退化检验 / 可观测性量级 (算法联盟)"""
G = 6.67430e-11
hbar = 1.054571817e-34
c = 2.99792458e8

print("=== 作用量量纲账本 (hbar=c=1, 质量幂次 d) ===")
dR, dT, dQ, dPi, dLm, dmeas = 2, 1, 1, 1, 4, -4
rows = [
    ("R/(2k) 曲率项", dR),
    ("a*T^2 挠率项", 2*dT),
    ("b*Q^2 非度规项", 2*dQ),
    ("c*Pi^2 射影项", 2*dPi),
    ("L_m 物质项", dLm),
]
for name, p in rows:
    tot = p + dmeas
    flag = "OK" if tot == 0 else "FAIL"
    print("  %-16s 被积 M^%d + 测度 M^%d = M^%d  [%s]" % (name, p, dmeas, tot, flag))
print("  => a,b,c(alpha,beta,gamma) 必须无量纲 (T,Q,Pi 量纲均 M^1, 平方 M^2 = R)")
print()

print("=== Einstein-Cartan 自旋二次修正可观测性 ===")
rho_P = c**5/(hbar*G**2)
rho_nuc = 2.8e17
print("  Planck 密度 rho_P   = %.3e kg/m^3" % rho_P)
print("  核物质密度 rho_nuc  = %.2e kg/m^3" % rho_nuc)
ratio = rho_nuc/rho_P
print("  rho_nuc/rho_P       = %.3e" % ratio)
print("  挠率自旋接触修正量级 ~ rho/rho_P = %.2e (远低可测阈值)" % ratio)
print()

print("=== 最小耦合退化 ===")
print("  a=b=c=0 且物质无自旋/超荷源 => T=Q=Pi=0, Gamma=LC => EH+Lm = 标准 GR")
print()

print("=== 非度规性源: hypermomentum 而非电荷 ===")
# 电子荷质比 vs sqrt(4*pi*eps0*G)
eps0 = 8.8541878128e-12
import math
qm_dual = math.sqrt(4*math.pi*eps0*G)
e = 1.602176634e-19
me = 9.1093837015e-31
print("  对偶荷质比 sqrt(4*pi*eps0*G) = %.4e C/kg" % qm_dual)
print("  电子实际荷质比 e/m_e          = %.4e C/kg" % (e/me))
print("  比值 (e/m_e)/dual             = %.2e 倍 => 不对应任何真实粒子" % ((e/me)/qm_dual))
