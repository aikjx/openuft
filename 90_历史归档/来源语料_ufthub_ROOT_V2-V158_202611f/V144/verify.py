import math,csv,json
from pathlib import Path
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.special import roots_legendre
P=Path(__file__).resolve().parent
c=299792458.; G=6.67430e-11; R=6371000.; mu=398600.435507e9; ell=124600.; alpha=1/3
xi=(7.2973525643e-3)/(360*math.pi)*(3.8615926744e-13)**2
# PREM coefficients g/cm^3; radial coordinate x=r/R. 11 layers.
layers=[(0,1221.5,[13.0885,0,-8.8381]),(1221.5,3480,[12.5815,-1.2638,-3.6426,-5.5281]),(3480,5701,[7.9565,-6.4761,5.5283,-3.0807]),(5701,5771,[5.3197,-1.4836]),(5771,5971,[11.2494,-8.0298]),(5971,6151,[7.1089,-3.8045]),(6151,6291,[2.691,.6924]),(6291,6346.6,[2.691,.6924]),(6346.6,6356,[2.9]),(6356,6368,[2.6]),(6368,6371,[1.02])]
checks=[]
def check(n,cond):
 assert cond,n
 checks.append(n)
def write(name,header,rows):
 with (P/name).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(header);w.writerows(rows)
def rho(r,co):return 1000*np.polynomial.polynomial.polyval(r/R,co)
def integrate(fn):return sum(quad(lambda r:fn(r,rho(r,co)),lo*1000,hi*1000,epsabs=0,epsrel=1e-11)[0] for lo,hi,co in layers)
M=4*math.pi*integrate(lambda r,d:d*r*r)
# shifted shape integral avoids exp(R/ell) overflow and is dimensionless
F=4*math.pi/M*integrate(lambda r,d:d*r*ell*.5*(math.exp((r-R)/ell)-math.exp(-(r+R)/ell)))
x,w=roots_legendre(48)
def gauss(fn):
 return sum(np.dot(w,fn((lo+hi)*500+(hi-lo)*500*x,co))*(hi-lo)*500 for lo,hi,co in layers)
M2=4*math.pi*gauss(lambda r,co:rho(r,co)*r*r)
F2=4*math.pi/M2*gauss(lambda r,co:rho(r,co)*r*ell*.5*(np.exp((r-R)/ell)-np.exp(-(r+R)/ell)))
check('mass quadratures',abs(M/M2-1)<1e-12);check('shape quadratures',abs(F/F2-1)<1e-12)
# exact exterior spherical potential and derivatives
A=alpha*F
def e(r):return A*math.exp(-(r-R)/ell)
def delta(r):return e(r)*(1+r/ell)
def phi(r):return -mu/r*(1+e(r))
def grav(r):return mu/r**2*(1+delta(r))
def precession(r):
 d=delta(r); k2=1+d-e(r)*(r/ell)**2
 return 2*math.pi*(e(r)*(r/ell)**2/k2)/(math.sqrt((1+d)/k2)+1) if k2>0 else float('nan')
def red(h):
 r=R+h; return mu/c**2*(e(R)/R-e(r)/r)
def orbit(r,rtol):
 # dimensionless radius r/r0, time t sqrt(mu/r0^3), angular momentum for circular reference
 l=math.sqrt(1+delta(r)); x0=1-1e-5
 def rhs(t,y):
  x,v,ang=y; return [v,l*l/x**3-(1+delta(r*x))/x**2,l/x**2]
 def peri(t,y):return y[1]
 peri.direction=1
 sol=solve_ivp(rhs,(0,22),[x0,0.,0.],events=peri,rtol=rtol,atol=rtol*.01,max_step=.05,method='DOP853',dense_output=True)
 check('orbit success '+str(r)+' '+str(rtol),sol.success)
 ev=sol.y_events[0]; dphi=ev[1,2]-ev[0,2]-2*math.pi
 ts=np.linspace(0,20,501); ys=sol.sol(ts); xs,vs,ang=ys
 en=.5*(vs**2+l*l/xs**2)-(1+np.array([e(r*z) for z in xs]))/xs
 return dphi,float(np.ptp(en)),[(r,t*math.sqrt(r**3/mu),xx*r,aa) for t,xx,aa in zip(ts,xs,ang)]
