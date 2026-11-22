import csv,json,math
from pathlib import Path
from model import fields,norm,forces
out=Path(__file__).resolve().parent
rows=[]
for alt in [0,100000,400000,1000000]:
 for lat in range(-90,91,15):
  for lon in range(-180,180,30):
   f=fields(lat,lon,alt)
   rows.append({'lat_deg':lat,'lon_deg':lon,'alt_m':alt,'gravity_m_s2':norm(f['gravity_m_s2']),'magnetic_uT':norm(f['magnetic_T'])*1e6,'gx':f['gravity_m_s2'][0],'gy':f['gravity_m_s2'][1],'gz':f['gravity_m_s2'][2],'bx_T':f['magnetic_T'][0],'by_T':f['magnetic_T'][1],'bz_T':f['magnetic_T'][2]})
with (out/'earth_field_grid.csv').open('w',newline='') as fp:
 w=csv.DictWriter(fp,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
examples={name:{'g_m_s2':norm(fields(lat,lon,alt)['gravity_m_s2']),'B_uT':norm(fields(lat,lon,alt)['magnetic_T'])*1e6} for name,lat,lon,alt in [('equator',0,0,0),('pole',90,0,0),('midlatitude',45,120,0),('ISS_altitude',0,0,400000)]}
(out/'verified_samples.json').write_text(json.dumps(examples,indent=2),encoding='utf8')
print('Generated',len(rows),'grid points');print(json.dumps(examples,indent=2))
