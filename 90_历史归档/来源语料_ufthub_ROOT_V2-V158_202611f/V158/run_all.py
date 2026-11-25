from pathlib import Path
import csv,json,unittest
import numpy as np
from scipy.integrate import simpson
from numpy.polynomial.legendre import leggauss
from probe import solve
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results'
def U(f):return .5*f*f-.5*f**4+.25*f**6
def Up(f):return f*(1-2*f*f+1.5*f**4)
def write(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as file:
        w=csv.DictWriter(file,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def boost(s,w,b):
    r=np.linspace(0,50,12001);f,d=s.sol(r);mu,weights=leggauss(16);g=1/np.sqrt(1-b*b)
    f=f[:,None];d=d[:,None];mu=mu[None,:]
    dt=g*(1j*w*f-b*d*mu);dz=g*(d*mu-1j*b*w*f)
    e=.5*(abs(dt)**2+abs(dz)**2+d*d*(1-mu*mu))+U(f)
    p=-np.real(dt*np.conj(dz));q=np.imag(f*dt)
    integrate=lambda x: float(simpson(2*np.pi*r*r*(x@weights)/g,x=r))
    return dict(beta=b,gamma=g,E=integrate(e),Pz=integrate(p),Q=integrate(q),phase_time=g*w,phase_z=-g*b*w)
def evolution(s,w,N,case):
    L=40.;dx=L/N;steps=int(np.ceil(6/(.19*dx)));dt=6/steps
    x=(np.arange(N)-N//2)*dx; X,Y,Z=np.meshgrid(x,x,x,indexing='ij',sparse=True); r=np.sqrt(X*X+Y*Y+Z*Z)
    f=s.sol(r.ravel())[0].reshape(r.shape); k=w if case=='null_initial' else 0.
    u=f*np.exp(-1j*k*Z);v=1j*w*u
    def accel(u):
        lap=np.zeros_like(u)
        for axis in range(3):lap+=np.roll(u,1,axis)+np.roll(u,-1,axis)-2*u
        a=abs(u)**2;return lap/dx**2-(1-2*a+1.5*a*a)*u
    def measure(t):
        a=abs(u)**2; q=np.imag(np.conj(u)*v); en=.5*abs(v)**2+U(abs(u))
        for axis in range(3):en+=.5*abs(np.roll(u,-1,axis)-u)**2/dx**2
        j2=np.zeros_like(a)
        for axis in range(3):
            derivative=(np.roll(u,-1,axis)-np.roll(u,1,axis))/(2*dx)
            j2+=np.imag(np.conj(u)*derivative)**2
        phase_invariant=float((j2-q*q).sum()/(a*a).sum())
        norm=a.sum();zc=(a*Z).sum()/norm; width=np.sqrt((a*(X*X+Y*Y+(Z-zc)**2)).sum()/norm)
        return dict(case=case,N=N,t=t,E=float(en.sum()*dx**3),Q=float(q.sum()*dx**3),center_z=float(zc),rms=float(width),peak=float(abs(u).max()),phase_invariant=phase_invariant)
    rows=[measure(0)];a=accel(u)
    for i in range(steps):
        v+=.5*dt*a;u+=dt*v;a=accel(u);v+=.5*dt*a
        if (i+1)%max(1,steps//20)==0 or i+1==steps:rows.append(measure((i+1)*dt))
    e0,q0=rows[0]['E'],rows[0]['Q'];return rows,dict(case=case,N=N,dx=dx,dt=dt,steps=steps,E_drift=max(abs(a['E']/e0-1) for a in rows),Q_drift=max(abs(a['Q']/q0-1) for a in rows),initial_rms=rows[0]['rms'],final_rms=rows[-1]['rms'],final_center=rows[-1]['center_z'],initial_peak=rows[0]['peak'],final_peak=rows[-1]['peak'],initial_phase_invariant=rows[0]['phase_invariant'],final_phase_invariant=rows[-1]['phase_invariant'])
def main():
    OUT.mkdir(exist_ok=True);w=.8
    s=solve(.83,tol=1e-8);assert s.success
    for a in [.82,.81,.80]:s=solve(a,tol=1e-9,old=s);assert s.success and s.y[0,0]>.1
    boosts=[boost(s,w,b) for b in [0,.3,.6,.8,.95,.99,-.8]];E0=boosts[0]['E'];Q0=boosts[0]['Q']
    for a in boosts:
        a['M_over_E0']=np.sqrt(a['E']**2-a['Pz']**2)/E0;a['E_error']=a['E']/(a['gamma']*E0)-1;a['P_error']=(a['Pz']-a['gamma']*a['beta']*E0)/(a['gamma']*E0);a['Q_error']=a['Q']/Q0-1;a['phase_invariant_error']=a['phase_z']**2-a['phase_time']**2+w*w
    write('boost.csv',boosts)
    r=np.linspace(0,50,20001);f,d=s.sol(r);fac=4*np.pi*r*r; integ=lambda a:float(simpson(fac*a,x=r));K=integ(d*d);V=integ(f*Up(f));F=integ(f*f)
    residual=dict(grad2=K,fUp=V,f2=F,null_integral=K+V,timelike_integral=K+V-w*w*F,lower_bound=F/3,relative_timelike_residual=(K+V-w*w*F)/(w*w*F),solver_residual=float(max(s.rms_residuals)),central=float(f[0]))
    null_runs=[]
    for guessR in [2,5,8]:
        a=solve(0,50,1e-8,guessR=guessR);null_runs.append(dict(guess_radius=guessR,success=bool(a.success),max_amplitude=float(max(abs(a.y[0]))),residual=float(max(a.rms_residuals))))
    dyn=[];rows=[]
    for N in [48,64,96]:
        for case in ['rest','null_initial']:
            ar,m=evolution(s,w,N,case);rows+=ar;dyn.append(m);print(m,flush=True)
    write('evolution.csv',rows)
    result=dict(w=w,boosts=boosts,residual=residual,null_runs=null_runs,dynamics=dyn)
    (OUT/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
    fig,ax=plt.subplots()
    for case in ['rest','null_initial']:
        a=[x for x in rows if x['case']==case and x['N']==64];ax.plot([x['t'] for x in a],[x['rms'] for x in a],label=case)
    ax.set(xlabel='t/L0',ylabel='Amplitude-weighted RMS radius / L0');ax.legend();fig.tight_layout();fig.savefig(OUT/'evolution.png',dpi=160);plt.close(fig)
class Audit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=json.loads((OUT/'summary.json').read_text())
    def test_symbolic(self):
        import sympy as s
        f,L=s.symbols('f L',real=True,nonzero=True);u=f*f/(2*L*L)-f**4/2+L*L*f**6/4
        self.assertEqual(s.expand(f*s.diff(u,f)-f*f*(s.Rational(3,2)*L*L*(f*f-2/(3*L*L))**2+1/(3*L*L))),0)
    def test_boost_energy(self):
        for a in self.d['boosts']:self.assertLess(abs(a['E_error']),1e-7)
    def test_boost_momentum(self):
        for a in self.d['boosts']:self.assertLess(abs(a['P_error']),1e-7)
    def test_boost_charge(self):
        for a in self.d['boosts']:self.assertLess(abs(a['Q_error']),1e-12)
    def test_boost_invariant(self):
        for a in self.d['boosts']:
            self.assertLess(abs(a['M_over_E0']-1),1e-6);self.assertLess(abs(a['phase_invariant_error']),1e-12)
    def test_null_integral(self):
        a=self.d['residual'];self.assertGreater(a['null_integral'],a['lower_bound']);self.assertLess(abs(a['relative_timelike_residual']),1e-7)
    def test_null_solver(self):
        for a in self.d['null_runs']:self.assertTrue(a['success']);self.assertLess(a['max_amplitude'],1e-6)
    def test_evolution(self):
        for a in self.d['dynamics']:
            self.assertLess(a['E_drift'],.015);self.assertLess(a['Q_drift'],1e-11)
    def test_phase_evolution(self):
        a=[x for x in self.d['dynamics'] if x['case']=='null_initial']
        self.assertLess(abs(a[-1]['initial_phase_invariant']),abs(a[0]['initial_phase_invariant']))
        self.assertGreater(abs(a[-1]['final_phase_invariant']-a[-1]['initial_phase_invariant']),.05)
    def test_null_different(self):
        for N in [48,64,96]:
            a,b=[x for x in self.d['dynamics'] if x['N']==N];self.assertLess(abs(a['final_rms']/a['initial_rms']-1),.1);self.assertGreater(abs(b['final_center']),.1)
if __name__=='__main__':main();unittest.main(argv=['audit'],verbosity=2)
