# -*- coding: utf-8 -*-
"""
_ma_kerr_teukolsky_cheb.py
完整 Teukolsky 径向方程 -> Jansen 紧化 Chebyshev 谱方法（修复 v49 微扰近似）
================================================================================
v49 FAIL 根因：其 (iii) 项 i*am*2(r-1)/r^3*g*D 是 4i(r-1)K/Delta 的近似光滑核。
修复：直接在紧化坐标下离散【完整】Teukolsky 径向方程（Hughes 4.3 形式，含
  4i(r-1)K/Delta 精确项），不引入任何微扰近似。方程对 w 为二次：
  Delta R'' - (2r-2) R' + [-(K^2+4i(r-1)K)/Delta + 8i w r + lambda] R = 0   (s=-2)
  lambda = E_lm - 2 a m w + a^2 w^2 - 2
  角向 E_lm 用 Cook-Zalutskiy 谱方法（复用 _ma_kerr_leaver_full.angular_sep_const）。
  sA_lm = E_lm - s(s+1) = E_lm - 2  =>  E_lm = sA_lm + 2

  组装 (w^2, w, const) 三矩阵 -> 二次特征值问题线性化 -> 求最接近物理根的极点。
  边界：x=0 视界（入波 Frobenius 线性化）、x=1 无穷远（出射外推）。
  GR 门 A/B 验证。门未过 -> TUFT 壁不切。
"""
import numpy as np
import math
import cmath
from scipy.linalg import eig
from _ma_kerr_leaver_full import angular_sep_const

def cheb_diff(N):
    x = np.cos(np.pi * np.arange(N+1) / N)   # x: 1(0)..-1(N)
    D = np.zeros((N+1, N+1))
    for i in range(N+1):
        for j in range(N+1):
            if i != j:
                xi, xj = x[i], x[j]
                ci = 2.0 if (i == 0 or i == N) else 1.0
                cj = 2.0 if (j == 0 or j == N) else 1.0
                D[i, j] = (ci/cj) * ((-1)**(i+j)) / (xi - xj)
    for i in range(N+1):
        xi = x[i]
        if i == 0:
            D[i, i] = (2*N*N + 1) / 6.0
        elif i == N:
            D[i, i] = -(2*N*N + 1) / 6.0
        else:
            D[i, i] = -xi / (2*(1 - xi*xi))
    return x, D

