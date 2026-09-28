# -*- coding: utf-8 -*-
"""
_ma_gateB_fullVH.py
第三独立 GATE B —— 完整 V_H 精确 O(a) 结构（非 v49 三项微扰）
========================================================================
v49 门 B FAIL 根因：O(a) 三项微扰不完整且 (iii) 项（i am 2(r-1)/r^3 g D 导数耦合）
是编造结构——真实 O(a) 来自完整 V_H（Hughes 4.3）：
  V_H = -(K^2 + 4i(r-1)K)/Delta + 8 i w r + (sA - 2 a m w + a^2 w^2)
  K = (r^2+a^2)w - a m ;  Delta = (r-r+)(r-r-) = r(r-2)+a^2
O(a) 一阶（对 a m，归一 m=1）：
  dK2w = +2(r^2+a^2)/Delta        (K^2 的 -2am(r^2+a^2)w 项 -> +2am(r^2+a^2)w/Delta)
  dic_w = -4i(r-1)(r^2+a^2)/Delta (4i(r-1)K 的 w 项)
  dlam  = -2                      (sA - 2 a m w 的 -2amw)
  dic_c = +4i(r-1)/Delta          (4i(r-1)K 的 -am 常数项)
  (注意 Delta 本身含 a^2，一阶无影响；但 r+ 也移动——一阶 dDelta=-2 a dr? 由 a^2 阶，一阶忽略)
组装：M(w) = Lop + diag(A2 w^2 + A1 w + A0)；a 一阶：dM = diag(dA2 w^2 + dA1 w + dA0)
Rayleigh: dw = - u^T dM v / (u^T dM/dw v),  dM/dw = diag(2 A2 w + A1)
splitR/a = 4 Re(dw/a)|_{m=1}（m=+2 vs -2 差 4 倍 per-am）
靶：splitR/a = 0.2515323（GR 门 B >=4 位）
"""
import numpy as np
import math, sys
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib')
from scipy.linalg import eig, null_space

GR_N0 = 0.37367168441804166 - 0.08896231568893410j
GR_SPLIT_SLOPE = 0.2515323

def cheb_gauss(N):
    j = np.arange(1, N+1); th = np.pi*(j-0.5)/N
    z = np.cos(th); w = ((-1.0)**(j-1))*np.sin(th)
    zi, zj = np.meshgrid(z, z, indexing='ij'); wi, wj = np.meshgrid(w, w, indexing='ij')
    with np.errstate(divide='ignore', invalid='ignore'):
        D = (wj/wi)/(zi-zj)
    np.fill_diagonal(D, 0.0); np.fill_diagonal(D, -D.sum(axis=1))
    return z, D, D@D

def angular_sep_const(c, s, l, m, Nmat=28):
    lmin = max(abs(s), abs(m))
    def F(l):
        t1 = (l+1)**2 - m*m; t2 = (l+1)**2 - s*s
        if t1 <= 0 or t2 <= 0: return 0.0
        return math.sqrt(t1/((2*l+3)*(2*l+1))) * math.sqrt(t2)/(l+1)
    def G(l):
        if l == 0: return 0.0
        t1 = l*l - m*m; t2 = l*l - s*s
        if t1 <= 0 or t2 <= 0: return 0.0
        return math.sqrt(t1/(4*l*l-1)) * math.sqrt(t2)/l
    def H(l):
        if l == 0 or s == 0: return 0.0
        return -m*s/(l*(l+1))
    def A(l): return F(l)*F(l+1)
    def D_(l): return F(l)*(H(l+1)+H(l))
    def B(l): return F(l)*G(l+1) + G(l)*F(l-1) + H(l)*H(l)
    def E(l): return G(l)*(H(l-1)+H(l))
    def Cc(l): return G(l)*G(l-1)
    Nn = Nmat
    lvals = [lmin+i for i in range(Nn)]
    Mm = np.zeros((Nn,Nn), dtype=complex)
    for i, lp in enumerate(lvals):
        for j, lc in enumerate(lvals):
            d = lc - lp
            if d == -2: Mm[i,j] = -c**2*A(lc)
            elif d == -1: Mm[i,j] = -c**2*D_(lc) + 2*c*s*F(lc)
            elif d == 0: Mm[i,j] = lp*(lp+1)-s*(s+1)-c**2*B(lp)+2*c*s*H(lp)
            elif d == 1: Mm[i,j] = -c**2*E(lc) + 2*c*s*G(lc)
            elif d == 2: Mm[i,j] = -c**2*Cc(lc)
    ev = np.linalg.eigvals(Mm)
    tgt = l*(l+1) - s*(s+1)
    return complex(min(ev, key=lambda e: abs(e-tgt)))

