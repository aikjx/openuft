#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 方向B · 三维参数稳定相图 + 极值恒等式校验
====================================================================
扩展 §5.4：变 V1∈{1.0,1.2,1.4} × M2 × V2 扫描，稳定性指标 S=min(E₀/Q)/m
（m=√(M2/2)，S<1 稳定）；并在每个参数点内对相邻收敛 ω 档校验 dE₀/dQ≈ω，
确认解族在整个参数空间都是真极值（作用量极值）Q-ball 分支。
约束：V1² > 4·M2·V2。基线自检：V1=1.2,V2=0.4,M2=0.4 → S≈0.970、dE/dQ≈ω。
用法： python V3.2_paramscan3d.py [dps]
"""
import sys, json, os
import mpmath as mp

RMAX = mp.mpf("12"); STEPS = 340
SHOOT_IT = 36

def U(w, V1, V2, M2): return mp.mpf("0.5")*M2*w - (V1/mp.mpf("4"))*w**2 + (V2/mp.mpf("6"))*w**3
def dUdw(w, V1, V2, M2): return mp.mpf("0.5")*M2 - (V1/mp.mpf("2"))*w + (V2/mp.mpf("2"))*w**2
def f(s, om, V1, V2, M2): return (dUdw(s*s, V1, V2, M2) - om*om)*s
def rhs(r, s, ds, om, V1, V2, M2):
    if r <= mp.mpf("1e-24"): return f(s, om, V1, V2, M2)/mp.mpf("3")
    return -(mp.mpf("2")/r)*ds + f(s, om, V1, V2, M2)
def integrate_full(s0, om, V1, V2, M2):
    h = RMAX/STEPS; r = h; f0 = f(s0, om, V1, V2, M2)
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
    dps = int(sys.argv[1]) if len(sys.argv)>1 else 24
    mp.mp.dps = dps
    print("TUFT V3.2 方向B · 三维参数稳定相图 + dE0/dQ 校验  dps=%d" % dps)
    V1s = [mp.mpf(x) for x in ["1.0","1.2","1.4"]]
    M2s = [mp.mpf(x) for x in ["0.20","0.40","0.60"]]
    V2s = [mp.mpf(x) for x in ["0.20","0.40","0.60","0.80"]]
    rows = []
    for V1 in V1s:
        for M2 in M2s:
            for V2 in V2s:
                if V1*V1 <= mp.mpf("4")*M2*V2:
                    rows.append({"V1":float(V1),"V2":float(V2),"M2":float(M2),"exists":False}); continue
                omax = mp.sqrt(M2/mp.mpf("2")); m_thr = omax
                ws = [omax*mp.mpf(k)/mp.mpf("6") for k in range(1,6)]
                center=None; pts=[]
                for om in ws:
                    s0 = shoot(om, V1, V2, M2, center)
                    if s0 is None: center=None; continue
                    center=s0
                    N,Q,E0 = observables(om, s0, V1, V2, M2)
                    pts.append({"omega":float(om),"s0":float(s0),"N":float(N),"Q":float(Q),"E0":float(E0),"EQ":float(E0/Q)})
                if not pts:
                    rows.append({"V1":float(V1),"V2":float(V2),"M2":float(M2),"exists":True,"converged":False}); continue
                mineq = min(p["EQ"] for p in pts)
                wmin = [p["omega"] for p in pts if abs(p["EQ"]-mineq)<1e-6][0]
                S = mineq/m_thr
                # dE0/dQ 相邻档中心差分（收敛档内）
                ratios=[]
                for i in range(1,len(pts)):
                    dE=pts[i]["E0"]-pts[i-1]["E0"]; dQ=pts[i]["Q"]-pts[i-1]["Q"]
                    if abs(dQ)>1e-9:
                        ratios.append(abs((dE/dQ)/mp.mpf(pts[i]["omega"])))
                row={"V1":float(V1),"V2":float(V2),"M2":float(M2),"exists":True,"converged":True,
                     "m":float(m_thr),"min_EQ":float(mineq),"omega_at_min":float(wmin),
                     "S":float(S),"stable":S<1,"n_points":len(pts),
                     "dEdQ_ratio_min":float(min(ratios)) if ratios else None,
                     "dEdQ_ratio_max":float(max(ratios)) if ratios else None}
                rows.append(row)
                print("  V1=%.1f V2=%.2f M2=%.2f  m=%.4f minE/Q=%.4f S=%.4f %s  dE/dQ比=%.2f..%.2f"
                      % (float(V1),float(V2),float(M2),float(m_thr),float(mineq),float(S),
                         "STABLE" if S<1 else "decay",
                         float(min(ratios)) if ratios else float('nan'),
                         float(max(ratios)) if ratios else float('nan')))
    out={"dps":dps,"rows":rows}
    base=os.path.join(os.path.dirname(os.path.abspath(__file__)),"V3.2_paramscan3d.json")
    with open(base,"w",encoding="utf-8") as fh: json.dump(out,fh,ensure_ascii=False,indent=1)
    print("已写盘 %s" % base)
    conv=[r for r in rows if r.get("converged")]; stab=[r for r in conv if r.get("stable")]
    print("收敛点=%d 稳定点=%d" % (len(conv),len(stab)))

if __name__=="__main__":
    main()