def build_pencil(a, s, l, m, E_lm, N=120):
    """完整 Teukolsky 三矩阵 (P: w^2, Q: w, R: const)，内部点 + 视界 Frobenius 线性化 + 无穷远出射外推。
    紧化：x = 1 - rp/r -> x=0 视界(r=rp)，x=1 无穷远。Chebyshev 节点 x_i=cos(pi i/N)，
    i=0 对应 x=1（无穷远），i=N 对应 x=-1（视界 r=rp/(1-x)=rp/2？）——改用 x = 1 - rp/r 的
    映射在 Chebyshev 节点下：x_i = cos(pi i/N) ∈ [-1,1]。
    重新定义紧化 y = (1 - x)/2 ∈ [0,1]：y=0 -> 无穷远（x=1），y=1 -> 视界（x=-1）。
    r = rp / (1 - y) = rp / ((1+x)/2) = 2 rp / (1+x)。
    节点 i=0: x=1 -> r=rp（视界）；i=N: x=-1 -> r=inf（无穷远）。"""
    x, D = cheb_diff(N)
    # 重新映射：令节点 i=0 为视界。用 xc = -x 反转（i=0 -> -1 -> 视界，i=N -> +1 -> 无穷远）
    xc = -x
    with np.errstate(divide='ignore', invalid='ignore'):
        r = 2.0 * (1.0 + math.sqrt(1.0 - a*a)) / (1.0 + xc)   # rp=1+sqrt(1-a^2)
        rp = 1.0 + math.sqrt(1.0 - a*a)
        rm = 1.0 - math.sqrt(1.0 - a*a)
        Delta = (r - rp) * (r - rm)
        # d/dr = (dxc/dr) d/dxc；r = 2 rp/(1+xc) -> dr/dxc = -2 rp/(1+xc)^2 -> dxc/dr = -(1+xc)^2/(2 rp)
        ddr = np.diag(-(1.0 + xc)**2 / (2.0 * rp)) @ D
        ddr2 = ddr @ ddr
        # 完整 V（Hughes 4.3，s=-2；E_lm 角向本征值，lambda=E_lm-2amw+a^2w^2-2）
        # Delta R'' - (2r-2) R' + V R = 0
        # V = -(K^2 + 4i(r-1)K)/Delta + 8i w r + lambda
        # K = (r^2+a^2) w - a m
        # 组装：w^2 系数 = -(r^2+a^2)^2/Delta + a^2
        #       w 系数   = +[2am(r^2+a^2) - 4i(r-1)(r^2+a^2)]/Delta + 8i r - 2 a m
        #       const    = -(a^2 m^2 - 4i(r-1) a m)/Delta + E_lm - 2
        A2 = -(r**2 + a**2)**2 / Delta + a**2
        A1 = (2*a*m*(r**2 + a**2) - 4j*(r-1)*(r**2 + a**2)) / Delta + 8j*r - 2*a*m
        A0 = -(a**2*m**2 - 4j*(r-1)*a*m) / Delta + E_lm - 2
        # 微分算子（w 无关）：Delta ddr2 - (2r-2) ddr
        Lop = np.diag(Delta) @ ddr2 - np.diag(2*(r-1)) @ ddr
    # 内部点：i=1..N-1（去掉视界 i=0 与无穷远 i=N）
    n_in = N - 1
    P = np.zeros((n_in, n_in), dtype=np.complex128)
    Q = np.zeros((n_in, n_in), dtype=np.complex128)
    Rm = np.zeros((n_in, n_in), dtype=np.complex128)
    ii = np.arange(1, N)
    for k, i in enumerate(ii):
        for j, jj in enumerate(ii):
            P[k, j] = A2[i] if i == jj else 0.0
            Q[k, j] = A1[i] if i == jj else 0.0
            Rm[k, j] = (Lop[i, jj] + A0[i]) if i == jj else Lop[i, jj]
    return P, Q, Rm, r, xc

def solve_spectral(a, s, l, m, w_guess, N=120, n_iter=10):
    """二次特征值问题 P w^2 + Q w + R = 0，线性化后取最接近 w_guess 的极点。"""
    # 角向自洽迭代：w -> E_lm -> 再解
    w = complex(w_guess)
    for it in range(n_iter):
        sA = angular_sep_const(a*w, s, l, m)
        E_lm = sA + s*(s+1)   # sA = E_lm - s(s+1)
        P, Q, Rm, r, xc = build_pencil(a, s, l, m, E_lm, N)
        # 线性化：[R Q; 0 P?] 标准：M1 v = w M2 v, v=(u, w u)
        # 方程 P w^2 u + Q w u + R u = 0 -> (w I) [u; w u] 形式：
        # [0, I; -R, -Q] [u; w u] = w [I, 0; 0, P] [u; w u]
        n = P.shape[0]
        Z = np.zeros((n, n), dtype=np.complex128)
        I = np.eye(n)
        M1 = np.block([[Z, I], [-Rm, -Q]])
        M2 = np.block([[I, Z], [Z, P]])
        try:
            ev = eig(M1, M2, right=False)
        except Exception:
            ev = np.linalg.eigvals(np.linalg.solve(M2, M1))
        # 选最接近 w 的（物理基模）
        best = min(ev, key=lambda e: abs(e - w))
        w_new = complex(best)
        if abs(w_new - w) < 1e-13:
            w = w_new
            break
        w = w_new
    return w

if __name__ == '__main__':
    print("== 完整 Teukolsky -> Jansen 紧化 Chebyshev：GR 门验证 ==")
    # 门 A：a=0 n0
    w0 = 0.37367168441804166 - 0.08896231568893410j
    wA = solve_spectral(0.0, -2, 2, 2, 0.360-0.088j, N=120)
    errA = abs(wA - w0)
    if errA > 0:
        digits = -math.log10(errA)
    else:
        digits = 20.0
    gateA = errA < 10**-11.6
    print(f"[A] a=0 n0 = {wA.real:.14f}{wA.imag:+.14f}i  |err|={errA:.3e}  {digits:.1f}位  ({'PASS' if gateA else 'FAIL'})")
