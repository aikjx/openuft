#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
求解器验证：纯质量势 mini-boson star（无自作用 U=½m²σ²）
================================================================
验证 EKG 求解器在强引力区（g=1）的正确性：对已知 mini-boson star，
最大质量应为 M_max≈0.633·M_Pl²/m。若本求解器还原该界，则强引力求解可信，
TUFT 六次势在 g=1 无解的结论才是物理的（而非数值假象）。
m=√(M2/2)=0.447，M_max 基准 = 0.633/0.447 = 1.416。
"""
import os, io
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location

H = os.path.dirname(os.path.abspath(__file__))
_spec = spec_from_file_location("bss", os.path.join(H, "V3.2_bosonstar_solve.py"))
B = module_from_spec(_spec); _spec.loader.exec_module(B)

MSC = mp.mpf("0.4472135954999579")   # m=√(0.4/2)
def Umini(s2): return mp.mpf("0.5") * MSC * MSC * s2
def dUmini(s2): return mp.mpf("0.5") * MSC * MSC

# 用模块的 rhs/integrate，但替换势函数
B.U = Umini
B.dUd = dUmini
RMAX = mp.mpf("60"); STEPS = 2000
B.RMAX = RMAX; B.STEPS = STEPS

def solve_one(omega):
    # 手动打靶：对给定 ω 求 σ0
    def end(s0):
        try:
            rs, ys = B.integrate(omega, s0, g=mp.mpf("1"))
            return ys[-1][2]
        except Exception:
            return mp.mpf("-1")
    # 扫描找根区间
    lo = None; hi = None
    s0 = mp.mpf("0.001"); step = mp.mpf("0.01")
    s_prev = s0; e_prev = end(s0)
    while s0 < mp.mpf("1.0"):
        e = end(s0)
        if (e_prev is not None) and (e_prev * e < 0):
            lo, hi = s_prev, s0; break
        s_prev, e_prev = s0, e; s0 += step
    if lo is None:
        return None
    flo = end(lo); fhi = end(hi)
    for _ in range(60):
        mid = (lo + hi) / 2; fm = end(mid)
        if flo * fm <= 0: hi = mid; fhi = fm
        else: lo = mid; flo = fm
    return (lo + hi) / 2

def main():
    mp.mp.dps = 30
    print("验证 mini-boson star（U=½m²σ², m=%.6f, g=1）" % float(MSC))
    print("已知最大质量界 M_max≈0.633·M_Pl²/m = %.6f" % float(mp.mpf("0.633")/MSC))
    rows = []
    for wstr in ["0.05","0.10","0.15","0.20","0.25","0.30","0.35","0.40","0.43","0.445"]:
        w = mp.mpf(wstr)
        s0 = solve_one(w)
        if s0 is None:
            print("ω=%.3f 未收敛" % float(w)); continue
        rs, ys = B.integrate(w, s0, g=mp.mpf("1"))
        M = ys[-1][0]
        Phi_inf = ys[-1][1]
        w_phys = w * mp.exp(-Phi_inf)
        rows.append((float(w), float(s0), float(M), float(w_phys)))
        print("ω=%.3f σ0=%.5f M=%.6g ω_phys=%.4f" % (rows[-1][0], rows[-1][1], rows[-1][2], rows[-1][3]))
    if rows:
        Mmax = max(rows, key=lambda r: r[2])
        print("-"*60)
        print("本求解器 M_max=%.6g @ ω=%.3f" % (Mmax[2], Mmax[0]))
        print("基准 0.633M_Pl²/m=%.6f   比值=%.4f" % (float(mp.mpf("0.633")/MSC), Mmax[2]/(mp.mpf("0.633")/MSC)))
        print("验证：比值≈1 ⇒ 求解器强引力区正确；否则需修求解器。")

if __name__ == "__main__":
    main()
