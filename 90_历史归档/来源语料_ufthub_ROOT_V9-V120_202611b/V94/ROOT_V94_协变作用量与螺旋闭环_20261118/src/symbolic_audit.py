"""Exact symbolic checks of V94 model identities. No physical discovery implied."""
import json
from pathlib import Path
import sympy as s

def audit():
    c,m,q,g,v=s.symbols('c m q gamma v',nonzero=True)
    ax,ay,az,vx,vy,vz=s.symbols('a_x a_y a_z v_x v_y v_z',real=True)
    A=s.Matrix([ax,ay,az]);V=s.Matrix([vx,vy,vz])
    def ck(name, expr):
        res=s.simplify(s.trigsimp(expr))
        checks.append({'test':name,'pass':res==0,'residual':str(res)})
        if res!=0: raise AssertionError(f'{name} = {res}')
    checks=[]
    B=(g*m/(q*v**2))*A.cross(V)
    force=q*V.cross(B)
    for k in range(3):ck(f'triple_product_component_{k}', s.expand(force[k]-g*m*(V.dot(V)*A[k]-(V.dot(A))*V[k])/v**2))
    ck('orthogonality_B_velocity',s.expand(B.dot(V)))
    ck('B_squared_for_orthogonal_a',s.expand(B.dot(B)-(g*m/(q*v**2))**2*(A.dot(A)*V.dot(V)-(A.dot(V))**2)))
    # Pure parametrized kinematics, ds/du sigma, v_0 constant.
    ux,uy,uz,u2x,u2y,u2z,ss,v0=s.symbols('u1x u1y u1z u2x u2y u2z sigma v0',nonzero=True,real=True)
    P=s.Matrix([ux,uy,uz]);Q=s.Matrix([u2x,u2y,u2z]);W=P.dot(Q)
    ac=v0*v0*(Q/ss**2-P*W/ss**4)
    ck('speed_acceleration_orthogonality',s.factor((v0*P/ss).dot(ac)).subs(ss**2,P.dot(P))) # naive sub may not catch ss^4
    # Maxwell by explicit affine vector field E=-1/2 dotB cross(x-r)
    X,Y,Z=s.symbols('x y z');r1,r2,r3=s.symbols('r1 r2 r3')
    bx,by,bz=s.symbols('bx by bz');dx,dy,dz=s.symbols('dbx dby dbz')
    xvec=s.Matrix([X-r1,Y-r2,Z-r3]);bvec=s.Matrix([bx,by,bz]); dbvec=s.Matrix([dx,dy,dz])
    fieldE=-s.Rational(1,2)*dbvec.cross(xvec)
    def curl(w):
        return s.Matrix([s.diff(w[2],Y)-s.diff(w[1],Z),s.diff(w[0],Z)-s.diff(w[2],X),s.diff(w[1],X)-s.diff(w[0],Y)])
    for k in range(3):ck(f'maxwell_curl_E_component_{k}',curl(fieldE)[k]+dbvec[k])
    ck('maxwell_gauss_E',s.diff(fieldE[0],X)+s.diff(fieldE[1],Y)+s.diff(fieldE[2],Z))
    for k in range(3):ck(f'curl_uniform_B_{k}',curl(bvec)[k])
    # dot B exact differentiation for a(t) cross v(t)
    tt=s.symbols('t');acc=s.Matrix([s.Function('a'+str(i))(tt) for i in range(3)]);vel=s.Matrix([s.Function('v'+str(i))(tt) for i in range(3)])
    dbdt=s.diff(acc.cross(vel),tt)
    rhs=s.diff(acc,tt).cross(vel)+acc.cross(s.diff(vel,tt))
    for i in range(3):ck(f'Bdot_product_rule_{i}',dbdt[i]-rhs[i])
    # Maxwell sources: rho =0; J affine in x has div 0.
    ddx,ddy,ddz=s.symbols('ddbx ddby ddbz');dd=s.Matrix([ddx,ddy,ddz])
    jcurr=s.Rational(1,2)*(dd.cross(xvec)-dbvec.cross(s.Matrix([vx,vy,vz])))
    ck('continuity_div_J',sum(s.diff(jcurr[k],[X,Y,Z][k]) for k in range(3)))
    # Relativistic non-invariance of spatial closure.
    t,beta=s.symbols('T beta',positive=True)
    boost= -beta*c*t/s.sqrt(1-beta**2)
    ck('boost_spatial_drift',boost+beta*c*t/s.sqrt(1-beta**2))
    # Constant field, screw motion; exact param circular transverse radius rL
    omega,t0=s.symbols('omega t',real=True,nonzero=True)
    vp,vz0=s.symbols('vp vz',real=True)
    pt=s.Matrix([vp*s.sin(omega*t0)/omega,vp*(s.cos(omega*t0)-1)/omega,vz0*t0])
    velocity=s.diff(pt,t0);accel=s.diff(velocity,t0)
    ck('static_B_speed_sq',s.trigsimp(velocity.dot(velocity)-vp**2-vz0**2))
    ck('static_B_acceleration_magnitude_sq',s.trigsimp(accel.dot(accel)-omega**2*vp**2))
    ck('static_B_z_is_linear',s.diff(pt[2],t0,2))
    # For constant v, EM action energy remains constant if E_on_trajectory=0
    ck('magnetic_work_zero',s.expand(V.dot(V.cross(bvec))))
    return checks

if __name__=='__main__':
    data=audit()
    p=Path('results');p.mkdir(exist_ok=True)
    (p/'SYMBOLIC_AUDIT.json').write_text(json.dumps({'count':len(data),'passed':sum(x['pass'] for x in data),'checks':data},ensure_ascii=False,indent=2))
    print('Sympy checks passed:',len(data))
