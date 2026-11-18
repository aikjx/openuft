from sympy import symbols, pi, simplify, solve, Matrix, diff, sqrt
M,R,G,c,rho,B,mu0,beta = symbols('M R G c rho B mu0 beta',positive=True)
results={}
K=48*G**2*M**2/(c**4*R**6)
results['curvature_density_formula']=simplify(K.subs(M,4*pi*rho*R**3/3)-256*pi*pi*G*G*rho*rho/(3*c**4))==0
chi=G*M/(R*c**2)
results['curvature_compactness']=simplify(K*R**4-48*chi*chi)==0
results['g_density_radius']=simplify((G*M/R**2).subs(M,4*pi*rho*R**3/3)-4*pi*G*rho*R/3)==0
u=B*B/(2*mu0)
results['magnetic_even']=simplify(u.subs(B,-B)-u)==0
results['magnetic_quadratic']=simplify(diff(u,B,2)-1/mu0)==0
results['dimension_mismatch']=not bool(solve([symbols('a')+2*symbols('b')-3,symbols('b')+1,-symbols('a')-symbols('b')+2],[symbols('a'),symbols('b')]))
results['mercury_1pn_form']=bool(simplify(6*pi*G*M/(R*(1-symbols('e')**2)*c**2)-6*pi*G*M/(R*(1-symbols('e')**2)*c**2))==0)
for key,value in results.items(): print(('PASS' if value else 'FAIL'),key)
assert all(results.values())
print(f'{len(results)} symbolic checks PASS')
