import math,csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
MU=3.986004418e14; RE=6378137.; RM=6371000.; J2=1.08263e-3; W=7.292115e-5
LAM=124600.; EPS=.005954

def accel(x,y,z,j2=True,rotation=False):
 r=math.sqrt(x*x+y*y+z*z); assert r>0
 f=-MU/r**3
 if j2:
  t=1.5*J2*(RE/r)**2; q=5*z*z/r**2
  ax=f*x*(1-t*(q-1)); ay=f*y*(1-t*(q-1)); az=f*z*(1-t*(q-3))
 else: ax,ay,az=f*x,f*y,f*z
 if rotation: ax+=W*W*x;ay+=W*W*y
 return (ax,ay,az)
def norm(a):return math.sqrt(sum(v*v for v in a))
def root_phenomenology(h):
 # Only a local effective exponential acceleration residual, NOT a density-convolved Yukawa field.
 return EPS*MU/RM**2*math.exp(-h/LAM)
def main():
 rows=[]
 for h in [0,100000,200000,400000,800000,2000000,10000000]:
  r=RM+h
  rows.append(dict(height_km=h/1000,central_g=MU/r**2,root_local_residual=root_phenomenology(h),root_ratio=root_phenomenology(h)/(MU/r**2)))
 with (P/'altitude.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 places=[]
 for name,x,y,z in [('equator',RE,0,0),('north_pole',0,0,6356752.3142),('mid_latitude',4500000,0,4500000)]:
  a=accel(x,y,z); eff=accel(x,y,z,rotation=True)
  places.append(dict(name=name,gravity_vector=a,gravity_magnitude=norm(a),rotating_effective_vector=eff,rotating_effective_magnitude=norm(eff)))
 (P/'locations.json').write_text(json.dumps(places,indent=2))
 # independent finite-difference potential derivative at equator for J2 model
 def pot(x,y,z):
  r=math.sqrt(x*x+y*y+z*z); p2=.5*(3*z*z/r**2-1)
  return -MU/r*(1-J2*(RE/r)**2*p2)
 h=10.
 numerical=-(pot(RE+h,0,0)-pot(RE-h,0,0))/(2*h)
 assert abs(numerical-accel(RE,0,0)[0])<1e-8
 assert abs(norm(accel(RE,0,0,j2=False))-MU/RE**2)<1e-12
 assert abs(accel(RE,0,0)[1])<1e-14
 assert abs(accel(0,0,6356752.3142)[0])<1e-14
 assert norm(accel(RE,0,0,rotation=True))<norm(accel(RE,0,0))
 assert all(rows[i]['central_g']>rows[i+1]['central_g'] for i in range(len(rows)-1))
 assert abs(root_phenomenology(0)/(MU/RM**2)-EPS)<1e-14
 print('PASS: 7 numerical tests; altitude points:',len(rows))
 for row in rows:print(row)
 for p in places:print(p)
if __name__=='__main__':main()