heights=[0,100,224,255,400,490,710,1000,1450,5850,10000,378000]
rows=[]; times=[]
for h in heights:
 r=R+h*1000; d=delta(r); g=mu/r**2; T=2*math.pi*math.sqrt(r**3/mu)
 rows.append([h,g,d,g*d,T,-T*d/(math.sqrt(1+d)*(1+math.sqrt(1+d))),precession(r),red(h*1000),(1+d)/(1+delta(R+490e3))-1])
 # finite difference derivative of potential (not acceleration at R boundary, use exterior)
 rr=r+100.; step=2.; check('potential derivative '+str(h),abs((phi(rr+step)-phi(rr-step))/(2*step)/grav(rr)-1)<2e-8)
 if h in (224,400,490,710,1450):
  p1,d1,_=orbit(r,1e-10); p2,d2,tr=orbit(r,1e-12); times+=tr
  check('near circular epicycle '+str(h),abs(p2-precession(r))<1e-6)
  check('orbit convergence '+str(h),abs(p1-p2)<2e-6)
  check('energy drift '+str(h),d2<1e-11)
write('prem_layers.csv',['rmin_km','rmax_km','rho0_g_cm3','rho1','rho2','rho3'],[[lo,hi,*co,*([0]*(4-len(co)))] for lo,hi,co in layers])
write('earth_predictions.csv',['height_km','g_baseline_m_s2','relative_yukawa','extra_g_m_s2','newton_period_s','delta_period_s','near_circular_advance_rad','extra_redshift_surface_to_height','relative_GM_residual_after_490km_calibration'],rows)
write('orbit_simulation.csv',['reference_radius_m','time_s','radius_m','angle_rad'],times)
# GM from JPL DE440; system values approximate planet-only where applicable
bodies=[('Sun',1.32712440041279419e20,695700e3),('Mercury',22031.868551e9,2439.4e3),('Venus',324858.592e9,6051.8e3),('Earth',mu,6371.0084e3),('Moon',4902.800118e9,1737.4e3),('Mars system',42828.375816e9,3389.5e3),('Jupiter system',126712764.1e9,69911e3),('Saturn system',37940584.8418e9,58232e3),('Uranus system',5794556.4e9,25362e3),('Neptune system',6836527.10058e9,24622e3)]
planet=[]
for name,gm,r in bodies:
 m=gm/c**2;q=m/r**3; dn=24*xi*q
 phase=64*math.pi*xi*m/(550e-9*r*r)
 planet.append([name,gm,r,gm/r**2,m/r,q,48*q*q,dn,phase])
 check('curvature scaling '+name,math.isclose(q,m/r**3))
write('planetary_benchmark.csv',['body','GM_SI','radius_m','spherical_g_SI','compactness','tidal_curvature_m-2','Kretschmann_m-4','QED_delta_n_max','QED_grazing_phase_rad_550nm'],planet)
# WEP: Gaussian quadrature of stat+syst as illustrative 95% absolute conservative limit
eta_mean=-1.5e-15; eta_sd=math.hypot(2.3e-15,1.5e-15); eta_bound=abs(eta_mean)+1.96*eta_sd
# differential couplings multiply e.g. gY/gN, exact Eotvos relation for q_A,q_B
D=delta(R+710e3)
# LARES-vs-LAGEOS: approximate monopole comparison to published reduced parameter, not a refit
Dlares=delta(7820e3); Dlageos=delta(12220e3)
slr_pred=(Dlares-Dlageos)/(1+Dlageos); slr_mean=2e-10; slr_sigma=1.1e-9
# Gravity Probe A endpoint screening comparison, not actual data fit
h=10000e3;base_red=mu/c**2*(1/R-1/(R+h))
result={'checks_passed':len(checks),'checks':checks,'prem_mass_kg':M,'prem_shape_shifted':F,'surface_relative_yukawa':delta(R),'surface_relative_uniform':alpha*3/(R/ell)**3*((R/ell-1)/2+(R/ell+1)/2*math.exp(-2*R/ell))*(1+R/ell),'surface_relative_v119':.005954,'xi_QED_m2':xi,'published_graph_conservative_alpha_upper':.001,'candidate_over_conservative_bound':alpha/.001,'MICROSCOPE_eta_mean':eta_mean,'MICROSCOPE_eta_combined_sigma':eta_sd,'MICROSCOPE_conservative_abs_95_gaussian':eta_bound,'MICROSCOPE_710km_yukawa_fraction':D,'MICROSCOPE_approx_delta_charge_bound':eta_bound/D,'GPA_endpoint_extra_redshift':red(h),'GPA_endpoint_relative_extra':red(h)/base_red,'SLR_approx_fractional_difference':slr_pred,'SLR_published_reduced_difference':slr_mean,'SLR_published_uncertainty':slr_sigma,'SLR_nominal_residual_over_published_uncertainty':(slr_pred-slr_mean)/slr_sigma,'scalar_mass_eV':1.973269804e-7/ell,'fR_a_m2':ell**2/6,'rows':rows,'planets':planet}
(P/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','rows','planets')},indent=2)); print('height rows');print(np.array(rows)); print('planets',[(v[0],v[5],v[7]) for v in planet])
