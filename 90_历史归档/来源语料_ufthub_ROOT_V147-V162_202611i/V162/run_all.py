import numpy as np, sympy as sp, json, csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent/'results';P.mkdir(exist_ok=True)
checks=[]
def check(name,ok):
    assert bool(ok),name
    checks.append(name)
def dump(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Symbolic trace, angle relations, energy flux.
X,Y,u,a,b=sp.symbols('X Y u a b',real=True)
L=X+a*X**2+b*Y**2
trace=4*(L-X*sp.diff(L,X)-Y*sp.diff(L,Y))
check('trace identity',sp.expand(trace+4*(a*X**2+b*Y**2))==0)
rho=sp.expand((1+2*a*X)*(u+X)+2*b*Y**2-L)
check('energy identity',sp.expand(rho-(u+a*(2*X*u+X**2)+b*Y**2))==0)
t=sp.symbols('t', real=True)
check('magnetic limiting pressure',sp.expand((rho+trace).subs({X:-u,Y:0})-(u-5*a*u**2))==0)
rng=np.random.default_rng(162); n=16384
ang=rng.uniform(0,np.pi,n); pol=rng.uniform(-np.pi,np.pi,n); A=rng.uniform(.01,2,n); C=rng.uniform(.01,2,n)
z=np.zeros(n); o=np.ones(n)
n1=np.stack([z,z,o],1); n2=np.stack([np.sin(ang),z,np.cos(ang)],1)
e1=np.stack([A,z,z],1); e2=C[:,None]*np.stack([np.cos(pol)*np.cos(ang),np.sin(pol),-np.cos(pol)*np.sin(ang)],1)
B1=np.cross(n1,e1);B2=np.cross(n2,e2); E=e1+e2;B=B1+B2
xx=(np.sum(E*E,1)-np.sum(B*B,1))/2;yy=np.sum(E*B,1)
err=max(np.max(abs(xx+A*C*(1-np.cos(ang))*np.cos(pol))),np.max(abs(yy-A*C*(1-np.cos(ang))*np.sin(pol))))
check('two beam invariants 16384',err<2e-14)
# random field bound with positive couplings
E=rng.normal(size=(n,3));B=rng.normal(size=(n,3)); ee=np.sum(E*E,1);bb=np.sum(B*B,1);u=(ee+bb)/2;xx=(ee-bb)/2;yy=np.sum(E*B,1)
a=.2;b=.35; p=u+a*(2*xx*u-3*xx**2)-3*b*yy**2
bound=u-5*max(a,b)*u*u
check('invariant inequality',np.max(xx**2+yy**2-u*u)<1e-12)
check('stress lower bound',np.min(p-bound)>=-1e-12)
# rescale to uniformly weak regime, test strict positive spatial trace
s=np.sqrt(.1/(max(a,b)*u));E*=s[:,None];B*=s[:,None]; ee=np.sum(E*E,1);bb=np.sum(B*B,1);u=(ee+bb)/2;xx=(ee-bb)/2;yy=np.sum(E*B,1)
p=u+a*(2*xx*u-3*xx**2)-3*b*yy**2
check('weak field strict trace',np.min(p/u)>.499999999)
# magnetic background exact characteristic speeds
speed=[]
for B0 in [0,.1,.2,.3,.4,.5,.6,.7,.8,1.0]:
    v1=(1-3*a*B0**2)/(1-a*B0**2);v2=(1-a*B0**2)/(1-a*B0**2+2*b*B0**2)
    check(f'magnetic speeds {B0}',0<v1<=1 and 0<v2<=1)
    speed.append(dict(B0=B0,v_perp=np.sqrt(v1),v_parallel=np.sqrt(v2)))
dump('speeds.csv',speed)
# Conservative variables D,B, pseudospectral derivative periodic. Smooth well-separated pulses.
def simulate(N,a,T=12):
    box=40.;dx=box/N;x=np.arange(N)*dx-box/2;k=2*np.pi*np.fft.fftfreq(N,dx); k[N//2]=0
    ep=.5*np.exp(-((x+5)/1.2)**2/2);em=.5*np.exp(-((x-5)/1.2)**2/2)
    E=ep+em;B=ep-em;D=(1+a*(E*E-B*B))*E
    def recover(D,B):
        E=D.copy()
        for _ in range(7): E-=(E*(1+a*(E*E-B*B))-D)/(1+a*(3*E*E-B*B))
        return E
    def energy(D,B,E):
        X=(E*E-B*B)/2;return dx*np.sum(D*E-X-a*X*X)
    def rhs(D,B):
        E=recover(D,B);H=(1+a*(E*E-B*B))*B
        return -np.fft.ifft(1j*k*np.fft.fft(H)).real,-np.fft.ifft(1j*k*np.fft.fft(E)).real
    E0=energy(D,B,E);P0=dx*np.sum(D*B);d0=dx*np.sum(D);b0=dx*np.sum(B)
    steps=int(np.ceil(T/(.22*dx)));dt=T/steps;maxdr=0;maxp=0;maxflux=0;maxinv=0;maxres=0;minjac=1e9;maxweak=0
    hist=[]
    def record(t):
        E=recover(D,B);up=(E+B)**2/4;um=(E-B)**2/4
        return dict(t=t,right_center=np.sum(x*up)/np.sum(up),left_center=np.sum(x*um)/np.sum(um),energy=energy(D,B,E),max_X=float(np.max(abs((E*E-B*B)/2))))
    hist.append(record(0.))
    for j in range(steps):
        d1,b1=rhs(D,B);d2,b2=rhs(D+dt*d1/2,B+dt*b1/2);d3,b3=rhs(D+dt*d2/2,B+dt*b2/2);d4,b4=rhs(D+dt*d3,B+dt*b3)
        D+=dt*(d1+2*d2+2*d3+d4)/6;B+=dt*(b1+2*b2+2*b3+b4)/6
        E=recover(D,B); maxdr=max(maxdr,abs(energy(D,B,E)/E0-1));maxp=max(maxp,abs(dx*np.sum(D*B)-P0)/E0);maxflux=max(maxflux,abs(dx*np.sum(D)-d0),abs(dx*np.sum(B)-b0));maxinv=max(maxinv,np.max(abs((E*E-B*B)/2)));maxres=max(maxres,np.max(abs(E*(1+a*(E*E-B*B))-D)));minjac=min(minjac,np.min(1+a*(3*E*E-B*B)));maxweak=max(maxweak,np.max(a*(E*E+B*B)/2))
        if (j+1)%max(1,steps//120)==0 or j+1==steps:hist.append(record((j+1)*dt))
    final=record(T);right=final['right_center'];ref=ep # analytic shifted Gaussian
    exact=.5*np.exp(-((x+5-T)/1.2)**2/2)+.5*np.exp(-((x-5+T)/1.2)**2/2)
    err=np.linalg.norm(E-exact)/np.linalg.norm(exact)
    check(f'energy drift N{N} a{a}',maxdr<2e-5);check(f'flux momentum N{N} a{a}',max(maxp,maxflux)<1e-8);check(f'constitutive N{N} a{a}',maxres<1e-12 and minjac>0);check(f'weak N{N} a{a}',maxweak<.2)
    dump(f'history_{N}_{a}.csv',hist)
    return dict(N=N,a=a,steps=steps,energy_drift=maxdr,momentum_error=maxp,flux_error=maxflux,max_X=maxinv,max_au=maxweak,min_jac=minjac,constitutive_error=maxres,right_center=right,left_center=final['left_center'],delay=7-right,maxwell_relative_difference=err),hist,x,E,exact
rows=[];histories={}
for coef in [0.,.2]:
    for N in [256,512,1024]:
        row,h,x,E,exact=simulate(N,coef);rows.append(row);histories[N,coef]=h
        if N==1024 and coef==.2:
            plt.plot(x,exact,label='Maxwell');plt.plot(x,E,'--',label='Nonlinear');plt.xlim(-12,12);plt.xlabel('x/L0');plt.ylabel('E L0^2');plt.legend();plt.tight_layout();plt.savefig(P/'collision.png',dpi=180);plt.close()
check('Maxwell analytic accuracy',rows[2]['maxwell_relative_difference']<1e-6)
check('nonlinear delay positive',rows[-1]['delay']>0.01)
check('delay convergence',abs(rows[-1]['delay']-rows[-2]['delay'])<1e-5)
dump('collision.csv',rows)
for coef in [0.,.2]:
    h=histories[1024,coef];plt.plot([v['t'] for v in h],[v['right_center'] for v in h],label=f'a/L0^4={coef}')
plt.xlabel('t/L0');plt.ylabel('Right-moving centroid / L0');plt.legend();plt.tight_layout();plt.savefig(P/'centroid.png',dpi=180);plt.close()
# QED benchmark, SI conversion only; input alpha, electron rest energy, reduced Compton wavelength.
alpha=7.2973525643e-3; mec2=510998.95069; lam=3.8615926744e-13
qed=[]
for ev in [1,1.55,10,100,1000]:
    sig=973/(10125*np.pi)*alpha**4*(ev/mec2)**6*lam**2
    qed.append(dict(photon_eV=ev,cross_section_m2=sig))
dump('qed.csv',qed)
check('QED scaling',abs(qed[2]['cross_section_m2']/qed[0]['cross_section_m2']/1e6-1)<1e-14)
result=dict(check_count=len(checks),checks=checks,angular_samples=n,angular_max_error=err,stress_samples=n,weak_min_trace_ratio=float(np.min(p/u)),collision=rows,qed=qed,speeds=speed)
(P/'summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
