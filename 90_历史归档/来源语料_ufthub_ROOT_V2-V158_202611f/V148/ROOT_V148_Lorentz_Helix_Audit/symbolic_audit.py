"""Exact algebraic verification with SymPy; not a validation of physical ROOT assumptions."""
import sympy as s
from pathlib import Path
from datetime import date

def audit():
    t=s.symbols('t', real=True)
    a,w,u=s.symbols('a omega u', positive=True,real=True)
    b=s.symbols('beta',real=True)
    pos=s.Matrix([a*s.cos(w*t),a*s.sin(w*t),u*t]);v=pos.diff(t);acc=v.diff(t);jerk=acc.diff(t)
    v2=s.trigsimp(v.dot(v)); a2=s.trigsimp(acc.dot(acc));cross2=s.trigsimp(v.cross(acc).dot(v.cross(acc)))
    assert s.simplify(v2-(a*a*w*w+u*u))==0
    assert s.simplify(a2-a*a*w**4)==0
    assert s.simplify(cross2-a*a*w**4*v2)==0
    numerator=s.trigsimp(v.dot(acc.cross(jerk)))
    assert s.simplify(numerator-a*a*u*w**5)==0
    assert s.simplify(numerator/cross2-u*w/v2)==0
    assert s.simplify((a*a*w**4+u*u*w*w)-w*w*v2)==0
    # Lorentz boost under a boost along the axial direction.
    D=(1-b*u)/s.sqrt(1-b*b)
    wp=w/D;up=(u-b)/(1-b*u)
    assert s.simplify((a*a*wp*wp+up*up-1).subs(a*a*w*w,1-u*u))==0
    assert s.simplify(D*wp-w)==0
    assert s.simplify(up.subs(b,u))==0
    assert s.simplify(D.subs(b,u)**2-(1-u*u))==0
    assert s.simplify(D/(1/D)-D*D)==0
    # Pure SO(3) connection has zero Maurer-Cartan curvature.
    x,y=s.symbols('x y',real=True)
    Rz=s.Matrix([[s.cos(x),-s.sin(x),0],[s.sin(x),s.cos(x),0],[0,0,1]])
    Ry=s.Matrix([[s.cos(y),0,s.sin(y)],[0,1,0],[-s.sin(y),0,s.cos(y)]])
    R=Rz*Ry
    X=s.trigsimp(R.T*R.diff(x));Y=s.trigsimp(R.T*R.diff(y))
    F=s.trigsimp(Y.diff(x)-X.diff(y)+X*Y-Y*X)
    assert all(s.trigsimp(entry)==0 for entry in F)
    # Maxwell wave: helicity +1, propagation along +z.
    z,k=s.symbols('z k',real=True)
    phase=k*(t-z)
    E=s.Matrix([s.cos(phase),s.sin(phase),0]);B=s.Matrix([-s.sin(phase),s.cos(phase),0])
    curlE=s.Matrix([-E[1].diff(z),E[0].diff(z),0])
    curlB=s.Matrix([-B[1].diff(z),B[0].diff(z),0])
    assert all(s.trigsimp(v)==0 for v in (B.diff(t)+curlE))
    assert all(s.trigsimp(v)==0 for v in (curlB-E.diff(t)))
    assert s.trigsimp(E.dot(B))==0
    assert s.trigsimp(E.dot(E)-B.dot(B))==0
    # Single smooth scalar theta gives identically F=d(d theta)=0.
    theta=s.sin(x*y)+x*x*y
    assert s.simplify(s.diff(s.diff(theta,x),y)-s.diff(s.diff(theta,y),x))==0
    return 17

if __name__=='__main__':
    print(f'SymPy exact audits: {audit()}/17 PASSED')
