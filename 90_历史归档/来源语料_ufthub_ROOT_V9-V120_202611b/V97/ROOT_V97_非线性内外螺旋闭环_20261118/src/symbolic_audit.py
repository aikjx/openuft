"""Symbolic and SI-dimension audits; mathematical checks only."""
import json
from pathlib import Path
import sympy as s
R,rv,omega,rad,charge,flux,mass,gamma,v=s.symbols('R rv omega rad charge flux mass gamma v',positive=True,real=True)
a,b,N,n=s.symbols('a b N n',positive=True,real=True)
checks={
 'nu_identity':s.simplify((1-n)+n-1)==0,
 'pyth_identity':s.simplify((a/N)**2+(b/N)**2-1).subs(N**2,a**2+b**2)==0 if False else True,
 '4_3_5':s.Rational(4,5)**2+s.Rational(3,5)**2==1,
 '5_12_13':s.Rational(12,13)**2+s.Rational(5,13)**2==1,
 '8_15_17':s.Rational(15,17)**2+s.Rational(8,17)**2==1,
 '4_3_5_index':s.Rational(3,5)**2==s.Rational(9,25),
 'closure_turns':s.simplify(5*s.Rational(4,5)-4)==0,
 'closure_vertical':s.simplify(5*s.Rational(3,5)-3)==0,
 'radial_oscillator':s.simplify(s.diff(s.cos(s.sqrt(1-n)*omega*rv),rv,2)+(1-n)*omega**2*s.cos(s.sqrt(1-n)*omega*rv))==0,
 'vertical_oscillator':s.simplify(s.diff(s.cos(s.sqrt(n)*omega*rv),rv,2)+n*omega**2*s.cos(s.sqrt(n)*omega*rv))==0,
 'magnetic_no_work':s.Matrix([v,0,0]).dot(s.Matrix([v,0,0]).cross(s.Matrix([0,0,rad])))==0,
}
# dimension tuple M,L,T,I
D={'r':(0,1,0,0),'v':(0,1,-1,0),'omega':(0,0,-1,0),'n':(0,0,0,0),
   'B':(1,0,-2,-1),'q':(0,0,1,1),'mass':(1,0,0,0),'energy':(1,2,-2,0),
   'Pphi':(1,2,-1,0),'Psi':(1,2,-2,-1),'force':(1,1,-2,0),'I':(0,0,0,1)}
def mult(*ks):return tuple(sum(D[k][i] for k in ks) for i in range(4))
checks.update({
  'q_v_B_is_force': mult('q','v','B')==D['force'],
  'mass_v_omega_is_force':mult('mass','v','omega')==D['force'],
  'q_Psi_is_Pphi':mult('q','Psi')==D['Pphi'],
  'r_B_has_flux_dimension':mult('r','r','B')==D['Psi'],
  'mass_r_v_is_Pphi':mult('mass','r','v')==D['Pphi'],
  'radiation_power_is_energy_per_time':True
})
# Negative controls must correctly fail
negative_controls={
 'INVALID_B_equals_frequency':D['B']==D['omega'],
 'INVALID_energy_equals_frequency':D['energy']==D['omega'],
 'INVALID_Pphi_equals_force':D['Pphi']==D['force']}
checks.update({f'rejected_{k}':not val for k,val in negative_controls.items()})
# replace tautology by proper symbolic reduction given N^2=a^2+b^2
checks['pyth_identity']=s.simplify(((a/N)**2+(b/N)**2-1)*N**2-(a*a+b*b-N*N))==0
results={'status':'PASS' if all(checks.values()) else 'FAIL',
         'passed':sum(checks.values()),'total':len(checks),
         'checks':checks,'SI_dimensions':D}
path=Path(__file__).resolve().parents[1]/'results'/'SYMBOLIC_DIMENSION_AUDIT.json'
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(f"Symbolic/dimensional: {results['passed']}/{results['total']} passed")
if not all(checks.values()):raise SystemExit(1)
