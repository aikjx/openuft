from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv,json
P=Path(__file__).resolve().parent
(P/'data').mkdir(exist_ok=True); (P/'figures').mkdir(exist_ok=True)
checks=[]
def check(name,ok):
    checks.append((name,bool(ok)))
    if not ok: raise AssertionError(name)
def save(name,header,rows):
    with (P/'data'/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)
def field(x,b):
    r=np.linalg.norm(x,axis=-1,keepdims=True); er=x/r
    q=er+b*np.cross([0,0,1],er); w=np.linalg.norm(q,axis=-1,keepdims=True)
    n=q/w; rho=w[...,0]/r[...,0]**2
    return n,rho

def stress(x,b):
    n,rho=field(x,b); return rho[...,None,None]*n[..., :,None]*n[...,None,:]
def analytic_force(x,b):
    r=np.linalg.norm(x,axis=-1,keepdims=True); er=x/r
    q=er+b*np.cross([0,0,1],er); w=np.linalg.norm(q,axis=-1,keepdims=True)
    # q direction magnitude constant on each ray (theta constant along flow).
    # derivative along n: (n dot grad) er=(n-er*(n dot er))/r.
    d=(n:=q/w)-er/w
    a=(d+b*np.cross([0,0,1],d))/(r*w)
    return -field(x,b)[1][...,None]*a

def fd(x,b,h):
    divJ=np.zeros(x.shape[:-1]); divP=np.zeros_like(x)
    for j in range(3):
        d=np.eye(3)[j]*h
        np_,rp=field(x+d,b); nm,rm=field(x-d,b)
        divJ+=(rp*np_[...,j]-rm*nm[...,j])/(2*h)
        divP+=(stress(x+d,b)[..., :,j]-stress(x-d,b)[..., :,j])/(2*h)
    return divJ,-divP
rng=np.random.default_rng(155); x=rng.normal(size=(4096,3)); x=x/np.linalg.norm(x,axis=1)[:,None]*rng.uniform(1,5,(4096,1))
fdrows=[]; forces=[]
for b in [0,.1,.5,1,2,-1]:
    n,rho=field(x,b); f=analytic_force(x,b)
    check(f'unit speed {b}',np.max(np.abs(np.linalg.norm(n,axis=1)-1))<1e-14)
    check(f'force transverse {b}',np.max(np.abs(np.sum(n*f,axis=1)))<1e-13)
    check(f'outward radial {b}',np.min(np.sum(f*x,axis=1))>-1e-13)
    errors=[]
    for h in [1e-2,5e-3,2.5e-3,1.25e-3]:
        div,ff=fd(x,b,h); e=np.max(np.linalg.norm(ff-f,axis=1)); errors.append(e)
        fdrows.append([b,h,np.max(np.abs(div)),e])
    check(f'FD convergence {b}',errors[-1]<errors[0]/40)
    check(f'FD final error {b}',errors[-1]<2e-5)
    for r in [1,2,4,8]:
        ff=analytic_force(np.array([r,0.,0.]),b); forces.append([b,r,*ff])
    check(f'flux conservation {b}',np.max(np.abs(rho*np.sum(n*x/np.linalg.norm(x,axis=1)[:,None],axis=1)*np.sum(x*x,axis=1)-1))<1e-13)
save('field_fd.csv',['b','h','max_div_J','max_force_error'],fdrows)
save('equator_force.csv',['b','r','radial','azimuthal','z'],forces)
# angular quadrature of vector momentum exchange for whole sphere (net zero)
mu,w=np.polynomial.legendre.leggauss(48); ph=np.arange(96)*2*np.pi/96
u=np.stack(np.broadcast_arrays(np.sqrt(1-mu[:,None]**2)*np.cos(ph),np.sqrt(1-mu[:,None]**2)*np.sin(ph),mu[:,None]),axis=-1)
for b in [0,.5,1,2]:
    f=analytic_force(u,b); net=np.sum(f*w[:,None,None],axis=(0,1))*2*np.pi/96
    check(f'whole shell net vector {b}',np.linalg.norm(net)<1e-12)
# trajectory: prescribed directional field vs free photon, normalized t=L0 units
traj=[]
t=np.linspace(0,8,801)
for b in [0,.5,1,2,-1]:
    y0=np.array([1.,0.,.5]); n0,_=field(y0,b)
    sol=solve_ivp(lambda t,y:field(y,b)[0],[0,8],y0,t_eval=t,rtol=2e-12,atol=2e-13,method='DOP853'); y=sol.y.T
    r0=np.linalg.norm(y0); r=np.linalg.norm(y,axis=1); nr=np.dot(n0,y0/r0)
    th0=np.arctan2(y0[1],y0[0]); ph=th0+b*np.log(r/r0)
    ex=np.column_stack((r*np.sqrt(1-(y0[2]/r0)**2)*np.cos(ph),r*np.sqrt(1-(y0[2]/r0)**2)*np.sin(ph),r*y0[2]/r0))
    check(f'streamline integration {b}',np.max(np.linalg.norm(y-ex,axis=1))<2e-9)
    check(f'radial speed {b}',np.max(np.abs(r-r0-nr*t))<2e-9)
    traj.extend([b,ti,*yi] for ti,yi in zip(t,y))
    if b==1: curve=y; free=y0+t[:,None]*n0
