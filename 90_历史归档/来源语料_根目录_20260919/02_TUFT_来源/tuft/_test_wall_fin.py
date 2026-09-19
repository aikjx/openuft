"""验证（决定版）：RW 势 + 反射壁 r_s=2.05 的腔模 = 入波 Jost 解 f_in 在墙处取零
f_in(u_s)=0（S 矩阵极点 = 腔模共振）。方法已在方形势垒上校验：入波种子反向
射击能找到 |Psi(u_s)|->0 的极点；此处同法用于 RW。若找到 <<1 的极小值且在
u_0 增大时保持（真极点），则 TUFT 反射壁确有真腔模；否则 R21/R24 的 0.41-0.03
仅为有限域箱模。
"""
import numpy as np

M = 1.0
r_s = 2.05
u_s = r_s + 2.0 * M * np.log(r_s / (2.0 * M) - 1.0)

DU = 0.02
U_MAX_TOT = 400.0
NU = int(round((U_MAX_TOT - u_s) / DU)) + 1
ugrid = u_s + np.arange(NU) * DU


def build_V():
    c = ugrid / (2.0 * M) - 1.0
    y = np.where(c > 1.0, c, np.exp(c))
    y = np.maximum(y, 1e-12)
    for _ in range(50):
        f = y + np.log(y) - c
        y = y - f / (1.0 + 1.0 / y)
        y = np.maximum(y, 1e-14)
    r = 2.0 * M * (1.0 + y)
    fr = 1.0 - 2.0 * M / r
    return fr * (6.0 / r ** 2 - 6.0 * M / r ** 3)


VG = build_V()


def V_of_u(u):
    idx = int(round((u - u_s) / DU))
    idx = max(0, min(NU - 1, idx))
    return VG[idx]


def shoot_back_in(omega, u_0=60.0, du=DU):
    """种纯入波 f_in: P=1, P'=-iω，向后积分到墙，返回 P(u_s)。"""
    n = int(round((u_0 - u_s) / du))
    P = 1.0 + 0j
    dP = -1j * omega

    def rhs(Pv, dPv, uv):
        return dPv, -(omega ** 2 - V_of_u(uv)) * Pv

    for k in range(n):
        u0 = u_0 - k * du
        u1 = u0 - du
        k1P, k1d = rhs(P, dP, u0)
        k2P, k2d = rhs(P + du / 2 * k1P, dP + du / 2 * k1d, u1)
        k3P, k3d = rhs(P + du / 2 * k2P, dP + du / 2 * k2d, u1)
        k4P, k4d = rhs(P + du * k3P, dP + du * k3d, u1)
        P = P + du / 6 * (k1P + 2 * k2P + 2 * k3P + k4P)
        dP = dP + du / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
    return P


print("u_s=%.5f  V0~0.151 => sqrt(V0)~0.389 ; 腔模需 wR<0.389(被势垒囚禁)" % u_s)
print("扫描 f_in(u_s) (入波种子反向射击)，找 <<1 的极小值：")
cands = []
for wr in np.linspace(0.10, 0.62, 52):
    for wi in np.linspace(-0.15, -0.0005, 38):
        w = complex(wr, wi)
        g = abs(shoot_back_in(w))
        cands.append((g, w))
cands.sort(key=lambda t: t[0])
print("  top-8 最小 |f_in(u_s)|:")
for g, w in cands[:8]:
    print("    |f_in|=%.4e  omega=%.5f%+.5fi" % (g, w.real, w.imag))

g0, w0 = cands[0]
print("\n全局最小 |f_in(u_s)|=%.4e @ %.5f%+.5fi" % (g0, w0.real, w0.imag))
print("u_0 无关性（真极点应随 u_0 增大保持 <<1）：")
for u0 in (40.0, 60.0, 90.0, 140.0):
    print("  u_0=%-5.0f  |f_in(u_s)|=%.4e" % (u0, abs(shoot_back_in(w0, u0))))
