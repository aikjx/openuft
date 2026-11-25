"""ROOT V132: reproducible Earth gravity and phenomenological Yukawa checks. SI computational units; c=1 only in symbolic field theory."""
import math
MU=3.986004418e14
G=6.67430e-11
RE=6378137.0
RP=6356752.314245
OMEGA=7.292115e-5
J2=1.08262668e-3
LAMBDA=124600.0
ALPHA=1/3

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm(v): return math.sqrt(dot(v,v))
def central(pos):
 r=norm(pos)
 if r==0: raise ValueError('central field undefined at origin')
 return tuple(-MU*x/r**3 for x in pos)
def j2(pos):
 x,y,z=pos; r=norm(pos)
 if r==0: raise ValueError('undefined')
 q=5*z*z/(r*r); k=1.5*J2*MU*RE**2/r**5
 return (-k*x*(1-q),-k*y*(1-q),-k*z*(3-q))
def gravity(pos): return tuple(a+b for a,b in zip(central(pos),j2(pos)))
def effective(pos):
 a=gravity(pos); x,y,z=pos
 return (a[0]+OMEGA**2*x,a[1]+OMEGA**2*y,a[2])
def potential(pos):
 x,y,z=pos; r=norm(pos)
 return -MU/r*(1-J2*(RE/r)**2*0.5*(3*(z/r)**2-1))
def finite_diff_grad(pos,h=1.0):
 out=[]
 for i in range(3):
  p=list(pos);m=list(pos);p[i]+=h;m[i]-=h
  out.append(-(potential(p)-potential(m))/(2*h))
 return tuple(out)
def layers():
 # Illustrative 5-layer piecewise-constant model; NOT PREM and NOT fitted to measurements.
 return [(0,1221500,13000),(1221500,3480000,11000),(3480000,5701000,5000),(5701000,6346600,3800),(6346600,6371000,2800)]
def mass_layers(lay):
 return sum(4*math.pi/3*rho*(b**3-a**3) for a,b,rho in lay)
def yukawa_ratio_exterior(r,lam=LAMBDA,alpha=ALPHA,lay=None,n=3000):
 """Exact spherical-shell angular integral, radial Simpson integration; r>=outer radius.
    ratio is extra acceleration / Newtonian acceleration for the SAME density model.
 """
 if lam<=0 or r<=0: raise ValueError('positive r and lambda required')
 lay=layers() if lay is None else lay
 if r < max(b for a,b,rho in lay): raise ValueError('exterior only')
 if n%2: raise ValueError('Simpson n must be even')
 total=0.; mass=mass_layers(lay)
 for a,b,rho in lay:
  step=(b-a)/n; subtotal=0.
  for i in range(n+1):
   s=a+i*step
   # s²*sinh(s/lambda)/(s/lambda)*exp(-r/lambda) in stable form
   term=0.5*lam*s*(math.exp(-(r-s)/lam)-math.exp(-(r+s)/lam))
   subtotal+=(1 if i in (0,n) else 4 if i%2 else 2)*term
  total+=4*math.pi*rho*step*subtotal/3
 return alpha*(total/mass)*(1+r/lam)
def yukawa_point_ratio(r,lam=LAMBDA,alpha=ALPHA):
 return alpha*(1+r/lam)*math.exp(-r/lam)
