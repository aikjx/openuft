# -*- coding: utf-8 -*-
"""§15 前置审计：光速螺旋场标架的 Frenet 自洽性 + 真空 Maxwell 兼容性。

审计四项（红线：仅报告数值事实，不粉饰为 PASS）：
  [A] §13 显式标架是否满足它自己声明的 Frenet-Serret 方程（kappa=K cos, tau=K sin）
  [B] 修正标架（绕固定 Darboux 轴匀角速转动）的 Frenet 残差
  [C] §13 场拟设 E=E0(e1+i e2)e^{i(kz-wt)} 的真空 Maxwell 残差
        R1=div E, R2=div B, R3=curl E - i w B, R4=curl B + i(w/c^2) E
  [D] 对合法解（若存在）核验守恒律：div<S>=0, div<T>=0

记号：相量 E~(z) 满足 E(r,t)=Re[E~(z) e^{-i w t}]；场仅依赖 z（§13 取 s=z）。
"""
import math
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

c = 299792458.0
mu0 = 4.0 * math.pi * 1e-7
eps0 = 1.0 / (mu0 * c ** 2)
hbar = 1.054571817e-34
TWO_PI = 2.0 * math.pi


# ==================================================================
# 两套显式标架
# ==================================================================
def frame_s13(z, K, theta):
    """§13 文档 Part B / momentum_darboux.py 中给出的显式标架（原版）。"""
    phi = K * z
    e1 = np.array([math.cos(phi), math.sin(phi), 0.0])
    e2 = np.array([-math.sin(phi) * math.cos(theta),
                   math.cos(phi) * math.cos(theta),
                   math.sin(theta)])
    e3 = np.array([-math.sin(phi) * math.sin(theta),
                   math.cos(phi) * math.sin(theta),
                   -math.cos(theta)])
    return e1, e2, e3


def frame_correct(z, K, theta):
    """修正标架：绕固定 Darboux 轴 n=z_hat 以角速率 K 匀角速转动。
    e1(0)=(cos th,0,sin th), e2(0)=(0,1,0), e3(0)=(-sin th,0,cos th)
    """
    phi = K * z
    e1 = np.array([math.cos(theta) * math.cos(phi),
                   math.cos(theta) * math.sin(phi),
                   math.sin(theta)])
    e2 = np.array([-math.sin(phi), math.cos(phi), 0.0])
    e3 = np.array([-math.sin(theta) * math.cos(phi),
                   -math.sin(theta) * math.sin(phi),
                   math.cos(theta)])
    return e1, e2, e3


def frame_gen(z, q, theta):
    """通用：绕 z_hat 以角速率 q 转动（frame_correct 取 q=K）。"""
    phi = q * z
    return frame_correct(z, q, theta) if False else (
        np.array([math.cos(theta) * math.cos(phi),
                  math.cos(theta) * math.sin(phi), math.sin(theta)]),
        np.array([-math.sin(phi), math.cos(phi), 0.0]),
        np.array([-math.sin(theta) * math.cos(phi),
                  -math.sin(theta) * math.sin(phi), math.cos(theta)]),
    )


# ==================================================================
# [A][B] Frenet 残差
# ==================================================================
def frenet_residual(frame_fn, K, theta, z0=0.0, h=None):
    """数值 d/ds vs Frenet 方程 de1/ds=k e2, de2/ds=-k e1+tau e3, de3/ds=-tau e2。"""
    if h is None:
        h = 1e-9 / K
    kappa = K * math.cos(theta)
    tau = K * math.sin(theta)

    e1p, e2p, e3p = frame_fn(z0 + h, K, theta)
    e1m, e2m, e3m = frame_fn(z0 - h, K, theta)
    d1 = (e1p - e1m) / (2 * h)
    d2 = (e2p - e2m) / (2 * h)
    d3 = (e3p - e3m) / (2 * h)

    e1, e2, e3 = frame_fn(z0, K, theta)
    r1 = np.linalg.norm(d1 - kappa * e2) / K
    r2 = np.linalg.norm(d2 - (-kappa * e1 + tau * e3)) / K
    r3 = np.linalg.norm(d3 - (-tau * e2)) / K
    # 正交性
    orth = max(abs(np.dot(e1, e2)), abs(np.dot(e2, e3)), abs(np.dot(e3, e1)),
               abs(np.linalg.norm(e1) - 1), abs(np.linalg.norm(e2) - 1),
               abs(np.linalg.norm(e3) - 1))
    return max(r1, r2, r3), orth, (r1, r2, r3)


