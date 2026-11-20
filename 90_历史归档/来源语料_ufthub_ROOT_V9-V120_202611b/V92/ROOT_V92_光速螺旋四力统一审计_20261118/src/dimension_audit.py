"""All pairwise SI dimensional collisions and hypothesis equation dimensional vetting."""
import csv,json
from itertools import combinations
from pathlib import Path
from src.helix_physics import dimension_dict,dimension_dict as Dfunc,dimensional_product as prod,dimensional_power as power
ROOT=Path(__file__).resolve().parents[1]

def build():
 D=dimension_dict()
 D['Z=Gc/2']=prod(D['G'],D['speed v, c, p'])
 D['Zprime=c/(8pi epsilon0)']=prod(D['speed v, c, p'],power(D['permittivity epsilon0'],-1))
 D['hbar omega']=prod(D['angular momentum J / hbar'],D['angular frequency omega'])
 D['hbar c kappa']=prod(D['angular momentum J / hbar'],D['speed v, c, p'],D['curvature kappa'])
 D['c B field']=prod(D['speed v, c, p'],D['magnetic field Bfield'])
 D['R kappa']=prod(D['length R'],D['curvature kappa'])
 D['kappa squared']=power(D['curvature kappa'],2)
 with (ROOT/'results'/'DIMENSION_CROSS_ALL_PAIRS.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['A','B','unit_dimension_A_MLTI','unit_dimension_B_MLTI','same_SI_dimensions','interpretation'])
  for (n1,d1),(n2,d2) in combinations(D.items(),2):
   w.writerow([n1,n2,str(d1),str(d2),int(d1==d2), 'dimension match does NOT prove physical equality' if d1==d2 else 'cannot directly add/equate without a compensating factor'])
 vec=[{'quantity':k,'M':v[0],'L':v[1],'T':v[2],'I':v[3]} for k,v in D.items()]
 with (ROOT/'results'/'DIMENSION_VECTOR_CATALOG.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=['quantity','M','L','T','I']);w.writeheader();w.writerows(vec)
 formulas=[
 ('v=R*omega',D['speed v, c, p'],prod(D['length R'],D['angular frequency omega']),'KINEMATIC_IDENTITY'),
 ('omega=v*sqrt(kappa²+tau²)',D['angular frequency omega'],prod(D['speed v, c, p'],D['curvature kappa']),'HELIX_ONLY'),
 ('force=m*v²*kappa',D['force F'],prod(D['mass m'],power(D['speed v, c, p'],2),D['curvature kappa']),'NEEDS_DYNAMICS_AND_GAMMA'),
 ('energy=hbar*omega',D['energy E'],prod(D['angular momentum J / hbar'],D['angular frequency omega']),'PHASE_FREQUENCY_ONLY'),
 ('energy=hbar*c*kappa',D['energy E'],prod(D['angular momentum J / hbar'],D['speed v, c, p'],D['curvature kappa']),'DIMENSION_ONLY'),
 ('G=c³/(hbar*kappa²)',D['G'],prod(power(D['speed v, c, p'],3),power(D['angular momentum J / hbar'],-1),power(D['curvature kappa'],-2)),'DIMENSION_ONLY_NEEDS_INDEPENDENT_KAPPA'),
 ('G=c/kappa',D['G'],prod(D['speed v, c, p'],power(D['curvature kappa'],-1)),'DIMENSION_FAIL'),
 ('force=m*omega*kappa',D['force F'],prod(D['mass m'],D['angular frequency omega'],D['curvature kappa']),'DIMENSION_FAIL'),
 ('omega=c*kappa*tau',D['angular frequency omega'],prod(D['speed v, c, p'],D['curvature kappa'],D['torsion tau']),'DIMENSION_FAIL'),
 ('kappa+tau',D['curvature kappa'],D['torsion tau'],'DIMENSION_PASS_NEEDS_DIRECTION_PARITY'),
 ('kappa+kappa²',D['curvature kappa'],D['kappa squared'],'DIMENSION_FAIL'),
 ('Z+i Zprime',D['Z=Gc/2'],D['Zprime=c/(8pi epsilon0)'],'DIMENSION_FAIL'),
 ('Efield+Bfield',D['electric field Efield'],D['magnetic field Bfield'],'DIMENSION_FAIL'),
 ('Efield+c*Bfield',D['electric field Efield'],D['c B field'],'DIMENSION_PASS_BUT_VECTOR_VS_PSEUDOVECTOR'),
 ('Riemann_scalar=kappa²',D['GR Riemann curvature'],D['kappa squared'],'DIMENSION_PASS_NOT_A_PHYSICAL_IDENTITY'),
 ('v_total²=(Romega)²+p²',power(D['speed v, c, p'],2),power(prod(D['length R'],D['angular frequency omega']),2),'KINEMATIC_IDENTITY'),
 ('v=omega/kappa',D['speed v, c, p'],prod(D['angular frequency omega'],power(D['curvature kappa'],-1)),'NOT_TRUE_FOR_NONZERO_TAU'),
 ('a=v²*kappa',D['acceleration a'],prod(power(D['speed v, c, p'],2),D['curvature kappa']),'TRANSVERSE_ACCEL_ONLY'),
 ('a=omega²*R',D['acceleration a'],prod(power(D['angular frequency omega'],2),D['length R']),'CIRCULAR_HELIX'),
 ('F=q*Efield',D['force F'],prod(D['charge q'],D['electric field Efield']),'LORENTZ_FORCE'),
 ('F=q*v*Bfield',D['force F'],prod(D['charge q'],D['speed v, c, p'],D['magnetic field Bfield']),'MAGNETIC_TRANSVERSE'),
 ('Einstein Gmunu=G*T/c4',D['Einstein tensor Gmunu'],prod(D['G'],D['stress-energy tensor (SI)'],power(D['speed v, c, p'],-4)),'GR_BASELINE'),
 ]
 with (ROOT/'results'/'CANDIDATE_EQUATION_DIMENSION_AUDIT.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['candidate_formula','lhs_MLTI','rhs_MLTI','dimensionally_possible','scientific_interpretation'])
  for n,a,b,note in formulas:w.writerow([n,str(a),str(b),int(a==b),note])
 return {'base_catalog':len(dimension_dict()),'augmented_dimension_vectors':len(D),'pairwise_collisions':len(D)*(len(D)-1)//2,'candidate_equations':len(formulas),'dimension_failures':sum(a!=b for _,a,b,_ in formulas),
         'Z_dimension':D['Z=Gc/2'],'Zprime_dimension':D['Zprime=c/(8pi epsilon0)'],
         'warning':'same dimensions are necessary but not sufficient for a physical identity'}

if __name__=='__main__':print(json.dumps(build(),ensure_ascii=False,indent=2))
