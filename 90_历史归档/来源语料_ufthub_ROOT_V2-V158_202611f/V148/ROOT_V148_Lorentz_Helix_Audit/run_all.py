"""Deterministic run: tests, independent symbolic audit, numeric result generation."""
import csv,io,json,sys,unittest,re
from pathlib import Path
from math import pi
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from root_v148.helix import NullHelix
from root_v148.emwave import CircularWave
from root_v148.gravity import EARTH,MOON
from symbolic_audit import audit

def write_csv(filename,cols,rows):
    with (ROOT/'results'/filename).open('w',newline='',encoding='utf-8') as f:
        out=csv.writer(f);out.writerow(cols);out.writerows(rows)

def main():
    output=io.StringIO()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
    result=unittest.TextTestRunner(stream=output,verbosity=2).run(suite)
    text=re.sub(r"Ran (\d+) tests in [\d.]+s", r"Ran \1 tests [timing omitted for reproducibility]", output.getvalue())
    print(text[-1200:])
    if not result.wasSuccessful():
        (ROOT/'results'/'test_log.txt').write_text(text,encoding='utf-8');raise SystemExit('Numeric tests failed')
    sym_count=audit()
    log=text+f'\nSymbolic exact checks: {sym_count} passed\n'
    (ROOT/'results'/'test_log.txt').write_text(log,encoding='utf-8')
    h=NullHelix(.6,1,.8)
    betas=[-.95,-.8,-.5,-.3,0,.2,.3,.5,.8,.95]
    boost_rows=[]
    for b in betas:
        hb=h.boost(b);D=h.doppler_particle(b)
        boost_rows.append([f'{b:.8f}',f'{D:.12f}',f'{hb.omega:.12f}',f'{hb.u:.12f}',f'{hb.curvature():.12f}',f'{hb.torsion():.12f}',f'{D*D:.12f}',f'{hb.speed():.12f}'])
    write_csv('boost_scan.csv',['beta','E_prime_over_E','omega_prime','u_prime','kappa_prime','tau_prime','E_over_hbar_omega_ratio_factor','spatial_speed'],boost_rows)
    write_csv('earth_moon_reference.csv',['body','altitude_km','g_spherical_m_s2','normalized_r2g_over_GM'],[[body.name,alt,f'{body.g(alt*1000):.12f}',f'{body.distance_ratio(0,alt*1000):.12f}'] for body in (EARTH,MOON) for alt in (0,100,200,400,800,2000)])
    wave=CircularWave(1,1,1)
    write_csv('circular_wave.csv',['phase','Ex','Ey','Bx','By','poynting_z','E_dot_B'],[[f'{2*pi*i/48:.12f}',*(f'{x:.12f}' for x in (*wave.fields(2*pi*i/48,0)[0][:2],*wave.fields(2*pi*i/48,0)[1][:2],wave.poynting(2*pi*i/48,0)[2],wave.invariants(2*pi*i/48,0)[0]))] for i in range(49)])
    data={'status':'Model and mathematical tests only; no observational ROOT confirmation',
      'units':'c=1 only, hbar and G remain dimensionful',
      'tests':{'python':result.testsRun,'passed':result.testsRun-len(result.failures)-len(result.errors),'sympy_checks':sym_count},
      'sample':{'a_in_L0':.6,'omega_in_invL0':1.,'u':.8,'kappa_in_invL0':h.curvature(),'tau_in_invL0':h.torsion(),
      'beta_equal_u':.8,'transformed_omega_in_invL0':h.boost(.8).omega,
      'transformed_kappa_in_invL0':h.boost(.8).curvature(),
      'transformed_tau_in_invL0':h.boost(.8).torsion(),
      'particle_Eprime_over_E':h.doppler_particle(.8),'particle_Eprime_over_hbar_omega_prime_factor':h.doppler_particle(.8)**2,
      'four_accel_squared_in_invL0sq':h.four_second_norm(0)},
      'gravity_empirical_inputs':{'source':'JPL DE440 https://ssd.jpl.nasa.gov/astro_par.html', 'earth_GM_km3_s2':398600.435507,'moon_GM_km3_s2':4902.800118,'earth_mean_radius_m_approx':EARTH.radius_m,'moon_mean_radius_m':MOON.radius_m},
      'baseline_g_m_s2':{'Earth_surface_spherical':EARTH.g(),'Moon_surface_spherical':MOON.g()},
      'open_questions':['derive dynamical action from microscopic helix','derive correct gauge groups and chiral matter','derive G and particle parameters without imported measurements','validate against actual data with covariance']}
    (ROOT/'results'/'results.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f"ROOT V148: {result.testsRun} Python tests + {sym_count} SymPy exact checks PASSED. Outputs in results/")
    return data

if __name__=='__main__':main()
