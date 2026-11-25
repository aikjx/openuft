import csv,json,pathlib,sys
from earth import *
base=pathlib.Path(__file__).resolve().parents[1]/'results';base.mkdir(exist_ok=True)
rows=[]
for h in [0,100,200,400,800,2000,10000]:
 r=6371000+h*1000
 ratio=yukawa_ratio_exterior(r,n=2000)
 g=MU/r**2
 rows.append(dict(height_km=h,central_g_m_s2=g,yukawa_ratio_illustrative=ratio,yukawa_extra_m_s2=g*ratio))
with (base/'altitudes.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
pts={}
for name,p in {'equator':(RE,0,0),'north_pole':(0,0,RP),'midlatitude':(RE*.70710678118,0,RE*.70710678118)}.items():
 pts[name]={'position_m':p,'gravity_vector_m_s2':gravity(p),'effective_vector_m_s2':effective(p),'gravity_magnitude':norm(gravity(p)),'effective_magnitude':norm(effective(p))}
(base/'locations.json').write_text(json.dumps(pts,indent=2),encoding='utf8')
(base/'model_metadata.json').write_text(json.dumps({'model':'illustrative five-layer density, not PREM','layer_mass_kg':mass_layers(layers()),'source':'user ROOT hypothesis alpha=1/3, lambda=124.6km','status':'not an observational validation','limitations':['No GOCE/GRACE raw data','No EGM2008 harmonics','No covariance','No orbit fit','No GR full solution']},indent=2),encoding='utf8')
for row in rows: print(row)
