import math,json,csv,pathlib
G=6.67430e-11;c=299792458.0;mu0=1.25663706212e-6;g=9.80665
root=pathlib.Path(__file__).resolve().parents[1]
def helix(R,omega,p):
    v2=(R*omega)**2+p*p
    k=R*omega**2/v2
    t=p*omega/v2
    return dict(speed=math.sqrt(v2),curvature=k,torsion=t,identity_residual=k*k+t*t-omega*omega/v2)
def artificial(radius,accel=g):
    mass=accel*radius**2/G
    return dict(radius_m=radius,target_accel_m_s2=accel,equivalent_point_mass_kg=mass,rest_energy_J=mass*c*c,rotation_rpm=60/(2*math.pi)*math.sqrt(accel/radius),rotation_edge_speed_m_s=math.sqrt(accel*radius))
def magnetic(B,radius):
    volume=4*math.pi*radius**3/3
    energy=B*B/(2*mu0)*volume
    mass=energy/c**2
    return dict(B_T=B,radius_m=radius,ideal_uniform_field_energy_J=energy,energy_mass_kg=mass,point_mass_equivalent_surface_g_m_s2=G*mass/radius**2)
def tidal(mass,radius,separation):return 2*G*mass*separation/radius**3
if __name__=='__main__':
    d={'constants':{'G_SI':G,'c_SI':c,'mu0_SI':mu0},'artificial_gravity':[artificial(r) for r in (1,10,100,1000)],'magnetic_energy':[magnetic(B,1) for B in (1,10,100)],'helix_examples':[helix(2,w,math.sqrt(1-(2*w)**2)) for w in (.1,.2,.4)],'notes':'Magnetic equivalent is an order-of-magnitude energy-only estimate, not a GR solution. Point-mass formula is not applicable inside distributed sources.'}
    (root/'data'/'results.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    for x in d['artificial_gravity']:print(x)
    for x in d['magnetic_energy']:print(x)
