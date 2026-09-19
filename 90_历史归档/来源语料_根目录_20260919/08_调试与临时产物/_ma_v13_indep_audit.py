# -*- coding: utf-8 -*-
"""
MainAgent v13 independent audit (does NOT import coalition code).
Same RK4 shooting + bare (psi'/psi = iw) outgoing matcher applied FIRST to
GR Schwarzschild RW s=-2 horizon-ingoing (known answer), THEN to TUFT wall.

Decides whether the coalition's TUFT roots (0.363/0.387...) are asymptotic QNMs
or s_out=30 finite-box artifacts. Coalition itself reported jumps to spurious
Re~18 roots at s_out=26/34 and never ran the shooting code on the GR gate.

Units M=1. RW scalar-like 1D: psi_ss + (w^2 - V) psi = 0, s = tortoise.
"""
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import numpy as np
from scipy.optimize import root as sp_root
from scipy.interpolate import interp1d

t0 = time.time()
def P(*a): print(*a, flush=True)

# ---------- shared 4-real-component RK4 (independently written) ----------
def make_shooter(V_of_s, h):
    """V_of_s: array on uniform s-grid 0..s_out spacing h. Returns F(w)
    with caller-supplied inner BC vector (psi, psi_s) at s=0 via init(w)."""
    Vg = V_of_s
    N = len(Vg)
    def shoot(w, init):
        a, b = float(w.real), float(w.imag)
        Wk0 = -a*a + b*b          # V - a^2 + b^2 added per step
        twoab = 2*a*b
        u, v, us, vs = init
        for k in range(N-1):
            W = Vg[k] + Wk0
            # RK4
            k1u, k1v, k1us, k1vs = us, vs, W*u + twoab*v, W*v - twoab*u
            u2, v2 = u+0.5*h*k1u, v+0.5*h*k1v
            us2, vs2 = us+0.5*h*k1us, vs+0.5*h*k1vs
            k2u, k2v = us2, vs2
            Wm = Vg[k]+Wk0
            k2us, k2vs = Wm*u2 + twoab*v2, Wm*v2 - twoab*u2
            u3, v3 = u+0.5*h*k2u, v+0.5*h*k2v
            us3, vs3 = us+0.5*h*k2us, vs+0.5*h*k2vs
            k3u, k3v = us3, vs3
            k3us, k3vs = Wm*u3 + twoab*v3, Wm*v3 - twoab*u3
            u4, v4 = u+h*k3u, v+h*k3v
            us4, vs4 = us+h*k3us, vs+h*k3vs
            k4u, k4v = us4, vs4
            Wp = Vg[min(k+1,N-1)]+Wk0
            k4us, k4vs = Wp*u4 + twoab*v4, Wp*v4 - twoab*u4
            u  += h/6*(k1u+2*k2u+2*k3u+k4u)
            v  += h/6*(k1v+2*k2v+2*k3v+k4v)
            us += h/6*(k1us+2*k2us+2*k3us+k4us)
            vs += h/6*(k1vs+2*k2vs+2*k3vs+k4vs)
        psi = complex(u, v); psis = complex(us, vs)
        return psis/psi - 1j*complex(a, b)   # log-deriv - i w
    return shoot

def find(shoot, init_fn, guess, tol=1e-10):
    def f(x):
        z = shoot(complex(x[0], x[1]), init_fn(complex(x[0],x[1])))
        return [z.real, z.imag]
    try:
        sol = sp_root(f, [guess.real, guess.imag], method="hybr",
                      options={"xtol":1e-12,"maxfev":2000})
        w = complex(*sol.x); r = abs(shoot(w, init_fn(w)))
        return w, r, sol.success
    except Exception as e:
        return None, 1e9, False

# ---------- GR Schwarzschild RW potential on tortoise grid ----------
def gr_grid(s_out, h=0.012, delta=1e-4):
    rh = 2.0
    r0 = rh*(1+delta)
    # build r -> rstar
    r = np.linspace(r0, 120.0, 400000)
    f = 1-2/r
    rstar0 = r0 + 2*np.log(r0/2-1)
    rstar = r + 2*np.log(r/2-1) - rstar0     # local s, 0 at r0
    V = f*(6.0/r**2 - 6.0/r**3)              # RW l=2, s=-2
    # local s-grid 0..s_out
    s = np.arange(0, s_out+0.5*h, h)
    Vg = interp1d(rstar, V, kind="linear", fill_value="extrapolate")(s)
    return s, Vg

def gr_init(w):
    # horizon ingoing psi ~ e^{-i w r*}: psi(0)=1, psi_s(0) = -i w = b - i a
    a, b = float(w.real), float(w.imag)
    return (1.0, 0.0, b, -a)

