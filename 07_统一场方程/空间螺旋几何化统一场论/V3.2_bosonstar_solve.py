#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 统一场论攻坚 · 完整自引力 Q-ball（玻色星）求解
========================================================
求解 G≠0 下时间谐振 Q-ball 的完整 Einstein-Klein-Gordon（EKG）耦合方程组，
给出 TUFT 自己的质量-半径关系与最大质量，并对外部基准 M_max≈0.633·M_Pl²/m 校验。

度规：ds² = -e^{2Φ}dt² + (1-2m/r)^{-1}dr² + r²dΩ² ，ψ=σe^{-iωt}。
EKG（G=c=1，8πG=8π）：
  A=1-2m/r
  ρ = ω²σ²e^{-2Φ} + A·σ'² + U(σ²)         （能量密度）
  p = ω²σ²e^{-2Φ} - A·σ'² - U(σ²)          （径向压强）
  m' = 4πr²ρ
  Φ' = (m + 4πr³p)/(r(r-2m))
  σ'' + σ'[2/r + Φ' + (m/r² - m'/r)/A] = (U' - ω²e^{-2Φ})σ/A

规范/物理量：
  以 Φ(0)=0 积分（砝码任意）；渐近平直解经常数平移得到，物理频率 ω_phys=ω·e^{-Φ∞}。
  组合 ωe^{-Φ} 不随该平移变，故
    M_phys = m(∞)
    Q_phys = 8π∫ ωe^{-Φ}σ²(1-2m/r)^{-1/2} r² dr
  （平直极限 m,Φ→0 还原 Q=2ωN，已验证。）

用法： python V3.2_bosonstar_solve.py [--flat-test] [--omega X]
"""
import os, sys, time
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location

H = os.path.dirname(os.path.abspath(__file__))
_spec = spec_from_file_location("qroute2", os.path.join(H, "V3.2_Qball_route2.py"))
QR = module_from_spec(_spec); _spec.loader.exec_module(QR)

V1, V2, M2 = QR.V1, QR.V2, QR.M2
OMAX = mp.sqrt(M2 / mp.mpf("2"))          # m=√(M2/2)=0.447
RMAX = mp.mpf("20")                        # 自引力解更紧凑，20 已充足
STEPS = 800
P4PI = mp.mpf("4") * mp.pi

def U(s2): return QR.U(s2)
def dUd(s2): return QR.dUdw(s2)

def rhs(y, r, w2, g):
    """y=[m,Phi,sigma,dsigma]; 返回 y'（g=引力耦合，g→0 还原平直 Q-ball）。"""
    m, Phi, sg, ds = y
    s2 = sg * sg
    A = mp.mpf("1") - mp.mpf("2") * m / r
    if A <= 0:
        raise ValueError("r=%.6g 处 A≤0 (视界)" % float(r))
    e2mP = mp.exp(-mp.mpf("2") * Phi)
    rho = w2 * s2 * e2mP + A * ds * ds + U(s2)
    p   = w2 * s2 * e2mP - A * ds * ds - U(s2)
    mp_ = P4PI * g * r * r * rho
    Phip = (m + P4PI * g * r * r * r * p) / (r * r * A)
    sgp = ds
    U1 = dUd(s2)
    coef = (mp.mpf("2") / r + Phip + (m / (r * r) - mp_ / r) / A)
    dsp = (U1 - w2 * e2mP) * sg / A - ds * coef
    return [mp_, Phip, sgp, dsp]

