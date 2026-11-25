from pathlib import Path
import csv,json,math
import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.optimize import minimize_scalar,brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)
checks=[]
def check(name,ok):
    if not bool(ok): raise AssertionError(name)
    checks.append(name)

f=s.symbols('f', positive=True)
models={'Maxwell':f,'Rational':f/(1+f),'Arctan':s.atan(f),'Log':s.log(1+f),'Born-Infeld':s.sqrt(1+2*f)-1}
expected={'Maxwell':s.Integer(1),'Rational':(1-3*f)/(1+f),'Arctan':(1-3*f*f)/(1+f*f),'Log':(1-f)/(1+f),'Born-Infeld':1/(1+2*f)}
# stable implementations for very small or very large f
func={'Maxwell':lambda z:z,'Rational':lambda z:z/(1+z),'Arctan':np.arctan,'Log':np.log1p,'Born-Infeld':lambda z:2*z/(np.sqrt(1+2*z)+1)}
rng=np.random.default_rng(163)
rows=[]; summary={}; fdmax=0; metricmax=0
xgrid=np.geomspace(1e-4,1e3,351)
for name,h in models.items():
    hp=s.diff(h,f); hpp=s.diff(hp,f); v=s.simplify(1+2*f*hpp/hp)
    check(name+' Maxwell limit',s.limit(h/f,f,0)==1)
    check(name+' exact speed',s.simplify(v-expected[name])==0)
    check(name+' derivative identity',s.simplify(s.diff(s.sqrt(f)*hp,f)-(hp+2*f*hpp)/(2*s.sqrt(f)))==0)
    hpfn=s.lambdify(f,hp,'numpy'); vfn=s.lambdify(f,v,'numpy'); hf=func[name]
    def I(x, tol=1e-10):
        return quad(lambda t:t*t*float(hf(t**-4)),0,x,epsabs=tol,epsrel=tol,limit=300)[0]
    if name!='Maxwell':
        total=quad(lambda t:t*t*float(hf(t**-4)),0,np.inf,epsabs=1e-11,epsrel=1e-11,limit=300)[0]
        total2=I(1)+quad(lambda t:t*t*float(hf(t**-4)),1,np.inf,epsabs=1e-12,epsrel=1e-12)[0]
        check(name+' total mass independent split',abs(total-total2)<1e-9)
        if name=='Rational': check('rational exact mass',abs(total-math.pi/(2*math.sqrt(2)))<1e-10)
        if name=='Log': check('log exact mass',abs(total-math.sqrt(2)*math.pi/3)<1e-10)
        if name=='Arctan': check('arctan exact mass',abs(total-math.pi/(6*math.sin(math.pi/8)))<1e-10)
        # gamma=0.1, A=1-2 gamma I/x, normalized radial geodesic acceleration at rest = -A'/2
        gamma=.1
        for x in np.geomspace(.025,30,80):
            dx=x*1e-4
            deriv=(I(x+dx)-I(x-dx))/(2*dx)
            exact=x*x*hf(x**-4)
            fdmax=max(fdmax,abs(deriv-exact)/max(abs(exact),1e-10))
            ap_num=((1-2*gamma*I(x+dx)/(x+dx))-(1-2*gamma*I(x-dx)/(x-dx)))/(2*dx)
            ap=2*gamma*(I(x)/x**2-x*hf(x**-4))
            metricmax=max(metricmax,abs(ap_num-ap))
        opt=minimize_scalar(lambda lx:-I(np.exp(lx))/np.exp(lx),bounds=(-10,7),method='bounded')
        crit=.5/(-opt.fun)
        if name=='Born-Infeld': crit=1/(2*math.sqrt(2))
        summary[name]={'mass_integral':total,'gamma_critical':crit,'max_compactness_radius':None if name=='Born-Infeld' else float(np.exp(opt.x))}
        if name in ['Rational','Arctan','Log']:
            root=brentq(lambda x:x**3*hf(x**-4)-I(x),.001,100)
            check(name+' acceleration reversal',abs(root**3*hf(root**-4)-I(root))<1e-9)
            summary[name]['acceleration_reversal_radius']=root
            check(name+' horizonless gamma .1',crit>.1)
        for x in xgrid:
            z=x**-4; hv=float(hf(z)); p=float(hpfn(z)); vv=float(vfn(z)); integ=I(x)
            rows.append([name,x,hv,-hv,-hv+2*z*p,vv,integ,1-2*gamma*integ/x,gamma*(x*hv-integ/x**2),8*gamma*(hv-z*p)])
    else: summary[name]={'mass_integral':None,'reason':'divergent at center'}
    for z in np.exp(rng.uniform(-8,8,512)):
        hv=float(hf(z)); p=float(hpfn(z)); vv=float(vfn(z)); p_t=-hv+2*z*p
        check(name+' stress trace sample '+str(z),abs((-hv-hv+2*p_t)-4*(z*p-hv))<=1e-11*max(1,abs(hv)))
        check(name+' positive kinetic sample '+str(z),p>0 and vv<=1+1e-12)
    summary[name]['central_density_limit']=str(s.limit(h,f,s.oo))
    summary[name]['high_field_v2_limit']=str(s.limit(v,f,s.oo))
    summary[name]['v2_zero_radius']={'Rational':3**.25,'Arctan':3**.125,'Log':1.0}.get(name)
