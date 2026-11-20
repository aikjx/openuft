"""Exact symbolic audits, independent of float engine; exit nonzero on failure."""
import sympy as sp

x,r,R,h,G,M,c,hh,m,g,t,alpha,lamb,a=sp.symbols('x r R h G M c hbar m g t alpha lambda a',positive=True, real=True)
I=sp.I
checks={}
def check(name,expr):
    s=sp.simplify(expr)
    if s!=0: raise AssertionError(f'{name}: {s}')
    checks[name]='PASS'

# 1-2: Einstein Newtonian sector, linearized metric and harmonic trace reverse
Phi=sp.Function('Phi')(x)
h00=-2*Phi/c**2;hij=-2*Phi/c**2
trace=-h00+3*hij
bar_h00=h00+trace/2 # eta00=-1
check('metric_trace_reverse_00',bar_h00+4*Phi/c**2)
G00_lin=-sp.diff(bar_h00,x,2)/2
check('linearized_Einstein_Poisson_1D',G00_lin-2*sp.diff(Phi,x,2)/c**2)
check('metric_geodesic_Newton_limit',-c**2*(-sp.diff(-1-2*Phi/c**2,x)/2)+sp.diff(Phi,x))

# 4-5: KG rest-frequency cancellation + Schrodinger coefficient
omega=m*c**2/hh
q=sp.Function('psi')(x,t)
full=-(1/c**2)*sp.diff(sp.exp(-I*omega*t)*q,t,2)+sp.diff(sp.exp(-I*omega*t)*q,x,2)-(m*c/hh)**2*sp.exp(-I*omega*t)*q
kg_reduced=sp.simplify(sp.expand(full/sp.exp(-I*omega*t)))
check('Klein_Gordon_nonrel_expansion',kg_reduced-(2*I*m/hh*sp.diff(q,t)+sp.diff(q,x,2)-sp.diff(q,t,2)/c**2))
check('KG_Schrodinger_limit',sp.expand((hh**2/(2*m))*(kg_reduced+sp.diff(q,t,2)/c**2)-I*hh*sp.diff(q,t)-hh**2*sp.diff(q,x,2)/(2*m)))

# 6-7: exact accelerating frame/unitary map: free -> uniform gravity.
y=x+g*t**2/sp.Integer(2)
S=-m*g*x*t-m*g**2*t**3/sp.Integer(6)
free=sp.Function('f')(y,t)
Psi=sp.exp(I*S/hh)*free
res=I*hh*sp.diff(Psi,t)+(hh**2/(2*m))*sp.diff(Psi,x,2)-m*g*x*Psi
pred=sp.exp(I*S/hh)*(I*hh*sp.Subs(sp.Derivative(sp.Function('f')(sp.Symbol('Y'),t),t),sp.Symbol('Y'),y) + hh**2/(2*m)*sp.Subs(sp.Derivative(sp.Function('f')(sp.Symbol('Y'),t),sp.Symbol('Y'),2),sp.Symbol('Y'),y))
# Direct comparison by applying the free equation to f, replacing time and space derivatives with symbols via independent chain rule.
ft,fyy,fy,ff=sp.symbols('f_t f_yy f_y f')
r_known=sp.expand(res/sp.exp(I*S/hh)).subs({sp.Derivative(free,(x,2)): fyy,sp.Derivative(free,t):ft,sp.Derivative(free,x):fy,free:ff})
# Sympy may store Subs derivatives rather than ordinary Derivatives; map to formal placeholders.
r_known=sp.expand(r_known).replace(lambda z:isinstance(z,sp.Subs) and isinstance(z.expr,sp.Derivative),
                                    lambda z: ft if (z.expr.variables==(t,)) else (fyy if len(z.expr.variables)==2 else fy))
r_known=sp.simplify(r_known)
# More robust scalar verification using a free plane wave f=exp(i(k y - omega t)), omega= hbar k^2/(2m).
k=sp.symbols('k',real=True)
Psi_plane=sp.exp(I*S/hh)*sp.exp(I*(k*y-hh*k**2*t/(2*m)))
check('uniform_gravity_free_wave_unitary',sp.simplify((I*hh*sp.diff(Psi_plane,t)+hh**2/(2*m)*sp.diff(Psi_plane,x,2)-m*g*x*Psi_plane)/Psi_plane))

