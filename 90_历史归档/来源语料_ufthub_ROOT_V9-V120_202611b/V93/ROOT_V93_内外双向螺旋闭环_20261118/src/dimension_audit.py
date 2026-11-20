"""Dimensional analysis in base SI [M,L,T,I], including electromagnetic charge."""
import csv,itertools
from pathlib import Path
M,L,T,I=range(4)
D={
'mass':(1,0,0,0), 'length':(0,1,0,0), 'time':(0,0,1,0),
'phase_u':(0,0,0,0), 'winding_m':(0,0,0,0),'winding_n':(0,0,0,0),
'R':(0,1,0,0),'a':(0,1,0,0),'rho':(0,1,0,0),'sigma_dr_du':(0,1,0,0),
'c':(0,1,-1,0),'physical_v':(0,1,-1,0),'beta':(0,0,0,0),
'omega':(0,0,-1,0),'frequency':(0,0,-1,0),'kappa':(0,-1,0,0),'torsion':(0,-1,0,0),
'acceleration':(0,1,-2,0),'force':(1,1,-2,0),'momentum':(1,1,-1,0),
'energy':(1,2,-2,0),'action_hbar':(1,2,-1,0),'G':(-1,3,-2,0),
'electric_charge':(0,0,1,1),'electric_current':(0,0,0,1),'B_magnetic':(1,0,-2,-1),
'electric_field':(1,1,-3,-1),'flux':(1,2,-2,-1),'vector_potential':(1,1,-2,-1),
'phase_AB':(0,0,0,0),'phase_angle':(0,0,0,0),'arc_length':(0,1,0,0),
'period':(0,0,1,0),'gamma':(0,0,0,0),'power':(1,2,-3,0),
'pressure':(1,-1,-2,0),'rho_mass_density':(1,-3,0,0),
'compton_length':(0,1,0,0), 'planck_length':(0,1,0,0), 'spin':(1,2,-1,0)
}
def add(*dims): return tuple(map(sum,zip(*dims)))
def neg(d): return tuple(-x for x in d)
def mul(d,n):return tuple(x*n for x in d)

def candidates():
    cases=[
        ('sigma²=(an)²+(m*rho)²',mul(D['sigma_dr_du'],2),mul(D['R'],2),'EXACT'),
        ('dt/du=sigma/c',D['time'],add(D['sigma_dr_du'],neg(D['c'])),'EXACT'),
        ('du/dt=c/sigma',D['frequency'],add(D['c'],neg(D['sigma_dr_du'])),'EXACT'),
        ('omega=m*c/sigma',D['omega'],add(D['c'],neg(D['sigma_dr_du'])),'EXACT'),
        ('v_r²+v_theta²+v_z²=v²',mul(D['c'],2),mul(D['physical_v'],2),'EXACT'),
        ('kappa=|rprime x rsecond|/sigma³',D['kappa'],add(mul(D['R'],2),mul(D['sigma_dr_du'],-3)),'EXACT'),
        ('tau=det/(crossnorm²)',D['torsion'],add(mul(D['R'],3),mul(D['R'],-4)),'EXACT'),
        ('normal_accel=v²*kappa',D['acceleration'],add(mul(D['physical_v'],2),D['kappa']),'EXACT'),
        ('force=gamma*m*v²*kappa',D['force'],add(D['mass'],mul(D['physical_v'],2),D['kappa']),'EXACT'),
        ('B_min=F/(q*v)',D['B_magnetic'],add(D['force'],neg(D['electric_charge']),neg(D['physical_v'])),'EXACT'),
        ('flux=B*area',D['flux'],add(D['B_magnetic'],mul(D['length'],2)),'EXACT'),
        ('phase_AB=q*flux/hbar',D['phase_AB'],add(D['electric_charge'],D['flux'],neg(D['action_hbar'])),'EXACT'),
        ('energy=m*c²',D['energy'],add(D['mass'],mul(D['c'],2)),'EXACT'),
        ('omega=c*kappa',D['omega'],add(D['c'],D['kappa']),'DIMENSION_ONLY'),
        ('G from c3/hbar/kappa2',D['G'],add(mul(D['c'],3),neg(D['action_hbar']),mul(D['kappa'],-2)),'DIMENSION_ONLY_NOT_DERIVATION'),
        ('G from c and kappa only',D['G'],add(D['c'],mul(D['kappa'],-1)),'INVALID'),
        ('force=omega*kappa',D['force'],add(D['omega'],D['kappa']),'INVALID'),
        ('energy=omega',D['energy'],D['omega'],'INVALID'),
        ('force=kappa*mass',D['force'],add(D['kappa'],D['mass']),'INVALID'),
        ('phase_AB=B*length',D['phase_AB'],add(D['B_magnetic'],D['length']),'INVALID'),
        ('torsion=omega',D['torsion'],D['omega'],'INVALID'),
        ('G=c³/curvature',D['G'],add(mul(D['c'],3),neg(D['kappa'])),'INVALID'),
        ('flux=I*time',D['flux'],add(D['electric_current'],D['time']),'INVALID'),
        ('pressure=F/area',D['pressure'],add(D['force'],mul(D['length'],-2)),'EXACT'),
        ('energy=force*length',D['energy'],add(D['force'],D['length']),'EXACT'),
        ('mass=energy/c²',D['mass'],add(D['energy'],mul(D['c'],-2)),'EXACT'),
        ('period=length/c',D['period'],add(D['length'],neg(D['c'])),'EXACT'),
        ('density=mass/volume',D['rho_mass_density'],add(D['mass'],mul(D['length'],-3)),'EXACT'),
        ('hbar=energy*time',D['action_hbar'],add(D['energy'],D['time']),'EXACT'),
        ('compton=hbar/(m*c)',D['compton_length'],add(D['action_hbar'],neg(D['mass']),neg(D['c'])),'EXACT'),
        ('planck length=sqrt(G*hbar/c³)',mul(D['planck_length'],2),add(D['G'],D['action_hbar'],mul(D['c'],-3)),'EXACT'),
        ('spin has angular momentum units',D['spin'],D['action_hbar'],'EXACT'),
    ]
    return [(name,left,right,left==right,status) for name,left,right,status in cases]

def generate(out):
    out=Path(out);out.mkdir(exist_ok=True,parents=True)
    with (out/'DIMENSION_BASE_SI.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['name','M','L','T','I']);w.writerows([[name,*vec] for name,vec in D.items()])
    with (out/'DIMENSION_PAIR_COLLISIONS.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['quantity_a','quantity_b','same_dimension']);w.writerows([[a,b,da==db] for (a,da),(b,db) in itertools.combinations(D.items(),2)])
    with (out/'EQUATION_DIMENSION_CHECK.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['candidate','lhs','rhs','dimension_match','interpretation']);w.writerows([[name,str(l),str(r),match,status] for name,l,r,match,status in candidates()])
    nbad=sum(not x[3] for x in candidates())
    return {'dimension_variables':len(D),'pairwise_comparisons':len(D)*(len(D)-1)//2,'candidate_equations':len(candidates()),'dimension_mismatches':nbad}

if __name__=='__main__': print(generate('results'))
