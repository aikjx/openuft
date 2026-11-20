"""Exact SymPy certificates for mathematical identities (not physical evidence)."""
import sympy as s

def run():
    checks={}
    vx,vy,vz,bx,by,bz=s.symbols('vx vy vz bx by bz',real=True)
    v=s.Matrix([vx,vy,vz]); b=s.Matrix([bx,by,bz]); I=s.eye(3)
    cross=s.Matrix([[0,-vz,vy],[vz,0,-vx],[-vy,vx,0]])
    checks['cross matrix']=s.simplify(cross*b-v.cross(b))==s.zeros(3,1)
    de=-v.cross(b); checks['Lorentz field null direction']=s.simplify(de+v.cross(b))==s.zeros(3,1)
    v2=s.Matrix(s.symbols('wx wy wz',real=True));dv=v2-v
    checks['2-probe invisible B parallel dv']=s.simplify((v.cross(dv)+(-v.cross(dv))))==s.zeros(3,1) and s.simplify((v2-v).cross(dv))==s.zeros(3,1)
    R,v0,u,c=s.symbols('R v0 u c',positive=True)
    gb2=1/(1-u*u/c/c);gp2=1/(1-v0*v0/c/c)
    omega2=v0/R/s.sqrt(gb2)
    vp2=v0*v0/gb2+u*u
    k2=R*omega2**2/vp2
    proper_boost= s.simplify((1/(1-vp2/c**2))*vp2*k2)
    proper_before= gp2*v0*v0/R
    checks['proper acceleration boost invariant']=s.simplify(proper_boost-proper_before)==0
    kt,L=s.symbols('K L',positive=True)
    mean=kt/L
    checks['curvature variance decomposition']=s.simplify((s.Symbol('K2')/L-mean**2)+mean**2-s.Symbol('K2')/L)==0
    t=s.symbols('t',positive=True)
    def block(vx,vy,vz):
        return s.eye(3).row_join(s.Matrix([[0,-vz,vy],[vz,0,-vx],[-vy,vx,0]]))
    D1=block(0,0,0)
    D2=D1.col_join(block(t,0,0))
    D3=D2.col_join(block(0,t,0))
    checks['one distinct velocity rank3']=D1.rank()==3
    checks['two distinct velocities rank5']=D2.rank()==5
    checks['three nonparallel velocity differences rank6']=D3.rank()==6
    vs=s.symbols('vs',real=True)
    gg=(1-vs**2/c**2)**s.Rational(-1,2)
    checks['longitudinal gamma-cubed derivative']=s.simplify(s.diff(gg*vs,vs)-gg**3)==0
    # Dimensionally and analytically distinct: pointwise invertibility cannot be inferred from output geometry alone.
    invalid=[k for k,vv in checks.items() if not vv]
    print(f'SYMPY: {sum(checks.values())}/{len(checks)} checks passed: {list(checks)}')
    if invalid:raise RuntimeError('failed '+str(invalid))
if __name__=='__main__':run()