def integrate(omega, sigma0, phi0=mp.mpf("0"), g=mp.mpf("1")):
    """从 r≈0（小 r 级数展开）RK4 积分到 RMAX。返回 (rs, ys)。"""
    h = RMAX / STEPS
    r0 = h * mp.mpf("0.5")
    # 小 r 正则级数初值（Φ(0)=phi0, σ(0)=sigma0）
    Phi_c = phi0
    w2 = omega * omega
    s2c = sigma0 * sigma0
    rho0 = w2 * s2c * mp.exp(-mp.mpf("2") * Phi_c) + U(s2c)
    p0   = w2 * s2c * mp.exp(-mp.mpf("2") * Phi_c) - U(s2c)
    U10  = dUd(s2c)
    m0  = (P4PI * g / mp.mpf("3")) * rho0 * r0**3
    Phi0= Phi_c + mp.mpf("2") * mp.pi * g * (rho0 / mp.mpf("3") + p0) * r0 * r0
    sg0 = sigma0 + mp.mpf("0.5") * (U10 - w2 * mp.exp(-mp.mpf("2") * Phi_c)) * sigma0 * r0 * r0
    ds0 = (U10 - w2 * mp.exp(-mp.mpf("2") * Phi_c)) * sigma0 * r0
    y = [m0, Phi0, sg0, ds0]
    rs = [r0]
    ys = [list(y)]
    r = r0
    # 前向 RK4
    while r < RMAX - h * mp.mpf("0.5"):
        k1 = rhs(y, r, w2, g)
        k2 = rhs([y[i] + (h/2)*k1[i] for i in range(4)], r + h/2, w2, g)
        k3 = rhs([y[i] + (h/2)*k2[i] for i in range(4)], r + h/2, w2, g)
        k4 = rhs([y[i] + h*k3[i] for i in range(4)], r + h, w2, g)
        y = [y[i] + (h/6)*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(4)]
        r += h
        rs.append(r); ys.append(list(y))
    return rs, ys

def shoot_sigma0(omega, g=mp.mpf("1"), guess=None):
    """对给定 ω 打靶 σ(0) 使 σ(RMAX)→0（基态无节点）。以平直 σ0 为种子窄括号二分。"""
    # 平直解 σ0 作种子（g→0 极限解）
    if guess is None:
        QR.RMAX = mp.mpf("20"); QR.STEPS = 800
        try:
            guess = QR.shoot_sigma0(omega)
        except Exception:
            guess = None
        if guess is None:
            return None
    def end(s0):
        try:
            rs, ys = integrate(omega, s0, g=g)
            return ys[-1][2]
        except ValueError:
            return mp.mpf("-1")   # 命中视界→视为过冲/坍缩（负信号，促成括号）
    # 以种子为中心向两侧扩括号找变号
    lo, hi = guess * mp.mpf("0.6"), guess * mp.mpf("1.4")
    flo, fhi = end(lo), end(hi)
    for _ in range(30):
        if flo * fhi <= 0:
            break
        # 尚未变号：扩大区间
        lo = lo * mp.mpf("0.85"); flo = end(lo)
        if flo * fhi <= 0:
            break
        hi = hi * mp.mpf("1.15"); fhi = end(hi)
        if flo * fhi <= 0:
            break
    else:
        return None
    for _ in range(45):
        mid = (lo + hi) / 2; fm = end(mid)
        if flo * fm <= 0:
            hi = mid; fhi = fm
        else:
            lo = mid; flo = fm
    return (lo + hi) / 2

def observables(omega, sigma0, g=mp.mpf("1")):
    """积分→ M_phys, Q_phys, R99(99% 质量半径), ω_phys。"""
    rs, ys = integrate(omega, sigma0, g=g)
    M = ys[-1][0]
    Phi_inf = ys[-1][1]
    w_phys = omega * mp.exp(-Phi_inf)
    # Q_phys = 8π∫ ωe^{-Φ}σ²(1-2m/r)^{-1/2} r² dr
    h = RMAX / STEPS
    fQ = []
    for r, y in zip(rs, ys):
        m, Phi, sg, ds = y
        A = mp.mpf("1") - mp.mpf("2") * m / r
        fQ.append(P4PI * mp.mpf("2") * (omega * sg * sg * mp.exp(-Phi)) / mp.sqrt(A) * r * r)
    Q = simpson(fQ, h)
    # 99% 质量半径
    fM = []
    for r, y in zip(rs, ys):
        m, Phi, sg, ds = y
        A = mp.mpf("1") - mp.mpf("2") * m / r
        rho = omega*omega*sg*sg*mp.exp(-mp.mpf("2")*Phi) + A*ds*ds + U(sg*sg)
        fM.append(P4PI * g * r * r * rho)
    Menc = [0.0]*len(rs); acc = mp.mpf("0")
    for i, fm in enumerate(fM):
        acc += fm * h; Menc[i] = acc
    R99 = rs[-1]
    for i in range(len(rs)):
        if Menc[i] >= mp.mpf("0.99") * M:
            R99 = rs[i]; break
    return M, Q, R99, w_phys