# 8: independent proper-time point particle action: weak field and low velocity
v2,eps,phi0=sp.symbols('v2 eps phi0',real=True)
# Insert Phi/c² -> eps*phi0 and v²/c² -> eps*v2, expand square root.
L_series=sp.series(-m*c**2*sp.sqrt(1+eps*(2*phi0-v2)),eps,0,2).removeO()
check('proper_time_action_Newton_Lagrangian',sp.diff(L_series,eps).subs(eps,0)+m*c**2*phi0-m*c**2*v2/2)

# 8-10: Newtonian spherical phase and exact normalized geometry
pot=lambda z:-G*M/z
check('spherical_potential_difference',pot(R+h)-pot(R)-G*M*h/(R*(R+h)))
ratio=sp.simplify((pot(R+h)-pot(R))/((G*M/R**2)*h))
check('quantum_phase_shape_ratio',ratio-R/(R+h))
check('relative_phase_gradient',sp.diff(ratio,h)+R/(R+h)**2)

# 11-12: finite-range interaction and shape
V=-G*M/r*(1+alpha*sp.exp(-r/lamb))
gmod=G*M/r**2*(1+alpha*(1+r/lamb)*sp.exp(-r/lamb))
check('Yukawa_acceleration_from_potential',sp.diff(V,r)-gmod)
Q=1+alpha*(r/lamb)**2*sp.exp(-r/lamb)/(2*(1+alpha*(1+r/lamb)*sp.exp(-r/lamb)))
check('Yukawa_shape_Q',-r*sp.diff(gmod,r)/(2*gmod)-Q)

# 13: Gaussian radial potential derivative vs enclosed mass
Phi_gauss=-G*M*sp.erf(r/a)/r
Mencl=M*(sp.erf(r/a)-2*r/(a*sp.sqrt(sp.pi))*sp.exp(-(r/a)**2))
check('Gaussian_gradient_Poisson',sp.diff(Phi_gauss,r)-G*Mencl/r**2)
# 14: Gaussian center limit
check('Gaussian_center_regular',sp.limit(Phi_gauss,r,0)+2*G*M/(sp.sqrt(sp.pi)*a))
# 15: Gaussian density normalization
rho=M/(sp.pi**sp.Rational(3,2)*a**3)*sp.exp(-r**2/a**2)
check('Gaussian_mass_normalization',sp.integrate(4*sp.pi*r**2*rho,(r,0,sp.oo))-M)
# 16-17: SN Gaussian extremum and virial
E=3*hh**2/(4*m*a**2)-G*m**2/(sp.sqrt(2*sp.pi)*a)
a_star=3*sp.sqrt(2*sp.pi)*hh**2/(2*G*m**3)
check('SN_Gaussian_extremum',sp.diff(E,a).subs(a,a_star))
check('SN_Gaussian_virial', (3*hh**2/(4*m*a_star**2))-G*m**2/(2*sp.sqrt(2*sp.pi)*a_star))
# 18-19: dimensional/Planck and G-M degeneracy
ell2=hh*G/c**3
mP2=hh*c/G
check('Planck_length_mass_identity',sp.simplify(ell2*mP2-hh**2/c**2))
acc=G*M/R**2; phase=G*M*h/(R*(R+h))
J=sp.diff(acc,G)*sp.diff(phase,M)-sp.diff(acc,M)*sp.diff(phase,G)
check('G_mass_jacobian_zero',J)
# 20: local phase rephasings cancel in two-body entanglement invariant
p00,p01,p10,p11,u0,u1,v0,v1=sp.symbols('p00 p01 p10 p11 u0 u1 v0 v1')
chi=(p00+u0+v0)+(p11+u1+v1)-(p01+u0+v1)-(p10+u1+v0)
check('entanglement_phase_local_gauge_invariant',chi-(p00+p11-p01-p10))

if __name__=='__main__':
    import json
    print(json.dumps({'total':len(checks),'checks':checks},indent=2,ensure_ascii=False))
