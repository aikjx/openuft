import csv, json, math, pathlib, unittest, io
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=pathlib.Path(__file__).resolve().parent
C=299792458.; G=6.67430e-11; HBAR=6.62607015e-34/(2*math.pi)
BODIES={'Earth':(398600.435507e9,6371e3),'Moon':(4902.800118e9,1737.4e3)}
def mass_pair(a,b,theta): return 2*math.sqrt(a*b)*abs(math.sin(theta/2))
def potential(r,A,S,B): return A/r+S*r*r+B*r**3
def grad(r,A,S,B): return -A/r**2+2*S*r+3*B*r*r
def hess(r,A,S,B): return 2*A/r**3+2*S+6*B*r
def eq(A,S,B):
    if A<=0 or min(S,B)<0 or S+B==0: raise ValueError('requires A>0 and positive confinement')
    return brentq(lambda r: -A+2*S*r**3+3*B*r**4,1e-10,1e6,xtol=1e-14)
def ray_data():
    rng=np.random.default_rng(156); N=4096
    x=rng.normal(size=(N,3)); n=rng.normal(size=(N,3)); n/=np.linalg.norm(n,axis=1)[:,None]
    # each initial position hosts equal opposite momenta
    t=np.linspace(0,8,81); I=np.array([np.mean((np.sum((x+s*n)**2,axis=1)+np.sum((x-s*n)**2,axis=1))/2) for s in t]); return t,I,x,n

def breathing(A,S,B,r0):
    rstar=eq(A,S,B); m=potential(rstar,A,S,B) # illustrative inertia, not independently derived
    t=np.linspace(0,30,3001)
    def ode(t,y):
        r,p=y; return [p/math.sqrt(m*m+p*p),-grad(r,A,S,B)]
    def run(method,tol): return solve_ivp(ode,(0,30),[r0*rstar,0],t_eval=t,method=method,rtol=tol,atol=tol*.01)
    sol=run('DOP853',1e-12); alt=run('RK45',1e-10)
    r,p=sol.y; energy=np.sqrt(m*m+p*p)-m+potential(r,A,S,B)
    return t,r,p,energy, float(np.max(abs(energy-energy[0]))/energy[0]),float(np.max(abs(sol.y-alt.y))),rstar,m

def flux_stress(x,b):
    r=np.linalg.norm(x); h=x/r; w=h+b*np.cross([0,0,1],h); norm=np.linalg.norm(w); n=w/norm; rho=norm/r**2
    return rho*n, rho*np.outer(n,n)
def fd_force(x,b,step=1e-5):
    f=np.zeros(3); d=0.
    for j in range(3):
        dx=np.eye(3)[j]*step; jp,tp=flux_stress(x+dx,b); jm,tm=flux_stress(x-dx,b); f-=(tp[:,j]-tm[:,j])/(2*step); d+=(jp[j]-jm[j])/(2*step)
    return f,d

def symbolic():
    R,A,S,B=sp.symbols('R A S B',positive=True); V=A/R+S*R**2+B*R**3
    a=2*S*R**3+3*B*R**4
    exprs={'gradient':sp.diff(V,R)-(-A/R**2+2*S*R+3*B*R**2),'equilibrium':sp.diff(V,R).subs(A,a),'hessian_equilibrium':sp.diff(V,R,2).subs(A,a)-(6*S+12*B*R),'stress_trace_balance':(A/R-2*S*R**2-3*B*R**3).subs(A,a),'active_mass_balance':(2*A/R-S*R**2-2*B*R**3-V).subs(A,a)}
    return {k:str(sp.simplify(v)) for k,v in exprs.items()}

def write_csv(name,header,rows):
    with (P/'results'/name).open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(header); w.writerows(rows)

