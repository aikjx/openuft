#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补 G* 点（ω=0.16,0.22,0.28）使相界更平滑，合并入 Gstar 数据"""
import os, time, json
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location

H = os.path.dirname(os.path.abspath(__file__))
_spec = spec_from_file_location("bss", os.path.join(H, "V3.2_bosonstar_solve.py"))
B = module_from_spec(_spec); _spec.loader.exec_module(B)
mp = B.mp; mp.mp.dps = 15
B.RMAX = mp.mpf("16"); B.STEPS = 600

def exists(omega, g, base):
    def end(s0):
        try:
            rs, ys = B.integrate(omega, s0, g=mp.mpf(g))
            return ys[-1][2]
        except Exception:
            return None
    lo = base * mp.mpf("0.85"); hi = base * mp.mpf("1.06")
    n = 30; step = (hi - lo) / n
    prev_v = None
    for i in range(n + 1):
        cur = lo + step * i
        v = end(cur)
        if v is None:
            prev_v = None; continue
        if prev_v is not None and prev_v * v < 0:
            return True
        prev_v = v
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
    for _ in range(22):
        mid = mp.sqrt(lo * hi)
        if exists(omega, mid, base): lo = mid
        else: hi = mid
    return mp.sqrt(lo * hi)

def main():
    print("="*60)
    print("补 G*(ω) 点：0.16, 0.22, 0.28")
    jf = os.path.join(H, "V3.2_bosonstar_Gstar.json")
    existing = json.load(open(jf, encoding="utf-8")) if os.path.exists(jf) else []
    new_ws = ["0.16","0.22","0.28"]
    t0 = time.time()
    for ws in new_ws:
        w = mp.mpf(ws)
        gs = find_Gstar(w)
        if gs is None:
            print("ω=%s G* 未定位" % ws); continue
        existing.append([float(w), float(gs)])
        print("ω=%-5s G*=%.6g (%.0fs)" % (ws, float(gs), time.time()-t0))
    # 去重排序
    seen = set(); uniq = []
    for r in existing:
        k = (round(r[0],4), round(r[1],5))
        if k in seen: continue
        seen.add(k); uniq.append(r)
    uniq.sort(key=lambda r: r[0])
    json.dump(uniq, open(jf,"w",encoding="utf-8"))
    print("落盘 %d 点：%s" % (len(uniq), [[round(a,4),round(b,5)] for a,b in uniq]))

if __name__ == "__main__":
    main()
