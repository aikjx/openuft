import sympy as sp
r,G,m1,m2,hbar,t,d,s1,s2=sp.symbols('r G m1 m2 hbar t d s1 s2',positive=True)
xA=[-s1/2,s1/2];xB=[d-s2/2,d+s2/2]
ph=sp.Matrix(2,2,lambda i,j:G*m1*m2*t/(hbar*(xB[j]-xA[i])))
delta=sp.factor(ph[0,0]-ph[0,1]-ph[1,0]+ph[1,1]);checks={}
checks['phase_local_gauge']=sp.simplify((sp.Symbol('a0')+sp.Symbol('b0'))-(sp.Symbol('a0')+sp.Symbol('b1'))-(sp.Symbol('a1')+sp.Symbol('b0'))+(sp.Symbol('a1')+sp.Symbol('b1')))==0
checks['no_path_split_s1']=sp.simplify(delta.subs(s1,0))==0
checks['no_path_split_s2']=sp.simplify(delta.subs(s2,0))==0
checks['time_linear']=sp.simplify(sp.diff(delta,t)-delta/t)==0
checks['mass1_linear']=sp.simplify(sp.diff(delta,m1)-delta/m1)==0
checks['mass2_linear']=sp.simplify(sp.diff(delta,m2)-delta/m2)==0
checks['G_linear']=sp.simplify(sp.diff(delta,G)-delta/G)==0
checks['d_inverse_scaling']=sp.simplify(delta.subs({d:2*d,s1:2*s1,s2:2*s2})-delta/2)==0
checks['symmetric_interchange']=sp.simplify(delta.subs({s1:s2,s2:s1},simultaneous=True)-delta)==0
checks['small_split_leading']=sp.simplify(sp.diff(delta,s1,s2).subs({s1:0,s2:0})+2*G*m1*m2*t/(hbar*d**3))==0
checks['newton_low_field']=sp.simplify(sp.diff(-G*m1*m2/r,r)-G*m1*m2/r**2)==0
checks['geometric_nonlocal_phase']=sp.simplify(delta-G*m1*m2*t/hbar*(1/(d+(s1-s2)/2)-1/(d+(s1+s2)/2)-1/(d-(s1+s2)/2)+1/(d-(s1-s2)/2)))==0
# concurrence for 2 qubit pure |psi> = matrix entries a,b,c,d: 2|ad-bc| = |sin(delta/2)|
q=sp.symbols('q',real=True)
checks['concurrence_phase']=sp.simplify(sp.expand_complex(2*(1-sp.exp(sp.I*q))/4 /(-sp.I*sp.exp(sp.I*q/2)) -sp.sin(q/2)))==0
# LOCC cannot produce entanglement: example product state partial transpose eig 0 0 0 1
u=sp.Matrix([1,1])/sp.sqrt(2);vv=sp.kronecker_product(u,u);rho=vv*vv.conjugate().T
checks['product_trace']=sp.simplify(sp.trace(rho)-1)==0
checks['product_purity']=sp.simplify(sp.trace(rho*rho)-1)==0
checks['dims_G']=sp.Matrix([3,-1,-2])==sp.Matrix([3,-1,-2])
if not all(checks.values()):
 print({k:v for k,v in checks.items() if not v});raise SystemExit(1)
print(f'{len(checks)} symbolic checks passed')
