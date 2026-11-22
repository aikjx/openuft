"""ROOT V56: SI units, ECEF Cartesian coordinates, educational Earth field model."""
import math
G=6.67430e-11; M=5.9722e24; MU=G*M; R=6371000.; OMEGA=7.2921150e-5; J2=1.08262668e-3
MU0=4*math.pi*1e-7; B_EQ=3.12e-5

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(s,a):return tuple(s*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return math.sqrt(dot(a,a))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def ecef(lat_deg,lon_deg,alt_m=0):
    lat=math.radians(lat_deg);lon=math.radians(lon_deg);r=R+alt_m
    return (r*math.cos(lat)*math.cos(lon),r*math.cos(lat)*math.sin(lon),r*math.sin(lat))
def gravity(p,j2=True):
    x,y,z=p;r=norm(p)
    if r<R*0.1:raise ValueError('Model applies outside central region; not an interior-Earth model')
    k=-MU/r**3
    if not j2:return (k*x,k*y,k*z)
    f=1.5*J2*(R/r)**2;u=5*(z/r)**2
    return (k*x*(1-f*(u-1)),k*y*(1-f*(u-1)),k*z*(1-f*(u-3)))
def magnetic(p):
    r=norm(p)
    if r<R*0.1:raise ValueError('Outside-Earth dipole approximation only')
    n=mul(1/r,p);mhat=(0.,0.,1.)
    return mul(B_EQ*(R/r)**3,add(mul(3*dot(mhat,n),n),mul(-1,mhat)))
def electric(p,E0=0):
    # Controlled synthetic radial test field, not measured global atmospheric E field.
    return mul(E0*R**2/norm(p)**3,p)
def centrifugal(p):return (OMEGA**2*p[0],OMEGA**2*p[1],0.)
def fields(lat,lon,alt=0,E0=0):
    p=ecef(lat,lon,alt);g=gravity(p);b=magnetic(p);e=electric(p,E0)
    return {'position_m':p,'gravity_m_s2':g,'magnetic_T':b,'electric_V_m':e,'effective_g_m_s2':add(g,centrifugal(p))}
def forces(lat,lon,alt,m,q,v,E0=0):
    f=fields(lat,lon,alt,E0);fg=mul(m,f['gravity_m_s2']);fe=mul(q,f['electric_V_m']);fb=mul(q,cross(v,f['magnetic_T']))
    return {'gravity_N':fg,'electric_N':fe,'magnetic_N':fb,'total_N':add(add(fg,fe),fb),'fields':f}
