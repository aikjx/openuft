"""V94 deterministic numerical benchmarks. Theory/simulation ONLY, not measured data."""
from __future__ import annotations
import csv,json,math
from pathlib import Path
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.inverse_maxwell import InverseDrive,lorentz_frame_displacement
from src.v93_reference import TorusLoop,C,E,ME

ROOT=Path(__file__).resolve().parents[1]

def high_precision_B():
    mp.mp.dps=85
    R,a=mp.mpf('0.01'),mp.mpf('0.002')
    m,n=2,3
    v=mp.mpf('0.8')*mp.mpf('299792458')
    q=-mp.mpf('1.602176634e-19')
    mass=mp.mpf('9.1093837139e-31')
    gamma=1/mp.sqrt(1-mp.mpf('0.8')**2)
    def r(u):
        return mp.matrix([(R+a*mp.cos(n*u))*mp.cos(m*u),
                          (R+a*mp.cos(n*u))*mp.sin(m*u),a*mp.sin(n*u)])
    def dot(X,Y):return sum(x*y for x,y in zip(X,Y))
    def cross(X,Y):return mp.matrix([X[1]*Y[2]-X[2]*Y[1],X[2]*Y[0]-X[0]*Y[2],X[0]*Y[1]-X[1]*Y[0]])
    cases=[]; drive=InverseDrive()
    for j in range(8):
        angle=(mp.mpf(j)+mp.mpf('0.217'))*2*mp.pi/8
        rp=mp.matrix([mp.diff(lambda x:r(x)[i],angle) for i in range(3)])
        rpp=mp.matrix([mp.diff(lambda x:r(x)[i],angle,2) for i in range(3)])
        speed=mp.sqrt(dot(rp,rp))
        vv=rp*v/speed
        acc=v**2*(rpp/speed**2-rp*dot(rp,rpp)/speed**4)
        bm=cross(acc,vv)*gamma*mass/(q*v*v)
        bn=np.array([float(x) for x in bm])
        bfast=drive.B_and_dotB(float(angle))[0]
        rel=float(np.linalg.norm(bn-bfast)/np.linalg.norm(bn))
        cases.append({'phase_rad':float(angle),'B_tesla_high_precision':[float(x) for x in bm],
                      'B_tesla_fast':bfast.tolist(),'relative_difference':rel})
    return {'digits':85,'cases':cases,'max_relative_difference':max(c['relative_difference'] for c in cases)}


