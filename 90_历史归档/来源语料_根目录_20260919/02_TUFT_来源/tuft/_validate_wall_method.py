"""方法校验：方形势垒腔（已知腔模）验证反向射击法能找到 f_out(u_s)=0 的极点。
腔 [u_s, u_b] 宽 W=u_b-u_s，壁垒高 V_b>>w^2 从 u_b 起长 L_bar，墙 Dirichlet 于 u_s。
已知腔模（Fabry-Perot）：omega_n = pi*n/W（往返相位 2*pi*n），漏泄给小 Im<0。
若本脚本在 omega_1=pi/W 附近找到 |Psi(u_s)|->0 的极点，则方法正确，
此前 RW 的"无极点"结论可信；若找不到，则方法本身有缺陷。
"""
import numpy as np
import sys

M = 1.0
u_s = -5.33
u_b = 1.6
W = u_b - u_s
L_bar = 1.0
V_b = 1.0          # 高壁垒，近似理想反射
U0 = u_b + L_bar + 30.0   # 壁垒之外 V=0 处种入出波


def V_of_u(u):
    if u_b <= u <= u_b + L_bar:
        return V_b
    return 0.0


def shoot_back(omega, seed, u_0=U0, du=0.01):
    """seed='out' 种纯出波(即 f_out)；seed='in' 种纯入波(即 f_in)。向后积分到墙。"""
    n = int(round((u_0 - u_s) / du))
    if seed == "out":
        P, dP = 1.0 + 0j, 1j * omega
    else:
        P, dP = 1.0 + 0j, -1j * omega

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


omega1 = np.pi / W
print("cavity width W=%.4f  expected omega_1 = pi/W = %.5f" % (W, omega1))
for seed in ("in", "out"):
    print("\nseed=%s  (腔模极点= f_%s(u_s)=0 处)" % (seed, seed))
    best = None
    bestv = 1e30
    for wr in np.linspace(omega1 - 0.15, omega1 + 0.15, 31):
        for wi in np.linspace(-0.05, -0.0005, 25):
            w = complex(wr, wi)
            g = abs(shoot_back(w, seed))
            if g < bestv:
                bestv = g
                best = w
    print("  min |Psi(u_s)| = %.3e at omega=%.5f%+.5fi" % (bestv, best.real, best.imag))
