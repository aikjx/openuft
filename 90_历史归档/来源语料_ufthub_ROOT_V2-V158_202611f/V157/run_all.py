import csv,json,unittest
from pathlib import Path
import numpy as np
from scipy.integrate import simpson
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh,LinearOperator
from probe import solve
ROOT=Path(__file__).resolve().parent

def potential(f): return .5*f*f-.5*f**4+.25*f**6

def profile(w,s,R):
    r=np.linspace(0,R,20001); f,v=s.sol(r); fac=4*np.pi*r*r
    U=potential(f); t=.5*w*w*f*f; k=.5*v*v; e=t+k+U
    integ=lambda a: float(simpson(fac*a,x=r))
    T,K,V=map(integ,[t,k,U]); E=T+K+V; Q=2*T/w
    pr=t+k-U; pt=t-k-U
    return dict(w=w,central=float(f[0]),Q=Q,E=E,E_per_Q=E/Q,virial=(3*T-K-3*V)/E,active_mass_ratio=integ(e+pr+2*pt)/E,rms_radius=np.sqrt(integ(e*r*r)/E),fixed_Q_scaling_second=12*T+6*V,tail=float(f[-1]),solver_residual=float(max(s.rms_residuals))), (r,f,e,pr,pt)

def evolve(w,s,dr,perturb=0.03,Tend=60,R=65):
    # u=r Phi, regular at r=0. Center has no weight in radial quadrature.
    r=np.linspace(0,R,round(R/dr)+1); dr=r[1]; dt=.35*dr; steps=round(Tend/dt);dt=Tend/steps
    base=s.sol(np.minimum(r,50))[0]; base[r>50]=0
    u=r*base*(1+perturb)+0j; v=1j*w*r*base/(1+perturb);u[[0,-1]]=0;v[[0,-1]]=0
    def acceleration(u):
        out=np.zeros_like(u); f2=abs(u[1:-1]/r[1:-1])**2
        out[1:-1]=(u[2:]-2*u[1:-1]+u[:-2])/dr**2-(1-2*f2+1.5*f2*f2)*u[1:-1];return out
    def measure(t,u,v):
        f2=abs(u[1:-1]/r[1:-1])**2
        e_site=.5*abs(v[1:-1])**2+r[1:-1]**2*potential(np.sqrt(f2)); grad=.5*abs(np.diff(u)/dr)**2
        E=4*np.pi*dr*(sum(e_site)+sum(grad)); Q=4*np.pi*dr*np.sum(np.imag(np.conj(u)*v));
        return [t,float(E),float(Q),float(np.sqrt(np.sum(r*r*abs(u)**2)/np.sum(abs(u)**2))),float(abs(u[1]/r[1]))]
    rows=[measure(0,u,v)]; a=acceleration(u)
    for i in range(steps):
        v+=dt/2*a;u+=dt*v;a=acceleration(u);v+=dt/2*a
        if (i+1)%max(1,steps//300)==0 or i+1==steps: rows.append(measure((i+1)*dt,u,v))
    ar=np.array(rows); eerr=max(abs(ar[:,1]/ar[0,1]-1)); qerr=max(abs(ar[:,2]/ar[0,2]-1))
    return dict(w=w,dr=dr,dt=dt,steps=steps,perturbation=perturb,energy_drift=float(eerr),charge_drift=float(qerr),initial_rms=ar[0,3],final_rms=ar[-1,3],min_rms=min(ar[:,3]),max_rms=max(ar[:,3])),ar

def hessian(w,s,dr,R=50):
    r=np.arange(dr,R,dr); f=s.sol(r)[0]; u=r*f
    a=diags([-np.ones(len(r)-1)/dr**2,2/dr**2+1-6*f*f+7.5*f**4-w*w,-np.ones(len(r)-1)/dr**2],[-1,0,1])
    v=u/np.linalg.norm(u)
    L=LinearOperator(a.shape,matvec=lambda x:a@x+4*w*w*v*np.dot(v,x),dtype=float)
    vals,vecs=eigsh(L,k=2,which='SA',tol=1e-10,v0=np.ones(len(r)))
    return dict(w=w,dr=dr,R=R,eigenvalues=vals.tolist(),residuals=[float(np.linalg.norm(L@vecs[:,i]-vals[i]*vecs[:,i])) for i in range(2)])

def write_csv(path,header,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        wr=csv.writer(f);wr.writerow(header);wr.writerows(rows)

def main():
    out=ROOT/'results';out.mkdir(exist_ok=True)
    solutions={.83:solve(.83)}
    for seq in [np.arange(82,77,-1)/100,np.arange(84,99)/100]:
        old=solutions[.83]
        for w in seq:
            s=solve(w,old=old); assert s.success and s.y[0,0]>.1,(w,s.message); solutions[float(w)]=s;old=s
    metrics=[]
    for w,s in sorted(solutions.items()):
        m,p=profile(w,s,50); metrics.append(m)
        assert min(p[1])>-1e-8
        if w in [.8,.95,.98]:write_csv(out/f'profile_{w:.2f}.csv',['r','f','energy_density','radial_pressure','tangential_pressure'],zip(*(a[::20] for a in p)))
    write_csv(out/'branch.csv',list(metrics[0]),[m.values() for m in metrics])
    # Independent mesh/domain convergence, same branch seeded by baseline.
    conv=[]
    for R,tol in [(35,1e-6),(50,1e-8),(65,1e-9)]:
        s=solve(.8,R,tol,old=solutions[.8]);assert s.success; m,_=profile(.8,s,R);conv.append(dict(R=R,tol=tol,**m))
    # Energy threshold root via BVP, not interpolating from sparse samples.
    def threshold(w):
        s=solve(w,50,1e-8,old=solutions[.92]);assert s.success;return profile(w,s,50)[0]['E_per_Q']-1
    cross=brentq(threshold,.91,.93,xtol=1e-10)
    dyn=[]
    for w,dr in [(.8,.1),(.8,.05),(.98,.1),(.98,.05)]:
        m,ar=evolve(w,solutions[w],dr);dyn.append(m);write_csv(out/f'evolution_{w:.2f}_{dr:.2f}.csv',['t','E','Q','amplitude_weighted_rms','central_amplitude'],ar)
    hs=[hessian(w,solutions[w],dr) for w in [.8,.98] for dr in [.1,.05]]
    result=dict(branch=metrics,convergence=conv,energy_threshold_w=cross,dynamics=dyn,hessian=hs)
    (out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    # Figures are generated from actual data.
    import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
    fig,ax=plt.subplots();ax.plot([m['w'] for m in metrics],[m['E_per_Q'] for m in metrics],'o-');ax.axhline(1,ls='--');ax.set(xlabel='omega L0',ylabel='E/(Q hbar/L0)');fig.tight_layout();fig.savefig(out/'binding.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots();
    for w in [.8,.98]:
        d=np.loadtxt(out/f'evolution_{w:.2f}_0.05.csv',delimiter=',',skiprows=1);ax.plot(d[:,0],d[:,3],label=f'omega={w}')
    ax.set(xlabel='t/L0',ylabel='RMS radius / L0');ax.legend();fig.tight_layout();fig.savefig(out/'evolution.png',dpi=150);plt.close(fig)
    return result

class Audit(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.d=json.loads((ROOT/'results/summary.json').read_text())
    def test_branch(self):
        for m in self.d['branch']:
            with self.subTest(w=m['w']):
                self.assertGreater(m['central'],.1);self.assertLess(abs(m['virial']),2e-6);self.assertLess(abs(m['active_mass_ratio']-1),2e-6);self.assertGreater(m['fixed_Q_scaling_second'],0)
    def test_threshold(self): self.assertTrue(.91<self.d['energy_threshold_w']<.93)
    def test_convergence(self):
        a,b,c=self.d['convergence'];self.assertLess(abs(b['Q']/c['Q']-1),1e-6);self.assertLess(abs(a['E']/c['E']-1),1e-5)
    def test_dynamics(self):
        for m in self.d['dynamics']:
            with self.subTest(w=m['w'],dr=m['dr']):self.assertLess(m['energy_drift'],.001);self.assertLess(m['charge_drift'],1e-10)
    def test_hessian(self):
        for m in self.d['hessian']:
            self.assertLess(max(m['residuals']),1e-7)
            self.assertTrue(m['eigenvalues'][0]>0 if m['w']==.8 else m['eigenvalues'][0]<0)
    def test_bound_vs_unbound(self):
        a={m['w']:m for m in self.d['branch']}; self.assertLess(a[.8]['E_per_Q'],1);self.assertGreater(a[.98]['E_per_Q'],1)
    def test_potential(self): self.assertGreaterEqual(min(potential(np.linspace(0,5,1001))),0)
    def test_symbolic(self):
        import sympy as s
        f,w,T,K,V,z=s.symbols('f w T K V z',real=True); U=f*f/2-f**4/2+f**6/4
        self.assertEqual(s.expand(s.diff(U,f)-(f-2*f**3+s.Rational(3,2)*f**5)),0)
        self.assertEqual(s.expand(2*U/f**2-(s.Rational(1,2)+s.Rational(1,2)*(f*f-1)**2)),0)
        self.assertEqual(s.diff(T/z**3+K*z+V*z**3,z,2).subs(z,1),12*T+6*V)
if __name__=='__main__':
    main();unittest.main(argv=['audit'],verbosity=2)
