# -*- coding: utf-8 -*-
"""v15 probe: GR gate core. r-coord ODE + outgoing asymptotic tail + log-derivative match."""
import mpmath as mp
mp.mp.dps = 50
I = mp.mpc(0,1)

def gr_g(r):   # dr/ds = 1-2/r
    return (r-2)/r
def gr_dlng(r):
    return 1/(r-2) - 1/r
def gr_V(r,l=2):
    f = (r-2)/r
    return f*(l*(l+1)/r**2 - 6/r**3)
def gr_s(r):
    return r + 2*mp.log(r/2 - 1)

# asymptotic v_p of V(s)~6/s^2-18/s^3+12/s^4 (r~s leading; log corrections are O(log s/s^3), higher)
VP = {2: mp.mpf(6), 3: mp.mpf(-18), 4: mp.mpf(12)}

def tail_a(w, Na):
    """a=[1,a1,...,a_Na] via recurrence. m=2..Na+1 determines a_{m-1}."""
    a = [mp.mpf(1)]
    for m in range(2, Na+2):
        s_acc = (m-2)*(m-1)*a[m-2]
        for p in range(2, m+1):
            j = m-p
            if 0 <= j < len(a):
                s_acc -= VP.get(p, mp.mpf(0))*a[j]
        a_new = s_acc/(2*I*w*(m-1))
        a.append(a_new)
    return a

def tail_logderiv(w, s, a):
    chi = mp.mpf(0); dchi = mp.mpf(0)
    for k in range(0, len(a)):
        chi += a[k]*s**(-k)
    for k in range(1, len(a)):
        dchi += -k*a[k]*s**(-k-1)
    return I*w + dchi/chi

def F(w, r0, rm, Na):
    y0 = [mp.mpf(1), -I*w*gr_g(r0)]  # ingoing psi_s=-iw -> psi_r=g*psi_s
    def sys(r, y):
        rhs = -(gr_dlng(r))*y[1] - (w**2 - gr_V(r))/gr_g(r)**2*y[0]
        return [y[1], rhs]
    sol = mp.odefun(sys, r0, y0, tol=mp.mpf('1e-42'))
    yr = sol(mp.mpf(rm))
    ld_in = gr_g(mp.mpf(rm))*yr[1]/yr[0]
    s_m = gr_s(mp.mpf(rm))
    a = tail_a(w, Na)
    return ld_in - tail_logderiv(w, s_m, a)

def main():
    target = mp.mpc('0.37367168441804166','-0.0889623156889341')
    print("target", target)
    for rm in [20, 30, 50]:
        for Na in [1,2,3]:
            try:
                Fv = lambda z: F(z, mp.mpf('2.002'), mp.mpf(rm), Na)
                w = mp.findroot(Fv, target*mp.mpf('0.98')-I*mp.mpf('0.09'))
                diff = abs(w-target)
                dig = 99 if diff==0 else max(0, int(-mp.floor(mp.log10(diff))))
                print(f"rm={rm:3d} Na={Na}  w={w}  |diff|={float(diff):.2e}  digits={dig}", flush=True)
            except Exception as e:
                print(f"rm={rm} Na={Na} FAIL {e}", flush=True)

main()
