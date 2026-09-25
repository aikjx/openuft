#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第03章 数值验证：闵氏时空与狭义相对论
验证项：
  B-001 随机洛伦兹变换保范数 Λ^T η Λ = η（机器零）
  B-002 Noether 能动张量守恒 ∂_μ T^{μν}=0（自由 KG 场 1+1 维，有限差分）
  B-003 快度加法、时间膨胀 γ=5/3、质量壳 E²-p²c²=m²c⁴
零依赖，python3 verify_minkowski.py
"""
import math, random

ETA = (-1.0, 1.0, 1.0, 1.0)   # 闵氏号差 (-,+,+,+)

def mat_mul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def boost_x(phi):
    c, s = math.cosh(phi), math.sinh(phi)
    return [[c, s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

def rot_z(th):
    c, s = math.cos(th), math.sin(th)
    return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]

def rot_y(th):
    c, s = math.cos(th), math.sin(th)
    return [[1, 0, 0, 0], [0, c, 0, s], [0, 0, 1, 0], [0, -s, 0, c]]

def random_lorentz(rng):
    """随机 SO^+(1,3) 元素：三个 boost 加三个旋转复合"""
    L = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    for _ in range(3):
        L = mat_mul(boost_x(rng.uniform(-1.2, 1.2)), L)
        L = mat_mul(rot_z(rng.uniform(-3, 3)), L)
        L = mat_mul(rot_y(rng.uniform(-3, 3)), L)
    return L

def eta_sandwich(L):
    """(Λ^T η Λ)_{μν}"""
    Lt = [[L[j][i] for j in range(4)] for i in range(4)]
    M = [[Lt[i][k]*ETA[k] for k in range(4)] for i in range(4)]  # Λ^T·η
    return [[sum(M[i][k]*L[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def check_B001(n=200, tol=1e-13):
    rng = random.Random(42)
    worst = 0.0
    for _ in range(n):
        L = random_lorentz(rng)
        S = eta_sandwich(L)
        for i in range(4):
            for j in range(4):
                want = ETA[i] if i == j else 0.0
                worst = max(worst, abs(S[i][j] - want))
    return worst

def check_B003():
    """快度加法 + 时间膨胀 γ + 质量壳"""
    errs = []
    for phi1, phi2 in [(0.3, 0.7), (1.0, -0.5), (2.0, 1.5)]:
        A, B, C = boost_x(phi1), boost_x(phi2), boost_x(phi1 + phi2)
        AB = mat_mul(A, B)
        errs.append(max(abs(AB[i][j]-C[i][j]) for i in range(4) for j in range(4)))
    beta = 0.8                                  # v=0.8c
    gamma = 1.0/math.sqrt(1-beta*beta)
    errs.append(abs(gamma - 5.0/3.0))           # 精确值 5/3
    m, gm = 1.0, 2.0                            # γ=2, m=1
    E, p = m*gm, m*math.sqrt(gm*gm-1.0)
    errs.append(abs(E*E - p*p - m*m))           # 质量壳
    return max(errs)

def check_B002():
    """Noether 数值：自由 KG 场（1+1 维，η=diag(-1,+1)）
    L = (1/2)φ_t² - (1/2)φ_x² - (1/2)m²φ²
    正则能动张量（Noether，混合指标）：
      Θ^0_0 = φ_t²-L,  Θ^1_0 = -φ_tφ_x
      Θ^0_1 = φ_tφ_x,  Θ^1_1 = -φ_x²-L
    守恒：∂_0Θ^0_ν + ∂_1Θ^1_ν = 0（ν=0,1），场满足 KG 时精确成立
    """
    m = 1.0
    N, h = 60, 0.01        # 二阶中心差分截断 ~ h² ≈ 1e-4
    k = 1.0
    omega = math.sqrt(k*k + m*m)
    A, B = 1.0, 0.3
    def phi(x, t):
        return A*math.cos(k*x - omega*t) + B*math.sin(k*x - omega*t)
    def dphi(x, t, mu):
        if mu == 0:
            return (phi(x, t+h) - phi(x, t-h))/(2*h)
        return (phi(x+h, t) - phi(x-h, t))/(2*h)
    def Theta(x, t):
        ft, fx = dphi(x, t, 0), dphi(x, t, 1)
        Lv = 0.5*(ft*ft - fx*fx) - 0.5*m*m*phi(x, t)**2
        return [[ft*ft - Lv, ft*fx], [-ft*fx, -fx*fx - Lv]]
    worst = 0.0
    for i in range(2, N-2):
        x, t = i*h, 3*h
        # ∂_μΘ^μ_0 = ∂_1Θ^1_0 + ∂_0Θ^0_0
        dT0 = (Theta(x+h, t)[1][0]-Theta(x-h, t)[1][0])/(2*h) + \
              (Theta(x, t+h)[0][0]-Theta(x, t-h)[0][0])/(2*h)
        # ∂_μΘ^μ_1 = ∂_1Θ^1_1 + ∂_0Θ^0_1
        dT1 = (Theta(x+h, t)[1][1]-Theta(x-h, t)[1][1])/(2*h) + \
              (Theta(x, t+h)[0][1]-Theta(x, t-h)[0][1])/(2*h)
        worst = max(worst, abs(dT0), abs(dT1))
    return worst

if __name__ == "__main__":
    print("=== ch03 闵氏时空数值验证 ===")
    e1 = check_B001()
    e2 = check_B003()
    e3 = check_B002()
    print(f"B-001 随机 Lorentz 保范数 最大残差 = {e1:.3e}  {'PASS' if e1 < 1e-12 else 'FAIL'}")
    print(f"B-003 快度加法/γ/质量壳 最大残差 = {e2:.3e}  {'PASS' if e2 < 1e-12 else 'FAIL'}")
    print(f"B-002 Noether 能动张量守恒 最大残差 = {e3:.3e}  {'PASS' if e3 < 1e-3 else 'FAIL'}（限差分截断 h²）")
    print("结论: 洛伦兹保范数、快度加性、质量壳精确成立；平移对称 ⟹ 能动张量守恒（数值坐实）。")
