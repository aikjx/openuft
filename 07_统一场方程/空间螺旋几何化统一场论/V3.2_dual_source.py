#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 · 引力-电磁同源检验（统一场论核心主张数值实证）
================================================================
统一主张：同一 TUFT 包络标量场 ψ=σe^{-iωt} 的单一轮廓 σ(r)，同时源出
  (A) 电磁源：U(1) 相位电流 → 电荷 Q=2ω∫4πr²σ²dr（经 q0 耦合）；
  (B) 引力源：能动张量 → 场能量 E₀=∫4πr²[ω²σ²+σ'²+U(σ²)]dr（经 G 耦合）。
检验：Q 与 E₀ 均为同一 σ 的泛函，比值（固有特异荷）Q/E₀ 由理论锁定。
用稳定窗 ω∈[0.18,0.25] 多档实算，验证：
  1) 双源同包络：电荷密度 2ωσ² 与能量密度 ω²σ²+σ'²+U 共享同一 σ 包络，
     局域半径一致（R_charge≈R_energy）；
  2) 特异荷锁定：Q/E₀ 在该窗内 ≈ const（与 ω 弱依赖），为理论固有比值；
  3) 物理特异荷 = (q0/G)·(Q/E₀)，q0/G 为唯一外部自由比（诚实标注）。
"""
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location
_spec = spec_from_file_location("qr", __file__.replace("V3.2_dual_source.py", "V3.2_Qball_route2.py"))
qr = module_from_spec(_spec); _spec.loader.exec_module(qr)
V1, V2, M2, U = qr.V1, qr.V2, qr.M2, qr.U
shoot_sigma0 = qr.shoot_sigma0
integrate_full, simpson_int, RMAX, STEPS = qr.integrate_full, qr.simpson_int, qr.RMAX, qr.STEPS

def dual_source(omega, s0):
    h = RMAX / STEPS
    arr = integrate_full(s0, omega)
    rs = [mp.mpf("0")] + [h*mp.mpf(i) for i in range(1, STEPS+1)]
    darr = [mp.mpf("0")]*len(arr)
    for i in range(1, len(arr)-1):
        darr[i] = (arr[i+1]-arr[i-1])/(2*h)
    darr[0] = (arr[1]-arr[0])/h
    darr[-1] = (arr[-1]-arr[-2])/h
    # 电荷密度（EM 源）ρ_ch = 2ωσ²；能量密度（引力源）ρ_E = ω²σ²+σ'²+U
    rho_ch = [mp.mpf("2")*omega*arr[i]**2 for i in range(len(arr))]
    rho_E  = [omega*omega*arr[i]**2 + darr[i]**2 + U(arr[i]**2) for i in range(len(arr))]
    fQ = [mp.mpf("4")*mp.pi*rr*rr*rho_ch[i] for i, rr in enumerate(rs)]
    fE = [mp.mpf("4")*mp.pi*rr*rr*rho_E[i] for i, rr in enumerate(rs)]
    Q = simpson_int(fQ, h)
    E0 = simpson_int(fE, h)
    # 局域半径：累计 90% 的量
    def r90(fvals, tot):
        acc = mp.mpf("0")
        for i, rr in enumerate(rs):
            acc += fvals[i]*h
            if tot > 0 and acc >= mp.mpf("0.90")*tot:
                return rr
        return rs[-1]
    R_ch = r90(fQ, Q); R_E = r90(fE, E0)
    return Q, E0, R_ch, R_E

def main():
    mp.mp.dps = 25
    print("="*70)
    print("TUFT V3.2 · 引力-电磁同源检验（稳定窗 ω∈[0.18,0.25]）")
    print("V1=%s V2=%s M2=%s  RMAX=%s STEPS=%d" % (V1, V2, M2, RMAX, STEPS))
    print("-"*70)
    rows = []
    for om in ["0.1841","0.1900","0.2000","0.2105","0.2200","0.2300","0.2368"]:
        w = mp.mpf(om)
        s0 = shoot_sigma0(w)
        if s0 is None:
            print("  ω=%s 无解" % om); continue
        Q, E0, Rch, RE = dual_source(w, s0)
        rows.append((float(w), float(Q), float(E0), float(Q/E0), float(Rch), float(RE)))
        print("  ω=%.4f  Q=%.2f  E₀=%.2f  Q/E₀=%.4f  R_q=%.3f  R_E=%.3f  R_q/R_E=%.4f"
              % (float(w), float(Q), float(E0), float(Q/E0), float(Rch), float(RE), float(Rch/RE)))
    print("-"*70)
    if rows:
        ratios = [r[3] for r in rows]
        rmean = sum(ratios)/len(ratios)
        spread = max(ratios)-min(ratios)
        print("特异荷 Q/E₀：均值=%.4f  极差=%.4f  相对展宽=%.4f%%"
              % (rmean, spread, 100*spread/rmean))
        print("同包络 R_q/R_E：均值=%.4f（≈1 即双源同包络）"
              % (sum(r[4]/r[5] for r in rows)/len(rows)))
        print("物理特异荷 e/m=(q0/G)·(Q/E₀)，q0/G 为唯一外部自由比（诚实标注）")

if __name__ == "__main__":
    main()