# ---------- TUFT wall grid ----------
def tuft_grid(cm, d, s_out, h=0.012):
    # wall: 1 + cm/r^2 + d/r^3 = 0
    rr = np.linspace(1e-3, 120.0, 600000)
    g = 1 + cm/rr**2 + d/rr**3
    rh = None
    for i in range(len(rr)-1):
        if g[i]*g[i+1] < 0:
            from scipy.optimize import brentq
            rh = brentq(lambda r: 1+cm/r**2+d/r**3, rr[i], rr[i+1], xtol=1e-14)
            break
    r = np.linspace(rh*(1+1e-12), 120.0, 600000)
    F = np.exp(2/r)*np.sqrt(np.clip(1+cm/r**2+d/r**3, 0, None))
    s = np.concatenate([[0.0], np.cumsum(0.5*(F[1:]+F[:-1])*np.diff(r))])
    V = np.exp(-2/r)*6.0/r**2
    sg = np.arange(0, s_out+0.5*h, h)
    Vg = interp1d(s, V, kind="linear", fill_value="extrapolate")(sg)
    # cavity length wall->barrier peak (tortoise)
    ipk = int(np.argmax(V)); L = s[ipk]
    return sg, Vg, rh, L

def neumann_init(w):
    return (1.0, 0.0, 0.0, 0.0)

# =====================================================================
P("="*80)
P("MAINAGENT v13 INDEPENDENT AUDIT  (same shooter: GR self-test then TUFT)")
P("="*80)

GR_TRUTH = complex(0.37367168441804166, -0.08896231568893410)

# ---- Audit 1: does the SAME RK4+bare-iw shooter recover GR vs s_out? ----
P("\n[AUDIT 1] GR horizon-ingoing shooter, scan outer matching s_out")
P("  truth = 0.3736716844 - 0.0889623157 i")
P("  %-8s %-24s %-12s %-10s" % ("s_out","omega","|F|","|w-truth|"))
gr_rows = []
for so in [15, 20, 25, 30, 40, 50]:
    s, Vg = gr_grid(float(so))
    shoot = make_shooter(Vg, s[1]-s[0])
    w, r, ok = find(shoot, gr_init, complex(0.40,-0.10))
    if w is None:
        P("  %-8d %-24s %-12s %-10s" % (so, "NO CONV", "-", "-")); continue
    err = abs(w-GR_TRUTH)
    gr_rows.append((so,w,err))
    P("  %-8d %-24s %-12.2e %-10.2e %s" % (so,
      "%.10f %+.10f i"%(w.real,w.imag), r, err,
      "DIG=%d"%max(0,int(-np.floor(np.log10(err)))) if err>0 else ""))

# ---- Audit 2: TUFT wall roots vs s_out (same shooter, several seeds) ----
P("\n[AUDIT 2] TUFT wall Neumann, scan s_out; multi-seed to expose box roots")
seeds = [complex(0.40,-0.08), complex(0.30,-0.05), complex(0.55,-0.10), complex(0.70,-0.12)]
for (cm,d,tag) in [(-0.29,-0.05,"c=-0.29"), (-0.50,0.0,"c=-0.50")]:
    P("\n  ---- %s ----" % tag)
    for so in [20, 25, 30, 35, 40, 50]:
        sg, Vg, rh, L = tuft_grid(cm,d,float(so))
        shoot = make_shooter(Vg, sg[1]-sg[0])
        found = []
        for g0 in seeds:
            w,r,ok = find(shoot, neumann_init, g0)
            if w is not None and r<1e-7 and 0.05<w.real<3 and -0.6<w.imag<-1e-4:
                if all(abs(w-q)>0.02 for q in found): found.append(w)
        found.sort(key=lambda z:-z.imag)
        w0 = found[0] if found else None
        txt = ("%.6f %+.6f i"%(w0.real,w0.imag)) if w0 is not None else "no phys root"
        P("  s_out=%-3d L=%6.3f  nroots=%d  w0=%s  all=%s" % (
            so, L, len(found), txt,
            ";".join("%.3f%+.3fi"%(q.real,q.imag) for q in found[:4])))

P("\n[AUDIT 3] grid-step convergence at fixed s_out=30 (TUFT c=-0.29)")
for hh in [0.024, 0.012, 0.006]:
    sg,Vg,rh,L = tuft_grid(-0.29,-0.05,30.0,h=hh)
    shoot = make_shooter(Vg, sg[1]-sg[0])
    w,r,ok = find(shoot, neumann_init, complex(0.40,-0.08))
    P("  h=%.4f Ngrid=%-6d w=%s  |F|=%.2e" % (
        hh, len(sg), ("%.8f %+.8f i"%(w.real,w.imag)) if w is not None else "NO", r))

P("\nTotal %.1f s" % (time.time()-t0))