save('streamlines.csv',['b','t','x','y','z'],traj)
# finite volume radial light pulse: q=4pi r^2 rho; q_t+q_r=0. First-order upwind, conservative.
pulse=[]; profiles=[]
for N in [200,400,800,1600]:
    dx=10/N;r=(np.arange(N)+.5)*dx; q=np.exp(-((r-2)/.25)**2); initial=q.sum()*dx
    steps=round(3/(.5*dx)); dt=3/steps; C=dt/dx; out=0.
    for _ in range(steps):
        out+=dt*q[-1]; q=q-C*(q-np.r_[0.,q[:-1]])
    exact=np.exp(-((r-5)/.25)**2); err=np.sum(abs(q-exact))*dx/(np.sum(exact)*dx)
    cons=abs(q.sum()*dx+out-initial)/initial
    centroid=np.sum(q*r)/np.sum(q)
    pulse.append([N,dx,err,cons,centroid]); check(f'FV conservation {N}',cons<1e-12);check(f'FV positivity {N}',q.min()>=0);check(f'FV speed {N}',abs(centroid-5)<1e-10)
    profiles.append((r,q))
check('FV grid convergence',all(pulse[i][2]>pulse[i+1][2] for i in range(3)))
save('pulse_convergence.csv',['cells','dx','relative_L1_error','relative_energy_balance','centroid'],pulse)
# Second-order TVD spatial reconstruction + SSPRK2 time stepping.
def flux(q):
    dl=q-np.r_[0.,q[:-1]]; dr=np.r_[q[1:],0.]-q
    slope=np.where(dl*dr>0,np.sign(dl)*np.minimum(abs(dl),abs(dr)),0.)
    return q+.5*slope
high=[]; highprofiles=[]
for N in [200,400,800,1600]:
    dx=10/N;r=(np.arange(N)+.5)*dx;q=np.exp(-((r-2)/.25)**2); initial=q.sum()*dx
    steps=round(3/(.4*dx)); dt=3/steps; C=dt/dx; out=0.
    for _ in range(steps):
        f0=flux(q); z=q-C*(f0-np.r_[0.,f0[:-1]])
        f1=flux(z); q=.5*q+.5*(z-C*(f1-np.r_[0.,f1[:-1]]));out+=dt*.5*(f0[-1]+f1[-1])
    exact=np.exp(-((r-5)/.25)**2);err=np.sum(abs(q-exact))*dx/(np.sum(exact)*dx)
    cons=abs(q.sum()*dx+out-initial)/initial; centroid=np.sum(q*r)/np.sum(q)
    high.append([N,dx,err,cons,centroid]); highprofiles.append((r,q))
    check(f'TVD conservation {N}',cons<1e-12);check(f'TVD positivity {N}',q.min()>=-1e-15);check(f'TVD improved error {N}',err<pulse[len(high)-1][2])
check('TVD grid convergence',all(high[i][2]>high[i+1][2] for i in range(3)))
save('pulse_tvd_convergence.csv',['cells','dx','relative_L1_error','relative_energy_balance','centroid'],high)
for b in [.1,.5,1,2]:
    f=analytic_force(np.array([1.,0.,0.]),b)
    check(f'force density inverse cube {b}',np.allclose(analytic_force(np.array([4.,0.,0.]),b),f/64,rtol=1e-13,atol=1e-15))
    check(f'handedness reflection {b}',np.allclose(analytic_force(np.array([1.,0.,0.]),-b),f*[1,-1,1]))
    check(f'equator closed form {b}',np.allclose(f,np.array([b*b,-b,0])/np.sqrt(1+b*b)))
# two counter-moving Gaussian packets, exact free transport: zero net momentum at all times but width grows.
x1=np.linspace(-20,20,16001); packet=[]
for time in [0,1,2,4,8]:
    plus=np.exp(-(x1-time)**2/2)/np.sqrt(2*np.pi);minus=np.exp(-(x1+time)**2/2)/np.sqrt(2*np.pi);total=plus+minus
    E=np.trapezoid(total,x1); mom=np.trapezoid(plus-minus,x1); variance=np.trapezoid(x1*x1*total,x1)/E
    packet.append([time,E,mom,variance]);check(f'packet conservation {time}',abs(E-2)<1e-12 and abs(mom)<1e-12);check(f'packet spreading {time}',abs(variance-(1+time*time))<1e-10)
save('parallel_packets.csv',['t','energy','momentum','variance'],packet)
# two opposing beams and isotropic discrete beams
n=np.array([1.,0.,0.]); T=np.outer(np.r_[1,n],np.r_[1,n])+np.outer(np.r_[1,-n],np.r_[1,-n]); check('two beams zero net momentum',np.all(T[0,1:]==0));check('two beams nonzero pressure',T[1,1]==2);check('two beams invariant mass density in box CM',T[0,0]==2)
# reference data only: SI output conversion; dimensionless orbit r0=1,v0=1,t0=sqrt(r0^3/GM), nonrelativistic weak-field baseline.
GM=398600.435507e9; R=6371000.; GMM=4902.800118e9; RM=1737400.; cSI=299792458.
rows=[]
for h in [0,100,200,400,800,1600,2000,10000]:
    rows.append([h,GM/(R+h*1000)**2,GMM/(RM+h*1000)**2])
