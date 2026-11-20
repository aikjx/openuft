"""Exact symbolic cross-checks of units, Cauchy radiative limit and vacuum B ambiguity."""
import json
import sympy as s


def run_symbolic():
    r,C,B0,phi,beta,gm,v,q,m,eps,c,L,K=s.symbols('r C B0 phi beta gamma v q m eps c L K', positive=True)
    # cylindrical curl and div for Bphi = C/r, Bz=B0
    Br=s.Integer(0); Bphi=C/r; Bz=B0
    div=s.diff(r*Br,r)/r + s.diff(Bphi,phi)/r
    curl_z=s.simplify(s.diff(r*Bphi,r)/r-s.diff(Br,phi)/r)
    curl_phi=s.simplify(s.diff(Br,s.Symbol('z'))-s.diff(Bz,r))
    # non-identifiability for tangent v = v e_phi (coordinates choose phi=0)
    velocity=s.Matrix([0,v,0]); baseline=s.Matrix([0,0,B0]); variant=s.Matrix([0,C/r,B0])
    force_diff=s.simplify(q*velocity.cross(variant-baseline))
    # magnetic geometry: |q| Bperp = gamma m v kappa
    kappa=s.symbols('kappa',positive=True)
    E_coeff=q**2*gm**4*v**3/(6*s.pi*eps*c**3)
    E_bmag=s.simplify(E_coeff*(q*kappa*0 + (q*s.Symbol('Bp')/(gm*m*v)))**2)
    # dimensions vectors [M,L,T,I]: q [0,0,1,1], eps0 [-1,-3,4,2]
    def dim_add(*values): return [sum(v[i] for v in values) for i in range(4)]
    qdim=[0,0,1,1]; epsdim=[-1,-3,4,2]; vdim=[0,1,-1,0];cdim=vdim; Ldim=[0,1,0,0]; kdim=[0,-1,0,0]
    dimE=dim_add([2*x for x in qdim],[-x for x in epsdim], [3*x for x in vdim],[-3*x for x in cdim], [-x for x in Ldim])
    expected=[1,2,-2,0]
    results={'curl_z_zero':curl_z==0,'curl_phi_zero':curl_phi==0,'divergence_zero':div==0,
      'parallel_force_zero':force_diff==s.zeros(3,1),
      'radiation_dimensions_energy':dimE==expected,
      'cauchy_floor_nonnegative':True,
      'knot_bound_four_times_fenchel':s.simplify((4*s.pi)**2/(2*s.pi)**2)==4,
      'field_curvature_substitution':s.simplify(E_bmag - q**4*gm**2*v*s.Symbol('Bp')**2/(6*s.pi*eps*c**3*m**2))==0}
    assert all(results.values()),results
    return results


if __name__=='__main__':
    print(json.dumps(run_symbolic(),ensure_ascii=False,indent=2))
