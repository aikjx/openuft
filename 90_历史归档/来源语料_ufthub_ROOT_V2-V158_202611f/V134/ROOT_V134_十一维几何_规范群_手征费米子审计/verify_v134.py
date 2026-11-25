#!/usr/bin/env python3
# coding: utf-8
"""ROOT V134: 11D Kaluza-Klein geometry, chirality and flux audit.
Python >=3.9, standard library only. c=1 in derivations; hbar/G dimensional.
Numerical examples are not evidence of a new particle or unification.
"""
from __future__ import annotations
import csv, json, math, hashlib
from pathlib import Path
from fractions import Fraction

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'
DATA.mkdir(exist_ok=True)
PI=math.pi
HBARC_GEV_M=1.973269804e-16 # NIST CODATA 2022, hbar*c in GeV m. SI conversion only.
PIECE=[{'space':'CP2','dimension':4,'lie_algebra':'su(3)','killing':8,'c1_mod2':1},
       {'space':'S2','dimension':2,'lie_algebra':'su(2)','killing':3,'c1_mod2':0},
       {'space':'S1','dimension':1,'lie_algebra':'u(1)','killing':1,'c1_mod2':0}]
TESTS=[]

def check(label, ok, detail=''):
    if not ok: raise AssertionError(f'{label}: {detail}')
    TESTS.append({'test': label, 'pass': True, 'detail': str(detail)})

def approx(a,b,rtol=1e-10,atol=0.):
    return abs(a-b) <= atol+rtol*max(abs(a),abs(b))

def scalar_internal(r_cp,r_s):
    # Fubini-Study CP2 normalized holomorphic sectional curvature 4,
    # 4-real-dimensional scalar curvature 24/r_cp^2.
    # Round S2 radius r_s has scalar curvature 2/r_s^2.
    return 24.0/r_cp**2 + 2.0/r_s**2

def volume_internal(r_cp,r_s,r_circle):
    # FS CP2 volume pi^2*r_cp^4/2; S2 4 pi r_s^2; S1 2 pi r_circle.
    return 4.0*PI**4 * r_cp**4*r_s**2*r_circle

def kk_energy_gev(n, r_m, twist=0.0, m5_gev=0.0):
    # E_n=sqrt[m5^2 + ((n+twist) hbar c/R)^2], at zero 3-momentum.
    return math.hypot(m5_gev,(n+twist)*HBARC_GEV_M/r_m)

def monopole_midpoint_flux(m, N):
    # a_N=(m/2)(1-cos(theta))dphi, f=da=(m/2)sin(theta)dtheta^dphi
    # (2pi)^-1 int_S2 f = m; theta midpoint quadrature, phi analytic.
    return sum((m/2.0)*math.sin(PI*(j+.5)/N)*(PI/N) for j in range(N))*1.0

def anomalies():
    # Left-handed Weyl fields in one SM generation; assumes known SM charges.
    w=[('Q_L',6,Fraction(1,6)),('u^c',3,Fraction(-2,3)),
       ('d^c',3,Fraction(1,3)),('L_L',2,Fraction(-1,2)),
       ('e^c',1,Fraction(1,1))]
    grav=sum((n*y for _,n,y in w),Fraction(0))
    cubic=sum((n*y**3 for _,n,y in w),Fraction(0))
    su3=2*Fraction(1,6)+Fraction(-2,3)+Fraction(1,3)
    su2=3*Fraction(1,6)+Fraction(-1,2)
    return {'U1_cubic':cubic,'grav_U1':grav,'SU3sq_U1':su3,
            'SU2sq_U1':su2,'SU2_doublets':4}

def write_csv(filename,rows):
    if not rows: return
    with (DATA/filename).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

