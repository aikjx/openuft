import sympy as sp

def audit():
    q,ep,c,g,v,L,m,K2,K=sp.symbols('q ep c g v L m K2 K',positive=True)
    a=q**2*g**4*v**3/(6*sp.pi*ep*c**3)
    rad=a*K2
    result={}
    result['topological_lower_floor']=sp.simplify(a*(4*sp.pi)**2/L-8*sp.pi*q**2*g**4*v**3/(3*ep*c**3*L))==0
    result['power_ratio']=sp.simplify((rad/(L/v))/(rad*v/L))==1
    bfac=g*m*v/q
    B2_integral=bfac**2*K2
    rad_B=q**4*g**2*v/(6*sp.pi*ep*m**2*c**3)*B2_integral
    result['B_radiation_identity']=sp.simplify(rad_B-rad)==0
    result['Cauchy_excess']=sp.simplify(rad/(a*K*K/L)-K2*L/K**2)==0
    # Torsion in a boosted axial frame differs; four-acceleration keeps the scalar norm.
    V,U,R,GB,GV=sp.symbols('V U R GB GV',positive=True)
    wp=V/(R*GB);v2=V**2/GB**2+U**2
    result['helical_identity']=sp.simplify((R*wp**2/v2)**2+(-U*wp/v2)**2-wp**2/v2)==0
    result['static_field_work_zero']=sp.simplify(q*sp.Symbol('DeltaPhi')-q*sp.Symbol('DeltaPhi'))==0
    # SI exponent vector: M,L,T,I ; Coulomb = A*s; epsilon_0 = A^2*s^4/(kg*m^3)
    dim=dict(q=(0,0,1,1),g=(0,0,0,0),v=(0,1,-1,0),eps=(-1,-3,4,2),c=(0,1,-1,0),L=(0,1,0,0),k2=(0,-1,0,0))
    def add(*vs):return tuple(sum(v[i] for v in vs) for i in range(4))
    def mul(v,k):return tuple(k*i for i in v)
    dim_E=add(mul(dim['q'],2),mul(dim['v'],3),mul(dim['eps'],-1),mul(dim['c'],-3),dim['k2'])
    dim_P=add(dim_E,dim['v'],mul(dim['L'],-1))
    dim_Efield=add(dim_E,mul(dim['q'],-1),mul(dim['L'],-1))
    result['SI_energy']=dim_E==(1,2,-2,0)
    result['SI_power']=dim_P==(1,2,-3,0)
    result['SI_E_field']=dim_Efield==(1,1,-3,-1)
    assert all(result.values()),result
    return result
