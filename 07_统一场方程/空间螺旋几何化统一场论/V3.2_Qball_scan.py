#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 方向B · ω 全谱扫描（Q-ball 解族与稳定性边界）
====================================================================
对「有下界六次势 + 质量项」时间谐振 Q-ball 修复候选，扫描整个允许频带
ω∈(0, ω_max=√(M2/2))，得到解族分支曲线：σ(0)(ω)、N(ω)、Q(ω)、E₀(ω)、
E₀/Q(ω)，并校验 Q-ball 约束 dE₀/dQ = ω（相邻档中心差分）。

单位：c=1 天然单位；绝对质量/电荷需尺度锚（未提供）。诚实边界见输出。
用法： python V3.2_Qball_scan.py [dps] [n_omega]
默认 dps=30、n_omega=16。
"""
import sys
import json
import mpmath as mp

V1   = mp.mpf("1.2"); V2 = mp.mpf("0.4"); M2 = mp.mpf("0.4")
C    = mp.mpf("1")
RMAX = mp.mpf("14"); STEPS = 640
SHOOT_IT = 45

def U(w): return mp.mpf("0.5")*M2*w - (V1/mp.mpf("4"))*w**2 + (V2/mp.mpf("6"))*w**3
def dUdw(w): return mp.mpf("0.5")*M2 - (V1/mp.mpf("2"))*w + (V2/mp.mpf("2"))*w**2
def f(s, om): return (dUdw(s*s) - om*om)*s
def rhs(r,s,ds,om):
    if r <= mp.mpf("1e-24"): return f(s,om)/mp.mpf("3")
    return -(mp.mpf("2")/r)*ds + f(s,om)
def integrate_full(s0, om):
    h = RMAX/STEPS
    r = h; f0=f(s0,om)
    s = s0 + (f0/mp.mpf("6"))*h*h
    ds = (f0/mp.mpf("3"))*h
    for _ in range(STEPS-1):
        k1=rhs(r,s,ds,om); k2=rhs(r+h/2,s+(h/2)*ds,ds+(h/2)*k1,om)
        k3=rhs(r+h/2,s+(h/2)*(ds+(h/2)*k1),ds+(h/2)*k2,om); k4=rhs(r+h,s+h*(ds+(h/2)*k2),ds+h*k3,om)
        ds += (h/6)*(k1+2*k2+2*k3+k4); s += h*ds; r += h
    return s
def end(s0,om): return integrate_full(s0,om)

def shoot(omega, center):
    """延续法打靶：在 center 邻域找首个 +→− 符号变化并二分。"""
    if center is None:
        lo0, hi0, stp = mp.mpf("0.05"), mp.mpf("3.0"), mp.mpf("0.05")
    else:
        lo0, hi0, stp = center - mp.mpf("0.25"), center + mp.mpf("0.25"), mp.mpf("0.05")
    s0 = lo0
    lo = hi = None
    while s0 <= hi0:
        if end(s0, omega) < 0:
            lo, hi = max(lo0, s0-stp), s0
            break
        s0 += stp
    if lo is None: return None
    flo = end(lo, omega); fhi = end(hi, omega)
    if flo*fhi > 0:
        lo -= stp; flo = end(lo, omega)
        if flo*fhi > 0: return None
    for _ in range(SHOOT_IT):
        mid=(lo+hi)/2; fm=end(mid, omega)
        if flo*fm <= 0: hi=mid; fhi=fm
        else: lo=mid; flo=fm
    return (lo+hi)/2

def simpson(fvals, h):
    n = len(fvals)-1
    if n % 2 == 1: n -= 1
    s = fvals[0]+fvals[n]
    for i in range(1,n,2): s += mp.mpf("4")*fvals[i]
    for i in range(2,n-1,2): s += mp.mpf("2")*fvals[i]
    return s*h/mp.mpf("3")

def observables(omega, s0):
    h = RMAX/STEPS
    arr=[s0]
    r=h; f0=f(s0,omega)
    s=s0+(f0/mp.mpf("6"))*h*h; ds=(f0/mp.mpf("3"))*h; arr.append(s)
    for _ in range(STEPS-1):
        k1=rhs(r,s,ds,omega); k2=rhs(r+h/2,s+(h/2)*ds,ds+(h/2)*k1,omega)
        k3=rhs(r+h/2,s+(h/2)*(ds+(h/2)*k1),ds+(h/2)*k2,omega); k4=rhs(r+h,s+h*(ds+(h/2)*k2),ds+h*k3,omega)
        ds+=(h/6)*(k1+2*k2+2*k3+k4); s+=h*ds; r+=h; arr.append(s)
    darr=[mp.mpf("0")]*len(arr)
    for i in range(1,len(arr)-1): darr[i]=(arr[i+1]-arr[i-1])/(2*h)
    darr[0]=(arr[1]-arr[0])/h; darr[-1]=(arr[-1]-arr[-2])/h
    rs=[mp.mpf("0")]+[h*mp.mpf(i) for i in range(1,STEPS+1)]
    fN=[mp.mpf("4")*mp.pi*rr*rr*arr[i]**2 for i,rr in enumerate(rs)]
    N=simpson(fN,h)
    fE=[]
    for i,rr in enumerate(rs):
        w=arr[i]**2
        # 规范能量密度 T⁰⁰ = |φ̇|²+|∇φ|²+W = ω²σ²+σ'²+U(σ²)
        fE.append(mp.mpf("4")*mp.pi*rr*rr*(omega*omega*w + darr[i]**2 + U(w)))
    E0=simpson(fE,h)
    Q=mp.mpf("2")*omega*N
    M=E0/(C*C)
    return N,Q,E0,M,arr[-1]

def main():
    dps = int(sys.argv[1]) if len(sys.argv)>1 else 30
    nw  = int(sys.argv[2]) if len(sys.argv)>2 else 16
    mp.mp.dps = dps
    omax = mp.sqrt(M2/mp.mpf("2"))
    print("TUFT V3.2 方向B · ω 全谱扫描  dps=%d  n_omega=%d" % (dps,nw))
    print("ω∈(0, %.6f), V1=1.2 V2=0.4 M2=0.4 c=1" % float(omax))
    rows=[]; center=None
    # 对数网格覆盖全谱
    ws=[omax*mp.mpf(k)/mp.mpf(nw+1) for k in range(1,nw+1)]
    for om in ws:
        s0 = shoot(om, center)
        if s0 is None:
            rows.append({"omega":float(om),"converged":False})
            print("  ω=%.6f : 无收敛解" % float(om))
            center=None; continue
        N,Q,E0,M,tail = observables(om,s0)
        rows.append({"omega":float(om),"converged":True,"s0":float(s0),
                     "N":float(N),"Q":float(Q),"E0":float(E0),"M":float(M),
                     "EQ":float(E0/Q),"tail":float(tail)})
        print("  ω=%.6f σ0=%.7f N=%.7g Q=%.7g E0=%.7g E0/Q=%.7f tail=%.3g"
              % (float(om),float(s0),float(N),float(Q),float(E0),float(E0/Q),float(tail)))
        center=s0
    # dE0/dQ 校验（相邻收敛档中心差分）
    conv=[r for r in rows if r.get("converged")]
    for i in range(1,len(conv)):
        dE=(conv[i]["E0"]-conv[i-1]["E0"])/(conv[i]["Q"]-conv[i-1]["Q"])
        conv[i]["dEdQ"]=dE; conv[i]["dEdQ_omega"]=conv[i]["omega"]
    out = {"dps":dps,"V1":float(V1),"V2":float(V2),"M2":float(M2),"omax":float(omax),
           "rows":rows}
    import os
    base=os.path.join(os.path.dirname(os.path.abspath(__file__)),"V3.2_Qball_scan.json")
    with open(base,"w",encoding="utf-8") as fh:
        json.dump(out,fh,ensure_ascii=False,indent=1)
    print("已写盘 %s" % base)
    print("=== dE0/dQ 校验（Q-ball 约束：应≈ω）===")
    for r in conv[1:]:
        if "dEdQ" in r:
            print("  ω=%.6f: dE0/dQ=%.7f  比值=%.6f" % (r["omega"],r["dEdQ"],r["dEdQ"]/r["omega"]))

if __name__=="__main__":
    main()
