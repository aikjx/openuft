from pathlib import Path
import json,csv, numpy as np
from scipy.integrate import solve_bvp, simpson
from scipy.special import roots_legendre
import sympy as s
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)
checks=[]
def check(name,condition):
    checks.append((name,bool(condition)))
    if not condition: raise AssertionError(name)
def hopf(x,y,z,t):
    a=x-1j*y; b=t-1j-z; d=x*x+y*y+z*z-(t-1j)**2
    return 4*np.stack([b*b-a*a,-1j*(a*a+b*b),2*a*b],axis=-1)/d[...,None]**3
# exact symbolic verification using rational numerator, avoiding slow full simplifications
x,y,z,t=s.symbols('x y z t',real=True); a=x-s.I*y; b=t-s.I-z; d=x*x+y*y+z*z-(t-s.I)**2
n=s.Matrix([b*b-a*a,-s.I*(a*a+b*b),2*a*b]); coords=[x,y,z]
def derivative(i,j): return d*s.diff(n[i],j)-3*n[i]*s.diff(d,j)
check('Hopf null complex invariant',s.expand(n.dot(n))==0)
check('Hopf divergence',s.expand(sum(derivative(i,j) for i,j in enumerate(coords)))==0)
for i,j,k in [(0,1,2),(1,2,0),(2,0,1)]:
    check('Hopf Maxwell evolution '+str(i),s.expand(derivative(i,t)+s.I*(derivative(k,coords[j])-derivative(j,coords[k])))==0)
# rotationally invariant density/momentum z component: integrate 2pi azimuth, radial compactification
# confirm azimuth independence numerically first
rng=np.random.default_rng(160); xyz=rng.normal(size=(4096,3)); ts=rng.uniform(-3,3,4096)
F=hopf(*xyz.T,ts); E=F.real; B=F.imag; w=(np.sum(E*E+B*B,axis=-1))/2; p=np.cross(E,B)
null_err=float(np.max(np.abs(np.sum(E*B,axis=-1))/w)); speed_err=float(np.max(np.abs(np.linalg.norm(p,axis=-1)/w-1)))
check('4096 point orthogonality',null_err<1e-13); check('4096 point energy flow speed',speed_err<1e-13)
rot=.71; FF=hopf(xyz[:,0]*np.cos(rot)-xyz[:,1]*np.sin(rot),xyz[:,0]*np.sin(rot)+xyz[:,1]*np.cos(rot),xyz[:,2],ts)
check('azimuthal density symmetry',np.max(np.abs(np.sum(abs(FF)**2,axis=-1)/2-w))<1e-12)
def moments(t,N):
    q,ww=roots_legendre(N); R=np.tan(np.pi*(q+1)/4); dr=(np.pi/4)*(1+R*R)
    rr=R[:,None]; mu=q[None,:]; zz=rr*mu; xx=rr*np.sqrt(1-mu*mu)
    F=hopf(xx,np.zeros_like(xx),zz,t); en=np.sum(abs(F)**2,axis=-1)/2; P=np.cross(F.real,F.imag)[...,2]
    wt=2*np.pi*(ww*R*R*dr)[:,None]*ww[None,:]
    return np.array([np.sum(wt*en),np.sum(wt*en*rr**2),np.sum(wt*en*zz),np.sum(wt*P)])
rows=[]
for tt in [0,0.5,1,2,3,4,6]:
    m=moments(tt,256); fine=moments(tt,512); en,I,Z,P=fine
    check(f'Hopf quadrature convergence t={tt}',np.max(abs(m-fine)/np.maximum(1,abs(fine)))<1e-7)
    check(f'Hopf energy t={tt}',abs(en-2*np.pi**2)<1e-8)
    check(f'Hopf second moment t={tt}',abs(I/en-(1+tt*tt))<1e-7)
    check(f'Hopf center t={tt}',abs(Z/en-tt*P/en)<1e-7)
    rows.append(dict(t=tt,E=en,I_over_E=I/en,center_z=Z/en,Pz_over_E=P/en,central_variance=I/en-(Z/en)**2))