def audit_frame():
    print("=" * 78)
    print("[A][B] 显式标架的 Frenet-Serret 自洽性（残差已用 1/K 无量纲化）")
    print("=" * 78)
    lam = 500e-9
    K = TWO_PI / lam
    print("  theta    §13原版 残差    修正版 残差    §13正交性   修正正交性")
    for deg in [0, 15, 30, 45, 60, 75, 89]:
        th = math.radians(deg)
        r_s13, o_s13, _ = frenet_residual(frame_s13, K, th)
        r_cor, o_cor, _ = frenet_residual(frame_correct, K, th)
        flag = "  <-- 原版失效" if r_s13 > 1e-6 else ""
        print(f"  {deg:3d}deg   {r_s13:.6e}     {r_cor:.6e}     "
              f"{o_s13:.2e}      {o_cor:.2e}{flag}")
    print("  --> §13 原版仅在 theta=0 成立；修正版全角度机器精度成立。")


# ==================================================================
# [C] Maxwell 残差
# ==================================================================
def phasor_fields(z, K, theta, q, k, E0=1.0, corrected=True):
    """相量 E~(z)=E0(e1+i e2)e^{i k z}；B~=(1/c) e3 x E~。
    q: 标架绕 z 轴的转动速率;  k: 指数中的波数。§13 原版 q=K, k=K。
    """
    if corrected:
        e1, e2, e3 = frame_correct(z, q, theta)
    else:
        e1, e2, e3 = frame_s13(z, q, theta)
    psi = e1 + 1j * e2
    E = E0 * psi * np.exp(1j * k * z)
    B = np.cross(e3, E) / c
    return E, B, e3


def maxwell_residual(K, theta, q, k, z0=0.0, E0=1.0, corrected=True):
    """真空 Maxwell 残差（相量，e^{-i w t}）：
    R1=div E ; R2=div B ; R3=curl E - i w B ; R4=curl B + i(w/c^2) E
    场仅依赖 z： div E = dEz/dz ; curl E = (-dEy/dz, dEx/dz, 0)
    """
    w = c * K
    h = 1e-9 / K
    Ep, Bp, _ = phasor_fields(z0 + h, K, theta, q, k, E0, corrected)
    Em, Bm, _ = phasor_fields(z0 - h, K, theta, q, k, E0, corrected)
    E, B, _ = phasor_fields(z0, K, theta, q, k, E0, corrected)

    dE = (Ep - Em) / (2 * h)
    dB = (Bp - Bm) / (2 * h)

    R1 = dE[2]                                   # div E = dEz/dz
    R2 = dB[2]                                   # div B = dBz/dz
    curlE = np.array([-dE[1], dE[0], 0.0])
    curlB = np.array([-dB[1], dB[0], 0.0])
    R3 = np.linalg.norm(curlE - 1j * w * B)
    R4 = np.linalg.norm(curlB + 1j * (w / c ** 2) * E)

    scale = max(np.linalg.norm(dE), K * np.linalg.norm(E), 1e-300)
    return dict(R1=abs(R1) / scale, R2=abs(R2) / scale,
                R3=R3 / scale, R4=R4 / scale,
                Ez_over_E=abs(E[2]) / np.linalg.norm(E))


