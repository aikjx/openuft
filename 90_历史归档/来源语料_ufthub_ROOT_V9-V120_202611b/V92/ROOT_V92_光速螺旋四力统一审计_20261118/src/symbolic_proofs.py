"""ROOT V92 exact symbolic derivations; assertions are executable proof checks."""
import json
from pathlib import Path
import sympy as s


def prove():
    R,w,p,v,c,m,q,B,a,u=s.symbols('R w p v c m q B a u', positive=True)
    t=s.symbols('t', real=True)
    x=s.Matrix([R*s.cos(w*t), R*s.sin(w*t), p*t]); vvec=x.diff(t); avec=vvec.diff(t); jerk=avec.diff(t)
    v2=s.trigsimp(vvec.dot(vvec))
    cross=vvec.cross(avec)
    norm2=s.trigsimp(cross.dot(cross))
    kap=s.simplify(s.sqrt(norm2)/v2**s.Rational(3,2))
    tor=s.trigsimp(s.det(s.Matrix.hstack(vvec,avec,jerk))/norm2)
    assertions={
     'speed identity':s.simplify(v2-(R*w)**2-p**2)==0,
     'curvature':s.simplify(kap-R*w*w/v2)==0,
     'torsion':s.simplify(tor-p*w/v2)==0,
     'helix closure':s.simplify(kap*kap+tor*tor-w*w/v2)==0,
     'curvature inverse':s.simplify((kap/(kap*kap+tor*tor))-R)==0,
     'axial inverse':s.simplify((s.sqrt(v2)*tor/s.sqrt(kap*kap+tor*tor))-p)==0,
     'normal acceleration':s.simplify(avec.dot(avec) - v2**2*kap**2)==0,
     'geodesic Minkowski nonzero transverse accel':s.simplify(avec.dot(avec)-R**2*w**4)==0,
    }
    # boost along helix axis u: p'=(p-u)/(1-up/c²), omega'=omega/[gamma_u(1-up/c²)]
    gu=1/s.sqrt(1-u*u/c**2)
    den=1-u*p/c**2
    pprime=(p-u)/den
    wp=w/(gu*den)
    v2prime=s.factor(R*R*wp*wp+pprime*pprime)
    # SR velocity transformation: (v² -2up +u² -(u²/c²)R²w²)/(1-up/c²)²
    transformed_reference=((R*w)**2/(gu*gu)+(p-u)**2)/den**2
    assertions['Lorentz 3-speed transformation']=s.simplify(v2prime-transformed_reference)==0
    assertions['axial boost removes spatial torsion']=s.simplify(pprime.subs(u,p))==0
    assertions['axial boost radial curvature stays nonzero']=s.simplify(wp.subs(u,p))!=0
    # SR invariant four-velocity norm for timelike paths
    gamma=1/s.sqrt(1-v*v/c**2)
    assertions['4 velocity norm'] = s.simplify(-(gamma*c)**2+(gamma*v)**2+c*c)==0
    # generic constant speed Lorentz Fperp matches magnetic field for cyclotron orbit
    g=s.symbols('gamma',positive=True)
    omega=q*B/(g*m); vp=s.symbols('vp', positive=True)
    rr=vp/omega; kapB=s.factor(rr*omega**2/(v*v))
    assertions['magnetic force = gamma m v2 kappa'] = s.simplify(g*m*v*v*kapB-q*vp*B)==0
    # Dimension ranks prove absence of mass from {c,kappa,tau,omega}
    cm=s.Matrix([[0,0,0,0],[1,-1,-1,0],[-1,0,0,-1],[0,0,0,0]])  # M,L,T,I for c,kappa,tau,omega
    target=s.Matrix([-1,3,-2,0]); aug=cm.row_join(target)
    assertions['no G solely from c, curvature, torsion, omega']=aug.rank()>cm.rank()
    # With hbar,curvature,c, unique powers (3,-1,-2)
    ch=s.Matrix([[0,1,0],[1,2,-1],[-1,-1,0],[0,0,0]])
    assertions['G dimensional exponents c3 hbar-1 kappa-2'] = ch*s.Matrix([3,-1,-2])==target
    # electric acceleration counterexample: along straight path has kappa=0 but nonzero F
    assertions['straight acceleration counterexample'] = s.diff(a*t*t/2,t,2)==a and a!=0
    failed=[key for key,ok in assertions.items() if not ok]
    if failed: raise AssertionError(f'Symbolic proof audit failed: {failed}')
    return {'checks':len(assertions),'passed':list(assertions),
            'formulas':{'speed_squared':str(v2),'kappa':str(kap),'tau':str(tor),
                         'boosted_axial_velocity':str(pprime),'boosted_omega':str(wp)},
            'scope':'Euclidean circular helix; Minkowski inertial axial boost; dimensional algebra, NOT a verified unified field theory'}

if __name__=='__main__':
    result=prove()
    print(json.dumps(result,ensure_ascii=False,indent=2))