# Skyrme hedgehog: dimensionless r, energy divided by sqrt(ab)*hbar
# E2=4pi int (r² f'²+2sin²f), E4=4pi int(2 sin²f f'²+sin⁴f/r²)
def solve(R,tol):
    eps=1e-3; r=np.geomspace(eps,R,1000); f=2*np.arctan((1.2/r)**2); v=-4*1.2**2*r/(r**4+1.2**4)
    def fun(r,y):
        f,v=y; sn=np.sin(f); return np.vstack((v,(-2*r*v-np.sin(2*f)*(v*v-1-sn*sn/r**2))/(r*r+2*sn*sn)))
    def bc(a,b): return np.array([a[0]-np.pi-eps*a[1],R*b[1]+2*b[0]])
    sol=solve_bvp(fun,bc,r,np.vstack((f,v)),tol=tol,max_nodes=30000)
    check(f'BVP convergence R={R} tol={tol}',sol.success)
    r=np.geomspace(eps,R,24000); f,v=sol.sol(r); sn=np.sin(f)
    e2=4*np.pi*simpson(r*r*v*v+2*sn*sn,x=r); e4=4*np.pi*simpson(2*sn*sn*v*v+sn**4/r**2,x=r)
    # leading tail f=C/r²; exact leading E2 tail = 8pi*C²/R³, origin missing integrals O(eps³)
    tail=8*np.pi*f[-1]**2*R; e2+=tail
    winding=-2/np.pi*simpson(sn*sn*v,x=r)
    ratio=(e2+e4)/(12*np.pi**2)
    check('unit topological degree '+str(R),abs(winding-1)<1e-5)
    check('Derrick balance '+str(R),abs(e2-e4)/(e2+e4)<2e-5)
    check('positive scale curvature '+str(R),e4>0)
    check('energy benchmark '+str(R),1.23<ratio<1.24)
    return sol,dict(R=R,tol=tol,nodes=len(sol.x),E2=e2,E4=e4,E_over_12pi2=ratio,winding=winding,virial_rel=abs(e2-e4)/(e2+e4),scale_hessian=2*e4,tail_E2=tail,peak_rms_residual=float(np.max(sol.rms_residuals)))
sols=[]; sr=[]
for R,tol in [(20,1e-6),(40,1e-7),(80,3e-8)]:
    sol,res=solve(R,tol); sols.append(sol); sr.append(res)
check('Skyrme energy convergence',abs(sr[-1]['E_over_12pi2']-sr[-2]['E_over_12pi2'])<1e-5)
# independently verify scale dependence by numerical quadrature of rescaled profile
base=sr[-1]; sol=sols[-1]; e2,e4=base['E2'],base['E4']; scan=[]
for scale in [.5,.75,1.,1.25,1.5,2.]:
    R=80; r=np.geomspace(1e-3*scale,R*scale,20000); f,v=sol.sol(r/scale); v=v/scale; sn=np.sin(f)
    E2=4*np.pi*simpson(r*r*v*v+2*sn*sn,x=r)+8*np.pi*f[-1]**2*r[-1]; E4=4*np.pi*simpson(2*sn*sn*v*v+sn**4/r**2,x=r)
    pred=scale*e2+e4/scale
    check('independent scale integration '+str(scale),abs(E2+E4-pred)/pred<1e-8)
    scan.append(dict(scale=scale,energy_ratio=(E2+E4)/(e2+e4),analytic_ratio=pred/(e2+e4)))
# nonidentifiability: same dimensionless shape, independent positive dimensional coefficients
couplings=[]
for A,Bb in [(1,1),(4,1),(1,4),(4,4),(0.25,4)]:
    L=np.sqrt(Bb/A); mass=np.sqrt(A*Bb)*(e2+e4)
    check('scale coefficient relation '+str((A,Bb)),abs(A*L-Bb/L)<1e-12)
    couplings.append(dict(a_L0_squared=A,b=Bb,L_over_L0=L,M_over_hbar_L0=mass))
def csvwrite(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvwrite('hopfion.csv',rows);csvwrite('skyrme_convergence.csv',sr);csvwrite('scale_scan.csv',scan);csvwrite('couplings.csv',couplings)
rr=np.linspace(.001,15,1001); ff,vv=sol.sol(rr); csvwrite('profile.csv',[dict(r=r,F=f,dF=v) for r,f,v in zip(rr,ff,vv)])
summary=dict(checks=len(checks),passed=sum(v for _,v in checks),null_error=null_err,speed_error=speed_err,hopfion=rows,skyrme=sr,scale_scan=scan,couplings=couplings)
(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(OUT/'tests.txt').write_text('\n'.join(f'{"PASS" if ok else "FAIL"} {name}' for name,ok in checks)+'\n',encoding='utf-8')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(); ax.plot([r['t'] for r in rows],[r['I_over_E'] for r in rows],'o-',label='about origin');ax.plot([r['t'] for r in rows],[r['central_variance'] for r in rows],'s-',label='about energy centroid');ax.set(xlabel='t / L0',ylabel='mean squared radius / L0²',title='Null Maxwell Hopfion: expansion despite linked field lines');ax.legend();fig.tight_layout();fig.savefig(OUT/'hopfion.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots();ax.plot(rr,ff);ax.set(xlabel='r / L',ylabel='F(r)',title='Skyrme B=1 radial boundary value solution');fig.tight_layout();fig.savefig(OUT/'skyrme.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots();sc=np.linspace(.3,3,300);ax.plot(sc,(e2*sc+e4/sc)/(e2+e4));ax.scatter([r['scale'] for r in scan],[r['energy_ratio'] for r in scan]);ax.set(xlabel='scale s',ylabel='E(s)/E(1)',title='Scale stability with two and four derivative energies');fig.tight_layout();fig.savefig(OUT/'scale.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
