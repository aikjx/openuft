"""Reproducible V96 numerical study. All values are THEORY, not observations."""
import csv, json, sys, time
from pathlib import Path
import numpy as np
from scipy.constants import c,e,m_e,epsilon_0
from scipy.optimize import brentq,minimize_scalar
from numpy.polynomial.legendre import leggauss
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from coil_model import TwoCoilField,circular_reference,trajectory,jacobian_return,loop_field_cyl,direct_biot_savart_ring

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'; PLOTS=ROOT/'plots'
OUT.mkdir(exist_ok=True);PLOTS.mkdir(exist_ok=True)

def fit_tune(t,x,lower,upper):
    def loss(nu):
        A=np.column_stack((np.ones_like(t),np.cos(nu*t),np.sin(nu*t)))
        coef=np.linalg.lstsq(A,x,rcond=None)[0]
        return np.mean((A@coef-x)**2)
    sol=minimize_scalar(loss,bounds=(lower,upper),method='bounded',options={'xatol':1e-12})
    return float(sol.x),float(sol.fun)

def conductor_ohmic_estimate(I,coil_radius=.01,wire_radius=.001,resistivity=1.68e-8,N=121):
    """Optional *approximate* copper heating; constant resistivity, not device design."""
    nodes,quad=leggauss(N)
    x,y=np.meshgrid(nodes,nodes,indexing='ij')
    rs=x*x+y*y
    profile=np.zeros_like(rs);sel=rs<1
    profile[sel]=np.exp(-rs[sel]/(1-rs[sel]))
    weight=quad[:,None]*quad[None,:]*wire_radius**2
    area_int=float(np.sum(weight*profile))
    square_int=float(np.sum(weight*profile**2))
    J_peak=I/area_int
    P_one=resistivity*2*np.pi*coil_radius*I**2*square_int/area_int**2
    return {'assumed_copper_resistivity_ohm_m':resistivity,'J_peak_A_per_m2':J_peak,
            'P_ohmic_two_coils_W':2*P_one,'profile_integral_m2':area_int,
            'note':'illustrative constant-room-temperature resistivity; no thermal, power-supply or insulation design'}

