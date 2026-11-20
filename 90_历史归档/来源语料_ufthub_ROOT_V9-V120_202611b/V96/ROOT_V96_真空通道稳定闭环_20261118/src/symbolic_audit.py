"""Symbolic physics and dimension audit for V96."""
import sympy as sp
r,omega,n,q,m,gamma,B,db,z,dr,dx=sp.symbols('r omega n q m gamma B db z dr dx',positive=True,real=True)
# circular radial restoring coefficient f(r)= vphi^2/r+q*vphi*B(r)/(gamma*m)
v=r*omega
# At fixed canonical angular momentum around a reference circular orbit d(vphi)/dr=0
# force variation f'(r0)=-omega^2 + q*v/(gamma*m)*dB/dr
expr=-omega**2+q*v*db/(gamma*m)
subs={q*B/(gamma*m):-omega,db:-n*B/r}
radial=sp.simplify(expr.subs(db,-n*B/r).subs(q,-omega*gamma*m/B))
vertical=sp.simplify((-q*v*db/(gamma*m)).subs(db,-n*B/r).subs(q,-omega*gamma*m/B))
# vertical a_z = - q vphi B_r/(gamma*m) with B_r=z dB/dr ; coefficient is this expression
assert sp.simplify(radial+omega**2*(1-n))==0,radial
assert sp.simplify(vertical+n*omega**2)==0,vertical
assert sp.simplify((1-n)+n-1)==0
# Unit algebra [M,L,T,Q] (charge rather than current); convert Q=I*T if needed.
dims={'m':(1,0,0,0),'v':(0,1,-1,0),'r':(0,1,0,0),
      'omega':(0,0,-1,0),'B':(1,0,-1,-1),'q':(0,0,0,1),
      'F':(1,1,-2,0),'J':(1,2,-2,0),'mu0':(1,1,0,-2),
      'dBdr':(1,-1,-1,-1),'n':(0,0,0,0),
      'I':(0,0,-1,1),'Jcurrent':(0,-2,-1,1),
      'resistivity':(1,3,-1,-2),'P':(1,2,-3,0),
      'c':(0,1,-1,0),'eps0':(-1,-3,2,2)}

def dprod(*args):return tuple(sum(x[i] for x in args) for i in range(4))
def dm(d,k):return tuple(k*x for x in d)
checks={
 'Lorentz q v B = force':(dprod(dims['q'],dims['v'],dims['B']),dims['F']),
 'q B /(gamma m) = angular velocity':(dprod(dims['q'],dims['B'],dm(dims['m'],-1)),dims['omega']),
 'n = r Bgradient / B':(dprod(dims['r'],dims['dBdr'],dm(dims['B'],-1)),dims['n']),
 'centripetal m v2/r = force':(dprod(dims['m'],dm(dims['v'],2),dm(dims['r'],-1)),dims['F']),
 'magnetic energy B2 volume/mu0':(dprod(dm(dims['B'],2),dm(dims['r'],3),dm(dims['mu0'],-1)),dims['J']),
 'current density I/area':(dprod(dims['I'],dm(dims['r'],-2)),dims['Jcurrent']),
 'J dot E volume = power':(dprod(dm(dims['Jcurrent'],2),dims['resistivity'],dm(dims['r'],3)),dims['P']),
 'omega2 = beta oscillation coefficient':(dm(dims['omega'],2),(0,0,-2,0)),
 'radiation power q2 a2 /(eps0 c3)':(dprod(dm(dims['q'],2),dm(dims['r'],2),dm(dims['omega'],4),dm(dims['eps0'],-1),dm(dims['c'],-3)),dims['P']),
 'known-false B = omega':(dims['B'],dims['omega']),
 'known-false G = c*kappa':((-1,3,-2,0),(0,0,-1,0))
}
for name,(left,right) in checks.items():
    if 'known-false' in name:
        assert left!=right, name
    else:assert left==right,(name,left,right)
if __name__=='__main__':
    print('Symbolic checks: radial',radial,'vertical',vertical)
    for name,(left,right) in checks.items(): print('PASS_EXPECTED_MISMATCH' if 'known-false' in name else 'PASS',name,left,right)
