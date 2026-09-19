# -*- coding: utf-8 -*-
"""
补充对照：
对照1: 3+1D 自由场(lambda=0)演化下 Q_H 是否守恒（|Psi| 逐点不变 -> 应守恒）
对照2: 平方映射高分辨率整数谱复核（box=4,N=96 / box=6,N=96）
"""
import numpy as np

def spinor_hopf(X, Y, Z):
    r2 = X**2 + Y**2 + Z**2
    denom = 1 + r2
    z0 = (2*X + 2j*Y) / denom
    z1 = (2*Z + 1j*(r2 - 1)) / denom
    nrm = np.sqrt(np.abs(z0)**2 + np.abs(z1)**2)
    return z0/nrm, z1/nrm

def spinor_hopf_sq(X, Y, Z):
    z0, z1 = spinor_hopf(X, Y, Z)
    z0s, z1s = z0**2, z1**2
    nrm = np.sqrt(np.abs(z0s)**2 + np.abs(z1s)**2)
    return z0s/nrm, z1s/nrm

def hopf_charge(z0, z1, dx):
    gz0 = np.gradient(z0, dx, axis=0); gy0 = np.gradient(z0, dx, axis=1); gz0z = np.gradient(z0, dx, axis=2)
    gz1 = np.gradient(z1, dx, axis=0); gy1 = np.gradient(z1, dx, axis=1); gz1z = np.gradient(z1, dx, axis=2)
    ax = -np.imag(np.conj(z0)*gz0 + np.conj(z1)*gz1)
    ay = -np.imag(np.conj(z0)*gy0 + np.conj(z1)*gy1)
    az = -np.imag(np.conj(z0)*gz0z + np.conj(z1)*gz1z)
    bx = np.gradient(az, dx, axis=1) - np.gradient(ay, dx, axis=2)
    by = np.gradient(ax, dx, axis=2) - np.gradient(az, dx, axis=0)
    bz = np.gradient(ay, dx, axis=0) - np.gradient(ax, dx, axis=1)
    return (ax*bx + ay*by + az*bz).sum() * dx**3 / (4*np.pi**2)

print("="*66)
print("对照2 | 平方映射整数谱高分辨率复核")
print("="*66)
for box, N in [(4, 96), (6, 96)]:
    x = np.linspace(-box, box, N)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    Q = hopf_charge(*spinor_hopf_sq(X, Y, Z), 2*box/(N-1))
    print(f"  box={box}, N={N}: Q_H = {Q:+.6f}")

print("="*66)
print("对照1 | 3+1D 自由场(lambda=0)演化下 Q_H 守恒性")
print("="*66)
box, N = 8, 64
lamb = 0.0
T, dt = 0.5, 0.01
x = np.linspace(-box, box, N)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
p0, p1 = spinor_hopf(X, Y, Z)
k = np.fft.fftfreq(N, d=2*box/(N-1)) * 2*np.pi
kx, ky, kz = np.meshgrid(k, k, k, indexing='ij')

def rhs(p0, p1):
    f0 = np.fft.fftn(p0); f1 = np.fft.fftn(p1)
    d0 = -np.fft.ifftn(1j*kz*f0) - np.fft.ifftn(1j*(kx - 1j*ky)*f1) - lamb*np.conj(p1)
    d1 = -np.fft.ifftn(1j*(kx + 1j*ky)*f0) + np.fft.ifftn(1j*kz*f1) + lamb*np.conj(p0)
    return d0, d1

def rk4(p0, p1, dt):
    k1a, k1b = rhs(p0, p1)
    k2a, k2b = rhs(p0 + dt/2*k1a, p1 + dt/2*k1b)
    k3a, k3b = rhs(p0 + dt/2*k2a, p1 + dt/2*k2b)
    k4a, k4b = rhs(p0 + dt*k3a, p1 + dt*k3b)
    return (p0 + dt/6*(k1a + 2*k2a + 2*k3a + k4a),
            p1 + dt/6*(k1b + 2*k2b + 2*k3b + k4b))

idx = np.where(np.abs(x) <= 2.5)[0]
sub = np.ix_(idx, idx, idx)
dx = 2*box/(N-1)
steps = int(T/dt)
Qlist = []
for it in range(steps + 1):
    if it % 25 == 0:
        t = it*dt
        p0s, p1s = p0[sub], p1[sub]
        nrm = np.sqrt(np.abs(p0s)**2 + np.abs(p1s)**2)
        Q = hopf_charge(p0s/nrm, p1s/nrm, dx)
        Qlist.append(Q)
        print(f"  t={t:.2f} | Q_H = {Q:+.6f} | 内域 min|Ψ| = {np.min(nrm):.6f}")
    p0, p1 = rk4(p0, p1, dt)
print(f"  >> Q_H 全程漂移 = {max(Qlist)-min(Qlist):.3e}（lambda=0 自由场，应≈0）")
