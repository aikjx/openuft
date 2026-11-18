"""Supplemental SymPy algebra. Import optional; exit if unavailable.
Each assertion is an identity/units verification, not a physics discovery.
"""
import json
from pathlib import Path
import sympy as s
BASE=Path(__file__).resolve().parents[1]
G,c,hbar,m,r,R,omega,u,lam,delta=s.symbols('G c hbar m r R omega u lam delta',positive=True)
checks={}

def check(name, expr):
    ok=bool(s.simplify(expr)==0)
    if not ok: raise AssertionError(name+' : '+str(s.simplify(expr)))
    checks[name]=True

# algebraic identity and dimensions
check('Z_inverse', (2*(G*c/2)/c)-G)
check('gravitational_radius_inverse', (c*c*(G*m/c**2)/m)-G)
check('planck_length_inverse', (c**3*((hbar*G/c**3)) / hbar)-G)
check('planck_mass_inverse', (hbar*c/(hbar*c/G))-G)
check('alpha_from_radius_ratio', (G*m/c**2)/(hbar/(m*c))-G*m*m/(hbar*c))
check('planck_crossing_solution', s.sqrt(hbar*c/G)**2 - hbar*c/G)
check('velocity_helix_c', (c*s.cos(lam))**2 + (c*s.sin(lam))**2 - c**2)
check('helix_accel_from_c', R*(c*s.cos(lam)/R)**2 - c**2*s.cos(lam)**2/R)
check('Einstein_coupling_relation_Z', 8*s.pi*G/c**4 - 16*s.pi*(G*c/2)/c**5)
# Rank test that c/hbar cannot span dimension of G
A=s.Matrix([[1,2],[0,1],[-1,-1]])
b=s.Matrix([3,-1,-2])
checks['dimensional_no_go_rank']=bool(A.rank()==2 and A.row_join(b).rank()==3)
if not checks['dimensional_no_go_rank']: raise AssertionError('dimensional basis unexpectedly spans G')
# Mass-radius degeneracy: G -> delta G; M -> M/delta, GM invariant
check('GM_parameter_degeneracy', (delta*G)*(m/delta)-G*m)
# Planck crossing occurs only at m=mP, positive m
check('planck_radius_compton_at_mP', (G*(s.sqrt(hbar*c/G))/c**2)-(hbar/(s.sqrt(hbar*c/G)*c)))
# exact symbolic logarithmic exponents for conditional models
x=s.symbols('x',positive=True)
check('fixed_Z_log_derivative', x*s.diff(x**-1,x)/(x**-1)+1)
check('fixed_radius_log_derivative', x*s.diff(x**2,x)/(x**2)-2)
check('fixed_length_log_derivative', x*s.diff(x**3,x)/(x**3)-3)
(BASE/'results/symbolic_verification.json').write_text(json.dumps({'checks':checks,'count':len(checks),'status':'PASSED'},indent=2),encoding='utf-8')
print(f'SymPy independent identities: {len(checks)} PASSED')