check('mass derivative convergence',fdmax<2e-6)
check('metric derivative agreement',metricmax<1e-6)
# analytic power-law window: H~F^p, density~r^-4p, integral finite iff p<3/4, v^2=2p-1
p=s.symbols('p',positive=True); check('power-law speed',s.simplify(1+2*f*s.diff(f**p,f,2)/s.diff(f**p,f)-(2*p-1))==0)
# actual horizon roots for rational: 0.8 and 1.2 times critical
hf=func['Rational']; I=lambda x:quad(lambda t:t*t*hf(t**-4),0,x,epsabs=1e-11,epsrel=1e-11)[0]
crit=summary['Rational']['gamma_critical']; xc=summary['Rational']['max_compactness_radius']; gamma=1.2*crit
roots=[brentq(lambda x:1-2*gamma*I(x)/x,1e-5,xc),brentq(lambda x:1-2*gamma*I(x)/x,xc,100)]
for r in roots:check('rational horizon residual',abs(1-2*gamma*I(r)/r)<1e-10)
summary['Rational']['horizons_at_1.2_gamma_critical']=roots
with (OUT/'profiles.csv').open('w',newline='') as fp:
    w=csv.writer(fp);w.writerow(['model','r_L0','rho_scaled','p_r_scaled','p_t_scaled','v_perp_squared','mass_integral','metric_A_gamma_0.1','radial_acceleration_scaled','Ricci_scaled']);w.writerows(rows)
summary['verification']={'assertions':len(checks),'random_field_samples':5*512,'mass_derivative_max_relative_error':fdmax,'metric_derivative_max_absolute_error':metricmax,'profile_rows':len(rows)}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
(OUT/'tests.txt').write_text('\n'.join('PASS '+x for x in checks)+'\n',encoding='utf-8')
fig,axes=plt.subplots(2,2,figsize=(11,8))
for name in models:
    if name=='Maxwell':continue
    d=np.array([r[1:] for r in rows if r[0]==name],float)
    for ax,idx in zip(axes.flat,[1,4,6,7]):ax.plot(d[:,0],d[:,idx],label=name)
for ax,title in zip(axes.flat,['Energy density','Perpendicular characteristic speed squared','Metric A (gamma=0.1)','Radial acceleration (gamma=0.1)']):
    ax.set_xscale('log');ax.set_xlabel('r / L0');ax.set_title(title);ax.grid(alpha=.2);ax.legend(fontsize=8)
axes[0,0].set_yscale('log');axes[0,1].axhline(0,ls='--',color='black');axes[1,1].set_yscale('symlog',linthresh=1e-4)
fig.tight_layout();fig.savefig(OUT/'profiles.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
