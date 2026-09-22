# -*- coding: utf-8 -*-
"""
全域双向分形统一场论 —— 新方程验证（拓扑荷升维定律 / 涌现对偶规范场 / 霍普夫荷）
实验A: 标准霍普夫映射 Q_H 收敛（盒尺寸与分辨率）
实验B: 光滑形变下 Q_H 不变（拓扑保护实证）
实验C: 平方映射整数谱（z -> z^2）
实验D: 3+1D 旋量对偶方程演化下 Q_H 守恒（稳定区）
"""
import numpy as np

def spinor_hopf(X, Y, Z):
    """标准霍普夫旋量（Q_H=1），归一化 (z0, z1)"""
    r2 = X**2 + Y**2 + Z**2
    denom = 1 + r2
    z0 = (2*X + 2j*Y) / denom
    z1 = (2*Z + 1j*(r2 - 1)) / denom
    nrm = np.sqrt(np.abs(z0)**2 + np.abs(z1)**2)
    return z0/nrm, z1/nrm

def spinor_hopf_sq(X, Y, Z):
    """平方版：基映射 z -> z^2（全局光滑旋量提升）"""
    z0, z1 = spinor_hopf(X, Y, Z)
    z0s, z1s = z0**2, z1**2
    nrm = np.sqrt(np.abs(z0s)**2 + np.abs(z1s)**2)
    return z0s/nrm, z1s/nrm

def hopf_charge(z0, z1, dx):
    """Q_H = (1/4pi^2) ∫ a·(∇×a) d³x,  a_i = -Im(ẑ†∂_iẑ)"""
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
print("实验A | 标准霍普夫映射 Q_H 收敛")
print("="*66)
for box, N in [(2, 48), (3, 64), (4, 64), (5, 72)]:
    x = np.linspace(-box, box, N)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    Q = hopf_charge(*spinor_hopf(X, Y, Z), 2*box/(N-1))
    print(f"  box={box}, N={N}: Q_H = {Q:+.6f}")

print("="*66)
print("实验B | 光滑形变（保体积剪切）下 Q_H 不变")
print("="*66)
box, N = 4, 64
x = np.linspace(-box, box, N)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
Q0 = hopf_charge(*spinor_hopf(X, Y, Z), 2*box/(N-1))
print(f"  未形变:        Q_H = {Q0:+.6f}")
for a, b, c in [(0.3, 0.0, 0.0), (0.3, 0.3, 0.3), (0.5, 0.2, -0.4), (0.8, -0.6, 0.5)]:
    Xd = X + a*np.sin(Y)
    Yd = Y + b*np.cos(Z)
    Zd = Z + c*np.sin(X)
    Q = hopf_charge(*spinor_hopf(Xd, Yd, Zd), 2*box/(N-1))
    print(f"  形变({a:+.1f},{b:+.1f},{c:+.1f}): Q_H = {Q:+.6f} | ΔQ = {Q-Q0:+.3e}")

print("="*66)
print("实验C | 平方映射整数谱（z -> z^2 全局光滑提升）")
print("="*66)
for box, N in [(3, 64), (4, 64), (5, 72)]:
    x = np.linspace(-box, box, N)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    Q = hopf_charge(*spinor_hopf_sq(X, Y, Z), 2*box/(N-1))
    print(f"  box={box}, N={N}: Q_H = {Q:+.6f}")

print("="*66)
print("实验D | 3+1D 旋量对偶方程演化下 Q_H 守恒")
print("="*66)
box, N = 8, 64
lamb = 0.2
T, dt = 0.5, 0.01
x = np.linspace(-box, box, N)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
p0, p1 = spinor_hopf(X, Y, Z)   # |Ψ|=1 真空态初始数据
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

# 内域子盒 |x|,|y|,|z| <= 2.5（避开周期边界伪影）
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
        minpsi = np.min(nrm)
        print(f"  t={t:.2f} | Q_H = {Q:+.6f} | 内域 min|Ψ| = {minpsi:.4f}")
    p0, p1 = rk4(p0, p1, dt)
print(f"  >> Q_H 全程漂移 = {max(Qlist)-min(Qlist):.3e}（应为 0）")
