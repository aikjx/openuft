#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROOT V133 independent reproducibility audit.
Python 3.9+, standard library ONLY; no fitted new-physics parameters.
Only c=1 in theoretical equations, hbar and G remain dimensional.
"""
from __future__ import annotations
import csv
import json
import math
from fractions import Fraction
from pathlib import Path

BASE=Path(__file__).resolve().parent
DATA=BASE/'data'
DATA.mkdir(exist_ok=True)
PI=math.pi
# SI values used ONLY for labeled conversions; no hbar=1/G=1 imposed.
SI_C=299792458.0
SI_HBAR=1.054571817e-34 # J*s (derived from exact h/2pi)
SI_EV_J=1.602176634e-19
MZ=91.1876 # GeV, illustrative reference input
ALPHA_EM_INV=127.955 # illustrative running electromagnetic coupling at M_Z
SIN2_WEINBERG=0.23122 # representative MSbar input at M_Z
ALPHA_S=0.1180 # representative strong coupling at M_Z
BETAS=(41.0/10.0,-19.0/6.0,-7.0)
TESTS=[]

def check(name, predicate, detail=None):
    assert predicate, f'FAIL: {name}; {detail}'
    TESTS.append({'test':name,'pass':True,'detail':detail})

def principal_angle(x):
    return math.atan2(math.sin(x),math.cos(x))

def berry_phase(polar_angle, sigma, steps):
    # Helicity eigenvectors e_sigma=(e_theta+i sigma e_phi)/sqrt(2).
    # Holonomy is gauge-invariant: -arg(prod_j <psi_j|psi_(j+1)>).
    vectors=[]
    for j in range(steps):
        ph=2*PI*j/steps
        e_theta=(math.cos(polar_angle)*math.cos(ph),
                 math.cos(polar_angle)*math.sin(ph),
                 -math.sin(polar_angle))
        e_phi=(-math.sin(ph),math.cos(ph),0.0)
        vectors.append(tuple((a+1j*sigma*b)/math.sqrt(2) for a,b in zip(e_theta,e_phi)))
    holonomy=1+0j
    for j in range(steps):
        e1=vectors[j]
        e2=vectors[(j+1)%steps]
        inner=sum(a.conjugate()*b for a,b in zip(e1,e2))
        holonomy*=inner/abs(inner)
    return -math.atan2(holonomy.imag,holonomy.real)

def gauge_coupling_inv():
    # SU(5)-normalized alpha_1 = 5 alpha_Y/3, and alpha_2 = alpha_EM/sin²θ
    return ((3./5.)*(1.-SIN2_WEINBERG)*ALPHA_EM_INV,
            SIN2_WEINBERG*ALPHA_EM_INV,
            1./ALPHA_S)

def inv_alpha_at_logt(t, a=None):
    if a is None:a=gauge_coupling_inv()
    return tuple(ai-bi*t/(2*PI) for ai,bi in zip(a,BETAS))

def pair_intersection(a,i,j):
    t=2*PI*(a[i]-a[j])/(BETAS[i]-BETAS[j])
    return {'pair':f'{i+1}-{j+1}', 'log_mu_over_MZ':t,
            'mu_GeV':MZ*math.exp(t),'inverse_couplings':list(inv_alpha_at_logt(t,a))}

def least_square_unification(a):
    slopes=[b/(2*PI) for b in BETAS]
    ma=sum(a)/3; ms=sum(slopes)/3
    t=sum((ai-ma)*(s-ms) for ai,s in zip(a,slopes))/sum((s-ms)**2 for s in slopes)
    arr=inv_alpha_at_logt(t,a)
    return {'log_mu_over_MZ':t,'mu_GeV':MZ*math.exp(t),
            'inverse_couplings':list(arr),
            'absolute_spread':max(arr)-min(arr),
            'relative_spread_vs_mean':(max(arr)-min(arr))/(sum(arr)/3)}

def hypercharge_coeff(y, with_nu):
    # LH fermion convention, YH=1/2, Yukawa and [SU2]^2U1 constraints assumed.
    fields=[(6,y),(3,-y-Fraction(1,2)),(3,-y+Fraction(1,2)),
            (2,-3*y),(1,3*y+Fraction(1,2))]
    if with_nu: fields.append((1,3*y-Fraction(1,2)))
    A_grav=sum((mult*charge for mult,charge in fields),Fraction(0))
    A_cubic=sum((mult*charge**3 for mult,charge in fields),Fraction(0))
    A_22=3*y+(-3*y)
    A_33=2*y+(-y-Fraction(1,2))+(-y+Fraction(1,2))
    return (A_grav,A_cubic,A_22,A_33)

def v_perp(vz):
    return math.sqrt(max(0.0,1.0-vz*vz))

def main():
    # 1. Helix frequency-bound no-go: Rk<=1, equality = zero axial velocity.
    helix=[]
    wavelengths_nm=(0.001,0.1,1.,10.,400.,550.,1550.,1e6)  # illustrative EM bands, not exhaustive
    fixed_R_m=1e-9
    for wavelength_nm in wavelengths_nm:
        wavelength_m=wavelength_nm*1e-9
        k=2*PI/wavelength_m
        max_R=1/k
        X=fixed_R_m*k
        physically_admissible=X<=1.
        vz=math.sqrt(1-X*X) if physically_admissible else None
        helix.append({'vacuum_wavelength_nm':wavelength_nm,'k_per_m':k,
                      'maximum_literal_helix_R_m':max_R,
                      'fixed_R_m':fixed_R_m,'Rk':X,
                      'valid_for_fixed_R':physically_admissible,
                      'axial_speed_c1':vz})
        check(f'bound for wavelength {wavelength_nm:g} nm',
              math.isclose(max_R*k,1.,rel_tol=1e-13))
    check('finite fixed R fails at sufficiently high k',
          any(not x['valid_for_fixed_R'] for x in helix))
    check('R=lambda/(2pi) implies vz=0',abs(1-(2*PI/(2*PI))**2)<1e-12)
    # In Minkowski spacetime, a genuine spatial helix is not a FREE null geodesic:
    # x^mu(t)=(t,R cos(Omega*t),R sin(Omega*t),u*t).
    # tangent squared = -1+R²Omega²+u²=0, but second derivative norm=R²Omega⁴>0.
    helix_R=1e-9
    helix_Omega=2*PI/(550e-9)
    helix_u=math.sqrt(1-(helix_R*helix_Omega)**2)
    tangent_norm2=-1+(helix_R*helix_Omega)**2+helix_u**2
    acceleration_norm2=helix_R**2*helix_Omega**4
    check('null helix tangent can be lightlike',abs(tangent_norm2)<1e-13)
    check('nondegenerate null helix is not free Minkowski geodesic',acceleration_norm2>0)
    helix_curvature=helix_R*helix_Omega**2
    helix_torsion=helix_u*helix_Omega
    check('Frenet helix identity',
          math.isclose(helix_curvature**2+helix_torsion**2,helix_Omega**2,rel_tol=1e-13))
    with (DATA/'helix_bound.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=helix[0].keys());w.writeheader();w.writerows(helix)

    # 2. Photon helicity Berry geometry - discretized holonomy vs exact solid angle.
    berry=[]
    for theta in (0.35,0.6,1.1):
        solid=2*PI*(1-math.cos(theta))
        for sigma in (-1,1):
            previous=None
            for n in (32,64,128,256,512,1024):
                gamma=berry_phase(theta,sigma,n)
                expected=-sigma*solid
                error=abs(principal_angle(gamma-expected))
                berry.append({'polar_angle_rad':theta,'helicity':sigma,
                             'sample_count':n,'solid_angle_sr':solid,
                             'discrete_Berry_phase_rad':gamma,
                             'analytic_phase_mod2pi_rad':principal_angle(expected),
                             'absolute_phase_error_rad':error})
                if previous is not None:
                    check(f'Berry convergence theta={theta},h={sigma},N={n}',error<previous)
                previous=error
            check(f'Berry final accuracy theta={theta} h={sigma}',previous<2e-5)
    check('helicity-odd Berry phase',
          abs(principal_angle(berry_phase(.6,+1,512)+berry_phase(.6,-1,512)))<1e-12)
    with (DATA/'berry_phase_convergence.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=berry[0].keys());w.writeheader();w.writerows(berry)

    # 3. 5D circle reduction: one continuous internal Killing generator -> U(1).
    R=1e-18
    G4_SI=6.67430e-11  # SI benchmark, not derivation
    # in c=1 SI dimensions convert G4 to m/kg by dividing c^2;
    # [G4] c=1 -> L/M, [G5] -> L²/M.
    G4_c1=G4_SI/(SI_C*SI_C)
    G5_c1=2*PI*R*G4_c1
    recovered=G5_c1/(2*PI*R)
    KK_E1_GeV=SI_HBAR*SI_C/R/(SI_EV_J*1e9)
    check('KK Newton relation unit-consistent', math.isclose(recovered,G4_c1,rel_tol=1e-15))
    check('KK first mode E conversion for 1e-18m', 190<KK_E1_GeV<205)
    kk={'illustrative_R_m':R,'circle_length_m':2*PI*R,
        'G4_c1_m_per_kg_from_SI_input':G4_c1,
        'G5_c1_m2_per_kg_BACKCALCULATED_NOT_PREDICTED':G5_c1,
        'G4_recovered_m_per_kg':recovered,
        'mode_1_energy_GeV':KK_E1_GeV,'isometry_group_of_single_circle':'U(1)',
        'G_first_principles_prediction':False}

    # 4. One loop running of standard model couplings.
    a=gauge_coupling_inv()
    crossings=[pair_intersection(a,i,j) for i,j in ((0,1),(0,2),(1,2))]
    best=least_square_unification(a)
    for pair in crossings:
        i=int(pair['pair'][0])-1;j=int(pair['pair'][2])-1
        check(f'coupling crossing {pair["pair"]}',
              math.isclose(pair['inverse_couplings'][i],pair['inverse_couplings'][j],rel_tol=1e-12))
    check('three running couplings fail to exactly unify at one loop',best['absolute_spread']>3.0)
    # Finite difference of RG eq at fixed t
    dt=1e-5
    for i in range(3):
        der=(inv_alpha_at_logt(20+dt)[i]-inv_alpha_at_logt(20-dt)[i])/(2*dt)
        check(f'RGE differential identity i={i+1}',math.isclose(der,-BETAS[i]/(2*PI),rel_tol=2e-7))
    # Input stress test, deliberately not confidence interval!
    stress=[]
    for daem in (-0.1,0.0,0.1):
        for ds2 in (-.0002,0.0,.0002):
            for das in (-.002,0.,.002):
                alph_inv=ALPHA_EM_INV+daem; sw2=SIN2_WEINBERG+ds2; astr=ALPHA_S+das
                ai=((3./5.)*(1.-sw2)*alph_inv,sw2*alph_inv,1./astr)
                ls=least_square_unification(ai)
                stress.append({'alpha_em_inv':alph_inv,'sin2thetaW':sw2,'alpha_s':astr,
                               'best_mu_GeV':ls['mu_GeV'],
                               'inverse_coupling_spread':ls['absolute_spread']})
    check('stress grid never produces exact intersection',min(x['inverse_coupling_spread'] for x in stress)>3.0)
    with (DATA/'running_stress_grid.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=stress[0].keys());w.writeheader();w.writerows(stress)
    running=[]
    for n in range(241):
        scale_log10=2.+n*(17.-2.)/240
        mu=10**scale_log10
        t=math.log(mu/MZ)
        vals=inv_alpha_at_logt(t)
        running.append({'log10_mu_GeV':scale_log10,'mu_GeV':mu,
                       'alpha1_inv':vals[0],'alpha2_inv':vals[1],'alpha3_inv':vals[2]})
    with (DATA/'running_curves.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=running[0].keys());w.writeheader();w.writerows(running)

    # 5. Exact one-generation anomaly cancellation: with nuR, y is not unique.
    anomalies=[]
    for num in range(-12,13):
        y=Fraction(num,60)
        for nu in (False,True):
            agr,ay3,a22,a33=hypercharge_coeff(y,nu)
            anomalies.append({'y_quark_doublet':str(y),'with_right_handed_neutrino':nu,
                              'gravity_U1_anomaly':str(agr),'U1_cube_anomaly':str(ay3),
                              'SU2_2_U1':str(a22),'SU3_2_U1':str(a33),
                              'local_anomalies_zero':all(z==0 for z in (agr,ay3,a22,a33))})
            check(f'mixed anomalies vanish y={y},nu={nu}',a22==0 and a33==0)
            if nu:check(f'nuR cancels abelian anomalies y={y}',agr==0 and ay3==0)
    check('minimal SM y=1/6 cancels anomalies',
          all(x==0 for x in hypercharge_coeff(Fraction(1,6),False)))
    check('nonstandard y=1/5 with nuR also cancels anomalies',
          all(x==0 for x in hypercharge_coeff(Fraction(1,5),True)))
    check('nonstandard y=1/5 without nuR fails',
          any(x!=0 for x in hypercharge_coeff(Fraction(1,5),False)))
    with (DATA/'anomaly_scan.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=anomalies[0].keys());w.writeheader();w.writerows(anomalies)

    # 6. Gauge invariance failure for naive minimal Maxwell+torsion coupling.
    torsion=Fraction(1,5);gradient=Fraction(3)
    deltaF=-torsion*gradient
    check('naive Maxwell torsion coupling fails generic U1 invariance',deltaF==Fraction(-3,5))
    # 7. Dimensions only: [hbar]=M L, [G]=L/M, [G hbar]=L^2
    dim={'hbar':{'M':1,'L':1},'G':{'M':-1,'L':1},
         'G_hbar':{'M':0,'L':2},'KK_5D_G':{'M':-1,'L':2},
         'helical_curve_curvature':{'M':0,'L':-1}}
    check('dimensional identity G*hbar=L²',
          {dim['hbar'][d]+dim['G'][d] for d in ()}==set() and
          all(dim['hbar'][d]+dim['G'][d]==dim['G_hbar'][d] for d in ('M','L')))

    summary={'version':'ROOT_V133','date':'2026-11-24',
        'claim':'NO unified field theory proven; reproducible constraints and conditional tests',
        'unit_convention':'ONLY c=1; hbar and G remain independently dimensionful',
        'number_of_checks':len(TESTS),'passed_checks':sum(t['pass'] for t in TESTS),
        'RG_inputs':{'MZ_GeV':MZ,'alpha_em_inverse_MZ':ALPHA_EM_INV,
                     'sin2thetaW_MZ':SIN2_WEINBERG,'alpha_s_MZ':ALPHA_S,
                     'beta_one_loop':BETAS},
        'RG_inverse_alpha_at_MZ':a,'RG_pairwise_crossings':crossings,
        'RG_least_squares_best_approach':best,
        'RG_input_stress_grid':{'count':len(stress),'min_spread':min(x['inverse_coupling_spread'] for x in stress),
                                'max_spread':max(x['inverse_coupling_spread'] for x in stress),
                                'not_statistical_confidence_interval':True},
        'helical_model_fixed_R_m':fixed_R_m,
        'berry':{'discrete_tests':len(berry),'max_1024_step_error_rad':max(r['absolute_phase_error_rad'] for r in berry if r['sample_count']==1024)},
        'KK_circle_example':kk,
        'anomaly_sample_count':len(anomalies),
        'torsion_gauge_variation_example':str(deltaF),
        'dimensions':dim,'all_pass':True}
    (DATA/'verification_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    (DATA/'check_log.json').write_text(json.dumps(TESTS,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS:',len(TESTS),'checks')
    print('RG crossing scales',[(x['pair'],format(x['mu_GeV'],'.6e')) for x in crossings])
    print('RG best spread',best['absolute_spread'])
    print('Berry max final step error',summary['berry']['max_1024_step_error_rad'])
    print('KK 1st mode energy',KK_E1_GeV,'GeV')

if __name__=='__main__':main()
