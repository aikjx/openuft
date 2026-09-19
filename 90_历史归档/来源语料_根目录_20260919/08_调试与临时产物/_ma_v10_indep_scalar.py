# MainAgent 独立高精度复核 TUFT v10 标量 Leaver（不调用联盟脚本）
# E348 系数，mpmath 50 位，标准 Leaver 连分数 b0 - R0 = 0，R_n = a_n g_{n+1}/(b_{n+1}-R_{n+1})
import mpmath as mp
mp.mp.dps = 55
I = mp.mpc(0, 1)

def cfs_F(w, lam, N):
    R = mp.mpf(0)
    for n in range(N-1, -1, -1):
        an  = (n+1)*(n+1-4*I*w)
        bn1 = -lam - 2*(n+1)**2 + 16*I*(n+1)*w - 2*(n+1) + 32*w*w + 8*I*w - 1
        gn1 = ((n+1)-4*I*w)**2
        R = an*gn1/(bn1 - R)
    b0 = -lam + 32*w*w + 8*I*w - 1
    return b0 - R

def root(l, w0, N):
    lam = mp.mpf(l*(l+1))
    return mp.findroot(lambda z: cfs_F(z, lam, N), (w0,), tol=mp.mpf('1e-45'))

canon = {0: mp.mpc('0.1104557','-0.1048957'),
         1: mp.mpc('0.2929363','-0.0976600'),
         2: mp.mpc('0.4836439','-0.0967588')}
seed  = {0: mp.mpc('0.11','-0.105'), 1: mp.mpc('0.293','-0.098'), 2: mp.mpc('0.484','-0.097')}

print("independent mpmath 55-digit scalar Leaver (M=1, r_h=2)")
for l in (0,1,2):
    prev=None
    print(f"l={l}   canonical {mp.nstr(canon[l].real,8)} {mp.nstr(canon[l].imag,8)}i")
    for N in (200,500,1000,2000):
        w=root(l,seed[l],N)
        conv = "" if prev is None else f"  d(N)={mp.nstr(abs(w-prev),3)}"
        print(f"   N={N:5d}  {mp.nstr(w.real,10)} {mp.nstr(w.imag,10)}i{conv}")
        prev=w
    w=root(l,seed[l],2000)
    dc=abs(w-canon[l]); rel=dc/abs(canon[l])
    print(f"   -> |d_canon|={mp.nstr(dc,3)}  rel={mp.nstr(rel,2)} (~{mp.nstr(-mp.log10(rel),2)} digits)\n")

print("verdict on v10 l=0 double value 0.1104549-0.1048957i:")
w=root(0,seed[0],2000)
print("  high-prec true root real =", mp.nstr(w.real,10))
print("  d(true, v10double real 0.1104549) =", mp.nstr(w.real-mp.mpf('0.1104549'),3))
print("  d(true, canonical real 0.1104557) =", mp.nstr(w.real-mp.mpf('0.1104557'),3))
