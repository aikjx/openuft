#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 · TUFT 势自身最大质量 M_max 确定（G=0.0056 暗物质锚）
================================================================
玻色星支：ω→m 稀释 M→0；ω 降低 M 增至临界 M_max（坍缩/不稳定转折）。
固定 G=0.0056，向低 ω 扫至坍缩临界，取 M(ω) 峰值 = TUFT 势自身 M_max（G=0.0056）。
替换 mini-boson 文献界 1.415，使 M/Mmax 完全自洽。
窄窗打靶（解贴近平直 base，快）。
"""
import os, time, json
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location

H = os.path.dirname(os.path.abspath(__file__))
_spec = spec_from_file_location("bss", os.path.join(H, "V3.2_bosonstar_solve.py"))
B = module_from_spec(_spec); _spec.loader.exec_module(B)
mp = B.mp

G = mp.mpf("0.0056")

def shoot_narrow(omega, g, base):
    """窄窗打靶：解 σ0 贴近 base，在 [0.8,1.1]×base 二分精化。返回 σ0 或 None。"""
    def end(s0):
        try:
            rs, ys = B.integrate(omega, s0, g=mp.mpf(g))
            return ys[-1][2]
        except Exception:
            return None
    lo = base * mp.mpf("0.80"); hi = base * mp.mpf("1.10")
    n = 30; step = (hi - lo) / n
    prev_v = None; prev_s = None; brk = None
    for i in range(n + 1):
        cur = lo + step * i
        v = end(cur)
        if v is None:
            prev_s, prev_v = cur, None; continue
        if prev_v is not None and prev_v * v < 0:
            brk = (prev_s, cur, prev_v, v); break
        prev_s, prev_v = cur, v
    if brk is None:
        return None
    blo, bhi, fblo, fbhi = brk
    for _ in range(50):
        mid = (blo + bhi) / 2; fm = end(mid)
        if fm is None:
            bhi = mid; continue
        if fblo * fm <= 0: bhi, fbhi = mid, fm
        else: blo, fblo = mid, fm
    return (blo + bhi) / 2

def measure(omega, base):
    s0 = shoot_narrow(omega, G, base)
    if s0 is None:
        return None
    rs, ys = B.integrate(omega, s0, g=G)
    M = ys[-1][0]; Phi_inf = ys[-1][1]
    w_phys = omega * mp.exp(-Phi_inf)
    h = B.RMAX / B.STEPS
    # R99
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
    return (float(omega), float(s0), float(M), float(R99), float(w_phys), float(mp.mpf("2")*M/R99))

def main():
    mp.mp.dps = 25
    B.RMAX = mp.mpf("20"); B.STEPS = 800
    B.QR.RMAX = mp.mpf("20"); B.QR.STEPS = 800
    print("="*70)
    print("TUFT V3.2 · TUFT 势自身 M_max（G=0.0056），向低 ω 扫至坍缩临界")
    omegas = [mp.mpf(x) for x in
        ["0.29","0.27","0.25","0.24","0.23","0.22","0.21","0.20","0.19","0.18",
         "0.17","0.16","0.15","0.14","0.13","0.12","0.11","0.10"]]
    rows = []; t0 = time.time()
    for w in omegas:
        base = B.QR.shoot_sigma0(w)
        if base is None:
            print("ω=%.2f 平直无种子，跳过" % float(w)); continue
        r = measure(w, base)
        if r is None:
            print("ω=%.2f 无自引力解（坍缩/无过零）" % float(w)); continue
        rows.append(r)
        print("ω=%.2f σ0=%.5f M=%.5f R99=%.4f ω_phys=%.4f 2M/R99=%.4f (%.0fs)"
              % (r[0],r[1],r[2],r[3],r[4],r[5], time.time()-t0))
    json.dump(rows, open(os.path.join(H,"V3.2_bosonstar_Mmax.json"),"w",encoding="utf-8"))
    print("="*70)
    if rows:
        Mmax = max(rows, key=lambda r: r[2])
        print("TUFT 势 M_max(G=0.0056)=%.6g @ ω=%.3f" % (Mmax[2], Mmax[0]))
        print("对比 mini-boson 文献界 0.633/m=%.6f：比值=%.4f" % (float(mp.mpf("0.633")/mp.mpf("0.4472135954999579")), Mmax[2]/(mp.mpf("0.633")/mp.mpf("0.4472135954999579"))))
        print("落盘 V3.2_bosonstar_Mmax.json：%d 点" % len(rows))

if __name__ == "__main__":
    main()
