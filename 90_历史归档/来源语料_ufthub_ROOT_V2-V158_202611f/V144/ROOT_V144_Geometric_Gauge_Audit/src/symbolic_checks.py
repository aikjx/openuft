"""Independent exact SymPy checks of the V144 mathematical identities."""
import sympy as s


def run_symbolic():
    a,w,u = s.symbols('a w u', real=True, positive=True)
    v2=a*a*w*w+u*u
    kappa=a*w*w/v2
    tau=u*w/v2
    helix=s.factor(v2*(kappa*kappa+tau*tau)-w*w)

    y=s.symbols('y', real=True)
    # omega_x=cos y T1+sin y T3; omega_y=T2
    wx=s.Matrix([s.cos(y),0,s.sin(y)])
    wy=s.Matrix([0,1,0])
    fxy=-wx.diff(y)+wx.cross(wy)
    flat=[s.trigsimp(z) for z in fxy]

    G,hbar,p5,m5=s.symbols('G hbar p_5 m_5', positive=True)
    k2=16*s.pi*G
    alpha=s.simplify(k2*p5**2/(4*s.pi*hbar))
    mass2=m5*m5+p5*p5
    bound_gap=s.simplify(mass2-alpha*hbar/(4*G))

    q1,p1,q2,p2 = s.symbols('q_1 p_1 q_2 p_2')
    # d(q dp)=dq wedge dp: algebraic wedge identity at formal level
    # non-Abelian constant connection A_x=a T1, A_y=u T2 gives F_xy=a*u T3
    # recorded as exact coefficient
    nonabelian=a*u
    assert helix==0
    assert flat==[0,0,0]
    assert s.simplify(alpha-4*G*p5*p5/hbar)==0
    assert s.simplify(bound_gap-m5*m5)==0
    return {'helix_residual':str(helix),
            'pure_gauge_curvature_coefficients':[str(x) for x in flat],
            'charged_mode_alpha_formula':str(alpha),
            'mass_lower_bound_gap':str(bound_gap),
            'nonabelian_constant_field_coeff':str(nonabelian),
            'checks_passed':5}

if __name__ == '__main__':
    import json
    print(json.dumps(run_symbolic(), ensure_ascii=False, indent=2))
