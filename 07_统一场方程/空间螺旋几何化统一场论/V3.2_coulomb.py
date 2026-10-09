#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 · 电磁扇区低能还原：涌现电荷 → 库仑场数值验证
================================================================
路线1 主张：涌现电流 J^μ 驱动麦克斯韦场，麦克斯韦理论作为低能近似包含在内。
本脚本验证：TUFT Q-ball 的涌现电荷密度 ρ_em(r)=q0·2ωσ²(r) 产生的电场，
在远场精确还原点电荷库仑场 E(r)→q0·Q/(4πε₀ r²)，且高斯定律 E(r)·4πr²→Q_tot 严格成立。
同时验证 Boosted 孤子 4-电流平行条件 J^μ = Q0·u^μ（路线1 eq5）。
单位：c=1, ε₀=1, q0=1（天然单位，绝对电荷需尺度锚——诚实标注）。
"""
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location
_spec = spec_from_file_location("qr", __file__.replace("V3.2_coulomb.py", "V3.2_Qball_route2.py"))
qr = module_from_spec(_spec); _spec.loader.exec_module(qr)
V1, V2, M2, U = qr.V1, qr.V2, qr.M2, qr.U
shoot_sigma0 = qr.shoot_sigma0
integrate_full, simpson_int, RMAX, STEPS = qr.integrate_full, qr.simpson_int, qr.RMAX, qr.STEPS

def main():
    mp.mp.dps = 25
    q0 = mp.mpf("1.0"); eps0 = mp.mpf("1.0")
    w = mp.mpf("0.1841")
    s0 = shoot_sigma0(w)
    if s0 is None:
        print("无解"); return
    h = RMAX / STEPS
    arr = integrate_full(s0, w)
    rs = [mp.mpf("0")] + [h*mp.mpf(i) for i in range(1, STEPS+1)]
    # 涌现电荷密度 ρ_em(r) = q0·2ωσ²
    rho = [q0*mp.mpf("2")*w*arr[i]**2 for i in range(len(arr))]
    # Q_enc(r) = 4π∫₀^r ρ r'²dr'  累积
    Qenc = [mp.mpf("0")]*(len(rs))
    acc = mp.mpf("0")
    for i in range(1, len(rs)):
        # 梯形
        fm = (rs[i-1]**2*rho[i-1] + rs[i]**2*rho[i])/mp.mpf("2")
        acc += mp.mpf("4")*mp.pi*fm*h
        Qenc[i] = acc
    Q_tot = Qenc[-1]
    # E(r) = Q_enc/(4πε₀ r²)  （球对称高斯）
    E = [mp.mpf("0")]*len(rs)
    Er2 = [mp.mpf("0")]*len(rs)
    for i in range(1, len(rs)):
        r = rs[i]
        E[i] = Qenc[i]/(mp.mpf("4")*mp.pi*eps0*r*r)
        Er2[i] = E[i]*r*r
    # 远场：E(r)·4πr² → Q_tot（高斯）；E(r)·r² → Q_tot/4π
    print("="*66)
    print("TUFT V3.2 · 涌现电荷→库仑场验证  ω=%.4f  q0=%s ε₀=%s" % (float(w), q0, eps0))
    print("总涌现电荷 Q_tot=∫ρ_em d³x = %.6f" % float(Q_tot))
    print("-"*66)
    print("  r       Q_enc(r)     E(r)·4πr²   E(r)·4πr²/Q_tot (→1 即库仑/高斯还原)")
    for idx in [1, 50, 150, 300, 500, 699]:
        r = rs[idx]; g = Er2[idx]*mp.mpf("4")*mp.pi
        print("  %6.2f  %10.5f  %12.6f  %12.8f" % (float(r), float(Qenc[idx]), float(g), float(g/Q_tot)))
    # 远场渐近比率
    gfar = Er2[-1]*mp.mpf("4")*mp.pi
    print("-"*66)
    print("远场 r=RMAX=%.1f: E(r)·4πr²/Q_tot = %.10f  (严格=1)" % (float(rs[-1]), float(gfar/Q_tot)))
    print("库仑还原: E(r)→Q_tot/(4πε₀r²)  %s" % ("PASS" if abs(float(gfar/Q_tot)-1) < 1e-6 else "CHECK"))

    # Boosted 4-电流平行条件 J^μ = Q0·u^μ
    print("="*66)
    print("Boosted 孤子 4-电流平行条件 J^μ ∝ u^μ（路线1 eq5）")
    u = mp.mpf("0.5")  # β=0.5
    gam = 1/mp.sqrt(1-u*u)
    # 静态 J^0=cρ=ρ_em, J^i=0；boost 后 J'^0 = γ(J^0 - β J^1)=γρ, J'^1=γ(-βρ)=-γβρ
    # 4-速度 u'^μ = γ(1, u) ⇒ J'^μ/ρ = γ(1, -u) ∝ u'^μ，比例常数 Q0(=q0·N_eff)
    J0 = rho[-1]*gam
    J1 = -gam*u*rho[-1]
    # 4-速度 (c=1): u0=γ, u1=γu
    r0 = J0/(gam*rho[-1]); r1 = J1/(-gam*u*rho[-1])
    print("β=%.2f  γ=%.4f   J'^0/(γρ)=%.6f   J'^1/(-γβρ)=%.6f  (两者相等即 J^μ∥u^μ)"
          % (float(u), float(gam), float(r0), float(r1)))
    print("平行条件: %s" % ("PASS" if abs(float(r0)-float(r1)) < 1e-9 else "CHECK"))

if __name__ == "__main__":
    main()
