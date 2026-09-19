# MainAgent v12 独立复核引力 RW s=-2（不 import 联盟脚本）
# 独立写死标准 Leaver 自旋 s=-2 三项递推，mpmath 40 位，粗糙初值求根 + N 收敛
import mpmath as mp
mp.mp.dps = 40
I = mp.mpc(0,1)

def abc(w, lam, n):
    # 标准 spin-s=-2 Schwarzschild Leaver 系数（独立于联盟脚本，手抄标准形式）
    a = (n+1)*(n+3-4*I*w)
    b = -lam - 2*n*n + 16*I*n*w - 2*n + 32*w*w + 8*I*w + 3
    g = n*n - 8*I*n*w - 2*n - 16*w*w + 8*I*w
    return a,b,g

def F(w, l, N):
    lam = mp.mpf(l*(l+1))
    C = mp.mpf(0)                      # C_{N+1}=0
    for n in range(N, 0, -1):
        a,b,g = abc(w, lam, n)
        C = g/(b - a*C)
    a0,b0,_ = abc(w, lam, 0)
    return b0 - a0*C

def root(l, w_rough, N):
    lam = mp.mpf(l*(l+1))
    # secant 两个粗初值，避免"初值即答案"
    w0 = w_rough
    w1 = w_rough + mp.mpc('0.003','-0.002')
    return mp.findroot(lambda z: F(z,l,N), (w0,w1), tol=mp.mpf('1e-30'))

qnm = {0: mp.mpc('0.37367168441804166','-0.0889623156889341'),
       1: mp.mpc('0.34671099687909240','-0.2739148752911987')}
rough= {0: mp.mpc('0.37','-0.09'), 1: mp.mpc('0.35','-0.27')}

print("independent mpmath 40-digit gravitational RW s=-2, l=2 (M=1)")
for n in (0,1):
    prev=None
    print(f"mode n={n}  qnm={mp.nstr(qnm[n].real,12)} {mp.nstr(qnm[n].imag,12)}i")
    for N in (200,400,800):
        w=root(2,rough[n],N)
        conv="" if prev is None else f"  dN={mp.nstr(abs(w-prev),2)}"
        print(f"   N={N:4d} {mp.nstr(w.real,16)} {mp.nstr(w.imag,16)}i{conv}")
        prev=w
    w=root(2,rough[n],800); dd=abs(w-qnm[n]); rel=dd/abs(qnm[n])
    print(f"   -> |d_qnm|={mp.nstr(dd,2)}  ~{mp.nstr(-mp.log10(rel),2)} digits\n")
