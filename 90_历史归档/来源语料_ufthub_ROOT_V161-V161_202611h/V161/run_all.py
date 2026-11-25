from pathlib import Path
import csv,json
import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp,simpson,quad
from scipy.special import roots_legendre,erf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent; O=P/'results'; O.mkdir(exist_ok=True)
checks=[]
def check(name,ok):
    checks.append((name,bool(ok)))
    if not ok: raise AssertionError(name)
def write(name,rows):
    with (O/name).open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rng=np.random.default_rng(161)
# A: positive energy null stream stress; random directions and weights.
n=rng.normal(size=(256,128,3));n/=np.linalg.norm(n,axis=-1,keepdims=True)
w=rng.uniform(.01,1,size=(256,128));w/=w.sum(axis=1,keepdims=True)
T=np.einsum('ba,bai,baj->bij',w,n,n)
eig=np.linalg.eigvalsh(T)
check('null stream trace',np.max(abs(np.trace(T,axis1=1,axis2=2)-1))<1e-14)
check('null stream positive semidefinite',eig.min()>0)
check('opposite directions identical stress',np.allclose(T,np.einsum('ba,bai,baj->bij',w,-n,-n)))
# rank one and isotropic edge cases
for dirs,target in [(np.array([[1,0,0],[-1,0,0]]),[0,0,1]),(np.vstack((np.eye(3),-np.eye(3))),[1/3]*3)]:
    check('zero momentum '+str(len(dirs)),np.max(abs(dirs.mean(0)))==0)
    check('stress spectrum '+str(len(dirs)),np.allclose(np.linalg.eigvalsh(dirs.T@dirs/len(dirs)),target))
# B: independently solve V160 radial profile, then integrate spatially affine deformations.
def solve(R,tol):
    eps=.001;r=np.geomspace(eps,R,1000);f=2*np.arctan((1.2/r)**2);v=-4*1.2**2*r/(r**4+1.2**4)
    def fun(r,y):
        f,v=y;sn=np.sin(f);return np.vstack((v,(-2*r*v-np.sin(2*f)*(v*v-1-sn*sn/r**2))/(r*r+2*sn*sn)))
    def bc(a,b):return [a[0]-np.pi-eps*a[1],R*b[1]+2*b[0]]
    sol=solve_bvp(fun,bc,r,np.vstack((f,v)),tol=tol,max_nodes=30000)
    check(f'BVP R={R}',sol.success)
    r=np.geomspace(eps,R,24000);f,v=sol.sol(r);sn=np.sin(f)
    e2=4*np.pi*simpson(r*r*v*v+2*sn*sn,x=r)+8*np.pi*R*f[-1]**2
    e4=4*np.pi*simpson(2*sn*sn*v*v+sn**4/r**2,x=r)
    B=-2/np.pi*simpson(sn*sn*v,x=r)
    check(f'BVP virial R={R}',abs(e2-e4)/(e2+e4)<1e-7)
    check(f'BVP winding R={R}',abs(B-1)<1e-6)
    return sol,r,f,v,e2,e4,B
s1=solve(40,1e-7);sol,r,f,v,e2,e4,B=solve(80,3e-8)
check('radial convergence',abs(s1[4]+s1[5]-e2-e4)<1e-5)
# Exact affine result with x_i=ln s_i; integrated strain and cofactor isotropic.
A=np.ones((3,3))-2*np.eye(3)
def affine(x):
    z=A@np.asarray(x);return (e2*np.exp(z).sum()+e4*np.exp(-z).sum())/3
# Independent spatial quadrature: integrate diagonal strain and cofactor on sphere.
mu,wm=roots_legendre(24); phi=np.arange(48)*2*np.pi/48
nx=np.sqrt(1-mu[:,None]**2)*np.cos(phi);ny=np.sqrt(1-mu[:,None]**2)*np.sin(phi);nz=np.broadcast_to(mu[:,None],nx.shape)
N=np.stack([nx,ny,nz],axis=-1);weights=np.broadcast_to(wm[:,None]*2*np.pi/48,nx.shape)
# radial coefficients: D=t I+(p-t)nn^T; cofactor(D)=pt I+(t²-pt)nn^T
p=v*v;t=(np.sin(f)/r)**2
pint=simpson(r*r*p,x=r);tint=simpson(r*r*t,x=r)
pt=simpson(r*r*p*t,x=r);tt=simpson(r*r*t*t,x=r)
# add leading tail separately to p and t: f=C/r²
C=f[-1]*r[-1]**2;pint+=4*C*C/(3*r[-1]**3);tint+=C*C/(3*r[-1]**3)
D=tint*np.eye(3)+(pint-tint)*N[..., :,None]*N[...,None,:]
Cof=pt*np.eye(3)+(tt-pt)*N[..., :,None]*N[...,None,:]
def direct(F):
    d=np.linalg.det(F); inv=np.linalg.inv(F);a=inv@inv.T; b=F.T@F
    return float(np.sum(weights*(d*np.einsum('...ij,ij->...',D,a)+np.einsum('...ij,ij->...',Cof,b)/d)))
rows=[];maxerr=0
for i in range(256):
    x=rng.uniform(-1.1,1.1,3);Q,_=np.linalg.qr(rng.normal(size=(3,3)))
    if np.linalg.det(Q)<0:Q[:,0]*=-1
    V,_=np.linalg.qr(rng.normal(size=(3,3)))
    if np.linalg.det(V)<0:V[:,0]*=-1
    F=Q@np.diag(np.exp(x))@V.T
    calc=direct(F); pred=affine(x); err=abs(calc-pred)/pred;maxerr=max(maxerr,err)
    check(f'affine direct quadrature {i}',err<1e-10)
    check(f'affine energy bound {i}',calc/(e2+e4)>1-1e-7)
    rows.append(dict(case=i,sx=np.exp(x[0]),sy=np.exp(x[1]),sz=np.exp(x[2]),det=np.linalg.det(F),relative_energy=calc/(e2+e4),analytic_energy=pred/(e2+e4),relative_error=err))
