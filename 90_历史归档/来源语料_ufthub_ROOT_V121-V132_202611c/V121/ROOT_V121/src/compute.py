import math,json
from pathlib import Path
G=6.67430e-11;c=299792458.;mu0=4*math.pi*1e-7;g=9.80665

def helix(R,p):
    assert R>0 and abs(p)<1
    w=math.sqrt(1-p*p)/R
    k=R*w*w;t=p*w
    return {'R':R,'p':p,'omega':w,'kappa':k,'tau':t,'identity_residual':k*k+t*t-w*w}
def spectral(L,a,n):return 2*math.pi*n/L+a
def gravity_mass(r):return g*r*r/G
def rotation_rpm(r):return 60/(2*math.pi)*math.sqrt(g/r)
def magnetic(B,r):
    E=B*B/(2*mu0)*4*math.pi*r**3/3
    return {'stored_J':E,'mass_equiv_kg':E/c**2,'point_mass_proxy_accel_m_s2':G*E/c**2/r**2}
def run():
    data={'helix':[helix(1.,p) for p in [0,.3,.6,.9]],'circle_spectrum':{'L':2*math.pi,'a':.2,'eigenvalues':[spectral(2*math.pi,.2,n) for n in range(-4,5)]},'gravity_mass':[{'r_m':r,'required_kg':gravity_mass(r),'equivalent_J':gravity_mass(r)*c*c} for r in [1,10,100]],'rotation':[{'r_m':r,'rpm':rotation_rpm(r)} for r in [1,10,100,1000]],'magnetic_10T_1m':magnetic(10,1),'theory_status':'No derivation of unique F(chi), V(chi), standard model, or new gravity demonstrated.'}
    Path(__file__).resolve().parents[1].joinpath('data/results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print(json.dumps(data,indent=2))
if __name__=='__main__':run()
