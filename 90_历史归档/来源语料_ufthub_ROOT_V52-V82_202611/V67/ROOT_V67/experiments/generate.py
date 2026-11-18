"""Generate reproducible V67 artifacts. Requires numpy, scipy, matplotlib, sympy for full figures.
No live external inputs. All graphs label analytical toy vs published experimental constraints.
"""
from pathlib import Path
import sys,csv,json,math,datetime
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.root_v67 import *
import numpy as np
from scipy.special import jn_zeros,jv,exp1
from scipy.integrate import quad
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=ROOT/'results';DATA=ROOT/'data';OUT.mkdir(exist_ok=True);DATA.mkdir(exist_ok=True)

def csvfile(name,headers,rows):
    with (DATA/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)

# 1. independent symbolic helical calculus
r,w,u,t=sp.symbols('r omega u t',positive=True,real=True)
R=sp.Matrix([r*sp.cos(w*t),r*sp.sin(w*t),u*t]);V=R.diff(t);A=V.diff(t);J=A.diff(t)
sp_speed2=sp.simplify(V.dot(V))
sp_curvature=sp.simplify((V.cross(A)).dot(V.cross(A))/sp_speed2**3)
sp_torsion=sp.simplify(V.cross(A).dot(J)/(V.cross(A)).dot(V.cross(A)))
symbolic={
'v2':str(sp_speed2),'kappa_squared':str(sp_curvature),
'geometric_torsion':str(sp_torsion),
'v_dot_acceleration':str(sp.simplify(V.dot(A))),
'convention':'positive r and omega and u chosen for symbolic branch; numerical code supports negative axial u'
}
(OUT/'symbolic_derivations.json').write_text(json.dumps(symbolic,ensure_ascii=False,indent=2),encoding='utf-8')

# 2. three independent GUT crossings, RG plot
mz=91.1876;triples=[]
for vexp in np.linspace(math.log10(mz),19,180):
    E=10**vexp
    inverses=gauge_inverse_at_mu(E)
    triples.append([E,vexp,*inverses])
csvfile('MATH_1loop_SM_gauge_running.csv',['energy_GeV','log10_E','alpha1_inv','alpha2_inv','alpha3_inv'],triples)
crossings={f'{i+1}_{j+1}':gauge_pair_intersection(i,j) for i,j in [(0,1),(0,2),(1,2)]}
fig,ax=plt.subplots(figsize=(9,5.4))
for i,label in enumerate([r'$\alpha_1^{-1}$',r'$\alpha_2^{-1}$',r'$\alpha_3^{-1}$']):
    ax.plot([x[1] for x in triples],[x[i+2] for x in triples],label=label,lw=2)
ax.set(xlabel=r'$\log_{10}(\mu/\mathrm{GeV})$',ylabel=r'$\alpha_i^{-1}(\mu)$',title='SM one-loop gauge running — illustrative inputs, no exact triple meeting')
ax.legend();ax.grid(alpha=.3);fig.tight_layout();fig.savefig(OUT/'one_loop_gauge_running.png',dpi=160);plt.close(fig)

# 3. independent scalar threshold E1
thr=[];max_abs=0
for mu in [0.0]+list(np.geomspace(1e-5,6,150)):
    ours=threshold_F(float(mu))
    reference=1 if mu==0 else float(math.exp(-mu*mu)-mu*mu*exp1(mu*mu))
    err=abs(ours-reference);max_abs=max(max_abs,err)
    thr.append((mu,ours,reference,err))
csvfile('MATH_scalar_heatkernel_threshold.csv',['mu','F_python','F_scipy','abs_error'],thr)
fig,ax=plt.subplots(figsize=(8,4.8));ax.plot([z[0] for z in thr],[z[1] for z in thr]);ax.set(xlabel=r'$\mu=m c\ell/\hbar$',ylabel='F(mu)',title='Proper-time cutoff function (scheme-dependent)');ax.set_xscale('symlog',linthresh=.0001);ax.grid(alpha=.3);fig.tight_layout();fig.savefig(OUT/'scalar_heatkernel_threshold.png',dpi=150);plt.close(fig)

# 4. KG independent numerical check
j=jn_zeros(1,1)[0];a=1.3;ampl=.8;k=.6;mass=.4;q=j/a;omega=math.sqrt(q*q+k*k+mass*mass)
U_analytic=2*math.pi*omega**2*a*a*ampl**2*jv(2,j)**2

def energy_integrand(rad):
    J1=jv(1,q*rad);grad=q*(jv(0,q*rad)-jv(2,q*rad))/2
    over_r=J1/rad if rad>0 else q/2
    return 2*math.pi*rad*ampl**2*((omega*omega+k*k+mass*mass)*J1*J1+grad*grad+over_r*over_r)
