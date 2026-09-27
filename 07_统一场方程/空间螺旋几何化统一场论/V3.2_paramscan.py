#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 方向B · 参数空间稳定相图（min E₀/Q vs m 扫描）
====================================================================
对「有下界六次势 + 质量项」修复候选，在 (V1, V2, M2) 参数空间扫描，
判定电荷稳定：对每个参数集求 E₀/Q(ω) 的最小值，对比衰变阈值 m=√(M2/2)。
稳定性指标 S = min(E₀/Q) / m ：S<1 稳定、S>1 可衰变。
约束（Q-ball 存在）：V1² > 4·M2·V2；ω 上界 √(M2/2)。
基线自检：(V1=1.2,V2=0.4,M2=0.4) 应得 S≈0.434/0.447≈0.971（稳定）。
用法： python V3.2_paramscan.py [dps]
"""
import sys, json, os
import mpmath as mp

V1_FIX = mp.mpf("1.2")
RMAX = mp.mpf("13"); STEPS = 520
SHOOT_IT = 40

def U(w, V1, V2, M2): return mp.mpf("0.5")*M2*w - (V1/mp.mpf("4"))*w**2 + (V2/mp.mpf("6"))*w**3
def dUdw(w, V1, V2, M2): return mp.mpf("0.5")*M2 - (V1/mp.mpf("2"))*w + (V2/mp.mpf("2"))*w**2
def f(s, om, V1, V2, M2): return (dUdw(s*s, V1, V2, M2) - om*om)*s
def rhs(r, s, ds, om, V1, V2, M2):
    if r <= mp.mpf("1e-24"): return f(s, om, V1, V2, M2)/mp.mpf("3")
    return -(mp.mpf("2")/r)*ds + f(s, om, V1, V2, M2)
def integrate_full(s0, om, V1, V2, M2):
    h = RMAX/STEPS
    r = h; f0 = f(s0, om, V1, V2, M2)
    s = s0 + (f0/mp.mpf("6"))*h*h; ds = (f0/mp.mpf("3"))*h
    for _ in range(STEPS-1):
        k1 = rhs(r,s,ds,om,V1,V2,M2); k2 = rhs(r+h/2, s+(h/2)*ds, ds+(h/2)*k1, om,V1,V2,M2)
        k3 = rhs(r+h/2, s+(h/2)*(ds+(h/2)*k1), ds+(h/2)*k2, om,V1,V2,M2)
        k4 = rhs(r+h, s+h*(ds+(h/2)*k2), ds+h*k3, om,V1,V2,M2)
        ds += (h/6)*(k1+2*k2+2*k3+k4); s += h*ds; r += h
    return s
def end(s0, om, V1, V2, M2): return integrate_full(s0, om, V1, V2, M2)

def shoot(omega, V1, V2, M2, center):
    if center is None:
        lo0, hi0, stp = mp.mpf("0.05"), mp.mpf("3.2"), mp.mpf("0.06")
    else:
        lo0, hi0, stp = center - mp.mpf("0.3"), center + mp.mpf("0.3"), mp.mpf("0.06")
    s0 = lo0; lo = hi = None
    while s0 <= hi0:
        if end(s0, omega, V1, V2, M2) < 0:
            lo, hi = max(lo0, s0-stp), s0; break
        s0 += stp
    if lo is None: return None
    flo = end(lo, omega, V1, V2, M2); fhi = end(hi, omega, V1, V2, M2)
    if flo*fhi > 0:
        lo -= stp; flo = end(lo, omega, V1, V2, M2)
        if flo*fhi > 0: return None
    for _ in range(SHOOT_IT):
        mid=(lo+hi)/2; fm=end(mid, omega, V1, V2, M2)
        if flo*fm <= 0: hi=mid; fhi=fm
        else: lo=mid; flo=fm
    return (lo+hi)/2

def simpson(fv, h):
    n = len(fv)-1
    if n % 2 == 1: n -= 1
    s = fv[0]+fv[n]
    for i in range(1,n,2): s += mp.mpf("4")*fv[i]
    for i in range(2,n-1,2): s += mp.mpf("2")*fv[i]
    return s*h/mp.mpf("3")

def observables(omega, s0, V1, V2, M2):
    h = RMAX/STEPS
    arr=[s0]; r=h; f0=f(s0,omega,V1,V2,M2)
    s=s0+(f0/mp.mpf("6"))*h*h; ds=(f0/mp.mpf("3"))*h; arr.append(s)
    for _ in range(STEPS-1):
        k1=rhs(r,s,ds,omega,V1,V2,M2); k2=rhs(r+h/2,s+(h/2)*ds,ds+(h/2)*k1,omega,V1,V2,M2)
        k3=rhs(r+h/2,s+(h/2)*(ds+(h/2)*k1),ds+(h/2)*k2,omega,V1,V2,M2)
        k4=rhs(r+h,s+h*(ds+(h/2)*k2),ds+h*k3,omega,V1,V2,M2)
        ds+=(h/6)*(k1+2*k2+2*k3+k4); s+=h*ds; r+=h; arr.append(s)
    darr=[mp.mpf("0")]*len(arr)
    for i in range(1,len(arr)-1): darr[i]=(arr[i+1]-arr[i-1])/(2*h)
    darr[0]=(arr[1]-arr[0])/h; darr[-1]=(arr[-1]-arr[-2])/h
    rs=[mp.mpf("0")]+[h*mp.mpf(i) for i in range(1,STEPS+1)]
    fN=[mp.mpf("4")*mp.pi*rr*rr*arr[i]**2 for i,rr in enumerate(rs)]; N=simpson(fN,h)
    fE=[]
    for i,rr in enumerate(rs):
        w=arr[i]**2
        fE.append(mp.mpf("4")*mp.pi*rr*rr*(omega*omega*w + darr[i]**2 + U(w,V1,V2,M2)))
    E0=simpson(fE,h)
    return N, mp.mpf("2")*omega*N, E0

def main():
    dps = int(sys.argv[1]) if len(sys.argv)>1 else 25
    mp.mp.dps = dps
    V1 = V1_FIX
    print("TUFT V3.2 方向B · 参数空间稳定相图  dps=%d  V1=1.2  S=min(E₀/Q)/m" % dps)
    M2s = [mp.mpf(x) for x in ["0.20","0.40","0.60","0.80","1.00"]]
    V2s = [mp.mpf(x) for x in ["0.20","0.40","0.60","0.80","1.00"]]
    rows = []
    for M2 in M2s:
        for V2 in V2s:
            if V1*V1 <= mp.mpf("4")*M2*V2:
                rows.append({"V1":float(V1),"V2":float(V2),"M2":float(M2),
                             "exists":False}); continue
            omax = mp.sqrt(M2/mp.mpf("2")); m_thr = omax   # m=√(M2/2)
            # 扫描 6 个 ω 找 min E₀/Q
            ws = [omax*mp.mpf(k)/mp.mpf("7") for k in range(1,7)]
            center = None; mineq = None; w_min = None
            ok_any = False
            for om in ws:
                s0 = shoot(om, V1, V2, M2, center)
                if s0 is None: center=None; continue
                center = s0; ok_any = True
                N,Q,E0 = observables(om, s0, V1, V2, M2)
                eq = E0/Q
                if mineq is None or eq < mineq: mineq, w_min = eq, om
            if not ok_any:
                rows.append({"V1":float(V1),"V2":float(V2),"M2":float(M2),
                             "exists":True,"converged":False}); continue
            S = mineq/m_thr
            rows.append({"V1":float(V1),"V2":float(V2),"M2":float(M2),
                         "exists":True,"converged":True,"m":float(m_thr),
                         "min_EQ":float(mineq),"omega_at_min":float(w_min),
                         "S":float(S),"stable":(S < 1)})
            print("  V1=1.2 V2=%.2f M2=%.2f  m=%.4f  minE/Q=%.4f@ω=%.4f  S=%.4f  %s"
                  % (float(V2),float(M2),float(m_thr),float(mineq),float(w_min),
                     float(S), ("STABLE" if S<1 else "decay")))
    out = {"V1":float(V1),"dps":dps,"rows":rows}
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "V3.2_paramscan.json")
    with open(base,"w",encoding="utf-8") as fh: json.dump(out,fh,ensure_ascii=False,indent=1)
    print("已写盘 %s" % base)
    stab = [r for r in rows if r.get("stable")]
    print("稳定参数点：%d / %d" % (len(stab), len([r for r in rows if r.get("converged")])))

if __name__=="__main__":
    main()