def audit_maxwell():
    lam = 500e-9
    K = TWO_PI / lam
    print("\n" + "=" * 78)
    print("[C] §13 场拟设的真空 Maxwell 兼容性（残差相对尺度归一）")
    print("=" * 78)
    print("  构型                          R1=divE     R2=divB     R3=Faraday  R4=Ampere   |Ez|/|E|")
    cases = [
        ("§13 原版 θ=0°   q=K,k=K", 0.0, K, K, False),
        ("§13 原版 θ=45°  q=K,k=K", math.radians(45), K, K, False),
        ("修正标架 θ=0°   q=K,k=K", 0.0, K, K, True),
        ("修正标架 θ=45°  q=K,k=K", math.radians(45), K, K, True),
        ("修正 θ=0°  q=K, k=K+q(补偿)", 0.0, K, 2 * K, True),
        ("修正 θ=45° q=K, k=K+q(补偿)", math.radians(45), K, 2 * K, True),
    ]
    for name, th, q, k, corr in cases:
        r = maxwell_residual(K, th, q, k, corrected=corr)
        print(f"  {name:34s} {r['R1']:.3e}  {r['R2']:.3e}  {r['R3']:.3e}  "
              f"{r['R4']:.3e}  {r['Ez_over_E']:.3e}")
    print("  --> 真空要求四项残差 ~0。R1≠0 意味着存在非零电荷密度 rho=eps0*div E。")


# ==================================================================
# [D] 守恒律核验（对合法真空解）
# ==================================================================
def conservation_check(K, theta, q, k, corrected=True, E0=1.0):
    """时均守恒律： div<S>=0（能量）, div·<T>=0（动量）。
    相量时均： <S> = (1/2mu0) Re[E x B*] ; <T_ij> = (1/2)Re[eps0(E_i E_j* - 1/2 dij |E|^2)
              + (1/mu0)(B_i B_j* - 1/2 dij |B|^2)]
    """
    h = 1e-9 / K
    z0 = 0.0

    def S_of(z):
        E, B, _ = phasor_fields(z, K, theta, q, k, E0, corrected)
        return (0.5 / mu0) * np.real(np.cross(E, np.conj(B)))

    def T_of(z):
        E, B, _ = phasor_fields(z, K, theta, q, k, E0, corrected)
        T = np.zeros((3, 3), dtype=complex)
        for i in range(3):
            for j in range(3):
                T[i, j] = 0.5 * np.real(
                    eps0 * (E[i] * np.conj(E[j]) - 0.5 * (i == j) * np.dot(E, np.conj(E)))
                    + (1.0 / mu0) * (B[i] * np.conj(B[j]) - 0.5 * (i == j) * np.dot(B, np.conj(B))))
        return T

    dS = (S_of(z0 + h) - S_of(z0 - h)) / (2 * h)
    Tp, Tm = T_of(z0 + h), T_of(z0 - h)
    dT = (Tp - Tm) / (2 * h)
    divT = np.array([dT[0, 2], dT[1, 2], dT[2, 2]])  # 仅有 z 依赖 -> div T = dT_ij/dz (j=z)

    S0 = S_of(z0)
    T0 = T_of(z0)
    sS = max(np.linalg.norm(S0), 1e-300)
    sT = max(abs(T0).max(), 1e-300)
    return dict(divS=abs(dS[2]) / (sS * K), divT=np.linalg.norm(divT) / (sT * K),
                S=np.linalg.norm(S0), Sz=S0[2])


def audit_conservation():
    lam = 500e-9
    K = TWO_PI / lam
    print("\n" + "=" * 78)
    print("[D] 时均守恒律核验（div<S>=0 能量, div·<T>=0 动量；相对尺度归一）")
    print("=" * 78)
    print("  构型                          div<S>/K|S|   div<T>/K|T|   |<S>|       <S>_z")
    cases = [
        ("§13 原版 θ=45° q=K,k=K", math.radians(45), K, K, False),
        ("修正 θ=0°  q=K, k=K+q", 0.0, K, 2 * K, True),
        ("修正 θ=45° q=K, k=K+q", math.radians(45), K, 2 * K, True),
    ]
    for name, th, q, k, corr in cases:
        r = conservation_check(K, th, q, k, corr)
        print(f"  {name:34s} {r['divS']:.3e}     {r['divT']:.3e}     "
              f"{r['S']:.4e}  {r['Sz']:.4e}")
    print("  --> 仅当 Maxwell 残差为零时守恒律才成立；否则出现源项（非守恒）。")


# ==================================================================
def main():
    print("=" * 78)
    print("§15 前置审计 —— Frenet 自洽性 + Maxwell 兼容性 + 守恒律")
    print("=" * 78)
    audit_frame()
    audit_maxwell()
    audit_conservation()
    print("\n=== 审计完成 ===")


if __name__ == "__main__":
    main()