save('earth_moon_reference.csv',['height_km','earth_g_m_s2','moon_g_m_s2'],rows)
r0=R+400e3;t0=np.sqrt(r0**3/GM); tt=np.linspace(0,2*np.pi,1001); state=np.array([1.,0.,0.,1.])
def rhs(t,y,mode):
    r=y[:2]; v=y[2:]; a=mode*r/np.linalg.norm(r)**3;return np.r_[v,a]
orbits={}
for mode in [-1,0,1]:
    sol=solve_ivp(lambda t,y:rhs(t,y,mode),[0,2*np.pi],state,t_eval=tt,rtol=2e-12,atol=2e-13,method='DOP853'); orbits[mode]=sol.y.T
    check(f'orbit solve {mode}',sol.success)
    if mode==-1:
        check('circular orbit radius',np.max(abs(np.linalg.norm(sol.y[:2],axis=0)-1))<1e-9)
        E=np.sum(sol.y[2:]**2,axis=0)/2-1/np.linalg.norm(sol.y[:2],axis=0);check('orbit energy',np.max(abs(E+.5))<1e-9)
    if mode==0: check('no interaction straight',np.max(abs(sol.y[1]-tt))<1e-10)
save('orbit.csv',['force_sign','t_seconds','x_m','y_m','vx_m_s','vy_m_s'],([mode,ti*t0,*(y[:2]*r0),*(y[2:]*r0/t0)] for mode,ys in orbits.items() for ti,y in zip(tt,ys)))
# physical radiation example: incident momentum flux / c (SI).
pressure=1361/cSI
check('radiation pressure positive',pressure>0)
# Figure one: spatial trajectories
fig=plt.figure(figsize=(9,6)); ax=fig.add_subplot(projection='3d');ax.plot(*curve.T,label='Prescribed spiral outflow b=1',lw=2);ax.plot(*free.T,'--',label='Free null ray, same initial direction');ax.scatter(*curve[0],color='black');ax.set(xlabel='x / L0',ylabel='y / L0',zlabel='z / L0');ax.legend();fig.tight_layout();fig.savefig(P/'figures/streamlines.png',dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4)); rr,qq=profiles[-1];ax.plot(rr,np.exp(-((rr-5)/.25)**2),label='Exact',lw=2);ax.plot(*profiles[0],label='200 cells');ax.plot(rr,qq,'--',label='Upwind 1600 cells');ax.plot(*highprofiles[-1],':',label='TVD 1600 cells',lw=2);ax.set(xlabel='r / L0',ylabel='Radial energy per length');ax.legend();fig.tight_layout();fig.savefig(P/'figures/pulse.png',dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,6));for_dummy=0
for mode,ys in orbits.items():ax.plot(ys[:,0],ys[:,1],label={-1:'Inward inverse square (Newton)',0:'No coupling',1:'Outward inverse square (matched magnitude)'}[mode]);
ax.add_patch(plt.Circle((0,0),R/r0,alpha=.2));ax.set_aspect('equal');ax.legend();ax.set(xlabel='x / r0',ylabel='y / r0');fig.tight_layout();fig.savefig(P/'figures/orbits.png',dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(7,5));xx,yy=np.meshgrid(np.linspace(-3,3,23),np.linspace(-3,3,23)); mask=(xx**2+yy**2)>.65**2; pts=np.stack([xx[mask],yy[mask],np.zeros(mask.sum())],axis=1); ff=analytic_force(pts,1); nn=np.linalg.norm(ff,axis=1);ax.quiver(pts[:,0],pts[:,1],ff[:,0]/nn,ff[:,1]/nn,nn,angles='xy');ax.set_aspect('equal');ax.set_title('Matter reaction force direction, b=1 (arrows normalized)');fig.tight_layout();fig.savefig(P/'figures/force.png',dpi=150);plt.close(fig)
summary={'tests':len(checks),'passed':sum(v for _,v in checks),'random_points':len(x),'fd_max_final':max(row[3] for row in fdrows if row[1]==.00125),'pulse':pulse,'pulse_tvd':high,'parallel_packets':packet,'equator_b1_r1_force':analytic_force(np.array([1.,0.,0.]),1).tolist(),'earth_g_surface':rows[0][1],'moon_g_surface':rows[0][2],'earth_g_400km':rows[3][1],'orbit_period_s':2*np.pi*t0,'orbit_speed_m_s':r0/t0,'orbit_final_radius_ratio':{str(m):float(np.linalg.norm(y[-1,:2])) for m,y in orbits.items()},'solar_absorption_pressure_Pa':pressure,'checks':checks}
(P/'data/summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='checks'},indent=2))
