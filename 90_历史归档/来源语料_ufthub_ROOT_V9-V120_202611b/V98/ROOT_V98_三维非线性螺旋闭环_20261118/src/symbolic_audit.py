"""ROOT V98 symbolic and SI audit: exact identities and dimensional checks.
Does not prove that nature selects this periodic orbit or any unification.
"""
import json
from pathlib import Path
from sympy import symbols, sqrt, simplify, Matrix, diff, pi, Rational, Function
ROOT=Path(__file__).resolve().parents[1]


def main():
    checks={}
    r, dr, phi, dphi, z, dz, m, c, q, B, A, gamma, psi = symbols(
      'r dr phi dphi z dz m c q B A gamma psi',real=True,nonzero=True)
    vx,vy,vz,bx,by,bz=symbols('vx vy vz bx by bz',real=True)
    velocity=Matrix([vx,vy,vz]);bfield=Matrix([bx,by,bz])
    checks['magnetic_lorentz_no_work']=simplify(velocity.dot(velocity.cross(bfield)))==0
    checks['speed_v2_component_decomp']=simplify((dr*dr+r*r*dphi*dphi+dz*dz)-(dr**2+(r*dphi)**2+dz**2))==0
    # Canonical momentum from L = -mc^2 sqrt(1-v^2/c^2)+q psi phi_dot
    v2=dr**2+r**2*dphi**2+dz**2
    L=-m*c**2*sqrt(1-v2/c**2)+q*psi*dphi
    desired=m*r**2*dphi/sqrt(1-v2/c**2)+q*psi
    checks['noether_p_phi']=simplify(diff(L,dphi)-desired)==0
    checks['p_phi_cyclic']=simplify(diff(L,phi))==0
    flux=Function('Psi')(r,z)
    Br=-diff(flux,z)/r; Bz=diff(flux,r)/r
    checks['axisymmetric_flux_divB_identity']=simplify(diff(r*Br,r)/r+diff(Bz,z))==0
    # product SI powers [M,L,T,I], coordinates, moments, energy, B, q, flux
    units={
      'm':(1,0,0,0),'r':(0,1,0,0),'v':(0,1,-1,0),
      'a':(0,1,-2,0),'time':(0,0,1,0),'omega':(0,0,-1,0),
      'curvature':(0,-1,0,0),'torsion':(0,-1,0,0),
      'B':(1,0,-2,-1),'q':(0,0,1,1),
      'G':(-1,3,-2,0),'hbar':(1,2,-1,0),
      'c':(0,1,-1,0),'force':(1,1,-2,0),
      'energy':(1,2,-2,0),'Pphi':(1,2,-1,0),
      'flux':(1,2,-2,-1),'current':(0,0,0,1)
    }
    def add(*args):return tuple(sum(v[i] for v in args) for i in range(4))
    def neg(vec):return tuple(-x for x in vec)
    def minus(vec1,vec2):return add(vec1,neg(vec2))
    checks['SI_magnetic_lorentz_force']=add(units['q'],units['v'],units['B'])==units['force']
    checks['SI_centripetal_mass_v2_kappa']=add(units['m'],units['v'],units['v'],units['curvature'])==units['force']
    checks['SI_momentum_unit']=add(units['m'],units['v'],units['r'])==units['Pphi']
    checks['SI_charge_flux_angular_momentum']=add(units['q'],units['flux'])==units['Pphi']
    checks['SI_magnetic_energy_density']=add(units['B'],units['B'],neg((1,1,-2,-2)))==(1,-1,-2,0) # B²/mu0 = J/m³
    checks['SI_angular_rate_v_over_r']=minus(units['v'],units['r'])==units['omega']
    checks['SI_curvature_rate_kappa_v']=add(units['curvature'],units['v'])==units['omega']
    checks['SI_B_required_gamma_m_v_over_q_r']=minus(add(units['m'],units['v']),add(units['q'],units['r']))==units['B']
    checks['SI_period_length_over_speed']=minus(units['r'],units['v'])==units['time']
    checks['SI_magnetic_gyro_frequency_qB_over_m']=minus(add(units['q'],units['B']),units['m'])==units['omega']
    checks['SI_grav_c3_over_hbar_kappa2']=minus(add(units['c'],units['c'],units['c']),add(units['hbar'],units['curvature'],units['curvature']))==units['G']
    checks['SI_wrong_force_equals_curvature_rejected']=units['force']!=units['curvature']
    checks['SI_wrong_angle_velocity_equals_linear_v_rejected']=units['omega']!=units['v']
    # algebra for 3-4-5 resonance
    checks['weak_focus_pythagoras']=simplify((Rational(4,5))**2+(Rational(3,5))**2-1)==0
    checks['linear_n_9_25']=simplify((Rational(3,5))**2-Rational(9,25))==0
    # avoid falsely claiming exact numerical equilibrium stable, or new force
    if not all(checks.values()):
        raise AssertionError('Symbolic audit failed: '+str({k:v for k,v in checks.items() if not v}))
    out={'status':'PASS','count':len(checks),'tests':checks,
       'scope':'algebra and SI consistency, not a field unification or exact orbit proof'}
    (ROOT/'results'/'SYMBOLIC_SI_AUDIT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f"PASS: {len(checks)} symbolic / SI checks")

if __name__=='__main__':main()