def main():
    (P/'results').mkdir(exist_ok=True);(P/'figures').mkdir(exist_ok=True)
    t,I,x,n=ray_data(); rays_err=float(np.max(np.abs(I-I[0]-t*t)))
    write_csv('free_rays.csv',['t/L0','I/E/L0^2','analytic'],zip(t,I,I[0]+t*t))
    runs=[]
    for A,S,B in [(3,0,1),(2,1,0),(5,1,1)]:
        for r0 in [.7,1.2,1.5]:
            tt,r,p,e,err,diff,rstar,m=breathing(A,S,B,r0)
            runs.append(dict(A=A,S=S,B=B,r0_ratio=r0,Rstar=rstar,min_R=float(r.min()),max_R=float(r.max()),energy_rel_error=err,solver_max_difference=diff,omega_small=math.sqrt(hess(rstar,A,S,B)/m)))
            write_csv(f'breathing_{A}_{r0}.csv',['t','R','p','H'],zip(tt,r,p,e))
    grav=[]
    for body,(gm,R) in BODIES.items():
        for h in [0,100e3,400e3,800e3,2000e3]:
            r=R+h; grav.append([body,h/1000,gm/r**2,2*gm/r**3,gm/r**3,math.sqrt(gm/r),2*math.pi*math.sqrt(r**3/gm)/60,2*gm/(r*C*C),gm/G])
    write_csv('gravity.csv',['body','alt_km','g_m_s2','radial_tidal_s-2','transverse_tidal_abs_s-2','orbit_m_s','period_min','compactness','mass_kg_from_GM'],grav)
    angles=np.linspace(0,180,181); write_csv('mass_angle.csv',['degrees','M_over_E'],[(a,mass_pair(1,1,math.radians(a))) for a in angles])
    flux=[]
    for b in [-2,-1,0,.1,.5,1,2]:
        for r in [.5,1,2,4]:
            f,d=fd_force(np.array([r,0,0]),b); exact=np.array([b*b,-b,0])/(r**3*math.sqrt(1+b*b)); flux.append([b,r,*f,*exact,d,np.linalg.norm(f-exact)])
    write_csv('flux.csv',['b','r','fx','fy','fz','fx_exact','fy_exact','fz_exact','divJ','abs_error'],flux)
    sym=symbolic(); summary=dict(ray_count=2*len(x),ray_max_abs_error=rays_err,ray_I0=float(I[0]),ray_I8=float(I[-1]),breathing=runs,symbolic=sym,flux_max_abs_error=max(row[-1] for row in flux),flux_max_divJ=max(abs(row[-2]) for row in flux),earth_moon=grav,units='theory c=1; SI conversion only for reported terrestrial values')
    (P/'results'/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    plt.plot(t,I,label='free rays (8192)');plt.plot(t,I[0]+t*t,'--',label='virial prediction');plt.xlabel('t / L0');plt.ylabel('I / (E L0²)');plt.legend();plt.tight_layout();plt.savefig(P/'figures'/'free_rays.png',dpi=160);plt.close()
    rr=np.linspace(.4,2,400)
    for A,S,B in [(3,0,1),(2,1,0),(5,1,1)]: plt.plot(rr,potential(rr,A,S,B)/potential(1,A,S,B),label=f'A={A}, S={S}, B={B}')
    plt.xlabel('R / L0');plt.ylabel('V / V(R=1)');plt.legend();plt.tight_layout();plt.savefig(P/'figures'/'potential.png',dpi=160);plt.close()
    for r0 in [.7,1.2,1.5]:
        tt,r,*_=breathing(3,0,1,r0);plt.plot(tt,r,label=f'R(0)={r0}')
    plt.xlabel('t / L0');plt.ylabel('R / L0');plt.legend();plt.tight_layout();plt.savefig(P/'figures'/'breathing.png',dpi=160);plt.close()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests); stream=io.StringIO(); out=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite); (P/'results'/'tests.txt').write_text(stream.getvalue(),encoding='utf8');print(stream.getvalue());print(json.dumps({k:summary[k] for k in ['ray_count','ray_max_abs_error','ray_I0','ray_I8','flux_max_abs_error','flux_max_divJ','symbolic']},indent=2)); print('breathing',max(r['energy_rel_error'] for r in runs),max(r['solver_max_difference'] for r in runs));
    if not out.wasSuccessful(): raise SystemExit(1)
class Tests(unittest.TestCase):
    def test_mass_angles(self):
        for theta in np.linspace(0,math.pi,181):
            with self.subTest(theta=theta):
                p=np.array([0.,0.,1.])+np.array([math.sin(theta),0,math.cos(theta)])
                self.assertAlmostEqual(mass_pair(1,1,theta)**2,4-p@p,places=12)
    def test_unequal(self): self.assertAlmostEqual(mass_pair(2,8,math.pi),8)
    def test_ray_virial(self):
        t,I,x,n=ray_data(); self.assertLess(np.max(abs(I-I[0]-t*t)),1e-12);self.assertLess(np.max(abs(np.linalg.norm(n,axis=1)-1)),1e-14)
    def test_equilibria(self):
        for A,S,B in [(3,0,1),(2,1,0),(5,1,1),(1,.3,.4),(10,0,2)]:
            r=eq(A,S,B);self.assertAlmostEqual(grad(r,A,S,B),0,places=10);self.assertGreater(hess(r,A,S,B),0);self.assertAlmostEqual(A/r,2*S*r*r+3*B*r**3,places=10);self.assertAlmostEqual(potential(r,A,S,B),2*A/r-S*r*r-2*B*r**3,places=10)
    def test_no_binding(self):
        with self.assertRaises(ValueError): eq(1,0,0)
    def test_flux(self):
        for b in [-2,-1,0,.1,.5,1,2]:
            for r in [.5,1,2,4]:
                f,d=fd_force(np.array([r,0.,0.]),b); exact=np.array([b*b,-b,0])/(r**3*math.sqrt(1+b*b));self.assertLess(np.linalg.norm(f-exact),1e-7);self.assertLess(abs(d),1e-7)
    def test_breathing(self):
        for A,S,B in [(3,0,1),(2,1,0),(5,1,1)]:
            for r0 in [.7,1.2,1.5]:
                _,r,_,_,err,diff,_,_=breathing(A,S,B,r0);self.assertLess(err,1e-9);self.assertLess(diff,1e-7);self.assertGreater(min(r),0)
    def test_symbolic(self): self.assertTrue(all(x=='0' for x in symbolic().values()))
    def test_gravity(self):
        for gm,r in BODIES.values():
            g=gm/r**2; v=math.sqrt(gm/r); self.assertAlmostEqual(v*v/r,g,places=12); self.assertLess(2*gm/r/C**2,1e-8);x=np.array([r,0.,0.]); step=r*1e-5
            def acc(x): return -gm*x/np.linalg.norm(x)**3
            jac=np.column_stack([(acc(x+step*d)-acc(x-step*d))/(2*step) for d in np.eye(3)])
            self.assertLess(np.max(abs(jac-np.diag([2,-1,-1])*gm/r**3))/(gm/r**3),1e-8)
if __name__=='__main__':main()