U_numeric,quaderror=quad(energy_integrand,0,a,epsabs=1e-12,epsrel=1e-12)
rg=np.linspace(0,a,160);ecurve=[energy_integrand(z) for z in rg]
csvfile('MATH_KG_cylindrical_energy.csv',['radial_coordinate','dU_drad_natural_units'],zip(rg,ecurve))
fig,ax=plt.subplots(figsize=(8,5));ax.plot(rg,ecurve);ax.set(xlabel='radius a.u.',ylabel='dU/dr natural units',title='Conditional Klein–Gordon helical-phase cylinder energy');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'KG_helical_energy_radial.png',dpi=150);plt.close(fig)

# 5. G fit degeneracy: fitting G with N and ell produces infinite solutions
rows=[]
for N in [1,2,3,5,8,13,21,34,55,89,100]:
    ell=cutoff_length_fitted_to_G(N)
    rows.append([N,ell,g_from_length_cutoff(ell),g_from_length_cutoff(ell)/G,'FIT_TO_CODATA_NOT_PREDICTION'])
csvfile('FIT_G_N_length_degeneracy.csv',['N','fitted_ell_m','reconstructed_G_SI','ratio_to_input_G','status'],rows)
fig,ax=plt.subplots(figsize=(8,5));ax.plot([x[0] for x in rows],[x[1]/1e-35 for x in rows],marker='o');ax.set(xlabel='number of identical toy scalar fields N',ylabel='fitted cutoff length (10^-35 m)',title='Infinitely many (N, ell) reproduce G when calibrated to it');ax.grid(alpha=.3);fig.tight_layout();fig.savefig(OUT/'G_fitting_degeneracy.png',dpi=150);plt.close(fig)

# 6. Earth: point-mass + ideal dipole only
mom=earth_dipole_moment();earth=[]
for lat in range(-90,91,15):
    theta=math.radians(lat)
    for altkm in (0,200,400,1000):
        rr=R_EARTH+1000*altkm
        pos=(rr*math.cos(theta),0,rr*math.sin(theta))
        b=dipole_magnetic(pos,mom)
        earth.append([lat,altkm,rr,gravity_magnitude(rr),norm(b)*1e6])
csvfile('TOY_earth_spherical_dipole.csv',['latitude_deg','altitude_km','radius_m','gravity_m_s2','dipole_B_uT'],earth)

# 7. fifth force & experiment constraint, avoid claiming universal MICROSCOPE bound
ff=[];rplanet=R_EARTH+700e3;lam=rplanet;betaE=1.;betaB=0.;
for d in np.linspace(-1e-14,1e-14,161):
    eta=comp_dependent_eta(betaE,float(d),betaB,rplanet,lam)
    ff.append([d,eta])
csvfile('TOY_EEP_composition_dependent.csv',['betaA_minus_betaB','eta_model'],ff)
eta_obs=-1.5e-15;eta_stderr=math.sqrt(2.3**2+1.5**2)*1e-15
fig,ax=plt.subplots(figsize=(8,5));ax.plot([z[0] for z in ff],[z[1] for z in ff],label='toy eta');ax.axhline(eta_obs,label='MICROSCOPE central',linestyle='--');ax.axhspan(eta_obs-2*eta_stderr,eta_obs+2*eta_stderr,alpha=.2,label='illustrative ±2 combined sigma');ax.set(xlabel=r'$(\beta_A-\beta_B)$ [toy: beta_E=1]',ylabel='Eotvos eta',title='Composition-dependent Yukawa toy vs MICROSCOPE');ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(OUT/'MICROSCOPE_toy_constraint.png',dpi=150);plt.close(fig)

summary={
 'version':'ROOT V67','date':'2026-11-17','status':'MATHEMATICAL_AND_CONDITIONAL_RESULTS_ONLY',
 'symbolic':symbolic,
 'gauge_coupling_inverse_at_mz':gauge_inverse_at_mu(mz),
 'gauge_crossing_geV':crossings,
 'gauge_triple_unification_at_one_loop':False,
 'KG_energy_per_length_natural_units':{'analytic':U_analytic,'quadrature':U_numeric,'quad_error_estimate':quaderror,'relative_difference':abs(U_analytic-U_numeric)/U_analytic},
 'threshold_independent_max_abs_error':max_abs,
 'earth_ideal_model_surface_gravity':gravity_magnitude(R_EARTH),
 'earth_ideal_equatorial_field_uT':norm(dipole_magnetic((R_EARTH,0,0),mom))*1e6,
 'MICROSCOPE_data':{'eta_central':eta_obs,'sigma_combined':eta_stderr,'note':'External reference data, not new experiment; toy does not imply universal fifth-force exclusion.'},
 'G_input':G,'G_was_not_derived':True,
 'new_physics_experimentally_confirmed':False
}
(OUT/'numerical_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k in ('gauge_crossing_geV','KG_energy_per_length_natural_units','threshold_independent_max_abs_error','G_was_not_derived')},indent=2))