write('affine_random.csv',rows)
# Hessian exact (balanced ideal) and centered finite difference.
H=A.T@A/3;h=1e-4;I=np.eye(3);hf=np.zeros((3,3));E0=e2+e4
for i in range(3):
    for j in range(3):
        hf[i,j]=(affine(h*(I[i]+I[j]))-affine(h*(I[i]-I[j]))-affine(h*(-I[i]+I[j]))+affine(-h*(I[i]+I[j])))/(4*h*h*E0)
check('Hessian spectrum',np.allclose(np.linalg.eigvalsh(H),[1/3,4/3,4/3]))
check('independent finite difference Hessian',np.max(abs(hf-H))<1e-6)
x=sp.symbols('x0:3');J=sp.ones(3)-2*sp.eye(3);z=J*sp.Matrix(x)
Es=sum(sp.cosh(q) for q in z)/3
check('symbolic Hessian',sp.hessian(Es,x).subs(dict.fromkeys(x,0))==J.T*J/3)
scan=[]
for s in [.5,.75,1,1.25,1.5,2]:
    scan.append(dict(s=s,isotropic=affine(np.log([s,s,s]))/E0,volume_preserving=affine(np.log([s,1/s,1]))/E0))
write('affine_scan.csv',scan)
# C: same static Green kernel, opposite source coupling. Two normalized Gaussian sources.
# sigma is each source's Cartesian standard deviation; pair transform exp(-sigma² k²).
def kernel(R,mu,sig):
    upper=12/sig
    val=quad(lambda k:k*np.sin(k*R)*np.exp(-(sig*k)**2)/(k*k+mu*mu),0,upper,epsabs=2e-11,limit=600)[0]/(2*np.pi**2*R)
    deriv=quad(lambda k:k*k*np.cos(k*R)*np.exp(-(sig*k)**2)/(k*k+mu*mu),0,upper,epsabs=2e-11,limit=600)[0]/(2*np.pi**2*R)-val/R
    return val,deriv
force=[];cerr=0;ferr=0
for mu in [0,.5,1,2]:
    for sig in [.1,.2,.4]:
        for R in [.5,1,2,4]:
            K,Kp=kernel(R,mu,sig);hh=1e-4*R
            fd=(kernel(R+hh,mu,sig)[0]-kernel(R-hh,mu,sig)[0])/(2*hh)
            ferr=max(ferr,abs(fd-Kp)/max(abs(Kp),1e-12))
            check(f'kernel derivative {mu} {sig} {R}',abs(fd-Kp)<1e-7)
            check(f'force signs {mu} {sig} {R}',K>0 and Kp<0)
            if mu==0:
                ex=erf(R/(2*sig))/(4*np.pi*R);err=abs(K-ex)/ex;cerr=max(cerr,err)
                check(f'Coulomb gaussian analytic {sig} {R}',err<1e-9)
            force.append(dict(mu=mu,sigma=sig,r=R,kernel=K,scalar_force=Kp,vector_force=-Kp,point_force_abs=(1+mu*R)*np.exp(-mu*R)/(4*np.pi*R*R),derivative_error=abs(fd-Kp)))
write('exchange.csv',force)
summary=dict(checks=len(checks),passed=sum(ok for _,ok in checks),null_stress_min_eigen=float(eig.min()),null_stress_trace_error=float(np.max(abs(np.trace(T,axis1=1,axis2=2)-1))),E2=e2,E4=e4,winding=B,affine_max_relative_error=maxerr,Hessian=H.tolist(),Hessian_fd=hf.tolist(),Hessian_eigenvalues=np.linalg.eigvalsh(H).tolist(),Hessian_max_error=float(np.max(abs(hf-H))),affine_cases=len(rows),exchange_cases=len(force),Coulomb_max_relative_error=cerr,force_fd_max_relative_error=ferr)
(O/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');(O/'tests.txt').write_text('\n'.join('PASS '+k for k,v in checks if v)+'\n',encoding='utf8')
fig,ax=plt.subplots();ss=np.linspace(.45,2.2,200);ax.plot(ss,[affine(np.log([s]*3))/E0 for s in ss],label='isotropic');ax.plot(ss,[affine(np.log([s,1/s,1]))/E0 for s in ss],label='volume preserving');ax.set(xlabel='scale s',ylabel='E / E0',title='Affine deformation of Skyrme B=1');ax.legend();fig.tight_layout();fig.savefig(O/'affine.png',dpi=150);plt.close(fig)
fig,ax=plt.subplots();rr=np.linspace(.35,5,100)
for mu in [0,1]:
    fp=np.array([kernel(x,mu,.2)[1] for x in rr]);ax.plot(rr,fp,label=f'scalar, mu={mu}');ax.plot(rr,-fp,'--',label=f'vector, mu={mu}')
ax.axhline(0,lw=.7);ax.set(xlabel='r / L0',ylabel='force / (hbar/L0²)',title='Same propagator, different interaction signs');ax.legend();fig.tight_layout();fig.savefig(O/'exchange.png',dpi=150);plt.close(fig)
print(json.dumps(summary,indent=2))