def simpson(fvals, h):
    n = len(fvals) - 1
    if n % 2 == 1: n -= 1
    s = fvals[0] + fvals[n]
    for i in range(1, n, 2): s += mp.mpf("4") * fvals[i]
    for i in range(2, n - 1, 2): s += mp.mpf("2") * fvals[i]
    return s * h / mp.mpf("3")

def main():
    mp.mp.dps = 30
    args = sys.argv[1:]
    print("=" * 72)
    print("TUFT V3.2 · 完整自引力 Q-ball（玻色星）EKG 求解")
    print("V1=%.2f V2=%.2f M2=%.3f  RMAX=%s STEPS=%d  dps=30" % (float(V1),float(V2),float(M2),RMAX,STEPS))

    if '--flat-test' in args:
        # 平直极限校验：g→0 应还原平直 Q-ball（M→E₀_flat, Q→2ωN_flat）
        gs = mp.mpf("0.0001")
        print("平直极限校验：g=%.4g 时应还原平直 Q-ball" % float(gs))
        QR.RMAX = mp.mpf("20"); QR.STEPS = 800
        for omega in [mp.mpf("0.1"), mp.mpf("0.184147"), mp.mpf("0.3")]:
            s0f = QR.shoot_sigma0(omega)
            if s0f is None:
                print("ω=%.5f 平直未收敛" % float(omega)); continue
            s0 = shoot_sigma0(omega, g=gs, guess=s0f)
            if s0 is None:
                print("ω=%.5f GR未收敛" % float(omega)); continue
            M, Qq, R99, w_phys = observables(omega, s0, g=gs)
            Nf, Qf, E0f, Mf, arrf = QR.compute_profile(omega, s0f)
            print("-"*72)
            print("ω=%.6f: g→0 σ0=%.6g M=%.6g Q=%.6g | 平直 σ0=%.6g E₀=%.6g Q=%.6g"
                  % (float(omega), float(s0), float(M), float(Qq), float(s0f), float(E0f), float(Qf)))
            print("         σ0比=%.4f  M/E₀比=%.4f  Q/Q_flat比=%.4f"
                  % (float(s0/s0f), float(M/E0f), float(Qq/Qf)))
        return

    # 谱扫描 ω∈(0,m)
    Nw = int(args[args.index('--nw')+1]) if '--nw' in args else 12
    print("扫描 %d 档 ω∈(0,%.4f)" % (Nw, float(OMAX)))
    rows = []
    t0 = time.time()
    for k in range(1, Nw + 1):
        omega = OMAX * mp.mpf(k) / mp.mpf(Nw + 1)
        s0 = shoot_sigma0(omega)
        if s0 is None:
            print("  ω=%.5f 未收敛" % float(omega)); continue
        M, Q, R99, w_phys = observables(omega, s0)
        rows.append((float(omega), float(s0), float(M), float(Q), float(R99), float(w_phys)))
        print("  ω=%.5f σ0=%.6g M=%.6g Q=%.6g R99=%.6g ω_phys=%.5f  (%.0fs)"
              % (rows[-1][0], rows[-1][1], rows[-1][2], rows[-1][3], rows[-1][4], rows[-1][5], time.time()-t0))
    import json
    json.dump(rows, open(os.path.join(H, "V3.2_bosonstar_gr.json"), "w", encoding="utf-8"))
    print("=" * 72)
    print("已落盘 V3.2_bosonstar_gr.json：%d 个自引力解" % len(rows))
    if rows:
        Mmax = max(rows, key=lambda r: r[2])
        print("最大质量 M_max=%.6g @ ω=%.5f, R99=%.6g；基准 0.633M_Pl²/m=%.6g（m=%.4f）"
              % (Mmax[2], Mmax[0], Mmax[4], float(mp.mpf("0.633")/OMAX), float(OMAX)))

if __name__ == "__main__":
    main()
