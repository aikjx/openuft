#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 · 稳定支玻色星质量-电荷关系（暗物质锚 G=0.0056）
============================================================
固定引力耦合 G=0.0056（< G*，暗物质候选稳定区），扫 ω 测稳定玻色星：
M(ω) 引力质量、Q(ω) 电荷、R99 质量半径、紧致度 2M/R99、ω_phys、M/M_max。
给出 TUFT 玻色星作为暗物质候选的质量-半径-电荷具体数值。
M_max 参考 = 0.633·M_Pl²/m（m=0.447 ⇒ 1.415，mini-boson 文献界，标自作用修正待明）。
"""
import os, time, json
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location

H = os.path.dirname(os.path.abspath(__file__))
_spec = spec_from_file_location("bss", os.path.join(H, "V3.2_bosonstar_solve.py"))
B = module_from_spec(_spec); _spec.loader.exec_module(B)
mp = B.mp

G = mp.mpf("0.0056")          # 暗物质锚（稳定区）
MSC = mp.mpf("0.4472135954999579")
MMAX_BENCH = mp.mpf("0.633") / MSC   # 1.4154

def measure(omega):
    """对给定 ω（G 固定）测稳定玻色星物理量。"""
    B.QR.RMAX = mp.mpf("20"); B.QR.STEPS = 800
    base = B.QR.shoot_sigma0(omega)
    if base is None:
        return None
    s0 = B.shoot_sigma0(omega, g=G, guess=base)
    if s0 is None:
        return None
    rs, ys = B.integrate(omega, s0, g=G)
    M = ys[-1][0]; Phi_inf = ys[-1][1]
    w_phys = omega * mp.exp(-Phi_inf)
    # Q via observables 逻辑（复用）
    h = B.RMAX / B.STEPS
    fQ = []
    for r, y in zip(rs, ys):
        m, Phi, sg, ds = y
        A = mp.mpf("1") - mp.mpf("2") * m / r
        fQ.append(B.P4PI * mp.mpf("2") * (omega * sg * sg * mp.exp(-Phi)) / mp.sqrt(A) * r * r)
    # 手动 simpson
    n = len(fQ) - 1
    if n % 2 == 1: n -= 1
    s = fQ[0] + fQ[n]
    for i in range(1, n, 2): s += mp.mpf("4") * fQ[i]
    for i in range(2, n - 1, 2): s += mp.mpf("2") * fQ[i]
    Q = s * h / mp.mpf("3")
    # R99 与紧致度
    fM = []
    for r, y in zip(rs, ys):
        m, Phi, sg, ds = y
        A = mp.mpf("1") - mp.mpf("2") * m / r
        rho = omega*omega*sg*sg*mp.exp(-mp.mpf("2")*Phi) + A*ds*ds + B.U(sg*sg)
        fM.append(B.P4PI * G * r * r * rho)
    acc = mp.mpf("0"); R99 = rs[-1]
    for r, fm in zip(rs, fM):
        acc += fm * h
        if acc >= mp.mpf("0.99") * M:
            R99 = r; break
    comp = mp.mpf("2") * M / R99
    mmax_r = M / MMAX_BENCH
    return (float(omega), float(s0), float(M), float(Q), float(R99), float(w_phys), float(comp), float(mmax_r))

def main():
    mp.mp.dps = 25
    print("="*72)
    print("TUFT V3.2 · 稳定支玻色星质量-电荷关系（G=0.0056 暗物质锚）")
    print("M_max 基准(0.633/m)=%.6f" % float(MMAX_BENCH))
    omegas = [mp.mpf(x) for x in ["0.18","0.19","0.20","0.21","0.22","0.23","0.24","0.25","0.27","0.29"]]
    rows = []; t0 = time.time()
    for w in omegas:
        r = measure(w)
        if r is None:
            print("ω=%.3f 未收敛" % float(w)); continue
        rows.append(r)
        print("ω=%.3f σ0=%.5f M=%.5f Q=%.5f R99=%.4f ω_phys=%.4f 2M/R99=%.4f M/Mmax=%.3f (%.0fs)"
              % (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7], time.time()-t0))
    json.dump(rows, open(os.path.join(H,"V3.2_bosonstar_MQ.json"),"w",encoding="utf-8"))
    print("="*72)
    print("落盘 V3.2_bosonstar_MQ.json：%d 个稳定玻色星" % len(rows))
    if rows:
        print("M范围 [%.4g, %.4g]；Q范围 [%.4g, %.4g]" %
              (min(r[2] for r in rows), max(r[2] for r in rows),
               min(r[3] for r in rows), max(r[3] for r in rows)))

if __name__ == "__main__":
    main()
