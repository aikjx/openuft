#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""临界引力耦合 G*(ω) —— 窄窗 σ0 扫描探测存在性（快）"""
import os, time, json
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location

H = os.path.dirname(os.path.abspath(__file__))
_spec = spec_from_file_location("bss", os.path.join(H, "V3.2_bosonstar_solve.py"))
B = module_from_spec(_spec); _spec.loader.exec_module(B)
mp = B.mp; mp.mp.dps = 18
B.RMAX = mp.mpf("16"); B.STEPS = 600

def exists(omega, g, base):
    """窄窗 σ0 扫描：解 σ0 贴近平直 base ⇒ 在 [0.85,1.06]×base 细扫找真实过零。"""
    def end(s0):
        try:
            rs, ys = B.integrate(omega, s0, g=mp.mpf(g))
            return ys[-1][2]
        except Exception:
            return None
    s0 = base * mp.mpf("0.85"); smax = base * mp.mpf("1.06")
    n = 40; step = (smax - s0) / n
    prev_v = None; prev_s = None
    for i in range(n + 1):
        cur = s0 + step * i
        v = end(cur)
        if v is None:
            prev_s, prev_v = cur, None; continue
        if prev_v is not None and prev_v * v < 0:
            return True
        prev_s, prev_v = cur, v
    return False

def find_Gstar(omega):
    B.QR.RMAX = mp.mpf("16"); B.QR.STEPS = 600
    base = B.QR.shoot_sigma0(omega)
    if base is None:
        return None
    lo, hi = mp.mpf("1e-4"), mp.mpf("1.0")
    if not exists(omega, lo, base):
        return None
    if exists(omega, hi, base):
        return None
    for _ in range(24):
        mid = mp.sqrt(lo * hi)
        if exists(omega, mid, base): lo = mid
        else: hi = mid
    return mp.sqrt(lo * hi), base

def main():
    print("="*60)
    print("TUFT V3.2 · 临界引力耦合 G*(ω)（窄窗扫描, dps=18）")
    omegas = [mp.mpf(x) for x in ["0.18","0.2064","0.25","0.30"]]
    rows = []; t0 = time.time()
    for w in omegas:
        r = find_Gstar(w)
        if r is None:
            print("ω=%.4f  G*: 未定位" % float(w)); continue
        Gs, base = r
        rows.append((float(w), float(Gs)))
        print("ω=%.4f  G*=%.6g  (%.0fs)" % (float(w), float(Gs), time.time()-t0))
    json.dump(rows, open(os.path.join(H,"V3.2_bosonstar_Gstar.json"),"w",encoding="utf-8"))
    print("="*60)
    print("落盘 V3.2_bosonstar_Gstar.json：%d 点" % len(rows))
    if rows:
        print("参考：解析估算 G*(M/M_max=1)=0.01398；G=0.0056 时 M/M_max=0.40（稳定暗物质候选）")

if __name__ == "__main__":
    main()
