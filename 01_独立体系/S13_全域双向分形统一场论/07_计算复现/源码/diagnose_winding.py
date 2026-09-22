# -*- coding: utf-8 -*-
"""
诊断：绕数拓扑荷 Q 突变定位 + 真守恒量 ∫J0 检验
"""
import numpy as np

print("诊断1 | 高分辨率追踪 Q、∫J0、min|psi0|、min|psi1|（lambda=0.5, N=512）")
L = 2 * np.pi
N = 512
x = np.linspace(0, L, N, endpoint=False)
kv = np.fft.fftfreq(N, d=L / N) * 2 * np.pi
lamb = 0.5
w = L / 8
gauss = np.exp(-(x - L / 2) ** 2 / (2 * w ** 2))
psi0 = gauss * np.exp(1j * x)
psi1 = 1.0 + 0.5 * gauss

def rhs(u):
    p0 = u[:N]; p1 = u[N:]
    d0 = -np.fft.ifft(1j * kv * np.fft.fft(p0)) - lamb * np.conj(p1)
    d1 = np.fft.ifft(1j * kv * np.fft.fft(p1)) + lamb * np.conj(p0)
    return np.concatenate([d0, d1])

def rk4(u, dt):
    k1 = rhs(u); k2 = rhs(u + dt / 2 * k1); k3 = rhs(u + dt / 2 * k2); k4 = rhs(u + dt * k3)
    return u + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

u = np.concatenate([psi0, psi1])
T, dt = 3.0, 0.002
steps = int(T / dt)
Q0 = None
for it in range(steps + 1):
    if it % 100 == 0:
        t = it * dt
        p0 = u[:N]; p1 = u[N:]
        z = p0 / p1
        arg = np.unwrap(np.angle(z))
        Q = (arg[-1] - arg[0]) / (2 * np.pi)
        J0 = np.abs(p0) ** 2 + np.abs(p1) ** 2
        QJ = J0.sum() * (L / N)
        m0 = np.min(np.abs(p0)); m1 = np.min(np.abs(p1))
        if Q0 is None:
            Q0 = Q; QJ0 = QJ
        print(f"  t={t:5.2f} | Q={Q:+.6f} | ∫J0={QJ:.12f} (Δ={QJ - QJ0:+.3e}) | min|ψ0|={m0:.3e} | min|ψ1|={m1:.3e}")
    u = rk4(u, dt)

print()
print("诊断2 | lambda=0.2 鲁棒性检验：绕数是否仍突变（N=512）")
lamb = 0.2
u = np.concatenate([psi0, psi1])
T, dt = 5.0, 0.002
steps = int(T / dt)
for it in range(steps + 1):
    if it % 250 == 0:
        t = it * dt
        p0 = u[:N]; p1 = u[N:]
        z = p0 / p1
        arg = np.unwrap(np.angle(z))
        Q = (arg[-1] - arg[0]) / (2 * np.pi)
        J0 = np.abs(p0) ** 2 + np.abs(p1) ** 2
        QJ = J0.sum() * (L / N)
        print(f"  t={t:4.1f} | Q={Q:+.6f} | ∫J0={QJ:.12f} | min|ψ0|={np.min(np.abs(p0)):.3e} | min|ψ1|={np.min(np.abs(p1)):.3e}")
    u = rk4(u, dt)

print()
print("诊断3 | 静态配置绕数检验：自由场（lambda=0）下绕数是否守恒")
lamb = 0.0
u = np.concatenate([psi0, psi1])
T, dt = 5.0, 0.002
steps = int(T / dt)
for it in range(steps + 1):
    if it % 250 == 0:
        t = it * dt
        p0 = u[:N]; p1 = u[N:]
        z = p0 / p1
        arg = np.unwrap(np.angle(z))
        Q = (arg[-1] - arg[0]) / (2 * np.pi)
        print(f"  t={t:4.1f} | Q={Q:+.6f}（自由场：左右行波各自传播，绕数应保持）")
    u = rk4(u, dt)
