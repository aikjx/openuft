#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""M_max(G) 标度律 —— 精简版（dps=15, 4 个 G, 每 G 少 ω 点）"""
import os, time, json
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location

H = os.path.dirname(os.path.abspath(__file__))
_spec = spec_from_file_location("bss", os.path.join(H, "V3.2_bosonstar_solve.py"))
B = module_from_spec(_spec); _spec.loader.exec_module(B)
mp = B.mp; mp.mp.dps = 15
B.RMAX = mp.mpf("16"); B.STEPS = 600
B.QR.RMAX = mp.mpf("16"); B.QR.STEPS = 600

def shoot_narrow(omega, g, base):
    def end(s0):
        try:
            rs, ys = B.integrate(omega, s0, g=mp.mpf(g))
            return ys[-1][2]
        except Exception:
            return None
    lo = base * mp.mpf("0.80"); hi = base * mp.mpf("1.10")
    n = 24; step = (hi - lo) / n
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
    for _ in range(40):
        mid = (blo + bhi) / 2; fm = end(mid)
        if fm is None:
            bhi = mid; continue
        if fblo * fm <= 0: bhi, fbhi = mid, fm
        else: blo, fblo = mid, fm
    return (blo + bhi) / 2

def measure(omega, g, base):
    s0 = shoot_narrow(omega, g, base)
    if s0 is None:
        return None
    rs, ys = B.integrate(omega, s0, g=mp.mpf(g))
    M = ys[-1][0]
    h = B.RMAX / B.STEPS
    fM = []
    for r, y in zip(rs, ys):
        m, Phi, sg, ds = y
        A = mp.mpf("1") - mp.mpf("2") * m / r
        rho = omega*omega*sg*sg*mp.exp(-mp.mpf("2")*Phi) + A*ds*ds + B.U(sg*sg)
        fM.append(B.P4PI * g * r * r * rho)
    acc = mp.mpf("0"); R99 = rs[-1]
    for r, fm in zip(rs, fM):
        acc += fm * h
        if acc >= mp.mpf("0.99") * M:
            R99 = r; break
    return (float(omega), float(s0), float(M), float(R99), float(mp.mpf("2")*M/R99))

def Mmax_for_G(g):
    omegas = [mp.mpf(x) for x in ["0.30","0.26","0.22","0.18","0.16","0.14","0.12"]]
    pts = []
    for w in omegas:
        base = B.QR.shoot_sigma0(w)
        if base is None:
            continue
        r = measure(w, g, base)
        if r is None:
            continue
        pts.append(r)
    if not pts:
        return None
    mx = max(pts, key=lambda r: r[2])
    return mx, pts

def main():
    print("="*66)
    print("TUFT V3.2 · 最大质量 M_max(G) 标度律（精简, dps=15）")
    Gs = ["0.001","0.0056","0.014","0.02"]
    rows = []; allpts = {}; t0 = time.time()
    for gstr in Gs:
        g = mp.mpf(gstr)
        r = Mmax_for_G(g)
        if r is None:
            print("G=%-6s 无稳定支解" % gstr); continue
        mx, pts = r
        rows.append((float(g), mx[2], mx[0], mx[4]))
        allpts[gstr] = pts
        print("G=%-6s  M_max=%.6g @ ω=%.3f 紧致=%.4f (%d点, %.0fs)"
              % (gstr, mx[2], mx[0], mx[4], len(pts), time.time()-t0))
    json.dump({"Mmax":rows, "branches":{k:[[p[0],p[2]] for p in v] for k,v in allpts.items()}},
              open(os.path.join(H,"V3.2_bosonstar_MmaxG.json"),"w",encoding="utf-8"))
    print("="*66)
    print("落盘 V3.2_bosonstar_MmaxG.json；%d 个 G" % len(rows))
    if len(rows) >= 2:
        g1, m1 = rows[0][0], rows[0][1]; g2, m2 = rows[1][0], rows[1][1]
        alpha = mp.log(mp.mpf(m2)/mp.mpf(m1))/mp.log(mp.mpf(g2)/mp.mpf(g1))
        print("前两点标度指数 α=%.3f (M_max ∝ G^α)" % float(alpha))
        if len(rows) >= 4:
            g3, m3 = rows[2][0], rows[2][1]; g4, m4 = rows[3][0], rows[3][1]
            a34 = mp.log(mp.mpf(m4)/mp.mpf(m3))/mp.log(mp.mpf(g4)/mp.mpf(g3))
            print("后两点标度指数 α=%.3f" % float(a34))

if __name__ == "__main__":
    main()