def assemble_fullVH(w, a, s, l, m, N, b, mazi=1.0):
    """完整 V_H 组装（a 一阶保留）：M(w) = Lop + diag(A2 w^2 + A1 w + A0)"""
    z, D, D2 = cheb_gauss(N)
    omz = 1.0 - z
    rp = 1.0 + math.sqrt(1.0 - a*a); rm = 1.0 - math.sqrt(1.0 - a*a)
    r = rp + b*(1.0+z)/omz
    Delta = (r - rp)*(r - rm)
    dzdr = omz**2/(2.0*b)
    d2zdr2 = -omz**3/(2.0*b*b)
    Lop = (np.diag(Delta*dzdr**2)@D2 + np.diag(Delta*d2zdr2)@D
           - np.diag((2.0*r-2.0)*dzdr)@D)
    r2pa2 = r*r + a*a
    # V_H 各项
    K2c_w2 = -(r2pa2)**2/Delta          # K^2 w^2 项
    K2c_w  = +2.0*a*mazi*r2pa2/Delta     # K^2 -2amw 项
    K2c_c  = -a*a*mazi*mazi/Delta        # K^2 +a^2m^2 项
    ic_w   = -4j*(r-1.0)*r2pa2/Delta     # 4i(r-1)K w 项
    ic_c   = +4j*(r-1.0)*a*mazi/Delta    # 4i(r-1)K -am 常数项
    sA = angular_sep_const(a*w, s, l, mazi)
    lam_c = sA                          # 常数
    lam_w = -2.0*a*mazi                  # -2 a m w
    lam_w2 = a*a                         # + a^2 w^2
    A2 = K2c_w2 + lam_w2
    A1 = K2c_w + ic_w + 8j*r + lam_w
    A0 = K2c_c + ic_c + lam_c
    return Lop, A2, A1, A0, z, D, D2, r

def gateB_fullVH(N=60, b=complex(4.0,0.5)):
    """a->0 split via adjoint Rayleigh with FULL V_H O(a) structure."""
    a0 = 0.0
    # a=0 求特征对
    Lop, A2, A1, A0, z, D, D2, r = assemble_fullVH(GR_N0, a0, -2, 2, 2, N, b)
    M0 = Lop + np.diag(A2*GR_N0*GR_N0 + A1*GR_N0 + A0)
    # 求 a=0 精确特征对（Beyn 或直接 eig）
    # 用特征分解验证 w0 是根
    # 组装 w-参数化 M(w) 求奇异最小
    w0 = GR_N0
    # 数值：eig of companion？直接用 M(w) 在 w0 的 null space（若正确应奇异）
    ev = np.linalg.svd(M0, compute_uv=False)
    print("  a=0 M(w0) sigma_min = %.3e (应极小若 V_H 组装正确)" % ev[-1])
    # 即使不奇异，也用 adjoint Rayleigh 求修正（需左/右零空间）
    # 更稳：小 a 直接 eig 求 m=+2/-2，外推到 a=0
    res = []
    for aa in (0.005, 0.01, 0.02):
        ws = []
        for mm in (+2.0, -2.0):
            # 组装 M(w; a) 并在 w0 邻域用 Beyn 求根
            Lop, A2, A1, A0, *_ = assemble_fullVH(GR_N0, aa, -2, 2, mm, N, b)
            Mlin = Lop + np.diag(A2)  # w^2 矩阵
            # 线性化 companion: [0 I; -A0 -A1] - w[-I 0; 0 A2]
            n = Lop.shape[0]; Z = np.zeros_like(Lop); I = np.eye(n)
            Mm_ = np.block([[Z, I], [-np.diag(A0) - Lop, -np.diag(A1)]])
            Lm_ = np.block([[I, Z], [Z, np.diag(A2)]])
            # 直接 eig（N=60 -> 120x120，OK）
            evv = np.linalg.eigvals(np.linalg.solve(Lm_, Mm_))
            wb = min(evv, key=lambda e: abs(e - w0))
            ws.append(wb)
        res.append((ws[0]-ws[1])/aa)   # split/a for m=+2 vs -2 (差 = 4 c)
    # Richardson a^2 线性外推
    aarr = np.array([0.005, 0.01, 0.02]); sarr = np.array([r.real for r in res])
    from numpy.polynomial import polynomial as P
    cfit = np.polyfit(aarr*aarr, sarr, 1)
    split_a = cfit[1]  # 截距
    print("  split/a @a: ", sarr)
    print("  Richardson(a^2 线性) splitR/a = %.8f  (靶 %.6f)" % (split_a, GR_SPLIT_SLOPE))
    err = abs(split_a/GR_SPLIT_SLOPE - 1.0)
    print("  GATE B: %s (rel err %.2e)" % ("PASS" if err < 5e-4 else "FAIL", err))
    return split_a

if __name__ == '__main__':
    print("="*78)
    print("第三独立 GATE B —— 完整 V_H 精确 O(a)（非 v49 三项微扰）")
    print("="*78)
    gateB_fullVH()