def main():
    print('NUMERIC STAGE init',flush=True)
    res=ROOT/'results';res.mkdir(exist_ok=True)
    figs=ROOT/'figures';figs.mkdir(exist_ok=True)
    drive=InverseDrive()
    loop=drive.loop
    phases=np.linspace(0,loop.primitive_period,701)
    xyz=np.array([drive.curve_state(x)[0] for x in phases])
    bfields=np.array([drive.B_and_dotB(x)[0] for x in phases])
    kappa=loop.curvature(phases)
    forces=np.array([np.linalg.norm(drive.charge*np.cross(drive.curve_state(u)[1],drive.B_and_dotB(u)[0])) for u in phases])
    # Plot: externally prescribed knot and local inverse magnetic field direction.
    fig=plt.figure(figsize=(8,6.6));ax=fig.add_subplot(projection='3d')
    ax.plot(xyz[:,0]*1000,xyz[:,1]*1000,xyz[:,2]*1000,lw=2)
    ix=np.arange(0,len(phases)-1,45)
    unitb=bfields[ix]/np.linalg.norm(bfields[ix],axis=1)[:,None]
    ax.quiver(*(xyz[ix,k]*1000 for k in range(3)), *(unitb[:,k] for k in range(3)),length=3.3,normalize=True)
    ax.set(xlabel='x (mm)',ylabel='y (mm)',zlabel='z (mm)',title='Prescribed torus-knot path and inverse magnetic drive (THEORY)')
    fig.tight_layout();fig.savefig(figs/'torus_knot_inverse_B_THEORY.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.4))
    ax.plot(phases,np.linalg.norm(bfields,axis=1))
    ax.set(xlabel='Path parameter u (rad)',ylabel='Required |B| (T)',title='Inverse magnetic field is not uniform (THEORY)')
    fig.tight_layout();fig.savefig(figs/'B_vs_phase_THEORY.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.4))
    ax.plot(phases,kappa)
    ax.set(xlabel='Path parameter u (rad)',ylabel='Curvature (1/m)',title='Nonconstant curvature excludes single uniform-B helical orbit')
    fig.tight_layout();fig.savefig(figs/'curvature_vs_phase_THEORY.png',dpi=160);plt.close(fig)
    integration=drive.integrated_orbit(samples=301)
    errs=np.linalg.norm(integration['solution']-integration['reference'],axis=1)
    fig,ax=plt.subplots(figsize=(8,4.4))
    ax.semilogy(integration['phases'],np.maximum(errs,1e-16))
    ax.set(xlabel='Path parameter u (rad)',ylabel='Scaled 6D state deviation',title='Forward Lorentz-force integration vs prescribed orbit')
    fig.tight_layout();fig.savefig(figs/'orbit_residual_THEORY.png',dpi=160);plt.close(fig)
    print('NUMERIC STAGE highprecision',flush=True)
    high=high_precision_B()
    print('NUMERIC STAGE highprecision-done',flush=True)
    (res/'INDEPENDENT_85_DIGITS.json').write_text(json.dumps(high,ensure_ascii=False,indent=2))
    monodromies=[]
    for beta in [.2,.5,.8,.95]:
        print('NUMERIC STAGE monodromy',beta,flush=True)
        dr=InverseDrive(beta=beta)
        mon=dr.monodromy_estimate(step=2e-6)
        eigen=mon['eigenvalues']
        monodromies.append({'beta':beta,'spectral_radius':mon['spectral_radius'],
                            'determinant':mon['determinant'],
                            'multipliers_real_imag':[[float(x.real),float(x.imag)] for x in eigen],
                            'matrix':mon['matrix'].tolist()})
    # Finite difference convergence diagnostic for baseline stability map
    monsteps=[]
    for h in [1e-5,2e-6,4e-7]:
        print('NUMERIC STAGE monodromy-step',h,flush=True)
        m=drive.monodromy_estimate(step=h)
        monsteps.append({'step':h,'spectral_radius':m['spectral_radius'],'determinant':m['determinant']})
    fig,ax=plt.subplots(figsize=(8,4.4))
    ax.plot([x['beta'] for x in monodromies],[x['spectral_radius'] for x in monodromies],marker='o')
    ax.axhline(1,linestyle='--')
    ax.set(xlabel='beta = v/c',ylabel='Maximum |Floquet multiplier|',title='Conditional linear stability of the inverse-driven orbit (THEORY)')
    fig.tight_layout();fig.savefig(figs/'floquet_vs_beta_THEORY.png',dpi=160);plt.close(fig)
    lorentz=lorentz_frame_displacement(drive.period,.3)
    radiation=loop.classical_radiated_energy_one_lap(beta=.8)
    summary={
       'classification':'THEORY / INVERSE-DESIGN / NUMERIC / NOT-AN-EXPERIMENT',
       'baseline':{'R_m':loop.R,'a_m':loop.a,'m':loop.m,'n':loop.n,'beta':drive.beta,'particle':'electron test particle; charge=-e','period_s':drive.period,'arc_length_m':loop.arc_length()},
       'inverse_field':{'B_min_tesla':float(np.min(np.linalg.norm(bfields,axis=1))),
                        'B_max_tesla':float(np.max(np.linalg.norm(bfields,axis=1))),
                        'max_force_N':float(np.max(forces)),
                        'max_relative_force_residual':float(max(np.linalg.norm(drive.field_force_residual(x))/max(np.linalg.norm(drive.gamma0*drive.mass*drive.curve_state(x)[2]),1e-35) for x in phases))},
       'integration':{'max_scaled_6d_error':integration['max_scaled_state_error'],
                      'terminal_scaled_6d_error':integration['terminal_scaled_state_error'],
                      'rhs_calls':integration['rhs_calls']},
       'monodromy_by_speed':monodromies,
       'monodromy_step_convergence':monsteps,
       'maxwell':{'E_zero_on_reference_path':True,'B_spatially_uniform_not_time_uniform':True,'divB_zero':True,'faraday_curlE_minus_dBdt_zero':True,'gaussE_zero':True,'required_external_current':'affine in position, unbounded spatial field energy'},
       'boost_0p3c':lorentz,
       'classical_radiation_energy_per_lap_J':radiation,
       'high_precision_B':{'digits':85,'max_relative_error':high['max_relative_difference']},
       'limitations':['prescribed fields, not a spontaneous solution','nonlocalized infinite-energy background',
                      'point particle test limit, no self field','radiation reaction omitted',
                      'linearized monodromy is local numerical property',
                      'no independent prediction of G, charge, SM representations, particle masses']
    }
    (res/'NUMERICAL_SUMMARY_THEORY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    with (res/'PHASE_FIELD_SCAN_THEORY.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['u_rad','curvature_per_m','B_tesla','force_N','x_m','y_m','z_m'])
        for k,u in enumerate(phases):w.writerow([u,kappa[k],np.linalg.norm(bfields[k]),forces[k],*xyz[k]])
    with (res/'STABILITY_BY_BETA_THEORY.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['beta','max_multiplier_abs','det_monodromy'])
        for case in monodromies:w.writerow([case['beta'],case['spectral_radius'],case['determinant']])
    print('V94 results:',json.dumps({
      'integrated_max_err':summary['integration']['max_scaled_6d_error'],
      'high_precision_max_relative':high['max_relative_difference'],
      'B_T_range':(summary['inverse_field']['B_min_tesla'],summary['inverse_field']['B_max_tesla']),
      'monodromy':[(x['beta'],x['spectral_radius']) for x in monodromies],
      'boost_drift_m':lorentz['delta_x_prime_m']},ensure_ascii=False))
    return summary
if __name__=='__main__':main()
