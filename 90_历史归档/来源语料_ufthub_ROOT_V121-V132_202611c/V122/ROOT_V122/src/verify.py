import math,json
from pathlib import Path
G=6.67430e-11;c=299792458.;mu0=4*math.pi*1e-7;g=9.80665
# c=1 in theoretical derivations; SI restored in engineering examples
rows=[]
for R in [1,10,100,1000]:
 rows.append({'radius_m':R,'rotation_rpm':60/(2*math.pi)*math.sqrt(g/R),'mass_for_1g_kg':g*R*R/G,'energy_equivalent_J':g*R*R/G*c*c})
helices=[]
for R,p in [(1.,0.),(2.,0.3),(10.,0.8),(0.25,-0.6)]:
 w=math.sqrt(1-p*p)/R;k=R*w*w;t=p*w
 helices.append({'R':R,'p':p,'omega':w,'kappa':k,'tau':t,'residual':k*k+t*t-w*w,'R_recovered':k/(k*k+t*t)})
# dimensional estimate of magnetic energy; not full GR source solution
B=10.;r=1.;U=B*B/(2*mu0)*4*math.pi*r**3/3
# closed loop connection: spectrum n*2pi/L + a, only holonomy aL modulo 2pi is physical
L=2*math.pi;a=.37
spectrum=[{'n':n,'lambda':2*math.pi*n/L+a} for n in range(-3,4)]
# standard scalar-tensor fifth force phenomenology: Yukawa ratio alpha (1+r/lambda)exp(-r/lambda)
yukawa=[]
for alpha in [1e-2,1e-4]:
 for lam in [1.,100.,10000.]:
  for r0 in [1.,10.,100.]:
   yukawa.append({'alpha':alpha,'lambda_m':lam,'r_m':r0,'delta_g_over_g':alpha*(1+r0/lam)*math.exp(-r0/lam)})
res={'constants':{'G_SI':G,'c_SI':c,'g_SI':g},'engineering':rows,'helices':helices,'magnetic':{'B_T':B,'sphere_radius_m':r,'energy_J':U,'energy_mass_kg':U/c**2,'point_mass_acceleration_at_1m_m_s2':G*U/c**2},'spectrum':spectrum,'yukawa_illustrative':yukawa}
Path(__file__).resolve().parents[1].joinpath('results','calculations.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print('max helix residual:',max(abs(x['residual']) for x in helices));print('magnetic energy:',U);print('rotation 100m rpm:',rows[2]['rotation_rpm'])
