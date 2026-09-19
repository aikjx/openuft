"""
GAQ‑UFT Supplemental: Frenet‑Serret 200‑digit precision solver
Generalized Kakeya Helical Vacuum Unified Field Theory
"""
import mpmath as mp
mp.mp.dps = 200

def diff_central(f, t, h=mp.mpf("1e-120")):
    return (f(t+h)-f(t-h))/(2*h)

def cross3(a,b):
    return mp.matrix([
        a[1]*b[2]-a[2]*b[1],
        a[2]*b[0]-a[0]*b[2],
        a[0]*b[1]-a[1]*b[0]
    ])

def frenet_decompose(curve_func, t):
    r1 = diff_central(curve_func, t)
    r2 = diff_central(lambda s: diff_central(curve_func,s), t)
    r3 = diff_central(lambda s: diff_central(lambda u: diff_central(curve_func,u),s), t)
    dr = mp.norm(r1)
    T = r1 / dr
    r1xr2 = cross3(r1,r2)
    cr_norm = mp.norm(r1xr2)
    kappa = cr_norm/(dr**3)
    N = cross3(r1, r1xr2)/(dr*cr_norm)
    B = cross3(T,N)
    triple = (r1xr2.T * r3)[0,0]
    tau = triple/(cr_norm**2)
    return T,N,B,kappa,tau

# variable‑kappa‑tau counterexample curve
def gamma_var(t):
    Rt = mp.mpf("2.0") + mp.mpf("0.2")*mp.sin(t)
    x = Rt*mp.cos(t)
    y = Rt*mp.sin(t)
    z = mp.mpf("0.8")*t + mp.mpf("0.1")*mp.cos(t)
    return mp.matrix([x,y,z])

# reference constant helix
def helix_const(t,R=1,omega=1,c=1):
    return mp.matrix([R*mp.cos(omega*t), R*mp.sin(omega*t), c*t])

if __name__=="__main__":
    sample_ts = [mp.mpf("0"), mp.pi/3, mp.pi/2, mp.pi]
    print("==== Variable Geometry Curve (counterexample) ====")
    for ti in sample_ts:
        T,N,B,kap,tau = frenet_decompose(gamma_var, ti)
        ratio = tau/kap
        print(f"t={ti:.4f}  κ={kap:.14f}  τ={tau:.14f}  τ/κ={ratio:.14f}")
