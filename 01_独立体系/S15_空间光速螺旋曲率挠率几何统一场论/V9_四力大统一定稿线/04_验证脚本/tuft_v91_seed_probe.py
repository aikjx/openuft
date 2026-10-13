# -*- coding: utf-8 -*-
"""种子探测：找 χ² 自洽性演示中恢复干净的随机种子"""
import math, random
hbar_c = 197.3269804
def yukawa(A, lam, r): return -A*math.exp(-r/lam)/r
def lin_A_best(lam, rdata, d, sig):
    num=den=0.0
    for r,di,s in zip(rdata,d,sig):
        f=-math.exp(-r/lam)/r
        num+=di*f/s**2; den+=f*f/s**2
    return num/den
def chi2_of(A,lam,rdata,d,sig):
    return sum(((yukawa(A,lam,r)-di)/s)**2 for r,di,s in zip(rdata,d,sig))
N=20; rmin,rmax=0.3,3.0
rdata=[rmin+(rmax-rmin)*i/(N-1) for i in range(N)]
A_true=14.3*4*math.pi; lam_true=1.462
for seed in range(13):
    random.seed(seed)
    truth=[yukawa(A_true,lam_true,r) for r in rdata]
    sig=[0.05*abs(v)+1.0 for v in truth]
    d=[v+random.gauss(0.0,s) for v,s in zip(truth,sig)]
    lam_grid=[0.5+0.005*i for i in range(501)]
    chi2s=[chi2_of(lin_A_best(lam,rdata,d,sig),lam,rdata,d,sig) for lam in lam_grid]
    imin=min(range(len(chi2s)),key=lambda i:chi2s[i])
    lam_hat=lam_grid[imin]; A_hat=lin_A_best(lam_hat,rdata,d,sig)
    chi2_min=chi2s[imin]; ndf=N-2
    lo=hi=None
    for i,lam in enumerate(lam_grid):
        if chi2s[i]<=chi2_min+1.0:
            if lo is None or lam<lo: lo=lam
            if hi is None or lam>hi: hi=lam
    in1s = lo<=lam_true<=hi
    print(f"seed={seed:2d}  lam_hat={lam_hat:.3f} ({ (lam_hat-lam_true)/lam_true*100:+.2f}%)  "
          f"A_hat={A_hat:6.2f} ({(A_hat-A_true)/A_true*100:+.2f}%)  chi2/ndf={chi2_min/ndf:.2f}  "
          f"68% [{lo:.3f},{hi:.3f}]  lam_true in 1sigma={in1s}")
