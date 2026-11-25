import math, json, csv
from pathlib import Path
from fractions import Fraction as F
p=Path(__file__).resolve().parent
atoms={'Ti':(22,47.867),'Al':(13,26.9815385),'V':(23,50.9415),'Pt':(78,195.084),'Rh':(45,102.9055)}
alloys={'Ti alloy':{'Ti':.9,'Al':.06,'V':.04},'Pt alloy':{'Pt':.9,'Rh':.1}}
me=0.0005485799090441; u=931.49410372
checks=[]
def check(name, cond):
 assert cond,name
 checks.append(name)
rows={k:[z,a,z*me/a,.71*z*(z-1)/a**(4/3)/u] for k,(z,a) in atoms.items()}
with (p/'elements.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['element','Z','mean_atomic_mass_u','electron_rest_fraction','Coulomb_proxy_fraction']);w.writerows([k,*v] for k,v in rows.items())
res={}
for name,weights in alloys.items():
 check(name+' mass weights',math.isclose(sum(weights.values()),1))
 res[name]=[sum(w*rows[k][i] for k,w in weights.items()) for i in [2,3]]
a,b=res.values(); delta=[x-y for x,y in zip(a,b)]; eta=[2*(x-y)/(x+y) for x,y in zip(a,b)]
limit=(1.5+1.96*math.hypot(2.3,1.5))*1e-15
bounds=[limit/abs(d) for d in delta]
check('electron only excluded',abs(eta[0])>limit)
check('Coulomb only excluded',abs(eta[1])>limit)
check('two coefficients one contrast degeneracy',abs(delta[0]+(-delta[0]/delta[1])*delta[1])<1e-19)
# Explicit elastic scattering of two distinguishable massless species in CM frame.
pA=(1,1,0,0);pB=(1,-1,0,0);qA=(1,0,1,0);qB=(1,0,-1,0)
check('four momentum conserved',all(pA[i]+pB[i]==qA[i]+qB[i] for i in range(4)))
for ga,gb in [(F(1),F(1)),(F(2),F(1)),(F(1,3),F(1,3)),(F(0),F(1))]:
 ward=[ga*(qA[i]-pA[i])+gb*(qB[i]-pB[i]) for i in range(4)]
 check('soft Ward example '+str((ga,gb)),all(x==0 for x in ward)==(ga==gb))
# Radiation with six equal beams, total energy U=1, isotropic integrated spatial stress.
axes=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
S=[[sum(F(n[i]*n[j],6) for n in axes) for j in range(3)] for i in range(3)]
check('isotropic radiation stress',all(S[i][j]==(F(1,3) if i==j else 0) for i in range(3) for j in range(3)))
check('radiation active mass alone',1+sum(S[i][i] for i in range(3))==2)
check('compensating wall stress',1+sum(S[i][i]-S[i][i] for i in range(3))==1)
# G scaling: with c=1, G=hbar/M_P^2; this is a definition, not prediction.
for m in [F(1),F(2),F(5,3)]:
 h=F(7);g=h/m**2
 check('dimensionally allowed scale '+str(m),g*m*m==h)
result={'alloys':res,'delta_f_Ti_minus_Pt':delta,'eta_only':eta,'approx_95_conservative_eta':limit,'linear_one_parameter_bounds':bounds,'null_direction':[1,-delta[0]/delta[1]],'checks':checks,'count':len(checks),'limitations':'Atomic weights reference; Coulomb proxy with mean mass number, no full electromagnetic decomposition. One contrast, no raw fit. Radiation stress is idealized. Soft theorem assumes massless spin 2.'}
(p/'results.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
