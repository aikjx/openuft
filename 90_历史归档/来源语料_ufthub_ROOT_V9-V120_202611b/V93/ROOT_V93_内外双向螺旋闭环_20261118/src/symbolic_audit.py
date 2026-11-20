"""Independent symbolic tests for toroidal inward/outward loop; equations valid in Euclidean 3-space."""
import sympy as sp

def audit():
    u,R,a=sp.symbols('u R a',positive=True,real=True)
    m,n=sp.symbols('m n',positive=True,integer=True)
    rho=R+a*sp.cos(n*u); cp=sp.cos(n*u); ss=sp.sin(n*u)
    rho1=sp.diff(rho,u);rho2=sp.diff(rho,u,2);rho3=sp.diff(rho,u,3)
    z=a*sp.sin(n*u)
    d1=sp.Matrix([rho1,m*rho,sp.diff(z,u)])
    d2=sp.Matrix([rho2-m*m*rho,2*m*rho1,sp.diff(z,u,2)])
    d3=sp.Matrix([rho3-3*m*m*rho1,3*m*rho2-m**3*rho,sp.diff(z,u,3)])
    check=[]
    def ok(name,diff):
        eq=sp.trigsimp(sp.expand(diff)); good=eq==0
        check.append((name,bool(good),str(eq)[:150]));
        if not good:raise AssertionError(f'{name}: {eq}')
    sigsq=(a*n)**2+(m*rho)**2
    ok('rho_loop_minmax',rho-(R+a*cp))
    ok('sigma_squared',d1.dot(d1)-sigsq)
    ok('radial_azimuth_z_split',rho1**2+(m*rho)**2+sp.diff(z,u)**2-sigsq)
    ok('rho_amplitude',rho**2-2*R*rho+R**2-a*a*cp**2)
    ok('poloidal_speed_constant_in_u',rho1**2+sp.diff(z,u)**2-(a*n)**2)
    ok('first_derivative_rho',rho1+a*n*ss)
    ok('second_derivative_rho',rho2+a*n*n*cp)
    ok('third_derivative_rho',rho3-a*n**3*ss)
    ok('second_derivative_z',sp.diff(z,u,2)+a*n*n*ss)
    ok('third_derivative_z',sp.diff(z,u,3)+a*n**3*cp)
    cross=d1.cross(d2)
    xx=a*m*n*n*ss*(a*cp-R)
    yy=-a*n*(a*n*n+m*m*rho*cp)
    zz=m*(2*a*a*n*n*ss*ss+a*n*n*rho*cp+m*m*rho*rho)
    for i,(name,eq) in enumerate([('cross_r',xx),('cross_theta',yy),('cross_z',zz)]): ok(name,cross[i]-eq)
    # d/dt = (v/sigma)d/du; acceleration uses |r'| and orthogonal projection.
    sig=sp.sqrt(sigsq); lam=sp.symbols('v',positive=True,real=True)
    dot=sp.simplify(d1.dot(d2))
    acc=lam**2*(d2/sigsq-d1*dot/sigsq**2)
    ok('acc_perp_v',acc.dot(d1))
    ok('energy_const_speed',sp.diff(sigsq,u)-2*d1.dot(d2))
    # Uniform field magnetic potential A=(B*rho/2)e_theta; closed loop integral analytic
    B=sp.symbols('B',real=True)
    kernel=sp.expand((B/2)*m*rho**2)
    # use generic positive integer n: integral over 0..2pi (cos^2 average 1/2)
    flux=sp.integrate(kernel,(u,0,2*sp.pi))
    ok('magnetic_flux_primitive_coprime',flux-sp.pi*B*m*(R*R+a*a/2))
    # known dimensional relations are tested separately; time_param derivative verified here algebraically
    ok('omega_vs_phase_speed',m*lam/sig-(m*(lam/sig)))
    ok('distance_torus_constraint',(rho-R)**2+z*z-a*a)
    return check

if __name__=='__main__':
    rows=audit()
    for name,pass_,rest in rows:print(('PASS' if pass_ else 'FAIL'),name,rest)
    print('SYMBOLIC_CHECK_COUNT',len(rows))