def main():
    start=time.time()
    field=TwoCoilField(order=21)
    base=circular_reference(field=field)
    # generate field gradient scan with current fixed at baseline
    scan=[]
    for r in np.linspace(.001,.009,161):
        br,bz=field.field(r,0.)
        idx=float(field.index(r))
        scan.append({'r_mm':float(r*1000),'Bz_T':float(bz),'field_index_n':idx,
                     'linear_radial_stable':bool(idx<1),'linear_vertical_stable':bool(idx>0)})
    with (OUT/'FIELD_INDEX_SCAN_THEORY.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=scan[0].keys());w.writeheader();w.writerows(scan)
    # independent numerical simulation, baseline and small offset
    orbit=trajectory(field,turns=100,dx=20e-6,dz=20e-6,points=5000)
    assert orbit.success
    rr=np.hypot(orbit.y[0],orbit.y[1])
    zz=orbit.y[2]
    t=orbit.t
    norm_v=np.linalg.norm(orbit.y[3:],axis=0)
    rfit,lossr=fit_tune(t,rr,.73,.9)
    zfit,lossz=fit_tune(t,zz,.48,.7)
    # 100 turns include more nonlinear shift; compare also a small pert 40 turn experiment
    fine=trajectory(field,turns=40,dx=10e-6,dz=10e-6,points=4000)
    rr2=np.hypot(fine.y[0],fine.y[1]); zz2=fine.y[2]
    nur,lossr2=fit_tune(fine.t,rr2,.75,.88)
    nuz,lossz2=fit_tune(fine.t,zz2,.5,.65)
    with (OUT/'PERTURBED_ORBIT_100_TURNS_THEORY.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['t_in_r0_over_v','x_over_r0','y_over_r0','z_over_r0','vx_over_v0','vy_over_v0','vz_over_v0'])
        for i in range(t.size):w.writerow([float(t[i]),*[float(x) for x in orbit.y[:,i]]])
    # fixed-time one-turn map six-dimensional Jacobian
    center,mat=jacobian_return(field)
    eigen=np.linalg.eigvals(mat)
    eig_records=[{'re':float(z.real),'im':float(z.imag),'modulus':float(abs(z))} for z in eigen]
    np.savetxt(OUT/'RETURN_MATRIX_6D_THEORY.csv',mat,delimiter=',',fmt='%.16e')
    # independent conductor quadrature refinement
    qscan=[]
    for order in (9,13,17,21,29,41):
        model=TwoCoilField(order=order)
        ref=circular_reference(field=model)
        qscan.append({'quadrature_order':order,'coil_current_A':ref['I_per_coil'],
                      'field_index_n':ref['n'],'B0_T':ref['B0']})
    with (OUT/'CONDUCTOR_QUADRATURE_THEORY.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=qscan[0].keys());w.writeheader();w.writerows(qscan)
    # source-free vacuum region Maxwell residual at representative off-plane point
    r0=base['r0']; z0=.001; h=5e-6
    br,bz=field.field(r0,z0)
    brp,bzp=field.field(r0+h,z0);brm,bzm=field.field(r0-h,z0)
    brzp,bzzp=field.field(r0,z0+h);brzm,bzzm=field.field(r0,z0-h)
    curlphi=float((brzp-brzm)/(2*h)-(bzp-bzm)/(2*h))
    divergence=float(((r0+h)*brp-(r0-h)*brm)/(2*h*r0)+(bzzp-bzzm)/(2*h))
    # Lienard formula, classical diagnostic, radiation reaction not in integrator
    speed=base['v'];gamma=base['gamma'];acc=speed**2/r0
    P_rad=e*e*gamma**4*acc**2/(6*np.pi*epsilon_0*c**3)
    Eturn=P_rad*base['T'];Ekin=(gamma-1)*m_e*c*c
    # independently integrate one source filament Biot Savart to check implementation
    br0,bz0=loop_field_cyl(r0,.001,.01,.008,1)
    b_ind=direct_biot_savart_ring(r0,0,.001,.01,.008,1,num=8192)
    err_biot=float(np.linalg.norm(np.array([br0,0.,bz0])-b_ind))
    # tune 3-4-5 'linearized resonant' ratio in same coil geometry
    tune_model=TwoCoilField(order=21)
    tuned_radius=float(brentq(lambda r:tune_model.index(r)-9/25,.005,.006,xtol=1e-14))
    tuned_ref=circular_reference(r0=tuned_radius,field=tune_model)
    pert_5=trajectory(tune_model,r0=tuned_radius,turns=5,dx=10e-6,dz=10e-6,rtol=1e-11)
    five_turn_pos_error=float(tuned_radius*np.linalg.norm(pert_5.y[:3,-1]-pert_5.y[:3,0]))
    report={
       'status':'THEORETICAL_MODEL_ONLY','source':'Two smooth finite-cross-section toroidal azimuthal currents, numerical quadrature',
       'baseline':base,'long_trajectory':{
         'turns':100,'initial_radial_perturbation_m':20e-6,'initial_vertical_perturbation_m':20e-6,
         'radial_min_m':float(r0*rr.min()),'radial_max_m':float(r0*rr.max()),
         'z_min_m':float(r0*zz.min()),'z_max_m':float(r0*zz.max()),
         'max_relative_speed_error':float(np.max(np.abs(norm_v-1))),
         'fitted_tunes_100_turns':{'radial':rfit,'vertical':zfit,'loss_radial':lossr,'loss_vertical':lossz},
         'fitted_tunes_small_perturbation_40_turns':{'radial':nur,'vertical':nuz,'loss_radial':lossr2,'loss_vertical':lossz2}
       },
       'return_map':{'determinant':float(np.linalg.det(mat)),'eigenvalues':eig_records,
                     'note':'neutral unit eigenvalues and their possible Jordan shear are not asymptotic stability'},
       'vacuum_maxwell_finite_difference':{'r_m':r0,'z_m':z0,'derivative_step_m':h,
                         'curl_phi_T_per_m':curlphi,'divergence_T_per_m':divergence},
       'independent_biot_savart_filament_error_T':err_biot,
       'quadrature_convergence':qscan,
       'classical_radiation':{'W':float(P_rad),'E_per_turn_J':float(Eturn),'K_electron_J':float(Ekin),
                              'fraction_kinetic_per_turn':float(Eturn/Ekin),
                              'note':'radiation reaction omitted; cannot self-maintain static-magnetic orbit'},
       'engineering_rough':conductor_ohmic_estimate(base['I_per_coil']),
       'linear_rational_tune_case':{'n':9/25,'radius_m':tuned_radius,
              'nu_r':tuned_ref['nu_r'],'nu_z':tuned_ref['nu_z'],
              'coil_current_A':tuned_ref['I_per_coil'],
              'five_turn_non_linear_return_position_error_m':five_turn_pos_error,
              'note':'linearized 4 radial and 3 vertical cycles per 5 turns; finite-amplitude motion not exactly closed'},
       'elapsed_seconds':round(time.time()-start,3)
    }
    (OUT/'NUMERICAL_SUMMARY_THEORY.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    # plot scalar r trends
    plt.figure(figsize=(9,5))
    plt.plot([d['r_mm'] for d in scan],[d['field_index_n'] for d in scan],label='n(r)')
    plt.axhline(0,linestyle='--',label='n=0');plt.axhline(1,linestyle='--',label='n=1')
    plt.axvline(r0*1e3,linestyle=':',label='reference orbit')
    plt.xlabel('Orbit radius (mm)');plt.ylabel('Field index n');plt.title('Two external finite-width coils: weak focusing window (THEORY)')
    plt.grid(alpha=.25);plt.legend();plt.tight_layout();plt.savefig(PLOTS/'01_field_index_scan_THEORY.png',dpi=155);plt.close()
    # oscillation deviation
    plt.figure(figsize=(9,5))
    turns=t/(2*np.pi)
    plt.plot(turns,(rr-1)*r0*1e6,label='radial displacement (um)')
    plt.plot(turns,zz*r0*1e6,label='vertical displacement (um)')
    plt.xlabel('Reference revolutions');plt.ylabel('Displacement (micrometres)')
    plt.title('100-turn perturbed Lorentz trajectory: bounded in this model (THEORY)')
    plt.legend();plt.grid(alpha=.25);plt.tight_layout();plt.savefig(PLOTS/'02_100_turn_perturbation_THEORY.png',dpi=155);plt.close()
    plt.figure(figsize=(9,5))
    plt.plot([v['quadrature_order'] for v in qscan],[v['field_index_n'] for v in qscan],marker='o')
    plt.xlabel('Gaussian quadrature order per conductor section');plt.ylabel('Field index n')
    plt.title('Conductor cross-section numerical quadrature refinement (THEORY)')
    plt.grid(alpha=.25);plt.tight_layout();plt.savefig(PLOTS/'03_quadrature_convergence_THEORY.png',dpi=155);plt.close()
    print(json.dumps({'baseline':base,'return_det':report['return_map']['determinant'],
              'traj_range':report['long_trajectory'],'radiation':report['classical_radiation'],
              'ohmic':report['engineering_rough'],'tuned':report['linear_rational_tune_case'],
              'seconds':report['elapsed_seconds']},ensure_ascii=False,indent=2))
    return report
if __name__=='__main__':main()
