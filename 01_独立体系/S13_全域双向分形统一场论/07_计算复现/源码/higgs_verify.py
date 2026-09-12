# -*- coding: utf-8 -*-
"""
全域双向分形统一场论 —— 突破验证：对偶旋量即希格斯对偶
验证1: 对偶帧 E=(ẑ, Θẑ*) 酉性（机器精度）
验证2: 真空流形 S^3 与模式谱：Hessian 本征值 {0,0,0, 8κv²}
验证3: 未破缺 U(1)：存在生成元 g 使 g·ẑ₀ = 0
验证4: 零模方向 ⊥ 径向（3 个平坦方向 = 被吃掉的 NG 模）
"""
import numpy as np

print("="*66)
print("验证1 | 对偶帧 E = (ẑ, Θẑ*) 酉性（霍普夫旋量全网格）")
print("="*66)
def spinor_hopf(X, Y, Z):
    r2 = X**2 + Y**2 + Z**2
    denom = 1 + r2
    z0 = (2*X + 2j*Y)/denom
    z1 = (2*Z + 1j*(r2 - 1))/denom
    n = np.sqrt(np.abs(z0)**2 + np.abs(z1)**2)
    return z0/n, z1/n

x = np.linspace(-3, 3, 24)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
z0, z1 = spinor_hopf(X, Y, Z)
e1 = np.stack([z0, z1], axis=-1)
e2 = np.stack([-np.conj(z1), np.conj(z0)], axis=-1)   # Θẑ*
EE = (np.einsum('...i,...j->...ij', np.conj(e1), e1) +
      np.einsum('...i,...j->...ij', np.conj(e2), e2))
res = np.max(np.abs(EE - np.eye(2)))
print(f"  max|E†E - I| = {res:.3e}（应≈0，对偶帧全局酉）")
res2 = np.max(np.abs((np.conj(e1)*e2).sum(-1)))
print(f"  max|ẑ†Θẑ*| = {res2:.3e}（应≈0，对偶分量正交）")

print("="*66)
print("验证2 | 真空流形 S^3 与模式谱（κ=1, v=1）")
print("="*66)
kap, v = 1.0, 1.0
def vf(q):
    rho2 = q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2
    return kap*(rho2 - v**2)**2

def hessian(p, eps=2e-4):
    H = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            pp = p.copy(); pm = p.copy(); mp = p.copy(); mm = p.copy()
            pp[i] += eps; pp[j] += eps
            pm[i] += eps; pm[j] -= eps
            mp[i] -= eps; mp[j] += eps
            mm[i] -= eps; mm[j] -= eps
            H[i, j] = (vf(pp) - vf(pm) - vf(mp) + vf(mm)) / (4*eps**2)
    return H

rng = np.random.default_rng(7)
for trial in range(3):
    z = rng.normal(size=2) + 1j*rng.normal(size=2)
    z = z/np.sqrt(np.abs(z[0])**2 + np.abs(z[1])**2)
    p = np.array([z[0].real, z[0].imag, z[1].real, z[1].imag])
    H = hessian(p)
    ev = np.linalg.eigvalsh(H)
    # 零模方向与径向 p 的内积
    vecs = np.linalg.eigh(H)[1]
    proj = np.abs(vecs.T @ p)
    print(f"  真空点{trial+1}: 本征值 = {np.round(ev, 6)}")
    print(f"    |零模·径向| 投影 = {np.round(proj, 6)}（3 零模应⊥径向，质量模应∥径向）")

print("="*66)
print("验证3 | 未破缺 U(1) 生成元（u(2) 生成元作用真空的零空间）")
print("="*66)
sigma = [np.eye(2, dtype=complex),
         np.array([[0,1],[1,0]], dtype=complex),
         np.array([[0,-1j],[1j,0]], dtype=complex),
         np.array([[1,0],[0,-1]], dtype=complex)]
for trial in range(3):
    z = rng.normal(size=2) + 1j*rng.normal(size=2)
    z = z/np.sqrt(np.abs(z[0])**2 + np.abs(z[1])**2)
    # 生成元作用: 1j*sig @ z, 展开为 4 实分量
    M = np.zeros((4, 4))
    for a in range(4):
        gz = 1j*sigma[a] @ z
        M[:, a] = [gz[0].real, gz[0].imag, gz[1].real, gz[1].imag]
    _, s, _ = np.linalg.svd(M)
    nullity = int(np.sum(s < 1e-10))
    print(f"  真空点{trial+1}: u(2) 生成元作用矩阵奇异值 = {np.round(s, 6)} | 零空间维数 = {nullity}（应=1：未破缺 U(1)）")
