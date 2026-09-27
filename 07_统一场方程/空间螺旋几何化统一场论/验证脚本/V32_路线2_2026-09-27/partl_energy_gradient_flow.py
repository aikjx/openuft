# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part L：能量梯度流（E-ωQ 最小化）验证双阱 Q-ball 局域极小是否存在
固定电荷变分 δ(E-ωQ)=0 给出径向方程 φ''+(2/r)φ'=(m²-ω²)φ-λφ³+ηφ⁵。
梯度流：∂φ/∂τ = (φ''+2/rφ') - (m²φ-λφ³+ηφ⁵) + ω²φ  （= -δ(E-ωQ)/δφ）
在径向网格上松弛到局部极小；若真存在 Q-ball 局域解则此处收敛为 φ(0)>0、衰减到 0。
"""
import numpy as np
m2=1.0; lam=5.0; eta=4.0; q0=1.0; c=1.0
R=80.0; Np=4001
r=np.linspace(1e-6,R,Np); dr=r[1]-r[0]
r2=r*r

def lap(f):
    # (1/r²)d/dr(r² f') 用中心差分; 端点特殊
    d2=np.zeros_like(f)
    d2[1:-1]=(f[2:]-2*f[1:-1]+f[:-2])/dr**2 + (2.0/r[1:-1])*(f[2:]-f[:-2])/(2*dr)
    # r=0: 光滑 f'(0)=0 => (1/r²)d(r²f')/dr ~ 3 f''(0); 用三次外推估算
    d2[0]=3*(f[1]-2*f[0]+f[2])/dr**2  # 近似 f''(0) 用前三点的二阶差商*3
    d2[-1]=f[-2]-2*f[-1]+f[-2]  # 占位（边界固定0，不更新）
    return d2

def relax(om, r_wall, dt=2e-5, iters=40000, verbose=0):
    # 初值：球内真真空，球外 0，光滑过渡
    phi=phi_true*0.5*(1-np.tanh((r-r_wall)/1.5))
    phi[0]=phi_true
    Eprev=None
    for it in range(iters):
        L=lap(phi)
        Vp=m2*phi-lam*phi**3+eta*phi**5
        grad = -(L - Vp + om**2*phi)
        phi[1:-1] += dt*grad[1:-1]
        np.clip(phi,0.0,4.0,out=phi)   # 截断防止非线性上溢
        phi[-1]=0.0
        if it%4000==0:
            dphi=np.gradient(phi,r)
            E=4*np.pi*np.trapezoid(r2*(0.5*dphi**2 + 0.5*m2*phi**2-lam/4*phi**4+eta/6*phi**6 - 0.5*om**2*phi**2),r)
            if verbose:
                print(f"    it={it}: E-ωQ={E:+.6e}, φ(0)={phi[0]:.4f}, max={phi.max():.4f}")
            if Eprev is not None and abs(E-Eprev)<1e-10*abs(E)+1e-11:
                break
            Eprev=E
    dphi=np.gradient(phi,r)
    N=4*np.pi*np.trapezoid(r2*phi**2,r)
    E0=4*np.pi*np.trapezoid(r2*(0.5*dphi**2+0.5*m2*phi**2-lam/4*phi**4+eta/6*phi**6),r)
    E0_ph=E0+4*np.pi*np.trapezoid(r2*(0.5*om**2*phi**2),r)
    numC=4*np.pi*np.trapezoid(r2*(phi**2*(m2-3*lam*phi**2+5*eta*phi**4)*r2),r)
    C=numC/N
    return dict(phi=phi, a0=phi[0], fmin=phi.min(), fR=phi[-1], N=N, E0=E0, E0_ph=E0_ph, C=C,
                Q0=q0*om*N, Espec=E0/N)

phi_true=1.0
print("=== Part L（稳定版）：能量梯度流（E-ωQ 最小化）===")
for om in [0.5,0.9]:
    for rw in [15,20]:
        d=relax(om,rw,verbose=1)
        ok = d['a0']>0.5 and d['fmin']>0 and abs(d['fR'])<1e-4
        print(f"  ω={om} (wall={rw}): φ(0)={d['a0']:.4f} min={d['fmin']:+.2e} φ(R)={d['fR']:+.2e}"
              f"  N={d['N']:.6e} E0={d['E0']:+.6e} C={d['C']:+.6e} Q0={d['Q0']:.6e}"
              f"  {'<CLEAN>' if ok else '<not-localized>'}")