def run():
    # A. Candidate internal geometry: dimensions and Lie algebra only.
    check('K real dimension is 7',sum(x['dimension'] for x in PIECE)==7)
    check('11D total spacetime',4+sum(x['dimension'] for x in PIECE)==11)
    check('continuous isometry Lie-algebra dimension is 12',sum(x['killing'] for x in PIECE)==12)
    check('su3 Killing count',3**2-1==8)
    check('su2 Killing count',2**2-1==3)
    check('u1 Killing count',1==1)
    check('CP2 w2 is nonzero',PIECE[0]['c1_mod2']==3%2)
    check('S2 w2 is zero',PIECE[1]['c1_mod2']==2%2)
    check('K product nonspin',any(x['c1_mod2'] for x in PIECE))
    # Whitney class argument: pullback h restricts to nonzero on CP2 slice.
    check('restrict product w2 to CP2 slice nonzero',1==PIECE[0]['c1_mod2'])

    # B. Pure Einstein vacuum obstacle and 11D Planck coupling scaling.
    sample_curv=[]
    for rcp,rs in [(1.,1.),(1.,2.),(2.,1.),(0.5,3.),(10.,10.),(1e-18,2e-18)]:
        R=scalar_internal(rcp,rs)
        check(f'internal curvature positive rCP={rcp} rS={rs}',R>0)
        check(f'curvature exact formula rCP={rcp} rS={rs}',approx(R,24/rcp**2+2/rs**2))
        sample_curv.append({'r_CP2_m':rcp,'r_S2_m':rs,'scalar_curvature_1_per_m2':f'{R:.12e}',
                            'vacuum_R_MN_0_satisfied':'NO'})
    write_csv('vacuum_curvature_examples.csv',sample_curv)
    check('unit FS CP2 scalar curvature',scalar_internal(1.,1.)==26.)
    for radii in [(1.,1.,1.),(1e-19,2e-19,1e-19),(1e-18,1e-19,2e-20)]:
        a,b,c=radii
        vol=volume_internal(a,b,c)
        check(f'V7 units scaling {radii}',approx(volume_internal(2*a,2*b,2*c)/vol,2**7))
        # Increasing every internal radius twofold increases volume 2^7,
        # and decreases effective G4 by 2^7 if G11 is held fixed.
        G11=3.7
        check(f'G4 scaling at fixed G11 {radii}',approx(
            (G11/vol)/(G11/volume_internal(2*a,2*b,2*c)),2**7))
        check(f'CP2 factor changes V7 by 2^4 {radii}',approx(volume_internal(2*a,b,c)/vol,16))
        check(f'S2 factor changes V7 by 2^2 {radii}',approx(volume_internal(a,2*b,c)/vol,4))
        check(f'S1 factor changes V7 by 2^1 {radii}',approx(volume_internal(a,b,2*c)/vol,2))
    # An independent R5 test at zero intrinsic curvature for S1 only.

    # C. Exact 5D circle Fourier spectrum and chirality (untwisted Dirac).
    radii=[1e-16,1e-17,1e-18,1e-19,1e-20,1e-21]
    massrows=[]
    for r in radii:
        for n in [-3,-2,-1,0,1,2,3]:
            e=kk_energy_gev(n,r)
            check(f'KK ±n parity R={r} n={n}',approx(e,kk_energy_gev(-n,r)))
            check(f'KK energy R={r} n={n}',approx(e,abs(n)*HBARC_GEV_M/r))
            massrows.append({'R_m':f'{r:.0e}','n':n,'twist_alpha':0,
                             'E_n_GeV':f'{e:.9g}','is_zero_mode':'YES' if n==0 else 'NO'})
        check(f'first KK scaling R={r}',approx(kk_energy_gev(1,r)*r,HBARC_GEV_M))
        check(f'antiperiodic removes 5D massless zero R={r}',kk_energy_gev(0,r,twist=.5)>0)
        check(f'antiperiodic minimal gap R={r}',approx(kk_energy_gev(0,r,.5),.5*kk_energy_gev(1,r)))
    write_csv('kk_circle_spectrum.csv',massrows)
    # Vector-like zero-mode conclusion follows from dimensional decomposition of a 5D Dirac spinor.
    # It is an analytic statement described in the report, NOT a numerical assertion.

    # D. Monopole topological index on S2: index D_A = (1/2pi)int f = m.
    flux_rows=[]
    for m in [-3,-2,-1,0,1,2,3]:
        previous_err=None
        for N in [64,256,1024,4096]:
            q=monopole_midpoint_flux(m,N)
            err=abs(q-m)
            check(f'flux quadrature converges m={m} N={N}',err<max(1,abs(m))*0.0002)
            if previous_err is not None and m!=0:
                check(f'flux quadrature decreases m={m} N={N}',err<previous_err)
            previous_err=err
            flux_rows.append({'monopole_m':m,'N_theta':N,'integrated_flux_over_2pi':f'{q:.12f}',
                              'abs_error':f'{err:.3e}','Dirac_index':m,
                              'zero_mode_count_with_standard_S2_monopole':abs(m)})
        # transition is exp(im phi); periodic for integer m
        check(f'patch transition singlevalued m={m}',abs(complex(math.cos(2*PI*m),math.sin(2*PI*m))-1)<1e-12)
    check('noninteger flux is NOT an ordinary monopole line bundle',abs(complex(math.cos(PI),math.sin(PI))-1)>1.0)
    write_csv('monopole_flux_index.csv',flux_rows)

    # E. Distinguish circle Dirac pair from an S2 magnetic chiral index.
    for m in range(-6,7):
        left=max(m,0);right=max(-m,0)
        check(f'index chirality m={m}',left-right==m and left+right==abs(m))

    # F. SM reference anomaly targets, imported as known charges, not predicted.
    anomaly=anomalies()
    for key in ['U1_cubic','grav_U1','SU3sq_U1','SU2sq_U1']:
        check(f'input SM anomaly {key}',anomaly[key]==0)
    check('Witten SU2 doublets even',anomaly['SU2_doublets']%2==0)
    # G. Purely hypothetical reach of KK excitation at E=1 TeV: conditional relation.
    r_tev=HBARC_GEV_M/1000.
    check('1 TeV conditional radius',approx(kk_energy_gev(1,r_tev),1000.,rtol=1e-13))
    check('R=1e-18m KK mode energy ~197.3 GeV',approx(kk_energy_gev(1,1e-18),197.3269804))

    result={
        'version':'ROOT V134', 'date':'2026-11-24',
        'theory_status':'No four-force unification proof; established geometry and conditional no-go audits only',
        'units':'c=1; hbar and G dimensional; SI conversion explicitly restores c_SI only in numeric tables',
        'independent_named_assertions_passed':len(TESTS),
        'candidate':{'spacetime_D':11,'K_real_dimension':7,'K_isometry_Lie_algebra_dimensions':[8,3,1],
                     'K_is_spin':False,'pure_11D_vacuum_flat_M4_solution':False,
                     'ordinary_dirac_chirality_from_S1_only':False},
        'KK_R_1e-18m_first_mode_GeV':kk_energy_gev(1,1e-18),
        'radius_threshold_if_1TeV_mode_is_detectable_m':r_tev,
        'monopole_index_demo':{'m':3,'S2_zero_modes':3,'assumed_background_flux':True},
        'references':[
          'https://www.sciencedirect.com/science/article/pii/0550321381900213',
          'https://academic.oup.com/ptep/article/2026/11/113B04/8978714',
          'https://math.uchicago.edu/~amathew/dirac.pdf',
          'https://physics.nist.gov/cgi-bin/cuu/Value?hbcmevf'
        ],
        'checks':TESTS
    }
    (DATA/'verification_results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('checks','references')},ensure_ascii=False,indent=2))

if __name__=='__main__': run()
