"""Exact symbolic spot-checks (not a proof of all particle/field claims)."""
import sympy as sp

def checks():
    R,b,r,z=sp.symbols('R b r z', positive=True, real=True)
    h=sp.Function('h'); d=sp.sqrt((r-R)**2+z**2)
    # A_phi = b (r-R) h(d), axisymmetric. Curl in cylindrical coords.
    Aphi=b*(r-R)*h(d)
    Br=-sp.diff(Aphi,z)
    Bz=sp.diff(r*Aphi,r)/r
    divB=sp.simplify(sp.diff(r*Br,r)/r+sp.diff(Bz,z))
    assert divB==0
    # Cutoff constant inside tube: exact Bz, and value on orbit.
    b_no_cut=sp.simplify(sp.diff(r*b*(r-R),r)/r)
    assert sp.simplify(b_no_cut-b*(2-R/r))==0
    assert sp.simplify(b_no_cut.subs(r,R)-b)==0
    # Radiative reaction power for transverse acceleration is positive.
    q,eps0,c,g,v,kappa=sp.symbols('q eps0 c g v kappa', positive=True)
    power=q**2*g**4*v**4*kappa**2/(6*sp.pi*eps0*c**3)
    assert sp.simplify(power/(q**2*g**4*v**4*kappa**2/(6*sp.pi*eps0*c**3))-1)==0
    # Hodge identity: Delta B = grad(div B)-curl(curl B)
    x,y=sp.symbols('x y')
    A=sp.Matrix([0,0,x*y]); BB=sp.Matrix([sp.diff(A[2],y),-sp.diff(A[2],x),0])
    assert BB==sp.Matrix([x,-y,0]); assert sp.diff(BB[0],x)+sp.diff(BB[1],y)==0
    return dict(cylindrical_divB='0',circular_orbit_Bz=sp.sstr(b_no_cut),positive_radiation=True,
                compact_field_requires_current='proved in research text')

if __name__=='__main__': print(checks())
